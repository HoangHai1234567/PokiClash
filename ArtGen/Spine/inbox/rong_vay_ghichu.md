# Rồng vây (mã làm việc `rong_vay`): tướng thứ 8 đảo Thủy (2026-11-11)

Tên chưa đặt; mã `rong_vay` chỉ để đặt thư mục. Gói prompt: `ArtGen/Spine/build_rong_vay.py` → `gui_gpt/rong_vay_1/`, ảnh về
`inbox/rong_vay_1/tai_ve/`. Sơ đồ bố cục: `ArtGen/Spine/rong_vay_bo_cuc.py` → `inbox/rong_vay_1/mau/bo_cuc.png`.

## 1. Ý người dùng

- "Tôi muốn làm tướng này là tướng thứ 8 đảo Thủy" (ảnh chụp `monster_3458` của game tham khảo); hỏi có khả thi tự gen bằng Codex
  cho chất lượng gần tương đương không.
- Sau khi nghe đánh giá: "trên những gì bạn vừa tách mảnh, **reskin rồi bắt đầu gen, animation tính sau**".
- Chưa dặn: tên, màu, chi tiết đổi, số dạng tiến hóa, chiêu. Màu và chi tiết trong concept là **đề xuất của Claude**, chờ duyệt.

## 2. Thiết kế đề xuất (hình của mình, chỉ giữ cách dựng của rig)

Rồng biển kiểu **cá chuồn hóa rồng**; mọi thứ là chất liệu cá và biển, không lông, lông vũ, mây, vân sáng như con gốc.

| Phần | Con gốc | Của mình |
|---|---|---|
| Thân | lam đen, bụng lam xám | chàm tím `#34408F`, vạch bụng kem `#F3E6C4` |
| Đầu | mỏ chim sẫm, mắt tím phát sáng không con ngươi, mảng lông trắng trên má | mõm ngắn có mỏ sừng màu cát `#E9BE6E` kiểu rùa biển, mắt hổ phách `#F2B33D` con ngươi dọc dưới gờ mày sẫm |
| Trên đầu | hai lông vũ trắng, tai lông trắng lớn | hai sừng cam san hô trơn `#F0704A`, vây tai có tia (lớn + nhỏ), vây mang trên má |
| Cổ, ngực | bờm lông trắng | vạch bụng kem chạy từ cằm xuống ngực |
| Lưng | tấm đá rêu khắc hoa văn xoắn | ba vỏ sò điệp kem gân cam |
| Vây lưng | buồm gai lam nhạt | buồm lam ngọc `#49BFC4` trên tia cam |
| Cánh | lưỡi dài, mép rách kiểu lửa, vân chòm sao phát sáng | cánh vây cá chuồn: sống cam, sáu tia, mép lượn sò tròn, đốm kem |
| Đuôi | vây đuôi nhạt kiểu cá voi | vây đuôi cá chẻ đôi có tia |

## 3. Mổ xẻ con gốc `monster_3458` (chỉ học cách tách và nhịp)

Nguồn: `D:\Ripper\SwordxStaff\web\assets\Monster\monster_3458\` (Spine 4.2.28, skel 645 KB, ảnh 1376 × 428, tỉ lệ atlas 0,5).
Kết quả quét: `D:\Ripper\SwordxStaff\scan\monster_3458\` (`info.json`, `att_goc.json`, `manh_anh.png`, `manh_dang_goc.png`,
`manh_dang_goc_nho.png`, tờ khung `khung/`, ảnh cận `can/idle_01.jpg`).

- 165 xương, 53 slot, 13 clip. **45 xương `yun*` và 11 mảnh mây `P_yun*` không clip nào dùng** (ẩn mặc định, không khoá): con thật
  khoảng 120 xương, 34 ảnh mảnh, 35 slot hiện.
- Lưới thưa: cả con 949 đỉnh, 992 tam giác; mảnh nào cũng là lưới có trọng số.
- Chỉ dùng xoay, dời, co giãn xương. Không bẻ đỉnh, không IK, không mặt nạ cắt, không sự kiện. Đổi ảnh: chỉ mắt mở ↔ mắt nhắm (hit,
  die, stun). Đổi thứ tự vẽ: một lần trong `die_01`. Tô màu: bóng dưới chân ở `skill_04_2/3`.
- 8 path constraint: `H_shenti..H_shenti8` chạy trên đường cong `shenti` (15 đỉnh, bám `quxian..quxian5`); 1 transform constraint
  kéo `weiba` theo `H_shenti8`. Vào `.atomik` thì nướng thành khoá thường (`chay.py sample`).

### Bảng mảnh (thứ tự vẽ sau → trước; cỡ là ảnh trong atlas, ngoài rig gấp đôi)

| # | Slot | Cỡ | Là gì | Xương bám |
|---|---|---|---|---|
| 12 | `P_yuqi16` | 128 × 108 | vây sau thân giữa | 2 |
| 13 | `P_weiba` | 161 × 146 | vây đuôi (sau cổ, bên phải) | 8: chuỗi `weiba` + `bone30..34` |
| 14 | `P_yuqi13` | 29 × 99 | vây nhỏ dưới vai | 2 |
| 15 | `P_yuqi12` | 61 × 147 | vây dưới thân cạnh gốc cánh | 3 |
| 16, 17 | `P_shenti06`, `P_shenti07` (cùng ảnh) | 90 × 166 | hai khúc đuôi mảnh, đi lên sau ngực | 4, 3 |
| 18 | `P_shenti05` | 282 × 180 | khúc thân đáy (khuất sau cánh gần) | 5 |
| 19 | `P_chibangL06` | 198 × 256 | màng cánh xa | 9 |
| 20 | `P_chibangR08_3` (ảnh `R08_2`) | 301 × 22 | dải cạnh cánh xa (nhìn nghiêng) | 4 |
| 21 | `P_chibangL05` | 90 × 261 | sống cánh xa | 7 |
| 22 | `P_yuqi11` | 72 × 52 | vây nhỏ trong lòng vòng cuộn | 3 |
| 23 | `P_yuqi10` | 99 × 121 | vây mép ngoài vòng cuộn | 3 |
| 24 | `P_yuqi15` | 114 × 203 | vây buồm cạnh gáy | 4 |
| 25 | `P_yuqi14` | 188 × 171 | cụm vây buồm lớn | 9 |
| 26 | `P_shenti04` | 166 × 305 | khúc vòng cuộn (chữ C bên trái) | 5 |
| 27 | `P_yuqi08` | 40 × 81 | vây nhỏ lòng vòng cuộn | 2 |
| 28 | `P_shenti03` | 234 × 207 | khúc lưng (mang giáp) | 4 |
| 29 | `P_yuqi09` | 151 × 89 | vây buồm trái | 3 |
| 32 | `P_yuqi07` | 177 × 104 | vây buồm | 4 |
| 33 | `P_yuqi06` | 121 × 75 | vây | 3 |
| 35 | `P_shenti02` | 260 × 182 | khúc ngực / thân giữa | 5 |
| 36 | `P_shenti01` | 181 × 163 | cổ (mang cả mảng ngực trước) | 6 |
| 37 | `P_erduo` | 43 × 25 | gờ mày / tai sẫm trên đỉnh đầu | 1 |
| 38 | `P_tou` | 161 × 86 | đầu | 3 |
| 39 | `P_yuqi05` | 112 × 76 | tai lớn | 4 |
| 40 | `P_yuqi04` | 108 × 61 | sừng sau | 3 |
| 41 | `P_yuqi03` | 65 × 61 | sừng trước | 3 |
| 42 | `P_yuqi02` | 62 × 34 | tai nhỏ | 2 |
| 43, 44 | `P_yanjing02`, `P_yanjing01` | 22 × 8, 27 × 12 | mắt nhắm (ẩn), mắt mở | 1 |
| 45, 46 | `P_zuiba02`, `P_zuiba01` | 41 × 20, 52 × 32 | mỏ dưới, mỏ trên | 1 |
| 47 | `P_yuqi01` | 68 × 55 | chùm má | 5 |
| 48 | `P_chibangR06` | 436 × 309 | màng cánh gần | 12 (ba chuỗi song song 3 đốt + xương mép) |
| 49 | `P_chibangR08_2` | 301 × 22 | dải cạnh cánh gần | 4 |
| 50 | `P_chibangR08` | 303 × 248 | sống cánh gần | 6 |

### Cây xương (rút gọn)

```
root → all → xy → zhixin (tâm thân)
  ├─ Q_shenti → Q_shenti2 → 3 → 4 → 5 → tou      nửa trước: thân, cổ, đầu (xoay thường)
  │    ├─ tou: bone10, 11 (mỏ), bone12–13, 15–17 (tai), 36–38, 39–41 (sừng), 44–46 (chùm má)
  │    ├─ R_chibang11 → 10 → 9 (+ chibangR08_1..6, R_chibang12..14, 21)   cánh gần: sống + mép
  │    ├─ R_chibang15 → 16 → 17, R_chibang18 → 19 → 20                    cánh gần: hai chuỗi màng
  │    └─ L_chibang → 2 → 3, L_chibang4 → 5 → 6, L_chibang7 → 8 → 9        cánh xa
  ├─ H_shenti .. H_shenti8        nửa sau: 8 xương chạy trên đường cong; vây bám làm con (bone71..92)
  ├─ weiba → 2 → 3 → 4 → 5        đuôi 5 đốt → bone30–34 (vây đuôi)
  └─ quxian .. quxian5            điểm điều khiển đường cong thân
```

### Mẹo diễn chính

1. **Thân = 7 khúc ống rời viền kín chồng mép** bám một chuỗi xương; nửa sau trượt trên đường cong nên vòng cuộn siết, nới, duỗi được.
2. **Cánh vỗ giả 3D**: sống cánh xoay 70–130°, ba chuỗi màng song song uốn màng như vải, cả cánh bị ép dẹt bằng co giãn xương khi
   nhìn nghiêng; lúc đó **dải cạnh mỏng 301 × 22** hiện ra thay bề mặt cánh. Idle đã vỗ cánh (1,33 s một vòng).
3. Vây, sừng, tai mỗi cái 2–4 đốt lắc trễ pha.

### Clip (13)

`idle_01` 1,33 s (1.315 khoá; thân 4 khoá mỗi xương, cánh 13–18 khoá mỗi xương), `run_01` 0,8, `skill_01` 1,37, `skill_02` 1,67,
`skill_03` 2,33 (chồm cổ cao, 6.031 khoá), `skill_04_1..3` 1,77, `hit_01` 0,5, `hit_02` 0,67, `die_01` 1,0, `stun_01` 2,0,
`block_01` 0,5.

## 4. Đánh giá khả thi (đã báo người dùng)

Tách mảnh, rig, chạy trong `.atomik`: làm được. Thân, đầu, vây, đuôi: gần tương đương. Cánh vỗ: khó nhất, phải sửa nhiều vòng.
Hình: tô phẳng theo luật game nên không có độ bóng bẩy của con gốc. Ước khoảng 80% chất lượng chuyển động.

## 5. Concept (người dùng duyệt 2026-11-11)

- Bản 1 (`L1_concept.png`): vây lam ngọc, tia và sừng cam san hô → người dùng: "phối màu cánh xanh cam nhìn loè loẹt quá, đổi tông màu
  đi, sang màu trầm trầm một chút".
- Bản 2 (`L1_concept_2.png`): vây lam xám trầm `#6A9BA8`, tia và sống cánh chàm sẫm `#242C68`, sừng và mỏ màu cát → người dùng: "mỏ
  và sừng cho sang màu đen".
- Bản 3 (`L1_concept_3.png` = **`L1_duyet.png`**, người dùng: "chốt"): sừng và mỏ đen than `#26252C`. Mỗi bản sau đính bản trước làm
  ảnh mẫu, dặn "giữ nguyên nét vẽ, chỉ đổi ...": dáng và chỗ đặt các phần không đổi giữa ba bản.
- Concept đã duyệt khác bảng con gốc ở hai chỗ: **không có vây tai nhỏ** (`P_yuqi02`) và mỏ trên / mỏ dưới vẽ liền một khối đen.

## 6. Mảnh (2026-11-11): gen từ concept, đúng chỗ, đúng cỡ

Lệnh: `rong_vay.py nhan` → `nhom` → `build_rong_vay.py` → `gen.py luot_2_nhom_<X>.txt` (X = A..G, M) → `rong_vay.py cat` → `ghep`.

- **Bản thử đầu hỏng**: tờ hướng dẫn là hình bóng mảnh lấy từ rig con gốc. GPT vẽ theo tờ đó chứ không theo concept nên mảnh lệch
  concept 20–25 px, đầu mất dáng. Bỏ (`tai_ve/_bo/N_B_cach_cu.png`).
- **Cách đạt**: tách vùng từng mảnh ngay trên concept (`nhan`): ô = cụm liền cùng lớp màu không phải nét mực; mỗi ô bỏ phiếu theo mặt
  nạ rig, chỉ tính mảnh hợp màu ô (chàm → thân / đầu, lam xám → vây / màng cánh, navy → tia / sống cánh, đen → sừng / mỏ); thân chàm
  liền nhiều khúc thì chia theo mặt nạ rig. Soi `mau/nhan.png`. Tờ hướng dẫn mỗi nhóm (`mau/nhom_<X>.png`) = **chính concept đã xoá
  mọi thứ ngoài các mảnh của nhóm**, phần khuất của từng mảnh (mặt nạ rig ∩ hình concept) tô **hồng** để GPT vẽ bù và khép viền.
  Câu lệnh: giữ nguyên mọi vùng đã vẽ, đúng chỗ đúng cỡ; thay vùng hồng bằng phần nối tiếp; mỗi mảnh một hình kín.
- Bẫy khi tách vùng: mảng đen than (sừng, mỏ) trùng độ tối với nét mực → tách mảng đen dày bằng phép mở bán kính 6 px; tia / sống
  cánh navy `(45, 55, 138)` và thân chàm `(58, 74, 178)` phải là hai lớp màu riêng (màu đo trên concept, không lấy mã màu trong prompt);
  lòng vòng cuộn là giấy trắng khép kín, phải tính là nền.
- **Nhóm** (mảnh cùng nhóm cách nhau ≥ 32 px): A `vay_duoi, canh_x_song, vay_11, vay_14, tai_lon, canh_g_mang`; B `than_4, than_2,
  dau`; C `than_5, vay_15, vay_08, vay_07, than_1, sung_t`; D `canh_x_mang, vay_10, than_3, vay_ma`; E `vay_16, vay_09, sung_s,
  canh_g_song`; F `than_6, vay_06`; G `vay_13, vay_12`; M (tờ phóng to 6 lần) `mo_tren, mo_duoi, mat_nham`.
- `cat`: tách nền trắng, gán cụm cho mảnh theo mặt nạ lộ + khuất, lưu **cả khung 1536 × 1024** (`manh/<tên>.png`, khỏi dò chỗ khi rig).
  `khop`: dời cả mảnh cho phần lộ khớp màu concept (GPT xê dịch: `canh_x_mang` +18 px, `vay_11` +30 / −18, `vay_08` +8, `vay_10` −8,
  `canh_x_song` −6; còn lại 0–2 px); ba mảnh khuất hẳn (`vay_16`, `vay_12`, `vay_13`) co 0,66–0,9 lần và đặt vào vùng khuất sao cho
  dáng nghỉ không thò ra ngoài hình. Bản trước khi chỉnh ở `manh/_goc/`.
- Mỏ: GPT không giữ đúng tỉ lệ 6 lần (mỏ trên 1/4,8; mỏ dưới 1/3,6; mí 1/6,3) nên dò tỉ lệ + chỗ theo khối mỏ và con mắt của concept.
  **Mỏ trên lấy thẳng từ concept** (nửa khối mỏ phía trên đường miệng; nó nằm trên cùng nên không có phần khuất, dáng nghỉ y như
  concept); bản GPT có gốc kéo dài để ở `manh/_goc/mo_tren_gpt.png`. Mỏ dưới là mảnh GPT (có phần nấp sau mỏ trên).
- Thứ tự vẽ: theo slot con gốc; `mo_duoi`, `mo_tren` ngay trên `dau`; `mat_nham` ẩn mặc định (đổi hình khi nhắm mắt).
- **Kết quả ghép** (`rig/ghep.png`, `rig/so_concept.png`, `rig/manh_soi.png`): 29 mảnh + mí mắt; IoU hình bóng với concept **0,979**; lỗ
  bên trong hình 143 px ở bốn chỗ sát mép (29–39 px mỗi chỗ), không có khe giữa hai mảnh; thừa ra ngoài concept 4.110 px rải theo mép
  (nhiều nhất `canh_x_mang` ~1.300 px, `vay_10` ~600 px).
- Khác concept còn thấy: đỉnh đầu mất mỏm nhọn nhỏ sau gờ mày (GPT bo tròn); mỏ dưới vân sáp đậm hơn mỏ trên; `than_3` và `than_4` có
  một khấc nhọn ở mép bị cắt (nấp sau vây ở dáng nghỉ).

## 7. Rig và clip bản đầu (2026-11-11, người dùng: "rig xương làm animation giống con gốc đi rồi cho tôi xem")

Lệnh: `py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/rong_vay_rig.py` → `inbox/rong_vay_1/rig/` (`xem.html`,
`khung_<clip>.png`, `rong_vay_1.json/.atlas/.png/.atomik`); `rong_vay_rig.py uon` (uốn thử); `rong_vay_rig.py soi <clip> <giây,...> [tỉ lệ]`
(khung lớn nền xám → `rig/soi_<clip>.png`).

- **Xương** (101): lấy đúng cây xương của con gốc (tên, cha – con, chỗ đặt khớp dáng gốc đổi về toạ độ của mình; đặt đè lên ảnh ghép
  thấy sống lưng, chuỗi vây buồm, ba chuỗi mỗi cánh trùng mảnh của mình). Khác con gốc: nửa thân sau (`H_shenti..8`, con gốc chạy trên
  đường cong) nối thành chuỗi cha – con thường, đuôi `weiba` nối vào khúc cuối; bỏ xương mây, điểm điều khiển đường cong; **đuôi đặt
  khớp riêng** (`RIENG`): `weiba4` khuất sau ngực, `weiba5` là cuống đuôi dựng lên bên phải cổ, hai thuỳ vây đuôi `bone30..32`, `bone33..34`.
- **Lưới**: `luoi_vung` từng mảnh (bước viền 10, trong 14 px rig; mảnh nhỏ 7 / 10): 2.785 đỉnh, 4.047 tam giác. Tỉ lệ rig 0,55 lần concept.
- **Trọng số**: mỗi mảnh bám nhóm xương mà mảnh tương ứng của con gốc bám (đọc từ lưới gốc, ngưỡng 0,12), chia theo khoảng cách từ
  đỉnh tới từng đốt (Gauss, σ = 0,4 × dài đốt trung vị, kẹp 9–34), làm trơn 2 vòng, tối đa 4 xương. Mỏ trên, mỏ dưới, mí mắt bám cứng.
- **Clip tự viết bằng hàm thời gian theo nhịp con gốc, không chép khoá**:
  - `canh(P, t, U)`: hai cánh theo hàm nâng `U(t)` (0 = buông như dáng gốc, 1 = giơ hết: cánh gần quay −72°, cánh xa +96°). **Cả cánh
    quay cứng quanh vai** (gốc hai chuỗi màng dời theo vòng quanh gốc sống cánh); bản đầu để ba chuỗi quay quanh ba gốc riêng thì
    bắt chéo, cánh xa vò nát. **Gập màng giả 3D**: lúc đang giơ lên, gốc hai chuỗi màng kéo về gốc sống cánh và xoay trùng hướng sống
    (tối đa 85%), lúc đập xuống xoè lại; đốt ngoài trễ 0,05 s mỗi đốt và oằn ngược chiều quay.
  - `nen`: thân nhô lên sau cú đập cánh (7 px), cổ uốn trễ pha, đầu bù 75% để giữ hướng nhìn, vòng cuộn và đuôi gợn sóng; 19 chuỗi
    vây, tai, vây má, thuỳ đuôi lắc ±3,2° lệch pha và có lò xo (`LoXo`); sừng cứng.
  - `idle` 2,8 s (hai nhịp vỗ 1,4 s, chớp mắt ở nhịp hai); `attack` 1,3 s (co lùi giơ cánh → lao + đập cánh + há mỏ, `trung` 0,5 s);
    `skill` 2,3 s (vọt lên, hai nhịp vỗ nhanh, há mỏ gầm `gam` 0,7 – `het_gam` 1,5 s, bổ xuống); `hit` 0,55 s (giật lùi, ngửa đầu, nhắm mắt).
- **Số đo**: `.atomik` 294 KB; khung 0 mọi clip lệch 0,1 px; nối clip về idle 0 px; khép vòng idle 4,95 px (bước thường 31,5 px, do mút
  cánh). Runtime Spine thật (`rig/spine_that/idle.jpg`, `attack.jpg`) dựng giống bộ vẽ Python, không rách.
- **Chưa đạt như con gốc**: chưa có dải cạnh cánh mỏng (cánh nghiêng cạnh chỉ còn sống cánh + màng gập); màng cánh xa hơi nhăn lúc gập
  nhanh; `skill` chồm chưa cao bằng `skill_03` của con gốc; mới 4 clip (con gốc 13); chưa có `die`, `appear`, `cast`.

## 8. Góp ý lần 1 về rig và mổ idle con gốc (2026-11-11)

Người dùng xem trang xem rồi báo: (a) trang "not found": trang mẫu luôn `setMix("die", ...)` mà rig chưa có clip `die` → thêm `die`
1,5 s và **tự mở `xem.html` bằng Chrome ngầm trước khi đưa** (dòng trạng thái + đủ nút clip, không lỗi JS); (b) "phần cuối đuôi chưa
connect với khớp gần nhất"; (c) "bỏ outline những khúc nối nhau đi cho liền mạch"; (d) "mổ xẻ kĩ hơn phần animation idle xem họ còn
những mảnh nào thêm nữa thì mình gen tiếp".

- **(b) Vây đuôi**: cuống đuôi + vây đuôi (bên phải cổ) để cuối chuỗi 13 đốt thân sau thì góc cộng dồn làm nó trôi rời khỏi thân. Nay
  `weiba4` (khớp khuất sau ngực) là con của `Q_shenti3` (khớp ngực ngay cạnh); `weiba5` + hai thuỳ theo nó. `than_6` chỉ còn bám
  `weiba..weiba3`.
