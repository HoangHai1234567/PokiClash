# Vua robot (`vua_may`): tướng 10 / final boss đảo Kim

Bắt đầu 2026-11-17 (máy ổ D, kho `D:\RefAnimation\SwordxStaff`). Con gốc của rig: **`monster_3637`** (vua robot giáp vàng nhìn ¾ sang PHẢI,
vương miện răng thành, râu trắng hoa văn chữ chi, mũi tròn đỏ, áo choàng đỏ vắt vai gần, dải xanh vai xa, hai cẳng tay tròn to, bàn tay ba
ngón sẫm, NGỒI trên khối hông giữa hai CHÂN XÍCH tam giác, tay gần cầm quyền trượng dựng đứng: cán sẫm, đầu tháp vàng, ngọc lam, ĐẦU
TRƯỢNG là bánh răng + hai vòng lơ lửng trên ngọc; game tham khảo), **do người dùng chỉ** (ảnh chụp trang xem, clip `skill_01_3`). Xương,
lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là của mình. Suất 10 đảo Kim = ải 70
"Tháp Thiên Chung" (`IslandGen.cs` Plan Kim), id game hiện là **`kim_nghe`** (Kim Nghê). Mã làm việc `vua_may`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-17)

- "finalboss đảo kim; concept **vua robot như hình nhưng làm thêm nhiều chi tiết hơn nữa**, tôi đề xuất **đổi chân máy thành chân robot đi
  lại**, **thêm 4 cánh máy móc robot ở sau lưng lơ lửng**".
- "**appear** làm tướng **bay lên rồi hạ cánh**".
- "các chiêu tấn công bạn cứ làm **đủ cho tôi từ skill 1 đến skill 4**".
- "**walk** làm tướng **bay bằng cánh**".
- "con này là 1 con khó, **mổ xẻ kĩ con gốc**, riêng phần **cánh xem lại các con trước (trong game) làm cánh thế nào để tự làm**, có thể làm
  thành **cánh thiên thần lông vũ** cũng được, **cánh màu đen hoặc trắng**".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3637/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample_goc.json` 13 clip 30 khung/giây,
`khung/` tờ khung từng clip, `mo/` tờ mổ + `nhom_idle0.jpg`, `parts/`; script `vua_may.py`)

93 xương, 115 slot (112 hình bật ở idle 0), 13 clip, 7 230 khoá. Gần như mọi hình là lưới 4 đỉnh bám MỘT xương (mảnh cứng giáp robot);
lưới trọng số chỉ ở áo choàng (`pifenghou_01` sau 50 đỉnh / 10 xương, `pifengqian` trước 41 đỉnh), ngực `xiongqiong`, râu, vương miện.

Cây xương: `root → all → all2` → `xiabanshen_02` (KHỐI HÔNG, cha của cả thân) → `xiabanshen_01` (thân dưới) → `xiabanshen_03` (NGỰC) →
`xiabanshen_04` (ĐẦU: `touguan` vương miện, `yanjing`, `toufa_*` râu / ria, `t`, `t1`); ngực → `dabi_l > xiaobi_l_01 > shouwan_l > ngón`
(TAY XA = bên phải hình, nắm tay trước ngực), `dabi_r_02 > xiaobi_r_01 > shouwan__r > fazhang_01` (TAY GẦN = bên trái hình, cầm QUYỀN TRƯỢNG
`fazhang_01`, ngọc `fazhang_06`), giáp vai `jianjia_l/r`, vai `jian_l/r`, áo choàng `pifengqian > 2 > 3 > 4`, `xiabanshen_09 > 010..013`
(inherit 2), `s`, `s1` (xương phụ cho transform constraint). `all2 → jiao_l_03` (XÍCH phải hình, x +235), `jiao_r_3` (XÍCH trái hình,
x −266), mỗi xích một thanh `jiao_*_4` IK chĩa về khối hông. `all2 → fazhang_03 / 04 / 05` (HAI VÒNG + BÁNH RĂNG đầu trượng): transform
constraint `wq1..3` mix 0 ở idle (lơ lửng tự do), bật trong clip đòn để bám trượng. Ba BÁNH RĂNG PHỐI CẢNH (`fatiao3/4/5`: tỉ lệ lệch
1,27 × 0,52 = hình elip, ~19 răng `fatiao_3` 22 × 21 mỗi răng một slot, xương răng inherit 1, quay nhiều vòng) ở khuỷu tay gần, khuỷu
tay xa, eo; răng đổi lớp trước / sau khi quay (slot di động).

