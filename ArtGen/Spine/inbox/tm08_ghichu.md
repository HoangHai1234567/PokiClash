# Ghi chú dòng tm08: Uyên Xà (rắn vực sâu), lô 10 tướng mới đảo Thủy (2026-11-11)

Thay suất ải 50 đảo Thủy (Thương Lam, epic). Con gốc tham khảo: `monster_3247` (Sword x Staff) là **dạng 2** của dòng.
Gói prompt: `ArtGen/Spine/build_tm08.py` → `gui_gpt/tm08_2/`, `gui_gpt/tm08_1/`; ảnh về `inbox/tm08_<k>/tai_ve/`.

## 1. Mổ con gốc (chỉ lấy cấu trúc và nhịp; hình, màu, diễn xuất là của mình)

Nguồn: `D:\RefAnimation\SwordxStaff\scan\monster_3247\info.json, keys.json` (đọc bằng script tóm tắt + `mo_xe/nhip.py`), atlas
`monster_3247.png` 104 × 1172 (tỉ lệ 0,75), `.skel` 0,1 MB.

**Dáng:** rắn rồng con thân cuộn chữ S dựng đứng, đầu tròn to (chibi), hai vây tai hồng kem lớn, bụng hồng kem, vân xoắn sẫm,
mắt hồng to, đuôi cuộn ra sau kết bằng vây "ngọn lửa". Nhìn sang trái (ta lật khi làm).

**41 xương:**

| Nhóm | Xương | Để làm gì |
|---|---|---|
| gốc | `root → bone → bone30 → A1 → bone2` | `bone30` xoay cả con (hit_02 lật 360°), `A1` là đích IK + gốc thân, `bone2` dời thân (lao trong skill) |
| thân + đầu | `bone3 → bone4 → bone5 → bone6 → bone16` (4 đốt dài 77/80/80/26 + đầu 96) | chuỗi thân đứng uốn S; đầu `bone16` `inherit=3` (không theo xoay cha): đầu giữ thăng bằng, cổ uốn |
| mặt | `bone17 → bone18, bone19` (hai mắt), `bone20` (miệng) | mắt dời riêng (nhìn theo), miệng há một xương |
| vây tai | `bone21-23`, `bone24-26` (3 đốt mỗi tai) | tai vẫy trễ pha, biên độ lớn nhất ở ngọn (tới 95°) |
| đuôi | `A2 → bone11..bone15` (5 đốt), IK `A2` trên 2 đốt gốc | quẫy sóng, IK giữ gốc đuôi bám đất |
| đuôi bản sao | `bone38 → bone32..36` (5 đốt), `inherit` 3/4 | bộ mảnh đuôi thứ hai (`weiba03/04`, `huoyan2`, mặc định ẩn) bật khi con lật hoặc đổi tư thế |
| vòng thân | `bone7` (IK `A1`), `bone8, bone9, bone10, bone27(+bone28)` trên **path** `B1` 9 đỉnh | khúc thân cuộn dưới (`shenti03`) chạy dọc đường cong: phồng chạy quanh vòng |
| khác | `bone37`, `bone29` (điều khiển lưới), `shadow` | |

**22 slot, 13 lưới + 4 mảnh mắt + path + bóng** (sau → trước): bóng; đuôi `weiba02` (158×91, 6 xương), `weiba01` (96×72), vây đuôi
`huoyan` (90×128, 4 xương); thân `shenti03` (vòng cuộn, 5 xương, path), `shenti02`, `shenti01` (3–4 xương); cổ `bozi` (3 xương); miệng
`mouth` (1 xương); mí `yanpi`; mắt 4 mảnh (`yanjing01-04`, mỗi mắt hai hình: mở / `shouji` nhắm-bị đánh); mặt `face`; hai tai (3 xương).
Tổng 408 đỉnh. Mọi lưới thân chia trọng số 3–6 xương, tối đa 4 xương mỗi đỉnh. Mắt và mặt là lưới 4 đỉnh bám cứng đầu.

**9 clip:** `idle_01` 4,0 s; `hit_01` 0,5; `hit_02` 0,67 (lật 360°); `skill_01` 0,93; `block_01` 0,5; `die_01` 1,0; `floating_01` 1,5
(bị hất bay: `A2` dời y 340); `run_01` 0,53; `stun_01` 1,33.

