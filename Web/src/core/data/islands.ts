import type { Elem } from '../types';
import { HERO } from './heroes';
import { MINION } from './minions';
import type { StageDef, StageDrop, StageEnemy } from './stages';

// Hệ thống ải mới (người dùng chốt 2026-11-02, làm thử ở đảo Thủy): mỗi đảo 70 ải, 10 tướng.
// - Ải ra mắt tướng mới ("ải tướng"): 1, 5, 10, 15, 20, rồi 10 ải một tướng (30 … 70). Ải 1 là tướng khởi đầu của chính người
//   chơi. Từ ải 20, ải tướng là mini boss; ải 70 là boss đảo (tiến hóa trong trận).
// - Ải xen giữa trộn ba kiểu: tướng đã gặp được cường hóa (+% Máu, Công), nhóm 2–3 con, và lính (minions.ts).
// Thiết kế, số đo: GD_Claude/14_HeThongAi.md. Các đảo chưa có kế hoạch ở đây vẫn dùng 8 ải cũ (stages.ts, RAW).

export type StageTag = 'hero' | 'minion' | 'buff' | 'group' | 'pair' | 'elite' | 'gate';
export const TAG_NAME: Record<StageTag, string> = {
  hero: 'Tướng mới', minion: 'Bầy lính', buff: 'Cường hóa', group: 'Tướng và lính', pair: 'Hai tướng', elite: 'Lính tinh nhuệ', gate: 'Cửa ải',
};

export interface IslandIntro {
  at: number; // số ải trong đảo
  hero: string;
  name: string; // tên chặng (ải tướng và các ải xen giữa sau nó)
}
export interface IslandPlan {
  size: number;
  intros: IslandIntro[]; // theo thứ tự ải; intros[0].at = 1
  levels: [at: number, lv: number][]; // cấp địch ở vài mốc, giữa hai mốc nội suy rồi làm tròn xuống
  minions: [kind1: string, kind2: string][]; // [bậc 1, bậc 2] theo loại; loại thứ i mở từ chặng minionFrom[i]
  minionFrom: number[];
  tier2From: number; // từ ải này lính lên bậc 2
  gifts: [at: number, hero: string][]; // tướng tặng khi qua ải lần đầu (đủ mảnh)
}

// đảo Thủy: Giọt Sương (tướng khởi đầu) rồi 2 tướng thường, rồi 7 tướng người dùng chọn cho đảo (2026-11-02), Vạn Quân
// (dòng Lam Quân) là boss. Thứ tự theo độ hiếm. Tám Tay, Cá Ngựa, Mập Răng Cưa không có suất trên đảo (GD_Claude/14).
export const ISLANDS: Partial<Record<Elem, IslandPlan>> = {
  thuy: {
    size: 70,
    intros: [
      { at: 1, hero: 'giot_suong', name: 'Bãi Vỏ Sò' },
      { at: 5, hero: 'tieu_y', name: 'Vũng San Hô' },
      { at: 10, hero: 'canh_cut', name: 'Cầu Gỗ Rêu' },
      { at: 15, hero: 'mi_nhi', name: 'Làng Vỏ Ốc' },
      { at: 20, hero: 'ma_ket', name: 'Ngọn Hải Đăng' },
      { at: 30, hero: 'vay_lam', name: 'Thác Bạc' },
      { at: 40, hero: 'kuba', name: 'Rạn Ngọc Trai' },
      { at: 50, hero: 'thuong_lam', name: 'Hồ Gương' },
      { at: 60, hero: 'huyen_vu', name: 'Đền Rùa Cổ' },
      { at: 70, hero: 'lam_quan', name: 'Xoáy Nước Đinh Ba' },
    ],
    levels: [[1, 1], [5, 1.5], [10, 2], [15, 3], [20, 3], [30, 4], [40, 5], [50, 6], [60, 7], [70, 8]],
    minions: [['linh_cua', 'linh_cua2'], ['linh_noc', 'linh_noc2'], ['linh_ngu', 'linh_ngu2']],
    minionFrom: [0, 2, 4],
    tier2From: 35,
    gifts: [[3, 'vo_su'], [25, 'nu_hoa']],
  },
};

