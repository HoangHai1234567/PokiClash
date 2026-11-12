# Người cây đầm lầy (`nguoi_cay`): tướng thứ 7 đảo Mộc

Bắt đầu 2026-11-12. Con gốc của rig: `monster_3491` (game tham khảo, kho `D:\Ripper\SwordxStaff`), **do Claude chọn** (người dùng không
chỉ con gốc): trong 347 quái đây là con dáng người đấm bốc rõ nhất, có sẵn cú đấm lao tới và cú nhảy lên đập xuống. Xương, lưới,
chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình.
Tên, id game, số dạng: chưa đặt.

**Đổi tên thư mục 2026-11-12** (khi làm thêm dạng non): dạng LỚN (bản D) từ `nguoi_cay_1` thành **`nguoi_cay_2`**; dạng NON là **`nguoi_cay_1`**. Mọi đường dẫn trong ghi chú này đã theo tên mới. Chọn dạng khi chạy script: biến môi trường `NC_DANG=1 | 2` (mặc định 2).

## 1. Lời dặn của người dùng (2026-11-12)

Kèm ba ảnh: hươu gỗ dạng 2 của mình (ảnh chụp trang xem) và hai ảnh nhân vật Swamp Thing của DC (tượng + tranh) làm gợi ý.

- "làm tướng thứ 7 của đảo mộc; concept là **giống với swampthing của DC, một humanoid bọc trong các lớp thực vật**".
- "các anim appear, walk, idle, die bạn tự làm".
- Đánh thường: "cứ cho đấm là được".
- Chiêu mana: "đưa tay lên triệu rồi **cây gai quật / trói đối thủ**".
- Chiêu cuối: "đưa hai tay lên gần nhau, **tụ 1 quả cầu thực vật** rồi **nhảy lên hướng vào đối thủ rồi đập xuống**".
- Gửi thêm lúc đang làm: "**trước khi bắt đầu tách lớp rig xương cho tôi xem concept đã nhé**" → dừng ở concept, chưa dựng tờ mảnh, chưa rig.

Màu, kiểu đầu, chi tiết: người dùng chưa dặn. Mục 3 là **đề xuất của Claude**, chờ chọn hướng.

