# Cốt truyện mở đầu: gói gửi GPT

Đoạn truyện tranh 2 trang, 6 khung chạy lần đầu vào game (trước màn tải con tàu). Chạm một lần hiện một khung; chữ do game in, GPT không vẽ chữ. Mỗi lượt bạn chỉ gửi GPT **đường dẫn file prompt**; GPT tự mở ảnh mẫu và tự lưu ảnh.

**Nhân vật chính** (người chơi): cậu bé thuần thú sư khoảng 11 tuổi, tóc nâu hạt dẻ có một chỏm dựng, băng cá nhân trên má trái, áo choàng ngắn có mũ màu xanh mòng két cài khuy đồng, khăn đỏ, áo kem xắn tay, dây chéo ngực cài 5 cây bút chì 5 màu hệ, quần soóc nâu, tất sọc, ủng nâu. Cầm **sổ phép** bìa da nâu góc đồng, ngôi sao 5 màu trên bìa, và **bút chì phép** to cỡ cẳng tay (thân vàng, tẩy đỏ, buộc lông vũ) dùng như đũa phép. Thuần phục sinh vật bằng cách vẽ chúng vào sổ. Cũng nói vài lời dẫn trong hướng dẫn người mới (chân dung bán thân).

| Trang | Khung | Nội dung | Chữ game in |
|---|---|---|---|
| 1 | 1 | cơn bão (ngang) | Một đêm giông bão... |
| 1 | 2 | tỉnh dậy trên bãi biển lạ (dọc) | Tỉnh dậy ở một thế giới lạ. |
| 1 | 3 | rừng sương, sinh vật kỳ bí (dọc) | (không chữ) |
| 2 | 4 | năm người bạn mới (dọc) | Những người bạn mới. |
| 2 | 5 | chúa tể đảo lửa (dọc) | Mỗi đảo một chúa tể. |
| 2 | 6 | năm đảo, lên đường (ngang) | Đi chinh phục thôi! |

## Các lượt

### Lượt 0: tờ thiết kế nhân vật chính (ngang)
- Gửi GPT: `D:\PokiClash\ArtGen\Story\gui_gpt\luot_0.txt`
- Ảnh mẫu trong file:
  - image 1 = `D:\PokiClash\ArtGen\Islands\refs\world_style.png`: bản đồ vẽ tay mẫu của game (1024 x 1536, nền giấy kem): chỉ lấy nét vẽ (viền mực nâu rung, chì màu, sáp)
  - image 2 = `D:\PokiClash\Assets\03 Art\Heroes\Resources\ti_tach_1\ti_tach_1_portrait.png`: chân dung Tí Tách (nền trong suốt): lấy tỉ lệ mập, dễ thương và lối tô phẳng cho cậu bé
- Lưu: `D:\PokiClash\ArtGen\Story\tai_ve\nhan_vat.png` (1536 x 1024)

### Lượt 1: chân dung bán thân, nền trong suốt (vuông), tỉnh dậy trên bãi biển lạ (dọc)
- Gửi GPT: `D:\PokiClash\ArtGen\Story\gui_gpt\luot_1.txt`
- Ảnh mẫu trong file:
  - image 1 = `D:\PokiClash\ArtGen\Story\duyet\nhan_vat.png`: tờ thiết kế nhân vật chính đã duyệt (1536 x 1024): khoá hình cậu bé, sổ phép, bút chì phép
  - image 2 = `D:\PokiClash\ArtGen\Islands\refs\world_style.png`: bản đồ vẽ tay mẫu của game (1024 x 1536, nền giấy kem): chỉ lấy nét vẽ (viền mực nâu rung, chì màu, sáp)
  - image 3 = `D:\PokiClash\Assets\03 Art\Islands\sanh_dao_thuy.png`: đảo Thủy trên bản đồ sảnh (nền trong suốt): lấy dáng cây dừa, cát, đá, biển xanh ngọc
- Lưu: `D:\PokiClash\ArtGen\Story\tai_ve\chan_dung.png` (1024 x 1024)
- Lưu: `D:\PokiClash\ArtGen\Story\tai_ve\khung_2.png` (1024 x 1536)

### Lượt 2: cơn bão (ngang), rừng sương, sinh vật kỳ bí (dọc)
- Gửi GPT: `D:\PokiClash\ArtGen\Story\gui_gpt\luot_2.txt`
- Ảnh mẫu trong file:
  - image 1 = `D:\PokiClash\ArtGen\Story\duyet\khung_2.png`: khung 2 đã duyệt (1024 x 1536): khoá nét vẽ truyện cho các khung sau
  - image 2 = `D:\PokiClash\ArtGen\Story\duyet\nhan_vat.png`: tờ thiết kế nhân vật chính đã duyệt (1536 x 1024): khoá hình cậu bé, sổ phép, bút chì phép
- Lưu: `D:\PokiClash\ArtGen\Story\tai_ve\khung_1.png` (1536 x 1024)
- Lưu: `D:\PokiClash\ArtGen\Story\tai_ve\khung_3.png` (1024 x 1536)

