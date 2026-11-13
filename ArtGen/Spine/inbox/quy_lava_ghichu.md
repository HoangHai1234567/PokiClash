# Tiểu quỷ lava (`quy_lava`): tướng đầu tiên đảo Hỏa

Bắt đầu 2026-11-13 (máy ổ C). Con gốc của rig: `monster_3336` (game tham khảo, kho `D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh
chụp trang xem, clip `skill_02`), làm dạng 1. Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng
công khai. Hình là thiết kế của mình. Tên, id game: chưa đặt. Suất 1 đảo Hỏa (ải 71 "Bến Đá Đen") hiện là `su_tu_lua` (Sư Tử Lửa).

## 1. Lời dặn của người dùng (2026-11-13)

- "làm tướng đầu tiên của đảo hỏa; concept **tiểu quỷ lava**, con gốc lấy ref làm **dạng 1**".
- "**idle và run** có thể làm **gần giống con gốc**, thay đổi đi 1 chút nhưng **phần tóc lửa** tôi muốn bạn **cải thiện thêm cho giống ngọn lửa
  thật hơn**".
- Đánh thường: "tướng dùng **tay cầm khiên đập khiên** vào người địch".
- Chiêu mana: "**chĩa kiếm/giáo** vào người đối thủ rồi **bắn 1 tia lửa**" (tia lửa là VFX, rig chỉ đặt xương mũi giáo + sự kiện).
- Chiêu cuối: "**chắp 2 tay** vào nhau, **cầm giáo bằng 2 tay** rồi **nhảy lên đâm giáo thẳng xuống** đối thủ; làm anim **nhảy**, anim **hold giáo
  trên không** rồi animation **đâm giáo xuống**".
- die: "**ngã quỵ xuống**". appear: "**nhảy vào** màn chơi".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3336/`: `info.json`, `att_goc.json`, `att_idle0.json`, `mo/idle0_*.jpg`, `mo/nhom_idle0*.jpg`, `parts/`, `khung/`)

52 xương (tên đã bị xáo: `xem_*`), 32 slot, 10 clip; atlas nhỏ (ảnh vùng ~0,5 px / đơn vị). 2 IK hai chân (`l_t`: xem_24 → xem_26, đích
xem_41; `r_t`: xem_21 → xem_22, đích xem_42), 2 transform constraint (`t`, `t2`). Không path, không physics. Con nhìn sang PHẢI, lộ HAI mắt.

Bảng mảnh (thứ tự vẽ sau → trước; "→" là vai trò trong thiết kế mình):
| thứ tự | slot | ảnh (px) | là gì | bám |
|---|---|---|---|---|
| 1–2 | `xem_30`, `xem_31` | | bản sao khiên + vệt lửa trên xương xem_44 (ẩn; vệt mờ của `skill_02`) | |
| 3 | `xem_25` | 74 × 59 | bắp tay XA (màu thân) | xem_25 |
| 4 | `xem_24` | 74 × 132 | **KHIÊN** đá dựng đứng (region, một xương) | xem_20 |
| 5 | `xem_23` | 55 × 76 | cẳng tay xa (màu thân) | xem_23 / xem_25 |
| 6 | `xem_22` | 41 × 88 | vệt dung nham dọc trên khiên | xem_20 |
| 7 | `xem_18` | 41 × 55 | chân xa (màu thân) | xem_21 / xem_22 |
| 8 | `xem_17` | 143 × 119 | **TÓC** (63 đỉnh, 13 xương) → NGỌN LỬA | xem_27..35, bone, bone2 |
| 9 | `xem_16` | 117 × 119 | thân dưới + mảng bụng | xem_18 / xem_16 / xem_11 |
| 10 | `xem_15` | 32 × 35 | chân gần (màu thân) | xem_24 / xem_26 |
| 11–13 | `xem_14`, `xem_13`, `xem_12` | | khối đá dưới chân (giày đá) | xem_39 / xem_16 / xem_38 |
| 14 | `xem_11` | 136 × 113 | **ĐẦU** (nửa trên của khối thân) | xem_11 |
| 15–16 | `xem_4`, `xem_3` | | mắt xa, mắt gần (bản nhắm: `r_yan`, `l_yan`, đổi ở die / floating) | xem_3 |
| 17 | `xem_2` | 43 × 16 | miệng chữ w răng nanh | xem_2 |
| 18–19 | `xem_1`, `xem_0` | | sừng gần, sừng xa | xem_11 |
| 20–22 | `xem_27..29` | | ba khối đá ngón của nắm tay xa (nắm cán khiên) | xem_43, 42, 41 |
| 23 | `xem_10` | 285 × 65 | **GIÁO** hai phần: nửa sau phiến đá sẫm, nửa trước mũi tinh thể dung nham (region, một xương xem_12) | xem_12 |
| 24–25, 27 | `xem_9`, `xem_8`, `xem_6` | | khối đá chân / đốt ngón tay gần | |
| 26 | `xem_7` | 75 × 85 | **GĂNG TAY ĐÁ** tay gần (vết nứt chữ Y) | xem_8 / xem_7 |
| 28 | `xem_5` | 43 × 40 | núm vai đá tay gần | xem_5 |
| 29–31 | `xem_19`, `xem_20`, `xem_10a` | | bản sao giáo + vệt mờ (ẩn; dùng ở `skill_02`) | |

