# Gói gửi GPT: dòng `ca_den` dạng 1, lượt 2: hình há miệng

Con gốc há miệng bằng cách đổi sang một hình miệng há vẽ riêng (hai hàm khít nhau ở mép bên kia). GPT vẽ lại đúng concept, chỉ đổi miệng; `ArtGen/Spine/ca_den.py` khớp ảnh này vào concept rồi chỉ lấy vùng miệng và hàm dưới.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\ca_den_1\luot_2_ha_mieng.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_den_1\tai_ve\M01.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ca_den_1/luot_2_ha_mieng.txt` (thêm `--note "..."`).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_den_1\tai_ve\L1_duyet.png` | cá đèn lồng dạng 1 (chưa đặt tên) đã duyệt (1536 × 1024, nền trắng), miệng khép |

## Kiểm

- Mọi thứ ngoài miệng **giữ nguyên chỗ, nguyên cỡ**: hai mắt, cần đèn, vây lưng, vây bên, đuôi, chân (chồng lên concept phải trùng).
- Miệng há thành **một hốc tròn khép kín**: môi trên chàm vồng lên, vành hàm kem võng xuống.
- **Mép bên kia (bên phải)**: môi trên và hàm dưới **gặp nhau, khít lại bên trong viền thân**; bên phải mép là dải má (chàm trên, kem dưới). Thịt hồng **không chạm viền ngoài**.
- Vòm môi **nằm dưới mắt**, không đè lên mắt.
- Trong miệng: hồng mận phẳng, họng sẫm ở giữa, lưỡi hồng có viền. Răng dưới đứng trên vành hàm; hàng răng trên nhỏ chĩa xuống.
- Tô phẳng, không bóng, không nước dãi, không hiệu ứng; nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Con vật bị dời, đổi cỡ, đổi dáng | `Do not re-pose: the eyes, the lantern, the fins, the tail and the legs must be in exactly the same place and size as in image 1; change only the mouth and the lower jaw.` |
| Thịt hồng chạy ra tới viền bên phải | `Close the far corner: on the right the indigo upper lip curves down and the cream jaw rim curves up and they meet INSIDE the body; a band of cheek skin (indigo above, cream below) separates the mouth from the right outline.` |
| Miệng đè lên mắt | `Lower the upper lip arch: at least 15 px of indigo skin between each eye and the mouth opening; the mouth opens mostly downward.` |
| Có bóng, điểm sáng, nước dãi | `Flat colours only, no shading, no highlights, no drool or spit.` |
