## 1. Dọn project

- [x] 1.1 Hỏi chủ dự án rồi mới gỡ `BanThu.unity` khỏi Build Settings; giữ nguyên code `Assets/01 Script/BanThu`
- [x] 1.2 Tạo thư mục `Assets/01 Script/{Core,App,UI,Game,Editor}`, `Assets/02 Data`, `Assets/03 Art`; asmdef `PokiClash.Core` (không tham chiếu UnityEngine), `PokiClash.Game`, `PokiClash.Editor`, `PokiClash.Tests` (hỏi trước khi thêm asmdef)
- [x] 1.3 Chuyển `AolaActor.cs`, `MiniJson.cs` sang `Assets/01 Script/Game/Heroes`, bỏ đường dẫn cứng `E:/ProjectAtomik`, đọc đường dẫn từ `EditorPrefs` hoặc `AOLA_RESKIN`, bọc trong `#if POKICLASH_DEV`
  - Chép (không chuyển) để BanThu vẫn biên dịch: `Game/Heroes/AolaActor.cs`, `Core/MiniJson.cs` (thêm phần ghi JSON). Menu `PokiClash/Đặt thư mục aola (bản dev)...`. Define `POKICLASH_DEV` chưa bật (đổi ProjectSettings, chờ chủ dự án).
- [x] 1.4 Refresh Unity qua MCP, `read_console` không lỗi

## 2. Logic thuần (chép từ Web/src/core)

- [x] 2.1 `Rng` (mulberry32) chép đúng phép bit; test 1.000 số đầu với hạt giống 1, 42, 123456 khớp bản web
- [x] 2.2 `Types`, `Elements` (Ngũ hành, khắc ×1,5 / ×0,75), `BalanceConfig` (đủ trường của `CFG`)
  - Thêm hằng số tiến trình (cấp tối đa, bảng bản sao, sao, nút ×N, tỉ trọng rút thẻ) vào `BalanceConfig`; `Progress` có `ExpToNext`, `AddExp`.
- [x] 2.3 `CardText`: sinh mô tả thẻ theo cấp thẻ, khớp chữ của bản web cho cả 56 thẻ ở cấp 1 và cấp 5
- [x] 2.4 `Web/scripts/export_golden.ts`: xuất JSON đối chiếu (số ngẫu nhiên, mô tả thẻ) để EditMode test dùng

## 3. Dữ liệu một nguồn

- [x] 3.1 `Web/scripts/export_data.ts`: xuất `heroes.json`, `cards.json`, `zones.json`, `stages.json`, `balance.json` vào `Assets/02 Data`
  - Ghi vào `Assets/02 Data/Json/`. Chạy: `npx tsx scripts/export_data.ts` trong thư mục Web.
- [x] 3.2 ScriptableObject `HeroDb`, `CardDb`, `ZoneDb`, `BalanceConfigAsset` và menu `PokiClash/Nhập dữ liệu` dựng chúng từ JSON
  - Cây hiệu ứng của thẻ giữ dạng JSON trong `CardDef.effectsJson` (Unity không giữ được cây đệ quy), đọc ra lúc chạy.
- [x] 3.3 Kiểm tra: số tướng 11, thẻ chung 23, thẻ riêng 33, đảo 5, ải 40, toạ độ ải trong khoảng 0–1

## 4. Scene và chuyển scene

- [x] 4.1 `Boot.unity` với `AppRoot` (`DontDestroyOnLoad`), `SceneRouter`, `ModalService`, `ToastService`, `AudioService`
  - Lớp gốc tên `App`; dựng camera, EventSystem (Input System), 3 canvas (nội dung, thanh trên, phủ) bằng code.
- [x] 4.2 `SceneRoot` cho mỗi scene: kiểu thanh trên (Hud/Back/None), tên, đích quay lại, `Enter(args)`
  - Bấm Play thẳng ở một scene chức năng thì scene tự nạp Boot rồi Boot mở lại scene đó.
- [x] 4.3 Màn mây vẽ tay (hai khối mây SVG chép từ bản web hoặc ảnh `ArtGen/UIKit`), khép và mở mỗi chiều 0,38 giây, chặn chạm, xếp hàng yêu cầu
  - Mây vẽ bằng code (`Sketch.Cloud`); khi có `cloud_wipe` của ArtGen thì thay.
- [x] 4.4 Tạo scene rỗng có `SceneRoot`: Hub, Zone, Battle, Machine, Heroes, Cards, Notebook; thêm vào Build Settings (hỏi trước)
  - Menu `PokiClash/Cài đặt/2. Dựng tất cả` dựng lại các scene. Build Settings: Boot, 7 scene chức năng, SampleScene (BanThu không có trong build).
- [x] 4.5 Thanh trên sảnh (vòng cấp, bi, AFK, Sổ tay) và thanh quay lại (nút quay lại, tên, cấp, bi)
  - Số bi AFK chờ là móc `TopBars.AfkPending`, mốc `add-afk-rewards` gắn hàm thật.