**Bẫy:** 13 xương inherit khác 0 (răng bánh răng inherit 1, chuỗi áo choàng inherit 2) mà runtime `.atomik` không có → biến đổi riêng của
các xương đó tính từ ma trận THẾ GIỚI mẫu khung (`l_cua` trong `vua_may_rig.py`); bản đầu không làm vậy thì áo choàng sau gập vểnh lên.

Đo chuyển động (`b` = thế giới): khối hông ở y 118 khi nghỉ, nhô lên tới 209 (skill_03), 206 (die); xích nhấc tới y 191 (hit_02), trượt x
±100 (skill_02, die).

Clip của họ (tờ `khung/`):
| clip | dài | động tác |
|---|---|---|
| `idle_01` | 1,33 | thở, đầu trượng lơ lửng nhấp nhô |
| `run_01` | 0,67 | chúi tới, trượng ngả chéo, đầu trượng áp vai |
| `skill_01_1` | 1,00 | giơ trượng qua đầu, ĐẬP ngang tới trước (đầu trượng chạm đất xa bên phải 0,44), về |
| `skill_01_2` | 1,00 | giơ trượng, vung ngang qua đầu, HẤT chéo lên trước (0,44–0,78) |
| `skill_01_3` | 1,00 | nhấc trượng, QUÉT thấp ra sau (đầu trượng chúc đất bên trái 0,44–0,78), quét tới 0,89 |
| `skill_02` | 1,37 | giơ trượng lên trời (0,30–0,61), CHĨA ngang tới trước (0,76–1,06) |
| `skill_03` | 2,27 | trượng cắm đất, hai vòng + bánh răng tách khỏi trượng BAY VÒNG quanh thân (0,5–2,0), về |
| `skill_04` | 2,17 | giơ trượng thẳng lên trời giữ 0,48–1,2 (vòng + bánh răng bay lên khỏi màn), hạ, chúng rơi về trượng 1,44–1,93 |
| `die_01` | 1,43 | đứng lên, gục, đầu trượng rơi lăn trên đất |
| `hit_01/02`, `block_01`, `stun_01` | | |

## 3. Cánh: các tướng có cánh trong game làm thế nào (người dùng dặn xem)

- Rồng trúc (`moc_vuong`, `monster_3709`): bốn gốc cánh dưới ngực, mỗi gốc một "tay cánh" 2–3 đốt mang lông dài, MỖI CHIẾC LÔNG một part trên
  chuỗi 3–4 xương riêng (lông tự uốn), lông phủ bám thẳng gốc cánh; vỗ bằng xoay tay cánh, lông trễ nhịp.
- Chim lá (`chim_la`): chuỗi `bone123 > 124 > 125 > 144` rồi các nhánh, mỗi lông một part; hai bộ mảnh cho hai mặt cánh (bật bộ kia khi cánh
  lật); vỗ một nhịp: giơ ở 0, quạt xuống nhanh 0,27–0,44 trong 0,80 s.
- Rồng vây (skill mục 00 "CÁNH"): màng một lưới 12 xương; không dùng (cánh vua robot không có màng).
→ Cánh vua robot dựng theo khuôn hai con đầu: `cw_<k>` (gốc, con của ngực, LƠ LỬNG: không dính thân) → `cw_<k>_tay` → 6 lông `cw_<k>_l<j>`
(mỗi lông một mảnh cứng trên xương riêng, j = 0 lông ngoài cùng). Bốn cánh: `tren_gan` (lên trái), `tren_xa` (lên phải), `duoi_gan` (sang
trái), `duoi_xa` (sang phải), đều SAU thân. Vỗ tự viết (`vo_canh`): hất lên chậm 60 %, đập xuống nhanh 40 %, lông xoè khi giơ, khép khi đập,
trễ từ trong ra ngoài; cánh dưới lệch pha 0,10. Cánh máy hay cánh lông vũ dùng CHUNG khung này (chỉ khác hình lông).

## 4. Bố cục (`vua_may_da.py bo_cuc` → `vua_may_1/mau/bo_cuc.png`)

Thân con gốc NÂNG lên DY = 150 đơn vị (setup y của `xiabanshen_02` và ba mảnh đầu trượng) để có chỗ cho chân; bỏ hai xích. Chân (đơn vị rig,
sau nâng): háng (±145, 260), cổ chân (±262, 74), bàn rộng ~300; chân gần (trái hình) vẽ ngay sau khối hông (chỗ xích gần của họ), chân xa
vẽ ngay trước khối hông. Bốn cánh: gốc / hướng / dài ở `CANH` của `vua_may_da.py`.

## 5. Concept lượt 1 (gói `gui_gpt/vua_may_1/`, `vua_may_da.py concept`, mô tả ở `vua_may_huong.py`)

Ảnh mẫu 1 = sơ đồ bố cục; 2 = robot cổ (tướng 7 Kim: nét, kim loại phẳng); 3 = Vong Kỵ (tướng 8 Kim: áo choàng, vương miện). Giữ dáng, chỗ, cỡ
từng mảnh thân; đổi vương miện, mặt (mắt trong khe vương miện, râu, mũi), đầu trượng; thêm chi tiết (giáp nhiều lớp, viền khắc, đinh tán,
hoa văn áo choàng) nhưng tô phẳng:
- `L1_A` **vàng hoàng kim + men trắng, 4 cánh MÁY** (khung vàng, lông thép trắng viền vàng tách rời, lõi ngọc lam); mắt lam; vương miện tia
  mặt trời; râu kim loại trắng ba lớp; mũi giáp hồng ngọc (Claude đề xuất).
- `L1_B` **vàng + bạc, 4 cánh LÔNG VŨ TRẮNG** thiên thần (ngọn vàng nhạt, vòng vàng ở gốc); mắt vàng; vương miện nguyệt quế; râu bạc chẻ đôi.
- `L1_C` **thép đen + vàng, 4 cánh LÔNG VŨ ĐEN** (ánh tím than, ngọn vàng, ngọc đỏ ở gốc); mắt đỏ; vương miện răng nhọn ngọc đỏ.

Codex đạt lượt đầu cả ba (112 / 99 / 100 s, sau khi chờ khoá Codex của phiên khác). GPT vẽ to hơn sơ đồ ~14 % và thẳng mặt hơn; IoU cả hình
với sơ đồ 0,66 / 0,66 / 0,69 (cánh khác dáng là chủ ý); co về cùng cỡ thì nửa dưới (thân + chân) 0,81 / 0,80 / 0,82 (tỉ lệ 0,86 / 0,86 /
0,90), ngang robot cổ (0,82–0,86): đủ để lắp theo khung part. Trang xem `inbox/vua_may_xem_concept.html`, tờ so `mau/_so_bo_cuc.png`
(`vua_may_da.py so_bo_cuc`). A: râu trắng xoăn + mũi hồng ngọc hơi hiền (sửa được nếu chọn). CHỜ người dùng chọn.

### Lượt 2 (2026-11-17): người dùng "cánh nhìn chưa epic, nhiều lớp hơn, hoàng gia hơn, làm thêm 1 vòng tròn hoa văn ánh sáng đằng sau"

