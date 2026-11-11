# tm06: dòng Giông Bão (lô 10 tướng mới đảo Thủy, dòng 6, thay suất ải 30 Vây Lam, hiếm)

Đặc tả chung: `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`. Gói prompt: `ArtGen/Spine/build_tm06.py` → `gui_gpt/tm06_1/`, `gui_gpt/tm06_2/`.

## 1. Con gốc monster_3241 (chỉ học cấu trúc và nhịp, không lấy hình)

Đọc từ `D:\RefAnimation\SwordxStaff\scan\monster_3241\info.json, keys.json, mesh.json` và atlas.

- Dáng: thủy quái ếch/kappa ngồi xổm hai chân, áo choàng, tóc lá, đĩa trên đầu, mỏ; cõng **gậy có thùng gỗ** vắt vai (cái "thùng"
  trên lưng thật ra là đầu gậy `P_gunzi`, tay xa cầm cán chìa ra trước), dây đỏ buộc thùng (`P_shengjie1..3`).
- Số: Spine 4.2.28, 95 xương, 45 slot (44 lưới có trọng số, 1 slot bóng trống), **638 đỉnh, 630 tam giác** (mỗi mảnh 6–27 đỉnh,
  tối đa 4 xương/đỉnh, phần lớn 1–2), 6 IK (2 chân × 2, 2 tay), không transform, không physics, không sự kiện. Atlas 320 × 752,
  tỉ lệ 0,75, 0,3 MB cả con.
- Cây xương: `bone2` (dời cả con) → `bone` → `bone3` (hông) → `bone4` (bụng, lưới `P_shenti`) → `bone5` (ngực) → `bone6` → `bone7`
  (đầu: lưới `P_tou` bám đầu + 2 xương phụ `bone65`, `bone66` để phồng má/méo đầu; 2 xương mắt; `bone46` đĩa đỉnh đầu → **8 chuỗi lá
  tóc 2–3 đốt**; `bone75` mỏ trên, `bone85` hàm dưới). Tay gần `bone8→9→10→11→12` (IK SR1, SR2) + chuỗi tay áo 3 đốt; tay xa
  `bone13→14→15→16→17` (gậy dài 401, hai chuỗi dây 3 và 5 đốt) + chuỗi tay áo 3 đốt; vạt áo trước, sau mỗi cái chuỗi 4 đốt; hai chân
  3 đốt + IK. `bone76` (con của root) là **bản sao gậy + dây** ẩn sẵn: clip chết bật nó lên để gậy văng ra, xoay 400° rơi xuống đất.
- Mảnh trong atlas: đầu, thân, 8 lá, 2 mỏ, 6 hình mắt (mở, nheo, nhắm), áo choàng 7 mảnh (trước, sau, tay áo), tay 2 × 2 mảnh,
  chân 2 × 3 mảnh, gậy + thùng một mảnh lớn (309 × 248, gần 1/3 atlas), 3 đoạn dây.
- 10 clip (khoá thật): idle 2,67 s (328 khoá, 96% bezier), block 0,5, hit_01 0,5, hit_02 0,67, run 0,53, skill_01 1,27,
  skill_02 1,33, stun 1,33, floating 1,5, die 1,0 (459 khoá). Clip đánh 96–98% nội suy thẳng (dáng → dáng).
- Nhịp đọc được (`mo_xe/nhip.py`):
  - **idle**: chu kỳ thân 1,33 s (2 vòng mỗi clip): nảy lên 22 đơn vị ở 0,67 s, nén 0,946 lúc chạm; đầu lệch pha thân. **Chuỗi
    dây, lá: mỗi đốt trễ 5 khung (0,17 s) từ gốc ra ngọn, biên độ lớn dần ra ngọn** (lá 9° → 20° → 23°; dây 5 đốt 18° → 68°,
    chu kỳ 0,67 s). Mỗi đốt 2 cực trị một vòng.
  - **skill_01** (đòn chính): nhún, bật lên 180 đơn vị và ngả ra sau 46° (0,1–0,37 s), **nện xuống ở 0,47 s** (khung 14), gậy quật
    −93 → −128°, giữ 0,3 s, rồi xoay gậy tròn 360° trước khi về (múa gậy).
  - **skill_02**: nhảy rất cao (486) rồi đập thân xuống đất ở 0,47–0,5 s.
  - **hit_01**: khung 0 đã là dáng bị đánh, bật lùi 95 đơn vị ở 0,07 s, đầu ngửa −59° ở 0,2 s, lá tóc vẫy 55–75°, về ở 0,5 s.
  - **die**: bật lên, lộn ngửa (−156°), gậy văng (bản sao `bone76`), nằm ngửa đất, mắt nhắm.
