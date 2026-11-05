// Tiến trình, chép từ Web/src/core/progression.ts: cấp, EXP, nút ×N (mốc 0); ải, thưởng ải, mảnh tướng (mốc add-card-battle).
// Mốc add-hero-roster chép tiếp phần nâng thẻ, tiến hóa sao, thẻ rơi từ rương.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class ShardResult
    {
        public string hero;
        public int n;
        public bool unlocked;
        public int converted; // mảnh của tướng đã có đổi thành bản sao thẻ
    }

    public sealed class StageReward
    {
        public int balls;
        public bool first;
        public List<ShardResult> shards = new List<ShardResult>();
    }

    public static class Progress
    {
        public static readonly CardSlot[] Slots = { CardSlot.Skill, CardSlot.Ult, CardSlot.Passive };

        public static int ExpToNext(int lv, BalanceConfig cfg) => Js.RoundInt(cfg.expBase * Math.Pow(lv, cfg.expPow));

        // Cộng EXP, trả số cấp vừa lên.
        public static int AddExp(SaveData s, int n, BalanceConfig cfg)
        {
            int ups = 0;
            s.exp += n;
            while (s.level < cfg.maxLevel && s.exp >= ExpToNext(s.level, cfg))
            {
                s.exp -= ExpToNext(s.level, cfg);
                s.level++;
                ups++;
            }
            if (s.level >= cfg.maxLevel) s.exp = Math.Min(s.exp, ExpToNext(s.level, cfg));
            return ups;
        }

        // mức cược đang mở: theo số bi đang có (×1 luôn mở). Bi tụt dưới mốc thì mất mức đó cho tới khi có lại.
        public static List<int> XAllowed(SaveData s, BalanceConfig cfg)
        {
            var l = new List<int>();
            foreach (var x in cfg.xSteps) if (x.x == 1 || s.balls >= x.balls) l.Add(x.x);
            return l;
        }

        // mức cược cao nhất đang mở, không quá want
        public static int XBest(SaveData s, BalanceConfig cfg, int want)
        {
            int best = 1;
            foreach (int x in XAllowed(s, cfg)) if (x <= want && x > best) best = x;
            return best;
        }

        // ---------- thẻ riêng và sao ----------

        // bản sao để lên cấp lv -> lv+1 (cấp tối đa thì không lên nữa)
        public static int CardReq(BalanceConfig cfg, int lv) => lv >= cfg.cardMax ? int.MaxValue : cfg.cardReq[lv];

        public static bool CanUpCard(SaveData s, BalanceConfig cfg, string hero, CardSlot slot)
        {
            var p = s.Hero(hero);
            var c = p.Card(slot);
            return p.owned && c.lv < cfg.cardMax && c.copies >= CardReq(cfg, c.lv);
        }

        public static bool UpCard(SaveData s, BalanceConfig cfg, string hero, CardSlot slot)
        {
            if (!CanUpCard(s, cfg, hero, slot)) return false;
            var c = s.Hero(hero).Card(slot);
            c.copies -= CardReq(cfg, c.lv);
            c.lv++;
            return true;
        }

        public static int CardSum(SaveData s, string hero)
        {
            var p = s.Hero(hero);
            return p.skill.lv + p.ult.lv + p.passive.lv;
        }

        // điều kiện lên sao n: tổng cấp 3 thẻ và cấp người chơi
        public static (int cards, int level) StarNeed(BalanceConfig cfg, int star) =>
            (star < cfg.starCards.Length ? cfg.starCards[star] : int.MaxValue, star < cfg.starLevel.Length ? cfg.starLevel[star] : int.MaxValue);

        public static bool CanEvolve(SaveData s, BalanceConfig cfg, string hero)
        {
            var p = s.Hero(hero);
            if (!p.owned || p.star >= cfg.maxStar) return false;
            var need = StarNeed(cfg, p.star + 1);
            return CardSum(s, hero) >= need.cards && s.level >= need.level;
        }

        public static bool Evolve(SaveData s, BalanceConfig cfg, string hero)
        {
            if (!CanEvolve(s, cfg, hero)) return false;
            s.Hero(hero).star++;
            return true;
        }

        // số việc đang chờ ở mục Tướng (nâng thẻ, tiến hóa): chấm đỏ và số trên nút Tướng
        public static int HeroAlerts(SaveData s, GameData d, string onlyHero = null)
        {
            int n = 0;
            foreach (var h in d.Heroes)
            {
                if (onlyHero != null && h.id != onlyHero) continue;
                if (!s.Hero(h.id).owned) continue;
                if (CanEvolve(s, d.Cfg, h.id)) n++;
                foreach (var k in Slots)
                    if (CanUpCard(s, d.Cfg, h.id, k)) n++;
            }
            return n;
        }

        public static string CardOf(HeroDef h, CardSlot slot) => slot == CardSlot.Skill ? h.skill : slot == CardSlot.Ult ? h.ult : h.passive;

        // ---------- thẻ rơi từ rương: bản sao thẻ riêng của tướng đã có ----------

        public sealed class CardDrop
        {
            public string hero;
            public CardSlot slot;
            public string card;
            public Rarity rarity;
        }

        // thẻ đúng độ hiếm của tướng đã có; không có thì lùi xuống độ hiếm thấp hơn; không có gì thì null (người gọi đổi thành EXP)
        public static CardDrop RollCardDrop(SaveData s, GameData d, Rarity rarity, Rng rng)
        {
            for (int r = (int)rarity; r >= 0; r--)
            {
                var opts = new List<CardDrop>();
                foreach (var h in d.Heroes)
                {
                    if (!s.Hero(h.id).owned) continue;
                    foreach (var slot in Slots)
                    {
                        var id = CardOf(h, slot);
                        if ((int)d.Card(id).rarity == r) opts.Add(new CardDrop { hero = h.id, slot = slot, card = id, rarity = (Rarity)r });
                    }
                }
                if (opts.Count > 0) return rng.Pick(opts);
            }
            return null;
        }

        public static void GiveCard(SaveData s, CardDrop drop) => s.Hero(drop.hero).Card(drop.slot).copies++;

        public static void UnlockHero(SaveData s, string hero)
        {
            var p = s.Hero(hero);
            p.owned = true;
            p.shards = 0;
        }

        // ---------- mảnh tướng ----------

        public static ShardResult AddShards(SaveData s, GameData d, string hero, int n, Rng rng)
        {
            var p = s.Hero(hero);
            if (p.owned)
            {
                for (int i = 0; i < n; i++) p.Card(rng.Pick(Slots)).copies++;
                return new ShardResult { hero = hero, n = n, unlocked = false, converted = n };
            }
            p.shards += n;
            if (p.shards >= d.Hero(hero).shards)
            {
                p.shards = 0;
                p.owned = true;
                return new ShardResult { hero = hero, n = n, unlocked = true };
            }
            return new ShardResult { hero = hero, n = n };
        }

        // ---------- ải theo đảo ----------

        public static int TotalCleared(SaveData s) => s.zones.Sum();
        public static bool StageCleared(SaveData s, StageDef st) => st.idx <= s.zones[(int)st.zone];
        public static bool StageOpen(SaveData s, StageDef st) => st.idx <= s.zones[(int)st.zone] + 1;

        public static StageDef NextStage(SaveData s, GameData d, Elem z) =>
            d.ZoneStages(z).FirstOrDefault(st => st.idx == s.zones[(int)z] + 1);

        // bi mỗi ải theo độ sâu trong đảo, như nhau ở mọi đảo (5 đảo chơi song song, người dùng sửa 2026-11-05; trước đó đảo sau cho
        // thêm bi theo thứ tự đảo): đảo 70 ải BallsBase bi ở ải 1, cứ BallsStep ải thêm 1 bi; đảo 8 ải (tạm) quy số ải về thang 70 ải.
        // Lần đầu qua ải tướng +2, mini boss +4, boss +8.
        public const int BallsBase = 1, BallsStep = 14;

        public static int StageBalls(GameData d, StageDef st, bool first)
        {
            int n = Math.Max(2, Islands.Size(st.zone));
            int depth = (st.idx - 1) * 69 / (n - 1); // 0..69
            int b = BallsBase + depth / BallsStep;
            return b + (first ? (st.kind == StageKind.Boss ? 8 : st.kind == StageKind.Mini ? 4 : st.tag == StageTag.Hero ? 2 : 0) : 0);
        }

        // ---------- độ khó, đảo gợi ý ----------

        public enum Difficulty { Easy, Fit, Hard, Wall, Done }

        // cấp địch của ải kế tiếp trong đảo z (0 nếu đã qua hết)
        public static int NextLevel(SaveData s, GameData d, Elem z) => NextStage(s, d, z)?.enemies.Max(e => e.level) ?? 0;

        // độ khó của đảo theo ải kế tiếp (5 đảo song song nên không xét theo khoảng cấp của đảo): hơn địch từ EasyMargin cấp là Dễ,
        // bằng hoặc hơn là Vừa sức, thiếu tới LevelSlack cấp là Khó, thiếu nhiều hơn là Quá mạnh
        public static Difficulty DifficultyOf(SaveData s, GameData d, ZoneDef z)
        {
            if (ZoneDone(s, z.id)) return Difficulty.Done;
            int lv = NextLevel(s, d, z.id);
            if (s.level >= lv + EasyMargin) return Difficulty.Easy;
            if (s.level >= lv) return Difficulty.Fit;
            if (s.level >= lv - LevelSlack) return Difficulty.Hard;
            return Difficulty.Wall;
        }

        public static string DifficultyText(Difficulty d) =>
            d == Difficulty.Done ? "Đã chinh phục" : d == Difficulty.Easy ? "Dễ" : d == Difficulty.Fit ? "Vừa sức" : d == Difficulty.Hard ? "Khó" : "Quá mạnh!";

        // xong đảo: qua hết ải (70 hoặc 8, Islands.Size)
        public static bool ZoneDone(SaveData s, Elem z) => s.zones[(int)z] >= Islands.Size(z);
        public static int ZonesDone(SaveData s) => Elements.All.Count(z => ZoneDone(s, z));

        // ô đội mở theo cấp người chơi (người dùng chốt 2026-11-03, GD_Claude/15_TuongKhoiDau.md; web mở theo số đảo đã xong):
        // lúc đầu mang 1 tướng, ô 2 ở cấp 10, ô 3 ở cấp 30
        public const int TeamSlotMax = 3;
        // thang cấp 200 (2026-11-04): ô 2 ở cấp 60 (giữa đảo Hỏa, như cấp 10 của thang cũ), ô 3 ở cấp 200 (cấp tối đa, như cấp 30 cũ)
        public static readonly int[] SlotLevels = { 1, 60, 200 };

        // thiếu tới LevelSlack cấp so với địch của ải kế vẫn tính là Khó (thiếu 6 cấp: tỉ lệ thắng còn 8–73% tùy kiểu ải); hơn từ
        // EasyMargin cấp là Dễ
        public const int LevelSlack = 6, EasyMargin = 10;

        public static int TeamSlots(SaveData s) => SlotsAt(s.level);
        public static int SlotsAt(int level) => SlotLevels.Count(lv => level >= lv);

        // điều kiện mở ô đội i (0..2), hiện ở ô đang khoá: "mở khi …"
        public static string SlotNeed(int i) => i <= 0 || i >= SlotLevels.Length ? "" : $"đạt cấp {SlotLevels[i]}";

        // đảo nên đánh: 5 đảo chơi song song, nên gợi ý đảo chưa xong có ải kế tiếp cấp thấp nhất (bằng nhau thì theo thứ tự đảo)
        public static ZoneDef RecommendedZone(SaveData s, GameData d)
        {
            var order = d.Zones.OrderBy(z => z.order).ToList();
            return order.Where(z => !ZoneDone(s, z.id)).OrderBy(z => NextLevel(s, d, z.id)).FirstOrDefault() ?? order[0];
        }

        // hệ khắc hệ z (để gợi ý): Thủy khắc Hỏa...
        public static Elem CounterOf(Elem z) => Elements.All.First(e => Elements.Beats(e) == z);

        // ---------- rương mốc của đảo: đảo 8 ải qua 4 và 8 ải, đảo 70 ải mỗi 10 ải (Islands.Chests) ----------

        public sealed class ZoneChest
        {
            public Elem zone;
            public int n; // chỉ số rương trong Islands.Chests(zone)
            public int balls;
            public List<CardDrop> cards = new List<CardDrop>();
            public bool big;
        }

        // rương mở được (chỉ số trong Islands.Chests), -1 nếu chưa
        public static int ZoneChestReady(SaveData s, Elem z)
        {
            int n = s.zoneChests[(int)z];
            var at = Islands.Chests(z);
            return n < at.Length && s.zones[(int)z] >= at[n] ? n : -1;
        }

        static readonly Rarity[] ChestRarities = { Rarity.Common, Rarity.Uncommon, Rarity.Rare, Rarity.Epic };
        static readonly double[] ChestWeights = { 30, 40, 25, 5 };

        public static ZoneChest ClaimZoneChest(SaveData s, GameData d, Elem z, Rng rng)
        {
            int n = ZoneChestReady(s, z);
            if (n < 0) return null;
            int N = Islands.Chests(z).Length;
            bool big = n == N - 1;
            // như nhau ở mọi đảo (đảo song song): 2 rương (đảo 8 ải, tạm): 20 bi 2 thẻ, 40 bi 4 thẻ; 7 rương: 4, 7, 10 … bi (thêm 3 mỗi
            // rương), 1–2 thẻ, rương cuối 35 bi 4 thẻ
            var r = new ZoneChest
            {
                zone = z,
                n = n,
                balls = N == 2 ? (n == 0 ? 20 : 40) : big ? 35 : 4 + 3 * n,
                big = big,
            };
            int nCards = N == 2 ? (n == 0 ? 2 : 4) : big ? 4 : n < 3 ? 1 : 2;
            s.balls += r.balls;
            for (int i = 0; i < nCards; i++)
            {
                var rar = rng.Weighted(ChestRarities, x => ChestWeights[(int)x]);
                var drop = RollCardDrop(s, d, rar, rng);
                if (drop != null)
                {
                    GiveCard(s, drop);
                    r.cards.Add(drop);
                }
            }
            s.zoneChests[(int)z] = n + 1;
            return r;
        }

        // tướng boss đã gặp: rơi mảnh khi AFK và trong rương máy bi (ải không phải thường đã qua, bỏ tướng tặng)
        public static List<string> AfkBossPool(SaveData s, GameData d)
        {
            var outL = new List<string>();
            foreach (var st in d.Stages)
                if (StageCleared(s, st) && st.kind != StageKind.Normal)
                    foreach (var dr in st.drops)
                        if (!dr.gift && !outL.Contains(dr.hero)) outL.Add(dr.hero);
            return outL;
        }

        // ---------- công trình side meta ở rìa làng ----------

        public static bool FarmOpen(SaveData s) => s.heroes.Values.Count(h => h.owned) >= 3;
        // đảo song song (2026-11-05): Đền Huy Hiệu mở khi thắng mini boss đầu của một đảo bất kỳ (ải 20, đảo 8 ải là ải 4; trước đây là
        // qua hết Đảo Thủy); Hang Tiềm Năng mở ở cấp CaveLevel (tầng Dễ cấp 29; trước đây là thắng mini boss Đảo Hỏa)
        public const int CaveLevel = 30;
        public static bool BadgesOpen(SaveData s) => Elements.All.Any(z => s.zones[(int)z] >= Islands.MiniAt(z));
        public static bool CaveOpen(SaveData s) => s.level >= CaveLevel;

        public static StageReward WinStage(SaveData s, GameData d, int id, Rng rng)
        {
            var st = d.Stage(id);
            bool first = !StageCleared(s, st);
            int balls = StageBalls(d, st, first);
            s.balls += balls;
            s.clears[id] = (s.clears.TryGetValue(id, out var c) ? c : 0) + 1;
            if (first) s.zones[(int)st.zone] = st.idx;
            var r = new StageReward { balls = balls, first = first };
            foreach (var dr in st.drops)
            {
                if (dr.gift)
                {
                    if (!first) continue;
                    var gh = dr.HeroFor(s);
                    var res = AddShards(s, d, gh, dr.min, rng);
                    r.shards.Add(res);
                    // tướng tặng vào ô đội còn trống (ô 2 mở cùng lúc nhận quà ở ải 3 đảo Thủy, 15_TuongKhoiDau.md)
                    if (res.unlocked && !s.team.Contains(gh) && s.team.Count < TeamSlots(s)) s.team.Add(gh);
                    continue;
                }
                double chance = first ? dr.chance : dr.chance * (dr.chance >= 1 ? 0.5 : 0.8);
                if (rng.Chance(chance)) r.shards.Add(AddShards(s, d, dr.hero, rng.Int(dr.min, dr.max), rng));
            }
            s.stats.battles++;
            s.stats.wins++;
            return r;
        }
    }
}
