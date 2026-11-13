# Gói gửi GPT: `cung_lua` (quỷ lửa bắn cung, tướng thứ 3 đảo Hỏa, tên chưa đặt)

Làm lại từ đầu 2026-11-13 theo lời người dùng: "xem con gốc tách như nào thì mình tách và gen như thế". Reskin trên con gốc `monster_3357`: mỗi tờ là các mảnh GỐC cắt ra từ rig (phóng to), GPT vẽ lại da từng mảnh đúng chỗ, đúng cỡ, đúng hình bóng. Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai. Ghi chú: `ArtGen/Spine/inbox/cung_lua_ghichu.md`.

## Tờ `A`: ngọn lửa (chùm lông mũ), mặt nạ mũ, vòm sau mũ + hai sừng, cây cung, mũi tên, ống tên

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\cung_lua_1\luot_1_da_A.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\tai_ve\D_A.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/cung_lua_1/luot_1_da_A.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\mau\goc_A.png` | Tờ mảnh gốc cắt từ rig con gốc (1536 × 1024, nền trắng), phóng 2,5–5 lần: ngọn lửa (chùm lông mũ), mặt nạ mũ, vòm sau mũ + hai sừng, cây cung, mũi tên, ống tên. Hình cel số màu lam xám, viền vàng |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\mau\concept_A.png` | Concept đã duyệt của mình (bản A, 1536 × 1024, nền trắng): chỉ lấy màu, chất liệu, nét vẽ tay |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\kiem_si_1\tai_ve\L1_duyet.png` | Voọc Tướng đã duyệt: chỉ lấy nét vẽ |

## Tờ `B`: giáp ngực, váy giáp, bao tay gần, cẳng tay xa, hai tấm vai, hai bắp tay, hông, hai đùi, hai ủng, bốn mảnh bàn tay

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\cung_lua_1\luot_1_da_B.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\tai_ve\D_B.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/cung_lua_1/luot_1_da_B.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\mau\goc_B.png` | Tờ mảnh gốc cắt từ rig con gốc (1536 × 1024, nền trắng), phóng 2,5–5 lần: giáp ngực, váy giáp, bao tay gần, cẳng tay xa, hai tấm vai, hai bắp tay, hông, hai đùi, hai ủng, bốn mảnh bàn tay. Hình cel số màu lam xám, viền vàng |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\mau\concept_A.png` | Concept đã duyệt của mình (bản A, 1536 × 1024, nền trắng): chỉ lấy màu, chất liệu, nét vẽ tay |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\kiem_si_1\tai_ve\L1_duyet.png` | Voọc Tướng đã duyệt: chỉ lấy nét vẽ |

## Kiểm

- Mỗi mảnh nằm ĐÚNG chỗ, đúng cỡ, đúng hình bóng mảnh gốc (chồng lên tờ mảnh gốc phải trùng); đủ số mảnh, không dính nhau.
- Da mới: giáp cháy nâu đen, mảng sẫm, lửa ba màu phẳng, khe mũ vàng sáng; không còn lam xám, viền vàng, chữ S đỏ; không bóng, không quầng sáng.
- Nét bút nâu rung, vân sáp; nền trắng tinh.

Cắt: `py -3 -I ArtGen/Spine/cung_lua_da.py cat` (in độ khớp hình bóng từng mảnh).

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Mảnh lệch chỗ / đổi cỡ | `Every part must stay at exactly the same place and size as in image 1; lay your picture over image 1 and check.` |
| Còn màu lam, viền vàng, chữ S | `Remove every blue-grey colour, gold trim and the red letter emblem: charred brown-black armour only.` |
| Tô khối, có bóng | `Flat colour only: no shading bands, no highlights, no gradients.` |

## Lượt 2: mũi tên lửa năng lượng của chiêu cuối (2026-11-13)

