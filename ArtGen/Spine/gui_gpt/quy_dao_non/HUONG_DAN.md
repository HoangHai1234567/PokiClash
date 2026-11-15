# Gói gửi GPT: `quy_dao_non` (Viêm Đao dạng 1, quỷ lửa con chibi vác đao; suất `giap_long` đảo Hỏa)

Làm 2026-11-14 (máy ổ D). Người dùng: "làm dạng 1 cho tướng thứ 7 đảo hỏa". Hai hướng là đề xuất của Claude, chờ người dùng chọn. Ghi chú: `ArtGen/Spine/inbox/quy_dao_ghichu.md` mục 8.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\quy_dao_non\mau\bo_cuc.png` | Hình bố cục dựng từ rig dạng 2 đổi tỉ lệ xương (1536 × 1024, nền trắng): quỷ con đầu to, hai sừng mầm, bờm lửa nhỏ, đao ngắn; ghép thô từ mảnh dạng 2 (lửa còn răng cưa, giáp vai còn gai). Lấy chỗ đặt, cỡ từng bộ phận |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\quy_dao_1\tai_ve\L1_duyet.png` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): quỷ lửa da tro, mặt nạ + giáp sắt đen, sừng đen, bờm và râu lửa, đao lớn một lưỡi. Lấy loài, màu, chất liệu, nét vẽ |

## Hướng `theo_bo_cuc`: theo hình bố cục: chỗ đặt từng bộ phận giữ như rig đổi tỉ lệ, vẽ lại thành một con chibi hẳn hoi (đầu khoảng 45 %)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\quy_dao_non\luot_1_concept_theo_bo_cuc.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\quy_dao_non\tai_ve\L1_theo_bo_cuc.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_dao_non/luot_1_concept_theo_bo_cuc.txt` (thêm `--note "..."` để sửa nhanh).

## Hướng `tron_hon`: chibi mạnh hơn: đầu gần nửa chiều cao, thân tròn lùn như củ khoai, tay chân ngắn hẳn, đao ngắn bè như dao phay

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\quy_dao_non\luot_1_concept_tron_hon.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\quy_dao_non\tai_ve\L1_tron_hon.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_dao_non/luot_1_concept_tron_hon.txt` (thêm `--note "..."` để sửa nhanh).

## Kiểm

- Chibi thật: đầu gần nửa chiều cao (không tính đao), thân tròn lùn, tay chân ngắn; vẫn mặt "chiến" (mày đè xuống mắt), không cười.
- Cùng loài với dạng 2: da tro nhạt, mặt nạ + giáp sắt đen, sừng đen than, vải đỏ sẫm, đao thép xám lam có dải lưỡi cam.
- Hai **sừng mầm** ngắn (lành lặn); bờm lửa **nhỏ, ba búi**; **không râu lửa**; giáp vai vòm tròn **không gai**.
- **Đao một lưỡi** ngắn và bè (khâu tròn ở chuôi, bản loe về mũi, sống có một khấc), vẫn to quá khổ so với con non.
- Nhìn sang phải, tay xa vòng lên sau đầu nắm cán đao, mũi đao chống đất bên phải; tay chân dính thân; từng khối có viền kín.
- Tô phẳng, không bóng, không quầng sáng; nền trắng.

## GPT vẽ sai thì gửi thêm

| Sai | Gửi thêm |
|---|---|
| Chưa đủ chibi | `Make it more chibi: the head must be about half of the whole height, the body shorter and rounder, the arms and legs shorter.` |
| Mặt cười / hiền | `Not cute-smiling: the heavy brow of the mask comes down over the eyes, a determined fierce look, no mouth.` |
| Sừng dài / có râu lửa / giáp vai có gai | `Only two short horn buds, NO fire beard under the mask, NO spike on the shoulder guard.` |
| Đao thành kiếm | `The weapon is a DAO: one cutting edge only, blade widening toward a slanted clipped tip, thick back with one notch, small oval guard, ring pommel. No cross-guard.` |
| Quay sang trái | `The creature FACES THE VIEWER'S RIGHT: mask at the right, fire hair streaming to the left.` |
