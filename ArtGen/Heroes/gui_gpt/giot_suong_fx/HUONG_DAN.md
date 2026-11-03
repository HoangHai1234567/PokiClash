# Gói gửi GPT: hiệu ứng chiêu Giọt Sương (`giot_suong_fx`)

Hiệu ứng vẽ tay cho clip CHIÊU của cả ba dạng (thay quầng sáng gốc của aola), người dùng dặn 2026-11-03: đẹp và hoành tráng hơn. Mỗi hiệu ứng là một hình rời trên nền trắng; Claude ghép vào clip CHIÊU (aola `tools/anim_moi.py`). Quy trình: `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\QUY_TRINH.md`.

**Chỉ gửi GPT đường dẫn file prompt:** `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\gui_gpt\giot_suong_fx\luot_1_hieu_ung.txt` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_fx\tai_ve\`.

1. GPT vẽ FX09. Gõ `next`: GPT vẽ FX02. Nhắn Claude "soi thử giot_suong_fx".
2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: FX03, FX01, FX04, FX05, FX06, FX07, FX08.
3. Đủ ảnh thì nhắn Claude "ghép giot_suong_fx".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_1\concept_duyet.png` | Concept đã duyệt dạng 1 (giot_suong_1, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_2\concept_duyet.png` | Concept đã duyệt dạng 2 (giot_suong_2, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_3\concept_duyet.png` | Concept đã duyệt dạng 3 (giot_suong_3, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con |

Kiểm từng ảnh trước khi lưu (nét vẽ tay như bản đồ, viền mực nâu, không bóng loáng, không quầng sáng mờ, nền trắng, không bóng đổ, không chạm mép ảnh, không có con, không chữ):

- **FX09** tia nước bắn thẳng (viền khoảng 16 px): tia nước bắn ngang sang phải, dài khoảng gấp năm lần chiều cao: đầu tia tròn bắn bọt trắng ở bên phải, thân hơi gợn có vệt xanh nhạt và xanh đậm, đuôi thon thành sợi mảnh và vài giọt ở bên trái
- **FX02** sóng nước lưỡi liềm (viền khoảng 16 px): sóng hình lưỡi liềm bay sang phải: mép trước dày cong ở bên phải, hai sừng nhọn kéo về trên trái và dưới trái, bọt trắng dọc mép trước, vài giọt bắn phía sau
- **FX03** nước nổ tung (viền khoảng 16 px): vụ nổ nước tròn nhìn thẳng: 8-10 mũi nước nhọn và giọt bắn ra quanh tâm, giữa là bọt trắng, giọt nhỏ bay ra giữa các mũi
- **FX01** vòng nước xoáy (viền khoảng 14 px): vòng nước xoáy nhìn thẳng: ba dòng nước cuộn đuổi nhau quanh tâm rỗng (giữa để trắng), đầu dòng dày đuôi mảnh, vài giọt văng ra
- **FX04** chùm giọt nước (viền khoảng 12 px): năm giọt nước rời to nhỏ khác nhau, mỗi giọt hình giọt lệ có chấm sáng trắng, cùng rơi xuống chéo trái
- **FX05** tia lấp lánh (viền khoảng 12 px): một ngôi sao lấp lánh bốn cánh lớn, trắng viền xanh nhạt, tâm vàng nhỏ, cạnh là hai sao nhỏ
- **FX06** bong bóng (viền khoảng 14 px): một bong bóng nước tròn lớn xanh nhạt trông trong, vệt sáng cong trắng ở trên trái, viền xanh đậm mảnh
- **FX07** sóng thần cuộn (viền khoảng 18 px): sóng lớn nhìn ngang cuộn sang phải: dâng từ chân phẳng bên trái, cuộn lại ở trên phải thành vòm rỗng, mào bọt trắng và bụi nước ở mép sóng
- **FX08** vòng sóng loang mặt đất (viền khoảng 14 px): vòng sóng nước loang trên mặt đất nhìn chếch thấp: hình bầu dục rộng gấp ba chiều cao, viền có tia nước nhỏ bắn lên, giữa rỗng trắng

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Quầng sáng mờ, bóng loáng | `Hand-drawn like the map: dark-brown ink outlines, flat colours with coloured-pencil hatching; no glow, no glossy shine, no gradients.` |
| Chạm mép ảnh, nền không trắng | `Keep the whole effect inside the canvas with a clear white margin; plain pure white background.` |
| Có con, tay, vũ khí | `Only the effect itself, nothing else.` |
| Có bóng đổ, bóng in xuống nền | `NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the feet or on the ground or background. Shade only with colour-pencil hatching inside the shapes.` |

Gói này sinh từ `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\build_fx.py`; sửa prompt ở đó rồi chạy lại.
