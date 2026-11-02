## Context

Bản web có ba công cụ:
- `scripts/sim.ts` (máy bi, trận theo đảo);
- `core/sim.ts` (chạy một trận máy tự chơi);
- mục "Máy tự chơi" và "Chỉnh số" trong Sổ tay.

Bản thử Unity cũ (BanThu) có ghi trận vào `tran.csv` và máy tự chơi qua menu.

## Goals / Non-Goals

**Goals:**
- Chỉnh một hệ số, chạy lại, thấy tỉ lệ thắng mọi ải trong vài giây.
- Người thử tua tới bất kỳ phần nào của game trong một phút.
- Bản phát hành không chứa công cụ.

**Non-Goals:**
- Analytics từ người chơi thật (để sau, cần backend).
- Máy chơi giỏi như người (máy chỉ để so tương đối).

## Decisions

### Chạy trong Editor, không cần Play

Cửa sổ Editor gọi thẳng `Core` (C# thuần). 40 ải × 6 mức cấp × 60 trận khoảng 14.400 trận; trên web mất khoảng 3 giây, trong Unity chạy đồng bộ có thanh tiến độ.

### Mô phỏng tiến độ

Mỗi kiểu người chơi có:
- số lần vào game mỗi ngày;
- số trận mỗi lần;
- có xem quảng cáo không.

Mỗi ngày mô phỏng:
1. đánh ải kế tiếp của đảo gợi ý (tỉ lệ thắng lấy từ bảng máy tự chơi, cộng một mức "người giỏi hơn máy" chỉnh được, mặc định +15%);
2. nhận AFK, thu hoạch trang trại;
3. thả hết bi;
4. nâng thẻ, tiến hóa khi đủ.

Ra cấp theo ngày và ngày chinh phục từng đảo.

### Bảng thử và chỉnh số chỉ trong bản dev

Bọc `#if POKICLASH_DEV`. Chỉnh số sửa `BalanceConfig` lúc chạy, không ghi vào asset; "Về số gốc" nạp lại asset.

## Risks / Trade-offs

- **[Máy chơi kém hơn người nên số lệch]:** có hệ số "người giỏi hơn máy" và ghi trận thật để so; chỉnh hệ số theo số liệu chơi thử.
- **[Quên bọc bản dev, công cụ lọt vào bản phát hành]:** bước kiểm tra trước build tìm các lớp công cụ trong bản phát hành.

## Open Questions

- Kiểu người chơi mặc định: chăm (6 lần/ngày, 5 trận), vừa (3, 3), ít (1, 2)?
