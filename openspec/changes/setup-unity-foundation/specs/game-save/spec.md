## ADDED Requirements

### Requirement: Lưu cục bộ có phiên bản
Game SHALL lưu toàn bộ tiến trình của người chơi vào một file JSON trong bộ nhớ của máy, có số phiên bản. Tiến trình gồm:
- cấp, EXP, bi, số bi đã thả, mốc Huyền thoại;
- tướng (có hay chưa, mảnh, sao, thẻ riêng và bản sao), đội hình;
- tiến độ từng đảo và rương mốc;
- AFK, cài đặt, thống kê;
- dữ liệu side meta khi có.

Ghi file MUST qua file tạm rồi mới đổi tên, để mất điện giữa chừng không làm hỏng bản lưu.

#### Scenario: Mở lại game
- **WHEN** người chơi tắt game rồi mở lại
- **THEN** cấp, bi, tướng, tiến độ đảo, đội hình giữ nguyên như lúc tắt

#### Scenario: Tắt ngang lúc đang ghi
- **WHEN** game bị tắt đúng lúc đang ghi bản lưu
- **THEN** lần mở sau đọc được bản lưu đầy đủ gần nhất

### Requirement: Ghi sau mỗi thay đổi quan trọng
Game SHALL ghi bản lưu ngay sau mỗi thay đổi tiến trình:
- thắng hoặc thua trận;
- mỗi bi rơi vào ô, mở rương;
- nâng thẻ, tiến hóa, nhận AFK;
- đổi đội hình, đổi cài đặt.

#### Scenario: Thoát giữa đợt thả bi
- **WHEN** người chơi thoát game khi 10 bi đã rơi vào ô và 5 bi còn đang lăn
- **THEN** thưởng của 10 bi đã rơi được giữ; 5 bi đang lăn được tính vào ô giữa (EXP 10) khi rời scene

### Requirement: Bản lưu cũ hoặc hỏng
Khi bản lưu có phiên bản cũ hơn, game SHALL chạy bước di chuyển dữ liệu nếu có. Không có bước di chuyển, hoặc file hỏng, thì game MUST báo cho người chơi rồi mới tạo bản lưu mới. Bản cũ MUST được giữ lại thành file dự phòng.

#### Scenario: Đổi cấu trúc đảo
- **WHEN** bản lưu phiên bản 1 (20 ải theo chương) gặp game phiên bản 2 (5 đảo × 8 ải)
- **THEN** game báo "Dữ liệu bản thử cũ không dùng được, sẽ bắt đầu lại", giữ file cũ thành `save_v1.bak`, rồi tạo bản lưu mới

### Requirement: Cài đặt
Game SHALL lưu các cài đặt: nét vẽ rung (bật/tắt), âm thanh (bật/tắt), bong bóng gợi ý trong trận (bật/tắt), tốc độ trận mặc định (×1, ×2, ×3). Cài đặt MUST có hiệu lực ngay khi đổi.

#### Scenario: Đổi tốc độ trận
- **WHEN** người chơi chọn ×2 trong trận
- **THEN** các trận sau mở ở ×2

### Requirement: Xoá dữ liệu
Sổ tay SHALL có nút xoá dữ liệu, kèm hộp xác nhận. Xoá xong, game MUST về trạng thái người chơi mới: cấp 1, 10 bi, chỉ có Tiểu Y, mọi đảo 0/8.

#### Scenario: Xác nhận xoá
- **WHEN** người chơi bấm "Xoá dữ liệu" rồi bấm "Xoá" trong hộp xác nhận
- **THEN** bản lưu được làm mới và game về sảnh, hiện màn giới thiệu
