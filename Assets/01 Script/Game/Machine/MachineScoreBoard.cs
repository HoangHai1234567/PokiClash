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

        static T Child<T>(string name, Transform parent) where T : Component
        {
            if (typeof(T) == typeof(RectTransform)) return MachineGlow.NewRect(name, parent) as T;
            return MachineGlow.NewImage(name, parent) as T;
        }

        // kẹo EXP bay từ một điểm thế giới lên bảng (chia 1..4 kẹo, 10 EXP một kẹo); tới nơi bảng cộng
        public void Receive(MachineExpBar bar, Vector3 from, int n, float delay = 0)
        {
            if (n <= 0) return;
            bar.Held += n;
            int k = Mathf.Clamp(Mathf.CeilToInt(n / 10f), 1, 4), left = n;
            for (int i = 0; i < k; i++)
            {
                int part = i == k - 1 ? left : n / k;
                left -= part;
                incoming++;
                bar.FlyIcon(Candy, from, IconWorld, delay + i * 0.06f, () =>
                {
                    incoming--;
                    Add(part);
                }, 64, 0.55f);
            }
        }

        // cộng lên bảng: số chạy tới, nhún, quầng loé, đèn viền nháy, vệt sáng lia qua
        public void Add(int n)
        {
            target += n;
            joltT = 0;
            Plus(n);
            punchT = 0;
            flashT = 0.35f;
            if (sweep && !sweep.gameObject.activeSelf) sweepT = SweepEvery;
        }

        // đổ số trên bảng lên thanh: kẹo bay từ bảng tới đầu thanh, số đếm lùi; chờ thanh nhận hết
        public IEnumerator Collect(MachineExpBar bar)
        {
            for (float t = 0; Busy && t < 3; t += Time.unscaledDeltaTime) yield return null;
            if (target <= 0) yield break;
            // viền chớp 3 lần rồi mới thu (clip collect của bảng máy tham khảo)
            collectT = 0;
            yield return new WaitForSecondsRealtime(CollectFlash);
            int total = target, k = Mathf.Clamp(Mathf.CeilToInt(total / 15f), 3, 10), left = total;
            for (int i = 0; i < k; i++)
            {
                int part = i == k - 1 ? left : total / k;
                left -= part;
                target -= part;
                punchT = 0;
                bar.FlyIcon(Candy, IconWorld, bar.TipWorld, 0, () => bar.Deposit(part), 52, 0.5f);
                App.Audio.Play("pick", 0.35f, 1.0f + i * 0.04f);
                yield return new WaitForSecondsRealtime(0.07f);
            }
            target = 0;
            for (float t = 0; bar.Busy && t < 3; t += Time.unscaledDeltaTime) yield return null;
        }

        // chữ "+N" bật lên trên số rồi trôi lên, mờ
        void Plus(int n)
        {
            if (!fontRef || !screen) return;
            var t = Ui.Spawn(fontRef, rt);
            t.name = "cong";
            t.text = "+" + n;
            t.alignment = TextAlignmentOptions.Center;
            t.fontSize = num.fontSize * 0.55f;
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
            if (num) num.text = "0";
        }

        void Update()
        {
            float dt = Time.unscaledDeltaTime;
            if (Mathf.RoundToInt(shown) != target)
            {
                float step = Mathf.Max(1, Mathf.Abs(target - shown) * CountRate * dt);
                shown = Mathf.MoveTowards(shown, target, step);
                num.text = Mathf.RoundToInt(shown).ToString();
            }
            if (punchT >= 0)
            {
                punchT += dt;
                float end = Punch[Punch.Length - 2];
                float s = punchT >= end ? 1 : MachineFx.Curve(Punch, punchT);
                num.rectTransform.localScale = Vector3.one * s;
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
            if (bulbs.Count > 0)
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
