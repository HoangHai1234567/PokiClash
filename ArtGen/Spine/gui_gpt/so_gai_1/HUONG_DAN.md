# Gói gửi GPT: dòng `so_gai` dạng 1 (sò đột biến dạng 1)

Tướng thứ 4 đảo Thủy, làm 2026-11-11 theo ý người dùng: sò đột biến có mắt ở mai trên, có lưỡi. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/so_gai_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\so_gai_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/so_gai_1/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ti_tach_1\tai_ve\L1_duyet.png` | Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam mắt bầu dục. Chỉ lấy nét bút rung, vân sáp, tô phẳng |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\vay_lam_1\tai_ve\L1_lien.png` | Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Lấy cách vẽ nanh, mắt dữ, nét mặt quả quyết |
| 3 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.

## Kiểm

- Con sò tròn gần như quả bóng, **hai mai rời nhau**, bản lề bên trái, miệng hé về bên **phải**; hai mai không chồng lên nhau.
- Mai trên lam lục có gân quạt, **hai mắt vàng con ngươi dọc** nằm trên mai trên (mắt gần to, mắt xa hẹp), mày mực xếch.
- Vành mép hai mai là dải cam lượn sóng; ba nanh kem thả xuống từ mép trên, hai nanh nhỏ dựng lên từ mép dưới, **không chạm mép đối diện**.
- Bốn gai cam trên mai trên (một gai to trên đỉnh), ba gai trên mai dưới; hai u hà kem ở lưng.
- Trong miệng tím than, **lưỡi hồng mập nằm trong miệng**, không thò ra ngoài.
- Tô phẳng: **không** bóng, không điểm sáng (trừ chấm mắt), không ánh xà cừ; viền mực nâu; nền trắng tinh; không có ngọc trai, bong bóng.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng, ánh xà cừ | `Flat colour only: remove every shadow, highlight, shine spot, pearly sheen and gradient; keep the crayon hatching as texture only.` |
| Hai mai dính liền hoặc chồng lên nhau | `The upper shell and the lower shell are two separate solid pieces touching only at the hinge on the left; open the mouth wider so a dark gap separates the two rim bands all the way from the middle to the right.` |
| Mắt nằm ở mai dưới hoặc trong miệng | `Both eyes sit on the outside of the UPPER shell, above its rim band.` |
| Nanh, gai chạm hoặc đè lên mai đối diện | `Shorten the fangs and move the spikes so that nothing of one shell touches or crosses the other shell.` |
| Quay sang trái hoặc nhìn thẳng | `Turn the clam three-quarters toward the viewer's RIGHT: hinge on the left, mouth opening and both eyes on the right.` |
| Có tay, chân, ngọc trai, bong bóng, nước | `Remove them: only the two shell halves, eyes, fangs, spikes, barnacles and the tongue, on pure white.` |
| Dạng 2 không khác dạng 1 mấy | `Make form 2 much bigger in the frame, with a darker navy upper shell, a crown of three big spikes, longer fangs and a scar.` |
