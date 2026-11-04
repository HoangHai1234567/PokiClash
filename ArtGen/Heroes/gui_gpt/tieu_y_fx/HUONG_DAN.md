# Gói gửi GPT: hiệu ứng chiêu Tiểu Y (`tieu_y_fx`)

Quả cầu nước của chiêu cuối Tiểu Y dạng 1 (người dùng dặn 2026-11-04): giơ đinh ba tụ quả cầu nước rồi ném về phía địch. Thay bong bóng FX06 của Giọt Sương (còn vệt sáng trắng, trông như bong bóng xà phòng); các hiệu ứng khác của chiêu dùng lại gói `giot_suong_fx`. Mỗi hiệu ứng là một hình rời trên nền trắng; Claude ghép vào clip CHIÊU (aola `tools/anim_moi.py`). Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Chỉ gửi GPT đường dẫn file prompt:** `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\tieu_y_fx\luot_1_hieu_ung.txt` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\tieu_y_fx\tai_ve\`.

1. GPT vẽ FX10. Nhắn Claude "soi tieu_y_fx".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\tieu_y_1\concept_duyet.png` | Concept đã duyệt dạng 1 (tieu_y_1, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_fx\tai_ve\FX01.png` | Hiệu ứng vòng nước xoáy FX01 của gói Giọt Sương (1024 × 1024, nền trắng): ba dòng nước cuộn quanh tâm rỗng. Quả cầu phải cùng nét, cùng màu với nó |

Kiểm từng ảnh trước khi lưu (vẽ tay trên giấy, viền mực nâu, tô chì sáp phẳng; không mảng sáng tối, không điểm sáng, không bóng loáng, không quầng sáng, không bóng đổ; nền trắng, không chạm mép ảnh, không có con, không chữ):

- **FX10** quả cầu nước (viền khoảng 14 px): quả cầu nước tròn nhìn thẳng: bên trong ba dải nước xanh đậm và xanh nhạt xoáy quanh tâm như xoáy nước nhốt trong quả cầu, bọt trắng cuộn nhỏ dọc mép, ba bốn giọt văng ra; là khối nước cuộn, không phải bong bóng hay thuỷ tinh, không vệt sáng; dáng tròn

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Không giống vẽ tay trên giấy | `Draw it by hand on paper: dark-brown ink-pen outlines, every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |
| Quầng sáng, điểm sáng, mảng sáng tối, bóng loáng | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine, no glow, no gradients.` |
| Chạm mép ảnh, nền không trắng | `Keep the whole effect inside the canvas with a clear white margin; plain pure white background.` |
| Có con, tay, vũ khí | `Only the effect itself, nothing else.` |
| Có bóng đổ, bóng in xuống nền | `Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, no white highlights or shine, no glow, no gradients.` |
| Trông như bong bóng, thuỷ tinh, có vệt sáng | `Make it a ball of solid churning water, not a bubble or glass: no see-through look, no shine spot; fill the whole ball with spiralling bands of deep blue and light blue water and white foam curls.` |

Gói này sinh từ `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\build_fx.py`; sửa prompt ở đó rồi chạy lại.
