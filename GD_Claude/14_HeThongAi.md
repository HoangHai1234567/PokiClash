# Hệ thống ải mới: 70 ải mỗi đảo, 10 tướng mỗi đảo

Viết 2026-11-02. Chủ dự án chốt hướng; bản thử chạy ở đảo Thủy trên web (`Web/`). Unity vẫn dùng 8 ải mỗi đảo cho tới khi chép sang.

## Vì sao

Mỗi đảo một tướng mới thì không đủ nội dung cho người chơi cày. Hướng mới: mỗi đảo dài 70 ải và có 10 tướng. Các ải xen giữa dùng lại tướng đã gặp, ở dạng mạnh hơn hoặc theo nhóm, cùng một loại quái mới là **lính**.

## Luật

- **Ải tướng** (ra mắt tướng mới): 1, 5, 10, 15, 20, rồi cứ 10 ải một tướng: 30, 40, 50, 60, 70.
  - Ải 1: người chơi đánh với **bóng của chính tướng khởi đầu** (Giọt Sương, yếu đi 20%).
    - Từ 2026-11-03 (`15_TuongKhoiDau.md`): ải 1 luôn là Giọt Sương; người chọn tướng khởi đầu khác đấu với Giọt Sương thật và thu phục được (rơi 2–4 mảnh).
  - Ải 5, 10, 15: tướng mới, cường hóa +15%.
  - Ải 20–60: tướng mới là mini boss.
  - Ải 70: boss đảo, tiến hóa trong trận (thẻ Tiến Hóa như boss ải 8 cũ).
  - **Tiến hóa trong trận ở ải 5–60** (người dùng dặn 2026-11-04): tướng mới của ải tướng cũng tiến hóa hết dòng như boss ải 70 (cờ `evo` trong `stages.json`):
    - vào trận ở dạng 1;
    - máu cả dòng cộng lại bằng 1,5 lần, chia cho các dạng theo tỉ lệ 1 : 2 (: 3);
    - Công các dạng trước kém 10% mỗi dạng;
    - máu dưới 25% thì lên dạng sau và hồi đầy máu.
    - Mini boss tiến hóa lấy máu ×0,7 như boss ải 70, thay cho ×0,95.
    - Ải 1 (bóng tướng khởi đầu) không tiến hóa.
    - Đòn kết liễu (đánh hoặc bỏng) giáng vào tướng còn dạng sau, kể cả khi nó đang trên 25% máu: chừa 1 máu rồi tiến hóa ngay, không gục (người dùng dặn 2026-11-04).
  - Hộp Chuẩn bị trận (người dùng dặn 2026-11-04):
    - hiện to Máu, Công, Thủ khi vào trận của từng địch, kèm lực chiến;
    - không so với tướng người chơi, vì dễ hiểu lầm;
    - tướng tiến hóa chỉ hiện dạng đầu; đầu mục ghi "còn 25% máu thì tiến hóa, hồi đầy máu"; lực chiến tính cả dòng.
- **Chặng**: từ một ải tướng tới trước ải tướng sau. Tên chặng là tên địa danh, ví dụ ải 23 là "Ngọn Hải Đăng 4".
- **Ải xen giữa** trộn 3 kiểu:
  - tướng đã gặp được **cường hóa** (+% Máu và Công, Thủ cộng một nửa);
  - **nhóm 2–3 con** (tướng và lính, hai tướng, bầy lính);
  - **lính**: quái không thu thập được, chỉ để gây khó.

### Mẫu ải xen giữa

H là tướng của chặng này, P là tướng chặng trước, Q là tướng hai chặng trước. M và N là hai loại lính khác nhau, xoay vòng theo số ải. Tướng khởi đầu của người chơi chỉ xuất hiện ở ải 1.

| Vị trí trong chặng | Chặng ngắn (5 ải: 5–9, 10–14, 15–19) | Chặng dài (10 ải: 20–29 … 60–69) |
|---|---|---|
| +1 | Bầy lính: M, N | Bầy lính: M, N |
| +2 | Cường hóa: H +12% | Cường hóa: H +12% |
| +3 | Tướng và lính: P, M | Tướng và lính: P, M |
| +4 | **Cửa ải**: H +15%, M | Bầy lính: M, N, M (mỗi con −20%) |
| +5 | | Hai tướng: H, Q |
| +6 | | Cường hóa: H +25% |
| +7 | | Lính tinh nhuệ: N +40%, M |
| +8 | | Tướng và lính: H, M, N (mỗi con −20%) |
| +9 | | **Cửa ải**: H +10%, P +10% |

Chặng đầu (ải 2–4) chỉ có lính, để tập: 1 cua; 2 cua (mỗi con −25%); 1 cua +25%.

Nhóm 3 con bị yếu đi 20% mỗi con: người chơi chỉ mang 1 tướng suốt đảo đầu (ô đội 2 mở khi xong đảo), phải đánh lần lượt cả 3 con.

**Đổi 2026-11-03 (Unity, `15_TuongKhoiDau.md`):**
- Ô đội mở theo cấp người chơi: ô 2 ở cấp 10, ô 3 ở cấp 30. Đánh đúng cấp đảo Thủy (1–8) thì vẫn chỉ 1 tướng.
- Võ Sư lên Khá, nên từ ải 4 mọi địch đảo Thủy được cộng thêm cường hóa: +0,15 cho Bầy lính, Cường hóa, Tướng và lính, Lính tinh nhuệ, Hai tướng, Cửa ải; mini boss +0,10; boss +0,05; Tướng mới giữ nguyên. Nhờ vậy Võ Sư một mình vẫn có tỉ lệ thắng như bảng số đo dưới.

## Đảo Thủy

### 10 tướng

7 tướng chính là 7 hình aola người dùng gửi cho đảo Thủy (theo session hình aola): Mi Nhi, Ma Kết, Vây Lam, Kuba, Thương Lam, Huyền Vũ, và Vạn Quân (dạng 2 của Lam Quân, người dùng gắn nhãn BOSS). Thêm Giọt Sương ở ải 1, và hai tướng Thường (Tiểu Y, Cánh Cụt) cho chặng đầu. Thứ tự xếp theo độ hiếm.

| Ải | Chặng | Tướng | Độ hiếm (tạm) | Loại ải |
|---|---|---|---|---|
| 1 | Bãi Vỏ Sò | Giọt Sương (bóng của tướng khởi đầu) | Khá | thường, −20% |
| 5 | Vũng San Hô | Tiểu Y | Thường | thường, +15% |
| 10 | Cầu Gỗ Rêu | Cánh Cụt | Thường | thường, +15% |
| 15 | Làng Vỏ Ốc | Mi Nhi | Khá | thường, +15% |
| 20 | Ngọn Hải Đăng | Ma Kết | Hiếm | mini boss |
| 30 | Thác Bạc | Vây Lam | Hiếm | mini boss |
| 40 | Rạn Ngọc Trai | Kuba | Sử thi | mini boss |
| 50 | Hồ Gương | Thương Lam | Sử thi | mini boss |
| 60 | Đền Rùa Cổ | Huyền Vũ | Huyền thoại | mini boss |
| 70 | Xoáy Nước Đinh Ba | Lam Quân → Vạn Quân → Hắc Dực | Sử thi | boss tiến hóa |

Không có suất trên đảo: Tám Tay, Cá Ngựa, Mập Răng Cưa (Thủy hiện có 13 tướng).

Tướng tặng: Võ Sư ở ải 3 (Thổ, khắc Thủy), Nụ Hoa ở ải 25. Từ 2026-11-03: Võ Sư lên Khá; người chọn Thạch Nhân nhận Mèo Quyền Sắt thay Võ Sư; quà ải 25 là Mầm Gỗ (Nụ Hoa thành tướng khởi đầu).

### Lính (6 loại, `Web/src/core/data/minions.ts`)

