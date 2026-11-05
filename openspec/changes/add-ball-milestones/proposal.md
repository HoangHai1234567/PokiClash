## Why

Chủ dự án (2026-11-05), xem màn Máy bi trên điện thoại:
- thanh kinh nghiệm có nhún khi nhận EXP, nhưng chỉ phần đầy nhún, phải nhún cả viền;
- học các mốc phần thưởng của Clash of Critters: thả n bi thì nhận một món, rồi đổi sang món mới;
- nút ×N không mở theo cấp mà theo số bi đang có: nhiều bi thì chọn mức cao để thả nhanh hơn, như Critters.

Đọc từ bản đục Critters (`D:\CrittersRipper`, chỉ asset không mã hoá; ảnh dựng lại ở `analysis/ui_shots/sheet.png`):
- **Bảng cược** `pbui_pinball_multi_popup`: "Mọi phần thưởng ×2", và ở mức tối đa "Mốc tiếp theo: mở khi có 8000 bi".
  - Wiki và guide cùng ghi ngưỡng: ×1, ×2 luôn mở; ×3 từ 240, ×5 từ 360, ×10 từ 600–720, ×20 từ 1.200, ×40 từ 2.400, ×60 từ 4.800, ×100 từ 7.200 bi đang có.
  - Tức khoảng 60–80 lần thả ở mức đó. Bi tụt dưới ngưỡng thì mất mức đó; hết bi hoặc mở lại game thì về mức thấp nhất.
- **Thanh cấp** `pbui_pinball_level_bar`: cả nền và phần đầy cùng nhún (clip `anui_pinball_bottom_slider_add`: 1,2 → 1,08 → 1,2 → 1,08 → 1,2 → 1 trong 0,25 giây, chữ số 1,3/1,1). Dọc thanh có các mốc nhỏ (`pbui_small_level_template`, icon hệ có mũi tên lên).
- **Mốc quà:** nấm trứng có vòng tiến độ, đầy thì ra tướng hoặc bi, mỗi ngày tối đa vài lần (`pbui_drop_egg_tips`: "2/3", đếm ngược làm mới). Sự kiện có 150 bậc quà, tiến độ lấy từ ô sự kiện (số món nhân theo cược).

## What Changes

- **Nút cược mở theo số bi đang có** (`progression.xSteps[].balls`, thay `lv`):
  - ×1, ×2 luôn mở; ×3 từ 150, ×5 từ 300, ×10 từ 700 bi (khoảng 50–70 lần thả, mô phỏng: người chăm có 600–1.200 bi một ngày, người ít 50–150);
  - nút chưa mở mờ, ghi "n bi", chạm vào báo cần bao nhiêu bi;
  - đủ bi mở thêm mức thì báo và nút mới nhún;
  - bi tụt dưới ngưỡng của mức đang chọn: hết đợt cược tự về mức cao nhất còn mở và báo (đợt đang chạy giữ nguyên cược);
  - hộp "Lên cấp!" thôi ghi "Mở nút ×N".
- **Mốc quà** (`pachinko.gifts`): sau mốc Huyền thoại, mỗi bi tiêu (×N tính N) cộng vào mốc đang chạy:
  - 30 bi rương gỗ, 40 bi +8 bi, 50 bi rương bạc, 60 bi +120 XP, 80 bi rương vàng, rồi vòng lại;
  - đủ thì nhận ngay lúc thả, phần dư sang mốc kế. Rương vào khay "Rương chờ" (không nhân cược), bi và EXP cộng ngay;
  - thanh mốc dưới cùng bên phải (chỗ thanh Huyền thoại cũ) ghi "Rương Bạc: 12/50 bi". Ô quà tròn ở đầu thanh hiện quà đang chờ;
  - nhận quà: thanh đứng đầy "Nhận quà!", ô quà nhún, loé to, quà bay ra (rương vào khay, sao EXP lên thanh kinh nghiệm, bi về dòng đếm). Rồi ô quà đổi sang quà kế và nhún vào;
  - chạm thanh hoặc ô quà báo ba mốc kế ("Rương Vàng sau 61 bi · …");
  - bảng tỉ lệ ghi thêm bảng mốc quà và ngưỡng cược.
  - Giá trị thêm vào kinh tế khoảng 7–8 % mỗi vòng 260 bi (một rương mỗi loại, 8 bi, 120 XP).
- **Thanh kinh nghiệm nhún cả viền:**
  - rãnh vẽ tay cắt khỏi thân máy (`ArtGen/Pachinko/cat_ranh.py` → `pk_ranh_exp.png`), đặt trùng khít lên rãnh;
  - rãnh cùng thanh gom thành `khung_thanh` và nhún cùng nhau theo dáng chép Critters, chữ số nhún thêm;
  - không bao giờ nhỏ hơn 1, để luôn che rãnh vẽ sẵn bên dưới.
- Bản lưu thêm `gift`, `giftTier`. Bi tiêu trong mô phỏng tiến độ cũng tính mốc quà.

## Capabilities

### New Capabilities

<!-- không có -->

### Modified Capabilities

- `pachinko-machine`: nút cược mở theo số bi, mốc quà sau mốc Huyền thoại, thanh kinh nghiệm nhún cả viền.

## Impact

- **Unity, code:**
  - `Core/BalanceConfig.cs` (`XStep.balls`, `GiftStep`, `gifts`), `Core/Progress.cs` (`XAllowed` theo bi, `XBest`), `Core/Pachinko.cs` (`GiftNow`, `GiftAt`, `GiftCredit`, `GiftAdd`, `GiftName`), `Core/SaveData.cs`, `Core/ProgressSim.cs`;
  - `App/Scenes/MachineScene.cs`, `App/Scenes/MachineRatesDialog.cs`, `App/Dialogs.cs`, `Game/Machine/MachineExpBar.cs`;
  - `Editor/MachineCabinetMenu.cs` (`khung_thanh`), `Editor/MachineGiftMenu.cs` (mới, menu "PokiClash/Prefab/Máy bi: mốc quà"), `Editor/PlayTour.cs` (tour "Máy bi: mốc quà, cược theo số bi"), `Tests/PachinkoTests.cs`.
- **Dữ liệu:** `Json/balance.json` (khối `progression.xSteps`, `pachinko.gifts`) → `BalanceConfig.asset` qua "PokiClash/Nhập dữ liệu". Golden không đổi.
- **Prefab:** `Screens/Machine` (`khung_thanh`, `o_qua`, thanh mốc gốc giữa có nút).
- **Ảnh:** `Assets/03 Art/Pachinko/pk_ranh_exp.png` (585 × 55, cắt từ thân máy), `ArtGen/Pachinko/refs/ranh_exp.json`.
- **Bản web:** chưa đổi (luật 2026-11-03: chỉ làm Unity). `Web/src/core` còn mở cược theo cấp.
