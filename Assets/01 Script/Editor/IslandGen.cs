// Bộ sinh ải đảo 70 ải, chép buildIsland của Web/src/core/data/islands.ts sang Unity (2026-11-05, khi làm lại đảo Mộc theo 10 hình aola
// người dùng gửi). Mẫu ải xen giữa giữ % cường hóa đang dùng ở đảo Thủy trong stages.json (đã chỉnh bên Unity 2026-11-03/04, không phải
// số gốc của web). Kèm bộ ghi JSON thụt 1 khoảng như các file dữ liệu và bộ tính lại golden islands.json từ code.
// Không dùng UnityEditor: menu ở IslandGenMenu.cs; dự án console ngoài Unity cũng biên dịch được file này cùng Core.
// Thiết kế ải: GD_Claude/14_HeThongAi.md.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using PokiClash.Core;

namespace PokiClash.EditorTools
{
    public static class IslandGen
    {
        // ô trong mẫu ải: H tướng chặng này, P chặng trước, Q hai chặng trước, M và N hai loại lính, S tướng khởi đầu cùng hệ (Plan.starter)
        public enum Slot { H, P, Q, M, N, S }

        public sealed class Pattern
        {
            public StageTag tag;
            public (Slot slot, double buff)[] units;
            public Pattern(StageTag tag, params (Slot, double)[] units)
            {
                this.tag = tag;
                this.units = units;
            }
        }

        public sealed class Intro
        {
            public int at;
            public string hero, name;
            // mini boss, boss ở 5 mốc cuối (người dùng dặn 2026-11-05): trait là bị động boss (thẻ "traits" của cards.json), buff cộng
            // thêm vào cường hóa của ải tướng này (có bị động thì giảm chỉ số, không có thì tăng), dò bằng máy tự chơi
            public string trait;
            public double buff;
            public Intro(int at, string hero, string name, string trait = null, double buff = 0)
            {
                this.at = at;
                this.hero = hero;
                this.name = name;
                this.trait = trait;
                this.buff = buff;
            }
        }

        // tướng tặng ở ải at (lần đầu qua, đủ mảnh mở khóa); altFor: người chơi chọn tướng khởi đầu này thì tặng altHero thay
        public sealed class Gift
        {
            public int at;
            public string hero, altFor, altHero;
            public Gift(int at, string hero, string altFor = null, string altHero = null)
            {
                this.at = at;
                this.hero = hero;
                this.altFor = altFor;
                this.altHero = altHero;
            }
        }

        public sealed class Plan
        {
            public Elem zone;
            public int size = 70;
            public Intro[] intros; // theo thứ tự ải, intros[0].at = 1; ải 20 trở đi là mini boss, ải tướng cuối là boss tiến hóa
            // cấp ải 1 và ải cuối (boss cuối đảo), giữa thì min + (max − min)·((ải − 1)/(size − 1))^LevelPow làm tròn.
            // 5 đảo chơi song song (người dùng sửa 2026-11-05): đảo nào cũng từ cấp 1 lên gần cấp tối đa, chỉ lệch nhau vài cấp ở boss cuối
            public int levelMin = 1, levelMax;
            public string[][] minions; // [loại] = { bậc 1, bậc 2 }
            public int[] minionFrom; // chặng mở từng loại lính
            public int tier2From = 35; // từ ải này lính lên bậc 2
            public Pattern[] first; // các ải xen giữa của chặng 0
            public bool firstIsPlayer; // ải 1 là bóng tướng khởi đầu của người chơi: P, Q không lấy tướng chặng 0
            public string starter; // ô S: tướng khởi đầu cùng hệ, thu phục được (lần đầu chắc chắn rơi 2–4 mảnh)
            public Gift[] gifts = new Gift[0];
            // cường hóa cộng thêm theo số ô đội người chơi có ở cấp của ải: extra[số ô − 1][nhóm X…], mặc định SlotExtra
            public double[][] extra = SlotExtra;
        }

        // % cường hóa đảo Thủy hiện tại (stages.json, từ ải 4): ải tướng thường +15%, boss +15%, mini boss 0
        public const double IntroBuff = 0.15, MiniBuff = 0, BossBuff = 0.15;

        // độ cong của đường cấp trong đảo (< 1: lên nhanh ở đầu đảo, chậm dần về cuối)
        public const double LevelPow = 0.85;

