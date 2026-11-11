# Gói gửi GPT: dòng tm03, dạng 1 (Nòng Xoáy)

Lô 10 tướng mới đảo Thủy (đặc tả `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`), pha 1: concept trọn con một ảnh. Ghi chú thiết kế cả dòng: `D:\PokiClash\ArtGen\Spine\inbox\tm03_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm03_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu theo đường dẫn ghi trong file và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm03_1\tai_ve\L1_concept.png` (trùng tên thì `L1_concept_2.png`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm03_1/luot_1_concept.txt` (chạy nền; thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\canh_cut_1\tai_ve\L1_lien.png` | Cánh Cụt Con đã duyệt (1536 × 1024, nền trắng): chim cánh cụt tròn xanh mòng két cầm chảo, nhìn sang phải. Lấy khung, cách đứng tách chân tay, nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\kuba_1\tai_ve\L1_lien.png` | Kuba dạng 1 đã duyệt (1536 × 1024, nền trắng): cua cam đeo pha lê, mặt quả quyết. Lấy nét bút, vân sáp, nét mặt |
| 3 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |

Không đính ảnh con gốc (game khác) hay ảnh chụp trang xem: thiết kế chỉ tả bằng lời.

## Kiểm ảnh

- Nòng nọc tròn mập, **nhìn sang phải**, mắt to lồi trên đỉnh đầu, tròng vàng hổ phách, **con ngươi ngang**, mí dày hạ xuống cho mặt quả quyết (không cười).
- Lưng xanh cerulean có 3–4 vằn lam đậm cuộn móc; bụng, cằm vàng chanh kem.
- Miệng rộng **hé**, thấy lòng miệng hồng đậm và chóp lưỡi hồng; không răng.
- Hai chân sau ngắn, hai chân trước tí hon, đệm ngón cam; các chân tách nhau và tách bụng bằng khe trắng.
- **Đuôi cuộn xoắn ốc** (khoảng 2,5 vòng) dựng sau mông bên trái, vây xanh nước nhạt, vằn lam đậm chạy theo vòng; đuôi không đè lên thân, mắt.
- Tô phẳng, không bóng, không điểm sáng trên da (trừ chấm mắt), nền trắng tinh, không giọt nước, không bong bóng.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng trên da | `Flat colour only: remove every shadow, highlight, shine spot and gradient; keep the crayon hatching as texture; only one small catchlight dot in each eye.` |
| Quay sang trái | `Mirror the creature so it faces the viewer's RIGHT.` |
| Mặt cười, vui tươi | `More determined face: heavy lowered brows, focused eyes, mouth slightly open, not a happy grin.` |
| Miệng khép | `Open the mouth slightly so the deep-rose inside of the mouth and the tongue are visible.` |
| Chân tay dính nhau, dính thân | `Leave clear white gaps between the legs and between the legs and the body.` |
| Đuôi không cuộn xoắn hoặc đè lên thân | `The tail must coil up into a big flat spiral (about two and a half turns) standing behind the body on the viewer's left, touching the body only at its root.` |
| Giống một con vật quen trong game khác (bụng trắng có xoắn ốc) | `The belly is plain lemon cream with no spiral; the only spirals are on the coiled tail and the small stripe hooks on the back.` |

## Lượt 2: tờ mảnh (cách lai: thân chính cắt từ concept, tờ này chỉ cho phần tách / bị che)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm03_1\luot_2_manh.txt`, các bước M01, M02 (gõ `next` sau mỗi ảnh). GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm03_1\tai_ve`.

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm03_1/luot_2_manh.txt --steps M01,M02`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\tm03_1\tai_ve\L1_duyet.png` | Concept dạng 1 đã duyệt (1536 × 1024, nền trắng) |
| 2 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ (1024 × 1536) |

Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px, đúng cỡ và hình như trên concept, tô phẳng.

- **M01**: quả bóng thân (không mắt, không chân, không đuôi; nguồn vẽ bù), mắt gần nhắm, mắt xa nhắm, lòng miệng có lưỡi, lưỡi duỗi
- **M02**: đuôi duỗi thẳng (1400 px, gốc 115 px thuôn còn 24 px, vây hai mép, 11 vằn), chân sau gần, chân trước gần, chân trước xa (ngắn hơn concept 15 %, mập hơn)

| Sai | Gửi thêm |
|---|---|
| Mảnh khác hình, khác cỡ concept | `Draw each part with the same silhouette, proportions and size as on image 1.` |
| Đuôi vẽ cong | `The tail must be a ruler-straight horizontal ribbon, root on the left, tapering to the tip on the right.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |
