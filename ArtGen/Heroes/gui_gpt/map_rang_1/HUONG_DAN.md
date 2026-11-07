# Gói gửi GPT: Mập Răng Cưa dạng 1/3 (Cá Mập Con, `map_rang_1`)

Tướng Hiếm hệ Thủy (quái thường đảo Thủy), dạng 1/3, rig aola #31. Thiết kế: cá mập con biển sâu tròn mập: lưng xám chì ánh tím, bụng và hàm dưới trắng kem; mang là ba vằn cam cháy mép răng cưa; mắt vàng chanh con ngươi đen, gờ mày sẫm xếch; miếng giáp trán xương ngà có ba khía thay huy hiệu số; cười nhếch lộ hàng răng cưa nhỏ; vây lưng và vây đuôi có vằn cam. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\map_rang_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\map_rang_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (824 × 614): con gốc #31 là cá mập con tròn mập lơ lửng, nhìn nghiêng quay sang phải người xem: thân liền đầu, lưng xanh hải quân, bụng trắng; mắt đỏ to ở giữa mặt; huy hiệu số 01 trên trán; ba khe mang đỏ sau mắt; vây lưng trên trái, vây đuôi bên trái, vây ngực dưới bụng chĩa xuống trái, vây bụng nhỏ dưới thân; miệng ở dưới phải có răng nanh nhỏ. Bỏ khỏi bóng xám: bóng dưới chân, lớp viền cả con |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (824 × 614, nền trắng): 1 thân liền đầu, 2 mắt, 3 miệng, 4 huy hiệu trên trán, 5 ba khe mang, 6 vây lưng, 7 vây đuôi, 8 vây ngực, 9 vây bụng nhỏ |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept map_rang_1". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\map_rang_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi thử map_rang_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N03, N04, N05.
3. Đủ ảnh thì nhắn Claude "ghép map_rang_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_1\orig\N01.png` | Thân cá mập tròn mập xanh hải quân bụng trắng quay sang phải (1024 × 1024, nền trắng): mắt đỏ to, ba khe mang đỏ, huy hiệu xám '01' trên trán, miệng nhỏ có răng nanh |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_1\orig\N02.png` | Vây lưng xanh hải quân mép trước nhạt (1024 × 1024, nền trắng), gốc rộng ở dưới (trên lưng), chóp ở trên phải |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_1\orig\N03.png` | Vây đuôi hình lưỡi liềm xanh hải quân và đỏ (1024 × 1024, nền trắng), gốc hẹp ở bên phải nối vào thân, hai thuỳ ở bên trái |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_1\orig\N04.png` | Vây ngực xanh hải quân mép dưới nhạt (1024 × 1024, nền trắng), chĩa xuống trái; đầu trên phải nối vào bụng |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_1\orig\N05.png` | Vây bụng nhỏ xanh hải quân rủ xuống (1024 × 1024, nền trắng), mép trên nối vào bụng |
| 6 | `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 thân có mặt, vằn mang, giáp trán** (giữ viền, viền khoảng 6 px):
- giữ viền thân như cũ (tròn mập), lưng xám chì ánh tím, bụng và hàm dưới trắng kem;
- mắt vàng chanh to đúng chỗ mắt cũ, con ngươi đen một chấm sáng, gờ mày xám sẫm xếch xuống;
- ba vằn cam cháy mép răng cưa đúng chỗ ba khe mang cũ; miếng giáp trán xương ngà nhỏ có ba khía đúng chỗ huy hiệu cũ (không chữ số);
- cười nhếch lộ hàng răng cưa nhỏ ở chỗ miệng cũ;
- không vẽ vây; không xanh hải quân, không đỏ.

**N02 vây lưng** (đổi dáng, viền khoảng 16 px):
- gốc vây đúng chỗ gốc cũ, chóp chĩa cùng hướng;
- tím ánh xám, dải cam cháy răng cưa dọc mép sau như concept;
- không vẽ thân.

**N03 vây đuôi** (đổi dáng, viền khoảng 14 px):
- gốc hẹp ở bên phải đúng chỗ cũ, hai thuỳ xoè sang trái;
- tím ánh xám, hai vằn cam cháy răng cưa như concept;
- không vẽ thân; không đỏ.

**N04 vây ngực** (giữ viền, viền khoảng 18 px):
- giữ viền như cũ; đầu trên phải là chỗ nối vào bụng;
- tím ánh xám, mép dưới kem;
- không vẽ thân.

**N05 vây bụng** (giữ viền, viền khoảng 30 px):
- giữ viền như cũ; mép trên nối vào bụng;
- tím ánh xám;
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
