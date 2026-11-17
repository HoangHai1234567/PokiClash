# Thú giáp pháo (`thu_phao`): tướng 9 đảo Kim

Bắt đầu 2026-11-16 tối (máy ổ D, kho `D:\RefAnimation\SwordxStaff`). Con gốc của rig: **`monster_3629`** (thú đá lục bốn chân thấp như rùa,
quay PHẢI, giáp khối hoa văn xoắn, đầu khối nhỏ hai tai vây cao ở dưới bên phải, bốn khối đá tròn cuộn xuống ở sau làm đuôi, trên lưng khẩu
pháo khối dài có lõi tròn sáng ở đuôi pháo, hai móc nâu, khối họng vuông có ô cửa vòm sáng ở trên đầu, chĩa tới trước; game tham khảo),
**do người dùng chỉ** (ảnh chụp trang xem, clip `idle_01`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ,
không đăng công khai. Hình là của mình. Suất 9 đảo Kim = ải 60 "Tổ Cánh Pha Lê" (`IslandGen.cs` Plan Kim), id game hiện là **`ung_thep`**
(Ưng Thép, 2 dạng). Mã làm việc `thu_phao`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-16)

- "làm tướng thứ 9 đảo kim; concept **quái thú mặc kín giáp, đuôi là 1 khẩu pháo to**".
- appear: "tôi chưa nghĩ ra gì, bạn có thể **sáng tạo 1 animation độc đáo**".
- idle / walk: "**làm giống họ**".
- Đánh thường: "làm **giống skill_01, bắn 1 quả đạn sắt gây nổ**".
- Chiêu mana: "làm **giống skill_03, bắn nhiều quả đạn pháo lên trời, các quả đó tách ra thành các tên lửa nhỏ homing missile** tấn công mục
  tiêu".
- Chiêu cuối: "quái vật **gồng người, tụ 1 quả cầu năng lượng rất lớn ở họng súng rồi bắn vào địch, gây giật**, giống skill_04_1 nhưng **epic
  hơn và impact hơn**".
