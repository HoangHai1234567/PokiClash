# Gói gửi GPT: bản đồ dài đảo Mộc 70 ải (`zone_moc_70`)

Sinh bằng `D:\PokiClash\ArtGen\Islands\build_zone70_moc.py`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Mộc mới cho 70 ải, cùng khuôn bản đồ dài đảo Thủy: một bản đồ dọc ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ 1024 × 4288. Đường cát rộng lượn chữ S (lượn trái trước, ngược đảo Thủy) từ bờ rêu lên bãi đấu boss dưới cây thần, 10 bãi tròn cho 10 ải tướng, địa danh của từng chặng đứng sát đường. Không vẽ vòng tròn ải: game đặt bệ tướng và chấm ải lên đường.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude "duyệt đoạn <k> đảo Mộc"; Claude soi, lưu bản duyệt và dựng file prompt của lượt sau. Nên làm cả 3 lượt trong cùng một chat để GPT giữ nét. Gói nền trận đảo Mộc (`ArtGen\BattleBG\gui_gpt\moc`) làm song song được, ở một chat khác.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
| 1: đoạn dưới, địa danh 1, 2, 3, 4, 5 | `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_moc_70\luot_1.txt` | 1 `D:\PokiClash\ArtGen\Islands\zones\thuy70\doan_1.png`: đoạn 1 bản đồ dài đảo Thủy đã duyệt (1024 × 1536, nền đặc): đường cát rộng lượn có bãi tròn, bậc đất có vách ngắn, cọ, đá, đồ vật chen sát đường, đất ngọc lam; lấy nét và cách dựng, không lấy màu, đồ vật biển, bố cục; 2 `D:\PokiClash\ArtGen\Islands\zones\zone_moc.png`: bản đồ đảo Mộc 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền xanh lá gạch chì, đường mòn mảnh có 8 vòng tròn kem, sông xanh, nấm đỏ chấm trắng, vòm dây leo, hang đá có nanh, cụm hoa, cây thần có miếu nhỏ, cây tròn, đá xám; lấy màu và dáng đồ vật; 3 `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_moc_70\bo_cuc_1.png`: bố cục đoạn 1 (1024 × 1536, nền xanh lá nhạt); đáy là bờ cát sỏi rêu và biển, đường bắt đầu từ mép nước; chấm xám số 1 là chỗ Bờ Rêu; chấm xám số 2 là chỗ Đồng Hoa Sáng; chấm xám số 3 là chỗ Đồi Nấm; suối xanh chạy ngang hết bề ngang, thanh nâu số 4 ngang đường là cầu dây leo; chấm xám số 5 là chỗ Hang Nanh Gió | `D:\PokiClash\ArtGen\Islands\zones\moc70\tai_ve\doan_1.png` |
| 2: đoạn giữa, địa danh 6, 7, 8 | `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_moc_70\luot_2.txt` | 1 `D:\PokiClash\ArtGen\Islands\zones\moc70\doan_1.png`: đoạn 1 bản đồ đảo Mộc đã duyệt (1024 × 1536); 2 `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_moc_70\bo_cuc_2.png`: bố cục đoạn 2 (1024 × 1536, nền xanh lá nhạt); dải 160 px ở đáy là dải đỉnh của đoạn 1; chấm xanh số 6 là hồ lá sen Thung Lũng Lá, lạch nước chảy ra mép phải; chấm xám số 7 là chỗ Vách Vuốt Rồng; chấm xám số 8 là chỗ Rừng Trúc Ngọc; 3 `D:\PokiClash\ArtGen\Islands\zones\zone_moc.png`: bản đồ đảo Mộc 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền xanh lá gạch chì, đường mòn mảnh có 8 vòng tròn kem, sông xanh, nấm đỏ chấm trắng, vòm dây leo, hang đá có nanh, cụm hoa, cây thần có miếu nhỏ, cây tròn, đá xám; lấy màu và dáng đồ vật | `D:\PokiClash\ArtGen\Islands\zones\moc70\tai_ve\doan_2.png` |
| 3: đoạn trên, địa danh 9, 10 | `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_moc_70\luot_3.txt` | 1 `D:\PokiClash\ArtGen\Islands\zones\moc70\doan_2.png`: đoạn 2 bản đồ đảo Mộc đã duyệt (1024 × 1536); 2 `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_moc_70\bo_cuc_3.png`: bố cục đoạn 3 (1024 × 1536, nền xanh lá nhạt); dải 160 px ở đáy là dải đỉnh của đoạn 2; chấm xám số 9 là chỗ Hang Pha Lê Lục; đường kết thúc ở bãi đấu tròn lớn gần đỉnh, chấm xanh sẫm số 10 sau bãi là gốc cây thần; dải biển dọc mép trên; 3 `D:\PokiClash\ArtGen\Islands\zones\zone_moc.png`: bản đồ đảo Mộc 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền xanh lá gạch chì, đường mòn mảnh có 8 vòng tròn kem, sông xanh, nấm đỏ chấm trắng, vòm dây leo, hang đá có nanh, cụm hoa, cây thần có miếu nhỏ, cây tròn, đá xám; lấy màu và dáng đồ vật | `D:\PokiClash\ArtGen\Islands\zones\moc70\tai_ve\doan_3.png` |

