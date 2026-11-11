# Dòng sò đột biến (mã làm việc `so_gai`): tướng thứ 4 đảo Thủy (2026-11-11)

Người dùng lên ý tưởng và duyệt concept; mảnh, rig Claude tự làm. Gói prompt: `ArtGen/Spine/build_so_gai.py` →
`gui_gpt/so_gai_<k>/`, ảnh về `inbox/so_gai_<k>/tai_ve/`.

## 1. Ý người dùng

- Concept: con sò đột biến, ở trong có lưỡi, có mắt ở mai trên như con gốc (`monster_3237`).
- `idle`: giống con gốc, sửa một chút cũng được.
- Đòn thường: há hai mai to rồi **đớp mạnh**, có sức nặng như `skill_01` của con gốc.
- Chiêu mana: vẽ thêm phần **chu môi** (hai mai khép khít, chụm lại ở giữa như chu môi), **nhổ ngọc trai** bắn vào đối thủ;
  đạn ngọc trai vẽ riêng.
- Chiêu cuối: như `skill_02`, **lè lưỡi lao tới, dùng lưỡi quật vài phát**.
- Dạng 2: y vậy nhưng to hơn, chiến hơn. Mỗi dạng ≤ 0,5 MB, ít hơn càng tốt.

## 2. Mổ xẻ con gốc `monster_3237` (chỉ học cấu trúc và nhịp, không lấy hình)

Nguồn: `D:\Ripper\SwordxStaff\web\assets\Monster\monster_3237\` (Spine 4.2.28, 0,1 MB, atlas 588 × 232, tỉ lệ 0,75).
Kết quả quét: `D:\Ripper\SwordxStaff\scan\monster_3237\` (`info.json`, `keys.json`, `mesh.json`, `khung/<clip>.jpg`).

### Ảnh (22 vùng)

Mai trên `P_tou1` 232 × 116 · mai dưới mặt ngoài `P_xiaba` 222 × 102 · lòng mai dưới (mảng tối) `P_xiaba1` 219 × 102 · 8 gai rời
`P_ci1..8` · 2 nanh `ya1, ya2` · 2 mày hình sừng `P_meimao1, 2` · lưỡi 3 ảnh thay nhau `P_shetou` (nằm trong miệng), `P_shetou1`,
`P_shetou2` (thè ra, quật) · mắt 2 ảnh trên một slot: `P_yanjing1` (mở: hai chấm đen), `P_yanjing2` (nhắm: hai nét chữ V).

### Xương (16)

```
root    cha -       x     0.0 y     0.0 góc    0.0 dài   0.0   
bone    cha root    x     0.0 y   -50.0 góc    0.0 dài   0.0   gốc (y −50)
bone2   cha bone    x     0.0 y   567.8 góc    0.0 dài   0.0   trục lộn nhào (ở cao, chỉ dùng khi bị hất)
shadow  cha bone    x     0.0 y    50.0 góc    0.0 dài 250.0   bóng
bone3   cha bone2   x   252.9 y  -355.5 góc    0.0 dài 100.0   đệm
bone4   cha bone3   x  -250.3 y    -2.3 góc    0.0 dài   0.0   TÂM THÂN: dời, nén giãn, nghiêng cả con
bone5   cha bone4   x  -112.8 y    23.8 góc   17.5 dài 200.0   MAI TRÊN (xoay quanh bản lề phía sau)
bone6   cha bone4   x  -101.8 y   -63.1 góc  -13.8 dài 180.0   MAI DƯỚI (xoay quanh bản lề phía sau)
bone19  cha bone5   x   185.8 y   -46.4 góc  -17.5 dài   0.0   mắt (trên mai trên)
bone17  cha bone19  x   -30.7 y    17.1 góc  148.4 dài  92.6   mày gần
bone18  cha bone19  x    31.9 y    15.5 góc   71.4 dài  61.3   mày xa
bone20  cha bone6   x    52.0 y    88.9 góc  -19.0 dài  50.8   lưỡi đốt 1 (con của mai dưới)
bone21  cha bone20  x    50.8 y     0.0 góc   -2.4 dài  36.2   lưỡi đốt 2
bone22  cha bone21  x    36.2 y     0.0 góc   -8.3 dài  25.0   lưỡi đốt 3
bone23  cha bone22  x    25.0 y     0.0 góc  -10.1 dài  22.9   lưỡi đốt 4
bone24  cha bone21  x    -1.9 y    -6.5 góc    0.0 dài   0.0   đệm lưỡi
```

### Slot (sau → trước) và lưới

`shadow` · gai 8 · **lòng mai dưới** · lưỡi (3 slot ảnh) · **mai dưới mặt ngoài** · gai 7, 1 · nanh 1, 2 · gai 2, 3, 4 · **mai trên**
· gai 6 · mắt · mày 2, 1 · gai 5. Lưỡi nằm KẸP giữa lòng mai dưới (sau) và mặt ngoài mai dưới (trước): khép miệng thì lưỡi nấp sau
vành mai dưới.

- Hai mai, gai, nanh, mày: ảnh chữ nhật 4 đỉnh bám CỨNG một xương (mai trên `bone5` kèm nanh và gai của nó; mai dưới `bone6`).
- Lưỡi: 3 lưới 20–30 đỉnh bám chuỗi 4 đốt `bone20..23` (+ `bone6` ở gốc), là phần mềm duy nhất.
- Không IK, không physics, không deform.

### Mẹo diễn chính

1. **Hai mai xoay quanh bản lề phía sau** (`bone5`, `bone6` cùng gốc ở lưng): há là mai trên ngửa lên, mai dưới gần như đứng yên.
2. **Cả con nén giãn, nghiêng trên `bone4`** (tâm thân); đòn đánh ngửa hẳn cả thân ra sau rồi bổ xuống.
3. Mày xoay nhẹ theo nhịp (nhíu khi đánh), mắt đổi sang ảnh nhắm lúc trúng đòn, lúc đớp.
4. Lưỡi: đổi ảnh theo dáng (nằm, thè, quật) + uốn 4 đốt; `skill_02` thè lưỡi quật hai phát.

### Clip (10)

| Clip | Dài | Số timeline |
|---|---|---|
| `block_01` | 0.50 s (15 khung) | 15 |
| `die_01` | 1.00 s (30 khung) | 23 |
| `floating_01` | 1.50 s (45 khung) | 15 |
| `hit_01` | 0.50 s (15 khung) | 15 |
| `hit_02` | 0.67 s (20 khung) | 24 |
| `idle_01` | 4.00 s (120 khung) | 13 |
| `run_01` | 0.80 s (24 khung) | 16 |
| `skill_01` | 1.00 s (30 khung) | 15 |
| `skill_02` | 1.13 s (34 khung) | 23 |
| `stun_01` | 1.33 s (40 khung) | 23 |

`idle_01` 4 s: thở chậm, hai mai hé ra khép vào lệch pha, lưỡi nhúc nhích. `skill_01` 1 s: ngửa cả thân + há to (0,1–0,5 s), bổ
xuống đớp (0,55–0,64 s), nảy về. `skill_02` 1,13 s: há, thè lưỡi, quật hai phát (0,2 và 0,6 s), thu lưỡi.

## 3. Khoá gốc của các clip sẽ học (khung 30 fps; góc là lệch so với dáng gốc; `x/y` dời hoặc tỉ lệ)

```
== idle_01  4.00 s = 120 khung
  Rotate    bone2   0:3.85  20:-2.96  40:3.85  60:-2.96  80:3.85  100:-2.96  120:3.85
  Rotate    bone5   0:0.112  16:1.79  38:0.048  40:0.112  51:1.79  55:0.048  59:2.68  63:-0.214  67:3.63  71:0.377  80:0.112  96:1.79  118:0.048  120:0.112
  Rotate    bone6   40:0  51:-4.36  55:-1.86  59:-4.13  63:-1.86  67:-3.32  80:0
  Translate bone6   0:-0.955/-2.9  40:-0.955/-2.9  51:-5.78/-0.17  55:-1.06/-0.616  63:-4.85/-2.81  67:-2.3/-2.95  80:-0.955/-2.9
  Rotate    bone17  0:0  20:7.21  40:0  60:7.21  80:0  100:7.21  120:0
  Rotate    bone18  0:0  20:-11.8  40:0  60:-11.8  80:0  100:-11.8  120:0
  Rotate    bone20  0:2.22  5:3.77  27:-4.33  40:2.22  45:3.77  67:-4.33  80:2.22  85:3.77  107:-4.33  120:2.22
  Rotate    bone21  0:4.83  11:15.7  29:-6.09  40:4.83  51:15.7  69:-6.09  80:4.83  91:15.7  109:-6.09  120:4.83
  Rotate    bone22  0:-13.1  20:21  40:-13.1  60:21  80:-13.1  100:21  120:-13.1
  Rotate    bone23  0:-13.3  5:-20.1  26:18.8  40:-13.3  45:-20.1  66:18.8  80:-13.3  85:-20.1  106:18.8  120:-13.3
  Rotate    bone4   0:0.807  10:8.79  30:-7.17  50:8.79  70:-7.17  90:8.79  110:-7.17  120:0.807
  Translate shadow  0:22/0  20:-21.8/0  40:22/0  60:-21.8/0  80:22/0  100:-21.8/0  120:22/0
  Scale     shadow  0:1/1  20:0.969/0.969  40:1/1  60:0.969/0.969  80:1/1  100:0.969/0.969  120:1/1
