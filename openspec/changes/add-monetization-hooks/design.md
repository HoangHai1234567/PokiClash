## Context

Bản web có một nút "Nhận ×2 (giả lập quảng cáo)" cho AFK. Nghiên cứu máy bi trước đây (Clash of Critters, Coin Master) ghi:
- bán bi là bán lượt quay;
- dạng game này đã thua kiện lớn ở Mỹ;
- Úc xếp game mô phỏng cờ bạc vào R18+.

Dự án trước đây đã chốt "bi chỉ kiếm bằng chơi". GDD mới nhắc quảng cáo và IAP cho AFK.

## Goals / Non-Goals

**Goals:**
- Mỗi chỗ quảng cáo là một tên chỗ đặt; tính năng không biết SDK nào ở dưới.
- Bản dev chơi được trọn mà không cần SDK.
- Giới hạn mỗi ngày đếm ở một chỗ.

**Non-Goals:**
- Chọn và tích hợp SDK thật.
- Tiền tệ cao cấp (kim cương), gói ngẫu nhiên, bán bi.

## Decisions

### Lớp móc

```
IRewardAds.Show(string placement, Action<bool> done)
IStore.Buy(string productId, Action<bool> done)
```

- `AdGate.CanShow(placement)` đọc giới hạn ngày.
- Ngày đặt lại lúc 0 giờ theo giờ máy, dùng chung chống chỉnh giờ với AFK.
- Có "Bỏ quảng cáo" thì `Show` trả `true` ngay.

### Quyền lợi gói

`Entitlements`: `adventurePassUntil`, `noAds`. Các công thức AFK đọc `Entitlements`:
- AFK ×1,5 khi còn hạn Thẻ Phiêu Lưu;
- khay rương AFK 5 ô thay vì 4;
- giờ mở rương AFK 1 tiếng thay vì 2.

### Không bán tài nguyên vào máy bi

Không có gói nào cho bi, đá tiềm năng hay lượt quay. Đổi nguyên tắc này phải có change riêng và chủ dự án duyệt.

## Risks / Trade-offs

- **[Ít doanh thu hơn bán bi]:** đổi lại rủi ro pháp lý thấp và người chơi tin tưởng hơn. Chủ dự án có thể đổi sau.
- **[Quảng cáo làm gãy nhịp]:** chỉ ở các nút người chơi tự bấm, không có quảng cáo xen ngang.

## Open Questions

- SDK quảng cáo và IAP nào (AdMob, Unity LevelPlay, AppLovin)?
- Có muốn gói khởi đầu có tướng (dễ thành mua sức mạnh) không? Đề xuất là không.
