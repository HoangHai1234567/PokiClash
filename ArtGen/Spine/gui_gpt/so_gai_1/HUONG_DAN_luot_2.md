# Gói gửi GPT: dòng `so_gai`, lượt 2: tờ mảnh (dùng chung dạng 1 và 2)

Hai mai (kèm mắt, nanh, gai, u hà) **không** nhờ GPT vẽ lại: cắt thẳng từ concept đã duyệt bằng `ArtGen/Spine/so_gai.py` (khớp concept 100 %). GPT chỉ vẽ thứ concept không có đủ: lưỡi duỗi thẳng (để quật), lòng miệng (lộ ra khi há to), môi chu (chiêu nhổ ngọc), hai mí mắt, viên ngọc trai (đạn của lớp VFX).

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\so_gai_1\luot_2_manh.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_1\tai_ve\M01.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/so_gai_1/luot_2_manh.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_1\tai_ve\L1_duyet.png` | Sò đột biến dạng 1 đã duyệt (1536 × 1024, nền trắng): sò tròn mai lam lục, vành cam, mắt vàng, lưỡi hồng trong miệng tím. Lấy màu, nét, vân sáp, tỉ lệ |

## Kiểm

- Năm mảnh rời trên nền trắng: nửa trên là **lưỡi duỗi thẳng nằm ngang** (dài ~1150 px, gốc bên trái tù tròn, chóp bên phải mập tròn, một đường giữa đậm); nửa dưới bốn mảnh xếp hàng.
- Lòng miệng: nửa hình tròn tím than trơn, đáy phẳng. Môi chu: vòng môi cam mập như bánh vòng, lỗ tím nhỏ lệch phải, vài nếp nhăn toả quanh lỗ.
- Hai mí: mảng lam lục **không viền mực**, mỗi mảng một nét mực nhắm mắt (trái: chéo xuống phải; phải: chéo xuống trái).
- Ngọc trai: viên tròn trắng xà cừ, một vệt lưỡi liềm tím nhạt, viền mực; không bóng sáng.
- Không vẽ con sò, không nhãn chữ, không khung ô; tô phẳng, không bóng.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Vẽ cả con sò hoặc mai | `Draw only the five loose parts on pure white; remove the clam and its shells.` |
| Lưỡi cong, cuộn hoặc ngắn | `The tongue is perfectly straight and horizontal, about 1150 px long, root on the left, rounded tip on the right.` |
| Mí mắt có viền mực quanh mảng | `The eyelid patches have NO outline around them: only flat teal with one ink stroke across each.` |
| Có nhãn chữ, số, khung ô | `Remove every label, number, frame and grid line.` |
| Ngọc trai, môi có bóng sáng | `Flat colour only: no highlights, no shine, no pearly sheen.` |
