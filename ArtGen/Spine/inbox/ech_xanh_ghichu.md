# Dòng ếch xanh (mã tạm `ech_xanh`): tướng thứ 2 đảo Thủy, làm theo ý người dùng (2026-11-11)

Người dùng lên ý tưởng và duyệt từng bước (chưa đặt tên; mã `ech_xanh` chỉ để đặt thư mục).
Gói prompt: `ArtGen/Spine/build_ech_xanh.py` → `gui_gpt/ech_xanh_<k>/`, ảnh về `inbox/ech_xanh_<k>/tai_ve/`.

## 1. Ý người dùng (nguyên văn tóm lại)

- Dựa trên con gốc `monster_3230` (game tham khảo). Concept: **một con ếch xanh**, miếng giấy trên mồm con gốc thay bằng **lưỡi đỏ**.
- `idle`: làm giống con gốc, bụng thở phình co; lưỡi đung đưa nhẹ, thò ra thụt vào nhẹ nhàng.
- Đánh thường: há mồm rồi **bắn lưỡi dài** vào kẻ địch; lưỡi tốc độ cao, có sức nặng.
- Bắn nước: chỉ há mồm, nước bắn từ mồm ra (**fx không làm**, thuộc lớp VFX).
- Chiêu cuối: **phình to bụng** rồi **ợ ra một quả cầu nước**; mềm và mượt: quả cầu đi từ bụng lên mồm rồi ếch há mồm phụt ra.
- Chết: ngửa người ra sau, lè lưỡi.
- Dạng 2: y như vậy nhưng to hơn và chiến hơn.
- Dung lượng mỗi dạng **tối đa 0,5 MB**, ít hơn càng tốt.

Chưa rõ, đã hỏi người dùng: "xanh" là xanh lá (đang làm theo nghĩa này) hay xanh lam; suất trên đảo (thứ 2 = ải 5, đang là Thạch
Giải; dòng Nòng Xoáy ải 10 cũng là ếch).

## 2. Mổ xẻ con gốc `monster_3230` (chỉ học cấu trúc và nhịp, không lấy hình)

Nguồn: `D:\Ripper\SwordxStaff\web\assets\Monster\monster_3230\` (Spine 4.2.28, skel 40 KB + ảnh 77 KB). Kết quả quét:
`D:\Ripper\SwordxStaff\scan\monster_3230\` (`info.json`, `keys.json`, `mesh.json`, tờ khung `khung/<clip>.jpg`).
Quét lại: `py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/mo_xe/chay.py info|keys|mesh|sheet ...`.

### Ảnh (atlas 420 × 332, xuất tỉ lệ 0,75; 16 vùng)

| Vùng | Cỡ | Là gì |
|---|---|---|
| `P_shenti1` | 164 × 94 | **mũ đầu**: nửa trên (lưng, đỉnh đầu, môi trên), luôn hiện, vẽ trên cùng của thân |
| `P_shenti2` | 149 × 131 | **bụng lúc miệng khép** (cả khối kem tròn) |
| `P_shenti3` | 144 × 93 | **bụng lúc miệng há** (hàm dưới + bụng, mép trên là môi dưới) |
| `P_shenti4` | 93 × 104 | mảng lưng sau (lấp phía sau khi đầu ngửa) |
| `P_kouqiang2` | 138 × 78 | lòng miệng trên (vòm họng đỏ), luôn hiện, nằm sau bụng |
| `P_kouqiang1` | 121 × 44 | lòng miệng dưới (mặt lưỡi đỏ), chỉ hiện khi há |
| `P_shetou2` | 54 × 104 | "lưỡi" ngắn buông trước bụng (ở con gốc là lá bùa), 4 đốt |
| `P_shetou1` | 53 × 192 | "lưỡi" dài lúc bắn, 6 đốt, có deform |
| `P_yanjing1`, `2` | 63 × 63 | hai mắt lồi (mỗi mắt một xương) |
| `P_tuiL1..3`, `P_tuiR1..3` | ~60 × 75, 44 × 24 | hai chân, mỗi chân đùi + ống + bàn (IK 2 đốt, bàn chân bám đích riêng) |

**Miệng há = đổi ảnh**, không uốn một ảnh: lúc há tắt `shenti2`, bật `shenti3` + `kouqiang1`; đồng thời tắt lưỡi ngắn, bật lưỡi
dài (đòn lưỡi) hoặc không bật gì (clip há miệng gầm). Đổi đúng 1 khung, ngay lúc thân đang giật mạnh nên không lộ.

### Xương (34) và slot (17)

```
root
└─ bone2 (y −100; đích IK bàn chân R2→R1, L2→L1 và bóng là con của nó)
    └─ bone (đất)
        └─ bone3 (tâm thân: nhún, dời, lộn cả thân; chân theo qua IK)
            ├─ bone4 (đáy thân phía sau: nghiêng cả khối)
            │   ├─ bone5 (nửa trên / đầu: ngửa ra sau là há miệng, +18..29°)
            │   │   ├─ bone6 (môi trên phía trước: nhích khi lấy đà)
            │   │   │   └─ bone19 → 20 → 21 → 22 (lưỡi ngắn, bám môi trên)
            │   │   └─ bone9, bone10 (hai mắt)
            │   ├─ bone7 (môi dưới phía trước: xoay −19° khi há)
            │   ├─ bone8 (**bụng**: phình bằng scale 1 → 1,77; dời khi lắc)
            │   └─ bone23 → … → bone28 (lưỡi dài 6 đốt, gốc ở trong miệng)
            ├─ bone11 → 12 → 13 → 14 (chân trái: hông dời, đùi, ống, bàn)
            └─ bone15 → 16 → 17 → 18 (chân phải)
