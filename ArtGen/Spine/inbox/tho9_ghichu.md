# Tướng 9 đảo Thổ (ải 60, mini boss): ba hướng concept (`tho9`)

Bắt đầu 2026-11-17 (máy ổ C, kho `D:\Ripper\SwordxStaff`). Suất 9 đảo Thổ = ải 60 "Lò Gốm Đất Nung" (`IslandGen.cs` Plan Tho), id game hiện
là **`cu_phu`** (Cự Phủ, chiến binh rìu tím). Tên, số dạng, có thay hẳn `cu_phu` hay không: chưa bàn. Xương, lưới, chuyển động gốc là của
nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai.

## 1. Lời dặn của người dùng (2026-11-17)

- "làm tướng thứ 9 đảo thổ; tôi không nghĩ ra concept nữa rồi, bạn research và cho tôi concept đi, miễn đẹp, epic và chiến hơn 8 con trước
  là được". Người dùng giao Claude chọn cả con gốc lẫn concept (khác suất 6–8, người dùng tự chỉ con gốc).

## 2. Chọn rig

- Tờ thu nhỏ cả 347 con quái / boss (`web/thumbs/Monster`), lọc con to, có đòn mạnh, chưa dùng ở đảo nào, hợp hệ đất: 3662 rồng kaiju,
  3664, 3666 khủng long gai pha lê, 3626, 3623, 3628, 3457 bò yak giáp, 3456, 3602 quỷ rìu, 3413 bò rừng, 3403 quỷ vác phiến đá, 3517 hiệp
  sĩ rìu, 3622 hổ trắng, 3411 gấu, 3533.
- `chay.py info` cả 15 con, tờ khung chiêu 6 con (3626, 3623, 3662, 3457, 3456, 3602). Chọn ba rig có đòn mạnh nhất và dáng khác nhau:
  - `monster_3623` (127 xương, 25 clip): sư tử đá vác hai đại kiếm + một kiếm sau lưng; kiếm bay ra chém, mưa kiếm (skill_03_1, skill_04_1
    3,13 s); bộ clip `_2` là dạng ngậm một kiếm ngang miệng.
  - `monster_3626` (125 xương, 29 clip): quái thú gù mai đồng, xích, tinh thể trên tay; skill_04 nhảy vọt khỏi khung rồi nện; skill_05 đập
    đất mảnh vỡ văng; mọi clip có bản `_B` (dạng nổi giận, tinh thể bật lên vai).
  - `monster_3456` (99 xương, 11 clip): người quạ cánh lông, búa nhỏ + dùi; skill_03 vút lên khỏi khung rồi bổ nhào, skill_04 móc lên.
  - Không lấy 3662 (rồng, trùng kiểu rồng sa thạch suất 4, clip hiền), 3457 (đòn chỉ húc), 3602 (nhỏ, rối).
- Quét vào `<SXS>/scan/monster_<số>/`: `info.json`, `att_goc.json`, `att_idle0.json` (idle khung 0: 3623 `idle_01_1`), `khung/*.jpg`.

## 3. Concept lượt 1 (Claude đề xuất ba hướng, mỗi hướng một rig; chờ người dùng chọn)

Script `ArtGen/Spine/tho9.py` (ca_con, slot, concept, so_goc; dùng lại `tho5.py`). File prompt `gui_gpt/<mã>_1/luot_1_concept_<k>.txt`,
hướng dẫn `gui_gpt/tho9/HUONG_DAN.md`. Ảnh mẫu: 1 = con gốc (chỉ lấy dáng), 2 = rồng giáp sa thạch, 3 = vượn núi (nét). Gen thẳng bằng công
cụ Magnific trong phiên (GPT 2.6, 1k high, 3:2, 95 credit / ảnh, 285 credit cả lượt; ~1 phút / ảnh, ba ảnh song song).
Trang so: `inbox/tho9_xem_concept.html` (con gốc, concept, tờ khung clip gốc, đề xuất chiêu).

