// Trận theo lượt, luân phiên. Mỗi hiệp: người chơi (bên 0) đi trước. Mỗi lượt:
//   1. đầu lượt (trước lần chọn đầu) được đổi tướng;
//   2. chọn 5 lần, mỗi lần 1 trong 3 thẻ chung; chiêu và tuyệt kỹ dùng xen vào lúc chọn, không tốn lần chọn;
//   3. thẻ chạy lần lượt theo thứ tự xếp, rồi đánh thường (hoặc tuyệt kỹ nếu đã bật).
// Mọi hàm trả về danh sách sự kiện (kèm ảnh chụp số liệu) để giao diện chiếu lại.
import { CFG } from './data/config';
import { CARD, POOL, POOL_WEIGHT } from './data/cards';
import { HERO } from './data/heroes';
import { elemMult } from './elements';
import { Rng } from './rng';
import { scaleEffects, lvFactor } from './cardtext';
import type { CardDef, Effect, HeroDef, Member, Stat, StatMods, StatusId, TeamSetup } from './types';

export type SideId = 0 | 1;

export interface Buff {
  stat: Stat;
  v: number;
  left: number;
  until: 'end' | 'start';
}
export interface StatusInst {
  id: StatusId;
  left: number;
  v: number;
}
export interface Fighter {
  idx: number;
  side: SideId;
  hero: HeroDef;
  level: number;
  star: number;
  cardLv: Member['cardLv'];
  boss: boolean;
  maxHp: number;
  hp: number;
  atk: number;
  def: number;
  spd: number;
  mana: number;
  rage: number;
  shield: number;
  buffs: Buff[];
  statuses: StatusInst[];
  lowHpUsed: boolean;
  revived: boolean; // đã dùng lần hồi sinh
  dead: boolean;
}
export interface Side {
  name: string;
  ai: boolean;
  unlock: number;
  fighters: Fighter[];
  active: number;
  needSwap: boolean;
}
export interface QueueItem {
  card: string;
  kind: 'pool' | 'skill';
  lv: number;
}
export interface Turn {
  side: SideId;
  picksTotal: number;
  picksLeft: number;
  offer: string[];
  queue: QueueItem[];
  swapped: boolean;
  firstPick: boolean;
  skillUsed: boolean;
  ult: { card: string; lv: number } | null;
  doubleNext: boolean;
  extra: number[];
  trueStrike: number;
  stunned: boolean;
}
export type Phase = 'idle' | 'picking' | 'ready' | 'forceSwap' | 'over';

export interface FSnap {
  hp: number;
  maxHp: number;
  shield: number;
  mana: number;
  rage: number;
  dead: boolean;
  st: [StatusId, number][];
  atkB: number;
  defB: number;
}
export interface Snap {
  active: [number, number];
  f: [FSnap[], FSnap[]];
}

export type DmgKind = 'attack' | 'extra' | 'skill' | 'ult' | 'card' | 'burn' | 'self';

export type EvBody =
  | { t: 'start' }
  | { t: 'round'; round: number; first: SideId }
  | { t: 'turn'; side: SideId }
  | { t: 'card'; side: SideId; card: string; kind: 'pool' | 'skill'; lv: number; rep: number }
  | { t: 'innate'; side: SideId; card: string; kind: 'skill' | 'ult' }
  | { t: 'ult'; side: SideId; card: string }
  | { t: 'passive'; side: SideId; idx: number; card: string }
  | { t: 'attack'; side: SideId; extra: boolean }
  | { t: 'dmg'; from: SideId; to: SideId; amount: number; toHp: number; blocked: number; crit: boolean; elem: number; kind: DmgKind; dodged?: boolean }
  | { t: 'heal'; side: SideId; amount: number }
  | { t: 'maxhp'; side: SideId; amount: number }
  | { t: 'shield'; side: SideId; amount: number }
  | { t: 'mana'; side: SideId; v: number }
  | { t: 'rage'; side: SideId; v: number }
  | { t: 'buff'; side: SideId; stat: Stat; v: number; turns: number }
  | { t: 'status'; side: SideId; id: StatusId; turns: number }
  | { t: 'resist'; side: SideId }
  | { t: 'cleanse'; side: SideId }
  | { t: 'double'; side: SideId }
  | { t: 'stunned'; side: SideId }
  | { t: 'swap'; side: SideId; from: number; to: number; forced: boolean }
  | { t: 'death'; side: SideId; idx: number }
  | { t: 'revive'; side: SideId; idx: number; hp: number }
  | { t: 'end'; winner: SideId };
