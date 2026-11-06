# Gói gửi GPT: Ma Kết dạng 1/3 (Ma Kết Con, `ma_ket_1`)

Tướng Hiếm hệ Thủy (ải 20 đảo Thủy, mini boss), dạng 1/3, rig aola #758. Thiết kế: dê biển con lơ lửng, thân dê đuôi cá: lông ngắn xanh mòng két, mõm và cằm trắng kem, chỏm len trắng kem ba lọn nhọn trên trán (không xoáy); hai sừng bạc ngắn có ngấn; tai là vây cam san hô gân xanh mòng két; mắt hổ phách to, vệt mày xếch; cười nhếch; thân tròn bụng kem, thon thành đuôi cá ngắn có vảy, vây đuôi cam san hô; móng xanh thẫm; mặt quả quyết. Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\ma_ket_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (508 × 666): con gốc #758 là dê biển con lơ lửng, nhìn thẳng hơi quay phải: đầu rất to lông trắng xù có xoáy lông cuộn trên trán, hai sừng nâu nhạt (sừng trái to, sừng phải nhỏ sau đầu, cả hai chĩa lên hơi nghiêng trái), hai tai thỏ hồng chìa ngang hai bên đầu, mắt đỏ to (mắt trái to, mắt phải nhỏ sát mép phải), má hồng; thân tròn nhỏ dưới đầu, hai chân trước ngắn buông thẳng; thân thon thành đuôi cá ngắn ở dưới trái, vây đuôi màu kem rủ xuống. Bỏ khỏi bóng xám: bóng dưới chân |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (508 × 666, nền trắng): 1 sừng trái to, 2 sừng phải nhỏ, 3 tai trái, 4 tai phải, 5 đầu có mặt và hai mắt, 6 thân tròn (đuôi cá bắt đầu ở dưới trái), 7 chân trước trái, 8 chân trước phải, 9 vây đuôi |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept ma_ket_1". Duyệt xong Claude lưu `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\ma_ket_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N03. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi thử ma_ket_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N01, N04, N05, N06.
3. Đủ ảnh thì nhắn Claude "ghép ma_ket_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_1\orig\N01.png` | Hai sừng nâu nhạt (1024 × 1024, nền trắng): sừng trái to (gốc rộng ở dưới phải, cong lên tới chóp ở trên trái), sừng phải nhỏ (gốc ở dưới, chóp ở trên); đầu không có trong ảnh |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_1\orig\N02.png` | Hai tai thỏ lòng hồng chìa ngang (1024 × 1024, nền trắng): tai trái to chĩa sang trái (gốc ở đầu phải, có mẩu nhỏ nối vào đầu), tai phải nhỏ chĩa sang phải (gốc ở đầu trái) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_1\orig\N03.png` | Đầu lông trắng xù rất to (1024 × 1024, nền trắng): xoáy lông cuộn ở trên phải, hai mắt đỏ (mắt trái to, mắt phải nhỏ sát mép phải), má hồng, mũi và miệng nhỏ; mép dưới gần phẳng |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_1\orig\N04.png` | Thân tròn nhỏ tím trắng (1024 × 1024, nền trắng): mảng nâu nhạt ở dưới trái là chỗ đuôi cá bắt đầu; mép trên hở vì đầu che |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_1\orig\N05.png` | Hai chân trước ngắn màu trắng (1024 × 1024, nền trắng): chân trái và chân phải buông thẳng, móng kem ở dưới; mép trên hở là chỗ nối vào thân |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_1\orig\N06.png` | Vây đuôi nâu nhạt hình hạt đậu có vân nâu (1024 × 1024, nền trắng): rủ xuống ở dưới trái, đầu trên phải là chỗ nối vào khúc đuôi |
| 7 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 hai sừng** (đổi dáng, viền khoảng 10 px):
- gốc hai sừng đúng chỗ gốc cũ, rộng như cũ; sừng to bên trái, sừng nhỏ bên phải, chóp chĩa lên hơi nghiêng trái như cũ;
- sừng bạc một màu xám bạc đều, ba bốn ngấn xám sẫm ngang, chóp nhọn; cỡ gần như cũ;
- không vẽ đầu, chỏm len, tai; không sừng nâu.

**N02 hai vây tai** (đổi dáng, viền khoảng 10 px):
- gốc mỗi tai đúng chỗ gốc cũ (tai trái gốc ở bên phải, tai phải gốc ở bên trái); tai trái mở sang trái, tai phải mở sang phải;
- mỗi tai là vây: màng cam san hô căng trên ba gân xanh mòng két tỏa từ gốc, mép ngoài lượn sóng, gân trên cùng xanh mòng két như concept; cỡ gần như tai cũ, to hơn chút được;
- không vẽ đầu, sừng; không tai thỏ hồng.

**N03 đầu có mặt** (giữ viền, viền khoảng 10 px):
- giữ viền ngoài đầu như cũ (hai bên, mép dưới); chỉ chỏm len kem được nhô lên khỏi mép trên một chút;
- lông ngắn xanh mòng két, mõm và cằm trắng kem, mũi xanh thẫm nhỏ, cười nhếch; chỏm len kem ba lọn nhọn trên trán, không xoáy;
- hai mắt hổ phách to (con ngươi đen, một chấm sáng) đúng chỗ mắt cũ, vệt mày xanh thẫm xếch xuống phía mũi;
- không má hồng; không vẽ sừng, tai, thân.

**N04 thân** (giữ viền, viền khoảng 23 px):
- giữ viền thân như cũ;
- thân xanh mòng két, bụng kem phía trước; dưới trái thon thành khúc đuôi cá xanh mòng két có vài vảy sẫm như concept;
- không vẽ đầu, chân, vây đuôi; không thân tím trắng.

**N05 hai chân trước** (giữ viền, viền khoảng 22 px):
- viền và chỗ hai chân như cũ; móng ở đầu dưới;
- chân xanh mòng két, móng xanh thẫm nhỏ;
- không vẽ thân, bụng kem; không móng kem.

**N06 vây đuôi** (đổi dáng, viền khoảng 16 px):
- đầu nối (trên phải) đúng chỗ cũ, vây rủ xuống như cũ, cỡ như cũ hoặc to hơn chút;
- vây cam san hô hình quạt, gân xanh mòng két tỏa từ chỗ nối, mép lượn, gốc xanh mòng két như concept;
- không vẽ thân, khúc đuôi có vảy; không vây nâu.

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
