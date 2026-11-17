# Tượng đá cổ đại cầm cột đá (`tuong_cot`): tướng thứ 6 đảo Mộc

Bắt đầu 2026-11-17. Con gốc của rig: `monster_3608` (game tham khảo, kho `D:\Ripper\SwordxStaff`), người dùng chỉ (ảnh chụp trang xem
Spine). Xương, lưới, chuyển động gốc là của nhà phát hành game đó: dùng nội bộ, không đăng công khai. Hình là thiết kế của mình.

## 1. Lời dặn của người dùng (2026-11-17)

- "con tướng thứ 6 đảo mộc, concept tượng đá cổ đại cầm 1 cột đá lớn".
- Animation: "bạn thử tự làm các animation đi, yêu cầu của tôi phải độc đáo, lạ và epic, dựa trên rig xương con gốc mà làm".
- Gen bằng Magnific; "đừng làm quá nhiều chi tiết, vừa phải thôi"; gen concept cho người dùng xem trước.

Chưa dặn: tên, số dạng, có thay hẳn `chim_la` hay không. Suất 6 đảo Mộc (ải 30, id game `gio_loc`) hiện là chim bảo hộ rừng cánh lá
(`chim_la`, 2 dạng, đã vào Unity): khi tướng này xong phải hỏi rồi bỏ hẳn tướng cũ (memory "thay tướng thì bỏ hẳn tướng cũ").
Lưu ý trùng chủ đề với tướng 3 đảo Mộc (`tuong_da`, tượng đá giữ rừng màu be, mầm cây, xoắn ốc, lõi hạt xanh): concept này tránh các
nét đó.

## 2. Con gốc (`<SXS>/scan/monster_3608/`: `info.json`, `att_idle0.json`, `att_goc.json`, `khung/`)

- 111 xương, 120 slot, 59 hình bật lúc idle, 13 clip: block_01, die_01, hit_01, hit_01X, hit_02, hit_02X, idle_01 (2 s), run_01,
  skill_01 (vung cột vòng qua đầu), skill_02 (bật nhảy lên, cắm cột xuống), skill_02XX, skill_04, stun_01.
- Golem đá quay phải, đầu thấp giữa hai vai (`P_tou`, mảnh nhọn một xương, không mặt); tay gần (R, vẽ trước) bên trái: vai tròn có lỗ
  khoá (`P_jianjiaR01–05`), nắm tay khối đá rời từng ngón (`P_shouR01`, `P_shouzhiR01–08`); tay xa (L) bên phải: ngón khối đá nắm đầu
  dưới cột (`P_shouL01–09`); cột đá `P_wuqi` một mảnh một xương (bone54) vác chéo sau lưng; lõi cầu xanh `P_jiejingqiu` + `P_qiu`, giáp
  ngực `P_xiongjia01–03`; không chân, cụm đá lơ lửng `P_shitou01–08`; pha lê `P_jiejing01–06`; dây leo `P_tengwan01–02` (lưới).
- Hình cả con khung 0 idle: `inbox/tuong_cot_1/mau/goc_ca_con.png` (`tuong_cot.py ca_con`).

## 3. Lượt 1: concept, ba hướng (Magnific GPT 2.6, 1k high, 95 credit / ảnh, 285 credit)

Script `ArtGen/Spine/tuong_cot.py concept`; file prompt `gui_gpt/tuong_cot_1/luot_1_concept_<A|B|C>.txt`; ảnh `inbox/tuong_cot_1/tai_ve/
L1_<k>.png`; tờ so `inbox/tuong_cot_so_concept.jpg`; chồng viền con gốc `inbox/tuong_cot_1/mau/_so_goc.png`. Ảnh mẫu: con gốc (chỉ lấy
dáng), golem lửa và vượn núi đá đã duyệt (nét vẽ).

| Hướng | Ý (Claude đề xuất) | IoU hình bóng với con gốc |
|---|---|---|
| A | thần giữ đền: đá hoa cương xám, đầu mũ đá vuông mặt nghiêm mắt ngọc, vai khối bậc vuông, lõi ngọc lá trong khung vuông, cột đền tròn có rãnh, hai vòng dây leo | 0,721 |
| B | vua cổ rễ quấn: đá xám ngả lục, vương miện nhọn ba tầng, rễ nâu bò qua vai, tay, cột; lõi ba pha lê lá; cột vuông | 0,710 |
| C | đầu dài bazan kiểu tượng đảo: đá xám lam sẫm, gờ mày, mũi dài, khe mắt xanh; vai tảng tròn; lõi tròn xanh; cột đá thô | 0,762 |