Clip của họ (tờ `khung/`):
| clip | dài | nội dung | dùng cho |
|---|---|---|---|
| idle_01 | 7,0 s | đứng thở, nhún, giáo chúc mũi xuống | **idle** (giữ gần như cũ, thêm lửa lay) |
| run_01 | 0,53 s | chạy lon ton tại chỗ | **walk / run** |
| skill_01 | 1,17 s | giơ giáo chĩa lên trước 0,11–0,32, vung bổ xuống 0,42–0,85, về | nền cho **cast** (chĩa giáo, bắn tia) |
| skill_02 | 1,47 s | quét giáo ngang có vệt mờ 0,27–0,67, đấm găng tay 0,8–1,33 | (để dành) |
| block_01 | 0,5 s | nâng khiên đỡ | nền cho dáng nâng khiên của **attack** |
| hit_01 / hit_02 | 0,5 / 0,67 s | giật lùi | **hit** |
| stun_01 | 1,67 s | choáng | |
| floating_01 | 1,5 s | bị hất tung lộn vòng rồi rơi | (để dành; dáng trên không cho appear) |
| die_01 | 1,0 s | bật ngửa ra sau, khiên văng, nằm sấp | không dùng (người dùng muốn **ngã quỵ**) |

## 3. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `quy_lava.py` (`mo`, `nhom`, `part_goc`), `quy_lava_bo_cuc.py` (sơ đồ bố cục 1536 × 1024 ở khung 0 idle, tỉ lệ 1,817 px / đơn vị rig;
tóc thay bằng ngọn lửa vẽ bằng mã), `build_quy_lava.py` (gói `gui_gpt/quy_lava_1/`).

Giữ của con gốc: thân hạt đậu liền đầu, nhìn ba phần tư sang phải, lộ hai mắt (mắt gần to hơn), mắt vàng nửa trăng không con ngươi cạnh trên
xếch, miệng chữ w hai răng nanh, mảng bụng sáng hơn, sừng gần dựng đứng, sừng xa cong ra ngoài, găng tay đá to có núm vai và vết nứt chữ Y,
giáo hai phần chéo trước người, tay xa màu thân với nắm tay ba khối đá cầm khiên hẹp dựng đứng, giày đá.
Đổi: **tóc → ngọn lửa thật** (4–5 lưỡi gốc dày uốn chữ S, ngọn móc ngả ra sau, liền khối ở gốc, ba lớp đỏ cam / cam / lõi vàng); nét vẽ tay
tô phẳng của game (con gốc có bóng, điểm sáng).

