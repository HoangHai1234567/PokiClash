# Gói gửi GPT: Tiểu Y dạng 1/2 (Tiểu Y, `tieu_y_1`)

Tướng Thường hệ Thủy, dạng 1/2, rig aola #1319. Thiết kế: tiểu thần biển dạng người (người dùng chốt 2026-11-04: giữ theme thần Poseidon, dạng người): bé trai chibi tóc xanh thẫm thành năm lọn sóng cuộn, ngọn vỡ bọt trắng; chóp vương miện vàng nhỏ có ngọc trai trên trán, kẹp sao biển vàng trên lọn tóc phải; hai vây tai xanh ngọc viền vàng; da hồng nhạt, mắt xanh ngọc to; hai vai vỏ sò điệp trắng ngà viền vàng; cổ áo chiton trắng viền hoa văn sóng vàng, ghim tròn vàng có ngọc xanh ngọc; tay mũm mĩm đeo vòng vàng mảnh, cầm đinh ba tập sự cán gỗ trôi dạt, ba mũi vỏ sò trắng ngà buộc vàng; nửa dưới là vòi rồng nước nhỏ; mặt quả quyết, cười tự tin. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\tieu_y_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\tieu_y_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\tieu_y_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tieu_y_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (438 × 533): con gốc #1319 là bé chibi nhìn chéo 3/4 quay phải: đầu rất to, chỏm năm lọn tóc to vuốt lên, hai vây tai sau hai bên đầu (vây trái to chĩa lên trái, vây phải mảnh chĩa lên), hai cục vai ở hai bên dưới đầu, cổ giáp nhỏ dưới cằm, không thấy cánh tay; tay trái nắm cây đinh ba ngắn nằm chéo (đuôi cán trên trái, đầu dưới phải), tay phải nắm lại cạnh cằm; nửa dưới là lốc nước thay chân. Bỏ khỏi bóng xám: bóng dưới chân và hai vòng nước |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tieu_y_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (438 × 533, nền trắng): 1 hai vây tai, 2 chỏm năm lọn tóc, 3 đầu và mặt, 4 hai hạt trang sức nhỏ (trán, lọn tóc phải), 5 hai cục vai, 6 cổ giáp dưới cằm, 7 tay trái nắm đinh ba, 8 nắm tay phải, 9 đinh ba, 10 lốc nước thay chân (vùng hồng phía dưới; số 10 in đè lên chỗ đinh ba) |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept tieu_y_1". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\tieu_y_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\tieu_y_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\tieu_y_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N02. Gõ `next`: GPT vẽ N05. Nhắn Claude "soi thử tieu_y_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N01, N03, N04, N06, N07.
3. Đủ ảnh thì nhắn Claude "ghép tieu_y_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tieu_y_1\orig\N01.png` | Hai vây xanh lam có vảy (1024 × 1024, nền trắng): vây trái to chĩa lên trái, gốc ở góc dưới bên phải; vây phải mảnh chĩa lên, gốc ở đầu dưới; khoảng trống giữa là chỗ của đầu |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tieu_y_1\orig\N02.png` | Đầu tròn to (1024 × 1024, nền trắng): mảng tóc nâu trùm đỉnh và trán, mặt da nâu ở dưới, hai mắt to đỏ hơi lệch sang phải, má hồng; năm lọn tóc và hai vây là nhóm khác |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tieu_y_1\orig\N03.png` | Năm lọn tóc trắng xám to vuốt lên (1024 × 1024, nền trắng): hai lọn lớn trên trái và trên phải, ba lọn nhỏ phía trước trán; hai hạt xanh, một trên lọn trước trán, một trên lọn phải |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tieu_y_1\orig\N04.png` | Ba mảnh (1024 × 1024, nền trắng): hai cục vàng hình thoi hai bên (vai), giữa là cổ giáp vàng có ngọc xanh, ngay dưới cằm |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tieu_y_1\orig\N05.png` | Bàn tay nhỏ (1024 × 1024, nền trắng, khung rộng): nắm quanh cán chéo (cán không có trong ảnh), cổ tay ở trên phải có vòng vàng, khớp ngón ở dưới trái |
| 6 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tieu_y_1\orig\N06.png` | Nắm tay tròn nhỏ (1024 × 1024, nền trắng, nằm giữa khung rộng): ngón cái ở trên |
| 7 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tieu_y_1\orig\N07.png` | Đinh ba vàng nằm chéo (1024 × 1024, nền trắng): đuôi cán ở trên trái, đầu ở dưới phải (mũi giữa hình lá, hai mũi bên cong, ngọc xanh ở chỗ nối) |
| 8 | `D:\PokiClash\ArtGen\Heroes\inbox\tieu_y_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 hai vây tai** (đổi dáng, viền khoảng 9 px):
- gốc vây trái ở góc dưới phải, gốc vây phải ở đầu dưới, đúng chỗ gốc cũ;
- vây cá xanh ngọc viền vàng mảnh, vài gân xanh đậm, đúng hướng cũ, cỡ như cũ hoặc to hơn chút;
- không vẽ đầu, tóc, vảy xanh lam.

**N02 đầu và mặt** (đổi dáng, viền khoảng 15 px):
- cằm đúng chỗ cũ, đầu cỡ như cũ; hai mắt đúng chỗ hai mắt cũ;
- mặt bé trai da hồng nhạt, mắt xanh ngọc to, mày xếch xuống, cười tự tin; mảng tóc xanh thẫm trùm đỉnh và trán ở chỗ mũ tóc nâu cũ;
- không vẽ năm lọn tóc to, vây, chóp vương miện (nhóm N03); không mắt đỏ, không vệt đỏ trên má;
- tô phẳng, chỉ một chấm sáng nhỏ trong mỗi mắt.

**N03 chỏm tóc sóng, chóp vương miện, kẹp sao biển** (đổi dáng, viền khoảng 11 px):
- năm lọn đúng chỗ, đúng hướng, gốc lọn dọc đỉnh đầu như cũ;
- mỗi lọn là sóng cuộn tóc xanh thẫm, ngọn vỡ thành bọt trắng;
- chỗ hạt trước trán: chóp vương miện vàng nhỏ giữ ngọc trai trắng; chỗ hạt bên phải: kẹp sao biển vàng nhỏ;
- không vẽ mặt, vây; không tóc trắng xám.

**N04 vai vỏ sò và cổ áo** (giữ viền, viền khoảng 13 px):
- ba mảnh đúng chỗ, đúng cỡ cũ;
- hai vai thành vỏ sò điệp trắng ngà viền vàng; giữa là cổ áo chiton trắng viền hoa văn sóng vàng, ghim tròn vàng có ngọc xanh ngọc;
- không vẽ đầu, tay, lốc nước.

**N05 tay trái nắm đinh ba** (giữ viền, viền khoảng 23 px):
- viền và chỗ như cũ; cổ tay trên phải, khớp ngón dưới trái;
- tay mũm mĩm da hồng nhạt, vòng vàng mảnh ở cổ tay;
- nắm rỗng, không vẽ cán đinh ba (cán ở nhóm N07).

**N06 nắm tay phải** (giữ viền, viền khoảng 18 px):
- đúng chỗ, đúng cỡ cũ;
- nắm tay mũm mĩm da hồng nhạt, vòng vàng mảnh ở cổ tay nếu có chỗ;
- không vẽ cánh tay.

**N07 đinh ba tập sự** (đổi dáng, viền khoảng 16 px):
- cán chéo đúng đường cũ, đuôi cán trên trái, đầu dưới phải, dài như cũ;
- cán gỗ trôi dạt nhạt màu, dây xanh quấn hai chỗ (gần đuôi cán và ngay dưới đầu) như concept;
- chạc vàng nhỏ giữ ba mũi là vỏ ốc xoắn trắng ngà, mũi giữa dài nhất, chĩa xuống phải;
- không vẽ bàn tay; không cán vàng, không ngọc xanh.

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Không giống vẽ tay trên giấy, không thấy nét chì sáp | `Draw it by hand on paper: dark-brown ink-pen outlines, every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |
| Có mảng sáng tối, điểm sáng trắng, bóng loáng, chuyển sắc | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine (only a small catchlight dot in each eye), no glow, no gradients.` |
| Nét nguệch ngoạc, quá thô | `Hand-drawn but clean and appealing, like a professional storybook illustrator; not a crude scribble.` |
| Có viền trắng quanh hình | `No white border or sticker outline; the game adds it.` |
| Mặt vui tươi, cười toe | `Make the face battle-ready: brows angled down, a small confident smile; not a big happy grin.` |
| Vẽ cả con hoặc thêm phần ngoài nhóm | `Only the pieces of image 1, nothing else.` |
| Mảnh lệch chỗ, xoay, đổi cỡ | `Put every piece back exactly where it is in image 1: same position, size and angle on the same 1024 x 1024 canvas.` |
| Bàn tay, bàn chân ở sai đầu | `The hand/foot is at the BOTTOM end; the TOP end is the shoulder/hip.` |
| Viền mảnh quá mảnh hoặc quá dày | `Make the dark-brown outline about <N> px thick, the same on every edge.` (N ghi ở từng nhóm trên) |
| Có bóng đổ, bóng dưới chân, bóng in xuống nền | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine (only a small catchlight dot in each eye), no glow, no gradients.` |
| Nền xám, có ô lưới | `Plain pure white background, nothing else.` |

Gói này sinh từ `D:\PokiClash\ArtGen\Heroes\build.py`; sửa prompt ở đó rồi chạy lại.
