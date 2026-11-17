# Thạch Giáp DẠNG 2 (`cong_da_2`, rig `monster_3528`)

Người dùng 2026-11-17: "làm thêm dạng 2 cho 3 con đầu đi", chọn rig 3528 (đống pha lê trên bốn chân pha lê), duyệt concept `L1_B`
("chân dài quá nhìn hơi dị, sửa lại" → chân tatu ngắn mập dưới váy đá) = `cong_da_2/tai_ve/L1_duyet.png`. Agent làm trọn tới `.atomik`.
Hình gốc Sword x Staff chỉ dùng nội bộ.

## Kết quả

- Rig: `inbox/cong_da_2/rig/cong_da_2.atomik` (287 KB, đạt đích 0,3 MB; 48 xương, 16 slot, 2348 đỉnh, 8 clip, 17 sự kiện), chân dung
  `rig/chan_dung.png`, tờ khung `rig/khung_<clip>.png`, `rig/xem.html`, `rig/game.json` (`cong_da_2_game.json`).
- Xem trước chiêu (rig thật + VFX tạm Python): `inbox/tho5_fx/cong_da2_{attack,cast,skill}.gif` + `_soi.png` (`tho5_fx_cong_da2.py`).
- Script: `cong_da2_manh.py` (prompt, mat, cat, ghep), `cong_da2_rig.py` (dựng + xuất; `soi`, `kiem`, `diem`), `tho5_fx_cong_da2.py`.
- Ảnh gen: 4 nhóm mảnh qua `gen_magnific.py` (Magnific gpt-2-6, bản 2k trước khi đặt trần, ~65 credit / ảnh, tổng ~260 credit); không dùng
  Codex.

## Mảnh và lớp

Concept to hơn con gốc ~1,2 lần: mỗi mảnh đặt theo chỗ trên concept, bám xương / lưới gần nhất của họ. Lớp (sau → trước):
bốn chân < `mai` < `tou` < `yankuang` < `vay` < `weiba_1` < `tinh_the`, `phach_t`, `phach_p`, `yezi_1`.

| Mảnh | Là gì | Gen | Bám |
|---|---|---|---|
| `mai` | núi đá trên (ba hốc trống), vẽ đủ phần khuất | M1 | MỀM nhiều khối `fangkuai_4/_1/_5/_6/__2/__3` (khối gần nhất, hoà mép 40 đv); vùng đỉnh (y concept < 280) chỉ `fangkuai_4` để cụm đỉnh không trượt khỏi hốc |
| `vay` | vòng tấm đá tròn dưới, trước thân | M2 | cứng `yao` |
| `tinh_the` / `phach_t` / `phach_p` / `yezi_1` | cụm pha lê đỉnh / hốc trái / hốc phải / mảnh nhỏ đỉnh trái | M2 | xương `pha_le` (con `fangkuai_8`), `ph_t` (`fangkuai_5`), `ph_p` (`fangkuai__2`), `yezi_2` của họ |
| `tou` | thân + đầu (tai, mày, mũi, miệng, nét mắt nhắm; không mắt) | M3 | mềm lưới `tou` + `yao`; phần xích đầu chuyển sang xương thêm `dau` |
| `weiba_1` | đuôi khoanh (tách khỏi thân M3 theo mảng màu) | M3 | lưới `weiba_1` |
| chân `jiao_l/shou_l/jiao_r/shou_r` | sau gần / trước gần / sau xa / trước xa (tách cặp giữa chồng nhau) | M4 | cứng xương chân dưới của họ |
| `yankuang` | CẢ con mắt cắt thẳng concept | — | xương `mat` (con `dau`): chớp = bóp dọc, lộ nét mắt nhắm của `tou` |

Mọi mảnh cứng và xương thêm đặt theo thế giới KHUNG 0 IDLE (att_idle0), không theo dáng gốc (dáng gốc lệch idle_01, làm pha lê lệch hốc).
Xương thêm: `move`, `day` (đáy chân), `tam` (giữa núi đá, cha `all`), `dau`, `mat`, `mieng` (chóp mõm), `pha_le`, `ph_t`, `ph_p`,
`far`, `fly_a/b/c`, `bay_a/b/c` (bản sao bay của cast).

## Chuyển động (giống ý dạng 1, mạnh hơn)

Clip gốc của 3528 xoay xích đầu và chân quá mạnh (thân tatu kéo giãn, chân văng khỏi váy) nên mọi clip viết trên dáng khung 0 `idle_01`
(chỉ xương thân, đầu, đùi, đuôi, pha lê); không dùng `run_01`, `skill_01_x`, `hit_01`, `die_01`.

| Clip | Dài | Mốc (giây clip) |
|---|---|---|
| appear | 1,70 | núi đá rơi, `cham_dat` 0,36, nảy, `bung` 0,66 (chân, đầu, đuôi hiện, chân duỗi ra), rũ mình 1,00–1,34, cau mày 1,38 |
| idle | 2,00 lặp | thở, đầu / khối / pha lê / đuôi lệch pha; đầu thò ra hít hít 0,50–0,98, chớp mắt 1,30, đầu rụt nhẹ 1,55–1,82 |
| walk | 0,60 lặp | chân bước chéo cặp, nhấc chân, núi đá lắc, đầu gật, đuôi vẫy |
| attack | 1,00 | ngửa lấy đà 0–0,30, lao húc chúi đầu, **trúng 0,46** (`trung`), quãng lao 0,55 × cao dồn vào `move` (game nắn), giữ 0,12, quá đà, về |
| cast | 1,52 | chồm đứng (đỉnh 0,46), lắc núi đá `ran` 0,26–0,60; cụm rời hốc `phong` a 0,46 (trái), b 0,52 (phải), c 0,58 (mảnh nhỏ); bay 0,20 → găm **0,66** (`trung`, khung trúng), 0,72, 0,78; giữ 0,14; bay về 0,30 (`ve` 1,10 / 1,16 / 1,22); dậm xuống `cham_dat` 0,68 |
| skill | 2,20 | rụt chân, hạ sát đất 0–0,22; gồng rung `gong` 0,30–0,84; cụm đỉnh nén rồi vọt lên trời `ban_troi` 0,90 (hai cụm hốc nảy theo); đứng chĩa mõm 1,06; mưa `mua` 1,22; mảnh to **trúng 1,56** (`trung`); cụm mọc lại `moc` 1,74 |
| hit | 0,50 | bật lùi đỉnh 0,07, nheo, pha lê lắc |
| die | 1,10 + 0,45 mờ | bật lùi, chân rụt, núi đá sụp chúi 0,28–0,62, mắt nhắm, đầu gục |

`game.json`: height 779,55; hitClips attack / cast / skill, hitTimes 0,46 / 0,66 / 1,56; stay cast, skill; far cast; muzzle
(249,6; 237,2); impact stop 0,08 / 0,07 / 0,16, shake 0,45 / 0,48 / 0,85, push 0,10 / 0,10 / 0,20, chớp `#ffffff40` ở skill.
`kiem`: attack dời 0,22–0,26 cao/khung ở khung lao (cú lao, đúng ý); cast cụm bay xoay 360° trong 0,2 s; skill cụm đỉnh vọt (vật bay) và
về hốc lúc còn ẩn.

## Vị trí xương cho HatTho.cs

Đơn vị chiều cao dáng đứng; x về phía đối thủ (+x của rig), y lên; gốc = giữa đáy hộp idle 0 (`cong_da2_rig.py diem`):
- idle `mieng` (chóp mõm) (0,349; 0,361); attack `mieng` 0,46 (0,820; 0,296) (đã cộng quãng lao của clip); cast `mieng` 0,68 (0,361; 0,412);
  skill `mieng` 1,22 / 1,56 (0,342; 0,334) / (0,347; 0,332).
- cast giữa núi đá `tam` 0,26 → 0,58 bước 0,08: (-0,011; 0,636), (-0,015; 0,644), (-0,016; 0,648), (-0,015; 0,647), (-0,014; 0,644).
- cụm rời hốc: a `ph_t` 0,46 (-0,312; 0,583); b `ph_p` 0,52 (0,281; 0,694); c `yezi_2` 0,58 (-0,297; 0,838).
- skill cụm đỉnh `pha_le` lúc vọt 0,90 (0,085; 0,870).
So dạng 1 (`NGiapSoi` / `NGiapMua` / `NGiapHuc`): mốc gần như cũ (cast trúng 0,66, skill 1,56 thay 1,50, attack 0,46 thay 0,40), nên hàm của
dạng 1 dùng lại được với bảng vị trí mới (mai cao ~0,64 thay ~0,6; hốc đỉnh 0,87 thay 0,725).

## Sửa lớp và đuôi (người dùng 2026-11-17: "lỗi layer và đuôi cũng lỗi")

