# Quỷ xích (`quy_xich`): tướng 5 đảo Kim

Bắt đầu 2026-11-16 (máy ổ C). Con gốc của rig: `monster_3408` (quỷ béo tím, cánh dơi, mũ giáp sẫm sừng hồng, gai tinh thể đỏ ở lưng và giáp
vai, xích chéo ngực có ổ khoá đồng, đuôi mũi tên, tay cầm móc lưỡi liềm nối xích; game tham khảo, kho `D:\Ripper\SwordxStaff`). **Người dùng
không chỉ con gốc**: Claude tìm trong kho theo tên mảnh xích (`suolian`), con duy nhất là quỷ béo cầm móc nối xích và có `skill_01` quay xích
ném (đúng lời dặn "chiêu mana làm giống skill_01"). Các ứng viên khác có xích (3614, 3616, 3626, 3632, 3651, 3652, 3670) đều không phải quỷ béo
cầm móc. Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là của mình. Suất 5 đảo
Kim = ải 20 ("Gác Chuông Đồng", `IslandGen.cs` Plan Kim), id game hiện là **`khien_bac`**. Mã làm việc `quy_xich`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-16)

- "làm tướng thứ 5 của đảo kim; concept **quỷ béo mặc giáp, vũ khí là móc liền gắn với xích sắt**".
- "**idle / walk làm giống họ**".
- appear: "làm nó **bay vào rồi rơi xuống**".
- Đánh thường: "**bay tới dùng móc gõ vào đầu** đối thủ".
- Chiêu mana: "làm **giống skill_01, quay xích ném** đối thủ".
- Chiêu cuối: "**xích sắt bốc lửa, xoay xích tạo ra trail lửa và khói, ném trói đối thủ sau đó thiêu đốt**; thêm FX / animation **1 cột lửa
  rất to, thiêu cháy** đối thủ".
- die: chưa dặn (con gốc có `die_01`: bị hất, lộn, nằm ngửa).

## 2. Mổ rig gốc (`<SXS>/scan/monster_3408/`: `info.json`, `att_goc.json`, `att_idle0.json`, `khung/`, `khung_rong/`, `mo/`, `parts/`;
script `quy_xich.py` mo / nhom / part_goc)

88 xương, 72 slot (56 hình bật ở idle 0), 9 clip, 3 510 khoá. Ràng buộc: **IK hai chân** (`L` → `bone6`/`bone7`, `R` → `bone4`/`bone5`, bend
−1; `L2`, `R2` một xương bàn chân), **21 path constraint** (`xian_1..5`): xích quấn ngực (`bone41..54`, con của `bone40` = ổ khoá) chạy trên
các đường `xian_1..4`; `xian_5` (con của `bone14b2`, xương móc) dẫn 7 mắt xích tay khi xích duỗi dài. Không transform, không physics. Con
nhìn sang PHẢI. **Tay cầm móc là tay XA** (vẽ SAU thân, bên phải hình): `P_shouL1/L2` + ngón `P_shouL31..33` (ngón vẽ TRƯỚC móc); tay GẦN
(trái hình, vẽ trước thân) là `P_shouR1/R2` + ba vuốt `P_shouR31..33`.

Cây xương chính: `root` → `bone` → `bone2` → `bone3` (HÔNG / TÂM; bụng `P_duzi` bám bone3 + bone9 + bone24) → `bone8` → `bone9` (NGỰC) →
`bone10` → `bone11` (ĐẦU; mặt, hai sừng) → `bone12` (mũ) → `bone55` (đỉnh mũ). `bone9` → `rotate_01` → `bone13` → `bone14` → `bone14b` (TAY
XA cầm móc: bắp, cẳng, nắm tay; ngón `bone15..17`) → `bone14b2` (MÓC) → `bone14b4..10` (mắt xích treo dưới cán); `bone14b` → `bone14b13..19`
→ `bone14b11` (chuỗi xích phụ, ẩn ở idle). `bone9` → `bone18` → `bone19` → `bone20` → `bone20b` (TAY GẦN; vuốt `bone21..23`). `bone9` →
`bone27..32` (CÁNH trái hình, chuỗi 6), `bone33..38` (CÁNH phải hình). `bone3` → `bone39..39d` (ĐUÔI). `bone9` → `bone40` (ổ khoá) → `bone41..54`
(mắt xích ngực). Chân: `bone3` → `bone4` → `bone5` (+ `bone59` bàn), `bone3` → `bone6` → `bone7` (+ `bone58`).