- **(c) Chỗ nối khúc** (`rong_vay.py noi` → `manh_rig/`, rig đọc ở đây; `manh/` giữ bản GPT): với mỗi cặp khúc kề (`dau–than_1 … than_5–than_6`):
  xoá nét mực ở ĐẦU khúc (nét trong phần khuất của mảnh, lọt sâu ≥ 8 px trong lòng khúc kia, sát mép mảnh; tô bằng màu thịt gần nhất của
  chính mảnh), viền hai sườn giữ; khúc vẽ TRÊN chỉ chờm 18 px đặc rồi mờ tới 30 px, và phần chờm **lấy luôn màu của khúc dưới** (hai mảnh
  GPT vẽ bù mỗi cái một kiểu: để nguyên thì lộ vệt kem nhạt khi cánh nhấc lên). Kèm theo: **hai khúc kề phải bám chung các đốt quanh chỗ
  nối**: nhóm xương mỗi khúc nới thêm một đốt về mỗi phía dọc sống thân, không thì chỗ chồng mép trượt lên nhau và hở vệt trắng.
  Soi cận bằng runtime Spine thật: `rig/spine_that/can_day_vong.jpg`, `can_co_duoi.jpg`.
- **(d) Mổ idle con gốc** (`scan/monster_3458/att_idle_<t>.json` ở t = 0,2 / 0,4 / 0,57 / 0,76 / 0,95 / 1,14; bảng px lộ từng slot
  `idle_lo.json`; tờ `idle_manh_lo.png` tô đỏ mảnh lúc nghỉ khuất mà giờ lộ):
  - idle không bật thêm ảnh nào: vẫn 35 slot của dáng nghỉ (không có timeline đổi hình; mây không hiện).
  - mảnh lúc nghỉ khuất hẳn mà idle lộ ra: **dải cạnh cánh `P_chibangR08_2`** (slot cánh gần lộ tới 3.384 px ở t = 0,95, đúng lúc sống
    cánh `P_chibangR08` co còn 1.011 px; slot cánh xa `P_chibangR08_3` lộ 605 px ở t = 0,57). Ba vây `yuqi12/13/16` cả clip vẫn lộ dưới 10%.
  - mảnh mình thiếu so với idle: dải cạnh cánh (đã gen: `luot_2_nhom_S.txt` → `N_S.png` → `manh/canh_canh.png`, 674 × 64, một ảnh
    cho hai slot `canh_g_canh`, `canh_x_canh` đặt dọc sống cánh ngay dưới sống, ẩn mặc định, đậm dần khi màng gập quá 42%); vây tai nhỏ
    `P_yuqi02` (concept đã duyệt không có); gờ mày `P_erduo` và mắt mở (gộp vào đầu); `P_shenti07` (dùng lại ảnh khúc đuôi, lộ < 850 px).
  - **nhịp cánh đo được** (diện tích lộ của màng `P_chibangR06`: 33.860 → 28.198 → 12.727 → 10.693 → 19.283 → 6.127 → 27.820): cánh
    quay ngang HAI lần mỗi chu kỳ (giữa lúc giơ lên, và lúc lật ở đỉnh ngay trước khi đập xuống); giơ lên chậm (~0,58 chu kỳ), đập
    xuống nhanh (~0,3 chu kỳ cuối). Clip idle của mình viết lại theo nhịp này (`U_nghi`, `G_nghi`), vẫn không chép khoá.
- Sau sửa: 101 xương, 32 slot, 3.031 đỉnh, `.atomik` 311 KB.

## 9. Góp ý lần 2 (2026-11-11): thân cắt từ một ảnh liền, cánh lật hai mặt, nâng độ nét

Người dùng (ảnh cận đáy vòng cuộn): "phần này nối nhau chưa ổn, con gốc của họ làm 1.1mb cơ mà, xem lại phần cánh đi, cánh họ đập lên
xuống tôi thấy cả 2 lớp trên dưới, ngoài ra để các khớp nối match nhau tôi nghĩ bạn note vào skill những khớp nối thì gen cả con ra rồi
cắt chứ không gen riêng không thì sẽ lệch"; và "bạn không đọc ngược được file atlas của họ để xem texture à".

- **Thân cắt từ MỘT ảnh** (đã ghi vào skill `pokiclash-spine-rig` mục 00): `rong_vay.py nhom_than` → `mau/nhom_T.png` (concept chỉ còn
  năm khúc thân, phần bị cánh / vây / đầu che tô hồng) → `luot_2_nhom_T.txt` → `tai_ve/N_T.png` (cả thân một ống liền, vạch bụng chạy
  suốt) → `rong_vay.py cat_than`: đục lòng vòng cuộn (giấy trắng khép kín 31.753 px), gán điểm thân cho khúc có vùng lộ gần nhất, mỗi
  khúc chờm 34 px sang khúc kề, mép cắt mờ 10 px; `than_5` lấy thêm 3.368 px nấp sau ngực từ bản gen riêng cũ (`manh/_rieng/`).
  `noi` chỉ còn cặp `dau – than_1`. Ghép: IoU với concept 0,971. Soi cận runtime thật: `rig/spine_that/can_day_vong.jpg`.
- **Cánh lật hai mặt**: tờ nhuộm màu từng lớp cánh của con gốc theo 14 thời điểm (`scan/monster_3458/idle_canh_tint.png`: màng vàng,
  sống đỏ, dải cạnh xanh lá) cho thấy màng nằm một bên sống cánh lúc nghỉ, ép thành vạch ở ~0,38 chu kỳ, sang hẳn bên kia sống cánh
  suốt lúc giơ cao, ép lần nữa ở ~0,71 rồi trả mặt khi đập xuống; trước khi giơ còn vung nhẹ về trước. Hai cách tôi thử trước đều
  hỏng: kéo gốc hai chuỗi màng về gốc sống cánh (chỉ gập, không lật); lật gốc và góc từng chuỗi quanh sống cánh (phần màng bám sống
  cánh không lật theo, màng vò nát). **Cách đạt**: xương `canh_g` / `canh_x` ở vai, dọc dây cung vai → mút sống, cha của cả ba chuỗi;
  xoay = vỗ (cánh gần −90°, cánh xa +112°), tỉ lệ y = mặt cánh (`F_nghi`: 1 → 0,05 → −0,7 → 0 → 1). Dải cạnh cánh bám cứng xương
  `canh_<k>_c` không bị ép, hiện khi |mặt| < 0,42. Clip khác suy mặt cánh từ độ nâng và chiều chuyển động. Runtime Spine thật và
  `.atomik` đều dựng đúng tỉ lệ âm (lệch giữa clip tối đa 2,2 px).
- **Độ nét**: ảnh atlas 0,8 lần concept (trước 0,55; đơn vị rig giữ 0,55 nên số trong clip không đổi): atlas 1288 × 1368, `.atomik`
  405 KB (trần đặt 1,1 MB như con gốc). 102 xương, 32 slot, 3.046 đỉnh, 11.131 khoá.
- Texture cánh của con gốc (đọc từ atlas theo lưới từng mảnh): màng `P_chibangR06` sáng có vân, **lớp sẫm `P_chibangR08` là một lưỡi
  rộng cỡ 1/4 bề ngang cánh** (không chỉ là thanh sống mảnh như của mình), dải cạnh `P_chibangR08_2`. Sống cánh của mình mảnh hơn; nếu
  người dùng muốn giống hơn thì gen lại sống cánh thành lưỡi rộng.

## 10. Góp ý lần 3–5 (2026-11-11): rig v4 = nguyên bộ xương, lưới, chuyển động của con gốc; mảnh vẽ đúng khung từng part

Người dùng: "làm giống 100% cánh gốc đi", "dịch ngược các part của con gốc được không?", "vậy sao không gen theo đó ghép lại rồi đổi
pose là được", "gen theo y hệt đúng tỉ lệ luôn, đúng hướng"; sau đó: cánh xa gập xuống còn hở, bỏ bớt vây thân, thân còn mất mảnh,
đuôi cuối chưa nối, màng cánh chưa bám sống cánh ở vài clip.

