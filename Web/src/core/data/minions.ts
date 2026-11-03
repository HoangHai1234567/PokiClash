import type { CardDef, Elem, HeroDef } from '../types';
import { CARD } from './cards';
import { HERO } from './heroes';

// Lính (hệ thống ải 70 ải mỗi đảo, người dùng chốt 2026-11-02): quái chỉ để gây khó ở các ải xen giữa, KHÔNG thu thập được
// (không có trong HEROES, không rơi mảnh, không vào bản lưu). Trong trận dùng như tướng: đăng ký vào HERO và CARD ở cuối file.
// Mỗi loại 2 bậc: bậc 2 thay bậc 1 ở nửa sau đảo (islands.ts). Hình: dạng aola gốc chưa có trong danh sách tướng
// (reskin/goc_<id>), CHỈ DÙNG TRONG BẢN THỬ. Chỉ số gốc là 6 chỉ số aola (pmDataMap cột 4–9), chỉ quyết dáng như tướng.

// lính yếu hơn tướng cùng cấp: nhân vào Máu, Công, Thủ (enemyTeam cộng thêm phần cường hóa của ải)
export const MINION_POWER = { hp: 0.85, atk: 0.9, def: 0.9 };

export interface MinionDef extends HeroDef {
  minion: true;
  tier: 1 | 2;
  kind: string; // loại lính (cùng loại khác bậc), để không xếp hai con giống hệt vào một ải
}

function minion(
  id: string, name: string, title: string, elem: Elem, stats: HeroDef['stats'], aola: string, kind: string, tier: 1 | 2,
  size = 0.8,
): MinionDef {
  return {
    id, name, title, aola, elem, rarity: 'common', stats,
    skill: `${id}_skill`, ult: `${id}_ult`, passive: `${id}_pas`,
    shards: 0, line: 'Lính', size, forms: [{ name, aola, size }], minion: true, tier, kind,
  };
}

export const MINIONS: MinionDef[] = [
  // Cua: trâu, giảm sát thương nhận
  minion('linh_cua', 'Cua Kìm', 'Lính gác bãi cát', 'thuy', [44, 55, 33, 55, 33, 22], 'goc_1313', 'cua', 1),
  minion('linh_cua2', 'Cua Pháo', 'Càng to bắn bọt', 'thuy', [66, 77, 55, 77, 55, 44], 'goc_1314', 'cua', 2, 0.86),
  // Cá nóc: bị đánh thì đâm gai (bỏng), phồng lên làm khiên
  minion('linh_noc', 'Cá Nóc', 'Quả bóng gai', 'thuy', [40, 30, 30, 40, 50, 30], 'goc_16', 'noc', 1),
  minion('linh_noc2', 'Cá Nóc Điện', 'Gai điện tê tê', 'thuy', [60, 40, 50, 60, 70, 60], 'goc_17', 'noc', 2, 0.86),
  // Song ngư: nhanh, né, đánh hai lần
  minion('linh_ngu', 'Song Ngư Con', 'Đôi cá lượn nhanh', 'thuy', [80, 40, 40, 60, 40, 60], 'goc_829', 'ngu', 1),
  minion('linh_ngu2', 'Song Ngư', 'Đôi cá rẽ sóng', 'thuy', [100, 60, 60, 80, 60, 80], 'goc_830', 'ngu', 2, 0.86),
];
export const MINION: Record<string, MinionDef> = Object.fromEntries(MINIONS.map((m) => [m.id, m]));
export const isMinion = (id: string) => id in MINION;

const c = (id: string, kind: 'skill' | 'ult' | 'passive', name: string, icon: string, effects: CardDef['effects'], extra: Partial<CardDef> = {}): CardDef =>
  ({ id: `${id}_${kind === 'passive' ? 'pas' : kind}`, owner: id, name, rarity: 'common', kind, icon, effects, ...extra });

export const MINION_CARDS: CardDef[] = [
  c('linh_cua', 'skill', 'Kẹp Kìm', 'claw', [{ k: 'dmg', mult: 1.0 }], { cost: { mana: 30 } }),
  c('linh_cua', 'ult', 'Kìm Sắt', 'claw', [{ k: 'dmg', mult: 1.6 }], { cost: { rage: 100, mana: 30 } }),
  c('linh_cua', 'passive', 'Mai Cứng', 'shield', [{ k: 'buff', stat: 'dmgTaken', v: -0.15, turns: 99 }], { trigger: 'start' }),
  c('linh_cua2', 'skill', 'Pháo Bọt', 'bubble', [{ k: 'dmg', mult: 1.2 }], { cost: { mana: 30 } }),
  c('linh_cua2', 'ult', 'Pháo Kép', 'bubble', [{ k: 'dmg', mult: 0.9, hits: 2 }], { cost: { rage: 100, mana: 35 } }),
  c('linh_cua2', 'passive', 'Mai Thép', 'shield', [{ k: 'buff', stat: 'dmgTaken', v: -0.2, turns: 99 }], { trigger: 'start' }),
  c('linh_noc', 'skill', 'Phồng Gai', 'bubble', [{ k: 'shield', pct: 0.15 }], { cost: { mana: 30 } }),
  c('linh_noc', 'ult', 'Nổ Gai', 'crack', [{ k: 'dmg', mult: 1.5 }], { cost: { rage: 100, mana: 30 } }),
  c('linh_noc', 'passive', 'Gai Độc', 'fang', [{ k: 'status', id: 'burn', turns: 2, v: 0.04, on: 'foe' }], { trigger: 'onHit', chance: 0.3 }),
  c('linh_noc2', 'skill', 'Điện Giật', 'bolt', [{ k: 'dmg', mult: 1.1 }, { k: 'status', id: 'stun', turns: 1, chance: 0.15, on: 'foe' }], { cost: { mana: 35 } }),
  c('linh_noc2', 'ult', 'Sấm Gai', 'bolt', [{ k: 'dmg', mult: 1.8 }], { cost: { rage: 100, mana: 35 } }),
  c('linh_noc2', 'passive', 'Gai Điện', 'fang', [{ k: 'status', id: 'burn', turns: 2, v: 0.05, on: 'foe' }], { trigger: 'onHit', chance: 0.35 }),
  c('linh_ngu', 'skill', 'Đớp Kép', 'fang', [{ k: 'extra', mult: 0.6 }], { cost: { mana: 25 } }),
  c('linh_ngu', 'ult', 'Lượn Sóng', 'wave', [{ k: 'dmg', mult: 0.7, hits: 2 }], { cost: { rage: 100, mana: 30 } }),
  c('linh_ngu', 'passive', 'Vảy Trơn', 'wind', [{ k: 'buff', stat: 'dodge', v: 0.12, turns: 99 }], { trigger: 'start' }),
  c('linh_ngu2', 'skill', 'Song Đớp', 'fang', [{ k: 'extra', mult: 0.8 }], { cost: { mana: 30 } }),
  c('linh_ngu2', 'ult', 'Xoáy Đôi', 'wave', [{ k: 'dmg', mult: 0.85, hits: 2 }], { cost: { rage: 100, mana: 35 } }),
  c('linh_ngu2', 'passive', 'Vảy Bạc', 'wind', [{ k: 'buff', stat: 'dodge', v: 0.15, turns: 99 }], { trigger: 'start' }),
];

// trận tra tướng và thẻ qua HERO, CARD: thêm lính vào đó (HEROES, bộ thẻ chung không đổi)
for (const m of MINIONS) HERO[m.id] = m;
for (const card of MINION_CARDS) CARD[card.id] = card;