Swamp Thing là nhân vật của DC: chỉ lấy Ý (hình người to vai, cả thân bọc trong các lớp thực vật), KHÔNG chép nhận diện của nó (mặt nạ
rễ có sống mũi và gờ mày rêu, mắt đỏ, thân bùn rêu lục một màu, dáng tả thực kinh dị), không đính ảnh của nó vào prompt nào.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3491/`: `info.json`, `att_goc.json`, `att_idle0.json`, `manh_anh.png`, `manh_dang_goc.png`, `manh_dang_idle0.png`, `parts/`, `khung/`)

64 xương, 43 slot (32 hình bật ở idle), 18 clip, atlas 39 vùng (ảnh nhỏ: thân 125 × 128). Con gốc là "rương ăn thịt" đội rương làm đầu,
thân người quấn băng; nhìn sang PHẢI, góc ba phần tư: không lật. Mọi hình là lưới (4–40 đỉnh).
IK: hai chân (`jiao`: bone43-44 → bone46; `jiao2`: bone47-48 → bone50), bốn IK kéo giãn một xương cho bốn chân rương (`target..4`).

Cây xương: `root > all > xy` (dời cả con) `> zhixin` (tâm thân) `> bone4 > bone5` (ngực).
- Ngực `bone5`: tay GẦN (bên trái hình, buông thấp, vẽ TRƯỚC thân) `bone31 > bone32 > bone33 > bone34` (slot `P_shouR1` bắp, `R2` cẳng,
  `R3` nắm); tay XA (bên phải hình, nắm đấm giơ, vẽ SAU thân) `bone35 > bone36 > bone37 > bone38` (`P_shouL1..3`); cổ `bone39 > tou` (đầu).
- Đầu `tou`: nắp rương `bone41` (+ 7 xương con), 6 xương răng `bone10..15`, lưỡi 7 đốt `bone16..22`, bốn chân rương `jiao..jiao4`.
- `zhixin`: hai chân `bone43-44`, `bone47-48` (IK, bàn chân `bone45-46`, `bone49-50` là con của `all`); vạt váy `bone51-52-53`, `bone54-55-56`.
- Thứ tự vẽ (sau → trước): tay xa (`shouL2`, `L1`, `L3`), `bu2`, chân xa (`jiaoL`, `tuiR1`, `tuiR2`), chân gần (`jiaoR`, `tuiL1`, `tuiL2`),
  thân `shenti2`, váy `bu`, tay gần (`shouR3`, `R2`, `R1`), rồi cụm đầu rương (`ya10`, `tou3`, `shetou2`, `tou2`, `tou1_1..3`, `shetou1`,
  `ya9..ya1`). Tên chân của họ lệch: bàn `jiaoL` đi với ống `tuiR2`.

Clip của họ (tờ `khung/`):
| clip | dài | nội dung |
|---|---|---|
| idle_01 | 4,0 s | thế thủ đấm bốc, nhún nhẹ |
| run_01 | 0,6 s | chạy chúi người, hai tay vung |
| skill_01_1 / _2 / _3 | 1,17 s | xoay vai lấy đà 0,13–0,26; ĐẤM thẳng tay xa 0,39–0,65; thu về |
| skill_02 | 2,17 s | chạy lấy đà 0–0,7; NHẢY lên 0,96–1,2; ĐÁP xuống đấm 1,44; về |
| skill_03, skill_04, morph_01 | | riêng của rương (nhảy ra từ rương, hoá rương): không dùng |
| hit_01/02, stun_01, block_01 | | |
| die_01 | 1,0 s | lảo đảo, ngã sấp về trước |

## 3. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `ArtGen/Spine/nguoi_cay.py` (`part_goc`, `luoi_xem`, `bo_cuc [hướng]`), `nguoi_cay_bo_cuc.py`, `build_nguoi_cay.py` (gói
`gui_gpt/nguoi_cay_2/`). Sơ đồ bố cục = khối thân, tay, chân của rig ở dáng thủ idle giây 0, làm trơn, tô màu của mình; ĐẦU RƯƠNG BỎ
HẲN, đầu và các lớp phủ vẽ mới bằng mã. Tỉ lệ rig → khung concept 1,24.

Giữ của con gốc: dáng người lùn mập thế thủ nhìn sang phải, tay gần buông thấp, tay xa nắm đấm giơ, hai chân choãi, có vạt váy.
Của mình (cả hai hướng): cả thân là thực vật xếp LỚP tách rời (để mỗi lớp có xương đung đưa riêng):
- hai **u rêu** làm đệm vai; **cổ áo bốn lá to** phủ ngực; **đai dây leo** + **váy năm lá dài**;
- tay, bụng, ống chân là **rễ bện**; cẳng tay **quấn dây gai** có gai kem (báo trước chiêu "cây gai"); hai **nắm tay gỗ rễ rất to**;
- đùi phủ rêu, bàn chân là gốc rễ ba ngón.

Lượt 1, hai hướng:
- `dam_lay` (`tai_ve/L1_dam_lay.png`) **A · người rêu đầm lầy**: đầu là mũ trùm rêu tròn, **hốc mặt tối chỉ có hai mắt vàng xếch**
  (hình người bên trong không lộ ra), ba dải rêu rủ sau gáy, **một chồi dương xỉ cuộn** trên đỉnh đầu, ba cây nấm cam đỏ trên vai gần.
  Rêu ô-liu `#6F9440`, lá lục lam sẫm `#2F7558`, rễ nâu `#8B6238`, gỗ rễ `#AA7C4A`, dây gai `#3E6B3A`, mắt vàng `#F6D93E`.
- `mat_go` (`tai_ve/L1_mat_go.png`) **B · người rễ mặt gỗ**: **mặt nạ gỗ nhạt** `#D6BE96` có gờ mày vỏ cây chữ V, mắt hổ phách, khe miệng
  mím; **ba chiếc lá rất to** quét ra sau làm mũ; hai bông hoa kế tím trên vai gần. Lá `#3E8448` / `#5C9646`, rễ `#966E46`.

**Bản 1 bị trả (2026-11-12, cùng buổi):** "tôi thấy **chưa đủ chiến, đầu nhìn xấu quá**, làm **sát với swampthing hơn 1 chút**".
(Nhận định của Claude: cả hai hướng ra kiểu chibi đầu to tròn, mũ trùm / mặt nạ dễ thương, thân nâu nhiều hơn lục; thiếu khối vai u,
đầu thụt, lớp rêu rậm của một con quái đầm lầy.)

