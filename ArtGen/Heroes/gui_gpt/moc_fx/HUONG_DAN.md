# Gói gửi GPT: hiệu ứng chiêu các tướng hệ Mộc (`moc_fx`)

Hiệu ứng vẽ tay dùng chung cho animation các tướng đảo Mộc (lốc lá, lá nổ, chùm lá, phấn hoa, dây gai, vòng cỏ) và tia lá của chiêu mana hệ Mộc. Mỗi hiệu ứng là một hình rời trên nền trắng; Claude ghép vào clip CHIÊU (aola `tools/anim_moi.py`). Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Chỉ gửi GPT đường dẫn file prompt:** `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\moc_fx\luot_1_hieu_ung.txt` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\moc_fx\tai_ve\`.

1. GPT vẽ FX09. Gõ `next`: GPT vẽ FX01. Nhắn Claude "soi thử moc_fx".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: FX03, FX04, FX05, FX07, FX08.
3. Đủ ảnh thì nhắn Claude "ghép moc_fx".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\tien_la_1\concept_duyet.png` | Concept đã duyệt dạng 1 (tien_la_1, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con |

Kiểm từng ảnh trước khi lưu (vẽ tay trên giấy, viền mực nâu, tô chì sáp phẳng; không mảng sáng tối, không điểm sáng, không bóng loáng, không quầng sáng, không bóng đổ; nền trắng, không chạm mép ảnh, không có con, không chữ):

- **FX09** tia lá bắn thẳng (viền khoảng 16 px): tia gió lá bắn ngang sang phải, dài gấp năm lần chiều cao: dòng gió xanh cuộn đầy lá nhọn xanh rêu, xanh lá, ô liu đang xoay, vài chấm phấn vàng nhạt; đầu bên phải là chùm lá bung ra, đuôi bên trái thon thành lọn gió và vài lá rời
- **FX01** lốc lá xoáy (viền khoảng 14 px): vòng lốc lá nhìn thẳng: ba dải gió xanh cuộn đuổi nhau quanh tâm rỗng (giữa để trắng), mỗi dải mang 4-5 lá nhọn
- **FX03** lá nổ tung (viền khoảng 16 px): vụ nổ lá tròn nhìn thẳng: 8-10 lá nhọn xanh rêu, xanh lá, ô liu bay ra quanh tâm, giữa là chùm hình sao xanh vàng nhạt, vụn lá và chấm phấn giữa các lá
- **FX04** chùm lá bay (viền khoảng 12 px): năm chiếc lá nhọn rời to nhỏ khác nhau (xanh rêu, xanh lá, ô liu, có gân giữa), cùng bay rơi chéo xuống trái
- **FX05** phấn hoa lấp lánh (viền khoảng 12 px): một ngôi sao lấp lánh bốn cánh lớn màu vàng phấn hoa viền xanh lá mảnh, tâm trắng nhỏ, cạnh là hai sao nhỏ, ba chấm phấn
- **FX07** dây gai quật lên (viền khoảng 18 px): dây gai lớn nhìn ngang trồi lên từ mặt đất rồi quật sang phải: dây xoắn xanh ô liu, gai nhọn nâu vỏ cây, gốc là đất cỏ bật lên bên trái, ngọn cong cuộn ở bên phải, vài lá và vụn lá bay
- **FX08** vòng cỏ loang mặt đất (viền khoảng 14 px): vòng cỏ trên mặt đất nhìn chếch thấp: hình bầu dục rộng gấp ba chiều cao, viền là ngọn cỏ và lá nhỏ bật lên, giữa rỗng trắng

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Không giống vẽ tay trên giấy | `Draw it by hand on paper: dark-brown ink-pen outlines, every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |
| Quầng sáng, điểm sáng, mảng sáng tối, bóng loáng | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine, no glow, no gradients.` |
| Chạm mép ảnh, nền không trắng | `Keep the whole effect inside the canvas with a clear white margin; plain pure white background.` |
| Có con, tay, vũ khí | `Only the effect itself, nothing else.` |
| Có bóng đổ, bóng in xuống nền | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine, no glow, no gradients.` |

Gói này sinh từ `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\build_fx.py`; sửa prompt ở đó rồi chạy lại.
