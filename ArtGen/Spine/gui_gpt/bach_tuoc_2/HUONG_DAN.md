# Gói gửi GPT: `bach_tuoc` dạng 2 (bạch tuộc quái vật, tên chưa đặt)

Làm 2026-11-12: reskin theo khung part của con gốc `monster_3616` (con gốc là dạng 2); màu và chi tiết là đề xuất của Claude, chờ người dùng duyệt concept. Ghi chú: `ArtGen/Spine/inbox/bach_tuoc_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_2\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/bach_tuoc_2/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

Lượt 2 (tờ mảnh theo khung part) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\mau\nhap_3_lat_ngang.png` | Bản nháp 3 đã lật ngang bằng mã (1536 × 1024, nền trắng): bạch tuộc hồng đỏ nhìn nghiêng, một mắt vàng trong vành hốc mắt, hai xúc tu to ở bên TRÁI, ba xúc tu ngắn ở giữa và bên phải; con mắt còn nhìn sang trái và mào gai còn ở trên phải. Giữ nguyên mọi thứ, chỉ sửa: mắt nhìn sang PHẢI (phía xúc tu ngắn), mào gai dời ra sau đầu (trên trái) |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\mau\bo_cuc.png` | Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): bạch tuộc hồng đỏ nhìn sang PHẢI, một mắt vàng con ngươi ngang lệch phải dưới gờ mày dốc xuống phải, ba gai mào ở trên TRÁI (sau đầu), hai xúc tu to bên trái, xúc tu ngắn bên phải. Lượt này chỉ lấy hướng mắt và chỗ đặt mào gai |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\L1_duyet.png` | Rồng vây đã duyệt (1536 × 1024, nền trắng): rồng rắn chàm tím có cánh vây lam xám, sừng đen. Chỉ lấy nét bút rung, vân sáp, tô phẳng |
| 4 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_voi_2\tai_ve\L1_duyet.png` | Cá voi biến dị dạng 2 đã duyệt (1536 × 1024, nền trắng): quái cá voi há miệng đầy nanh. Lấy nét, tô phẳng, mức "dữ" và mật độ chi tiết của một dạng 2 |
| 5 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/bach_tuoc.py bo_cuc`).

## Kiểm

- Nhìn sang **phải**, tức là về phía **ba xúc tu ngắn** (như con gốc); hai xúc tu to lộ mặt dưới kem nằm bên **trái** (phía sau). Đầu vòm to **hồng đỏ**, **đầu trần** (không mũ, vỏ, san hô, xích), ngồi trên **sáu xúc tu** ngắn mập.
- Mặt dựng như con gốc: **nhìn nghiêng, chỉ MỘT mắt** vàng **con ngươi ngang** nằm giữa vòm đầu, trong **vành hốc mắt tròn**; một **gờ mày đỏ sẫm** (nếp da thuôn hai đầu) cao ở bên trái, dốc xuống về bên phải; con ngươi lệch về bên **phải**; **không mồm, không phễu, không mắt thứ hai**.
- **Mào ba gai thịt** đỏ sẫm ở trên **trái** (sau đầu), mũi gai ngả sang trái; **đốm sẫm** lốm đốm trên đỉnh và sau đầu.
- Hai xúc tu to bên **trái** cong lên lộ **mặt dưới kem có giác hút**; ba xúc tu nhỏ như ba ngón dưới đầu ở giữa và bên phải; một xúc tu nhỏ ngoài cùng bên phải.
- Mỗi bộ phận có viền mực kín riêng. Tô phẳng: **không** bóng, không điểm sáng, không ướt bóng; nền trắng tinh. Không tím, lam.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có mũ, vỏ ốc, mảnh tàu, san hô, xích | `The head is BARE: remove everything on it except the three fleshy crest spikes. No hat, no shell, no planks, no coral, no chain.` |
| Có bóng, mảng sáng tối, da ướt bóng | `Flat colour only: remove every shadow, highlight, gradient and wet shine; keep the crayon hatching as texture only.` |
| Mặt hiền, dễ thương kiểu linh vật | `Make it a glaring monster: heavy dark brow ridges slanting down toward the middle, eyelids lowered over the top of the eyes, the body heavy and squat. Not cute, not smiling.` |
| Con ngươi tròn hoặc dọc | `Each pupil is a dark HORIZONTAL bar across the yellow eye.` |
| Mắt nhìn sang trái, mào gai ở bên phải | `The creature faces the viewer's RIGHT, toward its short tentacles: the pupil sits toward the right of the eye, the brow slants down to the right, and the three crest spikes are over the upper LEFT of the head, leaning left.` |
| Có hai mắt, hoặc có mồm / phễu / lỗ trên má | `The head is in profile: exactly ONE eye is visible, and there is NO mouth, no funnel, no hole anywhere on the head.` |
| Màu tím, lam, hoặc đỏ chói | `Use only the listed colours: muted coral red skin, darker red blotches, dark maroon spikes and brows, pale cream undersides, salmon suckers, yellow eyes.` |

## Hố đất của clip appear

