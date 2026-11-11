# tm05: dòng Sò Ngọc (thay suất ải 20 đảo Thủy, Ma Kết, rare), ghi chú pha 1

Lô 10 tướng mới đảo Thủy, đặc tả `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`. Con gốc tham khảo: `monster_3237` (Sword x Staff), là
**dạng 1**. Làm: vẽ lại dạng 1 (thiết kế khác hẳn) + thiết kế dạng 2 (dạng cuối).

## 1. Con gốc monster_3237: mổ nhanh

Nguồn: `D:\RefAnimation\SwordxStaff\web\assets\Monster\monster_3237\` (`.skel` 22 KB, atlas 588 × 232 tỉ lệ 0,75, 89 KB);
quét `D:\RefAnimation\SwordxStaff\scan\monster_3237\info.json, mesh.json, keys.json`; nhịp đọc bằng `mo_xe/nhip.py`.

**Hình:** cầu sò tròn nhìn 3/4, vỏ trên xanh lam có hoa văn sóng, vỏ dưới trắng xanh, gai nón kem (8), hai "lông mày" sừng xoắn kem
trên mắt, mắt đen trong khe, lưỡi hồng to giữa hai vỏ, hai răng nhỏ. Rộng 361, cao 387 đơn vị.

**Cắt mảnh (20 vùng atlas):** `P_tou1` vỏ trên, `P_xiaba` vỏ dưới, `P_xiaba1` lòng vỏ tối (mảng xanh đen nằm sau mọi thứ, che khe
khi há), `P_shetou`, `P_shetou1`, `P_shetou2` ba hình lưỡi (đổi hình theo tư thế), `P_meimao1/2` hai sừng xoắn trên mắt,
`P_yanjing1/2` mắt mở / mắt nhắm (một slot, đổi hình), `P_ci1..8` tám gai rời, `ya1/2` hai răng.

**Xương (16):** `root` → `bone` → `bone2` (trục lắc đặt **cao 568 đơn vị trên con**: xoay bone2 vài độ là cả con đung đưa như con lắc)
→ `bone3` → `bone4` (tâm thân: nhún, nghiêng, nhảy) → `bone5` **vỏ trên** (bản lề sau, len 200) và `bone6` **vỏ dưới** (len 180).
`bone19` (con vỏ trên) = mắt; `bone17`, `bone18` (con bone19) = hai sừng xoắn; `bone20..23` chuỗi lưỡi 4 đốt (con vỏ dưới) +
`bone24` điểm điều khiển ngọn lưỡi; `shadow` bóng dưới chân.

**Lưới:** 136 đỉnh. Mọi mảnh trừ lưỡi là **tứ giác cứng 4 đỉnh bám 100% một xương** (vỏ, gai, răng, sừng: gai bám xương vỏ, không lắc
riêng). Chỉ ba hình lưỡi là lưới có trọng số (20–30 đỉnh, 4–5 xương, tối đa 4 xương mỗi đỉnh). Mắt là region đổi hình mở / nhắm.

**Clip (10):** `idle_01` 4 s, `block_01` 0,5, `hit_01` 0,5, `hit_02` 0,67, `die_01` 1,0, `floating_01` 1,5, `run_01` 0,8,
`skill_01` 1,0, `skill_02` 1,13, `stun_01` 1,33.

**Nhịp đọc từ khoá:**
- `idle_01` (4 s, 98% bezier): thân `bone4` nghiêng ±8° chu kỳ 1,33 s (3 vòng trong clip); con lắc `bone2` ±3°; vỏ trên `bone5`
  khép mở rất nhẹ (0–1,8°) và **điểm phá nhịp "lập cập" 1,70–2,23 s** (vỏ trên 1,8 → 0 → 2,7 → −0,2 → 3,6°, vỏ dưới ngược pha
  −4,4 → −1,9 → −4,1°): con sò nhai nhai một nhịp giữa vòng; lưỡi 4 đốt vẫy sóng, hai sừng lắc lệch pha.
- `skill_01` (1 s, 95% nội suy thẳng, khoá cùng khung = dáng → dáng): há vỏ 43° ngay khung 3, giữ há 55° tới khung 13 (lấy đà),
  khung 16 há 59° + vỏ dưới −56° + thân lao tới 208 đơn vị, **khung 17 sập vỏ** (vỏ trên −38°, đổi 97° trong 1 khung = cú ngoạm),
  dội lại, về ở khung 30. Đòn cắn lao tới.
- `skill_02` (1,13 s): **quất lưỡi**: lưỡi giãn 2–3,3 lần (scale x các đốt), xoay ±60–86°, thân lắc 101°; đổi thứ tự vẽ cho lưỡi ra
  trước. Đòn xa bằng lưỡi.
- `hit_01` (0,5 s): khung 0 đã là dáng bị đánh (thân nghiêng 69°, vỏ trên khép −24°), khung 9 vỏ trên bật há 65° (dội), về.
  Không lấy đà; mắt nhắm 0,3 s.
- `die_01` (1 s): thân lật 62°, **vỏ trên há tung 148°**, lưỡi đổi hình rũ ra, mắt nhắm; `stun_01` lưỡi thè lặp, mắt nhắm.

**Học được:** con tròn cứng sống nhờ (1) vỏ khép mở có điểm phá nhịp lập cập, (2) cả con đung đưa quanh trục cao (con lắc), (3) một
phần mềm duy nhất (lưỡi) vẫy sóng, (4) hai sừng nhỏ lắc lệch pha. Gai cứng bám vỏ, không lắc. **Chỗ làm tốt hơn:** gai mỗi cái một
xương có lò xo (lắc trễ theo vỏ), màng mép vỏ là lưới mềm (lượn khi há), thêm phần mềm (chân, xúc tu) để có chuyển động mềm thay vì
chỉ đổi hình lưỡi; mí mắt phủ thay đổi hình mắt.

## 2. Thiết kế dòng: Sò Ngọc (danh hiệu đề xuất: "Pháo đài ngọc trai")

**Lore:** con sò gai sống ở rạn san hô, ngậm trong miệng viên ngọc trai nó tự nuôi từ nhỏ. Ngọc là "tim" của nó: nhỏ thì phun bọt và
bắn gai để giữ ngọc; lớn lên vỏ hóa thành pháo đài có vành đồng và vương miện gai, viên ngọc thành nòng pháo nước. Chiêu theo lore
và chiêu Pokémon hệ nước: Clamp, Bubble Beam, Spike Cannon, Razor Shell, Hydro Pump, Shell Smash, Surf.

Khác con gốc: con gốc là quả cầu xanh lam, gai kem, sừng xoắn trên mắt, mắt đen trong khe, lưỡi hồng to thè ra, không chi. Dòng này:
vỏ xanh đá có vân tăng trưởng đồng tâm và dải xanh lơ (không hoa văn sóng), gai san hô cam ngọn hồng đào, **màng mép vỏ ngọc
lam** lượn sóng, **mắt to tròng hổ phách** nằm dưới mép vỏ như hàng mày cau, **ngọc trai** trong miệng thay lưỡi thè, **ba xúc tu
râu** ở khoé miệng, **một chân mềm** để đứng và nhảy (dạng 2: bốn xúc tu đứng dựng). Không sừng xoắn, không lưỡi thè.

### Bảng màu

| Vai | Dạng 1 Sò Gai | Dạng 2 Bạng Vương |
|---|---|---|
| Vỏ (chủ đạo) | xanh đá `#3D5C9C` (lam xám, GPT tô hơi ngả chàm) | chàm sẫm `#232A66` |
| Dải mép vỏ | xanh lơ `#5EC2E0` | xanh mòng két `#1F9AA8` |
| Gai | san hô cam `#F07F55`, ngọn hồng đào `#FFD2B4` | đỏ san hô sẫm `#D2493A`, ngọn trắng ngà |
| Thân mềm, màng | ngọc lam `#36C2B4`, chấm xanh đá | mòng két sẫm `#15827F`, chấm chàm |
| Chân / xúc tu | ngọc lam nhạt `#7ED8CB` | mòng két sẫm, giác bám kem `#F0E2C4` |
| Lòng miệng | đỏ mâm xôi `#B83A5A` | mâm xôi sẫm `#9E2E4D` |
| Ngọc trai | kem `#F5F0E6`, mảng tím nhạt `#D8CCF0` | trắng ngọc `#EFEAF7`, vệt xoáy xanh lơ `#9FD8F0` |
| Mắt | tròng hổ phách `#F2B33D` | tròng vàng `#F2B33D`, đồng tử dọc |
| Giáp | (không) | đồng thau `#C9923C`, răng vỏ trắng ngà `#F0E4CA` |

