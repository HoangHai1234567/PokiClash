# Gói gửi GPT: `bach_tuoc` dạng 1 (bạch tuộc con non, tên chưa đặt)

Làm 2026-11-12 sau khi dạng 2 xong (người dùng: "làm dạng 1, con non"). Cùng rig, cùng lưới, cùng clip với dạng 2 (con gốc `monster_3616`); chỉ vẽ lại da trong cùng khung part và đổi tỉ lệ vài xương. Thiết kế là đề xuất của Claude, chờ duyệt concept. Ghi chú: `ArtGen/Spine/inbox/bach_tuoc_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `BT_DANG=1 py -3 -I ArtGen/Spine/build_bach_tuoc.py` rồi `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/bach_tuoc_1/luot_1_concept.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\L1_duyet.png` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): bạch tuộc hồng đỏ nhìn nghiêng sang phải, một mắt vàng trong vành hốc mắt dưới gờ mày dữ, mào ba gai, đốm, sẹo. Lấy nét vẽ, cách vẽ mắt, vành hốc mắt, đốm, giác hút |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\mau\bo_cuc.png` | Sơ đồ bố cục dựng từ rig dạng 1 (1536 × 1024, nền trắng): đầu vòm rất to hồng nhạt, một mắt to vàng trong vành hốc mắt, hai gai mào nhỏ ở trên trái, hai xúc tu to hơn bên trái, các xúc tu ngắn bên phải. Lấy cách dựng, chỗ đặt, tỉ lệ, thứ tự chồng |
| 3 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Sơ đồ bố cục dựng lại bằng `BT_DANG=1 py -3 -I ArtGen/Spine/bach_tuoc_rig.py bo_cuc <đường dẫn mau/bo_cuc.png>`.

## Kiểm

- Con NON của dạng 2: cùng loài, cùng nét; **đầu rất to** so với xúc tu, da **hồng san hô nhạt** hơn dạng 2.
- Nhìn nghiêng sang **phải**, **một mắt rất to** vàng con ngươi ngang lệch phải, trong vành hốc mắt tròn có bướu nhỏ ở trên trái; mí mỏng, **gờ mày nhỏ** dốc nhẹ xuống phải: lì lợm, quả quyết, chưa dữ. **Không mồm.**
- Mào mới nhú **hai gai nhỏ** ở trên trái; khoảng năm đốm nhỏ; **không sẹo, không mụn gai**.
- **Sáu xúc tu ngắn mập**: hai cái to hơn ở bên trái lộ mặt dưới kem có giác hút, ba ngón nhỏ ở giữa và bên phải, một cái nhỏ ngoài cùng bên phải.
- Mỗi bộ phận có viền mực kín riêng. Tô phẳng, không bóng, không điểm sáng; nền trắng tinh.

## Lượt 3: tờ mảnh theo khung part (concept đã duyệt)

Ảnh 1 của mọi tờ = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\tai_ve\L1_duyet.png` (concept dạng 1 đã duyệt, 1536 × 1024, nền trắng: bạch tuộc non hồng nhạt, một mắt rất to, hai gai mào nhỏ). Ảnh 2 = tờ hướng dẫn (1536 × 1024, nền trắng): mỗi part của rig là một hình bóng kín đúng cỡ, đúng hướng, tô phẳng bằng mã theo thiết kế dạng 1. Dựng tờ hướng dẫn: `BT_DANG=1 py -3 -I ArtGen/Spine/bach_tuoc.py nhom_part`; cắt: `BT_DANG=1 ... bach_tuoc.py cat_part Q1 Q2 ...`.

| Tờ | File prompt | Tờ hướng dẫn (ảnh 2) | Lưu vào | Mảnh |
|---|---|---|---|---|
| Q1 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_1\luot_3_part_Q1.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\mau\part_Q1.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\tai_ve\N_Q1.png` | `P_tou` (đầu (vòm, đốm, sẹo, vành hốc mắt, gờ mày; không vẽ mắt)), `P_shou5_1` (ngón 3) |
| Q2 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_1\luot_3_part_Q2.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\mau\part_Q2.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\tai_ve\N_Q2.png` | `P_shou4_1` (ngón 2), `P_shou3_1` (ngón 1), `P_shou1_1` (xúc tu 1 ngọn) |
| Q3 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_1\luot_3_part_Q3.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\mau\part_Q3.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\tai_ve\N_Q3.png` | `P_shou2_2` (xúc tu 2 gốc), `P_shou6_2` (xúc tu trước ngọn), `P_shou2_1` (xúc tu 2 ngọn), `P_yanjing3` (mắt nhắm), `P_yanjing1` (mắt mở), `P_yanjing2` (mắt lim dim), `P_shou1_2` (xúc tu 1 gốc), `P_shou6_1` (xúc tu trước gốc) |
| Q4 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_1\luot_3_part_Q4.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\mau\part_Q4.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_1\tai_ve\N_Q4.png` | `P_shou1_3` (khối gốc xúc tu), `gai_1` (gai mào to), `gai_2` (gai mào vừa) |

Hố đất, bạch tuộc con, xúc tu dài của appear: dùng chung ảnh của dạng 2 (`inbox/bach_tuoc_2/tai_ve/H01, C01, V01`).
