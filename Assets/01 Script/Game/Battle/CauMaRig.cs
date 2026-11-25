// RIG CHỤP HIỆU ỨNG PREFAB GỐC vào RenderTexture (2026-11-25; người dùng chọn "hướng A, dùng thẳng prefab của gói" cho cầu ma thủy Thôn Kình).
// Prefab Assets/04 Prefabs/Fx/CauMaRig (dựng bằng menu "PokiClash/Prefab/Trận/Cầu ma thủy: dựng rig + gắn vào sân", CauMaRigMenu.cs): camera
// phối cảnh nhìn chếch xuống 18° như camera demo của gói, xoá trong suốt, vẽ vào cau_ma_rt; hệ hạt FX_PF_MagicWater_OrbLoop (bỏ quầng tối
// Glow / Mask và sóng chấn khúc xạ). Rig đặt ở góc xa thế giới (CauMaHien sinh từ prefab), camera chỉ bật khi đang hiện. Hệ hạt KHÔNG tự chạy:
// HatLua đẩy theo đồng hồ sân (Buoc) nên khựng / tua / chạy chậm của sân áp đúng.
using UnityEngine;

namespace PokiClash
{
    public sealed class CauMaRig : MonoBehaviour
    {
        [SerializeField] Camera cam;
        [SerializeField] ParticleSystem ps;

        public void Setup(Camera c, ParticleSystem p)
        {
            cam = c;
            ps = p;
        }

        // bắt đầu lại từ khung 0 (Simulate dừng hệ hạt sau khi chạy, HatLua đẩy từng khung)
        public void Bat()
        {
            gameObject.SetActive(true);
            if (cam) cam.enabled = true;
            if (ps) ps.Simulate(0, true, true, false);
        }

        public void Buoc(float dt)
        {
            if (ps && dt > 0) ps.Simulate(dt, true, false, false);
        }

        public void Tat()
        {
            if (ps) ps.Clear(true);
            if (cam) cam.enabled = false;
            gameObject.SetActive(false);
        }
    }
}
