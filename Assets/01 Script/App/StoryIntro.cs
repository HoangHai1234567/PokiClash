// Đoạn cốt truyện mở đầu (GD_Claude/25_FTUE.md mục 11): chạy lần đầu vào game, trước màn tải con tàu; học trang truyện tranh mở đầu
// Kingdom Rush. Hai trang sổ, mỗi trang 3 khung tranh: chạm một lần hiện một khung (khung đập xuống nghiêng nhẹ, tranh trôi chậm), một
// dòng chữ ngắn chạy dần trên băng giấy; hết trang 1 thì lật sang trang 2; chạm sau khung cuối là xong. Nút "Bỏ qua" ở góc. Chạm lúc
// khung đang hiện thì hiện xong ngay. Xem lại ở Sổ tay, hộp Cách chơi.
// Prefab Assets/04 Prefabs/Screens/CotTruyen (canvas riêng thứ tự 25: trên mây và hộp thoại), dựng bằng menu "PokiClash/Prefab/Cốt
// truyện mở đầu (CotTruyen)", gán App.storyPrefab. Ảnh khung ở Assets/03 Art/Story/khung_1..6.png (gói GPT ArtGen/Story/build_story.py);
// chưa có thì menu tạm gắn ảnh đảo có sẵn.
using System;
using System.Collections;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class StoryIntro : MonoBehaviour
    {
        [Serializable]
        public struct Panel
        {
            public RectTransform frame; // khung giấy viền mực (đập xuống lúc hiện)
            public RectTransform window; // vùng cắt tranh (Mask, chịu được khung nghiêng)
            public Image art; // tranh (phủ kín vùng cắt, trôi chậm)
            public RectTransform caption; // băng giấy chữ (ẩn nếu khung không có chữ)
            public TextMeshProUGUI captionText;
            public float tilt; // độ nghiêng cuối
        }

        [SerializeField] CanvasGroup group;
        [SerializeField] RectTransform book; // chứa hai trang, co lại vừa màn thấp
        [SerializeField] RectTransform[] pages = new RectTransform[2];
        [SerializeField] Panel[] panels = new Panel[6];
        [SerializeField] ClickCatcher tap;
        [SerializeField] SketchButton skip;
        [SerializeField] TextMeshProUGUI hint;

        public const int PerPage = 3;

        // chữ từng khung (ít chữ; rỗng = khung không có chữ). Khoá là chuỗi Việt, bảng tiếng Anh Resources/Loc/en/ui.json
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
        public void Setup(CanvasGroup cg, RectTransform bookRt, RectTransform[] pageRts, Panel[] panelParts, ClickCatcher tapCatcher,
            SketchButton skipButton, TextMeshProUGUI hintText)
        {
            group = cg;
            book = bookRt;
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
        int shown; // số khung đã hiện
        bool finishing, tapped;
        readonly float[] revealAt = new float[6];
        Coroutine run;

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

        IEnumerator Run()
        {
            shown = 0;
            group.alpha = 0;
            yield return null; // chờ bố cục canvas để đo
            var area = book.parent as RectTransform;
            if (area)
            {
                float k = Mathf.Min(1f, area.rect.height / (book.sizeDelta.y + 90), area.rect.width / (book.sizeDelta.x + 40));
                book.localScale = new Vector3(k, k, 1);
            }
            for (int p = 0; p < pages.Length; p++)
            {
                pages[p].gameObject.SetActive(p == 0);
                pages[p].anchoredPosition = Vector2.zero;
                pages[p].localEulerAngles = Vector3.zero;
            }
            for (int i = 0; i < panels.Length; i++)
            {
                panels[i].frame.gameObject.SetActive(false);
                Cover(panels[i]);
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

        // khung đập xuống: từ to và nghiêng về đúng chỗ, nảy nhẹ; rồi chữ chạy dần. Chạm giữa chừng thì hiện xong ngay.
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
            float startTilt = pn.tilt + (i % 2 == 0 ? -7 : 7);
            for (float t = 0; t < 0.38f && !tapped; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.38f;
                float e = 1 - Mathf.Pow(1 - k, 3) + Mathf.Sin(k * Mathf.PI) * 0.08f; // vượt nhẹ rồi về
                float s = Mathf.Lerp(1.22f, 1f, e);
                pn.frame.localScale = new Vector3(s, s, 1);
                pn.frame.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(startTilt, pn.tilt, e));
                if (cg) cg.alpha = Mathf.Clamp01(k * 2.5f);
                yield return null;
            }
            pn.frame.localScale = Vector3.one;
            pn.frame.localEulerAngles = new Vector3(0, 0, pn.tilt);
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

        // lật trang: trang cũ trượt sang trái và nghiêng, trang mới trượt vào từ phải
        IEnumerator TurnPage(int p)
        {
            var oldP = pages[p - 1];
            var newP = pages[p];
            newP.gameObject.SetActive(true);
            App.Audio?.Play("whoosh", 0.7f);
            float w = 1300;
            for (float t = 0; t < 0.5f; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.5f;
                float e = k * k * (3 - 2 * k);
                oldP.anchoredPosition = new Vector2(-w * e, 40 * Mathf.Sin(e * Mathf.PI));
                oldP.localEulerAngles = new Vector3(0, 0, 8 * e);
                newP.anchoredPosition = new Vector2(w * (1 - e), 0);
                newP.localEulerAngles = new Vector3(0, 0, -6 * (1 - e));
                yield return null;
            }
            oldP.gameObject.SetActive(false);
            newP.anchoredPosition = Vector2.zero;
            newP.localEulerAngles = Vector3.zero;
        }

        // tranh phủ kín vùng cắt (giữ tỉ lệ ảnh), chừa 12% để trôi (phóng 5% và lia 14 không lộ mép)
        static void Cover(Panel pn)
        {
            if (!pn.art || !pn.window) return;
            var sp = pn.art.sprite;
            var size = pn.window.rect.size;
            if (size.x < 1 || size.y < 1) size = pn.window.sizeDelta;
            float aspect = sp ? sp.rect.width / Mathf.Max(1, sp.rect.height) : size.x / Mathf.Max(1, size.y);
            var rt = pn.art.rectTransform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            float w = Mathf.Max(size.x, size.y * aspect), h = w / aspect;
            if (h < size.y)
            {
                h = size.y;
                w = h * aspect;
            }
            rt.sizeDelta = new Vector2(w, h) * 1.12f;
            rt.anchoredPosition = Vector2.zero;
        }

        void Update()
        {
            // tranh đã hiện trôi chậm (phóng nhẹ và lia), mỗi khung một hướng
            for (int i = 0; i < shown && i < panels.Length; i++)
            {
                var art = panels[i].art;
                if (!art) continue;
                float t = Mathf.Clamp01((Time.unscaledTime - revealAt[i]) / 9f);
                float e = t * t * (3 - 2 * t);
                float s = 1 + 0.05f * e;
                art.rectTransform.localScale = new Vector3(s, s, 1);
                var dir = new Vector2(i % 2 == 0 ? -1 : 1, i % 3 == 0 ? 0.6f : -0.4f);
                art.rectTransform.anchoredPosition = dir * (14 * e);
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
