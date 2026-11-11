# Gói gửi GPT: dòng `ti_tach` dạng 1 (Tí Tách)

Tướng khởi đầu hệ Thủy (ải 1 đảo Thủy), làm lại 2026-11-11 theo ý người dùng: giọt nước dáng vòm, mắt bầu dục trắng viền lam. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/ti_tach_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\ti_tach_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ti_tach_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ti_tach_1/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\vay_lam_1\tai_ve\L1_lien.png` | Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Chỉ lấy nét bút, vân sáp, cách tô phẳng |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\canh_cut_1\tai_ve\L1_lien.png` | Cánh Cụt dạng 1 đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi. Lấy độ đơn giản, tròn trịa của dạng 1 |
| 3 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.

## Kiểm

- Một khối nước **dáng vòm** đáy bằng, rộng hơn cao (~1,4 lần), hơi lệch như thạch mềm; không chóp nhọn, không tay chân đuôi.
- Mắt là **hai hình bầu dục đứng, trắng lam nhạt, viền lam đậm dày, trống trơn** (không tròng, không chấm); mắt gần to, mắt xa hẹp sát mép phải; dưới mỗi mắt một vệt má lam. **Không có miệng.**
- **Hai giọt con** tròn bay trên đỉnh, lệch trái, không chạm thân, không chạm nhau.
- Vài đốm bong bóng lam nhạt bên trong thân, phía dưới trái.
- Nhìn nghiêng 3/4 sang **phải**; không nước toé, không vũng nước.
- Tô phẳng: **không** bóng, không điểm sáng, không kiểu thạch trong suốt bóng loáng; viền mực nâu; nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng trắng trên thân | `Flat colour only: remove every shadow, highlight, shine spot, darker rim and gradient; keep the crayon hatching as texture only.` |
| Thành thạch trong suốt bóng loáng | `The body is an opaque flat aqua colour with crayon texture, not glassy jelly: no reflections, no transparency, no shine.` |
| Mắt có tròng, có chấm sáng, có mày | `The eyes are completely empty ovals: very pale ice-blue fill and a thick deep blue ring, nothing inside, no pupils, no dots, no brows.` |
| Có miệng | `Remove the mouth: the face is only the two oval eyes and the two cheek marks.` |
| Quay sang trái hoặc nhìn thẳng | `Turn the creature three-quarters toward the viewer's RIGHT: both eyes on the right half of the dome, the far eye narrower and close to the right edge.` |
| Có chóp nhọn, tay, chân, đuôi | `The body is only a smooth dome: remove the tip, arms, legs, feet and tail.` |
| Giọt con dính thân hoặc dính nhau, có nước toé | `The beads float clear of the body and of each other with white space around each; remove every splash, drip and extra drop.` |
| Dạng 2 không to hơn hẳn dạng 1 | `Make the dome much bigger and heavier in the frame (about 860 px wide, 640 px tall) and the eyes smaller relative to the body.` |
