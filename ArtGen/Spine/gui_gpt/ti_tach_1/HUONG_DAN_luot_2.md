# Gói gửi GPT: dòng `ti_tach`, lượt 2: tờ nét mặt và miệng (dùng chung dạng 1 và 2)

Thân, mắt mở, vệt má và các giọt con **không** nhờ GPT vẽ lại: cắt thẳng từ concept đã duyệt bằng `ArtGen/Spine/ti_tach.py` (khớp concept 100 %). GPT chỉ vẽ thứ concept không có: mắt lúc trúng đòn, choáng, cười, chớp, và miệng há để bắn nước.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\ti_tach_1\luot_2_net_mat.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ti_tach_1\tai_ve\M01.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ti_tach_1/luot_2_net_mat.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ti_tach_1\tai_ve\L1_duyet.png` | Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt vòm lam, hai mắt bầu dục trắng viền lam. Chỉ lấy kiểu nét, cỡ và khoảng cách hai mắt |

## Kiểm

- Sáu nhóm rời trên nền trắng, mỗi ô một nhóm, không chạm nhau; **không** vẽ thân, không vệt má, không nhãn chữ.
- Bốn cặp mắt: `> <` · bầu dục có xoáy · `^ ^` bo tròn · hai nét cong nhắm mắt. Trong mỗi cặp, **bên trái to hơn** (mắt gần), bên phải hẹp hơn (mắt xa), tâm cách nhau khoảng 205 px.
- Hai miệng: chữ `o` nhỏ lòng xanh chàm; miệng há to hình trứng đứng, viền lam dày, lòng xanh chàm, có u lưỡi lam.
- Nét lam đậm dày, hơi rung như sáp, cùng kiểu viền mắt trong concept; tô phẳng, không bóng, không điểm sáng.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Vẽ cả thân hoặc nền lam sau các mảnh | `Draw only the loose face parts on pure white: remove the body, the blue background shapes and the cheek marks.` |
| Có nhãn chữ, số, khung ô | `Remove every label, number, frame and grid line; only the six groups on pure white.` |
| Hai mắt trong cặp bằng nhau | `In every pair the LEFT symbol is the bigger near eye (about 125 x 160 px) and the RIGHT symbol is the narrower far eye (about 80 x 145 px).` |
| Nét mảnh hoặc đều như vector | `Thicker strokes, about 12 px, slightly wobbly like a wax crayon, round ends.` |
| Miệng có răng, có bóng, có điểm sáng | `The mouth is a flat dark-navy opening with a thick deep-blue ring and a small flat blue tongue bump: no teeth, no shading, no shine.` |