Không trùng 13 tướng Thủy đang có (Thủy Long lam + mòng két + vàng, Tám Tay cam + chàm, Thương Lam lam nhạt, Kuba cam đỏ + pha lê,
Huyền Vũ lục, Lam Quân lam + kem mây, Vây Lam lam hoàng gia + trắng, Mi Nhi tím nhạt, Cánh Cụt mòng két, Tiểu Y lam trời, Ma Kết lục
bạc hà, Hải Long ngọc bích + san hô): cặp xanh đá + ngọc lam + san hô cam là riêng.

### Dạng 1: Sò Gai (chibi)

Sò tròn mập (rộng hơn cao), nhìn nghiêng 3/4 quay phải, khe vỏ mở phía trước như cái miệng hé. Năm gai nón trên vỏ trên, hai gai dưới
vỏ dưới. Hai mắt to dưới mép vỏ trên (mép vỏ như hàng mày cau, mặt quả quyết). Màng ngọc lam lượn ở mép hai vỏ; trong miệng đỏ mâm
xôi, ngọc trai nhỏ nằm trên môi dưới; ba xúc tu cong nhỏ ở khoé miệng. Đứng trên một chân mềm, nhảy lò cò bằng chân đó.

### Dạng 2: Bạng Vương (dạng cuối)

