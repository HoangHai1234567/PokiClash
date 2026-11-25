// HIỆN HIỆU ỨNG PREFAB GỐC TRÊN SÂN (2026-11-25, cầu ma thủy Thôn Kình, hướng A): RawImage ở lớp hạt TRƯỚC (HatTruoc) của sân đấu / ô xem tướng,
// texture = RenderTexture của CauMaRig, material shader PokiClash/UIVeTayRT (dải phẳng + vân chì + quầng ngoại lệ), mỗi hệ một material
// (2026-11-25: cầu ma đổi màu cho Mộc, Hỏa). Đặt sẵn trong prefab bằng
// menu CauMaRigMenu (không tạo GameObject lúc chạy; rig sinh từ prefab ở góc xa thế giới, huỷ cùng thành phần này).
// HatLua (NCauMa) gọi Bat → mỗi khung Ve (vị trí, cỡ theo toạ độ UI của lớp hạt, độ hiện, giây sân vừa qua) → Tat.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class CauMaHien : MonoBehaviour
    {
        [SerializeField] RawImage img;
        [SerializeField] CauMaRig rigPrefab;
        [SerializeField] Material[] matHe; // material theo hệ (HatLua.CauMaThuy / CauMaMoc / CauMaHoa), menu CauMaRigMenu
        static readonly Vector3 GocXa = new Vector3(20000, 20000, 0); // ngoài tầm camera UI

        CauMaRig rig;

        public bool San => img && rigPrefab;

        public void Setup(RawImage i, CauMaRig prefab, Material[] mats)
        {
            img = i;
            rigPrefab = prefab;
            matHe = mats;
        }

        // he: chỉ số material theo hệ (0 nước xanh biển, 1 Mộc lục, 2 Hỏa đỏ cam); thiếu thì giữ material đang gắn
        public void Bat(int he = 0)
        {
            if (!San) return;
            if (matHe != null && he >= 0 && he < matHe.Length && matHe[he]) img.material = matHe[he];
            if (!rig)
            {
                rig = Instantiate(rigPrefab, GocXa, Quaternion.identity);
                rig.name = rigPrefab.name;
            }
            rig.Bat();
            img.enabled = true;
            img.color = new Color(1, 1, 1, 0);
        }

        // pos, co: toạ độ / cạnh vuông theo đơn vị UI của lớp hạt (StageView.P); a: độ hiện; dt: giây sân vừa qua (đẩy hệ hạt)
        public void Ve(Vector2 pos, float co, float a, float dt)
        {
            if (!rig || !img) return;
            var rt = img.rectTransform; // neo góc trên trái lớp hạt như NuocFx: anchoredPosition = toạ độ StageView.P
            rt.anchoredPosition = pos;
            rt.sizeDelta = new Vector2(co, co);
            img.color = new Color(1, 1, 1, Mathf.Clamp01(a));
            rig.Buoc(dt);
        }

        public void Tat()
        {
            if (rig) rig.Tat();
            if (img) img.enabled = false;
        }

        void OnDisable() => Tat();

        void OnDestroy()
        {
            if (rig) Destroy(rig.gameObject);
        }
    }
}
