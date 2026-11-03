## ADDED Requirements

### Requirement: Tích luỹ AFK
Khi người chơi đã qua ít nhất một ải, game SHALL tích luỹ bi AFK theo thời gian thực (kể cả khi tắt game), tốc độ `4 + 0,8 × tổng số ải đã qua` bi mỗi giờ (giá trị khởi điểm). Giờ AFK MUST dừng tích luỹ ở 12 giờ cho tới khi người chơi nhận.

#### Scenario: Đầy 12 giờ
- **WHEN** người chơi đã qua 10 ải và vắng 20 giờ
- **THEN** hộp AFK ghi "12 / 12 giờ" và 144 bi chờ nhận (12 giờ × 12 bi/giờ)

#### Scenario: Chưa qua ải nào
- **WHEN** người chơi mới mở hộp AFK
- **THEN** hộp ghi "Qua ải 1 để mở. Đội sẽ tự đánh các ải đã qua và nhặt bi, cả khi bạn tắt game."

### Requirement: Mảnh tướng từ AFK
Mỗi giờ AFK tròn SHALL có 8% cơ hội ra 1 mảnh của một tướng rơi ở ải đội đang AFK, bốc theo tỉ lệ rơi của ải đó (không tính tướng tặng). Mảnh của tướng đã có MUST đổi thành bản sao thẻ như mọi nguồn khác.

AFK theo ải (Unity, người dùng chọn 2026-11-03; bản web vẫn lấy mọi boss đã thắng): ải đảo đã thắng có nút "AFK ải này". Chưa chọn thì đội AFK ở ải xa nhất đã qua có rơi mảnh. Đổi ải thì mảnh của các giờ tròn đã dồn tính theo ải cũ và nhận luôn, phần giờ lẻ giữ lại.

#### Scenario: Chọn ải AFK
- **WHEN** người chơi đã qua ải 30 đảo Thủy, mở ải 29 (Ma Kết, Mi Nhi) và bấm "AFK ải này"
- **THEN** nút đổi thành "Đang AFK", nhãn AFK trên đảo dời xuống ải 29, mảnh AFK từ đó chỉ là Ma Kết hoặc Mi Nhi

#### Scenario: Nhận sau 12 giờ
- **WHEN** người chơi nhận AFK sau 12 giờ, đội đang AFK ải boss Đảo Thủy
- **THEN** có 12 lần thử 8%, mỗi lần trúng ra 1 mảnh Y Trạch (hoặc 1 bản sao thẻ nếu đã có Y Trạch)

### Requirement: Rương AFK
Cứ mỗi 3 giờ AFK hiệu dụng, game SHALL thêm một rương AFK vào khay (tối đa 4 rương). Rương đầu khay tự đếm giờ mở 2 tiếng; mở xong thì rương kế bắt đầu. Rương AFK MUST ra bi, EXP, hoặc bản sao thẻ với độ hiếm thấp hơn rương máy bi (Thường 60, Khá 30, Hiếm 9,5, Sử thi 0,5).

#### Scenario: Khay đầy
- **WHEN** khay đã có 4 rương AFK
- **THEN** không sinh thêm rương; hộp AFK ghi "Khay đầy, mở bớt rương"

#### Scenario: Rương mở xong
- **WHEN** rương đầu khay đếm hết 2 tiếng
- **THEN** rương có nhãn "Mở được", chạm vào thì mở và hiện thưởng

### Requirement: Hộp AFK
Nút đồng hồ ở sảnh SHALL hiện số bi AFK đang chờ (hoặc số phút nếu chưa đủ 1 bi), và nhún khi có từ 5 bi trở lên. Chạm vào mở hộp AFK gồm:
- câu "Đội tự đánh n ải đã qua: x bi mỗi giờ, giữ tối đa 12 giờ";
- thanh giờ; số bi chờ nhận;
- khay rương AFK kèm giờ mở;
- nút "Nhận", "Nhận ×2" (quảng cáo), "Mở ngay" trên rương đang đếm (quảng cáo), "Tăng tốc ×2" (quảng cáo).

Nhận xong MUST đặt lại đồng hồ AFK và hiện thông báo thưởng.

#### Scenario: Nhận ×2
- **WHEN** người chơi bấm "Nhận ×2" khi có 40 bi chờ và xem xong quảng cáo
- **THEN** người chơi nhận 80 bi, đồng hồ AFK về 0

#### Scenario: Bỏ quảng cáo giữa chừng
- **WHEN** người chơi đóng quảng cáo trước khi xong
- **THEN** không nhân đôi; bi vẫn chờ nhận như cũ

### Requirement: Tăng tốc ×2
Nút "Tăng tốc ×2" SHALL làm AFK tích luỹ gấp đôi (cả bi lẫn tiến độ rương) trong 2 giờ thực kể từ lúc bật, tối đa 3 lần mỗi ngày (giá trị khởi điểm). Khi đang tăng tốc, hộp AFK MUST ghi giờ còn lại của tăng tốc.

#### Scenario: Tăng tốc rồi tắt game
- **WHEN** người chơi bật tăng tốc rồi tắt game 5 giờ
- **THEN** 2 giờ đầu tính ×2, 3 giờ sau tính ×1, tổng tương đương 7 giờ AFK

### Requirement: Chống chỉnh giờ máy
Game SHALL bỏ qua mọi đoạn thời gian âm (giờ máy bị lùi). Mỗi lần tính MUST chỉ cộng tối đa tới giới hạn 12 giờ.

#### Scenario: Lùi giờ máy
- **WHEN** người chơi chỉnh giờ máy lùi 5 giờ rồi mở game
- **THEN** AFK không bị trừ, không cộng thêm; đồng hồ tiếp tục từ thời điểm hiện tại
