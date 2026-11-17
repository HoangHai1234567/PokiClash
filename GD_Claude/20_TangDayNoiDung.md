# Tăng dày nội dung (2026-11-17)

Người dùng dặn 2026-11-17 (kèm ảnh hộp chi tiết Pháo Giáp và màn Tướng ở cấp 200):

1. Tăng dày nội dung Đền Huy Hiệu và Tiềm năng. Trang trại đã có plan, chưa đụng.
2. Tiến hóa dày hơn, kiểu Clash of Critters: đủ 5 sao Đồng mới tiến hóa; lên sao bằng mảnh tướng, tiến hóa tốn đá tiến hóa (từ rương, thưởng ải; sau này thêm mỏ trong trang trại, chưa làm). Mốc tiến hóa hợp với tiến độ cấp nhưng đủ khó, không dễ lên tối đa một tướng.
3. Thêm nhiều thẻ bài để không lặp; dày thêm logic trận. Boss dạng 1 "chết" là dạng 2 hiện ra ngay, chưa mượt: phải có animation chết, polish gameplay thật kỹ.
4. Chia rõ độ hiếm của từng tướng; chỉ số từ 1000 trở lên ghi theo k (1k, 2k, 3.3k…).
5. Bộ lọc, xếp ở màn Tướng.
6. Lực chiến boss cuối đảo (tướng đã thu) phải cách xa tướng thứ 9 (Thủy: 600k so với 576k), vì càng về sau càng khó.
7. Chia nhiều agent làm.

## Quyết định (Claude chốt, người dùng duyệt sau)

### Bậc sao và tiến hóa

- **4 bậc × 5 sao = 20 nấc**: Đồng 1–5, Bạc 1–5, Vàng 1–5, Kim Cương 1–5. `HeroProg.star`, `Member.star` là **sao tổng 1..20** (`Core/StarTier.cs`).
- **Lên sao trong bậc** (Đồng 1★ → 2★ …): tốn **mảnh tướng**. Mảnh của tướng đã có dồn vào `HeroProg.shards` (thôi đổi thành bản sao thẻ), trừ khi tướng đã 20 sao thì đổi bản sao thẻ như cũ. Giá mảnh tăng theo bậc và độ hiếm.
- **Tiến hóa** (đủ 5★ của bậc → 1★ bậc sau): tốn **đá tiến hóa** (`SaveData.evoStones`) và cần **cấp người chơi** tối thiểu theo bậc. Bỏ điều kiện "tổng cấp 3 thẻ" của sao; thẻ riêng vẫn lên cấp bằng bản sao, độc lập.
- **Đổi dạng**: `formStars` = 6, 11 (dạng 2 ở Bạc 1★, dạng 3 ở Vàng 1★). Kim Cương giữ dạng cuối.
- **Chỉ số**: mỗi sao trong bậc cộng ít, mỗi lần tiến hóa là một cú nhảy rõ.
- **Nguồn đá tiến hóa**: rương máy bi (bạc ít, vàng nhiều), rương mốc đảo, lần đầu qua ải tướng / mini boss / boss (boss nhiều nhất), qua lại ải boss tỉ lệ nhỏ, rương AFK ít, rương bậc của Đền Huy Hiệu. Mỏ trong trang trại: để sau.
- **Bản lưu v12**: sao cũ 1..5 đổi sang 1, 3, 6, 8, 11 (giữ dạng đang có).
- **Địch**: `Teams.EnemyStar(level)` theo thang mới, bám sao kỳ vọng của người chơi ở cấp đó (đo bằng ProgressSim).
- **Độ khó mục tiêu**: người chơi "vừa" lên Bạc cho tướng chủ lực trong đảo đầu, Vàng khoảng giữa game, không max (Kim Cương 5★) được tướng nào trước khoảng ngày 45–60. Số cụ thể đo bằng máy, báo lại.

### Độ hiếm và khoảng cách lực chiến

