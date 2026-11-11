# Dòng rắn nước có sừng (mã làm việc `ran_sung`): tướng thứ 5 đảo Thủy (2026-11-11)

Người dùng lên ý tưởng và duyệt concept (chưa đặt tên; mã `ran_sung` chỉ để đặt thư mục); mảnh, rig Claude tự làm.
Gói prompt: `ArtGen/Spine/build_ran_sung.py` → `gui_gpt/ran_sung_<k>/`, ảnh về `inbox/ran_sung_<k>/tai_ve/`.

## 1. Ý người dùng (nguyên văn tóm lại)

- Dựa trên con gốc `monster_3247` (game tham khảo). Concept: **rắn nước có sừng**: hai chùm lông trắng trên đầu con gốc đổi thành
  **hai sừng đen**; **chót đuôi cũng là sừng đen, nhọn kiểu kunai** (sừng nên **cứng**, không mềm mại như chùm đuôi con gốc).
- `idle`: có thể làm giống con gốc, sửa nhẹ đi chút.
- Đòn thường: rắn **lao đến cắn** đối thủ, **nhanh**.
- Chiêu mana: **há nhẹ mồm bắn nước** (tia nước là VFX, rig không vẽ).
- Chiêu cuối: **dùng đuôi quật chém liên tiếp nhiều phát** vào người đối thủ (nhiều phát và nhanh).
- Cái khó: **pose ở idle** và làm **đủ mềm mại, uyển chuyển giống rắn**.
- Dạng 2: dài hơn, to hơn, chiêu mạnh hơn. Mỗi dạng vẫn giới hạn **0,5 MB**.

Người dùng không dặn màu thân (chỉ dặn sừng đen). Màu trong concept là **đề xuất của Claude**, chờ duyệt: lưng lam cô-ban
`#2E6FD8` đốm bong bóng lam nhạt `#86D6F0`, bụng lam băng `#DDF0F7`, sừng và lưỡi kunai đen than `#26252C`, mắt hổ phách `#FFA92E`
con ngươi dọc. Tránh bảng màu con gốc (lục lam + kem + mắt hồng) và hoa văn chữ triện của nó.

### Góp ý của người dùng về concept (2026-11-11)

Bản 1 (`L1_concept.png`: rắn nhìn nghiêng sang phải, miệng cười dài, chót đuôi là con dao kunai có vòng cổ) bị chê:
- "phần đuôi thô quá, **chỉ hơi hướng giống kunai thôi**": không vẽ con dao gắn vào đuôi. Chót đuôi tự hoá sừng, mọc liền từ
  đuôi, dáng lá thon cong, chóp nhọn.
- "phần đầu, miệng **phải giống rắn**, nhìn kĩ con gốc đi"; "**hướng nhìn** cũng không giống với con gốc".

Cách dựng hình của con gốc phải giữ (đọc trên ảnh cận `scan/monster_3247/can/idle_t0_x2.png`):
- **Nhìn gần chính diện, hơi từ trên xuống**; đầu cúi, cằm thu, mắt nhìn ra người xem. Không phải nhìn nghiêng.
- **Đầu hình trứng**, rộng nhất ở ngang mắt, thon xuống mõm tù ở đáy đầu (hơi lệch phải). Màu lưng phủ đỉnh đầu rồi chạy xuống
  giữa hai mắt thành mảng lưỡi tròn, dừng ngay trên miệng; má, môi, cằm màu bụng.
- **Hai mắt rất to ở hai bên đầu**, mép ngoài nằm trên viền đầu; mí trên dày, xếch vào giữa.
- **Miệng nhỏ, thấp, ngay mõm**: môi trên có mỏm nhọn ở giữa (chữ V ngược), hai nét ngắn cong ra hai bên; cằm tròn nhỏ ở dưới.
- **Thân mập** (cổ rộng hơn nửa đầu), **bụng nhạt quay ra trước** chiếm gần hết bề ngang cổ, lưng chỉ là dải bên trái; vòng cuộn
  ở dưới trái lộ lưng, vòng ra sau gốc cổ; đuôi chạy sang phải sát đất rồi chùm đuôi dựng lên, cao gần bằng đầu.
- Hai chùm lông ở hai góc trên đỉnh đầu (như tai mèo nhìn từ trước) → của mình là hai sừng đen ở đúng chỗ đó.

## 2. Mổ xẻ con gốc `monster_3247` (chỉ học cấu trúc và nhịp, không lấy hình)

