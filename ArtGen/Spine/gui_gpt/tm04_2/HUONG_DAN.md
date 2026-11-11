# Gói gửi GPT: dòng tm04 (đề xuất tên **Hà Bá**, hà mã nước)

Lô 10 tướng mới đảo Thủy, dòng 4 (thay suất ải 15, Mi Nhi). Hai dạng: **Hà Mã Con** (chibi) → **Hà Bá** (dạng cuối, chiến mã hà mã giáp đồng). Mỗi dạng một file prompt, gen dạng 1 trước; file dạng 2 chỉ có sau khi đã chọn concept dạng 1 (`inbox/tm04_1/tai_ve/L1_chon.png` hoặc `L1_duyet.png`).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm04_<k>/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh). Người dùng tự gửi thì **chỉ gửi GPT đường dẫn file prompt**, GPT tự mở ảnh mẫu và tự lưu.

## Dạng 1

**File prompt:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm04_1\luot_1_concept.txt`

**GPT lưu ảnh vào:** `D:\PokiClash\ArtGen\Spine\inbox\tm04_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…)

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\huyen_vu_1\tai_ve\L1_lien.png` | Rùa Ngọc (Huyền Vũ dạng 1) đã duyệt (1536 × 1024, nền trắng): rùa xanh lá chibi bốn chân tách rời, quay phải. Lấy nét, vân sáp, dáng bốn chân; không chép loài, mai, màu |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\canh_cut_1\tai_ve\L1_lien.png` | Cánh Cụt Con đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi cầm chảo, mắt cau quả quyết. Lấy tỉ lệ chibi, mắt, cách tô; không chép loài, màu |
| 4 | `D:\PokiClash\Assets\03 Art\Fx\xoay_nuoc.png` | Vòng nước xoáy đã duyệt của game (384 × 362, nền trong): mào sóng cuộn, ba màu lam phẳng, bọt trắng. Mẫu cho linh hồn nước ở đuôi |

**Kiểm:**

- Hà mã con chibi tròn như quả bóng (đầu khoảng nửa hình, rộng ≈ cao), **quay sang phải**, **đúng bốn chân** (đếm bàn chân: 4) ngắn, tách rời nhau, không chéo.
- Thân xanh xám đá `#7A93BE`, mõm/cằm/bụng hồng đào nhạt, vài đốm bọt xanh nhạt trên lưng.
- Ba vây buồm tròn màu bạc hà có gai sẫm dọc lưng (không phải hai lá nhọn vàng), tai hình vây nhỏ.
- Mõm hà mã hình hạt đậu có hai lỗ mũi, miệng hé thấy lòng miệng hồng và lưỡi, hai nanh cụt nhô lên từ hàm dưới.
- Hai mắt tròn nằm cao trên đỉnh đầu, tròng vàng, mày cau quả quyết (không cười kiểu linh vật).
- Đuôi ngắn, chóp là một mào sóng nước cuộn có bọt trắng (không phải ngọn lửa), đứng tách khỏi lưng.
- Tô phẳng, không bóng (kể cả dưới chân), không điểm sáng (trừ chấm mắt), nền trắng tinh, không đường đất.

## Dạng 2

**File prompt:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm04_2\luot_1_concept.txt`

**GPT lưu ảnh vào:** `D:\PokiClash\ArtGen\Spine\inbox\tm04_2\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…)

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\vay_lam_3\tai_ve\L1_lien.png` | Cá Mập Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): cá mập bốn chân dữ, thế lao. Lấy nét, vẻ dữ, thế đứng; không chép loài, màu |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\ma_ket_3\tai_ve\L1_lien.png` | Ma Kết Thánh Giáp dạng 3 đã duyệt (1536 × 1024, nền trắng): dê giáp vàng. Lấy mức giáp, cách vẽ giáp tô phẳng; không chép loài, sừng, màu |
| 4 | `D:\PokiClash\Assets\03 Art\Fx\xoay_nuoc.png` | Vòng nước xoáy đã duyệt của game (384 × 362, nền trong): mào sóng cuộn. Mẫu cho linh hồn nước ở đuôi |
| 5 | `D:\PokiClash\ArtGen\Spine\inbox\tm04_1\tai_ve\L1_duyet.png` | Concept dạng 1 đã chọn (1536 × 1024, nền trắng): Hà Mã Con chibi xanh xám, vây bạc hà, đuôi sóng nước |

**Kiểm:**

