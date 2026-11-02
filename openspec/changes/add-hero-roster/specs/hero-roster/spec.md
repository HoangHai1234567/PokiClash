## ADDED Requirements

### Requirement: Danh sách tướng
Game SHALL có 11 tướng khởi điểm. Mỗi tướng có hệ Ngũ hành, độ hiếm, 6 chỉ số gốc và 3 thẻ riêng:

| Tướng | Hệ | Độ hiếm |
|---|---|---|
| Võ Sư | Thổ | Thường |
| Võ Tăng Bồ Đề | Hỏa | Hiếm |
| Thiền Sư Pháp Luân | Hỏa | Sử thi |
| Đại Sư Cà Sa | Thổ | Huyền thoại |
| Gia Bỉ | Mộc | Thường |
| Sứ Giả Gia Bỉ | Mộc | Hiếm |
| Lam Quân | Kim | Thường |
| Vạn Quân | Kim | Hiếm |
| Hắc Dực Vạn Quân | Kim | Sử thi |
| Tiểu Y | Thủy | Thường |
| Y Trạch | Thủy | Hiếm |

Thêm tướng MUST chỉ cần thêm dữ liệu, không sửa code.

#### Scenario: Thêm tướng mới
- **WHEN** người làm thêm một bản ghi tướng vào dữ liệu kèm 3 thẻ riêng
- **THEN** tướng đó hiện trong scene Tướng, rơi mảnh được, vào trận được

### Requirement: Chỉ số tướng
Chỉ số SHALL tính từ:
- sức theo độ hiếm (Thường 1; Khá 1,1; Hiếm 1,22; Sử thi 1,36; Huyền thoại 1,5);
- dáng chỉ số lấy từ 6 chỉ số gốc (căn bậc hai, so với trung bình của chính tướng đó);
- cấp: +10% mỗi cấp;
- sao: +8% mỗi sao;
- phần cộng từ side meta (huy hiệu, đá tiềm năng).

Máu, Công, Thủ gốc lần lượt là 600, 180, 55. Tốc bằng tốc gốc cộng cấp. Mọi số là giá trị khởi điểm, chỉnh được.

#### Scenario: Tướng hiếm mạnh hơn
- **WHEN** so Lam Quân (Thường) và Vạn Quân (Hiếm) cùng cấp 10, cùng 1 sao
- **THEN** máu, Công, Thủ của Vạn Quân cao hơn khoảng 22% tính theo sức độ hiếm, rồi lệch thêm theo dáng chỉ số

### Requirement: Cấp người chơi là cấp tướng
Người chơi SHALL có một cấp duy nhất (1–30), dùng làm cấp của mọi tướng, cả tướng vừa mở. EXP lên cấp kế tiếp bằng `round(40 × cấp^1,35)`. EXP thừa được giữ sang cấp sau. Lên cấp MUST hiện hộp "Lên cấp!", ghi:
- mọi tướng mạnh thêm;
- nút cược máy bi vừa mở (nếu có);
- thẻ chung vừa vào bộ rút (nếu có).

#### Scenario: Lên hai cấp một lúc
- **WHEN** một rương vàng cho đủ EXP để vượt 2 cấp
- **THEN** cấp tăng 2, EXP thừa giữ lại, hộp lên cấp ghi cấp mới và mọi thứ vừa mở ở cả 2 cấp

### Requirement: Mảnh và mở tướng
Tướng chưa có SHALL mở bằng mảnh: Thường 10, Hiếm 20, Sử thi 30, Huyền thoại 50. Đủ mảnh thì tướng mở ngay, có 3 thẻ ở cấp 1 và 1 sao. Mảnh của tướng đã có MUST đổi thành bản sao thẻ riêng của tướng đó (mỗi mảnh 1 bản sao, thẻ chọn ngẫu nhiên).

#### Scenario: Đủ mảnh Vạn Quân
- **WHEN** người chơi có 17/20 mảnh Vạn Quân và nhận thêm 5 mảnh từ boss Đảo Kim
- **THEN** Vạn Quân mở, hộp thưởng ghi "Mở khóa Vạn Quân!"

