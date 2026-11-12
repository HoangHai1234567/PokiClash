# Gói gửi GPT: `rong_vay_non` (rồng vây non = dạng 1 trong game; tên chưa đặt)

Làm 2026-11-12 (người dùng: "làm dạng 1 đi"). Hình đang có (`rong_vay_1`, rồng trưởng thành) là dạng 2. Dạng 1 chạy trên cùng rig, cùng clip, chỉ đổi tỉ lệ (đầu to 1,26; cánh 0,6) và vẽ lại da. Màu và chi tiết dưới đây là ĐỀ XUẤT của Claude, chờ người dùng duyệt concept. Ghi chú: `ArtGen/Spine/inbox/rong_vay_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_non\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/rong_vay_non/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

Lượt 2 (các tờ part đúng khung rig) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\L1_duyet.png` | Concept đã duyệt của dạng 2 (rồng trưởng thành): thân chàm, sừng đen dài, ba vỏ sò trên lưng, cánh lớn; 1536 × 1024, nền trắng. |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\mau\bo_cuc.png` | Hình bố cục rồng non do rig dựng (khung 0 của idle): đầu to hơn, cánh nhỏ, da còn của dạng 2; 1536 × 1024, nền trắng. Dựng lại: `RV_DANG=non py -3 -I ArtGen/Spine/rong_vay_rig.py bo_cuc <đường dẫn này>`. |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\tai_ve\L1_concept_3.png` | Bản nháp concept rồng non lượt trước (mặt, màu, nụ sừng, vây ngắn đã ưng; vòng cuộn và đuôi còn dài); 1536 × 1024, nền trắng. |

Người dùng 2026-11-12 sau bản nháp: "mặt nhìn non hơn rồi nhưng thân bạn cũng phải làm ngắn hơn" → rig co thân dọc chiều dài còn 0,72 (`K_THAN`), bố cục dựng lại. Sau `L1_concept_2`: "làm vây của nó ngắn hơn chút nữa" → rig co vây (lưng 0,74; tai 0,80; đuôi 0,82); Sau `L1_concept_3`: "phần đuôi vẫn dài, thu ngắn các part thân/đuôi lại chút" → rig: thân trước 0,70, thân sau 0,62, đuôi 0,54; lượt này giữ thiết kế của bản nháp trên bố cục mới.

Đề xuất dạng 1: thân lam nhạt `#6C86DC`, bụng kem; mắt to tròn màu hổ phách, mày thẳng; mỏ ngắn tù; hai nụ sừng ngắn; cánh và vây lam ngọc nhạt `#9CD3D6`; lưng trơn, không vỏ sò.

## Kiểm

- Một con, nền trắng, không bóng, không chữ, không viền trắng kiểu sticker.
- Bố cục trùng `mau/bo_cuc.png`: đầu to ở góc trên phải nhìn sang phải, THÂN NGẮN cuộn một vòng nhỏ, vây đuôi bên phải, hai cánh nhỏ.
- Thân lam nhạt (khác hẳn chàm đậm của dạng 2), bụng kem; KHÔNG có ba vỏ sò trên lưng.
- Không có sừng dài: chỉ hai nụ sừng ngắn màu đen than.
- Mắt to tròn màu hổ phách, nét mày thẳng: mặt quả quyết, dễ thương, không cười toe, không đáng sợ.
- Tô phẳng: không mảng sáng tối, không bóng loáng; chỉ một chấm sáng nhỏ trong mắt.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Vòng cuộn, đuôi vẫn dài như bản nháp | `The coil and the tail must be as SHORT and tight as in image 2: a small tight coil, a short tail with its fin close behind the chest.` |
| Vây vẫn dài như bản nháp | `Every fin must be as SHORT as in image 2: shorten the back fins, the ear fins and the tail fin.` |
| Thân vẫn dài như bản nháp | `The body must be as SHORT and compact as in image 2: do not lengthen the body or widen the loop.` |
| Có sừng dài như dạng 2 | `No long horns: only two short rounded charcoal horn buds on top of the head.` |
| Thân vẫn chàm đậm | `The body is LIGHT periwinkle blue #6C86DC, clearly lighter than the adult in image 1.` |
| Đổi dáng, đổi hướng, cánh to lại | `Keep image 2's layout exactly: same pose, same facing, same small wings, same places and sizes.` |
| Vẫn còn vỏ sò trên lưng | `Remove the scallop shells: the juvenile's back is plain periwinkle.` |
| Có bóng, mảng sáng tối | `Flat colour only: remove all shading, highlights and shadows.` |
| Mặt cười hiền như linh vật | `Determined fighter's face: straight brow line, closed beak, focused eye; cute but serious.` |

## Lượt 2: da rồng non cho từng part (concept đã duyệt 2026-11-12: `tai_ve/L1_duyet.png`)

Ảnh 1 của mọi tờ: concept rồng non đã duyệt (1536 × 1024, nền trắng). Ảnh 2: tờ part của DẠNG 2 đã xong (mỗi part nằm đúng ô, đúng khung ảnh vùng của rig; thân chàm, vây lam xám), dựng bằng `py -3 -I ArtGen/Spine/rong_vay_non.py to`. GPT vẽ lại đúng tờ đó với màu rồng non, giữ nguyên hình bóng. Cắt: `py -3 -I ArtGen/Spine/rong_vay_non.py cat G<k>` (lấy lại độ đậm và chỗ không có mực của dạng 2). Sừng, mỏ không vẽ lại (giữ đen than; sừng thu thành nụ ở rig).

| Tờ | File prompt | Tờ hướng dẫn (ảnh 2) | Lưu vào | Part |
|---|---|---|---|---|
| G1 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_non\luot_2_part_G1.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\mau\part_G1.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\tai_ve\N_G1.png` | `P_chibangR08` (sống cánh), `P_weiba` (vây), `P_shenti06` (khúc thân), `P_chibangL05` (sống cánh), `P_yuqi02` (vây) |
| G2 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_non\luot_2_part_G2.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\mau\part_G2.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\tai_ve\N_G2.png` | `P_chibangR06` (màng cánh), `P_shenti04` (khúc thân) |
| G3 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_non\luot_2_part_G3.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\mau\part_G3.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\tai_ve\N_G3.png` | `P_chibangL06` (màng cánh), `P_yuqi10` (vây) |
| G4 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_non\luot_2_part_G4.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\mau\part_G4.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\tai_ve\N_G4.png` | `P_shenti03` (khúc thân có vỏ sò (dạng 1 bỏ vỏ sò)), `P_yuqi15` (vây), `P_shenti02` (khúc thân), `P_shenti05` (khúc thân) |
| G5 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_non\luot_2_part_G5.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\mau\part_G5.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\tai_ve\N_G5.png` | `P_yuqi14` (vây), `P_shenti01` (khúc thân), `P_yuqi05` (vây) |
| G6 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_non\luot_2_part_G6.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\mau\part_G6.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_non\tai_ve\N_G6.png` | `P_yuqi01` (vây), `P_yuqi07` (vây), `P_yuqi09` (vây), `P_tou` (đầu), `P_erduo` (mào) |

Kiểm mỗi tờ: đủ số part, đúng chỗ, hình bóng không đổi; thân lam nhạt, bụng kem; vây và màng lam ngọc nhạt, tia lam đậm; khúc lưng không còn vỏ sò; đầu mắt to tròn. Sai thì chạy lại với `--note "<câu sửa>"`.
