// Khung hình tướng: tỉ lệ 4:5, chân ở 6% đáy (chân dung aola dựng theo khung này, tools/portrait_png.py). Hình giữ chỗ vẽ tay
// theo hệ đã bỏ (2026-11-02): không có hình aola thì ô tướng để trống.
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public static class HeroArt
    {
        public const int W = 192, H = 240;
        // vị trí bụng (tâm biểu tượng) và chân theo tỉ lệ khung ảnh, gốc dưới trái
        public static readonly Vector2 Belly = new Vector2(0.5f, 0.43f);
        public const float FootY = 0.06f; // chân chạm đất ở 6% chiều cao ảnh

        // ---------- dùng trong UI ----------

        // Dạng của tướng trong dòng tiến hóa: star > 0 là sao đã biết (tướng trên sân, địch: Teams.EnemyStar); không thì sao của
        // người chơi nếu đã có tướng, chưa có thì dạng 1.
        public static HeroForm FormOf(HeroDef h, int star = 0)
        {
            if (star <= 0)
            {
                var p = App.Save?.Data?.Hero(h.id);
                star = p != null && p.owned ? p.star : 1;
            }
            return App.Data != null ? App.Data.Cfg.FormOf(h, star) : h.Form(new int[0], star);
        }

        // Chân dung tướng (prefab kit ChanDung), cao height, gốc ở chân; star như FormOf.
        public static RectTransform Portrait(Transform parent, HeroDef h, float height, bool silhouette = false, int star = 0)
        {
            var p = Ui.Spawn(Theme.Prefabs.portrait, parent);
            p.Bind(h, height, silhouette, star);
            return p.Rect;
        }
    }
}