Ba hướng màu:
- `than_tim` **A · đá than tím** (sát con gốc): thân tím than #5C5070, bụng tím hồng nhạt, đá gần đen #383240, nứt đỏ cam #EC5630.
- `da_nung` **B · đá đỏ nung**: thân nâu đỏ gạch #7C4238, bụng đất nung, đá đen nâu, nứt cam vàng #FFA034.
- `tro_nui` **C · tro núi lửa**: thân xám tro #96908C như đá bọt, đá than, nứt cam #F67028.

## 4. Kế hoạch rig và clip (sau khi concept được duyệt; theo skill pokiclash-spine-rig mục 00)

- Rig = của họ (`gan_nguyen`, lấy mẫu trường `l`; IK chân được runtime nướng). Mảnh theo khung part (hình bóng kín → Codex vẽ lại).
- **Thân** (đầu `xem_11` + thân dưới `xem_16` + tay xa `xem_25`, `xem_23` + hai chân `xem_18`, `xem_15`): cùng một bề mặt → gen LIỀN một tờ rồi
  nướng vào khung từng part (`to_lien` / `cat_lien` kiểu hươu gỗ), không gen từng ô.
- **Ngọn lửa**: lưới dày của mình biến dạng như lưới tóc của họ (`gan_goc`), hình bóng vượt hull được; tách 2–3 lớp lưỡi lửa có lò xo, lay
  lệch pha, ngọn liếm lên (memory animation-khong-don-dieu).
- Mảnh cứng một xương (khiên, giáo, sừng, mắt, miệng, găng tay, núm vai, khối đá chân): đặt theo concept, hình bóng tự do.
- Clip: idle (idle_01 + lửa lay), walk (run_01), attack (lấy đà nâng khiên kiểu block_01 → lao tới ĐẬP khiên bằng tay xa), cast (dáng chĩa
  giáo của skill_01, giữ chĩa, sự kiện `phun` ở mũi giáo, xương `mieng` ở mũi), skill (chắp tay cầm giáo hai tay → nhảy lên → GIỮ trên không
  → đâm thẳng xuống đối thủ, `far`), hit (hit_01), die (khuỵu gối, gục xuống, lửa tắt dần), appear (nhảy vào từ ngoài sân, đáp thụp).
- VFX ngoài rig: tia lửa (cast), vệt lao / chấn động đất lúc đâm xuống (skill), tia lửa toé lúc đập khiên.

## 5. Kết quả gen concept (2026-11-13)

Cả ba ra đúng bố cục ngay lượt đầu (95–170 s mỗi bản): `tai_ve/L1_than_tim.png`, `L1_da_nung.png`, `L1_tro_nui.png`; tờ so với con gốc
`inbox/quy_lava_1/so_concept.png`. Ngọn lửa ra lửa thật (lưỡi uốn chữ S, ngọn móc, ba lớp màu) ở cả ba. Nhận xét của Claude: găng tay và hai đồ
cầm to, chắc hơn con gốc (giáo nửa sau là phiến đá hình diều); nắm tay xa vẽ kiểu bốn đốt nắm dọc; B có hai giọt lửa rời bay trên ngọn (lúc rig
là mảnh thêm). **Chờ người dùng chọn hướng** (chưa có `L1_duyet.png`).

## 6. Người dùng chốt (2026-11-13): "làm B, khiên tôi thấy hơi mỏng"

Lượt 1b (`build_quy_lava.py 1b` → `tai_ve/L1b_khien_day.png`): vẽ lại y bản B, chỉ đổi khiên thành khiên hình cái khiên (heater) rộng gấp đôi
(x 985–1192), có dải cạnh dày lộ bên trái, viền vát, vết nứt dung nham. Lượt gen đầu bị Codex treo 25 phút (tiến trình không dùng CPU), gen lại
ra ngay. `L1_duyet.png` = bản này. Khớp concept ↔ sơ đồ bố cục: dò hình bóng (bỏ vùng khiên), s 0,824, IoU 0,90 (`mau/khop_concept.json`).