#### Scenario: Mảnh của tướng đã có
- **WHEN** người chơi đã có Y Trạch và nhận 4 mảnh Y Trạch
- **THEN** 4 mảnh thành 4 bản sao thẻ của Y Trạch; hộp thưởng ghi "Đã có tướng: đổi thành 4 bản sao thẻ"

### Requirement: Tướng khởi đầu và tướng tặng
Người chơi mới SHALL chỉ có Tiểu Y (Thủy), trong đội. Qua lần đầu ải 3 Đảo Thủy MUST tặng Võ Sư; qua lần đầu ải 6 Đảo Thủy MUST tặng Gia Bỉ. Cả hai mở thẳng, không cần mảnh.

#### Scenario: Qua ải 6 Đảo Thủy
- **WHEN** người chơi thắng ải 6 Đảo Thủy lần đầu
- **THEN** Gia Bỉ gia nhập, có thể đưa vào đội ngay

### Requirement: Đội hình
Người chơi SHALL chọn đội tối đa 3 tướng đã có, có thứ tự; tướng đầu ra sân trước. Đội được lưu và dùng làm mặc định cho trận sau. Đội trống MUST không vào trận được.

#### Scenario: Đội đã đủ 3
- **WHEN** đội đã có 3 tướng và người chơi chọn thêm tướng thứ 4
- **THEN** báo "Đội tối đa 3 tướng", đội không đổi

### Requirement: Tiến hóa sao
Tướng SHALL lên sao 2, 3, 4, 5 khi:
- tổng cấp 3 thẻ riêng đạt 5, 8, 11, 15;
- cấp người chơi đạt 2, 5, 9, 14.

Mỗi sao +8% mọi chỉ số. Đủ điều kiện thì nút "Tiến hóa" nhấp nháy; người chơi bấm mới lên sao, kèm hoạt cảnh và tiếng.

#### Scenario: Chưa đủ cấp người chơi
- **WHEN** Tiểu Y có tổng cấp thẻ 8 nhưng người chơi mới cấp 4
- **THEN** mục tiến hóa ghi "Tổng cấp 3 thẻ 8/8 · Cấp người chơi 4/5", nút Tiến hóa xám

### Requirement: Scene Tướng
Scene Tướng SHALL hiện lưới 3 cột thẻ tướng: tướng đã có xếp trước. Mỗi thẻ tướng có:
- dải màu theo hệ, sticker tướng, tên, nhãn hệ, độ hiếm;
- hàng sao (nếu đã có) hoặc thanh mảnh (nếu chưa có);
- nhãn "TRONG ĐỘI";
- chấm đỏ khi có thẻ nâng được hoặc tiến hóa được.

Nút Tướng ở sảnh MUST hiện tổng số việc đang chờ.

#### Scenario: Có thẻ nâng được
- **WHEN** Võ Sư có đủ bản sao để nâng Thiết Quyền
- **THEN** thẻ tướng Võ Sư có chấm đỏ, nút Tướng ở sảnh có số việc chờ

### Requirement: Hộp chi tiết tướng
Chạm thẻ tướng SHALL mở hộp chi tiết gồm:
- ô xem tướng chạy được 4 clip: Đứng, Đánh, Chiêu, Trúng;
- tên, danh hiệu, hệ, độ hiếm, sao, dòng tướng;
- Máu, Công, Thủ, Tốc ở cấp và sao hiện tại;
- 3 thẻ riêng ở cấp hiện tại, mỗi thẻ có thanh bản sao và nút "Lên cấp n" khi đủ;
- mục tiến hóa;
- nút "Cho vào đội" / "Bỏ khỏi đội".

Với tướng chưa có, hộp MUST ghi số mảnh còn thiếu và nơi rơi mảnh (đảo và ải, AFK, rương máy bi; Đại Sư Cà Sa thêm mốc 300 bi).

#### Scenario: Xem tướng chưa có
- **WHEN** người chơi mở chi tiết Hắc Dực Vạn Quân khi chưa có
- **THEN** hộp hiện bóng sẫm, "Chưa có: cần 30 mảnh", thanh mảnh, và "Mảnh rơi ở Đảo Kim ải 7, ải 8; ải boss đã qua còn rơi khi AFK"