- Độ hiếm tăng theo suất ải trong đảo: ải 1, 5 Thường; 10, 15 Khá; 20, 30 Hiếm; 40, 50, 60 Sử thi; **ải 70 (boss cuối đảo) Huyền thoại**. Đảo Thủy đã đúng phân bố, chỉ sai chỗ (Hàn Ngạc Huyền thoại ở ải 60, Hải Long Sử thi ở ải 70).
- Giãn `HeroStats.RarityPower` để cùng cấp, cùng sao, Huyền thoại hơn Sử thi ít nhất khoảng 30% lực chiến; các bậc dưới giãn đều.
- Địch vẫn quy về sức tướng Khá cùng cấp, nên phải đo lại tỉ lệ thắng ải sau khi đổi.

### Hiển thị

- `Core/NumFmt.Short`: dưới 1000 giữ nguyên, rồi 3.3k, 57.6k, 602k, 1.43M. Dùng cho chỉ số và lực chiến ở mọi chỗ hiện ra (thẻ tướng, đội hình, hộp chi tiết, hộp chuẩn bị, màn VS, đối thủ).
- Độ hiếm rõ: khung, dải màu, nhãn theo độ hiếm trên thẻ tướng; lọc và xếp ở màn Tướng.
- `UiStars.SetTiered(star)`: 5 sao tô màu bậc (Đồng, Bạc, Vàng, Kim Cương).

## Hợp đồng chung (đã có trong code, đừng đổi tên)

- `Core/StarTier.cs`: `PerTier` 5, `Count` 4, `MaxStar` 20, `Tier(star)`, `InTier(star)`, `Name(tier)`, `Star(tier, inTier)`, `AtEvolveGate(star)`, `Label(star)`.
- `Core/NumFmt.cs`: `NumFmt.Short(double|int)`.
- `SaveData.evoStones` (khoá JSON `evoStones`, đã đọc, ghi).
- `RewardKind.EvoStones` (cuối enum), dòng bảng rương khoá `"evo"`; `StageReward.evoStones`, `Progress.ZoneChest.evoStones`.
- `UiStars.SetTiered(int star)`, `UiStars.TierColor(tier)`.
- API agent A viết trong `Core/Progress.cs` (UI gọi theo đúng tên này):
  - `int ShardCost(BalanceConfig cfg, HeroDef h, int toStar)`: mảnh để lên sao `toStar` trong bậc;
  - `bool CanStarUp(SaveData s, GameData d, string hero)`, `bool StarUp(SaveData s, GameData d, string hero)`;
  - `(int stones, int level) EvolveCost(BalanceConfig cfg, HeroDef h, int toTier)`;
  - `bool CanEvolve(SaveData s, GameData d, string hero)`, `bool Evolve(SaveData s, GameData d, string hero)` (đổi chữ ký: `GameData` thay `BalanceConfig`);
  - `enum StarStep { Max, StarUp, Evolve }`, `StarStep NextStep(SaveData s, GameData d, string hero)`.

## Chia việc

