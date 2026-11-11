# Dòng Tí Tách: làm lại theo ý người dùng (2026-11-11)

Thay bản `tm01` của lô cũ (giọt nước có tay chân, băng đô; ghi chú cũ `tm01_ghichu.md`). Người dùng lên ý tưởng và duyệt từng bước.
Gói prompt: `ArtGen/Spine/build_ti_tach.py` → `gui_gpt/ti_tach_<k>/`, ảnh về `inbox/ti_tach_<k>/tai_ve/`.

## 1. Ý người dùng (nguyên văn tóm lại)

- Hình giọt nước dáng vòm và kiểu mắt như con gốc `monster_3203` (game tham khảo). Đây là dạng 1.
- `idle`, `die`, `appear`: làm giống của con gốc.
- Đánh thường: **húc đầu** vào đối thủ. Chỉ làm animation húc; lao tới đối thủ do code.
- Chiêu (bắn nước): vẽ thêm **miệng há**; người hơi co lại và cao lên để bắn tia nước, **bắn xong mới ngậm miệng**.
- Chiêu cuối: **phình to** rồi **nhảy lên đầu đối thủ**; rơi xuống thì bẹp, có độ nặng. Quỹ đạo nhảy do code. Làm 2 clip:
  nhún bật nhảy lên, và tiếp đất nối từ cú nhảy đó.
- Mổ xẻ kỹ cách họ rig xương và biểu cảm mặt (vài clip mắt nhắm là một ảnh khác).
- Dạng 2: y như vậy, giọt to hơn, có thể thêm nhiều giọt nhỏ trên đầu hơn.

## 2. Mổ xẻ con gốc `monster_3203` (chỉ học cấu trúc và nhịp, không lấy hình)

