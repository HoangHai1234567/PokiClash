# Kiếm sĩ rừng mặc giáp (`kiem_si`): tướng thứ 8 đảo Mộc

Bắt đầu 2026-11-12. Con gốc của rig: `monster_3620` (game tham khảo, kho `D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang
xem, clip `skill_2_2`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là
thiết kế của mình. Tên, id game, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-12)

- "làm tiếp tướng thứ 8 đảo mộc; **concept như con gốc tôi gửi, biến tấu đi**, con gốc là bọ hung bạn có thể **đổi sang con khỉ hoặc không
  nhất thiết phải là 1 sinh vật**, chỉ cần nó **mặc giáp, có 1 chút thiên hướng rừng rậm, samurai**".
- "idle và run bạn làm tùy thuộc theo kiểu concept gen ra".
- Đánh thường: "làm giống `skill_1` là **dùng báng kiếm đập đối thủ**".
- Chiêu mana: "làm theo kiểu `skill_2`, **cúi xuống hold, rút kiếm chém**, trong lúc hold **có thể move tới đối thủ**".
- Chiêu cuối: "là kết hợp của `skill_4` tới `4_4`: `skill_4` tướng **rút ra 2 kiếm** rồi làm hiệu ứng **di chuyển biến mất cực nhanh**, sau
  đó **spawn các ảo ảnh chém tướng địch ở nhiều góc** (`4_1` đến `4_4`), sau đó **về lại vị trí ban đầu rồi đóng kiếm**; **khi đóng kiếm
  tướng địch bị chém liên tục từ các vết trước**".
- "appear và die bạn tự làm".

Loài, mũ, màu, chi tiết người dùng chưa chốt: mục 3 là **đề xuất của Claude**, chờ chọn hướng.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3620/`: `info.json`, `att_goc.json`, `att_idle0.json`, `manh_anh.png`, `manh_dang_idle0.png`, `parts/`, `khung/`, `can/`)

71 xương, 65 slot (56 hình bật ở idle), 17 clip, atlas 57 vùng. Con gốc là bọ hung samurai gù lưng thế iai, nhìn sang PHẢI, chỉ lộ một
mắt: không lật. **Gần như mọi hình là mảnh cứng một xương** (lưới 4–26 đỉnh); nhiều xương chỉ có: hai chùm lông sau lưng
(`P_shengzi_da1` bone34-35-37, `da2` bone38-39-40: chuỗi 3 đốt), bốn tua vai (`P_jianjia*_G*`: chuỗi 3 đốt `bone53..56` + `b`, `c`), áo
trùm cổ `P_tou2` (bone5-6-7), ngực `P_shenti2` (bone3 + bone5).

IK: bốn chân, mỗi chân hai khúc (`Lq`: bone12-13, `Lh`: bone8-9, `Rh`: bone10-11, `Rq`: bone14-15; đích là con của `bone`); hai IK tay
xa (`shouL`, `shouL2`) mặc định tắt (mix 0).

Cây xương: `root > bone > bone2 > bone3` (hông) `> bone4 > bone5` (ngực) `> bone6` (mũ) `> bone7` (đầu, mặt, mắt).
- `bone3`: bốn hông chân (bone8, 10, 12, 14), bụng `P_shenti1`, ba đoạn thừng bện `P_shenti_sheng1..3`.
- `bone4`: `bone46` (kiếm ngắn B giắt đai), `bone49` (kiếm dài A lúc giắt hông).
- `bone5` (ngực): tay XA (bên phải hình) `bone17 > bone18 > bone19 > bone20` (bắp `P_shouL1` + khuỷu `L2_2` trên bone18, bao tay `P_shouL2`
  bone19, bàn tay bone20 + ba ngón bone25-27); tay GẦN (bên trái hình) `bone21 > bone22 > bone23 > bone24` (bắp `P_shouR1` + khuỷu
  `R2_2` trên bone22, bao tay `P_shouR2` bone23, bàn tay bone24 + ngón bone28-30); tấm vai gần `P_jianjiaR2` bone42, `P_jianjiaR1`
  bone43 (con của bone21); tấm vai xa `P_jianjiaL2` bone44, `L1` bone45 (con của bone17); giáp ngực `P_shenti2_2` bone16; cụm sau lưng
  `bone33` (cánh cứng `P_ke`, `P_keR` bone31, `P_keL` bone32, hai chuỗi chùm lông).
