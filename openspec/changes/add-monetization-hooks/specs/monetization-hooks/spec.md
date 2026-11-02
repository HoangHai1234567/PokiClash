## ADDED Requirements

### Requirement: Quảng cáo thưởng qua tên chỗ đặt
Mọi quảng cáo thưởng SHALL gọi qua một giao diện chung với tên chỗ đặt (`afk_double`, `afk_chest_open`, `afk_boost`, `farm_boost`, `cave_extra`), trả về "xem xong" hoặc "bỏ ngang". Thưởng MUST chỉ trao khi xem xong.

#### Scenario: Bỏ ngang
- **WHEN** người chơi đóng quảng cáo `afk_boost` trước khi xong
- **THEN** không bật tăng tốc, không trừ lượt trong ngày

### Requirement: Giới hạn mỗi ngày
Mỗi chỗ đặt SHALL có giới hạn lượt mỗi ngày (giá trị khởi điểm):

| Chỗ | Giới hạn |
|---|---|
| `afk_double` | không giới hạn, mỗi lần nhận AFK một lần |
| `afk_chest_open` | 4 |
| `afk_boost` | 3 |
| `farm_boost` | 3 |
| `cave_extra` | 1 |

Hết lượt thì nút quảng cáo xám, ghi "Hết lượt hôm nay". Ngày đặt lại lúc 0 giờ theo giờ máy; giờ máy lùi MUST không mở lại lượt.

#### Scenario: Qua ngày mới
- **WHEN** người chơi đã dùng 3/3 lượt `afk_boost` rồi mở game sau 0 giờ hôm sau
- **THEN** nút "Tăng tốc ×2" dùng được lại, đếm 0/3

### Requirement: Quảng cáo và cửa hàng giả lập
Bản dev SHALL có quảng cáo giả lập (hộp "Quảng cáo giả lập" đếm ngược 3 giây, có nút bỏ) và cửa hàng giả lập (mua thành công ngay, không trừ tiền). Bản phát hành MUST dùng SDK thật hoặc ẩn các nút nếu chưa có SDK.

#### Scenario: Bản dev
- **WHEN** người chơi bấm "Nhận ×2" ở bản dev
- **THEN** hộp quảng cáo giả lập đếm 3, 2, 1 rồi trao thưởng ×2

### Requirement: Gói IAP khởi điểm
Mục "Gói hỗ trợ" trong Sổ tay SHALL có hai gói:
- **Thẻ Phiêu Lưu 30 ngày:** AFK ×1,5; khay rương AFK 5 ô; giờ mở rương AFK 1 tiếng.
- **Bỏ quảng cáo:** mọi chỗ quảng cáo thưởng trao thưởng ngay, không cần xem; vẫn theo giới hạn mỗi ngày.

Quyền lợi MUST lưu và áp ngay sau khi mua, còn hiệu lực sau khi mở lại game.

#### Scenario: Mua Thẻ Phiêu Lưu
- **WHEN** người chơi mua Thẻ Phiêu Lưu ở bản dev
- **THEN** hộp AFK ghi tốc độ ×1,5, khay rương AFK có 5 ô, và hạn còn 30 ngày

### Requirement: Không bán tài nguyên vào máy bi
Game SHALL không bán bi, đá tiềm năng hay lượt quay máy bi bằng tiền thật hoặc qua quảng cáo trực tiếp. Mọi thay đổi nguyên tắc này MUST đi qua một change riêng được chủ dự án duyệt.

#### Scenario: Rà soát cửa hàng
- **WHEN** kiểm tra danh sách sản phẩm IAP
- **THEN** không có sản phẩm nào cho bi, đá tiềm năng hay lượt quay
