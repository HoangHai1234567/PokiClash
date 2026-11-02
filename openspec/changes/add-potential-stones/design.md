## Context

GDD muốn đá tiềm năng từ rương máy bi, 4 tiềm năng mỗi tướng, khai phá tốn đá, tiềm năng hiếm ra ít, và một nhánh đánh boss để cày đá (phải chơi).

Chỉ số tướng đi qua `HeroStats.Compute(..., mods)`. Đầu trận dựng `Fighter` từ `Member`.

## Goals / Non-Goals

**Goals:**
- Trục nuôi có may rủi nhẹ nhưng không làm hỏng cân bằng (tổng tối đa có giới hạn).
- Người chơi không mất dòng tốt vì xui: khoá ô và chọn "Giữ cũ".
- Nhánh cày đá phải tự chơi, có giới hạn mỗi ngày.

**Non-Goals:**
- Bán đá bằng tiền thật.
- Tiềm năng đổi luật trận (chỉ cộng chỉ số và tài nguyên đầu trận).

## Decisions

### Bảng dòng tiềm năng

| Loại | Thường | Khá | Hiếm | Sử thi | Huyền thoại |
|---|---|---|---|---|---|
| Công % | 3 | 5 | 8 | 12 | 16 |
| Thủ % | 3 | 5 | 8 | 12 | 16 |
| Máu % | 3 | 5 | 8 | 12 | 16 |
| Tốc | 2 | 4 | 6 | 9 | 12 |
| Chí mạng % | 2 | 3 | 5 | 7 | 10 |
| Hút máu % (đánh thường) | 2 | 3 | 5 | 7 | 10 |
| Mana đầu trận | 5 | 10 | 15 | 20 | 30 |
| Nộ đầu trận | 5 | 10 | 15 | 20 | 30 |

- Mỗi ô quay một loại (8 loại đều nhau), rồi một độ hiếm (55 / 28 / 12 / 4,5 / 0,5).
- Hai ô có thể cùng loại; khi đó cộng dồn.
- Phần %: cộng vào `mods`. Phần còn lại: hiệu ứng đầu trận (chí mạng và hút máu là buff "cả trận").

### Giá khai phá

- Mỗi lần: `số ô quay` đá.
- Mỗi ô khoá: +2 đá.
- Tối đa khoá 2 ô.

Quay xong thì hiện cặp cũ/mới; người chơi chọn "Giữ mới" hoặc "Giữ cũ". Đá đã tiêu không hoàn.

### Hang Tiềm Năng

| Tầng | Đề nghị cấp | Đá thưởng |
|---|---|---|
| Dễ | 6 | 2 |
| Thường | 12 | 3 |
| Khó | 18 | 5 |
| Ác mộng | 24 | 8 |

- Mỗi lần vào: một trận với 1 boss và 1 tướng phụ. Hệ của boss theo thứ trong tuần (Thứ Hai Kim, Thứ Ba Mộc, …; Chủ nhật chọn được), để người chơi đổi đội theo ngày.
- Mỗi ngày 3 lượt, chỉ trừ khi thắng; quảng cáo thêm 1 lượt (`add-monetization-hooks`).

### Bảng rương máy bi đổi

- Rương bạc thêm 8% "1–2 đá".
- Rương vàng thêm 12% "2–4 đá".
- Các dòng cũ giữ trọng số tương đối (chia lại tỉ lệ).

Chạy lại mô phỏng và cập nhật bảng tỉ lệ hiển thị.

## Risks / Trade-offs

- **[Cộng dồn quá mạnh]:** 4 ô Công Huyền thoại là +64% Công. Rất hiếm (0,5% mỗi ô) nhưng có. Đặt trần tổng mỗi loại +40%; công cụ cân bằng đo trường hợp xấu nhất.
- **[Hang thành nơi cày bi]:** Hang chỉ ra đá, không ra bi.

## Open Questions

- Đã chốt: ô mở theo sao.
- Đã chốt (chủ dự án để Claude quyết, 2026-10-31): Hang giữ 3 lượt thắng mỗi ngày, thua không mất lượt, +1 lượt bằng quảng cáo; ải chính vẫn không giới hạn.
