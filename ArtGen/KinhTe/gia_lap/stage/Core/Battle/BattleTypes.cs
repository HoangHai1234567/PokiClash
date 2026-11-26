// Kiểu dữ liệu của trận, chép từ Web/src/core/battle.ts. Số liệu dùng double như number của JS
// (tránh chia số nguyên và để ảnh chụp so khớp từng giá trị với bản web).
using System.Collections.Generic;

namespace PokiClash.Core
{
    public enum Phase { Idle, Picking, Ready, ForceSwap, Over }
    // Poison: độc mỗi lượt và kích nổ độc; Thorns: phản đòn (2026-11-17, thêm cuối)
    public enum DmgKind { Attack, Extra, Skill, Ult, Card, Burn, Self, Poison, Thorns }
    public enum InnateKind { Skill, Ult }

    public enum EvType
    {
        Start, Round, Turn, Card, Innate, Ult, Passive, Attack, Dmg, Heal, MaxHp, Shield, Mana, Rage, Buff, Status,
        Resist, Cleanse, Double, Stunned, Swap, Death, Revive, End, Evolve,
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
        public double v; // bỏng, hồi: phần máu tối đa mỗi lượt; độc: tổng số máu mất mỗi lượt của mọi lớp (định lúc tẩm)
        public int stacks; // độc: số lớp (1..CardText.PoisonMax)
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
        public bool evo; // boss ải 8: có thẻ Tiến Hóa (dòng 1 dạng thì không tiến hóa được)
        public int form; // dạng đang hiện trong dòng tiến hóa (tướng thường theo sao, boss tiến hóa từ 0)
        public bool partner; // tướng đồng hành: không chịu thiệt khi khắc hệ (Battle.ElemMult)
        // tên hiện trên sân (web fighterName): boss tiến hóa theo dạng đang có, tướng khác theo tên dòng
        public string Name => evo && form < hero.forms.Length ? hero.forms[form].name : hero.name;
        public double maxHp, hp, atk, def, spd;
        public double mana, rage, shield;
        public List<Buff> buffs = new List<Buff>();
        public List<StatusInst> statuses = new List<StatusInst>();
        public bool lowHpUsed;
        public string trait; // bị động boss của ải (Member.trait), chạy sau bị động của tướng; null = không có
        public bool traitLowUsed; // bị động boss kiểu "máu thấp" đã chạy (một lần mỗi trận, kể cả khi boss tiến hóa)
        public bool revived; // đã dùng lần hồi sinh
        public int stunImmune; // Sổ Phép "Tỉnh Táo": số lượt của mình còn miễn choáng (giảm cuối mỗi lượt của mình)
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
        public StatusInst spread; // độc của tướng vừa gục, chờ lan sang tướng ra thay (null = không có)
        public BattleRules rules; // luật thêm của Sổ Phép (null = không có, như mọi trận cũ và mọi đội máy)
        public RuleState rs = new RuleState(); // lượt dùng còn lại của các luật một-lần-mỗi-trận
    }

    // Luật trận thêm từ Sổ Phép (Core/SoPhep.cs, GD_Claude/28_SoPhep.md, người dùng duyệt 2026-11-24). Số 0 / false = tắt.
    public sealed class BattleRules
    {
        public int rerolls, bossRerolls; // Lật Trang, Sổ Tay Chúa Tể (trận có boss / mini boss): lượt đổi cả bộ thẻ đang chọn
        public int firstOfferAdd; // Rộng Tay: lần chọn đầu mỗi lượt hiện thêm thẻ
        public double groupWeight; // Dồn Tay: thẻ cùng nhóm (Công / Thủ / Hồi) với thẻ vừa chọn nặng thêm bấy nhiêu lần ở lần rút kế
        public int holds; // Giữ Nét: số lần giữ thẻ tốt nhất chưa chọn của lần chọn cuối sang lần chọn đầu lượt sau
        public double rareWeight; // Mắt Tinh: thẻ Hiếm trở lên nặng thêm bấy nhiêu lần
        public int picks, offer; // Chốt 1: số lần chọn mỗi lượt, số thẻ mỗi lần (0 = theo cấu hình)
        public double benchMana; // Mực Chờ: mana thêm mỗi lượt cho tướng dự bị
        public double swapInShield, swapOutHeal; // Vào Sân (khiên, phần máu tối đa) | Rút Lui (hồi tướng vừa rút ra)
        public double manaCarry; // Tiếp Sức: tự đổi tướng thì tướng vào nhận phần này mana của tướng ra
        public double koRage; // Tiếp Nối: tướng gục thì tướng ra thay nhận bấy nhiêu nộ
        public int midSwaps; // Chốt 2 Đổi Vai: số lần đổi tướng được cả khi đã chọn thẻ
        public double assist; // Chốt 2 Hợp Lực: tướng dự bị còn sống đánh phụ (phần Công của nó) khi tướng chính tung Tuyệt kỹ
        public double advAdd, disAdd; // Mũi Nhọn: đánh hệ mình khắc cộng thêm hệ số | Lá Chắn: đánh hệ khắc mình bớt thiệt
        public double lowAt, lowHeal; // Nét Cứu: lần đầu một tướng xuống dưới lowAt máu mỗi trận thì hồi lowHeal máu tối đa
        public int stunGuard; // Tỉnh Táo: hết choáng thì miễn choáng bấy nhiêu lượt của mình
        public double revivePct; // Chốt 3 Vẽ Lại: một lần mỗi trận, tướng gục sống lại với phần máu này (không áp cho boss)
        public double thornsAt, thorns; // Chốt 3 Phản Nét: lần đầu xuống dưới thornsAt máu, phản lại phần sát thương này tới hết trận
        public int elemExtra = -1, elemExtraN; // Năm Bút Chì: đánh địch hệ này (Elem) thì mỗi lần chọn hiện thêm elemExtraN thẻ
        public int lastOffer; // Trang Cuối: lần chọn cuối mỗi lượt hiện ít nhất bấy nhiêu thẻ
        public double executeBelow; // Nét Kết: đòn của mình để địch (không phải boss) dưới ngưỡng này thì kết liễu
        public double ultDiscount; // Chốt 4 Chữ Ký: Tuyệt kỹ đầu tiên mỗi trận bớt phần nộ này (0,5 = nửa nộ)
        public bool doubleFirst; // Chốt 4 Nét Kép: thẻ chọn đầu tiên của trận chạy hai lần
    }

    public sealed class RuleState
    {
        public int rerolls, holds, midSwaps;
        public string held; // thẻ đang giữ chờ lần chọn đầu lượt sau
        public bool hasLastGroup;
        public CardGroup lastGroup; // nhóm của thẻ vừa chọn (Dồn Tay)
        public bool lowHealUsed, reviveUsed, thornsUsed, freeUltUsed, doubleUsed;
    }

    public sealed class QueueItem
    {
        public string card; // thẻ chung (chiêu ra ngay, không vào hàng)
        public int lv;
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
        public double empower; // cường hóa thẻ kế tiếp trong hàng (cộng dồn, dùng một lần)
    }

    // ảnh chụp số liệu một tướng sau mỗi sự kiện (màn trận chỉ vẽ theo ảnh chụp)
    public sealed class FSnap
    {
        public double hp, maxHp, shield, mana, rage;
        public bool dead;
        public List<(StatusId id, int left)> st = new List<(StatusId, int)>();
        public List<int> stk = new List<int>(); // số lớp từng trạng thái, cùng thứ tự st (độc; trạng thái khác 0)
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
        public string kind; // card: "pool"; innate: "skill" (ra đòn ngay, hiệu ứng theo sau)/"ult"
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
        public int form; // evolve: dạng mới
        public int winner;
        public Snap snap;

        public static readonly string[] TypeKeys =
        {
            "start", "round", "turn", "card", "innate", "ult", "passive", "attack", "dmg", "heal", "maxhp", "shield", "mana",
            "rage", "buff", "status", "resist", "cleanse", "double", "stunned", "swap", "death", "revive", "end", "evolve",
        };

        public static readonly string[] DmgKindKeys = { "attack", "extra", "skill", "ult", "card", "burn", "self", "poison", "thorns" };

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
                case EvType.Evolve: d["side"] = (double)side; d["idx"] = (double)idx; d["form"] = (double)form; d["hp"] = hp; break;
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
                    for (int i = 0; i < f.st.Count; i++)
                    {
                        var x = f.st[i];
                        int k = i < f.stk.Count ? f.stk[i] : 0;
                        // độc ghi thêm số lớp: ["poison", lượt, lớp]
                        st.Add(k > 0 ? new List<object> { Keys.Of(x.id), (double)x.left, (double)k } : new List<object> { Keys.Of(x.id), (double)x.left });
                    }
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
