// Hướng dẫn người mới (FTUE, GD_Claude/25_FTUE.md): cờ từng bước trong bản lưu, kịch bản trận và máy bi lần đầu, hệ mình khắc,
// nút sảnh hiện dần, khoảnh khắc mở tính năng, trang "Cách chơi". Logic thuần; phần hiện (lớp phủ, khoanh, ghi chú) ở App/Guide.
// Cờ lưu ở SaveData.extra["ftue"] (chuỗi mã bước cách nhau dấu phẩy; "*" = bản lưu cũ, coi mọi bước đã xong), không đổi phiên bản
// bản lưu. Bản lưu chưa có cờ: đã qua ải hoặc đã đánh trận thì là bản cũ, chưa thì bắt đầu hướng dẫn.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    // kịch bản trận hướng dẫn: thẻ rút sẵn theo lần rút của phe người chơi (null = rút thường), máu phe người chơi không xuống dưới floor
    public sealed class BattleScript
    {
        public readonly List<string[]> offers = new List<string[]>();
        public double floor;
        int drawn;

        // lần rút kế của phe người chơi: thẻ có sẵn (bỏ thẻ không có trong dữ liệu) hoặc null
        public List<string> NextOffer(GameData d)
        {
            int i = drawn++;
            if (i >= offers.Count || offers[i] == null) return null;
            var o = offers[i].Where(id => d.Card(id) != null).ToList();
            return o.Count > 0 ? o : null;
        }
    }

    public static class Tutorial
    {
        const string Key = "ftue";
        public const string Legacy = "*";

        // công cụ thử trong Editor (tour chạy trên bản lưu thật) tắt hướng dẫn: mọi bước coi như xong, sảnh hiện đủ
        public static bool Off;

        // ---------- mã bước (GD_Claude/25_FTUE.md mục 4) ----------
        // A: mở game (a0: đoạn cốt truyện trước màn tải, mục 11)
        public const string Story = "a0", Intro = "a2", Home1 = "a6", Island = "a7", Fight = "a8", Go = "a9";
        // B: trận 1
        public const string PickCard = "b1", Queue = "b2", RunQueue = "b3", FoeTurn = "b4", Skill = "b5", PickMore = "b6", Balls = "b8";
        // C: vòng lõi đầu
        public const string Drop = "c1", Exp = "c2", Hold = "c3", Chest = "c5", Copies = "c6", NoBalls = "c7", Heroes = "c8",
            HeroTile = "c9", UpCard = "c10", Isles = "c11", CounterIsle = "c12", CounterGo = "c13", Counter = "c14", Ult = "c15",
            Shards = "c16", Free = "c17";
        // C sau trận 2 (người dùng 2026-11-24): ép chạm Sổ thẻ, gợi ý về sảnh; "Nhà đã mở", ép chạm tàu về Nhà; trong Nhà giới thiệu qua
        // Nhà chính, ruộng vườn, xưởng gỗ và kho, rồi đặt Cây bi (G3), gợi ý về sảnh; sảnh báo Cửa hàng mở, rồi lời chào cuối (C17)
        public const string CardsGo = "c18", CardsBack = "c19", HomeNews = "c20", HomeGo = "c21", HomeMain = "c22", HomeFarm = "c23",
            HomeWood = "c24", HomeBack = "c25", ShopNews = "c26";
        // khắc hệ là chìa khoá chiến thuật (người dùng 2026-11-27): C12a bài học vòng Tương khắc ở sảnh trước C12 (thuộc chuỗi bắt buộc);
        // D11 gợi ý nút vòng 5 chấm ở ô tướng (màn Tướng), D13 cùng nút ở hộp chọn đội; D12 lần đầu đem tướng bị địch khắc vào trận
        public const string CounterWheel = "c27", WheelTile = "d11", CounteredTeam = "d12", WheelPick = "d13";
        // D–F: theo lúc
        public const string MultiFoe = "d1", Stun = "d3", EvoFoe = "d4", EvoNow = "d5", Auto = "d6", RareCard = "d7", ZoneChest = "d8",
            CardsBook = "d9", Underlevel = "e1", FirstLoss = "e2", Tree = "e3", TreeSeed = "e0", AfkBtn = "f1", AfkStage = "f3",
            Legend = "f4", Rings = "f5", Bet = "f6", Swap = "f8", StarUp = "f10";
        // G: Nhà. Cây bi đến cùng Nhà, người chơi tự đặt (người dùng 2026-11-23): Xây → chọn Cây bi → kéo, Đặt (ba bước lặp tới khi đặt
        // xong, cờ TreePlaced), rồi chạm cây hái bi (TreeTap)
        public const string TreePlaced = "g3t", TreeBuild = "g3t1", TreeTray = "g3t2", TreeSpot = "g3t3", TreeTap = "g3h";
        // trạng thái: "d2_<id>" mỗi loại một lần (StatusTip)

        // ---------- cờ ----------

        static string Raw(SaveData s)
        {
            if (s?.extra == null) return Legacy;
            if (!s.extra.TryGetValue(Key, out var o) || !(o is string str))
            {
                str = Progress.TotalCleared(s) > 0 || s.stats.battles > 0 ? Legacy : "";
                s.extra[Key] = str;
            }
            return str;
        }

        public static bool IsLegacy(SaveData s) => Raw(s) == Legacy;

        public static bool Done(SaveData s, string id)
        {
            if (Off) return true;
            var r = Raw(s);
            return r == Legacy || ("," + r + ",").Contains("," + id + ",");
        }

        public static void Mark(SaveData s, string id)
        {
            if (Off || s?.extra == null || Done(s, id)) return;
            var r = Raw(s);
            s.extra[Key] = r.Length == 0 ? id : r + "," + id;
        }

        public static void MarkAll(SaveData s, params string[] ids)
        {
            foreach (var id in ids) Mark(s, id);
        }

        // bản lưu mới (SaveData.New của game) và nút "Chạy lại hướng dẫn" của bản dev
        public static void Begin(SaveData s)
        {
            if (s?.extra != null) s.extra[Key] = "";
        }

        public static void Skip(SaveData s)
        {
            if (s?.extra != null) s.extra[Key] = Legacy;
        }

        // chuỗi bắt buộc (chặng A–C) xong
        public static bool CoreDone(SaveData s) => Done(s, Free);

        // đoạn cốt truyện mở đầu: chỉ bản lưu mới chưa chọn tướng đồng hành, chưa xem lần nào (bản lưu cũ "*" coi như đã xem)
        public static bool StoryNeeded(SaveData s) => s != null && string.IsNullOrEmpty(s.starter) && !Done(s, Story);

        // bước thuộc chuỗi bắt buộc: không tắt bằng công tắc "Gợi ý" của Sổ tay. Đặt Cây bi đầu (G3) nằm trong chuỗi từ 2026-11-24
        public static bool IsCore(string id) => id.Length > 0 && (id[0] == 'a' || id[0] == 'b' || id[0] == 'c' || id.StartsWith("g3"));

        // trận 2 (ải đầu của đảo mình khắc) đã thắng: mở Sổ thẻ, rồi Nhà, rồi Cửa hàng
        public static bool Battle2Won(SaveData s, GameData d) => s.zones[(int)CounterIsland(s, d)] > 0;

        // đã đi hết phần giới thiệu Nhà (công trình và hái Cây bi đầu)
        public static bool HomeToured(SaveData s) => Done(s, HomeWood) && Done(s, TreeTap);

        // ---------- tướng đồng hành, đảo ----------

        public static HeroDef Starter(SaveData s, GameData d) => string.IsNullOrEmpty(s?.starter) ? null : d.Hero(s.starter);

        // đảo của hệ mà tướng đồng hành khắc (trận 2: học khắc hệ)
        public static Elem CounterIsland(SaveData s, GameData d) => Elements.Beats(Starter(s, d)?.elem ?? Elem.Thuy);

        // 4 đảo còn lại tan mây sau trận thắng đầu và bước nâng Chiêu (C10), để mỗi lần vào sảnh chỉ một việc
        public static bool IslesOpen(SaveData s) => Done(s, UpCard);

        // bước nâng Chiêu (C8–C10) còn phải ép: chưa xong, Chiêu của tướng đồng hành còn cấp 1 và đủ bản sao. Chiêu đã lên cấp mà cờ
        // chưa có (lớp phủ lỡ cú chạm, lỗi 2026-11-23) thì coi như đã làm, sảnh đánh dấu rồi đi tiếp chứ không ép vào màn Tướng lại
        public static bool UpCardDue(SaveData s, GameData d)
        {
            if (Done(s, UpCard) || string.IsNullOrEmpty(s?.starter)) return false;
            return s.Hero(s.starter).Card(CardSlot.Skill).lv <= 1 && Progress.CanUpCard(s, d.Cfg, s.starter, CardSlot.Skill);
        }

        // vai một chữ của 5 tướng khởi đầu (hộp chọn bạn đồng hành)
        public static string Role(string starterId)
        {
            switch (starterId)
            {
                case "ti_tach": return Loc.T("Bền bỉ");
                case "su_tu_lua": return Loc.T("Thiêu đốt");
                case "bo_cap": return Loc.T("Phá giáp");
                case "tien_la": return Loc.T("Hồi phục");
                case "thach_nhan": return Loc.T("Phòng thủ");
                default: return "";
            }
        }

        // ---------- trận hướng dẫn ----------

        public const double LoseFloor = 0.2;

        // trận 1 (ải 1 đảo của tướng đồng hành, trận gương) và trận 2 (ải 1 đảo mình khắc): rút sẵn thẻ, khoá thua ngầm
        public static BattleScript BattleFor(SaveData s, GameData d, StageDef st)
        {
            var h = Starter(s, d);
            if (Off || h == null || st == null || st.idx != 1 || st.enemies.Count != 1) return null;
            if (!Done(s, Balls) && st.zone == h.elem)
            {
                var b = new BattleScript { floor = LoseFloor };
                b.offers.Add(new[] { "nem_da", "mai_vuot", "bang_gac" }); // đánh, tăng Công, hồi máu: ba kiểu dễ hiểu nhất
                return b;
            }
            if (!Done(s, Shards) && st.zone == CounterIsland(s, d))
            {
                var b = new BattleScript { floor = LoseFloor };
                // lượt 2 và 3 có Gầm Gừ (+15 nộ) để Tuyệt kỹ kịp đầy trong trận (5 lần rút mỗi lượt)
                for (int i = 0; i < 11; i++) b.offers.Add(null);
                b.offers[5] = new[] { "gam_gu", "nem_da", "hit_tho" };
                b.offers[10] = new[] { "gam_gu", "can_xe", "mai_vuot" };
                return b;
            }
            return null;
        }

        // ---------- máy bi lần đầu ----------

        // kết quả 6 bi đầu (ô đáy 0..4: Exp5, Exp10, ChestGold, Exp10, Exp5; 5 = cốc thẻ, rương bạc): 10+10+5+10+10 = 45 EXP lên cấp 2
        // ở bi thứ 5, rồi rương bạc
        public static readonly int[] MachineOutcomes = { 1, 3, 0, 1, 3, 5 };

        // rương đầu tiên: 2 bản sao thẻ Chiêu của tướng đồng hành (thẻ cấp 2 cần 2 bản sao), để nâng Chiêu ngay (C8–C10)
        public static List<Reward> FirstChest(SaveData s, GameData d)
        {
            var h = Starter(s, d);
            if (Done(s, Chest) || h == null || s.Hero(h.id)?.owned != true) return null;
            Mark(s, Chest);
            var card = d.Card(h.skill);
            var outL = new List<Reward>();
            for (int i = 0; i < 2; i++)
            {
                var drop = new Progress.CardDrop { hero = h.id, slot = CardSlot.Skill, card = h.skill, rarity = card.rarity };
                Progress.GiveCard(s, drop);
                outL.Add(new Reward { k = RewardKind.Card, drop = drop });
            }
            return outL;
        }

        // cây bi đầu tiên có sẵn 10 bi để lần hái đầu đã tay (câu 8 của 25_FTUE.md); gọi khi vào Nhà (cây mở cùng Nhà) và sau trận thắng
        public const int TreeSeedBalls = 10;

        public static void SeedTree(SaveData s, BalanceConfig cfg, double now)
        {
            if (Done(s, TreeSeed) || Trees.Open(s, cfg) <= 0) return;
            Trees.Tick(s, cfg, now);
            var t = Trees.Of(s, now);
            if (t.stock.Count > 0) t.stock[0] = Math.Max(t.stock[0], TreeSeedBalls);
            Mark(s, TreeSeed);
        }

        // ---------- sảnh hiện dần (mục 5) ----------

        // Next: nút Đánh tiếp cũ (bỏ khỏi sảnh 2026-11-23, giữ cho test); Shop: nút Cửa hàng ở hàng đáy
        public enum HubPart { Heroes, Cards, Machine, Next, Trees, Home, Temple, Cave, Afk, Shop, SoPhep }

        public static bool Shows(SaveData s, GameData d, HubPart part, double now)
        {
            if (Off || IsLegacy(s)) return true;
            bool core = CoreDone(s);
            switch (part)
            {
                case HubPart.Machine: return Done(s, Balls) || s.ballsSpent > 0;
                case HubPart.Heroes: return Done(s, NoBalls) || core;
                case HubPart.Next: return core;
                // sau trận 2: Sổ thẻ ngay, Nhà từ lúc báo "Nhà đã mở", Cửa hàng sau khi đi hết Nhà (2026-11-24)
                case HubPart.Shop: return core || HomeToured(s);
                case HubPart.Cards: return core || Battle2Won(s, d);
                case HubPart.Trees: return core && Trees.Open(s, d.Cfg) > 0;
                case HubPart.Home: return Home.Open(s, d.Cfg) && (core || Done(s, HomeNews));
                case HubPart.Temple: return core && (Progress.BadgesOpen(s) || s.zones.Max() >= 10);
                case HubPart.Cave: return core && (Progress.CaveOpen(s) || s.level >= 20);
                // Sổ Phép (2026-11-24): thẻ phác chì hiện từ 5 cấp trước khi mở
                case HubPart.SoPhep: return core && s.level >= d.Cfg.sophep.openLevel - 5;
                case HubPart.Afk:
                    if (Done(s, AfkBtn)) return true;
                    if (!core || Progress.TotalCleared(s) == 0) return false;
                    var ap = Afk.Pending(s, d.Cfg, now);
                    return ap.hours >= 1 || Afk.ReadyChests(s, d.Cfg, now) > 0;
            }
            return true;
        }

        // ---------- khoảnh khắc mở tính năng (chặng G, H) ----------

        public sealed class Unlock
        {
            public string id, title, text, icon;
        }

        // tính năng vừa mở chưa báo, theo thứ tự (mỗi lần vào sảnh báo một cái); null = không có
        public static Unlock NextUnlock(SaveData s, GameData d)
        {
            if (Off || !CoreDone(s) || IsLegacy(s)) return null;
            var cfg = d.Cfg;
            Unlock U(string id, string title, string text, string icon) => Done(s, id) ? null : new Unlock { id = id, title = title, text = text, icon = icon };
            Unlock u = null;
            if (Home.Open(s, cfg)) u = U("g1", Loc.T("Nhà đã mở!"), Loc.T("Tướng làm việc ra bi và gỗ cả khi bạn vắng. Cây bi cũng ở đó, chờ bạn đặt. Chạm nút Nhà ở hàng dưới để về Nhà."), "seed");
            if (u == null && SoPhep.Open(s, cfg))
                u = U("h_sophep", Loc.T("Sổ phép có thêm trang!"),
                    Loc.T("Vẽ nét vào sổ để đổi luật trận: đổi bộ thẻ, đổi tướng giữa lượt, cứu nguy lúc máu thấp. Cuốn sổ ở rìa làng."), "pencil");
            if (u == null && s.potentialStones > 0)
                u = U("h_stone", Loc.T("Đá tiềm năng"), Loc.T("Mở thêm dòng chỉ số cho tướng: nút Tiềm năng trong chi tiết tướng."), "rock");
            if (u == null && Progress.CaveOpen(s))
                u = U("h_cave", Loc.T("Hang Tiềm Năng"), Loc.T("Đánh boss lấy đá tiềm năng, 3 lượt mỗi ngày."), "rock");
            int trees = Trees.Open(s, cfg);
            for (int k = 2; u == null && k <= trees; k++) u = U("h_tree" + k, Loc.T("Thêm một cây bi!"), Loc.F("Giờ có {0} cây, mỗi cây {1} bi mỗi giờ. Về Nhà, bấm Xây để đặt cây mới.", k, cfg.trees.perHour.ToString("0.#")), "leaf");
            if (u == null && s.heroes.Any(kv => kv.Value.owned && Progress.CanEvolve(s, d, kv.Key)))
            {
                var id = s.heroes.First(kv => kv.Value.owned && Progress.CanEvolve(s, d, kv.Key)).Key;
                u = U("h_evo", Loc.F("{0} tiến hóa được!", d.Hero(id).name), Loc.T("Đổi dạng, mạnh hơn hẳn: nút Tiến hóa trên thanh tiến hóa ở màn Tướng."), "up");
            }
            if (u == null && Progress.BadgesOpen(s))
                u = U("h_temple", Loc.T("Đền Huy Hiệu"), Loc.T("Thắng chuỗi trận boss theo hệ, tướng cùng hệ mạnh thêm."), "crown");
            if (u == null && Progress.TeamSlots(s) >= 2)
                u = U("h_slot2", Loc.T("Ô đội thứ 2!"), Loc.T("Mang 2 tướng vào trận, đổi được ở đầu lượt."), "star");
            if (u == null && Progress.TeamSlots(s) >= 3) u = U("h_slot3", Loc.T("Ô đội thứ 3!"), Loc.T("Mang đủ 3 tướng vào trận."), "star");
            return u;
        }

        // ---------- trang "Cách chơi" (mục 6) ----------

        public sealed class Page
        {
            public string step, title, text;
        }

        // trang mở khi bước step đã chạy; cfg: số của Cây bi (tốc độ, sức chứa, cấp mở cây sau)
        public static List<Page> Pages(BalanceConfig cfg) => new List<Page>
        {
            P(Balls, Loc.T("Vòng chơi"), Loc.T("Thắng ải để có bi. Thả bi vào Máy Bi để có kinh nghiệm và rương. Lên cấp, nâng tướng, rồi đánh ải khó hơn.")),
            P(RunQueue, Loc.T("Lượt đánh"), Loc.T("Mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ. Thẻ xếp hàng, chạy lần lượt cuối lượt, rồi tướng đánh thường. Bạn luôn đi trước.")),
            P(Ult, Loc.T("Chiêu và Tuyệt kỹ"), Loc.T("Mana +20 mỗi lượt. Chiêu tốn mana, ra đòn ngay, mỗi lượt một lần. Nộ tăng khi đánh và khi bị đánh; đầy 100 nộ (và đủ mana) thì Tuyệt kỹ thay cú đánh thường.")),
            P(Counter, Loc.T("Khắc hệ"), Loc.T("Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy. Khắc địch: đánh ×1,5, chịu đòn ×0,75. Bị khắc: đánh ×0,75, chịu đòn ×1,5. Trước mỗi trận xem hệ địch, mang tướng khắc nó. Chạm vòng 5 chấm ở ô tướng để xem. Tướng đồng hành không bao giờ chịu thiệt vì hệ.")),
            P("d2", Loc.T("Hiệu ứng"), Loc.T("Bỏng, độc: mất máu đầu lượt. Hồi phục: hồi máu đầu lượt. Choáng: mất trọn lượt. Né: tránh cú đánh thường kế tiếp. Khiên: đỡ trước khi trừ máu.")),
            P(Hold, Loc.T("Máy Bi"), Loc.T("Chạm để thả, giữ để thả liền. Ô ra kinh nghiệm, cốc ra rương. Bi chạm nấm đủ 25 lần ra quà. Bảng tỉ lệ ở nút Tỉ lệ.")),
            P(Bet, Loc.T("Cược"), Loc.T("×N tốn N bi mỗi lần thả, mọi thưởng ×N. Mở theo số bi đang có. Chỉ nhanh hơn, không lời hơn.")),
            P(Copies, Loc.T("Rương"), Loc.T("Rương gỗ, bạc, vàng: bi, kinh nghiệm, bản sao thẻ, mảnh tướng, đá.")),
            P(Exp, Loc.T("Cấp"), Loc.T("Cấp của bạn là cấp của mọi tướng. Kinh nghiệm chỉ đến từ Máy Bi và rương. Lên cấp mở thêm thẻ vào bộ.")),
            P(Isles, Loc.T("Đảo và ải"), Loc.T("5 đảo chơi song song, mỗi đảo 70 ải. Cấp địch là cấp nên có. Ải tướng chắc chắn rơi mảnh; mỗi 10 ải có một rương mốc.")),
            P(Shards, Loc.T("Tướng"), Loc.T("Mảnh: thu phục, rồi lên sao. Bản sao thẻ: nâng chiêu, tuyệt kỹ, nội tại. Đá tiến hóa và cấp: tiến hóa, đổi dạng.")),
            P(Swap, Loc.T("Đội hình"), Loc.T("Đội 1 ô; cấp 60 thêm ô 2, cấp 200 thêm ô 3. Chọn tướng khắc hệ địch. Có từ 2 ô thì đổi tướng được ở đầu lượt.")),
            P(AfkBtn, Loc.T("AFK"), Loc.T("Ải đã qua tự đánh lúc bạn vắng, tối đa 12 giờ: ra mảnh và rương. Chọn ải AFK ở hộp Chuẩn bị.")),
            P(TreePlaced, Loc.T("Cây bi"), Loc.F("Cây bi ở Nhà: mỗi cây {0} bi mỗi giờ, chứa {1}, chạm cây để hái. Thêm cây ở cấp {2}: đặt bằng nút Xây.",
                cfg.trees.perHour.ToString("0.#"), cfg.trees.cap.ToString("0"), string.Join(", ", cfg.trees.unlockLevels))),
            P("g1", Loc.T("Nhà"), Loc.T("Tướng làm việc ra bi, gỗ, quặng. Gỗ và quặng dùng để xây, nâng cấp. Lên cấp thì mở thêm ô rừng, miễn phí.")),
            P("h_stone", Loc.T("Tiềm năng"), Loc.T("Đá tiềm năng mở thêm dòng chỉ số. Hang Tiềm Năng ra đá.")),
            P("h_temple", Loc.T("Đền Huy Hiệu"), Loc.T("Thắng chuỗi trận boss theo hệ: tướng cùng hệ mạnh thêm.")),
        };

        static Page P(string step, string title, string text) => new Page { step = step, title = title, text = text };

        // trang đã mở: bước của trang đã chạy (trang "Hiệu ứng" mở khi đã gặp một hiệu ứng bất kỳ)
        public static bool PageOpen(SaveData s, Page p) =>
            p.step == "d2" ? Done(s, StatusTip(StatusId.Burn)) || Done(s, StatusTip(StatusId.Poison)) || Done(s, StatusTip(StatusId.Stun)) ||
                             Done(s, StatusTip(StatusId.Regen)) || Done(s, StatusTip(StatusId.Evade)) || IsLegacy(s)
            : Done(s, p.step);

        public static string StatusTip(StatusId id) => "d2_" + (int)id;
    }
}
