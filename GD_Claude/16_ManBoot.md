# Màn boot (màn mở game): 3 ý tưởng, bản web thử

Viết 2026-11-06. Người dùng muốn màn mở game **đẹp, độc đáo, lạ mắt, hợp dòng chiến thuật**, làm bản web trước.

**Người dùng chốt (2026-11-06): ý tưởng A "Sa bàn giấy"**, làm trong Unity (mục cuối).

## Tiêu chí và cách giải

- **Hợp chiến thuật:** cả 3 ý đều vẽ **vòng khắc Ngũ Hành** (Thủy → Hỏa → Kim → Mộc → Thổ → Thủy).
  - Đây là luật chiến thuật lõi của game (đánh hệ mình khắc ×1,5).
  - Đó cũng là thứ tự đảo, nên mũi tên vẽ theo đúng đường người chơi sẽ đi.
  - Vẽ nối 5 đỉnh theo thứ tự đó thì ra ngôi sao năm cánh, dùng làm mô-típ chung.
- **Độc đáo:** giữ chất "sổ tay phiêu lưu" của cả game (giấy kẻ ô, nét mực rung, sáp màu, băng keo, sticker viền trắng). Mỗi ý có một chiêu riêng: sách pop-up, vòng ấn tự vẽ, bìa sổ lật mở.
- **Có sức sống:** 5 tướng khởi đầu cử động thật bằng clip aola: đứng, bị khắc thì trúng đòn, chạm vào game thì cùng ra đòn.
  - Bu Lông, Nụ Hoa, Giọt Sương, Sư Tử Lửa, Thạch Nhân (`15_TuongKhoiDau.md`).
- **Theo luật UI:**
  - không bóng đổ, không bóng lệch cứng, không bóng dưới chân (bóng aola dưới chân tướng bị bỏ khi vẽ);
  - lớp tách nhau bằng viền mực.
- **Thông tin có ích lúc chờ:** thanh tải tô 5 màu hệ, bút chì chạy theo, kèm mẹo luật thật (vòng khắc, ×1,5, chọn 1 trong 3 thẻ…).

## 3 ý tưởng

| | A · Sa bàn giấy (đề xuất) | B · Ấn Ngũ Hành | C · Bìa sổ chiến thuật |
|---|---|---|---|
| Hình | Bản đồ đảo (`Islands/world.png`) đặt nghiêng trên bàn gỗ như sa bàn; thẻ úp và bút chì cạnh bên | Trang sổ lề đỏ; vòng ấn tròn, chữ "THỦY KHẮC HỎA ✦ …" chạy quanh; 5 tướng đứng trên bệ đá ở 5 đỉnh | Bìa kraft, gáy vải, dây chun; nhãn tên có logo, "SỔ TAY CHIẾN THUẬT", "Chủ sổ: Bạn"; 5 sticker tướng; dấu đỏ "TUYỆT MẬT" |
| Cảnh mở (~4,3 giây) | Tấm bản đồ trượt vào, đảo được tô dần; tướng và cờ hệ **bật dựng lên như sách pop-up** ở đảo cùng hệ; mũi tên kế hoạch đứt nét vẽ theo vòng khắc; khoanh "Xuất phát!" quanh đảo Thủy; logo gấp bật lên | Bút mực vẽ vòng tròn; bệ rơi xuống, tướng dán "bộp"; mũi tên khắc vẽ thành ngôi sao, tướng bị khắc giật mình; dấu kiếm chéo ở tâm, logo đóng dấu | Sổ đặt xuống bàn; nhãn, sticker dán lần lượt; bút bi vẽ vòng khắc, ghi chú "khắc!", "×1,5"; viết tên chủ sổ; đóng dấu TUYỆT MẬT |
| Lúc chờ chạm | Mũi tên chạy nét, cờ bay, tướng thở | Vòng chữ xoay chậm, vệt dạ quang chạy theo vòng khắc | Tướng trên sticker cử động, dây chun rung |
| Chạm để vào | Tướng ra đòn, camera lao vào đảo Thủy, mây khép mở ra sảnh | Tướng ra đòn, vòng ấn xoay một nhịp, mây ra sảnh | Dây chun bật ra, bìa lật mở: **trang đầu chính là sảnh** |
| Mạnh | Đọc ra "chiến thuật" ngay (sa bàn, mũi tên tác chiến); khoe thế giới thật của game; nối liền sang sảnh (sảnh cũng là bản đồ đảo) | Gọn, dễ nhớ, làm được biểu tượng game và icon; dạy luật khắc ngay từ màn đầu; làm Unity dễ nhất (toàn 2D) | Duyên nhất, hợp tên "Sổ Tay Phiêu Lưu"; lật bìa vào sảnh rất "đã" |
| Yếu | 3D giả bằng nghiêng mặt phẳng, máy yếu phải thử; tướng ở xa hơi nhỏ | Ít "thế giới", nặng về sơ đồ | Nhiều chi tiết, hơi rối; ý chiến thuật nằm ở chữ và ghi chú nhiều hơn |

