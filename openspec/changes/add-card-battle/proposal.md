## Why

Trận đánh là lõi của game. GDD gốc mục "Gameplay chính":
- mỗi bên 1–3 tướng;
- theo lượt, đầu lượt được đổi tướng;
- chọn 1 trong 3 thẻ, 5 lần;
- thẻ riêng của tướng: chiêu tốn mana, tuyệt kỹ cần đầy nộ và mana, bị động;
- cuối lượt thẻ chạy lần lượt rồi đánh thường, hoặc ra tuyệt kỹ thay đòn thường;
- trận kết thúc khi một bên hết tướng và không còn hồi sinh.

Bản web đã chạy thử và cân số các luật này. Change này đưa trận vào Unity, giữ đúng luật, máy chơi và cách trình bày đã duyệt.

## What Changes

- Chép `Web/src/core/battle.ts` và `ai.ts` sang C#: luật trận, sự kiện kèm ảnh chụp số liệu, máy chơi.
- **Luật** (theo bản web):
  - lượt luân phiên, người chơi luôn đi trước mỗi hiệp;
  - đổi tướng đầu lượt; 5 lần chọn 1 trong 3 thẻ chung;
  - chiêu và tuyệt kỹ xen vào hàng thẻ, không tốn lần chọn; tuyệt kỹ thay cú đánh thường;
  - mana và nộ; Ngũ hành khắc ×1,5 / ×0,75;
  - chí mạng, khiên, hút máu, né;
  - trạng thái bỏng, hồi phục, choáng, né; bị động theo điều kiện; tướng gục thì thay.
- **Mới so với bản web:** hiệu ứng **hồi sinh** (GDD: "lỡ có thẻ hồi sinh skill của con nào đó"). Bị động "Phật Tâm" của Đại Sư Cà Sa đổi thành "lần đầu gục: hồi sinh với 35% máu". Trận chỉ kết thúc khi một bên hết tướng và không còn lần hồi sinh nào.
- **Máy chơi:** chấm điểm thẻ theo tình huống; ở các ải đầu chọn kém hơn; dùng chung cho địch và nút "Tự chơi".
- **Màn trận Unity** (theo bản web):
  - màn VS;
  - sân đấu: địch trên-trái, phe mình dưới-phải, tướng dạng sticker;
  - bảng thông tin hai bên, hàng thẻ 5 ô và ô đòn kết, 3 thẻ để chọn, nút Chiêu và Tuyệt kỹ, chân dung đội để đổi tướng;
  - hoạt cảnh thẻ chạy, đòn đánh nắn hướng lao, chữ tượng thanh, dòng tin chữ nổi;
  - tốc độ ×1/×2/×3, tự chơi, tạm dừng, hộp kết quả.

## Capabilities

### New Capabilities

- `card-battle`: luật trận: đội hình, hiệp và lượt, đổi tướng, chọn thẻ, chiêu, tuyệt kỹ, tài nguyên, sát thương, hiệu ứng và thời hạn, trạng thái, bị động, gục và thay, hồi sinh, kết thúc trận, tái lập theo hạt giống.
- `battle-ai`: máy chọn thẻ, dùng chiêu và tuyệt kỹ, đổi tướng, chọn tướng thay; độ khéo theo ải; tự chơi cho người chơi.
- `battle-presentation`: bố cục và hoạt cảnh màn trận, phát lại sự kiện, hộp kết quả.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code:**
  - `Assets/01 Script/Core/Battle/` (luật, sự kiện, máy chơi; C# thuần);
  - `Assets/01 Script/Game/Battle/` (sân đấu, phát sự kiện, hoạt cảnh);
  - `Assets/01 Script/UI/Battle/`.
- **Scene:** `Battle.unity`.
- **Dữ liệu:** `CardDb` (23 thẻ chung, 33 thẻ riêng); đổi bị động Phật Tâm. Đổi cả ở `Web/src/core/data/cards.ts` để hai bản cùng luật.
- **Ảnh:**
  - nền trận theo 5 hệ (`ArtGen/BattleBG`);
  - icon thẻ (`ArtGen/Icons`);
  - khung thẻ (`ArtGen/UIKit`).

  Chưa có thì dùng nền vẽ bằng code và icon SVG của bản web.
- **Phụ thuộc:** `setup-unity-foundation`. Change `add-hero-roster` cung cấp chỉ số tướng, cấp thẻ, sao; trước khi có thì trận dùng cấp và sao truyền vào trực tiếp.
