// Túi bi (người dùng 2026-11-27: "cần phải giới hạn max số bóng 1 lúc người chơi có thể cầm ... Khi đang max bóng người chơi sẽ không thể nhận
// thêm từ cây từ home nữa nhưng nếu nhận từ các phần quà / mở rương hoặc iap thì vẫn nhận được"). Học Clash of Critters (trang cộng đồng,
// GD_Claude/26 mục 16): túi 420 bi, mốc trại "Kho Bi" +80 ba lần; cây 50 bi, đầy thì ngừng ra; dưới trần mới hái được cây; quà, sự kiện, thư,
// gói nạp cộng vượt trần.
// - Trần = (ballCap + ballCapPerTree × (số cây đã mở − 1)) × hệ số sức chứa cây (Thẻ Tuần, Thẻ Phiêu Lưu): 400 lúc mở Nhà, 800 khi đủ 5 cây.
// - Chỉ chặn nguồn tự sinh ở Nhà: cây bi (Trees.Harvest), công trình ra bi (Home.Collect), trang trại (Farm.Harvest). Hái tới đầy túi, phần
//   thừa nằm lại chỗ cũ (khác Critters: họ cho hái cả cây khi còn dưới trần, sinh mẹo xả về 419 rồi hái tràn).
// - Quà, rương, ải, sự kiện, quảng cáo, gói nạp không qua đây nên cộng vượt trần; đang vượt trần thì Room = 0.
using System;

namespace PokiClash.Core
{
    public static class BallBag
    {
        public static int Cap(SaveData s, BalanceConfig cfg, double now)
        {
            int trees = Math.Max(1, Trees.Open(s, cfg));
            double c = (cfg.trees.ballCap + cfg.trees.ballCapPerTree * (trees - 1)) * Trees.CapMult(s, cfg, now);
            return (int)Math.Round(c);
        }

        // còn chứa thêm được bao nhiêu bi từ nguồn tự sinh
        public static int Room(SaveData s, BalanceConfig cfg, double now) => Math.Max(0, Cap(s, cfg, now) - s.balls);

        public static bool Full(SaveData s, BalanceConfig cfg, double now) => Room(s, cfg, now) <= 0;
    }
}