```
Thứ tự vẽ sau → trước: bóng, chân xa (3), mắt xa, lưng sau, bụng há, lòng miệng trên, lòng miệng dưới, bụng khép, lưỡi ngắn,
lưỡi dài, mũ đầu, chân gần (3), mắt gần. (Lưỡi nằm **dưới** mũ đầu nên gốc lưỡi khuất sau môi trên.)

### Lưới và trọng số

- Rất thưa: mỗi mảnh 8–25 đỉnh. Bụng khép 18 đỉnh: mép sau bám `bone4`, mép trên bám `bone5` (đi theo đầu), **mặt trước và đáy
  bám `bone8` 0,6–1,0** (tâm bụng 1,0) → scale `bone8` là bụng phồng ra trước mà lưng không đổi.
- Mũ đầu 24 đỉnh: phía sau `bone5`, vành môi trước `bone6`.
- Lòng miệng trên: mép trên theo `bone5/bone6`, mép dưới theo `bone4` → há ra thì tấm đỏ **giãn** lấp khoảng hở.
- Lưỡi: dải 2 cột, mỗi đốt một cặp đỉnh. Kéo dài lưỡi = **scale x xương gốc** (1,0 → 1,5) + deform.
- Chân: mỗi khúc cứng theo một xương. Không physics, không sự kiện.

### Mẹo diễn chính

1. **Bụng thở tách khỏi nhún thân**: `bone3` nhún 2 lần mỗi vòng (lên 9,7 px), `bone8` phình **một lần** (5 khung lên 1,77, giữ 10
   khung, 5 khung về) rồi nghỉ nửa vòng → nhịp "hít một hơi, giữ, xả, nghỉ". Hông hai chân dời ngược (−8, −9 px) nên chân như
   lún khi thân nhô.
2. **Lưỡi ngắn rung như giấy trước gió**: 4 đốt, khung 15–27 đổi chiều mỗi 2 khung (±14..30°), trước và sau đó lắc chậm.
   Của mình: lưỡi thịt, nặng, nên **bỏ rung nhanh**, thay bằng đung đưa trễ pha + thò thụt.
3. **Đòn lưỡi `skill_01`** (35 khung): 0–4 ngồi thụt ra sau (thân −27 px, đầu cúi −19°, lưỡi ngắn co lại scale 0,37 và rút lên
   = "nuốt lưỡi vào"), 4–9 giữ, bụng phình 1,43; **11–12 bung trong 1 khung**: thân lao +41/+36 px, đầu ngửa +18°, đổi ảnh há
   miệng, lưỡi dài quất ra (gốc xoay 49° → 68° → 130°, scale 0,53 → 1,0 → 1,51 ở khung 14); 14–25 giữ, lưỡi uốn sóng dư lực;
   25–27 rút về 2 khung, đổi ảnh khép ở khung 27; 27–35 nảy tắt dần, bụng phình lần nữa (1,49).
4. **Há miệng `skill_03`** (38 khung): lấy đà như trên (0–6), khung 8–9 há, chồm tới +73 px, chân sau duỗi chống; giữ há tới khung
   22–26 (đầu lắc nhẹ), khép khung 26, nảy về.
5. **Chết `die_01`**: bị hất lộn 360° lên cao 325 px (khung 0–12), rơi khung 14 nằm nghiêng, miệng há, lưỡi dài văng ra đất, 14–30
   nảy tắt dần (đầu, bụng, lưỡi lắc ngược pha). Của mình đổi: **ngã ngửa ra sau** (không lộn vòng), lưỡi thè.
6. Hầu hết khoá thẳng; nhịp giật (1–2 khung) ở lúc ra đòn, 4–8 khung ở lúc nảy về.

### Clip (13)

`idle_01` 1,33 s; `skill_01` 1,17 s (đòn lưỡi); `skill_02` 1,0 s (nhảy khỏi màn rồi rơi xuống đè); `skill_03` 1,27 s (há miệng);
`hit_01` 0,5 s; `hit_02` 0,67 s; `die_01` 1,0 s; `block_01` 0,5 s; `floating_01` 1,5 s; `run_01` 0,87 s; `stun_01` 1,33 s;
`skill_02XX`, `hit_02XXX` (bản nháp của họ).

| Clip của mình | Học từ | Ghi chú |
|---|---|---|
| `idle` | `idle_01` | bụng phình co một nhịp, nhún 2 lần; lưỡi đung đưa trễ pha + thò thụt nhẹ |
| `attack` | `skill_01` | lưỡi bắn **ngang** về phía đối thủ (con gốc quất chéo lên), ra trong 1–2 khung, khựng, dư lực, rút nhanh |
| `cast` | `skill_03` | chỉ há miệng; sự kiện `phun` / `het_phun`, xương `mieng` cho VFX |
| `skill` | mới | bụng phình to → cục phồng chạy từ bụng lên họng → há miệng phụt; sự kiện `nha` |
| `hit` | `hit_01` | |
| `die` | nửa sau `die_01` | ngã ngửa ra sau, lưỡi thè, nảy tắt dần |
| `appear`, `evolve` | chưa có ý của người dùng | hỏi khi tới bước clip |

## 3. Thiết kế của mình (dạng 1)

- Dáng: ếch tròn như cục bánh, đầu liền thân; nửa trên xanh lá (lưng + đầu), nửa dưới trước là bụng kem tròn trơn. **Đường miệng
  = ranh xanh / kem** (như con gốc: há miệng là tách đúng ranh này, cả bụng là hàm dưới + túi họng).
- Khác con gốc: xanh lá thay lam, **mắt ếch có tròng vàng, con ngươi ngang, mí sụp quả quyết** thay hai cục xoắn ốc; đốm tròn thay
  vằn; lưỡi đỏ thay lá bùa; không có hình xoắn ốc nào (tránh gợi một dòng nòng nọc nổi tiếng). Nét dự án: mực nâu `#2B2118`, sáp phẳng.
- Màu: thân `#5DB947`, đốm `#3C8C3A`, bụng `#F4EBCB`, lưỡi `#D93A32` (đường giữa `#A8231F`), tròng `#F7E37E`.
- Chân: bản chính chỉ hai chân sau như con gốc (rig nhẹ); bản phụ `--note` thêm hai tay trước nhỏ để người dùng chọn.

## 4. Dự kiến rig (làm sau khi concept được duyệt)

- Ảnh cần thêm (lượt 2, cùng khung 1536 × 1024, đính concept đã duyệt): **thân miệng khép không lưỡi**; **dáng há miệng** (mũ đầu
  ngửa, hàm dưới + bụng, lòng miệng đỏ trên và dưới); **lưỡi ngắn** rời vẽ đủ gốc; **lưỡi dài** rời (thẳng, đầu lưỡi bè có khối
  nặng); chân gần, chân xa vẽ đủ phần khuất; mảng lưng sau.
- Xương: `root → move (code dời) → than (nhún, dời) → day (nghiêng) → dau (ngửa = há), moi_tren, moi_duoi, bung (phình),
  hong (cục phồng chạy lên: 2–3 xương dọc bụng → họng, phình lần lượt), mat ×2, luoi ngắn 4–5 đốt, luoi dài 6–8 đốt, mieng
  (chỗ và hướng nhả cho VFX)`, chân IK bám đất. Lưới dày hơn con gốc ở bụng (viền 1,5 % H, trong 2 % H) để phình mượt.
- Cầu nước của chiêu cuối: phần **ra khỏi miệng** là VFX (sự kiện `nha` + xương `mieng`); phần **trong thân** (cục phồng chạy từ
  bụng lên họng) là diễn của rig.
- Dung lượng: con gốc 0,1 MB. Của mình: atlas thu ~0,5 lần, bảng 256 màu; nướng 30 khung/giây lọc RDP; đích < 0,3 MB mỗi dạng
  (dạng 1 có gộp dạng 2 cho `evolve` thì thu dạng sau 0,5 lần).

## 5. Khoá gốc của các clip sẽ học (khung 30 fps; `x/y` là dời hoặc tỉ lệ; tên xương xem cây ở mục 2)