Nguồn: `D:\Ripper\SwordxStaff\web\assets\Monster\monster_3203\` (Spine 4.2.28, 0,1 MB). Kết quả quét:
`D:\Ripper\SwordxStaff\scan\monster_3203\` (`info.json`, `keys.json`, `mesh.json`, `sample.json`, tờ khung `khung/<clip>.jpg`).
Quét lại: `py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/mo_xe/chay.py info|keys|mesh|sample|sheet ...`.

### Ảnh (atlas 316 × 148, xuất tỉ lệ 0,75; chỉ 6 vùng)

| Vùng | Cỡ | Là gì |
|---|---|---|
| `F_SS_shenti1` | 170 × 126 | thân vòm, **không có mặt** (mặt là lớp riêng) |
| `F_SS_shenti2` | 50 × 50 | **một ảnh** chứa cả cụm 3 giọt nhỏ |
| `P_SS_bq04` | 108 × 54 | mặt mặc định: hai mắt bầu dục trắng + vệt má |
| `P_SS_bq01` | 108 × 44 | mặt nhăn `> <` (trúng đòn, lúc húc trúng, chết, bị hất) |
| `P_SS_bq02` | 108 × 44 | mắt cười `^ ^` (clip chạy nhảy `run_02`) |
| `P_SS_bq03` | 105 × 55 | mắt xoáy (choáng `stun_01`) |

Biểu cảm = **đổi nguyên ảnh mặt trên một slot** (timeline attachment), không có mí, không có miệng.

### Xương (10) và slot (4)

```
root
├─ bone (y −50)
│   └─ bone8 (trục lộn nhào cả con, đặt gần đỉnh thân; chỉ dùng khi bị hất / rơi)
│       └─ bone2 (ở mặt đất, giữa đáy: NÉN GIÃN + nghiêng + dời cả con)
│           └─ bone3 (tâm thân, cao 74: khối trên lắc, phình, dời)
│               ├─ bone7  (mặt: chỉ dời, đôi khi co dọc)
│               └─ bone4 → bone5 → bone6 (cần 3 đốt đỡ cụm giọt; bone6 mang ảnh cụm giọt và tự quay)
└─ shadow (bóng: dời x theo thân, co theo độ cao)
```
Slot sau → trước: `shadow` (trống), thân, mặt, cụm giọt.

### Lưới và trọng số

- Thân: 17 đỉnh (16 đỉnh viền + 1 đỉnh tâm), 16 tam giác hình quạt. Chỉ bám **2 xương**: `bone2` (đáy) và `bone3` (tâm trên).
  Trọng số chia **theo chiều cao**: đáy 0,9 `bone2`; hai bên hông 0,5 / 0,5; vai 0,3 / 0,7; đỉnh 1,0 `bone3`.
  Nhờ vậy dời hay phình `bone3` thì nửa trên lắc như thạch còn đáy bám đất.
- Cụm giọt: 4 đỉnh bám cứng `bone6`. Mặt: ảnh chữ nhật trên `bone7`.
- Không IK, không physics, không sự kiện, không deform.

### Mẹo diễn chính

1. **Giả 3D bằng trượt mặt**: mặt là lớp dán, `bone7` dời ngang tới −36 px (16 % bề rộng thân) rồi về, trong lúc `bone3` dời
   ngược chiều: trông như con vật quay đầu. Lúc bị đánh mặt trượt hẳn ra mép (−116 px) rồi bật về.
2. **Nén giãn giữ thể tích** trên `bone2` (x × y ≈ 1), gốc ở đất nên đáy không rời đất.
3. **Hai tầng lệch pha**: `bone2` nén giãn chậm, `bone3` nẩy nhanh hơn và trễ → cảm giác thạch.
4. Cụm giọt: cần 3 đốt vung trễ sau thân (lấy đà thì ngả ngược, ra đòn thì quất theo), `bone6` quay tròn liên tục.
5. Hầu hết khoá là đường thẳng; clip lặp chậm (`idle`, `stun`) dùng bezier.

### Clip (11)

| Clip | Dài | Diễn | Mình dùng cho |
|---|---|---|---|
| `idle_01` | 1,33 s | nén giãn (0,91; 1,06) ↔ (1,07; 0,89), có cú nấc nhanh ở khung 2–5 (khối trên thụt 10 px rồi trồi 17 px), mặt trượt trái rồi về, cụm giọt quay 2 vòng | `idle` |
| `die_01` | 1,0 s | mặt `> <` cả clip; khung 0 bị hất lệch (−97 px), khung 3 dựng cao (0,80; 1,31), khung 7 bẹp (1,55; 0,63), khung 10 về dáng, rồi 20 khung **chảy xẹp dần** thành vũng (khối trên tụt 99 px, bè ngang 1,62), giọt rơi xuống | `die` |
| `skill_01` | 1,0 s | **húc**: khung 0–9 ngả ra sau, vươn cao (0,51; 1,74); khung 10 quật tới trong 1 khung, bẹp dài (+105 px, 1,30; 0,67), giữ tới khung 14; khung 9–17 mặt `> <`; khung 17 bật ngược lên; khung 20–30 nảy tắt dần | `attack` |
| `skill_02` | 1,0 s | **nhảy**: khung 6 nén (1,08; 0,68), khung 13 vươn (0,44; 1,78), khung 14–17 bay lên (+327 px), khung 21 chạm đất, khung 23 bẹp (1,11; 0,64), khung 25 nảy, khung 30 về | `skill` (nhún bật) + `skill_land` (tiếp đất) |
| `hit_01` | 0,5 s | khung 0 đã ở dáng méo nhất (ép dẹt 0,37; 1,70, nghiêng 35°), mặt `> <` tới khung 9 rồi mở mắt, nảy về | `hit` |
| `hit_02` | 0,67 s | bị hất lên, lộn 360° trên không rồi rơi, khung 11 bẹp (1,55; 0,63), nảy | gợi ý cho `appear` |
| `floating_01` | 1,5 s | bị hất tung, lộn, rơi nảy hai lần, mặt `> <` tới khung 35 | (không dùng) |
| `block_01` | 0,5 s | co lại đỡ đòn | (không dùng) |
| `run_01`, `run_02` | 0,6 s | nhảy lóc cóc; `run_02` mắt `^ ^` | (không dùng) |
| `stun_01` | 1,67 s | lắc lư, mắt xoáy | (để dành: trạng thái choáng) |

**Con gốc không có clip `appear`.** Cần người dùng chọn: rơi từ trên xuống rồi bẹp nảy (nửa sau `hit_02`), hoặc chỉ ra clip khác.

## 3. Thiết kế của mình

- Dáng: vòm nước mập đáy bằng, rộng ~1,4 lần cao, không tay chân. Nét dự án: viền bút mực nâu `#2B2118`, tô chì sáp **phẳng**
  (không bóng loáng, không điểm sáng như con gốc), vài đốm bong bóng lam nhạt làm hoạ tiết.
