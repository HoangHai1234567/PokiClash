# Gói gửi GPT: Giọt Sương dạng 3/3 (Sương Long, `giot_suong_3`)

Tướng khởi đầu hệ Thủy, dạng 3/3, rig aola #9. Thiết kế: rồng nước hiệp sĩ: rồng bốn chân bằng nước trong, nhìn nghiêng quay phải, đội mũ giáp bạc như dạng 1 (vành ngắn, hình thoi vàng trên trán), mào sáu vây nước viền bạc (cánh mũ dạng 1 lớn thành mào rồng), giáp cổ vảy bạc có huy hiệu giọt nước vàng, giáp ngực bạc, giáp ống chân bạc, móng ngắn, đuôi dài cuối đuôi là hai vây hình lưỡi kiếm (kiếm tập sự thành lưỡi đuôi); mặt quả quyết, oai mà vẫn dễ thương. Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_3\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\giot_suong_3\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_3\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\Silhouette.png` | Bóng xám của con gốc trên nền trắng (1160 × 1103): con gốc #9 bốn chân nhìn nghiêng, quay sang phải, ngồi thẳng: cổ dài vươn lên, đầu ở trên bên phải mõm chĩa phải, sáu vây mào trên đầu (bốn vây dài quét ra sau lên trái, hai vây nhỏ chĩa thẳng lên), chuỗi hạt và vỏ sò chéo trên ngực, hai chân trước thẳng xuống đất (chân gần to, chân xa sau nó), một chân sau, đuôi dài quét xuống trái sát đất có hai vây ở cuối |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (1160 × 1103, nền trắng): 1 vây mào, 2 đầu, 3 cổ và thân, 4 chuỗi hạt và vỏ sò, 5 chân trước gần, 6 chân trước xa, 7 chân sau, 8 mẩu nhỏ ở bàn chân trước gần, 9 đuôi |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_1\concept_duyet.png` | Concept đã duyệt của `giot_suong_1` (1143 × 1376, nền trắng): dạng 1, tinh linh nước hiệp sĩ tập sự đội mũ giáp tròn có hai cánh nhỏ và chùm lông mũ giọt nước, giáp ngực bạc, găng bạc, cầm kiếm ngắn chắn tay vàng, đuôi nước cuộn. Giữ màu, mũ, mặt, giáp, nét vẽ |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_2\concept_duyet.png` | Concept đã duyệt của `giot_suong_2` (950 × 1656, nền trắng): dạng 2, hiệp sĩ nước lơ lửng: mũ giáp tròn mỗi bên hai lông cánh bạc, chùm lông mũ nước xanh đậm trên đế vàng, giáp cổ bạc có giọt nước vàng, giáp ngực viền vàng, áo choàng nước che tay trái, kiếm chắn tay hình hai cánh vàng, hai chân nhọn bọc giáp, đuôi nước chữ S vây chẻ đôi. Giữ màu, mũ, mặt, giáp cổ, nét vẽ |

