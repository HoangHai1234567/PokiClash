# Gói gửi GPT: Tám Tay dạng 1/2 (Tám Tay Bong Bóng, `tam_tay_1`)

Tướng Khá hệ Thủy (quái thường đảo Thủy), dạng 1/2, rig aola #1053. Thiết kế: bạch tuộc con màu vàng cát có vòng xanh coban (kiểu bạch tuộc đốm xanh), đầu tròn to trong bong bóng nước trong suốt chỉ có viền; mũ nồi pháo thủ đỏ thẫm huy hiệu mỏ neo vàng, hai que thổi bong bóng cong thay râu ăng-ten; mắt to tròng xanh thẫm, mày coban xếch, miệng chu sẵn sàng phụt bong bóng; năm xúc tu xoăn; ba bong bóng vẽ tay chỉ có viền. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\tam_tay_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (618 × 775): con gốc #1053 là bạch tuộc con lơ lửng, nhìn thẳng: đầu tròn rất to màu hồng đỏ nằm trong vòm kính tròn trong suốt có vệt sáng, trên vòm đội mũ lưỡi trai xanh có huy hiệu, hai râu ăng-ten mảnh đầu tròn; năm xúc tu ngắn xoăn dưới đầu; ba bong bóng bay phía dưới. Bỏ khỏi bóng xám: bóng dưới chân |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (618 × 775, nền trắng): 1 mũ có hai râu ăng-ten, 2 vòm bong bóng (lòng sau đầu và vành trước), 3 đầu có hai mắt và miệng, 4 năm xúc tu, 5 ba bong bóng |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept tam_tay_1". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\tam_tay_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N03. Gõ `next`: GPT vẽ N01. Nhắn Claude "soi thử tam_tay_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N02, N04, N05.
3. Đủ ảnh thì nhắn Claude "ghép tam_tay_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_1\orig\N01.png` | Mũ lưỡi trai xanh có huy hiệu vàng đỏ (1024 × 1024, nền trắng), hai râu ăng-ten mảnh đầu tròn xanh mọc từ hai bên mũ |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_1\orig\N02.png` | Vòm kính tròn to xanh nhạt có vệt sáng trắng (1024 × 1024, nền trắng): lòng vòm và vành ngoài; đầu không có trong ảnh |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_1\orig\N03.png` | Đầu bạch tuộc tròn to hồng đỏ có mảng tím trên đỉnh (1024 × 1024, nền trắng), hai mắt xanh to, miệng tròn nhỏ, nhìn thẳng |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_1\orig\N04.png` | Năm xúc tu ngắn đỏ sẫm có mảng tím (1024 × 1024, nền trắng), buông cạnh nhau, đầu xúc tu cuộn ra ngoài |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\tam_tay_1\orig\N05.png` | Ba bong bóng tròn xanh có chấm sáng (1024 × 1024, nền trắng): to bên trái, vừa ở giữa, nhỏ bên phải |
| 6 | `D:\PokiClash\ArtGen\Heroes\inbox\tam_tay_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 mũ nồi và hai que thổi bong bóng** (đổi dáng, viền khoảng 9 px):
- mũ nồi đỏ thẫm đội hơi lệch, huy hiệu mỏ neo vàng ở trước; mép dưới mũ đúng chỗ mép dưới mũ cũ;
- hai que thổi bong bóng vàng đồng mọc từ hai bên mũ, cong ra ngoài, đầu là vòng tròn rỗng (không phải quả cầu);
- không vẽ bong bóng, đầu; không lưỡi trai.

**N02 bong bóng nước bọc đầu** (giữ viền, viền khoảng 9 px):
- giữ đúng viền, cỡ, chỗ của vòm cũ;
- chỉ viền mực mảnh và tô xanh nước rất nhạt đều khắp lòng; không vệt sáng, không phản chiếu, không chấm sáng;
- không vẽ đầu, mặt, mũ.

**N03 đầu có mặt** (giữ viền, viền khoảng 12 px):
- giữ viền đầu như cũ; vẽ trọn cả đỉnh đầu (mũ đè lên sau);
- vàng cát với các vòng xanh coban (giữa vòng vẫn vàng cát); hai mắt to tròng xanh thẫm, mỗi mắt một chấm sáng, đúng chỗ hai mắt cũ;
- mày coban xếch xuống phía giữa, miệng chu, má hơi phồng như concept;
- không vẽ bong bóng, mũ, xúc tu; không hồng, không mảng tím.

**N04 năm xúc tu** (giữ viền, viền khoảng 17 px):
- đúng năm xúc tu, mỗi cái đúng chỗ, dáng, chiều cuộn như cũ; đầu trên là chỗ nối dưới đầu, đầu cuộn ở dưới;
- vàng cát, vài vòng xanh coban nhỏ;
- không vẽ đầu, bong bóng; không thêm xúc tu.

**N05 ba bong bóng** (giữ viền, viền khoảng 20 px):
- ba bong bóng đúng chỗ và cỡ như cũ;
- viền mực mảnh, tô xanh nước rất nhạt; không chấm sáng, không vệt sáng;
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