- Học được cho dòng này: phần mềm (lá, dây, vạt áo) là chuỗi 2–5 đốt trễ pha mỗi đốt 5 khung; đồ cứng trên lưng là một mảnh lớn
  có xương riêng, **có bản sao ẩn để văng ra khi chết**; má phồng bằng 2 xương phụ trong lưới đầu; mắt đổi hình (mở / nheo / nhắm).

## 2. Thiết kế (của mình, khác hẳn con gốc)

Ý: con gốc là "thủy quái lưỡng cư cõng đồ". Dòng 3 (`tm03`) đã là ếch/nòng nọc tròn, nên dòng này đổi sang **kỳ giông** (đuôi dài,
đầu dẹt rộng, mang ngoài như lông chim), không ếch, không cóc. Tên chơi chữ: kỳ **giông** và cơn **giông** (mưa bão).

- Lore: Giông Mưa là kỳ giông con ở suối núi, cõng quả bầu hồ lô hứng nước mưa đầu mùa; bầu vơi là trời đổ mưa. Lớn lên thành
  Giông Bão, chúa kỳ giông thác ngàn, cõng bình đồng nhốt cả một cơn giông; mở nắp là mưa như trút, nước cuộn thành lốc.
- Bảng màu (không trùng 13 tướng Thủy đang có: lam tươi Tiểu Y, ngọc Cánh Cụt, tím Mi Nhi, lục Ma Kết, lam đậm Vây Lam, cam Kuba,
  lam nhạt Thương Lam, lục Huyền Vũ, lam Lam Quân, cam Tám Tay):

| | Dạng 1 Giông Mưa | Dạng 2 Giông Bão |
|---|---|---|
| Da | xanh đá mưa `#6E88BC` | chàm bão `#34477E` |
| Bụng, họng | cam mơ `#F4A65A` (một mảng) | hổ phách `#E8782E` (tấm bụng chia đốt) |
| Mang | 3 lá mỗi bên, san hô `#E5603F` | 4 lá dài mỗi bên, đỏ son `#C8383A`, vuốt ra sau như mũ chiến |
| Hoa văn | đốm kem tròn `#F4EEDC` như giọt mưa | sọc bọt sóng `#EAF2F8` hình mào sóng cuộn |
| Vây | vây đuôi thấp lam nhạt `#9CC0E8` | vây lưng cao chạy đầu → đuôi, lam bão `#8FB3E0` |
| Mắt | vàng `#F2C641`, đồng tử tròn | hổ phách `#F0A030`, đồng tử dọc, mày nặng |
| Miệng | hồng sẫm `#C2475E`, lưỡi `#E27C92`, không răng to | `#B8405A`, răng nhọn ngắn, hai nanh nhỏ |
| Đồ trên lưng | bầu hồ lô vàng rơm `#E8C66A`, nút gỗ `#8A5A33`, tua kem, dây chàm `#2F4F8F` chéo ngực | bình đồng xanh rỉ `#4E9E8A`, đai vàng đồng `#D4A23F`, phù điêu sóng, nắp vòm có vòng; dây thừng chàm `#2A3F78` chéo chữ X |
| Giáp | không | giáp vai đồng hình mào sóng (vai gần), đai cổ tay đồng |

- Dạng 1 **Giông Mưa** (chibi, đầu ~45%): kỳ giông con đứng xổm hai chân, thân quả lê, đầu dẹt như hạt đậu, miệng rộng hé, mắt
  tròn mày hạ quả quyết; tay gần nắm đấm giơ trước ngực, tay xa xoè sau; đuôi dày có vây nằm sau bên trái; quả bầu trên lưng.
- Dạng 2 **Giông Bão** (dạng cuối, không chibi, đầu ~25%): kỳ giông khổng lồ khom thế võ, chân cong rộng, tay dài móng sẫm (tay gần
  vồ trước, tay xa nắm đấm giơ sau vai); đầu nêm dẹt, mắt xếch đồng tử dọc, nanh nhỏ; vây lưng cao; bình đồng to trên lưng. Đổi
  màu (đậm), đổi hoa văn, đổi đồ (bầu → bình đồng), thêm giáp, đổi bóng dáng (tròn thấp → dài, rộng, có vây lưng); giữ mang, bụng
  cam, cõng đồ.
