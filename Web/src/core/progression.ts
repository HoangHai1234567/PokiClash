// Tiến trình: cấp người chơi (= cấp mọi tướng), thẻ nội tại (lên cấp bằng bản sao), tiến hóa sao, mảnh tướng, AFK.
import type { TreeState } from './trees';
import { badgeBonus } from './data/badges';
import { potentialTotals, type PotLine } from './data/potential';
import type { FarmState } from './farm';
import type { AdState, Entitlements } from './ads';
import { CARD } from './data/cards';
import { HERO, HEROES, LEGEND_MILESTONE_HERO, STARTERS } from './data/heroes';
import { STAGE, STAGES, ZONE, ZONES, zoneStages, type StageDef, type StageEnemy } from './data/stages';
import { Rng } from './rng';
import { RARITIES, type BattleStart, type Elem, type HeroDef, type HeroForm, type Member, type Rarity, type StatMods, type TeamSetup } from './types';

export type CardSlot = 'skill' | 'ult' | 'passive';
export const SLOTS: CardSlot[] = ['skill', 'ult', 'passive'];

export interface CardProg {
  lv: number;
  copies: number;
}
export interface HeroProg {
  owned: boolean;
  shards: number;
  star: number;
  cards: Record<CardSlot, CardProg>;
  potential?: (PotLine | null)[]; // 4 ô tiềm năng
  potentialNew?: (PotLine | null)[]; // kết quả khai phá đang chờ chọn giữ mới / giữ cũ
}
export interface Settings {
  boil: boolean;
  sound: boolean;
  speed: number;
  hints: boolean;
}
export interface SaveData {
  v: number;
  level: number;
  exp: number;
  balls: number;
  ballsSpent: number;
  legendDone: boolean;
  heroes: Record<string, HeroProg>;
  team: string[];
  zones: Record<Elem, number>; // số ải đã qua trong từng đảo (qua lần lượt)
  zoneChests: Record<Elem, number>; // số rương mốc đã nhận trong từng đảo
  clears: Record<number, number>;
  afkSince: number; // lần nhận AFK gần nhất
  afk: AfkState;
  badges: Record<Elem, BadgeProg>; // Đền Huy Hiệu: bậc cao nhất đã có, số trận đã thắng trong bậc đang đánh
  potentialStones: number; // đá tiềm năng
  cave?: { day: number; wins: number; pick: Elem | null }; // Hang Tiềm Năng: lượt thắng trong ngày
  ads?: AdState; // lượt quảng cáo đã dùng trong ngày theo chỗ đặt
  ent?: Entitlements; // quyền lợi gói đã mua
  farm?: FarmState; // trang trại (farm.ts)
  trees?: TreeState; // cây bi (trees.ts)
  settings: Settings;
  stats: { battles: number; wins: number; dropped: number };
  intro: boolean;
}

// đồng hồ AFK theo đoạn (xem afk.ts)
export interface AfkState {
  hours: number; // giờ AFK hiệu dụng đã dồn, tối đa AFK_CAP_H, về 0 khi nhận
  lastTick: number; // ms: lần tính gần nhất
  boostUntil: number; // ms: hết tăng tốc ×2
  chestAcc: number; // giờ hiệu dụng dồn cho rương AFK tiếp theo
  chests: number[]; // ms lúc từng rương AFK vào khay
  chainAt: number; // ms: rương đầu khay đếm giờ mở từ max(lúc vào khay, chainAt)
}

export const afkFresh = (now: number): AfkState => ({
  hours: 0, lastTick: now, boostUntil: 0, chestAcc: 0, chests: [], chainAt: 0,
});

export interface BadgeProg {
  tier: number;
  won: number;
}
export const badgesFresh = (): Record<Elem, BadgeProg> => ({
  thuy: { tier: 0, won: 0 }, hoa: { tier: 0, won: 0 }, kim: { tier: 0, won: 0 }, moc: { tier: 0, won: 0 }, tho: { tier: 0, won: 0 },
});

