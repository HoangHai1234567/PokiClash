# 27. Tải nội dung sau khi cài: Play Asset Delivery + tải ngầm (kế hoạch 2026-11-23)

Người dùng hỏi 2026-11-23: "nghiên cứu cách làm có thể đẩy bớt asset kiểu addressable lên cloud được không?", rồi chốt: kết hợp
(1) gói tải sau của Google Play (fast-follow) và (2) tải ngầm hết trong phiên chơi đầu.

## Tóm tắt

- **Vì sao:** APK Android 167 MB (bản build 2026-11-23 13:50, đã nén LZ4HC), ngân sách người dùng đặt từ 2026-11-03 là 60–70 MB. Phần nội dung gắn
  với từng hệ (tướng cùng hệ, nền đảo, nền trận, nhạc đảo) chiếm khoảng 79 MB trong APK.
- **Không giữ sẵn đảo nào:** người chơi chọn đảo đầu qua tướng khởi đầu (`25_FTUE.md` A3–A6: "Đảo {hệ} là nhà mình") và cả 5 đảo mở từ đầu.
  Bản cài chứa phần dùng chung và đủ để đánh trận đầu của bất kỳ đảo nào; nội dung từng hệ nằm trong 5 gói tải sau.
- **Android:** 5 gói kiểu **fast-follow** của Play Asset Delivery: Google Play tự tải ngay sau khi cài, không tính vào dung lượng hiện trên
  Store, Google giữ hộ (không cần máy chủ). Trong game, gói nào chưa xong thì xin tải ngay, gói của đảo vừa chọn đi trước.
- **Mạng:** cần mạng một lần cho mỗi gói. Tải xong thì chơi offline như bây giờ. Mất mạng ngay sau khi cài vẫn chọn tướng, đánh trận đầu, vào
  Nhà, máy bi được.
- **Kết quả ước:** bản cài khoảng 75 MB (gồm tách atlas hạt theo hệ), mỗi gói 14–23 MB. Bản APK thử gửi tester vẫn là bản đủ, như bây giờ.
- **Công:** khoảng 8–9 ngày, 8 mốc (mục 6). Phần khó nhất là đổi đường nạp ảnh đảo và hình tướng từ trỏ thẳng sang nạp theo gói.
- **iOS** để sau (mục 8). 5 câu cần chốt ở mục 9, câu nào cũng có đề xuất.

## 1. Hiện trạng (đo 2026-11-23)

### 1.1. Dung lượng theo hệ

Đọc thẳng APK 167 MB (bảng khối của `data.unity3d`, cộng phần đã nén của từng ảnh và đối tượng). MB đã nén, không phải MB trước nén: atlas
tướng và atlas hạt có nhiều vùng trong suốt nên LZ4HC nén được khoảng 40%.

| | Thủy | Hỏa | Kim | Mộc | Thổ |
|---|---|---|---|---|---|
| Tướng cùng hệ (atlas, khoá + lưới, chân dung) | 4,3 | 6,1 | 6,2 | 5,4 | 5,5 |
| Nền đảo, nền trận | 15,4 | 10,1 | 4,8 | 10,8 | 5,1 |
| Nhạc đảo | 0,9 | 1,1 | 1,0 | 1,1 | 1,3 |

Thủy nặng nhất vì đã có 16 nền trận riêng. Phần dùng chung lớn nhất: atlas hạt hiệu ứng 17,4 MB (một atlas cho mọi hệ), máy bi 5,9 MB, bản
đồ thế giới 3,9 MB, Nhà 3,7 MB, code khoảng 25 MB.

### 1.2. Chia theo hệ có sạch không

Có. Mỗi đảo chỉ dùng tướng và lính cùng hệ làm địch (đếm `stages.json`: 59–61 lượt tướng cùng hệ và 66 lượt lính cùng hệ mỗi đảo, không có
hệ khác). Mảnh rơi ở đảo Thủy có 1 Thổ, 1 Mộc: chỉ là dữ liệu, không cần hình tướng lúc rơi. Ngoại lệ là rương cửa hàng (`26_CuaHang_IAP_QuangCao.md`):
rương ra được tướng mọi hệ.

### 1.3. Cách nạp hiện tại

