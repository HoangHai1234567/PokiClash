## Context

`Web/src/core/battle.ts` là một máy trạng thái thuần:
- tạo trận từ hai đội và hạt giống;
- các hàm `startBattle`, `advance`, `swap`, `pick`, `useInnate`, `execute`, `forceSwap` trả về danh sách sự kiện;
- mỗi sự kiện kèm ảnh chụp số liệu của mọi tướng.

Màn trận web (`battleScreen.ts`) phát lại sự kiện bằng `async/await`, cập nhật thanh số theo ảnh chụp. `ai.ts` chấm điểm thẻ.

Số đã cân bằng máy tự chơi trên web (`npm run sim`): trận 2–6 hiệp ở các đảo đầu.

## Goals / Non-Goals

**Goals:**
- Unity cho ra cùng chuỗi sự kiện với web khi cùng hạt giống và cùng lựa chọn.
- Luật tách khỏi hiển thị: chạy được nghìn trận trong EditMode test hoặc công cụ cân bằng, không cần scene.
- Màn trận giữ đúng bố cục và cảm giác của bản web (nhịp, dòng tin chữ, nắn hướng lao).

**Non-Goals:**
- Đấu người với người, đồng bộ mạng.
- Thẻ chung lên cấp (chỉ thẻ riêng lên cấp, xem `add-hero-roster`).
- Hình tướng mới.

## Decisions

### Luật là máy trạng thái phát sự kiện

C# giữ đúng cấu trúc TypeScript:
- lớp `Battle`, các pha `Idle | Picking | Ready | ForceSwap | Over`;
- `List<BattleEvent>` có `Snapshot` (máu, máu tối đa, khiên, mana, nộ, gục, trạng thái, tổng buff Công/Thủ của từng tướng).

Màn trận chỉ đọc sự kiện. Màn trận không bao giờ đọc thẳng trạng thái `Battle` để vẽ thanh số, vì trạng thái đã đi trước hoạt cảnh.

- **Phương án khác: hiển thị đọc trực tiếp trạng thái.** Bỏ, vì máu sẽ tụt trước khi đòn chạm tới.

### Phát lại bằng hàng đợi coroutine

`BattlePlayer` nhận danh sách sự kiện, chạy từng cái:
- mỗi loại sự kiện có một handler `IEnumerator`;
- chờ tính theo `1 / speed`;
- sự kiện `attack`, `ult` và chiêu (`card` loại `skill`) mở clip của tướng và chờ tới khung trúng đòn rồi mới chạy tiếp;
- phần còn lại của clip chạy song song; trước sự kiện `card`, `turn`, `ult`, `attack`, `round`, `swap` kế tiếp thì chờ clip trước xong.

### Nắn hướng lao của clip đánh

Clip đánh mặt trước của aola lao sang phải-xuống khoảng 500–650 điểm ảnh. Địch đứng trên-trái nên lao đúng hướng; phe mình đứng dưới-phải, lật ngang.

Mỗi khung, độ dời là `A·m(t) − m(t)`:
- `m(t)`: chuyển động trong clip (trung bình vị trí các hình, làm mượt 5 khung);
- `A`: phép xoay và co giãn đưa đỉnh lao tới 72% quãng đường giữa hai tướng.

Clip lao ít (dưới 30 điểm ảnh, kiểu bắn từ xa) thì tướng tự nhún tới 35% quãng đường. Khung trúng đòn là khung lao xa nhất; không có thì là 60% clip (55% với chiêu). Chép từ `Web/src/view/battle/stage.ts`.

### Hồi sinh

Thêm loại hiệu ứng `revive { pct }` và cờ `reviveLeft` trên tướng:
- khi tướng gục mà còn lượt hồi sinh, phát sự kiện `revive` thay cho `death`;
- máu về `pct × máu tối đa`, xoá trạng thái xấu, giữ vị trí ra sân.

Phật Tâm đổi từ "dưới 30% máu: hồi 35%" thành "lần đầu gục: hồi sinh 35% máu". Đổi cả bản web để hai bên cùng luật, rồi chạy lại `npm run sim` xem đảo Thổ còn ổn.

### Bên đi trước

Người chơi luôn đi trước mỗi hiệp (chủ dự án chốt 2026-10-31). Tốc chưa dùng trong trận; giữ trong chỉ số cho các chế độ sau.

### Máy chơi có độ khéo theo ải