| Hướng | Mã | Rig | Nội dung | IoU |
|---|---|---|---|---|
| A | `nhan_su` | 3623 | nhân sư sa thạch, khăn trùm đầu kẻ sọc đất nung / kem thay bờm, râu tết, ba BIA KIẾM hình tháp mũi hổ phách, dây da | 0,810 |
| B | `nguu_ma` | 3626 | trâu nước khổng lồ đứng hai chân, sừng trâu cong, khoen mũi đá, lưng mọc NÚI BÀN sa thạch có ba cụm hổ phách, bờm nâu, giáp đá cẳng tay, vòng cùm đá nứt, dây thừng đứt | 0,712 |
| C | `thach_quy` | 3456 | gargoyle đá: sừng cừu, nanh, tai dơi; cánh dơi lợp phiến sa thạch; búa tạ đầu bazan gắn hổ phách; cọc đá; khố đỏ | 0,718 |

Claude soi: cả ba đúng dáng, đúng hướng, chi dính thân, nhìn ra con khác. Lưu ý khi đưa duyệt: A ba bia kiếm (lục giác, mũi cam, chuôi tròn)
trông như bút chì sáp, cần gen lại dáng lưỡi; B đầu và vai to, cao hơn khung rig (đầu gốc nhỏ, thấp giữa hai vai), phải nắn khi chia mảnh;
C cánh và thân rộng hơn rig, búa to hơn búa gốc (mảnh cứng một xương nên lắp được). Claude đề xuất B.

**Người dùng (2026-11-17): "nhìn được nhưng chưa đủ ấn tượng so với các con trước, bạn có thể tự nghĩ concept của riêng mình".**
(Diễn giải của tôi: ba hướng lượt 1 là kiểu nhân vật quen thuộc (nhân sư, minotaur, gargoyle) và cùng bảng vàng cát / nâu với 8 con trước;
thiếu một điểm nhấn nhìn là nhớ.)

## 3b. Concept lượt 2: ba ý tưởng riêng của Claude, trên rig boss

Rig mới (đều chưa dùng): `monster_3806` (98 xương, 65 slot, 15 clip; quái thú gù ôm chuỗi quả cầu + vòng; skill_03 bật lên xoay một vòng quanh sân cùng các
quả cầu, skill_04 dựng đuôi chạc đâm, skill_05 lao mờ; 9 clip chiêu), `monster_3624` (rồng rắn; skill_04_1..3 vọt khỏi khung lên / xuống),
`monster_3704` (rồng giáp cánh tấm; skill_02 / skill_05 bắn mũi nhọn rồi thu về, skill_04 bay vút khỏi khung 3 s, skill_06 khép cánh xoay
rồi bung). Atlas 3806 có HAI trang (`.png` + `_2.png`): đã sửa `mo_xe/to_manh.py` (doc_atlas ghi trang của từng vùng, nap mở đúng trang;
atlas một trang không đổi).

`tho9.py concept2` (bảng `HUONG2`, `MOOD2` đòi "epic hơn mọi tướng Thổ trước, tương phản màu", `style2` = style() đổi "VERY SIMPLE" thành
"CLEAN, BOLD ... moderate detail"). Ảnh `inbox/<mã>_1/tai_ve/L1_<k>.png`, 285 credit.

| Hướng | Mã | Rig | Nội dung | IoU |
|---|---|---|---|---|
| D | `tinh_hach` | 3806 | THIÊN THẠCH THÚ: da đá vỏ chai đen mạch hổ phách, sừng mũi pha lê hổ phách, hai sừng ngọc lam, lưỡi liềm thành hốc tinh thể bổ đôi lòng ngọc lam, đuôi giáo ba chạc hổ phách, quả cầu thành HỐC ĐÁ (geode) nứt lộ lõi hổ phách / ngọc lam | 0,710 |
| E | `son_long` | 3624 | LONG MẠCH: rồng phương Đông thân là dãy núi, vây lưng thành tháp đá vôi, CHÙA ĐÁ ba tầng mái ngọc lam trên đỉnh, thân đỏ hẻm núi, vây lớn thành vách đá phân tầng | 0,690 |
| F | `phach_long` | 3704 | PHÁCH LONG: giáp cẩm thạch kem, cánh là quạt LƯỠI PHA LÊ HỔ PHÁCH có bóng chuồn chuồn hoá thạch, mũ ba gai ngọc hổ phách, gai hổ phách | 0,689 |

