// Hàng sao (có / chưa có). Prefab Assets/04 Prefabs/Kit/Sao: 5 sao cỡ 36, xếp ngang.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.UI
{
    public sealed class UiStars : MonoBehaviour
    {
        [SerializeField] Image[] stars;
        [SerializeField] HorizontalLayoutGroup row;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image[] images, HorizontalLayoutGroup layout)
        {
            stars = images;
            row = layout;
        }

        // n sao vàng trên tổng max (max không quá số sao của prefab)
        public void Set(int n, int max)
        {
            for (int i = 0; i < stars.Length; i++)
            {
                stars[i].gameObject.SetActive(i < max);
                stars[i].color = i < n ? Theme.Yellow : Theme.Paper3;
            }
            Rect.sizeDelta = new Vector2(Mathf.Min(max, stars.Length) * Size * 0.9f, Size);
        }

        // màu sao theo bậc (Core.StarTier): Đồng, Bạc, Vàng, Kim Cương. 2026-11-19 (người dùng: sao cần hiện rõ hơn): Bạc ngả xanh thép
        // đậm hơn để khỏi lẫn với sao trống trên nền giấy
        public static readonly Color[] TierColors =
        {
            new Color32(0xd0, 0x84, 0x3c, 0xff), new Color32(0x9f, 0xb6, 0xcc, 0xff), new Color32(0xff, 0xc4, 0x2a, 0xff), new Color32(0x6c, 0xd2, 0xff, 0xff),
        };

        public static Color TierColor(int tier) => TierColors[Mathf.Clamp(tier, 0, TierColors.Length - 1)];

        // sao chưa có: ruột giấy, cả sao (cả viền) mờ để sao đã có nổi hẳn lên
        public static readonly Color Empty = new Color(0.9f, 0.83f, 0.66f, 0.42f);

        // sao tổng (1..StarTier.MaxStar) theo thang 4 bậc chung (chỗ không biết tướng): 5 sao, tô số sao trong bậc bằng màu của bậc
        public void SetTiered(int star) => SetTier(Core.StarTier.Tier(star), Core.StarTier.InTier(star));

        // sao tổng theo bậc của tướng (bậc theo dạng 2026-11-19: tướng 2 dạng chỉ có Đồng, Bạc; Core.StarTier.Stops)
        public void SetTiered(Core.BalanceConfig cfg, Core.HeroDef hero, int star) =>
            SetTier(Core.StarTier.TierOf(cfg, hero, star), Core.StarTier.InTierOf(cfg, hero, star));

        // n sao (0..5) của bậc tier tô màu bậc, còn lại trống (mốc bậc chưa tới trên thanh tiến hóa: 0 sao)
        public void SetTier(int tier, int n)
        {
            int max = Core.StarTier.PerTier;
            var c = TierColor(tier);
            for (int i = 0; i < stars.Length; i++)
            {
                stars[i].gameObject.SetActive(i < max);
                stars[i].color = i < n ? c : Empty;
            }
            Rect.sizeDelta = new Vector2(Mathf.Min(max, stars.Length) * Size * 0.9f, Size);
        }

        float Size => stars.Length > 0 ? stars[0].rectTransform.sizeDelta.x : 36;

        public void SetSize(float size)
        {
            row.spacing = -size * 0.12f;
            foreach (var s in stars) s.rectTransform.sizeDelta = new Vector2(size, size);
        }
    }
}
