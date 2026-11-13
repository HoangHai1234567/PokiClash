# Gói gửi GPT: `kiem_si_non` (DẠNG 1 của Voọc Tướng: voọc non; tướng thứ 8 đảo Mộc, id game `tho_hoang`)

Làm 2026-11-13 ở máy ổ D. Dạng 1 dùng CHUNG rig với dạng lớn (`monster_3620`), đổi tỉ lệ ở rig (`ArtGen/Spine/kiem_si_non.py`): nửa thân
trên co 0,8 quanh hông (hai tay vẫn cùng nắm một thanh kiếm), đầu + mũ to 1,4 lần so với thân, chân ngắn lại, lá mào còn mầm nhỏ. Bố cục =
hình rig dạng non ghép bằng da dạng lớn (`py -3 -I ArtGen/Spine/kiem_si_non.py bo_cuc`). Mảnh giáp, kiếm, áo tơi, chân giữ HÌNH dạng lớn
(sau đổi màu bằng mã); chỉ đầu, mặt, mũ, mào vẽ mới. Màu và mũ là đề xuất của Claude, chờ người dùng chọn. Ghi chú: `ArtGen/Spine/inbox/kiem_si_ghichu.md`.

## Hướng `cam`: A · voọc con lông cam (như voọc con ngoài đời, lớn lên mới sẫm lại)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\kiem_si_non\luot_1_concept_cam.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L1_cam.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_non/luot_1_concept_cam.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\mau\bo_cuc.png` | Bố cục voọc non (1536 × 1024, nền trắng): hình rig dạng non ghép bằng da dạng lớn: mũ giáp + đầu rất to, thân gọn, tấm vai to có huy hiệu lá và ba tua ở trái, hai tay cầm kiếm còn trong vỏ thấp trước bụng, chân ngắn. Lấy dáng, tỉ lệ, chỗ đặt, hình từng mảnh; màu, mặt, mũ phải đổi |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_1\tai_ve\L1_duyet.png` | Concept dạng lớn đã duyệt (1536 × 1024, nền trắng): voọc tướng quân lông than, ria trắng, giáp sơn lục rêu, mũ kabuto mào lá. Lấy nét vẽ, tô phẳng, vẻ cùng loài |

## Hướng `xam`: B · voọc con lông xám tro nhạt, nón lá nhỏ thay mũ giáp

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\kiem_si_non\luot_1_concept_xam.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L1_xam.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_non/luot_1_concept_xam.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\mau\bo_cuc.png` | Bố cục voọc non (1536 × 1024, nền trắng): hình rig dạng non ghép bằng da dạng lớn: mũ giáp + đầu rất to, thân gọn, tấm vai to có huy hiệu lá và ba tua ở trái, hai tay cầm kiếm còn trong vỏ thấp trước bụng, chân ngắn. Lấy dáng, tỉ lệ, chỗ đặt, hình từng mảnh; màu, mặt, mũ phải đổi |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_1\tai_ve\L1_duyet.png` | Concept dạng lớn đã duyệt (1536 × 1024, nền trắng): voọc tướng quân lông than, ria trắng, giáp sơn lục rêu, mũ kabuto mào lá. Lấy nét vẽ, tô phẳng, vẻ cùng loài |

## Lượt 2: khỉ voọc con KHÔNG GIÁP (người dùng 2026-11-13, thay hai hướng trên)

"làm dạng 1 chibi cute kiểu con khỉ không giáp cầm kiếm cũ cùn hoặc cành cây thôi". Lông cam như hướng A; hai hướng chỉ khác vũ khí.
Bố cục mới: `py -3 -I ArtGen/Spine/kiem_si_non.py bo_cuc_tran` (đầu × 1,55; ẩn mọi mảnh giáp, mũ, áo tơi, vỏ kiếm, kiếm ngắn; lưỡi kiếm dài trần
hiện ở dáng nghỉ, hai tay cùng nắm).