export type Ev = EvBody & { snap: Snap };

export interface Battle {
  rng: Rng;
  seed: number;
  sides: [Side, Side];
  round: number;
  order: [SideId, SideId];
  step: number; // 0, 1 trong hiệp; 2 = hết hiệp
  turn: Turn;
  phase: Phase;
  resume: 'advance' | 'turn';
  winner: -1 | SideId;
  turns: number;
  dmgDealt: [number, number];
  events: Ev[];
}

// ---------- chỉ số ----------

// tổng sức mạnh theo độ hiếm; 6 chỉ số gốc của Aola chỉ quyết dáng (trâu hay công cao), căn bậc hai cho đỡ lệch
const RARITY_POWER = { common: 1, uncommon: 1.1, rare: 1.22, epic: 1.36, legend: 1.5 } as const;

export function heroStats(h: HeroDef, level: number, star: number, boss = false, mods?: StatMods) {
  const [atkP, defP, matk, mdef, hpS, spd] = h.stats;
  const a = Math.max(atkP, matk), d = (defP + mdef) / 2, mean = (a + d + hpS) / 3;
  const m = RARITY_POWER[h.rarity] * (1 + CFG.lvStep * (level - 1)) * (1 + CFG.starStep * (star - 1));
  let hp = CFG.hpBase * Math.sqrt(hpS / mean) * m * (boss ? CFG.bossHp : 1);
  let atk = CFG.atkBase * Math.sqrt(a / mean) * m * (boss ? CFG.bossAtk : 1);
  let def = CFG.defBase * Math.sqrt(d / mean) * m;
  let sp = spd;
  // phần cộng side meta nhân trước khi làm tròn (như HeroStats.Compute của Unity)
  if (mods) {
    hp *= 1 + mods.hpPct;
    atk *= 1 + mods.atkPct;
    def *= 1 + mods.defPct;
    sp += mods.spd;
  }
  return { hp: Math.round(hp), atk: Math.round(atk), def: Math.round(def), spd: sp + level };
}

function makeFighter(m: Member, side: SideId, idx: number): Fighter {
  const hero = HERO[m.heroId];
  const s = heroStats(hero, m.level, m.star, m.boss, m.mods);
  const st = m.start;
  const f: Fighter = {
    idx, side, hero, level: m.level, star: m.star, cardLv: m.cardLv, boss: !!m.boss,
    maxHp: s.hp, hp: s.hp, atk: s.atk, def: s.def, spd: s.spd,
    mana: st ? Math.min(CFG.maxMana, st.mana) : 0, rage: st ? Math.min(CFG.maxRage, st.rage) : 0,
    shield: 0, buffs: [], statuses: [], lowHpUsed: false, revived: false, dead: false,
  };
  // tiềm năng chí mạng, hút máu: buff cả trận (left ≥ 99 không giảm)
  if (st?.crit) f.buffs.push({ stat: 'crit', v: st.crit, left: 99, until: 'end' });
  if (st?.lifesteal) f.buffs.push({ stat: 'lifesteal', v: st.lifesteal, left: 99, until: 'end' });
  return f;
}

const other = (s: SideId): SideId => (s === 0 ? 1 : 0);
export const activeOf = (b: Battle, s: SideId) => b.sides[s].fighters[b.sides[s].active];