// Sức địch ở hệ thống mới (enemyMods): "Lv" của địch là sức thật. Tướng địch mọi độ hiếm đều quy về sức của độ hiếm `rarity`
// (tướng khởi đầu), nên Huyền Vũ cấp 7 không mạnh hơn tướng Khá cấp 7; tướng của người chơi vẫn mạnh theo độ hiếm.
// Người chơi chỉ mang 1 tướng suốt đảo đầu (ô đội 2 mở khi xong đảo): mini boss và boss nhân máu, công ít hơn boss cũ
// (CFG.bossHp 1,8, bossAtk 1,1; boss tiến hóa thêm bossEvoHp).
export const ENEMY_NORM = { rarity: 'uncommon' as const, miniHp: 0.95, miniAtk: 0.95, bossHp: 0.7, bossAtk: 0.95 };

// cường hóa theo kiểu ải: phần cộng Máu và Công (Thủ cộng một nửa)
// intro: ải tướng thường (5, 10, 15); mirror: ải 1 (bóng tướng khởi đầu, yếu đi); trio: mỗi con trong nhóm 3 con (đánh lần lượt
// với 1 tướng nên mỗi con phải yếu hơn)
const BUFF = { intro: 0.15, mirror: -0.2, buff: 0.12, buffLate: 0.25, elite: 0.4, gate: 0.15, gateLate: 0.1, trio: -0.2 };

// mảnh rơi ở ải xen giữa: theo độ hiếm của tướng (ải cửa ải ×1,5); ải tướng chắc chắn rơi mảnh tướng mới
const SHARD_CHANCE = { common: 0.3, uncommon: 0.25, rare: 0.2, epic: 0.15, legend: 0.1 } as const;

const lerpLevel = (p: IslandPlan, at: number) => {
  const L = p.levels;
  for (let i = 1; i < L.length; i++)
    if (at <= L[i][0]) {
      const [a0, l0] = L[i - 1], [a1, l1] = L[i];
      return Math.floor(l0 + ((l1 - l0) * (at - a0)) / (a1 - a0) + 1e-9);
    }
  return L[L.length - 1][1];
};

// mẫu ải xen giữa theo vị trí trong chặng. H = tướng chặng này, P = tướng chặng trước, Q = tướng hai chặng trước,
// M, N = hai loại lính khác nhau (chưa mở loại thứ hai thì lặp loại một)
type Slot = 'H' | 'P' | 'Q' | 'M' | 'N';
type Pattern = { tag: StageTag; units: [Slot, number][] }; // [ai, cường hóa]
const SHORT: Pattern[] = [
  { tag: 'minion', units: [['M', 0], ['N', 0]] },
  { tag: 'buff', units: [['H', BUFF.buff]] },
  { tag: 'group', units: [['P', 0], ['M', 0]] },
  { tag: 'gate', units: [['H', BUFF.gate], ['M', 0]] },
];
const LONG: Pattern[] = [
  { tag: 'minion', units: [['M', 0], ['N', 0]] },
  { tag: 'buff', units: [['H', BUFF.buff]] },
  { tag: 'group', units: [['P', 0], ['M', 0]] },
  { tag: 'minion', units: [['M', 0], ['N', 0], ['M', 0]] },
  { tag: 'pair', units: [['H', 0], ['Q', 0]] },
  { tag: 'buff', units: [['H', BUFF.buffLate]] },
  { tag: 'elite', units: [['N', BUFF.elite], ['M', 0]] },
  { tag: 'group', units: [['H', 0], ['M', 0], ['N', 0]] },
  { tag: 'gate', units: [['H', BUFF.gateLate], ['P', BUFF.gateLate]] },
];
// chặng đầu (sau ải 1): chỉ có lính, tập làm quen; người chơi còn cấp 1 với tướng khởi đầu (không khắc hệ đảo) nên lính yếu hơn
const FIRST: Pattern[] = [
  { tag: 'minion', units: [['M', 0]] },
  { tag: 'minion', units: [['M', -0.25], ['M', -0.25]] },
  { tag: 'elite', units: [['M', 0.25]] },
];

