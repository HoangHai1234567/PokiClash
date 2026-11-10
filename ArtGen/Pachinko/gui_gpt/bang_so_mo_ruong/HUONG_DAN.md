# Gói gửi GPT: máy bi, bảng số và mở rương

Sinh bằng `C:\Atomik\PokiWar\ArtGen\Pachinko\build_mo_ruong.py`, đừng sửa tay (chạy lại script sẽ ghi đè).

Chép hiệu ứng máy bi tham khảo: bảng số dưới thanh cấp (kẹo EXP bay từ ô lên bảng, số đếm tăng, hết đợt mới đổ lên thanh), mở rương như mở capsule thú (tối đa 5 cái một lượt, lơ lửng, chạm từng cái hoặc mở tất cả, hiện thưởng một lượt). Hình vẽ theo nét đã duyệt (thân máy, rương); không đính ảnh của game đó cho GPT, không nhắc tên game.

Ánh sáng và gradient (quầng mềm, tia sáng, cột sáng từ rương, vệt sáng lia qua bảng, chấm LED) game tự sinh bằng code, GPT chỉ vẽ hình phẳng.

**Chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Ba lượt độc lập, gửi lượt nào trước cũng được.

## Lượt 1: bảng số

File prompt: `C:\Atomik\PokiWar\ArtGen\Pachinko\gui_gpt\bang_so_mo_ruong\luot_1_bang_so.txt`. GPT lưu `C:\Atomik\PokiWar\ArtGen\Pachinko\tai_ve\bang_so.png` (trùng tên thì thêm `_2`, `_3`).

Bảng số kiểu biển đèn hội chợ treo trên đỉnh vòm mặt chơi (như bảng LED của máy tham khảo): kẹo EXP bay từ ô lên bảng, số trên bảng đếm tăng, hết đợt số đổ lên thanh cấp. GPT vẽ khung gỗ và màn tối trống; chữ số, chấm LED, bóng đèn chạy viền, quầng sáng do game làm.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` | thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu (1024 × 1536) |
| 2 | `C:\Atomik\PokiWar\Assets\03 Art\Baked\Machine\may_tinh.png` | mặt chơi game đang vẽ (đinh, máng, 5 ô); bảng số treo trên đỉnh vòm mặt chơi (920 × 1360) |

Soi:
- ảnh 1536 × 1024 nền trong suốt, một biển ở giữa, dài khoảng 3,7 : 1;
- viền gỗ đỏ cam đều quanh, trơn (không bóng đèn, không lỗ), giữa mép trên nhô vòm thấp có sao vàng nhỏ;
- màn tím sẫm phẳng, trống trơn (không số, không chấm, không phản chiếu);
- hai giá gỗ ngắn dưới hai góc; không bóng đổ, không quầng sáng.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same sign, but the screen must be completely empty flat dark plum, no digits, dots or reflections.`
- `Same sign, but no bulbs or holes on the frame band: a plain even wooden band.`
- `Same sign, but wider and lower, about 3.7 : 1, and fully inside the image with a margin.`

Xong thì nhắn Claude "duyệt bảng số". Tự cắt: `py -3 -I C:\Atomik\PokiWar\ArtGen\Pachinko\build_mo_ruong.py --duyet bang_so` (lưu `Assets/03 Art/Pachinko/pk_bang_so.png` và `refs/bang_so.json`); đặt bảng lên máy là việc code của Claude.

## Lượt 2: kẹo EXP, đồ hộp mở rương

File prompt: `C:\Atomik\PokiWar\ArtGen\Pachinko\gui_gpt\bang_so_mo_ruong\luot_2_keo_exp.txt`. GPT lưu `C:\Atomik\PokiWar\ArtGen\Pachinko\tai_ve\keo_exp.png` (trùng tên thì thêm `_2`, `_3`).

