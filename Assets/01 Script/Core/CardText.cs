// Đổi hiệu ứng của thẻ ra chữ tiếng Việt theo cấp thẻ, chép từ Web/src/core/cardtext.ts để mô tả khớp số thật.
// Kèm bộ đọc cây hiệu ứng từ JSON.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public static class EffectJson
    {
        public static List<Effect> ParseList(object v)
        {
            var list = new List<Effect>();
            foreach (var x in J.Arr(v)) list.Add(Parse(J.Obj(x)));
            return list;
        }

        public static Effect Parse(Dictionary<string, object> o)
        {
            var e = new Effect { K = Keys.ToEffect(J.Str(o, "k")) };
            switch (e.K)
            {
                case EffectKind.Buff:
                    e.Stat = Keys.ToStat(J.Str(o, "stat"));
                    e.V = J.Num(o, "v");
                    e.Turns = J.Int(o, "turns");
                    if (J.Has(o, "until")) e.Until = J.Str(o, "until") == "start" ? Core.Until.Start : Core.Until.End;
                    break;
                case EffectKind.Heal:
                case EffectKind.MaxHp:
                case EffectKind.Shield:
                case EffectKind.Revive:
                    e.Pct = J.Num(o, "pct");
                    break;
                case EffectKind.SelfDmg:
                    e.PctCur = J.Num(o, "pctCur");
                    break;
                case EffectKind.Mana:
                case EffectKind.Rage:
                    e.V = J.Num(o, "v");
                    break;
                case EffectKind.Dmg:
                    e.Mult = J.Num(o, "mult");
                    e.Hits = J.IntOpt(o, "hits");
                    e.Pierce = J.NumOpt(o, "pierce");
                    e.Lifesteal = J.NumOpt(o, "lifesteal");
                    break;
                case EffectKind.Status:
                    e.Status = Keys.ToStatus(J.Str(o, "id"));
                    e.Turns = J.Int(o, "turns");
                    e.V = J.Num(o, "v");
                    e.Chance = J.NumOpt(o, "chance");
                    break;
                case EffectKind.Extra:
                case EffectKind.TrueStrike:
                    e.Mult = J.Num(o, "mult");
                    break;
                case EffectKind.IfLow:
                    e.Below = J.Num(o, "below");
                    e.Then = ParseList(J.Get(o, "then"));
                    if (J.Has(o, "else")) e.Else = ParseList(J.Get(o, "else"));
                    break;
            }
            if (J.Has(o, "on")) e.On = J.Str(o, "on") == "foe" ? Target.Foe : Target.Self;
            return e;
        }
    }

    public static class CardText
    {
        static double R2(double x) => Js.Round(x * 100) / 100;

        public static double LvFactor(double cardLvStep, int lv) => 1 + cardLvStep * (lv - 1);

        public static List<Effect> ScaleEffects(List<Effect> effects, int lv, double cardLvStep)
        {
            if (lv <= 1) return effects;
            double f = LvFactor(cardLvStep, lv);
            var res = new List<Effect>(effects.Count);
            foreach (var src in effects)
            {
                var e = src.Clone();
                switch (e.K)
                {
                    case EffectKind.Buff: e.V = R2(e.V * f); break;
                    case EffectKind.Heal:
                    case EffectKind.MaxHp:
                    case EffectKind.Shield:
                        e.Pct = R2(e.Pct * f);
                        break;
                    case EffectKind.SelfDmg: e.PctCur = R2(e.PctCur / f); break;
                    case EffectKind.Mana:
                    case EffectKind.Rage:
                        e.V = Js.Round(e.V * f);
                        break;
                    case EffectKind.Dmg:
                        e.Mult = R2(e.Mult * f);
                        e.Lifesteal = e.Lifesteal.HasValue && e.Lifesteal.Value != 0 ? R2(e.Lifesteal.Value * f) : (double?)null;
                        break;
                    case EffectKind.Status:
                        if (e.V != 0) e.V = R2(e.V * f);
                        if (e.Chance.HasValue && e.Chance.Value != 0) e.Chance = Math.Min(1, R2(e.Chance.Value * f));
                        break;
                    case EffectKind.Extra:
                    case EffectKind.TrueStrike:
                        e.Mult = R2(e.Mult * f);
                        break;
                    case EffectKind.IfLow:
                        e.Then = ScaleEffects(e.Then, lv, cardLvStep);
                        e.Else = e.Else != null ? ScaleEffects(e.Else, lv, cardLvStep) : null;
                        break;
                    case EffectKind.Revive:
                        e.Pct = Math.Min(1, R2(e.Pct * f));
                        break;
                }
                res.Add(e);
            }
            return res;
        }

        public static string Pct(double x) => $"{Js.RoundInt(x * 100)}%";

        static string LowFirst(string t) => t.Length == 0 ? t : char.ToLowerInvariant(t[0]) + t.Substring(1);

        static string StatName(Stat s)
        {
            switch (s)
            {
                case Stat.Atk: return "Công";
                case Stat.Def: return "Thủ";
                case Stat.Crit: return "chí mạng";
                case Stat.Lifesteal: return "hút máu";
                case Stat.Dodge: return "né";
                default: return "sát thương nhận";
            }
        }

        // Buff thủ (def, dmgTaken, dodge) mặc định che tới đầu lượt sau, buff khác hết cuối lượt.
        public static Until DefaultUntil(Stat s) =>
            s == Stat.Def || s == Stat.DmgTaken || s == Stat.Dodge ? Until.Start : Until.End;

        static string TurnsText(int turns, Until until, bool foe)
        {
            if (turns >= 99) return " cả trận";
            if (foe) return turns == 1 ? " 1 lượt" : $" {turns} lượt";
            if (until == Until.Start) return turns == 1 ? " tới lượt sau" : $" trong {turns} lượt địch";
            return turns == 1 ? " lượt này" : $" trong {turns} lượt";
        }

        public static string EffectText(Effect e)
        {
            switch (e.K)
            {
                case EffectKind.Buff:
                {
                    bool foe = e.On == Target.Foe;
                    var until = e.Until ?? DefaultUntil(e.Stat);
                    string sign = e.V >= 0 ? "+" : "−";
                    string t = TurnsText(e.Turns, until, foe);
                    if (e.Stat == Stat.Lifesteal) return $"Hút {Pct(e.V)} sát thương thành máu{t}";
                    if (e.Stat == Stat.Dodge) return $"{Pct(e.V)} né đòn đánh thường{t}";
                    if (e.Stat == Stat.DmgTaken) return $"{(e.V < 0 ? "Giảm" : "Nhận thêm")} {Pct(Math.Abs(e.V))} sát thương{t}";
                    return $"{(foe ? "Địch " : "")}{sign}{Pct(Math.Abs(e.V))} {StatName(e.Stat)}{t}";
                }
                case EffectKind.Heal:
                    return $"Hồi {Pct(e.Pct)} máu";
                case EffectKind.MaxHp:
                    return $"+{Pct(e.Pct)} máu tối đa cả trận";
                case EffectKind.SelfDmg:
                    return $"Mất {Pct(e.PctCur)} máu đang có";
                case EffectKind.Mana:
                    if (e.On == Target.Foe) return $"Hút {Js.Num(Math.Abs(e.V))} mana của địch";
                    return $"+{Js.Num(e.V)} mana";
                case EffectKind.Rage:
                    if (e.On == Target.Foe) return $"Hút {Js.Num(Math.Abs(e.V))} nộ của địch";
                    return $"+{Js.Num(e.V)} nộ";
                case EffectKind.Dmg:
                {
                    string s = e.Hits.HasValue && e.Hits.Value > 1
                        ? $"Đánh {e.Hits.Value} lần, mỗi lần {Pct(e.Mult)} Công"
                        : $"Gây {Pct(e.Mult)} Công sát thương";
                    if (e.Pierce.HasValue && e.Pierce.Value != 0) s += $", xuyên {Pct(e.Pierce.Value)} Thủ";
                    if (e.Lifesteal.HasValue && e.Lifesteal.Value != 0) s += $", hút {Pct(e.Lifesteal.Value)} thành máu";
                    return s;
                }
                case EffectKind.Shield:
                    return $"Khiên bằng {Pct(e.Pct)} máu tối đa";
                case EffectKind.Status:
                {
                    string c = e.Chance.HasValue && e.Chance.Value != 0 && e.Chance.Value < 1 ? $"{Pct(e.Chance.Value)} cơ hội: " : "";
                    switch (e.Status)
                    {
                        case StatusId.Burn: return $"{c}Đốt địch {e.Turns} lượt ({Pct(e.V)} máu mỗi lượt)";
                        case StatusId.Regen: return $"{c}Hồi {Pct(e.V)} máu đầu mỗi lượt, {e.Turns} lượt";
                        case StatusId.Stun: return $"{c}Làm địch choáng";
                        case StatusId.Evade: return $"{c}Né trọn đòn đánh kế tiếp";
                    }
                    return "";
                }
                case EffectKind.Cleanse:
                    return "Xoá hiệu ứng xấu";
                case EffectKind.Double:
                    return "Thẻ kế tiếp chạy 2 lần";
                case EffectKind.Extra:
                    return $"Cuối lượt đánh thêm một cú {Pct(e.Mult)} Công";
                case EffectKind.TrueStrike:
                    return $"Đòn đánh lượt này bỏ qua Thủ, ×{Js.Num(e.Mult).Replace('.', ',')}";
                case EffectKind.IfLow:
                    return $"Máu dưới {Pct(e.Below)}: {LowFirst(string.Join(", ", e.Then.Select(EffectText)))}" +
                           (e.Else != null ? $". Không thì: {LowFirst(string.Join(", ", e.Else.Select(EffectText)))}" : "");
                case EffectKind.Revive:
                    return $"Hồi sinh với {Pct(e.Pct)} máu";
            }
            return "";
        }

        public static string Text(CardDef c, int lv, double cardLvStep)
        {
            string body = string.Join(". ", ScaleEffects(c.Effects, lv, cardLvStep).Select(EffectText));
            if (c.kind != CardKind.Passive) return body + ".";
            string low = LowFirst(body);
            switch (c.trigger)
            {
                case PassiveTrigger.Start: return $"Vào trận: {low}.";
                case PassiveTrigger.TurnStart: return $"Đầu mỗi lượt: {low}.";
                case PassiveTrigger.LowHp: return $"Lần đầu máu dưới {Pct(c.below)}: {low}.";
                case PassiveTrigger.OnAttack:
                {
                    double ch = Math.Min(1, (c.Chance ?? 1) * LvFactor(cardLvStep, lv));
                    return $"Mỗi đòn đánh thường: {Pct(ch)} cơ hội {low}.";
                }
                case PassiveTrigger.OnHit: return $"Mỗi lần bị đánh: {low}.";
                case PassiveTrigger.Death: return $"Lần đầu gục: {low}.";
            }
            return body + ".";
        }

        public static string Text(CardDef c, int lv = 1) => Text(c, lv, GameData.Current.Cfg.cardLvStep);

        public static string CostText(CardDef c)
        {
            var parts = new List<string>();
            if (c.costRage > 0) parts.Add($"{c.costRage} nộ");
            if (c.costMana > 0) parts.Add($"{c.costMana} mana");
            return string.Join(" + ", parts);
        }
    }
}
