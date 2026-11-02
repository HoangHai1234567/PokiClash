// Máy bi: vật lý thuần (đinh, nấm bật, cốc hứng, ô đáy) và bảng thưởng. Chạy được trong Node để đo tỉ lệ từng ô.
import { CARD } from './data/cards';
import { HEROES } from './data/heroes';
import { Rng } from './rng';
import {
  addExp, addShards, afkBossPool, giveCard, LEGEND_HERO, LEGEND_MILESTONE, rollCardDrop, unlockHero,
  SLOTS, type CardDrop, type CardSlot, type SaveData, type ShardResult,
} from './progression';
import type { Rarity } from './types';

export const BW = 460, BH = 680;
export const BALL_R = 9;
export const DROP_Y = 46;
// mỗi đợt thả tối đa 20 bi, từ cấp 15 là 30 bi
export const MAX_PER_DROP = 20, MAX_PER_DROP_HIGH = 30, MAX_PER_DROP_LEVEL = 15;
export const maxPerDrop = (level: number) => (level >= MAX_PER_DROP_LEVEL ? MAX_PER_DROP_HIGH : MAX_PER_DROP);
// mốc Huyền thoại khi đã có tướng đó (nhặt đủ mảnh trước): đổi thành bản sao thẻ Huyền thoại của tướng
export const LEGEND_COPIES = 15;

export type SlotKind = 'exp5' | 'exp10' | 'exp15' | 'ball' | 'chest_wood' | 'chest_silver' | 'chest_gold';

export interface Peg { x: number; y: number; r: number; kind: 'peg' | 'bumper' | 'post'; }
export interface Seg { x1: number; y1: number; x2: number; y2: number; }
export interface Cup { x: number; y: number; r: number; reward: SlotKind; }
export interface Slot { x0: number; x1: number; reward: SlotKind; }
export interface Ball { id: number; x: number; y: number; vx: number; vy: number; mult: number; alive: boolean; age: number; }

export type PEvent =
  | { t: 'peg'; peg: number; ball: Ball; speed: number }
  | { t: 'land'; reward: SlotKind; slot: number; cup: boolean; ball: Ball };

export const SLOT_LAYOUT: SlotKind[] = [
  'chest_wood', 'exp15', 'exp5', 'ball', 'exp10', 'ball', 'exp5', 'exp15', 'chest_wood',
];
export const LEFT = 14, RIGHT = BW - 14;
// ô mép (rương vàng) hẹp, ô giữa rộng
export const SLOT_W = [22, 50, 66, 30, 96, 30, 66, 50, 22];
export const SWING = 150; // máng thả đung đưa quanh giữa, biên độ này
export const SLOT_TOP = 572, FLOOR = BH - 30;

export function buildBoard() {
  const pegs: Peg[] = [];
  const cups: Cup[] = [];
  for (let i = 0; i < 10; i++) {
    const y = 120 + i * 42;
    const odd = i % 2 === 1;
    const n = odd ? 8 : 9;
    // khe giữa tường và đinh mép phải rộng hơn bi (18), không thì bi kẹt
    const gap = 46.25;
    for (let j = 0; j < n; j++) {
      const x = (odd ? 45 + gap / 2 : 45) + j * gap;
      if (i === 3 && (j === 1 || j === 6)) {
        pegs.push({ x, y, r: 15, kind: 'bumper' });
        continue;
      }
      if (i === 6 && j === 4) {
        pegs.push({ x, y, r: 15, kind: 'bumper' });
        continue;
      }
      if (i === 7 && (j === 1 || j === 6)) {
        cups.push({ x, y: y + 6, r: 3.5, reward: 'chest_silver' });
        continue;
      }
      if (i === 4 && j === 4) {
        cups.push({ x, y: y + 6, r: 3, reward: 'chest_gold' });
        continue;
      }
      pegs.push({ x, y, r: 5, kind: 'peg' });
    }
    // u lồi trên tường ở hàng lẻ: bi trượt dọc tường bị đẩy vào trong
    if (odd) {
      pegs.push({ x: LEFT, y, r: 10, kind: 'post' });
      pegs.push({ x: RIGHT, y, r: 10, kind: 'post' });
    }
  }
  const xs = [LEFT];
  for (const w of SLOT_W) xs.push(xs[xs.length - 1] + w);
  const slots: Slot[] = SLOT_LAYOUT.map((reward, i) => ({ x0: xs[i], x1: xs[i + 1], reward }));
  const segs: Seg[] = [
    { x1: LEFT, y1: 0, x2: LEFT, y2: BH },
    { x1: RIGHT, y1: 0, x2: RIGHT, y2: BH },
    // vai nghiêng hai bên trên cùng: bi thả sát mép trượt vào giữa
    { x1: LEFT, y1: 70, x2: LEFT + 40, y2: 104 },
    { x1: RIGHT, y1: 70, x2: RIGHT - 40, y2: 104 },
  ];
  for (let i = 1; i < SLOT_LAYOUT.length; i++) {
    const x = xs[i];
    segs.push({ x1: x, y1: SLOT_TOP, x2: x, y2: BH });
    pegs.push({ x, y: SLOT_TOP, r: 3.5, kind: 'post' });
  }
  return { pegs, cups, slots, segs };
}