Gần như mọi ảnh lớn được trỏ thẳng từ prefab App trong scene Boot, nên nằm chung gói của scene đầu (`sharedassets0`). Nhiều khả năng chúng được
nạp vào RAM ngay lúc mở game (chưa đo bằng Memory Profiler):

- `ArtLibrary` (`App/ArtLibrary.cs`): danh sách tên → Sprite của mọi ảnh gen (nền đảo, nền trận, bệ…). Code gọi `App.Art.Get(tên)` khoảng
  90 chỗ, đồng bộ.
- `UiAssets.heroes` → `HeroModels` → prefab tướng `AolaActor` → `forms` (`AolaAnim`) → `atomik` (`AtomikAsset`) → atlas. Danh mục tướng được
  dùng khoảng 26 chỗ.
- `Resources.Load`: atlas và chân dung dạng aola (`AolaAnim.LoadAtlas`, `LoadPortrait`), mặt tướng `HeroFaces/mat_<dạng>` (`HeroArt`), ảnh
  riêng của vài tướng (`HatHon`, `HatSat`, `HatXich` nạp `<dạng>/<khoá>`), nền và dấu VS của màn mở trận.
- Atlas hạt `Fx/hat.spriteatlasv2` gom mọi ảnh trong `Fx/Hat`, `HatLua` nhận mảng Sprite chung.
- Nhạc: `AudioService` lấy clip từ danh sách trong `BakedArt`.

Game chưa gọi mạng chỗ nào (không có `UnityWebRequest`; quảng cáo mới đếm lượt tại máy).

## 2. Cách làm đã chốt

- **Addressables** (gói `com.unity.addressables`) làm lớp nạp theo địa chỉ, cộng **Addressables for Android** (`com.unity.addressables.android`)
  để gắn kiểu tải của Play Asset Delivery vào từng nhóm. Mặc định mỗi nhóm Addressables thành một asset pack của Google.
- Nhóm nền (bản cài) kiểu **Install Time**, 5 nhóm theo hệ kiểu **Fast Follow**.
- Phát hành bằng **AAB** qua Google Play. Giới hạn hiện hành của Play: mỗi asset pack tối đa 1,5 GB, tổng các gói fast-follow và on-demand 4 GB,
  tối đa 100 gói (theo trang trợ giúp Play Console). Mình dùng 5 gói nhỏ, còn rất xa giới hạn.
- Tải ngầm trong game: gói nào chưa có thì xin tải ngay, đảo vừa chọn ưu tiên trước.

## 3. Chia nội dung

### 3.1. Bản cài (Install Time, nằm trong APK/AAB)

- Code, scene, giao diện, phông, cốt truyện, sảnh (bản đồ thế giới, ảnh 5 đảo trên sảnh `sanh_dao_*`, nước sảnh `sanh_nuoc_*`), Nhà, máy bi,
  cửa hàng.
- **5 dòng tướng khởi đầu** đủ các dạng tiến hóa (`heroes.json` khoá `starters`: ti_tach, su_tu_lua, bo_cap, tien_la, thach_nhan) cùng
  hiệu ứng của chúng.
- **Chân dung và mặt của mọi tướng** (câu 1 mục 9): để bộ sưu tập, kết quả rương, hộp chi tiết hiện ngay khi offline.
- **Nền trận ải đầu của mỗi đảo** (ải `GameData.StarterStage` của từng tướng khởi đầu, mỗi cái khoảng 0,4–0,7 MB).
- Atlas hạt chung (sau khi tách, mục 6 mốc T4), nhạc chung (sảnh, trận, boss, máy bi, chủ đề).

### 3.2. Gói tải sau theo hệ (Fast Follow), 5 gói `noi_dung_<hệ>`

Mỗi gói gồm:

- **Đảo:** `land_<hệ>*` (ảnh đất, biển, mây), `zone_<hệ>`, `land_<hệ>_dist`, `land_<hệ>_vung`, ghi chú bút chì `Islands/Co/*_<hệ>*`, bệ ải
  `be_<hệ>*`, atlas hình rời `dao_hinh_roi_<hệ>`.
- **Nền trận** `battle_<hệ>_*`, trừ nền ải đầu.
- **Tướng và lính cùng hệ**, trừ dòng khởi đầu: asset dạng (`AolaAnim`, `.atomik`, atlas, dữ liệu animation) và ảnh riêng của tướng.
- **Hiệu ứng hạt của hệ** (atlas `hat_<hệ>` sau khi tách).
- **Nhạc đảo** `bgm_dao_<hệ>`.

Ước mỗi gói 14–23 MB (bảng 1.1 cộng phần hạt của hệ).

## 4. Luồng người chơi

1. **Cài từ Play Store:** tải bản cài khoảng 75 MB; Play tự tải tiếp 5 gói fast-follow ngay sau đó, kể cả trước khi mở game.
2. **Mở game lần đầu:** game hỏi trạng thái 5 gói. Gói nào chưa xong thì xin tải; hàng chờ theo thứ tự đảo (`zones.json` `order`).
3. **Chọn tướng (A5):** đẩy gói cùng hệ lên đầu hàng chờ. Đoạn cốt truyện và chọn tướng thường lâu hơn thời gian tải một gói 14–23 MB qua 4G.
4. **Chạm đảo (A7):**
   - gói đã xong: vào đảo như bây giờ;
   - đang tải: màn chờ có thanh tiến độ và số MB còn lại;
   - không có mạng: đánh **trận đầu thẳng từ sảnh** (ải 1 là "bóng của chính mình", đối thủ là tướng khởi đầu, nền trận ải đầu có sẵn), xong
     về sảnh và báo "Cần mạng để tải đảo {hệ} lần đầu (~N MB)" (câu 3 mục 9).
5. **Ở sảnh:** đảo chưa tải có dấu nhỏ (mây hoặc vòng tiến độ); chạm vào thì như bước 4.
6. **Rương ra tướng của gói chưa tải:** hiện chân dung ngay (có trong bản cài); hoạt ảnh tướng chờ gói xong. Mở xem tướng đó thì xin tải gói
   trước.
7. **Sau khi đủ 5 gói:** game chạy offline hoàn toàn. Gói được cài theo app; bản cập nhật Store mang gói mới.

Mất mạng ngay sau khi cài vẫn làm được: chọn tướng, trận đầu, Nhà, máy bi, cửa hàng (trừ thanh toán), xem tướng bằng chân dung.

## 5. Đổi gì trong code

- **Dịch vụ gói** (`App/ContentPacks.cs`, mới): trạng thái 5 gói, hàng chờ ưu tiên, `Prepare(hệ)` (bất đồng bộ, có tiến độ), nạp và trả asset theo địa chỉ.
  Trong Editor và bản APK đủ thì luôn sẵn sàng ngay, nên luồng làm việc hằng ngày không đổi (Addressables chế độ "Use Asset Database").
- **`ArtLibrary`:** chia mục bản cài và mục theo gói. Mục theo gói lưu địa chỉ thay vì Sprite. `App.Art.Get(tên)` giữ nguyên chữ ký, trả từ
  bộ nhớ đệm sau khi `Prepare(hệ)`. Các màn đảo (`ZoneScene`, `LandView`, `IslandAnim*`) và màn trận gọi `Prepare` trước khi dựng. Menu
  `PokiClash/Nhập ảnh` ghi thêm nhóm Addressables cho từng ảnh.
- **Tướng:** `HeroModels` trỏ prefab dòng khởi đầu như cũ; tướng khác trỏ bằng địa chỉ (`AssetReference`). Hộp Chuẩn bị chờ hình hai đội
  trước khi Xuất trận; hộp chi tiết tướng và mở rương chờ dạng cần hiện. Thư mục dạng trong `Heroes/Resources/<dạng>/` chuyển ra
  `Heroes/<dạng>/` (Addressables không lấy được nội dung trong `Resources`), sửa đường dẫn ở `AolaImport`, `AtomikForms`, `AolaAnim`,
  `BuildExclude`, và các chỗ `Resources.Load` ảnh riêng của tướng (`HatHon`, `HatSat`, `HatXich`). Chân dung và mặt tướng sang nhóm bản cài.