`aiPickIndex(noise)`: điểm mỗi thẻ nhân thêm một hệ số ngẫu nhiên trong khoảng `1 ± noise`. Địch dùng `noise = max(0,12; 0,6 − 0,05 × số ải)`, nên ải đầu chọn kém. Tự chơi của người chơi dùng 0,12.

### Màn trận dựng bằng uGUI cộng một camera sân đấu

- **Sân đấu (phần trên):** camera trực giao riêng render ra RenderTexture, cao 464/960 màn hình. Gồm nền ảnh `battle_<hệ>`, hai `AolaActor` dạng sticker, hiệu ứng.
- **Phần dưới:** uGUI.
- Chữ nổi và số vẽ bằng TMP trên một canvas đè lên sân đấu, xếp thành dòng tin theo tướng.

## Risks / Trade-offs

- **[Lệch chuỗi sự kiện web ↔ Unity]:** golden test chạy 200 trận cố định hạt giống, so từng sự kiện và ảnh chụp.
- **[Trận dài ở đảo sau]:** đảo Thổ 8–12 hiệp. Theo dõi bằng công cụ cân bằng; giảm hồi máu của Đại Sư Cà Sa nếu cần.
- **[Sticker 8 hướng tốn GPU với clip lớn]:** clip đánh có khung tới 1.634 × 936 điểm ảnh. Chỉ dựng lại khi đổi khung; giới hạn độ phân giải RenderTexture theo cỡ hiển thị.
- **[Hồi sinh làm trận dài]:** mỗi tướng tối đa 1 lần; boss của địch không hồi sinh (đã làm trong luật, cả bản web).

## Kết quả đo (2026-10-31)

### Đảo Thổ sau khi đổi Phật Tâm thành hồi sinh

`npm run sim -- battle 100`, đội Sứ Giả, Gia Bỉ, Hắc Dực (3 sao, thẻ cấp 3), tỉ lệ thắng và số hiệp trung bình:

| Ải | cấp 21 | cấp 25 | cấp 28 | cấp 30 |
|---|---|---|---|---|
| 5 Ruộng Bậc Thang | 32%, 12,0 | 65%, 12,0 | 84%, 11,1 | 96%, 10,3 |
| 6 Chùa Đá | 43%, 9,9 | 75%, 9,8 | 89%, 8,5 | 95%, 7,5 |
| 7 Sân Tượng Đá | 5%, 12,2 | 28%, 13,3 | 53%, 13,7 | 59%, 14,0 |
| 8 Kim Tự Viện (boss) | 12%, 12,0 | 16%, 14,4 | 43%, 14,2 | 46%, 14,4 |

- Lần đầu cho cả boss hồi sinh: boss ở cấp 28 chỉ còn 7% thắng. Nên chốt **boss của địch không hồi sinh**: boss ở cấp 28 lên 43% (trước khi đổi Phật Tâm là 28%).
- Trận đảo Thổ vẫn dài 10–14 hiệp. Để công cụ cân bằng (`add-balance-tools`) chỉnh: giảm hồi máu Khói Hương hoặc máu của Đại Sư Cà Sa.

### Nhịp trận trong Unity

Đo bằng menu `PokiClash/Thử/Đánh thử ải …` (chọn tay 2 thẻ, rồi Tự chơi), đội 3 tướng cấp 7 ở ải 7–8:

| Ải | Số hiệp | Thời gian cả trận ở ×3 | Phần ra đòn một lượt người chơi, quy về ×1 |
|---|---|---|---|
| 1 Bãi Vỏ Sò (1 tướng, cấp 1) | 2 | 7,3 giây | 7,0 giây |
| 7 Hồ Gương | 5 | 37,1 giây | 8,4 giây |
| 8 Xoáy Nước Đinh Ba (boss) | 5 | 38,3 giây | 7,9 giây |

Phần ra đòn (5 thẻ chạy, đòn đánh, chữ nổi) mất 7–8 giây ở ×1, chưa kể lúc chọn thẻ. Giống nhịp bản web. Nếu thấy chậm: rút thời gian chờ của thẻ thường (420 ms) trước.

## Open Questions

- Choáng hiện là "lượt sau chỉ chọn 3 thẻ, không chiêu, không đánh". Có muốn choáng mất trọn lượt không?
- Có giới hạn thời gian chọn thẻ cho chế độ sau này (đấu trường) không?