- [x] 4.6 Canvas Scaler 1080 × 1920 khớp chiều rộng; thành phần Safe Area; khung Game view 1080×1920, 1080×2400, 1536×2048
  - Canvas Screen Space - Camera (để hình tướng xen giữa nền và UI). Màn rộng hơn 9:16 khớp chiều cao, nội dung giữ khung 1080 ở giữa.

## 5. Bộ UI vẽ tay

- [x] 5.1 Shader `PokiClash/UIInkBoil` (3 bộ dời, 6 lần/giây, tắt được) và material dùng chung
- [x] 5.2 Khung 9-slice vẽ tay (viền mực, bóng cứng) và nền giấy có lưới; ảnh thay thế vẽ bằng code
- [x] 5.3 Prefab nút (đỏ, xanh lá, xanh dương, cam, tím, giấy; cỡ lớn, thường, nhỏ, tròn), hiệu ứng lún khi nhấn
  - Dựng bằng code (`Ui.Button`, `SketchButton`) thay cho prefab.
- [x] 5.4 Prefab thanh (máu có khiên và vệt vàng, mana, nộ phát sáng, EXP), chip tài nguyên, nhãn hệ, hàng sao
- [x] 5.5 Prefab thẻ bài (cỡ thường 160×232 và mini 100×146 ở khung 540) theo 5 độ hiếm, vệt sáng Huyền thoại, nhãn giá, khoá
- [x] 5.6 Hộp thoại (tờ giấy, băng keo, nút đóng, nền tối, bắt buộc hay không), thông báo, con dấu, bong bóng gợi ý
- [x] 5.7 Phông TMP Baloo 2 (700, 800) và Pangolin với bộ ký tự tiếng Việt đầy đủ; kiểm tra chuỗi mẫu có mọi dấu
  - TTF tải từ Google Fonts (giấy phép OFL kèm theo), font asset động, phông mặc định của TMP đổi sang Pangolin.
- [x] 5.8 Bộ âm thanh: thu các tiếng tổng hợp của `Web/src/view/sfx.ts` thành clip WAV, hoặc làm lại bằng công cụ sfxr; `AudioService` giới hạn tiếng chạm đinh
  - Tổng hợp lại lúc chạy (`Core/SfxSynth.cs`, cùng công thức WebAudio), không có file âm thanh.

## 6. Lưu

- [x] 6.1 `SaveData` chép từ `progression.ts` (`SAVE_VERSION = 2`), `SaveService` ghi qua file tạm rồi đổi tên
- [x] 6.2 Bước di chuyển phiên bản và xử lý file hỏng (báo, giữ `.bak`, tạo mới)
- [x] 6.3 Cài đặt (nét rung, âm thanh, gợi ý, tốc độ) có hiệu lực ngay; nút xoá dữ liệu có xác nhận

## 7. Ảnh

- [x] 7.1 `ArtLibrary` tìm sprite theo tên trong `Assets/03 Art`, báo cảnh báo và gọi ảnh thay thế khi thiếu
- [x] 7.2 Bộ vẽ bản đồ nét tay (chép `Web/src/view/scenery.ts`) cho đảo lớn và đảo hệ khi thiếu ảnh
  - Không chép sang C#: `Web/scripts/export_fallback.mjs` chạy chính code vẽ của web và xuất PNG (đảo lớn, 5 đảo hệ, 75 icon) vào `Assets/03 Art/Fallback`.
- [x] 7.3 Script xử lý `ArtGen/*/inbox` → `Assets/03 Art` (cắt nền trắng, cắt lưới theo hướng dẫn, đặt 9-slice, nén ASTC)
  - Menu `PokiClash/Nhập ảnh ArtGen`; bảng cắt lưới cho 6 sheet UIKit và 5 sheet icon trong `ArtImporter.Sheets`.
- [x] 7.4 Bước kiểm tra trước build: báo lỗi nếu Assets có ảnh hay đường dẫn aola

## 8. Kiểm tra

- [x] 8.1 EditMode test: `Rng`, `CardText` khớp golden của bản web
  - 18 test: Rng, mô tả thẻ, dữ liệu, bản lưu (mới, ghi đọc, file tạm, v1, hỏng), âm thanh, phông, Build Settings, aola, asset dữ liệu, cắt sheet.
- [x] 8.2 Play từ Boot: đi Hub → mọi scene con → quay lại, màn mây chạy, không lỗi console
  - Menu `PokiClash/Thử/Đi một vòng các scene (đang Play)`, có thử xếp hàng chuyển scene.
- [x] 8.3 Chụp màn hình Game view 3 khung (1080×1920, 1080×2400, 1536×2048) để soi bố cục và vùng an toàn
  - Menu `PokiClash/Thử/Chụp 3 khung màn hình (đang Play)`, ảnh ở `Temp/PokiShots`.
