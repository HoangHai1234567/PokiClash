# Gói gửi GPT: Cá Ngựa dạng 2/3 (Cá Ngựa Song Đao, `ca_ngua_2`)

Tướng Hiếm hệ Thủy (quái thường đảo Thủy), dạng 2/3, rig aola #182. Thiết kế: Cá Ngựa lớn lên thành lính gác song đao: xanh lục biển, bụng vàng kem có ngấn như dạng 1; bỏ mặt nạ, mặt thật có băng trán xanh thẫm buộc sau gáy; mào san hô đỏ to hơn; hai vây má; cán cờ cờ đuôi nheo to hơn; dây tảo bện; khăn cổ xanh thẫm; giáp ngực mai rùa xanh rêu; hai dao găm lưỡi răng cá mập trắng ngà chuôi quấn tảo; đuôi cuộn. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_2\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\ca_ngua_2\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_2\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\Silhouette.png` | Bóng xám của con gốc trên nền trắng (904 × 1039): con gốc #182 là cá ngựa đứng trên đuôi cuộn, đầu quay sang phải: mặt nạ đỏ có hai lỗ mắt, mõm kèn cam chĩa sang phải, hai vây má xanh, chỏm tóc vàng nâu trên đỉnh, ống trắng sau gáy có chỏm ở đầu, chuỗi hạt ống thở từ mõm vòng ra sau, cổ áo đen, giáp ngực xám tròn, bụng ngấn nâu; hai tay găng trắng cầm hai dao phi tiêu có vòng ở chuôi (trái chĩa lên trái, phải chĩa lên phải); đuôi cuộn dưới. Bỏ khỏi bóng xám: bóng dưới chân, lớp viền đen cả con |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (904 × 1039, nền trắng): 1 đầu có mặt nạ và mắt, 2 mõm, 3 hai vây má, 4 chỏm trên đầu, 5 cán sau gáy và chỏm, 6 chuỗi hạt ống thở, 7 cổ áo, 8 giáp ngực, 9 bụng và hông, 10 tay trái, 11 bàn tay trái, 12 dao trái, 13 tay phải, 14 bàn tay phải, 15 dao phải, 16 đuôi cuộn |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |
| 6 | `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_1\concept_duyet.png` | Concept đã duyệt của `ca_ngua_1` (1225 × 1284, nền trắng): dạng 1 đã duyệt: cá ngựa xanh lục biển bụng kem, mào san hô đỏ, cờ đuôi nheo, ôm quả cầu nhím tím |