Claude soi: cả ba đúng dáng, chi dính thân, khác hẳn con gốc, nổi hơn lượt 1. Lưu ý: D lưng và tay to hơn rig; E khối núi trên lưng to hơn
hàng vây gốc (lúc chia mảnh: mỗi tháp một mảnh cứng trên xương vây); F cánh rộng hơn, thân nhỏ hơn (mỗi lưỡi cánh là mảnh cứng, lắp dễ).
Đề xuất chiêu ở trang so; F có cơ chế "nhốt đối thủ trong hổ phách" (choáng). Claude đề xuất D.

**Người dùng (2026-11-17): "tôi thích D nhất nhưng nhìn quá giống con gốc".** D giữ 1:1 mọi mảnh nhận diện của 3806 (hai sừng dài vuốt
sau, sừng mũi, lưỡi liềm bên sườn, cung quả cầu tròn, vòng, đuôi chạc); chỉ đổi màu, mặt, chất liệu.

## 3c. Concept lượt 3: ba biến thể D đổi dáng mảnh nhận diện

`tho9.py concept3` (bảng `HUONG3`, `PLAN3` bỏ mọi chữ "sừng dài / lưỡi liềm / quả cầu / vòng", `COMMON3` = giữ da đen mạch hổ phách + mặt dữ,
CẤM các mảnh cũ). Ảnh mẫu 2 = `L1_D.png` (chỉ lấy màu, chất liệu, mặt). Rig cho phép: đầu / sừng `jiao_*`, `tou` cứng trên xương đầu `all6`;
đuôi `weiba`, từng quả cầu `qiu_*`, từng vòng `jinhuan_*`, mây `yun_*` là mảnh một xương; lưỡi liềm `shenti_04` là lưới trên xương thân
(`all4/7/8/9`). Vòng, mây, sao bỏ thì ẩn slot. Ảnh `tinh_hach_1/tai_ve/L2_<k>.png`, tờ chồng viền `tinh_hach_1/mau/_so_goc_L2.png`, 285 credit.

| Bản | Nội dung | IoU |
|---|---|---|
| D1 Gù thiên thạch | lưng = tảng thiên thạch khổng lồ nứt mạch ngọc lam; vương miện 3 tinh thể hổ phách, 2 nanh vểnh; sườn giáp đá chồng; đuôi CHÙY đá cắm gai hổ phách; mảnh thiên thạch góc cạnh bay | 0,592 |
| D2 Lưng rừng tinh thể | rừng trụ tinh thể ngọc lam + hổ phách trên lưng, vai; diềm đá sau đầu viền gai hổ phách; đuôi xoè 3 lưỡi ngọc lam; cụm tinh thể bay | 0,612 |
| D3 Bờm thiên thạch | bờm sư tử bằng đá thiên thạch; ba miệng hố va chạm chứa hổ phách trên lưng; đuôi một lưỡi giáo ngọc lam; tảng đá lõi ngọc lam bay | 0,625 |

Claude soi: cả ba khác hẳn con gốc, thân / tay / đuôi vẫn trùng khung rig, chi dính thân. Khối trên lưng (D1 tảng, D2 trụ tinh thể, D3 bờm) to
hơn bướu gốc: là mảnh cứng gắn xương thân / đầu, lắp được.

