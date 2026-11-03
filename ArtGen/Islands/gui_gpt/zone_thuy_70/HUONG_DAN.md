# Gói gửi GPT: bản đồ dài đảo Thủy 70 ải (`zone_thuy_70`)

Sinh bằng `D:\PokiClash\ArtGen\Islands\build_zone70.py`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Thủy mới cho 70 ải: một bản đồ dọc dài ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ 1024 × 4288. Đường cát rộng lượn chữ S từ bãi biển lên bãi đấu boss, 10 bãi tròn trên đường cho 10 ải tướng, địa danh của từng chặng đứng sát đường. Không vẽ vòng tròn ải: game đặt bệ tướng và chấm ải lên đường.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude "duyệt đoạn <k>"; Claude soi, lưu bản duyệt và dựng file prompt của lượt sau. Nên làm cả 3 lượt trong cùng một chat để GPT giữ nét.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
| 1: đoạn dưới, địa danh 1, 2, 3, 4, 5 | `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_thuy_70\luot_1.txt` | 1 `D:\PokiClash\ArtGen\Islands\refs\world_style.png`: ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền biển xanh đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu hơi rung, tô chì màu gạch chéo; lấy nét, không lấy nội dung; 2 `D:\PokiClash\ArtGen\Islands\zones\zone_thuy.png`: bản đồ đảo Thủy 8 ải đang dùng (1024 × 1536, nền tối quầng xanh): đảo dọc nền ngọc lam gạch chì, đường mòn mảnh có 8 vòng tròn kem, thác, suối, cầu gỗ, hải đăng, nhà vỏ ốc, san hô, vỏ sò, hồ tròn; lấy màu và dáng đồ vật; 3 `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_thuy_70\bo_cuc_1.png`: bố cục đoạn 1 (1024 × 1536, nền xanh lá nhạt): đường cát rộng lượn chữ S, bãi tròn ở mỗi ải tướng; đáy là bãi cát và biển, đường bắt đầu từ mép nước; suối xanh chạy ngang từ mép trái sang mép phải, qua đường ở cầu; vịnh biển ăn vào từ mép phải tới chỗ hải đăng; chấm xám số 1 là chỗ Bãi Vỏ Sò; chấm xanh số 2 là Vũng San Hô; thanh nâu số 3 ngang đường là cầu gỗ; chấm xám số 4 là chỗ Làng Vỏ Ốc; chấm xám số 5 là chỗ Ngọn Hải Đăng | `D:\PokiClash\ArtGen\Islands\zones\thuy70\tai_ve\doan_1.png` |
| 2: đoạn giữa, địa danh 6, 7, 8 | `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_thuy_70\luot_2.txt` | 1 `D:\PokiClash\ArtGen\Islands\zones\thuy70\doan_1.png`: đoạn 1 đã duyệt (1024 × 1536); 2 `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_thuy_70\bo_cuc_2.png`: bố cục đoạn 2 (1024 × 1536, nền xanh lá nhạt); dải 160 px ở đáy là dải đỉnh của đoạn 1; hồ tròn dưới chỗ thác và suối chảy ra mép trái; chấm xám số 6 là chỗ Thác Bạc; chấm xanh số 7 là Rạn Ngọc Trai; chấm xanh số 8 là Hồ Gương | `D:\PokiClash\ArtGen\Islands\zones\thuy70\tai_ve\doan_2.png` |
| 3: đoạn trên, địa danh 9, 10 | `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_thuy_70\luot_3.txt` | 1 `D:\PokiClash\ArtGen\Islands\zones\thuy70\doan_2.png`: đoạn 2 đã duyệt (1024 × 1536); 2 `D:\PokiClash\ArtGen\Islands\gui_gpt\zone_thuy_70\bo_cuc_3.png`: bố cục đoạn 3 (1024 × 1536, nền xanh lá nhạt); dải 160 px ở đáy là dải đỉnh của đoạn 2; đường kết thúc ở bãi đấu tròn lớn gần đỉnh; dải biển dọc mép trên; chấm xám số 9 là chỗ Đền Rùa Cổ; chấm xanh số 10 là Xoáy Nước Đinh Ba | `D:\PokiClash\ArtGen\Islands\zones\thuy70\tai_ve\doan_3.png` |

Bản duyệt Claude lưu ở `D:\PokiClash\ArtGen\Islands\zones\thuy70\doan_<k>.png`. Không để ảnh vào `D:\PokiClash\ArtGen\Islands\inbox` (menu nhập ảnh sẽ chép nguyên khổ vào game).

## Soi trước khi nhắn Claude

- Đường cát rộng đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường và các bãi tròn **trống**.
- Địa danh đúng số, đứng sát đường, không đè lên đường.
- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).
- Lượt 1, 2: dải 160 px trên cùng chỉ có đường, đất, bụi, đá.
- Không chữ, không số, không sinh vật, người; không viền đảo ở hai bên; không xoáy nước, đinh ba, bọt sóng.

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road and the round clearings completely empty: remove everything standing on them.` |
| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round clearings.` |
| Có số, chữ | `Same image without any numbers, letters or text.` |
| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |
| Dải đáy không nối với đoạn trước | `Redraw it so the bottom 160 px show exactly the same scene as the painted bottom strip of the sketch: same road position and width, same trees and rocks.` |
| Quá vụn, kiểu 3D | `Too detailed and too realistic. Redraw it as a hand-drawn notebook map: pencil hatching on cream paper, wobbly ink outlines, every tree and rock a chunky doodle with a clear silhouette. Keep the same layout.` |