        // Cộng thêm vào cường hóa của địch (trừ ải bóng) theo số ô đội người chơi có ở cấp của ải (Progress.SlotsAt) và nhóm ải:
        // ải tướng mới thường (trước ải 20), ải 1 địch (cường hóa), 2 địch, 3 địch, mini boss, boss. Mẫu ải đo với 1 tướng (đảo Thủy);
        // có 2, 3 ô đội thì người chơi đánh lần lượt nhiều tướng, nên địch phải mạnh hơn để giữ tỉ lệ thắng mục tiêu từng kiểu ải.
        // Hệ khắc làm số đo lệch nhiều giữa các đảo, nên mỗi đảo đo riêng với đội 2 tướng Khá khắc hệ, bằng cấp địch, sao và thẻ theo
        // cấp (Plan.extra). Mục tiêu (như đảo Thủy 1 ô): cường hóa 92%, ải 2 địch trung bình 76% (tướng và lính 78, cửa ải 62, hai
        // tướng 69, lính tinh nhuệ 78, bầy lính 91), ải 3 địch 84%, mini boss 72%, boss 61%. Dò bằng máy tự chơi 150 trận mỗi ải (dự án
        // console, lệnh tune; 2026-11-05). Bảng mặc định là của đảo Mộc (đội Kim: cường hóa 92%, 2 địch 74%, 3 địch 84%, mini boss 73%,
        // boss 59–63%); đảo mới phải dò lại. Hàng 3 ô chỉ dùng cho ải cấp 200, tạm lấy như 2 ô.
        public const int XIntro = 0, XOne = 1, XTwo = 2, XThree = 3, XMini = 4, XBoss = 5;
        public static readonly double[][] SlotExtra =
        {
            new[] { 0.0, 0, 0, 0, 0, 0 },
            new[] { 0.2, 1.05, 0.65, 0.45, 1.0, 0.95 },
            new[] { 0.2, 1.05, 0.65, 0.45, 1.0, 0.95 },
        };

        public static double Extra(Plan p, int level, int kind) => p.extra[Math.Min(p.extra.Length, Progress.SlotsAt(level)) - 1][kind];

        public static readonly Pattern[] Short =
        {
            new Pattern(StageTag.Minion, (Slot.M, 0.1), (Slot.N, 0.1)),
            new Pattern(StageTag.Buff, (Slot.H, 0.12)),
            new Pattern(StageTag.Group, (Slot.P, 0.15), (Slot.M, 0.15)),
            new Pattern(StageTag.Gate, (Slot.H, 0.35), (Slot.M, 0.2)),
        };

        public static readonly Pattern[] Long =
        {
            new Pattern(StageTag.Minion, (Slot.M, 0.1), (Slot.N, 0.1)),
            new Pattern(StageTag.Buff, (Slot.H, 0.12)),
            new Pattern(StageTag.Group, (Slot.P, 0.15), (Slot.M, 0.15)),
            new Pattern(StageTag.Minion, (Slot.M, -0.1), (Slot.N, -0.1), (Slot.M, -0.1)),
            new Pattern(StageTag.Pair, (Slot.H, 0.1), (Slot.Q, 0.1)),
            new Pattern(StageTag.Buff, (Slot.H, 0.25)),
            new Pattern(StageTag.Elite, (Slot.N, 0.5), (Slot.M, 0.1)),
            new Pattern(StageTag.Group, (Slot.H, -0.05), (Slot.M, -0.05), (Slot.N, -0.05)),
            new Pattern(StageTag.Gate, (Slot.H, 0.3), (Slot.P, 0.3)),
        };

        // mảnh rơi ở ải xen giữa theo độ hiếm (cửa ải ×1,5)
        static readonly double[] ShardChance = { 0.3, 0.25, 0.2, 0.15, 0.1 };

