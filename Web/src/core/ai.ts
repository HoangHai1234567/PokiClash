// Máy chơi: chấm điểm thẻ theo tình huống. Dùng cho địch, cho nút "Tự chơi" và cho máy tự chơi đo cân bằng.
import { CARD } from './data/cards';
import { CFG } from './data/config';
import { elemMult } from './elements';
import { activeOf, buffSum, innateBlock, innateCard, pick, swap, useInnate, type Battle, type Ev, type Fighter, type SideId } from './battle';
import { scaleEffects } from './cardtext';
import type { Effect } from './types';

function value(b: Battle, me: Fighter, foe: Fighter, effects: Effect[]): number {
  const hpR = me.hp / me.maxHp;
  const sk = innateCard(me, 'skill').card;
  const manaNeed = (sk.cost?.mana ?? 0) - me.mana;
  const ultSoon = me.rage >= CFG.maxRage - 20 || !!b.turn.ult;
  let v = 0;
  for (const e of effects) {
    switch (e.k) {
      case 'buff': {
        const turns = e.turns >= 99 ? 4 : e.turns;
        if (e.on === 'foe') {
          if (e.stat === 'def') v += -e.v * 55 * turns * 0.8;
          else if (e.stat === 'atk') v += -e.v * 50;
          else v += Math.abs(e.v) * 30;
        } else if (e.stat === 'atk') v += e.v * 60 * (ultSoon ? 1.6 : 1) * (turns > 1 ? 1.5 : 1);
        else if (e.stat === 'def') v += e.v * 50 * (hpR < 0.5 ? 1.6 : 1) * (e.v < 0 && hpR < 0.4 ? 2 : 1) * turns * 0.8;
        else if (e.stat === 'crit') v += e.v * 45;
        else if (e.stat === 'lifesteal') v += e.v * 60 * (1.3 - hpR);
        else v += Math.abs(e.v) * 40;
        break;
      }
      case 'heal':
        v += Math.min(e.pct, 1 - hpR) * 140 + (hpR < 0.35 ? 25 : 0);
        break;
      case 'maxhp':
        v += e.pct * 70;
        break;
      case 'selfdmg':
        v -= e.pctCur * hpR * 120 * (hpR < 0.4 ? 2.5 : 1);
        break;
      case 'mana':
        v += e.on === 'foe' ? Math.abs(e.v) * 0.5 : e.v * (manaNeed > 0 ? 0.9 : 0.25);
        break;
      case 'rage':
        v += e.on === 'foe' ? Math.abs(e.v) * 0.5 : e.v * (me.rage < CFG.maxRage ? 0.8 : 0.1);
        break;
      case 'dmg':
        v += e.mult * (e.hits ?? 1) * 45 * elemMult(me.hero.elem, foe.hero.elem);
        break;
      case 'shield':
        v += e.pct * 110 * (hpR < 0.6 ? 1.3 : 1);
        break;
      case 'status':
        if (e.id === 'burn') v += e.turns * (e.v ?? 0) * 100 * 1.3 * (foe.hp / foe.maxHp + 0.2);
        else if (e.id === 'stun') v += 55 * (e.chance ?? 1);
        else if (e.id === 'regen') v += e.turns * (e.v ?? 0) * 100 * (1.4 - hpR);
        else if (e.id === 'evade') v += 35 * (hpR < 0.5 ? 1.5 : 1);
        break;
      case 'cleanse': {
        const bad = me.buffs.filter((x) => x.v < 0).length + me.statuses.filter((x) => x.id === 'burn' || x.id === 'stun').length;
        v += bad * 25;
        break;
      }
      case 'double':
        v += b.turn.picksLeft > 1 ? 30 : 0;
        break;
      case 'extra':
        v += e.mult * 50;
        break;
      case 'trueStrike':
        v += 45 * e.mult * (1 + foe.def / 100);
        break;
      case 'ifLow':
        v += value(b, me, foe, hpR < e.below ? e.then : e.else ?? []);
        break;
    }
  }
  return v;
}

export function aiPickIndex(b: Battle, noise = 0.12): number {
  const s = b.turn.side;
  const me = activeOf(b, s), foe = activeOf(b, (1 - s) as SideId);
  let best = 0, bestV = -Infinity;
  b.turn.offer.forEach((id, i) => {
    const v = value(b, me, foe, CARD[id].effects) * b.rng.range(1 - noise, 1 + noise);
    if (v > bestV) {
      bestV = v;
      best = i;
    }
  });
  return best;
}

// gọi trước mỗi lần chọn; trả về chiêu nên dùng ngay (nếu có)
export function aiInnate(b: Battle): 'skill' | 'ult' | null {
  const t = b.turn;
  if (!innateBlock(b, 'ult')) return 'ult';
  if (!innateBlock(b, 'skill')) {
    const me = activeOf(b, t.side);
    const ult = innateCard(me, 'ult').card;
    // để dành mana cho tuyệt kỹ nếu nộ sắp đầy
    const reserve = me.rage >= CFG.maxRage - 15 && !t.ult ? ult.cost?.mana ?? 0 : 0;
    const sk = innateCard(me, 'skill');
    if (me.mana - (sk.card.cost?.mana ?? 0) < reserve) return null;
    const atkUp = buffSum(me, 'atk') > 0 || t.queue.some((q) => CARD[q.card].effects.some((e) => e.k === 'buff' && e.stat === 'atk' && e.on !== 'foe'));
    if (atkUp || t.picksLeft <= 2) return 'skill';
  }
  return null;
}

// đầu lượt: có nên đổi tướng không (trả về chỉ số, -1 là không)
export function aiSwapChoice(b: Battle): number {
  const s = b.turn.side, side = b.sides[s];
  const me = activeOf(b, s), foe = activeOf(b, (1 - s) as SideId);
  const hpR = me.hp / me.maxHp;
  let best = -1, bestScore = 0;
  side.fighters.forEach((f, i) => {
    if (f.dead || i === side.active) return;
    const r = f.hp / f.maxHp;
    let sc = 0;
    if (hpR < 0.25 && r > 0.5) sc = 1 + r;
    const weakNow = elemMult(foe.hero.elem, me.hero.elem) > 1;
    const okThere = elemMult(foe.hero.elem, f.hero.elem) <= 1 && elemMult(f.hero.elem, foe.hero.elem) >= 1;
    if (weakNow && okThere && r > 0.6) sc = Math.max(sc, 0.8 + r * 0.5);
    if (sc > bestScore) {
      bestScore = sc;
      best = i;
    }
  });
  if (best >= 0 && b.rng.chance(0.55)) return best;
  return -1;
}

// cả lượt của máy, trừ phần chạy thẻ (để giao diện tự gọi execute)
export function aiTurn(b: Battle, noise = 0.12): Ev[] {
  const out: Ev[] = [];
  const sw = aiSwapChoice(b);
  if (sw >= 0) out.push(...swap(b, sw));
  while (b.phase === 'picking') {
    const inn = aiInnate(b);
    if (inn) out.push(...useInnate(b, inn));
    out.push(...pick(b, aiPickIndex(b, noise)));
  }
  return out;
}

// giá trị một thẻ cho tướng đang ra sân (để gợi ý)
export function cardValue(b: Battle, id: string, lv = 1): number {
  const s = b.turn.side;
  return value(b, activeOf(b, s), activeOf(b, (1 - s) as SideId), scaleEffects(CARD[id].effects, lv));
}