- Khác con gốc: không ếch (kỳ giông có đuôi, mang), không mỏ, không đĩa, không tóc lá, không áo choàng, không gậy; đồ trên lưng là
  bầu / bình đồng chứ không phải thùng trên gậy; màu lam + cam thay lục; con gốc cầm gậy đánh cận, dòng này phun nước đứng tại chỗ.

## 3. Đòn, chiêu (đứng tại chỗ, dạng sau đổi kiểu và dữ hơn)

| Clip | Dạng 1 Giông Mưa | Dạng 2 Giông Bão |
|---|---|---|
| attack | **Súng Nước** (Water Gun): ngửa đầu lấy đà, chúi tới há miệng nhả một viên nước; mang dựng lên; sự kiện `trung`, xương `mieng` ở môi | **Đuôi Thủy Triều** (Aqua Tail): vặn hông, quất đuôi đập đất, cột nước trồi dưới chân đối thủ (far); `trung` |
| cast | **Bầu Phun** (Hydro Pump nhỏ): rút nút bầu, bầu xoay qua vai thành vòi, dòng nước bắn thẳng, giữ 0,9 s; `phun`, `het_phun`, xương `mieng` ở miệng bầu | **Pháo Bình Đồng** (Hydro Cannon): hạ thấp, gồng chân, nắp bình bật lên, bình chúc qua vai nhả luồng nước xoáy dày giữ 1,2 s, giật lùi, há miệng gầm theo; `phun`, `het_phun` |
| skill | **Cầu Mưa** (Rain Dance): dậm chân hai lần, vỗ bụng, bầu phụt cột nước lên trời; mưa rơi quanh đối thủ (kiểu `rain`, 3 đợt); `gam`, `het_gam` | **Giông Bão** (Whirlpool + mưa giông): đứng thẳng ngửa cổ gầm há to, bình phun cột nước lên thành mây giông; mưa xối + vòi rồng nước cuốn đối thủ (kiểu `vortex`, 3 nhịp, chớp màn); `gam`, `het_gam` |
| hit | bật lùi ở 0,07 s, mắt nhắm, mang và tua vẫy từ ngọn về gốc, bầu nảy trễ | như dạng 1, nặng hơn, ít bật, vây lưng gợn |
| die | giật, nhắm mắt, ngồi bệt lả đi một nhịp, bầu tuột dây lăn ra (bản sao ẩn như con gốc), đổ ngửa, tan | quỳ một gối, bình nghiêng đổ nước, gục xuống, tan |
| evolve | ôm bầu, nước dâng lốc, đổi dạng lúc lốc đậm nhất, Giông Bão bung ra gầm, về idle dạng 2 | (dạng cuối, không có) |
| aura (tuỳ) | 2–3 giọt nước lượn quanh miệng bầu | vũng nước gợn dưới chân + giọt bay vòng quanh bình |

Hiệu ứng (viên nước, dòng phun, mưa, vòi rồng) là lớp VFX trên sân, không vẽ trong rig; rig để xương `mieng` và sự kiện.

## 4. Dự kiến pha 2 (chỉ làm khi được duyệt)

Cách dựng như Hải Long (`pokiclash-spine-rig` mục 20): concept làm mốc, GPT vẽ tờ mảnh rời đủ phần bị che, rig dựng bằng mã.

Tờ mảnh mỗi dạng (1536 × 1024, mảnh cách nhau ≥ 60 px):
- **M01 đầu**: đầu trên (sọ + hàm trên + mắt mở, không mang, gáy tròn vẽ dư), hàm dưới rời có lòng miệng + lưỡi (dạng 2 có răng,
  nanh), mảng lòng miệng, mí mắt nhắm (mắt gần, mắt xa).
- **M02 mang, vây**: lá mang duỗi thẳng (dạng 1: 1 lá to + 1 lá nhỏ dùng lại cho 3 lá/bên; dạng 2: 2 cỡ cho 4 lá/bên), vây đuôi;
  dạng 2 thêm dải vây lưng duỗi thẳng.
- **M03 thân, chi**: thân (ngực, bụng, vẽ dư cổ và hông), tay gần liền (vai → cổ tay) + bàn tay nắm, bàn tay xoè, tay xa, chân gần
  (đùi + cẳng) + bàn chân, chân xa, đuôi duỗi thẳng.
- **M04 đồ**: dạng 1 quả bầu nguyên (cả phần sau lưng), nút gỗ rời, dây đeo dải thẳng, tua kem dải thẳng; dạng 2 bình đồng nguyên,
  nắp rời, giáp vai, hai đai cổ tay, dây thừng dải thẳng.