```
== idle_01 1.33s = 40 khung
  Rotate     bone3        0:0  10:0.981  20:0  30:0.981  40:0
  Translate  bone3        0:0/0  10:0/9.68  20:0/0  30:0/9.68  40:0/0
  Scale      shadow       0:1/1  10:1.03/1.03  20:1/1  30:1.03/1.03  40:1/1
  Rotate     bone4        0:0.045  5:2.16  15:-2.07  25:2.16  35:-2.07  40:0.045
  Rotate     bone5        0:-3.73  5:-8.37  15:0.919  25:-8.37  35:0.919  40:-3.73
  Translate  bone6        0:0/0  5:7.78/5.18  15:7.78/5.18  20:0/0
  Translate  bone8        0:0/0  5:7.18/1.41  15:17.4/4.2  20:0/0
  Scale      bone8        0:1/1  5:1.77/1.77  15:1.77/1.77  20:1/1
  Translate  bone11       0:0/0  10:0/-7.74  20:0/0  30:0/-7.74  40:0/0
  Rotate     bone12       0:0  20:0  40:0
  Rotate     bone13       0:0
  Rotate     bone14       0:0  20:0  40:0
  Translate  bone15       0:0/0  10:0.071/-9.39  20:0/0  30:0.071/-9.39  40:0/0
  Rotate     bone17       0:0
  Rotate     bone18       0:0
  Rotate     bone19       0:3.28  5:6.57  15:3.11  17:17.9  19:13.9  21:17.9  23:13.9  25:17.9  27:18.3  35:0  40:3.28
  Rotate     bone20       0:-0.993  10:5.32  14:19.6  16:20.1  18:29.5  20:17.3  22:29.5  24:17.3  26:31.1  30:13.8  35:4.31  40:-0.993
  Rotate     bone21       0:-0.56  5:-4.35  15:11  17:-14.6  19:13  21:-11.5  23:14.7  25:-10.1  30:8.78  35:4.58  40:-0.56
  Rotate     bone22       0:7.42  10:-7.92  15:4.84  17:-13.3  19:14.6  21:-13.3  23:14.6  25:-5.77  30:2.77  35:14.8  40:7.42
== skill_01 1.17s = 35 khung
  Attachment P_kouqiang1  {"n": 1, "f": [0.367, 0.9], "slotIndex": 8, "names": ["P_kouqiang1", null]}
  Attachment P_shenti2    {"n": 1, "f": [0.367, 0.9], "slotIndex": 9, "names": [null, "P_shenti2"]}
  Attachment P_shenti3    {"n": 1, "f": [0.367, 0.9], "slotIndex": 6, "names": ["P_shenti3", null]}
  Attachment P_shetou1    {"n": 1, "f": [0.367, 0.9], "slotIndex": 11, "names": ["P_shetou1", null]}
  Attachment P_shetou2    {"n": 1, "f": [0.367, 0.9], "slotIndex": 10, "names": [null, "P_shetou2"]}
  Rotate     bone3        0:0  4:3.53  9:-0.61  11:-12.1  12:0  25:7.4  27:-6.62  31:0.272  35:0
  Translate  bone3        0:0/0  4:-26.9/1.9  9:-26.9/1.9  11:-12.4/-5.17  12:40.7/36.1  14:27.5/22.5  19:23.4/22.5  25:20.6/17.4  26:-12.5/7.27  27:-12.4/5.04  31:-1.43/20  35:0/0
  Translate  shadow       0:0/0  4:-22/0  9:-23.4/0  12:22/0  25:12.4/0  27:0/0  31:-3.97/0  35:0/0
  Scale      shadow       0:1/1  4:1.07/1.07  9:1.1/1.1  12:1/1  25:1/1  27:1.08/1.08  31:0.963/0.963  35:1/1
  Rotate     bone4        0:0.045  9:0.045  11:24.4  12:10.8  14:10.5  19:8.74  25:-2.43  27:0.045  31:-1.68  35:0.045
  Rotate     bone5        0:-3.73  4:-19.4  9:-24.5  11:-12.2  12:18.4  14:29.2  19:19.9  25:24.2  27:-14.7  31:-9.84  35:-3.73
  Translate  bone6        9:0/0  11:-10.7/-6.5  12:0/0
  Rotate     bone7        9:0  12:-18.9  25:-18.9  26:4.3  27:0
  Translate  bone7        9:0/0  11:35.8/0.943  12:0/0
  Rotate     bone8        9:0  11:-17.7  12:0  25:0  27:5.98  35:0
  Translate  bone8        4:0/0  9:7.65/1.95  11:-41.4/-1.09  12:-33/-1.72  14:-13.2/-0.433  19:-0.732/-0.129  25:-11.4/-1.76  27:13.3/4.93  31:-7.74/-2.1  35:0/0
  Scale      bone8        4:1/1  9:1.43/1.43  12:1/1  25:1/1  27:1.49/1.49  31:1/1
  Rotate     bone11       0:0  4:-27.5  9:-27.5  11:23.6  12:-41.7  25:-28.2  26:-9.29  27:0  31:-12.8  35:0
  Translate  bone11       0:0/0  4:-2.7/11.1  9:-2.7/11.1  11:-41.5/12.3  12:0/0
  Rotate     bone12       0:0  4:23.7  9:23.7  12:0
  Rotate     bone13       0:0  4:38.1  9:38.1  12:0
  Rotate     bone14       0:0  4:-50.1  9:-50.1  12:0
  Rotate     bone15       0:0  2:-14.8  4:-30.4  9:-11.1  11:-5.13  12:-31.4  14:-31.2  19:-37  25:-44.2  26:-0.949  27:11  31:7.33  35:0
  Translate  bone15       0:0/0  2:1.8/7.09  4:20.5/5.65  9:5.49/3.55  11:0.059/-15.9  12:21.2/-12.8  14:27.2/-20.7  19:27.6/-14.1  25:29.2/-4.99  26:11.8/-8.32  27:1.49/-12.9  31:-8/-4.95  35:0/0
  Rotate     bone16       0:0  4:-43.8  9:-43.8  12:0
  Rotate     bone17       0:0  4:3.87  9:3.87  12:0
  Rotate     bone18       0:0  4:52.8  9:52.8  12:0
  Rotate     bone19       0:3.28  4:4.09  9:34.1  11:12.1  12:3.28  25:3.28  27:3.85  31:-17.1  35:3.28
  Translate  bone19       0:0/0  4:-21.1/39.5  9:-40.3/40.2  10:-8.28/-3.2  11:-7.04/13.2  12:0/0
  Scale      bone19       4:1/1  6:0.374/1  9:0.363/1  27:1/1
  Rotate     bone20       0:-0.993  4:21.2  6:3.21  9:-10.3  11:27.6  12:-0.993  25:-0.993  27:32  31:-6.13  35:-0.993
  Rotate     bone21       0:-0.56  4:21.7  6:-1.38  9:-6.8  10:-18.4  11:-5.56  12:-0.56  25:-0.56  27:32.4  31:-0.505  35:-0.56
  Rotate     bone22       0:7.42  4:29.6  6:1.38  9:-4.45  11:-28.5  12:7.42  25:7.42  27:40.4  31:11  35:7.42
  Rotate     bone23       9:0  11:48.8  12:67.6  14:130  19:118  25:131  26:72.8  27:1.19  35:0
  Scale      bone23       11:0.527/1.01  12:1/1  14:1.51/1  19:1.42/1  25:1.18/1  26:0.606/1
  Rotate     bone24       9:0  11:-5.29  12:20.3  14:11.3  19:11.1  25:-14.1  26:6.38  27:0
  Rotate     bone25       9:0  11:-28.4  12:-38.1  14:30.7  19:30  25:-19.5  26:15.4  27:0
  Rotate     bone26       9:0  11:-25.5  12:-50.1  14:-29.1  19:24.1  25:21.4  26:5.09  27:0
  Rotate     bone27       9:0  11:-44.1  12:-25.3  14:-39.7  19:33.4  25:26.2  26:21  27:0
  Rotate     bone28       9:0  12:-46.4  14:-63.5  19:30.7  25:22.8  26:-14.1  27:0
  Translate  R2           0:0/0  2:-39.3/0  11:-39.3/0  12:0/0
  Deform     P_shetou1    11:  12:  13:  14:  19:  25:  26:  27:
  _DrawOrder ?            11:
== skill_03 1.27s = 38 khung
  Attachment P_kouqiang1  {"n": 1, "f": [0.267, 0.867], "slotIndex": 8, "names": ["P_kouqiang1", null]}
  Attachment P_shenti2    {"n": 1, "f": [0.267, 0.867], "slotIndex": 9, "names": [null, "P_shenti2"]}
  Attachment P_shenti3    {"n": 1, "f": [0.267, 0.867], "slotIndex": 6, "names": ["P_shenti3", null]}
  Attachment P_shetou2    {"n": 1, "f": [0.233, 0.867], "slotIndex": 10, "names": [null, "P_shetou2"]}
  Rotate     bone3        0:0  2:3.53  6:-0.61  8:-12.1  9:-16.2  18:11.1  22:-3.53  26:5.49  34:-10.7  38:0
  Translate  bone3        0:0/0  2:-45.3/1.9  6:-38.7/1.9  8:-12.4/-5.17  9:72.7/31.7  14:52.4/35.7  18:32.8/46.2  22:-2.3/23.6  26:-26.9/27.6  34:-0.24/17.2  38:0/0
  Translate  shadow       0:0/0  2:-32.7/0  6:-32.7/0  8:-13.1/0  9:9.06/0  18:1.29/0  22:-18.1/0  26:-32.8/0  34:-3.97/0  38:0/0
  Scale      shadow       0:1/1  2:1.12/1.12  6:1.12/1.12  8:1.07/1.07  9:1.2/1.2  18:1.08/1.08  22:1.02/1.02  26:1.02/1.02  34:0.963/0.963  38:1/1
  Rotate     bone4        0:0.045  6:0.045  8:24.4  9:10.8  14:8.74  18:-2.43  22:9.8  26:-9.45  34:-1.68  38:0.045
  Rotate     bone5        0:-3.73  2:-19.4  6:-24.5  8:-6.23  9:18.4  14:19.9  18:19.4  26:-11  29:3.03  34:2.81  38:-3.73
  Translate  bone6        6:0/0  8:-10.7/-6.5  9:0/0
  Rotate     bone7        6:0  9:-18.9  22:-18.9  26:0
  Translate  bone7        6:0/0  8:35.8/0.943  9:0/0  22:0/0  26:50/14  38:0/0
  Rotate     bone8        6:0  8:-17.7  9:0  18:0  22:1.41  26:21.8  34:8.78  38:0
  Translate  bone8        2:0/0  6:7.65/1.95  8:-41.4/-1.09  9:-33/-1.72  14:-0.732/-0.129  18:-11.4/-1.76  22:-19.1/20  26:14.9/-19.3  30:-11.4/8.26  34:2.12/1.58  38:0/0
  Scale      bone8        2:1/1  6:1.43/1.43  9:1/1  18:1/1  26:1.49/1.49  30:1/1
  Rotate     bone11       0:0  2:-27.5  6:-27.5  8:23.6  9:-41.7  18:-41.7  22:-17.1  26:-16.3  28:-23.3  30:-8.46  32:0
  Translate  bone11       0:0/0  2:-2.7/11.1  6:-2.7/11.1  8:-41.5/12.3  9:0/41.4  18:0/41.4  26:-21.8/7.15  32:0/0
  Rotate     bone12       0:0  2:23.7  6:23.7  9:0
  Rotate     bone13       0:0  2:38.1  6:38.1  9:0
  Rotate     bone14       0:0  2:-50.1  6:-50.1  9:0
  Rotate     bone15       0:0  2:-30.9  6:-22.9  8:-20.5  9:-30.9  14:-36.5  18:-43.6  22:-28.4  26:1.52  30:-10  34:0
  Translate  bone15       0:0/0  2:20.5/5.65  6:5.49/3.55  8:0.059/-15.9  9:21.2/2.11  14:29.9/15.5  18:40.3/24.1  26:-5.22/7.9  30:7.79/-4.56  34:0/0
  Rotate     bone16       0:0  2:-43.8  6:-43.8  9:0  14:178  18:-150  26:0
  Rotate     bone17       0:0  2:3.87  6:3.87  9:0  14:160  18:110  26:0
  Rotate     bone18       0:0  2:52.8  6:52.8  9:0  14:46.7  18:71.7  26:0
  Rotate     bone19       0:3.28  2:4.09  6:34.1  8:12.1  9:3.28  18:3.28  26:4.9  35:6.91  38:3.28
  Translate  bone19       0:0/0  2:-21.1/39.5  6:-42.4/45.1  7:-8.28/-3.2  8:-7.04/13.2  9:0/0  18:-3.95/27.8  26:-3.95/27.8  29:0/0
  Scale      bone19       2:1/1  4:0.374/1  6:0.363/1  26:0.363/1  29:1/1  35:1.09/1  38:1/1
  Rotate     bone20       0:-0.993  2:21.2  4:3.21  6:-10.3  8:27.6  9:-0.993  18:-0.993  26:7.16  29:-7.01  32:-16.5  35:-3.15  38:-0.993
  Rotate     bone21       0:-0.56  2:21.7  4:-1.38  6:-6.8  7:-18.4  8:-5.56  9:-0.56  18:-0.56  26:41.1  29:46.9  32:-19.4  35:-8.8  38:-0.56
  Rotate     bone22       0:7.42  2:29.6  4:1.38  6:-4.45  8:-28.5  9:7.42  18:7.42  26:-66.1  29:54.8  32:42.8  35:-25.4  38:7.42
  Rotate     bone23       6:0  8:48.8  9:67.6  14:118  18:131  26:1.19  38:0
  Scale      bone23       8:0.527/1.01  9:1/1  14:1.42/1  18:1.18/1
  Rotate     bone24       6:0  8:-5.29  9:20.3  14:11.1  18:-14.1  26:0
  Rotate     bone25       6:0  8:-28.4  9:-38.1  14:30  18:-19.5  26:0
  Rotate     bone26       6:0  8:-25.5  9:-50.1  14:24.1  18:21.4  26:0
  Rotate     bone27       6:0  8:-44.1  9:-25.3  14:33.4  18:26.2  26:0
  Rotate     bone28       6:0  9:-46.4  14:30.7  18:22.8  26:0
  Rotate     R2           0:0  2:-8.69  4:0  32:0  34:-36.9  36:0
  Translate  R2           0:0/0  2:-52.8/0  32:-52.8/0  34:-13.9/2.02  36:0/0
  Rotate     L2           28:0  30:-10.2  32:0
  Translate  L2           22:0/0  24:-49.9/0  28:-49.9/0  30:-19.9/-0.821  32:0/0
  _DrawOrder ?            8:
== die_01 1.00s = 30 khung
  Attachment P_kouqiang1  {"n": 1, "f": [0], "slotIndex": 8, "names": ["P_kouqiang1"]}
  Attachment P_shenti2    {"n": 1, "f": [0.433], "slotIndex": 9, "names": [null]}
  Attachment P_shenti3    {"n": 1, "f": [0.433], "slotIndex": 6, "names": ["P_shenti3"]}
  Attachment P_shetou1    {"n": 1, "f": [0.433], "slotIndex": 11, "names": ["P_shetou1"]}
  Attachment P_shetou2    {"n": 1, "f": [0.433], "slotIndex": 10, "names": [null]}
  Rotate     bone3        0:46.4  2:108  6:192  10:292  12:315  14:364  17:360  20:359  23:358  27:360
  Translate  bone3        0:0/78.3  2:0/289  6:0/325  10:0/289  12:0.895/249  14:0.076/20.9  17:0.095/44.1  20:0.076/15.7  23:0.083/17.3  27:0.076/6.97
  Scale      shadow       0:1/1  2:0.775/0.775  7:0.719/0.719  12:0.775/0.775  14:1.07/1.07  17:1.05/1.05  20:1.07/1.07  23:1.09/1.09  30:1.13/1.13
  Rotate     bone4        0:-11.2  2:0.045  12:-16.3  14:-19.6  17:-11.5  20:-25.2  23:-11.2  27:-20.7  30:-19.8
  Rotate     bone5        0:-32.6  2:-9.39  6:-23.8  10:-2.01  12:7.87  14:23.9  17:-25.6  20:3.95  23:-17.3  27:-4.35  30:-12.4
  Translate  bone5        12:0/0  14:12.1/6.68  17:-19.4/-0.991  20:-3.17/6.7  23:-19.2/-1.46  30:-21.1/-0.447
  Translate  bone7        12:0/0  14:36.8/20.4  17:-9.51/-4.5  20:0/0
  Rotate     bone8        0:21.4  2:0  12:21.1  14:6.35  17:15.9  20:25.3  23:21.4  30:25.3
  Translate  bone8        0:-31/-7.32  2:0/0  12:14.2/14.8  14:2.16/9.46  17:-16/2.07  20:17.1/17.7  23:5.42/11.8  27:24/23.7  30:22.1/21.1
  Scale      bone8        0:1/1  2:1.85/1.85  12:1.85/1.85  14:1/1
  Rotate     bone11       0:-39.7  2:-46.2  12:-48.9  14:-49.4
  Rotate     bone12       0:-27.5  2:-86.2  6:-102  10:-21.6  12:-37  14:-34.1  17:-40.2  20:-47.5  23:-23.2  27:-25  30:-27.7
  Rotate     bone13       0:65.8  2:59.5  6:110  10:104  12:127  14:135  17:168  20:196  23:133  27:142  30:147
  Rotate     bone14       0:0  2:-64  6:-14.3  10:-6.03  12:-10.7  14:0  17:-32.7  20:9.33  23:-1.14  27:-11.4  30:-13.3
  Rotate     bone15       2:0  12:-11.8  14:24.7  17:-14.2
  Rotate     bone16       0:-71.4  2:-241  6:-156  12:-147  14:-237  17:-106  20:-94.7  23:-87.1  27:-79.4  30:-77.3
  Rotate     bone17       0:44.3  2:80.9  12:1.18  14:31.9  17:44.7  20:-0.459  23:12.1  27:-8.79  30:-4.33
  Rotate     bone18       0:0  2:-80  12:-51.6  14:-46  17:-13.9  20:11.7  23:-13.4  27:0.107  30:-22.6
  Rotate     bone19       0:13.8  2:-31  6:-14  10:-8.02  12:25.5  14:11.4  17:-25  20:-20.8  23:2.48  30:24.9
  Scale      bone19       2:1/1  12:1.51/1
  Rotate     bone20       0:14.6  2:-10.1  6:-11.4  10:-21.2  12:26.3  14:51.5  17:-39.6  20:-26.7  23:0.015  30:-4.94
  Rotate     bone21       0:37.7  2:-26.6  10:-37.5  12:-31.1  14:32.4  17:46.2  20:-36.9  23:-56.5  30:-2.73
  Rotate     bone22       0:47.1  2:-18.6  10:-24.2  12:-40  14:-28.4  17:51.5  20:-27.1  23:-46  30:-8.48
  Rotate     bone23       12:0  13:117  14:122  17:42.6  20:89.7  23:53.4  27:54.4  30:49
  Rotate     bone24       12:0  13:-12.6  14:20.9  17:49.4  20:1.95  23:10.8  27:33.3  30:37.2
  Scale      bone24       20:1/1  23:1/0.513
  Rotate     bone25       12:0  13:-17.6  14:17.5  17:23.6  20:27.1  23:27.2  27:20  30:19.8
  Rotate     bone26       12:0  13:-20.4  14:-26.1  17:40.1  20:25.7  23:35.5  27:15.8  30:12.4
  Rotate     bone27       12:0  13:-31.7  14:-23.1  17:45.7  20:14.8  23:-10.5  27:20.3  30:8.87
  Rotate     bone28       12:0  13:-24.2  14:-37.8  17:-21.5  20:21.1  23:-17.4  27:17.9  30:0.845
  Deform     P_shetou1    13:  14:  20:
== hit_01 0.50s = 15 khung
  Attachment P_kouqiang1  {"n": 1, "f": [0.067], "slotIndex": 8, "names": ["P_kouqiang1"]}
  Attachment P_shenti2    {"n": 1, "f": [0.067, 0.5], "slotIndex": 9, "names": [null, "P_shenti2"]}
  Attachment P_shenti3    {"n": 1, "f": [0.067], "slotIndex": 6, "names": ["P_shenti3"]}
  Attachment P_shetou1    {"n": 1, "f": [0.067, 0.5], "slotIndex": 11, "names": ["P_shetou1", null]}
  Attachment P_shetou2    {"n": 1, "f": [0.067, 0.5], "slotIndex": 10, "names": [null, "P_shetou2"]}
  Rotate     bone3        0:-5.28  2:47.2  6:33.9  10:5.88  15:0
  Translate  bone3        0:-23.8/8.1  2:-57.5/125  6:-31.7/110  10:3.7/51.2  15:0/0
  Translate  shadow       0:-28.9/0  2:-50.8/0  6:-34/0  10:-3.38/0  15:0/0
  Scale      shadow       0:1/1  2:0.833/0.833  6:0.856/0.856  10:0.973/0.973  15:1/1
  Rotate     bone4        0:0.045
  Rotate     bone5        0:-32.7  2:14.6  6:42.2  10:35.1  15:-3.73
  Rotate     bone6        0:-16.3  2:-17  6:-11  10:-12.8  15:0
  Translate  bone7        10:0/0  15:54.3/13.2
  Rotate     bone11       0:-53.9  2:0  6:-37.9  10:-21.7  15:0
  Rotate     bone12       0:0
  Rotate     bone13       0:0
  Rotate     bone17       0:0
  Rotate     bone18       0:0
  Rotate     bone19       0:3.28  2:58.3  6:23.6  10:20.1  15:3.28
  Rotate     bone20       0:25.1  1:-10.2  2:-15.3  6:28.4  10:25.4  15:-0.993
  Rotate     bone21       0:24.6  1:-21.2  2:-36.8  6:-1.62  10:36.2  15:-0.56
  Rotate     bone22       0:35.2  1:-7.91  2:-20.8  6:-46.4  10:40.1  15:7.42
  Rotate     bone23       0:0  2:43.1  6:78.3  10:68.8  15:0
  Scale      bone23       2:0.777/0.787  10:0.777/0.787  15:0.552/0.787
  Rotate     bone24       0:0  2:25.6  6:57  10:34  15:0
  Rotate     bone25       0:0  2:-9.39  6:35.4  10:34.5  15:0
  Rotate     bone26       0:0  2:-51.1  6:-2.05  10:31.2  15:0
  Rotate     bone27       0:0  2:-34.5  6:-39.4  10:28.8  15:0
  Rotate     bone28       0:0  2:-31  6:-34.4  10:18.5  15:0
  Rotate     L2           0:0  2:-7.89  6:51.7  8:4.99  10:0
  Translate  L2           0:-24.1/0  2:-32.6/218  6:-42.5/237  8:0/0
  Deform     P_shetou1    2:  6:  10:  14:
```

## 6. Lượt gen

- 2026-11-11 `ech_xanh_1/tai_ve/L1_concept.png` (bản chính, chỉ hai chân sau): đúng đặc tả; bụng kem trơn, đường miệng là ranh
  xanh / kem, lưỡi buông thẳng có viền riêng, tô phẳng. Xanh tươi hơn mã màu đã ghi. Claude đề xuất bản này (bụng không bị che,
  dễ phình và tách hàm).
- 2026-11-11 `ech_xanh_1/tai_ve/L1_concept_2.png` (`--note` thêm tay trước): ra dáng ếch hơn, nhưng tay gần vắt ngang bụng từ
  khoé miệng xuống đất (phình bụng, há miệng phải tách thêm lớp tay), tay xa dính bàn chân xa.
- Người dùng chọn `L1_concept_2.png` (có tay trước), dặn chân sau bên kia phải khuất sau thân lúc nghỉ, chỉ lộ trong animation
  nào làm nó lộ. `ech_xanh.py bo_chan_xa` xoá chân đó bằng mã → `L1_sua.png` = `L1_duyet.png` (dạng 1 đã duyệt).
- 2026-11-11 11:23 `ech_xanh_2/tai_ve/L1_concept.png` (dạng 2, ảnh mẫu là `L1_duyet.png` dạng 1): to, bè vai, xanh đậm, gờ mày nhọn
  tù, ba u lưng, lưỡi dài đầu phình như găng; cùng dáng ngồi, bên phải chỉ lộ bàn tay xa. **Chờ người dùng duyệt** (chưa chép
  `L1_duyet.png` cho dạng 2, chưa có `CAT[2]`, `RIG[2]`).