export function buffSum(f: Fighter, stat: Stat): number {
  let v = 0;
  for (const x of f.buffs) if (x.stat === stat) v += x.v;
  return v;
}

function snap(b: Battle): Snap {
  const fs = (s: SideId) =>
    b.sides[s].fighters.map((f) => ({
      hp: f.hp, maxHp: f.maxHp, shield: f.shield, mana: f.mana, rage: f.rage, dead: f.dead,
      st: f.statuses.map((x) => [x.id, x.left] as [StatusId, number]),
      atkB: buffSum(f, 'atk'), defB: buffSum(f, 'def'),
    }));
  return { active: [b.sides[0].active, b.sides[1].active], f: [fs(0), fs(1)] };
}

function emit(b: Battle, e: EvBody) {
  b.events.push({ ...e, snap: snap(b) } as Ev);
}
function flush(b: Battle): Ev[] {
  return b.events.splice(0, b.events.length);
}

// ---------- tạo trận ----------

export function createBattle(teams: [TeamSetup, TeamSetup], seed: number, unlock: [number, number] = [99, 99]): Battle {
  const sides = teams.map((t, s) => ({
    name: t.name, ai: t.ai, unlock: unlock[s], active: 0, needSwap: false,
    fighters: t.members.map((m, i) => makeFighter(m, s as SideId, i)),
  })) as [Side, Side];
  return {
    rng: new Rng(seed), seed, sides, round: 0, order: [0, 1], step: 2,
    turn: emptyTurn(0), phase: 'idle', resume: 'advance', winner: -1, turns: 0, dmgDealt: [0, 0], events: [],
  };
}

function emptyTurn(side: SideId): Turn {
  return {
    side, picksTotal: CFG.picks, picksLeft: CFG.picks, offer: [], queue: [], swapped: false, firstPick: false,
    skillUsed: false, ult: null, doubleNext: false, extra: [], trueStrike: 0, stunned: false,
  };
}

// bị động "vào trận" của mọi tướng, rồi vào hiệp đầu
export function startBattle(b: Battle): Ev[] {
  emit(b, { t: 'start' });
  for (const s of [0, 1] as SideId[])
    for (const f of b.sides[s].fighters) runPassive(b, f, 'start');
  advanceInner(b);
  return flush(b);
}

// ---------- tiến trận ----------

export function advance(b: Battle): Ev[] {
  advanceInner(b);
  return flush(b);
}

function advanceInner(b: Battle) {
  if (b.phase === 'over') return;
  for (const s of [0, 1] as SideId[]) {
    const side = b.sides[s];
    if (!side.needSwap) continue;
    if (side.ai) doSwap(b, s, aiForcedChoice(b, s), true);
    else {
      b.phase = 'forceSwap';
      b.resume = 'advance';
      b.turn = { ...emptyTurn(s), side: s };
      return;
    }
  }
  if (b.step >= 2) {
    if (b.round >= CFG.maxRounds) {
      timeOut(b);
      return;
    }
    b.round++;
    // người chơi luôn đi trước mỗi hiệp (chốt 2026-10-31)
    const first: SideId = 0;
    b.order = [first, other(first)];
    b.step = 0;
    emit(b, { t: 'round', round: b.round, first });
  }
  beginTurn(b, b.order[b.step] as SideId);
}

