# Dòng cá voi biến dị (mã làm việc `ca_voi`): tướng thứ 7 đảo Thủy (2026-11-11)

Người dùng lên ý tưởng và duyệt concept (chưa đặt tên; mã `ca_voi` chỉ để đặt thư mục); mảnh, rig Claude tự làm.
Gói prompt: `ArtGen/Spine/build_ca_voi.py` → `gui_gpt/ca_voi_<k>/`, ảnh về `inbox/ca_voi_<k>/tai_ve/`.
Sơ đồ bố cục tự vẽ: `ArtGen/Spine/ca_voi_bo_cuc.py` → `inbox/ca_voi_<k>/mau/bo_cuc.png`.

## 1. Ý người dùng (nguyên văn tóm lại)

- Dựa trên con gốc `monster_3281` (game tham khảo). Concept: **cá voi biến dị, không có mặt như con gốc**; **bỏ sừng**; **cuối
  đuôi thay bằng kiểu đá đen dưới biển gắn vào đuôi** (na ná mấy viên pha lê của con gốc).
- **Con gốc lấy làm dạng 2; phải làm thêm dạng 1.**
- `idle`, `die`: làm giống con gốc.
- Đòn thường: giống `skill_01`, **lao tới cắn đớp mạnh**.
- Chiêu mana: **lao tới quật đuôi** vào kẻ địch.
- Chiêu cuối: giống `skill_02`, **há to mồm bắn một luồng nước siêu to** (luồng nước là VFX, rig không vẽ).
- `appear`: **rơi từ trên trời xuống mạnh (lắc cam nhẹ), sau đó chống chân đứng dậy**.
- Mỗi dạng tối đa **0,5 MB**.

Người dùng không dặn màu. Màu trong concept là **đề xuất của Claude**, chờ duyệt (tránh bảng màu trắng + tím của con gốc):

| | Dạng 2 (bám con gốc) | Dạng 1 (cá voi con) |
|---|---|---|
| Lưng, hàm trên, đuôi, chân | lam đá sẫm `#2F4A6E` | lam biển `#4F86B0` |
| Hàm dưới, bụng | trắng băng `#E6F1F4`, rãnh họng `#8FB8CC` | như dạng 2 |
| Lòng miệng | hồng san hô `#E2607A` (một màu phẳng) | hồng nhạt `#F08A96` |
| Nanh | kem `#FBF1D2`, 10 cái (5 trên, 5 dưới) | 6 cái nhỏ (3 trên, 3 dưới) |
| Đá đuôi, móng | đen than `#26252C`, mặt cắt xám `#5A5866`; 3 mảnh | 2 mảnh nhỏ |
| Nét cá voi | rãnh họng trên bụng, lỗ phun trên đỉnh đầu | như dạng 2 |

## 2. Cách dựng hình của con gốc phải giữ (đọc trên ảnh cận `scan/monster_3281/can/idle_01.jpg`)

- **Nhìn ba phần tư, quay sang phải và hơi ra phía người xem**: miệng ở bên phải, đuôi bên trái; nhìn thẳng vào lòng miệng.
- **Không có mặt**: không mắt, mũi. Cả đầu là **một cái miệng tròn** (bầu dục đứng, cao gần bằng cả đầu), viền quanh là 10 nanh to
  (5 trên thả xuống, 5 dưới dựng lên), gốc nanh đè ra ngoài mép môi, mũi chĩa vào tâm.
- **Dáng hình nêm**: cao nhất ở đầu (phải), lưng là một đường chéo gần thẳng chạy xuống đuôi mảnh (trái); bụng sát đất.
- **Thân chính là hai cái hàm**: hàm trên (vòm) và hàm dưới (bát) dài gần hết thân, bản lề nằm sâu trong thân, ngay trên chân sau.
- **Chỉ hai chân**: chân sau bên gần (đùi trắng viền riêng đè lên thân, ba móng sẫm) ở giữa thân; chân trước bên xa nấp sau cằm,
  chỉ lộ ống chân xám và ba móng ở dưới phải.
- **Đuôi mảnh ngắn** lơ lửng trên đất, có khoanh sọc; chót là cụm ba tinh thể (một dài chĩa trái, hai ngắn xoè) → của mình là ba
  mảnh đá đen.
