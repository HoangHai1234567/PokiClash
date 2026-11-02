// Trang trại (side meta của GDD): 8 chỗ làm, mỗi chỗ hợp một hệ; tướng làm ra bi theo sức (độ hiếm, sao), hết sức thì ngồi nghỉ,
// rút ra phải nghỉ 15–60 phút mới vào lại. Sức làm tách khỏi trận. Ca dài như cây bi (chốt 2026-10-31): người vào 2 lần mỗi ngày
// không mất phần lớn sản lượng. Mọi số là giá trị khởi điểm.
import type { Elem } from '../types';

export const FARM = {
  minHeroes: 3, // mở khi có từ 3 tướng
  base: 2, // bi mỗi giờ của tướng Thường 1 sao
  rarityPower: [1, 1.1, 1.22, 1.36, 1.5], // như chỉ số tướng
  lvStep: 0, // không tăng theo cấp
  starStep: 0.1,
  match: 1.25, // đúng hệ hợp
  durBase: 8, // giờ làm = 8 + 1·(sao − 1)
  durStar: 1,
  durRarity: 0,
  restPerHour: 15, // phút nghỉ = clamp(giờ làm × 15, 15, 60)
  restMin: 15,
  restMax: 60,
  capHours: 10, // kho mỗi chỗ giữ tối đa 10 giờ sản lượng
  openSpots: 3, // lúc mở có 3 chỗ; mở thêm theo cấp
  spotLevels: [8, 11, 14, 17, 20],
  boostH: 1, // quảng cáo: năng suất ×2 trong 1 giờ
  boostMult: 2,
};

// 8 chỗ theo thứ tự mở (mỗi hệ một chỗ trước); x, y: toạ độ 0..1 trên ảnh đảo trang trại
export const FARM_SPOTS: { id: string; kind: 'duck' | 'veg' | 'orchard' | 'bakery' | 'smithy'; name: string; elem: Elem; x: number; y: number }[] = [
  { id: 'duck1', kind: 'duck', name: 'Ao vịt', elem: 'thuy', x: 0.26, y: 0.3 },
  { id: 'veg1', kind: 'veg', name: 'Ruộng rau', elem: 'tho', x: 0.72, y: 0.3 },
  { id: 'orchard1', kind: 'orchard', name: 'Vườn cây', elem: 'moc', x: 0.26, y: 0.48 },
  { id: 'bakery', kind: 'bakery', name: 'Lò bánh', elem: 'hoa', x: 0.72, y: 0.48 },
  { id: 'smithy', kind: 'smithy', name: 'Xưởng nông cụ', elem: 'kim', x: 0.26, y: 0.66 },
  { id: 'duck2', kind: 'duck', name: 'Ao vịt', elem: 'thuy', x: 0.72, y: 0.66 },
  { id: 'veg2', kind: 'veg', name: 'Ruộng rau', elem: 'tho', x: 0.26, y: 0.84 },
  { id: 'orchard2', kind: 'orchard', name: 'Vườn cây', elem: 'moc', x: 0.72, y: 0.84 },
];
