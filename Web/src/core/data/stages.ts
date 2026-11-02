import type { Elem } from '../types';

// 5 đảo theo hệ, không khoá đảo nào: đảo sau mạnh hơn hẳn nên vào sớm là thua.
// Thứ tự gợi ý Thủy → Hỏa → Kim → Mộc → Thổ: mỗi đảo rơi tướng hệ của đảo đó, đúng là hệ khắc đảo kế tiếp
// (Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ). Trong một đảo, ải mở lần lượt.

export interface StageEnemy {
  hero: string;
  level: number;
  boss?: boolean;
}
export interface StageDrop {
  hero: string;
  chance: number;
  min: number;
  max: number;
  gift?: boolean; // tướng tặng khi qua ải lần đầu (đủ mảnh mở luôn)
}
export interface StageDef {
  id: number; // số toàn cục 1..40
  zone: Elem;
  idx: number; // 1..8 trong đảo
  name: string;
  kind: 'normal' | 'mini' | 'boss';
  enemies: StageEnemy[];
  drops: StageDrop[];
}
export interface ZoneDef {
  id: Elem;
  order: number; // 0..4, độ khó tăng dần
  name: string;
  sub: string;
  level: [number, number]; // cấp đề nghị
  art: string; // public/art/<art>.png
  sky: [string, string];
  ground: string;
  sea: string;
  // vị trí 8 ải trên ảnh đảo (tỉ lệ 0..1 theo khung 9:16), dọc đường mòn từ bãi dưới lên hang boss
  nodes: [number, number][];
  // vị trí vùng này trên ảnh đảo lớn
  world: [number, number];
}

export const ZONES: ZoneDef[] = [
  {
    id: 'thuy', order: 0, name: 'Đảo Thủy', sub: 'Đầm phá, thác bạc và xoáy nước đinh ba', level: [1, 7], art: 'zone_thuy',
    sky: ['#bfe6f5', '#f4f1dc'], ground: '#8fc9d8', sea: '#3fb3c9',
    nodes: [[0.4, 0.86], [0.4, 0.75], [0.4, 0.64], [0.46, 0.53], [0.55, 0.44], [0.5, 0.34], [0.6, 0.26], [0.66, 0.15]],
    world: [0.23, 0.66],
  },
  {
    id: 'hoa', order: 1, name: 'Đảo Hỏa', sub: 'Dung nham, chùa sen lửa và miệng núi cháy', level: [6, 12], art: 'zone_hoa',
    sky: ['#f7c9a8', '#fbe9d0'], ground: '#d98a5a', sea: '#7a3a2a',
    nodes: [[0.32, 0.91], [0.48, 0.81], [0.36, 0.7], [0.43, 0.57], [0.6, 0.48], [0.55, 0.36], [0.42, 0.26], [0.56, 0.09]],
    world: [0.5, 0.17],
  },
  {
    id: 'kim', order: 2, name: 'Đảo Kim', sub: 'Núi thép, cầu bánh răng và tháp chuông đồng', level: [11, 17], art: 'zone_kim',
    sky: ['#d6dee8', '#f1efe6'], ground: '#a9b6c2', sea: '#3d7fb5',
    nodes: [[0.4, 0.84], [0.44, 0.72], [0.46, 0.62], [0.58, 0.52], [0.68, 0.42], [0.62, 0.33], [0.54, 0.24], [0.64, 0.12]],
    world: [0.8, 0.33],
  },
  {
    id: 'moc', order: 3, name: 'Đảo Mộc', sub: 'Rừng nấm, dây leo và cây thần ngàn năm', level: [16, 22], art: 'zone_moc',
    sky: ['#cfeec0', '#f4f1dc'], ground: '#7cc06a', sea: '#3fb3a0',
    nodes: [[0.5, 0.87], [0.36, 0.77], [0.5, 0.67], [0.64, 0.58], [0.48, 0.49], [0.34, 0.4], [0.48, 0.3], [0.52, 0.15]],
    world: [0.18, 0.32],
  },
  {
    id: 'tho', order: 4, name: 'Đảo Thổ', sub: 'Vách đất nung, ruộng bậc thang và kim tự viện', level: [21, 28], art: 'zone_tho',
    sky: ['#f6dfae', '#fbf0d8'], ground: '#d9b46a', sea: '#3fb3c9',
    nodes: [[0.46, 0.87], [0.62, 0.78], [0.48, 0.69], [0.34, 0.6], [0.5, 0.51], [0.66, 0.42], [0.5, 0.31], [0.5, 0.15]],
    world: [0.7, 0.67],
  },
];
export const ZONE: Record<Elem, ZoneDef> = Object.fromEntries(ZONES.map((z) => [z.id, z])) as Record<Elem, ZoneDef>;
// làng ở giữa đảo lớn (máy bi)
export const WORLD_VILLAGE: [number, number] = [0.5, 0.44];

const e = (hero: string, level: number, boss = false): StageEnemy => ({ hero, level, boss });
const d = (hero: string, chance: number, min: number, max: number, gift = false): StageDrop => ({ hero, chance, min, max, gift });

