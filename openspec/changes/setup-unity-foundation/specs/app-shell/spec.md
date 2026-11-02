## ADDED Requirements

### Requirement: Scene Boot và scene chức năng
Game SHALL khởi động từ scene Boot, nơi giữ các dịch vụ dùng chung (lưu, âm thanh, chuyển scene, hộp thoại, thông báo) suốt phiên chơi. Mỗi chức năng (Hub, Zone, Battle, Machine, Heroes, Cards, Notebook và các scene side meta sau này) MUST là một scene Unity riêng, nạp cộng và gỡ khi rời đi.

#### Scenario: Mở game lần đầu
- **WHEN** người chơi mở game lần đầu
- **THEN** Boot nạp dữ liệu lưu (hoặc tạo mới), rồi mở scene Hub

#### Scenario: Chỉ một scene chức năng tại một thời điểm
- **WHEN** người chơi đi từ Hub sang Machine
- **THEN** scene Hub được gỡ, scene Machine được nạp, dịch vụ ở Boot vẫn giữ nguyên trạng thái

### Requirement: Chuyển scene bằng màn mây
Mỗi lần chuyển scene, game SHALL đóng màn mây vẽ tay (hai khối mây từ hai bên khép vào giữa), đổi scene khi mây đã che kín, rồi mở mây. Trong lúc chuyển MUST chặn mọi thao tác chạm.

#### Scenario: Chuyển scene thường
- **WHEN** người chơi chạm vào vùng Đảo Thủy trên sảnh
- **THEN** mây khép trong khoảng 0,38 giây, scene Zone của Đảo Thủy được nạp sau lớp mây, rồi mây tách ra trong khoảng 0,38 giây

#### Scenario: Yêu cầu chuyển chồng lên nhau
- **WHEN** một yêu cầu chuyển scene đến khi đang chuyển dở
- **THEN** yêu cầu mới được xếp hàng và chạy sau khi lần chuyển hiện tại xong; chỉ giữ yêu cầu mới nhất

### Requirement: Thanh trên của sảnh
Scene Hub SHALL hiện thanh trên gồm:
- vòng cấp người chơi có cung EXP;
- số bi đang có;
- nút AFK hiện số bi đang chờ nhận;
- nút Sổ tay.

#### Scenario: Cập nhật sau khi thả bi
- **WHEN** người chơi quay về sảnh sau khi được EXP và tiêu bi ở máy bi
- **THEN** vòng cấp, cung EXP và số bi hiện đúng giá trị đã lưu

#### Scenario: AFK có bi chờ nhận
- **WHEN** số bi AFK chờ nhận từ 5 trở lên
- **THEN** nút AFK nhún nhịp nhàng để gây chú ý

### Requirement: Thanh quay lại ở scene con
Scene con (Zone, Machine, Heroes, Cards, Notebook và các scene side meta) SHALL hiện thanh trên gồm nút quay lại, tên scene, cấp và số bi. Nút quay lại MUST đưa về đích do scene khai báo (mặc định là Hub). Scene Battle MUST dùng thanh riêng của trận.

#### Scenario: Quay lại từ đảo hệ
- **WHEN** người chơi đang ở scene Đảo Hỏa và bấm nút quay lại
- **THEN** game chuyển về Hub bằng màn mây

#### Scenario: Không có thanh tab
- **WHEN** người chơi ở bất kỳ scene nào
- **THEN** không có thanh tab chuyển trang; mọi lối đi giữa các chức năng là nút trên đảo, hàng nút ở sảnh hoặc nút quay lại

### Requirement: Hộp thoại và thông báo
Game SHALL có hộp thoại dạng tờ giấy dán băng keo, trượt vào hơi nghiêng, có nút đóng và nền tối mờ. Game cũng SHALL có thông báo ngắn hiện ở phía trên rồi tự tắt sau khoảng 2,7 giây. Hộp thoại kết quả quan trọng (kết quả trận, chọn tướng thay khi tướng gục) MUST không đóng được bằng cách chạm ra ngoài.

#### Scenario: Chạm ra ngoài hộp thoại thường
- **WHEN** người chơi chạm vào nền tối quanh hộp thoại xem chi tiết tướng
- **THEN** hộp thoại đóng

#### Scenario: Hộp thoại bắt buộc
- **WHEN** hộp chọn tướng thay đang mở và người chơi chạm ra ngoài
- **THEN** hộp thoại vẫn mở cho tới khi người chơi chọn tướng

### Requirement: Khung dọc co giãn
Giao diện SHALL dựng theo khung tham chiếu 1080 × 1920 (khớp theo chiều rộng). Phần trên và dưới MUST tôn trọng vùng an toàn (tai thỏ, thanh điều hướng). Màn dài hơn 9:16 thì phần dôi ra dồn cho nền scene. Máy tính bảng 3:4 thì nội dung giữ cỡ, hai bên để nền.

#### Scenario: Máy 9:19,5 có tai thỏ
- **WHEN** game chạy trên máy 1080 × 2340 có tai thỏ
- **THEN** thanh trên nằm dưới tai thỏ, hàng nút dưới nằm trên thanh điều hướng, ảnh nền phủ kín màn