        // Đảo Thủy (đảo 70 ải đầu tiên, 2026-11-02/03; tướng các mốc ở GD_Claude/14). Ải 1 là bóng tướng khởi đầu của người chơi (Giọt
        // Sương, thu phục được); ải 3 tặng Võ Sư (chọn Thạch Nhân làm tướng khởi đầu thì tặng Mèo Quyền Sắt), ải 25 tặng Mầm Gỗ.
        public static Plan Thuy => new Plan
        {
            zone = Elem.Thuy,
            intros = new[]
            {
                // 5 mốc cuối (2026-11-05): con có bị động boss giữ hoặc giảm chỉ số, con không có +10%; đội Thổ Khá khắc hệ, bằng cấp,
                // 300 trận: Vây Lam 52%, Kuba 57%, Thương Lam 63%, Huyền Vũ 62%, Lam Quân 61%
                new Intro(1, "giot_suong", "Bãi Vỏ Sò"),
                new Intro(5, "tieu_y", "Vũng San Hô"),
                new Intro(10, "canh_cut", "Cầu Gỗ Rêu"),
                new Intro(15, "mi_nhi", "Làng Vỏ Ốc"),
                new Intro(20, "ma_ket", "Ngọn Hải Đăng"),
                new Intro(30, "vay_lam", "Thác Bạc", null, 0.1),
                new Intro(40, "kuba", "Rạn Ngọc Trai", "kuba_boss", -0.05),
                new Intro(50, "thuong_lam", "Hồ Gương", null, 0.1),
                new Intro(60, "huyen_vu", "Đền Rùa Cổ", "huyen_vu_boss", 0),
                new Intro(70, "lam_quan", "Xoáy Nước Đinh Ba", "lam_quan_boss", -0.15),
            },
            levelMax = 195,
            minions = new[] { new[] { "linh_cua", "linh_cua2" }, new[] { "linh_noc", "linh_noc2" }, new[] { "linh_ngu", "linh_ngu2" } },
            minionFrom = new[] { 0, 2, 4 },
            firstIsPlayer = true,
            gifts = new[] { new Gift(3, "vo_su", "thach_nhan", "meo_quyen"), new Gift(25, "mam_go") },
            // đội Thổ khắc Thủy (Võ Sư, Sóc Đá): cường hóa 93%, 2 địch 76%, 3 địch 86%, mini boss 72%, boss 59–68%
            extra = new[]
            {
                new[] { 0.0, 0, 0, 0, 0, 0 },
                new[] { 0.2, 0.6, 0.45, 0.3, 0.4, 0.85 },
                new[] { 0.2, 0.6, 0.45, 0.3, 0.4, 0.85 },
            },
            first = new[]
            {
                new Pattern(StageTag.Minion, (Slot.M, 0)),
                new Pattern(StageTag.Minion, (Slot.M, -0.25), (Slot.M, -0.25)),
                new Pattern(StageTag.Elite, (Slot.M, 0.35)),
            },
        };

        // Đảo Mộc (người dùng gửi 10 hình aola 2026-11-05, thứ tự trái sang phải là thứ tự ải tướng). Nụ Hoa (tướng khởi đầu hệ Mộc)
        // mất ải 1 nên đứng ở ải 2 cùng một lính, vẫn thu phục được như cũ.
        public static Plan Moc => new Plan
        {
            zone = Elem.Moc,
            intros = new[]
            {
                // 5 mốc cuối (2026-11-05): đội Kim Khá khắc hệ, bằng cấp, 300 trận: Gió Lốc 58%, Long Vuốt 65%, Thỏ Hoàng 60%,
                // Mộc Tinh 56%, Thanh Long 56%
                new Intro(1, "tien_la", "Bờ Rêu"),
                new Intro(5, "hoa_nhuy", "Đồng Hoa Sáng"),
                new Intro(10, "de_hoa", "Đồi Nấm"),
                new Intro(15, "bom_la", "Rừng Dây Leo"),
                new Intro(20, "phong_linh", "Hang Nanh Gió"),
                new Intro(30, "gio_loc", "Thung Lũng Lá", "gio_loc_boss", -0.15),
                new Intro(40, "long_vuot", "Vách Vuốt Rồng", null, 0.1),
                new Intro(50, "tho_hoang", "Rừng Trúc Ngọc", "tho_hoang_boss", 0),
                new Intro(60, "moc_tinh", "Hang Pha Lê Lục", null, 0.1),
                new Intro(70, "thanh_long", "Cây Thần Ngàn Năm", "thanh_long_boss", -0.15),
            },
            levelMax = 190,
            minions = new[] { new[] { "linh_bo", "linh_bo2" }, new[] { "linh_ran", "linh_ran2" }, new[] { "linh_chim", "linh_chim2" } },
            minionFrom = new[] { 0, 1, 2 },
            starter = "nu_hoa",
            first = new[]
            {
                new Pattern(StageTag.Group, (Slot.S, 0.15), (Slot.M, 0.15)),
                new Pattern(StageTag.Minion, (Slot.M, 0.1), (Slot.N, 0.1)),
                new Pattern(StageTag.Gate, (Slot.H, 0.35), (Slot.M, 0.2)),
            },
        };

