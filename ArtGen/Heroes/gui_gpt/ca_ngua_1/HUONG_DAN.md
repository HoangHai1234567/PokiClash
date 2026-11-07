# Gói gửi GPT: Cá Ngựa dạng 1/3 (Cá Ngựa Tân Binh, `ca_ngua_1`)

Tướng Hiếm hệ Thủy (quái thường đảo Thủy), dạng 1/3, rig aola #181. Thiết kế: cá ngựa tân binh lính gác rạn san hô: xanh lục biển, bụng vàng kem có ngấn ngang; mắt hổ phách to, mày xếch; mào ba nhánh san hô đỏ; cán cờ sau lưng có cờ đuôi nheo đỏ trắng, dây tảo bện từ mõm vòng ra sau; ôm quả cầu nhím biển tím có ngòi tảo và tia lửa hình sao. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\ca_ngua_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (1022 × 1071): con gốc #181 là cá ngựa con đứng trên hai bàn chân nhỏ, quay sang phải người xem: đầu xanh to, một mắt to giữa đầu và mắt kia nhỏ sát mép phải, mõm ống chĩa sang phải loe miệng như kèn, vây má xanh bên trái đầu, ba chỏm tóc nâu trên đỉnh đầu, ống thở trắng chĩa lên sau gáy về trên trái có chỏm nâu ở đầu, ống cao su đen từ dưới mõm vòng ra sau; thân tròn nhỏ; hai tay ôm quả bom sắt đen to trước bụng (dưới phải), ngòi và tia lửa đỏ ở trên phải quả bom. Bỏ khỏi bóng xám: bóng dưới chân, lớp viền đen cả con |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (1022 × 1071, nền trắng): 1 đầu có mắt, 2 mõm ống, 3 vây má, 4 ba chỏm trên đầu, 5 cán sau gáy và chỏm ở đầu cán, 6 ống từ mõm vòng ra sau, 7 thân, 8 bàn tay, 9 bàn chân, 10 quả bom có ngòi và tia lửa |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept ca_ngua_1". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\ca_ngua_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi thử ca_ngua_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N03, N04, N05, N06, N07, N08, N09.
3. Đủ ảnh thì nhắn Claude "ghép ca_ngua_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\orig\N01.png` | Đầu cá ngựa tròn to màu xanh (1024 × 1024, nền trắng) quay sang phải: một mắt to xanh xám ở giữa, mép phải có mẩu mắt xa |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\orig\N02.png` | Mõm hình kèn màu cam (1024 × 1024, nền trắng): đầu hẹp ở trên trái nối vào đầu, miệng loe mở ở dưới phải |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\orig\N03.png` | Vây má xanh có các thuỳ tròn ở mép trái (1024 × 1024, nền trắng); mép phải thẳng nối vào bên đầu |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\orig\N04.png` | Ba chỏm tóc nâu nhạt cong lên (1024 × 1024, nền trắng), đứng trên đỉnh đầu; đầu không có trong ảnh |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\orig\N05.png` | Ống trắng có ngấn xám chạy lên trên trái (1024 × 1024, nền trắng), đầu trên trái là chỏm tóc nâu |
| 6 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\orig\N06.png` | Ống cao su xám đen (1024 × 1024, nền trắng) cong từ phải (dưới mõm) sang trái và xuống (vòng quanh cổ) |
| 7 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\orig\N07.png` | Thân tròn nhỏ màu xanh có mảng bụng nâu nhạt to quay sang phải (1024 × 1024, nền trắng), bàn tay nhỏ nâu nhạt ở mép trái |
| 8 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\orig\N08.png` | Hai mảnh nhỏ nâu nhạt (1024 × 1024, nền trắng): một mảnh dẹt ở trên phải, một bàn chân tròn ở dưới trái |
| 9 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_1\orig\N09.png` | Quả bom sắt tròn đen xám có nắp sọc ở trên phải (1024 × 1024, nền trắng), ngòi ngắn và tia lửa đỏ ở mép phải, tay xanh nhỏ đỡ dưới bên trái, ngón tay nâu nhạt ở trên phải |
| 10 | `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 đầu có mắt** (giữ viền, viền khoảng 13 px):
- giữ viền đầu như cũ; mắt to đúng chỗ mắt cũ, mẩu mắt xa ở mép phải;
- xanh lục biển, vài gờ nhỏ phía sau đầu; mắt hổ phách con ngươi đen một chấm sáng, mày xanh sẫm dày xếch xuống;
- không vẽ mõm, vây má, mào, dây, cán cờ.

**N02 mõm ống** (đổi dáng, viền khoảng 23 px):
- đầu hẹp ở trên trái đúng chỗ cũ (nối vào đầu), chĩa cùng hướng xuống phải;
- mõm ống ngắn xanh lục biển, miệng tròn viền vàng kem, trong miệng sẫm; không loe như kèn;
- không vẽ đầu, dây.

**N03 vây má** (đổi dáng, viền khoảng 22 px):
- mép phải đúng chỗ cũ (nối vào đầu), thuỳ vây xoè sang trái;
- xanh lục biển, ba gân vàng nhạt như concept;
- không vẽ đầu.

**N04 mào san hô** (đổi dáng, viền khoảng 11 px):
- ba nhánh san hô đỏ, gốc mỗi nhánh đúng chỗ gốc chỏm cũ, chĩa lên;
- có thể cao hơn chỏm cũ một chút, phân nhánh tròn đầu như concept;
- không vẽ đầu; không tóc nâu.

**N05 cán cờ và cờ đuôi nheo** (đổi dáng, viền khoảng 22 px):
- chân cán ở dưới phải đúng chỗ cũ (sau gáy), cán chạy lên trên trái như ống cũ;
- cán gỗ nâu, gần chân có quấn dây xanh tảo, đầu cán có núm tròn; cờ đuôi nheo đỏ trắng bay sang trái ở đầu trên;
- không vẽ đầu; không ống trắng, không chỏm tóc.

**N06 dây tảo bện** (giữ viền, viền khoảng 24 px):
- đúng đường đi, độ dày, hai đầu như ống cũ;
- dây bện xanh tảo, thấy các vòng xoắn như concept;
- không vẽ mõm, đầu, thân.

**N07 thân và tay xa** (giữ viền, viền khoảng 18 px):
- giữ viền thân và chỗ bàn tay như cũ;
- thân xanh lục biển, bụng vàng kem có các vạch ngang nâu mảnh; tay xanh lục biển;
- vẽ trọn thân (quả cầu đè lên sau); không vẽ quả cầu, đầu, dây.

**N08 hai bàn chân** (giữ viền, viền khoảng 33 px):
- hai mảnh đúng chỗ, cỡ, dáng như cũ;
- xanh lục biển;
- không vẽ thân, quả cầu.

**N09 quả cầu nhím biển và hai tay** (giữ viền, viền khoảng 14 px):
- quả cầu đúng chỗ, cỡ như quả bom cũ; ngòi và tia lửa đúng chỗ cũ; hai tay đúng chỗ cũ;
- quả cầu nhím biển tím gai ngắn tù; ngòi là cọng tảo xoắn, tia lửa hình sao cam vàng tô phẳng; tay xanh lục biển;
- không bom sắt, không nắp sọc, không quầng sáng.

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
