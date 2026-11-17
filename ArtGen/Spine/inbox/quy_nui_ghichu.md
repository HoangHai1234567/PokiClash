# Vượn núi đá bốn tay (`quy_nui`): tướng 5 đảo Thổ (ải 20)

Bắt đầu 2026-11-17 (máy ổ C, kho `D:\Ripper\SwordxStaff`). Con gốc của rig: `monster_3612` (golem bốn tay nhìn thẳng, một mắt, hai sừng, tay
phụ máy; game tham khảo), Claude chọn, người dùng duyệt. Concept: hướng C (`quy_nui_1/tai_ve/L1_duyet.png`): vượn núi bằng đá bốn tay, mặt khỉ
đột hai mắt hổ phách, vương miện ba gai đá, thân tảng đá tròn hoa cương, mạch pha lê hổ phách chéo ngực, nắm đấm to, tay phụ vuốt đá, khố da.
Đề xuất animation ở `tho5_anim.py`; người dùng: "làm đi", "chia multiagent làm cùng lúc đi" (agent riêng làm con này). Xương, lưới, chuyển
động gốc là của nhà phát hành game đó: dùng nội bộ, không đăng công khai. Hình là của mình. Ghi chú chung năm con: `tho5_ghichu.md`.

## 1. Mổ rig gốc (`<SXS>/scan/monster_3612/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample_goc.json` 12 clip 30 khung/giây,
`khung/`, `khung5/` tờ khung đọc được)

81 xương, 52 slot (mọi slot là lưới có trọng số, đều bám `root`), 12 clip. Ràng buộc: **8 IK** (chân `R1/R2` trên `bone2/bone3` + `bone4`,
`L1/L2` trên `bone5/bone6` + `bone7`; tay trước `SL1/SL2` trên `bone16/bone17` + `bone18` (nắm đấm nửa phải tranh), `SR1/SR2` trên
`bone20/bone21` + `bone22`). IK đã được runtime nướng vào biến đổi riêng `l` của mẫu khung → rig của mình FK thuần, bỏ 8 xương đích + shadow.

Cây: `root → bone56 → bone55 → bone` (hông) `→ bone11 → bone12` (ngực) `→ bone13 → bone14` (đầu). Tay trước nửa trái tranh (slot `shouR*`):
`bone12 → bone19 → bone20` (vai) `→ bone21` (cẳng) `→ bone22` (nắm đấm), `bone65` (tảng vai trên); nửa phải (`shouL*`): `bone15 → bone16 →
bone17 → bone18`, `bone66`. Tay phụ nửa trái (`jixieshouR*`): `bone33 → bone34` (bắp) `→ bone35 → bone36` (lòng bàn tay) + ba ngón hai đốt
`bone37/38, 39/40, 41/42`; nửa phải: `bone23 → bone24 → bone25 → bone26` + `bone27..32`. Chân: `bone → bone2 → bone3 → bone4`, `bone5 → bone6
→ bone7`. Khố `weiqun` bám `bone57..60, 67..70`; bốn dải `piaodai1..4`; đuôi `weiba1/2` + `jiapian` bám `bone8..10`.

Thứ tự vẽ của họ: tay phụ phải → tay phụ trái → tay trước nửa PHẢI tranh (SAU thân) → chân phải → đuôi → hông → chân trái → khố → thân
(`shenti2`) → cổ / ngực → tay trước nửa TRÁI tranh (TRƯỚC thân) → đầu (`tou`) → nắm đấm trái.

Lưu ý khi ghép clip: cẳng tay phụ `bone25`, `bone35` LẬT `sy = −1` trong `skill_02` (dáng dang tay), `bone34` trong `skill_01`; hoà hai dáng
mà nội suy tỉ lệ qua 0 thì lưới bẹp thành vệt (đã gặp, sửa trong `pha`: kênh tỉ lệ đổi dấu thì nhảy ở giữa). Clip gốc tự có cú nhảy 100–165°
một khung (dáng snap của IK nướng) ở `skill_01/02/03`.

Clip gốc: `idle_01` 4,0 (thở), `run_01` 0,8, `skill_01` 2,17 (liên hoàn: đấm 0,48, móc 0,96, tay phụ đập 1,69), `skill_02` 1,30 (hai nắm đấm
quá đầu 0,14–0,58, nện 0,72, tay phụ dang), `skill_03` 2,07 (nhún, nhảy xoay 1,15–1,38, đáp nện 1,61–1,84), `skill_04` 1,57 (lao húc 0,52, móc
lên 0,70–1,04), `skill_05` 0,67 (tay phụ chém), `hit_01/02`, `block_01`, `stun_01`, `die_01` 1,0.

