# Kỵ sĩ cổ đại bị nguyền (`ky_nguyen`): tướng 8 đảo Kim

Bắt đầu 2026-11-16 (máy ổ C). Con gốc của rig: **`monster_3642`** (hiệp sĩ giáp trắng viền vàng RỖNG RUỘT, không chân, lơ lửng; áo choàng tím
rách, tinh thể tím mọc trên giáp, chùm lông vũ trên mũ, kiếm bản rộng lưỡi mẻ có ngọc lam, đá vụn bay dưới thân; game tham khảo, kho
`D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `run_01`). Xương, lưới, chuyển động gốc là của nhà phát hành game
đó (như aola): dùng nội bộ, không đăng công khai. Hình là của mình. Suất 8 đảo Kim = ải 50 "Thành Ba Kiếm" (có boss), id game hiện là
**`tam_kiem`** (Tam Kiếm). Mã làm việc `ky_nguyen`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-16)

- Concept: "**kĩ sĩ cổ đại bị nguyền rủa bất tử** như kiểu Mordekaiser (LoL); **giáp sắt đen rỉ sét**, ở trong là **ngọn lửa aura xanh lá
  tỏa ra** kiểu Mordekaiser / Viego". (Claude: chỉ lấy ý "giáp rỗng + lửa linh hồn xanh"; prompt không nhắc tên nhân vật / game nào.)
- appear: "**bộ giáp rỗng nằm dưới đất, mắt sáng lên màu xanh rồi bắt đầu lơ lửng thành hình**".
- idle / walk: "**giống họ**".
- Đánh thường: "**lao tới dùng kiếm chém**".
- Chiêu mana: "**giơ kiếm lên trời, gọi những linh hồn đồng đội từ thời xưa dạng linh hồn xanh lao tới đánh kẻ thù**".
- Chiêu cuối: "**đoạn đầu giống skill_03_1, đưa tay kia lên vuốt lên trên, thanh kiếm cùn hút những khí xanh xung quanh (linh hồn xanh), được
  khôi phục bằng một loại vật chất linh hồn màu xanh lá thành một thanh kiếm hoàn chỉnh, tỏa aura linh hồn xanh; kiếm RẤT DÀI; chém một phát
  thật mạnh xuống đối thủ, epic, impact**".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3642/`: `info.json`, `att_goc.json`, `att_idle0.json`, `khung/`, `mo/`, `parts/`; script `ky_nguyen.py`)

125 xương, 70 slot (61 hình bật ở idle 0), 12 clip, 12 370 khoá. **FK thuần**: không IK / path / physics; một transform `all2` mix 0 (không
tác dụng). Con quay PHẢI (ba phần tư), KHÔNG CHÂN: phần dưới là áo choàng rách. Ảnh mẫu `inbox/ky_nguyen_1/mau/goc_ca_con.png` 1536 × 1024:
0,684 px / đơn vị. Tên slot `y_` = tay GẦN (bên trái hình, cầm kiếm), `z_` = tay XA (bên phải hình, bàn tay vuốt xoè).

Chuỗi xương mềm: áo choàng `bone68/69/70` (3 chuỗi × 5 đốt, lưới 58 đỉnh), chùm lông vũ `bone26..30` (5 chuỗi × 3 đốt), vạt trước `bone40 →
bone41..41d`, sợi sau gáy `bone33..39` (+ `b`), đá vụn `bone62..66` (con của `jiao`).

