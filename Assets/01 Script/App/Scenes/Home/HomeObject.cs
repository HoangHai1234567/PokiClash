// Một vật trên bản đồ Nhà (prefab Items/NhaVat, dựng bằng menu "PokiClash/Prefab/Nhà và side meta/Nhà: dựng màn"): công trình, trang trí, khối rừng,
// bóng ma lúc xây. Ảnh neo ở góc dưới chân thoi (pivot lấy từ home_art.json); nhãn nổi trên đầu (tên, cấp, giờ còn lại); bong bóng
// báo có đồ để thu (Cây bi: bong bóng có số bi đang có, kiểu Clash of Critters). HomeScene đặt vị trí, cỡ và thứ tự vẽ.
// - Chọn (người dùng 2026-11-22): nhún (Bounce: nén rồi giãn quanh chân, tắt dần) và đổi vật liệu sáng nhẹ PokiClash/UIHomeSelect
//   (Select; độ sáng là biến toàn cục _HomeSel do HomeScene đặt). Đổi ảnh (Place) giữ vật liệu chọn.
// - Bong bóng: hiện thì nảy ra, lơ lửng nhẹ lên xuống; thu xong thì nảy to rồi tắt (Pop).
using System;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using Random = UnityEngine.Random;

namespace PokiClash
{
    public sealed class HomeObject : MonoBehaviour
    {
        [SerializeField] Image img;
        [SerializeField] TextMeshProUGUI label;
        [SerializeField] Image bubble, bubbleIcon;
        [SerializeField] TextMeshProUGUI bubbleCount; // số trong bong bóng (Cây bi); trống thì bong bóng chỉ có icon
        // vòng tiến độ quanh icon (kiểu bong bóng nông trại của Clash of Critters: vòng xanh chạy theo lượng chờ thu, đầy thì phập phồng);
        // nền vòng mờ dưới, vòng đầy dần (Image Filled Radial360) trên
        [SerializeField] Image bubbleTrack, bubbleFill;
        [SerializeField] ClickCatcher bubbleTap; // chạm bong bóng là thu (HomeScene gán BubbleTapped)

        public RectTransform Rt => (RectTransform)transform;
        public Action<HomeObject> BubbleTapped; // chạm bong bóng
        float fill = -1; // -1 = không vòng
        bool full;
        public Image Img => img;
        public int Id { get; set; } = -1; // công trình (id) hoặc -2 - ô rừng
        public float Depth { get; set; } // y góc dưới (px từ trên xuống): lớn hơn vẽ sau

        Material selMat;
        float bounceT = -1, bounceK = 1;
        float bubbleInT = -1, bubbleOutT = -1, bobPhase;
        Vector2 bubbleBase, bubbleSize0;
        bool bubbleInit;

        const float BounceLen = 0.8f;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Image image, TextMeshProUGUI text, Image bubbleBg, Image icon)
        {
            img = image;
            label = text;
            bubble = bubbleBg;
            bubbleIcon = icon;
        }

        // Dùng khi dựng prefab (Editor): số trong bong bóng
        public void SetupCount(TextMeshProUGUI count) => bubbleCount = count;

        // Dùng khi dựng prefab (Editor): vòng tiến độ và chỗ chạm của bong bóng
        public void SetupRing(Image track, Image fillImg, ClickCatcher tapCatcher)
        {
            bubbleTrack = track;
            bubbleFill = fillImg;
            bubbleTap = tapCatcher;
        }

        void Awake()
        {
            bobPhase = Random.value * 6.28f;
            InitBubble();
            if (bubbleTap) bubbleTap.OnClick = () => BubbleTapped?.Invoke(this);
        }

        // vòng tiến độ: 0..1 (đầy = 1, đổi màu và phập phồng), âm = tắt vòng (Cây bi có số)
        public void Fill(float k)
        {
            fill = k;
            full = k >= 1 - 1e-4f;
            bool on = k >= 0;
            if (bubbleTrack) bubbleTrack.gameObject.SetActive(on);
            if (!bubbleFill) return;
            bubbleFill.gameObject.SetActive(on);
            if (!on) return;
            bubbleFill.fillAmount = Mathf.Clamp01(k);
            bubbleFill.color = full ? Theme.Orange : Theme.Green;
        }