Xương dự kiến:
- Dạng 1 (~60): `root`, `move`, `shadow`, `hip`, thân 2 đốt, cổ, đầu, `jaw`, `mieng` (môi), 2 xương má phụ, mang 6 chuỗi × 3 đốt
  (18), tay 2 × 3, chân 2 × 3 + đích IK, đuôi 5 đốt, `bau` (khớp ở vai, lò xo lắc), `bau_mieng` (chỗ phát cast), `nut`, tua 3 đốt,
  dây đeo 3 đốt bám thân, bản sao bầu ẩn cho clip chết.
- Dạng 2 (~80): như trên với thân 3 đốt, đuôi 7 đốt, vây lưng là dải lưới bám chuỗi thân + đuôi, mang 8 chuỗi × 3–4 đốt, `binh`,
  `nap` (bật mở), `binh_mieng`, giáp vai cứng trên cánh tay trên, đai cổ tay cứng.
- Lưới: mọi mảnh mềm lưới tam giác đều cạnh, trọng số B-spline cho chuỗi (mang, đuôi, tua, dây, vây lưng), hoà theo khoảng cách đi
  trong hình cho thân; đồ cứng (bầu, bình, nắp, giáp) bám 100% một xương. Mang, tua, dây: mô phỏng dây mềm rồi nướng (chặn góc khớp).
- Đích dung lượng ≤ 0,3 MB mỗi dạng (atlas 256 màu, lọc RDP; mang dùng lại một hình, lật bằng tỉ lệ âm).

## 5. Nhật ký pha 1

- 2026-11-11: đọc đặc tả, skill, mổ con gốc; viết `build_tm06.py`; gen concept dạng 1.
- Dạng 1, 3 lần gen:
  - `L1_concept.png`: dáng, mặt, bầu đẹp; nhưng da lam hoa ngô `#718FCF` sát Lam Quân `#5884D1`, hai vệt sáng trắng trên đỉnh đầu,
    tay xa chồng lên bầu.
  - `L1_concept_2.png` (`--note` đổi màu): da xanh đá đúng `#7284B5`, dáng rộng; nhưng mặt cười nhếch, bầu như đặt trên đuôi, vệt
    sáng trên bầu, bầu mất sọc.
  - `L1_concept_3.png` (`luot_1_sua.txt`: đính bản 1, giữ bố cục, chỉ sửa màu, vệt sáng, tay): **chọn** → `L1_duyet.png`. Da
    `#7D8EBA` xám hơn hẳn Lam Quân; không vệt sáng (còn hai chấm kem rất nhỏ gần gốc mang, đọc như đốm); tay xa đã tách bầu.
- Dạng 2: dựng prompt đính `tm06_1/tai_ve/L1_duyet.png`, Khổng Lồ 3 (thần thái, thế võ), Thương Lam 3 (nét, hoa văn), bản đồ.
  Tay: hai tay thủ thế phía trước một cao một thấp (tránh tay xa giơ sau vai đụng bình). Vây lưng khuất sau bình.
- Dạng 2, 1 lần gen (chờ khoá Codex khoảng 60 phút): `L1_concept.png` **chọn** → `L1_duyet.png`. Đúng thiết kế: khom thế võ, đầu
  rất nhỏ (khoảng 1/6 chiều cao), mắt xếch, nanh; chàm `#465493` (khác Vây Lam `#1C38A5`), bụng hổ phách chia đốt, sọc bọt sóng, vây
  lưng ở gáy và dọc đuôi, bốn lá mang đỏ son, bình đồng xanh rỉ đai vàng có phù điêu sóng, nắp vòm có vòng, dây thừng chéo, giáp vai
  hình sóng, hai đai cổ tay. Tô phẳng, không điểm sáng. Lỗi nhỏ: gốc mang có vệt đỏ loang sang đầu (chuyển màu), mắt không thấy
  chấm sáng, mang chồng lên mép bình; đầu hơi giống thằn lằn (mõm dài) hơn kỳ giông khổng lồ. Tờ mảnh pha 2 vẽ lại nên sửa được ở đó.
- Tờ so sánh hai dạng: `inbox/tm06_2/so_sanh_2_dang.png`.

## 6. Đổi dạng 2 (điều phối, 2026-11-11) và pha 2

