# Gói gửi GPT: `nguoi_cay_1` (người cây DẠNG 1, con non; dạng lớn là `nguoi_cay_2`)

Làm 2026-11-12 theo lời người dùng "ok gen dạng 1 đi". Thiết kế con non là đề xuất của Claude, chờ người dùng duyệt concept. Ghi chú: `ArtGen/Spine/inbox/nguoi_cay_ghichu.md` mục 8.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\nguoi_cay_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\nguoi_cay_1\tai_ve\L1.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/nguoi_cay_1/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\nguoi_cay_2\tai_ve\L1_duyet.png` | Concept DẠNG LỚN đã duyệt (1536 × 1024, nền trắng): quái rêu dáng người thế thủ nhìn sang phải, hai u rêu vai to có cành khô, đầu nhỏ nhe nanh có râu lá, tay gỗ quấn dây gai, váy lá. Lấy dáng, chỗ đặt tay chân, nét, vân sáp |
| 2 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp |

## Kiểm

- **Cùng dáng thủ, cùng chỗ đặt thân, tay, chân** như dạng lớn (chồng lên bản dạng lớn thì khuỷu, cổ tay, gối, bàn chân trùng).
- **Đầu to tròn hơn** như cái nụ, mày mảnh, hai mắt cam to hơn có con ngươi, **miệng mím có hai nanh nhỏ**; không râu, không hàm răng.
- Trên đầu **một mầm hai lá non**; vai là **hai túm rêu nhỏ**, không cành khô.
- Cổ áo ba lá nhỏ trơn mép; váy năm lá ngắn; mỗi tay một dải rêu rủ ngắn.
- Cẳng tay gỗ nhạt quấn **dây leo trơn không gai**; hai nắm tay **nhỏ hơn, trơn**; cả con không có gai.
- Màu lục non sáng hơn dạng lớn; tô phẳng, không bóng, nền trắng tinh, không bị cắt mép.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Dáng, chỗ tay chân lệch dạng lớn | `Keep the pose and the place of every limb exactly as in image 1: same shoulders, elbows, wrists, knees and feet.` |
| Vẫn còn gai, cành khô, râu | `Remove every thorn, the dead twigs and the beard: the young form has none.` |
| Mặt hiền, cười | `Keep the determined frown: slanted eyes under the brow band, closed frowning mouth with two small tusks.` |
| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient.` |

## Lượt 2: mảnh dạng 1 (concept duyệt 2026-11-12)

Ảnh mẫu 1 của mọi tờ: `C:\Atomik\PokiWar\ArtGen\Spine\inbox\nguoi_cay_1\tai_ve\L1_duyet.png` (concept dạng 1 đã duyệt, 1536 × 1024, nền trắng: con non đầu to tròn có mầm hai lá, hai túm rêu vai nhỏ, tay gỗ quấn dây leo trơn, váy lá ngắn). Mỗi tờ một file prompt; **chỉ gửi GPT đường dẫn file prompt**. Claude tự gen bằng `py -3 -I ArtGen/Spine/gen.py <file prompt>` rồi cắt bằng `NC_DANG=1 py -3 -I ArtGen/Spine/nguoi_cay_manh.py lam`.

| Tờ | File prompt | Giữ lại / vẽ gì | Ảnh lưu vào |
|---|---|---|---|
| `A` | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\nguoi_cay_1\luot_2_manh_A.txt` | đúng chỗ, đúng cỡ: đầu, hai cẳng tay, hai ống chân, đai (6 mảnh, vẽ đủ phần khuất) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\nguoi_cay_1\tai_ve\M_A.png` |
| `B` | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\nguoi_cay_1\luot_2_manh_B.txt` | đúng chỗ, đúng cỡ: thân, hai nắm tay, hai bàn chân (5 mảnh, vẽ đủ phần khuất) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\nguoi_cay_1\tai_ve\M_B.png` |
| `C` | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\nguoi_cay_1\luot_2_manh_C.txt` | đúng chỗ, đúng cỡ: hai túm rêu vai, hai đùi (4 mảnh, vẽ đủ phần khuất) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\nguoi_cay_1\tai_ve\M_C.png` |
| `D` | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\nguoi_cay_1\luot_2_manh_D.txt` | đúng chỗ, đúng cỡ: hai bắp tay (2 mảnh, vẽ đủ phần khuất) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\nguoi_cay_1\tai_ve\M_D.png` |
| `S1` | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\nguoi_cay_1\luot_2_manh_S1.txt` | tờ mảnh rời, ba hàng: 2 lá mầm + 3 lá cổ áo; 5 lá váy; 2 dải rêu rủ (12 mảnh) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\nguoi_cay_1\tai_ve\M_S1.png` |

Dây gai và quả cầu của hai chiêu dùng lại ảnh của dạng lớn (`inbox/nguoi_cay_2/manh/gai.png`, `cau.png`), thu nhỏ khi dựng rig.

Kiểm từng tờ: tờ A..D các mảnh nằm ĐÚNG chỗ, đúng cỡ như concept, mỗi mảnh kín viền, không chạm nhau, nền trắng tinh; tờ S1 đủ 12 mảnh rời theo ba hàng.
