# Kế hoạch làm game trong Unity (OpenSpec)

Viết 2026-10-31, sau khi chủ dự án duyệt bản web (luật trận, bố cục scene, phong cách). Plan chi tiết nằm ở `openspec/` (OpenSpec 1.3, schema `spec-driven`). Mỗi change có:
- `proposal.md`: vì sao, đổi gì, ảnh hưởng;
- `design.md`: quyết định, rủi ro, câu hỏi mở;
- `tasks.md`: danh sách việc;
- `specs/*/spec.md`: yêu cầu và tình huống kiểm thử.

Kiểm tra: `openspec validate --all --strict`. Hiện cả 12 change hợp lệ.

## Lộ trình

| Mốc | Change | Nội dung | Phụ thuộc | Việc |
|---|---|---|---|---|
| 0 | `setup-unity-foundation` | Scene Boot và scene chức năng, màn mây, thanh trên và thanh quay lại, bộ UI vẽ tay, phông tiếng Việt, lưu, dữ liệu một nguồn từ web, quy ước ảnh, aola chỉ trong bản dev | — | 35 |
| 1 | `add-card-battle` | Luật trận thẻ bài (chép từ web), hồi sinh, máy địch, màn trận, hộp kết quả | 0 | 24 |
| 2 | `add-hero-roster` | 11 tướng, cấp chung, mảnh, thẻ riêng lên cấp bằng bản sao, tiến hóa sao, scene Tướng và Sổ thẻ | 0 | 12 |
| 3 | `add-world-islands` | Sảnh đảo lớn 5 vùng, scene đảo hệ 8 ải, rương mốc, chuẩn bị trận, thưởng ải | 0, 1, 2 | 19 |
| 4 | `add-pachinko-machine` | Máy bi vật lý, cược ×N, rương, mốc Huyền thoại, bảng tỉ lệ | 0, 2 | 14 |
| 5 | `add-afk-rewards` | AFK ra bi và mảnh, rương AFK có giờ mở, tăng tốc ×2 | 2, 3 | 10 |
| 6 | `add-balance-tools` | Máy tự chơi hàng loạt, mô phỏng máy bi và tiến độ, bảng thử, chỉnh số, ghi trận, golden | 1–4 | 11 |
| 7 | `add-element-badges` | Đền Huy Hiệu: chuỗi 5/10 trận boss theo hệ, +5%…+20% cho tướng cùng hệ | 1, 2, 3 | 11 |
| 8 | `add-potential-stones` | Đá tiềm năng, 4 ô mỗi tướng, khai phá có khoá ô, Hang Tiềm Năng | 1, 2, 3, 4 | 11 |
| 9 | `add-hero-farm` | Trang trại 8 chỗ, năng suất và thời lượng theo sức tướng, nghỉ ngơi | 2, 3, 5 | 9 |
| 10 | `add-monetization-hooks` | Quảng cáo thưởng và IAP qua lớp móc, giới hạn mỗi ngày, không bán bi | 0 | 8 |
| 11 | `add-ball-trees` | Cây bi trên sảnh thay bi AFK, trang trại ca dài, đường cong cấp vào cấu hình (chốt 2026-10-31) | 5, 9, 10 | 14 |
| 12 | `convert-to-prefabs` | Mọi thứ là prefab và asset làm sẵn (kể cả UI), runtime không sinh gì; nướng một lần bằng code dựng cũ rồi xoá code dựng | 0–11 | 31 |

Mốc 0–4 là vòng lõi chơi được (đánh ải → bi → máy bi → nuôi tướng). Mốc 5–6 làm vòng lõi bền và đo được. Mốc 7–9 là side meta của GDD. Mốc 10 làm song song được với mốc 5 trở đi.

## Đối chiếu GDD gốc

