# Thú một sừng bốn chân (`giac_moc`): tướng thứ 9 đảo Mộc (suất `moc_tinh`, ải 60 "Hang Pha Lê Lục")

Bắt đầu 2026-11-13 ở máy ổ D. Con gốc của rig: `monster_3804` (game tham khảo, `D:\RefAnimation\SwordxStaff`), **do người dùng chỉ** (ảnh chụp
trang xem, clip `skill_01_3`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là
thiết kế của mình. Tên, id game, số dạng: chưa đặt (`giac_moc` là mã làm việc).

## 1. Lời dặn của người dùng (2026-11-13)

- "tướng thứ 9 của đảo mộc; concept là **1 sinh vật lớn, đi lại bằng 4 chân, có 1 sừng ở trên đầu**, các phần trên lưng bạn có thể chủ động
  **đổi thành dây leo, hoa**,...".
- appear: "làm nó **nhảy vào** thôi". idle: "làm **giống họ** cũng được". run và die: "làm **giống họ**".
- Đánh thường: "làm giống skill 1, **dậm chân mạnh tạo vết nứt tới đối thủ** (fx làm riêng)".
- Chiêu mana: "làm giống `skill_02`, **ngẩng lên tụ cầu năng lượng ở trên đỉnh sừng rồi cúi xuống phóng tia năng lượng từ cầu**".
- Chiêu cuối: "kết hợp kiểu `open_01` để **mở phần bụng**, sau đó `open_02` để **hold lúc mở**; trong phần bụng sẽ có **1 quả cầu năng lượng
  kiểu trái tim phát sáng (luôn có sẵn)**, nó sẽ **phát sáng cực mạnh rồi bắn ra 1 tia sáng cực mạnh chết chóc** vào người đối thủ".
- "**trước khi làm cho tôi xem concept**, khi đã chốt concept thì làm và sửa trong auto mode, gọi gpt gen ảnh".
- Nhắn thêm lúc đang mổ: "tướng này phức tạp, **trước khi gen nên tách kĩ từng animation con gốc xem họ tách part thế nào, đọc kĩ skill**".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3804/`)

File: `info.json`, `att_goc.json`, `att_idle0.json`, `att_open.json` (open_02 @ 0,5 s), `att_cui.json` (skill_02 @ 1,45 s), `att_dam.json`
(skill_01_1 @ 0,59 s), `att_die.json` (die_01 @ 1 s); tờ khung 17 clip `khung/<clip>.jpg`; tờ mổ từng part `mo/idle0_0..5.jpg` + bảng
`mo/idle0_bang.txt`; tờ nhóm màu `mo/nhom_<dáng>.jpg` (idle0, open, cui, dam, die); từng part cắt theo lưới `parts/` + `parts/_tong.jpg`.
Script: `ArtGen/Spine/giac_moc.py` (`mo`, `nhom`, `part_goc`). (`manh_dang_idle0.png` 145 MB do `to_manh.py dang` sinh ra là file hỏng cỡ, không dùng.)

**Số liệu:** 268 xương, 143 slot, **136 hình, tất cả là lưới** (trừ 2 region nhỏ), 17 clip. 8 IK (bốn chân, mỗi chân hai khúc + bàn), **43
path constraint** (thân, cổ, vỏ ngực chạy trên 6 đường cong `lujin_*`), 1 transform constraint, **8 physics constraint** (chuỗi lông lưng).
Con nhìn sang PHẢI, lộ một mắt (mắt vẽ liền trong ảnh đầu), **không có mảnh hàm, không mảnh mắt nhắm, không đuôi**.

**Mọi clip chỉ có khoá xoay / dời / tỉ lệ của xương**: KHÔNG clip nào đổi ảnh, đổi độ đậm, đổi thứ tự vẽ hay bẻ đỉnh lưới. Bộ mảnh và thứ tự
chồng giống hệt nhau ở mọi clip; cái khác nhau giữa các clip chỉ là chỗ nào bị lộ ra.

### Bảng mảnh (thứ tự vẽ sau → trước)

| thứ tự | slot của họ | số | là gì | xương bám | ghi chú |
|---|---|---|---|---|---|
| 1–2 | `P_beifa_2/1` | 2 | hai túm tóc trắng sau đầu (phía xa) | 5–6 xương `toumao_*` | |
| 3–18 | `B_beimao_*` | 16 | **bờm lưng**: 12 mảng lông sẫm to hình ngọn lửa / dải dài có ngọn tím + 4 sợi râu mảnh (cùng ảnh `B_beimao_04`, 296 × 26) | mỗi mảng 4–13 xương (chuỗi `timao_*`, `baimao_*`), có physics | mềm nhất con; ba mảng `_11/_12/_13` dùng chung một ảnh |
| 19–27 | `TH_tuiL_*` | 9 | chân SAU phía xa: đùi, ống, bàn, 4 ngón có móng, 2 gai gót | bone6–11, IK `THL_*` | |
| 28–39 | `TQ_tuiL_*`, `P_tuimao_L*`, `P_tuijiao_L01` | 12 | chân TRƯỚC phía xa + 3 túm lông + 1 gai vai to | bone32–34, IK `TQL_*` | gai `P_tuijiao_L01` chìa ra trước ngực |
| 40–41 | `P_toufa5/4` | 2 | hai phiến mào đầu phía xa | cứng 1 xương | |
| 42–46 | `S_shitou_05..01` | 5 | **5 tinh thể** trên sống lưng | **cứng 1 xương** (4 đỉnh) | hình bóng đổi tự do được |
| 47–50, 65 | `P_bei_02..05`, `_01` | 5 | **4 gai xương trắng** dọc sống lưng + 1 mẩu nhỏ | 2 xương (`lujin_bozi_3_*`) | |
| 51–53 | `B_bozi_E_10/11/12` | 3 | ba dải trắng **mặt dưới bụng / mặt trước cổ** (phía xa của bầu ngực) | 4–14 xương `bone30*` | nền phía sau lòng ngực |
| 54 | `P_shenti04` | 1 | **mông** (khối thân sau) | 11 xương | |
| 55–63 | `TH_tuiR_*` | 9 | chân SAU phía gần | bone15–23, IK `THR_*` | |
| 64 | `P_shenti_01` | 1 | **vai / thân giữa** (khối tròn to, đáy sẫm) | 10 xương | |
| 66 | `B_bozi_1` | 1 | **cổ** (217 × 347) | 21 xương | nối đầu với thân |
| 67 | `P_shenti_02` | 1 | **LÒNG NGỰC** (lưỡi liềm tím 223 × 360) | 19 xương | lúc nghỉ nấp kín dưới vỏ; `open` thì lộ |
| 68–69 | `P_shenti_02_2/_1` | 2 | hai cụm lỗ tối trên lòng ngực | 4 xương | → chỗ đặt QUẢ TIM của mình |
| 70 | `B_tou_B_01` | 1 | lược răng sau gáy | 3 xương | |
| 71–73 | `P_bozi03..01` | 3 | ba tấm đốt cổ | 2–4 xương | |
| 74–82 | `B_bozi_D_01..09` | 9 | **vành trước** của bầu ngực (9 mảnh sẫm mỏng từ họng vòng xuống đáy) | 2–4 xương `bone30*` (chạy trên `lujin_bozi_2`) | lúc mở bị kéo dài, mỏng |
| 83–85 | `B_bozi_F_03..01` | 3 | ba gai nón trên vành | cứng 1 xương | |
| 86–95 | `B_bozi_C_01..10` | 10 | **10 TẤM VỎ NGỰC** (C_01–05 nhỏ, dọc cổ; C_06–10 to, ở bầu) | 2 xương mỗi tấm (`bone26*`, `shenti_2_*`) | lúc mở TRƯỢT dồn về mép trái (phía thân) |
| 96–103 | `B_bozi_E_08..01` | 8 | tám mảnh viền mảnh dọc mép trước | 1–3 xương | |
| 104–111 | `B_bozi_B_08..01` | 8 | **cột 8 tấm sườn trắng** cạnh chân trước gần, từ khuỷu lên gốc cổ | 2–4 xương | |
| 112–115 | `B_bozi_A_04..01` | 4 | mảng trắng trên gốc cổ + 3 mẩu nhỏ | 1–2 xương | |
| 116–119 | `P_tou_jiao_2`, `P_tou1`, `P_tou2`, `P_tou_jiao_1` | 4 | sừng nhỏ, **ĐẦU** (91 × 107), mẩu đầu, **SỪNG LỚN** (184 × 218) | **cứng 1 xương** (bone65 đầu, bone66 sừng) | hình bóng đổi tự do: đầu của mình vẽ to hơn |
| 120–122 | `P_toufa3/2/1` | 3 | hai phiến mào đầu dài phía gần + túm nhỏ | cứng 1 xương (trừ `toufa1`) | |
| 123–142 | `TQ_tuiR_*`, `P_tuimao_R*`, `P_tuijiao_R*` | 20 | chân TRƯỚC phía gần (trên cùng): đùi 124, ống 137, bàn 138, 4 ngón, 4 túm lông, 2 gai | bone53–55, IK `TQR_*` | |

### Cách "mở ngực" của họ (`open_01` 2,17 s rồi `open_02` 1,07 s lặp)

Không có mảnh nào bật tắt. Lòng ngực (`P_shenti_02` + hai cụm lỗ) LUÔN nằm đó, lúc nghỉ bị 10 tấm vỏ `C` che kín thành một bầu tròn có khe sáng
tím. `open_01`: thân trước rướn cao (0–0,5 s), cổ duỗi thẳng đứng, sừng dựng thẳng lên; các xương `bone26*`, `bone30*` chạy trên đường cong
`lujin_bozi*` được kéo giãn (18 timeline tỉ lệ) nên vành trước `D` / `E` kéo dài theo mép cổ – ngực, còn 10 tấm vỏ `C` và cột sườn `B` dồn sát
về mép trái; khoang lộ ra là một lưỡi liềm dài từ dưới hàm tới đáy bầu, rộng nhất ở nửa dưới. `open_02` giữ dáng đó và thở nhẹ.
→ Của mình: 10 tấm vỏ = 10 mảnh riêng đúng khung part (trượt như cửa chớp); lòng ngực = một mảnh vẽ đủ; **quả tim = mảnh THÊM** (slot riêng trên
lòng ngực, dưới các tấm vỏ, có xương riêng để đập / phình), luôn có sẵn nên lúc nghỉ chỉ lọt ánh sáng qua khe vỏ.

### Clip của họ (tờ `khung/`)

| clip | dài | nội dung | dùng cho |
|---|---|---|---|
| idle_01 | 4,0 s | đứng thở, bờm lưng phất, đầu gật nhẹ | **idle** |
| run_01 | 1,67 s | bước nặng bốn chân tại chỗ, thân lắc | **run** |
| generate_01 | 2,67 s | từ trên rơi xuống (co người 0,3 s), đáp thụp sâu 0,6–0,9 s, đứng dậy, ngẩng gầm 1,5–2,1 s, về | **appear** (nhảy vào) |
| skill_01_1 | 1,33 s | nhấc chân TRƯỚC XA lên (0,3–0,6 s) rồi DẬM xuống 0,74 s, thân chúi | **attack** (dậm, vết nứt chạy tới đối thủ) |
| skill_01_3 | 1,33 s | như trên nhưng nhấc chân TRƯỚC GẦN (co lên trước ngực 0,44–0,6 s) rồi dậm 0,74 s | attack (bản người dùng chụp) |
| skill_02 | 2,0 s | ngẩng cao dần, ngực hé mở (0,4–1,1 s), giữ; 1,33 s CÚI gập đầu chĩa sừng ngang về trước, giữ tới 1,8 s; về | **cast** (tụ cầu trên đỉnh sừng lúc ngẩng, cúi xuống phóng tia) |
| open_01 | 2,17 s | rướn cao, mở ngực (xem trên) | **skill** phần mở |
| open_02 | 1,07 s lặp | giữ dáng mở | **skill** phần giữ + bắn tia từ tim |
| skill_03 | 2,33 s | nhún, NHẢY cả con lên cao (0,78–1,04 s), rơi đập xuống 1,3 s | (để dành) |
| skill_04 | 3,0 s | đứng dựng bằng hai chân sau, ngực mở (1,0–1,33 s), đổ sập hai chân trước xuống 1,67 s | (để dành) |
| skill_05 | 1,83 s | co chân trước gần, ngẩng, quật xuống | (để dành) |
| skill_06 | 1,5 s | cúi húc sừng ngang 0,33–0,5 s rồi bật ngẩng mở ngực 0,67 s, giữ | (để dành) |
| hit_01 / hit_02 | 0,5 / 0,67 s | giật lùi, đầu ngửa | **hit** |
| block_01, stun_01 | 0,5 / 4,0 s | | |
| die_01 | 1,0 s | ngửa cổ, khuỵu bốn chân, đổ sụp nằm bẹp, đầu gục chĩa sừng ngang | **die** |

Chỗ lộ thêm ở các dáng lệch nhất (đã soi tờ nhóm màu): cúi đầu (`cui`): mào đầu dựng đứng, gáy và ba tấm đốt cổ lộ rõ; dậm chân (`dam`): lòng
bàn chân xa và mặt trong chân; chết (`die`): bốn chân gập chồng lên bầu ngực, không lộ mảnh mới. Không dáng nào cần mảnh mà dáng nghỉ không có.

## 3. Hướng làm rig (theo skill pokiclash-spine-rig mục 00, 23, 24; áp dụng sau khi concept được duyệt)

- **Rig = của họ, nguyên lưới và chuyển động** (`gan_nguyen`, lấy mẫu trường `l` 30 khung/giây: path, IK, physics được runtime nướng). Không tự
  dựng xương, không tự viết lại bộ giải ràng buộc. Clip riêng (cast, skill ghép open_01 + open_02, appear) dựng ở TẦNG ĐIỀU KHIỂN rồi cho runtime nướng.
- **Mảnh nối liền một bề mặt** (mông 54, vai 64, cổ 66, các khúc bốn chân): gen LIỀN một tờ "thân liền" từ hợp hình bóng ở dáng gốc rồi nướng vào
  khung từng part bằng mã (`to_lien` / `cat_lien` kiểu hươu gỗ), không gen từng khúc.
- **Mảnh không nối liền màu** (bờm lưng, tinh thể, gai lưng, tấm vỏ, vành, sườn, gai, túm lông, ngón): tờ khung part (hình bóng kín tô phẳng,
  IoU ≥ 0,9 mới lắp).
- **Mảnh cứng một xương** (đầu, sừng, mào đầu, 5 mảnh trên sống lưng, gai): đặt theo concept, hình bóng tự do.
- **Quả tim**: mảnh thêm, bám trọng số của lòng ngực ngay chỗ nó nằm + xương riêng (đập, phình lúc chiêu cuối).
- VFX ngoài rig: vết nứt đất (attack), cầu trên đỉnh sừng + tia (cast), tim rực sáng + tia lớn (skill): rig chỉ đặt xương (`sung_ngon`, `tim`) và sự kiện.

## 4. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `giac_moc_bo_cuc.py` (sơ đồ bố cục hai dáng `nghi`, `mo`, khung 1024 × 1536, tỉ lệ 0,679 px / đơn vị rig, đầu vẽ to 1,45 lần),
`build_giac_moc.py` (gói `gui_gpt/giac_moc_1/`: `luot_1_concept_<hướng>.txt`, `luot_1b_mo_nguc_<hướng>.txt`, `HUONG_DAN.md`).

Giữ của con gốc: dáng bốn chân vai cao mông thấp nhìn sang phải, một sừng lớn trên sống mũi, mào đầu dài quét sau, bờm lưng bay, hàng mảnh nhọn
dọc sống lưng, bầu ngực tròn nhiều tấm có khe sáng. Đổi: bộ xương trắng + tinh thể tím → sinh vật hệ Mộc; đầu sọ nhỏ → đầu to hơn có mặt.

- `co_thu` **A · thú cổ thụ**: thân vỏ cây nâu óc chó, rêu ở vai; sừng gỗ sẫm có vòng, ngọn tinh thể hổ phách; mào và bờm là dương xỉ, lá to, tua
  dây leo; sống lưng xen 4 tấm gai gỗ nhạt và 5 tinh thể hổ phách; bầu ngực là thùng 10 tấm vỏ cây sẫm, khe sáng vàng hổ phách, vành là dây leo
  quấn; bàn chân rễ sẫm, móng hổ phách. Tim: cầu nhựa hổ phách vàng trong hốc sẫm có rễ ôm.
- `bach_thu` **B · bạch thú hoa**: thú sống lông trắng kem; sừng gỗ xoắn ngọn vàng hình nụ; mào và bờm là lá to lục sẫm, dây leo, hoa trắng nhỏ;
  sống lưng xen 4 đài hoa lục nhạt và 5 nụ sen hồng; bầu ngực là một nụ sen khổng lồ 10 cánh hồng sẫm, khe sáng vàng, đài hoa ôm phía trước; bàn
  chân nâu, móng vàng. Tim: cầu vàng giữa vòng nhị vàng trong lòng nụ hồng rượu.

Đã gen 2026-11-13 (mỗi hướng hai ảnh, cả bốn ra đúng bố cục ngay lượt đầu): `tai_ve/L1_co_thu.png`, `L1b_co_thu_mo.png`, `L1_bach_thu.png`,
`L1b_bach_thu_mo.png`; trang so `inbox/giac_moc_xem_concept.html`. Đã gửi người dùng, **chờ chọn hướng** (chưa có `L1_duyet.png`).
Nhận xét của Claude: A dữ và hợp boss hơn, bầu ngực vẽ thành các nan ngang có khe hổ phách, lúc mở các nan dồn thành cột dọc cạnh hốc; B hiền
hơn (dáng dê / kỳ lân lông xù), bầu ngực là nụ sen, lúc nghỉ gần như không thấy khe sáng, vành gai quanh nụ hơi dày.

Tránh trùng tướng đã có ở đảo: hươu gỗ (gỗ kem đốm nâu, lá phong cam, tinh thể lục), voi rừng (da xám lam phủ lá lục), tượng đá (đá be, lõi lục).

## 5. Người dùng chốt (2026-11-13)

- "**dạng A**; tùy bạn quyết (đòn dậm → Claude chọn `skill_01_3`); **dạng non làm sau**; tôi duyệt concept rồi, **auto mode làm hết đi**".
- Rồi: "từ từ, hướng A **cái sừng xấu quá, làm lại để nó liên kết với phần đầu thành 1 khối hơn**". Lượt 1c (`build_giac_moc.py 1c`, vẽ lại y hệt
  `L1_co_thu.png`, chỉ đổi sừng): `lien` (sừng mọc liền từ sống mũi như sừng tê giác) và `mu` (mảng trán gỗ sẫm như mũ giáp vuốt lên thành sừng).
  **Người dùng chọn kiểu 2 (`mu`)**: "ok làm kiểu 2, chốt automode đi" → `tai_ve/L1_duyet.png` = `L1c_sung_mu.png`.
- Xương sừng `bone66` không bao giờ cử động so với xương đầu `bone65` (đã đo trên 11 clip) → **đầu liền sừng là MỘT mảnh cứng** của mình.

## 6. Mảnh (`giac_moc_manh.py`, prompt `build_giac_moc.py manh | dau`)

- **Thân liền** (`to_lien` → `mau/lien.png`, 0,796 px / đơn vị; `luot_2_than_lien.txt` → `tai_ve/N_lien.png`; `cat_lien`): mông `P_shenti04`, vai
  `P_shenti_01`, cổ `B_bozi_1`, đùi + ống + bàn của hai chân gần hợp thành một hình; hai chân xa mỗi chân một hình riêng. Lượt đầu ra đúng:
  không nét mực bên trong, phủ 1,00–1,03 hình bóng từng part.
- **Tám tờ khung part** (`nhom_part` tự chọn tỉ lệ phóng lớn nhất còn vừa tờ; `luot_2_manh_<tờ>.txt` → `tai_ve/N_<tờ>.png`; `cat_part`, `so_part`):
  A (×2,1) sáu mảng dương xỉ; B (×2,7) năm dải lá dài, sợi dây leo (một ảnh dùng cho 4 slot), hai túm lá sau đầu; C (×2,2) mào đầu, 5 tinh thể,
  5 tấm gai; D (×3,3) 10 tấm vỏ ngực (dải sáng hổ phách ở mép DƯỚI theo hướng thế giới), 8 tấm sườn, 3 gai; E (×4,4) 9 đoạn dây leo vành, 8 lá
  nhỏ, rêu nhỏ, 3 tấm đốt cổ, mẩu gỗ gáy; F (×2,0) lòng ngực (hốc sẫm + ba sợi rễ), quả tim (ô thêm), ba dải vách xa, rêu gốc cổ; G (×3,7) 16 ngón
  chân (móng hổ phách đặt đúng chỗ móng của họ), 6 gai gót; H (×3,4) 7 túm rêu, 3 gai vai. Tờ D: IoU 0,95–0,99 ngay lượt đầu.
- **Đầu liền sừng** "đúng chỗ, đúng cỡ" từ concept: `luot_2_dau_sung.txt` → `tai_ve/M_dau.png` (ra đúng chỗ, viền kín).
- Bỏ của họ: hai cụm lỗ trên lòng ngực, đầu, sừng lớn, sừng nhỏ, hai region tí hon `B_bozi_A_01/02` (`BO_PART`).

## 7. Clip (`giac_moc_clip.py`: tầng điều khiển của rig gốc → `sample_moi.json`, `kenh_rieng.json`)

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| appear | 1,75 s | generate_01 từ 0,26 s (đang co người trên không), bay vào từ sau 1050 đơn vị (xương `move`), hiện dần 0,18 s; đáp thụp 0,56; đứng dậy; về nghỉ | dap_dat 0,56 |
| idle | 4,0 s lặp | nguyên idle_01 | |
| walk | 1,67 s lặp | nguyên run_01 | |
| attack | 1,40 s | skill_01_3: co chân trước gần lên 0,30–0,60, DẬM 0,74, thân dộng + rung; đứng tại chỗ | dam 0,74; trung 0,92 |
| cast | 2,70 s | skill_02 kéo dài đoạn giữ: ngẩng cao, ngực hé mở, cầu tụ ở đỉnh sừng từ 0,40; cúi 1,11–1,33; phóng tia 1,36 (giật lùi), ghìm tới 2,30 | tu 0,40; phun 1,36; het_phun 2,30 |
| skill | 3,75 s | open_01 mở ngực 0–0,95; open_02 giữ: tim đập nhanh dần, phình 1,3 lần, rung mạnh dần; 2,05 bắn (giật lùi mạnh), ghìm tới 3,05; open_01 chạy ngược đóng ngực 3,55 | mo 0,15; tu 1,00; phun 2,05; trung 2,13; het_phun 3,05; dong 3,15 |
| hit | 0,5 s | nguyên hit_01 | |
| die | 1,0 s + tan 0,45 | nguyên die_01 | |

Kênh riêng: `bay` (xương `move`), `cau` (tỉ lệ xương `cau` ở đỉnh sừng: cỡ quả cầu mana), `tim` (tỉ lệ xương `tim`), `hien` (độ đậm lúc appear).

## 8. Rig (`giac_moc_rig.py` → `inbox/giac_moc_1/rig/`)

- Đủ 267 xương của họ + `move`, `tim` (con của xương bám nặng nhất quanh điểm rộng nhất của lòng ngực: `bone5`), `mieng` (đỉnh sừng, con của
  `bone65`), `cau`. Mỗi slot của họ dùng NGUYÊN lưới của họ (`gan_nguyen`) với ảnh của mình; 0,5 px atlas / đơn vị rig.
- `dau` (đầu liền sừng): ô cứng 4 đỉnh trên `bone65`; chỗ đặt = phép khớp concept ↔ sơ đồ (s = 0,98, IoU 0,84) ở khung 0 idle rồi đưa về dáng
  gốc theo `bone65`; vẽ SAU mào đầu (`P_toufa1`) để mào nằm sau đầu như concept (rig gốc vẽ mào trước đầu).
- `tim`: ô cứng trên xương `tim`, bán kính 104 đơn vị, ngay trên lòng ngực và dưới các tấm vỏ; lúc nghỉ chỉ lọt ánh vàng qua khe vỏ.
