# tm09 "Hàn Ngạc": ghi chú dòng 9 lô Thủy (2026-11-11)

Thay suất ải 60 đảo Thủy (Huyền Vũ, legend), đứng ngay trước boss cuối. Con gốc tham khảo `monster_3281` (Sword x Staff) là
**dạng 2** của dòng; phải vẽ lại dạng 2 rồi thiết kế thêm dạng 1 (chibi). Hình, màu, diễn xuất là của mình; con gốc chỉ cho
cấu trúc rig và nhịp.

## 1. Mổ con gốc (scan `D:\RefAnimation\SwordxStaff\scan\monster_3281\`)

Số: 35 xương, 29 slot (28 lưới + bóng), 224 đỉnh, 10 clip, 4 IK, không physics, không event. Atlas 992 × 120 (tỉ lệ 0,75), 0,1 MB.
Dáng: thú bò sát trắng thấp người, cặp sừng đen cong lớn, hàm to đầy răng, lòng miệng tím, 4 chân (chỉ vẽ 2 chân gần + 2 chân xa),
đuôi 5 đốt có 3 mảnh pha lê tím.

Cây xương:

```
root > bone (dời −50) > bone12 (thân: mọi clip xoay/dời ở đây) > bone29 (trục ở gáy, −63, 3)
  ├ bone2 (43°, len 50) > bone3 (len 125): ĐẦU / sọ trên; sừng jiao01, jiao02 bám bone3 (cứng); răng trên bone19..23 (5 xương, mỗi răng một xương)
  ├ bone11 (−15°, len 139): HÀM DƯỚI; răng dưới bone24..28 (5 xương)
  ├ bone4 (−145°) > bone5 > bone6 > bone7 > bone8: ĐUÔI 5 đốt; bone9, bone10 (con của bone7) + bone8: 3 mảnh pha lê ci01..03
  ├ bone13 > bone14 > bone15: chân trái gần (IK L1 2 đốt, L2 bàn chân); bone16 > 17 > 18: chân phải xa (IK R1, R2)
  └ shadow (con của bone)
IK target L1/L2/R1/R2 là con của bone (không theo thân) → bàn chân bám đất khi thân nhún
```

Mảnh (28): **thân cắt theo đường miệng**: `P_mouth01` (185 × 108, 26 đỉnh) là nửa TRÊN (sọ + lưng), bám bone3 đầu 9,5 / bone2 7,6 /
bone4 gốc đuôi 5,6 / bone11 3,3; `P_mouth02` (184 × 109, 18 đỉnh) là nửa DƯỚI (hàm dưới + bụng), bám bone11 hàm 7,4 / bone2 5,5 /
bone4 3,2 / bone5 1,8. Tức là cả con là một cái miệng: há miệng = lưới nửa dưới xoay theo bone11, hoà về gốc đuôi nên không hở
ở gáy. 10 răng mỗi cái một xương một mảnh (để răng lệch theo hàm). Đuôi `P_weiba` 30 đỉnh bám 5 xương (23/30 đỉnh nhiều xương,
tối đa 3). Chân gần 2 mảnh (đùi 16 đỉnh 3 xương, cẳng 17 đỉnh 2 xương) + 3 móng rời (mỗi móng một mảnh cứng). Chân xa tương tự.
Sừng 2 mảnh cứng. Pha lê đuôi 3 mảnh cứng.

Clip (nhịp từ khoá thật, `mo_xe/nhip.py`):

| Clip | Dài | Diễn |
|---|---|---|
| `idle_01` | 1,0 s, 100% bezier, 55 khoá | thân bone12 nhún; hàm bone11 mở 10,7° ở 0,23 s và 0,77 s (hai nhịp thở phập phồng hàm); đuôi 4 đốt lắc lệch pha; sừng đứng im |
| `skill_01` đòn cắn | 1,0 s, 89% thẳng | khoá cùng khung 0/3/14/16/18/22/26/30: 0,10 s nhún; **0,47 s hàm há −40°** (đuôi cuộn), 0,53 s thân chồm, **0,60 s hàm táp +17°** (quá đà 1 khung), 0,73 s giữ, về. Đúng luật "dáng → dáng, khoảng cách khoá quyết định tốc độ" |
| `skill_02` chiêu | 1,17 s, 42 timeline | hàm há −31° ở 0,33 s rồi **giữ há 20–31° từ 0,40 tới 0,80 s** (khoá mỗi 2 khung, dáng rung): kiểu "phun/gầm giữ" |
| `hit_01` | 0,5 s, 100% thẳng | khung 0 đã lệch (14°), đỉnh ở **0,07 s** (hàm −35°, thân bật), về ở 0,5 s. Không lấy đà |
| `hit_02` | 0,67 s | bị hất văng: thân xoay 56 → 408° (lộn một vòng), dời 239 lên |
| `die_01` | 1,0 s | thân xoay 165°, dời 210: lật ngửa, chân giãy, hàm trễ −43° ở cuối |
| `block_01` 0,5 · `floating_01` 1,5 · `run_01` 0,53 · `stun_01` 1,33 | | đỡ, bị hất lên, chạy (IK bước), choáng |

