# Đưa lô 10 tướng mới đảo Thủy vào game (2026-11-11)

Quyết định người dùng: 10 tướng mới (id, tên mới), chỉ số và thẻ chép theo tướng cũ cùng suất, thay vào 10 suất đảo Thủy theo thứ
tự; tướng cũ giữ trong danh sách (chỉ mất suất trên đảo); Tí Tách thành tướng khởi đầu hệ Thủy thay `giot_suong` trong `starters`.
Phần dữ liệu, code, test, golden không cần Unity đã làm xong; phần Unity (menu, chép rig, prefab, test) Claude điều phối chạy theo mục 4.

## 1. Khảo sát (ngắn)

- **`heroes.json`** (CRLF, thụt 1): `heroes[]` mỗi tướng `id, name, title, aola (= forms[0].aola), elem, rarity, stats[6], skill,
  ult, passive (id thẻ), shards (mảnh mở khóa), line, size (= forms[0].size), forms[{name, aola, size}]`; `minions[]` (lính, thêm
  `minion, tier, kind`); `starters` (5 tướng khởi đầu, mỗi hệ một, thứ tự đảo); `legendMilestoneHero`. `aola` của dạng .atomik = tên
  thư mục `Assets/03 Art/Heroes/Resources/<dạng>/`. `size` là cỡ hiển thị tương đối (rig quy về cùng chiều cao bằng `game.height`
  rồi nhân `size`): dòng 2 dạng 0,92 / 1,1; dòng 3 dạng 0,9 / 1,02 / 1,14, boss 0,95 / 1,1 / 1,16.
- **`cards.json`** (LF): `pool` (35 thẻ chung), `innate` (thẻ riêng `<id>_skill/_ult/_pas`: `owner, name, rarity, kind, icon, cost,
  effects`, bị động thêm `trigger`), `minions`, `traits` (bị động boss ải 30–70: `owner` phải là tướng đứng ở ải đó;
  `IslandTests.BiDongBoss_5MocCuoi` bắt mọi trait phải gắn đúng chủ ở một ải). Thẻ không có mô tả chữ (chữ thẻ sinh từ `effects`).
- **`Editor/IslandGen.cs`**: `Plan Thuy` (`Intro(ải, tướng, tên ải, trait, buff)`), `firstIsPlayer = true` (ải 1 là bóng tướng
  khởi đầu, buff −20 %, rơi chắc 2–4 mảnh), ải xen giữa lấy tướng theo chặng (H, P, Q). Ải tướng có `evo` khi tướng có > 1 dạng
  (boss tiến hóa trong trận theo số dạng). Menu ở `Editor/IslandGenMenu.cs`: "PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (5 đảo)"
  (ghi `stages.json` + Nhập dữ liệu), "PokiClash/Thử/Tính lại golden islands, roster, cardtext, zones", "PokiClash/Thử/Tính lại
  golden theo danh sách tướng (progression, badges, potential)"; `Editor/GoldenRecalcMenu.cs`: "PokiClash/Thử/Tính lại golden sim,
  tướng trên nút ải (Temp/GoldenRecalc.json)" (chỉ ghi ra Temp, phải ghép vào golden bằng script).
- **`stages.json`** (LF): 350 ải, đảo Thủy id 1–70; địch `{hero, level, boss, evo, buff, trait}`, rơi `{hero, chance, min, max,
  gift, altFor, altHero}`.
- **`Core/GameData.cs`**: `Starters` đọc từ `starters`; `StarterStage(id)` = ải 1–4 có tướng đó, rơi chắc, không phải quà;
  `Validate()` có số cứng (tướng 78, thẻ riêng 235) đã sửa thành 88 / 265; mỗi hệ đúng một tướng khởi đầu.
- **`Core/SaveData.cs`**: `New(d, now)` chọn sẵn `Starters[0]` (test, máy tự chơi, bộ tính golden); game thật `New(d, now, null)`
  (hộp chọn). `MigrateStarterV4` (v4 → v5) coi bản lưu cũ đã chọn Giọt Sương: vẫn đúng (Giọt Sương còn). Không thêm bước chuyển
  bản lưu (xem mục 6).
- **`Game/Battle/HatNuoc.cs`** `WThemes` (5 màu: mực, đậm, giữa, nhạt, bọt; `fx` họa tiết thêm: `tinh_the`, `sao`, `may`,
  `canh_sen`, `giap`) chỉ có tác dụng khi tướng có trong **`StageView.WaterFx`** (chiêu mana + chiêu cuối theo dạng, mã `n_*`);
  tướng Thủy không có trong bảng thì bắn "tia cũ". Vì vậy đã thêm cả hai bảng (mục 3).