**Người dùng chọn D2 (2026-11-17): "làm D2"** → `tinh_hach_1/tai_ve/L1_duyet.png` (= `L2_D2.png`): thú thiên thạch đá vỏ chai đen mạch hổ
phách, RỪNG TRỤ TINH THỂ ngọc lam + hổ phách trên lưng, diềm đá sau đầu viền gai hổ phách, đuôi quạt ba lưỡi tinh thể, năm cụm tinh thể
bay. Mã làm việc `tinh_hach`, rig `monster_3806`.

## 3d. Mảnh "đúng chỗ, đúng cỡ" (`tinh_hach_manh.py`, như quy_nui_manh.py)

Concept căn lên con gốc: co 0,87 + dời (IoU hình bóng 0,72; concept to hơn rig ~15 %, `mau/can.json`). Gen Magnific (ảnh mẫu duy nhất =
creation của D2), 7 tờ × 95 credit. Q1 thân; Q2 đầu + 5 cụm bay (+ tay gần, BỎ); Q3 tay xa + đuôi; Q4 hàm + móng tay gần; Q5 lòng miệng +
móng tay xa; Q6 cả rừng tinh thể (sau thân, chân cụm kéo dài khuất sau thân); Q7 tinh thể lớn vắt vai (trước thân) + tay gần.
- Lượt đầu Q2–Q5 mỗi tờ đều vẽ lại gần TRỌN rừng tinh thể có đáy phẳng (dặn "mỗi tờ một cụm, đáy phẳng" là sai) → ba bản chồng nhau; Q2 vẽ
  tay gần lấn cả mảng ngực có mạch hổ phách. Sửa: rừng gen MỘT ảnh (Q6), tinh thể vắt vai riêng (Q7, vì trên concept nó nằm TRƯỚC thân),
  tay gần gen lại kèm toạ độ vai / khuỷu / bàn và câu "ngực có hai mạch hổ phách không phải tay" (Q7). Bảng `BO` bỏ bản cũ khi cắt.
- Ghép 24 mảnh lại trùng hình bóng concept 0,941 (`manh/_ghep.png`). Móng: tay gần 2 khối (1 + 3 móng dính nhau), tay xa 2 khối.

## 3e. Rig (`tinh_hach_rig.py`, ra `tinh_hach_1/rig/`)

- Xương của họ dựng ở KHUNG 0 IDLE (dáng gốc của rig lệch khung 0 idle tới ~140 đv ở ngón tay; mảnh đặt theo hình khung 0 idle). Rig có 20
  xương kế thừa `noRotationOrReflection` (all5, all6, all7–9, shenti_03/04 ...) mà bộ dựng .atomik không có: góc riêng các xương đó = góc thế
  giới (trường `m` của mẫu khung) − góc thế giới của cha; vị trí riêng lấy `l`. Kiểm: xương của mình lệch khung 0 idle của họ 0,06 đv.
- Hình region / lưới không trọng số của họ đổi về dạng lưới trước khi gộp (`att_luoi`). Bỏ xương vòng, mây, sao, tinh vân, thân rồng biến
  hình `shenti_z*`, đuôi chạc `weiba`. 67 xương, 18 slot (+5 slot bản sao cụm bay), 2543 đỉnh.
- Gắn: thân trên gộp shenti_02/04/03; tay trên gộp bắp + cẳng + ngón của họ (làm trơn trọng số); đầu / hàm / lòng miệng trên tou / zuiba_02 /
  zuiba_01; móng cứng trên xương ngón nặng nhất ở tâm móng; 5 cụm cứng trên qiu_07/01/02/04/05 (gán một – một); rừng tinh thể trên hai
  xương riêng tt_sau (con all4) / tt_truoc (con all5) hoà theo bề ngang; tinh thể vắt vai trên tt_nam_g (con all5); đuôi chuỗi duoi0..2 (con
  all3, khớp đọc trên concept). Góc hàm all10: DƯƠNG = KHÉP (hàm xoay lên chui vào đầu; ghi "dương = há" trước đây sai, đo lại 2026-11-18 ở `tinh_hach_non_ghichu.md` mục 5: mọi pha há / gầm của bản đang trong game đang khép miệng; code đã đổi chiều bằng `HA = -1`, bản trong game chưa xuất lại).