- Kiếm dài A: vỏ `W_daoA_1` / `A_3` / khâu `A_5` trên `bone47` (con của bàn tay gần bone24); lưỡi `A_4` + chuôi `A_2` trên `bone51` (con
  của bone47: trượt ra khỏi vỏ). Bộ thứ hai `A_6`, `A_7` trên `bone48` (con của bàn tay xa: kiếm trần trong tay xa); bộ thứ ba `A_8..12`
  trên `bone49` (giắt hông). Kiếm ngắn B: `B_1..4` trên `bone46` (giắt đai), `B_5`, `B_6` trên `bone50` (con của bàn tay xa).
- Thứ tự vẽ (sau → trước): chùm lông `da2`, `ke`, chùm lông `da1`, cánh cứng `keR`, `keL`, chân xa sau `tuiL_H`, bụng `shenti1`, chân xa
  trước `tuiL_Q`, chân gần sau `tuiR_H`, chân gần trước `tuiR_Q`, thừng `sheng2`, `sheng3`, tua vai xa, tay xa (`shouL2_2`, `L1`), ngực
  `shenti2`, giáp ngực, bao tay xa, tấm vai xa (`L2`, `L1`), kiếm B, thừng `sheng1`, ngón tay sau kiếm, kiếm A, ngón tay trước kiếm,
  đầu (`tou2`, `tou`, mắt, mặt nạ `toukui2`), mũ `toukui`, bàn tay gần, khuỷu + bắp + bao tay gần, tấm vai gần (`R2`, ba tua, `R1`).

Clip của họ (tờ `khung/`):
| clip | dài | nội dung |
|---|---|---|
| idle_01 | 4,0 s | thế thủ gù, nhún nhẹ, hai tay giữ kiếm dài còn trong vỏ |
| run_01 | 0,67 s | bốn chân bọ chạy lon ton, thân nhấp nhô |
| skill_1, skill_1_2 | 1,67 s | lấy đà 0–0,56 (dựng vỏ kiếm ra sau); xoay người QUẬT cả kiếm còn trong vỏ tới trước 0,74–0,93; giữ; thu về 1,48 |
| skill_2 | 2,0 s | cúi thấp GIỮ THẾ 0,22–0,67 (tay đặt chuôi); RÚT chém vọt lên 0,89 (kiếm giơ cao, vỏ ra sau); giữ 1,11–1,33; chém xuống 1,56; tra kiếm 1,78 |
| skill_2_2 | 2,0 s | bản khác: giữ thế, rút kiếm đưa lên cao bên trái 0,89–1,33, bổ dọc xuống 1,56, tra kiếm |
| skill_3 | 2,5 s | (chưa dùng) |
| skill_4 | 3,17 s | cúi 0,35; rút HAI kiếm 0,70–1,06 (kiếm dài tay gần, kiếm ngắn tay xa, bắt chéo); BIẾN MẤT 1,41–2,11; hiện lại 2,46 đã tra một kiếm, dựng kiếm dài tra vào vỏ 2,81; về |
| skill_4_1 .. 4_4 | 0,5–0,67 s | ẢO ẢNH (cả con nhuộm lục, trong suốt) lướt qua chém từ bốn hướng: 4_1 ngang từ trái, 4_3 từ trên trái chéo xuống, ... |
| hit_01/02, stun_01, block_01 | | |
| die_01 | 1,0 s | bật ngửa lên rồi đổ sấp, mũ chúc xuống đất |

## 3. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `ArtGen/Spine/kiem_si.py` (`part_goc`, `luoi_xem`, `bo_cuc [hướng]`), `kiem_si_bo_cuc.py`, `build_kiem_si.py` (gói
`gui_gpt/kiem_si_1/`). Sơ đồ bố cục = khối từng part của rig ở dáng thủ idle giây 0 (tỉ lệ rig → khung concept 0,86), tô màu của mình;
MŨ SỪNG của con gốc bỏ, mũ của mình vẽ bằng mã; chùm lông sau lưng đổi thành đuôi / chùm dương xỉ.

Giữ của con gốc: dáng gù thế rút kiếm nhìn sang phải, một mắt; tấm vai gần rất to có huy hiệu + ba tua; hai kiếm còn trong vỏ (kiếm dài
chéo từ sau lưng xuống tay gần, kiếm ngắn giắt đai); giáp ngực, đai thừng bện, bao tay; áo sau lưng.

