// Ngũ hành, độ hiếm và tên hiển thị, chép từ Web/src/core/elements.ts.
// Kèm bảng đổi enum <-> chuỗi khoá dùng trong JSON và file lưu.
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    public static class Elements
    {
        public static readonly Elem[] All = { Elem.Kim, Elem.Moc, Elem.Thuy, Elem.Hoa, Elem.Tho };

        // Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy, Thủy khắc Hỏa, Hỏa khắc Kim
        public static Elem Beats(Elem e)
        {
            switch (e)
            {
                case Elem.Kim: return Elem.Moc;
                case Elem.Moc: return Elem.Tho;
                case Elem.Tho: return Elem.Thuy;
                case Elem.Thuy: return Elem.Hoa;
                default: return Elem.Kim;
            }
        }

        public const double Strong = 1.5;
        public const double Weak = 0.75;

        public static double Mult(Elem att, Elem def)
        {
            if (Beats(att) == def) return Strong;
            if (Beats(def) == att) return Weak;
            return 1;
        }

        // tướng đồng hành (tướng khởi đầu người chơi đã chọn, GD_Claude/15_TuongKhoiDau.md) không chịu thiệt khi khắc hệ: đánh hệ khắc
        // mình và bị hệ khắc mình đánh đều ×1; vẫn ×1,5 khi mình khắc
        public static double Mult(Elem att, Elem def, bool attPartner, bool defPartner)
        {
            double m = Mult(att, def);
            return m < 1 && attPartner || m > 1 && defPartner ? 1 : m;
        }

        public static string Name(Elem e)
        {
            switch (e)
            {
                case Elem.Kim: return "Kim";
                case Elem.Moc: return "Mộc";
                case Elem.Thuy: return "Thủy";
                case Elem.Hoa: return "Hỏa";
                default: return "Thổ";
            }
        }

        public static string Color(Elem e)
        {
            switch (e)
            {
                case Elem.Kim: return "#b8c4cf";
                case Elem.Moc: return "#6cbf4f";
                case Elem.Thuy: return "#4a90d9";
                case Elem.Hoa: return "#e8553f";
                default: return "#e2a93b";
            }
        }

        public static string RarityName(Rarity r)
        {
            switch (r)
            {
                case Rarity.Common: return "Thường";
                case Rarity.Uncommon: return "Khá";
                case Rarity.Rare: return "Hiếm";
                case Rarity.Epic: return "Sử thi";
                default: return "Huyền thoại";
            }
        }

        public static string RarityColor(Rarity r)
        {
            switch (r)
            {
                case Rarity.Common: return "#b9b1a3";
                case Rarity.Uncommon: return "#6cbf4f";
                case Rarity.Rare: return "#4a90d9";
                case Rarity.Epic: return "#9a6ad6";
                default: return "#f39a2d";
            }
        }

        public static string KindName(CardKind k)
        {
            switch (k)
            {
                case CardKind.Pool: return "Thẻ chung";
                case CardKind.Skill: return "Chiêu";
                case CardKind.Ult: return "Tuyệt kỹ";
                default: return "Bị động";
            }
        }
    }

    // Khoá chuỗi trong JSON (giống bản web): "kim", "dmgTaken", "trueStrike"...
    public static class Keys
    {
        static readonly Dictionary<string, Elem> ElemOf = new Dictionary<string, Elem>
        {
            ["kim"] = Elem.Kim, ["moc"] = Elem.Moc, ["thuy"] = Elem.Thuy, ["hoa"] = Elem.Hoa, ["tho"] = Elem.Tho,
        };
        static readonly Dictionary<string, Rarity> RarityOf = new Dictionary<string, Rarity>
        {
            ["common"] = Rarity.Common, ["uncommon"] = Rarity.Uncommon, ["rare"] = Rarity.Rare, ["epic"] = Rarity.Epic, ["legend"] = Rarity.Legend,
        };
        static readonly Dictionary<string, Stat> StatOf = new Dictionary<string, Stat>
        {
            ["atk"] = Stat.Atk, ["def"] = Stat.Def, ["crit"] = Stat.Crit, ["lifesteal"] = Stat.Lifesteal, ["dodge"] = Stat.Dodge, ["dmgTaken"] = Stat.DmgTaken,
        };
        static readonly Dictionary<string, StatusId> StatusOf = new Dictionary<string, StatusId>
        {
            ["burn"] = StatusId.Burn, ["stun"] = StatusId.Stun, ["regen"] = StatusId.Regen, ["evade"] = StatusId.Evade,
        };
        static readonly Dictionary<string, EffectKind> EffectOf = new Dictionary<string, EffectKind>
        {
            ["buff"] = EffectKind.Buff, ["heal"] = EffectKind.Heal, ["maxhp"] = EffectKind.MaxHp, ["selfdmg"] = EffectKind.SelfDmg,
            ["mana"] = EffectKind.Mana, ["rage"] = EffectKind.Rage, ["dmg"] = EffectKind.Dmg, ["shield"] = EffectKind.Shield,
            ["status"] = EffectKind.Status, ["cleanse"] = EffectKind.Cleanse, ["double"] = EffectKind.Double, ["extra"] = EffectKind.Extra,
            ["trueStrike"] = EffectKind.TrueStrike, ["ifLow"] = EffectKind.IfLow, ["revive"] = EffectKind.Revive,
            ["evolve"] = EffectKind.Evolve,
        };
        static readonly Dictionary<string, CardKind> KindOf = new Dictionary<string, CardKind>
        {
            ["pool"] = CardKind.Pool, ["skill"] = CardKind.Skill, ["ult"] = CardKind.Ult, ["passive"] = CardKind.Passive,
        };
        static readonly Dictionary<string, PassiveTrigger> TriggerOf = new Dictionary<string, PassiveTrigger>
        {
            ["start"] = PassiveTrigger.Start, ["turnStart"] = PassiveTrigger.TurnStart, ["lowHp"] = PassiveTrigger.LowHp,
            ["onAttack"] = PassiveTrigger.OnAttack, ["onHit"] = PassiveTrigger.OnHit, ["death"] = PassiveTrigger.Death,
        };
        static readonly Dictionary<string, StageKind> StageKindOf = new Dictionary<string, StageKind>
        {
            ["normal"] = StageKind.Normal, ["mini"] = StageKind.Mini, ["boss"] = StageKind.Boss,
        };
        static readonly Dictionary<string, StageTag> StageTagOf = new Dictionary<string, StageTag>
        {
            ["hero"] = StageTag.Hero, ["minion"] = StageTag.Minion, ["buff"] = StageTag.Buff, ["group"] = StageTag.Group,
            ["pair"] = StageTag.Pair, ["elite"] = StageTag.Elite, ["gate"] = StageTag.Gate,
        };

        static T Of<T>(Dictionary<string, T> map, string s, string what)
        {
            if (s != null && map.TryGetValue(s, out var v)) return v;
            throw new FormatException($"Không rõ {what} '{s}'");
        }

        static string KeyOf<T>(Dictionary<string, T> map, T v)
        {
            foreach (var kv in map) if (EqualityComparer<T>.Default.Equals(kv.Value, v)) return kv.Key;
            return v.ToString();
        }

        public static Elem ToElem(string s) => Of(ElemOf, s, "hệ");
        public static Rarity ToRarity(string s) => Of(RarityOf, s, "độ hiếm");
        public static Stat ToStat(string s) => Of(StatOf, s, "chỉ số");
        public static StatusId ToStatus(string s) => Of(StatusOf, s, "trạng thái");
        public static EffectKind ToEffect(string s) => Of(EffectOf, s, "hiệu ứng");
        public static CardKind ToKind(string s) => Of(KindOf, s, "loại thẻ");
        public static PassiveTrigger ToTrigger(string s) => s == null ? PassiveTrigger.None : Of(TriggerOf, s, "kích hoạt");
        public static StageKind ToStageKind(string s) => Of(StageKindOf, s, "loại ải");
        public static StageTag ToStageTag(string s) => s == null ? StageTag.None : Of(StageTagOf, s, "kiểu ải");

        public static bool TryElem(string s, out Elem e) => ElemOf.TryGetValue(s ?? "", out e);

        public static string Of(Elem e) => KeyOf(ElemOf, e);
        public static string Of(Rarity r) => KeyOf(RarityOf, r);
        public static string Of(Stat s) => KeyOf(StatOf, s);
        public static string Of(StatusId s) => KeyOf(StatusOf, s);
        public static string Of(StageTag t) => t == StageTag.None ? null : KeyOf(StageTagOf, t);
    }
}