        // Đảo Hỏa (người dùng gửi 10 hình aola 2026-11-05, thứ tự trái sang phải là thứ tự ải tướng). Hình ải 1 là dạng 3 của Sư Tử Lửa
        // (tướng khởi đầu hệ Hỏa) nên Sư Tử Lửa giữ ải 1. Ải 20 là 魔焰吉拉, siêu tiến hóa của chính dòng Sư Tử Lửa: người dùng để trống
        // để tìm tướng khác, Hồ Lửa đứng tạm (2026-11-05).
        public static Plan Hoa => new Plan
        {
            zone = Elem.Hoa,
            intros = new[]
            {
                // 5 mốc cuối (2026-11-05): đội Thủy Khá khắc hệ, bằng cấp, 300 trận: Hồng Liên 70%, Giáp Long 71%, Huyễn Viêm 69%,
                // Hỏa Tinh 55%, Lân Hỏa 57%. Hồng Liên, Huyễn Viêm tự thân yếu nên dù có bị động vẫn giữ cường hóa 0
                new Intro(1, "su_tu_lua", "Bến Đá Đen"),
                new Intro(5, "khong_lo", "Suối Dung Nham"),
                new Intro(10, "kim_su", "Rừng Than Hồng"),
                new Intro(15, "nham_than", "Sườn Núi Khói"),
                new Intro(20, "ho_lua", "Lò Lửa Thiền"), // tạm, chờ người dùng chọn tướng
                new Intro(30, "hong_lien", "Chùa Liên Hoa", "hong_lien_boss", 0),
                new Intro(40, "giap_long", "Lò Rèn Gai Thép", null, 0.1),
                new Intro(50, "huyen_viem", "Rừng Lửa Ảo", "huyen_viem_boss", 0),
                new Intro(60, "hoa_tinh", "Hang Hồng Ngọc", null, 0.1),
                new Intro(70, "lan_hoa", "Miệng Núi Lửa", "lan_hoa_boss", -0.15),
            },
            levelMax = 198,
            minions = new[] { new[] { "linh_lo", "linh_lo2" }, new[] { "linh_nam", "linh_nam2" }, new[] { "linh_khi", "linh_khi2" } },
            minionFrom = new[] { 0, 1, 2 },
            // đội Thủy khắc Hỏa (Giọt Sương, Mi Nhi), 150 trận mỗi ải: cường hóa 93%, 2 địch 75%, 3 địch 85%, mini boss 74%, boss 56%
            extra = new[]
            {
                new[] { 0.0, 0, 0, 0, 0, 0 },
                new[] { 0.2, 0.7, 0.5, 0.35, 0.65, 0.95 },
                new[] { 0.2, 0.7, 0.5, 0.35, 0.65, 0.95 },
            },
            first = new[]
            {
                new Pattern(StageTag.Group, (Slot.H, 0.15), (Slot.M, 0.15)),
                new Pattern(StageTag.Minion, (Slot.M, 0.1), (Slot.N, 0.1)),
                new Pattern(StageTag.Gate, (Slot.H, 0.35), (Slot.M, 0.2)),
            },
        };

