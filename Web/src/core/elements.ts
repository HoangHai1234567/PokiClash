import type { Elem, Rarity } from './types';

// Ngũ hành tương khắc: Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy, Thủy khắc Hỏa, Hỏa khắc Kim
export const BEATS: Record<Elem, Elem> = { kim: 'moc', moc: 'tho', tho: 'thuy', thuy: 'hoa', hoa: 'kim' };
export const ELEMS: Elem[] = ['kim', 'moc', 'thuy', 'hoa', 'tho'];

export const ELEM_NAME: Record<Elem, string> = { kim: 'Kim', moc: 'Mộc', thuy: 'Thủy', hoa: 'Hỏa', tho: 'Thổ' };
export const ELEM_COLOR: Record<Elem, string> = {
  kim: '#b8c4cf',
  moc: '#6cbf4f',
  thuy: '#4a90d9',
  hoa: '#e8553f',
  tho: '#e2a93b',
};

export const RARITY_NAME: Record<Rarity, string> = {
  common: 'Thường',
  uncommon: 'Khá',
  rare: 'Hiếm',
  epic: 'Sử thi',
  legend: 'Huyền thoại',
};
export const RARITY_COLOR: Record<Rarity, string> = {
  common: '#b9b1a3',
  uncommon: '#6cbf4f',
  rare: '#4a90d9',
  epic: '#9a6ad6',
  legend: '#f39a2d',
};
export const RARITY_INDEX: Record<Rarity, number> = { common: 0, uncommon: 1, rare: 2, epic: 3, legend: 4 };

export const ELEM_STRONG = 1.5;
export const ELEM_WEAK = 0.75;

export function elemMult(att: Elem, def: Elem): number {
  if (BEATS[att] === def) return ELEM_STRONG;
  if (BEATS[def] === att) return ELEM_WEAK;
  return 1;
}
