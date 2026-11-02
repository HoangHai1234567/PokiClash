// Tiềm năng (chép Web/src/core/potential.ts và data/potential.ts): 4 ô mỗi tướng mở theo sao; khai phá tốn đá, quay lại mọi ô đã mở
// và không khoá (khoá tối đa 2 ô, mỗi ô khoá +2 đá), kết quả chờ người chơi chọn giữ mới / giữ cũ. Dòng Công, Thủ, Máu, Tốc vào StatMods;
// chí mạng, hút máu, mana, nộ là hiệu ứng đầu trận (BattleStart). Hang Tiềm Năng: 4 tầng, 3 lượt thắng mỗi ngày, thắng ra đá.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public enum PotKind { Atk, Def, Hp, Spd, Crit, Lifesteal, Mana, Rage }

    // một dòng tiềm năng: loại và độ hiếm (0 Thường … 4 Huyền thoại)
    public sealed class PotLine
    {
        public PotKind k;
        public int r;
        public PotLine Copy() => new PotLine { k = k, r = r };
    }

    // lượt Hang trong ngày (theo giờ máy)
    public sealed class CaveDay
    {
        public int day;
        public int wins;
        public Elem? pick; // hệ người chơi chọn (Thứ Bảy, Chủ nhật)
    }

    public static class Potential
    {
        public static readonly string[] KindKeys = { "atk", "def", "hp", "spd", "crit", "lifesteal", "mana", "rage" };
        public static readonly PotKind[] Kinds = (PotKind[])Enum.GetValues(typeof(PotKind));
        static readonly int[] RarityIdx = { 0, 1, 2, 3, 4 };

        public static string Key(PotKind k) => KindKeys[(int)k];
        public static PotKind FromKey(string s) => (PotKind)Math.Max(0, Array.IndexOf(KindKeys, s));
        public static bool IsPct(PotKind k) => k != PotKind.Spd && k != PotKind.Mana && k != PotKind.Rage;

        public static string Name(PotKind k) =>
            k == PotKind.Atk ? "Công" : k == PotKind.Def ? "Thủ" : k == PotKind.Hp ? "Máu" : k == PotKind.Spd ? "Tốc"
            : k == PotKind.Crit ? "Chí mạng" : k == PotKind.Lifesteal ? "Hút máu" : k == PotKind.Mana ? "Mana đầu trận" : "Nộ đầu trận";

        public static double Value(BalanceConfig cfg, PotLine x) => cfg.potential.Val((int)x.k, x.r);

        // "Công +8%", "Tốc +6", "Nộ đầu trận +20"
        public static string Text(PotKind k, double v) =>
            IsPct(k) ? $"{Name(k)} +{Math.Round(v * 100, 1).ToString("0.#").Replace('.', ',')}%" : $"{Name(k)} +{v:0}";

        // tổng mỗi loại (hai ô cùng loại cộng dồn), chặn ở trần
        public static double[] Totals(BalanceConfig cfg, IEnumerable<PotLine> lines)
        {
            var t = new double[Kinds.Length];
            if (lines != null)
                foreach (var x in lines)
                    if (x != null) t[(int)x.k] += Value(cfg, x);
            for (int i = 0; i < t.Length; i++) t[i] = Math.Min(cfg.potential.caps[i], t[i]);
            return t;
        }

        public static int OpenSlots(BalanceConfig cfg, int star) => cfg.potential.slotStar.Count(x => star >= x);

        // số ô khoá thật (ô đã mở và đang có dòng)
        public static int LockCount(SaveData s, BalanceConfig cfg, string hero, IList<bool> locks)
        {
            var p = s.Hero(hero);
            int open = OpenSlots(cfg, p.star), n = 0;
            for (int i = 0; i < open; i++)
                if (i < locks.Count && locks[i] && p.potential[i] != null) n++;
            return n;
        }

        // giá: mỗi ô được quay 1 đá, mỗi ô khoá thêm lockCost đá
        public static int SpinCost(SaveData s, BalanceConfig cfg, string hero, IList<bool> locks)
        {
            int open = OpenSlots(cfg, s.Hero(hero).star), lk = LockCount(s, cfg, hero, locks);
            return open - lk + cfg.potential.lockCost * lk;
        }

        // khai phá: trừ đá, quay các ô mở không khoá; kết quả để ở potentialNew chờ Keep. null nếu không quay được.
        public static PotLine[] Spin(SaveData s, BalanceConfig cfg, string hero, IList<bool> locks, Rng rng)
        {
            var p = s.Hero(hero);
            if (p == null || !p.owned) return null;
            int open = OpenSlots(cfg, p.star), lk = LockCount(s, cfg, hero, locks);
            if (lk > cfg.potential.maxLocks || open - lk <= 0) return null;
            int cost = SpinCost(s, cfg, hero, locks);
            if (s.potentialStones < cost) return null;
            s.potentialStones -= cost;
            var next = new PotLine[4];
            for (int i = 0; i < 4; i++)
            {
                var x = p.potential[i];
                if (i >= open || (i < locks.Count && locks[i] && x != null))
                {
                    next[i] = x?.Copy();
                    continue;
                }
                var k = rng.Pick(Kinds);
                int r = rng.Weighted(RarityIdx, j => cfg.potential.rarityWeight[j]);
                next[i] = new PotLine { k = k, r = r };
            }
            p.potentialNew = next;
            return next;
        }

        // chọn giữ mới hay giữ cũ (đá đã tiêu không hoàn)
        public static void Keep(SaveData s, string hero, bool keepNew)
        {
            var p = s.Hero(hero);
            if (p?.potentialNew == null) return;
            if (keepNew) p.potential = p.potentialNew;
            p.potentialNew = null;
        }

        // phần cộng của tướng: huy hiệu hệ + tiềm năng (Máu, Công, Thủ, Tốc); null nếu không có gì (để số khớp bản web)
        public static StatMods Mods(SaveData s, GameData d, HeroDef h)
        {
            var cfg = d.Cfg;
            double b = Badges.Bonus(cfg, s.badges[(int)h.elem].tier);
            var t = Totals(cfg, s.Hero(h.id).potential);
            double hp = b + t[(int)PotKind.Hp], atk = b + t[(int)PotKind.Atk], def = b + t[(int)PotKind.Def], spd = t[(int)PotKind.Spd];
            return hp != 0 || atk != 0 || def != 0 || spd != 0 ? new StatMods { hpPct = hp, atkPct = atk, defPct = def, spd = spd } : null;
        }

        // hiệu ứng đầu trận của tiềm năng; null nếu không có
        public static BattleStart Start(SaveData s, GameData d, string hero)
        {
            var t = Totals(d.Cfg, s.Hero(hero).potential);
            double mana = t[(int)PotKind.Mana], rage = t[(int)PotKind.Rage], crit = t[(int)PotKind.Crit], ls = t[(int)PotKind.Lifesteal];
            return mana != 0 || rage != 0 || crit != 0 || ls != 0 ? new BattleStart { mana = mana, rage = rage, crit = crit, lifesteal = ls } : null;
        }

        // ---------- Hang Tiềm Năng ----------

        public static bool CaveOpen(SaveData s) => Progress.CaveOpen(s);

        // thứ trong tuần của ngày (đếm từ 1/1/1970 là thứ Năm): 0 = Chủ nhật
        public static int WeekdayOf(int day) => ((day + 4) % 7 + 7) % 7;

        public static CaveDay CaveOf(SaveData s, int day)
        {
            if (s.cave == null || s.cave.day != day) s.cave = new CaveDay { day = day };
            return s.cave;
        }

        public static int CaveLeft(SaveData s, BalanceConfig cfg, int day)
        {
            var c = CaveOf(s, day);
            return cfg.cave.winsPerDay + AdGate.Used(s, day, AdGate.CaveExtra) * cfg.cave.adExtra - c.wins;
        }

        // hệ boss hôm nay (null: hôm nay người chơi chọn mà chưa chọn)
        public static Elem? CaveElem(SaveData s, BalanceConfig cfg, int day) => cfg.cave.Weekday(WeekdayOf(day)) ?? CaveOf(s, day).pick;

        public static bool CavePick(SaveData s, BalanceConfig cfg, int day, Elem z)
        {
            if (cfg.cave.Weekday(WeekdayOf(day)) != null) return false;
            CaveOf(s, day).pick = z;
            return true;
        }


        // trận của tầng: 1 boss và 1 tướng phụ cùng hệ (tướng theo vòng trong danh sách tướng của hệ)
        public static StageDef CaveStage(GameData d, Elem z, int tier)
        {
            var t = d.Cfg.cave.tiers[tier];
            var hs = d.Heroes.Where(h => h.elem == z).ToList();
            var st = new StageDef { id = 2000 + d.Zone(z).order * 10 + tier, zone = z, idx = tier + 1, name = $"Hang {t.name}", kind = StageKind.Boss };
            st.enemies.Add(new StageEnemy { hero = hs[tier % hs.Count].id, level = t.level, boss = true });
            st.enemies.Add(new StageEnemy { hero = hs[(tier + 1) % hs.Count].id, level = Math.Max(1, t.level - 2), boss = false });
            return st;
        }

        // thắng tầng: đá, trừ một lượt; hết lượt thì 0
        public static int WinCave(SaveData s, BalanceConfig cfg, int day, int tier)
        {
            if (CaveLeft(s, cfg, day) <= 0) return 0;
            CaveOf(s, day).wins++;
            int n = cfg.cave.tiers[tier].stones;
            s.potentialStones += n;
            return n;
        }
    }
}