| nhóm | slot (thứ tự vẽ) | là gì |
|---|---|---|
| áo choàng | `P_pifeng01` (2) | áo choàng lớn sau lưng, rách, rủ xuống trái (lưới trọng số 3 chuỗi) |
| đá | `P_shitou00..04` (4–8) | 5 viên đá lơ lửng dưới ngực |
| tay xa | `P_y_dabi` (9, khối tối), `P_z_xiaobi` (12, cẳng tay quấn băng trắng), `P_z_shou` + `P_z_shouzhi00..07` (13–21, bàn tay vuốt tối 5 ngón) | |
| thân rỗng | `P_shenti_1` (25, khối tối thân), `P_shenti_9` (41, dải tối dưới vai), `P_z_dabi` (52, khối tối bắp tay gần), `P_shenti_2..8` (34–40, sợi tối sau gáy, lưới 2 xương) | khoảng rỗng của bộ giáp |
| mũ | `P_tou` (33), `P_yanse` / `P_yanse01` (31–32, khe mắt), `P_yumao00..04` (26–30, chùm lông vũ) | |
| giáp | `P_jianjia` + `P_jianjia2` (53, 51, giáp vai gần lớn), `P_xiongjia01` + `00` (43, 45, giáp ngực), `P_pifeng00` (42, vạt vải trước) | |
| tay gần | `P_y_xiaobi` (62, cẳng tay giáp có ấn tím), `P_y_shou` + `P_y_shouzhi00..04` (58–61, 48–49, nắm tay trắng cầm kiếm) | |
| kiếm | `P_jian` (50) | 430 × 246, một xương `bone23`; lưỡi mẻ ở mũi |
| gai | `P_ci00..12` (11, 22–24, 47, 54–57, 63–66) | tinh thể tím (mảnh cứng một xương) |
| khói | `P_yanwu` | khói đen (die) |

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho (dự kiến) |
|---|---|---|---|
| `idle_01` | 10,00 | lơ lửng, áo choàng bay | **idle** (giống họ) |
| `run_01` | 1,33 | lướt tới | **walk** (giống họ) |
| `skill_01` | 1,00 | xoay người giơ kiếm qua đầu (0,18–0,27), CHÉM vòng xuống (0,36–0,55), về | nguồn **attack** (lao tới + chém) |
| `skill_02` | 1,73 | giơ kiếm thẳng đứng (0,16–0,32), vung, nhảy xoay chém qua đầu, về | (dự phòng: giơ kiếm lên trời cho chiêu mana) |
| `skill_03_1` | 2,73 | DỰNG KIẾM THẲNG TRƯỚC MẶT, tay xa GIƠ LÊN (0,25–1,24), chém ngang (1,49–1,74), đâm tới (1,99–2,24), về | đoạn đầu cho **chiêu cuối** |
| `skill_03_2` | 2,73 | như 03_1 tới 1,74, rồi GIƠ KIẾM THẲNG LÊN TRỜI qua đầu (1,99–2,24) | nguồn **cast** (giơ kiếm lên trời) |
| `skill_03_3` | 2,73 | như 03_1 tới 1,74, rồi CẮM / BỔ KIẾM THẲNG XUỐNG (1,99–2,48) | đoạn chém dọc cho **chiêu cuối** |
| `die_01` | 2,00 | khói thoát ra, bộ giáp ĐỔ SỤP thành đống dưới đất (1,64–2,00) | **die**; chạy NGƯỢC làm **appear** (đống giáp → lơ lửng ráp lại) |
| `hit_01/02`, `block_01`, `stun_01` | | | **hit** = hit_01 |

## 3. Concept lượt 1 (Claude đề xuất ba hướng, CHỜ người dùng chọn)

Gói `gui_gpt/ky_nguyen_1/` (`ky_nguyen_da.py ca_con`, `concept`; mô tả từng mảnh và ba hướng ở `ky_nguyen_huong.py`). Ảnh mẫu 1 = hình cả con
gốc `mau/goc_ca_con.png` (khung 0 idle); ảnh 2 = sói giáp sắt (tướng 6 đảo Kim: nét, tô sắt sẫm phẳng); ảnh 3 = pháp sư lửa (khoảng tối trong
mũ trùm với mắt sáng, lửa phẳng có viền mực). Mọi hướng giữ dáng lơ lửng quay phải, chỗ và cỡ từng mảnh; giáp sắt đen rỉ; lửa linh hồn xanh lá
tô phẳng hai tông, KHÔNG quầng sáng (aura tỏa ra là việc của lớp VFX trong game); kiếm GÃY lưỡi (để chiêu cuối phục hồi). Đổi dáng mảnh
nhận diện:
- `tai_ve/L1_A.png` **lửa linh hồn trong giáp**: khoảng rỗng thành lửa xanh; mũ thùng khe chữ thập; lông vũ thành chùm lửa xanh; gai tinh thể
  thành gai sắt rỉ; giáp vai ba tấm mép răng cưa; giáp ngực nứt lộ lửa; áo choàng đen than, mép rách thành lưỡi lửa; đá thành mảnh giáp vụn.
