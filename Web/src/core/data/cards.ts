import type { CardDef } from '../types';

// Thẻ chung: mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ rút từ bộ này (thẻ mở dần theo cấp người chơi).
// "lượt này" = tới hết lượt của mình; "tới lượt sau" = che cả lượt địch kế tiếp.
export const POOL: CardDef[] = [
  // Thường
  { id: 'mai_vuot', name: 'Mài Vuốt', rarity: 'common', kind: 'pool', icon: 'claw', unlock: 1,
    effects: [{ k: 'buff', stat: 'atk', v: 0.25, turns: 1 }], flavor: 'Mài cho sắc rồi hẵng cào.' },
  { id: 'giap_go', name: 'Giáp Gỗ', rarity: 'common', kind: 'pool', icon: 'shield', unlock: 1,
    effects: [{ k: 'buff', stat: 'dmgTaken', v: -0.2, turns: 1, until: 'start' }], flavor: 'Gỗ thông, hơi thơm.' },
  { id: 'bang_gac', name: 'Băng Gạc', rarity: 'common', kind: 'pool', icon: 'bandage', unlock: 1,
    effects: [{ k: 'heal', pct: 0.08 }] },
  { id: 'hit_tho', name: 'Hít Thở', rarity: 'common', kind: 'pool', icon: 'drop', unlock: 1,
    effects: [{ k: 'mana', v: 15 }] },
  { id: 'gam_gu', name: 'Gầm Gừ', rarity: 'common', kind: 'pool', icon: 'flame', unlock: 1,
    effects: [{ k: 'rage', v: 15 }] },
  { id: 'nem_da', name: 'Ném Đá', rarity: 'common', kind: 'pool', icon: 'rock', unlock: 1,
    effects: [{ k: 'dmg', mult: 0.45 }], flavor: 'Viên to nhất nhặt được.' },
  // Khá
  { id: 'binh_thuoc', name: 'Bình Thuốc', rarity: 'uncommon', kind: 'pool', icon: 'potion', unlock: 1,
    effects: [{ k: 'heal', pct: 0.18 }] },
  { id: 'banh_bao', name: 'Bánh Bao Thịt', rarity: 'uncommon', kind: 'pool', icon: 'bun', unlock: 1,
    effects: [{ k: 'maxhp', pct: 0.12 }], flavor: 'Ăn xong thấy mình to ra.' },
  { id: 'lieu_mang', name: 'Liều Mạng', rarity: 'uncommon', kind: 'pool', icon: 'skull', unlock: 1,
    effects: [{ k: 'selfdmg', pctCur: 0.25 }, { k: 'buff', stat: 'atk', v: 0.5, turns: 1 }] },
  { id: 'thu_the', name: 'Thủ Thế', rarity: 'uncommon', kind: 'pool', icon: 'bubble', unlock: 1,
    effects: [{ k: 'shield', pct: 0.12 }] },
  { id: 'tinh_tam', name: 'Tĩnh Tâm', rarity: 'uncommon', kind: 'pool', icon: 'lotus', unlock: 1,
    effects: [{ k: 'mana', v: 30 }] },
  { id: 'dam_kep', name: 'Đấm Kép', rarity: 'uncommon', kind: 'pool', icon: 'fist2', unlock: 2,
    effects: [{ k: 'extra', mult: 0.5 }] },
  // Hiếm
  { id: 'cuong_no', name: 'Cuồng Nộ', rarity: 'rare', kind: 'pool', icon: 'rage', unlock: 1,
    effects: [{ k: 'buff', stat: 'atk', v: 1.0, turns: 1 }, { k: 'buff', stat: 'def', v: -0.3, turns: 2, until: 'start' }],
    flavor: 'Bỏ thủ, dồn hết vào một cú.' },
  { id: 'hut_mau', name: 'Hút Máu', rarity: 'rare', kind: 'pool', icon: 'fang', unlock: 3,
    effects: [{ k: 'buff', stat: 'lifesteal', v: 0.5, turns: 1 }] },
  { id: 'pha_giap', name: 'Phá Giáp', rarity: 'rare', kind: 'pool', icon: 'crack', unlock: 1,
    effects: [{ k: 'buff', stat: 'def', v: -0.3, turns: 2, until: 'end', on: 'foe' }] },
  { id: 'dot_lua', name: 'Đốt Lửa', rarity: 'rare', kind: 'pool', icon: 'torch', unlock: 3,
    effects: [{ k: 'status', id: 'burn', turns: 3, v: 0.06, on: 'foe' }] },
  { id: 'guong_doi', name: 'Gương Đôi', rarity: 'rare', kind: 'pool', icon: 'mirror', unlock: 5,
    effects: [{ k: 'double' }], flavor: 'Thẻ ngay sau nó chạy hai lần.' },
  { id: 'mat_ung', name: 'Mắt Ưng', rarity: 'rare', kind: 'pool', icon: 'eye', unlock: 5,
    effects: [{ k: 'buff', stat: 'crit', v: 0.5, turns: 1 }] },
  // Sử thi
  { id: 'bua_choang', name: 'Bùa Choáng', rarity: 'epic', kind: 'pool', icon: 'bolt', unlock: 7,
    effects: [{ k: 'status', id: 'stun', turns: 1, on: 'foe' }] },
  { id: 'hoa_khi', name: 'Hoà Khí', rarity: 'epic', kind: 'pool', icon: 'yinyang', unlock: 7,
    effects: [{ k: 'mana', v: 30 }, { k: 'rage', v: 30 }] },
  { id: 'ao_choang', name: 'Áo Choàng Ma', rarity: 'epic', kind: 'pool', icon: 'ghost', unlock: 7,
    effects: [{ k: 'status', id: 'evade', turns: 1, on: 'self' }] },
  // Huyền thoại
  { id: 'nghich_thien', name: 'Nghịch Thiên', rarity: 'legend', kind: 'pool', icon: 'phoenix', unlock: 10,
    effects: [{ k: 'ifLow', below: 0.5,
      then: [{ k: 'heal', pct: 0.4 }, { k: 'buff', stat: 'atk', v: 0.6, turns: 1 }],
      else: [{ k: 'buff', stat: 'atk', v: 0.3, turns: 1 }] }] },
  { id: 'thien_menh', name: 'Thiên Mệnh', rarity: 'legend', kind: 'pool', icon: 'crown', unlock: 10,
    effects: [{ k: 'trueStrike', mult: 1.5 }] },
];

