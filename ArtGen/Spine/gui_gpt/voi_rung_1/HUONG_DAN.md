# Gói gửi GPT: `voi_rung` dạng 1 (voi con của ma mút rừng, tướng thứ 5 đảo Mộc)

Làm 2026-11-12 sau khi rig dạng 2 xong. Hình dạng 1 là ĐỀ XUẤT của Claude (hai hướng), chờ người dùng chọn. Ghi chú: `ArtGen/Spine/inbox/voi_rung_ghichu.md`.

## Hướng `ao_choang`: áo choàng lá non ngắn (hai tầng), bụng và chân để trần, mầm xoắn trên đầu

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_1_concept_ao_choang.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\L1_ao_choang.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/voi_rung_1/luot_1_concept_ao_choang.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_2\tai_ve\L1_duyet.png` | Dạng 2 đã duyệt (1536 × 1024, nền trắng): ma mút rừng áo lá lục sẫm xếp tầng, da đá lam, hai ngà rễ gỗ màu mật cuộn to, nhìn ba phần tư sang phải. Lấy loài, góc nhìn, kiểu lá, nét và cách tô |

## Hướng `nam_la`: ụ lá non tròn phủ gần kín thân (ba tầng) như dạng lớn, mầm xoắn trên u vai

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_1_concept_nam_la.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\L1_nam_la.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/voi_rung_1/luot_1_concept_nam_la.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_2\tai_ve\L1_duyet.png` | Dạng 2 đã duyệt (1536 × 1024, nền trắng): ma mút rừng áo lá lục sẫm xếp tầng, da đá lam, hai ngà rễ gỗ màu mật cuộn to, nhìn ba phần tư sang phải. Lấy loài, góc nhìn, kiểu lá, nét và cách tô |

## Lượt 1b: người dùng chọn hướng B (`nam_la`) 2026-11-12

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_1b_to_phang.txt`. GPT lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\L2.png` (trùng tên thì `_2`, `_3`…).

Ảnh mẫu duy nhất: `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\L1_nam_la.png` (bản nháp hướng B, 1536 × 1024, nền trắng: voi con ụ lá non tròn ba tầng, mái lá che trán, mắt hổ phách to, ngà mới nhú, mầm xoắn trên lưng). Vẽ lại y hệt, chỉ đổi lá về tô phẳng: hai tầng trên và mái lá lục tươi, tầng dưới cùng + lá đuôi + mầm lục vàng, không chuyển màu.

Kiểm: đặt chồng lên bản nháp phải khít mọi nét; không còn chuyển màu trên lá. Bản đạt chép thành `tai_ve/L1_duyet.png`.

## Lượt 2: mảnh (đúng chỗ, đúng cỡ như concept đã duyệt)

| File prompt (chỉ gửi GPT đường dẫn này) | Ảnh mẫu | Ảnh ra | Là gì |
|---|---|---|---|
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_2_ao.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\L1_duyet.png` (Voi con đã duyệt (1536 × 1024, nền trắng): ụ lá non tròn ba tầng, mái lá che trán, mắt hổ phách to, vòi ngắn, hai ngà mới nhú, mầm xoắn trên lưng) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\B01.png` | ụ lá của thân kèm mầm xoắn (bỏ đầu, vòi, ngà, bốn chân, đuôi) |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_2_dau.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\L1_duyet.png` (Voi con đã duyệt (1536 × 1024, nền trắng): ụ lá non tròn ba tầng, mái lá che trán, mắt hổ phách to, vòi ngắn, hai ngà mới nhú, mầm xoắn trên lưng) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\H01.png` | đầu: mái lá + mặt + mắt + vòi (bỏ hai ngà nhú và túm rêu, thân, chân) |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_2_nga.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\L1_duyet.png` (Voi con đã duyệt (1536 × 1024, nền trắng): ụ lá non tròn ba tầng, mái lá che trán, mắt hổ phách to, vòi ngắn, hai ngà mới nhú, mầm xoắn trên lưng) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\T01.png` | hai ngà mới nhú, mỗi ngà kèm túm rêu ở gốc (ngà xa vẽ đủ phần bị che) |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_2_chan.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\L1_duyet.png` (Voi con đã duyệt (1536 × 1024, nền trắng): ụ lá non tròn ba tầng, mái lá che trán, mắt hổ phách to, vòi ngắn, hai ngà mới nhú, mầm xoắn trên lưng) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\G01.png` | ba chân (chân ngoài cùng bên trái, chân thứ hai từ trái, chân trước to bên phải) vẽ đủ phần bị lá che + đuôi |

Kiểm: đặt chồng lên ảnh mẫu thì phần giữ lại phải khít; mỗi mảnh / lớp một hình kín viền mực; nền trắng tinh; không bóng.

## Lượt 3: tách lớp lá (ảnh mẫu là ảnh mảnh lượt 2)

| File prompt (chỉ gửi GPT đường dẫn này) | Ảnh mẫu | Ảnh ra | Là gì |
|---|---|---|---|
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_3_la_day.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\B01.png` (Ảnh mảnh ụ lá của thân voi con (B01, 1536 × 1024, nền trắng): hai tầng lá lục tươi, tầng dưới cùng lục vàng, mầm xoắn) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\C01.png` | tầng lá dưới cùng (lục vàng) vẽ đủ phần bị lá trên che |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_3_la_giua.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\B01.png` (Ảnh mảnh ụ lá của thân voi con (B01, 1536 × 1024, nền trắng): hai tầng lá lục tươi, tầng dưới cùng lục vàng, mầm xoắn) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\C02.png` | tầng lá giữa (lục tươi, mũi lá rủ thấp hơn y ≈ 580) vẽ đủ phần bị tầng trên che |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_3_la_tren.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\B01.png` (Ảnh mảnh ụ lá của thân voi con (B01, 1536 × 1024, nền trắng): hai tầng lá lục tươi, tầng dưới cùng lục vàng, mầm xoắn) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\C03.png` | các lá phía trên (lá to có chấm kem, mũi lá cao hơn y ≈ 580) kèm mầm xoắn |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_3_so.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\H01.png` (Ảnh mảnh đầu voi con (H01, 1536 × 1024, nền trắng): mặt da đá lam một mắt hổ phách to, vòi ngắn, mái lá lục tươi) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\H02.png` | đầu TRỌC (không lá) liền vòi: sọ tròn, mắt to vẽ đủ |
| `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\voi_rung_1\luot_3_mai.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\H01.png` (Ảnh mảnh đầu voi con (H01, 1536 × 1024, nền trắng): mặt da đá lam một mắt hổ phách to, vòi ngắn, mái lá lục tươi) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\voi_rung_1\tai_ve\F01.png` | mái lá của đầu (vòm lá lục tươi, các lọn mái rủ trước trán và hai bên mặt) |

Kiểm: đặt chồng lên ảnh mẫu thì phần giữ lại phải khít; mỗi mảnh / lớp một hình kín viền mực; nền trắng tinh; không bóng.

## Kiểm

- Voi con **chibi**: đầu to gần bằng thân, vòi ngắn mập (chóp cong lên, không chạm đất), hai **ngà mới nhú** (mẩu ngắn có túm rêu), mắt to hơn dạng lớn nhưng vẫn quả quyết; cùng góc ba phần tư nhìn sang phải.
- Lá **non, lục tươi và lục vàng** (không có lục sẫm của dạng lớn); một **mầm xoắn**; đủ bốn chân tách nhau, đuôi một lá.
- Tô phẳng, không bóng; nền trắng tinh; cả con không bị cắt mép.

