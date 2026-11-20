# Máy bi: hiệu ứng và trải nghiệm (cần phóng, đèn chạy, jackpot, rương)

Viết 2026-11-20. Người dùng dặn: "quét app AtomSpine mới, làm thêm VFX cho máy bắn bóng, đèn chạy, jackpot FX, animation khi mở
rương (rương shake nhẹ nhắc người chơi mở, hé hé, trong trong glowing), lên plan cải thiện trải nghiệm khi chơi pinball", rồi
duyệt kế hoạch ("làm đi") với các lựa chọn Claude đề xuất. Nền tảng máy bi và các hiệu ứng đã có: `07_MayBi.md`.

## Đã chốt (2026-11-20)

1. **Rig rương làm bằng AtomSpine** (`D:\AtomSpine`, CLI `packages/cli/dist/atom.mjs`; bản dựng sẵn đã có `vfx.*`, `fx.*` dù chuỗi
   phiên bản còn ghi 0.1.0). Chạy trong Canvas bằng **gói Unity của AtomSpine** (`AtomikGraphic`, uGUI):
   - `Packages/manifest.json`: `"com.atomspine.runtime": "https://github.com/HoangHai1234567/AtomSpine.git?path=/runtimes/unity#v0.2.0"`
     (repo riêng tư: máy cần đăng nhập git GitHub);
   - define `ATOMSPINE_DISABLE_IMPORTER` (giữ `Editor/AtomikImporter.cs` của dự án cho `.atomik`); rig của gói nạp lúc chạy từ
     `.bytes` bằng `AtomikFile.Load`.
2. **Hình rương tách từ ảnh có sẵn** (0 credit): `pk_ruong_<bậc>_than`, `_nap`, `_mo_sach`; lòng sáng và tia vẽ bằng script.
3. **Sáng trong rương**: quầng mềm ấm (máy bi được phép quầng, gradient từ 2026-11-10, `MachineGlow`) cộng tia phẳng.
4. **Jackpot**: được chậm máy, phóng to nhẹ, chớp mạnh; thêm tuỳ chọn "giảm nhấp nháy" trong cài đặt.
5. **Không làm**: giả "suýt trúng" (kết quả chọn trước nên làm được, nhưng là mánh máy cờ bạc; giữ nguyên tắc hiệu ứng tỉ lệ
   với giá trị thật của `07_MayBi.md`).

## Kế hoạch

| Giai đoạn | Việc |
|---|---|
| **1. Rương** | Rig 3 bậc (thân, lòng sáng, tia lọt khe, nắp, rương mở sạch, lấp lánh). Clip `cho` (đứng thở), `nhac` (nhắc mở: nhún, lắc hai nhịp, nắp hé hai lần có sáng ấm và tia lọt khe, sập lại; lặp khoảng 3 giây), `gong` (gồng: lắc mạnh dần, nắp lạch cạch, sáng tăng), `bat` (nắp bật, sự kiện `open` đổi sang rương mở sạch), `mo` (mở rồi, lòng sáng phập phồng). Dùng cho rương chờ trong khay (nhắc mở khi máy rảnh, lệch nhịp) và màn mở rương |
| **2. Cần phóng, đèn** | Mũi tên đèn dọc làn chạy lên khi sẵn sàng; lúc phóng đèn làn bật theo bi, vòng loé ở miệng ống, chạm gờ đỉnh nấm sáng và màn rung rất nhẹ. Kịch bản đèn vòm theo trạng thái (chờ, sẵn sàng, đang thả, trúng ô, rương bạc, jackpot, lên cấp). Hàng đèn dưới 5 ô: bi xuống thấp thì đèn chạy qua các ô rồi dừng ở ô thật |
| **3. Jackpot** | Báo trước 0,5–0,8 giây (đèn kiểu jackpot, chậm máy, phóng to nhẹ về ô, tiếng trống dồn); lúc trúng thêm chữ "JACKPOT!" nảy từng chữ (rig), vòi xu, giấy màu, rung màn, rung máy; sau đó rương vàng bay vào khay rồi nhắc mở |
| **4. Trải nghiệm** | Rương bay vào khay; mở mức cược mới (hút vào nút rồi nổ); bàn tay chỉ nút Thả khi rảnh khoảng 6 giây; vòng nấm từ 80 % phập phồng; tiếng chạm đinh cao dần trong một bi, tiếng và rung theo bậc thưởng; tuỳ chọn giảm nhấp nháy |
| **5. Thử máy thật** | Android: đọc được, nhịp, hiệu năng (số hạt, số Image) |