Soi cạnh concept: ở góc dưới trái concept LỘ một khe hình nêm của thân tatu giữa hai tấm váy, phần cong của đuôi nằm TRƯỚC tấm váy giữa,
gốc đuôi chui dưới mép tấm váy trái. Bản trước: váy (M2) vẽ thêm tấm đá đè khe thân, thân (M3) vẽ hụt, đuôi "chỉ phần lộ" có mép cắt + nét
thừa chĩa lên trái, dán trên tấm váy. Sửa (`cong_da2_manh.py sua_lop`, chạy lại luôn tính từ bản gốc `*_goc.png`):
- Gen lại ĐUÔI LIỀN có gốc (`gui_gpt/cong_da_2/luot_4_duoi.txt` → `tai_ve/M_M5.png`, Magnific 1k high, 95 credit); tự dò dời (-2, 10) px cho
  khớp đuôi lộ trên concept; gốc lòi xuống dưới đáy tấm trái (chỗ concept là chân sau) xoá theo đường viền dưới đuôi trên concept
  (`VIEN_DUOI_DUOI`), lấy đúng nét mực concept làm viền.
- Váy: khoét khe nêm thân (điểm concept ấm mà váy vẽ đá, trừ vùng đuôi), mực concept giữ làm mép; thân: vá khe bằng điểm ảnh concept.
- Lỗ hai lớp: `vay_truoc` = LƯỚI CON trên chính ảnh `vay` (cùng điểm ảnh, cùng cứng trên `yao`: không lộ mép) chỉ phủ vùng gốc đuôi bên
  trái mép phải tấm váy trái (`MEP_TAM_TRAI`, đọc trên lưới px). Lớp mới: thân < váy < đuôi < `vay_truoc` < pha lê.
- Đuôi bám chuỗi xương riêng `duoi1` → `duoi3` (gốc ở chỗ chui dưới váy, con `yao`), trọng số mềm exp(-d / 28 px); lắc 1,5° / 4° / 7°
  (đuôi gốc của họ dài, khớp ở xa nên lắc làm gốc trồi khỏi váy).
- Soi bằng runtime Spine thật (`mo_xe/chay.py sheet`): phóng to đuôi + váy `inbox/cong_da_2/rt/*.jpg`, toàn thân 8 clip
  `inbox/cong_da_2/rt_full/*.jpg`, trước / sau `inbox/cong_da_2/rt/_truoc_sau.jpg`. .atomik 300 KB. Tổng Magnific: 5 ảnh ≈ 355 credit.

## Thân trước váy (người dùng 2026-11-17, lần 2: "phần đá vẫn bị nằm trên vỏ")

Người dùng coi việc váy đá đè thân (như concept vẽ) là lỗi lớp: THÂN + ĐẦU tatu phải nằm TRƯỚC váy đá dưới, thân là một khối tròn liền.
- Gen lại THÂN LIỀN không đuôi từ chính mảnh M3 (`gui_gpt/cong_da_2/luot_5_than.txt` → `tai_ve/M_M6.png`, Magnific 1k high, 95 credit):
  cùng chỗ, cùng cỡ, mặt / tai / mày / miệng y như cũ, chỗ đuôi cũ vẽ bù hông và bụng kem.
- `sua_lop` viết lại: váy bản gốc (không khoét), thân = M6 (bỏ miếng vá concept cũ: nó thành mẩu cam nhọn), mai nằm sau lưng (mép lưng của
  thân trùng mép dưới mai concept, phần chồng chỉ ~550 px vụn nên bỏ, giữ mã `mai_truoc` để dùng lại), đuôi trước thân, `vay_truoc` che gốc
  đuôi nhưng không đè thân.
- Lớp rig: chân < mai < váy < thân + đầu < mắt < đuôi < `vay_truoc` < pha lê. .atomik 302 KB.
- Soi runtime thật: toàn thân 8 clip `inbox/cong_da_2/rt_full/`, phóng to đuôi `inbox/cong_da_2/rt/`, trước / sau
  `inbox/cong_da_2/rt/_truoc_sau_2.jpg`. Tổng Magnific con này: 6 ảnh ≈ 450 credit.

## Hốc pha lê hai lớp (người dùng 2026-11-17, lần 3: "mấy cục đá vàng kia phải ở giữa lõm, bạn phải tách thành 2 layer, đọc lại skill")

Lỗi: ba cụm pha lê dán ĐÈ lên mai, đế rộng che vành hốc. Sửa theo memory lo-hai-lop (`cong_da2_manh.py hoc_pha_le`, gọi cuối `sua_lop`):
- Lòng hốc = khối sẫm trên ảnh mai (mean < 95, mở 4 px bỏ nét, đóng / mở 6 px cho trơn), gần gốc cụm nhất.
- Gốc cụm (trọng tâm 20 % điểm thấp nhất theo hướng mọc) đặt dưới tâm hốc 0,3 bán kính; cụm rộng hơn 92 % miệng hốc ở ngang tâm thì thu
  quanh gốc (hốc trái: thu 0,90); bỏ điểm pha lê phía gốc của đường cắt mà nằm ngoài lòng hốc.
