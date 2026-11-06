# Gói gửi GPT: máy bi, bộ mới (nút, trạng thái sáng, hạt hiệu ứng)

Sinh bằng `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\build_bo_moi.py`, đừng sửa tay (chạy lại script sẽ ghi đè).

Học từ máy bi tham khảo: bộ phận nào có, mỗi bộ phận mấy trạng thái, hiệu ứng nào chạy lúc nào. Bảng đối chiếu đủ bộ phận và 36 hiệu ứng của máy đó ở `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\THAM_KHAO_MAY_BI.md`. Hình vẽ mới theo nét đã duyệt của mình (thân máy, tờ bộ phận): không đính ảnh của game đó cho GPT, không nhắc tên game.

Màn Máy bi giờ nằm trên mặt bàn gỗ nâu (#7D5031), nên nút cần viền kem và viền mực rõ. Mọi tờ: không bóng đổ, không quầng sáng (luật UI và hiệu ứng tô phẳng).

**Chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Ba lượt độc lập, gửi lượt nào trước cũng được.

## Lượt 1: nút thả, nút thả liền, viên cược

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\gui_gpt\bo_moi\luot_1_nut.txt`. GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\nut.png` (trùng tên thì thêm `_2`, `_3`).

Nút thả tròn kiểu nút bấm máy thay hai nút chữ nhật dưới máy (học từ nút bấm vòm của máy tham khảo: một hình, nhiều trạng thái đổi màu, nhấn thì lún), viên cược tròn thay cột ×1…×10, bảng nút dưới máy, bàn tay chỉ cho hướng dẫn. Chữ (THẢ BI, ×2…) game tự viết đè lên.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` | thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu (1024 × 1536) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\guides\G_Sheet4x3.png` | lưới 4 × 3 đánh số (ô hồng, khung xám là vùng an toàn) (1536 × 1024) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\refs\man_may_bi_go.png` | ảnh chụp màn Máy bi bây giờ (nền bàn gỗ nâu, cột cược bên trái, hai nút thả chữ nhật dưới máy) (540 × 960) |

Soi:
- lưới 1536 × 1024, nền trong suốt, mỗi ô một món đúng số, không chạm mép ô;
- ô 1–4 cùng một nút y hệt dáng, cỡ, chỗ; chỉ khác màu (đỏ, đỏ lún, xám, vàng sao); ô 2 nắp lún thấp;
- ô 5–6 và ô 7–10 cũng cùng dáng trong nhóm; viên khoá có ổ khoá nhỏ ở mép;
- mặt nút, giữa viên cược trống trơn (không chữ, không số, không ký hiệu);
- bảng nút ô 11 dài khoảng 4 : 1, có hai hốc tròn trống (to bên trái, nhỏ bên phải);
- không bóng đổ, không quầng sáng, không bóng loáng; viền kem và viền mực rõ để nổi trên nền gỗ nâu.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same sheet, but cells 1 to 4 must be exactly the same button shape and size; only the colours change.`
- `Same sheet, but leave the tops of the buttons and the centres of the tokens completely empty, no text.`
- `Same sheet, but no shadow under the buttons and no glossy highlight; flat colours with crayon hatching.`

Xong thì nhắn Claude "duyệt nút". Tự cắt: `py -3 -I E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\build_bo_moi.py --duyet nut` (lưu `Assets/03 Art/Pachinko/pk_nut_*.png`, `pk_cuoc*.png`, `pk_bang_nut.png`, `pk_tay_chi.png`); nối vào màn Máy bi là việc code của Claude.

## Lượt 2: trạng thái sáng của mặt máy

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\gui_gpt\bo_moi\luot_2_trang_thai.txt`. GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\trang_thai.png` (trùng tên thì thêm `_2`, `_3`).

Bản sáng của đinh, nấm, u lồi, cốc bạc, tấm két (máy tham khảo đổi hình đinh sang hình sáng 0,067 giây mỗi lần bi chạm); bóng đèn vòm tắt, sáng vàng, sáng hồng để game cho đèn chạy; lớp sáng ô đáy khi bi rơi vào; mây nháy mắt khi thả, mây há miệng khi trúng két.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` | thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu (1024 × 1536) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\guides\G_Sheet4x3.png` | lưới 4 × 3 đánh số (ô hồng, khung xám là vùng an toàn) (1536 × 1024) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\bo_phan.png` | tờ bộ phận đã duyệt (đinh, nấm, u lồi, cọc, cốc bạc, mái két, đáy két, mây, bi, ván vai, ray, tấm két) (1536 × 1024) |

Soi:
- lưới 1536 × 1024, nền trong suốt, mỗi ô một món đúng số;
- ô 1–5 trùng khít viền và cỡ với ô 1, 2, 3, 5, 12 của tờ bộ phận, chỉ đổi màu sáng; nấm vẫn 5 chấm;
- bóng đèn 6–8 cùng một dáng; đèn sáng có vạch mực nhỏ quanh, không quầng sáng;
- ô 9–10 là chữ nhật đứng khoảng 1 : 3, tia trắng từ đáy toả lên, khe trong suốt giữa các tia;
- mây 11–12 trùng dáng mây cũ, chỉ đổi mặt (nhắm cười, tròn mắt há miệng);
- không chữ, không bóng đổ, không quầng sáng.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same sheet, but each lit part must have exactly the outline and size of the matching part in image 3.`
- `Same sheet, but no glow at all: light is only flat bright colour and small ink tick marks.`
- `Same sheet, but the slot lights 9 and 10 white only, rays with transparent gaps, about 1 : 3.`

Xong thì nhắn Claude "duyệt trạng thái". Tự cắt: `py -3 -I E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\build_bo_moi.py --duyet trang_thai` (lưu `pk_dinh_sang`, `pk_bumper_sang`, `pk_u_loi_sang`, `pk_coc_sang`, `pk_ket_sang`, `pk_den_*`, `pk_o_sang*`, `pk_may_tha_nhay`, `pk_may_tha_wow`); nối vào mặt máy là việc code của Claude.

## Lượt 3: hạt hiệu ứng mới

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\gui_gpt\bo_moi\luot_3_hieu_ung.txt`. GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\hieu_ung_2.png` (trùng tên thì thêm `_2`, `_3`).

12 hình hạt mới cho các bộ hiệu ứng chép từ máy tham khảo (bảng ở `THAM_KHAO_MAY_BI.md`). Máy đó dùng nhiều lớp quầng mềm (glow, flash); luật mình tô phẳng nên lớp đó thay bằng hình loé, vòng dày, tia toả vẽ tay. GPT vẽ trắng, game tô màu.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` | thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu (1024 × 1536) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\guides\G_Sheet4x3.png` | lưới 4 × 3 đánh số (ô hồng, khung xám là vùng an toàn) (1536 × 1024) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\hieu_ung.png` | 6 hình hiệu ứng đang dùng (trắng, nền trong suốt): quầng, lấp lánh, vòng, sao, vệt, khói (1536 × 1024) |

Soi:
- lưới 1536 × 1024, nền trong suốt, mỗi ô một hình đúng thứ tự;
- chỉ trắng, gạch chì xám nhạt, viền mực nâu mảnh; không màu khác;
- hình nào cũng sắc nét, phẳng: không quầng, không mờ mép, không chuyển màu;
- vòng 2, 3, sao 8, lấp lánh 9, xoáy 7, ngoặc 10 rỗng giữa (trong suốt); vạch tốc đầu tròn bên phải;
- không chữ, không nền.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same sheet, but only white with light grey hatching and thin dark-brown outlines, no colour at all.`
- `Same sheet, but no glow and no soft edges: every effect a crisp flat shape with an ink outline.`
- `Same sheet, but each effect smaller and fully inside the grey box of its cell.`

Xong thì nhắn Claude "duyệt hiệu ứng 2". Tự cắt: `py -3 -I E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\build_bo_moi.py --duyet hieu_ung_2` (lưu `Assets/03 Art/Pachinko/pk_fx_*.png`, tên không trùng ảnh thay thế trong Fallback); thêm vào các bộ hạt trong `MachineFx.cs` là việc code của Claude.

