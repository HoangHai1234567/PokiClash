## Why

Người dùng chốt danh sách 40 tướng (`GD_Claude/13_DanhSachTuong.md`, 2026-10-31 và 2026-11-01):
- 8 tướng mỗi hệ, mỗi tướng là một dòng tiến hóa của aola;
- lên sao thì đổi hình;
- Giọt Sương thay Tiểu Y làm tướng khởi đầu.

Hình aola của cả 79 dạng đã xuất xong (2026-11-02), nhưng dữ liệu game vẫn là 11 tướng cũ. Ngày 2026-11-02 người dùng chọn hướng "đủ 40 tướng, thẻ tạm":
- thêm đủ 40 tướng vào dữ liệu;
- tướng mới tạm mượn bộ 3 thẻ của tướng cùng hệ;
- ải giữ khung;
- thẻ riêng của từng tướng thiết kế sau.

GDD gốc: "Các tướng sẽ có 1-3 thẻ nội tại riêng biệt" (phần thẻ riêng chưa đáp ứng ở change này, xem Non-Goals trong design).

## What Changes

- **40 tướng thay 11 tướng:**
  - bỏ `gia_bi` và `su_gia`;
  - `y_trach` thành dạng 2 của `tieu_y`;
  - `van_quan`, `hac_duc` thành dạng 2, 3 của `lam_quan`, và Lam Quân chuyển từ Kim sang Thủy, Sử thi;
  - thêm 31 tướng mới theo `GD_Claude/13`.
- **Dạng tiến hóa theo sao:**
  - mỗi tướng có danh sách dạng (tên, hình aola, cỡ trên sân);
  - mốc đổi dạng: dòng 2 dạng đổi ở sao 3, dòng 3 dạng đổi ở sao 3 và sao 5 (khởi điểm, chỉnh được);
  - địch lấy dạng theo sao của nó.
- **Tướng khởi đầu:** Giọt Sương (`giot_suong`) thay Tiểu Y.
- **Chỉ số:** tướng mới lấy 6 chỉ số aola của dạng 1, như 11 tướng cũ.
- **Thẻ tạm:** mỗi tướng mới chép bộ 3 thẻ của một tướng cũ cùng hệ, độ hiếm gần nhất (id mới, tên giữ nguyên).
- **Ải:** giữ tên, loại, cấp, lượng rơi của 40 ải. Tướng bị bỏ hoặc chuyển hệ được thay bằng tướng mới cùng hệ, cùng độ hiếm. Ải 6 Đảo Thủy tặng Nụ Hoa thay Gia Bỉ.
- **Bản lưu v4:**
  - gộp `y_trach` vào `tieu_y`, gộp `van_quan`, `hac_duc` vào `lam_quan`;
  - đổi `gia_bi` thành `nu_hoa`, `su_gia` thành `de_hoa`.
- **BREAKING:** id tướng trong dữ liệu, golden và test đổi; bản lưu v3 tự nâng lên v4.

## Capabilities

### New Capabilities

<!-- Không có. -->

### Modified Capabilities

- `hero-roster`: danh sách 40 tướng, dạng tiến hóa theo sao, tướng khởi đầu, tướng tặng.
- `hero-cards`: thẻ riêng tạm mượn của tướng cùng hệ.

## Impact

- **Web (nguồn số liệu):**
  - `src/core/data/heroes.ts`, `cards.ts`, `stages.ts`, `config.ts`;
  - `src/core/types.ts`, `progression.ts` (dạng theo sao, bản lưu v4);
  - phần hiển thị dùng hình theo dạng.
- **Unity:**
  - `Core/Types.cs`, `Core/GameData.cs` (đọc dạng), `Core/SaveData.cs` (nâng bản lưu);
  - `Game/Heroes` (`HeroPortrait`, `HeroViewer`, `AolaSticker`), `Game/Battle/StageView` (hình theo sao);
  - `02 Data` (JSON, Golden, asset nhập lại);
  - test và `Editor/PlayTour` dùng id cũ.
- **Hình:** `reskin/pokiclash_lines.json` (AolaRipper) là bảng tướng → dạng. Hình chỉ nạp trong Editor lúc Play và bản dev.
- **Phụ thuộc:** `add-hero-roster`, `add-card-battle`, `add-world-islands`, `add-element-badges`, `add-potential-stones`. Làm sau `convert-to-prefabs`, không đổi prefab.
