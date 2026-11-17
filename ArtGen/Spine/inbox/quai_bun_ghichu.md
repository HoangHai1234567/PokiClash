# Quái bùn / quái đất sét (`quai_bun`): tướng 8 đảo Thổ

Bắt đầu 2026-11-17 (máy ổ C, kho `D:\Ripper\SwordxStaff`). Con gốc của rig: **`monster_3668`** (game tham khảo), **người dùng chỉ** (ảnh chụp
trang xem, clip `skill_02_1`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó: dùng nội bộ, không đăng công khai. Hình là của mình.
Suất 8 đảo Thổ = ải 50 "Vách Kim Cương" (`IslandGen.cs` Plan Tho), id game hiện là **`ho_kim_cuong`** (Hổ Kim Cương, có bản boss
`ho_kim_cuong_boss`). Mã làm việc `quai_bun`. Tên, số dạng, có thay hẳn `ho_kim_cuong` hay không: chưa bàn.

## 1. Lời dặn của người dùng (2026-11-17)

- "tướng thứ 8 đảo thổ, concept **quái vật bùn lầy hoặc quái vật đất sét như con gốc**".
- "các animation **bạn tự sáng tạo** xoay quanh con gốc và việc **co dãn, biến hình** được của nó, **xem kĩ rig con gốc và animation** của nó".
- "dùng **magnific** để gen ảnh"; "các ảnh bộ phận khi gen **không được quá 100 credit**, nếu quá hỏi tôi".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3668/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample_goc.json` 18 clip 30 khung/giây, `khung/`)

144 xương, 76 slot (48 hình bật ở idle 0), 22 clip, 18 912 khoá. Ràng buộc: 2 IK (`shouL1` bone20/21, `shouL2` bone22; mix 0, chỉ bật trong
run_01 / stun_01), 1 transform (`bone82`, mix 0, bật trong clip thân xẻ), **5 path**: `lujing_01..04` (4 xương trên path `lujing` của thân,
bone2) và **`shou`: 8 xương `all2..all2h` chạy trên path `shou` (slot 67, xương `all3`)** = TAY CO GIÃN.

- Thân: `all → bone2 → bone3 → bone4` (ngực) → `bone5 → bone6` (ĐẦU; mắt `bone39..44`), `bone37 → bone38..38c` (hàm / bụng dưới đầu).
- Tay R (bên TRÁI hình, vai gù to ở sau lưng, vẽ trước cùng): `bone7 → bone8 → bone9 → bone10` (nắm đấm, ngón `bone11..18`); slot `P_shouR1`
  (vai), `P_shouR2` (cẳng), `P_shouR3*` (bàn + 8 đốt ngón), xúc tu trên vai `P_shouR1_1/1_2`, `P_shouR2_1/2_2`.
- Tay L (bên PHẢI hình, phía địch): `bone19 → bone20 → bone21 → bone22` (nắm đấm, ngón `bone23..30`); slot `P_shouL1` (bắp tay, vẽ sau thân),
  `P_shouL2`, `P_shouL3*` (bàn vẽ trước đầu), xúc tu `P_shouL1_1`.
- Đế nhầy `P_shenti1`, `P_shenti1_1..3` (bone2, bone31..36); thân `P_shenti2*` (trọng số theo `lujing_*`, `bone50/51*`); xúc tu lưng
  `P_shenti2_1..4`; đầu `P_tou_2_01..07`, mắt `P_yanjing_3..6`.
- **Ba bộ hình biến hình:**
  - TAY CO GIÃN `G_shoudabi` (bắp tay), `G_shoubi` (ống tay dài), `G_shouzhang` (nắm đấm): lưới trên chuỗi `all2..all2h`; skill_02_* và
    skill_03 TẮT cả tay L thường (`P_shouL*`) và BẬT bộ này. Lúc nghỉ chuỗi đậu ngoài màn (x 1619–2852).
  - ĐẦU HÀM KHỔNG LỒ `P_tou_1_01..06` + mắt `P_yanjing_1/2` (skill_04 đổi cả đầu `P_tou_2_*` sang bộ này): hàm trên to, lòng miệng, lưỡi,
    hàm dưới / bụng có răng.
  - THÂN XẺ ĐÔI `A_shenti04..011`, `A_tou06`, `A_shou14` (deform_01 → idle_02 / block_02 / charge_01 / charge_02): hai nửa thân tách, giữa là
    khoang nhầy; trong khoang là nhân vật người chơi bị bắt (`A_shenti07` mặt, `A_shenti08` tay): cơ chế riêng của game đó, mình không dùng
    nguyên.

Clip của họ (tờ `khung/`, đo theo `sample_goc.json`):
| clip | dài | động tác |
|---|---|---|
| `appear_01` | 1,00 | hình `appear` ở 0–0,47; thân mọc lên từ đất thành cột mảnh cao (bone2 tỉ lệ 0,25 × 1,3 → 1,09 × 0,47), bập xuống thành dáng |
| `idle_01` | 10,67 | thở, xúc tu lượn |
| `run_01` | 0,93 | lê đế nhầy, chống nắm đấm |
| `skill_01_1` | 1,00 | giơ nắm đấm thường lên cao (y 1180 ở 0,30), NỆN xuống 0,50 |
| `skill_01_2` / `_3` | 1,00 | vung hai lần / quét ra sau rồi chồm |
| `skill_02_1` | 1,70 | nhún, rướn (0–0,4), 0,50 TAY VƯƠN NGANG (chuỗi dài ~1400 đơn vị tới x 1665), quẫy 0,5–1,1, co về 1,2 |
| `skill_02_2` | 1,70 | như trên nhưng tay vươn THẲNG LÊN TRỜI (y ~1950) |
| `skill_02_3` | 1,70 | tay cắm XUỐNG ĐẤT (y −876) 0,5–1,1, rút lên 1,2 |
| `skill_03` | 1,83 | 0,6 đấm cắm đất ngay trước mặt, giữ tới 1,1, 1,3 móc vụt lên cao (y ~1850) rồi về |
| `skill_04` | 1,97 | co rúm (0–0,44), 0,66 ĐẦU PHÌNH THÀNH HÀM KHỔNG LỒ, dang hai tay, giữ tới 1,53, về 1,75 |
| `deform_01` | 0,67 | thân xẻ đôi |
| `show_01` | 1,97 | khoe: há to, dang tay |
| `hit_01/02`, `stun_01`, `die_01` (chảy sụp xuống) | | |

## 3. Concept lượt 1 (Magnific GPT 2.6, 1k high, 95 credit / ảnh, 3 ảnh = 285 credit, ~2 phút / ảnh)

Script `ArtGen/Spine/quai_bun.py` (ca_con, slot, concept, so_goc); gói `gui_gpt/quai_bun_1/luot_1_concept_<A|B|C>.txt` + `HUONG_DAN.md`;
ảnh `inbox/quai_bun_1/tai_ve/L1_<k>.png`; tờ so 4 ô `inbox/quai_bun_so_concept.jpg`; chồng viền con gốc `inbox/quai_bun_1/mau/_so_goc.png`.
Ảnh mẫu: 1 = con gốc (dáng, bố cục chi, cách dựng miệng ngực), 2 = chiến binh đất nung, 3 = vượn núi đá (nét vẽ, mặt dữ). Giữ: quay phải,
miệng to mở từ dưới đầu xuống ngực (đầu = hàm trên, bụng = hàm dưới), hai mắt nhỏ, hai nắm đấm chống đất, đế loang trái, chùm xúc tu đúng
chỗ. Đổi: đầu, xúc tu, chất liệu, màu; cấm hồng, lòng miệng xanh phát sáng, mạch xanh, đầu xúc tu dẹt, mào nhọn vuốt sau.

| Hướng | Ý (Claude đề xuất) | IoU hình bóng |
|---|---|---|
| A | BÙN LẦY nâu sô-cô-la: xúc tu thành giọt bùn dựng (đầu giọt tròn), gờ mày bùn, mắt hổ phách, hai sừng đá cuội; lòng miệng vàng hổ phách, răng đá cuội; nắm đấm đá cuội; bong bóng bùn; đế vũng bùn | 0,809 |
| B | ĐẤT SÉT vàng son: cuộn sét vê (dễ đọc thành xúc tu bạch tuộc), vết ngón ấn, mắt vàng chanh; lòng miệng nâu đỏ như lòng hũ sét, răng sét nhọn kem | 0,848 |
| C | BÙN + MẶT NẠ ĐẤT SÉT ngà (vạch đỏ son trên má, tai nhọn), nắm đấm quấn băng sét ngà, xúc tu giọt bùn xoắn; lòng miệng hổ phách. Mặt nạ hơi giống mũ sọ | 0,824 |

Claude soi: cả ba đúng dáng, đúng hướng, mọi chi dính thân, miệng đúng cách dựng. A vẽ nhiều giọt bùn rời bay quanh: lúc chia mảnh bỏ (để
VFX làm). **Người dùng chọn A** (2026-11-17) → `tai_ve/L1_duyet.png`; bảng animation mục 4 không bị sửa.

## 4. Đề xuất animation (Claude, 2026-11-17; người dùng chọn concept A, không sửa bảng này)

Ý chung: tướng là một khối bùn "nặn" được: vươn, cắm, phình, chảy. Ba bộ biến hình của rig gốc dùng làm ba đòn; đoạn tay lúc ẩn dưới đất,
bùn văng, sóng bùn là VFX (rig chỉ để xương miệng, xương `far` và sự kiện).

| Clip | Nguồn | Diễn |
|---|---|---|
| appear | appear_01 | vũng bùn loang trên đất (VFX) → cột bùn vọt lên mảnh và cao (co dãn) → bập xuống nặn thành hình, nảy thạch hai nhịp, rũ văng giọt, há miệng gầm ngắn |
| idle | idle_01 (cắt đoạn lặp ~2,7 s) | thở nặng, xúc tu bùn lượn trễ nhịp; trò riêng: bong bóng bùn phồng rồi vỡ trên lưng, nắm đấm bóp "bẹp" một cái |
| walk | run_01 | lê đế bùn, chống nắm đấm như khỉ đột |
| đánh thường | skill_02_1 | nhún, rướn, TAY BÙN VƯƠN THẲNG tới đối thủ như dây chun (code lái nắm đấm tới đúng chỗ địch), đấm "bẹp", co về nảy quá đà |
| chiêu mana | skill_02_3 | đấm cắm tay xuống đất, gò bùn / vết nứt chạy ngầm tới chân đối thủ (VFX), NẮM ĐẤM BÙN KHỔNG LỒ trồi lên hất tung, rút về |
| chiêu cuối | skill_04 | co rúm run, cả đầu ngực PHÌNH THÀNH CÁI HÀM KHỔNG LỒ, hút đất đá vào, rồi PHUN một dòng bùn đá trùm đối thủ, bùn đọng thành vũng (VFX), xẹp về dáng cũ rung thạch |
| hit | hit_01 | lún vào, bật ra rung như thạch |
| die | die_01 | sụp chảy thành vũng bùn rồi thấm xuống đất |

Phương án thay cho chiêu cuối (nếu người dùng muốn dùng cả bộ thân xẻ đôi): thân xẻ dọc (deform_01) lộ khoang bùn chứa một tảng đá lớn,
hai tay giơ cao ôm tảng (charge_02) rồi ném / nện. Đòn dự phòng: skill_02_2 (tay vươn lên trời rồi nắm đấm nện từ trên xuống đối thủ).

## 5. Mảnh (`ArtGen/Spine/quai_bun_manh.py`; gói `gui_gpt/quai_bun_1/luot_2_*.txt`; Magnific GPT 2.6 1k high, 95 credit / tờ, 9 tờ = 855 credit)

- **Tờ T1–T5 "đúng chỗ, đúng cỡ" trên concept** (ảnh mẫu duy nhất là concept): T1 thân + vũng bùn; T2 vai gù + bắp tay xa; T3 đầu (không mắt,
  giữ hàng răng trên) + cẳng tay xa; T4 bụng = hàm dưới (hàng răng dưới) + khối cẳng tay gần; T5 lòng miệng hổ phách. Cắt cụm theo tâm dự
  kiến (`TAM`). Ghép 9 mảnh so concept: IoU 0,819 (phần thiếu là xúc tu + nắm đấm, đến từ tờ D). Mắt cắt thẳng từ concept, mắt nhắm dựng bằng mã.
- **Tờ D_P / D_X / D_V / D_H "theo khung part"** (ảnh 1 = các part gốc cắt theo lưới, phóng 1,7–2,6 lần; ảnh 2 concept lấy màu): 2 lòng bàn
  tay + 16 đốt ngón (ngón co 50–80° trong clip nên mỗi đốt một mảnh như họ) → đá cuội xám; 9 xúc tu → giọt bùn dựng; tay co giãn (bắp, ống,
  nắm đấm); đầu hàm khổng lồ skill_04 (6 mảnh + khung mắt + mắt). IoU từng part 0,80–0,97 (`manh/_iou.json`, tờ so `manh/_so_<tờ>.png`).
- `can_mau`: dời màu bùn các mảnh tờ D về trung vị bùn của thân (xúc tu đỏ hơn ~10, hàm khổng lồ ~17) → `manh/part_can/` (rig dùng).
- `tach_than` (sau khi soi rig, xem mục 6): mảnh thân tách ba lớp CÙNG một ảnh: `than_lot` (cột thân lót, y 600 → mép vũng bùn, đủ bề ngang),
  `than_sau` (thân, thừa 18 px dưới mép vũng bùn), `vung_bun` (vũng bùn phía trước, mép trên mờ 8 px trong lòng thân). Đường tách y 805 px;
  trái góc lõm (x < 525) hạ lên 780 để trọn nét viền lưỡi vũng bùn nằm trong mảnh vũng bùn.

## 6. Rig (`ArtGen/Spine/quai_bun_rig.py` → `inbox/quai_bun_1/rig/`, không theo git)

157 xương (đủ 144 xương của họ + `move`, `dat_cat`, `fly_tay0..7`, `far`, `nam_ngam`, `mieng`, `mieng_to`), 61 slot, 3811 đỉnh, 8 clip, 14 sự
kiện; `.atomik` **484 KB** (atlas 1048 × 1072, D_PX 0,42). Mọi clip nối khung 0 idle 0,00 px; runtime thật 60 khung/giây không có bước xoay
> 150°. Trang xem `rig/xem.html` (thu_xem: đủ 8 clip); tờ khung runtime thật `rig/that/`.

- Mảnh concept bám HỢP lưới các part gốc ở idle 0 (`trong_so_goc` + làm mịn), mảnh tờ D dùng NGUYÊN lưới gốc (`gan_nguyen`). Chuyển động = `l`
  của mẫu khung (IK, transform, 5 path đã nướng). Hiện / ẩn theo slot lái của họ (trường `n`); skill_04 hoà chéo hai bộ đầu bằng độ đậm
  1,5 → 1,733 s (con gốc dùng RGBA, mẫu khung không có độ đậm: đọc bằng `chay.py keys`).
- **Tay co giãn tới đúng đối thủ**: tám xương path `all2..all2h` treo dưới `fly_tay0..7` (con của root), hai xương nắm đấm `all2h2/h3`
  (NoScale ở rig họ) dưới `fly_tay7`; mỗi khung biến đổi riêng tính từ ma trận THẾ GIỚI mẫu khung (đúng cả NoScale). Ở attack `fly_tay_k`
  đặt ở w_k · far (w_k = phần quãng của xương k chiếu trên đoạn vai → far) → `AolaActor.FarAtomik` dời mỗi xương đúng w_k × (đối thủ − far):
  cả cánh tay giãn đều, nắm đấm tới đúng đối thủ. far mặc định = nắm đấm lúc duỗi ngang hết cỡ (1821, 572). Tay phóng ra 0,42 → 0,50 s (họ
  bật trong một khung).
- skill_02_1 đổi thứ tự vẽ (cẳng + nắm tay xa ra sau thân lúc giơ tay): bản sao `@sau`.
- MỘT mặt nạ đất phủ mọi slot (mép thấp hơn đáy idle 110 đơn vị; idle gốc thò xuống 75, die 97); appear nâng mặt nạ sát đất bằng xương
  `dat_cat` (cột bùn trồi từ đất). Tay cắm đất ở cast bị giấu dưới đất.
- Lỗi đã sửa khi tự soi: lưới thân gập răng cưa ở góc lõm trái dưới khi skill_04 phình thân (họ là hai mảnh P_shenti2 / P_shenti1 chồng nhau,
  mình gộp một lưới) → tách ba lớp như mục 5, thân chỉ bám P_shenti2, cột lót bám P_shenti1, vũng bùn đứng yên theo xương vũng bùn; đã thử và
  bỏ: kéo dải trên vũng bùn theo thân (nghiền sỏi, thành tấm đứng khi thân rướn), cột lót chỉ phía trái (lộ góc), hạ đường tách phía phải
  (cột lót ngoài lưới văng thành đuôi). Khe trắng của bắp tay co giãn (của họ là lỗ thủng) → trong suốt. Mép cắt mờ ở die (co dẹt quanh gốc
  `all` nằm dưới đáy hình) → co quanh mặt đất.
- Còn lại (nhỏ, ghi để soát lại nếu người dùng chê): đầu phải vũng bùn thành mũi bùn nhọn khi thân rướn cao (attack 0,3, cast 0,38); viền đôi
  rất sát ở sườn trái lúc cast 0,7 (cột lót lộ sau thân); tay co giãn lúc rút về (1,23–1,3 s) vẽ sau thân (họ cho ra trước 0,07 s).

| Clip | Nguồn | Mốc |
|---|---|---|
| appear 2,05 s | appear_01 + nảy thạch + gầm (dáng show_01) | `dap` 0,42, `gam` 1,25 |
| idle 2,67 s | idle_01 hai chu kỳ nền + chớp mắt + thân nở xẹp trễ pha | `bong` 1,90 (VFX bong bóng bùn) |
| walk 0,93 s | run_01 | |
| attack 1,30 s | skill_02_1 co giờ (giữ 0,5–1,1 → 0,5–0,78) | `vuon` 0,42, `trung` 0,50 |
| cast 1,70 s | skill_03 (đấm cắm đất 0,6) + nắm đấm khổng lồ `nam_ngam` trồi ở far 0,74 → lún 1,04 | `cam` 0,60, `troi` 0,74, `trung` 0,84 |
| skill 1,97 s | skill_04 (hàm khổng lồ 0,6 → 1,5) + rung lúc phun | `hut` 0,22, `ha` 0,66, `phun` 0,78, `trung` 1,05, `khep` 1,55 |
| hit 0,50 s | hit_01 + lún nảy thạch | |
| die 1,50 s | die_01 + chảy dẹt quanh mặt đất + mờ | `chay` 0,55 |

## 7. Việc tiếp

1. Người dùng xem `rig/xem.html`.
2. VFX (chưa làm): vũng bùn trồi (appear), bong bóng bùn vỡ (idle), vệt bùn theo tay + toé bùn trúng (attack), toé bùn chỗ cắm + gò bùn / vết
   nứt chạy tới + toé ở nắm đấm khổng lồ (cast), hút đất đá vào miệng + dòng bùn đá phun + vũng bùn đọng (skill), vũng chảy (die).
3. Vào game: thay suất ải 50 `ho_kim_cuong` (+ `ho_kim_cuong_boss`)? tên, số dạng, thẻ: hỏi người dùng; bỏ hẳn tướng cũ khi thay.

## 8. Lượt sửa 1 (người dùng 2026-11-17, xem `rig/xem.html`)

Người dùng: "chiêu cuối có thể sáng tạo hơn bằng cách há to miệng, nuốt kẻ thù vào bụng (lúc đó người phồng to như quả bóng tròn), sau đó
sinh các gai đất đâm chi chít xuyên thủng cơ thể của chính nó để đâm vào tướng ở trong ... sinh thêm biểu cảm mặt mắt căng ra mồm mím lại
kiểu cố giữ đối thủ trong bụng"; "appear có thể làm là có 1 cục đất tròn rơi từ trên trời xuống rồi nảy phát bung ra thành con tướng";
"phần dưới thân này bị rách lỗi rồi" (ảnh chụp skill: lỗ ở góc lõm trái dưới, mép mờ đầu phải vũng bùn).

- **Rách đáy thân**: bỏ hẳn bản ba lớp (than_lot / than_sau / vung_bun, mục 5–6: vẫn hở ở vài dáng). Thân là MỘT mảnh `than` liền, trọng
  số hoà theo chiều cao: trên bám P_shenti2, dưới bám P_shenti1 + P_shenti1_1..3, dải hoà y 700 → 890 px concept (`Y_HOA`, `HOA_Y["than"]`).
  Soát tờ toàn thân 22 dáng + tờ cận góc trái dưới mọi clip: liền, không gập, không mép mờ, không đuôi.
- **Tờ M_B1** (Magnific, 95 credit; `quai_bun_manh.py bong`, `cat_bong`): quả bóng mặt căng (mắt trợn, má phồng, mồm mím, răng thò, hai
  nắm đá ôm bụng), cục đất tròn trơn, ba gai đất. Rig: xương `bong` (tâm bóng ở x bụng, đáy chạm đất, R = 477) + `bong_r0..5` (phồng) +
  `gai0..9` (gai từ tâm, vẽ sau bóng), `cuc` (cục đất appear).
- **skill 3,2 s** (mới): co rúm, há hàm khổng lồ 0,62 (`ha`), hút 0,70 (`hut`: game kéo đối thủ vào miệng), nuốt 1,00 (`nuot`: game giấu đối
  thủ), thân bẹp → ĐỔI BẬC sang quả bóng 1,04 (`phong`), quẫy 1,24–1,70 (`giay`: bụng lồi từng góc, lắc, nảy), mười gai đâm xuyên ra
  1,70–2,10 (`dam`, `trung` 1,85), gai rút 2,36 (`rut`), bóng bẹp ngang → ĐỔI BẬC sang tướng há miệng dang tay 2,56 (`nha`: game nhả đối
  thủ về chỗ), nảy thạch, về dáng đứng.
- **appear 2,5 s** (mới): cục đất rơi từ 0,8 chiều cao (hiện dần 0,12 s), chạm đất bẹp 0,36 (`nay`), nảy, chạm lần hai 0,76, bẹp rồi BUNG
  0,82 (`bung`) thành tướng ở dáng bẹp của appear_01 (0,42) vươn lên, gầm 1,65.
- Xuất: 175 xương, 71 slot, 8 clip, 21 sự kiện, `.atomik` 497 KB (D_PX 0,39, sai số lược khoá xoay 0,15 / dời 0,3 để dưới trần 0,5 MB;
  lệch lớn nhất do lược khoá 2,4 px). Runtime thật 60 khung/giây: không có bước xoay > 150°.
- Việc game cần làm cho chiêu cuối (lúc vào game): ở `hut` kéo hình đối thủ về miệng (xương `mieng_to`) và thu nhỏ, `nuot` giấu, `nha` trả về
  chỗ; VFX phụt bùn ở `phong` / `nha` / `bung` (che chỗ đổi hình), toé đất ở `nay`, bụi đá mỗi gai.

## 9. Lượt sửa 2 (người dùng 2026-11-17)

Người dùng: "đoạn bung ra trong appear nhìn chưa mượt"; "chiêu cuối phải là lao vào địch, ngoạm địch rồi mới biến thành quả bóng, làm mượt hơn
nữa đi".

- **skill 3,4 s** (thay bản nuốt tại chỗ): lùi lấy đà, co rúm 0 → 0,42 (`lao`) → nhảy vồ cung thấp, chúi người, thân kéo dài theo đà, há hàm
  khổng lồ giữa không trung 0,58 (`ha`; hàm chúi về phía đối thủ) → chạm đích 0,80, sập hàm nửa chừng + bẹp 0,86 (`ngoam`: game giấu đối thủ)
  → ĐỔI BẬC sang quả bóng 0,90 (`phong`) ở đúng chỗ đã lao tới, bóng hiện cỡ 0,90 (≈ thân đang bẹp) vọt 1,14 → 0,96 → 1,0 → quẫy 1,18–1,72
  (`giay`, có đường bao êm vào / ra) → gai đâm 1,72 (`dam`, `trung` 1,88) → rút 2,38 (`rut`) → căng rồi bẹp → ĐỔI BẬC 2,62 (`nha`) sang tướng
  há miệng dang tay còn phồng 1,16 xẹp dần → nhảy lùi về chỗ 2,86–3,24 (`ve`). Hàm không khép kín được (mảnh vẽ cho dáng há chồng chéo khi
  khép hẳn), nên chỉ sập nửa chừng rồi đổi sang bóng mồm mím.
- Cú lao đi bằng xương `move` (D_LAO = 1,25 × chiều cao trong rig); xuất `lao=("skill",)` → game.json `lunge: ["skill"]`, `AolaSticker.Lunge`
  co cho đỉnh cú lao = 72 % quãng tới đối thủ. Skill không còn trong `stay`.
- **appear 2,6 s**: bung 0,84 (`bung`) không còn đổi bậc: cục đất phình đục tới (1,55; 1,65) trong 0,08 s rồi tan trong 0,035 s; tướng nở
  từ trong ra phía sau cục đất 0,42 → 0,86 → 1,08 → 0,97 → 1,0 (nảy đàn hồi, quanh điểm mặt đất dưới tâm cục), thân lắc thạch tắt dần; gầm 1,75.
- Trang xem: `xuat` lấy khung giữa mỗi clip làm khung nhìn nên cú lao, quả bóng, gai bị xén; `quai_bun_rig.py` dựng lại `xem.html` với khung
  nhìn ôm mọi khung (mỗi 5 khung) của mọi clip: tâm (751, 563), cỡ 3480 × 1884 đơn vị rig.
- Xuất: 175 xương, 71 slot, 8 clip, 22 sự kiện, `.atomik` 497 KB (dưới trần 0,5 MB). Runtime thật: tờ `rig/that2/skill.jpg`, `appear.jpg`,
  `cast.jpg` (khung nhìn của trang xem); 60 khung/giây không có bước xoay > 150°.
- Việc game (khi vào game): ở `ngoam` giấu đối thủ (đã bị ngoạm), `nha` trả đối thủ về chỗ; VFX phụt bùn ở `phong` / `nha` / `bung`, bụi đất
  khi đáp ở `ngoam` và `ve`, toé đất ở `nay`, bụi đá mỗi gai.

## 10. Lượt sửa 3 (người dùng 2026-11-17)

Người dùng: "chiêu cuối cho nhiều gai hơn, làm thêm animation nhổ đối thủ ra khi đã thực hiện xong chiêu cuối"; "mồm nó phải há thật to cho lố
vào để nuốt gọn đối thủ".

- **skill 4,3 s**:
  - Lao (0,42) → há hàm khổng lồ LỐ: phóng cả hàm quanh bone63 tới 1,7 lần (`HA_TO`), banh hàm trên +36°, hàm dưới −28° (`HA_TREN`,
    `HA_DUOI`), há rộng nhất 0,74–0,81 → sập từ 0,81 tới 0,92 (`ngoam`), tướng còn lơ lửng 0,08 chiều cao lúc ngoạm (`LO_LUNG`: hàm to
    không thụt đất) rồi rơi xuống đổi thành bóng 0,99 (`phong`); bóng hiện ra còn bẹp ngang như hàm vừa sập rồi nảy tròn.
  - Sập hàm: hàm trên −40°, hàm dưới +24°, mõm dưới (bone65) +22°; sập mạnh hơn thì dải họng cam sẫm của P_tou_1_06 gập thành mẩu lòi.
  - Gai 22 chiếc (`N_GAI`, `GAI1` + `GAI2`): đợt 1 mười gai dài từng chiếc từ 1,78 (`dam`, `trung` 1,94), đợt 2 mười hai gai ngắn hơn
    (độ dài 0,70–0,95) xen giữa, dồn dập từ 2,16 (`dam`); rút cùng lúc 2,72 (`rut`).
  - Thôi làm bóng 3,00 (`hien`): tướng hiện lại còn phồng 1,16, đang ngậm đối thủ, run bần bật; ọe hai cơn 3,12 (`oe`); ngả lấy đà; chúi
    tới NHỔ 3,44: đầu bung toác thành hàm khổng lồ (skill_04 qua 0,6), phóng 1,5 lần, banh lố, rung; sự kiện `nho` 3,47 (game phóng đối thủ
    từ xương `mieng_to` bay về chỗ); thân xẹp phụt 0,93; sức nhổ hất tướng bật lên, bay lùi về chỗ 3,54–3,90 (`ve`), hàm khép dần (chạy
    ngược skill_04), đổi về đầu thường ngay lúc đáp; đáp bẹp, nảy thạch, về dáng đứng 4,3.
- Sửa kèm: mặt nạ đất (`dat_cat`, con của `move`) đứng yên ở mặt đất khi tướng bật lên; phần bị ẩn ở chỗ đổi thân ↔ bóng giữ nguyên dáng
  lúc đổi, gai ẩn giữ cỡ 0 (trước đó ở 60 khung/giây lộ một khung thân méo ngay trước lúc thành bóng).
- Xuất: 187 xương, 83 slot, 25 sự kiện, `.atomik` 509 KB (dưới trần 512 KB, sát trần). Không khung nào thụt dưới đường cắt (đo theo toạ độ
  thế giới). 60 khung/giây: bước xoay lớn nhất trên slot đang hiện 81° ở cú chúi nhổ (đầu bung thành hàm, soi runtime thật: liền).
  Tờ runtime thật: `rig/that2/skill.jpg`.
- Việc game (khi vào game): giấu đối thủ từ `ngoam` tới `nho`; ở `nho` phóng đối thủ từ `mieng_to` theo cung về chỗ cũ (code lái đường bay);
  VFX phụt bùn ở `phong` / `hien` / `nho`, bụi khi đáp (`ngoam`, sau `ve`), bụi đá mỗi gai.
