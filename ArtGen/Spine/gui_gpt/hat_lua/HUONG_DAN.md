# Gói gửi GPT: hình hạt lửa, khói, dung nham (`hat_lua`)

Người dùng dặn 2026-11-10: hình hạt lửa, khói cho GPT vẽ cho đẹp. Hiệu ứng vẫn là hạt chồng lớp (`fxlib.py`, `bo_hoa.py`); GPT chỉ vẽ **hình của hạt**. H01–H05 là hình **xám, không viền** (game tự nhuộm màu và tự vẽ một viền mực ngoài cả khối); H06, H07 đủ màu, có viền.

**Chỉ gửi GPT đường dẫn file prompt:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\hat_lua\luot_1_hat.txt` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hat_lua\tai_ve`.

1. GPT vẽ H01. Gõ `next`: GPT vẽ H02. Nhắn Claude "soi hat_lua".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: H03, H04, H05, H06, H07.
3. Đủ ảnh thì nhắn Claude "nhập hat_lua" (Claude chạy `py -3 -I build_hat.py --nhap` rồi xuất lại bộ Hỏa).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\chuan_fx\hat_bo_cuc.png` | Bố cục mẫu (1024 vuông, nền trắng): lưới 2 × 2, mỗi ô một hình xám thô do máy vẽ; chỉ để GPT hiểu bố cục |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\chuan_fx\hat_dung_the_nao.png` | Một khung phun lửa của game (1080 × 928, sân Hỏa): cho GPT thấy game chồng nhiều hình, nhuộm màu, viền mực ngoài khối |

Mỗi ảnh: 1024 vuông, nền trắng tinh, lưới 2 × 2 bốn hình rời không chạm nhau, không chạm mép. Kiểm từng ảnh:

- **H01** khói (xám, KHÔNG viền): bốn cụm khói hoạt hình khác nhau: mỗi cụm là 3–6 bướu tròn chồng nhau, mép xù tròn, một cụm tròn, một cụm bè, một cụm cao, một cụm lổn nhổn
- **H02** cụm lửa tròn (xám, KHÔNG viền): bốn cụm lửa tròn: mỗi cụm là khối tròn mập, mép gợn mềm, có 1–3 ngọn lửa ngắn tròn đầu nhô lên phía trên, đáy rộng
- **H03** lưỡi lửa móc câu (xám, KHÔNG viền): bốn lưỡi lửa rời chĩa thẳng lên: đáy tròn mập, thân cong chữ S, ngọn nhọn quặp sang một bên như móc câu (hai cái quặp trái, hai cái quặp phải)
- **H04** lưỡi lửa xoắn (xám, KHÔNG viền): bốn lưỡi lửa trang trí kiểu phương Đông chĩa lên: ngọn kết thúc bằng một vòng xoắn ốc chặt, bên hông có 1–2 xoắn nhỏ
- **H05** giọt và vệt dung nham (xám, KHÔNG viền): hàng trên: hai giọt chất lỏng đặc bay lên (khối tròn mập, đuôi thon ngắn phía dưới, một giọt nhỏ bên cạnh); hàng dưới: hai vệt toé dẹt trên mặt đất nhìn chếch thấp (vũng bầu dục rộng gấp ba chiều cao, 3–4 lưỡi toé ngắn, hai giọt nhỏ)
- **H06** hạt nhỏ có màu (đủ màu, viền mực khoảng 10 px): bốn hạt nhỏ: trên trái tia lửa bay sang phải (vệt thuôn dài, đuôi nhọn trái, đầu tròn phải, vàng lõi kem); trên phải cục than hồng (khối tròn méo nhỏ, cam giữa vàng); dưới trái sao bốn cánh (vàng tâm kem); dưới phải ba mảnh tro dẹt (hai đen than, một xám tro)
- **H07** đá dung nham (đủ màu, viền mực khoảng 12 px): bốn cục đá núi lửa góc cạnh màu tím than (khoảng #48394A), có vài khe nứt mảnh tô cam lõi vàng (màu phẳng, không phát sáng), bốn dáng khác nhau

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| H01–H05 có viền mực hoặc mép sẫm | `No outline at all: only the flat grey crayon fill, the edge is just where the grey stops.` |
| H01–H05 có màu (đỏ, cam...) | `Only neutral grey, no colour: the game tints the grey itself.` |
| Có bóng, mảng sáng tối, quầng sáng | `FLAT, NO LIGHT, NO SHADOW: every area one even colour, the strokes are texture only. No shading, no darker side, no shadows of any kind (nothing on the background), no white highlights or shine spots, no gloss, no glow or halo, no gradients, no 3D render.` |
| Hình chạm nhau, chạm mép | `Four separate shapes, one centred in each quarter, with clear white gaps between them and around the edge.` |
| Không giống vẽ tay | `Draw it by hand on paper with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |

Gói sinh từ `C:\Atomik\PokiWar\ArtGen\Spine\build_hat.py`; sửa prompt ở đó rồi chạy lại.
