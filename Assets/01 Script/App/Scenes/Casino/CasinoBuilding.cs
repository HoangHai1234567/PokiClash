// Một công trình rời trên đảo Casino (GD_Claude/29_DaoCasino.md, C8; người dùng dặn 2026-11-25 "tách từng building ra để sau này có thể
// thay đổi hoặc bảo trì, đổi hình ảnh"). Mỗi công trình là một GameObject "ct_<mã>" riêng trong lớp cong_trinh của Screens/Casino, ảnh
// riêng Assets/03 Art/Casino/casino_ct_<mã>.png, khung riêng trong casino_art.json (px ảnh đảo trống 2048 x 1360, gốc trên trái).
// Đổi hình một công trình: thay file ảnh đó (giữ cỡ, hoặc sửa khung trong casino_art.json), chạy menu "PokiClash/Prefab/Đảo Casino/Đảo:
// dựng màn". Công trình khác không đụng tới. Mã: thap, hang, cho, dua, quan_tro, ben_cau, ben_tau, bai_tren/phai/trai (cọc bãi lều),
// leu_blackjack/roulette/slot (lều sự kiện).
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class CasinoBuilding : MonoBehaviour
    {
        [SerializeField] string id;
        [SerializeField] Image art;

        public string Id => id;
        public Image Art => art;

        // Dùng khi dựng prefab (Editor).
        public void Setup(string buildingId, Image image)
        {
            id = buildingId;
            art = image;
        }

        public void Show(bool on) => gameObject.SetActive(on);
    }
}
