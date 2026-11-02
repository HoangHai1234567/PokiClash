## 1. Luật trận (C# thuần)

- [x] 1.1 Chép `Web/src/core/battle.ts` sang `Core/Battle/Battle.cs`: các pha, `Fighter`, `Side`, `Turn`, sự kiện có `Snapshot`, các hàm `CreateBattle`, `StartBattle`, `Advance`, `Swap`, `Pick`, `UseInnate`, `Execute`, `ForceSwap`, `InnateBlock`
  - Số liệu dùng `double` như `number` của JS (tránh chia số nguyên, so ảnh chụp từng giá trị). Kiểu ở `BattleTypes.cs`.
- [x] 1.2 Áp hiệu ứng: buff (thời hạn end/start, cả trận), hồi máu, máu tối đa, tự mất máu, mana/nộ (cả hút của địch), sát thương (nhiều đòn, xuyên, hút máu), khiên (trần 60%), trạng thái, xoá xấu, Gương Đôi, đánh thêm, Thiên Mệnh, điều kiện máu thấp
- [x] 1.3 Thêm hiệu ứng `revive`, cờ hồi sinh một lần, sự kiện `revive`; điều kiện kết thúc tính cả hồi sinh; giới hạn 60 hiệp
  - Bị động kích hoạt `death`; boss của địch không hồi sinh. Quá 60 hiệp: bên có tổng phần trăm máu cao hơn thắng, hoà thì địch thắng (`CFG.maxRounds`).
- [x] 1.4 Đổi bị động Phật Tâm thành hồi sinh 35% ở cả `Web/src/core/data/cards.ts` và dữ liệu Unity; chạy lại `npm run sim -- battle` và ghi lại số đảo Thổ
  - Số đo ghi ở `design.md`, mục "Kết quả đo".
- [x] 1.5 Chép `ai.ts` sang `Core/Battle/Ai.cs` (điểm thẻ, nhiễu, Chiêu/Tuyệt kỹ, đổi tướng, chọn tướng thay) và `sim.ts` (`RunBattle`)
  - Tên file `BattleAi.cs` (gồm `BattleAi` và `BattleSim`); dựng đội ở `Teams.cs`; thưởng ải `Progress.WinStage`.
- [x] 1.6 Golden: `Web/scripts/export_golden.ts` xuất 200 trận (hạt giống cố định, cả hai bên do máy chơi); EditMode test so từng sự kiện và ảnh chụp
  - 12 trận so từng sự kiện kèm ảnh chụp; 200 trận so kết quả, số hiệp, số lượt, chuỗi loại sự kiện, sát thương, ảnh chụp cuối. Có 34 trận có hồi sinh.

## 2. Sân đấu

- [x] 2.1 Camera sân đấu render ra RenderTexture; nền theo hệ đảo (`battle_<hệ>` hoặc nền vẽ bằng code theo bảng màu của đảo); bệ đứng hai tướng
  - Sân dựng bằng uGUI (`StageView`), không cần camera riêng; RenderTexture chỉ dùng cho tướng aola. Nền thay thế xuất từ code vẽ của web (`export_fallback.mjs`).
- [x] 2.2 `AolaActor` dạng sticker (viền trắng + viền mực bằng shader 8 hướng), cỡ theo `size` của tướng và boss ×1,18, chỉ dựng lại khi đổi khung
  - `AolaSticker` + shader `PokiClash/StickerOutline`. Chỉ chạy khi bật define `POKICLASH_DEV` (chưa bật, chưa xem được trên máy). Không có aola thì dùng hình giữ chỗ theo hệ (`HeroArt`).
- [x] 2.3 Nắn hướng lao clip đánh (độ dời trong clip, đỉnh lao, khung trúng đòn) chép từ `stage.ts`; tự nhún tới với clip lao ít
- [x] 2.4 Hiệu ứng: chữ nổi dòng tin theo tướng, số sát thương, ngôi sao tượng thanh, vòng sáng, tia, loé màn, rung, nháy trắng; trạng thái trên đầu
- [x] 2.5 Gục, rút lui, rơi xuống sân, hồi sinh

## 3. Giao diện trận

- [x] 3.1 Thanh trên (tạm dừng, hiệp, nhãn lượt, tốc độ, Tự chơi), bảng thông tin hai bên
- [x] 3.2 Hàng thẻ (ô đã chọn, ô trống, ô đòn kết, ô đang chạy nhô lên, ô xong mờ), 3 thẻ để chọn có hoạt cảnh chia và bay vào ô
- [x] 3.3 Hàng dưới: chân dung đội (đổi tướng đầu lượt, nhấp nháy khi đổi được), nút Chiêu/Tuyệt kỹ (sẵn sàng nhịp, thiếu thì rung và báo lý do)
- [x] 3.4 Lượt địch: lá úp chia một lần, lá chọn nhô lên, hàng thẻ địch lấp dần
- [x] 3.5 Hộp chọn tướng thay (bắt buộc, gợi ý khắc hệ), hộp tạm dừng, màn VS, băng rôn hiệp và Tuyệt kỹ
- [x] 3.6 Bong bóng gợi ý cho 2 trận đầu
- [x] 3.7 Hộp kết quả thắng/thua với con dấu, thưởng, các nút; nối sang hộp lên cấp

## 4. Điều khiển trận

- [x] 4.1 `BattleController`: vòng trận (Picking → người chơi hoặc máy; Ready → Execute; Idle → Advance; ForceSwap → hộp chọn), tự chơi bật/tắt giữa chừng
- [x] 4.2 `BattlePlayer`: hàng đợi coroutine, handler cho mọi loại sự kiện, chờ khung trúng đòn, áp ảnh chụp sau mỗi sự kiện, tốc độ ×1/2/3
- [x] 4.3 Nối vào `SceneRouter`: vào từ hộp chuẩn bị trận của scene Zone, ra về Zone hoặc sang Machine
  - Hộp chuẩn bị trận tạm thời (địch, đội trong bản lưu, nút Đánh); chọn đội làm ở `add-world-islands`.

## 5. Kiểm tra

- [x] 5.1 EditMode: golden 200 trận khớp; luật đổi tướng, choáng, hồi sinh, kết thúc, giới hạn 60 hiệp
- [x] 5.2 Play: đánh ải 1 Đảo Thủy bằng tay và bằng Tự chơi ở ×3; chụp màn hình lúc chọn thẻ, lúc chạy thẻ, lúc trúng đòn, hộp kết quả; `read_console` không lỗi
  - Menu `PokiClash/Thử/Đánh thử ải 1`, `… ải 7, đội 3 tướng`, `… ải 8 boss`: chọn tay 2 thẻ (gọi cùng hàm như bấm thẻ), rồi Tự chơi; công cụ giữ và trả lại bản lưu.
- [x] 5.3 Đo thời gian một lượt người chơi và độ dài trận ở 3 ải khác nhau, ghi vào design