## 2. Mảnh (`quy_nui_manh.py`, gói `gui_gpt/quy_nui_1/luot_2_Q1..Q6.txt`)

Concept TO HƠN rig (IoU hình bóng 0,63): căn bằng co k = 0,84 + dời (131, 71) px (`mau/can.json`, tìm theo IoU → 0,82). Mảnh "đúng chỗ, đúng
cỡ" trên concept (GPT vẽ lại chỉ vài mảnh không chồng nhau mỗi tờ, vẽ đủ phần khuất), đặt theo chỗ trên concept đã căn, gắn vào NHÓM lưới gốc
(gan_goc trên lưới gộp, `quy_nui_rig.gop_att`):

| mảnh | tờ | lưới gốc |
|---|---|---|
| `than` thân + mạch hổ phách | Q1 | `shenti2, bozi1, bozi2, xiongjia1, xiongjia2, shenti3` |
| `dau` đầu vượn + vương miện | Q2 | `tou` |
| `dam_R`, `dam_L` nắm đấm | Q2 | `shouR3_1`, `shouL3_1` |
| `kho` khố | Q2 | `weiqun` |
| `vai_R`, `vai_L` tảng vai | Q3 | `shouR1_2 + shouR1_1`, `shouL1_2 + shouL1_1` |
| `chan_R`, `chan_L` chân | Q3 | `tuiR1..3`, `tuiL1..3` |
| `canh_R`, `canh_L` cẳng tay trước | Q4 | `shouR2 + shouR3_2`, `shouL2 + shouL3_2 + shouL1_3` |
| `tren_R`, `tren_L` bắp tay phụ | Q4 | `jixieshouR1`, `jixieshouL1` |
| `duoi_R`, `duoi_L` cẳng + lòng bàn tay phụ | Q5 | `jixieshouR2`, `jixieshouL2` |
| `ngon_R1..`, `ngon_L1..` ngón vuốt | Q6 | ngón gốc gần nhất (`shouzhi*` hai đốt gộp) |

BỎ (Claude tự quyết, concept không có): đuôi `weiba1/2` + `jiapian` (vượn không đuôi), bốn dải `piaodai*` (concept chỉ có khố trơn).
Bộ mảnh tạm bằng da gốc để dựng thử: `quy_nui_rig.py goc_tam` → `manh_goc/`.

## 3. Rig + clip (`quy_nui_rig.py` → `inbox/quy_nui_1/rig/`)

Xương của họ (FK, bỏ shadow + 8 đích IK) + `move` + `mieng` (điểm phát VFX). Tay trước nửa phải tranh có BẢN SAO vẽ trước thân (`vai_L~t`,
`canh_L~t`, `dam_L~t`, ẩn sẵn) để lúc đấm ngực nắm đấm ra trước ngực (đổi thứ tự vẽ bằng hai slot).

| clip | dài | nguồn | ý |
|---|---|---|---|
| appear | 2,70 | skill_03 + skill_02 | rơi từ trên cao (dáng bay 1,30–1,42, hiện dần 0,12 s), `cham_dat` 0,36 đáp quỳ nện (dáng 1,58 → 1,84, bẹp nảy), đứng dậy 0,80–1,05, ĐẤM NGỰC so le 1,12 / 1,26 (hai nắm đấm trước, IK tới giữa ngực) / 1,40 / 1,54 (hai tay phụ vỗ đỉnh vai) / 1,68, ngực nảy mỗi cú, `gam` 1,86–2,32 (dáng dang tay skill_02 0,95, ngửa đầu, rung) |
| idle | 4,00 | idle_01 | + ngón tay phụ co duỗi lệch pha hai bên; tay phụ nửa phải tranh GÃI ĐẦU 2,35–3,35 (IK tới đỉnh sọ, gãi 0,22 s một nhịp, nghiêng đầu); `soi_roi` 1,2 |
| walk | 0,80 | run_01 | |
| attack | 1,40 | skill_01 nén | `dam1` 0,28, `dam2` 0,54, `trung` 0,94 (tay phụ đập); thân giật đúng mỗi nhịp |
| cast | 1,55 | skill_02 kéo dài | giơ hai nắm đấm quá đầu 0–0,40, gồng rung 0,40–0,64, `nen` = `trung` 0,72 (sóng chấn là VFX), `mieng` ở mặt đất giữa hai nắm đấm |
| skill | 2,80 | idle + skill_02 + IK | `tu` 0,15: hai tay phụ giơ dần lên ôm hai bên tảng đá (VFX, tâm = xương `mieng`, bán kính = 100 × tỉ lệ `mieng`, lớn 70 → 220 tới 1,15), ngón quặp, thân gồng rung; `nen` 1,32 và 1,62 (hai nắm đấm trước theo skill_02, tay phụ vẫn ôm); ngả ra sau 1,62–1,82, `nem` = `trung` 2,02: chồm tới, tay phụ vung theo đà, `mieng` thu về 0,02 (code sinh đạn từ đó); về idle |
| hit | 0,50 | hit_01 | |
| die | 1,45 | die_01 + tan | |