- Hai sừng trên vòm hàm trên → bỏ.

## 3. Mổ xẻ con gốc `monster_3281` (chỉ học cấu trúc và nhịp, không lấy hình)

Nguồn: `D:\Ripper\SwordxStaff\web\assets\Monster\monster_3281\` (Spine 4.2.28, skel 27 KB + ảnh 80 KB). Kết quả quét:
`D:\Ripper\SwordxStaff\scan\monster_3281\` (`info.json`, `att_goc.json`, `keys.json`, `keys.txt` = khoá 6 clip đọc được, `mesh.json`,
`manh_anh.png` = 28 ảnh mảnh, `manh_dang_goc.png` = từng mảnh trong dáng gốc, tờ khung `khung/<clip>.jpg`, ảnh cận `can/`, `can2/`).

### Bảng mảnh (28 hình, thứ tự vẽ sau → trước)

| # | Con gốc | Là gì, bám xương nào | Của mình (dự kiến) |
|---|---|---|---|
| 1, 2 | `P_tuiL01` 48 × 56, `P_tuiL02` 57 × 56 | **chân trước bên xa** (xám nhạt): đùi + ống, chuỗi `bone13 → 14 → 15`, IK `L1`, `L2` | `chan_x_dui`, `chan_x_ong` |
| 3–5 | `P_tuiL03..05` ~25 × 25 | ba móng chân xa, cứng theo `bone15` | `mong_x1..3` |
| 6 | `P_jiao01` 60 × 99 | sừng xa, cứng theo hàm trên | bỏ |
| 7 | `P_ci03` 38 × 71 | tinh thể đuôi (sau đuôi), xương riêng `bone8` | `da_3` |
| 8 | `P_weiba` 107 × 98 | **mông + đuôi**: lưới bám `bone2` (thân), `bone4 → 5 → 6 → 7` (đuôi 4 đốt) | `duoi` |
| 9 | `P_mouth02` 184 × 109 | **hàm dưới + bụng + LÒNG MIỆNG** (cả cái bát, mảng tím trong miệng nằm trên mảnh này); lưới bám `bone11` (hàm dưới), `bone2`, `bone4`, `bone5` | `ham_duoi` |
| 10 | `P_ya08` | nanh dưới trong cùng, vẽ SAU hàm trên; xương riêng `bone28` | `nanh_d5` |
| 11 | `P_mouth01` 185 × 108 | **hàm trên + vòm miệng** (vòm trắng, mảng tím vòm họng ở mặt dưới); lưới bám `bone3` (hàm trên), `bone2`, `bone4`, `bone11` | `ham_tren` |
| 12–17 | `P_ya05, 10, 09, 07, 06, 04` | nanh dưới (4) + nanh trên trong cùng (2), **mỗi nanh một xương riêng** (`bone23..27`, `bone22`) | `nanh_*` |
| 18, 19 | `P_tuiR02` 42 × 59, `P_tuiR01` 56 × 61 | **chân sau bên gần** (trắng): ống + đùi, chuỗi `bone16 → 17 → 18`, IK `R1`, `R2` | `chan_g_ong`, `chan_g_dui` |
| 20, 21, 24 | `P_tuiR05, 04, 03` | ba móng chân gần, cứng theo `bone18` | `mong_g1..3` |
| 22, 23 | `P_ci02`, `P_ci01` | hai tinh thể đuôi trước, xương riêng `bone10`, `bone9` | `da_2`, `da_1` |
| 25 | `P_jiao02` 106 × 119 | sừng gần, cứng theo hàm trên | bỏ |
| 26–28 | `P_ya03, 02, 01` | ba nanh trên ngoài cùng, mỗi nanh một xương (`bone19..21`), vẽ trên cùng | `nanh_t1..3` |

### Xương (35) và ràng buộc

```
root → bone (y −50)
  ├─ bone12 (TÂM THÂN: dời, xoay cả con) → bone29 (bản lề, giữa thân trên chân sau)
  │     ├─ bone2 (50, 43°) → bone3 (125): HÀM TRÊN  ├─ bone19..23: năm nanh trên (mỗi nanh một xương)
  │     ├─ bone11 (139, −15°): HÀM DƯỚI             └─ bone24..28: năm nanh dưới
  │     ├─ bone4 → bone5 → bone6 → bone7: ĐUÔI 4 đốt (50, 40, 30, 34) → bone8, bone9, bone10: ba tinh thể
  │     ├─ bone13 → bone14 → bone15: chân trước (xa), IK tới L1 / L2
  │     └─ bone16 → bone17 → bone18: chân sau (gần), IK tới R1 / R2
  ├─ L2 → L1, R2 → R1 (đích IK bàn chân, con của gốc: chân bám đất khi thân nhún)
  └─ shadow
