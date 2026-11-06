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

**Prefab:** menu `PokiClash/Prefab/Bộ UI Sa Bàn: hiệu ứng, nút sticker, chỉ khâu` (`Editor/SaBanKitMenu.cs`, chạy lại được) làm các việc sau.
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

**Bể tướng (hộp chọn đội, 2026-11-06):** hàng lọc giữa tiêu đề và khung cuộn, dựng bằng menu `PokiClash/Prefab/Hộp chọn đội: lọc theo hệ, xếp` (`Editor/TeamPickerFilterMenu.cs`).
- 7 nút tròn sticker: Tất cả, Thủy, Hỏa, Kim, Mộc, Thổ, Khắc (chỉ tướng khắc tướng chính của địch; ẩn khi không có địch).
- Nút viên xếp đổi vòng Lực chiến → Sao → Hệ.
- Tướng trong đội luôn đứng đầu và luôn hiện.
- Đổi lọc hay cách xếp thì các ô nảy ra lần lượt; lựa chọn giữ cho lần mở sau trong phiên chơi (`TeamPickerDialog`).

**Chưa đụng:** nút thả bi, thả liền, nút cược ở Máy bi. pokiwar-9a đang vẽ lại các nút đó với hoạt cảnh riêng.

**Đã kiểm trong Play:** bảng tên vùng nhún (dịch ~5 đơn vị, nghiêng ±1°), chấm đỏ thở (scale 1 → 1,12), nút Máy Bi thở, thẻ trên tay nhún. Chụp mọi màn bằng menu `PokiClash/Thử/Chụp mọi màn để soi giao diện (đang Play)`.

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