Nguồn: `D:\Ripper\SwordxStaff\web\assets\Monster\monster_3247\` (Spine 4.2.28, skel 48 KB + ảnh 77 KB, atlas 104 × 1172, tỉ lệ
0,75). Kết quả quét: `D:\Ripper\SwordxStaff\scan\monster_3247\` (`info.json`, `keys.json`, `keys.txt` = khoá 6 clip dạng đọc được,
`mesh.json`, tờ khung `khung/<clip>.jpg`). Quét lại:
`py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/mo_xe/chay.py info|keys|mesh|sheet ...`.

### Ảnh (18 vùng)

| Vùng | Cỡ | Là gì |
|---|---|---|
| `P_shenti01` | 97 × 134 | khúc cổ trên (dưới đầu) |
| `P_shenti02` | 87 × 121 | khúc cổ dưới / ngực |
| `P_shenti03` | 114 × 86 | vòng cuộn trên đất |
| `P_bozi` | 107 × 91 | gáy, nối cổ với đầu |
| `P_weiba01` | 96 × 72 | khúc đuôi nằm trên đất |
| `P_weiba02` | 158 × 91 | khúc thân sau (từ vòng cuộn ra đuôi) |
| `P_huoyan` | 90 × 128 | chùm đuôi (mềm, 4 đốt) |
| `P_face`, `P_yanpi`, `P_mouth` | ≤ 103 × 86 | mặt, mí, miệng (ảnh chữ nhật cứng theo xương đầu; miệng xương riêng) |
| `P_yanjing01..04`, `P_shouji01, 02` | ≤ 44 × 44 | tròng, con ngươi; mắt lúc trúng đòn (chữ V) đổi ảnh |
| `P_ear01, 02` | 50 × 74, 40 × 60 | hai chùm lông trên đầu, mỗi chùm 3 đốt |

**Thân chia 6 khúc ảnh chồng mép nhau**, mỗi khúc một lưới thưa 22–40 đỉnh, bám 3–6 xương. Không có ảnh riêng cho dáng duỗi:
dáng lao tới **uốn lại chính các ảnh đó** (cùng ảnh gắn vào slot thứ hai `P_weiba03/04`, `P_shenti04`, `P_huoyan2` với bộ xương
thẳng `bone38 → bone32..36`, đổi slot trong 1 khung ở `run_01`).

### Xương (41), ràng buộc

```
root → bone (y −25) → bone30
  ├─ A1 (đích IK của vòng cuộn; dời x +45 khi lao)
  │   └─ bone2 (GỐC CỔ ở sát đất: dời cả phần dựng)
  │       └─ bone3 (77) → bone4 (80) → bone5 (80) → bone6 (26, gáy) → bone16 (ĐẦU)
  │                                                    ├─ bone17/19, bone18 (con ngươi), bone20 (miệng)
  │                                                    └─ bone21→22→23, bone24→25→26 (hai chùm lông, 3 đốt)
  │           bone7, bone8, bone9, bone10, bone27 → bone28 (vòng cuộn: con của bone3, đi theo path B1)
  ├─ A2 (đích IK gốc đuôi) → bone11 → 12 → 13 → 14 → 15 (đuôi 5 đốt: 67, 51, 40, 41 px)
  ├─ bone38 → bone32 → 33 → 34 → 35 → 36 (bộ xương thẳng cho dáng bò / duỗi)
  └─ shadow
```
IK `A1` (1 xương, co giãn), `A2` (2 xương); path `B1` rải 4 xương vòng cuộn theo đường cong 9 điểm. Không physics, không sự kiện.

### Mẹo diễn chính

1. **Phần dựng (cổ) là chuỗi 4 đốt từ đất lên đầu; vòng cuộn và đuôi là hai nhánh riêng** gắn vào gốc: cổ ngả, vòng cuộn gần
   như nằm yên, đuôi tự vẫy. Ba khối lệch pha nhau nên con rắn không lắc như que.
2. **Hai đốt kề xoay ngược dấu, đầu bù góc**: idle `bone4` +3 → −2,5, `bone5` +2 → −2,8, đầu `bone16` −1,4 → +4,3.
3. **Đuôi mềm lan sóng**: 5 đốt, đốt gốc ±6°, đốt ngọn ±30°, cực trị trễ 4 khung mỗi đốt (khung 4, 8, 19, 24, 31).

### Clip (9)

| Clip | Dài | Ghi chú |
|---|---|---|
| `idle_01` | 4,00 s | 3 vòng 1,33 s (40 khung); vòng giữa có **điểm phá nhịp** khung 55–70 |
| `skill_01` | 0,93 s | lao cắn, trúng ở khung 15 (0,5 s) |
| `hit_01` | 0,50 s | đổi mắt chữ V; đầu giật, sóng chạy xuống |
| `hit_02` | 0,67 s | |
| `die_01` | 1,00 s | ngửa ra, đuôi dựng, đổ gập xuống đất ở khung 13–20 |
| `run_01` | 0,53 s | đổi sang bộ slot duỗi, bò |
| `stun_01` | 1,33 s | gục, lắc lư |
| `floating_01`, `block_01` | 1,50 s, 0,50 s | |

## 3. Khoá gốc sẽ học (khung 30 fps; góc là lệch so với dáng gốc; `x/y` dời). Đủ ở `scan/monster_3247/keys.txt`

```
== idle_01  4.00 s = 120 khung        (cổ bone3..5, đầu bone16, gốc bone2, đuôi bone11..15, chùm lông bone21..26, miệng bone20)
  Translate bone2   0:0/0  20:-10.1/-4.8  40:0/0  55:-10.1/-4.8  60:-11/-6.01  70:-17.4/-7.01  80:0/0  100:-10.1/-4.8  120:0/0
  Rotate    bone3   0:0.413  11:-0.423  30:1.14  40:0.413  51:-0.423  55:3.09  60:-2.49  70:-6.76  80:0.413  91:-0.423  110:1.14  120:0.413
  Rotate    bone4   0:3.01  19:-2.54  40:3.01  55:9.61  60:10.8  70:8.74  80:3.01  99:-2.54  120:3.01
  Rotate    bone5   0:0.376  8:2.1  28:-2.81  40:0.376  48:2.1  55:-13.3  60:-10.9  70:-16.5  80:0.376  88:2.1  108:-2.81  120:0.376
  Rotate    bone16  0:-1.42  20:4.28  40:-1.42  55:-8.73  60:4.73  70:23.8  80:-1.42  100:4.28  120:-1.42
  Rotate    bone20  40:0  60:-0.696  72:-8.2  80:0                                   (miệng hé ở điểm phá nhịp)
  Rotate    bone11  0:-4.33  4:-5.72  24:7.71  40:-4.33  ...                         (đuôi gốc)
  Rotate    bone12  0:0.754  11:-13.4  31:11.3  40:0.754  51:-13.4  55:-9.88  71:19.5  80:0.754 ...
  Rotate    bone13  0:13  19:-12.5  40:13  58:-28.1  74:19.8  80:13  99:-12.5  120:13
  Rotate    bone14  0:8.43  4:12.4  24:-26  40:8.43  44:12.4  64:-55.3  80:8.43 ...
  Rotate    bone15  0:-0.151  8:28  31:-33.7  40:-0.151  48:34  71:-68.4  80:-0.151 ...   (đuôi ngọn; vòng giữa vẫy to gấp đôi)