- **Test nhắc tướng cũ / tướng khởi đầu**: RosterTests, StarterTests, IslandTests, ProgressionTests, AfkTests, SaveTests,
  CoreGoldenTests (số lượng); test golden phụ thuộc bản lưu mặc định (tướng khởi đầu sở hữu sẵn, tướng đồng hành): FarmTests,
  PotentialTests, PachinkoTests (rương), ProgressionTests (thẻ rơi từ rương), BadgeTests (tiến độ đền). BattleGoldenTests dùng
  `giot_suong`, `tieu_y`, `huyen_vu` như tướng thường: không phải đổi (tướng cũ còn, boss Thủy cuối vẫn 3 dạng).
- **Tour Editor nhắc `giot_suong`** (dùng như tướng thường, vẫn chạy; không sửa): PlayTour, GiotSuongCombatTour, PopupTour,
  PrepFoeTour, SkillNowTour, VsIntroTour, EvolutionStripMenu, BalanceWindow. `balance.json` `simTeams` (đội mẫu máy tự chơi Thủy,
  Hỏa) có `giot_suong`: giữ (Sim không đặt tướng đồng hành, chỉ số y hệt Tí Tách).

## 2. Id cuối cùng (không trùng tướng, lính, thẻ, thư mục Resources nào)

| suất | tướng cũ | id mới | tên | danh hiệu | dạng (`aola` = `<id>_<k>`, cỡ) | thẻ skill / ult / bị động | bị động boss |
|---|---|---|---|---|---|---|---|
| ải 1 (khởi đầu) | giot_suong | `ti_tach` | Tí Tách | Võ sĩ giọt mưa | Tí Tách 0,92; Sóng Thần 1,1 | Súng Nước / Mưa Rào / Mưa Đầu Mùa | |
| ải 5 | tieu_y | `thach_giai` | Thạch Giải | Cua ẩn sĩ nhà đá | Thạch Giải; Thạch Thành Giải | Bọt Nước / Đá Ngầm Trồi / Vũng Triều | |
| ải 10 | canh_cut | `ca_den` (trước 2026-11-11 chiều: `nong_xoay`, Nòng Xoáy; đổi bằng `quai/doi_ca_den.py`) | Hải Đăng | Cá đèn lồng vực sâu | Lồng Đèn; Hải Đăng | Vòi Nước / Thủy Pháo / Vụng San Hô | |
| ải 15 | mi_nhi | `ha_ba` (id giữ; trước 2026-11-11 tối là Hà Bá, hà mã) | Sò Ngoạm | Sò đột biến lưỡi dài | Sò Háu; Sò Ngoạm | Phụt Ngọc / Lưỡi Quật / Hồn Nước | 2026-11-11 tối: HÌNH và chiêu của suất này nay là dòng **sò đột biến** (mã làm việc `so_gai`, người dùng lên ý tưởng và chốt; rig `ArtGen/Spine/inbox/so_gai_<k>/rig`, ghi chú `inbox/so_gai_ghichu.md`). Tên tướng, dạng, thẻ đã đổi (Claude đặt tạm, người dùng có thể đổi); id nội bộ giữ `ha_ba`. Chiêu mana = `n_ngoc` (phụt viên ngọc trai), chiêu cuối lè lưỡi lao tới quật = `n_va`. |
| ải 20 | ma_ket | `so_ngoc` (id giữ; trước 2026-11-12 là Sò Ngọc, "Pháo đài ngọc trai", dạng Sò Gai / Bạng Vương, thẻ Phun Bọt Ngọc / Mưa Gai / Tim Ngọc Trai) | Bát Trảo | Bạch tuộc quái vật gọi bầy | Trảo Nhi; Bát Trảo | Bóng Mực / Gọi Bầy / Túi Mực | 2026-11-12: HÌNH và chiêu của suất này nay là dòng **bạch tuộc quái vật** (mã làm việc `bach_tuoc`, người dùng lên ý tưởng, duyệt concept từng dạng và bảo "thay thế vào game"; hình mình trên rig `monster_3616`, rig `ArtGen/Spine/inbox/bach_tuoc_<k>/rig`, ghi chú `inbox/bach_tuoc_ghichu.md`). `so_ngoc_1` = con non (nhảy vào, 3 bạch tuộc con, có `evolve`), `so_ngoc_2` = trưởng thành (trồi lên từ hố, 6 bạch tuộc con). Chép tay 4 file vào Resources (`.atomik` + `_portrait.png`; không chạy `vao_game.py` trên máy này). Chiêu mana = `n_muc` (quả bóng mực đen: `HatNuoc.NNgoc(..., muc: true)`), chiêu cuối = `n_va` ở khung bạch tuộc con đầu tiên trúng (bạch tuộc con nằm trong rig, xương `far` / `fly_c*`, `game.far = ["skill"]`); `HatNuoc.WThemes` đổi sang màu mực đen tím than, bỏ gai san hô. Số dạng không đổi nên không đổi golden. Tên tướng, danh hiệu, tên dạng, tên thẻ đã đổi 2026-11-12 (người dùng: "đổi đi"; Claude đặt, người dùng có thể đổi): sửa `heroes.json`, `cards.json`, `tuong_moi_thuy.py` và sửa thẳng chuỗi tên trong `HeroDb.asset`, `CardDb.asset` (chưa chạy được menu "Nhập dữ liệu"); id nội bộ và biểu tượng thẻ giữ nguyên. C# đã biên dịch thử sạch bằng trình biên dịch của Unity (`Editor/Data/NetCoreRuntime/dotnet.exe` + `DotNetSdkRoslyn/csc.dll` với `Library/Bee/artifacts/1900b0aE.dag/PokiClash.Game.rsp`, đổi `-out` ra thư mục tạm); CHƯA xem trong trận (không có cầu MCP tới Editor). |
| ải 30 | vay_lam | `giong_bao` | Giông Bão | Kỳ giông gọi mưa | Giông Mưa; Giông Bão | Bầu Phun / Cầu Mưa / Bầu Hứng Mưa | |
| ải 40 | kuba | `lien_kinh` | Liên Kình | Kình ngư cõng sen thiêng | Kình Nụ; Liên Kình | Bong Bóng Sen / Nụ Bung / Sen Thiêng | `lien_kinh_boss` Sen Hộ Thể (= kuba_boss) |
| ải 50 | thuong_lam | `uyen_xa` | Uyên Xà | Rắn đèn vực sâu | Uyên Nhi; Uyên Xà | Thủy Thương / Mưa Bọt / Đèn Vực Sâu | 2026-11-11 khuya: HÌNH và chiêu của suất này nay là dòng **rắn nước có sừng** (mã làm việc `ran_sung`, người dùng lên ý tưởng, duyệt từng bước và bảo thay tướng cũ; reskin rig `monster_3247`, rig `ArtGen/Spine/inbox/ran_sung_<k>/rig`, ghi chú `inbox/ran_sung_ghichu.md`). Id, tên tướng, danh hiệu, tên dạng, thẻ CHƯA đổi (chờ người dùng đặt; "rắn đèn", "Mưa Bọt", "Đèn Vực Sâu" không còn khớp hình). Chiêu mana = `n_tia` (há nhẹ miệng bắn nước), chiêu cuối lao tới đuôi sừng quất chém = `n_va` (vệt chém riêng chưa làm). Màu nước trong `HatNuoc.WThemes` đổi sang lam cô-ban, bỏ họa tiết sao. |
| ải 60 | huyen_vu | `han_ngac` | Hàn Ngạc | Cá sấu băng vực sâu | Ngạc Nhi; Hàn Ngạc Vương | Hàn Phong / Cọc Băng / Hàm Băng | `han_ngac_boss` Giáp Băng Hộ Thể (= huyen_vu_boss). 2026-11-12: HÌNH của suất này nay là dòng **rồng vây** (mã làm việc `rong_vay`, người dùng bảo "thay cho con thứ 9 đảo thủy"; hình mình trên rig `monster_3458`, rig `ArtGen/Spine/inbox/rong_vay_1/rig`, ghi chú `inbox/rong_vay_ghichu.md`). 2026-11-12 (máy ổ C): đủ 2 dạng: `han_ngac_1` = rồng non (rig `inbox/rong_vay_non/rig`, cùng xương và clip, thân ngắn, đầu to, da lam nhạt), `han_ngac_2` = rồng trưởng thành (rig `rong_vay_1`); cả hai có 7 clip mới (`appear` bay vào rồi gầm, `attack` quật đuôi, `cast` quạt cánh, `skill` gầm vỗ cánh; dựng bằng `rong_vay_clip.py`). Chép tay 4 file vào Resources (không chạy `vao_game.py` trên máy này: rig các tướng khác thiếu hoặc cũ); Unity nhập lại không lỗi. Dạng 1 có clip `evolve` (gộp bản nhẹ dạng 2, 609 KB). Chiêu mana dùng `n_loc` (lốc xoáy nước lướt từ trước mặt tướng tới địch: `HatNuoc.NVoi(tu)`). Chưa kiểm trong trận (MCP Unity không mở). Số dạng không đổi nên không đổi golden. Id, tên, danh hiệu, tên dạng, thẻ CHƯA đổi ("cá sấu băng", "Cọc Băng", "Hàm Băng" không còn khớp hình). Chiêu giữ `n_tia` / `n_song`, `n_mua`; màu nước `HatNuoc.WThemes` đổi sang chàm + lam ngọc, bỏ mảnh băng; rig có xương `mieng` (game.muzzle). Rig thiếu clip `appear`, `evolve`. |
| ải 70 (boss) | lam_quan | `hai_long` | Hải Long | Rồng biển nhiều đầu | Hải Long Nhi 0,95; Hải Long Tam Thủ 1,1; Hải Long Ngũ Đầu 1,16 | Hải Long Phun / Hải Long Gầm / Vảy Ngọc | `hai_long_boss` Long Uy Chấn (= lam_quan_boss) |

