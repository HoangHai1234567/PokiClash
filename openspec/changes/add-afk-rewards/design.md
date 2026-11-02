## Context

Bản web tính AFK từ `afkSince` (mốc lần nhận trước):
- số giờ = `min(12, (bây giờ − afkSince) / 1 giờ)`;
- bi = `floor(giờ × tốc độ)`;
- mỗi giờ tròn có 8% ra 1 mảnh boss.

Nhận xong thì đặt lại `afkSince`. Nút ×2 giả lập quảng cáo 3 giây.

## Goals / Non-Goals

**Goals:**
- AFK là lý do quay lại game (tối đa 12 giờ thì đầy, nhắc người chơi về nhận).
- Thẻ từ AFK có nhưng hiếm, đúng GDD.
- Có chỗ khai thác quảng cáo thưởng tự nhiên: nhận ×2, mở rương ngay, tăng tốc.

**Non-Goals:**
- AFK thay cho đánh ải (không ra EXP lớn, không qua ải hộ).
- Thông báo đẩy (để sau).

## Decisions

### Đồng hồ AFK tính theo đoạn

Lưu `afkSince`, `afkLastTick` và danh sách đoạn tăng tốc. Khi mở hộp AFK hoặc mỗi phút:
1. tính phần giờ mới từ `afkLastTick`;
2. phần nằm trong đoạn tăng tốc tính ×2;
3. cộng vào bộ đếm giờ hiệu dụng, chặn ở 12 giờ.

Rương AFK sinh khi bộ đếm giờ hiệu dụng vượt qua bội số 3 giờ (còn chỗ trong khay).

### Rương AFK mở theo giờ, từng cái

Rương đầu khay tự bắt đầu đếm 2 tiếng khi vào khay. Mở xong thì rương kế bắt đầu. "Mở ngay" xem quảng cáo, mỗi ngày tối đa 4 lần. Bảng rương AFK (ở mức thưởng ×1):

| Kết quả | Tỉ lệ | Lượng |
|---|---|---|
| Bi | 40% | 4–8 |
| EXP | 30% | 30–60 |
| Thẻ | 30% | 1–2 thẻ (Thường 60, Khá 30, Hiếm 9,5, Sử thi 0,5) |

### Chống chỉnh giờ

- `bây giờ < afkLastTick` thì bỏ qua đoạn đó, ghi cảnh báo.
- Một đoạn mới không cộng quá 12 giờ.
- Có máy chủ sau này thì đổi sang giờ máy chủ.

## Risks / Trade-offs

- **[Người chơi chỉnh giờ tới để cày]:** giới hạn 12 giờ và 4 rương chặn phần lớn; bản thử chấp nhận rủi ro còn lại.
- **[AFK quá hào phóng so với đánh ải]:** tốc độ AFK chỉ bằng khoảng 1–2 ải mỗi giờ; theo dõi bằng công cụ cân bằng.

## Open Questions

- Mảnh tướng AFK lấy từ boss đã gặp (như web), hay chỉ từ boss của đảo gần nhất?
- Có giới hạn số lần "Tăng tốc ×2" mỗi ngày không (đề xuất 3 lần)?