- **Atlas hạt:** tách `hat.spriteatlasv2` thành `hat_chung` và `hat_<hệ>` theo hiệu ứng mỗi hệ dùng (bảng `HatLua.Fbs` và các file `HatFb<hệ>`,
  `HatNuoc`, `HatLua`…); tên sprite giữ nguyên. `HatLua` nhận sprite từ các atlas đã nạp.
- **Nhạc:** clip `bgm_dao_<hệ>` sang gói; `AudioService` hỏi `ContentPacks`, gói chưa có thì phát nhạc sảnh.
- **Build** (`Editor/Build/PokiBuild.cs`): build nội dung Addressables trước khi build game.
  - `Android thử (APK)`: **bản đủ**, mọi nhóm nằm trong APK. Tester cài tay vẫn chơi đủ, không cần mạng.
  - `Android phát hành (AAB)`: bản cài + 5 gói fast-follow.
  - Thêm `Android thử tải sau`: build AAB rồi cài lên máy bằng `bundletool --local-testing` để thử luồng tải trên máy thật.
  - `BuildSizeReport` ghi cỡ bản cài và cỡ từng gói. `BuildExclude` làm việc với đường dẫn mới.
- **Gỡ lỗi:** thêm tuỳ chọn SRDebugger "giả lập gói chưa tải / mất mạng" để thử luồng ở bước 4–6 ngay trong Editor.

## 6. Mốc

| Mốc | Việc | Công | Kiểm |
|---|---|---|---|
| T0 | Thêm Addressables, Addressables for Android; menu `PokiClash/Tải sau/Xem trước gói` liệt kê asset và cỡ từng gói | 0,5 ngày | Bảng gói khớp mục 3; không asset bản cài nào phụ thuộc asset trong gói |
| T1 | `ContentPacks` (trạng thái, hàng chờ, `Prepare`), chế độ bản đủ | 1 ngày | Test EditMode: bản đủ luôn sẵn sàng; hàng chờ đổi ưu tiên đúng |
| T2 | Ảnh đảo, nền trận, nhạc đảo qua `ContentPacks` | 1,5 ngày | Tour 5 đảo và trận mỗi hệ trong Editor: không ảnh trống, không nháy |
| T3 | Tướng qua `ContentPacks`; dời thư mục dạng ra khỏi `Resources` | 2 ngày | Test so hình (`AtomikKeysTests`, chụp thử dạng .atomik); trận, chi tiết tướng, mở rương mọi hệ |
| T4 | Tách atlas hạt theo hệ | 0,5–1 ngày | Soát atlas hạt (menu có sẵn); chụp chiêu mỗi hệ |
| T5 | Nhóm Play Asset Delivery, build AAB, APK bản đủ, báo cáo cỡ gói | 1 ngày | AAB: bản cài ~75 MB, 5 gói 14–23 MB; APK đủ chạy như cũ |
| T6 | Hàng tải theo đảo đã chọn, dấu trên sảnh, màn chờ, báo mất mạng, trận đầu từ sảnh, luồng rương | 1 ngày | Tour "giả lập chưa tải" và "mất mạng" bước 1–6 mục 4 |
| T7 | Thử trên máy: `bundletool --local-testing` (có bật chế độ máy bay), rồi kênh thử nội bộ của Play Console; đo RAM lúc mở game trước/sau | 1 ngày | Mục 7 |

Tổng khoảng 8–9 ngày. T1–T4 làm được mà chưa cần tài khoản Play; T7 cần kênh thử nội bộ (mục 8).

## 7. Đạt khi

- Bản cài trên Play khoảng 75 MB; mỗi gói 14–23 MB.
- Cài xong có mạng: không chờ gì trước trận đầu; vào đảo đã chọn hầu như không phải chờ.
- Bật chế độ máy bay ngay sau khi cài: chọn tướng, trận đầu, Nhà, máy bi vẫn chạy; chạm đảo chưa tải thì có thông báo rõ, không treo.
- Đủ 5 gói: tắt mạng vẫn chơi mọi đảo.
- APK thử (bản đủ) chạy như bây giờ.
- RAM lúc mở game giảm (đo bằng Memory Profiler trên máy thật, ghi số vào tài liệu này).

## 8. Rủi ro, điều kiện

