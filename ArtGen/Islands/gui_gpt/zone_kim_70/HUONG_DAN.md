# Gói gửi GPT: bản đồ dài đảo Kim 70 ải (`zone_kim_70`)

Sinh bằng `E:\ProjectAtomik\PokiWar\ArtGen\Islands\build_zone70_kim.py`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Kim mới cho 70 ải, cùng khuôn bản đồ dài đảo Thủy, Mộc, Hỏa: một bản đồ dọc ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ 1024 × 4288. Đường cát rộng lượn chữ S (lượn trái trước, như đảo Mộc) từ cảng sắt lên bãi đấu boss dưới núi thép có tháp chuông, 10 bãi tròn cho 10 ải tướng, địa danh của từng chặng đứng sát đường. Không vẽ vòng tròn ải: game đặt bệ tướng và chấm ải lên đường. Khói, hơi nước, tia lửa, lấp lánh, sóng là phần động game thêm sau, GPT không vẽ.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude "duyệt đoạn <k> đảo Kim"; Claude soi, lưu bản duyệt và dựng file prompt của lượt sau. Nên làm cả 3 lượt trong cùng một chat để GPT giữ nét.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
| 1: đoạn dưới, địa danh 1, 2, 3, 4, 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_kim_70\luot_1.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\moc70\doan_1.png`: đoạn 1 bản đồ dài đảo Mộc đã duyệt (1024 × 1536, nền đặc): đường cát rộng lượn có bãi tròn, bậc đất có vách ngắn, cây tròn, đá, đồ vật chen sát đường, nền xanh lá; lấy nét và cách dựng, không lấy màu, đồ vật rừng, bố cục; 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\zone_kim.png`: bản đồ đảo Kim 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền xám xanh gạch chì, đường mòn mảnh có 8 vòng tròn kem, núi xám đỉnh trắng, đá xám sẫm, suối xám xanh, cần cẩu sắt ở cảng, chòi canh thép, nhà chuông mái sẫm, cửa mỏ có xe goòng, lò đúc, tổ thép, miếu đá có cánh trên đỉnh; lấy màu và dáng đồ vật; 3 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_kim_70\bo_cuc_1.png`: bố cục đoạn 1 (1024 × 1536, nền xám xanh nhạt); đáy là bờ sỏi xám, cát nhạt và biển, đường bắt đầu từ mép nước; chấm xám số 1 là chỗ Cảng Sắt; dải xanh (sông) chạy ngang hết bề ngang, thanh màu đồng số 2 ngang đường là cầu sắt bánh răng; chấm xám số 3 là chỗ Rừng Lưỡi Liềm; chấm xám số 4 là chỗ Tháp Canh Thép; chấm xám số 5 là chỗ Gác Chuông Đồng | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\kim70\tai_ve\doan_1.png` |
| 2: đoạn giữa, địa danh 6, 7, 8 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_kim_70\luot_2.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\kim70\doan_1.png`: đoạn 1 bản đồ đảo Kim đã duyệt (1024 × 1536); 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_kim_70\bo_cuc_2.png`: bố cục đoạn 2 (1024 × 1536, nền xám xanh nhạt); dải 160 px ở đáy là dải đỉnh của đoạn 1; chấm xanh số 6 là hồ nước của Xưởng Đúc Chuông, lạch nước chảy ra mép phải; chấm xám số 7 là chỗ Mỏ Sắt Ngân; chấm xám số 8 là chỗ Thành Ba Kiếm; 3 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\zone_kim.png`: bản đồ đảo Kim 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền xám xanh gạch chì, đường mòn mảnh có 8 vòng tròn kem, núi xám đỉnh trắng, đá xám sẫm, suối xám xanh, cần cẩu sắt ở cảng, chòi canh thép, nhà chuông mái sẫm, cửa mỏ có xe goòng, lò đúc, tổ thép, miếu đá có cánh trên đỉnh; lấy màu và dáng đồ vật | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\kim70\tai_ve\doan_2.png` |
| 3: đoạn trên, địa danh 9, 10 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_kim_70\luot_3.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\kim70\doan_2.png`: đoạn 2 bản đồ đảo Kim đã duyệt (1024 × 1536); 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_kim_70\bo_cuc_3.png`: bố cục đoạn 3 (1024 × 1536, nền xám xanh nhạt); dải 160 px ở đáy là dải đỉnh của đoạn 2; chấm xám số 9 là chỗ Tổ Cánh Pha Lê; đường kết thúc ở bãi đấu tròn lớn gần đỉnh, chấm xám đá sẫm số 10 sau bãi là núi thép có tháp chuông; dải biển dọc mép trên; 3 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\zone_kim.png`: bản đồ đảo Kim 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền xám xanh gạch chì, đường mòn mảnh có 8 vòng tròn kem, núi xám đỉnh trắng, đá xám sẫm, suối xám xanh, cần cẩu sắt ở cảng, chòi canh thép, nhà chuông mái sẫm, cửa mỏ có xe goòng, lò đúc, tổ thép, miếu đá có cánh trên đỉnh; lấy màu và dáng đồ vật | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\kim70\tai_ve\doan_3.png` |

