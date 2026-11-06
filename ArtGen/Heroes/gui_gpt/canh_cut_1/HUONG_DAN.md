# Gói gửi GPT: Cánh Cụt dạng 1/2 (Cánh Cụt Con, `canh_cut_1`)

Tướng Thường hệ Thủy (ải 10 đảo Thủy), dạng 1/2, rig aola #1691. Thiết kế: cánh cụt con tập sự bếp kiểu cánh cụt mào: đầu, lưng và mặt xanh thẫm, bụng trắng lên tới dưới mỏ, mắt to lòng trắng, mày lông vàng xếch xuống phía mỏ, chóp lông nhọn ở hai bên; mào lông nhọn xanh thẫm trên đỉnh; mỏ cam đỏ cười nhếch; khăn bếp xanh trời viền trắng thắt nút bên trái; hai vây ôm chảo gang nhỏ giơ như chùy (mép chảo đóng sương trắng, băng nhũ nhỏ, cán gỗ quấn dây xanh trời, vòng treo tròn); đuôi nhọn xanh thẫm; chân màng hồng nhạt; mặt quả quyết. Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\canh_cut_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\canh_cut_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\canh_cut_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\canh_cut_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (543 × 482): con gốc #1691 là chim cánh cụt con mập nhìn thẳng hơi quay phải: đầu liền thân thành một khối tròn, chỏm lông hai thùy trên đỉnh, mỏ hơi lệch phải, khăn vắt ngang ngực thắt nút bên trái hai vạt bay sang trái, hai vây ngắn ôm con cá băng dựng đứng trước bụng (đầu cá trên phải, đuôi cá tròn ở dưới), đuôi nhọn lộ sau thân ở dưới trái, hai bàn chân màng phẳng. Bỏ khỏi bóng xám: bóng dưới chân và vòng băng có sao băng |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\canh_cut_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (543 × 482, nền trắng): 1 chỏm lông, 2 đầu liền thân và mặt, 3 mỏ, 4 dải khăn, 5 hai vạt nút khăn, 6 con cá cầm tay (thành chảo), 7 vây trái, 8 vây phải, 9 đuôi, 10 hai bàn chân |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept canh_cut_1". Duyệt xong Claude lưu `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\canh_cut_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\canh_cut_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\canh_cut_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N02. Gõ `next`: GPT vẽ N04. Nhắn Claude "soi thử canh_cut_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N01, N03, N05, N06.
3. Đủ ảnh thì nhắn Claude "ghép canh_cut_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\canh_cut_1\orig\N01.png` | Chỏm lông xanh hai thùy (1024 × 1024, nền trắng): thùy trái to, thùy phải nhỏ; mép dưới phẳng là chỗ cắm vào đỉnh đầu |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\canh_cut_1\orig\N02.png` | Khối tròn xanh là đầu liền thân (1024 × 1024, nền trắng): mặt trắng, hai mắt đen, má hồng, mỏ vàng hơi lệch phải; bụng nâu nhạt và trắng; mép dưới phẳng là đáy thân |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\canh_cut_1\orig\N03.png` | Khăn đỏ (1024 × 1024, nền trắng): dải khăn cong lõm xuống vắt ngang ngực, nút ở đầu trái với hai vạt bay sang trái (vạt trên chĩa lên trái, vạt dưới chĩa trái); đầu phải nhọn cong lên |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\canh_cut_1\orig\N04.png` | Con cá băng xanh nhạt dựng đứng (1024 × 1024, nền trắng): đầu cá rộng hình bầu dục ở trên bên phải, thân cong xuống trái, đuôi tròn ở dưới |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\canh_cut_1\orig\N05.png` | Hai vây xanh ngắn (1024 × 1024, nền trắng): vây trái to bè, gốc ở đầu trái, chóp tròn ở bên phải; vây phải nhỏ hơn, gốc ở bên phải, chóp ở bên trái; khoảng trống giữa là chỗ cán chảo |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\canh_cut_1\orig\N06.png` | Đuôi xanh nhọn ở trên trái (chóp hẹp ở trên, đầu rộng ở dưới phải là chỗ giấu sau thân) và hai bàn chân màng cam phẳng ở dưới: chân trái dưới đuôi, chân phải ở bên phải |
| 7 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\canh_cut_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 mào lông** (đổi dáng, viền khoảng 17 px):
- mép dưới (chỗ cắm vào đầu) đúng chỗ mép dưới cũ, rộng như cũ;
- ba bốn lông xanh thẫm nhọn dựng lên như concept, cao hơn chỏm cũ một chút được;
- không vẽ đầu, không chỏm tròn hai thùy, không lông vàng.

**N02 đầu liền thân, mặt, mỏ** (giữ viền, viền khoảng 8 px):
- giữ viền ngoài khối tròn như cũ (đỉnh, hai bên, đáy phẳng);
- đầu, lưng, hai bên và mặt xanh thẫm; bụng trắng lên tới ngay dưới mỏ;
- hai mắt to (lòng trắng, con ngươi đen, một chấm sáng nhỏ) đúng chỗ mắt cũ; mày lông vàng xếch xuống phía mỏ, chóp lông nhọn ở hai bên nằm trong viền;
- mỏ cam đỏ ngắn đúng chỗ mỏ cũ, cười nhếch tự tin; không má hồng;
- không vẽ khăn, mào, vây, chảo, chân.

**N03 khăn bếp** (đổi dáng, viền khoảng 6 px):
- dải khăn đi đúng đường cong cũ, hai đầu dải đúng chỗ cũ;
- nút ở đầu trái, hai vạt bay sang trái đúng hướng cũ, cỡ như cũ;
- khăn xanh trời viền trắng mảnh như concept; không khăn đỏ;
- không vẽ thân, đầu.

**N04 chảo gang** (đổi dáng, viền khoảng 14 px):
- mặt chảo tròn ở chỗ đầu cá (trên phải), cán cong xuống trái tới vòng treo tròn ở chỗ đuôi cá (dưới); cỡ như cá cũ;
- chảo gang đen, lòng chảo quay ra người xem, mép đóng sương trắng và băng nhũ nhỏ; cán gỗ nhạt quấn dây xanh trời;
- không vẽ vây (nhóm N05), không vẽ cá, không hơi nóng.

**N05 hai vây** (giữ viền, viền khoảng 10 px):
- viền và chỗ hai vây như cũ;
- vây xanh thẫm, mặt dưới xanh nhạt hơn; chóp hai vây khép về phía khoảng trống (chỗ cán chảo);
- không vẽ chảo, thân, ngón tay, móng.

**N06 đuôi và hai bàn chân** (giữ viền, viền khoảng 8 px):
- đuôi và hai bàn chân đúng chỗ, đúng cỡ, đúng hướng cũ;
- đuôi xanh thẫm, chóp nhọn ở trên trái; hai bàn chân màng hồng nhạt;
- không vẽ thân, không vẽ chân dài.

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