        // Đảo Kim (người dùng gửi 10 hình aola 2026-11-05, thứ tự trái sang phải là thứ tự ải tướng). Bu Lông (tướng khởi đầu hệ Kim)
        // nhường ải 1 cho Bọ Cạp Đồng, đứng ở ải 2 cùng một lính như Nụ Hoa ở đảo Mộc. Tên, thẻ của 8 tướng mới là tạm.
        public static Plan Kim => new Plan
        {
            zone = Elem.Kim,
            intros = new[]
            {
                // 5 mốc cuối (2026-11-05): đội Hỏa Khá khắc hệ (Sư Tử Lửa, Kim Sư), bằng cấp, 300 trận: Chiến Thần 73%, Thiết Phủ 69%,
                // Tam Kiếm 69%, Ưng Thép 67%, Kim Nghê 63%. Thiết Phủ, Ưng Thép không có bị động boss nhưng tự thân yếu nên +20%, +30%
                new Intro(1, "bo_cap", "Cảng Sắt"),
                new Intro(5, "doc_giac", "Cầu Bánh Răng"),
                new Intro(10, "bo_ngua", "Rừng Lưỡi Liềm"),
                new Intro(15, "phi_thuong", "Tháp Canh Thép"),
                new Intro(20, "khien_bac", "Gác Chuông Đồng"),
                new Intro(30, "chien_than", "Xưởng Đúc Chuông", "chien_than_boss", 0),
                new Intro(40, "thiet_phu", "Mỏ Sắt Ngân", null, 0.2),
                new Intro(50, "tam_kiem", "Thành Ba Kiếm", "tam_kiem_boss", 0),
                new Intro(60, "ung_thep", "Tổ Cánh Pha Lê", null, 0.3),
                new Intro(70, "kim_nghe", "Tháp Thiên Chung", "kim_nghe_boss", -0.15),
            },
            levelMax = 193,
            minions = new[] { new[] { "linh_giap", "linh_giap2" }, new[] { "linh_khien", "linh_khien2" }, new[] { "linh_may", "linh_may2" } },
            minionFrom = new[] { 0, 1, 2 },
            starter = "bu_long",
            // đội Hỏa khắc Kim (Sư Tử Lửa, Kim Sư), 150 trận mỗi ải: cường hóa 93%, 2 địch 76%, 3 địch 84%, mini boss 68%, boss 63%
            extra = new[]
            {
                new[] { 0.0, 0, 0, 0, 0, 0 },
                new[] { 0.2, 0.88, 0.47, 0.34, 0.67, 0.8 },
                new[] { 0.2, 0.88, 0.47, 0.34, 0.67, 0.8 },
            },
            first = new[]
            {
                new Pattern(StageTag.Group, (Slot.S, 0.15), (Slot.M, 0.15)),
                new Pattern(StageTag.Minion, (Slot.M, 0.1), (Slot.N, 0.1)),
                new Pattern(StageTag.Gate, (Slot.H, 0.35), (Slot.M, 0.2)),
            },
        };

        // các đảo đã có kế hoạch 70 ải (menu "sinh lại ải" ghi lại tất cả)
        public static Plan[] All => new[] { Thuy, Hoa, Kim, Moc };

        public static int Level(Plan p, int at) =>
            p.levelMin + (int)Math.Floor((p.levelMax - p.levelMin) * Math.Pow((at - 1) / (double)(p.size - 1), LevelPow) + 0.5);

