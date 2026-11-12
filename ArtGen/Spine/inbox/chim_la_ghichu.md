# Chim bảo hộ rừng cánh lá (`chim_la`): tướng thứ 6 đảo Mộc

Bắt đầu 2026-11-12. Con gốc của rig: `monster_3630` (game tham khảo, kho `D:\Ripper\SwordxStaff`). Xương, lưới, chuyển động gốc là của
nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình. Tên, id game, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-12, kèm ảnh chụp `monster_3630`)

- Concept: **chim bảo hộ rừng**; reskin **phần cánh thành lá cây**; **đuôi vẫn có thể để là đá**; **làm khác con gốc đi**.
- appear: chim bay vào.
- Tấn công thường: lao tới đâm mỏ vào đối thủ (tận dụng `run` của nó, tăng tốc lên).
- run: làm giống họ.
- Chiêu mana: na ná `skill_03`: chim đứng dọc, dùng cánh quạt mạnh MỘT phát, các lá lông trên cánh bay ra găm vào người đối thủ rồi
  quay về cánh.
- Chiêu cuối: giống `skill_04`, gọi ra một thiên thạch đá rơi từ trên trời xuống đầu đối thủ.

Màu, kiểu mào, chi tiết: người dùng chưa dặn. Mục 3 là **đề xuất của Claude**, chờ chọn hướng.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3630/`: `info.json`, `att_goc.json`, `att_idle0.json`, `cay_xuong.txt`, `parts/`, `parts_<nhóm>.png`, `khung/`, `can/`, `sample_dk.json`)

239 xương, 169 slot (138 hình bật ở dáng gốc), 11 clip, atlas 148 vùng (ảnh nhỏ: thân 186 × 157). **FK thuần**: chỉ có hai IK `L1`, `L2`
mặc định tắt (bật trong một đoạn của `skill_03`); không path / transform constraint. Mọi hình là lưới có trọng số, phần lớn 1–3 xương.
Con gốc nhìn sang PHẢI (đầu nghiêng, lộ một mắt): không lật. Dáng gốc (setup) khép cánh; dáng xoè cánh như ảnh người dùng chụp là
`idle_01` giây 0 → bố cục concept lấy ở `att_idle0.json`.

Cây xương: `root > bone2 > bone` (dời cả con) `> bone3` (hông) `> bone4 > bone5` (ngực) `> bone6 > bone7 > bone8` (cổ, đầu).
- Đầu `bone8`: mỏ trên `bone41`, mỏ dưới `bone42` (+ lưỡi `bone43-45`), mắt `bone115`, mào `bone92..114`, `bone207`.
- Ngực `bone5`: giáp ngực `bone116..119`; cánh GẦN (bên trái hình) `bone123 > bone124 > bone125 > bone144 >` hai nhánh (`bone126..150`
  bộ R1, `bone164..177`, `bone219` bộ R3) + `bone151..163` (bộ R2); cánh XA (bên phải hình) `bone178 > bone179 > bone180 > bone181 >
  bone182 ...` + `bone183..186`, `bone193..218`; túm lông gáy `bone120-122`.
- Hông `bone3`: chân gần `bone9-10-11-16` + bốn ngón; chân xa `bone12-13-14-15` + bốn ngón (bộ xương thứ hai `bone220..235` cho bộ slot
  chân dự phòng); bốn chuỗi đá `bone46 > bone47..52`, `bone53..56`, `bone57..61`, `bone62..66`; sáu lông đuôi `bone67 >` sáu chuỗi 4–5 đốt.

Mảnh theo nhóm (tờ `parts_<nhóm>.png`):
- **Cánh gần ngoài** `chibangR1_01..16` (trên cùng): 2 dải đá hoa văn (01, 02), 11 lông pha lê hình thoi (03..13), túm lửa (14), hai
  mảng lông phủ lớn (15, 16). **Cánh gần trong** `chibangR2_1..14`: 2 dải đá, 10 lông, 2 mảng phủ (9, 14).
  **Bộ `chibangR3_01..15`** (mặc định tắt): mặt kia của cánh gần; clip bật R3 và tắt R1 khi cánh giơ lật (run, skill_02/03/04, die).
- **Cánh xa** `chiabangL_01..27` + `010`, `011` (sau cùng): 5 dải đá (01..05), 21 lông, túm lửa (22), hai mảng phủ (21, 23).
- **Mào** `toushi_01..09`: hai dải lông dài cong (05: 6 xương, 07: 5 xương), 08 (3 xương), 09 (chạc đôi sau gáy, 5 xương) vẽ SAU đầu;
  năm tấm pha lê dẹt trên trán (01, 02, 03, 04, 06; mỗi tấm một xương) vẽ TRƯỚC đầu.
- **Đầu** `tou_01` (23 đỉnh, 3 xương), mắt `yanjing_01` (hình `yanjing_02` = mắt nhắm lúc hit / die), mỏ `zui_01`, `zui_02`, lưỡi.
- **Thân** `xiong` (cổ – ngực, yếm trắng), `xiashen` (bụng, có mảng vảy pha lê), `mao_01` (túm lông gáy), `mao_02`.
- **Giáp ngực** `xiongjia_05` (cụm pha lê lớn), `06`, `07`; móc đá `01`, `03`, khoá đá có ngọc `02`, vòng đá `04`.
- **Chân**: đùi `datuiR_01`, `datuiL_01`; ống `xiaotuiR/L_01`; bàn `jiaozhangR1_01`, `jiaozhangiL_01`; mỗi ngón 2 đốt + 1 vuốt
  (`jiaozhi*_03`, `jiaozhiR4_02`). Bộ slot chân thứ hai (`*_02`, `*_04..06`, mặc định tắt) bật khi co chân lúc bay (run, die).
- **Lông đuôi** `weiba5_01..06` (sáu tàu lông lớn, 4–5 xương). **Chuỗi đá** `weiba1..4`: tảng đầu chuỗi + 3–4 viên nhỏ + viên cuối to.

Clip của họ (tờ `khung/`):
| clip | dài | nội dung |
|---|---|---|
| idle_01 | 1,33 s | lơ lửng, hai cánh khép – mở một nhịp |
| run_01 | 0,80 s | bay ngang: thân nằm ngang, co chân, vỗ cánh một nhịp (cánh giơ ở 0 s, quạt xuống 0,27–0,44) |
| skill_01 | 1,33 s | dựng người khép cánh 0,15–0,44; LAO chúi tới, đầu và vuốt đi trước 0,59; xoè cánh 0,74; về |
| skill_02 | 1,50 s | xoè ngang, giơ cánh cao 0,50–0,67, đập xuống 0,83, khép 1,00 |
| skill_03 | 2,17 s | đứng dọc giơ hai cánh cao 0,24–0,48; quạt xuống 0,72–0,96; giơ lại 1,20; vặn người quét cánh 1,44–1,69; về |
| skill_04 | 2,00 s | thu hai cánh ôm thân 0,22–0,67; bung cánh, ngửa mặt lên trời 0,89–1,56; hạ cánh 1,78; về |
| hit_01/02, stun_01, block_01 | | |
| die_01 | 1,00 s | lộn nhào, rơi nằm sấp, cánh trải (đổi thứ tự vẽ) |

## 3. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `ArtGen/Spine/chim_la.py` (`part_goc`, `tho`, `bo_cuc [hướng]`), `build_chim_la.py` (gói `gui_gpt/chim_la_1/`).
Sơ đồ bố cục = khối từng mảnh của rig ở dáng xoè cánh, làm trơn, tô phẳng theo nhóm màu của mình (không đính ảnh con gốc); mào vẽ
mới bằng mã. Tỉ lệ rig → khung concept 0,7062.

Giữ của con gốc: chim săn mồi lơ lửng nhìn sang phải, lộ một mắt, hai cánh xoè, hai chân vuốt giơ trước (chân gần buông, chân xa
vươn), sáu lông đuôi dài rủ, bốn chuỗi đá.
Của mình:
- **cánh**: dải đá hoa văn → **cành cây** làm xương cánh (nhánh móc như tua cuốn); mảng lông phủ → **tán lá** sẫm xếp lớp; từng lông
  pha lê → **từng chiếc lá** nhọn có gân giữa (hàng dài + hàng ngắn nhạt); túm lửa → **chồi non**;
- **mào đổi hẳn dáng** (mảnh nhận diện): bỏ hai dải lông dài cong + vương miện pha lê; thay bằng quạt lá hoặc tàu dương xỉ, có vòng gỗ
  ở trán;
- cụm pha lê ngực → **vòng cổ lá**; khoá đá → **bùa đá** có viên ngọc nhỏ + vòng đá; mảng vảy bụng → mảng rêu;
- chuỗi đá: giữ là đá (người dùng cho phép), tảng cuối **phủ rêu + mầm hai lá** thay cho đầu pha lê;
- mặt "chiến": mắt xếch, nét mày ghì xuống mỏ.

Lượt 1, ba hướng (tờ so `inbox/chim_la_1/so_ba_huong.html`):
- `nau` (`tai_ve/L1_nau.png`) **A · đại bàng rừng**: lông nâu vỏ cây `#9A6B42`, mũ + đùi nâu sẫm `#5E4028`, ngực + mặt kem `#F1E3BC`,
  lá lục `#5FA646` / `#9CCB58`, tán `#3B7F43`, cành `#7A5232`, đá xám `#8C8A7E`, mỏ hổ phách; mào **quạt năm lá**.
