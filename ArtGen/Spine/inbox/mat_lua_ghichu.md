# Mắt lửa bọc giáp (`mat_lua`): tướng thứ 2 đảo Hỏa

Bắt đầu 2026-11-13 (máy ổ C). Con gốc của rig: `monster_3342` (game tham khảo, kho `D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh
chụp trang xem, clip `idle_01`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai.
Hình là thiết kế của mình. Tên, id game: chưa đặt (`mat_lua` chỉ là mã làm việc).

## 1. Lời dặn của người dùng (2026-11-13)

- "tướng thứ 2 đảo hỏa; concept **flaming fire eyeball có tay chân và bọc giáp**".
- appear: "1 **bộ giáp đá nằm đất** sau đó **mắt sáng lên, phồng lên** rồi **tay ở trong cũng trồi ra** rồi **bay lên**".
- idle: "làm giống họ cũng ổn". walk: "cũng có thể làm giống họ" (`run_01`).
- Đánh thường: "tướng **bay đến đấm 1 phát**, có sức nặng, mạnh, nhanh".
- Chiêu mana (cast): "animation **gần giống `skill_02`** bổ sung thêm **bắn tia lửa từ giữa mắt**" (tia là VFX; rig đặt xương ở con
  ngươi + sự kiện).
- Chiêu cuối: "**dơ 2 tay sang ngang, xoay liên tục quanh cơ thể như chong chóng** rồi **lao vào đập liên tục** vào đối thủ".
- die: "nó **rơi xuống, mắt tắt ngỏm, giáp rơi ra**".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3342/`: `info.json`, `att_goc.json`, `att_idle0.json`, `mo/idle0_0.jpg`, `mo/nhom_idle0.jpg`, `parts/`, `khung/`)

25 xương, 17 slot, 12 clip, 2333 khoá. Không IK, không path; **12 transform constraint** (dời theo xương `bone3`/`bone22`/`bone2`, trộn
0,15–0,65: các tấm giáp đi theo quả cầu một phần, nên quả cầu nhún thì giáp "lơ lửng" trễ theo). Con nhìn sang PHẢI, MỘT mắt.
**Mọi hình là mảnh cứng một xương, trừ quả cầu** (`shenti_01`: lưới có trọng số bone 0,79 / bone3 0,20) → kiểu "mảnh lơ lửng" như tượng
đá (skill mục 25): mảnh của mình là ô cứng đặt theo concept, hình bóng tự do.

Bảng mảnh (thứ tự vẽ sau → trước; "→" là vai trò trong thiết kế mình):
| thứ tự | slot | ảnh (px) | là gì | xương |
|---|---|---|---|---|
| 1 | `shoubi_02` | 45 × 50 | khúc tay XA (cục đỏ nhỏ nối cầu với nắm tay) → khúc tay lửa | bone15 / bone16 |
| 2 | `shou_02` | 74 × 93 | nắm tay đá XA (phải) → nắm tay giáp | bone17 |
| 3 | `jian_02` | 71 × 95 | tấm vai XA (dựng ở trên phải) | bone11 |
| 4 | `shenti_01` | 156 × 141 | **QUẢ CẦU** dung nham (lưới có trọng số) → **cầu lửa** | bone, bone3 |
| 5 | `yanjing_01` | 80 × 74 | **MẮT**: con ngươi đỏ + quầng kem hình sao → tròng vàng + con ngươi khe | bone18 |
| 6 | `tou_03` | 50 × 47 | tấm nhỏ dưới đầu mút phải của tấm đầu | bone7 |
| 7 | `tou_01` | 143 × 107 | **TẤM ĐẦU** lớn, đè chéo lên mép trên con mắt (mày cau) | bone5 |
| 8 | `tou_02` | 41 × 42 | tấm nhỏ dính trên cầu, bên trái mắt | bone6 |
| 9 | `shitou_03` | 98 × 68 | tấm dưới phải (dưới mắt) | bone9 |
| 10 | `shitou_04` | 110 × 71 | tấm dưới giữa (cùng xương với slot 11 `shitou_02`, đang tắt) | bone8 |
| 12 | `shitou_01` | 78 × 53 | tấm dưới trái | bone6 |
| 13 | `shoubi_01` | 44 × 50 | khúc tay GẦN | bone12 / bone13 |
| 14 | `jian_03` | 91 × 108 | tấm vai GẦN (to, ngả về sau, bên trái) | bone10 |
| 16 | `shou_01` | 81 × 104 | nắm tay đá GẦN (trái) | bone14 |