Chưa chọn A/B/C nên sửa cả ba (`vua_may_da.py canh2` → `gui_gpt/vua_may_1/luot_2_canh_<k>.txt`, ảnh mẫu 1 = bản lượt 1 cùng chữ, khối KEEP
IDENTICAL cho cả thân): bốn cánh to hơn ~15 %, BA TẦNG lông (phủ nhỏ, giữa, lông dài), tay cánh chạm hoa văn có ngọc; thêm VÒNG HÀO QUANG hoa văn
sau mọi thứ (tâm sau gáy), tô phẳng màu sáng, không quầng (luật nét của game; trong game cho xoay chậm bằng clip `aura`, quầng sáng thật nếu
cần thì để VFX). Codex đạt lượt đầu cả ba (~100 s mỗi ảnh), thân giữ đúng: `L2_A` (cánh máy lông phủ men xanh, vòng mặt trời răng bánh răng),
`L2_B` (lông trắng ngọn vàng, vòng nguyệt quế ngọc trai), `L2_C` (lông đen phủ tím mận, vòng răng nhọn tím nhạt ngọc đỏ, chỉ lộ nửa trên).
Cánh rộng gần hết khung 1536: rig sẽ cần mỗi cánh ~3 tầng × 5–7 lông (≈ 18 mảnh / cánh) và một mảnh vòng lớn sau cùng. CHỜ người dùng chọn.

### Lượt 3 (2026-11-17): người dùng "làm ít hoa văn và giảm bớt chi tiết trên người tướng lại, đổi các miếng bánh răng trên quyền trượng
thành hình các hành tinh như mặt trời (là cục gắn với quyền trượng), sao hỏa, trái đất, sao thủy"

`vua_may_da.py l3` → `luot_3_<k>.txt`, ảnh mẫu 1 = `L2_<k>`. Ánh xạ mảnh rig: ngọc `fazhang_06` → MẶT TRỜI (gắn trượng), bánh răng
`fazhang_05` → TRÁI ĐẤT, hai vòng `fazhang_04` / `fazhang_03` → SAO HỎA / SAO THỦY (vẫn lơ lửng, bám trượng bằng ràng buộc đã nướng như
con gốc). Codex đạt lượt đầu cả ba (`L3_A/B/C`): thân thành mảng trơn lớn, ít đinh, nét gọn hơn lượt 2; GPT vẽ ba hành tinh NHỎ (Trái Đất
~1/3 bánh răng cũ) xếp dọc trên Mặt Trời. A3, C3 bỏ luôn ba bánh răng phối cảnh ở khuỷu / eo (rig: bỏ các slot `fatiao*` nếu chọn bản đó);
B3 còn bánh răng sau cẳng tay. CHỜ người dùng chọn.

## 6. Rig thử bằng DA GỐC + chân, cánh GIỮ CHỖ (`VM_GOC=1 vua_may_rig.py` → `inbox/vua_may_1/rig_goc/`, không theo git, chỉ soi)

130 xương (93 của họ + move + 6 chân + 30 cánh), 230 slot, `.atomik` 0,40 MB. Chân: `dui_<s>` (con khối hông) → `ong_<s>`, `ban_<s>` (con move);
mỗi khung IK hai đoạn (`dat_chan`): dưới đất cổ chân bám điểm trên xương xích của họ (nên bước, trượt, nhấc xích của họ thành chân bước);
trên không treo theo hông, gối co, mũi chân chúc. Đùi, ống dài hơn sơ đồ 1,22 lần cho gối gập ở dáng nghỉ (hông nhô 90 vẫn với tới đất).
- `idle` = idle_01 + cánh vỗ nhẹ 5° + gốc cánh nhấp nhô; `walk` = BAY: thân run_01, nâng 0,24 chiều cao, nhấp nhô ngược nhịp cánh, cánh vỗ
  30° mỗi 0,67 s, chân treo.
- `appear` 2,25 s: hiện dần ngồi thụp cánh khép → `vo_canh` 0,22 bung cánh → `bay_len` 0,42 đập cánh vọt lên 0,55 chiều cao → lượn → hạ nhanh,
  cánh giơ hãm → `cham_dat` 1,58 khuỵu gối, cánh đập xuống → đứng dậy.
- `die` = die_01, cánh rủ, rơi, tắt dần. Đòn: tạm attack = skill_01_1, cast = skill_02, skill = skill_04 + skill_01_2, skill_01_3, skill_03
  NGUYÊN của họ (chờ người dùng chốt cách ghép bốn skill vào ba ô chiêu).