function beginTurn(b: Battle, s: SideId) {
  b.turn = emptyTurn(s);
  b.turns++;
  emit(b, { t: 'turn', side: s });
  const f = activeOf(b, s);
  // buff thủ (hết khi tới lượt chủ), né chưa dùng thì mất
  tickBuffs(b, s, 'start');
  f.statuses = f.statuses.filter((x) => x.id !== 'evade');
  // bỏng, hồi phục
  for (const st of [...f.statuses]) {
    if (st.id === 'burn') {
      const d = Math.max(1, Math.round(f.maxHp * st.v));
      const toHp = Math.min(f.hp, d);
      f.hp -= toHp;
      emit(b, { t: 'dmg', from: other(s), to: s, amount: d, toHp, blocked: 0, crit: false, elem: 1, kind: 'burn' });
    } else if (st.id === 'regen') heal(b, f, st.v);
    if (st.id === 'burn' || st.id === 'regen') st.left--;
  }
  f.statuses = f.statuses.filter((x) => x.left > 0);
  if (f.hp <= 0) kill(b, f);
  if (f.dead) {
    if (b.winner >= 0) return;
    const side = b.sides[s];
    if (side.ai) doSwap(b, s, aiForcedChoice(b, s), true);
    else {
      b.phase = 'forceSwap';
      b.resume = 'turn';
      return;
    }
  }
  continueTurn(b);
}

function continueTurn(b: Battle) {
  const s = b.turn.side;
  const f = activeOf(b, s);
  checkLow(b, f);
  runPassive(b, f, 'turnStart');
  addMana(b, f, CFG.manaPerTurn, false);
  for (const o of b.sides[s].fighters) if (o !== f && !o.dead) o.mana = Math.min(CFG.maxMana, o.mana + CFG.benchMana);
  const stun = f.statuses.find((x) => x.id === 'stun');
  if (stun) {
    // choáng: mất trọn lượt (không chọn thẻ, không đổi tướng, không đánh); mana đầu lượt vẫn nhận (chốt 2026-10-31)
    f.statuses = f.statuses.filter((x) => x.id !== 'stun');
    b.turn.stunned = true;
    b.turn.picksTotal = b.turn.picksLeft = 0;
    emit(b, { t: 'stunned', side: s });
    endTurn(b, s);
    return;
  }
  b.turn.offer = drawOffer(b, s);
  b.phase = 'picking';
}

export function drawOffer(b: Battle, s: SideId): string[] {
  const unlock = b.sides[s].unlock;
  const pool = POOL.filter((c) => (c.unlock ?? 1) <= unlock);
  const out: CardDef[] = [];
  while (out.length < CFG.offer && out.length < pool.length) {
    const left = pool.filter((c) => !out.includes(c));
    out.push(b.rng.weighted(left, (c) => POOL_WEIGHT[c.rarity]));
  }
  return out.map((c) => c.id);
}

// ---------- hành động của người chơi (máy cũng gọi các hàm này) ----------

export function canSwap(b: Battle, idx: number): boolean {
  const t = b.turn, side = b.sides[t.side];
  if (b.phase !== 'picking' || t.firstPick || t.swapped) return false;
  const f = side.fighters[idx];
  return !!f && !f.dead && idx !== side.active;
}

export function swap(b: Battle, idx: number): Ev[] {
  if (!canSwap(b, idx)) return [];
  doSwap(b, b.turn.side, idx, false);
  b.turn.swapped = true;
  // tướng vào sân đầu lượt nhận đủ mana của lượt (lúc ở dự bị mới được phần nhỏ)
  addMana(b, activeOf(b, b.turn.side), CFG.manaPerTurn - CFG.benchMana, false);
  return flush(b);
}

export function forceSwap(b: Battle, idx: number): Ev[] {
  const s = b.turn.side;
  const f = b.sides[s].fighters[idx];
  if (b.phase !== 'forceSwap' || !f || f.dead) return [];
  doSwap(b, s, idx, true);
  if (b.resume === 'turn') continueTurn(b);
  else advanceInner(b);
  return flush(b);
}

function doSwap(b: Battle, s: SideId, idx: number, forced: boolean) {
  const side = b.sides[s];
  const from = side.active;
  side.active = idx;
  side.needSwap = false;
  emit(b, { t: 'swap', side: s, from, to: idx, forced });
}