Trạng thái: xem mục 4.

## 4. Kết quả (2026-11-17), việc còn lại

- Tờ mảnh Q1–Q6: Codex đạt lượt đầu cả 6 (60–76 s mỗi tờ). Ghép 21 mảnh so concept: IoU hình bóng **0,978** (`manh/_ghep.png`).
  Cẳng tay trước GPT vẽ bù dài tới đất (chồng chỗ nắm đấm): cắt NGANG ở mép trên giữa nắm đấm + 75 px (`quy_nui_manh.py cat_canh`; cắt theo
  cột để lại hai dải mép dài, thành vệt nhọn khi cổ tay gập).
- Vai gắn CHỈ lưới `shouR1_2` / `shouL1_2` (cứng theo cánh tay): gắn gộp thêm `shouR1_1` (`bone65`, giáp vai tự vẫy của họ) thì tảng vai bị
  kéo nhọn ở dáng đấm.
- Rig `inbox/quy_nui_1/rig/`: 74 xương, 24 slot (21 mảnh + 3 bản sao tay), 3202 đỉnh, 8 clip, 18 sự kiện, `.atomik` 264 KB (atlas 720 × 800),
  chiều cao game 1006. Mọi clip không lặp nối về khung 0 idle lệch 0 px; appear khung đầu trống, die khung cuối trống. Trang `rig/xem.html`
  (thu_xem: đủ 8 clip, không lỗi JS); tờ khung runtime Spine thật `rig/khung_rt/<clip>.jpg`; tờ soi Python `rig/soi_<clip>.png`.
- Đo góc nhảy (`kiem`): các cú 36–107° một khung còn lại đều là nhịp snap của clip gốc (`skill_01/02/03`, `die_01` của họ có 100–165° một
  khung) hoặc cú đáp đất có chủ ý (appear 0,37 s). Đã sửa: tỉ lệ lật dấu (`bone25`, `bone35`, `bone34`) nội suy qua 0 (vệt bẹp), IK giữ nắm
  đấm tắt đột ngột ở skill, đoạn giơ nắm đấm của skill nén quá nhanh.
- (Lượt đầu còn: mép cắt cẳng tay lộ ở dáng đáp, dải rách trên đầu khi cúi / ngửa: đã sửa ở mục 4b.) Tảng vai nửa phải tranh vẽ sau thân như
  con gốc nên bị thân che nhiều hơn concept (giữ thứ tự vẽ gốc).

### 4b. Lượt sửa sau góp ý của người dùng trên tatu (2026-11-17, qua điều phối)

- **Idle mềm** (chê "idle giật, không mềm mại"): idle KHÔNG còn dùng chuyển động gốc. Dựng từ dáng tĩnh khung 0 idle_01 + sóng: ngực tỉ lệ
  1 ± 2 % (dọc) / 1 % (ngang) chu kỳ 2 s, hông nhấp 5 đv, đầu ±1,2° trễ 0,1 s, tay phụ ba đốt ±2,5 / 3,5 / 4,5° trễ 0,20 / 0,30 / 0,35 s
  (chu kỳ 4 s, hai bên lệch nửa chu kỳ), ngón co duỗi trễ 0,35 s, khố ±2° trễ 0,15–0,33 s; nắm đấm giữ đất bằng IK. Gãi đầu 1,80 → 3,90 s:
  với tay / hạ tay 0,75 s theo đường cong bậc năm (vận tốc, gia tốc 0 ở hai đầu), hai nhịp gãi nhỏ 12 đv chu kỳ 0,30 s. Đo (`kiem`): góc
  lớn nhất 6,6°/khung (cú với tay), gia tốc góc ≤ 1,85°/khung², nắm đấm 0 đv/khung, không cú snap nào. Nền của skill, appear cũng đổi sang
  dáng tĩnh khung 0 (không lấy idle_01 chạy).