Mỗi loại có 2 bậc; từ ải 35, bậc 2 thay bậc 1. Cua có từ chặng đầu, cá nóc từ ải 10, song ngư từ ải 20. Hình là dạng aola gốc chưa có trong danh sách tướng (`reskin/goc_<id>`), chỉ dùng trong bản thử.

| Lính | Hình aola | Vai | Bị động |
|---|---|---|---|
| Cua Kìm, Cua Pháo | 1313 蟹小拳, 1314 炮炮蟹 | trâu | giảm 15% / 20% sát thương nhận |
| Cá Nóc, Cá Nóc Điện | 16 闪光河豚, 17 电击河豚 | phản đòn | bị đánh có 30% / 35% gây bỏng; Cá Nóc Điện có chiêu choáng 15% |
| Song Ngư Con, Song Ngư | 829 小双鱼, 830 双鱼灵 | nhanh | né 12% / 15%, chiêu đánh thêm một đòn |

Lính yếu hơn tướng cùng cấp: Máu ×0,85, Công ×0,9, Thủ ×0,9 (`MINION_POWER`).

### Cấp và sức địch

- Cấp địch theo mốc: ải 1 cấp 1, ải 10 cấp 2, ải 15 và 20 cấp 3, rồi mỗi 10 ải +1 cấp, tới ải 70 cấp 8. Giữa hai mốc thì nội suy rồi làm tròn xuống. Cấp đề nghị của đảo: 1–8.
- **"Lv" của địch là sức thật**: ở hệ thống mới, mọi tướng địch quy về sức của độ hiếm Khá, nên Huyền Vũ cấp 7 không mạnh hơn tướng Khá cấp 7. Tướng của người chơi vẫn mạnh theo độ hiếm. Không quy như vậy thì từ ải 20, tướng Hiếm, Sử thi, Huyền thoại cùng cấp thắng gần như mọi trận.
- Boss so với hệ thống cũ (máu ×1,8, công ×1,1): mini boss còn máu ×1,71, công ×1,05; boss tiến hóa máu ×0,7 so với boss cũ (`ENEMY_NORM` ở `islands.ts`).

### Thưởng

| Thưởng | Số |
|---|---|
| Bi mỗi ải | 1 bi (địch cấp 1–4), 2 bi (cấp 5–8) |
| Bi thêm lần đầu qua | ải tướng +2, mini boss +4, boss +8 |
| Rương mốc | mỗi 10 ải (7 rương): 4, 5 … 9 bi và 1–2 thẻ; rương ải 70 có 15 bi, 4 thẻ |
| Mảnh: ải tướng | chắc chắn rơi mảnh tướng mới: thường 2–4, mini boss 3–5, boss 4–6 |
| Mảnh: ải xen giữa | mỗi tướng trong ải rơi 1–2 mảnh. Tỉ lệ theo độ hiếm: Thường 30%, Khá 25%, Hiếm 20%, Sử thi 15%, Huyền thoại 10%. Cửa ải ×1,5. Lính không rơi mảnh |

Đánh lại ải: mảnh rơi theo luật cũ (tỉ lệ ×0,8, ải chắc chắn rơi còn 50%).

## Số đo (máy tự chơi, `npm run sim -- island 100`)

Người chơi mang 1 tướng, cấp bằng cấp địch của ải. Sao theo kịp cấp (sao 2 từ cấp 2, sao 3 từ cấp 5), cấp thẻ bằng sao. Bảng là tỉ lệ thắng trung bình theo kiểu ải; người thật thường thắng nhiều hơn máy.

| Kiểu ải | Võ Sư (Thổ, khắc đảo) | Giọt Sương (Thủy, không khắc) |
|---|---|---|
| Ải tướng thường (1, 5, 10, 15) | 100% | 84% |
| Bầy lính | 91% | 63% |
| Cường hóa | 92% | 49% |
| Tướng và lính | 78% | 36% |
| Lính tinh nhuệ | 78% | 32% |
| Mini boss (20–60) | 72% | 20% |
| Hai tướng | 69% | 17% |
| Cửa ải | 62% | 16% |
| Boss ải 70 | 61% | 29% |

Trong một chặng, độ khó lên xuống kiểu răng cưa: đầu chặng dễ, cửa ải khó nhất, rồi tới tướng mới. Tướng không khắc hệ đảo thì cần hơn địch 1–2 cấp.

Tiến độ: qua lần đầu cả đảo được 137 bi từ ải và 54 bi từ rương, khoảng 1.760 EXP, đủ lên cấp 7. Chưa tính cây bi, trang trại, rương máy bi, đánh lại. Đánh lại một ải được 1–2 bi.

## Màn đảo (web)

- Đảo 70 ải phóng to bản đồ (×2,2 thay vì ×1,27).
- 10 ải tướng là mốc lớn trên đường mòn, có tướng đứng trên. Ải xen giữa là chấm nhỏ: vàng là đã qua, cam là đang đánh, xám là chưa mở.
- Chạm mốc hoặc chấm thì mở **bảng chặng**: mỗi ải một dòng có kiểu ải, địch, cấp, % cường hóa và bi; chạm dòng thì vào chuẩn bị trận.
- Thanh tiến độ có 7 rương. Khung dưới ghi "Ải 23/70 · Ngọn Hải Đăng 4" kèm nhãn kiểu ải.
- Hộp chuẩn bị trận ghi % cường hóa, "Lính, không thu phục". Ở ải 1 có dòng "Mặt nước in bóng Giọt Sương của bạn".

Đảo khác vẫn 8 ải như cũ. Code chạy được cả hai kiểu.

Thử nhanh: `chay_web.bat`, rồi vào Sổ tay để dùng bảng thử; hoặc mở `?fresh&skipintro&screen=zone&zone=thuy`.

## Code (web)

| File | Nội dung |
|---|---|
| `Web/src/core/data/islands.ts` | Kế hoạch đảo (`ISLANDS`), mẫu ải, cường hóa, `ENEMY_NORM`, hàm sinh 70 ải |
| `Web/src/core/data/minions.ts` | 6 lính, 18 thẻ; đăng ký vào `HERO`, `CARD` để trận dùng như tướng |
| `Web/src/core/data/stages.ts` | Đảo có kế hoạch thì sinh ải, đảo khác dùng 8 ải cũ. Thêm `zoneSize`, `zoneMiniAt`, `ZONE_CHESTS`, `buff`, `tag`, `chapter` |
| `Web/src/core/data/stages_v1.ts` | Cờ "ải cũ" cho `export_data.ts`, `export_golden.ts`: JSON và golden của Unity không đổi (đã đối chiếu từng file) |
| `Web/src/core/progression.ts` | `enemyMods` (cường hóa, lính, quy độ hiếm), bi mỗi ải, rương theo đảo, `zoneDone` |
| `Web/src/view/screens/zone.ts` | Đường mòn mốc và chấm, bảng chặng, nhãn kiểu ải |
| `Web/scripts/sim.ts` | Chế độ `island` |

## Unity (chép 2026-11-03)

Từ 2026-11-03 làm ở Unity, bản web chỉ làm khi người dùng yêu cầu. Lần xuất cuối từ web dùng script trong thư mục tạm (không sửa `Web/`): JSON có 102 ải và khoá `minions` ở `heroes.json`, `cards.json`; golden có thêm `islands.json`. Từ nay số liệu sửa thẳng trong `Assets/02 Data/Json` rồi chạy menu `PokiClash/Nhập dữ liệu`.

**Đừng chạy lại `Web/scripts/export_data.ts`, `export_golden.ts` vào `Assets/`:** hai script này vẫn xuất bộ 8 ải cũ, không có lính, sẽ ghi đè mất 70 ải.