## 7. Rig dạng 1 (2026-11-11, `ech_xanh.py cat 1` → `rig 1`)

Cách lai, **không gen thêm tờ nào**: mọi mảnh cắt thẳng từ `L1_duyet.png` (ghép lại trùng concept, chỉ lệch ở mép khử răng cưa),
phần bị che vẽ bù bằng vân sáp lát từ chỗ sạch của chính ảnh, nét mực kẻ nối theo tâm nét đo trên concept.

| Mảnh (`inbox/ech_xanh_1/manh/`) | Từ đâu | Ghi chú |
|---|---|---|
| `than` | vùng xanh liền (đầu, lưng, dải hông, hai mắt) | bỏ nét mực của đùi và của tay; mọc thêm dưới đùi (có nét viền đáy lưng kẻ nối) và dưới vai |
| `bung` | vùng kem | lấp chỗ lưỡi, tay, bàn tay che; nét đáy nối qua chỗ bàn tay che; nét môi là mép trên (dùng chung với `than`) |
| `luoi` | vùng đỏ | gốc mọc thêm 44 px lên trên (khuất dưới môi) bằng cách chép dải ngay dưới môi |
| `chan`, `tay` | đùi + bàn chân gần; tay gần | tay liền màu với thân (vai không có nét mực): cắt theo đường vai, đầu vai mờ dần |
| `tay_x` | bàn tay xa | cổ tay mọc thêm 90 px lên trên (khuất dưới bụng) |
| `luoi_dai` | dựng từ `luoi` | duỗi thẳng từng hàng, lát đoạn giữa cho dài 640 px, giữ đầu lưỡi; gốc ngả màu vòm họng |
| `hong` | dựng bằng mã | lòng miệng: nửa trên vòm họng đậm, nửa dưới sàn miệng, nét mực ngăn + nét mép trước; vân sáp lấy từ lưỡi |
| `mi_g`, `mi_x` | dựng bằng mã | mí nhắm: phủ xanh lên tròng + con ngươi, một nét khép song song gờ mày |
| chân sau bên kia | dùng lại ảnh `chan` | slot `chan_x` ẩn lúc nghỉ, chỉ hiện trong `die` |