Bản duyệt Claude lưu ở `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\kim70\doan_<k>.png`. Không để ảnh vào `E:\ProjectAtomik\PokiWar\ArtGen\Islands\inbox` (menu nhập ảnh sẽ chép nguyên khổ vào game).

## Địa danh

| Số | Chặng (ải) | Vẽ gì |
|---|---|---|
| 1 | Cảng Sắt (1–4) | cảng sắt nhỏ cạnh đầu đường: cần cẩu sắt tán đinh có móc lớn, thùng kim loại xếp chồng, vài thùng phuy, mỏ neo sắt trên sỏi xám |
| 2 | Cầu Bánh Răng (5–9) | cầu tấm sắt tán đinh qua sông, rộng bằng đường, mỗi đầu cầu một bánh răng đồng lớn dựng đứng cạnh đường; mặt cầu trống |
| 3 | Rừng Lưỡi Liềm (10–14) | rừng cây thân xám bạc, tán tròn lá dài cong hình lưỡi liềm (lá, không phải vũ khí) xanh thép và xanh nhạt, xen đá xám |
| 4 | Tháp Canh Thép (15–19) | tháp canh khung thép tán đinh cao, chòi canh nhỏ trên đỉnh, chóp nhọn như mũi thương, vài thùng sắt dưới chân |
| 5 | Gác Chuông Đồng (20–29) | nhà chuông mở mái đá sẫm trên bốn cột gỗ to, nền đá vuông, chuông đồng lớn treo bên trong |
| 6 | Xưởng Đúc Chuông (30–39) | hồ nước làm nguội tròn; sau hồ trên mỏm đá là xưởng đúc chuông: lò đá thấp có ống khói ngắn, nồi sắt đầy đồng nóng chảy (mảng cam vàng phẳng, không quầng sáng), hai chuông đồng trên giá gỗ; lạch nước chảy ra mép |
| 7 | Mỏ Sắt Ngân (40–49) | cửa mỏ khung gỗ dày trong đồi đá xám, đường ray ngắn chạy ra có xe goòng đầy quặng bạc |
| 8 | Thành Ba Kiếm (50–59) | cổng thành đá xám nhỏ có hai tháp thấp, cửa sắt đóng; trước cổng ba thanh kiếm khổng lồ cắm mũi xuống đất, chuôi đỏ, xanh, vàng |
| 9 | Tổ Cánh Pha Lê (60–69) | tổ tròn lớn đan bằng thanh thép uốn trên mỏm đá, mảnh pha lê xanh nhạt dài cắm quanh vành như lông vũ; tổ trống |
| 10 | Tháp Thiên Chung (70) | núi thép xám đỉnh tuyết trắng ngay sau bãi đấu boss, trên đỉnh là tháp chuông đá và thép tán đinh mái đồng cong, chuông đồng khổng lồ ở tầng trên mở; hai tượng đá đôi cánh xếp nhỏ ở chân núi hai bên sau bãi; đỉnh tháp chạm dải biển trên |

## Soi trước khi nhắn Claude

- Đảo kim loại xám xanh (không phải đảo rừng xanh lá như ảnh mẫu đảo Mộc), nét và cách dựng giống ảnh mẫu.
- Đường cát rộng đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường, mặt cầu và các bãi tròn **trống**.
- Địa danh đúng số, đứng sát đường, không đè lên đường.
- Sông, hồ, lạch là nước xám xanh có bờ đá, không bọt, không thác; đồng nóng chảy trong nồi là mảng cam vàng phẳng.
- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).
- Lượt 1, 2: dải 160 px trên cùng chỉ có đường, đất, bụi, đá.
- Không chữ, không số, không sinh vật, người máy, người; không viền đảo ở hai bên; không khói, hơi nước, tia lửa, lấp lánh (game thêm).

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Ra màu xanh lá, cây rừng như đảo Mộc | `Same layout, but this is the cool blue-grey Metal island: blue-grey hatched ground, grey rocks and peaks, iron and bronze props, silver-grey trees with steel-blue crowns; no green grass, no green forest trees.` |
| Kim loại bóng loáng, kiểu 3D | `Too shiny and too realistic. Redraw the metal as flat colour-pencil hatching with wobbly ink outlines, no chrome reflections, no gradients. Keep the same layout.` |
| Có khói, hơi nước, tia lửa, quầng sáng | `Same image, but remove all smoke, steam, sparks, flames, sparkles and glows. The molten bronze stays a flat orange and yellow surface.` |
| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road, the bridge deck and the round clearings completely empty: remove everything standing on them.` |
| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round clearings.` |
| Có số, chữ | `Same image without any numbers, letters or text.` |
| Có người, người máy, sinh vật | `Same image without any people, robots or creatures.` |
| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |
| Dải đáy không nối với đoạn trước | `Redraw it so the bottom 160 px show exactly the same scene as the painted bottom strip of the sketch: same road position and width, same trees and rocks.` |
| Chân núi hay tháp chuông đè lên bãi đấu | `Same image, but the mountain and the bell tower stay behind the arena: the round arena is completely empty.` |
| Quá vụn | `Too detailed. Redraw it as a hand-drawn notebook map: pencil hatching on cream paper, wobbly ink outlines, every rock, tree and prop a chunky doodle with a clear silhouette. Keep the same layout.` |
