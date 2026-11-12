# Hươu gỗ (`huou_go`): tướng thứ 4 đảo Mộc, hai dạng (dạng 1 khúc gỗ non, dạng 2 hươu cổ dài)

Bắt đầu 2026-11-12. Con gốc của rig: `monster_3504` (game tham khảo, kho `D:\Ripper\SwordxStaff`). Xương, lưới, chuyển động gốc là
của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình.

## 1. Lời dặn của người dùng (2026-11-12)

- Concept: sinh vật **lai hươu và hươu cao cổ, thân gỗ, lông là lá cây, kết hợp pha lê, đá**.
- Khác con gốc: **làm thêm mồm há / đóng được**.
- idle / walk: giống họ là ổn.
- Đánh thường: lao tới dùng sừng húc.
- Chiêu mana: hơi cúi đầu, tụ một quả cầu năng lượng nhỏ ở giữa hai sừng rồi bắn một tia từ quả cầu đó vào đối thủ.
- Chiêu cuối: đứng bằng hai chân, ngửa đầu há to mồm tụ một quả cầu siêu to, tụ xong gật đầu nện mạnh vào đối thủ.
- die: gục xuống. appear: mở một cánh cổng teleport kiểu rừng rồi sinh vật walk qua.

Màu, chi tiết, tên, số dạng: người dùng chưa dặn. Bảng màu ở mục 3 là **đề xuất của Claude**, chờ chọn hướng.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3504/`: `info.json`, `att_goc.json`, `manh_anh.png`, `manh_dang_goc.png`, `parts/`, `khung/`, `sample_dk.json`)

107 xương, 40 slot (34 hình đang bật; `wangge`, `shadow` trống; 4 slot lá rơi `P_weiba4..7` mặc định trống, dùng lại ảnh `P_weiba2`), 12
clip, 6 IK chân, atlas tỉ lệ ~0,33. Con gốc nhìn sang PHẢI (đầu quay ba phần tư, **lộ một mắt nhắm**, miệng chỉ là một nét nhỏ): không lật.

Cây xương: `root > all > xy` (dời cả con) `> bone3` (hông, góc gốc 90) `> bone4` (lưng) `> bone5` (ngực) `> bone6a > bone6b > bone6b2`
(cổ) `> bone7` (đầu). Con của đầu: bốn nhánh gạc (`bone10-11-32`, `bone33-34`, `bone35-36`, `bone37-38-39`), hai tai (`bone40..44`,
`bone45..47`). Bờm: `bone6b2 > bone6b7 >` bốn chuỗi (`bone6b3..`, `bone6b5..`, `bone6b6..`, `bone6b8-9`). Cụm pha lê + túm lông: con
của `bone5` (`bone59` gần, `bone60` xa). Đuôi: `bone3 > bone8 > bone9 >` các chuỗi lá. Chân trước `bone12-13-14` (IK `SR1`),
`bone17-18-19` (IK `SL1`); chân sau `bone22-23-70-24` (IK `R1`, `R2`), `bone28-29-71-30` (IK `L1`, `L2`). Thứ tự IK trong mẫu khung:
L1, L2, R1, R2, SL1, SR1.

Mảnh (sau → trước): chân sau xa (3 khúc), **bờm** `P_toufa` (72 đỉnh, 11 xương), pha lê + túm lông xa, chân trước xa (2 khúc), đuôi
(chùm lá `P_weiba3`, lá nhỏ, cán `P_weiba1`), **thân** `P_shenti`, chân sau gần (3 khúc + túm lá), tai xa, **cổ liền ngực** `P_bozi`
(43 đỉnh, 6 xương), chân trước gần (2 khúc), hai túm lông + bốn pha lê gần, ba nhánh gạc, **đầu** `P_tou` (CỨNG, một xương `bone7`),
tai gần, nhánh gạc gần. Pha lê là mảnh cứng một xương; mọi mảnh khác là lưới có trọng số (2–5 xương).
Đầu cứng một xương → **hàm dưới là mảnh thêm của mình** (xương `ham` con của `bone7`), con gốc không có.

Clip của họ: `idle_01` 5,33 s; `run_01` 0,53 s (phi nước kiệu); `skill_01_1/2/3` 1,17 s (chồm hai chân trước 0,26–0,39 rồi BỔ đầu
húc gạc xuống – tới 0,52–0,65, giữ tới 0,91); `skill_02` 1,47 s (dậm chân trước); `skill_03` 1,67 s (chồm rồi nhảy cao, đáp);
`hit_01/02`; `die_01` 1 s (chồm dựng người 0,11–0,22 rồi đổ nghiêng nằm xuống); `stun_01`; `block_01`.

## 3. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `ArtGen/Spine/huou_go.py` (`part_goc`, `bo_cuc [he|thu]`), `build_huou_go.py` (gói `gui_gpt/huou_go_2/`).
Sơ đồ bố cục = khối từng mảnh của rig làm trơn, tô phẳng theo nhóm màu của mình (không đính ảnh con gốc); đầu vẽ lại: sọ tròn + mõm
dài chĩa xuống phải, nét mắt nhắm, khe miệng. Tỉ lệ rig → khung concept 1,2817.

Giữ của con gốc: hướng nhìn, cổ dài dựng đứng, một mắt nhắm, bốn nhánh gạc, hai tai lá, bờm sau cổ, cụm pha lê ở vai, bốn chân, đuôi
cán + chùm lá. Của mình: mảng vỏ cây kiểu đốm hươu cao cổ, bờm là vòng lá to xếp lớp (không phải lông xù), gạc là cành cây có vân
nhựa và nụ lá, móng đá xám, đệm rêu + đá nhỏ ở chân cụm pha lê, mõm dài có khe miệng.

Lượt 1, hai hướng màu (tờ so `inbox/huou_go_2/so_hai_huong.html`), cả hai đạt điểm kiểm ngay lượt đầu:
- `he` (`tai_ve/L1_he.png`): gỗ sồi `#CDA670`, mảng vỏ `#8E623C`, gạc `#704C30`, lá lục `#569646` / `#92C458`, pha lê hổ phách `#F2B43E`.
- `thu` (`tai_ve/L1_thu.png`): gỗ bạch dương `#E2D6BA`, lá phong đỏ cam `#D66C32`, tai lá vàng `#F0AC3E`, pha lê lục bảo `#40CE96`.