Xương (33), khác con gốc ở mấy điểm:
- **Nắp đầu** `dau`: cả phần xanh phía trên xoay quanh bản lề phía sau (470, 660) như con gốc (`bone5`); `ham` (môi dưới) là **con của
  `dau`** nên đầu gật thì miệng vẫn khép, há miệng = xoay `ham` ngược lại (`ha(P, gật, ngửa, trễ môi)`).
- Lòng miệng `hong` là lưới ô 10 × 5: hàng trên bám `dau`, hàng dưới bám `ham`; lúc khép dẹt lại và khuất sau môi (không đổi ảnh).
- Bụng: dải sát môi theo `ham` (hoà rộng 230 px, hẹp hơn thì gãy nếp ở chóp môi), mép sau theo `day`, còn lại theo `bung`; ba xương
  `u1..u3` dọc mặt trước bụng để **cục phồng chạy từ dưới lên họng** (đẩy viền bụng lồi ra lần lượt).
- Chân gần, tay gần, bàn tay xa là lưới giãn: đầu trên theo thân, bàn theo xương bám đất (con của `move`); `theo()` cho chúng dính
  theo thân lúc rơi và lúc lật ngửa, `vung()` vung bàn quanh hông / vai.
- Lưỡi ngắn 5 đốt (con của `moi`, lò xo `LoXo`), lưỡi dài 8 đốt (con của `day`, gốc trong miệng, ẩn lúc nghỉ).
- `mieng` (chỗ và hướng nhả cho VFX) nằm giữa hai môi lúc há.

Clip (30 khung/giây, nhịp học từ khoá con gốc): `appear` 0,8 s (rơi, bẹp, nảy, lưỡi bung ra: **Claude đề xuất**, người dùng chưa
cho ý), `idle` 2,67 s (hai vòng: nhún 2 lần mỗi vòng, bụng hít - giữ - xả - nghỉ, lưỡi đung đưa trễ pha + thò thụt, vòng hai chớp
mắt), `attack` 1,27 s (nuốt lưỡi, phình bụng, bung 1 khung, lưỡi dài tới hết tầm ở 0,47 s = `trung`, đầu lưỡi chúi rồi nảy, rút 2
khung, thả lưỡi ra lại), `cast` 1,27 s (há ở 0,32 s = `phun`, giữ há có rung tới 0,73 s = `het_phun`), `skill` 1,93 s (hít ba hơi
bụng phình dần, nín rung, cục phồng chạy lên họng, ợ bật miệng ở 1,17 s = `nha`), `hit` 0,53 s, `die` 1,93 s (ngã ngửa 72°, chân
tay chổng lên, lưỡi dài thè ra vắt trên bụng, nảy tắt dần, mờ). `evolve` chờ dạng 2.

Số liệu: 4.619 đỉnh, 8.332 tam giác, lưới hở 0 px; `.atomik` 207 KB (đích 0,3 MB, trần 0,5 MB); nối clip khung đầu và khung cuối
0,00 px so với khung 0 `idle`; lệch `.atomik` so với bộ vẽ Python 0,03 px ở khung 0, tối đa 0,9 px giữa clip (do lược khoá).

**Sửa theo người dùng (2026-11-11 trưa, sau khi xem `xem.html` và so với con gốc): "phần mồm khi mở không đúng, lưỡi cũng sai".**
Bản đầu há hẹp (ngửa 19° + trễ 7°), sàn miệng chỉ là một dải mỏng trong ảnh vòm họng, lưỡi dài bắt đầu bằng vết cắt đứng giữa
miệng và nằm TRƯỚC bụng nên đè lên môi dưới như tấm ván. Đã đổi:
- Há rộng như con gốc: nắp đầu ngửa 28–34°, môi dưới trễ 10–11° (`attack`, `cast`, `skill`).
- `hong` chỉ còn vòm họng một màu đậm + nét mực mép trước; thêm mảnh **`san`** (sàn miệng = mặt trên hàm dưới, hình thấu kính đáy
  phẳng, mép trên cong là môi dưới bên kia có nét mực), lưới ô 12 × 4 đặt dọc nét môi, bám 100 % `ham`, lúc khép khuất sau nắp đầu.
