# Gói gửi GPT: Uyên Xà (dạng 2, trưởng thành) (`tm08_2`)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_2\luot_1_concept.txt`. GPT lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm08_2\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`...).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_2\luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\thuong_lam_3\tai_ve\L1_lien.png` | Rồng băng Thương Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): lấy nét bút, vân sáp, tỉ lệ trưởng thành; không chép dáng, màu |

## Kiểm concept

- Rắn biển thân dài không chân, không cánh, nhìn nghiêng sang **phải**; thân một đường S hở: đuôi trái, bướu giữa, phần trước dựng đứng, không vắt chéo.
- Thân chàm vực sâu `#2E2F6E`, bụng bạc hà trăng `#D8F3EA` chia tấm, một hàng chấm tròn bạc hà dọc sườn, vây lưng liền một dải bạc hà `#8FE3D0` có vân tia, đuôi vây mái chèo hai thuỳ.
- Đầu dài hẹp, hàm dưới trề, mày nhíu, mắt hổ phách `#F2B544` đồng tử dọc; miệng hé thấy lòng miệng mận `#5A2A5E`, hai nanh kem; ba gai xương trắng sau gáy; hai râu cằm đầu hạt đèn.
- Tỉ lệ trưởng thành (đầu ~1/6 chiều cao), vẻ chiến; không tai, không gạc, không bờm.
- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh, không nước, không đất.

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

## Tờ mảnh `luot_2_manh.txt`: `D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_2\luot_2_manh.txt`

Các bước M01, M02, gõ `next` sau mỗi ảnh; GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm08_2\tai_ve`. Ảnh mẫu thêm: ảnh 3 = `D:\PokiClash\ArtGen\Spine\inbox\tm08_2\tai_ve\L1_duyet.png`.
Claude tự gen: `py -3 -I ArtGen/Spine/gen.py D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_2\luot_2_manh.txt --steps M01,M02`.

Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px, không vẽ cả con; ống thân, râu, lưỡi **thẳng nằm ngang**, gốc bên trái; đầu chỉ phần trên (không hàm dưới, không cổ).
- **M01**: đầu (phần trên, có ba gai gáy, nanh), hàm dưới rời, mảng lòng miệng + lưỡi thẳng, mí nhắm + một vây ngực, một râu thẳng có hạt đèn ở đầu phải, vây đuôi mái chèo hai thuỳ gốc bên trái
- **M02**: ống thân duỗi thẳng nằm ngang ~1450 px: trái = đầu cổ (dày 150), phải = đuôi (dày 70), vây lưng liền dọc mép trên, hàng chấm, tấm bụng mép dưới

| Sai | Gửi thêm |
|---|---|
| Vẽ cả con | `This must be a sheet of separate parts laid flat on white, not a creature or a scene. Redraw only the parts listed.` |
| Ống thân cong | `The body tube must be perfectly straight and horizontal, like a ruler, both ends rounded.` |
| Đầu dính hàm dưới / cổ | `The head part is the UPPER part only: no lower jaw, no neck; the lower jaw is its own separate part.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |

## Tờ mảnh `luot_3_vay_lung.txt`: `D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_2\luot_3_vay_lung.txt`

Các bước M03, gõ `next` sau mỗi ảnh; GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm08_2\tai_ve`. Ảnh mẫu thêm: ảnh 3 = `D:\PokiClash\ArtGen\Spine\inbox\tm08_2\tai_ve\L1_duyet.png`.
Claude tự gen: `py -3 -I ArtGen/Spine/gen.py D:\PokiClash\ArtGen\Spine\gui_gpt\tm08_2\luot_3_vay_lung.txt --steps M03`.

Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px, không vẽ cả con; ống thân, râu, lưỡi **thẳng nằm ngang**, gốc bên trái; đầu chỉ phần trên (không hàm dưới, không cổ).
- **M03**: vây lưng gợn rời duỗi thẳng ~1450 px, mép gốc thẳng ở dưới, mép ngoài gợn to, trái = cổ (cao 170), phải = đuôi (cao 70)

| Sai | Gửi thêm |
|---|---|
| Vẽ cả con | `This must be a sheet of separate parts laid flat on white, not a creature or a scene. Redraw only the parts listed.` |
| Ống thân cong | `The body tube must be perfectly straight and horizontal, like a ruler, both ends rounded.` |
| Đầu dính hàm dưới / cổ | `The head part is the UPPER part only: no lower jaw, no neck; the lower jaw is its own separate part.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |
