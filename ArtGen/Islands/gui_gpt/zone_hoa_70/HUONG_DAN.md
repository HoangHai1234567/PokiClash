# Gói gửi GPT: bản đồ dài đảo Hỏa 70 ải (`zone_hoa_70`)

Sinh bằng `E:\ProjectAtomik\PokiWar\ArtGen\Islands\build_zone70_hoa.py`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Hỏa mới cho 70 ải, cùng khuôn bản đồ dài đảo Thủy, đảo Mộc: một bản đồ dọc ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ 1024 × 4288. Đường cát rộng lượn chữ S (lượn phải trước, ngược đảo Mộc) từ bến đá đen lên bãi đấu boss dưới núi lửa, 10 bãi tròn cho 10 ải tướng, địa danh của từng chặng đứng sát đường. Không vẽ vòng tròn ải: game đặt bệ tướng và chấm ải lên đường. Khói, lửa, tàn lửa, dòng dung nham chảy là phần động game thêm sau, GPT không vẽ.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude "duyệt đoạn <k> đảo Hỏa"; Claude soi, lưu bản duyệt và dựng file prompt của lượt sau. Nên làm cả 3 lượt trong cùng một chat để GPT giữ nét.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
| 1: đoạn dưới, địa danh 1, 2, 3, 4, 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_hoa_70\luot_1.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\moc70\doan_1.png`: đoạn 1 bản đồ dài đảo Mộc đã duyệt (1024 × 1536, nền đặc): đường cát rộng lượn có bãi tròn, bậc đất có vách ngắn, cây tròn, đá, đồ vật chen sát đường, nền xanh lá; lấy nét và cách dựng, không lấy màu, đồ vật rừng, bố cục; 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\zone_hoa.png`: bản đồ đảo Hỏa 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền đỏ cam gạch chì, đường mòn mảnh có 8 vòng tròn kem, sông dung nham cam, núi lửa có bánh xe vàng trên đỉnh, cổng bánh xe, lò đá tròn, chùa sen mái đỏ, cây cháy tán cam, đất nứt, đá đen, bến gỗ ở đáy; lấy màu và dáng đồ vật (không lấy bánh xe vàng); 3 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_hoa_70\bo_cuc_1.png`: bố cục đoạn 1 (1024 × 1536, nền cam đất nhạt); đáy là bờ cát sẫm sỏi đen và biển, đường bắt đầu từ mép nước; chấm xám số 1 là chỗ Bến Đá Đen; dải cam (dung nham) chạy ngang hết bề ngang, thanh xám số 2 ngang đường là cầu đá; chấm xám số 3 là chỗ Rừng Than Hồng; chấm xám số 4 là chỗ Sườn Núi Khói; chấm xám số 5 là chỗ Lò Lửa Thiền | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\hoa70\tai_ve\doan_1.png` |
| 2: đoạn giữa, địa danh 6, 7, 8 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_hoa_70\luot_2.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\hoa70\doan_1.png`: đoạn 1 bản đồ đảo Hỏa đã duyệt (1024 × 1536); 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_hoa_70\bo_cuc_2.png`: bố cục đoạn 2 (1024 × 1536, nền cam đất nhạt); dải 160 px ở đáy là dải đỉnh của đoạn 1; chấm cam số 6 là hồ dung nham Chùa Liên Hoa, lạch dung nham chảy ra mép trái; chấm xám số 7 là chỗ Lò Rèn Gai Thép; chấm xám số 8 là chỗ Rừng Lửa Ảo; 3 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\zone_hoa.png`: bản đồ đảo Hỏa 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền đỏ cam gạch chì, đường mòn mảnh có 8 vòng tròn kem, sông dung nham cam, núi lửa có bánh xe vàng trên đỉnh, cổng bánh xe, lò đá tròn, chùa sen mái đỏ, cây cháy tán cam, đất nứt, đá đen, bến gỗ ở đáy; lấy màu và dáng đồ vật (không lấy bánh xe vàng) | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\hoa70\tai_ve\doan_2.png` |
| 3: đoạn trên, địa danh 9, 10 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_hoa_70\luot_3.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\hoa70\doan_2.png`: đoạn 2 bản đồ đảo Hỏa đã duyệt (1024 × 1536); 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_hoa_70\bo_cuc_3.png`: bố cục đoạn 3 (1024 × 1536, nền cam đất nhạt); dải 160 px ở đáy là dải đỉnh của đoạn 2; chấm xám số 9 là chỗ Hang Hồng Ngọc; đường kết thúc ở bãi đấu tròn lớn gần đỉnh, chấm nâu đỏ sẫm số 10 sau bãi là núi lửa; dải biển dọc mép trên; 3 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\zone_hoa.png`: bản đồ đảo Hỏa 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền đỏ cam gạch chì, đường mòn mảnh có 8 vòng tròn kem, sông dung nham cam, núi lửa có bánh xe vàng trên đỉnh, cổng bánh xe, lò đá tròn, chùa sen mái đỏ, cây cháy tán cam, đất nứt, đá đen, bến gỗ ở đáy; lấy màu và dáng đồ vật (không lấy bánh xe vàng) | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\hoa70\tai_ve\doan_3.png` |

