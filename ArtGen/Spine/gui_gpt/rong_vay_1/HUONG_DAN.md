# Gói gửi GPT: `rong_vay` dạng 1 (rồng vây, tên chưa đặt)

Tướng thứ 8 đảo Thủy, làm 2026-11-11: reskin theo cách tách mảnh của con gốc `monster_3458`; màu và chi tiết là đề xuất của Claude, chờ người dùng duyệt concept. Ghi chú: `ArtGen/Spine/inbox/rong_vay_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/rong_vay_1/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

Lượt 2 (từng mảnh, theo bảng mổ 34 mảnh) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\L1_concept_3.png` | Bản nháp trước (1536 × 1024, nền trắng): rồng vây thân chàm tím, vây lam xám trầm, sừng và mỏ màu cát. Giữ nguyên nét vẽ và màu, chỉ đổi hai sừng và mỏ sang đen than |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\bo_cuc.png` | Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): rồng rắn thân chàm tím cuộn một vòng bên trái, đầu nhỏ có mỏ ở trên phải, bụng kem có vạch, năm vây buồm và ba vỏ sò trên lưng, hai cánh vây lam xám trầm có sống chàm sẫm buông xuống, đốm kem. Lấy cách dựng, chỗ đặt, tỉ lệ, thứ tự chồng |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ran_sung_1\tai_ve\L1_duyet.png` | Rắn sừng dạng 1 đã duyệt (1536 × 1024, nền trắng): rắn lam cuộn tròn, sừng đen, mắt cam. Lấy nét bút rung, vân sáp, tô phẳng, cách vẽ vạch bụng, mắt, sừng trơn |
| 4 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ti_tach_1\tai_ve\L1_duyet.png` | Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam. Chỉ lấy nét bút rung, vân sáp, tô phẳng |
| 5 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/rong_vay_bo_cuc.py`).

## Kiểm

- Dáng như sơ đồ: đầu nhỏ ở trên phải quay sang phải, cổ chữ S, thân dày cuộn **một vòng hở** bên trái, đuôi vòng ra sau ngực.
- Đầu: mõm ngắn có **mỏ sừng đen**, **một mắt hổ phách con ngươi dọc** dưới gờ mày sẫm, **hai sừng đen trơn** vuốt ra sau, vây tai lớn + vây tai nhỏ + vây mang trên má. **Không lông, lông vũ, bờm, râu.**
- Ngực và bụng: **vạch bụng kem** ngang thân, ranh với phần chàm là đường trơn.
- Lưng: **ba vỏ sò** kem gân màu cát; **năm vây buồm** lam xám trầm có tia chàm sẫm nhọn; vài vây nhỏ ở lòng vòng cuộn và dưới thân.
- **Hai cánh vây** buông xuống: cánh gần quét xuống trái, đè trước thân, sống chàm sẫm dày, sáu tia, mép sau **lượn sò tròn** (không rách kiểu lửa), ba đốm kem; cánh xa buông xuống phải sau thân.
- Vây đuôi chẻ đôi sau cổ, bên phải.
- Mỗi bộ phận có viền mực kín riêng (để cắt mảnh): từng khúc thân, từng vây, sống cánh, màng cánh.
- Tô phẳng: **không** bóng, không điểm sáng, không vân phát sáng, không mây, nước; nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có lông, lông vũ, bờm trắng quanh cổ | `Remove all fur, feathers and mane: the throat and chest are smooth cream belly plates, the horns are smooth charcoal-black horn, the ear is a webbed fin with rays.` |
| Mép cánh rách kiểu ngọn lửa, có vân sáng / chòm sao | `The trailing edge of each wing is cut into soft rounded scallops between the ray tips, clean curves; remove every glowing line and star: the membrane is flat dusty grey-teal with dark-navy rays and three cream spots.` |
| Có bóng, mảng sáng tối, điểm sáng, màng vây trong suốt | `Flat colour only: remove every shadow, highlight, gradient and transparency; keep the crayon hatching as texture only.` |
| Chibi, đầu to | `Grown-up proportions: the head is small (about 270 px wide), the body long and thick, as in the layout guide.` |
| Thân không cuộn vòng hoặc vòng bị lấp kín | `The body curls into one big open loop at the left with an empty hole in its middle, exactly as in the layout guide.` |
| Cánh dính liền thân, không có viền riêng | `Each wing spar and each wing membrane has its own closed ink outline and is drawn over (near wing) or behind (far wing) the body.` |
| Thiếu vỏ sò, vây buồm, đốm cánh | `Add every listed detail: three scallop shells on the back, five ray-finned sail fins, the small fins, three cream spots on the near wing, two on the far wing.` |
| Có mây, nước, tia sáng quanh con | `Remove everything around the creature: plain white background only.` |
| Mặt hiền, mắt tròn | `Make the eye almond shaped under a dark pointed brow ridge: a determined, fierce look.` |

