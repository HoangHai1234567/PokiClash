# Dòng pháp sư nước bí ẩn (mã làm việc `phap_su`): tướng thứ 6 đảo Thủy (2026-11-11)

Người dùng lên ý tưởng và duyệt concept (chưa đặt tên; mã `phap_su` chỉ để đặt thư mục); mảnh, rig Claude tự làm.
Gói prompt: `ArtGen/Spine/build_phap_su.py` → `gui_gpt/phap_su_<k>/`, ảnh về `inbox/phap_su_<k>/tai_ve/`.

## 1. Ý người dùng (nguyên văn tóm lại)

- Dựa trên con gốc `monster_3313` (game tham khảo). Concept: **pháp sư nước bí ẩn, không thấy mặt, mũ che kín mặt**.
- `idle`, `die`: có thể làm giống con gốc, sửa đi chút.
- Đòn thường: giống `skill_01` của con gốc, **bắn tia nước** (tia là VFX, rig không vẽ).
- Chiêu mana: dùng lại động tác đòn thường, **đổi kiểu tia nước**.
- Chiêu cuối: giống `skill_02`: **triệu hồi các mũi kim nước** (đã có trong game), **dậm gậy xuống thì các kim bắn vào đối thủ**.
- Ra sân (triệu hồi): **gen thêm một vòng tròn triệu hồi rồi tướng trồi lên**.
- Dạng 2: cao lớn hơn là được.
- Cái khó: **rig kỹ phần quần áo, áo choàng** của phù thủy; mổ xẻ kỹ xương con gốc.

Người dùng không dặn màu, chi tiết. Thiết kế trong concept là **đề xuất của Claude**, chờ duyệt (khác hẳn con gốc: con gốc áo trắng
viền vàng, lông vũ lam trên mũ và gậy, mắt trên mũ, quần phồng lộ chân):

- sinh vật lùn quấn kín trong mũ áo, **dưới vành mũ chỉ một khoảng tối phẳng** `#151A33` (không mắt, không chấm sáng); bàn tay
  cầm gậy và mũi giày cùng màu tối đó (không ai biết bên trong là gì);
- **mũ chóp chàm** `#2A3580` to gần nửa chiều cao, chóp gập ngả ra sau có hạt cam san hô `#F2845C`; đai mũ lam băng, hai dải
  đai buông sau mũ;
- **khăn vai** lam băng `#DDF0F7` viền lượn sóng; **áo dài chuông** lam ngọc `#2F9FB3` chấm đất (không lộ chân, chỉ hai mũi
  giày); **vạt trước** lam băng có hình giọt nước; **áo choàng chàm** sau lưng gấu ba lượn sóng;
- **gậy gỗ lũa** `#9A7B63` đầu móc hình ngọn sóng ôm **quả cầu nước** `#86D6F0` (chỗ nhả tia), hai dây treo hạt cam.

## 2. Mổ xẻ con gốc `monster_3313` (chỉ học cấu trúc và nhịp, không lấy hình)

