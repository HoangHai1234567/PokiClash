// Chân dung tướng: ảnh aola (bóng sẫm nếu chưa có tướng), gốc ở chân; không có ảnh aola thì ô trống. emblem không dùng nữa
// (là biểu tượng trên bụng hình giữ chỗ cũ), luôn ẩn.
// Prefab Assets/04 Prefabs/Kit/ChanDung.
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HeroPortrait : MonoBehaviour
    {
        [SerializeField] Image body, emblem;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bodyImg, Image emblemImg)
        {
            body = bodyImg;
            emblem = emblemImg;
        }

        // cao height; silhouette: bóng sẫm. Hình là chân dung aola trong prefab tướng (AolaActor.Portrait); dạng chưa nhập thì ô
        // để trống (đã bỏ hình giữ chỗ vẽ tay theo hệ, người dùng chốt 2026-11-02).
        // star: chọn dạng trong dòng tiến hóa (HeroArt.FormOf: 0 là sao của người chơi)
        public void Bind(HeroDef h, float height, bool silhouette = false, int star = 0)
        {
            name = "chan_dung_" + h.id;
            Rect.sizeDelta = new Vector2(height * HeroArt.W / HeroArt.H, height);
            emblem.gameObject.SetActive(false);
            var aola = Game.AolaActor.Portrait(HeroArt.FormOf(h, star).aola);
            body.enabled = aola;
            if (!aola) return;
            Theme.SetSprite(body, aola);
            body.preserveAspect = false; // ảnh lưu vuông 512x512 kéo giãn từ khung 4:5 (AolaImport.PortraitSide): khung ô trả lại 4:5
            body.color = silhouette ? Theme.Hex("#4a3c30") : Color.white;
        }
    }
}