Xong thì nhắn Claude "duyệt concept giot_suong_3". Duyệt xong Claude lưu `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_3\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\giot_suong_3\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_3\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N02. Gõ `next`: GPT vẽ N05. Nhắn Claude "soi thử giot_suong_3".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N01, N03, N04, N06, N07, N08.
3. Đủ ảnh thì nhắn Claude "ghép giot_suong_3".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\orig\N01.png` | Sáu vây rời (1024 × 1024, nền trắng): bên trái bốn vây dài thành hai cặp quét lên trái, gốc ở đầu dưới bên phải; bên phải hai vây nhỏ chĩa thẳng lên, gốc ở đầu dưới; khoảng trống giữa là chỗ của đầu |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\orig\N02.png` | Đầu nhìn nghiêng quay phải (1024 × 1024, nền trắng): mũ trùm xanh đậm trên đỉnh và sau đầu, mắt hẹp trắng, mặt dưới xanh nhạt, chóp mõm ở bên phải; mép dưới trái nối cổ (cổ là mảnh khác vẽ đè lên mép đó) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\orig\N03.png` | Cổ và thân nhìn nghiêng quay phải (1024 × 1024, nền trắng): đầu hẹp trên phải là đỉnh cổ (đè lên đáy đầu), ngực bên phải, lưng dốc xuống trái tới chỗ nối đuôi, bụng ở dưới; trước xanh nhạt, lưng xanh đậm |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\orig\N04.png` | Chuỗi hạt trên ngực (1024 × 1024, nền trắng): hàng hạt tròn từ trên trái chạy xuống phải, cuối là vỏ sò to ở dưới phải; vẽ đè lên cổ, thân và chân trước gần |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\orig\N05.png` | Chân trước gần, cao (1024 × 1024, nền trắng): đầu trên tròn là vai (ngay dưới chuỗi hạt), chạy thẳng xuống, cuối có vòng xanh chanh và ba móng đỏ |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\orig\N06.png` | Chân trước xa (1024 × 1024, nền trắng): đầu trên hẹp khuất sau ngực, chạy thẳng xuống, cuối có vòng xanh chanh và móng đỏ |
| 7 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\orig\N07.png` | Hai chân sau (1024 × 1024, nền trắng): chân gần bên trái xanh đậm, hông ở trên, bàn chân nhọn ở dưới; chân xa bên phải là tấm hẹp xanh đậm, gần như khuất |
| 8 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_3\orig\N08.png` | Đuôi (1024 × 1024, nền trắng): đầu dày trên phải nối lưng, quét xuống trái, cuối là hai vây (trên, dưới) chĩa trái có chóp cam đỏ |
| 9 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_3\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 sáu vây mào** (đổi dáng, viền khoảng 20 px):
- đủ sáu vây, mỗi vây đúng chỗ, đúng hướng, gốc ở đúng chỗ gốc cũ;
- vây nước xanh viền bạc như concept; không vẽ đầu, mũ; không sọc cam đỏ.

**N02 đầu, mặt và mũ** (đổi dáng, viền khoảng 22 px):
- chóp mõm, đỉnh đầu, mép dưới trái (chỗ nối cổ) đúng chỗ cũ; cỡ như cũ;
- mũ bạc vành ngắn, hình thoi vàng trên trán; một mắt tròn to quả quyết dưới vành; miệng cười tự tin khép, lộ một nanh nhỏ;
- không mặt nạ đậm, không mắt hẹp; không vẽ vây mào, cổ, thân.

**N03 cổ và thân** (giữ viền, viền khoảng 14 px):
- giữ viền ngoài: đỉnh cổ trên phải, lưng dốc xuống trái, bụng ở dưới;
- nước xanh trong, họng, ngực và bụng xanh nhạt, lưng xanh đậm có vài vệt sóng như concept;
- không vẽ đầu, giáp cổ, giáp ngực, chân, đuôi.

**N04 giáp cổ và huy hiệu** (đổi dáng, viền khoảng 31 px):
- hàng vảy bạc tròn có đinh vàng nhỏ đi đúng đường hàng hạt cũ;
- huy hiệu giọt nước vàng đúng chỗ vỏ sò, cỡ gần bằng vỏ sò;
- không vẽ giáp ngực (nằm ở nhóm N05), cổ, thân; không hạt, không vỏ sò.

**N05 chân trước gần và giáp ngực** (giữ viền, viền khoảng 11 px):
- giữ viền ngoài; vai ở **đầu trên**, bàn chân ở **đầu dưới**;
- phần trên (ngay dưới chuỗi hạt) phủ giáp ngực bạc, mép dưới viền vàng như ngực trong concept;
- giáp ống chân bạc viền vàng ở chỗ vòng xanh chanh cũ; ba móng ngắn màu kem ở chỗ ba móng đỏ.

**N06 chân trước xa** (giữ viền, viền khoảng 17 px):
- giữ viền ngoài; đầu trên là vai, bàn chân ở **đầu dưới**;
- nước xanh, giáp ống chân bạc viền vàng ở chỗ vòng xanh chanh, móng ngắn màu kem ở chỗ móng đỏ.

**N07 hai chân sau** (giữ viền, viền khoảng 24 px):
- giữ viền cả hai chân; hông ở **đầu trên**, bàn chân ở **đầu dưới**;
- chân gần nước xanh đậm, giáp gối hoặc ống chân bạc viền vàng, móng ngắn màu kem ở đầu dưới; chân xa xanh đậm trơn.

**N08 đuôi lưỡi kiếm** (đổi dáng, viền khoảng 12 px):
- đầu nối thân (đầu dày trên phải) đúng chỗ cũ; hai vây cuối đúng chỗ hai vây cũ, chĩa trái;
- đuôi nước xanh có vệt sóng đậm; hai vây hình lưỡi kiếm viền bạc như concept; không chóp cam đỏ.

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Nét số bóng loáng, chuyển sắc | `Render it hand-drawn like the map: dark-brown ink outlines, flat warm colours with coloured-pencil hatching; no glossy shine, no gradients.` |
| Nét nguệch ngoạc, quá thô | `Hand-drawn but clean and appealing, like a professional storybook illustrator; not a crude scribble.` |
| Có viền trắng quanh hình | `No white border or sticker outline; the game adds it.` |
| Mặt vui tươi, cười toe | `Make the face battle-ready: brows angled down, a small confident smile with a tiny fang; not a big happy grin.` |
| Vẽ cả con hoặc thêm phần ngoài nhóm | `Only the pieces of image 1, nothing else.` |
| Mảnh lệch chỗ, xoay, đổi cỡ | `Put every piece back exactly where it is in image 1: same position, size and angle on the same 1024 x 1024 canvas.` |
| Bàn tay, bàn chân ở sai đầu | `The hand/foot is at the BOTTOM end; the TOP end is the shoulder/hip.` |
| Viền mảnh quá mảnh hoặc quá dày | `Make the dark-brown outline about <N> px thick, the same on every edge.` (N ghi ở từng nhóm trên) |
| Có bóng đổ, bóng dưới chân, bóng in xuống nền | `NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the feet or on the ground or background. Shade only with colour-pencil hatching inside the shapes; the game adds shadows itself where needed.` |
| Nền xám, có ô lưới | `Plain pure white background, nothing else.` |

Gói này sinh từ `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\build.py`; sửa prompt ở đó rồi chạy lại.
