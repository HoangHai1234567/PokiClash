# Tướng 10 đảo Thổ (ải 70, final boss): khổng lồ đá nổi (`thach_de`, rig `monster_3802`)

Bắt đầu 2026-11-18 (máy D, chế độ hỏi, `SXS=D:/RefAnimation/SwordxStaff`). Suất 10 đảo Thổ = ải 70, id game hiện là **`giap_nham`** (Giáp
Nham, hình aola cũ). Thay hẳn `giap_nham` hay không, tên, số dạng: CHƯA hỏi xong (Claude giả định thay suất này, đã báo người dùng). Xương,
lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai.

## 1. Lời dặn của người dùng

- 2026-11-18: "tôi cần làm final boss đảo thổ nhưng chưa nghĩ ra concept gì, bạn có thể research và gợi ý không, điều kiện là phải đẹp,
  chiến, chất hơn tất cả các con trước ở đảo đó, phải độc đáo và lạ".
- Claude đưa năm ý tưởng trên năm rig chưa dùng (3805 thú hoa hồng sa mạc nghìn mắt, 3801 sơn thần bốn tay, 3622 nghê vá vàng, 3628 thao
  thiết đồng, 3617 tượng sáu tay) và loại 3802 vì trùng chất đá với Sơn Viên.
- Người dùng tự mở trang xem kho, gửi ảnh `monster_3802`: **"con này ổn nhưng tôi muốn bạn cải tiến nó thêm nữa, chiến hơn nữa, lạ hơn"**.
  (Diễn giải của Claude: giữ kiểu thân của con gốc: lõi tròn, đá nổi, đầu nhỏ, hai nắm đấm rời; thêm một điểm nhấn lạ và làm dữ hơn.)

## 2. Rig `monster_3802`

- 134 xương, 108 slot, 2 IK, 15 clip: `generate_01` (trồi từ đất lên, 3,1 s), `idle_01`, `run_01`, `skill_01_1..3` (ba nhịp đấm),
  `skill_02` (vung nắm đấm trái lên rồi nện), `skill_03` (ôm hai nắm đấm nện xuống trước mặt), `skill_04` (2,83 s, giơ cao nắm đấm, đá văng),
  `skill_05` (dang hai nắm đấm), `block_01`, `hit_01/02`, `stun_01`, `die_01` (sụp thành đống).
- Hầu hết tảng đá là mảnh cứng một xương: `P_*_shitou*` (đá vai), `P_R_beiji*` (hàng đá lưng, 13 mảnh), `P_*_xiaobi*` (cẳng tay),
  `P_*_shouzh*` (đốt ngón tay, mỗi đốt một xương). Lưới: `P_shenti01/02` (lõi + bụng, xương bone4/5), `P_tou1/2/3` (đầu + hàm), vài mảnh đùi.
- Đã quét vào `<SXS>/scan/monster_3802/`: `info.json`, `att_goc.json`, `att_idle0.json`, `khung/*.jpg` (tờ khung 3 khung mỗi clip).
- Hình cả con gốc: `inbox/thach_de_1/mau/goc_ca_con.png` (tỉ lệ 0,562 px / đơn vị); bảng slot: `tho10.py slot`.

## 3. Concept lượt 1 (ba hướng cải tiến, cùng rig; CHỜ người dùng chọn)

Script `ArtGen/Spine/tho10.py` (dùng lại `tho5.py`, `tho9.py`). File prompt `gui_gpt/thach_de_1/luot_1_concept_<k>.txt`, hướng dẫn
`gui_gpt/thach_de_1/HUONG_DAN.md`. Ảnh mẫu: 1 = con gốc (dáng), 2 = Sơn Viên, 3 = Thiên Thạch Thú (nét). Gen thẳng bằng công cụ Magnific
(GPT 2.6, 1k high, 3:2, 95 credit / ảnh, 285 credit cả lượt). Ảnh `inbox/thach_de_1/tai_ve/L1_<k>.png`, tờ chồng viền
`inbox/thach_de_1/mau/_so_goc.png`.