**Người dùng chọn hướng B (`thu`) 2026-11-12**, dặn sửa: "bỏ mắt đi, làm mặt chiến hơn, mồm tách hàm". Bản đầu tôi giữ vẻ mặt
hiền của con gốc (mắt nhắm cười, miệng cười) và chỉ kẻ một nét miệng.

Lượt 1b (`gui_gpt/huou_go_2/luot_1b_mat_chien.txt` → `tai_ve/L1b_thu.png`; vẽ lại y hệt `L1_thu.png`, chỉ đổi mặt): KHÔNG mắt; một tấm
vỏ cây sẫm phủ trán, mép dưới thẳng xếch xuống phía mõm (kiểu mặt nạ gỗ ra trận); mõm dài, vuông hơn; hai hàm tách rời bằng khe răng
cưa (răng gỗ cùng màu thân, đan nhau, ngậm, khoé không cười); hàm dưới là khối cằm vuông viền kín có chốt bản lề. "Bỏ mắt" tôi hiểu
là không có mắt hẳn (diễn giải của tôi, chờ người dùng xem).
Codex hết hạn mức lúc 12:31, mở lại 14:16: `scratchpad/cho_gen.py` chạy nền tự gen sau 14:17 (có ảnh rồi thì thôi).

Chồng concept `thu` lên sơ đồ (`mau/_chong_thu.png`): GPT vẽ to hơn sơ đồ chừng 8% (chân dài hơn, móng ở y ≈ 990 thay vì 955, đuôi
thấp hơn, gạc rộng hơn), IoU cả con 0,76 → mảnh làm theo KHUNG PART (hình bóng của rig), concept là ảnh thiết kế; không cắt thẳng từ
concept.

## 4. Clip (dựng ở tầng điều khiển của rig gốc: `huou_go_clip.py`)

Xem thử trên rig gốc (hình của họ, nội bộ): `<SXS>/scan/monster_3504/lam_clip/xem/xem.html` (`huou_go_clip.py song`: trang sống 60
khung/giây, nút từng clip, tốc độ 1× / 0,5× / 0,25×; vòng tròn lục = quả cầu năng lượng; dòng "mồm há" = kênh hàm; ở appear vòng bầu
dục + mảng che = cánh cổng và phần bị mặt nạ giấu).

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| hg_idle | 5,33 s lặp | nguyên idle_01 | |
| hg_walk | 0,53 s lặp | nguyên run_01 | |
| hg_attack | 1,40 s | chạy lao tới 0,06–0,34 (run_01, đầu chúi); chồm lấy đà 0,34–0,47; BỔ đầu húc gạc 0,47–0,58 (skill_01_1 0,39 → 0,65); khựng tới 0,78; nhảy lùi về 1,22 | trung 0,58 |
| hg_cast | 2,35 s | cúi đầu 45% mức húc 0–0,36; tụ cầu nhỏ giữa hai gạc tới 1,00 (rung mạnh dần); bắn: đầu giật lên, thân giật lùi, ghìm tới 1,94; ngẩng, lắc đầu | tu 0,36; phun 1,00; het_phun 1,94 |
| hg_skill | 3,10 s | nhún, dựng hai chân sau 0–0,42 (dáng die_01 0,16 s + thân dựng thêm 11°); ngửa đầu há mồm 0,60; tụ cầu to trước mõm tới 1,80 (rung, chân trước đạp nhẹ); ngả sau lấy đà; gật đầu nện 1,96–2,08 (về dáng skill_01_1 0,65 s); khựng tới 2,50; ngậm mồm, về | tu 0,60; day 1,80; nem 2,02; trung 2,08 |
| hg_appear | 2,40 s | cổng mở 0–0,40; bước ra 0,46–1,62 (run_01 chậm 0,62 lần, từ sau 760 đơn vị, chậm dần); ngẩng đầu lắc bờm; cổng khép tới 2,10 | cong_mo 0; buoc_ra 0,46; cong_dong 1,66 |
| hg_hit, hg_die | 0,5 s; 1,0 s | nguyên hit_01, die_01 | |

