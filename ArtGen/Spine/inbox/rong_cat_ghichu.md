# Rồng giáp sa thạch (`rong_cat`): tướng 4 đảo Thổ (ải 15)

Bắt đầu 2026-11-17 (máy ổ C, kho `D:\Ripper\SwordxStaff`). Con gốc của rig: `monster_3424` (rồng bốn chân màu be cúi rạp sắp vồ; game tham
khảo), Claude chọn trong năm tướng đầu đảo Thổ, người dùng duyệt. Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội
bộ, không đăng công khai. Hình là của mình. Suất ải 15 hiện là `ho_khoan` (chưa bàn thay id, tên, số dạng). Ghi chú chung năm con:
`inbox/tho5_ghichu.md`. Làm bằng một agent riêng (người dùng: "chia multiagent làm cùng lúc đi").

## 1. Concept đã duyệt

Hướng D (`tai_ve/L1_duyet.png`): da nâu bụi, giáp sa thạch kem vạch son trên vai, cẳng tay gần và dọc sống lưng xuống đuôi, hai sừng đá dài vuốt
ra sau (thay mào sáu gai), sừng mũi pha lê hổ phách, mắt vàng đồng tử dọc, vuốt nâu sẫm. Concept "gần giống" lệch tỉ lệ con gốc (IoU 0,71).

