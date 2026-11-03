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
| [10_BanThu_1v1.md](10_BanThu_1v1.md) | Bản thử Unity xếp khối 1v1 (bàn A và C). **Đã thay bằng lõi thẻ bài từ 2026-10-31** |
| [11_BanWeb_TheBai.md](11_BanWeb_TheBai.md) | **Bản web thử theo "GDD game Pokiwar"**: trận thẻ bài luân phiên; scene kiểu Clash of Critters: đảo lớn 5 vùng hệ, mỗi hệ một đảo 8 ải; máy bi cược ×N, cấp chung, thẻ riêng, tiến hóa sao, AFK; số đo máy tự chơi; các điểm tự chọn cần duyệt |
| [12_KeHoach_OpenSpec.md](12_KeHoach_OpenSpec.md) | **Kế hoạch làm trong Unity** theo OpenSpec (`openspec/`): 11 change theo mốc, đối chiếu từng mục GDD, câu hỏi còn mở, gói ảnh cần gen (`ArtGen/`) |
| [13_DanhSachTuong.md](13_DanhSachTuong.md) | **40 tướng, 8 mỗi hệ**, chọn theo hệ gốc aola; mỗi tướng là một dòng tiến hóa (đảo Thủy đã chọn lại, các hệ khác chờ); nguồn từng dạng, tướng giữ, tướng bỏ; việc dữ liệu còn lại. Prompt hình ở `ArtGen/Heroes` |
| [14_HeThongAi.md](14_HeThongAi.md) | **Hệ thống ải mới: 70 ải, 10 tướng mỗi đảo** (ải tướng 1, 5, 10, 15, 20, rồi mỗi 10 ải; ải xen giữa: cường hóa, nhóm 2–3 con, lính không thu thập được). Bản thử đảo Thủy trên web, số đo máy tự chơi, việc chép sang Unity |
| [15_TuongKhoiDau.md](15_TuongKhoiDau.md) | **Kế hoạch chọn 1 trong 5 tướng khởi đầu** (mỗi hệ một con): chỗ lệch do khắc hệ, thứ tự đảo, 1 ô đội; 4 luật cho đảo đầu; bảng đo và tiêu chí đạt; các bước làm; câu cần chốt |

## Đã chốt (2026-10-31): đổi lõi sang thẻ bài

| Câu hỏi | Người dùng chốt |
|---|---|
| Lõi | **Thẻ bài theo "GDD game Pokiwar"** (chọn 1 trong 3, 5 lần mỗi lượt), bỏ xếp khối |
| Nhịp | **Luân phiên**: một bên chọn và đánh xong mới tới bên kia |
| Chiêu, Tuyệt kỹ | Không tốn lần chọn, chỉ tốn mana và nộ |
| Nút X máy bi | Mức cược: ×N tốn N bi mỗi lần thả, thưởng ×N |
| Làm thử | Bản web trước (`D:\PokiClash\Web`), duyệt xong mới lên plan Unity |

Mục "Tóm tắt đề xuất" bên trên và file 03–05, 07, 10 là hướng xếp khối cũ. Phần nào còn dùng được (bố cục dọc, mảnh tướng, máy bi in tỉ lệ) đã đưa vào file 11.

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
