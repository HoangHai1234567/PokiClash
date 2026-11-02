## ADDED Requirements

### Requirement: Bố cục màn trận
Màn trận SHALL chia theo khung 540 × 960 của bản web (nhân 2 ở khung 1080 × 1920):
- **Thanh trên** (0–56): nút tạm dừng, "Hiệp n" (đầu hiệp có băng rôn "Hiệp n · Bạn đi trước"), nhãn "Lượt bạn" hoặc "Lượt địch", nút tốc độ ×1/×2/×3, nút Tự chơi.
- **Sân đấu** (56–520): nền theo hệ của đảo; địch đứng trên-trái, phe mình dưới-phải (lật ngang), cả hai dạng sticker; bảng thông tin địch ở trên-phải, của mình ở dưới-trái.
- **Bảng dưới** (520–960) nền giấy có dòng kẻ và lề đỏ:
  - dòng tiêu đề "Hàng thẻ của …" kèm "Chọn n/5";
  - hàng thẻ: các ô đã chọn, ô trống, mũi tên, ô đòn kết;
  - 3 thẻ để chọn;
  - hàng dưới: chân dung đội (có thanh máu nhỏ, nhãn "ĐANG ĐÁNH"), nút Chiêu và Tuyệt kỹ (có vạch nộ).

Bảng thông tin MUST có: tên, nhãn hệ, cấp, nhãn BOSS nếu có, thanh máu (kèm khiên), thanh mana, thanh nộ, chip buff Công/Thủ, chip trạng thái, chấm đội hình.

#### Scenario: Mở trận
- **WHEN** trận bắt đầu
- **THEN** mọi vùng trên hiện đúng chỗ, thanh số khớp ảnh chụp số liệu đầu trận

### Requirement: Màn VS mở đầu
Trước hiệp đầu, game SHALL hiện màn VS khoảng 1,5 giây: tên đảo và ải, đội địch ở trên, chữ "VS" to, đội mình ở dưới.

#### Scenario: Ải boss
- **WHEN** vào ải boss
- **THEN** màn VS hiện tướng boss to hơn các tướng khác

### Requirement: Chọn thẻ có hoạt cảnh
Khi người chơi chạm một thẻ, thẻ SHALL bay vào ô trống đầu tiên của hàng thẻ (khoảng 0,27 giây), rồi 3 thẻ mới được chia ra. Chọn đủ lần thì hàng thẻ chạy sau khoảng 0,35 giây. Chiêu bật lên MUST hiện ở đúng vị trí của nó trong hàng; Tuyệt kỹ bật lên đổi ô đòn kết.

#### Scenario: Chọn thẻ thứ 5
- **WHEN** người chơi chọn thẻ thứ 5
- **THEN** thẻ bay vào ô cuối, nhãn đổi thành "Ra đòn!", hàng thẻ bắt đầu chạy

### Requirement: Lượt địch nhìn thấy được
Trong lượt địch, bảng dưới SHALL hiện "<tên> đang chọn thẻ...":
- 3 lá úp chia một lần mỗi lượt;
- lá được chọn nhô lên rồi trở về;
- hàng thẻ của địch lấp dần theo lựa chọn.

Khi địch bật Chiêu hoặc Tuyệt kỹ, tên chiêu MUST hiện trên đầu tướng địch.

#### Scenario: Địch bật Tuyệt kỹ
- **WHEN** địch đủ nộ và bật Tuyệt kỹ
- **THEN** trên đầu tướng địch hiện "Tuyệt kỹ: <tên>", ô đòn kết của hàng địch đổi thành Tuyệt kỹ

### Requirement: Hoạt cảnh chạy thẻ
Khi một thẻ chạy, ô của nó SHALL nhô lên và sáng, một bản sao của ô bay lên đầu tướng rồi tan, tên thẻ hiện trên đầu tướng. Hiệu ứng của thẻ MUST hiện bằng chữ nổi màu:
- xanh lá: buff, hồi máu;
- đỏ: debuff, mất máu;
- xanh dương: mana, khiên;
- cam: nộ, bỏng.

Chữ liên tiếp xếp thành dòng tin.

#### Scenario: Năm thẻ liên tiếp
- **WHEN** năm thẻ chạy liền, mỗi thẻ có một hiệu ứng
- **THEN** mỗi tên thẻ và hiệu ứng hiện thành một dòng, dòng cũ đẩy lên trên, đọc được hết

### Requirement: Đòn đánh và trúng đòn
Đòn đánh SHALL có hoạt cảnh lao tới, trúng đòn và phụ chú như sau:
- **Cú đánh thường:** tướng chạy clip đánh, quãng lao được nắn để tới khoảng 72% quãng đường tới đối thủ; clip lao ít thì tướng tự nhún tới.
- **Khung trúng đòn:** đối thủ chạy clip trúng đòn và nháy trắng; màn rung (đòn mạnh rung mạnh hơn); bảng thông tin của đối thủ rung; nổ ngôi sao răng cưa có chữ tượng thanh; số sát thương nảy lên.
- **Phụ chú:** chí mạng hiện "CHÍ MẠNG!" và số vàng to; khắc hệ hiện "Khắc hệ ×1,5"; bị khắc hiện "Bị khắc ×0,75"; né hiện "Né!" và đối thủ nhảy lên.