Hình phụ: `att_goc` có 15 hình (thêm một hình mắt khác: mắt chữ X dùng ở `die_01`, `floating_01`). Slot `jian_01`, `shitou_02` mặc định trống.

Clip của họ (tờ `khung/`):
| clip | dài | nội dung | dùng cho |
|---|---|---|---|
| idle_01 | 6,67 s | quả cầu lơ lửng nhún chậm, giáp trôi trễ theo, nắm tay chống đất | **idle** (gần như cũ + lửa lay) |
| run_01 | 0,60 s | lăn / nảy tới, nắm tay xoay vòng | **walk** |
| skill_01_1 | 1,13 s | vươn hai nắm tay sang hai bên, đấm thẳng ra trước 0,52–0,82, thu về | nền cho **attack** (thêm bay tới, nặng) |
| skill_01_2 | 1,13 s | dang tay, xoay giơ một nắm tay thẳng lên trời 0,52–0,82 rồi nện xuống | nền cho **skill** (phần đập) |
| skill_01_3 | 1,13 s | (biến thể đấm) | |
| skill_02 | 1,63 s | thu mình 0,15, cuộn tròn bay lên xoay 0,45–0,59, bung dang hai tay 0,74–1,34, về | nền cho **cast** (+ tia lửa từ mắt) |
| block_01, hit_01/02, stun_01 | | | **hit** |
| floating_01 | 1,5 s | bị hất tung, mắt X, rơi đáp | (dáng rơi cho die) |
| die_01 | 1,0 s | bật ngửa, lộn, mắt X, đổ xuống | nền cho **die** (thêm mắt tắt, giáp rơi ra bằng mảnh rời) |

## 3. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `mat_lua.py` (`mo`, `nhom`, `part_goc`), `mat_lua_bo_cuc.py` (sơ đồ bố cục 1536 × 1024 ở khung 0 idle, tỉ lệ 2,762 px / đơn vị
rig; lưỡi lửa vẽ bằng mã sau quả cầu), `build_mat_lua.py` (gói `gui_gpt/mat_lua_1/`).

Giữ của con gốc: bố cục quả cầu một mắt nhìn phải, tấm đầu đè chéo mép trên mắt, hai tấm vai dựng, ba tấm dưới ôm đáy cầu, hai khúc tay
ngắn, hai nắm tay to chạm đất (rig không có chân: **nắm tay làm chân luôn**).
Đổi: **quả cầu → cầu lửa sống** (ba vùng màu phẳng, ranh uốn như lưỡi lửa), **mắt → tròng vàng con ngươi khe dọc** (mắt rồng, "chiến"),
thêm **lưỡi lửa liếm ra ở khe giáp** (lớp mới sau giáp, sẽ rig lay riêng), giáp theo chất liệu của mình; nét vẽ tay tô phẳng.

Ba hướng giáp:
- `da_den` **A · đá vỏ chai đen tím** (sát con gốc): giáp #343040, nứt dung nham mảnh #EC5A2E, cầu lửa đỏ cam, con ngươi đỏ sẫm.
- `sat_ren` **B · sắt rèn có đinh tán**: giáp xám than #545660, đinh tán, dải mép nung cam #FA8C2E, cầu lửa cam vàng, con ngươi đen nâu.
- `tro_nui` **C · đá bọt xám tro**: giáp #96908C có lỗ rỗ, nứt cam, cầu lửa đỏ cam (tương phản mạnh nhất).

Tướng 1 đảo Hỏa (`quy_lava`) đã chọn đá nâu đỏ / đen nâu, nên cả ba hướng tránh tông đó.