Cả ba: cột to và dài hơn cột gốc một chút (đầu trên cao hơn); cột là một mảnh một xương nên vẽ to hơn vẫn lắp được, nhưng clip vung cột
sẽ quét rộng hơn. Chờ người dùng chọn.

**Người dùng chọn B (2026-11-17)** → `tai_ve/L1_duyet.png`.

## 4. Mảnh (Magnific GPT 2.6, 5 tờ × 95 credit = 475 credit)

`tuong_cot_manh.py` (can → tren → prompt → cat → tay_xa → hong → ghep). Ảnh mẫu duy nhất là concept B (dùng thẳng creation của
Magnific, khỏi tải lên lại). GPT 2.6 giữ đúng chỗ, đúng cỡ như Codex: ghép 21 mảnh lại trùng hình bóng concept 0,950, thêm hai khối đá
lót cắt thẳng từ concept (`hong` giữa tay gần và ngực = chỗ viên đá số 1 của con gốc; `hong_x` dưới cột) → 0,966.

| Nhóm | Mảnh |
|---|---|
| Q1 | `cot` (cột vuông + hai rễ + lá), `da_1..8` (8 đá lơ lửng, khớp đúng 8 viên của họ bằng thuật toán Hungary) |
| Q2 | `dau` (mặt vua + vương miện), `tay_gan` (cánh tay gần + đoạn rễ + lá) |
| Q3 | `vai_gan` (vai vòm + rễ + lá), `than` (ngực + vòng rễ, chừa hốc lõi), `nam_xa` (ba khối ngón tay xa trên cột) |
| Q4 | `lung` (đá sau đầu), `nam_gan` (nắm tay gần một khối), `pha_le_1/2`, `vai_xa` |
| Q5 | `loi` (ba pha lê), `tay_xa` (cánh tay xa, khuất sau cột: vẽ ở góc trống, đặt theo khung part gốc, co 0,825) |

Bỏ: `P_qiu` (viên tròn ở cổ), `P_tengwan02` (dây leo lưng: rễ trên cột đã vẽ liền vào cột). Pha lê `P_jiejing01, 04..06` (khuất lúc
nghỉ) mượn ảnh `pha_le_1/2` đặt đúng khung part gốc. Ngón tay của họ (8 + 8 ngón, xoay tới 100°) không tách: nắm tay gần một khối
trên `bone8`, ngón tay xa một khối trên `bone21` (vẽ trước cột).

## 5. Rig + animation (`tuong_cot_rig.py`, ra `tuong_cot_1/rig/`)

Rig gốc FK thuần (không IK), mọi hình một xương, có bộ xương rời cho run_01 / die_01 của họ (bỏ). Mỗi mảnh của mình bám một xương
riêng `m_<mảnh>` (con của xương gốc, đặt ở tâm mảnh) nên appear / die tách từng mảnh bay riêng. 98 xương, 28 slot, 3371 đỉnh, 8 clip,
18 sự kiện, `.atomik` 286 KB (đạt). Mọi clip nối về khung 0 idle 0,00 px; appear khung đầu trống, die khung cuối trống; trang xem chạy
đủ 8 clip (`thu_xem.py`); runtime Spine thật khớp bộ vẽ Python (`rig/that/`).

Claude tự thiết kế (người dùng: "độc đáo, lạ và epic"):

