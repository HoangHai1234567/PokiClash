# Tinh linh tinh thể sắt (`tinh_sat`): tướng 1 đảo Kim

Bắt đầu 2026-11-15 (máy ổ D). Con gốc của rig: `monster_3346` (khối tròn trắng mặt ":3", 9 tinh thể bay quanh, đuôi 3 tinh thể; game tham khảo,
kho `D:\RefAnimation\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `idle_01`). Xương, lưới, chuyển động gốc là của nhà phát hành
game đó (như aola): dùng nội bộ, không đăng công khai. Hình là của mình. Suất 1 đảo Kim = ải 1 ("Cảng Sắt", `IslandGen.Plan Kim`), id game hiện là
**`bo_cap`** (Bọ Cạp Đồng, 3 dạng). Mã làm việc `tinh_sat`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-15)

- "làm tướng 1 đảo kim, **concept như ảnh**".
- "**idle / die / walk làm giống con gốc**, sửa đi chút cũng được".
- Đánh thường: "**lao vào tông vào đối thủ**".
- Chiêu mana: "**gọi tất cả các tinh thể sắt quanh người đâm vào đối thủ**, làm các tinh thể sắt **bay lên trên đầu**, sau đó **dùng code điều khiển**".
- Chiêu cuối: "**phình to cơ thể nhảy dập lên đầu đối thủ**, làm hiệu ứng kiểu **rung rung squash stretch giống tướng 1 đảo Thủy**" (Tí Tách).

## 2. Mổ rig gốc (`<SXS>/scan/monster_3346/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample_goc.json` 12 clip 30 khung/giây, `keys.json`,
`khung/`, `mo/`, `parts/`)

24 xương, 20 slot (19 hình đang bật + 2 hình mắt phụ), 12 clip, 2 796 khoá. **FK thuần**: không IK, transform, path, physics. Con nhìn sang PHẢI
(hơi nghiêng). Atlas 0,749 px / đơn vị rig. Dáng idle x −264..209, y 25..378: con LƠ LỬNG (đáy thân y 109, gốc / bóng ở y 0). Script mổ:
`tinh_sat.py` (`mo`, `nhom`, `part_goc`; dùng lại hàm của `hoa_ho.py`).

Cây xương: `root` → `all` (y −99,7; không clip nào động) → `all2` (TÂM THÂN, mang mọi thứ; idle nhún ±24, attack quật tới +187) → mọi xương
mảnh là con trực tiếp của `all2`, trừ đuôi `all15 → all17 → all18` và hai chân (`all16 → all20`, `all22 → all21`).

| thứ tự vẽ | slot | ảnh vùng (px) | là gì | xương |
|---|---|---|---|---|
| 1 | `bin8` | 72×58 | tinh thể nhỏ dưới cánh phải | all14 |
| 2 | `bin6` | 128×91 | tinh thể cánh dài PHẢI (sau thân) | all12 |
| 3–5 | `tail3`, `tail2`, `weitail1` | 96×46, 41×44, 42×45 | đuôi: tinh thể dài nhọn, tí hon, nhỏ sát đáy | all18, all17, all15 |
| 6 | `bin7` | 75×42 | tinh thể nhỏ dưới cánh trái | all13 |
| 7 | `bin9` | 71×107 | tinh thể lớn trên đầu bên phải | all10 |
| 8 | `youshou` | 35×53 | tay phải (mẩu trắng, mép giáp thân không viền) | all6 0,9 + all2 0,1 |
| 9 | `youjiao` | 38×41 | chân phải | all20 + all16 |
| 10 | `body` | 156×143 | thân tròn trắng (13 đỉnh, một xương) | all2 |
| 11 | `zuojiao` | 47×42 | chân trái | all22 + all21 |
| 12 | `zuoshou` | 38×55 | tay trái | all3 |
| 13–14 | `bin5`, `bin4` | 32×34, 26×31 | tinh thể vuông tí hon trên hai má (ô 4 đỉnh) | all4, all5 |
| 15 | `bin2` | 130×83 | tinh thể cánh dài TRÁI | all11 |
| 16 | `bin1` | 65×73 | tinh thể nhỏ giữa đỉnh đầu (ô 4 đỉnh) | all8 |
| 17 | `mt` | 37×25 | miệng ":3" (ô 4 đỉnh) | all19 |
| 18 | `bin3` | 82×98 | tinh thể lớn trên đầu bên trái | all9 |
| 19 | `eyes` | 95×43 | MỘT ảnh hai mắt; hình phụ `biyan` (nhắm `> <`), `yun` (choáng xoáy) | all7 |

"Tai mèo" trên đỉnh thân chỉ là phần thân tròn lộ giữa các tinh thể. Mắt đổi hình theo khung (`n` của mẫu khung): idle chớp `biyan`, đòn / chiêu /
trúng đòn / chết nhắm `biyan`, `stun_01` dùng `yun`.

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho |
|---|---|---|---|
| `idle_01` | 3,20 | nhún, tinh thể đung đưa, chớp mắt | **idle** |
| `run_01` | 1,33 | lắc lư đi | **walk** |
| `skill_01_1` | 0,77 | ngả ra sau lên cao (khung 0–13), QUẬT tới +187 (khung 14–16), nảy về | **attack** (tông) |
| `skill_01_2` | 0,77 | vươn cao, nhún | (chưa dùng) |
| `skill_02` | 1,20 | co tinh thể sát người (khung 3–16), bung tinh thể ra quanh người, về | **cast** (đoạn co) |
| `hit_01`, `hit_02`, `block_01`, `floating_01`, `stun_01` | | | **hit** = hit_01 |
| `die_01` | 1,00 | văng xoay, đổ bẹp, tinh thể xoè | **die** + tan 0,45 |

## 3. Rig thử trên DA GỐC (chỉ để soi clip trong máy, KHÔNG đưa vào game, không đăng)

`TS_GOC=1 py -3 -I tinh_sat_rig.py [soi <clip> n=12]` → `inbox/tinh_sat_1/rig_goc/`. 26 xương (24 của họ + `move`, `day` ở đáy thân là tâm phình /
bẹp), 19 slot, 140 đỉnh (nguyên lưới của họ; hình region đổi thành lưới 4 đỉnh). Chiều cao 378.

- `idle` = idle_01, `walk` = run_01, `hit` = hit_01, `die` = die_01 + tan.
- `attack` 1,0 s = skill_01_1: lấy đà 0–0,42, quật tới, **`tong` = `trung` 0,52**; quãng tới của `all2` dồn sang `move` (đỉnh lao 0,62 chiều cao,
  sân nắn tới 72 % quãng), thân bẹp theo chiều tông đúng khung chạm.
- `cast` 2,38 s: co tinh thể (skill_02 tới khung 10, `tu` 0,05); 8 tinh thể (`BAY`: hai cánh, ba trên đầu, hai dưới cánh, đuôi dài) lần lượt bay
  lên xếp **vòng cung ôm quanh đầu**, mũi chĩa về đối thủ (điểm `DICH`), nhấp nhô; lùi lấy đà theo trục rồi **phóng** (`ban` 0,98 → 1,51, cách
  0,075 s, chuỗi = tên xương; tinh thể ẩn trong rig, CODE GAME cho bay); `het_ban` 1,56; **mọc lại** đúng chỗ (`moc` 1,69, nở vượt nhẹ). Thân
  hoà dần từ dáng co về idle.
- `skill` 1,2 s: PHÌNH to 1,32 lần + tinh thể xù ra, nhún (bẹp 1,2 × 0,66), **bật** (`bat` 0,83), kết thúc ở dáng đang bay (không hoà về idle).
- `skill_land` 1,0 s: rơi duỗi → **DẬP** (`cham_dat` 0,15) bẹp 1,66 × 0,48, tinh thể văng xoè → **rung squash stretch tắt dần** (chu kỳ ~4 khung)
  → xẹp về cỡ thường. Cả con hạ xuống cho đáy thân chạm chỗ đáp rồi nổi lên lại (con lơ lửng). Game đã có sẵn đường `skill` → cung nhảy →
  `skill_land` (làm cho Tí Tách: `AolaSticker.Jump`, `StageView.Place`).
- `appear` 0,8 s (Claude tự đặt): thân bật ra, các tinh thể bay từ ngoài vào xoay rồi ráp quanh người.

## 4. Concept (Claude đề xuất ba hướng màu, CHỜ người dùng chọn)

Gói `gui_gpt/tinh_sat_1/` (`tinh_sat_da.py concept`), ảnh mẫu 1 = hình cả con gốc `mau/goc_ca_con.png`. Giữ nguyên dáng, mặt ":3", từng mảnh.
- `tai_ve/L1_A.png` **thép lam** (gần màu con gốc nhất): tinh thể lớn thép lam, nhỏ dưới cánh bạc lam, đuôi thép oải hương; thân kem.
- `tai_ve/L1_B.png` **sắt rèn đen**: mọi tinh thể xám than, cạnh mặt bạc, đuôi ánh tím; thân trắng bạc; mắt hổ phách.
- `tai_ve/L1_C.png` **bạc + đồng thau**: tinh thể lớn bạc, nhỏ + đuôi + má đồng thau; thân ngà (lượt đầu `L1_C_hong.png` lệch bố cục, đã gen lại).
Claude đề xuất **A**. Mặt giữ y con gốc theo lời "concept như ảnh" (luật chung muốn mặt "chiến" hơn: có thể thêm mày quả quyết nếu người dùng muốn).

### 4b. Lượt 1b: ĐỔI KIỂU DÁNG (người dùng xem trang concept: "nhìn giống con gốc quá")

Ba hướng màu ở trên bị trả (chỉ đổi màu, hình y con gốc). Lượt 1b (`tinh_sat_da.py kieu`, ảnh mẫu 1 = `L1_A.png` để giữ bố cục) giữ số mảnh,
chỗ, cỡ, hướng, thứ tự chồng (lắp được lên đúng xương), đổi kiểu dáng mặt, thân, mọi tinh thể; bỏ mặt ":3":
- `tai_ve/L2_1.png` **lưỡi thép**: vương miện ba lưỡi giáo, cánh là hai lưỡi kiếm có chắn, dưới cánh là phi tiêu, đuôi vòng xích + mắt xích + mũi
  tên; thân trắng thép có đai bụng đinh tán; tay chân sắt; mắt tròn con ngươi xanh đen + mày quả quyết, miệng cười có một răng nanh.
- `tai_ve/L2_2.png` **quặng khối**: tinh thể thành cụm khối lập phương (vàng đồng thau + sắt từ sẫm), cánh là hàng ba khối nhỏ dần, đuôi khối +
  thỏi sắt nhọn; trán có dấu nam châm móng ngựa; mắt vuông bo hổ phách.
- `tai_ve/L2_3.png` **bismuth bậc thang**: tinh thể thành khối bậc thang nhiều dải màu phẳng (vàng, hồng tím, xanh ngọc), thân sắt sẫm, mắt vàng
  xếch không con ngươi, miệng cười răng vuông.
Mảnh đổi dáng sẽ là ô cứng một xương đặt đúng chỗ mảnh cũ (như `dat_nung` lượt 4–5); mắt / miệng mới phải vẽ lại cả bản nhắm, choáng.

### 4c. Lượt 1c: SỬA NHẸ (người dùng: lượt 1b "xấu quá, giữ dạng tinh thể như vừa rồi, sửa khác đi chút thôi")

`tinh_sat_da.py sua`, ảnh mẫu duy nhất `L1_A.png`, khối KEEP IDENTICAL / CHANGE:
- `tai_ve/L3_1.png` mày xếch quả quyết, miệng cười một răng nanh, mọi tinh thể dài nhọn hơn ~15 %, má là sao bốn cánh bạc (Claude đề xuất);
- `tai_ve/L3_2.png` năm tinh thể lớn có đai sắt đinh tán ôm gốc, mắt nheo, miệng thẳng có răng nanh, má đinh tán tròn;
- `tai_ve/L3_3.png` mỗi tinh thể lớn mọc thêm tinh thể con, đuôi chẻ đôi, mắt con ngươi khe, miệng cười há.
CHỜ người dùng chọn. Mảnh đổi dáng (tinh thể dài hơn, đai, mắt mới) là ô cứng một xương đúng chỗ mảnh cũ; mắt mới phải vẽ lại bản nhắm, choáng.

### 4d. Chốt concept + rig da mình (2026-11-15 ~02:40)

Người dùng chọn phương án 1 của lượt 1c → `tai_ve/L1_duyet.png` (= `L3_1.png`). Vì tinh thể đổi dáng (dài, nhọn hơn) nên KHÔNG đổi da theo khung
part (tờ P, Q, R bỏ); mảnh gen "đúng chỗ, đúng cỡ" từ concept (`tinh_sat_manh.py`): nhóm M1 (hai cánh, đuôi dài, hai chân), M2 (thân trơn
không mặt, đuôi tí hon), M3 (hai tinh thể lớn trên đầu, hai tinh thể dưới cánh), M4 (tinh thể giữa đầu, tinh thể đuôi nhỏ; Codex vẽ thừa hai
bàn chân → `BO_CUM`), M5 (hai tay, có toạ độ), F1 (mắt + mày, miệng răng nanh, hai sao má), F2 (mắt nhắm `> <`), F3 (mắt choáng). Ghép lại so
concept: IoU hình bóng 0,959 (`manh/_ghep.png`).
Rig (`tinh_sat_rig.py`, `gan_moi`): mỗi mảnh là lưới 4 đỉnh đặt đúng chỗ concept (concept vẽ đúng khung 0 idle: `mau/goc_ca_con.json`), điểm gắn
tính bằng ma trận idle 0; chân, tay phải lấy trọng số 3 đỉnh gần nhất của lưới cũ. Tay trái chuyển ra SAU thân (concept là cục u ở sườn).
`inbox/tinh_sat_1/rig/`: 26 xương, 19 slot, 84 đỉnh, .atomik 126 KB, chiều cao 401; mọi clip nối về idle 0 px. Ảnh động 8 clip
(`_xem_dong.py` → `rig/dong/`, chiêu cuối ghép cung nhảy giả) đã lên artifact riêng tư https://claude.ai/artifact/PUGUTpxuyDjyCsabYarY36. CHỜ người dùng xem.

### 4e. Chiêu cuối bản 2 (người dùng: "chiêu cuối chưa đủ ấn tượng" → "ok" làm đủ ba pha Claude gợi ý)

- RIG (đã làm, `tinh_sat_rig.py` f_skill / f_land): skill 1,86 s: ba nhịp bơm phồng (đỉnh 0,18 / 0,48 / 0,85; tới 1,66 lần), tinh thể xoè theo nhịp
  rồi khoá chĩa ra (quả cầu gai) và run; nhún 0,98 → 1,21; `bat` 1,24; khựng + lộn một vòng quanh tâm thân (`all2` −360°) 1,50 → 1,74 (đỉnh cung
  của game rơi đúng đây vì game bay từ bat tới cham_dat); cắm xuống, tinh thể dồn lên như đuôi sao chổi. skill_land 1,15 s: `cham_dat` 0,10, bẹp
  1,86 × 0,42 (× 1,66), tinh thể cắm phập xuống quanh người rồi bật về, rung 4 nhịp tắt dần trong lúc xì hơi về cỡ thường. IMPACT skill
  (0,22; 1,2; 0,3; chớp trắng), `span` 4,4. .atomik 129 KB.
- CODE GAME (làm lúc vào game): (1) `AolaSticker.Jump` cho con này đường cung "lên nhanh, TREO ở đỉnh, cắm xuống nhanh" (độ cao: ease-out tới
  u 0,42, giữ tới 0,62, ease-in xuống; ngang 1 − (1 − u)^1,5; như `_xem_dong.py` hàm `nhay`); (2) VFX: bóng đen to dần dưới chân đối thủ lúc
  rơi, vệt rơi; lúc dập khựng / rung / chớp, sóng xung kích, đất nứt, VÒNG CỘT TINH THỂ SẮT trồi lên quanh đối thủ rồi vỡ vụn, mảnh sắt văng;
  lúc gồng mảnh sắt nhỏ dưới đất hút về, bụi xoáy.

## 5. Việc tiếp

1. (xong) concept, mảnh, rig da mình. Người dùng xem ảnh động, góp ý.
2. Hỏi: thay suất `bo_cap` (Bọ Cạp Đồng) không đè `bo_cap_1..3` cũ? tên, số dạng (con gốc trông như dạng 1: có làm thêm dạng sau)?
3. Vào game: script `quai/doi_tinh_sat.py` (như `doi_nui_lua.py`), VFX riêng (tinh thể bay homing tới đối thủ theo sự kiện `ban`, nổ mảnh sắt khi
   trúng; sóng dập ở `cham_dat`), heroes.json, menu Unity.
