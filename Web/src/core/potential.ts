// Tiềm năng: khai phá (quay lại mọi ô đã mở và không khoá, kết quả chờ người chơi chọn giữ mới / giữ cũ) và Hang Tiềm Năng.
import { adUsed } from './ads';
import { CAVE, POTENTIAL, type PotLine } from './data/potential';
import { HEROES } from './data/heroes';
import { ZONE, type StageDef } from './data/stages';
import type { SaveData } from './progression';
import type { Rng } from './rng';
import type { Elem } from './types';

export const openSlots = (star: number) => POTENTIAL.slotStar.filter((x) => star >= x).length;

export function potentialOf(s: SaveData, hero: string): (PotLine | null)[] {
  const p = s.heroes[hero];
  if (!p.potential) p.potential = [null, null, null, null];
  return p.potential;
}

// số ô khoá thật (chỉ tính ô đã mở và đang có dòng)
export function lockCount(s: SaveData, hero: string, locks: readonly boolean[]) {
  const cur = potentialOf(s, hero);
  const open = openSlots(s.heroes[hero].star);
  let n = 0;
  for (let i = 0; i < open; i++) if (locks[i] && cur[i]) n++;
  return n;
}

// giá: mỗi ô được quay 1 đá, mỗi ô khoá thêm 2 đá
export function spinCost(s: SaveData, hero: string, locks: readonly boolean[]) {
  const open = openSlots(s.heroes[hero].star);
  const lk = lockCount(s, hero, locks);
  return open - lk + POTENTIAL.lockCost * lk;
}

// khai phá: trừ đá, quay các ô mở không khoá; kết quả để ở potentialNew chờ keepPotential. null nếu không quay được.
export function spinPotential(s: SaveData, hero: string, locks: readonly boolean[], rng: Rng): (PotLine | null)[] | null {
  const p = s.heroes[hero];
  if (!p?.owned) return null;
  const open = openSlots(p.star);
  const lk = lockCount(s, hero, locks);
  if (lk > POTENTIAL.maxLocks || open - lk <= 0) return null;
  const cost = spinCost(s, hero, locks);
  if ((s.potentialStones ?? 0) < cost) return null;
  s.potentialStones -= cost;
  const cur = potentialOf(s, hero);
  const idx = [0, 1, 2, 3, 4];
  const next = cur.map((x, i) => {
    if (i >= open || (locks[i] && x)) return x;
    const k = rng.pick(POTENTIAL.kinds);
    const r = rng.weighted(idx, (j) => POTENTIAL.rarityWeight[j]);
    return { k, r };
  });
  p.potentialNew = next;
  return next;
}

// chọn giữ mới hay giữ cũ (đá đã tiêu không hoàn)
export function keepPotential(s: SaveData, hero: string, keepNew: boolean) {
  const p = s.heroes[hero];
  if (!p.potentialNew) return;
  if (keepNew) p.potential = p.potentialNew;
  delete p.potentialNew;
}

// ---------- Hang Tiềm Năng ----------

export const caveOpen = (s: SaveData) => s.zones.hoa >= 4;
// thứ trong tuần của ngày (theo giờ máy, đếm từ 1/1/1970 là thứ Năm): 0 = Chủ nhật
export const weekdayOf = (day: number) => (((day + 4) % 7) + 7) % 7;

export function caveOf(s: SaveData, day: number) {
  if (!s.cave || s.cave.day !== day) s.cave = { day, wins: 0, pick: null };
  return s.cave;
}
export const caveLeft = (s: SaveData, day: number) => {
  const c = caveOf(s, day);
  return CAVE.winsPerDay + adUsed(s, day, 'cave_extra') * CAVE.adExtra - c.wins;
};
// hệ boss hôm nay (null: hôm nay người chơi chọn mà chưa chọn)
export const caveElem = (s: SaveData, day: number): Elem | null => CAVE.weekday[weekdayOf(day)] ?? caveOf(s, day).pick;
export function cavePick(s: SaveData, day: number, z: Elem) {
  if (CAVE.weekday[weekdayOf(day)]) return false;
  caveOf(s, day).pick = z;
  return true;
}

// trận của tầng: 1 boss và 1 tướng phụ cùng hệ (tướng theo vòng trong danh sách tướng của hệ)
export function caveStage(z: Elem, tier: number): StageDef {
  const t = CAVE.tiers[tier];
  const hs = HEROES.filter((h) => h.elem === z);
  return {
    id: 2000 + ZONE[z].order * 10 + tier, zone: z, idx: tier + 1, name: `Hang ${t.name}`, kind: 'boss',
    enemies: [
      { hero: hs[tier % hs.length].id, level: t.level, boss: true },
      { hero: hs[(tier + 1) % hs.length].id, level: Math.max(1, t.level - 2), boss: false },
    ],
    drops: [],
  };
}

// thắng tầng: đá, trừ một lượt; hết lượt thì 0
export function winCave(s: SaveData, day: number, tier: number) {
  if (caveLeft(s, day) <= 0) return 0;
  caveOf(s, day).wins++;
  const n = CAVE.tiers[tier].stones;
  s.potentialStones = (s.potentialStones ?? 0) + n;
  return n;
}