- Đo nối: các clip không lặp về khung 0 idle lệch 0 px; idle / walk báo "khép vòng inf" chỉ vì một răng bánh răng của họ đổi lớp khi quay.

## 8. Concept chốt + mảnh + rig da mình (2026-11-17)

**Người dùng chọn B** (bản lượt 3 = `L3_B`) → `tai_ve/L1_duyet.png`. Chưa chốt cách ghép skill 1–4.

Mảnh (`vua_may_manh.py`; gói `gui_gpt/vua_may_1/luot_4_*`, Codex đạt lượt đầu cả 13 tờ, 72–131 s mỗi tờ):
- `can`: concept B3 thẳng mặt, hẹp thân hơn rig → căn bằng 8 MỐC đọc trên ảnh kẻ lưới (Mặt Trời, đầu tháp, hai nắm tay, vương miện, hông, hai
  cẳng tay; sơ đồ bố cục ↔ concept), đồng dạng không xoay: a 1,077, lệch từng mốc tới ~40 px concept → mảnh thân KHÔNG đặt theo concept.
- K1–K5 (giữ hình bóng gốc, đổi da theo màu B3 đo bằng trung vị): IoU 0,93–0,99. Ba ảnh bánh răng (`fatiao`, `fatiao_1`, `fatiao_3`) dùng chung
  cho ba bánh răng phối cảnh + 57 răng.
- G1–G8 (đúng chỗ, đúng cỡ trên concept): G1 vương miện + râu dính nhau, Mặt Trời + ba hành tinh dính chuỗi → `tach_g1` (lòng tô theo tâm gần
  nhất). Đầu (vương miện, mặt, râu) neo chung theo tâm vương miện ↔ `touguan` của họ; trượng neo đầu tháp ↔ `fazhang_02`; Mặt Trời / Trái Đất /
  Sao Hỏa / Sao Thủy neo vào tâm `fazhang_06/05/04/03` (thay đúng các mảnh đó, vẫn bám trượng / bay vòng như con gốc). Gộp: vương miện gộp vành
  sau (`touguan_1` bỏ), râu gộp hai đầu ria + má (`toufa_02/03/04` bỏ), trượng gộp đầu tháp (`fazhang_02` bỏ).
- CHÂN: ba tờ đùi / ống / gối đều ra cùng MỘT khối giáp ngắn (đúng B3: chân là khối giáp trên bàn chân) → **chân ống lồng**: khối giáp
  (`chan_<s>_goi`, xương `ong_<s>` con của bàn chân, chĩa lên hông) + pít-tông thép sẫm vẽ bằng mã (`chan_<s>_pit`, xương `dui_<s>` con của
  khối hông, chĩa xuống cổ chân, nấp sau khối giáp) + bàn chân (`ban_<s>`, con move, bám điểm trên xương xích của họ). Thân nhô lên thì
  pít-tông lộ ra, ngồi thụp thì thụt vào; không méo hình. Bàn chân nâng 25 cho ngón lọt dưới khối giáp.
- CÁNH: mỗi cánh tay cánh + ba tầng (ngoài / giữa / phủ) là ba mảnh cứng trên ba xương con của tay cánh (gốc = đầu tay cánh gần thân, trục PCA
  của mảnh tay cánh); vỗ: tầng ngoài trễ + xoè nhiều nhất. VÒNG HÀO QUANG: xương `hao_quang` con của ngực, clip `aura` 16 s một vòng.
- Chỉnh tay: vương miện nâng 38 (GPT vẽ vành sau thấp, che mắt).

Rig (`vua_may_rig.py` → `inbox/vua_may_1/rig/`, không theo git): 121 xương, 204 slot, `.atomik` 0,62 MB (VƯỢT trần 0,5 MB lúc còn 6 clip đòn
gốc tạm; cánh / vòng đã thu ×0,62). Clip: idle, walk (bay), appear (cất cánh → hạ cánh), hit, die, aura + tạm attack = skill_01_1, cast =
skill_02, skill = skill_04, skill_01_2, skill_01_3, skill_03 NGUYÊN của họ. Trang `rig/xem.html` (đã chạy thử). Còn: chốt ghép skill → làm
3 clip đòn + VFX, giảm dung lượng, Trái Đất khuyết đáy nhỏ, vào game.

### Sửa theo góp ý 2026-11-17 ("các khớp cánh và lông cánh không match nhau, lòng bàn chân xấu quá, chuyển động của cánh khi bay chưa đẹp")

- Cánh: bốn mảnh cứng (tay cánh + ba tầng) xoay lệch nhau quanh gốc → lông trượt khỏi tay cánh. Nay MỖI CÁNH MỘT LƯỚI LIỀN (`canh_lien`: ghép
  tầng ngoài, giữa, phủ, tay cánh đúng chỗ thế giới thành `manh/canh_<k>_lien.png`; `luoi_vung` bước 9 / 14 px), bám ba xương dọc tay cánh
  (`cw_<k>_tay` gốc, `_co` 45 %, `_ngon` 80 %; `ts_canh`: chiếu lên trục, hoà 0,30–0,52 và 0,62–0,86). Vỗ như cánh chim: đập xuống nhanh
  cánh duỗi, ngọn trễ; hất lên chậm cánh GẬP ở cổ cánh (nửa ngoài rủ, cả cánh ngắn ~10 %). Walk: 1,33 s một nhịp vỗ lớn 32° (trước 0,67 s);
  lượn ở appear 0,48 s một nhịp (trước 0,30).
- Bàn chân: tờ G9 vẽ lại thành ỦNG giáp robot (mũi vàng ba múi, tấm cổ chân bạc lọt dưới khối giáp, đế thép sẫm), Codex đạt lượt đầu; bỏ chúc
  mũi chân khi bay (24° → 5°). G9 khai báo SAU khối `__main__` của `vua_may_manh.py` nên `cat G9` không chạy: gọi `cat_g("G9")` qua import.

## 9. Đề xuất ba chiêu (2026-11-17, chờ người dùng duyệt)

Người dùng: "bạn thử đề xuất cho tôi 3 attack animation đánh thường, chiêu mana và chiêu cuối dựa theo những animation có sẵn"; "3 chiêu phải
thật độc đáo, epic, gây ấn tượng với người chơi, có thể làm thêm fx bất kỳ bạn muốn". Nhịp gốc đo bằng mẫu khung (góc trượng, chỗ Mặt Trời,
hành tinh): skill_01_1 lấy đà 0–0,30, đập vụt qua đầu 0,30–0,40 (khoá gần bậc), giữ tới 0,80; skill_02 giơ trời 0–0,5, chĩa tới 0,6–0,7, giữ
tới 1,1; skill_03 nhún cắm trượng 0–0,4, ba mảnh bay vòng rộng (x ±1000) 0,5–2,0; skill_04 giơ trượng thẳng trời 0,1–1,3 (mảnh xoáy trên đầu
trượng), bung lên 1,40, về 1,5.
1. Đánh thường "Nhật Ấn" (skill_01_1, ~1,25 s, đứng tại chỗ): lấy đà, Mặt Trời trên trượng bừng to; đập vụt qua đầu để lại vệt cung lửa vàng;
   đầu trượng nện đất → một đường nứt ánh sáng chạy dọc đất tới đối thủ → dưới chân đối thủ nở một ẤN MẶT TRỜI (hình vòng nguyệt quế của hào
   quang) và bắn một cột sáng lên. Lựa chọn thêm: ba biến thể luân phiên (01_1 đập / 01_2 hất chéo lên: ba tia lửa / 01_3 quét thấp: sóng lửa
   sát đất), cần thêm code trận.
2. Chiêu mana "Tam Tinh Quang Pháo" (skill_02, ~1,9 s): giơ trượng lên trời, hào quang sau lưng nở to, cánh bung; Trái Đất, Sao Hỏa, Sao Thủy
   rời trượng bay ra XẾP THẲNG HÀNG giữa vua và đối thủ (thiên thể thẳng hàng); vụt trượng chĩa tới, Mặt Trời phóng tia sáng xuyên qua lần lượt
   ba hành tinh, mỗi lần qua một hành tinh tia to và đổi màu thêm một dải → tia khổng lồ đánh trúng, nổ mặt trời; hành tinh bay về trượng.
   (Hành tinh và các đoạn tia nằm trên xương `fly*` chia theo quãng tới `far`, cơ chế `farAim` game đã có của quỷ xích.)
