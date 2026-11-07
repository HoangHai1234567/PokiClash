# Gói gửi GPT: Cá Ngựa dạng 3/3 (Cá Ngựa Tướng Quân, `ca_ngua_3`)

Tướng Hiếm hệ Thủy (quái thường đảo Thủy), dạng 3/3, rig aola #183. Thiết kế: Cá Ngựa thành tướng quân rạn san hô: xanh lục biển, bụng kem như dạng 1; mũ giáp vỏ ốc trắng ngà viền xanh thẫm, mào san hô đỏ to như vương miện; cờ soái vuông đỏ hình sóng trắng; đao mỏ cá kiếm răng cưa đeo sau lưng; giáp ngực mai rùa xanh rêu viền ngà; đai vỏ sò khoá san hô; khiên tay trái và giáp tay phải bằng mảng san hô đỏ viền đồng; đuôi cuộn. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_3\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\ca_ngua_3\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_3\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\Silhouette.png` | Bóng xám của con gốc trên nền trắng (857 × 1123): con gốc #183 là cá ngựa tướng lơ lửng, đầu quay sang phải: đầu xanh nhiều gai có dải đỏ, mặt nạ đỏ, bờm xanh ngọc, mõm kèn chĩa sang phải, ống trắng sau gáy có chỏm xanh ở đầu (trên trái), chuôi kiếm đỏ hoa văn trắng ló sau đầu và bao kiếm ở cổ, hai ống thở đen, cổ áo đen, giáp ngực xám có viền nâu, đai đỏ có khoá tròn và tua; tay trái có khiên sao đỏ vàng to ở cẳng tay và tấm giáp đỏ, tay phải có giáp cẳng tay xám và tấm đỏ; đuôi cuộn dưới. Bỏ khỏi bóng xám: bóng dưới chân, lớp viền đen cả con |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (857 × 1123, nền trắng): 1 đầu có mặt nạ và mắt, 2 mõm, 3 bờm, 4 cán sau gáy và chỏm, 5 kiếm sau lưng, 6 hai ống thở, 7 cổ áo, 8 giáp ngực, 9 đai và giáp bụng, 10 tay trái và bàn tay, 11 khiên cẳng tay trái, 12 tay phải và bàn tay, 13 tấm giáp cẳng tay phải, 14 đuôi cuộn |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |
| 6 | `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_1\concept_duyet.png` | Concept đã duyệt của `ca_ngua_1` (1225 × 1284, nền trắng): dạng 1 đã duyệt: cá ngựa xanh lục biển bụng kem, mào san hô đỏ, cờ đuôi nheo, ôm quả cầu nhím tím |