## Lượt 2: từng nhóm mảnh (concept đã duyệt)

Mỗi nhóm một file prompt, một ảnh: GPT vẽ lại concept chỉ còn các mảnh của nhóm, **đúng chỗ, đúng cỡ**, mỗi mảnh một hình kín có cả phần khuất. Chia mảnh một – một theo con gốc (bảng ở `inbox/rong_vay_ghichu.md`).

Ảnh mẫu của mọi nhóm: ảnh 1 = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\L1_duyet.png` (concept đã duyệt, 1536 × 1024, nền trắng: rồng vây thân chàm tím, vây lam xám, sừng và mỏ đen); ảnh 2 = tờ hướng dẫn của nhóm (1536 × 1024, nền trắng: chính concept đã xoá mọi thứ ngoài các mảnh của nhóm, đúng chỗ; phần khuất của từng mảnh tô hồng để GPT vẽ bù).

Nhóm M (mỏ trên, mỏ dưới, mí mắt nhắm) vẽ rời trên tờ phóng to 6 lần: ảnh 2 của nó là ô mặt của concept phóng 6 lần (mắt hổ phách bên trái, mỏ đen bên phải).

Nhóm S (dải cạnh cánh) chỉ đính concept (ảnh 1) để lấy màu, nét; không có ảnh 2: cột tờ hướng dẫn ghi lại concept.

**Nhóm T thay các khúc thân của nhóm B, C, D**: khúc nối nhau phải cắt từ MỘT ảnh cả thân, gen riêng thì vạch bụng lệch ở chỗ nối. Ảnh 2 của T: concept chỉ còn năm khúc thân, phần thân bị cánh, vây, đầu che tô hồng.

**Lượt 3 (tờ P1…): mảnh vẽ đúng khung part của rig.** Ảnh 2: mỗi part một hình bóng phẳng đúng cỡ, đúng hướng như ảnh part trong rig (không có nét vẽ của game gốc); GPT tô lại theo thiết kế của mình mà giữ nguyên hình bóng. Cắt bằng `rong_vay.py cat_part P1` → `manh/part/<slot>.png`.

| Nhóm | File prompt | Tờ hướng dẫn (ảnh 2) | Lưu vào | Mảnh |
|---|---|---|---|---|
| A | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_A.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\nhom_A.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_A.png` | vay_duoi (vây đuôi + cuống đuôi), canh_x_song (sống cánh xa), vay_11 (vây), vay_14 (cụm vây buồm lớn), tai_lon (vây tai lớn), canh_g_mang (màng cánh gần (không sống)) |
| B | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_B.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\nhom_B.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_B.png` | than_4 (vòng cuộn chữ C), than_2 (ngực), dau (đầu (có mắt, gờ mày; không mỏ, sừng, vây)) |
| C | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_C.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\nhom_C.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_C.png` | than_5 (khúc đáy), vay_15 (vây buồm cạnh cổ), vay_08 (vây), vay_07 (vây), than_1 (cổ), sung_t (sừng trước) |
| D | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_D.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\nhom_D.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_D.png` | canh_x_mang (màng cánh xa), vay_10 (vây), than_3 (lưng mang ba vỏ sò), vay_ma (vây má) |
| E | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_E.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\nhom_E.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_E.png` | vay_16 (vây), vay_09 (vây), sung_s (sừng sau), canh_g_song (sống cánh gần) |
| F | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_F.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\nhom_F.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_F.png` | than_6 (khúc đuôi mảnh sau ngực), vay_06 (vây) |
| G | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_G.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\nhom_G.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_G.png` | vay_13 (vây), vay_12 (vây) |
| M | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_M.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\mo_x6.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_M.png` | mo_tren (mỏ trên), mo_duoi (mỏ dưới), mat_nham (mí mắt nhắm) |
| S | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_S.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\L1_duyet.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_S.png` | canh_canh (dải cạnh cánh, một ảnh dùng cho cả hai cánh) |
| T | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_T.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\nhom_T.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_T.png` | than_1 … than_5 (cả thân liền một ảnh, `rong_vay.py cat_than` cắt thành năm khúc chờm mép nhau) |
| U | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_2_nhom_U.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\nhom_U.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_U.png` | phần đuôi liền một ảnh: nối khúc đáy → than_6 → vay_duoi (cuống + vây); `rong_vay.py cat_duoi` cắt |
| P1 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_P1.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_P1.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_P1.png` | `P_chibangR08` (sống cánh gần), `P_weiba` (vây đuôi), `P_shenti06` (khúc đuôi (dùng cho cả khúc đuôi thứ hai)), `P_chibangL05` (sống cánh xa), `P_yuqi02` (vây tai nhỏ) |
| P2 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_P2.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_P2.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_P2.png` | `P_chibangR06` (canh_g_mang), `P_shenti04` (than_4) |
| P3 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_P3.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_P3.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_P3.png` | `P_chibangL06` (canh_x_mang), `P_yuqi10` (vay_10), `P_yuqi16` (vay_16) |
| P4 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_P4.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_P4.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_P4.png` | `P_shenti03` (than_3), `P_yuqi15` (vay_15), `P_yuqi13` (vay_13), `P_shenti02` (than_2), `P_shenti05` (than_5) |
| P5 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_P5.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_P5.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_P5.png` | `P_yuqi14` (vay_14), `P_shenti01` (than_1), `P_yuqi08` (vay_08), `P_yuqi05` (tai_lon), `P_yuqi06` (vay_06), `P_yuqi12` (vay_12) |
| P6 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_P6.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_P6.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_P6.png` | `P_yuqi03` (sung_t), `P_yuqi04` (sung_s), `P_yuqi01` (vay_ma), `P_yuqi07` (vay_07), `P_yuqi11` (vay_11), `P_yuqi09` (vay_09), `P_tou` (dau), `P_zuiba01` (mo_tren), `P_erduo` (dau), `P_zuiba02` (mo_duoi) |
| Q2 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_Q2.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_Q2.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_Q2.png` | `P_chibangR06` (canh_g_mang), `P_shenti04` (than_4) |
| Q3 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_Q3.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_Q3.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_Q3.png` | `P_chibangL06` (canh_x_mang), `P_yuqi10` (vay_10), `P_yuqi16` (vay_16) |
| Q4 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_Q4.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_Q4.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_Q4.png` | `P_shenti03` (than_3), `P_yuqi15` (vay_15), `P_yuqi13` (vay_13), `P_shenti02` (than_2), `P_shenti05` (than_5) |
| Q5 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_Q5.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_Q5.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_Q5.png` | `P_yuqi14` (vay_14), `P_shenti01` (than_1), `P_yuqi08` (vay_08), `P_yuqi05` (tai_lon), `P_yuqi06` (vay_06), `P_yuqi12` (vay_12) |
| Q6 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_vay_1\luot_3_part_Q6.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\mau\part_Q6.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\N_Q6.png` | `P_yuqi03` (sung_t), `P_yuqi04` (sung_s), `P_yuqi01` (vay_ma), `P_yuqi07` (vay_07), `P_yuqi11` (vay_11), `P_yuqi09` (vay_09), `P_tou` (dau), `P_zuiba01` (mo_tren), `P_erduo` (dau), `P_zuiba02` (mo_duoi) |

Kiểm từng ảnh: đủ số mảnh; mảnh không chạm nhau; mỗi mảnh viền mực kín; phần lộ trùng concept; nền trắng tinh. Sau đó `py -3 -I ArtGen/Spine/rong_vay.py cat` rồi `ghep` để soi ghép khít.

| Sai | Gửi thêm |
|---|---|
| Mảnh dính nhau hoặc thiếu mảnh | `Draw exactly the listed parts, each as its own closed shape, with white background between them.` |
| Mảnh lệch chỗ, sai cỡ | `Every part must stay in the same position and at the same size as in image 1.` |
| Còn bộ phận khác của con | `Remove everything that is not one of the listed parts.` |
