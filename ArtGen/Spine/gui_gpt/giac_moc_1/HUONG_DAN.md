# Gói gửi GPT: `giac_moc` (thú một sừng bốn chân, tướng thứ 9 đảo Mộc, suất `moc_tinh`, tên chưa đặt)

Làm 2026-11-13: dựng trên rig của con gốc `monster_3804` (thú bốn chân một sừng, 136 mảnh lưới, vỏ ngực trượt mở). Hai hướng thiết kế là đề xuất của Claude, chờ người dùng chọn và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/giac_moc_ghichu.md`.

Mỗi hướng hai ảnh: `luot_1_concept_<hướng>.txt` (dáng nghỉ, ngực đóng) rồi `luot_1b_mo_nguc_<hướng>.txt` (ngẩng cao, ngực mở, lộ quả tim; chỉ dựng khi đã có ảnh dáng nghỉ). Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).

## Hướng `co_thu`: thú cổ thụ: thân vỏ cây nâu, sừng gỗ ngọn hổ phách, lưng dương xỉ + dây leo + tinh thể hổ phách, ngực là thùng vỏ cây

### Lượt 1: dáng nghỉ

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_1_concept_co_thu.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1_co_thu.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/giac_moc_1/luot_1_concept_co_thu.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\bo_cuc_co_thu_nghi.png` | Sơ đồ bố cục tự dựng bằng mã (1024 × 1536, nền trắng), dáng nghỉ: các khối tô phẳng theo nhóm màu (sừng ngọn khác màu ở trên phải; đầu một mắt; mào lá dài sau đầu; bờm lưng to bay sang trái; hàng tấm nhạt xen mảnh nhọn dọc sống lưng; thân; bầu ngực tròn sẫm phía trước; bốn chân). Lấy chỗ đặt, cỡ, thứ tự chồng |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\nguoi_cay_2\tai_ve\L1_duyet.png` | Người cây đầm lầy đã duyệt (1536 × 1024, nền trắng): quái rêu lục vai u, nắm tay gỗ. Lấy nét bút rung, vân sáp, tô phẳng, thần thái chiến |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\voi_rung_2\tai_ve\L1_duyet.png` | Voi rừng đã duyệt (1536 × 1024, nền trắng): thú bốn chân phủ lá. Lấy nét, tô phẳng, cách vẽ lá to và bốn chân |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp |

Kiểm riêng hướng này:

- Thân là **vỏ cây nâu**, không phải cây có chân, không phải bộ xương; sừng gỗ sẫm có vòng, **ngọn là tinh thể hổ phách**.
- Lưng: **dương xỉ + lá to + tua dây leo**; hàng sống lưng xen **4 tấm gai gỗ nhạt** và **5 tinh thể hổ phách**.
- Ngực: **thùng vỏ cây sẫm** khoảng 10 tấm, **khe sáng vàng hổ phách**, vành là dây leo quấn; cột tấm sườn gỗ nhạt cạnh chân trước.

### Lượt 1b: ngẩng cao, mở ngực, lộ quả tim

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_1b_mo_nguc_co_thu.txt`. GPT tự lưu vào `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1b_co_thu_mo.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1_co_thu.png` | Concept dáng nghỉ của chính hướng này (1024 × 1536, nền trắng): con vật, màu, nét phải giữ y nguyên |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\bo_cuc_co_thu_mo.png` | Sơ đồ bố cục dáng mở ngực (1024 × 1536, nền trắng): sừng dựng thẳng, đầu ngửa, khoang ngực sẫm dài phía trước có quả cầu sáng tròn ở nửa dưới, các tấm vỏ dồn thành dải hẹp bên trái khoang. Lấy chỗ đặt, cỡ, thứ tự chồng |

Kiểm: cùng một con với ảnh dáng nghỉ (màu, chi tiết); sừng dựng thẳng lên; khoang ngực mở dài phía trước cổ và ngực; Lòng ngực sẫm có vài sợi rễ nhạt ôm lấy **quả tim tròn vàng hổ phách** (có một vòng sẫm hơn và một dấu xoắn / hạt ở giữa). Các tấm vỏ dồn sang trái khoang; không quầng sáng, không tia.

## Hướng `bach_thu`: bạch thú hoa: thú lông trắng kem, sừng gỗ xoắn ngọn vàng, lưng lá to + dây leo + nụ sen hồng, ngực là một nụ hoa khổng lồ