- **Đổi đồng bộ sang bất đồng bộ** ở đường nạp ảnh và tướng dễ gây ảnh trống hoặc nháy; phải nạp trước ở các mốc chuyển màn (vào đảo, Chuẩn
  bị, mở rương). Đây là lý do T2, T3 chiếm nhiều công nhất.
- **Play Asset Delivery chỉ chạy khi cài từ Play** (hoặc `bundletool --local-testing`). APK cài tay không có gói tải sau, vì vậy APK thử luôn
  là bản đủ.
- **Diễn đàn Unity báo** `Addressables.GetDownloadSizeAsync` trả 0 với gói Play Asset Delivery (Unity 6000.0, Addressables 2.2.2, Addressables
  for Android 1.0.4); chính người hỏi về sau thấy lỗi do cách họ dựng. Lấy trạng thái và cỡ gói qua API của Play cho chắc.
- **Phát hành AAB cần** keystore thật và mã ứng dụng riêng: `PokiBuild` đang cảnh báo khoá debug và mã template `com.unity.template`. Kênh thử
  nội bộ cần hai thứ này.
- **Thêm tướng, đảo mới** đi theo bản cập nhật Store (Play Asset Delivery không đẩy nội dung ngoài bản cập nhật). Muốn đẩy nội dung không qua
  Store thì chuyển các nhóm sang tải từ CDN (cùng Addressables).
- **iOS (để sau):** cùng các nhóm Addressables, đổi nơi tải sang CDN (Unity Cloud Content Delivery: 50 GB/tháng miễn phí, sau đó 0,08 USD/GB;
  hoặc Cloudflare R2: không tính phí tải về, lưu 0,015 USD/GB/tháng) hoặc On-Demand Resources của Apple.
- **Nhiều phiên làm song song:** T3 dời thư mục `Heroes/Resources` và đụng công cụ nhập tướng; phải báo các phiên đang làm tướng trước khi làm.

## 9. Cần chốt

1. **Chân dung và mặt mọi tướng giữ trong bản cài** (khoảng 5 MB đã nén) để bộ sưu tập và rương hiện ngay khi offline. Đề xuất: giữ.
2. **Gói theo hệ** (đảo + tướng cùng hệ trong một gói, 5 gói). Phương án khác: tách gói tướng riêng (10 gói). Đề xuất: 5 gói, vì mỗi đảo chỉ
   dùng tướng cùng hệ.
3. **Mất mạng ở bước chạm đảo lần đầu:** đánh trận đầu thẳng từ sảnh rồi báo cần mạng. Đề xuất: làm.
4. **Tách atlas hạt theo hệ ngay đợt này** (bản cài bớt thêm khoảng 14 MB). Đề xuất: làm.
5. **iOS** làm sau, khi đó chọn CDN hay On-Demand Resources. Đề xuất: để sau.

## 10. Đã làm (2026-11-23, người dùng đồng ý cả 5 đề xuất mục 9)

- **Gói:** `com.unity.addressables` 2.11.2, `com.unity.addressables.android` 1.1.1.
- **Lớp nạp:** `Game/Content/ContentPacks.cs`.
  - Hàng chờ một gói một lúc; `Request(hệ, first)` đẩy gói lên đầu.
  - Nạp cả gói theo nhãn `pack_<hệ>`, sau đó `Get<T>(tên)` trả asset.
  - `Prefetch` xin Play tải trước mọi gói, không nạp vào RAM.
  - Bộ nạp bundle của Addressables for Android tự xin Play tải gói fast-follow chưa có. `ContentPacks` chỉ lấy thêm tiến độ.
  - `App.Update` gọi `Tick` mỗi khung (không tự sinh GameObject, theo luật `PrefabOnlyTests`).
- **Chặn chuyển màn:** `App/ContentGate.cs` cộng một đoạn trong `SceneRouter.Run`.
  - Vào đảo cần gói của đảo; vào trận cần gói đảo của ải và gói của tướng trong đội.
  - Gói lỗi thì ở lại màn cũ, báo "Cần mạng để tải {đảo} lần đầu…".
