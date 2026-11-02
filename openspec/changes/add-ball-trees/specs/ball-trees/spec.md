## ADDED Requirements

### Requirement: Cây bi ra bi đều, đầy thì ngừng
Mỗi cây bi đã mở SHALL ra 5 bi mỗi giờ, kể cả khi tắt game, và MUST ngừng khi đạt sức chứa 50 bi. Giờ máy lùi MUST không cộng và không trừ bi.

#### Scenario: Vắng lâu
- **WHEN** người chơi có 3 cây, hái hết rồi tắt game 30 giờ
- **THEN** lúc vào lại mỗi cây có đúng 50 bi, tổng 150

### Requirement: Cây mở theo tiến độ
Cây 1 SHALL mở khi qua ải 1; cây 2, 3, 4, 5 SHALL mở khi qua boss Đảo Thủy, Hỏa, Kim, Mộc. Cây mới mở MUST bắt đầu từ 0 bi.

#### Scenario: Qua boss Đảo Thủy
- **WHEN** người chơi thắng ải 8 Đảo Thủy
- **THEN** hộp Cây bi có 2 cây đang ra bi, 3 cây ghi điều kiện mở

### Requirement: Hái và hái ×2
"Hái" SHALL lấy phần nguyên số bi của mọi cây và giữ phần lẻ. "Hái ×2" SHALL đi qua chỗ quảng cáo `tree_double` (3 lần mỗi ngày) và nhân đôi số bi hái được; bỏ ngang quảng cáo thì bi vẫn ở trên cây.

#### Scenario: Bỏ ngang quảng cáo
- **WHEN** người chơi bấm "Hái ×2" rồi bấm "Bỏ qua" khi quảng cáo chưa xong
- **THEN** không nhận bi, bi vẫn trên cây, lượt `tree_double` không bị trừ

### Requirement: Thẻ Phiêu Lưu tăng cây bi
Khi còn Thẻ Phiêu Lưu, tốc độ và sức chứa mỗi cây SHALL nhân 1,5 (7,5 bi/giờ, chứa 75). Hết thẻ thì cây giữ số bi đang có và ngừng ra cho tới khi xuống dưới 50.

#### Scenario: Có thẻ
- **WHEN** người chơi có Thẻ Phiêu Lưu và 2 cây, vắng 12 giờ
- **THEN** hái được 150 bi (không thẻ là 100)

### Requirement: AFK không ra bi theo giờ
Đội tự đi ải SHALL chỉ ra mảnh tướng boss và rương AFK; bi thụ động chỉ đến từ cây bi và trang trại.

#### Scenario: Nhận AFK
- **WHEN** người chơi bấm "Nhận mảnh" sau 12 giờ AFK
- **THEN** số bi không đổi; có thể nhận mảnh tướng
