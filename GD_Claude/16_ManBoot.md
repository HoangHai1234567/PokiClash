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

- **Prefab** `Assets/04 Prefabs/Screens/BootTitle.prefab`, dựng bằng menu `PokiClash/Prefab/Hộp thoại và màn/Màn mở game: sa bàn (BootTitle)`. Menu cũng gán `App.bootTitle` trong `App.prefab`. Chạy lại menu thì dựng lại từ đầu.
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
  - Bỏ hẳn khi thử trong Editor: menu `PokiClash/Thử/Người chơi mới/Bỏ màn mở game (Play vào thẳng sảnh)`.
- **Chụp thử:** đang Play thì chạy menu `PokiClash/Thử/Người chơi mới/Màn mở game: chụp từng nhịp (đang Play)`. Ảnh ra `Temp/PokiShots/boot_*.png`.

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
- Dựng lại bằng menu `PokiClash/Prefab/Giao diện chung/Giao diện: bàn gỗ, trang sổ, tiêu đề băng keo` (`Editor/UiRefreshMenu.cs`, chạy lại không nhân đôi).
- Chụp mọi màn để soi: đang Play thì chạy menu `PokiClash/Thử/Giao diện/Chụp mọi màn để soi giao diện (đang Play)`. Ảnh ra `Temp/PokiShots/ui/`.

## Màn tải chuyến tàu, bến tàu sảnh ↔ Nhà (2026-11-19, thay màn sa bàn)

Người dùng dặn: sảnh có bến tàu cạnh đảo Thủy, đậu một con tàu. Ấn về Nhà thì tàu đi lên, đi tới đâu mây toả ra rồi khép lại tới đó, tới bến ở mép dưới đảo Nhà; về đảo thì đi ngược lại. Màn tải là con tàu đi trên biển lên trên, tải xong thì tàu cập bến chỗ các đảo luôn (không chạm để vào).