- **Tướng:** `AolaActor` có `formKeys` và `pack`. Tướng ngoài 5 dòng khởi đầu không trỏ thẳng dạng; `Form(i)` lấy từ gói.
  - `Ready`, `Prewarm`, `LoadForm` tự xin nạp gói; trong lúc chờ, nơi gọi hiện chân dung như cơ chế cũ.
  - Phần hình dời từ `Heroes/Resources/<dạng>/` sang `Heroes/Forms/<dạng>/`; chân dung ở lại `Resources`.
  - Kết quả lần đầu: 75 tướng (kể cả lính) vào gói, 5 dòng khởi đầu ở bản cài.
- **Ảnh đảo, nền trận:** `ArtLibrary.Entry.pack`. `ArtImporter.BuildLibrary` tự gán tên `land_/zone_/be_/battle_<hệ>` nằm thẳng trong `Islands/`, `BattleBG/`.
  - Trừ nền ải đầu (`battle_<hệ>_c01`, `_s1`) và ảnh nằm trong sprite atlas.
  - Kết quả lần đầu: 55 ảnh vào gói.
- **Tải ngầm:** `App.Start` gọi `Prefetch` theo thứ tự đảo; `StarterDialog` đẩy gói đảo của tướng vừa chọn lên đầu.
- **Menu `PokiClash/Tải sau/`:**
  - Gán gói (tướng + ảnh đảo); Gán gói tướng.
  - Bỏ ảnh của gói nướng sẵn trong prefab (`Zone.prefab` từng nướng `zone_thuy`).
  - Xem trước gói (`Temp/PokiShots/tai_sau.txt`).
  - Gỡ gói: bản cài mang hết như trước.
  - Tour thử (vào đảo, trận, mất mạng).
- **Giữ việc gán gói khi chạy lại công cụ:** các menu nhập tướng (`AolaImport`, `AtomikForms.Attach`) trả dạng về `Resources` trước khi chạy và gán gói lại sau. "Dựng lại danh mục ảnh" tự gán ảnh.
- **Build:** `PokiBuild` bật Split Application Binary cho AAB phát hành, tắt cho APK thử. `BuildSizeReport` của AAB ghi cỡ từng module, bản cài và 5 gói.
- **Gỡ lỗi:** SRDebugger mục "Tải sau" có giả lập gói chưa tải (Editor), giả lập mất mạng, trạng thái 5 gói.
- **Kiểm:**
  - Test `ContentPackTests` 4/4 đạt: tướng đúng gói, chân dung ở `Resources`, bản cài không phụ thuộc gói, ảnh gói có địa chỉ.
  - Cả bộ EditMode chỉ hỏng `PrefabOnlyTests`, hỏng từ trước.
  - Tour thử đạt 10/10: vào đảo Hỏa có ảnh thật; trận Hỏa có hình tướng; mất mạng thì ở lại sảnh; có mạng thì chờ tải rồi vào đảo Kim.

**Số đo (build 2026-11-23 16:06, `Build/BaoCao/PokiWar_0.1.0_26112315.txt`):**

| Bản | Cỡ |
|---|---|
| AAB phát hành: bản cài (base 87,8 MB cộng install-time 7,4 MB) | **~95 MB** |
| 5 gói tải sau | 65,7 MB: Thủy 18,4, Mộc 15,5, Hỏa 14,0, Kim 9,1, Thổ 8,6 |
| APK thử (bản đủ, gói nằm trong `assets/aa`) | 168,5 MB (trước đó 167 MB) |

Số đã nén trong file `.aab`; cỡ tải về Play tính lại khi tải lên Play Console.

**Giữ ở bản cài (đừng đưa vào gói):**
- Nước động của sảnh: `Islands/Resources/sanh_nuoc_*.mat`, `Baked/Islands/Resources/sanh_nuoc_*_hc.png`, sprite `sanh_nuoc_*` và `anim_*`.
- Hải âu trên sảnh: `land_thuy_chim_1..3`. Hiện nằm trong atlas `dao_hinh_roi_thuy` nên ở bản cài; khi chuyển atlas theo hệ vào gói thì phải giữ ba ảnh này lại.