Lấy gì: cây xương (thân → gáy → đầu / hàm / đuôi), hàm là một xương, lưới thân chia trọng số đầu / hàm / gốc đuôi để há không hở,
răng rời theo hàm, bàn chân IK bám đất, nhịp cắn (há 0,47 → táp 0,60 trong 1 khung), chiêu giữ há rung. Không lấy: hình, màu, lộn vòng
khi trúng đòn (game mình `hit` chỉ bật lùi).

## 2. Thiết kế dòng

**Tên đề xuất:** dòng **Hàn Ngạc** (cá sấu băng vực sâu). Dạng 1 **Ngạc Nhi** (con non), dạng 2 **Hàn Ngạc Vương**. Tên khác để
chọn: Băng Ngạc / Băng Ngạc Vương; Ngạc Băng / Hàn Ngạc Đế.

**Lore:** loài cá sấu ngủ dưới đáy biển lạnh, sừng và gờ lưng là băng sông băng đục mọc trên xương, đuôi là chùy băng. Canh vực sâu
trước hang Hải Long (boss ải 70). Hàm khỏe nhất đảo Thủy: cắn vỡ tảng băng.

**Khác con gốc ở đâu:** loài khác (cá sấu mõm dài thay thú mõm ngắn), thân xanh petrol sẫm thay trắng, sừng băng đục thay sừng đen
bóng, lòng miệng xanh thẫm thay tím, thêm gờ băng dọc lưng, vảy sừng vai hông, đuôi chùy pha lê băng (3–4 khối đục) thay 3 mảnh pha
lê tím mỏng, tấm bụng, cổ rõ, góc nhìn 3/4 quay phải. Giữ: bò sát bốn chân thấp người, cặp sừng cong lớn, hàm to đầy răng, pha lê ở đuôi.

**Bảng màu** (tránh Thương Lam, Kuba: pha lê lam nhạt trong; Vây Lam: lam hoàng gia; Hải Long: ngọc lam sáng + san hô; Huyền Vũ:
lục + lam + vàng):

| Vùng | Dạng 1 | Dạng 2 |
|---|---|---|
| thân | `#3C8396` petrol sáng | `#1F5566` petrol sẫm |
| vảy sừng (vai, hông, gáy) | không | `#3F7585` |
| tấm bụng | `#D9E6EA` | `#D9E6EA` |
| băng đục (sừng, gờ lưng, pha lê đuôi) | `#E6F1F4`, cạnh `#9DBAC6` | như dạng 1 |
| mắt | `#F2B544` hổ phách | như dạng 1, đồng tử dọc |
| lòng miệng / lưỡi / răng | `#1B4F66` / `#4A9BB5` / `#F6FBFD` | như dạng 1 |
| móng | `#2B3F4A` | như dạng 1 |

**Dạng 1 — Ngạc Nhi (chibi):** đầu ~45% chiều dài, mõm ngắn, mắt hổ phách to, thân tròn, bốn chân mập ngắn, đuôi ngắn một pha lê
băng nhỏ; hai chồi sừng băng, ba gai băng nhỏ trên lưng; miệng hé thấy hai nanh sữa; mặt gan lì (mày cụp). Thân petrol sáng, không vảy sừng.

**Dạng 2 — Hàn Ngạc Vương (trưởng thành, legend):** đầu ~1/4 chiều dài, mõm cá sấu dài dẹt, mày gồ, mắt sắc đồng tử dọc; hai sừng
băng lớn cong ra sau rồi vút lên như lưỡi liềm (dài bằng đầu); gờ băng răng cưa dọc sống lưng từ sau sừng tới giữa đuôi, cao nhất ở
vai; vảy sừng to ở vai, hông, gáy; đuôi dài kết thúc chùy 3–4 khối băng; răng to kem lệch cỡ; thân petrol sẫm. Thế đứng thấp, bốn
chân dang, hàm hé: sẵn sàng táp. Khác hẳn dạng 1 về màu (đậm), bóng dáng (sừng liềm + gờ lưng + chùy đuôi), tỉ lệ.

**Đòn / chiêu** (theo lore hàm khỏe + băng; Pokémon: Ice Fang, Icy Wind, Frost Breath, Icicle Crash; phần lớn đứng tại chỗ):

| | Dạng 1 Ngạc Nhi | Dạng 2 Hàn Ngạc Vương |
|---|---|---|
| `attack` | **Cắn (Bite)**: chồm nhẹ tại chỗ, há 0,45 s, táp 1 khung ở 0,55 s, giữ có trôi, về (nhịp con gốc) | **Băng Nha (Ice Fang)**: lấy đà dài hơn (hạ thấp 0,35 s), há to 50°, táp mạnh kèm đuôi chùy quật xuống đất cùng khung; khựng, rung lớn hơn |
| `cast` | **Hàn Phong (Icy Wind)**: há mồm phun luồng hơi lạnh ngắn có mảnh băng vụn (VFX `beam` yếu), sự kiện `phun`/`het_phun` | **Hàn Lưu (Frost Breath)**: ngửa tụ 0,5 s, luồng băng dày dài hơn, mảnh băng to bay theo, giữ há rung hai dáng 0,9 s |
| `skill` | **Cọc Băng (Icicle Spear)**: dậm chân trước, 3 cọc băng trồi nối nhau dọc đất tới đối thủ (`line_erupt`, power 1) | **Băng Hà Sụp (Icicle Crash)**: gầm há tối đa, đuôi chùy nện đất → tảng băng lớn rơi từ trên xuống chỗ đối thủ, vỡ thành mưa mảnh băng (`rain` power 3, khối lớn cuối); khựng 0,2 s, rung, chớp màn |
| `hit` | bật lùi, đầu ngửa, hàm há, mí sụp, đỉnh 0,07 s | như dạng 1, sóng chạy từ mõm về đuôi, chùy đuôi văng sau cùng |
| `die` | giật, nhắm mắt, lả đi (đầu gục, lưỡi thè), đổ nghiêng, tan | thêm: sừng/gờ băng "rụng" (mờ dần trước) rồi thân đổ |
| `evolve` | nước dâng lốc, đổi dạng lúc lốc đậm nhất, dạng 2 gầm, khớp khung 0 idle dạng 2 | (dạng cuối không có) |

Hiệu ứng tia, mảnh băng, tảng băng rơi thuộc lớp VFX trên sân (không vẽ trong rig); rig để xương `mieng` (trục x hướng nhả) và
sự kiện `phun`, `het_phun`, `can`, `gam`, `het_gam`, `nen` (chùy đuôi chạm đất).

## 3. Dự kiến pha 2: tờ mảnh và xương

Tờ mảnh GPT (vẽ đủ phần bị che, mỗi dạng một bộ; 1536 × 1024, nền trắng, cách nhau ≥ 60 px):

- **M01 đầu:** sọ + hàm trên (không hàm dưới, không sừng, gáy để stump tròn), hàm dưới rời có dải lòng miệng + lưỡi nằm trong, mảng
  lòng miệng, lưỡi rời duỗi thẳng, 2 sừng rời (sừng xa, sừng gần cùng hình; lật bằng tỉ lệ âm), 2 mí mắt nhắm.
- **M02 thân:** thân từ gáy tới gốc đuôi (không chân, không gờ lưng) hai đầu tròn; gờ băng lưng rời thành 3–4 mảnh (vai, lưng, hông,
  đuôi); 2 mảnh vảy sừng vai/hông nếu cần tách; đuôi duỗi thẳng nằm ngang hai đầu tròn; chùy pha lê đuôi rời.
- **M03 chân:** chân trước gần (đùi + cẳng + bàn liền, duỗi, 3 móng) và chân sau gần; chân xa dùng lại hình chân gần tô tối hơn 8%
  (hoặc vẽ riêng nếu GPT ra đẹp).
- Dạng 1 giống nhưng ít mảnh: không vảy sừng, gai lưng 1 mảnh, sừng = 2 chồi.

Xương dự kiến (dạng 2 ~48, dạng 1 ~40; con gốc 35):

```
root > move > (shadow) > base (nghiêng, nén giãn) > hip > body1 > body2 > chest > neck > head
  head > jaw (khớp ở góc hàm sau) > tongue1..3 (rope, trọng lực); head > horn_b, horn_f (cứng); head > mieng (trục x hướng nhả); head > lid_b/lid_f (mí)
  chest > ridge1..2, hip > ridge3..4 (gờ băng, hơi xoay theo đốt thân, gần cứng)
  hip > tail1..5 > mace (cứng) — đuôi dải lưới B-spline, quẫy sóng từ gốc ra ngọn, mace nặng trễ 0,1 s
  chest > leg_fn (đùi) > shin_fn > foot_fn (IK bàn chân bám đất qua ground); chest > leg_ff ...; hip > leg_bn, leg_bf
  root > ground_fn/ff/bn/bf (mục tiêu IK, không theo base: thân nhún, chân không trượt)
```

Lưới: thân một dải dài (gáy → gốc đuôi) chia 4 đốt trọng số B-spline (không cột nào bám 100%), lòng miệng theo hàm (hàng dưới 100%
hàm, hàng trên chỉ bám đầu ở bản lề), đuôi dải 5 đốt, chân mỗi chân 2 đốt + bàn cứng, sừng/chùy/gờ cứng. Đích lưới dày đều theo
README `quai/`. Dung lượng đích ≤ 0,3 MB mỗi dạng (atlas 256 màu, dùng lại chân, sừng).

## 4. Pha 1: concept đã gen (2026-11-11, gói `build_tm09.py`, gen bằng `gen.py`)

Ảnh mẫu đính cho GPT: `Islands/refs/world_style.png` (nét), `inbox/hai_long/tai_ve/L1_duyet.png` (boss Thủy đã duyệt, mức chi tiết),
`inbox/vay_lam_3/tai_ve/L1_lien.png` (thú bốn chân Thủy đã duyệt, kiểu dáng đứng). Dạng 1 đính thêm concept dạng 2 đã chọn. Không đính
con gốc.

- **Dạng 2, lần 1** `inbox/tm09_2/tai_ve/L1_concept.png` → bản khác (lúc đầu chọn, sau đổi sang lần 2). Đúng thiết kế: thân petrol sẫm, sừng
  băng liềm, gờ băng lưng cao ở vai nhỏ dần về đuôi, vảy sừng vai hông, chùy đuôi 4 khối, tấm bụng, răng kem lệch cỡ, lòng miệng
  xanh thẫm + lưỡi, mắt hổ phách đồng tử dọc, móng xám; tô phẳng, không bóng, nền trắng, quay phải, bốn chân rời. Chưa ưng: miệng
  hé hơi ít (vẫn thấy lưỡi), sừng chạm gờ lưng. Tỉ lệ rộng/cao ≈ 2,2 → pha 2 khai `max_w` cho vừa sân.
- **Dạng 2, lần 2** (`--note` há miệng rộng hơn, ngẩng đầu, đuôi lộ trọn) → `L1_concept_2.png` → **chọn**, chép thành `L1_duyet.png`:
  cùng thiết kế, miệng há ~1/3 thấy rõ lòng miệng + lưỡi + hai hàng răng, đầu ngẩng, sừng không chạm gờ lưng, đuôi vểnh lên rời hẳn
  chân sau (dễ cắt mảnh, thế sẵn sàng hơn). Dạng 1 đã gen với bản 1 làm mẫu; cùng loài, cùng màu nên không gen lại.

Vướng mắc: không có. Codex không hết hạn mức trong lượt này (3 ảnh, 92–179 s mỗi ảnh). Chưa gen tờ mảnh, chưa rig (chờ duyệt).
- **Dạng 1, lần 1** `inbox/tm09_1/tai_ve/L1_concept.png` → **chọn**, chép thành `L1_duyet.png`. Chibi đầu ~45%, mõm ngắn, mắt hổ phách to,
  hai chồi sừng băng, ba gai lưng, một pha lê đuôi, tấm bụng, miệng há thấy hai nanh sữa + lòng miệng + lưỡi, thân petrol sáng
  `#3C8396`, mặt gan lì; tô phẳng, quay phải, bốn chân rời. Nét vân sáp hơi dày hơn dạng 2 (chấp nhận được; tờ mảnh pha 2 dặn lại độ dày).

## 5. Pha 2 (2026-11-11, sau khi concept được duyệt)

Tờ mảnh: `build_tm09.py` thêm `luot_2_manh.txt` mỗi dạng (M01 đầu/hàm/lòng miệng/sừng/lưỡi/mí/chùy, M02 thân/đuôi/gờ, M03 bốn
chân). Dạng 2 gen một lượt đạt (254 s): đầu không hàm không sừng, hàm dưới có răng, sừng gốc trái, lưỡi thẳng, thân ngang có vảy
sừng, đuôi thẳng gốc trái (GPT vẽ 1232 px, dài hơn dặn → co 0,72, dày 1,25), ba gờ đáy phẳng, bốn chân gập gối. Cắt: `tm09.py cat 2`
(ô lưới; ô giữa dưới tách lưỡi = mảnh dẹt nhất, mí = mảnh to, mí nhỏ = mảnh nhỏ), đục lòng miệng tự động; `_soi.png` kiểm: băng đục
`#E6F1F4` không bị coi là nền (doc_to loang từ mép, ngưỡng 236).

Rig `tm09.py` (thư viện `quai/`): 26 xương (root, move, than, hong, nguc, co, dau, ham, mieng, luoi0..2, duoi0..5, 4 chân × 2 đốt),
17 slot. Thân lưới vùng 4 xương (hong / than / nguc / co) hoà geodesic; đầu lưới vùng, gáy hoà vào cổ; hàm dưới lưới hai xương;
lòng miệng 5×3 thuộc hàm; lưỡi dải 3 đốt (DayMem trọng lực); đuôi dải 6 đốt B-spline + LoXo; chân lưới vùng + `chuoi_chieu` 2 đốt,
IK bàn chân bám đất theo `move`; sừng, chùy, gờ cứng; mí `fit_lid` còn hở 0 px. Mắt tìm tự động theo màu hổ phách.

Lỗi đã sửa khi soi: đuôi dài quá thân và vểnh như bọ cạp (co + bớt curl); sừng to bằng đầu (co 0,62); thân kiễng (bụng 0,40 chân);
lưới chân `luoi_dai` hở 10–28 px ở móng (đổi sang lưới vùng); clip chết thân không hạ vì đích IK đi theo `move` (thêm `theo_move=False`);
đuôi dựng lên lúc chết vì lò xo trễ (clip chết lò xo cứng hơn). `height` khai = max(cao, rộng / 2) (rộng 1430 / cao 497) → 715.

Dạng 2 kết quả: `inbox/tm09_2/rig/` 26 xương, 17 slot, 1921 đỉnh, 3038 tam giác, 7 clip, 3389 khoá, .atomik 219 KB (ĐẠT); nối clip
0,00 px; .atomik nạp lại lệch 0,10 px khung 0; runtime Spine thật (`spine_that/`) trùng bộ vẽ Python.

Dạng 1 (tờ mảnh về sau khi đợi khoá Codex): cắt `cat 1`, đạt ngay; tỉ lệ chibi chỉnh lúc nạp (`ti_rieng`: đầu, hàm, lòng miệng, mí
×1,3; thân 0,85; đuôi 0,5 dày 1,3; pha lê 0,6; chân 0,85) vì GPT vẽ tờ mảnh theo cỡ ô chứ không theo tỉ lệ concept. Chân gần của
con non vẽ **sau** thân (chân mập thò ra dưới bụng, giấu cục vai tròn); dạng 2 chân gần đè lên thân (cục vai = vảy vai). Mí dạng 1
còn hở 0 px. Rig gộp tiến hóa với dạng 2: 50 xương, 34 slot, 3600 đỉnh, 8 clip, .atomik 395 KB (dưới trần 0,5; vượt đích 0,3 vì atlas
gộp cả hai dạng 1008×1000); evolve khung cuối lệch 0,00 px, dạng sau co 0,772. `height` khai 575 (rộng 1150 / 2).

Chưa xem ở tốc độ thật (chỉ tờ khung 12 khung + runtime Spine thật `spine_that/`): rung hai dáng lúc giữ chiêu, lưỡi rũ, lò xo đuôi.
Việc cho Claude điều phối khi vào game: VFX hơi băng (cast), cọc băng (skill 1, sự kiện `nen` 0,7 s chỗ chân trước), tảng băng rơi +
mưa mảnh (skill 2, `gam` 0,8 / `nen` 0,93 chùy đuôi), đòn thường là cắn (sân kéo lao tới, `trung` 0,55 / 0,5); `height` đã khai theo
rộng/2, nếu trên sân còn to hoặc nhỏ thì đổi hệ số 2,0 trong `tm09.py rig()`.

### Sửa theo soi của Claude điều phối (vòng 2)

1. **Sừng mất**: mảnh sừng co nhầm còn 134 px (0,62 × 0,5 của tờ 432 px) và đặt góc thấp. Nay `sung` ×1,45 (≈ 300 px, cao ≈ dài
   đầu), gốc ở đỉnh sau sọ (0,15, 0,04 ảnh đầu), góc −28° (vươn ra sau rồi vút lên), sừng xa lệch sau, vẽ **sau đầu nhưng trước gờ
   vai** (slot `sung_xa` sau các `go_*`).