Bản duyệt Claude lưu ở `D:\PokiClash\ArtGen\Islands\zones\moc70\doan_<k>.png`. Không để ảnh vào `D:\PokiClash\ArtGen\Islands\inbox` (menu nhập ảnh sẽ chép nguyên khổ vào game).

## Địa danh

| Số | Chặng (ải) | Vẽ gì |
|---|---|---|
| 1 | Bờ Rêu (1–4) | đá tròn phủ rêu, thuyền gỗ cũ phủ rêu trên bờ cạnh đầu đường |
| 2 | Đồng Hoa Sáng (5–9) | đồng hoa chuông khổng lồ thân cao, cánh vàng nhạt, hồng, xanh trời |
| 3 | Đồi Nấm (10–14) | đồi cỏ nhỏ mọc đầy nấm khổng lồ mũ đỏ, cam chấm kem; hai cây to là nhà có cửa gỗ tròn |
| 4 | Rừng Dây Leo (15–19) | cầu gỗ quấn dây leo qua suối, rộng bằng đường; cây cao rủ dây leo hai bờ |
| 5 | Hang Nanh Gió (20–29) | miệng hang tối trong gò đá xám, mép trên dưới có nanh đá nhọn như miệng mở; vài cây gió uốn |
| 6 | Thung Lũng Lá (30–39) | hồ tròn đầy lá sen khổng lồ, vài bông súng hồng, cây lá to; lạch nước chảy ra mép |
| 7 | Vách Vuốt Rồng (40–49) | vách đá xám xanh có ba vết vuốt chéo khổng lồ, hai mỏm đá cong như vuốt |
| 8 | Rừng Trúc Ngọc (50–59) | rừng trúc xanh ngọc quanh miếu đá nhỏ mái ngói xanh cong, hai đèn đá |
| 9 | Hang Pha Lê Lục (60–69) | miệng hang trong đồi đá rêu, pha lê lục bảo to tua tủa |
| 10 | Cây Thần Ngàn Năm (70) | cây thần cổ thụ sau bãi đấu boss, thân to sần có miếu nhỏ trong hốc, rễ ôm sau bãi, tán tròn phủ tới biển trên |

## Soi trước khi nhắn Claude

- Đảo rừng xanh lá (không phải đảo biển ngọc lam như ảnh mẫu đảo Thủy), nét và cách dựng giống ảnh mẫu.
- Đường cát rộng đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường và các bãi tròn **trống**.
- Địa danh đúng số, đứng sát đường, không đè lên đường.
- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).
- Lượt 1, 2: dải 160 px trên cùng chỉ có đường, đất, bụi, đá.
- Không chữ, không số, không sinh vật, người; không viền đảo ở hai bên; không lá bay, đom đóm, lấp lánh, vệt gió (game thêm).

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Ra màu ngọc lam, đồ biển như đảo Thủy | `Same layout, but this is the green forest island: lush green hatched ground, broad-leaf trees, pines, ferns, mushrooms and mossy rocks; no palm trees, no turquoise ground, no seaside props.` |
| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road and the round clearings completely empty: remove everything standing on them.` |
| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round clearings.` |
| Có số, chữ | `Same image without any numbers, letters or text.` |
| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |
| Dải đáy không nối với đoạn trước | `Redraw it so the bottom 160 px show exactly the same scene as the painted bottom strip of the sketch: same road position and width, same trees and rocks.` |
| Rễ, tán cây thần đè lên bãi đấu | `Same image, but the great tree's roots and crown stay behind the arena: the round arena is completely empty.` |
| Quá vụn, kiểu 3D | `Too detailed and too realistic. Redraw it as a hand-drawn notebook map: pencil hatching on cream paper, wobbly ink outlines, every tree and rock a chunky doodle with a clear silhouette. Keep the same layout.` |
