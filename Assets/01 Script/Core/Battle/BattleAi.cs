// Máy chơi: chấm điểm thẻ theo tình huống, chép đúng Web/src/core/ai.ts.
// Dùng cho địch, cho nút "Tự chơi" và cho máy tự chơi đo cân bằng.
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    public static class BattleAi
    {
        static double Value(Battle b, Fighter me, Fighter foe, List<Effect> effects)
        {
            var cfg = b.Data.Cfg;
            double hpR = me.hp / me.maxHp;
            var sk = b.InnateCard(me, InnateKind.Skill).card;
            double manaNeed = sk.costMana - me.mana;
            bool ultSoon = me.rage >= cfg.maxRage - 20 || b.turn.ult != null;
            double v = 0;
            foreach (var e in effects)
            {
                switch (e.K)
                {
                    case EffectKind.Buff:
                    {
                        double turns = e.Turns >= 99 ? 4 : e.Turns;
                        if (e.On == Target.Foe)
                        {
                            if (e.Stat == Stat.Def) v += -e.V * 55 * turns * 0.8;
                            else if (e.Stat == Stat.Atk) v += -e.V * 50;
                            else v += Math.Abs(e.V) * 30;
                        }
                        else if (e.Stat == Stat.Atk) v += e.V * 60 * (ultSoon ? 1.6 : 1) * (turns > 1 ? 1.5 : 1);
                        else if (e.Stat == Stat.Def) v += e.V * 50 * (hpR < 0.5 ? 1.6 : 1) * (e.V < 0 && hpR < 0.4 ? 2 : 1) * turns * 0.8;
                        else if (e.Stat == Stat.Crit) v += e.V * 45;
                        else if (e.Stat == Stat.Lifesteal) v += e.V * 60 * (1.3 - hpR);
                        else v += Math.Abs(e.V) * 40;
                        break;
                    }
                    case EffectKind.Heal:
                        v += Math.Min(e.Pct, 1 - hpR) * 140 + (hpR < 0.35 ? 25 : 0);
                        break;
                    case EffectKind.MaxHp:
                        v += e.Pct * 70;
                        break;
                    case EffectKind.SelfDmg:
                        v -= e.PctCur * hpR * 120 * (hpR < 0.4 ? 2.5 : 1);
                        break;
                    case EffectKind.Mana:
                        v += e.On == Target.Foe ? Math.Abs(e.V) * 0.5 : e.V * (manaNeed > 0 ? 0.9 : 0.25);
                        break;
                    case EffectKind.Rage:
                        v += e.On == Target.Foe ? Math.Abs(e.V) * 0.5 : e.V * (me.rage < cfg.maxRage ? 0.8 : 0.1);
                        break;
                    case EffectKind.Dmg:
                        v += e.Mult * (e.Hits ?? 1) * 45 * Battle.ElemMult(me, foe);
                        break;
                    case EffectKind.Shield:
                        v += e.Pct * 110 * (hpR < 0.6 ? 1.3 : 1);
                        break;
                    case EffectKind.Status:
                        if (e.Status == StatusId.Burn) v += e.Turns * e.V * 100 * 1.3 * (foe.hp / foe.maxHp + 0.2);
                        else if (e.Status == StatusId.Stun) v += 55 * (e.Chance ?? 1);
                        else if (e.Status == StatusId.Regen) v += e.Turns * e.V * 100 * (1.4 - hpR);
                        else if (e.Status == StatusId.Evade) v += 35 * (hpR < 0.5 ? 1.5 : 1);
                        break;
                    case EffectKind.Cleanse:
                    {
                        int bad = me.buffs.FindAll(x => x.v < 0).Count +
                                  me.statuses.FindAll(x => x.id == StatusId.Burn || x.id == StatusId.Stun).Count;
                        v += bad * 25;
                        break;
                    }
                    case EffectKind.Double:
                        v += b.turn.picksLeft > 1 ? 30 : 0;
                        break;
                    case EffectKind.Extra:
                        v += e.Mult * 50;
                        break;
                    case EffectKind.TrueStrike:
                        v += 45 * e.Mult * (1 + foe.def / 100);
                        break;
                    case EffectKind.IfLow:
                        v += Value(b, me, foe, hpR < e.Below ? e.Then : e.Else ?? new List<Effect>());
                        break;
                }
            }
            return v;
        }

        public static int PickIndex(Battle b, double noise = 0.12)
        {
            int s = b.turn.side;
            var me = b.ActiveOf(s);
            var foe = b.ActiveOf(1 - s);
            int best = 0;
            double bestV = double.NegativeInfinity;
            for (int i = 0; i < b.turn.offer.Count; i++)
            {
                double v = Value(b, me, foe, b.Data.Card(b.turn.offer[i]).Effects) * b.rng.Range(1 - noise, 1 + noise);
                if (v > bestV)
                {
                    bestV = v;
                    best = i;
                }
            }
            return best;
        }

        // gọi trước mỗi lần chọn; trả về chiêu hoặc tuyệt kỹ nên dùng ngay (nếu có)
        public static InnateKind? Innate(Battle b)
        {
            var t = b.turn;
            var cfg = b.Data.Cfg;
            if (b.InnateBlock(InnateKind.Ult) == "") return InnateKind.Ult;
            if (b.InnateBlock(InnateKind.Skill) == "")
            {
                var me = b.ActiveOf(t.side);
                var ult = b.InnateCard(me, InnateKind.Ult).card;
                // để dành mana cho tuyệt kỹ nếu nộ sắp đầy
                double reserve = me.rage >= cfg.maxRage - 15 && t.ult == null ? ult.costMana : 0;
                var sk = b.InnateCard(me, InnateKind.Skill);
                if (me.mana - sk.card.costMana < reserve) return null;
                // chiêu ra ngay, thẻ đã xếp chỉ chạy cuối lượt: chờ trong lượt không mạnh hơn, dùng luôn
                return InnateKind.Skill;
            }
            return null;
        }

        // đầu lượt: có nên đổi tướng không (trả về chỉ số, -1 là không)
        public static int SwapChoice(Battle b)
        {
            int s = b.turn.side;
            var side = b.sides[s];
            var me = b.ActiveOf(s);
            var foe = b.ActiveOf(1 - s);
            double hpR = me.hp / me.maxHp;
            int best = -1;
            double bestScore = 0;
            for (int i = 0; i < side.fighters.Count; i++)
            {
                var f = side.fighters[i];
                if (f.dead || i == side.active) continue;
                double r = f.hp / f.maxHp;
                double sc = 0;
                if (hpR < 0.25 && r > 0.5) sc = 1 + r;
                bool weakNow = Battle.ElemMult(foe, me) > 1;
                bool okThere = Battle.ElemMult(foe, f) <= 1 && Battle.ElemMult(f, foe) >= 1;
                if (weakNow && okThere && r > 0.6) sc = Math.Max(sc, 0.8 + r * 0.5);
                if (sc > bestScore)
                {
                    bestScore = sc;
                    best = i;
                }
            }
            if (best >= 0 && b.rng.Chance(0.55)) return best;
            return -1;
        }

        // cả lượt của máy, trừ phần chạy thẻ (để màn trận tự gọi Execute)
        public static List<BattleEvent> Turn(Battle b, double noise = 0.12)
        {
            var outL = new List<BattleEvent>();
            int sw = SwapChoice(b);
            if (sw >= 0) outL.AddRange(b.Swap(sw));
            while (b.phase == Phase.Picking)
            {
                var inn = Innate(b);
                if (inn.HasValue)
                {
                    // chiêu hạ đối thủ thì hết lúc chọn (vòng tự dừng)
                    outL.AddRange(b.UseInnate(inn.Value));
                    continue;
                }
                outL.AddRange(b.Pick(PickIndex(b, noise)));
            }
            return outL;
        }

        // giá trị một thẻ cho tướng đang ra sân (để gợi ý)
        public static double CardValue(Battle b, string id, int lv = 1)
        {
            int s = b.turn.side;
            var c = b.Data.Card(id);
            return Value(b, b.ActiveOf(s), b.ActiveOf(1 - s), CardText.ScaleEffects(c.Effects, lv, b.Data.Cfg.cardLvStep));
        }

        // Độ khéo của địch theo ải: ải đầu chọn kém (nhiễu lớn), về sau 0,12 như tự chơi.
        public static double EnemyNoise(int stageId) => Math.Max(0.12, 0.6 - 0.05 * stageId);
    }

    // Máy tự chơi cả trận (cả hai bên do máy chọn), chép Web/src/core/sim.ts.
    public static class BattleSim
    {
        public static Battle Run(Battle b, double noise = 0.15, List<BattleEvent> log = null)
        {
            var evs = b.StartBattle();
            log?.AddRange(evs);
            int guard = 0;
            while (b.phase != Phase.Over && guard++ < 2000)
            {
                if (b.phase == Phase.ForceSwap)
                {
                    evs = b.ForceSwap(b.AiForcedChoice(b.turn.side));
                    log?.AddRange(evs);
                    continue;
                }
                if (b.phase == Phase.Picking)
                {
                    evs = BattleAi.Turn(b, noise);
                    log?.AddRange(evs);
                    evs = b.Execute();
                    log?.AddRange(evs);
                    continue;
                }
                evs = b.Advance();
                log?.AddRange(evs);
            }
            return b;
        }
    }
}
