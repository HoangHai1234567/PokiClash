## Context

Trang trại là một dạng AFK thứ hai, khác AFK ải ở chỗ người chơi phải sắp xếp: chọn tướng hợp chỗ, đổi ca khi tướng hết sức. Chỉ có 11 tướng, nên 8 chỗ là gần như cả kho tướng: trang trại thành chỗ dùng cho tướng ít ra trận.

## Goals / Non-Goals

**Goals:**
- Tướng mạnh (độ hiếm, cấp, sao) làm được nhiều và lâu hơn, đúng GDD.
- Có nhịp quay lại: tướng hết sức sau 2–6 giờ, nghỉ 15–60 phút.
- Không đụng tới trận: sức làm và sức đánh tách riêng.

**Non-Goals:**
- Xây dựng, trang trí trang trại (kiểu homestead của Critters): để sau.
- Trang trại ra thứ khác ngoài bi.

## Decisions

### Công thức (giá trị khởi điểm)

- **Năng suất (bi/giờ)** = `1,2 × sức độ hiếm × (1 + 0,05·(cấp − 1)) × (1 + 0,1·(sao − 1)) × (1,25 nếu đúng hệ hợp)`, với sức độ hiếm như chỉ số tướng (1; 1,1; 1,22; 1,36; 1,5).
- **Thời lượng làm (giờ)** = `2 + 0,5·(sao − 1) + 0,5·chỉ số độ hiếm`, với chỉ số độ hiếm Thường 0 … Huyền thoại 4.

  | Tướng | Thời lượng |
  |---|---|
  | Thường 1 sao | 2 giờ |
  | Huyền thoại 5 sao | 6 giờ |

- **Nghỉ (phút)** = `clamp(thời lượng × 60 / 4, 15, 60)`.

  | Thời lượng | Nghỉ |
  |---|---|
  | 2 giờ | 30 phút |
  | 6 giờ | 60 phút |

  GDD ghi "15-30 phút hoặc 1 tiếng". Muốn nghỉ 15 phút thì tướng phải có thời lượng 1 giờ (chỉnh hệ số nếu cần).

Ví dụ (đều đúng hệ hợp):
- Tiểu Y cấp 5, 1 sao ở Ao vịt: `1,2 × 1 × 1,2 × 1 × 1,25 = 1,8` bi/giờ, làm 2 giờ, ra khoảng 3,6 bi.
- Y Trạch cấp 15, 3 sao ở Ao vịt: `1,2 × 1,22 × 1,7 × 1,2 × 1,25 ≈ 3,7` bi/giờ, làm 4 giờ.

### Đồng hồ và kho

- Mỗi chỗ lưu tướng, lúc bắt đầu ca, sức còn (giờ), bi tích (số thực).
- Khi mở scene hoặc thu hoạch: tính phần thời gian mới, trừ sức, cộng bi. Hết sức thì dừng sản xuất.
- Kho mỗi chỗ chặn ở 12 giờ sản lượng.
- Chống chỉnh giờ dùng chung với AFK (bỏ đoạn âm).

### Đổi ca

- Rút tướng ra khỏi chỗ (đang làm hoặc đã hết sức) thì tướng vào trạng thái nghỉ, thời gian nghỉ theo công thức. Rút giữa ca vẫn phải nghỉ đủ.
- Tướng đang nghỉ không vào chỗ nào được.
- "Tự xếp": với mỗi chỗ trống, chọn tướng rảnh có năng suất ở chỗ đó cao nhất.

## Risks / Trade-offs

- **[Trang trại ra quá nhiều bi so với ải]:** 8 tướng × ~2–4 bi/giờ ≈ 16–32 bi/giờ, lớn hơn AFK ải (4–36 bi/giờ tuỳ số ải). Nhưng phải đổi ca mỗi 2–6 giờ, nên thực tế chỉ khoảng 60–70%. Công cụ cân bằng ước số bi theo 3 kiểu người chơi (vào 2, 4, 8 lần mỗi ngày); giảm hệ số 1,2 nếu cần.
- **[Người chơi quên đổi ca]:** chấm báo trên công trình sảnh khi có tướng hết sức hoặc kho đầy.

## Open Questions

- Đã chốt: mở chỗ 4–8 theo cấp người chơi.
- Có cho trang trại ra thêm một chút EXP không? GDD chỉ nói bi.