- Thứ tự lớp: `hong` < **`luoi_dai`** < `san` < `bung` < `luoi_ru` < `luoi` < `than`. Lưỡi bắn nằm sau sàn miệng và hàm dưới nên
  trông như chui từ trong họng ra, vượt qua mép môi bên kia; gốc lưỡi dời vào sâu (555, 516), khuất hẳn sau má. Ảnh lưỡi dài 900 px.
- `luoi_ru`: cùng ảnh, cùng chuỗi xương `d0..d7` nhưng ở slot trước bụng, chỉ dùng trong `die` (lưỡi thè vắt trên bụng).
- Số liệu sau khi sửa: 13 slot, 5.631 đỉnh, 10.150 tam giác, `.atomik` 233 KB.

**Sửa lần hai theo người dùng (2026-11-11 trưa, xem bản há rộng):**
- "Cuống lưỡi đẩy sâu vào trong nữa cho đỡ lộ": gốc lưỡi dài dời tới (445, 532), sau má và dải hông; ảnh lưỡi dài 1010 px. Khoé
  miệng thành **bản lề đứng yên** (`vung_day` ôm cả khoé miệng và vai): trước đó khoé bị nhấc theo nắp đầu (lệch trái 60 px ở 30°)
  nên lộ cuống lưỡi và mép mờ của vai.
- "Ở góc nhìn này không thấy được phần thịt đỏ trong ở hàm dưới": **bỏ hẳn mảnh `san`** (sàn miệng). Miệng há chỉ còn vòm họng;
  lưỡi ló ra từ sau môi dưới. Con gốc có vẽ sàn miệng nhưng góc nhìn của nó chếch từ trên; con mình nhìn ngang.
- "Lưỡi xoay ngang quá, phải xoay theo hướng mảnh hơn, lưỡi này là góc nhìn từ trên xuống": lưỡi bắn bóp bề ngang phần thịt còn
  0,40 (`LUOI_HEP`), giữ nguyên bề dày nét mực hai mép. Lưỡi buông lúc nghỉ vẫn bản rộng (nhìn chính diện).
- `die`: phần lưỡi trong miệng nằm thẳng dọc khe miệng, ba đốt ngoài cùng mới rũ.
- Số liệu: 12 slot, `.atomik` 212 KB.

**Sửa lần ba (2026-11-11 trưa): "chiêu cuối chưa ra được kiểu bóng phình bụng rồi lên trên miệng".**
Bản cũ cả bụng phình đều rồi xẹp, ba cục phồng nhỏ lướt qua trong 6 khung nên không đọc được. Làm lại `skill` (2,13 s, `nha` ở 1,41 s):
- Ba **vùng phồng lớn** thay cho cục nhỏ: `u1` bụng dưới (bán kính 175 px), `u2` giữa (130), `u3` túi họng ngay dưới môi (120); trọng
  số tới 0,88, chừa dải sát môi (kẻo hở nét môi với nắp đầu). Mỗi vùng vừa nở (scale) vừa lồi ra theo hướng riêng.
- Nhịp: 0–0,67 s hít ba hơi, **bụng dưới** phình thành quả bóng; nín, rung; 0,87–1,27 s khối phồng dồn lên: bụng dưới xẹp hẳn (hơi
  hóp), giữa lồi rồi xẹp, **túi họng** phồng chìa ra dưới miệng; nín, rung; 1,41 s bật miệng, túi họng xẹp tức thì, đầu hất ngửa.
- Mảnh `gon` (nét cong mực nửa vòng, slot trước bụng, xương `bong`): ôm phía trong quả bóng, chạy theo từ viền bụng dưới lên túi họng.
- Đã thử và bỏ: phồng cả đầu (scale `dau`) lúc bóng vào miệng: mỏ chúi xuống đè lên bụng, không ra "phồng má".

**Sửa lần bốn (2026-11-11 trưa):**
- "Idle thi thoảng bị thừa ra phần miệng" (góc trên bụng lòi khỏi chóp môi lúc bụng thở): do `phinh()` co giãn xương `bung`, kéo cả
  vùng `u3` sát chóp môi ra ngoài. Nay `phinh()` chỉ nở vùng bụng dưới và giữa (`phong(P, 0|1, a)`), **không co giãn `bung` nữa**;
  dải sát môi đứng yên theo `ham`. Áp cho mọi clip.
- "Chiêu cuối chưa đúng ý, không cần làm phần hằn lên; làm bụng phình rồi chuyển phần phình đấy từ từ lên phần miệng rồi mở mồm
  như bây giờ": **bỏ mảnh `gon` và xương `bong`**; khối phình chuyển chậm hơn (0,87 → 1,57 s, ba vùng gối nhau), bật miệng ở 1,62 s
  (`nha`); clip dài 2,33 s.
- Số liệu: 33 xương, 12 slot, `.atomik` 221 KB.

**Sửa lần năm (2026-11-11 trưa): người dùng khoanh ba chỗ trên ảnh, "phình từ đoạn khoanh đỏ ở phần chân (nhưng không làm phình
chân) sau đó đi lên theo những vùng khoanh đỏ tiếp theo".** Ba vùng phồng dời về đúng ba chỗ đó (toạ độ concept):
`u1` (735, 825) đáy bụng phía sau bàn tay gần, bán kính 150; `u2` (915, 735) giữa bụng, 190; `u3` (1077, 605) góc trên phải ngay
dưới miệng, 125. Bản trước chạy dọc mép trước của bụng nên lệch ý.
- `u1` nằm sau bàn tay và sát đất nên nở tại chỗ thì không thấy: cho nó lồi XUỐNG dưới và đội cả thân lên (0,085 H); tay, chân chỉ
  giãn theo chứ không phình.
- `phinh()` (bụng thở, nảy ở các clip khác) nay chỉ dùng vùng giữa bụng `u2`.

Người dùng xem bản lần năm: **"ok ổn, dạng 2 đâu"** (2026-11-11 trưa) → dạng 1 coi như xong phần rig và clip.

## 8. Rig dạng 2 và clip tiến hóa (2026-11-11, `ech_xanh.py cat 2`, `all`)

- Rig trên `ech_xanh_2/tai_ve/L1_concept.png` (`CAT[2]["src"]`). **Người dùng chưa nói duyệt concept dạng 2**, chỉ hỏi "dạng 2 đâu";
  chưa chép `L1_duyet.png`. Nếu đổi concept thì đọc lại toạ độ `CAT[2]`, `RIG[2]` trên ảnh mới.
- Cùng bộ cắt, cùng xương, cùng clip với dạng 1; khác ở cấu hình:
  - nét mực dày ~15 px (`muc=18`, `net_day=15`); đốm xanh sẫm tối gần bằng mực nên `nguong_muc=82` (dạng 1 là 118); vạch giữa lưỡi
    `vach=(125, 195)`; ô vân xanh lấy theo trung vị màu thân chứ không theo ngưỡng cứng;
  - vai dạng 2 rộng, nét phải của tay chạy liền lên khoé miệng: cắt tay theo đường ngang y = 607; `vung_day` ôm trọn vai và khoé
    miệng (ôm hẹp thì khi há miệng vai bị kéo theo nắp đầu, lòi mảnh vẽ bù thành gai xanh nhạt);
  - `ti=1.45`: mọi khoảng hoà trọng số (px concept) nhân theo cỡ con; `PX` trong clip nhân các độ dời tuyệt đối theo chiều cao;
  - `CHAM[2] = 1.12` (mọi clip chậm hơn 12 %), `CAO_HIEU = {1: 1.25, 2: 1.0}` (dạng 1 vẽ nhỏ hơn dạng 2).