- Điều phối duyệt dạng 1 (`tm06_1/tai_ve/L1_duyet.png` = `L1_concept_3.png`). Dạng 2 đứng hai chân thế võ trùng dạng 2 của tm01
  (Sóng Thần) nên đổi: **kỳ giông núi khổng lồ bò bốn chân**, thân to dẹt, đầu rộng dẹt mõm tròn, xám tím mây giông `#5A5878`
  (đo được `#716889`, sống lưng `#415379`), sọc bọt sóng, bụng hổ phách, mang đỏ son lớn, vây lưng nối vây đuôi dẹt, bình đồng cõng như
  mai, dây thừng chàm, vòng cổ đồng. Gen 1 lần (`tm06_2/tai_ve/L1_concept_2.png`) → chọn, chép thành `L1_duyet.png` (bản cũ
  `L1_concept.png` để lại, không dùng). Ảnh mẫu: dạng 1, Giáp Long 2 (dáng bò thấp), Thương Lam 3 (nét), bản đồ.
- Tờ mảnh (`build_tm06.py manh k`, GPT vẽ từng mảnh **đúng dáng concept**, đủ phần bị che): dạng 1 M01 đầu/hàm/lòng miệng/2 mí/3 lá
  mang/nút bầu, M02 thân/đuôi/2 tay, M03 2 chân/bầu; dạng 2 M01 đầu/hàm/lòng miệng/2 mí/3 lá mang, M02 thân (có vòng cổ, dây thừng,
  vây lưng thấp)/đuôi, M03 bình không nắp/nắp/4 chân. Mỗi dạng 1 lần gen, dùng được ngay.
- Đặt mảnh **dò tự động** (`tm06_place.py`, cv2 qua `D:/spine-venv`): SQDIFF có mặt nạ trên Lab, dò thô ½ độ phân giải rồi tinh;
  điểm số chia `diện tích^1.1–1.3` để bớt thiên về tỉ lệ nhỏ; lá mang đặt theo hai đầu khớp đọc trên concept (`tm06_cfg.py` HINT,
  TWO). Ràng buộc nối `NOI`: thân dạng 2 kéo dài cho đầu cổ chui dưới đầu 60 px. IoU ghép mảnh: dạng 1 0,882, dạng 2 0,865.
- Rig (`tm06.py`, `tm06_d2.py`, thư viện `quai/`): toạ độ concept → rig (G = 0,5 dạng 1, 0,45 dạng 2), mỗi mảnh nạp ở đúng độ phân
  giải hiển thị (T = tỉ lệ đặt × G). Lưới theo chiều cao con: bước viền 1,5 %, trong 2 % (dạng 1: 5,3 / 7,1 px; dạng 2: 4,4 / 5,9 px,
  thân và đuôi dạng 2 thưa hơn 7–15 % cho vừa dung lượng). Chuỗi (đuôi, tay, chân, lá mang) trọng số B-spline: chân tay chiếu lên
  đường khớp tính tự động theo khoảng cách đi trong hình (`geo_truc`), đuôi theo khoảng cách đi trong lưới (`chuoi_geo`). Chân 3 đốt
  (đùi, cẳng, bàn), IK giữ cổ chân, bàn chân xoay bù giữ phẳng. Mí mắt: mặt nạ tròng vàng + bao lồi (`mat_mat`) → `fit_lid` còn hở 0 px.
- Chỗ nối dạng 2 (tờ GPT vẽ đầu mảnh như miệng ống): cắt nắp ống rồi mờ dần (`mo_mep`): thân trái dưới đuôi, đầu trái trên vòng cổ,
  đỉnh 4 chân, gốc đuôi; chân gần nằm sau thân (mép bụng che đỉnh chân). Soi `rig/soi_noi.png` 7 khung × 6 chỗ nối: không khe.
- Lòng miệng: miệng kỳ giông rộng nhìn 3/4 nên khoang miệng là màng giãn giữa môi trên (đầu) và hàm (hàng trên bám đầu, hàng dưới bám
  hàm); lưỡi vẽ liền trong ảnh hàm nên không có "lưỡi thứ hai"; há to vẫn kín (`can_mieng_cast.png`, `can_mieng_skill.png`).
- Nền idle tuyến tính, lệch về 0 ở t = 0 (`songz`, `chuoi_songz`): khung 0 idle = dáng concept; clip không lặp hoà `nen(t)` → `nen(t−D)`
  (`xfade`) nên khung 0 và khung cuối mọi clip đúng khung 0 idle (đo trên đỉnh lưới: 0,00 px). Không dùng lò xo (khung 0 phụ thuộc
  trạng thái lò xo); phần mềm (mang, đuôi, bầu, nắp) là sóng trễ pha tất định.