Cả ba ra đúng bố cục ngay lượt đầu (`mat_lua_1/tai_ve/L1_da_den.png`, `L1_sat_ren.png`, `L1_tro_nui.png`; tờ so `mat_lua_1/so_concept.png`),
đã mở cho người dùng chọn 2026-11-13. Soi: đủ 14 mảnh, tấm đầu đè mép trên mắt, lửa ba lớp ngọn móc về sau, tô phẳng. C: nắm tay tròn
giống bàn chân thú có đệm; tấm đầu có một vệt sáng nhỏ trong vết nứt (bỏ khi gen mảnh). Quả cầu ở cả ba bị lửa và giáp che nhiều, chưa
đọc rõ là một quả cầu tròn.

## 4. Kế hoạch rig và clip (sau khi concept được duyệt)

- Rig = của họ (mọi xương, transform constraint nướng qua `chay.py sample`, trường `l`). Mảnh cứng một xương đặt theo concept; quả cầu
  dùng lưới của họ (`gan_goc`).
- Mảnh thêm: **lớp lửa** (2–3 lưỡi tách lớp, mỗi lưỡi chuỗi 2–3 xương con của `bone`, lò xo lệch pha), **mắt tắt** (đổi hình: tròng
  xám tro, không con ngươi) cho die / appear, **cầu tắt** (cầu than nguội) cho appear.
- appear: mọi tấm giáp nằm chồng trên đất (bộ giáp bẹp), cầu tắt → mắt sáng lên, cầu phồng to → hai khúc tay + nắm tay trồi ra → cả con
  bay lên vào dáng idle.
- attack: dựa `skill_01_1`, lấy đà lùi + thu nắm tay, LAO tới (`lunge`), đấm một nắm tay xa nhất, khựng, về.
- cast: `skill_02` (thu mình, bay lên xoay, bung dang tay) + giữ dáng bung, xương `mieng` ở con ngươi, sự kiện `phun` / `het_phun`.
- skill: dang hai tay ngang → hai nắm tay quay vòng quanh thân như chong chóng (xoay nhanh dần) → lao tới (`lunge`) đập liên tục (nhiều
  `hitTimes`) → về.
- die: dựa `die_01` / `floating_01` rơi xuống, mắt tắt dần, các tấm giáp rời ra rơi xuống đất (slot `~2` trên xương rời như tượng đá).
- VFX ngoài rig: tia lửa từ mắt (cast), vệt xoáy lửa quanh thân (skill), bụi đá + tia lửa toé lúc đấm.

## 5. Mảnh và rig (2026-11-13, người dùng chọn A → `mat_lua_1/tai_ve/L1_duyet.png` = `L1_da_den.png`)

Trình tự: `build_mat_lua.py manh` (năm file `luot_2_manh_A..E.txt`) → `gen.py` từng tờ → `mat_lua_manh.py lam` → `mat_lua_rig.py`
(qua `quai/khoa.py nang`) → `mo_xe/thu_xem.py <rig/xem.html>` → `chay.py sheet` rig mình (`rig/that/`).

- **Năm tờ "đúng chỗ, đúng cỡ"** (mỗi tờ giữ vài mảnh không chồng nhau, vẽ đủ phần khuất; 75–127 giây một tờ): A cầu lửa tròn đủ (không
  mắt) + nắm tay gần; B tấm đầu + tấm dưới trái + nắm tay xa; C hai tấm vai + tấm dưới phải + tấm nhỏ cạnh mắt; D mắt tròn đủ + hai khúc
  tay lửa; E lửa sau lưng (đáy tròn nấp sau cầu) + hai giọt lửa + tấm dưới giữa + tấm nhỏ dưới mép phải tấm đầu. Ghép lại lệch concept
  3,9% điểm (`manh/_so_ghep.png`); khe giữa tấm dưới trái và tấm dưới giữa lộ lửa mảnh hơn concept một chút.