| Hướng | Tên | Điểm nhấn lạ | Màu | IoU |
|---|---|---|---|---|
| A | Tam Thủ Thạch Vương | hai nắm đấm là hai đầu nghê đá há mồm (đốt ngón tay = hàm dưới): ba đầu, đấm là cắn | đá ngà, mạch hàn vàng, bazan than, ngọc bích | 0,647 |
| B | Thổ Tinh | lõi là hành tinh đá kẻ dải có vành đá nghiêng bay quanh | dải kem / vàng đất / đỏ gạch, đá phiến xanh đen, thạch anh tím | 0,641 |
| C | Nhãn Sơn | lõi nứt lộ MỘT CON MẮT KHỔNG LỒ; đầu nhỏ chỉ là mặt nạ chiến | đen / trắng / tím như con gốc | 0,693 |

Claude soi:

- Cả ba đúng kiểu thân, nét vẽ tay, tô phẳng, mạch nứt không phát sáng. Cả ba vẽ dáng CHÍNH DIỆN, cân hai bên hơn con gốc (con gốc
  nghiêng ba phần tư, nắm đấm trái to và thấp hơn): lúc chia mảnh phải làm theo khung part của rig.
- A: khác con gốc nhất, màu tách hẳn dải nâu của đảo. Mặt đầu chính ra kiểu khỉ đột, gần mặt Sơn Viên: nếu chọn phải đổi mặt. Đốt ngón tay
  thành răng hàm dưới: các clip nắm / xoè tay sẽ thành ngoạm.
- B: lõi đọc ra sao Mộc (có đốm đỏ) hơn là đá; vành mảnh, dễ chìm; ít dữ nhất. Mặt cũng kiểu khỉ.
- C: dữ nhất, giữ đúng thứ người dùng khen ở con gốc. Mặt nạ ra kiểu sọ quỷ (prompt cấm sọ): nếu chọn phải làm lại mặt nạ bớt sọ. Con mắt
  có thể làm slot riêng: idle hé, tung chiêu mở to, trúng đòn nhắm.
- Claude đề xuất C; A là lựa chọn nếu muốn bộ màu khác hẳn. Có thể ghép: mắt trong lõi của C + nắm đấm đầu thú của A.

**Người dùng (2026-11-18): "concept B lấy hành tinh làm lõi rất hay nhưng có thể phát triển thêm nữa cho nhất quán hơn, các bộ phận cùng
các rải đá xung quanh nhìn chưa được hợp".** (Diễn giải của Claude: bản B có bốn kiểu hình không liên quan: lõi nhẵn kẻ dải, đá phiến đen
góc cạnh, tinh thể tím, chuỗi sỏi làm vành. Giữ lõi; mọi bộ phận phải cùng một thế giới với lõi, mỗi bản chỉ hai chất liệu.)

## 3b. Concept lượt 2: ba cách làm hướng B nhất quán (CHỜ người dùng chọn)

`tho10.py concept2` (bảng `HUONG2`, `COMMON2`: lõi đọc ra ĐÁ (dải địa tầng mép lượn, hố tròn, bỏ đốm bão), bỏ tinh thể / đá phiến / chuỗi
sỏi, mặt KHÔNG khỉ (mặt nạ thú sừng, mõm bò-sư tử), dáng ba phần tư lệch như con gốc). Ảnh mẫu 4 = `L1_B.png` (dùng luôn bản đã có trên
Magnific, không tải lại). Ảnh `tai_ve/L2_<k>.png`, tờ chồng viền `mau/_so_goc_L2.png` (`tho10.py so_goc2`), 285 credit.