## 7. Mảnh (`build_quy_lava.py manh` → `luot_2_manh_A..F.txt`; `quy_lava_manh.py lam` → `inbox/quy_lava_1/manh/`)

Sáu tờ "đúng chỗ, đúng cỡ", ra dùng được ngay lượt đầu: A thân (không mặt); B lửa (đáy khép kín), hai giọt lửa, giáo liền một khối có khâu;
C khiên, sừng gần, hai mắt, miệng; D sừng xa, tay xa, hai chân; E nắm tay xa (một khối), hàng đốt ngón tay gần, hai mắt nhắm; F găng tay LIỀN
núm vai (tờ C vẽ găng thấp hơn concept ~30 px, vuông góc cạnh, núm vai lơ lửng như hạt đậu rời → bỏ, gen lại riêng). Giáo cắt hai mảnh ở khâu
nối (`tach_giao`): phiến đá đuôi `giao` và mũi tinh thể `giao_mui`. 20 mảnh; bản ghép lại trùng concept (`manh/_so_ghep.png`).

## 8. Rig (`quy_lava_rig.py` → `inbox/quy_lava_1/rig/`, clip ở `quy_lava_clip.py`)

- Đủ 52 xương của họ + `move`, `mieng` (mũi giáo, con của xem_12), `far`. Dáng gốc = khung 0 idle_01. KG 1,25; chiều cao game 285 (đỉnh đầu,
  không tính lửa). Mỗi đỉnh lưới của mình lấy trọng số từ lưới part của họ đúng chỗ đó (trọng tâm trong tam giác; ngoài thì nghịch đảo d⁴).
- **Ba xương inherit 2** (đầu xem_11, hai vai xem_36, xem_37: "không nhận góc xoay của cha"; runtime .atomik chỉ có noScale): biến đổi riêng
  tính lại từ 2×2 thế giới của mẫu (`rieng`) ở dáng gốc và mọi khung clip. Trước khi sửa, mắt lệch 72 đơn vị, tóc 200–350 so với con gốc.
- Lỗi đã gặp: cắt bớt trọng số còn 4 xương mà quên chuẩn hoá lại → lửa (bám 13 xương tóc) co về gốc toạ độ ở dáng gốc.
- Slot sinh đôi: `nam_x2` (nắm tay xa vẽ TRƯỚC mũi giáo, bật lúc cầm giáo hai tay), `giao_sau` (phiến đá đuôi giáo vẽ SAU thân lúc giáo dựng).
- `.atomik` 239 KB, 54 xương, 22 slot, 380 đỉnh; atlas 1112 × 1264. Nối clip về idle lệch 0 px; vòng idle / walk khép.
- Đo góc nhảy bằng runtime thật 60 khung/giây (`rig/that/mau60.json`): mọi xương có hình ≤ ~21°/khung (chỉ xương ngón xa xem_41..43, không
  mảnh nào bám, tới 49°). Đã thêm `unwrap` góc trong `quai/hoat.py thanh_khoa` (khiên đi qua ±180° bị nội suy ngược nửa vòng 1 khung).

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| appear | 1,3 s | nhảy vòng từ phía sau vào, co người trên không, đáp nhún | cham_dat 0,42 |
| idle | 7,0 s lặp | idle_01 của họ + lửa lay lệch pha nhanh, giọt lửa nhấp nhô, chớp mắt 2,3 / 5,6 s | |
| walk | 0,53 s lặp | run_01 của họ, lửa lay mạnh hơn | |
| attack | 1,0 s | ngả ra sau kéo khiên sát người 0,28 → lao tới ĐẨY KHIÊN thẳng tới 0,40 (giải hai khúc tay xa, khiên giữ góc gần đứng) | trung 0,40 |
| cast | 1,85 s | dáng chĩa giáo của skill_01; mũi giáo ghìm 18° chếch lên trỏ vào đối thủ; giật lùi lúc bắn; giữ tới 1,45 | phun 0,50; het_phun 1,45 |
| skill | 2,3 s | gom tay (điểm nắm đi theo cung quanh vai, khuỷu cố định chiều gập) → nhảy 0,46 → giữ giáo dựng trên không 0,82–1,30 → đâm thẳng xuống, trúng 1,44 (khung dời xa nhất) → rút về | nhay 0,46; dam 1,30; trung 1,44 |
| hit | 0,5 s | hit_01 của họ, nhắm mắt | |
| die | 1,9 s | giật → khuỵu gối 0,42 → đổ sấp về trước 1,05, giáo đổ nằm, lửa tàn dần → mờ | nga 1,05 |

