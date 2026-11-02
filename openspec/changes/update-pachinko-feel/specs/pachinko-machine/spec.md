## MODIFIED Requirements

### Requirement: Mặt máy
Máy bi SHALL có khung 460 × 680 (đơn vị máy), gồm:
- 10 hàng đinh so le;
- 3 nấm bật;
- u lồi trên hai tường ở các hàng lẻ;
- hai vai nghiêng trên cùng;
- trần ở ray máng thả;
- hai cốc bạc tròn hai bên;
- một két vàng giữa máy, phía dưới. Két có mái chữ ^ chừa khe hẹp ở đỉnh (giá trị khởi điểm 25,5, chỉnh được), một đinh gác ngay trên khe, đáy chữ V có hai cọc ở hai đầu. Hông két để hở. Đinh nằm trong khung két bị bỏ.
- 11 ô đáy theo thứ tự: rương gỗ, EXP 15, EXP 5, +1 bi, EXP 10, rương vàng, EXP 10, +1 bi, EXP 5, EXP 15, rương gỗ. Độ rộng khởi điểm (chỉnh được, nguồn `Web/src/core/pachinko.ts`): 25,25; 38; 46; 29,75; 59,25; 35,5; 59,25; 29,75; 46; 38; 25,25.

Ô rương vàng ở giữa MUST nằm trọn dưới đáy két, để bi chỉ vào được khi chui ngang qua khe giữa đáy két và đầu vách ô. Mọi ô MUST rộng ít nhất 22 (bi đường kính 18). Khe giữa tường và đinh mép MUST rộng hơn đường kính bi, để bi không kẹt.

#### Scenario: Không bi nào kẹt
- **WHEN** thả 6.000 bi với máng đung đưa đều
- **THEN** mọi bi đều rơi vào một ô, một cốc hoặc két

#### Scenario: Ô vàng khuất dưới két
- **WHEN** dựng mặt máy mặc định
- **THEN** ô giữa là rương vàng, nằm trong khoảng hai đầu đáy két, và bàn có đúng một két, hai cốc bạc, 11 ô

### Requirement: Vật lý có hạt giống
Vật lý SHALL chạy bước thời gian cố định 1/120 giây chia 4 bước con. Vật liệu chép máy bi tham khảo (`GD_Claude/07_MayBi.md`, mục "Vật lý chép"):
- mọi va chạm nảy 0,8 (đinh, nấm, cọc, tường, trần, vai, vách ô, mái và đáy két);
- tường, trần, vai, vách ô, nấm và cọc có ma sát 0,22; đinh, mái và đáy két trơn;
- va chậm (tốc pháp tuyến dưới 111) thì không nảy;
- bi va bi không nảy;
- mất tốc 0,3 mỗi giây;
- không lệch ngẫu nhiên khi chạm đinh.

Trọng lực 1.100 và tốc độ kẹp 150–525 (trần gấp 3,5 sàn như máy tham khảo) chọn cho mặt máy đinh dày này: chép nguyên số của máy tham khảo (đổi theo đường kính bi) thì bi bay trung vị 9 giây. Đó là các giá trị khởi điểm, chỉnh được. Cốc tròn tính khi bi đang rơi qua tâm. Két tính khi tâm bi lọt vào vùng cảm biến bên trong.

Mọi phần ngẫu nhiên MUST lấy từ bộ số có hạt giống. Sin và cos của góc lệch (khi có lệch) MUST tính bằng cùng một đa thức chỉ dùng cộng, trừ, nhân, chia ở bản web và Unity, để hai bên ra cùng từng bit. Bi lăn quá 14 giây MUST bị đẩy xuống.

#### Scenario: Tỉ lệ khớp bản web
- **WHEN** chạy mô phỏng 6.000 bi cùng cách thả trên Unity và bản web
- **THEN** tỉ lệ từng ô và cốc lệch nhau dưới 1 điểm phần trăm, và 400 bi đầu rơi vào cùng chỗ

#### Scenario: Bi bồng bềnh mà không kéo dài đợt
- **WHEN** thả 6.000 bi đều
- **THEN** thời gian bay trung vị trong khoảng 4–5 giây

### Requirement: Bảng tỉ lệ công khai
Nút "Tỉ lệ" SHALL mở bảng ghi:
- tỉ lệ từng loại ô và cốc theo số đo mô phỏng. Số đo hiện tại: rương vàng ≈3,2% (két và ô khuất dưới két), bạc ≈5,6%, gỗ ≈7,8%, EXP 15 ≈22,1%, EXP 10 ≈22,1%, EXP 5 ≈29,9%, +1 bi ≈9,4%;
- bảng rương;
- tỉ lệ thẻ Huyền thoại;
- mốc 300 bi;
- câu "×N nhân mọi thưởng, kể cả số thẻ trong rương".

Số trong bảng MUST cập nhật mỗi khi mặt máy hoặc vật lý đổi (chạy lại mô phỏng). Kinh tế mỗi bi ở ×1 (EXP, bi hoàn, thẻ) MUST giữ như mặt máy cũ, lệch dưới 5%.

