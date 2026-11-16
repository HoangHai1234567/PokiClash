# Robot hủy diệt cổ đại (`robot_co`): tướng 7 đảo Kim

Bắt đầu 2026-11-16 (máy ổ C). Con gốc của rig: **`monster_3613`** (golem robot cổ giáp vàng cát nhìn thẳng, chỏm đầu chữ T có lưỡi chẻ,
mặt nạ vàng hình chìa khoá quanh một mắt đỏ, hai tấm giáp ngực cong ôm lõi tròn, sừng đen cong trên vai, năm dải vải đỏ hoa văn mạch ở eo,
cẳng tay tròn to, hai nắm đấm ba ngón chống đất, chân ống ngắn sẫm; game tham khảo, kho `D:\Ripper\SwordxStaff`), **do người dùng chỉ**
(ảnh chụp trang xem, clip `hit_02`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công
khai. Hình là của mình. Suất 7 đảo Kim = ải 40, id game hiện là **`thiet_phu`** (Thiết Phủ). Mã làm việc `robot_co`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-16)

- "làm tướng thứ 7; concept **robot hủy diệt từ thời cổ đại**".
- appear: "**các bộ phận bay bezier vào**".
- idle / walk: "**làm giống họ**".
- Đánh thường: "**dơ 1 tay phải lên, tụ 1 quả cầu năng lượng kiểu dragonball rồi bắn, tay bị giật lại như skill_01**".
- Chiêu mana: "**đưa 2 tay lên trời, xoay lòng bàn tay liên tục tụ 1 quả cầu năng lượng to hơn rồi ném xuống đầu đối thủ, impact lớn,
  nặng**".
- Chiêu cuối: "**làm giống skill_04, mở mặt ra có lõi tên lửa lục giác, phóng các tên lửa ra bay random theo đường cong bezier kiểu homing
  missile vào đối thủ, impact nặng, nổ lớn**". Claude hiểu "mở mặt ra" = mở hai tấm giáp ngực như `skill_04` (lõi lục giác nằm sau đó). Chưa
  hỏi lại.