| Mục trong "GDD game Pokiwar" | Change |
|---|---|
| Core loop: đánh ải nhận bi → pachinko → nâng tướng → quái cao cấp hơn | `add-world-islands`, `add-pachinko-machine`, `add-hero-roster` |
| Boss, mini boss có cơ hội ra mảnh tướng | `add-world-islands` (thưởng ải) |
| AFK ải đã qua: bi hoặc mảnh tướng (tỉ lệ thấp), khai thác reward | `add-afk-rewards`, `add-monetization-hooks` |
| Mỗi bên 1–3 tướng; đầu lượt được đổi tướng (địch cũng thế) | `add-card-battle` |
| Chọn 1 trong 3 thẻ, 5 lần; các thẻ ví dụ (+10% công, +15% máu, hi sinh máu lấy công, hồi 30%, +10 mana, +10% thủ, hi sinh thủ lấy +100% công, +10 nộ) | `add-card-battle` (23 thẻ chung) |
| 1–3 thẻ nội tại mỗi tướng: chiêu (mana), ultimate (đầy nộ + mana), bị động (luôn có, hoặc khi dưới x% máu) | `add-card-battle`, `add-hero-roster` |
| Thẻ có độ hiếm; mở tướng thì có thẻ cấp 1; nâng thẻ bằng cách thu thập | `add-hero-roster` (hero-cards) |
| AFK cũng ra thẻ nhưng hiếm hơn; mở rương, ×2 tốc độ bằng reward hoặc IAP | `add-afk-rewards`, `add-monetization-hooks` |
| Cuối lượt thẻ chạy lần lượt, rồi đánh thường; có ultimate thì ra ultimate thay đòn thường | `add-card-battle` |
| Kết thúc khi một bên hết tướng, không còn hồi sinh (thẻ hồi sinh) | `add-card-battle` (hồi sinh) |
| 5 hệ Ngũ hành xung khắc | `add-card-battle`, `add-world-islands` |
| Máy pachinko: hạt EXP (cấp người chơi = cấp tướng), thẻ để tiến hóa, ô rương, tối đa 20 hoặc 30 bi một lần, nút X nhân thưởng, thẻ ×X khác nhau, Huyền thoại lần đầu ở mốc bi rồi cực hiếm | `add-pachinko-machine`, `add-hero-roster` |
| Side meta: huy hiệu hệ (thắng 5 hoặc 10 ải boss, +5% cho tướng cùng hệ, càng về sau càng khó) | `add-element-badges` |
| Side meta: đá tiềm năng (từ hòm pachinko, 4 ô mỗi tướng, khai phá tốn đá, hiếm ra ít, side quest đánh boss cày đá phải tự chơi) | `add-potential-stones` |
| Side meta: trang trại (8 tướng, năng suất và thời lượng theo sức tướng, nghỉ 15–60 phút, không dính tới ải) | `add-hero-farm` |
| Bố cục scene kiểu Clash of Critters, đảo lớn chia hệ, phong cách vẽ tay (chốt sau bản web) | `setup-unity-foundation`, `add-world-islands` |

## Đã chốt (2026-10-31)

- Người chơi luôn đi trước mỗi hiệp.
- Phật Tâm đổi thành hồi sinh 35% máu (chủ dự án để Claude quyết).
- Ô tiềm năng mở theo sao; chỗ làm trang trại mở theo cấp.
- Hang Tiềm Năng 3 lượt thắng mỗi ngày, +1 bằng quảng cáo (chủ dự án để Claude quyết).
- Không bán bi, đá tiềm năng, lượt quay máy bi.

Chốt thêm khi trả lời câu hỏi còn mở (2026-10-31, lượt 2):
- Choáng: mất trọn lượt (không chọn thẻ, không đổi tướng, không đánh; mana đầu lượt vẫn nhận). Đã sửa ở web và Unity.
- Trận Đảo Thổ dài 10–14 hiệp: chấp nhận.
- Máy bi: 30 bi mỗi đợt từ cấp 15; mốc Huyền thoại khi đã có Đại Sư Cà Sa thì cho 15 bản sao thẻ; chưa thêm thanh "hũ sắp đầy".
- Rương ra thẻ: chỉ cho tướng đã có (giữ như đang làm).
- Bảng tỉ lệ máy bi của web đọc số đo (đã sửa).
- Mở Đền Huy Hiệu sau boss Đảo Thủy: để vậy, chơi thử rồi tính.
- Thử thách huy hiệu: cấp địch tiếp tục tăng theo bậc, không chặn ở cấp 30.
- Hệ chỉ có 2 tướng: sẽ thêm tướng sau. Hiệu ứng huy hiệu trong trận: để sau.
- Giữ 3 kiểu người chơi mặc định của mô phỏng.
- Duyệt các chỗ tự chọn ở tiềm năng (hút máu mọi đòn, Thứ Bảy chọn hệ boss Hang, tướng phụ Hang, rương AFK 1 đá, dải Tiềm năng) và trang trại (lưới tạm, tự xếp theo năng suất, chấm đỏ khi vừa mở, rút giữa ca vẫn nghỉ đủ).
- AFK thôi ra bi theo giờ, học cây sinh bi của Clash of Critters: thêm Cây bi trên sảnh (change `add-ball-trees`). Trang trại đổi sang ca dài như cây.
- Mục tiêu nhịp: người chơi "vừa" xong cả 5 đảo khoảng ngày 21.
- Tướng: 8 mỗi hệ (40 tướng), chọn lại theo hệ gốc aola. Danh sách ở `13_DanhSachTuong.md`, prompt ở `ArtGen/Heroes`. Dữ liệu game chưa đổi (vẫn 11 tướng).
- Tướng (2026-11-01):
  - Mỗi tướng là một dòng tiến hóa, lên sao thì đổi hình.
  - Quái thường lấy dòng 2–4 dạng, boss lấy dòng từ 3 dạng.
  - Prompt đính ảnh tham chiếu aola, GPT vẽ lại theo style riêng và đổi chi tiết.
  - Đảo Thủy xong prompt (`ArtGen/Heroes/Thuy.md`, 21 ảnh); các hệ khác chờ chọn lại.

