# Gói gửi GPT: dòng `so_gai` dạng 1, lượt 2b: hàm dưới vẽ lại

Vẽ lại concept nhưng **chỉ còn mai dưới** (bỏ mai trên, bỏ lưỡi), thấy lòng bát tím và **vành trong phía xa** như cách con gốc tách hàm dưới. `so_gai.py cat` căn ảnh này trùng mai dưới của concept rồi lấy phần lòng bát + vành xa làm lớp sau lưỡi, và lấy chỗ vành bị lưỡi che (dạng 2) để vá mặt trước.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\so_gai_1\luot_2_ham_duoi.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_1\tai_ve\H01.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/so_gai_1/luot_2_ham_duoi.txt --timeout 420`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_1\tai_ve\L1_duyet.png` | Sò đột biến dạng 1 đã duyệt (1536 × 1024, nền trắng): lấy đúng mai dưới (cái bát có vành cam), giữ nguyên chỗ, cỡ |

## Kiểm

- Chỉ còn mai dưới, **đúng chỗ, đúng cỡ** như trong concept (chồng lên concept thì bát trùng nhau).
- Vành gần liền mạch từ bản lề tới đầu miệng, nanh dưới và gai còn đủ.
- Lòng bát tím than trơn, trống; phía sau là **vành xa** một cung trơn cao, mỏng hơn vành gần.
- Không còn gì của mai trên, không lưỡi; tô phẳng, nền trắng.

## GPT vẽ sai thì gửi thêm

| Sai | Gửi thêm |
|---|---|
| Còn sót mai trên, mắt, lưỡi | `Remove every remaining piece of the upper shell and the tongue; only the lower shell.` |
| Bát bị dời chỗ, đổi cỡ | `Keep the lower shell in exactly the same position and size as in image 1.` |
| Vành xa thấp, dẹt | `Raise the far rim: one big smooth arc, much higher above the near rim in the middle.` |
| Lòng bát có bóng, có thịt, có lưỡi | `The inside is flat dark plum and completely empty.` |
