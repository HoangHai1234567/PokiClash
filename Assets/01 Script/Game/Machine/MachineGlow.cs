// Ánh sáng của máy bi (2026-11-10, người dùng cho chép ánh sáng, gradient của máy bi tham khảo): material cộng sáng
// Resources/UIAdditive (shader PokiClash/UIAdditive) và ảnh mềm pk_g_* (ArtGen/Pachinko/sinh_anh_sang.py). Các lớp quầng, tia,
// cột sáng, vệt lia của máy bi, bảng số, màn mở rương đều lấy từ đây. Chưa có ảnh mềm thì không vẽ lớp sáng (trả null).
// Không dựng GameObject lúc chạy (PrefabOnlyTests): ảnh, khung chứa, khung cắt, nút sinh bằng Ui.Spawn từ bộ prefab nhỏ trong Items
// (menu "PokiClash/Prefab/Máy bi: prefab ánh sáng, bảng số, mở rương"); MachineBoard gắn bộ này vào Prefabs lúc Bind.
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public static class MachineGlow
    {
        static Material add;
        static bool tried;

        [System.Serializable]
        public struct Kit
        {
            public Image image; // Items/AnhMayBi: Image trơn; tắt Image thì làm khung chứa
            public RectMask2D mask; // Items/MatNaMayBi: khung cắt
            public Button button; // Items/NutAnhMayBi: Image trong suốt nhận chạm + Button
            public MachineScoreBoard scoreBoard; // Items/BangSoMayBi
            public MachineChestOpen chestOpen; // Items/MoRuongNhom: Canvas riêng + GraphicRaycaster
        }

        public static Kit Prefabs;

        public const string Glow = "pk_g_quang", Ring = "pk_g_vong", Rays = "pk_g_tia", Beam = "pk_g_cot", Sweep = "pk_g_lia",
            Grad = "pk_g_doc", Led = "pk_g_led", Spark = "pk_g_sao";

        public static Material Add
        {
            get
            {
                if (!tried)
                {
                    tried = true;
                    add = Resources.Load<Material>("UIAdditive");
                }
                return add;
            }
        }

        public static Sprite Sprite(string name) => ArtLibrary.Current ? ArtLibrary.Current.Get(name) : null;

        // tên ảnh có tiền tố pk_g_ là ảnh sáng mềm: vẽ cộng sáng
        public static bool IsGlow(string name) => name != null && name.StartsWith("pk_g_");

        // một Image sáng mới (con của parent, neo giữa), cộng sáng nếu additive; null nếu chưa có ảnh hay prefab
        public static Image Make(string name, Transform parent, string sprite, Color color, bool additive = true)
        {
            var s = Sprite(sprite);
            if (!s) return null;
            var img = NewImage(name, parent);
            if (!img) return null;
            img.sprite = s;
            img.color = color;
            if (additive && Add) img.material = Add;
            return img;
        }

        // ảnh thường (không cộng sáng) theo tên trong danh mục; null nếu chưa có
        public static Image MakePlain(string name, Transform parent, string sprite)
        {
            var img = Make(name, parent, sprite, Color.white, false);
            if (img) img.preserveAspect = true;
            return img;
        }

        static T Spawn<T>(T prefab, string name, Transform parent) where T : Component
        {
            if (!prefab) return null;
            var c = Ui.Spawn(prefab, parent);
            c.name = name;
            var rt = (RectTransform)c.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = Vector2.zero;
            rt.localScale = Vector3.one;
            rt.localRotation = Quaternion.identity;
            return c;
        }

        // Image trơn (không nhận chạm, vật liệu mặc định); null nếu chưa có prefab
        public static Image NewImage(string name, Transform parent)
        {
            var img = Spawn(Prefabs.image, name, parent);
            if (img) img.raycastTarget = false;
            return img;
        }

        // khung chứa (Image tắt)
        public static RectTransform NewRect(string name, Transform parent)
        {
            var img = NewImage(name, parent);
            if (!img) return null;
            img.enabled = false;
            return img.rectTransform;
        }

        // khung cắt con theo khung (RectMask2D)
        public static RectTransform NewMask(string name, Transform parent)
        {
            var m = Spawn(Prefabs.mask, name, parent);
            return m ? m.rectTransform : null;
        }

        // nút: Image trong suốt nhận chạm, không đổi màu khi bấm
        public static Button NewButton(string name, Transform parent) => Spawn(Prefabs.button, name, parent);

        public static Color A(Color c, float a)
        {
            c.a = a;
            return c;
        }

        public static Color Hex(string hex, float a = 1) => A(Theme.Hex(hex), a);
    }
}