Nguồn: `D:\Ripper\SwordxStaff\web\assets\Monster\monster_3313\` (Spine 4.2.28, skel 85 KB + ảnh 115 KB, atlas 204 × 760, tỉ lệ
0,75). Kết quả quét: `D:\Ripper\SwordxStaff\scan\monster_3313\` (`info.json`, `keys.json`, `keys.txt` = khoá 8 clip dạng đọc được có
ghi vai từng xương, `mesh.json`, tờ khung `khung/<clip>.jpg`). Quét lại:
`py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/mo_xe/chay.py info|keys|mesh|sheet ...`.

102 xương, 42 slot (37 ảnh), 7 IK, 10 clip, 4932 khoá. Không physics, không path, không sự kiện, không deform: **mọi chuyển
động vải là khoá xoay tay trên chuỗi xương** (569 / 650 timeline là xoay).

### Xương theo nhóm

```
root → bone2 (gốc, y −100) ├─ shadow
                           ├─ bone → bone3 (HÔNG: dời, nghiêng cả thân)
                           │    ├─ bone4 (lưng) → bone5 (NGỰC) ─┬─ bone6 (cổ) → bone7 (ĐẦU, mặt) → bone27 (MŨ)
                           │    │                               │      ├─ bone23→24→25→26   chóp mũ, 4 đốt (58, 39, 22, 17)
                           │    │                               │      ├─ bone31→32→33, bone34→35→36   hai lông vũ trên mũ, 3 đốt
                           │    │                               │      └─ bone37→38, bone39→40, bone41→42   vành mũ: trái, giữa, phải, mỗi bên 2 đốt
                           │    │                               ├─ bone14 (vai P) → bone15 (bắp) → bone16 (cẳng, ống tay áo) → bone17→18 (bàn tay)
                           │    │                               │      ├─ bone53→54→55   gấu ống tay rủ, 3 đốt (con của cẳng tay)
                           │    │                               │      └─ bone30   giáp vai (con của vai)
                           │    │                               ├─ bone19 (vai T) → bone20 (bắp) → bone21 (cẳng) → bone22 (bàn tay) → bone28 (GẬY, dài 192)
                           │    │                               │      ├─ bone43→44→45, 46→47→48, 49→50, 51→52   bốn lông / tua trên đầu gậy
                           │    │                               │      ├─ bone56→57→58   gấu ống tay rủ, 3 đốt
                           │    │                               │      └─ bone29   giáp vai
                           │    │                               ├─ bone59 (gốc ÁO CHOÀNG) ─ bone60→…→64 (mép trái, 5 đốt) ; bone65→…→69 (mép phải, 5 đốt)
                           │    │                               └─ bone89 (gốc VẠT TRƯỚC) ─ bone90→…→93 (mép trái, 4 đốt) ; bone94→…→97 (mép phải, 4 đốt)
                           │    ├─ bone8→9→10    chân P (đùi, ống, bàn chân)
                           │    └─ bone11→12→13  chân T
                           ├─ R2→R1, L2→L1       đích IK hai chân (bàn chân bám đất)
                           ├─ Z1 → SL2 → SL1     Z1 = CHÂN GẬY trên đất; SL2, SL1 = đích IK bàn tay, cánh tay cầm gậy
                           └─ bone98 (+14 xương) GẬY THỨ HAI, rời tay: bản sao gậy và lông để văng đi lúc chết