export class Board {
  pegs: Peg[];
  cups: Cup[];
  slots: Slot[];
  segs: Seg[];
  balls: Ball[] = [];
  rng: Rng;
  private nextId = 1;
  gravity = 1150;
  constructor(seed = 1) {
    const b = buildBoard();
    this.pegs = b.pegs;
    this.cups = b.cups;
    this.slots = b.slots;
    this.segs = b.segs;
    this.rng = new Rng(seed);
  }

  drop(x: number, mult: number): Ball {
    const ball: Ball = {
      id: this.nextId++, x: Math.max(LEFT + BALL_R + 2, Math.min(RIGHT - BALL_R - 2, x)), y: DROP_Y,
      vx: this.rng.range(-20, 20), vy: 60, mult, alive: true, age: 0,
    };
    this.balls.push(ball);
    return ball;
  }

  step(dt: number): PEvent[] {
    const ev: PEvent[] = [];
    const sub = 4, h = dt / sub;
    for (let k = 0; k < sub; k++) this.substep(h, ev);
    this.balls = this.balls.filter((b) => b.alive);
    return ev;
  }

  private substep(h: number, ev: PEvent[]) {
    const R = BALL_R;
    for (const b of this.balls) {
      if (!b.alive) continue;
      b.age += h;
      b.vy += this.gravity * h;
      const sp = Math.hypot(b.vx, b.vy);
      if (sp > 950) {
        b.vx *= 950 / sp;
        b.vy *= 950 / sp;
      }
      b.x += b.vx * h;
      b.y += b.vy * h;
      // đinh và nấm
      for (let i = 0; i < this.pegs.length; i++) {
        const p = this.pegs[i];
        const dx = b.x - p.x, dy = b.y - p.y;
        const rr = R + p.r;
        const d2 = dx * dx + dy * dy;
        if (d2 >= rr * rr || d2 === 0) continue;
        const d = Math.sqrt(d2), nx = dx / d, ny = dy / d;
        b.x = p.x + nx * rr;
        b.y = p.y + ny * rr;
        const vn = b.vx * nx + b.vy * ny;
        if (vn < 0) {
          const e = p.kind === 'bumper' ? 0.75 : 0.5;
          b.vx -= (1 + e) * vn * nx;
          b.vy -= (1 + e) * vn * ny;
          // một chút lệch ngẫu nhiên, để không lần nào giống lần nào
          const j = this.rng.range(-0.18, 0.18);
          const c = Math.cos(j), s = Math.sin(j);
          const vx = b.vx * c - b.vy * s, vy = b.vx * s + b.vy * c;
          b.vx = vx * 0.985;
          b.vy = vy * 0.985;
          if (-vn > 60) ev.push({ t: 'peg', peg: i, ball: b, speed: -vn });
        }
      }
      // tường, vách ô
      for (const sg of this.segs) {
        const ex = sg.x2 - sg.x1, ey = sg.y2 - sg.y1;
        const len2 = ex * ex + ey * ey;
        let t = ((b.x - sg.x1) * ex + (b.y - sg.y1) * ey) / len2;
        t = Math.max(0, Math.min(1, t));
        const cx = sg.x1 + ex * t, cy = sg.y1 + ey * t;
        const dx = b.x - cx, dy = b.y - cy;
        const d2 = dx * dx + dy * dy;
        if (d2 >= R * R) continue;
        const d = Math.sqrt(d2) || 0.001, nx = dx / d, ny = dy / d;
        b.x = cx + nx * R;
        b.y = cy + ny * R;
        const vn = b.vx * nx + b.vy * ny;
        if (vn < 0) {
          b.vx -= 1.4 * vn * nx;
          b.vy -= 1.4 * vn * ny;
        }
      }
      // cốc hứng giữa máy
      for (const c of this.cups) {
        const dx = b.x - c.x, dy = b.y - c.y;
        if (b.vy > 0 && dx * dx + dy * dy < c.r * c.r) {
          b.alive = false;
          ev.push({ t: 'land', reward: c.reward, slot: -1, cup: true, ball: b });
          break;
        }
      }
      if (!b.alive) continue;
      // chạm đáy
      if (b.y > FLOOR) {
        const i = this.slots.findIndex((s) => b.x >= s.x0 && b.x < s.x1);
        const slot = i < 0 ? (b.x < BW / 2 ? 0 : this.slots.length - 1) : i;
        b.alive = false;
        ev.push({ t: 'land', reward: this.slots[slot].reward, slot, cup: false, ball: b });
      }
      // kẹt quá lâu thì tính rơi thẳng
      if (b.age > 14 && b.alive) b.vy += 400;
    }
    // bi va bi
    const bs = this.balls;
    for (let i = 0; i < bs.length; i++) {
      const a = bs[i];
      if (!a.alive) continue;
      for (let j = i + 1; j < bs.length; j++) {
        const c = bs[j];
        if (!c.alive) continue;
        const dx = c.x - a.x, dy = c.y - a.y;
        const d2 = dx * dx + dy * dy;
        if (d2 >= 4 * R * R || d2 === 0) continue;
        const d = Math.sqrt(d2), nx = dx / d, ny = dy / d;
        const push = (2 * R - d) / 2;
        a.x -= nx * push;
        a.y -= ny * push;
        c.x += nx * push;
        c.y += ny * push;
        const rv = (c.vx - a.vx) * nx + (c.vy - a.vy) * ny;
        if (rv < 0) {
          const imp = -(1 + 0.6) * rv / 2;
          a.vx -= imp * nx;
          a.vy -= imp * ny;
          c.vx += imp * nx;
          c.vy += imp * ny;
        }
      }
    }
  }
}