## Tiến độ

**Mốc 0 `setup-unity-foundation`: xong (2026-10-31).** 35/35 việc, 18 EditMode test đạt.

Chạy thử trong Unity:
1. Lần đầu (hoặc sau khi đổi dữ liệu web): menu `PokiClash/Cài đặt/1. Nhập TMP Essentials`, rồi `PokiClash/Cài đặt/2. Dựng tất cả`.
2. Mở `Assets/00 Scenes/Boot.unity`, chọn Game view `PokiClash 1080x1920`, bấm Play.
3. Đi thử tự động: `PokiClash/Thử/Đi một vòng các scene (đang Play)`; chụp 3 khung: `PokiClash/Thử/Chụp 3 khung màn hình (đang Play)` (ảnh ở `Temp/PokiShots`).

Mã nguồn:
- `Assets/01 Script/Core`: logic thuần chép từ web, không dùng UnityEngine.
- `App`, `UI`, `Game`: một assembly `PokiClash.Game`.
- `Editor`, `Tests`: công cụ và test.

Dữ liệu ở `Assets/02 Data` (JSON xuất từ web và ScriptableObject). Ảnh ở `Assets/03 Art`: ảnh gen nhập bằng menu `PokiClash/Nhập ảnh ArtGen`; chưa có thì dùng ảnh thay thế trong `Fallback/`.

