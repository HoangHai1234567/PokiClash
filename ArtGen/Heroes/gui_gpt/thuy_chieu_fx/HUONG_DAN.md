# Gói gửi GPT: hiệu ứng chiêu các tướng đảo Thủy (đòn đánh, chiêu cuối) (`thuy_chieu_fx`)

Hiệu ứng thêm cho đòn đánh và chiêu cuối viết lại của các tướng đảo Thủy (người dùng dặn 2026-11-07): cột nước xả xuống từ quả cầu trên đầu địch, giáo băng khổng lồ của Thương Lam, rắn nước của Huyền Vũ, xoáy nước mặt đất. Mỗi hiệu ứng là một hình rời trên nền trắng; Claude ghép vào clip CHIÊU (aola `tools/anim_moi.py`). Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Chỉ gửi GPT đường dẫn file prompt:** `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\thuy_chieu_fx\luot_1_hieu_ung.txt` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\thuy_chieu_fx\tai_ve\`.

1. GPT vẽ FX16. Gõ `next`: GPT vẽ FX17. Nhắn Claude "soi thử thuy_chieu_fx".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: FX18, FX19.
3. Đủ ảnh thì nhắn Claude "ghép thuy_chieu_fx".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\thuong_lam_3\concept_duyet.png` | Concept đã duyệt dạng 1 (thuong_lam_3, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\huyen_vu_3\concept_duyet.png` | Concept đã duyệt dạng 2 (huyen_vu_3, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\lam_quan_3\concept_duyet.png` | Concept đã duyệt dạng 3 (lam_quan_3, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con |
| 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_fx\tai_ve\FX07.png` | Sóng thần FX07 của gói Giọt Sương (1024 × 1024, nền trắng): hiệu ứng mới cùng nét, cùng màu nước với nó |
| 6 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\tieu_y_fx\tai_ve\FX10.png` | Quả cầu nước FX10 (1024 × 1024, nền trắng): cột nước FX16 xả ra từ quả cầu như thế này |

Kiểm từng ảnh trước khi lưu (vẽ tay trên giấy, viền mực nâu, tô chì sáp phẳng; không mảng sáng tối, không điểm sáng, không bóng loáng, không quầng sáng, không bóng đổ; nền trắng, không chạm mép ảnh, không có con, không chữ):

- **FX16** cột nước xả (viền khoảng 16 px): cột nước xả ngang sang phải (game xoay cho xả thẳng xuống từ quả cầu): khối nước rộng dài gấp ba bề ngang, 4-5 dải xanh đậm xanh nhạt xoắn, dải bọt trắng dọc hai mép; đầu trái là cổ nước hẹp có lọn cuộn, đầu phải đập thành đầu bọt trắng rộng có mũi nước và giọt văng
- **FX17** giáo băng khổng lồ (viền khoảng 16 px): giáo băng khổng lồ chĩa sang phải: tinh thể băng dài nhọn gấp bốn bề dày, xanh băng có dải mặt cắt trắng phẳng và vài đường cạnh thẳng, viền xanh mòng két mảnh; đầu phải nhọn hoắt, đầu trái là chân băng lởm chởm có mảnh băng nhỏ và hoa tuyết vỡ ra
- **FX18** rắn nước thần (viền khoảng 18 px): rắn thần bằng nước vươn lên mổ sang phải, nhìn ngang: thân là một khúc nước cuộn hình chữ S xanh đậm và xanh ngọc bích trồi lên từ xoáy bọt ở dưới trái, đầu rắn rồng bằng nước ở trên phải (há miệng, hai nanh trắng, mào vây, mắt tròn bọt trắng), bọt trắng dọc sống lưng, giọt văng; không vảy, không phải con thật
- **FX19** xoáy nước mặt đất (viền khoảng 14 px): xoáy nước trên mặt đất nhìn chếch thấp: phễu bầu dục dẹt rộng gấp ba chiều cao, bốn dải nước xanh đậm xanh nhạt xoáy vào một lỗ nhỏ xanh thẫm ở giữa, bọt trắng cuộn dọc mép ngoài và giữa các dải, vài giọt bắn lên

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Không giống vẽ tay trên giấy | `Draw it by hand on paper: dark-brown ink-pen outlines, every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |
| Quầng sáng, điểm sáng, mảng sáng tối, bóng loáng | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine, no glow, no gradients.` |
| Chạm mép ảnh, nền không trắng | `Keep the whole effect inside the canvas with a clear white margin; plain pure white background.` |
| Có con, tay, vũ khí | `Only the effect itself, nothing else.` |
| Có bóng đổ, bóng in xuống nền | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine, no glow, no gradients.` |

Gói này sinh từ `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\build_fx.py`; sửa prompt ở đó rồi chạy lại.
