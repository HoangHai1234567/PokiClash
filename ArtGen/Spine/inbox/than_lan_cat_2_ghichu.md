# Sa Tích DẠNG 2 (`than_lan_cat_2`): tướng ải 5 đảo Thổ (id game `lung_vuong`)

Bắt đầu 2026-11-17 (agent dạng 2, máy ổ C). Con gốc của rig: `monster_3530` (thằn lằn gai ngồi xổm, game tham khảo Sword x Staff; người dùng
chọn trong tờ `inbox/tho5_dang2_ung_vien.png`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó: dùng nội bộ, không đăng công khai.
Dạng 1: `than_lan_cat_ghichu.md` (rig 3257). Ghi chú chung: `tho5_ghichu.md`.

## 1. Concept

- Duyệt: `than_lan_cat_2/tai_ve/L1_duyet.png` (= L1_A; người dùng "ok concept 3 con kia ổn rồi làm đi" dù Claude chê dáng còn giống dạng 1:
  nằm rạp, to hơn khung rig, đầu lệch phải).
- **Concept nắn** (`than_lan_cat_2_manh.py tuthe` → `tai_ve/L2_tuthe.png`, Codex 1 ảnh, 170 s): vẽ lại ĐÚNG thiết kế L1_A trong ĐÚNG dáng,
  chỗ, cỡ của con gốc 3530 (ảnh 1 = `mau/goc_ca_con.png` chỉ lấy dáng). IoU hình bóng với con gốc **0,828**. Chỗ đổi so với L1_A (để lắp
  lưới): ngồi xổm thẳng lưng, bụng tròn thấp, hai tay buông trước bụng (mỗi tay một phiến giáp + ba vuốt nâu), hai chân sau gập ở đáy; mỗi
  gai vàng của họ thành một phiến đất nung (mũ trùm = 6 phiến lưng + 2 phiến cổ), hai sừng râu trên đầu thành hai phiến mào cao, mày trắng
  của họ thành mũ giáp đá kem. Thiết kế (đầu nêm mũ giáp, mắt vàng đồng tử dọc, da khaki, bụng kem, phiến đất nung viền kem) giữ y L1_A.

## 2. Mảnh (`than_lan_cat_2_manh.py`; gói `gui_gpt/than_lan_cat_2/luot_3_T1..T7.txt`)

Gen bằng `gen_magnific.py` (Magnific GPT 2.6, 1k high, **95 credit / ảnh**): T1–T6 song song (97–112 s mỗi tờ), T7 (95 s) = 7 ảnh, 665
credit. Ghép (`ghep`) IoU với concept nắn **0,962**.

| mảnh | slot của họ để gắn | tờ | ghi chú |
|---|---|---|---|
| `than` | hợp lưới tail3, tail2, tail1, chest3, chest2, chest1 | T1 | thân + cổ + bụng kem, không phiến |
| `dau` | cứng trên `all8` | T2 | đầu + mũ giáp đá (gộp mày mml/mmr của họ), KHÔNG mắt; `ham` tách ra (mục dưới) |
| `ham`, `long_mieng` | cứng trên xương mới `ham` | (tách) | `tach_ham`: vùng kem dưới đường miệng → hàm; đầu trên bỏ hàm theo từng cột + kẻ nét mực dọc chỗ cắt; lòng miệng nâu đỏ cùng hình hàm, dời lên 0,9 bề cao (nấp sau đầu khi ngậm) |
| `mat` / `mat_nham` | cứng trên `all8` | (cắt) | mắt mở cắt thẳng từ concept nắn; mắt nhắm dựng từ mặt nạ (tô da + nét mí); nhắm khi con ngươi họ (`beyes1`) đổi hình (hit, die, skill_02) + chớp ở idle |
| `duoi` | hợp tail4, weici1, weici2, weici3 | T2 | GPT vẽ dính một khối đùi + phiến → `duoi_sach` bỏ phần nằm sâu dưới chân gần (mặt nạ co 22 px) |
| `chan_xa` | hợp footr_1, footr_2, footr_3 (chân A của họ) | T2 | |
| `tay_gan` / `tay_xa` | hợp lhand_3..1 / handr_3..1 | T3 | mỗi tay một phiến giáp + ba vuốt |
| `chan_gan` | hợp footl_2, footl_1 (chân C của họ) | T4 | vuốt ở x 610–700 trùng chân C; chân lá B (footr_4) và D (footl_4, footl_3) của họ KHÔNG có mảnh |
| `p1..p6` | beici1..6 (một xương mỗi phiến: all28, 29, 30, 31, 26, 27) | T4–T7 | p3 (phiến tam giác đỉnh mũ) T3 vẽ nhầm thành bản sao mào cong → tờ riêng T7 tả rõ |
| `sl` / `sr` | chuỗi sừng râu jiaol (all33–35) / jiaor (all36–38) | T6 / T4 | hai phiến mào cao; vẽ SAU mũ giáp (gốc khuất dưới mũ), khác thứ tự của họ (sừng vẽ trước đầu) |
| `p4` | beici4 (all31) | T5 | phiến mào giữa |
| `pe1` / `pe2` | cứng trên all7 / all6 (slot mới) | T6 / T4 | hai phiến nằm trên cổ (concept nắn có, họ không có gai ở đó) |
| bỏ | `pc` (weici4: T6 vẽ lệch đè p4, phiến nhỏ gần như bị che), vạt miệng ya1..4, mày mml/mmr, con ngươi, vệt xoáy `xuanzhuan`, shadow | | |

Thứ tự vẽ (sau → trước): duoi, chan_xa, than, chan_gan, p3, p4, sl, sr, p2, p1, pe1, p5, pe2, p6, tay_xa, tay_gan, long_mieng, ham, dau, mat
(phiến dưới đè phiến trên như ngói, đúng concept; mào sau mũ giáp).

## 3. Rig (`than_lan_cat_2_rig.py` → `inbox/than_lan_cat_2/rig/`, không theo git)

Đủ xương của họ (FK; 8 IK đã nướng vào `l` của mẫu khung `<SXS>/scan/monster_3530/sample_goc.json`, 10 clip 30 khung/giây) + `move`, `day`,
`tam`, `ham` (bản lề góc miệng), `mieng` (chóp mõm), `far`, `fly_1..5`, `bay_1..5`. Gắn như dạng 1 (`trong_so_goc` + `lam_muot`: thân 10
vòng, chi 8, đuôi 5, mào 3), các hàm chép vào file (không import `than_lan_cat_rig`: import đó đặt lại trạng thái `hoa_ho` về con 3257).

**Hai bẫy của rig 3530 (đáng nhớ cho rig Sword x Staff khác):**
1. `all46`, `all49` (gốc hai tay) và `all8` (đầu) có **`inherit = 2` (NoRotationOrReflection)**: góc thế giới = góc riêng, không cộng góc cha.
   Khung của mình luôn cộng góc cha → lần đầu hai tay chĩa ngang ngang tầm đầu. Sửa `bu_ke_thua`: CUỐI mỗi khung cộng −(góc thế giới của
   cha) vào góc riêng ba xương này (mảnh gắn theo ma trận thế giới idle 0 của họ nên khớp khi góc thế giới khớp).
2. Cú vung tay của họ nhảy > 180° trong MỘT khung (skill_01 0,5 → 0,6, tay xa +234°): `np.unwrap` hiểu thành quay ngược, chuỗi góc kết thúc ở
   −363° (≡ −3°). Phát nguyên clip thì đúng, nhưng NHÂN hệ số (k) hay hoà dáng thì sai hẳn (tay kẹt trên đầu). Sửa: `dang()` đưa góc về
   (−180°, 180°] trước khi hoà; tay ở attack không nhân hệ số lên góc đã unwrap.

| clip | dài | nguồn | ý |
|---|---|---|---|
| appear | 1,60 | tự dựng + skill_02 0,17 | ẩn tới 0,10; rơi từ trên xuống ở dáng nhảy co người; ĐÁP 0,42 (bẹp nảy, phiến lạch cạch); dang hai tay gầm, há hàm, rung (0,90–1,22); về đứng |
| idle | 4,00 | khung 0 idle_01 + sóng | thở 2 %, cổ / đầu trễ 0,05 / 0,10 s, hàm hé theo thở, tay đung đưa trễ, sáu phiến nhấp nhô so le, mào chuỗi trễ dần, đuôi 4 s; trò 2,30–3,60: nghiêng đầu, MŨ TRÙM DỰNG PHIẾN lần lượt từ trên xuống rồi xếp lại lạch cạch, chớp mắt |
| walk | 0,667 | run_01 | + phiến nhấp nhô |
| attack | 1,00 | skill_01 (thân) + tự dựng (tay) | cúi lấy đà, lao tới (`move` 0,45 cao ở khung đớp) há hàm to, ĐỚP sập 0,52 (đầu thúc tới, duỗi 8 %), hai tay vươn lên trước rồi cào sập xuống theo đà, phiến lắc theo cú dừng |
| cast | 1,64 | tự dựng | thu người, tay co, mũ trùm dựng (0–0,40); hất: chúi tới, hai tay vung ra trước và lên, há hàm (0,52); NĂM PHIẾN rời lần lượt 0,46–0,62, xoay như phi tiêu bay tới `far` (code lái, farAim), găm, bay về lắp đúng chỗ (`ve` 1,12–1,28); giữ dáng hất rung |
| skill | 2,20 | tự dựng | giơ hai tay cao, ngả sau, mũ xoè, há hàm (0–0,50); ĐẬP 1 xuống đất phía trước (0,62); giơ lại; ĐẬP 2 sâu hơn (1,00 = trúng, lốc cát ở đối thủ); gù người rít rung, hàm há tới `het` 1,78; về |
| hit | 0,50 | hit_01 | + phiến bật ngược |
| die | 1,45 | die_01 | + năm phiến mũ trùm rời lần lượt (0,30–0,54), rơi theo trọng lực tới đất, nảy một lần, xoay; mờ |

Đo (`kiem`): idle, walk sạch; còn lại là cú bật có chủ ý (hit 0,07; đầu die; cú lao vồ của skill_01 ở attack 0,50 → 0,53 khoảng 3 khung;
hai cú đập của skill 40–57°/khung trong 2–3 khung; phiến bay) và chân lá B, D của họ (không có mảnh). Phóng to soi (walk 0,13 / 0,40,
skill 0,62 / 1,40, attack 0,13–0,57): thân, chân, tay, đuôi, đầu liền một bề mặt, không khe, chân gần / xa không lật dù xương đùi IK của
họ nhảy góc.

Xuất (2026-11-17, bản đầu; bản sau khi sửa vảy ở mục 6): `rig/than_lan_cat_2.atomik` 170 KB (73 xương, 25 slot, 26 hình, 1770 đỉnh, 8 clip, 23 sự kiện, atlas 592 × 680),
`xem.html`, `chan_dung.png`, tờ `khung_<clip>.png`; mọi clip nối về khung 0 idle 0,00 px; appear khung đầu trống, die khung cuối trống.
Game: `height` 700, `hitTimes` attack 0,52 / cast 0,672 / skill 1,00; stay cast + skill; far + farAim cast; muzzle (360, 281) = `mieng`.

## 4. Mốc cho VFX game (giây trong clip)

| clip | sự kiện |
|---|---|
| appear | `dap` 0,42 đáp đất (vòng bụi, bụi hai bên); `gam` 0,90 dang tay gầm |
| idle | `ru` 2,40 mũ trùm dựng phiến (không cần VFX) |
| attack | `lao` 0,38 bụi sau chân lúc phóng; `trung` 0,52 vết cắn + cát văng (dạng 1 dùng `n_tich_dop`, cùng giờ trúng ±0,04) |
| cast | `xoe` 0,05 cát bốc quanh mũ trùm (0,05–0,45); `phong` k=1..5 lúc 0,46 / 0,50 / 0,54 / 0,58 / 0,62; phiến tới đích sau BAY 0,20 → găm 0,66 / 0,70 / 0,74 / 0,78 / 0,82 (`trung` 0,672 = phiến đầu); phiến bay về từ 0,82 / 0,86 / 0,90 / 0,94 / 0,98, `ve` (lắp xong) 1,12 / 1,16 / 1,20 / 1,24 / 1,28 |
| skill | `tu` 0,08 cát xoáy quanh chân đối thủ; `dam` 0,62 (đập 1) và 1,00 (đập 2) sóng bụi + rung; `trung` 1,00 LỐC CÁT trùm đối thủ; `het` 1,78 lốc tan |
| die | `roi` 0,75 phiến chạm đất (bụi) |

Vị trí xương (đơn vị chiều cao dáng đứng; x về phía đối thủ, y lên; đo bằng `tho5_fx.Tuong`, như scratch `do_diem.py`):
- cast `all7` (gốc mũ trùm, chỗ cát bốc) t = 0,05 / 0,15 / 0,25 / 0,35 / 0,45: (0,101, 0,650), (0,085, 0,655), (0,065, 0,660), (0,052, 0,663),
  (0,140, 0,618); `mieng` lúc hất 0,56: (0,502, 0,438).
- cast chỗ phiến rời (`fly_k` lúc `phong`): 1 (0,101, 0,752), 2 (0,077, 0,667), 3 (−0,040, 0,657), 4 (−0,103, 0,519), 5 (−0,133, 0,401).
- attack `mieng` 0,38: (0,479, 0,306); lúc đớp 0,52: (0,829, 0,605) (trước khi game nắn quãng lao); tay gần `all48` lúc đớp (0,541, 0,417).
- skill tay gần `all48` lúc đập 0,62 / 1,00: (0,076, 0,410), (0,093, 0,416); tay xa `all51`: (0,424, 0,300), (0,419, 0,287) (gốc bàn tay;
  vuốt chạm đất thấp hơn chừng 0,25); `mieng` lúc gầm 1,00 / 1,40: (0,556, 0,253), (0,547, 0,286).

Bản xem trước: `tho5_fx_than_lan_cat2.py` (import `tho5_fx`, không sửa nó) → `inbox/tho5_fx/than_lan_cat2_{cast,skill,attack}.gif` + `_soi.png`:
cast năm cú găm dăm đất nung (cú cuối nặng hơn), skill hai cú đập + lốc cát cao 1,45 thân (trong game nhớ kẹp chiều cao như `NTichLoc`:
`Mathf.Min(…, foeFeet.y − 30)`), attack vết cắn + cát văng.

## 6. Sửa "vảy bay lơ lửng" (người dùng 2026-11-17, soi xem.html idle)

Người dùng: "phần vảy không gắn vào người mà bay lơ lửng, sửa lại đi" (ảnh: khe nền xám giữa gốc phiến mũ trùm và lưng / cổ, hai phiến
gần đầu cũng hở). Nguyên nhân: mỗi phiến GPT là một hình kín, gốc bo tròn ngắn (concept có nhiều lớp phiến hơn số gai của rig, các lớp
chồng kín nhau); thân GPT vẽ cổ hẹp, không có lưng dưới mũ trùm → ngay cả ảnh ghép tĩnh đã có khe.

Sửa (không gen thêm ảnh):
- **Lớp lưng** `lot` (`than_lan_cat_2_manh.py lot`): mảng da khaki phủ vùng GỐC các phiến tới lưng, cổ, gáy (hợp hình bảy phiến lưng / cổ co
  24 px, trong 170 px quanh thân + đầu, chui dưới gáy và lưng; không lấy ba phiến mào: giữa các mào là nền như concept), mép làm tròn
  (Gauss 16 px) như cái lưng gù, viền mực 5 px, vân sáp dựng bằng mã (`van_sap`: nét chéo ngắn sáng / tối, độ lệch đo trên mảnh thân). Rig
  vẽ ngay sau thân, trước mọi phiến, bám lưới chest3..1 (làm mịn 8 vòng): gốc phiến cắm lên lưng như vảy giáp, khe giữa phiến lộ da;
  phiến bay đi (cast) / rơi (die) thì lộ lưng gù.
- **Gốc đuôi** (soi thêm thấy hở ở hit): đuôi chỉ bám xương đuôi `tail4` (gai đuôi weici của họ quật 67°/khung ở hit, kéo vặn mảnh đuôi);
  `duoi_sach` giữ gốc đuôi chui sâu 55 px dưới chân gần, phần khuất tô da đuôi có vân (bỏ phiến, vành, nét mực của khối đùi thừa).
- Xuất lại: `rig/than_lan_cat_2.atomik` **187 KB** (73 xương, 26 slot, 27 hình, 2013 đỉnh, 8 clip; nối idle 0,00 px), GIF xem trước.
- Soi bằng **runtime Spine thật** (`mo_xe/chay.py sheet` trên bản xuất, 8 khung mỗi clip, cắt phóng vùng mũ trùm + gốc đuôi): idle (cả lúc
  dựng phiến 2,3–3,3), walk, attack, cast (phiến rời, bay, về lắp), skill (giơ, hai cú đập, gù rít), hit, die (phiến rơi), appear: không
  còn khe nền giữa phiến và thân. Ảnh trước / sau: `rig/_vay_truoc_sau.png`.

## 5. Còn lại / câu hỏi

1. Người dùng xem `rig/xem.html` và các GIF, sửa clip theo ý.
2. Clip `evolve` gộp dạng 1 (rig 3257) + dạng 2 (như `doi_tinh_sat.th`) và đưa vào game (Claude chính).
3. Hỏi: dáng nắn (ngồi thẳng lưng) có được không, vì khác L1_A đã duyệt (vốn nằm rạp)? Chiêu cuối dạng 2 đập hai lần rồi lốc cát cao hơn:
   đủ "mạnh hơn" chưa?
