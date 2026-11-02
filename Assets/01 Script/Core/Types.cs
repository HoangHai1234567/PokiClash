// Kiểu dữ liệu dùng chung của phần logic, chép từ Web/src/core/types.ts và data/*.ts.
// Không dùng UnityEngine; các lớp định nghĩa có [Serializable] để ScriptableObject giữ được.
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    // Thứ tự giống ELEMS của web: kim, moc, thuy, hoa, tho
    public enum Elem { Kim, Moc, Thuy, Hoa, Tho }
    public enum Rarity { Common, Uncommon, Rare, Epic, Legend }

    // Atk, Def: cộng phần trăm vào chỉ số; Crit: cộng tỉ lệ chí mạng; Lifesteal: phần sát thương hút thành máu;
    // Dodge: tỉ lệ né đòn đánh thường; DmgTaken: phần sát thương nhận thêm (âm là giảm)
    public enum Stat { Atk, Def, Crit, Lifesteal, Dodge, DmgTaken }
    public enum StatusId { Burn, Stun, Regen, Evade }
    public enum Target { Self, Foe }

    // End: hết khi kết thúc lượt của chủ (buff đánh); Start: hết khi bắt đầu lượt sau của chủ (buff thủ)
    public enum Until { End, Start }

    public enum EffectKind { Buff, Heal, MaxHp, SelfDmg, Mana, Rage, Dmg, Shield, Status, Cleanse, Double, Extra, TrueStrike, IfLow, Revive }
    public enum CardKind { Pool, Skill, Ult, Passive }
    public enum PassiveTrigger { None, Start, TurnStart, LowHp, OnAttack, OnHit, Death }
    public enum StageKind { Normal, Mini, Boss }

    // Một hiệu ứng của thẻ. Trường nào không dùng cho loại đó thì để mặc định; trường "?" là có thể vắng (giống undefined của web).
    public sealed class Effect
    {
        public EffectKind K;
        public Stat Stat;
        public double V; // buff, mana, rage; status (vắng = 0)
        public int Turns;
        public Until? Until;
        public Target? On;
        public double Pct; // heal, maxhp, shield, revive
        public double PctCur; // selfdmg
        public double Mult; // dmg, extra, trueStrike
        public int? Hits;
        public double? Pierce;
        public double? Lifesteal;
        public StatusId Status;
        public double? Chance;
        public double Below; // ifLow
        public List<Effect> Then;
        public List<Effect> Else;

        public Effect Clone() => (Effect)MemberwiseClone();
    }

    [Serializable]
    public class CardDef
    {
        public string id;
        public string name;
        public Rarity rarity;
        public CardKind kind;
        public string icon;
        public int costMana;
        public int costRage;
        public PassiveTrigger trigger;
        public bool hasChance; // bị động: có tỉ lệ kích hoạt
        public double chance;
        public double below = 0.3; // bị động lowHp: ngưỡng máu
        public int unlock = 1; // thẻ chung: cấp người chơi để mở
        public string flavor;
        public string owner; // thẻ nội tại: id tướng
        public string effectsJson; // cây hiệu ứng dạng JSON (Unity không giữ được cây đệ quy)

        [NonSerialized] List<Effect> effects;

        public List<Effect> Effects => effects ??= EffectJson.ParseList(MiniJson.Parse(effectsJson ?? "[]"));
        public double? Chance => hasChance ? chance : (double?)null;
        public bool HasCost => costMana > 0 || costRage > 0;
    }

    // Một dạng trong dòng tiến hóa của tướng: lên sao thì đổi dạng (mốc ở BalanceConfig.formStars).
    [Serializable]
    public class HeroForm
    {
        public string name;
        public string aola; // thư mục trong reskin (chỉ bản dev)
        public double size = 1; // hệ số cỡ trên sân
    }

    [Serializable]
    public class HeroDef
    {
        public string id;
        public string name;
        public string title;
        public string aola; // = forms[0].aola (chỉ bản dev)
        public Elem elem;
        public Rarity rarity;
        public int[] stats = new int[6]; // công, thủ, công phép, thủ phép, máu, tốc (dạng 1)
        public string skill;
        public string ult;
        public string passive;
        public int shards; // số mảnh để mở
        public string line; // dòng tiến hóa (để hiển thị)
        public double size = 1; // = forms[0].size
        public HeroForm[] forms = new HeroForm[0]; // 1–3 dạng, dạng 1 trước

        // dạng ở sao này (chép formIndex của Web/src/core/progression.ts): đủ mốc formStars[i] thì sang dạng i + 2
        public int FormIndex(int[] formStars, int star)
        {
            int i = 0;
            while (i < formStars.Length && star >= formStars[i]) i++;
            return Math.Max(0, Math.Min(i, forms.Length - 1));
        }

        public HeroForm Form(int[] formStars, int star) =>
            forms.Length > 0 ? forms[FormIndex(formStars, star)] : new HeroForm { name = name, aola = aola, size = size };
    }

    [Serializable]
    public struct Pt
    {
        public double x;
        public double y;
        public Pt(double x, double y) { this.x = x; this.y = y; }
        public override string ToString() => $"({x}, {y})";
    }

    [Serializable]
    public class StageEnemy
    {
        public string hero;
        public int level;
        public bool boss;
    }

    [Serializable]
    public class StageDrop
    {
        public string hero;
        public double chance;
        public int min;
        public int max;
        public bool gift; // tướng tặng khi qua ải lần đầu (đủ mảnh mở luôn)
    }

    [Serializable]
    public class StageDef
    {
        public int id; // số toàn cục 1..40
        public Elem zone;
        public int idx; // 1..8 trong đảo
        public string name;
        public StageKind kind;
        public List<StageEnemy> enemies = new List<StageEnemy>();
        public List<StageDrop> drops = new List<StageDrop>();
    }

    [Serializable]
    public class ZoneDef
    {
        public Elem id;
        public int order; // 0..4, độ khó tăng dần
        public string name;
        public string sub;
        public int levelMin; // cấp đề nghị
        public int levelMax;
        public string art; // tên ảnh trong Assets/03 Art (zone_thuy...)
        public string skyTop;
        public string skyBottom;
        public string ground;
        public string sea;
        public List<Pt> nodes = new List<Pt>(); // 8 ải trên ảnh đảo, tỉ lệ 0..1 theo khung 9:16
        public Pt world; // vị trí vùng trên ảnh đảo lớn
    }

    // hiệu ứng đầu trận của tiềm năng: mana, nộ cộng lúc dựng tướng; chí mạng, hút máu thành buff cả trận
    public sealed class BattleStart
    {
        public double mana, rage, crit, lifesteal;
    }

    public class Member
    {
        public string heroId;
        public int level;
        public int star;
        public int cardSkill = 1;
        public int cardUlt = 1;
        public int cardPassive = 1;
        public bool boss;
        public StatMods mods; // phần cộng của side meta (null = không có)
        public BattleStart start; // hiệu ứng đầu trận của tiềm năng (null = không có)
    }

    public class TeamSetup
    {
        public string name;
        public bool ai;
        public List<Member> members = new List<Member>();
    }
}