- `tai_ve/L1_B.png` **hồn ma bóng tối**: khoảng rỗng đen xanh thẫm, lửa liếm ở mép; gai tinh thể thành lưỡi lửa xanh phụt ra khe giáp; mũ hai
  sừng, khe ngang; lông vũ thành bờm lửa ma; viền đồng xỉn; áo choàng xanh rêu thẫm.
- `tai_ve/L1_C.png` **vua chiến trận cổ**: rỉ nặng, còn vệt viền vàng sờn; mũ vương miện gai, khe dọc; lửa bốc từ trong vương miện; gai tinh
  thể thành mũi tên gãy + giáo gãy cắm trên giáp; áo choàng đỏ rượu phai.

Kết quả (Codex, 97–124 s mỗi tờ, KHÔNG bị từ chối dù đính ảnh con gốc làm ảnh 1): khớp hình bóng con gốc (`ky_nguyen_da.py so_goc` →
`mau/_so_goc.png`) A 0,689, B 0,763, C 0,596. Lệch chung: lưỡi kiếm ngắn hơn (do dặn gãy 2/3, cố ý), áo choàng phần dưới trái và đoạn giữa tay
gần với ngực ngắn hơn; C phóng to và mũ cao hơn. Mảnh sẽ gen theo khung từng part của rig nên bố cục được nắn lại ở bước đó. Trang so:
`inbox/ky_nguyen_xem_concept.html`. CHỜ người dùng chọn (Claude nghiêng về B: khớp bố cục nhất, lửa phụt ra khe giáp làm aura sẵn).

## 4. Kế hoạch clip (dự kiến, làm sau khi chốt concept)

| clip | nguồn | ý |
|---|---|---|
| idle | idle_01 | giống họ |
| walk | run_01 | giống họ |
| appear | die_01 chạy NGƯỢC | đống giáp nằm đất (khung cuối die) → mắt bật sáng xanh (sự kiện `mat_sang`) → các mảnh nhấc lên lơ lửng ráp lại → dáng idle 0 |
| attack | skill_01 | lao tới (`move`), giơ kiếm qua đầu, chém vòng xuống (`chem`) |
| cast | skill_03_2 (đoạn giơ kiếm lên trời) | giơ kiếm thẳng lên trời, giữ; sự kiện `goi` → code thả các linh hồn đồng đội xanh lao tới đánh (VFX + code lái) |
| skill | skill_03_1 (0–1,24) → skill_03_3 (bổ dọc) | dựng kiếm trước mặt, tay xa vuốt lên; kiếm cùn hút linh hồn xanh (VFX); ĐỔI ẢNH kiếm gãy → kiếm hồn xanh RẤT DÀI (mảnh riêng gen sau); giơ cao rồi bổ một nhát cực mạnh xuống (`chem`), khựng, rung, chớp |
| hit | hit_01 | |
| die | die_01 | khói xanh thoát, giáp đổ sụp |

**Người dùng chọn C** (2026-11-16) → `tai_ve/L1_duyet.png`.

## 5. Mảnh (`ky_nguyen_manh.py`; gói `gui_gpt/ky_nguyen_1/luot_2_*`, `luot_3_luoi_hon.txt`; Codex đạt lượt đầu cả 8 tờ, không bị từ chối)

- `can`: căn concept lên hình con gốc (IoU 0,712; concept to hơn 1,09 lần, dời −25, +12 px) → `mau/can.json`.
- **LIEN** khoảng rỗng (thân tối `P_shenti_1`, dải dưới vai `P_shenti_9`, hai bắp tay tối `P_z_dabi`, `P_y_dabi`) = một hình liền đen xanh có vài lưỡi
  lửa xanh ở mép trên → `tai_ve/N_lien.png` → nướng vào khung từng part qua lưới.