- `mat_tat`, `cau_tat` đổi màu bằng mã (`doi_mau`: giữ vân sáp, giữ nét mực).
- **Rig**: đủ xương của họ (thêm root + move), mẫu khung `l` nướng 12 transform constraint. Mảnh cứng đặt ở thế giới DÁNG IDLE GIÂY 0
  (concept dựng từ dáng đó) và tính toạ độ gắn theo ma trận xương ở dáng đó (`gan_cung`, `gan_luoi`), vì dáng gốc của họ lệch idle.
  Cầu và hai khúc tay: lưới ô 7×7, trọng số nội suy từ lưới của họ (`trong_so_ho`). Lửa: lưới `luoi_vung`, xương `lua` + 7 lưỡi × 2 đốt
  (trọng số theo khoảng cách tới sống lưỡi), lay lệch pha + lò xo; hai giọt lửa trên `giot1/2`. `mieng` ở con ngươi.
  Thứ tự vẽ theo concept: vai xa đè mép phải tấm đầu, tấm dưới giữa đè tấm dưới trái, nắm tay xa trước tấm dưới phải.
- Kết quả `mat_lua_1/rig/`: 45 xương, 19 slot, 464 đỉnh, 8 clip, atlas 712 × 768, `.atomik` 217 KB; chiều cao game 245 (đỉnh tấm giáp
  đầu, không tính lửa). Mọi clip nối về idle 0 px, appear khung đầu trống, die khung cuối trống; nạp lại `.atomik` lệch ≤ 0,24 px; góc
  nhảy lớn nhất ở 60 khung/giây (runtime thật): cú bung tay của cast 54°, cú đấm 35°, còn lại ≤ 23°.

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| appear | 2,20 s | đống giáp nằm đất, cầu nguội ló ra, mắt tắt → mắt SÁNG 0,4–0,65 → cầu PHỒNG, giáp bung về chỗ 0,62–1,05, lửa bùng 0,75 → nắm tay TRỒI từ giữa ra 0,95–1,3 (khúc tay lửa hiện sau) → BAY lên dáng nghỉ 1,3–1,75 | sang 0,40; xong 0,95; bay 1,30 |
| idle | 6,67 s lặp | nguyên idle_01 + lửa lay, giọt lửa nhấp nhô | |
| walk | 0,60 s lặp | nguyên run_01 + lửa ngả về sau | |
| attack | 1,30 s | lấy đà kéo nắm tay gần ra sau (skill_01_1) + lùi; BAY tới 0,36–0,56 (move 330); ĐẤM 0,56–0,62 (cú vung một khung của họ trải ba khung); rung, khựng; bay lùi về | trung 0,62 |
| cast | 2,10 s | skill_02: thu mình, cuộn bay lên, BUNG dang tay (cú bật giãn 0,60–0,74); giữ dáng bung tới 1,78, mắt phồng 14%, rung nhẹ | tu 0,70; phun 0,82; het_phun 1,78 |
| skill | 2,90 s | dang tay (dáng bung skill_02) → hai cánh tay QUAY CHONG CHÓNG 6 vòng quanh tâm HÌNH quả cầu (nắm tay kéo sát, bán kính 120), tấm vai quay bù đứng yên → LAO tới 1,05–1,25 (move 360), đập liên tục 5 nhát → chậm dần, lùi về 2,15–2,45 | xoay 0,30; trung 1,30 / 1,48 / 1,66 / 1,84 / 2,02 |
| hit | 0,50 s | hit_01; lúc họ đổi mắt chữ X thì mắt mình nheo (ép dọc 35%) | |
| die | 2,25 s | giật ngửa, mắt TẮT, lửa lụi, cầu nguội, rơi xuống đất; từng tấm giáp + hai nắm tay RỜI ra 0,42–1,0 (bay chéo, quay, chạm đất, nảy), nằm yên; mờ dần 1,80–2,25 | tat 0,12; roi 0,42; cham_dat 0,75 |