== skill_01  1.00 s = 30 khung
  Rotate    bone4   0:0.807  3:5.61  13:5.61  15:-0.637  16:-28.9  17:-35.7  21:8.56  25:10.4  30:0.807
  Translate bone4   0:0/0  3:37.5/85.3  13:37.5/85.3  15:136/66.7  16:208/-22.2  17:102/-170  21:-32.9/-8.56  25:-24/40.6  30:0/0
  Translate shadow  0:22/0  3:23/0  13:28.3/0  16:190/0  17:72.8/0  21:-23.1/0  25:-12.7/0  30:22/0
  Scale     shadow  0:1/1  3:0.896/0.896  13:0.943/0.943  16:0.737/0.737  17:1.1/1.1  21:1.29/1.29  25:0.936/0.936  30:1/1
  Rotate    bone2   0:3.85
  Rotate    bone5   0:0.112  3:42.8  13:55.4  15:33.1  16:59.3  17:-37.7  19:-19.3  21:-21.3  25:-4.93  30:0.112
  Rotate    bone6   0:0  3:-24.7  13:-35.2  15:-33.4  16:-56  17:-3.48  21:-8.64  25:-17.7  30:0
  Translate bone6   0:-0.955/-2.9  3:4.97/-3.13  13:4.97/-3.13  15:-20.1/-0.424  17:-10.7/-5.69  21:-16.6/-9.38  25:-21.3/0.186  30:-0.955/-2.9
  Rotate    bone17  0:0  3:-28.6  15:-34.5  17:20.6  21:12.1  25:-24.3  30:0
  Rotate    bone18  0:0  3:16.7  15:2.16  17:-34.8  21:-21.3  25:4.81  30:0
  Rotate    bone20  0:2.22  3:1.79  12:10.9  13:8.89  15:13.2  17:3.44  21:-10.8  25:4.52  30:2.22
  Scale     bone20  0:1/1  3:1.61/1  25:1.61/1  30:1/1
  Rotate    bone21  0:4.83  3:-22.1  13:-0.82  15:-15.6  17:-18.5  21:-13.6  25:-9.93  30:4.83
  Rotate    bone22  0:-13.1  3:-19.3  13:-4.97  15:-16.7  17:-2.06  21:1.43  30:-13.1
  Rotate    bone23  0:-13.3  3:1.55  13:-3.32  15:-1.05  17:0.7  21:43.2  25:-9.92  30:-13.3
== skill_02  1.13 s = 34 khung
  doi anh P_shetou: kh 0 -> None
  doi anh P_shetou1: kh 0 -> P_shetou1
  doi anh P_shetou2: kh 0 -> P_shetou2
  Rotate    bone4   0:0.807  8:22  11:-35.7  13:-31.6  16:17.2  18:65.5  21:4.66  23:-31.4  26:-2.2  30:26.2  34:0.807
  Translate bone4   0:0/0  8:-6.93/4.63  11:83.5/-70.5  13:48.8/-157  16:73/-29.2  18:-15.1/40.7  21:-15.9/-10  23:-5.15/-11.1  26:25.7/8.19  30:-0.127/38.4  34:0/0
  Translate shadow  0:22/0  3:19.9/0  8:22.1/0  11:113/0  13:55.6/0  16:114/0  18:-2.2/0  23:13.9/0  30:26/0  34:22/0
  Scale     shadow  0:1/1  3:0.926/0.926  8:0.918/0.918  11:1.1/1.1  13:1.15/1.15  18:1/1  23:1.16/1.16  30:1.01/1.01  34:1/1
  Rotate    bone2   0:3.85
  Rotate    bone5   0:0.112  3:39.4  8:20.3  11:26.4  16:28.7  18:21.1  23:25.7  30:2.74  34:0.112
  Rotate    bone6   0:0  3:7.57  8:7.57  11:15.9  13:-3.42  16:-4.8  18:11.8  21:10  23:-2.64  30:11.1  34:0
  Translate bone6   0:-0.955/-2.9  3:26.3/-4.05  8:14.5/-2  11:27.8/-1.89  13:11/0.961  16:12.6/-3.09  18:23.1/-6.49  21:24.5/-1.81  23:8.11/2.45  30:13.4/-9.71  34:-0.955/-2.9
  Rotate    bone17  0:0  8:17.6  18:9.51  34:0
  Rotate    bone18  0:0  8:-27.5  18:-20.3  34:0
  Rotate    bone20  0:2.22  3:14.2  8:75.2  11:56.8  13:6.77  16:-53.6  18:2.92  21:73.8  23:-15.6  26:14.9  30:28.8  34:2.22
  Scale     bone20  0:1/1  3:1.66/1  8:1.72/1  11:2.07/1  13:1.38/1  18:1.68/1.01  21:1.96/1.01  23:1/1
  Rotate    bone21  0:4.83  3:-59.9  8:66.5  11:76.5  13:2.62  16:-66  18:-30.3  21:67.4  23:-49.7  26:-44.9  30:48.6  34:4.83
  Scale     bone21  0:1/1  3:2.61/1  8:2/1  11:2.55/1  13:2.2/1  16:2.6/0.867  18:2.61/1  21:3.02/1  23:1.72/1  26:1.98/1  34:1/1
  Rotate    bone22  0:-13.1  3:-39  8:49.2  11:69.5  13:86  16:-60.9  18:79.3  21:56.2  23:78.7  26:-40.1  30:-59.1  34:-13.1
  Scale     bone22  0:1/1  3:1.62/1  8:1.62/1  13:3.21/1  16:2.95/1  18:3.21/1  23:2.17/1  26:2.51/1  34:1/1
  Rotate    bone23  0:-13.3  3:-14.5  8:46.1  11:54  13:66.4  16:-59.6  18:-78.2  21:46.7  23:71.1  26:-25.3  30:-49  34:-13.3
  Scale     bone23  0:1/1  3:2.08/1  8:2.08/1  13:2.82/1  16:3.11/1  18:3.26/1  23:2.38/1  26:2.84/1  34:1/1
  Translate bone24  0:0/0  3:-16.2/-13.1  13:0/0  16:-26.5/-43.9  18:-32.7/-18.9  21:-23.4/28.2  23:-8.04/13.5  26:0/0
  _DrawOrder slot shadow (2 số)