export const SAVE_VERSION = 4; // v3: lượt quảng cáo gom về ads, thêm ent (quyền lợi gói); v4: 40 tướng (migrateRosterV3)
export const MAX_LEVEL = 30;
export const AFK_CAP_H = 12;
export const LEGEND_MILESTONE = 300; // bi đã thả để chắc chắn ra tướng Huyền thoại lần đầu
export const X_STEPS = [
  { x: 1, lv: 1 },
  { x: 2, lv: 3 },
  { x: 3, lv: 5 },
  { x: 5, lv: 8 },
  { x: 10, lv: 12 },
];
export const CARD_MAX = 5;
export const CARD_REQ = [0, 2, 4, 8, 15]; // bản sao để lên cấp lv -> lv+1
export const STAR_CARDS = [0, 0, 5, 8, 11, 15]; // tổng cấp 3 thẻ để lên sao n (thẻ khởi đầu tổng 3)
export const STAR_LEVEL = [0, 1, 2, 5, 9, 14]; // cấp người chơi để lên sao n
export const MAX_STAR = 5;
// sao đổi sang dạng 2, dạng 3 của dòng tiến hóa: dòng 2 dạng đổi ở sao 3, dòng 3 dạng đổi ở sao 3 và 5
export const FORM_STARS = [3, 5];

// dạng của tướng ở sao này (địch có sao theo cấp, xem enemyTeam)
export function formIndex(h: HeroDef, star: number) {
  let i = 0;
  while (i < FORM_STARS.length && star >= FORM_STARS[i]) i++;
  return Math.min(i, h.forms.length - 1);
}
export const formOf = (h: HeroDef, star: number): HeroForm => h.forms[formIndex(h, star)];

// v3 -> v4 (40 tướng, 2026-11-02): tướng cũ thành dạng của tướng khác (gộp) hoặc bị bỏ khỏi danh sách (đổi sang tướng thay)
export const ROSTER_V4: Record<string, string> = {
  y_trach: 'tieu_y', van_quan: 'lam_quan', hac_duc: 'lam_quan', gia_bi: 'nu_hoa', su_gia: 'de_hoa',
};
// Gộp tiến trình: có tướng nếu một trong hai có, cộng mảnh và bản sao, lấy sao và cấp thẻ cao hơn, giữ tiềm năng của bên đã có
// dòng. Đội, chỗ trang trại, giờ nghỉ đổi id theo; tướng trùng trong đội hoặc trên hai chỗ trang trại thì giữ chỗ đầu.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function migrateRosterV3(o: any): void {
  const hs = o.heroes ?? {};
  for (const [from, to] of Object.entries(ROSTER_V4)) {
    const a = hs[from];
    if (!a) continue;
    delete hs[from];
    const b = hs[to];
    if (!b) {
      hs[to] = a;
      continue;
    }
    b.owned = b.owned || a.owned;
    b.shards += a.shards;
    b.star = Math.max(b.star, a.star);
    for (const k of SLOTS) {
      b.cards[k].lv = Math.max(b.cards[k].lv, a.cards[k].lv);
      b.cards[k].copies += a.cards[k].copies;
    }
    if (!(b.potential ?? []).some(Boolean) && (a.potential ?? []).some(Boolean)) b.potential = a.potential;
  }
  o.team = [...new Set(((o.team ?? []) as string[]).map((t) => ROSTER_V4[t] ?? t))];
  const fm = o.farm;
  if (fm) {
    const seen = new Set<string>();
    for (const sp of fm.spots ?? []) {
      if (sp.hero) sp.hero = ROSTER_V4[sp.hero] ?? sp.hero;
      if (sp.hero && seen.has(sp.hero)) {
        sp.hero = null;
        sp.energy = 0;
      } else if (sp.hero) seen.add(sp.hero);
    }
    const rest: Record<string, number> = {};
    for (const [k, v] of Object.entries((fm.rest ?? {}) as Record<string, number>)) {
      const id = ROSTER_V4[k] ?? k;
      rest[id] = Math.max(rest[id] ?? 0, v);
    }
    fm.rest = rest;
  }
}

function heroProg(owned: boolean): HeroProg {
  return {
    owned, shards: 0, star: 1,
    cards: { skill: { lv: 1, copies: 0 }, ult: { lv: 1, copies: 0 }, passive: { lv: 1, copies: 0 } },
    potential: [null, null, null, null],
  };
}

