# Sa Long DẠNG 1 (dạng non, `rong_cat_non`): tướng ải 15 đảo Thổ (id game `ho_khoan`)

Bắt đầu 2026-11-17 (agent dạng 1, máy ổ C). Người dùng: "làm thử dạng 1 của tướng thứ 4 đảo thổ" (gen qua Magnific, trần < 100 credit / ảnh),
chọn rig `monster_3529` (thằn lằn rồng gai bốn chân, game tham khảo Sword x Staff; tờ `inbox/tho5_salong_dang1_ung_vien.png`), duyệt
concept: "duyệt rồi mà làm ngay đi". Bản Sa Long hiện có (`rong_cat_1`, rig 3424, `rong_cat_ghichu.md`) thành DẠNG 2. Xương, lưới, chuyển
động gốc là của nhà phát hành game đó: dùng nội bộ, không đăng công khai. Ghi chú chung: `tho5_ghichu.md`.

## 1. Concept

`rong_cat_non/tai_ve/L1_duyet.png` (= L1_A, Magnific GPT 2.6, 95 credit, Claude chính gen; `tho5_dang2.py non_concept rong_cat`): rồng non
nâu bụi, mắt vàng, sừng mũi hổ phách nhỏ, hai sừng đá ngắn + phiến má sọc, cổ nâu sẫm, ngực bụng kem, ba phiến sa thạch sọc trên lưng, đuôi
dài sọc cong lên có hai phiến nhỏ. Đã vẽ theo dáng rig 3529 (bàn chân, hông, đầu, đuôi trùng chỗ con gốc; chỉ chùm gai mào và gai lưng lớn của
họ thành hai sừng ngắn + vài phiến nhỏ) nên KHÔNG cần concept nắn: mảnh cắt thẳng trên concept duyệt.

## 2. Mảnh (`rong_cat_non_manh.py`; gói `gui_gpt/rong_cat_non/luot_2_T1..T5.txt`)

Gen bằng `gen_magnific.py` (GPT 2.6, 1k high, **95 credit / tờ**), năm tờ song song (87–104 s mỗi tờ) = **5 ảnh, 475 credit**. Ghép (`ghep`)
IoU với concept **0,972**.

| mảnh | gắn vào (slot / xương của họ) | tờ | ghi chú |
|---|---|---|---|
| `than` | hợp lưới shenti_2, shenti_1, bozi_1 | T1 | thân + cổ + ngực bụng kem, không phiến, không chân, không đuôi |
| `dau` | (thay bằng `dau_tren` T6 + `ham` T7, mục 2b) | T2 | đầu + hai sừng + phiến má + sừng mũi hổ phách, KHÔNG mắt |
| `duoi` | weiba_2 | T2 | đuôi + vằn + hai phiến nhỏ trên đuôi |
| `chan_gan` | tui_1..3 + zhuazi_4..6 | T3 | chân sau gần (trái) |
| `tay_xa` | shou_4..6 + zhuazi_10..12 | T3 | chân trước xa (phải, sau thân). GPT cắt THẲNG đầu trên (không viền) → `vai` nối dài 80 px theo trục chân, đầu tròn, vân lấy từ giữa chân, viền mực hai bên (khi vung lên / duỗi tới không lộ mép cắt hở vai) |
| `tay_gan` | shou_1..3 + zhuazi_1..3 | T4 | chân trước gần (trước bụng) |
| `pa` / `pc` | cứng trên xương riêng `pl_a` / `pl_c` | T4 | phiến lưng sau cổ / phiến ở hông |
| `chan_xa` | tui_4..6 + zhuazi_7..9 | T5 | chân sau xa (nửa khuất) |
| `pb` | cứng trên `pl_b` | T5 | phiến lưng giữa |
| `mat` / `mat_nham` | cứng trên `bone6` | (cắt) | mắt mở cắt thẳng từ concept; mắt nhắm dựng từ mặt nạ (tô da + mí); nhắm khi mắt họ (`yanjing_0`) đổi sang hình `yanjing_0` (hit, die) + chớp ở idle |
| bỏ | 18 vảy / gai `linpian_*` (chùm gai mào, gai lưng, gai đuôi lớn), shadow | | |

Thứ tự vẽ (sau → trước): tay_xa, chan_xa, duoi, than, pc, pb, pa, chan_gan, tay_gan, dau, mat (chân xa sau thân như con gốc).

