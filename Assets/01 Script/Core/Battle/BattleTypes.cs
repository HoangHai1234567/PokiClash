// Kiểu dữ liệu của trận, chép từ Web/src/core/battle.ts. Số liệu dùng double như number của JS
// (tránh chia số nguyên và để ảnh chụp so khớp từng giá trị với bản web).
using System.Collections.Generic;

namespace PokiClash.Core
{
    public enum Phase { Idle, Picking, Ready, ForceSwap, Over }
    public enum DmgKind { Attack, Extra, Skill, Ult, Card, Burn, Self }
    public enum InnateKind { Skill, Ult }

    public enum EvType
    {
        Start, Round, Turn, Card, Innate, Ult, Passive, Attack, Dmg, Heal, MaxHp, Shield, Mana, Rage, Buff, Status,
        Resist, Cleanse, Double, Stunned, Swap, Death, Revive, End,
    }

    public sealed class Buff
    {
        public Stat stat;
        public double v;
        public int left;
        public Until until;
    }

    public sealed class StatusInst
    {
        public StatusId id;
        public int left;
        public double v;
    }

    public sealed class Fighter
    {
        public int idx;
        public int side;
        public HeroDef hero;
        public int level;
        public int star;
        public int cardSkill, cardUlt, cardPassive;
        public bool boss;
        public double maxHp, hp, atk, def, spd;
        public double mana, rage, shield;
        public List<Buff> buffs = new List<Buff>();
        public List<StatusInst> statuses = new List<StatusInst>();
        public bool lowHpUsed;
        public bool revived; // đã dùng lần hồi sinh
        public bool dead;

        public double HpR => hp / maxHp;
        public int CardLv(InnateKind k) => k == InnateKind.Skill ? cardSkill : cardUlt;
        public bool Has(StatusId id) => statuses.Exists(x => x.id == id);
    }

    public sealed class Side
    {
        public string name;
        public bool ai;
        public int unlock;
        public List<Fighter> fighters = new List<Fighter>();
        public int active;
        public bool needSwap;
    }

    public sealed class QueueItem
    {
        public string card;
        public bool skill; // false = thẻ chung ("pool"), true = chiêu ("skill")
        public int lv;
        public string KindKey => skill ? "skill" : "pool";
    }

    public sealed class UltItem
    {
        public string card;
        public int lv;
    }

    public sealed class Turn
    {
        public int side;
        public int picksTotal;
        public int picksLeft;
        public List<string> offer = new List<string>();
        public List<QueueItem> queue = new List<QueueItem>();
        public bool swapped;
        public bool firstPick;
        public bool skillUsed;
        public UltItem ult;
        public bool doubleNext;
        public List<double> extra = new List<double>();
        public double trueStrike;
        public bool stunned;
    }

    // ảnh chụp số liệu một tướng sau mỗi sự kiện (màn trận chỉ vẽ theo ảnh chụp)
    public sealed class FSnap
    {
        public double hp, maxHp, shield, mana, rage;
        public bool dead;
        public List<(StatusId id, int left)> st = new List<(StatusId, int)>();
        public double atkB, defB;
    }

    public sealed class Snap
    {
        public int[] active = new int[2];
        public List<FSnap>[] f = { new List<FSnap>(), new List<FSnap>() };
    }

    // Một sự kiện trận. Trường nào dùng tuỳ loại (xem ToDict, giữ đúng khoá của bản web).
    public sealed class BattleEvent
    {
        public EvType t;
        public int side;
        public int round, first;
        public string card;
        public string kind; // card: "pool"/"skill"; innate: "skill"/"ult"
        public int lv, rep;
        public bool extra;
        public int from, to;
        public double amount, toHp, blocked;
        public bool crit;
        public double elem;
        public DmgKind dmgKind;
        public bool dodged;
        public double v;
        public Stat stat;
        public int turns;
        public StatusId status;
        public int idx;
        public bool forced;
        public double hp;
        public int winner;
        public Snap snap;