== skill_01  0.93 s = 28 khung        (lao cắn)
  Translate bone2   0:0/0  6:-10.1/-0.747  13:-12.1/-3.59  14:1.53/1.62  15:20.8/-0.479  17:39.6/-0.479  22:20.8/20.2  28:0/0
  Rotate    bone3   0:0.413  6:19.4  13:44.1  14:-0.263  15:-47.6  17:-32.3  22:-25.2  28:0.413
  Rotate    bone4   0:3.01  6:-7.94  13:-29.8  14:23.4  15:-17.9  17:-20.1  22:-16.6  28:3.01
  Rotate    bone5   0:0.376  6:-49.7  13:-49.7  14:-77.7  15:28  17:13.6  22:-0.78  28:0.376
  Rotate    bone6   0:0  6:33.9  13:6  14:-6.74  15:91.4  17:62.3  22:78.2  28:0
  Rotate    bone16  0:-1.42  6:3.64  13:31.7  14:82.3  15:2.21  17:-1.94  22:-10.1  28:-1.42
  Rotate    bone20  0:0  6:-3.28  13:-5.62  15:-20.5  17:-30.3  22:-20.5  28:0     (miệng há lúc cắn, giữ, khép khi về)
  Translate A1      13:0/0  15:45/0  22:45/0  28:0/0