== hit_01  0.50 s = 15 khung
  doi anh P_yanjing1: kh 0 -> P_yanjing2, kh 9 -> P_yanjing1
  Rotate    bone4   0:68.8  4:78.8  6:57.6  9:15  15:0.807
  Translate bone4   0:-76.2/-5.82  2:40.2/0.869  4:-45.9/14.3  6:-53.6/5.14  9:-31.3/-52  12:-18.7/-77.7  15:0/0
  Rotate    bone2   0:1.62  15:3.85
  Translate shadow  0:-66.1/0  2:44.4/0  4:-11.5/0  6:-38.2/0  9:-60.5/0  15:22/0
  Scale     shadow  0:0.859/0.665  2:0.864/0.641  4:0.866/0.624  6:0.979/0.979  9:1.12/0.95  15:1/1
  Rotate    bone5   0:-24.1  4:-18  6:14.5  9:65.3  15:0.112
  Rotate    bone6   0:1.69  4:-2.87  6:-1.34  9:32.5  15:0
  Translate bone6   0:5.47/3.04  4:-11/-3.61  6:4.75/-4.13  9:56.1/26.6  15:-0.955/-2.9
  Rotate    bone17  0:-9.31  4:-21.3  6:-26.1  9:-13.6  15:0
  Rotate    bone18  0:16.2  4:32.3  6:23.5  9:5.49  15:0
  Rotate    bone20  0:-3.93  6:32.4  9:14  15:2.22
  Rotate    bone21  0:-1.22  6:-17.8  9:13.7  15:4.83
  Rotate    bone22  0:26  6:-16.6  9:44.6  15:-13.1
  Rotate    bone23  0:8.16  6:-41.8  9:-32.6  15:-13.3
== die_01  1.00 s = 30 khung
  doi anh P_shetou: kh 0 -> None, kh 2 -> P_shetou, kh 25 -> None
  doi anh P_shetou1: kh 0 -> P_shetou1, kh 2 -> None, kh 25 -> P_shetou1
  doi anh P_shetou2: kh 0 -> P_shetou2, kh 2 -> None, kh 21 -> P_shetou2
  doi anh P_yanjing1: kh 0 -> P_yanjing2
  Rotate    bone4   0:17.4  2:36.7  6:47.6  9:61.6  11:46.4  13:6.83  15:-33  17:-30.2  25:-27.6  30:-25.1
  Translate bone4   0:-5.71/122  2:-21.2/161  6:-77.4/145  9:-148/-20.1  11:-120/-26.4  12:-106/-43.8  13:-102/-61.2  17:-79.4/-74.6  25:-24.7/-60.2
  Rotate    bone6   0:18.7  2:-0.467  6:0.082  9:23.9  11:-33.5  13:3.82  15:22.2  17:19.2  25:12.8
  Translate bone6   0:33.4/-12.8  9:33.4/-12.8  10:12.2/-5.2  11:14.4/13.9  13:50.5/10.9  15:64.9/18.7  17:55.8/14.9  25:16.1/-12.1  30:16.6/-7.52
  Rotate    bone5   0:16.4  2:43.4  6:49.8  9:11.9  11:63.3  13:148  15:85.2  25:-5.92  30:3.38
  Rotate    bone20  0:20.2  2:52.2  6:66.2  9:72.8  11:101  15:54.6  25:1.42  30:18.5
  Scale     bone20  0:1.79/1
  Rotate    bone21  0:-30.1  2:-58.8  6:44.9  9:54.5  11:71.2  15:41.2  21:0.382  25:-40.7  30:-65.1
  Scale     bone21  0:1.51/1
  Rotate    bone22  0:-29.4  2:-27.5  6:-35.3  9:-9.19  11:71.3  15:66.2  21:1.89  25:-37.4  30:-32.7
  Scale     bone22  0:1.36/1
  Rotate    bone23  0:-28.2  2:-27.4  6:-24.2  9:-31.2  11:58.4  15:66  21:18.1  25:40.8  30:-19.6
  Scale     bone23  0:1.44/1
  Rotate    bone17  0:-19.8  2:5.83  6:19.6  9:-13.8  11:7.58  13:-8.59  17:-0.622  30:23.4
  Rotate    bone18  0:-50.1  2:-26  6:6.06  9:-29.8  11:6.26  13:12.7  17:-3.07  30:-41.2
  Translate shadow  0:0/0  2:-8.44/0  6:-74.3/0  9:-112/0  11:-78.1/0  13:-68.4/0  15:-41.6/0  25:-37.4/0  30:-35.7/0
  Scale     shadow  0:0.827/0.827  2:0.766/0.766  6:0.74/0.74  9:0.8/0.8  11:0.976/0.976  13:1.03/1.03  15:0.96/0.96  25:1.02/1.02  30:1.1/1.1
  Deform slot P_shetou2 (1 số)
  _DrawOrder slot shadow (1 số)
