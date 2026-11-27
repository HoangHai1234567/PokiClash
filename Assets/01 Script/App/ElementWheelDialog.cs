// Hộp "Tương khắc" (prefab Assets/04 Prefabs/Dialogs/TuongKhac, biến thể tờ giấy gốc HopThoai; dựng bằng menu
// "PokiClash/Prefab/Hộp thoại và màn/Tương khắc: hộp và icon ô tướng"). Mở khi chạm icon vòng 5 chấm ở ô tướng (màn Tướng, hộp chọn đội,
// chi tiết tướng, chọn tướng khởi đầu) và ở bước hướng dẫn C12a (GD_Claude/25_FTUE.md, người dùng dặn 2026-11-27: người chơi phải biết
// khắc hệ quan trọng với chiến thuật).
// Từ trên xuống: băng tiêu đề (chữ sáng viền mực), dòng tướng; vòng 5 hệ theo chiều khắc (Thủy → Hỏa → Kim → Mộc → Thổ → Thủy, mũi tên
// từ hệ khắc tới hệ bị khắc); hai dòng của hệ đang xem: KHẮC (xanh lá) và BỊ KHẮC (đỏ), mỗi dòng hai icon hệ và "Đánh ×1,5 · Chịu đòn
// ×0,75" (hai dòng); câu chiến thuật; nút "Hiểu rồi!" (chỉ bài học). Mũi tên vẽ dần lần lượt bắt đầu từ mũi tên hệ đang xem đi ra, vòng một
// lượt về mũi tên vào nó. Tướng đồng hành không chịu thiệt vì hệ (Elements.Mult có cờ đồng hành): dòng BỊ KHẮC ghi ×1 và câu riêng.
// Mọi phần dựng sẵn trong prefab; Show chỉ tô màu, gán chữ và chạy hoạt cảnh.
using System;
using System.Collections;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ElementWheelDialog : Dialog
    {
        // một hệ trên vòng: đĩa màu hệ, icon hệ, vòng sáng (hệ đang xem vàng, hệ bị khắc xanh, hệ khắc mình đỏ), tên hệ
        [Serializable]
        public struct Node
        {
            public RectTransform root;
            public Image disk, icon, ring;
            public TextMeshProUGUI label;
        }

        // mũi tên từ hệ thứ i tới hệ thứ i + 1 trên vòng: nét mực dưới, nét màu trên (cùng đường, gồm thân cung và đầu chữ V)
        [Serializable]
        public struct Arrow
        {
            public InkPath ink, fill;
        }

        // một dòng quan hệ: nền, viên nhãn (KHẮC / BỊ KHẮC), icon hệ trái → phải, chữ hệ số
        [Serializable]
        public struct Row
        {
            public Image bg, pill, from, to;
            public TextMeshProUGUI tag, text;
        }

        [Serializable]
        public struct Parts
        {
            public TextMeshProUGUI title, sub, tip;
            public Node[] nodes; // theo Order
            public Arrow[] arrows; // arrows[i]: Order[i] → Order[i + 1]
            public Row beat, beaten;
            public CanvasGroup rows; // hai dòng và câu chiến thuật hiện sau khi vẽ xong vòng
            public SketchButton ok; // "Hiểu rồi!" (bài học)
            public RectTransform sheet; // tờ giấy: cao fullH khi có nút "Hiểu rồi!", shortH khi không
            public float fullH, shortH;
        }

        [SerializeField] Parts p;

        // thứ tự trên vòng, theo chiều kim đồng hồ từ đỉnh: mỗi hệ khắc hệ kế tiếp (Elements.Beats)
        public static readonly Elem[] Order = { Elem.Thuy, Elem.Hoa, Elem.Kim, Elem.Moc, Elem.Tho };

        // màu mũi tên: khắc (xanh lá), bị khắc (đỏ), còn lại (giấy sẫm)
        public static readonly Color Good = Theme.Hex("#5fb84a"), Bad = Theme.Hex("#e0533d"), Other = Theme.Hex("#d8c7a2");

        // Dùng khi dựng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        static int IndexOf(Elem e) => Array.IndexOf(Order, e);

        // chạm icon ở ô tướng: vòng tô theo hệ của tướng đó
        public static void Open(HeroDef hero)
        {
            if (hero == null || !Ready) return; // tiếng chạm do nút phát
            // đã tự mở xem thì không dẫn lại nữa (người dùng báo 2026-11-27: chạm xem rồi vẫn bị bắt mở tiếp): gợi ý nút ở màn Tướng / hộp
            // chọn đội và bài học C12a coi như xong, gỡ khỏi hàng chờ của lớp phủ
            if (App.Save?.Data != null) Guide.Skip(Tutorial.WheelTile, Tutorial.WheelPick, Tutorial.CounterWheel);
            App.Modals.Open<ElementWheelDialog>().Show(hero, false, null);
        }

        // bài học hướng dẫn (C12a): bắt buộc, vẽ chậm, đóng bằng "Hiểu rồi!"; chưa dựng prefab thì gọi done ngay
        public static bool OpenLesson(HeroDef starter, Action done)
        {
            if (starter == null || !Ready) return false;
            App.Modals.Open<ElementWheelDialog>(mandatory: true).Show(starter, true, done);
            return true;
        }

        // prefab đã có trong UiKit.dialogs (menu Tương khắc đã chạy)
        public static bool Ready
        {
            get
            {
                var kit = Theme.Prefabs;
                if (!kit || App.Modals == null) return false;
                foreach (var d in kit.dialogs)
                    if (d is ElementWheelDialog)
                        return true;
                return false;
            }
        }

        bool lesson;
        Action onDone;

        public void Show(HeroDef hero, bool isLesson, Action done)
        {
            lesson = isLesson;
            onDone = done;
            var s = App.Save?.Data;
            bool partner = s != null && hero.id == s.starter;
            var e = hero.elem;
            Elem beat = Elements.Beats(e), by = Progress.CounterOf(e);

            if (p.sheet) p.sheet.sizeDelta = new Vector2(p.sheet.sizeDelta.x, lesson ? p.fullH : p.shortH);
            p.title.text = Loc.T("Tương khắc");
            p.sub.text = Loc.F("{0} · hệ {1}", hero.name, Elements.Name(e));

            int fi = IndexOf(e);
            for (int i = 0; i < p.nodes.Length && i < Order.Length; i++)
            {
                var n = p.nodes[i];
                var el = Order[i];
                n.disk.color = Color.Lerp(Theme.Of(el), Color.white, 0.55f);
                n.label.text = Elements.Name(el);
                n.label.color = Color.Lerp(Theme.Of(el), Theme.Ink, 0.45f);
                bool on = el == e || el == beat || el == by;
                n.ring.gameObject.SetActive(on);
                n.ring.color = el == e ? Theme.Yellow : el == beat ? Good : Bad;
                n.root.localScale = Vector3.one * (el == e ? 1.15f : 1f);
            }
            for (int i = 0; i < p.arrows.Length; i++)
            {
                // arrows[i] đi từ Order[i]: ra khỏi hệ đang xem là khắc, vào hệ đang xem (từ hệ trước nó) là bị khắc
                var c = i == fi ? Good : (i + 1) % Order.Length == fi ? Bad : Other;
                p.arrows[i].fill.color = c;
                p.arrows[i].ink.Reveal = p.arrows[i].fill.Reveal = 0;
            }

            // hệ số thật của tướng này (đồng hành không chịu thiệt): đánh hệ mình khắc / bị hệ đó đánh; đánh hệ khắc mình / bị hệ đó đánh
            double hitBeat = Elements.Mult(e, beat, partner, false), takeBeat = Elements.Mult(beat, e, false, partner);
            double hitBy = Elements.Mult(e, by, partner, false), takeBy = Elements.Mult(by, e, false, partner);
            Fill(p.beat, Loc.T("KHẮC"), Good, e, beat, hitBeat, takeBeat);
            Fill(p.beaten, Loc.T("BỊ KHẮC"), Bad, by, e, hitBy, takeBy);
            p.tip.text = partner
                ? Loc.T("Bạn đồng hành không bao giờ bị thiệt vì hệ.") + "\n" + Loc.T("Tướng khác bị khắc thì yếu hẳn: xem hệ địch rồi mới chọn đội.")
                : Loc.T("Trước mỗi trận, xem hệ địch và mang tướng khắc nó!");

            if (p.ok)
            {
                p.ok.gameObject.SetActive(lesson);
                p.ok.SetText(Loc.T("Hiểu rồi!"));
                p.ok.SetOnClick(Close);
                p.ok.Interactable = false;
            }
            if (Modal != null)
            {
                var prev = Modal.OnClose;
                Modal.OnClose = () =>
                {
                    prev?.Invoke();
                    var d = onDone;
                    onDone = null;
                    d?.Invoke();
                };
            }
            StartCoroutine(Play(fi));
        }

        // một dòng quan hệ: from khắc to; hit: hệ số đòn của tướng đang xem, take: hệ số đòn nó phải chịu
        void Fill(Row r, string tag, Color c, Elem from, Elem to, double hit, double take)
        {
            r.pill.color = c;
            r.tag.text = tag;
            r.bg.color = Color.Lerp(c, Color.white, 0.82f);
            Theme.SetSprite(r.from, App.Art ? App.Art.Icon(IconOf(from)) : null);
            Theme.SetSprite(r.to, App.Art ? App.Art.Icon(IconOf(to)) : null);
            r.text.text = Loc.F("Đánh {0}\nChịu đòn {1}", Mult(hit, true), Mult(take, false));
        }

        // "×1,5" tô xanh khi có lợi cho tướng đang xem, đỏ khi bất lợi (đánh: lớn hơn 1 là lợi; chịu đòn: nhỏ hơn 1 là lợi)
        static string Mult(double m, bool hit)
        {
            string num = Math.Abs(m - Math.Round(m)) < 1e-6 ? m.ToString("0", System.Globalization.CultureInfo.InvariantCulture)
                : m.ToString("0.0#", System.Globalization.CultureInfo.InvariantCulture);
            string s = "×" + (Loc.IsEn ? num : num.Replace('.', ',')); // tiếng Việt dấu phẩy thập phân, tiếng Anh dấu chấm
            bool good = hit ? m > 1 : m < 1, bad = hit ? m < 1 : m > 1;
            if (!good && !bad) return s;
            return $"<color=#{ColorUtility.ToHtmlStringRGB(good ? Theme.GreenD : Theme.RedD)}>{s}</color>";
        }

        public static string IconOf(Elem e) => e == Elem.Hoa ? "e_hoa" : e == Elem.Thuy ? "e_thuy" : e == Elem.Moc ? "e_moc" : e == Elem.Kim ? "e_kim" : "e_tho";

        // vẽ 5 mũi tên lần lượt (bắt đầu từ mũi tên ra khỏi hệ đang xem), nảy 3 hệ được tô, rồi hiện hai dòng và câu chiến thuật
        IEnumerator Play(int fi)
        {
            if (p.rows) p.rows.alpha = 0;
            float each = lesson ? 0.32f : 0.13f;
            yield return new WaitForSecondsRealtime(lesson ? 0.35f : 0.12f);
            for (int k = 0; k < p.arrows.Length; k++)
            {
                var a = p.arrows[(Mathf.Max(0, fi) + k) % p.arrows.Length];
                for (float t = 0; t < each; t += Time.unscaledDeltaTime)
                {
                    float r = Mathf.SmoothStep(0, 1, t / each);
                    a.ink.Reveal = a.fill.Reveal = r;
                    yield return null;
                }
                a.ink.Reveal = a.fill.Reveal = 1;
                App.Audio?.Play("pick", lesson ? 0.45f : 0.25f, 0.9f + 0.06f * k);
            }
            App.Audio?.Play("counter", 0.7f);
            for (int i = 0; i < p.nodes.Length; i++)
                if (p.nodes[i].ring.gameObject.activeSelf)
                    UiMotion.Of(p.nodes[i].root).Punch(0.7f);
            if (p.rows)
                for (float t = 0; t < 0.25f; t += Time.unscaledDeltaTime)
                {
                    p.rows.alpha = t / 0.25f;
                    yield return null;
                }
            if (p.rows) p.rows.alpha = 1;
            if (lesson && p.ok)
            {
                yield return new WaitForSecondsRealtime(0.4f);
                p.ok.Interactable = true;
            }
        }
    }
}
