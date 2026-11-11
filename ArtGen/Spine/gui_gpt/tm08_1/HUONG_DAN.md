# Gói gửi GPT: Uyên Nhi (dạng 1, chibi) (`tm08_1`)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_1\luot_1_concept.txt`. GPT lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm08_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`...).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_1\luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\thuong_lam_1\tai_ve\L1_lien.png` | Rồng băng Thương Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): lấy nét, tỉ lệ chibi; không chép dáng, màu |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\tm08_2\tai_ve\L1_duyet.png` | Concept dạng 2 (Uyên Xà) đã chọn (1536 × 1024, nền trắng): cùng dòng, bé con phải nhận ra là cùng loài |

## Kiểm concept

- Bé rắn biển chibi (đầu ~45%), nhìn sang **phải**, ngồi trên vòng đuôi hở hình chữ C, vây đuôi nhỏ chìa sang trái.
- Thân chàm xám `#5058A8` nhạt hơn dạng 2, bụng bạc hà, ba chấm tròn, vây mào bạc hà mềm to như mào gà úp về sau, hai râu cằm ngắn đầu hạt đèn.
- Mắt to tròn hổ phách, mày nhíu, hàm dưới trề nhỏ một răng; một mấu xương trắng sau gáy.
- Nhận ra cùng dòng với concept dạng 2 nhưng dễ thương, quả quyết; không linh vật vui tươi.
- Tô phẳng, không bóng, nền trắng, không nước, không đất.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng | `Flat colour only: remove every shadow, highlight, glow and gradient; keep the crayon hatching as texture.` |
| Nhìn sang trái | `The head must face the viewer's RIGHT.` |
| Có chân, tay, cánh | `This is a legless, wingless sea serpent: remove all legs, arms, claws and wings.` |
| Thân vắt chéo nhau | `The body must be ONE open S-curve: no part of the body passes in front of or behind another part.` |
| Có tai, vây tai, gạc | `No ears, no ear fins, no antlers: only the three bone-white spines on the back of the skull (one soft nub for the baby).` |
| Có nước, đất, nền | `Pure white background only: no water, no ground, no rocks.` |
| Dạng 2 vẫn chibi | `Not chibi at all: adult proportions, the head about one sixth of the figure's height, small fierce eye.` |

## Tờ mảnh `luot_2_manh.txt`: `D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_1\luot_2_manh.txt`

Các bước M01, M02, gõ `next` sau mỗi ảnh; GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm08_1\tai_ve`. Ảnh mẫu thêm: ảnh 3 = `D:\PokiClash\ArtGen\Spine\inbox\tm08_1\tai_ve\L1_duyet.png`.
Claude tự gen: `py -3 -I ArtGen/Spine/gen.py D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_1\luot_2_manh.txt --steps M01,M02`.

Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px, không vẽ cả con; ống thân, râu, lưỡi **thẳng nằm ngang**, gốc bên trái; đầu chỉ phần trên (không hàm dưới, không cổ).
- **M01**: đầu tròn (phần trên, có mấu xương), hàm dưới nhỏ, lòng miệng + lưỡi, mí + vây ngực, mào vây to dựng đứng gốc ở mép dưới, râu ngắn có hạt đèn + vây đuôi nhỏ
- **M02**: ống thân ngắn duỗi thẳng ~950 px: trái = cổ (dày 150), phải = đuôi (dày 55), vây lưng thấp mép trên, ba chấm, tấm bụng

| Sai | Gửi thêm |
|---|---|
| Vẽ cả con | `This must be a sheet of separate parts laid flat on white, not a creature or a scene. Redraw only the parts listed.` |
| Ống thân cong | `The body tube must be perfectly straight and horizontal, like a ruler, both ends rounded.` |
| Đầu dính hàm dưới / cổ | `The head part is the UPPER part only: no lower jaw, no neck; the lower jaw is its own separate part.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |

## Tờ mảnh `luot_3_than_cong.txt`: `D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_1\luot_3_than_cong.txt`

Các bước M03, gõ `next` sau mỗi ảnh; GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm08_1\tai_ve`. Ảnh mẫu thêm: ảnh 3 = `D:\PokiClash\ArtGen\Spine\inbox\tm08_1\tai_ve\L1_duyet.png`.
Claude tự gen: `py -3 -I ArtGen/Spine/gen.py D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_1\luot_3_than_cong.txt --steps M03`.

Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px, không vẽ cả con; ống thân, râu, lưỡi **thẳng nằm ngang**, gốc bên trái; đầu chỉ phần trên (không hàm dưới, không cổ).
- **M03**: thân cong đúng dáng concept (cổ lên, bụng tròn, đuôi mảnh vòng ra trước), không đầu, không mào, không vây ngực, không vây đuôi

| Sai | Gửi thêm |
|---|---|
| Vẽ cả con | `This must be a sheet of separate parts laid flat on white, not a creature or a scene. Redraw only the parts listed.` |
| Ống thân cong | `The body tube must be perfectly straight and horizontal, like a ruler, both ends rounded.` |
| Đầu dính hàm dưới / cổ | `The head part is the UPPER part only: no lower jaw, no neck; the lower jaw is its own separate part.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |
