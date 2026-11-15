# Pháp sư lửa (`phap_lua`): tướng thứ 6 đảo Hỏa

Bắt đầu 2026-11-13 (máy ổ C). Con gốc của rig: `monster_3481` (pháp sư bóng ma cầm trượng có con mắt, hai bàn tay vuốt rời; game tham khảo,
kho `D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như
aola): dùng nội bộ, không đăng công khai. Tên, id game: chưa đặt (`phap_lua` chỉ là mã làm việc).

## 1. Lời dặn của người dùng (2026-11-13)

- "tướng thứ 6 đảo hỏa; concept **pháp sư lửa giống như ref**, **con mắt trong quyền trượng đổi thành cầu lửa cháy liên tục** (làm anima lửa
  cháy, **thêm fx khói bốc đằng sau lớp cầu lửa**)".
- appear: "làm nó **bay vào**".
- "**idle và walk** làm giống con gốc nhưng **sửa khác đi chút**".
- Đánh thường: "dùng **tay không cầm trượng cào** vào đối thủ".
- Chiêu cast mana: "giống `skill_02`, **giơ trượng lên triệu hồi các mũi kim lửa rồi bắn** vào người đối thủ".
- Chiêu cuối: "giống `skill_03`, **dang 2 tay làm quyền trượng bay lơ lửng, tách cầu lửa của quyền trượng ra bay lên cao, hút lửa xung quanh
  tạo thành 1 quả cầu lửa to rồi bắn** vào đối thủ".
- die: "làm giống con gốc".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3481/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample.json` 30 khung/giây, `mo/`, `parts/`, `khung/`, `can/`)

107 xương, 53 slot, 11 clip; 29 vùng ảnh, 52 hình. **FK thuần** (không IK, path, transform constraint). Con **nhìn sang PHẢI** (clip trúng đòn
ngả về trái, chạy thì áo bay về trái): trượng ở bên TRÁI hình, tay vuốt giơ bên PHẢI (phía đối thủ). Không chân, không cánh tay: thân là áo
choàng lơ lửng, hai bàn tay rời có cổ tay khói.

| thứ tự | slot | ảnh (px) | là gì | xương |
|---|---|---|---|---|
| 1 | `pifeng_03` | 304 × 232 | ÁO thân (lưới 95 đỉnh, 16 xương: ba chuỗi đuôi áo bone31–41, 49) | |
| 2 | `shenti` | 82 × 117 | dây bện zíc zắc giữa ngực | bone4 |
| 3 | `pifeng_02` | 201 × 174 | khăn vai TRÁI to (49 đỉnh; chuỗi bone26–30, 42, 50–52), vạt vuông bên trái | |
| 4 | `pifeng_01` | 101 × 71 | khăn vai PHẢI nhỏ (20 đỉnh; bone31, 53–55, 7) | |
| 5 | `maofa_01` | 261 × 164 | BỜM TÓC (83 đỉnh, 15 xương bone57–71: bốn chuỗi) | |
| 6–7 | `zhuangshi_02/01` | 28 × 51 | hai gai sao bốn cánh ở ngực | bone3 |
| 8–9 | `tou_05`, `tou_04` | | hai tấm mặt nạ (mỏ nhọn chĩa xuống) | bone6 |
| 10 | `tou_03` | 19 × 38 | viên ngọc trán | bone6 |
| 11–12 | `tou_02`, `tou_01` | 44 × 140, 87 × 134 | hai nhánh sừng cao + móc sừng cong | bone6 |
| 13 | `shouzhangR_01` | 87 × 66 | cổ tay khói của TAY TRƯỢNG (36 đỉnh; bone45–48) | |
| 14 | `wuqi` | 215 × 334 | TRƯỢNG liền con mắt (14 đỉnh) | bone56 |
| 15 | `wuqi2` | | bản trượng thả rời (ẩn) | bone102 (con của `bone`) |
| 16–19 | `shouzhiR_04..01` | | bốn ngón tay trượng (trước cán) | bone45 |
| 20–50 | `shouzhiL_10..01`, `shouzhangL_01` | | TAY VUỐT: cổ tay khói (32 đỉnh; bone10, 21–24) + mười đốt vuốt, mỗi đốt một xương (bone11–20) | |
| xen kẽ | `shouzhiL_010..018`, `_11`, `shouzhangL_02` | | bộ tay vuốt thứ 2 (ẩn) trên chuỗi bone103 → 104 → bone72… ở x ≈ 694: **bàn tay hiện ra chỗ đối thủ** | |
| xen kẽ | `shouzhiL_019..027`, `_12`, `shouzhangL_03` | | bộ tay vuốt thứ 3 (ẩn) trên bone87 (con của bone43, lật `sy = −1`): **tay trượng mở ra thành vuốt** | |

Bẫy: atlas có vùng `rotate: 90/180/270` (`to_manh.nap` đã quay về chiều gốc).

Clip của họ:

| clip | dài | động tác | dùng cho |
|---|---|---|---|
| `idle_01` | 4,00 s | lơ lửng, áo tóc bay, tay vuốt co duỗi | **idle** (sửa khác chút) |
| `run_01` | 0,80 s | chúi tới, trượng vác chéo, áo bay sau | **walk** (sửa khác chút) |
| `skill_01` | 1,40 s | giơ tay vuốt lên (0,13–0,25), tay tan (0,33), hiện lại 1,10; không đổi thứ tự vẽ | **attack** |
| `skill_01_1` | 1,40 s | CHỈ bàn tay thứ 2 ở chỗ đối thủ: hiện 0,47, cào hai nhát (0,5–1,0), tan 1,15–1,23 | bàn tay cào chỗ đối thủ |
| `skill_02` | 1,50 s | giơ trượng thẳng lên 0,14–0,68, vụt trượng xuống trái 0,82–1,09, về; đổi thứ tự vẽ từ khung 24 | **cast** |
| `skill_03` | 1,87 s | giơ trượng 0,17 (trượng chuyển sang `wuqi2` thả rời, tay trượng mở thành bộ vuốt thứ 3), dang hai tay 0,68–1,36, trượng lơ lửng trước ngực, chụp lại 1,53–1,63 | **skill** |
| `hit_01/02`, `block_01`, `stun_01` | 0,5 / 0,67 / 0,5 / 1,33 s | | **hit** |
| `die_01` | 1,33 s | bật ngửa lên, trượng văng (`wuqi2`), rơi úp xuống nằm bẹp | **die** |

## 3. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `phap_lua.py` (`mo`, `nhom`, `part_goc`), `phap_lua_bo_cuc.py` (sơ đồ bố cục 1536 × 1024 ở khung 0 idle, 1,179 px / đơn vị rig: hình
bóng từng part tô phẳng theo màu của mình; con mắt trong đầu trượng thay bằng cầu lửa vẽ bằng mã: quả cầu ba vùng + ba lưỡi lửa bốc lên sau
khung trượng), `build_phap_lua.py` (gói `gui_gpt/phap_lua_1/`; ảnh mẫu: sơ đồ, Voọc Tướng, quỷ lửa bắn cung bản A, bản đồ).

Giữ của con gốc (theo lời "giống như ref"): mọi hình bóng, chỗ, cỡ, thứ tự chồng. Đổi: **con mắt → cầu lửa đang cháy**; màu và chất liệu của
mình; hoa văn áo của mình (một vùng trong sáng hơn, ranh uốn lưỡi lửa). Tránh tông đã dùng ở đảo Hỏa: nâu đỏ gạch (`quy_lava`), vỏ chai đen
tím (`mat_lua`), giáp cháy nâu đen (`cung_lua`), đá tro xám (`golem_lua`).

Ba hướng màu:
- `ao_do` **A · áo đỏ**: áo đỏ thẫm #A32E22 vùng trong cam #E8782A; tóc và cổ tay tro trắng kem #E9E1D2; mặt nạ, sừng, sao, trượng, vuốt đen
  than #2F2A30; khăn vai than #3C353B viền vàng nhạt; dây ngực vàng nhạt; ngọc vàng. Sát con gốc nhất (tóc sáng, giáp sẫm, áo màu).
- `toc_lua` **B · tóc lửa**: tóc là bờm lửa ba màu, hai cổ tay là đốm lửa; áo xám than #5B5357 vùng trong than hồng #BE542C; khăn vai đỏ thẫm
  #8A2A22; giáp sắt đen; dây ngực trắng ngà.
- `khoi` **C · khói + đồng**: tóc khói xám than #605A66, cổ tay khói xám nhạt; áo cam hổ phách #E08A2E vùng trong vàng; khăn vai nâu đỏ
  #6E2630; mặt nạ, sừng, sao, trượng đồng thau #B57438; vuốt than; ngọc đỏ cam.

Lượt 1 (2026-11-13, 82–102 s mỗi ảnh, cả ba dùng được ngay): `phap_lua_1/tai_ve/L1_ao_do.png`, `L1_toc_lua.png`, `L1_khoi.png`; trang so
`inbox/phap_lua_xem_concept.html`. Soi: đúng bố cục sơ đồ, không lật, cầu lửa trong đầu trượng có lưỡi lửa sau khung, mặt nạ hai khe mắt.

**Người dùng xem lượt 1: "nhìn concept đầu, áo choàng bị giống con gốc quá".** (Bài học: "giống như ref" không có nghĩa giữ hình bóng mảnh to
nhất; memory `doi-dang-manh-nhan-dien`.) → Lượt 2 (`build_phap_lua.py ao` → `gui_gpt/phap_lua_1/luot_2_ao_<kiểu>.txt`): giữ nguyên bản A, chỉ
vẽ lại áo thân + hai khăn vai, ba dáng là đề xuất của Claude:
- `ao_lua` **D · áo cháy thành lửa**: nửa trên áo vải đỏ thẫm mép cháy sém, nửa dưới thân là khối lưỡi lửa; khăn vai thành áo vai ngắn, bên
  trái một đuôi nhọn dài. → `L2_ao_lua.png` (đạt lượt đầu, mọi thứ khác trùng bản A).
- `ao_chuong` **E · áo chuông thầy pháp**: áo dài loe hình chuông, gấu lượn sóng tròn có dải lửa; khăn quàng dài đuôi én. → `L2_ao_chuong.png`.
- `ao_tang` **F · áo tầng lông phượng**: ba tầng vạt lông vũ đỏ thẫm → đỏ → cam ngọn vàng; khăn vai cắt vạt lông. → `L2_ao_tang.png`.

Áo đổi hình bóng thì KHÔNG dùng nguyên lưới `pifeng_03 / 02 / 01` của họ được: gen riêng áo + khăn vai "đúng chỗ, đúng cỡ" từ concept đã
duyệt, lưới dày của mình, mỗi đỉnh biến dạng như điểm tương ứng trên lưới thưa của họ (`gan_goc`, mẫu `rong_vay_rig.py`).

