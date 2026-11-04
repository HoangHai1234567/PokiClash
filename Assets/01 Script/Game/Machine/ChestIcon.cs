// Hình rương, prefab kit Kit/Ruong. Bind đặt loại, bề rộng, màu thân.
// Có ảnh gen (ArtGen/Pachinko, "build.py --duyet ruong": pk_ruong_go / _bac / _vang, bản mở thêm "_mo") thì dùng ảnh đó, bỏ khoá
// vẽ tạm; không thì vẽ tạm như cũ (thân giấy tô màu + khoá tròn, vật liệu UIKit). Rương có màu riêng (fill, rương AFK) giữ hình
// vẽ tạm cho khỏi mất màu. Open(): đổi sang ảnh rương mở, giữ bề rộng và mép đáy (bản mở cao hơn vì có nắp lật và sao).
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ChestIcon : MonoBehaviour
    {
        [SerializeField] Image body, lockImg;

        public RectTransform Rect => (RectTransform)transform;
        public SlotKind Kind { get; private set; }

        Sprite sketch; // hình vẽ tạm của prefab (khi ảnh gen chưa có)
        Material sketchMat;
        bool art;
        float openShift; // Open() nhích lên giữ mép đáy; Bind sau đó trả lại (hộp mở rương dùng lại một icon cho nhiều rương)

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bodyImg, Image lockImage)
        {
            body = bodyImg;
            lockImg = lockImage;
        }

        static string ArtName(SlotKind kind) =>
            kind == SlotKind.ChestGold ? "pk_ruong_vang" : kind == SlotKind.ChestSilver ? "pk_ruong_bac" : "pk_ruong_go";

        static Sprite Art(string name) => ArtLibrary.Current && ArtLibrary.Current.HasArt(name) ? ArtLibrary.Current.Get(name) : null;

        public ChestIcon Bind(SlotKind kind, float w, Color? fill = null)
        {
            Kind = kind;
            name = "ruong_" + Pachinko.Key(kind);
            if (openShift != 0)
            {
                Rect.anchoredPosition -= new Vector2(0, openShift);
                openShift = 0;
            }
            if (!sketch)
            {
                sketch = body.sprite;
                sketchMat = body.material;
            }
            var sprite = fill == null ? Art(ArtName(kind)) : null;
            art = sprite;
            lockImg.gameObject.SetActive(!art);
            if (art)
            {
                body.sprite = sprite;
                body.material = null;
                body.color = Color.white;
                body.preserveAspect = true;
                Rect.sizeDelta = new Vector2(w, w * sprite.rect.height / sprite.rect.width);
                return this;
            }
            body.sprite = sketch;
            body.material = sketchMat;
            body.preserveAspect = false;
            body.color = fill ?? MachineBoard.ChestColor(kind);
            Rect.sizeDelta = new Vector2(w, w * 88 / 96f);
            lockImg.color = kind == SlotKind.ChestGold ? Theme.Orange : Theme.Hex("#ffd24a");
            lockImg.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -w * 0.05f), new Vector2(w * 0.22f, w * 0.22f));
            return this;
        }

        // rương bật nắp (hộp mở rương): ảnh rương mở nếu có
        public void Open()
        {
            var sprite = art ? Art(ArtName(Kind) + "_mo") : null;
            if (!sprite) return;
            var size = Rect.sizeDelta;
            float h = size.x * sprite.rect.height / sprite.rect.width;
            body.sprite = sprite;
            float shift = (h - size.y) * Rect.pivot.y;
            Rect.anchoredPosition += new Vector2(0, shift);
            openShift += shift;
            Rect.sizeDelta = new Vector2(size.x, h);
        }
    }
}
