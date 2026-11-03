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

### Requirement: Hình tướng aola nhập vào Assets thành prefab tướng
Quyết định của chủ dự án (2026-11-02, thay cách đọc từ đĩa và chép vào `StreamingAssets` lúc build): tướng lấy từ AolaRipper SHALL được nhập vào project thành prefab tướng và nén ngay lúc nhập, bằng menu `PokiClash/Tướng/Nhập hình tướng aola thành prefab` (`Editor/AolaImport.cs`).
- Mỗi dạng nằm ở `Assets/03 Art/Heroes/Resources/<dạng>/`, gồm: một atlas (hình mảnh thu nhỏ về độ nét RenderTexture thật sự dùng, ASTC 6x6, không mipmap), chân dung, animation gzip, và asset `AolaAnim`.
- Mỗi tướng là prefab `Assets/04 Prefabs/Heroes/<id>.prefab` (`AolaActor` giữ các dạng); danh mục `Assets/02 Data/HeroModels.asset` gắn vào `UiAssets.heroes`.
- Atlas và chân dung SHALL nạp khi cần (`Resources.Load`), không trỏ thẳng từ danh mục; nếu trỏ thẳng thì mọi ảnh tướng vào bộ nhớ ngay lúc mở game.

Giai đoạn prototype thì mọi bản build đều mang hình. Trước khi phát hành công khai MUST tắt `PreBuildCheck.HeroArtInBuild`; khi đó build báo lỗi cho tới khi thay hết hình Baitian.

#### Scenario: Build lên máy (prototype)
- **WHEN** build Android khi `HeroArtInBuild` bật
- **THEN** bước kiểm tra trước build vẫn báo lỗi nếu Assets có đường dẫn aola hoặc ảnh `pet*_parts` ngoài `Assets/03 Art/Heroes`; bản build mang hình tướng như asset thường, không chép gì vào `StreamingAssets`

#### Scenario: Build phát hành công khai
- **WHEN** `HeroArtInBuild` tắt
- **THEN** build báo lỗi nếu `Assets/03 Art/Heroes` còn ảnh hay animation

#### Scenario: Thêm tướng hoặc sửa hình bên AolaRipper
- **WHEN** thêm dạng vào dữ liệu web (`forms[].aola`) hoặc xuất lại `reskin/<dạng>/export`
- **THEN** chạy lại menu nhập: dạng mới hoặc đổi được nhập lại, dạng không đổi bỏ qua; thư mục aola tìm như trước (EditorPrefs hoặc biến `AOLA_RESKIN`)