### Lượt 1: dáng nghỉ

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_1_concept_bach_thu.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1_bach_thu.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/giac_moc_1/luot_1_concept_bach_thu.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\bo_cuc_bach_thu_nghi.png` | Sơ đồ bố cục tự dựng bằng mã (1024 × 1536, nền trắng), dáng nghỉ: các khối tô phẳng theo nhóm màu (sừng ngọn khác màu ở trên phải; đầu một mắt; mào lá dài sau đầu; bờm lưng to bay sang trái; hàng tấm nhạt xen mảnh nhọn dọc sống lưng; thân; bầu ngực tròn sẫm phía trước; bốn chân). Lấy chỗ đặt, cỡ, thứ tự chồng |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\nguoi_cay_2\tai_ve\L1_duyet.png` | Người cây đầm lầy đã duyệt (1536 × 1024, nền trắng): quái rêu lục vai u, nắm tay gỗ. Lấy nét bút rung, vân sáp, tô phẳng, thần thái chiến |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\voi_rung_2\tai_ve\L1_duyet.png` | Voi rừng đã duyệt (1536 × 1024, nền trắng): thú bốn chân phủ lá. Lấy nét, tô phẳng, cách vẽ lá to và bốn chân |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp |

Kiểm riêng hướng này:

- **Thú sống lông trắng kem** (không phải cây có chân); sừng gỗ xoắn, **ngọn vàng** hình nụ; mũi nâu, tai lá nhỏ.
- Lưng: **lá to + tua dây leo + hoa trắng nhỏ**; hàng sống lưng xen **4 đài hoa lục nhạt** và **5 nụ sen hồng**.
- Ngực: **một nụ sen khổng lồ** khoảng 10 cánh hồng sẫm, **khe sáng vàng**, đài hoa lục ôm phía trước; cột cánh hồng nhạt cạnh chân trước.

### Lượt 1b: ngẩng cao, mở ngực, lộ quả tim

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_1b_mo_nguc_bach_thu.txt`. GPT tự lưu vào `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1b_bach_thu_mo.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1_bach_thu.png` | Concept dáng nghỉ của chính hướng này (1024 × 1536, nền trắng): con vật, màu, nét phải giữ y nguyên |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\bo_cuc_bach_thu_mo.png` | Sơ đồ bố cục dáng mở ngực (1024 × 1536, nền trắng): sừng dựng thẳng, đầu ngửa, khoang ngực sẫm dài phía trước có quả cầu sáng tròn ở nửa dưới, các tấm vỏ dồn thành dải hẹp bên trái khoang. Lấy chỗ đặt, cỡ, thứ tự chồng |

Kiểm: cùng một con với ảnh dáng nghỉ (màu, chi tiết); sừng dựng thẳng lên; khoang ngực mở dài phía trước cổ và ngực; Lòng nụ hoa hồng rượu, vòng **nhị vàng** quanh **quả tim tròn vàng** (có một vòng sẫm hơn và một dấu xoắn / hạt ở giữa). Các tấm vỏ dồn sang trái khoang; không quầng sáng, không tia.

Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/giac_moc_bo_cuc.py all all`).

## Kiểm chung (dáng nghỉ)

- Thú **bốn chân** to nặng, vai cao hơn mông, nhìn sang PHẢI, chỉ lộ **một mắt**, **mồm ngậm**, không đuôi.
- **Một sừng** lớn mọc từ sống mũi chĩa lên phía trên bên phải, ngọn khác màu.
- Mào đầu **bốn lá dài** quét ra sau; bờm lưng khoảng mười mảnh lớn bay về bên trái.
- **Bầu ngực** tròn to phía trước giữa hai chân trước, đang ĐÓNG, có khe sáng mảnh (không quầng sáng).
- Bốn chân trụ, mỗi bàn **bốn ngón có móng**.
- Tô phẳng: **không** bóng, không mảng sáng tối, không điểm sáng, không quầng; nền trắng tinh; hình nằm ở 2/3 dưới của khung.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Vẽ thành linh vật dễ thương / chibi | `It is a huge fierce final-stage guardian beast: small head on a massive body, stern eye, no smile.` |
| Giống rùa cóc có hoa trên lưng | `Not a toad or turtle: long pillar legs, high shoulders, a neck, a horned wedge head; the back carries a mane of many leaves, not one flower.` |
| Thiếu chân / chân lẫn vào nhau | `All FOUR legs must be clearly visible as in image 1: near foreleg in front, near hind leg at the far left, far foreleg at the right under the pod, far hind leg between.` |
| Có bóng, mảng sáng tối, quầng sáng | `Flat colour only: remove every shadow, highlight, shine, glow and gradient; keep the crayon hatching as texture only.` |
| Bầu ngực mở sẵn / không thấy bầu ngực | `The chest pod is CLOSED: a big round bulge of overlapping plates on the front of the chest, with only thin bright lines in the seams.` |
| Hình bị phóng to lấp cả khung | `Keep the size and place of image 1: the figure fills only the lower two thirds; top of the head crest at about y = 465.` |
| Há mồm, có hai mắt, có đuôi | `Mouth closed; three-quarter profile to the right with only ONE eye; no tail.` |

## Lượt 1c: sửa SỪNG của hướng A (người dùng 2026-11-13: "cái sừng xấu quá, làm lại để nó liên kết với phần đầu thành 1 khối hơn")

Vẽ lại y hệt `L1_co_thu.png`, chỉ đổi sừng và chỗ sừng nối đầu. Hai kiểu để người dùng chọn.

