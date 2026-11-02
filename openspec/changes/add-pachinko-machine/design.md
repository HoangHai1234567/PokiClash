## Context

`Web/src/core/pachinko.ts` có:
- lớp `Board`: đinh, segment tường và vách ô, cốc cảm biến, ô đáy;
- `step(dt)` chạy 4 bước con: trọng lực 1.150, va đinh có hệ số nảy (nấm 0,75, đinh 0,5), lệch ngẫu nhiên ±0,18 rad, va tường, va bi;
- thưởng: `slotReward`, `openChest`, `spendBall`.

Khung máy 460 × 680, bi bán kính 9. Mô phỏng `npm run sim -- pachinko` đo tỉ lệ. Hai lỗi đã sửa trên web:
- bi kẹt giữa tường và đinh mép (khe phải rộng hơn đường kính bi);
- danh sách đinh mép làm bi trượt thẳng xuống ô rương.

## Goals / Non-Goals

**Goals:**
- Unity cho tỉ lệ ô giống bản web (sai lệch dưới 1 điểm phần trăm mỗi ô trên 6.000 bi).
- Cảm giác "đã tay": bi va nhau, đinh loé, tiếng tích, rương bay vào khay.
- Tỉ lệ công khai, khớp số đo.

**Non-Goals:**
- Bán bi bằng tiền thật. Bi chỉ kiếm bằng chơi; quảng cáo và IAP ở change `add-monetization-hooks` không bán bi.
- Máy theo mùa, mặt máy đổi theo sự kiện.

## Decisions

### Vật lý tự viết, không dùng Physics2D

Chép đúng thuật toán web (va hình tròn, đoạn thẳng, bi–bi, bước cố định). Lý do:
- giữ tỉ lệ đã đo;
- có hạt giống, tái lập được;
- chạy được trong EditMode test.

Physics2D khó tái lập và tỉ lệ sẽ khác.

### Vẽ bằng một camera trực giao riêng

Thân máy, đinh, nấm, cốc, ô là sprite tĩnh (vẽ một lần). Bi là sprite pool (tối đa 30). Loé đinh và sáng ô là sprite cộng sáng. UI điều khiển (nút cược, nút thả, khay rương, mốc Huyền thoại) là uGUI quanh máy.

### Giới hạn mỗi đợt theo cấp

`MaxPerDrop(level) = level >= 15 ? 30 : 20`, chỉnh trong `BalanceConfig`. Đổi cả ở bản web.

### Rương mở sau đợt

Rương rơi vào thì bay vào khay, chờ tới khi mọi bi đã rơi rồi mới mở lần lượt (mỗi rương một hộp, nút "Mở tiếp (n)"). Hộp lên cấp hiện sau rương cuối. Rời scene khi đang có bi lăn thì các bi đó tính vào ô giữa (EXP 10).

### Mốc Huyền thoại theo bi đã tiêu

Đếm bi đã tiêu (×N tính N). Lần đầu vượt 300 thì mở Đại Sư Cà Sa nếu chưa có. Nếu đã có (vì nhặt đủ mảnh) thì cho 15 bản sao thẻ Huyền thoại của tướng này: đề xuất, cần duyệt; bản web hiện chưa xử lý trường hợp này.

## Risks / Trade-offs

- **[Cược ×10 làm tiến độ quá nhanh]:** ×10 mở ở cấp 12, và vẫn tốn 10 bi mỗi lần thả, nên tổng giá trị không đổi, chỉ nhanh hơn. Theo dõi số bi trung bình mỗi người chơi.
- **[Rương vàng ~3% nhưng có cảm giác hay trúng]:** đúng như ý (luôn có thưởng nhỏ, thỉnh thoảng thưởng lớn). Tiếng và hiệu ứng chỉ to ở ô hiếm, để tránh "thua mà tưởng thắng".
- **[Kết quả tuỳ máng thả]:** canh lúc thả có tác dụng nhẹ (máng ở giữa thì dễ vào cốc vàng giữa hơn). Bảng tỉ lệ ghi số đo khi thả đều.

## Open Questions

- Mốc Huyền thoại khi người chơi đã có Đại Sư Cà Sa: đổi thành bản sao thẻ (đề xuất) hay chọn một tướng Huyền thoại khác khi có thêm?
- Có thêm thanh "hũ sắp đầy" kiểu Critters (đầy hũ được mảnh tướng tự chọn) không?