- Dọn chung cho cả hai dạng: mảnh `than` bỏ mẩu rời < 3000 px; trong vùng khuất của bụng (`an_bung`) không giữ nét mực nào; mép
  lưỡi dài làm mượt và lấy mẫu dưới điểm ảnh (bản trước bóp từng hàng theo số nguyên nên mép răng cưa).
- **Tiến hóa:** `all` dựng dạng 2 đủ nét (file dạng 2), rồi dựng thêm **bản nhẹ của dạng 2** (`NHE = (0.6, 1.8)`: ảnh nhỏ còn 0,6,
  lưới thưa 1,8 lần) chỉ để gộp vào rig dạng 1 cho clip `evolve` 2,8 s: dạng 1 nhắm mắt, bụng phình rung → đổi dạng ở 1,27 s →
  dạng 2 hiện, há miệng gầm, bụng nảy → về đúng khung 0 `idle` dạng 2.
- Số liệu: dạng 2 6.333 đỉnh, 11.395 tam giác, `.atomik` 304 KB; dạng 1 gộp dạng 2: 66 xương, 24 slot, 7.295 đỉnh, 8 clip,
  `.atomik` 339 KB (trần 0,5 MB). `evolve`: khung cuối lệch khung 0 idle dạng sau 0,00 px, không còn slot dạng cũ hiện.

**Sửa mí nhắm (người dùng xem dạng 2: "mắt nhắm bị lỗi, 1 bên thừa phần đen, 1 bên vẫn thấy ánh vàng"):** cách cũ lấy bao lồi của MỘT
mảnh vàng + khối mực dày trong 34 px quanh nó. Ở dạng 2 con ngươi to nằm lệch xa vùng vàng (sót mảng đen), vùng vàng mắt xa bị con
ngươi chia hai mảnh (mí chỉ phủ một mảnh). Cách mới, dùng cho cả hai dạng: gom các mảnh vàng gần nhau (nới 22 px) thành từng mắt;
lòng mắt = mọi điểm không phải da xanh, cách da xanh hơn một bề dày nét mực và không sát nền giấy (nét mực quanh mắt, gờ mày, viền
ngoài cùng đều bị loại), liền với vùng vàng của mắt đó; cộng lại vùng vàng và chấm sáng.

## 9. Vào game (2026-11-11 13:10, người dùng: "ok cho vào game đi")

- Dạng 2 coi như đã duyệt: chép `ech_xanh_2/tai_ve/L1_concept.png` → `L1_duyet.png`, `CAT[2]` bỏ khoá `src`.
- **Suất**: tướng thứ 2 đảo Thủy = ải 5 = id game **`thach_giai`** (dữ liệu lô 10 tướng mới; trước là cua "Thạch Giải", rig `tm02`).
  Ếch vào đúng suất này, **giữ nguyên id** để không đụng `heroes.json`, `cards.json`, `stages.json`, test, golden. Tên tướng, danh
  hiệu, tên dạng, tên ba thẻ trong game **vẫn là của con cua** (Thạch Giải / Thạch Thành Giải; Bọt Nước, Đá Ngầm Trồi, Vũng Triều):
  chờ người dùng đặt (phiên khác đổi suất ải 10 sang `ca_den` bằng script `quai/doi_ca_den.py`: mẫu để đổi id + tên khi có tên).
- Đã làm:
  - `quai/da_nhan.json`: mục `thach_giai` trỏ sang `inbox/ech_xanh_1|2/rig`.
  - Chép tay `ech_xanh_<k>.atomik` → `Assets/03 Art/Heroes/Resources/thach_giai_<k>/thach_giai_<k>.atomik`, `chan_dung.png` →
    `thach_giai_<k>_portrait.png` (`.meta`, `.asset` giữ nguyên nên prefab tướng không phải dựng lại). Không chạy `vao_game.py` không
    tham số (nó chép luôn dạng của phiên khác); `vao_game.py --kiem` báo hai dạng "giữ" (trùng rig mới nhất).
  - `Game/Battle/StageView.cs` `WaterFx["thach_giai"]` = `n_tia` (chiêu mana: tia nước từ miệng), chiêu cuối hai dạng `n_cau` (cầu
    nước từ miệng). `Game/Battle/HatNuoc.cs` `WTheme["thach_giai"]`: bỏ họa tiết mảnh đá `giap`; màu nước giữ tạm.
  - Unity (không có MCP ở phiên này): đưa cửa sổ lên trước cho nó tự nhập; nhật ký Editor: biên dịch không lỗi, nhập
    `thach_giai_1.atomik`, `thach_giai_2.atomik` và hai chân dung không lỗi.
- **Clip `cast` kéo dài đoạn há miệng**: clip có sự kiện `het_phun` nên sân không ghìm giờ clip ở khung nhả (`AolaActor.SelfHold`);
  tia `n_tia` chảy 0,93 s (`HatNuoc.HoldNuoc`). Bản cũ chỉ há 0,42 s (ngậm miệng lúc nước còn chảy). Nay há từ 0,32 s tới 1,25 s
  (`het_phun`), clip dài 1,8 s (dạng 2 nhân 1,12). `skill` không có `het_*` nên sân ghìm ở khung `nha` 0,12 s (`n_cau`): đúng ý.
- Chưa kiểm (không điều khiển được Unity): chưa thấy ếch trong trận, hộp chi tiết, nút Tiến hóa; chưa chạy menu "Chụp thử dạng
  .atomik", EditMode test. Cần xem: tầm lưỡi lúc đánh (thân lao 0,36 H rồi lưỡi vươn), cỡ hai dạng (`size` 0,92 / 1,1), chỗ tia và
  cầu nước ra có đúng miệng (`game.muzzle` lấy ở khung nhả của `cast`; chiêu cuối há to hơn nên miệng cao hơn một chút).
- `vao_game.py --kiem` cảnh báo `game.shadow 'shadow' không có slot đó` (rig không có bóng riêng; Tí Tách cũng vậy).

Chưa làm / còn yếu:
- Tên tướng, danh hiệu, tên thẻ, màu nước của suất `thach_giai` chờ người dùng.
- `skill`: nhịp đầu (đáy bụng) bị bàn tay che một phần, chỉ thấy đáy bụng tròn ra và thân được đội lên; chỗ phồng dưới miệng hơi
  gãy góc ở chóp môi (dải sát môi không phồng theo). Dạng 2: lúc bụng phình, tay bên kia bị kéo dài như chân.
- `evolve`: lúc dạng 2 há miệng gầm, lưỡi buông vẫn treo ở môi trên.
- Lưỡi bắn còn thẳng đơ (mới có đầu lưỡi chúi rồi nảy), chưa có sóng quất rõ như lá bùa của con gốc.
- `hit`: cổ tay xa bị kéo dài thành que khi thân ngả ra sau. `die`: dáng nằm ngửa mới là bản đầu, chờ người dùng xem.
- Đòn lưỡi: thân nhún tới 0,36 H trên `move` (sân kéo tới đối thủ), lưỡi dài ~1,2 H; tầm cần chỉnh khi thử trong trận.
- Chưa đặt tên, chưa có suất trên đảo, chưa vào `heroes.json`.
