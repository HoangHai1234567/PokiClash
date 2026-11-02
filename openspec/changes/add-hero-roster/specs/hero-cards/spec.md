## ADDED Requirements

### Requirement: Ba thẻ riêng mỗi tướng
Mỗi tướng SHALL có 3 thẻ riêng, mỗi thẻ có độ hiếm riêng:
- **Chiêu:** tốn mana, dùng tối đa một lần mỗi lượt.
- **Tuyệt kỹ:** cần 100 nộ và một lượng mana, thay cú đánh thường cuối lượt.
- **Bị động:** tự kích theo điều kiện.

Thẻ riêng mở cùng tướng ở cấp 1. Bộ 33 thẻ khởi điểm ghi ở `GD_Claude/11_BanWeb_TheBai.md` (bảng sinh từ `Web/src/core/data/cards.ts`).

#### Scenario: Mở Lam Quân
- **WHEN** Lam Quân vừa mở
- **THEN** Chuông Đồng, Hồng Chung, Vỏ Thép đều ở cấp 1 và dùng được ngay trong trận

### Requirement: Lên cấp thẻ bằng bản sao
Thẻ riêng SHALL lên cấp 2, 3, 4, 5 khi có đủ 2, 4, 8, 15 bản sao (tiêu bản sao khi nâng). Mỗi cấp tăng các con số của thẻ thêm 15% so với cấp 1 (sát thương, buff, hồi máu, khiên, mana, nộ, tỉ lệ kích). Thời hạn và giá không đổi; thẻ tự mất máu thì giảm phần mất máu. Mô tả thẻ MUST tự sinh theo cấp, nên luôn khớp số thật.

#### Scenario: Nâng Thiết Quyền lên cấp 2
- **WHEN** Thiết Quyền cấp 1 (gây 120% Công) có 2 bản sao và người chơi bấm "Lên cấp 2"
- **THEN** thẻ lên cấp 2, mô tả đổi thành "Gây 138% Công sát thương. +12 nộ.", bản sao còn 0

#### Scenario: Cấp tối đa
- **WHEN** thẻ đã ở cấp 5
- **THEN** thẻ ghi "Cấp tối đa"; bản sao nhận thêm vẫn được giữ

### Requirement: Nguồn bản sao thẻ
Bản sao thẻ riêng SHALL đến từ:
- rương máy bi (theo bảng độ hiếm của từng loại rương);
- rương mốc của đảo;
- mảnh của tướng đã có;
- rương AFK (hiếm hơn).

Bản sao chỉ ra cho thẻ của tướng đã có. Nếu không có thẻ nào đúng độ hiếm vừa quay, game MUST lùi xuống độ hiếm thấp hơn; không có thẻ nào thì đổi thành EXP.

#### Scenario: Quay ra Sử thi khi chưa có thẻ Sử thi
- **WHEN** rương bạc quay ra một thẻ Sử thi mà người chơi chỉ có tướng Thường
- **THEN** người chơi nhận bản sao một thẻ Hiếm, nếu không có thì Khá, rồi Thường

### Requirement: Thẻ chung mở theo cấp
Bộ 23 thẻ chung SHALL mở dần theo cấp người chơi (cấp mở ghi trong dữ liệu: phần lớn mở ở cấp 1; Đấm Kép cấp 2; Hút Máu, Đốt Lửa cấp 3; Gương Đôi, Mắt Ưng cấp 5; Bùa Choáng, Hoà Khí, Áo Choàng Ma cấp 7; Nghịch Thiên, Thiên Mệnh cấp 10). Thẻ chung MUST không lên cấp.

#### Scenario: Lên cấp 7
- **WHEN** người chơi lên cấp 7
- **THEN** hộp lên cấp ghi "Thẻ mới vào bộ rút: Bùa Choáng, Hoà Khí, Áo Choàng Ma", và từ lượt sau các thẻ này có thể được rút

### Requirement: Scene Sổ thẻ
Scene Sổ thẻ SHALL hiện:
- khung "Cách xếp thẻ": 5 lần chọn 1 trong 3; thẻ chạy theo thứ tự; Chiêu và Tuyệt kỹ không tốn lần chọn; "lượt này" và "tới lượt sau" nghĩa là gì;
- chú giải độ hiếm kèm trọng số rút;
- lưới 23 thẻ chung, thẻ chưa mở xám kèm "Mở ở cấp n".

#### Scenario: Thẻ chưa mở
- **WHEN** người chơi cấp 3 mở Sổ thẻ
- **THEN** Gương Đôi hiện xám có ổ khoá và "Mở ở cấp 5"
