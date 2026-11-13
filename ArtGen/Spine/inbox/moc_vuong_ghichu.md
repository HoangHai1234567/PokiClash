# Boss cuối đảo Mộc (`moc_vuong`): tướng thứ 10 đảo Mộc

Bắt đầu 2026-11-13 (máy D). Con gốc của rig: `monster_3709` (game tham khảo, kho `D:\RefAnimation\SwordxStaff`), **do người dùng chỉ** (ảnh
chụp trang xem, clip `idle_01` và `skill_03`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không
đăng công khai. Hình là thiết kế của mình. Tên, id game, suất trên đảo: chưa đặt (giả định của Claude: thay suất 10 `thanh_long`, như Voọc
Tướng thay suất 8).

## 1. Lời dặn của người dùng (2026-11-13)

- "làm tướng cuối cùng ở đảo mộc, final boss; **concept như con gốc nhưng phải thay đổi nhiều tránh copy**".
- `appear`: "tướng **bay vào rồi rơi mạnh xuống đất đáp bằng 4 chân**".
- `idle`, `die`: "làm giống họ".
- `walk`: "đi bộ bằng 4 chân"; `fly`: "vỗ cánh bay lướt trong không trung".
- Đánh thường: "làm giống `skill_04`: **dậm 2 chân trước thật mạnh, tạo địa chấn cùng sấm sét vào đầu đối thủ (fx làm riêng)**".
- Chiêu mana: "làm giống `skill_02`: **hét mạnh, shake cam, tạo ra những đợt sóng âm cực mạnh**".
- Chiêu cuối: "tôi chưa nghĩ ra... làm 1 animation thật epic, hoành tráng, fx thật đẹp và animation ngầu vào, **bạn cứ tự quyết**".
- "đây là 1 tướng rất khó nên cần **mổ xẻ rất kĩ tướng gốc, từng animation để xem họ tách part thế nào**".
- "**lên concept rồi cho tôi xem, sau khi đã chốt concept rồi thì auto mode làm**".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3709/`)

Tệp: `info.json`, `att_goc.json`, `att_idle0.json`, `manh_anh.png` (mọi vùng atlas), `nhom_idle0_1..4.jpg` (từng NHÓM part trên nền cả con
mờ), `anh_<nhóm>.jpg` (ảnh vùng từng part của nhóm), `khung/<clip>.jpg` (tờ 10 khung của cả 20 clip). (`manh_dang_idle0.png` của
`to_manh.py dang` ra 29385 × 162864 px, không mở được: con này 175 part, dùng `nhom_*` thay.)

**508 xương, 178 slot (176 hình, mỗi slot đúng một hình, TẤT CẢ là lưới), 20 clip, 110 188 khoá, atlas 176 vùng (ảnh 1,3 MB), không
path / physics.** Nhìn sang PHẢI, đầu nghiêng lộ MỘT mắt: không lật. Khung dáng idle: x −984..975, y −90..1418 (đơn vị rig).

### 2.1 Bảng nhóm part (thứ tự vẽ sau → trước)

| nhóm slot | số part | thứ tự vẽ | xương bám | là gì, tách thế nào |
|---|---|---|---|---|
| `chibang_h_l_01..31` | 31 | 2–32 | 101 | cánh TRÊN phía xa (bên phải hình), sau mọi thứ. **Mỗi chiếc lông một part**: lông dài 13–19 đỉnh bám chuỗi 3–4 đốt riêng (`allN > Nb > Nc > Nd`: lông tự uốn), lông phủ nhỏ 13–14 đỉnh / 3 đốt, mảnh vụn bay 4–5 đỉnh / 1 đốt bám đốt ngọn của lông to. Hai part to `22`, `23` (38–46 đỉnh, 9–11 xương) là DẢI DÂY dài rủ xuống có móc cam ở ngọn. `02`, `03` (43–45 đỉnh, 8 xương) là hai hàng lông tơ ở gốc cánh |
| `chibang_q_l_01..20` | 20 | 33–52 | 80 | cánh DƯỚI phía xa (lông hồng rủ xuống), cùng cách tách |
| `weiba_l_02..04`, `weiba_r_04` | 4 | 53–55, 73 | 3–5 | nửa đuôi phía SAU thân (dải dẹt, 3 đốt `all16 > all17 > ...`) |
| `houzhi_l_01..07` | 7 | 56–62 | 8 | chân sau xa: đùi, ống, bàn, 3–4 móng rời |
| `qianzhi_l_01..10` | 9 | 63–71 | 13 | chân trước xa: bắp (07), ống (06), bàn (04), móng 01–03, 05, chùm lông khuỷu 08–10 |
| `hujian_l_01` | 1 | 72 | 1 | giáp vai xa |
| `shenti_01` | 1 | 74 | 9 | **cả thân là MỘT lưới 111 đỉnh**: cổ + ngực + bụng + hông, kèm hàng vảy cổ và mảng vảy bụng vẽ sẵn trong ảnh; bám `all2..all7` |
| `xiongjia_01..09` | 9 | 75–81, 162 | 4–8 | giáp ngực: hai tấm ách trái phải, ngọc giữa ngực (`08`, vẽ trước cánh gần), chùm lông dưới ngọc, bốn mấu nhỏ |
| `houzhi_r_01..08` | 8 | 83–90 | 8 | chân sau gần |
| `toufa_02, 04, 05, 06` | 4 | 91–94 | 41 (cả nhóm) | bờm dọc gáy và lưng (4 dải, mỗi dải 5–12 xương) |
| `chibang_h_r_01..31` | 31 | 95–125 | 107 | cánh TRÊN phía gần (bên trái hình) |
| `chibang_q_r_14..25` rồi `01..13` | 25 | 127–160 | 89 | cánh DƯỚI phía gần; **chân trước gần `qianzhi_r_01..09` (139–147) chen GIỮA hai lớp lông của cánh này** |
| `hujian_r_01` | 1 | 161 | 1 | giáp vai gần |
| `longjiao_01, 02` | 2 | 163, 166 | 1 mỗi cái | hai sừng (cứng, một xương), con của xương đầu `all8` |
| `toufa_03, 01` | 2 | 164, 165 | | chỏm bờm trên trán, giữa hai sừng |
| `tou_01..06` | 6 | 167–172 | 8 | đầu: sọ + mắt (01), hàm dưới (02), lòng miệng đỏ (03), ba tấm má / gáy (04–06) |
| `weiba_r_01..03`, `weiba_l_01` | 4 | 173–176 | | nửa đuôi phía TRƯỚC thân: **vẽ trên cùng, vắt ngang trước cả bốn chân** |
| `biyan` | 1 | 177 | 1 | mắt nhắm (ẩn; bật ở `hit`, `stun`, `die`) |

### 2.2 Cây xương và ràng buộc

`root > all` (cả con) `> all2` (hông: mọi clip dời / xoay ở đây) `> all3 > all4` (ngực) `> all5 > all6 > all7 > all8` (cổ → đầu).
- Dưới `all4`: bốn gốc cánh `all38` (trên gần, 109 xương), `all155` (trên xa, 103), `all63` (dưới gần, 92), `all127` (dưới xa, 83); mỗi gốc
  có một "cánh tay" 2–3 đốt (`all97 > all98`, ...) mang lông dài, còn lông phủ bám thẳng gốc cánh. Hai vai chân trước `all40 > all41 > all42`
  (gần), `all39 > all44 > all45` (xa), giáp vai là con của bắp chân.
- Dưới `all2`: đuôi sau `all16 > all17`, đuôi trước `all9 > all10`, hai hông chân sau `all15 > all19 > all20 > all21`, `all29 > all30 > all31 > all32`.
- **IK (6)**: chân trước `all41 + all42 → all43`, `all44 + all45 → all46` (đích là con của `all`, mang bốn xương ngón); chân sau
  `all19 + all20 → target`, `all30 + all31 → target3`, bàn chân `all21 → target2`, `all32 → target4`. Vậy **bốn bàn chân là bốn điểm điều khiển
  đứng yên trên đất**: muốn đi bộ, dậm chân thì lái bốn đích này.
- **Transform (16)**: 6 cái kéo gốc bờm theo cổ (`mixX/Y 0,5`); 10 cái mặc định mix 0 (bật trong clip bay, chạy, chết, `skill_03/04/05`).
- Hầu hết chuyển động là FK: mỗi clip có 460–496 timeline xoay (mọi đốt lông đều có khoá), chỉ 32–112 timeline dời.

### 2.3 Hai mươi clip (tờ `khung/`)

| clip | dài | nội dung | ta dùng làm |
|---|---|---|---|
| `idle_01` | 2,00 | thở, cánh trên khép mở nhẹ, đuôi và dây cánh lượn | **idle (giữ nguyên)** |
| `generate_01` | 1,83 | nằm cuộn tròn trong cánh → vươn dậy 0,4 → xoè bốn cánh dựng đứng, gầm 0,6–1,2 → về | (không dùng làm appear; lấy dáng xoè cánh gầm) |
| `die_01` | 1,43 | khuỵu 0,16 → gượng dậy 0,48 → bật lên không 0,64–0,96 (dời `all2` rất xa) → rơi sập nằm bẹp 1,11 → mờ hết 1,27 | **die (giữ nguyên)** |
| `fly_01` | 1,50 | lao ngang màn hình trong thế bay sấp, cánh dựng (chỉ thấy 0,33–0,67; đổi `inherit` 6 xương) | nguồn cho **fly** và nửa đầu **appear** |
| `run_01` | 1,53 | nhún 0,17 → bật lên không, bốn chân rời đất, cánh xoè ngang 0,34–0,51 → vỗ cánh 0,68 → đáp cúi thấp 0,85 → về | nguồn cho nửa sau **appear** (đáp bốn chân) |
| `skill_01_1/2/3` | 1,23 | cánh dưới gần quạt ra trước rồi phủ xuống (ba biến thể) | (để dành) |
| `skill_02_1` | 1,83 | ngẩng lấy hơi 0,2–0,41 → **chúi đầu tới trước sát đất, há mồm gầm** 0,61–1,22 (cánh trên dựng đứng) → về | **cast: gầm sóng âm** |
| `skill_02_2 / _3` | 1,83 | bản gầm ngửa đầu lên trời / chúi đầu xuống đất | nguồn pha cho chiêu cuối |
| `skill_03` | 2,53 | xoè cánh 0,56 → dựng bốn cánh, gầm 0,84 → **quạt cánh gần ra trước** 1,13–1,41 → sấp xuống quét 1,69–1,97 → về | nguồn chiêu cuối |
| `skill_04` | 2,33 | cúi 0,26 → **chồm dựng, hai chân trước giơ cao** 0,52–0,78 → **dậm xuống** 1,04 → cánh xoè, gầm 1,3–1,8 → về | **attack: dậm hai chân trước** (khung dậm ~1,0) |
| `skill_05` | 3,30 | sấp xuống xoè cánh sát đất 0,37 → dựng bốn cánh gầm 0,73–1,1 → khép cánh trùm thân 1,47 → mở 1,83 → dựng gầm lần hai 2,2 → khép 2,57–2,93 | nguồn chiêu cuối (dài nhất, 16 760 khoá) |
| `skill_06` | 1,23 | chân trước gần cào nhẹ ra trước | (để dành) |
| `hit_01/02` | 0,5 / 0,67 | giật lùi, nhắm mắt | **hit** |
| `stun_01` | 2,67 | gục đầu, nhắm mắt | (để dành) |
| `block_01`, `reward_01` | | thủ; ăn mừng (như `skill_02_2`) | |

**Timeline đặc biệt** (`keys_a.json`: `skill_04, run_01, fly_01, die_01, hit_01`):
- **Thứ tự vẽ đổi giữa clip** (`DrawOrder`): `skill_04` ở 0,37 / 0,87 / 0,90 / 2,13 s (chân trước giơ lên phải vẽ TRƯỚC cánh dưới và đuôi
  trước, dậm xong trả lại); `run_01` ở 0,37 / 0,77 / 0,83; `die_01` ở 0,70; `fly_01` ngay giây 0; cả `generate_01`, `skill_01_1/3`,
  `skill_03`, `skill_05`. `.atomik` chưa có thứ tự vẽ theo clip → mỗi slot đổi chỗ phải có slot sinh đôi ở chỗ mới, bật tắt hình theo
  `sample` (trường thứ tự vẽ), như bộ `~2` của tượng đá; hoặc thêm timeline thứ tự vẽ vào định dạng.
- **IK chân trước tắt khi chân rời đất**: `skill_04` mix 0 từ 0 tới 0,9 s (chân giơ lên là FK), bật lại đúng khung dậm; `fly_01` tắt cả
  clip; `die_01` tắt từ 0,93. Cùng lúc 8 transform constraint (chỉ số 8–15) đổi mix: ngón chân và bàn chân chuyển từ "bám đích trên đất"
  sang "theo ống chân". Lấy mẫu `l` đã nướng hết các thứ này.
- `fly_01` đổi `inherit` của 6 xương (đuôi, gốc cánh không thừa hưởng xoay của thân khi lộn) và làm mờ bóng (`shadow`) theo độ cao.
- Mắt nhắm `biyan`: slot 177, hiện bằng alpha trong `hit` (0,07–0,33 s), `die`, `stun`.
- `die_01`: 176 timeline tắt hình ở 1,43 s (cả con biến mất ở khung cuối), bóng mờ 1,13–1,27.

Con gốc KHÔNG có clip đi bộ bốn chân và không có clip bay vào rồi đáp: `walk`, `fly` (lặp), `appear`, chiêu cuối phải dựng ở tầng điều
khiển (skill mục "CLIP MỚI trên rig gốc"): lái `all2`, bốn đích IK chân, bốn gốc cánh; cánh lấy TRỌN dáng của một clip nguồn.

## 3. Thiết kế (đề xuất của Claude, chờ người dùng duyệt)

**Rồng trúc bốn cánh.** Lý do: con gốc là rồng lông vũ pha lê trắng – lam – hồng, sừng lửa. Các tướng Mộc đã có: chim lá (cánh lông lá +
cành hoa), hươu gỗ (gạc cành + bờm lá phong), người cây, voi rừng (tán lá), Voọc Tướng (giáp tre). Trúc chưa ai dùng làm chủ đề, hợp bóng
dáng (lông dài nhọn = lá trúc), và rất Việt (tre ngà).

| phần | con gốc | của mình |
|---|---|---|
| cánh trên | lông pha lê lam nứt vân, mảnh vỡ bay | quạt LÁ TRÚC ba tầng lục sẫm – lục – lục non, sống lá |
| cánh dưới | lông vũ hồng tím | lá trúc khô VÀNG NGÀ, hàng cuối lục non |
| dây cánh | dải lam móc cam | dây leo mảnh, nụ đỏ son ở móc |
| sừng | gạc lam bốc lửa cam | hai ỐNG TRÚC ngà vát nhọn, có mắt trúc, nhánh con hai lá |
| đầu | sọ chim – rồng trắng có mỏ | đầu rồng – lân mõm dài, nanh, KHÔNG mỏ; vảy ngọc |
| bờm | lục chanh – chàm | kem, ngọn lục non |
| thân | lông trắng, vảy cổ ô liu, vảy bụng chàm | lông kem (kiểu `nga`) hoặc mực than (kiểu `mac`), vảy cổ hình đốt trúc |
| giáp | vàng nhạt, ngọc opal | tre chẻ ngà, NGỌC BÍCH |
| chân | xám lam, móng lam | ống giáp trúc ba đốt, bàn ngà |
| đuôi | dải pha lê mint – tím | một chiếc lá dài như dải lụa, hai mặt lục / lục sẫm |

Hai kiểu màu: `nga` (sáng: kem + lục trúc + ngà vàng), `mac` (tối: mực than + lục bảo + vàng ngà).

Tệp: `ArtGen/Spine/moc_vuong.py` (`bo_cuc`: sơ đồ bố cục = khối từng part ở idle giây 0, tô phẳng bảng màu mình, tầng màu của lông lấy theo
tầng sắc của lông gốc; sừng vẽ mới bằng mã), `build_moc_vuong.py` (gói GPT) → `gui_gpt/moc_vuong_1/luot_1_concept_<kiểu>.txt`, ảnh về
`inbox/moc_vuong_1/tai_ve/L1_<kiểu>.png`.

## 3b. Người dùng duyệt (2026-11-13)

- Xem `L1_nga.png` (sáng) và `L1_mac.png` (tối): "**bản màu đen đẹp hơn** nhưng **2 cái sừng hình 2 ống tre không đẹp** và **sừng bên phải
  đang cắm ở sai chỗ theo logic**" (sừng xa mọc từ sau mõm). Gen ba kiểu sừng trên bản tối (`luot_1b_sung_<kiểu>.txt`: `mang` sừng măng xếp
  bẹ, `nhanh` gạc rồng, `liem` sừng liềm trúc đen), cả hai gốc sừng đặt trên đỉnh sọ sau mày.
- "**ok sừng măng, chốt, làm auto mode đi**" → `tai_ve/L1_duyet.png` (= `L1_mac_mang.png`).
- Concept chỉ bám LỎNG sơ đồ (GPT dựng thân cao hơn, đầu lệch phải): không nướng concept vào khung part được. Con trong game = bố cục và
  dáng của rig gốc + ngôn ngữ thiết kế của concept (màu, chất liệu, đầu, sừng, giáp). Phải nói rõ điều này khi báo người dùng.

## 3c. Đã làm sau khi chốt (2026-11-13, auto mode)

- **Mẫu khung** `scan/sample_dk.json` (16 clip, 30 khung/giây; có thêm `tc` độ trộn transform constraint, `ih` kiểu thừa hưởng: đã thêm vào
  `mo_xe/mo_xe.html`, cùng `transforms`, `inherit` cho `extra.json`). `fly_01` đổi `inherit` của đúng sáu xương đặc biệt về 0.
- **Mảnh theo khung part** (`moc_vuong.py`): `thiet_ke(part)` = hình bóng kín của part tô phẳng bảng màu `mac`; vai trò từng part ở
  `vai_cua` (lá, hàng lá, dây + nụ đỏ, dải đuôi, lông mực, ống giáp trúc ba vòng vàng, ngón + móng vàng, thân + vảy cổ vàng, giáp, ngọc,
  bờm, sọ + gờ mày vàng + mắt, hàm, lưỡi, tai lá). Vùng phụ (móng, vảy, mắt, gờ mày, nụ) tách theo sắc của ảnh part gốc (chỉ lấy vùng,
  không lấy màu). Sừng: ô riêng `o_sung` (sừng măng năm bẹ viền vàng, ô nằm ngang), không dùng hình bóng sừng lửa. `nhom_part` → 19 tờ
  Q1–Q19 theo nhóm (cánh trên gần / xa, cánh dưới gần / xa, đuôi, thân chân); Q20 đầu + bờm, Q21 hai sừng (dựng riêng, không dựng lại các
  tờ đang gen). `build_moc_vuong.py parts` viết prompt (ảnh 1 tờ hướng dẫn, ảnh 2 concept đã duyệt; đoạn "WHAT THE PIECES ARE" ghép theo
  kiểu part có trên tờ). `moc_vuong_gen.py` chạy nối các tờ, về tờ nào cắt tờ đó (`cat_part`, IoU vào `manh/part/_iou.json`). Tờ thử Q2:
  IoU 0,91–0,95. `can_mau` kéo trung vị từng vùng màu về bảng màu chuẩn → `manh/part_cb/` (rig ưu tiên).
  Codex dùng chung khoá với hai phiên khác (giac_moc, kiem_si_non): hàng chạy xen kẽ, chậm.
- **Rig** `moc_vuong_rig.py` (KG 0,30; PXU 0,40): 508 xương của họ + `root`, `move`, `mieng`, `chan_tg`, `chan_tx`, `far`. Sáu xương inherit 2
  (`all12`, `all18`, bốn gốc cánh): dáng gốc và từng khung tính từ ma trận thế giới (`m`) chia ma trận cha. Xương khác: ma trận riêng của
  Spine dựng từ `l` (có xiên tới 180° = lật) rồi tách xoay + tỉ lệ có dấu. Thứ tự vẽ: `day_chung` ghép mọi thứ tự gặp trong clip dùng
  thành một dãy (dãy con chung dài nhất), slot lặp thành bản `~k`; mỗi khung bật hình ở bản đúng chỗ (`P.att`), không dùng độ đậm (khỏi
  mờ đôi lúc game trộn clip). Bản thử da tạm: 200 slot (24 sinh đôi, 7 thứ tự), 3285 đỉnh, `.atomik` 755 KB.
  Sừng: ô cứng bám xương `jiao`, `jiao2`, co 0,76 dài × 0,68 ngang, xoay −8° / −18° (chỉnh lại khi có da thật).
- **Clip** (`CLIPS`): `idle` = idle_01; `hit` = hit_01; `die` = die_01; `attack` = skill_04 (sự kiện `chom` 0,52, `dam` 0,93, `trung` 1,15 =
  sét giáng, `gam` 1,3); `cast` = skill_02_1 (`hit_hoi` 0,2, `gam` 0,62 = khung nhả, `het_gam` 1,25).
  - `appear` (1,64 s, ghép trong rig từ run_01: lấy từ lúc đã rời đất, lượn vào 0 → 0,58 chậm dần, treo giương cánh tới 0,80, RƠI nhanh
    tới 0,91 `cham_dat`, rồi phần đáp – về của họ; cả con dời trên `move` từ (−1180, +560) đơn vị; hiện dần 0,14 s; bẹp nảy lúc chạm).
  - `fly` (0,8 s lặp, từ fly_01 0,5 → 1,3: bỏ đường bay của `all2` và bốn đích bàn chân, trừ dần độ trôi hai đầu để khép vòng, cao 300
    đơn vị, nhấp nhô theo nhịp cánh).
  - `skill` (3,31 s) = skill_05 0 → 1,47 (sấp xoè cánh, dựng cánh gầm, khép cánh thành KÉN) + pha 0,13 s + skill_03 0,82 → hết (kén
    BUNG dựng cánh, QUẠT cánh chém tới = `trung` 2,00, sập cánh quét 2,50).
  - `walk` (1,2 s lặp, `moc_vuong_clip.py`, runtime giải IK): nền idle_01, bốn đích bàn chân đi kiểu chéo (sải 230, nhấc 105), thân nhún
    hai lần mỗi chu kỳ, bốn gốc cánh nảy trễ, hai gốc đuôi đung đưa (con gốc che gần hết chân nên bước đi phải đọc qua cả khối thân).
- **Hiệu ứng trong game** `Assets/01 Script/Game/Battle/HatRong.cs` (đã biên dịch thử sạch bằng csc của Unity, CHƯA xem trong trận):
  `n_rong_dam` (đánh thường: bụi chồm, DẬM, ba chỗ đất nứt chạy tới, SÉT gấp khúc giáng vào đầu đối thủ đúng khung trúng), `n_rong_gam`
  (lấy hơi hút lá, bảy đợt sóng âm hình cung lao tới, rung màn từng đợt), `n_rong_van` (chiêu cuối VẠN DIỆP: vòng đất, lá cuốn lên, lá
  hút vào kén + măng nhú báo trước, kén bung, bão lá + sáu lưỡi chém, rừng măng trúc + cột lá + sét kết liễu). Đã gắn: `StageView.MocAtk`,
  `MocFx` ("thanh_long"), `HatNuoc.PlayNuoc` / `HoldNuoc` / `WThemes`.
- **Vào game** (chưa chạy): `quai/doi_moc_vuong.py` (`chep` rig vào thư mục MỚI `Resources/moc_vuong_1/`; đổi `aola` của `thanh_long` và
  ba dạng sang `moc_vuong_1`; giữ tên Thanh Long, thẻ, số dạng → không đổi golden; `--ve_cu` trả lại). Không đè file Thanh Long cũ.

## 3d. Kết quả lượt đầu (2026-11-13, khoảng 03:25)

- 21 tờ mảnh Q1–Q21 đã gen và cắt, IoU hình bóng 0,91–0,99 (không tờ nào phải gen lại); `can_mau` 175 mảnh (lệch kênh trung vị 14).
- Rig da thật: 512 xương, 237 slot (61 bản sinh đôi cho 10 thứ tự vẽ), 3802 đỉnh, atlas 1368 × 1392, **`.atomik` 938 KB**; khung đầu
  `appear` và khung cuối `die` trống; mọi clip không lặp nối về idle lệch 0 px; `fly` khép vòng 7 px (bước thường 125). Lược khoá RDP
  lệch tối đa 3,9 px giữa clip. Tờ khung bằng runtime Spine thật: `rig/khung_rt/`; trang xem `rig/xem.html` (đã kiểm bằng `thu_xem.py`
  với đường dẫn TUYỆT ĐỐI; đường dẫn tương đối cho DOM rỗng).
- Sừng: co 0,66 dài × 0,82 ngang (bản 0,76 × 0,68 trông như hai cái râu; 0,66 × 0,95 to quá đầu). `CAO_KHAI` 1,12: game vẽ nhỏ lại chừng
  11 % (ở cỡ dạng 3 = 1,16 cánh chờm bảng tên và sát bệ đối thủ).
- **Trong game:** `quai/doi_moc_vuong.py chep` + đổi `aola` (đã chạy), Unity biên dịch sạch, "Nhập dữ liệu", "Gắn dạng .atomik vào prefab
  tướng" (`thanh_long: prefab giữ 3 dạng (moc_vuong_1 ×3)`), tour "Đảo Mộc: Thanh Long ra trận ở 3 dạng" chạy hai lượt (da tạm, da thật),
  console không lỗi; ảnh `Temp/PokiShots/thanh_long_combat/`, tờ ghép `rig/xem_trong_tran.jpg`. Sau khi đổi `CAO_KHAI` CHƯA chụp lại trận.
- Sóng âm bản đầu là một nét mảnh; đã đổi thành dải dày (bốn cung lồng sát + hai viền mực), hai lớp kem và lục nhạt.
- **Chưa làm / còn yếu:** chưa xem ở tốc độ thật trong trận và trên Android; `walk` khó đọc (chân bị cánh dưới và đuôi che); `appear`, `walk`,
  `fly`, `die` chưa thấy trong game (tour chỉ chạy cast, skill, attack); ba dạng của suất cùng một rig (chưa có dạng non, chưa có `evolve`);
  sóng âm còn thô; chưa chạy EditMode test; chưa thử hộp chi tiết tướng.

## 4. Kế hoạch sau khi duyệt concept (auto mode)

1. Quét `sample` 30 khung/giây các clip dùng (`idle_01, die_01, hit_01, skill_04, skill_02_1/2/3, skill_03, skill_05, fly_01, run_01,
   generate_01`), xuất `parts/` từng part cắt theo lưới.
2. Mảnh theo KHUNG PART (skill mục 00 "CÁCH CHUẨN"): thân `shenti` + cổ là một lưới sẵn nên không phải lo nối; lông cánh mỗi chiếc một ô
   (107 + 45 lông: khoảng 8–10 tờ Q), đầu / sừng / giáp đặt tự do theo concept (mảnh cứng 1–8 xương).
3. Rig = của họ (`gan_nguyen`), IK và transform nướng qua `sample.l`.
4. Clip: `idle`, `die`, `hit` của họ; `attack` = `skill_04`; `cast` = `skill_02_1`; `appear`, `walk`, `fly`, `skill` dựng ở tầng điều khiển.
5. VFX ngoài rig: địa chấn + sét (attack), sóng âm + rung màn (cast), chiêu cuối. Xương bám `mieng`, `chan_truoc`; sự kiện đúng khung.