- Màu: thân `#35BFE6`, đốm `#9FE3F5`, lòng mắt `#EAF8FC`, viền mắt `#1B4F8F`, vệt má `#2A8FD0`.
- Mắt: hai bầu dục đứng trống trơn viền lam dày (theo ý người dùng). Lúc nghỉ không có miệng.
- Dạng 1: 2 giọt con bay trên đầu. Dạng 2: vòm to nặng hơn, mắt nhỏ hơn so với thân, 5 giọt con xếp vòng cung.

## 4. Dự kiến rig (làm sau khi concept được duyệt)

- Ảnh cần thêm (lượt 2): **thân trơn không mặt**; tờ nét mặt cùng cỡ: mắt mở, `> <`, mắt xoáy, mắt nhắm lúc lấy hơi, và
  **miệng há** (tròn nhỏ → há to) cho chiêu bắn; từng giọt con rời.
- Xương: `root → move (code dời) → day (đất: nén giãn) → than (khối trên) → mat (trượt mặt), mieng (chỗ và hướng nhả), cần giọt 3 đốt
  → từng giọt`. Thân là lưới dày, trọng số theo chiều cao như con gốc nhưng 3–4 tầng để lắc mượt hơn.
- Clip: `appear, idle, attack (húc), cast (há miệng bắn), skill (phình + nhún bật), skill_land (tiếp đất), hit, die, evolve`.
  Sự kiện: `trung` (attack), `phun` / `het_phun` (cast), `bat` (rời đất), `cham_dat` (tiếp đất).
- Việc phía game: hiện trận chỉ có một clip `skill`; chiêu nhảy hai clip cần code nối (bay theo cung tới đầu đối thủ giữa hai clip).

## 5. Khoá gốc của các clip sẽ học (khung 30 fps; `x/y` là dời hoặc tỉ lệ)