#### Scenario: Xem tỉ lệ
- **WHEN** người chơi bấm "Tỉ lệ"
- **THEN** bảng hiện đủ các mục trên, ghi chú "Đo bằng mô phỏng 6.000 bi", dòng rương vàng ghi "két giữa máy và ô khuất dưới két"

### Requirement: Phản hồi hình và tiếng
Máy SHALL phản hồi từng va chạm và từng thưởng. Hình chép cấu trúc, thời lượng, số hạt, tốc và trọng lực hạt của máy bi tham khảo (`GD_Claude/07_MayBi.md`, mục "Hiệu ứng chép"); hình hạt là ảnh `fx_*` (ảnh thay thế, thay bằng ảnh gen P4 khi có). Hạt chạy theo giờ của máy (chậm lại khi máy chạy chậm). Gồm:
- vệt đuôi mỗi bi: dải liền 0,3 giây, rộng hơn bi một chút, màu bi, mờ dần về đuôi;
- đinh loé vàng khi bị chạm mạnh: phồng 1,15 → 1 trong 0,067 giây, quầng sau đinh co 1,10 → 0,68, rồi mờ trong 0,1 giây; hai lấp lánh nhỏ văng ra;
- nấm phồng xẹp 0,23 giây (0,9 → 1,18 → 0,89 → 1,05 → 1) kèm quầng và vòng lan theo màu nấm;
- thả bi: máng mây co giãn 0,23 giây, khói và chớp dưới mây;
- bi rơi vào ô: ba quầng, sáu sao bắn ra rồi lơ lửng, sáu vệt sáng hướng tâm;
- bi lọt cốc bạc: chớp, vòng, mười chấm và mười sao văng;
- rương rơi vào: bảng loé (chớp, quầng, hai vòng, sao), rương vàng thêm sáu tia bắn nhanh;
- tiếng chạm đinh cách nhau ít nhất 0,1 giây, ba biến thể cao độ không lặp liền nhau, độ to theo tốc độ, tối đa 0,6;
- ô sáng khi bi rơi vào (ô thường 0,5 giây, rương gỗ và bạc 1,1 giây, rương vàng 1,6 giây và nhấp nháy);
- chữ nổi ("+10 XP" tím, "+1 bi" hồng, "Rương Vàng!");
- rương bay từ chỗ rơi vào khay;
- rung chia bậc theo giá trị: đinh nhẹ nhất, rồi thả bi, ô thường, rương gỗ, bạc, vàng. Rung bật tắt bằng nút "Rung" trong Sổ tay (lưu trong bản lưu, mặc định bật; bật lên thì rung thử một cú).

Chỉ rương vàng MUST có thêm:
- bộ jackpot khoảng 0,5 giây: vòng, hai quầng to gần bằng mặt máy, bốn tia rơi nhẹ, ba sao bắn, một sao nảy, sao lõi;
- máy chạy chậm 0,3× trong 0,45 giây rồi nhanh dần lại trong 0,25 giây, máng thả tạm ngừng;
- mặt máy rung;
- vòng loé thứ hai to hơn;
- ba tiếng xu lên cao dần.

Hộp mở rương MUST lắc lâu hơn với rương quý (gỗ 0,65, bạc 0,85, vàng 1,1 giây, vàng lắc mạnh dần) trước khi bật. Lên cấp báo bằng hộp "Lên cấp!" sau khi mở hết rương, không chồng hộp.

#### Scenario: Lên cấp do rương
- **WHEN** EXP từ ô và rương trong một đợt đủ lên cấp
- **THEN** hộp rương hiện trước; mở xong rương cuối thì hộp "Lên cấp!" mới hiện

#### Scenario: Rương vàng
- **WHEN** một bi lọt vào két vàng trong lúc người chơi đang giữ nút thả
- **THEN** máy chạy chậm rồi nhanh dần lại trong khoảng 0,7 giây, không thả thêm bi trong lúc đó, mặt máy rung, chữ "Rương Vàng!" nổi to, rồi rương bay vào khay

#### Scenario: Nhiều bi chạm đinh cùng lúc
- **WHEN** 30 bi đang lăn và chạm đinh liên tục
- **THEN** tiếng chạm đinh phát không quá 10 lần mỗi giây, hai tiếng liền nhau khác cao độ

### Requirement: Rời máy khi bi đang rơi
Khi người chơi rời scene máy trong lúc còn bi đang lăn, mỗi bi đó SHALL được tính như rơi vào ô EXP 10 (EXP 10 × mức cược). Rương đang chờ MUST giữ lại trong khay cho lần sau.

#### Scenario: Thoát giữa chừng
- **WHEN** người chơi bấm quay lại khi còn 5 bi ×1 đang lăn và 1 rương trong khay
- **THEN** người chơi nhận 50 EXP; lần sau vào máy, rương vẫn ở khay