```
4 IK (mỗi chân: 2 xương + 1 xương bàn). Không path, không physics, không sự kiện, không đổi ảnh.

### Mẹo diễn chính

1. **Cả con là hai hàm bản lề giữa thân**: `bone3` (hàm trên) và `bone11` (hàm dưới) xoay ngược chiều nhau quanh bản lề `bone29`.
   Há to = hàm trên ngửa +44°, hàm dưới hạ −40° (lòng miệng trên mảnh hàm dưới + vòm họng trên mảnh hàm trên tự lộ ra, không đổi ảnh).
2. **Nanh xoè**: khi há cực đại (`skill_02`) từng nanh xoay 85–177° quanh gốc và dời ra mép, chĩa ra ngoài như cánh hoa.
3. **Chân bám đất bằng IK**; thân (`bone12`) dời / xoay tự do phía trên; lúc lấy đà đích IK lùi 31 px (bước chân).
4. **Đuôi 4 đốt vẫy to liên tục** (đốt gốc ±12°, đốt ngọn ±60°, cực trị trễ 4–8 khung mỗi đốt), ba tinh thể lắc riêng ±20°.

### Clip (10)

| Clip | Dài | Ghi chú |
|---|---|---|
| `idle_01` | 1,00 s lặp | thân lắc ±8° + dời vòng; hai hàm hé ra khép vào 2 lần mỗi vòng (trên −5,6°, dưới +10,7°); đuôi quất cao |
| `skill_01` | 1,00 s | **cắn**: nhổm lùi + há dần 3 → 14 (hàm trên +44°, dưới −40°, thân lùi 88 px, ngửa 25°) → khung 16 **sập** (hàm trên −50°, thân lao +126 px trong 2 khung) → khung 18 quá đà, nảy → 22–26 giữ ngậm → 30 về |
| `skill_02` | 1,17 s | **há phun**: rạp xuống ngậm miệng 3 → 10 (thân lùi 34 px, cúi −32°) → khung 12 **bật há cực đại** (hàm dưới −42°, trên +21°, nanh xoè) → 12 → 26 **giữ rung** (thân nhấp nhô 3–17 px mỗi 2 khung, hàm ±3°) → 30 sập → 35 về |
| `hit_01` | 0,50 s | bật ngửa (thân +33° ở khung 2), há miệng −35°, chân trước nhấc khỏi đất (đích IK lên 190 px) rồi rơi về |
| `die_01` | 1,00 s | hất tung lên (y +210), lộn 165°, rơi ngửa lưng xuống ở khung 15–16, nảy, nằm ngửa giãy chân |
| `run_01` | 0,53 s | chạy hai chân, thân nhún 2 nhịp |
| `hit_02`, `stun_01`, `floating_01`, `block_01` | | chưa dùng |

## 4. Khoá gốc sẽ học

Đủ ở `D:\Ripper\SwordxStaff\scan\monster_3281\keys.txt` (khung 30 fps; góc lệch so với dáng gốc). Tóm tắt nhịp:

```
== skill_01 (cắn) 30 khung
  bone12 (thân) dời   0:-16/-3  3:-7/21  14:-88/1  16:38/-19  18:-14/-28  22:-15/-20  26:-2/10  30:-16/-3
  bone12 xoay         0:-5  3:-3  14:25  16:7  18:-27  22:-11  26:6  30:-5
  bone3 (hàm trên)    0:0  3:3  14:44  15:27  16:-50  18:-25  22:-28  26:-27  30:0
  bone11 (hàm dưới)   0:0  3:-4  14:-40  15:-29  16:-10  18:17  20:13  22:7  30:0