Bản duyệt Claude lưu ở `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\hoa70\doan_<k>.png`. Không để ảnh vào `E:\ProjectAtomik\PokiWar\ArtGen\Islands\inbox` (menu nhập ảnh sẽ chép nguyên khổ vào game).

## Địa danh

| Số | Chặng (ải) | Vẽ gì |
|---|---|---|
| 1 | Bến Đá Đen (1–4) | đá bazan đen mặt sáu cạnh, bến gỗ ngắn trên cọc đen, thuyền gỗ cũ kéo lên bờ cát sẫm cạnh đầu đường |
| 2 | Suối Dung Nham (5–9) | cầu vòm đá bazan qua sông dung nham, rộng bằng đường, lan can đá thấp; đá đen, cây cháy hai bờ |
| 3 | Rừng Than Hồng (10–14) | rừng cây cháy đen, vỏ có vết nứt cam, tán lá tròn cam đỏ, xen đá đen |
| 4 | Sườn Núi Khói (15–19) | sườn đá xám xếp lớp, ba lỗ phun viền lưu huỳnh vàng; không vẽ khói (game thêm) |
| 5 | Lò Lửa Thiền (20–29) | lò vòm tròn gạch đá xám có cửa vòm tối, cạnh bệ thiền đá nhỏ có lư hương đồng và hai đèn đá |
| 6 | Chùa Liên Hoa (30–39) | hồ dung nham tròn có lá sen đá, chùa nhỏ mái đỏ cong có hoa sen vàng trên nóc đứng trên mỏm đá sau hồ; lạch dung nham chảy ra mép |
| 7 | Lò Rèn Gai Thép (40–49) | lò rèn mái tôn đen, ống khói đá cao, đe lớn, giá khiên và giáo gai thép; vài gai sắt cắm quanh |
| 8 | Rừng Lửa Ảo (50–59) | rừng cây xoắn lạ, tán lá hình ngọn lửa (lá, không phải lửa) cam, hồng, tím; vài pha lê tím tròn giữa rễ |
| 9 | Hang Hồng Ngọc (60–69) | miệng hang trong đồi đá sẫm, hồng ngọc đỏ to tua tủa |
| 10 | Miệng Núi Lửa (70) | núi lửa sẫm ngay sau bãi đấu boss, miệng rộng đầy dung nham, vài dòng dung nham chảy xuống hai bên sườn (không chạm bãi), hai tượng đá hộ vệ nhỏ ở chân núi, đỉnh chạm dải biển trên |

## Soi trước khi nhắn Claude

- Đảo núi lửa đỏ cam (không phải đảo rừng xanh lá như ảnh mẫu đảo Mộc), nét và cách dựng giống ảnh mẫu.
- Đường cát rộng đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường và các bãi tròn **trống**.
- Địa danh đúng số, đứng sát đường, không đè lên đường.
- Dung nham là mảng cam vàng phẳng có vân vỏ sẫm, không quầng sáng, không bọt, không khói.
- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).
- Lượt 1, 2: dải 160 px trên cùng chỉ có đường, đất, bụi, đá.
- Không chữ, không số, không sinh vật, người; không viền đảo ở hai bên; không khói, lửa, tàn lửa, lấp lánh (game thêm).

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Ra màu xanh lá, cây rừng như đảo Mộc | `Same layout, but this is the red-orange volcanic Fire island: warm red-orange hatched ground, charred trees with orange crowns, black basalt rocks, red crystals; no green grass, no green forest trees.` |
| Có khói, lửa, quầng sáng | `Same image, but remove all smoke, flames, sparks, embers and glows. Lava stays a flat orange and yellow surface with dark crust lines.` |
| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road and the round clearings completely empty: remove everything standing on them.` |
| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round clearings.` |
| Có số, chữ | `Same image without any numbers, letters or text.` |
| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |
| Dải đáy không nối với đoạn trước | `Redraw it so the bottom 160 px show exactly the same scene as the painted bottom strip of the sketch: same road position and width, same trees and rocks.` |
| Dung nham hay chân núi lửa đè lên bãi đấu | `Same image, but the volcano and its lava stay behind the arena: the round arena is completely empty.` |
| Quá vụn, kiểu 3D | `Too detailed and too realistic. Redraw it as a hand-drawn notebook map: pencil hatching on cream paper, wobbly ink outlines, every tree and rock a chunky doodle with a clear silhouette. Keep the same layout.` |
