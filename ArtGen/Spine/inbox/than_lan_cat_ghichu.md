# Thằn lằn áo choàng đất nung (`than_lan_cat`): tướng 2 đảo Thổ (ải 5)

Bắt đầu 2026-11-17 (máy ổ C, kho `D:\Ripper\SwordxStaff`). Con gốc của rig: `monster_3257` (thằn lằn sừng ngồi rạp, diềm ba tấm; game tham
khảo), Claude chọn trong năm tướng đầu đảo Thổ, người dùng duyệt. Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola):
dùng nội bộ, không đăng công khai. Hình là của mình. Suất ải 5 đảo Thổ, id game hiện là `lung_vuong`. Mã làm việc `than_lan_cat`. Tên, id,
số dạng: chưa bàn. Ghi chú chung năm con: `tho5_ghichu.md`.

## 1. Lời dặn của người dùng (2026-11-17)

- Concept: người dùng chọn **D** (lượt "gần giống con gốc"): thằn lằn giáp, đầu nêm mày giáp đá, mắt vàng, áo choàng phiến đất nung dựng sau
  đầu như mũ trùm, da vàng xám đất, bụng kem, đuôi khoanh phiến đất nung → `than_lan_cat_1/tai_ve/L1_duyet.png`.
- Animation: người dùng bảo Claude tự đề xuất dựa trên skill anim + VFX (`tho5_anim.py`), rồi "làm đi", "chia multiagent làm cùng lúc đi"
  (con này do một agent làm riêng).

## 2. Mổ rig gốc (`<SXS>/scan/monster_3257/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample_goc.json` 10 clip 30 khung/giây,
`khung/`, `manh_anh.png`)

40 xương, 23 slot, 10 clip. **5 IK** (a1..a4 chân sau / trước, b1 mix 0) đã được runtime nướng vào biến đổi riêng `l` của mẫu khung → rig
mình chỉ FK. Mắt `P_yanjing01` là hình REGION xoay 90° trong atlas (lỗi `hoa_ho.luoi` làm bẹp, sửa ở `tho5.luoi_sua`); hình phụ
`P_yanjing02` = mắt nhắm (idle chớp ở 0,5–0,67 s; hit, die nhắm). Lưỡi `P_shetou` bám chuỗi `bone31..34` (con của hàm `bone6`), hiện ở
skill_01 (0–0,85 s), skill_02 (0,4 s →), die. skill_02 đổi ba tấm diềm sang hình xoè to (`P_qi05..07`) + tỉ lệ xương diềm 1,2.

Cây xương: `bone → bone30 → bone2` (hông) `→ bone3 → bone4` (ngực) `→ bone5` (cổ) `→ bone27` (ĐẦU) → `bone6` (HÀM, gốc ở góc miệng sau;
lưỡi `bone31..34`), `bone7` / `bone8` / `bone9` (ba tấm diềm `P_qi01` / `02` / `03`), `bone10` (gai cằm `P_qi04`), `bone15` (mắt).
Chân trước gần `bone28 → bone11 → bone12` (`P_shoubi03`, `P_shoubi02`, ngón `P_shouzhi01`), chân trước xa `bone29 → bone13 → bone14`
(`P_shoubi04`, `P_shoubi01`, `P_shouzhi02`); chân sau gần `bone21..23`, xa `bone24..26`; đuôi `bone16..19`.

| clip | dài | động tác | dùng cho |
|---|---|---|---|
| `idle_01` | 4,00 | thở, chớp mắt 0,5 s | **idle** |
| `run_01` | 0,80 | bò | **walk** |
| `skill_01` | 1,00 | chồm lên thè lưỡi (0,11–0,44), phóng rạp đớp (0,56), về | **attack** |
| `skill_02` | 1,17 | xoè diềm to, há miệng rít (0,39–0,91) | **cast**, **skill**, xoè mũ ở appear |
| `hit_01` / `die_01` | 0,50 / 1,00 | | **hit** / **die** |

## 3. Mảnh (`than_lan_cat_manh.py`; gói `gui_gpt/than_lan_cat_1/luot_2_S1..S6.txt`; Codex đạt lượt đầu S1–S5, 59–77 s mỗi tờ)

"Đúng chỗ, đúng cỡ" trên concept (cách `quang_sat_manh.py`), mỗi tờ vài mảnh không chồng nhau. Ghép lại (`ghep`) IoU hình bóng với concept
**0,953**. Mảnh (tên ảnh → slot của họ ở `than_lan_cat_rig.SLOT`):
- `than` → `P_shenti`; `dau` (đầu trên, không mắt) → `P_tou`; `ham` → `P_zhui`; `mat` / `mat_nham` → `P_yanjing01` (mắt mở cắt thẳng từ
  concept: bao lồi vùng vàng từng mắt + vành mực 5 px; mắt nhắm tờ S4); `luoi` (vẽ mới ở góc trống S5) → `P_shetou` (đặt vào chỗ lưỡi
  của họ ở dáng gốc bằng khớp tâm + trục PCA + độ dài).