Bài học: xương quay nhiều vòng (chong chóng) phải giữ góc riêng LIÊN TỤC (`dat_tg(..., them=g)`), đừng quy về một vòng; và bước hoà
cuối clip `hoat.khop_cuoi` nay chọn cùng vòng 360° trước khi trộn (trước đó tay quay ngược 6 vòng trong 0,2 s cuối). Tâm quay lấy tâm
HÌNH quả cầu: gốc xương `bone` thấp hơn tâm cầu 39 đơn vị (bản đầu nắm tay văng xa khỏi thân ở nửa dưới vòng quay).

CHƯA làm: VFX (tia lửa từ mắt, vệt lửa xoáy quanh thân lúc chiêu cuối, bụi đá lúc đấm và lúc giáp rơi), tên, id, suất trong game.

## 6. Dạng 2 (người dùng 2026-11-13: "ok nhìn ổn, con này là dạng 1, bạn làm tiếp dạng 2 to hơn, chiến hơn")

Rig và clip dạng 1 coi như được duyệt. Dạng 2 làm trên CÙNG rig, cùng clip; mọi script đọc dạng ở biến môi trường **ML_DANG** (1 | 2;
thư mục `inbox/mat_lua_<k>`, `gui_gpt/mat_lua_<k>`). Khung concept ↔ thế giới con gốc đo ở dạng 1 (`mat_lua_1/manh/khop.json`), dạng 2
dùng lại.

- **Tỉ lệ trước, concept sau**: `ML_DANG=2 mat_lua_rig.py bo_cuc` dựng HÌNH BỐ CỤC bằng da dạng 1 ở khung 0 idle, mỗi mảnh phóng
  quanh tâm của nó (nắm tay quanh điểm chạm đất): nắm tay ×1,30, tấm vai ×1,22, tấm đầu ×1,15, tấm nhỏ ×1,10–1,15, tấm dưới ×1,12, lửa
  ×1,22; cả con thu 0,86 cho vừa khung concept (trong game dạng 2 to hơn nhờ cỡ tướng). → `mat_lua_2/mau/bo_cuc.png`. Lưu ý: đổi tỉ lệ
  xương ở dáng gốc KHÔNG làm mảnh to ra (mảnh đặt theo toạ độ concept), nên tỉ lệ chỉ áp lúc dựng hình bố cục.
- Bán kính quay chong chóng nay tính theo cỡ quả cầu và cỡ nắm tay thật (`r_quay = bán kính cầu + 0,72 × nửa cạnh nắm tay`), để nắm tay
  dạng 2 to hơn vẫn quay sát mép cầu.