- **K1–K4** giữ hình bóng gốc (tờ = mảnh gốc phóng to, IoU 0,89–0,98): áo choàng + vạt trước (đỏ rượu viền vàng sờn), giáp vai (vạt lá thành mép sắt
  gãy), giáp ngực (vết chém lửa xanh), cẳng tay giáp (ấn Ø xanh), giáp tay xa, năm lông vũ → năm lưỡi lửa xanh (bám chuỗi xương nên tự uốn), bảy
  sợi sau gáy → lửa xanh nhỏ, nắm tay + năm ngón, bàn tay xa + bảy ngón (găng sắt đen). Vùng ảnh dùng chung (`P_jianjia` của hai slot) lấy theo
  slot có lưới lớn. Khói đen `P_yanwu*` của họ bỏ (die làm khói hồn bằng VFX).
- **KT** gai tinh thể → giáo gãy (`P_ci07`), mũi giáo xuyên ngực (`P_ci08`), tám mũi tên gãy, ba dằm tên; đá → ba mảnh khiên vỡ + hai đầu mũi tên.
  Tờ vẽ từng mảnh theo HƯỚNG THẾ GIỚI ở khung 0 idle, ghi đầu cắm (gần gốc xương) / đầu ngọn cho GPT; mảnh cứng một xương, ô 4 đỉnh mới (`moi.json`).
- **R1** mũ vương miện (khe mắt tối, không mắt, không lửa) + kiếm gãy đủ chuôi, gen đúng chỗ trên concept; mũ đặt theo phép căn, kiếm xoay −3,5°
  cho trục trùng kiếm gốc và dời nắm tay concept về nắm tay rig. **Mắt** cắt thẳng từ concept bằng mã → slot riêng `P_mat` trên xương mũ.
- **Lưỡi hồn** (`luot_3_luoi_hon.txt`): kiếm gãy của mình nằm ngang ở trái tờ, GPT vẽ lưỡi vật chất linh hồn xanh mọc tiếp từ chỗ gãy dài ~3 lần kiếm
  (`tai_ve/H_kiem.png`); mã cắt phần bên phải chỗ gãy → `manh/luoi_hon.png` (dài 1606 đơn vị).

## 6. Rig + clip (`ky_nguyen_rig.py` → `inbox/ky_nguyen_1/rig/`, không theo git; `KN_GOC=1` dựng bằng da gốc ra `rig_goc/`, chỉ để soi)

129 xương (125 của họ + `move`, `mieng` ở mũi kiếm gãy, `luoi_hon` ở chỗ gãy, `mui_hon` ở mũi lưỡi hồn), 97 slot, 800 đỉnh, 8 clip, 16 sự kiện,
`.atomik` 373 KB (ảnh mảnh 0,6 px / đơn vị: `KN_PX`), chiều cao 1106; mọi clip nối về khung 0 idle 0 px.
- Thứ tự vẽ của họ đổi gần như mọi khung → slot di động nhân bản theo chỗ chèn (như `quy_dao_rig`); `P_mat` đi theo từng bản của `P_tou`,
  `P_jian_hon` theo từng bản của `P_jian`.
- `skill_01` lấy mẫu thêm 120 khung/giây (`<SXS>/scan/monster_3642/sample_120.json`): kiếm chỉ chĩa tới trước ở 0,36 s (giữa hai khung 30/giây).
- Clip: idle 2,0 s (chu kỳ gốc của idle_01 10 s, hoà 0,25 s cuối về khung 0); walk = run_01; hit = hit_01; die = die_01 (mắt tắt 0,25–0,70,
  `hon_thoat`, `nga`) + mờ; appear 2,65 s = die_01 chạy ngược (đống giáp, `mat_sang` 0,40 nhấp nháy, `bay_len` 0,75, ráp xong `rap` 2,30; vạt trước
  làm trơn ±0,08 s); attack 1,12 s = skill_01 (nhát bổ 0,33 → 0,375 giãn ra 0,10 s) + lao, `trung` 0,467; cast 1,85 s = skill_03_2 1,70 → 2,73 (giữ
  kiếm trên trời 0,62–1,40, `goi` 0,70, `trung` 1,05); skill 3,85 s = skill_03_1 0 → 1,24 (giữ lâu, `hut` 0,90), `hoi_phuc` 1,70 lưỡi hồn mọc (co giãn
  trục x của `luoi_hon`, vượt nhẹ), giơ qua đầu (skill_03_2 @ 2,0, `gong` 2,35), bổ: sang skill_01 @ 0,34 rồi cung 0,34 → 0,36, chúc xuống thêm
  7°, `trung` 2,72, khựng + rung tới 3,25, lưỡi hồn rút về chỗ gãy trong lúc khựng (3,03 → 3,25), thu theo đà skill_01. Impact skill (0,26; 1,2;
  0,22; chớp xanh), `span` 6.