- Clip: tay gần của mình KHÔNG giơ quá đầu được (lưới tay của họ mảnh, giơ cao kéo tay mình thành cọng dài như xúc tu: thử skill_02,
  skill_04 đều xấu) → attack và skill tự viết trên dáng idle, chỉ xoay thân / đầu / hàm / tay xa:
  - appear 2,5 s: rơi từ trời (nghiêng), đáp nện + bẹp nảy, 5 cụm trồi lên so le, rừng tinh thể dựng lên nảy, gầm (cham_dat, nen,
    tro_lai, gam);
  - idle 4 s: sóng mềm lệch pha (thở, đầu, hàm, hai tay, rừng, đuôi, cụm nhấp nhô) + trò 2,05 → 3,25 s: lắc đầu rũ mình, rừng tinh thể rung
    lách cách;
  - walk = run_01; hit = hit_01 + đuôi quất; die = die_01 (bỏ khung 0 khoá bậc, hoà từ idle 0,12 s) + cụm rơi + tan;
  - attack 1,0 s "cắn xé": lùi lấy đà, ngóc đầu há to, tay xa giơ → lao tới đớp + tay xa vồ xuống (trung 0,50);
  - cast 2,3 s: đoạn gầm skill_04 (ngóc đầu thêm), 5 cụm bay thành VÒNG elip quanh thân, phóng lần lượt 1,05 → 1,45 s tới đối thủ (far +
    fly_j, game co quãng), cụm thật mọc lại 1,95 s (bay, phong, no, trung, moc);
  - skill 2,8 s "mưa thiên thạch": thu mình rừng rung → bật dậy gầm, rừng tinh thể phóng vọt lên trời 0,62 s (ẩn), tay xa chỉ trời, mưa
    1,00 s (VFX), hạ người nện 1,80 s (trung), rừng mọc lại 2,10 s.

- Bản xuất 2026-11-17: 78 xương, 23 slot, 4192 đỉnh, 8 clip, 31 sự kiện, `.atomik` 393 KB (đạt đích 0,4 MB); mọi clip nối về khung 0 idle
  0,00 px, idle khép vòng 1,9 px, walk 4,3 px (sóng đuôi / cụm bay phải khép đúng độ dài clip 1 s); trang `tinh_hach_1/rig/xem.html` chạy đủ
  8 clip (`thu_xem.py`); tờ khung runtime Spine thật `rig/that/`.
- Lỗi đã sửa sau soi: bản sao cụm bay (slot ẩn) hiện ra khi appear / die chỉnh độ mờ cả con (bỏ qua slot `bay_*`); khung 0 của die_01 là
  khoá bậc (cả con bật 40–100°): bắt đầu từ khung 1, hoà từ idle 0,12 s; tay xa vẽ sau đầu nên giơ cao thì chỉ lòi móng trên đầu như sừng
  (skill "chỉ trời", attack lấy đà) → giơ ít, chỉ vồ / nện là mạnh.

**Người dùng xem lượt 1 clip (2026-11-17): "đánh thường nhìn yếu quá", "chiêu cuối chưa đủ epic", "cho các đảo bay xung quanh người nó",
"animation xoay tay cast chiêu ở mana có thể làm đẹp hơn, xem con gốc".** Lượt 2 (`tinh_hach_rig.py`, khối clip viết lại):
- `aura` 8 s (clip lặp chồng lên mọi clip, AtomikPose.Overlay): 5 đảo bay vòng elip nghiêng −9° quanh người, tâm ngang giữa thân, rộng nửa
  bề ngang thân + 0,30 cao; mỗi đảo hai slot (`cumN` sau lưng, `cumN~t` trên cùng), aura đổi HÌNH (att) ở hai mép vòng (đảo không chồng thân
  ở đó); nửa xa nhỏ 13 %, nhấp nhô, tự xoay. Clip trận KHÔNG khoá xương qiu_* nữa (trừ appear: trồi lên, die: rơi, cast: tắt / mọc lại).