export function pick(b: Battle, i: number): Ev[] {
  const t = b.turn;
  if (b.phase !== 'picking' || i < 0 || i >= t.offer.length) return [];
  t.queue.push({ card: t.offer[i], kind: 'pool', lv: 1 });
  t.firstPick = true;
  t.picksLeft--;
  if (t.picksLeft > 0) t.offer = drawOffer(b, t.side);
  else {
    t.offer = [];
    b.phase = 'ready';
  }
  return flush(b);
}

export function innateCard(f: Fighter, which: 'skill' | 'ult') {
  const id = which === 'skill' ? f.hero.skill : f.hero.ult;
  return { card: CARD[id], lv: f.cardLv[which] };
}

// lý do không dùng được (rỗng là dùng được)
export function innateBlock(b: Battle, which: 'skill' | 'ult'): string {
  const t = b.turn;
  if (b.phase !== 'picking') return 'Hết lúc chọn';
  if (t.stunned) return 'Đang choáng';
  const f = activeOf(b, t.side);
  const { card } = innateCard(f, which);
  if (which === 'skill' && t.skillUsed) return 'Đã dùng lượt này';
  if (which === 'ult' && t.ult) return 'Đã bật';
  if ((card.cost?.rage ?? 0) > f.rage) return 'Chưa đủ nộ';
  if ((card.cost?.mana ?? 0) > f.mana) return 'Chưa đủ mana';
  return '';
}

export function useInnate(b: Battle, which: 'skill' | 'ult'): Ev[] {
  if (innateBlock(b, which)) return [];
  const t = b.turn, f = activeOf(b, t.side);
  const { card, lv } = innateCard(f, which);
  f.mana -= card.cost?.mana ?? 0;
  f.rage -= card.cost?.rage ?? 0;
  t.firstPick = true; // đã ra quyết định: hết lúc đổi tướng
  if (which === 'skill') {
    t.queue.push({ card: card.id, kind: 'skill', lv });
    t.skillUsed = true;
  } else t.ult = { card: card.id, lv };
  emit(b, { t: 'innate', side: t.side, card: card.id, kind: which });
  return flush(b);
}

// chạy hết hàng thẻ, đánh, kết thúc lượt
export function execute(b: Battle): Ev[] {
  if (b.phase !== 'ready') return [];
  const t = b.turn, s = t.side;
  for (const item of t.queue) {
    const reps = t.doubleNext && item.card !== 'guong_doi' ? 2 : 1;
    if (reps === 2) t.doubleNext = false;
    for (let r = 0; r < reps; r++) {
      if (b.winner >= 0 || activeOf(b, s).dead) break;
      emit(b, { t: 'card', side: s, card: item.card, kind: item.kind, lv: item.lv, rep: r });
      applyEffects(b, s, scaleEffects(CARD[item.card].effects, item.lv), item.kind === 'skill' ? 'skill' : 'card');
    }
  }
  const me = activeOf(b, s), foe = activeOf(b, other(s));
  if (b.winner < 0 && !me.dead && !foe.dead && !t.stunned) {
    if (t.ult) {
      emit(b, { t: 'ult', side: s, card: t.ult.card });
      applyEffects(b, s, scaleEffects(CARD[t.ult.card].effects, t.ult.lv), 'ult');
    } else {
      normalAttack(b, s, 1, false);
      for (const m of t.extra) if (!activeOf(b, other(s)).dead && b.winner < 0) normalAttack(b, s, m, true);
    }
  }
  if (b.winner < 0) endTurn(b, s);
  return flush(b);
}

function endTurn(b: Battle, s: SideId) {
  tickBuffs(b, s, 'end');
  b.step++;
  b.phase = 'idle';
}

// ---------- hiệu ứng ----------

function normalAttack(b: Battle, s: SideId, mult: number, extra: boolean) {
  const me = activeOf(b, s);
  emit(b, { t: 'attack', side: s, extra });
  const d = dealDamage(b, s, mult, extra ? 'extra' : 'attack', 0, 0);
  if (d > 0) addRage(b, me, CFG.rageOnAttack, false);
  if (d > 0) runPassive(b, me, 'onAttack');
}