Tay gần rất ngắn (tầm với ~111 đơn vị từ vai): điểm nắm giáo hai tay đặt trong tầm, lệch về bên trái mặt.

## 9. Việc tiếp

1. Người dùng xem `rig/xem.html`, dặn sửa.
2. VFX (lớp hạt trên sân): tia lửa từ mũi giáo (cast, sự kiện phun / het_phun, xương mieng), chấn động + toé dung nham lúc đâm xuống (skill),
   tia lửa toé lúc đập khiên (attack), bụi khi đáp (appear).
3. Vào game: tên, id, suất (suất 1 đảo Hỏa hiện là su_tu_lua, ải 71) do người dùng quyết; chép `.atomik` + chân dung vào Resources.
4. Nếu muốn game lái chiêu cuối bằng code (nhảy tới đúng chỗ đối thủ, giữ trên không lâu ngắn tuỳ trận): tách ba clip nhảy / giữ (lặp) / đâm.

## 10. Lượt sửa thứ nhất (2026-11-13)

Người dùng (ba ảnh trang xem): "tay cầm khiên thì phần ngón tay đúng ra phải không nhìn thấy"; "chiêu bắn chỉ cần dơ tay chĩa giáo về phía trước, không
cần đề tay khiên ngược về sau"; "chiêu cuối nên gen thêm cánh tay bên kia, nếu có thì cho dài hơn chút, đẩy giáo ra giữa hơn, layer nằm trên body nhưng
nằm dưới bàn tay, 2 tay đều phải đưa ra phía trước, chân ở animation này cũng bị hở không nối với cơ thể"; "chân bên phải layer phải nằm ở dưới thân".

- Nắm tay xa vẽ SAU khiên (`THU_TU`: tay_x, nam_x, khien...). Chân phải (chan_x) vẽ dưới thân.
- Chiêu mana: bỏ chuỗi tay xa (`TAY_XA`) khỏi nền skill_01: tay khiên giữ dáng idle.
- Chân hở: cụm đá chân gần nằm lệch ra ngoài đáy thân (lúc nghỉ găng tay và giáo che). Thêm đùi chân gần `dui_g` (vẽ sau thân, trước nó là cụm đá
  chân); Codex treo hai lần nên vẽ bằng mã (`quy_lava_dui.py`: vân sáp lát từ mảnh thân, viền mực) thành tờ M_G.
- Chiêu cuối: bỏ bản giáo-sau-thân; giáo ở lớp mặc định (trên thân, dưới găng tay); trục giáo ở x ≈ 25 (giữa hai mắt), nắm ngang bụng; trong lúc cầm
  giáo hai vai dời xuống hai bên hông (`VAI_HA_*`) để tay mọc từ hai bên bụng chìa ra trước, không vắt qua mặt (vai gần của con gốc ngang miệng);
  tay gần dài thêm 40 (dời xem_8 dọc bắp tay) với bắp tay mới `bap_g` (dùng lại ảnh tay xa, giãn theo); găng tay thành mảnh CỨNG theo cẳng tay
  xem_8 (tay duỗi dài không kéo méo găng); tay xa dài thêm 0,09 chiều cao, bản sao `tay_x2` + `nam_x2` vẽ trước thân, nắm cán dưới găng; khiên ẩn
  lúc cầm giáo hai tay. 54 xương, 24 slot; `.atomik` 244 KB; nối clip 0 px; xương có hình ≤ 37°/khung ở 60 khung/giây (cú đẩy khiên, lúc rút giáo).