- `ngoc` (`tai_ve/L1_ngoc.png`) **B · chim ngọc rừng mưa** (kiểu chim quetzal): lông lục lam `#1F8C7C`, ngực đỏ `#C9463A`, lá
  `#6DBB4A` / vàng chanh `#C2E062`, đá bazan `#6A6C72`, vuốt kem; mào **hai tàu dương xỉ** + ba lá sau gáy.
- `bach` (`tai_ve/L1_bach.png`) **C · linh điểu trắng**: lông trắng kem `#F4EFDC`, mũ lục xám `#7E9E7A`, lá lục sẫm `#4C9A52`, cành
  cánh nở **hoa hồng nhỏ**, mỏ + chân cam `#EE8A3E`; mào quạt lá.

## 4. Clip (dựng ở tầng điều khiển của rig gốc: `chim_la_clip.py`)

Xem thử trên rig gốc (hình của họ, nội bộ): `<SXS>/scan/monster_3630/lam_clip/xem/xem.html` (`chim_la_clip.py song`: trang sống 60
khung/giây, nút từng clip, tốc độ 1× / 0,5× / 0,25×; người que = chỗ đối thủ; lá lục = lá cánh bay ra / về; khối xám = thiên thạch).
Clip của họ đổi hình theo khung (bộ cánh R1 ↔ R3, bộ chân, mắt nhắm) và die đổi thứ tự vẽ → mỗi dáng mang theo tên hình từng slot
và thứ tự vẽ của khung nguồn; pha hai dáng thì lấy của dáng nặng hơn.

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| ca_idle | 1,33 s lặp | nguyên idle_01 | |
| ca_walk | 0,80 s lặp | nguyên run_01 | |
| ca_attack | 1,30 s | lấy đà 0–0,16 (ngả lùi, cánh giơ); BAY LAO 0,16–0,42 (run_01 nhanh 1,9 lần, tăng tốc, tới 560 đơn vị); ĐÂM MỎ 0,42–0,50 (dáng lao của skill_01 0,63 s, cổ vươn thêm); khựng tới 0,66; bật lùi bay về 1,12 | trung 0,50 |
| ca_cast | 2,20 s | (bản 2, theo lời người dùng) CHỈ nhịp đập cánh THỨ BA của skill_03 (1,16 → 2,17 s): dựng người xoè cánh 0–0,26; giơ hai cánh ra sau lấy đà, giữ đỉnh tới 0,58; VẶN NGƯỜI QUÉT cánh ra trước 0,58–0,72; giữ hai cánh khép chéo tới 1,30; mở cánh đón lá 1,30–1,64; về | tu 0,26; nem 0,70; trung 0,95; ve 1,30; toi 1,64 |
| ca_skill | 2,60 s | thu cánh ôm thân 0–0,26; tụ lực tới 0,90 (rung mạnh dần); BUNG cánh ngửa mặt 0,90–1,08; giữ dáng gọi tới 1,80; đập cánh xuống 1,80–1,94 đúng lúc thiên thạch nện | tu 0,26; goi 1,08; roi 1,34; trung 1,94 |
| ca_appear | 1,75 s | bay vào từ sau – trên (−760, +380), hiện dần 0,2 s đầu, tới nơi 0,95; dựng người xoè cánh hãm tới 1,22; hạ về nghỉ | toi 0,95 |
| ca_hit, ca_die | 0,5 s; 1,0 s | nguyên hit_01, die_01 | |

