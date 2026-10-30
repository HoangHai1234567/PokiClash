# Màn hình dọc

Mọi số ở đây là đề xuất, tính trên khung tham chiếu **1080 × 1920** (9:16). Máy dài hơn (9:19,5, 9:21) thì phần dôi ra dồn cho sân đấu. Máy tính bảng (3:4) thì bàn giữ cỡ tối đa, hai bên để viền.

## Bố cục màn trận

| Vùng | Chiều cao (% màn) | Chứa gì |
|---|---|---|
| Thanh trên | 0–6 | nút dừng, tên ải, đợt 1/3, vàng nhặt được |
| Sân đấu | 6–38 | địch ở trên (mặt trước, nhìn ra người chơi), máu và số lượt đếm ngược trên đầu; đội mình ở dưới (mặt sau), như bố cục trận của Aola và Pokémon |
| Hàng tướng | 38–44 | 3–5 chân dung tướng, mỗi cái một vòng nộ; nộ đầy thì chạm để tung chiêu |
| Bàn | 44–84 | bàn 8 × 8; ô khoảng 112 px, bàn khoảng 900 px, chừa lề hai bên |
| Khay | 84–95 | 3 khối thu nhỏ 0,5 |
| Vùng an toàn | 95–100 | để trống cho thanh điều hướng của máy |

Lý do xếp như vậy:

- **Ngón cái ở dưới.** Kéo khối là việc làm nhiều nhất, nên khay nằm sát đáy. Chạm tung chiêu làm ít hơn, nên hàng tướng nằm giữa màn, vẫn với tới bằng một tay.
- **Đòn đi từ dưới lên.** Xoá một hàng thì các ô bay từ bàn lên chân dung tướng cùng màu, rồi tướng đánh lên địch. Mắt người chơi đi một đường thẳng từ dưới lên trên, nên hiểu ngay đòn từ đâu ra.
- **Khối nhấc lên trên ngón tay** khi kéo, để ngón tay không che chỗ đặt. Bản Block Blast ở 2PlayersGame đã đo sẵn độ nhấc (khoảng 2,2 ô cộng phần theo chiều cao khối), dùng lại được.

## Các màn khác

- **Bản đồ ải:** cuộn dọc từ dưới lên, như Candy Crush. Mỗi chương là một vùng, boss ở đỉnh vùng.
- **Danh sách tướng:** lưới 3 cột, thẻ dọc. Lọc theo hệ.
- **Máy bi:** máy đứng dọc chiếm gần cả màn, bi rơi từ trên xuống, hợp màn dọc hơn bất cứ màn nào khác ([07_MayBi.md](07_MayBi.md)).
- **Thanh dưới của menu:** 5 tab (Tướng, Máy bi, Ải ở giữa, Đấu trường, Cửa hàng). Tab giữa to nhất.

## Cài đặt Unity

Project hiện để **tự xoay** (`defaultScreenOrientation: 4`, cho phép cả ngang) và khung mặc định 1024 × 768. Cần đổi:

- Player Settings → Resolution and Presentation → Default Orientation: **Portrait**. Bỏ chọn hai hướng ngang và Portrait Upside Down.
- Canvas Scaler: Scale With Screen Size, 1080 × 1920, **Match = 0 (theo chiều rộng)**. Bàn và khay bám chiều rộng; sân đấu giãn theo phần chiều cao còn lại.
- Một thành phần Safe Area cho tai thỏ và thanh điều hướng.
- Game view của Editor: thêm khung 1080 × 1920, 1080 × 2400 và 1536 × 2048 để soi ba kiểu máy.
- Nếu bàn và sân đấu vẽ trong world space (như bản Block Blast cũ, camera orthographic): tính cỡ camera theo chiều rộng, rồi đặt vị trí bàn và sân từ tỉ lệ màn hình lúc chạy.