| File | Nội dung |
|---|---|
| `Core/Islands.cs` | Cỡ đảo, mini boss đầu, rương mốc theo đảo (điền từ danh sách ải); `EnemyMods` (cường hóa, lính, quy độ hiếm); tên kiểu ải |
| `Core/Types.cs`, `GameData.cs` | `StageTag`, `StageDef.tag`, `chapter`, `StageEnemy.buff`, `HeroDef.minion`; `GameData.Minions`, `MinionCards` (`Hero(id)` tìm được, không nằm trong `Heroes`) |
| `Core/Progress.cs`, `Badges.cs`, `Trees.cs` | Bi ải 70, rương 7 cái, xong đảo theo cỡ đảo, đền và dãy huy hiệu theo cỡ đảo và mini boss đầu |
| `Core/Battle/Teams.cs` | `Enemy(st, d)` gắn phần cộng của địch |
| `App/Scenes/ZoneScene.cs` | Đường mòn, chấm ải, rương theo tỉ lệ. Chạm chấm hay bệ mở hộp chuẩn bị của đúng ải đó, ải khoá cũng xem được (bảng chặng bỏ 2026-11-03). Bản đồ dài (2026-11-03, `ZoneDef.path`, `stops`, `plates`): bản đồ rộng 1,27 màn, đường mòn theo con đường cát của ảnh, bệ ải tướng cỡ thật ở bãi của ảnh, bảng tên ngược phía địa danh. Đảo chưa có bản đồ dài: bản đồ ×3, bệ thu nhỏ 0,75 |
| `ZonePip`, `ZoneChapterRow`, `ZoneChapterDialog` | Prefab `Items/ChamAi`, `Items/DongChang`, `Dialogs/BangChang`, dựng bằng menu `PokiClash/Prefab/Đảo 70 ải (ChamAi, DongChang, BangChang)`. Bảng chặng không mở nữa từ 2026-11-03 |
| `StagePrepDialog`, `PrepFoe`, `ZoneEnemy` | Nhãn kiểu ải, dòng "Mặt nước in bóng…", "Cường hóa +x%", "Yếu hơn x%", "Lính, không thu phục", máu boss tính cả phần cộng. Từ 2026-11-03: lực chiến từng đối thủ, dòng so lực chiến địch / đội bạn, thưởng là ô hình (`RewardTile`), ải khoá chỉ xem |
| `Tests/IslandTests.cs` | So từng ải với golden: kiểu ải, chặng, bi, đội địch, phần cộng khớp từng bit |
| `Editor/PlayTour.cs` | Menu `PokiClash/Thử/Đảo 70 ải: …` chụp màn đảo, hộp chuẩn bị (chạm chấm), trận có lính |

Hình 6 lính đã nhập thành prefab (`Assets/04 Prefabs/Heroes/linh_*.prefab`, nén ASTC). Toàn bộ test EditMode qua (86).

## Còn lại

1. **Chạy lại `Quét nhịp`** (ProgressSim) để xem nhịp ngày với 70 ải.
2. **Ảnh đảo Thủy mới: xong (2026-11-03).** Bản đồ dài 1024 × 4288 ghép từ 3 đoạn GPT (`ArtGen/Islands/PROMPTS.md`, mục "Đảo Thủy 70 ải"), đã vào game: chấm ải cách nhau 92 px khung 1080 (trước khoảng 30 px), bệ tướng cỡ thật, 10 địa danh sát bãi ải tướng. Đảo khác muốn 70 ải thì làm bản đồ dài theo cùng cách.
3. **Bốn đảo còn lại:** chọn 10 tướng, 3 loại lính mỗi đảo. Bộ sinh 70 ải (`islands.ts`) hiện chỉ có ở web; danh sách ải trong Unity là dữ liệu đã sinh sẵn. Làm đảo mới thì chép bộ sinh sang Unity (menu Editor ghi `stages.json`), hoặc dùng web nếu người dùng cho.
4. **Bản lưu:** bản lưu cũ có `zones.thuy = 8` nay thành 8/70. Số ải toàn cục của đảo sau đổi (Hỏa từ 71), nhưng chỉ ảnh hưởng `clears`, chưa chỗ nào đọc.

Câu hỏi còn mở ghi ở `12_KeHoach_OpenSpec.md`, mục "Câu hỏi còn mở" (15–20).
