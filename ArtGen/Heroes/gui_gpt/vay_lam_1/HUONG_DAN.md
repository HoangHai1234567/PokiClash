# Gói gửi GPT: Vây Lam dạng 1/3 (Cá Đốm, `vay_lam_1`)

Tướng boss hệ Thủy (mini boss ải 30 đảo Thủy, dạng 1/3), rig aola #546. Thiết kế: cá mập con tròn vo cuộn trong quả trứng bong bóng nước (chỉ viền), lưng xanh coban đốm trắng, bụng trắng, vây viền vàng nghệ, mắt hổ phách. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\vay_lam_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\vay_lam_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\vay_lam_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\vay_lam_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (493 × 544): con gốc #546 (xem Rig_Numbered.png) |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\vay_lam_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (493 × 544, nền trắng): 1 quả trứng bong bóng, 2 cá mập con có mặt, 3 hai bong bóng nhỏ |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept vay_lam_1". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\vay_lam_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\vay_lam_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\vay_lam_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi thử vay_lam_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N03.
3. Đủ ảnh thì nhắn Claude "ghép vay_lam_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\vay_lam_1\orig\N01.png` | quả trứng bong bóng cũ (1024 × 1024, nền trắng) |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\vay_lam_1\orig\N02.png` | cá mập con có mặt cũ (1024 × 1024, nền trắng) |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\vay_lam_1\orig\N03.png` | hai bong bóng nhỏ cũ (1024 × 1024, nền trắng) |
| 4 | `D:\PokiClash\ArtGen\Heroes\inbox\vay_lam_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 quả trứng bong bóng** (giữ viền, viền khoảng 8 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: quả trứng bong bóng;
- không vẽ phần khác.

**N02 cá mập con có mặt** (giữ viền, viền khoảng 9 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: cá mập con có mặt;
- không vẽ phần khác.

**N03 hai bong bóng nhỏ** (giữ viền, viền khoảng 7 px):
- đúng chỗ, cỡ như mảnh cũ, giữ viền;
- như concept: hai bong bóng nhỏ;
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
