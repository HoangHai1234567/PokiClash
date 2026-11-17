// Bậc sao (người dùng dặn 2026-11-17, học Clash of Critters): mỗi bậc 5 sao; đủ 5 sao một bậc mới tiến hóa lên bậc sau.
// Lên sao trong bậc tốn mảnh tướng; tiến hóa (sang bậc sau) tốn đá tiến hóa và cần cấp người chơi. Chi tiết: GD_Claude/20_TangDayNoiDung.md.
//
// HeroProg.star (và Member.star) là sao TỔNG 1..MaxStar: sao 1–5 là Đồng 1–5, 6–10 Bạc, 11–15 Vàng, 16–20 Kim Cương.
// Đổi dạng của dòng tiến hóa theo BalanceConfig.formStars (6, 11: dạng 2 ở Bạc 1 sao, dạng 3 ở Vàng 1 sao).
namespace PokiClash.Core
{
    public static class StarTier
    {
        public const int PerTier = 5;
        public const int Count = 4;
        public const int MaxStar = PerTier * Count; // 20

        public static readonly string[] Names = { "Đồng", "Bạc", "Vàng", "Kim Cương" };

        // bậc 0..Count-1 của sao tổng
        public static int Tier(int star) => System.Math.Max(0, System.Math.Min(Count - 1, (star - 1) / PerTier));

        // sao trong bậc 1..PerTier
        public static int InTier(int star) => star < 1 ? 0 : (star - 1) % PerTier + 1;

        public static string Name(int tier) => Names[System.Math.Max(0, System.Math.Min(Count - 1, tier))];

        // sao tổng của (bậc, sao trong bậc)
        public static int Star(int tier, int inTier) => tier * PerTier + inTier;

        // đang ở 5 sao của một bậc chưa phải bậc cuối: bước kế là tiến hóa (tốn đá), không phải lên sao (tốn mảnh)
        public static bool AtEvolveGate(int star) => star < MaxStar && star % PerTier == 0;

        // "Bạc 3 sao" (chữ hiện trong game: phông Baloo2, Pangolin không có ký tự ★)
        public static string Label(int star) => $"{Name(Tier(star))} {InTier(star)} sao";

        // sao cũ 1..5 (trước 2026-11-17) đổi sang sao tổng khi đọc bản lưu v11 (SaveCodec, bước v11 -> v12): giữ dạng đang có
        // (dạng 2 ở sao cũ 3 = Bạc 1★, dạng 3 ở sao cũ 5 = Vàng 1★)
        public static readonly int[] FromOld = { 1, 1, 3, 6, 8, 11 }; // chỉ số là sao cũ (0 coi như 1)

        public static int Migrate(int oldStar) => FromOld[System.Math.Max(0, System.Math.Min(FromOld.Length - 1, oldStar))];

        // sao quy về thang cũ 1..5 cho chỗ còn tính theo sao cũ (trang trại): sao tổng 1, 6, 11 là sao cũ 1, 3, 5; mỗi sao tổng 0,4 sao
        // cũ, Kim Cương 5★ là 8,6
        public static double Legacy(int star) => 1 + 0.4 * (System.Math.Max(1, star) - 1);
    }
}