- Đo góc nhảy (`ky_nguyen_rig.py kiem`, 30 khung/giây): attack bone7 57°, cast bone7 48°, die bone40 47° (như con gốc), appear bone23 41°, skill 41°.
- Soi: `rig/soi_*.png` (bộ vẽ Python), `rig/that/*.jpg`, `rig/that_can/*.jpg` (runtime Spine thật, cận thân): không rách, không hở.
- Ảnh động `inbox/ky_nguyen_1/_xem_dong.py` → `rig/dong/*.webp`; trang xem `inbox/ky_nguyen_xem_rig.html`. **CHỜ người dùng xem.**

## 7. Việc tiếp

1. Người dùng xem rig.
2. Hỏi: thay suất `tam_kiem` (ải 50, có boss)? tên, số dạng?
3. Vào game: VFX (hạt chồng lớp, chuẩn `chuan_fx/phun_lua.gif`, hệ hồn xanh): aura lửa hồn quanh giáp (clip lặp / hạt bám thân), `goi` hồn đồng đội
   (hình kỵ sĩ hồn xanh mờ lao tới đối thủ, code lái), `hut` khí hồn xoáy vào kiếm, `hoi_phuc` chớp xanh ở chỗ gãy, vệt chém theo `luoi_hon` →
   `mui_hon`, nổ hồn + nứt đất ở `trung` chiêu cuối, `mat_sang` chớp mắt, `hon_thoat` khói hồn lúc chết; heroes.json, menu Unity.

### 6b. Chiêu cuối bản 2 (người dùng xem rig: "chiêu cuối bạn hiểu sai ý rồi và ảnh cũng không đúng")

Lời dặn: "phần kiếm linh hồn **hiện lên dần theo tay** của tướng khi vuốt lên"; "**dài quá, cho ngắn đi**"; "phải **match vào đúng các vết gãy** của kiếm
cùn, như kiểu **sửa lại kiếm đó bằng một vật liệu khác**". Bản 1 (lưỡi hồn dài 1606 đơn vị, lưỡi lửa ở gốc, mọc bằng co giãn xương) bỏ.
- **Phần vá** (`ky_nguyen_manh.py hon2`, `cat HON2`): hình bóng do MÃ dựng trên kiếm gãy nằm ngang: kéo dài hai mép lưỡi sắt (khớp đường thẳng
  đoạn lưỡi trơn) tới mũi nhọn, trừ phần sắt còn lại → mép trái trùng từng răng vết gãy (`mau/kiem_va.png`, `kiem_va_mask.png`); GPT chỉ tô
  chất liệu trong hình đó (xanh hồn, sống lưỡi xanh nhạt nối tiếp sống lưỡi sắt, vân nứt như vá pha lê; `tai_ve/H_va.png`); mã cắt lại đúng
  hình bóng, không lấn sắt → `manh/hon_va.png`, cùng khung với ảnh kiếm gãy. Dài 650 đơn vị (kiếm lành ≈ 1,7 lần kiếm gãy).
- **Hiện theo tay**: bàn tay xa chỉ với quá chỗ gãy ~250 đơn vị (giới hạn tay từ vai); thử hạ kiếm bằng xoay tay cầm kiếm thì kiếm dạt ngang
  260+ đơn vị, bỏ. Cách làm: tay lên nhanh dọc lưỡi sắt tới chỗ gãy (0,5 → 0,8 s, skill_03_1 0,40 → 0,63), vuốt chậm dọc phần vá (0,8 → 1,55 s,
  0,63 → 1,18; cộng vai 22°, khuỷu 12° cho tay sát mép, cao hơn), mép hiện = độ cao lòng bàn tay chiếu lên trục lưỡi + 50 đơn vị (cực đại dồn);
  tay hất lên (1,55 → 1,72) thì đoạn còn lại phóng tới mũi (`hat`), `hoi_phuc` 1,72.
