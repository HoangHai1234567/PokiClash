# Gói gửi GPT: Liên Kình (`tm07`), dòng 7 lô tướng mới đảo Thủy

Cá kỳ lân biển (cá voi một ngà) cõng hoa sen, hai dạng. Dạng 2 là dạng cuối (trưởng thành, chiến), dạng 1 là bé con chibi. Thiết kế khác hẳn con tham khảo, chỉ giữ chủ đề; không đính ảnh con tham khảo.

**Dạng 2, chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm07_2\luot_1_concept.txt`. GPT lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm07_2\tai_ve\L1_concept.png`.

**Dạng 1** (dựng sau khi chép concept dạng 2 đã chọn thành `D:\PokiClash\ArtGen\Spine\inbox\tm07_2\tai_ve\L1_duyet.png`): `D:\PokiClash\ArtGen\Spine\gui_gpt\tm07_1\luot_1_concept.txt`. GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm07_1\tai_ve\L1_concept.png`.

Claude tự gen: `py -3 -I gen.py gui_gpt/tm07_2/luot_1_concept.txt`, rồi `py -3 -I gen.py gui_gpt/tm07_1/luot_1_concept.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\hai_long\tai_ve\L1_duyet.png` | Hải Long Ngũ Đầu đã duyệt (1536 × 1024, nền trắng): lấy nét bút, vân sáp, mức chi tiết, kiểu nước, thần thái; không chép loài, màu, dáng |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\ma_ket_3\tai_ve\L1_lien.png` | Ma Kết dạng 3 đã duyệt (1536 × 1024, nền trắng): lấy cách tô phẳng, cách vẽ viền vàng và giáp thành mảng phẳng; không chép loài, màu, dáng |
| 4 (chỉ dạng 1) | `D:\PokiClash\ArtGen\Spine\inbox\tm07_2\tai_ve\L1_duyet.png` | Concept dạng 2 đã chọn (1536 × 1024, nền trắng) |

## Bảng màu

| Vùng | Dạng 2 Liên Kình | Dạng 1 Kình Nụ |
|---|---|---|
| Lưng, sườn | chàm `#3A4A9C` | lam phấn `#8FA7E6` |
| Bụng, cổ họng | ngà `#F4ECD8` | kem `#F7F0DF` |
| Sen | cánh ngoài đỏ thắm `#D9443A`, cánh trong hồng `#EE8A80`, đài vàng `#E8B64A` | nụ hồng nhạt `#F3B5AE`, chóp đỏ `#D9443A` |
| Ngà, mào trán, vòng đuôi | vàng `#E8B64A` | ngà cụt vàng nhạt `#F1D27A` |
| Viền vây, chóp đuôi | đỏ thắm `#D9443A` | đỏ thắm `#D9443A` (dải mỏng) |
| Mắt | mống cyan `#45CFE0`, hẹp, sắc | mống cyan `#45CFE0`, to tròn |
| Lòng miệng | đỏ rượu `#8B2F45` | đỏ rượu `#8B2F45` |
| Nước | lam `#1E68BE` `#3A96E2` `#8CD0F6`, bọt `#F4FCFF` | như dạng 2 |

## Kiểm concept dạng 2

- Nhìn nghiêng, **quay sang phải**, đầu ở phải, đuôi ở trái, đầu ngẩng ~20°; thân chữ S nhẹ; vây đuôi xoè thấy trọn.
- Một ngà vàng xoắn thẳng, không bị gì che; sen nở to đứng giữa lưng, không đè đầu, không đè đuôi; vây gần tách khỏi bụng.
- Miệng hé thấy lòng miệng đỏ rượu và răng nhọn nhỏ; hàm dưới là hình riêng; mắt hẹp quả quyết, một chấm sáng.
- Thân chàm + bụng ngà, không vân xoắn, không đốm, không vảy; ba vòng vàng ở gốc đuôi.
- Nước: đệm sóng thấp dưới bụng, chỉ che mép dưới bụng; ba màu lam phẳng, bọt trắng tròn.
- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh, không chữ.

## Kiểm concept dạng 1

- Chibi: đầu ~45% thân, mắt to tròn, thân bầu; vẫn cau mày, hai răng nhọn, miệng hé.
- Nụ sen **khép**, ngà **cụt**, màu nhạt hơn dạng 2; vẫn nhận ra cùng dòng với ảnh 4.

## GPT vẽ sai thì gửi thêm (`gen.py ... --note "..."`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |
| Quay sang trái | `The creature must face the viewer's RIGHT: head on the right, tail on the left.` |
| Dạng 2 vẫn chibi, dễ thương | `Not chibi at all: adult proportions, head about one quarter of the body length, narrow fierce eye, powerful body.` |
| Vẽ vân xoắn, đốm trên thân | `No swirl patterns, spots or scales on the body: plain indigo back, plain ivory belly with a few throat grooves.` |
| Sen che đầu hoặc đuôi, ngà bị che | `The lotus, the tusk, each flipper and the fluke must each stand clear with white around them; nothing overlaps.` |
| Nước quá to | `The water is only a low cushion under the belly, about one fifth of the picture height.` |
| Dạng 1 sen nở, ngà dài | `Baby form: the lotus is a CLOSED bud, the tusk only a short stub, colours lighter.` |