export function buildIsland(zone: Elem, p: IslandPlan): Omit<StageDef, 'id'>[] {
  const out: Omit<StageDef, 'id'>[] = [];
  const gift = new Map(p.gifts);
  for (let ch = 0; ch < p.intros.length; ch++) {
    const it = p.intros[ch];
    const end = ch + 1 < p.intros.length ? p.intros[ch + 1].at : p.size + 1;
    const kinds = p.minions.filter((_, i) => ch >= p.minionFrom[i]);
    for (let at = it.at; at < end; at++) {
      const lv = lerpLevel(p, at);
      const tier2 = at >= p.tier2From;
      const k = at - it.at; // 0 = ải tướng
      let enemies: StageEnemy[];
      let tag: StageTag;
      let kind: StageDef['kind'] = 'normal';
      if (k === 0) {
        tag = 'hero';
        const last = ch === p.intros.length - 1;
        kind = last ? 'boss' : it.at >= 20 ? 'mini' : 'normal';
        // ải 1: bóng của chính tướng khởi đầu, yếu hơn một chút
        enemies = [{ hero: it.hero, level: lv, ...(kind !== 'normal' ? { boss: true } : {}), ...(last ? { evo: true } : {}), ...(ch === 0 ? { buff: BUFF.mirror } : kind === 'normal' ? { buff: BUFF.intro } : {}) }];
      } else {
        const pats = ch === 0 ? FIRST : end - it.at <= 5 ? SHORT : LONG;
        const pat = pats[(k - 1) % pats.length];
        tag = pat.tag;
        // lính xoay vòng theo số ải, để hai ải liền nhau không cùng một cặp
        const kM = kinds[at % kinds.length], kN = kinds[(at + 1) % kinds.length];
        const pick = (slot: Slot): string => {
          if (slot === 'M' || slot === 'N') return (slot === 'M' ? kM : kN)[tier2 ? 1 : 0];
          // tướng chặng trước; không lấy tướng khởi đầu của người chơi (chặng 0): chưa đủ chặng thì lấy tướng chặng này
          const back = slot === 'H' ? 0 : slot === 'P' ? 1 : 2;
          return p.intros[ch - back >= 1 ? ch - back : ch].hero;
        };
        const trio = pat.units.length >= 3 ? BUFF.trio : 0;
        enemies = pat.units.map(([slot, b]) => {
          const buff = Math.round((b + trio) * 100) / 100;
          return { hero: pick(slot), level: lv, ...(buff ? { buff } : {}) };
        });
      }
      out.push({ zone, idx: at, name: k === 0 ? it.name : `${it.name} ${k + 1}`, kind, enemies, drops: drops(at, tag, enemies, gift.get(at)), tag, chapter: ch });
    }
  }
  return out;
}

function drops(at: number, tag: StageTag, enemies: StageEnemy[], gift?: string): StageDrop[] {
  const out: StageDrop[] = [];
  if (gift) out.push({ hero: gift, chance: 1, min: HERO[gift].shards, max: HERO[gift].shards, gift: true });
  if (at === 1) return out; // ải 1: tướng của chính người chơi
  const seen = new Set<string>();
  for (const e of enemies) {
    if (MINION[e.hero] || seen.has(e.hero)) continue;
    seen.add(e.hero);
    if (tag === 'hero') out.push({ hero: e.hero, chance: 1, min: e.evo ? 4 : e.boss ? 3 : 2, max: e.evo ? 6 : e.boss ? 5 : 4 });
    else out.push({ hero: e.hero, chance: SHARD_CHANCE[HERO[e.hero].rarity] * (tag === 'gate' ? 1.5 : 1), min: 1, max: 2 });
  }
  return out;
}