| Agent | Việc | Giữ file (chỉ agent này sửa) |
|---|---|---|
| A, Tiến hóa | Bậc sao, đá tiến hóa, mảnh lên sao, nguồn đá, bản lưu v12, sao của địch, độ hiếm theo suất ải, giãn RarityPower, đo nhịp bằng ProgressSim; UI tiến hóa trong hộp chi tiết, thanh tiến hóa, ô thưởng đá | `Core/Progress.cs`, `StarTier.cs`, `HeroStats.cs`, `Battle/Teams.cs`, `Pachinko.cs`, `Afk.cs`, `ProgressSim.cs`, `Sim.cs`, `Islands.cs`, `SaveData.cs`, khối `progression` + bảng rương trong `balance.json`, `rarity` trong `heroes.json`; `Game/Heroes/HeroDetailDialog.cs`, `EvolutionStrip.cs`, `UI/Kit/UiStars.cs`, `App/Chest/*`, `Game/Machine/MachineChestOpen.cs`, `App/TopBars.cs`; test Progression, Roster, Save, Pachinko |
| B, Huy hiệu + Tiềm năng | Đền thêm bậc, sao từng trận, đặc tính theo hệ; tiềm năng thêm loại, thêm ô theo bậc sao, bộ (set), đá tinh, Hang thêm tầng | `Core/Badges.cs`, `Core/Potential.cs`, khối `badges`, `potential`, `cave` trong `balance.json`, `App/Scenes/Badge*.cs`, `Cave*.cs`, `Game/Potential/*`, `Game/Badges/*`; test Badge, Potential |
| C, Thẻ bài + luật trận | Thêm thẻ chung (35 → khoảng 75), cơ chế mới trong bộ máy trận, máy chọn thẻ; boss tiến hóa khi gục thay vì dưới 25% máu | `cards.json`, `Core/Battle/Battle.cs`, `BattleAi.cs`, `BattleTypes.cs`, `Core/CardText.cs`, enum hiệu ứng trong `Core/Types.cs`, `App/Scenes/Card*.cs`; test BattleGolden (chỉ sửa kỳ vọng, không tính lại golden) |
| D, Trình diễn trận | Animation chết, chuỗi tiến hóa boss (chết → biến hình → ra sân), chuyển tướng, nhịp lượt, polish cảm giác | `Game/Battle/BattleView.cs`, `BattlePlayer.cs`, `BattleController.cs`, `ArenaAnim.cs`, `BattleIntro.cs`, `StageView.cs` (dùng chung với phiên làm FX tướng, sửa từng chỗ), `App/Scenes/BattleScene.cs` |
| E, Màn Tướng | Độ hiếm rõ trên thẻ tướng, lọc và xếp, số gọn ở mọi chỗ hiện | `App/Scenes/HeroesScene.cs`, `Game/Heroes/HeroTile.cs`, `App/Scenes/TeamLineup.cs`, `TeamPickerDialog.cs`, `PrepRosterCell.cs`, `PrepFoe.cs`, `StagePrepDialog.cs`, `Game/Battle/VsFace.cs` |

File dùng chung giữa nhiều agent (`Core/BalanceConfig.cs`, `Core/Types.cs`, `balance.json`): mỗi agent chỉ sửa khối của mình, đọc lại đoạn đó ngay trước khi sửa, sửa bằng thay chuỗi từng chỗ.

## Luật làm việc của đợt này