Hết chibi, bóng dáng khác hẳn: vỏ to nặng (cao gấp rưỡi dạng 1) có **vương miện năm gai dài đỏ san hô sẫm** cong ra sau, ba gai dưới
vỏ dưới, đi trên **bốn xúc tu** giác bám kem như thú chống chân. Vỏ chàm sẫm, **vành đồng thau đinh tán** chạy quanh mép hai vỏ, nắp
đồng ở bản lề, một **mũ miện đồng nhỏ gắn ngọc lam** trên vỏ trên (GPT tự thêm, hợp chữ "Vương"); mép vỏ răng cưa trắng ngà như hàm
thú; vỏ trên chìa ra như lưỡi trai mũ giáp che hai mắt nhỏ xếch dữ. Hàm há rộng: lòng đỏ mâm xôi, lưỡi xanh mòng két, **ngọc trai
lớn có vệt xoáy xanh lơ** (nòng pháo), hai xúc tu cong ở khoé hàm. Giữ lại từ dạng 1: ngọc trai, gai san hô, thân mềm ngọc lam (sẫm
đi), vân đồng tâm, bản lề tròn.

## 3. Đòn, chiêu từng dạng (đứng tại chỗ là chính; tia, đạn, sóng là lớp VFX, rig chỉ để xương `mieng` và sự kiện)