```

IK: `R1/L1` (đùi + ống, 2 xương), `R2/L2` (bàn chân), `SL1` (bắp + cẳng tay cầm gậy), `SL2` (bàn tay), `Z1` (gậy chĩa về chân gậy).

### Mẹo diễn chính

1. **Gậy cắm đất bằng IK, tay bám gậy**: đích `Z1` ở mặt đất là con của gốc; `SL1/SL2` là con của `Z1`. Thân thở, nghiêng thế
   nào thì chân gậy vẫn đứng yên một chỗ và bàn tay vẫn nắm đúng chỗ đó trên gậy; chỉ cần xoay `Z1` ±2° là gậy đung đưa. Lúc
   vung gậy thì **tắt IK** (mix 1 → 0 ngay khung 0, bước), tay chạy bằng khoá xoay; hạ gậy xong **bật lại** đúng khung chạm đất.
2. **Vải = hai chuỗi xương chạy dọc HAI MÉP tấm vải**, không phải một chuỗi giữa. Áo choàng: gốc `bone59` (hàng đỉnh trên cùng
   bám 100 %) rồi hai chuỗi 5 đốt; vạt trước: gốc `bone89` rồi hai chuỗi 4 đốt. Hai mép vẫy lệch pha nhau nên tấm vải **xoắn,
   lật mép** được chứ không chỉ lắc như lá cờ.
3. **Trọng số áo choàng** (48 đỉnh, 66 tam giác, `mesh.json`): đỉnh mép ở khớp chia 0,5 / 0,5 hai đốt kề; đỉnh mép giữa đốt chia
   0,25 / 0,5 / 0,25; **không đỉnh nào bám 100 % một đốt** trừ hàng đỉnh (gốc) và góc gấu. Đỉnh giữa tấm trộn cả hai chuỗi theo vị
   trí ngang (cột giữa: 0,25 × 4 xương, tức hai đốt kề của mỗi chuỗi); hàng gấu trộn `bone64` ↔ `bone69` tuyến tính theo x
   (0,83 / 0,17 → 0,21 / 0,79).
4. **Sóng lan từ gốc ra ngọn, trễ 5 khung mỗi đốt, biên độ lớn dần**: idle áo choàng mép trái cực trị ở khung 5 / 10 / 15 / 20 /
   25 (đốt 1 → 5), biên độ ±6° → ±12°; chóp mũ 4 đốt cực trị ở 20 / 5 → 25 / 10 → 30 / 15 → 35; ống tay, lông gậy cũng vậy. Mỗi đốt
   chỉ **2 khoá cực trị một vòng** + khoá khép vòng.
5. **Ống tay áo rộng = ảnh ống tay bám cẳng tay + một chuỗi 3 đốt cho phần gấu rủ** (con của cẳng tay): vung tay thì gấu văng trễ.
6. **Vành mũ có xương riêng** (3 chuỗi 2 đốt): thân nhún thì vành mũ dập dờn; chóp mũ là chuỗi riêng 4 đốt.
7. **Đổi thứ tự chồng bằng nhiều ảnh cho một bộ phận**: ống tay phải có 4 ảnh (`xiabiR_01..04`: mặt ngoài, lòng ống, gấu…), khăn
   quàng 2 ảnh, giáp vai phải 2 ảnh: lớp trước và lớp sau của cùng một món đồ kẹp cánh tay ở giữa.
8. Thân ngắn nên chỉ 4 xương dọc (hông, lưng, ngực, cổ); ảnh thân trên bám hông + lưng + ngực; chân IK bám đất, bước lùi khi ra đòn.

### Clip (10)

| Clip | Dài | Ghi chú |
|---|---|---|
| `idle_01` | 1,33 s (40 khung) | một vòng thở; mọi chuỗi vải lắc lệch pha; hông nhún 2 px, bóng co 4 % |
| `skill_01` | 1,17 s (35 khung) | vung gậy lên vai, chĩa ngang ra trước, giữ; trúng ở khung 12 (0,4 s) |
| `skill_02` | 1,53 s (46 khung) | giơ gậy cao, gồng 18 khung, dậm xuống ở khung 25 (0,83 s), giữ, về |
| `hit_01` | 0,50 s | ngực gập −31° ở khung 2, hông lùi 52 px; chân gậy trượt lùi 36 px rồi về |
| `hit_02` | 0,67 s | |
| `die_01` | 1,00 s | bị hất lộn một vòng lên cao (y +257 ở khung 6), gậy rời tay ở 0,2 s bay xoay đi; rơi nằm ở khung 14–17, nảy nhẹ |
| `run_01`, `stun_01`, `floating_01`, `block_01` | 0,53; 1,67; 1,5; 0,5 s | không dùng |

## 3. Khoá gốc sẽ học (khung 30 fps; góc là lệch so với dáng gốc; `x/y` dời). Đủ ở `scan/monster_3313/keys.txt`

```
== idle_01  40 khung                      (mỗi đốt 2 cực trị, trễ 5 khung mỗi đốt)
  Rotate    HONG       0:-1.37  5:-1.79  25:0.832  40:-1.37        Translate HONG  0:7.69/0  20:5.46/1.94  40:7.69/0
  Rotate    NGUC       0:-0.872  15:-2.8  35:-0.504  40:-0.872
  Rotate    co         0:0.899  20:-2.25  35:0.395  40:0.899       Rotate DAU  0:-0.928  15:-0.171  35:-1.07  40:-0.928
  Rotate    chopmu1..4 cực trị 20 | 5→25 | 10→30 | 15→35, biên độ +5.2 ↔ −1.9
  Rotate    vanh mu    trái −5.7 ↔ 0, giữa +13.6 ↔ 0, phải +8.4 ↔ −6.2 (cực trị khung 10 và 30, hai đốt cùng khoá)
  Rotate    choangA1..5  5:+3.7→25:−8.8 | 10:+1.9→30:−1.9 | 15:+1.8→35:−7.1 | 20:+15.1→40:−7.2 | 25:+14.7→5:−13.7
  Rotate    choangB1..5  20:−15.9 | 5:+2.3→25:−4.5 | 10:+4.9→30:−7.8 | 15:+8.3→35:−10 | 20:+16.6→40:−11
  Rotate    vatA1..4   5→25: +0.4 ↔ −4.1 | 10→30: +0.4 ↔ −3.3 | 15→35: +0.4 ↔ −10.2 | 20→40: +0.4 ↔ −10.2
  Rotate    ongR1..3   20:+2.7 ↔ 0:−7 | 25 ↔ 5 | 30:+14.2 ↔ 10:−7      Rotate Z1 (gậy)  0:4  15:1.81  35:4.42  40:4

