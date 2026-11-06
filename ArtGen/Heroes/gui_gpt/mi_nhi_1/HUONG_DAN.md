# Gói gửi GPT: Mi Nhi dạng 1/2 (Tiểu Mi, `mi_nhi_1`)

Tướng Khá hệ Thủy (ải 15 đảo Thủy), dạng 1/2, rig aola #983. Thiết kế: tiên cá nhỏ chơi đàn dạng người (người dùng chốt 2026-11-06: giữ tiên cá dạng người): bé gái chibi tóc tím oải hương, mái và lọn tóc cuộn bọt trắng ở ngọn, một lọn tóc dựng cong trên đỉnh; vây tai xanh nhạt gân tím viền trắng ngọc; kẹp vỏ sò hồng giữ ngọc trai trắng; da hồng nhạt, mắt xanh sapphire to, mày xếch quả quyết; áo vảy vỏ sò hồng nhạt; tay mũm mĩm đeo vòng ngọc trai; đàn lia nhỏ bằng san hô trắng hồng, dây bạc, ngọc trai trên đỉnh, đế vỏ ốc hồng; đuôi cá xanh ngọc bích vảy chấm đậm, vây tím nhạt. Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT tự lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\mi_nhi_1\tai_ve\`). Claude xem rồi đặt tên và chép vào đúng chỗ.

Viền trắng kiểu giấy xé quanh tướng do game vẽ bằng shader; GPT không vẽ viền đó.

## Lượt 1: concept

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\mi_nhi_1\luot_1_concept.txt`. Gửi trong **chat mới**. GPT vẽ một ảnh cả con trên rig, lưu vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\mi_nhi_1\tai_ve\concept.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\Silhouette.png` | Bóng xám của con gốc trên nền trắng (543 × 547): con gốc #983 là bé tiên cá chibi nhìn thẳng hơi quay phải: đầu rất to, mái tóc dày, hai lọn tóc hai bên mặt, một lọn tóc dựng cong trên đỉnh vắt sang phải, tóc dài phía sau xõa xuống dưới trái, một vây tai to sau bên trái đầu, kẹp sao ở trên trái đầu; thân nhỏ dưới đầu; hai tay ngắn với sang phải gảy cây đàn lia nhỏ dựng ở bên phải; dưới là đuôi cá ngắn cuộn ở dưới, vây nhỏ chĩa trái. Bỏ khỏi bóng xám: bóng dưới chân và vòng sao |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\RegionMap.png` | Cùng hình, tô màu từng vùng và đánh số (543 × 547, nền trắng): 1 vây tai, 2 tóc trên đầu (mái, lọn hai bên, lọn dựng trên đỉnh), 3 tóc dài phía sau, 4 mặt, 5 kẹp tóc, 6 thân, 7 tay sau, 8 tay trước, 9 đàn lia, 10 đuôi cá |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style\style_sheet.png` | Tờ mẫu thiết kế (1536 × 1024, nền trắng): 8 tướng aola ở khung đứng đầu (rùa ngọc, rùa biển ngọc, huyền vũ, sư tử lửa con, heo lửa, mèo máy, tiểu tướng mũ sừng, cá ngựa). Chỉ học cách thiết kế, không lấy nét bóng, không chép con nào |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\style_anchor.png` | Ảnh mốc style (1143 × 1376, nền trắng): concept Giọt Sương dạng 1 đã chốt, tinh linh nước đội mũ giáp bạc cầm kiếm. Chỉ lấy nét mực và vân chì sáp; không lấy thiết kế, không lấy chấm sáng trắng và mảng tối của nó |

Xong thì nhắn Claude "duyệt concept mi_nhi_1". Duyệt xong Claude lưu `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\mi_nhi_1\concept_duyet.png` và chạy lại `build.py` để có file prompt lượt 2.