```

Đọc nhịp `skill_01`: **co 6 khung** (cổ gập lùi, đầu rụt: `bone5` −50°) → **giữ 7 khung, co sâu thêm** (`bone3` +44, `bone4` −30)
→ **khung gãy 14** (đốt giữa bật trước: `bone4` +23, ngọn còn ở sau: `bone5` −78, đầu +82) → **chạm ở khung 15** (1 khung;
`bone3` −48, `bone6` +91, gốc dời +21) → **quá đà khung 17** (gốc +40) → **giữ có trôi tới khung 22** (mỗi đốt đổi 3–15°) → về 6
khung. Chùm lông, đuôi văng trễ 2 khung.

## 4. Kế hoạch rig của mình (sau khi duyệt concept)

- Thân cắt thẳng từ concept (cách lai, skill mục 21, 22): cổ + đầu là lớp trước; vòng cuộn + đuôi lớp sau; chỗ khuất tô lại bằng
  vân sáp lát (tô phẳng nên làm bằng mã được). Sừng đầu và **lưỡi kunai cứng** (100 % một xương), không lò xo.
- Chuỗi xương: cổ 5–6 đốt từ đất lên gáy, vòng cuộn 4–5 đốt, đuôi 6–7 đốt; trọng số B-spline (không đỉnh nào bám 100 % một đốt).
  Idle: đầu mút dẫn, đốt kề ngược dấu, đầu bù góc; điểm phá nhịp = thè lưỡi chẻ + nghiêng đầu.
- Đòn thường (lao cắn): theo nhịp `skill_01` ở trên; miệng há to lúc cắn = **đổi ảnh** (xin GPT ảnh "giống hệt concept, chỉ há
  miệng, lộ nanh").
- Chiêu mana: há nhẹ (uốn lưới hàm dưới, `m < 0,55`), xương `mieng`, sự kiện `phun`; giữ há tới `phun` + 0,94 s.
- Chiêu cuối: đuôi quật chém 4–5 phát (dạng 2: 6–7 phát), mỗi phát 3–4 khung, khựng ở phát đầu và phát cuối; thân xoay theo đuôi,
  đầu vẫn nhìn đối thủ. Lưỡi chém / vệt là VFX; rig để xương `luoi_dao` ở mũi kunai và sự kiện `chem`.
- Dạng 2 gộp tiến hóa: bản nhẹ (ảnh 0,6 lần, lưới thưa 1,8 lần) để dạng 1 ≤ 0,5 MB.

## 5. Đã làm (2026-11-11)

- **Concept dạng 1 chốt**: `inbox/ran_sung_1/tai_ve/L1_duyet.png` (= `L1_sua_2.png`). Ba lượt mới đạt: tả lời ra đầu nhìn nghiêng,
  rồi chính diện mõm nhọn; lượt đạt đính **sơ đồ bố cục đầu tự vẽ** (`ran_sung_bo_cuc.py` → `inbox/ran_sung_1/mau/dau_bo_cuc.png`)
  cho GPT bám hướng quay, chỗ đặt mắt, đường miệng.
- **Concept dạng 2** (chờ người dùng duyệt): `inbox/ran_sung_2/tai_ve/L1_concept_2.png` (thân của bản thử `L1_thu.png`, đầu vẽ lại
  theo đầu dạng 1).
- **Ảnh miệng dạng 1** (lượt 2, đổi ảnh đầu): `M01.png` há to (cắn), `M02.png` hé nhỏ (bắn nước); lệch concept 0,1 px.
- **Rig dạng 1** `ran_sung.py` (`cat 1`, `rig 1`, `xem 1 <clip> <khung,...> [xuong]`) → `inbox/ran_sung_1/rig/` (130 KB, 22 xương):
  - lớp sau → trước: `duoi` (đuôi + sừng đuôi, gốc mọc thêm sau cổ), `than` (cổ + bụng + vòng cuộn MỘT lưới, chỏm cổ mọc thêm
    dưới đầu), `dau` (cứng, ba hình `dau` / `dau_ha` / `dau_he`), `mi_g`, `mi_x`, `luoi` (lưỡi chẻ vẽ bằng mã);
  - xương: `root → move → nhun → goc` (gốc cổ ở đất) `→ cuon` (vòng cuộn), `co0..6 → dau → mieng, luoi`, `duoi0..5 → sung`;
  - nét mực chung của hai lớp kề nhau thuộc lớp TRƯỚC, lớp sau gọt 3 px rồi tô nối dài (để lại thì thành sợi chỉ);
  - **vùng hoà trọng số cổ ↔ vòng cuộn phải rộng** (−30..130 px concept): hẹp (56 px) thì cổ ngả vào vòng cuộn là lưới gập,
    đốm và nét xoắn bị vò;
  - **kéo giãn chuỗi bằng dời đốt, không bằng tỉ lệ xương**: tỉ lệ truyền xuống con nên đầu phình 2,6 lần (7 đốt × 1,15);
  - mắt nhắm: tô lam kín mống (hai mảng vàng hai bên con ngươi, con ngươi vẽ bằng mực nên phải đóng khe rồi lấp lỗ).
- Clip (30 fps): `idle` 4 s (3 vòng 40 khung; vòng 2 nghiêng đầu, thè lưỡi hai lần, đuôi vẫy to; vòng 3 chớp mắt), `attack` 1 s
  (trúng 0,5 s: co 6 khung, giữ 7, khung gãy 14, chạm 15 có giãn 1,15, há to 14–17, ngoạm 18), `cast` (phun 0,5 s, hé miệng tới
  phun + 0,97 s), `skill` (5 nhát đuôi ở khung 16, 19, 22, 25, 30; sự kiện `chem`; lao 0,46 H), `hit`, `die`, `appear`.
- Chưa làm: dạng 2 (chờ duyệt concept), `evolve`, vào Unity (chờ người dùng chọn suất và tên).

## 6. Dựng lại theo KHÚC như con gốc (người dùng chê bản thân liền một cục, 2026-11-11 chiều)

Người dùng: "dạng 1 không ổn... phần thân bên trái này phải tách ra chứ giờ bạn đang làm thành 1 cục liền, xem kĩ họ gen từng khúc
như nào". Bản đầu tôi cắt cổ + bụng + vòng cuộn thành MỘT lưới (vòng cuộn chỉ là vùng trọng số): cổ ngả thì vòng cuộn bị kéo
méo theo, và không duỗi ra thành con rắn dài được.

**Cách con gốc dựng thân** (ảnh từng khúc: `scan/monster_3247/khuc_anh.png`; từng khúc trong dáng gốc: `khuc_dang_goc.png`; script
`khuc_3247.py` ở scratchpad phiên làm, vẽ lại từ `mesh.json` + atlas):
- Thân là **5 khúc "hạt đậu" rời**, mỗi khúc là một ống ngắn **tròn hai đầu, viền mực kín**, xếp chồng mép lên nhau như chuỗi xúc
  xích. Thứ tự vẽ sau → trước: `P_weiba02` (khúc thân sau DÀI hình chữ S, nằm khuất gần hết sau vòng cuộn và ngực, nối ra đuôi) →
  `P_weiba01` (chóp đuôi) → `P_huoyan` (chùm đuôi) → `P_shenti03` (khúc vòng cuộn bên trái) → `P_shenti02` (ngực / bụng dưới) →
  `P_shenti01` (cổ trên) → `P_bozi` (gáy) → mặt.
- Mép dưới của khúc trên (chỗ đè lên khúc dưới) vẽ bằng **nét nhạt màu vạch bụng**, không phải mực đen: nhìn thành vạch bụng, không
  thành đường cắt.
- Cả thân bám MỘT chuỗi xương liền từ đầu xuống đuôi; lúc đứng chuỗi cuộn lại (các khúc chồng lên nhau thành vòng cuộn), lúc lao /
  bò chuỗi duỗi ra và **vẫn những khúc ấy** xếp thành con rắn dài: đầu, cổ, ngực, "bướu" (khúc vòng cuộn), khúc thân sau, đuôi.

**Của mình (dạng 1), sau → trước:** `duoi` (ống dài từ sau vòng cuộn ra tới sừng: phần khuất sau thân tô bằng mã, có đốm, đầu mút
tròn) → `cuon` (khúc vòng cuộn riêng: phần khuất sau thân tô nốt thành hạt đậu kín) → `than` (cổ + ngực một khúc kín) → `dau`.
- Concept không có nét mực ở mép trái dưới của thân (lưng thân liền màu với vòng cuộn): **kẻ thêm một nét mực** nối tiếp viền trái
  cổ xuống viền đáy (`vien_than_them`) để thân thành khúc kín. Đây là chỗ duy nhất hình khác concept đã chốt.
- Xương: `goc → cuon → cn0, cn1` (vòng cuộn); `goc → co0..6 → dau`; `goc → duoi0..7 → sung` (ba đốt đầu của đuôi khuất sau thân).
- Lao cắn / trườn vào: cổ ngả dài ra trước, vòng cuộn thành bướu sau thân, **đuôi quăng qua phía trên ra sau** (`duoi_ra_sau`: xoay
  đốt gốc 168°, duỗi thẳng phần ngọn): thân duỗi thành con rắn dài như dáng `run_01` / `skill_01` của con gốc.
- `.atomik` 145 KB, 26 xương, 7 slot.

## 7. Tách mảnh MỘT – MỘT theo file Spine gốc (người dùng: "dịch ngược file spine gốc xem họ tách mảnh như nào... dựa vào đó mà gen theo", 2026-11-11)

Bản mục 6 vẫn bị trả: tôi mới tách được vòng cuộn, còn gộp cổ với ngực, thân sau với đuôi, cả đầu là một ảnh cứng đổi ảnh khi há.
Lần này rút hết file gốc bằng `mo_xe/chay.py att` (mọi hình của mọi slot, cả bộ hình không bật mặc định) và `mo_xe/to_manh.py`:
`scan/monster_3247/manh_anh.png` (18 ảnh mảnh), `manh_dang_goc.png`, `manh_dang_run.png`, `manh_dang_can.png` (từng mảnh trong từng dáng).

**Bảng mảnh của con gốc** (thứ tự vẽ sau → trước) **và mảnh của mình** (`inbox/ran_sung_1/manh/`, bảng so: `_so_voi_goc.png`):

| # | Con gốc | Là gì, bám xương nào | Của mình |
|---|---|---|---|
| 0 | `P_weiba02` 158 × 91 | khúc thân sau dài chữ S, khuất gần hết sau vòng cuộn và ngực; bám xương vòng cuộn + gốc đuôi | `than_sau` |
| 1 | `P_weiba01` 96 × 72 | chóp đuôi thon; bám 3 đốt đuôi | `duoi` |
| 2 | `P_huoyan` 90 × 128 | chùm đuôi mềm 4 đốt | `sung_duoi` (cứng, 1 xương `sung`) |
| 3 | `P_shenti03` 114 × 86 | khúc vòng cuộn | `cuon` (2 đốt `cn0`, `cn1`) |
| 4 | `P_shenti02` 87 × 121 | ngực / bụng dưới; bám gốc + 2 đốt cổ dưới | `nguc` |
| 5 | `P_shenti01` 97 × 134 | cổ trên, ĐÈ lên ngực; mép dưới vẽ nét nhạt như vạch bụng | `co` (mép dưới cắt đúng vạch bụng thứ hai) |
| 6 | `P_bozi` 107 × 91 | gáy: khối tròn sau mặt, bám ĐỐT CỔ CUỐI (không bám xương đầu) | `gay` |
| 7 | `P_mouth` 66 × 65 | khối miệng hồng, đáy có dải cằm; xương riêng, **trượt xuống từ sau mặt là há** | `ham` (vành hàm của concept + lòng miệng lấy từ ảnh M01 dời lên 92 px) |
| 8 | `P_yanpi` 100 × 83 | nền mắt (da + tròng trắng) sau mặt nạ | `nen_mat` (hai mảng vàng) |
| 9, 10 | `P_yanjing04`, `03` | hai con ngươi rời, mỗi cái một xương (liếc); lúc trúng đòn đổi sang `P_shouji02`, `01` (dấu < >) | `con_nguoi_x`, `con_nguoi_g` (+ `trung_x`, `trung_g`) |
| 11, 12 | `P_yanjing02`, `01` | hai mí rời | `mi_x`, `mi_g` (trượt xuống là nhắm) |
| 13 | `P_face` 103 × 86 | **mặt nạ có hai LỖ MẮT**, mép dưới là nét môi; bám xương đầu | `mat_na` |
| 14, 15 | `P_ear02`, `01` | hai chùm tai, mỗi chùm 3 đốt | `sung_x`, `sung_g` (cứng, mỗi sừng 1 xương; nằm SAU mặt nạ vì da phủ lên gốc sừng) |

Mẹo của họ đã chép: (1) mặt nạ bám xương đầu còn gáy bám đốt cổ cuối → xoay / dời xương đầu là mặt xê dịch trên khối gáy, đầu như
quay; (2) mắt là lỗ trên mặt nạ, sau lỗ có nền mắt, con ngươi, mí nên liếc và chớp được mà không cần mặt nạ cắt; (3) há miệng không
đổi ảnh đầu: khối miệng nấp sau mặt, trượt xuống là lộ lòng miệng; (4) lúc lao họ đổi sang bộ slot thứ hai (cùng ảnh, bám chuỗi xương
thẳng); của mình không có path constraint nên xoay chuỗi đuôi ra sau bằng khoá (mục 6).

Rig dạng 1 sau khi tách: 33 xương, 17 slot, 19 hình, `.atomik` 140 KB. Ảnh `M02` (hé miệng) không còn dùng; `M01` chỉ dùng lấy
lòng miệng, lưỡi, nanh cho mảnh `ham`.

## 8. Mảnh GEN theo kiểu mảnh của con gốc (người dùng: "tách ra và phải gen theo giống họ chứ, vài mảnh gen hơi khác", 2026-11-11)

Bản mục 7 đúng số mảnh nhưng hình từng mảnh là mẩu cắt nham nhở từ concept, phần khuất tô phẳng bằng mã: không giống mảnh của họ
(khối kín vẽ hoàn chỉnh). Sửa:
- `ran_sung.py cat 1` dựng **tờ hướng dẫn** `inbox/ran_sung_1/mau/manh_A.png` (+ `manh_A.json`): sáu mảnh cổ, ngực, vòng cuộn, thân sau
  chữ S (đường giữa + bề dày khai trong CFG), chóp đuôi (đầu trái tròn kín), khối miệng, đặt rời đúng tỉ lệ concept.
- `build_ran_sung.py` → `gui_gpt/ran_sung_1/luot_3_manh.txt`: GPT **vẽ lại sáu mảnh thành khối kín hoàn chỉnh, đúng chỗ, đúng cỡ**
  (ảnh 1 concept, ảnh 2 tờ hướng dẫn) → `tai_ve/M03.png`. Một lượt là được, GPT giữ chỗ và cỡ rất sát.
- `ran_sung.py nhan 1`: cắt tờ GPT theo ô, đưa về toạ độ concept, dò lệch ±16 px so với bản mã, thay ảnh trong `manh/` (bản mã giữ
  ở `manh/_ma_<tên>.png`). IoU với bản mã: cổ 0,91; ngực 0,86; vòng cuộn 0,97; thân sau 0,91; chóp đuôi 0,94; khối miệng 0,85.
  **Chạy `cat` rồi phải chạy lại `nhan`** (cat ghi đè mảnh bằng bản mã).
- Mí là mảnh bán nguyệt như `P_yanjing01/02` (không mọc thêm lên trên): nheo = kéo giãn mí từ mép trên lỗ mắt; nhắm hẳn = đổi hình
  trong slot mí sang `nham_g/x` (lấp kín lỗ mắt màu da + một nét mắt nhắm), như họ đổi hình mắt lúc trúng đòn. Thử cho mí trượt / giãn
  che kín mắt thì mí thò ra ngoài đầu, và tắt nền mắt thì lộ lòng miệng qua lỗ mắt.
- Nền mắt là một tấm da có hai tròng vàng như `P_yanpi`.
- IoU khung 0 idle với concept còn 0,95 (mảnh GPT không trùng concept từng pixel); `.atomik` 152 KB, 33 xương, 17 slot, 21 hình.

## 9. Vòng cuộn là một KHÚC THÂN chữ C; gáy chỉ là phần trên sau đầu (2026-11-11)

- Người dùng: "phần vòng cuộn này khác quá... ảnh animation run thấy 3 khúc của nó phân biệt rõ nhất". `P_shenti03` là khúc thân cong
  như hạt đậu (lưng một phía, bụng nhạt một phía); bản của mình là đĩa tròn có nét xoắn. Sửa: `cat` khoét mép phải khối tròn
  (`cuon_khoet`) thành chữ C mở sang phải, dải bụng nhạt dọc mép trong → tờ hướng dẫn `mau/manh_B.png` → GPT vẽ lại
  (`luot_4_cuon.txt` → `M04.png`) → `ran_sung.py nhan 1 M04 B`. Lúc đứng hai đầu chữ C khuất sau ngực (nhìn vẫn như concept); lúc lao,
  trườn, chết thì `bung_cuon` xoay khúc 86° quanh tâm thành cái bướu giữa ngực và thân sau, như dáng `run_01` của con gốc.
- Người dùng: "idle cũng bị lỗi nặng" (ảnh chụp: một vành lam có viền lòi ra dưới cằm). Nguyên nhân: khối gáy làm cùng hình bóng với
  cả đầu, mặt nạ xê dịch là gáy thò ra dưới hàm. `P_bozi` chỉ nằm phía trên sau mặt. Sửa: gáy cắt từ ngang giữa mắt trở lên, bo tròn đáy.
- Mảnh ngực GPT vẽ có mũi nhọn ở góc dưới trái, lúc thân duỗi nó thò ra như cái chân: `CFG["got"]` gọt và kẻ lại viền sau khi `nhan`.
- Thứ tự chạy khi làm lại: `cat 1` → `nhan 1 M03 A` → `nhan 1 M04 B` → `rig 1`.

## 10. XOÁ HẾT, RESKIN RIG GỐC (người dùng: "xóa hết tất cả đi mà xây lại, gen y hệt con gốc rồi reskin thôi", 2026-11-11 tối)

Bỏ mọi bản rig tự dựng (mục 4–9). Dùng NGUYÊN rig Spine của `monster_3247` (41 xương, lưới, trọng số, 9 clip), chỉ vẽ lại DA
từng mảnh, như cách dự án vẽ đè lên rig aola. Hình và chuyển động gốc là của hãng làm game tham khảo: không đăng công khai.

Đường làm (`ArtGen/Spine/ran_sung.py`, viết lại hoàn toàn):

1. `to k`: dựng hai tờ mảnh gốc phóng 3 lần cho GPT (`inbox/ran_sung_<k>/mau/goc_A.png` 7 mảnh thân, `goc_B.png` 11 mảnh đầu),
   mỗi mảnh cắt theo đa giác lưới của nó (atlas gốc xếp theo đa giác, khung chữ nhật lẫn mẩu mảnh khác).
2. `build_ran_sung.py` sinh `gui_gpt/ran_sung_<k>/luot_2_reskin_A.txt`, `_B.txt` (ảnh 1 concept đã duyệt, ảnh 2 tờ mảnh gốc):
   GPT vẽ lại từng mảnh, GIỮ hình bóng, chỗ, cỡ; chùm tai và chùm đuôi đổi thành sừng đen. Lưu `tai_ve/R01.png`, `R02.png`.
3. `nhan k`: cắt theo ô, dò lệch ±12 px, thu về cỡ ảnh gốc × 4/3, lưu `da/<vùng>.png`. Lần đầu GPT giữ hình bóng rất sát
   (IoU 0,93–0,98 với mảnh gốc).
   - Lỗ mắt của mặt nạ: mảng trắng kín trong hình mà nằm ở chỗ mảnh gốc trong suốt thì khoét trong suốt.
   - Alpha nhân với alpha gốc nới 5 px: hình không tràn lưới, mép mềm của mảnh gốc vẫn mềm.
   - Sừng (P_ear01, P_ear02, P_huoyan): không dò lệch (hình khác hẳn); sừng to hơn khung thì nới khung ảnh (`da/_noi.json`);
     sừng phải lật ngang (GPT vẽ hai sừng cong cùng chiều).
   - Đĩa con ngươi không viền: tô lại dải mép bằng màu giữa (mép lẫn nền trắng thành vành nhạt); tròng mắt trên nền mắt kéo về
     đúng màu đĩa.
4. `rig k`: NƯỚNG rig gốc. Mọi xương gốc thành con trực tiếp của `nhun` (root → move → nhun), mỗi khung khoá vị trí, góc, tỉ lệ
   thế giới lấy từ `mau_khung.json` (lấy mẫu bằng runtime Spine thật, 30 khung/giây, có ma trận): IK và path constraint của rig
   gốc biến thành khoá FK, `.atomik` chạy được. Lưới, uv, trọng số giữ nguyên.
   - Sừng CỨNG: cả hình bám một xương, lưới là ô chữ nhật cả khung ảnh. Sừng đầu → `bone16` (không bám xương tai: tai gốc vẫy);
     sừng đuôi → `bone13` (đốt cuối mà chóp đuôi còn bám); dáng bò (`P_huoyan2`) → `bone34`.
   - Hai sừng đầu vẽ SAU mặt nạ (gốc sừng khuất sau đỉnh đầu như concept; chùm tai gốc thì đè lên trán).
5. `them`: hai clip con gốc không có, viết khoá trên chính bộ xương gốc (`extra.json` nạp vào runtime Spine thật, IK/path của nó
   vẫn chạy), lấy mẫu rồi nướng như clip gốc:
   - `cast` 1,67 s: ngửa lấy hơi → chồm tới há nhẹ miệng (`bone20` −11°) → giữ, rung nhẹ → ngậm. Sự kiện `phun` 0,47 s,
     `het_phun` 1,4 s. Đuôi hạ xuống né đường tia (dáng đứng thì sừng đuôi nằm ngay trước miệng). Tia là việc của lớp VFX.
   - `skill` 1,4 s: lao tới, đuôi giơ cao rồi quất chém 7 nhát lên xuống trong nửa giây (khung 12, 15, 17, 20, 22, 25, 27), nhát
     cuối giơ thêm một nhịp rồi bổ mạnh nhất; sự kiện `chem` mỗi nhát (chuỗi `xuong` / `len`). Nâng gốc đuôi bằng xương `A2`.
6. Clip dùng lại của con gốc: `idle` = idle_01, `attack` = skill_01 (lao cắn, trúng ở khung 15) + xương `move`, `hit` = hit_01,
   `die` = die_01 + mờ dần, `appear` = run_01 lặp rồi hoà về dáng đứng.

Kết quả dạng 1: 45 xương, 20 slot, 333 đỉnh, 7 clip, `.atomik` 124 KB. Đã soi tờ khung cả 7 clip; chưa xem tốc độ thật.

Lỗi gặp: gỡ xoay vùng atlas `rotate: 90` sai chiều làm mảnh lộn 180° (sửa trong `mo_xe/to_manh.py`); sừng bị cắt mép vì to
hơn khung chùm lông; gốc sừng đầu đè trán (đổi thứ tự vẽ).

Còn lại: dạng 2 (chờ duyệt concept), `evolve`, vào Unity (chờ người dùng chọn suất và tên).

## 11. Liền khối: bỏ nét mực ở chỗ nối các khúc thân (người dùng dặn 2026-11-11 tối, sau khi duyệt bản reskin)

Người dùng: "phần nối giữa các part bỏ viền đen đi tạo cảm giác liền khối" (ba chỗ: đỉnh vòng cuộn, mép trái khúc ngực, gáy cạnh
mắt). Con gốc viền đen quanh từng khúc nên chỗ khúc trước đè khúc sau có nét mực cắt ngang thân.

`ran_sung.py lien k` (chạy sau `nhan`, trước `rig`):
- Dựng rig với da còn nét, nướng idle, với từng điểm trên mép mỗi khúc thân (cổ, ngực, vòng cuộn, gáy) dò ra ngoài mép 4 px: sau
  nó là khúc thân khác CÙNG MÀU (lưng trên lưng, bụng trên bụng) hoặc nét mực của khúc dưới (nét đôi) thì là chỗ nối. Điểm nào là
  chỗ nối ở ≥ 80% số khung nhìn thấy thì bỏ mực (tô lại bằng màu gần nhất bên trong). Giữ nét ở viền ngoài và ở chỗ đổi màu
  (bụng nhạt đè lên lưng: thân vòng ra sau, cần nét để thấy lớp).
- Nét lam nhạt GPT vẽ ở mép mềm mà chạy qua phần lưng cũng tô lại (trên lưng chàm của dạng 2 nó thành một vệt sáng).
- Hai mảnh đuôi không bỏ nét của chính nó (đuôi vẫy, mép lộ ra luôn).
- Kết quả `da/_lien/<vùng>.png`, ảnh soi `da/_lien/_soi.png` (đỏ = đoạn bỏ mực).
- Lúc lao cắn, bò vào, trúng đòn thân duỗi ra, mép đã bỏ mực lộ thành viền ngoài không nét. Nên mỗi khúc có thêm hình
  `<hình>_vien` (da còn nét); `lien` ghi `da/_lien/_lo.json` (khung nào khúc nào lộ quá 40% đoạn đã bỏ mực), clip đổi sang bản
  còn nét đúng những khung đó. idle, cast, skill, die: không khung nào phải đổi.
- Lỗi đã gặp: nhận "mực" bằng kênh lam thấp thì lưng chàm đậm của dạng 2 (lam 143) bị coi là mực, tô thành vệt nhạt. Mực = cả ba
  kênh đều tối.

## 12. Dạng 2 (concept duyệt 2026-11-11 tối: "dạng 2 tôi thấy ổn")

Cùng rig gốc, cùng cách reskin; khác dạng 1 ở:
- To hơn: cả rig và ảnh da phóng 1,15 (`KK`); chậm hơn 10% (`CHAM`).
- Da: lưng chàm đậm `#22388F`, sừng đầu to có nhánh phụ, lưỡi đuôi to có hai đôi ngạnh (khung ảnh sừng tự nới).
- Mảnh thêm con gốc không có: script vẽ hình giữ chỗ xám vào tờ B, GPT vẽ lại; rig đặt nhiều bản:
  - `X_nanh`: 2 nanh (một bản lật), bám xương đầu, vẽ sau mặt nạ (gốc nanh khuất sau môi trên), trước khối miệng.
  - `X_gai`: 5 gai lưng dọc mép sau khúc cổ, mỗi gai lấy trọng số của da cổ ngay chỗ nó (đi theo cổ uốn), vẽ sau khúc cổ.
  - `vong2`: vòng thân thứ hai = bản sao khúc vòng cuộn phóng 1,2, vẽ sau lưng mọi thứ (thân dài hơn); ẩn theo khúc vòng cuộn
    ở dáng bò.