- Áo choàng: `ao3` (phiến trên) → `P_qi03` (`bone9`), `ao2` → `P_qi02` (`bone8`), `ao1` → `P_qi01` (`bone7`); `ao4` (phiến trên lưng) → slot
  mới `ao4`, cứng trên xương mới `ao4` (con của `bone4`). Ba phiến trên đầu là phiến bay của cast.
- Chi: MỘT mảnh liền mỗi chi, bám HỢP lưới các part của họ (đùi + cẳng + ngón): `tay_xa` → `P_shoubi01`, `chan_gan` → `P_jiao01`, `tay_gan`
  → `P_shoubi02`, `chan_xa` → `P_jiao03`. Bỏ slot các part đã gộp và gai cằm `P_qi04` (concept không có).
- Sửa sau khi cắt: (1) `ham`: GPT vẽ hàm như đang há (lòng đỏ lộ dưới đường miệng) → `tach_ham`: lòng đỏ tô kem (hàm ngậm), lòng đỏ tách
  thành `long_mieng` dời lên đúng bề cao của nó (nấp sau đầu), cứng trên xương hàm: há thì xoay theo ra khe miệng; hàm cắt ở đường cằm (mục
  4). (2) `chan_xa`: GPT chỉ vẽ
  bàn chân cụt → nhổm lên thì bàn chân nằm lại trên đất, rời thân; thay bằng ảnh `chan_gan` tối 12 % đặt vào khung chân sau xa của họ
  (`chan_xa_tu_gan`; bản GPT giữ ở `chan_xa_gpt.png`). (3) `ao2`: S4 vẽ thành dải cong mảnh, để hở mảng trắng giữa phiến trên và phiến
  thứ ba → tờ S6 vẽ lại thành phiến đặc (Codex đạt lượt đầu; IoU ghép tăng 0,953 → 0,965).

## 4. Rig (`than_lan_cat_rig.py` → `inbox/than_lan_cat_1/rig/`, không theo git)

Đủ xương của họ (trừ shadow) + `move`, `day`, `tam`, `far`, `fly_3/2/1`, `bay_3/2/1`, `mieng` (chóp mõm, con của đầu), `ao4`, `cat_x` (mặt nạ
cắt: chỉ giữ phần trên mặt đất ở appear). Mỗi mảnh là lưới phủ hình, mỗi đỉnh biến dạng như điểm tương ứng trên (hợp) lưới của họ
(`trong_so_goc`: tam giác chứa nó, ngoài lưới thì cạnh gần nhất + khoảng lệch). Phiến diềm của họ xoè rất mạnh ở skill_02 (`bone9` xoay
143°): phiến của mình là ngói xếp lớp nên giảm (`GIAM_QI`: skill_02 0,32–0,45, skill_01 0,5–0,6).

| clip | dài | nguồn | ý |
|---|---|---|---|
| appear | 1,60 | tự dựng | ẩn tới 0,12 (`troi`); đầu + mũ trùm vọt lên khỏi đất (mặt nạ cắt); hai chân trước vươn lên rồi BẤU đất (`bam` 0,56; xoay cả chi chĩa về chỗ bấu, đích đứng yên trong lúc thân được kéo lên; IK hai xương bỏ vì cẳng ngắn làm khuỷu lật 120–360°/khung); chạm đất nảy 0,95 (`ru_cat`), rũ cát (thân lắc, phiến lạch cạch trễ dần), xoè mũ một lần rồi xếp |
| idle | 4,00 | khung 0 idle_01 + sóng | MỀM (áp lời chê idle tatu "giật, không mềm mại"): dáng nền đứng yên, mọi chuyển động là sin lệch pha biên độ nhỏ: ngực nở 2 % chu kỳ 2 s, cổ / đầu trễ 0,05 / 0,10 s (đầu ±1,1°), hàm hé theo nhịp thở, phiến áo choàng trễ 0,15–0,35 s (2–2,8°), đuôi chu kỳ 4 s trễ dần từng đốt; trò nhỏ 2,45–3,55 s: nghiêng đầu 3°, chớp mắt chậm, hé hàm thè lưỡi nếm gió MỘT nhịp chậm (lưỡi chĩa sẵn khi còn ẩn, tỉ lệ đều). Đo: gia tốc góc mọi xương hiện ≤ 3,4°/khung², khép vòng 0,12 px |
| walk | 0,80 | run_01 | + phiến phập phồng |
| attack | 1,00 | skill_01 | chồm lên thè lưỡi, lao tới (`move` 0,42 cao) rạp đớp: hàm há to rồi sập đúng khung `trung` 0,56, duỗi dài 8 % đúng khung chạm |
| cast | 1,63 | skill_02 | xoè mũ trùm, rít (đầu rung hai dáng); ba phiến rời lần lượt (`phong` 0,47 / 0,53 / 0,60), xoay như phi tiêu bay tới `far` (code lái, farAim), găm, bay về lắp đúng chỗ phiến thật (`ve`); `trung` 0,68 |
| skill | 2,20 | skill_02 + tự dựng | xoè mũ, nhổm, hai chân trước nhấc cao rồi ĐẬP xuống (`dam` 0,62, IK bám đúng chỗ chân), giữ dáng rít rung tới `het` 1,78 (lốc cát là VFX ở đối thủ, `trung` 1,0) |
| hit | 0,50 | hit_01 | |
| die | 1,45 | die_01 | + bốn phiến áo choàng rời lần lượt (0,38–0,58), rơi theo trọng lực tới đất, nảy một lần, xoay quanh tâm (`roi` 0,70), mờ |