## Lượt 2: nhóm mảnh

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\mi_nhi_1\luot_2_nhom_manh.txt`. Gửi cùng chat với lượt 1 hoặc chat mới. GPT lưu mỗi nhóm thành `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\mi_nhi_1\tai_ve\<mã nhóm>.png`.

1. GPT vẽ N02. Gõ `next`: GPT vẽ N06. Nhắn Claude "soi thử mi_nhi_1".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N01, N03, N04, N05, N07, N08.
3. Đủ ảnh thì nhắn Claude "ghép mi_nhi_1".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\orig\N01.png` | Vây tai xanh lam đậm có gân (1024 × 1024, nền trắng): mép phải dựng đứng là gốc (nằm sau đầu), các gân xòe ra trái, chóp nhọn ở trên trái và dưới |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\orig\N02.png` | Mặt chibi (1024 × 1024, nền trắng): da hồng, hai mắt xanh lá to (mắt trái to hơn), miệng nhỏ há, hơi quay phải; tóc là nhóm khác |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\orig\N03.png` | Tóc xanh ngọc trên đầu (1024 × 1024, nền trắng): mái dày trùm trán, hai lọn ngắn hai bên mặt, một lọn dài dựng trên đỉnh cong sang phải, kẹp sao vàng ở trên trái; chỗ trống ở giữa dưới là chỗ của mặt |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\orig\N04.png` | Tóc dài xanh ngọc phía sau (1024 × 1024, nền trắng): mảng lớn lượn sóng bên trái, ngọn nhọn ở dưới trái; lọn nhỏ hơn bên phải; mép trên là chỗ mọc từ sau đầu |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\orig\N05.png` | Thân chibi nhỏ (1024 × 1024, nền trắng, khung rộng): trên là da hồng (vai, ngực), dưới là dải xanh và vảy xanh lam |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\orig\N06.png` | Hai tay hồng ngắn với sang phải (1024 × 1024, nền trắng, khung rộng): tay sau ở trên, tay trước ở dưới có bàn tay nhỏ ở đầu phải; đầu trái của mỗi tay là vai |
| 7 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\orig\N07.png` | Đàn lia vàng nhỏ (1024 × 1024, nền trắng): khung chữ S, cuộn tròn ở trên phải và ở dưới trái, dây xanh ngọc, đế tròn cam ở dưới trái |
| 8 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\refs\thuy\mi_nhi_1\orig\N08.png` | Đuôi cá xanh lam ngắn (1024 × 1024, nền trắng): vây nhỏ chĩa trái ở trên trái, chóp đuôi cong xuống thành mũi nhọn ở dưới phải; mép trên là chỗ nối thân |
| 9 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\mi_nhi_1\concept_duyet.png` | concept đã duyệt của dạng này (nền trắng) |

Kiểm từng ảnh trước khi lưu:

**N01 vây tai** (đổi dáng, viền khoảng 16 px):
- gốc (mép phải) đúng chỗ cũ, vây xòe ra trái như cũ, cỡ như cũ hoặc to hơn chút;
- vây xanh nhạt, gân tím nhạt, viền trắng ngọc mảnh;
- không vẽ đầu, tóc; không xanh lam đậm.

**N02 mặt** (đổi dáng, viền khoảng 13 px):
- mặt đúng chỗ, đúng cỡ cũ; hai mắt đúng chỗ hai mắt cũ, miệng đúng chỗ cũ;
- da hồng nhạt, mắt xanh sapphire to, mày xếch quả quyết, cười nhỏ;
- không vẽ tóc (mái tóc phủ lên mặt ở nhóm N03); không mắt xanh lá.

**N03 tóc trên đầu và kẹp tóc** (đổi dáng, viền khoảng 9 px):
- mái, hai lọn hai bên, lọn dựng trên đỉnh đúng chỗ, đúng hướng, cỡ như cũ; chỗ trống cho mặt như cũ;
- tóc tím oải hương, ngọn cuộn bọt trắng nhỏ;
- chỗ kẹp sao: kẹp vỏ sò hồng giữ ngọc trai trắng;
- không vẽ mặt, vây tai, tóc dài phía sau; không tóc xanh ngọc, không sao.

**N04 tóc dài phía sau** (đổi dáng, viền khoảng 9 px):
- hai mảng tóc đúng chỗ, đúng hướng; mép trên (chỗ mọc sau đầu) đúng chỗ cũ;
- tóc tím oải hương lượn sóng, ngọn cuộn bọt trắng;
- không vẽ đầu, mặt, vây tai; không tóc xanh ngọc.

**N05 thân** (giữ viền, viền khoảng 15 px):
- viền thân như cũ;
- da hồng nhạt ở trên, áo ngắn bằng vảy vỏ sò hồng nhạt chồng lên nhau ở dưới;
- không vẽ đầu, tay, đuôi.

**N06 hai tay** (giữ viền, viền khoảng 21 px):
- viền và chỗ hai tay như cũ; vai ở đầu trái, bàn tay ở đầu phải;
- tay mũm mĩm da hồng nhạt, vòng ngọc trai mảnh ở cổ tay trước;
- không vẽ đàn, thân.

**N07 đàn lia san hô** (đổi dáng, viền khoảng 21 px):
- khung đàn đúng đường cong cũ, cuộn trên phải và dưới trái đúng chỗ, đế ở dưới trái; cỡ như cũ;
- khung bằng san hô trắng ánh hồng, dây bạc, ngọc trai trắng ở cuộn trên, đế là vỏ sò điệp hồng như concept;
- không vẽ bàn tay; không vàng, không cam.

**N08 đuôi cá** (giữ viền, viền khoảng 16 px):
- viền đuôi và vây như cũ; vây chĩa trái, chóp đuôi cong xuống phải;
- vảy xanh ngọc bích có chấm đậm, vây tím nhạt;
- không vẽ thân, chân; không xanh lam.

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