        void InitBubble()
        {
            if (bubbleInit || !bubble) return;
            bubbleInit = true;
            bubbleBase = bubble.rectTransform.anchoredPosition;
            bubbleSize0 = bubble.rectTransform.sizeDelta;
        }

        // sprite, cỡ hiển thị (px), pivot (góc dưới chân thoi), toạ độ góc dưới tính từ góc trên trái bản đồ (y xuống)
        public void Place(Sprite s, Vector2 size, Vector2 pivot, Vector2 at)
        {
            Theme.SetSprite(img, s);
            if (selMat) img.material = selMat; // đang chọn: giữ sáng
            img.preserveAspect = false;
            var rt = Rt;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = pivot;
            rt.sizeDelta = size;
            rt.anchoredPosition = new Vector2(at.x, -at.y);
            Depth = at.y;
        }

        public void Tint(Color c) => img.color = c;

        public void Label(string text)
        {
            if (!label) return;
            label.gameObject.SetActive(!string.IsNullOrEmpty(text));
            label.text = text ?? "";
        }

        // bong bóng trên đầu: icon (null = tắt), count = số đi kèm (Cây bi; null = chỉ icon)
        public void Bubble(Sprite icon, string count = null)
        {
            if (!bubble) return;
            InitBubble();
            if (!icon)
            {
                // đang nảy tắt (vừa thu): để nảy xong tự tắt
                if (bubbleOutT < 0) bubble.gameObject.SetActive(false);
                return;
            }
            bool was = bubble.gameObject.activeSelf && bubbleOutT < 0;
            bubbleOutT = -1;
            bubble.gameObject.SetActive(true);
            if (bubbleIcon) Theme.SetSprite(bubbleIcon, icon);
            LayoutBubble(count);
            if (!was)
            {
                bubbleInT = 0; // vừa hiện: nảy ra
                bubble.rectTransform.localScale = Vector3.zero;
            }
        }

        // không số: tròn 84 x 84, icon phủ (cách mép 14) như prefab; có số: viên dài, icon bên trái, số bên phải
        void LayoutBubble(string count)
        {
            var brt = bubble.rectTransform;
            var irt = bubbleIcon ? bubbleIcon.rectTransform : null;
            bool num = bubbleCount && !string.IsNullOrEmpty(count);
            if (bubbleCount) bubbleCount.gameObject.SetActive(num);
            if (!num)
            {
                brt.sizeDelta = bubbleSize0;
                if (irt)
                {
                    irt.anchorMin = Vector2.zero;
                    irt.anchorMax = Vector2.one;
                    irt.pivot = new Vector2(0.5f, 0.5f);
                    irt.offsetMin = new Vector2(14, 14);
                    irt.offsetMax = new Vector2(-14, -14);
                }
                return;
            }
            const float H = 76, Pad = 12, IconS = 54, Gap = 4;
            bubbleCount.text = count;
            float tw = Mathf.Ceil(bubbleCount.GetPreferredValues(count).x);
            if (irt)
            {
                irt.anchorMin = irt.anchorMax = new Vector2(0, 0.5f);
                irt.pivot = new Vector2(0, 0.5f);
                irt.sizeDelta = new Vector2(IconS, IconS);
                irt.anchoredPosition = new Vector2(Pad, 0);
            }
            var crt = bubbleCount.rectTransform;
            crt.anchorMin = crt.anchorMax = new Vector2(0, 0.5f);
            crt.pivot = new Vector2(0, 0.5f);
            crt.sizeDelta = new Vector2(tw + 4, H - 12);
            crt.anchoredPosition = new Vector2(Pad + IconS + Gap, 2);
            brt.sizeDelta = new Vector2(Pad + IconS + Gap + tw + Pad + 6, H);
        }

        public bool BubbleOn => bubble && bubble.gameObject.activeSelf && bubbleOutT < 0;