- Chiêu mạnh hơn: skill 11 nhát (dạng 1: 7 nhát), nhịp dồn hai khung một nhát, nhát cuối giơ lâu rồi bổ; cast biên độ 1,25, há to
  hơn.
- `ran_sung.py all`: xuất dạng 2, rồi dạng 1 gộp bản nhẹ của dạng 2 (ảnh 0,55) cho clip `evolve` 2,8 s: dạng 1 ngửa gồng (dáng
  lấy hơi của cast), đổi dạng lúc 1,25 s, dạng 2 chồm tới há miệng gầm rồi hoà về khung 0 idle dạng 2.

Dung lượng: dạng 1 (có evolve) 180 KB, dạng 2 168 KB. Đã soi tờ khung mọi clip; chưa xem tốc độ thật.

### Sửa thêm bước liền khối cho dạng 2 (người dùng: "dạng 2 xóa outline đen các chỗ giống dạng 1", 2026-11-11 tối)

- Vòng thân thêm (`P_vong2`) tính là thân (`THAN_SAU`): khúc vòng cuộn đè lên nó thì bỏ nét, hai vòng liền thành một khối, chỉ còn
  viền ngoài. Gai lưng thì không: mép cổ sau gai vẫn giữ nét.
- Tô lại cả DẢI MÉP rộng bằng nét mực ở đoạn bỏ (không chỉ pixel mực): pixel lẫn mực với lưng chàm không tối hẳn, để lại vệt sẫm.
- Tô theo ngữ cảnh: mép ở phần lưng lấy màu lưng, mép ở phần bụng lấy màu bụng (lấy màu gần nhất bất kể lớp thì ra chấm nhạt
  trong lưng, vệt lam giữa bụng).
