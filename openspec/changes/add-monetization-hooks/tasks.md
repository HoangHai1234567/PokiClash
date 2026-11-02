## 1. Lớp móc

- [x] 1.1 `IRewardAds`, `IStore` và cổng `Ads` / `Store` (`App/Ads.cs`); `AdGate` (`Core/AdGate.cs`, chép `Web/src/core/ads.ts`): giới hạn theo chỗ đặt mỗi ngày, ngày theo giờ máy, qua ngày thì đếm lại, giờ máy lùi về ngày trước không mở lại lượt; `Entitlements` (hạn Thẻ Phiêu Lưu, cờ Bỏ quảng cáo). Xem xong mới trừ lượt và trao thưởng; bỏ ngang thì không trừ. Đã mua Bỏ quảng cáo thì trao ngay, vẫn trừ lượt
- [x] 1.2 Quảng cáo giả lập (hộp đếm 3 giây, nút "Bỏ qua") và cửa hàng giả lập (mua thành công ngay, không trừ tiền) ở `App/Dev/FakeMonetization.cs`, chỉ có trong Editor và bản Development. Bản phát hành chưa gắn SDK: nút quảng cáo và mục "Gói hỗ trợ" ẩn (đã thử bằng cách bỏ hai bản giả lập lúc Play; menu "Biên dịch thử bản phát hành" đạt)
- [x] 1.3 Lưu `ads` (ngày, số lượt đã dùng theo chỗ) và `ent`. Bản lưu lên v3 (web và Unity): bước v2 → v3 dồn bộ đếm cũ của AFK (`adOpen`, `adBoost`), trang trại (`adCount`) và Hang (`ad`) về `ads`, chỉ giữ số của ngày mới nhất; file `save_v2.json` được đọc, chuyển lên v3, giữ bản cũ thành `.bak`

## 2. Nối tính năng

- [x] 2.1 AFK: `afk_double` (không giới hạn), `afk_chest_open` (4), `afk_boost` (3). Thẻ Phiêu Lưu: bi AFK ×1,5, khay rương 5 ô, rương mở trong 1 giờ; hộp AFK ghi "(×1,5 Thẻ Phiêu Lưu)" và vẽ 5 ô
- [x] 2.2 Trang trại: `farm_boost` (3); Hang Tiềm Năng: `cave_extra` (1, mỗi lần +1 lượt thắng). Nút ghi số lượt còn; hết lượt thì xám "Hết lượt hôm nay" và bỏ hình TV
- [x] 2.3 Mục "Gói hỗ trợ" trong Sổ tay (bản phát hành cũng có khi đã gắn cửa hàng): 2 gói, trạng thái ("Còn n ngày", "Đã mua", "Chưa có"), nút "Mua" / "Gia hạn" (Thẻ Phiêu Lưu cộng dồn hạn), dòng "Không bán bi, đá tiềm năng hay lượt quay máy bi.". Sổ tay bản dev thêm "Đặt lại lượt QC", "Bỏ gói đã mua"

## 3. Kiểm tra

- [x] 3.1 EditMode (`AdsTests`, 7 test): golden `ads.json` (giới hạn, qua ngày, lùi ngày, chỗ không giới hạn) khớp web; giới hạn từng chỗ theo spec; Bỏ quảng cáo vẫn theo giới hạn ngày; Thẻ Phiêu Lưu (mua, gia hạn, AFK ×1,5, 5 ô, mở 1 giờ, hết hạn về số gốc) khớp web; lưu và đọc lại quyền lợi; bước v2 → v3 khớp web. `SaveTests`: file v2 chuyển lên v3. AFK, Hang, trang trại đọc lượt từ `AdGate`, golden cũ vẫn khớp. "Bỏ quảng cáo trả thưởng ngay" cần App nên thử ở Play (3.3)
- [x] 3.2 Rà danh sách gói: chỉ có `adventure_pass`, `no_ads`; mua gói nào cũng không đổi bi, đá tiềm năng, rương máy bi, rương AFK; tên và mô tả không nhắc bi, đá, lượt quay
- [x] 3.3 Play (`PokiClash/Thử/Gói hỗ trợ: …`): chưa có SDK thì mọi nút quảng cáo và mục gói ẩn; mua Thẻ Phiêu Lưu còn 30 ngày, AFK 12 giờ ra 187 bi (gốc 124), khay 5 ô; hết 3/3 lượt tăng tốc thì nút xám "Hết lượt hôm nay"; mua Bỏ quảng cáo thì "Nhận ×2" trao ngay (+62 bi = 31 × 2, không mở hộp quảng cáo); Hang hết lượt thắng, "+1 lượt" ra 1 lượt rồi nút ẩn. Các lượt AFK, trang trại, tiềm năng cũ chạy lại đúng; console không lỗi
- [ ] 3.4 Gắn SDK thật (quảng cáo, IAP) và giá gói: change riêng khi chủ dự án chọn