**Nhịp idle (120 khung, 94% bezier):** hai nửa 0–60 và 60–120 gần như trùng; khoá dồn ở khung 0 / 40 / 80 / 120 (dáng chính) và
55–70 (điểm phá nhịp: đầu ngẩng `bone16` +23,8° ở khung 70, thân `bone5` −16,5°). Thân chỉ lắc 10–19°, **đầu 33°** nhưng lệch pha thân.
Đuôi: biên độ tăng dần ra ngọn **13° → 33° → 48° → 68° → 102°**, mỗi đốt đạt cực trị trễ đốt trước 3–7 khung (sóng chạy từ gốc ra
ngọn), 2–3 khoá mỗi đốt mỗi nửa vòng. Tai 10 khoá/4 s, ngọn tới ±50°.

**Nhịp skill (28 khung, 89% thẳng, dáng → dáng cùng khung 0/6/13/14/15/17/22/28):** 0 → 6 lấy đà (thân `bone5` −50°, đầu cúi), 13 cuộn
chặt (bone3 +44°), **14 → 15 bung trong 1 khung** (bone3 44 → −48°, bone5 −78 → +28°, đầu 82° → 2°), `bone2` dời tới 40 đơn vị ở khung
17, giữ có trôi tới 22, về khung 28 bằng khoá bậc. Đúng công thức "khung gãy → chạm 1 khung → giữ có trôi" của `skill-petclash` 7.2.

**Hit_01 (15 khung):** khung 0 đã là dáng bị đánh (`bone16` −88°, cổ 42°), về trong 0,5 s; mắt đổi sang hình `shouji`.

Lấy gì: chuỗi thân đứng 4–5 đốt + đầu không theo xoay cha; đuôi 5 đốt biên độ tăng ra ngọn, trễ pha; mắt đổi hình; miệng một xương;
"lật cả con" (hit_02) **không lấy** (luật dự án: không lộn). Path/IK thay bằng giải cổ và nướng như Hải Long.

## 2. Thiết kế dòng Uyên Xà

**Tên đề xuất:** dòng **Uyên Xà** (淵蛇, rắn vực sâu). Dạng 1 **Uyên Nhi**, dạng 2 **Uyên Xà**. Tên khác để chọn: Thâm Xà / Mặc Giao /
Hắc Triều (dạng 2), Xà Nhi / Lươn Nhí (dạng 1).

**Lore:** rắn rồng sống ở rãnh sâu nhất đảo Thủy, nơi không có ánh sáng; dọc sườn có hàng chấm đèn lồng và hai râu cằm đầu hạt đèn
để dụ mồi trong bóng tối. Bé Uyên Nhi theo thuỷ triều trôi lên vùng nước nông, lớn lên thành Uyên Xà canh giữ vực. Chiêu lấy từ
Pokémon nước: Water Gun → Hydro Pump; Bubble/Rain → Whirlpool (maelstrom); đòn thường mổ rắn / quật đuôi.

**Khác con gốc ở đâu:** con gốc là mầm chibi mắt hồng, tai vây hồng kem lớn, bụng hồng, thân xanh ngọc vân xoắn, đuôi vây lửa, cuộn
chữ S đứng gọn. Dòng này: màu chàm vực sâu + bạc hà (không xanh ngọc, không hồng); **không tai vây** (thay bằng ba gai xương gáy +
vây lưng liền kiểu cá mái chèo); đuôi mái chèo hai thuỳ (không ngọn lửa); đầu dạng 2 dài hẹp hàm trề kiểu lươn moray; râu cằm đèn
lồng; thân nằm S hở dài ngang (không cuộn ball dựng). Chỉ giữ chủ đề "rắn rồng nước thân dài".

**Khác ba rồng đảo Thủy:** Thủy Long (rồng người cobalt + ngọc lam + giáp vàng), Thương Lam (rồng bốn chân có cánh, băng lam trắng),
Hải Long Ngũ Đầu (xanh ngọc, bờm đỏ san hô, gạc vàng, năm cổ trên sóng). Uyên Xà: một thân rắn không chân không cánh, chàm đậm + bạc
hà, vây lưng liền, đèn lồng. Không trùng bảng màu 13 tướng Thủy hiện có (cáo aqua, cánh cụt xám ngọc, Mi Nhi tím lam nhạt, Ma Kết lục
biển, cá mập cobalt, cua cam, Huyền Vũ lục ngọc, Lam Quân lam + bờm kem).