## 2b. Sửa khớp đầu–cổ + tách hàm (người dùng 2026-11-17, xem `rig/xem.html` dáng gầm: "đầu và thân bị ghép hở, sao bạn không tách hàm ra để há mồm được")

- **Lỗi**: đầu cứng trên `bone6`, cổ nằm trong lưới thân (bozi_1: bone5 / bone23); ngẩng đầu thì gáy + phiến má tách khỏi đỉnh cổ, lộ mép
  dưới đầu và khe (ảnh trước / sau: `rig/_truoc_sau_dau_ham.png`).
- **Hai tờ Magnific thêm** (95 + 95 = 190 credit): `T6` = đầu KHÔNG hàm dưới, không mắt, giữ hàng răng trên, không thịt dưới răng trên
  (`manh/dau_tren.png`); `T7` = hàm dưới riêng: hàm kem + răng dưới chĩa lên + dải lòng miệng đỏ nâu hẹp trên hàm (lòng miệng thuộc hàm
  dưới, phía trước giữa hai hàm để trống; memory "trong miệng không có thịt") (`manh/ham.png`). Mảnh `dau` cũ không dùng nữa.
- **Rig**: xương `ham` (bản lề góc miệng = đầu trái mảnh hàm, con `bone6`), hàm cứng trên `ham`, vẽ SAU đầu. Đầu bám LƯỚI hợp tou_1 + bozi_1
  của họ: mặt, mõm, sừng (ngoài vùng hoà) cứng theo bone6, gáy + phiến má dưới phía sau góc miệng (px x < 930 → 860, y 400 → 520) hoà dần
  sang trọng số lưới họ (cùng trọng số đỉnh cổ trong mảnh thân), làm mịn 4 vòng → đầu, cổ uốn cùng nhau. Mắt vẫn cứng bone6 (nằm ngoài
  vùng hoà).
- **Há miệng** (hàm quay xuống tối đa 32°): appear gầm 0,72–1,16 (há 1,05 + hàm rung), skill gồng gầm 0,72–1,38 (há 0,9–1,0 + rung), sập lúc
  nện 1,60, há vừa 0,55 lúc cột trồi; attack há dần tới 0,95 ngay trước cú vồ rồi SẬP đúng khung trúng 0,40; cast há 0,6 lúc quét; hit há
  nhẹ 0,35; die há 0,5; idle ngáp nhỏ một lần 1,20–1,95 (há 0,55, ngẩng 4°).
- Soi (`soi`, tỉ lệ 0,42–0,6): appear 0,85 / 1,0, skill 0,85 / 1,0 / 1,20 / 1,62 / 1,96, attack 0,30 / 0,36 / 0,40 / 0,50, idle 0 / 1,55,
  hit 0,10, die 0,60, cast 0,42: đầu–cổ liền ở mọi góc (cả dáng ngẩng lớn nhất), hàm bám bản lề, lòng miệng chỉ lộ khi há. `kiem`: không cú
  nhảy mới (hàm mở / sập ≤ 25° / khung).
- Xuất lại: `rig/rong_cat_non.atomik` **132 KB** (61 xương, 12 slot, 13 hình, 894 đỉnh, 8 clip, 14 sự kiện, atlas 488 × 552); mọi clip nối
  về khung 0 idle 0,00 px; GIF `tho5_fx/rong_cat_non_{cast,skill,attack}.gif` làm lại.
- (Vùng hoà và cách bám cổ ở trên đã đổi ở mục 2c.)

## 2c. Bỏ viền chỗ nối, da liền (người dùng 2026-11-17: "thân vẫn bị hở giữa thân và đầu, bỏ outline đoạn nối thân và đầu đi", "làm kĩ vào")

Ảnh trước / sau: `rig/_truoc_sau_noi_da.png` (walk 0 / 0,27 cả con + phóng to gáy và hông). Tờ soi tổng: `rig/_tu_soi.jpg` (runtime Spine
thật 4.2: concept cạnh idle 0, rồi 24 dáng cực trị của tám clip × năm chỗ nối đầu–cổ, hàm, vai, hông, gốc đuôi).