// Thẻ nội tại: mỗi tướng 3 thẻ (chiêu tốn mana, tuyệt kỹ cần đủ nộ và mana, bị động). Nâng cấp bằng cách thu thập bản sao.
// 6 tướng có bộ thẻ riêng:
const OWN: CardDef[] = [
  // Võ Sư (Thổ)
  { id: 'vs_skill', owner: 'vo_su', name: 'Thiết Quyền', rarity: 'common', kind: 'skill', icon: 'fist', cost: { mana: 30 },
    effects: [{ k: 'dmg', mult: 1.2 }, { k: 'rage', v: 10 }] },
  { id: 'vs_ult', owner: 'vo_su', name: 'Bách Liệt Quyền', rarity: 'rare', kind: 'ult', icon: 'fist2', cost: { rage: 100, mana: 40 },
    effects: [{ k: 'dmg', mult: 0.5, hits: 5 }] },
  { id: 'vs_pas', owner: 'vo_su', name: 'Da Đồng', rarity: 'common', kind: 'passive', icon: 'shield', trigger: 'start',
    effects: [{ k: 'buff', stat: 'def', v: 0.15, turns: 99 }] },
  // Võ Tăng Bồ Đề (Hỏa)
  { id: 'bd_skill', owner: 'bo_de', name: 'Liên Hoa Hỏa', rarity: 'uncommon', kind: 'skill', icon: 'torch', cost: { mana: 35 },
    effects: [{ k: 'dmg', mult: 1.0 }, { k: 'status', id: 'burn', turns: 3, v: 0.05, on: 'foe' }] },
  { id: 'bd_ult', owner: 'bo_de', name: 'Hỏa Dực Phần Thiên', rarity: 'epic', kind: 'ult', icon: 'phoenix', cost: { rage: 100, mana: 40 },
    effects: [{ k: 'dmg', mult: 2.6 }, { k: 'status', id: 'burn', turns: 3, v: 0.08, on: 'foe' }] },
  { id: 'bd_pas', owner: 'bo_de', name: 'Lửa Thiền', rarity: 'rare', kind: 'passive', icon: 'flame', trigger: 'onAttack', chance: 0.3,
    effects: [{ k: 'status', id: 'burn', turns: 2, v: 0.05, on: 'foe' }] },
  // Thiền Sư Pháp Luân (Hỏa)
  { id: 'pl_skill', owner: 'phap_luan', name: 'Pháp Luân Chuyển', rarity: 'rare', kind: 'skill', icon: 'wheel', cost: { mana: 40 },
    effects: [{ k: 'dmg', mult: 1.3 }, { k: 'mana', v: -20, on: 'foe' }] },
  { id: 'pl_ult', owner: 'phap_luan', name: 'Đại Pháp Luân', rarity: 'epic', kind: 'ult', icon: 'sun', cost: { rage: 100, mana: 50 },
    effects: [{ k: 'dmg', mult: 2.2 }, { k: 'status', id: 'stun', turns: 1, on: 'foe' }] },
  { id: 'pl_pas', owner: 'phap_luan', name: 'Thiền Định', rarity: 'rare', kind: 'passive', icon: 'lotus', trigger: 'turnStart',
    effects: [{ k: 'mana', v: 10 }] },
  // Đại Sư Cà Sa (Thổ)
  { id: 'cs_skill', owner: 'ca_sa', name: 'Khói Hương', rarity: 'rare', kind: 'skill', icon: 'incense', cost: { mana: 40 },
    effects: [{ k: 'heal', pct: 0.25 }, { k: 'cleanse' }] },
  { id: 'cs_ult', owner: 'ca_sa', name: 'Kim Cang Pháp Tướng', rarity: 'legend', kind: 'ult', icon: 'crown', cost: { rage: 100, mana: 50 },
    effects: [{ k: 'dmg', mult: 3.0 }, { k: 'shield', pct: 0.3 }] },
  // đổi 2026-10-31: từ "dưới 30% máu hồi 35%" thành hồi sinh (GDD: thẻ hồi sinh)
  { id: 'cs_pas', owner: 'ca_sa', name: 'Phật Tâm', rarity: 'epic', kind: 'passive', icon: 'heart', trigger: 'death',
    effects: [{ k: 'revive', pct: 0.35 }] },
  // Lam Quân (Thủy, trước 2026-11-02 là Kim)
  { id: 'lq_skill', owner: 'lam_quan', name: 'Chuông Đồng', rarity: 'common', kind: 'skill', icon: 'bell', cost: { mana: 30 },
    effects: [{ k: 'dmg', mult: 1.0 }, { k: 'status', id: 'stun', turns: 1, chance: 0.3, on: 'foe' }] },
  { id: 'lq_ult', owner: 'lam_quan', name: 'Hồng Chung', rarity: 'uncommon', kind: 'ult', icon: 'bell', cost: { rage: 100, mana: 40 },
    effects: [{ k: 'dmg', mult: 2.3 }, { k: 'buff', stat: 'def', v: -0.2, turns: 2, until: 'end', on: 'foe' }] },
  { id: 'lq_pas', owner: 'lam_quan', name: 'Vỏ Thép', rarity: 'common', kind: 'passive', icon: 'bubble', trigger: 'start',
    effects: [{ k: 'shield', pct: 0.12 }] },
  // Tiểu Y (Thủy)
  { id: 'ty_skill', owner: 'tieu_y', name: 'Bọt Nước', rarity: 'common', kind: 'skill', icon: 'bubble', cost: { mana: 25 },
    effects: [{ k: 'dmg', mult: 0.9 }, { k: 'buff', stat: 'atk', v: -0.15, turns: 1, until: 'end', on: 'foe' }] },
  { id: 'ty_ult', owner: 'tieu_y', name: 'Vòi Rồng Nhỏ', rarity: 'uncommon', kind: 'ult', icon: 'wave', cost: { rage: 100, mana: 35 },
    effects: [{ k: 'dmg', mult: 2.0 }, { k: 'heal', pct: 0.15 }] },
  { id: 'ty_pas', owner: 'tieu_y', name: 'Mát Lành', rarity: 'common', kind: 'passive', icon: 'drop', trigger: 'turnStart',
    effects: [{ k: 'heal', pct: 0.04 }] },
];