## Tiến độ

- 2026-11-20: viết kế hoạch; bắt đầu giai đoạn 1.
- 2026-11-20: **giai đoạn 1 (rương) xong, đã chạy trong Unity**:
  - gói `com.atomspine.runtime` v0.2.0 đã vào `Packages/manifest.json`; define `ATOMSPINE_DISABLE_IMPORTER` cho Standalone, Android,
    iPhone (menu `PokiClash/AtomSpine: bật define tắt importer của gói`, `Editor/AtomSpineSetup.cs`); asmdef `PokiClash.Game`,
    `PokiClash.Editor` tham chiếu `AtomSpine.Runtime` (người dùng cho sửa).
  - rig: `ArtGen/Pachinko/ruong_rig/build_rig.py` dựng ba dự án AtomSpine `ruong_rig/<go|bac|vang>/` (ops trong `rig.ops`, tờ soi
    `.atomspine/soi_*.png`), xuất `--atlas-cap 240` vào `Assets/03 Art/Pachinko/Rig/ruong_<bậc>.bytes` (khoảng 360 KB mỗi bậc,
    atlas khoảng 440 px). Thân, nắp, rương mở sạch là ảnh có sẵn; quầng mềm và tia vẽ bằng script; lấp lánh `fx_sparkle`. Gỗ 3 tia,
    bạc 4, vàng 5.
  - clip: `cho`, `nhac` (3,2 giây lặp: nhún, lắc, nắp hé nhỏ rồi hé to; khe phát sáng, tia lọt khe toả hai bên, lấp lánh bay lên;
    sập lại), `gong` (0,6 giây), `bat` (sự kiện `open` ở 0,07 giây đổi sang rương mở, đổi thứ tự vẽ cho quầng, tia đè lên lòng
    rương), `mo` (lòng sáng phập phồng, tia gom lên).
  - `Kit/Ruong` có con `rig` (`AtomikGraphic`, tắt sẵn) và ba file rig (menu `PokiClash/Prefab/Máy bi: rig rương (AtomSpine)`,
    `Editor/MachineChestRigMenu.cs`). `ChestIcon.PlayRig/StopRig`; rig nạp một lần mỗi bậc (`AtomikFile.Load`), icon nhỏ trên mặt
    máy vẫn là ảnh tĩnh.
  - khay "Rương chờ": máy rảnh thì `nhac`, lệch nhịp 1,07 giây giữa các nút; đang thả, đang mở thì `cho` (`MachineScene.TrayRigs`).
    Icon khay nướng sẵn trong prefab nên gán bậc một lần lúc chạy (`ChestIcon.Bound`).
  - màn mở rương nhóm: rương chờ chạm chạy `nhac`; gồng chạy `gong` theo thời gian gồng của bậc (code lắc nửa biên độ, không nén);
    bật chạy `bat` rồi `mo`, bỏ đổi ảnh và bóp giãn của code; hạt, loé, giấy màu, xu như cũ.
  - Lượt soi `PokiClash/Thử/Máy bi: rig rương nhắc mở (đang Play)` (`Editor/MachineRigTour.cs`), ảnh `Temp/PokiShots/7xx_*.png`.
- 2026-11-20: **giai đoạn 2–3 (đèn, cần phóng, jackpot)** viết xong code: đèn làn, đèn chạy qua ô khi một bi, báo trước jackpot
  (đèn dồn, tích tắc, phóng nhẹ), chữ JACKPOT nảy từng chữ, vòi xu, loé miệng ống, tiếng đinh cao dần, tuỳ chọn "Giảm nhấp nháy"
  trong Sổ tay (`Settings.lowFlash`). Lượt soi `PokiClash/Thử/Máy bi: đèn, phóng, jackpot (đang Play)`, ảnh `8xx_*.png`.
