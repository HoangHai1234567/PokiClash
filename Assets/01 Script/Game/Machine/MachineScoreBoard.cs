// Bảng số của máy bi (2026-11-10, chép bảng LED của máy tham khảo): nằm ở đầu máy, ngay dưới thanh kinh nghiệm (thanh dời lên vòm
// tủ lúc dựng bảng). Bi rơi vào ô EXP thì kẹo EXP bay từ ô lên bảng, số trên bảng đếm tăng dần (nhún, loé, đèn viền nháy); hết đợt
// thì Collect: kẹo bay từ bảng lên đầu thanh, số trên bảng đếm lùi về 0 trong khi thanh đầy dần. Bản lưu đã cộng EXP lúc bi rơi;
// thanh giữ chậm lại phần đang nằm trên bảng (MachineExpBar.Held).
// Dựng lúc vào màn bằng code (không cần nướng prefab): khung pk_bang_so (ArtGen/Pachinko/build_mo_ruong.py, cắt 9 mảnh theo
// refs/bang_so.json để kéo dài vừa đầu máy; chưa có ảnh thì tấm tím sẫm), màn tối có lớp chấm LED (pk_g_led lát), quầng sau số,
// vệt sáng lia qua (pk_g_lia, cộng sáng), bóng đèn viền chạy (pk_den_*), icon kẹo, số.
using System.Collections;
using System.Collections.Generic;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class MachineScoreBoard : MonoBehaviour
    {
        // khung màn tối trong ảnh pk_bang_so theo tỉ lệ (refs/bang_so.json, chép vào đây khi duyệt ảnh)
        public static Vector4 ScreenUv = new Vector4(0.045f, 0.241f, 0.955f, 0.747f); // x0, y0, x1, y1 (gốc trên trái)
        public const float CountRate = 9f; // số hiện chạy tới số thật: phần còn thiếu × CountRate mỗi giây (ít nhất 1 mỗi khung)
        public const float SweepEvery = 2.6f, SweepTime = 0.55f; // vệt sáng lia qua màn lúc rảnh
        public const int Bulbs = 22;
        static readonly float[] Punch = { 0, 1, 0.06f, 1.28f, 0.14f, 0.94f, 0.22f, 1 };

        RectTransform rt, screen, sweep;
        Image glow, icon, frame;
        TextMeshProUGUI num;
        readonly List<Image> bulbs = new List<Image>();
        Sprite bulbOff, bulbOn, bulbPink;
        int target; // EXP đang nằm trên bảng
        float shown, punchT = -1, sweepT, flashT, bulbStep;
        int incoming; // kẹo đang bay lên bảng
        float joltT = -1, collectT = -1, idleT;
        Vector2 home;
        TextMeshProUGUI fontRef;
        readonly List<(TextMeshProUGUI t, float age)> plus = new List<(TextMeshProUGUI, float)>();
        // số đo bảng LED của máy tham khảo: khung giật lên 3,8 px trong 0,033 giây, về chỗ lúc 0,067; chữ "+N" bật 0 → 1,51 (0,1) →
        // 0,75 (0,167) → 0,89 (0,233), trôi lên 41 px, mờ 0,367–0,567; thu số: viền chớp 3 lần (đỉnh 0,167 / 0,35 / 0,533 giây) trong
        // 0,65 giây rồi số mới bay lên thanh; đèn viền hai nhóm luân phiên chu kỳ 2,7 giây, nhanh 3 lần khi đang cộng
        static readonly float[] PlusScale = { 0, 0, 0.1f, 1.51f, 0.167f, 0.75f, 0.233f, 0.89f };
        public const float BulbCycle = 2.7f, CollectFlash = 0.65f;

        // bản 2 (GD_Claude/23, concept 2, 2026-11-20): khung pk_bang_so_v2 (ArtGen/Pachinko/v2/cat_v2.py, refs/v2_do.json) đặt đúng tỉ lệ
        // 1024 x 316 (bản casino 2026-11-20), màn tối theo ScreenUvV2, 26 bóng vẽ sẵn (tắt) phủ lớp sáng fx2_den_* theo BulbsV2 (u, v tâm theo tỉ lệ ảnh, r theo
        // chiều cao), số vẽ bằng hình pk_so_0..9. Nhịp đèn theo bảng số máy tham khảo (bản đục 2026-11-20): rảnh chu kỳ 2,22 giây (cả
        // bảng sáng 0,36 → nhóm A 0,75 → tắt hết 0,36 → nhóm B 0,75), đang cộng 0,83 giây (mỗi nhóm 0,415).
        public static readonly Vector4 ScreenUvV2 = new Vector4(0.0566f, 0.1835f, 0.9434f, 0.8133f);
        public const float BulbCoreV2 = 0.597f; // lõi bóng trong ảnh fx2_den_vang (phần còn lại là quầng)
        static readonly Vector3[] BulbsV2 =
        {
            new Vector3(0.0274f, 0.3519f, 0.0333f), new Vector3(0.1152f, 0.0885f, 0.0331f), new Vector3(0.1918f, 0.0885f, 0.0334f),
            new Vector3(0.2689f, 0.0884f, 0.0334f), new Vector3(0.3458f, 0.0885f, 0.0334f), new Vector3(0.4224f, 0.0885f, 0.0333f),
            new Vector3(0.4995f, 0.0884f, 0.0332f), new Vector3(0.5763f, 0.0884f, 0.0332f), new Vector3(0.6528f, 0.0884f, 0.0332f),
            new Vector3(0.7302f, 0.0883f, 0.0333f), new Vector3(0.8068f, 0.0884f, 0.0334f), new Vector3(0.8836f, 0.0886f, 0.0333f),
            new Vector3(0.9716f, 0.3518f, 0.033f), new Vector3(0.9717f, 0.6392f, 0.0329f), new Vector3(0.8836f, 0.9049f, 0.0334f),
            new Vector3(0.8068f, 0.9051f, 0.0334f), new Vector3(0.7303f, 0.9049f, 0.0333f), new Vector3(0.6528f, 0.905f, 0.0334f),
            new Vector3(0.5764f, 0.905f, 0.0334f), new Vector3(0.4995f, 0.9051f, 0.0333f), new Vector3(0.4225f, 0.905f, 0.0334f),
            new Vector3(0.3458f, 0.905f, 0.0334f), new Vector3(0.2689f, 0.905f, 0.0335f), new Vector3(0.1919f, 0.9051f, 0.0334f),
            new Vector3(0.1152f, 0.905f, 0.0332f), new Vector3(0.0274f, 0.6391f, 0.033f),
        };
        public const float IdleCycleV2 = 2.22f, BusyCycleV2 = 0.83f;
        bool v2;
        RectTransform digitBox;
        readonly List<Image> digits = new List<Image>();
        readonly Sprite[] digitSprites = new Sprite[10];
        float digitH;

        public int Value => target;
        public bool Busy => incoming > 0 || Mathf.RoundToInt(shown) != target;
        public RectTransform Rect => rt;
        public Vector3 IconWorld => icon ? icon.rectTransform.position : rt.position;
        public Vector3 NumWorld => num ? num.rectTransform.position : rt.position;

        public static Sprite Candy => MachineGlow.Sprite("pk_keo_exp") ?? (App.Art ? App.Art.Icon("exp") : null);

        // dựng bảng trong khối máy: rect theo px khối máy (gốc trên trái, y xuống); font lấy từ chữ mẫu
        public static MachineScoreBoard Build(RectTransform block, Rect r, TextMeshProUGUI font)
        {
            var prefab = MachineGlow.Prefabs.scoreBoard;
            if (!prefab || !MachineGlow.Prefabs.image || !MachineGlow.Prefabs.mask) return null;
            var b = Ui.Spawn(prefab, block);
            b.name = "bang_so";
            b.rt = (RectTransform)b.transform;
            b.rt.Place(new Vector2(0, 1), new Vector2(r.x, -r.y), r.size, new Vector2(0, 1));
            b.Make(font);
            b.fontRef = font;
            b.home = b.rt.anchoredPosition;
            return b;
        }

        void Make(TextMeshProUGUI font)
        {
            if (MachineGlow.Sprite("pk_bang_so_v2"))
            {
                MakeV2(font);
                return;
            }
            var size = rt.rect.size;
            frame = Child<Image>("khung", rt);
            frame.rectTransform.Stretch();
            frame.raycastTarget = false;
            var tex = MachineGlow.Sprite("pk_bang_so");
            if (tex)
            {
                // 9 mảnh: viền là phần ngoài màn tối (viền ghi trong cách nhập ảnh, menu prefab máy bi đặt theo ScreenUv), kéo dài
                // giữ dày viền theo tỉ lệ chiều cao bảng
                var rr = tex.rect;
                frame.sprite = tex;
                frame.type = Image.Type.Sliced;
                frame.pixelsPerUnitMultiplier = rr.height / size.y;
            }
            else frame.color = Theme.Hex("#3B2A4A");
            float k = tex ? size.y / tex.rect.height : 0;
            float bl = tex ? tex.rect.width * ScreenUv.x * k : 10, bt = tex ? tex.rect.height * ScreenUv.y * k : 10;
            float br = tex ? tex.rect.width * (1 - ScreenUv.z) * k : 10, bb = tex ? tex.rect.height * (1 - ScreenUv.w) * k : 10;

            screen = MachineGlow.NewMask("man", rt);
            screen.Stretch(bl, bt, br, bb);
            // màn: gradient tím sáng dần xuống đáy, lớp chấm LED, quầng sau số
            var grad = MachineGlow.Make("gradient", screen, MachineGlow.Grad, MachineGlow.Hex("#8a5cc8", 0.35f));
            if (grad) grad.rectTransform.Stretch();
            var led = MachineGlow.Make("led", screen, MachineGlow.Led, MachineGlow.Hex("#ffcf6a", 0.13f));
            if (led)
            {
                led.type = Image.Type.Tiled;
                led.pixelsPerUnitMultiplier = led.sprite.rect.height / 9f; // chấm LED 9 px
                led.rectTransform.Stretch();
            }
            float sh = size.y - bt - bb;
            glow = MachineGlow.Make("quang", screen, MachineGlow.Glow, MachineGlow.Hex("#ffd468", 0.25f));
            if (glow) glow.rectTransform.sizeDelta = new Vector2(sh * 3.2f, sh * 1.6f);

            icon = Child<Image>("keo", screen);
            icon.sprite = Candy;
            icon.preserveAspect = true;
            icon.raycastTarget = false;
            icon.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(-sh * 0.95f, 0), new Vector2(sh * 0.95f, sh * 0.8f));

            num = Ui.Spawn(font, screen);
            num.name = "so";
            num.text = "0";
            num.alignment = TextAlignmentOptions.MidlineLeft;
            num.fontSize = sh * 0.78f;
            num.fontStyle = FontStyles.Bold;
            num.color = Theme.Hex("#fff3c4");
            num.textWrappingMode = TextWrappingModes.NoWrap;
            num.raycastTarget = false;
            num.outlineWidth = 0.18f;
            num.outlineColor = Theme.Hex("#2B2118");
            num.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(sh * 0.15f + sh * 1.1f, 0), new Vector2(sh * 2.6f, sh), new Vector2(0.5f, 0.5f));

            var sw = MachineGlow.Make("lia", screen, MachineGlow.Sweep, MachineGlow.A(Color.white, 0.55f));
            if (sw)
            {
                sweep = sw.rectTransform;
                sweep.sizeDelta = new Vector2(sh * 0.9f, sh * 2.2f);
                sweep.localEulerAngles = new Vector3(0, 0, -22);
                sweep.gameObject.SetActive(false);
            }

            // bóng đèn viền: giữa dải viền, chạy quanh bảng
            bulbOff = MachineGlow.Sprite("pk_den_tat");
            bulbOn = MachineGlow.Sprite("pk_den_sang");
            bulbPink = MachineGlow.Sprite("pk_den_sang_hong") ?? bulbOn;
            if (bulbOff && bulbOn)
            {
                float d = Mathf.Min(bt, bb, bl) * 0.62f;
                var w = size.x;
                var h = size.y;
                // đường chạy: chữ nhật giữa mép bảng và mép màn
                float x0 = bl * 0.5f, x1 = w - br * 0.5f, y0 = bt * 0.5f, y1 = h - bb * 0.5f;
                float per = 2 * (x1 - x0) + 2 * (y1 - y0);
                for (int i = 0; i < Bulbs; i++)
                {
                    float s = per * i / Bulbs;
                    Vector2 p;
                    if (s < x1 - x0) p = new Vector2(x0 + s, y0);
                    else if ((s -= x1 - x0) < y1 - y0) p = new Vector2(x1, y0 + s);
                    else if ((s -= y1 - y0) < x1 - x0) p = new Vector2(x1 - s, y1);
                    else p = new Vector2(x0, y1 - (s - (x1 - x0)));
                    var bimg = Child<Image>("den", rt);
                    bimg.sprite = bulbOff;
                    bimg.raycastTarget = false;
                    bimg.rectTransform.Place(new Vector2(0, 1), new Vector2(p.x, -p.y), Vector2.one * d, new Vector2(0.5f, 0.5f));
                    bulbs.Add(bimg);
                }
            }
        }

        void MakeV2(TextMeshProUGUI font)
        {
            v2 = true;
            var size = rt.rect.size;
            frame = Child<Image>("khung", rt);
            frame.rectTransform.Stretch();
            frame.raycastTarget = false;
            frame.sprite = MachineGlow.Sprite("pk_bang_so_v2");
            frame.type = Image.Type.Simple;
            float bl = size.x * ScreenUvV2.x, bt = size.y * ScreenUvV2.y;
            float br = size.x * (1 - ScreenUvV2.z), bb = size.y * (1 - ScreenUvV2.w);
            screen = MachineGlow.NewMask("man", rt);
            screen.Stretch(bl, bt, br, bb);
            float sw = size.x - bl - br, sh = size.y - bt - bb;
            var led = MachineGlow.Make("led", screen, MachineGlow.Led, MachineGlow.Hex("#ffcf6a", 0.1f));
            if (led)
            {
                led.type = Image.Type.Tiled;
                led.pixelsPerUnitMultiplier = led.sprite.rect.height / 9f;
                led.rectTransform.Stretch();
            }
            // quầng sau số (ảnh sáng vẽ tay fx2_quang, gỡ nền đen), thở nhẹ, bừng khi cộng
            glow = MachineGlow.Make("quang", screen, MachineGlow.Sprite("fx2_quang") ? "fx2_quang" : MachineGlow.Glow, MachineGlow.Hex("#ffd468", 0.25f));
            float iconX = -sw / 2 + sh * 0.62f;
            float numX = (iconX + sh * 0.45f + sw / 2) / 2; // giữa phần màn bên phải icon
            if (glow) glow.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(numX, 0), new Vector2(sh * 3.6f, sh * 1.7f));

            icon = Child<Image>("keo", screen);
            icon.sprite = Candy;
            icon.preserveAspect = true;
            icon.raycastTarget = false;
            icon.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(iconX, 0), new Vector2(sh * 0.9f, sh * 0.78f));

            // chữ số TMP giữ làm dự phòng (thiếu hình số) và cho chỗ đặt; có hình thì ẩn chữ
            num = Ui.Spawn(font, screen);
            num.name = "so";
            num.text = "0";
            num.alignment = TextAlignmentOptions.Center;
            num.fontSize = sh * 0.78f;
            num.fontStyle = FontStyles.Bold;
            num.color = Theme.Hex("#fff3c4");
            num.textWrappingMode = TextWrappingModes.NoWrap;
            num.raycastTarget = false;
            num.outlineWidth = 0.18f;
            num.outlineColor = Theme.Hex("#2B2118");
            num.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(numX, 0), new Vector2(sw - sh * 1.2f, sh), new Vector2(0.5f, 0.5f));
            bool all = true;
            for (int i = 0; i < 10; i++) all &= digitSprites[i] = MachineGlow.Sprite("pk_so_" + i);
            if (all)
            {
                digitBox = Child<RectTransform>("so_hinh", screen);
                digitBox.Place(new Vector2(0.5f, 0.5f), new Vector2(numX, 0), new Vector2(sw - sh * 1.2f, sh), new Vector2(0.5f, 0.5f));
                digitH = sh * 0.72f;  // hình chữ số cắt sát (chữ cao ~94 % hình, cùng đáy) từ 2026-11-21
                num.alpha = 0;
                SetNumber(0);
            }

            var sw2 = MachineGlow.Make("lia", screen, MachineGlow.Sweep, MachineGlow.A(Color.white, 0.4f));
            if (sw2)
            {
                sweep = sw2.rectTransform;
                sweep.sizeDelta = new Vector2(sh * 0.9f, sh * 2.2f);
                sweep.localEulerAngles = new Vector3(0, 0, -22);
                sweep.gameObject.SetActive(false);
            }

            // lớp sáng phủ đúng các bóng vẽ sẵn trên khung (bóng tắt là hình vẽ, không cần ảnh tắt)
            bulbOff = null;
            bulbOn = MachineGlow.Sprite("fx2_den_vang");
            bulbPink = MachineGlow.Sprite("fx2_den_hong") ?? bulbOn;
            if (!bulbOn) return;
            foreach (var b in BulbsV2)
            {
                var img = Child<Image>("den", rt);
                img.sprite = bulbOn;
                img.raycastTarget = false;
                img.color = new Color(1, 1, 1, 0);
                float d = 2 * b.z * size.y / BulbCoreV2;
                img.rectTransform.Place(new Vector2(0, 1), new Vector2(b.x * size.x, -b.y * size.y), Vector2.one * d, new Vector2(0.5f, 0.5f));
                bulbs.Add(img);
            }
        }

        // số bằng hình: mỗi chữ một ảnh pk_so_*, cao digitH, sát nhau (chồng 6 %), canh giữa hộp số
        void SetNumber(int v)
        {
            if (num) num.text = v.ToString();
            if (!digitBox) return;
            string s = Mathf.Max(0, v).ToString();
            while (digits.Count < s.Length)
            {
                var img = Child<Image>("chu", digitBox);
                img.raycastTarget = false;
                digits.Add(img);
            }
            float total = 0;
            for (int i = 0; i < s.Length; i++)
            {
                var sp = digitSprites[s[i] - '0'];
                total += digitH * sp.rect.width / sp.rect.height * (i == 0 ? 1 : 0.94f);
            }
            float x = -total / 2;
            for (int i = 0; i < digits.Count; i++)
            {
                var img = digits[i];
                bool on = i < s.Length;
                if (img.gameObject.activeSelf != on) img.gameObject.SetActive(on);
                if (!on) continue;
                var sp = digitSprites[s[i] - '0'];
                float w = digitH * sp.rect.width / sp.rect.height;
                if (i > 0) x -= w * 0.06f;
                img.sprite = sp;
                img.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(x + w / 2, 0), new Vector2(w, digitH), new Vector2(0.5f, 0.5f));
                x += w;
            }
        }

        static T Child<T>(string name, Transform parent) where T : Component
        {
            if (typeof(T) == typeof(RectTransform)) return MachineGlow.NewRect(name, parent) as T;
            return MachineGlow.NewImage(name, parent) as T;
        }

        // kẹo EXP từ một điểm thế giới lên bảng: chùm kẹo phụt ra, khựng, rồi lần lượt phóng về icon kẹo của bảng
        // (MachineExpBar.Spray, 7..16 viên, kẹo 76 px, toả 125 px từ 2026-11-21); viên nào tới thì bảng cộng phần của viên đó, chữ
        // "+N" của cả chùm bật một lần ở viên tới đầu tiên, tiếng tách cao dần theo từng viên
        public void Receive(MachineExpBar bar, Vector3 from, int n, float delay = 0)
        {
            if (n <= 0) return;
            bar.Held += n;
            int k = MachineExpBar.SprayCount(n);
            incoming += k;
            int got = 0;
            bar.Spray(Candy, from, () => IconWorld, k, delay, i =>
            {
                incoming--;
                Add(MachineExpBar.Part(n, k, i), got == 0 ? n : 0);
                float now = Time.unscaledTime;
                if (now - lastTick >= 0.05f)
                {
                    lastTick = now;
                    App.Audio.Play("counter", 0.4f, 1f + Mathf.Min(got, 12) * 0.035f);
                }
                got++;
            }, 76, 125);
        }

        float lastTick = -1;

        // cộng lên bảng: số chạy tới, nhún, quầng loé, đèn viền nháy, vệt sáng lia qua; label > 0: bật chữ "+label"
        public void Add(int n, int label)
        {
            target += n;
            joltT = 0;
            if (label > 0) Plus(label);
            punchT = 0;
            flashT = 0.35f;
            if (sweep && !sweep.gameObject.activeSelf) sweepT = SweepEvery;
        }

        public void Add(int n) => Add(n, n);

        // đổ số trên bảng lên thanh: kẹo bay từ bảng tới đầu thanh, số đếm lùi; chờ thanh nhận hết
        public IEnumerator Collect(MachineExpBar bar)
        {
            for (float t = 0; Busy && t < 3; t += Time.unscaledDeltaTime) yield return null;
            if (target <= 0) yield break;
            // viền chớp 3 lần rồi mới thu (clip collect của bảng máy tham khảo)
            collectT = 0;
            yield return new WaitForSecondsRealtime(CollectFlash);
            // cả chùm phụt khỏi bảng một lần (số trên bảng đếm lùi về 0), khựng, rồi lần lượt bay mượt lên đầu thanh
            int total = target, k = Mathf.Clamp(Mathf.CeilToInt(total / 6f) + 4, 8, 18); // 2026-11-21: đông hơn (trước 4..10)
            target = 0;
            punchT = 0;
            joltT = 0;
            App.Audio.Play("whoosh", 0.35f, 1.25f);
            bar.Spray(Candy, IconWorld, () => bar.TipWorld, k, 0, i =>
            {
                bar.Deposit(MachineExpBar.Part(total, k, i));
            }, 66, 150);
            for (float t = 0; bar.Busy && t < 4; t += Time.unscaledDeltaTime) yield return null;
        }

        // chữ "+N" bật lên trên số rồi trôi lên, mờ
        void Plus(int n)
        {
            if (!fontRef || !screen) return;
            var t = Ui.Spawn(fontRef, rt);
            t.name = "cong";
            t.text = "+" + n;
            t.alignment = TextAlignmentOptions.Center;
            t.fontSize = num.fontSize * 0.7f; // 2026-11-21: to hơn (0,55) cho rõ
            t.fontStyle = FontStyles.Bold;
            t.color = Theme.Hex("#ffe27a");
            t.outlineWidth = 0.22f;
            t.outlineColor = Theme.Hex("#2B2118");
            t.raycastTarget = false;
            t.rectTransform.anchorMin = t.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            t.rectTransform.anchoredPosition = new Vector2(rt.rect.width * 0.3f, rt.rect.height * 0.35f);
            t.rectTransform.localScale = Vector3.zero;
            plus.Add((t, 0));
        }

        public void Clear()
        {
            foreach (var (t, _) in plus)
                if (t) Destroy(t.gameObject);
            plus.Clear();
            collectT = joltT = -1;
            target = 0;
            shown = 0;
            incoming = 0;
            SetNumber(0);
        }

        void Update()
        {
            float dt = Time.unscaledDeltaTime;
            if (Mathf.RoundToInt(shown) != target)
            {
                float step = Mathf.Max(1, Mathf.Abs(target - shown) * CountRate * dt);
                shown = Mathf.MoveTowards(shown, target, step);
                SetNumber(Mathf.RoundToInt(shown));
            }
            if (punchT >= 0)
            {
                punchT += dt;
                float end = Punch[Punch.Length - 2];
                float s = punchT >= end ? 1 : MachineFx.Curve(Punch, punchT);
                num.rectTransform.localScale = Vector3.one * s;
                if (digitBox) digitBox.localScale = Vector3.one * s;
                if (icon) icon.rectTransform.localScale = Vector3.one * (1 + (s - 1) * 0.6f);
                if (punchT >= end) punchT = -1;
            }
            if (flashT > 0) flashT -= dt;
            if (joltT >= 0)
            {
                joltT += dt;
                float j = joltT < 0.033f ? joltT / 0.033f : Mathf.Max(0, 1 - (joltT - 0.033f) / 0.034f);
                rt.anchoredPosition = home + new Vector2(0, 3.8f * 1.2f * j);
                if (joltT > 0.067f)
                {
                    joltT = -1;
                    rt.anchoredPosition = home;
                }
            }
            for (int i = plus.Count - 1; i >= 0; i--)
            {
                var (t, age) = plus[i];
                age += dt;
                if (!t || age > 0.567f)
                {
                    if (t) Destroy(t.gameObject);
                    plus.RemoveAt(i);
                    continue;
                }
                t.rectTransform.localScale = Vector3.one * MachineFx.Curve(PlusScale, age);
                t.rectTransform.anchoredPosition = new Vector2(rt.rect.width * 0.3f, rt.rect.height * 0.35f + 41 * 1.2f * Mathf.Min(1, age / 0.567f));
                t.alpha = age < 0.367f ? 1 : 1 - (age - 0.367f) / 0.2f;
                plus[i] = (t, age);
            }
            if (collectT >= 0)
            {
                collectT += dt;
                if (collectT > CollectFlash) collectT = -1;
            }
            if (glow)
            {
                // quầng thở nhẹ lúc rảnh, bừng lên khi cộng
                float a = 0.2f + 0.05f * Mathf.Sin(Time.unscaledTime * 3) + Mathf.Max(0, flashT) * 1.6f;
                glow.color = MachineGlow.Hex("#ffd468", Mathf.Min(0.85f, a));
            }
            if (sweep)
            {
                sweepT += dt;
                if (sweepT >= SweepEvery)
                {
                    float k = (sweepT - SweepEvery) / SweepTime;
                    sweep.gameObject.SetActive(k < 1);
                    float w = screen.rect.width;
                    sweep.anchoredPosition = new Vector2(Mathf.Lerp(-w * 0.6f, w * 0.6f, k), 0);
                    if (k >= 1) sweepT = 0;
                }
            }
            if (bulbs.Count > 0 && v2)
            {
                // bản 2: hai nhóm xen kẽ (chẵn A, lẻ B), lớp sáng bật/tắt; thu số: cả bảng sáng ở ba đỉnh như bản cũ
                bool all = collectT >= 0 && Mathf.Abs(Mathf.Repeat(collectT - 0.167f + 0.09f, 0.183f) - 0.09f) < 0.05f;
                float t = Time.unscaledTime;
                int ph; // 0 cả bảng, 1 nhóm A, 2 tắt hết, 3 nhóm B
                if (flashT > 0 || Busy) ph = t % BusyCycleV2 < BusyCycleV2 / 2 ? 1 : 3;
                else
                {
                    float c = t % IdleCycleV2;
                    ph = c < 0.36f ? 0 : c < 1.11f ? 1 : c < 1.47f ? 2 : 3;
                }
                for (int i = 0; i < bulbs.Count; i++)
                {
                    bool on = all || ph == 0 || ph == 1 && i % 2 == 0 || ph == 3 && i % 2 == 1;
                    var b = bulbs[i];
                    var s = i % 5 == 2 ? bulbPink : bulbOn;
                    if (b.sprite != s) b.sprite = s;
                    float a = on ? 1 : 0;
                    if (b.color.a != a) b.color = new Color(1, 1, 1, a);
                }
            }
            else if (bulbs.Count > 0)
            {
                bulbStep += dt * (flashT > 0 || Busy ? 3 : 1) / (BulbCycle / 2);
                int step = (int)bulbStep;
                // thu số: cả dãy sáng ở ba đỉnh 0,167 / 0,35 / 0,533 giây
                bool all = collectT >= 0 && Mathf.Abs(Mathf.Repeat(collectT - 0.167f + 0.09f, 0.183f) - 0.09f) < 0.05f;
                for (int i = 0; i < bulbs.Count; i++)
                {
                    bool on = all || (i + step) % 2 == 0;
                    var s = !on ? bulbOff : i % 2 == 0 ? bulbOn : bulbPink;
                    if (bulbs[i].sprite != s) bulbs[i].sprite = s;
                }
            }
        }
    }
}
