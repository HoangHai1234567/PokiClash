## Why

GDD gốc, Side Meta: "Farm ball: có thể có 1 màn trang trại, người chơi có thể deploy 8 con tướng xuống để chúng có thể trồng rau, chăn vịt,… 1 dạng afk lấy được ball. Tướng càng mạnh thì năng suất càng cao, thời lượng làm việc càng lâu (… làm việc được trong n giờ, hết thời gian thì chúng sẽ ngồi nghỉ không làm nữa, phải vào đổi tướng khác cho tướng kia nghỉ ngơi (nghỉ nhanh tầm 15-30 phút hoặc 1 tiếng), sức này không liên quan gì đến việc cho tướng đi cày ải)."

Trang trại cho người chơi lý do quay lại vài lần mỗi ngày (đổi ca, thu hoạch), và cho tướng ít dùng trong trận một việc để làm. Bản web chưa có phần này.

## What Changes

- **Trang trại:** công trình ở rìa làng trên sảnh, scene riêng với ảnh đảo trang trại. Mở khi người chơi có từ 3 tướng (thường là sau ải 6 Đảo Thủy).
- **8 chỗ làm,** mỗi chỗ hợp một hệ:

  | Chỗ | Số lượng | Hệ hợp |
  |---|---|---|
  | Ruộng rau | 2 | Thổ |
  | Ao vịt | 2 | Thủy |
  | Vườn cây | 2 | Mộc |
  | Lò bánh | 1 | Hỏa |
  | Xưởng nông cụ | 1 | Kim |

  Lúc mở có 3 chỗ; mở thêm theo cấp người chơi (8, 11, 14, 17, 20).
- **Đưa tướng vào chỗ làm:**
  - năng suất (bi mỗi giờ) theo độ hiếm, cấp, sao, nhân 1,25 nếu đúng hệ hợp;
  - thời lượng làm việc 2–6 giờ theo độ hiếm và sao;
  - hết giờ thì tướng ngồi nghỉ tại chỗ, không làm nữa;
  - phải đổi tướng khác vào; tướng vừa rút ra nghỉ 15–60 phút rồi mới vào lại được.
- **Sức làm của trang trại tách khỏi trận:** tướng đang làm vẫn ra trận được.
- **Bi tích ở mỗi chỗ,** giữ tối đa 12 giờ sản lượng. Nút "Thu hoạch" lấy hết; nút "Tự xếp" đưa tướng hợp nhất vào chỗ trống.
- **Quảng cáo** "Năng suất ×2 trong 1 giờ" (qua `add-monetization-hooks`).

## Capabilities

### New Capabilities

- `hero-farm`: mở trang trại, chỗ làm và hệ hợp, năng suất và thời lượng theo sức tướng, nghỉ ngơi, thu hoạch, tự xếp, tách khỏi trận, scene trang trại.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code:** `Core/SideMeta/Farm` (tính năng suất, đồng hồ làm và nghỉ, kho từng chỗ, chống chỉnh giờ dùng chung với AFK); `Game/Farm`.
- **Scene:** `Farm.unity`. Sảnh thêm công trình Trang trại.
- **Lưu:** `farm.spots[8] = { tướng, lúc bắt đầu, sức còn, bi tích }`, `farm.rest[tướng] = hết nghỉ lúc`.
- **Dữ liệu:** `BalanceConfig.farm`.
- **Ảnh:**
  - ảnh đảo trang trại có 8 chỗ (`ArtGen/SideMeta`);
  - icon 5 loại chỗ làm (`ArtGen/Icons`);
  - công trình Trang trại trên sảnh (`ArtGen/Hub`).
- **Phụ thuộc:** `add-hero-roster`, `add-world-islands`. Dùng đồng hồ chống chỉnh giờ của `add-afk-rewards`.