| Clip | Diễn | Sự kiện (cho VFX) |
|---|---|---|
| appear 2,85 s | PHẾ TÍCH THỨC TỈNH: cột rơi từ trời cắm đứng xuống đất; các mảnh nằm rải thành đống phế tích hiện dần, rung rồi lần lượt bay vòng cung lên ráp quanh lõi (đá → ngực → lưng → tay xa → vai → tay gần → nắm tay); lõi bừng sáng; đầu rơi xuống cổ sau cùng; nhổ cột vác lên lưng (block_01 của họ), ngửa đầu | cam_cot 0,32 · loi_sang 1,06 · dat_dau 1,32 · nho_cot 1,46 |
| idle 4 s | idle_01 hai vòng + đá nhấp nhô lệch pha, pha lê trôi, lõi phồng xẹp; trò: đầu nhấc khỏi cổ ngó lên rồi đặt xuống nảy nhẹ (2,15 → 3,55 s) | dat_dau 3,55 |
| walk 1,2 s | trôi nặng: thân nhún hai nhịp, ngả tới, tay gần đưa, đá và pha lê trễ sau | |
| attack 1,4 s | TRỤ CÔNG THÀNH: vung cột lên cao, khựng, bổ ngang tới trước (skill_01 của họ bỏ đoạn hạ chéo), lao 0,3 cao | trung 0,58 |
| cast 1,95 s | RỄ TRÓI ĐẤT: nhảy lộn vòng cắm cột xuống đất (skill_02), giữ cột gồng cho rễ chạy dưới đất tới đối thủ, rút cột; xương `mieng` = chân cột | cam 0,76 · trung 1,12 · rut 1,36 |
| skill 3,05 s | THẦN TRỤ GIÁNG THẾ: nhấc cột qua đầu (skill_04), tung lên trời xoay 1,5 vòng; giơ tay gồng, đá bị hút bay lên quanh thân, lõi phồng; cột KHỔNG LỒ (×1,85) giáng thẳng xuống chỗ đối thủ (xương `fly_cot` → `cot_bay`, game co quãng), cắm rung; nhổ lên, thu nhỏ, bay vòng cung về tay xoay một vòng, bắt lại khựng | nem_cot 0,56 · tu 0,62 · giang 1,42 · trung 1,64 · re 1,72 · bat_cot 2,62 |
| hit 0,5 s | hit_01 + lõi co giật, pha lê văng | |
| die 1,75 s | SỤP ĐỔ: lõi chập chờn rồi tắt (còn hốc rễ), mọi mảnh rơi theo trọng lực, lật, nảy, nằm thành đống; cột đổ ra sau quanh chân, nằm ngang trên đống; mờ | tat 0,30 · sup 0,34 · do 0,86 |

Cú xoay nhanh còn lại (20–80° mỗi khung 60/s) nằm sẵn trong clip gốc (nhảy lộn cast, nhấc cột skill, bổ cột attack), không có
bước quấn 360°. Cánh tay xa lúc giơ cao (skill) lơ lửng tách vai như kiểu golem đá rời của con gốc.

## 6. Việc tiếp

1. Người dùng xem `rig/xem.html`, góp ý.
2. VFX (bụi cột cắm, rễ chạy đất của cast, bóng / vết nứt báo trước + sóng chấn khi cột giáng, lá hút vào lõi) theo bộ hạt Mộc.
3. Hỏi: thay hẳn `chim_la` (suất 6, id `gio_loc`)? cần dạng 1 không? tên.

## 7. Lượt sửa 1 (người dùng 2026-11-17: "đánh thường tôi chưa hiểu lắm"; "chiêu mana có 1 đoạn giật frame"; "có cần dạng 1"; "tên bạn tự đặt")

- **Chiêu mana giật**: skill_02 của họ có hai khoá bậc lộ rõ ở hình to (0,53 → 0,56 s thân bật từ chúc ngược sang đứng trong một khung;
  0,69 → 0,72 s thân tụt 270 đơn vị trong một khung), cộng đoạn rung hai khung lúc gồng. Bỏ skill_02, dựng lại bằng ba dáng khoá của họ
  (idle 0, skill_01 0,68 = cột dựng giơ cao, block_01 0 = cột cắm đứng trước mặt): nhún → bật nhảy (0,42 cao) → lộn một vòng trơn quanh
  tâm thân (`lat`, tâm đi theo độ cao nhảy) → nện cột cắm đất 0,76 → tì người vào cột gồng (sóng sin, không rung) → rút cột (block_01) →
  idle. Đo 60 khung/giây: không còn bước xoay > 25° ở xương nào.
- **Đánh thường** làm lại cho dễ đọc: ĐẬP TRỤ = giơ cột thẳng lên trời (0 → 0,30), khựng 0,12 s, lao tới đập cột chúi xuống đầu đối thủ
  (0,50, khung trúng), khựng 0,12 s, về theo đường của họ (cột vòng qua đầu lên vai). Lúc đầu thu về bằng pha thẳng thì cột quét vòng
  xuống đất: đổi sang dùng đoạn về của skill_01.
- **Tên (Claude đặt)**: dạng 2 **Cổ Vương** (danh hiệu "Tượng vua cổ cầm trụ"); dạng 1 **Cổ Vương Nhi**. Đòn: Đập Trụ / Rễ Trói Đất /
  Thần Trụ Giáng Thế. (Tránh "Lâm Vương" vì đã có Lâm Tượng; "Trụ Vương" trùng tên vua bạo chúa.)
- **Dạng 1**: tờ ứng viên `inbox/tuong_cot_dang1_ung_vien_2.png` (A 3273 cổ vật đá chạm tròn, B 3274 dạng lớn của nó, C summons_3932 golem
  đá nhỏ đeo ngọc, D summons_3181 bia đá dựng, E 3226 cục đá một mắt, F 3253 vòm đá rêu đội nấm, G chính 3608 thu nhỏ). Cả bảy đều có đủ
  clip idle / run / skill / hit / die. Chờ người dùng chọn.