- die: "tùy bạn làm".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3629/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample_goc.json` 13 clip 30 khung/giây,
`khung/` tờ khung từng clip, `mo/` tờ mổ + `nhom_idle0.jpg`; script `thu_phao.py`)

120 xương, 93 slot (88 hình bật ở idle 0), 13 clip, 10 005 khoá. Ràng buộc: **8 IK** cho bốn CHÂN (`SR1`/`SR2` chân trước gần `bone9/10` →
bàn `bone11`; `SL1`/`SL2` chân trước xa `bone13/14` → `bone15`; `R1`/`R2` chân sau gần `bone17/18` → `bone44`; `L1`/`L2` chân sau xa
`bone21/22` → `bone23`; đích là con của `bone2`, mix của IK thứ hai = 0); **2 transform**: `bone99` (gốc pháo, con của `bone`) theo góc
`bone4` (thân), `bone26` theo vị trí. Không path, physics. Thứ tự vẽ KHÔNG đổi, trừ die_01 (`P_shenti02` có hai chỗ). Đổi hình chỉ ở die_01
(vài mảnh chân xa). Ảnh mẫu `inbox/thu_phao_1/mau/goc_ca_con.png` 1536 × 1024: 0,807 px / đơn vị.

Cây xương: `root → bone2 → bone → bone3 → bone4` (THÂN, trục từ đuôi x −367 tới trước); `bone4 → bone6 → bone7 → bone27 → bone28` (cổ → ĐẦU:
`bone33` `P_tou02`, `bone34` `P_tou00`, `bone29` `P_tou01`, tai `bone36` `P_erduo00`, `bone37` `P_erduo01`); bốn chân `bone8/12/16/20` → chuỗi
IK + các khối giáp chân (`bone58..64`, `bone91..96`, `bone45..51`, `bone73..78`, mảnh thêm `bone100..105`); tấm giáp thân `bone65..72` (một xương
mỗi tấm). `bone → bone24 → bone25 → bone26` (chuỗi ĐUÔI) + bốn khối đuôi `bone31`, `bone32`, `bone35`, `bone38`. `bone → bone99 → bone30` (PHÁO,
L 321) → `bone97` (NÒNG thò ra / thụt vào: dời x 305 → 568 ở skill_04_1) → `bone119/120/121` (mặt trước khối họng); `bone30 → bone98` (móc
trước), `bone118/122/123` (điểm trên thân pháo).

| nhóm | slot (thứ tự vẽ) | là gì |
|---|---|---|
| pháo | `P_pao09` (2), `P_pao00` (15) | hai móc nâu trên thân pháo (148 × 131) |
| đuôi | `P_pao08` (3, khối tối 4 xương sau đuôi), `P_pao07..04` (4–7) | bốn khối đá tròn cuộn xuống làm đuôi |
| pháo | `P_pao01_5/4/3` (8–10) | mẩu nhỏ trên thân pháo |
| pháo | `P_pao01_2` (11, 304 × 229) | KHỐI HỌNG + ô cửa vòm sáng; lưới 9 đỉnh: mặt trước bám `bone119–121` (theo nòng), mặt sau bám `bone30` → GIÃN khi nòng thò |
| pháo | `P_pao03` (12), `P_pao02` (13, lõi tròn sáng), `P_pao01_1` (14, 394 × 208, thân pháo khối dài) | |
| chân sau xa | `P_z_houtui00..12` (16–28) | khối giáp + ngón |
| chân trước xa | `P_z_qiantui00..13` (29–42) | |
| thân | `P_shenti09..00` (43–55), `P_bozi*` (45–47, cổ) | các tấm giáp mai, cổ |
| chân sau gần | `P_y_houtui00..15` (56–71) | `P_y_houtui15` bản thứ hai trên `bone105` (ẩn) |
| chân trước gần | `P_y_qiantui00..15` (72–87) | `P_y_qiantui15` bản thứ hai trên `bone104` (ẩn) |
| đầu | `P_erduo01` (88), `P_tou02/01/00` (89–91), `P_erduo00` (92) | đầu khối nhỏ KHÔNG có mắt, hai tai vây |

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho |
|---|---|---|---|
| `idle_01` | 6,00 | thở; chu kỳ 2,0 s lặp hai lần + biến tấu 4–6 s | **idle** (chu kỳ 2 s) |
| `run_01` | 1,33 | bước | **walk** |
| `skill_01` | 1,00 | nâng nòng (0 → 0,33, +33°), bắn ~0,37 (nòng giật nhẹ), hạ | nguồn **attack** |
| `skill_02` | 1,17 | nòng dựng gần đứng (+52 → 66°), bắn, hạ | (dự phòng) |
| `skill_03` | 2,17 | nòng chĩa trời (+45 → 50°), cú thò nòng 0,40, ba cú giật ~0,97 / 1,12 / 1,52, hạ 1,53 → 2,17 | nguồn **cast** |
| `skill_04_1` | 2,67 | thủ thế (0 → 0,27), nòng THÒ DÀI ra (0,33 → 0,73), giữ, BẮN 1,40 (nòng bật về, cả con trượt lùi 151 qua `bone2`), giữ, trượt về 2,0 → 2,67 | nguồn **chiêu cuối** |
| `skill_04_2/3` | 2,67 | biến thể | |
| `die_01` | 1,00 | nòng hất lên, giáp vỡ bắn mảnh (0,56–0,78), đổ sụp thành đống | **die** |
| `hit_01/02`, `block_01`, `stun_01` | | | **hit** = hit_01 |

## 3. Concept lượt 1 (Claude đề xuất ba hướng; người dùng chọn C)

Gói `gui_gpt/thu_phao_1/` (`thu_phao_da.py ca_con`, `concept`; mô tả từng mảnh và ba hướng ở `thu_phao_huong.py`). Ảnh mẫu 1 = hình cả con gốc
`mau/goc_ca_con.png` (khung 0 idle); ảnh 2 = sói giáp sắt (tướng 6 đảo Kim: nét, tô kim loại phẳng); ảnh 3 = robot cổ (tướng 7: đinh tán, đai,
ô tròn, mắt sáng). Mọi hướng giữ dáng và chỗ, cỡ từng mảnh; đổi chất liệu đá → kim loại, bỏ hoa văn xoắn; đổi dáng đầu (thêm mắt), tai, họng
pháo (khối vuông → họng tròn), lõi, móc, đốt đuôi:
- `tai_ve/L1_A.png` **thép xám lam + đồng thau, lõi điện lam** (Claude đề xuất: màu điện hợp chiêu cuối gây giật; nòng tròn đọc ra pháo ngay;
  khác các tướng Kim trước đều sắt sẫm viền vàng): mũ giáp heo rừng hai mắt lam xếch, hai sừng lưỡi thép, nòng tròn hai đai đồng, họng loe
  vành đồng lòng lam, lõi ô cửa đồng, hai tay cầm chữ C, bốn đốt đuôi viền đồng.
- `tai_ve/L1_B.png` **sắt đen rèn + đồng đỏ, lõi lửa lò cam**: mũ tê giác một sừng mũi, nòng ba đai đồng đỏ đinh to, họng răng cưa, cửa lò có
  song, ống khói, hai vây tản nhiệt, đốt đuôi có gai tù.
- `tai_ve/L1_C.png` **thép bạc trắng + vàng kim, lõi vàng**: mũ hiệp sĩ khe chữ T, tai giáp dựng, thân pháo khối giữ dáng hộp, họng tròn có
  cánh vàng, lõi mặt trời, hai cánh vàng thay móc, vảy đuôi viền vàng.

Codex đạt lượt đầu cả ba (khoảng 2 phút mỗi ảnh). Khớp hình bóng con gốc (`thu_phao_da.py so_goc` → `mau/_so_goc.png`): A 0,932, B 0,915,
C 0,925. A và B vẽ nòng TRÒN thay khối hộp (mảnh nhận diện, đổi dáng có chủ ý), C giữ dáng hộp.

## 4. Kế hoạch clip (rig thử bằng DA GỐC đã dựng: `TP_GOC=1 thu_phao_rig.py` → `inbox/thu_phao_1/rig_goc/`, chưa xuất, chỉ soi)

| clip | nguồn | ý |
|---|---|---|
| idle | idle_01 (chu kỳ 2 s) | giống họ |
| walk | run_01 | giống họ |
| attack 1,15 s | skill_01 | nâng nòng, ngắm, `ban` 0,44 (nòng thụt mạnh 75 vào vỏ, hất +7°, thân lùi), đạn sắt do code bay từ `mieng`, `trung` 0,72, nổ |
| cast 2,25 s | skill_03 | nòng chĩa trời + `nap` 0,42, BẮN LIỀN 5 QUẢ (`ban` 0,62 / 0,80 / 0,98 / 1,16 / 1,34, mỗi quả một cú giật), hạ nòng; code cho đạn vọt khỏi màn, tách thành tên lửa nhỏ homing lao xuống, `trung` 2,00 |
| skill 3,55 s | skill_04_1 kéo dài | thủ thế, nòng thò dài, `gong` 0,85: thân lún dần + rung tăng dần, nòng vươn thêm, cầu năng lượng lớn dần ở `mieng` (VFX), `day` 2,05, `ban` 2,25: nòng bật về, nòng hất +9°, cả con trượt lùi (họ), rung tắt dần, `trung` 2,47 (giật điện), trượt về |
| appear 1,75 s | Claude tự đặt | "thả quân": rơi từ 0,8 chiều cao, nòng chĩa trời; `cham_dat` 0,30 dộng đất, nhún theo dáng thủ thế; nòng hạ xuống vượt nhẹ rồi `khoa` 0,98 (cạch); nòng thụt thử `xa_khoi` 1,16 (họng xì khói), `loi_sang` |
| hit | hit_01 | |
| die 1,55 s | die_01 + mờ | `vo` 0,48 giáp vỡ, `tat_loi` 0,62, `nga` 0,86 |

Đo góc nhảy (`thu_phao_rig.py kiem`, da gốc): die có mảnh bay quay nhanh (của họ, 118–179° / khung); skill chân sau xa 65–75° ở khung bắn (cả con
trượt lùi trong một khung của họ) → soi kỹ khi có da mình.

**Người dùng chọn C** (2026-11-17) → `tai_ve/L1_duyet.png`. Trang so `inbox/thu_phao_xem_concept.html`.

## 5. Mảnh (`thu_phao_manh.py`; gói `gui_gpt/thu_phao_1/luot_2_*`; Codex đạt lượt đầu cả 8 tờ, 68–102 s mỗi tờ)

- `can`: căn concept C lên hình con gốc (IoU 0,951; a 1,025, dời −5, −3 px) → `mau/can.json`.
- **K1–K6** giữ hình bóng gốc (tờ = mảnh gốc cắt theo lưới phóng 1,6–4; bỏ hoa văn xoắn, tô bạc mặt trước / bạc sẫm mặt bên, viền vàng mép
  dưới): K1 đai sống lưng + bốn tấm mai | K2 bụng tối, khối tối dưới ngực, khối sau gáy `P_tou02`, ba khúc cổ | K3 chân trước gần + xa | K4 chân
  sau gần + xa | K5 24 ngón (vuốt vàng sẫm) | K6 bốn vảy đuôi, khối tối sau đuôi, mặt dưới pháo. 76 part, chỉ `P_z_qiantui02` 0,894, còn lại
  ≥ 0,9. NGUYÊN lưới của họ.
- **R1, R2** đổi dáng, gen đúng chỗ đúng cỡ trên concept, mảnh cứng một xương (`manh/moi.json`): mũ (cả đầu, mắt vàng trong khe chữ T) thay
  `P_tou00` trên `bone34` (khối đỉnh đầu `P_tou01` bỏ); thân pháo hộp trọn thay `P_pao01_1` (`bone30`); họng tròn có cánh thay `P_pao01_2`
  (`bone97`); lõi mặt trời thay `P_pao02` (`bone30`); hai cánh vàng thay hai móc (`P_pao00` `bone98`, `P_pao09` `bone30`); hai tai giáp
  (`P_erduo00` gần / trái `bone36`, `P_erduo01` xa / phải `bone37`). Ba mẩu nhỏ trên thân pháo của họ (`P_pao01_3/4/5`) bỏ.
- **Ống nòng** (`nong`, vẽ ở góc trống tờ R2): cứng trên `bone97`, trục x của xương nòng, đầu trước lùi 70 sau tâm họng, dài 470, dày nửa
  chiều cao vành họng (198); nấp sau thân pháo ở dáng nghỉ, thò ra khi nòng vươn (chiêu cuối +230). Thứ tự vẽ: ống nòng ở chỗ cũ của họng (sau
  thân pháo), họng + lõi dời ra SAU thân pháo (vẽ đè như concept). `_mieng` = tâm vùng vàng trong họng, `_loi` = tâm lõi.

## 6. Rig da mình (`thu_phao_rig.py` → `inbox/thu_phao_1/rig/`, không theo git)

123 xương, 88 slot, 536 đỉnh, 8 clip, 20 sự kiện, `.atomik` 394 KB (ảnh mảnh 0,6 px / đơn vị), chiều cao 987; mọi clip nối về khung 0 idle 0 px,
appear khung đầu trống; walk khép vòng 44 px = cỡ một bước thường (của họ, không giật). Trang xem `rig/xem.html` chạy đủ 8 clip. Soi `rig/soi_*.png`:
dáng nghỉ khớp concept, nòng chĩa trời (cast), nòng thò dài lộ ống nòng (skill), die giáp vỡ đổ sụp. **CHỜ người dùng xem.**

### 6b. Pháo làm lại theo khung part (người dùng 2026-11-17: "phần súng nhìn 2D quá, bề rộng họng súng không khớp với miệng súng, sửa lại kĩ")

Bản R (thân pháo hộp vẽ lại nhìn NGANG phẳng, vòng họng tròn to gắn rời phía trước, ống nòng tự chế) bỏ: concept C vẽ pháo nhìn ngang còn con gốc
dựng pháo theo phối cảnh BA PHẦN TƯ (thân hộp có mặt trên dốc + bậc nhô + sàn; khối họng = mặt bên dài của nòng + khung mặt trước chứa miệng).
Tờ **K7** (`thu_phao_manh.py`, `MO_TA_PHAO`): `P_pao01_1`, `P_pao01_2`, `P_pao02`, `P_pao01_3/4/5` giữ hình bóng + đường cấu trúc của họ, chỉ đổi
da: mặt trên bạc sáng, mặt bên bạc sẫm, mặt quay xuống xám; gờ vàng; núm tròn vàng thay hoa văn xoắn trên bậc nhô; khung mặt trước họng thành
khung vàng dày, miệng giữ đúng chỗ / dáng / cỡ vòm sáng của họ (lòng sáng vàng hai tông); lõi = vòng vàng có bề dày, mặt trời trong. IoU 0,89–0,98
(Codex lượt đầu). Rig: NGUYÊN lưới + thứ tự vẽ của họ cho pháo (mặt bên khối họng tự giãn khi nòng vươn, không cần ống nòng); `BO_R` trong
`thu_phao_manh.py` bỏ bốn mảnh R cũ khỏi `moi.json`; `_mieng` về lại tâm vòm sáng của họ (`MIENG_PX`). Hai cánh vàng (R2) giữ. `.atomik` 397 KB.
**CHỜ người dùng xem lại.**

## 7. Việc tiếp

1. Người dùng xem rig, sửa clip theo ý.
2. Hỏi: thay suất `ung_thep` (ải 60)? tên, số dạng?
3. Vào game: VFX (đạn sắt nổ, 5 quả lên trời tách tên lửa homing, cầu năng lượng điện gây giật, bụi dộng đất, khói họng appear, mảnh giáp die),
   heroes.json, menu Unity; dạng 1.

## 8. Dạng 1 non (bắt đầu 2026-11-17; người dùng: "ok làm dạng 1 cho tướng này")

Bản giáp bạc mũ hiệp sĩ vừa làm là **dạng 2** (dạng cuối). Dạng 1 trên CÙNG rig, cùng clip (`TP_DANG=non thu_phao_rig.py`, mẫu ky_nguyen_rig):
- Tỉ lệ (`TI_LE`, biến `TP_DAU / TP_TAI / TP_PHAO / TP_DUOI`): đầu `bone28` × 1,45 (mũ + hai tai theo), hai tai `bone36/37` × 0,8 (tổng ≈ 1,16), pháo
  `bone99` × 0,78 (thân, họng, lõi, cánh theo), chuỗi đuôi `bone24` × 0,85. **Chân giữ**: bàn chân là đích IK dưới `bone2`, thu chân thì hở ống
  với bàn. Mảnh cứng (moi.json) gắn theo thế giới KHÔNG đổi tỉ lệ (`Wc`) nên co / phóng cùng xương; `mieng`, `loi` tính trong `Wc`.
- Soi bằng da dạng 2 ở walk / skill / cast / die / hit (`inbox/thu_phao_non/rig/_soi_ti_le.png`): ổn.
- Bố cục `inbox/thu_phao_non/mau/bo_cuc.png` (+ `bo_cuc_khung.png` 1536 × 1024).
- Concept (`thu_phao_non.py concept` → `gui_gpt/thu_phao_non/luot_1_concept_<A|B|C>.txt`; ảnh mẫu 1 = bố cục, 2 = concept dạng 2; dặn GIỮ pháo ba
  phần tư của ảnh 1, không chép pháo phẳng của ảnh 2). Codex đạt lượt đầu (75–84 s), khớp bố cục: A 0,950 / B 0,943 / C 0,927. Trang
  `inbox/thu_phao_non_xem_concept.html`.
  - A **thú con giáp bạc nhẹ** (Claude đề xuất): mũ tròn hở mặt lộ mặt thú con (da xanh xám, mắt tròn to vàng, mõm nhỏ), tai thú ngắn viền vàng,
    giáp bớt tấm; GPT vẽ chân thành các khúc tròn trơn (ít khối hơn bố cục).
  - B **đồng thau học việc**: mũ tròn kín một khe mắt, hai núm sừng đồng, giáp đồng thau + khớp thép, giữ khối chân.
  - C **giáp gỗ đai sắt**: mũ thùng gỗ hai lỗ mắt, chốt gỗ thay tai, pháo gỗ đóng đai, khung họng sắt.
  **CHỜ người dùng chọn.** Sau đó: chuyển da tờ K1–K7 (tờ = mảnh dạng 2 đã xong) + mũ / tai / cánh gen lại đúng chỗ trên concept dạng 1.

### 8b. Lượt 1b: sửa đầu bản A (người dùng: "A ổn nhưng cái đầu nhìn không liên quan gì đến dạng 2, sửa lại đi")

`thu_phao_non.py dau` → `gui_gpt/thu_phao_non/luot_1b_dau_<1|2|3>.txt` (ảnh mẫu 1 = bản A, giữ y nguyên trừ đầu + tai; ảnh 2 = dạng 2 lấy kiểu mũ):
`tai_ve/L2_1.png` + `L2_1_2.png` (kiểu 1 mũ hiệp sĩ non khép, khe chữ T rộng lộ mắt; hai lượt gen: lệnh xếp hàng cũ chạy xong trước khi bị dừng),
`L2_2.png` (mũ dạng 2 mở tấm che, lộ mặt thú con), `L2_3.png` (mũ khoét chữ T, mặt thú nhìn qua). Khớp bản A 0,983–0,990. Cận đầu
`mau/_dau_can.png`, trang `inbox/thu_phao_non_xem_dau.html`. Claude đề xuất **1b** (gần mũ dạng 2 nhất). CHỜ chọn. Khoá Codex bị phiên khác
(`vua_may_1`) giữ liên tục → lượt này gọi thẳng `ArtGen/Heroes/tools/gen_codex.py` (bỏ qua khoá gen.py, chạy song song 2 lệnh Codex).

### 8c. Mảnh dạng 1 (người dùng chọn 1b → `thu_phao_non/tai_ve/L1_duyet.png`)

`thu_phao_non_manh.py` (dùng lại hàm của `thu_phao_manh.py`): `can` concept dạng 1 ↔ khung bố cục (IoU 0,947) → `phep_can` thế giới rig non ↔ px
concept (bố cục `box` × `scale` × `k` + lệch); `chep` 38 mảnh dạng 2 dùng lại (K5 ngón, K6 đuôi, K7 pháo, hai cánh với `"he": "lon"`);
`to` 4 tờ CHUYỂN DA (tờ = mảnh dạng 2 đặt đúng ô tờ K; bỏ đinh, viền vàng mảnh một nửa) + tờ R1 (mũ 1b cả đầu, tai gần, tai xa, đúng chỗ trên
concept dạng 1, toạ độ thế giới non); `cat` (K1–K4 bằng `thu_phao_manh.cat_k`, R1 → moi.json không "he").

### 8d. Rig dạng 1 (`TP_DANG=non thu_phao_rig.py` → `inbox/thu_phao_non/rig/`, không theo git)

Cắt: 46 mảnh chuyển da K1–K4 đều IoU ≥ 0,9. Tờ R1 (mũ + tai) Codex vẽ đúng mũ nhưng hai tai bè hai bên hông → chỉ lấy MŨ từ R1 (lần đầu mắt phải
và chỏm vàng bị `tach_manh` gán sang tai vì tâm tai đặt sát: dời tâm tai ra đúng chỗ tai trên tờ: mu (1030, 730), tai (795, 680) / (1165, 650));
hai tai gen riêng tờ R2 (chỉ hai tai, dặn toạ độ, hướng, nối dài chân khuất sau mũ). Rig: 123 xương, 90 slot, `.atomik` 393 KB, 8 clip, mọi clip
nối về khung 0 idle 0 px; trang `rig/xem.html` chạy đủ; so concept `rig/_soi_non.png`. **CHỜ người dùng xem.** Còn: clip `evolve` (gộp dạng 2 bản
nhẹ) khi vào game; khối mai của rig giữ đường tấm của họ (concept A vẽ mai trơn hai vạch vàng).

## 9. Vào game (2026-11-17; người dùng: "cho vao game di")

- **Dữ liệu** `quai/doi_thu_phao.py` (dùng hàm `doi_phap_lua.py`): suất `ung_thep` giữ id, thẻ, chỉ số, hiệu ứng thẻ, SỐ DẠNG 2. Tên tạm do Claude đặt:
  **Pháo Giáp** ("Thú giáp pháo công thành", "Dòng Pháo Giáp"); dạng **Pháo Giáp Nhi** (`thu_phao_1`, cỡ 0,92) / **Pháo Giáp** (`thu_phao_2`, 1,1); thẻ
  Lông Pha Lê → **Pháo Tán Hỏa Tiễn** (crack), Săn Trời → **Lôi Pháo Đại Cầu** (bolt), Cánh Gió → **Giáp Hiệp Sĩ** (helmet). `th` gộp dạng 2 (atlas × 0,5)
  + clip `evolve` vào rig dạng 1 → `thu_phao_non_th.atomik` 501 KB (khung cuối evolve khớp idle dạng 2 lệch 0); `chep` → `Resources/thu_phao_1|2`.
  Resources `ung_thep_*` cũ để nguyên.
- **VFX** `Assets/01 Script/Game/Battle/HatPhao.cs` (dùng lại hạt của HatRobot.cs + tia sét `Set()` của HatRong.cs), bảng `HatPhaoBang.cs` SINH bằng
  `ArtGen/Spine/thu_phao_do_hat.py` (họng pháo `mieng` + hướng nòng bone97 + lõi, 30 khung/giây, cả hai dạng): `n_phao_ban1|n_phao_ban` (đạn sắt vòng
  cung, nổ lửa), `n_phao_mua1|n_phao_mua` (5 quả lên trời, tách 2 / 3 tên lửa nhỏ homing), `n_phao_cau1|n_phao_cau` (gồng tụ cầu năng lượng vàng, sét
  lách tách, bắn, nổ rất lớn, giật điện ~0,9 s). Đăng ký: StageView `KimFx["ung_thep"]`, `AtkDang["ung_thep"]`, HatNuoc 6 case, HatLua
  `Themes["ung_thep"]` (pal "nang"), KimFxTour hai menu Pháo Giáp / Pháo Giáp Nhi. Kiểm biên dịch ngoài Unity bằng dotnet (Game + Editor): qua.
- **Unity**: CHỜ cầu MCP (instance 0: người dùng bấm Window > MCP for Unity > Start Session); assets-af đã nhường lượt.
