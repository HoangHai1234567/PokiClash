# Gói gửi GPT: dòng `ran_sung` dạng 2 (rắn nước có sừng dạng 2)

Tướng thứ 5 đảo Thủy, làm 2026-11-11 theo ý người dùng: rắn nước có hai sừng đen, chót đuôi là sừng đen nhọn kiểu kunai. Màu thân là đề xuất của Claude, chờ người dùng duyệt. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/ran_sung_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\ran_sung_2\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_2\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ran_sung_2/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_1\tai_ve\L1_duyet.png` | Rắn sừng dạng 1 đã chọn (1536 × 1024, nền trắng): rắn con lam cô-ban cuộn một vòng, sừng đen, sừng đen ở chót đuôi |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ti_tach_1\tai_ve\L1_duyet.png` | Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam mắt bầu dục. Chỉ lấy nét bút rung, vân sáp, tô phẳng |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\vay_lam_1\tai_ve\L1_lien.png` | Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Lấy cách vẽ mắt dữ, nét mặt quả quyết |
| 4 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.

Chỗ lưu: `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_2\tai_ve`. Bản được chọn chép thành `L1_duyet.png` cùng thư mục.

## Kiểm

- Cùng con với dạng 1 nhưng **dài, to, dữ hơn**: không còn chibi (đầu chừng 1/4 chiều cao), **hai vòng cuộn**, cổ dựng cao chữ S.
- Lưng **chàm đậm**, hàng vảy nhọn lam trên sống cổ, nhiều đốm bong bóng hơn.
- Sừng dài hơn hẳn, mỗi sừng **một nhánh nhọn**; **hai nanh kem** lộ ra dù miệng khép; mắt hẹp, mày rất dày.
- Sừng đuôi **to hơn, mỗi bên hai ngạnh** ở gốc; đuôi dựng cao bên phải, tách hẳn khỏi cổ.
- Tô phẳng, không bóng, nền trắng tinh; chỗ thân đè nhau có viền mực rõ.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng trên sừng | `Flat colour only: remove every shadow, highlight, shine spot and gradient, also on the black horns; keep the crayon hatching as texture only.` |
| Đuôi đè lên cổ, đầu hoặc chạm sừng | `Move the raised tail further to the right: at least 60 px of pure white between the tail horn and the neck, head and horns.` |
| Chót đuôi mềm như vây, lá, chùm lông | `The tail ends in a HARD black horn growing seamlessly out of the tail: a slender curved leaf shape with a needle-sharp tip, stiff like a horn.` |
| Chót đuôi thô như con dao gắn vào (có cán, vòng, hình thoi thẳng) | `The tail horn is not a knife or a separate object: remove the handle, ring and collar; it grows out of the tail through a zigzag edge, with smooth flowing hand-drawn curves and a gently curved tip, only hinting at a kunai.` |
| Đầu nhìn nghiêng, mõm chìa ngang, miệng cười dài | `Redraw the head seen from the FRONT and slightly from above, chin tucked in, looking at the viewer: an egg-shaped snake head with one big eye on each side, the snout at the bottom, and a small low mouth shaped like an upside-down V with a little point in the middle. No smile, no long muzzle.` |
| Sừng có nhánh, có lông, hoặc thành tai | `The two head horns are plain smooth charcoal-black cones, slightly curved, sharp tips, no branches, no fur, not ears.` |
| Thân cuộn rối, nhiều chỗ đè nhau | `Simplify the body: ONE flat loop on the ground only; the neck stands in front of it; the tail leaves to the right. No other crossing.` |
| Quay sang trái hoặc nhìn thẳng | `Turn the snake three-quarters toward the viewer's RIGHT: snout and both eyes on the right side of the head, tail raised on the right.` |
| Có tay, chân, vây, râu, lưỡi thè, nước | `Remove them: only the snake body, head, eyes, two horns and the tail horn, mouth closed, on pure white.` |
| Dạng 2 không khác dạng 1 mấy | `Make form 2 much longer and bigger in the frame, adult proportions with a smaller head, a deep navy back, two coils, long pronged horns, visible fangs and a larger barbed tail horn.` |
