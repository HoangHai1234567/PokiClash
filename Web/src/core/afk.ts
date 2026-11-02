// AFK: ải đã qua tự đánh khi người chơi vắng, ra mảnh tướng boss (tỉ lệ thấp) và rương AFK. Bi thụ động nay đến từ cây bi (trees.ts).
// Đồng hồ theo đoạn: mỗi lần tính (mở hộp, nhận, mỗi phút) cộng phần giờ mới từ afk.lastTick;
// phần nằm trong đoạn tăng tốc tính ×2; giờ hiệu dụng chặn ở AFK_CAP_H tới khi nhận; giờ máy lùi thì bỏ qua đoạn đó.
// Cứ AFK.chestEveryH giờ hiệu dụng ra 1 rương AFK (khay tối đa AFK.chestSlots); rương đầu khay đếm AFK.chestOpenH giờ rồi mở được,
// mở xong (hoặc tới giờ) thì rương kế đếm tiếp. Thẻ Phiêu Lưu: khay 5 ô, rương mở trong 1 giờ.
import { passActive } from './ads';
import { PASS } from './data/ads';
import { rollChest, type ChestRoll, type Reward } from './pachinko';
import {
  AFK_CAP_H, addShards, afkBossPool, afkFresh, totalCleared, type AfkState, type SaveData, type ShardResult,
} from './progression';
import type { Rng } from './rng';

const H = 3600000;

export const AFK = {
  shardChance: 0.08, // mỗi giờ AFK tròn
  chestEveryH: 3,
  chestSlots: 4,
  chestOpenH: 2,
  boostH: 2,
  boostMult: 2,
};

// rương AFK ở ×1: thẻ hiếm hơn rương máy bi
// đá tiềm năng hiếm (5%); các dòng cũ × 0,95
export const AFK_CHEST: ChestRoll[] = [
  { w: 38, k: 'balls', min: 4, max: 8 },
  { w: 28.5, k: 'exp', min: 30, max: 60 },
  { w: 28.5, k: 'cards', min: 1, max: 2, rar: { common: 60, uncommon: 30, rare: 9.5, epic: 0.5 } },
  { w: 5, k: 'stones', min: 1, max: 1 },
];

// ngày theo giờ máy (đặt lại lượt quảng cáo lúc 0 giờ): tzMin = số phút lệch so với UTC (+420 ở Việt Nam)
export const localDay = (now: number, tzMin: number) => Math.floor((now + tzMin * 60000) / 86400000);

export function afkOf(s: SaveData): AfkState {
  if (!s.afk) s.afk = afkFresh(s.afkSince);
  return s.afk;
}

// số ô khay và giờ mở rương (Thẻ Phiêu Lưu đổi cả hai)
export const afkSlots = (s: SaveData, now: number) => (passActive(s, now) ? PASS.afkSlots : AFK.chestSlots);
export const afkOpenH = (s: SaveData, now: number) => (passActive(s, now) ? PASS.afkOpenH : AFK.chestOpenH);

// rương đã đủ giờ dồn mà khay còn chỗ: vào khay lúc at
function flushChest(a: AfkState, at: number, slots: number) {
  if (a.chestAcc >= AFK.chestEveryH && a.chests.length < slots) {
    a.chests.push(at);
    a.chestAcc = 0;
  }
}

// cộng giờ hiệu dụng trong đoạn [from, to] với hệ số r; dừng khi đầy giờ; ra rương đúng lúc dồn đủ
function advance(a: AfkState, from: number, to: number, r: number, slots: number) {
  let t = from;
  while (t < to) {
    const room = AFK_CAP_H - a.hours;
    if (room <= 0) return;
    const avail = ((to - t) / H) * r;
    const toChest = a.chests.length >= slots ? Infinity : AFK.chestEveryH - a.chestAcc;
    const gain = Math.min(avail, room, toChest);
    a.hours += gain;
    a.chestAcc = Math.min(AFK.chestEveryH, a.chestAcc + gain);
    t += (gain / r) * H;
    if (gain === toChest) {
      a.chests.push(t);
      a.chestAcc = 0;
      continue;
    }
    return; // hết đoạn hoặc đầy giờ
  }
}

// tính tới now; trả false nếu giờ máy bị lùi (đoạn đó bỏ qua, đồng hồ tính tiếp từ now)
export function afkTick(s: SaveData, now: number): boolean {
  const a = afkOf(s);
  if (now < a.lastTick) {
    a.lastTick = now;
    return false;
  }
  if (totalCleared(s) === 0) {
    a.lastTick = now;
    return true;
  }
  const slots = afkSlots(s, now);
  flushChest(a, a.lastTick, slots);
  const boostEnd = Math.min(now, a.boostUntil);
  if (boostEnd > a.lastTick) advance(a, a.lastTick, boostEnd, AFK.boostMult, slots);
  const from = Math.max(a.lastTick, a.boostUntil);
  if (now > from) advance(a, from, now, 1, slots);
  a.lastTick = now;
  return true;
}

export function afkPending(s: SaveData, now: number) {
  afkTick(s, now);
  const hours = afkOf(s).hours;
  return { hours, full: hours >= AFK_CAP_H };
}

// nhận mảnh (× mult): mỗi giờ tròn một lần thử
export function claimAfk(s: SaveData, now: number, mult: number, rng: Rng) {
  const p = afkPending(s, now);
  const shards: ShardResult[] = [];
  const pool = afkBossPool(s);
  for (let h = 0; h < Math.floor(p.hours); h++)
    if (pool.length && rng.chance(AFK.shardChance)) shards.push(addShards(s, rng.pick(pool), 1 * mult, rng));
  afkOf(s).hours = 0;
  s.afkSince = now;
  return { shards, hours: p.hours };
}

// giờ bắt đầu đếm và giờ mở được của từng rương trong khay
export function afkChestTimes(s: SaveData, now: number): { start: number; ready: number }[] {
  const openH = afkOpenH(s, now);
  const a = afkOf(s);
  let prev = a.chainAt;
  return a.chests.map((at) => {
    const start = Math.max(at, prev);
    prev = start + openH * H;
    return { start, ready: prev };
  });
}

// mở rương đầu khay; early: "Mở ngay" (đã xem quảng cáo) khi chưa tới giờ. Chưa tới giờ mà không early thì null.
export function openAfkChest(s: SaveData, now: number, rng: Rng, early = false): Reward[] | null {
  afkTick(s, now);
  const a = afkOf(s);
  if (!a.chests.length) return null;
  const t = afkChestTimes(s, now)[0];
  if (now < t.ready && !early) return null;
  a.chainAt = Math.min(now, t.ready);
  a.chests.shift();
  flushChest(a, now, afkSlots(s, now));
  return rollChest(s, AFK_CHEST, 1, rng);
}

export const afkBoosting = (s: SaveData, now: number) => afkOf(s).boostUntil > now;

// bật tăng tốc ×2 trong AFK.boostH giờ (không chồng khi đang tăng tốc)
export function afkBoost(s: SaveData, now: number): boolean {
  afkTick(s, now);
  const a = afkOf(s);
  if (a.boostUntil > now) return false;
  a.boostUntil = now + AFK.boostH * H;
  return true;
}

// bảng thử: giả như đã trôi qua ms (lùi mọi mốc giờ đã lưu)
export function afkTravel(s: SaveData, ms: number) {
  const a = afkOf(s);
  s.afkSince -= ms;
  a.lastTick -= ms;
  if (a.boostUntil) a.boostUntil -= ms;
  if (a.chainAt) a.chainAt -= ms;
  a.chests = a.chests.map((t) => t - ms);
}