export function newSave(now: number): SaveData {
  const heroes: Record<string, HeroProg> = {};
  for (const h of HEROES) heroes[h.id] = heroProg(STARTERS.includes(h.id));
  return {
    v: SAVE_VERSION, level: 1, exp: 0, balls: 10, ballsSpent: 0, legendDone: false,
    heroes, team: [...STARTERS], clears: {}, afkSince: now, afk: afkFresh(now), badges: badgesFresh(), potentialStones: 0,
    zones: { thuy: 0, hoa: 0, kim: 0, moc: 0, tho: 0 }, zoneChests: { thuy: 0, hoa: 0, kim: 0, moc: 0, tho: 0 },
    settings: { boil: true, sound: true, speed: 1, hints: true },
    stats: { battles: 0, wins: 0, dropped: 0 }, intro: false,
  };
}

// ---------- cấp ----------

export const EXP_BASE = 40, EXP_POW = 1.35; // EXP lên cấp sau = EXP_BASE × cấp^EXP_POW
export const expToNext = (lv: number) => Math.round(EXP_BASE * Math.pow(lv, EXP_POW));

export function addExp(s: SaveData, n: number): number {
  let ups = 0;
  s.exp += n;
  while (s.level < MAX_LEVEL && s.exp >= expToNext(s.level)) {
    s.exp -= expToNext(s.level);
    s.level++;
    ups++;
  }
  if (s.level >= MAX_LEVEL) s.exp = Math.min(s.exp, expToNext(s.level));
  return ups;
}

export function xAllowed(s: SaveData): number[] {
  return X_STEPS.filter((x) => s.level >= x.lv).map((x) => x.x);
}

// ---------- thẻ và sao ----------

export const cardReq = (lv: number) => (lv >= CARD_MAX ? Infinity : CARD_REQ[lv]);

export function canUpCard(s: SaveData, hero: string, slot: CardSlot): boolean {
  const c = s.heroes[hero].cards[slot];
  return s.heroes[hero].owned && c.lv < CARD_MAX && c.copies >= cardReq(c.lv);
}
export function upCard(s: SaveData, hero: string, slot: CardSlot): boolean {
  if (!canUpCard(s, hero, slot)) return false;
  const c = s.heroes[hero].cards[slot];
  c.copies -= cardReq(c.lv);
  c.lv++;
  return true;
}

export const cardSum = (s: SaveData, hero: string) => SLOTS.reduce((a, k) => a + s.heroes[hero].cards[k].lv, 0);

export function starNeed(star: number) {
  return { cards: STAR_CARDS[star] ?? Infinity, level: STAR_LEVEL[star] ?? Infinity };
}
export function canEvolve(s: SaveData, hero: string): boolean {
  const p = s.heroes[hero];
  if (!p.owned || p.star >= MAX_STAR) return false;
  const need = starNeed(p.star + 1);
  return cardSum(s, hero) >= need.cards && s.level >= need.level;
}
export function evolve(s: SaveData, hero: string): boolean {
  if (!canEvolve(s, hero)) return false;
  s.heroes[hero].star++;
  return true;
}

// ---------- mảnh tướng ----------

export interface ShardResult {
  hero: string;
  n: number;
  unlocked: boolean;
  converted: number; // mảnh của tướng đã có đổi thành bản sao thẻ
}

export function addShards(s: SaveData, hero: string, n: number, rng: Rng): ShardResult {
  const p = s.heroes[hero];
  if (p.owned) {
    for (let i = 0; i < n; i++) p.cards[rng.pick(SLOTS)].copies++;
    return { hero, n, unlocked: false, converted: n };
  }
  p.shards += n;
  if (p.shards >= HERO[hero].shards) {
    p.shards = 0;
    p.owned = true;
    return { hero, n, unlocked: true, converted: 0 };
  }
  return { hero, n, unlocked: false, converted: 0 };
}

export function unlockHero(s: SaveData, hero: string) {
  s.heroes[hero].owned = true;
  s.heroes[hero].shards = 0;
}

// ---------- thẻ rơi từ rương: bản sao thẻ nội tại của tướng đã có ----------

export interface CardDrop {
  hero: string;
  slot: CardSlot;
  card: string;
  rarity: Rarity;
}
const RARITY_ORDER: Rarity[] = ['common', 'uncommon', 'rare', 'epic', 'legend'];