| thứ tự vẽ | slot | ảnh vùng (px) | đỉnh | là gì | xương |
|---|---|---|---|---|---|
| 1 | `P_chibang` | 138×103 | 24 | CÁNH trái hình (lưới) | bone27..29 |
| 2 | `P_chibang2` | 138×103 (cùng ảnh) | 24 | CÁNH phải hình | bone33..35 |
| 3 | `P_shouL1` | 91×99 | 15 | bắp tay XA (cầm móc) | bone13 0,84 + bone14 |
| 4 | `P_shouL2` | 126×91 | 16 | cẳng tay + nắm tay XA | bone14 / bone14b / bone13 |
| 5–11 | `W_wuqi2`, `W_sB05..07`, `W_sA05/08/09` | | | (ẩn) mắt xích phụ của skill_01 | bone14b11..19 |
| 12–17, 19 | `W_sB02..04` (35×44), `W_sA02..04`, `W_sA06` (17×42) | | 4 | 7 MẮT XÍCH treo dưới cán móc (hai ảnh: `W_suolian2` mắt nhìn thẳng, `W_suolian1` mắt nhìn nghiêng) | bone14b4..10 |
| 18 | `W_wuqi` | 136×234 | 15 | MÓC: lưỡi lưỡi liềm, khâu sẫm có tinh thể đỏ, cán, vòng cuối | bone14b2 |
| 21–23 | `P_shouL32/33/31` | ~40×35 | 4 | ba NGÓN tay xa (vẽ trước cán móc) | bone16 / 15 / 17 |
| 24, 25 | `P_tuiR2`, `P_tuiR1` | 34×24, 51×36 | 9 | bàn chân, chân phải hình | bone59 / bone4 / bone5 |
| 26 | `P_weiba` | 142×38 | 22 | ĐUÔI mũi tên | bone39..39d |
| 27 | `P_duzi` | 232×188 | 24 | BỤNG phệ + quần sẫm | bone3 0,49 + bone9 0,35 + bone24 |
| 28–30 | `P_jiejing3/2/1` | 22×19, 22×24, 36×43 | 4 | ba GAI tinh thể đỏ trên lưng | bone9 / bone10 / bone10 + 11 |
| 31, 32 | `P_tuiL2`, `P_tuiL1` | 38×26, 51×32 | 13 | bàn chân, chân trái hình | bone7 / bone58 / bone6 |
| 33 | `P_jianjiaL` | 72×73 | 7 | giáp vai nhỏ (sau đầu, phải hình) | bone25 |
| 34 | `P_xionqiang` | 167×120 | 12 | NGỰC | bone9 / bone10 / bone8 |
| 35 | `P_bozi` | 80×69 | 12 | CỔ / cằm | bone9 + bone11 |
| 36, 37 | `P_xiongjiaL1`, `P_xiongjiaR1` | 25×48, 62×60 | 7–10 | mảnh giáp sẫm hai bên cổ | rotate_01 / bone18 |
| 38–51 | `S1..S4_suolian*` | 35×44, 17×42 | 4 | 14 MẮT XÍCH chéo ngực (path) | bone41..54 |
| 52 | `P_suo` | 55×55 | 8 | Ổ KHOÁ đồng chỗ hai xích chéo | bone40 |
| 53 | `P_jiaoL1` | 52×87 | 6 | SỪNG to cong (phải hình) | bone11 |
| 54 | `P_toukui3` | 64×55 | 7 | má mũ phải (SAU mặt) | bone12 |
| 55 | `P_tou` | 92×96 | 15 | MẶT (hai mắt xếch, miệng cau, một nanh) | bone11 0,71 |
| 56 | `P_toukui1` | 60×83 | 12 | má mũ trái (trước mặt) | bone12 |
| 57 | `P_toukui2` | 72×52 | 9 | ĐỈNH mũ (dải trán hai khe) | bone55 |
| 58 | `P_jiaoR1` | 37×68 | 7 | SỪNG ngắn (trái đỉnh) | bone11 |
| 59–61 | `P_shouR31..33` | ~35×43 | 4 | ba VUỐT tay gần | bone23 / 21 / 22 |
| 62, 63 | `P_shouR1`, `P_shouR2` | 98×103, 114×123 | 15–17 | bắp, cẳng tay GẦN (trái hình, trước thân) | bone19 / bone20 / bone20b |
| 64 | `P_jianjiaR` | 101×103 | 7 | GIÁP VAI to (trái hình) có gai tinh thể đỏ | bone26 |