        // các ải của đảo (chưa có id), dạng cây JSON như stages.json
        public static List<Dictionary<string, object>> Build(Plan p, GameData d)
        {
            var o = new List<Dictionary<string, object>>();
            var gift = p.gifts.ToDictionary(g => g.at);
            string zone = Keys.Of(p.zone);
            for (int ch = 0; ch < p.intros.Length; ch++)
            {
                var it = p.intros[ch];
                int end = ch + 1 < p.intros.Length ? p.intros[ch + 1].at : p.size + 1;
                var kinds = p.minions.Where((_, i) => ch >= p.minionFrom[i]).ToArray();
                for (int at = it.at; at < end; at++)
                {
                    int lv = Level(p, at), k = at - it.at;
                    bool tier2 = at >= p.tier2From;
                    var enemies = new List<Dictionary<string, object>>();
                    var drops = new List<Dictionary<string, object>>();
                    StageTag tag;
                    string kind = "normal";
                    if (gift.TryGetValue(at, out var g))
                    {
                        var gd = Drop(g.hero, 1, d.Hero(g.hero).shards, d.Hero(g.hero).shards, true);
                        if (g.altFor != null)
                        {
                            gd["altFor"] = g.altFor;
                            gd["altHero"] = g.altHero;
                        }
                        drops.Add(gd);
                    }
                    if (k == 0)
                    {
                        tag = StageTag.Hero;
                        bool last = ch == p.intros.Length - 1, mini = !last && it.at >= 20;
                        kind = last ? "boss" : mini ? "mini" : "normal";
                        var h = d.Hero(it.hero);
                        bool mirror = ch == 0 && p.firstIsPlayer;
                        var e = Enemy(it.hero, lv, last || mini, !mirror && h.forms.Length > 1,
                            mirror ? -0.2 : Round2(it.buff + (last ? BossBuff + Extra(p, lv, XBoss) : mini ? MiniBuff + Extra(p, lv, XMini) : IntroBuff + Extra(p, lv, XIntro))));
                        if (mini) e["buff"] = Round2(it.buff + MiniBuff + Extra(p, lv, XMini)); // như đảo Thủy: mini boss ghi cả buff 0
                        if (it.trait != null) e["trait"] = it.trait;
                        enemies.Add(e);
                        // bóng tướng khởi đầu cũng rơi mảnh chắc chắn (GameData.StarterStage)
                        drops.Add(Drop(it.hero, 1, last ? 4 : mini ? 3 : 2, last ? 6 : mini ? 5 : 4));
                    }
                    else
                    {
                        var pats = ch == 0 ? p.first : end - it.at <= 5 ? Short : Long;
                        var pat = pats[(k - 1) % pats.Length];
                        tag = pat.tag;
                        // lính xoay vòng theo số ải để hai ải liền nhau không cùng một cặp
                        var kM = kinds[at % kinds.Length];
                        var kN = kinds[(at + 1) % kinds.Length];
                        string Pick(Slot s)
                        {
                            switch (s)
                            {
                                case Slot.M: return kM[tier2 ? 1 : 0];
                                case Slot.N: return kN[tier2 ? 1 : 0];
                                case Slot.S: return p.starter;
                            }
                            int back = s == Slot.H ? 0 : s == Slot.P ? 1 : 2, lo = p.firstIsPlayer ? 1 : 0;
                            return p.intros[ch - back >= lo ? ch - back : ch].hero;
                        }
                        var seen = new HashSet<string>();
                        foreach (var (slot, b) in pat.units)
                        {
                            var hid = Pick(slot);
                            enemies.Add(Enemy(hid, lv, false, false, Round2(b + Extra(p, lv, Math.Min(XThree, pat.units.Length)))));
                            var h = d.Hero(hid);
                            if (h.minion || !seen.Add(hid)) continue;
                            if (slot == Slot.S) drops.Add(Drop(hid, 1, 2, 4));
                            else drops.Add(Drop(hid, ShardChance[(int)h.rarity] * (tag == StageTag.Gate ? 1.5 : 1), 1, 2));
                        }
                    }
                    o.Add(new Dictionary<string, object>
                    {
                        ["zone"] = zone, ["idx"] = (double)at, ["name"] = k == 0 ? it.name : $"{it.name} {k + 1}", ["kind"] = kind,
                        ["enemies"] = enemies.Cast<object>().ToList(), ["drops"] = drops.Cast<object>().ToList(), ["tag"] = Keys.Of(tag),
                        ["chapter"] = (double)ch,
                    });
                }
            }
            return o;
        }

        static double Round2(double x) => Math.Round(x * 100) / 100;

        static Dictionary<string, object> Enemy(string hero, int lv, bool boss, bool evo, double buff)
        {
            var e = new Dictionary<string, object> { ["hero"] = hero, ["level"] = (double)lv };
            if (boss) e["boss"] = true;
            if (evo) e["evo"] = true;
            if (buff != 0) e["buff"] = buff;
            return e;
        }

        static Dictionary<string, object> Drop(string hero, double chance, int min, int max, bool gift = false)
        {
            var o = new Dictionary<string, object> { ["hero"] = hero, ["chance"] = chance, ["min"] = (double)min, ["max"] = (double)max };
            if (gift) o["gift"] = true;
            return o;
        }

        // thay các ải của đảo p.zone trong stages.json bằng bản sinh mới (đúng chỗ theo thứ tự đảo), đánh lại id toàn cục 1..N
        public static string ApplyToStages(string stagesJson, Plan p, GameData d)
        {
            var root = J.Obj(MiniJson.Parse(stagesJson));
            var list = J.Arr(root, "stages");
            string zone = Keys.Of(p.zone);
            int order = d.Zone(p.zone).order;
            int at = list.FindIndex(x => J.Str(J.Obj(x), "zone") == zone);
            if (at < 0) at = list.FindIndex(x => d.Zone(Keys.ToElem(J.Str(J.Obj(x), "zone"))).order > order);
            if (at < 0) at = list.Count;
            list.RemoveAll(x => J.Str(J.Obj(x), "zone") == zone);
            list.InsertRange(Math.Min(at, list.Count), Build(p, d));
            for (int i = 0; i < list.Count; i++)
            {
                var o = J.Obj(list[i]);
                var copy = new Dictionary<string, object> { ["id"] = (double)(i + 1) };
                foreach (var kv in o)
                    if (kv.Key != "id") copy[kv.Key] = kv.Value;
                list[i] = copy;
            }
            return Write(root) + "\n";
        }

