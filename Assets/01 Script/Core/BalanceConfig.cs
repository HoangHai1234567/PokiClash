// Mọi con số cân bằng ở một chỗ, nạp từ Assets/02 Data/Json/balance.json (xuất từ CFG và hằng số
// tiến trình của bản web). Sửa số thì sửa ở web rồi xuất lại; không sửa tay trong Unity.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    [Serializable]
    public class XStep
    {
        public int x;
        public int lv;
    }

    [Serializable]
    public class RarityWeight
    {
        public Rarity rarity;
        public double w;
    }

    // một dòng của bảng rương máy bi: trọng số, loại thưởng (balls, exp, cards, shards), khoảng số, tỉ trọng độ hiếm của thẻ
    [Serializable]
    public class ChestRoll
    {
        public double w;
        public string k;
        public int min, max;
        public List<RarityWeight> rar = new List<RarityWeight>();
    }

    [Serializable]
    public class ChestTable
    {
        public string kind; // chest_wood, chest_silver, chest_gold
        public List<ChestRoll> rolls = new List<ChestRoll>();
    }

    // AFK: mảnh, rương AFK (3 giờ/rương, khay 4, đếm 2 giờ), tăng tốc ×2 trong 2 giờ. Bi thụ động đến từ cây bi (TreesConfig).
    [Serializable]
    public class AfkConfig
    {
        public double shardChance = 0.08;
        public double chestEveryH = 3, chestOpenH = 2, boostH = 2, boostMult = 2;
        public int chestSlots = 4;
        public ChestTable chest = new ChestTable { kind = "chest_afk" };
    }

    // Tiềm năng và Hang Tiềm Năng (Web/src/core/data/potential.ts); mảng theo PotKind (atk, def, hp, spd, crit, lifesteal, mana, rage).
    // Mảng phẳng (Unity không lưu được mảng lồng trong ScriptableObject).
    [Serializable]
    public class PotentialConfig
    {
        public double[] values = new double[8 * 5]; // values[loại * 5 + độ hiếm]
        public double Val(int kind, int rarity) => values[kind * 5 + rarity];
        public double[] rarityWeight = { 55, 28, 12, 4.5, 0.5 };
        public double[] caps = new double[8];
        public int[] slotStar = { 1, 2, 3, 4 };
        public int lockCost = 2, maxLocks = 2;
    }

    [Serializable]
    public class CaveTier
    {
        public string name;
        public int level, stones;
    }

    [Serializable]
    public class CaveConfig
    {
        public List<CaveTier> tiers = new List<CaveTier>();
        public int winsPerDay = 3, adExtra = 1;
        public int[] weekday = { -1, -1, -1, -1, -1, -1, -1 }; // hệ boss theo thứ (0 = Chủ nhật), số của Elem; −1 = người chơi chọn
        public Elem? Weekday(int wd) => weekday[wd] < 0 ? (Elem?)null : (Elem)weekday[wd];
    }

    // Quảng cáo thưởng và gói (Web/src/core/data/ads.ts): giới hạn lượt mỗi ngày theo chỗ đặt (0 = không giới hạn)
    [Serializable]
    public class AdLimit
    {
        public string p;
        public int n;
    }

    [Serializable]
    public class PassConfig
    {
        public int days = 30;
        public double treeMult = 1.5, afkOpenH = 1;
        public int afkSlots = 5;
    }

    [Serializable]
    public class ProductDef
    {
        public string id, name, desc;
    }

    [Serializable]
    public class AdsConfig
    {
        public List<AdLimit> limits = new List<AdLimit>();
        public PassConfig pass = new PassConfig();
        public List<ProductDef> products = new List<ProductDef>();
    }

    // Cây bi (Web/src/core/data/trees.ts): mỗi cây perHour bi/giờ, chứa tối đa cap; cây 1 mở khi qua ải 1, cây sau mở khi qua boss các đảo
    [Serializable]
    public class TreesConfig
    {
        public double perHour = 5, cap = 50;
        public List<Elem> unlockZones = new List<Elem>();
    }

    // Trang trại (Web/src/core/data/farm.ts)
    [Serializable]
    public class FarmSpotDef
    {
        public string id, kind, name;
        public Elem elem;
        public double x, y; // toạ độ 0..1 trên ảnh đảo trang trại
    }

    [Serializable]
    public class FarmConfig
    {
        public int minHeroes = 3;
        public double @base = 1.2;
        public double[] rarityPower = { 1, 1.1, 1.22, 1.36, 1.5 };
        public double lvStep = 0.05, starStep = 0.1, match = 1.25;
        public double durBase = 2, durStar = 0.5, durRarity = 0.5;
        public double restPerHour = 15, restMin = 15, restMax = 60, capHours = 12;
        public int openSpots = 3;
        public int[] spotLevels = { 8, 11, 14, 17, 20 };
        public double boostH = 1, boostMult = 2;
        public List<FarmSpotDef> spots = new List<FarmSpotDef>();
    }

    // Đền Huy Hiệu (Web/src/core/data/badges.ts)
    [Serializable]
    public class BadgeConfig
    {
        public List<string> tiers = new List<string> { "Đồng", "Bạc", "Vàng", "Ngọc", "Kim Cương" };
        public int[] counts = { 5, 5, 10, 10, 10 }; // số trận mỗi bậc
        public double[] bonus = { 0.05, 0.08, 0.12, 0.16, 0.2 }; // phần cộng Máu, Công, Thủ theo bậc cao nhất
        public int levelPerTier = 3, ballsBase = 5, ballsPerTier = 2;
        public double levelPerFight = 0.5; // cấp địch thêm mỗi trận trong bậc
        public List<string> chest = new List<string> { "chest_silver", "chest_silver", "chest_gold", "chest_gold", "chest_gold" };
    }

    // đội mẫu của bảng đo theo đảo (Web/src/core/sim.ts SIM_TEAMS)
    [Serializable]
    public class SimTeam
    {
        public Elem zone;
        public List<string> team = new List<string>();
        public int star = 1, card = 1;
    }

    // tỉ lệ một loại ô của máy bi, đo bằng mô phỏng ở bản web (exp5, exp10, exp15, ball, chest_wood, chest_silver, chest_gold)
    [Serializable]
    public class SlotRate
    {
        public string k;
        public double p;
    }

    [Serializable]
    public class BalanceConfig
    {
        // lượt
        public int picks;
        public int offer;

        // tài nguyên
        public int manaPerTurn;
        public int benchMana;
        public int maxMana;
        public int maxRage;
        public int rageOnAttack;
        public double rageOnHit; // nộ nhận thêm = phần máu mất / máu tối đa × số này

        // sát thương
        public double critBase;
        public double critMult;
        public double defK; // sát thương × defK / (defK + thủ)
        public double dmgVar;
        public double shieldCap; // khiên tối đa so với máu tối đa

        // chỉ số tướng theo cấp và sao
        public double hpBase;
        public double atkBase;
        public double defBase;
        public double lvStep;
        public double starStep;
        public double bossHp;
        public double bossAtk;
        // boss ải 8 (thẻ Tiến Hóa, dòng n dạng): máu các dạng cộng lại bằng bossEvoHp lần máu boss, chia theo tỉ lệ 1 : 2 : … : n;
        // Công dạng cuối đủ, mỗi dạng trước kém bossEvoAtk
        public double bossEvoHp;
        public double bossEvoAtk;
        public double cardLvStep; // mỗi cấp thẻ tăng số của thẻ thêm 15 %
        public int maxRounds; // giới hạn an toàn số hiệp của một trận

        // tiến trình (progression.ts)
        public int saveVersion;
        public int maxLevel;
        public double expBase = 40, expPow = 1.35; // EXP lên cấp sau = expBase × cấp^expPow
        public double afkCapH;
        public int legendMilestone;
        public int cardMax;
        public int maxStar;
        public List<XStep> xSteps = new List<XStep>();
        public int[] cardReq = new int[0]; // bản sao để lên cấp lv -> lv+1
        public int[] starCards = new int[0]; // tổng cấp 3 thẻ để lên sao n
        public int[] starLevel = new int[0]; // cấp người chơi để lên sao n
        public int[] formStars = new int[0]; // sao đổi sang dạng 2, dạng 3 của dòng tiến hóa

        public HeroForm FormOf(HeroDef h, int star) => h.Form(formStars, star);

        // tỉ trọng rút thẻ chung theo độ hiếm (thường..huyền thoại)
        public double[] poolWeight = new double[5];

        // máy bi: giới hạn mỗi đợt theo cấp, bản sao khi mốc Huyền thoại đã có tướng, bảng rương
        public int maxPerDrop = 20, maxPerDropHigh = 30, maxPerDropLevel = 15, legendCopies = 15;
        public List<ChestTable> chests = new List<ChestTable>();
        public int ratesBalls; // số bi của lần mô phỏng đo tỉ lệ
        public List<SlotRate> rates = new List<SlotRate>();

        public double Rate(string kind) => rates.Find(r => r.k == kind)?.p ?? 0;

        public AfkConfig afk = new AfkConfig();
        public List<SimTeam> simTeams = new List<SimTeam>();
        public BadgeConfig badges = new BadgeConfig();
        public PotentialConfig potential = new PotentialConfig();
        public CaveConfig cave = new CaveConfig();
        public FarmConfig farm = new FarmConfig();
        public AdsConfig ads = new AdsConfig();
        public TreesConfig trees = new TreesConfig();

        public SimTeam SimTeamOf(Elem z) => simTeams.Find(t => t.zone == z);

        public int MaxPerDrop(int level) => level >= maxPerDropLevel ? maxPerDropHigh : maxPerDrop;

        public ChestTable Chest(string kind) => chests.Find(c => c.kind == kind);

        public double PoolWeight(Rarity r) => poolWeight[(int)r];

        public BalanceConfig Clone()
        {
            var c = (BalanceConfig)MemberwiseClone();
            c.xSteps = new List<XStep>(xSteps);
            c.cardReq = (int[])cardReq.Clone();
            c.starCards = (int[])starCards.Clone();
            c.starLevel = (int[])starLevel.Clone();
            c.formStars = (int[])formStars.Clone();
            c.poolWeight = (double[])poolWeight.Clone();
            c.chests = new List<ChestTable>(chests);
            c.rates = new List<SlotRate>(rates);
            return c;
        }

        public static BalanceConfig FromJson(Dictionary<string, object> root)
        {
            var o = J.Obj(root, "cfg");
            var p = J.Obj(root, "progression");
            var c = new BalanceConfig
            {
                picks = J.Int(o, "picks"),
                offer = J.Int(o, "offer"),
                manaPerTurn = J.Int(o, "manaPerTurn"),
                benchMana = J.Int(o, "benchMana"),
                maxMana = J.Int(o, "maxMana"),
                maxRage = J.Int(o, "maxRage"),
                rageOnAttack = J.Int(o, "rageOnAttack"),
                rageOnHit = J.Num(o, "rageOnHit"),
                critBase = J.Num(o, "critBase"),
                critMult = J.Num(o, "critMult"),
                defK = J.Num(o, "defK"),
                dmgVar = J.Num(o, "dmgVar"),
                shieldCap = J.Num(o, "shieldCap"),
                hpBase = J.Num(o, "hpBase"),
                atkBase = J.Num(o, "atkBase"),
                defBase = J.Num(o, "defBase"),
                lvStep = J.Num(o, "lvStep"),
                starStep = J.Num(o, "starStep"),
                bossHp = J.Num(o, "bossHp"),
                bossAtk = J.Num(o, "bossAtk"),
                bossEvoHp = J.Num(o, "bossEvoHp"),
                bossEvoAtk = J.Num(o, "bossEvoAtk"),
                cardLvStep = J.Num(o, "cardLvStep"),
                maxRounds = J.Int(o, "maxRounds", 60),
                saveVersion = J.Int(p, "saveVersion"),
                maxLevel = J.Int(p, "maxLevel"), expBase = J.Num(p, "expBase"), expPow = J.Num(p, "expPow"),
                afkCapH = J.Num(p, "afkCapH"),
                legendMilestone = J.Int(p, "legendMilestone"),
                cardMax = J.Int(p, "cardMax"),
                maxStar = J.Int(p, "maxStar"),
                cardReq = Ints(J.Arr(p, "cardReq")),
                starCards = Ints(J.Arr(p, "starCards")),
                starLevel = Ints(J.Arr(p, "starLevel")),
                formStars = Ints(J.Arr(p, "formStars")),
            };
            foreach (var x in J.Arr(p, "xSteps"))
            {
                var xo = J.Obj(x);
                c.xSteps.Add(new XStep { x = J.Int(xo, "x"), lv = J.Int(xo, "lv") });
            }
            var w = J.Obj(root, "poolWeight");
            c.poolWeight = new double[5];
            foreach (Rarity r in Enum.GetValues(typeof(Rarity))) c.poolWeight[(int)r] = J.Num(w, Keys.Of(r));
            var pk = J.Obj(root, "pachinko");
            if (pk != null)
            {
                c.maxPerDrop = J.Int(pk, "maxPerDrop", 20);
                c.maxPerDropHigh = J.Int(pk, "maxPerDropHigh", 30);
                c.maxPerDropLevel = J.Int(pk, "maxPerDropLevel", 15);
                c.legendCopies = J.Int(pk, "legendCopies", 15);
                var chests = J.Obj(pk, "chests");
                if (chests != null)
                    foreach (var kv in chests)
                    {
                        c.chests.Add(new ChestTable { kind = kv.Key, rolls = Rolls(J.Arr(kv.Value)) });
                    }
                var m = J.Obj(pk, "measured");
                c.ratesBalls = J.Int(m, "balls");
                var rates = J.Obj(m, "rates");
                if (rates != null)
                    foreach (var kv in rates) c.rates.Add(new SlotRate { k = kv.Key, p = (double)kv.Value });
            }
            var tr = J.Obj(root, "trees");
            if (tr != null)
            {
                c.trees = new TreesConfig { perHour = J.Num(tr, "perHour"), cap = J.Num(tr, "cap") };
                foreach (var z in J.Arr(tr, "unlockZones")) c.trees.unlockZones.Add(Keys.ToElem((string)z));
            }
            var adc = J.Obj(root, "ads");
            if (adc != null)
            {
                c.ads = new AdsConfig();
                foreach (var kv in J.Obj(adc, "limits") ?? new Dictionary<string, object>()) c.ads.limits.Add(new AdLimit { p = kv.Key, n = (int)(double)kv.Value });
                var ps = J.Obj(adc, "pass");
                c.ads.pass = new PassConfig { days = J.Int(ps, "days"), treeMult = J.Num(ps, "treeMult"), afkSlots = J.Int(ps, "afkSlots"), afkOpenH = J.Num(ps, "afkOpenH") };
                foreach (var x in J.Arr(adc, "products"))
                {
                    var po = J.Obj(x);
                    c.ads.products.Add(new ProductDef { id = J.Str(po, "id"), name = J.Str(po, "name"), desc = J.Str(po, "desc") });
                }
            }
            var fm = J.Obj(root, "farm");
            if (fm != null)
            {
                c.farm = new FarmConfig
                {
                    minHeroes = J.Int(fm, "minHeroes"), @base = J.Num(fm, "base"),
                    rarityPower = J.Arr(fm, "rarityPower").Select(x => (double)x).ToArray(),
                    lvStep = J.Num(fm, "lvStep"), starStep = J.Num(fm, "starStep"), match = J.Num(fm, "match"),
                    durBase = J.Num(fm, "durBase"), durStar = J.Num(fm, "durStar"), durRarity = J.Num(fm, "durRarity"),
                    restPerHour = J.Num(fm, "restPerHour"), restMin = J.Num(fm, "restMin"), restMax = J.Num(fm, "restMax"), capHours = J.Num(fm, "capHours"),
                    openSpots = J.Int(fm, "openSpots"), spotLevels = Ints(J.Arr(fm, "spotLevels")),
                    boostH = J.Num(fm, "boostH"), boostMult = J.Num(fm, "boostMult"),
                };
                foreach (var x in J.Arr(fm, "spots"))
                {
                    var o2 = J.Obj(x);
                    c.farm.spots.Add(new FarmSpotDef
                    {
                        id = J.Str(o2, "id"), kind = J.Str(o2, "kind"), name = J.Str(o2, "name"), elem = Keys.ToElem(J.Str(o2, "elem")),
                        x = J.Num(o2, "x"), y = J.Num(o2, "y"),
                    });
                }
            }
            var pt = J.Obj(root, "potential");
            if (pt != null)
            {
                var vals = J.Obj(pt, "values");
                var caps = J.Obj(pt, "caps");
                c.potential = new PotentialConfig
                {
                    rarityWeight = J.Arr(pt, "rarityWeight").Select(x => (double)x).ToArray(),
                    slotStar = Ints(J.Arr(pt, "slotStar")),
                    lockCost = J.Int(pt, "lockCost"), maxLocks = J.Int(pt, "maxLocks"),
                };
                for (int i = 0; i < Potential.KindKeys.Length; i++)
                {
                    var row = J.Arr(vals, Potential.KindKeys[i]);
                    for (int r = 0; r < 5 && r < row.Count; r++) c.potential.values[i * 5 + r] = (double)row[r];
                    c.potential.caps[i] = J.Num(caps, Potential.KindKeys[i]);
                }
            }
            var cvc = J.Obj(root, "cave");
            if (cvc != null)
            {
                c.cave = new CaveConfig { winsPerDay = J.Int(cvc, "winsPerDay"), adExtra = J.Int(cvc, "adExtra") };
                foreach (var x in J.Arr(cvc, "tiers"))
                {
                    var t = J.Obj(x);
                    c.cave.tiers.Add(new CaveTier { name = J.Str(t, "name"), level = J.Int(t, "level"), stones = J.Int(t, "stones") });
                }
                var wd = J.Arr(cvc, "weekday");
                for (int i = 0; i < 7 && i < wd.Count; i++) c.cave.weekday[i] = wd[i] is string e ? (int)Keys.ToElem(e) : -1;
            }
            var bg = J.Obj(root, "badges");
            if (bg != null)
                c.badges = new BadgeConfig
                {
                    tiers = J.Arr(bg, "tiers").OfType<string>().ToList(),
                    counts = Ints(J.Arr(bg, "counts")),
                    bonus = J.Arr(bg, "bonus").Select(x => (double)x).ToArray(),
                    levelPerTier = J.Int(bg, "levelPerTier"), ballsBase = J.Int(bg, "ballsBase"), ballsPerTier = J.Int(bg, "ballsPerTier"),
                    levelPerFight = J.Num(bg, "levelPerFight", 0.5),
                    chest = J.Arr(bg, "chest").OfType<string>().ToList(),
                };
            var stm = J.Obj(root, "simTeams");
            if (stm != null)
                foreach (var kv in stm)
                {
                    var o2 = J.Obj(kv.Value);
                    var t = new SimTeam { zone = Keys.ToElem(kv.Key), star = J.Int(o2, "star", 1), card = J.Int(o2, "card", 1) };
                    foreach (var h in J.Arr(o2, "team")) if (h is string id) t.team.Add(id);
                    c.simTeams.Add(t);
                }
            var af = J.Obj(root, "afk");
            if (af != null)
                c.afk = new AfkConfig
                {
                    shardChance = J.Num(af, "shardChance"),
                    chestEveryH = J.Num(af, "chestEveryH"), chestOpenH = J.Num(af, "chestOpenH"), boostH = J.Num(af, "boostH"), boostMult = J.Num(af, "boostMult"),
                    chestSlots = J.Int(af, "chestSlots"),
                    chest = new ChestTable { kind = "chest_afk", rolls = Rolls(J.Arr(af, "chest")) },
                };
            return c;
        }

        static List<ChestRoll> Rolls(List<object> rows)
        {
            var list = new List<ChestRoll>();
            foreach (var x in rows)
            {
                var ro = J.Obj(x);
                var roll = new ChestRoll { w = J.Num(ro, "w"), k = J.Str(ro, "k"), min = J.Int(ro, "min"), max = J.Int(ro, "max") };
                var rar = J.Obj(ro, "rar");
                if (rar != null)
                    foreach (var rv in rar) roll.rar.Add(new RarityWeight { rarity = Keys.ToRarity(rv.Key), w = (double)rv.Value });
                list.Add(roll);
            }
            return list;
        }

        static int[] Ints(List<object> l)
        {
            var a = new int[l.Count];
            for (int i = 0; i < a.Length; i++) a[i] = l[i] is double d ? (int)d : 0;
            return a;
        }
    }
}
