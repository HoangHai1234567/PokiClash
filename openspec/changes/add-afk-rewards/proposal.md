## Why

GDD gốc có hai câu về AFK:
- "Khi chinh phục được 1 ải người chơi có thể afk cho đánh afk để nhận ball hoặc mảnh tướng (tỉ lệ thấp thôi, có thể khai thác reward ở đây)."
- "Việc afk cày ải cũng có thể kiếm được thẻ nhưng độ hiếm ra sẽ khó hơn rất nhiều. (phần này có thể kích mở rương, kích x2 tốc độ,… bằng reward hoặc kích mua iap)."

Bản web mới có AFK ra bi, mảnh tướng theo giờ và nút ×2 giả lập quảng cáo. Còn thiếu ba thứ GDD nói: thẻ từ AFK, rương phải mở, tăng tốc ×2.

## What Changes

- **AFK ra bi** khi đã qua ít nhất một ải:
  - `4 + 0,8 × tổng số ải đã qua` bi mỗi giờ;
  - giữ tối đa 12 giờ, tính cả khi tắt game.
- **Mảnh tướng:** mỗi giờ AFK có 8% cơ hội ra 1 mảnh tướng boss đã gặp.
- **Rương AFK (mới):**
  - cứ 3 giờ AFK ra 1 rương, khay giữ tối đa 4;
  - rương có giờ mở 2 tiếng, mở từng cái;
  - bên trong: bi, EXP, bản sao thẻ hiếm hơn rương máy bi (Thường 60, Khá 30, Hiếm 9,5, Sử thi 0,5).
- **Hộp AFK** (nút đồng hồ ở sảnh):
  - thanh giờ, bi chờ nhận, khay rương AFK kèm giờ mở;
  - các nút "Nhận", "Nhận ×2", "Mở ngay", "Tăng tốc ×2".
  - Quảng cáo và IAP đi qua lớp `add-monetization-hooks`.
- **Tăng tốc ×2:** AFK chạy gấp đôi trong 2 giờ.
- **Chống chỉnh giờ máy:** thời gian lùi thì bỏ qua; một lần nhận không vượt giới hạn 12 giờ.

## Capabilities

### New Capabilities

- `afk-rewards`: tích luỹ AFK (bi, mảnh), giới hạn giờ, rương AFK có giờ mở, tăng tốc ×2, hộp AFK, chống chỉnh giờ.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code:** `Core/Progression/Afk` (chép `afkRate`, `afkPending`, `claimAfk`; thêm rương AFK và tăng tốc); `Game/World/AfkPanel`.
- **Lưu:** thêm `afkChests` (loại, lúc bắt đầu mở), `afkBoostUntil`, `afkLastTick`.
- **Dữ liệu:** `BalanceConfig` thêm mục AFK (tốc độ, giới hạn, 3 giờ/rương, 4 ô, giờ mở 2 tiếng, bảng rương AFK, tăng tốc ×2 trong 2 giờ).
- **Phụ thuộc:** `add-world-islands` (số ải đã qua, boss đã gặp), `add-hero-roster` (bản sao thẻ, mảnh). Nút quảng cáo và IAP dùng `add-monetization-hooks`; trước khi có thì dùng quảng cáo giả lập 3 giây như bản web.