**Mảnh** (`rong_cat_non_manh.py noi_da`, chuẩn là concept duyệt; bản GPT gốc giữ ở `manh/<tên>_truoc_noi.png`):
- `noi_theo_concept`: ở mép mảnh nằm đè lên bộ phận khác mà concept không có nét ở đó thì xoá viền (nở theo vệt tối liền tới hết khử răng
  cưa, sợi mảnh < 4 px sát chỗ xoá bỏ nốt), tô bằng VÂN da chép từ sâu trong mảnh 12 px (không ra mảng trơn), chỉnh độ sáng theo da quanh đó,
  mép nối gần như đục (mờ 5–8 px), điểm sẫm trong dải mờ tô da (kẻo thành vệt đen loang).
- Đầu (`dau_tren`) và đỉnh cổ trong thân: chế độ `mat_trong` — chỉ bỏ viền ở mép QUAY VÀO (nhìn ra ngoài mép 6–12 px, concept ở đó là thân
  con vật); mép quay ra nền giữ: nét lưng cổ sau gáy, mép trước họng dưới hàm (x > 925, lúc nghỉ khuất sau hàm, khi đi / ngẩng thì lộ).
  Nét concept tính là mực khi lum < 62 (mảng bóng nâu sẫm ở gáy concept không phải nét). Góc phiến má giữ nguyên, gai mực sót ở đó tô da.
- Vai chân trước gần, đỉnh đùi chân sau gần: bỏ cung viền đè lên thân. Hông: concept có MỘT nét hông chạy từ phiến lưng xuống chân, đuôi
  mọc sau hông → giữ nét hông của thân, cắt phần đùi lồi qua nét đó (`cat_hong`, trên y 738), dưới đó mép sau cẳng chân giữ viền.
- Mảnh sau thân (chân xa, đuôi) giữ nguyên bản; đỉnh vai nối thêm của chân trước xa mờ dần trên y 636 (khi cổ hạ theo đầu ở walk đỉnh vai
  từng lú lên trên nét lưng cổ thành cục có viền).

**Rig** (`rong_cat_non_rig.py`):
- Phần cổ trong mảnh thân bám xương đầu theo KHOẢNG CÁCH tới hình bóng đầu (0,85 trong hình, về 0 cách 75 px) và tới hàm dưới (32 px: hàm
  thấp sát ngực, kéo rộng thì ngực + vai chân xa bị lôi theo) — một thước dọc cổ cho cả gáy lẫn họng nên cổ giãn đều như ống khi lao / ngẩng /
  cúi: không xiên lệch, không hở khe nền ở gáy (trước đó attack 0,40 hở nêm nền giữa phiến mang tai và lưng cổ). Làm mịn 3 vòng sau khi hoà.
- Đầu gần như cứng `bone6` (vùng hoà chỉ y 500–560 sau góc miệng): phiến mang tai không còn bị kéo xiên thành sợi lúc lao tới.

**Bảng soi (runtime thật, phóng to, idle + dáng cực trị mọi clip):**

