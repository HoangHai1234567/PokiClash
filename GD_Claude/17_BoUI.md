# Bộ UI "Sa Bàn" (bản web thử)

Viết 2026-11-06. Người dùng muốn một bộ UI mới, làm trên web trước:
- đẹp, độc đáo;
- có hiệu ứng làm tăng độ hoàn thiện, nhưng ít và đơn giản: thở (breath), nảy khi nhấn (punch), đứng tại chỗ (idle, ví dụ thẻ bài chia ra rồi nhún tại chỗ).

**Xem:** `http://localhost:5180/uikit.html` (điện thoại cùng wifi: `http://192.168.1.22:5180/uikit.html`).
- Thanh trên cùng chọn trang: **Thành phần**, **Sảnh**, **Tướng**, **Trận**.
- Mở thẳng một trang bằng `?p=parts|hub|heroes|battle`.

## Nét chung

- Cùng nét màn mở game: mặt bàn gỗ, trang giấy kẻ ô có lề đỏ, mực nâu (#2b2118), sáp màu gạch chéo, băng keo giấy (washi), sticker viền trắng.
- **Không bóng đổ, không bóng lệch, không ánh sáng.** Tách lớp bằng viền mực.
  - Nút có dải sáp tối ở phần dưới, nằm trong viền mực, không phải bóng.
- Chữ: Baloo 2 cho tiêu đề và số (chữ trắng viền mực kiểu sticker), Pangolin cho chữ thường.
- Ảnh đảo và nền trận lấy thẳng từ Unity, giữ nguyên.

## Thành phần

| Thành phần | Hình | Hiệu ứng |
|---|---|---|
| Nút (đỏ, xanh lá, xanh dương, vàng, tím, cam, giấy; to, vừa, nhỏ, tí; tắt) | Khối sáp gạch chéo, viền mực bo lệch góc, chữ trắng viền mực; ô giá (×3) | Nhấn: lún 0,9 rồi nảy 1,12 rồi đứng; 5 gạch mực bung quanh chỗ chạm. Nút chính thở 1 → 1,045, chu kỳ 2,2 giây |
| Nút tròn | Sticker: viền giấy trắng + viền mực, lõi màu; nhãn băng keo bên dưới; chấm đỏ số | Như nút. Chấm đỏ thở nhanh. Nút giữa hàng dưới sảnh (Máy Bi) thở |
| Chip tài nguyên, vòng cấp | Viên giấy, icon to đè mép trái; vòng cấp có cung XP | Số đổi thì đếm chạy rồi nảy; chữ "+12" bay lên rồi tan |
| Thanh máu, mana, nộ, XP | Rãnh giấy, lõi sáp gạch chéo, chữ số trắng viền mực | Vạch sáp trượt chậm (thanh "sống"); mất máu thì vệt vàng lùi theo sau |
| Nhãn hệ, độ hiếm, sao | Viên sáp màu hệ có icon; chữ màu độ hiếm; sao vẽ tay | Sao hiện lần lượt, nảy từng cái |
| Khung giấy | Giấy kem hoặc kraft, viền mực, đường chỉ khâu đứt nét bên trong, băng keo giữ góc | Hiện ra: rơi xuống, nảy, đứng |
| Tiêu đề mục | Mảnh băng keo có chữ, hơi nghiêng, 4 màu | Hiện cùng mục khi cuộn tới |
| Thẻ bài | Dải màu độ hiếm, icon trong tròn giấy, tên, chữ hiệu ứng | Chia từ chồng bài (bay, xoay, lật); đứng nhún tại chỗ, mỗi lá một nhịp. Chọn: nhấc lên, viền dày, dấu tích. Chạm lần hai: bay vào ô hàng thẻ |
| Ô tướng | Dải màu hệ, chân dung sticker, tên, nhãn hệ, lực chiến, sao; tướng chưa có là bóng sẫm | Nhún nhẹ tại chỗ; chạm nảy (tướng chưa có thì lắc); dấu "!" lắc lư |
| Công tắc | Rãnh giấy, núm tròn; bật thì rãnh xanh sáp | Núm trượt có quá đà, nảy |
| Tab | Mảnh băng keo nhiều màu | Tab đang chọn nhấc lên, nghiêng, phóng nhẹ |
| Hộp thoại | Trang giấy kẻ ô, tiêu đề băng keo đè mép trên, nút X sticker | Mở: nảy từ dưới lên; con dấu đóng xuống; đóng: thu nhỏ rơi xuống |
| Giấy nhớ | Giấy vàng gạch sáp, băng keo hồng | Trượt xuống có xoay, tự đi sau 2,2 giây |
| Thanh trên | Nằm trên mặt bàn gỗ: nút quay lại sticker, tiêu đề băng keo, chip cấp và bi | |

Màn mẫu:
- **Sảnh:** đảo giữ nguyên; bảng tên vùng nhún tại chỗ; mũi tên chỉ đảo nên đánh nhún; hàng nút dưới kiểu sticker.
- **Tướng:** khung đội hình có tướng cử động (chạm để đánh); lưới ô tướng hiện lần lượt.
- **Trận:** chọn thẻ bay vào hàng 5 ô; đủ 5 thì nút "Đánh!" hiện và thở; đánh thì tướng ra đòn, địch giật, số sát thương bay lên, thanh máu lùi.

## Code

- `Web/uikit.html`, `Web/src/uikit/`:
  - `kit.css`: token màu, thành phần, keyframe thở và nhún;
  - `fx.ts`: punch, nét bung, hiện ra, chia bài, bay đi, lắc, đếm số, chữ bay;
  - `parts.ts`: các thành phần;
  - `pages.ts`: 4 trang;
  - `main.ts`.
- Nhún và thở là animation CSS trên phần tử bọc ngoài; punch chạy trên phần tử bên trong. Nhờ vậy hai hiệu ứng không giẫm lên nhau.
- Pha của mỗi phần tử ngẫu nhiên (`phase()`), nên không nhún đồng loạt.

## Unity (người dùng duyệt 2026-11-06)

**Hiệu ứng** (`Assets/01 Script/UI/Kit`):
- **`UiMotion`**: một component gom thở, nhún tại chỗ, lún khi đè, nảy khi thả, lắc, hiện ra (Pop, Drop, Up, trễ theo thứ tự anh em).
  - Nó giữ phần scale, xoay, dịch thêm của phần tử. Khi layout group hay code khác dời phần tử, gốc mới được nhận lại.
  - Đứng yên thì không ghi transform. Thời gian không theo timeScale.
  - `UiMotion.Of(x)` tự gắn nếu chưa có.
- **`SketchButton`**: đè thì lún, thả thì nảy, kèm `InkBurst` (5 gạch mực bung tại chỗ chạm, prefab `Kit/NetBung`, `UiKit.burst`). Bấm khi tắt thì lắc.
  - Nút tự vẽ hoạt cảnh riêng thì bật `noMotion`.
  - Nút tròn có lõi màu (`core`): màu vai trò tô lõi, nền giữ màu giấy làm viền trắng sticker.
- **`NumberTicker`**: số đếm chạy rồi chip nảy (số bi trên thanh trên).
- **Thẻ, ô tướng:** thẻ khi chạm thì nảy và có nét bung (`UiCard`); ô tướng chạm thì nảy (`HeroTile`).
- **Trận:** chia bài bay từ chồng bài dưới giữa lên, xoay, quá đà rồi đứng (`BattleView.Deal`). Sau đó thẻ nhún tại chỗ, mỗi lá một nhịp; thẻ được chọn thì thôi nhún.
- **Tướng:** ô tướng nhún nhẹ. Lúc vào màn thì nảy ra lần lượt từ dưới lên; làm mới sau đó thì không nảy lại (`HeroesScene`).
- **Hộp chuẩn bị:** nút Xuất trận thở khi bấm được (`StagePrepDialog`).

**Prefab:** menu `PokiClash/Prefab/Giao diện chung/Bộ UI Sa Bàn: hiệu ứng, nút sticker, chỉ khâu` (`Editor/SaBanKitMenu.cs`, chạy lại được) làm các việc sau.
- Dựng `Kit/NetBung`.
- `Kit/Nut_Tron` thành nút tròn sticker: thêm lõi `loi`. Hàng nút dưới sảnh, nút quay lại, nút đóng đổi theo.
- Đường chỉ khâu `chi_khau` (`Assets/03 Art/Kit/ui_chi_khau.png`, 9-slice lát lặp):
  - gắn vào `Kit/Khung` và khung giấy lớn trong các prefab;
  - tờ giấy hộp thoại có lớp lưới kẻ ô phủ kín, nên chỉ khâu đặt làm con của lớp lưới;
  - khung VS truyện tranh không khâu.
- Thở: nút chính của các hộp Lên cấp, Giới thiệu, Huyền thoại, Rương đảo, Chọn tướng khởi đầu; nút Đánh ở đảo; nút Máy Bi ở sảnh.
- Chấm đỏ thở nhanh: hàng nút sảnh, thẻ tướng, nút AFK.
- Bảng tên 5 vùng ở sảnh nhún tại chỗ.
- Thông báo (`Dialogs/ThongBao`) thành giấy nhớ vàng có băng keo hồng.

**Bể tướng (hộp chọn đội, 2026-11-06):** hàng lọc giữa tiêu đề và khung cuộn, dựng bằng menu `PokiClash/Prefab/Hộp thoại và màn/Hộp chọn đội: lọc theo hệ, xếp` (`Editor/TeamPickerFilterMenu.cs`).
- 7 nút tròn sticker: Tất cả, Thủy, Hỏa, Kim, Mộc, Thổ, Khắc (chỉ tướng khắc tướng chính của địch; ẩn khi không có địch).
- Nút viên xếp đổi vòng Lực chiến → Sao → Hệ.
- Tướng trong đội luôn đứng đầu và luôn hiện.
- Đổi lọc hay cách xếp thì các ô nảy ra lần lượt; lựa chọn giữ cho lần mở sau trong phiên chơi (`TeamPickerDialog`).

**Chưa đụng:** nút thả bi, thả liền, nút cược ở Máy bi. pokiwar-9a đang vẽ lại các nút đó với hoạt cảnh riêng.

**Đã kiểm trong Play:** bảng tên vùng nhún (dịch ~5 đơn vị, nghiêng ±1°), chấm đỏ thở (scale 1 → 1,12), nút Máy Bi thở, thẻ trên tay nhún. Chụp mọi màn bằng menu `PokiClash/Thử/Giao diện/Chụp mọi màn để soi giao diện (đang Play)`.

## Ghi chú chuyển từ web

- Sprite viền mực đã bỏ bóng lệch (đợt giao diện trước) dùng lại được cho nút, khung, chip.
- Cần thêm: băng keo nhiều màu, đường chỉ khâu, núm công tắc.
- Hiệu ứng thành component nhỏ dùng chung, chạy bằng thời gian không phụ thuộc timeScale:
  - `Breath`: scale theo sin;
  - `IdleBob`: dịch y + xoay, pha ngẫu nhiên;
  - `Punch`: đường cong nảy khi thả nút, gắn vào `SketchButton`;
  - `SpawnPop`: hiện ra lúc bật;
  - `Deal`: chia thẻ.
- Nét bung khi nhấn: một prefab nhỏ 5 gạch mực, tự huỷ sau 0,4 giây.

## Hàng nút đáy sảnh làm lại (2026-11-10)

Người dùng: "thiết kế lại bộ UI này, hơi xấu" (5 nút tròn trôi trên biển, nhãn chữ trắng). Nay:
- kệ gỗ (boot_ban_go xoay ngang) chạy suốt đáy màn, viền mực trên;
- 4 nút phụ là thẻ giấy ghi chú (boot_giay_ghi, 9 mảnh) nghiêng so le, băng keo màu mép trên, icon to, nhãn chữ mực trên thẻ;
- Máy Bi: nút tròn sticker phóng to, nhô lên khỏi mép bàn, vẫn thở, tên trên băng keo vàng; chấm số đỏ ở góc trên phải mỗi nút.
Dựng bằng menu `PokiClash/Prefab/Sảnh và đảo/Sảnh: hàng nút đáy (kệ gỗ, thẻ giấy)` (`Editor/HubDockMenu.cs`), chạy lại được.

Đổi thứ tự nút (người dùng 2026-11-23): từ trái sang phải là **Cửa hàng, Tướng, Máy Bi (giữa), Sổ thẻ, Nhà**.
- Bỏ Đánh tiếp và Sổ tay. Sổ tay vẫn mở bằng nút bánh răng trên thanh trên.
- Cửa hàng chưa có màn riêng: chạm thì báo "Cửa hàng: sắp có ở bản sau". Mục Gói hỗ trợ vẫn nằm trong Sổ tay.
- Nhà dời từ cột thẻ công trình xuống hàng đáy. Chưa mở thì chạm báo điều kiện mở; Nhà cần chăm thì chấm đỏ ghi "!". Con tàu ở bến vẫn đưa về Nhà.
- Cột thẻ công trình bỏ thẻ Nhà; các thẻ đang hiện dồn liền nhau từ chỗ thẻ đầu, không chừa chỗ thẻ ẩn.
- Icon `shop`, `house` trong `03 Art/Fallback/Icons` vẽ cùng nét bộ icon web (SVG 48 × 48, xuất 256 px).

## Giao diện sảnh chung: sảnh, Nhà, đảo Casino (2026-11-27)

Người dùng: "thiết kế lại để các UI này sống qua các màn home/đảo chính/đảo casino, chỉ tắt khi vào các scene bên trong thôi. ở 2 scene kia bỏ tên và nút back đi".

- Thanh trên kiểu sảnh (vòng cấp, nút AFK, bánh răng; chip bi chỉ ở đảo Casino) dùng chung cho sảnh, Nhà, đảo Casino. Hai màn kia không còn tên màn và nút quay lại.
- Sổ tay mở từ màn nào thì quay lại màn đó.
- Hàng nút đáy, cột công trình bên phải và cột ưu đãi bên trái dời từ `Screens/Hub` sang `App.prefab`:
  - nằm cùng canvas với thanh trên (Canvas thanh tren / Khung / `sanh_chung`, component `LobbyDock`);
  - cột ưu đãi `cua_hang_san` nằm trong vùng an toàn của canvas đó.
- Nhờ vậy cả cụm sống qua các màn và đứng yên khi đi tàu giữa các đảo (canvas thứ tự 10, vẽ trên lớp chuyến tàu 9). Lúc đang chuyển màn thì không nhận chạm.
- Cụm hiện khi màn dùng thanh Hud (sảnh, Nhà, đảo Casino) và tắt ở các màn bên trong (đảo hệ, trận, máy bi, Tướng, Sổ thẻ, Sổ tay, trò trên đảo Casino…).
- Ô dẫn tới màn đang đứng đổi thành **Đảo chính** (icon bản đồ, về sảnh):
  - ở Nhà là ô Nhà;
  - ở đảo Casino là nút Máy Bi giữa (Tháp Máy Bi vẫn chạm được trên đảo).
- Phím Back và con tàu ở bến vẫn về sảnh.
- Nhà:
  - chế độ thường: hàng nút riêng (Xây, Lát ô, Thu hết) bỏ kệ gỗ, các thẻ thu 0,8 xếp dọc ở mép phải ngay trên kệ chung; thẻ Ra đảo ẩn;
  - chế độ Xây / Lát ô: cụm chung ẩn (`LobbyDock.Hold`), hàng nút Nhà về đáy với kệ gỗ và thẻ Xong.
- Đảo Casino: bỏ nút Về sảnh; dòng tin và hai nút Bói sao, Lịch lữ khách đặt trên đỉnh nút Máy Bi giữa của kệ chung.
- Menu:
  - dời một lần: `PokiClash/Prefab/Sảnh và đảo/Sảnh chung: dời hàng nút, cột công trình, cột ưu đãi sang App` (`Editor/LobbyDockMenu.cs`);
  - các menu dựng hàng nút / cột (`HubDockMenu`, `HubTileMenu`, `HubBadgeMenu`, `SoPhepMenu`, `ShopMenu.BuildHub`) từ đây sửa ở `App.prefab`;
  - `HubMapMenu` không dựng lại cột công trình nữa.

## Thanh hải trình đầu màn đảo (2026-11-27)

Người dùng: "thanh này trong các đảo nhìn ổn nhưng chưa có sự ấn tượng và độc đáo, thử thiết kế sáng tạo hơn". Khung thông tin mỏng cũ (nhãn hệ, dòng cấp, độ khó, số ải, thanh rương, dòng gợi ý) đổi thành tấm bản đồ hải trình `ZoneHeader`, ít chữ:

- Trái: huy hiệu hệ to lấn ra ngoài mép tấm.
  - Vòng tiến độ màu hệ theo số ải đã qua, icon hệ ở giữa, viên mực "1/70" dưới chân.
  - Chạm vào thì hiện gợi ý hệ khắc (dòng mô tả cũ).
- Giữa: đường mòn chấm uốn lượn tới boss.
  - Quãng đã đi màu hệ, có làn sáng chạy dọc.
  - Rương mốc nằm trên đường theo tỉ lệ số ải.
  - Ghim "Lv N" của ải kế nhấp nhô đúng chỗ đang đánh.
- Phải: huy hiệu boss của đảo, gồm chân dung tướng chính ải cuối trên đĩa đỏ sẫm và băng "BOSS Lv N". Huy hiệu thở nhẹ; chinh phục xong thì đội vương miện.
- Độ khó là con dấu nghiêng đè góc huy hiệu boss.
- Dựng bằng menu `PokiClash/Prefab/Sảnh và đảo/Đảo: thanh hải trình` (`Editor/ZoneHeaderMenu.cs`).
  - Thanh mới cùng neo, cùng mép trên với khung cũ.
  - Khung cũ chỉ ẩn đi, không xoá; `ZoneScene` chưa có thanh mới thì dùng lại khung cũ.

## Thưởng bay về ô chứa (2026-11-27)

Người dùng: "từ giờ khi thu thập được cái gì thì biểu tượng của cái đấy sẽ move vào phần chứa nó".

- `App/RewardFly.cs`. Nhịp:
  - từ chỗ nhận, 3–10 icon (theo số lượng) toả ra, bật to;
  - khựng một nhịp so le;
  - bay cong về ô chứa, tăng tốc dần và nhỏ lại khi tới;
  - mỗi icon tới thì ô chứa nảy, tiếng "pick" cao dần; icon cuối tới thì rung nhẹ.
- Lớp bay là con của thanh trên, có Canvas đè thứ tự 60, nên vẽ trên cả hộp thoại.
- Ô chứa:

  | Thưởng | Ô chứa |
  |---|---|
  | Kinh nghiệm | Vòng cấp thanh trên (máy bi: thanh kinh nghiệm của máy) |
  | Bi | Chip bi; chip ẩn thì nút giữa kệ sảnh chung |
  | Mảnh tướng, đá tiến hóa, đá tinh | Ô Tướng |
  | Bản sao thẻ | Sổ thẻ |
  | Trứng, vé, quyền lợi | Cửa hàng |
  | Đá tiềm năng | Thẻ Hang Tiềm Năng |

- Không có ô chứa (màn trận, màn bên trong): icon bay về hướng chỗ ô chứa thường nằm (kinh nghiệm góc trái trên, bi góc phải trên, Cửa hàng / Tướng / Sổ thẻ chỗ các ô ở đáy) rồi mờ dần.
- Đã gắn ở:
  - hộp nhận quà `ChestDialog`, tức mọi `ChestBox`: mua gói, quà miễn phí, rương AFK, rương máy bi, rương huy hiệu;
  - nút Nhận mảnh của bảng AFK;
  - hộp rương mốc đảo;
  - bi thu ở Nhà (bay về nút giữa kệ chung).
  - hộp kết quả trận (cả Hầm đấu), lúc rời hộp; ô chứa đoán theo nội dung ô;
  - màn quà hôm nay: quà toả thành icon bay về ô chứa, thay cảnh quà bay lên góc trái cố định.
  - các trò đảo Casino: bi thắng ván và quà kèm ở lều Đêm Bài / Vòng Xoay / Máy Quả (bay từ giữa bàn), bán cá ở Bến câu và Chợ đen, món mua và đổi thẻ thừa ở Chợ đen, bi về đích (lúc rời bảng kết quả) và quà tuần ở Trường đua, quà việc ở Quán trọ; trang trí mua ở Chợ đen bay về ô Nhà.