3. Chiêu cuối "Nhật Thực Thiên Giáng" (skill_03 + skill_04, ~3,6 s): vua vỗ bốn cánh bay lên, hào quang to gấp rưỡi quay nhanh; ba hành tinh rời
   trượng bay vòng quanh vua để lại vệt quỹ đạo (skill_03); giơ trượng lên trời (skill_04), Trái Đất bay vào che Mặt Trời: NHẬT THỰC TOÀN PHẦN
   (Mặt Trời hoá đĩa đen viền vành nhật hoa trắng, màn tối lại); ba hành tinh vọt lên khỏi màn rồi lần lượt RƠI xuống đối thủ thành thiên thạch
   cháy: Sao Thủy, Sao Hỏa, rồi một Trái Đất khổng lồ (mỗi cú một lần rung, cú cuối rung mạnh nhất + bùng sáng); Mặt Trời sáng lại, hành tinh về
   trượng, vua đáp xuống.
Hiệu ứng: tờ hình hiệu ứng vẽ theo nét game (Codex, lưới 3 × 2: vệt cung lửa, ấn mặt trời, cột sáng, đoạn tia, vành nhật thực, đuôi lửa thiên
thạch, vết nổ), phần nằm trong rig (Mặt Trời to lên, hành tinh, thiên thạch, ấn, tia) + lớp hạt Unity riêng (tia lửa, than, bụi, khói, rung,
khựng, chớp màn) như HatXich / HatHo.

### Đã dựng ba chiêu (2026-11-17, người dùng "làm đi"; đánh thường làm MỘT đòn, chưa luân phiên)

- Tờ hình hiệu ứng `tai_ve/FX_1.png` (`vua_may_fx.py`, Codex đạt lượt đầu): cung, an, cot, tia, nhat_thuc, duoi → `manh/fx_*.png`.
- Xương / slot hiệu ứng trong rig (`fx_*`, khai `plain`, ẩn mặc định, vẽ trên cùng): `mieng` (tâm Mặt Trời, con fazhang_06); `far` (con root,
  dáng gốc (1,6 · 1130, 0,4 · 1130)); đánh thường: `fly_n0..5` + `nut*` (cột sáng nhỏ nối nhau trên đất), `ff_an` / `ff_cot` (con far, hạ xuống
  đất); `fx_cung` (vệt cung lửa lật ngang phủ hộp đường bay Mặt Trời trong cú vụt, xương `fx_cung_b`); chiêu mana: `fly_t0..13` + `tia*` (đoạn tia,
  dài 1,45 × quãng / 14, dày 150 / 220 / 300 / 400 theo số hành tinh đã qua), `fly_p0..2` + `p*` (bản sao Thủy / Hỏa / Trái Đất ở 0,30 / 0,48 /
  0,66 quãng), `ff_no`; chiêu cuối: `fx_nhat_thuc` trên `mieng`, `ff_m0..2` (đuôi lửa + hành tinh to, rơi từ (−0,62; 2,1) · 1130 trong hệ far),
  `ff_no0..2`. Mảnh giữa đường theo cơ chế `fly*` của quỷ xích (`fly` = w · far, con = (1 − w) · A), chiêu mana khai `farAim`.
- attack 1,30 s (skill_01_1): `tu` 0,10, `dap` 0,52, `an` 0,76, `trung` 0,80. cast 1,95 s (skill_02): `tu` 0,30, `thang_hang` 0,95, `ban` 1,12,
  `trung` 1,22. skill 3,70 s (skill_03 0 → 1,6 rồi skill_04 0,15 → 1,38, giữ trượng giơ tới 3,10, hoà 0,18 s về 1,50 → hết): `bay` 0,30,
  `quy_dao` 0,50, `nhat_thuc` 2,00, `phong` 2,45, `no` 2,82 / 2,96 / 3,20, `sang` 2,98, `trung` 3,20.