```
== idle_01  1.33 s = 40 khung
  Scale     bone2       0:1/1  5:0.963/1.02  8:0.926/1.05  10:0.913/1.06  16:1.07/0.894  21:0.966/1.04  25:1/1  35:0.913/1.06  40:1/1
  Rotate    bone4       0:32.6  10:6.32  16:-8.89  21:35  25:32.6  35:6.32  40:32.6
  Rotate    bone5       0:17.7  10:14.1  16:-23.6  21:-30.9  25:17.7  35:14.1  40:17.7
  Translate bone3       0:0/0  2:0/-10.4  5:0/16.7  8:0/0  16:22.3/0  35:-5.13/0  40:0/0
  Scale     bone3       0:1/1  2:1/1.13  5:1/0.859  8:1/1
  Translate bone7(mat)  0:0/0  6:-35.9/0  23:-26.4/7.78  35:-2.88/0  40:0/0
  Rotate    bone6       0:0  40:706
  Translate shadow      0:0/0  8:-1.63/0  16:12/0  21:12/0  25:8.22/0  35:-4.16/0  40:0/0
  Scale     shadow      0:1/1  8:0.902/0.902  16:0.976/0.976  21:0.94/0.94  25:0.907/0.907  35:0.874/0.874  40:1/1
== die_01  1.00 s = 30 khung
  doi anh mat: khung 0 -> bq01
  Rotate    bone2       0:16.3  3:-2.56  7:-8  10:0.848  30:2.34
  Translate bone2       0:-97.3/17.3  3:0/-3.31  7:0/-8.58  10:0/0
  Scale     bone2       0:0.969/1.01  3:0.799/1.31  7:1.55/0.625  10:1/1  30:1/1.11
  Rotate    bone4       0:-58.7  3:-114  10:32.6  30:-9.57
  Translate bone4       10:0/0  30:-0.813/-32.2
  Rotate    bone5       0:-59.4  3:0.592  10:17.7  30:-6.22
  Rotate    bone3       0:-3.72  3:23.3  10:0
  Translate bone3       0:33.8/-53.3  3:-4.07/45.8  10:0/0  30:-4.06/-99.2
  Scale     bone3       0:1.46/1.36  3:1/1  10:1/1  30:1.62/1
  Rotate    bone6       0:-77.7  3:-60.8  10:0  30:-413
  Translate bone7(mat)  0:-82.2/0  3:0/0  10:0/0  30:0.976/38.7
  Translate shadow      0:-92.5/0  3:-6.8/0  7:-0.756/0  10:0.756/0
  Scale     shadow      0:1.28/1.28  3:0.813/0.813  7:1.51/1.51  10:0.967/0.967  30:1.35/1.35
== skill_01  1.00 s = 30 khung
  doi anh mat: khung 9 -> bq01, khung 17 -> bq04
  Rotate    bone2       0:0  9:-0.326  10:1.5  14:1.5  17:7.22  20:0
  Translate bone2       9:0/0  10:36.5/-4.88  14:36.5/-4.88  15:33.4/2.5  17:27.2/60.9  20:-19.4/0  22:-19.4/0  25:-5.66/24.3  28:0/0
  Scale     bone2       0:1/1  9:0.513/1.74  10:1.3/0.666  14:1.3/0.666  15:0.787/1.61  17:0.82/0.926  20:0.806/1.21  22:1.08/0.677  25:0.896/1  28:1.1/0.92  30:1/1
  Rotate    bone4       0:32.6  9:-3.51  10:33.6  12:-59.9  14:-89.6  17:-88.3  20:1.46  22:47.1  25:62.3  30:32.6
  Rotate    bone5       0:17.7  9:3.81  10:25.8  14:-28.1  17:-36.1  20:-30.3  22:22.8  30:17.7
  Rotate    bone3       0:0  3:1.69  9:5.43  10:-23.5  14:-23.5  17:-3.3  20:0
  Translate bone3       0:0/0  3:-74.3/29  9:-54.3/-35.1  10:105/-25  12:44.9/-21.9  14:41.8/-21.7  17:-25.6/43.8  20:0/0
  Scale     bone3       0:1/1  3:1.45/0.88  9:1.41/0.731  10:1.35/1  14:1/1.18  30:1/1
  Rotate    bone6       0:0  9:-1.36  10:21.6  14:21.6  17:-2.48  20:0
  Translate shadow      0:0/0  3:-18.1/0  9:-8.25/0  10:89.1/0  14:57.8/0  15:33.8/0  17:9.07/0  20:-14.8/0  22:-20.6/0  25:6.6/0  30:0/0
  Scale     shadow      0:0.985/0.985  3:0.926/0.926  9:0.789/0.926  10:1.52/1.5  14:1.44/1.42  15:0.877/1.37  17:0.572/0.897  20:0.94/1.47  22:1.17/1.83  25:0.842/1.32  28:1.11/1.31  30:0.985/0.985
== skill_02  1.00 s = 30 khung
  Translate bone2       0:0/0  6:7/0  9:-5.66/24.3  12:0/0  13:1.44/13.2  14:2.87/175  17:-19.4/327  20:-5.66/142  21:0/0  23:0/0  25:0/21.9  27:0/0
  Scale     bone2       0:1/1  6:1.08/0.677  9:0.896/1  12:1.1/0.92  13:0.442/1.78  14:0.806/1.21  17:1.18/0.711  20:0.659/1.35  21:0.554/1.18  23:1.11/0.637  25:0.903/1.11  27:1.05/0.884  30:1/1
  Rotate    bone4       0:32.6  6:-9.88  9:62.3  13:113  14:61.7  17:47.1  20:-20.8  25:56.3  30:32.6
  Rotate    bone5       0:17.7  6:-6.68  14:42.9  17:22.8  20:-8.06  25:17.7
  Translate bone3       0:0/0  12:0/-25.1  14:0/0
  Scale     bone3       0:1/1  12:1.07/0.951  14:0.86/1.18  25:1/1
  Rotate    bone6       14:0  25:30.6  30:0
  Translate shadow      0:0/0  6:7.28/0  9:-8.25/0  14:4.95/0  17:-1.57/0  20:6.6/0  25:0/0
  Scale     shadow      0:0.985/0.985  6:1.17/1.83  9:0.842/1.32  12:1.11/1.31  13:0.679/0.922  14:0.401/0.628  17:0.457/0.716  20:0.561/0.88  21:0.623/0.735  23:1.18/1.26  25:0.898/0.898  27:1.05/1.05  30:0.985/0.985
== hit_01  0.50 s = 15 khung
  doi anh mat: khung 0 -> bq01, khung 9 -> bq04
  Rotate    bone2       0:35.2  2:3.9  4:12.7  7:-0.63  9:-6.39  11:-2.6  15:0
  Translate bone2       0:41.4/0  2:-53.1/0  4:-21.6/1.5  7:-15.2/-1.92  9:0/16.1  11:0/1.79  15:0/0
  Scale     bone2       0:0.366/1.7  2:0.403/0.566  4:0.304/1.12  7:1.04/0.739  9:1/1  11:0.955/1.08  15:1/1
  Rotate    bone4       0:-138  2:2  4:59.8  7:58.9  9:65.4  11:12.6  13:38.1  15:32.6
  Rotate    bone5       0:-43.1  2:-53  4:-58.7  7:30.4  9:29.5  11:37.6  13:-27.6  15:17.7
  Rotate    bone3       0:0  2:17.2  4:3.46  7:-12.1  9:0
  Translate bone3       0:0/0  2:-65/152  4:-23.6/57.4  9:0/0  12:-0.491/13.2  15:0/0
  Scale     bone3       0:1/1  2:2.86/1.83  4:3/1.39  7:1.46/1.53  12:0.969/1.22
  Rotate    bone6       0:-33.7  2:-68.3  4:-61.8  7:-41.4  9:21  11:18.5  13:-28.8  15:0
  Translate bone7(mat)  0:-116/0  2:-74.5/-37.4  9:23.6/0  15:0/0
  Translate shadow      0:0/0  2:-44.5/0  4:-30.5/0  7:-15.7/0  9:5.78/0  15:0/0
  Scale     shadow      0:0.761/1.16  2:1.07/1.16  4:0.743/0.799  7:1.09/1.17  9:0.937/1.01  15:1/1
== hit_02  0.67 s = 20 khung
  Translate bone2       0:-0.447/-5.86  10:-0.447/-5.86  11:0/-8.58  13:0/34.3  15:0/-0.766  17:0/1.79  19:0.039/-7.35  20:0/0
  Scale     bone2       0:0.817/1  5:0.758/1  10:0.682/1  11:1.55/0.625  13:0.929/1.09  17:0.955/1.08  19:1.13/0.884  20:1/1
  Rotate    bone4       0:-73  10:-73  13:-49.9  15:35.3  17:53.1  20:32.6
  Rotate    bone5       10:0  13:-50.9  15:-61.8  17:22.6  20:17.7
  Rotate    bone3       10:0  13:2.64  20:0
  Translate bone3       0:-2.13/31.7  10:-2.44/82.2  11:-7.82/-43.6  13:-19.6/3.65  20:0/0
  Scale     bone3       0:1.21/1  5:1.54/0.745  10:0.955/0.807  13:1.16/1.04  20:1/1
  Rotate    bone6       10:0  13:-42.4  15:-77.4  17:-45.3  20:0
  Translate bone7(mat)  0:0/0  5:-10.8/-16.8  10:0/0  15:15/0  20:0/0
  Translate shadow      10:0/0  11:2.48/0  13:-4.12/0  15:-7.42/0  20:0/0
  Scale     shadow      0:0.798/0.798  5:0.409/0.409  10:0.8/0.8  11:1.55/1.55  13:0.807/0.807  15:1.11/1.11  19:1.14/1.14  20:1/1
  Rotate    bone8       0:-47  10:360
  Translate bone8       0:-4.23/72.1  5:-1.94/228  10:0.357/4.25
```