2. **Đuôi que**: dải lưới đuôi có độ dày đổi dọc chiều dài (`duoi_day`: đỉnh lưới đặt theo ảnh kéo dày gốc ×1,5 → ngọn ×0,9, uv giữ
   nguyên; dạng 1 ×1,8 → ×1,1), dài 0,75 tờ (≈ thân), gốc chôn sâu vào hông (−0,40 thân), vểnh lên bằng `curl` (−2° … −6° mỗi đốt,
   chùy ngang vai như concept).
3. **Dấu xoay chuỗi đuôi**: chuỗi đặt `lat=True` nên **góc âm = nhấc lên**, trước đó hiểu ngược. Attack: nhấc chùy lúc lấy đà →
   nện xuống đúng khung `trung` cùng cú táp → dội nhẹ → về. Sửa cùng dấu cho skill (nện ở `nen`), cast, hit (văng lên), die (rũ xuống),
   gồng/gầm trong evolve.
4. **Khung đầu clip = khung 0 idle**: dao động nền (`chuoi_song` lệch pha, thở, lắc) nhân cửa sổ sin²(πt/2) trong idle và sin²(πt/D)
   trong clip không lặp nên bằng 0 ở hai đầu; `curl` (dáng nghỉ đuôi) áp cho mọi clip kể cả die, evolve (gong/gam); mí trong die nhân
   thay vì ghi đè. Đo trên đỉnh lưới đã vẽ của mọi slot (`soi.lech`, gồm lò xo): khung đầu attack/cast/skill/hit/die/evolve lệch
   khung 0 idle **1,77 px (dạng 2) / 0,35 px (dạng 1)**, còn lại ở chùy do trạng thái lò xo idle (vòng lặp) khác trạng thái đã lắng.
5. **`so_concept.png`** (concept | khung 0 idle cùng bề rộng | chồng 55%): dạng 2 từ cao/rộng 0,35 → 0,41 (đầu ×1,5, chân ×1,15,
   bụng cao 0,5 chân, đuôi cong vểnh); dạng 1 0,36 → 0,44 (đầu ×1,6, thân 0,75, đuôi 0,45 mập, chân ×1,0, co cả con 0,42 cho
   nhẹ atlas). Còn khác concept: đầu dạng 2 vẫn nhỏ hơn concept một chút, gờ vai bị sừng che một phần, chân dạng 1 nằm sau thân (chồi
   sừng con non to hơn concept).
6. Chiêu 1 dạng 1 (dậm chân) đổi thành chồm nửa trước lên (hai chân trước rời đất) rồi dậm, vì chân gần vẽ sau thân.

Số mới: dạng 2 26 xương, 2423 đỉnh, 3927 tam giác, 3334 khoá, **.atomik 284 KB (ĐẠT)**, height 766 (cao 626, rộng 1531); dạng 1 gộp
50 xương, 3857 đỉnh, 6166 tam giác, 3715 khoá, **.atomik 442 KB (dưới trần)**, height 470 (cao 415, rộng 940), evolve khung cuối
0,00 px, dạng sau co 0,663.

### Vòng 3: đặt mảnh khớp concept bằng dò tự động (yêu cầu Claude điều phối)

- `tm09_place.py` (venv có cv2): mỗi mảnh dò SQDIFF có mặt nạ trên Lab (thô 0,5 → tinh 1,0) quanh **khung bao đọc trên concept kẻ lưới**
  (`rig/concept_luoi.png`); tỉ lệ ngang/dọc riêng (thân concept sâu hơn tờ GPT) nhưng chỉ dò ±2 % quanh tỉ lệ ước (dò tỉ lệ tự do bị
  lệch về mảnh nhỏ: SQDIFF chuẩn hoá theo diện tích, lần đầu co mọi mảnh còn 0,4–0,6, IoU ghép 0,48). Mảnh dài trơn (4 chân, đuôi)
  đặt theo hai đầu khớp đọc trên concept (`do_two`: gốc, ngọn, hệ cung / dây cung, bề dày đích). Ra `inbox/tm09_<k>/place.json`
  (toạ độ concept px) + `rig/so_ghep.png` (IoU ghép mảnh phẳng).
