## 1. Logic đảo (C# thuần)

- [x] 1.1 Chép phần đảo của `progression.ts`: `zones`, `zoneChests`, `TotalCleared`, `StageCleared/StageOpen/NextStage`, `StageBalls`, `WinStage` (tặng, rơi, đánh lại), `ZoneChestReady/ClaimZoneChest`
  - Thêm `DifficultyOf`, `RecommendedZone`, `CounterOf`, điều kiện mở công trình side meta (`FarmOpen`, `BadgesOpen`, `CaveOpen`) ở `Core/Progress.cs`.
- [x] 1.2 Dữ liệu 5 đảo (cấp, màu, ảnh, toạ độ vùng, toạ độ 8 ải) và 40 ải trong `ZoneDb` từ `zones.json`, `stages.json`
  - Đã có từ mốc 0.
- [x] 1.3 Golden: chuỗi `WinStage` và `ClaimZoneChest` theo hạt giống khớp bản web
  - `Golden/zones.json`: 8 ải đầu, 2 rương, 6 lần đánh lại boss, đánh lại ải tặng, 4 ải Đảo Hỏa và rương.

## 2. Scene Hub

- [x] 2.1 Ảnh `world` phủ kiểu cover, hoặc bản đồ nét tay; 3 mây trôi
- [x] 2.2 Bảng tên 5 vùng (icon hệ, tên, nhãn độ khó, "Cấp a–b · n/8 ải", thanh tiến độ), vùng chạm tròn
- [x] 2.3 Mũi tên đảo gợi ý; bảng "Làng Máy Bi"; chỗ đặt công trình side meta (nét chì khi chưa mở)
  - Công trình đã mở thì báo "sắp có" cho tới khi làm các mốc side meta.
- [x] 2.4 Hàng nút tròn: Tướng (số việc chờ), Sổ thẻ, Máy Bi (to, số bi), Đánh tiếp, Sổ tay
- [x] 2.5 Màn giới thiệu lần đầu (4 ô, "Bắt đầu!", chỉ một lần)

## 3. Scene Zone

- [x] 3.1 Khung cuộn dọc: ảnh đảo phóng 1,27 lần (đệm trên 110, dưới 150), tự cuộn tới ải đang đánh; nền ngoài ảnh tô màu biển của đảo
  - Đệm theo khung 1080: trên 260, dưới 330 (thanh trên của Unity cao hơn bản web). Chiều cao ảnh theo tỉ lệ ảnh thật.
- [x] 3.2 8 ô ải theo trạng thái (đã qua, đang đánh, khoá; thường, mini boss, boss), nét chấm vàng đường đã đi, sticker đội trưởng
- [x] 3.3 Khung thông tin: hệ, cấp đề nghị, độ khó, tiến độ, 2 rương mốc lắc khi nhận được, câu gợi ý hệ khắc; hộp nhận rương
- [x] 3.4 Khung ải tiếp theo (địch, thưởng, tặng, "Đánh!") hoặc "Đã chinh phục"
- [x] 3.5 Hộp chuẩn bị trận (cảnh báo, đối thủ, thưởng, đội 3 ô, kho tướng có mũi tên khắc hệ, "Xuất trận!")
  - `App/Scenes/StagePrep.cs`.

## 4. Nối luồng

- [x] 4.1 Sảnh → Zone → chuẩn bị → Battle → kết quả → Zone (hoặc "Ải tiếp" mở luôn hộp chuẩn bị ải kế); bỏ trận về Zone
- [x] 4.2 `WinStage` gọi từ kết quả trận; lưu ngay

## 5. Ảnh

- [ ] 5.1 Đưa `world`, `zone_thuy`, `zone_hoa`, `zone_kim` (Canva) vào `Assets/03 Art/Islands`; soi lại toạ độ vùng và ải trên ảnh độ phân giải gốc
  - Chờ ảnh: `ArtGen/Islands/inbox` đang trống. Có ảnh thì chạy menu `PokiClash/Nhập ảnh ArtGen`; toạ độ sửa ở `Web/src/core/data/stages.ts` rồi xuất lại.
- [ ] 5.2 Khi có `zone_moc`, `zone_tho` (gói `ArtGen/Islands`): chấm 8 ải theo đường mòn, cập nhật dữ liệu ở cả web và Unity
  - Chờ ảnh.

## 6. Kiểm tra

- [x] 6.1 EditMode: mở ải, thưởng, rương mốc, tặng tướng
  - 5 test mới, tổng 36.
- [x] 6.2 Play: người chơi mới đi trọn Đảo Thủy bằng Tự chơi ×3 (tặng Võ Sư, Gia Bỉ; 2 rương mốc; boss rơi Y Trạch); chụp màn hình sảnh, đảo, hộp chuẩn bị; `read_console` không lỗi
  - Menu `PokiClash/Thử/Người chơi mới đi trọn Đảo Thủy`: 8 thắng, 10 thua phải đánh lại, cấp 6 (thả bi ở máy bi giữ chỗ, 10 EXP mỗi bi), 8 mảnh Y Trạch, đảo gợi ý chuyển sang Đảo Hỏa. Giữ và trả lại bản lưu.
