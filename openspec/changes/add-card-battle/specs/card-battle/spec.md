## ADDED Requirements

### Requirement: Đội hình
Mỗi bên SHALL mang từ 1 đến 3 tướng vào trận. Tướng đầu danh sách ra sân trước, các tướng còn lại dự bị. Mỗi tướng MUST giữ riêng máu, mana, nộ, khiên, buff và trạng thái suốt trận, kể cả lúc ngồi dự bị.

#### Scenario: Một tướng
- **WHEN** người chơi mới chỉ có Tiểu Y và vào ải 1 Đảo Thủy
- **THEN** trận diễn ra 1 đấu 1, không có ô dự bị để đổi

#### Scenario: Nộ giữ riêng theo tướng
- **WHEN** Võ Sư có 80 nộ rồi bị đổi xuống dự bị
- **THEN** Võ Sư vẫn giữ 80 nộ khi được đổi lên lại

### Requirement: Hiệp và thứ tự lượt
Trận SHALL chia thành hiệp, mỗi hiệp mỗi bên đi một lượt, luân phiên. Người chơi MUST luôn đi trước mỗi hiệp (chủ dự án chốt 2026-10-31), bất kể Tốc. Một bên chọn thẻ và ra đòn xong thì mới tới bên kia.

#### Scenario: Địch nhanh hơn vẫn đi sau
- **WHEN** Gia Bỉ (Tốc 114) của địch gặp Võ Sư (Tốc 46) của người chơi
- **THEN** đầu hiệp hiện "Hiệp 1 · Bạn đi trước", và người chơi đi lượt đầu

### Requirement: Đầu lượt
Đầu lượt của một bên, theo thứ tự, game SHALL:
1. bỏ các buff hết hạn kiểu "tới lượt sau" và trạng thái né chưa dùng;
2. tính bỏng (mất phần trăm máu tối đa) và hồi phục;
3. chạy bị động đầu lượt;
4. cộng 20 mana cho tướng đang ra sân, 10 mana cho mỗi tướng dự bị còn sống;
5. xét choáng;
6. rút 3 thẻ đầu tiên.

Mana và nộ MUST không vượt quá 100.

#### Scenario: Bỏng làm gục đầu lượt
- **WHEN** tướng đang ra sân bị bỏng gục ở bước 2
- **THEN** bên đó chọn tướng thay ngay (người chơi chọn trong hộp, máy tự chọn), rồi tướng thay đi tiếp lượt này từ bước 3, không tính bỏng lần nữa

### Requirement: Đổi tướng đầu lượt
Trong lượt của mình, trước lần chọn thẻ đầu tiên và trước khi bật chiêu hay tuyệt kỹ, mỗi bên SHALL được đổi tướng đang ra sân với một tướng dự bị còn sống, tối đa một lần mỗi lượt, không mất gì. Tướng vừa vào sân MUST nhận đủ mana của lượt (bù phần chênh giữa mana ra sân và mana dự bị). Địch do máy điều khiển cũng được đổi tướng.

#### Scenario: Đổi sau khi đã chọn thẻ
- **WHEN** người chơi đã chọn 1 thẻ rồi chạm vào chân dung tướng dự bị
- **THEN** không đổi được, và thông báo "Chỉ đổi tướng đầu lượt, trước khi chọn thẻ"

#### Scenario: Đổi để khắc hệ
- **WHEN** đầu lượt, người chơi đổi từ Gia Bỉ (Mộc) sang Võ Sư (Thổ) khi địch là Tiểu Y (Thủy)
- **THEN** Võ Sư ra sân với mana của lượt, và đòn của Võ Sư lên Tiểu Y nhân 1,5

### Requirement: Chọn thẻ chung
Mỗi lượt, bên đang đi SHALL chọn 5 lần (3 lần nếu bị choáng). Mỗi lần game rút 3 thẻ chung khác nhau theo trọng số độ hiếm (Thường 50, Khá 30, Hiếm 14, Sử thi 5, Huyền thoại 1), chỉ trong số thẻ đã mở theo cấp người chơi. Thẻ được chọn MUST xếp vào cuối hàng thẻ của lượt.

#### Scenario: Thẻ chưa mở
- **WHEN** người chơi cấp 4 rút thẻ
- **THEN** không bao giờ rút ra Gương Đôi (mở ở cấp 5) hay Thiên Mệnh (mở ở cấp 10)

### Requirement: Chiêu
Trong lúc chọn, bên đang đi SHALL được bật Chiêu của tướng đang ra sân nếu đủ mana: tối đa một lần mỗi lượt, không tốn lần chọn. Mana bị trừ ngay khi bật. Chiêu MUST xếp vào hàng thẻ ngay sau các thẻ đã chọn tới lúc đó, nên thẻ tăng Công chọn trước sẽ làm Chiêu mạnh hơn.

#### Scenario: Thiếu mana
- **WHEN** Võ Sư có 20 mana và người chơi bấm Chiêu "Thiết Quyền" (30 mana)
- **THEN** nút rung, báo "Chưa đủ mana", hàng thẻ không đổi

