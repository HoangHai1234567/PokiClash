## Why

Bản web thử (Web/) đã được duyệt về luật trận, bố cục scene kiểu Clash of Critters và phong cách "sổ tay phiêu lưu" vẽ tay. Để làm game thật trong Unity cần một nền chung trước khi làm từng tính năng:
- cách chia và chuyển scene;
- bộ UI vẽ tay dùng lại được;
- lưu dữ liệu, dữ liệu game, quy ước ảnh.

Project Unity hiện chỉ có bản thử xếp khối `Assets/01 Script/BanThu` (hướng đã bỏ). Code đó còn trỏ thư mục aola ở `E:/ProjectAtomik` của máy cũ.

GDD gốc không nói về kỹ thuật. Change này phục vụ mọi phần còn lại: "Gameplay chính", "Máy pachinko", "Side Meta".

## What Changes

- Scene **Boot** giữ các dịch vụ dùng chung: lưu, âm thanh, chuyển cảnh, hộp thoại. Mỗi chức năng là một scene riêng, nạp cộng (additive): Hub (đảo lớn), Zone (đảo hệ), Battle, Machine, Heroes, Cards, Notebook; sau này thêm Farm, Badges, Potential.
- Chuyển scene bằng **màn mây vẽ tay** khép vào rồi tách ra, khoảng 0,38 giây mỗi chiều.
- Thanh trên của sảnh: vòng cấp có EXP, số bi, AFK, nút Sổ tay. Scene con có **thanh quay lại**: nút quay lại, tên scene, cấp, bi. Không có thanh tab.
- **Bộ UI vẽ tay** (uGUI):
  - giấy kẻ ô, khung nét mực rung (shader 3 nhịp), gạch sáp, băng keo;
  - nút, thanh máu/mana/nộ/EXP, chip tài nguyên, thẻ bài theo độ hiếm;
  - hộp thoại, thông báo, con dấu, bong bóng gợi ý.
- Phông TextMeshPro tiếng Việt: Baloo 2 (tiêu đề, số), Pangolin (chữ thường).
- **Lưu** JSON có phiên bản trong `Application.persistentDataPath`, kèm cài đặt (nét rung, âm thanh, gợi ý, tốc độ trận).
- Chép phần logic dùng chung của `Web/src/core` sang assembly C# thuần `PokiClash.Core`: số ngẫu nhiên có hạt giống, kiểu dữ liệu, Ngũ hành, cấu hình cân bằng, sinh mô tả thẻ.
- Dữ liệu tướng, thẻ, đảo, ải xuất từ `Web/src/core/data` ra JSON, nạp vào ScriptableObject. Bản web và Unity dùng chung một nguồn số.
- Quy ước ảnh theo các gói `ArtGen/` (tên file, import, 9-slice, atlas). Thiếu ảnh thì dùng ảnh thay thế, game vẫn chạy.
- Đọc animation tướng aola từ đường dẫn cấu hình được, **chỉ trong bản dev**. Bản phát hành không chứa hình Baitian.
- Gỡ scene `BanThu.unity` khỏi Build Settings. Giữ code BanThu cho tới khi chủ dự án cho xoá.

## Capabilities

### New Capabilities

- `app-shell`: scene Boot, nạp và chuyển scene bằng màn mây, thanh trên của sảnh, thanh quay lại, hộp thoại và thông báo, khung dọc co giãn.
- `ui-theme`: phong cách vẽ tay dùng chung: giấy, nét mực rung, gạch sáp, băng keo, nút, thanh, thẻ theo độ hiếm, phông tiếng Việt, tướng dạng sticker, chữ tượng thanh, âm thanh.
- `game-save`: lưu cục bộ có phiên bản, cài đặt, xoá dữ liệu.
- `art-assets`: quy ước và cách nạp ảnh gen (đảo, UI, icon), ảnh thay thế khi thiếu, animation tướng aola chỉ trong bản dev.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code mới:**
  - `Assets/01 Script/Core/` (asmdef `PokiClash.Core`, không tham chiếu UnityEngine);
  - `Assets/01 Script/App/` (Boot, chuyển scene, lưu, âm thanh);
  - `Assets/01 Script/UI/` (bộ UI vẽ tay);
  - `Assets/01 Script/Editor/` (nhập dữ liệu, tạo scene).
- **Scene mới:** `Assets/00 Scenes/Boot.unity`, `Hub.unity`, `Zone.unity`, `Battle.unity`, `Machine.unity`, `Heroes.unity`, `Cards.unity`, `Notebook.unity`.
- **Dữ liệu:** `Assets/02 Data/` (JSON xuất từ web, ScriptableObject).
- **Ảnh:** `Assets/03 Art/`. Ảnh gen lấy từ `ArtGen/*/inbox/` qua bước xử lý.
- **Phông:** Baloo 2, Pangolin (OFL) đưa vào `Assets/03 Art/Fonts`.
- **Shader:** `PokiClash/UIInkBoil` (UI nét rung), dùng cho Image và TMP.
- **ProjectSettings:** đổi Build Settings (thêm scene mới, bỏ BanThu). Phải hỏi chủ dự án trước khi sửa.
- **Web/:** thêm script xuất dữ liệu `Web/scripts/export_data.ts` (sinh JSON cho Unity) và bộ dữ liệu đối chiếu (golden) cho kiểm thử.
- **Phụ thuộc:** không. Mọi change khác phụ thuộc change này.
