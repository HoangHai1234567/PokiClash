# 24. Đa ngôn ngữ: bản tiếng Anh (2026-11-21)

Người dùng chốt: hệ tự viết nhẹ (không dùng gói Unity Localization); ngôn ngữ theo máy, có nút đổi trong Sổ tay; tên tướng, thẻ, ải đặt tên tiếng Anh mới; làm hết một lượt.

## Cách chạy

- **Tiếng Việt là gốc và là khoá.** Bảng tiếng Anh: `Assets/Resources/Loc/en/*.json`, mỗi file là một object phẳng `{ "chuỗi Việt": "English" }`.
  - `ui.json`: chữ trong code và prefab.
  - `names.json`: tên tướng, dạng, danh hiệu, dòng; đảo, ải, công trình Nhà, tầng Hang, bậc huy hiệu, gói.
  - `cards.json`: tên thẻ và lời thẻ.
- **Chọn ngôn ngữ** (`Game/Data/LocService.cs`): PlayerPrefs `PokiClash.Lang`. Chưa chọn thì máy tiếng Việt dùng tiếng Việt, máy khác dùng tiếng Anh. Trong Editor chưa chọn thì là tiếng Việt.
  - Đổi ở Sổ tay: dòng "Ngôn ngữ", nút ghi "Tiếng Việt" / "English".
  - Hoặc menu `PokiClash/Ngôn ngữ`.
  - Đổi lúc chạy (`App.SetLanguage`): dựng lại dữ liệu, dịch lại khung app, nạp lại màn đang mở.
- **Chữ trong code:** `Loc.T("Mở ngay")`, `Loc.F("Ải {0} · {1}", idx, name)`. Bản dịch được đổi thứ tự `{1} {0}`.
  - Thiếu bản dịch thì giữ tiếng Việt. Bản dev ghi lại; xem bằng menu `PokiClash/Ngôn ngữ/Ghi chuỗi chưa dịch gặp lúc chạy`.
- **Chữ có sẵn trong prefab/scene:** `LocService.Tree` dịch mọi TMP_Text có chữ khớp bảng. Gọi ở `Ui.Spawn`, `SceneRouter` (scene vừa nạp, trước `Enter`), `App` (khung app, màn tải), `BootTitle`. Không phải gắn component vào prefab.
- **Tên trong dữ liệu:**
  - `GameDb.Build` thay tướng, thẻ, đảo, ải bằng bản sao đã dịch (`Core/LocData.cs`). Không sửa ScriptableObject: Play trong Editor sẽ ghi đè asset.
  - Tên trong cấu hình cân bằng dùng thuộc tính `Name` / `Desc` (công trình, ô lát, tầng Hang, bộ tiềm năng, chỗ trang trại, gói).
- **Mô tả thẻ:** `Core/CardTextEn.cs` viết câu tiếng Anh riêng (cùng luật, cùng số). `CardText` rẽ sang khi `Loc.IsEn`; nhánh tiếng Việt giữ nguyên để khớp golden.

- **Ảnh có chữ:** chỉ có ghi chú bút chì ở vùng boss (`Islands/Co/trung_ghi_*`, 45 ảnh).
  - Bản tiếng Anh `trung_ghi_*_en.png` vẽ bằng `ArtGen/Islands/ve_trung_en.py`, cùng hàm vẽ với bản Việt.
  - `ZoneSceneEggs` chọn ảnh `<tên>_<mã ngôn ngữ>`, thiếu thì dùng bản Việt.
  - Gắn ảnh vào `Screens/Zone` bằng menu `PokiClash/Ngôn ngữ/Gắn ghi chú tiếng Anh vào màn đảo`.

## Thêm chữ mới

1. **Trong code:** bọc `Loc.T` / `Loc.F`.
   - Không bọc trong khởi tạo `static readonly` hay `const`: chúng chạy trước khi chọn ngôn ngữ. Giữ chuỗi Việt trong mảng, rồi bọc ở chỗ dùng (`Loc.T(Tips[i])`).
   - Không bọc trong tham số mặc định hay attribute.
2. **Tên GameObject** mà tour thử tìm theo (`nut_...`) giữ chữ Việt; chỉ dịch chữ hiện ra.
3. **Thêm bản dịch** vào file json tương ứng.
4. **Chạy `LocTests`.** Test kiểm:
   - luật tra;
   - chỗ điền khớp nhau;
   - đủ bản dịch cho chuỗi trong code, chữ prefab, tên dữ liệu;
   - mô tả thẻ tiếng Anh không sót chữ Việt.

## Không dịch

- Log, thông báo kiểm dữ liệu (`Validate`), Tooltip/Header, menu Editor.
- Bảng dev ở Sổ tay (`App/Dev`).
- Bản thử BanThu.
- Bản web.