- GPT tự tô mảng sẫm ở đầu dưới khúc cổ, khúc ngực của dạng 2 (trái luật tô phẳng): kéo sáng về mức giữa của lưng.
- Còn sót: vài đốm nhạt cỡ 2–3 px ở chỗ cổ giáp vòng cuộn của dạng 2.

### Sửa dạng 2 sau khi người dùng xem (2026-11-11 khuya): "xương đuôi đen ghép lệch", "đòn thường phần giữa rối, khớp đầu với thân giữa không match"

- **Sừng đuôi tự đặt (`TU_DAT`, chỉ dạng 2):** sừng dạng 2 to hơn chùm lông cũ mà vẫn đặt theo khung chùm lông + số dời tay của
  dạng 1 nên gốc sừng trượt khỏi chóp đuôi. Giờ tính trục của hình sừng và của mảnh chóp đuôi (`truc_hinh`: đầu to, đầu nhọn), đặt
  gốc sừng (lùi vào 13% chiều dài) đúng đầu mút nhọn của chóp đuôi, trục sừng theo hướng chóp đuôi rồi ngóc thêm 30°.
- **Khoá sừng theo TÊN SLOT, không theo tên hình:** slot dáng bò `P_huoyan2` có hình cũng tên `P_huoyan`, khoá theo tên hình thì
  sừng dáng bò bám nhầm xương dáng đứng (bone13 thay vì bone34). Dạng 1 trước đó "trông đúng" chỉ vì xương dáng đứng không động
  trong clip bò. Đã sửa cho cả hai dạng.