### Lượt 3: năm người bạn mới (dọc), chúa tể đảo lửa (dọc), năm đảo, lên đường (ngang)
- Gửi GPT: `D:\PokiClash\ArtGen\Story\gui_gpt\luot_3.txt`
- Ảnh mẫu trong file:
  - image 1 = `D:\PokiClash\ArtGen\Story\duyet\khung_2.png`: khung 2 đã duyệt (1024 x 1536): khoá nét vẽ truyện cho các khung sau
  - image 2 = `D:\PokiClash\ArtGen\Story\duyet\nhan_vat.png`: tờ thiết kế nhân vật chính đã duyệt (1536 x 1024): khoá hình cậu bé, sổ phép, bút chì phép
  - image 3 = `D:\PokiClash\Assets\03 Art\Heroes\Resources\ti_tach_1\ti_tach_1_portrait.png`: chân dung Tí Tách (nền trong suốt): lấy tỉ lệ mập, dễ thương và lối tô phẳng cho cậu bé
  - image 4 = `D:\PokiClash\Assets\03 Art\Heroes\Resources\quy_lava_1\quy_lava_1_portrait.png`: chân dung tướng khởi đầu dạng 1 (nền trong suốt)
  - image 5 = `D:\PokiClash\Assets\03 Art\Heroes\Resources\tinh_sat_1\tinh_sat_1_portrait.png`: chân dung tướng khởi đầu dạng 1 (nền trong suốt)
  - image 6 = `D:\PokiClash\Assets\03 Art\Heroes\Resources\tien_la_1\tien_la_1_portrait.png`: chân dung tướng khởi đầu dạng 1 (nền trong suốt)
  - image 7 = `D:\PokiClash\Assets\03 Art\Heroes\Resources\cong_da_1\cong_da_1_portrait.png`: chân dung tướng khởi đầu dạng 1 (nền trong suốt)
  - image 8 = `D:\PokiClash\Assets\03 Art\Heroes\Resources\nui_lua_1\nui_lua_1_portrait.png`: chân dung Hỏa Sơn Long, boss cuối đảo Hỏa (nền trong suốt): chỉ lấy dáng cho bóng chúa tể ở khung 5
  - image 9 = `D:\PokiClash\Assets\03 Art\Islands\world.png`: bản đồ thế giới năm đảo của sảnh (1480 x 2320): lấy dáng từng đảo cho khung 6
- Lưu: `D:\PokiClash\ArtGen\Story\tai_ve\khung_4.png` (1024 x 1536)
- Lưu: `D:\PokiClash\ArtGen\Story\tai_ve\khung_5.png` (1024 x 1536)
- Lưu: `D:\PokiClash\ArtGen\Story\tai_ve\khung_6.png` (1536 x 1024)

## Kiểm

- Tờ nhân vật: cậu bé trai mập, dễ thương, mặt quả quyết; đủ áo choàng xanh mòng két, khăn đỏ, dây 5 bút chì, sổ phép, bút chì phép; không mũ, không ba lô; không chữ, không ô màu, không bóng dưới chân.
- Chân dung: nền trong suốt thật (không giấy, không khung tròn), cắt ngang giữa ngực, viền mực quanh hình.
- Khung truyện: tràn kín khung, không viền, không chữ, không bóng loáng hay quầng sáng; phép thuật là nét chì màu, không phát sáng.
- Nét viền mực nâu rung, tô chì màu và sáp như bản đồ mẫu; nhân vật tô phẳng, không mảng sáng tối.
- Cậu bé cùng một hình ở mọi khung (so với tờ nhân vật).
- Khung 4: năm bạn nhỏ đúng dáng năm tướng khởi đầu. Khung 5: chúa tể chỉ là bóng to mắt vàng.

## Câu sửa nhanh (gửi GPT kèm ảnh vừa vẽ)

- `Redraw it full-bleed: remove the border and the white margin.`
- `Remove all text, letters, labels and speech bubbles.`
- `Make the outlines bolder and more wobbly, with crayon texture like the reference map; flat colours, no shading.`
- `Draw the boy exactly like on the design sheet (teal hooded cape, red scarf, pencil bandolier, sketchbook, magic pencil).`
- `Make the background fully transparent: remove the paper and any circle behind him.`

## Sau khi GPT lưu ảnh

- Duyệt tờ nhân vật: `py -3 -I ArtGen/Story/build_story.py --duyet nv` → lượt 1 được dựng.
- Duyệt chân dung: `--duyet cd`. Duyệt khung k: `--duyet k` (lấy ảnh mới nhất trong `tai_ve/`).
- Duyệt khung 2 thì lượt 2, 3 được dựng.
- Có ảnh duyệt: `py -3 -I ArtGen/Story/build_story.py --nhap`, rồi menu Unity `PokiClash/Prefab/Khác/Hộp thoại và màn∕Cốt truyện mở đầu (CotTruyen)` (khung) và `PokiClash/Prefab/Khác/Hộp thoại và màn∕Hướng dẫn người mới (lớp phủ)` (chân dung).
