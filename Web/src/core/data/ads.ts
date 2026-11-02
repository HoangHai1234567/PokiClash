// Quảng cáo thưởng và gói IAP (add-monetization-hooks). Mỗi chỗ đặt có giới hạn lượt mỗi ngày (0 = không giới hạn).
// Nguyên tắc: KHÔNG bán bi, đá tiềm năng hay lượt quay máy bi (đổi nguyên tắc này phải có change riêng được chủ dự án duyệt).
export const AD_LIMITS: Record<string, number> = {
  tree_double: 3, // hái cây bi ×2
  afk_chest_open: 4, // mở ngay rương AFK
  afk_boost: 3, // AFK ×2 trong 2 giờ
  farm_boost: 3, // năng suất trang trại ×2 trong 1 giờ
  cave_extra: 1, // +1 lượt Hang Tiềm Năng
};

// Thẻ Phiêu Lưu: cây bi ×1,5 (tốc độ và sức chứa), khay rương AFK 5 ô, rương AFK mở trong 1 giờ
export const PASS = { days: 30, treeMult: 1.5, afkSlots: 5, afkOpenH: 1 };

export const PRODUCTS: { id: 'adventure_pass' | 'no_ads'; name: string; desc: string }[] = [
  { id: 'adventure_pass', name: 'Thẻ Phiêu Lưu 30 ngày', desc: 'Cây bi ra nhanh ×1,5 và chứa ×1,5; khay rương AFK 5 ô; rương AFK mở trong 1 giờ.' },
  { id: 'no_ads', name: 'Bỏ quảng cáo', desc: 'Mọi chỗ quảng cáo thưởng trao thưởng ngay, không cần xem (vẫn theo giới hạn mỗi ngày).' },
];
