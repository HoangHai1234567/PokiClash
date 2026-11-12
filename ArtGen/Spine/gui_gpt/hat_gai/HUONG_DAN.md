# Gói gửi GPT: hình hạt gai xương rồng (gai, cụm gai trồi, dăm gai) (`hat_gai`)

Người dùng dặn 2026-11-10: hình hạt cho GPT vẽ cho đẹp. Hiệu ứng vẫn là hạt chồng lớp (`fxlib.py`, `bo_hoa.py`, `bo_thuy.py`); GPT chỉ vẽ **hình của hạt**. Bước ghi "xám, KHÔNG viền" là hình game tự nhuộm màu và tự vẽ một viền mực ngoài cả khối; bước ghi "đủ màu" thì có viền.

**Chỉ gửi GPT đường dẫn file prompt:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\hat_gai\luot_1_hat.txt` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hat_gai\tai_ve`.

1. GPT vẽ G01. Gõ `next`: GPT vẽ G02. Nhắn Claude "soi hat_gai".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: G03.
3. Đủ ảnh thì nhắn Claude "nhập hat_gai" (Claude chạy `py -3 -I build_hat.py --nhap hat_gai` rồi xuất lại bộ).
   Hoặc Claude tự gen: `py -3 -I gen.py gui_gpt/hat_gai/luot_1_hat.txt --steps G01,G02,G03`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\chuan_fx\hat_bo_cuc.png` | Bố cục mẫu (1024 vuông, nền trắng): lưới 2 × 2, mỗi ô một hình xám thô do máy vẽ; chỉ để GPT hiểu bố cục |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_2\tai_ve\L1_duyet.png` | Concept Cầu Gai dạng 2 đã duyệt (1536 × 1024, nền trắng): xương rồng cầu lục sẫm, gai kem nón mập mũi nhọn; chỉ lấy dáng gai và vân sáp |

Mỗi ảnh: 1024 vuông, nền trắng tinh, lưới 2 × 2 bốn hình rời không chạm nhau, không chạm mép. Kiểm từng ảnh:

- **G01** gai (xám, KHÔNG viền): bốn cái gai xương rồng rời, mũi chĩa thẳng lên, gốc ở dưới: một nón mập ngắn gốc phình tròn, một kim dài mảnh rất nhọn, một gai vừa mũi hơi cong như vuốt, một gai lùn mập; mỗi cái một khối đặc gốc tròn một mũi nhọn
- **G02** cụm gai trồi (xám, KHÔNG viền): bốn CỤM gai trồi lên từ đất nhìn ngang: đế thấp rộng, 4–6 gai nhọn dài ngắn khác nhau xoè lên và ra hai bên như vương miện gai (gai giữa cao nhất); một cụm cao hẹp, một cụm bè thấp, một cụm ngả trái, một cụm ngả phải; mỗi cụm một khối liền
- **G03** dăm gai (xám, KHÔNG viền): bốn mảnh dăm gai gãy rời: một đầu gai gãy (mũi nhọn ngắn, đầu kia nham nhở), một dăm mảnh hai đầu nhọn, một mẩu ba góc dày, một mảnh cong ngắn; góc cạnh, sắc, khác nhau rõ

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| H01–H05 có viền mực hoặc mép sẫm | `No outline at all: only the flat grey crayon fill, the edge is just where the grey stops.` |
| H01–H05 có màu (đỏ, cam...) | `Only neutral grey, no colour: the game tints the grey itself.` |
| Có bóng, mảng sáng tối, quầng sáng | `FLAT, NO LIGHT, NO SHADOW: every area one even colour, the strokes are texture only. No shading, no darker side, no shadows of any kind (nothing on the background), no white highlights or shine spots, no gloss, no glow or halo, no gradients, no 3D render.` |
| Hình chạm nhau, chạm mép | `Four separate shapes, one centred in each quarter, with clear white gaps between them and around the edge.` |
| Không giống vẽ tay | `Draw it by hand on paper with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |

Gói sinh từ `C:\Atomik\PokiWar\ArtGen\Spine\build_hat.py`; sửa prompt ở đó rồi chạy lại.
