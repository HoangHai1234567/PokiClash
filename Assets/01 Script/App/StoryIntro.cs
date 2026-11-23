// Đoạn cốt truyện mở đầu (GD_Claude/25_FTUE.md mục 11): chạy lần đầu vào game, trước màn tải con tàu; học trang truyện tranh mở đầu
// Kingdom Rush. Trang truyện tràn màn hình (người dùng 2026-11-23: "full screen, cấu trúc như comic panel"): mỗi trang 3 ô tranh tứ giác
// ghép kín trang, vách chia xiên, khe giấy giữa các ô, viền mực quanh ô (ComicPanel + InkPath). Chạm một lần hiện một ô (ô nảy ra từ tâm,
// tranh trôi chậm trong ô), khung lời dẫn ở góc ô chạy chữ dần; hết trang 1 thì trang 2 trượt vào; chạm sau ô cuối là xong. Nút "Bỏ qua"
// ở góc. Chạm lúc ô đang hiện thì hiện xong ngay. Xem lại ở Sổ tay: dòng "Cốt truyện mở đầu", hoặc nút trong hộp Cách chơi.
// Prefab Assets/04 Prefabs/Screens/CotTruyen (canvas riêng thứ tự 25: trên mây và hộp thoại), dựng bằng menu "PokiClash/Prefab/Cốt
// truyện mở đầu (CotTruyen)", gán App.storyPrefab. Ảnh ô ở Assets/03 Art/Story/khung_1..6.png (gói GPT ArtGen/Story/build_story.py);
// chưa có thì menu tạm gắn ảnh đảo có sẵn. Hình ô tính lúc chạy theo cỡ màn (Layout), nên máy dài, máy tính bảng đều kín trang.
using System;
using System.Collections;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class StoryIntro : MonoBehaviour
    {
        [Serializable]
        public struct Panel
        {
            public RectTransform frame; // ô (phủ cả trang, có CanvasGroup; pivot dời về tâm ô lúc chạy để nảy quanh tâm)
            public ComicPanel art; // tranh trong tứ giác
            public InkPath border; // viền mực quanh ô (pivot góc dưới trái)
            public RectTransform caption; // khung lời dẫn (ẩn nếu ô không có chữ)
            public InkPath captionBorder;
            public TextMeshProUGUI captionText;
        }

        [SerializeField] CanvasGroup group;
        [SerializeField] RectTransform[] pages = new RectTransform[2];
        [SerializeField] Panel[] panels = new Panel[6];
        [SerializeField] ClickCatcher tap;
        [SerializeField] SketchButton skip;
        [SerializeField] TextMeshProUGUI hint;

        public const int PerPage = 3;
        public const float Margin = 22, Gutter = 26, BorderWidth = 7, CaptionPadX = 26, CaptionPadY = 16;

        // ---------- bố cục trang ----------

        struct Line
        {
            public Vector2 a, b;
            public Line(float ax, float ay, float bx, float by)
            {
                a = new Vector2(ax, ay);
                b = new Vector2(bx, by);
            }
        }

        // đường theo tỉ lệ trang (0..1, y lên trên). 0 trên, 1 phải, 2 dưới, 3 trái là mép trang (lùi Margin); 4 vách ngang, 5 vách dọc là
        // vách chia xiên của từng trang (lùi nửa Gutter mỗi bên). Trang 1: ô ngang trên, hai ô dọc dưới; trang 2: hai ô dọc trên, ô ngang dưới.
        static readonly Line[] PageEdges = { new Line(0, 1, 1, 1), new Line(1, 0, 1, 1), new Line(0, 0, 1, 0), new Line(0, 0, 0, 1) };

        // tỉ lệ tranh: ô ngang 3:2, ô dọc 2:3 (gói GPT ArtGen/Story)
        const float WideAspect = 1.5f, TallAspect = 2f / 3f;

        // vách ngang đặt theo cỡ màn sao cho ô ngang và hai ô dọc bị cắt bớt bề ngang như nhau (màn dài 9:19,5 thì không tránh được cắt,
        // chia đều để không ô nào mất quá nhiều); vách dọc nối từ mép trang tới vách ngang
        static Line Divider(int page, int which, Vector2 size)
        {
            float wl = size.x - 2 * Margin, wp = (wl - Gutter) * 0.5f, usable = size.y - 2 * Margin - Gutter;
            float hl = Mathf.Clamp(usable / (1 + wp * WideAspect / (wl * TallAspect)), usable * 0.3f, usable * 0.6f);
            float cut = (Margin + hl + Gutter * 0.5f) / size.y; // từ mép có ô ngang tới giữa vách ngang
            if (page == 0)
            {
                float y = 1 - cut;
                return which == 0 ? new Line(0, y - 0.025f, 1, y + 0.025f) : new Line(0.56f, 0, 0.48f, y);
            }
            return which == 0 ? new Line(0, cut + 0.02f, 1, cut - 0.02f) : new Line(0.44f, 1, 0.53f, cut);
        }

        // điểm lấy nét của từng tranh (tỉ lệ ảnh, gốc dưới trái): giữ cậu bé, các tướng khi tranh bị cắt
        static readonly Vector2[] Focus =
        {
            new Vector2(0.52f, 0.5f), new Vector2(0.45f, 0.45f), new Vector2(0.42f, 0.4f),
            new Vector2(0.5f, 0.45f), new Vector2(0.5f, 0.4f), new Vector2(0.45f, 0.4f),
        };
        // mỗi ô là 4 đường đi vòng quanh; góc k nằm giữa đường k và đường k+1
        static readonly int[][] Edges =
        {
            new[] { 0, 1, 4, 3 }, new[] { 4, 5, 2, 3 }, new[] { 4, 1, 2, 5 },
            new[] { 0, 5, 4, 3 }, new[] { 0, 1, 4, 5 }, new[] { 4, 1, 2, 3 },
        };
        // góc đặt khung lời dẫn (chỉ số góc của ô): tránh nút Bỏ qua (trên phải) và dòng nhắc chạm (giữa đáy)
        static readonly int[] CaptionCorner = { 3, 3, 3, 3, 1, 0 };

        // góc ô i (đơn vị UI, gốc dưới trái trang) trên trang cỡ size
        public static Vector2[] Quad(int i, Vector2 size)
        {
            var e = Edges[i];
            var a = new Vector2[4];
            var b = new Vector2[4];
            var d = new float[4];
            for (int k = 0; k < 4; k++)
            {
                var ln = e[k] < 4 ? PageEdges[e[k]] : Divider(i / PerPage, e[k] - 4, size);
                a[k] = Vector2.Scale(ln.a, size);
                b[k] = Vector2.Scale(ln.b, size);
                d[k] = e[k] < 4 ? Margin : Gutter * 0.5f;
            }
            var c = Vector2.zero;
            for (int k = 0; k < 4; k++) c += Intersect(a[k], b[k], a[(k + 1) % 4], b[(k + 1) % 4]) * 0.25f;
            for (int k = 0; k < 4; k++)
            {
                var dir = (b[k] - a[k]).normalized;
                var n = new Vector2(-dir.y, dir.x);
                if (Vector2.Dot(c - a[k], n) < 0) n = -n;
                a[k] += n * d[k];
                b[k] += n * d[k];
            }
            var q = new Vector2[4];
            for (int k = 0; k < 4; k++) q[k] = Intersect(a[k], b[k], a[(k + 1) % 4], b[(k + 1) % 4]);
            return q;
        }

        static Vector2 Intersect(Vector2 a1, Vector2 b1, Vector2 a2, Vector2 b2)
        {
            Vector2 r = b1 - a1, s = b2 - a2;
            float den = r.x * s.y - r.y * s.x;
            if (Mathf.Abs(den) < 1e-6f) return a1;
            float t = ((a2.x - a1.x) * s.y - (a2.y - a1.y) * s.x) / den;
            return a1 + r * t;
        }

        static Vector2 Center(Vector2[] q) => (q[0] + q[1] + q[2] + q[3]) * 0.25f;

        // hộp (tâm pos, cỡ box) nằm trong tứ giác lồi, cách mép ít nhất pad
        static bool Inside(Vector2[] q, Vector2 pos, Vector2 box, float pad)
        {
            var c = Center(q);
            for (int k = 0; k < 4; k++)
            {
                Vector2 a = q[k], dir = (q[(k + 1) % 4] - a).normalized;
                var n = new Vector2(-dir.y, dir.x);
                if (Vector2.Dot(c - a, n) < 0) n = -n;
                for (int s = 0; s < 4; s++)
                {
                    var p = pos + new Vector2((s & 1) == 0 ? -box.x : box.x, (s & 2) == 0 ? -box.y : box.y) * 0.5f;
                    if (Vector2.Dot(p - a, n) < pad) return false;
                }
            }
            return true;
        }

        // nét mực vòng quanh đa giác: góc và điểm giữa mỗi cạnh lệch nhẹ (vẻ vẽ tay), cố định theo seed
        static Vector2[] InkLoop(Vector2[] q, int seed)
        {
            var rnd = new System.Random(seed * 7919 + 17);
            float J() => (float)(rnd.NextDouble() * 2 - 1) * 1.8f;
            var pts = new Vector2[q.Length * 2];
            for (int k = 0; k < q.Length; k++)
            {
                pts[k * 2] = q[k];
                pts[k * 2 + 1] = (q[k] + q[(k + 1) % q.Length]) * 0.5f + new Vector2(J(), J());
            }
            return pts;
        }

        // ---------- chữ ----------

        // chữ từng ô (ít chữ; rỗng = ô không có chữ). Khoá là chuỗi Việt, bảng tiếng Anh Resources/Loc/en/ui.json
        public static string Caption(int i)
        {
            switch (i)
            {
                case 0: return Loc.T("Một đêm giông bão...");
                case 1: return Loc.T("Tỉnh dậy ở một thế giới lạ.");
                case 3: return Loc.T("Những người bạn mới.");
                case 4: return Loc.T("Mỗi đảo một chúa tể.");
                case 5: return Loc.T("Đi chinh phục thôi!");
                default: return "";
            }
        }

        public static StoryIntro Current { get; private set; }

        // Dùng khi dựng prefab (Editor).
        public void Setup(CanvasGroup cg, RectTransform[] pageRts, Panel[] panelParts, ClickCatcher tapCatcher, SketchButton skipButton,
            TextMeshProUGUI hintText)
        {
            group = cg;
            pages = pageRts;
            panels = panelParts;
            tap = tapCatcher;
            skip = skipButton;
            hint = hintText;
        }

        // bản lưu người chơi mới chưa xem (Tutorial.StoryNeeded): App gọi trước màn tải
        public static bool Needed(SaveData s) => Tutorial.StoryNeeded(s);

        // xem lại (Sổ tay, hộp Cách chơi): không ghi cờ
        public static StoryIntro Replay(Action finished = null)
        {
            if (Current || !App.I || !App.I.storyPrefab) return null;
            var st = Instantiate(App.I.storyPrefab);
            st.name = App.I.storyPrefab.name;
            PokiClash.Game.LocService.Tree(st.gameObject);
            st.Play(() =>
            {
                Destroy(st.gameObject);
                finished?.Invoke();
            });
            return st;
        }

        Action onDone;
        int shown; // số ô đã hiện
        bool finishing, tapped;
        readonly float[] revealAt = new float[6];
        Coroutine run;
        Vector2 laidOut;

        void Awake()
        {
            Current = this;
            tap.OnClick = () => tapped = true;
            skip.SetOnClick(Finish);
        }

        void OnDestroy()
        {
            if (Current == this) Current = null;
        }

        public void Play(Action finished)
        {
            onDone = finished;
            run = StartCoroutine(Run());
        }

        // thử trong Editor: như một lần chạm
        public void DebugTap() => tapped = true;

        public bool Done => finishing;

        // cỡ trang = vùng phủ kín màn (cha của các trang, luôn bật)
        Vector2 PageSize => ((RectTransform)pages[0].parent).rect.size;

        // hình ô, viền, chỗ khung lời dẫn theo cỡ màn hiện tại
        void Layout()
        {
            var size = PageSize;
            if (size.x < 1 || size.y < 1) return;
            laidOut = size;
            for (int i = 0; i < panels.Length; i++)
            {
                var pn = panels[i];
                var q = Quad(i, size);
                pn.art.SetQuad(q);
                pn.art.Focus = Focus[i];
                pn.border.Setup(InkLoop(q, i), BorderWidth, 0, 0, true);
                var c = Center(q);
                pn.frame.pivot = new Vector2(c.x / size.x, c.y / size.y); // ô phủ kín trang: dời pivot không dời ô
                if (pn.caption) PlaceCaption(pn, q, CaptionCorner[i], Caption(i));
            }
        }

        // khung lời dẫn: bề rộng theo chữ (tối đa 620 và hẹp hơn ô), đặt sát góc ô rồi dời dần vào tâm cho tới khi nằm gọn trong ô
        void PlaceCaption(Panel pn, Vector2[] q, int corner, string text)
        {
            if (string.IsNullOrEmpty(text)) return;
            var t = pn.captionText;
            t.text = text;
            Vector2 min = q[0], max = q[0];
            foreach (var p in q)
            {
                min = Vector2.Min(min, p);
                max = Vector2.Max(max, p);
            }
            float maxW = Mathf.Min(620, max.x - min.x - 80);
            var pref = t.GetPreferredValues(text, maxW - CaptionPadX * 2, 0);
            var box = new Vector2(Mathf.Min(pref.x, maxW - CaptionPadX * 2) + CaptionPadX * 2, pref.y + CaptionPadY * 2);
            var rt = pn.caption;
            rt.anchorMin = rt.anchorMax = Vector2.zero;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = box;
            var c = Center(q);
            var at = q[corner];
            var pos = at + new Vector2(Mathf.Sign(c.x - at.x) * (box.x * 0.5f + 22), Mathf.Sign(c.y - at.y) * (box.y * 0.5f + 22));
            for (int k = 0; k < 60 && !Inside(q, pos, box, 18); k++) pos += (c - pos).normalized * 6;
            rt.anchoredPosition = pos;
            if (pn.captionBorder)
                pn.captionBorder.Setup(new[] { Vector2.zero, new Vector2(box.x, 0), box, new Vector2(0, box.y) }, 4, 0, 0, true);
        }

        IEnumerator Run()
        {
            shown = 0;
            group.alpha = 0;
            yield return null; // chờ bố cục canvas để đo
            Layout();
            for (int p = 0; p < pages.Length; p++)
            {
                pages[p].gameObject.SetActive(p == 0);
                pages[p].anchoredPosition = Vector2.zero;
            }
            for (int i = 0; i < panels.Length; i++)
            {
                panels[i].frame.gameObject.SetActive(false);
                panels[i].art.SetDrift(1, Vector2.zero);
            }
            hint.gameObject.SetActive(false);
            for (float t = 0; t < 0.45f; t += Time.unscaledDeltaTime)
            {
                group.alpha = t / 0.45f;
                yield return null;
            }
            group.alpha = 1;
            for (int i = 0; i < panels.Length; i++)
            {
                if (i > 0 && i % PerPage == 0) yield return TurnPage(i / PerPage);
                yield return Reveal(i);
                yield return WaitTap();
            }
            Finish();
        }

        IEnumerator WaitTap()
        {
            tapped = false;
            float t0 = Time.unscaledTime;
            while (!tapped)
            {
                // nhắc chạm sau 1,4 giây, chữ nhấp nháy nhẹ
                bool show = Time.unscaledTime - t0 > 1.4f;
                if (hint.gameObject.activeSelf != show) hint.gameObject.SetActive(show);
                if (show) hint.alpha = 0.55f + 0.45f * Mathf.Sin((Time.unscaledTime - t0) * 3f);
                yield return null;
            }
            hint.gameObject.SetActive(false);
        }

        // ô nảy ra từ tâm (to hơn rồi về, vượt nhẹ), hiện dần; rồi chữ lời dẫn chạy dần. Chạm giữa chừng thì hiện xong ngay.
        IEnumerator Reveal(int i)
        {
            var pn = panels[i];
            pn.frame.gameObject.SetActive(true);
            revealAt[i] = Time.unscaledTime;
            shown = i + 1;
            App.Audio?.Play("deal", 0.8f);
            Haptics.Play(Haptic.UiTap);
            var cg = pn.frame.GetComponent<CanvasGroup>();
            string text = Caption(i);
            bool hasText = !string.IsNullOrEmpty(text);
            if (pn.caption) pn.caption.gameObject.SetActive(false);
            tapped = false;
            for (float t = 0; t < 0.32f && !tapped; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.32f;
                float e = 1 - Mathf.Pow(1 - k, 3) + Mathf.Sin(k * Mathf.PI) * 0.06f;
                float s = Mathf.Lerp(1.14f, 1f, e);
                pn.frame.localScale = new Vector3(s, s, 1);
                if (cg) cg.alpha = Mathf.Clamp01(k * 3f);
                yield return null;
            }
            pn.frame.localScale = Vector3.one;
            if (cg) cg.alpha = 1;
            if (hasText && pn.caption)
            {
                pn.caption.gameObject.SetActive(true);
                pn.captionText.text = text;
                pn.captionText.ForceMeshUpdate();
                int n = pn.captionText.textInfo.characterCount;
                bool skipType = tapped;
                for (float t = 0; t < 0.04f * n && !skipType; t += Time.unscaledDeltaTime)
                {
                    pn.captionText.maxVisibleCharacters = Mathf.CeilToInt(t / 0.04f);
                    if (tapped) skipType = true;
                    yield return null;
                }
                pn.captionText.maxVisibleCharacters = 99999;
            }
            tapped = false;
        }

        // sang trang: trang cũ trượt sang trái, trang mới trượt vào từ phải (giữa hai trang lộ nền mực)
        IEnumerator TurnPage(int p)
        {
            var oldP = pages[p - 1];
            var newP = pages[p];
            newP.gameObject.SetActive(true);
            App.Audio?.Play("whoosh", 0.7f);
            float w = PageSize.x + 60;
            for (float t = 0; t < 0.5f; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.5f;
                float e = k * k * (3 - 2 * k);
                oldP.anchoredPosition = new Vector2(-w * e, 0);
                newP.anchoredPosition = new Vector2(w * (1 - e), 0);
                yield return null;
            }
            oldP.gameObject.SetActive(false);
            newP.anchoredPosition = Vector2.zero;
        }

        void Update()
        {
            if (laidOut != Vector2.zero && PageSize != laidOut) Layout(); // đổi cỡ màn (cửa sổ Editor, xoay máy)
            // tranh đã hiện trôi chậm trong ô (phóng nhẹ và lia), mỗi ô một hướng
            for (int i = 0; i < shown && i < panels.Length; i++)
            {
                float t = Mathf.Clamp01((Time.unscaledTime - revealAt[i]) / 9f);
                float e = t * t * (3 - 2 * t);
                var dir = new Vector2(i % 2 == 0 ? -1 : 1, i % 3 == 0 ? 0.6f : -0.4f);
                panels[i].art.SetDrift(1 + 0.03f * e, dir * (10 * e));
            }
        }

        public void Finish()
        {
            if (finishing) return;
            finishing = true;
            if (run != null) StopCoroutine(run);
            StartCoroutine(FadeOut());
        }

        IEnumerator FadeOut()
        {
            group.blocksRaycasts = false;
            for (float t = 0; t < 0.4f; t += Time.unscaledDeltaTime)
            {
                group.alpha = 1 - t / 0.4f;
                yield return null;
            }
            group.alpha = 0;
            var cb = onDone;
            onDone = null;
            cb?.Invoke();
        }
    }
}