Lượt 1, ba hướng:
- `khi_non` **A · khỉ ronin nón lá**: khỉ lông nâu hung, mặt da trần; **nón lá chóp rộng vành** (kasa) có hai lá giắt; giáp **nan tre**
  buộc dây lục, bao tay gỗ sẫm; áo tơi lá chuối; tua và dây quấn chuôi cam; **hai chân** khỉ, **đuôi cuộn** sau lưng.
- `khi_mu` **B · voọc tướng quân**: voọc lông than, **ria trắng** quanh mặt; **mũ kabuto** sơn lục có tấm che gáy, mào là **một chiếc lá
  to** quét lên phải (thay sừng); giáp sơn lục rêu viền tre, dây hổ phách; hai chân, đuôi dài chóp trắng.
- `giap_rong` **C · bộ giáp vô chủ**: không phải sinh vật: giáp gỗ cũ, bên trong là **bó dây leo**; **mặt nạ gỗ** một khe mắt vàng; mũ
  kabuto gỗ phủ rêu, mào là **nhánh cây**; **bốn chân rễ** (giữ đủ bốn chân của rig); chùm dương xỉ sau vai; tua đỏ gạch.

Cả ba ra đúng bố cục ngay lượt đầu (`tai_ve/L1_khi_non.png`, `L1_khi_mu.png`, `L1_giap_rong.png`; trang so `inbox/kiem_si_xem_concept.html`),
đã mở cho người dùng chọn 2026-11-12. Lưu ý lúc gen mảnh: trên bản A vỏ kiếm dài và vỏ kiếm ngắn bắt chéo sau bao tay gần, nhìn dễ lẫn
vỏ nào của kiếm nào (rig: vỏ kiếm DÀI đi từ tay gần lên trên-trái, vỏ kiếm NGẮN từ đai xuống dưới-trái).

Hai hướng khỉ chỉ dùng hai trong bốn chân của rig (chân gần-sau `Rh` và chân xa-trước `Lq`); hai chân còn lại bỏ, clip chạy phải viết lại
nhịp hai chân. Hướng C dùng nguyên bốn chân và nhịp chạy của họ.

**Người dùng chọn B** (2026-11-12: "B") → `tai_ve/L1_duyet.png` = `L1_khi_mu.png`. Không dặn sửa gì thêm.

## 4. Mảnh (`build_kiem_si.py manh` → gói `luot_2_manh_*.txt`; `kiem_si_manh.py lam` → `inbox/kiem_si_1/manh/`)

Gần như mọi mảnh của rig là mảnh cứng → tám tờ, cả tám ra dùng được ngay lượt đầu (mỗi tờ ~100 giây):
- Sáu tờ "đúng chỗ, đúng cỡ" từ concept (mỗi tờ giữ vài mảnh không chồng nhau, vẽ đủ phần khuất): `M_A` tấm vai gần, tấm vai xa, bao tay xa,
  hai giáp ống chân; `M_B` mũ (không lá mào), bao tay gần, hai bàn chân; `M_C` đầu (không mũ, có dây cằm), áo tơi lá, hai nắm tay; `M_D` thân
  lông, đuôi; `M_E` giáp ngực, váy vải; `M_F` đai thừng bện.
- Hai tờ mảnh rời: `M_S1` hai thanh kiếm tháo rời nằm ngang, mũi bên trái (vỏ dài, lưỡi dài, chuôi dài + kiếm cách; vỏ ngắn, lưỡi ngắn, chuôi
  ngắn); `M_S2` hai tua, lá mào to, lá mào nhỏ, bắp tay gần, bắp tay xa, hai đùi lông.
- Lá mào, bốn tua đặt lên concept theo (gốc, ngọn) đọc trên concept kẻ lưới (`ROI` trong `kiem_si_manh.py`); bắp tay, đùi đặt tạm rồi bước rig
  nắn theo xương; kiếm đặt ở bước rig. Tờ so: `manh/_so_ghep.png` (concept | ghép lại, chưa có kiếm); 32 ảnh, 28 mảnh + 6 mảnh kiếm.
- Thứ tự vẽ (sau → trước): đuôi, áo tơi, chân trước (bàn, đùi, giáp ống), chân sau, tua vai xa, bắp tay xa, thân, váy, giáp ngực, bao tay xa,
  tấm vai xa, [kiếm ngắn: lưỡi, vỏ], đai thừng, [chuôi kiếm ngắn; kiếm dài: lưỡi, chuôi, vỏ], nắm tay xa, đầu, lá mào nhỏ, lá mào to, mũ, nắm
  tay gần, bắp tay gần, bao tay gần, ba tua, tấm vai gần.