| Bản | Tên | Cách thống nhất | IoU |
|---|---|---|---|
| B1 | Vỏ hành tinh vỡ | mọi bộ phận là mảnh VỎ sẫm cong, mép vỡ lộ đúng dải địa tầng của lõi; vành hai làn mảnh vỏ; sừng kẻ khoang màu dải | 0,652 |
| B2 | Thổ Tinh và các vệ tinh | hai nắm đấm là hai MẶT TRĂNG đầy hố, vai và hàng đá lưng là trăng khuyết, sừng ghép thành trăng lưỡi liềm; vành là dải phẳng liền | 0,698 |
| B3 | Hỗn thiên nghi đá | lõi nằm trong các VÒNG ĐÁ CHẠM có khía vuông của cỗ máy thiên văn cổ; vai là cung vòng, nắm đấm là găng đá có đai; đinh ngọc bích | 0,676 |

Claude soi: cả ba nhất quán hơn hẳn L1_B, mặt hết kiểu khỉ, lõi đọc ra đá. B1 nhất quán và dữ nhất, đúng dáng lệch của con gốc, nhưng
cùng tông nâu cam với các con trước và nhiều sọc (lúc chia mảnh nên bớt sọc ở mảnh nhỏ). B2 đọc ra "hành tinh + vệ tinh" rõ nhất, vành
đẹp nhất, nhưng tròn trịa, hiền hơn. B3 ra kiểu tượng đài cổ, dáng lại chính diện, nhiều khía chạm (tốn công mảnh). Claude đề xuất B1,
có thể lấy vành dải phẳng của B2. VÀNH không có trong rig: phải thêm slot mới bám xương lõi (cung trước / cung sau), cho mảnh vành chạy
vòng quanh lõi ở mọi clip (như hành tinh của Nhật Vương).

**Người dùng (2026-11-18): "b3 khá đẹp nhưng có thể lược bỏ vành đai đi hoặc đổi sang đá di chuyển xung quanh, concept là 1 chuyện nhưng
bạn phải chắc chắn về tính khả thi của animation, animation cũng cần phải thật lạ, độc đáo nhưng cũng phải thật đẹp"**, rồi sửa: **"tôi
nhầm, b2 không phải b3"**. Bản được khen là **B2** (hành tinh + các mặt trăng).

## 3c. Concept lượt 3: B2 bỏ vành / mặt trăng nhỏ bay quanh (CHỜ người dùng chọn)

- Làm nhầm trước trên B3 (`tho10.py concept3` → `L3_X.png`, `L3_Y.png`, 190 credit): giữ làm tư liệu, KHÔNG phải bản người dùng chọn.
- Đúng bản: `tho10.py concept3b` (ảnh mẫu 1 = con gốc lấy dáng, 2 = `L2_B2.png` dùng bản có sẵn trên Magnific). Dáng ba phần tư lệch như
  rig, mặt và lưỡi trăng dữ hơn. `L3_B2X.png` = bỏ hẳn vành; `L3_B2Y.png` = năm mặt trăng nhỏ bay quanh (quả cầu nên đúng ở mọi chỗ trên
  quỹ đạo). 190 credit. Claude đề xuất B2Y (trong game dùng 3–4 quả cho đỡ rối mặt hành tinh).

## 3d. Tính khả thi của animation (đo 2026-11-18 từ `scan/monster_3802/sample.json`, 15 clip, 30 khung / giây)

Đã ĐO (chắc):

- Cây xương: `bone5` (lõi) là cha của đầu (`bone6` → `bone7`), hai tay (`bone8..`, `bone16..`), 13 mảnh lưng (`bone79..88`, bám thêm
  `b1..b3`), `bone92..94`; hai chân từ `bone3` (IK `jiao_L/R`). Tâm lõi trong hệ `bone5` = (364, 68), bán kính ~460 đơn vị.
- `bone5` KHÔNG co giãn ở clip nào (giá trị kì dị 1,00..1,00): đĩa hành tinh cứng bám `bone5` luôn tròn. Góc `bone5` lắc 34° ở idle, tới
  ~90° ở skill_02 / skill_04: dải ngang sẽ nghiêng theo; muốn giữ ngang hay nghiêng có chủ ý thì thêm một xương con bù góc.