// Bộ thẻ của các tướng cũ đã gộp thành dạng của tướng khác hoặc bị bỏ (bản lưu v3): chỉ làm mẫu cho thẻ tạm, không có trong game.
const OLD_KITS: CardDef[] = [
  // Gia Bỉ (Mộc)
  { id: 'gb_skill', owner: 'gia_bi', name: 'Hạt Giống', rarity: 'common', kind: 'skill', icon: 'seed', cost: { mana: 25 },
    effects: [{ k: 'status', id: 'regen', turns: 3, v: 0.07, on: 'self' }, { k: 'dmg', mult: 0.6 }] },
  { id: 'gb_ult', owner: 'gia_bi', name: 'Rừng Gai', rarity: 'uncommon', kind: 'ult', icon: 'leaf', cost: { rage: 100, mana: 35 },
    effects: [{ k: 'dmg', mult: 2.1 }, { k: 'buff', stat: 'def', v: -0.2, turns: 2, until: 'end', on: 'foe' }] },
  { id: 'gb_pas', owner: 'gia_bi', name: 'Quang Hợp', rarity: 'common', kind: 'passive', icon: 'sun', trigger: 'turnStart',
    effects: [{ k: 'rage', v: 8 }] },
  // Sứ Giả Gia Bỉ (Mộc)
  { id: 'sg_skill', owner: 'su_gia', name: 'Nanh Gió', rarity: 'uncommon', kind: 'skill', icon: 'fang', cost: { mana: 35 },
    effects: [{ k: 'dmg', mult: 0.75, hits: 2 }] },
  { id: 'sg_ult', owner: 'su_gia', name: 'Phong Mộc Sứ', rarity: 'epic', kind: 'ult', icon: 'wind', cost: { rage: 100, mana: 45 },
    effects: [{ k: 'dmg', mult: 2.4 }, { k: 'buff', stat: 'atk', v: 0.3, turns: 2 }] },
  { id: 'sg_pas', owner: 'su_gia', name: 'Nhanh Nhẹn', rarity: 'rare', kind: 'passive', icon: 'feather', trigger: 'start',
    effects: [{ k: 'buff', stat: 'dodge', v: 0.15, turns: 99 }] },
  // Vạn Quân (Kim)
  { id: 'vq_skill', owner: 'van_quan', name: 'Đại Chùy', rarity: 'uncommon', kind: 'skill', icon: 'hammer', cost: { mana: 40 },
    effects: [{ k: 'dmg', mult: 1.6 }] },
  { id: 'vq_ult', owner: 'van_quan', name: 'Vạn Quân Lôi Chung', rarity: 'epic', kind: 'ult', icon: 'bolt', cost: { rage: 100, mana: 45 },
    effects: [{ k: 'dmg', mult: 2.8 }, { k: 'status', id: 'stun', turns: 1, on: 'foe' }] },
  { id: 'vq_pas', owner: 'van_quan', name: 'Giáp Trụ', rarity: 'rare', kind: 'passive', icon: 'helmet', trigger: 'start',
    effects: [{ k: 'buff', stat: 'dmgTaken', v: -0.12, turns: 99 }] },
  // Hắc Dực Vạn Quân (Kim)
  { id: 'hd_skill', owner: 'hac_duc', name: 'Hắc Dực Trảm', rarity: 'rare', kind: 'skill', icon: 'wing', cost: { mana: 40 },
    effects: [{ k: 'dmg', mult: 1.5, lifesteal: 0.3 }] },
  { id: 'hd_ult', owner: 'hac_duc', name: 'Hắc Vũ Thiên Chung', rarity: 'legend', kind: 'ult', icon: 'moon', cost: { rage: 100, mana: 50 },
    effects: [{ k: 'dmg', mult: 3.2, pierce: 0.5 }] },
  { id: 'hd_pas', owner: 'hac_duc', name: 'Cánh Đêm', rarity: 'epic', kind: 'passive', icon: 'wing', trigger: 'lowHp', below: 0.5,
    effects: [{ k: 'buff', stat: 'atk', v: 0.25, turns: 99 }] },
  // Y Trạch (Thủy)
  { id: 'yt_skill', owner: 'y_trach', name: 'Đinh Ba', rarity: 'uncommon', kind: 'skill', icon: 'trident', cost: { mana: 35 },
    effects: [{ k: 'dmg', mult: 1.4 }, { k: 'buff', stat: 'def', v: -0.2, turns: 2, until: 'end', on: 'foe' }] },
  { id: 'yt_ult', owner: 'y_trach', name: 'Hải Long Quyển', rarity: 'epic', kind: 'ult', icon: 'wave', cost: { rage: 100, mana: 45 },
    effects: [{ k: 'dmg', mult: 2.5 }, { k: 'heal', pct: 0.25 }] },
  { id: 'yt_pas', owner: 'y_trach', name: 'Thủy Triều', rarity: 'rare', kind: 'passive', icon: 'wave', trigger: 'onHit',
    effects: [{ k: 'mana', v: 8 }, { k: 'rage', v: 4 }] },
];

