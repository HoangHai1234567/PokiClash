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

        // màu sao theo bậc (Core.StarTier): Đồng, Bạc, Vàng, Kim Cương
        public static readonly Color[] TierColors =
        {
            new Color32(0xc9, 0x86, 0x4a, 0xff), new Color32(0xb9, 0xc6, 0xd0, 0xff), new Color32(0xff, 0xc9, 0x3c, 0xff), new Color32(0x7c, 0xd8, 0xff, 0xff),
        };

        public static Color TierColor(int tier) => TierColors[Mathf.Clamp(tier, 0, TierColors.Length - 1)];

        // sao tổng (1..StarTier.MaxStar): 5 sao, tô số sao trong bậc bằng màu của bậc (Đồng 3★ = 3 sao đồng, 2 sao trống)
        public void SetTiered(int star) => SetTier(Core.StarTier.Tier(star), Core.StarTier.InTier(star));

        // n sao (0..5) của bậc tier tô màu bậc, còn lại trống (mốc bậc chưa tới trên thanh tiến hóa: 0 sao)
        public void SetTier(int tier, int n)
        {
            int max = Core.StarTier.PerTier;
            var c = TierColor(tier);
            for (int i = 0; i < stars.Length; i++)
            {
                stars[i].gameObject.SetActive(i < max);
                stars[i].color = i < n ? c : Theme.Paper3;
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