## 5. Rig (`kiem_si_rig.py` → `inbox/kiem_si_1/rig/`)

- **Dáng gốc của rig mình = khung 0 `idle_01` của họ** (thế thủ gù; concept vẽ theo dáng đó). Giữ xương thân, đầu, mũ, hai tay, hai tấm vai,
  giáp ngực, mọi xương kiếm, hai đích chân `Rh` (chân sau) và `Lq` (chân trước); bỏ hai chân kia, cánh cứng, chùm lông, chuỗi tua, ngón tay
  (`BO`). Tỉ lệ: 0,36 đơn vị mình / đơn vị con gốc; ảnh atlas 0,56 px / đơn vị con gốc.
- Khớp khung concept ↔ rig: bình phương tối thiểu trên tâm bốn mảnh (hai tấm vai, hai bao tay) + hai lòng bàn chân ↔ hai đích chân
  (0,891 px / đơn vị con gốc, lệch 12–40 px). Bản đầu lấy cả đai thừng và giáp ngực làm mốc thì lệch tới 112 px (hình mình khác hẳn hình họ).
- **Chân**: KHÔNG dùng hai khúc chân bọ của họ (đùi chìa ngang, móng dài cắm xuống: lắp giáp ống chân vào thì bị kéo dài 1,8 lần, nghiêng 35°).
  Bàn chân + giáp ống chân bám cứng xương ĐÍCH của họ (đích đứng yên trong mọi clip trừ chạy và vài bước của chiêu); đùi là lưới giãn: đầu
  trên theo hông `bone3`, đầu dưới theo đích.
- Tay: bắp và bao tay đặt theo HAI KHỚP (tỉ lệ khung ảnh → gốc xương và gốc xương con, chỉ đoạn giữa co giãn); nắm tay theo một khớp.
- **Kiếm**: mỗi slot kiếm của họ một slot của mình (cùng xương), ảnh của mình đặt cho trục dài trùng trục kiếm của họ (tính từ bốn góc hình ở
  dáng gốc → khung 0 idle); chuôi lùi 8 % về phía miệng vỏ cho kiếm cách che khe. Slot họ để trống mặc định (kiếm trên tay xa, kiếm giắt hông)
  thì của mình ẩn sẵn; clip bật tắt theo đúng mẫu khung của họ (`kiem_hien`). Bỏ khâu kiếm `W_dao*_5` và vỏ phụ `W_daoA_3`.
- Xương của mình (`x_*`): đuôi 5 đốt (con của hông), áo tơi 3 đốt (con của HÔNG: bám ngực thì lúc thân ngửa ra nó tụt xuống trước bụng), váy 2
  đốt, hai lá mào (con của mũ), bốn tua (con của tấm vai): đều có lò xo + gió. Áo tơi và tua TREO theo trọng lực (`sau()` giữ hướng thế giới).
- Xương `far` (chỗ đối thủ, game dời) + bốn xương `ao_a..d` (ảo ảnh) và `vet_a..d` (chỗ + hướng vết chém cho VFX) là con của nó.
- 63 xương, 45 slot, 824 đỉnh; chiều cao game 363; `.atomik` 462 KB (atlas 1392 × 1448; dưới trần 0,5 MB, trên đích 0,3 MB vì bốn ảnh ảo ảnh).

## 6. Clip (`kiem_si_clip.py`: nền lấy mẫu của họ + phần riêng)

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| appear | 1,75 s | rơi từ tán cây xuống (co người, hiện dần 0,07 s), chạm đất thụp sâu 0,34, giữ thấp, đứng dậy vào thế 1,12, bật chuôi rồi ấn "cạch" | dap_dat 0,34; cach 1,56 |
| idle | 4,0 s lặp | nguyên idle_01 + gió trên lá mào, tua, áo tơi, đuôi; 2,2–3,1 s liếc đối thủ, ngón cái bật chuôi (lưỡi ló ra), ấn vào, đuôi quất một nhịp | cach 3,12 |
| walk | 0,6 s lặp | run_01 của họ (chúi người, dựng vỏ kiếm ra sau); chân trước lấy trễ 7/20 nhịp cho hai chân so le | |
| attack | 1,2 s | skill_1 của họ nén lại: dựng kiếm còn trong vỏ ra sau 0–0,40, xoay người QUẬT tới 0,50, giữ, thu về; lao 0,55 chiều cao | trung 0,50 |
| cast | 2,23 s | skill_2 của họ: cúi 0,30; GIỮ THẾ tới 0,86 (rung gồng, trong lúc đó LƯỚT tới đối thủ 0,62 chiều cao); rút kiếm chém vọt lên 1,03; giơ; bổ xuống 1,76; tra kiếm; lướt về | trung 1,03; chem2 1,76 |
| skill | 3,11 s | skill_4: lùi cúi, rút HAI kiếm 0–0,90; kéo vệt về trước rồi BIẾN MẤT 1,04; bốn ẢO ẢNH lục lướt xuyên qua đối thủ (ngang 1,10; chéo xuống 1,34; bổ dọc 1,58; chéo lên 1,80); hiện lại chỗ cũ 2,14; tra kiếm "cạch" 2,64 | rut; bien; chem ×4; hien; trung 2,64 (đóng kiếm); vet ×6 |
| hit | 0,5 s | nguyên hit_01 | |
| die | 1,55 s | die_01 (bật ngửa rồi đổ sấp), mờ dần | nga 0,55 |

