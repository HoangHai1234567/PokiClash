// Bậc sao (người dùng dặn 2026-11-17, học Clash of Critters): mỗi bậc 5 sao; đủ 5 sao một bậc mới tiến hóa lên bậc sau.
// Lên sao trong bậc tốn mảnh tướng; tiến hóa (sang bậc sau) tốn đá tiến hóa và cần cấp người chơi. Chi tiết: GD_Claude/20_TangDayNoiDung.md.
//
// HeroProg.star (và Member.star) là sao TỔNG 1..MaxStar: thang chung sao 1–5 là Đồng 1–5, 6–10 Bạc, 11–15 Vàng, 16–20 Kim Cương
// (chỉ số, giá mảnh, đá, sao địch tính trên thang này). Đổi dạng của dòng tiến hóa theo BalanceConfig.formStars (6, 11).
// Người chơi thấy bậc THEO DẠNG của từng tướng (2026-11-19, phần cuối tệp): tướng có bao nhiêu hình thì bấy nhiêu bậc, mỗi bậc 5 sao.
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

        public static string Name(int tier) => Loc.T(Names[System.Math.Max(0, System.Math.Min(Count - 1, tier))]);

        // sao tổng của (bậc, sao trong bậc)
        public static int Star(int tier, int inTier) => tier * PerTier + inTier;

        // đang ở 5 sao của một bậc chưa phải bậc cuối: bước kế là tiến hóa (tốn đá), không phải lên sao (tốn mảnh)
        public static bool AtEvolveGate(int star) => star < MaxStar && star % PerTier == 0;

        // "Bạc 3 sao" (chữ hiện trong game: phông Baloo2, Pangolin không có ký tự ★)
        public static string Label(int star) => Loc.F("{0} {1} sao", Name(Tier(star)), InTier(star));

        // sao cũ 1..5 (trước 2026-11-17) đổi sang sao tổng khi đọc bản lưu v11 (SaveCodec, bước v11 -> v12): giữ dạng đang có
        // (dạng 2 ở sao cũ 3 = Bạc 1★, dạng 3 ở sao cũ 5 = Vàng 1★)
        public static readonly int[] FromOld = { 1, 1, 3, 6, 8, 11 }; // chỉ số là sao cũ (0 coi như 1)

        public static int Migrate(int oldStar) => FromOld[System.Math.Max(0, System.Math.Min(FromOld.Length - 1, oldStar))];

        // sao quy về thang cũ 1..5 cho chỗ còn tính theo sao cũ (trang trại): sao tổng 1, 6, 11 là sao cũ 1, 3, 5; mỗi sao tổng 0,4 sao
        // cũ, Kim Cương 5★ là 8,6
        public static double Legacy(int star) => 1 + 0.4 * (System.Math.Max(1, star) - 1);

        // ---------- bậc theo dạng (người dùng dặn 2026-11-19) ----------
        // Số bậc của tướng = số hình trong dòng tiến hóa (1..3): tướng 2 dạng chỉ có Đồng, Bạc; mỗi lần tiến hóa là một lần đổi hình.
        // Dạng trùng hình dạng trước (chờ vẽ dạng mới, chỉ to hơn: Thiết Cưa, Sơn Viên, dạng 3 Quỷ Lava) không thành bậc riêng.
        // Bên trong vẫn là sao tổng 1..MaxStar nên chỉ số, tổng giá, sao địch, bản lưu không đổi: bậc k ≥ 1 bắt đầu ở mốc đổi hình
        // (formStars, như HeroDef.FormIndex), bậc cuối kéo tới MaxStar. 5 sao hiện của một bậc là 5 điểm dừng trải đều trên đoạn sao
        // tổng của bậc (bậc dài 5 thì trùng sao tổng): tướng 2 dạng Đồng 1–5 = sao tổng 1–5, Bạc 1–5 = 6, 10, 13, 17, 20; tướng 1 dạng
        // Đồng 1–5 = 1, 6, 11, 15, 20; tướng 3 dạng Đồng, Bạc trùng sao tổng, Vàng 1–5 = 11, 13, 16, 18, 20.
        // Lên sao nhảy tới điểm dừng kế (Progress.StarUpCost gộp mảnh các sao tổng ở giữa, cần cấp của mốc bậc cũ nếu đi qua); tiến
        // hóa là bước từ sao cuối bậc sang bậc sau (đá, cấp, đổi hình).

        // chỉ số dạng mở đầu từng bậc: dạng 0 và mỗi dạng có hình khác dạng trước
        static int[] TierForms(HeroDef h)
        {
            if (h == null || h.forms.Length == 0) return new[] { 0 };
            var r = new System.Collections.Generic.List<int> { 0 };
            for (int i = 1; i < h.forms.Length && r.Count < Count; i++)
                if (h.forms[i].aola != h.forms[i - 1].aola) r.Add(i);
            return r.ToArray();
        }

        public static int Tiers(HeroDef h) => TierForms(h).Length;

        static int TierStart(int[] tierForms, int[] formStars, int k)
        {
            if (k <= 0) return 1;
            int f = tierForms[k] - 1;
            return f < formStars.Length ? formStars[f] : Star(k, 1);
        }

        static int TierEnd(int[] tierForms, int[] formStars, int k) =>
            k >= tierForms.Length - 1 ? MaxStar : TierStart(tierForms, formStars, k + 1) - 1;

        // sao tổng của các điểm dừng (Tiers × 5, tăng dần, đầu là 1, cuối là MaxStar)
        public static int[] Stops(BalanceConfig cfg, HeroDef h)
        {
            var tf = TierForms(h);
            var r = new int[tf.Length * PerTier];
            for (int k = 0; k < tf.Length; k++)
            {
                int a = TierStart(tf, cfg.formStars, k), b = System.Math.Max(a, TierEnd(tf, cfg.formStars, k));
                for (int i = 0; i < PerTier; i++) r[k * PerTier + i] = a + (int)System.Math.Floor(i * (b - a) / (double)(PerTier - 1) + 0.5);
            }
            return r;
        }

        // vị trí (0..) của điểm dừng lớn nhất ≤ star (sao của bản lưu cũ nằm giữa hai điểm dừng thì hiện theo điểm dưới)
        public static int StopIndex(BalanceConfig cfg, HeroDef h, int star)
        {
            var st = Stops(cfg, h);
            int i = 0;
            while (i + 1 < st.Length && st[i + 1] <= star) i++;
            return i;
        }

        // bậc của tướng (0..Tiers − 1) ở sao tổng này
        public static int TierOf(BalanceConfig cfg, HeroDef h, int star) => StopIndex(cfg, h, star) / PerTier;

        // sao trong bậc của tướng (1..5; 0 nếu star < 1)
        public static int InTierOf(BalanceConfig cfg, HeroDef h, int star) => star < 1 ? 0 : StopIndex(cfg, h, star) % PerTier + 1;

        // "Bạc 3 sao" theo bậc của tướng
        public static string Label(BalanceConfig cfg, HeroDef h, int star) => Loc.F("{0} {1} sao", Name(TierOf(cfg, h, star)), InTierOf(cfg, h, star));

        // sao tổng của điểm dừng kế (bước lên sao hoặc tiến hóa tới đây); MaxStar nếu đã tối đa
        public static int NextStop(BalanceConfig cfg, HeroDef h, int star)
        {
            foreach (int x in Stops(cfg, h))
                if (x > star) return x;
            return MaxStar;
        }

        // sao tổng đầu bậc k của tướng (sao 1 của bậc)
        public static int TierStartStar(BalanceConfig cfg, HeroDef h, int k) => Stops(cfg, h)[System.Math.Max(0, System.Math.Min(Tiers(h) - 1, k)) * PerTier];

        // đang ở sao cuối của một bậc chưa phải bậc cuối: bước kế là tiến hóa (đổi hình), không phải lên sao
        public static bool AtGate(BalanceConfig cfg, HeroDef h, int star)
        {
            var tf = TierForms(h);
            for (int k = 0; k < tf.Length - 1; k++)
                if (star == TierEnd(tf, cfg.formStars, k)) return true;
            return false;
        }
    }
}