- Nửa vành trước `vanh_d` / `vanh_t` / `vanh_p`: vành (nở 26 px) từ mép trong lòng hốc lấn vào 7 px (phủ nét mực mép trong), phía gốc của
  đường cắt qua tâm, chờm 5 px → rig dựng thành LƯỚI CON trên chính ảnh mai, bám mềm y như mai (cùng `bam_nhieu`, cùng chọn khối), vẽ ngay
  sau cụm của nó. Lớp: … đuôi < `vay_truoc` < `tinh_the` < `vanh_d` < `phach_t` < `vanh_t` < `phach_p` < `vanh_p`; cụm bay của cast (`bay_*`)
  vẽ trên cùng, về thì chui lại giữa hai nửa vành.
- Mầm pha lê nhỏ đỉnh trái (`yezi_1`): concept để gốc mầm khuất SAU mép tấm mai (rig gốc cũng để yezi sau các khối) → slot đưa ra SAU mai.

## Bảng tự soi trước khi báo (Claude chính 2026-11-17, runtime Spine thật, phóng to, idle + mọi clip ở dáng cực trị)

Tờ soi tổng: `inbox/cong_da_2/rt/_tu_soi.jpg` (concept duyệt cạnh idle 0, rồi mỗi clip một dải ba hốc + mầm, một dải chỗ nối); phóng to
`rt/hoc/<clip>.jpg`, `rt/noi/<clip>.jpg`, toàn thân `rt_full/<clip>.jpg`; trước / sau hốc `rt/_truoc_sau_3.jpg`.

| Mục | Kết quả |
|---|---|
| 1. Vật mọc từ hốc | ĐÃ SỬA: ba cụm hai lớp vành sau – pha lê – vành trước, gốc chìm trong lòng hốc ở mọi clip; cast lúc bay đi còn lòng hốc sẫm + hai nửa vành, về chui lại giữa; skill cụm đỉnh vọt rồi mọc lại từ trong hốc. Mầm đỉnh trái: ĐÃ SỬA (ra sau mép mai) |
| 2. Thân trước váy, mai sau lưng, chỗ nối | ĐẠT: thân + đầu một mảnh liền M6 (không nét mực trong giữa đầu và thân); chân sau thân và váy, đùi vẽ đủ phần khuất nên không hở; gốc đuôi chui dưới tấm váy trái (lưới con của váy, trừ chỗ thân) |
| 3. Thứ tự lớp so concept | ĐẠT trừ chỗ người dùng đổi (thân trước váy); mầm đỉnh và ba cụm hốc đã đưa về đúng concept |
| 4. Mép cắt, lỗ trắng / lỗ nền | ĐÃ SỬA: vào sân trước đây cho thân MỜ DẦN 0,06 s → nhìn xuyên thấy viền tấm váy qua thân; nay hiện tức thì. `lap_lo` quét mọi mảnh: không còn lỗ kẹp (đã lấp lòng xoắn đuôi, kẽ ngón). Chết mờ dần thì các lớp chồng thấy xuyên nhau (như mọi tướng) |
| 5. Mọi mảnh dính thân | ĐẠT: cụm pha lê chìm trong hốc, mầm mọc sau mép mai, chân dưới thân, đuôi từ mông |
| 6. Góc nhảy, bước dời 60 khung/giây (`cong_da2_rig.py kiem`) | ĐẠT: xoay lớn nhất 26° / khung (cast, lắc mai), không xương nào ≥ 45°; dời lớn nhất: attack 0,17 cao / khung ở cú lao (chủ ý), skill cụm đỉnh về hốc lúc còn ẩn (alpha 0) |
| 7. Idle không đơn điệu, đòn có lực | ĐẠT: idle thở + đầu thò hít hít + chớp mắt + đầu rụt + đuôi vẫy + cụm pha lê lắc trễ; attack lấy đà 0,3 s ngược chiều, lao, nén giãn, quá đà, pha lê lắc; cast chồm, lắc, dậm; skill rụt gồng rung, vọt. ĐÃ SỬA thêm: chân bật ra ở vào sân vượt 1,12 → 1,03 (trước thò dài khỏi váy như "chân cà kheo") |

.atomik 313 KB (dưới trần 0,5 MB; đích 0,3 MB vượt nhẹ vì thêm ba lưới vành). Không gen ảnh mới cho đợt hốc.

## Còn lại / câu hỏi

- Cụm bay của chiêu mana là pha lê hổ phách (hai hốc + mảnh nhỏ đỉnh), không phải sỏi: concept duyệt không có sỏi.
- Chưa làm clip `evolve` gộp dạng 1 → dạng 2 (như `doi_tinh_sat.py th`).