## 11. Dạng 2: hiệp sĩ dung nham (`quy_lava_2`, 2026-11-13)

Người dùng: "làm dạng 2 đi con này là dạng 1"; con gốc: "tự nghĩ thôi, lên concept rồi gen"; chiêu: "giữ kiểu dạng 1, mạnh hơn"; chọn hướng A.

- Cùng rig monster_3336 và cùng mã clip với dạng 1 (biến môi trường `QL_DANG=2` cho `quy_lava_manh.py`, `quy_lava_rig.py`, `quy_lava_clip.py`).
  Concept (`build_quy_lava_2.py`, `inbox/quy_lava_2/tai_ve/L1_duyet.png` = `L1_hiep_si.png`) vẽ cùng tư thế, cùng bố cục với dạng 1; khớp vào rig
  bằng phép đồng dạng concept 2 → concept 1 theo hai mắt + miệng (`DOI2`), nên mặt trùng xương đầu.
- Mảnh: sáu tờ "đúng chỗ" (`build_quy_lava_2.py manh`), ra dùng được ngay lượt đầu. Thêm `vai_g` (giáp vai gai, cứng trên bắp tay xem_7, vẽ trước
  găng). Miệng: GPT chỉ vẽ bốn răng rời → gộp cụm (`GOP`) + kẻ nét miệng bằng mã (`noi_mieng`). Bắp tay gần dùng ảnh tay xa dạng 2 (có bao tay đá).
- Mạnh hơn: đánh thường đập khiên HAI nhát (trúng 0,40 và `trung2` 0,74, 1,3 s); chiêu mana giữ luồng lửa tới 1,85 s (2,25 s); chiêu cuối nhảy cao
  hơn (giữ ở 1,2 chiều cao) và thêm sự kiện `chan_dong` (dung nham phun quanh đối thủ, 0,12 s sau cú đâm).
- Chiều cao game 344 (dạng 1: 285); `.atomik` 297 KB; nối clip 0 px.
- Sửa chung hai dạng: (1) khung TRÚNG của chiêu cuối phải là khung dời xa nhất (game xoay + co quỹ đạo cho khung đó trỏ vào đối thủ); trước đó khung
  xa nhất là lúc giữ trên không → `K_XA` 1,9 / 2,2 chiều cao. (2) Dáng cầm giáo giải trọn rồi TRỘN GÓC từng xương với dáng nền (`grip`); giải với đích
  trượt dần thì khuỷu tay xa lật chiều (~200° trong 4 khung lúc rút tay). Chiêu cuối nay ≤ 23°/khung ở 60 khung/giây.


## 12. Lượt sửa dạng 2 (2026-11-13)

Người dùng: "animation walk nhìn xấu quá"; "chiêu bắn chân bên trái nhấc lên làm gì"; chiêu cuối: vẽ tay vị trí giáo (dọc bên phải thân), tay phải
(nắm cán phía ngoài bên phải), tay trái (vòng qua bụng); "bàn tay trái cầm giáo ở chiêu này còn đang lỗi".

- Walk dạng 2: tự viết bước dậm nặng 0,72 s (`buoc`: mỗi chân giải hai khúc tới chỗ đặt, nửa chu kỳ bước nhấc cong, nửa chu kỳ trụ; thân nhún mỗi
  lần chạm đất, thân trên lắc, đầu bù, găng / giáo / khiên đung đưa trễ). Dạng 1 giữ run_01 của con gốc.
