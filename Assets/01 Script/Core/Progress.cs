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

        public static List<int> XAllowed(SaveData s, BalanceConfig cfg)
        {
            var l = new List<int>();
            foreach (var x in cfg.xSteps) if (s.level >= x.lv) l.Add(x.x);
            return l;
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

        // bi mỗi ải: đảo sau cho nhiều hơn; lần đầu qua có thưởng thêm
        public static int StageBalls(GameData d, StageDef st, bool first)
        {
            int o = d.Zone(st.zone).order;
            // đảo 70 ải: 1 bi mỗi 4 cấp địch (cấp 1–4: 1 bi, 5–8: 2 bi); lần đầu qua ải tướng +2, mini boss +4, boss +8
            if (st.tag != StageTag.None)
            {
                int lv = st.enemies.Max(e => e.level);
                int b = 1 + o * 2 + (lv - 1) / 4;
                return b + (first ? (st.kind == StageKind.Boss ? 8 : st.kind == StageKind.Mini ? 4 : st.tag == StageTag.Hero ? 2 : 0) : 0);
            }
            int bas = 3 + o * 4 + (st.idx - 1) / 2;
            int bonus = first ? 5 + o * 2 + (st.kind == StageKind.Boss ? 7 : st.kind == StageKind.Mini ? 3 : 0) : 0;
            return bas + bonus;
        }

        // ---------- độ khó, đảo gợi ý ----------

        public enum Difficulty { Easy, Fit, Hard, Wall, Done }

        public static Difficulty DifficultyOf(ZoneDef z, int level, bool done)
        {
            if (done) return Difficulty.Done;
            if (level >= z.levelMax) return Difficulty.Easy;
            if (level >= z.levelMin) return Difficulty.Fit;
            if (level >= z.levelMin - 3) return Difficulty.Hard;
            return Difficulty.Wall;
        }

        public static string DifficultyText(Difficulty d) =>
            d == Difficulty.Done ? "Đã chinh phục" : d == Difficulty.Easy ? "Dễ" : d == Difficulty.Fit ? "Vừa sức" : d == Difficulty.Hard ? "Khó" : "Quá mạnh!";

        // xong đảo: qua hết ải (70 hoặc 8, Islands.Size)
        public static bool ZoneDone(SaveData s, Elem z) => s.zones[(int)z] >= Islands.Size(z);
        public static int ZonesDone(SaveData s) => Elements.All.Count(z => ZoneDone(s, z));

        // ô đội mở theo tiến trình (chép TEAM_SLOT_ZONES, teamSlots của Web/src/core/progression.ts): lúc đầu mang 1 tướng;
        // xong 1 đảo (đánh tới đảo thứ 2) mở ô 2, xong 3 đảo (tới đảo thứ 4) mở ô 3. Phần tử i: số đảo phải xong để mở ô i + 1.
        public static readonly int[] TeamSlotZones = { 0, 1, 3 };
        public static int TeamSlots(SaveData s)
        {
            int done = ZonesDone(s);
            return TeamSlotZones.Count(n => done >= n);
        }

        // đảo nên đánh: đảo chưa xong đầu tiên (theo thứ tự) mà người chơi theo được (cấp ≥ cận dưới − 3)
        public static ZoneDef RecommendedZone(SaveData s, GameData d)
        {
            var order = d.Zones.OrderBy(z => z.order).ToList();
            return order.FirstOrDefault(z => !ZoneDone(s, z.id) && s.level >= z.levelMin - 3)
                   ?? order.FirstOrDefault(z => !ZoneDone(s, z.id))
                   ?? order[0];
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
            int o = d.Zone(z).order;
            int N = Islands.Chests(z).Length;
            bool big = n == N - 1;
            // 2 rương (đảo 8 ải): 10 bi 2 thẻ, 20 bi 4 thẻ; 7 rương: 4, 5, 6 … bi, 1–2 thẻ, rương cuối 15 bi 4 thẻ
            var r = new ZoneChest
            {
                zone = z,
                n = n,
                balls = N == 2 ? (n == 0 ? 10 : 20) + o * (n == 0 ? 5 : 10) : (big ? 15 : 4 + n) + o * (big ? 10 : 5),
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
        public static bool BadgesOpen(SaveData s) => ZoneDone(s, Elem.Thuy);
        public static bool CaveOpen(SaveData s) => s.zones[(int)Elem.Hoa] >= 4;

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
                    if (first) r.shards.Add(AddShards(s, d, dr.hero, dr.min, rng));
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
