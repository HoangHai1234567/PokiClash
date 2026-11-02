## Context

Mốc 0–11 dựng mọi thứ bằng code để chép nhanh bố cục bản web: hàm `Ui.*` tạo GameObject, `Sketch` vẽ sprite bằng SDF, mỗi `SceneRoot` dựng giao diện trong `Enter()`. Chủ dự án muốn ngược lại: mọi thứ là prefab, chỉnh trong Editor, runtime không sinh gì.

Không đổi luật, số, bản lưu, nên không cần chép thêm gì từ `Web/src/core`. Hành vi và hình ảnh phải giữ như trước khi chuyển; đo bằng ảnh chụp `PlayTour` trước và sau.

## Goals / Non-Goals

**Goals:**
- Runtime chỉ `Instantiate` prefab có sẵn và gán dữ liệu vào tham chiếu kéo thả.
- Mở prefab màn hình trong Editor là thấy đúng bố cục như khi chạy (với dữ liệu mẫu lúc nướng).
- Kit dùng lồng (nested prefab): sửa prefab nút thì mọi nút trong mọi màn đổi theo.
- Giữ tên GameObject như cũ để menu thử `PokiClash/Thử/...` chạy tiếp.

**Non-Goals:**
- Đổi bố cục, phong cách, luật. Chỉ đổi cách dựng.
- Hình tướng aola bản dev (ngoại lệ, chờ chủ dự án duyệt).
- Scene thử cũ `BanThu` (đã bỏ hướng xếp khối).

## Decisions

### Nướng bằng chính code dựng hiện có, rồi xoá code dựng

Mỗi phần có một hàm nướng trong `Editor/Bake/`. Hàm nướng là code dựng cũ chuyển sang Editor, bỏ phần gán dữ liệu:
1. dựng cây GameObject, đặt các mục kit bằng `PrefabUtility.InstantiatePrefab` để giữ liên kết lồng;
2. gắn component View, nối tham chiếu `[SerializeField]` qua `SerializedObject` theo tên trường;
3. lưu bằng `PrefabUtility.SaveAsPrefabAsset`.

Prefab đã có thì menu nướng bỏ qua, chỉ ghi đè khi chọn bản "(ghi đè)". Lý do: tránh xoá công chỉnh tay.

Khi mọi phần đã nướng và kiểm xong, xoá `Editor/Bake/` cùng phần dựng runtime (hỏi chủ dự án trước). Từ đó prefab là nguồn sự thật.

- **Phương án khác: dựng tay từng prefab qua MCP.** Bỏ: hàng nghìn lệnh, dễ lệch so với bản đang chạy.
- **Phương án khác: giữ code dựng làm "nguồn", nướng lại mỗi khi sửa.** Bỏ: trái ý chủ dự án (chỉnh trong Editor), và nướng lại sẽ xoá công chỉnh tay.

### Code runtime: View giữ tham chiếu, Bind gán dữ liệu

Mỗi màn hình và mỗi mục có một component View: tham chiếu `[SerializeField]` tới chữ, ảnh, nút, khung chứa, prefab mục. Hàm `Bind(...)` hoặc `Render()` chỉ gán chữ, ảnh, màu, bật/tắt, sinh bản sao prefab mục vào khung chứa.

Component trước đây thêm lúc chạy (`CanvasGroup` để mờ dần, `ClickCatcher`, `Pulse`, `Bob`, `LayoutElement`, `RectMask2D`) có sẵn trên prefab, tắt khi chưa dùng.

### Tài nguyên nướng

Tất cả ở `Assets/03 Art/Baked/`. Menu `PokiClash/Prefab/1. Nướng ảnh và âm thanh` tạo lại được, kết quả như nhau.

| Nguồn cũ | Asset | Ghi chú nhập |
|---|---|---|
| `Sketch.*` mã hoá (khung, nút, thanh, sao, mây…) | `Sketch/sk_<tên>.png` | sRGB tắt (kênh là dữ liệu), không nén, giữ viền 9-slice, pivot, wrap |
| `Sketch.*` ảnh thường (băng keo, giấy kẻ, vòng con dấu…) | `Sketch/<tên>.png` | sRGB bật, không nén |
| `Theme` nhiễu nét rung | `PokiNoise.png` | sRGB tắt, lặp |
| `Theme.Outlined(font, độ dày)` | `Fonts/<phông> vien <k>.mat` | tạo khi nướng prefab gặp cỡ viền mới |
| `SfxSynth` | `Audio/sfx_<tên>.wav` | PCM 16 bit mono |
| `HeroArt` hình giữ chỗ | `Heroes/giu_cho_<hệ>.png` (thân, mặt nạ) | sRGB bật |
| `MachineBoard` phần tĩnh | `Machine/may_tinh.png` | sRGB bật |

`Sketch.IsEncoded` (chọn material theo tên texture) bỏ: prefab giữ sẵn material đúng.

Sau bước nướng, `Sketch` và `HeroArt` tạm thời trả sprite đã nướng từ asset `BakedArt`. Nhờ vậy phần chưa chuyển sang prefab cũng thôi vẽ texture lúc chạy. Khi mọi phần đã thành prefab thì bỏ lớp tạm này.

### Bộ kit