Xong thì nhắn Claude "duyệt concept ca_ngua_2". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_2\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\ca_ngua_2\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_2\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N10. Nhắn Claude "soi thử ca_ngua_2".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N02, N03, N04, N05, N06, N07, N08, N09, N11, N12.
3. Đủ ảnh thì nhắn Claude "ghép ca_ngua_2".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N01.png` | Đầu cá ngựa tròn xanh quay sang phải (1024 × 1024, nền trắng), che bởi mặt nạ đỏ có hai lỗ mắt tròn |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N02.png` | Mõm hình kèn màu cam (1024 × 1024, nền trắng): đầu hẹp bên trái nối vào đầu, miệng loe bên phải |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N03.png` | Hai vây má xanh có thuỳ (1024 × 1024, nền trắng): một bên trái đầu, một bên phải sau mõm |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N04.png` | Chỏm tóc nâu nhạt to trên đỉnh đầu và chỏm nhỏ bên phải (1024 × 1024, nền trắng); đầu không có trong ảnh |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N05.png` | Ống trắng từ dưới phải chĩa lên trên trái (1024 × 1024, nền trắng), đầu là chỏm nâu nhạt nhiều gai |
| 6 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N06.png` | Chuỗi hạt xám đen thành ống cong từ phải sang trái (1024 × 1024, nền trắng) |
| 7 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N07.png` | Cổ áo tròn màu đen (1024 × 1024, nền trắng) |
| 8 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N08.png` | Giáp ngực tròn xám đỉnh tím có đệm, viền vàng (1024 × 1024, nền trắng), mẩu nâu nhỏ ở dưới trái |
| 9 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N09.png` | Mảng bụng nâu nhạt có ngấn, xanh bên trái (1024 × 1024, nền trắng), vài mẩu nâu nhỏ phía trên |
| 10 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N10.png` | Tay xanh từ phải cong xuống nắm tay găng trắng ở dưới trái (1024 × 1024, nền trắng), cầm dao phi tiêu chĩa lên trái, vòng ở chuôi |
| 11 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N11.png` | Tay xanh từ trái cong xuống nắm tay găng trắng ở dưới phải (1024 × 1024, nền trắng), cầm dao phi tiêu chĩa lên phải, vòng ở chuôi |
| 12 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\ca_ngua_2\orig\N12.png` | Đuôi cá ngựa xanh cuộn tròn ở bên phải, có gờ nâu nhạt (1024 × 1024, nền trắng) |
| 13 | `D:\PokiClash\ArtGen\Heroes\inbox\ca_ngua_2\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 đầu có mặt và băng trán** (giữ viền, viền khoảng 15 px):
- giữ viền đầu như cũ; hai mắt đúng chỗ hai lỗ mắt cũ (mắt gần to, mắt xa nhỏ);
- mặt xanh lục biển, mắt hổ phách mày xanh sẫm xếch; băng trán xanh thẫm buộc nút sau gáy như concept;
- không mặt nạ đỏ; không vẽ mõm, vây má, mào, cán cờ.

**N02 mõm ống** (đổi dáng, viền khoảng 29 px):
- đầu hẹp bên trái đúng chỗ cũ, mõm chĩa sang phải;
- mõm ống ngắn xanh lục biển, miệng tròn viền vàng kem như concept;
- không vẽ đầu; không loe như kèn.

**N03 hai vây má** (đổi dáng, viền khoảng 12 px):
- gốc mỗi vây đúng chỗ cũ, thuỳ xoè ra ngoài;
- xanh lục biển gân vàng nhạt;
- không vẽ đầu.

**N04 mào san hô** (đổi dáng, viền khoảng 14 px):
- gốc mào đúng chỗ gốc chỏm cũ, chĩa lên;
- san hô đỏ nhiều nhánh tròn đầu, to hơn chỏm cũ được như concept;
- không vẽ đầu; không tóc.

**N05 cán cờ và cờ đuôi nheo** (đổi dáng, viền khoảng 25 px):
- chân cán ở dưới phải đúng chỗ cũ, cán chạy lên trên trái;
- cán gỗ nâu núm tròn, quấn dây xanh tảo, cờ đuôi nheo đỏ trắng to ở đầu trên;
- không vẽ đầu; không ống trắng, không chỏm.

**N06 dây tảo bện** (giữ viền, viền khoảng 30 px):
- đúng đường đi và độ dày như chuỗi hạt cũ;
- dây bện xanh tảo có vòng xoắn;
- không vẽ đầu, cổ.

**N07 khăn cổ** (giữ viền, viền khoảng 44 px):
- giữ viền như cũ;
- khăn cổ xanh thẫm có nút thắt ở trước như concept;
- không vẽ đầu, thân.

**N08 giáp ngực mai rùa** (giữ viền, viền khoảng 22 px):
- giữ viền như cũ;
- mai rùa xanh rêu có hoa văn lục giác như concept;
- không vẽ tay, đầu.

**N09 bụng và hông** (giữ viền, viền khoảng 26 px):
- giữ viền các mảnh như cũ;
- bụng vàng kem có ngấn ngang, phần thân xanh lục biển;
- không vẽ giáp ngực, đuôi.

**N10 tay trái, nắm tay và dao** (giữ viền, viền khoảng 19 px):
- vai ở bên phải, nắm tay ở dưới trái đúng chỗ cũ; dao chĩa lên trái như cũ, vòng ở đáy chuôi;
- tay xanh lục biển, quấn cổ tay xanh thẫm, nắm tay xanh lục biển; dao lưỡi răng cá mập trắng ngà, chuôi quấn tảo, vòng đồng;
- không găng trắng, không dao kim loại; không vẽ thân.

**N11 tay phải, nắm tay và dao** (giữ viền, viền khoảng 20 px):
- vai ở bên trái, nắm tay ở dưới phải đúng chỗ cũ; dao chĩa lên phải như cũ, vòng ở đáy chuôi;
- tay xanh lục biển, quấn cổ tay xanh thẫm; dao lưỡi răng cá mập trắng ngà, chuôi quấn tảo, vòng đồng;
- không găng trắng, không dao kim loại; không vẽ thân.

**N12 đuôi cuộn** (giữ viền, viền khoảng 33 px):
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