- Concept (`build_mat_lua.py dang2` → `gui_gpt/mat_lua_2/luot_1_concept_<hướng>.txt`; ảnh mẫu: hình bố cục, concept dạng 1, Voọc Tướng,
  bản đồ). Chung cho ba hướng (đề xuất của Claude): giáp đen hơn (#2A2430), vết nứt dung nham dày có lõi vàng; lửa cao, nhiều lưỡi hơn,
  lõi vàng nhạt; mắt lộ ~4/5, tròng hổ phách, con ngươi khe đen đỏ hẹp hơn; sừng, gai, nanh, vuốt mọc LIỀN trên mảnh của nó (giữ đủ
  mảnh như dạng 1).
  - `sung` **A · mũ sừng chiến**: tấm đầu có hai sừng cong lớn vút ra sau; tấm vai có gai tù; nắm tay có ba gai đá trên đốt.
  - `ham` **B · hàm dung nham**: ba tấm dưới thành hàm đá lởm chởm có nanh lớn dưới con mắt; tấm đầu có gờ mày và một gai giữa; nắm tay
    có vuốt đá.
  - `ca_hai` **C · bạo chúa**: gộp A và B, lửa cao nhất.

Lượt 1 dạng 2 ra cả ba (`mat_lua_2/tai_ve/L1_sung.png`, `L1_ham.png`, `L1_ca_hai.png`; tờ so `mat_lua_2/so_concept.png` kèm dạng 1), đã
mở cho người dùng chọn 2026-11-13. Soi: cả ba giữ bố cục và đủ mảnh; sừng, gai, nanh, vuốt mọc liền trên mảnh. A và C để tấm đầu che
mắt nhiều hơn dặn (còn ~2/3); B lộ mắt rõ nhất. Vuốt ở B, C mọc dưới đáy nắm tay như móng chân thú (lúc đấm vẫn là mặt trước).

Người dùng chọn B, dặn "lấy dạng b nhưng bỏ gai ở tay đi" (vuốt đá ở hai nắm tay) → lượt 1b (`gui_gpt/mat_lua_2/luot_1b_tay_tron.txt`:
vẽ lại y hệt `L1_ham.png`, chỉ đổi hai nắm tay thành khối giáp trơn có đốt tròn) → `tai_ve/L1b_ham_tay_tron.png` = `L1_duyet.png`.

Cùng lúc người dùng sửa thứ tự lớp (chụp rig dạng 1): **"phần giáp vai tay phải layer phải nằm dưới giáp đầu và thân"** → tấm vai XA
về sau quả cầu và tấm đầu như con gốc (cả hai dạng; dạng 1 xuất lại).

**Mảnh dạng 2** (`build_mat_lua.py manh 2`: 6 tờ A–F vì mảnh dạng 2 to, chồng sát hơn): A cầu lửa; B tấm đầu có gai + hai nắm tay; C hai
tấm vai + tấm hàm phải; D mắt + hai khúc tay lửa (ẩn sau vai, nắm tay ở dáng nghỉ); E lửa + giọt + tấm hàm giữa + tấm nhỏ dưới mép phải
tấm đầu; F tấm nhỏ cạnh mắt + tấm hàm trái. Ghép lại lệch concept 6,8% điểm. Ba tấm dưới của rig gốc (bone6, bone8, bone9) thành ba tấm
hàm (trái, giữa có hai nanh, phải). Khúc tay GẦN cũng về sau quả cầu (bản đầu lúc quay chong chóng nó vắt ngang trước mắt và hàm).

**Rig dạng 2** (`ML_DANG=2 mat_lua_rig.py`): cùng xương, cùng clip; concept dạng 2 vẽ trên hình bố cục đã thu 0,86 quanh gốc thế giới nên
khung concept dạng 2 dùng tỉ lệ `s × 0,86` (mảnh về cỡ thật, khớp xương). Mạnh hơn dạng 1: chiêu cuối quay 8 vòng, đứng đập lâu hơn
0,4 s, 7 nhát; rung lúc đấm trúng ×1,5; mắt phồng 20% lúc bắn tia. Appear: đống giáp tính theo TÂM MẢNH và kê không lún đất (mảnh dạng 2
nằm xa gốc xương), quả cầu kê cao 0,74 cho mắt tắt ló ra.
Kết quả `mat_lua_2/rig/`: 45 xương, 19 slot, 713 đỉnh, 8 clip, atlas 904 × 984, `.atomik` 278 KB; chiều cao game 273 (thân tấm đầu,
không tính gai giữa và lửa). Mọi clip nối về idle 0 px, appear khung đầu trống, die khung cuối trống; nạp lại `.atomik` lệch ≤ 0,23 px;
góc nhảy lớn nhất (runtime thật, 60 khung/giây): bung tay của cast 54°, đấm 35°, lửa bùng lúc appear 32°, còn lại ≤ 24°.

CHƯA làm: clip `evolve` (dạng 1 → dạng 2, gộp bản nhẹ dạng 2 vào rig dạng 1 như Gạc Đá), VFX, tên, id, suất trong game.

Người dùng xem walk dạng 2 (2026-11-13): **"khi walk tay bên kia phải nằm dưới thân chứ"** → nắm tay XA về sau quả cầu như con gốc (thứ
tự bên xa: khúc tay, nắm tay, tấm vai, rồi mới tới quả cầu), cả hai dạng; cắt và xuất lại hai dạng (nối clip vẫn 0 px). Bài học: thứ tự
lớp của con gốc là để đúng ở MỌI clip (tay xa vung vào trong thân lúc đi); concept chỉ vẽ dáng đứng, đừng theo concept mà đưa mảnh bên
xa lên trước.

## 7. Vào game (người dùng 2026-11-13: "ổn đấy, thay vào game đi"; chọn "đổi id mới" và tên "Hỏa Nhãn")

- Thay suất 2 đảo Hỏa (ải 5 "Suối Dung Nham"): **khong_lo** (Khổng Lồ Lửa, 3 dạng) → **hoa_nhan**, tên Hỏa Nhãn, danh hiệu "Mắt lửa
  giáp nham", dòng "Dòng Hỏa Nhãn"; dạng 1 **Nhãn Than** (`hoa_nhan_1` ← `mat_lua_1.atomik`, cỡ 0,92), dạng 2 **Hỏa Nhãn** (`hoa_nhan_2`
  ← `mat_lua_2.atomik`, cỡ 1,1). Thẻ (tên Claude đặt): `hoa_nhan_skill` Hỏa Nhãn Xạ, `hoa_nhan_ult` Quyền Chong Chóng, `hoa_nhan_pas`
  Giáp Nham; số, hiệu ứng, biểu tượng, chỉ số, độ hiếm giữ của Khổng Lồ Lửa.