        // golden islands.json tính từ code hiện tại (như IslandTests so): cỡ đảo, mini boss đầu, rương, cấp; từng ải: kiểu, chặng, bi, đội địch
        public static string IslandsGolden(GameData d)
        {
            var zones = new List<object>();
            foreach (var z in d.Zones.OrderBy(z => z.order))
                zones.Add(new Dictionary<string, object>
                {
                    ["id"] = Keys.Of(z.id), ["size"] = (double)Islands.Size(z.id), ["miniAt"] = (double)Islands.MiniAt(z.id),
                    ["chests"] = Islands.Chests(z.id).Select(c => (object)(double)c).ToList(),
                    ["level"] = new List<object> { (double)z.levelMin, (double)z.levelMax },
                });
            var stages = new List<object>();
            foreach (var st in d.Stages)
            {
                var members = new List<object>();
                foreach (var m in Teams.Enemy(st, d).members)
                    members.Add(new Dictionary<string, object>
                    {
                        ["hero"] = m.heroId, ["level"] = (double)m.level, ["star"] = (double)m.star,
                        ["cards"] = new List<object> { (double)m.cardSkill, (double)m.cardUlt, (double)m.cardPassive },
                        ["boss"] = m.boss, ["evo"] = m.evo, ["trait"] = m.trait,
                        ["mods"] = m.mods == null ? null : new Dictionary<string, object>
                        {
                            ["hpPct"] = m.mods.hpPct, ["atkPct"] = m.mods.atkPct, ["defPct"] = m.mods.defPct, ["spd"] = m.mods.spd,
                        },
                    });
                stages.Add(new Dictionary<string, object>
                {
                    ["id"] = (double)st.id, ["tag"] = st.tag == StageTag.None ? null : Keys.Of(st.tag),
                    ["chapter"] = st.tag == StageTag.None ? null : (object)(double)st.chapter,
                    ["balls"] = new List<object> { (double)Progress.StageBalls(d, st, true), (double)Progress.StageBalls(d, st, false) },
                    ["members"] = members,
                });
            }
            return Write(new Dictionary<string, object> { ["zones"] = zones, ["stages"] = stages }) + "\n";
        }

        // golden zones.json: chạy lại các bước của golden cũ (thắng ải theo id, mở rương mốc theo đảo; Rng 9, bản lưu mới) như
        // ZoneTests.ThuongAi_VaRuongMoc_KhopBanWeb và ghi lại kết quả (bi, mảnh, thẻ rương) cùng trạng thái cuối
        public static string ZonesGolden(GameData d, string oldJson)
        {
            string[] slotKey = { "skill", "ult", "passive" };
            var root = J.Obj(MiniJson.Parse(oldJson));
            var s = SaveData.New(d, 0);
            var r = new Rng(9);
            foreach (var x in J.Arr(root, "steps"))
            {
                var o = J.Obj(x);
                if (J.Str(o, "t") == "win")
                {
                    var rw = Progress.WinStage(s, d, J.Int(o, "id"), r);
                    o["balls"] = (double)rw.balls;
                    o["first"] = rw.first;
                    o["shards"] = rw.shards.Select(sh => (object)new List<object> { sh.hero, (double)sh.n, sh.unlocked, (double)sh.converted }).ToList();
                }
                else
                {
                    Keys.TryElem(J.Str(o, "z"), out var z);
                    var c = Progress.ClaimZoneChest(s, d, z, r);
                    o["r"] = c == null ? null : new Dictionary<string, object>
                    {
                        ["balls"] = (double)c.balls, ["big"] = c.big,
                        ["cards"] = c.cards.Select(cd => (object)new List<object> { cd.hero, slotKey[(int)cd.slot], cd.card, Keys.Of(cd.rarity) }).ToList(),
                    };
                }
            }
            var end = J.Obj(root, "end");
            end["zones"] = d.Zones.ToDictionary(z => Keys.Of(z.id), z => (object)(double)s.zones[(int)z.id]);
            end["zoneChests"] = d.Zones.ToDictionary(z => Keys.Of(z.id), z => (object)(double)s.zoneChests[(int)z.id]);
            end["clears"] = s.clears.OrderBy(kv => kv.Key).ToDictionary(kv => kv.Key.ToString(CultureInfo.InvariantCulture), kv => (object)(double)kv.Value);
            end["balls"] = (double)s.balls;
            end["owned"] = d.Heroes.Where(h => s.Hero(h.id).owned).Select(h => (object)h.id).ToList();
            return Write(root) + "\n";
        }