export function rollCardDrop(s: SaveData, rarity: Rarity, rng: Rng): CardDrop | null {
  // thẻ đúng độ hiếm của tướng đã có; không có thì lùi xuống độ hiếm thấp hơn
  for (let r = RARITY_ORDER.indexOf(rarity); r >= 0; r--) {
    const opts: CardDrop[] = [];
    for (const h of HEROES) {
      if (!s.heroes[h.id].owned) continue;
      for (const slot of SLOTS) {
        const id = slot === 'skill' ? h.skill : slot === 'ult' ? h.ult : h.passive;
        if (CARD[id].rarity === RARITY_ORDER[r]) opts.push({ hero: h.id, slot, card: id, rarity: RARITY_ORDER[r] });
      }
    }
    if (opts.length) return rng.pick(opts);
  }
  return null;
}
export function giveCard(s: SaveData, d: CardDrop) {
  s.heroes[d.hero].cards[d.slot].copies++;
}

// ---------- đội, trận ----------

// phần cộng huy hiệu của hệ (bậc cao nhất, không cộng dồn); không có huy hiệu thì undefined
export function badgeMods(s: SaveData, elem: Elem): StatMods | undefined {
  const b = badgeBonus(s.badges?.[elem]?.tier ?? 0);
  return b > 0 ? { hpPct: b, atkPct: b, defPct: b, spd: 0 } : undefined;
}

// phần cộng của tướng: huy hiệu hệ (bậc cao nhất) + tiềm năng (đã chặn trần); hiệu ứng đầu trận của tiềm năng
export function heroBonus(s: SaveData, hero: string): { mods?: StatMods; start?: BattleStart } {
  const b = badgeBonus(s.badges?.[HERO[hero].elem]?.tier ?? 0);
  const t = potentialTotals(s.heroes[hero].potential);
  const hpPct = b + t.hp, atkPct = b + t.atk, defPct = b + t.def, spd = t.spd;
  const out: { mods?: StatMods; start?: BattleStart } = {};
  if (hpPct || atkPct || defPct || spd) out.mods = { hpPct, atkPct, defPct, spd };
  if (t.mana || t.rage || t.crit || t.lifesteal) out.start = { mana: t.mana, rage: t.rage, crit: t.crit, lifesteal: t.lifesteal };
  return out;
}

export function memberOf(s: SaveData, hero: string): Member {
  const p = s.heroes[hero];
  return {
    heroId: hero, level: s.level, star: p.star,
    cardLv: { skill: p.cards.skill.lv, ult: p.cards.ult.lv, passive: p.cards.passive.lv },
    ...heroBonus(s, hero),
  };
}

export function playerTeam(s: SaveData, team = s.team): TeamSetup {
  return { name: 'Đội bạn', ai: false, members: team.filter((h) => s.heroes[h]?.owned).map((h) => memberOf(s, h)) };
}

export function enemyTeam(st: StageDef): TeamSetup {
  return {
    name: st.name, ai: true,
    members: st.enemies.map((e) => ({
      heroId: e.hero, level: e.level, boss: e.boss, ...(e.evo ? { evo: true } : {}), star: 1 + Math.floor(e.level / 6),
      cardLv: { skill: 1 + Math.floor(e.level / 5), ult: 1 + Math.floor(e.level / 6), passive: 1 + Math.floor(e.level / 6) },
    })),
  };
}

// tướng chính của ải (đứng trên nút ải ở màn đảo): boss, không có thì địch cấp cao nhất, bằng cấp thì độ hiếm cao hơn
export function stageLead(st: StageDef): StageEnemy {
  const score = (e: StageEnemy) => (e.boss ? 1000 : 0) + e.level * 10 + RARITIES.indexOf(HERO[e.hero].rarity);
  return st.enemies.reduce((a, e) => (score(e) > score(a) ? e : a));
}
// sao để chọn hình (dạng) của địch ngoài trận: như enemyTeam, riêng boss tiến hóa vào trận ở dạng 1
export const enemyFormStar = (e: StageEnemy) => (e.evo ? 1 : 1 + Math.floor(e.level / 6));

export interface StageReward {
  balls: number;
  first: boolean;
  shards: ShardResult[];
}

// ---------- ải theo đảo ----------

