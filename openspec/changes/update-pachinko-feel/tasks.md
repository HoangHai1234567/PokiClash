## 1. Vật lý và mặt máy (web, nguồn số)

- [x] 1.1 `Web/src/core/pachinko.ts`:
  - `PHYS` (nảy, cản, kẹp tốc độ), trần ở ray;
  - `SegKind` cho đoạn thẳng, cốc tròn hoặc két chữ nhật;
  - két vàng (`VAULT`), ô vàng khuất, 11 ô;
  - `sinSmall`/`cosSmall` cho góc lệch.
- [x] 1.2 `scripts/tune_pachinko.ts`: chỉnh cốc bạc, khe két, độ rộng ô. Mọi loại ô lệch mục tiêu dưới khoảng 1 điểm; kinh tế 9,39 EXP, 0,321 bi, 0,086 thẻ mỗi bi (cũ 9,41 / 0,319 / 0,085).
- [x] 1.3 `src/view/screens/machine.ts`: vẽ két, vẽ vai và vách theo loại đoạn, rương theo màu loại ô, nhãn bảng tỉ lệ. `npx tsc --noEmit` sạch.
- [x] 1.4 Xuất lại: `measured.ts`, khối `pachinko.measured` của `balance.json` (chỉ khối này), `Golden/pachinko.json`.

## 2. Chép sang C#

- [x] 2.1 `Core/Pachinko.cs`: hằng vật lý, két, `SegKind`, `Cup.w/h`, `SinSmall`/`CosSmall`, thứ tự dựng đinh và đoạn như web.
- [x] 2.2 Ngoài Unity (`dotnet`, biên dịch `Core/*.cs`): 147.087 sự kiện của 6.000 bi trùng từng bit với web; golden trùng 400/400 bi đầu, cùng số khung (36.422) và số lần chạm đinh (126.991); 600 lần mở rương khớp với JSON trong Unity.
- [x] 2.3 `Editor/BalanceWindow.cs` ghi số ô theo bố cục; nhãn bảng tỉ lệ (`MachineRatesDialog`); rời máy tính như ô EXP 10.
- [x] 2.4 Test: `MatMay_KetVangVaOKhuat`, `SinCosGocNho_SaiSoDuoi1e13`. Biên dịch được ngoài Unity cùng `PachinkoTests` (NUnit của dự án).
- [x] 2.5 Chạy EditMode trong Unity qua MCP: toàn bộ `PokiClash.Tests` 81/81 đạt (gồm 7 test `PachinkoTests`, `PrefabOnlyTests`, `SaveTests`); console không lỗi.

## 3. Mặt máy Unity

- [x] 3.1 `scripts/export_board.ts` + `scripts/draw_machine.py` vẽ lại `03 Art/Baked/Machine/may_tinh.png` (920 × 1360). Đã xem ảnh: két, đinh gác, ô khuất.
- [x] 3.2 `MachineBoard.Bind` dựng lại sáng ô, nhãn số và rương nhỏ (kit `Ruong`) theo bàn (11 ô, 2 cốc bạc, két).
- [x] 3.3 Play `PokiClash/Thử/Máy bi: thả ×1 và ×3, mở rương`: thả, mở rương, rời máy khi bi đang lăn đều đúng; ảnh `Temp/PokiShots/80–96`: nhãn số giữa ô, rương nhỏ đúng chỗ (sửa rương cốc vàng cũ còn sót, ảnh tĩnh thôi vẽ rương); console không lỗi.

## 4. Cảm giác

