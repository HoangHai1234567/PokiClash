# Gói gửi GPT: mảnh của `quy_dao_non` (Viêm Đao dạng 1), lượt 2

Làm 2026-11-14 (máy ổ D) sau khi concept B được chọn. Mỗi tờ một file prompt; ảnh mẫu duy nhất là concept chốt.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\quy_dao_non\tai_ve\L1_duyet.png` | Concept dạng 1 đã chốt (1536 × 1024, nền trắng): quỷ lửa con đầu tròn to mặt nạ sắt đen, hai sừng mầm, ba búi lửa tạt sang trái, giáp vai vòm, đao lớn một lưỡi dựng chéo sau lưng |

## Tờ `DAU`: đầu quả cầu mặt nạ (không sừng), vẽ đủ phần bị giáp vai, sừng, bàn tay che; đúng chỗ, đúng cỡ

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\quy_dao_non\luot_2_manh_DAU.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\quy_dao_non\tai_ve\N_DAU.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_dao_non/luot_2_manh_DAU.txt --timeout 420`

## Tờ `DAO`: cây đao trọn vẹn (không bàn tay, không bị đầu che); đúng chỗ, đúng cỡ, đúng góc

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\quy_dao_non\luot_2_manh_DAO.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\quy_dao_non\tai_ve\N_DAO.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_dao_non/luot_2_manh_DAO.txt --timeout 420`

## Tờ `LUA`: ba búi lửa vẽ RỜI nhau, mỗi búi đủ cả gốc; cùng cỡ, cùng hướng như trên concept

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\quy_dao_non\luot_2_manh_LUA.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\quy_dao_non\tai_ve\N_LUA.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_dao_non/luot_2_manh_LUA.txt --timeout 420`

## Kiểm

- `DAU`: chỉ còn cái đầu, đúng chỗ cũ (đặt chồng lên concept thì trùng), tròn kín, KHÔNG sừng, đủ mào ba mũi + hai mắt vàng.
- `DAO`: chỉ còn cây đao, đúng chỗ, đúng góc; cán liền từ khâu tròn tới chắn tay (không bàn tay), dải lưỡi cam chạy suốt lưỡi sắc.
- `LUA`: đúng ba búi, rời nhau, mũi nhọn bên trái, gốc bo tròn bên phải, ba vùng màu phẳng, viền lửa mềm (không răng cưa).
- Tô phẳng, không bóng, không quầng sáng; nền trắng.

## GPT vẽ sai thì gửi thêm

| Sai | Gửi thêm |
|---|---|
| Mảnh bị dời / đổi cỡ | `Keep the piece at exactly the same position, size and angle as in image 1: laid over image 1 it must coincide.` |
| Còn sót bộ phận khác | `Only that one piece remains; everything else is pure white.` |
| Ba búi lửa dính nhau | `The three flame locks must be separate, with at least 40 px of white between them.` |