**Đề xuất:** A làm màn chính. Có thể lấy vòng chữ của B làm viền logo, hoặc làm icon game.

## Bản web

- Code: `Web/src/view/boot/`.
  - `boot.ts`: điều khiển, nạp trước, chọn ý tưởng.
  - `common.ts`: tướng cử động, logo, thanh tải, vân gỗ.
  - `sceneTable.ts` (A), `sceneSeal.ts` (B), `sceneCover.ts` (C), `boot.css`.
- Mở `http://localhost:5180/` là chạy màn boot rồi vào sảnh. Hộp giới thiệu lần đầu chờ boot xong mới hiện.
  - Thanh "Ý tưởng" trên cùng đổi qua lại A / B / C và diễn lại. Trình duyệt nhớ lựa chọn.
  - `?boot=a|b|c`: chọn ý tưởng (xem được cả khi mở thẳng scene khác).
  - `?skipboot` hoặc `?skipintro`: bỏ màn boot.
- Ảnh dùng chung với Unity, không chép sang web: máy chủ dev phục vụ `/unity/*` từ `Assets/03 Art` (đảo `Islands/world.png`, bệ `Islands/be_<hệ>.png`).
- Logo "PokiClash" vẽ bằng chữ SVG (Baloo 2), viền trắng mép xé như sticker tướng. Chữ CLASH tô 5 màu hệ theo vòng khắc. Đây là logo tạm, chờ người dùng chốt hình logo.

## Unity (ý tưởng A, làm 2026-11-06)

- **Prefab** `Assets/04 Prefabs/Screens/BootTitle.prefab`, dựng bằng menu `PokiClash/Prefab/Màn mở game: sa bàn (BootTitle)`. Menu cũng gán `App.bootTitle` trong `App.prefab`. Chạy lại menu thì dựng lại từ đầu.
- **Code:**
  - `App/BootTitle.cs`: diễn cảnh, camera sa bàn, tướng, chạm;
  - `UI/Kit/InkPath.cs`: nét mực vẽ dần, liền hoặc đứt, đầu tròn (mũi tên, vòng khoanh);
  - `Editor/BootTitleMenu.cs`: dựng prefab; toạ độ chép từ `sceneTable.ts`, nhân 2.
- **Ảnh** `Assets/03 Art/Boot/boot_*` xuất từ bản web bằng `node Web/scripts/export_boot_art.mjs` (cần dev server).
  - Gồm logo, tấm bản đồ (giấy kẻ ô, biển, băng keo, la bàn), mặt bàn gỗ, thẻ úp, bút chì, cờ 5 hệ, thanh tải, giấy ghi chú, băng keo chữ, đế tướng.
  - Đảo dùng lại `Islands/world.png` của sảnh, không tốn thêm dung lượng build.