- Nắm đấm = khối cẳng tay một xương (`bone96` trái, `bone102` phải) + mỗi đốt ngón một xương: mặt trăng + đốt tay khớp 1:1.
- Thứ tự vẽ: idle, hit, block không đổi; run, generate, skill_01_1/2, skill_02, skill_04, skill_05 có tay phải (`P_L_*`, 18–30 slot) đổi
  phía so với lõi (mỗi clip 1–9 thứ tự) → slot sinh đôi như Thanh Long. skill_04 / 05 / generate / die bật thêm slot đá vụn ẩn sẵn.
- Nắm đấm vào gần tâm lõi nhất 228–280 đơn vị (skill_01_3, 03, 04, 05): lúc đó nắm đấm che mặt hành tinh và quỹ đạo vệ tinh (vệ tinh vẽ
  dưới nắm đấm nên không chọi hình, chỉ bị che).
- Không clip nào dời xương `all` (đứng tại chỗ); skill_02 lõi lao ngang −553..248; skill_03 lõi vọt lên y 1757 (nhảy rồi nện);
  generate trồi từ y −514. idle dài 10 s (phải cắt đoạn lặp 2–3,3 s hoặc viết lại).
- Runtime `.atomik` (`AtomikAsset.cs`): khoá xoay, dời, tỉ lệ của xương; đổi hình và độ mờ của slot; sự kiện; mặt nạ cắt đa giác lồi bám
  một xương (bản 3). Vệ tinh trước / sau lõi = slot sinh đôi + độ mờ, đã làm ở Nhật Vương (`vua_may_rig.py`, `quanh_mat_troi`).

CHƯA chứng minh (phải thử chuyển động trước khi chia mảnh): hành tinh tự quay bằng lớp hố + sóng dải trôi ngang dưới mặt nạ TRÒN bám
`bone5` (mặt nạ mới dùng cho mép nước Hải Long, chưa dùng kiểu này); dáng lưỡi trăng lớn ở vai trên các tảng đá vai nổi độc lập.

Ý animation đã đề xuất với người dùng: hành tinh tự quay; vệ tinh bay vòng khác tốc; lưỡi trăng trên lưng nghiêng theo vệ tinh lớn đi
qua (thuỷ triều); đấm thì vệ tinh quất theo, đánh trễ một nhịp; chiêu mana bắn vệ tinh theo tiếp tuyến (far / fly, đường bay bằng mã
như Hỏa Sơn Long); chiêu cuối "trăng rơi" trên skill_03 / skill_04; xuất hiện kiểu trăng mọc trên generate_01; chết thì quỹ đạo rã.
Không làm nhật thực (trùng Nhật Vương).

## 3e. Ủy quyền đêm 2026-11-18 và việc đã làm

Người dùng: **"bạn cứ làm automode, mọi thứ tự quyết đến khi nào xong animation thì thôi. Tuy nhiên không vượt quá budget 3000 credit
gen ảnh, tôi cho bạn quyền tự quyết, làm đi tôi đi ngủ"**. Claude hiểu: dừng ở animation trong `inbox/thach_de_1/rig`, KHÔNG vào game;
trần 3000 tính cả phần đã tiêu. Đã tiêu tổng 1235 credit (13 ảnh × 95).

- **Concept chọn: B2Y** (`L3_B2Y.png` → `L1_duyet.png`).
- **Mảnh** (`thach_de_manh.py`): ba tờ mảnh RỜI, trọn hình, cùng tỉ lệ concept (`tai_ve/M_A.png` hành tinh không hố + hai mặt trăng +
  bốn hố; `M_B.png` đầu, hai vỏ vai, hai khối cẳng tay, năm vệ tinh; `M_C.png` tám lưỡi trăng, tám đốt tay, chân, hông, mảnh vụn), ra
  ngay lượt đầu, đủ 44 mảnh (`manh/`). Không gen theo khung part vì con gốc là mảnh cứng lơ lửng (skill mục 25).