- `lien`: sừng mọc liền từ sống mũi và gờ mày (kiểu sừng tê giác), cùng thớ gỗ với sọ, ngọn nứt lộ tinh thể hổ phách. **Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_1c_sung_lien.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1c_sung_lien.png`.
- `mu`: mảng trán gỗ sẫm như mũ giáp phủ từ gáy tới mũi rồi vuốt lên thành sừng, mép dưới xếch tạo gờ mày, ngọn tinh thể hổ phách. **Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_1c_sung_mu.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1c_sung_mu.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1_co_thu.png` | Concept hướng A dáng nghỉ (1024 × 1536, nền trắng): mọi thứ đã duyệt trừ sừng |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\bo_cuc_co_thu_nghi.png` | Sơ đồ bố cục dáng nghỉ (1024 × 1536, nền trắng): chỉ để thấy chỗ ngọn sừng và đầu |

Kiểm: sừng và đầu là MỘT khối (không vòng, không cổ, không nét ngăn ở chân sừng); ngọn vẫn là tinh thể hổ phách; mặt, thân, bờm, bầu ngực không đổi.

## Lượt 2: MẢNH theo khung part của rig (sau khi duyệt concept)

Mỗi tờ: ảnh 1 = concept đã duyệt (lấy nét, màu, vân sáp), ảnh 2 = tờ hướng dẫn tự dựng (mỗi part của rig một ô đúng khung, hình bóng kín tô phẳng). GPT vẽ lại sạch, GIỮ NGUYÊN hình bóng. Claude cắt bằng `giac_moc_manh.py cat_part <tờ>`, đo IoU.

- Tờ `A` (sáu mảng dương xỉ / lá to của bờm lưng; phóng 2.1 lần, nét ~7 px): **chỉ gửi GPT đường dẫn** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_manh_A.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\N_A.png`; ảnh 2 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\part_A.png` (1536 × 1024, nền trắng, 6 ô).
- Tờ `B` (năm dải lá dài + sợi dây leo + hai túm lá sau đầu; phóng 2.7 lần, nét ~9 px): **chỉ gửi GPT đường dẫn** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_manh_B.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\N_B.png`; ảnh 2 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\part_B.png` (1536 × 1024, nền trắng, 7 ô).
- Tờ `C` (mào đầu (sáu mảnh lá), năm tinh thể hổ phách, năm tấm gai gỗ; phóng 2.2 lần, nét ~7 px): **chỉ gửi GPT đường dẫn** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_manh_C.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\N_C.png`; ảnh 2 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\part_C.png` (1536 × 1024, nền trắng, 16 ô).
- Tờ `D` (mười tấm vỏ ngực, tám tấm sườn gỗ nhạt, ba gai; phóng 3.3 lần, nét ~11 px): **chỉ gửi GPT đường dẫn** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_manh_D.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\N_D.png`; ảnh 2 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\part_D.png` (1536 × 1024, nền trắng, 21 ô).
- Tờ `E` (chín đoạn dây leo vành ngực, tám lá nhỏ, mảng rêu nhỏ, ba tấm đốt cổ, mẩu gỗ gáy; phóng 4.4 lần, nét ~15 px): **chỉ gửi GPT đường dẫn** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_manh_E.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\N_E.png`; ảnh 2 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\part_E.png` (1536 × 1024, nền trắng, 22 ô).
- Tờ `F` (lòng ngực, quả tim, ba dải vách xa của bầu ngực, mảng rêu gốc cổ; phóng 2.0 lần, nét ~7 px): **chỉ gửi GPT đường dẫn** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_manh_F.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\N_F.png`; ảnh 2 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\part_F.png` (1536 × 1024, nền trắng, 6 ô).
- Tờ `H` (bảy túm rêu ở chân và vai, ba gai vai; phóng 3.4 lần, nét ~12 px): **chỉ gửi GPT đường dẫn** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_manh_H.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\N_H.png`; ảnh 2 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\part_H.png` (1536 × 1024, nền trắng, 10 ô).
- Tờ `G` (mười sáu ngón chân có móng, sáu gai gót; phóng 3.7 lần, nét ~13 px): **chỉ gửi GPT đường dẫn** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_manh_G.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\N_G.png`; ảnh 2 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\part_G.png` (1536 × 1024, nền trắng, 22 ô).
- Tờ **thân liền** (mông, vai, cổ, bốn chân gen LIỀN rồi cắt bằng mã): `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_than_lien.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\N_lien.png`; ảnh 2 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\mau\lien.png` (1536 × 1024, nền trắng: ở giữa một hình bóng nâu liền thân + cổ + hai chân gần, hai bên là hai chân xa; bàn chân nâu sẫm).

Kiểm: hình bóng trùng tờ hướng dẫn (IoU ≥ 0,9 mới lắp); tờ thân liền KHÔNG có nét mực nào bên trong; tô phẳng; nền trắng.

## Lượt 2 (đầu): ĐẦU LIỀN SỪNG "đúng chỗ, đúng cỡ"

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\giac_moc_1\luot_2_dau_sung.txt` → `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\M_dau.png`. Ảnh mẫu 1 = `D:\PokiClash\ArtGen\Spine\inbox\giac_moc_1\tai_ve\L1_duyet.png` (concept đã duyệt, 1024 × 1536, nền trắng).
Kiểm: chỉ còn đầu + sừng, đúng chỗ và cỡ như concept, viền kín (gáy và dưới hàm vẽ bù tròn), nền trắng.