#### Scenario: Chiêu sau thẻ tăng Công
- **WHEN** người chơi chọn "Mài Vuốt" rồi bật Chiêu, rồi chọn thêm 4 thẻ
- **THEN** Chiêu đứng ở ô thứ 2 của hàng và chạy khi Công đã +25%

### Requirement: Tuyệt kỹ
Khi tướng đang ra sân có đủ 100 nộ và đủ mana theo giá của Tuyệt kỹ, bên đang đi SHALL được bật Tuyệt kỹ trong lúc chọn, không tốn lần chọn. Nộ và mana bị trừ ngay. Tuyệt kỹ MUST chạy sau toàn bộ hàng thẻ và thay cho cú đánh thường của lượt đó.

#### Scenario: Bật Tuyệt kỹ
- **WHEN** Võ Sư có 100 nộ và 40 mana rồi bật "Bách Liệt Quyền"
- **THEN** ô đòn kết của hàng thẻ đổi thành Bách Liệt Quyền; cuối lượt Võ Sư đánh 5 lần, mỗi lần 50% Công, và không đánh thường

### Requirement: Chạy hàng thẻ và ra đòn
Chọn xong, game SHALL chạy từng thẻ trong hàng theo thứ tự, áp hiệu ứng lên bên mình hoặc lên tướng địch đang ra sân. Sau đó là cú đánh thường 100% Công, các cú đánh thêm (nếu có), hoặc Tuyệt kỹ nếu đã bật. Thẻ "Gương Đôi" MUST làm thẻ ngay sau nó chạy hai lần. Hiệu ứng sát thương MUST bỏ qua nếu tướng địch đang ra sân đã gục.

#### Scenario: Địch gục giữa hàng thẻ
- **WHEN** thẻ thứ 3 hạ gục tướng địch và còn 2 thẻ sau
- **THEN** 2 thẻ sau vẫn chạy phần lên bản thân (hồi máu, buff); phần sát thương và cú đánh thường bị bỏ qua; địch chọn tướng thay trước lượt của địch

### Requirement: Mana và nộ
Mana và nộ SHALL tính riêng cho từng tướng, tối đa 100. Nộ MUST tăng:
- 10 mỗi cú đánh thường trúng;
- khi bị đánh: phần máu mất chia máu tối đa, nhân 80;
- khi tự mất máu (thẻ Liều Mạng): một nửa mức trên;
- từ thẻ và bị động.

#### Scenario: Bị đánh mất 25% máu
- **WHEN** tướng mất đúng 25% máu tối đa vì một đòn
- **THEN** tướng đó được thêm 20 nộ

### Requirement: Sát thương
Sát thương mỗi đòn SHALL bằng:

`Công × (1 + tổng buff Công, tối thiểu 0,1) × hệ số đòn × 100 / (100 + Thủ × (1 + tổng buff Thủ) × (1 − xuyên)) × khắc hệ × chí mạng × (1 + sát thương nhận thêm) × ngẫu nhiên 0,92–1,08`

Làm tròn và tối thiểu là 1. Các thành phần:
- **Khắc hệ** theo vòng Kim → Mộc → Thổ → Thủy → Hỏa → Kim: đánh hệ mình khắc ×1,5, đánh hệ khắc mình ×0,75.
- **Chí mạng:** gốc 5% cộng buff, ×1,6.
- **Khiên** đỡ trước máu.
- **Hút máu** hồi theo phần máu thực mất.
- **Thiên Mệnh:** cú đánh thường bỏ qua Thủ và nhân thêm hệ số của thẻ.

Mọi số là giá trị khởi điểm, chỉnh trong cấu hình cân bằng.

#### Scenario: Khiên đỡ trọn
- **WHEN** đòn 120 sát thương trúng tướng có 150 khiên
- **THEN** khiên còn 30, máu không mất, hiện "Khiên đỡ 120"

### Requirement: Thời hạn hiệu ứng
Buff và debuff SHALL có thời hạn:
- "lượt này" (hết khi kết thúc lượt của chủ);
- "tới lượt sau" (hết khi bắt đầu lượt sau của chủ, nên che được lượt của địch);
- "n lượt";
- "cả trận".

Mặc định: buff Công, chí mạng, hút máu là "lượt này"; buff Thủ, giảm sát thương nhận, né là "tới lượt sau". Debuff lên địch đếm theo lượt của địch.

#### Scenario: Giáp Gỗ che lượt địch
- **WHEN** người chơi dùng "Giáp Gỗ" trong lượt của mình
- **THEN** mọi đòn của địch ở lượt kế tiếp giảm 20% sát thương, và hiệu ứng hết khi lượt sau của người chơi bắt đầu

