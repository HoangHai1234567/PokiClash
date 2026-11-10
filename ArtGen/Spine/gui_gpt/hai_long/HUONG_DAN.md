# Gói gửi GPT: Hải Long Ngũ Đầu (`hai_long`)

Quái năm đầu trồi lên từ sóng, làm theo cách dựng đã mổ xẻ ở `.claude/skills/skill-petclash/mo_xe_quai_nhieu_dau.md`. Con nhiều cổ chồng nhau không rig được từ một ảnh liền, nên có hai lượt: concept trọn con, rồi bốn tờ mảnh rời.

**Lượt 1, chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\hai_long\luot_1_concept.txt`. GPT lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hai_long\tai_ve\L1_concept.png`.

**Lượt 2** (Claude dựng file sau khi chép concept đã chọn thành `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hai_long\tai_ve\L1_duyet.png`): `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\hai_long\luot_2_manh.txt`, bốn bước M01, M02, M03, M04, gõ `next` sau mỗi ảnh. GPT lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hai_long\tai_ve`.

Claude tự gen: `py -3 -I gen.py gui_gpt/hai_long/luot_1_concept.txt`, rồi `py -3 -I gen.py gui_gpt/hai_long/luot_2_manh.txt --steps M01,M02,M03,M04`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thuong_lam_3\tai_ve\L1_lien.png` | Rồng băng Thương Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): lấy nét bút, vân sáp, mức chi tiết; không chép dáng |
| 3 | `C:\Atomik\PokiWar\Assets\03 Art\Fx\no_nuoc.png` | Vụ nước toé đã duyệt của game (512 × 505, nền trong): mũi nước mập, bọt tròn, ba màu lam phẳng |
| 4 | `C:\Atomik\PokiWar\Assets\03 Art\Fx\xoay_nuoc.png` | Vòng nước xoáy đã duyệt của game (384 × 362, nền trong): dòng nước có mào sóng cuộn |
| 5 (chỉ lượt 2) | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hai_long\tai_ve\L1_duyet.png` | Concept Hải Long đã duyệt (1536 × 1024, nền trắng) |

## Kiểm concept (lượt 1)

- Năm đầu rồng nhìn nghiêng, **đều quay sang phải**, không đầu nào che đầu nào; đầu giữa to nhất, có gạc lớn và ngọc trán.
- Vảy xanh ngọc, bụng kem vàng, vây và bờm đỏ san hô, gạc vàng, râu kem.
- Nước ba màu lam phẳng, bọt trắng tròn, viền mực nâu; sóng trước che chỗ cổ mọc ra.
- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh.

## Kiểm tờ mảnh (lượt 2): mỗi tờ 1536 × 1024, nền trắng, các mảnh rời nhau ít nhất 60 px

- **M01**: đầu thủ lĩnh (phần trên, có gạc, ngọc, bờm vây), hàm dưới thủ lĩnh, mảng lòng miệng, đầu thường (phần trên), hàm dưới thường, một sợi râu + một chùm vây
- **M02**: cổ to duỗi thẳng (1380 × 190), cổ nhỏ duỗi thẳng (1380 × 140), một vòng thân hình chữ U úp, chóp đuôi có vây
- **M03**: sáu hình nước rời: mào sóng to cuộn phải, mào sóng to cuộn trái, sóng đôi vừa, cuộn nhỏ, dải sóng thấp, cụm bọt
- **M04**: dải mặt nước dài có hàng mào sóng, mô nước nền xanh đậm, vương miện nước toé, ba giọt nước, một vòng sóng dẹt

## Lượt 3 (chiêu phun nước, mí mắt): `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\hai_long\luot_3_phun_nuoc.txt`

Một bước M05, GPT lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hai_long\tai_ve`. Ảnh mẫu thêm: ảnh 6 = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hai_long\tai_ve\M01.png` (tờ đầu đã duyệt, 1536 × 1024, nền trắng). Claude tự gen: `py -3 -I gen.py gui_gpt/hai_long/luot_3_phun_nuoc.txt --steps M05`.

- **M05**: tia nước to duỗi thẳng (1380 × 170), tia nước nhỏ (1380 × 105), vụ nổ nước chỗ tia chạm (xoè sang phải), loa nước ở miệng, ba vệt nước bay, hai mí mắt nhắm (to, nhỏ)

## Lượt 4 (lưỡi cho clip chết): `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\hai_long\luot_4_luoi.txt`

Một bước M06, GPT lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hai_long\tai_ve`, cùng sáu ảnh mẫu như lượt 3. Claude tự gen: `py -3 -I gen.py gui_gpt/hai_long/luot_4_luoi.txt --steps M06`.

- **M06**: hai cái lưỡi duỗi thẳng nằm ngang (to 320 px, nhỏ 260 px), hồng nhạt, chẻ nhẹ ở đầu, một nét giữa

## Lượt 5 (hình nước đợt hai): `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\hai_long\luot_5_nuoc.txt`

Một bước M07, GPT lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\hai_long\tai_ve`, cùng sáu ảnh mẫu như lượt 3. Claude tự gen: `py -3 -I gen.py gui_gpt/hai_long/luot_5_nuoc.txt --steps M07`.

- **M07**: dải sóng dài quét ngang (1000 × 200, mào cuộn ở đầu phải), cuộn xoắn nhỏ, vòi nước cao mảnh cuộn sang phải (130 × 400), vòi nước thấp mập hai móc, cuộn xoắn vừa, cuộn xoắn tí hon, dải gợn sóng lăn tăn (1300 × 120)
- Kiểm: hai tia **thẳng, nằm ngang**, đầu trái thuôn lại, không có nước toé dính vào; vụ nổ xoè sang **phải**; mí mắt là mảng xanh ngọc nhỏ có một nét cong sẫm.

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |
| Vẽ cả con thay vì mảnh rời | `This must be a sheet of separate parts laid flat on white, not a creature or a scene. Redraw only the parts listed.` |
| Cổ vẽ cong | `The necks must be perfectly straight horizontal tubes, like a ruler, both ends rounded.` |
| Đầu dính hàm dưới hoặc dính cổ | `The head part is the UPPER part only: no lower jaw, no neck; the lower jaw is its own separate part.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |
