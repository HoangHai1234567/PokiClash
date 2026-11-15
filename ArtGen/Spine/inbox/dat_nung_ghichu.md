# Chiến binh đất nung, lõi dung nham (`dat_nung`): tướng thứ 8 đảo Hỏa

Bắt đầu 2026-11-14 (máy ổ D). Con gốc của rig: `monster_3625` (game tham khảo, kho `D:\RefAnimation\SwordxStaff`), **do người dùng chỉ** (ảnh
chụp trang xem, clip `skill_04_2`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai.
Hình là thiết kế của mình. Suất 8 đảo Hỏa = ải 50, id game hiện là `huyen_viem` (Huyễn Viêm, ba dạng aola). Tên, id, số dạng: chưa bàn
(`dat_nung` chỉ là mã làm việc).

## 1. Lời dặn của người dùng (2026-11-14)

- "làm tướng thứ 8 đảo hỏa; concept **chiến binh đất nung đá dung nham, có lõi dung nham**".
- appear: "các bộ phận **bay vào quanh lõi**".
- idle: "làm giống họ cũng được, **sửa đi khác chút**". walk: "làm giống họ".
- Đánh thường: "có thể làm giống **skill_01_1**, sửa lại chút".
- Chiêu mana: "làm giống **skill_04_1**, đâm kiếm vào đối thủ rồi thực hiện nhiều động tác chém".
- Chiêu cuối: "tướng **dang tay, ngửa lòng bàn tay** ra, thanh kiếm **bay lơ lửng ở giữa, mũi kiếm hướng lên**, sau đó từ kiếm đó **phân thân sang
  2 bên** nhiều thanh kiếm nữa (**5 thanh**), sau đó **tất cả kiếm hướng về địch rồi bay vào**".
- Chết: "**lõi tắt ngỏm, rụng rời từng bộ phận**".

"5 thanh" = **tổng 5** (thanh thật ở giữa + hai thanh mỗi bên): người dùng xác nhận 2026-11-14.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3625/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample.json` 15 clip 30 khung/giây, `mo/`, `parts/`, `khung/`, `khung_can/`)

85 xương, 98 slot, 15 clip. **FK thuần** (không IK, không ràng buộc). **Mọi hình là lưới CỨNG một xương** (trừ kiếm `P_wuqi` hai xương
`bone11` + `bone185` và quầng lõi `P_huoyan20` hai xương) → hình bóng từng mảnh của mình tự do (skill pokiclash-spine-rig mục 25).
Bộ giáp rỗng lơ lửng, không chân; mặt đất y = 0 (`all` ở y −200, `shadow` +200).

Hướng: đầu con gốc ngoảnh sang TRÁI, nhưng mọi đòn (lao `skill_01`, đâm `skill_04`) đi về bên PHẢI (+x) → địch ở bên phải như các con
Sword x Staff khác; đầu của mình vẽ nhìn sang phải.

Cây xương: `root > all > xy > zhixin` (tâm thân) `> xiashen` (mảnh dưới), `shenti1 > shenti2 > bozi > tou` (đầu); `shenti1 > bone27` (viên lõi),
`bone90`, `bone94`; `zhixin > bone88, bone89`.
- Tay GẦN (L của họ; vai ở bên phải người xem, vắt ngang phía dưới sang trái nắm kiếm): `shenti2 > L_jianbang > L_dabi > L_xiaobi > L_shou >
  bone11` (kiếm) `> bone185` (mũi kiếm). Bàn tay XOÈ thứ hai của tay gần: `L_shou > bone115` + ngón `bone116…184` (dùng lại ảnh bàn tay xa; họ
  đặt `bone115` = (15,7; −5,2; −73,2°; tỉ lệ (1, −1)) khi dùng, dáng gốc để nó ở chỗ khác).
- Tay XA (R; bên trái, sau kiếm, bàn tay xoè năm ngón, mỗi ngón hai đốt rời): `shenti2 > R_jianbang > R_dabi > R_xiaobi > R_shou >` ngón.
- Giáp vai: `P_jianjiaL1..5` (gần, bên phải, to), `P_jianjiaR1..5` (xa, bên trái); mười hai phiến `P_dun01..12` (dun01–03 phiến trước / bên; dun04–12
  chín phiến cong xoè sau lưng, mỗi phiến một xương: bone107, 14, 28, 26, 25, 24, 23, 90, 94).
- Bộ nhân bản có sẵn: ba bộ tay gần + kiếm (`L_dabi2..4`, `P_wuqi3..5`: bóng mờ của `skill_03`), kiếm rời `P_wuqi2` trên `bone186` (con của `all`;
  `die_01`), bản tay gần ở thứ tự vẽ khác (`bone188`, `bone190`), nắm tay trên tay xa (`bone189`).

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho |
|---|---|---|---|
| `idle_01` | 4,0 s | nhấp nhô, các phiến trôi; 1,6–2,1 s vung kiếm dựng lên một nhịp; viên lõi quay 4 vòng | nền **idle** |
| `run_01` | 0,93 s | chúi tới, nhấp nhô | **walk** |
| `skill_01_1/2/3` | 1,0 s | kéo lùi 0–0,33; LAO vai tới (một khung nhảy bậc 10 → 11); giữ tới 0,67; lùi về | **attack** |
| `skill_02` | 2,13 s | giơ kiếm, nhảy, bổ | chưa dùng |
| `skill_03` | 2,83 s | vung kiếm có ba bóng mờ, cắm kiếm trước mặt | chưa dùng |
| `skill_04_1/2/3` | 2,5 s | thu kiếm ngang; ĐÂM tới (khung 11); hất lên; chém ngược về (khung 26); vung ra sau lấy đà 1,1–1,6; đâm / bổ kết (khung 50–51); về | **cast** |
| `hit_01/02`, `block_01`, `stun_01` | | | **hit** = hit_01 |
| `die_01` | 1,0 s | bật ngửa, rã thành đống, kiếm cắm đất | không dùng (die tự viết) |
Ba cú của `skill_04` và cú lao của `skill_01` đều là khoá BẬC một khung (lấy mẫu tốc độ mũi kiếm mới thấy): clip mình giãn mỗi cú ra 0,07–0,10 s.

## 3. Concept (đề xuất của Claude; người dùng chọn A, xem mục 5)

Script: `dat_nung.py` (mổ; dùng chung bộ mổ của `quy_dao.py`), `dat_nung_bo_cuc.py` (sơ đồ bố cục 1536 × 1024 ở khung 0 idle, 0,74 px / đơn vị rig,
gốc rig ở (759,7; 918,8)), `build_dat_nung.py` (gói `gui_gpt/dat_nung_1/`; ảnh mẫu: sơ đồ, golem lõi lửa, quỷ đao, bản đồ).

Giữ của con gốc: cách dựng (giáp rỗng lơ lửng, lõi tròn giữa ngực, hai giáp vai lớn, tay gần vắt ngang nắm kiếm dựng chéo bên trái, tay xa xoè
ngón, chùm phiến xoè sau lưng), chỗ, cỡ, thứ tự chồng. Đổi dáng ngay từ sơ đồ: đầu thú hai sừng → **đầu tượng binh có búi tóc** (hoặc mũ vò úp);
kiếm mảnh chữ triện → **kiếm bản rộng đá dung nham đen, rãnh dung nham giữa**, chắn tay + khâu chuôi đất nung; chín phiến cong như sừng → **chín
mảnh đá dung nham thẳng, nhọn** có khe dung nham; giáp vai khắc xoắn → vảy ngói / mảnh vò.

Lượt 1 (2026-11-14, hai ảnh, cả hai bám sơ đồ ngay lượt đầu; tờ so `inbox/dat_nung_1/so_hai_huong.png`):
- **A `tuong_binh`** (`tai_ve/L1_tuong_binh.png`): đất nung cam #C8683C, đầu tượng binh búi tóc đá + đai trán, mắt khe vàng, giáp vai xếp vảy ngói có
  đinh tán, đá dung nham nâu than, lõi cam có viên vàng. **Claude đề xuất bản này** (tông cam chưa tướng Hỏa nào dùng).
- **B `lo_gom`** (`tai_ve/L1_lo_gom.png`): gạch đỏ sẫm #A8432F, mũ là chiếc vò úp có khe chữ T, giáp vai mảnh vò vỡ vành men ngà + dải zíc zắc, đá
  dung nham đen. Gần tông Hiệp Sĩ Dung Nham (suất 1).

## 4. Rig thử trên DA GỐC + 8 clip (làm trong lúc chờ chọn concept)

`DN_GOC=1 py -3 -I dat_nung_rig.py` → `inbox/dat_nung_1/rig_goc/` (`xem.html`, tờ khung, `.atomik` 224 KB): 152 xương, 166 slot, 1239 đỉnh; chiều
cao game 800 (đỉnh đầu / giáp vai; không tính mảnh đá sau lưng và kiếm). Dáng gốc của rig = khung 0 idle_01. Chuyển động đọc thẳng từ
`sample.json` (rig FK thuần nên không cần nướng lại qua Chrome); clip tự viết đặt xương bằng mã (giải hai khúc tay bằng `hoat.ik_hai_doan`).

- Thứ tự vẽ đổi trong clip của họ → slot di động nhân bản theo chỗ chèn (`<slot>@<k>`, như quy_dao).
- **Bộ mảnh RỜI** (appear, die): mỗi mảnh hiện ở khung 0 idle (53 mảnh) có slot `<slot>~r` trên xương rời `r_<tên>` (con của `move`, gốc ở tâm
  mảnh); clip đặt từng mảnh theo thế giới (`bo_roi`).
- **5 kiếm bay** (chiêu cuối): `kiem_k` trên `nam_k` (con của `fly_k`, con của root); chỗ dáng gốc của `fly_k` = chỗ phóng (hình quạt trên đầu);
  `game.far = ["skill"]`, `farAim = ["skill"]`.
- Lõi của họ quay 4 vòng mỗi vòng idle (góc cộng dồn không khép vòng) → bỏ phần quay, lõi mình chỉ đập.

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| idle | 4,0 s lặp | idle_01; cú vung kiếm giữa vòng giảm còn ~55 %; thêm NHỊP BÙNG 1,55–2,6 s (lõi phồng, chùm đá sau lưng khép rồi xoè, bàn tay xa nắm rồi xoè); lõi đập hai nhịp mỗi giây; chùm đá "thở" lệch pha | tu 1,55 |
| walk | 0,93 s lặp | run_01 + lõi đập, chùm đá khép nhẹ | |
| hit | 0,5 s | hit_01 + chùm đá bật xoè | |
| attack | 1,30 s | skill_01_1: kéo lùi lâu hơn (giơ kiếm, chùm đá khép) 0–0,42; LAO 0,42–0,51 (giãn khung nhảy bậc); tới nơi BỔ thêm một nhát kiếm chéo về trước 0,51–0,60 (họ chỉ húc); khựng, chùm đá xoè, lõi bùng; lùi về. Lao 0,42 chiều cao | lao 0,42; chem + trung 0,60 |
| cast | 2,70 s | skill_04_1: thu kiếm; lao tới ĐÂM 0,42; hất lên; chém ngược 1,00; vung ra sau gồng 1,22–1,62; cú kết 1,72; về. Lao 0,50 chiều cao | lao 0,20; dam 0,42; chem 0,74 / 1,00; tu 1,30; chem + trung 1,72 |
| skill | 3,20 s | (tự làm) hai tay dang ra, bàn tay xoè ngửa; kiếm rời tay 0,14 bay lên giữa, mũi lên, thu còn 0,72 (0,58); phân thân ±1 ở 0,78, ±2 ở 0,94 thành hình QUẠT 5 thanh trên đầu (mở 24° mỗi thanh), lơ lửng; 1,50–1,86 cả dàn xoay mũi về phía địch, người ngả sau; phóng lần lượt từ thanh gần địch (2,02, cách 0,06 s, bay 0,17 s), hai tay đẩy tới; kiếm hiện lại trong tay 2,62–2,96. Đứng tại chỗ | tha, tu, phan 1 / 2, xoay, ban ×5, cham ×5, trung 2,44, hien |
| appear | 2,50 s | (tự làm) viên lõi hiện, quầng dung nham lớn dần 0–0,42; các nhóm mảnh BAY VÀO quanh lõi: vành cổ 0,34, mảnh dưới, đầu 0,56, giáp vai, tay, bàn tay, ngón, chùm đá 1,14–1,44, kiếm xoay tít bay vào tay 1,46; ráp xong 1,86, gồng một nhịp | loi, ghep dau / kiem, xong |
| die | 1,95 s | (tự làm) giật; lõi chập chờn rồi TẮT 0,36; các mảnh xệ, rụng dần từ 0,44: ngón, chùm đá, bàn tay, kiếm (cắm xuống đất bên trái), tay, giáp vai, vành cổ, đầu, lõi lăn ra; mờ dần 0,5 s cuối | tat 0,36; roi; cham_dat |

Nối: mọi clip về idle 0,00 px; idle khép vòng 2,35 px, walk 3,39 px; appear khung đầu trống, die khung cuối trống. `xem.html` chạy (thu_xem: đủ 8
nút + chạy nối, không lỗi JS; gọi `thu_xem.py` bằng đường dẫn TUYỆT ĐỐI).

Đã soi bằng bộ vẽ Python (tờ `rig_goc/soi_<clip>.png`): idle, attack, cast, skill (cả cận hai tay), appear, die. Chưa chạy runtime Spine thật từng
khung, chưa xem trong game.

## 5. Bản TỰ CHẾ theo concept A (ĐÃ BỎ, xem mục 6): mảnh, rig (2026-11-14 sáng; người dùng chọn A · tượng binh và tổng 5 kiếm)

Concept chốt: `tai_ve/L1_duyet.png` (= `L1_tuong_binh.png`).

**Mảnh "đúng chỗ, đúng cỡ"** (`build_dat_nung.py manh` → `gui_gpt/dat_nung_1/luot_2_manh_A..F.txt`; 6 tờ, ~85 s mỗi tờ, cả sáu dùng được ngay lượt đầu):
A đầu + giáp vai xa + nắm tay (không kiếm) + tấm dựng + mảnh đá dài; B kiếm trọn cây + giáp vai gần + mảnh đá sau đầu + viên lõi; C quầng dung nham
trọn đĩa (không lõi) + lòng bàn tay xa + các đốt ngón + mảnh đá thoi + khối cẳng tay + mảnh đá trên trái; D hai vành cổ + phiến trên + tấm đá dưới
cẳng tay; E bốn răng đá + mảnh đá chếch phải + phiến dưới + khối bắp tay trên; F khớp vai + khối tay dưới + cẳng tay xa + mảnh đá nhỏ + khối bắp tay xa
(khuất trên concept, vẽ ở góc trống).

**Cắt** (`dat_nung_manh.py lam` → `manh/*.png`, `manh/dat.json`, `_so_ghep.png`, `_to.png`): cụm liền trên nền trắng, gán tên theo tâm ước chừng
(`TO`); mỗi mảnh thay MỘT ảnh vùng của rig gốc (`VUNG`) và bám xương của vùng đó; chỗ đặt = chỗ trên concept (một phép đồng dạng cho cả con:
0,74 px / đơn vị, gốc (759,7; 918,8)), dò lại ± 70 px bằng so khớp có mặt nạ (mảnh lộ nhiều lệch 0–13 px; mảnh khuất nhiều / lẫn màu mảnh kề giữ nguyên
chỗ Codex vẽ: `KHONG_KHOP`). 36 mảnh + 2 hình tắt (`loi_tat`, `lava_nguoi`: đổi màu bằng mã). Kiếm xoay dựng đứng cho đỡ tốn atlas (M mang phép xoay).
- Đốt ngón tay xa Codex vẽ sát nhau dính thành cụm: bóp cụm lấy lõi rồi chia theo lõi gần nhất → 6 mảnh (vài mảnh là một cặp đốt); gán vào 6 trong 11
  ảnh vùng ngón theo vị trí tương đối. Bàn tay XOÈ của tay gần dùng lại đúng các mảnh này (phép afin bản chính → bản sao ở dáng gốc của họ).
- Thứ tự chồng theo concept khác rig gốc ở ba chỗ, xử lý bằng cách đổi ảnh vùng nhận mảnh: giáp vai xa → `P_jianjiaR3` (cùng xương, vẽ trước vành cổ
  trái); tấm dựng ↔ khối tay dưới đổi vùng cho nhau (`P_shouL2_1` ↔ `P_dun01`); viên LÕI dời slot ra sau hai vành cổ (lõi nằm trước, làm trong rig).

**Rig da mình** (`py -3 -I dat_nung_rig.py` → `inbox/dat_nung_1/rig/`): 135 xương, 117 slot, 468 đỉnh, 8 clip, `.atomik` **357 KB** (atlas 1224 × 1688;
dưới trần 0,5 MB, trên đích 0,3 MB). Nối: mọi clip về idle 0,00 px; idle khép vòng 2,3 px, walk 4,6 px; appear khung đầu trống, die khung cuối trống;
`.atomik` nạp lại lệch 0,2 px. `xem.html` chạy đủ 8 nút. Khác bản da gốc:
- chiêu mana giữ NẮM TAY (họ đổi sang bàn tay xoè ôm chuôi; bàn tay xoè của mình nhỏ);
- chiêu cuối: khuỷu tay gần chúc XUỐNG (`UON_G = −1`; khuỷu vểnh lên thì bắp tay quay 138°, các khối bắp tay văng lên che giáp vai và đầu); hai bàn tay
  đưa lên ngang đầu, ngoài hai giáp vai (tay xa thấp hơn thì nấp sau hai phiến nhọn); bàn tay xoè tay gần phóng 1,45 và bật bản vẽ TRƯỚC cẳng tay;
- chết: viên lõi và quầng dung nham đổi sang hình nguội (slot `~t`).

Đã soi bằng bộ vẽ Python trên da mình: idle, attack, cast, skill (cả cận), appear, die (`rig/soi_<clip>.png`, `rig/khung_<clip>.png`). CHƯA: runtime Spine
thật từng khung, trong game.

Còn xấu / biết mà chưa sửa: vành cổ phải Codex vẽ ngắn và mập hơn concept; mảnh đá dài bị gãy khúc; các khối tay gần khác concept đôi chút (khối dưới bo
tròn); tay gần của chiêu cuối các khối bắp tay còn chồng lộn xộn; hai phiến nhọn bên trái và bàn tay xa chồng nhau lúc nghỉ.

## 6. Người dùng TRẢ bản tự chế; làm lại ĐỔI DA THEO KHUNG PART (2026-11-14 trưa)

Người dùng mở `rig/xem.html` (bản mục 5) rồi nói: "**không được, concept này chưa đạt, làm giống con gốc, mổ xẻ kĩ con gốc ra làm theo**". Bản mục 3–5
(đầu búi tóc, kiếm bản rộng, mảnh đá thẳng, khối tay tự vẽ, mảnh đặt tự do) BỎ; file giữ nguyên (`manh/`, `rig/`, `M_*.png`, chế độ `DN_TU_DO=1`).
Bài học: mọi mảnh là mảnh cứng không có nghĩa là được đổi dáng; mặc định giữ hình bóng, tỉ lệ, cách tách mảnh của con gốc, chỉ đổi chất liệu và màu.

Làm lại (script `dat_nung_da.py`, mẫu là `quy_dao_da.py`; skill mục 00 "CÁCH CHUẨN", mục 23):
- **Concept theo con gốc** (`dat_nung_da.py ca_con` → `mau/goc_ca_con.png` = cả con gốc ở khung 0 idle nền trắng; prompt `luot_1c_concept_theo_goc.txt`:
  vẽ lại ĐÚNG con đó, đúng dáng, đúng từng mảnh, đổi chất liệu) → `tai_ve/L2_theo_goc.png` (124 s, đạt ngay). Chất liệu: giáp (đầu hai sừng, giáp vai,
  vành cổ, phiến bên, tấm tay, nắm tay, chắn kiếm) đất nung cam #C8683C, mặt bên / mặt dưới đất nung sẫm #96482C, hoa văn khắc thành rãnh sẫm; chín
  phiến cong sau lưng, chốt tròn, đốt ngón, mảnh dưới, lưỡi kiếm đá dung nham than #4A3E3C, mỗi phiến một khe dung nham cam; quầng dung nham cam
  #EE7A22 có mảng vỏ sẫm; viên lõi, mắt vàng #FFD64A; đường chữ triện trên kiếm thành đường dung nham cam – vàng. Claude tạm lấy bản này làm
  `L2_duyet.png` để chạy tiếp (người dùng CHƯA nói duyệt).
- **Sáu tờ mảnh GỐC** cắt theo lưới, phóng 1,5–4,4 lần (`dat_nung_da.py to` → `mau/goc_A..F.png` + ô từng mảnh; prompt `luot_3_da_A..F.txt`: ảnh 1 tờ mảnh
  gốc, ảnh 2 concept; giữ hình bóng, cỡ, chỗ, đường cấu trúc; tả từng mảnh đổi thành chất liệu gì): A đầu, hai giáp vai, hai vành cổ, khớp vai, lõi;
  B hai tấm bắp tay có chốt, nắm tay, tấm dựng, tấm cẳng tay, tấm dưới, thanh trụ, mẩu ngón cái; C chín phiến sau lưng; D kiếm, quầng dung nham, phiến
  bên; E phiến bên thứ hai, các mảnh giáp nhỏ, ba mảnh thân dưới; F bắp / cẳng / lòng bàn tay xa + 11 đốt ngón. ~105 s mỗi tờ (lô này phải chờ khoá Codex
  11 phút vì phiên khác đang gen).
- **Cắt** (`dat_nung_da.py cat` → `manh_part/<ảnh vùng>.png` = ảnh vùng × 2, `_so_<tờ>.png`, `_iou.json`): cả 51 part IoU **0,90–0,99** ngay lượt đầu
  (thấp nhất `P_dun11` 0,902).
- **Rig** (`py -3 -I dat_nung_rig.py`, chế độ PART mặc định → `inbox/dat_nung_1/rig_part/`): NGUYÊN lưới, xương, thứ tự vẽ của họ, ảnh của mình (0,64 px /
  đơn vị); cùng 8 clip như mục 4 (tư thế chiêu cuối theo số của bản da gốc); lõi và quầng dung nham có hình nguội cho clip chết (đổi màu bằng mã). 150
  xương, 164 slot, 1239 đỉnh, `.atomik` **418 KB** (atlas 1240 × 1552, dưới trần 0,5 MB). Nối: mọi clip về idle 0,00 px; idle khép vòng 2,35 px, walk
  3,39 px; appear khung đầu trống, die khung cuối trống. `xem.html` chạy đủ 8 nút (đã mở cho người dùng).
- Đã soi bằng bộ vẽ Python: idle, skill, die (`rig_part/soi_*.png`), tờ khung mọi clip (`rig_part/khung_*.png`). CHƯA soi cận từng khung attack, cast,
  appear trên da mới; chưa runtime thật, chưa trong game.
- Bẫy đã gặp: `ca_con` bản đầu vẽ thẳng các part lên nền bằng `_tris` → ô tam giác đè ĐEN lên phần đã vẽ (ảnh mẫu hỏng, đã dừng lượt gen đang chạy);
  phải vẽ mỗi part lên một lớp trong suốt rồi mới chồng.

## 6b. Đổi KIỂU DÁNG mặt + giáp trên bản theo khung part (2026-11-14 chiều)

Người dùng xem `rig_part`: "nhìn ổn nhưng gen lại mặt cho khác đi, giáp xung quanh cũng nên gen lại cho khác". Tay, kiếm, lõi, quầng dung nham, dáng, clip giữ.

- Ba concept (`dat_nung_da.py mat_giap` → `luot_4_concept_mat_giap_1..3.txt` → `tai_ve/L3_1..3.png`, ảnh mẫu duy nhất là `L2_theo_goc.png`); trang so
  `mau/_so_mat_giap.png`. Người dùng chọn **2** (mặt nạ thú gốm sừng ngắn, giáp vai đá vỡ có gai, vành cổ đinh, phiến sau lưng thành mảnh đá vỡ):
  `tai_ve/L3_duyet.png`.
- Mảnh mới: 17 mảnh (đầu `P_tou`, vành cổ `P_jianjiaL2/R2`, giáp vai `P_jianjiaL1/R1`, phiến bên `P_dun01..03`, chín phiến lưng `P_dun04..12`) trên bốn
  tờ G, K, H, I. `dat_nung_da.py to_minh` dựng tờ hướng dẫn = mảnh ĐANG DÙNG xếp đúng ô (`mau/minh_<tờ>.png`) + prompt `luot_5_manh_moi_<tờ>.txt`
  (ảnh 2 = `L3_duyet.png`; câu tả từng mảnh ở `TA2`); `cat_moi` cắt `tai_ve/N_<tờ>.png` → `manh_part2/<ảnh vùng>.png` + `.json` (`le` = lề theo px ảnh
  vùng; lề tự tính theo phần hình mới lấn ra ngoài ô cũ, mặt nạ chỉ lấy cụm liền của mảnh nên không dính mảnh bên). Các mảnh khác vẫn ở `manh_part/`.
- Rig: mảnh có trong `manh_part2/` gắn bằng lưới 4 đỉnh, bốn góc tính qua phép afin uv → thế giới của lưới gốc (mảnh cứng một xương) → nằm đúng chỗ
  mảnh cũ. Hình mới to hơn mảnh cũ 1,2–1,5 lần và đầu bè ngang nên bản lắp đầu che mất quầng dung nham + viên lõi: bảng `CHINH` (co quanh trọng tâm
  hình, dời) thu đầu 0,86 và dời sang phải 48, vành cổ và giáp vai gần 0,85, giáp vai xa 0,90. Đầu có hình TẮT (`tat_lava`: mắt, miệng, chóp sừng
  nguội) bật cùng lõi ở clip chết. Xuất ra `rig_moi/` (463 KB, 165 slot); `DN_CU=1` dựng lại bản cũ vào `rig_part/`.
- Đã soi khung idle, attack, cast, skill, appear, die bằng bộ vẽ Python và `thu_xem.py` (8 nút clip). Chưa soi runtime thật từng khung, chưa trong game.
- Khe dung nham trên giáp và kiếm vẫn sáng lúc chết (chỉ lõi, quầng, mắt, miệng tắt): làm thêm hình tắt thì atlas vượt trần 0,5 MB.

## 6c. Vào game (2026-11-14 tối, người dùng: "Ổn, cho vào game đi rồi làm dạng 1 của tướng này")

- **Suất `huyen_viem`** (ải 50 đảo Hỏa; id, thẻ, chỉ số giữ; số dạng 3 → 2): `quai/doi_dat_nung.py` (dùng lại `doi_phap_lua.py`). Tên do Claude đặt, người
  dùng chưa duyệt: tướng **Viêm Dũng** ("Tượng binh đất nung lõi dung nham", dòng "Dòng Viêm Dũng"; "dũng" = tượng binh như binh mã dũng), dạng 1
  **Viêm Dũng Nhi**; thẻ Ảo Hỏa → **Xuyên Tâm Liên Trảm** (crack), Huyễn Viêm Thiên Hỏa → **Ngũ Kiếm Tề Phi** (sword), Hồ Ảnh → **Lõi Nham Bùng
  Cháy** (flame), thẻ boss Ảo Ảnh Hồ Ly → **Giáp Nung Tự Liền** (shield). Rig `rig_moi/` chép vào `Resources/dat_nung_1/` (thư mục mới;
  `huyen_viem_1..3` cũ không đụng). Chưa có dạng 1: hai dạng tạm cùng trỏ `dat_nung_1`, cỡ 0,8 / 0,95 (1,1 thì kiếm chạm mép phải sân).
- **Hiệu ứng (bản tối thiểu, chưa phải VFX riêng đủ):** `Assets/01 Script/Game/Battle/HatDat.cs` mã `n_dat_dam` (chiêu mana: vệt lửa ở cú đâm, hất
  lên, chém ngược, dung nham trào `Eruption` đúng nhát bổ kết; mốc tính từ `lead` = 1,72 s); thêm vào `HatLua.CastLao` (HatKiem.cs) để sân nắn quãng
  lướt của clip cast tới đối thủ; `case` trong `HatNuoc.PlayNuoc`; `StageView.FireFx["huyen_viem"] = ("n_dat_dam", "no_lon")` (trước: "kim",
  "loc_xoay"); `HatLua.Themes["huyen_viem"]` về bảng "lua" (trước: "tim" của cáo lửa). Chiêu cuối: năm kiếm là mảnh của rig (xương far), nổ lớn mã
  chung. Menu thử: "PokiClash/Thử/Đảo Hỏa: riêng Viêm Dũng…" và "…Viêm Dũng Nhi (dạng 1)…" (`HoaFxTour.cs`, đang Play).
- **Unity** (phiên assets-4c xác nhận Unity rảnh): refresh + biên dịch sạch → "Nhập dữ liệu" (88 tướng) → "Gắn dạng .atomik" → "Đảo 70 ải: sinh lại"
  (`stages.json` không đổi) → ba menu golden + `golden_ghep.py`: chỉ `roster.json` 2 ô (n 3 → 2, dạng ở sao cuối 2 → 1) và `sim.json` 1 ải (hoa 120:
  boss tiến hóa một lần, 9 → 8 hiệp ở 2 ô). EditMode **106 / 107** (chỉ `PrefabOnlyTests` cũ ở `UI/Kit`).
- **Trong trận** (tour "riêng Viêm Dũng", sao cuối; tờ ảnh `inbox/dat_nung_1/trong_game/tran_danh.jpg`, `tran_mana.jpg`, `tran_ult.jpg`, chụp lúc cỡ còn
  1,1): đòn thường lao tới chém; chiêu mana lướt tới đâm rồi chém, có vệt lửa + dung nham trào; chiêu cuối năm kiếm xếp quạt, bay tới đối thủ, nổ lớn,
  kiếm hiện lại. Console không lỗi. CHƯA soi: cỡ mới 0,95, ô xem tướng, lật phía địch, appear / die trong trận.

## 6d. Dạng 1 "Viêm Dũng Nhi" (mã dat_nung_non; đang làm)

- Cùng xương, lưới, clip: `DN_NON=1 py -3 -I dat_nung_rig.py` (xuất `inbox/dat_nung_non/rig/`). Tỉ lệ dáng gốc `TI_NON` (đầu `tou` 1,5; lõi 1,2; vành cổ
  0,82 kéo theo giáp vai × 0,9; phiến bên 0,72–0,75; phiến lưng 0,72; kiếm `bone11` 0,75, năm kiếm bay nhỏ theo), bớt bốn phiến lưng `AN_NON`. Mảnh
  riêng đọc ở `inbox/dat_nung_non/manh_part2/`, thiếu thì lấy của dạng 2.
- Hình bố cục: `DN_NON=1 py -3 -I dat_nung_rig.py bo_cuc` → `inbox/dat_nung_non/mau/bo_cuc_non.png`. Concept hai phương án: `dat_nung_da.py non` →
  `gui_gpt/dat_nung_non/luot_1_concept_theo_bo_cuc.txt`, `…_tron_hon.txt` → `inbox/dat_nung_non/tai_ve/L1_*.png`. Chờ người dùng chọn.
- Còn phải làm sau khi chọn: gen mảnh đầu, giáp vai, vành cổ, kiếm theo concept; rig; clip `evolve` (`quai/tienhoa.py`); `doi_dat_nung.py chep_non` +
  `dang_1`; "Gắn dạng .atomik"; soi trong trận.

### 6d (tiếp). Dạng 1 đã vào game (2026-11-14 ~21:10)

- Người dùng chọn concept **A** (mặt nạ thú non): `inbox/dat_nung_non/tai_ve/L1_duyet.png`. Lưu ý: lúc chọn người dùng đang theo dõi từ thiết bị khác,
  trang so sánh chỉ mở trên máy này nên có thể họ chưa nhìn thấy hình; đã gửi ảnh qua SendUserFile sau khi lắp xong.
- Mảnh vẽ riêng (tờ G, K, W → `inbox/dat_nung_non/manh_part2/`): đầu, hai vành cổ, hai giáp vai, kiếm (kiếm dùng lưới 4 đỉnh bám `bone11`; `bone185`
  đứng yên so với `bone11` trong mọi clip). Bảng chỉnh: `CHINH_NON["P_tou"] = (0,72; +20; +60)`, `TI_NON["bone11"] = 0,58` (bản đầu đầu và kiếm to quá,
  che lõi và giáp vai xa).
- Rig `inbox/dat_nung_non/rig/` (425 KB, 146 xương, 157 slot, 8 clip nối về idle 0 px); `dat_nung_non.py th` gộp clip `evolve` →
  `dat_nung_non_th.atomik` (578 KB, vượt trần 0,5 MB của file thường vì mang cả dạng 2 bản nhẹ; khung cuối trùng khung 0 idle dạng 2).
- Vào game: `doi_dat_nung.py chep_non` + `dang_1` → `Resources/dat_nung_non`, dạng 1 "Viêm Dũng Nhi" cỡ 0,85, dạng 2 cỡ 0,95; "Nhập dữ liệu", "Gắn
  dạng .atomik". Tour "riêng Viêm Dũng Nhi (dạng 1)": ba đòn chạy đúng (tờ `inbox/dat_nung_non/trong_game/tran_*.jpg`). CHƯA chạy lại EditMode sau
  bước này (số dạng không đổi nên golden không đổi; phiên assets-4c đang dùng Unity).
- Ảnh động từng clip để người dùng xem từ xa: `[DN_NON=1] … inbox/dat_nung_non/_xem_dong.py` → `<rig>/dong/<clip>.webp`; trang gom sẵn ở scratchpad
  (chưa đăng artifact: ngoại lệ đăng artifact của người dùng chỉ cho một lần trang xem dạng lớn).
- SỰ CỐ đã sửa: gõ `quai/vao_game.py --help` thì script chạy thật (không có `--help`), chép đè `Resources/han_ngac_2` và `tho_hoang_1` (atomik + chân
  dung) bằng rig cũ trong inbox. Đã khôi phục bốn file bằng `git show HEAD:<file> > <file>`, mã băm khớp HEAD.

## 7. Việc tiếp

1. Người dùng xem dạng 1 (ảnh đã gửi) và góp ý; chạy lại EditMode khi Unity rảnh; soi cỡ 0,95 của dạng lớn, ô xem tướng, phía địch, appear / die trong trận.
2. Vào game khi người dùng bảo (suất 8 = `huyen_viem`, ải 50: tên, id, số dạng, thẻ hỏi lúc đó; `quai/doi_*.py` làm mẫu). Chân dung: `rig_moi/chan_dung.png`.
3. VFX ngoài rig theo sự kiện đã đặt (vệt kiếm, dung nham lúc `dam` / `chem`, kiếm phân thân `phan`, nổ lúc `cham`, bụi lúc `cham_dat`).
4. Dạng 1 (nếu người dùng muốn hai dạng như các suất khác).