- **Rig v4** (`rong_vay_rig.py`; bản v3 tự dựng xương đã bỏ): dựng lại đúng bộ xương của `monster_3458` (bỏ xương mây `yun*`, điểm
  điều khiển `quxian*`, `shadow`), đơn vị × 0,44. Chuyển động: `mo_xe/chay.py sample` nay xuất thêm trường `l` (toạ độ, góc, tỉ lệ
  cục bộ ĐÃ áp ràng buộc path / transform của từng xương từng khung) → nướng thành khoá cho xương cùng tên. Clip: `idle` ← idle_01,
  `attack` ← skill_01, `cast` ← skill_02, `skill` ← skill_03, `hit` ← hit_01, `die` ← die_01.
- **Mảnh đúng khung part** (`rong_vay.py`): `part_goc` (ảnh từng part cắt theo lưới) → tờ hướng dẫn mỗi part một ô đúng khung ảnh
  vùng × 2 (part nhỏ × 4) → Codex vẽ → `cat_part <tờ>` → `manh/part/<slot>.png` → rig lắp bằng `gan_nguyen` (nguyên đỉnh, tam giác,
  uv, trọng số của part đó). Ba kiểu tờ đã thử:
  - `P1` (5 part mới: sống cánh gần / xa, vây đuôi, khúc đuôi, vây tai nhỏ): hình bóng phẳng tô màu của mình → IoU 0,80–0,96. Đạt.
  - `P2`–`P6` (25 part còn lại): nướng mảnh cũ của mình vào khung part, phần thiếu tô HỒNG cho GPT vẽ bù → GPT bỏ phần hồng, mảnh
    lệch hình bóng (IoU 0,48–0,92, phần lớn dưới 0,8), lắp vào lưới thì thân khuyết, màng cánh rời sống cánh. **Không dùng kiểu này.**
  - `Q2`–`Q6` (thay P2–P6): phần thiếu tô sẵn bằng màu chỗ gần nhất, xoá nét mực cũ sát chỗ thiếu, kẻ viền sẫm đúng mép hình bóng →
    tờ hướng dẫn là HÌNH BÓNG KÍN như P1; sừng, mỏ, mào tô phẳng một màu. `cat_part` ghi IoU từng part vào `manh/part/_iou.json`,
    chỉ ghi đè khi bản mới khít hơn; với tờ Q, chỗ GPT vẽ hụt lấy màu của tờ hướng dẫn cho khỏi khuyết.
- **Vạch mực ở chỗ nối** (`rong_vay.py noi_part`): mảnh có viền kín nên đầu khúc nằm trên in vạch cắt ngang thân. Ở dáng gốc, nét
  mực trên vành mép một khúc mà rơi sâu trong khúc kề (hơn 5 đơn vị) được thay bằng màu tô gần nhất → `manh/part_noi/<slot>.png`
  (rig ưu tiên dùng; `P_shenti07` dùng lại ảnh `P_shenti06` nhưng có bản xoá vạch riêng).
- **Dọn mảnh bằng mã trong `cat_part`** (chỉ dọn, không vẽ): cắt sát hình bóng (nới 3 px); khúc thân bỏ búi nâu xám GPT bịa ở mép
  cổ và mảng trắng giấy; kẻ nét mực dọc phía trong mép lưới của part (lưới ôm sát hình bóng, viền của mình dày hơn nên chỗ lưới xén
  vào thì mất viền: lộ rõ ở vây đuôi); thu nhỏ ở dạng nhân sẵn alpha.
- **Kết quả tờ Q**: IoU 0,90–0,98 cho cả 25 part (tờ P cùng part: 0,48–0,92). Rig: 112 xương, 29 slot, 702 đỉnh, 772 tam giác,
  6 clip, 29.955 khoá, atlas 1176 × 1232, `.atomik` 387 KB. Soi runtime Spine thật: `rig/spine_that/` (tờ tổng từng clip,
  `can_phai/`, `can_trai/`, `can_co/` phóng cận). Còn thấy khi phóng 4 lần: vành bụng hai khúc cổ lệch nhau vài px ở chỗ nối, vân
  chì hai khúc không liền nhau.
