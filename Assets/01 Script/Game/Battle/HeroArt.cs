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

        // Mặt tướng vẽ tay cho màn VS (gói ArtGen/BattleIntro): Resources/HeroFaces/mat_<aola>.png theo dạng (star như FormOf), nạp khi
        // cần; dạng chưa có ảnh mặt thì null (màn VS cắt chân dung: FitHead).
        public static Sprite Face(HeroDef h, int star = 0)
        {
            var aola = FormOf(h, star).aola;
            return string.IsNullOrEmpty(aola) ? null : Resources.Load<Sprite>("HeroFaces/mat_" + aola);
        }

        // Chân dung thay mặt trong ô cỡ box (prefab kit ChanDung, con của ô, gốc ở giữa ô): phóng sao cho phần trên của hình (đầu, ~62%
        // chiều cao hình) lấp ô, đỉnh đầu sát mép trên, căn giữa theo hình; hình dẹt ngang (cua, cá) thì không phóng quá bề ngang ô
        // (thấy cả con, mắt nằm giữa thân) và căn giữa theo chiều cao. Hình to nhỏ trong khung ảnh khác nhau (lính nhỏ, boss to) nên đo
        // hộp phần có hình của từng ảnh (PortraitBoxes, đo sẵn trong Editor).
        public static void FitHead(HeroPortrait p, HeroDef h, int star, Vector2 box)
        {
            var c = PortraitBoxes.Of(FormOf(h, star).aola);
            const float aspect = W / (float)H;
            float height = Mathf.Min(box.y / (c.height * 0.62f + 0.05f), box.x / (c.width * aspect * 0.92f));
            height = Mathf.Clamp(height, box.y * 1.2f, box.y * 4.5f);
            p.Bind(h, height, false, star);
            var rt = p.Rect;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.pivot = new Vector2(0.5f, 0);
            float y = c.height * height < box.y * 0.88f ? -c.center.y * height : box.y / 2 - box.y * 0.06f - c.yMax * height;
            rt.anchoredPosition = new Vector2((0.5f - c.center.x) * height * aspect, y);
        }
    }
}
