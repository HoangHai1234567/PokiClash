# Quỷ lửa cầm đao lớn (`quy_dao`): tướng thứ 7 đảo Hỏa

Bắt đầu 2026-11-13 (máy ổ C). Con gốc của rig: `monster_3655` (quỷ lửa lưng gù, bờm lửa, vác kiếm khổng lồ; game tham khảo, kho
`D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `idle_01`). Xương, lưới, chuyển động gốc là của nhà phát hành game
đó (như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình. Tên, id game: chưa đặt (`quy_dao` chỉ là mã làm việc).

## 1. Lời dặn của người dùng (2026-11-13)

- "làm tướng thứ 7 đảo hỏa; concept **quỷ lửa cầm đao lớn**".
- "**idle làm khác con gốc** đi, **walk cũng vậy**".
- Đánh thường: "**vung đao chém một cách nặng nề nhưng impact lớn**".
- Chiêu cast mana: "làm **giống skill_01**, có thể **đổi nhẹ** đi một chút".
- Chiêu cuối: "làm **giống skill_04_1**, **lao tới rồi thực hiện liên hoàn chém** giống animation gốc".
- "**chết, appear** bạn có thể **tự làm**".
- Sau lượt concept 1: "tôi thích **dạng C** nhưng **đổi sừng sang đen đậm**".
- Sau khi xem rig: "**thêm trail dọc lưỡi đao**, trail **cam mờ mờ** thôi, kiểu thể hiện **nhát chém splash**".
- "**đưa tướng này vào game**" (2026-11-13; cho dừng Play để làm).

## 2. Mổ rig gốc (`<SXS>/scan/monster_3655/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample.json` 30 khung/giây, `mo/`, `parts/`, `khung/`, `khung_rong/`)

64 xương, 46 slot, 17 clip, 12657 khoá; 44 hình có ảnh. Con **nhìn sang PHẢI**. Ảnh atlas 0,5 px / đơn vị rig (cả con cao ~1000 đơn vị kể vũ khí).

Ràng buộc (đều đã nướng thành FK qua mẫu khung `l`):
- IK hai chân (`xiaotui_r2`, `xiaotui_l2`: đích là con của `bone2`), mix 1.
- IK tay GẦN (`target`: dabi_r + xiaobi_r; `target2`: shou_r): đích là xương con của VŨ KHÍ (`wuqi_02 → target2 → target`), mix 0 ↔ 1 theo clip.
- Transform `wuq`: xương vũ khí `wuqi_02` (con của `bone`, KHÔNG phải con của tay) bám CỨNG bàn tay xa `shou_l` (mix 1; skill_04 cuối, stun, die: 0).
  → hễ tự sửa thân / pha dáng thì phải tính lại `wuqi_02` theo `shou_l` (`quy_dao_rig.dao_theo_tay`), không thì đao rời tay.
- Transform `s1`, `s2`, `t`: nhích vai, đầu theo xương `s`, `t` (8 %, 50 %).
- `wuqi_03` (xương mang ảnh vũ khí; trục x = chuôi → mũi, gốc ở chỗ tay nắm) có xô lệch tới 27° + phóng 1,5 lần trong skill_04 (nhoè phối cảnh): rig
  mình bỏ phần xô lệch (định dạng không có), giữ tỉ lệ.

Bảng mảnh ở idle (thứ tự vẽ sau → trước; ảnh px atlas):
| thứ tự | slot | ảnh | là gì | xương |
|---|---|---|---|---|
| 1, 2 | `s_05`, `s_04` | | hình bàn tay xa kiểu khác (`s_01`, `s_02`; ẩn, chỉ skill_04) | shou_l |
| 3, 4 | `hsouzhitou` (+ `s_03`), `damuzhi_l` | 21 × 25, 50 × 39 | đầu ngón + ngón cái tay xa (sau vũ khí) | shou_l |
| 6 | `wuqi_02` | 154 × 541 | VŨ KHÍ (kiếm liền một ảnh) | wuqi_03 |
| 7, 8, 9 | `dabi_l`, `xiaobi_l`, `shou_l` | 156 × 157, 174 × 90, 81 × 46 | tay XA: bắp, cẳng, nắm tay (trước vũ khí) | từng xương |
| 10 | `jiajia_l` | 174 × 168 | giáp bắp tay xa (vòng cung) | dabi_l |
| 11, 12 | `yao`, `shenti` | 150 × 101, 248 × 222 | bụng, ngực (hai khối tròn chồng nhau) | yao2, shenti |
| 13–18 | `xiaotui_l`, `tuishi_02`, `datui_l`, `datui_r`, `tuishi_01`, `xiaotui_r` | | hai chân: ống (lưới 2 xương), đùi, hai mảnh giáp gối | |
| 19–23 | `yaojia_05/04/03/02/01` | | đai + khố: ba mảnh giáp, khố có nút sáng, khoá đai | yao, yaojia_04, yaojia_02 |
| 24 | `dajiao_l` | 97 × 129 | sừng XA | dajiao_l |
| 25–29 | `toufa_01/07/03/02/06` | tới 250 × 223 | NĂM BÚI BỜM (lưới 18–47 đỉnh, mỗi búi một chuỗi 3–4 xương) | toufa_* |
| 30 | `shouzhi_01` | 21 × 33 | ngón cái tay gần | shouzhi_01 |
| 31 | `lian_01` | 107 × 77 | mặt nạ (lưới 50 đỉnh) | lian_01 |
| 32 | `huzi` | 124 × 96 | râu (lưới, 2 xương), ĐÈ lên mép dưới mặt nạ | huzi, huzi2 |
| 33–36 | `jiao_04..01` | | bốn gai rời trên trán | jiao_* |
| 37 | `dajiao_r` | 155 × 186 | sừng GẦN | dajiao_r |
| 38, 39, 40 | `dabi_r`, `xiaobi_r`, `shou_r` | 184 × 168, 150 × 100, 63 × 63 | tay GẦN: bắp, cẳng (liền bao tay), mu bàn tay | |
| 41–44 | `shouzhi_02..05` | | bốn ngón vuốt (lưới 2–3 xương mỗi ngón) | shouzhi_* |
| 45 | `jianjia` | 189 × 210 | GIÁP VAI gần (trên cùng) | dabi_r |

**Đổi thứ tự vẽ trong clip**: vũ khí + nắm tay xa (và ngón, cẳng, giáp tay xa ở skill_04) chui ra trước chân / đai / bờm / mặt / cả thân. Rig mình:
slot "di động" (9 slot) nhân bản ở từng chỗ chèn (`<slot>@<số slot đứng yên vẽ trước nó>`), mỗi khung bật đúng bản (`quy_dao_rig._thu_tu`, `hien_theo_ho`).

Clip của họ (tờ `khung/`, `khung_rong/`):
| clip | dài | động tác | dùng cho |
|---|---|---|---|
| `idle_01` | 1,33 s | thở, bờm bay | nền **idle** (kéo giãn + trò riêng) |
| `run_01` | 1,33 s | lom khom bước, kiếm kéo thấp sau lưng | chân + hông của **walk** |
| `skill_01_1/2/3` | 1,93 s | xốc kiếm lên vai, nắm hai tay 0–0,59; giơ quá đầu 0,67–0,80; bổ cắm đất 0,87–0,93; giữ tới 1,26; rút về | **cast** |
| `skill_02_1/2/3` | 1,30 s | xốc kiếm lên vai 0–0,24, giữ tới 0,59, ngả sau 0,71, bổ xuống trước 0,83, về | **attack** |
| `skill_03` | 2,47 s | dựng kiếm trước mặt 0,22–0,67; dang hai tay ưỡn ngực 0,9–2,0; về | dáng **gầm** của appear |
| `skill_04_1/2/3` | 2,43 s | thu người 0–0,2; liên hoàn chém 0,27–1,16 (quét ngang, xoay chém, hất lên, bổ); đâm 1,27; bật nhảy vọt khỏi khung 1,40–1,73; rơi bổ cắm đất 1,87; đứng dậy | **skill**; đoạn rơi làm **appear** |
| `hit_01/02`, `block_01`, `stun_01` | | | **hit** = hit_01 |
| `die_01` | 1,00 s | bật ngửa, kiếm cắm thẳng xuống đất, đổ sấp trước kiếm | nền **die** |
Bản `_1/_2/_3` chỉ khác quãng trôi ngang của `bone2`. Hướng chém: xương vũ khí quay THUẬN kim lúc bổ → lưỡi sắc ở phía −y của xương `wuqi_03`
(dáng nghỉ: lưỡi quay xuống dưới - trái, sống đao quay lên trên - phải).

## 3. Concept

Script: `quy_dao.py` (`mo`, `nhom`, `part_goc`), `quy_dao_bo_cuc.py` (sơ đồ bố cục 1536 × 1024 ở khung 0 idle, 0,824 px / đơn vị rig, gốc rig ở
(646,8; 930,2)), `build_quy_dao.py` (gói `gui_gpt/quy_dao_1/`; ảnh mẫu: sơ đồ, Voọc Tướng, golem lõi lửa, bản đồ).

Giữ của con gốc: dáng (quỷ lưng gù nhìn phải, tay gần to buông trước, tay xa vòng lên sau đầu nắm cán, vũ khí khổng lồ dựng chéo sau lưng, chân
ngắn), chỗ, cỡ, thứ tự chồng. Đổi dáng ngay từ sơ đồ (đề xuất của Claude; các mảnh này cứng một xương nên đổi tự do): kiếm chắn tay hình sao →
**ĐAO một lưỡi** (khâu tròn ở chuôi, chắn tay bầu nhỏ, bản loe dần, sống có một khấc, mũi vát, dải lưỡi nung cam ở phía dẫn đầu cú chém); hai sừng
chữ S → **sừng nón**; mặt nạ đá + bốn gai rời → **mặt nạ quỷ liền, mào ba mũi** (bốn slot gai bỏ); giáp vai nhiều gai → **vòm tròn có vành, một
gai cong**; bờm → **lửa thật ba vùng màu phẳng** (viền ngoài thêm lưỡi lửa nhọn).

Lượt 1 (108–112 s mỗi ảnh, cả ba bám sơ đồ ngay lượt đầu): `quy_dao_1/tai_ve/L1_do_tham.png` (A: da đỏ thẫm, mặt nạ + sừng ngà, giáp sắt đen),
`L1_than.png` (B: da xám than, giáp đồng, mặt nạ đỏ son), `L1_tro.png` (C: da tro nhạt, mặt nạ + giáp sắt đen, sừng đỏ thẫm, vải đỏ sẫm). Trang
so `inbox/quy_dao_xem_concept.html`.

**Người dùng chọn C, đổi sừng sang đen đậm** → lượt 1b (`build_quy_dao.py sung` → `luot_1b_sung_den.txt`): vẽ lại đúng `L1_tro.png`, chỉ đổi màu
hai sừng thành đen than #1E1C21 → `tai_ve/L1b_tro_sung_den.png`.

## 4. Rig thử trên DA GỐC (làm trong lúc chờ concept; không phụ thuộc màu)

`QD_GOC=1 py -3 -I quy_dao_rig.py` → `quy_dao_1/rig_goc/` (`xem.html`, tờ khung, `.atomik` 197 KB): 69 xương (64 của họ + root, move, far, mui_dao,
than_dao, mieng), 77 slot (kể bản nhân của slot di động), 622 đỉnh; chiều cao game 760. Dựng lại trùng con gốc.

Clip (9):
- `aura` 4 s (lặp, phủ mọi clip): sóng chạy gốc → ngọn trên năm búi bờm + râu, lệch pha, phập phồng nhẹ.
- `idle` 4 s (KHÁC con gốc): nhịp thở idle_01 kéo giãn 1,5 lần, biên độ × 1,25; 1,95–2,8 s XỐC ĐAO trên vai (pha 62 % sang dáng skill_02 @ 0,15 s)
  rồi thả, nảy tắt dần; 0,45–1,6 s bấu vuốt; đầu gườm; lửa bùng theo cú xốc.
- `walk` 1,33 s (KHÁC con gốc): chân, hông, thân của run_01; tay xa nâng 27° cho bản đao rời đất nằm gần ngang sau đầu (VÁC ĐAO TRÊN VAI), đao nảy
  theo hai bước giậm (0,02 và 0,76 s, sự kiện `buoc`), tay gần đánh mạnh, ngực ưỡn.
- `hit` 0,5 s: hit_01.
- `attack` 1,90 s: nhát bổ CỐI XAY của skill_04 (u 0,585 → 1,0), co giãn giờ: pha từ idle sang dáng GIƠ ĐAO DỰNG ĐỨNG 0–0,34; gồng 0,34–0,52; quay
  đao một vòng nặng nề ra sau lưng 0,52–0,84; BỔ qua đầu xuống trước mặt 0,84–0,92 (trúng 0,92; bản đao lộ trọn, quét từ sau ra trước); đao ghì sát
  đất, khựng tới 1,22; nhấc chuôi lên (pha sang dáng đao ghì của skill_02 @ 0,90) tới 1,50; đoạn thu về của skill_02 tới 1,90. Lao 0,50 chiều cao
  (25 % lúc quay đao, 75 % theo cú bổ); bỏ độ trôi `bone2` của họ. Rung + bẹp ở `move` lúc trúng.
  (Bản đầu dựng trên skill_02, xốc đao lên vai rồi bổ: bản đao nằm KHUẤT sau thân suốt cú bổ, không thấy "vung" → bỏ.)
- `cast` 2,15 s: skill_01: nắm hai tay giơ quá đầu 0,64; GỒNG tụ lửa 0,64–1,04 (run, bờm bùng 1,3 lần; sự kiện `tu` 0,60); bổ cắm đất 1,14
  (`nen` = `trung`); giữ tới 1,60; rút về. Đứng tại chỗ; `mieng` = mũi đao (chỗ lửa trào theo đất: VFX).
- `skill` 2,67 s: skill_04_1 nguyên nhịp + LAO TỚI 0,10–0,28 (0,62 chiều cao); bảy nhát (`chem` 0,30 / 0,42 / 0,60 / 0,74 / 0,86 / 0,98 / 1,24);
  bật nhảy 1,38 (giữ 50 % độ cao của họ: họ vọt khỏi khung); bổ cắm đất 1,87 (`nen` = `trung`); lùi về từ 2,17. Trừ 60 % độ trôi ngang `bone2` của họ.
- `appear` 2,32 s (tự làm): khung đầu trống; rơi từ trên xuống bổ đao cắm đất (đoạn u 1,755 → 1,87 của skill_04 giãn ra 0,27 s, nhanh dần, giữ
  58 % độ cao; `nen` 0,27); rút đao đứng dậy 0,62–1,04; dang tay GẦM 1,24–1,74 (dáng skill_03 @ 1,0 s; `gam`); về thế.
- `die` 1,82 s (tự làm): die_01 (bật ngửa, đao cắm đất, đổ sấp; khung đầu của họ bật tức thì 300 đơn vị nên giãn ra 0,10 s) + bờm lửa lụi
  từ 0,50 (co còn 28 %), mờ dần 0,35 s cuối.

Bẫy đã gặp:
- Góc đã nướng của tay cộng dồn nhiều vòng sau liên hoàn chém; chỗ nối sang dáng khác lệch bội 360° trong một khung → hậu kỳ `GoVong` (mọi clip):
  bước xoay > 180° giữa hai khung thì dời phần sau về cùng vòng (kể cả xương vắng mặt ở khung sau). Pha hai dáng thì quy góc về cùng vòng trước
  (`pha_gan`).
- Pha dáng "đao ghì trước mặt" về dáng thu đao: từng xương tay xa đi đường ngắn nhất (−141°, −117°, −30°) nhưng CỘNG lại đao quay 288° trong 0,2 s
  (đao vụt một vòng) → `pha_tay`: tổng góc chuỗi tay xa vượt nửa vòng thì cho bắp tay quay chiều kia; đao giữ hướng, tay vòng qua phía trước.
- Cú bổ của họ là khoá BẬC (đao đứng yên 0,80–0,833 s rồi nhảy sang dáng đã bổ ở 0,842 s; lấy mẫu 120 khung/giây mới thấy). Nội suy thẳng hai dáng đó
  cho đao đi qua đầu (đúng cung chém), nên giãn cú bổ ra 0,08 s vẫn đọc được.
- Walk bản đầu lấy thân trên từ dáng vác của skill_02 @ 0,40 s còn hông từ run_01: không ra dáng vác (dáng đó nằm ở hông ngả sau 27° + lùi 126 đơn
  vị) → đổi sang run_01 trọn + nâng tay xa.
- Đo runtime thật 60 khung/giây (`chay.py sample … 60`): cú rơi của appear 449 đơn vị / khung (chưa kịp thấy) → giãn; khung đầu die bật 306 đơn vị → giãn.

Mọi clip nối về idle 0 px; appear khung đầu trống, die khung cuối trống. Trang `rig_goc/xem.html` (thu_xem: đủ 8 clip + chạy nối).

## 5. Mảnh và rig da của mình (2026-11-13 chiều)

Concept chốt: `tai_ve/L1b_tro_sung_den.png` = `L1_duyet.png` (bản C, sừng đen than; vẽ lại đúng bản C, mọi thứ khác trùng).

`quy_dao_da.py` (ba loại mảnh; `to` dựng tờ + prompt `gui_gpt/quy_dao_1/luot_2_*.txt`):
- **Giữ dáng, tờ mảnh GỐC cắt theo lưới** → `D_A` (ngực, bụng, hai bắp tay, hai cẳng tay, giáp tay xa; phóng 2,2), `D_B` (đùi, ống chân, khố, đai, giáp gối,
  mu bàn tay, nắm tay xa; 2,9), `D_C` (ngón, vuốt, ba mảnh bàn tay xa mở; 5,5). `cat` → `manh/<vùng>.png` (ảnh vùng × 2). Độ khớp hình bóng 0,91–0,98
  ngay lượt đầu; màu da ba tờ trùng nhau (207, 191, 178), không phải cân màu.
- **Bờm lửa + râu** → tờ `L` (ô = búi của rig + lưỡi lửa do mã thêm, tỉ lệ sơ đồ × 1,12); `cat_lua` → `manh/toufa_*.png`, `huzi.png` + `dat_moi.json`
  (`goc`, `ti`). Bản `D_L.png` khớp 0,94–0,97 nhưng GPT CHÉP Y lưỡi răng cưa của sơ đồ máy vẽ (cứng, không ra lửa của concept) → bản TẠM. Bản 2
  (`luot_2b_lua_L.txt` → `D_L2.png`: giữ chỗ, cỡ, hướng; vẽ lại viền thành lửa tự nhiên) CHƯA gen: Codex hết hạn mức 16:05, báo có lại 18:30;
  `quy_dao_cho_gen.py 18:32 …` đang chạy tách, tự gen khi có hạn mức (nhật ký `inbox/quy_dao_cho_gen.log`). Có `D_L2.png` thì: `quy_dao_da.py cat_lua`
  → `quy_dao_rig.py` → soi → mở lại `rig/xem.html`.
- **Đổi dáng, "đúng chỗ, đúng cỡ" từ concept** → `M_DAO` (đao trọn cây), `M_MAT` (mặt nạ + giáp vai), `M_SUNG` (hai sừng đen). `cat_moi` đặt từng mảnh
  bằng phép đồng dạng riêng (`dat_moi.json` trường `M`): đao = hai điểm (mép ngoài khâu tròn, mũi) ↔ trục đao của rig (1,029 đơn vị / px, xoay 1,7°);
  mặt nạ neo hai mắt (1,214); giáp vai neo đáy vòm (1,038); sừng gần neo gốc sừng ở mép trên trái mặt nạ (1,08); sừng xa neo mũi (1,026). Concept
  vẽ to hơn sơ đồ ~15 % nên không đặt theo toạ độ concept. Dọn bằng mã: đục lỗ khâu tròn; dải mép 2 px lấy màu tối nhất quanh nó (hết viền sáng quanh
  sừng đen, đao); chừa 4 px trong suốt quanh mảnh (mép ảnh chạm mảnh thì atlas lem vạch trắng).

Rig `quy_dao_1/rig/` (`py -3 -I quy_dao_rig.py`): 69 xương, 73 slot, 1975 đỉnh, atlas 1072 × 1264, `.atomik` 339 KB (dưới trần 0,5 MB). Mảnh giữ dáng lắp
nguyên lưới của họ (0,72 px / đơn vị); mảnh trong `dat_moi.json` dùng lưới dày của mình bám lưới của họ (đỉnh ngoài lưới gốc: trọng số của điểm gần
nhất, làm trơn 40 vòng theo cạnh lưới: lưỡi lửa không bị xé). Bốn slot gai trán `jiao_*` bỏ. `mieng` = điểm trước mặt sát đất (430, 40) trên `move`
(chỗ đao bổ xuống ở cast). Soi runtime thật: `rig/that/` (tờ khung từng clip), `rig/that_can/idle.jpg` (cận, không còn viền sáng, vạch trắng).

**Vệt chém dọc lưỡi đao** (người dùng dặn sau khi xem rig; nằm TRONG rig vì phải bám đúng lưỡi đao từng khung): slot `vet` trên cùng, một dải
lưới 11 cột × 5 hàng: hàng = năm điểm dọc lưỡi sắc (u 0,40 → mũi), cột 0 bám xương vũ khí, cột k bám xương `vet_k` (con của root) = biến đổi
thế giới của xương vũ khí ở k / 120 giây trước (hậu kỳ `VetDao` tính lại dáng bằng hàm của clip, kể cả phần lao). Đao đứng yên thì các cột trùng
nhau. Ảnh 96 × 64: cam #F7902A nhạt dần về đuôi, một vạch vàng cam theo cung mũi đao; độ đậm tối đa 0,42, theo tốc độ mũi đao lớn nhất trong
cửa sổ vệt (4500 → 9500 đơn vị / giây), chỉ bật trong đoạn chém: attack 0,60–1,15; cast 0,95–1,45; skill cả clip; appear 0–0,50.
`game.plain = ["vet"]` (vẽ không viền sticker). Cú bổ của attack giãn đúng khung nhảy bậc của họ (u 25/30 → 26/30) ra 0,08 s nên vệt ra một cung
tròn qua đầu. Soi runtime thật: `rig/that_vet/`, `rig/that/skill.jpg`.

## 6. Vào game (2026-11-13, người dùng: "đưa tướng này vào game")

Suất 7 đảo Hỏa = ải 40 của đảo ("Lò Rèn Gai Thép", `IslandGen.Plan Hoa`), id **`giap_long`** (trước là Giáp Long). GIỮ id tướng, id thẻ, chỉ số, hiệu
ứng thẻ, số dạng (2) → golden không đổi, không đổi saveVersion.
- `quai/doi_quy_dao.py` (`--kiem`, `--ve_cu`, `chep`): `heroes.json` khối `giap_long` (tên **Viêm Đao** cả hai dạng, danh hiệu "Quỷ lửa vác đại đao",
  dòng "Dòng Viêm Đao", `aola` tướng + hai dạng → `quy_dao_1`; cỡ 0,92 / 1,1 giữ); `cards.json`: Gai Thép → **Địa Hỏa Trảm** (flame), Thiết Long Xung
  → **Liên Hoàn Đao** (sword), Giáp Gai → **Giáp Vai Sắt**. Tên do Claude đặt, người dùng có thể đổi. `chep`: `rig/quy_dao_1.atomik` +
  `chan_dung.png` → `Assets/03 Art/Heroes/Resources/quy_dao_1/` (thư mục mới; `giap_long_1`, `giap_long_2` cũ giữ nguyên).
- Mã: `HatLua.Themes["giap_long"]` = lửa cam thường + mảnh giáp sắt đen; `HatLua.PlayMana` thêm mã **`dat_trao`** = `Eruption(foeFeet)` (bổ đao cắm
  đất, dung nham trào dưới chân địch); `StageView.FireFx["giap_long"] = ("dat_trao", "no_lon")` (chiêu cuối: nổ lớn ở địch đúng khung bổ kết);
  `HoaFxTour`: menu "Đảo Hỏa: riêng Viêm Đao, đòn thường, chiêu mana, chiêu cuối (đang Play)" + `giap_long` trong điều kiện đòn thường.
  `GD_Claude/13_DanhSachTuong.md` dòng ải 40 ghi thêm.
- Unity (cầu MCP cổng 8080; đã báo bốn phiên khác, người dùng cho dừng Play): refresh (biên dịch sạch), "Nhập dữ liệu" (88 tướng), "Gắn dạng .atomik
  vào prefab tướng" (`giap_long.prefab` → `quy_dao_1.asset`), EditMode **102 / 103** (chỉ hỏng `PrefabOnlyTests` cũ ở `UI/Kit`, không liên quan).
- **Trong trận** (tour Viêm Đao, ải 3, sao cuối = dạng 2; ảnh `Temp/PokiShots/hoa_fx/giap_long_*`, tờ `rig/_game_danh.jpg`, `_game_mana.jpg`,
  `_game_ult.jpg`): viền sticker và lật trái phải đúng; đòn thường giơ đao, lao tới bổ đúng chỗ địch; chiêu mana bổ đao cắm đất, dung nham trào dưới
  chân địch; chiêu cuối lao tới liên hoàn chém (vệt cam theo từng nhát), nhảy bổ, chớp màn + nổ lớn ở địch, lùi về. Console không lỗi.
- **Hai lỗi chỉ lộ trong trận, đã sửa rồi chạy lại tour:** (1) game GIỮ dáng ở khung trúng (~0,3 s + khựng) đúng lúc vệt chém to nhất → vệt đứng
  hình thành mảng cam phủ lên người → `VetDao` cho vệt tắt hẳn từ 0,05 s trước khung trúng tới 0,22 s sau; (2) đòn thường tôi xoá độ trôi `bone2`
  của họ nên cả thân lùi ~190 đơn vị khỏi bệ lúc giơ đao (ở dáng đó thân vốn ngả về sau đúng chừng ấy so với chân) → giữ nguyên `bone2`.

CHƯA làm: VFX riêng (bụi + vòng lửa ở chỗ đao cắm, vệt chém bằng hạt); `appear` / `die` của rig chưa được trận phát (`StageView` vẫn dùng rơi xuống /
nghiêng mờ chung); dạng 1 riêng (hai dạng đang chung một rig, chỉ khác cỡ); chưa thử trên Android; cú nhảy của chiêu cuối chạm mép trên màn hình.

## 7. Việc tiếp

- Bờm lửa bản 2 (xem mục 5) rồi dựng lại rig.
- VFX ngoài rig: vệt chém theo `mui_dao` / `than_dao`, lửa trào theo đất (cast), bụi + vòng lửa lúc `nen`.
- Dạng 1 riêng, tên chính thức: chờ người dùng.