**Người dùng xem lượt 2: "các dạng D E F mặt vẫn bị giống con gốc, bạn đổi dạng mặt nó đi, animation tôi thấy khá ổn rồi".** (Chưa nói chọn
dáng áo nào.) → Lượt 3 (`build_phap_lua.py mat [nền]` → `luot_3_mat_<kiểu>.txt`, nền mặc định bản D): chỉ vẽ lại cái đầu, bỏ mặt nạ mỏ nhọn
+ hai nhánh sừng cao + hai móc sừng. Đầu là mảnh cứng trên xương `bone6` nên ghép được với dáng áo nào cũng được. Ba kiểu (đề xuất của Claude),
cả ba đạt lượt đầu, mọi thứ khác trùng bản D:
- `mu_trum` **G · mũ trùm mắt lửa**: mũ trùm than viền vàng chóp nhọn ngả sau, trong mũ tối đen, hai mắt lửa xếch, ngọc vàng. → `L3_mu_trum.png`.
- `sung_cuu` **H · mặt nạ quỷ sừng cừu**: mặt nạ than hình khiên, mày cau, hai sừng cừu cuộn xoắn tro kem. → `L3_sung_cuu.png`.
- `trang_khuyet` **I · mặt nạ sứ + mào trăng khuyết**: mặt nạ trái xoan tro kem, hốc mắt lửa, mào trăng khuyết than viền vàng. → `L3_trang_khuyet.png`.
Đã mở trang so cho người dùng; CHỜ chọn mặt (G / H / I), dáng áo (D / E / F) và màu. Tóc, trượng, hai bàn tay, dây ngực vẫn giữ dáng con gốc
(đã hỏi người dùng có đổi luôn không).

**Tờ E (mảnh cầu lửa, tim lửa, bốn lưỡi lửa, ba cuộn khói)** không phụ thuộc áo / mặt nên đã gen trước: `phap_lua_da.py prompt_E` →
`luot_4_da_E.txt` → `tai_ve/D_E.png` (đạt lượt đầu) → `phap_lua_da.py cat E` → `manh/cau.png`, `tim.png`, `lua_0..3.png`, `khoi_0..2.png`; đã
chép vào `manh_goc/` nên rig thử dùng lửa, khói thật (`.atomik` thử 395 KB).

## 4. Kế hoạch rig và clip (sau khi concept được duyệt)

- **Reskin đúng nghĩa** như `cung_lua` (skill mục 23): tờ mảnh GỐC cắt theo lưới phóng 2,5–5 lần → GPT đổi da giữ hình bóng và đường cấu trúc
  (`phap_lua_da.py`); rig dùng đủ xương, nguyên lưới, trọng số, thứ tự vẽ của họ (`phap_lua_rig.py`); slot đổi thứ tự vẽ trong `skill_02`,
  `skill_03`, `die_01` thì nhân đôi slot.
- **Trượng tách ba lớp** (con gốc là một ảnh): khói (sau cùng) → cầu lửa (lưới + chuỗi xương, lửa uốn lượn liên tục như `golem_lua.lua_lay`) →
  khung trượng (trước). Khung trượng gen riêng "bỏ quả cầu", cầu lửa gen riêng.
- **Khói sau cầu lửa**: vài cuộn khói đen than ngả xám (memory `fx-smoke-style`) trên xương riêng, bốc lên, to dần, tan dần, lặp lệch pha
  (clip `aura` để liền qua mọi clip).
- appear: bay từ ngoài vào (áo tóc kéo ngược), hãm lại, vào thế.
- idle / walk: của họ + sửa khác chút (đề xuất: cầu lửa phập phồng, thỉnh thoảng bùng; nhịp nhấp nhô và tay vuốt khác đi).
- attack: `skill_01` + bộ tay thứ 2 trên xương `far` (game dời tới đối thủ) phát `skill_01_1`: bàn tay tan ở chỗ mình, hiện ra cào đối thủ.
- cast: `skill_02`; sự kiện `goi_kim` (kim lửa hiện quanh đầu trượng lúc giơ), `ban_kim` (lúc vụt trượng), `trung`. Kim lửa: VFX.
- skill: `skill_03`; cầu lửa rời đầu trượng bay lên cao (xương `cau`, slot bản sao), lớn dần lúc hút lửa (sự kiện `hut`), bắn tới đối thủ
  (`fly_*` → `far`, sự kiện `ban_cau`, `trung`), cầu lửa mới nhen lại trong đầu trượng lúc chụp trượng.
- die: `die_01` + cầu lửa tắt dần (bản cầu tắt đổi màu bằng mã), khói lịm.
- VFX ngoài rig: kim lửa, lửa bị hút về, vệt cầu lửa, nổ trúng, vệt cào.

## 5. Rig dựng thử trên DA GỐC (2026-11-13, trong lúc chờ duyệt concept; không phụ thuộc màu)

`phap_lua_da.py tam` → `phap_lua_1/manh_goc/` (ảnh part gốc × 2, trượng đã xoá quả cầu mắt, mảnh cầu lửa / lưỡi lửa / khói vẽ tạm bằng mã).
`PL_MANH=.../manh_goc PL_RA=.../rig_goc py -3 -I phap_lua_rig.py` → `phap_lua_1/rig_goc/` (`xem.html`, tờ khung, `.atomik` 323 KB).

- 135 xương (107 của họ + root, move, far, fly_cau, cau_goc, cau, tim, mieng, 4 × 4 xương lửa, 5 xương khói), 79 slot, 2498 đỉnh; chiều cao
  game 643; cầu lửa tâm (−273, 501) bán kính 82.
- Thứ tự vẽ: của họ; `wuqi` + bốn ngón tay trượng có bản `_t` trên cùng (skill_02 từ 0,80 s); `wuqi2` (trượng thả rời) chỉ có ở trên cùng;
  nhóm cầu lửa (khói → lửa 1, 2, 0, 3 → cầu → tim) có hai bản: ngay sau `wuqi` và bản `_t` sau `wuqi_t`.
- Nhóm cầu lửa trên `cau_goc` (con của `fly_cau`, con của root): mỗi khung đặt vào tâm đầu trượng (`cho_cau`: bone56 hoặc bone102) nhưng
  không xoay theo trượng; `LuaNga` (hậu kỳ trên khung đã nướng) cho lưỡi lửa ngả ngược chiều bay, làm mượt; lò xo `LoXo` trên ba đốt mỗi lưỡi.
- `aura` 4 s (lặp, phủ lên mọi clip): lửa uốn (sóng gốc → ngọn chu kỳ 1 s + hoạ âm), tim lửa đập, 5 cuộn khói đời 2 s lệch pha (bốc lên
  3,6 bán kính, to dần rồi co, đổi hình than → xám → xám nhạt, nhạt dần 30% cuối).
- Bàn tay thứ 2: `bone103` là con của `far` (toạ độ của `skill_01_1` tính từ tâm đối thủ).
- Clip: `idle` 4 s (của họ + nhấp nhô chậm, 2,15–3,55 s nâng trượng ngắm cầu lửa: lửa bùng, 0,55–1,8 s vuốt gõ nhịp), `walk` 0,8 s (của họ +
  nhún, lửa ngả sau), `hit` 0,5 s, `attack` 1,2 s (skill_01 × 0,857: tay tan 0,28, hiện chỗ đối thủ 0,40, trúng 0,48), `cast` 1,75 s (giơ
  trượng 0,16 `goi_kim`, giữ run, vụt 1,05 `ban_kim`, trúng 1,19), `skill` 3,4 s (tung trượng 0,17, cầu rời trượng 0,66, lên cao 1,05, hút
  lửa lớn 2,2 lần tới 2,05, lấy đà, bắn 2,25, trúng 2,45, chụp trượng 2,75, cầu mới nhen 2,87), `appear` 1,3 s (bay từ trên trái vào, tới
  0,62, quá đà rồi về thế), `die` 1,78 s (die_01 + lửa lụi 0,25–0,85, cầu thành than 0,8, mờ dần).
- Mọi clip nối về idle lệch 0 px; góc nhảy lớn nhất là của chính clip họ (tay thứ 2 đổi chỗ, cú vụt trượng 116°/khung).

## 6. Concept chốt và bản rig thật (2026-11-13 chiều)

**Người dùng chốt "G"** (mũ trùm mắt lửa, vẽ trên nền D áo cháy thành lửa, màu bản A) → `tai_ve/L1_duyet.png` = `L3_mu_trum.png`. Animation: "khá ổn rồi".

Khớp concept ↔ rig: concept = 1,0475 × sơ đồ + (−48, −20) px (`mau/khop_concept.json`, IoU 0,88; `phap_lua_da.tg_concept`).

Mảnh (`phap_lua_da.py`):
- **Giữ hình bóng part gốc** (tờ mảnh gốc → GPT đổi da, `to` + `prompt_goc` → `luot_5_da_<B|C|D>.txt`, `cat B C D`): B = bờm tóc, hai cổ tay khói, dây
  bện, hai gai sao (đã về, IoU 0,87–0,96); C = 14 đốt ngón / vuốt; D = khung trượng (lòng khung để trắng).
- **Đổi dáng, gen đúng chỗ đúng cỡ từ concept** (`prompt_concept` → `luot_6_manh_<tên>.txt`, `cat_concept` → `manh/dat_moi.json`): `dau_lua` (đầu mũ
  trùm + khối lửa dưới áo), `ao` (áo vải đỏ), `vai` (áo vai than viền vàng, tách hai nửa chờm 36 px quanh x = 865), `toc` (tóc theo concept).
- **Codex hết hạn mức 16:05, mở lại 18:30**: C, D, `toc` chưa gen. Tạm thời: ngón, vuốt, trượng tô bằng mã trên đúng hình bóng part gốc
  (`tam_than`: than (72, 62, 66) vân sáp chéo, viền mực rung; tên ghi ở `manh/_tam.json`, `cat C D` sẽ ghi đè); tóc dùng bản tờ B (hình bóng part gốc,
  nhỏ hơn tóc trên concept ở phía phải sau mũ). Tiến trình nền hẹn 18:32 chạy `chay_hoa.py` ba file đó.

Rig (`phap_lua_rig.py`, đọc `manh/dat_moi.json`):
- Đầu: năm mảnh `tou_*` của họ (cùng `bone6`) → MỘT mảnh cứng `dau`.
- Áo vải (`pifeng_03`) + khối lửa (`lua_ao`, ngay sau áo): `gan_xuong` = lưới của mình, trọng số trơn theo khoảng cách tới 14 đốt xương đuôi áo
  của họ (σ 62 / 54). ĐÃ THỬ và BỎ `gan_goc` (nội suy theo tam giác lưới áo của họ): chỗ đuôi áo nhọn bên phải của họ lưới gập → áo, lửa của mình
  bị xé, lòi vệt đỏ ở mép phải.
- Áo vai trái / phải: `gan_goc` trên lưới `pifeng_02` / `pifeng_01` (đỉnh ngoài lưới bám điểm gần nhất + nguyên độ lệch).
- Tóc: `gan_goc` trên lưới `maofa_01` khi có `toc`; chưa có thì nguyên lưới của họ với da tờ B.
- `aura`: thêm sóng trên bone34, 35, 39, 40 (đốt cuối hai chuỗi đuôi áo giữa) cho khối lửa dưới áo uốn liên tục.
- Chiều cao game 577 (đỉnh mũ trùm − 12). Cầu lửa chiêu cuối: tâm (64, 1000), to 2,2 lần (khung sticker của game cao 2,72 chiều cao trên chân).
- `ep_goc`: 0,23 s cuối `cast` dùng sẵn bản slot gốc (đoạn `khop_idle` hoà độ đậm làm bản `_t` và bản gốc cùng mờ nửa chừng → cầu lửa trong suốt).
- Dung lượng: 577 KB (vượt trần) → hạ mật độ lưới và px atlas (cầu lửa 1,35; mảnh concept 1,0) → **448 KB**.
- Kết quả: 135 xương, 76 slot, 2584 đỉnh; mọi clip nối về idle lệch 0 px; khung 0 idle so concept IoU hình bóng 0,91 (`rig/so_concept.png`).
  Soi runtime thật: `rig/that/*.jpg`, cận `rig/that_can/`. Xem: `rig/xem.html`.

