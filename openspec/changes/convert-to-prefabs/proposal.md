## Why

Chủ dự án (2026-11-01): "tất cả mọi thứ trong game quy về prefab, kể cả UI, không sinh runtime bất cứ thứ gì". Chọn hướng "nướng một lần rồi bỏ code dựng".

Hiện trạng khi chốt:
- `Assets` chưa có prefab nào. Khoảng 227 chỗ dựng lúc chạy trong 45 file.
- Bộ UI dựng bằng code: `UI/Kit/Ui.cs` (`new GameObject`, `AddComponent`), `Sketch.cs` vẽ sprite giấy và mực bằng `Texture2D`, `Theme.cs` tạo material viền chữ và texture nhiễu.
- Khung app (`App`, `PokiCanvas`, `TopBars`, `ModalService`, `ToastService`, `CloudCover`, `SceneRouter`) dựng trong `Awake`. `AudioService` tổng hợp `AudioClip` lúc khởi động.
- 10 scene chức năng chỉ có một GameObject rỗng gắn `SceneRoot`; giao diện dựng trong `Enter()`. Menu `Dựng tất cả` dựng lại scene mỗi lần chạy.
- Trận: `BattleView`, `StageView`, `HeroArt` (hình giữ chỗ vẽ bằng code), `BattleController` (hộp kết quả, tạm dừng, đổi tướng).
- Máy bi: `MachineBoard` vẽ phần tĩnh vào texture lúc chạy.

Không chỉnh được giao diện trong Editor, không xem trước được bố cục khi chưa Play.

## What Changes

- **Quy tắc:** code chạy trong game không tạo GameObject, component, sprite, texture, material, mesh hay âm thanh. Được phép:
  - `Instantiate` prefab có sẵn (danh sách dài ngắn theo dữ liệu, hiệu ứng, pool);
  - bật/tắt, đổi chữ, ảnh, màu, vị trí trên các tham chiếu kéo thả;
  - tìm ảnh theo tên trong `ArtLibrary` (ảnh đã nhập sẵn).
- **Nướng tài nguyên vẽ bằng code** thành asset (một lần, bằng menu Editor):
  - sprite của `Sketch` → PNG;
  - texture nhiễu nét rung → PNG;
  - chữ viền mực → material TMP;
  - tiếng tổng hợp → WAV;
  - hình tướng giữ chỗ → PNG theo hệ;
  - phần tĩnh của máy bi → PNG.
- **Bộ kit prefab:** nút (5 cỡ, màu chọn trong Inspector), khung giấy, chip, thanh, nhãn hệ, sao, băng keo, con dấu, bong bóng gợi ý, thẻ bài (thường, mini).
- **Khung app thành prefab** đặt trong `Boot.unity`: camera, EventSystem, âm thanh, canvas thanh trên, canvas phủ (hộp thoại, thông báo, mây), chuyển scene.
- **Hộp thoại thành prefab:** mỗi hộp là biến thể (prefab variant) của tờ giấy gốc, `ModalService` mở theo prefab.
- **Mỗi scene chức năng là một prefab màn hình** (gồm canvas, `SceneRoot`, nội dung); file `.unity` chỉ chứa prefab đó. Phần lặp theo dữ liệu (thẻ tướng, ải, ô trang trại…) là prefab mục.
- **Code dựng bị xoá** sau khi nướng và kiểm xong (hỏi chủ dự án trước khi xoá). Từ đó prefab là nguồn sự thật, chỉnh trong Editor.
- **Test chặn:** EditMode test quét mã runtime, báo lỗi khi gặp API dựng lúc chạy ngoài danh sách ngoại lệ.
- **Công cụ:** menu `Dựng tất cả` thôi dựng lại scene; menu `Nhập ảnh ArtGen` đổi tham chiếu ảnh thay thế sang ảnh gen trong prefab.

## Capabilities

### New Capabilities

- `prefab-content`: mọi nội dung game (UI, khung app, scene, hiệu ứng, âm thanh, ảnh) là asset làm sẵn; runtime chỉ sinh bản sao prefab và gán dữ liệu.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. Giao diện và hành vi giữ nguyên như các change trước; chỉ đổi cách dựng. -->

## Impact

- **Unity:**
  - mới: `Assets/04 Prefabs/` (Kit, App, Dialogs, Screens, Items, Battle); asset nướng trong `Assets/03 Art/Baked/`; `Editor/Bake/*` (tạm, xoá khi xong); test `Tests/PrefabOnlyTests.cs`;
  - sửa: gần như mọi file trong `App`, `UI`, `Game` (đổi từ dựng sang tham chiếu kéo thả); `Editor/ProjectSetup.cs`, `ArtImporter.cs`, `PlayTour.cs` nếu cần;
  - xoá (hỏi trước): phần dựng của `Ui.cs`, `Sketch.cs`, `SceneKit.cs`, các hàm `Create`/`Build`.
- **Không đổi:** luật, số liệu, bản lưu, bản web, `Core/`.
- **Ngoại lệ chờ chủ dự án duyệt:** hình aola bản dev (`AolaActor`, `AolaSticker`) đọc PNG ngoài project lúc chạy; scene thử cũ `BanThu` không chuyển.
- **Phụ thuộc:** mọi change trước (0–11) đã xong phần code.
- **GDD gốc:** không có dòng tương ứng; đây là yêu cầu kỹ thuật của chủ dự án.
