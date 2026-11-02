## ADDED Requirements

### Requirement: Quy ước ảnh gen
Ảnh gen (đảo, nền trận, bộ UI, icon, máy bi, side meta) SHALL đi theo các gói `ArtGen/<gói>/PROMPTS.md`. Mỗi ảnh có mã và tên file cố định, lưu vào `ArtGen/<gói>/inbox/`. Bước xử lý (cắt nền, cắt lưới, 9-slice, nén) MUST đưa ảnh vào `Assets/03 Art/<gói>/` với đúng tên mà code tìm.

#### Scenario: Thêm ảnh đảo mới
- **WHEN** chủ dự án lưu `zone_moc.png` vào `ArtGen/Islands/inbox/` và chạy bước xử lý
- **THEN** scene Đảo Mộc dùng ảnh đó thay cho bản đồ vẽ tay, không phải sửa code

### Requirement: Ảnh thay thế khi thiếu
Khi một ảnh chưa có, game SHALL dùng ảnh thay thế để vẫn chơi được:
- đảo dùng bản đồ nét tay vẽ bằng code (khối vùng tô gạch sáp, icon cảnh vật, đường mòn);
- khung dùng 9-slice vẽ bằng code;
- icon dùng bộ icon SVG của bản web.

Thiếu ảnh MUST chỉ ghi cảnh báo, không gây lỗi.

#### Scenario: Chưa có ảnh đảo Thổ
- **WHEN** người chơi vào Đảo Thổ khi chưa có `zone_tho`
- **THEN** scene hiện bản đồ nét tay có 8 ải trên đường mòn, chơi bình thường

### Requirement: Toạ độ theo ảnh
Vị trí các vùng trên ảnh đảo lớn và vị trí 8 ải trên mỗi ảnh đảo hệ SHALL lưu trong dữ liệu đảo, dạng tỉ lệ 0–1 theo khung ảnh. Thay ảnh mới MUST chỉ cần sửa toạ độ trong dữ liệu.

#### Scenario: Ảnh đảo gen lại
- **WHEN** ảnh `zone_hoa` được gen lại và đường mòn đổi chỗ
- **THEN** chỉ cần sửa 8 cặp toạ độ trong dữ liệu Đảo Hỏa để ải nằm lại trên đường mòn

### Requirement: Hình tướng aola không nằm trong Assets
Animation tướng lấy từ dự án AolaRipper SHALL được Editor đọc từ thư mục cấu hình được, không chép vào Assets.

Bản build lên máy thật SHALL mang theo bản chép của hình tướng: bước build chép tạm vào `StreamingAssets/PokiDev` rồi xoá ngay sau build. Lúc chạy, game đọc bản đó (Android: đọc từ APK, chép ra bộ nhớ app khi cần).

Quyết định của chủ dự án (2026-11-02): giai đoạn prototype thì mọi bản build đều mang hình. Trước khi phát hành công khai MUST tắt `AolaDevBuild.AllBuilds`; khi đó chỉ Development Build mang hình, và bản phát hành MUST không chứa hình hay dữ liệu chuyển động của Baitian.

#### Scenario: Build lên máy (prototype)
- **WHEN** build Android từ Build Profiles khi `AllBuilds` bật
- **THEN** bước kiểm tra trước build vẫn báo lỗi nếu Assets có đường dẫn aola hoặc ảnh `pet*_parts`; APK có `assets/PokiDev/reskin/...` đủ hình mọi tướng; sau build `Assets/StreamingAssets/PokiDev` không còn

#### Scenario: Build phát hành công khai
- **WHEN** `AllBuilds` tắt và build không phải Development
- **THEN** bản build không mang hình aola, ô tướng để trống cho tới khi có hình mới

#### Scenario: Bản dev đổi máy
- **WHEN** thư mục aola nằm ở ổ khác trên máy mới
- **THEN** người làm chỉ cần đặt lại đường dẫn trong cài đặt Editor hoặc biến `AOLA_RESKIN`, không sửa code