Việc tiếp: 18:32 gen C, D, `toc` → `cat C D`, `cat_concept` → dựng lại; người dùng xem, dặn sửa; vào game (suất 6 đảo Hỏa = ải 30, id hiện là
`hong_lien`, chiêu mana "kim" đã có sẵn `HatLua.Needles`) khi người dùng bảo.

### 6b. Chiêu cuối: đường bay của cầu lửa để code làm (người dùng 2026-11-13)

"bạn chỉ cần làm cầu lửa bay lên phình to, còn bay đi đâu do code làm". → `skill`: cầu lửa rời trượng, bay lên (64, 1000), phình 2,2 lần, lấy đà
(lùi (−70, +34), to thêm 10%); đúng mốc `ban_cau` (2,25 s) cầu của rig BIẾN MẤT tại chỗ, không còn nướng đường bay (`fly_cau` không khoá, `far` chỉ
còn `attack`). Code hiệu ứng lúc vào game: nghe `ban_cau`, sinh cầu lửa ở xương `mieng` (tâm cầu, con của `cau_goc`; bán kính lúc đó ≈ 82 × 2,4 đơn
vị rig) và lái tới đối thủ, nổ; `hut` (1,05 s) là lúc hút lửa về cầu; `trung` (2,45 s) là giờ trúng danh nghĩa cho game; `nhen` (2,87 s) cầu mới nhen
lại trong đầu trượng (rig tự làm).

## 7. Kiểm ở máy ổ D (2026-11-14, người dùng: "tướng thứ 6 đảo hỏa làm rồi mà, pháp sư lửa, kiểm tra kĩ lại")

- Nhánh `main` ở máy D trùng remote (`b227b581`, commit 18:23 ngày 13). Trong bản đó pháp sư lửa **đã làm xong phần hình + rig** (concept G chốt,
  mảnh, `phap_lua_rig.py`, animation người dùng nhận "khá ổn") nhưng **chưa vào game**: `heroes.json` suất 6 vẫn là `hong_lien` (Đốm Hồng → Phi
  Viêm → Hồng Liên), `Resources/hong_lien_1..3` là `.atomik` cũ ngày 11-11, không có `quai/doi_phap_lua.py`, không có VFX cầu lửa (`ban_cau`).
  Nếu máy kia đã làm tiếp sau 18:23 thì phần đó chưa được commit / push.
- Ba tờ hẹn gen 18:32 (`luot_5_da_C`, `luot_5_da_D`, `luot_6_manh_toc`) không có trong `tai_ve/`: ngón, vuốt, trượng vẫn là bản tô tạm bằng mã
  (`manh/_tam.json`), tóc là bản tờ B.
- Quét lại con gốc về máy D (`D:\RefAnimation\SwordxStaff\scan\monster_3481`: `info`, `att_goc`, `att_idle0`, `sample` 11 clip 30 khung/giây, qua
  `quai/khoa.py chrome`, chạy êm) rồi `SXS=D:/RefAnimation/SwordxStaff py -3 -I phap_lua_rig.py`: dựng lại được, trùng số mục 6 (135 xương, 76
  slot, 2584 đỉnh, 449 KB, mọi clip về idle 0 px) → `phap_lua_1/rig/` (thư mục `rig/` không theo git).
- Việc còn lại để vào game: gen C, D, `toc` (prompt đang ghi đường dẫn máy C, phải dựng lại bằng `phap_lua_da.py`) → `cat` → dựng lại rig; script
  đổi dữ liệu suất 6 (giữ id `hong_lien` hay đổi id, tên tướng, tên thẻ, số dạng: chờ người dùng); VFX cầu lửa chiêu cuối theo mục 6b.

## 8. Bản rig thật đủ mảnh và vào game (2026-11-14, máy ổ D; người dùng: "làm đi, suất 6 cho vào game rồi làm thêm dạng 1")

- **Ba tờ còn thiếu** gen ở máy D (đổi đường dẫn trong `luot_5_da_C.txt`, `luot_5_da_D.txt`, `luot_6_manh_toc.txt` sang `D:\PokiClash`): `D_C.png`
  (14 đốt ngón / vuốt, IoU 0,90–0,96), `D_D.png` (khung trượng, IoU 0,93), `M_toc.png` → `phap_lua_da.py cat C`, `cat D`, `cat_concept`
  (`manh/_tam.json` nay rỗng). Dựng lại: 135 xương, 76 slot, **2883 đỉnh** (tóc lưới của mình 382 đỉnh bám `maofa_01`), `.atomik` **472 KB**, mọi
  clip về idle 0 px. Đã soi `rig/khung_idle.png`, `khung_skill.png`.
- **Dữ liệu** (`quai/doi_phap_lua.py`, chạy lại không đổi thêm): giữ id `hong_lien`, id thẻ, chỉ số, hiệu ứng thẻ; tên **Viêm Sư**, danh hiệu "Pháp
  sư gọi cầu lửa", dòng "Dòng Viêm Sư"; forms 3 → 2, tạm cả hai trỏ `phap_lua_1` (0,92 / 1,1) cho tới khi có dạng 1 (`dang_1` đổi dạng 1 sang
  `phap_lua_non` "Viêm Đồng"); thẻ: Cánh Sen Lửa → **Hỏa Châm** (flame), Hồng Liên Nghiệp Hỏa → **Đại Hỏa Cầu** (sun), Lông Vũ Lửa → **Thân Khói**
  (ghost), thẻ boss Niết Bàn Hỏa → **Nhen Lại Lửa Tàn** (torch). Tên do Claude đặt. `chep` → `Resources/phap_lua_1/` (thư mục mới;
  `hong_lien_1..3` cũ giữ nguyên). Số dạng đổi nên golden roster phải tính lại trong Unity.
