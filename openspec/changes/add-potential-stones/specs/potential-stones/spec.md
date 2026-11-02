## ADDED Requirements

### Requirement: Đá tiềm năng và nguồn
Game SHALL có tài nguyên đá tiềm năng, đến từ:
- rương bạc của máy bi (8%, 1–2 đá);
- rương vàng (12%, 2–4 đá);
- Hang Tiềm Năng;
- rương AFK (hiếm).

Mức cược ×N của máy bi MUST nhân số đá như mọi thưởng khác. Bảng tỉ lệ máy bi MUST cập nhật theo.

#### Scenario: Rương vàng ra đá ở ×3
- **WHEN** rương vàng ở ×3 quay ra "3 đá tiềm năng"
- **THEN** người chơi nhận 9 đá

### Requirement: Bốn ô tiềm năng
Mỗi tướng SHALL có 4 ô tiềm năng, mở theo sao: ô 1 từ 1 sao, ô 2 từ 2 sao, ô 3 từ 3 sao, ô 4 từ 4 sao. Ô chưa mở MUST ghi "Mở ở n sao".

#### Scenario: Tướng 2 sao
- **WHEN** người chơi mở mục Tiềm năng của Tiểu Y 2 sao
- **THEN** 2 ô đầu dùng được, ô 3 ghi "Mở ở 3 sao", ô 4 ghi "Mở ở 4 sao"

### Requirement: Khai phá tiềm năng
Bấm "Khai phá" SHALL quay lại mọi ô đã mở và không khoá. Mỗi ô ra một dòng: loại chỉ số (8 loại đều nhau) và độ hiếm (Thường 55, Khá 28, Hiếm 12, Sử thi 4,5, Huyền thoại 0,5). Giá bằng số ô được quay, cộng 2 đá cho mỗi ô khoá; khoá tối đa 2 ô. Kết quả MUST hiện cạnh dòng cũ để người chơi chọn "Giữ mới" hoặc "Giữ cũ". Đá đã tiêu không hoàn.

#### Scenario: Khoá một ô
- **WHEN** tướng có 3 ô mở, người chơi khoá ô có "Công +12% (Sử thi)" rồi khai phá
- **THEN** tốn 2 + 2 = 4 đá; chỉ 2 ô còn lại được quay; ô khoá giữ nguyên

#### Scenario: Giữ cũ
- **WHEN** kết quả mới tệ hơn và người chơi chọn "Giữ cũ"
- **THEN** các ô trở lại như trước khi khai phá, đá vẫn bị trừ

#### Scenario: Thiếu đá
- **WHEN** người chơi có 1 đá mà giá khai phá là 3
- **THEN** nút Khai phá xám, ghi "Cần 3 đá"

### Requirement: Dòng tiềm năng áp vào tướng
Dòng Công %, Thủ %, Máu %, Tốc SHALL cộng vào chỉ số tướng qua phần cộng chung, nên thấy ở màn Tướng, trong trận và trong công cụ cân bằng. Dòng Chí mạng % và Hút máu % MUST thành buff "cả trận" khi vào trận. Dòng Mana và Nộ đầu trận MUST cộng vào mana và nộ lúc dựng tướng. Mỗi loại có trần tổng +40% (Tốc +30, mana và nộ +50).

#### Scenario: Nộ đầu trận
- **WHEN** Võ Sư có hai dòng "Nộ đầu trận +20" và "+15"
- **THEN** Võ Sư vào trận với 35 nộ

### Requirement: Hang Tiềm Năng
Hang Tiềm Năng SHALL mở khi người chơi thắng mini boss Đảo Hỏa lần đầu. Hang có 4 tầng:

| Tầng | Cấp đề nghị | Đá khi thắng |
|---|---|---|
| Dễ | 6 | 2 |
| Thường | 12 | 3 |
| Khó | 18 | 5 |
| Ác mộng | 24 | 8 |

Mỗi lần vào là một trận với 1 boss và 1 tướng phụ, hệ của boss đổi theo ngày trong tuần. Người chơi MUST tự đánh (có Tự chơi trong trận, không có quét, không AFK). Mỗi ngày có 3 lượt, chỉ trừ khi thắng; xem quảng cáo được thêm 1 lượt mỗi ngày.

#### Scenario: Hết lượt
- **WHEN** người chơi đã thắng 3 lần trong ngày
- **THEN** các tầng ghi "Hết lượt hôm nay", kèm nút "+1 lượt" (quảng cáo) nếu chưa dùng

#### Scenario: Thua không mất lượt
- **WHEN** người chơi thua ở tầng Khó
- **THEN** số lượt còn lại không đổi

### Requirement: Mục Tiềm năng trong chi tiết tướng
Hộp chi tiết tướng SHALL có mục "Tiềm năng" gồm:
- 4 ô (dòng hiện tại có màu độ hiếm, hoặc trạng thái khoá theo sao);
- công tắc khoá từng ô (tối đa 2);
- số đá đang có;
- nút "Khai phá" kèm giá;
- tổng phần cộng từ tiềm năng.

#### Scenario: Xem tổng
- **WHEN** tướng có hai dòng "Máu +8%" và "Máu +5%"
- **THEN** mục Tiềm năng ghi tổng "Máu +13%", và Máu trong hộp chi tiết đã gồm phần này
