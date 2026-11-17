// Tiềm năng (chép Web/src/core/potential.ts và data/potential.ts; 2026-11-17 tăng dày nội dung, GD_Claude/20_TangDayNoiDung.md):
// - 6 ô mỗi tướng, mở theo sao tổng (StarTier): Đồng 1★, Đồng 3★, Bạc 1★, Bạc 3★, Vàng 1★, Kim Cương 1★ (bản lưu cũ 4 ô vẫn đọc đúng:
//   sao cũ 1..5 đổi sang 1, 3, 6, 8, 11 nên ô đã mở vẫn mở);
// - khai phá tốn đá, quay lại mọi ô đã mở và không khoá (khoá tối đa maxLocks ô, mỗi ô khoá +lockCost đá), kết quả chờ người chơi chọn
//   giữ mới / giữ cũ. Khai phá bằng đá tinh: 1 đá tinh thay phần đá của các ô quay, mọi ô ra từ Hiếm trở lên (crystalWeight);
// - 10 loại dòng: Công, Thủ, Máu vào StatMods; chí mạng, hút máu, mana, nộ, khiên, giảm sát thương, né là hiệu ứng đầu trận
//   (BattleStart). Tốc đã bỏ (người dùng duyệt 2026-11-17: trận không dùng tốc): giữ chỗ trong enum để mảng cấu hình không lệch,
//   trọng số quay 0, không thuộc bộ nào; dòng Tốc trong bản lưu cũ đọc thành Công cùng độ hiếm (SaveData.ReadLines);
// - bộ: đủ 3 (5) dòng cùng nhóm thì có phần thưởng bộ cấp 1 (2), cộng ngoài trần của loại.
// Hang Tiềm Năng: 10 tầng mở lần lượt (qua tầng trước), thưởng lần đầu; 3 lượt thắng mỗi ngày (ải lần đầu không cần lượt), thắng ra đá;
// lượt thắng đầu tiên trong ngày ở tầng crystalFloor trở lên cho thêm đá tinh.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public enum PotKind { Atk, Def, Hp, Spd, Crit, Lifesteal, Mana, Rage, Shield, Guard, Dodge }

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

    // kết quả thắng một tầng Hang: đá của lượt (0 nếu hết lượt), thưởng lần đầu (first), đá tinh (lần đầu + lượt đầu ngày ở tầng cao)
    public sealed class CaveWin
    {
        public int stones, firstStones, crystals, evo;
        public bool first;
        public int Total => stones + firstStones;
    }

    public static class Potential
    {
        public const int Slots = 6; // số ô tối đa mỗi tướng
        public const int KindCount = 11;
        public static readonly string[] KindKeys = { "atk", "def", "hp", "spd", "crit", "lifesteal", "mana", "rage", "shield", "guard", "dodge" };
        public static readonly PotKind[] Kinds = (PotKind[])Enum.GetValues(typeof(PotKind));
        static readonly int[] RarityIdx = { 0, 1, 2, 3, 4 };

        public static string Key(PotKind k) => KindKeys[(int)k];
        public static PotKind FromKey(string s) => (PotKind)Math.Max(0, Array.IndexOf(KindKeys, s));
        public static bool IsKey(string s) => Array.IndexOf(KindKeys, s) >= 0;
        public static bool IsPct(PotKind k) => k != PotKind.Spd && k != PotKind.Mana && k != PotKind.Rage;

        static readonly string[] Names =
        {
            "Công", "Thủ", "Máu", "Tốc", "Chí mạng", "Hút máu", "Mana đầu trận", "Nộ đầu trận", "Khiên đầu trận", "Giảm sát thương", "Né đòn",
        };

        // tên ngắn cho ô nhỏ
        static readonly string[] ShortNames = { "Công", "Thủ", "Máu", "Tốc", "Chí mạng", "Hút máu", "Mana", "Nộ", "Khiên", "Giảm ST", "Né" };

        public static string Name(PotKind k) => Names[(int)k];
        public static string ShortName(PotKind k) => ShortNames[(int)k];

        public static double Value(BalanceConfig cfg, PotLine x) => cfg.potential.Val((int)x.k, x.r);

        // "Công +8%", "Tốc +6", "Nộ đầu trận +20"
        public static string Text(PotKind k, double v) =>
            IsPct(k) ? $"{Name(k)} +{Math.Round(v * 100, 1).ToString("0.#").Replace('.', ',')}%" : $"{Name(k)} +{v:0}";

        // số dạng ngắn: "+8%", "+20"
        public static string Amount(PotKind k, double v) =>
            IsPct(k) ? $"+{Math.Round(v * 100, 1).ToString("0.#").Replace('.', ',')}%" : $"+{v:0}";

        // dòng ở ô i (mảng của bản lưu cũ có thể ngắn hơn Slots)
        public static PotLine LineAt(PotLine[] lines, int i) => lines != null && i >= 0 && i < lines.Length ? lines[i] : null;

        // tổng mỗi loại (hai ô cùng loại cộng dồn), chặn ở trần; chưa gồm phần thưởng bộ
        public static double[] Totals(BalanceConfig cfg, IEnumerable<PotLine> lines)
        {
            var t = new double[KindCount];
            if (lines != null)
                foreach (var x in lines)
                    if (x != null) t[(int)x.k] += Value(cfg, x);
            for (int i = 0; i < t.Length; i++) t[i] = Math.Min(i < cfg.potential.caps.Length ? cfg.potential.caps[i] : 0, t[i]);
            return t;
        }

        // ---------- bộ ----------

        // số dòng thuộc nhóm của bộ set
        public static int SetCount(PotSet set, IEnumerable<PotLine> lines) =>
            lines == null ? 0 : lines.Count(x => x != null && Array.IndexOf(set.kinds, Key(x.k)) >= 0);

        // cấp bộ đang đạt: 0 (chưa đủ), 1, 2
        public static int SetLevel(PotSet set, IEnumerable<PotLine> lines)
        {
            int n = SetCount(set, lines), lv = 0;
            while (lv < set.need.Length && n >= set.need[lv]) lv++;
            return lv;
        }

        // phần thưởng của bộ set ở cấp lv (từ 1): (loại, số)
        public static IEnumerable<(PotKind k, double v)> SetBonusOf(PotSet set, int lv)
        {
            if (lv <= 0) yield break;
            int m = set.bonusKind.Length;
            for (int j = 0; j < m; j++)
            {
                double v = set.bonus[(lv - 1) * m + j];
                if (v != 0 && IsKey(set.bonusKind[j])) yield return (FromKey(set.bonusKind[j]), v);
            }
        }

        // phần thưởng của mọi bộ đang đạt, theo loại
        public static double[] SetBonus(BalanceConfig cfg, IEnumerable<PotLine> lines)
        {
            var t = new double[KindCount];
            var list = lines?.ToList();
            foreach (var set in cfg.potential.sets)
                foreach (var (k, v) in SetBonusOf(set, SetLevel(set, list)))
                    t[(int)k] += v;
            return t;
        }

        // tổng cuối của tướng: dòng (chặn trần) + bộ
        public static double[] Final(BalanceConfig cfg, IEnumerable<PotLine> lines)
        {
            var list = lines?.ToList();
            var t = Totals(cfg, list);
            var b = SetBonus(cfg, list);
            for (int i = 0; i < t.Length; i++) t[i] += b[i];
            return t;
        }

        // ---------- ô ----------

        public static int OpenSlots(BalanceConfig cfg, int star) => Math.Min(Slots, cfg.potential.slotStar.Count(x => star >= x));

        // sao tổng mở ô slot (0..), 0 nếu không có ô đó
        public static int SlotStar(BalanceConfig cfg, int slot) => slot < cfg.potential.slotStar.Length ? cfg.potential.slotStar[slot] : 0;

        // "Mở ở Bạc 1 sao"
        public static string SlotNeed(BalanceConfig cfg, int slot)
        {
            int st = SlotStar(cfg, slot);
            return st <= 0 ? "Chưa có" : $"Mở ở {StarTier.Name(StarTier.Tier(st))} {StarTier.InTier(st)} sao";
        }

        // số ô khoá thật (ô đã mở và đang có dòng)
        public static int LockCount(SaveData s, BalanceConfig cfg, string hero, IList<bool> locks)
        {
            var p = s.Hero(hero);
            int open = OpenSlots(cfg, p.star), n = 0;
            for (int i = 0; i < open; i++)
                if (i < locks.Count && locks[i] && LineAt(p.potential, i) != null) n++;
            return n;
        }

        // giá đá: mỗi ô được quay 1 đá, mỗi ô khoá thêm lockCost đá. Khai phá bằng đá tinh: phần các ô quay thay bằng 1 đá tinh
        // (CrystalCost), chỉ còn phần khoá tính bằng đá
        public static int SpinCost(SaveData s, BalanceConfig cfg, string hero, IList<bool> locks, bool crystal = false)
        {
            int open = OpenSlots(cfg, s.Hero(hero).star), lk = LockCount(s, cfg, hero, locks);
            return (crystal ? 0 : open - lk) + cfg.potential.lockCost * lk;
        }

        public const int CrystalCost = 1;

        // khai phá: trừ đá (và đá tinh), quay các ô mở không khoá; kết quả để ở potentialNew chờ Keep. null nếu không quay được.
        public static PotLine[] Spin(SaveData s, BalanceConfig cfg, string hero, IList<bool> locks, Rng rng, bool crystal = false)
        {
            var p = s.Hero(hero);
            if (p == null || !p.owned) return null;
            int open = OpenSlots(cfg, p.star), lk = LockCount(s, cfg, hero, locks);
            if (lk > cfg.potential.maxLocks || open - lk <= 0) return null;
            int cost = SpinCost(s, cfg, hero, locks, crystal);
            if (s.potentialStones < cost || (crystal && s.potentialCrystals < CrystalCost)) return null;
            s.potentialStones -= cost;
            if (crystal) s.potentialCrystals -= CrystalCost;
            var weights = crystal ? cfg.potential.crystalWeight : cfg.potential.rarityWeight;
            var kinds = Kinds.Where(k => KindWeight(cfg, k) > 0).ToArray();
            var next = new PotLine[Slots];
            for (int i = 0; i < Slots; i++)
            {
                var x = LineAt(p.potential, i);
                if (i >= open || (i < locks.Count && locks[i] && x != null))
                {
                    next[i] = x?.Copy();
                    continue;
                }
                var k = rng.Weighted(kinds, q => KindWeight(cfg, q));
                int r = rng.Weighted(RarityIdx, j => j < weights.Length ? weights[j] : 0);
                next[i] = new PotLine { k = k, r = r };
            }
            p.potentialNew = next;
            return next;
        }

        public static double KindWeight(BalanceConfig cfg, PotKind k) => (int)k < cfg.potential.kindWeight.Length ? cfg.potential.kindWeight[(int)k] : 0;

        // chọn giữ mới hay giữ cũ (đá đã tiêu không hoàn)
        public static void Keep(SaveData s, string hero, bool keepNew)
        {
            var p = s.Hero(hero);
            if (p?.potentialNew == null) return;
            if (keepNew) p.potential = p.potentialNew;
            p.potentialNew = null;
        }

        // phần cộng của tướng: huy hiệu (hệ + cả đội) + tiềm năng và bộ (Máu, Công, Thủ, Tốc); null nếu không có gì (để số khớp bản web)
        public static StatMods Mods(SaveData s, GameData d, HeroDef h)
        {
            var cfg = d.Cfg;
            double b = Badges.StatBonus(s, cfg, h.elem);
            var t = Final(cfg, s.Hero(h.id).potential);
            double hp = b + t[(int)PotKind.Hp], atk = b + t[(int)PotKind.Atk], def = b + t[(int)PotKind.Def], spd = t[(int)PotKind.Spd];
            return hp != 0 || atk != 0 || def != 0 || spd != 0 ? new StatMods { hpPct = hp, atkPct = atk, defPct = def, spd = spd } : null;
        }

        // hiệu ứng đầu trận của tiềm năng, bộ và đặc tính hệ của huy hiệu; null nếu không có
        public static BattleStart Start(SaveData s, GameData d, string hero)
        {
            var t = Final(d.Cfg, s.Hero(hero).potential);
            var h = d.Hero(hero);
            if (h != null)
            {
                var tr = Badges.Trait(s, d.Cfg, h.elem);
                if (tr != null) t[(int)tr.Value.k] += tr.Value.v;
            }
            var st = new BattleStart
            {
                mana = t[(int)PotKind.Mana], rage = t[(int)PotKind.Rage], crit = t[(int)PotKind.Crit], lifesteal = t[(int)PotKind.Lifesteal],
                shield = t[(int)PotKind.Shield], guard = t[(int)PotKind.Guard], dodge = t[(int)PotKind.Dodge],
            };
            return st.mana != 0 || st.rage != 0 || st.crit != 0 || st.lifesteal != 0 || st.shield != 0 || st.guard != 0 || st.dodge != 0 ? st : null;
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

        // tầng đã mở: tầng 0, và tầng ngay sau tầng cao nhất đã qua (s.caveFloor = số tầng đã qua lần đầu)
        public static bool CaveUnlocked(SaveData s, BalanceConfig cfg, int tier) => tier >= 0 && tier < cfg.cave.tiers.Count && tier <= s.caveFloor;

        public static bool CaveFirst(SaveData s, int tier) => tier >= s.caveFloor;

        // vào được tầng: đã mở và (còn lượt thắng hôm nay, hoặc chưa qua lần đầu)
        public static bool CaveCanEnter(SaveData s, BalanceConfig cfg, int day, int tier) =>
            CaveUnlocked(s, cfg, tier) && (CaveLeft(s, cfg, day) > 0 || CaveFirst(s, tier));

        // trận của tầng: 1 boss và 1 tướng phụ cùng hệ (tướng theo vòng trong danh sách tướng của hệ). Địch quy về sức tướng Khá như
        // đảo 70 ải (buff = hệ số độ hiếm × (1 + buff của tầng) − 1), để độ khó các tầng không lệch theo tướng hiếm của hệ
        public static StageDef CaveStage(GameData d, Elem z, int tier)
        {
            var t = d.Cfg.cave.tiers[tier];
            var hs = d.Heroes.Where(h => h.elem == z).ToList();
            var st = new StageDef { id = 2000 + d.Zone(z).order * 10 + tier, zone = z, idx = tier + 1, name = $"Hang {t.name}", kind = StageKind.Boss };
            string boss = hs[tier % hs.Count].id, mate = hs[(tier + 1) % hs.Count].id;
            st.enemies.Add(new StageEnemy { hero = boss, level = t.level, boss = true, buff = Badges.NormBuff(d, boss, t.buff) });
            st.enemies.Add(new StageEnemy { hero = mate, level = Math.Max(1, t.level - 2), boss = false, buff = Badges.NormBuff(d, mate, t.buff) });
            return st;
        }

        // thắng tầng: lần đầu thì thưởng lần đầu và mở tầng sau (không cần lượt); còn lượt thì đá của tầng, trừ một lượt, lượt đầu
        // trong ngày ở tầng cao cho thêm đá tinh
        public static CaveWin WinCave(SaveData s, BalanceConfig cfg, int day, int tier)
        {
            var r = new CaveWin();
            var t = cfg.cave.tiers[tier];
            if (CaveFirst(s, tier) && CaveUnlocked(s, cfg, tier))
            {
                r.first = true;
                s.caveFloor = tier + 1;
                r.firstStones = t.firstStones;
                r.crystals += t.firstCrystals;
                r.evo = t.firstEvo;
            }
            if (CaveLeft(s, cfg, day) > 0)
            {
                var c = CaveOf(s, day);
                if (c.wins == 0 && tier + 1 >= cfg.cave.crystalFloor) r.crystals += cfg.cave.crystalDaily;
                c.wins++;
                r.stones = t.stones;
            }
            s.potentialStones += r.stones + r.firstStones;
            s.potentialCrystals += r.crystals;
            s.evoStones += r.evo;
            return r;
        }
    }
}