Lượt 1b, bản 2 "quái đầm lầy nặng đô" (`bo_cuc chien`, `build_nguoi_cay.py ban2`), cùng dáng thủ của rig:
- tỉ lệ khỉ đột: **hai u rêu vai khổng lồ**, tay rất to, **đầu nhỏ (rộng ~200 px) thụt giữa hai vai**, ngực thùng, chân ngắn;
- thân, bắp tay, đùi là **bó dây leo phủ rêu sẫm** `#4E7A3E` (gần như toàn lục); u vai và rêu rủ `#7CA44A`; lá răng cưa sẫm `#2C6042` /
  nhạt `#92BA5C`; cẳng tay, nắm tay, ống chân, bàn chân gỗ rễ `#987248`; dây gai `#2F5233`, gai kem;
- mặt: **gờ mày chữ V nặng**, dải hốc mắt tối `#283224`, hai mắt cam lửa `#EE6C2C` hẹp xếch không con ngươi, **hàm rễ bạnh**; mào ba bốn
  lá răng cưa quét ra sau; không mũi;
- lớp phủ tách rời: ba **cành khô gãy** trên vai, **ba dải rêu rủ dưới mỗi bắp tay**, cổ áo năm lá, một dây leo vắt chéo bụng, đai + váy
  sáu lá hẹp so le; bỏ nấm, hoa, chồi dương xỉ.
- Hai kiểu đầu: `gam` (`tai_ve/L1b_gam.png`, **C**: mím miệng trễ xuống), `nanh` (`tai_ve/L1b_nanh.png`, **D**: há miệng nhe hàm răng
  gỗ + hai nanh dưới, chòm râu rêu).
- Vẫn giữ khác nhân vật gợi ý: không sống mũi rễ chạy từ mày xuống, mắt cam chứ không đỏ, có lá / cành / dây gai theo nét phẳng của game.

**Người dùng chọn D** (2026-11-12: "D") → `tai_ve/L1_duyet.png` = `L1b_nanh.png`. Hai câu Claude hỏi kèm (dây gai là mảnh của rig hay VFX;
ý appear / die) người dùng CHƯA trả lời: Claude làm theo đề xuất của mình, ghi ở mục 5–6 để người dùng đổi.

Lưu ý khi đọc `skill_01_1` của con gốc: đó là cú ĐỚP bằng đầu rương (đầu vọt tới trước ở 0,40 s), không phải cú đấm; chỉ lấy phần thân.

## 4. Mảnh (`build_nguoi_cay.py manh` → gói `luot_2_manh_*.txt`; `nguoi_cay_manh.py lam` → `inbox/nguoi_cay_2/manh/`)

Rig gốc là kiểu cắt giấy, thiết kế của mình có chỗ nối khác chất liệu (bắp tay dây leo lục ↔ cẳng tay gỗ nâu ↔ nắm tay) hoặc nấp sau lớp
phủ (u rêu vai, cổ áo lá, đai, váy lá) → mọi mảnh là **mảnh cứng**, không cần tờ "thân liền".
- Bốn tờ "đúng chỗ, đúng cỡ" từ concept (mỗi tờ giữ vài mảnh không chồng nhau, vẽ đủ phần khuất): `M_A` đầu, hai cẳng tay, hai ống chân,
  đai; `M_B` thân, hai nắm tay, hai bàn chân; `M_C` hai u rêu vai, hai đùi; `M_D` hai bắp tay. Cả bốn ra đúng chỗ ngay lượt đầu.
- Hai tờ mảnh rời: `M_S1` (5 lá sẫm, chòm râu, 4 lá nhạt, 3 cành khô, 3 dải rêu rủ), `M_S2` (quả cầu dây leo có gai, một dây gai dài duỗi thẳng).
- Mảnh rời đặt lên concept bằng (cuống, mũi, bề rộng) đọc trên concept kẻ lưới (`ROI`, `CANH` trong `nguoi_cay_manh.py`): 3 lá mào, 4 lá cổ
  áo, 11 lá váy (5 hàng sau + 6 hàng trước), 2 lá trên u vai, 6 dải rêu rủ, râu, 3 cành khô. Lá của tờ S1 có cuống nên kéo dài thêm 10 %
  về phía cuống (`CUONG`). Tờ so: `manh/_so_ghep.png` (concept | ghép lại); 35 ảnh, 47 mảnh.
