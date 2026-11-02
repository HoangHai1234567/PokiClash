## ADDED Requirements

### Requirement: Máy tự chơi hàng loạt
Cửa sổ Editor "PokiClash/Cân bằng" SHALL chạy N trận máy tự chơi (cả hai bên do máy chọn) cho một ải, một đảo, hoặc cả 40 ải, với đội, cấp, sao, cấp thẻ và phần cộng side meta chọn được. Kết quả MUST là bảng tỉ lệ thắng và số hiệp trung bình theo ải và theo cấp, xuất được ra CSV.

#### Scenario: Chạy cả đảo Thủy
- **WHEN** người làm chọn Đảo Thủy, đội Tiểu Y + Võ Sư + Gia Bỉ, cấp 1/4/7/9, 50 trận mỗi ô
- **THEN** cửa sổ hiện bảng 8 ải × 4 cấp, mỗi ô ghi "%thắng số hiệp", như `npm run sim -- battle` của bản web

### Requirement: Mô phỏng máy bi
Công cụ SHALL thả 6.000 bi với máng đung đưa đều theo mặt máy hiện tại, ra:
- tỉ lệ từng ô và cốc;
- giá trị trung bình mỗi rương;
- EXP, bi hoàn, thẻ và đá mỗi bi ở ×1.

Số này MUST là nguồn của bảng tỉ lệ hiện trong game.

#### Scenario: Đổi độ rộng ô
- **WHEN** người làm đổi độ rộng ô +1 bi rồi chạy mô phỏng
- **THEN** công cụ ra tỉ lệ mới và cảnh báo nếu bi hoàn mỗi bi vượt 0,5

### Requirement: Mô phỏng tiến độ
Công cụ SHALL mô phỏng 30 ngày chơi theo 3 kiểu người chơi (chăm, vừa, ít). Mỗi kiểu có số lần vào game, số trận, có xem quảng cáo hay không. Kết quả MUST là cấp người chơi theo ngày, ngày chinh phục từng đảo, và so với cấp đề nghị của đảo.

#### Scenario: Đảo Thổ quá xa
- **WHEN** mô phỏng cho thấy kiểu "vừa" tới ngày 30 vẫn dưới cấp 21
- **THEN** báo cáo đánh dấu Đảo Thổ "ngoài tầm 30 ngày" để chỉnh đường cong EXP hoặc thưởng

### Requirement: Bảng thử trong bản dev
Sổ tay bản dev SHALL có mục "Bảng thử" với các nút:
- +50 bi, +500 XP;
- tua AFK 1 giờ, 8 giờ; tua giờ trang trại;
- mở hết tướng, mở hết ải;
- +5 bản sao mọi thẻ, +10 đá tiềm năng;
- xoá dữ liệu.

Bản phát hành MUST không có mục này.

#### Scenario: Tua AFK
- **WHEN** người thử bấm "Tua AFK 8 giờ" rồi mở hộp AFK
- **THEN** hộp AFK ghi thêm 8 giờ, và rương AFK sinh theo đúng luật

### Requirement: Chỉnh số lúc chơi
Sổ tay bản dev SHALL có mục "Chỉnh số" cho các hệ số chính:
- số lần chọn, mana mỗi lượt, mana dự bị, nộ khi đánh và khi bị đánh;
- chí mạng gốc và hệ số, hằng số Thủ;
- Máu, Công, Thủ gốc; tăng mỗi cấp, mỗi sao, mỗi cấp thẻ;
- máu và Công boss.

Sửa xong có hiệu lực ở trận sau. Nút "Về số gốc" MUST trả lại số trong asset.

#### Scenario: Tăng mana mỗi lượt
- **WHEN** người thử đổi "Mana mỗi lượt" từ 20 thành 30 rồi vào trận
- **THEN** đầu mỗi lượt tướng nhận 30 mana

### Requirement: Ghi trận
Mỗi trận kết thúc SHALL ghi một dòng vào `PokiClash/Logs/tran.csv`:
- thời điểm, đảo, ải, đội;
- kết quả, số hiệp, giây thật, máu còn (%);
- tự chơi hay tay.

File MUST nằm ngoài Assets và không vào bản phát hành.

#### Scenario: Người thử chơi tay
- **WHEN** người thử thắng ải 5 Đảo Thủy bằng tay trong 95 giây, 4 hiệp
- **THEN** CSV có dòng mới với tự chơi = 0, giây = 95, hiệp = 4

### Requirement: Kiểm tra trùng khớp với bản web
Bộ test SHALL chạy golden: chuỗi số ngẫu nhiên, mô tả thẻ, 200 trận, mô phỏng máy bi, chỉ số tướng, thưởng ải. So với file đối chiếu xuất từ bản web; lệch MUST làm test đỏ và chỉ ra sự kiện đầu tiên lệch.

#### Scenario: Sửa luật ở một bên
- **WHEN** người làm sửa công thức sát thương trong Unity mà quên sửa bản web
- **THEN** golden test đỏ, báo trận và sự kiện đầu tiên có sát thương khác