// ---------- thưởng ----------

export type Reward =
  | { k: 'exp'; n: number; ups: number }
  | { k: 'balls'; n: number }
  | { k: 'card'; drop: CardDrop }
  | { k: 'shards'; res: ShardResult }
  | { k: 'stones'; n: number }
  | { k: 'hero'; hero: string }
  | { k: 'legendCopies'; hero: string; slot: CardSlot; n: number }
  | { k: 'chest'; kind: 'chest_wood' | 'chest_silver' | 'chest_gold' };

export const SLOT_INFO: Record<SlotKind, { label: string; exp?: number; balls?: number }> = {
  exp5: { label: '5', exp: 5 },
  exp10: { label: '10', exp: 10 },
  exp15: { label: '15', exp: 15 },
  ball: { label: '+1', balls: 1 },
  chest_wood: { label: 'Rương gỗ' },
  chest_silver: { label: 'Rương bạc' },
  chest_gold: { label: 'Rương vàng' },
};

export const CHEST_NAME = { chest_wood: 'Rương Gỗ', chest_silver: 'Rương Bạc', chest_gold: 'Rương Vàng' } as const;

export type ChestRoll = { w: number; k: 'balls' | 'exp' | 'cards' | 'shards' | 'stones'; min: number; max: number; rar?: Partial<Record<Rarity, number>> };
export const CHESTS: Record<'chest_wood' | 'chest_silver' | 'chest_gold', ChestRoll[]> = {
  chest_wood: [
    { w: 55, k: 'balls', min: 2, max: 3 },
    { w: 35, k: 'exp', min: 15, max: 30 },
    { w: 10, k: 'cards', min: 1, max: 1, rar: { common: 70, uncommon: 30 } },
  ],
  // đá tiềm năng (add-potential-stones): bạc 8%, vàng 12%; các dòng cũ giữ trọng số tương đối (× 0,92 và × 0,88)
  chest_silver: [
    { w: 27.6, k: 'balls', min: 3, max: 6 },
    { w: 27.6, k: 'exp', min: 40, max: 70 },
    { w: 32.2, k: 'cards', min: 2, max: 2, rar: { common: 45, uncommon: 35, rare: 18, epic: 2 } },
    { w: 4.6, k: 'shards', min: 1, max: 2 },
    { w: 8, k: 'stones', min: 1, max: 2 },
  ],
  chest_gold: [
    { w: 17.6, k: 'balls', min: 8, max: 12 },
    { w: 17.6, k: 'exp', min: 100, max: 160 },
    { w: 44, k: 'cards', min: 3, max: 3, rar: { uncommon: 45, rare: 40, epic: 14.99, legend: 0.01 } },
    { w: 8.8, k: 'shards', min: 2, max: 4 },
    { w: 12, k: 'stones', min: 2, max: 4 },
  ],
};

