## MODIFIED Requirements

### Requirement: Nút cược ×N
Máy SHALL có nút cược ×1, ×2, ×3, ×5, ×10. Mỗi mức mở khi người chơi đang có ít nhất số bi ghi trong `progression.xSteps` (khởi điểm: ×1, ×2 luôn mở; ×3 từ 150, ×5 từ 300, ×10 từ 700). Cấp người chơi không mở mức cược. Ở ×N:
- mỗi lần thả tốn N bi;
- EXP và bi ở ô nhân N;
- số lượng trong rương nhân N (với thẻ là N lần số thẻ, mỗi thẻ rút riêng).

Không đổi được mức cược khi đợt đang chạy. Nút chưa mở MUST mờ, ghi số bi cần có, chạm vào báo "Cần có n bi để mở ×N". Khi máy rảnh mà bi tụt dưới ngưỡng của mức đang chọn, cược MUST về mức cao nhất còn mở và báo. Khi máy rảnh mà có đủ bi mở thêm mức, máy MUST báo và nhún nút mới. Bi ở mức cược cao MUST có màu khác (×1 hồng, ×2–×3 xanh, ×5 trở lên vàng).

#### Scenario: Ô EXP 15 ở ×3
- **WHEN** một bi cược ×3 rơi vào ô EXP 15
- **THEN** người chơi nhận 45 EXP, chữ "+45 XP" nổi lên

#### Scenario: Thẻ trong rương ở ×5
- **WHEN** rương bạc ở ×5 quay ra kết quả "2 thẻ"
- **THEN** người chơi nhận 10 bản sao thẻ, mỗi bản rút riêng theo bảng độ hiếm, có thể khác nhau

#### Scenario: Chưa đủ bi cho ×3
- **WHEN** người chơi cấp 200 đang có 149 bi và chạm ×3
- **THEN** cược giữ nguyên, máy báo "Cần có 150 bi để mở ×3 (đang có 149)"

#### Scenario: Bi tụt dưới ngưỡng
- **WHEN** người chơi đang cược ×3, đợt xong còn 145 bi
- **THEN** cược về ×2, máy báo "Còn 145 bi, cược về ×2 (×3 cần có 150 bi)"

### Requirement: Mốc Huyền thoại
Máy SHALL hiện thanh "Huyền thoại chắc chắn: x/300" đếm số bi đã tiêu (×N tính N). Lần đầu vượt 300, người chơi MUST nhận tướng Huyền thoại đầu tiên (Đại Sư Cà Sa) với hộp "Huyền thoại!" riêng. Nếu đã có tướng này thì nhận 15 bản sao thẻ Huyền thoại của tướng đó. Sau mốc (và sau hộp "Huyền thoại!"), thanh đổi sang mốc quà. Nếu bảng mốc quà trống thì thanh đổi thành "Đã nhận …. Từ giờ Huyền thoại rất hiếm."

#### Scenario: Vượt mốc giữa đợt
- **WHEN** đợt thả làm số bi đã tiêu đi từ 290 lên 310
- **THEN** thanh đứng đầy tới hết đợt; sau khi đợt xong và mở hết rương, hộp "Huyền thoại!" hiện Đại Sư Cà Sa; rồi thanh hiện mốc quà đầu với 10 bi đã tính

## ADDED Requirements

### Requirement: Mốc quà
Sau mốc Huyền thoại, máy SHALL đếm bi tiêu (×N tính N) vào mốc đang chạy của bảng `pachinko.gifts` (khởi điểm: 30 bi rương gỗ, 40 bi +8 bi, 50 bi rương bạc, 60 bi +120 XP, 80 bi rương vàng). Hết bảng thì vòng lại từ đầu. Lần thả vượt mốc Huyền thoại chỉ tính phần dư.

Khi đủ số bi của mốc đang chạy:
- người chơi MUST nhận quà ngay lúc thả, phần dư chuyển sang mốc kế;
- rương MUST vào khay "Rương chờ" như rương ở ô và không nhân cược;
- bi và EXP MUST cộng ngay.

Thanh mốc MUST ghi "<quà>: x/n bi", kèm ô quà ở đầu thanh hiện quà đang chờ (rương, hoặc icon kèm số). Khi nhận:
- thanh đứng đầy "Nhận quà!", ô quà nhún, loé to;
- quà bay ra: rương vào khay, sao EXP lên thanh kinh nghiệm, bi về dòng đếm;
- sau đó ô quà đổi sang quà kế.

Chạm thanh hoặc ô quà MUST báo ba mốc kế, kèm số bi còn phải thả tính dồn. Mốc quà MUST lưu trong bản lưu (`gift`, `giftTier`).

#### Scenario: Nhận rương mốc
- **WHEN** mốc đang chạy là "Rương Gỗ" 30 bi, đã tính 26, người chơi thả một bi ×5
- **THEN** người chơi nhận một rương gỗ vào khay (×1), mốc kế "+8 bi" đã có 1 bi, ô quà đổi sang icon bi "+8"

#### Scenario: Vòng lại
- **WHEN** người chơi nhận xong mốc cuối của bảng (rương vàng)
- **THEN** mốc kế là mốc đầu bảng (rương gỗ 30 bi)

#### Scenario: Trước mốc Huyền thoại
- **WHEN** người chơi chưa vượt mốc Huyền thoại và thả bi
- **THEN** mốc quà không tăng

### Requirement: Thanh kinh nghiệm nhún cả viền
Khi sao EXP tới thanh kinh nghiệm, cả khung thanh (rãnh vẽ tay cắt từ thân máy, phần đầy, chữ số) SHALL nhún cùng nhau theo dáng nhún thanh của máy tham khảo: 1 → đỉnh → 0,4 đỉnh → đỉnh → 0,7 đỉnh → 1 trong 0,25 giây (ngang 3 %, dọc 18 %, chữ thêm 12 %). Khung MUST không bao giờ nhỏ hơn cỡ gốc, để rãnh vẽ sẵn của thân máy bên dưới luôn bị che.

#### Scenario: Sao tới thanh
- **WHEN** một sao EXP tới đầu phần đầy
- **THEN** viền rãnh và phần đầy cùng phóng to rồi về cỡ gốc trong 0,25 giây, không hở rãnh cũ bên dưới
