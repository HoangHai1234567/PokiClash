# GD_Claude: tài liệu thiết kế PokiWar

Game đánh nhau, vượt ải để thu phục tướng, ghép puzzle xếp khối, **màn hình dọc**. Cảm hứng: Pokiwar (CMN Online, đã ngừng). Viết 2026-10-30, mọi con số là đề xuất, chưa thử.

## Tóm tắt đề xuất

- **Lõi: bàn Block Blast 8 × 8, mỗi khối mang màu một hệ. Xoá hàng hay cột thì tướng cùng hệ ra đòn.** Đây là ý "ngọc quyết định hành động" của Pokiwar, đặt lên luật Block Blast.
- Bố cục dọc: sân đấu ở trên (địch mặt trước, đội mình mặt sau), hàng chân dung tướng ở giữa, bàn và khay ở dưới tầm ngón cái.
- Thu phục bằng **pha phong ấn**: tướng hoang còn ít máu thì người chơi phải xoá đủ các đường ấn trong vài lượt. Hụt thì rơi mảnh; đủ 10 mảnh ra tướng, nên không bao giờ kẹt vì xui.
- **Khối sập** (trọng lực, xoá dây chuyền) làm cơ chế boss và chế độ Tháp, không làm lõi.
- **Máy bi**: chỗ phát thưởng nuôi tướng, bi kiếm bằng chơi, in tỉ lệ trên máy, không mở tướng chưa gặp.

## Mục lục

| File | Nội dung |
|---|---|
| [01_HuongPhatTrien.md](01_HuongPhatTrien.md) | Pokiwar làm gì; 4 hướng (xếp khối, khối sập, xếp ngọc, máy bi tự đánh); so sánh; đề xuất |
| [02_ManHinhDoc.md](02_ManHinhDoc.md) | Bố cục màn trận và các màn khác; cài đặt Unity cho màn dọc |
| [03_XepKhoi.md](03_XepKhoi.md) | Luật bàn: màu là hệ, xoá ra đòn, ô đặc biệt, địch phá bàn, hết chỗ; biến thể sập |
| [04_ChienDau.md](04_ChienDau.md) | Đội 4 tướng, nhịp lượt, nộ và chiêu, địch, hiệu ứng, kết thúc trận |
| [05_VuotAi_ThuPhuc.md](05_VuotAi_ThuPhuc.md) | Bản đồ chương, pha phong ấn, mảnh, boss, Tháp Viễn Chinh |
| [06_Tuong_NuoiDuong.md](06_Tuong_NuoiDuong.md) | Thuộc tính tướng; cấp, sao, tiến hóa; nguồn hình từ dự án aola và rủi ro bản quyền |
| [07_MayBi.md](07_MayBi.md) | Máy bi Clash of Critters; khác ClashMaster ở đâu; máy bi Thu phục; chuyện kiếm tiền |
| [08_KyThuat_Unity.md](08_KyThuat_Unity.md) | Dùng lại logic Block Blast của 2PlayersGame; cấu trúc code; máy tự chơi để cân ải; các mốc |
| [09_CheDoKhac.md](09_CheDoKhac.md) | Đấu trường cùng hạt giống, đấu thật, boss tuần |
| [10_BanThu_1v1.md](10_BanThu_1v1.md) | **Bản thử đã chốt**: 1 tướng đấu 1 địch, bàn A và bàn C so nhau, màu là hành động, tướng từ aola, MCP, các bước |

## Đã chốt (2026-10-30)

| Câu hỏi | Người dùng chốt |
|---|---|
| Lõi | **Thử cả A (xếp khối) và C (xếp ngọc kiểu Pokiwar)** để so, rồi mới chọn |
| "Block Blast sập" | **Ô rơi sau khi xoá**, xoá dây chuyền (như 03 mục "Biến thể sập") |
| Đội hình | **Bản thử: 1 tướng, đánh solo 1 đấu 1.** Đội nhiều tướng để sau. Hệ (Ngũ hành hay 4 hệ) chưa chốt |
| Hình tướng | **Lấy các tướng đã gen trong dự án aola, chỉ dùng trong bản thử**; làm hình và chuyển động mới trước khi phát hành |
| Máy bi | **Bi chỉ kiếm bằng chơi**, không bán bi |
| Thể lực | **Không dùng** |

Còn mở: hệ Ngũ hành hay 4 hệ; máu chung hay máu riêng khi có đội; mặt sau cho tướng phe mình.

## Nguồn

- Research Pokiwar và đối thủ: artifact "Match-3 đấu pet" (29/10/2026) của người dùng.
- Trang tin về Pokiwar: [2game.vn](https://2game.vn/poki-mobile-se-la-phien-ban-game-di-dong-an-khach-cua-webgame-pokiwar-post229913.html), [download.com.vn](https://download.com.vn/pokiwar-132093) (ghi "đã ngừng phát hành"), [gamek.vn](https://gamek.vn/poki-mobile.htm).
- Máy bi: `ClashMaster/reports/Máy bi Critters và ClashMaster.md` và `ClashMaster/research_notes/Máy bi Critters và ClashMaster/`.
- Block Blast: `2PlayersGame/openspec/changes/add-block-blast-minigame/` (luật, cách chọn khối, số đo máy tự chơi).
- Game ghép xếp khối 8 × 8 với đánh nhau đã có: [Block Blast / RPG / Puzzle Fighter](https://superalv.itch.io/block-rpg) (itch.io), Spy Puzzle (App Store). Chưa tìm thấy số liệu doanh thu của chúng.
- Trọng lực sau khi xoá: [Tetris wiki, Cascade](https://tetris.wiki/Cascade).
