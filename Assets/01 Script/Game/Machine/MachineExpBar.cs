// Thanh kinh nghiệm trên đầu máy bi (như thanh cấp trên máy tham khảo: vòng cấp bên trái, thanh EXP, "số/số").
// Bi rơi vào ô EXP thì sao EXP bay từ ô lên đầu phần đầy của thanh; tới nơi thanh mới cộng, loé tím, và cả khung thanh
// (rãnh vẽ tay cắt từ thân máy + thanh + chữ) nhún như thanh năng lượng của máy tham khảo. Thanh hiện chậm hơn bản lưu trong
// lúc sao còn bay (bản lưu cộng ngay lúc bi rơi). Lên cấp: thanh đầy rồi về 0, vòng cấp nhún, loé to.
// Prefab: phần "thanh_kinh_nghiem" của Screens/Machine, dựng bằng menu "PokiClash/Prefab/Máy bi/thanh kinh nghiệm";
// nhóm "khung_thanh" (rãnh + thanh) do menu "Máy bi: thân máy vẽ tay" dựng theo số đo rãnh.
// Sao và hạt là bản sao Items/HatMayBi trên lớp bay "lop_bay" phủ cả khối máy.
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class MachineExpBar : MonoBehaviour
    {
        [SerializeField] UiBar bar;
        [SerializeField] Image arc; // cung EXP quanh vòng cấp
        [SerializeField] TextMeshProUGUI lvText;
        [SerializeField] RectTransform badge; // vòng cấp
        [SerializeField] RectTransform flyLayer;
        [SerializeField] Image particle; // Items/HatMayBi
        [SerializeField] RectTransform frame; // "khung_thanh": rãnh vẽ tay + thanh, nhún cùng nhau (thiếu thì chỉ thanh nhún)

        // sao bay: FlyTime giây (thêm ngẫu nhiên tới FlyJitter), sao sau trễ FlyGap giây; tối đa MaxStars sao một lần rơi
        public const float FlyTime = 0.55f, FlyJitter = 0.12f, FlyGap = 0.06f, StarSize = 56, SoundGap = 0.07f;
        public const int MaxStars = 4;

        // chùm EXP (chủ dự án dặn 2026-11-19: "nhận kinh nghiệm phải toả ra, trễ một chút rồi tween lên mượt"): mọi viên phụt ra cùng
        // lúc theo hình quạt quanh điểm đi, hãm dần trong SprayOut giây (nảy cỡ 0,3 → 1,18 → 1); khựng lơ lửng SprayHold giây, viên
        // sau khựng lâu hơn SprayGap giây nên rời chùm lần lượt; rồi bay về đích theo đường cong nhẹ, nhanh dần rồi chậm lại (ease
        // in-out bậc ba) trong SprayFly giây, nhỏ dần còn 0,72, tới nơi mới cộng
        // 2026-11-21: phụt lâu hơn (0,34), lấy đà WindUp trước khi phóng, phóng 0,46 giây nhanh dần (tới nơi còn đà)
        public const float SprayOut = 0.34f, SprayHold = 0.12f, SprayGap = 0.05f, SprayFly = 0.46f, SprayFlyJitter = 0.08f, WindUp = 0.07f;
        // thanh chạy tới số mới: phần còn thiếu × FillRate mỗi giây, ít nhất FillMin thanh mỗi giây (thanh đầy dần, chữ số đếm lên);
        // lên cấp thì chạy đầy, nhún vòng cấp, về 0 rồi chạy tiếp
        public const float FillRate = 7f, FillMin = 0.9f;

        // nhún khi cộng: dáng chép thanh năng lượng của máy tham khảo (nền và phần đầy cùng phóng 1,2 → 1,08 → 1,2 → 1,08 → 1,2 → 1
        // trong 0,25 giây, chữ số phóng mạnh hơn). Thanh này dài nên biên độ chia theo trục: ngang PunchX, dọc PunchY, chữ thêm PunchText.
        // Không bao giờ nhỏ hơn 1, để bản rãnh nhún luôn che kín rãnh vẽ sẵn của thân máy bên dưới.
        public static readonly float[] PunchCurve = { 0, 1, 0.05f, 0.4f, 0.1f, 1, 0.15f, 0.4f, 0.2f, 0.7f, 0.25f, 0 };
        public const float PunchX = 0.03f, PunchY = 0.18f, PunchText = 0.12f;

        int level, exp; // đích của thanh (đã nhận)
        int dispLv; // đang hiện: cấp và EXP chạy dần tới đích
        float dispExp;
        int flying;
        bool bound;
        MachineFx fx;
        float bumpT = -1, popT = -1, lastSound = -1;
        int combo; // sao tới liền nhau: tiếng cao dần
        readonly List<Image> stars = new List<Image>(); // sao đang bay
        Vector3 badgeScale = Vector3.one;

        public bool Busy => flying > 0;
        // EXP đang nằm trên bảng số (MachineScoreBoard): bản lưu đã cộng nhưng thanh chưa nhận, nên thanh không theo kịp bản lưu
        public int Held;
        public Vector3 TipWorld => bar.TipWorld();

        static SaveData S => App.Save.Data;
        static BalanceConfig Cfg => App.Data.Cfg;

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiBar b, Image a, TextMeshProUGUI lv, RectTransform badgeRt, RectTransform layer, Image item)
        {
            bar = b;
            arc = a;
            lvText = lv;
            badge = badgeRt;
            flyLayer = layer;
            particle = item;
        }

        // Dùng khi nướng prefab (Editor): nhóm rãnh + thanh nhún cùng nhau.
        public void SetFrame(RectTransform f) => frame = f;

        public RectTransform Frame => frame;

        // nhún khung thanh (sao tới, hoặc công cụ thử)
        public void Punch() => bumpT = 0;

        // loé ở một điểm thế giới trên lớp bay (mốc quà của máy dùng): big = loé to như lên cấp
        public void Burst(Vector3 world, bool big)
        {
            if (!bound) return;
            fx.Emit(big ? LevelUp : Hit, Anch(world), 40);
        }

        // một icon bay từ from tới to (thế giới) theo đường cong trên lớp bay, trễ delay giây, tới nơi gọi arrive
        // (mốc quà của máy dùng cho bi quà bay về dòng đếm). Hạt lấy từ kho Items/HatMayBi như sao EXP.
        public void FlyIcon(Sprite sprite, Vector3 from, Vector3 to, float delay, System.Action arrive, float size = 44, float dur = 0.5f)
        {
            if (!bound)
            {
                arrive?.Invoke();
                return;
            }
            flying++;
            StartCoroutine(FlyIconRun(sprite, from, to, delay, arrive, size, dur));
        }

        IEnumerator FlyIconRun(Sprite sprite, Vector3 from, Vector3 to, float delay, System.Action arrive, float size, float dur)
        {
            var img = fx.Take(flyLayer);
            stars.Add(img);
            img.sprite = sprite;
            img.color = Color.white;
            img.enabled = false;
            var rt = img.rectTransform;
            rt.sizeDelta = Vector2.one * size;
            rt.localEulerAngles = Vector3.zero;
            img.preserveAspect = true;
            for (float w = 0; w < delay; w += Time.unscaledDeltaTime) yield return null;
            img.enabled = true;
            var a = Anch(from);
            var b = Anch(to);
            // đường bậc ba tham số đều: vọt mạnh lên khỏi điểm đi (tiếp tuyến đầu 3 × (c1 - a)), lượn rồi lao vào đích từ phía dưới
            // (tiếp tuyến cuối lớn, chạm đích dứt khoát) như icon bay của máy tham khảo
            float side = Random.Range(-1f, 1f);
            var c1 = a + new Vector2(side * 150, 240 + Random.Range(0, 100));
            var c2 = b + new Vector2(-side * 70, -150);
            float star = 0;
            for (float t = 0; t < dur; t += Time.unscaledDeltaTime)
            {
                float k = t / dur, m = 1 - k;
                var pos = m * m * m * a + 3 * m * m * k * c1 + 3 * m * k * k * c2 + k * k * k * b;
                rt.anchoredPosition = pos;
                rt.localScale = Vector3.one * (t < 0.067f ? Mathf.Lerp(0.3f, 1.5f, t / 0.067f) : t < 0.167f ? Mathf.Lerp(1.5f, 1f, (t - 0.067f) / 0.1f) : Mathf.Lerp(1f, 0.78f, (t - 0.167f) / Mathf.Max(0.01f, dur - 0.167f)));
                rt.localEulerAngles = new Vector3(0, 0, Mathf.Sin(k * Mathf.PI) * 25 * side);
                // vệt sáng mỗi khung (dài 0,11 giây), sao rắc mỗi 0,035 giây; icon luôn nằm trên vệt
                fx.Emit(MachineFx.FlyTrail, pos, size * 0.85f);
                if ((star += Time.unscaledDeltaTime) > 0.035f)
                {
                    star = 0;
                    fx.Emit(MachineFx.FlyStars, pos, size * 1.1f);
                }
                rt.SetAsLastSibling();
                yield return null;
            }
            Return(img);
            flying--;
            fx.Emit(Hit, b, 30);
            arrive?.Invoke();
        }

        // vào màn: hiện đúng bản lưu, không chạy
        Image tipGlow;
        RectTransform sweep;
        float sweepT, tipT;

        // lớp sáng của thanh (chép thanh cấp của máy tham khảo): quầng ở đầu phần đầy bừng lên khi nhận EXP, vệt sáng lia qua thanh
        void MakeLights()
        {
            if (tipGlow || !bar) return;
            var brt = (RectTransform)bar.transform;
            tipGlow = MachineGlow.Make("quang_dau", brt.parent, MachineGlow.Glow, MachineGlow.Hex("#e9d2ff", 0));
            if (tipGlow) tipGlow.rectTransform.sizeDelta = Vector2.one * brt.rect.height * 3f;
            var mrt = MachineGlow.NewMask("lia_thanh", brt);
            if (!mrt) return;
            mrt.Stretch();
            var sw = MachineGlow.Make("lia", mrt, MachineGlow.Sweep, MachineGlow.A(Color.white, 0.5f));
            if (sw)
            {
                sweep = sw.rectTransform;
                sweep.sizeDelta = new Vector2(brt.rect.height * 1.2f, brt.rect.height * 2.4f);
                sweep.localEulerAngles = new Vector3(0, 0, -25);
            }
        }

        public void Bind()
        {
            fx = new MachineFx(particle, flyLayer);
            MakeLights();
            badgeScale = badge ? badge.localScale : Vector3.one;
            flying = 0;
            bound = true;
            Show(S.level, S.exp, true);
        }

        // bản lưu đổi ngoài sao bay (mở rương ra EXP, bảng thử): theo kịp khi không còn sao nào đang bay
        public void Sync()
        {
            if (!bound || flying > 0 || Held > 0) return;
            if (level != S.level || exp != S.exp) Show(S.level, S.exp, false);
        }

        // đặt đích của thanh; instant thì hiện ngay, không thì Update cho thanh chạy tới (lên cấp: chạy đầy rồi về 0)
        void Show(int lv, int e, bool instant)
        {
            level = lv;
            exp = e;
            if (instant || lv < dispLv || (lv == dispLv && e < dispExp - 0.5f))
            {
                dispLv = lv;
                dispExp = e;
            }
            Paint();
        }

        // vẽ thanh theo số đang hiện
        void Paint()
        {
            int need = Progress.ExpToNext(dispLv, Cfg);
            bool max = dispLv >= Cfg.maxLevel;
            int shown = Mathf.Min(need, Mathf.RoundToInt(dispExp));
            bar.Set(max ? need : dispExp, need, 0, max ? Loc.T("Tối đa") : $"{shown}/{need}", true);
            if (arc) arc.fillAmount = max ? 1 : Mathf.Clamp01(dispExp / Mathf.Max(1, need));
            if (lvText) lvText.text = dispLv.ToString();
        }

        // thanh chạy tới đích: đầy dần, chữ số đếm lên; qua cấp thì chạy đầy, nhún vòng cấp, về 0
        void Tween(float dt)
        {
            if (dispLv == level && Mathf.Abs(dispExp - exp) < 0.01f) return;
            int need = Mathf.Max(1, Progress.ExpToNext(dispLv, Cfg));
            float goal = dispLv < level ? need : exp;
            float step = Mathf.Max(Mathf.Abs(goal - dispExp) * FillRate, need * FillMin) * dt;
            dispExp = Mathf.MoveTowards(dispExp, goal, step);
            if (dispLv < level && dispExp >= need - 0.01f)
            {
                dispLv++;
                dispExp = 0;
                LevelPop();
            }
            else if (dispLv == level && Mathf.Abs(dispExp - exp) < 0.01f) dispExp = exp;
            Paint();
        }

        // số viên của một chùm EXP n: 7..16 (người dùng 2026-11-21 "làm nhiều kinh nghiệm toả ra hơn"; trước 3..7). Viên nhiều hơn
        // EXP thì vài viên mang 0 (vẫn bay, tới nơi không cộng)
        public static int SprayCount(int n) => Mathf.Clamp(Mathf.RoundToInt(n * 1.1f) + 2, 7, 16);

        // chia n cho k phần gần đều (phần đầu nhận dư)
        public static int Part(int n, int k, int i) => n / k + (i < n % k ? 1 : 0);

        // n EXP bay từ điểm from (thế giới) lên thanh: chùm kẹo toả ra, khựng, rồi lần lượt bay mượt về đầu phần đầy
        public void Fly(Vector3 from, int n, float delay = 0)
        {
            if (!bound || n <= 0) return;
            int k = SprayCount(n);
            Spray(MachineScoreBoard.Candy, from, () => bar.TipWorld(), k, delay, i => Arrive(Part(n, k, i)));
        }

        // một chùm count icon từ from (thế giới) về to() (đích tính lại mỗi khung, vì đầu thanh chạy), trễ delay giây; viên thứ i tới
        // nơi thì gọi arrive(i). radius: tầm toả (px lớp bay)
        public void Spray(Sprite sprite, Vector3 from, System.Func<Vector3> to, int count, float delay, System.Action<int> arrive,
            float size = StarSize, float radius = 105)
        {
            if (count <= 0) return;
            if (!bound)
            {
                for (int i = 0; i < count; i++) arrive?.Invoke(i);
                return;
            }
            // 2026-11-21 (người dùng: "toả ra tween lên chưa đã, chưa rõ"): phụt như vòi nước theo quạt hướng lên (±105° quanh trục
            // đứng), loé mềm ở điểm đi; thứ tự rời chùm xáo trộn (không quét trái sang phải); chùm đông thì rời dày hơn
            radius *= Mathf.Lerp(1f, 1.35f, (count - 7) / 9f); // chùm đông toả rộng hơn cho kẹo khỏi chụm một cục
            StartCoroutine(PopAt(from, delay, radius));
            float gap = Mathf.Min(SprayGap, 0.6f / count);
            var order = new int[count];
            for (int i = 0; i < count; i++) order[i] = i;
            for (int i = count - 1; i > 0; i--)
            {
                int j = Random.Range(0, i + 1);
                (order[i], order[j]) = (order[j], order[i]);
            }
            for (int i = 0; i < count; i++)
            {
                flying++;
                float ang = 90 + Mathf.Lerp(-105, 105, (i + 0.5f) / count) + Random.Range(-10f, 10f);
                StartCoroutine(SprayOne(sprite, from, to, ang, radius * Random.Range(0.6f, 1f), delay + i * 0.008f,
                    SprayHold + order[i] * gap, i, arrive, size));
            }
        }

        // loé mềm, vòng sáng và kim tuyến ở điểm đi lúc chùm phụt ra
        IEnumerator PopAt(Vector3 from, float delay, float radius)
        {
            for (float w = 0; w < delay; w += Time.unscaledDeltaTime) yield return null;
            if (fx != null) fx.Emit(SprayPop, Anch(from), radius * 0.5f);
        }

        IEnumerator SprayOne(Sprite sprite, Vector3 from, System.Func<Vector3> to, float ang, float rad, float delay, float hold, int index,
            System.Action<int> arrive, float size)
        {
            // quầng sáng mềm cộng sáng sau kẹo (kẹo tím trên mặt bàn tím khó thấy, người dùng 2026-11-21 "chưa rõ")
            var halo = fx.Take(flyLayer);
            stars.Add(halo);
            halo.sprite = fx.Sprite(MachineGlow.Glow);
            halo.material = MachineGlow.Add;
            halo.preserveAspect = true;
            halo.enabled = false;
            var hrt = halo.rectTransform;
            hrt.sizeDelta = Vector2.one * size * 2.1f;
            hrt.localEulerAngles = Vector3.zero;
            hrt.localScale = Vector3.one;
            var img = fx.Take(flyLayer);
            stars.Add(img);
            img.sprite = sprite;
            img.preserveAspect = true;
            img.color = Color.white;
            img.enabled = false;
            var rt = img.rectTransform;
            rt.sizeDelta = Vector2.one * size;
            rt.localEulerAngles = Vector3.zero;
            rt.localScale = Vector3.zero;
            for (float w = 0; w < delay; w += Time.unscaledDeltaTime) yield return null;
            img.enabled = true;
            halo.enabled = halo.sprite;
            void Glow(Vector2 at, float a, float s)
            {
                hrt.anchoredPosition = at;
                hrt.localScale = Vector3.one * s;
                halo.color = new Color(1f, 0.88f, 1f, a);
            }

            // 1. phụt lên như vòi nước: ra nhanh, hãm dần (ease-out bậc ba) theo đường vồng lên; cỡ nảy 0,2 → 1,3 → 1; xoay rồi chậm lại
            var a = Anch(from);
            var dir = new Vector2(Mathf.Cos(ang * Mathf.Deg2Rad), Mathf.Sin(ang * Mathf.Deg2Rad));
            var p1 = a + new Vector2(dir.x, dir.y * 0.85f + 0.25f) * rad;
            float rot = Random.Range(-30f, 30f), spin = Random.Range(-1f, 1f) * 320;
            for (float t = 0; t < SprayOut; t += Time.unscaledDeltaTime)
            {
                float u = t / SprayOut, e = 1 - (1 - u) * (1 - u) * (1 - u);
                var p = Vector2.LerpUnclamped(a, p1, e) + new Vector2(0, Mathf.Sin(Mathf.Min(1, u * 1.15f) * Mathf.PI) * rad * 0.2f);
                rt.anchoredPosition = p;
                float s = u < 0.35f ? Mathf.Lerp(0.2f, 1.3f, u / 0.35f) : Mathf.Lerp(1.3f, 1, (u - 0.35f) / 0.65f);
                rt.localScale = Vector3.one * s;
                rot += spin * (1 - u) * Time.unscaledDeltaTime;
                rt.localEulerAngles = new Vector3(0, 0, rot);
                Glow(p, 0.8f * Mathf.Min(1, u * 3), s);
                hrt.SetAsLastSibling();
                rt.SetAsLastSibling();
                yield return null;
            }
            // 2. khựng: lơ lửng nhấp nhô, quầng thở, xoay dần về thẳng
            float ph = Random.Range(0f, 6.28f), rot0 = rot;
            for (float t = 0; t < hold; t += Time.unscaledDeltaTime)
            {
                var p = p1 + new Vector2(0, Mathf.Sin(t * 10 + ph) * 4f);
                rt.anchoredPosition = p;
                float s = 1 + 0.05f * Mathf.Sin(t * 14 + ph);
                rt.localScale = Vector3.one * s;
                rot = Mathf.Lerp(rot0, 0, Mathf.Clamp01(t / 0.25f));
                rt.localEulerAngles = new Vector3(0, 0, rot);
                Glow(p, 0.62f + 0.18f * Mathf.Sin(t * 9 + ph), s);
                yield return null;
            }
            // 3. phóng về đích: lấy đà (lùi nhẹ khỏi đích, phồng 1,15) rồi tăng tốc theo đường cong lệch về phía đã toả, nhỏ dần
            // 1,15 → 0,8; vệt sáng mềm dày và lấp lánh rắc theo
            var p2 = rt.anchoredPosition;
            float dur = SprayFly + Random.Range(0, SprayFlyJitter), trail = 0, spark = 0, rotS = rot;
            float side = dir.x >= 0 ? 1 : -1;
            var b = Anch(to());
            var back = (p2 - b).normalized * 14;
            for (float t = 0; t < WindUp; t += Time.unscaledDeltaTime)
            {
                float u = t / WindUp, e = Mathf.Sin(u * Mathf.PI * 0.5f);
                var p = p2 + back * e;
                rt.anchoredPosition = p;
                rt.localScale = Vector3.one * Mathf.Lerp(1, 1.15f, e);
                Glow(p, Mathf.Lerp(0.7f, 0.95f, e), 1.1f);
                yield return null;
            }
            p2 += back;
            for (float t = 0; t < dur; t += Time.unscaledDeltaTime)
            {
                float u = t / dur, e = u * u * (2.2f - 1.2f * u); // ra nhanh dần, tới nơi vẫn còn đà
                b = Anch(to());
                var d = b - p2;
                var c = (p2 + b) * 0.5f + new Vector2(-d.y, d.x).normalized * side * Mathf.Min(150, d.magnitude * 0.24f);
                var p = (1 - e) * (1 - e) * p2 + 2 * (1 - e) * e * c + e * e * b;
                rt.anchoredPosition = p;
                rt.localScale = Vector3.one * Mathf.Lerp(1.15f, 0.8f, e);
                rt.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(rotS, 0, e) + Mathf.Sin(u * Mathf.PI) * 14 * side);
                Glow(p, 0.95f, Mathf.Lerp(1.1f, 0.85f, e));
                if ((trail += Time.unscaledDeltaTime) > 0.02f)
                {
                    trail = 0;
                    fx.Emit(Trail, p, size * 0.5f);
                }
                if ((spark += Time.unscaledDeltaTime) > 0.07f && u > 0.1f)
                {
                    spark = 0;
                    fx.Emit(TrailSpark, p, size * 0.5f);
                }
                yield return null;
            }
            Return(halo);
            Return(img);
            flying--;
            fx.Emit(Hit, b, 34);
            arrive?.Invoke(index);
        }

        void Arrive(int n)
        {
            int need = Progress.ExpToNext(level, Cfg);
            int e = exp + n, lv = level;
            while (lv < Cfg.maxLevel && e >= need)
            {
                e -= need;
                lv++;
                need = Progress.ExpToNext(lv, Cfg);
            }
            if (lv >= Cfg.maxLevel) e = Mathf.Min(e, need);
            // sao cuối tới: lấy đúng bản lưu (phòng khi lệch do làm tròn hay EXP từ chỗ khác)
            if (flying == 0 && Held == 0)
            {
                lv = S.level;
                e = S.exp;
            }
            Show(lv, e, false);
            if (tipT < 0.2f) bumpT = 0; // viên tới liền nhau: không nhún lại khi nhún trước còn đang mạnh
            tipT = 0.35f;
            fx.Emit(Hit, Anch(bar.TipWorld()), 40);
            float now = Time.unscaledTime;
            combo = now - lastSound < 0.4f ? Mathf.Min(combo + 1, 8) : 0;
            if (now - lastSound >= SoundGap)
            {
                lastSound = now;
                App.Audio.Play("pick", 0.45f, 1.05f + combo * 0.04f);
            }
        }

        // bảng số đổ n EXP lên thanh (kẹo đã bay tới đầu thanh)
        public void Deposit(int n)
        {
            Held = Mathf.Max(0, Held - n);
            Arrive(n);
        }

        public event System.Action LeveledUp; // thanh vừa qua cấp (màn máy bi cho đèn vòm dồn vào giữa, GD_Claude/23)

        void LevelPop()
        {
            popT = 0;
            LeveledUp?.Invoke();
            if (badge) fx.Emit(LevelUp, Anch(badge.position), 40);
            App.Audio.Play("machineLevel", 0.8f);
            Haptics.Play(Haptic.LevelUp);
        }

        // điểm thế giới -> toạ độ neo góc trên trái của lớp bay (Items/HatMayBi neo góc trên trái)
        Vector2 Anch(Vector3 world)
        {
            var l = (Vector2)flyLayer.InverseTransformPoint(world);
            var r = flyLayer.rect;
            return new Vector2(l.x - r.xMin, l.y - r.yMax);
        }

        void Update()
        {
            // fx không qua được lần nạp lại script giữa lúc Play (bound thì có): coi như chưa gắn
            if (!bound || fx == null) return;
            float dt = Time.unscaledDeltaTime;
            fx.Update(dt);
            Tween(dt);
            if (tipGlow)
            {
                tipT -= dt;
                tipGlow.rectTransform.position = bar.TipWorld();
                tipGlow.color = MachineGlow.Hex("#e9d2ff", Mathf.Clamp01(tipT / 0.35f) * 0.9f);
            }
            if (sweep)
            {
                // lia qua mỗi 3 giây trong 0,6 giây
                sweepT += dt;
                float w = ((RectTransform)bar.transform).rect.width;
                float k = Mathf.Clamp01((sweepT - 2.4f) / 0.6f);
                sweep.anchoredPosition = new Vector2(Mathf.Lerp(-w * 0.55f, w * 0.55f, k), 0);
                if (sweepT >= 3) sweepT = 0;
            }
            // khung thanh (rãnh + thanh) nhún mỗi lần sao tới, chữ số nhún thêm
            if (bumpT >= 0)
            {
                bumpT += dt;
                float end = PunchCurve[PunchCurve.Length - 2];
                float k = bumpT >= end ? 0 : MachineFx.Curve(PunchCurve, bumpT);
                var target = frame ? frame : bar.transform;
                target.localScale = new Vector3(1 + PunchX * k, 1 + PunchY * k, 1);
                if (bar.Label) bar.Label.rectTransform.localScale = Vector3.one * (1 + PunchText * k);
                if (bumpT >= end) bumpT = -1;
            }
            // vòng cấp nhún khi lên cấp: 1,35 → 0,92 → 1 trong 0,4 giây
            if (popT >= 0 && badge)
            {
                popT += dt;
                float s = MachineFx.Curve(PopCurve, popT);
                badge.localScale = badgeScale * s;
                if (popT >= PopCurve[PopCurve.Length - 2])
                {
                    popT = -1;
                    badge.localScale = badgeScale;
                }
            }
        }

        // trả sao về kho hạt (hạt dùng lại không tự đặt lại cỡ)
        void Return(Image img)
        {
            img.rectTransform.localScale = Vector3.one;
            stars.Remove(img);
            fx.Give(img);
        }

        public void Clear()
        {
            StopAllCoroutines();
            flying = 0;
            Held = 0;
            if (fx == null) return;
            for (int i = stars.Count - 1; i >= 0; i--) Return(stars[i]);
            fx.Clear();
        }

        static readonly float[] PopCurve = { 0, 1, 0.08f, 1.35f, 0.25f, 0.92f, 0.4f, 1 };

        static Color C(string hex, float a = 1)
        {
            ColorUtility.TryParseHtmlString(hex, out var c);
            c.a = a;
            return c;
        }

        // ánh sáng mềm cộng sáng (pk_g_*, 2026-11-21): vệt sau kẹo bay là chấm sáng mềm dày (trắng hồng → tím), mờ nhanh
        static readonly MachineFx.Burst[] Trail =
        {
            new MachineFx.Burst { sprite = MachineGlow.Glow, life = 0.18f, lifeMax = 0.24f, size = 1.1f, sizeMax = 1.3f, curve = new[] { 0, 1f, 1, 0.35f },
                from = C("#fff0ff", 0.75f), to = C("#b77cf0", 0.25f), fadeAt = 0.3f },
        };

        // lấp lánh bốn cánh rắc theo vệt, trôi chậm
        static readonly MachineFx.Burst[] TrailSpark =
        {
            new MachineFx.Burst { sprite = MachineGlow.Spark, life = 0.3f, lifeMax = 0.45f, size = 0.5f, sizeMax = 0.8f, speed = 0.3f, speedMax = 1.2f, arc = 360, radius = 0.4f,
                rotSpeed = 120, curve = new[] { 0, 0.2f, 0.3f, 1, 1, 0 }, from = Color.white, to = C("#e2c4ff") },
        };

        // chùm phụt ra: loé mềm, vòng sáng lan, kim tuyến và lấp lánh văng (unit = nửa tầm toả)
        static readonly MachineFx.Burst[] SprayPop =
        {
            new MachineFx.Burst { sprite = MachineGlow.Glow, life = 0.26f, size = 2.6f, curve = new[] { 0, 0.4f, 0.25f, 1.1f, 1, 1.25f }, from = C("#fff2ff", 0.9f), to = C("#c99bff", 0.5f), fadeAt = 0.3f },
            new MachineFx.Burst { sprite = MachineGlow.Ring, life = 0.32f, size = 2.4f, curve = new[] { 0, 0.2f, 1, 1 }, from = C("#ffffff", 0.9f), to = C("#c18cf0", 0.6f), fadeAt = 0.35f },
            new MachineFx.Burst { sprite = MachineGlow.Glow, count = 14, life = 0.45f, lifeMax = 0.8f, size = 0.07f, sizeMax = 0.13f, speed = 2.5f, speedMax = 5f, dir = 90, arc = 220,
                radius = 0.1f, grav = 0.6f, dampen = 0.12f, curve = new[] { 0, 1f, 1, 0.4f }, from = C("#fff6ff"), to = C("#d2a8ff"), fadeAt = 0.55f },
            new MachineFx.Burst { sprite = MachineGlow.Spark, count = 5, life = 0.35f, lifeMax = 0.6f, size = 0.35f, sizeMax = 0.55f, speed = 1.5f, speedMax = 3.5f, dir = 90, arc = 200,
                dampen = 0.2f, rotSpeed = 120, curve = new[] { 0, 0.2f, 0.25f, 1.1f, 1, 0 }, from = Color.white, to = C("#e2c4ff") },
        };

        // kẹo tới (bảng số, thanh): loé mềm co, vòng sáng lan, lấp lánh lớn giữa, 4 lấp lánh văng
        static readonly MachineFx.Burst[] Hit =
        {
            new MachineFx.Burst { sprite = MachineGlow.Glow, life = 0.2f, size = 2.6f, curve = new[] { 0, 0.5f, 0.3f, 1.15f, 1, 0.8f }, from = C("#fff2ff", 0.95f), to = C("#c18cf0", 0.6f), fadeAt = 0.35f },
            new MachineFx.Burst { sprite = MachineGlow.Ring, life = 0.24f, size = 2.0f, curve = new[] { 0, 0.2f, 1, 1 }, from = Color.white, to = C("#c18cf0"), fadeAt = 0.4f },
            new MachineFx.Burst { sprite = MachineGlow.Spark, life = 0.22f, size = 1.6f, curve = new[] { 0, 0.3f, 0.3f, 1.1f, 1, 0.4f }, from = Color.white, to = C("#e9d2ff"), fadeAt = 0.4f, rotRange = 10 },
            new MachineFx.Burst { sprite = MachineGlow.Spark, count = 4, life = 0.25f, lifeMax = 0.4f, size = 0.4f, sizeMax = 0.6f, speed = 2, speedMax = 5, arc = 360, dampen = 0.3f, rotSpeed = 160,
                curve = new[] { 0, 0.4f, 0.25f, 1, 1, 0.2f }, from = Color.white, to = C("#d9b8ff") },
        };

        // lên cấp: vòng to, quầng vàng, sao văng quanh vòng cấp
        static readonly MachineFx.Burst[] LevelUp =
        {
            new MachineFx.Burst { life = 0.35f, size = 5f, curve = new[] { 0, 0.3f, 0.4f, 1.1f, 1, 1 }, from = C("#fff0a0", 0.9f), to = C("#ffb347", 0.7f), fadeAt = 0.4f },
            new MachineFx.Burst { sprite = "fx_ring", life = 0.35f, size = 4.5f, curve = new[] { 0, 0.2f, 1, 1 }, from = C("#ffe052"), to = C("#c18cf0"), fadeIn = 0.1f, fadeAt = 0.5f },
            new MachineFx.Burst { sprite = "fx_star", count = 6, life = 0.4f, lifeMax = 0.7f, size = 0.5f, sizeMax = 0.9f, speed = 4, speedMax = 9, arc = 360, dampen = 0.25f, grav = 0.2f, spin = true,
                curve = new[] { 0, 0.5f, 0.2f, 1, 1, 0.3f }, from = C("#ffe27a"), to = C("#ffb000") },
        };
    }
}