- die: chưa dặn (con gốc có `die_01`: gục, mặt nạ rơi, mắt tắt).
- Lượt đầu người dùng dán nhầm ảnh `monster_3428` (con gốc tướng 6) rồi ngắt, gửi lại ảnh `monster_3613`.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3613/`: `info.json`, `att_goc.json`, `att_idle0.json`, `khung/`, `mo/`, `parts/`; script
`robot_co.py` mo / nhom / part_goc)

65 xương, 38 slot (36 hình bật ở idle 0), 12 clip, 3 833 khoá. Ràng buộc: **4 IK** cho hai CHÂN: `R1` (`bone40`/`bone41`, bend 1) + `R2`
(`bone42`), `L1` (`bone43`/`bone44`, bend −1) + `L2` (`bone45`); đích `R1`/`R2`, `L1`/`L2` là con của `bone` (dưới đất). Không transform, path,
physics. Có `_DrawOrderTimeline` ở skill_01..04. Con NHÌN THẲNG (gần đối xứng). Tên slot `R` = bên TRÁI hình, `L` = bên PHẢI hình.
**Chân mang tên `shou` (tay)**: `P_shouR2_2`/`P_shouL2_2` là ống chân sẫm có tấm giáp bên ngoài + nón đỏ trên đỉnh (xương IK), `_22` là hai
ngón chân. Gần như mọi hình bám MỘT xương (mảnh cứng); chỉ năm dải vải là lưới trọng số theo chuỗi xương. Ảnh mẫu `mau/goc_ca_con.png`
1536 × 1024: 0,746 px / đơn vị.

Cây xương chính: `root` → `bone` → `bone2` → `bone3` → `bone4` (THÂN: `P_shenti` cả đầu + cổ + thân dưới, `P_shenti2` nắp mắt tắt) →
`bone39` (MẶT NẠ `P_tou1`), `bone5` (LÕI tên lửa `P_wuqi1`) → `bone6` / `bone7` (GIÁP NGỰC trái / phải hình + giáp vai nhỏ `P_jianjia*`),
`bone5` → `bone40..42` / `bone43..45` (CHÂN, IK). `bone4` → `bone8` → `rotate_01` (vai phải hình: sừng `P_shouL1_2`) → `bone10` (CẲNG TAY phải
hình `P_shouL2_1`) → `bone24` → `bone18..23` (ba NGÓN, mỗi ngón hai đốt). `bone8` → `bone26` → `rotate_02` (giáp vai phải hình
`P_shouL1_1`, `_3`). `bone4` → `bone27` → `bone28` (vai trái hình: sừng `P_shouR1_3`) → `bone29` (CẲNG TAY trái hình `P_shouR2_1`) → `bone30`
→ `bone31..36` (ba ngón). `bone28` → `bone37` → `bone38` (giáp vai trái hình `P_shouR1_1`, `_2`, `_4`). `bone4` → `bone11` → `bone12..17` +
`b/c` (chuỗi dải vải). `bone` → `bone9` (mặt nạ RƠI ở die: bản thứ hai của `P_tou1` bám xương này).

| thứ tự vẽ | slot | ảnh vùng (px) | là gì | xương |
|---|---|---|---|---|
| 1 | `P_butiao4` | 39×133 | dải vải hẹp ngoài cùng trái (sau) | bone11 + chuỗi bone16 |
| 2, 3 | `P_shouR2_3`, `P_shouR2_2` | 67×42, 131×187 | CHÂN trái hình: hai ngón chân, ống chân (giáp ngoài + nón đỏ) | IK R2 / R1 |
| 4, 5 | `P_shouL2_3`, `P_shouL2_2` | 80×51, 143×180 | CHÂN phải hình | IK L2 / L1 |
| 6 | `P_shouL1_3` | 144×176 | giáp vai phải hình, lớp SAU | rotate_02 |
| 7 | `P_shouR1_4` | 161×193 | giáp vai trái hình, lớp SAU | bone38 |
| 8, 9 | `P_jianjiaR`, `P_jianjiaL` | 111×139 | hai giáp vai nhỏ sát cổ (khuất sau giáp ngực) | bone7 / bone6 |
| 10 | `P_shouL1_2` | 117×264 | SỪNG đen cong vai phải hình (+ tấm bọc vàng, nón đỏ) | rotate_01 |
| 11 | `P_shenti` | 357×440 | THÂN: chỏm chữ T + lưỡi chẻ, MẮT đỏ, cổ lỗ tròn, cổ áo hoa văn, thân dưới sẫm có hai răng vàng | bone4 |
| 12 | `P_shenti2` | | (ẩn) nắp tròn sẫm che MẮT: mắt tắt ở hit, block, die | bone4 |
| 13 | `P_wuqi1` | 103×93 | LÕI TÊN LỬA lục giác, 7 đầu đỏ (bản `P_wuqi2`: 7 ống rỗng, ở die và skill_04) | bone5 |
| 14–16 | `P_butiao3`, `_2`, `_1` | 41×133, 103×198, 39×133 | ba dải vải (giữa rộng) | bone11 + chuỗi |
| 17, 18 | `P_xiongjiaR`, `P_xiongjiaL` | 171×181, 117×173 | GIÁP NGỰC trái / phải hình, khuyết tròn ở mép trong (lộ đầu tên lửa giữa) | bone7 / bone6 |
| 19 | `P_tou1` | 115×220 | MẶT NẠ chìa khoá có lỗ tròn quanh mắt (bản rơi ở die bám `bone9`) | bone39 |
| 20 | `P_shouL1_1` | 128×187 | giáp vai phải hình, lớp TRƯỚC | rotate_02 |
| 21–23 | `P_shouR1_3`, `_2`, `_1` | 151×285, 31×103, 179×197 | SỪNG vai trái hình, mép giáp, giáp vai trái hình lớp trước | bone28 / bone38 |
| 24 | `P_shouR2_1` | 174×169 | CẲNG TAY trái hình (vỏ tròn, ổ nắm đấm vòng đỏ) | bone29 |
| 25–30 | `P_shouR3_*` | ~50×50 | ba NGÓN trái hình, mỗi ngón 2 đốt (a, b) | bone31..36 |
| 31 | `P_shouL2_1` | 148×178 | CẲNG TAY phải hình | bone10 |
| 32–37 | `P_shouL3_*` | ~50×50 | ba ngón phải hình | bone18..23 |

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho (dự kiến) |
|---|---|---|---|
| `idle_01` | 2,00 | thở nặng, nắm đấm chống đất nhún | **idle** (giống họ) |
| `run_01` | 1,33 | nhún bước, tay đánh đất luân phiên | **walk** (giống họ) |
| `skill_01` | 2,00 | tay PHẢI hình vươn thẳng ra trước (0,22–0,89, nắm đấm chĩa tới), giật về (1,11), về | nguồn **attack** (giơ tay tụ cầu, bắn, giật) |
| `skill_02` | 2,00 | hai tay bắt chéo trước ngực (0,22–0,89), dang rộng (1,11–1,33), quật xuống, về | |
| `skill_03` | 2,00 | HAI TAY GIƠ THẲNG LÊN TRỜI (0,44–0,89), giữ, đập xuống (1,11), về | nguồn **cast** (hai tay lên trời tụ cầu, ném xuống) |
| `skill_04` | 2,00 | đứng thẳng lên, HAI TẤM GIÁP NGỰC MỞ lộ LÕI lục giác (0,22–1,33), khép lại (1,56), ngồi về | nguồn **chiêu cuối** (mở ngực, phóng tên lửa) |
| `die_01` | 1,00 | gục xuống, MẶT NẠ RƠI (bản `P_tou1` trên `bone9`), mắt tắt, lõi rỗng | **die** |
| `hit_01..03`, `block_01`, `stun_01` | | mắt chớp tắt (`P_shenti2`) | **hit** = hit_01 |

Ghi nhớ cho rig: đầu, mắt, chỏm đều nằm trong MỘT mảnh thân cứng (`P_shenti`), mặt nạ là mảnh riêng có lỗ (rơi ra ở die). Lõi lục giác nấp
SAU hai tấm giáp ngực; lúc nghỉ chỉ lộ đầu tên lửa giữa qua lỗ tròn. Các bộ phận gần như đều là mảnh cứng một xương → appear "bay bezier vào"
làm được bằng cách cho từng xương mảnh bay theo đường cong về chỗ.

## 3. Concept lượt 1 (Claude đề xuất ba hướng, CHỜ người dùng chọn)

Gói `gui_gpt/robot_co_1/` (`robot_co_da.py ca_con`, `concept`; mô tả từng mảnh và ba hướng ở `robot_co_huong.py`). Ảnh mẫu 1 = hình cả con
gốc `mau/goc_ca_con.png` (khung 0 idle); ảnh 2 = sói giáp sắt (tướng 6 đảo Kim: nét, tô kim loại phẳng); ảnh 3 = golem lõi lửa (thân golem to,
nắm đấm to, tô phẳng). Mọi hướng giữ dáng nhìn thẳng, ngồi thụp, đầu nhỏ giữa hai vai cao, một mắt tròn, mặt nạ có lỗ, hai tấm giáp ngực gặp
nhau quanh lỗ tròn (lõi tên lửa ở sau), năm dải vải eo, cẳng tay tròn to, hai nắm đấm ba ngón chống đất, chân ống ngắn; đổi dáng mảnh nhận diện
(chỏm đầu, mặt nạ, gai vai) và chất liệu, màu:
- `tai_ve/L1_A.png` **đồng thau cổ phủ gỉ xanh**: chỏm miệng vạc hai quai vuông, mặt nạ khiên đáy nhọn gờ mày, gai vai lưỡi rìu đồng cổ, giáp
  ngực hoa văn xoắn vuông, vải xanh mòng két, đinh đồng thay nón đỏ, mắt đỏ cam.
- `tai_ve/L1_B.png` **thép đen + vàng kim + xanh lam kiểu Ai Cập cổ**: mũ trùm pharaoh hai vạt sọc vàng – lam, mặt nạ vàng hẹp có chòm cằm dài,
  gai vai cánh chim ưng ba bậc, giáp ngực thành vòng cổ sọc, vải lam viền vàng, nón vàng, mắt đỏ.
- `tai_ve/L1_C.png` **sắt cổ gỉ sét, cỗ máy chiến tranh có ống xả**: mũ vòm một vây sống, mặt nạ vuông hàm lưới bốn khe, mỗi vai hai ống xả,
  giáp tán đinh to, dải da nâu sẫm, gai sắt thay nón đỏ, mắt vàng hổ phách.

Ba ảnh đạt lượt đầu, không bị từ chối (91 / 157 / 88 s; lệnh A chờ khoá Codex 12 phút vì phiên khác đang gen). GPT vẽ to hơn con gốc ~13 %; co
về cùng cỡ thì độ khớp hình bóng A 0,82 / B 0,86 / C 0,84 (`robot_co_so.py` → `mau/_so_goc_co.png`), lệch ở chỏm đầu và gai vai (cố ý đổi
dáng, mảnh cứng một xương). Soát: cả ba nhìn thẳng, một mắt tròn có chấm sáng, mặt nạ là mảnh riêng quanh mắt, hai giáp ngực gặp nhau quanh
lỗ tròn, hai nắm đấm ba ngón chống đất, chân ống sau cẳng tay, tô phẳng không bóng. A: mặt nạ vẽ thành khối vuông (dặn khiên đáy nhọn), năm
dải vải gần như liền một tấm. B: mũ trùm làm đầu to hơn con gốc. C: nhiều đinh tán hơn mức chi tiết con gốc một chút. Trang xem
`inbox/robot_co_xem_concept.html`. **Người dùng chọn C** (2026-11-16) → `tai_ve/L1_duyet.png`.

## 4. Kế hoạch clip (dự kiến, làm sau khi chốt concept)

| clip | nguồn | ý |
|---|---|---|
| idle | idle_01 | giống họ |
| walk | run_01 | giống họ |
| appear | dáng idle 0 | từng mảnh (thân, mặt nạ, giáp ngực, vai, sừng, cẳng tay, ngón, chân, vải) bay từ ngoài vào theo đường cong bezier lệch nhịp, khớp vào chỗ, mắt bật sáng, nhún nặng |
| attack | skill_01 | giơ tay phải hình lên, lòng nắm đấm tụ cầu (VFX bám xương ổ nắm đấm `bone24` / `bone10`), đẩy tay ra bắn (`ban`), tay giật lùi như skill_01; đạn do code bay |
| cast | skill_03 | hai tay giơ lên trời, ngón xoay liên tục quanh ổ (đốt ngón `bone18..23`, `bone31..36` quay), cầu to tụ trên đầu (VFX), ném xuống (`nem`), code thả cầu xuống đầu đối thủ, impact nặng (rung) |
| skill | skill_04 | đứng lên, hai giáp ngực mở, lõi lục giác (đầu đỏ), phóng từng tên lửa (`phong` × 7, mỗi lần một đầu tắt → `P_wuqi2`), code cho tên lửa bay bezier ngẫu nhiên kiểu homing tới đối thủ, nổ lớn; khép ngực |
| hit | hit_01 | mắt chớp tắt |
| die | die_01 + mờ dần | mặt nạ rơi |

## 5. Rig thử bằng DA GỐC (`robot_co_rig.py`, `RC_GOC=1` → `inbox/robot_co_1/rig_goc/`, không theo git; dựng trong lúc chờ concept)

78 xương (65 của họ + `move`, `far`, `mieng`, `mat`, `cau_tay`, `cau_tay_t`, `ong_0..6`), 54 slot (38 của họ, 10 bản slot di động, 7 đầu
đạn `dau_k`), NGUYÊN lưới của họ.

- **Thứ tự vẽ đổi trong clip** (skill mục 28): sừng + giáp vai sau của tay trái hình (`P_shouR1_4/3/2`) ra SAU thân ở skill_03, skill_04;
  cẳng tay phải hình + ngón ra sau thân ở skill_01 khung 41–50. Mỗi slot di động hai bản, bật theo thứ tự vẽ của họ từng khung.
- **`skill_01` của họ là cú TAY TÊN LỬA**: từ 1,03 s cẳng tay phải hình bị ẩn (bay đi do code của họ), xương cẳng tay thụt ngược vào vai,
  1,37–1,67 lắp lại từ sau thân. Đòn thường của mình KHÔNG dùng đoạn đó: sau lúc bắn chuỗi tay giữ dáng duỗi + cú giật (bắp tay hất 9°,
  cẳng tay thụt 75 đơn vị như pít-tông) rồi hoà về dáng nghỉ; thân lùi, giáp vai bật mở vẫn theo họ. Họ quay ổ nắm đấm `bone24` đều cả clip
  (rút gọn ra 117° / khung, ba ngón cách 120° nhìn như đứng yên) → mình quay đúng 2 vòng lúc vươn + tụ.
- **Lõi tên lửa**: 7 đầu đạn cắt từ hiệu ảnh `P_wuqi1` (đủ đạn) − `P_wuqi2` (ống rỗng), mỗi quả một slot cứng trên `bone5` + xương `ong_k`
  ở tâm ống. Chiêu cuối: lõi đổi sang ảnh ống rỗng, đầu đạn tắt từng quả theo `phong`.
- **Appear**: mỗi nhóm (chân, thân, lõi, vải, cẳng tay, sừng, giáp vai, giáp ngực, mặt nạ) bay theo bezier bậc hai từ ngoài vào, lệch nhịp; vị
  trí đích tính trong thế giới rồi đổi về hệ xương cha đang bay (cha quay ít: lõi là cha của giáp ngực + chân, quay nhiều thì con lệch cung
  giữa hai khoá). Góc quay thêm giảm theo smoothstep (theo đường bay thì mặt nạ quay 200° / khung) và chọn đúng vòng theo góc mong muốn.
  Nắp mắt `P_shenti2` che mắt tới khi lắp xong, mắt chớp sáng ở 1,24 s.
- Lòng bàn tay xoay liên tục ở cast: 4 vòng tốc độ hình thang (`xoay_deu`), dừng đúng bội 360° (runtime trộn clip bằng LerpAngle nên bội
  360° nối về idle không quay ngược).
- Bộ đo `kiem`: còn bước lớn là cú giật / cú đập của chính họ (rotate_01, bone10 ~70° / khung; FK nên không lệch cung).

## 6. Mảnh (2026-11-16, `robot_co_manh.py`; gói `gui_gpt/robot_co_1/luot_2_*`, Codex đạt lượt đầu cả bảy tờ, 71–125 s mỗi tờ)

- `can`: căn concept C lên hình con gốc (IoU 0,84; a 1,135: GPT vẽ to hơn ~13 %; khoảng tìm tỉ lệ phải nới lên 1,00–1,22).
- Không có tờ thân liền: con gốc gồm các tấm giáp rời viền kín, không có bề mặt nối liền màu.
- **K1–K4** (giữ hình bóng gốc, tờ = mảnh gốc phóng 2,2–4,0): K1 giáp vai lớp sau trái / phải (mặt trong, thép sẫm), mép giáp vai, hai giáp cổ
  nhỏ | K2 hai giáp ngực, lõi tên lửa ĐỦ ĐẠN (7 đầu hổ phách) + ỐNG RỖNG, hai cẳng tay (đai đinh tán, ổ vòng hổ phách) | K3 hai chân (ống sắt sẫm,
  tấm giáp ngoài, gai thay nón đỏ), hai cặp ngón chân, bốn dải vải → dải da nâu | K4 12 đốt ngón. IoU 0,915–0,983. Mũi gai trên đỉnh lớp sau
  giáp vai trái của họ gọt bằng phép mở hình bóng (`MO`) cả ở tờ lẫn lúc cắt (giáp vai trước của mình tròn, không gai).
  `vung()` phải đọc thẳng `att_goc.json`: `nap()` chỉ giữ hình đang bật nên thiếu `P_wuqi2`.
- **R1–R3** (đổi dáng, mảnh cứng một xương, "đúng chỗ, đúng cỡ" trên concept → `manh/moi.json`): R1 thân (`P_shenti`, kèm tờ hình bóng
  `mau/huong_than.png` = thân của họ bỏ chỏm chữ T ∪ khối đầu concept; GPT phủ 99,9 %, vẽ ngoài 3,7 %; mắt tìm theo màu hổ phách → tâm + bán
  kính ghi vào `moi.json`) | R2 mặt nạ (`P_tou1`, lỗ tròn trắng ở chỗ mắt → trong suốt; bản rơi `P_tou2` cùng chỗ thế giới, bám `bone9`), giáp
  vai trước trái (`P_shouR1_1`) / phải (`P_shouL1_1`) | R3 cụm ống xả trái (`P_shouR1_3`) / phải (`P_shouL1_2`): hai ống + khối bắp tay sẫm khuất
  sau giáp vai + hai gai, thay cụm sừng + bắp tay của họ. Tâm tách mảnh = tâm part gốc sau phép căn (`tam_r`).
- Nắp mắt tắt `P_shenti2`: đĩa sắt sẫm viền mực dựng bằng mã đúng tâm + bán kính mắt của thân mình (hit, die, appear trước khi mắt sáng).

## 7. Rig + clip bản da mình (`robot_co_rig.py` → `inbox/robot_co_1/rig/`, không theo git)

78 xương, 54 slot, 450 đỉnh; `.atomik` 398 KB (ảnh mảnh hạ 0,8 px / đơn vị, `RC_PX`; 1 px / đơn vị thì 522 KB vượt trần 0,5 MB); chiều cao game
1105; mọi clip nối về khung 0 idle 0 px; appear khung đầu trống. Trang xem chạy đủ 8 clip (`mo_xe/thu_xem.py`, phải truyền đường dẫn tuyệt
đối); tờ khung runtime Spine thật `rig/that/*.jpg`; ảnh động `inbox/robot_co_1/_xem_dong.py` → `rig/dong/*.webp`; trang
`inbox/robot_co_xem_rig.html`.

Đo 60 khung/giây trên rig đã xuất (memory rig-kiem-goc-nhay) và sửa:
- **appear**: chân bị lõi (xương cha còn đang bay) kéo đi sau khi đã đáp: bỏ điều kiện "nhóm tới nơi thì thôi bù", MỌI nhóm được bù mỗi khung.
- **cast**: cú đập của họ là KHOÁ BẬC (1,000 → 1,033 s: bắp tay 140°, cẳng tay 216° trong một khung nguồn; nội suy thẳng thì bàn tay đi vòng
  xuống → lên → xuống, 560 đơn vị / khung 60). Tự vung dáng A (1,000) → dáng B (1,067) trong 0,15 s, mỗi chuỗi tay thử vòng ±360° cho hai khớp,
  chọn đường ổ nắm đấm ngắn nhất (1 495 so với 2 415 đơn vị), nhanh dần (mũ 1,3). Bước lớn nhất còn ~210 đơn vị / khung 60 ngay trước chạm.
- **skill**: đoạn 0,62–1,35 của họ (giật lùi 177 đơn vị + trả về) dồn vào 0,15 s làm tay nhảy 140 đơn vị / khung → hoà thẳng dáng giữ (0,55) sang
  dáng 1,35 trong 0,28 s.
- Còn lại: bước lớn nhất là lúc bộ phận bắt đầu bay ở appear (~237 đơn vị / khung 60, cố ý nhanh) và cú giật của đòn thường (57).

| clip | dài | sự kiện |
|---|---|---|
| idle, walk, hit | 2,00 / 1,33 / 0,50 | (của họ) |
| die | 1,45 | `nga` 0,45 |
| attack | 1,55 | `tu` 0,36, `ban` 0,84, `giat` 0,87, `trung` 1,14 (đạn bay do code, từ `cau_tay`) |
| cast | 2,48 | `tu` 0,30, `xoay` 0,30, `nem` 1,63, `trung` 2,08 (cầu to ở `mieng` giữa hai tay; rơi xuống đầu đối thủ do code) |
| skill | 2,62 | `mo_nguc` 0,25, `phong` × 7 (0,62–1,34, kèm số ống `ong_k`), `trung` 1,17, `dong_nguc` 2,05 |
| appear | 1,75 | `cham_dat` 0,52, `lap` × 13 (kèm tên xương nhóm), `mat_sang` 1,24 |

## 7b. Sửa walk tay phải (người dùng 2026-11-16: "animation nhìn chung ổn nhưng walk tay phải đung đưa bị lỗi")

Soi walk cạnh con gốc cùng khung (tô đậm riêng chuỗi tay phải hình, chấm khớp vai `rotate_01` / khuỷu `bone10`): (1) cụm ống xả R3 gắn
`rotate_01` (bắp tay) nên khi tay vung ống chĩa ngang như nòng pháo (walk xoay `rotate_01` −17…−68°); (2) khối bắp tay không chạm khuỷu → hở
giữa vai và cẳng tay. Ở con gốc khối bắp tay cũng không chạm khuỷu, chỗ hở được TẤM GIÁP VAI TRƯỚC DÀI (`P_shouL1_1`, lưỡi cong tới tận
cẳng tay) che; giáp vai trước của mình theo concept C ngắn hơn nên lộ.
- Ống xả tách thành mảnh riêng (`robot_co_manh.py tach_ong`: `tach_manh` theo tâm ống sau / ống trước / khối trên tờ M_R3, giới hạn nửa tờ
  của mỗi cụm), gắn XƯƠNG VAI (`bone8` phải, `bone27` trái; walk chỉ xoay ≤ 16°), vẽ SAU thân (chèn trước `P_shouL1_2`). Bỏ đế elip dưới chân
  ống: trông như bóng đổ, mà chân ống đã có viền mực kín theo nét mép khối.
- Bắp tay trái: phần khối của cụm R3 (`khoi_trai`, thay `P_shouR1_3`). Bắp tay phải: tờ K5 = hình bóng gốc `P_shouL1_2` BỎ SỪNG (cụm tím sẫm
  chạm mép trên ảnh vùng, `BO_SUNG`), đổi da sắt sẫm + tấm thép + hai gai, IoU 0,972, dùng lại lưới gốc.
- THANH NỐI pít-tông sắt sẫm (`them_thanh`, rộng 110 đơn vị, vạch thép dọc) từ `rotate_01` tới `bone10`: hai đỉnh trên bám vai, hai đỉnh
  dưới bám khuỷu → tự co giãn theo khớp; vẽ trước thân + giáp ngực, sau giáp vai trước và cẳng tay (lúc nghỉ bị che kín). Hiện ra ở walk,
  attack (tay duỗi), skill (đứng) như một cánh tay máy nối liền.
- Rig: 57 slot, 473 đỉnh, `.atomik` 400 KB; 60 khung/giây: walk lớn nhất 31 đơn vị / khung (ổ nắm đấm), không nhảy.
- Người dùng xem lại: "**tay vẫn lỗi**" (ảnh walk: thanh nối thành que mảnh). Thanh nối hai đỉnh dưới bám THẲNG `bone10`: cẳng tay xoay lệch
  bắp tay ~90° ở walk nên mép dưới thanh xoay theo, hình chữ nhật xoắn bẹp. Đo: khuỷu `bone10` chỉ TRƯỢT dọc trục x của `rotate_01` (walk
  252–388, skill_01 94–307), không lệch ngang → thay bằng **bắp tay máy ống lồng** (`them_tay_may`): ỐNG BỌC 150 đơn vị cứng trên `rotate_01`
  (từ trước vai 40 tới 0,78 L), CẦN PÍT-TÔNG 96 đơn vị trong ống (0,40 L → khuỷu + 34): đầu trên bám `rotate_01`, đầu dưới bám xương mới
  `pit_phai` (con của `rotate_01`, đặt ở khuỷu, không xoay; `nuong` chép độ trượt của `bone10` sang nó mỗi khung, trừ appear vì ở đó cẳng
  tay bay riêng). Hai khúc ống: hình bóng tự dựng (`TU_CHE`) → tờ K6 cho GPT tô đúng nét (đai đinh, gỉ, vân sáp), IoU 0,99; thiếu ảnh thì
  rig tự vẽ tô phẳng.
- Bản hiện tại: 79 xương, 58 slot, 477 đỉnh, `.atomik` 407 KB; `pit_phai` bám khuỷu đúng từng khung (bước bằng `bone10`).
- Người dùng tiếp: "**tôi không muốn tay phải cứ quẹt đất như thế, làm nó đung đưa nhẹ nhàng như tay trái thôi**". Tay phải hình ở run_01
  của họ quét rộng (bắp 43°, cẳng 97°, bàn 84°, cẳng trượt 136; ổ nắm đấm đi 621 đơn vị, sát đất), tay trái chỉ lệch nhẹ và nhấc khỏi đất.
  Thử: co biên độ quanh trung bình (nắm đấm vẫn sát đất vì dáng trung bình đã chạm đất), chép thẳng góc tay trái (nắm đấm sát đất), chép
  LẬT GƯƠNG (góc đổi dấu) → nắm đấm nhấc lên như tay trái. Chọn: chuỗi tay phải (bone8, rotate_01, bone10, bone24, bone26, rotate_02, sáu
  đốt ngón) = góc tay trái tương ứng đổi dấu, lệch nửa chu kỳ (so le). Đo runtime 60 khung/giây: nắm đấm phải x 310..361, y 234..305; trái
  x −270..−200, y 217..307 (đối xứng); bước lớn nhất 6 đơn vị / khung; khép vòng walk 16,7 px (trước 38).
- Moi.json trước khi tách ống lưu ở `manh/_moi_truoc_tach_ong.json`.

## 7c. DẠNG 1 NON (2026-11-16)

Người dùng: "**ok ổn rồi làm dạng 1 đi**" → như quỷ xích (lần đó hỏi lại, chọn "làm thêm dạng 1 non"): robot sắt gỉ vừa làm là **dạng 2
(dạng cuối)**, làm dạng 1 non trên CÙNG rig, cùng clip. Thư mục `inbox/robot_co_non/` (`mau`, `tai_ve`, `manh`, `rig`), xuất tên `robot_co_non`.

- Tỉ lệ trước (`RC_DANG=non py -3 -I ArtGen/Spine/robot_co_rig.py ...`): `TI_LE` giáp vai `bone26`, `bone37` × 0,82, cẳng tay + nắm đấm
  `bone10`, `bone29` × 0,88; ống xả (mảnh thêm trên xương vai) co × 0,72 quanh chân ống (`co`). Mảnh cứng (`moi.json`) tính toạ độ riêng theo
  thế giới KHÔNG đổi tỉ lệ (`Wc`) nên co cùng xương. Chưa có da non thì lấy mảnh dạng 2 (`MANH2`, từng tệp). Đầu vòm nằm chung mảnh cứng với
  thân nên không phóng bằng xương: concept dặn vẽ đầu to tròn hơn ~1,3 lần (mảnh thân gen lại). Soi walk / attack / cast / skill / die / hit
  bằng da dạng 2: ổn.
- Bố cục `mau/bo_cuc.png` (`robot_co_rig.py bo_cuc`), `mau/bo_cuc_khung.png` (`robot_co_non.py khung`).
- Concept (`robot_co_non.py concept` → `gui_gpt/robot_co_non/luot_1_concept_<A|B|C>.txt`, ảnh mẫu 1 = bố cục, 2 = concept dạng 2): giữ dáng,
  một mắt hổ phách trong mặt nạ vuông, giáp ngực ôm đèn tròn, cẳng tay thùng, ổ nắm đấm; đầu to tròn hơn; mới hơn, ít giáp, sáng màu hơn:
  - A **robot con thép mới** (thép sáng không gỉ, mỗi vai một ống, vây thành mẩu, vải bố vàng nhạt);
  - B **robot đồng thau học việc** (đồng thau + khớp sắt sẫm, ăng-ten thay vây, ống còi đồng, dải da nâu sáng);
  - C **robot gỗ đai sắt sơ khai** (tấm gỗ sáng + đai sắt đinh tán, chốt gỗ thay vây, ống phễu sắt, dây thừng).
- Ba ảnh đạt lượt đầu (97 / 103 / 109 s). Khớp bố cục sau khi co: A 0,80 / B 0,85 / C 0,85 (`mau/_so_bo_cuc.png`), lệch chủ yếu ở đầu (cố ý to
  hơn). A vẽ vải eo liền một tấm; C vẽ hai dây thừng thay bốn dải (rig vẫn có bốn dải vải: lượt mảnh sẽ chia). Trang
  `inbox/robot_co_non_xem_concept.html`. **Người dùng chọn A** (robot con thép mới) → `robot_co_non/tai_ve/L1_duyet.png`.
- Mảnh (`robot_co_non_manh.py`, dùng lại hàm của `robot_co_manh.py` bằng cách thay biến của module): phép căn concept ↔ thế giới rig non qua
  bố cục (`bo_cuc.json` + `bo_cuc_khung.json`), khớp bằng hình bóng DƯỚI CỔ (đầu concept cố ý to hơn; a 0,980, IoU 0,902). Hình bóng part ở dáng
  gốc non lấy thẳng từ rig non dựng bằng trọn da + `moi.json` dạng 2, rasterize ẢNH qua lưới (lấy ô lưới thì mảnh cứng ra hình chữ nhật).
  Lưu ý: `robot_co_rig` phải nạp TRƯỚC khi đổi `G.BASE` (rig tính đường dẫn da dạng 2 từ `G.BASE`).
  - CHUYỂN DA N1–N4: tờ = mảnh dạng 2 đã xong (thu 0,5 px / đơn vị) xếp ô; GPT tô lại thép sáng, bỏ gỉ, bớt đinh, dải da → vải bố khaki: giáp
    vai trước / sau, mép, giáp cổ | giáp ngực, lõi, cẳng tay | chân, ngón chân, bốn dải vải | khối bắp tay phải / trái, ống bọc + cần tay máy.
  - Gen đúng chỗ: R1 thân (đầu vòm to + mẩu vây, mặt trơn có mắt; tờ hình bóng `mau/huong_than.png`), R2 mặt nạ + ống xả đơn trái / phải
    (mảnh thêm trên xương vai, `co` 1,0).
  - Ngón tay: chép y dạng 2. `moi.json` non = của dạng 2 (giáp vai trước, khối bắp tay trái giữ hình bóng) + mảnh gen lại.
- R1, R2 Codex đạt lượt đầu (thân phủ 99,8 % hình bóng; mắt tìm được). Bốn tờ chuyển da N1–N4: Codex báo **hết hạn mức tới 19:01** (16:19) →
  CHUYỂN DA BẰNG MÃ (`robot_co_non_manh.py doi_mau`): ánh xạ bảng màu giữ vân sáp + nét mực (xám trung tính theo độ sáng [59, 75, 108, 145,
  165] → [75, 146, 174, 203, 219] nhuộm sắc lam thép; gỉ cam kể cả đốm hồng nhạt → thép chính giữ dao động vân; dải da → vải bố khaki #CDB98A;
  mực, hổ phách giữ). Không đổi được hình bóng: số đinh, gai trên chân / cẳng tay, mép rách của dải vải vẫn như dạng 2 (concept A ít đinh, nắp
  tròn, vải cắt nhọn). Có thể làm lại bằng GPT sau 19:01 (tờ + prompt `gui_gpt/robot_co_non/luot_2_da_N*.txt` đã có; `cat N1..N4`).
- Rig non (`RC_DANG=non`): 79 xương, 58 slot, 477 đỉnh, `.atomik` 441 KB, mọi clip nối về khung 0 idle 0 px, appear khung đầu trống; đo 60 khung
  / giây như dạng 2 (cú đập chiêu mana ~200 / khung ngay trước chạm, bộ phận bay vào ở appear ~260); trang xem chạy đủ 8 clip; ảnh động
  `robot_co_non/rig/dong/`; trang `inbox/robot_co_non_xem_rig.html`. **CHỜ người dùng xem.**

## 8. VÀO GAME (2026-11-16; người dùng: "ổn rồi, ghép vào game đi, làm thêm các fx cần thiết vì tôi chưa thấy tên lửa nào")

- Thay HÌNH suất 7 đảo Kim `thiet_phu` (ải 40 "Mỏ Sắt Ngân"); giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, số dạng (2). Tên do Claude đặt,
  người dùng có thể đổi: tướng **Thần Cơ** ("Cỗ máy hủy diệt cổ đại", "Dòng Thần Cơ"); dạng 1 **Thần Cơ Nhi** (`robot_co_1`, cỡ 0,92), dạng 2
  **Thần Cơ** (`robot_co_2`, cỡ 1,1); thẻ Rìu Bổ → **Thiên Cầu Giáng** (sun), Thiết Phủ Khai Sơn → **Hỏa Tiễn Liên Hoàn** (flame), Thân Thiếc →
  **Giáp Thép Cổ** (shield). Script `ArtGen/Spine/quai/doi_robot_co.py` (heroes/cards; `th` gộp dạng 2 bản nhẹ atlas × 0,5 + clip `evolve` vào
  rig dạng 1 → `robot_co_non_th.atomik` 569 KB, khung cuối evolve khớp idle dạng 2 lệch 0; `chep` vào `Resources/robot_co_1|2`). Resources
  `thiet_phu_*` cũ để nguyên.
- VFX `Assets/01 Script/Game/Battle/HatRobot.cs` (đường "n_", phát lúc clip bắt đầu, mốc co theo `lead`); bảng chỗ trên rig
  `HatRobotBang.cs` SINH bằng `ArtGen/Spine/robot_co_do_hat.py` (đo `cau_tay`, `mieng`, hai lòng bàn tay, `ong_0` + miệng ống ở từng phát cho cả
  hai dạng; phần chiều cao khai game; đổi clip / tỉ lệ thì chạy lại):
  - `n_robot_ban1|n_robot_ban` đòn thường: hạt hút vào ổ nắm đấm, cầu năng lượng vàng lớn dần (R 0,1 × chiều cao), hai cung điện quay, đầy thì
    nháy vòng; bắn: chớp, vòng, tia, hơi xì ở ổ lúc tay giật; cầu bay có đuôi; trúng: chớp + nổ vàng.
  - `n_robot_cau1|n_robot_cau` chiêu mana: cầu to (R 0,21) giữa hai bàn tay, xoáy cung điện ở hai lòng bàn tay + dải hạt cuốn vào cầu, hạt hút
    từ xa, sỏi bay lên, bụi xoáy, ba nhịp vòng nạp; đầu cú vung đập (1,55 s) cầu rời tay, vọt lên rồi cắm xuống đỉnh đầu đối thủ đúng khung
    trúng 2,08; nổ rất lớn (chớp, CauNo 1,6, cột năng lượng, hai vòng sóng đất, nứt đất, đá, bụi, khói).
  - `n_robot_ten1|n_robot_ten` chiêu cuối: giáp ngực mở xì hơi, vòng nháy ở lõi, than vàng bốc lên; 7 TÊN LỬA vẽ rõ (vỏ thép, mũi đỏ, đai, hai
    vây, lửa phụt, vệt khói xám; dài 0,2 × chiều cao) rời đúng ống, đúng giờ `phong`, Bézier bậc ba ngẫu nhiên kiểu homing (tầm vòng ≥ 6,5
    lần thân tên lửa để vòng cung rõ cả khi đối thủ đứng sát), quả đầu chạm đúng khung trúng 1,17; mỗi quả nổ lửa đỏ cam; sau quả cuối nổ
    rất lớn ba đợt; khép ngực xì hơi.
- Đăng ký: StageView `KimFx["thiet_phu"]`, bảng mới `AtkDang` (đòn thường theo dạng; `FireAtk(h, form)` thêm tham số dạng tuỳ chọn, AtkFx
  và HeroViewer truyền dạng), HatNuoc 6 case, HatLua `Pal["nang"]` + `Themes["thiet_phu"]`, KimFxTour hai menu Thần Cơ / Thần Cơ Nhi.
- Unity: biên dịch không lỗi; "Nhập dữ liệu" + "Gắn dạng .atomik" (robot_co_1 158 xương 9 clip có evolve, robot_co_2 79 xương 8 clip; prefab
  thiet_phu giữ 2 dạng); chạy KimFxTour cả hai dạng trong trận, soi từng khung (`Temp/PokiShots/kim_fx/thiet_phu_<1|5>sao_*`). Lần đầu tên lửa
  ngắn và bay gần thẳng (đối thủ đứng sát), lửa đuôi thành chuỗi hạt cam → tăng thân, mở tầm vòng, lửa đuôi nhỏ và tắt nhanh; cầu hai đòn to lên.

## 9. Việc tiếp

1. Người dùng xem trong game, đổi tên nếu muốn.
2. (Tuỳ) chuyển da dạng 1 bằng GPT (N1–N4) cho số đinh / mép vải đúng concept A; chưa có hạt cho `lap` / `cham_dat` của appear.
