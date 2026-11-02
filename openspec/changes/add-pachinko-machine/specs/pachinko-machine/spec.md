## ADDED Requirements

### Requirement: Mặt máy
Máy bi SHALL có khung 460 × 680 (đơn vị máy), gồm:
- 10 hàng đinh so le;
- 3 nấm bật (hệ số nảy cao);
- u lồi trên hai tường ở các hàng lẻ;
- hai vai nghiêng trên cùng;
- 3 cốc hứng: rương vàng ở giữa (nhỏ nhất), rương bạc hai bên;
- 9 ô đáy, độ rộng 22, 50, 66, 30, 96, 30, 66, 50, 22, thưởng theo thứ tự: rương gỗ, EXP 15, EXP 5, +1 bi, EXP 10, +1 bi, EXP 5, EXP 15, rương gỗ.

Khe giữa tường và đinh mép MUST rộng hơn đường kính bi, để bi không kẹt.

#### Scenario: Không bi nào kẹt
- **WHEN** thả 6.000 bi với máng đung đưa đều
- **THEN** mọi bi đều rơi vào một ô hoặc một cốc

### Requirement: Vật lý có hạt giống
Vật lý SHALL chạy bước thời gian cố định 1/120 giây chia 4 bước con:
- trọng lực;
- va đinh có hệ số nảy (nấm 0,75, đinh 0,5) và lệch ngẫu nhiên nhỏ;
- va tường và vách ô;
- bi va bi.

Mọi phần ngẫu nhiên MUST lấy từ bộ số có hạt giống. Bi lăn quá 14 giây MUST bị đẩy xuống.

#### Scenario: Tỉ lệ khớp bản web
- **WHEN** chạy mô phỏng 6.000 bi cùng cách thả trên Unity và bản web
- **THEN** tỉ lệ từng ô và cốc lệch nhau dưới 1 điểm phần trăm

### Requirement: Thả bi
Máng thả hình đám mây SHALL đung đưa trái phải phía trên máy. Người chơi:
- chạm máy hoặc nút "Thả bi" để thả 1 bi;
- giữ để thả liên tục, mỗi 0,16 giây;
- bấm "Thả liền 20" để thả tự động tới giới hạn.

Mỗi đợt thả tối đa 20 bi, từ cấp 15 là 30 bi. Đợt mới bắt đầu khi mọi bi của đợt trước đã rơi. Thiếu bi MUST báo "Cần N bi cho mỗi lần thả ×N".

#### Scenario: Chạm giới hạn đợt
- **WHEN** người chơi cấp 5 đang giữ nút thả và đã thả 20 bi
- **THEN** máy ngừng thả, báo "Tối đa 20 bi một đợt, chờ bi rơi hết"

### Requirement: Nút cược ×N
Máy SHALL có nút cược ×1, ×2, ×3, ×5, ×10, mở lần lượt ở cấp 1, 3, 5, 8, 12. Ở ×N:
- mỗi lần thả tốn N bi;
- EXP và bi ở ô nhân N;
- số lượng trong rương nhân N (với thẻ là N lần số thẻ, mỗi thẻ rút riêng).

Không đổi được mức cược khi đợt đang chạy. Bi ở mức cược cao MUST có màu khác (×1 hồng, ×2–×3 xanh, ×5 trở lên vàng).

#### Scenario: Ô EXP 15 ở ×3
- **WHEN** một bi cược ×3 rơi vào ô EXP 15
- **THEN** người chơi nhận 45 EXP, chữ "+45 XP" nổi lên

#### Scenario: Thẻ trong rương ở ×5
- **WHEN** rương bạc ở ×5 quay ra kết quả "2 thẻ"
- **THEN** người chơi nhận 10 bản sao thẻ, mỗi bản rút riêng theo bảng độ hiếm, có thể khác nhau

### Requirement: Rương
Rương rơi vào SHALL bay vào khay "Rương chờ" (đếm theo loại) và mở sau khi đợt thả xong, lần lượt, mỗi rương một hộp (rương lắc, bật mở, thưởng hiện ra, nút "Mở tiếp (n)" hoặc "Nhận"). Khay cũng MUST chạm để mở được.

Bảng rương ở ×1:

| Rương | Bi | EXP | Thẻ | Mảnh tướng |
|---|---|---|---|---|
| Gỗ | 55%: 2–3 | 35%: 15–30 | 10%: 1 thẻ (Thường 70, Khá 30) | — |
| Bạc | 30%: 3–6 | 30%: 40–70 | 35%: 2 thẻ (Thường 45, Khá 35, Hiếm 18, Sử thi 2) | 5%: 1–2 |
| Vàng | 20%: 8–12 | 20%: 100–160 | 50%: 3 thẻ (Khá 45, Hiếm 40, Sử thi 14,99, Huyền thoại 0,01) | 10%: 2–4 |

Mảnh tướng lấy từ tướng boss đã gặp. Chưa gặp boss nào thì từ mọi tướng không phải Huyền thoại.

#### Scenario: Ba rương trong một đợt
- **WHEN** một đợt 20 bi có 2 rương gỗ và 1 rương vàng
- **THEN** sau khi bi cuối rơi, hộp mở rương vàng hiện trước, rồi tới 2 rương gỗ, bấm "Mở tiếp (2)"

### Requirement: Mốc Huyền thoại
Máy SHALL hiện thanh "Huyền thoại chắc chắn: x/300" đếm số bi đã tiêu (×N tính N). Lần đầu vượt 300, người chơi MUST nhận tướng Huyền thoại đầu tiên (Đại Sư Cà Sa) với hộp "Huyền thoại!" riêng. Nếu đã có tướng này thì nhận 15 bản sao thẻ Huyền thoại của tướng đó. Sau mốc, thanh đổi thành "Đã nhận …. Từ giờ Huyền thoại rất hiếm."

#### Scenario: Vượt mốc giữa đợt
- **WHEN** đợt thả làm số bi đã tiêu đi từ 290 lên 310
- **THEN** sau khi đợt xong và mở hết rương, hộp "Huyền thoại!" hiện Đại Sư Cà Sa, kèm "Thả đủ 300 bi: chắc chắn nhận tướng Huyền thoại đầu tiên"

### Requirement: Bảng tỉ lệ công khai
Nút "Tỉ lệ" SHALL mở bảng ghi:
- tỉ lệ từng loại ô và cốc theo số đo mô phỏng (rương vàng ≈3%, bạc ≈6%, gỗ ≈8,5%, EXP 15 ≈23%, EXP 10 ≈22%, EXP 5 ≈30%, +1 bi ≈8%);
- bảng rương;
- tỉ lệ thẻ Huyền thoại;
- mốc 300 bi;
- câu "×N nhân mọi thưởng, kể cả số thẻ trong rương".

Số trong bảng MUST cập nhật mỗi khi mặt máy đổi (chạy lại mô phỏng).

#### Scenario: Xem tỉ lệ
- **WHEN** người chơi bấm "Tỉ lệ"
- **THEN** bảng hiện đủ các mục trên, ghi chú "Đo bằng mô phỏng 6.000 bi"

### Requirement: Phản hồi hình và tiếng
Máy SHALL phản hồi từng va chạm và từng thưởng:
- đinh loé vàng khi bị chạm mạnh;
- tiếng tích có giới hạn tần suất;
- ô sáng khi bi rơi vào;
- chữ nổi ("+10 XP" tím, "+1 bi" hồng, "Rương Vàng!");
- rương bay từ chỗ rơi vào khay.

Tiếng và hiệu ứng ô hiếm (rương) MUST nổi bật hơn hẳn ô thường. Lên cấp báo bằng hộp "Lên cấp!" sau khi mở hết rương, không chồng hộp.

#### Scenario: Lên cấp do rương
- **WHEN** EXP từ ô và rương trong một đợt đủ lên cấp
- **THEN** hộp rương hiện trước; mở xong rương cuối thì hộp "Lên cấp!" mới hiện

### Requirement: Rời máy khi bi đang rơi
Khi người chơi rời scene máy trong lúc còn bi đang lăn, mỗi bi đó SHALL được tính như rơi vào ô giữa (EXP 10 × mức cược). Rương đang chờ MUST giữ lại trong khay cho lần sau.

#### Scenario: Thoát giữa chừng
- **WHEN** người chơi bấm quay lại khi còn 5 bi ×1 đang lăn và 1 rương trong khay
- **THEN** người chơi nhận 50 EXP; lần sau vào máy, rương vẫn ở khay
