## Why

GDD gốc có ba ý về nuôi tướng:
- "Các tướng sẽ có 1-3 thẻ nội tại riêng biệt… Các thẻ này sẽ có độ hiếm thu thập được khác nhau. Khi unlock tướng thì sẽ unlock các thẻ của nó ở level 1, người chơi có thể nâng cấp sức mạnh thẻ bằng cách thu thập chúng."
- "Cấp của người chơi sẽ chính là cấp của tướng… kinh nghiệm là để nâng tướng còn thẻ là để tiến hóa tướng."
- "Những ải nào đánh boss… có cơ hội nhận mảnh tướng."

Bản web đã làm và chơi thử các luật này: 11 tướng, cấp chung, thẻ riêng lên cấp bằng bản sao, tiến hóa sao theo tổng cấp thẻ, mảnh mở tướng. Change này đưa chúng vào Unity, kèm scene Tướng và Sổ thẻ.

## What Changes

- **11 tướng.** Hệ, độ hiếm, 6 chỉ số gốc. Chỉ số tính theo độ hiếm, cấp và sao (công thức của bản web).
- **Cấp người chơi** 1–30 là cấp của mọi tướng. EXP đến từ máy bi và rương.
- **Mảnh mở tướng:**
  - cần 10/20/30/50 mảnh theo độ hiếm;
  - mảnh của tướng đã có đổi thành bản sao thẻ;
  - người mới chỉ có Tiểu Y; Đảo Thủy tặng Võ Sư và Gia Bỉ.
- **Thẻ riêng:** mỗi tướng 3 thẻ (Chiêu, Tuyệt kỹ, Bị động), có độ hiếm. Lên cấp 2–5 bằng 2/4/8/15 bản sao, mỗi cấp +15% số.
- **Tiến hóa sao:** sao 2–5 cần tổng cấp 3 thẻ (5/8/11/15) và cấp người chơi (2/5/9/14), mỗi sao +8% chỉ số.
- **Thẻ chung:** 23 thẻ, mở dần theo cấp người chơi, không lên cấp.
- **Scene Tướng:**
  - lưới 11 tướng; tướng chưa có hiện bóng chì kèm thanh mảnh;
  - chấm đỏ khi có thẻ nâng được hoặc tiến hóa được;
  - hộp chi tiết: xem 4 clip, chỉ số theo cấp, 3 thẻ có thanh bản sao và nút nâng, mục tiến hóa, nút vào/ra đội, nơi rơi mảnh.
- **Scene Sổ thẻ:** cách xếp thẻ, trọng số độ hiếm, 23 thẻ chung (khoá ghi "Mở ở cấp n").

## Capabilities

### New Capabilities

- `hero-roster`: danh sách tướng, chỉ số, cấp chung, EXP, mảnh và mở tướng, tướng khởi đầu và tướng tặng, đội hình, tiến hóa sao, scene Tướng và hộp chi tiết.
- `hero-cards`: thẻ riêng (Chiêu, Tuyệt kỹ, Bị động) và cách lên cấp bằng bản sao, nguồn bản sao, thẻ chung mở theo cấp, scene Sổ thẻ.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code:**
  - `Core/Progression` (chép `progression.ts` phần cấp, thẻ, sao, mảnh, đội);
  - `Game/Heroes` (scene Tướng, hộp chi tiết, xem clip);
  - `Game/Cards` (scene Sổ thẻ).
- **Scene:** `Heroes.unity`, `Cards.unity`.
- **Dữ liệu:** `HeroDb`, `CardDb`, `BalanceConfig` (bảng EXP, bản sao, sao).
- **Ảnh:** khung thẻ theo độ hiếm, icon thẻ, khung thẻ tướng (`ArtGen/UIKit`, `ArtGen/Icons`). Hình tướng: aola trong bản dev, hình giữ chỗ trong bản phát hành.
- **Phụ thuộc:** `setup-unity-foundation`. Dùng chung với `add-card-battle` (chỉ số, cấp thẻ vào trận).
