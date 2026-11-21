// Mô tả thẻ bằng tiếng Anh (2026-11-21), cùng luật và số với CardText (tiếng Việt, khớp golden). CardText gọi sang đây khi Loc.IsEn.
// Câu tiếng Anh viết riêng (không ghép từ mảnh tiếng Việt) vì thứ tự từ, số nhiều và cách nối vế khác nhau.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public static class CardTextEn
    {
        static string Pct(double x) => CardText.Pct(x);

        static string Num(double x) => Js.Num(x);

        static string Turns(int n) => n == 1 ? "1 turn" : $"{n} turns";

        static string LowFirst(string t) => t.Length == 0 ? t : char.ToLowerInvariant(t[0]) + t.Substring(1);

        static string LowList(List<Effect> l) => string.Join(", ", l.Select(x => LowFirst(EffectText(x))));

        public static string GroupName(CardGroup g) => g == CardGroup.Atk ? "attack" : g == CardGroup.Def ? "defense" : "healing";

        public static string Note(HashSet<EffectKind> kinds, HashSet<StatusId> st, HashSet<Stat> stats, HashSet<CardGroup> groups)
        {
            var l = new List<string>();
            foreach (var g in groups)
                l.Add(g == CardGroup.Atk ? "Attack cards: cards that deal damage (including extra strikes, execute, poison detonation, shield bash)."
                    : g == CardGroup.Def ? "Defense cards: shields, DEF up, damage taken down, dodge, thorns."
                    : "Healing cards: heal, regen, max HP up, cleanse.");
            if (st.Contains(StatusId.Poison) || kinds.Contains(EffectKind.Detonate))
                l.Add($"Poison stacks up to {CardText.PoisonMax} times; each new stack resets the duration. If a poisoned hero is knocked out, the poison spreads to the hero who comes in. " +
                      "Cleansing or evolving removes poison.");
            if (stats.Contains(Stat.Thorns)) l.Add("Thorns: reflects damage from basic attacks, skills and cards (not burn, poison or thorns); can knock out the attacker.");
            if (kinds.Contains(EffectKind.Execute)) l.Add("Execute: bosses are not knocked out instantly, they take ×2 damage instead.");
            if (kinds.Contains(EffectKind.Empower))
                l.Add("Empower: the next card in this turn's lineup is stronger (skips Twin Mirror; other empower cards stack); lost if placed last.");
            if (kinds.Contains(EffectKind.Resonance)) l.Add("Resonance: also counts living benched heroes of the same element; minions don't count.");
            return string.Join(" ", l);
        }

        public static string StatLabel(Stat s)
        {
            switch (s)
            {
                case Stat.Atk: return "ATK";
                case Stat.Def: return "DEF";
                case Stat.Crit: return "Crit";
                case Stat.Lifesteal: return "Lifesteal";
                case Stat.Dodge: return "Dodge";
                case Stat.Thorns: return "Thorns";
                case Stat.HealTaken: return "Healing";
                default: return "Damage taken";
            }
        }

        public static string StatusLabel(StatusId id)
        {
            switch (id)
            {
                case StatusId.Burn: return "Burn";
                case StatusId.Stun: return "Stun";
                case StatusId.Regen: return "Regen";
                case StatusId.Poison: return "Poison";
                default: return "Dodge";
            }
        }

        public static string StatusFloat(StatusId id)
        {
            switch (id)
            {
                case StatusId.Burn: return "Burned!";
                case StatusId.Stun: return "Stunned!";
                case StatusId.Regen: return "Regen";
                case StatusId.Poison: return "Poisoned!";
                default: return "Ready to dodge";
            }
        }

        public static string EvoRuleShort(double heal) =>
            $"evolves when knocked out, next form enters {(heal >= 1 ? "at full HP" : $"with {Pct(heal)} HP")}";

        static string StatName(Stat s)
        {
            switch (s)
            {
                case Stat.Atk: return "ATK";
                case Stat.Def: return "DEF";
                case Stat.Crit: return "crit";
                case Stat.Lifesteal: return "lifesteal";
                case Stat.Dodge: return "dodge";
                case Stat.Thorns: return "thorns";
                case Stat.HealTaken: return "healing received";
                default: return "damage taken";
            }
        }

        static string TurnsText(int turns, Until until, bool foe)
        {
            if (turns >= 99) return " for the whole battle";
            if (foe) return $" for {Turns(turns)}";
            if (until == Until.Start) return turns == 1 ? " until your next turn" : $" for {turns} enemy turns";
            return turns == 1 ? " this turn" : $" for {Turns(turns)}";
        }

        public static string EffectText(Effect e)
        {
            switch (e.K)
            {
                case EffectKind.Buff:
                {
                    bool foe = e.On == Target.Foe;
                    var until = e.Until ?? CardText.DefaultUntil(e.Stat);
                    string sign = e.V >= 0 ? "+" : "−";
                    string t = TurnsText(e.Turns, until, foe);
                    if (e.Stat == Stat.Lifesteal) return $"Heal for {Pct(e.V)} of damage dealt{t}";
                    if (e.Stat == Stat.Dodge) return $"{Pct(e.V)} chance to dodge basic attacks{t}";
                    if (e.Stat == Stat.DmgTaken) return $"Take {Pct(Math.Abs(e.V))} {(e.V < 0 ? "less" : "more")} damage{t}";
                    if (e.Stat == Stat.Thorns) return $"Reflect {Pct(e.V)} of damage taken back to the attacker{t}";
                    if (e.Stat == Stat.HealTaken)
                    {
                        if (foe) return e.V <= -1 ? $"Enemy can't heal{t}" : $"Enemy healing received −{Pct(Math.Abs(e.V))}{t}";
                        return $"{sign}{Pct(Math.Abs(e.V))} healing received{t}";
                    }
                    return $"{(foe ? "Enemy " : "")}{sign}{Pct(Math.Abs(e.V))} {StatName(e.Stat)}{t}";
                }
                case EffectKind.Heal:
                    return $"Heal {Pct(e.Pct)} HP";
                case EffectKind.MaxHp:
                    return $"+{Pct(e.Pct)} max HP for the whole battle";
                case EffectKind.SelfDmg:
                    return $"Lose {Pct(e.PctCur)} of current HP";
                case EffectKind.Mana:
                    if (e.On == Target.Foe) return $"Drain {Num(Math.Abs(e.V))} mana from the enemy";
                    return $"+{Num(e.V)} mana";
                case EffectKind.Rage:
                    if (e.On == Target.Foe) return $"Drain {Num(Math.Abs(e.V))} rage from the enemy";
                    return $"+{Num(e.V)} rage";
                case EffectKind.Dmg:
                {
                    string s = e.Hits.HasValue && e.Hits.Value > 1
                        ? $"Hit {e.Hits.Value} times for {Pct(e.Mult)} ATK each"
                        : $"Deal {Pct(e.Mult)} ATK damage";
                    if (e.Pierce.HasValue && e.Pierce.Value != 0) s += $", ignoring {Pct(e.Pierce.Value)} DEF";
                    if (e.Lifesteal.HasValue && e.Lifesteal.Value != 0) s += $", healing for {Pct(e.Lifesteal.Value)} of it";
                    if (e.Missing.HasValue && e.Missing.Value != 0) s += $", up to {Pct(e.Missing.Value)} stronger based on HP lost";
                    return s;
                }
                case EffectKind.Shield:
                    return $"Gain a shield equal to {Pct(e.Pct)} max HP";
                case EffectKind.Status:
                {
                    string s = StatusText(e);
                    // "30% chance to stun the enemy"
                    return s.Length > 0 && e.Chance.HasValue && e.Chance.Value != 0 && e.Chance.Value < 1 ? $"{Pct(e.Chance.Value)} chance to {LowFirst(s)}" : s;
                }
                case EffectKind.Cleanse:
                    return "Remove negative effects";
                case EffectKind.Double:
                    return "The next card triggers twice";
                case EffectKind.Extra:
                    return $"At the end of the turn, strike again for {Pct(e.Mult)} ATK";
                case EffectKind.TrueStrike:
                    return $"This turn's basic attack ignores DEF, ×{Num(e.Mult)}";
                case EffectKind.IfLow:
                    return $"HP below {Pct(e.Below)}: {LowFirst(string.Join(", ", e.Then.Select(EffectText)))}" +
                           (e.Else != null ? $". Otherwise: {LowFirst(string.Join(", ", e.Else.Select(EffectText)))}" : "");
                case EffectKind.Revive:
                    return $"Revive with {Pct(e.Pct)} HP";
                case EffectKind.Evolve:
                    return $"Evolve into the next form {(e.Pct >= 1 ? "at full HP" : $"with {Pct(e.Pct)} HP")}, gaining HP and ATK";
                case EffectKind.Execute:
                    return $"Deal {Pct(e.Mult)} ATK damage. Enemy below {Pct(e.Below)} HP: knocked out instantly (boss: ×2 damage)";
                case EffectKind.Combo:
                    return $"For each other {GroupName(e.Group)} card in this turn's lineup: {LowList(e.Then)}";
                case EffectKind.Resonance:
                    return $"For each living hero of the same element on the team (including itself, minions excluded): {LowList(e.Then)}";
                case EffectKind.IfBeat:
                    return $"Element advantage: {LowList(e.Then)}" + (e.Else != null ? $". Otherwise: {LowList(e.Else)}" : "");
                case EffectKind.Empower:
                    return $"The next card in the lineup is {Pct(e.V)} stronger";
                case EffectKind.Detonate:
                    return e.Mult == 1 ? "Detonate the enemy's poison: deal all remaining poison damage now, then remove it"
                        : $"Detonate the enemy's poison: deal {Pct(e.Mult)} of the remaining poison damage now, then remove it";
                case EffectKind.Bash:
                    return e.Mult == 1 ? "Consume all shield and deal damage equal to the shield consumed"
                        : $"Consume all shield and deal damage equal to {Pct(e.Mult)} of the shield consumed";
            }
            return "";
        }

        static string StatusText(Effect e)
        {
            switch (e.Status)
            {
                case StatusId.Burn: return $"Burn the enemy for {Turns(e.Turns)} ({Pct(e.V)} HP per turn)";
                case StatusId.Regen: return $"Regenerate {Pct(e.V)} HP at the start of each turn for {Turns(e.Turns)}";
                case StatusId.Stun: return "Stun the enemy";
                case StatusId.Evade: return "Fully dodge the next basic attack";
                case StatusId.Poison:
                {
                    int k = e.Stacks ?? 1;
                    return k <= 1
                        ? $"Poison the enemy +1 stack ({Pct(e.V)} ATK damage per turn, stacks up to {CardText.PoisonMax}) for {Turns(e.Turns)}"
                        : $"Poison the enemy +{k} stacks ({Pct(e.V)} ATK damage per stack per turn, up to {CardText.PoisonMax} stacks) for {Turns(e.Turns)}";
                }
            }
            return "";
        }

        public static string Text(CardDef c, int lv, double cardLvStep)
        {
            string body = string.Join(". ", CardText.ScaleEffects(c.Effects, lv, cardLvStep).Select(EffectText));
            if (c.kind != CardKind.Passive) return body + ".";
            string low = LowFirst(body);
            if (c.Effects.Count > 0 && c.Effects[0].K == EffectKind.Evolve) return $"When knocked out, if a next form exists: {low}.";
            switch (c.trigger)
            {
                case PassiveTrigger.Start: return $"Battle start: {low}.";
                case PassiveTrigger.TurnStart: return $"Start of each turn: {low}.";
                case PassiveTrigger.LowHp: return $"First time HP drops below {Pct(c.below)}: {low}.";
                case PassiveTrigger.OnAttack:
                {
                    double ch = Math.Min(1, (c.Chance ?? 1) * CardText.LvFactor(cardLvStep, lv));
                    return $"Each basic attack: {Pct(ch)} chance to {low}.";
                }
                case PassiveTrigger.OnHit:
                {
                    if (!c.hasChance) return $"When hit: {low}.";
                    double ch = Math.Min(1, c.chance * CardText.LvFactor(cardLvStep, lv));
                    return $"When hit: {Pct(ch)} chance to {low}.";
                }
                case PassiveTrigger.Death: return $"First time knocked out: {low}.";
            }
            return body + ".";
        }

        public static string CostText(CardDef c)
        {
            var parts = new List<string>();
            if (c.costRage > 0) parts.Add($"{c.costRage} rage");
            if (c.costMana > 0) parts.Add($"{c.costMana} mana");
            return string.Join(" + ", parts);
        }
    }
}
