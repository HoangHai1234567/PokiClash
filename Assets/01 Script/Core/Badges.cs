// Đền Huy Hiệu (chép Web/src/core/badges.ts): mở đền khi qua hết Đảo Thủy; dãy hệ X mở khi thắng mini boss đầu của Đảo X
// (ải 4 ở đảo 8 ải, ải 20 ở đảo 70 ải: Islands.MiniAt).
// Mỗi dãy 5 bậc; bậc k là chuỗi trận sinh từ công thức, thua thì đánh lại đúng trận đó, không mất tiến độ.
// Tướng hệ X được cộng Máu, Công, Thủ theo bậc cao nhất (không cộng dồn), áp qua StatMods vào HeroStats.Compute.
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class BadgeWin
    {
        public int balls;
        public int tierDone; // 0 nếu chưa xong bậc
        public SlotKind chest; // rương khi xong bậc
        public List<Reward> rewards = new List<Reward>();
    }

    public static class Badges
    {
        public static bool TempleOpen(SaveData s) => Progress.BadgesOpen(s);
        public static bool LineOpen(SaveData s, Elem z) => TempleOpen(s) && s.zones[(int)z] >= Islands.MiniAt(z);
        public static int Tier(SaveData s, Elem z) => s.badges[(int)z].tier;
        public static int MaxTier(BalanceConfig cfg) => cfg.badges.counts.Length;
        public static int Count(BalanceConfig cfg, int tier) => cfg.badges.counts[tier - 1];
        public static string TierName(BalanceConfig cfg, int tier) => cfg.badges.tiers[tier - 1];
        public static double Bonus(BalanceConfig cfg, int tier) => tier > 0 ? cfg.badges.bonus[System.Math.Min(tier, cfg.badges.bonus.Length) - 1] : 0;

        // phần cộng của hệ e theo bậc cao nhất; không có huy hiệu thì null (để số khớp bản web từng bit)
        public static StatMods Mods(SaveData s, BalanceConfig cfg, Elem e)
        {
            double b = Bonus(cfg, s.badges[(int)e].tier);
            return b > 0 ? new StatMods { hpPct = b, atkPct = b, defPct = b } : null;
        }

        // hạt giống và mã trận cố định theo (hệ, bậc, trận)
        public static uint Seed(GameData d, Elem z, int tier, int i) => (uint)(50000 + d.Zone(z).order * 1000 + tier * 100 + i);
        public static int StageId(GameData d, Elem z, int tier, int i) => 1000 + d.Zone(z).order * 100 + tier * 20 + i;

        // trận i (từ 1) của bậc tier: trận lẻ 1 boss; trận chẵn 2 tướng (tướng đầu là boss); trận cuối 3 tướng, boss là tướng hiếm nhất.
        // Tướng hệ X lấy theo vòng trong danh sách tướng của hệ (hệ chỉ có 2 tướng thì trận cuối lặp tướng).
        public static StageDef Stage(GameData d, Elem z, int tier, int i)
        {
            var cfg = d.Cfg;
            int n = Count(cfg, tier);
            var hs = d.Heroes.Where(h => h.elem == z).ToList();
            string Pick(int j) => hs[(i + tier + j) % hs.Count].id;
            int level = d.Zone(z).levelMin + cfg.badges.levelPerTier * (tier - 1) + (int)(i * cfg.badges.levelPerFight);
            List<string> ids;
            if (i == n)
            {
                var rarest = hs.Aggregate((a, b) => (int)b.rarity > (int)a.rarity ? b : a);
                ids = new List<string> { rarest.id, Pick(0), Pick(1) };
            }
            else ids = i % 2 == 0 ? new List<string> { Pick(0), Pick(1) } : new List<string> { Pick(0) };
            var st = new StageDef
            {
                id = StageId(d, z, tier, i), zone = z, idx = i, name = $"{TierName(cfg, tier)} {i}/{n}",
                kind = i == n ? StageKind.Boss : StageKind.Mini,
            };
            for (int k = 0; k < ids.Count; k++) st.enemies.Add(new StageEnemy { hero = ids[k], level = level, boss = k == 0 });
            return st;
        }

        // trận đang đánh của dãy: (bậc, trận); null nếu dãy chưa mở hoặc đã xong bậc cuối
        public static (int tier, int i)? Current(SaveData s, BalanceConfig cfg, Elem z)
        {
            if (!LineOpen(s, z)) return null;
            var b = s.badges[(int)z];
            if (b.tier >= MaxTier(cfg)) return null;
            return (b.tier + 1, b.won + 1);
        }

        // thắng trận đang đánh: bi; trận cuối của bậc thì lên bậc và mở rương (×1)
        public static BadgeWin Win(SaveData s, GameData d, Elem z, Rng rng)
        {
            var cfg = d.Cfg;
            var cur = Current(s, cfg, z);
            if (cur == null) return null;
            var (tier, _) = cur.Value;
            var b = s.badges[(int)z];
            var r = new BadgeWin { balls = cfg.badges.ballsBase + cfg.badges.ballsPerTier * tier, chest = Pachinko.FromKey(cfg.badges.chest[tier - 1]) };
            s.balls += r.balls;
            b.won++;
            if (b.won >= Count(cfg, tier))
            {
                b.tier = tier;
                b.won = 0;
                r.tierDone = tier;
                r.rewards = Pachinko.OpenChest(s, d, r.chest, 1, rng);
            }
            return r;
        }

        // dãy chưa đụng tới (vừa mở, bậc 0, chưa thắng trận nào): để sảnh hiện chấm báo
        public static bool HasNew(SaveData s, GameData d) =>
            TempleOpen(s) && d.Zones.Any(z => LineOpen(s, z.id) && s.badges[(int)z.id].tier == 0 && s.badges[(int)z.id].won == 0);
    }
}