- Chiêu mana (cả hai dạng): bỏ hai chân + khối đá chân (`CHAN`) khỏi nền skill_01.
- Chiêu cuối dạng 2: giáo dọc x ≈ 85 (giữa tâm và mép phải); tay trái dài thêm 100 vòng qua bụng; tay phải nắm cán TRÊN găng, lệch ra ngoài.
  Lỗi tìm ra: (1) điểm nắm viết theo toạ độ dạng 1 mà dạng 2 nâng cả con cao hơn 76 → cộng `NANG_LECH`; (2) nắm tay xa dạng 2 nằm sát khuỷu nên tầm
  với là vành hẹp quanh vai, giải hai khúc nhảy nghiệm → tay xa dạng 2 = bắp tay chĩa thẳng vào điểm nắm + co giãn đúng độ dài, cẳng tay giữ góc
  lúc đứng; (3) trộn góc lệch gần nửa vòng đổi chiều giữa hai khung → góc lệch giữ liên tục theo thời gian (`GRIP_NHO`). Chiêu cuối dạng 2 nay
  ≤ 34°/khung ở 60 khung/giây (đúng khung đâm trúng), dạng 1 ≤ 23°.


## 13. Chiêu cuối dạng 2: đổi ảnh khối hai tay + giáo (2026-11-13)

Người dùng: "tay lỗi, tay trái sao bạn lại bẻ cánh tay đi 90 độ, tay phải nhìn không rõ, cần ảnh thì gen thêm cho hợp". Ghép từ mảnh của dáng đứng
(găng tay cứng + bắp tay giãn) không ra dáng ôm giáo → làm như rig thương mại (skill mục 22): đổi ảnh.
- `build_quy_lava_2.py cam`: lượt 3 vẽ lại concept dạng 2 chỉ đổi tay (`tai_ve/L2_cam_giao.png`: giáo dựng bên phải, tay phải ôm cán phía trên từ
  ngoài, găng tay trái nằm ngang bụng nắm ngay dưới, khiên sau lưng), lượt 3b tách riêng khối hai tay + giáo (`M_cam.png`). Cả hai ra đúng ngay lượt
  đầu (Codex hết hạn mức tới 14:53 một lần; người dùng mua thêm lượt).
- Rig: mảnh `cam` cứng trên thân trên xem_18, vẽ trước nhất, ẩn sẵn. Clip: 0,28 s (giữa lúc nhún) → 1,76 s (lúc nhảy lùi về) hiện `cam`, ẩn găng,
  đốt ngón, giáp vai, bắp tay, tay xa, nắm tay xa, giáo, khiên; tay ghép bằng mã rút về trong 0,2 s.
- `.atomik` dạng 2: 354 KB (thêm ảnh khối tay + giáo).


## 14. Vào game (2026-11-13): suất 1 đảo Hỏa, id `su_tu_lua`

Người dùng: "ok ổn rồi cho vào game đi". `quai/doi_quy_lava.py` (chạy lại không đổi gì; `--ve_cu` trả về như cũ): giữ id tướng, id thẻ, chỉ số,
hiệu ứng thẻ, số dạng (ba) → golden không đổi. aola: tướng + dạng 1 → quy_lava_1, dạng 2 + 3 → quy_lava_2. Tên (Claude đặt, người dùng đổi được):
Tiểu Quỷ Lava / Hiệp Sĩ Dung Nham; danh hiệu "Quỷ lửa cầm khiên"; dòng "Dòng Quỷ Lava"; thẻ Giáo Phun Lửa (torch), Giáo Nham Giáng Thế (sword),
Khiên Than Hồng (shield). `chep`: Resources/quy_lava_1, quy_lava_2 (thư mục su_tu_lua_* cũ giữ nguyên).
Unity (cầu nối MCP 8080, đã báo các phiên khác): refresh, "Nhập dữ liệu" (88 tướng), "Gắn dạng .atomik" (prefab su_tu_lua giữ 3 dạng),
EditMode 102/103 (hỏng PrefabOnlyTests do UI/Kit NumberTicker, UiMotion: có từ trước, không liên quan), "Chụp thử dạng .atomik":
`Library/PokiHeroShots/su_tu_lua_atomik_1..3.png` hiện đúng; game đọc attack trúng khung 10 có lao, cast đứng tại chỗ tia ở mũi giáo, skill trúng
khung 36 có lao. Chưa có clip evolve (đổi dạng là đổi hình tức thì), chưa có VFX riêng (đang dùng hiệu ứng cũ của suất), chưa thử trên Android.