- cast 2,4 s: như skill_04 của họ (tay gần co trước ngực khuấy vòng, vuốt xoè) nhưng bằng IK (`ik_hai_doan` dabi_r / xiaobi_r) tới vòng tròn
  trước ngực, cổ tay xoay theo vòng, vuốt xoè, hất tay ở mỗi lần phóng; đầu ngóc gầm. Đảo thật tan đi (0,30 s), bản sao `bay_j` hiện thành
  lốc đảo xoay trước bàn tay, lần lượt phóng 1,10 → 1,50 s tới far; đảo thật mọc lại 2,00 s.
- attack 1,15 s: VỒ LAO trên xương move (0,55 cao, game kéo tới đối thủ; `lao=("attack","skill")`): thu mình bẹp → bật vồ cong lên, há to →
  đớp + tay xa vồ (0,46) → XÉ lắc đầu hai nhịp → nhảy lùi về.
- skill 3,0 s THIÊN THẠCH GIÁNG THẾ: thu mình rừng rung → gầm, rừng phóng lên trời (0,55) → nhún → bật cao 1,05 cao → ở đỉnh cuộn người lộn
  một vòng (all3 −360°, giữ −360° tới hết clip: về 0 thì runtime quay ngược một vòng) → lao chéo xuống nện ngay đối thủ (1,62, lao 0,60 cao)
  → gầm trên đối thủ, mưa thiên thạch 1,66 / 1,86 / 2,02 (VFX) → nhảy về (2,10 → 2,50) → rừng mọc lại.
- Đo runtime thật 60 khung/giây: bước xoay lớn nhất skill 29°, attack 37° (ngón lúc vồ), cast 50° (đảo đang bay xoay); bản sao đảo giữ góc
  lúc tới đích (tắt rồi mà góc bật về 0 là lộ nửa khung quay ngược). `.atomik` 398 KB (9 clip gồm aura).

**Người dùng xem lượt 2 (2026-11-17): "chiêu mana vẫn dùng 2 tay xoa nhau, các thiên thạch xung quanh bay nhanh hơn rồi lao vào người đối
thủ", "làm các thiên thạch bay xung quanh kiểu atom chứ không phải xoay quanh 1 vòng", "chiêu cuối tướng cuộn người lại thành 1 quả bóng
thiên thạch đầy gai, các thiên thạch xung quanh quay cực nhanh để lại trail rồi bay lên cao, lao xuống người đối thủ như 1 viên thiên thạch,
có hiệu ứng xé gió tạo lửa rồi nổ rất lớn".** Lượt 3 (bản lượt 2 cất ở scratchpad `t9/tinh_hach_rig_v2.py`):
- **Quỹ đạo nguyên tử**: mỗi thiên thạch một elip nghiêng riêng (0°, 22°, 45°, 135°, 158°) quanh tâm thân + đầu; bán trục 924 × 240, quỹ
  đạo dốc thì co bán trục lớn cho nửa bề cao ≤ 0,65 × độ cao tâm (không chui xuống đất). Elip dựng bằng chuỗi hai xương quay ngược chiều
  (`quy_j` quay +u → `quy2_j` −2u → `dao_j` mang hình; z = e^{iα}(a e^{iu} + b e^{−iu})) nên mọi clip CỘNG thêm vòng quay (+Δ, −2Δ, +Δ)
  mà không cần biết aura đang ở pha nào; `dao_j` giữ thẳng đứng. Co quỹ đạo về một điểm = dời `quy2_j`, `dao_j` về 0 (điểm biết trước,
  độc lập pha) → bản sao `bay_j` phóng đi từ đó. Xương `qiu_*` của họ không dùng nữa.