| # | mục | kết quả |
|---|---|---|
| 1 | chỗ nối cùng khối da (đầu–cổ, cổ–thân, vai, hông, gốc đuôi) không viền trong, không khe nền | ĐẠT sau sửa: bỏ viền đáy gáy + đỉnh cổ, cung vai, cung đùi; cổ bám đầu theo khoảng cách (hết nêm hở ở attack 0,40, walk 0,27); gốc đuôi là nét hông như concept (không phải viền nối) |
| 2 | phiến lưng / vảy / sừng cắm vào thân | ĐẠT: ba phiến cứng trên `pl_*` (con xương thân nặng nhất ở gốc), vẽ trước thân, chân phiến luôn đè lên lưng ở mọi dáng soi (cả die nằm); sừng thuộc mảnh đầu |
| 3 | thứ tự lớp theo concept | ĐẠT: chân trước xa, chân sau xa, đuôi sau thân; phiến, chân sau gần, chân trước gần trước thân; hàm sau đầu; mắt trên cùng; nét hông đè gốc đuôi như concept |
| 4 | vật mọc từ lỗ (hai lớp vành) | không có trong con này; lòng miệng thuộc hàm dưới, trước hai hàm để trống |
| 5 | không lộ mép cắt, không lỗ nền trong mảnh | ĐẠT sau sửa: cục vai xa (mờ đỉnh vai), đùi lồi qua hông (cắt), vệt đen ở đầu mút viền gáy, gai mực + đốm kem ở góc phiến má, mép họng không viền dưới hàm (giữ viền). Còn: hai đốm sáng 2–3 px ở đầu hai nét chân trước gần, vân tô ở đỉnh vai / đùi hơi sọc khi phóng 4 × |
| 6 | hàm mở đúng nhịp, lòng miệng thuộc hàm dưới | ĐẠT (mục 2b): appear / skill gầm, attack há trước cú vồ sập đúng 0,40, cast 0,6, hit 0,35, die 0,5, idle ngáp 1,20–1,95 |
| 7 | góc nhảy 360°, bước dời ở 60 khung/giây (`mo_xe/chay.py sample … 60` trên rig đã xuất) | ĐẠT: không xương nào quay ≥ 300° trong 0,3 s (không quay ngược vòng). Bước lớn nhất là cú vồ / quét của clip gốc: attack 0,37–0,40 đầu dời 0,52 + 0,49 cao / khung (hai khung), vuốt xa 56° / khung; cast 0,27 cao / khung; skill 41°; die 50° (chân IK của họ). idle ≤ 7° và 0,013 cao |
| 8 | idle không đơn điệu, đòn có lực | ĐẠT (giữ như trước): idle thở + cổ trễ + phiến so le + đuôi trễ, chớp mắt, ngáp há hàm, trò vẫy đuôi tíu tít + nghiêng đầu tò mò; attack ngửa lấy đà – vồ – bẹp 7 % – phiến lắc; skill chồm gồng rung – nện bẹp nảy |

Xuất (2026-11-17 chiều): `rig/rong_cat_non.atomik` **132 KB** (61 xương, 12 slot, 890 đỉnh, 1277 tam giác, 8 clip, atlas 488 × 552), `json`,
`xem.html`, `chan_dung.png`, `khung_<clip>.png`; mọi clip nối về khung 0 idle 0,00 px. GIF `tho5_fx/rong_cat_non_{cast,skill,attack}.gif`
làm lại. Không gen ảnh mới (vẫn 760 credit).

## 3. Rig (`rong_cat_non_rig.py` → `inbox/rong_cat_non/rig/`, không theo git)

Đủ xương của họ (FK; 4 IK đã nướng vào `l` của mẫu khung `<SXS>/scan/monster_3529/sample_goc.json`, 14 clip 30 khung/giây) + `move`, `day`,
`tam`, `mieng` (đầu vuốt trước gần, con của `bone2`: chỗ phóng lưỡi cát), `vuot_xa` (đầu vuốt trước xa, con của `bone44`), `pl_a` (con
`shenti_2`), `pl_b`, `pl_c` (con `bone18`) — cha của phiến chọn theo xương có trọng số lớn nhất của lưới thân ở gốc phiến. Gắn như Sa Tích
dạng 2 (`trong_so_goc` + `lam_muot`: thân 10 vòng, chi 8, đuôi 6).

**Bẫy của rig 3529 (đáng nhớ cho rig Sword x Staff khác):**
1. **Mười một** xương `inherit = 2` (NoRotationOrReflection) xếp thành CHUỖI: cổ đầu `bone4 → bone5 → bone23 → bone6`, đuôi `bone19 → bone20
   → bone21 → bone22 → bone40`, gai đuôi `bone31`, `bone32`. Bù cuối mỗi khung LẦN LƯỢT từ cha xuống con (mỗi xương tính lại thế giới sau
   khi cha đã bù), không bù một lượt như rig 3530 (chỉ ba xương lẻ).
2. **Góc cha phải mở gói**: góc thế giới cha lấy bằng `atan2` (gói ±180°) làm góc riêng của xương bù NHẢY 360° giữa hai khung khi đuôi đi
   qua 180° (walk 0,60). Hàm dựng khung vẫn đúng nhưng khoá nướng nội suy xuyên qua cú nhảy 360° → đuôi lật một khung (soi tờ khung tĩnh
   không thấy, `kiem` thấy 46–57°/khung). Sửa: lấy góc từ ma trận rồi đưa về gần TỔNG góc riêng dọc chuỗi cha (`goc_tong`).