Kênh riêng cho rig của mình (`<scan>/kenh_rieng.json`): `ham` 0..1 (độ há mồm), `cau` (bán kính đơn vị rig, x, y thế giới: cầu mana
46 giữa hai gạc; cầu chiêu cuối 175 trước mõm), `bay` (xương `move`: đòn thường tới trước 430; appear từ −760), `cong` 0..1 (cổng mở).
Mặt cổng ở x = −400 (sau đuôi khi con vật đã tới chỗ).

Bản đầu chiêu mana cúi 100% mức húc: cổ gập hẳn, không còn là "hơi cúi" → `C_MUC` 0,45.

## 4b. DẠNG 1: khúc gỗ non (người dùng 2026-11-12, kèm ảnh chụp `monster_3304`: "lấy con này làm dạng 1")

Con hươu cổ dài (`monster_3504`) thành **dạng 2**: thư mục đổi `inbox/huou_go_1` → `huou_go_2`, `gui_gpt/huou_go_1` → `huou_go_2`.
`huou_go.py` đọc dạng ở biến môi trường **`HG_DANG`** (1 | 2, mặc định 2; `MON` theo dạng); `build_huou_go.py` là gói dạng 2,
`build_huou_go_non.py` là gói dạng 1; `huou_go_clip.py` hiện chỉ cho dạng 2 (rig `monster_3504`).

Mổ rig `monster_3304` (`<SXS>/scan/monster_3304/`): 46 xương, 26 slot (24 hình bật), 10 clip, 4 IK chân (`tuiR_H`, `tuiR_Q`, `tuiL_H`,
`tuiL_Q`: mỗi chân hai xương, đích nằm trên đất). Con gốc nhìn sang PHẢI: không lật.
- Cây xương: `root > bone40 >` `bone` (mông: `P_shenti`; chân sau `bone2-3`, `bone4-5`; đuôi `bone14 >` ba chuỗi lá `bone15..17`,
  `bone18..20`, `bone21..23`) và `bone6 >` chân trước `bone27 > bone7-8`, `bone28 > bone9-10`; `bone11 > bone12 > bone13` (KHÚC GỖ
  `P_tou` = đầu liền ngực, 24 đỉnh, bám `bone, bone6, bone12, bone13`) `>` mồm `bone24`, ụ mắt gần `bone25 > bone26`, ụ mắt xa `bone39`,
  hai cành gạc `bone29` (+ lá `bone31-32`, `bone33`), `bone30` (+ lá `bone34`, `bone35-37`, `bone38`).
- Thứ tự vẽ: ba lá đuôi, gạc + lá bên xa (`JiaoL_*`), gạc + lá bên gần (`JiaoR_*`), ụ mắt xa `YanL_01`, hai chân sau (mỗi chân 2 khúc),
  mông `P_shenti`, khúc gỗ `P_tou`, MỒM `zuiba` (ba hình cùng lưới 4 đỉnh: `zuiba` há chữ w lộ lòng lam, `zuiba2` nét ^ ngậm lúc gồng,
  `zuiba3` răng cưa lúc đau / chết), ụ mắt gần `YanR_02` + lòng mắt `YanR_01`, hai chân trước.
- Clip của họ: `idle_01` 2 s; `run_01` 0,53 s (nước kiệu); `skill_01` 0,83 s (rạp người HÚC gạc tới trước 0,19–0,37, bật về);
  `skill_02` 1,33 s (nhảy vọt lên rồi lao xuống đập, mồm ^); `die_01` 1 s (bị hất tung, rơi nằm bẹp, mồm răng cưa); `floating_01`
  1,5 s (bị hất tung rồi đứng dậy); `hit_01/02`; `stun_01`; `block_01`.

