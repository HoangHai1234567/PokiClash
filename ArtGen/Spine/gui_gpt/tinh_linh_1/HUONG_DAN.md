# Gói gửi GPT: `tinh_linh` dạng 1 (tinh linh rừng mập, tướng thứ 2 đảo Mộc, tên chưa đặt)

DẠNG 1 (làm sau dạng 2, cùng rig): một file prompt, thiết kế là đề xuất của Claude, chờ duyệt. Làm 2026-11-12, lượt 2: bản đầu bị trả ("nhìn giống con gốc quá"; mắt chỉ lòng trắng; mồm chỉ hiện khi bắn chiêu). Ba hướng thiết kế cho người dùng chọn một; màu và chi tiết là đề xuất của Claude. Thân, tay, mắt theo khung part của con gốc `monster_3407`; tóc và thứ trong bụng là mảnh riêng. Ghi chú: `ArtGen/Spine/inbox/tinh_linh_ghichu.md`.

Mỗi hướng một file prompt; **chỉ gửi GPT đường dẫn file**, GPT tự mở ảnh mẫu và tự lưu (trùng tên thì `_2`, `_3`…):

| Hướng | File prompt | Ảnh lưu ở |
|---|---|---|
| dạng 1: hạt mầm (thân lục nhạt, hạt chưa nứt trong bụng, một mầm cong tí hon trên đầu) | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\tinh_linh_1\luot_1_concept_hat.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tinh_linh_1\tai_ve\L1_hat.png` |

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tinh_linh_1/luot_1_concept_<hướng>.txt` (thêm `--note "..."` để sửa nhanh).

Lượt 2 (tờ mảnh theo khung part, mồm tròn lúc bắn chiêu, các bộ mắt) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).

Ảnh mẫu (ảnh 1 mỗi hướng một sơ đồ `bo_cuc_<hướng>.png`, cùng hình, khác màu):

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tinh_linh_1\mau\bo_cuc_hat.png` | Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): khối thân mập (bụng to, đầu vòm nhỏ hơn), tay trước hình hạt đậu bên trái, hai mắt bầu dục trắng trơn có vành màu, má hồng. Không có tóc, không có thứ trong bụng (tả bằng lời) |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tinh_linh_2\tai_ve\L1_duyet.png` | Concept dạng 2 đã duyệt (mầm hai lá; 1536 × 1024, nền trắng): cùng thân, cùng mắt, cùng nét. Dạng 1 là bản non hơn |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ti_tach_1\tai_ve\L1_duyet.png` | Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam, mắt bầu dục trống vành lam dày, má lam, không mồm. Lấy nét, vân sáp, tô phẳng và CÁCH VẼ MẮT |
| 4 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_voi_1\tai_ve\L1_duyet.png` | Cá voi biến dị dạng 1 đã duyệt (1536 × 1024, nền trắng): cá voi lam nhỏ. Lấy nét, tô phẳng, tông màu trầm |
| 5 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/tinh_linh.py bo_cuc`).

## Kiểm

- **Mập, mềm, tròn**: bụng to xệ ngồi bệt, đầu vòm nhỏ hơn đặt thẳng lên bụng, không cổ; đầu và bụng **liền một khối**. Không chân, không đuôi, không tai.
- Tay trước (bên trái người xem) hình hạt đậu mập, **đè lên** mép trái bụng, có viền kín riêng; tay sau chỉ lộ một dải hẹp ở mép phải.
- **Mắt chỉ lòng trắng**: hai bầu dục trắng trơn, vành dày màu thân đậm (không mực đen), không con ngươi, không chấm sáng. Má hồng. **Không có mồm** (mồm tròn chỉ hiện lúc bắn chiêu, làm ở lượt sau).
- Tóc và thứ trong bụng đúng hướng thiết kế của file (mầm hai lá + hạt giống / mũ nấm + bào tử / mũ rêu hai cành + lá kẹt); thứ trong bụng nhạt màu, nét mảnh không mực.
- Tô phẳng: **không** vệt bóng trắng, không phản chiếu, không bóng đổ; nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Vẽ con ngươi, chấm sáng trong mắt | `The eyes are completely blank: plain white ovals with a thick coloured rim. Remove the pupils and every dot.` |
| Vẽ mồm, mũi | `Remove the mouth and the nose: the face is only the two blank eyes and the two blush marks.` |
| Vẽ bóng loáng, vệt sáng trắng, kiểu thuỷ tinh / nước | `Flat colour only: remove every white shine mark, reflection, glossy highlight, darker rim and gradient; only the pale things inside the belly show that it is translucent.` |
| Gầy, cao, có cổ, có chân | `Make it much fatter and rounder: a huge sagging belly sitting flat on the ground, a smaller head dome directly on it with no neck, NO legs and NO feet.` |
| Đầu và bụng tách hai khối có nét mực chạy ngang | `The head and the belly are ONE jelly mass: remove the ink line across the middle; keep only a short soft fold line at each side.` |
| Thứ trong bụng đậm như bên ngoài, nét mực đen | `The things inside the belly are INSIDE the jelly: redraw them paler and washed out, with thin pencil outlines in the darker body tone, no ink.` |
| Thân lệch sơ đồ | `Follow image 1 exactly for the body: turned slightly to the viewer's right, the front arm at the left overlapping the belly, the eyes low on the head.` |