```

## 4. Thiết kế và mảnh (2026-11-11, người dùng đã duyệt concept cả hai dạng)

- Dạng 1: sò tròn, mai trên lam lục gân quạt, vành và gai cam san hô, mai dưới trắng xà cừ, hai mắt vàng con ngươi dọc trên mai
  trên, nanh kem, u hà, lưỡi hồng nằm trong miệng. Dạng 2: to nặng hơn, mai chàm đậm, vương miện ba gai chóp đỏ, sẹo nứt, nanh
  nhiều và dài, mày dày, chóp lưỡi thè qua mép dưới.
- Cắt thẳng từ concept (`so_gai.py cat`): phân lớp theo màu rồi loang từ hạt giống thành MAI TRÊN / MAI DƯỚI / TRONG MIỆNG;
  nét mực chỉ thuộc một mai khi nằm sát phần màu của chính mai đó; sợi mảnh dưới 9 px trả về trong miệng. Quanh bản lề hai mai
  cùng giữ một đĩa 26 px nên xoay không hở.
- Tờ GPT `M01` (lòng miệng, môi chu, ngọc trai) và `M02` (lưỡi dài gen lại: bản đầu ra như cây xúc xích, người dùng chê).
  Hai mí GPT vẽ không dùng: nhắm mắt = tô che con mắt bằng màu mai gần nhất, giữ nét mày (còn hở 0 px).
- **Lòng miệng** (gắn mai dưới) = mảng tím của concept + vòm tím GPT nối ra sau mai trên. **Vòm trong** (gắn mai trên, vẽ sau
  cùng) = thân trơn tô tím gồm phần trên đường miệng và quạt 75° phía dưới: lúc nghỉ khuất sau thân, há miệng thì lấp khe giữa
  vành trên và lòng miệng (trước khi có nó, vừa hé miệng là nhìn xuyên qua). Khép miệng tương đối thì ẩn nó (kẻo lòi dưới thân).
- **Chóp lưỡi đè mép dưới (dạng 2)** giữ luôn trên mai dưới; lúc lưỡi dài thè ra đổi sang `mai_duoi_k` (đã vá chỗ chóp lưỡi
  bằng inpaint) để không thành hai lưỡi.

## 5. Rig (`so_gai.py all`)

Xương: `root → move → lac (trục con lắc ở cao) → than → mai_duoi (bản lề) [ln0, ln1 lưỡi nghỉ; lu0..7 lưỡi dài; moi → mieng]`
và `than → mai_tren (bản lề)`. Hai mai, lòng miệng, vòm trong, mí, môi là mảnh cứng; lưỡi nghỉ và lưỡi dài là lưới.
Slot sau → trước: vòm trong, lòng miệng, lưỡi nghỉ, mai dưới, lưỡi dài, mai trên, hai mí, môi chu.

| | Dạng 1 | Dạng 2 |
|---|---|---|
| .atomik | 221 KB (có dạng 2 bên trong cho evolve) | 142 KB |
| Góc khép khít (đo trên mặt nạ: khe giữa miệng còn < 15 %) | 20° | 20° |

Clip (dạng 2 chậm 1,1 lần): `appear` 0,8 s (rơi ngậm miệng, bẹp, nảy, đớp hai cái) · `idle` 4 s (lắc lư như lật đật quanh trục
con lắc + nghiêng thân, vòng giữa nhai nhai, chớp mắt) · `attack` 1,07 s, `trung` 0,57 s (há 56° / −35°, lao, sập khít, nén bẹp) ·
`cast` 1,33 s, `phun` 0,63 s (lấy hơi, khép khít, môi chu hiện ra, phồng, nhổ, giật lùi; xương `mieng` ở lỗ môi) ·
`skill` 1,47 s, `trung` 0,37 s, `quat` 0,60 và 0,87 s (há, lưỡi dài phóng ra, lao tới, quật ba phát, thu lưỡi, lùi) ·
`hit` 0,53 s · `die` 1,53 s (hất tung, rơi, mai bật mở, lưỡi thè nằm vật, tan) · `evolve` 2,8 s.
Lưỡi dài: góc gốc A(t) và độ cuộn mỗi đốt C(t), đốt xa đi trễ 0,012 s mỗi đốt (quất như roi), co cả lưỡi 0,22 → 1 khi phóng ra.

Kiểm hở: `lo_kin` đếm vùng trong suốt bị hình bao kín ở mọi khung. Còn lại: khe khoé miệng dạng 2 (khe tự nhiên giữa hai đầu
vành), vòng cuộn của lưỡi trong `skill`; không còn khe nhìn xuyên qua miệng.

Chưa làm: đưa vào game (suất ải 15 đang là `ha_ba`: chờ người dùng quyết id, tên), VFX viên ngọc trai cho `cast`
(ảnh `inbox/so_gai_1/to/ngoc.png`), tia / vệt quật của lưỡi.

## 6. Sửa theo người dùng (2026-11-11 chiều): bên trong miệng và chiêu nhổ ngọc

- **Bỏ "lòng miệng" vòm tím và "vòm trong"** ở mục 4 (người dùng: "cái gì tím tím kia, nhìn lại con gốc đi", "không cần làm thịt ở trong
  miệng", "hàm dưới khi há thấy cả viền trong của hàm đựng lưỡi"). Nay làm như con gốc: bên trong chỉ là **mặt trong của mai dưới**
  = hình thấu kính tím vẽ bằng mã (dây cung từ bản lề tới đầu miệng, vồng lên; đầu phía trước dựng đứng hơn để phủ khoé miệng), có
  **vành cam phía xa** dọc mép trên; gắn xương `long` (con của `mai_duoi`, gốc ở bản lề, trục x dọc dây cung). Mai trên mở như nắp,
  giữa nắp và mai dưới là khoảng trống. Lúc nghỉ vành xa khuất sau mai trên (cao hơn mép miệng ~13 % chiều cao vỏ, nên hé miệng nhỏ
  lúc idle không lộ khe); lúc ngậm thì `long` ép dẹt còn 0,7 để không lòi trên lưng. Mẩu vách ở khoé miệng dưới đầu vành trên mà
  thấu kính không phủ (dạng 1: ~700 px) chuyển sang mai trên.
- Dọn: nét mực vụn rời của hai mai bỏ hẳn; lưỡi nghỉ chỉ lấy khối hồng lớn nhất; sau lưỡi nghỉ luôn có lòng mai.
- **Chiêu nhổ ngọc** (người dùng: "animation bắn ngọc lỗi quá", "tưởng tượng ngậm mồm rồi nhổ ra ngọc"): hé miệng lấy hơi → ngậm khít
  (0,3 s) → nín hơi: phồng, run, ngả ra sau, **môi chu** hiện ở GIỮA đường miệng → `phun` 0,65 s: chồm tới, miệng BẬT MỞ, giật lùi →
  về dáng. Môi chu = tờ `M03` (hai vành cam ép vào nhau, phồng lên ở giữa, có lỗ nhổ), cắt bớt hai đầu dải, co cho dải kép cao
  bằng hai vành của con này; cái "bánh vòng" của M01 bỏ. Xương `mieng` ở lỗ môi. `rig/xem_nho_ngoc.gif`: ảnh động xem thử có ghép
  viên ngọc (ngọc là VFX của game, không nằm trong rig).
- Lưu ý gen: hai lần lệnh Codex cho tờ một mảnh (M02, M03) bị treo ~15 phút không ra ảnh và chặn hàng chờ chung; ngắt tiến trình
  `codex.exe exec` của chính mình rồi chạy lại thì 2 phút là xong (`gen.py ... --timeout 420`).

## 7. Hàm dưới làm lại theo đúng cách con gốc tách (2026-11-11 chiều)

Người dùng: "hàm dưới bạn gen lỗi quá, gen lại đi", "xem hàm dưới con gốc làm như nào làm y hệt". Con gốc có hai mảnh hàm dưới kẹp cái
lưỡi: **mảnh trước** `P_xiaba` (mặt ngoài cái bát, vành gần lượn sóng ở mép trên) và **mảnh sau** `P_xiaba1` (nửa đĩa tối màu, đường
vành xa mảnh ở mép trên), cao gần bằng nhau, mảnh sau nhô cao hơn mảnh trước một chút.

- Gen: `build_so_gai.py` → `gui_gpt/so_gai_<k>/luot_2_ham_duoi.txt` → `tai_ve/H01.png`: vẽ lại concept nhưng chỉ còn mai dưới
  (bỏ mai trên, bỏ lưỡi), giữ nguyên chỗ và cỡ, thấy lòng bát tím trống và vành xa một cung trơn. GPT giữ đúng chỗ: căn mặt bát
  với concept IoU 0,984 (dạng 1), 0,975 (dạng 2) mà không phải dời, co.
- `so_gai.ghep_ham`: mảnh sau `long` = lòng bát + vành xa của H01 (theo cột: từ mép trên vành xa xuống đáy lòng bát + 28 px; nanh
  dưới đứng trước lòng bát thì tô tím; kéo giãn dọc nếu vành xa chưa khuất sau mai trên lúc nghỉ: dạng 1 ×1,06; cắt theo bóng thân
  đã lấp lỗ; bỏ sợi mảnh). Mảnh trước giữ pixel concept; dạng 2 chỗ chóp lưỡi che vành lấy vành liền của H01, chóp lưỡi thành mảnh
  rời `luoi_mep` (slot trước mai dưới, ẩn khi lưỡi dài thè ra) thay cho bản vá inpaint `mai_duoi_k`.
- Lòng bát vẽ bằng mã (mục 6) chỉ còn là phương án dự phòng khi chưa có H01.
- Dung lượng: dạng 1 162 KB (gộp dạng 2), dạng 2 104 KB.

### Sửa tiếp 2026-11-11 (người dùng: "mép này bị hở, lưỡi không nằm chính giữa... tách hàm dưới thành 2 layer để lưỡi nằm giữa hàm", "dạng 2 cũng bị hở")

- **Lưỡi dài nằm GIỮA hai lớp hàm dưới** (slot `luoi_d` ngay trước `mai_duoi`, sau `long`), như con gốc. Cùng cái lưỡi có thêm slot
  `luoi_t` TRƯỚC mai dưới, chỉ dùng khi góc gốc lưỡi A < −6° (lưỡi vắt xuống qua mép: quật xuống, lúc chết); .atomik chưa đổi được
  thứ tự vẽ theo clip nên phải hai slot (con gốc dùng timeline drawOrder).
- **Lớp sau nối dài hai đầu** (±50 cột ngoài lòng bát lấy đúng hình H01): đầu vành xa cong xuống gặp đầu vành gần, hết hở ở mép
  đầu miệng và bản lề.
- Lớp sau không còn bị CẮT theo bóng thân: cột nào cao quá bóng thân lúc nghỉ (khoé miệng, nơi mai trên chỉ còn cái vành) thì ÉP
  cột đó xuống, hệ số làm trơn theo chiều ngang → vành xa lượn liền.
- Mẩu vách ở khoé miệng (vùng miệng lúc nghỉ nằm trên vành xa, dưới đầu vành trên) thành mảnh riêng `khoe`: gắn mai trên, vẽ sau
  mai trên, ẩn khi miệng há quá 4° (lúc đó khoé miệng mở tự nhiên).
- Kiểm dáng nghỉ: vẽ rig ở tỉ lệ concept rồi so bóng: cả hai dạng "concept có mà rig trống" = 0 px, "rig thừa" = 0 px.


## 8. LÀM LẠI TỪ ĐẦU 2026-11-11 chiều (người dùng: "đập đi gen lại từ đầu", "lòi xòm nhiều quá, đọc lại skill ... dịch ngược file spine xem các mảnh của họ")

Bộ cũ (mục 4–7: cắt hai mai ra từ concept theo màu rồi vá bằng mã: lòng bát, vách khoé miệng, mí mắt, nối đầu vành...) bị bỏ hẳn:
mép rách, lòi mẩu vụn ở mọi dáng há. `so_gai.py` giữ lại chỉ để `so_gai2.py` mượn vài hàm (lo_kin, gif_nho, hằng số).

### 8.1 Mổ mảnh con gốc (skill pokiclash-spine-rig mục 00)

Tờ mổ: `D:/Ripper/SwordxStaff/scan/monster_3237/manh_anh.png` (mọi ảnh trong atlas), `manh_dang_goc.png`, `manh_dang_ha.png`
(skill_01 @ 0.35 s), `manh_dang_luoi.png` (skill_02 @ 0.6 s); `att_goc.json`, `att_ha.json`, `att_luoi.json`.

| Thứ tự vẽ | Mảnh con gốc | Là gì | Xương |
|---|---|---|---|
| 1 | P_ci8 | gai sau của hàm dưới | bone6 |
| 2 | **P_xiaba1** 219×102 | **MẶT TRONG của hàm dưới**: mép TRÊN gần thẳng là **vành xa** (dải vành), bụng tối thõng XUỐNG theo dáng bát, khuất sau vách trước. (Bản ghi đầu viết ngược là "vòm tối, dải vành ở dây cung dưới": tờ mổ lúc đó gỡ xoay atlas sai chiều nên mảnh bị lộn 180°, xem 8.5) | bone6 (hàm dưới) |
| 3–5 | P_shetou (+ P_shetou1, P_shetou2 khi lè) | lưỡi; lúc lè qua hàm thì tách hai ảnh: gốc sau hàm, ngọn trước hàm, chỗ nối mờ dần | bone20..24 |
| 6 | **P_xiaba** 222×102 | **mặt trước hàm dưới**: lưỡi liềm kín có vành gần | bone6 |
| 7–13 | P_ci*, ya1, ya2 | gai, nanh: mảnh rời nhưng bám cùng xương với mai, không động riêng | bone5 / bone6 |
| 14 | **P_tou1** 232×116 | **vòm mai trên kín**, vành ở mép dưới; không có mặt trong | bone5 |
| 16 | P_yanjing1 / P_yanjing2 | mắt mở / mắt nhắm: đổi ảnh | bone19 |
| 17–18 | P_meimao1/2 | mày (sừng) | bone17, bone18 |

Điều rút ra: mỗi mảnh là MỘT hình kín vẽ đủ cả phần khuất; há miệng không lộ gì "bên trong mai trên", chỉ thấy vòm tối của hàm
dưới đứng sau lưỡi; không mảnh nào được cắt từ ảnh trọn con.

### 8.2 Mảnh của mình (một – một, GPT vẽ; prompt `build_so_gai2.py`, gói `gui_gpt/so_gai_<k>/luot_2_*.txt`)

| Slot (sau → trước) | Ảnh | Cách gen |
|---|---|---|
| `long` | L01 | vòm tím kín, **đúng chỗ đúng cỡ concept** (giữ mép khoé miệng của concept), cung trên trơn nằm sau mai trên |
| `luoi` | dạng 1: tờ P01 ô D; dạng 2: T01 (đúng chỗ đúng cỡ) | lưỡi nằm vẽ đủ phần khuất |
| `luoi_d` | tờ P01 ô F | lưỡi dài (cả lưỡi), giữa vòm tím và mặt trước mai dưới |
| `mai_duoi` | D01 | mặt trước mai dưới (bát + vành gần + gai + nanh dưới), đúng chỗ đúng cỡ; phía trên vành là nền trắng |
| `luoi_mep` (dạng 2) | T02 | chóp lưỡi vắt qua mép, mảnh riêng vẽ trước mai dưới (bám `ln1`) |
| `luoi_t` | (suy từ ô F) | lớp trước của lưỡi dài: lưỡi chĩa xuống thì cả lưỡi, chĩa ngang / lên thì chỉ khúc đã ra ngoài miệng |
| `mai_tren` | U01 | vòm mai trên kín (vành, gai, u hà, nanh trên), đúng chỗ đúng cỡ, **không mắt** |
| `mat_g`, `mat_x` | tờ P01 ô B (mở), ô C (nhắm) | đổi ảnh như con gốc; cỡ và chỗ theo mắt vàng của concept |
| `moi` | tờ P01 ô E | môi chu có lỗ nhổ ngọc, chỉ hiện ở `cast` |

Gai, nanh vẽ liền vào mai (cùng xương, không động riêng: gộp cho ít mảnh, không hở chân gai).
Mẹo quan trọng: mảnh lớn gen bằng câu **"redraw image 1 with ONLY <bộ phận>, SAME POSITION, SAME SIZE, complete it into ONE CLOSED
SHAPE"** với concept đã duyệt làm ảnh mẫu: GPT trả mảnh trùng concept (lệch 0–1 px), không phải dò tỉ lệ, dáng nghỉ ghép lại giống
concept. Tờ mảnh rời (P01) chỉ dùng cho mảnh nhỏ hoặc mảnh không có trong concept.

`so_gai2.py cat`: tách nền trắng (dải 2 px sát mép lấy màu mực), đặt chỗ, co giãn cả mảnh; KHÔNG vá, KHÔNG cắt theo màu. In số đo:
dáng nghỉ ghép từ mảnh so với concept (dạng 1 thiếu ~1300 px, thừa ~700 px: toàn rìa 1–2 px và mắt; dạng 2 thiếu ~2900 px).

### 8.3 Rig (`so_gai2.py`)

Xương như cũ: root → move → lac → than → {mai_duoi → {long, ln0 → ln1, lu0..7, moi → mieng}, mai_tren → mat}. Hai mai xoay quanh
bản lề. Góc khép đo trên vành cam của hai mảnh (dạng 1: chạm 17,5°, khít 26,5°; dạng 2: 19° và 28,5°). Clip giữ nhịp cũ; đổi:
`cast` ngậm miệng suốt lúc nhổ, môi chu dẩu ra rồi nhổ qua lỗ môi, sau đó mới hé về dáng nghỉ; `skill` lưỡi chỉ vung trong khoảng
miệng mở (lên tối đa ~54°), không vắt ra sau lưng mai trên; lưỡi dài dày thêm 30 %.

Kết quả: dạng 2 `.atomik` 105 KB, dạng 1 (gộp dạng 2 cho evolve) 165 KB. Soi 16 khung chính mỗi dạng (nghỉ, nhai, há to, đớp,
chu môi, lưỡi lên / xuống, trúng đòn, chết): mảnh nào cũng kín, không mẩu vụn, không hở khoé miệng.


### 8.4 BỎ MẢNG TÍM: lớp sau lưỡi là nửa sau của hàm dưới (2026-11-11, người dùng nhắc lần ba)

Người dùng xem bản 8.2 (lớp sau lưỡi là vòm tím L01): "tôi đã bảo con này không có thịt trong rồi sao bạn cứ gen cái mảng tím nhỉ,
đây là 2 hàm trên dưới của con sò, xóa mảng tím"; rồi: "gen hàm dưới phải nhìn thấy cả phần trong nữa, phần lưỡi là đặt lên, tức
là gen hàm dưới như con gốc, rồi đặt cái lưỡi ở đúng vị trí giữa hàm". Ảnh người dùng gửi (con gốc há miệng): hàm dưới là cái
bát thấy cả mặt trong tối và vành xa, lưỡi nằm giữa gần lấp đầy lòng bát; không có khối gì đứng sau lưỡi.

Sửa: slot `long` dùng **B01 = nửa sau của hàm dưới** (`gui_gpt/so_gai_<k>/luot_2_ham_duoi_sau.txt`): mặt trong vỏ màu tối CÙNG
TÔNG VỎ (dạng 1 lam lục sẫm #0F3A42, dạng 2 chàm sẫm #141D40, không tím), mép trên và mép trước là **vành xa màu cam**; mép trên
chạy ngay sau vành trên của concept (cao hơn 12 px) nên lúc nghỉ khuất hết sau mai trên và không hở khoé miệng; đáy khuất sau
vành gần. Thấp: chỉ vừa bằng khe miệng lúc nghỉ, không phải vòm. L01 (vòm tím) và ô A của tờ P01 không dùng nữa.
Lượt gen đầu (B01.png) vành xa thấp hơn vành trên → hở một khe ở đầu miệng lúc nghỉ; bản dùng là B01_2.png.

Kết quả: há miệng thấy hàm trên (mặt ngoài) và hàm dưới là cái bát có vành quanh miệng, lưỡi nằm giữa hai vách; lúc nghỉ trong
miệng là màu tối của vỏ, khoé miệng có vành cam nối kín. Dạng 2 108 KB, dạng 1 (gộp) 163 KB.
Bài học lưu ở memory `trong-mieng-khong-co-thit`: làm lại mảnh thì soát lại mọi lời dặn cũ của người dùng trước khi viết prompt.


### 8.5 ĐỌC NGƯỢC MẢNH HÀM DƯỚI CỦA CON GỐC (2026-11-11, người dùng: "nó phải vòng vào trong chứ tự nhiên lại chếch chéo lên trên... bạn đục ngược file spine xem họ tách những cái gì đã cho tôi xem nào")

Gốc của cả chuỗi lỗi "vòm tím", "vành xa chếch lên": tờ mổ dựng lúc đầu (`to_manh.py`) gỡ xoay vùng atlas `rotate: 90` sai chiều,
nên `P_xiaba1` hiện LỘN NGƯỢC: tôi đọc nó là "vòm tối cao, dải vành ở đáy" và dựng lớp sau lưỡi thành một vòm đứng sau lưỡi. Công
cụ đã được sửa (phiên khác, cùng ngày); dựng lại tờ mổ thì khớp với khung thật của runtime (`scan/monster_3237/khung/skill_01.jpg`):

- `P_xiaba1` = **mặt trong cái bát**: mép trên là vành xa, gần thẳng, nối hai đầu nhọn vểnh lên của vách trước; bụng tối thõng xuống,
  khuất sau vách trước. Miệng bát = hình hạt hạnh khép kín giữa vành xa (trên) và vành gần võng xuống (dưới).
- Lưỡi to, nằm trong hình hạt hạnh đó, gần lấp đầy; phần tối chỉ còn lộ một dải mỏng giữa lưỡi và vành xa.
- Há miệng: mai trên lật lên, KHÔNG có gì đứng sau lưỡi ngoài cái vành xa thấp ấy.

Tờ cho người dùng xem: `D:/Ripper/SwordxStaff/scan/monster_3237/to_mo_ham_duoi.png` (cả con + 3 mảnh hàm dưới), `manh_anh.png`.

Bài học: tờ mổ phải SO với khung thật của runtime (`chay.py sheet`) trước khi tin; mảnh đối xứng hoặc gần tròn lộn 180° vẫn "trông
hợp lý". Prompt B01 viết lại theo hình đúng (`build_so_gai2.py` `build_back2`): vành xa chạy sau mép dưới của vành trên rồi VÒNG
XUỐNG gặp đầu vành gần ở phía trước; bụng bát khuất sau vách trước. Bản dùng: B01_3.png.

Kết quả 8.5 (cùng ngày): mặt trong hàm dưới dùng `B01_4.png` (dạng 1; bản `_3` vành xa vòng xuống sớm quá, lúc nghỉ hở một khe
dưới nanh trên) và `B01_3.png` (dạng 2). `so_gai2.py cat` với B01: co giãn NGANG cả mảnh cho hai đầu vành xa trùng hai đầu vành
gần; phần bụng tràn ra ngoài bóng vách trước (dưới vành gần, vốn khuất) thì bỏ, mép bỏ nằm dưới viền mực của vách trước; đo khe
nhìn xuyên giữa vành trên và vành xa lúc nghỉ rồi hạ mai trên góc nhỏ nhất đủ hết khe (`nghi_tren` trong manh2.json: dạng 1 là
0°, dạng 2 là −4°; clip tính góc so với dáng nghỉ này). Soi 8 khung chính mỗi dạng: miệng bát là hình hạt hạnh khép kín, lưỡi nằm
giữa, không còn vòm hay mảng nào sau lưỡi. Dạng 2 105 KB, dạng 1 (gộp) 159 KB.


### 8.6 HÀM DƯỚI MỘT ẢNH (J01): hết lệch chỗ nối hai vành (2026-11-11, người dùng: "dạng to ở mép nối đầu miệng không match bị lệch, dạng 1 thì lệch hẳn luôn còn không khớp nhau")

Bản 8.5 dùng hai ảnh GPT rời cho hàm dưới (D01 vách trước + B01 mặt trong): hai lượt vẽ riêng thì đầu vành xa không bao giờ trùng
đầu vành gần, co giãn bằng mã cũng chỉ khớp được vị trí, không khớp được nét. Sửa tận gốc:

- **J01** (`gui_gpt/so_gai_<k>/luot_2_ham_duoi.txt`): GPT vẽ lại concept chỉ còn **cả hàm dưới trong MỘT ảnh**, đúng chỗ đúng cỡ:
  bát + vành gần + nanh, gai + lòng bát tối cùng tông vỏ + vành xa; vành là MỘT vòng liền quanh miệng bát hình hạt hạnh. Vành xa
  chạy ngay sau mép dưới của vành trên tới gần đầu miệng rồi mới vòng chữ U xuống thành vành gần (ghi bằng số px trong `--note`
  thì GPT mới vẽ đủ cao; bản đầu của cả hai dạng vành xa thấp, lúc nghỉ hở khe dưới nanh trên). Bản dùng: dạng 1 `J01_2.png`,
  dạng 2 `J01.png` (lượt gen lại ghi đè).
- `so_gai2.py cat`: slot `long` (sau lưỡi) = CẢ ảnh J01; slot `mai_duoi` (trước lưỡi) = phần của CHÍNH ảnh J01 nằm dưới lòng bát
  (mỗi cột: từ điểm tối thấp nhất của lòng bát trở xuống, tức từ viền mực mép trên vành gần, kèm nanh; ngoài hai đầu lòng bát
  lấy cả cột). Hai lớp cùng nét vẽ, cùng xương nên đường tách không bao giờ lộ; nó chỉ quyết định lưỡi bị che từ đâu.
  D01, B01, L01 không dùng nữa.
- Dáng nghỉ: cả hai dạng giữ đúng dáng concept (`nghi_tren` = 0°), không có khe nhìn xuyên.

Kết quả: dạng 2 123 KB, dạng 1 (gộp) 184 KB (atlas chứa hàm dưới hai lần: cả ảnh và vách trước).


### 8.7 Lưỡi chiêu cuối dày, mềm hơn; chiêu nhổ ngọc bỏ môi chu (2026-11-11, người dùng: "ổn hơn rất nhiều, ... phần lưỡi khi đánh chiêu cuối cho dày hơn nữa ... rig thêm xương ... cho mềm mại hơn; chiêu bắn ngọc bỏ cái hình gen thêm ở giữa đi nhìn lệch quá, thay vào đó làm con sò phồng lên rồi phụt ra viên ngọc")

- Lưỡi dài: bề dày ×1,9 so với tỉ lệ theo bề dài (trước ×1,3); **16 xương** (trước 8), lưới 49 cột × 9 hàng; góc cuộn chia đều theo
  thang 8 đốt chuẩn nên khoá cũ dùng lại được; khúc xa trễ hơn (0,017 s mỗi đốt chuẩn) và có gợn sóng nhỏ chạy từ gốc ra ngọn.
- `cast`: bỏ hẳn slot / ảnh / xương `moi` (ô E của tờ P01 không dùng nữa). Nhịp: hít hơi hé miệng → ngậm chặt → PHỒNG to dần tới
  ×1,24 ngang, ×1,2 dọc, run, ngả ra sau, mắt nhắm → khung 19,6: bật miệng (mai trên +20°), người xẹp và chúi tới, sự kiện `phun`
  → giật lùi → về. Xương `mieng` (chỗ VFX viên ngọc bám) nằm giữa khe miệng phía đầu miệng, con của `mai_duoi`.
- Dung lượng: dạng 2 156 KB, dạng 1 (gộp) 248 KB (nhiều khoá và đỉnh lưỡi hơn).


### 8.8 Bỏ mảnh chóp lưỡi vắt mép của dạng 2 (2026-11-11, người dùng: "thừa mảnh lưỡi ở giữa kìa")

Mảnh T02 (chóp lưỡi nửa tròn vẽ trước vành gần) nhìn như một mẩu lưỡi rời dính trên vành. Bỏ: `DUNG_CHOP_LUOI = False` trong
`so_gai2.py`, không còn slot `luoi_mep`. Lưỡi nằm của dạng 2 (T01) nằm trọn giữa hai vách hàm dưới như dạng 1; chóp rủ của nó
khuất sau vách trước.


### 8.9 Lưỡi chiêu cuối: cuống sâu, thon dần, dài và mềm hơn (2026-11-11, người dùng: "đặt cuống lưỡi sâu hơn nữa, phần gần cuống thì dày hơn, xuống đầu lưỡi nhỏ hơn, làm dài hơn và mềm mại hơn")

- Cuống: `F_GOC` 0,45 → 0,17 bề dài miệng tính từ bản lề, hạ xuống dưới mép vành giữa (trong lòng bát).
- Thon: `thon()` bóp bề dày từng cột của ảnh lưỡi quanh đường giữa của nó, ×1,0 ở cuống → ×0,52 ở đầu lưỡi (co giãn trơn cả mảnh),
  rồi nhân `DAY_LUOI` 1,9. Dài: `DAI_LUOI` 1,2 → 1,62 bề ngang thân. Xương: 16 → 22, lưới 45 cột × 9 hàng.
- Đường đi (vì cuống sâu): khúc trong miệng (thang 0..7: u < 3,1) đi thẳng theo góc gốc, chạy trong lòng bát, sau vành gần và nanh;
  góc gốc thấp nhất +9° để lưỡi vượt ngay TRÊN đầu vành phía trước (thấp hơn thì trông như chui qua vách bát); toàn bộ độ cuộn dồn
  vào khúc ngoài miệng, nên cú quật xuống là khúc ngoài cong xuống. Lớp trước (`luoi_t`) chỉ vẽ khúc ngoài miệng và tắt khi lưỡi
  đang thè ra / thu vào (co < 0,82).
- Dung lượng: dạng 2 158 KB, dạng 1 (gộp) 249 KB.


### 8.10 Dãi (2026-11-11, người dùng: "cho nó chảy dãi, chiêu cuối cũng bắn dãi lung tung")

- Ảnh: tờ `S01.png` (`gui_gpt/so_gai_1/luot_2_dai.txt`, dùng chung hai dạng): sợi dãi dài, sợi dãi ngắn, ba giọt (to, vừa, nhỏ); màu
  nước nhạt #BFE8E6 tô phẳng, viền mực. Vào rig thu rất nhỏ nên `cat` làm đậm nét mực trước (lọc min cả mảnh).
- Lúc nghỉ: slot `dai` (sợi ngắn) bám giữa dải vành gần phía đầu miệng (xương `dai`, con của `mai_duoi`), vẽ trước vách trước;
  kéo dài bằng tỉ lệ dọc theo vòng 120 khung (rủ dài dần → đứt → co lại), luôn rủ thẳng (bù góc xoay của lac + than + mai_duoi) và
  đung đưa trễ; giọt `giot_n` đứt ra, rơi, chạm đất thì bẹp rồi tan. Dáng gốc của sợi dãi = trạng thái khung 0 idle. Clip khác:
  sợi dãi co mất ở 3 khung đầu, hiện lại ở 4 khung cuối.
- Chiêu cuối: 16 slot giọt `gd*` (con của `move` để theo cú lao), phát ở đầu lưỡi theo từng cú vung / quật (17 đợt, 51 giọt, slot dùng
  lại); vận tốc lấy từ chuyển động đầu lưỡi, toả ±65°, rơi theo trọng lực, sống 0,4 s. Đây là hạt nướng sẵn trong rig (thuộc về con
  vật, không phải đạn / tia của chiêu).
- Dung lượng: dạng 2 172 KB, dạng 1 (gộp) 264 KB.


## 9. VÀO GAME (2026-11-11 tối, người dùng: "chốt, cho vào game đi")

- Suất: ải 15 đảo Thủy, id game **`ha_ba`** (giữ id như các suất đã đổi dòng khác: `thach_giai` = ếch xanh, `giong_bao` = pháp sư nước).
- Chép tay (không chạy `vao_game.py` trần, kẻo chép cả dòng của phiên khác):
  `inbox/so_gai_<k>/rig/so_gai_<k>.atomik` → `Assets/03 Art/Heroes/Resources/ha_ba_<k>/ha_ba_<k>.atomik`, `chan_dung.png` →
  `ha_ba_<k>_portrait.png` (512). `quai/da_nhan.json`: dòng `ha_ba` trỏ sang `inbox/so_gai_<k>/rig` (rig tm04 hà mã thôi dùng).
  `vao_game.py --kiem`: đủ clip, khối game có; cảnh báo cũ "game.shadow không có slot" như mọi rig thư viện quai.
- Mã trận: `HatNuoc.cs` thêm chiêu **`n_ngoc`** (`NNgoc`: viên ngọc rời miệng đúng khung nhả của clip cast, bay 0,2 s, kéo giọt
  dãi, chạm thì toé nước; ngọc vẽ lớp chồng viền mực + thân xà cừ + vệt tím, không điểm sáng) + `PlayNuoc` / `HoldNuoc`;
  `StageView.cs` bảng `WaterFx`: `ha_ba` = (`n_ngoc`, [`n_va`, `n_va`]). Biên dịch thử ngoài Unity (csc + rsp của Bee): không lỗi.
- Khối game của rig: cast đứng yên (`stay`), nhả ở 0,653 s (sự kiện `phun`, xương `mieng`); skill lao (`lunge`, cú lao trên xương
  `move`), trúng ở 0,367 s + hai sự kiện `quat`; attack trúng ở 0,567 s.
- CHƯA làm (chờ người dùng): tên tướng, tên hai dạng, tên và lời ba thẻ (đang là "Hà Bá / Hà mã nuốt sóng", "Hà Mã Con; Hà Bá",
  "Súng Nước / Ngáp Sóng / Hồn Nước"); đổi thì sửa `heroes.json`, `cards.json`, Nhập dữ liệu, tính lại golden roster / cardtext.
  Chưa xem trong Unity (phiên này không có cầu MCP): cần Refresh, menu "PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng",
  rồi vào trận ải 15.

Bổ sung cùng tối (người dùng: "tự chạy menu đi, thay thế tướng cũ luôn"):
- Tên (Claude đặt tạm, id nội bộ giữ `ha_ba`): tướng và dạng 2 **Sò Ngoạm**, dạng 1 **Sò Háu**, danh hiệu "Sò đột biến lưỡi dài", "Dòng Sò
  Ngoạm"; thẻ chiêu mana **Phụt Ngọc**, chiêu cuối **Lưỡi Quật**, bị động giữ "Hồn Nước". Sửa `heroes.json`, `cards.json`,
  `quai/tuong_moi_thuy.py`, `VAO_GAME.md`. Chỉ số, hiệu ứng thẻ, golden không đổi.
- Unity (cầu MCP không bật): thả script editor tạm `Assets/01 Script/Editor/ClaudeTam/ChayLenh.cs` (đọc `Temp/claude_lenh.txt`, mỗi dòng
  một menu, dòng TEST = test EditMode, ghi `Temp/claude_lenh.log`), đổi cửa sổ qua lại (AppActivate) cho Unity nạp; xong thì xoá thư mục.
  Đã chạy: "PokiClash/Nhập dữ liệu" (HeroDb, CardDb có tên mới), "PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng" (`ha_ba_1|2.asset`
  cập nhật `source`), test EditMode **102 đạt, 1 trượt** (`PrefabOnlyTests.MaRuntime_KhongSinhDoVat`, trượt từ trước, không do thay đổi
  này), "PokiClash/Tướng/Chụp thử dạng .atomik (mọi clip)": `Library/PokiHeroShots/ha_ba_atomik_1|2.png` (đường AolaActor của game):
  idle có dãi, hit, attack, cast phồng rồi phụt, skill lưỡi + giọt dãi, evolve sang dạng 2 đều đúng.
- Chưa xem trong trận thật (viên ngọc `n_ngoc`, cú lao của chiêu cuối).