Kênh riêng (`<scan>/kenh_rieng.json`): `bay` (xương `move`), `mo` (độ đậm cả con lúc appear), `la` (quãng 0..1 của lá bay + bật / tắt),
`da` (quãng rơi của thiên thạch).

Việc của rig cho chiêu mana (người dùng tả rõ lá CỦA CÁNH bay ra rồi quay về, nên lá là mảnh của rig như tảng tay của tượng đá, không
phải hạt VFX): bản sao một số lá dài trên xương `fly_*` (con của root, game co quãng tới `far`), lá thật ẩn trong lúc bay; về thì khớp
đúng chỗ lá thật. Thiên thạch là VFX (lớp hạt của game), rig chỉ đặt sự kiện `goi`, `roi`, `trung`.

**Người dùng chọn hướng C (`bach`) 2026-11-12** → `tai_ve/L1_duyet.png`. Cùng lúc góp ý chiêu mana: "chiêu cast chưa đúng ý tôi lắm, bạn
xem skill_03 sau 2 lần đập cánh đầu thì sang lần đập cánh thứ 3 chính là kiểu đập cánh tôi muốn" → bản đầu (nhịp quạt thứ nhất nén
lại) bỏ; `cast` nay chỉ dùng nhịp thứ ba (vặn người quét cánh, bảng trên). `nem` đặt ở 0,70 s vì bộ cánh gần đổi R3 → R1 đúng khung 21:
lá bay lấy chỗ xuất phát ở lá bộ R1.

## 5. Mảnh theo khung part (`chim_la_manh.py`, prompt `build_chim_la.py manh`)