### `kiem_cun`: khỉ voọc con không giáp, cầm thanh kiếm cũ cùn (băng vải sờn), buộc khăn trán

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\kiem_si_non\luot_2_concept_kiem_cun.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L2_kiem_cun.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_non/luot_2_concept_kiem_cun.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\mau\bo_cuc_tran.png` | Bố cục khỉ con không giáp (1536 × 1024, nền trắng): rig dạng non ghép bằng da dạng lớn đã bỏ giáp: đầu to bờm trắng, thân lông than, đuôi cong vút lên ở trên trái, hai tay cầm thanh kiếm trần chĩa lên trái, còn bao tay và giáp ống chân bằng tre (phải vẽ thành cẳng tay, ống chân lông). Lấy dáng, tỉ lệ, chỗ đặt |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_1\tai_ve\L1_duyet.png` | Concept dạng lớn đã duyệt (1536 × 1024, nền trắng): voọc tướng quân mặc giáp. Chỉ lấy nét vẽ, tô phẳng, nét mặt cùng loài |

### `canh_cay`: khỉ voọc con không giáp, cầm cành cây làm kiếm, đội một chiếc lá trên đầu

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\kiem_si_non\luot_2_concept_canh_cay.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L2_canh_cay.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_non/luot_2_concept_canh_cay.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\mau\bo_cuc_tran.png` | Bố cục khỉ con không giáp (1536 × 1024, nền trắng): rig dạng non ghép bằng da dạng lớn đã bỏ giáp: đầu to bờm trắng, thân lông than, đuôi cong vút lên ở trên trái, hai tay cầm thanh kiếm trần chĩa lên trái, còn bao tay và giáp ống chân bằng tre (phải vẽ thành cẳng tay, ống chân lông). Lấy dáng, tỉ lệ, chỗ đặt |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_1\tai_ve\L1_duyet.png` | Concept dạng lớn đã duyệt (1536 × 1024, nền trắng): voọc tướng quân mặc giáp. Chỉ lấy nét vẽ, tô phẳng, nét mặt cùng loài |

## Lượt 3: kiếm cũ cùn TRONG VỎ GỖ, lông xám (người dùng 2026-11-13)

Chọn `kiem_cun`; lông đổi sang xám nhạt hơn dạng lớn bằng mã (`py -3 -I ArtGen/Spine/kiem_si_non_long.py` → `L2_kiem_cun_6f6a63.png`);
"kiếm cùn ở trong, bao kiếm ở ngoài bằng gỗ". Bố cục `py -3 -I ArtGen/Spine/kiem_si_non.py bo_cuc_bao` (cùng hệ toạ độ với `bo_cuc_tran`).

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\kiem_si_non\luot_3_concept_bao_go.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L3_bao_go.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_non/luot_3_concept_bao_go.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\mau\bo_cuc_bao.png` | Bố cục (1536 × 1024, nền trắng): rig dạng 1 không giáp, có VỎ kiếm dài chéo từ trên trái xuống tay gần, kiếm cách ở miệng vỏ, chuôi qua tay xa. Lấy chỗ đặt vỏ, kiếm cách, chuôi |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L2_kiem_cun_6f6a63.png` | Concept đã chọn, lông đã đổi xám (1536 × 1024, nền trắng): khỉ con chibi, khăn trán xanh, váy lá, cầm kiếm cũ trần. Giữ y con này |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_1\tai_ve\L1_duyet.png` | Dạng lớn: chỉ xem cách cầm kiếm trong vỏ (tay gần nắm vỏ sát miệng, tay xa nắm chuôi) |

## Lượt 4: mảnh của dạng 1 (concept duyệt 2026-11-13, người dùng: "duyệt, làm hết 1 lượt đi")

Sinh bằng `py -3 -I ArtGen/Spine/kiem_si_non_manh.py to` (tờ hướng dẫn `inbox/kiem_si_non/mau/to_<tờ>.png`); cắt bằng `... cat`. Mảnh lông / da khác là mảnh dạng lớn đổi màu bằng mã (`... doi_mau`).

### `N1`: tờ thân 1: đầu chibi có khăn trán, hai đuôi khăn, đai dây leo

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\kiem_si_non\luot_4_manh_N1.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\N1.png` (trùng tên thì `_2`, `_3`…).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\mau\to_N1.png` | Tờ hướng dẫn 1536 × 1024 nền trắng: bốn ô: đầu cũ mờ trong viền xám (chỗ mắt, mõm, bờm) + vùng chấm phía trên, hai dải vải lục, đai dây thừng lục. Giữ đúng hình bóng, chỗ, cỡ |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L3_bao_go.png` | Concept dạng 1 đã duyệt: lấy kiểu, màu, nét |