- 2026-11-20: **màn máy bi bản 2** (người dùng: "UI và máy bắn bóng chưa đủ đẹp, chưa đủ ấn tượng", chọn concept 2 + cờ của concept 1):
  - bố cục, số đèn, nhịp đo từ bản đục máy bi Clash of Critters (`D:\CrittersRipper\analysis_ui\BAO_CAO_MAY_BI_UI.md`): vòm 87 bóng
    hai nhóm luân phiên (rảnh 1,43 giây, đang thả 0,5 giây), bảng số 26 bóng (rảnh 2,22 giây, đang cộng 0,83 giây), nút PUSH nhảy ở
    giây 13,48 mỗi 15 giây, nút cược nhún 0,9 → 1,1 → 1. Không gửi hình của họ cho Magnific.
  - 7 tờ Magnific GPT 2.6 (95 credit/tờ, `ArtGen/Pachinko/v2/PROMPTS_V2.md`): thân máy vòm đỏ có 90 bóng vẽ sẵn, gờ đế, cờ đuôi nheo;
    bảng số 30 bóng; chữ số 0–9; nút PUSH 4 trạng thái chung đế; 6 món (viên cược, khay, thanh đếm, nút liền); 12 hình sáng (nền đen,
    gỡ nền thành quầng trong suốt); nền phòng gỗ. Khung bố cục `make_parts_refs.py`, cắt `cat_v2.py` (ra `Assets/03 Art/Pachinko`
    và `Baked/Machine/may_tinh_v2.png`: góc cam ngoài vòm trong suốt), số đo `v2/refs/bo_cuc_v2.json`, `v2_do.json`.
  - Unity: menu `PokiClash/Prefab/Máy bi: bố cục bản 2 (concept 2)` (`Editor/MachineV2Menu.cs`); thân máy nằm sau bàn, bàn thu 0,92;
    lớp sáng `fx2_den_*` phủ bóng vẽ sẵn (`p.bulbs`); bảng số trên đỉnh vòm (`p.scoreSlot`, `MachineScoreBoard.MakeV2`, chữ số hình);
    viên cược bấm đổi mức (`p.betCycle`); khung khay chỉ hiện rương bậc cao nhất + tổng số (`p.trayFrame`); thanh đếm bi; ngôi sao
    huy hiệu vòm bỏ đi vì nấm đỉnh của bàn nằm đúng chỗ (thành viên ngọc giữa hai cuộn xanh).
  - Sửa mờ, vỡ (người dùng chê, cho tăng trần credit): thân máy và nền phòng gen lại GPT 2.6 bản 2k (175 credit/tờ, ảnh mẫu là bản 1k,
    giữ thiết kế, bỏ luôn ngôi sao); bản 1k cất ở `ArtGen/Pachinko/tai_ve/ban_1k/`. Nhập: nền phòng 2048 (trước bị thu còn 1024),
    ảnh máy bi bản 2 nén ASTC 4x4 (nền phòng 5x5) thay 6x6 (`ArtImporter.cs`), đèn sáng lưu sẵn 72 px (ảnh không mipmap). Unity 6
    nhập lại theo mã băm nội dung: đổi luật nhập thì phải ép nhập lại (chạm ngày giờ không đủ). Khay bản 2: bỏ nền giấy của nút, rương
    vào giữa khung.