function dealDamage(b: Battle, s: SideId, mult: number, kind: DmgKind, pierce: number, lifesteal: number): number {
  const A = activeOf(b, s), D = activeOf(b, other(s));
  if (D.dead || A.dead) return 0;
  const isAttack = kind === 'attack' || kind === 'extra';
  if (isAttack) {
    const ev = D.statuses.find((x) => x.id === 'evade');
    const dodge = buffSum(D, 'dodge');
    if (ev || (dodge > 0 && b.rng.chance(dodge))) {
      if (ev) D.statuses = D.statuses.filter((x) => x !== ev);
      emit(b, { t: 'dmg', from: s, to: other(s), amount: 0, toHp: 0, blocked: 0, crit: false, elem: 1, kind, dodged: true });
      return 0;
    }
  }
  const atk = A.atk * Math.max(0.1, 1 + buffSum(A, 'atk'));
  let def = D.def * Math.max(0, 1 + buffSum(D, 'def')) * (1 - pierce);
  let m = mult;
  if (kind === 'attack' && b.turn.trueStrike) {
    def = 0;
    m *= b.turn.trueStrike;
  }
  const em = elemMult(A.hero.elem, D.hero.elem);
  const crit = b.rng.chance(CFG.critBase + buffSum(A, 'crit'));
  const taken = Math.max(0.1, 1 + buffSum(D, 'dmgTaken'));
  const raw = atk * m * (CFG.defK / (CFG.defK + def)) * em * (crit ? CFG.critMult : 1) * taken *
    b.rng.range(1 - CFG.dmgVar, 1 + CFG.dmgVar);
  const dmg = Math.max(1, Math.round(raw));
  const blocked = Math.min(D.shield, dmg);
  D.shield -= blocked;
  const toHp = Math.min(D.hp, dmg - blocked);
  D.hp -= toHp;
  D.rage = Math.min(CFG.maxRage, D.rage + Math.round((toHp / D.maxHp) * CFG.rageOnHit));
  b.dmgDealt[s] += toHp;
  emit(b, { t: 'dmg', from: s, to: other(s), amount: dmg, toHp, blocked, crit, elem: em, kind });
  const ls = buffSum(A, 'lifesteal') + lifesteal;
  if (ls > 0 && toHp > 0) healFlat(b, A, Math.round(toHp * ls));
  if (D.hp <= 0) kill(b, D);
  else {
    runPassive(b, D, 'onHit');
    checkLow(b, D);
  }
  return dmg;
}

function kill(b: Battle, f: Fighter) {
  if (f.dead) return;
  // bị động hồi sinh: lần đầu gục thì sống lại ngay, giữ vị trí ra sân, xoá bỏng và choáng (boss không hồi sinh)
  const pc = CARD[f.hero.passive];
  if (pc.trigger === 'death' && !f.revived && !f.boss) {
    const rv = scaleEffects(pc.effects, f.cardLv.passive).find((e) => e.k === 'revive');
    if (rv && rv.k === 'revive') {
      f.revived = true;
      f.hp = Math.max(1, Math.round(f.maxHp * rv.pct));
      f.statuses = f.statuses.filter((x) => x.id !== 'burn' && x.id !== 'stun');
      emit(b, { t: 'passive', side: f.side, idx: f.idx, card: pc.id });
      emit(b, { t: 'revive', side: f.side, idx: f.idx, hp: f.hp });
      return;
    }
  }
  f.dead = true;
  f.hp = 0;
  f.shield = 0;
  emit(b, { t: 'death', side: f.side, idx: f.idx });
  const side = b.sides[f.side];
  if (side.fighters.some((x) => !x.dead)) side.needSwap = true;
  else {
    b.winner = other(f.side);
    b.phase = 'over';
    emit(b, { t: 'end', winner: b.winner });
  }
}