== skill_01  35 khung                     (IK gậy tắt 0 → 32)
  Rotate    HONG   0:-1.37  2:7.33  10:7.33  11:-4.88  12:-10.1  14:4.03  17:-4.41  23:-10.1  26:-5.43  35:-1.37
  Translate HONG   0:7.69/0  2:5.35/0  10:10.5/0  12:-42.4/-10.3  14:-37/-4.64  17:-38.8/-10.2  23:-41/-13.3  26:-21.7/-7.2  35:7.69/0
  Rotate    NGUC   0:-0.872  2:5.85  10:11.8  11:2.85  12:-0.872  14:-13.1  17:-1.61  23:6.44  26:8.41  35:-0.872
  Rotate    DAU    0:-0.928  2:-5.65  10:-8.47  11:-0.051  12:-3.69  14:-14.7  17:-1.14  20:2.99  23:2.7  26:-9.45  35:-0.928
  Rotate    bapL   0:-25.9  2:88.6  10:101  11:79  12:45.5  14:54.4  17:48.5  23:40.2  26:66.9  32:-1.39  35:-25.9      (tay cầm gậy)
  Rotate    cangL  0:31.4  2:-17  10:-8.09  11:-36.3  12:-37.7  14:-43.5  17:-35.2  23:-31.2  26:-34.7  32:-1.61  35:31.4
  Rotate    tayL   0:-2.84  2:-45  10:-29.9  11:-58.9  12:-88.7  23:-88.7  26:-68.2  32:-0.313  35:-2.84
  Rotate    choangA1  0:1.7  2:-38.3  5:-37.6  10:-22.5  12:-12.1  14:-40.6  17:-8.54  23:-10.1  35:1.7
  Rotate    choangA5  0:-9.13  2:-13.5  5:-5.61  10:35.1  12:-12.9  14:28.3  17:47.3  23:34.7  35:-9.13
  Translate R2 (chân sau)  0:0/0  2:-38.9/0  10:-38.9/0  12:-47.4/0  26:-47.4/0  32:0/0
```
Nhịp `skill_01`: **giật gậy lên vai trong 2 khung** (bắp +89°, hông ngả +7°, chân sau lùi 39 px) → **giữ 8 khung có trôi** (bắp 89
→ 101, ngực 6 → 12) → **khung gãy 11** (cẳng tay bật trước −36°, bàn tay −59°) → **chĩa ra ở khung 12** (hông lùi 42 px ngược
chiều bắn: giật lùi; bàn tay −89° cho gậy nằm ngang) → rung nẩy khung 14 (ngực −13°, đầu −15°) → **giữ tới khung 23 có trôi** →
thu về 26–35, IK bật lại ở khung 32. Áo choàng: gốc văng ngược −38° ngay khung 2, ngọn trễ tới khung 10–17 mới đạt +35..47°.

```
== skill_02  46 khung                     (IK gậy tắt 0 → 25, bật lại đúng khung dậm)
  Rotate    HONG   0:-1.37  4:17  22:15  24:2.51  25:-8.8  27:7.57  30:-5.18  36:-8.75  41:-0.056  46:-1.37
  Translate HONG   0:7.69/0  4:2.15/7.67  22:2.15/14.6  24:12.2/1.07  25:6.05/-23.7  27:6.05/-4.41  30:6.05/-10.6  36:6.05/-17.6  41:-3.25/-1.33  46:7.69/0
  Rotate    NGUC   0:-0.872  4:-10.3  22:2.31  24:-0.164  25:-22.3  27:-31.9  30:-10.4  36:-10.3  41:-12  46:-0.872
  Rotate    bapL   0:-25.9  4:124  10:140  16:124  22:140  24:111  25:30.4  26:18.2  27:13.2  36:8.65  46:-25.9
  Rotate    cangL  0:31.4  4:-55.1  8:-59.4  13:-42.7  18:-58.4  22:-34.3  24:-32.2  25:54  26:50.8  27:36.3  36:45.3  46:31.4
  Rotate    choangA1  0:1.7  4:-27.7  10:-45.4  15:-23.5  22:-18.8  25:-20.3  27:-52.9  30:-25.2  36:-4.76  41:-3.64  46:1.7
  Rotate    choangB1  0:-7.67  4:7.18  10:-0.807  15:-14.3  22:-21.2  24:20.5  25:72.6  27:85.5  30:41.2  36:8.2  41:19.9  46:-7.67
  Rotate    Z1     0:4  22:4  25:-4.49  26:-2.48  27:-4.49  36:-2.65  41:-1.6  46:4        Translate Z1  25:0/0  26:0/3.84  27:0/0
```
Nhịp `skill_02`: **giơ gậy cao trong 4 khung** (bắp +124°, hông ngả +17°, nhón lên 8 px) → **gồng 18 khung**: bắp đổi 124 ↔ 140
mỗi 6 khung, cẳng tay và gấu ống tay rung ngược pha, hông nhón dần 8 → 15 px, áo choàng phồng −45° rồi xẹp → **khung gãy 24** →
**dậm ở khung 25 (0,83 s)**: hông sụp −24 px, ngực gập −22° rồi −32° ở khung 27, **chân gậy nẩy lên 3,8 px đúng một khung** (26),
mép áo choàng phải bật +73..85° (áo tung lên vì cú dậm) → giữ dáng dậm tới khung 36 (trôi 3–7°) → về 10 khung.

```
== die_01  30 khung                       (gậy đổi sang bản rời ở khung 6; mọi IK giữ)
  Rotate    HONG   0:20.5  2:66.6  6:81  10:136  14:182  17:70  20:95  23:112  26:96.2  30:102
  Translate HONG   0:7.69/77.1  2:33.1/171  6:44.8/257  10:14.4/246  12:19.3/184  14:24.1/39.8  17:60/20.2  20:75.1/2.69  23:75.1/1.13  30:75.1/0.291
  Rotate    GAY2   6:0  10:117  14:162  17:197  21:248  24:259  27:280  30:271      Translate GAY2  6:-401/363 … 17:-401/307  21:-401/-136  30:-401/-164