- **Không điều khiển Unity Editor** (không refresh, không chạy menu, không Play, không chạy test trong Unity): một phiên khác đang dùng Unity nhập tướng đảo Thổ, và nhiều agent cùng biên dịch sẽ giẫm nhau. Claude chính chạy Unity một lượt khi gom.
- **Soát ngoài Unity**:
  - `corec.sh <thư mục ra> [runner.cs …]`: biên dịch `Core` (C# thuần) bằng csc đi kèm Unity rồi chạy runner bằng mono (đọc JSON ở `Assets/02 Data/Json`, xem `smoke.cs`).
  - `gamec.sh <thư mục ra>`: soát lỗi biên dịch cả assembly `PokiClash.Game` (App, Game, UI).
  - Hai script nằm ở `C:\Users\Admin\AppData\Local\Temp\claude\f0d219082acbfb1c\a421a1d5-0736-433a-a46d-228b248fa453\scratchpad\corec\`. Mỗi agent dùng thư mục ra riêng. Lỗi ở file của agent khác (đang sửa dở) thì ghi lại, đừng sửa hộ.
  - In chữ Việt từ runner: đặt `Console.OutputEncoding = System.Text.Encoding.UTF8` hoặc ghi ra file.
- **Prefab**: UI là prefab nướng sẵn, runtime không sinh đồ vật (`PrefabOnlyTests`). Đổi bố cục thì viết menu dựng trong `Editor/` (chạy lại được nhiều lần, theo mẫu `EvolutionStripMenu.cs`, `PopupUiMenu.cs`), **không chạy**, ghi tên menu vào báo cáo.
- **Golden** (`Assets/02 Data/Golden`): không tính lại; ghi golden nào sẽ đổi. Claude chính tính lại một lần khi gom.
- **JSON chung** (`balance.json`, `heroes.json`, `cards.json`): sửa từng chỗ bằng thay chuỗi, không đọc rồi ghi lại cả file bằng script (phiên khác cũng đang sửa `heroes.json`, `cards.json` cho tướng đảo Thổ).
- **Không đụng**: `ArtGen/**`, `Assets/03 Art/Heroes/**`, file `.atomik`, prefab tướng, `Game/Battle/Hat*.cs` (FX từng tướng của phiên khác). Không gen ảnh; icon tạm lấy sprite có sẵn hoặc vẽ bằng code.
- Không commit git. Chữ trong game tiếng Việt có dấu.

## Kết quả (2026-11-17)

### Tiến hóa (A)

- `balance.json` `progression`: `maxStar` 20, `formStars` 6, 11, `saveVersion` 12.
- Hệ số chỉ số: `tierPower` 1 / 1,25 / 1,55 / 1,9 × (1 + 0,025 × sao trong bậc). Mỗi sao +2,5%, mỗi lần tiến hóa +11–14%.
- Giá mảnh (tướng Khá): Đồng 4/6/8/12, Bạc 14/18/22/26, Vàng 28/34/40/48, Kim Cương 40/50/60/70 (tổng 480). Nhân theo độ hiếm 0,8 / 1 / 1,15 / 1,3 / 1,5.
- Tiến hóa: 20 / 55 / 120 đá, cần cấp 30 / 95 / 150.
- Nguồn đá:
  - lần đầu qua ải tướng 1, mini boss 3, boss cuối đảo 8; qua lại mini boss 10%, boss 25%;
  - rương mốc đảo 2, 2, 3, 3, 4, 4, 10 (28 mỗi đảo);
  - rương máy bi bạc và vàng, rương AFK (dòng `"evo"`);
  - Đền, Hang (B) tối đa khoảng 94.
- Mảnh AFK 0,08 → 0,4 mỗi giờ (không thì tướng chủ lực không lên sao được).
- `RarityPower` 1 / 1,1 / 1,23 / 1,38 / 1,76: Huyền thoại hơn Sử thi cùng cấp, cùng sao 35–39% lực chiến (cấp 200, 1 sao: Hải Long 588k, Hàn Ngạc 434k).
- Độ hiếm đổi: Hải Long Sử thi → Huyền thoại, Hàn Ngạc Huyền thoại → Sử thi, Hải Đăng Thường → Khá. Ải 1 giữ Khá (luật 5 tướng khởi đầu cùng Khá).
- Sao của địch bám sao trung bình đội người chơi "vừa": Bạc ở cấp 35, Vàng ở cấp 140, cao nhất Vàng 5 sao.
- Đo `ProgressSim` 60 ngày, ngày tướng mạnh nhất đạt mốc:

  | Người chơi | Bạc 1 | Vàng 1 | Kim Cương 1 | Kim Cương 5 |
  |---|---|---|---|---|
  | Chăm | 5 | 19 | 38 | 58 |
  | Vừa | 8 | 21 | 37 | 58 |
  | Ít | 25 | chưa tới | – | – |

### Huy hiệu, tiềm năng (B)

- Đền 10 bậc (thêm Hồng Ngọc, Lục Bảo, Tử Tinh, Nhật Nguyệt, Thần Thoại), 78 trận mỗi dãy, địch cấp 66–205.
- Mỗi trận 1–3 sao (thắng; không ai gục; thắng trong 2 hiệp mỗi địch), mốc quà mỗi 30 sao.
- Đặc tính hệ từ bậc 4: Kim chí mạng, Mộc hút máu, Thủy khiên đầu trận, Hỏa nộ đầu trận, Thổ giảm sát thương.
- Tiềm năng 6 ô (mở ở sao 1, 3, 6, 8, 11, 16); 3 loại mới (khiên đầu trận, giảm sát thương, né); bộ Cuồng Chiến / Kiên Thành / Phong Ảnh (3 và 5 dòng); đá tinh (mọi ô từ Hiếm trở lên); trần Công/Thủ/Máu 30%; Tốc thôi quay ra (trận không dùng tốc).
- Hang 10 tầng (cấp 29–195), thưởng lần đầu có đá tinh, đá tiến hóa.
- Đo: side meta "vừa" bằng khoảng +4–5 cấp ở ải đảo, trần +13–14 cấp.

### Thẻ bài, luật trận (C)

- 75 thẻ chung (thêm 40), rải tới cấp 190. Thẻ trong bộ rút: cấp 10 có 33, cấp 60 có 60, cấp 200 có 75.
- Cơ chế mới: độc cộng dồn (lan khi gục, kích nổ), phản đòn, kết liễu, combo theo nhóm thẻ, cộng hưởng hệ, khắc hệ, cường hóa thẻ kế, chặn hồi máu, liều theo máu đã mất, đập khiên.
- Boss tiến hóa khi máu về 0 (sát thương thừa bỏ); `bossEvoEarly` 0,75 giữ tổng máu phải đánh như cũ.
- Lượt chọn trùng thẻ 29% → 9,5%; tỉ lệ thắng ải lệch ≤ 4,7 điểm (mô hình `Sim.StarterIsland`).
- Thẻ riêng Hải Long lên Hiếm / Huyền thoại / Sử thi (sức thẻ chưa đổi).

### Trình diễn trận (D)

- Lỗi gốc: clip chết, ra sân chạy theo nhịp sân ×3 nên clip chết 2 giây chỉ diễn 0,66 giây, rồi tướng kế thay hình ngay.
- Nay: clip chết chạy trọn rồi mới tới tướng kế; tướng mới vào bằng clip ra sân; đầu trận ra sân lúc màn VS tách; chuỗi boss tiến hóa (chết, tụ sáng, chớp, "TIẾN HÓA!", ra sân, máu dâng) khoảng 3 giây; số sát thương so le không đè; hiện độc, phản đòn, chặn hồi.

### Màn Tướng (E)

- Khung thẻ theo độ hiếm (Huyền thoại cam dày nhất có vương miện, Sử thi tím gạch sáp, Hiếm xanh dương, Khá xanh lá, Thường xám), nhãn viên màu.
- Hàng lọc hệ, nút xếp (Lực chiến, Độ hiếm, Sao, Cấp thẻ, Hệ) và đảo chiều, nhớ bằng PlayerPrefs.
- Số gọn `NumFmt.Short` ở mọi chỗ hiện chỉ số, lực chiến, máu, sát thương.

### Gom trong Unity

- Biên dịch sạch; Nhập dữ liệu (57 tướng, 75 thẻ chung, 350 ải).
- Menu dựng đã chạy: thanh tiến hóa, hộp chi tiết tướng (bậc sao, mảnh, đá), Tiềm năng 6 ô, Đền Huy Hiệu, dấu độc trên sân, màn Tướng (độ hiếm, lọc, xếp).
- Golden tính lại ngoài Unity (`progression`, `pachinko`, `afk`, `zones`, `roster`, `islands`, `sim`, `battles`, `battle_events`, `cardtext`, `badges`, `potential`); test thuần Core 110/110 đạt ngoài Unity.

### Người dùng chốt (2026-11-17)

- Cà Sa: sẽ thay tướng khác sau, chưa cần nguồn mảnh.
- Địch dừng ở Vàng 5 sao: đồng ý. Tên 5 bậc đền mới, bậc 10 địch cấp 205: đồng ý.
- Mức side meta, luật trận Claude tự chốt (độc theo Công và lan khi gục, phản đòn hạ gục được, cộng hưởng không tính lính, kết liễu boss ×2): để Claude quyết, giữ như trên.
- Tốc: "không còn chỗ nào dùng thì bỏ". Trận, máy chọn thẻ, trang trại đều không dùng tốc, nên đã bỏ:
  - ẩn ô Tốc ở hàng chỉ số hộp chi tiết tướng (`HeroDetailDialog.DropSpeedGroup`) và khung Đội hình (`Ui.DropLastCell`);
  - bỏ Tốc khỏi tiềm năng (trọng số 0, không thuộc bộ Phong Ảnh); dòng Tốc trong bản lưu cũ đọc thành Công cùng độ hiếm.
  - `Stats.spd` vẫn giữ trong Core để golden trận không đổi.
- Thẻ riêng Hải Long (Claude quyết): theo mẫu tướng Huyền thoại.
  - Chiêu: 140% Công, 40 mana, 30% làm choáng.
  - Tuyệt kỹ: 300% Công, giảm 20% Thủ địch.
  - Bị động: mỗi đầu lượt khiên 5% máu, +6 mana.
  - Golden đã tính lại.
- Chuỗi tiến hóa 3 giây: ổn. Màu Huyền thoại: tạm giữ cam.
