// Cổng quảng cáo thưởng: đếm lượt theo chỗ đặt trong ngày (theo giờ máy). Ngày mới thì đặt lại; giờ máy lùi về ngày trước
// thì giữ nguyên số đã dùng (không mở lại lượt). Quyền lợi gói: Thẻ Phiêu Lưu (hạn), Bỏ quảng cáo (cờ).
import { AD_LIMITS, PASS } from './data/ads';
import type { SaveData } from './progression';

export const UNLIMITED = 999;

export interface AdState {
  day: number;
  used: Record<string, number>;
}
export interface Entitlements {
  passUntil: number; // ms: hết Thẻ Phiêu Lưu
  noAds: boolean;
}

export function adsOf(s: SaveData): AdState {
  if (!s.ads) s.ads = { day: 0, used: {} };
  return s.ads;
}
function roll(s: SaveData, day: number): AdState {
  const a = adsOf(s);
  if (day > a.day) {
    a.day = day;
    a.used = {};
  }
  return a;
}
export const adUsed = (s: SaveData, day: number, p: string) => roll(s, day).used[p] ?? 0;
export function adLeft(s: SaveData, day: number, p: string): number {
  const lim = AD_LIMITS[p] ?? 0;
  return lim > 0 ? lim - adUsed(s, day, p) : UNLIMITED;
}
export function adUse(s: SaveData, day: number, p: string): boolean {
  if (adLeft(s, day, p) <= 0) return false;
  const a = roll(s, day);
  a.used[p] = (a.used[p] ?? 0) + 1;
  return true;
}

export function entOf(s: SaveData): Entitlements {
  if (!s.ent) s.ent = { passUntil: 0, noAds: false };
  return s.ent;
}
export const passActive = (s: SaveData, now: number) => (s.ent?.passUntil ?? 0) > now;

// bước di chuyển bản lưu v2 -> v3: bộ đếm quảng cáo riêng của AFK, trang trại, hang dồn về ads (chỉ giữ số của ngày mới nhất)
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function migrateAdsV2(o: any): void {
  const af = o.afk ?? {}, fm = o.farm ?? {}, cv = o.cave ?? {};
  const day = Math.max(af.adDay ?? 0, fm.adDay ?? 0, cv.ad ? (cv.day ?? 0) : 0);
  const used: Record<string, number> = {};
  if (day > 0) {
    if (af.adDay === day && af.adOpen > 0) used.afk_chest_open = af.adOpen;
    if (af.adDay === day && af.adBoost > 0) used.afk_boost = af.adBoost;
    if (fm.adDay === day && fm.adCount > 0) used.farm_boost = fm.adCount;
    if (cv.ad && cv.day === day) used.cave_extra = 1;
    o.ads = { day, used };
  }
  delete af.adDay;
  delete af.adOpen;
  delete af.adBoost;
  delete fm.adDay;
  delete fm.adCount;
  delete cv.ad;
}

// mua (cửa hàng đã báo thành công): Thẻ Phiêu Lưu cộng dồn hạn; Bỏ quảng cáo một lần
export function buyProduct(s: SaveData, id: string, now: number): boolean {
  const e = entOf(s);
  if (id === 'adventure_pass') {
    e.passUntil = Math.max(now, e.passUntil) + PASS.days * 86400000;
    return true;
  }
  if (id === 'no_ads' && !e.noAds) {
    e.noAds = true;
    return true;
  }
  return false;
}