- **Bỏ vây thân** (`BO_VAY` trong `rong_vay_rig.py`): `vay_06, 08, 11, 12, 13, 16` (người dùng: "bỏ bớt vây ở thân đi để đỡ bị hiệu
  ứng vây lồng nhau").
- **Cánh**: màng, sống, dải cạnh đều dùng nguyên lưới và xương của họ (màng bám 3 chuỗi + xương gốc cánh; sống bám
  `chibangR08_1..6` có tỉ lệ âm lúc lật; dải cạnh `P_chibangR08_2/_3` là thanh trơn tô màu sống cánh của mình). Cách làm ghi ở skill
  `pokiclash-spine-rig` mục 00.
- **Bản quyền**: xương, lưới, chuyển động (và hình bóng từng part) là của game gốc; hình vẽ là của mình. Dùng nội bộ, không đăng
  công khai, kể cả artifact (như aola).

## 10b. Vá mép lẹm thân dưới (2026-11-12, người dùng: "phần thân ở dưới bị khuyết mất mấy mảnh")

- **Nguyên nhân**: part `P_shenti04` (mép trong vòng cuộn) và `P_shenti05` (mép trên) của con gốc bị KHOÉT chỗ cắm vây; vây
  `vay_11/12/13` từng che chỗ đó, bỏ vây (`BO_VAY`) thì lộ vết lẹm răng cưa. Lưới của họ cũng khoét theo, nên chỉ tô ảnh là bị xén.
- **Ảnh**: `rong_vay_va.py <vào> <ra> <sigma> <hộp...>` làm trơn viền ngoài (Gauss theo chiều dài) chỉ trong hộp chọn, lấp chỗ lõm,
  gọt bướu, tô màu thân (inpaint CHỈ từ thịt thân, điểm trong suốt không làm màu nguồn, không thì loang đen ở mép khung), kẻ lại viền.
  Đã chạy: `P_shenti04` sigma 14 hộp `200,280,332,470`; `P_shenti05` sigma 26 hộp `0,0,520,185` (từ `manh/part_noi`) → `manh/part_va/`.
  Rồi `rong_vay_va_noi.py P_shenti04 P_shenti05 1.5`: xoá nét mực mép của khúc 04 (vẽ trên) nằm trong hình bóng khúc 05 (vạch cắm
  vào thân dưới lỗ vòng cuộn; trước đây vây che).
- **Rig**: slot có ảnh trong `manh/part_va/` đi nhánh `gan_va` (`rong_vay_rig.py`): lưới của mình phủ đủ ảnh, đỉnh đặt vào thế giới
  qua lưới part của họ (toạ độ trọng tâm hệ uv), bám xương bằng `gan_goc`. `.atomik` 413 KB, 1324 đỉnh. Soi đủ 6 clip: hết lẹm.
- Lần 2 (người dùng: "vẫn thấy bị móp mất 1 ít, có vết mờ mờ ghép lỗi"): đầu khúc 04 cắt thẳng theo khung part chờm lên 05 → đường
  chéo đứt vân và nêm sáng ở vành bụng. `rong_vay_va_noi.py` thêm bước mờ alpha từ mép cắt nằm trong khúc dưới vào 26 px (`MO`).
- **Sừng cứng** (người dùng: "phần sừng không rig xương, để cứng"): `CUNG = {"sung_s": "tou", "sung_t": "tou"}` trong
  `rong_vay_rig.py`: mọi đỉnh sừng bám 100% xương đầu (chuỗi bone36–41 của con gốc là chùm lông mềm).
- Lần 3 (người dùng: "cạnh trên bị móp vào 1 chút"): đáy lỗ vòng cuộn gãy khúc (mép 04 dốc xuống gặp bậc vai của 05; lúc chuyển
  động hai khúc lệch nhau mở khe chữ V). `rong_vay_va_goc.py`: đặt hình bóng 04 vào hệ ảnh 05, `TRON` làm trơn viền HỢP hai khúc
  trong hộp (thêm/gọt vào 05), `LOT` lót thân + viền của 05 ngay dưới mép 04 quanh chỗ nối (lúc lệch thì lộ thân liền thay vì khe).
  Mép mềm cũ lọt vào trong thân thành vạch xám: vùng sửa phải đặc hẳn.
- Lần 4 (người dùng: "phần dưới bị mất outline 1 đoạn ngắn"): viền dưới vành bụng ở chỗ 04 chồng 05. Bước 3 đã xoá cả viền ngoài
  của 05 (nằm dưới 04) → giới hạn `VUNG`; viền 04 ở đó vốn bị `noi_part` cũ xoá dở (sọc) và một dải 04 thò ra ngoài 05 vài px mang
  riềm sáng → `PHU` (04 trong suốt hẳn ở chỗ chồng sát mép ngoài, nhường viền cho 05), `CAT` (gọt dải thò ra, CHỈ sát mép ngoài hình
  ghép, không thì nứt ngang vành bụng khi chuyển động), `SANG` (riềm sáng ngoài viền 05 thành mực); điểm trắng giấy tự tô lại.
- **Thứ tự chạy lại cả chuỗi** (từ `manh/part_noi`, SXS như trên; M = `ArtGen/Spine/inbox/rong_vay_1/manh`):
  1. `rong_vay_va.py M/part_noi/P_shenti05.png M/part_va/P_shenti05.png 26 0,0,520,185`
  2. `rong_vay_va.py M/part_noi/P_shenti04.png M/part_va/P_shenti04.png 24 200,280,332,520`
  3. `MO=0 VUNG="0,0,260,200" SANG="0,170,170,360" rong_vay_va_noi.py P_shenti05 P_shenti04 1.0`
  4. `TRON="34,100,60,430,200" rong_vay_va_goc.py P_shenti05 P_shenti04 41`
  5. `PHU=4 CAT="150,470,332,610,4" rong_vay_va_noi.py P_shenti04 P_shenti05 0.5` (xoá mực + mờ mép chờm của 04)
  6. `LOT="70,60,175,175" rong_vay_va_goc.py P_shenti05 P_shenti04 41` (lót SAU CÙNG, kẻo bước 3/5 xoá mất viền lót)
  rồi `rong_vay_rig.py` (xuất) và đăng lại trang xem.
- Còn thấy: vệt rất nhỏ ở chỗ nối khi phóng to; ở skill lúc cuộn chặt (lỗ khép thành khe) cuối nét mực chỗ nối còn một mẩu lởm
  chởm nhỏ (bản chưa vá có sẵn và nặng hơn: khấc + vạch nối ngang vành bụng).
- Trang xem riêng tư (dùng nội bộ, không Share): https://claude.ai/artifact/N245AYhu5GhJrvBZ7Fi1zX (đăng lại sau mỗi lần sửa).
- Máy D (nhà): không có `D:\Ripper`; dữ liệu quét sinh lại vào `D:\RefAnimation\SwordxStaff\scan\monster_3458` (info, att_goc,
  sample_clips 6 clip), chạy với `SXS=D:/RefAnimation/SwordxStaff`.

## 10c. Clip riêng theo ý người dùng (2026-11-12): dựng ở tầng điều khiển của rig gốc

Người dùng: "appear tướng uốn lượn bay vào rồi gầm; tấn công thường quật đuôi mạnh; chiêu mana hơi ngả người lại lấy đà cánh rồi
quạt 1 phát mạnh tạo 1 lốc xoáy nước (fx làm riêng); chiêu cuối tôi chưa nghĩ ra có thể biến tấu từ chiêu cuối hiện tại".

- **13 clip của họ là gì** (tờ khung `scan/monster_3458/khung/`): `run_01` bay tới (vòng 0,8 s); `skill_01` giơ cánh chém;
  `skill_02` thu người, đuôi vung LÊN (0,37 s) rồi BỔ XUỐNG (0,57 s), cánh giơ rồi đập (0,56 → 0,76 s), há mỏ; `skill_03` dựng thẳng
  người xoè cánh giữ 1 s (mỏ ngậm); `skill_04_1/2/3` bay vọt lên, lộn, bổ nhào (ngang / dọc / chéo); `stun`, `block`, `hit_02`.
- **Cách điều khiển của họ**: thân sau = 8 đốt `H_shenti*` chạy trên một đường cong (path constraint) có 5 điểm điều khiển
  `quxian*` (dời + xoay) và khoá vị trí dọc đường cong; đuôi = chuỗi FK `weiba..weiba5` (+ tia vây `bone30–34`), gốc đuôi bám đốt
  cuối bằng transform constraint; thân trước FK `Q_shenti..5 → tou`; mỏ `bone10` (trên), `bone11` (dưới, há tới −36°).
- **Công cụ** (`mo_xe/mo_xe.html`): `sample` xuất thêm `u` (biến đổi riêng CHƯA áp ràng buộc = giá trị điều khiển) và `p` (vị trí
  trên đường cong); `extra` nhận thêm `paths: {tên: {position: [[t, v]]}}`; chế độ `sheet` cũng nạp `extra`. Mẫu điều khiển của
  cả 13 clip: `scan/monster_3458/sample_dk.json`; bản chép rig gốc để chạy clip tự viết: `scan/monster_3458/lam_clip/`.
- **`rong_vay_clip.py`**: ghép ở tầng điều khiển (lấy dáng `dk(clip, giây)`, co giãn thời gian `cong`, pha `tron` có mặt nạ nhóm
  xương CANH / DUOI / MO, cộng góc `xoay`, dời `doi`) → `lam_clip/rv_extra.json` → runtime Spine thật áp ràng buộc → lấy mẫu
  `scan/monster_3458/sample_moi.json` → `rong_vay_rig.py` dùng như clip của họ. Lệnh: `dung`, `xem [clip] [n]` (tờ khung trên rig
  gốc), `mau` (lấy mẫu). Chạy qua `quai/khoa.py chrome`.
  - `appear` 2,45 s: dáng bay `run_01`, cả con dời từ sau – trên (−900, +300 đơn vị gốc ≈ 0,83 chiều cao) vào chỗ theo đường lượn
    sóng 1,25 Hz, thân nghiêng theo dốc, hiện dần 0,2 s đầu; 1,05 s thu về dáng nghỉ; gầm 1,38 → 1,92 s: thân vươn theo dáng 0,40 s
    của `skill_01` (78%), cánh lấy trọn dáng xoè 0,42 s của `skill_03`, há mỏ, đầu rung 12 Hz.
  - `attack` 1,05 s (quật đuôi): thân + đuôi của `skill_02` co giãn lại (lấy đà 0 → 0,32, quật 0,32 → 0,44, `trung` 0,44), cánh
    chỉ 30%, thân chúi tới lúc quật, ngọn đuôi vút thêm trễ pha và vươn dài 10–24% ở khung quật.
  - `cast` 1,60 s (quạt cánh), bản 2: dựng trên `skill_01` ("giơ cánh chém"): nhún nhẹ, ngả lưng +8° và cánh GIƠ CAO XOÈ HẲN MẶT
    (0,14 → 0,46, giữ tới 0,62), quạt xuống – ra trước 0,62 → 0,76 đúng tốc độ clip nguồn (`phun` 0,72, `het_phun` 1,24), chúi −7°,
    há mỏ lúc quạt, đuôi 60%, cánh êm về (bỏ nhịp thu cánh lật mỏng của clip nguồn). Lốc xoáy nước là VFX làm riêng, chưa làm.
    Bản 1 dựng trên `skill_02` bị trả ("chiêu bắn chưa thấy quạt cánh"): ở đó cánh "giơ" là LẬT NGHIÊNG mỏng như vạch rồi đập về
    gần dáng nghỉ, mắt không thấy cung quạt. **Muốn thấy cú quạt thì dáng lấy đà phải là dáng cánh xoè lộ mặt màng, giữ ≥ 0,15 s.**
  - `skill` 2,33 s: `skill_03` + há mỏ gầm và rung đầu suốt lúc giữ + cánh vỗ hai nhịp (0,74 → 1,12 → 1,50, pha 55% nhịp đập
    của `skill_02`). Sự kiện `gam` 0,70, `het_gam` 1,50 như cũ. Người dùng chưa chốt ý chiêu cuối.
- **Bài học**: pha cánh NỬA CHỪNG giữa hai mặt (mức 0,6–0,8) thì màng bị ép mỏng thành vạch; pha cả con 62% sang dáng cuộn đuôi
  thì đuôi tự đè lộ vệt trắng. Cánh phải lấy trọn một dáng sạch của họ; thân mới pha một phần.
- Rig: 7 clip, 39.870 khoá, `.atomik` 467 KB. Đã chép `rong_vay_1.atomik` + chân dung vào `han_ngac_1`, `han_ngac_2` (chép tay hai
  suất này; KHÔNG chạy `vao_game.py` trên máy ổ C vì thư mục `rig/` của các tướng khác không có ở đây hoặc đã cũ).

## 10d. Vào game bản clip mới, bắt đầu dạng 1 (2026-11-12, người dùng: "ok cho vào game và làm dạng 1 đi")

- **Vào game**: `rig/rong_vay_1.atomik` (7 clip, có `appear`) + chân dung đã chép vào `han_ngac_1`, `han_ngac_2`; Unity nhập lại 4
  file không lỗi (xem `Editor.log`). Cầu nối MCP của Unity (cổng 8090) không mở trên máy ổ C nên CHƯA chạy menu chụp thử và chưa
  vào trận kiểm; `<dạng>.asset` trỏ thẳng file `.atomik` nên không phải dựng lại.
- **Hình đang có là DẠNG 2** (rồng trưởng thành, bám con gốc, như cá voi). **Dạng 1 = rồng non** (mã làm việc `rong_vay_non`) trên
  CÙNG rig, cùng lưới, cùng clip: `rong_vay_rig.py` nhận `RV_DANG=non` → bảng `TI_LE` đổi tỉ lệ dáng gốc ở gốc từng chuỗi xương
  (`tou` 1,26; ba chuỗi màng + gốc sống của mỗi cánh 0,60): đầu to, cánh co về thân mà gốc cánh vẫn dính. Đã soi idle và cast:
  clip chạy đúng. Lỗi đã gặp: dải cạnh cánh gắn bằng dáng gốc của `sk` (đã đổi tỉ lệ) nên không co theo → gắn bằng ma trận `Wc`.
- **Concept dạng 1** (đề xuất của Claude, CHỜ DUYỆT): `inbox/rong_vay_non/tai_ve/L1_concept.png`: thân lam nhạt `#6C86DC`, bụng
  kem, đầu tròn mắt to hổ phách, hai nụ sừng đen, cánh và vây lam ngọc nhạt, lưng trơn không vỏ sò. Ảnh mẫu 2 là hình bố cục do rig
  dựng (`rong_vay_rig.py bo_cuc`, `inbox/rong_vay_non/mau/bo_cuc.png`). Gói: `build_rong_vay_non.py` → `gui_gpt/rong_vay_non/`.
- Người dùng xem bản nháp: "mặt nhìn non hơn rồi nhưng thân bạn cũng phải làm ngắn hơn". **Thân ngắn làm ngay trên rig** (`K_THAN`
  = 0,72, `rong_vay_rig.py`): co thân DỌC CHIỀU DÀI, giữ bề dày, không đổi tỉ lệ xương: (1) toạ độ x riêng của mọi xương con của
  xương thân (`Q_shenti*`, `H_shenti*`, `weiba*`) × K; (2) vị trí các đốt thân sau và gốc đuôi co về đốt `H_shenti` × K (vòng cuộn
  nhỏ lại); (3) x của điểm gắn lưới trong hệ xương thân × K; áp cho dáng gốc và khoá dời của mọi clip. Soi idle, skill: thân liền,
  cuộn chặt hơn, không rách. Concept lượt 2 trên bố cục thân ngắn, giữ thiết kế đầu của bản nháp (ảnh mẫu 3):
  `inbox/rong_vay_non/tai_ve/L1_concept_2.png`, CHỜ DUYỆT. (Một lượt Codex hết 420 s không trả ảnh; chạy lại thì 85 s.)
- Sau `L1_concept_2`: "làm vây của nó ngắn hơn chút nữa" → `TI_LE` thêm tỉ lệ ở xương GỐC từng vây (vây lưng `bone71, 73, 75, 76, 78,
  79, 80, 83, 86, 89, 91, 92` 0,74; vây tai và vây má `bone42, 44, 12, 15` 0,80; hai thuỳ vây đuôi `bone30, 33` 0,82), bố cục dựng
  lại, concept lượt 3: `inbox/rong_vay_non/tai_ve/L1_concept_3.png`, CHỜ DUYỆT. Cánh vẫn 0,60 (người dùng nói "vây", chưa nói cánh).
- Sau `L1_concept_3`: "tôi thấy phần đuôi vẫn dài, thu ngắn các part thân/đuôi lại chút" → hệ số co tách ba đoạn: thân trước
  `K_THAN` 0,70, thân sau (vòng cuộn) `K_SAU` 0,62, đuôi `K_DUOI` 0,54 (biến môi trường `RV_K_*` để thử số khác). Soi skill (cuộn
  chặt nhất), attack: thân liền. Concept lượt 4: `inbox/rong_vay_non/tai_ve/L1_concept_4.png`, CHỜ DUYỆT.
- **Concept dạng 1 chốt** ("ổn rồi"): `inbox/rong_vay_non/tai_ve/L1_duyet.png` (= `L1_concept_4.png`).
- **Da dạng 1 = chuyển da từ dạng 2** (`rong_vay_non.py`): tờ hướng dẫn G1–G6 = ảnh part ĐÃ XONG của dạng 2 (bản vá > bản xoá vạch
  nối > bản cắt) xếp đúng ô cũ; Codex vẽ lại với màu rồng non, giữ hình bóng (21 part; sừng, mỏ chép nguyên; 6 vây đã bỏ không
  vẽ). `cat`: lấy lại ĐỘ ĐẬM và CHỖ KHÔNG CÓ MỰC của ảnh dạng 2 (mọi bước dọn chỗ nối, vá mép được thừa hưởng), kéo trung vị từng
  lớp màu về màu chuẩn (GPT tô mỗi tờ một sắc → lộ mảng khi ghép). Phủ 95–100% hình của dạng 2 (khúc lưng 95%: phần vỏ sò bỏ).
- **Rig dạng 1** (`RV_DANG=non`, ra `inbox/rong_vay_non/rig/`): tỉ lệ đã duyệt + sừng co về gốc còn 0,42 (nụ sừng nhọn nhỏ, concept
  vẽ nụ tròn) + `noi_lai` (xoá vạch nối theo dáng thân ngắn, làm cứng mép mờ của bản vá) + mí mắt nhắm dựng từ ảnh đầu, bám lưới
  của `P_tou` (mảnh mí của dạng 2 chỉ che một phần mắt mới). 7 clip như dạng 2, `.atomik` 464 KB. Soi runtime thật: idle, attack,
  cast, skill, appear; soi hit (mắt nhắm).
- **Sửa khớp nối dạng 1** (người dùng gửi 3 ảnh: "các khớp này nối không match, chỗ bị hở, chỗ mất nét": đáy vòng cuộn, cổ, đỉnh
  vòng cuộn): lỗi ở cách co da theo từng xương (lệch ~ (1 − K) × nửa bề dày × góc gập ở chỗ thân uốn). Thay bằng `co_da`: dời
  mỗi điểm da theo điểm gần nhất trên trục thân rồi tính lại điểm gắn theo dáng gắn mới. `noi_lai` thêm: tô lại 2 px mép của khúc
  nằm trên ở chỗ chồng (hết vạch sáng mảnh). Soi cận runtime thật (`rig/spine_that/can_day`, `can_co`, `can_tren`): hết hở, vành
  bụng và nét viền liền; còn đường tóc rất mảnh ở chỗ hai ảnh giáp nhau khi phóng ~3 lần.
- **Sửa khớp nối lần 2** (người dùng: "vẫn lỗi các chỗ đấy, xem kĩ lại"; tôi đã báo "khớp" khi ảnh cận của chính mình còn lỗi):
  ba nguyên nhân còn lại, đều sửa trong `rong_vay_rig.py` cho dạng non:
  1. Da dạng non thừa hưởng "chỗ không có mực" của dạng 2, nhưng thân ngắn chồng khác đi nên đoạn đã xoá nay nằm trên mép ngoài
     (viền cổ đứt). `noi_lai` nay KẺ LẠI mực kín dọc mép mọi khúc rồi mới xoá phần rơi sâu trong khúc kề theo dáng này.
  2. Vạch sáng mảnh ở chỗ hai ảnh giáp nhau: mép của khúc nằm trên, ở chỗ nằm sâu trong khúc kề, cho mờ dần 6 px.
  3. Lỗ vòng cuộn bị bóp thành khe lởm chởm (trông như hở): thân sau thon lại (`DAY_SAU` 0,86; đốt đầu 0,95, 0,90) trong `co_da`
     → lỗ mở thành lỗ nhỏ viền kín như concept.
  Soi cận lại 3 chỗ × 4 khung idle + tờ tổng skill, attack: vành bụng liền, viền liền, lỗ gọn. Còn: vệt xám rất nhỏ ở mép phải
  chỗ nối cổ, mẩu kem nhỏ ở đầu vành bụng trên vòng cuộn.
- **Sửa khớp nối lần 3** (người dùng: "vẫn lỗi nhẹ, xem kĩ lại nữa đi"): phóng cận gấp đôi (≈ 5,8 px / đơn vị rig, `spine_that/sat_a,
  sat_b, sat_c`) mới thấy: `noi_lai` xoá cả vành 10 px nên các nét chạy NGANG qua mép (ranh vành bụng, vạch vảy bụng) bị cụt ~10 px
  và nhoè ở chỗ nối. Nay chỉ xoá nét viền ĐẦU KHÚC: nét ngang (điểm mực có mực "bên trong" nằm gần thẳng phía trong nó, cách ≤
  vành − độ sâu + 1) giữ tới cách mép 3 px và không bị mờ; điểm xám khử răng cưa quanh nét vừa xoá tô lại. Còn thấy ở mức phóng
  đó: đường viền rất nhạt của vạt khúc cổ trên nền kem (hai mảng kem khác vân).
- **Sửa khớp nối lần 4** (người dùng gửi ảnh cổ: "phần gần đầu vẫn bị mất 1 ít nét"): vạt kem của khúc cổ (nằm trên) chờm sâu xuống
  khúc ngực, che mất nửa phải một vạch vảy bụng của khúc dưới. Thử 1: cắt ngắn vạt chờm (9 px) → nét hiện đủ nhưng lộ bậc lệch của
  ranh vành bụng ở cổ và mẩu kem thò ở đỉnh vòng cuộn (vạt chờm chính là thứ che bậc đó): BỎ. Thử 2: in lại mọi nét của khúc dưới
  lên vạt → sinh nét thừa (nét khúc trên cố ý che). Chốt: `noi_lai` chỉ in tiếp nét của khúc dưới đang HIỆN DỞ DANG (lần theo nét
  từ phần còn lộ vào dưới vạt ≤ 40 px), trên nền kem, cách mực của khúc trên > 8 px, và mẩu in phải nối tới gần mực sẵn có của
  khúc trên; chỉ bật cho cặp cổ – ngực (`IN_LAI`). Soi cận idle và cast: vạch vảy liền tới viền phải, đỉnh vòng cuộn không có nét
  thừa. Đoạn in lại hơi răng cưa khi phóng ~6 lần.
- **Vào game**: `da_nhan.json` trỏ `han_ngac_1` → `rong_vay_non`, `han_ngac_2` → `rong_vay_1` (xuất lại với dạng 2/2); chép tay 4
  file, Unity nhập lại không lỗi. CHƯA có clip `evolve`; chưa kiểm trong trận (MCP Unity không mở).

## 10e. Làm nốt (2026-11-12, người dùng: "tạm ổn, cho vào game đi", "làm nốt những cái bạn chưa làm đi")

- **Lốc xoáy nước của chiêu mana** (`n_loc`): `HatNuoc.NVoi` thêm tham số `tu` (chỗ phễu dựng lên): phễu vòi rồng dựng ở trước mặt
  tướng (cách chân 0,85 chiều cao về phía địch) đúng khung quạt cánh, lướt tới chân địch trong 0,5 s (`T_DI`), quay tới khi sụp;
  `PlayNuoc` thêm `case "n_loc"`, `HoldNuoc` 0,3 s; `StageView.WaterFx["han_ngac"]` mana đổi `n_tia` → `n_loc` (chiêu cuối giữ
  `n_song` / `n_mua`, chưa chốt). Unity biên dịch lại không lỗi (Editor.log). CHƯA xem trong trận.
- **Clip `evolve` của dạng 1** (`rong_vay_rig.py`, `tien_hoa`): một lần chạy dựng cả hai dạng (`cau_hinh(dang, res)` đổi cấu hình giữa
  chừng); dạng 2 gộp vào bản nhẹ (ảnh 0,44) bằng `quai/tienhoa.py`. Dạng non ngửa người gồng, rung, há mỏ; đổi dạng ~1,2 s; dạng 2
  vươn người há mỏ gầm rồi hoà về khung 0 idle của nó. File dạng 1: 226 xương, 58 slot, 8 clip, 609 KB. Soi tờ khung runtime thật.
- Đã chép vào `han_ngac_1`. Còn: tên tướng / dạng / thẻ (chờ người dùng chọn: đổi tên kéo theo Nhập dữ liệu và tính lại golden trong
  Unity, máy này không mở được MCP); sừng nụ tròn và mỏ ngắn của dạng 1 (đang là sừng, mỏ dạng 2 thu nhỏ / giữ nguyên).

## 10f. Vệt sáng ở khớp nối trong game: lỗi shader chung (2026-11-12)

Người dùng gửi ảnh trong game (dạng 2, đáy vòng cuộn có vệt sáng cong và nêm sáng ở vành bụng): "shader làm chỗ này bị lộ lỗi, các khớp
nối đều bị", "các con khác có nhiều con cũng bị vậy, tìm giải pháp chung". Nguyên nhân: `PokiClash/PetPart` trộn kênh alpha như màu khi
vẽ tướng ra RenderTexture → alpha RT tụt ở chỗ mép mờ của mảnh trên đè mảnh dưới → `StickerOutline` lót giấy trắng vào. Sửa:
`PetPart.shader` trộn alpha riêng (One, OneMinusSrcAlpha), `AolaActor.Mat` đặt `_SrcBlendA/_DstBlendA` (mảnh cộng giữ cách cũ). Unity
nhập shader và biên dịch không lỗi. CHƯA nhìn lại trong game (MCP không mở): chờ người dùng xác nhận. Áp cho mọi tướng (aola và .atomik).

## 11. Còn lại

- Lòng miệng (khi mỏ há) chưa có: con gốc cũng không có mảnh này; quyết khi làm clip há mỏ.
- Chỉnh clip theo góp ý người dùng; thêm `die`, `appear`, `cast`; vào game: chưa làm.
- Tên, số dạng tiến hóa, chiêu: chờ người dùng.
