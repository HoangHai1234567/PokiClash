// Trận theo lượt, luân phiên, gốc là Web/src/core/battle.ts (cùng hạt giống, cùng lựa chọn thì cùng chuỗi sự kiện).
// Khác bản web từ 2026-11-03: chiêu ra ngay lúc bấm, không vào hàng thẻ.
// Mỗi hiệp: người chơi (bên 0) đi trước. Mỗi lượt:
//   1. đầu lượt (trước lần chọn đầu) được đổi tướng;
//   2. chọn 5 lần, mỗi lần 1 trong 3 thẻ chung; chiêu và tuyệt kỹ dùng xen vào lúc chọn, không tốn lần chọn.
//      Chiêu ra đòn ngay rồi chọn tiếp, tuyệt kỹ thay cú đánh thường cuối lượt;
//   3. thẻ chạy lần lượt theo thứ tự xếp, rồi đánh thường (hoặc tuyệt kỹ nếu đã bật).
// Mọi hàm hành động trả về danh sách sự kiện (kèm ảnh chụp số liệu) để màn trận chiếu lại.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class Battle
    {
        public readonly GameData Data;
        BalanceConfig Cfg => Data.Cfg;

        public Rng rng;
        public uint seed;
        public Side[] sides;
        public int round;
        public int[] order = { 0, 1 };
        public int step = 2; // 0, 1 trong hiệp; 2 = hết hiệp
        public Turn turn;
        public Phase phase = Phase.Idle;
        public bool resumeTurn; // hộp chọn tướng thay xong thì: false = tiến trận, true = chạy tiếp lượt
        public int winner = -1;
        public int turns;
        public double[] dmgDealt = { 0, 0 };
        readonly List<BattleEvent> events = new List<BattleEvent>();

        Battle(GameData data)
        {
            Data = data;
        }

        public static int Other(int s) => s == 0 ? 1 : 0;

        public Fighter ActiveOf(int s) => sides[s].fighters[sides[s].active];

        // ---------- chỉ số ----------

        // chỉ số: HeroStats.Compute (một nguồn cho trận và màn Tướng)

        // boss có thẻ Tiến Hóa: hệ số máu, Công của dạng i trong dòng n dạng (Cfg.bossEvoHp, bossEvoAtk). Dòng 1 dạng không tiến hóa
        // nhưng vẫn gánh đủ máu của cả dòng.
        public static (double hp, double atk) EvoMult(BalanceConfig cfg, int n, int i) =>
            (cfg.bossEvoHp * (i + 1) * 2 / (n * (n + 1)), 1 - cfg.bossEvoAtk * (n - 1 - i));

        Fighter MakeFighter(Member m, int side, int idx)
        {
            var hero = Data.Hero(m.heroId);
            var s = HeroStats.Compute(Cfg, hero, m.level, m.star, m.boss, m.mods);
            var st = m.start;
            // boss có thẻ Tiến Hóa vào trận ở dạng 1, yếu nhất
            var k = m.evo ? EvoMult(Cfg, Math.Max(1, hero.forms.Length), 0) : (hp: 1.0, atk: 1.0);
            double hp = m.evo ? Js.Round(s.hp * k.hp) : s.hp;
            var f = new Fighter
            {
                idx = idx, side = side, hero = hero, level = m.level, star = m.star,
                cardSkill = m.cardSkill, cardUlt = m.cardUlt, cardPassive = m.cardPassive, boss = m.boss,
                evo = m.evo, form = m.evo ? 0 : hero.FormIndex(Cfg.formStars, m.star), partner = m.partner,
                maxHp = hp, hp = hp, atk = m.evo ? Js.Round(s.atk * k.atk) : s.atk, def = s.def, spd = s.spd,
                mana = st != null ? Math.Min(Cfg.maxMana, st.mana) : 0, rage = st != null ? Math.Min(Cfg.maxRage, st.rage) : 0,
            };
            // tiềm năng chí mạng, hút máu: buff cả trận (left ≥ 99 không giảm)
            if (st != null && st.crit != 0) f.buffs.Add(new Buff { stat = Stat.Crit, v = st.crit, left = 99, until = Until.End });
            if (st != null && st.lifesteal != 0) f.buffs.Add(new Buff { stat = Stat.Lifesteal, v = st.lifesteal, left = 99, until = Until.End });
            return f;
        }

        // khắc hệ giữa hai tướng trên sân (tướng đồng hành không chịu thiệt, Elements.Mult)
        public static double ElemMult(Fighter a, Fighter d) => Elements.Mult(a.hero.elem, d.hero.elem, a.partner, d.partner);

        public static double BuffSum(Fighter f, Stat stat)
        {
            double v = 0;
            foreach (var x in f.buffs)
                if (x.stat == stat) v += x.v;
            return v;
        }

        Snap TakeSnap()
        {
            var sn = new Snap { active = new[] { sides[0].active, sides[1].active } };
            for (int s = 0; s < 2; s++)
                foreach (var f in sides[s].fighters)
                {
                    var fs = new FSnap
                    {
                        hp = f.hp, maxHp = f.maxHp, shield = f.shield, mana = f.mana, rage = f.rage, dead = f.dead,
                        atkB = BuffSum(f, Stat.Atk), defB = BuffSum(f, Stat.Def),
                    };
                    foreach (var x in f.statuses) fs.st.Add((x.id, x.left));
                    sn.f[s].Add(fs);
                }
            return sn;
        }

        void Emit(BattleEvent e)
        {
            e.snap = TakeSnap();
            events.Add(e);
        }

        List<BattleEvent> Flush()
        {
            var l = new List<BattleEvent>(events);
            events.Clear();
            return l;
        }

        // ---------- tạo trận ----------

        public static Battle Create(GameData data, TeamSetup t0, TeamSetup t1, uint seed, int unlock0 = 99, int unlock1 = 99)
        {
            var b = new Battle(data) { rng = new Rng(seed), seed = seed };
            var teams = new[] { t0, t1 };
            var unlock = new[] { unlock0, unlock1 };
            b.sides = new Side[2];
            for (int s = 0; s < 2; s++)
            {
                var side = new Side { name = teams[s].name, ai = teams[s].ai, unlock = unlock[s] };
                for (int i = 0; i < teams[s].members.Count; i++) side.fighters.Add(b.MakeFighter(teams[s].members[i], s, i));
                b.sides[s] = side;
            }
            b.turn = b.EmptyTurn(0);
            return b;
        }

        Turn EmptyTurn(int side) => new Turn { side = side, picksTotal = Cfg.picks, picksLeft = Cfg.picks };

        // bị động "vào trận" của mọi tướng, rồi vào hiệp đầu
        public List<BattleEvent> StartBattle()
        {
            Emit(new BattleEvent { t = EvType.Start });
            for (int s = 0; s < 2; s++)
                foreach (var f in sides[s].fighters.ToList()) RunPassive(f, PassiveTrigger.Start);
            AdvanceInner();
            return Flush();
        }

        // ---------- tiến trận ----------

        public List<BattleEvent> Advance()
        {
            AdvanceInner();
            return Flush();
        }

        void AdvanceInner()
        {
            if (phase == Phase.Over) return;
            for (int s = 0; s < 2; s++)
            {
                var side = sides[s];
                if (!side.needSwap) continue;
                if (side.ai) DoSwap(s, AiForcedChoice(s), true);
                else
                {
                    phase = Phase.ForceSwap;
                    resumeTurn = false;
                    turn = EmptyTurn(s);
                    return;
                }
            }
            if (step >= 2)
            {
                if (round >= Cfg.maxRounds)
                {
                    TimeOut();
                    return;
                }
                round++;
                // người chơi luôn đi trước mỗi hiệp (chốt 2026-10-31)
                const int first = 0;
                order = new[] { first, Other(first) };
                step = 0;
                Emit(new BattleEvent { t = EvType.Round, round = round, first = first });
            }
            BeginTurn(order[step]);
        }

        void BeginTurn(int s)
        {
            turn = EmptyTurn(s);
            turns++;
            Emit(new BattleEvent { t = EvType.Turn, side = s });
            var f = ActiveOf(s);
            // buff thủ (hết khi tới lượt chủ), né chưa dùng thì mất
            TickBuffs(s, Until.Start);
            f.statuses = f.statuses.Where(x => x.id != StatusId.Evade).ToList();
            // bỏng, hồi phục
            foreach (var st in f.statuses.ToList())
            {
                if (st.id == StatusId.Burn)
                {
                    double d = Math.Max(1, Js.Round(f.maxHp * st.v));
                    double toHp = Math.Min(f.hp, d);
                    if (CanEvolve(f) && toHp >= f.hp) toHp = f.hp - 1; // còn dạng sau: chừa 1 máu, tiến hóa ở CheckLow đầu lượt
                    f.hp -= toHp;
                    Emit(new BattleEvent
                    {
                        t = EvType.Dmg, from = Other(s), to = s, amount = d, toHp = toHp, blocked = 0, crit = false, elem = 1, dmgKind = DmgKind.Burn,
                    });
                }
                else if (st.id == StatusId.Regen) Heal(f, st.v);
                if (st.id == StatusId.Burn || st.id == StatusId.Regen) st.left--;
            }
            f.statuses = f.statuses.Where(x => x.left > 0).ToList();
            if (f.hp <= 0) Kill(f);
            if (f.dead)
            {
                if (winner >= 0) return;
                var side = sides[s];
                if (side.ai) DoSwap(s, AiForcedChoice(s), true);
                else
                {
                    phase = Phase.ForceSwap;
                    resumeTurn = true;
                    return;
                }
            }
            ContinueTurn();
        }

        void ContinueTurn()
        {
            int s = turn.side;
            var f = ActiveOf(s);
            CheckLow(f);
            RunPassive(f, PassiveTrigger.TurnStart);
            AddMana(f, Cfg.manaPerTurn, false);
            foreach (var o in sides[s].fighters)
                if (o != f && !o.dead) o.mana = Math.Min(Cfg.maxMana, o.mana + Cfg.benchMana);
            if (f.Has(StatusId.Stun))
            {
                // choáng: mất trọn lượt (không chọn thẻ, không đổi tướng, không đánh); mana đầu lượt vẫn nhận
                f.statuses = f.statuses.Where(x => x.id != StatusId.Stun).ToList();
                turn.stunned = true;
                turn.picksTotal = turn.picksLeft = 0;
                Emit(new BattleEvent { t = EvType.Stunned, side = s });
                EndTurn(s);
                return;
            }
            turn.offer = DrawOffer(s);
            phase = Phase.Picking;
        }

        public List<string> DrawOffer(int s)
        {
            int unlock = sides[s].unlock;
            var pool = Data.Pool.Where(c => c.unlock <= unlock).ToList();
            var outL = new List<CardDef>();
            while (outL.Count < Cfg.offer && outL.Count < pool.Count)
            {
                var left = pool.Where(c => !outL.Contains(c)).ToList();
                outL.Add(rng.Weighted(left, c => Cfg.PoolWeight(c.rarity)));
            }
            return outL.Select(c => c.id).ToList();
        }

        // ---------- hành động của người chơi (máy cũng gọi các hàm này) ----------

        public bool CanSwap(int idx)
        {
            var t = turn;
            var side = sides[t.side];
            if (phase != Phase.Picking || t.firstPick || t.swapped) return false;
            if (idx < 0 || idx >= side.fighters.Count) return false;
            var f = side.fighters[idx];
            return !f.dead && idx != side.active;
        }

        public List<BattleEvent> Swap(int idx)
        {
            if (!CanSwap(idx)) return new List<BattleEvent>();
            DoSwap(turn.side, idx, false);
            turn.swapped = true;
            // tướng vào sân đầu lượt nhận đủ mana của lượt (lúc ở dự bị mới được phần nhỏ)
            AddMana(ActiveOf(turn.side), Cfg.manaPerTurn - Cfg.benchMana, false);
            return Flush();
        }

        public List<BattleEvent> ForceSwap(int idx)
        {
            int s = turn.side;
            var fs = sides[s].fighters;
            if (phase != Phase.ForceSwap || idx < 0 || idx >= fs.Count || fs[idx].dead) return new List<BattleEvent>();
            DoSwap(s, idx, true);
            if (resumeTurn) ContinueTurn();
            else AdvanceInner();
            return Flush();
        }

        void DoSwap(int s, int idx, bool forced)
        {
            var side = sides[s];
            int from = side.active;
            side.active = idx;
            side.needSwap = false;
            Emit(new BattleEvent { t = EvType.Swap, side = s, from = from, to = idx, forced = forced });
        }

        public List<BattleEvent> Pick(int i)
        {
            var t = turn;
            if (phase != Phase.Picking || i < 0 || i >= t.offer.Count) return new List<BattleEvent>();
            t.queue.Add(new QueueItem { card = t.offer[i], lv = 1 });
            t.firstPick = true;
            t.picksLeft--;
            if (t.picksLeft > 0) t.offer = DrawOffer(t.side);
            else
            {
                t.offer = new List<string>();
                phase = Phase.Ready;
            }
            return Flush();
        }

        public (CardDef card, int lv) InnateCard(Fighter f, InnateKind which)
        {
            var id = which == InnateKind.Skill ? f.hero.skill : f.hero.ult;
            return (Data.Card(id), f.CardLv(which));
        }

        // lý do không dùng được (rỗng là dùng được)
        public string InnateBlock(InnateKind which)
        {
            var t = turn;
            if (phase != Phase.Picking) return "Hết lúc chọn";
            if (t.stunned) return "Đang choáng";
            var f = ActiveOf(t.side);
            var card = InnateCard(f, which).card;
            if (which == InnateKind.Skill && t.skillUsed) return "Đã dùng lượt này";
            if (which == InnateKind.Ult && t.ult != null) return "Đã bật";
            if (card.costRage > f.rage) return "Chưa đủ nộ";
            if (card.costMana > f.mana) return "Chưa đủ mana";
            return "";
        }

        public List<BattleEvent> UseInnate(InnateKind which)
        {
            if (InnateBlock(which) != "") return new List<BattleEvent>();
            var t = turn;
            var f = ActiveOf(t.side);
            var (card, lv) = InnateCard(f, which);
            f.mana -= card.costMana;
            f.rage -= card.costRage;
            t.firstPick = true; // đã ra quyết định: hết lúc đổi tướng
            if (which == InnateKind.Skill) t.skillUsed = true;
            else t.ult = new UltItem { card = card.id, lv = lv };
            Emit(new BattleEvent { t = EvType.Innate, side = t.side, card = card.id, kind = which == InnateKind.Skill ? "skill" : "ult" });
            if (which == InnateKind.Skill)
            {
                // chiêu ra đòn ngay (người dùng 2026-11-03), thẻ đã xếp vẫn chờ cuối lượt
                ApplyEffects(t.side, Scaled(card, lv), DmgKind.Skill);
                // chiêu hạ tướng đối thủ: hết lúc chọn, thẻ đã xếp chạy rồi hết lượt (gục hết đội thì trận đã xong)
                if (winner < 0 && (ActiveOf(t.side).dead || ActiveOf(Other(t.side)).dead))
                {
                    t.offer = new List<string>();
                    phase = Phase.Ready;
                }
            }
            return Flush();
        }

        List<Effect> Scaled(CardDef c, int lv) => CardText.ScaleEffects(c.Effects, lv, Cfg.cardLvStep);

        // chạy hết hàng thẻ, đánh, kết thúc lượt
        public List<BattleEvent> Execute()
        {
            if (phase != Phase.Ready) return new List<BattleEvent>();
            var t = turn;
            int s = t.side;
            foreach (var item in t.queue)
            {
                int reps = t.doubleNext && item.card != "guong_doi" ? 2 : 1;
                if (reps == 2) t.doubleNext = false;
                for (int r = 0; r < reps; r++)
                {
                    if (winner >= 0 || ActiveOf(s).dead) break;
                    Emit(new BattleEvent { t = EvType.Card, side = s, card = item.card, kind = "pool", lv = item.lv, rep = r });
                    ApplyEffects(s, Scaled(Data.Card(item.card), item.lv), DmgKind.Card);
                }
            }
            var me = ActiveOf(s);
            var foe = ActiveOf(Other(s));
            if (winner < 0 && !me.dead && !foe.dead && !t.stunned)
            {
                if (t.ult != null)
                {
                    Emit(new BattleEvent { t = EvType.Ult, side = s, card = t.ult.card });
                    ApplyEffects(s, Scaled(Data.Card(t.ult.card), t.ult.lv), DmgKind.Ult);
                }
                else
                {
                    NormalAttack(s, 1, false);
                    foreach (var m in t.extra)
                        if (!ActiveOf(Other(s)).dead && winner < 0) NormalAttack(s, m, true);
                }
            }
            if (winner < 0) EndTurn(s);
            return Flush();
        }

        void EndTurn(int s)
        {
            TickBuffs(s, Until.End);
            step++;
            phase = Phase.Idle;
        }

        // ---------- hiệu ứng ----------

        void NormalAttack(int s, double mult, bool extra)
        {
            var me = ActiveOf(s);
            Emit(new BattleEvent { t = EvType.Attack, side = s, extra = extra });
            double d = DealDamage(s, mult, extra ? DmgKind.Extra : DmgKind.Attack, 0, 0);
            if (d > 0) AddRage(me, Cfg.rageOnAttack, false);
            if (d > 0) RunPassive(me, PassiveTrigger.OnAttack);
        }

        double DealDamage(int s, double mult, DmgKind kind, double pierce, double lifesteal)
        {
            var A = ActiveOf(s);
            var D = ActiveOf(Other(s));
            if (D.dead || A.dead) return 0;
            bool isAttack = kind == DmgKind.Attack || kind == DmgKind.Extra;
            if (isAttack)
            {
                var ev = D.statuses.Find(x => x.id == StatusId.Evade);
                double dodge = BuffSum(D, Stat.Dodge);
                if (ev != null || (dodge > 0 && rng.Chance(dodge)))
                {
                    if (ev != null) D.statuses.Remove(ev);
                    Emit(new BattleEvent
                    {
                        t = EvType.Dmg, from = s, to = Other(s), amount = 0, toHp = 0, blocked = 0, crit = false, elem = 1, dmgKind = kind, dodged = true,
                    });
                    return 0;
                }
            }
            double atk = A.atk * Math.Max(0.1, 1 + BuffSum(A, Stat.Atk));
            double def = D.def * Math.Max(0, 1 + BuffSum(D, Stat.Def)) * (1 - pierce);
            double m = mult;
            if (kind == DmgKind.Attack && turn.trueStrike != 0)
            {
                def = 0;
                m *= turn.trueStrike;
            }
            double em = ElemMult(A, D);
            bool crit = rng.Chance(Cfg.critBase + BuffSum(A, Stat.Crit));
            double taken = Math.Max(0.1, 1 + BuffSum(D, Stat.DmgTaken));
            double raw = atk * m * (Cfg.defK / (Cfg.defK + def)) * em * (crit ? Cfg.critMult : 1) * taken *
                         rng.Range(1 - Cfg.dmgVar, 1 + Cfg.dmgVar);
            double dmg = Math.Max(1, Js.Round(raw));
            double blocked = Math.Min(D.shield, dmg);
            D.shield -= blocked;
            double toHp = Math.Min(D.hp, dmg - blocked);
            // đòn đủ hạ gục tướng còn dạng sau (kể cả từ trên ngưỡng tiến hóa): chừa 1 máu, ngay sau đòn tiến hóa (CheckLow), không gục
            // (người dùng dặn 2026-11-04)
            if (CanEvolve(D) && toHp >= D.hp) toHp = D.hp - 1;
            D.hp -= toHp;
            D.rage = Math.Min(Cfg.maxRage, D.rage + Js.Round((toHp / D.maxHp) * Cfg.rageOnHit));
            dmgDealt[s] += toHp;
            Emit(new BattleEvent
            {
                t = EvType.Dmg, from = s, to = Other(s), amount = dmg, toHp = toHp, blocked = blocked, crit = crit, elem = em, dmgKind = kind,
            });
            double ls = BuffSum(A, Stat.Lifesteal) + lifesteal;
            if (ls > 0 && toHp > 0) HealFlat(A, Js.Round(toHp * ls));
            if (D.hp <= 0) Kill(D);
            else
            {
                RunPassive(D, PassiveTrigger.OnHit);
                CheckLow(D);
            }
            return dmg;
        }

        void Kill(Fighter f)
        {
            if (f.dead) return;
            // boss còn dạng sau thì tiến hóa thay vì gục
            if (CanEvolve(f))
            {
                Evolve(f);
                return;
            }
            // bị động hồi sinh: lần đầu gục thì sống lại ngay, giữ vị trí ra sân, xoá bỏng và choáng (boss không hồi sinh)
            var pc = Data.Card(f.hero.passive);
            if (pc.trigger == PassiveTrigger.Death && !f.revived && !f.boss)
            {
                var rv = Scaled(pc, f.cardPassive).FirstOrDefault(e => e.K == EffectKind.Revive);
                if (rv != null)
                {
                    f.revived = true;
                    f.hp = Math.Max(1, Js.Round(f.maxHp * rv.Pct));
                    f.statuses = f.statuses.Where(x => x.id != StatusId.Burn && x.id != StatusId.Stun).ToList();
                    Emit(new BattleEvent { t = EvType.Passive, side = f.side, idx = f.idx, card = pc.id });
                    Emit(new BattleEvent { t = EvType.Revive, side = f.side, idx = f.idx, hp = f.hp });
                    return;
                }
            }
            f.dead = true;
            f.hp = 0;
            f.shield = 0;
            Emit(new BattleEvent { t = EvType.Death, side = f.side, idx = f.idx });
            var side = sides[f.side];
            if (side.fighters.Exists(x => !x.dead)) side.needSwap = true;
            else
            {
                winner = Other(f.side);
                phase = Phase.Over;
                Emit(new BattleEvent { t = EvType.End, winner = winner });
            }
        }

        // quá số hiệp tối đa: bên có tổng phần trăm máu cao hơn thắng, hoà thì địch thắng
        void TimeOut()
        {
            double Sum(int s)
            {
                double a = 0;
                foreach (var f in sides[s].fighters) a += f.dead ? 0 : f.hp / f.maxHp;
                return a;
            }
            winner = Sum(0) > Sum(1) ? 0 : 1;
            phase = Phase.Over;
            Emit(new BattleEvent { t = EvType.End, winner = winner });
        }

        void Heal(Fighter f, double pct) => HealFlat(f, Js.Round(f.maxHp * pct));

        void HealFlat(Fighter f, double amount)
        {
            double a = Math.Min(amount, f.maxHp - f.hp);
            if (a <= 0 || f.dead) return;
            f.hp += a;
            Emit(new BattleEvent { t = EvType.Heal, side = f.side, amount = a });
        }

        void AddMana(Fighter f, double v, bool show = true)
        {
            double before = f.mana;
            f.mana = Math.Max(0, Math.Min(Cfg.maxMana, f.mana + v));
            if (show && f.mana != before) Emit(new BattleEvent { t = EvType.Mana, side = f.side, v = f.mana - before });
        }

        void AddRage(Fighter f, double v, bool show = true)
        {
            double before = f.rage;
            f.rage = Math.Max(0, Math.Min(Cfg.maxRage, f.rage + v));
            if (show && f.rage != before) Emit(new BattleEvent { t = EvType.Rage, side = f.side, v = f.rage - before });
        }

        void TickBuffs(int s, Until when)
        {
            foreach (var f in sides[s].fighters)
            {
                foreach (var x in f.buffs)
                    if (x.until == when && x.left < 99) x.left--;
                f.buffs = f.buffs.Where(x => x.left > 0).ToList();
            }
        }

        public const string BossEvoCard = "boss_evo";

        static bool CanEvolve(Fighter f) => f.evo && !f.dead && f.form < f.hero.forms.Length - 1;

        // thẻ Tiến Hóa: lên dạng sau, máu tối đa và Công đổi theo hệ số của dạng (giữ phần cộng từ thẻ như Bánh Bao), hồi máu,
        // xoá bỏng và choáng; bị động "máu thấp" của tướng dùng lại được ở dạng mới
        void Evolve(Fighter f)
        {
            var c = Data.Card(BossEvoCard);
            int n = f.hero.forms.Length;
            var ko = EvoMult(Cfg, n, f.form);
            var kn = EvoMult(Cfg, n, f.form + 1);
            double heal = c.Effects.Count > 0 && c.Effects[0].K == EffectKind.Evolve ? c.Effects[0].Pct : 1;
            f.form++;
            f.maxHp = Js.Round(f.maxHp * (kn.hp / ko.hp));
            f.atk = Js.Round(f.atk * (kn.atk / ko.atk));
            f.hp = Math.Max(f.hp, Math.Max(1, Js.Round(f.maxHp * heal)));
            f.statuses = f.statuses.Where(x => x.id != StatusId.Burn && x.id != StatusId.Stun).ToList();
            f.lowHpUsed = false;
            Emit(new BattleEvent { t = EvType.Passive, side = f.side, idx = f.idx, card = c.id });
            Emit(new BattleEvent { t = EvType.Evolve, side = f.side, idx = f.idx, form = f.form, hp = f.hp });
        }

        void CheckLow(Fighter f)
        {
            if (CanEvolve(f) && f.hp / f.maxHp < Data.Card(BossEvoCard).below)
            {
                Evolve(f);
                return;
            }
            var c = Data.Card(f.hero.passive);
            if (c.trigger != PassiveTrigger.LowHp || f.lowHpUsed || f.dead) return;
            if (f.hp / f.maxHp < c.below)
            {
                f.lowHpUsed = true;
                Emit(new BattleEvent { t = EvType.Passive, side = f.side, idx = f.idx, card = c.id });
                ApplyEffectsTo(f, Scaled(c, f.cardPassive), DmgKind.Card);
            }
        }

        void RunPassive(Fighter f, PassiveTrigger trig)
        {
            var c = Data.Card(f.hero.passive);
            if (c.trigger != trig || f.dead) return;
            if (c.hasChance && !rng.Chance(Math.Min(1, c.chance * CardText.LvFactor(Cfg.cardLvStep, f.cardPassive)))) return;
            Emit(new BattleEvent { t = EvType.Passive, side = f.side, idx = f.idx, card = c.id });
            ApplyEffectsTo(f, Scaled(c, f.cardPassive), DmgKind.Card);
        }

        void ApplyEffects(int s, List<Effect> effects, DmgKind kind) => ApplyEffectsTo(ActiveOf(s), effects, kind);

        // self = tướng làm hiệu ứng (có thể là tướng dự bị khi bị động "vào trận"); foe = tướng đang ra sân của bên kia
        void ApplyEffectsTo(Fighter self, List<Effect> effects, DmgKind kind)
        {
            int s = self.side;
            bool isActive = ActiveOf(s) == self;
            foreach (var e in effects)
            {
                if (winner >= 0) return;
                var foe = ActiveOf(Other(s));
                switch (e.K)
                {
                    case EffectKind.Buff:
                    {
                        var tgt = e.On == Target.Foe ? foe : self;
                        if (tgt.dead) break;
                        var until = e.Until ?? CardText.DefaultUntil(e.Stat);
                        tgt.buffs.Add(new Buff { stat = e.Stat, v = e.V, left = e.Turns, until = until });
                        Emit(new BattleEvent { t = EvType.Buff, side = tgt.side, stat = e.Stat, v = e.V, turns = e.Turns });
                        break;
                    }
                    case EffectKind.Heal:
                        Heal(self, e.Pct);
                        break;
                    case EffectKind.MaxHp:
                    {
                        double inc = Js.Round(self.maxHp * e.Pct);
                        self.maxHp += inc;
                        self.hp += inc;
                        Emit(new BattleEvent { t = EvType.MaxHp, side = s, amount = inc });
                        break;
                    }
                    case EffectKind.SelfDmg:
                    {
                        double d = Math.Min(self.hp - 1, Js.Round(self.hp * e.PctCur));
                        if (d <= 0) break;
                        self.hp -= d;
                        self.rage = Math.Min(Cfg.maxRage, self.rage + Js.Round((d / self.maxHp) * Cfg.rageOnHit * 0.5));
                        Emit(new BattleEvent
                        {
                            t = EvType.Dmg, from = s, to = s, amount = d, toHp = d, blocked = 0, crit = false, elem = 1, dmgKind = DmgKind.Self,
                        });
                        CheckLow(self);
                        break;
                    }
                    case EffectKind.Mana:
                        if (e.On == Target.Foe)
                        {
                            double take = Math.Min(foe.mana, Math.Abs(e.V));
                            AddMana(foe, -take);
                            AddMana(self, take);
                        }
                        else AddMana(self, e.V);
                        break;
                    case EffectKind.Rage:
                        if (e.On == Target.Foe)
                        {
                            double take = Math.Min(foe.rage, Math.Abs(e.V));
                            AddRage(foe, -take);
                            AddRage(self, take);
                        }
                        else AddRage(self, e.V);
                        break;
                    case EffectKind.Dmg:
                        if (!isActive) break;
                        for (int i = 0; i < (e.Hits ?? 1); i++)
                        {
                            if (ActiveOf(Other(s)).dead || winner >= 0) break;
                            DealDamage(s, e.Mult, kind, e.Pierce ?? 0, e.Lifesteal ?? 0);
                        }
                        break;
                    case EffectKind.Shield:
                    {
                        double cap = Js.Round(self.maxHp * Cfg.shieldCap);
                        double add = Math.Max(0, Math.Min(cap - self.shield, Js.Round(self.maxHp * e.Pct)));
                        self.shield += add;
                        if (add > 0) Emit(new BattleEvent { t = EvType.Shield, side = s, amount = add });
                        break;
                    }
                    case EffectKind.Status:
                    {
                        var tgt = e.On == Target.Foe ? foe : self;
                        if (tgt.dead) break;
                        if (e.Chance.HasValue && !rng.Chance(e.Chance.Value))
                        {
                            Emit(new BattleEvent { t = EvType.Resist, side = tgt.side });
                            break;
                        }
                        var old = tgt.statuses.Find(x => x.id == e.Status);
                        if (old != null)
                        {
                            old.left = Math.Max(old.left, e.Turns);
                            old.v = Math.Max(old.v, e.V);
                        }
                        else tgt.statuses.Add(new StatusInst { id = e.Status, left = e.Turns, v = e.V });
                        Emit(new BattleEvent { t = EvType.Status, side = tgt.side, status = e.Status, turns = e.Turns });
                        break;
                    }
                    case EffectKind.Cleanse:
                        self.buffs = self.buffs.Where(x => x.stat == Stat.DmgTaken ? x.v <= 0 : x.v >= 0).ToList();
                        self.statuses = self.statuses.Where(x => x.id != StatusId.Burn && x.id != StatusId.Stun).ToList();
                        Emit(new BattleEvent { t = EvType.Cleanse, side = s });
                        break;
                    case EffectKind.Double:
                        turn.doubleNext = true;
                        Emit(new BattleEvent { t = EvType.Double, side = s });
                        break;
                    case EffectKind.Extra:
                        turn.extra.Add(e.Mult);
                        break;
                    case EffectKind.TrueStrike:
                        turn.trueStrike = Math.Max(turn.trueStrike, e.Mult);
                        break;
                    case EffectKind.IfLow:
                        ApplyEffectsTo(self, self.hp / self.maxHp < e.Below ? e.Then : e.Else ?? new List<Effect>(), kind);
                        break;
                }
            }
        }

        // ---------- máy chọn tướng thay khi tướng đang ra sân gục ----------

        public int AiForcedChoice(int s)
        {
            var side = sides[s];
            var foe = ActiveOf(Other(s));
            int best = -1;
            double bestScore = double.NegativeInfinity;
            for (int i = 0; i < side.fighters.Count; i++)
            {
                var f = side.fighters[i];
                if (f.dead) continue;
                double sc = f.hp / f.maxHp + (ElemMult(f, foe) - 1) - (ElemMult(foe, f) - 1) * 0.6;
                if (sc > bestScore)
                {
                    bestScore = sc;
                    best = i;
                }
            }
            return best;
        }
    }
}
