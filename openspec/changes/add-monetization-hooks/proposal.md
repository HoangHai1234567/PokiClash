## Why

GDD gốc nhắc kiếm tiền ở đúng một chỗ: phần AFK "có thể kích mở rương, kích x2 tốc độ,… bằng reward hoặc kích mua iap", và "có thể khai thác reward ở đây".

Các tính năng khác (Hang Tiềm Năng, Trang trại) cũng có chỗ hợp với quảng cáo thưởng. Change này làm lớp móc chung: mọi chỗ gọi quảng cáo hay IAP đi qua một giao diện, thay SDK mà không sửa tính năng. Bản thử dùng quảng cáo giả lập như bản web.

## What Changes

- **Giao diện chung:**
  - `IRewardAds.Show(placement)` trả về xem xong hay bỏ ngang;
  - `IStore.Buy(product)` trả về mua thành công hay không.

  Bản dev dùng quảng cáo giả lập (hộp đếm ngược 3 giây) và cửa hàng giả lập.
- **Danh sách chỗ đặt quảng cáo thưởng,** mỗi chỗ có giới hạn mỗi ngày:

  | Chỗ | Tác dụng | Giới hạn mỗi ngày |
  |---|---|---|
  | `afk_double` | Nhận AFK ×2 | không giới hạn, mỗi lần nhận một lần |
  | `afk_chest_open` | Mở ngay rương AFK | 4 |
  | `afk_boost` | AFK ×2 trong 2 giờ | 3 |
  | `farm_boost` | Năng suất trang trại ×2 trong 1 giờ | 3 |
  | `cave_extra` | +1 lượt Hang Tiềm Năng | 1 |

- **Gói IAP khởi điểm** (chỉ khung, giá để sau):
  - "Thẻ Phiêu Lưu 30 ngày": AFK ×1,5, thêm 1 ô rương AFK, rương AFK mở nhanh gấp đôi;
  - "Bỏ quảng cáo": mọi chỗ quảng cáo thưởng nhận thưởng ngay, không xem.

  **Không bán bi, không bán đá tiềm năng, không bán lượt quay máy bi.** Tránh rủi ro pháp lý kiểu casino xã hội. Đây là đề xuất, chủ dự án quyết.
- **Cửa hàng** đặt ở Sổ tay (mục "Gói hỗ trợ"); không thêm công trình trên sảnh ở bản này.

## Capabilities

### New Capabilities

- `monetization-hooks`: giao diện quảng cáo thưởng và IAP, danh sách chỗ đặt và giới hạn mỗi ngày, quảng cáo và cửa hàng giả lập cho bản dev, hai gói IAP khởi điểm, nguyên tắc không bán tài nguyên vào máy bi.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code:** `App/Monetization` (`IRewardAds`, `IStore`, bản giả lập, bộ đếm theo ngày); các tính năng gọi qua tên chỗ đặt.
- **Lưu:** đếm lượt quảng cáo theo ngày; quyền lợi gói đã mua (hạn Thẻ Phiêu Lưu, cờ Bỏ quảng cáo).
- **SDK thật** (AdMob, Unity Ads, IAP của Unity): chưa chọn; thêm bằng change riêng khi chọn.
- **Phụ thuộc:** `setup-unity-foundation`. Được gọi từ `add-afk-rewards`, `add-hero-farm`, `add-potential-stones`.