- **Ảnh** (`ArtGen/Islands/sanh_moi/ben_tau/`):
  - bến: GPT sửa vùng góc đông nam đảo Thủy (`ben_tau_vung.txt`, `ben_tau_vung_1.png`). `ghep_ben.py` dò khớp rồi chỉ dán phần đổi (bến, thùng, đèn, chỗ bỏ hòn đá và san hô). Ra `concept_I_ben_tau.png`, `build_sanh.py` đọc ảnh này.
  - tàu: một tờ GPT ba hướng cùng một tàu (`tau_3_huong.txt`, `tau_3_huong_1.png`). `cat_tau.py` cắt ra `Assets/03 Art/Ship/tau_len|tau_xuong|tau_ngang.png`, gốc (0,5; 0,25) ở mớn nước. Script cũng ra nét sóng `tau_song_*` cắt từ tranh, bọt `tau_bot_*`, mặt biển lát `tau_bien.png` (màu biển bản đồ, vân chì −38°).
  - mây che đảo Thủy chừa vùng chỗ đậu (`AVOID` trong `build_sanh.py`): người mới chơi vẫn thấy tàu cập bến.
  - vành mây vẽ liền của bản đồ bị thay bằng biển (`open_sea` trong `build_sanh.py`, người dùng: "mây xung quanh đảo chính cứ tách riêng ra để khi đi thì nó tách luôn"). Ảnh nới thêm biển 90 px trên, 170 px dưới, nên bến khỏi sát mép.
  - Tách từng đảo (người dùng: "tách từng đảo 1 ra rồi xếp chúng lại", "drag ra rìa vẫn phải thấy mây và nước", "sao mây che luôn cả các đảo"), làm bằng `tach_dao.py`, `build_sanh.py` gọi.
    - Mỗi hệ một ảnh trong suốt (`Assets/03 Art/Islands/sanh_dao_<hệ>.png`, khoá `islands`). Ảnh giữ viền bọt ven bờ, mép bờ mềm; mép cắt giữa hai đảo chồng 2 px. Vật nhỏ trên biển theo đảo gần nhất.
    - Biển là lớp lát riêng (`sanh_bien.png`: mặt biển chuyến tàu + nét sóng), tràn 2400 ra ngoài.
    - Mây vành (237 đám, khoá `ring`) chỉ đặt trên biển, cách bờ, càng xa càng dày, có cả ngoài mép.
    - HubPan kéo được quá mép đảo 300 / 220, nên rìa luôn thấy biển và mây.
  - Theo giờ: mây vành và mây che đảo gán vào DayNight.clouds (CloudTint); biển lát là seaDark.
  - tàu đậu ở mặt nam cầu, mớn nước thấp hơn chân cọc để thân tàu đè lên mép trước cầu.
  - Bến trên (người dùng: "thêm 1 bến đỗ nữa ở phần trên các đảo"): cầu gỗ ở khe giữa đảo Hỏa và Kim chĩa lên bắc (GPT, `bo_dao/ben_tren.txt`, dán vào `bo_dao/sua_bo_dao_1.png`).
    - Đây là chỗ đậu mặc định; chuyến về Nhà và từ Nhà về đi thẳng từ đây lên mây, không vòng đảo.
    - Tàu từ màn tải cập bến dưới, người chơi tương tác ngay. Tàu tự chạy nhanh (×2,4) vòng biển phía đông, ngoài rìa đảo Thổ và Kim, lên bến trên (`PierShip.SetupDock2`, `Transfer`).
  - Nước rẽ sóng: sóng mũi 6 khung (`tau_mui_*`), bọt rẽ từ mũi trôi dọc mạn, vệt chữ V 10 khung động (`tau_vet_*`, đổi khung theo tốc độ).
  - Mây dạt ngang hai bên đường tàu, mở trước mũi, khép lại đúng chỗ (`ShipVoyage.Side`, dùng cho cả CloudRing).
  - Tàu 3D (người dùng: "làm thẳng tàu thành model 3d ... để nó xoay cho mượt"): mô hình Tripo do người dùng gen từ ảnh tàu đã duyệt (bản không nước), ở `tau3d/goc/tau.glb`.
    - `render_32.py` (Blender 5.3 chạy nền) render 32 hướng: camera trực giao nhìn chếch 42° từ phía nam, màu gốc không ánh sáng, viền mực bằng vỏ lộn ngược. Kèm vị trí gốc, mũi, đèn lồng, đường mớn nước của từng khung.
    - `hau_ky.py` cắt phần chìm dưới mép trước đường mớn nước, vẽ đường bọt, phủ vân chì nhẹ. Ra `Assets/03 Art/Ship/3d/tau_hd_*.png` và `tau_hd.json`.
    - ShipLook chọn khung theo hướng (đổi ngay, xoay nhẹ phần lệch). ShipBuild tự dùng bộ 3D nếu có, không thì dùng 3 ảnh vẽ tay cũ.
  - Nhà: camera chỉ lướt lên Nhà chính ở lần đầu tàu tới (phiên Nhà, cờ `HomeState.dockIntro`); từ lần sau tàu cập bến xong thì người chơi tự kéo.
