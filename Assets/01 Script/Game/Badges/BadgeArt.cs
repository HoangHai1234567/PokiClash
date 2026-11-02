// Hình huy hiệu (chưa có ảnh gen ở ArtGen/SideMeta): huy chương tô màu theo bậc, biểu tượng hệ ở giữa (prefab kit HuyHieu).
// Bậc 0 (chưa có) là bóng xám mờ.
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public static class BadgeArt
    {
        // Đồng, Bạc, Vàng, Ngọc, Kim Cương
        static readonly Color[] TierColors =
        {
            Theme.Hex("#c98a4a"), Theme.Hex("#c9d3dc"), Theme.Hex("#f7c948"), Theme.Hex("#6fd3a8"), Theme.Hex("#8fe0ff"),
        };

        public static Color ColorOf(int tier) => tier > 0 ? TierColors[Mathf.Min(tier, TierColors.Length) - 1] : new Color(0.72f, 0.68f, 0.6f, 0.55f);

        // huy hiệu hệ e bậc tier (prefab kit HuyHieu), cao size (rộng theo tỉ lệ hình)
        public static RectTransform Icon(Transform parent, Elem e, int tier, float size)
        {
            var b = Ui.Spawn(Theme.Prefabs.badge, parent);
            b.Bind(e, tier, size);
            return b.Rect;
        }
    }
}
