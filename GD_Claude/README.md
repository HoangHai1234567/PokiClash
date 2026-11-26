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
| [16_ManBoot.md](16_ManBoot.md) | **Màn boot (màn mở game): 3 ý tưởng** (A sa bàn giấy pop-up, B ấn Ngũ Hành, C bìa sổ chiến thuật), đều vẽ vòng khắc; bản web thử ở `Web/src/view/boot/`, việc chuyển sang Unity |
| [17_BoUI.md](17_BoUI.md) | **Bộ UI "Sa Bàn"** (bản web thử `Web/uikit.html`): thành phần và 3 màn mẫu, hiệu ứng thở, nảy khi nhấn, nhún tại chỗ, chia bài; không bóng; việc chuyển sang Unity |
| [18_DaoVungDat_Habitat.md](18_DaoVungDat_Habitat.md) | **Kế hoạch đổi bản đồ đảo**: bỏ cuộn dọc, mỗi đảo là một vùng đất kéo hai chiều; mỗi ải tướng một habitat 3x3/4x4 đặt cố định, có animation; tách nền và habitat, chừa ô dự trữ để thêm boss; dữ liệu, code, gói ảnh, các mốc (M0–M1 làm bằng hình tạm). **Rà lại 2026-11-18 theo Clash of Critters**: vùng đất ghép mảnh như sảnh nhà của họ, nước bằng shader, tướng đồng hành chạy tới ải kế, nhuộm màu (chờ chốt); habitat theo lô tướng Thủy mới |
| [19_ClashOfCritters_VatLy_Logic.md](19_ClashOfCritters_VatLy_Logic.md) | **Vật lý và logic Clash of Critters đã đục được**: config bi, vật liệu và cách trộn, hình học bàn `table_01`, phóng bi, kết quả chọn trước rồi phát lại, flow của từng vật cản, nấm tiến độ, cược theo số bi, cây bi, phản hồi chia bậc; thang chương; đã chép vào máy mình ra sao |
| [25_FTUE.md](25_FTUE.md) | **Hướng dẫn người mới (FTUE)**: hiện trạng người mới gặp gì, nguyên tắc, lịch giới thiệu từng thứ, kịch bản từng bước (chuỗi bắt buộc A–C, gợi ý theo lúc D–H), sảnh hiện dần, trang "Cách chơi", kỹ thuật, câu đã chốt; đã làm trong Unity 2026-11-22 (lớp phủ `Kit/HuongDan`, `Core/Tutorial.cs`, tour thử) |
| [26_CuaHang_IAP_QuangCao.md](26_CuaHang_IAP_QuangCao.md) | **Cửa hàng, gói bán, ưu đãi chớp nhoáng, popup gạ mua, quảng cáo thưởng** (kế hoạch 2026-11-23): mổ shop Clash of Critters (gói bi, hộp tướng, lần đầu nạp, heo đất, chuỗi, tự chọn, thẻ tuần/tháng, quỹ, pass; không có quảng cáo thưởng); bảng giá gốc; các loại gói; Offer Engine (hàng popup lúc vào game, sau khi thua, hết bi, chớp nhoáng 2–3 giờ, nhóm người chơi, trần); 12 chỗ quảng cáo thưởng; kỹ thuật, mốc S0–S6, câu cần chốt. Đổi chốt cũ "không bán bi" |
| [27_TaiNoiDungSau.md](27_TaiNoiDungSau.md) | **Tải nội dung sau khi cài** (kế hoạch 2026-11-23): APK 167 MB, nội dung gắn theo hệ ~79 MB; bản cài ~75 MB + 5 gói fast-follow của Play Asset Delivery theo hệ (đảo + tướng cùng hệ), tải ngầm ưu tiên đảo vừa chọn; mất mạng vẫn đánh được trận đầu; mốc T0–T7 (~8–9 ngày); iOS để sau; 5 câu cần chốt |
| [29_DaoCasino.md](29_DaoCasino.md) | **Đảo Casino** (kế hoạch 2026-11-25): máy bi thành Tháp Máy Bi giữa một đảo nghỉ chân của thám hiểm gia, đi bằng tàu hoặc nút "Ra đảo" trong máy; trò cố định mở dần (Câu cá, Đua tướng, Chợ đen, Đấu trường ngầm, Quán trọ), bàn may rủi theo lịch sự kiện (Blackjack, Roulette, Slot) cược bằng bi, Hũ bàn ra mảnh tướng khách mời; kinh tế, tuổi store (mô phỏng cờ bạc), bản lưu, code, hình, mốc C0–C9, 12 câu cần chốt |
| [33_CanBangKinhTe.md](33_CanBangKinhTe.md) | **Cân bằng kinh tế sau đảo Casino** (kế hoạch 2026-11-26; **đợt 1–3 và đường EXP đã áp vào game tối 2026-11-26, bảng việc + số đo lại ở mục 0**): giả lập 300 người chơi ảo bằng lõi game (`ArtGen/KinhTe/gia_lap/`); lỗ vỡ kinh tế "bán thẻ thừa" ở Chợ đen; Hầm đấu, Câu cá, Quán trọ làm bi gấp 3,5–4 lần; trứng rương máy bi, Bỏ quảng cáo, Lọ Bi lệch; đối chiếu Clash of Critters (`research_notes/Kinh te Clash of Critters.md`); bộ số đề xuất B đã đo, 4 đợt đổi, 9 câu cần chốt |
| [34_KiemTien_KhoPhaDao.md](34_KiemTien_KhoPhaDao.md) | **Kiếm tiền và làm khó phá đảo** (kế hoạch 2026-11-26, tiếp `33`): vòng lõi thiếu cấp → cần bi → mua bi; đường EXP 9 × cấp^1,54 (người free phá đảo 33 → 55 ngày, người vừa 48 → khoảng 104 ngày, đo 90 ngày); boss mạnh hơn không có tác dụng; gói tướng theo mốc (giãn sức theo mốc, địch theo mốc, gói trọn bộ đi trước 3 mốc, thang giá, quảng cáo sức mạnh) đo được đi trước 4–10 ngày; bảng chép gói IAP Clash of Critters; 6 câu cần chốt |
| [35_Critters_KichBanGaMua.md](35_Critters_KichBanGaMua.md) | **Clash of Critters gạ mua IAP thế nào** (2026-11-26): bản đồ mọi điểm chào bán đọc từ prefab + catalog (không giải mã Lua); băng chuyền popup 3 bậc giá, popup bổ sung theo từng tài nguyên, gói theo sự kiện, thử thách người mới 4 phút, màn thua không bán; thời điểm và lịch xoay 9 ngày theo quan sát công khai; so với Offer Engine của mình; 9 việc nên chép, 5 thứ không chép; kịch bản đề xuất cho người chơi mới |
| [21_Nha_Home.md](21_Nha_Home.md) | **Nhà (Home) thay Trang trại** (kế hoạch 2026-11-18): đảo giáp biển lưới thoi, học phần nhà của Clash of Critters; công trình (ruộng, vườn, xưởng gỗ, ao cá, mỏ, lò rèn, bếp, tưới tiêu, suối nước nóng, cây bi), cấp Nhà chính, ô rừng mở theo cấp người chơi và cấp nhà, thẻ chỉ định tướng, trang trí và điểm đẹp, bản lưu v13, mốc H0–H6, 6 câu cần chốt |

## Simulation

[simulation/README.md](simulation/README.md): nhật ký các vòng giả lập kinh tế 300 người chơi ảo (2026-11-26, 2026-11-27): từng vòng hỏi
gì, đo được gì, chốt gì; kinh nghiệm khi chạy; bài học về kinh tế game; giới hạn của giả lập; hướng cải thiện máy giả lập và game. Đọc
trước khi chạy vòng tiếp theo. Kế hoạch gốc ở `33`, `34`, `35`.

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
