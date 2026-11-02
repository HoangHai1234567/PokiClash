## Why

GDD gốc: "Đánh ải nhận ball… lên level pet ⇒ đi săn các quái cao cấp hơn. Những ải nào đánh boss (boss to hoặc các mini boss) có cơ hội nhận mảnh tướng."

Sau bản web đầu, chủ dự án chốt thêm:
- phần ải là **một đảo lớn chia rõ từng hệ**;
- không khoá đảo nào, nhưng đảo sau mạnh hơn hẳn;
- người chơi được tặng một tướng Thủy nên bắt đầu ở đảo Thủy;
- chạm vùng thì sang scene đảo của hệ đó, to hơn;
- bố cục học Clash of Critters.

Bản web đã làm xong bố cục này và được duyệt ("layout khá tốt rồi"). Change này đưa nó vào Unity.

## What Changes

- **Scene Hub (sảnh):**
  - ảnh đảo lớn phủ kín màn, 5 vùng hệ;
  - bảng tên mỗi vùng: icon hệ, tên đảo, độ khó so với cấp người chơi, "Cấp a–b · n/8 ải", thanh tiến độ;
  - mũi tên nhún chỉ đảo nên đánh;
  - làng máy bi ở giữa; mây trôi;
  - hàng nút tròn dưới: Tướng, Sổ thẻ, Máy Bi (to nhất), Đánh tiếp, Sổ tay;
  - chỗ đặt công trình side meta (Trang trại, Đền huy hiệu, Hang tiềm năng) khi các change đó xong.
- **Scene Zone (đảo hệ):**
  - ảnh đảo hệ phóng to 1,27 lần, cuộn dọc, tự cuộn tới ải đang đánh;
  - 8 ải dọc đường mòn (ải 4 mini boss, ải 8 boss), mở lần lượt trong đảo; đường đã đi vẽ nét chấm vàng; tướng đội trưởng đứng ở ải hiện tại;
  - khung trên: hệ, cấp đề nghị, độ khó, thanh tiến độ có 2 rương mốc, câu gợi ý hệ khắc;
  - khung dưới: ải tiếp theo, địch, thưởng, nút "Đánh!".
- **Hộp chuẩn bị trận:**
  - đối thủ (sticker, hệ, cấp, boss), cảnh báo khi địch mạnh hơn nhiều;
  - thưởng (bi, mảnh kèm tỉ lệ, tướng tặng);
  - chọn đội 3 tướng có mũi tên khắc hệ; nút "Xuất trận!".
- **5 đảo × 8 ải:**
  - thứ tự gợi ý Thủy (cấp 1–7) → Hỏa (6–12) → Kim (11–17) → Mộc (16–22) → Thổ (21–28);
  - mỗi đảo rơi tướng hệ của mình, là hệ khắc đảo kế tiếp;
  - Đảo Thủy tặng Võ Sư (ải 3) và Gia Bỉ (ải 6).
- **Thưởng ải:**
  - bi tăng theo đảo, có thưởng lần đầu;
  - mảnh tướng: đánh lại giảm tỉ lệ (100% còn 50%, còn lại ×0,8);
  - rương mốc ở 4 và 8 ải (bi và bản sao thẻ).
- **Màn giới thiệu lần đầu:** 4 ô (Năm đảo năm hệ, Đánh bằng thẻ, Thắng nhận bi, Thả bi vào máy).

## Capabilities

### New Capabilities

- `world-map`: scene sảnh đảo lớn, bảng tên vùng và độ khó, đảo gợi ý, làng máy bi, hàng nút chính, chỗ đặt công trình side meta, màn giới thiệu.
- `zone-stages`: 5 đảo hệ và 40 ải, mở ải trong đảo, scene đảo hệ cuộn dọc, rương mốc, hộp chuẩn bị trận, thưởng ải (bi, mảnh, tướng tặng), đánh lại.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code:** `Game/World` (Hub), `Game/Zone` (đảo hệ, chuẩn bị trận); `Core/Progression` thêm phần đảo (`zones`, `zoneChests`, `StageBalls`, `WinStage`, `NextStage`, `ClaimZoneChest`).
- **Scene:** `Hub.unity`, `Zone.unity`.
- **Dữ liệu:** `ZoneDb` gồm 5 đảo (cấp đề nghị, màu, ảnh, toạ độ vùng trên đảo lớn, toạ độ 8 ải) và 40 ải (địch, rơi, tặng).
- **Ảnh:** `world`, `zone_thuy`, `zone_hoa`, `zone_kim` đã gen bằng Canva; `zone_moc`, `zone_tho` chưa có (gói `ArtGen/Islands`). Thiếu thì dùng bản đồ nét tay.
- **Phụ thuộc:** `setup-unity-foundation`, `add-card-battle`, `add-hero-roster`.
