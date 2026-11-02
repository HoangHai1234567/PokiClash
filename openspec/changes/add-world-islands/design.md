## Context

Bản web đã có scene sảnh (`Web/src/view/screens/world.ts`) và scene đảo hệ (`zone.ts`). Dữ liệu 5 đảo và 40 ải ở `Web/src/core/data/stages.ts`, tiến trình ở `progression.ts`.

Toạ độ 5 vùng trên ảnh đảo lớn và 8 ải trên ảnh 3 đảo đầu đã chấm theo ảnh Canva. Đảo Mộc và Thổ dùng toạ độ tạm trên bản đồ vẽ tay.

Máy tự chơi đo được, với đội khắc hệ ở cấp đề nghị:
- ải thường thắng 60–100%;
- boss thắng 50–95%;
- boss cuối Đảo Thổ còn khó (cần đo lại sau khi đổi Phật Tâm thành hồi sinh).

## Goals / Non-Goals

**Goals:**
- Giữ đúng bố cục đã duyệt trên web.
- Không khoá đảo; độ khó tự nói lên qua cấp đề nghị và nhãn độ khó.
- Thay ảnh đảo không phải sửa code; toạ độ là dữ liệu.

**Non-Goals:**
- Bản đồ cuộn ngang, bản đồ 3D xoay được.
- Sự kiện có hạn giờ, đảo theo mùa.
- Chuyển hệ của đảo (mỗi đảo một hệ cố định).

## Decisions

### Sảnh là ảnh đảo cộng lớp tương tác

- Ảnh `world` (2:3 từ GPT, hoặc 9:16) phủ kín theo kiểu cover.
- Bảng tên vùng neo tại toạ độ vùng, dời xuống 34 điểm ảnh (khung 540) để không che mốc chính.
- Vùng chạm là vòng tròn bán kính 95 quanh toạ độ vùng, cộng thêm bảng tên.

Mây trôi là 3 sprite mây chạy ngang lặp lại (70–120 giây mỗi vòng).

### Độ khó so với cấp

| Nhãn | Điều kiện |
|---|---|
| Dễ | cấp ≥ cận trên |
| Vừa sức | cấp ≥ cận dưới |
| Khó | cấp ≥ cận dưới − 3 |
| Quá mạnh! | còn lại |
| Đã chinh phục | 8/8 |

Đảo gợi ý là đảo chưa xong đầu tiên mà cấp người chơi ≥ cận dưới − 3; không có thì đảo chưa xong đầu tiên.

### Đảo hệ cuộn dọc

Ảnh đảo hệ phóng to 1,27 lần: khung 540 thành 686 × 1219, căn giữa, cắt hai bên. Khung cuộn có đệm trên 110 và đệm dưới 150, để ải 1 và ải 8 kéo ra được khỏi vùng khung trên và khung dưới che. Vào scene thì cuộn tới ải đang đánh ở giữa màn.

- **Phương án khác: thu nhỏ ảnh cho vừa màn.** Bỏ, vì ải ở hai đầu bị che và ảnh nhỏ mất chi tiết.

### Thưởng ải

```
o          = thứ tự đảo (0..4)
bi cơ bản  = 3 + 4·o + floor((ải − 1) / 2)
lần đầu    + 5 + 2·o (+3 mini boss, +7 boss)
```

Mảnh:
- lần đầu dùng đúng tỉ lệ trong dữ liệu;
- đánh lại: tỉ lệ 100% còn 50%, tỉ lệ khác nhân 0,8;
- tướng tặng chỉ ở lần đầu.

Rương mốc:
- qua 4 ải: 10 + 5·o bi và 2 bản sao thẻ;
- qua 8 ải: 20 + 10·o bi và 4 bản sao thẻ;
- độ hiếm bản sao: Thường 30, Khá 40, Hiếm 25, Sử thi 5.

### Chuẩn bị trận là hộp thoại trong scene Zone

Không thêm scene riêng. "Xuất trận!" lưu đội rồi chuyển sang Battle. Kết quả trận "Ải tiếp" quay về Zone và mở luôn hộp chuẩn bị của ải kế.

## Risks / Trade-offs

- **[Ảnh GPT khổ 2:3, màn 9:16]:** cắt hai bên khoảng 8% mỗi bên. Prompt yêu cầu giữ nội dung quan trọng trong dải giữa. Toạ độ chấm theo ảnh sau khi cắt.
- **[Người chơi vào đảo sau quá sớm và nản]:** nhãn "Quá mạnh!", cảnh báo trong hộp chuẩn bị, mũi tên đảo gợi ý.
- **[Bảng tên che mất cảnh đẹp của ảnh]:** bảng tên nhỏ gọn một dòng tên; có thể thu nhỏ khi cuộn (để sau).

## Open Questions

- Có cần cách vượt ải nhanh (quét ải đã 3 sao) không? GDD không nói; hiện chưa có sao ải.
- Đảo Mộc, Thổ: dùng ảnh GPT theo `ArtGen/Islands` hay Canva khi có lượt lại?