export const totalCleared = (s: SaveData) => ZONES.reduce((a, z) => a + s.zones[z.id], 0);
export const zonesDone = (s: SaveData) => ZONES.filter((z) => s.zones[z.id] >= 8).length;

// ô đội mở theo tiến trình (người dùng chốt 2026-11-02): lúc đầu mang 1 tướng; xong 1 đảo (đánh tới đảo thứ 2) mở ô 2,
// xong 3 đảo (tới đảo thứ 4) mở ô 3. TEAM_SLOT_ZONES[i]: số đảo phải xong để mở ô i + 1. Mô phỏng cân bằng chưa tính luật này.
export const TEAM_SLOT_ZONES = [0, 1, 3];
export const teamSlots = (s: SaveData) => TEAM_SLOT_ZONES.filter((n) => zonesDone(s) >= n).length;
export const stageCleared = (s: SaveData, st: StageDef) => st.idx <= s.zones[st.zone];
export const stageOpen = (s: SaveData, st: StageDef) => st.idx <= s.zones[st.zone] + 1;
export function nextStage(s: SaveData, z: Elem): StageDef | null {
  return zoneStages(z).find((st) => st.idx === s.zones[z] + 1) ?? null;
}

// bi mỗi ải: đảo sau cho nhiều hơn; lần đầu qua có thưởng thêm
export function stageBalls(st: StageDef, first: boolean): number {
  const o = ZONE[st.zone].order;
  const base = 3 + o * 4 + Math.floor((st.idx - 1) / 2);
  const bonus = first ? 5 + o * 2 + (st.kind === 'boss' ? 7 : st.kind === 'mini' ? 3 : 0) : 0;
  return base + bonus;
}

export function winStage(s: SaveData, id: number, rng: Rng): StageReward {
  const st = STAGE[id];
  const first = !stageCleared(s, st);
  const balls = stageBalls(st, first);
  s.balls += balls;
  s.clears[id] = (s.clears[id] ?? 0) + 1;
  if (first) s.zones[st.zone] = st.idx;
  const shards: ShardResult[] = [];
  for (const dr of st.drops) {
    if (dr.gift) {
      if (first) shards.push(addShards(s, dr.hero, dr.min, rng));
      continue;
    }
    const chance = first ? dr.chance : dr.chance * (dr.chance >= 1 ? 0.5 : 0.8);
    if (rng.chance(chance)) shards.push(addShards(s, dr.hero, rng.int(dr.min, dr.max), rng));
  }
  s.stats.battles++;
  s.stats.wins++;
  return { balls, first, shards };
}

// ---------- rương mốc của đảo: qua 4 ải và 8 ải ----------

export const ZONE_CHEST_AT = [4, 8];
export function zoneChestReady(s: SaveData, z: Elem): number {
  const n = s.zoneChests[z];
  return n < ZONE_CHEST_AT.length && s.zones[z] >= ZONE_CHEST_AT[n] ? n : -1;
}
export function claimZoneChest(s: SaveData, z: Elem, rng: Rng) {
  const n = zoneChestReady(s, z);
  if (n < 0) return null;
  const o = ZONE[z].order;
  const balls = (n === 0 ? 10 : 20) + o * (n === 0 ? 5 : 10);
  s.balls += balls;
  const cards: CardDrop[] = [];
  for (let i = 0; i < (n === 0 ? 2 : 4); i++) {
    const drop = rollCardDrop(s, rng.weighted(['common', 'uncommon', 'rare', 'epic'] as Rarity[], (r) => ({ common: 30, uncommon: 40, rare: 25, epic: 5 })[r as 'common']), rng);
    if (drop) {
      giveCard(s, drop);
      cards.push(drop);
    }
  }
  s.zoneChests[z] = n + 1;
  return { balls, cards, big: n === 1 };
}

// ---------- AFK (đồng hồ, rương, tăng tốc ở afk.ts) ----------

// tướng boss đã gặp: rơi mảnh khi AFK và trong rương máy bi
export function afkBossPool(s: SaveData): string[] {
  const out = new Set<string>();
  for (const st of STAGES) if (stageCleared(s, st) && st.kind !== 'normal') for (const d of st.drops) if (!d.gift) out.add(d.hero);
  return [...out];
}

export const LEGEND_HERO = LEGEND_MILESTONE_HERO;