- 2026-11-20 tối: **máy bi bản 3** (người dùng: ống phóng "không khớp gì cả", "đục kĩ con Clash of Critters và làm lại", "giảm bớt
  texture kiểu chì", "làm thật nét và thật đẹp, nặng cũng được"):
  - ống phóng như máy tham khảo: rãnh tím sẫm hẹp, mũi tên kem chỉ lên, ống vàng hai bên; vòm mặt chơi là ống vàng tô phẳng liền với
    ống phóng; sao băng to che chỗ ống chui vào mặt chơi (đuôi rủ dọc ống), sao nhỏ lật gương ở góc trái. Mặt bàn ghép lại bằng
    `v2/ghep_ban_v2.py` (cùng hình học va chạm, ống vẽ theo khoảng cách tới đường tâm làn, canvas nới 10 đơn vị bên phải; ra 2,5
    px/đơn vị), số đo `v2/refs/mat_v2.json`.
  - mũi tên sáng `fx2_mui_ten` leo dọc ống khi mời thả (dải ±0,12 làn, leo 1,8 giây, nghỉ 0,5, hai lớp lệch 1,1 giây; hiện 0,417
    giây, tắt 0,217), bi trên làn thì sáng vệt sau lưng bi (`MachineBoard.BuildChevrons`).
  - tô phẳng (Magnific GPT 2.6): thân máy 2k, bảng số 2k, nền mặt chơi 2k, nút PUSH và 6 món 1k, sao băng 1k; ảnh thu sẵn về 1,33
    lần cỡ hiện (máy 1440 px gần 1:1), nén ASTC 4x4, nền phòng 1600 x 2400 nhập 4096.
- 2026-11-20 khuya: **máy bi casino** (người dùng chọn `ArtGen/Pachinko/v2/casino_B.png`, "thêm 1 chút nhẹ kiểu tô chì, 1 chút
  thôi"; trước đó "đường vòm gấp khúc quá, làm tròn vào"):
  - vòm mặt chơi vẽ tròn (cắt góc Chaikin `smooth_poly` trong `ghep_ban_v2.py`, vách va chạm giữ nguyên).
  - 8 tờ Magnific GPT 2.6 ở `ArtGen/Pachinko/tai_ve/casino/` (thân máy 2k, bảng số 2k, nền mặt chơi 2k, nền phòng 2k, bộ phận 2k,
    nút PUSH 1k, 6 món 1k): thân máy đỏ ruby viền vàng, hai cột sao vàng, bệ đỏ sau hàng nút (khung `v2/make_casino_refs.py`, vùng vẽ
    rộng hơn `refs/bo_cuc_casino.json`); bảng số vàng 26 bóng, màn LED đỏ sẫm; đinh vàng, nấm là phỉnh casino, nấm đỉnh và núm
    đáy V là ngọc ruby, vách ô vàng, ô đáy là thẻ bài kem (ô rương thẻ vàng); nền tím lưới vàng (bỏ quầng mờ quanh lưới, ô tím tô
    phẳng giữ vân nhỏ), sảnh casino tím có vòm vàng đèn.
  - vân chì nhẹ: tờ gen dặn "very light, subtle", mặt bàn phủ thêm vân chéo 2 % (`GRAIN`).
  - cắt: `cat_v2.py` (tự dùng bản casino; `--v3` cắt lại bản 3), `ghep_ban_v2.py` (tự dùng bản casino; `--v3` bản cũ); bảng số
    `MachineScoreBoard` hằng số ScreenUvV2, BulbsV2 (26 bóng); chữ cược, chữ đếm, chữ gợi ý thành màu kem (`MachineV2Menu`);
    mặt bàn may_tinh_v2 và phỉnh, ngọc nén ASTC 4x4. Ảnh kiểm: `Temp/PokiShots/casino_man_may_1080.png`.
- 2026-11-21: **chữ số, màn mở rương** (người dùng: "số lệch", "chữ lệch không căn giữa, nút mở tất cả text quá to, fx glowing
  đằng sau nhìn xấu"; gửi ảnh mẫu chùm tia vàng toả lên, hộp quà mở toả sáng; "rương mở hé hé khi chưa tap, thi thoảng lắc lắc hé
  nhẹ, miệng rương ở trong cũng có glow"):
  - chữ số `pk_so_0..9`: hai hàng ô trên tờ GPT vẽ ở độ cao khác nhau, cắt theo trên / dưới chung cả tờ làm 6-9 cao hơn 0-5;
    `cat_v2.py digits()` giờ canh mỗi chữ theo đáy của nó, cao chung = chữ cao nhất; `MachineScoreBoard` digitH 0,86 → 0,72 sh
    (hình cắt sát hơn).
  - tiêu đề ruy băng canh giữa dải đỏ (rect giữa, lề 0, MidlineGeoAligned); nút "Mở tất cả" chữ cao ~36 % nút, nút rộng theo chữ.
  - project hoà màu trong không gian linear: alpha thấp sáng mạnh (vầng tia nền alpha 0,035 trông như ~20 %, nền đen 0,95 vẫn lộ
    mặt máy ~25 %). Bỏ vầng tia lớn sau cả màn, nền đen 0,97.
  - ánh sáng mềm cộng sáng theo ảnh mẫu (`ArtGen/Pachinko/sinh_anh_sang.py --moi` sinh `pk_g_chum` chùm tia toả lên, `pk_g_loe` loé
    ngang): chờ chạm có quầng mềm ấm sau rương (thay vầng tia răng cưa tím / xanh) + lấp lánh chớp quanh rương; mở thì hai lớp chùm tia
    sau rương lắc ngược pha, loé ngang trước miệng, kim tuyến + lấp lánh bắn ra rồi bay lên trong chùm; loé, vòng đổi sang `pk_g_quang`,
    `pk_g_sao`, `pk_g_vong`; quầng ô tổng kết mềm theo độ hiếm (Thường nhạt). Màu ánh sáng mọi bậc đều ấm (`TierLight`).
  - rig rương "nhac" (nhún, lắc, nắp hé có sáng và tia lọt khe) trước đây không chạy: rig trong prefab tắt playOnEnable nên bật holder
    là rig đứng im dáng gốc; `FlyIn` chạy lại "nhac" sau khi rương hiện.
  - menu thử mới "PokiClash/Thử/Máy bi: soi mở 3 rương (đang Play)" (không thả bi, chụp dày lúc chờ chạm).
