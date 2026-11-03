# Gói gửi GPT: Giọt Sương dạng 1/3 (Giọt Nước, `giot_suong_1`)

Tướng khởi đầu hệ Thủy, dạng 1/3, rig aola #7. Thiết kế: tinh linh nước hiệp sĩ tập sự: đầu tròn bằng nước đội mũ giáp tròn kiểu cute có đôi cánh nhỏ hai bên và chùm lông mũ hình giọt nước, giáp ngực bạc trơn, không họa tiết, tay phải nắm thanh kiếm ngắn hơi to so với người, găng giáp bạc bọc nắm tay, đuôi nước cuộn, chân đi ủng bạc; mặt quả quyết, cười tự tin. Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\giot_suong_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (779 × 937): con gốc #7 đứng hai chân, chéo 3/4: đầu to, hai vây tai hai bên đầu chĩa lên, chóp giọt nước trên đỉnh cong sang trái, thân nhỏ, hai tay buông (mỗi tay 2 mảnh: bắp tay, cẳng tay liền bàn tay), hai chân, đuôi nhỏ ở dưới trái cong lên |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (779 × 937, nền trắng): 1 vây tai, 2 đầu, 3 chóp, 4 thân, 5 vỏ sò ở ngực, 6 tay trái, 7 tay phải, 8 đuôi, 9 và 10 hai chân |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |

Xong thì nhắn Claude "duyệt concept giot_suong_1". Duyệt xong Claude lưu `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\giot_suong_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N02. Gõ `next`: GPT vẽ N06. Nhắn Claude "soi thử giot_suong_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N01, N03, N04, N05, N07, N08, N09.
3. Đủ ảnh thì nhắn Claude "ghép giot_suong_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\orig\N01.png` | hai vây tai hình sừng xanh nhạt, chóp có sọc cam và xanh lá; vây trái chĩa lên trái, gốc ở đầu dưới bên phải; vây phải chĩa lên, gốc ở đầu dưới bên trái; khoảng trống giữa là chỗ của đầu |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\orig\N02.png` | đầu tròn xanh bóng như giọt nước giữa ảnh; hai mắt to ở nửa dưới, má hồng nhạt, miệng nhỏ, vòng lưỡi liềm xanh chanh gần đỉnh |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\orig\N03.png` | chóp giọt nước xanh trong phóng to khoảng 4 lần, mép dưới tròn (chỗ cắm vào đầu), chóp nhọn cong lên phía trên bên trái |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\orig\N04.png` | thân xanh hình giọt nước dựng đứng, cổ hẹp ở trên, bụng tròn ở dưới; vỏ sò kem viền đỏ ở ngực |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\orig\N05.png` | tay xanh gầy chéo từ trên phải (vai) xuống dưới trái; bàn tay tròn ở đầu dưới, vòng xanh chanh ở cổ tay |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\orig\N06.png` | tay xanh từ trên trái (vai) chạy xuống rồi cong sang phải; bàn tay tròn ở đầu dưới, vòng xanh chanh ở cổ tay |
| 7 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\orig\N07.png` | đuôi xanh, mép thẳng rộng ở bên phải (chỗ nối thân), quét sang trái, chóp cong lên ở trên bên trái có sọc cam và xanh lá |
| 8 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\giot_suong_1\orig\N08.png` | hai chân xanh hình lá đứng cạnh nhau, đầu rộng ở trên (hông), mũi nhọn ở dưới (bàn chân) chĩa xuống hơi sang trái |
| 9 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 hai cánh mũ** (đổi dáng, viền khoảng 10 px):
- cánh trái mọc từ đầu dưới bên phải của nó, cánh phải mọc từ đầu dưới bên trái, đúng chỗ gốc cũ;
- hai cánh nhỏ bạc viền xanh, chĩa lên và ra ngoài; không vẽ đầu.

**N02 đầu, mặt, mũ giáp** (đổi dáng, viền khoảng 10 px):
- mép dưới đầu ngang mép dưới cũ (phủ cổ), đỉnh ngang đỉnh cũ;
- mắt, miệng đúng chỗ cũ (chồng lên ảnh 1 để so); mặt quả quyết, cười tự tin lộ răng nanh nhỏ;
- mũ giáp tròn che đỉnh và sau đầu, vành mũ ở chỗ vòng lưỡi liềm cũ; mặt lộ rõ dưới vành;
- không có cánh mũ, không có chùm lông mũ (hai nhóm riêng).

**N03 chùm lông mũ** (đổi dáng, viền khoảng 28 px):
- đáy chùm lông nằm dọc mép dưới cũ (chỗ cắm vào mũ);
- chóp cong lên sang trái như chóp cũ; cỡ như cũ.

**N04 thân và giáp ngực** (giữ viền, viền khoảng 28 px):
- viền thân như cũ: cổ hẹp ở trên, bụng tròn ở dưới;
- giáp ngực bạc trơn, không họa tiết đúng chỗ và cỡ của vỏ sò;
- không có tay, chân, đầu.

**N05 tay trái** (giữ viền, viền khoảng 28 px):
- vai ở đầu trên bên phải, tay chạy xuống trái;
- nắm tay ở **đầu dưới** đeo găng giáp bạc bọc cả nắm tay và cổ tay (chỗ vòng xanh chanh cũ); không tay áo.

**N06 tay phải nắm chuôi kiếm** (giữ viền, viền khoảng 28 px):
- vai ở đầu trên bên trái, tay chạy xuống rồi cong sang phải;
- nắm tay ở **đầu dưới** nắm chuôi kiếm, chỉ thấy khúc chuôi trong nắm tay (lưỡi kiếm vẽ riêng ở bước N09);
- găng giáp bạc bọc nắm tay và cổ tay (chỗ vòng xanh chanh cũ); không tay áo.

**N07 đuôi nước** (đổi dáng, viền khoảng 25 px):
- mép nối thân vẫn ở **bên phải**, đúng chỗ mép thẳng cũ;
- chóp cong lên ở trên bên trái; to hơn đuôi cũ một chút, không chạm mép ảnh.

**N08 hai chân đi ủng** (giữ viền, viền khoảng 28 px):
- hông ở **đầu trên** (đầu rộng), bàn chân ở **đầu dưới**;
- ủng bạc nhỏ ở đầu dưới, mũi chĩa xuống hơi sang trái ở cả hai chân.

**N09 thanh kiếm** (vẽ riêng, Claude gắn vào bàn tay khi ghép; viền khoảng 18 px):
- chỉ thanh kiếm, dựng thẳng: chuôi ở trên, mũi kiếm chĩa xuống;
- kiếm ngắn của hiệp sĩ tập sự như concept: lưỡi bạc, chắn tay vàng, chuôi ngắn, đốc tròn vàng nhỏ; cao khoảng 80% ảnh;
- không có tay, không có con vật.

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
