// Trang trại: đồng hồ theo đoạn (giờ máy lùi thì bỏ qua đoạn đó, như AFK), mỗi chỗ trừ sức và cộng bi theo năng suất,
// kho chặn ở 12 giờ sản lượng; rút tướng thì tướng nghỉ; thu hoạch lấy phần nguyên, giữ phần lẻ; tự xếp chọn cặp (chỗ, tướng) năng suất cao nhất.
import { FARM, FARM_SPOTS } from './data/farm';
import { HERO, HEROES } from './data/heroes';
import type { SaveData } from './progression';
import { RARITIES } from './types';

const H = 3600000;

export interface FarmSpot {
  hero: string | null;
  energy: number; // giờ làm còn lại của ca
  stock: number; // bi tích (số thực)
}
export interface FarmState {
  lastTick: number;
  boostUntil: number;
  spots: FarmSpot[];
  rest: Record<string, number>; // tướng → hết nghỉ lúc (ms)
}

export const farmFresh = (now: number): FarmState => ({
  lastTick: now, boostUntil: 0, spots: FARM_SPOTS.map(() => ({ hero: null, energy: 0, stock: 0 })), rest: {},
});
export function farmOf(s: SaveData, now: number): FarmState {
  if (!s.farm) s.farm = farmFresh(now);
  return s.farm;
}

export const farmOpen = (s: SaveData) => Object.values(s.heroes).filter((h) => h.owned).length >= FARM.minHeroes;
export const spotsOpen = (level: number) => FARM.openSpots + FARM.spotLevels.filter((l) => level >= l).length;

const rarityIdx = (hero: string) => RARITIES.indexOf(HERO[hero].rarity);

// bi mỗi giờ của tướng ở chỗ i
export function farmRate(s: SaveData, hero: string, i: number) {
  const p = s.heroes[hero];
  let r = FARM.base * FARM.rarityPower[rarityIdx(hero)] * (1 + FARM.lvStep * (s.level - 1)) * (1 + FARM.starStep * (p.star - 1));
  if (HERO[hero].elem === FARM_SPOTS[i].elem) r *= FARM.match;
  return r;
}
export const farmHours = (s: SaveData, hero: string) =>
  FARM.durBase + FARM.durStar * (s.heroes[hero].star - 1) + FARM.durRarity * rarityIdx(hero);
export const farmRestMin = (s: SaveData, hero: string) =>
  Math.min(FARM.restMax, Math.max(FARM.restMin, farmHours(s, hero) * FARM.restPerHour));

// tính tới now; false nếu giờ máy bị lùi (bỏ qua đoạn đó)
export function farmTick(s: SaveData, now: number): boolean {
  const f = farmOf(s, now);
  if (now < f.lastTick) {
    f.lastTick = now;
    return false;
  }
  const dt = (now - f.lastTick) / H;
  f.spots.forEach((sp, i) => {
    if (!sp.hero || sp.energy <= 0) return;
    const work = Math.min(dt, sp.energy);
    const boosted = Math.max(0, Math.min(f.lastTick + work * H, f.boostUntil) - f.lastTick) / H;
    const rate = farmRate(s, sp.hero, i);
    sp.energy -= work;
    sp.stock = Math.min(rate * FARM.capHours, sp.stock + rate * (work + boosted * (FARM.boostMult - 1)));
  });
  for (const k of Object.keys(f.rest)) if (f.rest[k] <= now) delete f.rest[k];
  f.lastTick = now;
  return true;
}

export const heroWorking = (f: FarmState, hero: string) => f.spots.findIndex((sp) => sp.hero === hero);
export const restLeft = (f: FarmState, hero: string, now: number) => Math.max(0, (f.rest[hero] ?? 0) - now);
export const heroFree = (s: SaveData, f: FarmState, hero: string, now: number) =>
  !!s.heroes[hero]?.owned && heroWorking(f, hero) < 0 && restLeft(f, hero, now) <= 0;

export function farmPlace(s: SaveData, now: number, i: number, hero: string): boolean {
  farmTick(s, now);
  const f = farmOf(s, now);
  if (i >= spotsOpen(s.level) || f.spots[i].hero || !heroFree(s, f, hero, now)) return false;
  f.spots[i].hero = hero;
  f.spots[i].energy = farmHours(s, hero);
  return true;
}

// rút tướng: tướng nghỉ theo công thức (rút giữa ca vẫn nghỉ đủ); bi tích vẫn ở chỗ
export function farmRemove(s: SaveData, now: number, i: number): boolean {
  farmTick(s, now);
  const f = farmOf(s, now);
  const sp = f.spots[i];
  if (!sp.hero) return false;
  f.rest[sp.hero] = now + farmRestMin(s, sp.hero) * 60000;
  sp.hero = null;
  sp.energy = 0;
  return true;
}

// thu hoạch: lấy phần nguyên của mọi chỗ, giữ phần lẻ
export function farmHarvest(s: SaveData, now: number): number {
  farmTick(s, now);
  let total = 0;
  for (const sp of farmOf(s, now).spots) {
    const n = Math.floor(sp.stock);
    sp.stock -= n;
    total += n;
  }
  s.balls += total;
  return total;
}

// tự xếp: lặp chọn cặp (chỗ trống, tướng rảnh) có năng suất cao nhất
export function farmAuto(s: SaveData, now: number): [number, string][] {
  farmTick(s, now);
  const f = farmOf(s, now);
  const placed: [number, string][] = [];
  for (;;) {
    let best: { i: number; hero: string; r: number } | null = null;
    for (let i = 0; i < spotsOpen(s.level); i++) {
      if (f.spots[i].hero) continue;
      for (const h of HEROES) {
        if (!heroFree(s, f, h.id, now)) continue;
        const r = farmRate(s, h.id, i);
        if (!best || r > best.r) best = { i, hero: h.id, r };
      }
    }
    if (!best) break;
    farmPlace(s, now, best.i, best.hero);
    placed.push([best.i, best.hero]);
  }
  return placed;
}

// năng suất ×2 trong 1 giờ (sau khi xem quảng cáo farm_boost); không chồng khi đang tăng
export function farmBoost(s: SaveData, now: number): boolean {
  farmTick(s, now);
  const f = farmOf(s, now);
  if (f.boostUntil > now) return false;
  f.boostUntil = now + FARM.boostH * H;
  return true;
}

// chấm báo ở sảnh: có tướng hết sức hoặc kho đầy
export function farmAlert(s: SaveData, now: number): boolean {
  if (!farmOpen(s)) return false;
  farmTick(s, now);
  return farmOf(s, now).spots.some((sp, i) => (sp.hero && sp.energy <= 0) || (sp.hero && sp.stock >= farmRate(s, sp.hero, i) * FARM.capHours));
}

// bảng thử: giả như đã trôi qua ms
export function farmTravel(s: SaveData, ms: number) {
  const f = s.farm;
  if (!f) return;
  f.lastTick -= ms;
  if (f.boostUntil) f.boostUntil -= ms;
  for (const k of Object.keys(f.rest)) f.rest[k] -= ms;
}
