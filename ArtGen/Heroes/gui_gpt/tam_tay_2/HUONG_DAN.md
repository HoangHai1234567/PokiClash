# Gói gửi GPT: Tám Tay dạng 2/2 (Tám Tay Pháo Thủ, `tam_tay_2`)

Tướng Khá hệ Thủy (quái thường đảo Thủy), dạng 2/2, rig aola #1054. Thiết kế: Tám Tay lớn lên thành pháo thủ: cùng da vàng cát vòng coban, mắt và mày như dạng 1; mũ giáp đồng thau có kính tiềm vọng nhỏ thay viên ngọc, hai que thổi bong bóng đồng to hơn; hai tai nghe là hai vỏ ốc xoắn; bong bóng nước chỉ viền; tám xúc tu ngồi thấp; xúc tu phải cầm pháo ống đồng miệng loe; hai pháo vỏ ốc anh vũ trắng kem sọc nâu cam bay hai bên. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_2\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\tam_tay_2\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_2\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\Silhouette.png` | Bóng xám của con gốc trên nền trắng (1092 × 1038): con gốc #1054 là bạch tuộc ngồi trên các xúc tu, nhìn thẳng: đầu hồng đỏ trong vòm kính, trên vòm là mũ giáp xanh có ngọc mắt đỏ, hai râu cong đầu tròn vàng mọc từ hai bên mũ, hai cục tai xanh hai bên vòm; tám xúc tu ngắn; xúc tu phải cầm khẩu pháo chĩa sang phải; hai pháo nhỏ bay hai bên (trái thấp, phải cao); các chùm bong bóng quanh chân. Bỏ khỏi bóng xám: bóng dưới chân |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (1092 × 1038, nền trắng): 1 mũ giáp có ngọc, 2 hai râu, 3 hai tai bên vòm, 4 vòm bong bóng, 5 đầu có mắt và miệng, 6 xúc tu, 7 pháo cầm ở xúc tu phải, 8 hai pháo bay, 9 các chùm bong bóng |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |
| 6 | `D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_1\concept_duyet.png` | Concept đã duyệt của `tam_tay_1` (1120 × 1405, nền trắng): dạng 1 đã duyệt: bạch tuộc vàng cát vòng coban trong bong bóng, mũ nồi đỏ mỏ neo, hai que thổi bong bóng |

Xong thì nhắn Claude "duyệt concept tam_tay_2". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_2\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\tam_tay_2\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_2\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N05. Gõ `next`: GPT vẽ N01. Nhắn Claude "soi thử tam_tay_2".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N02, N03, N04, N06, N07, N08, N09.
3. Đủ ảnh thì nhắn Claude "ghép tam_tay_2".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\orig\N01.png` | Mũ giáp xanh viền vàng có ngọc mắt đỏ ở giữa (1024 × 1024, nền trắng), rộng và cong |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\orig\N02.png` | Hai râu xanh nhỏ cong lên và vào trong (1024 × 1024, nền trắng), đầu mỗi râu có quả cầu vàng nhỏ |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\orig\N03.png` | Hai cục tai nhỏ màu xanh có đèn xanh ngọc (1024 × 1024, nền trắng), một bên trái, một bên phải |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\orig\N04.png` | Vòm kính tròn to xanh nhạt có vệt sáng trắng (1024 × 1024, nền trắng); đầu không có trong ảnh |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\orig\N05.png` | Đầu bạch tuộc tròn to hồng đỏ có mảng tím trên đỉnh (1024 × 1024, nền trắng), hai mắt xanh mày cau, miệng tròn nhỏ |
| 6 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\orig\N06.png` | Cụm xúc tu ngắn xoăn đỏ sẫm và tím dưới đầu (1024 × 1024, nền trắng), đầu xúc tu cuộn ra ngoài |
| 7 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\orig\N07.png` | Khẩu pháo ngắn chĩa sang phải (1024 × 1024, nền trắng): nòng vàng bên trái, vòng xanh và miệng bạc có đèn ở bên phải |
| 8 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\orig\N08.png` | Hai pháo bay nhỏ (1024 × 1024, nền trắng): một ở dưới trái chĩa sang trái, một ở trên phải chĩa sang phải |
| 9 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_2\orig\N09.png` | Nhiều bong bóng nhỏ xanh có chấm sáng rải quanh phía dưới (1024 × 1024, nền trắng) |
| 10 | `D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_2\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 mũ giáp đồng thau** (đổi dáng, viền khoảng 11 px):
- mép dưới mũ đúng chỗ mép dưới mũ cũ, rộng như cũ;
- mũ đồng thau có gờ đinh tán, kính tiềm vọng nhỏ ở đỉnh như concept; không ngọc mắt đỏ;
- không vẽ bong bóng, đầu, râu.

**N02 hai que thổi bong bóng** (đổi dáng, viền khoảng 11 px):
- gốc mỗi que đúng chỗ gốc râu cũ (ở dưới), que cong lên;
- que đồng thau dày, đầu là vòng tròn rỗng to như concept; không quả cầu;
- không vẽ mũ, đầu.

**N03 hai tai vỏ ốc** (đổi dáng, viền khoảng 9 px):
- mỗi vỏ ốc đúng chỗ cục tai cũ, cỡ gần như cũ (to hơn chút được);
- vỏ ốc xoắn trắng kem có dải nâu cam như concept;
- không vẽ bong bóng, đầu; không đèn.

**N04 bong bóng nước** (giữ viền, viền khoảng 11 px):
- giữ đúng viền, cỡ, chỗ của vòm cũ;
- viền mực mảnh, tô xanh nước rất nhạt đều; không vệt sáng, không chấm sáng;
- không vẽ đầu, mũ.

**N05 đầu có mặt** (giữ viền, viền khoảng 15 px):
- giữ viền đầu như cũ; vẽ trọn đỉnh đầu (mũ đè lên sau);
- vàng cát vòng coban; hai mắt to tròng xanh thẫm đúng chỗ mắt cũ, mày coban xếch, miệng chu, má phồng như concept;
- không vẽ bong bóng, mũ, xúc tu; không hồng, không mảng tím.

**N06 tám xúc tu** (giữ viền, viền khoảng 18 px):
- đúng số xúc tu, mỗi cái đúng chỗ, dáng, chiều cuộn như cũ;
- vàng cát, vòng coban nhỏ;
- không vẽ đầu, pháo.

**N07 pháo ống đồng** (đổi dáng, viền khoảng 21 px):
- đuôi pháo ở bên trái đúng chỗ cũ (chỗ xúc tu cầm), miệng pháo chĩa sang phải;
- ống đồng thau có vòng đinh tán, miệng loe như concept;
- không vẽ xúc tu; không đèn, không xanh.

**N08 hai pháo vỏ ốc anh vũ** (đổi dáng, viền khoảng 7 px):
- hai pháo đúng chỗ cũ, miệng chĩa ra ngoài như cũ; to hơn chút được;
- vỏ ốc anh vũ trắng kem sọc nâu cam, miệng pháo vòng đồng thau;
- không vẽ con bạch tuộc.

**N09 các chùm bong bóng** (giữ viền, viền khoảng 11 px):
- các bong bóng đúng chỗ, cỡ như cũ;
- viền mực mảnh, tô xanh nước rất nhạt; không chấm sáng;
- không thêm bong bóng.

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
