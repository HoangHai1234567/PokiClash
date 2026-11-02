## ADDED Requirements

### Requirement: Sảnh là đảo lớn chia 5 vùng hệ
Scene Hub SHALL hiện một đảo lớn phủ kín màn, chia rõ 5 vùng: Hỏa (trên), Mộc (trên-trái), Kim (trên-phải), Thủy (dưới-trái), Thổ (dưới-phải). Làng máy bi nằm ở giữa. Vị trí từng vùng MUST lấy từ dữ liệu đảo (tỉ lệ 0–1 theo ảnh).

#### Scenario: Có ảnh đảo lớn
- **WHEN** có ảnh `world`
- **THEN** sảnh dùng ảnh đó, bảng tên 5 vùng nằm đúng trên vùng núi lửa, rừng, núi thép, đầm nước, vùng đất vàng

#### Scenario: Chưa có ảnh
- **WHEN** chưa có ảnh `world`
- **THEN** sảnh hiện bản đồ nét tay 5 khối vùng tô gạch sáp, có icon cảnh vật, cùng toạ độ vùng

### Requirement: Không khoá vùng
Mọi vùng SHALL vào được ngay từ đầu. Mỗi vùng có bảng tên gồm:
- icon hệ, tên đảo;
- nhãn độ khó so với cấp người chơi: "Dễ", "Vừa sức", "Khó", "Quá mạnh!", "Đã chinh phục";
- dòng "Cấp a–b · n/8 ải";
- thanh tiến độ màu theo hệ.

#### Scenario: Người chơi mới
- **WHEN** người chơi cấp 1 mở sảnh lần đầu
- **THEN** Đảo Thủy ghi "Vừa sức", bốn đảo còn lại ghi "Quá mạnh!", nhưng chạm vào vẫn vào được

### Requirement: Đảo gợi ý
Sảnh SHALL có mũi tên nhún chỉ vào đảo nên đánh: đảo chưa chinh phục đầu tiên theo thứ tự Thủy → Hỏa → Kim → Mộc → Thổ mà cấp người chơi ≥ cận dưới cấp đề nghị − 3. Không đảo nào thoả thì chỉ đảo chưa chinh phục đầu tiên. Nút "Đánh tiếp" ở hàng dưới MUST đưa thẳng tới đảo gợi ý.

#### Scenario: Xong Đảo Thủy
- **WHEN** người chơi cấp 4 vừa chinh phục Đảo Thủy
- **THEN** mũi tên chỉ Đảo Hỏa (cận dưới 6 − 3 = 3 ≤ 4)

### Requirement: Chạm vùng sang đảo hệ
Chạm vùng hoặc bảng tên vùng SHALL chuyển sang scene đảo của hệ đó bằng màn mây.

#### Scenario: Chạm Đảo Kim
- **WHEN** người chơi chạm vùng núi thép
- **THEN** game chuyển sang scene Đảo Kim, thanh quay lại ghi "Đảo Kim"

### Requirement: Làng máy bi và hàng nút chính
Giữa đảo SHALL có bảng "Làng Máy Bi" ghi số bi đang có; chạm vào mở scene Máy bi. Đáy sảnh SHALL có hàng nút tròn vẽ tay: Tướng (kèm số việc chờ), Sổ thẻ, Máy Bi (to nhất, kèm số bi), Đánh tiếp, Sổ tay. Mỗi nút MUST mở scene của nó bằng màn mây.

#### Scenario: Có bi chưa thả
- **WHEN** người chơi có 18 bi
- **THEN** nút Máy Bi có chấm ghi 18

### Requirement: Chỗ đặt công trình side meta
Sảnh SHALL có chỗ cho công trình side meta ở rìa làng (Trang trại, Đền Huy Hiệu, Hang Tiềm Năng). Mỗi công trình hiện khi tính năng mở; trước đó hiện dạng phác chì kèm điều kiện mở.

#### Scenario: Chưa mở Trang trại
- **WHEN** người chơi chưa đủ điều kiện mở Trang trại
- **THEN** công trình Trang trại hiện nét chì mờ; chạm vào báo điều kiện mở

### Requirement: Màn giới thiệu lần đầu
Lần đầu vào sảnh, game SHALL hiện hộp "Sổ Tay Phiêu Lưu" có 4 ô:
1. Năm đảo, năm hệ (bắt đầu ở Đảo Thủy với Tiểu Y);
2. Đánh bằng thẻ;
3. Thắng thì nhận bi (có AFK, boss rơi mảnh);
4. Thả bi vào máy.

Có nút "Bắt đầu!". Hộp MUST chỉ hiện một lần.

#### Scenario: Mở lại game
- **WHEN** người chơi đã bấm "Bắt đầu!" rồi mở lại game
- **THEN** không hiện lại màn giới thiệu