`Assets/04 Prefabs/Kit/`:
- `Nut_To`, `Nut_Vua`, `Nut_Nho`, `Nut_Ti`, `Nut_Tron`: một prefab mỗi cỡ. Màu chọn bằng trường `BtnColor` của `SketchButton`. `OnValidate` áp màu nền, màu chữ và material viền trong Editor, nên không cần prefab riêng cho mỗi màu.
- `Khung`, `KhungMong`, `Chip`, `Thanh` (loại Hp/Mana/Nộ/EXP/Mảnh chọn trong Inspector), `NhanHe`, `Sao`, `BangKeo`, `ConDau`, `GoiY`, `The`, `TheMini`.

### Khung app ở Boot

`Boot.unity` chứa một bản `App.prefab`, gồm:
- `Camera`, `EventSystem`;
- `Am thanh`: 10 `AudioSource` gắn sẵn, danh sách clip WAV;
- `Canvas thanh tren` (`PokiCanvas`, `TopBars`);
- `Canvas phu`: `Hop thoai` (`ModalService`), `Thong bao` (`ToastService`, prefab `ThongBao`), `May` (`CloudCover`);
- `Chuyen scene` (`SceneRouter`).

`App.Awake` không tạo gì, chỉ đăng ký tham chiếu. Canvas ở scene chức năng là `Screen Space - Camera`. Camera nằm ở Boot nên không kéo thả được qua scene: `PokiCanvas.Awake` gán `worldCamera = PokiCanvas.UiCamera`. Đây là gán tham chiếu, không sinh gì.

### Hộp thoại

`Dialogs/HopThoai.prefab` là tờ giấy gốc: nền tối, tờ giấy, lưới, băng keo, nút đóng, `Body` dọc tự giãn, component `Dialog`. Mỗi hộp (Báo, Xác nhận, Lên cấp, Giới thiệu, AFK, Cây bi, Mở rương, Chuẩn bị trận, Chi tiết tướng, Tiềm năng, Kết quả trận, Tạm dừng, Đổi tướng…) là prefab variant của tờ giấy gốc, kèm component riêng kế thừa `Dialog`.

Cách gọi: `App.Modals.Open(prefab)` trả về bản sao, rồi gọi `Show(...)` để gán dữ liệu. Thuộc tính bắt buộc (không nút đóng, chạm ngoài không đóng) và bề rộng tờ giấy chỉnh trên prefab.

### Scene chức năng

Mỗi scene có một prefab màn hình `Screens/<Scene>.prefab`, gồm canvas (`PokiCanvas`), component `SceneRoot` của scene và toàn bộ nội dung. File `.unity` chỉ chứa prefab đó.

`SceneRoot.Awake` thôi tạo canvas, chỉ đọc tham chiếu. `Enter(args)` gán dữ liệu như cũ.

`ProjectSetup.BuildAll` thôi dựng lại scene: scene thiếu thì tạo, có rồi thì để yên.

### Ảnh gen và ảnh thay thế

- Ảnh cố định của một màn (nền đảo, icon nút đáy) kéo thẳng vào prefab.
- Ảnh chọn theo dữ liệu (icon thẻ, hình tướng, nền theo hệ) vẫn tìm bằng `ArtLibrary` lúc chạy. Đây là ảnh đã nhập sẵn, không sinh mới.
- `Nhập ảnh ArtGen` thêm bước: ảnh gen mới thay ảnh thay thế cùng tên ở mọi prefab.

### Test chặn

`Tests/PrefabOnlyTests.cs` quét file `.cs` dưới `Assets/01 Script`, trừ `Editor/`, `Tests/` và danh sách ngoại lệ có ghi lý do. Gặp các mẫu sau thì báo lỗi kèm file và dòng:
- `new GameObject(`, `AddComponent`, `CreatePrimitive(`;
- `Sprite.Create(`, `new Texture2D(`, `new RenderTexture(`;
- `new Material(`, `new Mesh(`, `AudioClip.Create(`.

Ngoại lệ ban đầu:
- `Game/Heroes/AolaActor.cs`, `AolaSticker.cs`: bản dev, đọc hình aola ngoài project;
- `BanThu/`: scene thử cũ.

### Kiểm tra từng phần

1. Trước khi chuyển một phần, chụp bằng menu `PokiClash/Thử/...` của phần đó (ảnh trước để ở scratchpad, không vào project).
2. Sau khi chuyển, chạy lại cùng menu, so ảnh, chạy 70+ EditMode test, kiểm tra console không lỗi.
3. Cuối cùng chạy `Kiểm tra trước build` và `Biên dịch thử bản phát hành`.

## Risks / Trade-offs

- **Diff rất lớn.** Mỗi phần có báo cáo riêng để chủ dự án commit theo phần.
- **Bố cục tự giãn theo dữ liệu** (nút rộng theo chữ, hộp cao theo nội dung) giờ là cỡ cố định hoặc `ContentSizeFitter` trên prefab. Chữ dài hơn mẫu lúc nướng có thể tràn; `TMP` tự co cỡ chữ ở các chỗ cũ đã bật.
- **Nướng lại xoá công chỉnh tay.** Vì vậy menu mặc định bỏ qua prefab đã có, và xoá code nướng khi xong.
- **Sửa nhiều prefab lồng cùng lúc** dễ có ghi đè (override) thừa. Hàm nướng chỉ ghi đè chữ, cỡ, màu, vị trí.

## Open Questions

- Hình aola bản dev: giữ ngoại lệ đọc PNG lúc chạy, hay nhập vào project thành asset (loại khỏi bản phát hành)?
- `BanThu`: bỏ qua hay xoá?