- **Chia 10 lát bị vạch mảnh ở ranh lát** (runtime thật, kể cả chồng 6 px) → đổi sang MỘT ảnh phần vá + **mặt nạ cắt** (Spine clipping) bám xương
  `hon_dau` (con `hon_goc` ở chỗ gãy, trục x dọc lưỡi): chỉ lộ phần vá sau mép; mặt nạ chỉ gắn hình trong đoạn chiêu cuối (bật TRƯỚC khi phần vá
  hiện 0,1 s: khoá đổi hình của mặt nạ trễ một khung thì lóe nguyên lưỡi), các clip khác tắt (runtime khỏi cắt). `.atomik` 363 KB, 4 mặt nạ cắt.
- Đã xuất lại rig + ảnh động chiêu cuối (`rig/dong/skill.webp`). **CHỜ người dùng xem bản 2.** (Tin "ok ổn rồi, làm thêm dạng 1" giữa lượt là
  người dùng nhắn nhầm phiên: chưa duyệt, chưa làm dạng 1.)

## 8. Vào game + VFX (2026-11-16; người dùng: "ok cho vào game, làm thêm các fx hiệu ứng nữa rồi làm dạng 1 của tướng này")

- **Dữ liệu** `quai/doi_ky_nguyen.py` (dùng hàm `doi_phap_lua.py`): suất `tam_kiem` giữ id, thẻ, chỉ số, hiệu ứng thẻ; SỐ DẠNG 3 → 2. Tên tạm do Claude
  đặt (người dùng chưa đặt): **Vong Kỵ**, "Kỵ sĩ cổ đại bị nguyền", "Dòng Vong Kỵ"; dạng **Vong Kỵ Nhi** 0,92 / **Vong Kỵ** 1,1 (chưa có rig dạng 1:
  cả hai trỏ `ky_nguyen_2`); thẻ Hồn Binh Cổ Chiến (ghost), Kiếm Hồn Phục Sinh (sword), Bất Tử Nguyền (skull), boss Kiếm Nguyền Phản (sword).
  `chep` → `Resources/ky_nguyen_2/` (rig, chân dung, ảnh hồn đồng đội `ky_nguyen_2_tt_hon.png` = hình bóng mũ vương miện tô xanh hồn + mắt của
  rig, tên `_tt_` để AolaImport nhập thành sprite). Resources/tam_kiem_* cũ không đụng.
- **VFX** `Assets/01 Script/Game/Battle/HatHon.cs` (SINH bằng `ArtGen/Spine/ky_nguyen_hat_cs.py` = khung C# + bảng đo rig 30 khung/giây: mũi kiếm
  gãy ở cast; mũi kiếm, chỗ gãy, MÉP ĐANG HIỆN của phần vá (xương `hon_dau`), mũi phần vá, độ đậm phần vá ở skill): `n_hon_chem` (đòn thường: vệt
  chém lửa hồn quét cung qua đối thủ 0,075 s trước khung trúng, chớp hồn, lưỡi lửa toé, mảnh giáp rỉ), `n_hon_goi1/n_hon_goi` (mana: mũi kiếm
  bùng lửa hồn, 3 / 5 HỒN ĐỒNG ĐỘI bay ra từ mũi kiếm, xếp vòng cung quanh vai, lao theo cung vào đối thủ, đuôi lửa hồn, hồn cuối nổ to),
  `n_hon_kiem1/n_hon_kiem` (chiêu cuối: khí hồn hút vào mép phần vá đúng theo mặt nạ cắt, tia ở mép, `hat` lửa chạy dọc lưỡi, `hoi_phuc` bùng dọc
  lưỡi, `gong` aura bùng quanh người + vòng sàn, vệt lửa hồn theo đúng đường mũi kiếm lúc bổ, trúng: chớp lớn, ba vòng sóng, cột lưỡi lửa hồn,
  khói, mảnh giáp, đá, rung mạnh, `tat` phần vá tan thành khí hồn). Bảng màu lửa `hon` + chủ đề `tam_kiem` (`HatLua.cs`), `StageView.KimFx` /
  `KimAtk`, `HatNuoc.PlayNuoc`, `HatVoi.AtkLao`. Màn chớp chiêu cuối của rig hạ `#b6ff7a55` → `#b6ff7a30` (soi trong trận: gắt quá).
