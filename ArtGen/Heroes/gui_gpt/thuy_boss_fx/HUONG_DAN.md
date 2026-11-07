# Gói gửi GPT: hiệu ứng chiêu boss cuối đảo Thủy (`thuy_boss_fx`)

Tia mana riêng của 3 boss cuối đảo Thủy (người dùng dặn 2026-11-07): Thương Lam tia băng, Huyền Vũ tia xoắn, Lam Quân tia triều đinh ba; kèm mảnh băng và vòng sóng âm. Mỗi hiệu ứng là một hình rời trên nền trắng; Claude ghép vào clip CHIÊU (aola `tools/anim_moi.py`). Quy trình: `D:\PokiClash\ArtGen\Heroes\QUY_TRINH.md`.

**Chỉ gửi GPT đường dẫn file prompt:** `D:\PokiClash\ArtGen\Heroes\gui_gpt\thuy_boss_fx\luot_1_hieu_ung.txt` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `D:\PokiClash\ArtGen\Heroes\inbox\thuy_boss_fx\tai_ve\`.

1. GPT vẽ FX11. Gõ `next`: GPT vẽ FX12. Nhắn Claude "soi thử thuy_boss_fx".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: FX13, FX14, FX15.
3. Đủ ảnh thì nhắn Claude "ghép thuy_boss_fx".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 2 | `D:\PokiClash\ArtGen\Heroes\inbox\giot_suong_1\concept_duyet.png` | Concept đã duyệt dạng 1 (giot_suong_1, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con |
| 3 | `D:\PokiClash\ArtGen\Heroes\inbox\giot_suong_fx\tai_ve\FX09.png` | Tia nước thường FX09 (1024 × 1024, nền trắng): tia mới cùng nét, cùng cỡ, khác dáng |

Kiểm từng ảnh trước khi lưu (vẽ tay trên giấy, viền mực nâu, tô chì sáp phẳng; không mảng sáng tối, không điểm sáng, không bóng loáng, không quầng sáng, không bóng đổ; nền trắng, không chạm mép ảnh, không có con, không chữ):

- **FX11** tia băng (viền khoảng 16 px): tia băng bắn sang phải, dài gấp năm lần chiều cao: nước xanh băng và trắng đang đông lại, dọc hai mép lởm chởm tinh thể băng dẹt, đầu tia bên phải là chùm mảnh băng và sương hoa tuyết, đuôi bên trái là sợi sương mảnh
- **FX12** tia xoắn (viền khoảng 16 px): tia xoắn bắn sang phải: hai dòng nước xanh đậm và xanh nhạt xoắn vào nhau như dây thừng, bọt trắng ở chỗ bắt chéo, đầu bên phải là xoáy nước tròn bọt cuộn, đuôi bên trái là hai lọn mảnh
- **FX13** tia triều đinh ba (viền khoảng 18 px): tia triều bắn sang phải: dòng nước xanh đậm rộng, dài gấp bốn lần chiều cao, đầu bên phải là ba mũi đinh ba bằng nước viền vàng đồng, mép trên có ngọn bọt trắng cuộn, thân có vệt sóng vàng đồng mảnh, đuôi tan thành bọt
- **FX14** mảnh băng (viền khoảng 12 px): năm mảnh băng dẹt rời to nhỏ khác nhau, xanh băng có một đường cạnh trắng, viền xanh mòng két mảnh, bay tách nhau
- **FX15** vòng sóng âm (viền khoảng 14 px): một vòng sóng âm tròn nhìn thẳng như tiếng chuông đồng hiện thành nước: vòng nước gợn xanh nhạt, viền trong vàng đồng, bọt nhỏ quanh vòng, giữa rỗng trắng

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Không giống vẽ tay trên giấy | `Draw it by hand on paper: dark-brown ink-pen outlines, every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |
| Quầng sáng, điểm sáng, mảng sáng tối, bóng loáng | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine, no glow, no gradients.` |
| Chạm mép ảnh, nền không trắng | `Keep the whole effect inside the canvas with a clear white margin; plain pure white background.` |
| Có con, tay, vũ khí | `Only the effect itself, nothing else.` |
| Có bóng đổ, bóng in xuống nền | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine, no glow, no gradients.` |

Gói này sinh từ `D:\PokiClash\ArtGen\Heroes\build_fx.py`; sửa prompt ở đó rồi chạy lại.