| Clip | Dạng 1 Sò Gai | Dạng 2 Bạng Vương |
|---|---|---|
| `attack` | **Ngoạm Vỏ** (Clamp): nhún lùi trên chân mềm, nhảy lò cò nửa bước tới, vỏ trên há rồi sập "cạch" ở khung trúng (`trung`), dội, nhảy về. Đòn lao duy nhất của dòng, ngắn | **Hàm Thép** (Razor Shell): đứng tại chỗ, bốn xúc tu ghì đất, vỏ ngả ra sau lấy đà, chồm tới bằng xúc tu trước (không rời chỗ) và sập hàm răng; mép vỏ quét một vệt trăng khuyết nước (VFX) |
| `cast` | **Phun Bọt Ngọc** (Bubble Beam): há vỏ, ngọc lăn ra môi, chuỗi bong bóng phụt từ miệng (`phun` → `het_phun`), vỏ rung nhẹ hai dáng | **Pháo Ngọc Trai** (Hydro Pump): há hàm hết cỡ, lưỡi đẩy ngọc lên môi, bốn xúc tu choãi, tia nước dày bắn từ viên ngọc, giữ 1 s rung hai dáng, giật lùi nhẹ |
| `skill` | **Mưa Gai** (Spike Cannon): khép chặt vỏ, xù gai (gai giãn, lắc), nhún sâu rồi bật thẳng lên (`gai`), gai nước bay vòng cung rơi xuống đối thủ (VFX kiểu `rain`) | **Vỏ Phá Triều Cường** (Shell Smash + Surf): khép vỏ, gồng rung, bốn xúc tu đập đất, bung vỏ há tung, vương miện gai xoè; sóng cuộn trồi từ chân lao tới đối thủ, gai lẫn trong sóng (`gam`, `song`; VFX kiểu `line_erupt` / sóng mảng liền) |
| `hit` | vỏ sập khép, mắt nhắm (mí phủ), thân bật lùi, gai và xúc tu trễ theo, chân bẹp | vỏ khép, xúc tu co, gai rung trễ |
| `die` | giật, nhắm mắt, vỏ trên há tung lả ra, xúc tu rũ, ngọc lăn khỏi môi, đổ nghiêng, tan | giật, nhắm, xúc tu khuỵu lần lượt, hàm há rũ, ngọc rơi, đổ, tan |
| `appear` | rơi xuống nảy trên chân, vỏ bật mở, mắt chớp | xúc tu mọc ra lần lượt chống dậy, vỏ dựng lên, hàm há gầm |
| `evolve` | gồng, khép vỏ, lốc nước, đổi dạng lúc lốc đậm nhất, hiện Bạng Vương há hàm gầm | (dạng cuối) |

## 4. Dự kiến pha 2 (chưa làm)

Tờ mảnh GPT vẽ đủ phần bị che, dạng 1:
- A: vỏ trên (không gai, có dải mép, mặt trong chừa viền), vỏ dưới, lòng vỏ tối (mảng sau mọi thứ), màng mép trên, màng mép dưới.
- B: lòng miệng (bám vỏ dưới, theo luật "thịt trong miệng đi theo hàm dưới"), ngọc trai, hai mắt mở, mí nhắm, ba xúc tu râu duỗi thẳng,
  chân mềm duỗi.
- C: bảy gai rời (năm trên, hai dưới).

Xương dạng 1 (dự kiến ~34): `root` → `move` (nhảy, nghiêng) → `than` → `vo_tren` (bản lề sau, há) / `vo_duoi`; `mat` con `than`
(theo vỏ trên 30%), `mi`; `ngoc` con `vo_duoi`; `mieng` (trục x chĩa phải, ở khe vỏ); chân 4 đốt (`chan1..4`, lưới dải B-spline);
ba xúc tu × 3 đốt (`rau_a..c`, dây mềm nướng); bảy gai mỗi cái một xương có lò xo (lắc trễ theo vỏ); màng mép trên / dưới là lưới
chia trọng số giữa `than` và xương vỏ (lượn khi há).