// quá số hiệp tối đa: bên có tổng phần trăm máu cao hơn thắng, hoà thì địch thắng
function timeOut(b: Battle) {
  const sum = (s: SideId) => b.sides[s].fighters.reduce((a, f) => a + (f.dead ? 0 : f.hp / f.maxHp), 0);
  b.winner = sum(0) > sum(1) ? 0 : 1;
  b.phase = 'over';
  emit(b, { t: 'end', winner: b.winner });
}

function heal(b: Battle, f: Fighter, pct: number) {
  healFlat(b, f, Math.round(f.maxHp * pct));
}
function healFlat(b: Battle, f: Fighter, amount: number) {
  const a = Math.min(amount, f.maxHp - f.hp);
  if (a <= 0 || f.dead) return;
  f.hp += a;
  emit(b, { t: 'heal', side: f.side, amount: a });
}
function addMana(b: Battle, f: Fighter, v: number, show = true) {
  const before = f.mana;
  f.mana = Math.max(0, Math.min(CFG.maxMana, f.mana + v));
  if (show && f.mana !== before) emit(b, { t: 'mana', side: f.side, v: f.mana - before });
}
function addRage(b: Battle, f: Fighter, v: number, show = true) {
  const before = f.rage;
  f.rage = Math.max(0, Math.min(CFG.maxRage, f.rage + v));
  if (show && f.rage !== before) emit(b, { t: 'rage', side: f.side, v: f.rage - before });
}

function tickBuffs(b: Battle, s: SideId, when: 'end' | 'start') {
  for (const f of b.sides[s].fighters) {
    for (const x of f.buffs) if (x.until === when && x.left < 99) x.left--;
    f.buffs = f.buffs.filter((x) => x.left > 0);
  }
}

function checkLow(b: Battle, f: Fighter) {
  const c = CARD[f.hero.passive];
  if (c.trigger !== 'lowHp' || f.lowHpUsed || f.dead) return;
  if (f.hp / f.maxHp < (c.below ?? 0.3)) {
    f.lowHpUsed = true;
    emit(b, { t: 'passive', side: f.side, idx: f.idx, card: c.id });
    applyEffectsTo(b, f, scaleEffects(c.effects, f.cardLv.passive), 'card');
  }
}

function runPassive(b: Battle, f: Fighter, trig: 'start' | 'turnStart' | 'onAttack' | 'onHit') {
  const c = CARD[f.hero.passive];
  if (c.trigger !== trig || f.dead) return;
  if (c.chance !== undefined && !b.rng.chance(Math.min(1, c.chance * lvFactor(f.cardLv.passive)))) return;
  emit(b, { t: 'passive', side: f.side, idx: f.idx, card: c.id });
  applyEffectsTo(b, f, scaleEffects(c.effects, f.cardLv.passive), 'card');
}

function applyEffects(b: Battle, s: SideId, effects: Effect[], kind: DmgKind) {
  applyEffectsTo(b, activeOf(b, s), effects, kind);
}

