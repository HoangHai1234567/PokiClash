// Nút khay chế độ Xây của màn Nhà có icon công trình (người dùng 2026-11-20: "gen thêm icon các building"): biến thể prefab của nút
// nhỏ kit (Kit/Nut_Nho) thêm ảnh "icon" bên trái, chữ dời sang phải; prefab Items/NutKhayNha dựng bằng menu
// "PokiClash/Prefab/Nhà: nút khay có icon công trình" (Editor/HomeTrayMenu). Icon: icon_home_<mã công trình> (ArtGen/Home/icons).
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HomeTrayItem : MonoBehaviour
    {
        [SerializeField] SketchButton button;
        [SerializeField] Image icon;

        public SketchButton Button => button;

        // Dùng khi nướng prefab (Editor).
        public void Setup(SketchButton b, Image i)
        {
            button = b;
            icon = i;
        }

        // icon công trình; null thì ẩn ảnh. Nút khoá (chưa đủ điều kiện) thì icon nhạt theo nút
        public void SetIcon(Sprite s, bool on)
        {
            if (!icon) return;
            icon.sprite = s;
            icon.enabled = s;
            icon.color = on ? Color.white : new Color(1, 1, 1, 0.55f);
        }
    }
}