**Bảng màu:**

| Vùng | Dạng 1 Uyên Nhi | Dạng 2 Uyên Xà |
|---|---|---|
| thân | chàm xám `#5058A8` | chàm vực sâu `#2E2F6E` |
| bụng (tấm) | bạc hà trăng `#D8F3EA` | như dạng 1 |
| vây (mào, lưng, đuôi, ngực) | bạc hà bọt biển `#8FE3D0` | như dạng 1, vân tia mực |
| chấm đèn sườn | 3 chấm `#8FE3D0` | ~12 chấm nhỏ dần về đuôi |
| gai xương gáy, răng | 1 mấu `#F3EBD9` | 3 gai `#F3EBD9` |
| mắt | hổ phách `#F2B544`, đồng tử tròn | hổ phách, đồng tử dọc |
| lòng miệng / lưỡi | mận `#5A2A5E` / `#C56A9A` | như dạng 1 |
| hạt đèn đầu râu | `#C9F7EA` | `#C9F7EA` |
| mực | `#2B2118` | `#2B2118` |

**Dạng 1 Uyên Nhi (chibi, ải 50 lúc mới nhận):** đầu ~45% chiều cao, mắt to tròn hổ phách, mày nhíu, hàm dưới trề nhỏ lộ một răng;
mào vây bạc hà mềm to úp về sau như mào gà, nối thành vây lưng thấp; thân ngắn mập, ba chấm đèn; ngồi trên một vòng đuôi hở hình C, vây
đuôi nhỏ chìa sang trái; hai râu cằm ngắn đầu hạt đèn; hai vây ngực tí hon. Nhìn phải.

**Dạng 2 Uyên Xà (trưởng thành, chiến):** thân ống dài thon dần, S hở nằm ngang: đuôi trái, bướu giữa, phần trước dựng đứng, đầu trên
cao bên phải; vây lưng liền từ gáy tới đuôi cao bằng một bề dày thân, mép lượn sóng; đuôi mái chèo hai thuỳ; đầu dài hẹp, mõm hơi
quặp, hàm dưới trề, mày nặng, mắt hổ phách đồng tử dọc, miệng hé lộ hai nanh và lòng miệng mận; ba gai xương gáy; hai râu cằm dài
buông xuống sau, đầu hạt đèn; một đôi vây ngực nhỏ. Không tai, không gạc, không bờm, không chân, không cánh.

Dạng 2 khác hẳn dạng 1 theo luật mục 3 đặc tả: màu đậm hơn, đổi bóng dáng (ball chibi dựng → dải S ngang dài), đầu dài hẹp thay đầu
tròn, mào mềm thành vây lưng liền + gai xương, râu dài; vẫn nhận ra: bạc hà + chàm, tấm bụng, chấm đèn, râu đèn lồng, hàm trề.

## 3. Đòn / chiêu từng dạng (rig chỉ diễn thân; tia, đạn, xoáy là VFX trên sân)

