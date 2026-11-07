# Gói gửi GPT: Kuba dạng 2/3 (Kuba Vỏ Cứng, `kuba_2`)

Tướng boss hệ Thủy (mini boss ải 40 đảo Thủy, dạng 2/3), rig aola #95. Thiết kế: ốc mượn hồn chiến binh: vỏ ốc xoắn vàng cát gai cứng trên lưng, càng phải to cam đỏ, tóc tảo tím, đuôi gai. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\kuba_2\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\kuba_2\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\kuba_2\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\Silhouette.png` | Bóng xám của con gốc trên nền trắng (956 × 982): con gốc #95 (xem Rig_Numbered.png) |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (956 × 982, nền trắng): 1 vỏ ốc gai, 2 đầu có mặt, 3 tóc, 4 khăn, 5 càng to, 6 thân và chân, 7 đuôi gai, 8 bụi nước |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |
| 6 | `D:\PokiClash\ArtGen\Heroes\inbox\kuba_1\concept_duyet.png` | Concept đã duyệt của `kuba_1` (1215 × 1295, nền trắng): dạng 1 đã duyệt của dòng này |

Xong thì nhắn Claude "duyệt concept kuba_2". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\kuba_2\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\kuba_2\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\kuba_2\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi thử kuba_2".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N03, N04, N05, N06, N07, N08.
3. Đủ ảnh thì nhắn Claude "ghép kuba_2".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\orig\N01.png` | vỏ ốc gai cũ (1024 × 1024, nền trắng) |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\orig\N02.png` | đầu có mặt cũ (1024 × 1024, nền trắng) |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\orig\N03.png` | tóc cũ (1024 × 1024, nền trắng) |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\orig\N04.png` | khăn cũ (1024 × 1024, nền trắng) |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\orig\N05.png` | càng to cũ (1024 × 1024, nền trắng) |
| 6 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\orig\N06.png` | thân và chân cũ (1024 × 1024, nền trắng) |
| 7 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\orig\N07.png` | đuôi gai cũ (1024 × 1024, nền trắng) |
| 8 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\kuba_2\orig\N08.png` | bụi nước cũ (1024 × 1024, nền trắng) |
| 9 | `D:\PokiClash\ArtGen\Heroes\inbox\kuba_2\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 vỏ ốc gai** (đổi dáng, viền khoảng 10 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: vỏ ốc gai;
- không vẽ phần khác.

**N02 đầu có mặt** (giữ viền, viền khoảng 12 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: đầu có mặt;
- không vẽ phần khác.

**N03 tóc** (đổi dáng, viền khoảng 9 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: tóc;
- không vẽ phần khác.

**N04 khăn** (giữ viền, viền khoảng 13 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: khăn;
- không vẽ phần khác.

**N05 càng to** (đổi dáng, viền khoảng 15 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: càng to;
- không vẽ phần khác.

**N06 thân và chân** (giữ viền, viền khoảng 15 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: thân và chân;
- không vẽ phần khác.

**N07 đuôi gai** (giữ viền, viền khoảng 13 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: đuôi gai;
- không vẽ phần khác.

**N08 bụi nước** (giữ viền, viền khoảng 8 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: bụi nước;
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
