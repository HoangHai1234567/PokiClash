## ADDED Requirements

### Requirement: Runtime không sinh nội dung
Code chạy trong game (ngoài `Editor/`, `Tests/` và danh sách ngoại lệ có ghi lý do) MUST NOT tạo GameObject, thêm component, tạo sprite, texture, render texture, material, mesh hay âm thanh. Runtime SHALL chỉ sinh bản sao của prefab có sẵn bằng `Instantiate`, và gán dữ liệu (chữ, ảnh đã nhập, màu, bật/tắt, vị trí) vào tham chiếu kéo thả.

#### Scenario: Test chặn
- **WHEN** chạy EditMode test và một file runtime có `new GameObject(` hoặc `AddComponent`
- **THEN** test báo lỗi, ghi tên file và số dòng

#### Scenario: Ngoại lệ có lý do
- **WHEN** một file nằm trong danh sách ngoại lệ (hình aola bản dev, scene thử cũ `BanThu`)
- **THEN** test bỏ qua file đó, và danh sách ngoại lệ ghi lý do cho từng file

### Requirement: Tài nguyên vẽ bằng code được nướng thành asset
Sprite giấy và mực, texture nhiễu nét rung, material chữ viền, tiếng tổng hợp, hình tướng giữ chỗ và phần tĩnh của máy bi SHALL là asset trong `Assets/03 Art/Baked/`, tạo bằng menu Editor. Hình ảnh và âm thanh MUST giống bản vẽ bằng code trước đó.

#### Scenario: Khởi động không vẽ gì
- **WHEN** game khởi động từ Boot và mở sảnh
- **THEN** không có texture, sprite, material hay `AudioClip` nào được tạo lúc chạy; khung, nút, mây, âm thanh trông và nghe như trước

### Requirement: Giao diện là prefab chỉnh được trong Editor
Mỗi scene chức năng SHALL có một prefab màn hình chứa canvas, gốc scene và toàn bộ nội dung. Mỗi hộp thoại SHALL là prefab variant của tờ giấy gốc. Phần lặp theo dữ liệu SHALL là prefab mục. Nút, khung, chip, thanh, nhãn hệ, sao, băng keo, con dấu, gợi ý, thẻ bài MUST là prefab kit, đặt lồng trong prefab khác.

#### Scenario: Sửa nút một chỗ
- **WHEN** chủ dự án đổi cỡ chữ của prefab `Nut_Vua`
- **THEN** mọi nút cỡ vừa trong mọi màn hình và hộp thoại đổi theo, không cần chạy lại menu nào

#### Scenario: Xem bố cục không cần Play
- **WHEN** mở prefab màn hình Sảnh trong Editor
- **THEN** thấy nền đảo, bảng tên 5 vùng, công trình, hàng nút đáy đúng vị trí như khi chạy

### Requirement: Hành vi giữ nguyên
Sau khi chuyển, luật, số liệu, bản lưu, thứ tự chuyển scene, hộp thoại, âm thanh và hoạt cảnh MUST như trước. Các menu thử `PokiClash/Thử/...` MUST chạy được và cho ảnh chụp tương đương ảnh trước khi chuyển.

#### Scenario: Đi một vòng
- **WHEN** chạy `PokiClash/Thử/Đi một vòng các scene (đang Play)` sau khi chuyển
- **THEN** console không lỗi, 10 ảnh chụp có cùng bố cục với 10 ảnh chụp trước khi chuyển

### Requirement: Công cụ không ghi đè công chỉnh tay
Menu nướng prefab MUST bỏ qua prefab đã có, trừ khi chọn bản ghi đè. Menu `Dựng tất cả` MUST NOT dựng lại scene đã có. `Nhập ảnh ArtGen` SHALL thay ảnh thay thế bằng ảnh gen cùng tên trong mọi prefab.

#### Scenario: Chạy lại Dựng tất cả
- **WHEN** chủ dự án đã kéo lệch một bảng tên trong prefab Sảnh rồi chạy `PokiClash/Cài đặt/2. Dựng tất cả`
- **THEN** bảng tên giữ nguyên vị trí đã chỉnh

#### Scenario: Có ảnh nền đảo mới
- **WHEN** nhập ảnh gen `world` qua `Nhập ảnh ArtGen`
- **THEN** prefab Sảnh dùng ảnh mới thay ảnh thay thế, không phải sửa tay