- Đòn đúng chiều: attack đuôi nhấc lên lúc lấy đà (0,1–0,36 s dạng 1; 0,12–0,5 s dạng 2), quật chạm đất đúng `trung` (0,48 / 0,62), giữ
  trôi, về.
- Evolve: rig gộp dạng 1 + dạng 2 bản lưới thưa ×2,2, ảnh ×0,62 (chỉ hiện ~1,4 s, `tm06_2.atomik` riêng vẫn đủ dày); khung cuối lệch
  khung 0 idle dạng 2 0,00 px; dạng sau co 0,873.
- Đòn/chiêu đã dựng (đổi so với mục 3 ở dạng 1 cho rõ): dạng 1 attack **Đuôi Hắt Nước** (đuôi đập đất, sóng nước lan tới đối thủ,
  `trung` 0,48), cast **Súng Nước** (há miệng phun tia, `phun` 0,5 – `het_phun` 0,95, xương `mieng` ở môi), skill **Cầu Mưa** (dậm chân
  0,28 / 0,55, bầu dựng, nút bật `bat_nut`, cột nước lên trời `gam` 0,95 – `het_gam` 1,45). Dạng 2 attack **Đuôi Thủy Triều** (`trung`
  0,62), cast **Pháo Bình Đồng** (`bat_nap` 0,6, `phun` 0,72 – `het_phun` 1,3, xương `mieng` ở miệng bình), skill **Giông Bão** (chồm,
  gầm `gam` 1,1 – `het_gam` 1,75, nện chân trước `nen` 1,9). Tất cả đứng tại chỗ (`stay`: attack, cast, skill).

## 7. Dạng 2 làm lại bằng cách lai (điều phối 2026-11-11, sau khi chê đầu nhỏ, cổ như rùa, nắp bay lơ lửng)

- `tm06_lai.py` (cv2 qua venv): cắt thẳng từ concept thân + đuôi + vây + vòng cổ + đầu trên (một lớp), bình, nắp, 4 chân. Vùng loang
  từ hạt giống (nét mực là tường), nét mực và ô kín lấy nhãn gần nhất, lọc đa số 7×7; lá mang lấy theo màu đỏ son, vây theo màu lam
  nhạt; bình kẹp trong đa giác. Soi `lai/nhan.png`, `lai/lop.png`.
- Vẽ bù chỗ bị che (lớp dưới mọc dưới lớp trên): lưng dưới bình và gáy dưới mang lấy từ thân/đầu GPT đã đặt; thân dưới đùi tới đường
  bụng nội suy qua cột chân (thân GPT trước, còn lại loang màu đã xoá nét mực), kẻ nét mực mép bụng dưới chân; miệng bình dưới nắp
  lấy từ bình GPT; chân xa mọc thêm 38 px lên trên. Đỉnh đùi phía trên đường cắt cong (đường bụng − 22 px, vồng 22 px giữa chân)
  ở lại lớp thân; mép trên lớp chân kẻ nét mực theo cung. Góc hàm dưới má (x < 1165) ở lại lớp thân.
- Mảnh GPT chỉ còn: hàm dưới (khớp lại vào vùng hàm concept bằng IoU mặt nạ, `tm06_khop_ham.py`, núm bản lề mờ vào má), khoang
  miệng (màng, sau lớp thân, lộ qua chỗ hàm đã khoét), 2 mí (dò trên mắt concept, hở 0 px), 6 lá mang.
- Trọng số lớp thân: thân theo chuỗi hông → thân → ngực → cổ, đầu theo trục gáy → tâm đầu (hoà cổ), đuôi theo chuỗi đi trong vùng
  đuôi; ba vùng hoà theo khoảng cách đi trong lưới (`trongso.vung`), tối đa 4 xương. Đầu xoay tới 35° (skill) vẫn liền vòng cổ.
- Nắp bình: bản lề ở mép sau (xương `nap` tại (668, 318) concept), lật mở 72° (cast, rung trong lúc phun, sập lại có nảy) và 88°
  (skill), idle lạch cạch 4°, chết lệch 16°; không bay.
- Số: 47 xương, 17 slot, 5547 đỉnh, 9687 tam giác, 6046 khoá, .atomik 263 KB; IoU khung 0 idle / concept 0,954; nối clip 0,00 px.
  Dạng 1 gộp lại evolve với dạng 2 mới: 238 KB, evolve khớp idle dạng 2 0,00 px.