Clip của họ (tờ `khung/`, `khung_rong/` khung nhìn rộng):
| clip | dài | động tác | dùng cho (dự kiến) |
|---|---|---|---|
| `idle_01` | 4,00 | thở, cánh vỗ nhẹ, móc lắc | **idle** (giống họ) |
| `run_01` | 0,80 | nhún chạy, cánh vỗ, xích kéo lê đất | **walk** (giống họ) |
| `skill_01` | 1,50 | giơ móc, QUAY xích vòng qua đầu (0,20–0,65), móc ẨN từ 0,72 (bay đi: phần bay do code của họ), tay duỗi về trước giữ xích; móc hiện lại trong tay 1,17–1,37 | **cast** (quay xích ném) + nguồn cho chiêu cuối |
| `skill_02` | 1,33 | thu người, BAY VỌT lên khỏi khung (0,24–0,61), rơi xuống chúi người (0,73), đáp, đứng | **appear** (bay vào rồi rơi), **attack** (bay tới gõ móc) |
| `die_01` | 1,00 | bị hất lộn, nằm ngửa, móc rơi cạnh | **die** |
| `hit_01`, `hit_02`, `block_01`, `stun_01` | | | **hit** = hit_01 |

## 3. Concept lượt 1 (Claude đề xuất ba hướng, CHỜ người dùng chọn)

Gói `gui_gpt/quy_xich_1/` (`quy_xich_da.py ca_con`, `concept`). Ảnh mẫu 1 = hình cả con gốc `mau/goc_ca_con.png` (khung 0 idle, 1,223 px /
đơn vị; khung bao từng part trong `.json`); ảnh 2 = chiến binh sắt (nét, tô thép phẳng); ảnh 3 = quỷ đao (thân quỷ chắc, giáp sắt sẫm). Mọi
hướng giữ dáng, chỗ, cỡ từng mảnh, mặt nghiêng phải hai mắt xếch miệng cau một nanh, cánh dơi, đuôi; đổi dáng mảnh nhận diện (mũ, sừng, ba gai
lưng, gai giáp vai, lưỡi móc) và THÊM GIÁP thân (lời dặn "mặc giáp"):
- `tai_ve/L1_A.png` **quỷ đỏ, giáp gang sẫm**: mũ chảo tròn có sống giữa, sừng bò ngà, ba vây sắt, giáp vai hai lớp + gai nón, giáp bụng tròn
  ôm bụng + đai, ổ khoá sắt, móc treo thịt có ngạnh, mắt vàng.
- `tai_ve/L1_B.png` **quỷ xanh than, giáp thép + đồng thau**: mũ chóp nhọn vành đồng, sừng thẳng xiên bịt đồng, ba chóp thép, giáp vai vòm
  không gai, giáp ngực + đai bụng khoá đồng (bụng lộ), vòng đồng, móc liềm, mắt cam.
- `tai_ve/L1_C.png` **quỷ xanh rêu, giáp đồng đỏ kiểu đai thùng**: mũ xô đỉnh bằng, sừng cong ngược như móc, ba móc sắt trên lưng, giáp vai vuông
  + gai móc, ba đai đồng ôm bụng, vòng đồng, móc cẩu công nghiệp, mắt vàng chanh.

