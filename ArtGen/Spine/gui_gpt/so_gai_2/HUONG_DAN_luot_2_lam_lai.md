# Gói gửi GPT: dòng `so_gai` dạng 2, lượt 2 làm lại (mảnh theo cách tách của con gốc)

Mỗi file prompt một ảnh. **Chỉ gửi GPT đường dẫn từng file**; GPT tự mở ảnh mẫu và tự lưu (trùng tên thì `_2`, `_3`…; `so_gai2.py cat` lấy bản mới nhất).

| File prompt | Ảnh ra | Là gì |
|---|---|---|
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\so_gai_2\luot_2_mai_tren.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_2\tai_ve\U01.png` | mai trên riêng, đúng chỗ đúng cỡ, không mắt, vành liền, nanh treo |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\so_gai_2\luot_2_mai_duoi.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_2\tai_ve\D01.png` | mặt trước mai dưới riêng, đúng chỗ đúng cỡ, phía trên vành là nền trắng |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\so_gai_2\luot_2_to_manh.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_2\tai_ve\P01.png` | tờ 6 mảnh: vòm tím (dự phòng), mắt mở, mắt nhắm, lưỡi nằm, môi chu, lưỡi dài |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\so_gai_2\luot_2_ham_duoi_sau.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_2\tai_ve\B01.png` | nửa sau của hàm dưới: mặt trong vỏ màu tối cùng tông vỏ (KHÔNG tím), mép trên và mép trước là vành xa màu cam; đúng chỗ đúng cỡ |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\so_gai_2\luot_2_luoi_nam.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_2\tai_ve\T01.png` | lưỡi nằm trọn vẹn, đúng chỗ đúng cỡ (dùng thay ô D của tờ mảnh) |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\so_gai_2\luot_2_chop_luoi.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_2\tai_ve\T02.png` | chóp lưỡi vắt qua mép, mảnh nhỏ vẽ trước mai dưới: nửa tròn, mép trên là nếp gấp thẳng, không có đuôi |

Ảnh mẫu (cả ba file): `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_2\tai_ve\L1_duyet.png` (concept đã duyệt, 1536 × 1024, nền trắng, con sò miệng hé).

## Kiểm

- U01, D01: chồng lên concept thì trùng khít; mỗi mảnh một hình kín, không còn gì của mảnh kia, không có vùng tím.
- U01 không còn mắt, mày; chỗ mắt là màu mai trơn có gân.
- P01 đủ sáu mảnh rời, cách nhau, mỗi mảnh viền mực kín; tô phẳng.
- B01: thấp, mép trên chạy ngay sau vành trên của concept (không hở khe nào giữa hai vành), có vành cam ở mép trên và mép trước, lòng màu tối cùng tông vỏ, không tím, không có gì bên trong.
- T01, T02 (dạng 2): chồng lên concept thì phần thấy được trùng khít; phần khuất nối trơn, một hình kín.

## GPT vẽ sai thì gửi thêm

| Sai | Gửi thêm |
|---|---|
| Mảnh bị dời chỗ, đổi cỡ | `Keep the part in exactly the same position and size as in image 1.` |
| Còn mắt trên mai trên | `Remove the eyes and brows completely; plain shell colour and ribs there.` |
| Còn vùng tím, lưỡi, vành xa | `Remove every dark plum area and the tongue; pure white there.` |
| Có bóng, điểm sáng | `Flat colour only: no shading, no highlights.` |
