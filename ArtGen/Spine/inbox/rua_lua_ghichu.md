# Rùa golem lửa (`rua_lua`): tướng thứ 5 đảo Hỏa

Bắt đầu 2026-11-13 (máy ổ C). Con gốc của rig: `monster_3425` (rùa golem đá bốn chân, pha lê đỏ trên lưng, mặt sọ đá, sừng to; game
tham khảo, kho `D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `run_01`). Cùng loạt golem với `monster_3422`
(golem lõi lửa, `golem_lua_ghichu.md`) và `monster_3423` (tượng đá giữ rừng). Xương, lưới, chuyển động gốc là của nhà phát hành game đó
(như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình. Tên, id game: chưa đặt (`rua_lua` chỉ là mã làm việc).

## 1. Lời dặn của người dùng (2026-11-13)

- "làm tướng thứ 5 đảo hỏa; concept **rùa golem lửa**, **đổi pha lê đỏ trên lưng thành gai lửa**, **lửa cũng phải có animation đung đưa nhẹ**".
- appear: "làm **cái mai nằm dưới đất** rồi **chân tay đầu đuôi mọc ra**, **gầm 1 phát**".
- idle, walk: "làm **giống họ đang làm**" (`idle_01`, `run_01`).
- Đánh thường: "tướng **bò nhanh tới mục tiêu** và **húc giống skill 03**".
- Chiêu mana: "làm giống **skill_04**: **đứng lên nhẹ, há mồm, tụ cầu lửa rồi bắn**".
- Chiêu cuối: "hơi đặc biệt: **tụ cầu lửa trên sừng** của tướng, **lửa sẽ được hút từ lửa trên lưng tướng**, khi **hút hết lửa** thì **phóng cầu
  năng lượng vào địch**".
- die: "**lửa tắt**, tướng **quỵ xuống**".

- Sau lượt concept 1 (2026-11-13): "**làm 2 sừng lành lặn** đi, **không làm gãy 1 bên**" (con gốc có sừng xa mũi cụt; mình bỏ chi tiết đó).

## 2. Mổ rig gốc (`<SXS>/scan/monster_3425/`: `info.json`, `att_goc.json`, `att_idle0.json`, `mo/idle0_*.jpg`, `mo/nhom_idle0.jpg`, `mo/can_*.png`, `parts/`, `khung/`)

48 xương, 27 slot (26 hình + `shadow`), 13 clip, 3405 khoá. Con nhìn sang PHẢI. Khác hai con golem kia: **có lưới trọng số** (mai, bụng, vành
mai, đuôi, bốn ống chân, cụm pha lê lớn), chỉ một bộ slot (không có bộ mảnh rời cho die). IK: bốn chân (`R1/R2` chân sau gần: bone17 →
bone18, bàn bone19; `L1/L2` chân sau xa: bone21 → bone22, bàn bone23; `SR1/SR2` chân trước gần: bone9 → bone10, bàn bone11; `SL1/SL2` chân
trước xa: bone13 → bone14, bàn bone15), mix 1. Không transform, path, physics.

Cây xương: `root → bone2 → bone → bone3 (hông) → bone4 (thân) → bone5 → bone6 (cổ) → bone7 (đầu)`; đầu: `bone33` hàm, `bone34` mặt,
`bone35` mắt, `bone36` sừng gần, `bone37` sừng xa (cha của 35–37 là bone34 theo chỉ số); đuôi `bone24 → 25 → 26` (con của bone3); trên mai
(con của bone4): `bone27` cụm cột đá gần, `bone28`, `bone29` cụm pha lê lớn, `bone30`, `bone31`, `bone32`, `bone38` pha lê / cột nhỏ.

Bảng mảnh ở idle (thứ tự vẽ sau → trước):
| thứ tự | slot | ảnh (px) | là gì → vai trò ở thiết kế mình | xương bám |
|---|---|---|---|---|
| 1 | `p_kuangshi07` | 65 × 86 | pha lê đỏ cuối mai bên phải, sau sừng → **gai lửa** | bone31 |
| 2 | `p_kuangshi06` | 43 × 51 | pha lê đỏ nhỏ sau mai, trên đuôi → **gai lửa nhỏ** | bone38 |
| 3, 4 | `p_datui05`, `p_xiaotui03` | | chân SAU XA: đùi, ống | bone21; bone22 0,64 + bone23 |
| 5 | `p_weiba` | 175 × 113 | đuôi ngắn, ba gai trắng (47 đỉnh) | bone24 0,45 + 25 + 26 |
| 6 | `p_kuangshi05` | 66 × 69 | hai cột đá đen đỉnh mai bên phải | bone32 |
| 7, 8, 9 | `p_xiaotuineice`, `p_datui02`, `p_xiaotui02` | | chân TRƯỚC XA: mặt trong ống, đùi, ống (có hai pha lê đỏ) | bone14; bone13; bone14 0,74 + bone15 |
| 10, 11 | `p_datui04`, `p_xiaotui04` | | chân SAU GẦN: đùi, ống | bone17; bone18 0,62 + bone19 |
| 12 | `p_xiongqiang` | 212 × 97 | bụng (tông sáng hơn) | bone5 + bone6 + bone4 |
| 13 | `p_guike02` | 247 × 81 | vành dưới mai / yếm | bone5 0,5 + bone4 0,5 |
| 14 | `p_datui01` | 85 × 75 | đùi chân TRƯỚC GẦN | bone9 |
| 15 | `p_ke` | 346 × 180 | **mai** (vòm đá ghép tấm, khoét vòm trên chân trước, móc xuống phía đầu) | bone5 0,55 + bone4 0,45 |
| 16 | `p_jiao01_2` | 86 × 114 | sừng XA: ngắn, mũi cụt | bone37 |
| 17 | `p_kuangshi04` | 22 × 32 | pha lê đỏ tí hon trên đùi trước gần → pha lê dung nham | bone9 |
| 18 | `p_kuangshi03` | 213 × 173 | **cụm bốn pha lê đỏ lớn** đỉnh mai (một cái cao nhất, hai cái ngả trái, một cái phải) → **bốn gai lửa** | bone29 0,5 + bone4 + bone28 |
| 19 | `p_kuangshi02` | 35 × 43 | pha lê đỏ nhỏ bên phải → gai lửa nhỏ | bone30 |
| 20 | `p_kuangshi01` | 164 × 131 | **cụm cột đá đen** phía gần, che gốc cụm pha lê | bone27 |
| 21, 23 | `p_xiaba01`, `p_xiaba` | 59 × 51, 95 × 99 | hàm: khối sau + hàm dưới (mép bậc như răng) | bone33 |
| 22 | `p_lian` | 95 × 112 | mặt sọ đá quay ba phần tư sang phải, một hốc mắt | bone34 |
| 24 | `p_yanjing` | 19 × 25 | mắt đỏ tam giác → mắt lửa | bone35 |
| 25 | `p_jiao01` | 117 × 196 | **sừng GẦN**: đế khối góc cạnh che góc trên trái mặt, vút cong lên phải | bone36 |
| 26 | `p_xiaotui01` | 116 × 131 | ống chân TRƯỚC GẦN (có ba pha lê đỏ) | bone10 0,71 + bone11 |

Clip của họ (tờ `khung/`):
| clip | dài | nội dung | dùng cho |
|---|---|---|---|
| idle_01 | 1,33 s | đứng thở, đầu gật nhẹ | **idle** |
| run_01 | 0,87 s | bò bốn chân | **walk**, đoạn "bò nhanh tới" của attack |
| skill_01 | 1,17 s | chồm hai chân trước lên 0,11–0,32, giậm xuống 0,42 | (tham khảo) |
| skill_02 | 1,20 s | cúi đầu chĩa sừng 0,11–0,44, chồm dựng người 0,55–0,76, giậm 0,87 | tham khảo cho chiêu cuối (dáng chĩa sừng) |
| skill_03 | 1,50 s | thụp xuống 0,14–0,41, **rạp người trượt tới húc** 0,55–0,82, bật dậy 1,09, về | nền **attack** |
| skill_04 | 1,17 s | thụp 0,11–0,21, **đứng cao bốn chân, ngẩng đầu** 0,32–0,85, về | nền **cast** (thêm há hàm) |
| block_01, hit_01/02, stun_01 | | | **hit** |
| die_01 | 1,00 s | bị hất tung 0,09–0,45, rơi sập bốn chân xoạc ra 0,55–0,73, nằm | nền **die** (thêm lửa tắt) |

## 3. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `rua_lua.py` (`mo`, `nhom`, `part_goc`), `rua_lua_bo_cuc.py` (sơ đồ bố cục 1536 × 1024 ở khung 0 idle, 1,048 px / đơn vị rig; bảy
pha lê đỏ trên lưng vẽ thành gai lửa bằng mã theo trục từng pha lê), `build_rua_lua.py` (gói `gui_gpt/rua_lua_1/`; ảnh mẫu: sơ đồ, Voọc
Tướng, golem lõi lửa đã duyệt, bản đồ).

Giữ của con gốc: dáng rùa golem bốn chân nhìn phải, đầu thấp phía trước, mặt sọ đá một mắt + hàm riêng, sừng gần to cong, sừng xa ngắn cụt,
mai vòm ghép tấm có cụm cột đá, bốn chân trụ, đuôi ngắn ba gai. Đổi: **pha lê đỏ trên lưng → gai lửa** (lửa thật dáng gai, mọc thẳng từ mai,
không vòng lỗ), mắt đỏ → mắt lửa vàng, pha lê nhỏ ở hai chân trước giữ là pha lê nhưng màu cam dung nham (người dùng chỉ dặn đổi pha lê
TRÊN LƯNG; đây là diễn giải của Claude), màu và chất liệu của mình. Tránh tông đã dùng ở đảo Hỏa (nâu đỏ gạch `quy_lava`, vỏ chai đen tím
`mat_lua`, giáp cháy đen `cung_lua`, đá tro xám kem `golem_lua`).

Ba hướng màu:
- `bazan` **A · đá bazan xám lam**: mai #4E5A6C, chân #5F6C7D, cột đá chàm than #353B48, bụng #8793A1, mặt sọ + hàm ngà #E6DAC0, sừng + gai đuôi ngà nhạt.
- `dat_son` **B · sa thạch vàng son**: mai #BA8E4A, chân #C9A05C, cột đá và HAI SỪNG nâu sẫm #5B4334, bụng cát nhạt, mặt sọ kem.
- `ca_phe` **C · đá nâu cà phê**: mai #5C4638, chân #68503F, cột đá nâu đen #382C28, bụng nâu nhạt, mặt sọ + sừng ngà.

Lượt 1 (2026-11-13, 94–105 s mỗi ảnh): `rua_lua_1/tai_ve/L1_bazan.png`, `L1_dat_son.png`, `L1_ca_phe.png` ra đúng bố cục sơ đồ ngay lượt
đầu (nhìn phải, một mắt vàng xếch, hàm riêng mép bậc, sừng gần cong to, sừng xa ngắn cụt, cụm cột đá che gốc lửa, bốn chân trụ, đuôi ba
gai, pha lê cam ở hai chân trước; tô phẳng, không quầng). Khác ý: lửa ra dáng **ngọn lửa bùng có móc cuộn** chứ chưa phải "gai lửa" →
gen thêm `L1_bazan_2.png` (`--note`: gai lửa thẳng, nhọn, một mũi, không móc cuộn) cho người dùng so. Trang so
`inbox/rua_lua_xem_concept.html`, đã mở cho người dùng chọn.

Lượt 1b (`build_rua_lua.py sung` → `luot_1b_sung_<bản>.txt`): vẽ lại đúng từng bản nháp, CHỈ đổi sừng xa thành sừng nguyên, mũi nhọn, cùng
kiểu sừng gần, nhỏ hơn, gốc nấp sau mặt (KEEP IDENTICAL / CHANGE) → `tai_ve/L1b_bazan.png`, `L1b_bazan_gai.png`, `L1b_dat_son.png`,
`L1b_ca_phe.png`. Sừng xa của rig (`p_jiao01_2`) là mảnh cứng một xương (`bone37`) nên đổi dáng tự do, không ảnh hưởng clip.

## 4. Kế hoạch rig và clip (sau khi concept được duyệt)

- Mảnh đá vẽ ĐÚNG KHUNG từng part của họ, lắp nguyên lưới (mai, bụng, đuôi, ống chân có trọng số); đủ 48 xương, IK chân nướng qua mẫu khung `l`.
- **Gai lửa**: 7 mảnh lưới riêng (4 của cụm lớn tách rời nhau), mỗi cái một chuỗi 3 đốt, gốc bám xương pha lê của họ; `lua_lay` như
  golem lõi lửa nhưng biên độ nhỏ hơn ("đung đưa nhẹ"). Co / tắt được từng cái (chiêu cuối hút lửa, die).
- Mảnh thêm: mắt tắt (die, appear), pha lê chân nguội (die), lòng miệng (cast há mồm: hàm `bone33` xoay xuống).
- **appear**: chỉ có cái mai nằm sát đất (đầu, bốn chân, đuôi rụt trong mai: co tỉ lệ về gốc, nấp sau mai và bụng; lửa chưa cháy) → rung nhẹ
  → chân sau, chân trước, đuôi thò ra lần lượt, đội mai lên → đầu thò ra sau cùng → lửa bùng trên lưng → gầm (ngẩng đầu há hàm, rung), về idle.
- **idle** = idle_01 (ba vòng, lửa đung đưa, một điểm phá nhịp: lắc đầu / phì lửa), **walk** = run_01.
- **attack**: bò nhanh (hai bước run_01 tăng tốc, `lunge`) → rạp người húc bằng sừng theo skill_03 (đỉnh lao = lúc húc) → lùi về.
- **cast**: skill_04 (đứng cao, ngẩng đầu) + há hàm; xương `mieng`, sự kiện `tu` / `phun`; cầu lửa là VFX.
- **skill** (chiêu cuối): cúi đầu chĩa sừng (dáng skill_02 0,11–0,44) → từng gai lửa trên lưng lần lượt co nhỏ, ngả về phía sừng rồi tắt
  (sự kiện `hut` mỗi cái, VFX vẽ dải lửa bay từ gai tới mũi sừng) → cầu lửa lớn dần ở mũi sừng (xương `cau`: chỗ + cỡ) → hết lửa: giật đầu
  hất sừng phóng cầu (sự kiện `nem`), thân giật lùi → lửa mọc lại dần, về idle.
- **die**: hit ngắn → lửa lụi từng cái, mắt tắt, pha lê nguội → bốn chân khuỵu, sập xuống (nửa sau die_01), đầu gục, mờ dần.
- VFX ngoài rig: cầu lửa ở miệng (cast), dải lửa hút + cầu năng lượng trên sừng (skill), bụi đá lúc húc.

## 5. Concept chốt, mảnh và rig (2026-11-13 chiều)

- Người dùng: "**A** nhưng **chân phải trước đang bị rách rời khỏi thân**" → lượt 1c (`build_rua_lua.py chan` → `luot_1c_chan_bazan.txt`): vẽ lại đúng
  `L1b_bazan.png`, chỉ nối chân TRƯỚC XA vào thân (tấm bụng chạy tiếp ra sau hàm tới chân, đùi lộ sau mặt) → `L1c_bazan.png` = **`L1_duyet.png`**.
  Lửa giữ dáng ngọn lửa bùng của A (người dùng không chọn A2 gai nhọn); pha lê cam ở hai chân trước giữ nguyên (người dùng không ý kiến).
- **Khung concept ↔ rig** (`rua_lua_rig.KHOP` = 1,144 px / đơn vị con gốc, ox 720, oy 934): khớp bằng mốc TAY (mũi sừng gần, mũi đuôi, mép
  ngoài và đáy ba chân). Viền part của rig chồng lên concept khít (`mau/_rig_tren_concept.png`). Khớp tự động theo tâm khung mảnh cho 1,20–1,24
  và lệch 40–70 px vì mảnh của mình vẽ thêm phần khuất.
- **25 mảnh, 6 tờ "đúng chỗ, đúng cỡ"** (`rua_lua_manh.py build` → `luot_2_manh_A..F.txt`, 77–152 s / tờ; cắt `rua_lua_manh.py lam`): mai, hàm,
  cụm cột gần, cột xa, hai sừng, mặt (có mắt), bụng, đuôi, bốn ống chân, đùi trước gần, bảy ngọn lửa vẽ đủ gốc; ba đùi khuất và lòng miệng vẽ ở
  góc trống của tờ (kiểu `r`: rig đặt theo khung part gốc; đùi trước gần Codex vẽ lệch nên cũng đặt kiểu `r`). Phần lớn mảnh Codex đặt đúng
  sẵn (lệch 0–2 px); chỉnh tay `CHINH`: mai (+10, −35), hàm (−4, −57, ×0,72), bụng (0, −55), lửa nhỏ (0, −22), lửa sau sừng (0, −6). Mai: Codex vẽ
  thừa cái móc cuộn + một ô đá dưới nét vành trái (gốc đuôi vẽ nhầm vào mai) → cắt (`MAI_CAT`, `MAI_O`). Đã thử dò tự động theo màu + nét mực:
  mảnh một màu cạnh mảnh cùng màu bị kéo lệch, phóng to → bỏ.
- Bằng mã: `mat_tat` (tròng mắt xám tro phẳng), `<ống chân trước>_nguoi` (pha lê nguội), `hong` đặt sau mặt + hàm, cắt trong hình mặt ∪ hàm lúc
  nghỉ và không thò ra bên phải mép răng cưa.
- **Thứ tự lớp** theo slot gốc, trừ: mặt đè lên hàm (mép răng cưa của mặt là răng trên); bụng nằm SAU chân sau gần (tấm bụng của mình dài hơn
  bụng gốc, lúc bò phủ lên chân sau như cái đĩa).
- **Rig** (`rua_lua_rig.py`): đủ 48 xương của họ + root + move + 7 × (gốc `_g` + 3 đốt) lửa + `mieng` + `cau` + `far` = 80 xương, 28 slot, 4200
  đỉnh. Mảnh cứng bám xương part gốc; mai, bụng, đuôi, bốn ống chân là lưới dày của mình bám theo lưới thưa của họ (`gan_theo_goc`, như
  `rong_vay_rig.gan_goc`). KG 0,80; PXU 0,92; chiều cao game 500 (bề ngang 710 / 1,42; đỉnh mai 383).
- **Clip** (8): `appear` 2,7 s (mai + bụng nằm sát đất, lắc → chân sau 0,56 → chân trước 0,74 → đuôi 0,98 → đầu 1,12 → lửa 1,42 → gầm 1,72);
  `idle` 4 s (3 vòng idle_01, vòng cuối phì lửa); `walk` (run_01); `hit` (hit_01); `attack` 1,56 s (bò nhanh = run_01 × 1,9 + lao 300 → rạp →
  húc theo skill_03, trúng 0,86); `cast` 1,6 s (skill_04 biên độ 0,62, há hàm 27°, tu 0,36 / phun 0,90); `skill` 2,7 s (thụp, bảy ngọn lửa lần
  lượt vươn về mũi sừng rồi co tắt từ 0,32, cách nhau 0,125 s; `day` 1,37; ngửa đầu; hất sừng `nem` 1,63; lửa mọc lại từ 2,05); `die` 2,2 s (giật
  lùi, lửa tắt từng ngọn, mắt tắt, pha lê nguội, sập 1,0, tan).
- **Bẫy đã gặp:** (1) góc xương chân nướng IK gần ±180° so với dáng gốc: quy từng clip về gần 0 thì hai clip lệch nhau một vòng, pha ra xương
  quay 350° / khung → quy KHUNG ĐẦU mọi clip về cùng vòng với khung đầu idle_01 (`_cd`). (2) Clip của họ bật cả thân trong 1–2 khung (thụp của
  skill_04, xoạc chân của skill_03, giật của hit_01): hình mình to nên lộ → `mau_tr` (trung bình tam giác ± 1–2 khung) + giãn giờ. (3) co
  `bone6` (cổ) ở appear làm rách mép bụng (bụng bám một phần vào cổ) → co `bone7`. (4) Lúc `die` tan, các lớp trong dần làm lộ lòng miệng cam →
  ẩn `hong`.
- **Đo** (`rua_lua_kiem.py` + `chay.py sample ... 60`): runtime thật 60 khung/giây không có bước xoay ngược vòng; lớn nhất 35° / khung (chân
  sau gần lúc lùi về của attack), 29° (hit, khung đầu: cú giật của họ). Mọi clip về idle 0 px; appear khung đầu trống, die khung cuối trống.
  `.atomik` 432 KB. Trang `rig/xem.html` (thu_xem: đủ 8 clip), tờ runtime `rig/that/`. Đã mở cho người dùng xem.

CHƯA làm: VFX (cầu lửa ở `mieng` cho cast; dải lửa hút từ `<lửa>_g` tới `cau` + cầu lửa lớn dần ở mũi sừng + cầu bay tới địch cho skill; bụi đá
lúc húc), gắn vào game (tên, id, suất 5 đảo Hỏa, số liệu), dạng 2.

### 5b. Sửa sau khi người dùng xem appear (2026-11-13)

Người dùng (ảnh chụp lúc chỉ còn cái mai): "phần mai bạn lại **tính 1 phần chân là mai rùa** nên nó **khuyết mất 1 mảnh**, ngoài ra có **1 cục đá dựng bên
kia lơ lửng hơi lệch**".
- **Mai**: tờ A vẽ mép dưới của mai lõm thành vòm ở chỗ chân trước gần đè lên (prompt của tôi còn tả "the arch over the near front leg"), cộng
  cái móc và ô đá tôi cắt bỏ → đứng một mình thì khuyết. Gen lại riêng tờ **G** (`P["mai"]`: vòm KÍN, mép dưới một đường liền phồng xuống, cấm
  khoét vòm / khấc cho chân); bỏ `MAI_CAT`, `MAI_O`. Codex vẽ thấp hơn concept → `CHINH["mai"] = (10, −60, 0,98, 0,90)` (dời lên, co dọc).
  Lượt gen đầu của tờ G treo 17 phút giữ khoá Codex (phiên phap_lua báo): đã dừng tiến trình, chạy lại với `--timeout 420`, 121 s là xong.
- **Cột đá xa** (`cot_xa`, nằm SAU mai như con gốc): mai cũ ngắn bên phải nên chân cột lộ ra ngoài mép mai, trông lơ lửng. Mai mới rộng gần bằng
  mai của rig gốc nên chân cột (đáy y 518) nấp sau mép mai (mép trên của mai ở đó y ≈ 454). Không phải dời cột.
- Xuất lại: 4439 đỉnh, `.atomik` 447 KB, mọi clip về idle 0 px; tờ runtime `rig/that/appear.jpg` đã soi.

## 6. Vào game (2026-11-13, người dùng: "ok ổn cho vào game đi")

Suất 5 đảo Hỏa = ải 20 của đảo ("Lò Lửa Thiền", `IslandGen.Plan Hoa`), id **`nguu_quyen`** (trước là Ngưu Quyền). GIỮ id tướng, id thẻ, chỉ số,
hiệu ứng thẻ, số dạng (3) → golden không đổi (golden chỉ ghi id), không đổi saveVersion.
- `quai/doi_rua_lua.py` (`--kiem`, `--ve_cu`, `chep`): `heroes.json` khối `nguu_quyen` (tên **Hỏa Quy** cả ba dạng, danh hiệu "Rùa đá cõng lửa",
  dòng "Dòng Hỏa Quy", `aola` tướng + ba dạng → `rua_lua_1`; cỡ 0,9 / 1,02 / 1,14 giữ); `cards.json` tên / icon ba thẻ: Song Quyền Lửa → **Hỏa
  Cầu** (flame), Ngưu Ma Liên Quyền → **Sừng Tụ Hỏa Cầu** (sun), Máu Đấu Sĩ → **Mai Nung Đỏ**. Tên do Claude đặt, người dùng có thể đổi.
  `chep`: `rig/rua_lua_1.atomik` + `chan_dung.png` → `Assets/03 Art/Heroes/Resources/rua_lua_1/` (thư mục mới; `nguu_quyen_1..3` cũ giữ nguyên).
- `HatLua.Themes["nguu_quyen"]`: bảng lửa cam thường + mảnh đá xám lam (trước: pal "nguu", mây xoắn vàng). `StageView.FireFx["nguu_quyen"]`
  giữ ("cau", "no_lon"): chiêu mana cầu lửa từ xương `mieng`, chiêu cuối nổ lớn ở địch; thêm chú thích. `HoaFxTour`: menu "Đảo Hỏa: riêng Hỏa
  Quy, đòn thường, chiêu mana, chiêu cuối (đang Play)". `GD_Claude/13_DanhSachTuong.md` dòng ải 20 ghi thêm.
- Unity (cầu MCP cổng 8080, đã báo bốn phiên khác): refresh (biên dịch sạch), "Nhập dữ liệu", "Gắn dạng .atomik vào prefab tướng"
  (`nguu_quyen.prefab`: ba dạng cùng trỏ `rua_lua_1.asset`), EditMode **102 / 103** (chỉ hỏng `PrefabOnlyTests` cũ ở `UI/Kit`, không liên quan;
  cùng mức các phiên khác báo trước đó).
- **Trong trận** (tour Hỏa Quy, ải 3, sao cuối = dạng 3; ảnh `Temp/PokiShots/hoa_fx/`, tờ `rig/_game_*.jpg`): bò tới húc đúng chỗ địch; há mồm
  tụ cầu lửa ở mõm rồi bắn, nổ ở địch; chiêu cuối lửa trên lưng co tắt lần lượt, hất sừng, nổ lớn ở địch, lửa mọc lại. Viền sticker, lật trái
  phải đúng.
- **Cỡ**: chiều cao game 500 (bề ngang / 1,42) thì ở dạng 3 con rộng ~60 % bề ngang màn hình, đuôi bị mép phải màn cắt → đổi sang bề ngang /
  1,16 = **612**; xuất lại, chép lại, chạy lại tour: con nằm gọn trên bệ.

CHƯA làm: VFX riêng của chiêu cuối (cầu lửa lớn dần trên mũi sừng `cau` + dải lửa hút từ `<lửa>_g`; hiện chỉ có vụ nổ ở địch); `appear` / `die`
của rig chưa được trận phát (`StageView` vẫn dùng rơi xuống / nghiêng mờ chung, xem `quai/VAO_GAME.md` mục 6); dạng 2, 3 riêng (đang dùng chung
một rig, chỉ to dần); chưa thử trên Android.

## 7. VFX cầu lửa (2026-11-13, người dùng: "bạn chưa làm cầu lửa trên sừng của rùa à")

`Assets/01 Script/Game/Battle/HatRua.cs` (phần `partial` của `HatLua`), đi đường "n_" (`StageView.PreFx` → `HatNuoc.PlayNuoc`: phát từ đầu clip,
biết `lead` = khung trúng của clip) vì cầu phải tụ TRƯỚC khung nhả. `StageView.FireFx["nguu_quyen"] = ("n_cau_rua", "n_cau_sung")`.
- **`n_cau_sung`** (chiêu cuối, `NCauSung`): từng ngọn lửa trên lưng, đúng thứ tự và giờ của clip (ngọn đầu 0,32 s, cách 0,125 s, mỗi ngọn 0,30 s),
  nháy tia ở gốc rồi nhả 46 lưỡi lửa nhỏ / giây: bốc lên theo đà rồi tự lái, nhanh dần, vào tâm cầu. Cầu = lõi `tron` 85 hạt / giây bám mũi sừng
  (`LoiCau`, như lõi `Fireball`), bán kính 0,2 → 1 lần R theo căn của tiến độ hút (R = 0,2 chiều cao tướng), tâm ngay trên mũi sừng; lưỡi lửa
  liếm ra từ thân cầu. Đầy (1,37 s): vòng nháy nhỏ + 8 tia, than hồng lách tách. Hất sừng (1,63 s = `lead`): cầu rời sừng bay 0,30 s (bắn nhanh
  rồi vào đích, vồng nhẹ), đuôi lưỡi lửa + khói + tia; chạm: `CauNo` 1,4 (sao gai, vòng dưới chân, vành lưỡi lửa rải đều góc, mảnh đá xám lam,
  tia), nổ phụ +0,13 s, khói và tro +0,34 s.
- **`n_cau_rua`** (chiêu mana, `NCauMieng`): 0,54 s trước khung nhả than hồng hút vào mõm, cầu lớn dần ở mõm (chỗ nhả = `game.muzzle` = xương
  `mieng`); nhả thì bay 0,36 s tới đối thủ, `CauNo` 0,9. Trước đó dùng mã "cau" (`Fireball`): cầu chỉ bắt đầu tụ SAU khung nhả, lệch với clip.
- **Vị trí** mũi sừng theo giây (`SungT`, `SungP`) và giữa từng ngọn lửa lúc bị hút (`LuaLung`) là số đo trên rig, phần của chiều cao game (612),
  x về phía trước, y lên. Đổi clip skill hoặc hình thì đo lại:
  `sk, info = R.dung(); clips = R.lam_clip(sk, info); fr = hoat.nuong(sk, clip skill); W = sk.the_gioi(fr[round(t * 30)]);`
  `W["cau"][:2, 2] / info["cao"]` (mũi sừng), `W["<lửa>_g"]`, `W["<lửa>_2"]` (gốc, ngọn từng ngọn lửa).
- Đã chạy tour "riêng Hỏa Quy" trong Play (tờ `rig/_game_ult2.jpg`, `_game_mana2.jpg`): dải lửa chảy từ lưng về mũi sừng, cầu lớn dần đúng trên
  mũi sừng, rời sừng đúng khung hất, nổ ở địch; chiêu mana cầu tụ ở mõm lúc há mồm. Console không lỗi. Vòng nháy lúc đầy bản đầu rộng 2,3 R
  trông như hồng tâm nâu → thu còn 1,55 R, 0,18 s (bản thu nhỏ chỉ biên dịch và chạy test, chưa chụp lại).

## 8. Hai dạng + dạng 1 rùa non chibi (2026-11-13 chiều)

Người dùng: "con này **2 dạng thôi**, **làm dạng 1 nữa** nhưng hình như gpt hết token rồi" (Codex báo hết hạn mức, mở lại 18:30), xem ba hướng đầu
(A mầm lửa, B đủ lửa nhỏ, C đầu to) rồi dặn "tôi muốn **chi bi hơn, nhỏ hơn nữa**".
- **Dạng 1 không cần gen** (`rua_lua_non.py`): xếp lại MẢNH dạng 2 ở tỉ lệ non: đầu phóng quanh một điểm, hai sừng co về gốc sừng, cụm cột đá co
  về chân cột, lửa co quanh gốc lửa, bỏ bớt lửa / cột đá xa; ghi `_sung_mui`, `_mieng` mới vào `dat.json`. Rig = `RL_NON=<hướng> rua_lua_rig.py`
  (cùng xương, cùng clip) → `inbox/rua_lua_non/rig_<hướng>/rua_lua_non.atomik`. Hướng đang dùng: **`chibi`** (D): đầu × 1,38 quanh (950, 800) (điểm
  thấp gần mõm: đầu nở lên trên, hàm không chạm đất), sừng × 0,40, cột đá × 0,60, ba ngọn lửa × 0,44–0,50, cỡ trong game **0,78** (dạng 2: 1,1).
  `chibi_1` (E) = như D, một ngọn lửa. Tờ so `inbox/rua_lua_non/so_dang.jpg`, trang `inbox/rua_lua_non_xem.html`. Người dùng CHƯA chọn giữa D / E.
- **Tiến hóa** (`rua_lua_non_th.py`, chép từ `golem_lua_non_th.py`; `RL_NON`, `RL_CO`): gộp dạng 2 × 1,41 vào rig dạng 1, clip `evolve`, 552 KB;
  `chep` → `Resources/rua_lua_non/` (+ chân dung).
- **Dữ liệu** (`quai/doi_rua_lua.py hai_dang`): khối `nguu_quyen` forms 3 → 2: "Hỏa Quy Con" (`rua_lua_non`, 0,78), "Hỏa Quy" (`rua_lua_1`, 1,1); aola /
  size chung = dạng 1. Tên do Claude đặt.
- **VFX theo dạng**: `HatRua.NCauSung(..., non: true)` (bảng `SungPNon`, `LuaNon`, lượt hút 1 / 3 / 4, cầu 0,155 chiều cao, nổ 1,1), mã `n_cau_sung1`;
  `StageView.HoaUltDang["nguu_quyen"] = { "n_cau_sung1", "n_cau_sung" }` (chiêu cuối hệ Hỏa theo dạng, đè lên `FireFx`).
- **Unity** (đã báo các phiên khác; sao lưu golden, heroes.json, stages.json, HeroDb, prefab ở scratchpad phiên này `sao_luu/`): refresh sạch →
  Nhập dữ liệu → Gắn dạng (`nguu_quyen.prefab` 2 dạng) → Đảo 70 ải sinh lại (`stages.json` không đổi) → ba menu golden + `golden_ghep.py`:
  **chỉ `roster.json` đổi 2 ô** (forms của nguu_quyen: n 3 → 2, dạng ở sao cuối 2 → 1); sim, battles, islands, progression… không đổi. EditMode
  102 / 103 (chỉ `PrefabOnlyTests` cũ).
- **Trong trận** (menu "Đảo Hỏa: riêng Hỏa Quy Con (dạng 1) …", tờ `inbox/rua_lua_non/_game_dang1.jpg`): rùa non húc, bắn cầu lửa từ mõm, chiêu cuối
  ba dải lửa hút vào cầu trên mầm sừng rồi phóng; console không lỗi.

CHƯA: người dùng chọn D hay E (hoặc đẩy chibi thêm); dạng 1 vẽ riêng (thân tròn mập) nếu muốn thì chờ Codex sau 18:30; chưa xem clip `evolve`
trong hộp chi tiết tướng; appear / die của rig chưa được trận phát; chưa thử Android; chưa commit.

## 9. Dạng 1 tạm = bản E; gen riêng bản chibi khi Codex mở lại (2026-11-13, 17:30)

Người dùng xem D, E: "**E cũng được** nhưng sẽ **phải gen lại bằng gpt cho chi bi hơn**".
- **Trong game hiện tại dạng 1 = E** (`rua_lua_non.py` hướng `chibi_1`: đầu × 1,38, sừng mầm, MỘT ngọn lửa giữa lưng, cỡ 0,78): rig
  `inbox/rua_lua_non/rig_chibi_1/`, gộp tiến hóa (`RL_NON=chibi_1 RL_CO=0.78 rua_lua_non_th.py chep`) → `Resources/rua_lua_non/`.
- `rua_lua_rig.py`: dạng ít lửa thì các ngọn CÓ MẶT chia đều quãng hút (`HUT_CO`, `HC_CACH`); chỉ một ngọn thì nó co chậm suốt quãng tụ
  (`HC_DAI = T_DAY − H0 − 0,08`); dạng 2 (7 ngọn) giữ nhịp cũ. `HatRua.NCauSung(non)`: một nguồn (0,22; 0,44), dải lửa 30 hạt / giây suốt quãng tụ.
- Unity: refresh sạch, Gắn dạng, tour "riêng Hỏa Quy Con" chạy không lỗi (tờ `inbox/rua_lua_non/_game_dang1.jpg`). Dữ liệu và golden không đổi
  thêm ở bước này.
- **Gói gen bản chibi vẽ riêng** (`build_rua_lua_non.py` → `gui_gpt/rua_lua_non/luot_1_concept_theo_e.txt`, `..._tron_hon.txt`, `HUONG_DAN.md`): ảnh
  mẫu 1 = hình bố cục bản E dựng từ rig (`inbox/rua_lua_non/mau/bo_cuc_e.png`), ảnh mẫu 2 = concept dạng 2 đã duyệt. Hai hướng (đề xuất của
  Claude): `theo_e` (giữ chỗ đặt của bản E, vẽ lại nét chibi), `tron_hon` (mai tròn ngắn như hòn cuội, chân lùn hẳn, đầu gần nửa chiều cao).
- **Hẹn giờ**: tiến trình tách `inbox/rua_lua_non/cho_gen.py` (bắt đầu 17:31) chờ tới 18:32 rồi chạy `chay_hoa.py` hai file; nhật ký
  `inbox/rua_lua_non/cho_gen.log`; ảnh về `inbox/rua_lua_non/tai_ve/L1_theo_e.png`, `L1_tron_hon.png`.

VIỆC TIẾP khi có ảnh: soi hai concept (chibi thật chưa, chân dính thân, hai mầm sừng lành lặn, một lửa), mở cho người dùng chọn; duyệt xong thì
gen mảnh "đúng chỗ, đúng cỡ" như dạng 2, khớp khung bằng mốc tay, đổi tỉ lệ xương nếu thân ngắn / chân lùn hơn rig, xuất lại, gộp tiến hóa, chép
đè `Resources/rua_lua_non/`, đo lại `SungPNon` / `LuaNon` cho `HatRua.cs`.
