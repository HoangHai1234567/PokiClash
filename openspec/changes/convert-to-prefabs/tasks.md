## 1. Nướng tài nguyên

- [x] 1.1 Menu `PokiClash/Prefab/1. Nướng ảnh và âm thanh`: sprite `Sketch` → PNG (đặt sRGB, 9-slice, pivot, wrap, không nén), nhiễu → `PokiNoise.png`, `SfxSynth` → WAV, hình tướng giữ chỗ → PNG theo hệ
- [x] 1.2 Asset `BakedArt` giữ tham chiếu; `Sketch`, `HeroArt`, `Theme` (nhiễu) và `AudioService` đọc asset đã nướng, thôi vẽ hoặc tổng hợp lúc chạy
- [x] 1.3 Material chữ viền nướng sẵn cho mọi cỡ viền đang dùng; `Theme.Outlined` lúc chạy chỉ tra bảng
- [x] 1.4 Kiểm: ảnh chụp vòng thử giống ảnh trước; EditMode test đạt; console không lỗi

## 2. Bộ kit prefab

- [x] 2.1 `SketchButton` giữ tham chiếu và màu `BtnColor` (áp trong `OnValidate`); 5 prefab nút theo cỡ
- [x] 2.2 `Khung`, `KhungMong`, `Chip`, `Thanh` (`UiBar` giữ tham chiếu, loại chọn trong Inspector), `NhanHe`, `Sao`, `BangKeo`, `ConDau`, `GoiY`
- [x] 2.3 `The`, `TheMini` (`UiCard.Bind(card, lv, icon, locked)`)
- [x] 2.4 Kiểm: mở từng prefab kit trong Editor thấy đúng hình; console không lỗi

## 3. Khung app và hộp thoại

- [x] 3.1 `App.prefab` trong `Boot.unity`: camera, EventSystem, âm thanh, canvas thanh trên (`TopBars` giữ tham chiếu), canvas phủ (hộp thoại, thông báo, mây), chuyển scene; `App.Awake` không tạo gì
- [x] 3.2 Prefab canvas màn hình (`PokiCanvas` giữ tham chiếu Nen / An toan / Khung)
- [x] 3.3 Tờ giấy gốc `HopThoai.prefab` (ModalService sinh mỗi hộp từ prefab này); prefab `ThongBao`
- [x] 3.4 Kiểm: vòng thử chạy đủ, hộp xác nhận ở Sổ tay giống ảnh trước
- [x] 3.5 Biến thể hộp Báo, Xác nhận, Lên cấp, Giới thiệu (`ModalService.Open(prefab)` + component riêng); làm cùng phần 4

## 4. Scene chức năng

- [x] 4.1 Sảnh: prefab màn hình, bảng tên vùng và công trình là prefab mục; hộp AFK, Cây bi, Mở rương
- [x] 4.2 Đảo: prefab màn hình, nút ải là prefab mục; hộp Chuẩn bị trận
- [x] 4.3 Tướng: lưới thẻ tướng (`Screens/Heroes`, ô `Items/TheTuong`); chân dung tướng và huy hiệu vào kit (`ChanDung`, `HuyHieu`)
- [x] 4.3b Hộp Chi tiết tướng, ô xem tướng, Tiềm năng
- [x] 4.4 Sổ thẻ: prefab màn hình `Screens/Cards`, thẻ sinh từ prefab kit; hộp chi tiết `Dialogs/ChiTietThe` (biến thể tờ giấy gốc); ảnh trùng khớp bản cũ
- [x] 4.5 Máy bi: mặt máy (ảnh tĩnh đã nướng, đinh và bi là prefab), khay rương, bảng tỉ lệ
- [x] 4.6 Sổ tay, Sổ tay bản dev, quảng cáo giả lập
- [x] 4.7 Đền Huy Hiệu, Hang Tiềm Năng, Trang trại
- [x] 4.8 Kiểm: mọi menu `PokiClash/Thử/...` chạy được, ảnh so với ảnh trước; console không lỗi

## 5. Trận đấu

- [x] 5.1 Prefab màn hình trận: thanh trên, sân đấu, bảng thông tin, bảng dưới
- [x] 5.2 Sân đấu: tướng, chữ tượng thanh, số sát thương, tia văng, vòng khiên là prefab (dùng pool)
- [x] 5.3 Hộp Kết quả, Tạm dừng, Đổi tướng; băng rôn, VS, gợi ý
- [x] 5.4 Kiểm: `Đánh thử ải 1`, `ải 7`, `ải 8 boss` chạy hết trận, ảnh so với ảnh trước; console không lỗi

## 6. Dọn và chốt

- [x] 6.1 `Tests/PrefabOnlyTests.cs`: quét mã runtime, danh sách ngoại lệ có lý do
- [x] 6.2 `ProjectSetup.BuildAll` thôi dựng lại scene đã có; Boot mới đặt prefab App
- [x] 6.3 Xoá `Editor/Bake/`, phần dựng của `Ui.cs`, `Sketch.cs`, `SceneKit.cs`, lớp tạm `BakedArt` nếu không còn dùng (hỏi chủ dự án trước khi xoá)
- [x] 6.4 Kiểm: EditMode test đạt (cả test chặn), `Kiểm tra trước build`, `Biên dịch thử bản phát hành`; cập nhật `GD_Claude/12_KeHoach_OpenSpec.md`
- [x] 6.5 `Nhập ảnh ArtGen` thay ảnh thay thế bằng ảnh gen cùng tên trong mọi prefab

## Ghi chú khi làm

- Prefab con lồng trong prefab khác: thay đổi bằng code (màu, `sortingOrder`, chữ) không tự thành ghi đè; `BakeEnv.RecordNested` ghi nhận trước khi lưu.
- Ô ảnh của prefab đổi sprite lúc chạy phải đổi material theo sprite (`Theme.SetSprite`): sprite giấy và mực dùng material mã hoá, icon dùng material thường.
- Canvas phải là canvas gốc lúc nướng (không nằm dưới canvas tạm) thì `sortingOrder` mới lưu được.
- MonoBehaviour dùng trong prefab phải nằm trong file cùng tên (đã tách `ClickCatcher`; còn `Bob`, `Wobble`, `Pulse`, `HoldArea` tách khi làm Sảnh, Tướng, Máy bi).
- Hộp mở từ hàm tĩnh hoặc từ nhiều màn (Báo, Xác nhận, Lên cấp, Giới thiệu, Mở rương, AFK, Cây bi, Chuẩn bị trận, Chi tiết tướng, Tiềm năng, Quảng cáo giả) nằm trong `UiKit.dialogs`, mở bằng `App.Modals.Open<T>()`; hộp riêng của một màn nằm trong `[SerializeField]` của màn.
- `ArtImporter` (OnPreprocessTexture) không được đụng `Assets/03 Art/Baked/`: trước đây nó ép cỡ 1024, nén ASTC trên Android, đổi nhiễu sang Sprite/Clamp. Menu `1b. Nướng lại ảnh` đặt lại cách nhập.
- Ảnh vòng thử lệch tự nhiên giữa hai lần chạy: hạt giống máy bi ngẫu nhiên, trận rút thẻ ngẫu nhiên, AFK theo giờ thật, Hang theo thứ trong tuần, mây sảnh trôi, bản lưu trôi sau vòng `Run()` đầu (không sao lưu). So bằng mức lệch nền (`diff_shell_all`) chứ không đòi 0%.
- Công cụ ghép ảnh `crop.ps1` có thể vẽ lệch cỡ ảnh bên trái: đo bằng hộp bao điểm ảnh khi nghi lệch cỡ.