- **Code:**
  - `App/ShipLook.cs`: hình tàu theo hướng (lên nhìn đuôi, xuống nhìn mũi, ngang nhìn hông, lật khi sang trái), bóp ngang khi quay đầu, nghiêng, nhấp nhô, bọt chữ V sau đuôi, bọt vỗ mạn khi đậu.
  - `App/Scenes/PierShip.cs`: tàu ở bến trong màn; đường ra khơi bắc / nam (Catmull-Rom), Depart / Arrive. Màn gán `Frame` (đặt camera), `Glide` (lướt camera tới tàu), `OnTap`. Ở sảnh chạm tàu là về Nhà.
  - `App/ShipVoyage.cs`: lớp phủ trên canvas riêng (thứ tự 9, dưới thanh trên; màn tải 15). Người dùng dặn chuyển cảnh "nối nhau như trong cùng 1 thế giới, không fade", nên mọi thứ nằm trên một dải thế giới dọc theo hướng đi, camera bám tàu: [ảnh chụp màn cũ] → [dải mây trên biển] → [ảnh chụp màn mới].
    - Chụp màn bằng camera UI, bỏ thanh trên, lớp tàu, giao diện cố định của màn (`SceneRoot.Chrome`) và tàu của màn.
    - Mây toả quanh tàu, lệch về trước mũi, mở nhanh (người dùng: thấy rõ thuyền, không lấp ló), khép chậm sau đuôi. Mép dải mây so le.
    - Lúc tới: ảnh màn mới đặt sau dải mây; tàu đi đường cong vào đúng hướng đường vào; camera dừng đúng lúc ảnh vào chỗ. Mây phủ mép màn mới chỉ dạt ra sau khi camera dừng, trên màn thật.
    - **Làm lại 2026-11-27** (người dùng: "nước của 3 đảo phải liền mạch nhau, move đi phải mượt … tưởng tượng 3 đảo trong 1 map to, chỉ cần follow cam theo thuyền và tách mây cho mượt"):
      - Biển chung (`App/SeaAnchor.cs`, shader `PokiClash/UISeaWorld`, `UIHomeSea._TileWorld`): mọi lớp biển (biển mở của sảnh `bien_lat`, Nhà `bien_ngoai`, Casino `bien`; biển trong ảnh nền Nhà; sóng bờ sảnh / Casino; biển chuyến tàu) vẽ cùng ảnh `sanh_bien` ô 1024, ghim theo toạ độ thế giới (biến toàn cục `_PokiSeaO`). Mỗi màn có `SeaAnchor` trên lớp kéo. Chuyến tàu ghim biển theo ảnh màn cũ, rồi dời gốc biển màn mới (`SeaAnchor.Match`) cho trùng lúc camera tới: ảnh chụp, dải biển, màn thật là một mặt nước. Vá bằng menu `PokiClash/Prefab/Sảnh và đảo/Biển chung: sảnh, Nhà, Casino` (cờ `Temp/sea_world.flag`); HomeSeaOutMenu, ShoreWaveMenu gọi lại.
      - Nạp trước, chạy sau: `Close` lướt camera tới bến, chụp màn cũ, tàu của lớp phủ đứng ở chỗ đậu; SceneRouter gỡ màn cũ, nạp màn mới lúc màn đứng yên (máy khựng lúc nạp chỉ thấy như tàu chờ ở bến). `Open` chụp màn mới rồi tàu chạy **một đường liền** từ chỗ đậu cũ tới tận chỗ đậu mới (đường ra khơi của bến cũ, đường cong Bézier qua dải mây, đường vào bến mới), hồ sơ tốc độ tính trước (êm sát bến, 1700 giữa biển). Camera trượt dọc dải bằng SmoothDamp, bù trễ để tàu nằm sau tâm màn. Đậu xong mới tắt lớp phủ, tàu của màn hiện ở chỗ đậu (`PierShip.DockedFrom`). Không còn chuyền tàu giữa màn và lớp phủ giữa đường (`Depart`, `Arrive` không dùng cho chuyến tàu).
      - Nhà: `LandView.hardEdge` (150, 150, 150, 0): rừng rìa cắt thẳng ở mép trái, phải, trên nên kéo quá tay không lộ đường cắt; mép dưới là biển chung nối dài.
    - Mây vành rời của màn (`CloudRing`) được mang sang dải đúng chỗ, đúng độ toả, lúc tới trả lại.
    - Màn tải: logo, giấy ghi có thanh tải, mẹo; tối thiểu 2,4 giây; tải xong dải mây hiện ra trước mặt, bản đồ sảnh trồi vào sau mây.
  - `App/Scenes/CloudRing.cs`: mây vành rời quanh bản đồ, trôi nhẹ, toả quanh tàu của màn (đậu: toả hẹp quanh thân).
  - `SceneRouter`: màn che chung giao diện `ISceneCover`. Sảnh ↔ Nhà và màn tải dùng `ShipVoyage.Takes`, còn lại vẫn mây hai bên (`CloudCover`).
  - `App`: tạo lớp tàu từ `App.voyagePrefab`. Mở thẳng vào sảnh thì `BeginBoot`, không còn `BootTitle`; giữ code sa bàn, có thể bỏ khi người dùng chốt. `App.Booting` gồm cả màn tải.
  - `HubPan`: kéo dư trên (thanh trên) / dưới (hàng nút đáy) để bến sát mép dưới ra khỏi hàng nút; `FrameAt` đặt ngay camera.