- Clip `evolve` thêm vào dạng 1 (`mat_lua_rig.py`, ML_DANG=1 tự dựng bản nhẹ dạng 2 `ML_NHE=1` rồi gộp): Nhãn Than thụp xuống gồng (mắt
  và cầu phồng, rung, lửa bùng), tan; Hỏa Nhãn hiện, bùng lửa, dang tay, về idle dạng 2 (khung cuối lệch 0 px). `.atomik` dạng 1 297 KB.
- Script dữ liệu: `quai/doi_hoa_nhan.py` (mẫu doi_gac_da.py; `--kiem` chạy thử: 16 file, bước chuyển bản lưu [9] = MigrateHoaNhan,
  saveVersion 9 → 10). VFX trận tạm dùng bảng của Khổng Lồ Lửa (HatLua theme "nham", StageView ("nham", "phun_nham")), chỉ đổi khoá id.
- Thứ tự Unity (theo Gạc Đá, mục 5d tuong_da_ghichu): dừng Play → chạy script → `manage_asset move` prefab khong_lo → hoa_nhan và
  Resources/khong_lo_1, 2 → hoa_nhan_1, 2 (giữ GUID), xoá khong_lo_3 → chép .atomik + chân dung → refresh → Nhập dữ liệu → Gắn dạng
  .atomik → menu golden (Đảo 70 ải sinh lại; golden islands/roster/cardtext/zones; theo danh sách tướng; sim) → `quai/golden_ghep.py` →
  nạp lại domain → EditMode.

**ĐÃ VÀO GAME (2026-11-13 trưa).** Người dùng cho dừng Play; báo bốn phiên khác trước (không phiên nào vướng; assets-ad có thay đổi
chưa commit ở heroes / stages / golden: script sửa đè lên bản trên đĩa nên giữ nguyên).
- `quai/doi_hoa_nhan.py` (ghi thật, 16 file): saveVersion 9 → 10, `Migrations[9] = MigrateHoaNhan` (HoaNhanMap khong_lo → hoa_nhan),
  CoreGoldenTests 10; IslandGen Intro(5, "hoa_nhan", "Suối Dung Nham"); HatLua / StageView / HoaFxTour đổi khoá id.
- Unity (MCP 8080, `scratchpad/mcp.py`): `manage_asset move` prefab khong_lo → hoa_nhan, Resources/khong_lo_1, 2 → hoa_nhan_1, 2 và ba
  file bên trong (công cụ báo success false nhưng đã đổi, giữ GUID); xoá khong_lo_3; chép mat_lua_<k>.atomik + chan_dung.png (512) đè
  lên; refresh; Nhập dữ liệu; Gắn dạng .atomik (log: hoa_nhan_1 90 xương 9 clip, hoa_nhan_2 45 xương 8 clip, prefab giữ 2 dạng).