#### Scenario: Đòn chí mạng khắc hệ
- **WHEN** Võ Sư đánh chí mạng lên Tiểu Y
- **THEN** sân rung mạnh, nổ "ẦM!!", số vàng to, kèm "CHÍ MẠNG!" và "Khắc hệ ×1,5"

### Requirement: Tuyệt kỹ có băng rôn
Khi Tuyệt kỹ chạy, game SHALL hiện băng rôn đỏ ngang màn có tên Tuyệt kỹ và tên tướng, sân đấu loé sáng, tướng chạy clip chiêu, rồi mới tới hiệu ứng trúng đòn.

#### Scenario: Tuyệt kỹ của địch
- **WHEN** địch dùng "Hải Long Quyển"
- **THEN** băng rôn "Hải Long Quyển · Tuyệt kỹ của Y Trạch" trượt qua, rồi đòn trúng tướng của người chơi

### Requirement: Trạng thái trên đầu tướng
Sân đấu SHALL vẽ trạng thái đang có trên đầu tướng:
- choáng: 3 ngôi sao xoay;
- bỏng: 3 ngọn lửa;
- hồi phục: dấu cộng bay lên;
- né: vòng nét đứt tím.

#### Scenario: Hết bỏng
- **WHEN** lượt bỏng cuối cùng qua đi
- **THEN** ngọn lửa trên đầu tướng biến mất

### Requirement: Gục, đổi tướng, hồi sinh
Sân đấu SHALL có hoạt cảnh riêng cho gục, đổi tướng và hồi sinh:
- **Gục:** tướng ngã nghiêng, xám dần, mờ đi, hiện "Gục!".
- **Đổi tướng:** tướng cũ trượt ra mép màn, tướng mới rơi từ trên xuống, nảy nhẹ, hiện "<tên>, ra sân!", bảng thông tin đổi theo.
- **Hồi sinh:** tướng đứng dậy, loé sáng, hiện tên bị động.

#### Scenario: Đổi tướng đầu lượt
- **WHEN** người chơi chạm chân dung Võ Sư đang dự bị lúc đầu lượt
- **THEN** tướng cũ rút lui, Võ Sư rơi xuống sân, chân dung Võ Sư có nhãn "ĐANG ĐÁNH"

### Requirement: Tốc độ, tự chơi, tạm dừng
Màn trận SHALL có nút tốc độ và hộp tạm dừng:
- **Tốc độ:** nút đổi ×1 → ×2 → ×3 → ×1, áp cho mọi hoạt cảnh và thời gian chờ, lưu làm mặc định.
- **Tạm dừng:** hộp gồm mẹo xếp thẻ, vòng khắc hệ, "Đánh tiếp" và "Bỏ trận (tính thua)".

#### Scenario: Bỏ trận
- **WHEN** người chơi chọn "Bỏ trận (tính thua)"
- **THEN** trận tính thua, game về scene đảo của ải đó

### Requirement: Gợi ý lần đầu
Ở hai trận đầu tiên của người chơi (khi bật gợi ý), game SHALL hiện bong bóng gợi ý một lần mỗi trận cho:
- cách chọn thẻ;
- nút Chiêu khi lần đầu đủ mana;
- nút Tuyệt kỹ khi lần đầu đủ nộ.

Bong bóng MUST tự tắt sau khoảng 4 giây, và không che hàng thẻ khi người chơi cần chạm.

#### Scenario: Lần đầu đủ mana
- **WHEN** ở trận đầu, tướng của người chơi lần đầu đủ mana cho Chiêu
- **THEN** bong bóng "Đủ mana: bấm Chiêu để xen chiêu vào hàng thẻ. Không tốn lần chọn!" hiện cạnh nút Chiêu

### Requirement: Hộp kết quả
Kết thúc trận, game SHALL hiện hộp kết quả không đóng được bằng chạm ngoài.

**Thắng:**
- con dấu đỏ "THẮNG!" đóng xuống (có tiếng);
- tên đảo và ải, số hiệp, sát thương đã gây;
- thưởng: bi (kèm nhãn "Lần đầu qua ải"), mảnh tướng (kèm tiến độ hoặc "Mở khóa <tên>!"), tướng tặng gia nhập;
- nút "Máy bi (n)", "Ải tiếp ➜" (nếu ải kế đã mở), "Đánh lại", "<tên đảo>".

**Thua:**
- con dấu xám "THUA RỒI";
- 3 mẹo: thả bi lên cấp, nâng thẻ và tiến hóa, dùng tướng khắc hệ địch (ghi đúng hệ khắc);
- nút "Đánh lại", "<tên đảo>".

Lên cấp trong lúc nhận thưởng thì hộp "Lên cấp!" hiện sau.

#### Scenario: Thắng ải 3 Đảo Thủy lần đầu
- **WHEN** người chơi thắng ải 3 Đảo Thủy lần đầu
- **THEN** hộp kết quả hiện "+9 bi · Lần đầu qua ải" và "Mở khóa Võ Sư!"
