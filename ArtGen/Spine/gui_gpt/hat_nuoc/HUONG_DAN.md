# Gói gửi GPT: hình hạt nước (sóng cuộn, giọt, nước toé, bọt) (`hat_nuoc`)

Người dùng dặn 2026-11-10: hình hạt cho GPT vẽ cho đẹp. Hiệu ứng vẫn là hạt chồng lớp (`fxlib.py`, `bo_hoa.py`, `bo_thuy.py`); GPT chỉ vẽ **hình của hạt**. Bước ghi "xám, KHÔNG viền" là hình game tự nhuộm màu và tự vẽ một viền mực ngoài cả khối; bước ghi "đủ màu" thì có viền.

**Chỉ gửi GPT đường dẫn file prompt:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\hat_nuoc\luot_1_hat.txt` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hat_nuoc\tai_ve`.

1. GPT vẽ N01. Gõ `next`: GPT vẽ N02. Nhắn Claude "soi hat_nuoc".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: N03, N04.
3. Đủ ảnh thì nhắn Claude "nhập hat_nuoc" (Claude chạy `py -3 -I build_hat.py --nhap hat_nuoc` rồi xuất lại bộ).
   Hoặc Claude tự gen: `py -3 -I gen.py gui_gpt/hat_nuoc/luot_1_hat.txt --steps N01,N02,N03,N04`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\chuan_fx\hat_bo_cuc.png` | Bố cục mẫu (1024 vuông, nền trắng): lưới 2 × 2, mỗi ô một hình xám thô do máy vẽ; chỉ để GPT hiểu bố cục |
| 3 | `C:\Atomik\PokiWar\Assets\03 Art\Fx\no_nuoc.png` | Vụ nước toé đã duyệt của game (512 × 505, nền trong): mũi nước nhọn mập, bọt tròn; chỉ lấy dáng hình |
| 4 | `C:\Atomik\PokiWar\Assets\03 Art\Fx\xoay_nuoc.png` | Vòng nước xoáy đã duyệt của game (384 × 362, nền trong): ba dòng nước mào sóng cuộn; chỉ lấy dáng mào sóng |

Mỗi ảnh: 1024 vuông, nền trắng tinh, lưới 2 × 2 bốn hình rời không chạm nhau, không chạm mép. Kiểm từng ảnh:

- **N01** sóng cuộn (xám, KHÔNG viền): bốn lưỡi nước rời dựng thẳng lên như sóng nhỏ đang đổ nhìn ngang: chân tròn mập, thân dày cong, ngọn cuộn tròn sang một bên như mào sóng (hai cái cuộn trái, hai cái cuộn phải), một hai cái có thêm cuộn nhỏ ở vai
- **N02** giọt nước (xám, KHÔNG viền): bốn giọt nước rời hình giọt lệ, đuôi nhọn chĩa thẳng lên, bụng tròn ở dưới: một giọt mập ngắn, một giọt dài thon, một giọt vừa đuôi hơi cong, một giọt nhỏ tròn đuôi rất ngắn
- **N03** nước toé (xám, KHÔNG viền): hàng trên: hai vương miện nước nhìn ngang (đế thấp rộng, 5–7 lưỡi nước nhọn cao thấp khác nhau vươn lên và ngả ra ngoài); hàng dưới: hai vụ nước toé tròn nhìn thẳng (7–9 mũi nước nhọn bo tròn toả từ tâm), mỗi hình một khối liền
- **N04** bọt nước (xám, KHÔNG viền): bốn cụm bọt biển: mỗi cụm 5–8 bong bóng tròn to nhỏ dính nhau (bướu tròn rõ, như bọt trắng trên mào sóng), một cụm tròn, một cụm bè, một cụm cao, một cụm nhỏ

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| H01–H05 có viền mực hoặc mép sẫm | `No outline at all: only the flat grey crayon fill, the edge is just where the grey stops.` |
| H01–H05 có màu (đỏ, cam...) | `Only neutral grey, no colour: the game tints the grey itself.` |
| Có bóng, mảng sáng tối, quầng sáng | `FLAT, NO LIGHT, NO SHADOW: every area one even colour, the strokes are texture only. No shading, no darker side, no shadows of any kind (nothing on the background), no white highlights or shine spots, no gloss, no glow or halo, no gradients, no 3D render.` |
| Hình chạm nhau, chạm mép | `Four separate shapes, one centred in each quarter, with clear white gaps between them and around the edge.` |
| Không giống vẽ tay | `Draw it by hand on paper with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |

Gói sinh từ `C:\Atomik\PokiWar\ArtGen\Spine\build_hat.py`; sửa prompt ở đó rồi chạy lại.