Concept dạng 1 (màu hướng B đã chọn; kiểu mặt là đề xuất của Claude, chờ người dùng chọn): sơ đồ `HG_DANG=1 huou_go.py bo_cuc` →
`inbox/huou_go_1/mau/bo_cuc_<kiểu>.png` (tỉ lệ rig → khung 2,0879). Khúc gỗ bạch dương có mảng vỏ sẫm, hai cành gạc chữ Y có lá
phong đỏ cam + lá vàng, ba lá đuôi, bốn chân móng đá, một nụ pha lê lục bảo tí hon trên mông (mảnh thêm, cứng), mồm là khe răng cưa.
- `mat` (`tai_ve/L1_mat.png`): hai ụ mắt của con gốc thành hốc gỗ rỗng sẫm (không con ngươi), nét mày xếch.
- `khong_mat` (`tai_ve/L1_khong_mat.png`): không mắt như dạng 2: ụ thành mấu cành cụt có vân vòng, mũ vỏ sẫm trên trán mép xếch.
**Người dùng chọn kiểu B (`mat`) 2026-11-12**, dặn: "dạng 1 theo hướng B nhưng làm mắt kiểu lác lác ngơ ngơ". Lượt 1b (vẽ lại y
hệt `L1_mat.png`, chỉ đổi mắt: hai con ngươi nhìn hai hướng, ụ mắt bên phải quay ra cho lộ mắt, bỏ nét mày xếch), hai cách vẽ:
- `nhan` (`tai_ve/L1b_lac_nhan.png`): tròng kem tròn trong hốc gỗ, con ngươi chấm sẫm nhỏ (trái nhìn lên – ra ngoài, phải nhìn xuống):
  đọc ra "lác, ngơ" rõ nhất.
- `dom` (`tai_ve/L1b_lac_dom.png`): hốc sẫm + chấm kem: GPT vẽ thành mắt đen to có chấm sáng, ít lác hơn.
Tờ xem cả hai dạng: `inbox/huou_go_xem_concept.html`. Dạng 1 ngơ, dạng 2 "chiến" (không mắt).

Clip dạng 1: người dùng chưa dặn; đề xuất làm cùng bộ ý với dạng 2 ở mức nhỏ hơn (húc = skill_01 của họ; chiêu mana, chiêu cuối
tụ cầu nhỏ hơn), chờ người dùng.

## 4c. Dạng 1: người dùng chốt mắt lác **cách 2 (`dom`)** 2026-11-12 → `inbox/huou_go_1/tai_ve/L1_duyet.png`; mảnh, clip, rig

- **Mảnh theo khung part** (`HG_DANG=1 huou_go.py nhom_part | cat_part <tờ> | so_part`; prompt `build_huou_go_non.py` → bốn file
  `gui_gpt/huou_go_1/luot_2_manh_A..D.txt` → `tai_ve/N_A..D.png`, mỗi tờ 60–90 giây, đạt ngay lượt đầu, IoU 0,87–0,98):
  A (×4) khúc gỗ, mông, hai ụ gỗ, mắt gần; B (×5) hai cành gạc, năm lá; C (×5) ba lá đuôi, mồm ngậm (chỉ một nét răng cưa), `mieng_ha`
  (mồm há), `pha_le` (nụ pha lê), `mat_xa` (ụ mắt xa có mắt); D (×6) tám khúc chân (bốn khúc dưới có móng đá).
  Màu gỗ trên tờ mảnh trùng concept (trung vị 242, 217, 166 so với 244, 221, 171): không phải cân màu.
- **Clip** `huou_go_non_clip.py` (sinh từ khung chung của `huou_go_clip.py`; kênh, lệnh như dạng 2; trang xem trên rig gốc
  `<SXS>/scan/monster_3304/lam_clip/xem/xem.html`): hn_attack 1,15 s (chạy lao, rạp người húc = skill_01; trung 0,46), hn_cast
  2,20 s (cúi 60%, cầu nhỏ giữa hai cành gạc, phun 0,90, het_phun 1,84), hn_skill 2,80 s (ngả ra sau, há mồm 0,52, tụ cầu tới 1,55,
  gật nện 1,70–1,82 về dáng skill_01 0,28 s), hn_appear 2,15 s (cổng, chạy nước kiệu từ −420), idle / walk / hit / die nguyên của họ.
  Clip dạng 1 là ĐỀ XUẤT của Claude (người dùng chưa dặn riêng).
- **Rig** `huou_go_non_rig.py` → `inbox/huou_go_1/rig/` (`xem.html`, `huou_go_1.atomik` 152 KB, 50 xương, 27 slot, 8 clip; nối clip 0
  px; runtime Spine thật dựng đủ: `rig/spine_that/`). Nguyên lưới của họ cho 24 part; mảnh thêm: `mat_xa` (bone39, tâm ngay mép phải
  khúc gỗ), `pha_le` (xương mông `bone`), `mieng_ha` = hình thứ hai của slot `zuiba` (lưới 4 đỉnh bám `bone24`; bật khi kênh `ham` >
  0,5). Xương thêm: `move`, `mieng` (giữa hai cành gạc), `cau` (con của move: chỗ + cỡ cầu, tỉ lệ = bán kính / 100), `mat_cong` (mặt
  nạ nửa mặt phẳng bên phải mặt cổng, để xa 3000 ngoài appear), `cong`.
  Lỗi đã gặp: `sk.manh(slot, ..., xuong=khác xương của slot)` xuất region lệch chỗ (mồm há rơi xuống chân) → dùng `luoi_gan` 4 đỉnh.
