## ADDED Requirements

### Requirement: Giấy và nét mực
Mọi màn hình SHALL dùng nền giấy kem có vân và lưới kẻ ô xanh nhạt, khung viền nét mực nâu đen (#2b2118) dày khoảng 3 px ở khung tham chiếu 540 × 960. Bóng đổ của khung MUST là bóng cứng lệch xuống phải, không mờ.

#### Scenario: Khung hộp thông tin
- **WHEN** một khung thông tin (bảng tên vùng, thẻ, hộp thoại) hiện lên
- **THEN** khung có nền giấy, viền mực bo góc không đều, bóng cứng lệch xuống phải

### Requirement: Nét mực rung
Khung, nút và icon SHALL có nét rung kiểu hoạt hình vẽ tay: ba bộ dời nét thay nhau khoảng 6 lần mỗi giây. Chữ nhỏ MUST không rung. Người chơi MUST tắt được nét rung trong Sổ tay; khi tắt, nét đứng yên.

#### Scenario: Tắt nét rung
- **WHEN** người chơi tắt "Nét vẽ rung" trong Sổ tay
- **THEN** mọi khung và icon đứng yên ngay, và lựa chọn này được lưu

### Requirement: Nút vẽ tay
Nút SHALL tô màu bút sáp có gạch chéo, viền mực, chữ in hoa (phông Baloo 2). Màu nút theo vai trò:
- đỏ: hành động chính (Đánh!, Xuất trận!);
- xanh lá: xác nhận, nhận;
- cam, tím: phụ;
- giấy: trung tính.

Khi nhấn, nút MUST lún xuống và bóng thu lại. Nút không dùng được MUST xám đi.

#### Scenario: Nhấn nút
- **WHEN** người chơi giữ ngón trên nút "Đánh!"
- **THEN** nút dịch xuống khoảng 3 px, bóng cứng ngắn lại, có tiếng "tách"

### Requirement: Thanh chỉ số gạch sáp
Thanh máu, mana, nộ, EXP và tiến độ SHALL có viền mực và phần đầy tô gạch chéo. Khi giảm, MUST có vệt vàng lùi chậm sau phần đầy. Thanh nộ đầy MUST phát sáng nhấp nháy.

#### Scenario: Mất máu
- **WHEN** tướng mất 30% máu
- **THEN** phần xanh rút ngay về 70%, vệt vàng phía sau rút theo chậm hơn khoảng 0,7 giây

### Requirement: Thẻ bài theo độ hiếm
Thẻ SHALL có dải màu trên theo độ hiếm (Thường xám, Khá xanh lá, Hiếm xanh dương, Sử thi tím, Huyền thoại cam), tên chữ trắng viền mực, icon vẽ tay trong vòng tròn nét đứt, mô tả, dòng độ hiếm, băng keo trên đỉnh. Thẻ Huyền thoại MUST có vệt sáng chạy ngang. Thẻ có giá (chiêu, tuyệt kỹ) MUST có nhãn giá mana hoặc nộ.

#### Scenario: Thẻ Huyền thoại
- **WHEN** thẻ "Thiên Mệnh" hiện trong lượt chọn
- **THEN** thẻ có dải cam và vệt sáng chạy ngang lặp lại

### Requirement: Phông tiếng Việt
Chữ SHALL dùng Baloo 2 (đậm, cho tiêu đề và số) và Pangolin (chữ viết tay, cho mô tả), đủ dấu tiếng Việt. Không ký tự nào được rơi về phông mặc định.

#### Scenario: Tên có dấu chồng
- **WHEN** hiện tên "Thiền Sư Pháp Luân" và "Hắc Dực Vạn Quân"
- **THEN** mọi dấu hiện đúng, không ô vuông, không phông thay thế

### Requirement: Tướng dạng sticker
Tướng trên sân đấu, trong chân dung và danh sách SHALL có viền trắng rồi viền mực bao quanh như hình dán. Tướng chưa có MUST hiện dạng bóng chì sẫm cùng viền.

#### Scenario: Tướng chưa mở
- **WHEN** danh sách tướng hiện một tướng chưa mở
- **THEN** tướng hiện là bóng sẫm có viền sticker, kèm thanh mảnh đã có trên số cần

### Requirement: Chữ tượng thanh và số nổi
Khi trúng đòn, sân đấu SHALL nổ ngôi sao răng cưa có chữ tượng thanh tiếng Việt ("BỐP!", "CHÁT!", "BỤP!", "HỰ!"; đòn mạnh "ẦM!!", "RẦM!!"), kèm số sát thương nảy lên. Chữ hiệu ứng liên tiếp của cùng một tướng MUST xếp thành dòng tin: chữ mới hiện ở chỗ cũ, chữ trước bị đẩy lên một dòng, không chồng lên nhau.

#### Scenario: Năm thẻ chạy liền nhau
- **WHEN** năm thẻ của một lượt chạy liền
- **THEN** tên thẻ và hiệu ứng của chúng xếp thành cột dòng tin đọc được, không đè lên nhau

### Requirement: Âm thanh kiểu đồ chơi
Âm thanh SHALL gồm các tiếng ngắn kiểu đồ chơi:
- nhấn nút, rút và chọn thẻ, thẻ chạy;
- trúng đòn thường và chí mạng, hồi máu, buff, debuff, khiên, né;
- bi chạm đinh, bi rơi vào ô, mở rương, lên cấp;
- thắng, thua, tuyệt kỹ, đổi tướng, đóng dấu.

Người chơi MUST tắt được âm thanh trong Sổ tay.

#### Scenario: Bi chạm đinh liên tục
- **WHEN** 20 bi cùng rơi qua đinh
- **THEN** tiếng "tích" bị giới hạn tối đa khoảng 25 lần mỗi giây, không thành tiếng rè