- **Người dùng chọn rig dạng 1: A (monster_3273)**. Mã làm việc `tuong_cot_non`, script `ArtGen/Spine/tuong_cot_non.py`. Concept lượt 1
  (Magnific GPT 2.6, 2 × 95 = 190 credit; ảnh mẫu: con gốc 3273, concept Cổ Vương đã duyệt, Thiết Tinh làm mốc vẽ mặt nhỏ): A vương miện đá
  hai tầng + hai rễ lá như tai, tay nắm đá quấn rễ (IoU 0,741); B mũ đầu cột vỡ có đai bậc + một rễ bò chéo, tay phiến đá (IoU 0,804). Cả hai:
  một mắt xanh hẹp nhìn phải dưới gờ mày, hốc bụng là cụm pha lê lá trong vòng rễ, thân tròn đá xám lục, chân đá ngắn. Tay của mình gần thân và
  nhỏ hơn tay cuộn của họ (tay là mảnh cứng một xương nên đặt theo concept được). Tờ so `inbox/tuong_cot_non_so_concept.jpg`. Chờ chọn.
- **Người dùng chọn concept A** → `tuong_cot_non_1/tai_ve/L1_duyet.png`. Hỏi thêm "chiêu mana tôi thấy tướng xoay 1 vòng là sao nhỉ": cú lộn
  vòng (giữ từ clip gốc) bị bỏ hẳn; chiêu mana dạng 2 giờ: nhún, giơ cột, bật nhảy (ngả nhẹ ra sau rồi chúi tới), nện cắm cột.

## 8. Dạng 1: Cổ Vương Nhi (`tuong_cot_non`, rig monster_3273)

- Mảnh (`tuong_cot_non_manh.py`, Magnific 2 tờ × 95 = 190 credit): N1 `than` (thân tròn + gờ mày + miệng + đai eo + vòng rễ, hốc tối, không
  mắt, không pha lê); N2 `mu` (vương miện + hai rễ lá), `loi`, `mat`, `mat_nham` (vẽ ở góc trống, đặt trùng tâm `mat`), `tay_trai`,
  `tay_phai`, `chan_trai`, `chan_phai`. Ghép trùng concept 0,972. Bỏ P_huo (đốm lửa 6×7 của họ).
- Rig (`tuong_cot_non_rig.py`): 12 xương của họ + `m_<mảnh>` + `far`, `fly_cot` → `cot_bay` (cột nhỏ mượn ảnh `cot` dạng 2, dựng đứng, dài
  1,05 chiều cao). 26 xương, 10 slot, 8 clip, `.atomik` 168 KB (đạt), mọi clip nối idle 0,00 px; runtime thật khớp (0,28 px).
  Bẫy: hình CỨNG (region) trong Spine luôn bám xương của SLOT, không bám xương ghi trong spec; slot cột ban đầu đặt trên `move` nên runtime vẽ
  cột ngay trước mặt tướng (lệch 636 px so với bộ vẽ Python). Slot phải nằm trên đúng xương (`sk.slot("cot_bay", "cot_bay", ...)`).
- Clip: appear LĂN TỚI (cuộn tròn lăn một vòng từ trái vào, mắt nhắm, tay chân + vương miện thu hẳn; dừng nảy; bung so le; mắt mở; lõi sáng;
  vung hai nắm tay lên) · idle (idle_01 + lõi phồng xẹp, vương miện lắc, chớp mắt 2,6 s) · walk = run_01 · attack HÚC VƯƠNG MIỆN (ngả ra sau,
  lao chúi chóp vương miện tới 0,52 cao, nhắm mắt lúc trúng, bật về; trúng 0,46) · cast RỄ CON (giơ hai nắm tay, nện xuống đất 0,62, gồng;
  rễ VFX tới đối thủ 0,95) · skill TIỂU TRỤ GIÁNG (giơ hai tay gồng gọi, cột nhỏ từ trời giáng xuống chỗ đối thủ 1,18, cắm rung, lún mờ;
  nhảy cẫng) · hit (hit_01, mắt nhắm khi họ hiện mắt chữ X) · die (die_01 lật ngửa, mắt nhắm, lõi tắt, mờ).
- Chưa làm: clip tiến hóa (dạng 1 → Cổ Vương), VFX, vào game.

## 9. Bản xem trước có đối thủ + hiệu ứng tạm (người dùng 2026-11-17: "dạng 2 của nó tôi thấy xoay đúng 1 vòng rồi làm gì đó, animation này là sao tôi chưa hiểu")

