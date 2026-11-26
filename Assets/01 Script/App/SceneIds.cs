// Tên các scene chức năng (trùng tên file .unity trong Assets/00 Scenes, và thứ tự trong Build Settings sau Boot).
namespace PokiClash
{
    public static class SceneIds
    {
        public const string Boot = "Boot";
        public const string Hub = "Hub";
        public const string Zone = "Zone";
        public const string Battle = "Battle";
        public const string Machine = "Machine";
        public const string Heroes = "Heroes";
        public const string Cards = "Cards";
        public const string Notebook = "Notebook";
        public const string Badges = "Badges";
        public const string Cave = "Cave";
        public const string Farm = "Farm";
        public const string Home = "Home"; // Nhà (2026-11-18), thay Trang trại trên sảnh
        public const string Casino = "Casino"; // đảo Casino "Bến Lữ Khách" (2026-11-25, GD_Claude/29_DaoCasino.md)
        public const string CasinoFishing = "CasinoFishing"; // Bến câu của đảo Casino (mỗi trò tương tác một scene riêng)
        public const string CasinoRace = "CasinoRace"; // Trường đua của đảo Casino
        public const string CasinoMarket = "CasinoMarket"; // Chợ đen của đảo Casino
        public const string CasinoUnderground = "CasinoUnderground"; // Hầm đấu (Đấu trường ngầm) của đảo Casino
        public const string CasinoBlackjack = "CasinoBlackjack"; // lều Đêm Bài (Blackjack), chỉ mở theo lịch sự kiện
        public const string CasinoRoulette = "CasinoRoulette"; // lều Vòng Xoay Ngũ Hành (Roulette)
        public const string CasinoSlot = "CasinoSlot"; // lều Hội Máy Quả (máy quả 3×3)

        public static readonly string[] Features =
        {
            Hub, Zone, Battle, Machine, Heroes, Cards, Notebook, Badges, Cave, Farm, Home, Casino, CasinoFishing, CasinoRace, CasinoMarket,
            CasinoUnderground, CasinoBlackjack, CasinoRoulette, CasinoSlot,
        };
    }
}