- **Dựng:**
  - chạy menu `PokiClash/Prefab/Sảnh và đảo/Sảnh bản đồ thế giới (mây, điểm bấm)` trước (mây che đọc lại `hub_map.json`);
  - rồi menu `PokiClash/Prefab/Sảnh và đảo/Bến tàu: tàu sảnh, chuyến tàu qua mây, màn tải`. Menu dựng `Screens/ChuyenTau.prefab`, gán vào App, đặt tàu ở bến sảnh (trên lớp mây che);
  - chạy lại menu sảnh thì phải chạy lại menu bến tàu.
- **Màn Nhà:** phiên Nhà vẽ bến ở mép dưới đảo, gọi `ShipBuild.Pier(world, dock, dockFace, south, null, scale)` và gán `Frame` / `Glide` / `OnTap`. Chưa có bến thì tàu chạy khuất khi mây tan.
- **Chụp thử:** menu `PokiClash/Thử/Đảo và sảnh/Bến tàu: sảnh → Nhà → sảnh, màn tải (đang Play)`, ảnh ra `Temp/PokiShots/ben_tau/`.

## Nước chảy và easter egg trên bản đồ sảnh (2026-11-23)

Người dùng: "các phần nước suối này vẫn hơi tĩnh, bạn học hỏi Kingdom Rush 5 … làm nước động hơn chút. Nhìn chung bố cục scene các đảo này vẫn hơi tĩnh … thêm các easter egg vào để người chơi khám phá".

- **KR5 làm nước thế nào** (dựng lại khung từ `D:\Ripper\KingdomRush5\map_viewer\scene.json`):
  - sông (`WavesRiver`): tới 225 nét bọt trắng nhỏ mỗi khung, xoay theo dòng, trôi xuôi, phình 0,42 → 0,54, hiện rồi tan trong 1,3 s, lệch pha;
  - thác (màn 1, 2, 4): tấm nước 9 khung có vệt sáng trôi xuống; chân thác có cụm bọt cuộn 20 khung và vòng gợn 16 khung toả ra;
  - đá giữa nước (`RockRipples`): vòng cung nở ra rồi mờ; mặt biển (`WaterSparks`): cụm đốm lấp lánh đổi hình mỗi 6 khung;
  - không viền mực, mép là màu đậm hơn của chính nó.
- **Thác, suối** (`ArtGen/Islands/sanh_moi/nuoc_dong.py`, shader `PokiClash/UIFlowWater`):
  - không vẽ lại thác: ảnh phủ `Islands/sanh_nuoc_<đảo>` (A = mặt nạ nước dò theo màu trong vùng `REGIONS`, ô thác `FALLS`) nằm đè đúng chỗ trên ảnh đảo, là con của gốc đảo nên nhún cùng đảo;
  - trường dòng chảy `Baked/Islands/Resources/sanh_nuoc_<đảo>_hc.png`: pha khoảng cách đi theo lòng nước từ đầu nguồn (Dijkstra), mã hoá cos / sin để lấy mẫu không gãy; B = thác;
  - shader giữ nguyên nét vẽ nền, chỉ vẽ nét bọt chồng lên: sông có dải bọt ngang dòng trôi xuôi, đứt khúc, hiện rồi tan; thác có vệt dọc trắng và lam đậm trôi xuống;
  - bản đầu cuộn chính ảnh theo hai pha làm thác nhoà, mất vệt lam sắc, nên đã bỏ;
  - vách băng đảo Kim là băng nên để yên.