Ba ảnh đạt lượt đầu (Codex 150 / 90 / 79 s, phải chờ khoá Codex ~65 phút vì hai phiên khác cùng gen). Độ khớp hình bóng với con gốc A 0,858 /
B 0,856 / C 0,873 (`mau/_so_goc.png`, `quy_xich_da.py so_goc`); lệch ở mũ, sừng, gai (cố ý đổi dáng) và lưỡi móc (cả ba vẽ nhỏ hơn lưỡi liềm
gốc; móc là mảnh cứng trên `bone14b2`, khung nới / thu tự do). Soát: mặt nghiêng phải, hai mắt xếch, miệng cau một nanh; tay xa nắm cán móc mọc
từ sau thân; tay gần thõng, vuốt cạnh hông; cánh, chân, đuôi dính thân; xích treo từ vòng cuối cán thõng xuống đất sang trái; tô phẳng, không
bóng. C: GPT vẽ ~5 đai đồng quanh bụng (dặn 3), nhìn như áo sọc. Trang xem: `inbox/quy_xich_xem_concept.html`. **Người dùng chọn A** (2026-11-16) → `tai_ve/L1_duyet.png`.

## 4. Kế hoạch clip (dự kiến, làm sau khi chốt concept)

| clip | nguồn | ý |
|---|---|---|
| idle | idle_01 | giống họ |
| walk | run_01 | giống họ (xích lê đất) |
| appear | skill_02 đoạn trên không + rơi | từ ngoài trên trái bay vào (cánh vỗ), khựng, rơi thẳng xuống, đáp nảy; `cham_dat` (bụi) |
| attack | skill_02 (bay vọt) + dáng giơ móc qua đầu của skill_01 | bay tới đối thủ theo cung (`move`, game nắn quãng), giơ móc, GÕ xuống đầu đối thủ `trung`, nảy lùi bay về |
| cast | skill_01 | quay xích qua đầu, ném: móc ẩn, code cho móc + xích bay tới `far` (`nem`, `trung`), giật về, móc hiện lại trong tay |
| skill | skill_01 kéo dài | `lua_xich` xích bốc lửa (VFX bám các xương mắt xích) → quay xích lâu hơn, nhanh dần (VFX vệt lửa + khói theo xương móc) → ném `nem` → móc quấn trói đối thủ `troi` (VFX vòng xích quanh đối thủ) → giữ / giật → `cot_lua` CỘT LỬA rất to dưới đối thủ thiêu (VFX hạt chồng lớp, chuẩn `chuan_fx/phun_lua.gif`) → thả, móc về |
| hit | hit_01 | |
| die | die_01 + mờ dần | |

## 5. Mảnh (2026-11-16, `quy_xich_manh.py`; gói `gui_gpt/quy_xich_1/luot_2_*`, Codex đạt lượt đầu cả bốn tờ)

- `can`: căn concept lên hình con gốc bằng phép đồng dạng khớp hình bóng nhất (IoU 0,88; a 1,025, dời −2, +3 px) → `mau/can.json`; mọi
  toạ độ concept ↔ thế giới khung 0 idle đi qua phép này.
- **LIEN** (thân liền, memory khop-noi-gen-lien): bụng + ngực + cổ, hai tay (bắp + cẳng), hai chân (ống + bàn) = năm hình bóng ở dáng gốc,
  tô bằng điểm ảnh concept đã căn, MỖI part chỉ nhận màu thuộc bảng của nó (`BANG`: bụng chỉ giáp / quần, bắp tay chỉ da...; concept lệch
  chỗ nên màu tay, xích, giáp vai của concept rơi vào chỗ rig là bụng), chỗ bị che lấp màu gần nhất (≤ 60 px) hoặc màu mặc định → `mau/lien.png`
  → GPT `tai_ve/N_lien.png` (viền chỉ ở ngoài) → nướng vào khung từng part qua lưới (`cat_lien`).
- **K** (mảnh rời giữ hình bóng gốc): cánh, mặt, giáp vai nhỏ (tinh thể → gai nón sắt), hai giáp cổ, đuôi, hai mắt xích, sáu ngón → tờ =
  mảnh gốc phóng 3–4,6 → `tai_ve/D_K.png`, IoU 0,85–0,95; lỗ mắt xích trong suốt.
- **R1, R2** (mảnh đổi dáng, mảnh cứng một xương, gen "đúng chỗ, đúng cỡ" trên concept): đỉnh mũ + vành đinh (`bone55`, nảy riêng khi trúng
  đòn như con gốc), giáp vai to + gai (`bone26`), ổ khoá (`bone40`), móc (`bone14b2`; bản thứ hai `W_wuqi2` ở đầu xích dài trên `bone14b11`
  đặt theo phép dời giữa hai bản móc của họ) | má mũ trái / phải (`bone12`), sừng to / nhỏ (`bone11`), ba vây lưng. Tách mảnh chạm viền
  nhau bằng LÒNG TÔ (`tach_manh`: mực nâu lum < 50, sắt sẫm lum ~70 vẫn là lòng tô; mỗi điểm viền về lòng tô gần nhất). Ba vây GPT dời chỗ
  → đặt theo part gốc (`THEO_GOC`: đáy + cao như part họ).
- **Chỉnh tay sau khi ghép** (`CHINH`): mắt của mặt rig (hình bóng mặt gốc) cao hơn mắt concept ~25 px; vành mũ đặt theo concept che mất mắt
  → cả cụm mũ (đỉnh, hai má, hai sừng) nâng 30 px; má mũ trái GPT vẽ to lấn che mắt trái → co 0,85, mép phải về x 728. Bài học: mảnh đổi dáng
  đặt theo concept phải soát với nét mặt CỦA RIG (mắt, miệng) trước khi xuất.

## 6. Rig + clip (`quy_xich_rig.py`; `inbox/quy_xich_1/rig/`, không theo git)

128 xương (88 của họ + `move`, `far`, `fly_m`/`moc_t`, 18 cặp `fly_k`/`xich_k`), 93 slot (72 của họ + 8 bản `_sau` + 18 mắt xích bay +
móc bay), 563 đỉnh, NGUYÊN lưới của họ; `.atomik` 337 KB, chiều cao game 665; mọi clip nối về khung 0 idle 0 px. `QX_GOC=1`: dựng bằng da gốc
(`manh_goc/`, chỉ để soi) trùng con gốc.

- **Thứ tự vẽ đổi trong clip**: skill_01 (quay xích, khung 0–21) vẽ móc thứ hai + xích dài SAU tay xa, die_01 / hit_02 / skill_01 khung
  22–37 vẽ TRƯỚC: slot `W_wuqi2`, `W_sB05..07`, `W_sA05/07/08/09` có bản `_sau` trước `P_shouL1`, bật theo thứ tự vẽ của họ từng khung.
- **Xích bay** (cast, skill): mắt k (k = 0..17, hai ảnh mắt xích xen kẽ, trục dài theo +x) trên `xich_k` con của `fly_k`: `fly_k` = w·far,
  `xich_k` = (1 − w)·A (A = vòng cuối cán móc tay `MOC_TRUC`, đo trên ảnh móc), w = (k+1)/18 · q, q = phần quãng móc đã bay. Móc bay `moc_bay`
  trên `moc_t` con của `fly_m` (gốc ở vòng cuối cán, lưỡi chĩa +x). Game (`far`, `farAim` cho cast + skill) co quãng mọi `fly*` tới đối thủ
  thật và xoay mắt xích theo hướng thật (A suy từ xương con / (1 − w)): mắt xích luôn nằm trên đoạn tay → đối thủ ở mọi khoảng cách.
- **Góc liền mạch** (`nuong` riêng): mẫu của họ có chỗ quấn góc; trộn hai dáng quy góc cùng vòng (`pha`); clip lặp không hoà về khung 0 (đuôi
  run_01 quay đều 5 vòng / chu kỳ, +75° / khung: hoà về khung 0 làm khựng rồi nhảy 245°).