- Thứ tự vẽ (sau → trước): tay xa (bắp, rêu rủ, cành, u rêu, lá, cẳng, nắm) → chân xa → chân gần → thân → váy (hàng sau, hàng trước) → đai
  → tay gần (rêu rủ, cành, bắp, cẳng, nắm, u rêu, lá) → cổ áo lá → mào → đầu → râu.

## 5. Rig (`nguoi_cay_rig.py` → `inbox/nguoi_cay_2/rig/`)

- **Dáng gốc của rig mình = khung 0 `idle_01` của họ** (thế thủ; concept vẽ theo dáng đó), không phải dáng gốc của họ. Đủ xương của họ (bỏ
  xương bóng, 4 mục tiêu IK); chân của họ chạy IK → dùng biến đổi riêng ĐÃ ÁP lấy mẫu bằng runtime thật (`<scan>/sample_goc.json`, trường `l`).
- Khớp khung concept ↔ rig: bình phương tối thiểu trên 9 cặp mảnh – part (1,658 px / đơn vị con gốc). Codex vẽ tay chân to hơn và choãi hơn
  rig (lệch 11–62 px) nên **mảnh chi đặt theo HAI KHỚP** đọc trên concept (`HAI`: khớp gốc → gốc xương, khớp ngọn → gốc xương con; co DỌC trục
  theo độ dài xương, bề ngang giữ nguyên), mảnh mút (nắm tay, bàn chân) đặt theo một khớp (`MOT`). Không làm bước này thì khớp lệch tới 56 px.
- Bàn chân của mình thấp hơn gốc rig 16 đơn vị → nâng cả con (xương `all`) cho đáy bàn chân ở y = 0.
- Thân: lưới 3 × 6, trên theo `bone5` (ngực), dưới theo `bone4` (eo), đai che chỗ nối với hông.
- Xương của mình (`x_*`): `x_vai_g/x` (u rêu, con của xương đòn, nhô theo bắp tay 14 %, tối đa 16°); mỗi lá mào, lá cổ áo, lá váy, dải rêu,
  râu, cành khô một chuỗi 1–2 đốt có lò xo (`MEM`, `hoat.LoXo`) + gió lệch pha (`gio`). Lá váy là con của hai chuỗi vạt váy của họ.
- **Mặt nạ mặt đất** (slot `cat`, luôn bật, y = −3): giấu phần thân dưới đất cho `appear`. Dây gai và quả cầu nằm ngoài mặt nạ.
- **Dây gai** (chiêu mana): chuỗi 10 đốt `gai0..9` trên `gai_goc`, con của `far` (chỗ đối thủ, game dời); lưới dải 31 × 3. **Quả cầu dây leo**
  (chiêu cuối): slot `cau` trên xương `cau` (con của `move`), ẩn sẵn. Cả hai là MẢNH CỦA RIG (đề xuất của Claude: vật cứng phải uốn / cầm
  trên tay); muốn chuyển sang VFX thì bỏ hai slot, sự kiện đã có sẵn.
- 126 xương, 50 slot, 467 đỉnh; chiều cao game 311; `.atomik` 306 KB. `game`: `lunge = [skill]`, `stay = [cast]`, `far = [cast]`.