- **Chân thác, mặt biển** (kiểu mới của `IslandAnim`, file `IslandAnimNuoc.cs`):
  - `splash`: múi bọt cuộn nối nhau, giữ đục rồi tan bằng co lại (mờ dần cả đời trông như bong bóng xà phòng); thay 4 bọt hình dán cũ;
  - `rings`: vòng gợn nhạt toả ra;
  - `glint`: đốm lấp lánh đổi hình.
  - Hình `anim_bot_*`, `anim_vong`, `anim_lap_*` vẽ bằng code, phẳng, viền lam, không viền mực.
- **Easter egg** (`IslandAnimTrung.cs`, chỗ đặt ở `trung_sanh/trung_sanh.py`):
  - hình sinh vật vẽ cùng nét bản đồ: `trung_sanh/to_sinh_vat_1.png` (Magnific GPT 2.6, ảnh mẫu cắt từ bản đồ), `cat_to.py` cắt ra `anim_ca`, `ca_vang`, `cua`, `ca_voi`, `duoi_ca_voi`, `voi_phun`, `chai`, `da_lua`, `rua`.
  - Cảnh sống tự chạy:
    - núi lửa phun đá dung nham mỗi 40–70 s;
    - cá nhảy rải rác;
    - cá voi nổi, phun nước, vẫy đuôi mỗi 30–45 s;
    - rùa bơi vòng;
    - lão cua thỉnh thoảng ló khỏi xác tàu;
    - 3 hải âu lượn.
  - 8 bí mật chạm vào mới lộ: núi lửa (chạm miệng núi), hải đăng (đèn quét), lão cua (bò ra bãi vẫy càng), thư trong chai (chạm xoáy nước nhả chai, chạm chai đọc thư), đàn cá san hô, cá voi (chạm lúc đang nổi), cá vàng (12 % lượt nhảy, cách nhau ít nhất 40 s), rùa lặn.
  - Lần đầu mỗi bí mật: +5 bi (cá vàng +10), báo "Bí mật bản đồ n/8". Lưu ở `SaveData.extra["hubEgg"]` (bit theo thứ tự trên).
  - Thư trong chai gợi ý các bí mật khác (7 thư).
  - Điểm chạm là Image trong suốt trên lớp phần động. `IslandAnim` nhận cú chạm nổi lên rồi tra bảng (không `AddComponent` lúc chạy, theo PrefabOnlyTests). Chạm không trúng thì chuyển tiếp lên lớp cha.
  - Sinh vật đặt trong dải biển cách bờ 18–70 px: mây vành phủ biển xa bờ, mây trong game to hơn hình elip ước lượng nên soát với elip phóng 1,35 lần.
- **Dựng lại:**
  - chạy `nuoc_dong.py` (hoặc `trung_sanh.py` khi chỉ đổi chỗ easter egg), rồi menu `PokiClash/Prefab/Sảnh và đảo/Sảnh: nước chảy (material, danh mục ảnh)`. Không phải sửa prefab: material nạp bằng `Resources.Load`;
  - `build_sanh.py` giữ phần nước và easter egg khi dựng lại bản đồ.
- **Chụp thử:**
  - menu `PokiClash/Thử/Đảo và sảnh/Sảnh: nước chảy, easter egg (chụp, đang Play)`, ảnh ra `Temp/PokiShots/nuoc/`;
  - tour phóng lớp kéo lên từng chỗ, chạm từng bí mật (núi lửa, hải đăng chạm thật qua raycast);
  - tour tự sao lưu và trả bản lưu.

## Còn có thể làm thêm

- ~~Logo đang là ảnh chụp từ chữ SVG của bản web; nên gen logo vẽ tay thật (cùng nét của game).~~ 2026-11-24: đã gen logo vẽ tay (Magnific, 3 phương án ở `ArtGen/UI/logo/`), dùng phương án 3 thay `Assets/03 Art/Boot/boot_logo.png` (cùng tỉ lệ, không sửa khung prefab).
- Hiện nét bút của mũi tên và vòng khoanh chưa khử răng cưa riêng (RenderTexture có MSAA 2x).
