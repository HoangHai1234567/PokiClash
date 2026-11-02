## Context

Bản web giữ tiến trình trong `Web/src/core/progression.ts`:
- `expToNext(L) = round(40 × L^1.35)`, cấp tối đa 30;
- `CARD_REQ = [0, 2, 4, 8, 15]`;
- `STAR_CARDS = [0, 0, 5, 8, 11, 15]`, `STAR_LEVEL = [0, 1, 2, 5, 9, 14]`;
- `addShards` (đã có tướng thì đổi thành bản sao thẻ ngẫu nhiên);
- `rollCardDrop` (rương ra bản sao thẻ riêng của tướng đã có, lùi độ hiếm nếu không có).

Chỉ số ở `heroStats` trong `battle.ts`:
```
m    = sức theo độ hiếm × (1 + 0,1 × (cấp − 1)) × (1 + 0,08 × (sao − 1))
Máu  = 600 × √(máu gốc / tb) × m
Công = 180 × √(max(công, công phép) / tb) × m
Thủ  = 55 × √(tb(thủ, thủ phép) / tb) × m
Tốc  = tốc gốc + cấp
```
`tb` là trung bình của ba giá trị (công, thủ, máu) của chính tướng đó.

## Goals / Non-Goals

**Goals:**
- Giữ đúng các con số đã chạy thử trên web; đổi số ở một chỗ (`BalanceConfig`).
- Mỗi tài nguyên có chỗ tiêu rõ ràng:
  - EXP để lên cấp;
  - bản sao để nâng thẻ, từ đó tiến hóa;
  - mảnh để mở tướng.
- Màn Tướng cho thấy ngay việc có thể làm (chấm đỏ, nút nhấp nháy).

**Non-Goals:**
- Cấp riêng cho từng tướng (GDD: cấp người chơi là cấp tướng).
- Đổi hình khi tiến hóa (dòng tiến hóa aola đã tách thành tướng riêng).
- Đá tiềm năng, huy hiệu (change riêng).

## Decisions

### Một nguồn chỉ số

`HeroStats.Compute(hero, level, star, boss, mods)`:
- `mods` là phần cộng thêm từ side meta (huy hiệu hệ, đá tiềm năng), mặc định rỗng;
- trận gọi hàm này khi dựng đội, màn Tướng gọi hàm này khi hiện chỉ số;
- side meta chỉ thêm `mods`, không sửa công thức.

### Tiến hóa là bấm nút, không tự động

Đủ điều kiện thì nút "Tiến hóa" nhấp nháy; bấm mới lên sao, có hoạt cảnh tướng chạy clip chiêu. Người chơi thấy khoảnh khắc mạnh lên.
- **Phương án khác: tự lên sao khi đủ.** Bỏ, vì mất khoảnh khắc thưởng.

### Xem clip trong hộp chi tiết

- Dáng đứng: cỡ 70% ô xem, chân sát đáy.
- Clip đánh và chiêu: giữ cỡ dáng đứng (60%), neo ở 32% chiều ngang. Vệt đòn bay xa thì bị cắt ở mép ô, không thu nhỏ cả tướng.

Như bản web.

### Mảnh thừa thành bản sao

Mảnh của tướng đã có: mỗi mảnh thành 1 bản sao của một trong 3 thẻ riêng của tướng đó, chọn ngẫu nhiên. Hộp thưởng ghi "Đã có tướng: đổi thành n bản sao thẻ".

## Risks / Trade-offs

- **[Tướng Thường quá yếu ở đảo sau]:** sao và cấp thẻ bù, kèm huy hiệu và đá tiềm năng. Theo dõi bằng công cụ cân bằng.
- **[Người chơi không hiểu "thẻ để tiến hóa"]:** mục tiến hóa ghi rõ "Tổng cấp 3 thẻ x/y · Cấp người chơi a/b"; thẻ có thanh bản sao.
- **[Rương ra thẻ của tướng ít dùng]:** cân nhắc sau: ưu tiên tướng trong đội.

## Open Questions

- Rương có nên ưu tiên ra thẻ của tướng đang trong đội không? Bản web đang chia đều cho mọi tướng đã có.
- Có cần "thẻ vạn năng" (bản sao dùng cho thẻ nào cũng được) để bớt xui không?