type Row = [string, StageDef['kind'], StageEnemy[], StageDrop[]];
// 40 tướng (2026-11-02): giữ tên, loại, cấp, lượng rơi của mọi ải; tướng đã gộp hoặc bỏ (Y Trạch, Vạn Quân, Hắc Dực, Gia Bỉ,
// Sứ Giả) và Lam Quân (sang Thủy) thay bằng tướng mới cùng hệ, cùng độ hiếm. Xếp lại địch theo vai của từng dòng là việc sau.
const RAW: Record<Elem, Row[]> = {
  thuy: [
    ['Bãi Vỏ Sò', 'normal', [e('tieu_y', 1)], []],
    ['Vũng San Hô', 'normal', [e('canh_cut', 2)], []],
    ['Cầu Gỗ Rêu', 'normal', [e('tieu_y', 2), e('tieu_y', 3)], [d('vo_su', 1, 10, 10, true)]],
    ['Ngọn Hải Đăng', 'mini', [e('ca_ngua', 3, true)], [d('ca_ngua', 1, 3, 5)]],
    ['Làng Vỏ Ốc', 'normal', [e('canh_cut', 4), e('ca_ngua', 4)], []],
    ['Thác Bạc', 'normal', [e('ca_ngua', 5), e('tieu_y', 5)], [d('nu_hoa', 1, 10, 10, true)]],
    ['Hồ Gương', 'normal', [e('tieu_y', 5), e('map_rang', 5), e('canh_cut', 5)], [d('map_rang', 0.3, 1, 2)]],
    ['Xoáy Nước Đinh Ba', 'boss', [e('canh_cut', 5), e('map_rang', 6, true)], [d('map_rang', 1, 4, 6)]],
  ],
  hoa: [
    ['Bến Đá Đen', 'normal', [e('bo_de', 6)], []],
    ['Suối Dung Nham', 'normal', [e('bo_de', 7)], []],
    ['Chùa Liên Hoa', 'normal', [e('bo_de', 7), e('bo_de', 8)], [d('bo_de', 0.3, 1, 2)]],
    ['Lò Lửa Thiền', 'mini', [e('bo_de', 9, true)], [d('bo_de', 1, 3, 5)]],
    ['Rừng Than Hồng', 'normal', [e('bo_de', 9), e('phap_luan', 8)], []],
    ['Cổng Bánh Xe', 'normal', [e('phap_luan', 10)], [d('phap_luan', 0.25, 1, 2)]],
    ['Sườn Núi Khói', 'normal', [e('bo_de', 9), e('phap_luan', 9), e('bo_de', 9)], []],
    ['Miệng Núi Lửa', 'boss', [e('bo_de', 9), e('phap_luan', 11, true)], [d('phap_luan', 1, 4, 6), d('bo_de', 0.5, 2, 3)]],
  ],
  kim: [
    ['Cảng Sắt', 'normal', [e('bu_long', 11)], []],
    ['Cầu Bánh Răng', 'normal', [e('phao_hop', 12)], [d('phao_hop', 0.3, 1, 2)]],
    ['Tháp Canh Thép', 'normal', [e('bu_long', 12), e('phao_hop', 13)], []],
    ['Gác Chuông Đồng', 'mini', [e('bo_cap', 13, true)], [d('bu_long', 1, 4, 6)]],
    ['Mỏ Sắt Ngân', 'normal', [e('bo_ngua', 15), e('bu_long', 15)], []],
    ['Xưởng Đúc Chuông', 'normal', [e('bo_cap', 16)], [d('bo_cap', 0.3, 1, 2)]],
    ['Tổ Cánh Đêm', 'normal', [e('soi_linh', 16)], [d('soi_linh', 0.25, 1, 2)]],
    ['Thiên Chung Hắc Dực', 'boss', [e('bo_ngua', 15), e('soi_linh', 17, true)], [d('soi_linh', 1, 4, 6), d('bo_ngua', 0.5, 2, 3)]],
  ],
  moc: [
    ['Bờ Rêu', 'normal', [e('nu_hoa', 16)], []],
    ['Đồi Nấm', 'normal', [e('mam_go', 17)], []],
    ['Rừng Dây Leo', 'normal', [e('nu_hoa', 17), e('mam_go', 18)], []],
    ['Hang Nanh Gió', 'mini', [e('de_hoa', 18, true)], [d('de_hoa', 1, 3, 5)]],
    ['Đồng Hoa Sáng', 'normal', [e('giac_long', 19), e('nu_hoa', 19)], []],
    ['Cây Cổ Thụ Con', 'normal', [e('giac_long', 20)], [d('giac_long', 0.3, 1, 2)]],
    ['Thung Lũng Lá', 'normal', [e('mam_go', 20), e('de_hoa', 20), e('nu_hoa', 20)], []],
    ['Cây Thần Ngàn Năm', 'boss', [e('mam_go', 20), e('giac_long', 22, true)], [d('giac_long', 1, 4, 6)]],
  ],
  tho: [
    ['Bãi Cát Vàng', 'normal', [e('vo_su', 21)], []],
    ['Đồi Đất Nung', 'normal', [e('vo_su', 22)], []],
    ['Cầu Treo', 'normal', [e('vo_su', 22), e('vo_su', 23)], []],
    ['Võ Đường Đá', 'mini', [e('vo_su', 24, true)], [d('vo_su', 1, 3, 5)]],
    ['Ruộng Bậc Thang', 'normal', [e('vo_su', 24), e('ca_sa', 21)], []],
    ['Chùa Đá', 'normal', [e('ca_sa', 22)], [d('ca_sa', 0.2, 1, 2)]],
    ['Sân Tượng Đá', 'normal', [e('vo_su', 25), e('ca_sa', 23), e('vo_su', 25)], []],
    ['Kim Tự Viện', 'boss', [e('vo_su', 24), e('ca_sa', 23, true)], [d('ca_sa', 1, 5, 8)]],
  ],
};

export const STAGES: StageDef[] = [];
for (const z of ZONES)
  RAW[z.id].forEach(([name, kind, enemies, drops], i) =>
    STAGES.push({ id: STAGES.length + 1, zone: z.id, idx: i + 1, name, kind, enemies, drops }));

export const STAGE: Record<number, StageDef> = Object.fromEntries(STAGES.map((s) => [s.id, s]));
export const zoneStages = (z: Elem) => STAGES.filter((s) => s.zone === z);
