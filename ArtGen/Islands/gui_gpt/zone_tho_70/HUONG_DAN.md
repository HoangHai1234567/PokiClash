# Gói gửi GPT: bản đồ dài đảo Thổ 70 ải (`zone_tho_70`)

Sinh bằng `E:\ProjectAtomik\PokiWar\ArtGen\Islands\build_zone70_tho.py`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Thổ mới cho 70 ải, cùng khuôn bản đồ dài đảo Thủy, Mộc, Hỏa, Kim: một bản đồ dọc ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ 1024 × 4288. Đường cát kem rộng lượn chữ S (lượn phải trước) từ bãi đá cuội lên bãi đấu boss dưới kim tự tháp có đền mái vàng, 10 bãi tròn cho 10 ải tướng, địa danh của từng chặng đứng sát đường. Đường qua hẻm núi khô bằng cầu treo ngay sau bãi ải 5. Không vẽ vòng tròn ải: game đặt bệ tướng và chấm ải lên đường. Khói, bụi, lửa, lấp lánh, sóng là phần động game thêm sau, GPT không vẽ.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude "duyệt đoạn <k> đảo Thổ"; Claude soi, lưu bản duyệt và dựng file prompt của lượt sau. Nên làm cả 3 lượt trong cùng một chat để GPT giữ nét.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
| 1: đoạn dưới, địa danh 1, 2, 3, 4, 5 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_tho_70\luot_1.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\moc70\doan_1.png`: đoạn 1 bản đồ dài đảo Mộc đã duyệt (1024 × 1536, nền đặc): đường cát rộng lượn có bãi tròn, bậc đất có vách ngắn, cây tròn, đá, đồ vật chen sát đường, nền xanh lá; lấy nét và cách dựng, không lấy màu, đồ vật rừng, bố cục; 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\zone_tho.png`: bản đồ đảo Thổ 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền vàng đất gạch chì có vân gió, đường mòn mảnh có 8 vòng tròn kem, núi đất đỏ đỉnh bằng, đá xám, đồi ruộng bậc thang, bệ đá có cọc gỗ, lòng sông khô nứt có cầu treo, ốc đảo có cây dừa, trên đỉnh là đền cột đỏ mái vàng trên nền đá bậc và hai tượng sư tử đá; lấy màu và dáng đồ vật; 3 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_tho_70\bo_cuc_1.png`: bố cục đoạn 1 (1024 × 1536, nền vàng đất); đáy là bờ cát nhạt, đá cuội và biển, đường bắt đầu từ mép nước; dải nâu sẫm chạy ngang hết bề ngang là hẻm núi khô, thanh màu gỗ có vạch ngang đường là cầu treo; chấm xám số 1 là chỗ Bãi Đá Cuội; chấm xám số 2 là chỗ Hang Lửng; chấm xám số 3 là chỗ Đồi Ngọc Lục; chấm xám số 4 là chỗ Mỏ Pha Lê; chấm xám số 5 là chỗ Đền Phù Văn | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\tho70\tai_ve\doan_1.png` |
| 2: đoạn giữa, địa danh 6, 7, 8 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_tho_70\luot_2.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\tho70\doan_1.png`: đoạn 1 bản đồ đảo Thổ đã duyệt (1024 × 1536); 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_tho_70\bo_cuc_2.png`: bố cục đoạn 2 (1024 × 1536, nền vàng đất); dải 160 px ở đáy là dải đỉnh của đoạn 1; chấm xanh số 6 là hồ nước của Rừng Sồi Già, lạch nước chảy ra mép trái; chấm xám số 7 là chỗ Ruộng Bậc Thang; chấm xám số 8 là chỗ Vách Kim Cương; 3 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\zone_tho.png`: bản đồ đảo Thổ 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền vàng đất gạch chì có vân gió, đường mòn mảnh có 8 vòng tròn kem, núi đất đỏ đỉnh bằng, đá xám, đồi ruộng bậc thang, bệ đá có cọc gỗ, lòng sông khô nứt có cầu treo, ốc đảo có cây dừa, trên đỉnh là đền cột đỏ mái vàng trên nền đá bậc và hai tượng sư tử đá; lấy màu và dáng đồ vật | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\tho70\tai_ve\doan_2.png` |
| 3: đoạn trên, địa danh 9, 10 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_tho_70\luot_3.txt` | 1 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\tho70\doan_2.png`: đoạn 2 bản đồ đảo Thổ đã duyệt (1024 × 1536); 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\gui_gpt\zone_tho_70\bo_cuc_3.png`: bố cục đoạn 3 (1024 × 1536, nền vàng đất); dải 160 px ở đáy là dải đỉnh của đoạn 2; chấm xám số 9 là chỗ Lò Gốm Đất Nung; đường kết thúc ở bãi đấu tròn lớn gần đỉnh, chấm xám sẫm số 10 sau bãi là kim tự tháp có đền mái vàng; dải biển dọc mép trên; 3 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\zone_tho.png`: bản đồ đảo Thổ 8 ải đang dùng (1024 × 1536, nền trong suốt): đảo dọc nền vàng đất gạch chì có vân gió, đường mòn mảnh có 8 vòng tròn kem, núi đất đỏ đỉnh bằng, đá xám, đồi ruộng bậc thang, bệ đá có cọc gỗ, lòng sông khô nứt có cầu treo, ốc đảo có cây dừa, trên đỉnh là đền cột đỏ mái vàng trên nền đá bậc và hai tượng sư tử đá; lấy màu và dáng đồ vật | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\tho70\tai_ve\doan_3.png` |

Bản duyệt Claude lưu ở `E:\ProjectAtomik\PokiWar\ArtGen\Islands\zones\tho70\doan_<k>.png`. Không để ảnh vào `E:\ProjectAtomik\PokiWar\ArtGen\Islands\inbox` (menu nhập ảnh sẽ chép nguyên khổ vào game).

## Địa danh

| Số | Chặng (ải) | Vẽ gì |
|---|---|---|
| 1 | Bãi Đá Cuội (1–4) | bãi đá cuội cạnh đầu đường: đống cuội tròn to nhỏ màu xám, be, đỏ gỉ, tháp đá dẹt xếp chồng cao, vỏ ốc xoắn lớn vùi nửa trong cát, khúc gỗ trôi dạt bạc màu |
| 2 | Hang Lửng (5–9) | hang lửng: gò đất phủ cỏ thấp có cửa hang tròn lớn, viền rễ cây và hai cột gỗ chống, đống đất mới đào, cuốc chim và xẻng dựng bên gò, vài cục vàng nhỏ trên đất; hang trống |
| 3 | Đồi Ngọc Lục (10–14) | đồi đá vàng đất nhỏ tròn, cụm pha lê xanh ngọc lục bảo to nhô ra sườn và đỉnh (màu phẳng, không lấp lánh) |
| 4 | Mỏ Pha Lê (15–19) | mỏ pha lê: cửa hang khung gỗ dày trong đồi đá vàng đất, cụm pha lê hồng tím quanh cửa, xe cút kít gỗ đầy pha lê hồng, mũi khoan xoắn lớn nằm dưới đất |
| 5 | Đền Phù Văn (20–29) | đền phù văn: vòng đá dựng cao màu xám trên nền đá tròn quanh phiến đá tế phẳng, đá khắc xoắn ốc, răng cưa, chấm (hoa văn, không phải chữ) |
| 6 | Rừng Sồi Già (30–39) | hồ tròn dưới gốc sồi cổ thụ: sồi đứng bờ sau hồ, thân to sần, rễ lớn thò xuống nước, tán tròn rộng xanh ô liu sẫm; quả sồi, hạt dẻ trên bờ, hai ba cây sồi nhỏ quanh; lạch nước chảy ra mép |
| 7 | Ruộng Bậc Thang (40–49) | đồi ruộng bậc thang: năm, sáu bậc ruộng xanh uốn quanh đồi tròn, bờ đất mảnh giữa các bậc, chòi mái rơm nhỏ trên bậc cao nhất, vài đống rơm dưới chân |
| 8 | Vách Kim Cương (50–59) | vách đá cao nhiều lớp vàng đất và nâu đỏ, kim cương xanh nhạt to nhô ra mặt vách (màu phẳng), đống kim cương rơi dưới chân vách |
| 9 | Lò Gốm Đất Nung (60–69) | xưởng gốm: lò gạch đỏ cao hình cổ chai, cửa lò vòm tối (không lửa, không quầng sáng), kệ gỗ xếp hàng chum, bình, vò đất nung đang phơi, bàn xoay gốm, đống củi |
| 10 | Kim Tự Viện (70) | kim tự tháp bậc bằng khối đá màu cát ngay sau bãi đấu boss, cầu thang thẳng rộng ở giữa đi xuống phía bãi đấu, đền nhỏ cột đỏ mái ngói vàng mái cong trên đỉnh; hai tượng sư tử đá lớn ngồi hai bên chân cầu thang, sau bãi; đỉnh đền chạm dải biển trên |

Hẻm núi khô có cầu treo (không thuộc chặng nào): khe sâu chạy ngang hết bề ngang ngay sau bãi ải 5, vách xa lộ vân đá nhiều lớp nâu đỏ và vàng đất, đáy gạch chì nâu sẫm, không nước, không dung nham; cầu ván gỗ buộc dây thừng giữa bốn cột gỗ, rộng bằng đường, mặt cầu trống.

## Soi trước khi nhắn Claude

- Đảo đất vàng (không phải đảo rừng xanh lá như ảnh mẫu đảo Mộc), nét và cách dựng giống ảnh mẫu.
- **Đường cát kem nhạt hơn hẳn nền vàng đất**, nhìn rõ mép đường (game dò đường theo màu cát nhạt).
- Đường đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường, mặt cầu và các bãi tròn **trống**.
- Địa danh đúng số, đứng sát đường, không đè lên đường.
- Lượt 1: hẻm núi khô (không có nước) chạy ngang, cầu treo rộng bằng đường, đường đi thẳng qua cầu.
- Hồ, lạch là nước xanh có bờ đá cuội, không bọt, không thác; lò gốm không có lửa.
- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).
- Lượt 1, 2: dải 160 px trên cùng chỉ có đường, đất, bụi, đá.
- Không chữ, không số, không sinh vật, người; không viền đảo ở hai bên; không khói, bụi, lửa, lấp lánh (game thêm).

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Ra màu xanh lá, cây rừng như đảo Mộc | `Same layout, but this is the warm golden-ochre Earth island: golden-ochre hatched ground, red-brown clay and sandstone, olive bushes and a few small trees; no bright green grass, no green forest.` |
| Đường lẫn vào nền | `Same image, but make the road and the clearings a much paler cream sand than the golden-ochre ground, with a clear wobbly ink edge.` |
| Hẻm núi có nước hoặc thành sông | `Same image, but the canyon is dry: layered rock walls going down to a dark brown bottom, no water, no lava.` |
| Cầu treo hẹp, lệch hay chắn đường | `Same image, but the rope bridge is exactly as wide as the road and the road runs straight across it; the bridge deck stays empty.` |
| Có khói, bụi, lửa, quầng sáng, lấp lánh | `Same image, but remove all smoke, dust, fire, flames, sparkles and glows. The kiln mouth is just dark, the crystals are flat colours.` |
| Đá đền Phù Văn có chữ | `Same image, but the standing stones carry only spirals, zigzags and dots, nothing that looks like letters or writing.` |
| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road, the bridge deck and the round clearings completely empty: remove everything standing on them.` |
| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round clearings.` |
| Có số, chữ | `Same image without any numbers, letters or text.` |
| Có người, sinh vật | `Same image without any people or creatures; stone statues are fine.` |
| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |
| Dải đáy không nối với đoạn trước | `Redraw it so the bottom 160 px show exactly the same scene as the painted bottom strip of the sketch: same road position and width, same trees and rocks.` |
| Kim tự tháp hay tượng sư tử đè lên bãi đấu | `Same image, but the pyramid, its stairway and the stone lions stay behind the arena: the round arena is completely empty.` |
| Quá vụn | `Too detailed. Redraw it as a hand-drawn notebook map: pencil hatching on cream paper, wobbly ink outlines, every rock, tree and prop a chunky doodle with a clear silhouette. Keep the same layout.` |
