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