- **Sa bàn 3D:** canvas thế giới đặt xa (x = −20000), một camera phối cảnh riêng render ra RenderTexture, RawImage trên canvas màn boot hiện ảnh đó.
  - Khung chiếu lệch tâm tính từ "mắt" (perspective 980, perspective-origin 270 × 60 của CSS) và vùng ảnh, nên ảnh khớp đúng chỗ như bản web.
  - Tướng là AolaSticker gắn vào tấm dựng, bật từ nằm phẳng lên đứng bằng cách quay trục X. Không vẽ bóng dưới chân (`AolaSticker.HideShadow`).
- **Thứ tự lớp:** canvas màn boot sortingOrder 15, trên thanh trên (10), dưới canvas phủ có mây và hộp thoại (20).
  - Mây che lúc sảnh đang nạp; mây mở thì cảnh mới diễn. Chạm thì camera lao vào đảo Thủy, mây khép, màn tắt, mây mở ra sảnh.
- **Khi nào hiện:** game chạy thẳng vào sảnh. Không hiện khi bấm Play ở scene khác trong Editor.
  - Scene nào được mở sau lần vào sảnh đầu tiên (tour thử gọi `Router.Go`) thì màn tự tắt.
  - Hộp giới thiệu và chọn tướng khởi đầu chờ màn tắt mới hiện (`App.Booting`). Nút Back không làm gì khi màn đang hiện.
  - Bỏ hẳn khi thử trong Editor: menu `PokiClash/Thử/Bỏ màn mở game (Play vào thẳng sảnh)`.
- **Chụp thử:** đang Play thì chạy menu `PokiClash/Thử/Màn mở game: chụp từng nhịp (đang Play)`. Ảnh ra `Temp/PokiShots/boot_*.png`.

## Giao diện các màn theo nét màn mở game (2026-11-06)

Người dùng dặn: cải thiện giao diện các màn, giữ nguyên ảnh đảo. Đợt 1 áp chung cho mọi màn; sảnh, đảo và sàn đấu không đổi:

- **Bỏ bóng lệch cứng** (luật UI không vẽ bóng). 8 sprite giấy/mực dùng chung trong `Assets/03 Art/Baked/Sketch` được dựng lại với viền mực đều, giữ nét rung vẽ tay. Mọi khung, thẻ, nút, chip trong game hết dải bóng ở cạnh phải/dưới.
  - Các sprite: `sk_Panel`, `sk_PanelThin`, `sk_Button`, `sk_ButtonPressed`, `sk_CardFrame`, `sk_Round`, `sk_RoundPressed`, `sk_Pill`.
  - Bản "nhấn" tô tối hơn. Nút nhấn thì co 4% và chữ lún 3 px (`SketchButton`), thay cho kiểu "thân dịch theo bóng" cũ.
- **Màn con là trang sổ đặt trên bàn gỗ.** Nền là mặt bàn gỗ của màn mở game (`boot_ban_go`).
  - Tướng, Sổ thẻ, Sổ tay, Đền Huy Hiệu, Hang, Trang trại: thêm trang giấy kẻ ô có viền mực và lề đỏ hai nét, nằm ngay dưới thanh trên (`An toan/Khung/trang`).
  - Máy bi: máy đứng thẳng trên bàn gỗ.
  - Nền cũ chỉ bị tắt, không xoá.
- **Thanh trên:** ô tên màn thành mảnh băng keo giấy hơi nghiêng (`Assets/03 Art/Kit/ui_bang_keo_ten.png`, 9-slice ngang).
- Dựng lại bằng menu `PokiClash/Prefab/Giao diện: bàn gỗ, trang sổ, tiêu đề băng keo` (`Editor/UiRefreshMenu.cs`, chạy lại không nhân đôi).
- Chụp mọi màn để soi: đang Play thì chạy menu `PokiClash/Thử/Chụp mọi màn để soi giao diện (đang Play)`. Ảnh ra `Temp/PokiShots/ui/`.

## Còn có thể làm thêm

- Logo đang là ảnh chụp từ chữ SVG của bản web; nên gen logo vẽ tay thật (cùng nét của game).
- Hiện nét bút của mũi tên và vòng khoanh chưa khử răng cưa riêng (RenderTexture có MSAA 2x).