| clip | dài | nguồn | ý |
|---|---|---|---|
| appear | 1,60 | tự dựng + dáng skill_01_02 0,55 + skill_03 0,75 | ẩn tới 0,10; rơi từ trên xuống co tay; ĐÁP 0,40 (bẹp nảy, phiến lạch cạch); ngẩng đầu chéo lên trời gầm (dáng gốc ngửa 92°, bù −62° còn ~45°), rung (0,72–1,16), đuôi quẫy; về đứng |
| idle | 4,00 | khung 0 idle_01 + sóng | thở 2 %, cổ / đầu trễ 0,05 / 0,08 / 0,12 s, ba phiến nhấp nhô so le, đuôi 4 s trễ dần ra ngọn; chớp mắt 0,90; trò 2,20–3,30: VẪY ĐUÔI tíu tít 4 Hz (ngọn trễ, biên độ lớn dần), nghiêng đầu tò mò 9°, nhún theo nhịp vẫy, phiến rung, chớp mắt |
| walk | 0,80 | run_01 | + phiến nhấp nhô |
| attack | 1,00 | skill_01_01 | ngửa lấy đà, giơ vuốt xa (0–0,37), VỒ CHÉM 0,40 (= trúng; `move` lao 0,48 cao ở khung trúng, game nắn quãng), bẹp 7 %, phiến lắc theo cú dừng, về |
| cast | 1,15 | skill_01_03 + giữ dáng | co vuốt gần lấy đà (0–0,37), QUÉT CHÉM xuống 0,40 (chem1 = trúng), chem2 0,47; giữ dáng quét rung nhỏ dần tới 0,80; về |
| skill | 2,30 | skill_03 + giữ dáng | thu người (0–0,5); CHỒM ĐỨNG giơ vuốt xa gồng 0,60–1,40 (đầu gốc ngửa ~90°, bù −35° còn ~55°; rung hai dáng); GIÁNG xuống NỆN 1,60 (đầu cúi −30°, bẹp nảy, phiến lạch cạch); cột 1 1,76, cột 2 1,96 (= trúng) rung nhẹ; giữ dáng nện tới 2,02; về |
| hit | 0,50 | hit_01 | + phiến bật ngược; mắt nhắm theo họ |
| die | 1,45 | die_01 + mờ 0,45 s | ngã nằm (chân sau xa lật IK như con gốc ở 0,47–0,50) |

Đo (`kiem`): idle, walk, hit sạch; còn lại là cú nhảy có chủ ý của clip gốc: attack 0,40 (cú vồ: cổ 90°, đầu 44° trong một khung), cast
0,40 (cú quét: đầu dời 0,52 cao / khung), skill 0,60 (cú chồm đứng: đầu 80°), appear 0,10 (hiện ra) / 0,40 (đáp), die (chân IK của họ).
Phóng to soi attack 0,18–0,73 (vai chân trước xa liền ngực cả khi vung lên lẫn duỗi tới, sau khi nối vai), skill 0,75–2,02, appear 0,30–1,40,
cast 0,21–0,60, walk 0,53–0,70 (đuôi liền sau khi sửa mở gói), die, hit: thân, chân, đuôi, đầu liền, không khe.

Xuất (2026-11-17): `rig/rong_cat_non.atomik` **124 KB** (60 xương, 11 slot, 12 hình, 656 đỉnh, 8 clip, 14 sự kiện, atlas 480 × 520),
`xem.html`, `chan_dung.png`, tờ `khung_<clip>.png`; mọi clip nối về khung 0 idle 0,00 px; appear khung đầu trống, die khung cuối trống.
Game: `height` 633, `hitTimes` attack 0,40 / cast 0,40 / skill 1,96; stay cast + skill; không far; attack lao (mặc định).

## 4. Mốc cho VFX game (giây trong clip)

| clip | sự kiện |
|---|---|
| appear | `dap` 0,40 đáp đất (vòng bụi, bụi hai bên); `gam` 0,72 ngẩng đầu gầm |
| idle | `vay` 2,25 vẫy đuôi (không cần VFX) |
| attack | `lao` 0,30 bụi sau chân lúc bật; `trung` 0,40 ba vệt vuốt + cát văng (như `n_long_vuot`, khung trúng 0,40 thay 0,54) |
| cast | `chem1` 0,40 (= `trung`), `chem2` 0,47: mỗi nhát một lưỡi cát nhỏ rời `mieng` bay tới đối thủ (~0,22 s); dạng 2 có ba lưỡi (0,70 / 0,76 / 0,84) |
| skill | `gong` 0,60 cát hút về `vuot_xa` (tới ~1,50); `nen` 1,60 vòng bụi + vết nứt chạy tới đối thủ; `cot1` 1,76 cột nhỏ; `cot2` 1,96 = trúng, cột vừa (dạng 2: ba cột, cột cuối to ở 1,82) |
| die | `nga` 0,70 chạm đất (bụi) |