        // golden roster.json: "forms" (dạng theo sao của mọi tướng, như RosterTests.DangTheoSao) và "leads" (tướng, sao đứng trên nút
        // ải, như RosterTests.TuongTrenNutAi) tính lại từ code; "migrate" (bản lưu cũ) giữ nguyên
        public static string RosterGolden(GameData d, string oldJson)
        {
            var root = J.Obj(MiniJson.Parse(oldJson));
            root["forms"] = d.Heroes.Select(h => (object)new Dictionary<string, object>
            {
                ["id"] = h.id, ["n"] = (double)h.forms.Length,
                ["idx"] = Enumerable.Range(1, 5).Select(star => (object)(double)h.FormIndex(d.Cfg.formStars, star)).ToList(),
            }).ToList();
            root["leads"] = d.Stages.Select(st =>
            {
                var en = Teams.StageLead(st, d);
                return (object)new Dictionary<string, object> { ["id"] = (double)st.id, ["hero"] = en.hero, ["star"] = (double)Teams.EnemyFormStar(en) };
            }).ToList();
            return Write(root) + "\n";
        }

        // golden cardtext.json: chữ thẻ cấp 1, cấp 5 và giá của mọi thẻ (thẻ chung, thẻ riêng, thẻ lính, bị động boss), như CoreGoldenTests.CardText
        public static string CardTextGolden(GameData d)
        {
            var cards = d.Pool.Concat(d.Innate).Concat(d.MinionCards).Concat(d.Traits).Select(c => (object)new Dictionary<string, object>
            {
                ["id"] = c.id, ["lv1"] = CardText.Text(c, 1, d.Cfg.cardLvStep), ["lv5"] = CardText.Text(c, 5, d.Cfg.cardLvStep),
                ["cost"] = CardText.CostText(c),
            }).ToList();
            return Write(new Dictionary<string, object> { ["cards"] = cards }) + "\n";
        }

        // JSON thụt 1 khoảng, mảng và đối tượng mỗi phần tử một dòng (như json.dumps(indent=1, ensure_ascii=False) và
        // JSON.stringify(x, null, 1) đã ghi các file dữ liệu), số theo cách viết của JS
        public static string Write(object v)
        {
            var sb = new StringBuilder();
            Value(sb, v, 0);
            return sb.ToString();
        }

        static void Value(StringBuilder sb, object v, int depth)
        {
            switch (v)
            {
                case null: sb.Append("null"); return;
                case string s: Str(sb, s); return;
                case bool b: sb.Append(b ? "true" : "false"); return;
                case double x: sb.Append(Js.Num(x)); return;
                case int n: sb.Append(n.ToString(CultureInfo.InvariantCulture)); return;
                case IDictionary<string, object> o:
                    if (o.Count == 0)
                    {
                        sb.Append("{}");
                        return;
                    }
                    sb.Append('{');
                    bool first = true;
                    foreach (var kv in o)
                    {
                        sb.Append(first ? "\n" : ",\n").Append(' ', depth + 1);
                        first = false;
                        Str(sb, kv.Key);
                        sb.Append(": ");
                        Value(sb, kv.Value, depth + 1);
                    }
                    sb.Append('\n').Append(' ', depth).Append('}');
                    return;
                case IEnumerable e:
                    var items = e.Cast<object>().ToList();
                    if (items.Count == 0)
                    {
                        sb.Append("[]");
                        return;
                    }
                    sb.Append('[');
                    for (int i = 0; i < items.Count; i++)
                    {
                        sb.Append(i == 0 ? "\n" : ",\n").Append(' ', depth + 1);
                        Value(sb, items[i], depth + 1);
                    }
                    sb.Append('\n').Append(' ', depth).Append(']');
                    return;
                default:
                    throw new ArgumentException($"IslandGen.Write không ghi được kiểu {v.GetType().Name}");
            }
        }

        static void Str(StringBuilder sb, string s)
        {
            sb.Append('"');
            foreach (char c in s)
                switch (c)
                {
                    case '"': sb.Append("\\\""); break;
                    case '\\': sb.Append("\\\\"); break;
                    case '\n': sb.Append("\\n"); break;
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append("\\t"); break;
                    default:
                        if (c < 0x20) sb.Append("\\u").Append(((int)c).ToString("x4"));
                        else sb.Append(c);
                        break;
                }
            sb.Append('"');
        }
    }
}