### Requirement: Trạng thái
Game SHALL có các trạng thái:
- **Bỏng:** mất phần trăm máu tối đa đầu mỗi lượt của tướng bị bỏng, n lượt, không qua khiên.
- **Hồi phục:** hồi phần trăm máu đầu mỗi lượt, n lượt.
- **Choáng:** lượt kế tiếp chỉ chọn 3 thẻ, không dùng Chiêu và Tuyệt kỹ, không ra đòn.
- **Né:** né trọn cú đánh thường kế tiếp; mất nếu chưa dùng khi tới lượt chủ.

Áp lại cùng trạng thái MUST làm mới số lượt và giữ mức cao hơn.

#### Scenario: Bị choáng
- **WHEN** tướng của người chơi bị "Bùa Choáng" ở lượt địch
- **THEN** lượt sau người chơi chỉ chọn 3 thẻ, nút Chiêu và Tuyệt kỹ khoá, ô đòn kết hiện "Choáng", cuối lượt không có cú đánh thường

### Requirement: Bị động
Thẻ bị động của mỗi tướng SHALL tự kích theo điều kiện ghi trên thẻ:
- vào trận (kể cả khi đang dự bị);
- đầu mỗi lượt của tướng đó khi đang ra sân;
- lần đầu máu xuống dưới ngưỡng;
- mỗi cú đánh thường (theo tỉ lệ);
- mỗi lần bị đánh;
- lần đầu gục (hồi sinh).

Mỗi lần kích MUST hiện tên bị động trên đầu tướng.

#### Scenario: Cánh Đêm
- **WHEN** Hắc Dực Vạn Quân lần đầu xuống dưới 50% máu
- **THEN** Hắc Dực được +25% Công cả trận, và hiện "◆ Cánh Đêm"

### Requirement: Tướng gục và thay tướng
Tướng hết máu (và không còn hồi sinh) SHALL gục. Nếu bên đó còn tướng sống, bên đó MUST chọn tướng thay trước lượt kế tiếp của họ (hoặc ngay đầu lượt nếu gục vì bỏng):
- người chơi chọn trong hộp thoại bắt buộc, có gợi ý "Khắc địch" / "Bị khắc";
- máy chọn tướng có điểm cao nhất theo tỉ lệ máu và khắc hệ với tướng địch đang ra sân.

#### Scenario: Người chơi mất tướng đầu
- **WHEN** tướng đang ra sân của người chơi gục và còn 2 tướng dự bị
- **THEN** hộp "Chọn tướng ra sân" hiện 2 tướng kèm máu và gợi ý khắc hệ; người chơi chọn xong thì trận tiếp tục

### Requirement: Hồi sinh
Hiệu ứng hồi sinh SHALL cho tướng vừa gục sống lại ngay với một phần trăm máu tối đa, xoá bỏng và choáng, giữ vị trí ra sân. Mỗi tướng MUST hồi sinh tối đa một lần mỗi trận. Tướng boss của địch MUST không hồi sinh. Nội dung khởi đầu: bị động "Phật Tâm" của Đại Sư Cà Sa là "lần đầu gục: hồi sinh với 35% máu".

#### Scenario: Đại Sư Cà Sa gục lần đầu
- **WHEN** Đại Sư Cà Sa nhận đòn chí mạng về 0 máu lần đầu trong trận
- **THEN** không có sự kiện gục; Đại Sư Cà Sa sống lại với 35% máu và hiện "◆ Phật Tâm"

### Requirement: Kết thúc trận
Trận SHALL kết thúc khi mọi tướng của một bên đã gục và không còn lần hồi sinh nào; bên còn lại thắng. Người chơi bỏ trận giữa chừng MUST tính là thua. Trận MUST có giới hạn an toàn 60 hiệp; quá giới hạn thì bên có tổng phần trăm máu cao hơn thắng.

#### Scenario: Thắng
- **WHEN** tướng địch cuối cùng gục
- **THEN** trận kết thúc, người chơi thắng, hộp kết quả hiện thưởng

### Requirement: Tái lập theo hạt giống
Mọi phần ngẫu nhiên của trận (rút thẻ, chí mạng, né, tỉ lệ hiệu ứng, ngẫu nhiên sát thương, máy chọn) SHALL lấy từ một bộ số ngẫu nhiên có hạt giống. Cùng hạt giống, cùng đội và cùng lựa chọn MUST cho ra cùng chuỗi sự kiện, cả trên Unity lẫn bản web.

#### Scenario: Đối chiếu với bản web
- **WHEN** chạy 200 trận máy tự chơi với các hạt giống cố định trên cả hai bản
- **THEN** chuỗi sự kiện và ảnh chụp số liệu trùng khớp từng sự kiện

### Requirement: Boss
Tướng boss SHALL có máu ×1,8 và Công ×1,1 so với tướng thường cùng cấp (giá trị khởi điểm), hiện to hơn khoảng 18% và có nhãn BOSS.

#### Scenario: Boss đảo Thủy
- **WHEN** vào ải 8 Đảo Thủy
- **THEN** Y Trạch cấp 6 của địch có nhãn BOSS và máu bằng 1,8 lần Y Trạch thường cấp 6