- Hà mã trưởng thành to, nặng, **không chibi** (đầu khoảng 1/3 hình), thế lao thấp, quay sang phải.
- Thân chàm xám đậm `#404C86` (không tím, không lam tươi của Vây Lam) có vằn sẫm, mõm/bụng kem cát; nhìn bóng dáng đã thấy khác dạng 1.
- Đúng bốn chân đặt như thú bốn chân: hai chân sau dưới mông (bên trái), hai chân trước dưới vai; không chân nào mọc dưới đầu.
- Giáp đồng vừa phải: tấm che trán có gờ hình mào sóng, vòng cổ có ngọc, giáp vai; ngà dài cong có khâu đồng.
- Bốn vây buồm cao hình mào sóng cuộn, xanh két sẫm, mũ bọt trắng; đuôi mang con sóng hai mào to.
- Mắt hẹp, dữ, tròng hổ phách; miệng há gầm thấy lòng miệng, răng.
- Còn nhận ra cùng dòng: mõm hạt đậu hai lỗ mũi, mắt trên đỉnh đầu, tai vây, vây buồm lưng, đuôi sóng.
- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh.

## Lượt 2, dạng 1: tờ mảnh (cách lai)

Thân, đầu trên, vây, đuôi sóng, chân gần, giáp, hàm dưới cắt thẳng từ concept đã duyệt (`ArtGen/Spine/tm04.py`). GPT chỉ vẽ phần bị che hoặc không có trên concept.

**File prompt:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm04_1\luot_2_manh.txt`; GPT lưu `D:\PokiClash\ArtGen\Spine\inbox\tm04_1\tai_ve\M01.png`.

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm04_1/luot_2_manh.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\tm04_1\tai_ve\L1_duyet.png` | Concept dạng 1 đã duyệt (1536 × 1024, nền trắng) |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\hai_long\tai_ve\M01.png` | Tờ mảnh đầu Hải Long đã duyệt (1536 × 1024, nền trắng): chỉ để GPT hiểu cách bày tờ mảnh |
| 3 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ (1024 × 1536): bản đồ vẽ tay; chỉ lấy nét |

**Kiểm M01:** mảng lòng miệng (220 × 150), mí nhắm mắt gần (110 × 105), mí nhắm mắt xa (70 × 85), chân trước xa vẽ trọn (120 × 170), chân sau xa vẽ trọn (120 × 170), ô cuối để trống; mỗi mảnh rời nhau ít nhất 70 px, nền trắng, đúng màu concept, chân đứng thẳng có đầu trên tròn, mí che kín mắt.

## Lượt 2, dạng 2: tờ mảnh (cách lai)

Thân, đầu trên, vây, đuôi sóng, chân gần, giáp, hàm dưới cắt thẳng từ concept đã duyệt (`ArtGen/Spine/tm04.py`). GPT chỉ vẽ phần bị che hoặc không có trên concept.

**File prompt:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm04_2\luot_2_manh.txt`; GPT lưu `D:\PokiClash\ArtGen\Spine\inbox\tm04_2\tai_ve\M01.png`.

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm04_2/luot_2_manh.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\tm04_2\tai_ve\L1_duyet.png` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng) |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\hai_long\tai_ve\M01.png` | Tờ mảnh đầu Hải Long đã duyệt (1536 × 1024, nền trắng): chỉ để GPT hiểu cách bày tờ mảnh |
| 3 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ (1024 × 1536): bản đồ vẽ tay; chỉ lấy nét |

**Kiểm M01:** mảng lòng miệng to (300 × 220), mí nhắm mắt gần (110 × 80), mí nhắm mắt xa (80 × 65), chân trước xa vẽ trọn (260 × 400), chân sau xa vẽ trọn (280 × 400), ô cuối để trống; mỗi mảnh rời nhau ít nhất 70 px, nền trắng, đúng màu concept, chân đứng thẳng có đầu trên tròn, mí che kín mắt.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, bóng dưới chân | `Flat colour only: remove every shadow (also under the feet), highlight and gradient; keep the crayon hatching as texture.` |
| Quay sang trái | `The creature must face the viewer's RIGHT: muzzle and eyes toward the right edge.` |
| Đuôi thành ngọn lửa | `The tail spirit is WATER: one plump curling wave crest with round white foam, no flame shapes.` |
| Chân dính nhau, chéo nhau | `All four legs clearly separated, none crossing; the far legs visible between the near legs.` |
| Dạng 1 cười kiểu linh vật | `Determined, ready-to-fight face with frowning brows, mouth open but not smiling.` |
| Dạng 2 vẫn chibi | `Not chibi at all: adult heavy war hippo, head about one third of the figure, thick pillar legs.` |