## 6. Kết quả rig (2026-11-11)

Lệnh: `py -3 -I ArtGen/Spine/ti_tach.py cat` (cắt concept), `... mat` (cắt tờ nét mặt), rồi
`py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ti_tach.py all` (dạng 2, rồi dạng 1 gộp dạng 2 cho `evolve`).
Ra `inbox/ti_tach_<k>/rig/`: `.atomik`, `xem.html`, `khung_<clip>.png`, `xem_nhay.png` (chiêu cuối ghép cung nhảy giả), `luoi.png`.

| | Dạng 1 | Dạng 2 |
|---|---|---|
| Xương / slot | 14 / 6 (gộp tiến hóa: 31 / 15) | 17 / 9 |
| Lưới thân | 1858 đỉnh, 3520 tam giác, góc nhỏ nhất 31,8°, hở 0 px | 2067 đỉnh, 3927 tam giác, góc nhỏ nhất 30,6°, hở 0 px |
| .atomik | 241 KB (có dạng 2 bên trong cho `evolve`) | 136 KB |
| Cao thật / game.height | 383 / 498 (khai cao hơn để vẽ nhỏ hơn dạng 2) | 434 / 434 |

- Mảnh: thân, mắt mở, vệt má, giọt con cắt thẳng từ concept (thân xoá mặt bằng vân sáp chép từ chỗ sạch); GPT chỉ vẽ tờ `M01`
  (mắt `> <`, xoáy, `^ ^`, chớp, miệng nhỏ, miệng há). Thân là một lưới liền nên không có khớp nào để hở.
