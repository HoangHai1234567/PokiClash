# Gói gửi GPT: Phong Linh dạng 1/2 (Tiểu Phong Linh, `phong_linh_1`)

Tướng hệ Mộc (ải 20 đảo Mộc, dạng 1/2), rig aola #943. Thiết kế: cú mèo nhỏ lông xanh xô thơm pha kem: mặt nạ lông trắng kem có hai mắt hổ phách to, mỏ nâu ô liu, hai túm tai là lá; hai cánh như tay, đầu cánh xòe như ngón nắm, cạnh mỗi đầu cánh lơ lửng một chong chóng hạt phong (thay hoa cam); thân phủ lông như áo lá. Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\phong_linh_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\phong_linh_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\phong_linh_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\phong_linh_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (530 × 575): con gốc #943 (xem Rig_Numbered.png) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\phong_linh_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (530 × 575, nền trắng): 1 đầu cú có mặt, 2 hai túm tai lá, 3 thân lông áo lá, 4 hai cánh như tay, 5 hai chong chóng hạt phong |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept phong_linh_1". Duyệt xong Claude lưu `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\phong_linh_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\phong_linh_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\phong_linh_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi thử phong_linh_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N03, N04, N05.
3. Đủ ảnh thì nhắn Claude "ghép phong_linh_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\phong_linh_1\orig\N01.png` | đầu cú có mặt cũ (1024 × 1024, nền trắng) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\phong_linh_1\orig\N02.png` | hai túm tai lá cũ (1024 × 1024, nền trắng) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\phong_linh_1\orig\N03.png` | thân lông áo lá cũ (1024 × 1024, nền trắng) |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\phong_linh_1\orig\N04.png` | hai cánh như tay cũ (1024 × 1024, nền trắng) |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\phong_linh_1\orig\N05.png` | hai chong chóng hạt phong cũ (1024 × 1024, nền trắng) |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\phong_linh_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 đầu cú có mặt** (đổi dáng, viền khoảng 12 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: đầu cú có mặt;
- không vẽ phần khác.

**N02 hai túm tai lá** (đổi dáng, viền khoảng 9 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: hai túm tai lá;
- không vẽ phần khác.

**N03 thân lông áo lá** (giữ viền, viền khoảng 14 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: thân lông áo lá;
- không vẽ phần khác.

**N04 hai cánh như tay** (giữ viền, viền khoảng 14 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: hai cánh như tay;
- không vẽ phần khác.

**N05 hai chong chóng hạt phong** (đổi dáng, viền khoảng 8 px):
- đúng chỗ, cỡ như mảnh cũ;
- như concept: hai chong chóng hạt phong;
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