== skill_02 (há phun) 35 khung
  bone12 dời          0:-16/-3  3:-23/-21  10:-50/-24  12:20/17  14:20/3  16:20/16  18:20/5  20:20/13  22:20/6  24:20/10  26:20/3  30:7/-7  35:-16/-3
  bone12 xoay         0:-5  3:-7  10:-32  12:16  26:11  35:-5
  bone3               0:0  3:-25  10:-31  12:21  14:26  16:23  18:27  20:24  22:31  24:30  26:34  30:-8  35:0
  bone11              0:0  10:8  12:-43  14:-47  16:-44  18:-47  20:-44  22:-49  24:-47  26:-50  30:0  35:0
  nanh (bone19..28)   10:0  12:±85..177 (xoè)  26:giữ  30:về
```

## 5. Kế hoạch clip của mình (sau khi duyệt concept)

| Clip | Ý người dùng | Dựng |
|---|---|---|
| `idle` | như con gốc | thân lắc + dời vòng, hai hàm hé – khép, đuôi 4 đốt quất trễ pha, đá lắc riêng; điểm phá nhịp: táp miệng một cái |
| `attack` | lao tới cắn đớp mạnh (`skill_01`) | nhổm lùi há to → sập hàm trong 2 khung lúc lao tới → nảy → giữ ngậm → về; sự kiện `trung` |
| `cast` | lao tới quật đuôi | lao tới, xoay thân vung đuôi qua đầu / quét ngang, đá đuôi đập xuống đúng `trung`; về |
| `skill` | há to bắn luồng nước siêu to (`skill_02`) | rạp xuống ngậm → bật há cực đại, nanh xoè → giữ rung tới hết luồng (`phun` + thời lượng tia) → sập → về; xương `mieng` ở tâm miệng, sự kiện `phun`, `het_phun` |
| `appear` | rơi từ trời xuống mạnh, chống chân đứng dậy | rơi ngửa / nghiêng → đập đất nén bẹp (sự kiện `rung` cho lắc cam) → nằm bẹp một nhịp → chống hai chân đẩy thân lên → lắc mình → dáng đứng |
| `hit`, `die` | die như con gốc | hit bật ngửa há miệng; die hất tung lộn ngửa, rơi lưng xuống, giãy rồi nằm |
| `evolve` (dạng 1) | | gộp bản nhẹ của dạng 2 |

Lắc cam lúc `appear`: rig chỉ phát sự kiện; phần rung màn do game làm (cần nối ở `StageView`, xem `quai/VAO_GAME.md` mục 6:
`appear` / `die` hiện chưa được trận phát).

## 6. Concept đã chốt và rig dạng 2 (2026-11-11 chiều)

Góp ý của người dùng về concept, theo thứ tự:
1. Bản đầu (miệng đĩa tròn, nanh tam giác đều): "nhìn sơ sài quá, bạn nhìn lại con gốc đi" → soi lại ảnh cận đầu / đuôi con gốc, vẽ lại
   sơ đồ bố cục theo toạ độ đọc trên ảnh cận (miệng quả trứng có khoé nhọn, nanh rất to cong đan cài, lòng miệng hai tông, dải sóng
   bụng, đá nhiều mặt cắt).
2. Bản hai: "bỏ mấy sọc trắng đi, phần đuôi làm đừng bị cụt lủn kiểu vậy, có thể đổi đuôi thành giống đuôi cá voi thật, 2 chân có
   thể đổi thành vây cá voi cũng được hoặc làm thế nào để kết nối giữa các móng với chân" → bỏ mọi khoanh / vệt trắng; đuôi dài thon
   dần, chót là **vây đuôi cá voi hai thuỳ bằng đá đen**; hai chân thành **hai vây ngực làm chân chống**, đầu vây chia ba mấu ôm gốc
   ba móng đá.
3. Bản ba (`inbox/ca_voi_2/tai_ve/L1_duyet.png` = `L1_concept_3.png`): "ok tạm ổn" → chốt dạng 2.
Dạng 1 (cá voi con) gen lại theo dạng 2 đã chốt: `inbox/ca_voi_1/tai_ve/L1_concept_2.png`, **chờ người dùng duyệt**.

Rig dạng 2: `ArtGen/Spine/ca_voi.py` (`cat 2`, `rig 2`) → `inbox/ca_voi_2/manh/`, `inbox/ca_voi_2/rig/` (`xem.html`, `khung_<clip>.png`).
- Mảnh chia theo con gốc (bảng mục 3), sau → trước: `vay_x` (vây xa + móng), `vay_duoi` (vây đuôi đá, hai thuỳ hai xương), `duoi`
  (mông + cuống đuôi 5 đốt + mẩu đá), `hong` (vách họng tím tô bằng mã, căng giữa hai hàm khi há), `ham_duoi` (bát + bụng + dải sóng +
  sàn miệng), `ham_tren` (vòm + dải môi + vòm họng + hà), 5 nanh dưới, 6 nanh trên (concept có 11 nanh; mỗi nanh một mảnh cứng một
  xương), `vay_g` (vây gần + móng).
- Chỗ khuất tô bằng hình học khai trong `CFG` (mép miệng trên / dưới sau gốc nanh, mép ngoài dải môi, ranh hai tông, phần hàm dưới
  khuất sau vây gần), vân sáp lát từ chỗ sạch cùng màu, nét mực kẻ lại theo các đường đó.
- Hai hàm là lưới bản lề mềm: trọng số 0 ở bản lề (ngay sau khoé miệng) lên 1 trong một phần tư đầu của hàm; mông + đuôi và vòm chồng
  nhau 70 px, cùng bám `than` ở chỗ nối nên không hở. Hai đầu vây là xương con của `move` (bám đất), phần trên vây gần theo thân,
  vây xa theo hàm dưới (nấp sau cằm, hàm hạ xuống không lòi ra).
- 26 xương, 18 slot, 6572 đỉnh, `.atomik` 265 KB; hình bóng khung 0 idle khớp concept 0,984; mọi clip nối về idle lệch 0 px.
- Clip (dạng 2 chậm 1,1 lần): `appear` 1,76 s (rơi từ trên xuống, nện bụng ở 0,29 s có sự kiện `cham_dat` cho sân lắc cam, nằm bẹp
  xoạc vây, chống vây đẩy người lên, lắc mình) · `idle` 2,2 s (thân lắc, hai hàm hé – khép, táp miệng một cái, đuôi quẫy) · `attack`
  1,32 s, `trung` 0,62 s (nhổm lùi há to, lao tới sập hàm, nén bẹp, giữ ngậm) · `cast` 1,69 s, `trung` 0,73 s (lao tới, bật nhảy lộn
  người, quật vây đuôi đá từ trên xuống, bật ngược về) · `skill` 2,2 s, `phun` 0,44 s, `het_phun` 1,8 s (rạp xuống ngậm miệng, bật há
  cực đại nanh xoè, giữ rung 1,25 s, sập, về) · `hit` 0,59 s · `die` 1,61 s (hất tung lộn ngửa, rơi lưng xuống, giãy vây, tan).
- Chưa làm: dạng 1 (chờ duyệt concept) và `evolve`; vào Unity (chờ người dùng chọn suất, tên); VFX (luồng nước của chiêu cuối, vệt
  quật đuôi); nối sự kiện `cham_dat` với lắc cam của sân. Mới soi tờ khung, chưa xem ở tốc độ thật trong game.

## 7. Chốt rig dạng 2, rig dạng 1 và tiến hóa (2026-11-11 chiều muộn)

Người dùng chốt rig dạng 2 ("ổn rồi, chốt đi") sau các lượt sửa:
- **idle**: bỏ cú táp miệng nhanh, chỉ để miệng mở thở nhẹ.
- **cast (chiêu mana)**: "xoay người quật đuôi mạnh chứ không phải lộn ngược quật" → lao tới, xoay người quay lưng lại (lật ngang cả con
  qua tỉ lệ x của xương `move`, 5 khung; shader sticker `Cull Off` nên vẽ được), đuôi vểnh cao quật xuống (`trung` 0,73 s), xoay lại, về.
- **Vây xa (chân bên phải)**, bốn lượt mới đạt:
  1. mảnh chỉ gồm phần lộ ra trên concept + mẩu vá → mép trái bị viền hàm khoét lõm ("móp"); người dùng: "chân con gốc đâu bị móp
     một bên... để nó làm layer dưới là được" → làm **một cánh vây đủ** ở lớp dưới cùng (dùng lại hình vây gần, lật ngang, thu 0,86);
  2. gốc vây bám `than` → thân nhổm lên là vây bị kéo dài thành cột trơ bên miệng → cho gốc bám hàm dưới;
  3. đầu vây ghim cố định trên đất → thân ngả lùi là đầu vây bị bỏ lại, tách khỏi cơ thể → đầu vây **trượt ngang theo cằm**;
  4. hàm hạ sát đất ép vây bẹp thành tấm dẹt (chỉ thấy khi soi bằng runtime Spine thật) → mảnh vây thấp lại (ép dọc 0,72), thêm khớp vai
     `vai_x`: vai lên theo hàm dưới, hạ tối đa 35 % chiều cao vây.
  Bài học: chân nấp sau thân phải là mảnh ĐỦ ở lớp dưới; đầu chân bám đất phải đi theo thân theo chiều ngang; sửa xong phải soi bằng
  runtime Spine thật (`mo_xe/chay.py sheet ... view=...`), phóng to đúng chỗ người dùng chụp, rồi mới báo.

Dạng 1 (`inbox/ca_voi_1/tai_ve/L1_duyet.png` = `L1_concept_2.png`; người dùng chưa nói rõ duyệt, tạm dùng): cùng mã `ca_voi.py`, số ở
`CFG[1]`. `ca_voi.py all` → dạng 2 264 KB; dạng 1 298 KB (gộp bản nhẹ dạng 2: ảnh 0,6 lần, lưới thưa 1,8 lần; 48 xương, 31 slot), có
`evolve` 2,8 s (rạp xuống ngậm miệng rung, tan, dạng 2 hiện ra há to gầm nanh xoè, hoà về idle dạng 2; lệch cuối 0 px). Mọi clip của
cả hai dạng nối về idle lệch 0 px. Đã soi bằng runtime Spine thật: dạng 2 (attack, skill, appear + cận vây xa), dạng 1 (attack, skill,
cast, appear, evolve + cận vây xa). Còn gợn nhỏ ở dạng 1: mép phải vách họng hơi xơ khi há to, một vệt trắng mảnh cạnh con hà.

Chưa làm: vào Unity (chờ tên, suất), VFX (luồng nước chiêu cuối, vệt quật đuôi), nối `cham_dat` với lắc cam.

## 8. Ngậm miệng và mép miệng lúc idle (người dùng báo trên dạng 1, 2026-11-11 tối)

- "dạng 1 lỗi khi gập hết miệng đánh thường": ngậm bằng xoay hai hàm quanh bản lề làm mỏm hàm trên chọc xuyên hàm dưới (miệng khép sẵn ở
  cả hai khoé), vòm họng tím nằm trên mảnh hàm trên nên đè lên hàm dưới, lộ nguyên mảng tím. Sửa:
  1. **vòm họng thành mảnh riêng `vom` nằm SAU hàm dưới** (trọng số như hàm trên);
  2. **ngậm = hai mép môi khép về trục miệng như mí mắt**: xương `moi_t` (con của `ham_tren`), `moi_d` (con của `ham_duoi`); trọng số
     1 ở mép môi giữa miệng, về 0 ở trục miệng (lòng miệng co lại), ở hai khoé, và ở viền ngoài của hàm (viền ngoài đứng yên: đầu giữ
     khối, vách họng không lòi); nanh dời theo môi theo chỗ gốc nanh dọc miệng nên hai hàng đan cài; hàm chỉ ép nhẹ (16 % / 13 %) và
     xoay nhẹ (−5° / +3°). Dạng 2 nanh rất to nên môi chỉ khép 74 % quãng (`CFG[2]["ngam"]`).
  Hai cách thử trước không đạt: ép dẹt cả hàm 50 % (miệng vẫn mở một nửa); môi khép nhưng viền ngoài cũng trôi theo (vách họng tím lòi
  trên đỉnh đầu và dưới bụng).
- "idle hở mép miệng": nhịp thở xoay hàm nên khoé trước tách ra → thở bằng phồng nhẹ hai hàm (tỉ lệ y), hai khoé luôn dính.
- Sau sửa: dạng 2 298 KB, dạng 1 343 KB (gộp dạng 2). Đã soi bằng runtime Spine thật: khung ngậm của attack và khung rạp ngậm của
  skill ở cả hai dạng, khoé miệng lúc idle dạng 1.

## 9. Lưng gãy lúc há to, nanh chồng nhau lúc ngậm (người dùng báo trên dạng 1, 2026-11-11 tối)

- "bẻ mesh kĩ hơn, phần giữa thân bị gãy": vùng bản lề của hàm chỉ rộng một phần tư hàm nên lúc há to cả đoạn lưng gập lại ở một chỗ;
  thêm một con hà bị đường cắt lưng chia đôi, nửa thừa lòi ra thành vệt trắng. Sửa: vùng chuyển của bản lề **rộng dần ra phía viền
  ngoài** (sát mép môi vẫn hết trong 27 % hàm cho nanh và môi bám chắc; ở lưng / bụng trải tới 70 % hàm) nên lưng uốn đều; vách họng
  dùng cùng trường này; mỗi con hà thuộc trọn một mảnh theo tâm của nó.
- "khi đóng mồm răng nhìn chồng nhau loạn quá, làm giống với dạng 2": dạng 1 có ba nanh dưới nằm đúng dưới ba nanh trên. Sửa: lúc ngậm
  nanh dưới **trượt dọc môi nửa khoảng cách** về phía bản lề (`CFG[1]["truot_nanh_d"] = -56`) để hai hàng so le cài răng lược; môi
  khép 80 % quãng (`"ngam": 0.80`).
- Chiêu cuối: hàm dưới hạ 23° (trước 30°) và thân nhấc cao hơn để đáy hàm không chìm dưới mặt đất lúc há cực đại.
- Sau sửa: dạng 2 302 KB, dạng 1 348 KB. Đã soi bằng runtime Spine thật: khung ngậm của attack và khung há cực đại của skill ở cả hai
  dạng, tờ 8 khung của evolve.
- Phiên khác (assets-7e) báo 2026-11-11: đã sửa `HatNuoc.cs` (thêm chiêu `n_ngoc`) và `StageView.cs` (`WaterFx` dòng `ha_ba`), đưa sò
  đột biến vào suất ải 15 `ha_ba`, `quai/da_nhan.json` dòng `ha_ba` trỏ sang rig sò. Khi đưa cá voi vào game phải đọc lại hai file đó
  trước khi ghi và không lấy suất ải 15.

## 10. Vào game (người dùng: "ổn rồi, cho vào game thay thế tướng cũ", 2026-11-11 tối)

Thay rig của **suất 7 đảo Thủy = ải 40, id `lien_kinh`** (trước là cá voi cõng sen tm07). Làm như các suất trước: giữ id, chỉ số, thẻ,
`heroes.json`, `cards.json`, golden; chỉ thay rig, chân dung, hiệu ứng nước.
- `quai/da_nhan.json`: dòng `lien_kinh` trỏ sang `inbox/ca_voi_<k>/rig/ca_voi_<k>.atomik`; `quai/vao_game.py` đã chép
  `Assets/03 Art/Heroes/Resources/lien_kinh_<k>/lien_kinh_<k>.atomik` (348 KB / 302 KB) và `_portrait.png` (kiểm: đủ 7 clip + `evolve` ở
  dạng 1, có khối `game`; cảnh báo chung của mọi dạng: `game.shadow` không có slot).
- `game.muzzle`: bộ xuất lấy xương miệng ở khung trúng của `cast`, mà `cast` của con này lật ngang cả con → thêm xương `nha` (con của
  root) đặt ở tâm miệng lúc đang há giữ chiêu cuối, truyền `mieng="nha"`: muzzle dạng 1 (92, 150), dạng 2 (164, 210).
- `StageView.WaterFx`: `lien_kinh` → mana `n_va` (cú va nước đúng khung trúng của cú quật đuôi), chiêu cuối `n_tia` ở cả hai dạng (tia chảy
  1,25 s, bằng đoạn giữ há của clip). `HatNuoc.WThemes`: bảng màu lam đá sẫm / lam biển / trắng băng, mảnh văng `tinh_the` màu đá đen.
- **Lắc cam lúc ra sân**: `AolaActor.EventTime(clip, name)` + `AolaSticker.EventTime`; `StageView` cộng trauma 0,35 khi giờ ra sân đi qua
  sự kiện `cham_dat` của clip `appear`. Áp cho MỌI rig có sự kiện đó trong `appear` (vd. cá đèn lồng).
- Biên dịch thử ngoài Unity bằng csc của Unity 6000.0.73f1 với `Library/Bee/artifacts/1900b0aE.dag/PokiClash.Game.rsp` (ra thư mục
  scratch): 0 lỗi. Unity lúc đó không mở nên CHƯA xem trong Editor, chưa chạy test EditMode, chưa thử Android.
- Còn chờ người dùng: tên tướng, tên hai dạng, danh hiệu, tên ba thẻ (đang là Liên Kình / Kình Nụ / "Kình ngư cõng sen thiêng" /
  Bong Bóng Sen, Nụ Bung, Sen Thiêng: không còn khớp hình); VFX riêng cho luồng nước "siêu to" nếu `n_tia` chưa đủ.

## 11. Tên, lưới dày, lưng hai lớp, đáy trơn (2026-11-11 tối)

- **Tên** (người dùng: "tên tùy bạn quyết, skill tự ghép"; `quai/doi_ten_thon_kinh.py`, sửa `heroes.json`, `cards.json` và đúng các dòng
  tên / biểu tượng trong `HeroDb.asset`, `CardDb.asset` vì Unity không mở để chạy "Nhập dữ liệu"; golden và test không chứa tên hiển thị):
  tướng **Thôn Kình**, danh hiệu "Cá voi vô diện đuôi đá", dòng "Dòng Thôn Kình"; dạng 1 **Kình Nhi**, dạng 2 **Thôn Kình**;
  thẻ mana **Quật Đuôi Đá** (rock), chiêu cuối **Thôn Hải Pháo** (wave), bị động **Nuốt Đòn** (fang), bị động boss **Da Đá Hộ Thể**
  (rock). Id (`lien_kinh`, `lien_kinh_*`), chỉ số, hiệu ứng thẻ giữ nguyên. Ghép chiêu: mana = `n_va`, chiêu cuối = `n_tia` (mục 10).
- "chia mesh phần cánh / đuôi thật kĩ, nhiều hơn nữa": bước lưới của `duoi`, `vay_duoi`, `vay_g`, `vay_x` còn 55 % (`MAU` trong `dung`);
  đuôi chia lại gấp đôi số đốt (dạng 2: 10 đốt, dạng 1: 8 đốt), hệ số từng đốt trong clip tính theo vị trí dọc đuôi nên tổng độ cong
  như cũ. Dạng 2: 35 xương, 10 808 đỉnh, 398 KB; dạng 1 (gộp dạng 2): 62 xương, 13 448 đỉnh, 458 KB (trần 0,5 MB, còn dư ít).
- "phần lưng nhìn như 2 lớp chồng lên nhau": mảnh mông + đuôi nằm dưới vòm hàm trên 70 px nhưng không uốn theo bản lề hàm → há to là
  hai mảnh lệch nhau. Nay mảnh `duoi` dùng chung trường bản lề `f_ham(…, hàm trên)` với vòm.
- "những đoạn đáy để màu trơn cho đỡ lộ khuyết điểm": bỏ dải sóng và rãnh họng ở hàm dưới, tô lại trắng băng (`CFG["day_tron"]`,
  mặc định bật). Bẫy: pixel răng cưa ở mép nét mực bị xếp nhầm màu tím / hồng nên vùng "giữ quanh miệng" phải lấy theo đa giác miệng,
  không theo nhãn màu.
- Đã chép lại vào `Assets/03 Art/Heroes/Resources/lien_kinh_<k>/`. Soi bằng runtime Spine thật sau các sửa này: attack nhổm há to và
  skill há cực đại dạng 2, idle và skill dạng 1 (lưng liền, đuôi cong tròn, bụng trơn). Còn sót: một chấm lam nhỏ ở đáy bụng dạng 1 sát
  mép vây gần (thấy ở idle); chưa xem trong Unity.
