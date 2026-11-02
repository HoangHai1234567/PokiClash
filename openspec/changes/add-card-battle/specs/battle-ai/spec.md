## ADDED Requirements

### Requirement: Máy chọn thẻ theo tình huống
Máy SHALL chọn trong 3 thẻ thẻ có điểm cao nhất theo tình huống của tướng đang ra sân:
- máu thấp thì quý thẻ hồi máu, khiên, giảm sát thương;
- sắp đầy nộ hoặc đã bật Tuyệt kỹ thì quý thẻ tăng Công;
- thiếu mana cho Chiêu thì quý thẻ mana;
- máu thấp thì tránh thẻ tự mất máu;
- tính sát thương có nhân khắc hệ.

Điểm MUST nhân thêm một hệ số ngẫu nhiên `1 ± nhiễu`.

#### Scenario: Máu thấp
- **WHEN** tướng của máy còn 20% máu và được rút "Liều Mạng", "Bình Thuốc", "Mài Vuốt"
- **THEN** máy gần như luôn chọn "Bình Thuốc"

### Requirement: Độ khéo theo ải
Mức nhiễu của địch SHALL là `max(0,12; 0,6 − 0,05 × số thứ tự ải)`, nên các ải đầu địch chọn thẻ kém hơn. Nút "Tự chơi" của người chơi MUST dùng mức nhiễu 0,12.

#### Scenario: Ải đầu tiên
- **WHEN** đánh ải 1 Đảo Thủy
- **THEN** địch chọn với mức nhiễu khoảng 0,55, thường chọn chưa tối ưu

### Requirement: Máy dùng Chiêu và Tuyệt kỹ
Trước mỗi lần chọn, máy SHALL:
- bật Tuyệt kỹ ngay khi đủ;
- bật Chiêu khi đã có thẻ tăng Công trong hàng (hoặc buff Công đang có), hoặc khi chỉ còn 2 lần chọn trở xuống.

Nếu nộ còn thiếu 15 trở xuống là đầy, máy MUST giữ lại đủ mana cho Tuyệt kỹ thay vì bật Chiêu.

#### Scenario: Để dành mana
- **WHEN** tướng của máy có 90 nộ, 50 mana; Chiêu tốn 30, Tuyệt kỹ tốn 40
- **THEN** máy không bật Chiêu ở lượt này

### Requirement: Máy đổi tướng
Đầu lượt, máy SHALL cân nhắc đổi tướng khi:
- tướng đang ra sân dưới 25% máu và có dự bị trên 50% máu; hoặc
- tướng đang ra sân bị khắc hệ, và có dự bị không bị khắc, không khắc ngược, trên 60% máu.

Khi đủ điều kiện, máy MUST đổi với xác suất 55%, để người chơi không đoán trước được.

#### Scenario: Bị khắc
- **WHEN** Tiểu Y (Thủy) của máy đối mặt Võ Sư (Thổ) và máy có Lam Quân (Kim) đầy máu
- **THEN** khoảng một nửa số lần, máy đổi Lam Quân ra sân đầu lượt

### Requirement: Tự chơi cho người chơi
Màn trận SHALL có nút "Tự chơi". Khi bật, máy chọn thay người chơi với cùng logic, kể cả khi bật giữa lúc đang chọn (máy chọn nốt phần còn lại) và khi phải chọn tướng thay. Tắt nút MUST trả quyền chọn cho người chơi từ lần chọn kế tiếp.

#### Scenario: Bật giữa lượt
- **WHEN** người chơi đã chọn 2 thẻ rồi bật "Tự chơi"
- **THEN** máy chọn 3 thẻ còn lại (có thể bật Chiêu, Tuyệt kỹ) rồi ra đòn