- Clip:
  | clip | dài | cách làm | sự kiện |
  |---|---|---|---|
  | idle | 4,00 | idle_01 | |
  | walk | 0,80 | run_01 | |
  | hit | 0,50 | hit_01 (đỉnh mũ nảy) | |
  | die | 1,45 | die_01 + mờ 0,32 s cuối | `nga` 0,55 |
  | attack | 1,42 | skill_02: thu người, bay vọt (độ cao × 0,38), giơ móc qua đầu, BỔ: cú bổ của họ nằm trong hai khung nguồn → giãn 0,62–0,76 (~45° / khung); lao `move` 0,72·1,9 chiều cao (≈ quãng game nắn, khỏi phóng cú nảy về), đỉnh lao lúc bay tới, lúc bổ lùi về 85 % | `bay_len`, `go` 0,70, `trung` 0,775 (lưỡi móc tới đỉnh đầu đối thủ), `cham_dat` 0,76 |
  | appear | 1,75 | dáng bay skill_02 0,36 + cánh vỗ run_01 × 1,6, bay từ ngoài trên trái vào, khựng; rơi: nguồn 0,36 → 0,733 (giơ móc), đáp: 0,733 → 0,80 trong 0,07 s (móc đập đất), đứng dậy; cánh hoà 0,15 s | `go`, `cham_dat` 1,00 |
  | cast | 1,50 | skill_01: quay 0–0,70 (xích dài của họ), ném 0,733, móc + xích bay 0,15 s, găm, giữ, giật 1,07–1,25, móc tay hiện 1,267 | `quay`, `nem`, `trung` 0,895, `rut`, `moc_ve` |
  | skill | 3,23 | skill_01: giơ móc; đoạn vòng khung 8–14 lặp 3 lần (tốc 1; 1,25; 1,55); ném 1,02; trói 1,18 (móc bay ẩn, xích căng giữ, dáng tay duỗi 0,87–0,97 lặp chậm + giật giật); cột lửa 1,58 (giật mạnh); thả 2,68, giật về, móc lắp lại | `lua_xich` 0,10, `quay`, `nem`, `troi`, `trung`, `cot_lua`, `chay` × 4, `tha`, `rut`, `moc_ve` |
- Đo giật (`quy_xich_rig.py kiem`): bước lớn còn lại là mắt xích chạy trên path lật gần 180° lúc vung nhanh (mắt xích lệch tâm 15–29 đơn vị,
  không quy mod 180° được; con gốc cũng vậy) và tay xa / chân (IK) ở đúng khung bổ móc (105–155°, cú vung nhanh của nguồn).
- Soi: `rig/soi_*.png` (bộ vẽ Python), `rig/that/*.jpg` (runtime Spine thật), ảnh động giả lập game `inbox/quy_xich_1/_xem_dong.py` →
  `rig/dong/*.webp`; trang xem `inbox/quy_xich_xem_rig.html`. **CHỜ người dùng xem.**

## 7. Việc tiếp

1. Người dùng xem rig.
2. Hỏi: thay suất `khien_bac` (ải 20)? tên, số dạng (có dạng 2 không)?
3. Vào game: VFX (hạt chồng lớp, chuẩn `chuan_fx/phun_lua.gif`, skill pokiclash-fx-congthuc): lửa bám mắt xích từ `lua_xich` (xương
   `bone14b4..10` xích tay, `bone14b13..19` + `bone14b11` xích dài lúc quay, `xich_k` lúc bay), vệt lửa + khói theo móc quay (`bone14b11`),
   vòng xích quấn đối thủ ở `troi` (tại `far`), CỘT LỬA rất to ở `cot_lua` + nhịp `chay`, bụi đáp (`cham_dat`), vệt bổ móc (`go`); heroes.json,
   menu Unity.

## 8. DẠNG 1 NON (2026-11-16)

Người dùng xem rig: "ok làm dạng 1" → hỏi lại, chọn **"làm thêm dạng 1 non"**: quỷ giáp kín vừa làm là **dạng 2 (dạng cuối)**, làm dạng 1
non trên CÙNG rig, cùng clip. Thư mục `inbox/quy_xich_non/` (`mau`, `tai_ve`, `manh`, `rig`), xuất tên `quy_xich_non`.

- Tỉ lệ trước (`QX_DANG=non py -3 -I ArtGen/Spine/quy_xich_rig.py ...`): `TI_LE` đầu `bone11` × 1,25 (mặt, sừng, mũ là con), cánh `bone27`,
  `bone33` × 0,72, móc tay `bone14b2` × 0,8 (cả xích treo dưới cán; móc bay + mắt xích bay thu theo). Mảnh cứng (moi.json) gắn theo thế giới
  dáng gốc KHÔNG đổi tỉ lệ (`Wc`) để co / phóng cùng xương. Chưa có da non thì dựng bằng da dạng 2. Soi die, cast bằng da dạng 2: ổn.
