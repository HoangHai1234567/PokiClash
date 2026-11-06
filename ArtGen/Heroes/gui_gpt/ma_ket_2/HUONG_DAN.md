# Gói gửi GPT: Ma Kết dạng 2/3 (Ma Kết Sừng Nhọn, `ma_ket_2`)

Tướng Hiếm hệ Thủy (ải 20 đảo Thủy, mini boss), dạng 2/3, rig aola #759. Thiết kế: dê biển trẻ, lớn lên từ dạng 1: cùng lông xanh mòng két, mõm kem dài hơn, mắt hổ phách, vệt mày xếch; sừng bạc dài nhọn có ngấn; vây tai cam san hô to hơn; túm len má và chỏm len trắng kem nhọn (chỏm hất sang phải như ngọn sóng); ngực kem đeo vỏ sò điệp hồng san hô trên vòng bạc (mảnh giáp đầu tiên); chân khỏe móng chẻ xanh thẫm; đuôi cá xanh mòng két vảy xanh thẫm, vây đuôi to cam san hô. Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_2\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\ma_ket_2\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_2\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_2\Silhouette.png` | Bóng xám của con gốc trên nền trắng (713 × 779): con gốc #759 là dê biển đứng trên hai chân trước, nhìn ba phần tư quay phải: đầu trắng, hai sừng tím hồng nhọn (sừng trái to vươn lên trái, sừng phải nhỏ chĩa lên), một tai hồng ở trên trái đầu, túm lông má bên trái, chỏm lông nhọn trên phải đầu, mắt xanh ngọc; thân trắng tím nhạt, hai chân trước móng tím (chân trái trước, chân phải sau), đuôi cá xanh ngọc sau thân, vây đuôi to hai thùy ở bên trái. Bỏ khỏi bóng xám: bóng |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_2\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (713 × 779, nền trắng): 1 sừng trái to, 2 sừng phải nhỏ, 3 tai, 4 đầu có mặt, 5 túm lông má trái, 6 chỏm lông trên phải đầu, 7 thân, 8 chân trước trái và móng, 9 chân trước phải và móng, 10 đuôi cá, 11 vây đuôi |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_1\concept_duyet.png` | Concept đã duyệt của `ma_ket_1` (1095 × 1436, nền trắng): dạng 1, dê biển con: lông xanh mòng két, mõm kem, chỏm len kem, sừng bạc ngắn có ngấn, vây tai và vây đuôi cam san hô, mắt hổ phách. Giữ màu, sừng, vây tai, mặt, nét vẽ |

Xong thì nhắn Claude "duyệt concept ma_ket_2". Duyệt xong Claude lưu `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_2\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\ma_ket_2\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_2\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N03. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi thử ma_ket_2".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N01, N04, N05, N06.
3. Đủ ảnh thì nhắn Claude "ghép ma_ket_2".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_2\orig\N01.png` | Hai sừng tím hồng (1024 × 1024, nền trắng): sừng trái to (gốc rộng ở dưới phải, cong lên tới chóp ở trên trái), sừng phải nhỏ (gốc ở dưới, chóp ở trên); đầu không có trong ảnh |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_2\orig\N02.png` | Một tai dê dài lòng hồng (1024 × 1024, nền trắng): chĩa lên trái, chóp ở đầu trái, gốc (mép hở) ở đầu phải là chỗ nối vào đầu |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_2\orig\N03.png` | Đầu trắng quay phải (1024 × 1024, nền trắng): hai mắt xanh ngọc, mũi và miệng nhỏ; túm lông má trắng nhọn ở bên trái, chỏm lông nhọn trắng tím ở trên phải |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_2\orig\N04.png` | Thân mập tím trắng (1024 × 1024, nền trắng): mảng ngực trắng, vệt lông nhỏ; mép trên phải hở vì đầu che |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_2\orig\N05.png` | Hai chân trước (1024 × 1024, nền trắng): chân trái thẳng xuống, chân phải chĩa xuống phải; chân tím trắng, móng chẻ tím sẫm ở dưới; mép trên hở là chỗ nối vào thân |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\ma_ket_2\orig\N06.png` | Đuôi cá xanh ngọc (1024 × 1024, nền trắng): khúc đuôi dày ở bên phải (giấu sau thân), vây to hai thùy ở bên trái (thùy trên chĩa lên, thùy dưới chĩa trái) |
| 7 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\ma_ket_2\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 hai sừng** (đổi dáng, viền khoảng 10 px):
- gốc hai sừng đúng chỗ gốc cũ, rộng như cũ; sừng to vươn lên trái, sừng nhỏ chĩa lên như cũ;
- sừng bạc một màu xám bạc đều, bốn năm ngấn xám sẫm ngang, chóp nhọn như concept; cỡ gần như cũ;
- không vẽ đầu, chỏm len, tai; không sừng tím.

**N02 vây tai** (đổi dáng, viền khoảng 11 px):
- gốc tai (đầu phải) đúng chỗ gốc cũ; vây mở lên trái như tai cũ, to hơn tai cũ được như concept;
- màng cam san hô căng trên ba gân xanh mòng két tỏa từ gốc, mép trên là gân xanh mòng két dày, mép ngoài lượn sóng;
- không vẽ đầu, sừng, túm len; không tai dê lòng hồng.

**N03 đầu, mặt, túm len má, chỏm len** (giữ viền, viền khoảng 11 px):
- giữ viền ngoài đầu như cũ; túm len má ở bên trái và chỏm len ở trên phải đúng chỗ cũ, cỡ như cũ;
- đầu lông xanh mòng két, mõm và cằm trắng kem, mũi xanh thẫm nhỏ, cười nhếch; túm len má kem lọn nhọn chĩa trái; chỏm len kem lọn nhọn hất sang phải;
- hai mắt hổ phách to (con ngươi đen, một chấm sáng) đúng chỗ mắt cũ, vệt mày xanh thẫm xếch;
- không má hồng; không vẽ sừng, tai, thân, vỏ sò.

**N04 thân** (giữ viền, viền khoảng 21 px):
- giữ viền thân như cũ;
- thân xanh mòng két, ngực trắng kem mép lông xù ở phía trước bên phải;
- trên ngực, ngay dưới cằm: vỏ sò điệp nhỏ hồng san hô nhạt gân kem treo trên vòng bạc như concept;
- không vẽ đầu, chân, đuôi; không thân tím trắng.

**N05 hai chân trước** (giữ viền, viền khoảng 18 px):
- viền và chỗ hai chân như cũ; móng ở đầu dưới;
- chân xanh mòng két, móng chẻ xanh thẫm;
- không vẽ thân, ngực kem; không móng tím.

**N06 đuôi cá và vây** (giữ viền, viền khoảng 13 px):
- viền khúc đuôi và vây như cũ; hai thùy chĩa đúng hướng cũ;
- khúc đuôi xanh mòng két vảy cong xanh thẫm; vây cam san hô, gân xanh mòng két dọc mỗi thùy, mép trước xanh mòng két như concept;
- không vẽ thân, chân; không vây xanh ngọc.

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