- Bẫy: điểm neo ảnh trong `fx_slot` là toạ độ ẢNH (y xuống) → mép trên = cao · neo_y (bản đầu cột sáng lộn xuống đất); `Wi` phải cập nhật khi
  thêm xương mới; heredoc dài bị Bash cắt → vá bằng file. `.atomik` 0,72 MB (vượt trần 0,5): còn phải giảm (ảnh hiệu ứng nhỏ lại, lược khoá).
- Còn: lớp hạt Unity (tia lửa, than, bụi, rung, khựng, màn tối lúc nhật thực), vào game, dạng non.

### Góp ý 2026-11-17 (khuya): quỹ đạo hành tinh, chiêu mana cột trên đầu đối thủ, VFX Unity

- "cho các hành tinh quay quanh mặt trời" (idle và các clip khác): `quanh_mat_troi` đặt ba xương hành tinh (con all2) lên elip nghiêng −14°
  quanh tâm Mặt Trời (`sun_c` trong hệ fazhang_06) SAU khi clip đặt dáng: Sao Thủy rx 185 / 3 vòng, Trái Đất 290 / 2 vòng, Sao Hỏa 390 / 1 vòng
  mỗi 2,67 s; nửa dưới elip to hơn (×1,12), nửa trên bật slot `sau_<xương>` chèn ngay trước slot Mặt Trời (đi sau Mặt Trời). idle nay 2,67 s
  (idle_01 hai vòng) để ba quỹ đạo khép kín. Áp cho idle, walk, hit, appear, attack, hai đầu chiêu cuối; die giữ rơi lăn của họ.
- "cho các tiểu hành tinh đứng thẳng hàng trên đầu của đối thủ rồi mặt trời lên trên cùng sau đó bắn tia sáng xuống": cast 2,10 s làm lại: bản sao
  cất từ đúng chỗ hành tinh thật trên quỹ đạo (`pl_c`), bay vòng cung tới cột trên đầu đối thủ (hệ far: Thủy +0,50, Hỏa +0,73, Trái Đất +1,02 ×
  1130), bản sao Mặt Trời (`fly_s` / `s_bay`, ×1,55) rời trượng 0,55 lên đỉnh +1,42 lúc 0,95; vụt trượng 1,00–1,10; tia THẲNG XUỐNG (`fly_t*`
  đặt ở far, con lệch dọc, xoay −90°) mọc trong 0,12 s, dày dần sau mỗi hành tinh, xuyên qua tâm đối thủ thêm 0,2; nổ `trung` 1,24; về trượng
  1,62–1,95. Sự kiện mới `len_dinh`.
- "các fx tia sáng và vụ nổ cần cải thiện thêm trong unity bằng skill tạo vfx": hỏi đưa vào game (suất kim_nghe) → người dùng chọn **"Chưa vào
  game"**: VFX Unity (lớp hạt chồng lớp phẳng theo skill pokiclash-vfx / pokiclash-hero-fx, file Hat*.cs + bảng trong StageView) để sau.

## 7. Việc tiếp

1. Người dùng chọn concept (A / B / C) → `tai_ve/L1_duyet.png`; chốt cách ghép skill 1–4 vào attack / cast / skill; xác nhận thay suất
   `kim_nghe` (không đè file cũ), tên, số dạng.
2. Mảnh: K = giữ hình bóng theo khung part (áo choàng, giáp vai, cẳng tay, bàn tay, ngón, ngực, bụng, khối hông, bánh răng + răng); R = đổi
   dáng đúng chỗ trên concept (vương miện, râu, mũi, đầu trượng, cán trượng dài tới đất); chân + cánh = mảnh mới gen "đúng chỗ, đúng cỡ" từ
   concept (lông cánh mỗi chiếc vẽ đủ phần khuất trên tờ rời), đo lại khớp chân, gốc cánh trên concept rồi sửa `CHAN`, `CANH`.
3. Rig da mình, clip đòn theo cách ghép đã chốt, VFX (đầu trượng / vòng / bánh răng), soi, người dùng xem, vào game, dạng non.