### `N2`: tờ thân 2: hai cẳng tay lông, hai ống chân lông, váy lá

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\kiem_si_non\luot_4_manh_N2.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\N2.png` (trùng tên thì `_2`, `_3`…).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\mau\to_N2.png` | Tờ hướng dẫn 1536 × 1024 nền trắng: năm hình bóng phẳng viền nâu: hai cẳng tay xám, váy lục, hai ống chân xám. Giữ đúng hình bóng, chỗ, cỡ |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L3_bao_go.png` | Concept dạng 1 đã duyệt: lấy kiểu, màu, nét |

### `S`: tờ kiếm: vỏ gỗ, lưỡi cùn, chuôi quấn vải + kiếm cách gỗ

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\kiem_si_non\luot_4_manh_S.txt`. Ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\S.png` (trùng tên thì `_2`, `_3`…).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\mau\to_S.png` | Tờ hướng dẫn 1536 × 1024 nền trắng: ba hình bóng nằm ngang, mũi bên trái: vỏ nâu, lưỡi xám, chuôi be có kiếm cách to ở đầu trái. Giữ đúng hình bóng, chỗ, cỡ |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L3_bao_go.png` | Concept dạng 1 đã duyệt: lấy kiểu, màu, nét |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_non\tai_ve\L2_kiem_cun_6f6a63.png` | Concept lông xám có lưỡi kiếm cùn lộ ra: chỉ lấy kiểu lưỡi (mẻ, gỉ, mũi gãy tròn) |

## Kiểm

- Lượt 4: mỗi mảnh trùng hình bóng của ô (cẳng tay, ống chân, váy IoU ≥ 0,95 là đạt); đầu có khăn, một mắt, không nanh, không đuôi khăn
  (đuôi khăn là mảnh riêng); kiếm: ba mảnh nằm ngang kín hết bề dài ô, mũi bên trái, mũi vỏ tròn kín. Script `cat` tự canh trục kiếm về giữa ảnh.
- Lượt 3: y con ở ảnh 2 (lông xám, khăn, váy lá, mặt), kiếm nằm TRONG vỏ gỗ trơn (không lộ lưỡi), tay gần nắm vỏ sát miệng, kiếm cách ở miệng vỏ,
  tay xa nắm chuôi quấn vải; vỏ chạy chéo lên trái sau tay gần như ảnh 1.
- Lượt 2: khỉ con lông cam, chibi dễ thương nhưng ánh mắt quả quyết; **không giáp, không mũ, không vỏ kiếm, không kiếm thứ hai**; đúng một
  vũ khí hai tay cùng nắm, chĩa lên trái như ảnh 1; cẳng tay, ống chân là lông (không bao tay, giáp ống); đai dây leo + váy lá; đuôi cong ở trên trái.
- Voọc non **nhìn sang phải**, đầu to, **một mắt** to tròn có nét mày quả quyết (không cười, không buồn), không nanh.
- Dáng, chỗ đặt, cỡ từng mảnh trùng ảnh 1; tấm vai, giáp ngực, đai thừng, bao tay, kiếm, áo tơi, chân **giữ hình**, chỉ đổi màu.
- Cả hai kiếm còn trong vỏ, không lộ lưỡi; đủ bốn tua; một đuôi.
- Màu đúng bảng của hướng, nhạt hơn dạng lớn; tô phẳng, không bóng; nền trắng.

Gửi thêm khi sai: `Keep the pose, proportions and piece outlines of image 1 exactly.` · `Flat colour only, remove shadows and highlights.` ·
`Only one eye, head in three-quarter profile facing right.` · `Keep the swords fully sheathed, no bare blade.`