- **Làm phẳng lưng ngay lúc nhận da (`phang_lung`):** GPT tô sẫm và gạch chì đậm ở cuối khúc cổ, khúc ngực dạng 2. Sửa ở `nhan` để
  cả bản còn nét (dùng lúc lao cắn) lẫn bản bỏ nét đều sạch.
- **Tô lại mép bằng màu LÕI gần nhất:** bỏ kiểu chọn màu theo ngữ cảnh lưng/bụng (ở góc lưng giáp bụng nó tạo mảng trắng lởm chởm,
  chính là chỗ "khớp không match").
- **Vòng thân thêm ẩn tức thì lúc bật ra lao cắn**, hiện lại lúc thu về (thân duỗi thì nó thành khối đôi; mờ dần thì thành bóng ma).

## 13. Vào game (người dùng: "ok cho vào game, thay thế tướng cũ đi", 2026-11-11 khuya)

- Suất: `uyen_xa` (ải 50 đảo Thủy), thay rig cũ tm08 (rắn đèn). Id giữ nguyên.
- `ArtGen/Spine/quai/da_nhan.json` dòng `uyen_xa` trỏ sang `inbox/ran_sung_<k>/rig`; `vao_game.py` đã chép `.atomik` và chân dung vào
  `Assets/03 Art/Heroes/Resources/uyen_xa_1|2/` (bản cũ còn trong lịch sử git; rig nguồn tm08 không có ở máy này).
- `StageView.WaterFx`: `uyen_xa` = `n_tia`, chiêu cuối `n_va` cả hai dạng. `HatNuoc.WThemes`: lam cô-ban, bỏ họa tiết sao.
- Không đổi `heroes.json`, `cards.json`, golden: tên tướng "Uyên Xà", danh hiệu "Rắn đèn vực sâu", dạng "Uyên Nhi; Uyên Xà", thẻ
  "Thủy Thương / Mưa Bọt / Đèn Vực Sâu" còn nguyên, chờ người dùng đặt lại.
- Chưa làm: Unity nhập lại và biên dịch (máy này không có MCP 8090; Unity tự nhập khi được đưa lên trước), chụp thử trong Unity,
  xem trong trận; vệt chém của chiêu cuối (lớp VFX, sự kiện `chem` + xương `b_bone13`); `game.shadow` không có slot (như các rig khác).