- **Ảo ảnh** là ảnh chụp chính rig này ở dáng chém của `skill_4_1..4` (thân đứng tại chỗ), nhuộm lục, 0,62 px / đơn vị; mỗi ảnh trên một xương
  con của `far`, lướt nhanh dần theo một hướng, nhạt dần (độ đậm tối đa 0,78). Game khai `far = [skill]`, `stay = [skill]`, `lunge = [cast]`.
- **Vết chém** (lúc ảo ảnh lướt qua và lúc "đóng kiếm thì đối thủ bị chém liên tục từ các vết trước") là việc của lớp VFX: rig chỉ đặt sự kiện
  `chem` (kèm tên ảo ảnh), `trung` (cạch), `vet` ×6 cách nhau 0,07 s và xương `vet_a..d` (chỗ + hướng). CHƯA làm VFX.
- Khung trúng của chiêu cuối đặt ở lúc ĐÓNG KIẾM (2,64 s); muốn đối thủ dính đòn ngay từ ảo ảnh đầu thì đổi `trung` của clip `skill`.

Xem: `inbox/kiem_si_1/rig/xem.html` (runtime Spine thật, nút từng clip); tờ khung `rig/khung_<clip>.png`; ảnh runtime thật `rig/that/`, `rig/that_can/`.

## 7. Việc tiếp

1. Người dùng xem rig và clip (bản 2, sau mục 8), dặn sửa.
2. VFX: vệt chém của ảo ảnh và chuỗi vết chém nổ lại lúc đóng kiếm; bụi lá lúc đáp đất; vệt lá lúc biến mất.
3. Chớp mắt (chưa có mảnh mắt nhắm); dạng thứ hai nếu người dùng muốn.
4. Vào game: tên, id, suất thứ 8 đảo Mộc (ải 50), chỉ số, thẻ do người dùng đặt; chép `.atomik` + chân dung vào `Assets/03 Art/Heroes/Resources/`.

## 8. Người dùng trả bản rig đầu (2026-11-12) và cách sửa

Kèm ba ảnh chụp trang xem (trúng đòn, idle, đánh thường):
- "trúng đòn lỗi **bị hở ở giữa**, **giáp tay phải lệch hẳn khỏi tay**"; "idle giáp tay phải cũng **lơ lửng không gắn vào tay**";
- "**tay trái chưa ôm vào bao kiếm**";
- "con này khó, **mổ xẻ kĩ con gốc và xem mọi part của nó**"; "đánh thường cũng bị hở ở giữa, **phần body tôi nghĩ nên gen đầy đủ không bị hở**".

Nguyên nhân (nhận định của Claude sau khi mổ): tôi thấy mọi hình của họ bám một xương nên làm kiểu "mảnh cứng đặt theo concept" như tượng đá
(mục 25 của skill), và chỉ có MỘT mảnh thân nhỏ + hai bắp tay mảnh nấp sau thân. Nhưng con gốc không phải các mảnh lơ lửng: thân của nó
dựng từ nhiều khối lớn chồng nhau lấp kín hình bóng, và bắp tay to mới là thứ nối tấm vai với bao tay.