- **Cổng rừng** (dùng chung hai dạng): `gui_gpt/huou_go_1/luot_3_cong.txt` → `tai_ve/cong.png`; `HG_DANG=1 huou_go.py cat_cong` tách
  `manh/cong/cong_sau.png` (cả cổng) + `cong_truoc.png` (nửa vành trái, vẽ trước con vật); rig tự gắn khi có ảnh.

## 4d. Dạng 2: lượt 1c (người dùng gửi nhầm sang phiên tuong_da, phiên đó chuyển tiếp nguyên văn 2026-11-12)

"dạng 2 bỏ phần nâu ở trên đầu cũng đốm nâu đi, phần bụi rêu và pha lê cho ra sau lưng" → `luot_1c_dau_dom_pha_le_lung.txt` →
`tai_ve/L1c_thu.png`: bỏ tấm vỏ nâu trên trán, cả đầu gỗ sáng có đốm nâu như thân (vẫn không mắt, hàm răng cưa); bỏ hai cụm pha lê +
rêu ở vai, MỘT cụm bốn pha lê trên đệm rêu nằm trên sống lưng. Chờ người dùng xác nhận (lời dặn tới qua chuyển tiếp).
Việc của rig dạng 2: pha lê / rêu của họ bám `bone59`, `bone60` (con của ngực `bone5`); cụm trên lưng của mình bám xương lưng
(`bone4` / `bone3`), bỏ các part pha lê + túm lông ở vai.

## 4e. Sửa dạng 1 sau khi người dùng xem rig (2026-11-12)

- "mắt bên phải dạng 1 nhìn không giống mắt bên trái", rồi "bạn xem con gốc mắt bên kia không thấy tròng mắt đâu, chỉ thấy mắt nó lồi
  ra thôi" → BỎ mảnh `mat_xa` (ụ mắt xa có tròng, tôi thêm theo concept); bên phải chỉ còn ụ gỗ `YanL_01` của rig như con gốc.
- (chuyển tiếp qua phiên Gạc Đá) "dạng 1 ở các khớp nối chân, thân bỏ outline đen đi để liền mạch", rồi kèm ảnh cận ranh mông – khúc gỗ:
  "phần này vẫn có outline, xem cả cho dạng 2" → `xoa_muc_noi` trong `huou_go_non_rig.py` (bảng `NOI`: cặp mảnh trên / mảnh dưới):
  ở dáng gốc, cả VÀNH MÉP (7 px ảnh atlas) của mảnh trên mà rơi sâu trong mảnh dưới thì lấy màu gỗ sạch gần nhất. Phải xoá cả điểm khử
  răng cưa của vành, không riêng điểm mực (bản đầu chỉ xoá điểm tối: còn một vòng chấm sáng quanh khớp). Gồm cả ranh mông – khúc gỗ
  (bản đầu tôi giữ vì concept có nét đó: bị trả). Dạng 2 dùng cùng hàm (`huou_go_rig.py`, bảng `NOI` riêng).
- Cổng rừng đã vào rig dạng 1 (`cong_sau` sau mọi thứ, `cong_truoc` = nửa vành trái trước mọi thứ, mặt nạ nửa mặt phẳng ở tâm cổng).

## 4f. Dạng 2: người dùng duyệt `L1c_thu.png` ("ok dạng 2 mới ổn", 2026-11-12) → `inbox/huou_go_2/tai_ve/L1_duyet.png`; mảnh và rig

- Bốn tờ theo khung part (`HG_DANG=2 huou_go.py nhom_part`; `build_huou_go.py` → `luot_2_manh_A..D.txt` → `N_A..D.png`): A (×3,6) bờm lá,
  cổ liền ngực; B (×3,0) thân, bốn nhánh gạc; C (×4,0) hai tai, chùm đuôi, cán đuôi, hai lá nhỏ, túm lá chân; D (×4,2) mười khúc chân.
  KHÔNG có sáu pha lê + ba túm lông ở vai và đầu của họ (bỏ ở rig: `BO_PART`).
  Đốm vỏ trên tờ hướng dẫn: bản đầu nhiều mảnh nhỏ tam giác → GPT vẽ theo, khác đốm sáu cạnh to của concept → đổi thành lục giác to
  (bán kính 0,17 × căn diện tích mảnh), gen lại A, B (`N_A_2`, `N_B_2`).
- Hai tờ "đúng chỗ, đúng cỡ" từ concept: `M_E1` (đầu không hàm dưới + cụm pha lê trên rêu), `M_E2` (hàm dưới). Đặt vào rig bằng phép
  khớp concept ↔ sơ đồ (`huou_go_rig.py khop`: s = 0,94, dời (24, −8) px, IoU 0,86; ảnh chồng `mau/_khop.png`).
