// Đền Huy Hiệu (chép Web/src/core/badges.ts; 2026-11-17 tăng dày nội dung, GD_Claude/20_TangDayNoiDung.md): mở đền khi thắng mini boss
// đầu của một đảo bất kỳ; dãy hệ X mở khi thắng mini boss đầu của Đảo X (ải 20 ở đảo 70 ải: Islands.MiniAt).
// - Mỗi dãy 10 bậc (Đồng … Thần Thoại); bậc k là chuỗi trận sinh từ công thức, thua thì đánh lại đúng trận đó, không mất tiến độ.
//   Cấp địch từ cấp mini boss mở dãy lên tới khoảng cấp 205 ở trận cuối bậc 10. Địch quy về sức tướng Khá (như đảo 70 ải) để độ khó
//   các dãy không lệch theo tướng hiếm của hệ.
// - Mỗi trận chấm 1–3 sao (thắng; không tướng nào gục; thắng trong starRounds hiệp mỗi địch), giữ số sao cao nhất; trận đã thắng đánh lại được
//   để lấy thêm sao. Tổng sao cả đền qua mỗi giftEvery sao là một mốc quà (rương, đá tiến hóa, đá tinh, đá tiềm năng).
// - Tướng hệ X được cộng Máu, Công, Thủ theo bậc cao nhất (không cộng dồn các bậc), áp qua StatMods vào HeroStats.Compute; bậc cao
//   của mỗi dãy cộng thêm chút cho mọi tướng (teamBonus, cộng 5 dãy). Đặc tính hệ (mở và nâng ở traitTiers): một hiệu ứng đầu trận
//   cho tướng cùng hệ (Thủy khiên, Hỏa nộ, Kim chí mạng, Mộc hút máu, Thổ giảm sát thương), đi qua BattleStart như tiềm năng.
// - Xong bậc: rương (mở ngay), đá tiến hóa, đá tinh theo bậc.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    // một mốc sao vừa nhận
    public sealed class BadgeGiftWin
    {
        public int at; // số sao của mốc
        public BadgeGift gift;
        public SlotKind chest;
        public List<Reward> rewards = new List<Reward>();
    }

    public sealed class BadgeWin
    {
        public int balls;
        public int tierDone; // 0 nếu chưa xong bậc
        public SlotKind chest; // rương khi xong bậc
        public List<Reward> rewards = new List<Reward>();
        public int evo, crystal; // đá tiến hóa, đá tinh khi xong bậc
        public bool replay; // đánh lại trận đã thắng (chỉ lấy sao)
        public int stars, oldStars; // sao của trận này, sao cao nhất trước đó
        public List<BadgeGiftWin> gifts = new List<BadgeGiftWin>(); // mốc sao vừa qua
    }

    public static class Badges
    {
        public static bool TempleOpen(SaveData s) => Progress.BadgesOpen(s);
        public static bool LineOpen(SaveData s, Elem z) => TempleOpen(s) && s.zones[(int)z] >= Islands.MiniAt(z);
        public static int Tier(SaveData s, Elem z) => s.badges[(int)z].tier;
        public static int MaxTier(BalanceConfig cfg) => cfg.badges.counts.Length;
        public static int Count(BalanceConfig cfg, int tier) => cfg.badges.counts[tier - 1];
        public static string TierName(BalanceConfig cfg, int tier) => Loc.T(cfg.badges.tiers[Math.Max(1, Math.Min(tier, cfg.badges.tiers.Count)) - 1]);
        public static double Bonus(BalanceConfig cfg, int tier) => tier > 0 ? cfg.badges.bonus[Math.Min(tier, cfg.badges.bonus.Length) - 1] : 0;

        // phần cộng cho mọi tướng của một dãy ở bậc tier
        public static double TeamBonusOf(BalanceConfig cfg, int tier) =>
            tier > 0 && cfg.badges.teamBonus.Length > 0 ? cfg.badges.teamBonus[Math.Min(tier, cfg.badges.teamBonus.Length) - 1] : 0;

        // phần cộng cho mọi tướng: cộng của 5 dãy
        public static double TeamBonus(SaveData s, BalanceConfig cfg)
        {
            double t = 0;
            for (int i = 0; i < s.badges.Length; i++) t += TeamBonusOf(cfg, s.badges[i].tier);
            return t;
        }

        // phần cộng Máu, Công, Thủ của tướng hệ e: bậc cao nhất của dãy e + phần cả đội
        public static double StatBonus(SaveData s, BalanceConfig cfg, Elem e) => Bonus(cfg, s.badges[(int)e].tier) + TeamBonus(s, cfg);

        // phần cộng của hệ e; không có gì thì null (để số khớp bản web từng bit)
        public static StatMods Mods(SaveData s, BalanceConfig cfg, Elem e)
        {
            double b = StatBonus(s, cfg, e);
            return b > 0 ? new StatMods { hpPct = b, atkPct = b, defPct = b } : null;
        }

        // ---------- đặc tính hệ ----------

        // nấc đặc tính của dãy ở bậc tier: 0 (chưa mở) .. traitTiers.Length
        public static int TraitLevel(BalanceConfig cfg, int tier) => cfg.badges.traitTiers.Count(t => tier >= t);

        public static string TraitName(BalanceConfig cfg, Elem e) =>
            (int)e < cfg.badges.traitName.Length ? cfg.badges.traitName[(int)e] : "";

        // loại và số của đặc tính hệ e ở nấc lv (từ 1); null nếu chưa có
        public static (PotKind k, double v)? TraitAt(BalanceConfig cfg, Elem e, int lv)
        {
            int n = cfg.badges.traitTiers.Length;
            if (lv <= 0 || n == 0 || (int)e >= cfg.badges.traitKind.Length || !Potential.IsKey(cfg.badges.traitKind[(int)e])) return null;
            lv = Math.Min(lv, n);
            return (Potential.FromKey(cfg.badges.traitKind[(int)e]), cfg.badges.traitValue[(int)e * n + lv - 1]);
        }

        // đặc tính hệ e của người chơi; null nếu chưa có
        public static (PotKind k, double v)? Trait(SaveData s, BalanceConfig cfg, Elem e) => TraitAt(cfg, e, TraitLevel(cfg, s.badges[(int)e].tier));

        // "Màng Nước: Khiên đầu trận +12%"
        public static string TraitText(BalanceConfig cfg, Elem e, int lv)
        {
            var t = TraitAt(cfg, e, lv);
            return t == null ? "" : $"{TraitName(cfg, e)}: {Potential.Text(t.Value.k, t.Value.v)}";
        }

        // bậc mở nấc kế tiếp của đặc tính (0 nếu đã tối đa)
        public static int NextTraitTier(BalanceConfig cfg, int tier) => cfg.badges.traitTiers.FirstOrDefault(t => t > tier);

        // ---------- trận ----------

        // hạt giống cố định theo (hệ, bậc, trận); mã trận riêng (10000+, không trùng ải đảo, Hang)
        public static uint Seed(GameData d, Elem z, int tier, int i) => (uint)(50000 + d.Zone(z).order * 1000 + tier * 100 + i);
        public static int StageId(GameData d, Elem z, int tier, int i) => 10000 + d.Zone(z).order * 1000 + tier * 20 + i;

        // cấp nền của dãy hệ z: cấp mini boss đầu của Đảo z (ải mở dãy, Islands.MiniAt)
        public static int BaseLevel(GameData d, Elem z) =>
            d.ZoneStages(z).FirstOrDefault(st => st.idx == Islands.MiniAt(z))?.enemies.Max(e => e.level) ?? d.Zone(z).levelMin;

        // cấp địch trận i của bậc tier
        public static int Level(GameData d, Elem z, int tier, int i) =>
            BaseLevel(d, z) + d.Cfg.badges.levelPerTier * (tier - 1) + (int)(i * d.Cfg.badges.levelPerFight);

        // cường hóa của địch: quy về sức tướng Khá (Islands.NormRarity) rồi nhân 1 + extra; làm tròn 2 chữ số
        public static double NormBuff(GameData d, string hero, double extra)
        {
            var h = d.Hero(hero);
            double norm = HeroStats.PowerOf(Islands.NormRarity) / HeroStats.PowerOf(h.rarity);
            return Math.Round(norm * (1 + extra) - 1, 2);
        }

        // trận i (từ 1) của bậc tier: trận lẻ 1 boss; trận chẵn 2 tướng (tướng đầu là boss); trận cuối 3 tướng, boss là tướng hiếm nhất.
        // Tướng hệ X lấy theo vòng trong danh sách tướng của hệ (hệ chỉ có 2 tướng thì trận cuối lặp tướng).
        public static StageDef Stage(GameData d, Elem z, int tier, int i)
        {
            var cfg = d.Cfg;
            int n = Count(cfg, tier);
            var hs = d.Heroes.Where(h => h.elem == z).ToList();
            string Pick(int j) => hs[(i + tier + j) % hs.Count].id;
            int level = Level(d, z, tier, i);
            List<string> ids;
            if (i == n)
            {
                var rarest = hs.Aggregate((a, b) => (int)b.rarity > (int)a.rarity ? b : a);
                ids = new List<string> { rarest.id, Pick(0), Pick(1) };
            }
            else ids = i % 2 == 0 ? new List<string> { Pick(0), Pick(1) } : new List<string> { Pick(0) };
            double extra = cfg.badges.foeBuff + cfg.badges.foeTierBuff * (tier - 1) + (i == n ? cfg.badges.foeLastBuff : 0);
            var st = new StageDef
            {
                id = StageId(d, z, tier, i), zone = z, idx = i, name = $"{TierName(cfg, tier)} {i}/{n}",
                kind = i == n ? StageKind.Boss : StageKind.Mini,
            };
            for (int k = 0; k < ids.Count; k++)
                st.enemies.Add(new StageEnemy { hero = ids[k], level = level, boss = k == 0, buff = NormBuff(d, ids[k], extra) });
            return st;
        }

        // trận đang đánh của dãy: (bậc, trận); null nếu dãy chưa mở hoặc đã xong bậc cuối. Bản lưu cũ đã thắng nhiều trận hơn số trận
        // mới của bậc thì đang ở trận cuối của bậc
        public static (int tier, int i)? Current(SaveData s, BalanceConfig cfg, Elem z)
        {
            if (!LineOpen(s, z)) return null;
            var b = s.badges[(int)z];
            if (b.tier >= MaxTier(cfg)) return null;
            return (b.tier + 1, Math.Min(b.won + 1, Count(cfg, b.tier + 1)));
        }

        // trận (bậc, i) đã thắng chưa
        public static bool Won(SaveData s, BalanceConfig cfg, Elem z, int tier, int i)
        {
            var b = s.badges[(int)z];
            if (tier <= b.tier) return true;
            var cur = Current(s, cfg, z);
            return cur != null && tier == cur.Value.tier && i < cur.Value.i;
        }

        // ---------- sao ----------

        // chỉ số của trận (bậc, i) trong chuỗi sao của dãy (bậc 1 trận 1 là 0)
        public static int FightIndex(BalanceConfig cfg, int tier, int i)
        {
            int k = 0;
            for (int t = 1; t < tier; t++) k += Count(cfg, t);
            return k + i - 1;
        }

        public static int FightsTotal(BalanceConfig cfg) => cfg.badges.counts.Sum();

        // sao cao nhất của trận; trận đã thắng từ trước khi có sao (bản lưu cũ) tính 1 sao
        public static int Stars(SaveData s, BalanceConfig cfg, Elem z, int tier, int i)
        {
            var str = s.badges[(int)z].stars ?? "";
            int idx = FightIndex(cfg, tier, i);
            int v = idx < str.Length ? Math.Max(0, Math.Min(3, str[idx] - '0')) : 0;
            return v == 0 && Won(s, cfg, z, tier, i) ? 1 : v;
        }

        static void SetStars(SaveData s, BalanceConfig cfg, Elem z, int tier, int i, int v)
        {
            var b = s.badges[(int)z];
            var c = (b.stars ?? "").ToCharArray().ToList();
            int idx = FightIndex(cfg, tier, i);
            while (c.Count <= idx) c.Add('0');
            c[idx] = (char)('0' + v);
            b.stars = new string(c.ToArray());
        }

        // tổng sao của một bậc, của một dãy, của cả đền
        public static int TierStars(SaveData s, BalanceConfig cfg, Elem z, int tier)
        {
            int n = 0;
            for (int i = 1; i <= Count(cfg, tier); i++) n += Stars(s, cfg, z, tier, i);
            return n;
        }

        public static int LineStars(SaveData s, BalanceConfig cfg, Elem z)
        {
            int n = 0;
            for (int t = 1; t <= MaxTier(cfg); t++) n += TierStars(s, cfg, z, t);
            return n;
        }

        public static int TotalStars(SaveData s, BalanceConfig cfg)
        {
            int n = 0;
            foreach (var z in Elements.All) n += LineStars(s, cfg, z);
            return n;
        }

        public static int MaxStars(BalanceConfig cfg) => 3 * FightsTotal(cfg) * Elements.All.Length;

        // số hiệp tối đa của sao 3: starRounds hiệp mỗi địch (1 địch 2 hiệp, 3 địch 6 hiệp)
        public static int StarRounds(BalanceConfig cfg, int foes) => cfg.badges.starRounds * Math.Max(1, foes);

        // điều kiện 3 sao của một trận đã xong: thắng; không tướng nào của người chơi gục; thắng trong StarRounds hiệp
        public static (bool win, bool safe, bool fast) StarChecks(BalanceConfig cfg, Battle b)
        {
            bool win = b.winner == 0;
            return (win, win && !b.sides[0].fighters.Any(f => f.dead), win && b.round <= StarRounds(cfg, b.sides[1].fighters.Count));
        }

        public static int Grade(BalanceConfig cfg, Battle b)
        {
            var (win, safe, fast) = StarChecks(cfg, b);
            return win ? 1 + (safe ? 1 : 0) + (fast ? 1 : 0) : 0;
        }

        // ---------- mốc sao ----------

        // mốc thứ m (từ 1): cần m × giftEvery sao, quà theo vòng gifts
        public static int GiftAt(BalanceConfig cfg, int m) => m * Math.Max(1, cfg.badges.giftEvery);
        public static BadgeGift GiftOf(BalanceConfig cfg, int m) => cfg.badges.gifts.Count == 0 ? null : cfg.badges.gifts[(m - 1) % cfg.badges.gifts.Count];
        public static int GiftsTotal(BalanceConfig cfg) => cfg.badges.gifts.Count == 0 ? 0 : MaxStars(cfg) / Math.Max(1, cfg.badges.giftEvery);

        // mốc kế tiếp chưa nhận (từ 1); 0 nếu đã hết mốc
        public static int NextGift(SaveData s, BalanceConfig cfg) => s.badgeGifts < GiftsTotal(cfg) ? s.badgeGifts + 1 : 0;

        // nhận mọi mốc đã đủ sao: rương mở ngay (×1), đá cộng thẳng
        public static List<BadgeGiftWin> ClaimGifts(SaveData s, GameData d, Rng rng)
        {
            var cfg = d.Cfg;
            var list = new List<BadgeGiftWin>();
            int total = TotalStars(s, cfg);
            for (int m = NextGift(s, cfg); m > 0 && total >= GiftAt(cfg, m); m = NextGift(s, cfg))
            {
                var g = GiftOf(cfg, m);
                var w = new BadgeGiftWin { at = GiftAt(cfg, m), gift = g };
                s.badgeGifts = m;
                if (!string.IsNullOrEmpty(g.chest))
                {
                    w.chest = Pachinko.FromKey(g.chest);
                    w.rewards = Pachinko.OpenChest(s, d, w.chest, 1, rng);
                }
                s.evoStones += g.evo;
                s.potentialCrystals += g.crystal;
                s.potentialStones += g.stones;
                list.Add(w);
            }
            return list;
        }

        // ---------- thắng ----------

        // thắng trận đang đánh (1 sao): giữ cho test và công cụ cũ
        public static BadgeWin Win(SaveData s, GameData d, Elem z, Rng rng)
        {
            var cur = Current(s, d.Cfg, z);
            return cur == null ? null : Win(s, d, z, cur.Value.tier, cur.Value.i, 1, rng);
        }

        // thắng trận (tier, i) với số sao stars (1..3). Trận đang đánh: bi; trận cuối của bậc thì lên bậc, mở rương (×1), đá tiến hóa,
        // đá tinh. Trận đã thắng (đánh lại): chỉ ghi sao cao hơn. Sau đó nhận các mốc sao vừa đủ. null nếu trận chưa tới.
        public static BadgeWin Win(SaveData s, GameData d, Elem z, int tier, int i, int stars, Rng rng)
        {
            var cfg = d.Cfg;
            var cur = Current(s, cfg, z);
            bool replay = Won(s, cfg, z, tier, i);
            bool now = cur != null && cur.Value.tier == tier && cur.Value.i == i;
            if (!replay && !now) return null;
            stars = Math.Max(1, Math.Min(3, stars));
            var r = new BadgeWin { replay = replay, stars = stars, oldStars = replay ? Stars(s, cfg, z, tier, i) : 0 };
            if (stars > r.oldStars) SetStars(s, cfg, z, tier, i, stars);
            if (now)
            {
                var b = s.badges[(int)z];
                r.balls = cfg.badges.ballsBase + cfg.badges.ballsPerTier * tier;
                r.chest = Pachinko.FromKey(cfg.badges.chest[Math.Min(tier, cfg.badges.chest.Count) - 1]);
                s.balls += r.balls;
                b.won = i;
                if (b.won >= Count(cfg, tier))
                {
                    b.tier = tier;
                    b.won = 0;
                    r.tierDone = tier;
                    r.rewards = Pachinko.OpenChest(s, d, r.chest, 1, rng);
                    r.evo = tier <= cfg.badges.evo.Length ? cfg.badges.evo[tier - 1] : 0;
                    r.crystal = tier <= cfg.badges.crystal.Length ? cfg.badges.crystal[tier - 1] : 0;
                    s.evoStones += r.evo;
                    s.potentialCrystals += r.crystal;
                }
            }
            r.gifts = ClaimGifts(s, d, rng);
            return r;
        }

        // dãy chưa đụng tới (vừa mở, bậc 0, chưa thắng trận nào): để sảnh hiện chấm báo
        public static bool HasNew(SaveData s, GameData d) =>
            TempleOpen(s) && d.Zones.Any(z => LineOpen(s, z.id) && s.badges[(int)z.id].tier == 0 && s.badges[(int)z.id].won == 0);
    }
}