Độ hiếm, 6 chỉ số, số mảnh, số và hiệu ứng thẻ (cost, effects, trigger, rarity, kind) chép nguyên của tướng cũ cùng suất; tên thẻ
skill ≈ chiêu `cast` dạng 1, ult ≈ chiêu `skill` dạng 1 (tm10 chưa có ghi chú: theo nhịp Hải Long, phun nước / gầm); biểu tượng
chọn trong bộ đã có. Bị động boss cũ `kuba_boss`, `huyen_vu_boss`, `lam_quan_boss` được đổi tại chỗ thành bản của tướng mới (test bắt
mọi trait phải có chủ ở một ải, giữ bản cũ là test hỏng). Tướng mới đứng ngay sau tướng cũ trong `heroes`, thẻ ngay sau thẻ cũ.

## 3. Đã làm (file)

- `ArtGen/Spine/quai/tuong_moi_thuy.py` (mới, idempotent, `--kiem`): thêm 10 tướng, 30 thẻ, 3 trait, đổi `starters`, đổi tướng ở
  10 suất trong `stages.json` (59 địch, 59 mảnh rơi, 3 trait, chỉ ải đảo Thủy). **Đã chạy**: `heroes.json`, `cards.json`,
  `stages.json` đã ghi (chạy lại báo "không có gì phải đổi").
