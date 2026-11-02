// Cây bi (chốt 2026-10-31, học cây sinh bi của Clash of Critters): nguồn bi thụ động chính, thay phần bi theo giờ của AFK.
// Mỗi cây ra bi đều tay, đầy thì ngừng, người chơi vào hái. Mọi số là giá trị khởi điểm.
import type { Elem } from '../types';

export const TREES = {
  perHour: 5, // bi mỗi giờ mỗi cây
  cap: 50, // mỗi cây chứa tối đa 50 bi (đầy sau 10 giờ), đầy thì ngừng
  // cây 1 mở khi qua ải 1; cây 2–5 mở khi qua boss Đảo Thủy, Hỏa, Kim, Mộc
  unlockZones: ['thuy', 'hoa', 'kim', 'moc'] as Elem[],
};