Ảnh vùng của họ 0,501 px mỗi đơn vị rig. Mỗi part một ô đúng khung ảnh vùng × z, trong ô hình bóng kín tô phẳng theo thiết kế (lá có
gân giữa; tán lá có hàng vảy; đá có chỏm rêu ở phía TRÊN theo thế giới dáng gốc; đầu có mũ lục xám, mặt kem, mắt vẽ sẵn trong ảnh đầu).
Viền trên tờ = 8 đơn vị (mảnh nhỏ 5,7) × 0,5 × z px, khớp nét 6 px / 4 px của concept. 15 tờ tự xếp + tờ thân liền:

| tờ | z | nội dung |
|---|---|---|
| la_gan1, la_gan2 | 3,2 | 21 lá cánh gần (bộ R1, R2) |
| la_xa | 3,2 | 15 lá cánh xa (6 slot khác dùng lại ảnh) |
| la_lat | 2,6 | 11 lá bộ R3 (mặt kia của cánh gần) |
| tan | 2,4 | 6 mảng tán lá |
| tan_lat | 2,6 | 2 mảng tán + 2 khúc cành của bộ R3 |
| canh | 3,0 | 9 khúc cành + 2 chồi non |
| duoi1, duoi2 | 2,2 | 6 lông đuôi (kem / lục xám xen kẽ) |
| da | 3,4 | 19 vùng đá (4 tảng đầu chuỗi + 4 tảng cuối có chỏm rêu, 11 vùng đá nhỏ) |
| dau1, dau2 | 3,2–8 | đầu (×5), hai nửa mỏ (×8), túm lông gáy, vòng cổ lá (3), bùa đá (4, ×5), hai đùi |
| chan1, chan2 | 5,0 | 19 khúc chân / ngón + 8 vuốt |
| X | (2 px / đơn vị) | ô THÊM: năm lá mào dựng đứng, vòng gỗ, mầm hai lá, bông hoa |
| L (thân liền) | 4,0 | cổ – ngực (`xiong`) + bụng (`xiashen`) + túm lông che gốc đùi (`mao_02`) là MỘT bề mặt kem: gen liền rồi nướng vào khung part (`chim_la_manh.py lien`) |

Bỏ của họ: mắt (2 hình; mắt vẽ trong ảnh đầu), lưỡi, 9 mảnh mào. Chân, ngón giữ mỗi khúc một ô có viền kín (ngón chim có đốt, concept
cũng vẽ vạch đốt); chỉ thân mới làm tờ liền.

## 6. Rig (`chim_la_rig.py` → `inbox/chim_la_1/rig/`)

- 259 xương (đủ của họ trừ `shadow`, `L1`, `L2`; thêm `move`, `mieng`, `far`, `fly_0..9`, `la_0..9`), 185 slot. `bone144` có inherit
  NoScale (gốc hai nhánh cánh gần; cha nó co giãn trong clip): phải khai `khong_ti_le`, không thì cánh gần ép thành vạch.
- Bộ slot ẩn sẵn (cánh R3, bộ chân thứ hai) bật / tắt theo trường `n`, `a` của mẫu; `dau_nham` (ảnh đầu mắt nhắm, mã tô lại vùng mắt) bật
  khi họ đổi hình mắt (hit, die). Clip `die` của họ đổi thứ tự vẽ: `.atomik` chưa hỗ trợ, bỏ qua (soi thấy vẫn ổn).
- **Mào**: năm chuỗi xương mào của họ nắn thẳng theo năm lá (`MAO`: bone110-113-114 lá 1; bone95 lá 5; bone96-98 lá 2; bone99-103 lá 4;
  bone104-109 lá 3), mỗi lá là dải lưới 3 cột bám chuỗi (B-spline); các đốt chỉ nhận độ lệch xoay của clip gốc nên lá đung đưa như mào
  của họ. Chỗ đặt lá lấy từ sơ đồ đã duyệt (dáng idle 0 s) đưa về dáng gốc qua xương đầu `bone8`. Vòng gỗ: mảnh cứng trên `bone8`.
- **Hoa** (7 bông): ô cứng bám theo trọng số của khúc cành ngay chỗ dày nhất của nó; ẩn / hiện theo slot cành. **Mầm** (4): mảnh cứng
  trên xương chính của tảng đá cuối chuỗi, vẽ ngay sau tảng đá.
- **Lá bay (chiêu mana)**: 10 lá dài (`LA_BAY`: 5 của cánh gần bộ R1, 5 của cánh xa). Mỗi lá: `fly_k` (con của root, chỉ mang quãng
  0..1 tới `far` để game co quãng) > `la_k` (độ lệch còn lại + góc); bản sao lưới lá bám 100% `la_k`; lá thật ẩn trong lúc bay. Đi: từ
  chỗ lá ở khung `nem`, bay vòng cung, mũi lá đi trước, tản quanh `far`; về: bám chỗ lá thật theo từng khung nên hạ đúng chỗ.
- Bản thử với ảnh giữ chỗ: `.atomik` 333 KB, nối clip 0 px, lệch đỉnh so với bộ vẽ Python 0,16 px.

## 6b. Sửa trong lúc lắp (2026-11-12)

