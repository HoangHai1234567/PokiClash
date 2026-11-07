# Gói gửi GPT: Mập Răng Cưa dạng 2/3 (Mập Răng Cưa, `map_rang_2`)

Tướng Hiếm hệ Thủy (quái thường đảo Thủy), dạng 2/3, rig aola #32. Thiết kế: Mập Răng Cưa lớn lên: thon và dữ hơn, lưng xám chì ánh tím, bụng kem như dạng 1; mép vây lưng và vây đuôi răng cưa, vằn cam cháy; tấm giáp xương ngà mép răng cưa trên đỉnh đầu; giáp trán xương ngà có khía; nhe trọn hàm răng cưa; mắt vàng chanh. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\map_rang_2\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\map_rang_2\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_2\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\Silhouette.png` | Bóng xám của con gốc trên nền trắng (1389 × 1069): con gốc #32 là cá mập thon lơ lửng, nhìn nghiêng ba phần tư quay sang phải: đầu to có tấm giáp xanh trên đỉnh và chóp vây nhỏ trên phải, huy hiệu số 02 trên trán, mắt đỏ, mang đỏ phát sáng, miệng răng nhọn ở dưới phải; vây lưng cao, vây nhỏ gần đuôi, thân sau hai khúc, vây đuôi đỏ xanh bên trái, vây ngực dưới bụng, vây bụng nhỏ. Bỏ khỏi bóng xám: bóng dưới chân, lớp viền cả con |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (1389 × 1069, nền trắng): 1 đầu và thân trước, 2 mắt, 3 tấm giáp trên đầu, 4 huy hiệu, 5 mang, 6 vây lưng, 7 vây nhỏ gần đuôi, 8 hai khúc thân sau, 9 vây đuôi, 10 vây ngực, 11 vây bụng |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |
| 6 | `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_1\concept_duyet.png` | Concept đã duyệt của `map_rang_1` (1774 × 887, nền trắng): dạng 1 đã duyệt: cá mập xám chì ánh tím bụng kem, vằn cam răng cưa, mắt vàng chanh, giáp trán xương ngà |

Xong thì nhắn Claude "duyệt concept map_rang_2". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_2\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\map_rang_2\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_2\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N03. Nhắn Claude "soi thử map_rang_2".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N02, N04, N05, N06, N07, N08.
3. Đủ ảnh thì nhắn Claude "ghép map_rang_2".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\orig\N01.png` | Đầu và thân trước cá mập xanh hải quân nhìn ba phần tư quay sang phải (1024 × 1024, nền trắng): mắt đỏ, mang đỏ phát sáng, huy hiệu '02', hàm trắng răng nhọn |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\orig\N02.png` | Tấm giáp xanh nằm dọc đỉnh đầu từ trái sang phải (1024 × 1024, nền trắng), và chóp vây nhỏ riêng ở bên phải |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\orig\N03.png` | Vây lưng cao xanh hải quân mép trước nhạt (1024 × 1024, nền trắng), gốc ở dưới phải, chóp ở trên trái |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\orig\N04.png` | Vây nhỏ xanh thẫm (1024 × 1024, nền trắng), gốc ở dưới |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\orig\N05.png` | Hai khúc thân sau xanh thẫm nối liền từ thân (phải) tới vây đuôi (trái) (1024 × 1024, nền trắng) |
| 6 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\orig\N06.png` | Vây đuôi xanh hải quân và đỏ (1024 × 1024, nền trắng), gốc hẹp bên phải, hai thuỳ bên trái |
| 7 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\orig\N07.png` | Vây ngực xanh hải quân mép dưới nhạt (1024 × 1024, nền trắng), chĩa xuống trái |
| 8 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_2\orig\N08.png` | Vây bụng nhỏ xanh hải quân và xám rủ xuống (1024 × 1024, nền trắng) |
| 9 | `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_2\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 đầu thân có mặt, vằn mang, giáp trán** (giữ viền, viền khoảng 8 px):
- giữ viền như cũ; mắt vàng chanh đúng chỗ mắt cũ, gờ mày xám sẫm xếch;
- xám chì ánh tím, bụng và hàm kem, cười nhe trọn hàm răng cưa ở chỗ miệng cũ;
- ba vằn cam răng cưa đúng chỗ mang cũ (không phát sáng); giáp trán xương ngà có khía ở chỗ huy hiệu (không chữ số);
- không vẽ vây, tấm giáp đầu; không đỏ, không xanh hải quân.

**N02 tấm giáp xương trên đầu** (đổi dáng, viền khoảng 17 px):
- tấm giáp nằm đúng chỗ cũ dọc đỉnh đầu, chóp nhỏ bên phải đúng chỗ cũ;
- xương ngà, mép răng cưa như concept;
- không vẽ đầu.

**N03 vây lưng** (đổi dáng, viền khoảng 16 px):
- gốc vây đúng chỗ cũ, chóp chĩa cùng hướng;
- tím ánh xám, mép sau răng cưa, dải cam răng cưa;
- không vẽ thân.

**N04 vây nhỏ gần đuôi** (đổi dáng, viền khoảng 68 px):
- gốc đúng chỗ cũ;
- tím ánh xám, chóp cam;
- không vẽ thân.

**N05 hai khúc thân sau** (giữ viền, viền khoảng 25 px):
- giữ viền hai khúc như cũ;
- xám chì, mỗi khúc một dải cam;
- không vẽ thân trước, vây đuôi.

**N06 vây đuôi** (đổi dáng, viền khoảng 13 px):
- gốc hẹp bên phải đúng chỗ cũ;
- tím ánh xám, vằn cam, mép răng cưa;
- không vẽ thân; không đỏ.

**N07 vây ngực** (giữ viền, viền khoảng 19 px):
- giữ viền như cũ;
- tím ánh xám, mép kem;
- không vẽ thân.

**N08 vây bụng** (giữ viền, viền khoảng 47 px):
- giữ viền như cũ;
- tím ánh xám, mép kem;
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