- `Editor/IslandGen.cs` `Plan Thuy`: 10 id mới, 3 trait mới; tên ải, lính, cường hóa giữ. Đã so ngoài Unity: chạy đúng code menu
  "Đảo 70 ải: sinh lại" cho ra **y hệt** `stages.json` hiện tại, `GameData.Validate()` rỗng lỗi.
- `Core/GameData.cs`: số mong đợi 88 tướng, 265 thẻ riêng. `Core/SaveData.cs`: chú thích.
- `Game/Battle/HatNuoc.cs`: `WTheme` cho 10 id (màu theo bảng màu từng dòng, họa tiết: Thạch Giải mảnh đá, Sò Ngọc gai san hô,
  Giông Bão mây xám, Liên Kình cánh sen đỏ, Uyên Xà chấm đèn, Hàn Ngạc mảnh băng, Hải Long sao vàng).
- `Game/Battle/StageView.cs` `WaterFx` (sửa nhỏ, cần để WTheme có tác dụng): chiêu mana / chiêu cuối từng dạng theo ghi chú dòng
  (tia, bong bóng, mưa, sóng, xoáy, vòi rồng). Là bảng nháp cho bước VFX riêng, chưa xem trong trận; bỏ dòng nào thì tướng đó về
  "tia cũ" như trước.
- `Editor/IslandGenMenu.cs` menu "Tính lại golden theo danh sách tướng": tính lại thêm `badges.json` "fights" (5 trận thật của đền
  hệ Thủy; đối thủ đền chọn theo danh sách tướng Thủy nên thêm tướng là đổi; trước đây không menu nào tính lại).