- **VFX** `Assets/01 Script/Game/Battle/HatPhap.cs` (partial `HatLua`, đi đường "n_"): `StageView.FireFx["hong_lien"] = ("n_kim_phap", "n_cau_phap")`,
  `HatLua.Themes["hong_lien"]` = bảng "lua" (trước: "sen", cánh sen), hai `case` mới trong `HatNuoc.PlayNuoc`, `HatLua.KimLua` (tách từ `Needles`,
  `Needles` giữ nguyên hành vi), `HoaFxTour` menu "Đảo Hỏa: riêng Viêm Sư …".
  - `n_kim_phap`: 7 kim lửa hiện dần thành vòng cung quanh đầu trượng đang giơ (`goi_kim` 0,16 s), `ban_kim` (1,05 s) thì phóng cách nhau 0,035 s,
    mũi đầu chạm đúng khung trúng (1,19 s).
  - `n_cau_phap`: từ `hut` (1,05 s) lưỡi lửa + than hồng bị hút vào quả cầu của rig đang phình; đầy (2,05 s) nháy vòng; `ban_cau` (2,25 s) cầu hạt
    cùng chỗ cùng cỡ lao tới đối thủ, chạm đúng `trung` (2,45 s), `CauNo` 1,6 + hai vụ nổ phụ.
  - Số đo trên rig (phần của chiều cao game 577; x về phía trước, y lên): đầu trượng lúc giơ ở cast (−0,39; 1,65); tâm cầu ở skill theo giây
    0,66 (0,097; 1,079) → 1,05 (0,111; 1,732) → 2,05 (0,110; 1,722) → 2,20 (0,009; 1,792) → 2,25 (−0,009; 1,798), tỉ lệ cầu 1 → 1 → 2,28 → 2,5 →
    2,41, bán kính gốc 0,142. Đo lại: `J, img, _ = atomik_dang.load(rig/phap_lua_1.atomik); P = atomik_dang.Pose(J).at(<chỉ số clip>, t);`
    `P.bone_pt(<chỉ số xương "mieng">) / J["game"]["height"]`, tỉ lệ = `hypot(P.w[i][0], P.w[i][2])`.
  - Kiểm biên dịch ngoài Unity (csproj tạm ở scratchpad, `UseSharedCompilation=false`): 0 lỗi.
- **Unity** (người dùng cho dừng Play): refresh + biên dịch sạch → "Nhập dữ liệu" (88 tướng) → "Gắn dạng .atomik" (`hong_lien: prefab giữ 2 dạng
  (phap_lua_1, phap_lua_1)`) → "Đảo 70 ải: sinh lại" (`stages.json` không đổi) → ba menu golden + `golden_ghep.py`: chỉ `roster.json` 2 ô (n 3 →
  2, dạng ở sao cuối 2 → 1) và `sim.json` 1 ải (hoa 100: boss tiến hóa một lần). EditMode **106 / 107** (chỉ `PrefabOnlyTests` cũ ở `UI/Kit`).
- **Trong trận** (tour "riêng Viêm Sư", sao cuối = dạng 2; ảnh `Temp/PokiShots/hoa_fx/hong_lien_*`, tờ `phap_lua_1/trong_game/tour_mana_ult.jpg`):
  kim lửa hiện ở đầu trượng rồi cả loạt bay tới địch; cầu lửa của rig bay lên, phình, mốc `ban_cau` cầu hạt lao tới, nổ lớn + chớp màn; bàn tay
  thứ hai hiện ra cào địch ở đòn thường. Console không lỗi.
- **Cỡ**: lượt tour đầu (chiều cao game 577 = đỉnh mũ) thân tràn mép phải màn hình ở sao cuối → `phap_lua_rig.py` khai chiều cao cho game =
  max(đỉnh mũ, bề ngang idle / 1,16) = **662**; các số đo của `HatPhap.cs` đã nhân 577 / 662 (đầu trượng (−0,34; 1,44), bán kính gốc 0,124,
  tâm cầu (0,085; 0,940) → (0,097; 1,510) → (0,096; 1,501) → (0,008; 1,562) → (−0,008; 1,567)). Tour lần hai: con nằm gọn, chỉ đầu trượng lúc
  vụt xuống còn chạm mép phải.
- CHƯA: lưỡi lửa bị hút vào cầu còn thưa (khó thấy trên nền trời); `appear` / `die` của rig chưa được trận phát; hộp chi tiết tướng chưa chụp;
  chưa thử Android; dạng 1.

## 9. Dạng 1 (2026-11-14): gói concept

`build_phap_lua_non.py` (hình bố cục dựng thẳng từ `.atomik` dạng 2 bằng `mo_xe/atomik_dang.py`: đầu `bone6` 1,45; tóc `bone61` 1,2; trượng
`bone56` 0,72 + `cau_goc` co 0,72 dời (36, −62); đuôi áo `bone25` 0,85; tay tự do `bone11` 0,82; tay trượng `bone42` 0,9 →
`inbox/phap_lua_non/mau/bo_cuc.png`, `ti_le.json`) → `gui_gpt/phap_lua_non/luot_1_concept_theo_bo_cuc.txt`, `..._tron_hon.txt`. Thiết kế (đề xuất
của Claude): pháp sư lửa con, mũ trùm to gần nửa người, mắt lửa to, tóc ít, áo choàng vai ngắn, áo đỏ bé + váy lửa ngắn, trượng ngắn có cầu lửa
nhỏ, hai bàn tay vuốt nhỏ lơ lửng.