Tờ mổ từng part: `kiem_si_mo.py` → `<SXS>/scan/monster_3620/mo/idle0_0..2.jpg` (mỗi ô = cả con mờ + một part tô đậm, ghi slot, xương, cỡ).
Cấu trúc thân của họ (sau → trước):
| part của họ | xương | là gì, phủ chỗ nào | của mình |
|---|---|---|---|
| `P_ke` | bone33 | bầu dục xám trên lưng, giữa tấm vai gần và mũ | `kp_gu`: gù lưng lông |
| `P_keR` | bone31 | nửa cánh cứng TO phía sau-trái, từ đỉnh lưng xuống gần đất | `kp_ao`: áo tơi lá (quạt lá sẫm đúng hình nửa đĩa) |
| `P_keL` | bone32 | nửa cánh cứng TO phía phải, sau đầu và tay xa | `kp_lung`: mảng lưng lông |
| `P_shenti1` | bone3 | bụng nhỏ ở đáy | `kp_bung`: bụng lông (dưới váy) |
| `P_shouL2_2`, `P_shouL1` | bone18 | khuỷu tròn + BẮP TAY XA to (dưới tấm vai xa, nối xuống bao tay) | `kp_khuyu_x`, `kp_bap_x` |
| `P_shenti2` | bone5 + bone3 | KHỐI NGỰC tròn rất to ở giữa (sau đầu, sau giáp ngực) | `kp_than` |
| `P_tou2` | bone5, 6, 7 | gáy / áo trùm nối đầu với ngực | `kp_co`: gáy lông |
| `P_shouR2_2`, `P_shouR1` | bone22 | khuỷu + BẮP TAY GẦN to (dưới tấm vai gần) | `kp_khuyu_g`, `kp_bap_g` |
| bàn tay: `R3_3`, `R3_4` SAU kiếm; `R3_2`, `R3_1` TRƯỚC kiếm (tay xa: `L3_4`, `L3_3` sau; `L3_2`, `L3_1` trước) | bone24 / bone20 + ngón | hai lớp kẹp thanh kiếm ở giữa | nắm tay hai lớp (dưới) |

Sửa:
- **Thân gen đủ theo ĐÚNG KHUNG part** (`kiem_si_part.py to | cat`, tờ `M_P`, gói `luot_3_khung_part.txt`): mười part trên mỗi part một ô đúng khung
  ảnh vùng của họ, hình bóng kín tô phẳng màu lông (riêng `P_keR` màu lá + gân lá toả từ đầu trên), Codex vẽ lại sạch giữ hình bóng: IoU
  0,95–0,98 ngay lượt đầu. Rig (`gan_khung`): đặt bằng affine ảnh vùng → thế giới của chính part đó, bám đúng xương của nó (một xương: ô
  cứng; nhiều xương: lưới 5 × 5 lấy trọng số các đỉnh lưới của họ). Bỏ mảnh thân cũ, hai bắp tay cũ, chuỗi áo tơi tự dựng; giữ lại xương
  `bone31`, `bone32` (cánh cứng).
- **Tấm vai xa**: không đổi chỗ; nay có bắp tay xa to nằm dưới nối xuống bao tay nên hết lơ lửng (trúng đòn: tấm vai nằm dọc theo cánh tay).
- **Nắm tay ôm kiếm** (`NAM`): tâm nắm tay đặt lên sống giữa thật của ảnh vỏ kiếm (tay gần) / chuôi kiếm (tay xa) ở chỗ gần tâm bàn tay của họ
  nhất, thanh nắm trong ảnh xoay trùng trục kiếm, các ngón quay xuống. Hai lớp như của họ: cả nắm tay vẽ SAU kiếm, nửa ngón tay (`*_n`, có
  nét mực dọc mép cắt) vẽ TRƯỚC kiếm → kiếm luồn giữa lòng bàn tay và các ngón.
- Sau khi sửa: 62 xương, 53 slot, 662 đỉnh; `.atomik` 500 KB (sát trần 0,5 MB). Đã soi runtime Spine thật: `rig/that_can/hit.jpg`,
  `idle.jpg`, `attack.jpg`, cận hai bàn tay `rig/that_can2/idle.jpg`: không còn hở giữa ở trúng đòn / đánh thường / chiêu mana.

## 9. Lượt sửa thứ hai (2026-11-12)

Người dùng (kèm hai ảnh: dáng giơ kiếm của chiêu mana, dáng rút hai kiếm của chiêu cuối): "**chân phải hở rồi, phần hông phải**"; "chiêu cuối khi
chuẩn bị đánh thì **đuôi bị lỗi, hở to luôn**".