        // tâm bong bóng (toạ độ thế giới) nếu đang hiện, không thì đỉnh giữa ảnh: chỗ đồ thu được bay ra
        public Vector3 BubbleWorld()
        {
            if (BubbleOn) return bubble.rectTransform.TransformPoint(bubble.rectTransform.rect.center);
            var r = Rt.rect;
            return Rt.TransformPoint(new Vector3(r.center.x, r.yMax - r.height * 0.25f, 0));
        }

        // thu xong: bong bóng nảy to rồi tắt
        public void PopBubble()
        {
            if (!BubbleOn) return;
            bubbleInT = -1;
            bubbleOutT = 0;
        }

        // chọn / bỏ chọn: vật liệu sáng nhẹ (null = như thường); nhún do HomeScene gọi Bounce riêng
        public void Select(Material m)
        {
            if (m == selMat) return;
            selMat = m;
            if (img) Theme.SetSprite(img, img.sprite); // trả vật liệu hợp ảnh (Plain / Kit)
            if (m && img) img.material = m;
        }

        // nhún: nén xuống rồi giãn lên quanh chân (pivot), tắt dần trong BounceLen giây; k: độ mạnh
        public void Bounce(float k = 1)
        {
            bounceT = 0;
            bounceK = k;
        }

        void Update()
        {
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            if (bounceT >= 0)
            {
                bounceT += dt;
                if (bounceT >= BounceLen)
                {
                    bounceT = -1;
                    transform.localScale = Vector3.one;
                }
                else transform.localScale = Squash(bounceT, bounceK);
            }
            if (!bubble || !bubble.gameObject.activeSelf) return;
            var brt = bubble.rectTransform;
            brt.anchoredPosition = bubbleBase + new Vector2(0, 5f * Mathf.Sin(Time.unscaledTime * 2.4f + bobPhase)); // lơ lửng
            // kho đầy: phập phồng cho thấy nên thu (chỉ khi không đang nảy vào / ra)
            if (bubbleInT < 0 && bubbleOutT < 0)
                brt.localScale = full && fill >= 0 ? Vector3.one * (1 + 0.07f * Mathf.Max(0, Mathf.Sin(Time.unscaledTime * 5.2f + bobPhase))) : Vector3.one;
            if (bubbleOutT >= 0)
            {
                bubbleOutT += dt;
                const float L = 0.22f;
                float t = bubbleOutT / L;
                float s = t < 0.35f ? Mathf.Lerp(1f, 1.25f, t / 0.35f) : Mathf.Lerp(1.25f, 0f, (t - 0.35f) / 0.65f);
                brt.localScale = Vector3.one * Mathf.Max(0, s);
                if (bubbleOutT >= L)
                {
                    bubbleOutT = -1;
                    brt.localScale = Vector3.one;
                    bubble.gameObject.SetActive(false);
                }
            }
            else if (bubbleInT >= 0)
            {
                bubbleInT += dt;
                const float L = 0.3f;
                float t = bubbleInT / L;
                float s = t < 0.55f ? Mathf.Lerp(0f, 1.15f, t / 0.55f) : Mathf.Lerp(1.15f, 1f, (t - 0.55f) / 0.45f);
                brt.localScale = Vector3.one * s;
                if (bubbleInT >= L)
                {
                    bubbleInT = -1;
                    brt.localScale = Vector3.one;
                }
            }
        }

        // nén giãn giữ thể tích: lò xo tắt dần bắt đầu bằng nén (cao 0,9, rộng 1,05), rồi giãn (cao ~1,04), rồi êm
        public static Vector3 Squash(float t, float k)
        {
            float f = -Mathf.Sin(t * Mathf.PI * 2 * 2.6f) * Mathf.Exp(-t * 4.5f);
            float y = 1 + 0.15f * k * f;
            float x = 1 - 0.5f * 0.15f * k * f;
            return new Vector3(x, y, 1);
        }

        void OnDisable()
        {
            bounceT = -1;
            transform.localScale = Vector3.one;
            if (bubble && bubbleOutT >= 0)
            {
                bubbleOutT = -1;
                bubble.rectTransform.localScale = Vector3.one;
                bubble.gameObject.SetActive(false);
            }
        }
    }
}