**Tách atlas hạt theo hệ (T4), đang dở (2026-11-23 17:00, người dùng bảo tạm dừng):**
- Quét xong: tour `PokiClash/Tải sau/Quét ảnh hạt từng tướng` cho 50 tướng diễn đòn, chiêu, chiêu cuối ở sao cuối. Kết quả ở `Assets/03 Art/Fx/hat_dung.json`, 969 ảnh được dùng.
- Chia theo diện tích ảnh:
  - chỉ một hệ dùng, vào gói được: 24% (Mộc 8, Thủy 7, Thổ 4, Kim 3, Hỏa 2%);
  - dùng chung hoặc tướng khởi đầu dùng, ở bản cài: 53%;
  - không thấy ai dùng ở dạng cuối, ở bản cài cho an toàn: 23%. Phần lớn là bộ khung code vẫn nhắc tới (lá xoáy, quạt đất, sét…), chắc dùng ở dạng 1–2 hoặc cho lính.
- Ước bớt khoảng 4 MB bản cài, không phải 14 MB như mục 9 ước: nhiều hiệu ứng là đồ dùng chung hoặc thuộc tướng khởi đầu.
- Lúc chạy: `HatLua.S` lấy ảnh không có trong mảng của bản cài từ gói đã nạp; `FbArt` không nhớ kết quả rỗng.
- **Menu `Gán gói ảnh hạt` lần đầu chạy bằng bản chưa gom:** mỗi lần dời một ảnh, Unity dựng lại cả atlas `hat` (10–20 giây). Code đã sửa: gom các lần dời trong `StartAssetEditing`, lần sau chỉ vài phút.
- **Lượt đó đã bị dừng** (người dùng bảo tắt Unity lúc 17:00). Mới dời 65 ảnh: Kim 25, Mộc 31, Thổ 9, nằm ở `Fx/HatGoi/<hệ>/`. Chưa dựng atlas `hat_<hệ>`, chưa gán gói, chưa bỏ khỏi mảng `hatSprites`.
  - Game vẫn chạy đủ hiệu ứng, vì prefab còn trỏ thẳng các ảnh này.
  - Nhưng nếu build lúc này, 65 ảnh đó vào bản cài dưới dạng ảnh rời không nén. **Đừng build bản phát hành trước khi chạy lại `Gán gói ảnh hạt`.**
- **Làm tiếp:**
  1. Chờ `Editor.log` có dòng `[Gói] Ảnh hạt: dời …`.
  2. Refresh để Unity biên dịch bản sửa.
  3. Chạy lại `Gán gói ảnh hạt` (bỏ qua ảnh đã đúng chỗ, dựng atlas `hat_<hệ>`, bỏ ảnh đã dời khỏi mảng `hatSprites`).
  4. Chạy test `ContentPackTests`, tour thử, rồi một tour hiệu ứng có trận (vd. `PokiClash/Thử/Tướng/Đảo Hỏa/…`) để soát hạt không mất.
  5. Build AAB đo lại.

**Còn lại:**
- Material nước, phác vùng của đảo (`land_water_<hệ>`, `land_sketch_<hệ>` cùng ảnh `_dist`, `_vung`).
- Atlas ảnh rời theo đảo `dao_hinh_roi_<hệ>`, nhạc đảo `bgm_dao_<hệ>`.
- Thanh tiến độ trên màn chờ (T6).
- Thử trên máy bằng `bundletool --local-testing` và kênh thử nội bộ của Play (T7).

## Nguồn

- Google Play: giới hạn app bundle và asset pack: https://support.google.com/googleplay/android-developer/answer/9859372
- Android Developers, Play Asset Delivery: https://developer.android.com/guide/playcore/asset-delivery
- Android Developers, tích hợp asset delivery cho Unity: https://developer.android.com/guide/app-bundle/asset-delivery/build-unity
- Unity, Addressables for Android (schema Play Asset Delivery): https://docs.unity3d.com/Packages/com.unity.addressables.android@1.0/manual/play-asset-delivery-schema-reference.html
- Unity Discussions, Play Asset Delivery x Addressables: https://discussions.unity.com/t/play-asset-delivery-x-addressables/1571063
- Unity, bảng giá Gaming Services (CCD): https://unity.com/products/gaming-services/pricing
- Cloudflare R2, bảng giá: https://developers.cloudflare.com/r2/pricing
