## 1. Logic tiến trình (C# thuần)

- [x] 1.1 Chép phần cấp, EXP, thẻ, sao, mảnh, đội của `progression.ts` sang `Core/Progression`: `ExpToNext`, `AddExp`, `CardReq`, `CanUpCard/UpCard`, `StarNeed/CanEvolve/Evolve`, `AddShards`, `RollCardDrop/GiveCard`, `MemberOf`, `PlayerTeam`
  - Ở `Core/Progress.cs` (thêm `HeroAlerts`, `UnlockHero`, `CardOf`) và `Core/Battle/Teams.cs` (`MemberOf`, `Player`).
- [x] 1.2 `HeroStats.Compute(hero, level, star, boss, mods)` chép `heroStats`, thêm `mods` cho side meta
  - `Core/HeroStats.cs`; trận gọi qua `Member.mods`. Không có mods thì số khớp từng bit với web.
- [x] 1.3 Golden: so `HeroStats` 11 tướng × cấp 1/10/20/30 × sao 1/3/5, và chuỗi `RollCardDrop` theo hạt giống, khớp bản web
  - Thêm cả boss và 80 lần nhận mảnh (`Golden/progression.json`).
- [x] 1.4 Tướng khởi đầu Tiểu Y; tướng tặng qua cờ `gift` trong dữ liệu ải (xử lý ở `add-world-islands`)
  - Tặng tướng đã chạy trong `Progress.WinStage` (mốc 1).

## 2. Scene Tướng

- [x] 2.1 Lưới 3 cột thẻ tướng (dải màu hệ, sticker hoặc bóng sẫm, tên, nhãn hệ, độ hiếm, sao hoặc thanh mảnh, "TRONG ĐỘI", chấm đỏ), tướng đã có xếp trước
  - Nhãn "TRONG ĐỘI n" ghi cả thứ tự ra sân.
- [x] 2.2 Hộp chi tiết: ô xem 4 clip (`AolaActor` dạng sticker, cách neo như bản web), thông tin, chỉ số, 3 thẻ có thanh bản sao và nút lên cấp, mục tiến hóa, nút đội, nơi rơi mảnh với tướng chưa có
  - `HeroViewer`: có aola (bản dev) thì `AolaSticker`, không thì hình giữ chỗ với hoạt cảnh giả cho 4 clip.
- [x] 2.3 Hoạt cảnh lên cấp thẻ và tiến hóa (tiếng, thông báo, tướng chạy clip chiêu)
- [x] 2.4 `heroAlerts` cho chấm đỏ ở thẻ tướng và số trên nút Tướng ở sảnh

## 3. Scene Sổ thẻ

- [x] 3.1 Khung "Cách xếp thẻ", chú giải độ hiếm, lưới 23 thẻ chung, thẻ khoá theo cấp

## 4. Lên cấp

- [x] 4.1 Hộp "Lên cấp!" (con dấu tím, cấp mới, nút cược vừa mở, thẻ chung vừa mở), gọi sau hộp kết quả hoặc sau khi mở hết rương
  - `Dialogs.LevelUp`, dùng chung cho trận, máy bi và bảng thử. Mốc máy bi gọi sau khi mở hết rương.

## 5. Kiểm tra

- [x] 5.1 EditMode: golden chỉ số và rút thẻ; luật nâng thẻ, tiến hóa, mảnh thừa
  - 8 test mới, tổng 31.
- [x] 5.2 Play: dùng bảng thử "+5 bản sao mọi thẻ" và "+500 XP", nâng thẻ, tiến hóa, kiểm số trong trận khớp màn Tướng; `read_console` không lỗi
  - Bảng thử ở Sổ tay (chỉ trong Editor và bản Development). Menu `PokiClash/Thử/Tướng: nâng thẻ, tiến hóa`; giữ và trả lại bản lưu.
