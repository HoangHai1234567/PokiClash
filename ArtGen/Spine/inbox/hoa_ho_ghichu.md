# Hổ lửa (`hoa_ho`): tướng thứ 9 đảo Hỏa

Bắt đầu 2026-11-14 (máy ổ D). Con gốc của rig: `monster_3645` (bạch hổ bờm mây đỏ đen, sừng, chuông đồng; game tham khảo, kho
`D:\RefAnimation\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `idle_01`). Xương, lưới, chuyển động gốc là của nhà phát hành
game đó (như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình. Suất 9 đảo Hỏa = ải 60 ("Hang Hồng Ngọc", `IslandGen.Plan Hoa`),
id game **`hoa_tinh`** (đang là Tiểu Hỏa Tinh / Hỏa Tinh, `hoa_tinh_1`, `hoa_tinh_2`). Mã làm việc `hoa_ho` (id `ho_lua` đã có tướng khác dùng).
Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-14)

- "tướng thứ 9 đảo hỏa; concept **hổ lửa**, bạn **phải giữ được kiểu style của nó như này** (phần **mây xung quanh đổi sang kiểu mây đỏ lửa hoặc
  làm lại như họ**), **bỏ sừng** đi, **bỏ chuông ở dưới** đi".
- "**idle / walk làm giống họ**, **appear làm nó nhảy vào sàn**".
- Đánh thường: "làm **gần giống skill_01_1, vả đối thủ**".
- Chiêu mana: "làm giống **skill 3**: **gồng người, ngửa đầu nhẹ hét to, impact cực lớn**, tạo **sóng xung kích cùng sóng nhiệt**".
- Chiêu cuối: "làm giống **skill_04**, **bật nhanh rồi biến mất**, làm **hiệu ứng âm bản màn chơi**, hổ **đánh liên tục (kiểu bay qua gây dam như
  chém) tầm 10–15 chiêu** sau đó **về vị trí ban đầu**, các nhát đánh **để lại lửa cháy tạo thành vụ nổ** ở đối thủ".

Cách hiểu của Claude (đã báo người dùng): "chuông ở dưới" = cả cái chuông đồng lớn ôm ngực (vẽ sẵn trong ảnh thân `P_shenti_01`) lẫn khuyên sắt
`P_tiehuan` + chuông nhỏ `P_lingdang` treo dưới bụng. Vòng đồng ở bốn cổ chân (`jiaphuan_*`) GIỮ (đổi màu, kiểu).

## 2. Mổ rig gốc (`<SXS>/scan/monster_3645/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample.json` 13 clip 30 khung/giây, `khung/`, `mo/`, `parts/`)

197 xương, 77 slot (75 hình, mỗi slot một hình), 13 clip, 22 035 khoá. Con **nhìn sang PHẢI**. Ảnh atlas 0,501 px / đơn vị rig; dáng idle
x −660..655, y −30..1020. Script mổ: `hoa_ho.py` (`mo`, `nhom`, `part_goc`).

Ràng buộc (đều đã nướng thành FK qua mẫu khung `l`): 8 IK chân (`L1..L4`, `R1..R4`; mix đổi theo clip), 2 transform (`bone2`, `bone14`: dời theo
90 %), không path, không physics. Một xương `bone40` (con của `bone9`, mang mây đuôi `P_maofa_24`) không thừa hưởng xoay của cha (inherit 2): rig
mình tính góc riêng từ ma trận thế giới. Không xương nào xô lệch. Gốc không trôi (`all`, `all2` đứng yên; thân dời ở `bone`).

Bảng nhóm part (thứ tự vẽ sau → trước; số = thứ tự slot):
| nhóm | slot | là gì |
|---|---|---|
| chân sau xa | 2–5 `P_L_hou*` + vòng `jiaphuan_06` (6) | ống, bàn (liền 4 móng), cổ chân, đùi |
| mây ngực | 7 `P_maofa_21`, 18 `P_maofa_20` | dải lửa răng cưa dọc mép trước ngực |
| chân trước xa | 8–10 `P_L_xiaotui`, `P_L_jiao`, `P_L_datui` + vòng `jiaphuan_01` (11) + mây nhỏ `P_maofa_02` (12) | cái chân DUỖI về phải; **chính chân này VẢ ở `skill_01_1`** |
| đuôi | 14 `P_weiba_02` (đoạn gốc, có mảnh xương vẽ sẵn), 15 `P_weiba_01` (đoạn ngọn + chổi lông); mây đuôi 13, 16, 17 (`P_maofa_23_01`, `_24`, `_23`) | |
| thân | 20 `P_tun` (mông), 21 `P_shenti_01` (ngực + bụng, lưới 33 đỉnh; **chuông đồng vẽ sẵn trong ảnh**) | |
| chân sau gần | 23–25 + vòng `jiaphuan_05` (22), `jiaphuan_02` (26) + bàn `P_R_houjiaozhang` (27) + 4 ngón rời (28–31) | |
| khuyên + chuông | 32 `P_tiehuan`, 33 `P_lingdang` | BỎ |
| chân trước gần | 35 `P_R_datui`, 37 `P_R_xiaotui`, 39 `P_R_jiao` + vòng 36, 38 + 4 ngón rời (40–43) | bàn to nhất, giữa tiền cảnh |
| mây bờm | 44–53 (`P_maofa_05..16`), 63 `_12`, 67 `_07` | ~12 cụm mây chồng như ngói, mỗi cụm một chuỗi xương riêng |
| mây hông | 19 `_19`, 34 `_17`, 75 `_22` (cụm móc đen viền đỏ trên hông), 76 `_01` | |
| đầu | 54 tai xa, 55 `P_zui_01`, 56 + 61 hai nanh (`liaoya`), 57 `P_zui` (hàm dưới + râu cằm), 58–59 răng, 60 + 64 râu xoắn, 62 `P_tou`, 65 `P_biyan` (mắt nhắm, ẩn), 66 `P_yanjing`, 68 + 70 hai chỏm lông xoăn trán (`P_maofa_04`, `_03`), 69 `P_jiao` (SỪNG, BỎ), 71 tai gần, 72–74 ba mảnh mày (`P_meimao`) | |

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho |
|---|---|---|---|
| `idle_01` | 4,00 | thở, mây bờm bay, đuôi lượn | **idle** (như họ) |
| `run_01` | 1,13 | chạy tại chỗ | **walk** (như họ) |
| `skill_01_1/2/3` | 1,13 | giơ chân trước XA 0,10–0,33; vả xuống 0,36–0,42 (bàn chân thọc xuống dưới mặt đất); giữ tới 0,9; về | **attack** |
| `skill_02` | 1,77 | (chưa dùng; có đổi thứ tự vẽ) | |
| `skill_03` | 2,00 | thu người thấp 0,18–0,36; vươn lên ngửa đầu gầm 0,55–1,45; về | **cast** |
| `skill_04` | 1,90 | thu người 0–0,35; bật tới, mờ hết 0,47–0,53; vắng 0,53–0,93; hiện lại 0,93–1,03 đang vồ duỗi dài trên không; đáp 1,2; đứng dậy | **skill**; đoạn 0,97 → 1,9 làm **appear** |
| `hit_01/02`, `block_01`, `stun_01` | | giật lùi, nhắm mắt (`P_biyan`) | **hit** = hit_01 |
| `die_01` | 1,00 | đổ; đổi thứ tự vẽ ở khung 17 (chưa xử lý) | **die** + tan 0,45 |

## 3. Concept (đề xuất của Claude, CHỜ người dùng chọn)

Script: `hoa_ho_bo_cuc.py` (sơ đồ bố cục 1536 × 1024 ở khung 0 idle, 0,872 px / đơn vị rig, gốc rig ở (774,1; 948,7); đã bỏ sừng, khuyên, chuông;
thân tô một màu lông), `build_hoa_ho.py` (gói `gui_gpt/hoa_ho_1/`; ảnh mẫu: sơ đồ, Viêm Đao, Giác Mộc, bản đồ).

Giữ của con gốc: dáng hổ lớn bốn chân nhìn phải, chân trước xa duỗi, đuôi cuộn chữ S, bờm là ~12 cụm MÂY bay sang trái, mây trên hông và đuôi, hai
nanh kiếm, vệt xoắn trên má, vòng hở quanh cổ chân. Đổi: mây đỏ đen chuyển màu → **mây lửa** (mây cổ kiểu Á Đông lai ngọn lửa: đầu xoắn, lưỡi nhọn
cong, tô DẢI MÀU PHẲNG); chỏm lông xoăn trán → chỏm lửa nhỏ; vằn zíc zắc → vằn hình lưỡi lửa; chổi đuôi → hình ngọn lửa; bỏ sừng, chuông, mảnh
xương quấn đuôi.

Ba hướng màu:
- `bach` **A · bạch hổ mây lửa**: lông trắng kem, vằn than, mây đỏ son + dải cam + xoáy vàng, vòng chân vàng đồng (gần con gốc nhất).
- `cam` **B · hổ cam**: lông cam vằn đen, mõm / ngực / bàn chân kem, mây đỏ thẫm viền vàng, vòng chân sắt đen.
- `than` **C · hổ than**: lông xám than, vằn cam than hồng, mây cam lõi vàng, vòng chân đỏ son.

Ảnh về `inbox/hoa_ho_1/tai_ve/L1_<hướng>.png`.

## 4. Rig thử trên DA GỐC (làm trong lúc chờ concept; không phụ thuộc màu)

`HH_GOC=1 py -3 -I hoa_ho_rig.py` → `inbox/hoa_ho_1/rig_goc/` (`xem.html`, `khung_<clip>.png`, `.atomik` 475 KB): 200 xương (197 của họ + root, move,
mieng, vuot), 72 slot, 1148 đỉnh; chiều cao thân 930 (không tính đuôi, chỏm trán). Mỗi slot dùng NGUYÊN lưới của họ. Chỉ để soi clip trong máy,
KHÔNG đưa vào game.

Clip (8), đều là co giãn giờ MỘT clip nguồn (nội suy mẫu `l`) + kênh riêng trên `move`:
- `idle` 4,0 s = idle_01; `walk` 1,13 s = run_01; `hit` 0,5 s = hit_01; `die` 1,45 s = die_01 + tan.
- `attack` 1,20 s = skill_01_1: giơ chân 0–0,30; GHÌM 0,30–0,44; vả 0,44–0,52 (`va` = `trung` 0,50); khựng, dộng thân; về.
- `cast` 2,10 s = skill_03: gồng thấp 0–0,42 (`tu` 0,20); vươn lên ngửa đầu gầm 0,70 (`gam`, `trung` 0,74); giữ rung tới 1,45 (`het_gam`); về.
- `skill` 3,03 s = skill_04: thu người 0–0,36; bật tới 0,55 chiều cao và tan 0,36–0,52 (`bien_mat`); 12 lượt lướt 0,62–1,94 (mỗi lượt 0,11 s: dáng
  vồ duỗi dài τ 1,04, hiện ~0,07 s quanh điểm 1,55 chiều cao trước mặt, lượt lẻ lật ngang lướt ngược lại; sự kiện `chem` × 12); hiện lại ở chỗ
  cũ 2,10 (`hien`) bằng đoạn đáp của họ; `no` = `trung` 2,40.
- `appear` 0,93 s = đoạn đáp của skill_04 (τ 0,97 → 1,9): nhảy từ sau 0,85 chiều cao vào, hiện dần 0,14 s; `dap_dat` 0,27.

Nối: appear, attack, cast, skill, hit về idle 0,00 px; idle khép vòng 1,1 px; walk 6,3 px (bước thường 63).

## 5. Việc tiếp (sau khi người dùng chọn concept)

1. Mảnh: thân + mông + các khúc bốn chân = tờ "thân liền" (gen liền rồi nướng vào khung part); mây, vòng, tai, nanh, mày, đầu = tờ khung part
   (hình bóng kín tô phẳng, IoU ≥ 0,9); thân KHÔNG còn chuông.
2. Rig da mình (`hoa_ho_rig.py` không đặt `HH_GOC`), soi runtime thật, `die_01` đổi thứ tự vẽ (slot sinh đôi).
3. VFX (C#, ngoài rig): vệt vuốt + chớp ở đòn vả; sóng xung kích + sóng nhiệt ở `gam`; chiêu cuối: ÂM BẢN màn chơi (người dùng yêu cầu: cần
   shader / lớp phủ mới ở `StageView`), vệt chém theo từng `chem`, lửa cháy lại ở đối thủ, vụ nổ lúc `no`.
4. Vào game: thư mục Resources mới, `heroes.json` khối `hoa_tinh` (không đè `hoa_tinh_1/2` cũ), tên, số dạng, thẻ: hỏi người dùng.

## 3b. Lượt concept 1 đã về (2026-11-14 02:59)

`tai_ve/L1_bach.png` (126 s), `L1_cam.png` (93 s), `L1_than.png` (96 s): cả ba bám sơ đồ ngay lượt đầu (đầu, bờm mây, đuôi, bốn vòng đúng chỗ),
không sừng, không chuông, mây tô dải phẳng. Trang so `inbox/hoa_ho_xem_concept.html`. Nhận xét của Claude: A giữ đúng tinh thần con gốc nhất và
mây lửa nổi nhất trên lông trắng; B đẹp nhưng cam trên cam nên mây chìm vào thân, lại gần dòng hổ đảo Thổ (Hổ Khoan, Hổ Kim Cương); C dữ nhất, hợp "hổ lửa"
nhưng xa con gốc. Cả ba: chân sau xa gần như khuất; A vẽ thêm chỏm lửa thứ ba trên mũi (ổn). CHỜ người dùng chọn (chưa có `L1_duyet.png`).

## 3c. Người dùng chốt (2026-11-14)

- "**A**" → `tai_ve/L1_duyet.png` = `L1_bach.png` (bạch hổ mây lửa). Ba câu hỏi kèm theo (chuông, số dạng, số lượt lướt) người dùng không trả lời:
  làm theo giả định đã báo (bỏ cả chuông đồng ôm ngực; một dạng trước; 12 lượt lướt).

## 6. Mảnh (`hoa_ho_manh.py`, prompt `build_hoa_ho.py manh`; bắt đầu 2026-11-14 12:20)

Theo cách tách của rig gốc. Con gốc viền riêng từng khúc và che chỗ nối chân – thân bằng mây + vòng cổ chân; mình giữ cách đó nhưng trong MỘT
chân, trong thân, trong đuôi thì gen liền (không nét nối giữa các khúc).

- **Hai tờ LIỀN** (`to_lien` → `mau/lien_LA.png`, `lien_LB.png` + `.json`; `luot_2_lien_<tờ>.txt` → `tai_ve/N_LA.png`, `N_LB.png`; `cat_lien`):
  LA = chân sau xa (4 part) + THÂN (`P_tun` + `P_shenti_01`) + ĐUÔI (`P_weiba_02` + `_01`), 0,884 px / đơn vị; LB = chân sau gần + chân trước gần
  + chân trước xa, 1,000 px / đơn vị. Bàn chân tô kem sẫm; hai bàn chân GẦN là mu bàn trơn (ngón rời ở tờ E), hai bàn chân XA vẽ liền bốn ngón
  có móng. Ô nướng × 2,0 ảnh vùng.
- **Năm tờ KHUNG PART** (`nhom_part` → `mau/part_<tờ>.png`; `luot_2_manh_<tờ>.txt` → `tai_ve/N_<tờ>.png`; `cat_part`, `so_part`):
  M1 (× 3,3) sáu cụm mây lớn; M2 (× 4,0) bảy cụm vừa; M3 (× 5,0) chín cụm nhỏ (mây: đỏ son, lõi cam theo biến đổi khoảng cách);
  D (× 3,7) đầu trên `P_tou` (mảng ĐỎ ở đúng chỗ con mắt rời: dặn KHÔNG vẽ mắt), hàm dưới `P_zui` (lòng miệng đỏ sẫm dò theo ảnh gốc), lông má xa
  `P_zui_01`, mắt `P_yanjing`, hai nanh, hai hàm răng, hai tai, hai chỏm lửa trán (`P_maofa_03/04`), ba mảnh mày (`P_meimao_*`);
  E (× 4,5) sáu vòng cổ chân, tám ngón chân gần (móng than dò bằng ngưỡng Otsu trên ảnh gốc).
- **Bỏ**: sừng, khuyên, chuông; hai chùm râu xoắn `P_L_huxu`, `P_R_huxu` (concept A không có; vệt xoắn đỏ vẽ ngay trên má của `P_tou`).
- **Mắt nhắm** `P_biyan` (hai nét mí) do mã vẽ lại bằng mực của mình (`hoa_ho_manh.py biyan`).
- Rig giữ chỗ (`HH_THIEU=1 HH_RA=…/rig_thu`): lắp hình tô phẳng của tờ hướng dẫn vào lưới của họ, ra đúng bố cục (`rig_thu/soi_idle.png`).
- Gen: `chay_hoa.py` chạy tách từ 12:24 (LA, LB, D, M1, M2, M3, E), nhật ký `inbox/chay_hoa.log`.

## 7. Mảnh đã về, rig da mình (2026-11-14 12:24–12:50)

- Gen một lượt, không tờ nào phải gen lại: `N_LA.png` (89 s), `N_LB.png` (75 s), `N_D.png` (85 s), `N_M1.png` (158 s), `N_M2.png` (82 s),
  `N_M3.png` (115 s), `N_E.png` (92 s). Tờ liền phủ 0,96–1,04 hình bóng từng part, không nét chia khúc bên trong. Tờ khung part IoU 0,93–0,99;
  dưới 0,9 chỉ có ba mảnh tí hon: `P_maofa_19` 0,87, `P_ya_02` 0,88, `P_yanjing` 0,86. Tờ so `mau/so_part.png`.
- **Con mắt** `P_yanjing`: Codex vẽ thành mảnh kem trơn (bỏ mống mắt) → vẽ bằng mã trong đúng hình bóng của họ (`hoa_ho_manh.py mat`: mí mực, mống hổ
  phách, con ngươi khe dọc, chấm sáng).
- **Rig** `py -3 -I quai/khoa.py nang -- py -3 -I hoa_ho_rig.py` → `inbox/hoa_ho_1/rig/`: 200 xương, 70 slot, 1088 đỉnh, 8 clip, 23 sự kiện, atlas
  1088 × 1136 (0,6 px / đơn vị rig), `.atomik` 587 KB; nối clip về idle 0,00 px; `chan_dung.png`. Trang `rig/xem.html` (thu_xem: đủ 8 clip + chạy nối).
- **Đã soi**: bộ vẽ Python (`khung_<clip>.png`, cận đầu `_can_dau.png`, cận gầm `_can_gam.png`) và runtime Spine thật (`rig/that/idle.jpg`,
  `attack.jpg`, `skill.jpg`). Mặt đúng concept A (vệt xoắn đỏ trên má, mắt hổ phách dưới mày đỏ, hai nanh); lúc gầm hàm há ~30° lộ lòng miệng đỏ sẫm,
  răng trên, nanh; đòn vả chân xa giơ cao rồi đập; die đổ sấp rồi tan.
- **Chiêu cuối sửa sau khi soi runtime thật**: bản đầu mỗi lượt 0,11 s (không trùng khung mẫu) → lúc lật ngang giữa hai lượt lộ một vạch mỏng (tỉ
  lệ x đi qua 0 khi còn hiện) và các lớp mờ chồng nhau lộ "xuyên thấu". Nay mọi ẩn / hiện rơi đúng khung mẫu: tan 1 khung ở 16/30 s; mỗi lượt đúng
  3 khung (ẩn ở đầu quãng → HIỆN đặc ở giữa quãng → ẩn ở cuối quãng), lật chỉ giữa hai khung ẩn; 12 lượt từ 19/30 s; hiện lại 2,00 s (2 khung);
  `no` = `trung` 2,30 s; dài 2,93 s. `appear` hiện trong 2 khung.
- Chưa làm: đổi thứ tự vẽ của `die_01` (khung 17 trở đi; nhìn tờ khung không thấy sai); móng chân trước gần hơi to so với concept; chưa xem trong
  game; VFX; vào game.

## 8. Vào game + dạng 1 + VFX (2026-11-14 chiều, người dùng: "Ok cho vào game rồi làm dạng 1")

- **Suất `hoa_tinh`** (id, thẻ, chỉ số giữ): `quai/doi_hoa_ho.py` (dùng lại `doi_phap_lua.py`). Tên Claude đặt, người dùng chưa duyệt: tướng
  **Bạch Viêm Hổ** ("Bạch hổ cưỡi mây lửa"), dạng 1 **Viêm Hổ Nhi**; thẻ Hổ Gầm Chấn Viêm / Ảnh Trảo Liên Hoàn / Mây Lửa Hộ Thân. Rig vào
  `Resources/hoa_ho_non` (dạng 1), `Resources/hoa_ho_1` (dạng 2); thư mục `hoa_tinh_1/2` cũ không đụng. Cỡ 0,8 / 0,95 (1,1 thì thân dài tràn mép
  phải sân). Golden không đổi (số dạng vẫn 2). EditMode 106 / 107 (lỗi cũ PrefabOnlyTests ở UI/Kit).
- **Dạng 1** (`hoa_ho_rig.py` với `HH_DANG=non`, `hoa_ho_non.py`): cùng xương, lưới, clip, da; khác: xương đầu `bone5` phóng 1,4; mắt tròn to
  vẽ bằng mã trên một ô vuông bám xương đầu (`HH_MAT` = tâm x, y, bán kính); bỏ nanh dài, vòng vàng cổ chân, mảnh mày `P_meimao_01`; lửa đổi
  sắc +20° bằng mã (đỏ → cam, cam → vàng); nửa đầu trên `P_tou` Codex vẽ lại đúng hình bóng (tờ `N_DAU`, IoU 0,98: bỏ hốc mắt đỏ, vòng xoáy
  cam); chiêu cuối 6 lượt (2,33 s), impact nhẹ hơn. KHÔNG có concept riêng (người dùng chưa xem trước), chưa có clip `evolve`.
- **VFX** (`Assets/01 Script/Game/Battle/HatHo.cs`, đi đường "n_"): `n_ho_va` (ba vệt vuốt lửa lúc vả; thêm vào `HatLua.AtkLao`),
  `n_ho_gam` (gồng hút than hồng; gầm: vòng xung kích ở mồm + hai vòng lửa loang trên đất, các đợt sóng gầm, lưỡi lửa thấp tạt dọc đất = sóng
  nhiệt; nổ ở đối thủ), `n_ho_anh` / `n_ho_anh1` (12 / 6 lượt: màn âm bản từ lúc tan tới lúc hiện lại, mỗi lượt một vệt lướt + vệt chém để lại
  sẹo lửa cháy, cuối cùng sẹo nổ lần lượt rồi nổ lớn). Màn âm bản: shader `PokiClash/UIInvert` + `Assets/Resources/UIInvert.mat`,
  `StageView.Neg(dur)` đổi vật liệu lớp chớp phủ sân (đảo cả bảng máu trong sân; hạt cũng bị đảo nên sẹo hiện màu lam trong lúc âm bản).
  `Themes["hoa_tinh"]` về bảng "lua". Thử: menu "PokiClash/Thử/Đảo Hỏa: riêng Bạch Viêm Hổ..." và "...Viêm Hổ Nhi (dạng 1)..." (đang Play).
- Đã soi trong trận (ảnh chụp tour, cả hai dạng): ba đòn chạy, hổ lướt qua đúng chỗ đối thủ. Chưa soi: ô xem trong hộp chi tiết tướng, lật
  phía địch (hổ đứng bên trái), cỡ mới 0,8 / 0,95.

## 9. Dạng 1 làm lại bản CHIBI (2026-11-14 tối, người dùng: "Hổ con xấu quá, gen lại chibi hơn")

- Bản mục 8 (da dạng 2 + đầu phóng to, `HH_DANG=non`) bị chê. Làm lại: tỉ lệ đổi trên rig trước (`HH_KDAU=2`, `HH_CHAN=0,68` chân ngắn + cả con hạ
  xuống bằng xương `all`, `HH_DUOI=0,6`) → hình bố cục `inbox/hoa_ho_non/mau/bo_cuc_chibi.png` → hai concept (`hoa_ho_non.py bo_cuc`, `concept`;
  `tai_ve/L1_A.png`, `L1_B.png`) → người dùng chọn **A** (`L1_duyet.png`).
- Mảnh: bốn tờ "đúng chỗ, đúng cỡ" từ concept (`hoa_ho_non.py manh_prompt` → `tai_ve/C_THAN`, `C_CHAN`, `C_DUOI`, `C_DAU`; đạt cả bốn ngay lượt đầu),
  cắt bằng `hoa_ho_chibi.py cat` → `inbox/hoa_ho_non/manh_chibi/` (ghép lại lệch concept 3,4 % điểm). Hàm dưới cắt từ ảnh đầu theo đường môi
  (đa giác `HAM`), chỗ đó trên ảnh đầu tô màu lòng miệng; mắt nhắm vẽ bằng mã; viền đỉnh ba chân trước thân xoá bằng mã.
- Rig `HH_DANG=chibi py -3 -I hoa_ho_rig.py` → `inbox/hoa_ho_non/rig_chibi/` (11 slot, 2485 đỉnh, 558 KB; `hoa_ho_chibi.lap`): dáng nghỉ = concept
  (gắn ở dáng khung 0 idle). Đầu cứng trên `bone5`, hàm trên `bone57`; thân tra trọng số theo lưới thân của họ rồi làm mượt; bờm tra theo các cụm mây
  cổ + pha 55 % xương cổ; đuôi bám 4 đốt gốc đuôi; mỗi chân bám chuỗi đùi – ống – bàn theo độ cao khớp (tra theo lưới chân của họ thì clip chạy
  vặn méo chân). Chân vả (`c_chan4`) có slot sinh đôi vẽ trên đầu, bật trong khung 4–20 của `attack` (đầu to che mất chân giơ).
- Vào game: đè `Resources/hoa_ho_non` (bản mục 8 còn ở `inbox/hoa_ho_non/rig/`), cỡ 0,9. Tour "riêng Viêm Hổ Nhi (dạng 1)" chạy đủ ba đòn.
- Còn yếu: clip `walk` chân sau gập thành cục ở vài khung (game chưa dùng `walk` trong trận); khung cuối `cast` bàn chân trước hơi méo; chưa có
  `evolve`.
- **Sửa theo người dùng (2026-11-14, xem trên điện thoại):** "đầu bị hở" ở clip gầm (đầu ngửa lên rời khỏi thân) → thêm mảnh cổ `c_co` vẽ bằng mã
  (viên thuốc màu lông, đáy bám như thân, đỉnh bám xương đầu, vẽ sau đầu); "animation đánh thường layer bị lỗi, chân phải ở dưới body" → chân vả
  `c_chan4` vẽ DƯỚI thân, bỏ slot sinh đôi vẽ trên đầu (chân giơ lên bị đầu che, cú vả vẫn thấy lúc chân duỗi tới). Đã xuất lại, đè
  `Resources/hoa_ho_non`; lần này chỉ soi khung bằng bộ vẽ Python, CHƯA chạy lại tour trong trận.
- **Sửa lần hai (người dùng: "Animation walk chân trái cũng lỗi", "Animation die cũng lỗi"):** chân không bám cả chuỗi đùi – ống – bàn nữa (gối gập
  tới 120° làm lưới nhàu, đỉnh chân bo tròn lòi ra ngoài thân lúc chạy và lúc gục). Nay mỗi chân là một ống co dãn: đỉnh bám như THÂN ở chỗ nó
  cắm vào, bàn chân bám cứng xương bàn (`KHOP[...][-1]`; chân vả dùng `bone45`, không dùng đốt ngón `bone68`), khúc giữa pha dần theo độ cao.
  Miếng mắt nhắm lấy màu lông của chính ảnh đầu (trước lệch tông, lộ thành miếng vá). Soi lại bằng bộ vẽ Python: walk, die, attack, cast, hit
  sạch; còn: lúc `die` mờ dần các mảnh nhìn xuyên qua nhau (mờ theo từng slot), chân sau dãn dài ở hai khung walk. CHƯA chạy lại tour trong trận.
- **Sửa lần ba (người dùng: "Walk chân sau lỗi"):** chân mập một khúc mà sải theo `run_01` của họ thì bị kéo dãn thành nêm và lòi phần đỉnh đã xoá
  viền. (1) Chỉ xoá viền ở 30 % trên cùng của chân (phần bám cứng theo thân), phần dưới giữ viền; (2) ở clip `walk` của bản chibi mọi độ lệch
  xương (trừ `move`) nhân `HH_BUOC` = 0,5: cả con nhún nhẹ, bước ngắn. Chỉ dịu riêng xương chân (đã thử 0,4–0,5) thì hông vẫn nhồi đủ biên độ,
  bàn chân bị kéo lún dưới mặt đất. Còn: ở khoảng 0,7–0,8 s một bàn chân hạ thấp hơn các chân khác ~50 px. Chỉ soi bằng bộ vẽ Python.
- **Sửa lần bốn (người dùng: "Cả 1 chân trái trước và sau khi walk đều lỗi, rig lại xương"):** bỏ cách "ống co dãn bám xương bàn của họ". Mỗi chân nay có
  BA XƯƠNG RIÊNG (`c_chanN_a` đùi, `_b` ống, `_c` bàn; `hoa_ho_chibi.lap`): háng nằm trong thân và là con của xương thân trội ở đó, gối gập theo
  `GOI` (chân sau gối ra trước, chân trước khuỷu ra sau), độ dài cố định (rig 212 xương). Góc ba xương do `hoa_ho_chibi.ik` đặt từng khung, sau
  hàm clip (`hoa_ho_rig.lam_clip` bọc `c.fn`): clip của họ → cổ chân tới chỗ xương bàn của họ (với không tới thì duỗi thẳng); clip `walk` → bước
  tự viết (hai nhịp mỗi vòng, hai cặp chân chéo lệch nửa nhịp, chống thì nằm trên mặt đất, đưa tới thì nhấc 20 % chiều dài chân). Thân trong `walk`
  = dáng đứng idle khung 0 + 0,5 lần dao động của `run_01` quanh dáng trung bình (dịu về dáng gốc của rig thì thân hạ thấp, chân phải gập gục).
  Soi tờ khung bằng bộ vẽ Python: walk, idle, attack, cast, die, hit, appear sạch ở cỡ soi; CHƯA chạy lại trong trận.
- **Sửa lần năm (người dùng: "khi nhún chân xuống 2 chân trước lỗi"; dặn ghi vào skill: nhún thì cho khớp ngắn lại, không đè khớp):** thêm xương
  gốc chân `_r` (háng → cổ chân). Đích gần hơn lúc nghỉ → ÉP NGẮN cả chân dọc trục bằng tỉ lệ của `_r`, không gập thêm gối; đích xa hơn → IK hai
  khúc như cũ. Xương bàn `_c` thành con của xương thân, `ik` dời nó tới đầu ống chân (làm con của ống rồi nhân tỉ lệ ngược thì bàn chân bị kéo
  méo thành vệt). Rig 216 xương, 597 KB (sát đích 0,6 MB). Luật đã ghi ở skill `pokiclash-spine-rig` mục 29. Soi khung bằng bộ vẽ Python (walk,
  cast lúc nhún sâu nhất, attack, die, hit, idle); CHƯA soi lại chiêu cuối, CHƯA chạy lại trong trận.
- **Người dùng duyệt 2026-11-14 tối ("Ok ổn cho vào game đi"):** bản chibi có xương chân riêng là bản trong `Resources/hoa_ho_non` (trùng
  `inbox/hoa_ho_non/rig_chibi/hoa_ho_non.atomik`, 597 KB), prefab `hoa_tinh` trỏ hoa_ho_non / hoa_ho_1, cỡ 0,9 / 0,95. Chạy lại tour "riêng Viêm
  Hổ Nhi (dạng 1)" trong trận sau khi rig lại chân: đủ ba đòn + hiệu ứng, chân không lỗi (tờ ảnh ở scratchpad phiên, không lưu trong dự án).
  EditMode 106 / 107 (lỗi cũ PrefabOnlyTests ở UI/Kit). Còn thiếu: clip `evolve` dạng 1 → dạng 2; soi ô xem tướng và phía địch.