- Golden: "Đảo 70 ải: sinh lại" (stages.json không đổi); "golden islands, roster, cardtext, zones" (roster: số dạng 3 → 2 và phần migrate
  ghi hoa_nhan; test qua); "theo danh sách tướng" (không đổi thêm); "golden sim" + `golden_ghep.py` (sim ải hoa 75). Bản sao lưu trước khi
  tính: `scratchpad/sao_luu`.
- EditMode 102/103 (chỉ hỏng PrefabOnlyTests.MaRuntime_KhongSinhDoVat có từ trước). Chụp thử `Library/PokiHeroShots/hoa_nhan_atomik_1/2.png`:
  đủ clip, hình đúng.
- CHƯA: VFX riêng (đang dùng bảng lửa / dung nham của Khổng Lồ Lửa: theme "nham", StageView ("nham", "phun_nham")); chưa xem trong trận
  (tia lửa từ mắt có đúng chỗ `muzzle` không, chiêu cuối lao tới đúng đối thủ); chưa commit.

## 8. VFX (người dùng 2026-11-13: "fx bạn cứ tự bổ sung nếu thiếu")

- `Assets/01 Script/Game/Battle/HatNhan.cs` (partial HatLua), nối vào `PlayMana` / `PlayUlt` / `HoldOf`; `StageView.FireFx` hoa_nhan =
  ("tia_mat", "quyen_xoay"); chủ đề `Themes["hoa_nhan"]` đổi sang bảng "lua" (lửa đỏ cam lõi vàng như rig; "nham" của Khổng Lồ Lửa ra màu
  nâu), mảnh văng "giap" màu giáp đen tím.
  - **tia_mat** (chiêu mana, phát ở khung `phun` 0,82): con ngươi loé; TIA lửa liền từ `mieng` tới thân đối thủ (mảng liền MRibbon 4 lớp:
    mực, cam, vàng cam, lõi kem; nửa bề ngang 0,11 × chiều cao đối thủ, mép lượn), lưỡi lửa bám dọc tia, con ngươi phụt lửa liên tục, chỗ
    trúng chớp nổ rồi toé lửa + tia lửa liên tục; 0,9 s; HoldOf 1,0 (clip giữ dáng bung 0,96 s sau khung nhả).
  - **quyen_xoay** (chiêu cuối, phát ở khung trúng đầu 1,30): lưỡi lửa bay vòng elip quanh đối thủ (nửa xa sau, nửa gần trước) + 6 chớp nổ
    cách 0,18 s ở thân đối thủ (so le), nhát cuối to nhất + vòng lửa dưới chân, khói tan.
- Sửa rig khi soi trong trận (tour "Đảo Hỏa: hạt lửa chiêu mana, chiêu cuối", ảnh Temp/PokiShots/hoa_fx/hoa_nhan_*):
  - dạng 2 quá to, tràn mép phải sân: con bè ngang (rộng 1,54 × chiều cao game) → khai chiều cao hiệu dụng ≥ bề rộng / 1,30 (`MAX_W`):
    dạng 2 khai 323 thay 273; tiến hóa dùng chiều cao hiệu dụng (dạng sau co 0,758 trong rig gộp);
  - chiêu cuối bị CẮT DỌC thân phía trước: clip tự dời `move` 360 (> 1 lần chiều cao) nên thân ra khỏi khung sticker (rộng 3,4 lần chiều
    cao); game tự nắn quãng lao (AolaSticker.Lunge) nên quãng trong clip chỉ cần nhỏ → đòn thường 0,6 × chiều cao, chiêu cuối 0,5 ×.
- Lần đầu biên dịch HatNhan.cs trúng lúc người dùng vừa vào Play (Unity nạp lại assembly giữa phiên); đã báo các phiên. Các lần sau dừng
  Play (phiên Play do tôi mở cho tour) rồi mới biên dịch.
- EditMode 102/103 (vẫn chỉ PrefabOnlyTests cũ). Đã xem trong trận ở dạng 2 (tour dùng sao cuối); dạng 1 và hộp chi tiết tướng chưa chụp.