- `tm09.py dung()` dựng rig hoàn toàn từ `place.json`: **toạ độ rig = toạ độ concept × K** (K 0,6 / 0,5), gốc ở đất giữa chân;
  mảnh nạp đúng cỡ rig (ti riêng = max(sx, sy)·K, không phí atlas); xương thân/hông/ngực/cổ theo phân số của mảnh thân đã đặt; sừng con
  của đầu, gốc trong sọ theo dò; gờ băng chìm xuống lưng 18 px concept; chùy gắn theo động học thuận (vị trí ngọn đuôi SAU curl =
  vị trí concept, vì đốt cuối ở dáng gốc thẳng); hàm dưới cùng tỉ lệ dị hướng với đầu ×0,85; miệng dáng nghỉ hé (`ham_nghi`) như concept.
- `so_concept.png` mới: rig khung 0 idle vẽ thẳng vào khung concept (tỉ lệ 1/K) → IoU mặt nạ in ra (và ghi `so_sanh.md`), ô 4 là mặt
  nạ khác (đỏ thiếu, lam thừa).
- Mật độ lưới theo chiều cao con (bổ sung của Claude điều phối): bước viền 1,5 %, bước trong 2 % chiều cao con (dạng 2: 451 px →
  6,8 / 9,0 px; 3334 đỉnh = 7,4 đỉnh/px chiều cao), ghi vào `so_sanh.md`.
- Dấu xoay chuỗi đuôi đo bằng số (`sk.the_gioi`): góc âm = nhấc ngọn (đúng như vòng 2).

Kết quả vòng 3 (sau 4 lần dò + dựng): IoU ghép mảnh phẳng 0,661 / 0,704; **IoU khung 0 idle so concept 0,661 (dạng 2) / 0,674
(dạng 1)**, chưa tới đích 0,85. Phần thiếu (đỏ) tập trung ở: cổ + họng dày dưới đầu (tờ thân GPT không có cổ, đầu tờ không có
họng), bụng dưới sâu hơn tờ thân, hàm dưới concept há 35° và to bản hơn mảnh hàm, đùi sau to; phần thừa (lam): sừng (tờ sừng dày
hơn concept), chân xa lộ trên bụng, chùy lệch 40–60 px rig so với concept (ngọn đuôi sau curl chưa tới đúng điểm). Muốn lên 0,85 cần
gen lại tờ thân (có cổ dày, ngực sâu như concept) và tờ hàm/đầu theo đúng hình concept, hoặc cắt mảnh trực tiếp từ concept (cách
`thuy_long_lien`), vì các mảnh GPT vẽ khác hình concept không khớp được chỉ bằng đặt vị trí/tỉ lệ. Số: dạng 2 3537 đỉnh (7,8 đỉnh/px
chiều cao 451), .atomik 240 KB; dạng 1 gộp 7861 đỉnh (riêng 4324 = 11,2 đỉnh/px cao 386), .atomik 467 KB (dưới trần).

### Vòng 4: cách lai (chuẩn mới DAC_TA mục 5) — IoU 0,992 / 0,994

- Lượt 3 tờ GPT (M08 thân có cổ/họng, M09 đầu + hàm to bản) đã gen cả hai dạng (`gui_gpt/tm09_<k>/luot_3_than_dau.txt`), nhưng
  theo chuẩn mới chỉ còn dùng M09 cho mí (và để dành); thân/đầu/hàm lấy thẳng từ concept.
- `tm09_lai.py` (venv cv2): tách concept thành lớp bằng loang vùng từ hạt giống đọc trên `concept_luoi.png`, **nét mực là tường**
  (độ sáng < 85), tường kẻ tay thêm ở ranh không có nét (dạng 1: đầu–cổ x ≈ 992); lớp: `dau` (sọ + sừng + hàm trên), `than`
  (thân + cổ/họng + gờ băng), `duoi` (+ chùy), 4 chân phần thấy, `ham` (= vùng hàm dưới + lòng miệng + lưỡi của concept: thịt trong
  miệng đi theo hàm, dáng gốc đã há như concept); vẽ bù thân dưới chân/đầu và gốc đuôi từ mảnh GPT đã đặt theo `place.json`; bỏ mẩu
  rời < 400 px; ra `inbox/tm09_<k>/manh_lai/` + `nhan.png` (bản đồ vùng).
- `tm09.py dung_lai()`: toạ độ rig = concept × K; xương thân/hông/ngực/cổ theo lớp thân, đầu ở điểm cổ, hàm ở khớp hàm chĩa tới mút
  hàm đã há (`LAI[k]`), đuôi chuỗi theo trục đọc trên concept (đã cong sẵn, `curl` = 0) trọng số geodesic, chân chuỗi 2 đốt theo hai
  đầu khớp; mí GPT `fit_lid` trên lớp đầu (hở 0 px). Mảnh GPT còn dùng: chỉ mí.
