// Mọi con số cân bằng ở một chỗ, nạp từ Assets/02 Data/Json/balance.json (xuất từ CFG và hằng số
// tiến trình của bản web). Sửa số thì sửa ở web rồi xuất lại; không sửa tay trong Unity.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    // mức cược ×x của máy bi mở khi đang có ít nhất `balls` bi (như máy tham khảo: có nhiều bi thì được thả nhanh hơn)
    [Serializable]
    public class XStep
    {
        public int x;
        public int balls;
    }

    // một mốc quà của máy bi: tiêu đủ n bi (tính theo cược) thì nhận k (chest_wood, chest_silver, chest_gold; balls, exp với số v)
    [Serializable]
    public class GiftStep
    {
        public int n;
        public string k;
        public int v;
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
        public string k; // balls, exp, cards, stones, evo, shards, egg (trứng capsule bậc tier vào túi, 2026-11-23)
        public int min, max;
        public int tier; // egg: bậc trứng 0..4
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
        public double[] values = new double[Potential.KindCount * 5]; // values[loại * 5 + độ hiếm]
        public double Val(int kind, int rarity) => values[kind * 5 + rarity];
        public double[] rarityWeight = { 55, 28, 12, 4.5, 0.5 };
        public double[] crystalWeight = { 0, 0, 80, 18, 2 }; // khai phá bằng đá tinh: mọi ô từ Hiếm trở lên (2026-11-17)
        public double[] kindWeight = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 }; // trọng số quay theo loại (0 = không ra nữa, dòng cũ vẫn tính)
        public double[] caps = new double[Potential.KindCount];
        public int[] slotStar = { 1, 3, 6, 8, 11, 16 }; // sao tổng (StarTier) mở từng ô
        public int lockCost = 2, maxLocks = 3;
        public List<PotSet> sets = new List<PotSet>(); // bộ: đủ need[lv] dòng cùng nhóm thì có phần thưởng bộ cấp lv
    }

    // Một bộ tiềm năng (2026-11-17): nhóm loại dòng; có need[0] dòng thuộc nhóm thì nhận phần thưởng cấp 1, need[1] dòng thì cấp 2.
    // Phần thưởng: bonusKind[j] (khoá loại dòng) cộng bonus[lv * bonusKind.Length + j] (không tính vào trần của loại). Mảng phẳng để
    // ScriptableObject giữ được.
    [Serializable]
    public class PotSet
    {
        public string key, name;
        public string Name => Loc.T(name); // tên theo ngôn ngữ
        public string[] kinds = new string[0];
        public int[] need = new int[0];
        public string[] bonusKind = new string[0];
        public double[] bonus = new double[0];
    }

    // Một tầng Hang Tiềm Năng: cấp, đá mỗi lượt thắng; thưởng lần đầu qua (đá tiềm năng, đá tinh, đá tiến hóa); buff: độ khó thêm
    [Serializable]
    public class CaveTier
    {
        public string name;
        public string Name => Loc.T(name);
        public int level, stones;
        public int firstStones, firstCrystals, firstEvo;
        public double buff;
    }

    [Serializable]
    public class CaveConfig
    {
        public List<CaveTier> tiers = new List<CaveTier>();
        public int winsPerDay = 3, adExtra = 1;
        public int[] weekday = { -1, -1, -1, -1, -1, -1, -1 }; // hệ boss theo thứ (0 = Chủ nhật), số của Elem; −1 = người chơi chọn
        public Elem? Weekday(int wd) => weekday[wd] < 0 ? (Elem?)null : (Elem)weekday[wd];
        public int crystalFloor = 8; // lượt thắng đầu tiên mỗi ngày ở tầng này trở lên (đếm từ 1) cho thêm crystalDaily đá tinh
        public int crystalDaily = 1;
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
        public string Name => Loc.T(name);
        public string Desc => Loc.T(desc);
    }

    [Serializable]
    public class AdsConfig
    {
        public List<AdLimit> limits = new List<AdLimit>();
        public PassConfig pass = new PassConfig();
        public List<ProductDef> products = new List<ProductDef>();
        // Bỏ quảng cáo: số lượt trao ngay mỗi ngày, các lượt sau vẫn xem được như thường (0: không giới hạn). Trước 2026-11-26 không
        // giới hạn: gói 4,99 USD thành khoảng 20 lượt, +1.500 bi mỗi ngày mãi mãi (GD_Claude/33 mục 2.4)
        public int noAdsInstant = 8;
    }

    // Cây bi (Web/src/core/data/trees.ts): mỗi cây perHour bi/giờ, chứa tối đa cap; cây 1 mở khi qua ải 1, cây sau mở theo cấp người
    // chơi (unlockLevels; 5 đảo chơi song song nên từ 2026-11-05 không mở theo boss từng đảo nữa, cấp 40/80/120/160 là lúc trước kia
    // xong Thủy, Hỏa, Kim, Mộc)
    [Serializable]
    public class TreesConfig
    {
        public double perHour = 5, cap = 50;
        // túi bi (BallBag, 2026-11-27): trần bi nhận từ nguồn tự sinh ở Nhà = ballCap + ballCapPerTree × (số cây mở − 1)
        public int ballCap = 400, ballCapPerTree = 100;
        public List<int> unlockLevels = new List<int>();
    }

    // bi thắng ải (Progress.StageBalls, đưa vào cấu hình 2026-11-24 để cân bằng): ải 1 của đảo @base bi, cứ step ải thêm 1 bi
    // (thang 70 ải); lần đầu qua ải boss, mini boss, ải tướng thêm boss, mini, hero bi
    [Serializable]
    public class StageBallsConfig
    {
        public int @base = 1, step = 14, boss = 8, mini = 4, hero = 2;
        // đánh lại ải đã qua: replayFull trận đầu mỗi ngày nhận đủ bi, các trận sau nhận replayPct (GD_Claude/33 việc 13); 0: không giới hạn
        public int replayFull = 10;
        public double replayPct = 0.25;
    }

    // Trang trại (Web/src/core/data/farm.ts)
    [Serializable]
    public class FarmSpotDef
    {
        public string id, kind, name;
        public string Name => Loc.T(name);
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

    // mốc sao của Đền Huy Hiệu (2026-11-17): rương (chest_silver, chest_gold), đá tiến hóa, đá tinh, đá tiềm năng
    [Serializable]
    public class BadgeGift
    {
        public string chest;
        public int evo, crystal, stones;
    }

    // Đền Huy Hiệu (Web/src/core/data/badges.ts; 2026-11-17 thêm bậc 6–10, sao từng trận, mốc sao, đặc tính hệ, phần cộng cả đội)
    [Serializable]
    public class BadgeConfig
    {
        public List<string> tiers = new List<string> { "Đồng", "Bạc", "Vàng", "Ngọc", "Kim Cương" };
        public int[] counts = { 5, 5, 10, 10, 10 }; // số trận mỗi bậc
        public double[] bonus = { 0.05, 0.08, 0.12, 0.16, 0.2 }; // phần cộng Máu, Công, Thủ theo bậc cao nhất
        public double[] teamBonus = new double[0]; // phần cộng Máu, Công, Thủ cho mọi tướng theo bậc của từng dãy (cộng 5 dãy)
        public int levelPerTier = 3, ballsBase = 5, ballsPerTier = 2;
        public double levelPerFight = 0.5; // cấp địch thêm mỗi trận trong bậc
        public List<string> chest = new List<string> { "chest_silver", "chest_silver", "chest_gold", "chest_gold", "chest_gold" };
        public int[] evo = new int[0]; // đá tiến hóa khi xong bậc
        public int[] crystal = new int[0]; // đá tinh khi xong bậc
        // độ khó: địch quy về sức tướng Khá (như đảo 70 ải), nhân 1 + foeBuff + foeTierBuff·(bậc − 1), trận cuối bậc thêm foeLastBuff
        public double foeBuff, foeTierBuff, foeLastBuff;
        public int starRounds = 2; // sao 3: thắng trong starRounds hiệp mỗi địch (sao 1: thắng; sao 2: không tướng nào gục)
        public int giftEvery = 30; // mỗi giftEvery sao (tổng cả đền) một mốc; quà theo vòng gifts
        public List<BadgeGift> gifts = new List<BadgeGift>();
        // đặc tính hệ: mở và nâng ở các bậc traitTiers; loại theo hệ (khoá loại dòng tiềm năng, theo thứ tự Elem), số theo
        // traitValue[hệ * traitTiers.Length + nấc]
        public int[] traitTiers = new int[0];
        public string[] traitKind = new string[0];
        public string[] traitName = new string[0];
        public double[] traitValue = new double[0];
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
        // 2026-11-17: dạng chưa cuối tiến hóa khi gục (trước: dưới 25% máu), máu các dạng chưa cuối nhân thêm số này (0,75) để tổng
        // máu phải đánh như cũ (Battle.EvoMult)
        public double bossEvoEarly = 1;
        public double cardLvStep; // mỗi cấp thẻ tăng số của thẻ thêm 15 %
        public int maxRounds; // giới hạn an toàn số hiệp của một trận

        // tiến trình (progression.ts)
        public int saveVersion;
        public int maxLevel;
        public double expBase = 40, expPow = 1.35; // EXP lên cấp sau = expBase × cấp^expPow
        // đoạn sau của đường EXP (2026-11-26, GD_Claude/34 mục 1): EXP lên cấp = max(expBase × cấp^expPow, expLateBase × cấp^expLatePow).
        // Với 45 × cấp và 9 × cấp^1,54 hai đường cắt nhau ở khoảng cấp 20: đầu game y như cũ (hướng dẫn người mới không đổi), cấp 100
        // tốn gấp 2,4, cấp 200 gấp 3,5. Để mỗi cấp đủ đắt cho tường thiếu cấp có nghĩa và gói bi có lý do. expLateBase 0: tắt
        public double expLateBase, expLatePow = 1;
        public double afkCapH;
        public int legendMilestone;
        public int cardMax;
        public int maxStar;
        public List<XStep> xSteps = new List<XStep>();
        public int[] cardReq = new int[0]; // bản sao để lên cấp lv -> lv+1
        public int[] formStars = new int[0]; // sao (tổng) đổi sang dạng 2, dạng 3 của dòng tiến hóa: 6, 11 (Bạc 1★, Vàng 1★)
        // bậc sao (2026-11-17, StarTier, GD_Claude/20_TangDayNoiDung.md; thay starCards / starLevel: tổng cấp thẻ và cấp người chơi):
        public double[] tierPower = new double[0]; // hệ số chỉ số của bậc Đồng, Bạc, Vàng, Kim Cương (HeroStats.StarMult)
        public int[] shardCost = new int[0]; // mảnh lên sao trong bậc của tướng Khá: 4 số mỗi bậc (lên 2★, 3★, 4★, 5★), Đồng → Kim Cương
        public double[] shardRarity = new double[0]; // nhân giá mảnh theo độ hiếm (Thường..Huyền thoại)
        public int[] evoStones = new int[0]; // đá tiến hóa lên Bạc, Vàng, Kim Cương
        public double[] evoRarity = new double[0]; // nhân giá đá theo độ hiếm (trống = như nhau)
        public int[] evoLevel = new int[0]; // cấp người chơi tối thiểu để tiến hóa lên Bạc, Vàng, Kim Cương
        public int[] evoFirst = new int[0]; // đá lần đầu qua ải tướng, mini boss, boss cuối đảo
        public double evoReplayMini, evoReplayBoss; // tỉ lệ ra 1 đá khi qua lại mini boss, boss cuối đảo
        public int[] evoChest = new int[0]; // đá trong rương mốc đảo 70 ải, theo thứ tự rương (rương cuối là rương chinh phục)

        public HeroForm FormOf(HeroDef h, int star) => h.Form(formStars, star);

        // tỉ trọng rút thẻ chung theo độ hiếm (thường..huyền thoại)
        public double[] poolWeight = new double[5];

        // máy bi: giới hạn mỗi đợt theo cấp, bản sao khi mốc Huyền thoại đã có tướng, bảng rương
        public int maxPerDrop = 20, maxPerDropHigh = 30, maxPerDropLevel = 15, legendCopies = 15;
        public List<ChestTable> chests = new List<ChestTable>();
        public List<GiftStep> gifts = new List<GiftStep>(); // mốc quà sau mốc Huyền thoại, hết thì vòng lại từ đầu
        // bảng tỉ lệ kết quả (%), theo thứ tự ô đáy trái sang phải (Board.SlotLayout) rồi cốc dưới mái: máy chọn kết quả theo bảng
        // này rồi phát đường bi vật lý rơi đúng chỗ (Board.odds)
        public double[] odds = new double[0];
        public List<GiftStep> rings = new List<GiftStep>(); // vòng nấm trái, phải: đủ n lần chạm (×cược) ra quà
        public int ratesBalls; // số bi của lần mô phỏng đo số lần chạm nấm
        public double[] ringHits = new double[0]; // số lần chạm mỗi nấm trung bình mỗi bi (đo bằng mô phỏng)
        public List<SlotRate> rates = new List<SlotRate>(); // tỉ lệ theo loại ô, tính từ odds lúc đọc

        public double Rate(string kind) => rates.Find(r => r.k == kind)?.p ?? 0;

        public AfkConfig afk = new AfkConfig();
        public List<SimTeam> simTeams = new List<SimTeam>();
        public BadgeConfig badges = new BadgeConfig();
        public PotentialConfig potential = new PotentialConfig();
        public CaveConfig cave = new CaveConfig();
        public FarmConfig farm = new FarmConfig();
        public AdsConfig ads = new AdsConfig();
        public TreesConfig trees = new TreesConfig();
        public StageBallsConfig stageBalls = new StageBallsConfig();
        public SoPhepConfig sophep = new SoPhepConfig(); // Sổ Phép (Core/SoPhep.cs, GD_Claude/28_SoPhep.md)
        public HomeConfig home = new HomeConfig(); // Nhà (2026-11-18, HomeConfig.cs)
        public ShopConfig shop = new ShopConfig(); // cửa hàng, ưu đãi (2026-11-23, ShopConfig.cs)
        public CasinoConfig casino = new CasinoConfig(); // đảo Casino (2026-11-25, CasinoConfig.cs, GD_Claude/29_DaoCasino.md)

        public SimTeam SimTeamOf(Elem z) => simTeams.Find(t => t.zone == z);

        public int MaxPerDrop(int level) => level >= maxPerDropLevel ? maxPerDropHigh : maxPerDrop;

        public ChestTable Chest(string kind) => chests.Find(c => c.kind == kind);

        public double PoolWeight(Rarity r) => poolWeight[(int)r];

        public BalanceConfig Clone()
        {
            var c = (BalanceConfig)MemberwiseClone();
            c.xSteps = new List<XStep>(xSteps);
            c.cardReq = (int[])cardReq.Clone();
            c.formStars = (int[])formStars.Clone();
            c.tierPower = (double[])tierPower.Clone();
            c.shardCost = (int[])shardCost.Clone();
            c.shardRarity = (double[])shardRarity.Clone();
            c.evoStones = (int[])evoStones.Clone();
            c.evoRarity = (double[])evoRarity.Clone();
            c.evoLevel = (int[])evoLevel.Clone();
            c.evoFirst = (int[])evoFirst.Clone();
            c.evoChest = (int[])evoChest.Clone();
            c.poolWeight = (double[])poolWeight.Clone();
            c.chests = new List<ChestTable>(chests);
            c.gifts = new List<GiftStep>(gifts);
            c.rates = new List<SlotRate>(rates);
            c.odds = (double[])odds.Clone();
            c.rings = new List<GiftStep>(rings);
            c.ringHits = (double[])ringHits.Clone();
            return c;
        }

        // tỉ lệ theo loại ô từ bảng tỉ lệ kết quả (ô đáy theo Board.SlotLayout, rồi cốc)
        public static List<SlotRate> OddsRates(double[] odds)
        {
            var list = new List<SlotRate>();
            double sum = odds.Sum();
            if (sum <= 0) return list;
            for (int i = 0; i < odds.Length; i++)
            {
                var kind = i < Board.SlotLayout.Length ? Board.SlotLayout[i] : Board.GiftReward;
                string k = Pachinko.Key(kind);
                var r = list.Find(q => q.k == k);
                if (r == null) list.Add(r = new SlotRate { k = k });
                r.p = Math.Round(r.p + odds[i] / sum, 6);
            }
            return list;
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
                bossEvoEarly = J.Num(o, "bossEvoEarly", 1),
                cardLvStep = J.Num(o, "cardLvStep"),
                maxRounds = J.Int(o, "maxRounds", 60),
                saveVersion = J.Int(p, "saveVersion"),
                maxLevel = J.Int(p, "maxLevel"), expBase = J.Num(p, "expBase"), expPow = J.Num(p, "expPow"), expLateBase = J.Num(p, "expLateBase"), expLatePow = J.Num(p, "expLatePow", 1),
                afkCapH = J.Num(p, "afkCapH"),
                legendMilestone = J.Int(p, "legendMilestone"),
                cardMax = J.Int(p, "cardMax"),
                maxStar = J.Int(p, "maxStar"),
                cardReq = Ints(J.Arr(p, "cardReq")),
                formStars = Ints(J.Arr(p, "formStars")),
                tierPower = Nums(J.Arr(p, "tierPower")),
                shardCost = Ints(J.Arr(p, "shardCost")),
                shardRarity = Nums(J.Arr(p, "shardRarity")),
                evoStones = Ints(J.Arr(p, "evoStones")),
                evoRarity = Nums(J.Arr(p, "evoRarity")),
                evoLevel = Ints(J.Arr(p, "evoLevel")),
                evoFirst = Ints(J.Arr(p, "evoFirst")),
                evoReplayMini = J.Num(p, "evoReplayMini"),
                evoReplayBoss = J.Num(p, "evoReplayBoss"),
                evoChest = Ints(J.Arr(p, "evoChest")),
            };
            foreach (var x in J.Arr(p, "xSteps"))
            {
                var xo = J.Obj(x);
                c.xSteps.Add(new XStep { x = J.Int(xo, "x"), balls = J.Int(xo, "balls") });
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
                foreach (var g in J.Arr(pk, "gifts"))
                {
                    var go = J.Obj(g);
                    c.gifts.Add(new GiftStep { n = J.Int(go, "n"), k = J.Str(go, "k"), v = J.Int(go, "v") });
                }
                foreach (var g in J.Arr(pk, "rings"))
                {
                    var go = J.Obj(g);
                    c.rings.Add(new GiftStep { n = J.Int(go, "n"), k = J.Str(go, "k"), v = J.Int(go, "v") });
                }
                c.odds = J.Arr(pk, "odds").Select(x => (double)x).ToArray();
                c.rates = OddsRates(c.odds);
                var m = J.Obj(pk, "measured");
                c.ratesBalls = J.Int(m, "balls");
                c.ringHits = J.Arr(m, "ringHits").Select(x => (double)x).ToArray();
            }
            var tr = J.Obj(root, "trees");
            if (tr != null)
            {
                c.trees = new TreesConfig
                {
                    perHour = J.Num(tr, "perHour"), cap = J.Num(tr, "cap"), ballCap = (int)J.Num(tr, "ballCap", 400), ballCapPerTree = (int)J.Num(tr, "ballCapPerTree", 100),
                };
                foreach (var lv in J.Arr(tr, "unlockLevels")) c.trees.unlockLevels.Add((int)(double)lv);
            }
            var sb = J.Obj(root, "stageBalls");
            if (sb != null)
                c.stageBalls = new StageBallsConfig
                {
                    @base = J.Int(sb, "base"), step = Math.Max(1, J.Int(sb, "step")), boss = J.Int(sb, "boss"), mini = J.Int(sb, "mini"),
                    hero = J.Int(sb, "hero"), replayFull = J.Int(sb, "replayFull", 10), replayPct = J.Num(sb, "replayPct", 0.25),
                };
            if (J.Obj(root, "sophep") is Dictionary<string, object> spo) c.sophep = SoPhepConfig.Parse(spo);
            var adc = J.Obj(root, "ads");
            if (adc != null)
            {
                c.ads = new AdsConfig();
                c.ads.noAdsInstant = J.Int(adc, "noAdsInstant", c.ads.noAdsInstant);
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
                var kw = J.Obj(pt, "kindWeight");
                c.potential = new PotentialConfig
                {
                    rarityWeight = J.Arr(pt, "rarityWeight").Select(x => (double)x).ToArray(),
                    slotStar = Ints(J.Arr(pt, "slotStar")),
                    lockCost = J.Int(pt, "lockCost"), maxLocks = J.Int(pt, "maxLocks"),
                };
                var cw = J.Arr(pt, "crystalWeight");
                if (cw.Count > 0) c.potential.crystalWeight = cw.Select(x => (double)x).ToArray();
                for (int i = 0; i < Potential.KindKeys.Length; i++)
                {
                    var row = J.Arr(vals, Potential.KindKeys[i]);
                    for (int r = 0; r < 5 && r < row.Count; r++) c.potential.values[i * 5 + r] = (double)row[r];
                    c.potential.caps[i] = J.Num(caps, Potential.KindKeys[i]);
                    // loại chưa có trong bảng dòng thì không quay ra
                    c.potential.kindWeight[i] = row.Count == 0 ? 0 : J.Num(kw, Potential.KindKeys[i], 1);
                }
                foreach (var x in J.Arr(pt, "sets"))
                {
                    var so = J.Obj(x);
                    var set = new PotSet
                    {
                        key = J.Str(so, "key"), name = J.Str(so, "name"),
                        kinds = J.Arr(so, "kinds").OfType<string>().ToArray(), need = Ints(J.Arr(so, "need")),
                    };
                    var bonus = J.Arr(so, "bonus"); // [{k, v: [cấp 1, cấp 2]}]
                    set.bonusKind = bonus.Select(b => J.Str(J.Obj(b), "k")).ToArray();
                    set.bonus = new double[set.need.Length * set.bonusKind.Length];
                    for (int j = 0; j < bonus.Count; j++)
                    {
                        var v = J.Arr(J.Obj(bonus[j]), "v");
                        for (int lv = 0; lv < set.need.Length && lv < v.Count; lv++) set.bonus[lv * set.bonusKind.Length + j] = (double)v[lv];
                    }
                    c.potential.sets.Add(set);
                }
            }
            var cvc = J.Obj(root, "cave");
            if (cvc != null)
            {
                c.cave = new CaveConfig
                {
                    winsPerDay = J.Int(cvc, "winsPerDay"), adExtra = J.Int(cvc, "adExtra"),
                    crystalFloor = J.Int(cvc, "crystalFloor", 99), crystalDaily = J.Int(cvc, "crystalDaily"),
                };
                foreach (var x in J.Arr(cvc, "tiers"))
                {
                    var t = J.Obj(x);
                    c.cave.tiers.Add(new CaveTier
                    {
                        name = J.Str(t, "name"), level = J.Int(t, "level"), stones = J.Int(t, "stones"),
                        firstStones = J.Int(t, "firstStones"), firstCrystals = J.Int(t, "firstCrystals"), firstEvo = J.Int(t, "firstEvo"),
                        buff = J.Num(t, "buff"),
                    });
                }
                var wd = J.Arr(cvc, "weekday");
                for (int i = 0; i < 7 && i < wd.Count; i++) c.cave.weekday[i] = wd[i] is string e ? (int)Keys.ToElem(e) : -1;
            }
            var bg = J.Obj(root, "badges");
            if (bg != null)
            {
                c.badges = new BadgeConfig
                {
                    tiers = J.Arr(bg, "tiers").OfType<string>().ToList(),
                    counts = Ints(J.Arr(bg, "counts")),
                    bonus = J.Arr(bg, "bonus").Select(x => (double)x).ToArray(),
                    teamBonus = J.Arr(bg, "teamBonus").Select(x => (double)x).ToArray(),
                    levelPerTier = J.Int(bg, "levelPerTier"), ballsBase = J.Int(bg, "ballsBase"), ballsPerTier = J.Int(bg, "ballsPerTier"),
                    levelPerFight = J.Num(bg, "levelPerFight", 0.5),
                    chest = J.Arr(bg, "chest").OfType<string>().ToList(),
                    evo = Ints(J.Arr(bg, "evo")), crystal = Ints(J.Arr(bg, "crystal")),
                    foeBuff = J.Num(bg, "foeBuff"), foeTierBuff = J.Num(bg, "foeTierBuff"), foeLastBuff = J.Num(bg, "foeLastBuff"),
                    starRounds = J.Int(bg, "starRounds", 2), giftEvery = J.Int(bg, "giftEvery", 30),
                };
                foreach (var x in J.Arr(bg, "gifts"))
                {
                    var go = J.Obj(x);
                    c.badges.gifts.Add(new BadgeGift { chest = J.Str(go, "chest"), evo = J.Int(go, "evo"), crystal = J.Int(go, "crystal"), stones = J.Int(go, "stones") });
                }
                var trt = J.Obj(bg, "traits"); // {tiers: [...], kim: {name, kind, v: [...]}, ...}
                if (trt != null)
                {
                    c.badges.traitTiers = Ints(J.Arr(trt, "tiers"));
                    int n = c.badges.traitTiers.Length;
                    c.badges.traitKind = new string[5];
                    c.badges.traitName = new string[5];
                    c.badges.traitValue = new double[5 * n];
                    foreach (Elem e in Enum.GetValues(typeof(Elem)))
                    {
                        var eo = J.Obj(trt, Keys.Of(e));
                        c.badges.traitKind[(int)e] = J.Str(eo, "kind", "");
                        c.badges.traitName[(int)e] = J.Str(eo, "name", "");
                        var v = J.Arr(eo, "v");
                        for (int k = 0; k < n && k < v.Count; k++) c.badges.traitValue[(int)e * n + k] = (double)v[k];
                    }
                }
            }
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
            c.home = HomeConfig.Parse(J.Obj(root, "home"), Rolls);
            c.shop = ShopConfig.FromJson(J.Obj(root, "shop"));
            c.casino = CasinoConfig.Parse(J.Obj(root, "casino"), Rolls);
            return c;
        }

        static List<ChestRoll> Rolls(List<object> rows)
        {
            var list = new List<ChestRoll>();
            foreach (var x in rows)
            {
                var ro = J.Obj(x);
                var roll = new ChestRoll { w = J.Num(ro, "w"), k = J.Str(ro, "k"), min = J.Int(ro, "min"), max = J.Int(ro, "max"), tier = J.Int(ro, "tier") };
                var rar = J.Obj(ro, "rar");
                if (rar != null)
                    foreach (var rv in rar) roll.rar.Add(new RarityWeight { rarity = Keys.ToRarity(rv.Key), w = (double)rv.Value });
                list.Add(roll);
            }
            return list;
        }

        static double[] Nums(List<object> l) => l.Select(x => x is double d ? d : 0).ToArray();

        static int[] Ints(List<object> l)
        {
            var a = new int[l.Count];
            for (int i = 0; i < a.Length; i++) a[i] = l[i] is double d ? (int)d : 0;
            return a;
        }
    }
}