// self = tướng làm hiệu ứng (có thể là tướng dự bị khi bị động "vào trận"); foe = tướng đang ra sân của bên kia
function applyEffectsTo(b: Battle, self: Fighter, effects: Effect[], kind: DmgKind) {
  const s = self.side;
  const isActive = activeOf(b, s) === self;
  for (const e of effects) {
    if (b.winner >= 0) return;
    const foe = activeOf(b, other(s));
    switch (e.k) {
      case 'buff': {
        const tgt = e.on === 'foe' ? foe : self;
        if (tgt.dead) break;
        const until = e.until ?? (e.stat === 'def' || e.stat === 'dmgTaken' || e.stat === 'dodge' ? 'start' : 'end');
        tgt.buffs.push({ stat: e.stat, v: e.v, left: e.turns, until });
        emit(b, { t: 'buff', side: tgt.side, stat: e.stat, v: e.v, turns: e.turns });
        break;
      }
      case 'heal':
        heal(b, self, e.pct);
        break;
      case 'maxhp': {
        const inc = Math.round(self.maxHp * e.pct);
        self.maxHp += inc;
        self.hp += inc;
        emit(b, { t: 'maxhp', side: s, amount: inc });
        break;
      }
      case 'selfdmg': {
        const d = Math.min(self.hp - 1, Math.round(self.hp * e.pctCur));
        if (d <= 0) break;
        self.hp -= d;
        self.rage = Math.min(CFG.maxRage, self.rage + Math.round((d / self.maxHp) * CFG.rageOnHit * 0.5));
        emit(b, { t: 'dmg', from: s, to: s, amount: d, toHp: d, blocked: 0, crit: false, elem: 1, kind: 'self' });
        checkLow(b, self);
        break;
      }
      case 'mana':
        if (e.on === 'foe') {
          const take = Math.min(foe.mana, Math.abs(e.v));
          addMana(b, foe, -take);
          addMana(b, self, take);
        } else addMana(b, self, e.v);
        break;
      case 'rage':
        if (e.on === 'foe') {
          const take = Math.min(foe.rage, Math.abs(e.v));
          addRage(b, foe, -take);
          addRage(b, self, take);
        } else addRage(b, self, e.v);
        break;
      case 'dmg':
        if (!isActive) break;
        for (let i = 0; i < (e.hits ?? 1); i++) {
          if (activeOf(b, other(s)).dead || b.winner >= 0) break;
          dealDamage(b, s, e.mult, kind, e.pierce ?? 0, e.lifesteal ?? 0);
        }
        break;
      case 'shield': {
        const cap = Math.round(self.maxHp * CFG.shieldCap);
        const add = Math.max(0, Math.min(cap - self.shield, Math.round(self.maxHp * e.pct)));
        self.shield += add;
        if (add > 0) emit(b, { t: 'shield', side: s, amount: add });
        break;
      }
      case 'status': {
        const tgt = e.on === 'foe' ? foe : self;
        if (tgt.dead) break;
        if (e.chance !== undefined && !b.rng.chance(e.chance)) {
          emit(b, { t: 'resist', side: tgt.side });
          break;
        }
        const old = tgt.statuses.find((x) => x.id === e.id);
        if (old) {
          old.left = Math.max(old.left, e.turns);
          old.v = Math.max(old.v, e.v ?? 0);
        } else tgt.statuses.push({ id: e.id, left: e.turns, v: e.v ?? 0 });
        emit(b, { t: 'status', side: tgt.side, id: e.id, turns: e.turns });
        break;
      }
      case 'cleanse':
        self.buffs = self.buffs.filter((x) => (x.stat === 'dmgTaken' ? x.v <= 0 : x.v >= 0));
        self.statuses = self.statuses.filter((x) => x.id !== 'burn' && x.id !== 'stun');
        emit(b, { t: 'cleanse', side: s });
        break;
      case 'double':
        b.turn.doubleNext = true;
        emit(b, { t: 'double', side: s });
        break;
      case 'extra':
        b.turn.extra.push(e.mult);
        break;
      case 'trueStrike':
        b.turn.trueStrike = Math.max(b.turn.trueStrike, e.mult);
        break;
      case 'ifLow':
        applyEffectsTo(b, self, self.hp / self.maxHp < e.below ? e.then : e.else ?? [], kind);
        break;
    }
  }
}

// ---------- máy chọn tướng thay khi tướng đang ra sân chết ----------

export function aiForcedChoice(b: Battle, s: SideId): number {
  const side = b.sides[s];
  const foe = activeOf(b, other(s));
  let best = -1, bestScore = -Infinity;
  side.fighters.forEach((f, i) => {
    if (f.dead) return;
    const sc = f.hp / f.maxHp + (elemMult(f.hero.elem, foe.hero.elem) - 1) - (elemMult(foe.hero.elem, f.hero.elem) - 1) * 0.6;
    if (sc > bestScore) {
      bestScore = sc;
      best = i;
    }
  });
  return best;
}