Kẹo EXP (icon bay từ ô lên bảng số, như kẹo của máy tham khảo, thay ngôi sao XP vẽ tạm), nắm kẹo cho ô nhiều EXP; đồ cho màn mở rương kiểu mở capsule: thẻ úp (game tô màu độ hiếm rồi lật), gối mây rương đứng lơ lửng, ruy băng tiêu đề, nút "Mở tất cả".

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` | thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu (1024 × 1536) |
| 2 | `C:\Atomik\PokiWar\ArtGen\guides\G_Sheet3x2.png` | lưới 3 × 2 đánh số (ô hồng, khung xám là vùng an toàn) (1536 × 1024) |
| 3 | `C:\Atomik\PokiWar\ArtGen\Pachinko\tai_ve\ruong.png` | tờ rương đã duyệt (gỗ, bạc, vàng; đóng và mở) (1536 × 1024) |

Soi:
- lưới 3 × 2, nền trong suốt, mỗi ô một món đúng thứ tự;
- kẹo ô 1 tím có xoắn giấy hai bên, nhìn rõ khi nhỏ; ô 2 là ba viên y hệt ô 1;
- thẻ úp xám nhạt có viền kem, giữa là hình bi tròn có một dải ngang;
- mây dẹt khoảng 3 : 1, mặt trên phẳng; không phải bóng;
- ruy băng và nút: giữa trống trơn, không chữ; không bóng đổ, không quầng sáng.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same sheet, but the candy in cell 1 simpler and chunkier, readable at 60 px, wrapper twists on both sides.`
- `Same sheet, but leave the middle of the ribbon and of the button completely empty, no text.`
- `Same sheet, but the card back light grey so the game can tint it.`

Xong thì nhắn Claude "duyệt kẹo". Tự cắt: `py -3 -I C:\Atomik\PokiWar\ArtGen\Pachinko\build_mo_ruong.py --duyet keo_exp` (lưu `pk_keo_exp`, `pk_keo_exp_nam`, `pk_the_up`, `pk_may_do`, `pk_ruy_bang`, `pk_nut_mo_het`).

## Lượt 3: nắp, thân rương rời

File prompt: `C:\Atomik\PokiWar\ArtGen\Pachinko\gui_gpt\bang_so_mo_ruong\luot_3_ruong_tach.txt`. GPT lưu `C:\Atomik\PokiWar\ArtGen\Pachinko\tai_ve\ruong_tach.png` (trùng tên thì thêm `_2`, `_3`).

Nắp và thân rương rời của ba loại rương (cắt từ đúng tờ rương đã duyệt): lúc mở, rương lắc rồi nắp bật bay xoáy lên, thân đứng lại và ánh sáng tuôn ra (như vỏ capsule tách đôi ở máy tham khảo).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Pachinko\tai_ve\than_may.png` | thân máy đã duyệt (tủ đỉnh vòm đỏ cam, nền trong suốt): mẫu nét và màu (1024 × 1536) |
| 2 | `C:\Atomik\PokiWar\ArtGen\guides\G_Sheet3x2.png` | lưới 3 × 2 đánh số (ô hồng, khung xám là vùng an toàn) (1536 × 1024) |
| 3 | `C:\Atomik\PokiWar\ArtGen\Pachinko\tai_ve\ruong.png` | tờ rương đã duyệt: 1 gỗ đóng, 2 gỗ mở, 3 bạc đóng, 4 bạc mở, 5 vàng đóng, 6 vàng mở (1536 × 1024) |

Soi:
- lưới 3 × 2, nền trong suốt; hàng trên ba nắp, hàng dưới ba thân mở;
- nắp trùng dáng nắp của rương đóng, mép dưới thẳng; thân có khoá tròn ở mép trên, miệng vàng nhạt phẳng;
- nắp và thân cùng loại ghép lại khớp rương đóng (cùng bề ngang, cùng đai);
- không sao, không xu, không bóng đổ, không quầng sáng.

Câu sửa nhanh (gửi kèm đường dẫn file prompt):
- `Same sheet, but each lid must be exactly the lid of the closed chest of image 3, same width, straight bottom edge.`
- `Same sheet, but the bodies without any lid or hinge, only a flat light-yellow opening at the top.`
- `Same sheet, but no stars, coins or glow around the pieces.`

Xong thì nhắn Claude "duyệt rương tách". Tự cắt: `py -3 -I C:\Atomik\PokiWar\ArtGen\Pachinko\build_mo_ruong.py --duyet ruong_tach` (lưu `pk_ruong_*_nap`, `pk_ruong_*_than`, cùng bề ngang rương đóng); hiệu ứng mở là việc code của Claude.

