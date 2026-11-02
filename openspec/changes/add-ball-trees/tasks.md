## 1. Logic (web trước, rồi C#)

- [x] 1.1 `Web/src/core/trees.ts`, `data/trees.ts` → `Core/Trees.cs`: mở theo tiến độ, ra đều theo đoạn (đoạn có Thẻ Phiêu Lưu tính riêng), đầy thì ngừng, lùi giờ bỏ qua, cây mới mở bắt đầu từ lần tính sau, hái giữ phần lẻ, hái ×2, tua
- [x] 1.2 AFK bỏ bi theo giờ (`rateBase`, `ratePerStage`), `claim` chỉ còn mảnh; chỗ quảng cáo `afk_double` → `tree_double` (3/ngày); `PASS.afkMult` → `treeMult`, mô tả gói đổi theo
- [x] 1.3 Trang trại: `base` 2, `lvStep` 0, ca 8 + 1·(sao − 1) giờ, kho 10 giờ
- [x] 1.4 Lưu khoá `trees` (bản lưu cũ thiếu khoá thì tạo khi tính lần đầu; không cần bước di chuyển)
- [x] 1.5 Đường cong cấp `expBase`, `expPow` vào cấu hình (số giữ nguyên 40 và 1,35)

## 2. Giao diện

- [x] 2.1 Công trình "Cây bi" trên sảnh (rìa làng), chấm đỏ khi có cây đầy; hộp Cây bi (`App/TreePanel.cs`): 5 ô cây (bi/sức chứa, thanh đầy, cây chưa mở ghi điều kiện), "Hái +n", "Hái ×2 (lượt còn)"
- [x] 2.2 Hộp AFK: bỏ dòng bi chờ và "Nhận ×2", nút "Nhận mảnh", dòng "Bi giờ mọc ở Cây bi trên sảnh"; nút đồng hồ trên thanh trên ghi số bi trên cây (không có thì số giờ AFK), nhún khi có cây đầy
- [x] 2.3 Web: hộp AFK có mục Cây bi (hái, hái ×2), nút nhận thành "Nhận mảnh"
- [ ] 2.4 Ảnh gen công trình Cây bi và cây (đang dùng icon lá)

## 3. Kiểm tra

- [x] 3.1 EditMode: golden `trees.json` 27 bước khớp web; ví dụ đầy 10 giờ, đầy thì ngừng, lùi giờ, lưu rồi đọc lại; AFK, gói (cây ×1,5 cả tốc độ và sức chứa), trang trại theo số mới; 70 test đạt
- [x] 3.2 Play: AFK và cây bi (2 cây × 9 giờ = 90 bi, bỏ quảng cáo ngang +0, Hái ×2 +180), gói hỗ trợ (thẻ: 2 cây × 12 giờ = 150 bi; Bỏ quảng cáo: Hái ×2 trao ngay; chưa có SDK thì Hái ×2 ẩn), trang trại (ca 8 giờ, nghỉ 60 phút); bản phát hành biên dịch đạt

## 4. Nhịp tiến độ (chưa đạt mục tiêu ngày 21, chờ chủ dự án chọn hướng)

- [ ] 4.1 Mục tiêu: người chơi "vừa" (3 lần/ngày × 3 trận, có xem quảng cáo) xong cả 5 đảo khoảng ngày 21. Sau khi đổi: vẫn ngày 6 (bi thụ động 30 ngày giảm từ 62.002 xuống 37.329)
- [ ] 4.2 Quét bằng menu `Quét nhịp`: EXP lên cấp ×6 → ngày 15; EXP ×2 + bi thụ động ×0,5 + Hái ×2 1 lần/ngày → ngày 13; người chơi "ít" không xong trong 30 ngày ở các tổ hợp đó. Sức mạnh chủ yếu đến từ sao tiến hóa và cấp thẻ (40–43 lần tiến hóa trong 30 ngày ở mọi tổ hợp), không phải cấp