- **Hông phải hở**: phần thân dưới chỉ có mảnh bụng nhỏ theo khung `P_shenti1` (bụng bọ), còn váy của mình rộng hơn; lúc hai tay giơ lên, bao tay
  không che nữa thì mép trên bên phải của váy chìa ra, phía trên nó là nền. Sửa: thêm slot `hong` = mảnh thân lông đặt theo concept (ảnh `than`
  của tờ `M_D`), nửa trên theo ngực `bone5`, nửa dưới theo hông `bone3`, vẽ sau hai chân và bụng, trước khối ngực: nối ngực với váy và hai chân.
- **Đuôi hở**: đuôi bám xương hông `bone3` nhưng gốc đuôi trên concept nằm tận sau tấm vai gần (cách hông ~300 px); lúc thân chúi xuống các mảnh
  lưng dạt đi, gốc đuôi chìa ra lơ lửng. Sửa: chuỗi đuôi bám cụm lưng trên `bone33` (đúng chỗ chùm lông `P_shengzi_da1` của họ bám): gốc đuôi
  luôn nấp sau gù lưng / áo tơi.
- Ảnh ảo ảnh thu còn 0,50 px / đơn vị để file về 500 KB (thêm mảnh hông thì vượt trần 524 KB).
- Đã soi runtime Spine thật: `rig/that_can3/cast.jpg` (1,05–1,35 s), `rig/that_can4/skill.jpg` (0,5–0,9 s); bộ vẽ Python: `rig/khung_attack.png`,
  `khung_die.png`, `khung_walk.png`.

## 10. Lượt sửa thứ ba (2026-11-12)

- Người dùng: "**phần quần/váy chưa khớp lúc chém**". Mép trên của váy trên concept ở y = 795, cách đai thừng ~100 px và nấp sau hai bao tay; lúc
  tay giơ lên chém thì váy lộ ra như một vạt rời treo lửng dưới nút thừng. Sửa: kéo dài váy lên (`VAY_TREN = 662`) cho mép trên chui dưới đai
  thừng, chuỗi váy bản lề ở đai (`VAY_J`); dáng nghỉ không đổi (phần kéo dài nấp sau bao tay). Soi: `rig/that_can5/cast.jpg`.
- Người dùng: "**chiêu cuối đuôi vẫn hở**". Bám `bone33` chưa đủ: lúc rút hai kiếm, áo tơi (`bone31`) lật lên như cánh, tấm vai dạt đi, đầu gốc
  đuôi thò ra dưới mép áo tơi (soi cận mới thấy: `rig/that_can9/skill.jpg`; tờ khung nhỏ lượt trước tôi nhìn sót). Sửa: đuôi bám CHÍNH xương áo
  tơi `bone31`; khớp gốc đuôi nằm trong lòng mảng áo tơi (script in ra "TRONG mảng áo tơi") nên bị áo tơi che ở mọi dáng; lúc áo tơi lật lên
  thì đuôi vung theo ra sau đầu (0,36–0,9 s đuôi khuất sau mũ và thân).
- `.atomik` 501 KB.

## 11. Lượt sửa thứ tư (2026-11-12)

Người dùng (ảnh cận bàn tay gần): "**tay trái ôm kiếm bị lỗi nằm dưới kiếm**". Cách hai lớp của mục 8 (cả nắm tay sau kiếm + nửa ngón tay trước
kiếm) chỉ che nửa dưới vỏ kiếm; ở cỡ thật trông như vỏ kiếm nằm đè lên bàn tay. Sửa: bỏ lớp `*_n`, CẢ nắm tay vẽ TRƯỚC kiếm (tay xa ngay sau các
slot kiếm, tay gần sau mũ như cũ); tâm nắm tay vẫn nằm trên sống giữa vỏ / chuôi kiếm nên kiếm chui qua lòng nắm tay, ló ra hai bên (miệng vỏ ở
bên phải nắm tay gần; kiếm cách và đầu chuôi hai bên nắm tay xa). 62 xương, 52 slot; `.atomik` 498 KB. Soi: `rig/that_can2/idle.jpg`.

## 12. Lượt sửa thứ năm: bàn tay hai mảnh như con gốc (2026-11-12)

Người dùng: "**phần bàn tay không ôm vào kiếm, bạn xem con gốc nó làm thế nào sửa lại đi**" (bản cả nắm tay phủ lên kiếm của mục 11 cũng bị trả).

