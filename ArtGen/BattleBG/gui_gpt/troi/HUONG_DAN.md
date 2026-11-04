# Gói gửi GPT: nối trời nền trận đảo Thủy (`troi`)

Sinh bằng `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\build_troi.py`, đừng sửa tay (chạy lại script sẽ ghi đè).

## Tiến độ (script tự ghi lúc dựng gói)

- **Đã ghép, đã vào game:** c01. Code game (`StageView.FitBg`) đã thử trong Play ở 1080 × 2400 và 1080 × 1920 (2026-11-04).
- **Còn:** c02, c03, c04, c05, c06, c07, c08, c09, m20, m30, m40, m50, m60, b70a, b70b, b70c. Làm bằng GPT (người dùng chốt 2026-11-04: gen lại từng nền, không mượn trời c01 cho nền khác).
- **Bước tiếp:** gửi GPT file gộp `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\gop_c02_c09.txt` (c02–c09 một thể, 8 ảnh: c02, c03, c04, c05, c06, c07, c08, c09; mỗi bước một ảnh, lưu riêng), rồi nhắn Claude "duyệt troi c02–c09". Sau đó m20–m60, b70a (file lẻ), cuối cùng b70b, b70c (dựng sau khi b70a duyệt).
- **Đổi máy:** file prompt ghi đường dẫn tuyệt đối của máy dựng gói. Sang máy khác thì chạy lại `py -3 -I ArtGen/BattleBG/build_troi.py` trước khi gửi GPT.
- **Duyệt:** `py -3 -I ArtGen/BattleBG/build_troi.py --duyet <mã>` (ghép, ảnh soi `troi/soi_<mã>.png`), soi mép cũ phóng to; rồi `py -3 -I ArtGen/BattleBG/build_thuy.py --xuat` và Play thử "Đánh thử ải …" ở khung 1080 × 2400.

**Vì sao:** máy dài hơn 9:16 thì vùng sân trận cao hơn khung nền 1080 × 928 (máy 2960 × 1440 thêm 300, 20:9 thêm 480, 21:9 thêm 600), phần trên chỉ có màu trời trơn. Mỗi nền cũ cho GPT vẽ nối lên trên; game neo đáy ảnh vào đáy khung, máy dài thấy thêm trời, máy 9:16 cắt bớt (không đổi gì).