File prompt: `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_2\luot_2_ho_dat.txt` → lưu `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\H01.png` (1536 × 1024, nền trắng: một cái hố đất nhìn chéo từ trên, lòng hố đen, vành đất vỡ đùn lên quanh miệng, vành trước cao nhất). Mã tách hai lớp trước / sau: `py -3 -I ArtGen/Spine/bach_tuoc.py cat_ho`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\L1_duyet.png` | Rồng vây đã duyệt (1536 × 1024, nền trắng): chỉ lấy nét bút rung, vân sáp, tô phẳng |
| 2 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): nét bút mực nâu, vân chì sáp, cách vẽ đất đá |

Kiểm: lòng hố là MỘT elip đen phẳng, không có gì bên trong; vành trước đè lên mép dưới elip; không cỏ, bụi, bóng đổ; nền trắng tinh.

## Lượt 3: tờ mảnh theo khung part (concept đã duyệt)

Ảnh 1 của mọi tờ = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\L1_duyet.png` (concept đã duyệt, 1536 × 1024, nền trắng: bạch tuộc hồng đỏ nhìn nghiêng sang phải, một mắt vàng, mào ba gai). Ảnh 2 = tờ hướng dẫn (1536 × 1024, nền trắng): mỗi part của rig là một hình bóng kín đúng cỡ, đúng hướng, tô phẳng bằng mã theo thiết kế; GPT vẽ lại sạch mà giữ nguyên hình bóng. Dựng tờ hướng dẫn: `py -3 -I ArtGen/Spine/bach_tuoc.py nhom_part`; cắt: `bach_tuoc.py cat_part Q1 Q2 ...` → `manh/part/<tên>.png`.

| Tờ | File prompt | Tờ hướng dẫn (ảnh 2) | Lưu vào | Mảnh |
|---|---|---|---|---|
| Q1 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_2\luot_3_part_Q1.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\mau\part_Q1.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\N_Q1.png` | `P_tou` (đầu (vòm, đốm, sẹo, vành hốc mắt, gờ mày; không vẽ mắt)), `P_shou5_1` (ngón 3) |
| Q2 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_2\luot_3_part_Q2.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\mau\part_Q2.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\N_Q2.png` | `P_shou4_1` (ngón 2), `P_shou3_1` (ngón 1), `P_shou1_1` (xúc tu 1 ngọn) |
| Q3 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_2\luot_3_part_Q3.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\mau\part_Q3.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\N_Q3.png` | `P_shou2_2` (xúc tu 2 gốc), `P_shou6_2` (xúc tu trước ngọn), `P_shou2_1` (xúc tu 2 ngọn), `P_yanjing3` (mắt nhắm), `P_yanjing1` (mắt mở), `P_yanjing2` (mắt lim dim), `P_shou1_2` (xúc tu 1 gốc), `P_shou6_1` (xúc tu trước gốc) |
| Q4 | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_2\luot_3_part_Q4.txt` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\mau\part_Q4.png` | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\N_Q4.png` | `P_shou1_3` (khối gốc xúc tu), `gai_1` (gai mào to), `gai_2` (gai mào vừa), `gai_3` (gai mào nhỏ) |

Kiểm từng tờ: đủ số mảnh, mỗi mảnh đúng chỗ, đúng cỡ, đúng hướng như tờ hướng dẫn; viền mực kín; nền trắng tinh; đầu không có mắt (mắt là mảnh riêng).

| Sai | Gửi thêm |
|---|---|
| Mảnh lệch chỗ, sai cỡ, bị xoay | `Every part must keep exactly the silhouette, size, orientation and position it has in image 2.` |
| Ghép các mảnh thành con, hoặc thêm mảnh | `Draw only the listed cut-out parts, separate, each in its own place; do not assemble them.` |

## Xúc tu dài của clip appear

File prompt: `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_2\luot_3_xuc_tu_dai.txt` → lưu `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\V01.png` (1536 × 1024, nền trắng: một xúc tu duỗi thẳng nằm ngang, gốc dày bên trái, ngọn thon bên phải, hai phần ba trên là da hồng đỏ có đốm, một phần ba dưới là mặt dưới kem có một hàng giác hút). Ảnh mẫu duy nhất: concept đã duyệt. Cắt nền: `py -3 -I ArtGen/Spine/bach_tuoc.py cat_voi`. Rig dựng nó thành dải lưới 10 đốt cho hai xúc tu chống đẩy thân lên khỏi hố.

Kiểm: thẳng tắp, nằm ngang, hai mép đối xứng qua trục giữa; không cong, không móc ở ngọn; viền kín; nền trắng tinh.

## Bạch tuộc con (chiêu cuối)

File prompt: `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\bach_tuoc_2\luot_3_bach_tuoc_con.txt` → lưu `C:\Atomik\PokiWar\ArtGen\Spine\inbox\bach_tuoc_2\tai_ve\C01.png` (1536 × 1024, nền trắng: một bạch tuộc con hồng đỏ nhìn sang phải, một mắt, một gai mào, bốn xúc tu ngắn). Ảnh mẫu duy nhất: concept đã duyệt. Cắt nền: `py -3 -I ArtGen/Spine/bach_tuoc.py cat_con`.