Mổ cận bàn tay con gốc (`<SXS>/scan/monster_3620/mo/tay_idle0_0..2.jpg`):
- Tay XA (trên chuôi): cổ tay ở phía TRÊN chuôi; `P_shouL3_4` (lòng bàn tay, bầu dục) và `L3_3` (một ngón) vẽ SAU kiếm; `L3_2`, `L3_1` là hai ngón
  dài vẽ TRƯỚC kiếm, vắt từ trên xuống NGANG QUA cả chuôi, đầu ngón thò xuống dưới.
- Tay GẦN (trên vỏ): `R3_3`, `R3_4` (ngón) SAU vỏ kiếm, ló ra phía trên và dưới; `R3_2` (khối lòng bàn tay) và `R3_1` (ngón) TRƯỚC vỏ kiếm.
→ Điểm chung: kiếm bị KẸP giữa hai lớp của bàn tay và có ngón vắt ngang qua trọn bề dày kiếm.

Sửa: gen tờ `M_T` (`build_kiem_si.py tay` → `luot_4_ban_tay.txt`): hai bản BỐN NGÓN (dọc, khớp trên, đầu ngón dưới) + hai bản LÒNG BÀN TAY có ngón
cái; cắt bằng `kiem_si_manh.py tay` (làm đậm nét mực 5 px vì mảnh vẽ to rồi thu ~0,3 lần). Rig (`TAY2`): với mỗi tay, chỗ nắm = điểm trên trục kiếm
gần tâm bàn tay của họ nhất, lấy sống giữa và bề dày thật của ảnh kiếm ở đó; **lòng bàn tay** (`long_g/x`) vẽ SAU kiếm, lệch về phía cổ tay (gốc
xương bàn tay); **bốn ngón** (`ngon_g/x`) vẽ TRƯỚC kiếm, vắt ngang: dài = bề dày kiếm + 16 px khớp nhô phía cổ tay + 30 px đầu ngón thò bên kia.
Tay xa: cổ tay phía trên → ngón vắt xuống; tay gần: cổ tay phía dưới vỏ kiếm → ngón vắt lên. Bỏ hai nắm tay một cục của tờ `M_C`.
62 xương, 54 slot; `.atomik` 507 KB. Soi runtime thật: `rig/that_can2/idle.jpg` (cận, 0 s và 2,7 s), `rig/that_can10/*.jpg`.

## 13. Lượt sửa thứ sáu: bàn tay TÁCH NGÓN đúng khung part của con gốc (2026-11-12)

Người dùng (ảnh idle của bản mục 12): "**lỗi nặng**"; rồi gửi ảnh con gốc: "**họ tách móng/ngón tay ra, bạn có thể học hỏi cách này**".
Bản mục 12 (lòng bàn tay + hàng bốn ngón tự vẽ) trông như hai cái lược dựng đứng kèm cục lòng bàn tay rời; tay gần như thò từ dưới bụng lên, không
nối với bao tay. Tự chế cách kẹp là sai hướng.

Sửa: dùng ĐÚNG tám part bàn tay của họ, mỗi part một mảnh của mình vẽ đúng khung (`kiem_si_part.py to Q | cat Q`, tờ `M_Q`, gói
`luot_5_khung_tay.txt`; phóng 4,6 lần; IoU 0,97–0,99; làm đậm nét mực 6 px trước khi thu):
| của họ | xương | lớp | của mình |
|---|---|---|---|
| `P_shouL3_4` | bone20 | lòng bàn tay XA, SAU kiếm | `kp_l34` |
| `P_shouL3_3` | bone26 | một ngón, SAU kiếm | `kp_l33` |
| `P_shouL3_2`, `L3_1` | bone27, bone25 | hai ngón dài vắt qua chuôi, TRƯỚC kiếm | `kp_l32`, `kp_l31` |
| `P_shouR3_3`, `R3_4` | bone30, bone28 | hai ngón tay GẦN, SAU vỏ kiếm | `kp_r33`, `kp_r34` |
| `P_shouR3_2` | bone24 | khối lòng bàn tay GẦN, TRƯỚC vỏ kiếm | `kp_r32` |
| `P_shouR3_1` | bone29 | một ngón nằm trên vỏ kiếm, TRƯỚC | `kp_r31` |
Giữ lại sáu xương ngón (bone25–30) của họ nên ngón cử động theo clip của họ (xoè lúc chết, nắm lúc rút kiếm). Thứ tự vẽ theo đúng slot của họ.
Bỏ `TAY2` (tờ `M_T`). 68 xương, 58 slot; `.atomik` 501 KB. Soi runtime thật: `rig/that_can2/idle.jpg` (cận), `rig/that_can11/*.jpg`.
