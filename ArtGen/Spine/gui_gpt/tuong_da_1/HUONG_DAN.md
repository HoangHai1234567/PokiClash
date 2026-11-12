# Gói gửi GPT: `tuong_da` dạng 1 (Mầm Đá: bản non của Gạc Đá, tướng thứ 3 đảo Mộc)

Làm 2026-11-12. Người dùng: "làm 2 dạng thôi, con vừa rồi là dạng 2, lát nữa bạn làm dạng 1"; không tả dạng 1 nên thiết kế là đề xuất của Claude (đầu to tròn hơn, chưa mọc gạc mà chỉ có một mầm hai lá, hạt mầm chưa nảy, vai và tay nhỏ, ít rêu, không dây leo, bốn viên đá nhỏ), chờ duyệt concept. Cùng rig, cùng clip với dạng 2 nên mỗi mảnh phải nằm quanh đúng chỗ của dạng 2. Ghi chú: `ArtGen/Spine/inbox/tuong_da_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\tuong_da_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tuong_da_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tuong_da_1/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tuong_da_2\tai_ve\L1_duyet.png` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): tượng đá lơ lửng phủ rêu, đầu trụ đá có hai nhánh gạc, lõi hạt mầm lục đã nảy mầm trong hai vòng ngực, hai tấm vai có dây leo, hai tảng cẳng tay quấn rễ, bàn tay đá, bảy viên đá nhỏ. Lấy nét, màu, kiểu dáng và CHỖ ĐẶT từng mảnh |

## Kiểm

- Cùng con với dạng 2 nhưng non hơn: đầu tròn to hơn, **không gạc**, một mầm hai lá; hạt mầm **chưa nảy**; vai, tay nhỏ lại; ít rêu, không dây leo; chỉ bốn viên đá nhỏ.
- Mỗi mảnh nằm quanh đúng chỗ của mảnh tương ứng ở dạng 2 (chồng hai ảnh lên nhau thì tâm các mảnh trùng); khe trắng rộng hơn.
- Không mặt, không chân; mỗi mảnh viền mực kín; tô phẳng, không bóng, lõi không phát sáng; nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Vẫn có gạc cây | `No antlers and no branches on the head: only ONE small sprout with two round leaves.` |
| Các mảnh dời chỗ, bố cục khác dạng 2 | `Every piece must be centred at the same place as the matching piece of image 1; only the sizes change.` |
| Hạt mầm đã nảy mầm | `The seed is still closed: remove the sprout from the seed.` |
| Có bóng, sáng tối | `Flat colour only: remove every shadow, highlight and gradient.` |
| Thêm mắt, mặt | `It has NO face: remove the eyes and mouth.` |

## Lượt 2: mảnh đúng chỗ, đúng cỡ (2026-11-12, sau khi người dùng chọn đầu kiểu A = `L1b_tru.png` → `L1_duyet.png`)

Mọi mảnh của rig là mảnh cứng một xương. Mỗi file vẽ lại concept đã duyệt nhưng chỉ giữ vài mảnh không chồng nhau, vẽ đủ phần khuất, bỏ hết thứ khác (nền trắng). Ảnh mẫu duy nhất của cả năm file:

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tuong_da_1\tai_ve\L1_duyet.png` | Concept đã duyệt (1536 × 1024, nền trắng): tượng đá non lơ lửng: đầu chum đá tròn có một mầm hai lá, lõi hạt mầm lục chưa nảy trong hai vòng ngực, hai tấm vai nhỏ, hai tảng cẳng tay tròn quấn một vòng rễ, bàn tay đá, bốn viên đá nhỏ ở khớp vai – tay |

- **`A`**: đầu (chum đá tròn + rêu + mầm hai lá), tấm vai XA vẽ đủ, chóp đá to vẽ đủ. Chỉ gửi GPT đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\tuong_da_1\luot_2_manh_A.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tuong_da_1\tai_ve\M_A.png` (trùng tên thì `_2`, `_3`…).
- **`B`**: vòng ngực đứng vẽ đủ (lỗ giữa để trắng), hai khối lòng bàn tay vẽ đủ (không ngón, không rễ). Chỉ gửi GPT đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\tuong_da_1\luot_2_manh_B.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tuong_da_1\tai_ve\M_B.png` (trùng tên thì `_2`, `_3`…).
- **`C`**: vòng ngực nằm (đai dưới) vẽ đủ thành một vành bầu dục kín + hai rễ nâu móc lên. Chỉ gửi GPT đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\tuong_da_1\luot_2_manh_C.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tuong_da_1\tai_ve\M_C.png` (trùng tên thì `_2`, `_3`…).
- **`D`**: hạt mầm lục chưa nảy, vẽ đủ hình trứng, không rễ. Chỉ gửi GPT đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\tuong_da_1\luot_2_manh_D.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tuong_da_1\tai_ve\M_D.png` (trùng tên thì `_2`, `_3`…).
- **`E`**: quả cầu cổ, tấm vai GẦN, khoá, hai tảng cẳng tay + vòng rễ (không bàn tay), hai chóp đá nhỏ, bốn viên đá nhỏ. Chỉ gửi GPT đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\tuong_da_1\luot_2_manh_E.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\tuong_da_1\tai_ve\M_E.png` (trùng tên thì `_2`, `_3`…).

Kiểm từng ảnh: đúng các mảnh đã kê, nằm trùng chỗ concept (chồng lên concept phải khít), mỗi mảnh viền mực kín, không chạm nhau, phần khuất đã vẽ đủ, nền trắng tinh, không bóng. Claude cắt bằng `tuong_da_manh.py`.