**Mốc 1 `add-card-battle`: xong (2026-10-31).** 24/24 việc, 23 EditMode test đạt (luật C# khớp web ở 200 trận golden).
- Luật mới, đổi cả ở web: Phật Tâm thành "lần đầu gục: hồi sinh 35% máu"; boss của địch không hồi sinh; trận dừng ở 60 hiệp.
- Vào trận: sảnh → đảo → chạm ải → hộp chuẩn bị → Đánh. Thử nhanh: menu `PokiClash/Thử/Đánh thử ải …` (đang Play).
- Tướng hiện bằng hình giữ chỗ theo hệ. Hình aola chỉ hiện khi bật define `POKICLASH_DEV` (chưa bật).
- Số đo đảo Thổ và nhịp trận: `openspec/changes/add-card-battle/design.md`, mục "Kết quả đo".

**Mốc 2 `add-hero-roster`: xong (2026-10-31).** 12/12 việc, 31 EditMode test đạt (chỉ số 11 tướng, thẻ rơi từ rương, mảnh khớp web).
- Scene Tướng: lưới 3 cột, chấm đỏ việc chờ, hộp chi tiết có ô xem 4 clip, nâng thẻ, tiến hóa, cho vào/bỏ khỏi đội, nơi rơi mảnh.
- Sổ thẻ: cách xếp thẻ, trọng số rút theo độ hiếm, thẻ khoá theo cấp.
- Sổ tay có "Bảng thử (tua nhanh)" như bản web, chỉ hiện trong Editor và bản Development.
- Đội trống thì hộp chuẩn bị trận không cho Đánh.

**Mốc 3 `add-world-islands`: xong phần code (2026-10-31).** 17/19 việc, 36 EditMode test đạt (thưởng ải, tặng tướng, rương mốc khớp web).
- Sảnh: bảng tên 5 vùng có độ khó và tiến độ, mây trôi, mũi tên đảo gợi ý, Làng Máy Bi, 3 công trình side meta phác chì kèm điều kiện mở, hàng nút tròn, màn giới thiệu lần đầu.
- Đảo hệ: cuộn dọc, 8 ô ải theo trạng thái, nét chấm vàng, sticker đội trưởng, rương mốc, khung ải tiếp theo, hộp chuẩn bị trận (đội 3 ô, kho tướng có mũi tên khắc hệ).
- Còn 2 việc chờ ảnh đảo (Canva và ArtGen/Islands): đưa ảnh vào và soi lại toạ độ.
- Người chơi mới đi trọn Đảo Thủy bằng Tự chơi ×3: thua 10 lần trước khi qua 8 ải khi chỉ thả bi ở máy bi giữ chỗ (10 EXP mỗi bi). Đo lại ở mốc 4 với máy thật: 8 thắng, 2 thua, xong đảo ở cấp 7, đã thả 156 bi.

**Mốc 4 `add-pachinko-machine`: xong (2026-10-31).** 13/14 việc, 41 EditMode test đạt (6.000 bi: tỉ lệ từng ô lệch dưới 1 điểm phần trăm so với web, không bi nào kẹt; 600 lần mở rương khớp từng thưởng).
- Máy vẽ trên uGUI (design ghi camera riêng): khung giấy viền mực; đinh, nấm, cốc, ô vẽ một lần vào texture; bi và hiệu ứng nằm trên canvas con.
- Cột cược ×1…×10 khoá theo cấp; "Thả bi" (chạm hoặc giữ); "Thả liền 20/30"; khay "Rương chờ" (lưu trong bản lưu); thanh mốc 300 bi; bảng "Tỉ lệ" đọc số đo mô phỏng do `export_data.ts` ghi vào `balance.json`.
- Đổi ở web: `maxPerDrop` 20, từ cấp 15 là 30; mốc Huyền thoại khi đã có Đại Sư Cà Sa thì cho 15 bản sao thẻ Huyền thoại.
- Thử: menu `PokiClash/Thử/Máy bi: thả ×1 và ×3, mở rương (đang Play)`. Còn đo FPS trên máy Android thật.

**Mốc 5 `add-afk-rewards`: xong (2026-10-31).** 11/11 việc, 45 EditMode test đạt (golden AFK 42 bước khớp web từng giá trị).
- Logic viết ở web trước (`Web/src/core/afk.ts`, hộp AFK web cũng có rương và tăng tốc), chép sang `Core/Afk.cs`. Bản lưu thêm khoá `afk` (bản lưu cũ tính tiếp từ `afkSince`).
- Đồng hồ theo đoạn: tăng tốc ×2 trong 2 giờ, chặn 12 giờ, lùi giờ máy thì bỏ qua đoạn đó.
- Rương AFK: 3 giờ/rương, khay 4, đếm 2 giờ từng cái, rương kế đếm ngay khi rương trước đếm xong; bộ đếm rương không về 0 khi nhận bi.
- Hộp AFK: Nhận, Nhận ×2, Mở ngay (4 lượt/ngày), Tăng tốc ×2 (3 lượt/ngày, xám khi giờ AFK đã đầy). Quảng cáo qua `IRewardAds`, bản thử là quảng cáo giả lập 3 giây có nút "Bỏ qua".
- Thử: menu `PokiClash/Thử/AFK: tua giờ, nhận, rương, tăng tốc (đang Play)`; Sổ tay có "Tua AFK 1 giờ / 8 giờ".

**Mốc 6 `add-balance-tools`: xong (2026-10-31).** 11/12 việc, 49 EditMode test đạt.
- Cửa sổ Editor `PokiClash/Cân bằng` (không cần Play): tab Trận (một ải / một đảo / 40 ải, đội, cấp, sao, cấp thẻ, phần cộng side meta, CSV), tab Máy bi (độ rộng ô, tỉ lệ, giá trị rương, EXP / bi hoàn / thẻ mỗi bi, cảnh báo bi hoàn > 0,5, ghi tỉ lệ vào asset), tab Tiến độ (3 kiểu người chơi × 30 ngày). Menu `PokiClash/Cân bằng nhanh/...` chạy không mở cửa sổ.
- Bảng 40 ải × 5 mức cấp của Unity khớp từng ô với `npm run sim -- battle` (đã so 50 trận mỗi ô: 200/200 ô trùng; test EditMode so 6 trận mỗi ô với golden `sim.json`). 10.000 trận mất khoảng 7 giây.
- Sổ tay bản dev (Editor và Development Build): Bảng thử, Chỉnh số (16 hệ số, nút − / +, "Về số gốc"), Máy tự chơi 100 trận. Sổ tay cuộn dọc.
- Ghi trận: mỗi trận thêm một dòng vào `Logs/tran.csv` của project (máy thật: `persistentDataPath/Logs`).
- Kiểm tra trước build: file trong `App/Dev` phải bọc kín `#if UNITY_EDITOR || DEVELOPMENT_BUILD`; menu `PokiClash/Biên dịch thử bản phát hành` biên dịch script người chơi không Development.
- Web: `runBattle` nâng giới hạn vòng lặp 400 → 2000 (như golden); đội mẫu theo đảo chuyển vào `src/core/sim.ts` (`SIM_TEAMS`) và xuất sang `balance.json`.
- Mô phỏng tiến độ 30 ngày (máy + 15%, AFK và máy bi theo luật hiện tại): chăm cấp 30 ngày 3, xong cả 5 đảo ngày 3; vừa cấp 30 ngày 7, xong Đảo Thổ ngày 7; ít cấp 27 ngày 14, xong Đảo Thổ ngày 22. Bi AFK chiếm phần lớn (vừa: 51.152 bi AFK so với 5.797 bi từ ải).

**Mốc 7 `add-element-badges`: xong (2026-10-31).** 11/12 việc, 53 EditMode test đạt (đội địch 200 trận thử thách, chỉ số có phần cộng, trận thật và tiến độ khớp web).
- Logic viết ở web trước (`src/core/badges.ts`; web thêm `StatMods` cho chỉ số tướng như Unity), chép sang `Core/Badges.cs`. Bản lưu thêm khoá `badges`.
- Scene `Badges` (đã thêm vào Build Settings): 5 bệ theo hệ, danh sách trận của bậc, hộp chuẩn bị trận dùng chung, kết trận riêng (bi, tiến độ, hộp huy hiệu, rương). Sảnh: Đền tô màu khi mở, chấm đỏ khi có dãy mới. Màn Tướng: icon huy hiệu cạnh nhãn hệ, chỉ số đã gồm phần cộng.
- Công cụ: tab "Huy hiệu" ở cửa sổ Cân bằng và `npm run sim -- badges` (hai bên ra cùng số).
- Đo bằng máy tự chơi (đội mẫu của đảo cùng hệ): trận cuối mỗi bậc (3 tướng, boss là tướng hiếm nhất) gần như không thắng ở cấp kỳ vọng, nhất là dãy Thổ (boss Đại Sư Cà Sa Huyền thoại: bậc Bạc 5–18%, Ngọc 0–4%). Bậc Kim Cương dãy Thổ có địch cấp 33–38, quá cấp tối đa 30. Huy hiệu +20% cho mọi tướng nâng tỉ lệ thắng ở cấp đề nghị thấp nhất: Thủy 49% → 69%, Thổ 59% → 73%.
- Còn ảnh gen huy hiệu, nền đền, công trình đền (huy hiệu đang vẽ bằng code).

**Mốc 8 `add-potential-stones`: xong (2026-10-31).** 11/12 việc, 58 EditMode test đạt (khai phá, trần, hiệu ứng đầu trận, trận thật, Hang khớp web).
- Logic viết ở web trước (`src/core/potential.ts`, `data/potential.ts`; web thêm `BattleStart` trên `Member`), chép sang `Core/Potential.cs`. Bản lưu thêm `potentialStones`, `potential`, `potentialNew` (kết quả chờ chọn), `cave`.
- Rương bạc thêm 8% "1–2 đá", rương vàng 12% "2–4 đá" (dòng cũ giữ trọng số tương đối), rương AFK 5% "1 đá".
- Hộp chi tiết tướng có dải Tiềm năng, mở hộp khoá ô / khai phá / so sánh cũ-mới. Scene `Cave` (đã thêm vào Build Settings): hệ boss theo thứ, 4 tầng, 3 lượt thắng mỗi ngày, "+1 lượt" (quảng cáo giả lập).
- Công cụ: tiềm năng không / trung bình / trần ở tab Trận; menu đo đảo Mộc, Thổ. Đảo Thổ cấp 21: không 62%, trung bình 61%, trần 81%.
- Sửa lỗi: cấu hình mảng lồng và nullable không qua được ScriptableObject (game chạy thì rỗng); đổi sang mảng phẳng, test asset dữ liệu kiểm tra mọi cấu hình side meta.

**Mốc 9 `add-hero-farm`: xong phần code (2026-10-31).** 9/10 việc, 60 EditMode test đạt (golden trang trại 24 bước khớp web).
- Logic viết ở web trước (`src/core/farm.ts`, `data/farm.ts`; web chưa có màn trang trại), chép sang `Core/Farm.cs`. Bản lưu thêm khoá `farm`.
- 8 chỗ, mỗi chỗ hợp một hệ (×1,25); mở khi có 3 tướng, lúc mở 3 chỗ, chỗ 4–8 mở ở cấp 8, 11, 14, 17, 20. Năng suất theo độ hiếm, cấp, sao; giờ làm 2–5 giờ; rút ra nghỉ 15–60 phút; kho mỗi chỗ giữ tối đa 12 giờ sản lượng. Sức làm tách khỏi trận.
- Scene `Farm` (đã thêm vào Build Settings): lưới 8 chỗ (chưa có ảnh đảo), Thu hoạch, Tự xếp, ×2 năng suất 1 giờ (quảng cáo); danh sách chọn tướng có bi/giờ, giờ làm, hợp hệ, nghỉ còn bao lâu. Sảnh: công trình tô màu khi mở, chấm đỏ khi có tướng hết sức hoặc kho đầy.
- Đo: trang trại 19–55 bi/ngày đầu game, 93–230 giữa game, 252–515 cuối game (vào 2–8 lần mỗi ngày), so với AFK 201–850. 30 ngày người chơi "vừa": trang trại 10.952 bi, AFK 51.050, ải 5.822.
- Thử: menu `PokiClash/Thử/Trang trại: tự xếp, tua giờ, thu hoạch, đổi ca (đang Play)`; Sổ tay bản dev có "Tua trang trại 2 giờ".

**Mốc 10 `add-monetization-hooks`: xong phần code (2026-10-31).** 11/12 việc (còn gắn SDK thật), 68 EditMode test đạt.
- Logic viết ở web trước (`src/core/ads.ts`, `data/ads.ts`), chép sang `Core/AdGate.cs`. Mọi quảng cáo đi qua `Ads.Show(chỗ đặt)`: giới hạn mỗi ngày theo spec (Nhận ×2 không giới hạn; Mở ngay 4; Tăng tốc AFK 3; ×2 trang trại 3; +1 lượt Hang 1), xem xong mới trừ lượt, bỏ ngang không trừ, lùi giờ máy không mở lại lượt. Bộ đếm riêng của AFK, trang trại, Hang bỏ đi.
- Bản lưu lên v3 (web và Unity), có bước di chuyển: bộ đếm quảng cáo cũ dồn về `ads`; file `save_v2.json` của bạn sẽ tự chuyển lên v3 khi mở game, bản cũ giữ thành `.bak`.
- Sổ tay có mục "Gói hỗ trợ": Thẻ Phiêu Lưu 30 ngày (bi AFK ×1,5, khay 5 ô, rương mở 1 giờ; mua tiếp thì cộng dồn hạn) và Bỏ quảng cáo (nhận thưởng ngay, vẫn theo giới hạn mỗi ngày). Không bán bi, đá, lượt quay; test rà danh sách gói.
- Quảng cáo giả lập và cửa hàng giả lập chuyển vào `App/Dev` (chỉ Editor và bản Development). Bản phát hành chưa gắn SDK thì nút quảng cáo và mục gói ẩn.
- Thử: menu `PokiClash/Thử/Gói hỗ trợ: Thẻ Phiêu Lưu, hết lượt quảng cáo, Bỏ quảng cáo (đang Play)`; Sổ tay bản dev có "Đặt lại lượt QC", "Bỏ gói đã mua".

**Sau mốc 10: chốt câu hỏi, change `add-ball-trees` (2026-10-31).** 70 EditMode test đạt.
- Choáng mất trọn lượt; golden trận xuất lại, Unity khớp web.
- **Cây bi** trên sảnh (cạnh Trang trại):
  - 5 cây, cây 1 mở khi qua ải 1, cây 2–5 khi qua boss Thủy, Hỏa, Kim, Mộc;
  - mỗi cây 5 bi/giờ, chứa 50, đầy thì ngừng; "Hái", "Hái ×2" (quảng cáo, 3 lần/ngày);
  - Thẻ Phiêu Lưu tăng cây ×1,5 (cả tốc độ và sức chứa).
- **AFK** chỉ còn mảnh tướng, rương AFK, tăng tốc; nút "Nhận mảnh". Bỏ "Nhận ×2".
- **Trang trại:** ca 8 giờ (+1 giờ mỗi sao), kho 10 giờ, 2 bi/giờ gốc, không tăng theo cấp. Đo:

  | Giai đoạn | Trang trại (bi/ngày) | Cây bi (bi/ngày) |
  |---|---|---|
  | Đầu game | 68–149 | 159–215 |
  | Cuối game | 284–537 | 399–539 |

- Đường cong cấp vào cấu hình (`expBase` 40, `expPow` 1,35, chưa đổi số). Menu mới `PokiClash/Cân bằng nhanh/Quét nhịp: EXP lên cấp, cây bi, trang trại`.
- **Nhịp chưa đạt mục tiêu:** người chơi "vừa" vẫn xong 5 đảo ở ngày 6, dù bi thụ động 30 ngày giảm từ 62.002 xuống 37.329. Xem câu hỏi 1.
- Thử: menu `PokiClash/Thử/AFK và cây bi: tua giờ, hái, mảnh, rương, tăng tốc (đang Play)`.

**Mốc 12 `convert-to-prefabs`: xong (2026-11-02).** Chủ dự án: mọi thứ trong game là prefab, kể cả UI, runtime không sinh gì. Đã nướng một lần bằng chính code dựng cũ, code runtime chỉ gán dữ liệu vào tham chiếu kéo thả, rồi xoá code dựng: prefab giờ là nguồn gốc, chỉnh trong Editor.
- Tài nguyên vẽ bằng code đã thành asset ở `Assets/03 Art/Baked`:
  - 27 sprite giấy và mực (5 hình tướng giữ chỗ đã bỏ 2026-11-02: tướng chỉ dùng hình aola, không có thì để trống);
  - nhiễu nét rung, mặt tĩnh máy bi;
  - 18 material chữ viền, 23 tiếng WAV.
- `Assets/04 Prefabs`:
  - `Kit/`: nút 5 cỡ, khung, chip, thanh, nhãn hệ, sao, băng keo, con dấu, gợi ý, thẻ, chân dung, huy hiệu, rương, canvas;
  - `App/App.prefab` (trong `Boot.unity`);
  - `Screens/`: 11 màn, mỗi scene chức năng chỉ chứa prefab màn của nó;
  - `Dialogs/`: tờ giấy gốc `HopThoai` và các biến thể của nó;
  - `Items/`: phần lặp theo dữ liệu.
- Hộp mở từ nhiều nơi nằm trong `UiKit.dialogs`, mở bằng `App.Modals.Open<T>()`.
- `Nhập ảnh ArtGen` tự thay ảnh thay thế bằng ảnh gen cùng tên trong mọi prefab. Có thêm menu riêng `PokiClash/Đổi ảnh thay thế trong prefab`.
- Kiểm:
  - 72 EditMode test đạt, gồm test chặn `PrefabOnlyTests`: quét mã runtime, ngoại lệ duy nhất là hình aola bản dev;
  - `Kiểm tra trước build` và `Biên dịch thử bản phát hành` đạt;
  - vòng `Chạy mọi menu thử` chạy đủ 112 ảnh, không lỗi.
- Ảnh vòng thử so với ảnh trước khi đổi: phần còn lệch đều có lý do ngoài code giao diện:
  - hạt giống máy bi ngẫu nhiên, thẻ rút ngẫu nhiên;
  - AFK theo giờ thật, Hang theo thứ trong tuần;
  - mây trôi, bản lưu trôi giữa các lần chạy.
- Sửa kèm: bộ lọc nhập ảnh `ArtImporter` từng đè lên ảnh nướng.
  - Hậu quả: ép cỡ 1024 nên mặt máy bi mờ; nén ASTC trên Android; nhiễu nét rung thành Clamp nên nét gần như đứng yên; danh mục ảnh lẫn sprite nướng.
  - Nay `ArtImporter` bỏ qua `Baked/`, cách nhập đã đặt lại.
  - Nét rung giờ đúng như bản gốc, nên ảnh chụp từ 2026-11-01 lệch khoảng 1% ở viền giấy.

## Câu hỏi còn mở (gom từ các design.md; đánh số lại sau lượt trả lời 2026-10-31)

1. **Nhịp tiến độ** (mục tiêu: người chơi "vừa" xong 5 đảo khoảng ngày 21). Sau khi có cây bi vẫn là ngày 6. Quét bằng menu `Quét nhịp`:
   - EXP lên cấp ×6: ngày 15;
   - EXP ×2, bi thụ động ×0,5, "Hái ×2" 1 lần/ngày: ngày 13;
   - ở các tổ hợp mạnh tay đó, người chơi "ít" không xong trong 30 ngày.

   Sức mạnh chủ yếu đến từ sao tiến hóa và cấp thẻ: 40–43 lần tiến hóa trong 30 ngày ở mọi tổ hợp, vì thẻ đến từ rương máy bi. Chọn hướng:
   - tăng giá thẻ và tiến hóa (bản sao mỗi cấp thẻ, thẻ mỗi sao);
   - giảm thẻ trong rương;
   - giảm tiếp bi thụ động;
   - hay nhận nhịp nhanh hơn và thêm ải, tướng sau?
2. **Trang trại** có ra thêm EXP không?
3. **Kiếm tiền:** chọn SDK nào (quảng cáo, IAP)? Giá hai gói?
4. **Kỹ thuật:** chốt Unity 6 bản vá nào? Có cần Addressables cho ảnh đảo không?
5. **Hình aola:** (2026-11-02, người dùng bảo "ghép hình aola các tướng đã chọn vào game, cả animation đánh") giờ Editor lúc Play luôn nạp hình aola từ thư mục reskin (tự tìm trên ổ đĩa), không cần define, không đổi ProjectSettings; bản build vẫn chỉ nạp khi có `POKICLASH_DEV`. Hình vẫn KHÔNG nằm trong Assets vì `PreBuildCheck` và test `KhongCoHinhAolaTrongAssets` chặn hình Baitian trong bản phát hành. Còn hỏi: có muốn nhập hình aola vào Assets để chạy trên máy thật (phải bỏ luật chặn đó, hình Baitian sẽ vào bản build) không?
6. **ProjectSettings:** giữ hay hoàn các thay đổi màn dọc do `BanThuSetup.cs` cũ ghi vào `ProjectSettings.asset`?
7. **Công cụ dev** bọc theo `UNITY_EDITOR || DEVELOPMENT_BUILD` (có cả trong bản Development) thay vì `POKICLASH_DEV` như design ghi, vì define đó gắn với hình aola. Được không?
8. **Máy bi và AFK, các chỗ tự chọn cần duyệt:**
   - máy bi: gộp bản sao cùng thẻ "×n", hộp "Huyền thoại!" sau rương cuối, lên cấp khi rời máy chỉ báo bằng thông báo;
   - AFK: bộ đếm rương không về 0 khi nhận, rương kế đếm khi rương trước đếm xong, khay đầy giữ tiến độ, tăng tốc xám khi đầy giờ, mảnh AFK từ mọi boss đã gặp, tăng tốc 3 lần/ngày.
9. **Kiếm tiền, các chỗ tự chọn cần duyệt:**
   - Thẻ Phiêu Lưu tăng cây bi ×1,5 cả tốc độ lẫn sức chứa (không nhân mảnh, không tác động trang trại và Hang);
   - mua thẻ khi còn hạn thì cộng dồn;
   - Bỏ quảng cáo vẫn trừ lượt mỗi ngày;
   - hết lượt thì nút xám, bỏ hình TV;
   - cửa hàng giả lập mua ngay, không hỏi lại;
   - bản lưu lên v3.
10. **Cây bi, các chỗ tự chọn cần duyệt:**
    - 5 cây (Critters có 8), mở theo boss đảo;
    - "Hái ×2" 3 lần/ngày (Critters không có);
    - hái một lần cho mọi cây (Critters hái từng cây);
    - cây mới mở bắt đầu từ lần tính sau;
    - không có trần kho bi (Critters chặn hái khi đã có 420 bi).
11. **Prefab, hình aola bản dev** (`convert-to-prefabs`): `AolaActor` và `AolaSticker` đọc PNG và json từ thư mục aola ngoài project lúc chạy, tạo quad, material, RenderTexture. Giữ ngoại lệ này (chỉ bản dev, test chặn bỏ qua), hay nhập hình vào project thành asset (loại khỏi bản phát hành)?
12. **Prefab, scene thử cũ `BanThu`:** không chuyển sang prefab (đã bỏ hướng xếp khối). Để nguyên hay xoá?
13. **Prefab, cấu trúc (đã chuyển hết theo cách này):** mỗi hộp thoại là biến thể (prefab variant) của tờ giấy gốc `Dialogs/HopThoai`; mỗi màn là `Screens/<Scene>.prefab`; phần lặp theo dữ liệu là `Items/*.prefab`; tên GameObject giữ tiếng Việt không dấu như cũ. Code nướng đã xoá nên sửa giao diện là sửa prefab. Phần có số lượng theo dữ liệu nhưng dựng sẵn cố định trong prefab (5 đảo ở sảnh, 5 nút cược máy bi, 5 nút chọn hệ ở Hang, 3 ô đội hình) phải thêm tay nếu dữ liệu tăng. Ổn chưa?
14. **Menu thử Tướng** báo "Lệch chỉ số: màn Tướng 1039/471/119, trận 1191/357/95" (có từ trước khi đổi sang prefab): màn Tướng và trận tính chỉ số khác nhau khi tướng có huy hiệu, tiềm năng. Cần xem lại phần nào đúng.

## Ảnh cần gen

Gói prompt ở `ArtGen/` (gốc dự án), theo quy trình cũ: đọc `PROMPTS.md`, gen bằng GPT (hoặc Tripo cho đảo 3D), lưu vào `inbox/` của gói. Danh sách gói và thứ tự gen: `ArtGen/README.md`.