## 6. Clip (viết trong `lam_clip` của `nguoi_cay_rig.py`: nền lấy mẫu của họ + tay FK đặt theo góc thế giới `tay()`)

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| appear | 2,1 s | mào lá + cành khô nhú khỏi đất, ngọ nguậy tới 0,30; cả người đội đất vọt lên tới 0,72 (hai tay khép sát); giương hai tay gồng gầm 1,08–1,52; về thế thủ | nhu 0; troi_len 0,30; gam 1,08 |
| idle | 4,0 s lặp | nguyên idle_01 (nhún thế thủ, nửa sau giơ nắm đấm xa) + gió trên lá, rêu; 2,2–3,4 s gầm gừ: chúi đầu, rung vai, siết nắm tay | |
| walk | 0,8 s lặp | run_01 chạy chậm lại | |
| attack | 1,17 s | thân: vặn người lấy đà rồi chồm tới của skill_01_1 (đã làm trơn); tay XA giơ nắm đấm lên cao ra sau đầu (0–0,26) rồi giáng thẳng tới (0,30–0,42), tay gần giật khuỷu về sau; lao 0,62 chiều cao | trung 0,42 |
| cast | 3,0 s | tay XA (bên phải hình) giơ lên trời (0,50), chém theo từng cú quật; BA dây gai nhú 0,62 / 0,74 / 0,84, quật ba kiểu 1,02 / 1,22 / 1,42 (xem 6c), siết 1,66–2,14, rút xuống đất | trieu 0,50; moc ×3; trung 1,02; quat 1,22, 1,42; troi 1,66; nha 2,14 |
| skill | 3,2 s | hai tay VỐC lên quá đầu, gần nhau (0,46); quả cầu dây leo lớn dần trên hai nắm tay tới 1,30, thân ngả dần, rung; nhún (skill_02 0,72 s) 1,52; nhảy tới, hai tay nện cầu xuống trước mặt 2,02; cầu bẹp rồi tan; đứng dậy, nhảy lùi về | tu 0,46; day 1,30; nhay 1,64; trung 2,02 |
| hit | 0,5 s | nguyên hit_01 | |
| die | 1,55 s | die_01 (lảo đảo, ngã sấp), các lớp lá cụp xuống, mờ dần | nga 0,55 |

Tay gần của chiêu cuối đi lên qua phía TRƯỚC thân (vốc lên) chứ không qua phía ngoài: nếu lên phía ngoài rồi đập xuống phía trước thì cả clip
tay quay trọn một vòng, khoá cuối lệch 360° so với idle và runtime quay ngược một vòng khi nối clip.

Xem: `inbox/nguoi_cay_2/rig/xem.html` (runtime Spine thật, nút từng clip); tờ khung `rig/khung_<clip>.png`; ảnh cận runtime thật `rig/that/`.

## 6b. Người dùng trả lượt rig đầu (2026-11-12) và cách sửa

- "Đánh thường lỗi, **tay đánh phải dơ lên chứ không phải chui vào trong**, đánh xong **tay lại xoay gần 1 vòng ngược lại** là sai."
- "chiêu cast phải **dơ cả 2 tay lên**, phần **vai rêu cũng phải rotate theo**."
- "chiêu cuối lỗi thấy **giật mấy frame**, thấy chân tay bị giật, phần vai cũng phải xoay."

Nguyên nhân đo được (`nguoi_cay_kiem.py`: góc nhảy giữa hai khung; `chay.py sample ... 60`: bước dời ở 60 khung/giây):
1. Nắm tay / cẳng tay / bắp tay nhảy 344–360° giữa hai khung ở appear, cast, skill: `huong()` so góc với dáng gốc để chọn bội 360°, sai khi cẳng
   tay hoặc thân đã quay quá nửa vòng. Sửa: chọn bội theo dáng gốc + tổng góc đã đặt lên xương và mọi xương tổ tiên.
2. Tay của clip nền (skill_01_1, skill_02: tay họ vung cả vòng, xương đòn vung theo) lẫn với tay tự viết. Sửa: `BO_TAY` bỏ hẳn xương đòn, bắp,
   cẳng, nắm khỏi clip nền ở attack và skill; tay hoàn toàn của mình.
3. Clip nền bật tức thì: skill_02 lúc rời đất cả thân vọt ~200 đơn vị trong một khung, bàn chân quay 122°, ống chân IK rung ±60°; skill_01_1 lúc
   chồm tới dời ~230 đơn vị trong một khung. Sửa: `lam_tron` lọc Gauss mọi kênh trong 0,78–1,36 s (skill_02) và 0,26–0,54 s (skill_01_1).
4. Chiêu cuối pha thẳng từ thế thủ vào giữa đoạn CHẠY lấy đà của skill_02. Sửa: pha dần 0,27 s sang dáng nhún (0,72 s) đứng yên, rồi mới chạy tiếp.
5. Rêu rủ quay cứng theo bắp tay, lò xo lật ±30° từng khung lúc tay vung nhanh. Sửa: gốc dải rêu giữ hướng thế giới (treo theo trọng lực).

Đổi theo lời dặn: đòn thường tay xa GIƠ nắm đấm lên cao ra sau đầu (0–0,26 s) rồi giáng thẳng tới (0,30–0,42); chiêu mana giơ CẢ HAI tay; **u rêu
vai xoay theo độ giơ của bắp tay** (`sau()`: tối đa 46°, tính theo cos góc giữa bắp tay và trục ngực nên tay lên đường nào cũng êm).
Sau khi sửa: không còn bước xoay ~360° ở clip nào; ở 60 khung/giây bước dời lớn nhất của nắm tay là cú nện (≈ 80 đơn vị / khung, cố ý).