| | Dạng 1 Uyên Nhi | Dạng 2 Uyên Xà |
|---|---|---|
| `attack` | **Mổ** (kiểu `bite`, đứng tại chỗ): cuộn lấy đà 0,3 s, đầu phóng tới trong 1 khung (cổ duỗi), giữ có trôi, về; sự kiện `trung` | **Quật đuôi sóng** (kiểu `tailwhip` tại chỗ, không lộn): thân vặn, đuôi mái chèo đập xuống đất phía trước → VFX sóng đất `flyw` chạy tới đối thủ; sự kiện `trung` lúc đuôi chạm |
| `cast` (mana) | **Thủy Thương** (Water Gun, `beam` nhỏ): ngửa tụ 0,45 s, há miệng, tia nước mảnh; `phun` / `het_phun`; xương `mieng` | **Thủy Pháo** (Hydro Pump, `beam` lớn): dựng cao hơn, nén thân, há to 60°, tia dày, giật lùi cả thân, giữ 1,0 s |
| `skill` (cuối) | **Mưa Bọt** (Bubble Beam → `rain`): cuộn chặt, ngẩng, phun chùm bong bóng lên trời, bong bóng rơi quanh đối thủ 3 nhịp | **Thâm Uyên Xoáy** (Whirlpool/Maelstrom → `vortex` cỡ 3): hạt đèn râu sáng màu (đổi hình), thân dựng cao xoắn hai vòng, gầm `gam`, xoáy nước dưới chân đối thủ quay nhanh dần, cột xoáy, nổ cuối; khựng 0,2 s, rung, chớp màn |
| `hit` | sóng từ đầu về đuôi, mắt nhắm (mí), 0,6 s | như dạng 1, biên độ nhỏ hơn (nặng hơn) |
| `die` | giật, nhắm mắt, lả đầu giữ một nhịp, rũ xuống vòng đuôi, tan | giật, nhắm, ngửa đầu lè lưỡi, thân duỗi đổ từng khúc từ đuôi lên, tan |
| `appear` | từ dưới trồi lên (mặt nạ cắt ngang đất), lắc tắt dần | từ dưới trồi lên theo S, đầu lên sau cùng, gầm nhẹ |
| `evolve` | lốc nước, đổi dạng lúc đậm nhất, khung cuối = idle dạng 2 | (dạng cuối, không có) |
| `aura` (tuỳ) | hạt đèn râu nhấp nhô | vòng nước cạn dưới thân 4–6 gợn, hạt đèn đung đưa |

Idle: thân sóng chạy đầu → đuôi (đốt trễ 0,17 s, hai đốt kề ngược dấu, đầu bù 80% góc cổ), 2 khoá mỗi đốt mỗi vòng; điểm phá nhịp: dạng
1 chớp mắt + táp miệng 0,45 s, dạng 2 chớp + râu đèn giật; idle 4,0 s (2 vòng sóng), như con gốc.

## 4. Dự kiến pha 2 (chờ duyệt concept)

**Tờ mảnh (GPT, mỗi tờ 1536 × 1024, nền trắng, cách nhau ≥ 60 px), dạng 2:**
- M01 đầu: sọ + hàm trên (gai gáy liền), hàm dưới rời có lòng miệng, mảng lòng miệng, lưỡi duỗi thẳng, mí nhắm, 1 râu duỗi thẳng + hạt đèn, 1 vây ngực.
- M02 thân: **ống thân duỗi thẳng nằm ngang** ~1400 × 200 có vây lưng dọc mép trên, tấm bụng mép dưới, hàng chấm sườn, thon về phải; mảnh đuôi mái chèo rời.
- M03 (tuỳ) nước cạn: 2–3 gợn nhỏ, vòng sóng dẹt (nếu quyết có `aura` nước).
Dạng 1: M01 đầu (sọ, hàm, lòng miệng, mào mềm rời, mí, râu ngắn, vây ngực), M02 thân cong C ngắn duỗi thẳng + đuôi nhỏ.

**Xương dạng 2 (ước ~60):** `root → move → base`; chuỗi thân 14 đốt từ gốc giữa thân ra hai phía (nửa trước 7 → gáy, nửa sau 7 → đuôi;
giải Bezier như cổ Hải Long để đầu dẫn); `head` (không theo xoay cha, bù 80%), `jaw`, `eye`, `mieng` (trục x hướng nhả); vây lưng
nằm trong lưới ống (hàng đỉnh trên lệch pha nhẹ); đuôi mái chèo 2 đốt; 2 vây ngực × 2 đốt; 2 râu × 5 đốt (`rope`, hạt đèn cứng ở ngọn);
lưỡi 4 đốt (chỉ clip chết); mí (slot ẩn `fade`); `shadow`. Dạng 1 ~40 xương (thân 8 đốt, mào 3 đốt lò xo).

**Lưới:** ống thân dải B-spline (mỗi đốt 2 cột, 5 hàng: mép vây, lưng, giữa, bụng, mép bụng), đỉnh cách đều ~24 px rig, không cột nào
bám 100% một đốt; hàm dưới lưới hai xương; lòng miệng 5×3 theo hàm. Đích `.atomik` ≤ 0,3 MB (atlas 256 màu, RDP).

## 5. Lịch sử gen

