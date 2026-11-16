# Sói giáp sắt (`soi_giap`): tướng 6 đảo Kim

Bắt đầu 2026-11-16 (máy ổ C). Con gốc của rig: **`monster_3428`** (sói to cơ bắp ngồi thụp, đầu cúi, mặt nạ + mũ giáp gỗ nâu có tinh thể đỏ,
giáp vai sừng cong đen, ngực trần, đai thừng + vạt vải dài, khiên gỗ cao gấp đôi người, búa gỗ đai sắt; game tham khảo, kho
`D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `skill_02`). Xương, lưới, chuyển động gốc là của nhà phát hành game
đó (như aola): dùng nội bộ, không đăng công khai. Hình là của mình. Suất 6 đảo Kim = ải 30, id game hiện là **`chien_than`** (Chiến Thần, 2
dạng). Mã làm việc `soi_giap`. Tên, số dạng: chưa đặt.

Lượt đầu (cùng ngày) người dùng chưa chỉ con gốc, Claude tự tìm và chọn `monster_3263` (sói chibi giáp xanh, cùng họ 3254 / 3259 / 3261), gen
ba concept trên đó; người dùng chỉ lại 3428. Bản cũ cất ở `inbox/soi_giap_bo3263/` (không dùng).

## 1. Lời dặn của người dùng (2026-11-16)

- "làm tướng thứ 6 đảo kim; concept **sói humanoid mặc giáp sắt, cầm khiên sắt và búa sắt**".
- appear: "làm nó **nhặt khiên lên và gầm**".
- idle / walk: "làm **giống con gốc**".
- Đánh thường: "**lao lên dùng búa gõ** đối thủ".
- Chiêu mana: "**ném búa** vào đối thủ".
- Chiêu cuối: "vào **tư thế che khiên**, sau đó **charge nhanh xé gió** tới đối thủ **húc mạnh**, tạo thêm FX".
- die: "làm igoongshoj" (gõ nhầm; hiểu là "làm giống gốc": `die_01` búa rơi, đổ sập úp lên khiên). Chưa hỏi lại.
- "gốc là con này" (ảnh trang xem `monster_3428`).

## 2. Mổ rig gốc (`<SXS>/scan/monster_3428/`: `info.json`, `att_goc.json`, `att_idle0.json`, `khung/`, `mo/`, `parts/`; script `soi_giap.py`
mo / nhom / part_goc)

60 xương, 43 slot (39 hình bật ở idle 0), 13 clip, 3 556 khoá. Ràng buộc: **6 IK** hai đoạn: chân XA `L1` (`P_tuiL1`/`P_tuiL2`, bend −1) + `L2`
(`P_tuiL3`/`P_tuiL4`, bend 1), chân GẦN `R1` + `R2` (tương tự), TAY XA `SL1` (`P_shenti10`/`P_shouL1`) + `SL2` (`P_shouL2`/`P_shouL3`); đích là
con của `bone`. Không transform, path, physics; không đổi thứ tự vẽ trong clip. Con nhìn sang PHẢI, đầu cúi thấp giữa hai vai. `R` = bên GẦN
(trái hình: chân sau, tay cầm búa, vẽ trước thân), `L` = bên XA (phải hình: chân trước, tay đeo khiên). Mọi hình là lưới (8–30 đỉnh). Ảnh mẫu
`inbox/soi_giap_1/mau/goc_ca_con.png` 1536 × 1024: 1,092 px / đơn vị.

Cây xương chính: `root` → `bone` → `bone2` → `P_shenti1` (HÔNG / TÂM) → `P_tuiL1..L4` (chân xa), `P_tuiR1..R4` (chân gần), `P_yaodai` →
`_2` → `_3` (vạt, chuỗi 3), `P_diaozhui4` (nút đai), `P_weiba` → `_2` → `_3` (đuôi); `P_shenti1` → `P_shenti2` → `P_shenti3` (NGỰC) →
`P_shenti8` → `P_tou2` (ĐẦU: bờm, mặt, mặt nạ, mảnh đỉnh, hai tai `P_erduoR/R2`, `P_erduoL/L2`); `P_shenti3` → `P_toushi3` (TẤM GÁY: gắn NGỰC,
không gắn đầu), `P_xianglian1/2` (dây cổ), `P_diaozhui1` → `_2` (mặt dây), `P_shenti4..7`, `P_shenti11/12` (da ngực, cổ), `P_shenti9` →
`P_shouR1` → `P_shouR2` → `P_shouR31` (TAY GẦN) → `W_futou` (BÚA trong tay), `P_shenti9` → `P_jianjiaR02` (GIÁP VAI), `P_shenti10` →
`P_shouL1` → `P_shouL2` → `P_shouL3` (TAY XA), `P_shouL2` → `W_dunpai3` (KHIÊN), `P_shouL1` → `P_diaozhui7` → `_8`. `bone` → `W_futou2` (BÚA
BAY: bản sao chỉ bật ở die_01).

| thứ tự vẽ | slot | ảnh vùng (px) | đỉnh | là gì | xương |
|---|---|---|---|---|---|
| 1 | `W_dunpai1` | 200×348 | 8 | KHIÊN nhìn nghiêng (mặt hẹp trái, cạnh dày phải, núm tròn) | W_dunpai3 |
| 2–3 | `P_shouL1`, `P_shouL2` | 74×87, 58×90 | 10 / 9 | TAY XA: bắp (đai sẫm), cẳng | P_shouL1 / L2 |
| 4 | `W_dunpai6` | 82×74 | 9 | quai khiên cong trên cẳng tay xa | P_shouL2 |
| 5–6 | `P_shouL3`, `P_shouL31` | 51×59, 49×60 | 10 / 12 | bàn tay xa, vuốt TRƯỚC | P_shouL3 |
| 7 | `W_dunpai4` | 79×96 | 8 | quai trong mảnh | P_shouL2 |
| 8 | `P_weiba` | 63×49 | 25 | ĐUÔI (chóp trắng, chĩa trái) | P_weiba..3 |
| 9–11 | `P_tuiL3`, `P_tuiL2`, `P_tuiL1` | 60×34, 55×64, 85×67 | 16–21 | CHÂN XA: bàn, ống, đùi (đai sẫm) | IK L1 / L2 |
| 12–14 | `P_tuiR3`, `P_tuiR2`, `P_tuiR1` | 45×38, 52×57, 59×81 | 14–18 | CHÂN GẦN: bàn, ống, đùi | IK R1 / R2 |
| 15 | `P_shenti1` | 76×75 | 12 | HÔNG | P_shenti1 0,67 + shenti3 |
| 16 | `P_yaodai` | 70×100 | 20 | VẠT vải dài rách mép | shenti1 + yaodai..3 |
| 17 | `P_diaozhui3` | 36×36 | 8 | nút thừng bên trái | P_diaozhui4 |
| 18 | `P_shenti2` | 133×117 | 18 | NGỰC trần cơ bắp (lông trắng + xám) | shenti3 / shenti9 / shenti2 |
| 19 | `P_tou2` | 239×109 | 30 | BỜM lông dài sau đầu vắt sang trái | P_tou2 + shenti6 + shenti4 |
| 20 | `P_xianglian1` | 84×75 | 18 | dây da quanh cổ (lưỡi liềm sẫm) | shenti3 + xianglian1/2 |
| 21 | `P_diaozhui2` | 19×48 | 10 | mặt dây nhỏ (ẩn ở die, skill_01) | P_diaozhui8 |
| 22 | `P_tou1` | 82×82 | 23 | MẶT: mõm trắng, mũi đen | P_tou2 |
| 23, 24 | `P_yanjin1`, `P_yanjin2` | 18×19 | 10 | MẮT đỏ (khe dưới mặt nạ); bản nhắm (hit, die, stun) | P_tou2 |
| 25, 27 | `P_toushi3`, `P_toushi4` | 77×69, 60×32 | 8 / 9 | TẤM GÁY sau đầu + vành cong | P_toushi3 (con của NGỰC) |
| 26 | `P_toushi2` | 110×79 | 8 | MẢNH ĐỈNH mũ | P_toushi2 (con của đầu) |
| 28 | `P_erduoL` | 36×24 | 11 | TAI XA nhỏ (chĩa phải) | P_erduoL / L2 |
| 29 | `P_toushi1` | 87×126 | 9 | MẶT NẠ (vòng vàng, tinh thể đỏ + tím) | P_tou2 |
| 30 | `P_erduoR` | 47×34 | 11 | TAI GẦN (lòng trắng, chĩa phải) | P_erduoR / tou2 / R2 |
| 31 | `P_shouR32` | 23×39 | 11 | ngón tay gần SAU cán búa | P_shouR31 |
| 32 | `W_futou` | 119×116 | 12 | BÚA: đầu gỗ đai sắt, ngọc đỏ, cán chìa lên trái | W_futou (con của nắm tay) |
| 33 | `W_futou2` | | 12 | (ẩn) búa bay ở die_01 | W_futou2 (con của `bone`) |
| 34–36 | `P_shouR31`, `P_shouR2`, `P_shouR1` | 43×65, 71×86, 94×91 | 12–16 | TAY GẦN: nắm, cẳng (đai sẫm), bắp | P_shouR31 / R2 / R1 |
| 37 | `P_shouR12` | 45×83 | 14 | dây da chéo từ vai xuống ngực | shenti3 + shenti9 |
| 38, 39 | `P_diaozhui1b`, `P_diaozhui1` | 20×46, 20×52 | 14 | MẶT DÂY nanh vàng | shenti12 / diaozhui2 |
| 40, 41 | `P_jianjiaR03`, `P_jianjiaR01` | 41×33, 111×151 | 10 / 11 | GIÁP VAI gần + SỪNG cong đen, tinh thể tím | P_jianjiaR02 |
| (ẩn) | `W_dunpai2` | | 9 | KHIÊN nhìn THẲNG (núm tròn giữa): bật ở skill_02..05, hit_03 | W_dunpai3 |

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho (dự kiến) |
|---|---|---|---|
| `idle_01` | 2,00 | thở nặng, khiên dựng sau tay | **idle** (giống họ) |
| `run_01` | 0,80 | chạy chúi, khiên chìa trước, búa kéo | **walk** (giống họ) |
| `skill_01` | 1,17 | nhấc búa lên cạnh khiên (0,21–0,32), quật búa sang trái / xuống (0,42–0,64), về | nguồn **attack** (gõ búa) và **cast** (lấy đà ném) |
| `skill_02` | 1,17 | GIƠ KHIÊN qua đầu (0,11–0,21), đập khiên úp xuống đất trước mặt (0,32–0,64, hình khiên nhìn thẳng), nhấc lại | nguồn **appear** (nhấc khiên lên) |
| `skill_05` | 0,50 | VÀO thế che khiên: khiên hạ chắn ngang trước người, ngồi thụp | **chiêu cuối** pha 1 |
| `skill_03` | 1,00 | GIỮ thế che khiên (lặp) | **chiêu cuối** pha giữ + lao |
| `skill_04` | 1,00 | từ thế che khiên đứng dậy về idle | **chiêu cuối** pha về |
| `hit_03` | 0,50 | khiên xoay mặt ra trước che kín (hình khiên nhìn thẳng) | dáng chắn cho cú húc |
| `block_01` | 0,50 | búa giơ chéo trước ngực đỡ, về | |
| `die_01` | 1,00 | lảo đảo, búa rơi (`W_futou2`), đổ sập úp lên khiên | **die** (giống họ) |
| `hit_01`, `hit_02`, `stun_01` | | | **hit** = hit_01 |

Cần thêm ngoài con gốc: **mặt há miệng gầm** (appear): mặt `P_tou1` của họ miệng ngậm, không có hình há → gen thêm ảnh mặt há cùng khung, clip
đổi ảnh (mục 22 skill rig). **Búa bay** của chiêu mana: thêm xương / slot như giáo bay của Thiết Vệ (`fly_0`, `far`). **Khiên nhìn thẳng**
`W_dunpai2` phải gen theo thiết kế khiên mới (cùng lúc với mảnh khiên nghiêng).

## 3. Concept lượt 1 (Claude đề xuất ba hướng, CHỜ người dùng chọn)

Gói `gui_gpt/soi_giap_1/` (`soi_giap_da.py ca_con`, `concept`). Ảnh mẫu 1 = hình cả con gốc `mau/goc_ca_con.png` (khung 0 idle); ảnh 2 = Thiết
Vệ (nét, tô thép phẳng); ảnh 3 = voọc samurai (thú chiến binh chắc nịch, lông, giáp phẳng). Mọi hướng giữ dáng ngồi thụp, khối người to (không
chibi hoá), đầu cúi giữa hai vai, một khe mắt dưới mặt nạ, hai tai chĩa ngang; bỏ tinh thể, vòng vàng, mắt phát sáng; đổi dáng mảnh nhận diện
(mặt nạ + mảnh đỉnh, tấm gáy, giáp vai sừng, đầu búa, khiên); THÊM giáp ngực sắt (lời dặn "mặc giáp sắt"):
- `tai_ve/L1_A.png` **sói xám tro, giáp thép xám + đỏ thẫm**: mũ thép tròn một sống, mặt nạ mõm nhọn, cổ áo thép hai lớp, giáp vai ba lá + gai nón
  thẳng, giáp ngực một sống dọc, mặt dây nanh thép, đai vải đỏ, búa đầu trống tròn, khiên tháp đỉnh vòm viền đinh.
- `tai_ve/L1_B.png` **sói đen than, giáp gang + đồng thau**: mũ đỉnh bằng, mặt nạ khe ngang viền đồng, hai vây sắt vuốt sau, tấm gáy vuông, giáp
  vai vòm + ba gai ngắn, giáp ngực ba đinh đồng, đĩa đồng, thắt lưng da khoá đồng, búa khối có mỏ, khiên vát góc có sống dọc.
- `tai_ve/L1_C.png` **sói nâu đỏ, giáp bạc + xanh lam**: mũ chóp nhọn, mặt nạ mõm sói có thanh che mũi, tấm gáy ba lá xoè, giáp vai ba lá + vây
  lưỡi cong, giáp ngực hai lớp, đá xanh, đai vải xanh, búa tạ đầu vuông, khiên hình diều.

12:08: Codex hết hạn mức ("try again at 2:00 PM"), cả ba lệnh không ra ảnh. Lệnh nền chờ 14:02 bị treo ở bước ngủ (máy ngủ?); người dùng "gen
đi" lúc 14:05 → dừng nó, gen ngay. Ba ảnh đạt lượt đầu (98–112 s mỗi ảnh, không bị từ chối).

Soát: GPT vẽ to hơn con gốc (A ×1,22, B ×1,38, C ×1,10) nên độ khớp theo chỗ tuyệt đối thấp (0,65 / 0,52 / 0,77, `mau/_so_goc.png`); co về cùng
cỡ thì dáng khớp 0,87 / 0,86 / 0,89 (`mau/_so_goc_co.png`): thân, tay, chân, đầu cúi, búa trùng chỗ. Lệch: khiên cả ba hẹp hơn khiên gốc (gốc loe
sang phải); tai gần dựng đứng trên mũ thay vì chĩa ngang (mảnh tai sẽ vẽ theo khung tai gốc); B mỏ búa vểnh lên như sừng, giáp ngực vẽ cả múi
cơ; C vây lưỡi trên vai gần như cùng hình bóng sừng gốc. Một khe mắt dưới mép mặt nạ, tô phẳng, không tinh thể: cả ba đạt. Trang xem
`inbox/soi_giap_xem_concept.html`.

**Người dùng chọn B** (2026-11-16) → `tai_ve/L1_duyet.png`.

## 4. Mảnh + rig (concept B, 2026-11-16)

`soi_giap_manh.py` (`to`, `cat`, `khop`), gói `gui_gpt/soi_giap_1/luot_2_*.txt`, ảnh về `tai_ve/` (cả bảy lượt đạt lượt đầu, 67–134 s mỗi lượt):
- **Tờ liền L** (`mau/lien.png` → `N_lien.png`): năm hình bóng liền dựng từ lưới khung 0 idle: tay gần (bắp lông + bao tay gang đai đồng + nắm
  tay), thân (hông + ngực/giáp ngực + bờm), tay xa, chân gần, chân xa; chỉ viền ngoài + ranh chất liệu, không nét giữa hai mảnh lông. Nướng vào
  khung từng part qua lưới (`cat_lien`), phủ 0,93–0,99 hình bóng part.
- **Tờ ô A, C** (mảnh gốc làm hướng dẫn): mặt + ô MẶT HÁ gầm (cao 1,55 lần, GPT vẽ hàm dưới há, lưỡi, bốn nanh) → `manh/mat_ha.png`; vạt, đuôi,
  dây cổ, dây vai, quai khiên, quai trong, vuốt, ngón, nút đai, mặt dây (đổi thành ĐĨA ĐỒNG), mắt cam, mắt nhắm. IoU 0,90–0,96 (ngón tay nhỏ
  0,82, mắt 0,85; mặt dây 0,69 do cố ý đổi dáng).
- **Lượt mới M1–M4** (gen đúng chỗ từ concept B): mũ (đỉnh bằng, vành đồng, hai vây), búa (khối + mỏ + cán vòng đồng), giáp vai vòm ba gai, khiên
  tám cạnh sống dọc bốn đinh đồng, tấm gáy vuông, hai tai dựng. Đặt vào rig qua `mau/khop_concept.json` (concept = ảnh gốc × 1,380 + dời; IoU
  0,863), chưa cần `CHINH`. Hai tai Codex tô gần như toàn xám nhạt (ít lông than ngoài): giữ, gen lại nếu người dùng chê.
- Bỏ khỏi rig: `P_toushi2` (mảnh đỉnh mũ gộp vào mũ), `P_toushi4`, `P_jianjiaR03`, `P_diaozhui1b`, `P_diaozhui2`. Khiên nhìn thẳng `W_dunpai2` =
  khiên của mình lật ngang (đặt qua px ảnh vùng của hai part); búa bay của die `W_futou2` = búa của mình trên xương `W_futou2`.

`soi_giap_rig.py` (mẫu `chien_sat_rig.py`; `SG_GOC=1` dựng bằng da gốc → `rig_goc/`, trùng con gốc): 66 xương (60 của họ + move, far, fly_0,
ten_0, dau_bua, tam_khien), 39 slot, 457 đỉnh, NGUYÊN lưới của họ cho mảnh lông / dây / mặt; mảnh đổi dáng là mảnh cứng một xương. `.atomik`
387 KB, chiều cao game 641; mọi clip không lặp nối về khung 0 idle lệch 0 px.

| clip | dài | cách làm |
|---|---|---|
| idle | 2,00 | idle_01 |
| walk | 0,80 | run_01 |
| hit | 0,50 | hit_01 |
| attack | 1,10 | lấy đà vung búa qua người lên cao (skill_01 0 → 0,26 s) + LAO 0,5 chiều cao (game nắn quãng), quật búa xuống đất trước mặt (bắp tay −110°, cẳng +35°, nắm −55°, chúi người; quá đà 6 %, rung tay) `trung` 0,45, về idle |
| cast | 1,65 | thụp lấy đà, vung búa lên đỉnh (skill_01 0,10 → 0,26), `nem` 0,56: `bua_bay` (ten_0 con của fly_0, tâm quay = đầu búa) xoay tròn bay tới `far` 0,22 s, `trung` 0,78, giữ 0,1, bay về tay 0,32 s (`bat_bua` 1,20; tổng quay −1080° nên góc khớp lúc bắt), tay quật theo đà rồi giơ đón, về idle |
| skill | 2,80 | skill_05 vào thế che khiên (`che_khien`), skill_03 giữ + run gồng (`tu_luc` 0,50), LAO 1,2 chiều cao nhanh dần (`lao` 1,10; chân chạy run_01 nhịp gấp đôi, chúi thấp; khai lunge), HÚC (`huc` / `trung` 1,34: khiên thúc 40, người dội lại), skill_04 đứng dậy |
| appear | 2,15 | khiên úp đất (skill_02 0,55 s; tay búa giữ thõng như idle), nhấc khiên (`nhat_khien` 0,25 → 0,95), ngẩng đầu GẦM đổi sang `mat_ha` (`gam` 1,05), về thế; khung đầu trống |
| die | 1,45 | die_01 (búa văng, đổ sập lên khiên) + mờ dần; `nga` 0,75 |

- **IK đổi nhánh trong clip của họ** (skill_05 khung 4–5, skill_04 khung 2–8, die_01 khung 12–18: góc tay xa / chân nhảy 100–180° trong một
  khung; runtime của họ giải IK mỗi khung nên mượt, FK nướng nội suy 60 khung/giây sẽ lộ dáng lạ): `NHANH` bỏ qua đoạn đó, pha mượt hai đầu.
  Nối skill_03 → skill_04 pha 0,15 s. Sau sửa: bước xoay lớn nhất mỗi khung ≤ 67° (đòn quật, chân chạy), búa bay 82° (tốc độ xoay).
- Soi: tờ khung `rig/khung_*.png`, runtime thật `rig/that/*.jpg`, cận khớp `rig/can/`, `rig/can_chan/`; trang xem `rig/xem.html` (đủ 8 clip, không
  lỗi JS).

## 5. Làm lại ba clip tấn công (2026-11-16, người dùng: "animation tấn công cả 3 kiểu còn yếu và hơi xấu, sửa lại theo mô tả")

Bản đầu chỉ xoay FK tay búa trên dáng có sẵn của họ: không nhún lấy đà, không bật người, chiêu cuối là trượt ngang sau khiên. Làm lại bằng
**dáng khoá** (`soi_giap_don.py`, lớp `Bo`): tham số có nghĩa (hông dời / xoay, ngực, đầu, xương đòn; tay búa = góc vai → nắm tay + độ duỗi + góc
búa thế giới, IK hai khúc; bàn tay khiên giữ chỗ bằng IK + khiên giữ góc thế giới; cổ chân IK bám đất, chế độ "nghi" theo dáng nghỉ hoặc "nen"
giữ chân của dáng nền của họ), nội suy có đường cong (`noi`), lớp phụ trễ theo vận tốc thân (`phu`: bờm, vạt, đuôi, tai, mặt dây). Góc tay và
góc búa ghi liền vòng (búa quay trọn vòng theo chiều kim đồng hồ; runtime trộn clip bằng LerpAngle nên lệch 360° giữa hai clip vô hại).

| clip | dài | dãy dáng |
|---|---|---|
| attack | 1,15 | nhún thấp, búa kéo ra sau (0,17) → bật nhảy tới 74–80 đơn vị, búa vung vòng qua đầu, ngả lưng (0,33–0,40) → NỆN trong 2 khung: gập người 44°, búa chạm đất trước mặt đúng lúc đáp, búa giãn 1,3 (`trung` 0,467) → lún quá đà, búa nảy, rung tay → kéo búa về qua dưới |
| cast | 1,70 | xoay người kéo búa ra sau vai, nhấc chân trước (0,24–0,40) → bước tới quăng cả người, `nem` 0,50 → tay theo đà xuống thấp, giữ; búa xoay bay tới `far` 0,20 s (`trung` 0,70), giữ 0,08, bay về 0,34 → giơ tay bắt (`bat_bua` 1,12), bị búa giật ngả ra sau → hạ búa |
| skill | 2,74 | skill_05 vào thế che khiên (0,45) → gồng (hai dáng lệch 1,4° đổi mỗi 2 khung) + CÀO CHÂN gần xuống đất hai lần → rút ra sau, khiên dựng mặt ra trước (pha sang dáng hit_03 của họ) (1,10) → LAO 1,2 chiều cao, nhanh dần bậc 3, chân chạy run_01 ×2, cả con giãn 1,10 → HÚC (`huc` / `trung` 1,333): khiên thúc 54, cả con nén 0,87 rồi nảy, dội trượt lùi 10 %, khiên rung, búa văng theo đà → hạ về thế che, skill_04 đứng dậy, lùi về chỗ |

Đo sau sửa: bước xoay lớn nhất mỗi khung 30 khung/giây: attack 120° (bắp tay khiên lúc thân lướt qua bàn tay giữ khiên, nằm khuất sau thân), cast
92°, skill 77° (chân lúc bật chạy). Lấy mẫu runtime thật 60 khung/giây: không xương nào quay ngược vòng; bước dời lớn nhất là đầu búa lúc nện
(512 đơn vị / khung, đúng ý ra đòn 2 khung). Mọi clip nối idle 0 px, `.atomik` 391 KB. Impact: attack (0,07; 0,35; 0,09), skill (0,16; 1,3; 0,24).
Tờ khung runtime thật của ba clip: `rig/that_don/`.

## 6. Dạng 1 (sói con chibi), 2026-11-16

Người dùng: "ok ổn rồi, làm dạng 1 đi"; hỏi lại hai câu (trang so `inbox/soi_giap_non_chon.html`): chọn **chung rig 3428** (không dùng rig sói con
3254 / 3263) và **"ít giáp, màu nhạt"**, Claude gen vài hướng.

- Rig: `SG_DANG=non py -3 -I ArtGen/Spine/soi_giap_rig.py ...` (tên `soi_giap_non`, thư mục `inbox/soi_giap_non/`; mảnh tìm ở `soi_giap_non/manh`
  trước, thiếu thì lấy `soi_giap_1/manh`). `TI_LE` (tỉ lệ riêng, con thừa hưởng): thân trên `P_shenti2` 0,85 (ngực, tay, đầu theo), đầu `P_tou2`
  1,45 / 0,85, chân `P_tuiL1` / `P_tuiR1` 0,82 (hông `bone2` hạ tự động cho bàn chân chạm đất như dáng gốc), giáp vai 0,72, khiên 0,95, búa 1,0
  (net 0,75 vì tay 0,88), bờm `P_shenti4/6` 0,62; bỏ tấm gáy `P_toushi3`. Mảnh cứng tính điểm gắn theo dáng CHƯA đổi tỉ lệ (`Wi0`) để co theo xương.
  Chiều cao game 535 (dạng 2: 641).
- Bố cục: `mau/bo_cuc.png` (`bo_cuc`), `mau/bo_cuc_khung.png` (`soi_giap_non.py khung`). Bờm vẫn vồng sau lưng vì một phần lưới bờm bám xương đầu:
  lúc vẽ mảnh cho bờm nhỏ lại trong khung.
- Concept (`soi_giap_non.py concept` → `gui_gpt/soi_giap_non/luot_1_concept_<A|B|C>.txt`; ảnh mẫu: bố cục, concept dạng 2, hổ con dạng 1):
  A xám tro + đồ da + sắt thô (mũ sắt tròn, áo gi lê da, khiên gỗ tám cạnh viền sắt, búa khối nhỏ); B xám xanh + mũ da (ngực lông xù, khiên tròn
  gỗ, vồ gỗ); C xám bạc + than, thép mỏng + đồng (dạng 2 thu nhỏ: mũ đỉnh bằng mầm vây, vai một gai cụt, khiên gỗ tám cạnh đinh đồng, búa u mỏ).

Ba ảnh đạt lượt đầu (88–103 s). Khớp bố cục rig (`soi_giap_non/mau/_so_bo_cuc.png`): A 0,72, B 0,65, C 0,74; cả ba bỏ bướu bờm (đúng dặn), thân gọn
hơn bố cục (A, C nhỏ hơn chút, B to hơn), một mắt to, tô phẳng. Thân / tay chân trên rig là lưới dạng 2 co lại nên sẽ đậm người hơn concept chút.
Trang xem: `inbox/soi_giap_non_xem_concept.html`. CHỜ người dùng chọn.

**Người dùng chọn A** (2026-11-16) → `soi_giap_non/tai_ve/L1_duyet.png`.

### 6b. Mảnh + rig dạng 1 (concept A)

- `soi_giap_non.py manh` (prompt) / `cat` / `dau` + `cat_dau` / `khop`. Bốn lượt gen + một lượt biến thể đầu, đều đạt lượt đầu (67–95 s):
  - Tờ liền dạng 1 (`mau/lien.png` → `N_lien.png`): cùng hình bóng khung part như dạng 2, màu A (lông xám tro #AD9A9E, kem #F1E4DB), áo gi lê da
    khoá sắt, cẳng tay quấn da; bờm co 0,62 về phía đầu (`soi_giap_manh.CO_BOM`) còn chỏm lông quanh cổ (phủ 0,45 khung bờm: đúng ý).
  - Mảnh viền riêng (đuôi, ngón, vuốt, dây cổ, dây vai, quai khiên, vạt, nút đai thành thừng vàng): ĐỔI MÀU mảnh dạng 2 bằng mã (`to_mau`), không gen.
  - Đúng chỗ trên concept A: M1 mũ sắt tròn + búa nhỏ cán gỗ + khiên gỗ tám cạnh; M2 ĐẦU trọn (mắt to, mõm kem, quai da; không mũ, không tai)
    + giáp vai da; M3 hai tai. `luot_3_dau` (tờ hướng dẫn = chính ảnh đầu): đầu NHẮM mắt ("`>`", trúng đòn / choáng / chết) + đầu HÁ gầm.
- Khớp concept A ↔ rig non (`mau/khop_concept.json`): concept = bố cục × 0,995 + (4,7; 8,6) theo năm mốc (mũi, hai bàn chân, hai bàn tay; sai
  5–35 px); dời riêng (`DOI`): đầu + mũ + tai +29 px theo mũi, búa theo nắm tay, khiên theo bàn tay xa; giáp vai "neo2" = tâm giáp vai dạng 2 đổi
  sang dáng non (vai rig cao hơn vai concept ~190 px).
- Rig (`SG_DANG=non`): mảnh đổi dáng của dạng non đặt theo thế giới ĐÃ đổi tỉ lệ (`goc=False`), mảnh dạng 2 theo dáng gốc (`Wi0`). Đầu mắt to thay
  `P_tou1`; mắt rời + mặt dây ẩn; tai gần vẽ TRƯỚC mũ (slot `P_toushi1` mang tai gần, slot `P_erduoR` mang mũ: vành mũ che gốc tai như concept).
  `mat_nham` bật đúng các khung họ bật `P_yanjin2`; `mat_ha` cho đoạn gầm của appear. Dáng khoá ba đòn: độ dời tuyệt đối (hông, nhảy, chân, tay
  khiên) nhân 504 / 641 (`co_khoa`). Impact nhẹ hơn dạng 2: attack (0,05; 0,25; 0,07), skill (0,12; 0,9; 0,18).
- **Tiến hóa** (gộp rig dạng 2 dựng ở tiến trình riêng, lệnh `nhe`): `evolve` 2,8 s: sói con vào thế che khiên, gồng run mạnh dần (`tu_luc`
  0,3), đổi dạng 1,25 (`doi_dang`), dạng 2 hiện đúng đoạn ngẩng đầu gầm của appear (`gam` 1,62), hoà về khung 0 idle dạng 2 (lệch 0,00 px; dạng 2
  co 0,786 trong rig gộp). Khiên nhìn thẳng của dạng 1 (ẩn mặc định) phải tắt tay theo nhịp mờ dạng cũ.
- Dung lượng: lần đầu 726 KB (vượt trần 0,5 MB); thu ảnh dạng 2 trong rig gộp còn 0,55 (chỉ hiện lúc tiến hóa), ảnh dạng 1 còn 0,88, nới lược khoá
  (xoay 0,12°, dời 0,25) → **457 KB**. `soi_giap_non.atomik`: 132 xương, 75 slot, 861 đỉnh, 9 clip, chiều cao game 504; mọi clip nối idle 0 px.
- Đo: bước xoay lớn nhất mỗi khung như dạng 2 (attack 119°: bắp tay khiên khuất sau thân; cast 107° khiên lúc vung; skill 77° chân chạy). Runtime
  thật: `rig/that/*.jpg`; trang xem `rig/xem.html` (9 clip, không lỗi JS).

## 7. Vào game + VFX (2026-11-16, người dùng: "ok cho vào game và làm các fx cần thiết")

- **Dữ liệu** `ArtGen/Spine/quai/doi_soi_giap.py` (mẫu doi_quy_xich): thay HÌNH suất `chien_than` (ải 30 Kim), giữ id, chỉ số, hiệu ứng thẻ, số dạng.
  Tên TẠM do Claude đặt, chờ người dùng: Sói Giáp (danh hiệu "Sói chiến binh khiên búa", "Dòng Sói Giáp"); dạng Sói Giáp Con (`soi_giap_1`, cỡ
  0,86) → Sói Giáp (`soi_giap_2`, cỡ 1,1); thẻ Ném Búa Sắt (hammer), Khiên Xé Gió (shield), Giáp Sắt (helmet). Cỡ 0,86 / 1,1 ≈ 504 / 641 (hai
  dạng cùng tỉ lệ điểm ảnh trên sân). Evolve trong rig gộp co dạng 2 về 504 đúng ô xem tướng (HeroViewer dựng hai dạng cùng chiều cao).
  `chep`: Resources/soi_giap_1 (soi_giap_non.atomik có evolve, 456 KB), Resources/soi_giap_2 (390 KB) + chân dung. Resources/chien_than_* giữ.
- **VFX** `Assets/01 Script/Game/Battle/HatSoi.cs` (partial HatLua, đường "n_", phát lúc clip bắt đầu, mốc co theo lead):
  - `n_soi_go` (đòn thường, một mã cho cả hai dạng): bụi lúc bật đi (0,17); cung búa bổ từ trên đầu (lead − 0,04); búa nện ở đầu búa đo trên rig
    (đỉnh lao + (0,6; 0,08) chiều cao): chớp sắt, tia, dăm thép, sóng đất, bụi, sỏi, rung.
  - `n_soi_nem1` / `n_soi_nem` (mana): bụi lúc vung (0,24); tia lúc búa rời tay (0,50); búa bay XOÁY: sợi gió + cung gió quay theo góc búa, bám
    đúng đường bay (bảng số đo bua_bay 0,50 → 1,133 s: phần riêng + W × thân đối thủ, như xương fly_0 được game lái); trúng (0,70); nảy (0,77);
    về tay (1,12).
  - `n_soi_huc1` / `n_soi_huc` (chiêu cuối, sói con 0,85): che khiên (chớp khiên, bụi); tụ lực 0,45–1,05 (sợi gió hút vào khiên, bụi xoáy, sỏi run
    nảy, khiên loé 0,75 / 0,98, vòng gió co lại); bật lao 1,17 (bụi tung, vòng đất); lao 1,17–1,333 (sợi gió xé ngược dọc thân, NÓN GIÓ cung trước
    mép khiên, bụi kéo vệt; thân theo bảng quãng move / đỉnh); húc 1,333 (chớp lớn, tia, dăm, vòng sóng kép, gió toạc sau lưng đối thủ, sóng
    đất, rung 0,6).
  - Đăng ký: StageView.KimFx / KimAtk, HatNuoc.PlayNuoc, HatVoi.AtkLao (`n_soi_go`), HatLua.Themes["chien_than"] (tia trắng ngà, vòng thép, mảnh
    sắt đen), menu thử KimFxTour (Sói Giáp / Sói Giáp Con). Không cần HoldNuoc (rig tự giữ dáng húc).
- **Soi trong trận** (menu thử Đảo Kim, ảnh `Temp/PokiShots/kim_fx/chien_than_<1|5>sao_*.jpg`): búa nện đúng đầu búa trước chân đối thủ; búa bay
  trúng mặt đối thủ, cung gió xoay quanh búa cả lượt về, chớp lúc bắt búa ở tay; húc đúng mép khiên chạm đối thủ. Lần đầu các vòng gió vẽ bằng
  `Ring` (có viền mực) thành vòng đen dày → đổi sang `SgVong` (vòng trắng không viền), vòng thép lúc húc thu còn 0,6 thân. Test EditMode 106/107
  (hỏng `PrefabOnlyTests` vì UI/Kit/NumberTicker.cs, UiMotion.cs: có từ trước, không thuộc phần này).
