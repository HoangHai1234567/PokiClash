// Đền Huy Hiệu (side meta của GDD): 5 dãy theo hệ, mỗi dãy 5 bậc. Thắng chuỗi trận boss của hệ X để lên bậc;
// tướng hệ X được cộng Máu, Công, Thủ theo bậc cao nhất (không cộng dồn).
export const BADGE = {
  tiers: ['Đồng', 'Bạc', 'Vàng', 'Ngọc', 'Kim Cương'],
  counts: [5, 5, 10, 10, 10], // số trận mỗi bậc
  bonus: [0.05, 0.08, 0.12, 0.16, 0.2], // phần cộng Máu, Công, Thủ theo bậc cao nhất
  levelPerTier: 3, // cấp địch = cận dưới đề nghị của đảo + 3·(bậc − 1) + floor(trận / 2)
  ballsBase: 5, // mỗi trận thắng: 5 + 2·bậc bi
  ballsPerTier: 2,
  chest: ['chest_silver', 'chest_silver', 'chest_gold', 'chest_gold', 'chest_gold'] as const, // rương khi xong bậc
};

export const badgeBonus = (tier: number) => (tier > 0 ? BADGE.bonus[Math.min(tier, BADGE.bonus.length) - 1] : 0);