- 2026-11-11 01:20 dạng 2 lần 1 → `inbox/tm08_2/tai_ve/L1_concept.png` (84 s). Đạt: chàm + bạc hà, vây lưng liền, đuôi mái chèo,
  râu đèn, ba gai gáy, miệng hé thấy lòng miệng mận + nanh, nhìn phải, S hở không vắt chéo, tô phẳng không bóng, nền trắng. Chưa ưng:
  đầu hơi nhỏ so với thân (gần 1/7), vây lưng mỏng ở đoạn gáy. **Chọn làm `L1_duyet.png`** (chép), dựng dạng 1 theo bản này.
- dạng 2 lần 2 (`--note`: đầu to hơn ~1/5, hàm khoẻ, miệng há rộng hơn, vây lưng liền tới sọ) → `L1_concept_2.png` (491 s, đợi khoá
  lâu). Miệng há rõ hơn, nanh đẹp, vây lưng liền tới sọ; nhưng đầu vẫn nhỏ như cũ, thân ngả tím (#4A2E8A, lệch bảng màu chàm), vân sáp
  mờ hơn, trông số hơn. **Giữ lần 1 làm `L1_duyet.png`**; lần 2 là bản khác để người dùng chọn. Cỡ đầu sẽ chỉnh ở pha 2 (tờ mảnh vẽ
  đầu rời theo cỡ dặn, lắp vào rig), không gen lần 3.
- dạng 1 lần 1 → `inbox/tm08_1/tai_ve/L1_concept.png` (93 s, đính L1_duyet dạng 2). Đạt: chibi đầu ~45%, chàm xám nhạt hơn
  dạng 2, mào bạc hà mềm úp sau, ba chấm, râu đèn ngắn, hàm trề một răng, mấu xương gáy, mắt hổ phách cau mày, nhìn phải, không bóng,
  nhận ra cùng dòng. Chưa ưng: vòng đuôi khép dưới thân (thân đè lên đuôi), không phải chữ C hở.
- dạng 1 lần 2 (`--note`: đuôi chữ C hở nằm bên trái, không gì đè lên đuôi) → `L1_concept_2.png` (180 s). Đuôi hở, không bộ phận nào
  chồng nhau, hai vây ngực rõ, mào to; dáng hơi giống cá ngựa nhưng vẫn là bé rắn cùng dòng. **Chọn làm `L1_duyet.png`** (dễ tách mảnh).

## 6. Pha 2 đã làm (2026-11-11, concept đã duyệt; đầu dạng 2 phóng 1,3 lần ở rig, không aura nước)

Tệp: `ArtGen/Spine/tm08.py` (`cat k | place k | rig k | all`, chạy bằng `D:/spine-venv/Scripts/python -I` qua `quai/khoa.py nang`), tờ mảnh
`gui_gpt/tm08_<k>/luot_2_manh.txt` (M01 đầu + hàm + lòng miệng + lưỡi + mí + vây ngực + râu + vây đuôi [+ mào dạng 1]; M02 ống thân duỗi
thẳng), mảnh cắt `inbox/tm08_<k>/manh/`, kết quả `inbox/tm08_<k>/rig/` (json/atlas/png Spine 4.2, `.atomik`, `_game.json`, `xem.html`,
`khung_<clip>.png`, `luoi.png`, `so_concept.png`, `so_ghep.png`, ảnh cận, `chan_dung.png`, `so_sanh.md`, `bao_cao.json`, `uon_thu.png`).

Cách dựng thân: đường giữa đọc tay trên concept (x, y, dày ước) nối mượt; bề dày từng đoạn đo bằng đoạn mặt nạ thân cắt pháp tuyến
(chặn ±30 % quanh ước; dạng 1 bụng tròn nên dùng ước); ống GPT được **nắn theo bề dày và chiều dài concept** (`nan_ong`: ống co giãn theo
cột, vây lưng cao theo cùng tỉ lệ) rồi uốn thành chữ S bằng toạ độ thế giới từng đỉnh của dải lưới; chuỗi xương hai phía từ `than` (chỗ
chạm đất): `fw*` lên gáy (đầu dẫn, đầu bù 80 % góc cổ), `bk*` ra đuôi; trọng số B-spline. Đầu: dò khớp tự động (SQDIFF Lab + nét mực) rồi
phóng `hk` quanh gáy; hàm neo bản lề trên ảnh đầu; lòng miệng 5×3 theo hàm; mí `fit_lid` (còn hở 0 px cả hai dạng); lưỡi 4 đốt dây
mềm (chỉ clip chết); râu 2 × 5 đốt (dạng 1: 3) dây mềm có gió; vây ngực 2 × 2 đốt lò xo; vây đuôi 2 đốt; mào dạng 1 3 đốt lò xo; mặt nạ
cắt ở y = −30 cho appear (trồi) và die (chìm).

Đã thử và bỏ: dò đường giữa tự động theo mặt nạ (lạc sang vây ngực, đầu, bụng mập); dò khớp hàm / vây đuôi / mào bằng SQDIFF (thiên về
mẫu nhỏ, hàm chui vào đầu) → đặt theo điểm neo đọc trên concept; phân loại chàm phải loại nét sáp bạc hà sẫm (b ≥ g), không thì cả vây
lưng bị tính là ống và ép dẹt.

Số đo: xem `so_sanh.md` từng dạng (dạng 2: 42 xương, 12 slot, 4201 đỉnh, 7433 tam giác, 5571 khoá, .atomik 344 KB, IoU concept 0,75 /
bỏ đầu 0,80; dạng 1 gộp dạng 2: 77 xương, 25 slot, 7474 đỉnh, .atomik 664 KB, IoU 0,75 / bỏ đầu 0,59). Còn lại: dạng 1 bụng tròn
chibi khớp concept kém (ống thẳng nắn không ra bụng tròn, mào đặt tay); dải thân hở 92–252 px ở hai chỏm tròn (lưới dải của thư viện
không phủ mũ tròn); dung lượng dạng 1 gộp vượt trần vì mang cả atlas dạng 2.

## 7. Sửa theo soi của Claude điều phối (2026-11-11, lần 2)

- **Vây lưng dạng 2 là mảnh riêng** (`gui_gpt/tm08_2/luot_3_vay_lung.txt` → `tai_ve/M03.png` → `manh/vay_lung.png`): dải gợn có tia vẽ
  thẳng, mép gốc là đáy; dải lưới trục ở mép gốc (`luoi_dai`, `mu=True`), bám 14 xương vây `vl0..13` (con của từng đốt thân) bằng
  B-spline; gốc chồng 18 px vào ống, vẽ sau ống. Idle: xương vây xoay ±2,4–3° lệch pha 0,62 rad mỗi đốt → gợn chạy dọc vây. Ống thân nắn
  bỏ phần vây (`bo_vay`). Chiều cao vây tự co ở đoạn cong về phía lưng (giới hạn 0,85 R, lọc cực tiểu ±40 px rồi trung bình ±30 px dọc
  thân cho co dần), có khâu chống bow-tie.
- **Vệt trắng chéo ở cổ uốn**: do dải thân tự gập ở đáy chữ U (bán kính cong < nửa bề dày). Sửa gốc: `duong_giua` làm mượt thêm cục bộ
  tới khi R ≥ 1,5 × nửa dày (dạng 2 thêm 124–177 lần ở đáy U, đường lệch concept vài chục px, IoU 0,757 → 0,741); không còn nén ống.
  Chỗ cong gắt còn một khe hình V giữa hai lá vây lưng (vây co về sát gốc), nền lộ ở đó như concept vẽ vây nhỏ lại; không phải lỗ lưới.
- **Thân dạng 1 vẽ đúng dáng** (`luot_3_than_cong.txt` → `M03.png` → `manh/than_cong.png`, dò khớp SQDIFF tỉ lệ 0,737): lưới vùng
  `luoi_vung` (1515 đỉnh, hở 0, 0,1 % dưới 25°), trọng số `chuoi_chieu` lên đường khớp 8 đốt; không nắn ống nữa. Hết chấm trắng quanh
  vây sau lưng (chúng là dải ống cũ hở ở viền bụng cong).
- **Hở 0 ở mọi mảnh**: dải thân và dải vây dùng `luoi_dai(mu=True, buoc_theo_cao=H)` của thư viện (mũ tròn hai chỏm).
- **Dung lượng dạng 1 gộp**: `TI_K[1] = 0,58` (rig dạng 1 và bản dạng 2 nhúng trong rig gộp đều ở 0,58), lọc khoá xoay 0,3° / dời 0,7
  → `.atomik` 493 KB (< trần 0,5; mật độ lưới giữ theo chiều cao: 6946 đỉnh / 522 px rig).
- Mào dạng 1 và vây đuôi hai dạng vẫn đặt theo điểm đọc trên concept (dò tự động lạc); thử 5 vị trí mào, giữ (1015, 435, 12°, 1,2).
- IoU cuối: dạng 2 0,741 (bỏ đầu 0,779; đích 0,85), dạng 1 0,820 (bỏ đầu 0,704; đích 0,80): chưa đạt đích, phần lệch còn lại là vây
  lưng gợn khác hình vây concept, đáy chữ U được bo tròn, mào dạng 1 lệch trên-trái, vây ngực xa.
- Chrome runtime Spine: 3 lần qua `khoa.py chrome` đều không trả JSON (trang không kết thúc, không LOI); ghi nhận, chưa sửa.

## 8. Cách lai (Claude điều phối chốt 2026-11-11, sau soi vòng 2): `tm08_lai.py`

- `cat k`: cắt thẳng từ concept các lớp thân, vây lưng gợn (dạng 2), vây đuôi, vây ngực gần (dạng 1: cả hai vây sườn), mào (dạng 1),
  đầu trên. Vùng loang từ hạt giống (`SEEDS`), tường = nét mực dày (dt ≥ 2,2 px; tia vây mảnh không chặn), **ràng buộc màu**: vùng vây
  chỉ loang vào pixel bạc hà + mực, vùng thân chỉ vào pixel không bạc hà (không thì thân tràn vào vây qua tia mảnh và ngược lại; dạng 1
  thêm vùng `vay_than` cho vây lưng thấp liền thân rồi nhập vào thân); phần còn lại nhãn gần nhất. Lớp mọc thêm (`GROW`): vây lưng
  36 px dưới thân, thân 45 px dưới đầu/hàm/vây ngực, mào 40 px dưới đầu, vây đuôi 20–22 px vào thân; tô trung vị màu vùng + nét mực mép.
  Hàm dưới và râu của concept bỏ (`bo_*`), thay bằng mảnh GPT. Ra `inbox/tm08_<k>/manh_lai/` (+ `lop.json`, `nhan.png`).
- Đường tâm thân: Dijkstra trên mặt nạ thân (+đầu) lưới thu 3 px, giá bước = dài × (1 + 60/(dt+2)) (ưu tiên giữa thân), từ gáy
  (`DAC.nape`, trong đầu một chút) tới chóp đuôi; làm mượt 12 lần. Bề dày = 2·dt tại điểm đường tâm.
- `dung_lai(k, ti)`: thân, vây lưng, đầu, vây, mào = `luoi_vung(buoc_theo_cao=H)` trên hình cắt, đỉnh đặt đúng toạ độ concept
  (`the_gioi`); trọng số thân `chuoi_chieu` lên đường khớp 14/8 đốt (fw/bk từ `than` chỗ chạm đất); vây lưng bám xương `vl_i` ở mép
  lưng từng khớp (con của đốt thân, gợn idle lệch pha); đầu phóng `HK[2] = 1,3` quanh gáy bằng `Dat(ti=1,3)` (hàm, râu, mieng, mí đi theo);
  hàm GPT neo bản lề `DAC.hinge`, dài theo `DAC.ham_dai`; râu GPT (dải) uốn theo đường râu `DAC.rau` đọc trên concept, co cho bằng
  dài; mí `fit_lid` trên đầu concept (hở 0 cả hai dạng); vây ngực xa GPT nấp sau vây gần (dạng 2). Mọi dao động idle `s0()` bằng 0 ở
  t = 0 nên khung 0 idle = dáng concept.
- Kết quả: dạng 2 IoU 0,873 / bỏ vùng đầu phóng 1,3× 0,925; dạng 1 0,965 / 0,956. Đầu dạng 2 hở 2 px, mào dạng 1 hở 4 px (mép mảnh
  rất mỏng), còn lại 0. `.atomik` dạng 2 404 KB, dạng 1 gộp 485 KB (TI 0,58).
- Bẫy: chạy `tm08.py` là `__main__` nên `tm08_lai` import `tm08` thành bản thứ hai: `T.TI`, `T.B_VIEN` không phải biến của `__main__`
  (so_concept vẫn đúng vì chuẩn hoá theo cỡ concept; mật độ lưới ghi qua `info["buoc"]`). Heredoc Bash nuốt `\n`: vá file bằng Write/Edit.