## 6c. Lượt sửa thứ hai (2026-11-12)

Người dùng: "ok sửa chỗ bạn thấy chưa đẹp; chiêu cast **dơ 1 tay bên phải lên thôi**, **triệu hồi nhiều cây hơn cùng quật nhiều kiểu**".
("Bên phải" theo người xem = tay XA, tay đang giơ nắm đấm ở thế thủ. Lượt trước người dùng dặn giơ cả hai tay, lượt này đổi lại một tay.)

- **cast** (3,0 s): chỉ tay xa giơ lên (tay gần ghì thấp); mỗi cú quật của một dây là một lần tay chém xuống rồi bật lại. **Ba dây gai** (`GAI`,
  mỗi dây một chuỗi 10 đốt trên `far`, chung một ảnh, xếp sau → trước c, b, a), ba kiểu:
  - `a` "quan" (bên trái đối thủ, dài 1,55 chiều cao): nhú 0,62; ngả ra sau, quật vòng qua đầu 1,02 (khung trúng của game), quấn thành vòng;
  - `b` "ngang" (bên phải, dài 1,22): nhú 0,74; gập xuống quét ngang tầm chân 1,22, ngọn bị kéo trễ rồi móc ngược lên ôm đối thủ;
  - `c` "dap" (phía sau bên phải, dài 1,64, dày hơn): nhú 0,84; vươn thẳng thật cao, ngả ra sau, gập khúc giữa bổ ngọn từ trên xuống 1,42
    thành vòm chụp qua đầu, ngọn nảy một nhịp.
  Cả ba siết theo nhịp 1,66–2,14 rồi duỗi ra rút xuống đất. Sự kiện: `trieu` 0,50; `moc` ×3 (chuỗi kèm tên dây); `trung` 1,02; `quat` 1,22 và
  1,42; `troi` 1,66; `nha` 2,14.
- **skill**: lúc giơ, hai cổ tay nhắm hai điểm cố định phía trên ĐẦU (`giai_tay`: giải hai khúc tay, khuỷu chìa ra ngoài) thay cho góc cố định,
  nên thân nhún / chúi / nhảy thì hai nắm tay vẫn ngang nhau cùng đỡ quả cầu (đo: lệch 0–28 đơn vị, trước đó một tay tụt hẳn xuống).
- 148 xương, 52 slot, 653 đỉnh; `.atomik` 320 KB.

## 6d. Thứ tự lớp tay xa (2026-11-12)

Người dùng (kèm ảnh chụp tay xa giơ lên): "ở đây phần cánh tay layer phải ở dưới vai chứ". U rêu vai xa trước đó vẽ TRƯỚC cẳng tay và nắm tay
xa (theo concept: nắm đấm đè lên mép u rêu) nên tay giơ lên trông như mọc ra trước vai. Đổi `THU_TU`: u rêu vai luôn vẽ SAU (đè lên) cả cánh
tay của bên đó. Hệ quả ở dáng nghỉ: mép u rêu che một chút cổ tay / mép nắm đấm xa.

## 8. Dạng 1 (con non, `nguoi_cay_1`), 2026-11-12

Người dùng: "ok gen dạng 1 đi" → xem concept: "nhìn ổn". Thiết kế con non là đề xuất của Claude: cùng dáng thủ và CÙNG chỗ đặt thân, tay, chân
với dạng lớn (prompt "KEEP IDENTICAL / CHANGE" trên bản D, `build_nguoi_cay.py non`), đầu to tròn như cái nụ (chibi chỉ ở dạng 1), mày mảnh,
mắt cam to có con ngươi, miệng mím hai nanh nhỏ, mầm hai lá trên đầu, hai túm rêu vai nhỏ, cổ áo ba lá, váy năm lá ngắn, mỗi tay một dải rêu,
tay gỗ nhạt quấn dây leo trơn, không gai, không cành khô, màu lục non `#6FA24A`. Nắm tay Codex vẽ vẫn to gần bằng dạng lớn (đã báo, người
dùng không sửa).

