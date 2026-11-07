# Gói gửi GPT: Gió Lốc dạng 3/3 (Gió Lốc, `gio_loc_3`)

Tướng hệ Mộc (ải 30 đảo Mộc, dạng 3/3), rig aola #852. Thiết kế: như dạng 2, thân dựng chữ S trên đuôi cuộn, cánh chuồn chuồn rất to viền xanh thẫm, thêm hàng gai lưng trắng; râu lông vũ cao, vòng gió trắng, ngọc gió xoáy, chóp đuôi chuồn chuồn, vây gió ở cổ, dải vây ở hông. Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_3\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\gio_loc_3\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_3\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_3\Silhouette.png` | Bóng xám của con gốc trên nền trắng (1200 × 1147): con gốc #852 (xem Rig_Numbered.png) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_3\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (1200 × 1147, nền trắng): 1 đầu có mặt, 2 hai râu lông vũ, 3 vây tai và mào đầu, 4 vòng gió trắng, 5 thân gai lưng và vây cổ, 6 ngọc gió xoáy, 7 hai cánh chuồn chuồn rất to, 8 hai chân, 9 đuôi chóp chuồn chuồn, 10 hai dải vây hông |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_1\concept_duyet.png` | Concept đã duyệt của `gio_loc_1` (1278 × 1231, nền trắng): dạng 1 đã duyệt của dòng này |

Xong thì nhắn Claude "duyệt concept gio_loc_3". Duyệt xong Claude lưu `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_3\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\gio_loc_3\luot_2_nhom_manh.txt`: **chưa có**. Claude viết prompt từng nhóm và dựng file này khi đã duyệt concept (cần `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\gio_loc_3\concept_duyet.png`). Ảnh gốc từng nhóm (GPT vẽ đè lên) đã có ở `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\moc\gio_loc_3\orig`.

## Concept sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Không giống vẽ tay trên giấy, không thấy nét chì sáp | `Draw it by hand on paper: dark-brown ink-pen outlines, every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |
| Có mảng sáng tối, điểm sáng trắng, bóng loáng, chuyển sắc | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine (only a small catchlight dot in each eye), no glow, no gradients.` |
| Có bóng đổ, bóng dưới chân, bóng in xuống nền | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine (only a small catchlight dot in each eye), no glow, no gradients.` |
| Nét nguệch ngoạc, quá thô | `Hand-drawn but clean and appealing, like a professional storybook illustrator; not a crude scribble.` |
| Có viền trắng quanh hình | `No white border or sticker outline; the game adds it.` |
| Mặt vui tươi, cười toe | `Make the face battle-ready: brows angled down, a small confident smile; not a big happy grin.` |
| Vẽ thêm chân, đuôi, cánh không có trong rig | `Only the parts listed under KEEP FROM THE RIG: no extra legs, tails or wings.` |
| Sai dáng rig (tay, đinh ba, vây lệch chỗ) | `Keep the pose and the parts of image 1 exactly: every part where image 2 puts it, pointing the same way.` |
| Có cảnh nền, chữ, khung | `Plain pure white background: no scenery, no text, no frame.` |

Gói này sinh từ `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\build.py`; sửa prompt ở đó rồi chạy lại.