Concept dạng 1 về 2026-11-14: `inbox/phap_lua_non/tai_ve/L1_theo_bo_cuc.png` (A), `L1_tron_hon.png` (B). Claude chọn **A** (có quả cầu lửa tròn
nằm trong móc trượng, trượng đủ dài để diễn chiêu cuối; B trượng ngắn như đũa, chỉ có ngọn lửa không có cầu). Người dùng chưa xem hai ảnh này
(đã dặn "làm đi ... làm thêm dạng 1"); muốn đổi sang B thì làm lại mảnh.

## 10. Dạng 1 "Viêm Đồng" (`phap_lua_non`, 2026-11-14, máy ổ D): mảnh, rig, tiến hóa

Concept chốt (phiên chính chọn hướng A: cầu lửa tròn nằm trong móc trượng): `inbox/phap_lua_non/tai_ve/L1_theo_bo_cuc.png` = `L1_duyet.png`.

**Cách làm** (`phap_lua_non.py` + chế độ `PL_NON=1` của `phap_lua_rig.py`; dạng 2 dựng lại sau mọi lần sửa: `.atomik`, JSON, atlas trùng từng byte):
- **Khung concept → rig bằng mốc tay**: X = (x − 812) · 0,8 + 51; Y = (640 − y) · 0,8 + 266 (cổ ↔ gốc xương đầu `bone6`; 0,8 đơn vị / px, gần
  tỉ lệ concept dạng 2). Cả thân **hạ 170** (dáng gốc của `bone2`) cho váy lửa sát đất: con non thấp, đỉnh mũ 642.
- **4 tờ "đúng chỗ, đúng cỡ"** từ concept non (`gui_gpt/phap_lua_non/luot_2_manh_*.txt`, 75–120 s / tờ, đạt cả 4 ngay lượt đầu): `M_dau_lua` (mũ
  trùm + váy lửa), `M_than` (cổ áo choàng + áo đỏ + dây vàng, MỘT mảnh), `M_toc_duoi` (hai búi tóc + đuôi áo choàng), `M_truong` (trượng
  ngắn, không cầu). `phap_lua_non.py cat` cắt theo cụm liền → `inbox/phap_lua_non/manh/` + `dat_moi.json`.
- **Mảnh trong rig** (khoá riêng của dạng non trong `dat_moi.json`, đều bắt đầu bằng `_`):
  - `dau`: ảnh cứng trên `bone6` (như dạng 2). `lua_ao`, `ao`: lưới của mình, trọng số theo 14 đốt xương đuôi áo (`gan_xuong`).
  - `vai_duoi` (đuôi áo choàng): `gan_goc` trên lưới `pifeng_02`, vẽ SAU thân (`_lop`: thứ tự `lua_ao`, `vai_duoi`, `ao` thế chỗ `pifeng_03`).
  - `toc_tren`, `toc_phai`: **mảnh cứng trên hai xương MỚI** `toc_tren_x`, `toc_phai_x` (con của `bone6`, gốc xoay ở chỗ búi chui vào sau mũ),
    đung đưa ±3,5° / ±4,5° trong `aura`. Bản đầu bám lưới tóc `maofa_01` của họ: búi nằm xa ngoài lưới (tới 222 đơn vị) nên lúc chết / vụt
    trượng xương tóc quật mạnh, búi văng rời khỏi mũ → bỏ.
  - `_truong`: trượng là ảnh cứng của mình (lưới 4 đỉnh) đặt đúng chỗ concept trên `bone56`; bản thả rời trên `bone102` lấy cùng chỗ đó đưa qua
    T102 = A(bone102) · A(bone56)⁻¹ (A = px ảnh trượng của họ → thế giới dáng gốc của mình) nên quan hệ trượng ↔ xương y như của họ. Tâm cầu
    (440; 466) px concept, bán kính 76 px = **60,8** đơn vị (dạng 2: 81,8); cầu, tim, bốn lưỡi lửa, khói dùng lại ảnh dạng 2, co theo bán kính.
  - Hai bàn tay + bàn tay thứ hai trên `far`: dùng lại mảnh dạng 2, cỡ 1,0 (đo trên concept: gần bằng). `_xuong` dời gốc tay trượng `bone42`
    (−29; +114) và gốc tay vuốt `bone7` (+16; −20) cho bàn tay rơi đúng chỗ concept.
  - `_an`: bỏ `shenti` (dây bện), `zhuangshi_01/02` (gai sao), `pifeng_01`, `pifeng_02`.
- **Sửa riêng cho dáng thấp, đầu to** (cùng clip, cùng sự kiện với dạng 2):
  - `bone102` (trượng thả rời) lấy dáng gốc dời như bàn tay trượng (−29; −56) để lúc buông / chụp trượng không nhảy; `_tr_lech`: chiêu cuối
    trượng lơ lửng dời thêm (−460; −20) vào ra êm 0,3 s (không thì đứng chắn giữa mặt: mũ to, thân thấp), lúc chết dời (29; +273).
  - `_die_nang` 275: dáng nằm của họ làm mũ trùm chìm ~300 dưới đất → nâng `bone2` dần 0,35–0,75 s; đo lại: nằm ở y ≈ −22.
  - `_top` (40; 930): chỗ cầu lửa bay lên ở chiêu cuối (dạng 2: (64; 1000)).
- **Tiến hóa** (`phap_lua_non.py th`): gộp dạng 2 bản nhẹ (atlas × 0,40; hình của 65 / 98 slot không hiện ở idle thay bằng tam giác rỗng; khói
  dạng 2 ẩn vì chỉ chạy trong aura của nó; khoá idle dạng 1 sau 1,5 s bỏ) + clip `evolve` 3 s; dạng 2 trong rig gộp × 1,334 (cỡ 0,8 / 1,1).
  Chân dung dựng riêng (`chan_dung`: khung 0 idle, có cầu lửa + tóc; bản của `xuat_het` bỏ mọi slot mà aura đụng tới nên mất cầu lửa, tóc).