Dạng 2: tờ A vỏ trên (có vành đồng, răng, chưa gai), vỏ dưới, lòng vỏ tối, hai màng mép; tờ B lòng miệng, lưỡi (dải 3 đốt), ngọc lớn,
mắt mở, mí; hai xúc tu khoé hàm; tờ C bốn xúc tu chân duỗi thẳng (to, giác bám dưới), tám gai rời. Xương ~55: bốn chân × 5 đốt (bàn
chân bám đất giải IK đơn giản), lưỡi 3, xúc tu khoé 2 × 3, gai 8, vỏ 2, thân, mắt, mí, ngọc, `mieng` ở ngọc.

Clip mỗi dạng theo mục 5 đặc tả: `appear`, `idle` (4 s = 3 vòng nghiêng thân, phá nhịp lập cập vỏ, chớp mắt, xúc tu và gai lệch
pha), `attack`, `cast`, `skill`, `hit`, `die`, `evolve` (dạng 1), `aura` (không cần).

## 5. Nhật ký pha 1

- 2026-11-11: viết `ArtGen/Spine/build_tm05.py`, gói `gui_gpt/tm05_1/` (luot_1_concept.txt, HUONG_DAN.md). Ảnh mẫu: world_style,
  Vây Lam dạng 1, Huyền Vũ dạng 1 (đều của dự án, không có ảnh con gốc).
- Gen dạng 1 lần 1 (`tai_ve/L1_concept.png`): bỏ. Ngọc có chấm sáng, gai tô hai nửa sáng tối theo chiều dọc, vỏ ngả tím, mắt lồi
  nhìn hai hướng, chân như thân nấm. Sửa prompt (màu vỏ `#3D5C9C` "không tím", gai một màu chỉ chóp hồng đào, ngọc một màu không
  chấm sáng, mắt ngang nhau cùng nhìn phải mí xếch, chân như ngón cái), gen lại.
- Gen dạng 1 lần 2 (`tai_ve/L1_concept_2.png`): **chọn**, chép thành `tai_ve/L1_chon.png`. Đúng 5 + 2 gai tô phẳng, ngọc phẳng
  không bóng, mặt quả quyết há miệng hô, ba xúc tu râu, một chân mềm. Còn: viền trắng mảnh quanh chân mỗi gai trên vỏ (pha 2 vẽ lại
  tờ mảnh nên không vướng), vỏ vẫn hơi ngả chàm, chân hơi giống cái ủng.
- Dạng 2: thay hai ảnh mốc chibi bằng hai dạng cuối đã duyệt (Vây Lam 3, Huyền Vũ 3) để GPT không vẽ lại chibi; đính concept dạng 1
  đã chọn làm ảnh 4.
- Gen dạng 2 lần 1 (`tm05_2/tai_ve/L1_concept.png`): **chọn**, chép thành `tm05_2/tai_ve/L1_chon.png`. Nét đậm đúng game, vương miện
  gai, vành đồng, răng vỏ, ngọc xoáy tô phẳng không bóng, bốn xúc tu, mắt nhỏ dữ. Còn: con chiếm gần cả khung (gai trên cách mép
  16 px, dưới 30 px), vỏ tròn chứ không "đứng dựng", bốn xúc tu ngắn và hai xúc tu sau khuất một phần, hàm răng to chiếm gần nửa thân.
- Gen dạng 2 lần 2 (`--note`: nhỏ lại, xúc tu dài tách rời, ít răng; `tm05_2/tai_ve/L1_concept_2.png`): bản khác. Xúc tu dài, tách
  rõ (dễ rig hơn) nhưng nét mảnh hơn nét game, mặt nằm trong hàm răng trông rợn, mất vẻ "vương". Giữ để người dùng so.
- Tờ so sánh bốn bản: `inbox/tm05_so_sanh_concept.png`.
- Pha 2 lưu ý: tờ mảnh dạng 2 vẽ bốn xúc tu duỗi dài (dài hơn concept khoảng 1,5 lần, lấy độ dài của bản 2), răng vỏ vẽ liền trên
  từng nửa vỏ; mũ miện là mảnh riêng (lắc trễ nhẹ).

## 6. Pha 2 (2026-11-11, concept đã duyệt)

