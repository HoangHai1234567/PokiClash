# Gói gửi GPT: Mập Răng Cưa dạng 3/3 (Vua Cá Mập, `map_rang_3`)

Tướng Hiếm hệ Thủy (quái thường đảo Thủy), dạng 3/3, rig aola #33. Thiết kế: Vua Cá Mập: to, oai, lưng xám chì ánh tím, bụng kem; mũ giáp xương ngà có vương miện răng cá mập; tấm chắn mõm xương ngà thay kính che mặt; giáp vai xương ngà; vằn cam cháy răng cưa dọc thân và vây; vây lưng lớn mép răng cưa; mắt vàng chanh, gờ mày sẫm; hàm răng cưa. Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`D:\PokiClash\ArtGen\Heroes\inbox\map_rang_3\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\map_rang_3\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_3\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\Silhouette.png` | Bóng xám của con gốc trên nền trắng (420 × 397): con gốc #33 là cá mập vua to lơ lửng, quay sang phải: kính che mặt xanh sẫm có nhiều chi tiết máy phủ mõm, tấm giáp xanh lớn trên đầu, tấm đỏ trên mắt, dải đỏ dọc đầu và tấm má, huy hiệu số 03, giáp lưng, mang đỏ, vây lưng lớn có hình chớp đỏ, vây nhỏ trước vây lưng, hai khúc thân sau, vây đuôi đỏ, vây ngực lớn chĩa xuống trái, vây bụng nhỏ, miệng răng cưa. Bỏ khỏi bóng xám: bóng dưới chân, lớp viền cả con |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (420 × 397, nền trắng): 1 đầu và thân trước, 2 mắt và tấm trên mắt, 3 kính che mõm, 4 tấm giáp trên đầu, 5 dải đầu và tấm má, 6 chóp mũi, 7 miệng, 8 huy hiệu, 9 giáp lưng, 10 mang, 11 vây lưng, 12 vây nhỏ trước vây lưng, 13 hai khúc thân sau, 14 vây đuôi, 15 vây ngực, 16 vây bụng |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |
| 6 | `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_1\concept_duyet.png` | Concept đã duyệt của `map_rang_1` (1774 × 887, nền trắng): dạng 1 đã duyệt: cá mập xám chì ánh tím bụng kem, vằn cam răng cưa, mắt vàng chanh, giáp trán xương ngà |

Xong thì nhắn Claude "duyệt concept map_rang_3". Duyệt xong Claude lưu `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_3\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `D:\PokiClash\ArtGen\Heroes\gui_gpt\map_rang_3\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_3\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N06. Nhắn Claude "soi thử map_rang_3".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N02, N03, N04, N05, N07, N08, N09, N10, N11.
3. Đủ ảnh thì nhắn Claude "ghép map_rang_3".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N01.png` | Đầu và thân trước cá mập to xanh hải quân bụng trắng quay sang phải (1024 × 1024, nền trắng), kính che mõm xanh sẫm có chi tiết máy, tấm đỏ trên mắt, dải đỏ dọc đầu, miệng răng cưa |
| 2 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N02.png` | Tấm giáp xanh dài phủ đỉnh đầu, cong xuống ở phía trước (bên phải) (1024 × 1024, nền trắng) |
| 3 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N03.png` | Huy hiệu xám có số '03' (1024 × 1024, nền trắng) |
| 4 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N04.png` | Tấm giáp lưng xanh thẫm (1024 × 1024, nền trắng) |
| 5 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N05.png` | Ba tấm mang đỏ sẫm xếp hàng (1024 × 1024, nền trắng) |
| 6 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N06.png` | Vây lưng lớn xanh hải quân có hình chớp đỏ trắng (1024 × 1024, nền trắng), gốc dưới phải, chóp trên trái |
| 7 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N07.png` | Vây nhỏ xanh (1024 × 1024, nền trắng), gốc ở dưới, chóp ở trên |
| 8 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N08.png` | Hai khúc thân sau xanh thẫm nối liền (1024 × 1024, nền trắng) |
| 9 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N09.png` | Vây đuôi xanh hải quân và đỏ (1024 × 1024, nền trắng), gốc hẹp bên phải, hai thuỳ bên trái |
| 10 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N10.png` | Vây ngực lớn xanh hải quân có sọc đỏ trắng (1024 × 1024, nền trắng), chĩa xuống trái |
| 11 | `D:\PokiClash\ArtGen\Heroes\refs\thuy\map_rang_3\orig\N11.png` | Vây bụng nhỏ xanh hải quân có sọc đỏ rủ xuống (1024 × 1024, nền trắng) |
| 12 | `D:\PokiClash\ArtGen\Heroes\inbox\map_rang_3\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 đầu thân có mặt và tấm chắn mõm** (giữ viền, viền khoảng 11 px):
- giữ viền như cũ; mắt vàng chanh đúng chỗ mắt cũ, gờ mày xám sẫm xếch;
- xám chì ánh tím, bụng hàm kem; chỗ kính che mõm thành tấm chắn mõm xương ngà (không kính, không máy);
- dải đầu thành vằn cam răng cưa; cười trọn hàm răng cưa ở chỗ miệng cũ;
- không vẽ vây, mũ giáp, huy hiệu; không đỏ, không xanh hải quân.

**N02 mũ giáp xương vương miện răng** (đổi dáng, viền khoảng 11 px):
- tấm giáp nằm đúng chỗ cũ trên đỉnh đầu;
- xương ngà, dọc mép trên là hàng răng cá mập trắng dựng lên như concept;
- không vẽ đầu; không xanh, không kim loại.

**N03 giáp trán xương ngà** (đổi dáng, viền khoảng 40 px):
- đúng chỗ huy hiệu cũ, cỡ gần như cũ;
- miếng xương ngà có ba khía; không chữ số;
- không vẽ đầu.

**N04 giáp lưng xương ngà** (giữ viền, viền khoảng 40 px):
- giữ viền như cũ;
- xương ngà;
- không vẽ thân.

**N05 vằn mang** (giữ viền, viền khoảng 36 px):
- giữ viền như cũ;
- ba vằn cam cháy mép răng cưa trên nền xám chì như concept;
- không vẽ thân; không đỏ.

**N06 vây lưng lớn** (đổi dáng, viền khoảng 19 px):
- gốc đúng chỗ cũ, chóp cùng hướng;
- tím ánh xám, mép sau răng cưa, dải cam răng cưa;
- không vẽ thân; không đỏ.

**N07 vây nhỏ trước vây lưng** (đổi dáng, viền khoảng 30 px):
- gốc đúng chỗ cũ;
- tím ánh xám;
- không vẽ thân.

**N08 hai khúc thân sau** (giữ viền, viền khoảng 33 px):
- giữ viền như cũ;
- xám chì, mỗi khúc một dải cam;
- không vẽ thân trước, vây đuôi.

**N09 vây đuôi** (đổi dáng, viền khoảng 17 px):
- gốc hẹp bên phải đúng chỗ cũ;
- tím ánh xám, vằn cam, mép răng cưa;
- không vẽ thân; không đỏ.

**N10 vây ngực lớn** (giữ viền, viền khoảng 16 px):
- giữ viền như cũ;
- tím ánh xám, mép kem, một dải cam;
- không vẽ thân; không đỏ.

**N11 vây bụng** (giữ viền, viền khoảng 31 px):
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
