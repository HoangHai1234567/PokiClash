## Context

Clash of Critters có thử thách boss theo loại để lên "huy hiệu" cho cả loại sinh vật. GDD muốn bản tương tự theo Ngũ hành:
- thắng chuỗi 5 hoặc 10 ải boss thì có huy hiệu, +5% sức mạnh cho tướng cùng hệ;
- bậc sau mạnh hơn và khó hơn;
- phải tự chơi.

Trận dùng lại `add-card-battle`, chỉ số dùng `HeroStats.Compute(..., mods)` của `add-hero-roster`.

## Goals / Non-Goals

**Goals:**
- Đích dài hạn theo hệ, khuyến khích nuôi đủ hệ.
- Dùng lại trận và dữ liệu tướng, không thêm luật trận mới.
- Độ khó bậc sau rõ ràng hơn bậc trước.

**Non-Goals:**
- Huy hiệu cộng cho hệ khác, hay huy hiệu đổi luật trận.
- Bảng xếp hạng.

## Decisions

### Chuỗi trận sinh từ công thức, không viết tay 125 trận

`L0` là cận dưới cấp đề nghị của Đảo X. Trận i của bậc k (i từ 1):
- **Cấp địch** = `L0 + 3·(k − 1) + floor(i / 2)`.
- **Đội địch:**
  - trận lẻ: 1 tướng boss hệ X;
  - trận chẵn: 2 tướng hệ X, một boss;
  - trận cuối của bậc: 3 tướng, boss là tướng hiếm nhất của hệ X.
- **Tướng hệ X** lấy theo vòng trong danh sách tướng của hệ đó.
- **Hạt giống** của trận cố định theo `(hệ, bậc, i)`, để thua đánh lại vẫn gặp cùng đội.

### Phần cộng huy hiệu

`mods.hp = mods.atk = mods.def = BADGE[bậc]` (0,05 / 0,08 / 0,12 / 0,16 / 0,20) cho tướng hệ X. Áp trong `HeroStats.Compute`, nên trận, màn Tướng và công cụ cân bằng đều thấy.

### Thưởng

- Mỗi trận thắng: `5 + 2·k` bi.
- Xong bậc k: rương bạc (k = 1, 2) hoặc rương vàng (k ≥ 3), mở bằng hộp rương của máy bi, mức thưởng ×1.

## Risks / Trade-offs

- **[Huy hiệu làm đảo dễ quá]:** +20% chỉ cho một hệ, và chỉ ở bậc 5 (cần 40 trận). Công cụ cân bằng chạy đảo với và không có huy hiệu.
- **[10 trận một bậc nhàm]:** đội địch xoay vòng; trận cuối có 3 tướng; ghi tiến độ "7/10" để thấy đích.

## Open Questions

- Mở đền sau boss Đảo Thủy có sớm quá không? Phương án khác: mở ở cấp 8.
- Huy hiệu có cho thêm hiệu ứng nhỏ trong trận (ví dụ +5 nộ đầu trận cho tướng cùng hệ) không?