        public static readonly string[] TypeKeys =
        {
            "start", "round", "turn", "card", "innate", "ult", "passive", "attack", "dmg", "heal", "maxhp", "shield", "mana",
            "rage", "buff", "status", "resist", "cleanse", "double", "stunned", "swap", "death", "revive", "end",
        };

        public static readonly string[] DmgKindKeys = { "attack", "extra", "skill", "ult", "card", "burn", "self" };

        public string TypeKey => TypeKeys[(int)t];

        // Cây JSON giống sự kiện của web (để so golden và để ghi trận).
        public Dictionary<string, object> ToDict(bool withSnap = true)
        {
            var d = new Dictionary<string, object> { ["t"] = TypeKey };
            switch (t)
            {
                case EvType.Round: d["round"] = (double)round; d["first"] = (double)first; break;
                case EvType.Turn: d["side"] = (double)side; break;
                case EvType.Card:
                    d["side"] = (double)side; d["card"] = card; d["kind"] = kind; d["lv"] = (double)lv; d["rep"] = (double)rep;
                    break;
                case EvType.Innate: d["side"] = (double)side; d["card"] = card; d["kind"] = kind; break;
                case EvType.Ult: d["side"] = (double)side; d["card"] = card; break;
                case EvType.Passive: d["side"] = (double)side; d["idx"] = (double)idx; d["card"] = card; break;
                case EvType.Attack: d["side"] = (double)side; d["extra"] = extra; break;
                case EvType.Dmg:
                    d["from"] = (double)from; d["to"] = (double)to; d["amount"] = amount; d["toHp"] = toHp; d["blocked"] = blocked;
                    d["crit"] = crit; d["elem"] = elem; d["kind"] = DmgKindKeys[(int)dmgKind];
                    if (dodged) d["dodged"] = true;
                    break;
                case EvType.Heal:
                case EvType.MaxHp:
                case EvType.Shield:
                    d["side"] = (double)side; d["amount"] = amount;
                    break;
                case EvType.Mana:
                case EvType.Rage:
                    d["side"] = (double)side; d["v"] = v;
                    break;
                case EvType.Buff: d["side"] = (double)side; d["stat"] = Keys.Of(stat); d["v"] = v; d["turns"] = (double)turns; break;
                case EvType.Status: d["side"] = (double)side; d["id"] = Keys.Of(status); d["turns"] = (double)turns; break;
                case EvType.Resist:
                case EvType.Cleanse:
                case EvType.Double:
                case EvType.Stunned:
                    d["side"] = (double)side;
                    break;
                case EvType.Swap: d["side"] = (double)side; d["from"] = (double)from; d["to"] = (double)to; d["forced"] = forced; break;
                case EvType.Death: d["side"] = (double)side; d["idx"] = (double)idx; break;
                case EvType.Revive: d["side"] = (double)side; d["idx"] = (double)idx; d["hp"] = hp; break;
                case EvType.End: d["winner"] = (double)winner; break;
            }
            if (withSnap && snap != null) d["snap"] = SnapDict(snap);
            return d;
        }

        public static Dictionary<string, object> SnapDict(Snap s)
        {
            var sides = new List<object>();
            foreach (var list in s.f)
            {
                var fs = new List<object>();
                foreach (var f in list)
                {
                    var st = new List<object>();
                    foreach (var x in f.st) st.Add(new List<object> { Keys.Of(x.id), (double)x.left });
                    fs.Add(new Dictionary<string, object>
                    {
                        ["hp"] = f.hp, ["maxHp"] = f.maxHp, ["shield"] = f.shield, ["mana"] = f.mana, ["rage"] = f.rage, ["dead"] = f.dead,
                        ["st"] = st, ["atkB"] = f.atkB, ["defB"] = f.defB,
                    });
                }
                sides.Add(fs);
            }
            return new Dictionary<string, object>
            {
                ["active"] = new List<object> { (double)s.active[0], (double)s.active[1] },
                ["f"] = sides,
            };
        }
    }
}