- Rig `huou_go_rig.py`: xương `ham` (con `bone7`, ở chốt bản lề đọc trên concept `CHOT_PX`), kênh `ham` → xoay −34° × ham; `hong` = lưới
  4 đỉnh màu sẫm căng giữa hai hàm (hai đỉnh bám `bone7`, hai đỉnh bám `ham`); `dau` cứng trên `bone7`, `pha_le` cứng trên xương lưng
  `bone4` (vẽ ngay sau thân); bốn slot lá rơi `P_weiba4..7` ẩn sẵn, hiện theo trường n, a của mẫu.

## 4g. Chỗ nối liền mạch: cách cuối cùng (2026-11-12, sau ba lần người dùng trả: "vẫn bị lỗi nhỏ ở gần chân", "phần chân bị lem nhem khá nhiều")

`xoa_muc_noi(A, B)` trong `huou_go_non_rig.py` (dạng 2 chép nguyên khối hàm sang `huou_go_rig.py`, `SAU` 7 thay 11 vì ảnh nhỏ hơn):
- Tiêu chí: xoá vành mép của A (mực + điểm khử răng cưa) ở những điểm nằm HẲN BÊN TRONG khối hợp A ∪ B ở dáng gốc, sâu hơn `SAU` px
  ảnh atlas kể từ viền ngoài của khối hợp, và có B ở dưới. Tiêu chí cũ "nằm sâu trong B" làm khúc chân dưới mất viền hai bên (mép nó
  gần trùng mép khúc trên) và đáy khúc gỗ nham nhở (trùng đáy mông).
- `SAU` phải đủ lớn (11 px ≈ 6 đơn vị): xoá là nướng theo dáng gốc, lúc idle / walk khúc chân trượt ra khỏi thân vài đơn vị; xoá nông
  thì lộ đoạn mép không viền ngay dưới mép thân.
- Chỗ nối nằm rất sâu: cho mép mảnh ĐẶC và nới 5 px màu gỗ (mép mềm nửa trong suốt gỗ-đè-gỗ hiện thành quầng sáng ở trang xem Spine).
- Cặp có cờ `"mo"` (mảnh A vẽ TRƯỚC thân có đốm: khúc chân trước trên; dạng 2: đùi gần, chân trước gần): phần A nằm rất sâu trong B mờ
  dần tới trong suốt, để đốm của thân hiện xuyên qua thay vì bị khối gỗ không viền che cụt.
- `got_mong`: cắt phần mông khuất sau khúc gỗ (viền đáy của nó thò ra dưới đáy khúc gỗ thành vệt lông tơ đen) và bỏ mảng vỏ trên mông
  (bị mép khúc gỗ cắt đôi). So chỗ nối với ảnh mông CHƯA cắt.
- Gỡ lỗi: `HG_AN=slot,slot huou_go_non_rig.py soi ...` ẩn vài slot để xem lớp dưới; soi bằng runtime Spine thật phóng to:
  `chay.py sheet <rig> huou_go_1 <ra> "anims=idle,walk&n=4&tw=760&th=420&cols=4&view=-10,45,300,165"`.
- Giới hạn còn lại: ở dáng xa dáng gốc (walk duỗi hết cỡ) đầu khúc chân trước xa lộ một khấc nhỏ ở mép thân.

Dạng 2 đã dựng: `inbox/huou_go_2/rig/` (`xem.html`, `huou_go_2.atomik` 427 KB, 112 xương, 35 slot, 8 clip, nối clip 0 px; runtime Spine
thật dựng đủ sáu clip chính: `rig/spine_that/_het.jpg`). Hàm dưới há trong chiêu cuối, cổng rừng dùng chung ảnh với dạng 1.

## 4h. THÂN LIỀN thay cho mọi bản vá chỗ nối (2026-11-12, cách đang dùng cho cả hai dạng)

Người dùng trả tiếp "nhìn dạng 1 chân vẫn lem nhem", rồi "dạng 2 chân nối với cơ thể chân trước chưa match, trong skill tôi đã note là
gen cả rồi cắt ra để lúc nối cho match cơ mà, đọc kĩ lại skill rồi bổ sung". Mục 4g (xoá nét mực theo cặp mảnh, mờ mép, gọt mông) là
LÀM SAI luật "các khúc nối nhau gen LIỀN một ảnh rồi cắt": đã bỏ hẳn (hàm còn trong file rig, không gọi). Skill đã bổ sung.

- `HG_DANG=k huou_go.py to_lien` → `mau/lien.png` + `lien.json` + prompt `gui_gpt/huou_go_k/luot_2_than_lien.txt`: hợp hình bóng các
  mảnh thân + chân phía gần ở dáng gốc thành MỘT hình (chỉ viền ngoài), mỗi chân phía xa là một hình liền riêng ở hai bên tờ
  (`LIEN_K`: dạng 1 gần = khúc gỗ, mông, chân sau gần, hai chân trước; xa = chân sau xa. Dạng 2 gần = cổ, thân, chân sau gần, chân
  trước gần; xa = chân sau xa, chân trước xa).
