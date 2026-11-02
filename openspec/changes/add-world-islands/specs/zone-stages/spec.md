## ADDED Requirements

### Requirement: Năm đảo hệ
Game SHALL có 5 đảo, mỗi đảo một hệ, 8 ải, với cấp đề nghị:

| Đảo | Cấp đề nghị |
|---|---|
| Thủy | 1–7 |
| Hỏa | 6–12 |
| Kim | 11–17 |
| Mộc | 16–22 |
| Thổ | 21–28 |

Địch mỗi đảo chủ yếu là tướng hệ của đảo đó. Mảnh rơi ra là tướng hệ đó, vì vậy đảo trước luôn rơi hệ khắc đảo sau. Ải 4 là mini boss, ải 8 là boss của đảo. Danh sách địch, cấp và rơi từng ải lấy từ dữ liệu (bảng ở `GD_Claude/11_BanWeb_TheBai.md`).

#### Scenario: Thứ tự khắc hệ
- **WHEN** người chơi chinh phục Đảo Thủy và có Y Trạch
- **THEN** Y Trạch (Thủy) khắc địch Hỏa ở đảo kế tiếp

### Requirement: Mở ải lần lượt trong đảo
Trong một đảo, ải SHALL mở lần lượt: ải n mở khi đã qua ải n − 1 của đảo đó. Ải đã qua MUST đánh lại được. Chạm ải chưa mở thì báo "Qua ải n − 1 của <đảo> trước đã".

#### Scenario: Đảo khác không ảnh hưởng
- **WHEN** người chơi mới qua ải 2 Đảo Thủy rồi vào Đảo Hỏa
- **THEN** ải 1 Đảo Hỏa mở được ngay, ải 2 Đảo Hỏa khoá

### Requirement: Scene đảo hệ
Scene đảo hệ SHALL hiện:
- ảnh đảo của hệ, phóng to và cuộn dọc;
- 8 ô ải đặt dọc đường mòn theo toạ độ dữ liệu: ô thường tròn có số, mini boss có vương miện, boss có đầu lâu và to hơn;
- ô đã qua tô xanh có dấu tích; ô đang đánh nhịp nhàng, có sticker tướng đội trưởng đứng cạnh; ô khoá xám có ổ khoá;
- đường đã đi vẽ nét chấm vàng nối các ô đã qua.

Vào scene MUST tự cuộn để ô đang đánh nằm giữa màn.

#### Scenario: Vào đảo đã đi một nửa
- **WHEN** người chơi vào Đảo Hỏa với 4/8 ải đã qua
- **THEN** màn cuộn tới ải 5, 4 ô đầu có dấu tích, nét chấm vàng nối ải 1 tới ải 5

### Requirement: Khung thông tin và rương mốc
Đầu scene đảo hệ SHALL có khung gồm:
- nhãn hệ, "Cấp đề nghị a–b", nhãn độ khó, "n/8 ải";
- thanh tiến độ có 2 rương mốc ở 4/8 và 8/8;
- một câu giới thiệu đảo kèm gợi ý hệ khắc ("Địch hệ Thủy: dùng tướng hệ Thổ để khắc").

Rương đủ điều kiện MUST lắc và mở được bằng cách chạm.

#### Scenario: Nhận rương nửa đảo
- **WHEN** người chơi qua ải 4 Đảo Thủy rồi chạm rương ở mốc 4
- **THEN** hộp "Rương nửa đảo" cho 10 bi và 2 bản sao thẻ riêng; rương mờ đi thành "Đã nhận"

### Requirement: Khung ải tiếp theo
Cuối scene đảo hệ SHALL có khung "Ải n/8 · <tên>" gồm:
- sticker và cấp các địch (nhãn BOSS nếu có);
- thưởng bi lần đầu;
- dòng "<tướng> gia nhập đội!" nếu ải tặng tướng, hoặc "rơi mảnh <tướng>" nếu có;
- nút "Đánh!".

Đảo đã chinh phục thì khung ghi "Đã chinh phục <đảo>!" và nhắc đánh lại để kiếm bi, mảnh.

#### Scenario: Ải tặng tướng
- **WHEN** ải kế tiếp là ải 3 Đảo Thủy
- **THEN** khung ghi "+9 bi · Võ Sư gia nhập đội!"

### Requirement: Hộp chuẩn bị trận
Bấm "Đánh!" hoặc chạm một ải đã mở SHALL mở hộp chuẩn bị gồm:
- tên đảo và ải, nhãn MINI BOSS hoặc BOSS ĐẢO;
- cảnh báo khi cấp người chơi thấp hơn cấp địch cao nhất trên 2 cấp;
- đối thủ (sticker, tên, hệ, cấp, "Boss: máu ×1,8");
- phần thưởng (bi kèm "lần đầu", mảnh kèm khoảng và tỉ lệ, tướng tặng);
- 3 ô đội hình (chạm để bỏ), kho tướng đã có kèm mũi tên xanh (khắc tướng chính của địch) hoặc đỏ (bị khắc);
- nút "Xuất trận!" (xám khi đội trống).

Xuất trận MUST lưu đội rồi chuyển sang trận.

#### Scenario: Cảnh báo quá sức
- **WHEN** người chơi cấp 3 mở hộp chuẩn bị ải 8 Đảo Hỏa (boss cấp 11)
- **THEN** hộp có dòng đỏ "Cảnh báo: địch cấp 11, bạn mới cấp 3. Đảo này đang quá mạnh, nên nuôi tướng thêm."

### Requirement: Thưởng ải
Thắng ải SHALL cho bi theo công thức (o là thứ tự đảo 0–4):
- cơ bản: `3 + 4·o + floor((ải − 1) / 2)`;
- lần đầu cộng thêm `5 + 2·o`, mini boss thêm 3, boss thêm 7.

Mảnh tướng:
- lần đầu theo tỉ lệ dữ liệu;
- đánh lại: tỉ lệ 100% còn 50%, tỉ lệ khác nhân 0,8.

Tướng tặng chỉ ở lần đầu. Thua MUST không cho thưởng nhưng vẫn tính vào thống kê.

#### Scenario: Đánh lại boss
- **WHEN** người chơi thắng lại boss Đảo Thủy (lần đầu rơi Y Trạch 100%)
- **THEN** thưởng 6 bi cơ bản, và 50% cơ hội rơi 4–6 mảnh Y Trạch