- Bố cục `mau/bo_cuc.png` (`quy_xich_rig.py bo_cuc`), `mau/bo_cuc_khung.png` (`quy_xich_non.py khung`, 1536 × 1024).
- Concept (`quy_xich_non.py concept` → `gui_gpt/quy_xich_non/luot_1_concept_<A|B|C>.txt`, ảnh mẫu 1 = bố cục, 2 = concept dạng 2): giữ da
  đỏ, mắt vàng xếch, nanh, cánh dơi, đuôi, móc nối xích; bỏ giáp nặng, bụng để trần:
  - A **đội nồi sắt** (quai một bên, sừng con nhú qua lỗ), vạt da nhỏ ở vai, dây thừng ở eo, vòng sắt thay ổ khoá, móc nhỏ gỉ, ba u sắt sau lưng;
  - B **mũ da tai bèo** viền sắt, giáp vai da một đinh, thắt lưng da khoá vuông, ủng da, móc nhỏ cong, ba gai da;
  - C **giáp vụn quá cỡ**: mũ xô lệch, nắp nồi làm giáp vai, miếng giáp ngực nhỏ buộc dây, móc lưỡi câu, ba đinh sắt cong.
- Lần gen đầu (13:5x) Codex báo hết hạn mức gói ChatGPT ("try again at 2:00 PM"); đặt chạy lại lúc 14:01.
- Lần hai (14:01) ra đủ A, B, C. **Người dùng chọn A** (đội nồi sắt) → `quy_xich_non/tai_ve/L1_duyet.png`; khớp bố cục 0,854 (lệch ở đỉnh: bố cục
  còn mũ + sừng dạng 2).
- Mảnh (`quy_xich_non_manh.py`, dùng lại hàm của `quy_xich_manh.py`; Codex đạt lượt đầu cả ba tờ): phép căn theo bố cục rig non (tinh chỉnh bằng
  hình bóng phần thân dưới y 420); hình bóng part ở dáng gốc NON (đỉnh lưới gốc qua xương đã đổi tỉ lệ). Tờ thân liền (bụng trần có rốn, dây
  thừng, quần nâu; tay trơn; bàn chân có vuốt) → nướng vào part. Mảnh đổi dáng R1 (nồi có quai, vạt da vai, vòng sắt, móc gỉ), R2 (hai sừng con).
  Dùng lại từ dạng 2: cánh, mặt, đuôi, sáu ngón, hai mắt xích. Rig non bỏ slot: hai má mũ, ba vây, giáp vai nhỏ, hai giáp cổ (`AN_NON`).
- Sửa sau ghép (`sua_noi`): GPT vẽ cả LÒNG NỒI tối dưới vành → che mắt (mắt rig non ở y 378–408 px concept, ngay dưới vành) → cắt dưới mép dải
  vành (vùng sáng liền rộng nhất, mép dưới làm trơn qua 25 cột; dò từng cột thì vân sáp làm răng cưa); lấp hai lỗ sừng, cả hai sừng đặt SAU nồi
  (slot `P_jiaoR1` dời lên trước `P_toukui2`), nhô lên khỏi đỉnh nồi.
- Rig non: 128 xương, 85 slot, 519 đỉnh, `.atomik` 298 KB, mọi clip nối về khung 0 idle 0 px; đo giật như dạng 2. Runtime thật `quy_xich_non/rig/that/`,
  ảnh động `QX_DANG=non ... inbox/quy_xich_1/_xem_dong.py` → `quy_xich_non/rig/dong/`; trang xem `inbox/quy_xich_non_xem_rig.html`. **CHỜ người dùng xem.**

## 9. VÀO GAME (2026-11-16, người dùng xem dạng non: "ổn rồi, cho vào game")