**Khung gửi GPT** (`khung_<mã>.png`, 1024 × 1536): 880 px dưới là nền trận cũ, 656 px trên để trắng. GPT vẽ lại cả khung; Claude chỉ lấy phần trên của GPT, phần dưới vẫn là ảnh cũ (khớp tỉ lệ, chỗ rồi nối theo đường ít lệch nhất), nên phần dưới GPT có lệch chút cũng không sao.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. GPT lưu xong thì nhắn Claude "duyệt troi <mã>" (vd `duyệt troi c01`); Claude ghép, soi rồi đưa vào game. Boss dạng 2, 3 (`b70b`, `b70c`) cần dạng 1 (`b70a`) đã duyệt, Claude dựng file prompt sau.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
| 1. Bãi Vỏ Sò (ải 1–4): trời xanh nhạt, hoàn chỉnh đám mây bị cắt ở góc trên trái, thêm 2, 3 đám mây nhỏ | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\01_c01.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_c01.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Bãi Vỏ Sò cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\c01.png` |
| 2. Vũng San Hô (ải 5–9): trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\02_c02.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_c02.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Vũng San Hô cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\c02.png` |
| 3. Cầu Gỗ Rêu (ải 10–14): trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\03_c03.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_c03.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Cầu Gỗ Rêu cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\c03.png` |
| 4. Làng Vỏ Ốc (ải 15–19): trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\04_c04.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_c04.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Làng Vỏ Ốc cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\c04.png` |
| 5. Ngọn Hải Đăng (ải 21–29): trời xanh nhạt; hải đăng bên trái đã đủ mái, phía trên chỉ là trời; vài đám mây nhỏ | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\05_c05.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_c05.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Ngọn Hải Đăng cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\c05.png` |
| 6. Thác Bạc (ải 31–39): trời xanh nhạt; vách và thác bên trái đã đủ đỉnh, phía trên chỉ là trời; hoàn chỉnh mây bị cắt ở mép trên, thêm vài đám mây | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\06_c06.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_c06.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Thác Bạc cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\c06.png` |
| 7. Rạn Ngọc Trai (ải 41–49): trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\07_c07.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_c07.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Rạn Ngọc Trai cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\c07.png` |
| 8. Hồ Gương (ải 51–59): trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\08_c08.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_c08.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Hồ Gương cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\c08.png` |
| 9. Đền Rùa Cổ (ải 61–69): trời xanh nhạt; đền mai rùa bên trái đã đủ, phía trên chỉ là trời; vài đám mây nhỏ | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\09_c09.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_c09.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Đền Rùa Cổ cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\c09.png` |
| 10. Ngọn Hải Đăng, mini boss (Ma Kết) (ải 20): mái nón đỏ của hải đăng bên trái bị cắt ở mép cũ: vẽ nốt tới chóp; trời hoàng hôn bão tiếp lên, mây tím xám viền hồng cam, lên cao tím xanh đậm dần; không vẽ tia đèn | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\10_m20.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_m20.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Ngọn Hải Đăng, mini boss (Ma Kết) cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\m20.png` |
| 11. Thác Bạc, mini boss (Vây Lam) (ải 30): vách đá rêu và hai dòng thác chảy từ trên mép cũ: vẽ tiếp lên tới đỉnh vách (rêu, dương xỉ, bụi, cây cọ) chỗ nước đổ xuống; trên đó và bên phải là trời sáng sớm xanh bạc, vài đám mây | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\11_m30.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_m30.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Thác Bạc, mini boss (Vây Lam) cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\m30.png` |
| 12. Rạn Ngọc Trai, mini boss (Kuba) (ải 40): trời chạng vạng tím xanh tiếp lên, cao lên chàm đậm dần, thêm sao nhỏ, vài đám mây tím nhạt; giữ trăng khuyết, không thêm trăng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\12_m40.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_m40.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Rạn Ngọc Trai, mini boss (Kuba) cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\m40.png` |
| 13. Hồ Gương, mini boss (Thương Lam) (ải 50): trời đêm xanh đậm nhiều sao tiếp lên, cao lên tối dần, vài đám mây nhỏ viền bạc; trăng tròn giữ nguyên, không thêm trăng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\13_m50.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_m50.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Hồ Gương, mini boss (Thương Lam) cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\m50.png` |
| 14. Đền Rùa Cổ, mini boss (Huyền Vũ) (ải 60): đền mai rùa bên trái bị cắt ở mép cũ: vẽ nốt mái vòm mai rùa phủ rêu, dây leo; lá cọ góc trên phải vươn thêm; trời chạng vạng xanh ngọc lên tím, vài đám mây tím | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\14_m60.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_m60.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Đền Rùa Cổ, mini boss (Huyền Vũ) cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\m60.png` |
| 15. Xoáy Nước Đinh Ba, dạng 1 (Lam Quân) (ải 70): cột đá chạm sóng bên trái nhô lên trên mép cũ: vẽ tiếp lên, đỉnh gãy lởm chởm; trời bão chạng vạng xanh đậm tiếp lên, mây xám xanh dày dần; không sét, mưa, đinh ba | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\15_b70a.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\gui_gpt\troi\khung_b70a.png`: khung nối trời (1024 × 1536): 880 px dưới là nền trận Xoáy Nước Đinh Ba, dạng 1 (Lam Quân) cũ, 656 px trên để trắng | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\b70a.png` |
| 16. Xoáy Nước Đinh Ba, dạng 2 (Vạn Quân) (ải 70): nối lên y như bản dạng 1 đã duyệt (ảnh 2): cùng đỉnh cột, cùng chỗ mây, chỉ theo trời bão tối hơn của ảnh này | chưa dựng | chưa có: cần `b70a` đã duyệt | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\b70b.png` |
| 17. Xoáy Nước Đinh Ba, dạng 3 (Hắc Dực Vạn Quân) (ải 70): nối lên y như bản dạng 1 đã duyệt (ảnh 2): cùng đỉnh cột, cùng chỗ mây, chỉ theo trời bão đêm tím đen của ảnh này | chưa dựng | chưa có: cần `b70a` đã duyệt | `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\tai_ve\b70c.png` |

Bản ghép Claude lưu ở `E:\ProjectAtomik\PokiWar\ArtGen\BattleBG\troi\<mã>.png` (1080 × 1528: 600 trời thêm + khung 928), kèm ảnh soi `soi_<mã>.png`: bên trái ảnh sạch, bên phải có vạch chỗ từng loại máy bắt đầu thấy (9:16, 2960 × 1440, 20:9, 21:9) và đường nối (đỏ).

## Soi trước khi nhắn Claude

- Phần trên kín màu, không còn trắng, không viền, không khung.
- Không thấy mép cũ: trời liền màu, nét chì cùng hướng; vật bị mép cũ cắt (hải đăng, vách thác, đền, cột đá) được vẽ tiếp đúng chỗ, đúng bề ngang.
- Phần trên êm: chủ yếu là trời, không thêm địa danh, vật to sáng, sinh vật, chữ.
- Không vẽ tia đèn, mưa, sét, đinh ba (game tự cho chạy).
- Phần dưới giống ảnh cũ (cùng bố cục); lệch nhẹ không sao.

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Còn trắng hoặc có viền | `Same image, but fill the whole top part edge to edge: no white area, no margin, no frame.` |
| Thấy rõ mép cũ | `Same image, but make the sky continue seamlessly across the old top edge: same colours and same pencil hatching, no line or colour change there.` |
| Vật bị cắt không được vẽ tiếp | `Same image, but continue the [lighthouse / cliff and waterfall / temple dome / stone pillar] upward from the old top edge, same width and place.` |
| Phần trên rối, có vật mới to | `Same image, but keep the new top part calm: mostly sky with a few small clouds, no new landmark or big bright object.` |
| Vẽ lại lệch phần dưới | `Keep the bottom part exactly like image 1, same layout, same size and place; only paint the top part.` |
| Có tia đèn, mưa, sét | `Same image without the [light beam / rain / lightning]; the game adds them.` |
| Có chữ, số, sinh vật | `Same image without any text, numbers, creatures or people.` |