- Clip: hàm ở dáng gốc đã há `ham_mo` (36° / 28°): cắn = xoay **+ham_mo** khép hẳn ở khung `trung`, há thêm khi cast/skill là góc âm
  nhỏ; idle táp = khép nhẹ hai nhịp; chết hàm trễ thêm 14°.
- Mặt nạ IoU: nền concept = vùng sáng nối mép (băng nhạt `#E6F1F4` bên trong là hình; ngưỡng 225 cũ coi băng là nền nên IoU bị
  trừ oan ~13 %); rig alpha > 160.
- Số: dạng 2: 22 xương, 9 slot, 3049 đỉnh (6,8 đỉnh/px cao 451), 5114 tam giác, 7 clip, 2554 khoá, **.atomik 195 KB**, IoU **0,992**;
  dạng 1 gộp: 42 xương, 18 slot, 6480 đỉnh (riêng 3431 = 8,9 đỉnh/px cao 386), 8 clip, 2791 khoá, **.atomik 372 KB**, IoU **0,994**,
  evolve cuối 0,00 px. Lưới hở 0 px (chân xa 1 px ở dạng 2). Khung đầu clip lệch khung 0 idle 0,49 / 0,07 px (đuôi, lò xo).
- Runtime Spine thật (`rig/spine_that/`, Chrome qua khoá): dạng 2 idle/attack/skill/die, dạng 1 idle/attack/evolve dựng trùng bộ vẽ
  Python (chùy nhấc 0,27–0,45 s, nện + hàm khép ở `trung` 0,55 s). Chưa xem ở tốc độ thật.

### Vòng 5: lớp thân mọc thêm dưới đầu / chân gần (sửa khe má–cổ dạng 1)

- `tm09_lai.py`: lớp thân MỌC THÊM dải `GROW_PX` (65 / 80 px concept ≈ 39 / 40 px rig) vào vùng đầu và chân GẦN (không mọc dưới
  chân xa: thân vẽ sau chân xa nên dải mọc sẽ che chân xa — lỗi đã gặp); dải bù lấy từ mảnh thân GPT đã đặt, chỗ GPT không phủ thì tô
  **màu chính của lớp thân** (trung vị pixel không phải mực, không phải tấm bụng) + vân nhẹ, kẻ nét mực dọc mép ngoài. Lỗi đã gặp:
  `cv2.inpaint` lấy màu từ biên vùng đã biết là nét mực → dải bù nâu đen (mảng đen ở họng dạng 1 trong evolve, ở cổ dạng 2 lúc chết).
- `rig()` thêm ảnh cận má–cổ ở khung đầu xoay mạnh nhất: `can_co_skill/attack2/hit/die.png` (+ `can_co_evolve.png`, `can_co_evolve2.png`
  dạng 1) và `can_bung_attack.png` (bụng–chân trước lúc 0,27 s). Soi: khe má–cổ kín ở mọi clip hai dạng; bụng–chân trước không khe;
  còn một nét mực mảnh của mép dải mọc thêm thi thoảng ló trên gáy khi đầu cúi (attack 0,64 s dạng 2), rất nhỏ.
- Số cuối: dạng 2 22 xương, 9 slot, 3275 đỉnh, 5484 tam giác, 7 clip, 2584 khoá, **.atomik 206 KB**, IoU 0,993; dạng 1 gộp 42 xương,
  18 slot, 7045 đỉnh, 12090 tam giác, 8 clip, 2801 khoá, **.atomik 395 KB**, IoU 0,994.

### Vòng 6: mép hàm/họng dạng 1 bo theo má

- Mảng chữ nhật dưới hàm (evolve 0,76 s) = dải thân mọc thêm lộ qua mép hàm/đầu, mép thẳng vì tường kẻ tay đầu–cổ là đường
  thẳng đứng. Sửa trong `tm09_lai.py`: tường thành cung `_ARC1` bo theo má (lồi về sau); lớp đầu/hàm làm mờ dần 30 px về phía
  tường, nhưng **chỉ** ở chỗ có dải thân mọc thêm nằm dưới và chỉ đoạn tường dưới mắt (y ≥ 400) — mờ cả đoạn qua sọ thì đỉnh đầu
  lộ nền xám (lỗi đã gặp). Dạng 2 không có tường kẻ tay nên không đổi.
- Soi: `can_co_evolve/evolve2/skill/cast.png` dạng 1 và `can_co_skill/cast.png` dạng 2: má–họng kín, mép tròn. IoU 0,994 / 0,993.