Đo góc nhảy (`kiem`): các cú xoay lớn còn lại là của chính clip họ (cú phóng đớp skill_01 0,53–0,57; chân run_01 do IK nướng; skill_02 diềm
xoè 0,33–0,37) và cú đập chân của skill (0,60–0,63, 45°).

Xuất (2026-11-17, sau khi sửa bụng): `rig/than_lan_cat_1.atomik` 196 KB (52 xương, 19 slot, 2604 đỉnh, 8 clip, 19 sự kiện, atlas 720 × 760), `xem.html`
chạy đủ 8 clip (`mo_xe/thu_xem.py`), mọi clip nối về khung 0 idle 0,00 px, appear khung đầu trống, die khung cuối trống.

Sự kiện cho VFX (giây trong clip; game: hitTimes attack 0,56, cast 0,679, skill 1,00):

| clip | sự kiện |
|---|---|
| appear | `troi` 0,12 cát nổ + gò cát; `bam` 0,56 bụi nhỏ dưới hai chân trước; `ru_cat` 0,95 chạm đất, cát rơi khi rũ |
| idle | `liem` 2,75 thè lưỡi (không cần VFX) |
| attack | `lao` 0,42 bụi sau chân lúc phóng; `trung` 0,56 vết cắn hai cung kem + cát văng |
| cast | `xoe` 0,12 cát bốc nhẹ quanh áo choàng; `phong` 0,467 / 0,533 / 0,600 (phiến 3 / 2 / 1 rời, vệt bụi sau phiến bay); `trung` 0,679 phiến đầu găm (mảnh gốm vỡ, bụi; hai phiến sau găm ở 0,733 / 0,800); `ve` 1,147 / 1,213 / 1,280 phiến lắp lại |
| skill | `tu` 0,08 cát bắt đầu xoáy quanh chân đối thủ; `dam` 0,62 hai chân trước đập đất (sóng bụi, rung); `trung` 1,00 LỐC CÁT trùm đối thủ, mảnh đất nung xoay trong lốc; `het` 1,78 lốc tan |
| die | `roi` 0,70 phiến áo choàng chạm đất (bụi) |

Soát chỗ chồng mảnh (phóng 4 lần ở idle 0, lao đớp 0,66, giữ rít 1,2, trúng đòn 0,13): hàm GPT vẽ kèm cả cổ họng (tới y 740) → hàm há
thì cả khối họng xoay như một tấm; cắt ở đường cằm (`CAM_Y`, đường cong dốc lên về mõm) + kẻ nét mực dọc chỗ cắt, cổ họng do mảnh thân lo;
vụn mực của ranh giới lòng đỏ cũ trong hàm tô kem. Không thấy dải hở hay viền đôi ở cổ, chân, đuôi.

**Người dùng chê "bụng bị lỗi"** (walk 0,2: nét mực vụn, khe hở lộ nền giữa chân sau gần và chân trước gần). Nguyên nhân: đỉnh của mình
nằm trên tam giác của các part họ khác nhau (đùi / cẳng / thân / gốc đuôi) nên nhận trọng số nhảy bậc; bước đi thì tam giác gập, viền lộn
ra giữa hình. Sửa trong `than_lan_cat_rig.py`: `lam_muot` làm mịn trọng số trên lưới của mình (thân 10 vòng, chi 8, đuôi 4) rồi gắn kiểu
LBS (điểm gắn = đỉnh trong hệ từng xương); `BO_XUONG`: thân bỏ ba đốt đuôi sau, chân sau gần / xa bỏ xương đùi (`bone21` / `bone24`: chân
của mình thấp hơn đùi của họ, phần lộ là cẳng + bàn). Soát phóng ~3 lần ở idle, 8 khung walk, attack, cast, skill, hit, appear, die: liền một
bề mặt, một đường viền, không khe, không mẩu mực. Ảnh trước / sau: `rig/_bung_truoc_sau.png`.

## 5. Việc còn lại / câu hỏi

1. Người dùng xem trang `rig/xem.html`, sửa clip theo ý.
2. VFX (lớp hạt, chưa làm): cát nổ + gò cát khi trồi (appear `troi`), bụi khi bấu / rũ cát, vết cắn + cát văng (attack), vệt bụi sau phiến bay
   + mảnh gốm vỡ khi găm (cast), sóng bụi khi đập chân + LỐC CÁT trùm đối thủ có mảnh đất nung xoay (skill), bụi khi phiến rơi (die).
3. Hỏi: thay suất `lung_vuong` (ải 5)? tên, số dạng?