**Kết quả**: `inbox/phap_lua_non/rig/phap_lua_non.atomik` **502 KB** (137 + 135 xương, 73 + 76 slot, 10 clip kể `evolve`) + `rig/chan_dung.png`;
bản chưa gộp `rig_d1/phap_lua_non.atomik` 349 KB (137 xương, 73 slot, 1666 đỉnh, atlas 1056 × 1128). Chiều cao khai **642** (đỉnh mũ 642; bề
ngang idle 727 / 1,16 = 627). hit, attack, cast, skill, appear về khung 0 idle lệch 0,00 px; appear khung đầu trống, die khung cuối trống; đỉnh
tính từ `.atomik` lệch bộ vẽ Python ≤ 0,62 px. Khung 0 idle so concept: IoU hình bóng **0,913** (`rig_d1/so_concept.png`). Đã soi tờ khung cả 8
clip + `evolve` (bộ vẽ Python), khung cận idle / cast. Chưa soi runtime Chrome, chưa vào game.

**Số đo cho `HatPhap.cs` dạng non** (theo chiều cao khai 642; x về phía trước, y lên; `phap_lua_non.py do`; KHÔNG sửa C#):
- đầu trượng lúc giơ ở cast: 0,16 s (−0,393; 1,256) → 0,30 (−0,373; 1,277) → 0,50 (−0,378; 1,290) → 0,80 (−0,353; 1,311); lấy (−0,37; 1,28);
- tâm cầu ở skill: 0,66 s (−0,629; 0,755) → 1,05 (0,060; 1,447) → 2,05 (0,061; 1,438) → 2,20 (−0,030; 1,501) → 2,25 (−0,046; 1,507); tỉ lệ cầu 1 →
  1 → 2,28 → 2,5 → 2,41 (như dạng 2); bán kính gốc 0,095. Mốc 0,66 s lệch hẳn về sau vì trượng thả rời đã dời sang trái mũ.
- hitTimes 0,48 / 1,19 / 2,45, sự kiện y như dạng 2.

**Vào game** (phiên chính): `py -3 -I ArtGen/Spine/quai/doi_phap_lua.py chep_non ArtGen/Spine/inbox/phap_lua_non/rig` rồi `dang_1`; cỡ đề xuất
0,8 (`CO_NON`; `phap_lua_non.SIZE_A` phải trùng số này, đổi thì chạy lại `th`). `HatPhap.cs` cần bảng theo dạng như `HatRua` (`StageView.HoaUltDang`).

**Còn xấu / chưa làm**: cổ tay khói của tay vuốt là mảnh dạng 2 (dải khói dài rủ xuống tới y 850 px trên khung concept, concept vẽ búi tròn
ngắn); lưỡi lửa trên cầu là bộ 4 lưỡi của dạng 2 (cao hơn lửa trên concept); hit: mũ to nghiêng mạnh (clip gốc); chân dung DẠNG 2 trong game
thiếu cầu lửa và lửa dưới áo (cùng lý do aura; chưa sửa, ngoài việc này); `manh/wuqi.png` là file tạm lúc chưa có tờ trượng (không dùng).

## 11. Dạng 1 vào game (2026-11-14, phiên chính máy D)

- `quai/doi_phap_lua.py chep_non inbox/phap_lua_non/rig` → `Resources/phap_lua_non/` (502 KB, đã gộp `evolve`); `dang_1` → `heroes.json` khối
  `hong_lien`: dạng 1 **Viêm Đồng** (`phap_lua_non`, cỡ 0,8), dạng 2 Viêm Sư (`phap_lua_1`, 1,1). Số dạng không đổi → golden không đổi thêm.
- `HatPhap.cs`: `NCauPhap(..., non)` với bảng `PhapPNon`, `PhapR0Non` (số đo mục 10), nổ nhẹ hơn; mã `n_cau_phap1`;
  `StageView.HoaUltDang["hong_lien"] = { "n_cau_phap1", "n_cau_phap" }`. Chiêu mana dùng chung `n_kim_phap` (đầu trượng dạng non thấp hơn dạng 2
  chừng 0,16 chiều cao: chưa tách bảng theo dạng vì `FireMana` chưa nhận dạng).
- **Chân dung dạng 2** thiếu cầu lửa và lửa dưới áo (bộ xuất bỏ slot chạy trong `aura`): `phap_lua_rig.py` vẽ lại ở khung 0 idle (chỉ bỏ khói),
  `.atomik` dạng 2 không đổi; `doi_phap_lua.py chep` chép chân dung mới.
- Unity: refresh + biên dịch sạch, "Nhập dữ liệu", "Gắn dạng .atomik" (`hong_lien: prefab giữ 2 dạng (phap_lua_non, phap_lua_1)`), EditMode 106 / 107
  (chỉ `PrefabOnlyTests` cũ). `HoaFxTour`: menu "Đảo Hỏa: riêng Viêm Đồng (dạng 1) …".
- **Trong trận** (tour "riêng Viêm Đồng", tờ `inbox/phap_lua_non/trong_game/tour_dang1.jpg`): bàn tay thứ hai hiện ra cào địch, kim lửa bay từ đầu trượng,
  cầu lửa nhỏ bay lên phình rồi lao vào địch, nổ + chớp màn; console không lỗi. Kim lửa hiện hơi cao hơn đầu trượng của con non (xem trên).
- CHƯA: xem `evolve` trong hộp chi tiết tướng; các chỗ còn xấu ở mục 10; Android.
