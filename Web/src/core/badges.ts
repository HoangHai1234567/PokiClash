// Đền Huy Hiệu: mở đền khi thắng boss Đảo Thủy; dãy hệ X mở khi thắng mini boss (ải 4) Đảo X.
// Chuỗi trận sinh từ công thức (không viết tay 125 trận), thua thì đánh lại đúng trận đó, không mất tiến độ.
import { BADGE } from './data/badges';
import { HEROES } from './data/heroes';
import { ZONE, type StageDef } from './data/stages';
import { openChest, type Reward } from './pachinko';
import { badgesFresh, type SaveData } from './progression';
import type { Rng } from './rng';
import { RARITIES, type Elem } from './types';

export const badgesOf = (s: SaveData) => (s.badges ??= badgesFresh());
export const templeOpen = (s: SaveData) => s.zones.thuy >= 8;
export const lineOpen = (s: SaveData, z: Elem) => templeOpen(s) && s.zones[z] >= 4;
export const badgeCount = (tier: number) => BADGE.counts[tier - 1];
export const badgeTierName = (tier: number) => BADGE.tiers[tier - 1];

// hạt giống cố định theo (hệ, bậc, trận): thua đánh lại vẫn gặp cùng trận
export const badgeSeed = (z: Elem, tier: number, i: number) => 50000 + ZONE[z].order * 1000 + tier * 100 + i;
export const badgeStageId = (z: Elem, tier: number, i: number) => 1000 + ZONE[z].order * 100 + tier * 20 + i;

// trận i (từ 1) của bậc tier: trận lẻ 1 boss; trận chẵn 2 tướng (tướng đầu là boss); trận cuối 3 tướng, boss là tướng hiếm nhất của hệ.
// Tướng hệ X lấy theo vòng trong danh sách tướng của hệ (hệ chỉ có 2 tướng thì trận cuối lặp tướng).
export function badgeStage(z: Elem, tier: number, i: number): StageDef {
  const n = badgeCount(tier);
  const hs = HEROES.filter((h) => h.elem === z);
  const pick = (j: number) => hs[(i + tier + j) % hs.length].id;
  const level = ZONE[z].level[0] + BADGE.levelPerTier * (tier - 1) + Math.floor(i / 2);
  let ids: string[];
  if (i === n) {
    const rarest = hs.reduce((a, b) => (RARITIES.indexOf(b.rarity) > RARITIES.indexOf(a.rarity) ? b : a));
    ids = [rarest.id, pick(0), pick(1)];
  } else ids = i % 2 === 0 ? [pick(0), pick(1)] : [pick(0)];
  return {
    id: badgeStageId(z, tier, i), zone: z, idx: i, name: `${badgeTierName(tier)} ${i}/${n}`, kind: i === n ? 'boss' : 'mini',
    enemies: ids.map((hero, k) => ({ hero, level, boss: k === 0 })),
    drops: [],
  };
}

// trận đang đánh của dãy (null nếu dãy chưa mở hoặc đã xong bậc cuối)
export function badgeCurrent(s: SaveData, z: Elem): { tier: number; i: number } | null {
  if (!lineOpen(s, z)) return null;
  const b = badgesOf(s)[z];
  if (b.tier >= BADGE.counts.length) return null;
  return { tier: b.tier + 1, i: b.won + 1 };
}

// thắng trận đang đánh: bi; trận cuối của bậc thì lên bậc và mở rương (×1)
export function winBadge(s: SaveData, z: Elem, rng: Rng) {
  const cur = badgeCurrent(s, z);
  if (!cur) return null;
  const b = badgesOf(s)[z];
  const balls = BADGE.ballsBase + BADGE.ballsPerTier * cur.tier;
  s.balls += balls;
  b.won++;
  let tierDone = 0, rewards: Reward[] = [];
  const chest = BADGE.chest[cur.tier - 1];
  if (b.won >= badgeCount(cur.tier)) {
    b.tier = cur.tier;
    b.won = 0;
    tierDone = cur.tier;
    rewards = openChest(s, chest, 1, rng);
  }
  return { balls, tierDone, chest: tierDone ? chest : null, rewards };
}