Vị trí xương (đơn vị chiều cao dáng đứng 633; x về phía đối thủ tính từ giữa hộp idle, y lên tính từ đáy; đo `rong_cat_non_rig.py diem`):
- cast `mieng` t = 0,30 / 0,40 / 0,47 / 0,55: (−0,075, 0,327), (0,088, −0,090), (0,090, −0,025), (0,091, −0,042) (vuốt gần quét xuống sát đất
  ngay trước ngực: lưỡi cát nên rời ở (0,09, 0,0) và bay lên tới thân đối thủ).
- attack lúc trúng 0,40 (trước khi game nắn quãng lao): `mieng` (0,565, 0,013), `vuot_xa` (1,155, 0,036), đầu `bone6` (1,095, 0,470).
- skill `vuot_xa` t = 0,60 … 1,40 bước 0,1: (0,426, 0,166), (0,460, 0,170), (0,469, 0,211), (0,472, 0,235), (0,472, 0,256), (0,472, 0,274),
  (0,473, 0,289), (0,476, 0,295), (0,500, 0,249); lúc nện 1,60: (0,500, 0,055); cột 1,76 / 1,96: (0,491, 0,045), (0,495, 0,044).

Bản xem trước: `tho5_fx_rong_cat_non.py` (import `tho5_fx`, không sửa nó) → `inbox/tho5_fx/rong_cat_non_{cast,skill,attack}.gif` + `_soi.png`:
cast hai lưỡi cát nhỏ găm; skill cát hút về vuốt, nện đất (vòng bụi + vết nứt), hai cột sa thạch (cột cuối vừa); attack ba vệt vuốt + cát văng.
Trong bản xem trước cột nằm lớp SAU đối thủ nên bị con slime to che gần hết (như dạng 2); hiệu ứng game của dạng 2 đã nâng cột cuối lên 1,45 ×
đối thủ và dời cột nhỏ ra hai bên (HatTho.cs) — dạng 1 nên theo cùng cách, cỡ nhỏ hơn.

## 5. Ảnh và credit

Magnific: concept 1 ảnh (95, Claude chính) + năm tờ mảnh (475) + hai tờ đầu / hàm (190) = **8 ảnh, 760 credit**. Không dùng Codex.

## 6. Còn lại / câu hỏi

1. Người dùng xem `rig/xem.html` và các GIF, sửa clip theo ý.
2. Clip `evolve` gộp dạng 1 (rig 3529) + dạng 2 (`rong_cat_1`, rig 3424) như `doi_tinh_sat.th`, mã hiệu ứng game theo dạng (bảng ThoFx thành
   mảng theo dạng như KimFx), sửa `doi_tho5.py` (dạng 1 → `rong_cat_non`) và đưa vào game (Claude chính).
3. Vai chân trước xa là phần nối thêm (vân lát lại từ giữa chân, không phải nét GPT), nay mờ dần trên y 636: chỉ lộ khi vung chân lên ở
   attack; nếu nhìn thấy khác màu hoặc hở vai thì gen lại tờ T3 dặn rõ "vẽ dài phần vai khuất sau ngực".
5. Cú vồ attack 0,37–0,40 (đầu đi ~1 chiều cao trong 2 khung 60 fps) giữ đúng nhịp clip gốc skill_01_01; nếu người dùng thấy như "giật cảnh"
   thì nới thành 3–4 khung (tmap quanh 0,36–0,40).
4. Hỏi người dùng: dáng gầm và dáng chồm gồng đã bù cho đầu ngửa chéo ~45–55° (gốc 90° trông như ngửa hẳn ra sau): được chưa? Chiêu mana chỉ
   hai lưỡi cát nhỏ, chiêu cuối hai cột (cột cuối vừa): đủ "nhẹ hơn dạng 2 nhưng vẫn có lực" chưa?