**Cách dựng: cách lai** (đặc tả mục 5). `tm05_lai.py` (venv có cv2) gán nhãn concept theo cụm màu giữa các nét mực, ưu tiên đa giác:
gai > mũ miện > xúc tu khoé hàm > lòng miệng, ngọc (theo màu) > chân > nửa trên / nửa dưới theo đường chia. Nét mực theo nhãn gần
nhất. Cắt thẳng từ concept: hai nửa vỏ, 8 / 7 gai, mũ miện, 4 xúc tu chân (dạng 2), chân mềm + 3 râu (dạng 1), xúc tu khoé hàm.
Lòng miệng, ngọc, mí cũng lấy từ concept:
- lòng miệng: vùng đỏ, phần bị che tô phẳng màu đỏ chủ đạo có vân chì, lấn dưới hai nửa vỏ và dọc đường môi tới bản lề;
- ngọc: khép vòng tròn chỗ răng che;
- mí: lõi mắt theo màu, bao lồi, nới bằng độ dày viền mực, màu lấy từ điểm da gần nhất, vẽ nét mắt nhắm. Còn hở 0 px.

Vẽ bù chỗ bị che: chân gai, gốc xúc tu lấn dưới vỏ, tô phẳng màu chủ đạo; vòng giấy trắng quanh chân gai tô màu vỏ (không còn khe
trắng). Tờ GPT M01–M03 đã gen (`tai_ve/M0*.png`) nhưng không dùng: mảnh cắt từ concept khớp hơn.

**Rig** (`tm05.py dung_lai`, clip `tm05_clip.py`):
- vỏ trên, vỏ dưới xoay quanh bản lề;
- lưới nửa vỏ: vỏ cứng 100%, vùng mặt theo xương `mat` (tối đa 92%), dải môi theo chuỗi `mt*` / `md*` 4–5 đốt;
- lòng miệng là màng nối hai vỏ (trên môi trên 100% vỏ trên, dưới môi dưới 100% vỏ dưới, giữa hoà): vỏ khép được kín;
- mỗi gai một xương có lò xo; mũ miện lò xo;
- xúc tu: lưới vùng trên mảnh cong, trọng số B-spline theo khoảng cách đi trong hình từ gốc (đường giữa tìm bằng đường đi ngắn nhất);
- chân / xúc tu chân giữ bám đất bằng CCD;
- xương `mieng` ở mép trước viên ngọc (dạng 2) / khoé miệng (dạng 1).

Mật độ lưới: bước viền 1,3%, bước trong 1,75% chiều cao con. Mọi mảnh hở 0 px.

**Kết quả**

| | Dạng 2 Bạng Vương | Dạng 1 Sò Gai (rig gộp tiến hóa) |
|---|---|---|
| Xương, slot | 57, 21 | 99, 38 (riêng dạng 1: 42 xương) |
| Đỉnh, tam giác | 3085, 5169 | 6676, 11415 (riêng dạng 1: 3591 đỉnh) |
| .atomik | 213 KB (đạt đích 0,3 MB) | 372 KB (dưới trần 0,5; chứa cả dạng 2 cho evolve) |
| IoU khung 0 với concept | 0,926 | 0,933 |

Nối clip đo trên đỉnh tính từ `.atomik` (gồm lò xo): mọi clip khung 0 và khung cuối lệch idle khung 0 là 0,00 px; idle khép vòng
0,00 px; appear khung 0 trống; die khung cuối trống; evolve khung cuối trùng idle dạng 2 (0,00 px).

Bài học:
- Dao động nền trong clip không lặp phải hoà từ giờ `t` sang `t − D`, không chỉ dùng `lui`: dùng `lui` thì khung 0 lệch idle.
- Lò xo phải cộng phần chênh với idle ở đầu clip.
- Chân bám đất phải gọi ở MỌI clip của dạng đó. Thiếu một clip là khung 0 lệch 7,8 px, bộ đo cũ báo 0.

