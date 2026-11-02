## 1. Vật lý và thưởng (C# thuần)

- [x] 1.1 Chép `Web/src/core/pachinko.ts`: `BuildBoard` (đinh, nấm, u lồi, vai, cốc, ô theo `SLOT_W`), `Board.Drop/Step` (4 bước con, va đinh, tường, bi–bi, đẩy bi kẹt), sự kiện `peg` và `land` — `Core/Pachinko.cs`; `Math.hypot` chép cách tính của V8
- [x] 1.2 Thưởng: `SlotReward`, `OpenChest` (bảng rương, ×N, thẻ rút riêng, mảnh), `SpendBall` (đếm bi đã tiêu, mốc Huyền thoại, nhánh đã có tướng → 15 bản sao)
- [x] 1.3 `MaxPerDrop(level)` 20/30, `XAllowed(level)`; thêm cả vào bản web (`maxPerDrop`, `LEGEND_COPIES`, nhánh `legendCopies` của `spendBall`)
- [x] 1.4 Mô phỏng 6.000 bi trong EditMode, so tỉ lệ với bản web (golden `pachinko.json`, cùng cách thả): mọi ô lệch dưới 1 điểm phần trăm. Không khớp từng bi (307/400 bi đầu trùng) vì làm tròn số thực khác nhau giữa V8 và .NET; đủ cho yêu cầu tỉ lệ

## 2. Scene Machine

- [x] 2.1 Mặt máy (`Game/Machine/MachineBoard.cs`): vẽ trên uGUI thay vì camera trực giao riêng (cùng hệ khung, canvas, nét rung của bộ UI). Thân và mặt máy là khung giấy viền mực; đinh, nấm chấm bi, u lồi, cốc vàng/bạc, ô gạch sáp, vách, ray vẽ một lần vào texture; nhãn ô (số EXP, +1 bi, rương gỗ) là chữ; máng mây đung đưa
- [x] 2.2 Bi (pool, màu theo mức cược ×1 hồng, ×2–3 xanh, ≥×5 vàng, vệt mờ), loé đinh, sáng ô, chữ nổi; lớp động nằm trên canvas con. Ô rương: loé răng cưa, sáng lâu hơn, chữ to hơn, rương bay vào khay
- [x] 2.3 Nhập liệu: chạm máy hoặc nút "Thả bi" thả 1 bi, giữ thả mỗi 0,16 giây, "Thả liền 20/30", "Đợt này n/max"; báo "Tối đa 20 bi một đợt…", "Cần N bi cho mỗi lần thả ×N"
- [x] 2.4 Cột cược bên trái (khoá ghi "Cấp n", không đổi giữa đợt), khay "Rương chờ" bên phải (đếm theo loại, chạm để mở), thanh "Huyền thoại chắc chắn: x/300" / "Đã nhận …", nút "Tỉ lệ" (đọc tỉ lệ đo bằng mô phỏng 6.000 bi do `export_data.ts` ghi vào `balance.json`, bảng rương, thẻ Huyền thoại 0,01 %, mốc 300)
- [x] 2.5 Hộp mở rương (lắc, bật, chip EXP/bi, thẻ mini kèm tên tướng, gộp bản sao cùng thẻ "×n", mảnh tướng), rương quý mở trước, "Mở tiếp (n)" / "Nhận"; hộp "Huyền thoại!" sau rương cuối; "Lên cấp!" sau cùng
- [x] 2.6 Rời scene khi bi đang lăn: mỗi bi tính ô giữa (EXP 10 × cược); rương chờ lưu trong bản lưu (`chests`)

## 3. Âm thanh

- [x] 3.1 Tiếng chạm đinh (tối đa ~25 lần/giây, cao độ ngẫu nhiên, to theo tốc độ), rơi ô, keng hoàn bi, rương, lắc rương, lên cấp

## 4. Kiểm tra

- [x] 4.1 EditMode: không bi nào kẹt trong 6.000 bi; tỉ lệ khớp; ×N nhân đúng; mốc Huyền thoại cả hai nhánh; bảng tỉ lệ đủ 7 loại ô; rương chờ ghi rồi đọc lại
- [x] 4.2 Play (`PokiClash/Thử/Máy bi: thả ×1 và ×3, mở rương`): thả 20 bi ×1 và ×3, mở rương, vượt mốc Huyền thoại, lên cấp, rời máy khi bi đang lăn, chụp màn hình; console không lỗi
- [ ] 4.3 Đo FPS khi 30 bi cùng lăn trên một máy Android tầm thấp (cần máy thật)
