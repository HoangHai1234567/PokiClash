# Gói gửi GPT: máy bi (thân máy, bộ phận, hiệu ứng, rương)

Sinh bằng `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\build.py`, đừng sửa tay (chạy lại script sẽ ghi đè).

Thân máy là tủ máy vẽ tay bao quanh mặt máy, có đầu máy chứa thanh kinh nghiệm (vòng cấp, thanh EXP, nút tỉ lệ) và đỉnh vòm có bóng đèn. Game vẫn tự vẽ đinh, ô, bi, số trên ô (đổi theo mức cược) và thanh kinh nghiệm; ảnh chỉ là cái tủ.

Bố cục học từ máy tham khảo: tủ đứng đỉnh vòm viền bóng đèn, đầu máy là bảng chứa thanh cấp, mặt chơi ở giữa. Không đính ảnh của game đó cho GPT, không nhắc tên game.

**Chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh.

## Lượt 1: thân máy

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\gui_gpt\than_may\luot_1_than_may.txt`. GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` (trùng tên thì thêm `_2`, `_3`).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | bản đồ thế giới của game: bốn đảo vẽ tay, viền mực nâu, tô sáp màu (chỉ để học nét) (1024 × 1536) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\refs\bo_cuc_than_may.png` | ảnh bố cục tủ máy: nền caro xám là trong suốt; thân cam, vòm cam nhạt có chấm vàng (bóng đèn) và tròn hồng (bi); rãnh tím là chỗ thanh kinh nghiệm, tròn hồng bên trái là vòng cấp, tròn xanh bên phải là nút tỉ lệ; chữ nhật kem là mặt chơi; hai khối nâu là chân (1024 × 1536) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\StyleRefs\R2b_MayBi_KetVang.png` | mặt máy game tự vẽ (đinh, nấm đỏ, cốc bạc, két vàng, 11 ô), chỉ để GPT hiểu, không vẽ lại (920 × 1360) |
| 4 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\refs\man_may_bi_hien_tai.png` | ảnh chụp màn Máy bi trong game bây giờ (có thanh kinh nghiệm trên đầu máy, cột cược, khay rương, nút thả) (540 × 960) |

Soi:
- ảnh dọc 1024 × 1536, nền trong suốt; tủ nằm trong x 61..963, y 28..1508, đúng chỗ như ảnh bố cục;
- mặt chơi x 85..939, y 222..1484 là một chữ nhật kem phẳng, trống trơn (không đinh, không chấm, không ô);
- rãnh thanh kinh nghiệm trống (không có thanh, không số), vòng cấp và hốc nút trống ở giữa;
- khung hai bên mỏng (khoảng 24 px ảnh), vòm có hàng bóng đèn vàng và bi hồng ở giữa, hai chân dưới đáy;
- không chữ, không số, không bóng đổ, không quầng sáng.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same cabinet, but the play window must be completely empty flat cream, exactly the rectangle of image 2.`
- `Same cabinet, but the side frame thinner, exactly as in image 2.`
- `Same cabinet, but the background must be transparent, no floor, no shadow.`
- `Same cabinet, but leave the groove, the badge socket and the button socket empty, no numbers, no bar.`

Xong thì nhắn Claude "duyệt thân máy". Tự làm cũng được:
1. `py -3 -I E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\build.py --duyet`: lọc mép, cắt sát, thu về đúng cỡ hiện trên màn, ghi `E:\ProjectAtomik\PokiWar\Assets\03 Art\Pachinko\pk_than_may.png`; đo rãnh thanh, hai hốc tròn, mặt chơi, ghi `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\refs\than_may_da_duyet.json`;
2. trong Unity, menu `PokiClash/Prefab/Máy bi: thân máy vẽ tay`: đặt thân máy sau mặt máy, tắt khung giấy tạm, dời thanh kinh nghiệm vào rãnh, nút tỉ lệ thành chữ "i" trong hốc tròn bên phải, nhích cột cược và khay rương khỏi viền tủ.

## Lượt 2: bộ phận mặt máy

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\gui_gpt\than_may\luot_2_bo_phan.txt`. GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\bo_phan.png` (trùng tên thì thêm `_2`, `_3`).

12 bộ phận thay hình tạm vẽ bằng code trên mặt máy: đinh, nấm, u lồi tường, cọc vách ô, cốc bạc, mái két, đáy két, máng mây, bi (trắng xám, game tô màu theo cược), ván vai, ray máng thả, tấm nền két.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` | thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu (1024 × 1536) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\guides\G_Sheet4x3.png` | lưới 4 × 3 đánh số (ô hồng, khung xám là vùng an toàn) (1536 × 1024) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\refs\mat_may_danh_so.png` | ảnh chụp máy trong game, nhãn hồng đánh số chỉ vào bộ phận tạm ứng với từng ô (860 × 1412) |

Soi:
- lưới 1536 × 1024, nền trong suốt, mỗi ô một món đúng số, không chạm mép ô;
- món nhỏ (đinh, bi, u lồi) viền mực dày, đơn giản, đọc được khi thu còn 17–34 px;
- cọc vách ô đứng dọc, mái két, ván vai, ray nằm ngang (game tự xoay);
- bi chỉ trắng và xám nhạt; máng mây có mắt;
- không chữ, không số, không bóng đổ.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same sheet, but every part simpler and bolder, with thicker ink outlines.`
- `Same sheet, but the ball only white and light grey, no colour.`
- `Same sheet, but each part fully inside the grey box of its cell, not touching the cell edge.`