- **Chỗ ghép** (chê "hở 1 chút"), soi cận ×3 ở idle 0 và các dáng xa nhất:
  - cẳng tay trước: cắt theo cột / cắt ngang để lại mép thẳng, góc nhọn, phần "trong lòng nắm đấm" lòi ra thành quạt mờ khi nắm đấm xoay →
    nay là ĐẦU TRÒN KHÉP KÍN có viền mực riêng ngay dưới mép trên nắm đấm (`cat_canh`: đường ngang + nửa elip, kẻ viền dọc mép mới);
  - thân: bỏ `bozi1/2` khỏi lưới gộp (xương cổ `bone62–64` giãn mạnh → lưới gập thành dải rách trên đầu khi cúi / ngửa);
  - chân (gộp đùi + cẳng + bàn), thân, cẳng tay, cẳng tay phụ: trọng số làm trơn theo lưới của mình (`MUOT`) rồi gắn kiểu thường (trọng số
    đổi đột ngột ở ranh hai khúc gốc → gối nứt một vạch sáng);
  - ngón vuốt: xương gốc ngón RIÊNG (`g_ngon_*`) đặt đúng chân ngón của mình, cha = xương nặng nhất của đỉnh lòng bàn tay gần nhất trên mảnh
    cẳng tay phụ của mình (bám xương ngón gốc thì ngón quay quanh khớp ngón của họ, văng khỏi lòng bàn tay).
- Rig sau sửa: 80 xương (thêm 6 xương gốc ngón), 24 slot, 3196 đỉnh, 13 432 khoá, `.atomik` 245 KB; nối clip lệch 0 px; thu_xem đủ 8 clip.

### 4c. Mốc sự kiện cho VFX (giây của clip; chiều cao game 1005)

| clip | sự kiện | VFX dự kiến |
|---|---|---|
| appear | `cham_dat` 0,36 | đáp từ trên cao: hố nứt, vòng bụi lớn, đá văng, rung mạnh |
| appear | `dam_nguc` 1,12 / 1,26 / 1,40 / 1,54 / 1,68 | bụi nhỏ ở ngực (cú nắm đấm) / ở đỉnh vai (cú tay phụ vỗ) |
| appear | `gam` 1,86 (rung 1,86–2,32) | rung nhẹ, sỏi rơi khỏi vai |
| idle | `soi_roi` 1,0 | 1–2 viên sỏi rơi khỏi vai |
| attack | `dam1` 0,28, `dam2` 0,54, `trung` 0,94 | mỗi nhịp chớp kem nhỏ + đá vụn ở đối thủ; nhịp 3 (tay phụ đập) to hơn, vòng bụi, khựng (khựng nhịp 1 cần code nghe `dam1`) |
| cast | `nen` = `trung` 0,72 | hai nắm đấm nện đất tại xương `mieng` (mặt đất giữa hai nắm đấm): vòng bụi + SÓNG CHẤN (bức tường đất cuộn đá lăn) chạy tới đối thủ, hất tung; cảm giác trúng khi sóng tới |
| skill | `tu` 0,15 | đá vụn dưới đất bay lên tụ thành TẢNG ĐÁ giữa hai tay phụ: tâm = xương `mieng`, bán kính = 100 × tỉ lệ `mieng` (70 → 220 đv, lớn dần tới 1,15) |
| skill | `nen` 1,32 và 1,62 | hai nắm đấm nện gồng: vòng bụi, rung nhẹ, vụn đá rơi khỏi tảng |
| skill | `nem` = `trung` 2,02 | tảng rời tay từ `mieng` (tỉ lệ `mieng` thu về 0,02 ngay sau): code bay vòng cung tới đối thủ ~0,4 s, nện: chớp màn kem, rung mạnh nhất, đá vỡ toé, bụi dày, mưa đá nhỏ |

- Việc tiếp: người dùng xem; VFX (bụi đáp đất, bụi đấm ngực, sóng chấn của cast, tảng đá tụ – bay – vỡ + mưa đá của skill, đá vụn từng nhịp đánh
  thường; khựng nhịp 1 của đánh thường cần code nghe sự kiện `dam1`); thay suất `phu_van` (ải 20)? tên, số dạng; heroes.json, prefab Unity.