- **Cành cánh đổi dáng**: 11 khúc dải đá hoa văn chữ triện của họ (mảnh rất dễ nhận ra) giữ nguyên hình bóng thì tô nâu vẫn ra hoa văn của
  con gốc → `chim_la_manh.canh_moi`: mỗi khúc dựng lại thành một cành cong mập chạy theo trục chính của khúc (bậc hai trong hệ PCA), có
  0–2 nhánh con ngắn chĩa về phía khúc cũ có móc, nằm gọn trong khung ảnh vùng. Rig gắn các mảnh này bằng Ô CẢ KHUNG cứng theo xương
  chính (không cắt theo bao lưới của họ). Đã thử nhánh cuộn tròn kiểu tua cuốn: khép thành vòng khuyên hoặc chìa khỏi khung → bỏ.
  Tờ `canh` gen ba lần (`N_canh.png` hoa văn cũ, `_2` cành mảnh, `_3` cành mập: đang dùng).
- Bỏ khỏi rig: `P_chiabangL_01` (khúc cành gốc cánh xa nằm ngay sau mỏ, nhìn như chim ngậm que), `P_mao_02` (túm lông kem không viền đè
  lên đùi lục xám, nhìn như miếng vá).
- `cat`: chỗ GPT vẽ hụt nằm ở vành mép hình bóng thì tô MỰC, không tô màu (bản đầu tô màu: ra một dải kem nằm ngoài nét viền ở mép đầu).
- `lien`: glob `N_L*` trên Windows không phân biệt hoa thường, ăn nhầm `N_la_*.png` (đã nướng nhầm tờ lá vào thân một lần) → lọc tên đúng
  `N_L.png` / `N_L_<số>.png`. Mép của mảnh thân nằm trong khối để đặc (bớt vệt chấm sáng ở ranh ngực – bụng trên trang xem Spine).
