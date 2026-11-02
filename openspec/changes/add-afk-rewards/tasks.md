## 1. Logic AFK (C# thuần)

- [x] 1.1 Chép `afkRate`, `afkPending`, `afkBossPool`, `claimAfk` — viết ở web trước (`Web/src/core/afk.ts`), chép sang `Core/Afk.cs`
- [x] 1.2 Đồng hồ theo đoạn: `afk.lastTick`, giờ hiệu dụng, đoạn tăng tốc ×2, chặn 12 giờ, bỏ đoạn âm (lùi giờ máy: không trừ, không cộng, tính tiếp từ bây giờ)
- [x] 1.3 Rương AFK: sinh mỗi 3 giờ hiệu dụng, khay 4, đếm 2 tiếng từng cái, bảng rương AFK, mở ngay. Cách làm cụ thể:
  - bộ đếm rương riêng, không về 0 khi nhận bi (nhận thường xuyên vẫn ra rương); dừng khi giờ AFK đầy, như bi;
  - khay đầy thì bộ đếm giữ ở 3 giờ, mở bớt một rương là rương mới vào khay ngay;
  - rương kế bắt đầu đếm khi rương trước đếm xong (không chờ người chơi mở), nên vắng lâu vẫn có nhiều rương mở được;
  - mở rương dùng chung hàm quay bảng rương với máy bi (`RollChest`).
- [x] 1.4 Đếm lượt quảng cáo theo ngày (mở ngay 4, tăng tốc 3), đặt lại lúc 0 giờ theo giờ máy. "Nhận ×2" không giới hạn.
- [x] 1.5 EditMode test: golden 42 bước khớp web từng giá trị (12 giờ đầy, tăng tốc rồi tắt game, lùi giờ, khay đầy, mở ngay, lượt quảng cáo, tua, mảnh theo hạt giống); thêm 3 tình huống của spec

## 2. Giao diện

- [x] 2.1 Nút đồng hồ ở thanh trên sảnh: "+n" bi (hoặc số phút khi chưa đủ 1 bi), nhún khi ≥ 5 bi, chấm đỏ khi có rương mở được; tự làm mới mỗi 20 giây
- [x] 2.2 Hộp AFK (`App/AfkPanel.cs`): câu tốc độ, thanh giờ, bi chờ, khay 4 ô (giờ mở đếm ngược, "Mở được", "Chờ"), Nhận / Nhận ×2 / Mở ngay / Tăng tốc ×2 kèm số lượt còn (xám khi hết lượt; tăng tốc xám khi giờ AFK đã đầy)
- [x] 2.3 Hộp mở rương AFK dùng chung hộp rương của máy bi (`App/ChestBox.cs`)

## 3. Nối quảng cáo

- [x] 3.1 `IRewardAds.Show(placement, done)` (`App/Ads.cs`) cho `afk_double`, `afk_chest_open`, `afk_boost`; bản thử dùng quảng cáo giả lập 3 giây có nút "Bỏ qua" (bỏ thì không nhận thưởng)

## 4. Kiểm tra

- [x] 4.1 Play (`PokiClash/Thử/AFK: tua giờ, nhận, rương, tăng tốc`): tua 1/8/14 giờ, nhận thường (+12) và ×2 (+192), bỏ quảng cáo giữa chừng (+0, bi vẫn chờ), khay đầy 4 rương, mở 4 rương, mở ngay, tăng tốc; chụp màn hình; console không lỗi. Bảng thử ở Sổ tay có "Tua AFK 1 giờ" và "Tua AFK 8 giờ".
