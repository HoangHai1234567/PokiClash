// Thanh kinh nghiệm trên đầu máy bi (như thanh cấp trên máy tham khảo: vòng cấp bên trái, thanh EXP, "số/số").
// Bi rơi vào ô EXP thì sao EXP bay từ ô lên đầu phần đầy của thanh; tới nơi thanh mới cộng, loé tím, và cả khung thanh
// (rãnh vẽ tay cắt từ thân máy + thanh + chữ) nhún như thanh năng lượng của máy tham khảo. Thanh hiện chậm hơn bản lưu trong
// lúc sao còn bay (bản lưu cộng ngay lúc bi rơi). Lên cấp: thanh đầy rồi về 0, vòng cấp nhún, loé to.
// Prefab: phần "thanh_kinh_nghiem" của Screens/Machine, dựng bằng menu "PokiClash/Prefab/Máy bi: thanh kinh nghiệm";
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

        // nhún khi cộng: dáng chép thanh năng lượng của máy tham khảo (nền và phần đầy cùng phóng 1,2 → 1,08 → 1,2 → 1,08 → 1,2 → 1
        // trong 0,25 giây, chữ số phóng mạnh hơn). Thanh này dài nên biên độ chia theo trục: ngang PunchX, dọc PunchY, chữ thêm PunchText.
        // Không bao giờ nhỏ hơn 1, để bản rãnh nhún luôn che kín rãnh vẽ sẵn của thân máy bên dưới.
        public static readonly float[] PunchCurve = { 0, 1, 0.05f, 0.4f, 0.1f, 1, 0.15f, 0.4f, 0.2f, 0.7f, 0.25f, 0 };
        public const float PunchX = 0.03f, PunchY = 0.18f, PunchText = 0.12f;

        int level, exp; // đang hiện
        int flying;
        bool bound;
        MachineFx fx;
        float bumpT = -1, popT = -1, lastSound = -1;
        int combo; // sao tới liền nhau: tiếng cao dần
        readonly List<Image> stars = new List<Image>(); // sao đang bay
        Vector3 badgeScale = Vector3.one;

        public bool Busy => flying > 0;

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
        public void FlyIcon(Sprite sprite, Vector3 from, Vector3 to, float delay, System.Action arrive)
        {
            if (!bound)
            {
                arrive?.Invoke();
                return;
            }
            StartCoroutine(FlyIconRun(sprite, from, to, delay, arrive));
        }

        IEnumerator FlyIconRun(Sprite sprite, Vector3 from, Vector3 to, float delay, System.Action arrive)
        {
            var img = fx.Take(flyLayer);
            stars.Add(img);
            img.sprite = sprite;
            img.color = Color.white;
            img.enabled = false;
            var rt = img.rectTransform;
            rt.sizeDelta = Vector2.one * 44;
            rt.localEulerAngles = Vector3.zero;
            for (float w = 0; w < delay; w += Time.unscaledDeltaTime) yield return null;
            img.enabled = true;
            var a = Anch(from);
            var b = Anch(to);
            var c = (a + b) / 2 + new Vector2(Random.Range(-90f, 90f), 150 + Random.Range(0, 80));
            const float dur = 0.5f;
            for (float t = 0; t < dur; t += Time.unscaledDeltaTime)
            {
                float k = t / dur;
                float e = k * k * (3 - 2 * k);
                rt.anchoredPosition = (1 - e) * (1 - e) * a + 2 * (1 - e) * e * c + e * e * b;
                rt.localScale = Vector3.one * Mathf.Lerp(1.2f, 0.7f, k);
                yield return null;
            }
            Return(img);
            arrive?.Invoke();
        }

        // vào màn: hiện đúng bản lưu, không chạy
        public void Bind()
        {
            fx = new MachineFx(particle, flyLayer);
            badgeScale = badge ? badge.localScale : Vector3.one;
            flying = 0;
            bound = true;
            Show(S.level, S.exp, true);
        }

        // bản lưu đổi ngoài sao bay (mở rương ra EXP, bảng thử): theo kịp khi không còn sao nào đang bay
        public void Sync()
        {
            if (!bound || flying > 0) return;
            if (level != S.level || exp != S.exp) Show(S.level, S.exp, false);
        }

        void Show(int lv, int e, bool instant)
        {
            bool up = lv > level && !instant;
            if (up) bar.Set(0, 1, 0, null, true); // lên cấp: thanh về 0 rồi đầy lại tới số mới
            level = lv;
            exp = e;
            int need = Progress.ExpToNext(level, Cfg);
            bool max = level >= Cfg.maxLevel;
            bar.Set(max ? need : exp, need, 0, max ? "Tối đa" : $"{exp}/{need}", instant);
            if (arc) arc.fillAmount = max ? 1 : Mathf.Clamp01((float)exp / Mathf.Max(1, need));
            if (lvText) lvText.text = level.ToString();
            if (up) LevelPop();
        }

        // n EXP bay từ điểm from (thế giới) lên thanh, chia cho 1..MaxStars sao (10 EXP một sao, ít nhất 1)
        public void Fly(Vector3 from, int n)
        {
            if (!bound || n <= 0) return;
            int k = Mathf.Clamp(Mathf.CeilToInt(n / 10f), 1, MaxStars);
            int left = n;
            for (int i = 0; i < k; i++)
            {
                int part = i == k - 1 ? left : n / k;
                left -= part;
                flying++;
                StartCoroutine(FlyOne(from, part, i * FlyGap));
            }
        }

        IEnumerator FlyOne(Vector3 from, int n, float delay)
        {
            var img = fx.Take(flyLayer);
            stars.Add(img);
            img.sprite = App.Art.Icon("exp");
            img.color = Color.white;
            img.enabled = false;
            var rt = img.rectTransform;
            rt.sizeDelta = Vector2.one * StarSize;
            rt.localEulerAngles = Vector3.zero;
            for (float w = 0; w < delay; w += Time.unscaledDeltaTime) yield return null;
            img.enabled = true;

            var a = Anch(from);
            // điểm uốn: văng sang một bên và lên trên trước khi lao về thanh (như kẹo nhảy khỏi ô rồi bay về thanh cấp)
            float side = Random.Range(-1f, 1f);
            var c = a + new Vector2(side * 220, 260 + Random.Range(0, 140));
            float dur = FlyTime + Random.Range(0, FlyJitter);
            float trail = 0;
            for (float t = 0; t < dur; t += Time.unscaledDeltaTime)
            {
                float k = t / dur;
                float e = k * k * (3 - 2 * k);
                var b = Anch(bar.TipWorld());
                var p = (1 - e) * (1 - e) * a + 2 * (1 - e) * e * c + e * e * b;
                rt.anchoredPosition = p;
                // nhảy ra 0,5 → 1,15 trong 0,12 giây đầu, nhỏ dần về 0,75 khi tới
                float s = k < 0.2f ? Mathf.Lerp(0.5f, 1.15f, k / 0.2f) : Mathf.Lerp(1.15f, 0.75f, (k - 0.2f) / 0.8f);
                rt.localScale = Vector3.one * s;
                rt.localEulerAngles = new Vector3(0, 0, Mathf.Sin(k * Mathf.PI) * 25 * side);
                if ((trail += Time.unscaledDeltaTime) > 0.045f)
                {
                    trail = 0;
                    fx.Emit(Trail, p, 40);
                }
                yield return null;
            }
            Return(img);
            flying--;
            Arrive(n);
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
            if (flying == 0)
            {
                lv = S.level;
                e = S.exp;
            }
            Show(lv, e, false);
            bumpT = 0;
            fx.Emit(Hit, Anch(bar.TipWorld()), 40);
            float now = Time.unscaledTime;
            combo = now - lastSound < 0.4f ? Mathf.Min(combo + 1, 8) : 0;
            if (now - lastSound >= SoundGap)
            {
                lastSound = now;
                App.Audio.Play("pick", 0.45f, 1.05f + combo * 0.04f);
            }
        }

        void LevelPop()
        {
            popT = 0;
            if (badge) fx.Emit(LevelUp, Anch(badge.position), 40);
            App.Audio.Play("level", 0.7f);
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
            if (!bound) return;
            float dt = Time.unscaledDeltaTime;
            fx.Update(dt);
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

        // vệt sau sao bay: chấm tím nhạt mờ nhanh
        static readonly MachineFx.Burst[] Trail =
        {
            new MachineFx.Burst { sprite = "fx_sparkle", life = 0.22f, lifeMax = 0.32f, size = 0.35f, sizeMax = 0.55f, speed = 0, speedMax = 0.4f, arc = 360, spin = true,
                curve = new[] { 0, 1f, 1, 0.2f }, from = C("#f3e6ff"), to = C("#c18cf0", 0.8f), fadeAt = 0.4f },
        };

        // sao tới thanh: quầng tím co, vòng mảnh lan, 4 lấp lánh văng
        static readonly MachineFx.Burst[] Hit =
        {
            new MachineFx.Burst { life = 0.18f, size = 2.2f, curve = new[] { 0, 0.4f, 0.3f, 1.1f, 1, 0.7f }, from = C("#efdcff", 0.95f), to = C("#b783e6", 0.8f), fadeAt = 0.4f },
            new MachineFx.Burst { sprite = "fx_ring", life = 0.22f, size = 1.8f, curve = new[] { 0, 0.2f, 1, 1 }, from = Color.white, to = C("#c18cf0"), fadeIn = 0.15f, fadeAt = 0.5f },
            new MachineFx.Burst { sprite = "fx_sparkle", count = 4, life = 0.25f, lifeMax = 0.4f, size = 0.3f, sizeMax = 0.5f, speed = 2, speedMax = 5, arc = 360, dampen = 0.3f, spin = true,
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
