# Gói gửi GPT: `phap_lua_non` (Viêm Sư dạng 1, pháp sư lửa con chibi; suất `hong_lien` đảo Hỏa)

Làm 2026-11-14 (máy ổ D). Người dùng: "suất 6 cho vào game rồi làm thêm dạng 1". Hai hướng là đề xuất của Claude. Ghi chú: `ArtGen/Spine/inbox/phap_lua_ghichu.md` mục 9.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\mau\bo_cuc.png` | Hình bố cục dựng từ rig dạng 2 đổi tỉ lệ xương (1536 × 1024, nền trắng): mũ trùm to, áo đỏ và váy lửa ngắn, trượng ngắn có cầu lửa bên trái, hai bàn tay vuốt lơ lửng; ghép thô từ mảnh dạng 2 (tóc và áo choàng còn dài). Lấy chỗ đặt, cỡ từng bộ phận |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_1\tai_ve\L1_duyet.png` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): pháp sư lửa mũ trùm than viền vàng, mắt lửa, tóc khói ngà, áo đỏ cháy thành lửa, trượng có cầu lửa. Lấy loài, màu, chất liệu, nét vẽ |

## Hướng `theo_bo_cuc`: theo hình bố cục: chỗ đặt từng bộ phận giữ như rig đổi tỉ lệ, vẽ lại thành một con chibi hẳn hoi (mũ trùm khoảng 45 % chiều cao)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\phap_lua_non\luot_1_concept_theo_bo_cuc.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\L1_theo_bo_cuc.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/phap_lua_non/luot_1_concept_theo_bo_cuc.txt` (thêm `--note "..."` để sửa nhanh).

## Hướng `tron_hon`: chibi mạnh hơn: mũ trùm tròn như quả chuông chiếm nửa người, thân áo bé xíu, trượng ngắn như đũa phép

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\phap_lua_non\luot_1_concept_tron_hon.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\L1_tron_hon.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/phap_lua_non/luot_1_concept_tron_hon.txt` (thêm `--note "..."` để sửa nhanh).

## Kiểm

- Chibi thật: mũ trùm gần nửa chiều cao, thân áo bé, váy lửa ngắn; vẫn mặt "chiến" (hai mắt lửa xếch chúi vào giữa), không cười.
- Cùng loài với dạng 2: mũ trùm than viền vàng có viên ngọc vàng, trong mũ tối đen chỉ có hai mắt lửa, tóc khói ngà, áo đỏ dây vàng.
- Tóc **ít** (hai ba búi ngắn), áo choàng vai **ngắn**, trượng **ngắn** có cầu lửa nhỏ trong móc vuốt; không khói.
- Hai bàn tay vuốt nhỏ **lơ lửng** (cổ tay là búi khói ngà), không có cánh tay; không chân, váy lửa thay chân.
- Nhìn sang phải, trượng bên trái người xem; từng khối có viền kín.
- Tô phẳng, không bóng, không quầng sáng; nền trắng.

## GPT vẽ sai thì gửi thêm

| Sai | Gửi thêm |
|---|---|
| Chưa đủ chibi | `Make it more chibi: the hood must be about half of the whole height, the robe tiny, the flame skirt short, the staff shorter.` |
| Mặt cười / hiền | `Not cute-smiling: two slanted fierce fire eyes tilted down toward the middle, no mouth, no face.` |
| Có mặt người / da | `Inside the hood there is NO face: only flat darkness and two eyes of fire.` |
| Có cánh tay / chân | `The hands FLOAT, joined to nothing (a puff of pale smoke as the wrist); no arms, no legs, no feet: a short skirt of flames under the robe.` |
| Tóc, áo choàng dài như dạng 2 | `Much less hair (two or three short tufts) and only a small collar-cape with one short tail.` |

## Lượt 2: mảnh, gen đúng chỗ đúng cỡ từ concept dạng 1 (2026-11-14)

Concept chốt: `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\L1_duyet.png` (hướng A, phiên chính chọn). Mỗi tờ vẽ lại concept, chỉ giữ một vài mảnh ĐÚNG CHỖ, ĐÚNG CỠ và vẽ đủ phần khuất. Cắt: `py -3 -I ArtGen/Spine/phap_lua_non.py cat`. Tay, cầu lửa, lưỡi lửa, khói dùng lại mảnh dạng 2.

### `dau_lua`: chỉ còn mũ trùm (trên) và váy lửa (dưới), mỗi thứ vẽ đủ phần khuất

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\phap_lua_non\luot_2_manh_dau_lua.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\M_dau_lua.png` (trùng tên thì `_2`, `_3`…).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\L1_duyet.png` | Concept dạng 1 đã chốt (1536 × 1024, nền trắng): pháp sư lửa con mũ trùm to, mắt lửa, hai búi tóc khói ngà, cổ áo choàng than viền vàng có đuôi nhọn, áo đỏ dây vàng, váy lửa, trượng ngắn có cầu lửa, hai bàn tay vuốt |

### `than`: chỉ còn thân: cổ áo choàng than viền vàng + áo đỏ + dây vàng, một mảnh liền, vẽ đủ phần bị mũ, tay, trượng che

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\phap_lua_non\luot_2_manh_than.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\M_than.png` (trùng tên thì `_2`, `_3`…).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\L1_duyet.png` | Concept dạng 1 đã chốt (1536 × 1024, nền trắng): pháp sư lửa con mũ trùm to, mắt lửa, hai búi tóc khói ngà, cổ áo choàng than viền vàng có đuôi nhọn, áo đỏ dây vàng, váy lửa, trượng ngắn có cầu lửa, hai bàn tay vuốt |

### `toc_duoi`: chỉ còn hai búi tóc khói ngà (trên đỉnh mũ, bên phải mũ) và cái đuôi áo choàng nhọn bên trái, mỗi thứ vẽ đủ phần khuất

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\phap_lua_non\luot_2_manh_toc_duoi.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\M_toc_duoi.png` (trùng tên thì `_2`, `_3`…).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\L1_duyet.png` | Concept dạng 1 đã chốt (1536 × 1024, nền trắng): pháp sư lửa con mũ trùm to, mắt lửa, hai búi tóc khói ngà, cổ áo choàng than viền vàng có đuôi nhọn, áo đỏ dây vàng, váy lửa, trượng ngắn có cầu lửa, hai bàn tay vuốt |

### `truong`: chỉ còn cây trượng (khung trượng than đen), KHÔNG có cầu lửa, không lửa, không bàn tay; vẽ đủ phần bị tay và cầu lửa che

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\phap_lua_non\luot_2_manh_truong.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\M_truong.png` (trùng tên thì `_2`, `_3`…).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\phap_lua_non\tai_ve\L1_duyet.png` | Concept dạng 1 đã chốt (1536 × 1024, nền trắng): pháp sư lửa con mũ trùm to, mắt lửa, hai búi tóc khói ngà, cổ áo choàng than viền vàng có đuôi nhọn, áo đỏ dây vàng, váy lửa, trượng ngắn có cầu lửa, hai bàn tay vuốt |

Kiểm: mảnh nằm đúng chỗ concept (chồng lên phải trùng phần lộ), mỗi mảnh một hình kín viền mực, phần khuất đã vẽ đủ, không dính thứ khác; trượng không còn cầu lửa và bàn tay.
