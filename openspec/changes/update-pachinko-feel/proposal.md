## Why

Chủ dự án (2026-11-02), sau bản quét máy bi của Clash of Critters (`D:\CrittersRipper\analysis\PINBALL_REPORT.md`, đục từ asset không mã hoá): "copy apply vào game mình", rồi chọn áp cả ba phần: cảm giác, vật lý bồng bềnh, mặt máy mới. Asset và FX của họ chỉ để tham khảo; hình mình tự gen bằng GPT.

Những gì học được và đáng lấy:
- **Tỉ lệ hiếm tạo bằng hình học, không bằng ô hẹp.** Cốc hiếm có mái chữ ^ với khe hẹp ở đỉnh và một đinh gác ngay trên khe; ô hiếm nhất nằm khuất dưới đáy cốc, bi chỉ chui ngang vào được.
- **Bi bồng bềnh:** nảy cao, mất tốc nhẹ, tốc độ bị kẹp nên bi không đứng yên và không vọt khỏi mắt.
- **Phản hồi đi theo giá trị thật:** ô thường chỉ có hiệu ứng cơ bản. Chậm thời gian, rung màn, nhạc mừng chỉ dành cho ô hiếm nhất. Tiếng và rung chạm đinh bị hãm nhịp. Mở rương quý có thêm hồi hộp.

GDD gốc, mục máy pachinko: "rơi vào ô rương", "Huyền thoại cực hiếm". Change này giữ nguyên kinh tế mỗi bi, chỉ đổi cách máy cho ra kết quả và cảm giác.

## What Changes

- **Vật lý:**
  - nảy đinh 0,5 → 0,65, tường và vách 0,4 → 0,7, nấm 0,75 → 0,9;
  - lực cản 0,1 mỗi giây, tốc độ kẹp 150–950;
  - thêm trần ở ray máng thả.

  Thời gian bay trung vị 3,7 → 4,6 giây. Nảy 0,8 hay hạ trọng lực đã thử: bay 5–6,5 giây, một đợt quá dài.
- **Mặt máy:**
  - cốc vàng nhỏ giữa máy thay bằng **két vàng**: mái ^ chừa khe 25,25 ở đỉnh, đinh gác trên khe, đáy chữ V có hai cọc, vùng cảm biến chữ nhật bên trong;
  - **ô vàng khuất** dưới đáy két, nên đáy máy có 11 ô;
  - cốc bạc thu nhỏ (bán kính 3,5 → 2,5).

  Độ rộng ô chỉnh bằng mô phỏng để tỉ lệ từng loại ô giữ như mặt máy cũ (lệch dưới khoảng 1 điểm).
- **Sin, cos của góc lệch ngẫu nhiên** tính bằng đa thức, để bản web và Unity ra cùng từng bit. Với nảy cao, sai khác ở bit cuối của `Math.sin` làm bi Unity tách khỏi bi web chỉ sau 5 bi; giờ trùng hết 6.000 bi.
- **Cảm giác (Unity):**
  - **Rương vàng:** máy chạy chậm 0,3× trong 0,45 giây rồi nhanh dần lại, máng thả tạm ngừng; mặt máy rung; vòng loé đôi; ba tiếng xu lên cao dần; ô sáng nhấp nháy 1,6 giây.
  - **Tiếng chạm đinh:** cách nhau ít nhất 0,1 giây, ba biến thể cao độ không lặp liền nhau, độ to tối đa 0,6.
  - **Loé đinh:** phồng 1,3 → 1 trong 0,067 giây.
  - **Rung chia bậc** (đinh, thả, ô thường, rương gỗ, bạc, vàng, mở rương, lên cấp): bật tắt bằng nút **Rung** mới trong Sổ tay (lưu trong bản lưu, mặc định bật).
  - **Hộp mở rương:** gỗ lắc 0,65 giây, bạc 0,85, vàng 1,1 và lắc mạnh dần.
- **Ảnh:**
  - vẽ lại ảnh tĩnh mặt máy (`may_tinh.png`) bằng script, vì bộ nướng cũ đã xoá;
  - sáng ô, nhãn số ô và rương nhỏ trong ô, cốc, két (prefab kit) đặt theo bàn lúc chạy;
  - gói prompt `ArtGen/Pachinko` thêm két vàng và bộ 12 hiệu ứng P4 (mô tả bằng chữ).

## Capabilities

### New Capabilities

<!-- không có -->

### Modified Capabilities

- `pachinko-machine`: mặt máy (két vàng, ô khuất, 11 ô), vật lý (hệ số nảy, lực cản, tốc độ kẹp, trần, sin/cos đa thức), bảng tỉ lệ (số đo mới), phản hồi hình, tiếng và rung chia bậc, rời máy tính như ô EXP 10.

## Impact

- **Web:**
  - `src/core/pachinko.ts` (PHYS, CUPS, VAULT, SegKind, cốc chữ nhật, sinSmall/cosSmall), `src/view/screens/machine.ts` (vẽ két, nhãn bảng tỉ lệ);
  - script mới `scripts/tune_pachinko.ts`, `scripts/export_board.ts`, `scripts/draw_machine.py`;
  - `src/core/data/measured.ts` sinh lại.
- **Unity:**
  - `Core/Pachinko.cs`, `Game/Machine/MachineBoard.cs`, `App/Scenes/MachineScene.cs`, `App/Chest/ChestDialog.cs`, `App/AudioService.cs`, `App/App.cs`, `App/Haptics.cs` (mới), `App/Scenes/MachineRatesDialog.cs`, `App/Scenes/NotebookScene.cs`, `Core/SaveData.cs` (`settings.haptics`), `Editor/BalanceWindow.cs`, `Editor/NotebookHapticsMenu.cs` (mới), `Tests/PachinkoTests.cs`;
  - dữ liệu: `Golden/pachinko.json`, khối `pachinko.measured` của `Json/balance.json` (nạp vào `BalanceConfig.asset` bằng "PokiClash/Nhập dữ liệu"), ảnh `03 Art/Baked/Machine/may_tinh.png`;
  - prefab: `Screens/Notebook` thêm dòng "Rung".
- **Ảnh:** `ArtGen/Pachinko/PROMPTS.md` (P2 đổi mảnh 4 và 11, thêm P4), `ArtGen/StyleRefs/R2b_MayBi_KetVang.png`.
- **Phụ thuộc:** `add-pachinko-machine` (spec gốc của `pachinko-machine`; archive change đó trước change này), `convert-to-prefabs` (prefab màn máy).
