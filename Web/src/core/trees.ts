// Cây bi trên sảnh: mỗi cây ra TREES.perHour bi mỗi giờ, chứa tối đa TREES.cap, đầy thì ngừng; hái là lấy phần nguyên của mọi cây,
// giữ phần lẻ. Đồng hồ theo đoạn như AFK: giờ máy lùi thì bỏ qua đoạn đó. Cây mới mở bắt đầu từ lần tính sau khi mở (không nhận bù).
// Thẻ Phiêu Lưu: tốc độ và sức chứa ×PASS.treeMult (đoạn có thẻ tính riêng; hết thẻ thì cây đang chứa quá mức thường giữ nguyên, ngừng ra).
import { PASS } from './data/ads';
import { TREES } from './data/trees';
import { totalCleared, zoneDone, type SaveData } from './progression';

const H = 3600000;

export interface TreeState {
  lastTick: number;
  stock: number[]; // bi đang có ở từng cây đã mở (số thực)
}

export function treesOpen(s: SaveData): number {
  if (totalCleared(s) === 0) return 0;
  return 1 + TREES.unlockZones.filter((z) => zoneDone(s, z)).length;
}

export function treesOf(s: SaveData, now: number): TreeState {
  if (!s.trees) s.trees = { lastTick: now, stock: [] };
  return s.trees;
}

const capOf = (m: number) => TREES.cap * m;

function grow(t: TreeState, hours: number, m: number) {
  for (let i = 0; i < t.stock.length; i++)
    if (t.stock[i] < capOf(m)) t.stock[i] = Math.min(capOf(m), t.stock[i] + TREES.perHour * m * hours);
}

// tính tới now; false nếu giờ máy bị lùi
export function treesTick(s: SaveData, now: number): boolean {
  const t = treesOf(s, now);
  if (now < t.lastTick) {
    t.lastTick = now;
    return false;
  }
  const until = s.ent?.passUntil ?? 0;
  const passEnd = Math.min(now, until);
  if (passEnd > t.lastTick) grow(t, (passEnd - t.lastTick) / H, PASS.treeMult);
  const from = Math.max(t.lastTick, until);
  if (now > from) grow(t, (now - from) / H, 1);
  const n = treesOpen(s);
  while (t.stock.length < n) t.stock.push(0);
  t.lastTick = now;
  return true;
}

// sức chứa mỗi cây lúc now (Thẻ Phiêu Lưu ×1,5)
export const treeCap = (s: SaveData, now: number) => capOf((s.ent?.passUntil ?? 0) > now ? PASS.treeMult : 1);
export const treeRate = (s: SaveData, now: number) => TREES.perHour * ((s.ent?.passUntil ?? 0) > now ? PASS.treeMult : 1);

// bi hái được ngay (phần nguyên)
export function treesStock(s: SaveData, now: number): number {
  treesTick(s, now);
  return treesOf(s, now).stock.reduce((a, x) => a + Math.floor(x), 0);
}

// hái mọi cây (× mult khi xem quảng cáo "Hái ×2"): lấy phần nguyên, giữ phần lẻ
export function treesHarvest(s: SaveData, now: number, mult = 1): number {
  treesTick(s, now);
  const t = treesOf(s, now);
  let n = 0;
  for (let i = 0; i < t.stock.length; i++) {
    const k = Math.floor(t.stock[i]);
    t.stock[i] -= k;
    n += k;
  }
  s.balls += n * mult;
  return n * mult;
}

// chấm báo ở sảnh: có cây đã đầy
export function treesFull(s: SaveData, now: number): boolean {
  treesTick(s, now);
  const cap = treeCap(s, now);
  return treesOf(s, now).stock.some((x) => x >= cap);
}

// bảng thử: giả như đã trôi qua ms
export function treesTravel(s: SaveData, ms: number) {
  if (s.trees) s.trees.lastTick -= ms;
}
