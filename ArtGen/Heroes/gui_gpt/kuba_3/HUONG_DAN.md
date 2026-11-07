# Gói gửi GPT: Kuba dạng 3/3 (Kuba Kim Cương, `kuba_3`)

Tướng boss hệ Thủy (mini boss ải 40 đảo Thủy, dạng 3/3), rig aola #96. Thiết kế: ốc mượn hồn vua kim cương: vỏ ốc vàng cát mọc tinh thể kim cương trắng xanh, tóc tảo tím dài, khăn bọt biển, khăn sọc tảo, đuôi gai. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\kuba_3\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\kuba_3\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\kuba_3\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_3\Silhouette.png` | Bóng xám của con gốc trên nền trắng (1325 × 1413): con gốc #96 (xem Rig_Numbered.png) |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_3\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (1325 × 1413, nền trắng): 1 vỏ ốc kim cương, 2 mặt, 3 tóc, 4 khăn, 5 thân, khăn sọc và chân, 6 đuôi gai, 7 giọt nước |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |
| 6 | `D:\PokiClash\ArtGen\Heroes\inbox\kuba_1\concept_duyet.png` | Concept đã duyệt của `kuba_1` (1215 × 1295, nền trắng): dạng 1 đã duyệt của dòng này |

Xong thì nhắn Claude "duyệt concept kuba_3". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\kuba_3\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\kuba_3\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\kuba_3\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi thử kuba_3".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N03, N04, N05, N06, N07.
3. Đủ ảnh thì nhắn Claude "ghép kuba_3".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_3\orig\N01.png` | vỏ ốc kim cương cũ (1024 × 1024, nền trắng) |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_3\orig\N02.png` | mặt cũ (1024 × 1024, nền trắng) |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_3\orig\N03.png` | tóc cũ (1024 × 1024, nền trắng) |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_3\orig\N04.png` | khăn cũ (1024 × 1024, nền trắng) |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_3\orig\N05.png` | thân, khăn sọc và chân cũ (1024 × 1024, nền trắng) |
| 6 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_3\orig\N06.png` | đuôi gai cũ (1024 × 1024, nền trắng) |
| 7 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_3\orig\N07.png` | giọt nước cũ (1024 × 1024, nền trắng) |
| 8 | `D:\PokiClash\ArtGen\Heroes\inbox\kuba_3\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 vỏ ốc kim cương** (đổi dáng, viền khoảng 9 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: vỏ ốc kim cương;
- không vẽ phần khác.

**N02 mặt** (giữ viền, viền khoảng 19 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: mặt;
- không vẽ phần khác.

**N03 tóc** (đổi dáng, viền khoảng 14 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: tóc;
- không vẽ phần khác.

**N04 khăn** (giữ viền, viền khoảng 12 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: khăn;
- không vẽ phần khác.

**N05 thân, khăn sọc và chân** (giữ viền, viền khoảng 12 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: thân, khăn sọc và chân;
- không vẽ phần khác.

**N06 đuôi gai** (giữ viền, viền khoảng 17 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: đuôi gai;
- không vẽ phần khác.

**N07 giọt nước** (giữ viền, viền khoảng 15 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: giọt nước;
- không vẽ phần khác.

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