- Test: RosterTests (88 tướng, Thủy 23, `starters` mới, dạng Tí Tách / Hải Long, Giọt Sương còn), CoreGoldenTests (88 / 265,
  `TestData.OldStarter`), StarterTests (mặc định `ti_tach`; tướng khởi đầu Tí Tách 2 dạng), IslandTests (ải 1 = `ti_tach`),
  ProgressionTests (thẻ rơi lùi độ hiếm, tiến hóa: `ti_tach`), AfkTests (cửa ải 29 = Sò Ngọc, Hà Bá), SaveTests (`ti_tach`),
  BadgeTests (đội 5 trận có `ti_tach`). Test golden chỉ phụ thuộc "tướng khởi đầu mặc định đang sở hữu" dựng bản lưu
  `SaveData.New(d, 0, TestData.OldStarter)` (Giọt Sương) để giữ golden xuất từ web: FarmTests, PotentialTests (khai phá, trận,
  tỉ lệ), PachinkoTests.MoRuong600Lan, ProgressionTests.TheRoiTuRuong, BadgeTests.TienDo.
- `ArtGen/Spine/quai/golden_thuy.py` (mới): `doi_id` đổi id tướng cũ → mới (và id thẻ) trong `afk.json`, `pachinko.json` (hai golden
  không menu nào tính lại; tướng mới là bản chép đứng đúng chỗ nên kết quả y hệt, chỉ khác tên). **Đã chạy.** `ghep_sim` ghép
  `Temp/GoldenRecalc.json` vào `sim.json` (Claude chạy sau menu, mục 4).
- `ArtGen/Spine/quai/vao_game.py` (mới) + `da_nhan.json` (thêm `_vi_du` dòng Hải Long, mảng `nhan` không đụng): chép rig đã nhận
  vào Resources, kiểm `.atomik` (khối `game`, clip, xương move, slot shadow), chân dung 512.

**Kiểm ngoài Unity** (bộ chạy ở scratchpad phiên này: dotnet 9 + nunit của Unity, biên dịch Core + IslandGen + test; một bản chạy
đúng code 3 menu golden với stub UnityEditor trên bản chép dữ liệu):
- 4 assembly thật (Core, Game, Editor, Tests) biên dịch được bằng csproj chép (`dotnet build`, 0 lỗi).
- Trước khi sửa: 81/85 test qua (4 test hỏng sẵn vì `TestContext.WriteLine` cần runner NUnit: phần kiểm trước dòng đó đều qua).
- Sau khi sửa + chạy 3 menu golden + `ghep_sim` trên bản chép: **81/85 qua, đúng 4 test như trước**. Sau khi chạy menu, `sim.json` chỉ
  đổi 4 ô ải đảo Thủy (ải tướng 20–60: tướng mới 2 dạng nên boss tiến hóa một lần).

## 4. Các bước Claude chạy trong Unity (theo thứ tự)

Trước hết nhắn session khác đang dùng Unity, chắc Editor không Play.