- **Rig** (`thach_de_rig.py`, chạy `SXS=... khoa.py nang -- thach_de_rig.py`): đủ 134 xương của họ dựng ở dáng khung 0 idle, chuyển
  động = `l` của `sample.json`; 34 slot của họ có mảnh của mình (bảng `BANG` + mười lưỡi trăng `LUNG` đứng trên vành hành tinh), còn lại
  ẩn (đá vụn, hàm, mảnh nhỏ). Thứ tự vẽ đổi: 11 slot di động nhân bản theo chỗ chèn (`thu_tu_ve`).
- **Thêm ngoài rig gốc**: `ht` (hành tinh, con bone5) → `tam`; hố `ho_k` (5 hố trôi ngang + co bề ngang = hành tinh tự quay, KHÔNG cần
  mặt nạ); 6 vệ tinh trên chuỗi `quy/quy2/dao` (tâm quỹ đạo nâng lên cho nửa gần đi ngang mặt hành tinh); `dat_cat` mặt nạ đất;
  `far`, `fly_j/bay_j` (bản sao vệ tinh bay), `fly_n/nem` (mặt trăng ném).
- **Clip**: `aura` 12 s (hố trôi, vệ tinh bay vòng, phủ lên mọi clip); `idle` = idle_01 10 s (có cú đấm tay vào lòng bàn tay ở giây 6);
  `walk` = run_01; `appear` = generate_01 + mặt nạ đất (trồi lên như trăng mọc, vệ tinh bung ra lúc đứng vững); `attack` = skill_01_1 +
  lao bằng `move`, trúng 0,55 s, quỹ đạo vệ tinh giật nở; `cast` "Nguyệt Xạ" 1,5 s = skill_05 giãn giờ: vỗ tay gom vệ tinh vào giữa hai
  nắm đấm, dang tay phóng 6 viên tới đối thủ (far), trúng 0,88 s, vệ tinh mọc lại; `skill` "Nguyệt Lạc" 2,2 s = skill_03 giãn giờ: nhảy
  vọt, ở đỉnh ném MẶT TRĂNG NẮM ĐẤM xuống đối thủ (far, trúng 1,18 s), rơi nện đất 1,30 s, nắm đấm mọc lại; `hit` = hit_01 + quỹ đạo văng
  lệch; `die` = die_01, hành tinh rơi xuống nằm trong đống đá rồi tan.
- **Kết quả**: `rig/thach_de_1.atomik` 507 KB (176 xương, 83 slot, 9 clip), mọi clip nối về idle lệch 0 px; `rig/xem.html` mở được
  (thu_xem: đủ nút clip); tờ khung Python `rig/khung_<clip>.png`, tờ khung runtime Spine thật `rig/rt/<clip>.jpg`.
- **Chưa làm / giới hạn**: mới soi tờ khung (Python + runtime Spine), CHƯA xem ở tốc độ thật, chưa chạy trong Unity; đầu chưa có hàm há;
  đá vụn của skill_04 / 05 / generate chưa dùng; cú đấm của họ bật 92° trong một khung (chưa giãn); chưa có VFX hạt Unity (chỉ đặt sự
  kiện `tu`, `nem`, `trung`, `cham_dat`, `troi`, `xong`); chưa làm dạng non, chưa `evolve`; CHƯA vào game.

## 3f. Lượt sửa đòn 2026-11-18 (máy C, sau khi người dùng xem)