- Mảnh: `build_nguoi_cay.py manh_non` (bốn tờ "đúng chỗ" A–D + tờ rời S1: 2 lá mầm, 3 lá cổ áo, 5 lá váy, 2 dải rêu), cắt bằng
  `NC_DANG=1 py -3 -I nguoi_cay_manh.py lam` (cấu hình riêng trong khối `if NC.K == 1`). Thân mầm là một que ngắn vẽ bằng mã (`mam_than`).
  Dây gai và quả cầu chép ảnh của dạng lớn. 32 ảnh, 30 mảnh.
- Rig: `NC_DANG=1 ... nguoi_cay_rig.py` (khối `if NC.K == 1`: `HAI`, `MOT`, `MEM`, `GAI`, `DK_CAU`). Cùng xương, cùng clip với dạng lớn; khác:
  chiêu mana MỘT dây gai nhỏ kiểu quật vòng rồi quấn (clip 2,64 s), quả cầu chiêu cuối nhỏ hơn (0,54 chiều cao). Hai điểm này là Claude
  tự chọn theo luật "mỗi dạng một chiêu, mạnh dần" vì người dùng chưa trả lời câu hỏi.
- **Tiến hóa** (`evolve`, 2,8 s): rig dạng 1 gộp bản nhẹ của dạng lớn (`NC_DANG=2 NC_NHE=1 ... nhe` → `_nhe.pkl`, `tienhoa.gop`); con non gồng,
  tan 1,05–1,35 s, dạng lớn hiện, bung tay, về đúng khung 0 idle của dạng lớn (lệch 0,00 px). Mặt nạ mặt đất phải bám xương riêng `dat`
  (bám thẳng `root` thì `gop` báo thiếu xương `n_root`).
- 98 xương riêng (247 khi gộp), `.atomik` 298 KB, 9 clip. Chiều cao game dạng 1 là 331 (đầu to), dạng lớn 311: cỡ hiển thị do `size` trong
  `heroes.json` quyết.
- Kiểm: không góc nhảy ~360° ở clip nào; lấy mẫu skill, cast, attack, appear, evolve trên runtime thật ở 60 khung/giây không có khung giật.
- Xem: `inbox/nguoi_cay_1/rig/xem.html`; tờ so hai dạng `inbox/nguoi_cay_1/so_hai_dang.html`.

## 9. Khớp chân không liền (2026-11-12, cả hai dạng)

Người dùng (ảnh chụp dạng 1): "chân bên phải hơi lỗi phần khớp cổ chân, cả con dạng 2 cũng vậy, **không liên kết**".
Nguyên nhân: mảnh chi đặt theo hai khớp bằng cách co giãn CẢ mảnh dọc trục cho vừa độ dài xương (đùi xa dạng 1: 1,59 lần, dạng 2: 1,52 lần),
nên hai đầu tròn cũng dài ra: đầu đùi thòi khỏi khớp gối sang bên kia ống chân, ống chân trông như một khối rời đặt trước chân.
Sửa (`chi()` trong `nguoi_cay_rig.py`): chỉ đoạn GIỮA hai khớp co giãn theo độ dài xương; phần ngoài hai khớp (hai đầu tròn) và bề ngang giữ
nguyên cỡ; mảnh chi thành lưới 9 × 9 bám một xương để theo được phép co từng đoạn. Áp cho bắp tay, cẳng tay, đùi, ống chân của cả hai dạng.
Soi lại bằng runtime thật (idle 0 / 1,3 / 2,6 s, cận phần chân): đùi nối thẳng vào ống chân, vòng dây leo nằm ngay trên bàn chân, ở cả hai chân.

## 7. Việc tiếp

1. Người dùng xem rig và clip, dặn sửa.
2. VFX của game: bụi đất lúc trồi lên, lá văng lúc đấm, gai / lá vụn lúc dây gai quật và siết, nổ lá khi quả cầu nện xuống (sự kiện đã đặt).
3. Vào game: tên, id, suất thứ 7 đảo Mộc, chỉ số, thẻ do người dùng đặt; chép `.atomik` + chân dung của CẢ HAI dạng vào `Assets/03 Art/Heroes/Resources/`. Lưu ý (phiên assets-aa báo 2026-11-12): `AolaSticker.Far` đã đổi cách dời khung camera cho tướng có mảnh bay (`game.far`): người cây có dây gai trên `far`, phải soi chiêu mana trong trận.