Xong thì nhắn Claude "duyệt bộ phận". Tự làm: `py -3 -I E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\build.py --duyet bo_phan` (cắt ô, ghép mặt máy tĩnh `Baked/Machine/may_tinh.png` theo đúng toạ độ vật lý, ghi `pk_bumper`, `pk_may_tha`, `pk_bi`), rồi trong Unity chạy menu `PokiClash/Dựng lại danh mục ảnh` và `PokiClash/Prefab/Máy bi: ảnh bộ phận`.

## Lượt 3: hiệu ứng

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\gui_gpt\than_may\luot_3_hieu_ung.txt`. GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\hieu_ung.png` (trùng tên thì thêm `_2`, `_3`).

6 hình hiệu ứng game đang dùng (hình tạm trong `Assets/03 Art/Fallback`): 1 `fx_glow`, 2 `fx_sparkle`, 3 `fx_ring`, 4 `fx_star`, 5 `fx_streak`, 6 `fx_puff`. Game tự phóng, xoay, mờ, tô màu nên GPT vẽ trắng.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` | thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu (1024 × 1536) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\guides\G_Sheet3x2.png` | lưới 3 × 2 đánh số (1536 × 1024) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\refs\hieu_ung_tam.png` | 6 hình hiệu ứng tạm game đang dùng (trắng trên nền tối), cùng thứ tự ô (1536 × 1024) |

Soi:
- lưới 1536 × 1024, nền trong suốt, mỗi ô một hình đúng thứ tự;
- chỉ trắng và xám nhạt (sao và khói có viền mực mảnh); không màu khác;
- quầng mờ dần về trong suốt ở mép; vòng rỗng giữa; vệt đầu sáng bên phải, đuôi mờ bên trái;
- không chữ, không nền.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same sheet, but only white and very pale grey, no colour at all.`
- `Same sheet, but the glow fades fully to transparent at its edge.`
- `Same sheet, but each effect smaller and fully inside the grey box of its cell.`

Xong thì nhắn Claude "duyệt hiệu ứng". Tự làm: `py -3 -I E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\build.py --duyet hieu_ung` (cắt 6 ô, lưu `Assets/03 Art/Pachinko/<tên>.png` cùng tên hình tạm), rồi trong Unity chạy menu `PokiClash/Dựng lại danh mục ảnh`. Game tự dùng ảnh mới ở mọi chỗ đang dùng hình tạm đó (cả sao EXP bay lên thanh kinh nghiệm).

## Lượt 4: rương

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\gui_gpt\than_may\luot_4_ruong.txt`. GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\ruong.png` (trùng tên thì thêm `_2`, `_3`).

Rương gỗ, bạc, vàng (đóng và mở) cho ô rương trên mặt máy, khay "Rương chờ" và hộp mở rương; thay hình rương vẽ bằng code (dùng chung với rương AFK).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` | thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu (1024 × 1536) |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\guides\G_Sheet3x2.png` | lưới 3 × 2 đánh số (1536 × 1024) |
| 3 | `E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\refs\ruong_hien_tai.png` | hộp mở rương trong game hiện giờ, rương vàng vẽ tạm bằng code (627 × 574) |

Soi:
- lưới 1536 × 1024, nền trong suốt, mỗi ô một rương đúng thứ tự gỗ, gỗ mở, bạc, bạc mở, vàng, vàng mở;
- sáu rương cùng dáng, cùng cỡ, chỉ khác chất liệu; rương mở thấy nắp lật ra sau;
- trong rương mở tô vàng nhạt phẳng, không quầng sáng; không bóng đổ;
- không chữ, không số.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same sheet, but all six chests exactly the same shape and size; only the material changes.`
- `Same sheet, but no glow halo: the inside of the open chests is a flat light-yellow colour.`
- `Same sheet, but each chest fully inside the grey box of its cell.`

Xong thì nhắn Claude "duyệt rương". Tự làm: `py -3 -I E:\ProjectAtomik\PokiWar\ArtGen\Pachinko\build.py --duyet ruong` (cắt 6 ô thành `pk_ruong_go`, `pk_ruong_bac`, `pk_ruong_vang`, bản mở thêm `_mo`), rồi trong Unity chạy menu `PokiClash/Dựng lại danh mục ảnh`. Rương trên mặt máy, khay và hộp mở rương tự dùng ảnh mới (rương AFK màu riêng giữ hình vẽ tạm).