// Thẻ tạm (2026-11-02, thiết kế thẻ riêng sau): tướng mới chép bộ 3 thẻ của một tướng mẫu cùng hệ, độ hiếm gần nhất (cách đều
// thì lấy mẫu thấp hơn). Id <tướng>_skill, _ult, _pas; tên, số, độ hiếm giữ như mẫu.
export const BORROW: Record<string, string> = {
  // Kim: mẫu Lam Quân (Thường), Vạn Quân (Hiếm), Hắc Dực (Sử thi)
  bu_long: 'lam_quan', phao_hop: 'lam_quan', kiem_linh: 'lam_quan', meo_quyen: 'lam_quan',
  bo_cap: 'van_quan', bo_ngua: 'van_quan', soi_linh: 'hac_duc', bach_ho: 'hac_duc',
  // Mộc: mẫu Gia Bỉ (Thường), Sứ Giả (Hiếm)
  mam_go: 'gia_bi', nu_hoa: 'gia_bi', kien_binh: 'gia_bi', banh_tet: 'gia_bi',
  de_hoa: 'su_gia', giac_long: 'su_gia', phong_linh: 'su_gia', thanh_long: 'su_gia',
  // Thủy: mẫu Tiểu Y (Thường), Y Trạch (Hiếm)
  canh_cut: 'tieu_y', giot_suong: 'tieu_y', tam_tay: 'tieu_y', ca_ngua: 'y_trach', map_rang: 'y_trach', huyen_vu: 'y_trach',
  // Hỏa: mẫu Bồ Đề (Hiếm), Pháp Luân (Sử thi)
  heo_lua: 'bo_de', dom_lua: 'bo_de', phao_tet: 'bo_de', su_tu_lua: 'bo_de', ho_lua: 'bo_de', chu_tuoc: 'phap_luan',
  // Thổ: mẫu Võ Sư (Thường), Cà Sa (Huyền thoại)
  gau_mo: 'vo_su', soc_da: 'vo_su', bo_hung: 'vo_su', thach_nhan: 'vo_su', sa_than: 'vo_su', ky_lan: 'ca_sa',
};
const SUFFIX = { skill: 'skill', ult: 'ult', passive: 'pas' } as const;
const borrow = (hero: string, from: string): CardDef[] =>
  [...OWN, ...OLD_KITS]
    .filter((c) => c.owner === from)
    .map((c) => ({ ...(JSON.parse(JSON.stringify(c)) as CardDef), id: `${hero}_${SUFFIX[c.kind as keyof typeof SUFFIX]}`, owner: hero }));

export const INNATE: CardDef[] = [...OWN, ...Object.entries(BORROW).flatMap(([h, from]) => borrow(h, from))];

export const CARD: Record<string, CardDef> = Object.fromEntries([...POOL, ...INNATE].map((c) => [c.id, c]));

// trọng số rút thẻ chung theo độ hiếm
export const POOL_WEIGHT = { common: 50, uncommon: 30, rare: 14, epic: 5, legend: 1 } as const;
