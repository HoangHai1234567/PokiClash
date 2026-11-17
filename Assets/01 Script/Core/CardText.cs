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
                case EffectKind.Evolve:
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
                    e.Missing = J.NumOpt(o, "missing");
                    break;
                case EffectKind.Status:
                    e.Status = Keys.ToStatus(J.Str(o, "id"));
                    e.Turns = J.Int(o, "turns");
                    e.V = J.Num(o, "v");
                    e.Chance = J.NumOpt(o, "chance");
                    e.Stacks = J.IntOpt(o, "stacks");
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
                // 2026-11-17
                case EffectKind.Execute:
                    e.Mult = J.Num(o, "mult");
                    e.Below = J.Num(o, "below");
                    break;
                case EffectKind.Detonate:
                case EffectKind.Bash:
                    e.Mult = J.Has(o, "mult") ? J.Num(o, "mult") : 1;
                    break;
                case EffectKind.Empower:
                    e.V = J.Num(o, "v");
                    break;
                case EffectKind.Combo:
                    e.Group = Keys.ToGroup(J.Str(o, "group"));
                    e.Then = ParseList(J.Get(o, "then"));
                    break;
                case EffectKind.Resonance:
                    e.Then = ParseList(J.Get(o, "then"));
                    break;
                case EffectKind.IfBeat:
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

        public static List<Effect> ScaleEffects(List<Effect> effects, int lv, double cardLvStep) =>
            lv <= 1 ? effects : ScaleBy(effects, LvFactor(cardLvStep, lv));

        // nhân số của hiệu ứng lên f lần (cấp thẻ; combo, cộng hưởng theo số thẻ / tướng; cường hóa thẻ kế tiếp), làm tròn như cấp thẻ
        public static List<Effect> ScaleBy(List<Effect> effects, double f)
        {
            if (f == 1 || effects == null) return effects;
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
                    case EffectKind.IfBeat:
                    case EffectKind.Combo:
                    case EffectKind.Resonance:
                        e.Then = ScaleBy(e.Then, f);
                        e.Else = e.Else != null ? ScaleBy(e.Else, f) : null;
                        break;
                    case EffectKind.Revive:
                        e.Pct = Math.Min(1, R2(e.Pct * f));
                        break;
                    case EffectKind.Execute:
                    case EffectKind.Detonate:
                    case EffectKind.Bash:
                        e.Mult = R2(e.Mult * f);
                        break;
                    case EffectKind.Empower:
                        e.V = R2(e.V * f);
                        break;
                }
                res.Add(e);
            }
            return res;
        }

        // ---------- nhóm thẻ (combo) ----------

        // thẻ thuộc nhóm nào, suy từ hiệu ứng (kể cả nhánh của ifLow, ifBeat, combo, cộng hưởng)
        public static bool InGroup(CardDef c, CardGroup g) => c != null && InGroup(c.Effects, g);

        static bool InGroup(List<Effect> list, CardGroup g)
        {
            if (list == null) return false;
            foreach (var e in list)
            {
                bool self = e.On != Target.Foe;
                switch (e.K)
                {
                    case EffectKind.Dmg:
                    case EffectKind.Extra:
                    case EffectKind.TrueStrike:
                    case EffectKind.Execute:
                    case EffectKind.Detonate:
                    case EffectKind.Bash:
                        if (g == CardGroup.Atk) return true;
                        break;
                    case EffectKind.Shield:
                        if (g == CardGroup.Def) return true;
                        break;
                    case EffectKind.Buff:
                        if (g == CardGroup.Def && self && (e.Stat == Stat.Def && e.V > 0 || e.Stat == Stat.DmgTaken && e.V < 0 ||
                                                           e.Stat == Stat.Dodge && e.V > 0 || e.Stat == Stat.Thorns && e.V > 0)) return true;
                        break;
                    case EffectKind.Status:
                        if (g == CardGroup.Def && self && e.Status == StatusId.Evade) return true;
                        if (g == CardGroup.Heal && self && e.Status == StatusId.Regen) return true;
                        break;
                    case EffectKind.Heal:
                    case EffectKind.MaxHp:
                    case EffectKind.Cleanse:
                        if (g == CardGroup.Heal) return true;
                        break;
                }
                if (InGroup(e.Then, g) || InGroup(e.Else, g)) return true;
            }
            return false;
        }

        public static string GroupName(CardGroup g) => g == CardGroup.Atk ? "đánh" : g == CardGroup.Def ? "thủ" : "hồi máu";

        static void CollectKinds(List<Effect> list, HashSet<EffectKind> kinds, HashSet<StatusId> st, HashSet<Stat> stats, HashSet<CardGroup> groups)
        {
            if (list == null) return;
            foreach (var e in list)
            {
                kinds.Add(e.K);
                if (e.K == EffectKind.Status) st.Add(e.Status);
                if (e.K == EffectKind.Buff) stats.Add(e.Stat);
                if (e.K == EffectKind.Combo) groups.Add(e.Group);
                CollectKinds(e.Then, kinds, st, stats, groups);
                CollectKinds(e.Else, kinds, st, stats, groups);
            }
        }

        // luật chi tiết của các cơ chế 2026-11-17 có trong thẻ (cho hộp chi tiết thẻ); rỗng nếu thẻ không có
        public static string Note(CardDef c)
        {
            var kinds = new HashSet<EffectKind>();
            var st = new HashSet<StatusId>();
            var stats = new HashSet<Stat>();
            var groups = new HashSet<CardGroup>();
            CollectKinds(c.Effects, kinds, st, stats, groups);
            var l = new List<string>();
            foreach (var g in groups)
                l.Add(g == CardGroup.Atk ? "Thẻ đánh: thẻ gây sát thương (kể cả đánh thêm, kết liễu, kích nổ độc, đập khiên)."
                    : g == CardGroup.Def ? "Thẻ thủ: khiên, tăng Thủ, giảm sát thương nhận, né, phản đòn."
                    : "Thẻ hồi máu: hồi máu, hồi mỗi lượt, tăng máu tối đa, xoá hiệu ứng xấu.");
            if (st.Contains(StatusId.Poison) || kinds.Contains(EffectKind.Detonate))
                l.Add($"Độc cộng dồn tới {PoisonMax} lớp, mỗi lần tẩm thêm thì tính lại số lượt. Tướng trúng độc gục thì độc lan sang tướng ra thay. " +
                      "Xoá hiệu ứng xấu hay tiến hóa thì hết độc.");
            if (stats.Contains(Stat.Thorns)) l.Add("Phản đòn: phản sát thương của đòn đánh, chiêu, thẻ (không phản bỏng, độc, phản đòn); hạ gục được kẻ đánh.");
            if (kinds.Contains(EffectKind.Execute)) l.Add("Kết liễu: boss không bị hạ gục ngay mà nhận sát thương ×2.");
            if (kinds.Contains(EffectKind.Empower))
                l.Add("Cường hóa: thẻ kế tiếp trong hàng thẻ lượt này mạnh hơn (bỏ qua Gương Đôi, thẻ cường hóa khác cộng dồn); xếp cuối hàng thì mất.");
            if (kinds.Contains(EffectKind.Resonance)) l.Add("Cộng hưởng: đếm cả tướng dự bị cùng hệ còn sống; lính không tính.");
            return string.Join(" ", l);
        }

        // độc: số lớp tối đa (Battle dùng chung)
        public const int PoisonMax = 5;

        // ---------- tên cho màn trận (thay chuỗi điều kiện ở Game/Battle) ----------

        // tên chỉ số viết hoa đầu (chữ nổi khi có buff)
        public static string StatLabel(Stat s)
        {
            switch (s)
            {
                case Stat.Atk: return "Công";
                case Stat.Def: return "Thủ";
                case Stat.Crit: return "Chí mạng";
                case Stat.Lifesteal: return "Hút máu";
                case Stat.Dodge: return "Né";
                case Stat.Thorns: return "Phản đòn";
                case Stat.HealTaken: return "Hồi máu nhận";
                default: return "Sát thương nhận";
            }
        }

        // buff này có lợi cho người mang không (sát thương nhận: âm là lợi)
        public static bool StatUp(Stat s, double v) => s == Stat.DmgTaken ? v < 0 : v > 0;

        public static bool StatusBad(StatusId id) => id == StatusId.Burn || id == StatusId.Stun || id == StatusId.Poison;

        // nhãn ngắn trên chip trạng thái
        public static string StatusLabel(StatusId id)
        {
            switch (id)
            {
                case StatusId.Burn: return "Bỏng";
                case StatusId.Stun: return "Choáng";
                case StatusId.Regen: return "Hồi";
                case StatusId.Poison: return "Độc";
                default: return "Né";
            }
        }

        // chữ nổi khi dính trạng thái
        public static string StatusFloat(StatusId id)
        {
            switch (id)
            {
                case StatusId.Burn: return "Bỏng!";
                case StatusId.Stun: return "Choáng!";
                case StatusId.Regen: return "Hồi phục";
                case StatusId.Poison: return "Trúng độc!";
                default: return "Sẵn sàng né";
            }
        }

        // luật tiến hóa của boss (đầu mục đối thủ ở hộp chuẩn bị), 2026-11-17: gục thì tiến hóa thay vì dưới 25% máu
        public static string EvoRuleShort(CardDef evo)
        {
            double heal = evo != null && evo.Effects.Count > 0 && evo.Effects[0].K == EffectKind.Evolve ? evo.Effects[0].Pct : 1;
            return $"gục thì tiến hóa, dạng sau vào trận {(heal >= 1 ? "đầy máu" : $"với {Pct(heal)} máu")}";
        }

        public static string Pct(double x) => $"{Js.RoundInt(x * 100)}%";

        static string LowFirst(string t) => t.Length == 0 ? t : char.ToLowerInvariant(t[0]) + t.Substring(1);

        // nhánh lồng của cơ chế 2026-11-17: mọi vế viết thường đầu (ifLow cũ giữ nguyên để khớp golden cardtext)
        static string LowList(List<Effect> l) => string.Join(", ", l.Select(x => LowFirst(EffectText(x))));

        static string StatName(Stat s)
        {
            switch (s)
            {
                case Stat.Atk: return "Công";
                case Stat.Def: return "Thủ";
                case Stat.Crit: return "chí mạng";
                case Stat.Lifesteal: return "hút máu";
                case Stat.Dodge: return "né";
                case Stat.Thorns: return "phản đòn";
                case Stat.HealTaken: return "máu được hồi";
                default: return "sát thương nhận";
            }
        }

        // Buff thủ (def, dmgTaken, dodge, thorns) mặc định che tới đầu lượt sau, buff khác hết cuối lượt.
        public static Until DefaultUntil(Stat s) =>
            s == Stat.Def || s == Stat.DmgTaken || s == Stat.Dodge || s == Stat.Thorns ? Until.Start : Until.End;

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
                    if (e.Stat == Stat.Thorns) return $"Phản {Pct(e.V)} sát thương nhận về kẻ đánh{t}";
                    if (e.Stat == Stat.HealTaken)
                    {
                        if (foe) return e.V <= -1 ? $"Địch không hồi được máu{t}" : $"Địch giảm {Pct(Math.Abs(e.V))} máu được hồi{t}";
                        return $"{sign}{Pct(Math.Abs(e.V))} máu được hồi{t}";
                    }
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
                    if (e.Missing.HasValue && e.Missing.Value != 0) s += $", mạnh thêm tới {Pct(e.Missing.Value)} theo máu đã mất";
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
                        case StatusId.Poison:
                        {
                            int k = e.Stacks ?? 1;
                            return k <= 1
                                ? $"{c}Tẩm độc địch thêm 1 lớp ({Pct(e.V)} Công sát thương mỗi lượt, cộng dồn tới {PoisonMax} lớp), {e.Turns} lượt"
                                : $"{c}Tẩm độc địch thêm {k} lớp (mỗi lớp {Pct(e.V)} Công sát thương mỗi lượt, tối đa {PoisonMax} lớp), {e.Turns} lượt";
                        }
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
                case EffectKind.Evolve:
                    // 2026-11-17: gục thì tiến hóa (trước: máu dưới 25%)
                    return $"Tiến hóa, dạng sau vào trận {(e.Pct >= 1 ? "đầy máu" : $"với {Pct(e.Pct)} máu")}, máu và Công tăng";
                case EffectKind.Execute:
                    return $"Gây {Pct(e.Mult)} Công sát thương. Địch dưới {Pct(e.Below)} máu: hạ gục luôn (boss: sát thương ×2)";
                case EffectKind.Combo:
                    return $"Mỗi thẻ {GroupName(e.Group)} khác trong hàng thẻ lượt này: {LowList(e.Then)}";
                case EffectKind.Resonance:
                    return $"Mỗi tướng cùng hệ còn sống trong đội (kể cả mình, không tính lính): {LowList(e.Then)}";
                case EffectKind.IfBeat:
                    return $"Khắc hệ địch: {LowList(e.Then)}" + (e.Else != null ? $". Không thì: {LowList(e.Else)}" : "");
                case EffectKind.Empower:
                    return $"Thẻ kế tiếp trong hàng mạnh thêm {Pct(e.V)}";
                case EffectKind.Detonate:
                    return e.Mult == 1 ? "Kích nổ độc trên địch: gây ngay toàn bộ máu độc còn lại, xoá độc"
                        : $"Kích nổ độc trên địch: gây ngay {Pct(e.Mult)} số máu độc còn lại, xoá độc";
                case EffectKind.Bash:
                    return e.Mult == 1 ? "Tiêu hết khiên, gây sát thương bằng số khiên đã tiêu"
                        : $"Tiêu hết khiên, gây sát thương bằng {Pct(e.Mult)} số khiên đã tiêu";
            }
            return "";
        }

        public static string Text(CardDef c, int lv, double cardLvStep)
        {
            string body = string.Join(". ", ScaleEffects(c.Effects, lv, cardLvStep).Select(EffectText));
            if (c.kind != CardKind.Passive) return body + ".";
            string low = LowFirst(body);
            if (c.Effects.Count > 0 && c.Effects[0].K == EffectKind.Evolve) return $"Khi gục, nếu còn dạng sau: {low}.";
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
                case PassiveTrigger.OnHit:
                {
                    // có tỉ lệ thì ghi tỉ lệ (trước 2026-11-05 chữ thiếu tỉ lệ, vd. Cá Nóc "bị đánh có 30% gây bỏng")
                    if (!c.hasChance) return $"Mỗi lần bị đánh: {low}.";
                    double ch = Math.Min(1, c.chance * LvFactor(cardLvStep, lv));
                    return $"Mỗi lần bị đánh: {Pct(ch)} cơ hội {low}.";
                }
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
