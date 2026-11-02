## ADDED Requirements

### Requirement: Mở Đền Huy Hiệu
Đền Huy Hiệu SHALL mở khi người chơi thắng boss Đảo Thủy (ải 8) lần đầu. Trước đó, công trình đền trên sảnh MUST hiện nét chì mờ; chạm vào báo "Thắng boss Đảo Thủy để mở Đền Huy Hiệu".

#### Scenario: Vừa thắng boss Đảo Thủy
- **WHEN** người chơi thắng ải 8 Đảo Thủy lần đầu
- **THEN** quay về sảnh thấy Đền Huy Hiệu tô màu, có chấm báo mới

### Requirement: Dãy huy hiệu theo hệ
Đền SHALL có 5 dãy huy hiệu, một dãy mỗi hệ, mỗi dãy 5 bậc: Đồng, Bạc, Vàng, Ngọc, Kim Cương. Dãy hệ X MUST mở khi người chơi thắng mini boss (ải 4) của Đảo X lần đầu. Dãy chưa mở hiện điều kiện mở.

#### Scenario: Dãy chưa mở
- **WHEN** người chơi chưa thắng ải 4 Đảo Kim
- **THEN** dãy Kim ghi "Thắng mini boss Đảo Kim để mở"

### Requirement: Thử thách theo bậc
Mỗi bậc SHALL là một chuỗi trận boss của hệ đó: bậc 1–2 có 5 trận, bậc 3–5 có 10 trận. Đánh lần lượt; thua thì đánh lại đúng trận đó, không mất tiến độ. Trong chuỗi:
- trận lẻ: 1 boss;
- trận chẵn: 2 tướng, có 1 boss;
- trận cuối: 3 tướng, boss là tướng hiếm nhất của hệ.

Cấp địch MUST bằng `cận dưới cấp đề nghị của đảo + 3·(bậc − 1) + floor(số trận / 2)`. Thử thách MUST không quét nhanh và không chạy AFK; nút "Tự chơi" trong trận vẫn dùng được.

#### Scenario: Thua giữa chuỗi
- **WHEN** người chơi đang ở trận 7/10 của bậc Vàng hệ Hỏa và thua
- **THEN** tiến độ vẫn là 6/10; lần sau đánh lại trận 7 với cùng đội địch

### Requirement: Thưởng thử thách
Mỗi trận thắng trong thử thách SHALL cho `5 + 2·bậc` bi. Xong một bậc MUST trao huy hiệu bậc đó, kèm một rương (bạc với bậc 1–2, vàng với bậc 3–5) mở ngay bằng hộp rương.

#### Scenario: Xong bậc Đồng hệ Thủy
- **WHEN** người chơi thắng trận 5/5 bậc Đồng hệ Thủy
- **THEN** hộp "Huy hiệu Thủy · Đồng" hiện, kèm mở một rương bạc; tướng hệ Thủy được +5%

### Requirement: Sức mạnh huy hiệu
Tướng hệ X SHALL được cộng Máu, Công, Thủ theo bậc huy hiệu cao nhất của hệ X: Đồng +5%, Bạc +8%, Vàng +12%, Ngọc +16%, Kim Cương +20% (giá trị khởi điểm). Các bậc MUST không cộng dồn nhau. Phần cộng áp cho trận ở đảo, trận thử thách, và chỉ số hiện ở màn Tướng.

#### Scenario: Có huy hiệu Bạc hệ Thủy
- **WHEN** người chơi có huy hiệu Bạc hệ Thủy và mở chi tiết Y Trạch
- **THEN** Máu, Công, Thủ của Y Trạch cao hơn 8% so với khi chưa có huy hiệu, và cạnh nhãn hệ có icon huy hiệu Bạc

### Requirement: Scene Đền Huy Hiệu
Scene Đền SHALL hiện 5 bệ huy hiệu theo hệ. Mỗi bệ có:
- huy hiệu bậc cao nhất đã có (hoặc bóng mờ);
- bậc đang đánh và tiến độ "n/5" hoặc "n/10";
- phần cộng hiện tại;
- nút "Thử thách".

Chạm "Thử thách" MUST mở danh sách các trận của bậc (sticker boss, cấp, trạng thái); chạm trận đang đánh thì mở hộp chuẩn bị trận dùng chung với đảo.

#### Scenario: Mở danh sách trận
- **WHEN** người chơi chạm "Thử thách" ở bệ Mộc đang 2/5 bậc Đồng
- **THEN** danh sách hiện 5 trận: 2 trận đầu có dấu tích, trận 3 sáng có nút đánh, 2 trận sau khoá