- File xuất 16:27 đã không còn clip nào xoay cả thân một vòng (chỉ cột tự xoay khi bị tung ở chiêu cuối); tab người dùng xem có thể là bản cũ
  (cú lộn ở chiêu mana trước khi bỏ). Nguyên nhân chính khó hiểu: chưa có VFX, chiêu mana chỉ thấy "cắm cột rồi đứng".
- `ArtGen/Spine/tuong_cot_fx.py` (khung sân, hạt của tho5_fx / fxlib; hai rig có `dung_het(far_xy)`): rễ trồi (dải cong thuôn nâu viền mực,
  lá ở ngọn), rễ nối nhau dọc đất tới đối thủ rồi quấn quanh; lá hút xoáy vào lõi; bóng báo dưới chân địch; vết nứt; vòng bụi; dăm đá.
  GIF + tờ soi: `inbox/tuong_cot_fx/` (trang `xem.html`), cả 6 chiêu của hai dạng.
- Sửa nhờ bản xem trước: cột khổng lồ (dạng 2) và cột nhỏ (dạng 1) trước cắm theo mặt đất PHE MÌNH (rig y = 0) nên ở sân thật thò xuống dưới
  chân địch; nay chân cột theo mặt đất dưới đối thủ (far.y − 0,45 cao) và lệch về phía trước địch (0,18 / 0,12 cao) cho đỡ che con bị trúng.

## 10. ĐÃ VÀO GAME (2026-11-17 ~16:50–17:05; người dùng: "ok ổn cho vào game đi")

- **Suất**: tướng 6 đảo Mộc = ải 30 "Thung Lũng Lá", id game GIỮ `gio_loc` (thay hẳn Linh Điểu / chim_la). Giữ id thẻ, chỉ số, hiệu ứng
  thẻ, tên thư mục dạng. Tên Claude đặt: **Cổ Vương** ("Tượng vua cổ cầm trụ", "Dòng Cổ Vương"); dạng 1 **Cổ Vương Nhi** (`gio_loc_1`
  = `tuong_cot_non_th.atomik`, cỡ 0,88, có clip evolve), dạng 2 **Cổ Vương** (`gio_loc_2` = `tuong_cot_1.atomik`, cỡ 1,1); thẻ Rễ Trói Đất
  (seed), Thần Trụ Giáng Thế (rock), Thân Đá Rời (shield, né đòn), bị động boss Rễ Hút Linh Lực (leaf). Script `quai/doi_co_vuong.py`
  (dữ liệu, `th` gộp tiến hoá, `chep`), `quai/da_nhan.json` cập nhật.
- **VFX** `Assets/01 Script/Game/Battle/HatCoVuong.cs` (rễ = `Spike` màu `ReC`, tảng đá rêu `Thach` / `ThachNo`, bụi, lá): `n_tru_dap` /
  `n_vuong_huc` (đòn thường theo dạng, `StageView.AtkDang`, cả hai trong `HatLua.AtkLao`), `n_re_troi` (chiêu mana, `MocFx`), `n_tru_giang1`
  / `n_tru_giang` (chiêu cuối theo dạng). Màu `HatNuoc.WThemes["gio_loc"]` (lục lá, dăm đá xám lục "giap"). `HatChim.cs` bỏ ba chiêu chim,
  GIỮ đồ dùng chung (SoiGio: HatKiem / HatSoi; ThachU: HatTho; Thach / ThachNo: Cổ Vương). Menu thử đổi tên (MocFxTour.TryChim).
- Biên dịch thử ngoài Unity 0 lỗi; Unity: refresh, Nhập dữ liệu, Gắn dạng (gio_loc_1 124 xương 9 clip, gio_loc_2 98 xương 8 clip, prefab 2
  dạng); EditMode 122/123 (hỏng duy nhất PrefabOnlyTests có từ trước). Golden không đổi (số dạng, chỉ số, hiệu ứng thẻ giữ; golden không
  chứa tên).
- Tour trong trận (menu "Đảo Mộc: rễ trói đất và thần trụ giáng thế Cổ Vương ...", ảnh `Temp/PokiShots/thuy_fx/gio_loc_*`); tờ tổng
  `inbox/tuong_cot_trong_tran.jpg`. Đã xem: tên, thẻ, đập cột / húc, rễ quấn, cột khổng lồ giáng đúng chỗ đối thủ và bay về, cột nhỏ dạng 1.
  CHƯA xem: Cổ Vương là địch (boss ải 30 đánh xuống), appear / die / evolve trong game, hộp chi tiết tướng.
