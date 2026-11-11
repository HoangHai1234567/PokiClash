# Gói gửi GPT: dòng `phap_su` dạng 2 (pháp sư nước dạng 2)

Tướng thứ 6 đảo Thủy, làm 2026-11-11 theo ý người dùng: pháp sư nước bí ẩn, mũ che kín mặt. Màu và chi tiết là đề xuất của Claude, chờ người dùng duyệt. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/phap_su_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\phap_su_2\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\phap_su_2\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/phap_su_2/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\phap_su_1\tai_ve\L1_duyet.png` | Pháp sư nước dạng 1 đã duyệt (1536 × 1024, nền trắng): pháp sư lùn mũ chàm sụp kín mặt, áo lam ngọc, gậy ôm cầu nước |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ti_tach_1\tai_ve\L1_duyet.png` | Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam mắt bầu dục. Chỉ lấy nét bút rung, vân sáp, tô phẳng |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_den_1\tai_ve\L1_duyet.png` | Cá đèn lồng dạng 1 đã duyệt (1536 × 1024, nền trắng): cá hai chân màu chàm. Lấy độ ít chi tiết, mảng màu đậm vẫn có vân sáp |
| 4 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.

Chỗ lưu: `C:\Atomik\PokiWar\ArtGen\Spine\inbox\phap_su_2\tai_ve`. Bản được chọn chép thành `L1_duyet.png` cùng thư mục.

## Kiểm

- Cùng con, cùng bộ đồ, cùng màu với dạng 1 nhưng **cao lớn hẳn**: mũ chỉ còn chừng 1/3 chiều cao, áo dài gấp đôi; vẫn **không thấy mặt**.
- Chóp mũ và hai dải đai dài hơn; khăn vai có **cổ dựng** thấp; áo có một dải lam băng gần gấu; vạt trước dài.
- Áo choàng chàm **to dài hơn**, gấu bốn lượn sóng, có đường viền cam; tay áo trái buông dài, không thấy bàn tay.
- Gậy **cao hơn chóp mũ**, móc ngọn sóng to ôm cầu nước lớn, thêm **một cầu nhỏ** ở đầu móc, ba hạt vỏ sò treo.
- Gậy tách hẳn khỏi áo và vành mũ (khe trắng ≥ 45 px); tay cầm gậy hở khỏi thân; chóp mũ, dải đai không chạm gì.
- Tô phẳng, không bóng, không phát sáng; nền trắng tinh; không hiệu ứng; không bị cắt mép ảnh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng trên cầu nước | `Flat colour only: remove every shadow, highlight, shine spot, glow and gradient, also on the water orb and under the hat brim; keep the crayon hatching as texture only.` |
| Lộ mặt, có mắt hoặc chấm sáng dưới mũ | `The face must be completely hidden: under the hat brim only ONE flat night-navy shape, with no eyes, no glowing dots, no mouth, no skin.` |
| Gậy đè lên áo, vành mũ hoặc bắt chéo người | `Move the staff further to the right: it stands upright, at least 45 px of pure white between the pole and the robe and between the staff head and the hat brim; only the mitten hand touches it.` |
| Quay sang trái hoặc nhìn thẳng | `Turn the mage three-quarters toward the viewer's RIGHT: staff on the right, back cloak and the drooping hat tip on the left.` |
| Thành người (thấy chân, cổ, tóc, ngón tay) | `It is a small squat creature wrapped in clothes, not a human: no legs (only two boot tips under the hem), no neck, no hair, no fingers (one round mitten), chibi proportions with the hat almost half of the height.` |
| Quá nhiều chi tiết, hoa văn, nếp vải | `Simplify: plain cloth with two or three fold lines per piece, no patterns except the one drop emblem on the front panel, no extra belts, pouches, books or jewellery.` |
| Có lông vũ, cánh, sao, trăng, mắt trên mũ | `Remove them: the hat has only its band, one teardrop gem, the bead on its tip and two ribbon tails.` |
| Có nước, bong bóng, vòng phép quanh người | `Remove every effect: only the mage and its staff on pure white.` |
| Dạng 2 không cao hơn dạng 1 mấy | `Make form 2 clearly taller and more slender: the hat only one third of the height, the robe twice as long as in image 1, a taller staff with a bigger orb.` |