- [x] 4.1 Tiếng chạm đinh hãm nhịp 0,1 giây, ba cao độ không lặp liền, độ to tối đa 0,6 (`AudioService.Peg` trả về có phát hay không).
- [x] 4.2 Loé đinh phồng 1,3 → 1 trong 0,067 giây; sáng ô ba bậc (0,5 / 1,1 / 1,6 giây, rương vàng nhấp nháy); vòng loé có cỡ; rung mặt máy.
- [x] 4.3 Rương vàng: chạy chậm 0,3× (0,45 + 0,25 giây), máng thả tạm ngừng, rung mặt máy, vòng loé đôi, ba tiếng xu.
- [x] 4.4 `App/Haptics.cs`: rung chia bậc (Android 8+ có biên độ; máy cũ và iOS chỉ bậc rương vàng). Biên dịch được cả nhánh Android (định nghĩa `UNITY_ANDROID`, bỏ `UNITY_EDITOR`).
- [x] 4.5 Hộp mở rương: lắc gỗ 0,65 / bạc 0,85 / vàng 1,1 giây (vàng mạnh dần), rung khi bật theo loại.
- [ ] 4.6 Thử trên máy Android thật: rung từng bậc rõ mà không tê tay khi 30 bi cùng lăn; FPS.
- [x] 4.7 Nút **Rung** trong Sổ tay: `settings.haptics` (lưu, đọc, mặc định bật), `App.ApplySettings`, `NotebookScene` (bật thì rung thử); menu `PokiClash/Prefab/Sổ tay: thêm dòng Rung` đã chạy, prefab có dòng `hang_Rung` (nút kit giữ liên kết). Ảnh `Temp/PokiShots/130_so_tay_dau`: dòng Rung dưới Âm thanh.

## 5. Ảnh

- [x] 5.1 `ArtGen/Pachinko/PROMPTS.md`: P2 đổi mảnh 4 (mái két) và 11 (đáy két); thêm P4 bộ 12 hiệu ứng mô tả bằng chữ kèm cách code dùng. Thêm ảnh tham chiếu `StyleRefs/R2b_MayBi_KetVang.png` (ảnh của dự án).
- [ ] 5.2 Chủ dự án gen P1–P4. Claude ghép vào `Assets/03 Art/Pachinko/`, rồi thay loé, vòng loé, sáng ô bằng hình P4.

## 6. Chép vật lý và hiệu ứng của máy tham khảo (chủ dự án: "copy hiệu ứng và vật lý của game đó sang")

- [x] 6.1 Web `pachinko.ts`:
  - nảy 0,8 mọi thứ, ma sát 0,22 (`rub`), ngưỡng nảy 111, bi va bi không nảy, cản 0,3, không lệch;
  - trọng lực 1.100, kẹp 150–525. Chép nguyên thì bay trung vị 9,3 giây; lý do ghi ở design.
- [x] 6.2 Chỉnh lại ô và khe két:
  - độ rộng ô 25,25 / 38 / 46 / 29,75 / 59,25 / 35,5, khe 25,5;
  - mọi loại ô lệch mục tiêu dưới 0,65 điểm; kinh tế EXP −0,3%, bi −1,7%, thẻ −1,6%;
  - xuất `measured.ts`, khối `pachinko.measured`, `Golden/pachinko.json`.
- [x] 6.3 C# `Pachinko.cs` (`Rub`, `Fric`, `VRest`):
  - `dotnet` trùng từng bit: 400/400 bi, 36.416 khung, 124.948 lần chạm đinh;
  - 600 lần mở rương khớp.
- [x] 6.4 Hình hạt `fx_*` và nấm `pk_bumper` (`Web/scripts/draw_machine_fx.py`, `03 Art/Fallback`); ảnh tĩnh máy bỏ nấm, vẽ lại theo ô mới.
- [x] 6.5 `MachineFx.cs`: các bộ PegHit, BumperHit, SlotHit, ChestHit (cấp 2, 3), Jackpot, RingHit, Launch chép số hạt, đời, tốc, cỡ và màu theo đời.
- [x] 6.6 `MachineBoard`:
  - vệt dải `TrailGraphic` 0,3 giây; đinh loé 0,067 giây;
  - nấm động phồng xẹp 0,23 giây; mây co giãn khi thả; số nhảy ra;
  - hạt theo giờ máy.
- [x] 6.7 `MachineScene` gọi hiệu ứng thả, ô, cốc, rương, jackpot. Prefab `Items/HatMayBi` và `Items/VetBiDai` dựng bằng menu `PokiClash/Prefab/Máy bi: hạt hiệu ứng`.
- [x] 6.8 Unity:
  - lượt thử `PokiClash/Thử/Máy bi: soi hiệu ứng` dừng máy và tua giờ hạt để chụp từng mốc (ảnh `Temp/PokiShots/200–216`);
  - EditMode 82/83: test hỏng duy nhất là `IslandAnim.cs` của phiên Islands (luật prefab), không thuộc change này.
- [ ] 6.9 Có ảnh P4 thì đặt vào `03 Art/Pachinko` đúng tên `fx_*`, chạy "Dựng lại danh mục ảnh", chụp lại.