== hit_01  15 khung
  Translate HONG   0:-39.3/-11.1  2:-52.4/-30.8  6:-39.5/-21.3  10:-24.2/-5.39  15:7.69/0
  Rotate    NGUC   0:3.23  2:-31.4  6:-18.9  10:-20.6  15:-0.872         Rotate DAU  0:-0.928  2:14.9  6:-16.2  10:-26.2  15:-0.928
  Rotate    choangA1  0:-45.4  2:-44  6:-17  10:5.75  15:1.7             Rotate choangA5  0:-22.4  2:30.1  6:48.5  10:45.6  13:-25.5  15:-9.13
  Translate Z1 (chân gậy)  0:-35.6/0  10:-35.6/0  12:-18.1/13  13:0/0     (gậy trượt lùi theo người rồi nhấc lên cắm lại)
```

## 4. Kế hoạch rig của mình (sau khi duyệt concept)

Rig thẳng từ concept, không tờ mảnh (skill mục 22: tô phẳng nên chỗ khuất tô lại bằng vân sáp lát). Lớp (sau → trước):

| Lớp | Xương | Ghi chú |
|---|---|---|
| áo choàng (dựng **cả tấm**, phần khuất sau áo lát vân chàm) | gốc ở vai + **hai chuỗi mép, mỗi chuỗi 5 đốt** | trọng số như con gốc: mép 0,5 / 0,5 và 0,25 / 0,5 / 0,25, giữa tấm trộn hai chuỗi theo x; lò xo nướng, chặn góc |
| tay áo trái (buông) | bắp, cẳng + **gấu 3 đốt** | không bàn tay |
| hai mũi giày | bám đất (con của `move`) | áo co giãn phía trên |
| áo dài chuông | hông, lưng, ngực + **gấu áo hai chuỗi 3 đốt** (mép trái, mép phải) | thay cho hai chân của con gốc: nhún, sụp thì gấu xoè |
| vạt trước | gốc ở ngực + **hai chuỗi mép 4 đốt** | lật mép khi dậm gậy |
| khăn vai | ngực (cứng 70 %) + 2 xương mép trái, phải | nẩy khi vung tay |
| gậy + hạt treo (2 chuỗi 2 đốt) | `gay` dài, con của bàn tay; **IK một xương về `chan_gay` trên đất** | xương `mieng` ở quả cầu nước (chỗ nhả tia), trục x chĩa theo đầu gậy |
| tay áo phải + bàn tay | bắp, cẳng (IK hai xương về điểm nắm trên gậy), bàn tay, **gấu 3 đốt** | tắt IK khi vung, bật lại khi cắm; nướng nên chỉ cần giải IK trong mã |
| khoảng tối dưới mũ | đầu | |
| mũ | `dau` → `mu`; **chóp 4 đốt**, **vành 3 chuỗi 2 đốt**, **hai dải đai 3 đốt** | hạt cam ở chóp cứng theo đốt cuối |

Clip (tên game → nguồn nhịp):

- `idle` 2,67 s (2 vòng 1,33 s của con gốc; vòng hai có điểm phá nhịp: nghiêng mũ, cầu nước nẩy) — gậy cắm đất bằng IK.
- `attack` = nhịp `skill_01`: giật gậy lên vai, chĩa ngang, **giữ tới `phun` + 0,94 s thật** (dòng tia của game chảy 0,88 s), giật
  lùi ngược chiều bắn. Sự kiện `phun`, `het_phun`; `game.muzzle` = quả cầu nước ở khung nhả. Đứng tại chỗ (`stay`).
- `cast` = cùng động tác, khác nhịp nhẹ (xoay cổ tay vẽ một vòng nhỏ trước khi chĩa) để lớp VFX đổi kiểu tia.
- `skill` = nhịp `skill_02`: giơ gậy, gồng (sự kiện `trieu_hoi`: kim nước hiện quanh gậy do VFX), dậm (sự kiện `dam` = lúc kim
  phóng đi), giữ dáng dậm tới khi kim bay hết.
- `hit` = `hit_01`. `die`: đề xuất **sửa** so với con gốc: bị hất, gậy văng, rồi **áo mũ xẹp xuống thành đống, mũ úp lên trên**
  (bên trong không có gì) — giữ kiểu hất lộn của con gốc thì áo chuông không chân sẽ lộ đáy trống.
- `appear`: vòng tròn triệu hồi hiện trên đất (ảnh gen ở lượt 2, elip nằm, xoay), tướng **trồi lên qua mặt nạ cắt ở mặt đất**
  (như Hải Long trồi từ nước), vòng tan. `evolve` gộp dạng 2 bản nhẹ.
- Dạng 2 gộp tiến hóa: bản nhẹ (ảnh 0,6 lần, lưới thưa 1,8 lần) để dạng 1 ≤ 0,5 MB.

VFX (bước sau, ngoài rig): đòn thường / mana `n_tia` hai kiểu; chiêu cuối `n_thuong` (kim nước) phát theo `trieu_hoi` → `dam`.

## 5. Đã làm (2026-11-11, bản đầu chờ người dùng xem chuyển động)

Concept hai dạng đã duyệt / đã gen: `inbox/phap_su_1/tai_ve/L1_duyet.png` (người dùng duyệt), `inbox/phap_su_2/tai_ve/L1_duyet.png`
(gen theo lời dặn "cao lớn hơn là được", người dùng chưa xem); vòng tròn triệu hồi `inbox/phap_su_1/tai_ve/V01.png`.
Script: `ArtGen/Spine/phap_su.py` (`cat k`, `thu k`, `xem k clip khung,... [phóng]`, `rig k`, `all`).

- **Cắt lớp thẳng từ concept, không tờ mảnh**: vùng = mảng liền không mực chứa hạt giống (`CFG[k]["hat"]`); nét mực trong 9,5 px
  của vùng thuộc lớp đó (nét chung thuộc cả hai lớp), mực xa mọi vùng theo vùng gần nhất. 14 lớp (sau → trước): áo choàng (cả
  tấm), tay áo xa, gậy, hai dây treo hạt, bàn tay, giày, áo, vạt, tay áo gần, khoảng tối, khăn vai, mũ, dải đai. Phần khuất lát
  vân sáp cùng màu (`them_lop`): nét chung với lớp nằm TRƯỚC thì tô lại, nét chung với lớp nằm sau thì giữ. Ghép lại so concept:
  IoU hình bóng 0,994 cả hai dạng.
- **Rig** 71 xương mỗi dạng: áo choàng 2 × 5 đốt (mép ngoài + ranh với áo, trộn theo vị trí ngang như con gốc), vạt trước 2 × 4,
  gấu áo 2 × 3, chóp mũ 4, vành mũ 2 × 2, dải đai 2 × 3, tay áo gần 3, tay xa 2 + gấu ống tay 2, dây treo hạt 2 × 3. Tay cầm gậy
  giải IK trong mã (`tay_gay`): gậy cắm đất thì chân gậy đứng yên, tay bám gậy; vung gậy thì hoà sang vị trí tay khoá trong hệ
  ngực; với không tới thì giãn tay (bàn tay, gậy giữ cỡ).
- **Vải rũ theo trọng lực bằng động học**: thân nghiêng thì gốc áo choàng, tay áo buông, vạt trước xoay bù; gậy nghiêng thì gốc
  hai dây treo hạt xoay bù đúng góc gậy (`hat_ru`), lò xo `LoXo` chỉ thêm độ trễ. (Đã thử `DayMem` có trọng lực cho dây hạt: giật
  1–2 khung ở idle, bỏ.)
- **Mặt nạ cắt ở mặt đất chỉ dùng cho clip `appear`**: dáng gốc mép cắt nằm dưới đất 0,6 H (xương `goc_cat`), `appear` nâng lên
  đúng mặt đất rồi hạ lại sau khi trồi xong. Để mép cắt cố định ở mặt đất thì áo choàng, gấu áo lúc vung bị xén ngang.
- **Vòng triệu hồi**: ảnh tròn trên xương `vong_x` (xoay), cha `vong` co dẹt theo y TRONG CLIP (không đặt tỉ lệ ở dáng gốc: mảnh
  đặt theo toạ độ thế giới dáng gốc nên tỉ lệ dáng gốc bị bù mất, vòng thành elip lật vòng vòng).
- Dung lượng: dạng 1 gộp tiến hóa 381 KB, dạng 2 263 KB (trần 0,5 MB). Mọi clip nối về idle lệch 0 px; `.atomik` nạp lại lệch
  khung 0 0,05 px.
- Clip (dạng 1; dạng 2 chậm 1,12 lần): `idle` 2,67 s; `attack` 1,2 s (trung / phun 0,40 s); `cast` 1,97 s (phun 0,53 s, giữ tới
  1,53 s); `skill` 1,83 s (trieu_hoi 0,13 s, dam 0,83 s); `hit` 0,5 s; `die` 1,53 s; `appear` 1,27 s (cham_dat 0,77 s); `evolve` 2,8 s.

Chưa làm: xem ở tốc độ thật (mới soi tờ khung và ảnh cận); vào Unity (chưa có tên, suất trên đảo, chỉ số, thẻ); nối VFX (tia đòn
thường / mana ở xương `mieng`, kim nước theo `trieu_hoi` → `dam`); game chưa phát `appear`, `die`.

## 6. Góp ý lần 1 của người dùng (2026-11-11, xem trang web dạng 2 lúc giơ gậy)

- **"Tay gần nách cầm gậy bị rách"**: ống tay áo xa vẽ thẳng (không có khuỷu) nhưng rig hai đốt giải IK có khuỷu → lúc giơ gậy khuỷu gập,
  ống tay gấp chồng lên nhau, cổ tay áo lật. Đổi thành **một xương vai → bàn tay, xoay quanh vai và co giãn dọc trục** (0,5–1,6 lần);
  bàn tay + gậy thành con của `nhun` (đặt vị trí, góc mỗi khung), không nhận co giãn của tay áo, của thân. Phần tay áo khuất ở vai
  kẻ viền mực và làm mượt mép. Còn một mép gồ nhỏ (~15 px) sát thuỳ khăn vai lúc tay giơ cao.
- **"Chiêu cuối cho nó khua khua cái đũa nữa"**: lúc gồng (0,13 → 0,93 s) gậy nghiêng qua lại ±19°, ba nhịp 8 khung, bàn tay đưa theo,
  đầu gậy vẽ số 8 trên mũ; thân, mũ, áo choàng, vạt, tay áo đung đưa trễ theo. `dam` dời từ 0,83 s sang 1,03 s (dạng 1).
- Dọn thêm: vệt nối mảnh quanh chỗ vạt / tay áo cũ trên lớp áo (nới vùng tô 2 px), mẩu nét viền giày dưới gấu áo.

## 7. Góp ý lần 2 (2026-11-11): "vẫn thấy bị rách, cả dạng 1 cũng bị tách khỏi áo choàng"

Lần sửa trước (một xương co giãn) chưa đúng gốc: cả ống tay vẫn xoay cứng quanh vai, mà mép dưới của ống tay ở chỗ nách nằm thấp
hơn vai 90 px nên tay giơ lên là mép đó văng ra, hở nền giữa tay áo và thân. Sửa gốc: **đường nách** (`CFG["nach"]`: từ mép khăn
vai xuống mép áo) bám 100 % ngực; từ đó ra cổ tay chuyển dần sang xương tay trong `nach_hoa` px. Tay giơ thì vải giãn giữa nách
và cổ tay như ống tay rộng thật, không mép nào rời thân. Kiểm bằng **runtime Spine thật** (`mo_xe/chay.py sheet ... view=` phóng
vào vai, 10 khung mỗi clip skill / attack / cast / hit, cả hai dạng): bộ vẽ Python cỡ nhỏ không cho thấy lỗi này.

Sửa kèm: cổ tay áo xa khép kín phần bị gậy che (bao lồi, tô lam băng, viền mực); dạng 2 gậy dài nên lúc chĩa ngang đuôi gậy xuyên
qua người lòi ra bên kia → gậy **trượt trong bàn tay** về phía đầu gậy (`truot` = dài đuôi gậy − 150·S); gấu phần khuất của áo
choàng dạng 2 có nét mực và dải cam. Còn: chỗ nối gấu thấy / gấu khuất của áo choàng lệch một bậc nhỏ; mép trái khuất của áo
(sau tay áo buông) còn vết khuyết vài px lúc tay áo buông lắc mạnh.

## 8. Vào game (2026-11-11, người dùng: "ổn rồi ghép vào game đi")

- **Suất**: tướng thứ 6 đảo Thủy = ải 30 = id game **`giong_bao`** (theo thứ tự suất của lô: ti_tach, thach_giai, ca_den, ha_ba,
  so_ngoc, giong_bao...; trước là kỳ giông "Giông Bão", rig `tm06`). **Giữ nguyên id** như cách ếch xanh vào suất `thach_giai`:
  không đụng `heroes.json`, `cards.json`, `stages.json`, test, golden. Tên tướng, danh hiệu, tên dạng, tên ba thẻ trong game **vẫn
  là của con kỳ giông** (Giông Bão; Giông Mưa / Giông Bão; Bầu Phun, Cầu Mưa, Bầu Hứng Mưa): chờ người dùng đặt (đổi id + tên theo
  mẫu `quai/doi_ca_den.py`).
- Đã làm (Unity Editor lúc đó không mở):
  - `quai/da_nhan.json`: mục `giong_bao` trỏ sang `inbox/phap_su_1|2/rig`.
  - Chép tay `phap_su_<k>.atomik` → `Assets/03 Art/Heroes/Resources/giong_bao_<k>/giong_bao_<k>.atomik`, `chan_dung.png` →
    `giong_bao_<k>_portrait.png` (`.meta`, `.asset` giữ nguyên). `vao_game.py --kiem`: hai dạng "giữ", đủ clip, `game` có; cảnh báo
    quen thuộc `game.shadow 'shadow' không có slot đó`.
  - `StageView.WaterFx["giong_bao"]` = chiêu mana `n_tia`, chiêu cuối hai dạng `n_thuong` (kim nước: tụ thành vòng cung trên đầu
    trong lúc lấy đà = lúc giơ gậy khua, tới khung `dam` thì phóng lần lượt 8 mũi × 0,1 s). `HatNuoc.WThemes["giong_bao"]`: màu
    nước chàm / lam ngọc / lam băng, bỏ họa tiết mây.
  - Clip `skill` thêm sự kiện `het_dam` (sân không ghìm ở khung dậm, clip tự giữ dáng dậm 0,87 s cho đủ loạt kim rồi về).
- Chưa làm: mở Unity cho nó nhập lại hai `.atomik` và biên dịch (hai chỗ sửa C# chỉ đổi chuỗi và màu); xem trong trận ải 30, hộp
  chi tiết, nút Tiến hóa; EditMode test. **Đòn đánh thường chưa có tia nước**: sân chưa vẽ đạn cho đòn thường của rig đứng yên
  (chỉ có hiệu ứng trúng ở đối thủ); muốn có tia ngắn thì thêm ở `StageView` (đọc sự kiện `phun` + xương `mieng`).

## 9. Hiệu ứng trong game (2026-11-11, người dùng: "làm nốt tia nước / các fx cần thiết, nhớ cho vào tướng")

| Động tác | Hiệu ứng | Nối ở đâu |
|---|---|---|
| đòn thường (`attack`, đứng yên) | **đạn nước `n_dan`** (mới): một viên nước thon rời cầu nước đầu gậy ở khung chĩa (`phun`), bay 0,13 s, chạm thì chớp toé nhỏ + 6 giọt + 2 bọt | `HatNuoc.NDan`, `StageView.WaterAtk["giong_bao"]` → `AtkFx` (gọi từ `PreFx` khi clip là attack và rig khai `stay`); ô xem tướng: `HeroViewer.PreFx` |
| chiêu mana (`cast`) | tia nước liền `n_tia` 0,88 s từ cầu nước (khác kiểu đòn thường: dòng liền thay vì một viên) | `WaterFx["giong_bao"].mana` (có sẵn) |
| chiêu cuối (`skill`) | kim nước `n_thuong`: 8 mũi tụ vòng cung trên đầu lúc giơ gậy khua, phóng lần lượt từ khung `dam` | `WaterFx["giong_bao"].ult` |
| ra sân, chết | vòng tròn triệu hồi, áo mũ xẹp: nằm trong rig; sân tự phát clip `appear` / `die` của rig có hai clip này (`StageView` `rigEnter`, `rigDie`) | có sẵn |

- **Giờ trúng của `attack`** trong rig = khung chĩa gậy + 0,13 s (`DAN_BAY` = `HatNuoc.DanTravel`): đạn rời đầu gậy đúng khung chĩa
  và chạm đối thủ đúng `game.hitTimes`, nên số sát thương, khựng, rung của sân không phải dời (dạng 1: 0,53 s; dạng 2: 0,578 s).
- Chỗ nhả của đạn = `game.muzzle` (xương `mieng` ở khung nhả của `cast`; `attack` cùng dáng chĩa).
- Thêm tướng Thủy khác bắn đạn ở đòn thường: rig khai `stay` cho attack, đặt giờ trúng = khung nhả + 0,13 s, thêm một dòng vào
  `StageView.WaterAtk`.
- Kiểm: biên dịch thử assembly `PokiClash.Game` ngoài Unity bằng csc của Unity (162 file): 0 lỗi. `vao_game.py --kiem`: hai dạng
  đủ clip. **Chưa xem trong Unity** (Editor không mở): chưa thấy đạn, tia, kim trong trận và trong hộp chi tiết; chưa chạy EditMode test.
