# Tinh linh rừng mập (`tinh_linh`): tướng thứ 2 đảo Mộc

Bắt đầu 2026-11-12. Con gốc của rig: `monster_3407` (game tham khảo, kho `D:\Ripper\SwordxStaff`). Xương, lưới, chuyển động gốc là
của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình.

## 1. Lời dặn của người dùng (2026-11-12)

- Concept: tinh linh rừng **chubby cute** như con gốc, **hơi trong suốt nhẹ** (người dùng biết texture vẽ tay khó làm trong suốt).
  Tạo hình mập giống con gốc; **phần tóc trên đầu tuỳ Claude**.
- idle: giống họ; thi thoảng mắt nhìn loanh quanh; thi thoảng tay đánh bụng, bụng rung rung.
- Đánh thường: lao tới dùng tay tát đối thủ.
- Chiêu mana: **gen thêm mồm**; há mồm bắn nhiều lá cây vào người đối thủ.
- Chiêu cuối: phình to cơ thể, dùng bụng lao thẳng vào đối thủ, bật nảy lại, bụng rung rung kiểu béo béo cute.
- Thêm `walk`. `die` giống họ. `appear` rơi từ trên trời xuống.

Trả bản đầu (2026-11-12, cùng buổi):
- "nhìn giống con gốc quá" → đổi hẳn tóc, màu, thứ trong bụng (mục 3).
- "mắt làm chỉ lòng trắng thôi" → bỏ con ngươi; "nhìn loanh quanh" = cả mắt trượt trên mặt như họ (`bone13`).
- "miệng gen thêm chỉ bật khi bắn chiêu, miệng cũng hình tròn tròn thôi, xem tướng 1 đảo thủy" → lúc nghỉ KHÔNG có mồm; mồm tròn kiểu
  Tí Tách (bầu dục sẫm, bên trong một mảng nhạt, không viền mực) chỉ hiện trong clip chiêu mana.
- "tát chứ không phải hất tay lên, tay tát phải đưa từ trái sang" → bỏ cú vung tay vòng qua đầu của skill_01; tay quét NGANG từ trái
  sang phải. "walk làm thành nhún xuống bật lên" → walk là chuỗi cú nhảy, không lạch bạch.
- "anim đánh thường là lao vào tát cơ mà" → clip phải thấy rõ quãng LAO rồi mới tát (bản đầu chỉ chồm tại chỗ).
- "sao nhìn animation demo giật thế" → GIF 12–20 khung/giây nhìn giật; đổi sang trang xem sống 60 khung/giây (runtime Spine thật).

Màu, chi tiết, tên: người dùng chưa dặn. Bảng màu và chi tiết ở mục 3 là **đề xuất của Claude**, chờ duyệt concept.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3407/`: `info.json`, `att_goc.json`, `manh_anh.png`, `manh_dang_goc.png`, `parts/`, `khung/`)

82 xương, 43 slot (42 hình; slot `shadow` trống, 5 slot `P_SL_bq2..6` trống), 11 clip, atlas 216 × 1608 (tỉ lệ 0,5). Con gốc nhìn sang
phải: không lật. Không có chân, **không có mồm**.

Cây xương:
- `bone` → `bone2` → `bone3` (THÂN: dời, xoay, co giãn) → tay trước `bone5-6-7` (bên trái người xem), tay sau `bone8-9-10`, hai góc đáy
  bụng `bone11` / `bone12` (IK có giãn tới `R` / `L` nằm trên đất, con của `bone2`), gốc mầm cây trong bụng `bone15` → các chuỗi `bone16–38`.
- `bone2` → `bone43` (dời đầu) → `bone44` (xoay đầu) → `bone4` (đầu; chỉ thừa hưởng độ dời) → `bone13` (mắt), `bone14` (gốc tóc) → 8 chuỗi
  lá 2–3 đốt (`bone39..48`) và hai dây leo 4–5 đốt (`bone49..`, `bone50..`).
- `bone` → `bone51` → `bone52–56`: năm lá nhỏ trôi lơ lửng trong thân.

Cách họ làm độ trong (thứ tự vẽ sau → trước):

| # | hình | là gì | bám xương |
|---|---|---|---|
| 1–2 | P_shouLB, P_shouLA | tay sau: lớp SAU (đậm, đặc) và lớp TRƯỚC (nhạt, giữa trong suốt) | bone3, 8–10 |
| 3 | P_shouRB | tay trước, lớp sau | bone3, 5–7 |
| 4–5 | P_shentiB, P_tou2B | bụng và đầu, lớp SAU (đậm, đặc) | bone3, 4, 11, 12 |
| 6–21 | D_* | mầm cây trong bụng (cuống, lá, hai quả cầu) + 5 lá trôi `D_Pyezi*` | bone15…38, bone52–56 |
| 22–23 | P_shentiA, P_tou2A | bụng và đầu, lớp TRƯỚC: viền + vệt bóng đặc, lòng trong suốt dần | như lớp sau |
| 24 | P_SL_bq1 (đổi sang bq2..6) | hai mắt, một ảnh | bone13 |
| 30 | P_shouRA | tay trước, lớp trước (đè lên thân) | bone3, 5–7 |
| 31–42 | T_yezi*, T_qiu*, T_meimao* | tóc: 8 lá, hai quả cầu trên hai dây leo | bone14 và các chuỗi |

Mỗi khối thân là HAI lớp cùng lưới (sau đặc, trước trong lòng), mầm cây kẹp ở giữa → nhìn xuyên được.
Bộ mắt: bq1 thường; bq2 xếch giận (mở to); bq3 xếch hẹp; bq4 "> <"; bq5 nhắm (nét lượn); bq6 nửa nhắm có mày (gồng).
Clip của họ: `idle_01` 4 s (thở, tay trước vẫy nhẹ 0,9–1,6 s, mắt trượt sang trái rồi về), `skill_01` 1,33 s (vung tay trước vòng qua
đầu: lấy đà 0–0,5, tát 0,5–0,63), `skill_02` (ôm bụng rồi xoè hai tay), `skill_03` (giơ tay phồng người rồi nện xuống 1,07),
`skill_04` (đánh tay sau), `run_01` 1,6 s (4 nhịp lạch bạch 0,4 s, tay dang), `hit_01/02`, `die_01` 1 s (đổ ra sau, chảy bẹp), `stun_01`.

## 3. Concept dạng 1 (đề xuất của Claude, chờ người dùng chọn)

Bản đầu (`tai_ve/L1_ban_dau_bi_tra.png`: thạch lục, vòng lá hai tông, hai nụ hồng trên dây leo, mầm cây trong bụng, mắt có con ngươi,
mồm chữ w) bị trả vì tôi giữ nguyên hình bóng MỌI part của con gốc, kể cả tóc và mầm cây: đổi màu và nét không đủ khác.

Lượt 2: sơ đồ bố cục chỉ còn thân + tay + mắt (`tinh_linh.py bo_cuc` → `mau/bo_cuc_<hướng>.png`); tóc và thứ trong bụng tả bằng lời,
sẽ là mảnh riêng của mình gắn lên các chuỗi xương tóc / xương mầm cây của họ. Ba hướng đã gen đủ (tờ so `inbox/tinh_linh_1/so_ba_huong.png`), cả ba đạt điểm kiểm, chờ người dùng chọn (`build_tinh_linh.py`, mỗi hướng một file
`gui_gpt/tinh_linh_1/luot_1_concept_<hướng>.txt` → `tai_ve/L1_<hướng>.png`):

| hướng | thân | tóc | trong bụng |
|---|---|---|---|
| `mam` | matcha non `#C8DE8E` | một mầm hai lá mập to xoè chữ V + vòng lá con ở gốc | hạt giống nâu nứt vỏ, rễ cong, ba bong bóng |
| `nam` | kem đào `#F6D9B8` | mũ nấm đỏ gạch đốm kem to quá cỡ + một nấm con | bào tử tròn trôi + một nấm tí hon |
| `ho_phach` | mật ong hổ phách `#EDB85A` | mũ rêu + hai cành non chẻ đôi như gạc nai, mỗi cành một lá | một chiếc lá kẹt như côn trùng trong hổ phách + bong bóng |

Chung: mắt bầu dục trắng trơn, vành dày màu thân đậm (kiểu Tí Tách, ảnh mẫu 2); má hồng; không mồm; thân tô phẳng, không vệt bóng.

Độ trong ở rig (dự định): giữ hai lớp như họ; lớp TRƯỚC của mình = viền mực + dải mép đặc, lòng giảm alpha còn ~60% bằng mã; thứ trong
bụng vẽ màu thật ở giữa hai lớp nên tự nhạt đi và lắc lư theo xương của nó.

## 4. Clip (dựng ở tầng điều khiển của rig gốc: `tinh_linh_clip.py`)

Xem thử trên rig gốc (hình của họ, nội bộ): `<SXS>/scan/monster_3407/lam_clip/xem/xem.html` (`tinh_linh_clip.py song`: trang sống 60
khung/giây, nút từng clip, tốc độ 1× / 0,5× / 0,25×; mở bằng file://). `gif` chỉ ra GIF ít khung, nhìn giật.

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| tl_idle | 8 s lặp | hai vòng idle_01: vòng một nguyên của họ (mắt trượt sang trái rồi về); vòng hai tay trước giơ ra rồi vỗ bụng 5,20 và 5,56, mắt nhắm, bụng rung tắt dần, đầu tóc nảy trễ | vo_bung 5,20; 5,56 |
| tl_walk | 0,9 s lặp | mỗi vòng MỘT cú nhảy tại chỗ (người dùng: "nhún xuống bật lên"): nhún bẹp 0,24; bật 0,32; đỉnh 0,49 cao 92, tay hất lên; đáp 0,68 bẹp, bụng nảy. Game lo dời ngang | |
| tl_attack | 1,34 s | nhún 0–0,16; LAO 0,16–0,44 (chúi 13°, tay trước duỗi ngang ra sau); TÁT NGANG 0,44–0,56: tay quét từ trái sang phải trên một đường ngang ngực qua trước bụng (giữa đường tay co ngắn), kết thúc duỗi gấp đôi vượt mép thân; khựng tới 0,70; nhảy lùi về 1,20. Thân, đầu, tóc theo skill_01 (bớt cú nhảy dựng), TAY TRƯỚC tự dựng (hàm `tay_thang`) | trung 0,56 |
| tl_cast | 2,0 s | hít phồng hai nấc, ngả sau tới 0,46; gập tới, HÁ MỒM 0,56; giữ há rung giật tới 1,50; ngậm, thở phào, bụng rung | phun 0,56; het_phun 1,50 |
| tl_skill | 2,7 s | (người dùng: "phình phần bụng ra cho béo là chủ yếu, tăng sự nảy nảy của bụng") bơm ba nấc, chỉ BỤNG béo ra (ngang ~1,5, cao ~1,2 lần; đầu +8%, tay giữ cỡ), mỗi nấc rung; ngả lấy đà; lao ưỡn bụng 0,74–0,90; húc, bẹp ngang, khựng tới 0,98; bật về theo cung cao, bụng lắc trong lúc bay; về chỗ NẢY ba lần (đáp 1,46 / 1,80 / 2,02, nảy cao 48 rồi 20), mỗi lần bẹp và rung mạnh tắt dần, tay vỗ theo; 2,07 xì hơi | phinh 0,60; trung 0,90; dap 1,46; 1,80; 2,02 |
| tl_appear | 1,8 s | rơi 0–0,40 (giãn dọc, tay tóc thốc lên); chạm đất bẹp dí; nảy; đáp lần hai 0,98, rung; mở mắt, lắc người, liếc hai bên | cham_dat 0,40; dap 0,98 |
| tl_hit, tl_die | 0,5 s; 1,0 s | nguyên hit_01, die_01 của họ | |

- Cung lao (`BAY`, đơn vị con gốc, đặt lên xương `move` ở rig của mình): đòn thường chạy tới trước 420 rồi mới tát (đỉnh giữ suốt cú tát); chiêu cuối lùi 22
  rồi lao 200, bật về nảy cao 96, về chỗ nảy thêm 48 và 20; appear rơi từ 640.
- Kênh riêng của rig mình ghi ở `<scan>/kenh_rieng.json`: `mieng` (0..1: mồm tròn hiện và to dần, chỉ clip cast), `bay`, sự kiện
  (`nguoi` còn trong file nhưng KHÔNG dùng: mắt chỉ lòng trắng).
- `than()` phồng / giãn / nghiêng cả khối quanh điểm tì đất (đáy bụng giữ trên đất, đầu ngồi theo đỉnh bụng); `lac_bung()` là nhịp rung
  mỡ (phình ngang – xẹp dọc, hai góc đáy xoè); `rung()` dao động tắt dần.
- Chạy `tinh_linh_clip.py xem` từ PowerShell: đối số rỗng bị bỏ, dùng `het` cho "mọi clip".

**Người dùng chốt hướng `mam` (mầm hai lá) 2026-11-12** → `inbox/tinh_linh_2/tai_ve/L1_duyet.png` (là DẠNG 2, xem mục 7). Clip: "ổn".

## 5. Mảnh (làm hết bằng mã từ concept đã duyệt, không gen thêm: `tinh_linh_manh.py lam`)

Nét của game tô phẳng nên không cần Codex vẽ tờ mảnh. Ra `inbox/tinh_linh_1/manh/` (+ `dat.json` chỗ đặt mảnh riêng, `_so_ghep.png` ghép dáng
gốc cạnh concept, `_mat.png` sáu bộ mắt):
- **Thân** (`bung` = P_shentiB, `dau` = P_tou2B, `tay_gan` = P_shouRB, `tay_xa` = P_shouLB; lấy lớp SAU của họ vì lớp trước lòng trong
  suốt nên hình bóng thủng): hình bóng kín của part (làm trơn, lấp lỗ, cắt theo mép lưới của họ), tô bằng **ô vân sáp lát** 160 px lấy
  từ thân trên concept, lát theo toạ độ THẾ GIỚI (đầu chồng lên bụng không lộ đường nối), viền mực kẻ bằng mã có bề dày rung nhẹ.
  Đầu: mép dưới nằm trong bụng không mực, hai nếp gấp lục ngắn, má hồng. Tay trước: đầu vai trong thân không mực.
- **Mắt** `mat1..6` (bq1..bq6): chỗ họ tô trắng → trắng, phần còn lại của hình bóng → vành lục `(73, 116, 37)`; vành nới mảnh lại ~7 đơn vị.
- **Tóc** `toc` (hai lá + cuống + vòng lá, một mảnh) và **trong bụng** `hat` (hạt + rễ + mầm), `bong1..3`: cắt thẳng từ concept theo màu.
- **Mồm** `mieng`: bầu dục lục sẫm + mảng lưỡi hồng, không viền mực (kiểu Tí Tách), 68 × 80 đơn vị, tâm ở (906, 594) trên khung concept.
- **Bụng lấy BAO LỒI của hình bóng** (người dùng 2026-11-12, ảnh chụp cú tát: "lõm mất 1 mảng người bên trái"): hình bụng của họ
  khuyết ba chỗ (hõm bên trái dưới tay trước, hõm trên chỗ đầu ngồi, khấc trên phải), hình họ trong mờ lại có tay và đầu che; hình
  mình đặc, tay vung đi là lộ mảng lõm. Lưới của họ vẫn phủ tới đó nên chỉ cần tô đầy. Soi mọi part thân trên nền xám kèm lưới
  (`manh/_luoi_than.png`) trước khi lắp, đừng chỉ xem tờ ghép dáng gốc (tay đang che chỗ khuyết).
- Lỗi đã gặp: bộ mắt bq2 bị cắt cụt vì vùng atlas xoay 90° mà đổi chỗ rộng / cao lần nữa (`tinh_linh.luoi`: cỡ đã cắt là cỡ CHƯA xoay;
  `to_manh.to_dang` còn lỗi này ở ô chữ nhật xoay, chỉ ảnh hưởng tờ xem).

## 6. Rig (`tinh_linh_rig.py` → `inbox/tinh_linh_1/rig/`)

34 xương, 16 slot, 2632 đỉnh, 4625 tam giác, 8 clip, `.atomik` 0,21 MB; nối clip 0 px; runtime Spine thật dựng đủ 8 clip
(`rig/spine_that/`).
- **Lưới dày + mỡ bụng** (người dùng 2026-11-12: "chia mesh / đỉnh thêm nữa cho mềm mại hơn và bụng rung mượt hơn"; bản đầu dùng nguyên
  lưới thưa của họ: bụng 23 đỉnh, đầu 15, nên lúc bẹp / phình viền gãy khúc). `gan_day`: lưới đều của mình trên cùng hình (bụng 1027
  đỉnh, đầu 499, mỗi tay ~245, tóc 573); mỗi đỉnh lấy trọng số nội suy theo toạ độ trọng tâm từ lưới thưa của họ rồi làm trơn 6 vòng
  (chỉ nội suy thì vẫn gãy đúng theo tam giác của họ), điểm gắn theo ma trận dáng gốc đã áp IK. Thêm ba xương mỡ bụng `mo_g`, `mo_t`,
  `mo_p` (con `bone3`, vùng ảnh hưởng hình chuông, tới 75% trọng số; đáy và đỉnh bụng không rung) chạy **lò xo điểm** `Nay` (3,3 Hz,
  giảm chấn 0,2, lệch tối đa 11–15 đơn vị): bụng tự trễ, vọt quá, rung tắt dần theo mọi chuyển động của thân ở mọi clip. Hạt giống
  theo `mo_g`, bong bóng theo `mo_t` / `mo_p`.
- Giữ của họ: `bone, bone2, bone3, bone43, bone44, bone4, bone5–10, bone11, bone12, bone13, bone14, bone15`; lưới bụng, đầu, hai tay
  nguyên đỉnh / tam giác / uv / trọng số. **bone4 của họ "chỉ thừa hưởng độ dời"**: rig mình thừa hưởng thường nên góc riêng bone4
  trừ tổng góc các xương cha (`bone, bone2, bone43, bone44`; các xương đó không co giãn nên tương đương).
- **Tay trước bám trọn `bone5`** thay cho nửa `bone3`: tay vung quá 90° (cú tát) thì gốc tay co rúm thành răng cưa trên mép bụng; hình
  của họ trong mờ nên không lộ, hình mình viền mực nên lộ. Tay sau nấp sau thân: giữ trọng số của họ (đổi thì hở ở vai).
- Một lớp thân đặc (không làm hai lớp trước / sau như họ): thứ trong bụng vẽ TRÊN bụng, đã nhạt màu sẵn trong concept nên vẫn đọc là
  "nhìn xuyên thạch". Thứ tự vẽ: tay sau, bụng, hạt, ba bong bóng, đầu, sáu bộ mắt, mồm, tay trước, tóc.
- Xương riêng: `toc_goc` (con `bone14`) → `la_trai0..2`, `la_phai0..2` (chuỗi dọc gân lá, có lò xo `LoXo`, mượn góc lắc của chuỗi lá
  `bone39..` / dây leo `bone49..` của họ × 0,3–0,4); `hat` (con `bone15`, mượn góc `bone16`); `bong1..3` (con `bone3`, trôi nhẹ);
  `mieng` (con `bone4`: mồm + chỗ nhả lá). Lá trái rủ thấp hơn vòng lá: vùng "bám cứng gốc" phải chặn theo cả x, không thì lá rách.
- Kênh riêng từ `kenh_rieng.json`: `bay` → xương `move`; `mieng` → độ đậm + cỡ mồm (chỉ `cast`). `game`: `stay` = cast, `lunge` = skill,
  chiều cao = đỉnh đầu + 45% mầm lá (tính cả lá thì thân bị thu nhỏ so với tướng khác).
- Xem: `inbox/tinh_linh_1/rig/xem.html`; tờ khung `khung_<clip>.png`; `tinh_linh_rig.py soi <clip> <giây,...> [tỉ lệ]`.

## 7. Hai dạng (người dùng 2026-11-12: "ok làm dạng 1 đi, con này là dạng 2")

Con mầm hai lá là **DẠNG 2** (`tinh_linh_2`: thư mục `inbox/tinh_linh_2`, `gui_gpt/tinh_linh_2`, đổi tên từ `_1`). **Dạng 1** làm sau,
cùng rig, cùng clip. Mọi script đọc dạng ở biến môi trường **`TL_DANG`** (1 | 2, mặc định 2): `tinh_linh.py`, `build_tinh_linh.py`,
`tinh_linh_manh.py`, `tinh_linh_rig.py` (`tinh_linh_clip.py` dùng chung cho hai dạng).

Dạng 1 "hạt mầm" (người dùng không tả: thiết kế là ĐỀ XUẤT của Claude, **chờ duyệt concept**): cùng thân, cùng mắt, non hơn: thân lục
nhạt `(228, 242, 155)`, trên đầu MỘT mầm cong tí hon có một lá còn gập, trong bụng hạt nâu CHƯA nứt (chỉ ló đầu rễ) và hai bong bóng.
- Prompt `gui_gpt/tinh_linh_1/luot_1_concept_hat.txt` (đính thêm concept dạng 2 đã duyệt làm ảnh 2: "cùng con, bản non hơn"); ảnh
  `inbox/tinh_linh_1/tai_ve/L1_hat.png` (lượt đầu, 72 giây, đạt điểm kiểm), tạm chép thành `L1_duyet.png` để dựng thử.
- Mảnh: `TL_DANG=1 tinh_linh_manh.py lam` (ngưỡng cắt tóc và màu thân theo dạng: `TOC_MAU`, `THAN`...).
- Rig: tóc một chuỗi 4 đốt `mam0..3` (cuống lên, vòng qua đỉnh, lá rủ), có lò xo. Bản đầu `KG` 0,38, tỉ lệ y như dạng 2 → người dùng:
  **"dạng 1 cho nhỏ hơn chút, chibi hơn, mặt cũng chibi hơn"**. Làm ngay ở rig, không gen lại: `KG` 0,34 (≈ 74% dạng 2); `DAU_TI` 1,17
  (tỉ lệ dáng gốc của xương đầu `bone4`: đầu, mắt, mồm, tóc to ra quanh tâm đầu; mảnh đặt theo thế giới như tóc, mồm đổi chỗ bằng
  `dau_tg`); `MAT_TI` 1,24 + `MAT_HA` 7 + `MAT_TRAI` 14 (xương mắt `bone13`: mắt to, thấp hơn, dời trái cho mắt phải không thò khỏi
  mép đầu); má hồng trên ảnh đầu hạ 15 đơn vị và to 1,22 lần (`MA_HA`, `MA_TO` ở `tinh_linh_manh.py`).
  31 xương, 2188 đỉnh, `.atomik` 0,17 MB; runtime Spine thật dựng đủ 8 clip. Ảnh so hai dạng cùng tỉ lệ: `inbox/tinh_linh_1/so_hai_dang.png`.
- Người dùng duyệt ("ok ổn rồi, thay vào game đi", 2026-11-12).
- **Tiến hóa**: dạng 1 gộp BẢN NHẸ của dạng 2 (`TL_DANG=2 TL_NHE=1 tinh_linh_rig.py nhe` → `inbox/tinh_linh_2/rig/_nhe.pkl`: ảnh 0,72 lần,
  lưới thưa 1,8 lần; chạy ở tiến trình riêng vì cấu hình theo dạng đọc lúc nạp mô-đun; `tinh_linh_rig.py` của dạng 1 tự gọi). Clip
  `evolve` 2,8 s của `tienhoa.clip_tien_hoa`: dạng 1 nhún lấy hơi, gồng phồng bụng, rung; tan 1,05–1,35 s; dạng 2 hiện, vươn người,
  hai lá xoè bật ra; khung cuối trùng khung 0 idle dạng 2 (lệch 0,00 px). Không đổi bộ mắt lúc gồng: bộ tan hình chỉ lo slot đang hiện
  mặc định (bật `mat4` thì nó còn lại sau khi dạng 1 tan). Dạng 1 có tiến hóa: 65 xương, `.atomik` 0,24 MB.
- **Cỡ trong game**: game quy mỗi dạng về cùng chiều cao theo `game.height` rồi nhân `size` của `heroes.json` (0,9 / 1,02), nên `KG` nhỏ
  ở rig không làm con nhỏ đi trong game. Khai `game.height` dạng 1 lớn hơn thật 1,19 lần (`CAO_GAME`) để thân dạng 1 = 74% thân dạng 2.

## 8. Vào game (2026-11-12)

Suất **tướng thứ 2 đảo Mộc = ải 5 = id `hoa_nhuy`** (`IslandGen.Plan Moc`). Làm như các suất đã thay ở đảo Thủy: giữ id, chỉ số, thẻ, chỉ
thay rig. Chép tay (KHÔNG chạy `quai/vao_game.py` trên máy này: nó chép lại rig mọi tướng trong `da_nhan.json`, có rig cũ / thiếu):
- `inbox/tinh_linh_1/rig/tinh_linh_1.atomik` + `chan_dung.png` → `Assets/03 Art/Heroes/Resources/hoa_nhuy_1/hoa_nhuy_1.atomik`,
  `hoa_nhuy_1_portrait.png`; `tinh_linh_2` → `hoa_nhuy_2`.
- `hoa_nhuy` đang khai **3 dạng**, dòng mới có 2: **dạng 3 TẠM dùng lại rig dạng 2** (`hoa_nhuy_3` = `tinh_linh_2`), để dòng không tiến
  hóa thành tiên hoa cũ. Số dạng không đổi nên không đổi golden. Chờ người dùng: vẽ dạng 3 thật, hoặc rút còn 2 dạng (phải tính lại
  golden roster / sim và chạy test trong Unity).
- Đã kiểm bằng `vao_game.check_rig`: không lỗi; cảnh báo `game.shadow` không có slot (như các rig reskin khác), dạng 2 thiếu `evolve`.
- Unity (đang mở, cầu MCP không chạy): đưa cửa sổ lên trước cho nó tự nhập; `Editor.log` ghi đã nhập 3 `.atomik` + 3 chân dung, không
  lỗi. **Chưa xem trong trận / hộp chi tiết tướng** (không có MCP để chụp).
- Ghi vào `quai/da_nhan.json` (mục `hoa_nhuy`).
- CHƯA đổi: tên tướng ("Hoa Nhụy", "Tiên hoa nhụy đỏ"), tên dạng ("Thú Ba Lá", "Thú Búp Hoa", "Tiên Hoa Nhụy"), tên thẻ: không còn khớp
  hình, chờ người dùng đặt. Chiêu mana đang bắn tia mặc định của game từ xương `mieng`; lá bay là VFX chưa làm.

### Dạng 3 và tiến hóa mới (người dùng 2026-11-12: "làm thêm dạng 3 cũng được, animation tiến hóa hơi xấu, có thể làm animation là dạng 1 nhảy lên cao hẳn sau đó dạng tiếp theo rơi xuống")

- **Dạng 3 "nở hoa"** (`TL_DANG=3`, `inbox/tinh_linh_3`; người dùng không tả: thiết kế là ĐỀ XUẤT của Claude, concept `tai_ve/L1_hoa.png`
  lượt đầu): cùng thân, cùng mắt; thân lục đậm hơn `(152, 205, 82)`; trên đầu MỘT bông hoa san hô năm cánh nhuỵ vàng nở giữa hai lá
  lớn; trong bụng một quả hồng có cuống lá + ba bong bóng. `KG` 0,50. Tóc ba chuỗi (`la_trai`, `la_phai`, `hoa` = cuống + hai nửa bông
  hoa), có lò xo. Cắt tóc theo từng nhóm màu (`TOC_MAU kieu="hoa"`: vòng lá rất gần màu thân nên không cắt theo "khác màu thân" được).
  Dòng thành hạt mầm → mầm hai lá → nở hoa. Ảnh so ba dạng: `inbox/tinh_linh_3/so_ba_dang.png`.
- **Tiến hóa mới** (thay bản "gồng rồi tan" của `tienhoa.clip_tien_hoa`, viết riêng trong `tinh_linh_rig.py`, 2,86 s): dạng cũ từ dáng nghỉ
  nhún sâu (0,42), bật 0,50 rồi vọt thẳng lên, giãn dọc, mờ hẳn trong 0,26 s (bay lên 0,8 chiều cao game: mép trên khung sticker);
  một nhịp trống; 1,02 dạng sau RƠI xuống bằng đúng clip `appear` của nó (bẹp dí 1,42, nảy, đáp lần hai, rung, mở mắt, lắc người);
  0,3 s cuối hoà về khung 0 idle dạng sau (lệch 0,00 px). Sự kiện `tu_luc` 0,2, `nhay` 0,50, `doi_dang` 1,02, `cham_dat` 1,42.
  Dạng sau trong rig gộp dùng chung mẫu chuyển động (`dang_sau`: xương `n_*`, độ dời nhân tỉ lệ `KG` hai dạng), có lò xo riêng.
  Cả dạng 1 (gộp bản nhẹ dạng 2) và dạng 2 (gộp bản nhẹ dạng 3) đều có. `SO_DANG` tự thành 3 khi `inbox/tinh_linh_3/manh/dat.json` có.
- Người dùng duyệt dạng 3 và tiến hóa ("tiến hóa ổn", "ok dạng 3 ổn, cho to hơn dạng 2 1 chút nhé"): `KG` dạng 3 0,50 → 0,54 (thân to hơn
  dạng 2 ~17% ở rig); trong game cỡ do `size` (1,02 / 1,14) và `game.height` quyết nên khai `CAO_GAME` dạng 3 = 0,94 (to hơn dạng 2 ~19%;
  để nguyên chỉ ~12%).
- Bẫy khi chép vào game: chép file và đưa cửa sổ Unity lên trước phải chạy NỐI TIẾP (hai lệnh gọi song song thì Unity nhập trước khi file
  chép xong, người dùng mở game không thấy dạng 3: "dạng 3 đâu"). Kiểm bằng số dòng `Editor.log` trước / sau.
- Xuất theo thứ tự 3 → 2 → 1 (`TL_DANG=k tinh_linh_rig.py`). `.atomik`: dạng 1 0,25 MB, dạng 2 0,30 MB, dạng 3 0,23 MB.
- Đã chép lại cả ba vào `Resources/hoa_nhuy_1..3` (dạng 3 thật thay bản tạm), Unity nhập không lỗi (`Editor.log`).

### Kiểm trong Unity và hiệu ứng lá (2026-11-12, có MCP; cổng **8080**, không phải 8090)

- Menu `PokiClash/Tướng/Chụp thử dạng .atomik (mọi clip)`: game nạp đủ ba dạng (`Library/PokiHeroShots/hoa_nhuy_atomik_1..3.png`): khung trúng
  attack 14, cast 14, skill 22 (25 khung/giây); attack và skill có lao, cast đứng yên; dạng 1, 2 có `evolve`.
- **Bộ hạt Mộc đầu tiên trong game** (đảo Mộc chưa có bộ hạt nên trước đó chiêu mana bắn tia cũ):
  - Ảnh hạt lá: `ArtGen/Spine/la.py` → `Assets/03 Art/Fx/Hat/hat_leaf_<0..3>.png` (xám có gân, nhuộm), `hat_leafs_<i>.png` (trắng đặc làm
    mực). Chạy lại hai menu `PokiClash/Prefab/Sàn đấu: hạt lửa (bộ Hỏa)` và `…Hộp chi tiết tướng: hạt lửa + nút Mana` (134 ảnh).
  - `Assets/01 Script/Game/Battle/HatMoc.cs` (phần `partial` của `HatLua`): `Leaf` / `DrawLeaf` (lá xoay, lật nghiêng), `NLa` = **phun lá**
    (lúc hít lá nhỏ bị hút vào mồm; từ khung nhả 72 lá/giây bắn tới thân đối thủ trong 0,9 s, mỗi lá tự lái về một điểm trong thân,
    lượn; chạm thì vỡ mẩu lá + phấn; hết luồng nổ chùm lá), `NLaVa` = **cú húc bụng** (lá vỡ tung, sao vàng văng, bụi dưới chân).
  - Mã chiêu `n_la`, `n_la_va` đi chung đường bộ Thủy (`HatNuoc.PlayNuoc`, `HoldNuoc`, `NuocAtHit`); màu ở `WThemes["hoa_nhuy"]`;
    bảng `StageView.MocFx` (`FireMana` / `FireUlt` thêm nhánh hệ Mộc).
  - Tour `PokiClash/Thử/Đảo Mộc: hạt lá tinh linh rừng… (đang Play)` (`Editor/MocFxTour.cs`, dùng `ThuyFxTour.TryOnly`), ảnh ở
    `Temp/PokiShots/thuy_fx/hoa_nhuy_*`. Đã xem: mồm há đúng lúc, luồng lá ra từ mồm tới địch, cú húc nổ lá + sao, bật về đáp bẹp.
  - Bản đầu 40 lá/giây cỡ nhỏ nhìn thưa → 72 lá/giây, lá to gấp ~1,35.
- CHƯA xem: hộp chi tiết tướng (nút Mana, Chiêu, Tiến hóa), máy Android; bụi lúc rơi (appear) chưa làm vì game chưa phát clip `appear`.

## 9. Việc tiếp



1. Người dùng xem rig + clip trên hình của mình (`rig/xem.html`), chỉnh nếu cần.
2. Vào game: tên, suất đảo Mộc (id), chỉ số do người dùng đặt; chép `.atomik` + chân dung vào `Assets/03 Art/Heroes/Resources/`, menu
   nhập dữ liệu và gắn dạng `.atomik`.
3. VFX là lớp riêng: lá bay từ `mieng` (chiêu mana, sự kiện `phun` / `het_phun`), bụi lúc rơi (`cham_dat`), sao văng lúc húc (`trung`).
4. Tên tướng, tên dạng, tên thẻ; xem trong trận, hộp chi tiết, nút Tiến hóa khi có MCP Unity; người dùng duyệt hình dạng 3.

## 10. Đổi id và tên (2026-11-12, người dùng: "bạn tự sửa tên và id đi")

Mọi chỗ ghi `hoa_nhuy` ở các mục trên nay là **`mam_u`** (thư mục hình `Resources/mam_u_1..3`, prefab `mam_u.prefab`, ảnh tour
`Temp/PokiShots/thuy_fx/mam_u_*`, ảnh chụp `Library/PokiHeroShots/mam_u_atomik_1..3.png`).

- Tên do Claude đặt (người dùng chưa duyệt từng tên): tướng **Mầm Ú**, danh hiệu "Tinh linh hạt mầm bụng bự", "Dòng Mầm Ú"; dạng
  **Hạt Ú / Mầm Ú / Hoa Ú**; thẻ **Phun Lá** (mana, icon leaf), **Húc Bụng** (chiêu cuối, icon fist), **Bụng Nảy** (bị động, icon seed).
  Chỉ số, độ hiếm, số và hiệu ứng thẻ, cỡ dạng giữ nguyên.
- Script: `ArtGen/Spine/quai/doi_mam_u.py [--kiem]` (chạy lại không đổi gì thêm): heroes / cards / stages.json, mọi golden (chỉ thay id),
  IslandGen, StageView.MocFx, HatNuoc.WThemes, MocFxTour, da_nhan.json, GD_Claude/13, 14; bước chuyển bản lưu `MigrateMamU`
  (`SaveCodec.Migrations[7]`, saveVersion 7 → 8; script đọc số phiên bản từ balance.json vì phiên Gạc Đá đổi `de_hoa` → `gac_da` ngay sau).
- Thư mục hình và prefab đổi tên bằng `manage_asset move` của MCP Unity (giữ GUID). Công cụ báo "MoveAsset call failed unexpectedly"
  nhưng thực ra đã đổi; kiểm trên đĩa. Sau đó: refresh + biên dịch, `PokiClash/Nhập dữ liệu`, `PokiClash/Tướng/Gắn dạng .atomik vào
  prefab tướng` (sửa lại `res` trong `mam_u_<k>.asset`).
- Kiểm: EditMode 102/103 (chỉ hỏng `PrefabOnlyTests` có từ trước); chụp thử ba dạng qua AolaActor số liệu như cũ; tour trong trận
  (menu `PokiClash/Thử/Đảo Mộc: hạt lá Mầm Ú, …`) ra tên Mầm Ú, thẻ Phun Lá / Húc Bụng, luồng lá và cú húc như trước; console sạch.
- Chép rig mới sau này: đích là `Resources/mam_u_<k>/mam_u_<k>.atomik` + `mam_u_<k>_portrait.png` (vẫn chép tay, không chạy `vao_game.py`).
- Gói cũ của dòng Hoa Nhụy aola (`ArtGen/Heroes/gui_gpt/hoa_nhuy_*`, `forms_moc/hoa_nhuy_*.json`, `beasts_cfg.py`) để nguyên, không còn dùng.
