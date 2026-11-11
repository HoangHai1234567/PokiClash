# Gói gửi GPT: dòng `ran_sung` dạng 1, lượt 2: RESKIN rig gốc

Người dùng chốt 2026-11-11: giữ nguyên rig Spine của con gốc (`monster_3247`: xương, lưới, trọng số, animation), chỉ **vẽ lại da từng mảnh**. GPT vẽ đè lên tờ mảnh gốc, **giữ hình bóng, chỗ, cỡ từng mảnh**; riêng chùm tai và chùm đuôi đổi thành sừng đen (gốc sừng đúng chỗ gốc chùm lông). Tờ mảnh gốc dựng bằng `py -3 -I ArtGen/Spine/ran_sung.py to 1`; ảnh về cắt bằng `py -3 -I ArtGen/Spine/ran_sung.py nhan 1`.

Ảnh mảnh gốc là của hãng làm game tham khảo: chỉ dùng làm mẫu trong máy, **không đăng công khai**.

## luot_2_reskin_A.txt

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\ran_sung_1\luot_2_reskin_A.txt` → lưu `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_1\tai_ve\R01.png` (trùng tên thì `_2`, `_3`…).
Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ran_sung_1/luot_2_reskin_A.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_1\tai_ve\L1_duyet.png` | Rắn sừng dạng 1 đã chốt (1536 × 1024, nền trắng): lấy màu, nét, vân sáp, đốm bong bóng, mắt hổ phách, sừng đen |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_1\mau\goc_A.png` | Tờ mảnh của rig gốc phóng 3 lần (1536 × 1024, nền trắng): bảy mảnh thân: cổ trên, ngực, khúc vòng cuộn, gáy, thân sau dài, chóp đuôi, chùm đuôi; màu gốc lục lam và kem |

## luot_2_reskin_B.txt

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\ran_sung_1\luot_2_reskin_B.txt` → lưu `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_1\tai_ve\R02.png` (trùng tên thì `_2`, `_3`…).
Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ran_sung_1/luot_2_reskin_B.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_1\tai_ve\L1_duyet.png` | Rắn sừng dạng 1 đã chốt (1536 × 1024, nền trắng): lấy màu, nét, vân sáp, đốm bong bóng, mắt hổ phách, sừng đen |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_1\mau\goc_B.png` | Tờ mảnh của rig gốc phóng 3 lần (1536 × 1024, nền trắng): mười một mảnh đầu: mặt nạ có lỗ mắt, nền mắt, khối miệng, hai chùm tai, hai mí, hai mống mắt, hai dấu mắt nheo; màu gốc lục lam và kem |

## Kiểm

- Mỗi mảnh **đúng chỗ, đúng cỡ, đúng hình bóng** của mảnh gốc (đặt đè lên tờ gốc thì viền trùng trong vài pixel).
- Lưng lam cô-ban có đốm bong bóng, bụng lam băng; hết hoa văn chữ triện và mảng sẫm của con gốc.
- Mép mềm của mảnh gốc (đầu dưới các khúc thân) vẫn là nét lam nhạt, không thành viền mực.
- Mặt nạ: **hai lỗ mắt để trắng**; nền mắt lam có hai tròng vàng; mống mắt vàng có con ngươi dọc; mí lam.
- Chùm tai và chùm đuôi đã thành **sừng đen**, gốc đúng chỗ gốc chùm lông, nằm trong vùng của chùm lông cũ.
- Tô phẳng, không bóng, nền trắng tinh, không nhãn chữ.

## GPT vẽ sai thì gửi thêm (`--note`)

| Sai | Gửi thêm |
|---|---|
| Mảnh bị dời, đổi cỡ, đổi dáng | `Every part must keep the exact silhouette, place and size it has in image 2; only colours, surface and style change.` |
| Tô kín lỗ mắt | `The two eye holes of the face mask stay empty: pure white inside their ink rings.` |
| Vẫn còn hoa văn chữ triện, mảng sẫm | `Remove the angular key pattern and the dark blotches; plain cobalt blue with a few round light-aqua bubble spots.` |
| Sừng to quá vùng chùm lông, hoặc vẫn có xoáy | `Each horn stays inside the area of the old tuft, base where the swirl was, tip where the tuft's tip was; no swirl, no fluff.` |