Người dùng: "mũi tên cuối trong chiêu cuối nên là 1 mũi tên lửa năng lực rực cháy, khác với mũi tên thường". Mảnh rời (con gốc không có).

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\cung_lua_1\luot_2_ten_lua.txt`. Ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\tai_ve\T_LUA.png` (trùng tên thì `_2`, `_3`…).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\tai_ve\D_A.png` | Tờ mảnh đã reskin của mình (1536 × 1024, nền trắng): ngọn lửa ba màu phẳng, mũ, cung, mũi tên thường thân sẫm đầu vàng, ống tên. Chỉ lấy nét vẽ và cách vẽ lửa |

Kiểm: một mũi tên toàn lửa nằm ngang chĩa phải, trục y = 512, đuôi tì dây ở x = 340, mũi ở (1390, 512); một hình kín viền mực; tô phẳng, không quầng sáng, không tàn lửa rời. Cắt: `py -3 -I ArtGen/Spine/cung_lua_da.py ten_lua_cat`.

## Dạng 1 (non), lượt 1: concept (2026-11-13)

Người dùng: "gen tiếp dạng 1 của tướng này". Dạng 1 làm trên CÙNG rig với dạng 2 (đổi tỉ lệ ở rig: đầu × 1,17, chùm lửa × 0,7), rồi chuyển da.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\cung_lua_1\non_luot_1_concept.txt`. Ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\non\tai_ve\C1.png` (trùng tên thì `C1_2.png`, `C1_3.png`...).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\non\mau\bo_cuc.png` | Hình bố cục dựng từ rig (1103 × 1376, nền trắng): con rối đứng dáng nghỉ quay phải, tỉ lệ dạng 1 (đầu to hơn, chùm lửa nhỏ hơn), còn mang da dạng 2 (hai sừng dài, giáp nứt lửa, cung có vân lửa). Cho dáng, tỉ lệ, chỗ và cỡ từng bộ phận. |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\kiem_si_1\tai_ve\L1_duyet.png` | Một tướng đã duyệt của game (1536 × 1024): chỉ lấy nét vẽ tay mực + chì sáp. |

Kiểm: đúng dáng và chỗ từng bộ phận như ảnh 1; hai sừng CỤT (chừng một phần tư), chùm lửa nhỏ hai màu, giáp trơn KHÔNG nứt lửa, cung trơn không vân lửa; mũ kín ba khe vàng; tô phẳng, không bóng, không quầng sáng; nền trắng, không viền sticker.

Câu sửa nhanh: "horns shorter and blunter", "remove the cracks of fire", "keep every part exactly where it is in image 1", "flat colour, no glow".

Duyệt xong Claude mới dựng lượt chuyển da (tờ part của dạng 2 xếp đúng ô, GPT chỉ đổi chi tiết).

## Dạng 1 (non), lượt 2: vòm mũ sừng cụt (2026-11-13)

Người dùng duyệt concept C1 ("dạng 1 ổn, làm đi"). Dạng 1 khác dạng 2 ở năm mảnh: ngực, găng lớn, cung (bỏ vết lửa) và chùm lửa (hai màu) sửa bằng mã (`py -3 -I ArtGen/Spine/cung_lua_non.py da`); chỉ vòm mũ + sừng phải gen lại.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\cung_lua_1\non_luot_2_sung.txt`. Ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\non\tai_ve\D_S.png` (trùng tên thì `D_S_2.png`, `D_S_3.png`...).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\non\mau\goc_S.png` | Một mảnh phóng to trên nền trắng (1536 × 1024): vòm sau mũ màu than sẫm (nửa dưới, có núm nhỏ) và hai sừng dài cong mọc từ đỉnh vòm, viền mực nâu. Mảnh của dạng 2. |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\cung_lua_1\non\tai_ve\C1.png` | Concept dạng 1 đã duyệt (ảnh dọc, nền trắng): chỉ xem hai mẩu sừng cụt trên mũ. |

Kiểm: vòm trùng khít vòm ảnh 1 (cùng chỗ, cùng cỡ); hai mẩu sừng cụt, tù, mọc đúng chỗ gốc sừng cũ, đỉnh khoảng y = 332; một hình kín viền mực; tô phẳng.

Câu sửa nhanh: "the dome must stay exactly where it is in image 1", "horn stubs shorter and blunter", "flat colour, no highlights".

Cắt: `py -3 -I ArtGen/Spine/cung_lua_non.py cat` → `inbox/cung_lua_1/non/manh/to_01.png`.