// ô đáy: thưởng ngay (rương thì đưa vào hàng chờ mở)
export function slotReward(s: SaveData, kind: SlotKind, x: number): Reward {
  const info = SLOT_INFO[kind];
  if (info.exp) return { k: 'exp', n: info.exp * x, ups: addExp(s, info.exp * x) };
  if (info.balls) {
    s.balls += info.balls * x;
    return { k: 'balls', n: info.balls * x };
  }
  return { k: 'chest', kind: kind as 'chest_wood' | 'chest_silver' | 'chest_gold' };
}

export function openChest(s: SaveData, kind: 'chest_wood' | 'chest_silver' | 'chest_gold', x: number, rng: Rng): Reward[] {
  return rollChest(s, CHESTS[kind], x, rng);
}

// quay một bảng rương (máy bi, rương AFK): một dòng theo trọng số, số lượng × x; thẻ rút riêng từng thẻ theo độ hiếm
export function rollChest(s: SaveData, rows: readonly ChestRoll[], x: number, rng: Rng): Reward[] {
  const roll = rng.weighted(rows, (r) => r.w);
  const n = rng.int(roll.min, roll.max) * x;
  switch (roll.k) {
    case 'balls':
      s.balls += n;
      return [{ k: 'balls', n }];
    case 'exp':
      return [{ k: 'exp', n, ups: addExp(s, n) }];
    case 'cards': {
      const out: Reward[] = [];
      const rar = Object.entries(roll.rar ?? {}) as [Rarity, number][];
      for (let i = 0; i < n; i++) {
        const r = rng.weighted(rar, (e) => e[1])[0];
        const drop = rollCardDrop(s, r, rng);
        if (drop) {
          giveCard(s, drop);
          out.push({ k: 'card', drop });
        }
      }
      return out.length ? out : [{ k: 'exp', n: 20 * x, ups: addExp(s, 20 * x) }];
    }
    case 'stones':
      s.potentialStones = (s.potentialStones ?? 0) + n;
      return [{ k: 'stones', n }];
    case 'shards': {
      const pool = afkBossPool(s);
      const cand = pool.length ? pool : HEROES.filter((h) => h.rarity !== 'legend').map((h) => h.id);
      return [{ k: 'shards', res: addShards(s, rng.pick(cand), n, rng) }];
    }
  }
}

// trừ bi khi thả; tới mốc thì chắc chắn ra tướng Huyền thoại lần đầu
export function spendBall(s: SaveData, x: number): Reward | null {
  s.balls -= x;
  s.ballsSpent += x;
  s.stats.dropped++;
  if (!s.legendDone && s.ballsSpent >= LEGEND_MILESTONE) {
    s.legendDone = true;
    if (!s.heroes[LEGEND_HERO].owned) {
      unlockHero(s, LEGEND_HERO);
      return { k: 'hero', hero: LEGEND_HERO };
    }
    // đã có tướng: bản sao thẻ Huyền thoại của tướng (không có thẻ Huyền thoại thì tuyệt kỹ)
    const h = HEROES.find((x) => x.id === LEGEND_HERO)!;
    const slot = SLOTS.find((k) => CARD[k === 'skill' ? h.skill : k === 'ult' ? h.ult : h.passive].rarity === 'legend') ?? 'ult';
    s.heroes[LEGEND_HERO].cards[slot].copies += LEGEND_COPIES;
    return { k: 'legendCopies', hero: LEGEND_HERO, slot, n: LEGEND_COPIES };
  }
  return null;
}