- **Vệt bay**: mỗi thiên thạch thêm hai chuỗi bóng mờ `quy_g1/g2_j` (slot `cumN~g1/g2`, ẩn; độ đậm 0,55 / 0,3) đi trễ 0,025 / 0,05 s;
  chỉ tách ra khỏi thiên thạch khi quay nhanh. Lửa, vệt sáng thật là việc của VFX.
- **cast 2,4 s**: hoà từ idle vào đoạn hai tay xoa của skill_04 (họ: tay gần cuộn qua ngực, hai bàn tay vờn quanh nhau, chu kỳ ~0,6 s);
  lấy 1,00 → 2,20 s của họ (hai vòng, đầu và cuối tay xa gần chỗ idle) chạy nhanh 1,6 lần trong 0,30 → 1,05 s, thêm miết ngược chiều
  cẳng / bàn 3 lần/giây. Đoạn 0 → 0,69 s của họ bỏ (tay xa buông xuống đất, nén vào 0,3 s thì góc nhảy 50°/khung). Thiên thạch quay
  thêm 3 vòng (0,25 → 2,05, khép tròn vòng), xoáy về điểm ngay trước đôi tay (0,80 → 1,05), lần lượt lao vào đối thủ 1,05 → 1,37
  (bản sao trên far / fly_j), mọc lại 1,85. Gầm và hất người theo mỗi lần phóng.