1. Refresh để biên dịch (6 file C# đổi: GameData, SaveData, IslandGen, IslandGenMenu, HatNuoc, StageView, 11 test). Xem console.
2. Menu **"PokiClash/Nhập dữ liệu"** (JSON → HeroDb, CardDb, StageDb, BalanceConfig asset).
   (Tuỳ chọn, để chắc: "PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (5 đảo) (stages.json)" — phải không đổi `stages.json`; `git diff`
   trống ở file đó.)
3. Menu **"PokiClash/Thử/Tính lại golden islands, roster, cardtext, zones"** → `islands.json`, `roster.json`, `cardtext.json`,
   `zones.json`.
4. Menu **"PokiClash/Thử/Tính lại golden theo danh sách tướng (progression, badges, potential)"** → `progression.json` (stats, shards,
   shardEnd), `badges.json` (stages, fights), `potential.json` (caveStages).
5. Menu **"PokiClash/Thử/Tính lại golden sim, tướng trên nút ải (Temp/GoldenRecalc.json)"**, rồi ngoài Unity
   `py -3 -I ArtGen/Spine/quai/golden_thuy.py ghep_sim` → `sim.json` (bản thử: 4 ải Thủy).
6. Chạy **EditMode test** (cả bộ). Mong đợi qua hết. Nếu lệch: test golden nào hỏng thì so với danh sách mục 5.
7. Rig: khi một dòng đạt, thêm vào `da_nhan.json` mảng `nhan` (mẫu `_vi_du`), chạy `py -3 -I ArtGen/Spine/quai/vao_game.py --kiem`
   rồi `vao_game.py` (chép `.atomik` + `_portrait.png`). **Chép đủ mọi dạng của một tướng** trước bước 8: `AtomikForms` chỉ dựng
   prefab tướng mới khi đủ dạng ("chưa có prefab và thiếu dạng, bỏ qua").
8. Refresh (nhập `.atomik`, ảnh chân dung), menu **"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng"** (dựng `<dạng>.asset`, prefab
   `Assets/04 Prefabs/Heroes/<id>.prefab`, thêm vào HeroModels). Không chạy menu nhập aola thường.
9. Soi: **"PokiClash/Tướng/Chụp thử dạng .atomik (mọi clip)"** (`Library/PokiHeroShots/`), rồi vào trận đảo Thủy ải 1, 5, 40, 70
   (chiêu nước theo `WaterFx`, cỡ `size`, lật trái phải, viền sticker), hộp chi tiết tướng, nút Tiến hóa (clip `evolve`).
10. Chỉnh `size` trong `heroes.json` nếu con nào to / bé quá (rồi Nhập dữ liệu; `size` không vào golden nào).

## 5. Golden

- Đã đổi sẵn (không có menu): `afk.json` (3 chỗ), `pachinko.json` (đổi id tướng boss Thủy và thẻ của chúng) — bằng
  `golden_thuy.py doi_id`, đã chạy test ngoài Unity.
- Claude sinh lại trong Unity (mục 4): `islands.json`, `roster.json` (forms, leads), `cardtext.json` (thêm 30 thẻ, đổi 3 trait),
  `zones.json`, `progression.json`, `badges.json`, `potential.json`, `sim.json` (qua `ghep_sim`).
- Không đổi: `battles.json`, `battle_events.json`, `farm.json`, `rng.json`, `ads.json`, `trees.json`.

## 6. Việc còn thiếu, để nối sau

- **`AolaActor` và clip mới** (`Game/Heroes/AolaActor.cs`): chỉ ánh xạ idle, hit, attack, cast, skill, evolve; clip `aura` có phủ
  liền qua mọi clip (`atkAura`, như Thanh Long). **`appear`, `die` chưa ai phát**: StageView ra sân là code rơi từ trên xuống
  0,45 s, chết là code nghiêng + mờ 0,7 s rồi ẩn ở 1,4 s (`StageView.Place`). Muốn dùng: lúc `StageView.Die` phát `die` (không lặp,
  khung cuối trống) và bỏ nghiêng/mờ cho dạng có clip `die`; lúc vào sân phát `appear` thay cho rơi (khung đầu trống). Không sửa lúc
  này vì đụng nhịp trận và mọi tướng .atomik khác.
- **Sự kiện trong clip** (`anims[].ev`: `trung`, `phun`, `het_phun`, `gam`...) có trong rig nhưng `AolaActor` không đọc (chỉ
  `AtomikPlayer.Fired` có); trận dùng `game.hitTimes`, `game.muzzle`. Lớp VFX bước sau nên đọc sự kiện + `BoneWorld("mieng")`.
- **Bước chuyển bản lưu** (chưa làm, cần người dùng chọn): người chơi cũ đã chọn Giọt Sương giữ Giọt Sương làm tướng đồng hành
  (vẫn chạy). Hai lựa chọn: (a) giữ như hiện tại (đề xuất: tướng cũ còn, không mất gì; ải 1 với họ là Tí Tách, không hiện chữ
  "bóng"); (b) thêm bước v5 → v6 đổi `starter` sang `ti_tach` và tặng Tí Tách — phải tăng `saveVersion` trong `balance.json` và
  `CoreGoldenTests` (đổi cấu hình, cần hỏi).
- **Cân bằng**: tướng mới ở ải 20–60 chỉ 2 dạng (tướng cũ 3 dạng), boss tiến hóa một lần: máu mỗi dạng, tỉ lệ thắng đổi (sim ải
  20–60 lệch). Đo lại 5 mốc cuối (`IslandGen.Plan Thuy` buff) bằng máy tự chơi nếu cần.
- **Dung lượng**: Hải Long dạng 1, 2 là 1,1 MB, 1,3 MB (đích lô ≤ 0,6 MB); Liên Kình, Uyên Xà ~0,5 MB (trần). Dạng 3 1,05 MB ổn.
- **Rig lúc viết**: `tm02` (Thạch Giải) chưa có rig; `tm03_1` chưa có clip `evolve`; tm10 / hai_long `game.shadow` rỗng, `move` = `root`.
- `GD_Claude/13_DanhSachTuong.md` chưa ghi 10 tướng mới.