Người dùng: **"các chiêu đánh của tướng này còn chưa đẹp, cần cải tiến nhiều"**; đánh thường **"lên cao, dùng 2 tay đập xuống người đối thủ"**;
**"tạo thêm hàm dưới cho tướng"**; cast **"hét gầm lên, các gai sau lưng bắt đầu tách ra nổi lên sau đó lần lượt từng gai xoay hướng vào
mục tiêu rồi lao vào"**; chiêu cuối **"dang 2 tay ngửa lòng bàn tay ra (cần thì gen thêm) rồi từ từ bay lên trời, sau đó rất nhiều tiểu
hành tinh / thiên thạch / đá sẽ lao vào bám xung quanh đối thủ, sau đó tướng ép 2 tay gần vào nhau ở phía trước, các hành tinh quanh đối
thủ co nhỏ lại (tướng ở trong cũng phải co theo để không bị lộ) rồi triệu hồi 1 mặt trời trên đầu đối thủ rồi bắn 1 tia nhiệt cực lớn
xuống tạo ra 1 vụ nổ hình nấm, đá văng tứ tung (vfx làm thêm cho hoành tráng)"**.

- Máy C chưa có `scan/monster_3802` (thư mục `rig/` bị gitignore): quét lại bằng `mo_xe/chay.py info / att "anim=idle_01&t=0" / sample
  <15 clip> 30` vào `D:\Ripper\SwordxStaff\scan\monster_3802\`.
- **Tờ D** (`thach_de_manh.py prompt_d` → `gui_gpt/thach_de_1/luot_5_manh_D.txt`, gen bằng Codex, 0 credit Magnific; tổng vẫn 1235):
  đầu trên (bỏ hàm, có hàng nanh trên), hàm dưới kèm lòng miệng, hai nanh rời, bàn tay to / nhỏ xoè ngửa. Ra đúng ngay lượt đầu.
- **Ghép đầu** (`thach_de_dau.py`): đầu trên dò tỉ lệ + dời cho vùng trên miệng trùng đầu cũ (IoU 0,956, tỉ lệ 0,745); nanh theo vùng kem
  của đầu cũ; hàm đặt cho răng dưới cài vào khe nanh trên lúc ngậm (cằm cao lên 19 px so với đầu cũ, nanh dời theo); lòng miệng ngoài hình
  bóng đầu trên (co 14 px) bị cắt, kẻ lại viền → `manh/ham_cat.png`. Tờ so `manh/_dau_so.png` (đầu cũ, há 0 / 14 / 28°). Há quá ~20° thì
  lòng miệng lòi ra sau má phải: rig dùng tối đa `HA = 19°`.
- **Rig** (`thach_de_rig.py`): xương `ham` (con bone7, bản lề sau miệng), slot `ham@k` (sau đầu) và `nanh_1@k`, `nanh_2@k` (trước đầu) đi
  theo độ đậm của `P_tou1@k`; bàn tay xoè `tay_xoe_to` (bone96), `tay_xoe_nho@k` (bone102) đi kèm mặt trăng nắm đấm, `dat_dang(xoe=...)`
  đổi trong một khung; mỗi lưỡi trăng lưng có xương riêng `gai_i` ở đế (trục x chĩa ra theo bán kính). Bỏ phần bay mặt trăng cũ
  (`fly_j`, `fly_n`); không khai `far` cho clip nào (gai, mặt trời do VFX lái). Thêm `tron()` trộn dáng nhiều clip gốc, `dich_tg` / `dat_tg`
  đặt xương theo trục thế giới; `span = 5,0` (chiêu cuối bay lên 0,72 chiều cao, tay giơ quá đầu).
- **attack "Thiên Chuỳ"** 1,40 s (trúng 0,68): skill_03 của họ giãn giờ (nhún, nhảy, ôm hai nắm đấm quá đầu), lao (`move`, sân nắn tới
  72 % quãng), hai nắm đấm đưa ra trước 0,36 / 0,22 chiều cao rồi nện; há quát ở đỉnh, nghiến răng lúc nện; thân nén, quỹ đạo vệ tinh bung.
  Cú vung tay vẫn nhanh (60 khung/giây: đốt tay đi ~470 đơn vị một khung) vì đó là tốc độ cú nện của clip gốc: người dùng xem rồi quyết.
- **cast "Nguyệt Nhận"** 2,10 s: idle trộn dáng dang của skill_05, ngửa đầu 28°, đầu phồng 7 %, há 19° run (gầm 0,32–0,92); mười lưỡi bứt
  khỏi vành (0,30 + 0,024 i), nổi thành vòng quạt quanh lưng, lần lượt (trước → sau) xoay mũi về đích, giật lùi rồi PHÓNG: sự kiện `ban`
  (chuỗi = số gai) ở 0,98 + 0,062 j, rig ẩn gai tại chỗ, VFX bay 0,20 s; `trung` = 1,192; lưỡi mới mọc lại từ vành (1,52 → 2,04).
- **skill "Hằng Tinh Diệt"** 4,70 s: dang tay (dáng dang skill_05) đổi sang bàn tay xoè ngửa ở 0,16; bay lên 0,36 → 1,45 (xương `all`,
  0,72 chiều cao, nhấp nhô); hai tay nâng nhịp gọi đá 1,0 → 2,15 (`hut`); ép 2,15 → 2,83 (`ep`): hai bàn tay xuống thấp trước bụng, lòng quay
  vào nhau, run, vệ tinh co sát lõi; gọi mặt trời 3,05 (`goi`, `gam`): hai tay giơ cao chữ V, há gầm; vung tay ra lệnh 3,40 (`tia`), đổi về
  nắm đấm; nổ 3,48 (`trung`); hạ xuống, đáp đất 4,15 (`cham_dat`).
- idle có gầm gừ khẽ ở 2,3 s; appear há gầm khi vừa đứng vững; hit bật há; die hàm trễ há.
- Đo: `thach_de_rig.py kiem` (bước xoay lớn nhất mỗi khung: attack 113° = cú nện của họ; cast 151° ở gai đang ẩn; skill 73° lúc đổi bàn tay),
  `chay.py sample ... 60` (skill tối đa 172 đơn vị / khung sau khi bỏ cú vung giữa chừng). Mọi clip nối về idle lệch 0 px. .atomik 592 KB.
- **Bản xem trước VFX** (`thach_de_fx.py`, rig thật + đối thủ + hạt phẳng, như `tho5_fx.py`) → `inbox/thach_de_1/fx/xem.html`:
  attack (bụi bật, nện: sao kem, dăm, nứt đất, đối thủ bẹp); cast (sóng gầm kem, đất rung, vụn ở đế gai, gai bay có bóng mờ + vệt bụi, cắm
  vào thân rồi vỡ); skill (sỏi nổi lên theo khi bay; 45 thiên thạch / đá trăng có đuôi lửa hoặc bụi lao tới bám thành vỏ cầu quanh đối thủ,
  nửa sau vẽ sau đối thủ; ép: vỏ co còn 44 %, đối thủ co theo, bụi dăm phì ra; mặt trời đĩa phẳng bốn lớp + vành lưỡi lửa quay; tia nhiệt
  mảng liền bốn lớp mép gợn; nổ: chớp, rung, vỏ đá văng tứ tung, cầu lửa, vành bụi, mây nấm dựng hình (cột + mũ vòm + cuộn mép, lửa → than
  → xám, cả khối trong 0,82 vì phủ lên đối thủ); đáp đất). Trong game: lớp hạt Unity làm lại theo bản này, game phải co đối thủ theo `ep`.

Chưa làm: chưa vào game / Unity (vẫn chờ: thay `giap_nham`? tên? số dạng?), chưa có VFX C#, chưa làm dạng non.

## 3g. Vào game 2026-11-18 (người dùng: "ok cho vào game đi rồi gen dạng 1 của nó")

- Thay hẳn suất 10 `giap_nham` (giữ id, chỉ số, hiệu ứng thẻ, không đổi bản lưu / golden số): `quai/doi_thach_de.py`. Tên Claude đặt, người
  dùng đổi được: **Thổ Tinh**, "Hành tinh đá gọi mặt trời", "Dòng Thổ Tinh"; thẻ Nguyệt Nhận (moon), Hằng Tinh Diệt (sun), Vệ Tinh Hộ
  Thể (shield), thẻ boss Lõi Hành Tinh (rock). Hai dạng tạm chung `Resources/thach_de_1` (cỡ 0,92 / 1,1); có rig dạng 1 thì
  `doi_thach_de.py chep_non <rig>` + `dang_1` (dạng 1 "Tiểu Thổ Tinh" → `thach_de_non`). RosterTests sửa dòng giap_nham.
- Unity (máy C): refresh, "Nhập dữ liệu", "Gắn dạng .atomik" (prefab giap_nham giữ 2 dạng thach_de_1), xoá `Resources/giap_nham_1`, `_2`.
- VFX C# (agent làm theo `thach_de_fx.py`): `Game/Battle/HatThoTinh.cs` (mã `n_tinh_nen` đòn thường, `n_tinh_gai` chiêu mana, `n_tinh_hang`
  chiêu cuối; lưỡi trăng, đá trăng vẽ bằng mảng đa giác / hạt có sẵn vì mã chạy không tạo sprite; mây nấm là hợp các hình tròn một mảng,
  trong 0,82), `Game/Battle/StageViewThoTinh.cs` (đối thủ co theo vỏ đá 2,15 → 2,83 còn ~0,405, bật về lúc nổ 3,48; bẹp lúc nện; giật
  theo từng lưỡi), dòng thêm ở `StageView.ThoFx` / `ThoAtk` / `Place` (`TinhDat`), `HatNuoc` (ba case), `HatVoi.AtkLao` (`n_tinh_nen`).
  Số điểm bám đo bằng `ArtGen/Spine/thach_de_do_hat.py`. Menu thử: `Editor/ThoTinhFxTour.cs` (ảnh `Temp/PokiShots/tho_fx/tinh_*.jpg`).

- 2026-11-18 sau tour, người dùng: **"khi tia năng lượng bắn xuống phải nổ thật epic, sau đó nổ xong có khói đen tỏa ra thì hiện tướng đằng
  sau khói đen mờ mờ cho mượt chứ không hiện tướng luôn sẽ bị kiểu hơi lỗi"**. Sửa trong game (`HatThoTinh.cs` mục 6, `StageViewThoTinh.cs`):
  chớp + rung hai nhịp, sao chớp lớn, cầu lửa bốn lớp hợp tròn (`TtCauLua`: phình 0,16 s, bốc lên, lõi co trước, lớp ngoài nguội thành than),
  cột lửa vọt theo tia 0,32 s, hai vòng sóng đứng + sóng sát đất + vành bụi, 40 dăm, 24 lưỡi lửa, 26 tia lửa, năm vết nứt, ba tiếng nổ phụ,
  KHÓI ĐEN dày (72 cụm / giây trong 0,52 s, phần lớn lớp trước phủ chỗ đối thủ, cụm thấp lan ngang; tan dần 1,7–2,4 s). Đối thủ ẩn từ lúc nổ
  tới +0,45 s rồi hiện MỜ DẦN tới +1,25 s sau làn khói (`HatLua.TinhHienDoiThu`, `TinhDat(..., ref alpha)`), bóng lớn dần theo.

## 4. Việc tiếp (sau khi người dùng xem)

0. Rig THỬ CHUYỂN ĐỘNG trước (da gốc + hình giữ chỗ: đĩa hành tinh có mặt nạ, vệ tinh, lưỡi trăng) cho idle, một cú đấm, một chiêu.
1. Chép bản chọn thành `L1_duyet.png`; nếu cần thì gen lượt nữa sửa chi tiết.
2. Tờ mổ từng part + tờ khung part (cách "khung part", skill pokiclash-spine-rig mục 00, 23); mẫu gần nhất `tinh_hach_manh.py`,
   `tinh_hach_rig.py`.
3. Hỏi gom: thay suất `giap_nham`? tên? số dạng (dạng 1 non)? ghép 8 clip chiêu vào 3 ô chiêu thế nào?
