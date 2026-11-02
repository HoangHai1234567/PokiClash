## Why

GDD gốc, Side Meta: "Đánh boss để nhận huy hiệu nâng cấp tộc hệ (học từ clash of critters): Đánh boss (theo hệ tộc) Nếu thắng 5 hoặc 10 ải (tùy tiến độ) sẽ nhận được huy hiệu hệ đó. Huy hiệu sẽ tăng 5% sức mạnh cho các tướng hệ đó. Huy hiệu về sau càng mạnh thì ải càng khó." Thêm: phải tự chơi, không AFK.

Huy hiệu cho người chơi một đích nuôi theo hệ, và lý do nuôi nhiều tướng cùng hệ. Bản web chưa có phần này.

## What Changes

- **Đền Huy Hiệu:** công trình ở rìa làng trên sảnh, scene riêng. Mở khi thắng boss Đảo Thủy (ải 8) lần đầu.
- **5 dãy huy hiệu** (một dãy mỗi hệ), mỗi dãy 5 bậc: Đồng, Bạc, Vàng, Ngọc, Kim Cương.
  - Dãy hệ X mở khi người chơi thắng mini boss (ải 4) của Đảo X.
- **Thử thách bậc k:**
  - chuỗi trận boss hệ X: 5 trận với bậc 1–2, 10 trận với bậc 3–5;
  - đánh lần lượt, thua thì đánh lại trận đó, không mất tiến độ;
  - không AFK, không quét nhanh;
  - cấp địch tăng theo bậc và theo trận trong chuỗi.
- **Thưởng:**
  - mỗi trận thắng: bi;
  - xong bậc: huy hiệu bậc đó kèm một rương.
- **Sức mạnh huy hiệu:** tướng hệ X được +5% / +8% / +12% / +16% / +20% Máu, Công, Thủ theo bậc cao nhất (không cộng dồn các bậc).
- **Hiển thị:** huy hiệu cạnh nhãn hệ ở thẻ tướng và hộp chi tiết; chỉ số trong hộp chi tiết đã gồm phần huy hiệu.

## Capabilities

### New Capabilities

- `element-badges`: Đền Huy Hiệu, mở dãy theo hệ, thử thách nhiều trận theo bậc, thưởng, phần cộng chỉ số cho tướng cùng hệ, hiển thị.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code:** `Core/SideMeta/Badges` (luật, sinh địch theo bậc, phần cộng `mods` vào `HeroStats`); `Game/Badges` (scene, chuỗi trận).
- **Scene:** `Badges.unity`. Sảnh thêm công trình Đền Huy Hiệu.
- **Lưu:** `badges[hệ] = { bậc đã đạt, trận đã thắng trong bậc đang đánh }`.
- **Dữ liệu:** `BalanceConfig.badges` (số trận mỗi bậc, phần cộng, công thức cấp địch, thưởng).
- **Ảnh:**
  - 5 hệ × 5 bậc huy hiệu (`ArtGen/SideMeta`, sheet huy hiệu);
  - ảnh nền đền (`ArtGen/SideMeta`);
  - công trình đền trên sảnh (`ArtGen/Hub`).
- **Phụ thuộc:** `add-card-battle`, `add-hero-roster`, `add-world-islands`.