- **skill 3,3 s QUẢ CẦU THIÊN THẠCH**: cuộn người (thân rụt, lăn tới, tay co, đuôi cuộp) → 0,32 s đổi sang quả cầu gai `bong.png` (Magnific,
  đường kính 1,35 × bán trục quỹ đạo; thân ẩn) → quay tại chỗ, thiên thạch quấn sát quả cầu quay thêm 7 vòng có vệt (0,30 → 2,75) →
  vọt lên 1,35 cao (1,00 → 1,36) → lao chéo xuống nện ngay đối thủ (1,70; lao 0,62 cao), kéo dài theo hướng rơi, bẹp dí lúc nện, thiên
  thạch nổ tung ra 1,9 lần quỹ đạo → nảy về giữa không trung, bung người (2,02 → 2,22) → đáp 2,50, gầm. Quả cầu: xương `bong` (kéo / bẹp,
  không xoay) → `bong_q` (lăn −7 vòng); bẹp trên xương đang xoay thì méo xiên theo góc lăn. Sự kiện cho VFX: `cuon` (bụi che lúc đổi
  hình), `bay_len`, `lua` (lửa xé gió lúc lao), `no_lon` (NỔ RẤT LỚN), `bung`, `cham_dat`. Va chạm skill (0,30 khựng, 2,4 rung, 0,26 bật,
  chớp #fff3d0a0).
- die: thiên thạch rơi theo phương thẳng đứng thế giới (đổi về hệ all2 đang lật) rồi mờ hết.
- Runtime Atomik nội suy góc theo giá trị thô (Sample1) nên quay nhiều vòng không bị cắt; chỗ trộn đổi clip (Mix, LerpAngle) thì vòng
  thêm đã khép bội 360°. Đo `kiem`: hết góc nhảy ở cast; attack, die còn như lượt 2. Runtime Spine thật: khớp bản Python.
  `.atomik` 495 KB (dưới trần 0,7 MB; đích 0,4 MB), 125 xương, 39 slot.

## 3f. Vào game (người dùng 2026-11-17 xem lượt 3: "ok cho vào game")

- Suất `cu_phu` (ải 60 "Lò Gốm Đất Nung", mini boss; giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ; không đổi bản lưu):
  `quai/doi_tinh_hach.py` (heroes.json, cards.json), `doi_tinh_hach.py chep` → `Assets/03 Art/Heroes/Resources/tinh_hach_1/`.
  Tên Claude đặt (người dùng đổi được): Cự Phủ → **Thiên Thạch Thú** "Quái thú lưng rừng tinh thể", dòng "Dòng Thiên Thạch Thú"; hai dạng
  như cũ, chưa có rig dạng 1 nên cả hai trỏ tinh_hach_1 (cỡ 0,92 / 1,1). Thẻ: Rìu Lửa → Thiên Thạch Xoáy (rock), Cự Phủ Khai Thiên →
  Quả Cầu Thiên Thạch (crack), Lửa Chiến → Rừng Tinh Thể (star). Bỏ hẳn Resources/cu_phu_1, cu_phu_2 sau khi gắn dạng mới.
- **Rig sửa trước khi vào game**: game xoay, giãn cả quỹ đạo xương `move` của clip lao cho điểm XA NHẤT (trung bình 5 khung) trỏ vào
  72 % quãng tới đối thủ (`AolaSticker.Lunge`). Chiêu cuối cũ dời `move` lên 1,35 cao ở đỉnh bay (xa hơn chỗ nện 0,62) → vào game quả
  cầu sẽ bay ngang vào đối thủ. Nay `move` chỉ mang cú lao ngang (xa nhất lúc nện), độ cao đặt trên xương con `all`.
- Hiệu ứng `Assets/01 Script/Game/Battle/HatThach.cs` (đường "n_", mốc rig × k = lead / giờ trúng): `n_thach_vo` (bụi, sỏi lúc bật vồ;
  vết cắn, dăm đá + mảnh tinh thể; hai nhịp xé), `n_thach_xoay` (tia lửa đá hổ phách / ngọc lam toé giữa hai bàn tay 0,30 → 1,05,
  chớp nhỏ theo nhịp miết; mảnh tinh thể hút về điểm xoáy; năm thiên thạch: lửa đuôi, tia, khói mỏng theo ĐÚNG đường bay bản sao của rig
  (S0_j → thân đối thủ, f = u², lệch ngang 0,05 sin); mỗi viên trúng: dăm đá, tinh thể, nổ lửa nhỏ, viên cuối to), `n_thach_cau` (bụi bung
  che lúc đổi hình; bụi, sỏi, tia ma sát lúc quay tại chỗ; đất phụt lúc vọt; LỬA XÉ GIÓ dày dần 50 → 160 lưỡi/giây ở nửa trước quả cầu,
  đuôi khói, vệt gió kem, than; NỔ RẤT LỚN: rung 0,9, chớp màn, lõi nổ 1,4 sau lưng đối thủ + nổ nhỏ phía trước, vành 20 lưỡi lửa, cột
  lửa 0,45 s, hai vòng sóng, vòng bụi, 12 đá + 10 tinh thể văng, 5 vết nứt toả, vành khói, nấm khói, hai nổ phụ 0,13 / 0,30; nảy về kéo
  than; đáp: vòng bụi). Tâm quả cầu theo giờ: bảng `ThtCau` (đo trên rig, bước 0,05 s: phần cú lao + tâm so với move).
- Nối: `HatNuoc.PlayNuoc` (3 case), `HatVoi.AtkLao` (`n_thach_vo`), `StageView.ThoFx` / `ThoAtk` (dòng `cu_phu`). Ba file đó do phiên
  Bùn Ngoạm đang sửa nên nhờ phiên đó chèn hộ.

## 4. Việc tiếp

1. ~~Người dùng chọn hướng~~ (D2).
2. Người dùng xem rig + clip lượt 3; VFX trên sân (tia đá giữa hai tay, vệt bay thiên thạch, nứt cụm, bụi đổi hình, lửa xé gió, nổ lớn, sóng xung kích), vào game (thay `cu_phu`?, tên, số
   dạng: hỏi).
2. Sửa concept theo lời người dùng → `L1_duyet.png` → nhóm mảnh → rig + clip → VFX → vào game (thay `cu_phu`, hỏi trước khi bỏ tướng cũ).