- **Lá bay phải trúng mục tiêu** (người dùng 2026-11-12: "lá phải bắn vào trúng mục tiêu nên kết hợp giữa điều khiển bằng code và
  animation... điều khiển lá bay bằng code rồi điều khiển lá rút về rồi làm anim đoạn lá gần về thì fill vào cánh cho match nhau"):
  đích là xương `far` (game dời tới tâm đối thủ; `AolaActor.FarAtomik` co quãng từng `fly_k` theo x), đặt mặc định ở 1,25 chiều cao
  (xa hơn mọi chỗ lá xuất phát: x 0..590); lá tản HẸP quanh `far` (x −36..14, y ±80 đơn vị ≈ ±9% chiều cao thân); đoạn về bám vị trí +
  góc của lá thật theo từng khung, 22% quãng cuối xoay dần về góc lá thật rồi đổi sang lá thật. CHƯA kiểm trong trận với đối thủ ở chỗ
  khác mặc định; nếu cần lái tự do hơn thì chuyển phần bay sang lớp VFX, rig chỉ giữ đoạn lấp về.
- Codex hết hạn mức giữa chừng (16:30, báo mở lại 19:17); người dùng nạp thêm, gen nốt 6 tờ. Đủ 16 tờ: IoU 0,86–0,98 (thấp nhất là
  vài lá bé và vòng đá).
- Bản đủ hình: `inbox/chim_la_1/rig/` (`xem.html`, `chim_la_1.atomik` 461 KB, 259 xương, 183 slot, 8 clip; nối clip 0 px; runtime Spine
  thật dựng đủ: `rig/spine_that/`).

## 6c. Cành cánh thành cánh tay có khớp (2026-11-12, người dùng gửi ảnh cận cánh: "các khớp gỗ ở cánh không match nhau")

Bản 6b đặt mỗi khúc cành ở chỗ khúc dải hoa văn cũ (ô cả khung) nên các khúc rời nhau, không ăn khớp. Sửa ở rig, không gen lại:
mỗi khúc cành nằm đúng dọc MỘT đốt xương cánh (gốc xương → mút xương), hai tâm đầu tròn của ảnh đặt đúng hai khớp, bám cứng đốt đó.
Chuỗi xương cánh nối mút – gốc (cánh gần: bone124 → 125 → 126 → 127; bộ R3: bone164 → 165; cánh xa: bone180 → 181 → 182) nên các
khúc luôn dính nhau ở khớp trong mọi dáng. Ảnh cho từng đốt chọn theo chiều dài tự nhiên gần nhất (`chon_canh`: đỡ kéo giãn); khúc
bị kéo dài thì cho mập thêm tới 1,25. Hoa đặt trên thân khúc cành (38–66% chiều dài đốt). Bỏ thêm `P_chiabangL_04` (trùng đốt
bone181 với `L_03`). Soi runtime Spine thật ở idle, walk, skill, cast: khớp dính ở mọi khung đã xem. Rig: 182 slot, `.atomik` 461 KB.

## 6d. Người dùng duyệt rig dạng lớn (2026-11-12: "ok ổn đấy, nhớ để ý chiêu cast tôi vừa bảo, làm dạng 1 đi")

Con trên rig `monster_3630` là DẠNG 2 (dạng lớn; thư mục vẫn `chim_la_1`, như `rong_vay_1`); dạng 1 = chim non, thư mục `chim_la_non`.
Chiêu mana: giữ cách lá bay ở mục 6b (đích `far` do game lái, đoạn về bám lá thật); còn nợ việc kiểm trong trận.

Lá bay nay tính theo ĐỘNG HỌC CỦA CHÍNH RIG (`sk.the_gioi(P)`), không đọc toạ độ xương trong mẫu của con gốc: `fly_k` để ở gốc toạ độ,
chỉ mang `q × far` (game tính phần quãng = x / x của far); `la_k` mang độ lệch còn lại + góc tuyệt đối (giữ liền mạch, không nhảy 360
độ); chỗ xuất phát = dáng ở khung `nem`. Nhờ vậy dùng được cho dạng đã đổi tỉ lệ. Dạng lớn soi lại: như cũ.

## 6e. DẠNG 1: chim non trên cùng rig (`CL_DANG=non`; skill mục 00 "DẠNG KHÁC trên CÙNG rig gốc")

- **Tỉ lệ ở rig trước** (`chim_la_rig.py`, `TI_NON`): nhân tỉ lệ ở xương gốc của chuỗi SAU KHI đã gắn xong mọi mảnh ở dáng gốc của dạng
  lớn (mọi điểm gắn tính theo dáng lớn nên tự co theo xương): cổ trên + đầu `bone6` × 1,34; hai cánh `bone123`, `bone144` (NoScale: nhân
  riêng), `bone178` × 0,60; lông đuôi `bone67` × 0,60; chuỗi đá `bone46` × 0,55; vòng cổ lá `bone116` × 0,74; chân × 0,86. Lá bay `la_k`
  co bằng đúng tỉ lệ thế giới của lá thật.
- **Bỏ** (`BO_NON`): bốn mảnh bùa đá, hai chuỗi đá (`weiba1`, `weiba4`), cụm lá ở vai, hai khúc cành trong của cánh xa (đầu to lên thì
  chạm mỏ); không có hoa, vòng gỗ, mầm trên đá. **Mào**: hai lá chữ V (`MAO_NON`: lá 4 và lá 3 dài 0,5, xoay −16° / +12°).
- **Bố cục cho concept**: `CL_DANG=non chim_la_rig.py bo_cuc` → `inbox/chim_la_non/mau/bo_cuc.png` (khung 0 idle, da dạng lớn, nền
  trắng, 0,953 px mỗi đơn vị rig).
- **Concept** (đề xuất của Claude, chờ người dùng chọn): `build_chim_la.py non` → `gui_gpt/chim_la_non/luot_1_concept_<hướng>.txt` →
  `inbox/chim_la_non/tai_ve/L1_<hướng>.png`. Ảnh mẫu: bố cục + concept dạng lớn. Chim non đầu to, mắt to tròn có nét mày quả quyết, mỏ
  ngắn, mào hai lá mầm, vòng cổ lá nhỏ, cành cánh có nụ hồng (chưa nở), sáu lông đuôi ngắn, hai chuỗi sỏi ngắn; màu nhạt hơn dạng lớn.
  Hai hướng: `kem` (lông kem `#F7EFCB`, mũ lục nhạt `#A8C690`) và `to_vang` (lông tơ vàng `#F5DC86`, mũ ô liu `#8FB36A`); lá lục non
  `#7FC25A` / `#B8DC72`, mỏ chân cam.

## 6f. Dạng 1: người dùng chọn hướng A (`kem`) 2026-11-12 → `inbox/chim_la_non/tai_ve/L1_duyet.png`; da, rig, tiến hóa

- **Chuyển da bằng MÃ, không gen lại** (`chim_la_non.py doi_mau`): 144 ảnh part đã xong của dạng lớn → `inbox/chim_la_non/manh/part`.
  Mỗi điểm cộng độ lệch màu của lớp màu dạng lớn gần nó nhất (pha mềm giữa các lớp, σ 26; mực, trắng, hồng giữ nguyên) nên hình
  bóng, nét mực, vân sáp y nguyên. Đo trung vị: tán lá (35,119,54) → (59,154,65); lá dài (87,159,75) → (123,190,86); lông đuôi lục
  xám (133,170,124) → (165,198,141); thân kem (252,242,217) → (254,242,204).
- **Chỉ gen một tờ** (`chim_la_non.py to_dau` → `gui_gpt/chim_la_non/luot_2_dau.txt` → `tai_ve/N_dau.png`; `cat_dau`): cái ĐẦU mới đúng
  khung part `P_tou_01` × 5 (mắt cam to tròn, nét mày ngắn, mũ lục nhạt; IoU 0,96) và ô NỤ HOA (thay hoa nở trên cành cánh).
- **Rig** `CL_DANG=non chim_la_rig.py` → `inbox/chim_la_non/rig/` (`chim_la_non.atomik` 615 KB kể cả dạng lớn bản nhẹ; 9 clip). Thêm
  so với mục 6e: mỏ `bone41`, `bone42` × 0,86; chuỗi sỏi `bone46` × 0,65 (0,55 thì khuất hẳn, 0,8 thì lơ lửng dưới đuôi ngắn); ảnh đầu
  mắt nhắm vẽ theo mắt tròn to. Tám clip dùng nguyên của dạng lớn (lá bay của chiêu mana co theo cánh nhỏ).
- **Tiến hóa** (`evolve` 3,0 s, `quai/tienhoa`): rig non gộp bản NHẸ của dạng lớn (`CL_NHE=1`: ảnh 0,3 px / đơn vị, không lá bay;
  `inbox/chim_la_1/rig/_nhe.pkl`). Chim non thu cánh ôm thân, co người, rung (đoạn 0 → 0,70 s của chiêu cuối); dạng lớn hiện ra đang
  vỗ một nhịp idle kéo chậm, vươn lên 60 đơn vị, ngẩng đầu, về đúng khung 0 idle. Dạng lớn co 1,063 trong rig gộp (tỉ lệ chiều cao
  đỉnh đầu 960 / 904). **Bẫy**: `n_bone144` là NoScale nên không nhận tỉ lệ của xương `evo` → khung cuối lệch 46 px; nhân bù tỉ lệ
  `evo` cho riêng xương này ở bước hậu kỳ (sau bước hoà về idle) → lệch 0,00 px.
- Soi runtime Spine thật: idle, attack, cast, skill, die, evolve của chim non; cast của dạng lớn sau khi đổi cách tính lá bay.
  Dạng lớn xuất lại với `dang=2, so_dang=2` (460 KB).

## 7. ĐÃ VÀO GAME (2026-11-12 tối; người dùng: "ok 2 dạng ổn, ghép vào game đi")

- **Suất**: tướng thứ 6 đảo Mộc = ải 30 "Thung Lũng Lá", id game GIỮ `gio_loc` (trước là Gió Lốc, ba dạng). Tên do Claude đặt, người dùng
  có thể đổi: tướng **Linh Điểu**, danh hiệu "Chim thần giữ rừng", dòng "Dòng Linh Điểu"; dạng 1 **Điểu Nhi** (`gio_loc_1` =
  `chim_la_non.atomik`, cỡ 0,92), dạng 2 **Linh Điểu** (`gio_loc_2` = `chim_la_1.atomik`, cỡ 1,1); thẻ **Lông Lá Găm** (leaf), **Thiên
  Thạch Giáng** (rock), **Cánh Lá Nhẹ** (wing); bị động boss "Gió Cuốn" giữ. Chỉ số, hiệu ứng thẻ không đổi.
- `quai/doi_linh_dieu.py` (heroes.json, cards.json; chạy lại không đổi gì), `quai/da_nhan.json` thêm dòng `gio_loc`. Chép tay 4 file vào
  `Assets/03 Art/Heroes/Resources/gio_loc_1, 2` (`.atomik` + `_portrait.png` từ `chan_dung.png`), xoá `Resources/gio_loc_3` bằng
  `manage_asset delete`. Unity (MCP 8080): refresh, "Nhập dữ liệu", "Gắn dạng .atomik vào prefab tướng" (prefab `gio_loc` còn hai dạng).
- **Golden** (ba dạng → hai dạng): "Đảo 70 ải: sinh lại" (stages.json không đổi), ba menu tính lại golden, `quai/golden_ghep.py`:
  chỉ đổi `roster.json` (số dạng của gio_loc 3 → 2) và `sim.json` ải 240 (ải 30 đảo Mộc). EditMode 102/103 (hỏng `PrefabOnlyTests` có
  từ trước).
- **VFX** `Assets/01 Script/Game/Battle/HatChim.cs` (partial HatLua), màu ở `HatNuoc.WThemes["gio_loc"]` (ba lục của lá cánh, họa tiết
  `canh_sen` hồng = cánh hoa trên cành cánh), bảng `StageView.MocAtk` / `MocFx`:
  - `n_mo_dam` (đòn thường, `HatLua.AtkLao`): bụi lúc bật, sợi gió + lá tuột lại lúc lao, chớp toé và lá bật ở chỗ mỏ chạm.
  - `n_la_gam` (chiêu mana): lá bị hút lên lúc giơ cánh, luồng sợi gió + bụi thổi về đối thủ lúc quạt (lead − 0,30), ba nhịp chớp + mẩu
    lá + cánh hoa chỗ lá găm (lead), vụn lá kéo về lúc rút (lead + 0,35), vòng nhỏ ở cánh lúc lá về (lead + 0,69). Lá bay là mảnh của
    rig (xương `fly_*`), `StageView` đặt đích cho clip Cast (đã có từ Gạc Đá).
  - `n_thach_roi` / `n_thach_roi1` (chiêu cuối dạng 2 / dạng 1 nhỏ 0,78): gồng (lá, sợi gió cuốn lên), gọi (chớp ở mỏ, chùm lá vút
    lên), lá xoáy tụ ở chỗ đá hiện, tảng đá gồ ghề phủ rêu (bốn khối tròn chung một viền mực + mảng rêu + ba lá dính) rơi chéo xuống
    ĐẦU đối thủ kèm đuôi bụi, dăm đá, lá, sợi gió, bóng báo trước dưới chân; trúng: tảng con nảy trên đất, dăm đá, bụi lan, lá và
    cánh hoa rơi.
  - **Bẫy sân thấp**: đối thủ phía trên đứng sát mép trên sân (đầu cách mép ~100 đơn vị) nên đá rơi thẳng từ ngoài sân vào chỉ thấy
    1–2 khung. Cách đang dùng: đá hiện NHỎ (0,2) ở trên cao TRONG sân rồi vừa rơi chéo vừa lớn dần tới cỡ thật (như từ rất xa lao tới).
  - Ảnh `hat_rock_*`, `hat_crack_*` là đá dung nham (vệt cam) của bộ Hỏa: không dùng cho đá rừng.
- **Lỗi đã gặp**: lúc ra chiêu mana chân và đuôi chim bị cắt ngang. `AolaSticker.Far` dời khung camera nửa quãng về phía đích; đích ở
  trên thì khung dời lên, mất phần dưới chân (khung chỉ có 0,68 chiều cao dưới chân; đuôi chim thõng dưới chân lúc đứng dọc). Sửa (dùng
  chung): đích ở trên chỉ dời lên khi cao quá 1,9 chiều cao (khung sẵn có 2,7 chiều cao phía trên chân); đích ở dưới như cũ.
- **Soi**: menu "PokiClash/Thử/Đảo Mộc: lá găm và thiên thạch đá Linh Điểu, chiêu mana và chiêu cuối từng dạng (đang Play)"
  (`MocFxTour.TryChim`), ảnh `Temp/PokiShots/thuy_fx/gio_loc_*`; tờ tổng `inbox/chim_la_1/trong_tran.jpg`. Đã xem (người chơi đánh
  đối thủ phía trên trái, ải 3): tên, thẻ, đâm mỏ, lá bay tới ĐÚNG đối thủ rồi về cánh, thiên thạch hai dạng. CHƯA xem: chim là địch
  (đánh xuống phía người chơi), appear, die, evolve và hộp chi tiết tướng trong game.

## 7b. Lá chĩa theo hướng bắn (2026-11-12 tối; người dùng: "lá khi bắn vào kẻ thù hướng lá có cùng vectơ hướng bắn, giờ lá đang ngang quá")

- Nguyên nhân: góc của lá bay (`la_k`) nướng trong rig theo hướng tới đích CỦA RIG (`far` = 1,25 × cao, 0,45 × cao; từ cánh nhìn ra gần
  như nằm ngang), còn game dời lá tới đối thủ thật (chéo lên ~40 độ khi người chơi đánh) mà không xoay.
- Sửa ở game (bật theo rig, rig khác không đổi): `game.farAim = ["cast"]` (`AtomikGame.farAim`). `AolaActor.FarAtomik`: với clip khai
  farAim, mỗi xương CON của `fly_*` xoay thêm góc = hướng (đích thật − A) − hướng (đích rig − A), A = chỗ xuất phát suy từ độ lệch của
  xương con / (1 − w) lúc w < 0,3 (nhớ lại cho đoạn sau), vào dần trong 22 % quãng đầu như rig. `AtomikPose.LocalY`, `Turn`.
- Rig: `xuat.xuat_het(..., far_aim=("cast",))` (`chim_la_rig.py` đã khai). Hai file đã xuất được vá cờ bằng `quai/va_game.py` (không
  dựng lại rig: xương, lưới, clip, atlas không đổi) rồi chép lại vào `Resources/gio_loc_1, 2`.
- VFX: sợi gió và lá vụn của cú quạt (`NLaGam`) cũng thổi theo véc-tơ cánh → thân đối thủ (trước đó thổi ngang).
- Đã xem trong trận (người chơi đánh lên): lá, sợi gió cùng hướng bắn; lá về cánh vẫn khớp. Ảnh `inbox/chim_la_1/trong_tran_la.jpg`.
  EditMode sau lượt này: 102/103 (lượt do phiên người cây chạy trên cùng mã nguồn, 2026-11-12; vẫn chỉ hỏng
  `PrefabOnlyTests.MaRuntime_KhongSinhDoVat` có từ trước). Chưa xem chiều chim là địch đánh xuống.

## 8. Việc tiếp

1. Người dùng chơi thử ải 30 đảo Mộc, hộp chi tiết tướng, tiến hóa; chỉnh tên, cỡ, hiệu ứng theo lời họ.
2. Soi chiều ngược lại (Linh Điểu là boss ải 30 đánh xuống người chơi), appear / die / evolve trong game.