- **Unity** (cầu MCP 8080; phiên assets-b8 báo Unity rảnh): biên dịch sạch, Nhập dữ liệu, Gắn dạng (`tam_kiem: prefab giữ 2 dạng (ky_nguyen_2,
  ky_nguyen_2)`), Đảo 70 ải sinh lại, ba menu golden + `golden_ghep.py` (sim: ô kim 190; roster `tam_kiem` n 3 → 2). EditMode 106 / 107 (chỉ
  `PrefabOnlyTests` cũ ở `UI/Kit`).
- **Soi trong trận**: menu "PokiClash/Thử/Đảo Kim: riêng Vong Kỵ (dạng 2) / Vong Kỵ Nhi (dạng 1)…" (`Editor/KimFxTour.cs`), tờ ghép
  `inbox/ky_nguyen_1/trong_tran/vong_ky_5sao_<danh|mana|ult>.jpg`. Lượt 1: hồn đồng đội xếp quạt TRÊN mũi kiếm (mũi kiếm giơ sát mép trên màn) nên
  lọt khỏi màn, nấp sau bảng máu đối thủ, hình nhỏ → xếp vòng cung quanh vai (1,05–1,3 thân), hình 0,46 thân. Lượt 2: đạt (hồn thấy rõ, lao trúng,
  vệt chém đòn thường, chiêu cuối đủ pha).

## 9. Dạng 1 (Vong Kỵ Nhi), bắt đầu 2026-11-16

- **Tỉ lệ trên CÙNG rig** (`KN_DANG=non ky_nguyen_rig.py`, mẫu quy_xich_rig): đầu `bone5` × 1,4; gốc năm chuỗi lửa trên mũ `bone26–30` × 0,58 (lửa là
  con của xương đầu: tổng ≈ 0,8 lửa dạng 2); cánh tay trên `bone7` / `bone43` × 0,85; bàn tay `bone9` / `bone45` × 1,1; giáp vai `bone31` × 0,8; kiếm
  `bone23` × 0,8 (tổng ≈ 0,75); vạt trước `bone40`, áo choàng `bone67` × 0,85. Biến `KN_DAU / KN_LUA / KN_TAY / KN_BAN / KN_VAI / KN_KIEM / KN_AO`.
  Mảnh cứng có toạ độ thế giới dạng 2 (da dạng 2, hoặc mảnh dạng 1 ghi `"he": "lon"` trong moi.json) gắn theo thế giới KHÔNG đổi tỉ lệ (`Wc`) thì
  co / phóng cùng xương; `hon_goc` dựng cùng hệ với ảnh vá; mép hiện chiêu cuối đổi về đơn vị dọc `hon_goc` (chia tỉ lệ xương kiếm). Dạng 2 không đổi
  (thế giới xương kiếm tỉ lệ 1).
- **Kiếm giữ y hình dạng 2** (cùng vết gãy): dạng 1 dùng lại `kiem.png` + `hon_va.png` (ghi `"he": "lon"`), chiêu cuối vá kiếm như dạng 2, nhỏ hơn.
- Bố cục `inbox/ky_nguyen_non/mau/bo_cuc.png` (+ `bo_cuc_khung.png` 1536 × 1024) dựng bằng da dạng 2 ở tỉ lệ dạng 1.
- **Concept lượt 1** (`ky_nguyen_non.py concept`, `gui_gpt/ky_nguyen_non/luot_1_concept_<A|B|C>.txt`): A cận vệ tập sự (mũ chỏm tròn khe ngang,
  túm lửa nhỏ, giáp vai một tấm tròn, không mũi tên), B hiệp sĩ giáp vá (mũ chóp nhọn có thanh che mũi, giáp vá đinh tán dây da, một mũi tên gãy ở
  vai, mảnh khiên gỗ bay), C mũ thùng sứt (mũ thùng quá cỡ móp một góc, khe chữ thập, khe hở lộ hồn nhiều hơn, một mũi tên ở cẳng tay). Codex hết
  lượt đến 19:01 → hẹn tự chạy 19:03.
