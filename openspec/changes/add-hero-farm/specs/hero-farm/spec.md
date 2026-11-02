## ADDED Requirements

### Requirement: Mở trang trại
Trang trại SHALL mở khi người chơi có từ 3 tướng. Trước đó, công trình Trang trại trên sảnh MUST hiện nét chì mờ; chạm vào báo "Có 3 tướng để mở Trang trại".

#### Scenario: Gia Bỉ gia nhập
- **WHEN** người chơi thắng ải 6 Đảo Thủy và có tướng thứ 3
- **THEN** công trình Trang trại trên sảnh tô màu, có chấm báo mới

### Requirement: Chỗ làm và hệ hợp
Trang trại SHALL có 8 chỗ làm:

| Chỗ | Số lượng | Hệ hợp |
|---|---|---|
| Ruộng rau | 2 | Thổ |
| Ao vịt | 2 | Thủy |
| Vườn cây | 2 | Mộc |
| Lò bánh | 1 | Hỏa |
| Xưởng nông cụ | 1 | Kim |

Lúc mở dùng được 3 chỗ; các chỗ còn lại mở ở cấp người chơi 8, 11, 14, 17, 20. Mỗi chỗ MUST ghi loại, hệ hợp, điều kiện mở nếu còn khoá.

#### Scenario: Chỗ khoá
- **WHEN** người chơi cấp 9 mở trang trại
- **THEN** 4 chỗ dùng được, chỗ thứ 5 ghi "Mở ở cấp 11"

### Requirement: Năng suất và thời lượng theo sức tướng
Tướng đặt vào một chỗ SHALL làm ra bi theo năng suất:

`1,2 × sức độ hiếm × (1 + 0,05·(cấp − 1)) × (1 + 0,1·(sao − 1))` bi/giờ, nhân 1,25 nếu hệ của tướng hợp chỗ đó.

Thời lượng làm MUST bằng `2 + 0,5·(sao − 1) + 0,5·chỉ số độ hiếm` giờ (Thường 0 … Huyền thoại 4). Hết thời lượng thì tướng ngồi nghỉ tại chỗ và ngừng làm ra bi. Mọi số là giá trị khởi điểm, chỉnh được.

#### Scenario: Đúng hệ hợp
- **WHEN** Tiểu Y (Thủy, Thường, 1 sao) làm ở Ao vịt khi người chơi cấp 5
- **THEN** Tiểu Y làm ra 1,8 bi mỗi giờ trong 2 giờ, rồi ngồi nghỉ

### Requirement: Đổi ca và nghỉ ngơi
Người chơi SHALL rút tướng khỏi chỗ bất kỳ lúc nào. Tướng bị rút MUST nghỉ `clamp(thời lượng × 15, 15, 60)` phút trước khi vào chỗ nào khác. Tướng đang nghỉ hiện xám kèm giờ còn lại trong danh sách chọn. Sức làm ở trang trại MUST tách khỏi trận: tướng đang làm hoặc đang nghỉ vẫn vào đội và ra trận bình thường.

#### Scenario: Đổi ca
- **WHEN** Võ Sư hết sức ở Ruộng rau và người chơi đưa Gia Bỉ vào thay
- **THEN** Gia Bỉ bắt đầu ca mới; Võ Sư nghỉ 30 phút rồi mới vào chỗ khác được

#### Scenario: Ra trận khi đang làm
- **WHEN** Y Trạch đang làm ở Ao vịt và người chơi đưa Y Trạch vào đội đánh ải
- **THEN** Y Trạch ra trận với đủ máu, ca làm ở Ao vịt không bị ảnh hưởng

### Requirement: Thu hoạch
Bi làm ra SHALL tích ở từng chỗ (tối đa bằng 12 giờ sản lượng của chỗ đó) và tính cả khi tắt game. Nút "Thu hoạch" MUST lấy hết bi tích (phần lẻ giữ lại cho lần sau), bay bi về chỉ số bi, và hiện tổng.

#### Scenario: Thu hoạch sau khi ngủ dậy
- **WHEN** người chơi vắng 8 tiếng, 5 tướng đều đã hết sức sau 2–4 giờ
- **THEN** mỗi chỗ có số bi bằng năng suất × thời lượng đã làm; "Thu hoạch" cộng tất cả

### Requirement: Tự xếp
Nút "Tự xếp" SHALL đưa vào mỗi chỗ trống tướng rảnh (không đang làm, không đang nghỉ) có năng suất ở chỗ đó cao nhất, ưu tiên đúng hệ hợp.

#### Scenario: Thiếu tướng rảnh
- **WHEN** có 3 chỗ trống nhưng chỉ 1 tướng rảnh
- **THEN** tướng đó vào chỗ hợp nhất với nó, 2 chỗ còn trống

### Requirement: Scene Trang trại
Scene Trang trại SHALL hiện ảnh đảo trang trại với 8 chỗ theo toạ độ dữ liệu. Mỗi chỗ có:
- icon loại chỗ;
- sticker tướng đang làm (nhún nhịp khi làm, ngồi khi nghỉ);
- vòng sức còn lại;
- bong bóng số bi tích.

Chạm một chỗ MUST mở danh sách chọn tướng: năng suất và thời lượng ở chỗ đó, dấu hệ hợp, tướng nghỉ xám có giờ. Có nút "Rút ra" nếu chỗ đang có tướng.

#### Scenario: Chọn tướng cho Lò bánh
- **WHEN** người chơi chạm Lò bánh (hệ hợp Hỏa)
- **THEN** danh sách xếp tướng theo năng suất ở Lò bánh, Võ Tăng Bồ Đề có dấu "Hợp hệ ×1,25"