Xong thì nhắn Claude "duyệt concept ca_ngua_3". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_3\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\ca_ngua_3\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_3\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N11. Nhắn Claude "soi thử ca_ngua_3".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N02, N03, N04, N05, N06, N07, N08, N09, N10, N12, N13, N14.
3. Đủ ảnh thì nhắn Claude "ghép ca_ngua_3".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N01.png` | Đầu cá ngựa xanh nhiều gai quay sang phải có dải đỏ (1024 × 1024, nền trắng), che bởi mặt nạ đỏ có lỗ mắt |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N02.png` | Mõm hình kèn nâu cam (1024 × 1024, nền trắng): đầu hẹp ở trên trái nối vào đầu, miệng loe ở dưới phải |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N03.png` | Bờm xanh ngọc nhỏ trên đỉnh đầu và mái xanh ngọc phía trước (1024 × 1024, nền trắng); đầu không có trong ảnh |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N04.png` | Ống trắng từ dưới phải chĩa lên trên trái (1024 × 1024, nền trắng), đầu là chỏm xanh ngọc to |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N05.png` | Thanh katana nằm chéo (1024 × 1024, nền trắng): chuôi đỏ hoa văn trắng ở trên trái, bao kiếm sẫm đầu nâu ở dưới phải |
| 6 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N06.png` | Hai ống thở xám đen có ngấn (1024 × 1024, nền trắng): một cong từ trên phải xuống trái, một ở dưới cong sang phải |
| 7 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N07.png` | Cổ áo tròn màu đen (1024 × 1024, nền trắng) |
| 8 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N08.png` | Giáp ngực tròn xám viền nâu (1024 × 1024, nền trắng), dây nhỏ ở trên phải |
| 9 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N09.png` | Ba mảnh đỏ nhỏ (1024 × 1024, nền trắng): khoá tròn tâm vàng ở trên, tấm giáp bụng đỏ ở dưới, tua nâu nhạt nhỏ bên phải |
| 10 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N10.png` | Bắp tay xanh và ống tay tím có đệm (1024 × 1024, nền trắng) cong xuống nắm tay xanh ở dưới trái có giáp nắm tay tròn đỏ |
| 11 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N11.png` | Khiên hình sao vàng đỏ to (1024 × 1024, nền trắng) với tấm đỏ phía sau |
| 12 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N12.png` | Tay xanh dài cong từ trên trái xuống nắm tay xanh ở dưới phải (1024 × 1024, nền trắng), vòng xám ở cẳng tay |
| 13 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N13.png` | Tấm giáp cao đỏ vàng ở mặt ngoài cẳng tay (1024 × 1024, nền trắng) |
| 14 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_3\orig\N14.png` | Đuôi cá ngựa xanh có gờ nâu cuộn tròn (1024 × 1024, nền trắng) |
| 15 | `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_3\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 đầu có mặt và mũ vỏ ốc** (đổi dáng, viền khoảng 13 px):
- cổ (mép dưới đầu) đúng chỗ cũ; hai mắt đúng chỗ hai lỗ mắt cũ;
- mặt xanh lục biển, mắt hổ phách mày xếch, cười nhếch; mũ vỏ ốc ngà viền xanh thẫm có vỏ sò vàng nhỏ ở trán như concept;
- không gai xanh, không mặt nạ đỏ; không vẽ mõm, mào san hô, cờ, đao.

**N02 mõm ống** (đổi dáng, viền khoảng 32 px):
- đầu hẹp ở trên trái đúng chỗ cũ, chĩa cùng hướng;
- mõm ống ngắn xanh lục biển, miệng tròn viền vàng kem;
- không vẽ đầu; không loe như kèn.

**N03 vương miện san hô** (đổi dáng, viền khoảng 13 px):
- gốc đúng chỗ gốc bờm cũ (trên đỉnh mũ);
- san hô đỏ to nhiều nhánh tròn như vương miện, cao hơn bờm cũ nhiều như concept;
- không vẽ đầu, mũ; không xanh ngọc.

**N04 cán cờ soái** (đổi dáng, viền khoảng 25 px):
- chân cán ở dưới phải đúng chỗ cũ, cán chạy lên trên trái;
- cán gỗ có núm vàng đồng, cờ soái vuông đỏ viền vàng có hình sóng trắng, mép dưới cờ răng cưa như concept;
- không chữ; không vẽ đầu.

**N05 đao mỏ cá kiếm sau lưng** (đổi dáng, viền khoảng 18 px):
- nằm chéo đúng như cũ, chuôi ở trên trái, đoạn dưới ở dưới phải;
- lưỡi mỏ cá kiếm trắng ngà răng cưa nhỏ, chuôi quấn dây xanh thẫm, đốc san hô đỏ, đoạn bao xanh rêu như concept;
- không katana, không hoa văn kim cương; không vẽ đầu, thân.

**N06 hai dây tảo** (giữ viền, viền khoảng 29 px):
- đúng đường đi, độ dày như ống cũ;
- dây bện xanh tảo;
- không vẽ đầu, thân.

**N07 khăn cổ** (giữ viền, viền khoảng 37 px):
- giữ viền như cũ;
- khăn cổ xanh thẫm có nút thắt;
- không vẽ đầu, thân.

**N08 giáp ngực mai rùa** (giữ viền, viền khoảng 26 px):
- giữ viền như cũ;
- mai rùa xanh rêu hoa văn lục giác, viền ngà, dây vai xanh thẫm khoá vàng như concept;
- không vẽ tay, đầu; không xám.

**N09 đai vỏ sò** (giữ viền, viền khoảng 19 px):
- ba mảnh đúng chỗ, cỡ như cũ;
- khoá tròn san hô đỏ viền đồng; tấm bụng thành đoạn đai vỏ sò ngà; tua thành tua tảo xanh;
- không vẽ thân.

**N10 tay trái và nắm tay** (giữ viền, viền khoảng 20 px):
- vai ở trên phải, nắm tay ở dưới trái đúng chỗ cũ;
- tay xanh lục biển, quấn cổ tay xanh thẫm, giáp nắm tay san hô đỏ;
- không vẽ khiên, thân; không tím.

**N11 khiên san hô tay trái** (đổi dáng, viền khoảng 26 px):
- tâm khiên đúng chỗ tâm khiên cũ, cỡ gần như cũ;
- khiên tròn san hô đỏ hoa văn san hô, viền đồng có đinh tán như concept; không hình sao;
- không vẽ tay, thân.

**N12 tay phải, nắm tay và giáp tay** (giữ viền, viền khoảng 25 px):
- vai ở trên trái, nắm tay ở dưới phải đúng chỗ cũ;
- tay xanh lục biển, giáp cẳng tay vỏ sò ngà, quấn cổ tay xanh thẫm;
- không vẽ tấm giáp đỏ, thân.

**N13 tấm giáp san hô tay phải** (đổi dáng, viền khoảng 30 px):
- đúng chỗ, cỡ gần như cũ;
- tấm san hô đỏ viền đồng có vỏ sò ngà nhỏ như concept;
- không vẽ tay.

**N14 đuôi cuộn** (giữ viền, viền khoảng 20 px):
- giữ viền và chiều cuộn như cũ;
- xanh lục biển, gờ vàng kem;
- không vẽ thân.

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