- **Mặt không thò ra ngoài thân**: `ep_mat` đo diện tích mắt, má, miệng nằm ngoài thân (thân co vào 4 px) ở mọi khung, đẩy xương
  `mat` về tâm thân, vẫn thò thì co mặt. Sau khi ép: 0 px² ở mọi clip (riêng `die` dạng 1 còn 4 px² lúc đang mờ).
- Clip (dạng 2 chậm hơn 1,12 lần): `appear` 0,8 s · `idle` 2,67 s (2 vòng idle gốc, vòng hai chớp mắt) · `attack` 1,07 s, sự kiện
  `trung` 0,40 s, cú lao nằm trên xương `move` (sân kéo tới đối thủ) · `cast` 1,33 s, `phun` 0,45 s, `het_phun` 0,93 s ·
  `skill` 1,2 s, `bat` 0,83 s, **kết thúc ở dáng đang bay** · `skill_land` 0,87 s, `cham_dat` 0,15 s · `hit` 0,53 s ·
  `die` 1,47 s · `evolve` 2,8 s (chỉ dạng 1).
- Giọt con: dạng 1 hai giọt quay quanh tâm cụm (dời chỗ, không xoay, để khép vòng được); dạng 2 năm giọt nhấp nhô lượn sóng.
  Cần đỡ giọt và đỉnh vòm chạy lò xo (`LoXo`) nên mọi clip đều có rung thạch và giọt văng trễ.
- Chưa làm: đưa vào game (chép `.atomik` vào `Assets/03 Art/Heroes/Resources/ti_tach_<k>/`, code nối `skill` → cung nhảy →
  `skill_land`, gọi `appear` / `die`), VFX tia nước của `cast`.

## 7. Đã vào game (2026-11-11)

- Chép bằng `quai/vao_game.py` (`da_nhan.json` dòng `ti_tach` trỏ `inbox/ti_tach_<k>/rig`): `.atomik` + chân dung vào
  `Assets/03 Art/Heroes/Resources/ti_tach_1`, `ti_tach_2`. `heroes.json` không đổi (cỡ 0,92 / 1,1; tên, thẻ như cũ).
- Code (assembly PokiClash.Game, biên dịch thử bằng csc của Unity ngoài Editor: 0 lỗi):
  - `AolaSticker`: rig có clip `skill_land` thì `Duration(Skill)` = dài `skill` + `skill_land`, `HitTime(Skill)` = lúc
    `cham_dat`, `Show` tự chuyển sang `skill_land` khi hết `skill`; `Jump(clip, t, to, h, out o)` tính cung nhảy: rời đất ở
    sự kiện `bat` (game.hitTimes của `skill`), bay parabol tới chỗ đáp, đè 0,16 s, bật về 0,42 s.
  - `StageView.Place`: chiêu cuối gọi `Jump` với chỗ đáp = đầu đối thủ (62 % chiều cao đối thủ); rig có clip `appear` / `die`
    thì sân phát clip đó thay cho rơi / xoay mờ bằng code (áp cho mọi rig có hai clip này). `WaterFx` của `ti_tach`: chiêu mana
    `n_tia`, chiêu cuối `n_va` (nước toé lúc chạm).
  - `HeroViewer`: nút Chiêu trong hộp chi tiết nhảy tới trước rồi bật về.
- Chưa xem chạy trong Unity ở phiên này (cầu MCP không mở). Kiểm: hộp chi tiết tướng (mọi nút clip), trận ải 1 đảo Thủy.

### Sửa 2026-11-11: tia nước phải ra từ miệng (người dùng báo)

- `HeroViewer.FxGeo` đặt cứng chỗ bắn ở 62 % chiều cao tướng; Tí Tách có miệng ở ~19 % nên trong hộp chi tiết tia phun từ trên
  đầu. Nay khung xem đọc chỗ bắn của rig (`AolaSticker.BeamUnit` = `game.muzzle` chia chiều cao), như `StageView.Muzzle` trên sân.
- Dòng nước `n_tia` (HatNuoc.NTia) chảy 0,88 s thật kể từ `phun`, clip cũ chỉ há miệng 0,48 s. Nay `cast` giữ miệng há 0,94 s
  tính bằng giây (không co theo `CHAM`), `het_phun` = `phun` + 0,94 s; clip dài 1,79 s (dạng 2: 1,89 s). Miệng nhỏ hiện từ khung 5
  lúc nước đang tụ trước miệng. `game.muzzle` dạng 1 = (80; 71) trên chiều cao 383, dạng 2 = (101; 86) trên 434.