Thay HÌNH suất 5 đảo Kim (`khien_bac`, ải 20 "Gác Chuông Đồng"); giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, số dạng (2 → 2): bản lưu và golden
không đổi (golden chỉ ghi id + số dạng; chữ thẻ sinh từ hiệu ứng).
- `ArtGen/Spine/quai/doi_quy_xich.py` (mẫu `doi_tinh_sat.py`): `heroes.json` (Quỷ Xích, "Quỷ béo móc xích lửa", "Dòng Quỷ Xích"; dạng Quỷ Xích Nhi
  `quy_xich_1` 0,92 / Quỷ Xích `quy_xich_2` 1,1), `cards.json` (Ném Móc Xích claw / Xích Lửa Thiêu flame / Bụng Thép fist). Tên Claude đặt,
  người dùng có thể đổi. `th`: gộp bản nhẹ dạng 2 + clip `evolve` vào rig dạng 1 → `quy_xich_non_th.atomik` (389 KB; khung cuối trùng khung 0
  idle dạng 2). `chep`: Resources/quy_xich_1 (rig dạng 1 có tiến hóa + chân dung), Resources/quy_xich_2 (rig dạng 2 + chân dung + hai ảnh mắt xích
  `quy_xich_2_tt_xich_<1|2>.png`, tên có `_tt_` để AolaImport nhập thành sprite). Thư mục Resources/khien_bac_* cũ giữ nguyên.
- Hiệu ứng `Assets/01 Script/Game/Battle/HatXich.cs` (SINH bằng `ArtGen/Spine/quy_xich_hat_cs.py` = khung C# + bảng đo `quy_xich_do_hat.py` hai
  dạng: tâm lưỡi móc khi quay, ba điểm giữa xích dài, chỗ xích nối tay; theo khung 30 / giây, phần của chiều cao khai cho game):
  `n_xich_go` (đòn thường, thêm vào `HatLua.AtkLao`), `n_xich_nem1/n_xich_nem` (mana), `n_xich_lua1/n_xich_lua` (chiêu cuối: móc bốc lửa, vệt
  lửa + khói theo đường móc quay, lửa chạy dọc xích lúc ném, vòng xích quấn đối thủ nóng đỏ dần, cột lửa rất to (cao tới gần mép trên màn,
  tối đa 2,4 thân), bốn nhịp đốt, thả: vòng xích rơi, lửa tắt theo xích rút). Bảng: `StageView.KimFx` / `KimAtk`, `HatNuoc.PlayNuoc`, `HatLua.Themes`.
  Tour `PokiClash/Thử/Đảo Kim: riêng Quỷ Xích (dạng 2) / Quỷ Xích Nhi (dạng 1) ...` (`Editor/KimFxTour.cs`).
- Unity: biên dịch sạch (PokiClash.Game.dll 14:40:55, 0 lỗi), "Nhập dữ liệu" (HeroDb / CardDb có Quỷ Xích), "Gắn dạng .atomik vào prefab tướng"
  (khien_bac: prefab giữ 2 dạng quy_xich_1, quy_xich_2). CHƯA soi trong trận: lúc chạy tour Editor kẹt ở "đang chuyển Play" (phiên khác đang dùng
  Play cho tour đảo Kim), tour không chạy. Ảnh mắt xích đổi tên `_tt_` SAU lần biên dịch / nhập đó: cần refresh lại khi Editor rảnh.
- Soi trong trận (tour KimFxTour, 2026-11-16 ~15:05, sau khi người dùng thoát Play cho Editor rảnh; tour chỉ chạy được khi cửa sổ Unity ở trên cùng):
  hai dạng đủ đòn thường / mana / chiêu cuối (`Temp/PokiShots/kim_fx/khien_bac_<1|5>sao_*`; tờ ghép `inbox/quy_xich_1/trong_tran/`, trang
  `inbox/quy_xich_trong_tran.html`). Đúng như thiết kế: vệt lửa + khói theo móc quay, lửa dọc xích lúc ném, vòng xích quấn đối thủ, cột lửa vọt khỏi
  mép trên màn, chớp sắt ở đỉnh đầu (đòn thường), móc găm + vòng sóng (mana). Lỗi: lúc thả, mắt xích của vòng trói rơi tự do xuống tận chân Quỷ Xích
  → sửa (`ground` = mặt đất dưới chân đối thủ, nảy 0,25 rồi nằm yên, chỉ xoay lúc rơi); đã biên dịch 15:12:55, CHƯA chụp lại (lần chạy lại
  15:19 Play bị tắt giữa tour; bản lưu trên đĩa không bị đụng).
- Chụp lại 15:27 (tour dạng 2): lúc thả, mắt xích rơi xuống ngay chân đối thủ rồi mờ; cột lửa tắt dần, khói bốc. ĐẠT.