Animation (đề xuất `tho5_anim.py`, người dùng "làm đi"): appear vuốt bấu đất kéo thân trồi lên, gầm; idle thân lắc vòng rình mồi, cào đất; attack
đứng lên chém vuốt; cast ba lưỡi cát; skill gồng, nện, cột sa thạch ba nhịp; die giáp rơi.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3424/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample_goc.json` 10 clip 30 khung/giây,
`khung/` tờ khung, `mo/idle0_*.jpg` tờ mổ từng part)

56 xương, 40 slot (39 hình bật ở idle 0), 10 clip. 8 IK (`R1/R2/L1/L2` mix 1: hai chân sau; `A1/A2/B1/B2` mix 0: tay, tắt): đã nướng trong `l`.
Hầu hết hình là lưới bám 100 % MỘT xương (mảnh cứng); lưới nhiều xương: `P_shenti02` (hông), `P_weiba` (đuôi), chân sau xa (`P_datui02`,
`P_xiaotui02`, `P_jiao02`), `P_jiao01`.

| nhóm | slot | xương | là gì |
|---|---|---|---|
| tay GẦN | `P_shoubi01`, `P_shouzhang01`, vuốt `P_zhuazi01/03/04` | bone19, bone20 (gốc ở KHUỶU, tấm cẳng to chạy xuống), 40/29/43 | giữa trái, vẽ trước thân |
| tay XA | `P_shoubi02`, `P_shouzhang02`, vuốt `P_zhuazi02/05/06` | bone16, bone17, 45/46/44 | bên phải sau đầu, vẽ đầu tiên |
| thân | `P_shenti01` (ngực, vai), `P_shenti02` (hông) | bone5; bone4/7/5 | |
| đuôi | `P_weiba`, vảy `P_linpian01/02` | bone7..10; 42, 41 | |
| chân sau gần | `P_datui01`, `P_xiaotui01`, `P_jiao01` | 11, 12, 21/22 | |
| chân sau xa | `P_datui02`, `P_xiaotui02`, `P_jiao02` | 23..26 | |
| đầu | `P_tou`, hàm `P_xiaba`, mắt `P_yanjing01` (hai hình: `P_yanjing02` mở, `P_yanjing01` nhắm) | bone13, bone14 | |
| mào | `P_qi07`(slot `P_qi01`), `P_qi08..12` | 28, 30..34 | |
| sừng | `P_jian01..03` | bone13 | |
| đá lưng | `P_shitou0/01/02/03/05/06` | 27, 38, 39, 37, 36, 35 | con của thân |

Thứ tự vẽ đổi trong skill_01 (0,50–0,83 s: tay xa ra trước ngực, vuốt xa trước đầu), skill_02 / skill_03 (tay xa, tay gần ra trước, đầu đè lên
cả hai tay). Họ đổi hình tay xa thành tấm cẳng to ở skill_02 (mình không đổi) và cho đá lưng bay đi ở skill_03 (mình giữ giáp trên lưng).

## 3. Mảnh (`rong_cat_manh.py`)

Concept lệch tỉ lệ nên làm hai bước: BỐ CỤC (`L2_bocuc`: GPT vẽ lại con của mình ĐÚNG dáng, chỗ, cỡ từng mảnh của con gốc) rồi NHÓM MẢNH
(`M_N1..N6`: mỗi lượt vài khối không chồng nhau, đúng chỗ, đúng cỡ, vẽ đủ phần khuất; ảnh 2 = bố cục có viền đỏ quanh khối cần giữ). Mặt liền màu
(thân + đuôi + chân sau gần; chân sau xa; tay xa; tay gần) gen LIỀN một khối rồi cắt theo vùng part của họ (lấn 26 px, mép cắt mờ 10 px).
Bỏ bốn gai mào thừa (`P_qi01/10/11/12`): `P_qi08`, `P_qi09` thành hai sừng dài. Mắt nhắm dựng từ mảnh mắt (`mat_nham`).

Kết quả (Codex đạt lượt đầu mọi tờ, 80–160 s mỗi tờ): bố cục `L2_bocuc` IoU 0,829 với hình bóng con gốc (giữ đúng thiết kế D). Tấm giáp, sừng,
sừng mũi tô theo VÙNG kín của bố cục (`rong_cat_manh.py vung` → `mau/_vung_lab.npy`; giáp GPT vẽ khác chỗ đá của họ): giáp → `P_shitou0/03/05/06`,
vảy → `P_linpian01/02` (hai tấm đuôi chung một mảnh); `P_shitou01/02` (chỗ đó là hai sừng) bỏ. Nhóm đặt tay `NHOM_TAY`: N1 vuốt xa, N2 tay gần +
tay xa + vảy, N3 đầu + chân xa + giáp + vuốt, N4 sừng dưới + hàm + giáp + vuốt, N5 giáp + sừng trên + sừng mũi + vuốt, N6 chân sau gần, N7 thân
+ đuôi (N1 vẽ lại BỎ chân sau gần; ở N1 chân dính liền thân, cắt theo hình bóng gốc thì ống chân rơi vào mảnh đuôi). Mắt cắt thẳng từ bố cục, mắt
nhắm dựng bằng mã (màu da đầu + nét mí). Ghép lại IoU 0,933 với bố cục.

Sửa sau khi soi dáng xa: (1) tay gần cắt tay (`cat_tay_gan`: tấm giáp cẳng riêng; phần nâu bên phải khuỷu là cánh tay; phần nâu GPT vẽ dài quá khuỷu
bỏ, không thì cục nâu xoay theo cẳng); (2) HAI CHÂN SAU tô lại trên HÌNH BÓNG part gốc (`chan_goc`: da nâu + vân sáp lấy từ thân GPT, vuốt nâu sẫm,
viền mực): mảnh GPT "đúng chỗ" của chân lệch tỉ lệ chân gốc nên dáng lao rạp (cast) chân đứt làm ba khúc; hình bóng gốc thì các khúc chồng đúng
như người vẽ gốc dựng. (3) `P_shitou0`, `P_shitou06` dời slot lên TRÊN cánh tay gần (bố cục: giáp che cánh tay).

**Người dùng chê "bụng bị lỗi rồi"** (2026-11-17, ảnh cận khung 0 idle): giữa giáp cẳng gần và chân sau gần thấy vết rách gấp khúc: đùi tô trên
hình bóng gốc có MÉP TRÊN RĂNG CƯA và viền kín, vẽ ĐÈ lên bụng (thứ tự của họ: chân gần trên thân). Thử cho mép đùi nằm trong thân không viền +
mờ dần: lúc chân bước / lao mép đó lộ ra thành vệt nhoè (bỏ). Cách giữ: ba khúc chân sau gần dời slot xuống DƯỚI đuôi và thân
(`rong_cat_rig.thu_tu_slot`), đỉnh đùi luôn nấp sau hông; bụng chỉ còn một đường viền ngoài; khúc chân viền kín, mép gọt răng cưa (mở 4 px), màu
da + vân lấy theo thân (N7). Soi cận ở idle 0, walk 0,2, attack 0,36 và skill 0,6 (đứng thẳng), cast 0,85 (lao rạp): không còn rách, không vệt nhoè.

## 4. Rig + clip (`rong_cat_rig.py` → `inbox/rong_cat_1/rig/`; `RC_GOC=1` dựng bằng da gốc vào `rig_goc/` để làm clip trước khi có mảnh)

Dáng gốc = khung 0 idle_01 (biến đổi riêng đã áp ràng buộc). Mỗi đỉnh lưới của mình biến dạng như điểm tương ứng trên lưới của họ; đỉnh nằm ngoài
lưới của họ làm trơn trọng số theo cạnh lưới mình (40 vòng). Slot di động nhân bản theo chỗ chèn (9 slot: hai tay, sáu vuốt). Thêm `move`, `cat_x`
(mặt nạ cắt mặt đất cho appear), `mieng` (con của hàm).

| clip | dài | nguồn | ý |
|---|---|---|---|
| appear | 2,10 | tự làm | thân dưới đất (khung đầu trống), chồi lên chúc mũi 26°, vuốt XA giơ lên rồi đập xuống bấu đất (0,40), IK hai đoạn giữ NGỌN cẳng tay ở chỗ bám trong lúc thân được kéo lên về ngang; vuốt gần theo thân, chạm đất 0,90 (IK vuốt gần lật khuỷu khi thân còn thấp: bỏ); rũ cát 1,22–1,50; ngẩng đầu há hàm gầm 1,60 |
| idle | 4,00 | tự làm | SÓNG MỀM trên dáng đứng (người dùng chê idle tướng 1 "giật"): thở 2 s (ngực 1 ± 1,8 %), cổ trễ 0,1 s, đầu xoay bù gần như đứng yên, hàm / giáp / sừng / vảy trễ 0,16–0,35 s, đuôi sóng 4 s gốc dẫn ngọn; cào đất chậm một lần 2,30–3,70 (sin², vận tốc vào ra 0) |
| walk | 0,67 | run_01 | khép vòng theo vòng góc (góc nướng của họ cộng dồn ±360) |
| attack | 1,15 | skill_01 | lấy đà chậm hơn, cú chém trải 5 khung (0,40–0,555), nén thân, quá đà + nảy; trúng 0,54 |
| cast | 1,55 | skill_02 | đứng dậy dang tay, gồng ngắn (hai dáng lệch), lao rạp hai vuốt quét: `chem1` 0,70 (vuốt xa), `chem2` 0,76 (vuốt gần, = giờ nhả game), `chem3` 0,84 (cả hai); `mieng` = ngọn cẳng tay gần |
| skill | 2,25 | skill_03 | giơ hai tay GỒNG 0,36–1,02 (hai dáng lệch 2–3°, phồng ngực), NỆN 1,16 (cú quay tay của họ trải ra 4 khung), giáp lưng nảy lên rồi về (họ cho đá bay đi: bỏ), cột đá `cot1..3` 1,34 / 1,56 / 1,82 (= giờ trúng) |
| hit | 0,50 | hit_01 | mắt nhắm như họ (hình `mat_nham`) |
| die | 1,55 | die_01 | khung đầu dịu lại (họ bật mạnh ngay khung 1) + bốn tấm giáp trượt khỏi lưng rơi xuống đất nảy nhẹ, mờ dần |

## 5. Kết quả, việc tiếp

Rig `inbox/rong_cat_1/rig/`: 58 xương, 47 slot (9 slot di động nhân theo chỗ chèn), 1 006 đỉnh, 8 clip, 18 sự kiện, `.atomik` 182 KB (atlas 840 ×
848, 0,62 px / đơn vị), chiều cao 700. Mọi clip về khung 0 idle 0,00 px; idle khép vòng 0,36 px; walk 38 px (bước thường 95: run_01 của họ nhanh);
appear khung đầu trống, die khung cuối trống. `xem.html` chạy (thu_xem: 8 nút clip). Tờ khung runtime thật: `rig/that/*.jpg`; soi Python
`rig/soi_*.png`. Góc nhảy lớn nhất ở 60 khung/giây (runtime thật): idle 1°, appear 15°, hit 14°, skill 32°, die 31°, cast 51°, walk 61° (của
họ), attack 77° (cú chém của bàn tay xa).

Sự kiện cho VFX (giây trong clip):
- appear: `nut` 0,05 (đất nứt dưới chân), `vuot1` 0,40 (vuốt xa đập bấu đất: bụi, đá vụn), `troi` 0,58 (đất nổ quanh thân, cát trào và rơi tới
  1,16), `vuot2` 0,90 (vuốt gần chạm đất), `ru` 1,22 (rũ cát văng hai bên tới 1,50), `gam` 1,60 (gầm: bụi bay, rung nhẹ).
- idle: `cao_dat` 3,20 (cát văng nhỏ dưới vuốt gần).
- attack: `trung` 0,54 (ba vệt vuốt màu cát + dăm đá).
- cast: `chem1` 0,70, `chem2` 0,76, `chem3` 0,84 (ba lưỡi cát trăng khuyết bay từ vuốt tới đối thủ, trúng so le); game nhả 0,76.
- skill: `gong` 0,36 (tụ: đá vụn / cát hút về hai vuốt, sừng mũi loé, tới 1,02), `nen` 1,16 (nứt đất lan tới đối thủ, bụi tròn lớn, rung),
  `cot1` 1,34, `cot2` 1,56, `cot3` 1,82 (cột sa thạch trồi quanh / dưới đối thủ, cột 3 to nhất hất tung; = giờ trúng), đá rơi nảy một lần.

Việc tiếp: người dùng xem; VFX (bản xem trước có đối thủ: Claude chính làm cho cả năm con); hỏi thay suất `ho_khoan`, tên, số dạng; vào game.
