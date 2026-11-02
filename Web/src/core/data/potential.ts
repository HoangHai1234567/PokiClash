// Tiềm năng (side meta của GDD): 4 ô mỗi tướng, mở theo sao; khai phá tốn đá, quay mỗi ô một dòng (loại và độ hiếm).
// Hang Tiềm Năng: 4 tầng, mỗi lần vào một trận boss phải tự chơi, thắng ra đá.
import type { Elem } from '../types';

export type PotKind = 'atk' | 'def' | 'hp' | 'spd' | 'crit' | 'lifesteal' | 'mana' | 'rage';
// một dòng tiềm năng: loại và độ hiếm (0 Thường … 4 Huyền thoại)
export interface PotLine {
  k: PotKind;
  r: number;
}

export const POTENTIAL = {
  kinds: ['atk', 'def', 'hp', 'spd', 'crit', 'lifesteal', 'mana', 'rage'] as PotKind[],
  // giá trị theo độ hiếm; phần trăm ghi dạng 0,03
  values: {
    atk: [0.03, 0.05, 0.08, 0.12, 0.16],
    def: [0.03, 0.05, 0.08, 0.12, 0.16],
    hp: [0.03, 0.05, 0.08, 0.12, 0.16],
    spd: [2, 4, 6, 9, 12],
    crit: [0.02, 0.03, 0.05, 0.07, 0.1],
    lifesteal: [0.02, 0.03, 0.05, 0.07, 0.1],
    mana: [5, 10, 15, 20, 30],
    rage: [5, 10, 15, 20, 30],
  } as Record<PotKind, number[]>,
  rarityWeight: [55, 28, 12, 4.5, 0.5],
  // trần tổng mỗi loại
  caps: { atk: 0.4, def: 0.4, hp: 0.4, spd: 30, crit: 0.4, lifesteal: 0.4, mana: 50, rage: 50 } as Record<PotKind, number>,
  slotStar: [1, 2, 3, 4], // ô i mở ở slotStar[i] sao
  lockCost: 2, // mỗi ô khoá tốn thêm 2 đá
  maxLocks: 2,
};

export const CAVE = {
  tiers: [
    { name: 'Dễ', level: 6, stones: 2 },
    { name: 'Thường', level: 12, stones: 3 },
    { name: 'Khó', level: 18, stones: 5 },
    { name: 'Ác mộng', level: 24, stones: 8 },
  ],
  winsPerDay: 3, // chỉ trừ lượt khi thắng
  adExtra: 1, // xem quảng cáo thêm 1 lượt mỗi ngày
  // hệ boss theo thứ trong tuần (0 = Chủ nhật); null = người chơi chọn
  weekday: [null, 'kim', 'moc', 'thuy', 'hoa', 'tho', null] as (Elem | null)[],
};

// tổng mỗi loại từ các dòng (hai ô cùng loại thì cộng dồn), chặn ở trần
export function potentialTotals(lines: readonly (PotLine | null)[] | undefined): Record<PotKind, number> {
  const t = { atk: 0, def: 0, hp: 0, spd: 0, crit: 0, lifesteal: 0, mana: 0, rage: 0 } as Record<PotKind, number>;
  for (const x of lines ?? []) if (x) t[x.k] += POTENTIAL.values[x.k][x.r];
  for (const k of POTENTIAL.kinds) t[k] = Math.min(POTENTIAL.caps[k], t[k]);
  return t;
}