- Đốm trên tờ hướng dẫn: mỗi đốm nằm TRỌN trong phần riêng của một mảnh (không chạm vùng hai mảnh chồng nhau), cỡ theo mảnh; dạng 1
  chân để gỗ trơn, nửa trên khúc gỗ (mặt) để trơn. Bản đầu đốm lấn vào vùng khúc chân → chân nhấc là đốm bị xẻ đôi.
- `cat_lien` nướng `tai_ve/N_lien*.png` vào khung từng part (pixel khung → thế giới dáng gốc qua lưới → tờ, lấy mẫu song tuyến nhân
  sẵn alpha), alpha nhân với HÌNH BÓNG của chính part (nới 0,7·z, mép mềm): lấy cả khung lưới thì mảnh mang theo mép thẳng của lưới.
  Ghi đè `manh/part/<hình>.png` của các ô gen riêng (tờ A, D dạng 1; A (cổ), B (thân), D dạng 2 không còn dùng cho các mảnh này).
- Rig không còn bước xoá mực; lắp bằng `gan_nguyen` như thường.

- Chiêu cuối dạng 2 (người dùng 2026-11-12, xem rig: "chiêu cuối dạng 2 không stretch chân trước và chân sau, làm nó đứng lên thôi là
  được"): die_01 / skill_01_1 của họ khoá TỈ LỆ xương chân (tới 1,4 lần) và tôi còn nhấc hông thêm 22 → chân dài ngoằng. `skill()` giờ
  trả tỉ lệ mọi xương chân (`CHAN`) về dáng gốc suốt clip và hạ hông 18 (`S_HA_THAN`) để hai móng sau vẫn chạm đất.

- Người dùng xem lại: "tôi vẫn thấy bị stretch". Nguyên nhân THẬT không phải tỉ lệ xương: DA khúc chân dưới bám một phần vào xương bàn
  chân (`bone15`, `bone20`, `bone25`, `bone31`), xương này là con của ĐÍCH IK. (1) Thân bị nâng quá tầm với của chân sau (móng ghim trên
  đất) → da kéo dài. (2) Clip của họ khi cho chân sang FK thì bật ràng buộc transform để bàn chân theo chân; mẫu `u`, `k` của mình không
  mang độ trộn transform → bàn chân nằm lại ở đích cũ. Sửa trong `huou_go_clip.py`: `chuan_ik` (mọi clip: chân nào IK < 1 thì dời đích
  tới đầu mút FK của chân, xoay đích theo góc lệch của ràng buộc, rồi đặt IK = 1) và `dung_len(e)` (dáng đứng tự dựng từ dáng nghỉ thay
  cho dáng die_01: xoay `bone3` 30°, đùi sau `bone22` / `bone28` xoay ngược 30° để giữ hướng, chân sau xa lùi 34, vòng lặp hạ hông tới
  khi hai chân sau trong tầm với `TAM_VOI`, hai chân trước FK co lên). Bài học: chân "dãn" thì đo khoảng hông → đích so với chiều dài
  chuỗi xương trước, đừng chỉ nhìn khoá tỉ lệ. Đòn thường (`hg_attack`) vẫn dùng cú chồm của họ (có khoá tỉ lệ chân của họ), chưa đổi.

## 4i. Tiến hóa, tên, vào game, VFX (2026-11-12; người dùng: "đòn thường tôi thấy ổn rồi, làm clip tiến hóa đi, tên bạn tự đặt, vfx tự làm nốt")

- **Tiến hóa** (`huou_go_non_rig.tien_hoa`, clip `evolve` 3,24 s trong `huou_go_1.atomik`, 409 KB): rig dạng 1 gộp BẢN NHẸ của dạng 2
  (`HG_NHE=1 huou_go_rig.py nhe` → `inbox/huou_go_2/rig/_nhe.pkl`: rig ảnh 0,72 px/đơn vị + các khung `appear` + khung 0 idle + chiều cao;
  dạng sau co 0,527 trong rig gộp). Cổng rừng của dạng 2 mở phía sau 0–0,35; dạng 1 quay đầu (lật `move` 0,30–0,46), chạy nước kiệu
  vào cổng, mặt nạ của dạng 1 dời về mặt cổng dạng 2, khuất hẳn 1,15; 1,30 dạng 2 bước ra bằng đúng các khung `appear` của nó (từ mốc
  bước ra), cổng khép; khung cuối trùng khung 0 idle dạng 2 (0,00 px). Sự kiện: cong_mo 0, chay_vao 0,52, doi_dang 1,30, cong_dong 2,50.
- **Tên (Claude đặt)**: tướng **Lộc Phong** ("Hươu gỗ rừng phong", "Dòng Lộc Phong"); dạng 1 **Gốc Ngơ**, dạng 2 **Lộc Phong**; thẻ chiêu
  mana **Tia Gạc Phong**, chiêu cuối **Cầu Rừng Thu**; thẻ nội tại giữ "Bờm Dựng".
- **Suất**: tướng thứ 4 đảo Mộc = ải 15 = id `bom_la` (`IslandGen` "Rừng Dây Leo"). GIỮ id (bờm lá vẫn đúng với bờm lá phong): không đổi
  SaveData / saveVersion / golden; chỉ đổi tên hiển thị trong `heroes.json`, `cards.json` và thay rig + chân dung ở
  `Assets/03 Art/Heroes/Resources/bom_la_1`, `bom_la_2` (chép tay từ `inbox/huou_go_k/rig`; đã ghi `quai/da_nhan.json`).
- **VFX** `Assets/01 Script/Game/Battle/HatLoc.cs` (partial `HatLua`, dùng lại `CauLa` / `GatherLa` của Gạc Đá và `NTia`):
  `n_cau_tia` (chiêu mana: lá, gió hút về điểm `mieng` giữa hai gạc từ lead − 0,62 s, cầu nhỏ 0,11 × cao, chớp, bắn tia 0,88 s, cầu cạn
  dần) và `n_cau_mom` (chiêu cuối: tụ cầu 0,36 × cao chếch trên mõm từ lead − 1,45 s, đầy lead − 0,28, ngả sau, rời mõm lead − 0,06, lao
  chéo xuống thân đối thủ, nổ lá + vòng lan + chớp màn). Nối: `HatNuoc.PlayNuoc` (2 case), `HoldNuoc` (n_cau_tia 0,93 s), `WThemes`
  "bom_la" (lục bảo, sao vàng), `StageView.MocFx` "bom_la", menu thử `PokiClash/Thử/Đảo Mộc: cầu năng lượng Lộc Phong…`.
- **Đã kiểm trong Unity (2026-11-12 chiều, qua cầu MCP cổng 8080)**: biên dịch không lỗi; `Nhập dữ liệu` (88 tướng); Play từ Boot, chạy
  menu thử 4 lượt, soi ảnh chụp `Temp/PokiShots/thuy_fx/bom_la_*`. Sửa sau khi soi:
  - cầu chiêu cuối bản đầu (0,50 × cao ra trước) cách mõm ~100 px: đo mõm lúc ngửa đầu trên ảnh chụp (dạng 2 ở −0,05; 0,88 × cao so
    với chân; dạng 1 ở −0,15; 0,75) → `NCauMom(…, truoc, len)`: dạng 2 (0,22; 1,15), dạng 1 (0,10; 1,02) qua mã riêng `n_cau_mom1`;
    cầu to lên 0,36 × cao ("siêu to").
  - cầu chiêu mana bị một đám giọt che: `NTia` tự tụ giọt + cầu nước ở miệng từ lúc gọi; gọi từ đầu clip thì đám đó hiện suốt lúc
    đầu chưa cúi. Sửa: gọi `NTia` ở lead − 0,14 s (trong `At`), giờ trúng tự tính lại = lead + quãng bay; cầu 0,11 × cao, gió hút thưa lại.
  - chưa xem: hộp chi tiết tướng, nút Tiến hóa trong game (clip `evolve` mới soi trên trang xem của rig), chiêu mana dạng 1 (menu
    thử chỉ bắn mana ở dạng cuối).
- **Cỡ trong game** (người dùng 2026-11-12: "làm dạng 1 trong game nhỏ đi, còn 0.8"): `heroes.json` `size` và `forms[0].size` của
  `bom_la` 0,92 → 0,8 (dạng 2 giữ 1,1). Golden không chứa cỡ.

## 5. Việc tiếp

1. Người dùng chọn hướng màu (hoặc dặn sửa) → `tai_ve/L1_duyet.png`; xem clip trên rig gốc.
2. Mảnh theo khung part (`thiet_ke(part)` nướng concept vào khung ảnh vùng, tờ hình bóng kín, `cat_part`, `so_part`, `noi_part`); mảnh
   thêm: hàm dưới + lòng miệng (đầu hai hình: ngậm / há, hoặc hàm xoay quanh khoé), cánh cổng rừng (một ảnh, tách lớp sau / trước).
3. Rig `huou_go_rig.py`: đủ xương, nguyên lưới của họ; xương `ham`, `cau`, `move`; mặt nạ cắt cho appear; `.atomik`; soi runtime thật.
4. VFX (lớp riêng): cầu + tia mana từ `cau`, cầu to chiêu cuối, cổng rừng (lá xoáy), bụi lúc dộng chân.
5. Vào game: tên, suất đảo Mộc (id), chỉ số, số dạng do người dùng đặt.
