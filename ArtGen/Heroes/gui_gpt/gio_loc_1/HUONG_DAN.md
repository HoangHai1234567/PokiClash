# Gói gửi GPT: Gió Lốc dạng 1/3 (Gió Con, `gio_loc_1`)

Tướng hệ Mộc (ải 30 đảo Mộc, dạng 1/3), rig aola #850. Thiết kế: rồng chuồn chuồn con: thân thon xanh ngọc lam bụng kem, cánh chuồn chuồn bạc hà nhạt gân xanh thẫm, hai râu lông vũ thay gạc, vòng gió trắng trên đầu, ngọc gió trắng xanh xoáy trước bụng, chóp đuôi chuồn chuồn, khăn gió bạc hà. Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\gio_loc_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (577 × 556): con gốc #850 (xem Rig_Numbered.png) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (577 × 556, nền trắng): 1 đầu có mặt, 2 hai râu lông vũ, 3 vây tai và mào đầu, 4 vòng gió trắng, 5 thân và khăn gió, 6 ngọc gió xoáy, 7 hai cánh chuồn chuồn, 8 hai chân, 9 đuôi chóp chuồn chuồn |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept gio_loc_1". Duyệt xong Claude lưu `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\gio_loc_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi thử gio_loc_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N03, N04, N05, N06, N07, N08, N09.
3. Đủ ảnh thì nhắn Claude "ghép gio_loc_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\orig\N01.png` | đầu có mặt cũ (1024 × 1024, nền trắng) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\orig\N02.png` | hai râu lông vũ cũ (1024 × 1024, nền trắng) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\orig\N03.png` | vây tai và mào đầu cũ (1024 × 1024, nền trắng) |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\orig\N04.png` | vòng gió trắng cũ (1024 × 1024, nền trắng) |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\orig\N05.png` | thân và khăn gió cũ (1024 × 1024, nền trắng) |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\orig\N06.png` | ngọc gió xoáy cũ (1024 × 1024, nền trắng) |
| 7 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\orig\N07.png` | hai cánh chuồn chuồn cũ (1024 × 1024, nền trắng) |
| 8 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\orig\N08.png` | hai chân cũ (1024 × 1024, nền trắng) |
| 9 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_1\orig\N09.png` | đuôi chóp chuồn chuồn cũ (1024 × 1024, nền trắng) |
| 10 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 đầu có mặt** (giữ viền, viền khoảng 15 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: đầu có mặt;
- không vẽ phần khác.

**N02 hai râu lông vũ** (đổi dáng, viền khoảng 16 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: hai râu lông vũ;
- không vẽ phần khác.

**N03 vây tai và mào đầu** (đổi dáng, viền khoảng 13 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: vây tai và mào đầu;
- không vẽ phần khác.

**N04 vòng gió trắng** (đổi dáng, viền khoảng 20 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: vòng gió trắng;
- không vẽ phần khác.

**N05 thân và khăn gió** (giữ viền, viền khoảng 19 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: thân và khăn gió;
- không vẽ phần khác.

**N06 ngọc gió xoáy** (đổi dáng, viền khoảng 25 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: ngọc gió xoáy;
- không vẽ phần khác.

**N07 hai cánh chuồn chuồn** (đổi dáng, viền khoảng 7 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: hai cánh chuồn chuồn;
- không vẽ phần khác.

**N08 hai chân** (giữ viền, viền khoảng 18 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: hai chân;
- không vẽ phần khác.

**N09 đuôi chóp chuồn chuồn** (đổi dáng, viền khoảng 16 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: đuôi chóp chuồn chuồn;
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

Gói này sinh từ `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\build.py`; sửa prompt ở đó rồi chạy lại.
