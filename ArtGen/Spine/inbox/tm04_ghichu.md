# tm04: ghi chú dòng 4 lô Thủy (con gốc monster_3233 → dòng Hà Bá)

Đặc tả chung: `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`. Gói prompt: `ArtGen/Spine/build_tm04.py` → `gui_gpt/tm04_<k>/`.
Ảnh: `inbox/tm04_<k>/tai_ve/`. Thay suất ải 15 đảo Thủy (Mi Nhi, uncommon).

## 1. Con gốc monster_3233 (chỉ học cấu trúc và nhịp, không lấy hình)

Đọc từ `D:\RefAnimation\SwordxStaff\scan\monster_3233\info.json, mesh.json, keys.json` và atlas.

**Hình:** thú tròn như một cái miệng biết đi: nửa trên (đầu + lưng xanh lam, mắt to trên đỉnh) và nửa dưới (hàm dưới kem có gờ)
tách nhau bằng khe miệng; hai vây lớn vàng hình lá trên lưng (một xa, một gần), đuôi ngọn lửa xanh ngọc, hai chân ngắn xám (đứng
hai chân), răng tam giác rời. Nhìn sang phải, góc nghiêng.

**Số:** Spine 4.2.28; 45 xương, 30 slot (toàn lưới, không region), 370 đỉnh, 348 tam giác; atlas một trang 220 × 680 (tỉ lệ
xuất 0,75), 32 vùng; 4 IK (hai chân, mỗi chân IK 2 xương + bàn chân), 3 transform constraint (mắt xa và gốc vây gần đi theo xương
vây sau 30% trục Y); không physics, không sự kiện; 12 clip.

**Cắt mảnh (atlas):** `shenti1` nửa trên thân (xanh), `shenti2` hàm dưới/bụng (kem, có gờ), `shenti3`, `shenti4` là **bản vẽ
riêng cho lúc há to** (nửa trên lộ mặt dưới, hàm dưới cong hình lưỡi liềm), `kouqiang` lòng miệng hồng, `yachi1..8` răng rời
(1–3 bộ thường, 4–8 bộ lúc há to), `yanjing1..4` mắt gần (tròng kem + con ngươi) và mắt xa (nhỏ, vẽ sau cùng phía sau), `yuqi1`
vây gần, `yuqi2` vây xa, `weiba1` gốc đuôi, `weiba2` ngọn lửa, `tuiL1..4` / `tuiR1..4` chân xa / gần (đùi, cẳng, bàn, ngón).

**Thứ tự vẽ (sau → trước):** mắt xa → vây xa → chân xa → ngọn đuôi → gốc đuôi → lòng miệng → răng trên → nửa trên thân → mắt gần
→ răng dưới → hàm dưới → vây gần → chân gần.

**Cây xương:** `root → bone34 (gốc thân, có bóng) → bone33 → bone` (tâm thân, mọi cú nhảy, lật). Dưới `bone`: `bone10` (khối
thân, xoay quanh đáy) → `bone11` (nửa trên/đầu, dài 91) → `bone19` (đỉnh đầu, hàm trên); `bone10 → bone18` (hàm dưới) →
`bone37`; đuôi `bone12..17` (6 đốt); vây xa `bone20..22` + `bone23..25` (hai chuỗi 3 đốt), vây gần `bone28..30` + `bone31..32`
(hai chuỗi), mắt `bone26/38/35`, `bone27/39/36`; chân: `bone5→bone2→bone3` + `bone4` (IK `R1`, `R2`), `bone9→bone6→bone7→bone8`
(IK `L1`, `L2`), đích IK `R1/R2/L1/L2` con của `bone34` (bàn chân bám đất).

**Trọng số:** vây, đuôi là dải chia trọng số theo chuỗi (45% đỉnh bám cứng một đốt, phần còn lại hoà hai đốt); nửa trên thân
hoà `bone11` 0,71 / `bone19` 0,29; hàm dưới hoà 4 xương; **lòng miệng chia đôi: nửa trên bám 100% đầu (`bone19`), nửa dưới 100%
hàm (`bone18`)**, thành màng căng giữa hai hàm (khác luật dự án: dự án cho lòng miệng theo hàm dưới, chỉ màng nhỏ ở khoé nối đầu).
Chân, mắt mảnh cứng một xương.

**Clip và nhịp (khoá thật, `mo_xe/nhip.py`):**

| Clip | Dài | Diễn |
|---|---|---|
| `idle_01` | 1,07 s | mỗi xương 2 khoá một vòng, bezier 94%; thân `bone11` −3,3° ↔ −6,6°, hàm dưới dời ±3 đơn vị lệch pha; đuôi, vây lệch khung |
| `skill_01` (đòn) | 1,20 s | thẳng 97%. Ngửa lấy đà 0,07–0,23 s (đầu −15 → −20°), **đớp 1 ở 0,57–0,67 s** (hàm 44 → 67°, đầu +19°, hàm dẹt 0,8 đúng khung), đớp 2 ở 0,77–0,97 s, về 1,2 s. Đổi `shenti1 → shenti3` lúc há |
| `skill_02` (chiêu) | 1,50 s | nhảy lùi lên (dời −200, +115, xoay 60°) 0–0,2 s, giữ tới 0,5 s, **bổ xuống đớp 0,53–0,57 s**, giữ cắn **rung hai dáng đổi mỗi khung** (hàm ±1,5 đơn vị, 2,5°) 0,57–1,03 s, về. Đổi cả bộ mảnh há to (thân, hàm, răng 4–8) + deform |
| `skill_02X` | 1,33 s | như trên, không rung, đáp tại chỗ |
| `generate_01` | 0,80 s | rơi từ trời: co 0,1 → 1 trong 3 khung, cao 392 → 438 → 0 tới 0,53 s, xoay 81° → 0, nảy 23 đơn vị rồi đứng |
| `hit_01` | 0,50 s | khung 0 đã lệch sẵn, **đỉnh ở 0,07 s** (thân ngửa 92°, bật lùi lên 128), hồi về 0,5 s |
| `hit_02` | 0,67 s | trúng nặng |
| `die_01` | 1,00 s | bật lên 225 ở 0,07 s, lơ lửng tới 0,3 s, rơi 0,4–0,5 s, nảy nhỏ, nằm |
| `floating_01`, `stun_01`, `block_01`, `run_01` | 1,5 / 1,33 / 0,5 / 0,53 s | bay, choáng, đỡ, chạy (dự án không cần) |

Học được: miệng là khớp chính của cả con (đòn đớp đôi, chiêu cắn giữ rung); khung đớp có hàm dẹt 0,8 (smear); lúc há to đổi
sang bản vẽ riêng của nửa trên và hàm dưới để không méo; chân IK bám đất; idle chỉ 2 khoá mỗi xương.

## 2. Thiết kế dòng (đề xuất)

**Tên dòng:** Hà Bá (`ha_ba`), danh hiệu "Hà mã nuốt sóng". Dạng 1 **Hà Mã Con**, dạng 2 **Hà Bá**.

**Lore:** hà mã con của dòng sông thiêng, nuốt sóng rồi nhả ra; chóp đuôi giữ một "hồn nước" là con sóng nhỏ biết cuộn. Lớn lên
thành Hà Bá, chúa sông mặc giáp đồng, ngáp một cái là sông dậy sóng.

Giữ từ con gốc làm điểm xuất phát (chủ đề, không lấy hình): thú tròn miệng to, vây trên lưng, đuôi có linh hồn. Khác con gốc:
loài (hà mã, bốn chân, mõm hạt đậu, lỗ mũi, mắt nằm trên đỉnh đầu, ngà), hai mắt thấy cả hai (3/4), ba vây buồm tròn có gai
thay hai lá nhọn vàng, đuôi là con sóng nước thay ngọn lửa, bảng màu xanh xám đá + hồng đào + bạc hà thay xanh lam + kem + vàng,
có đốm bọt; dạng 2 có giáp đồng, ngà dài, thân chàm xám.

**Concept dạng 1:** gen 3 lần (`inbox/tm04_1/tai_ve/`): `L1_concept.png` thân dài kiểu khủng long, chưa chibi, ngả tím;
`L1_concept_2.png` tròn đẹp nhưng 5 bàn chân; **`L1_concept_3.png` chọn** (đúng 4 chân, tròn, xanh xám đá), chép thành
`L1_chon.png`. Phần dặn thêm của lần 2, 3 đã gộp vào `build_tm04.py` (thân tròn, đếm 4 chân, màu không ngả tím).

**Concept dạng 2:** gen 3 lần (`inbox/tm04_2/tai_ve/`): `L1_concept.png` thế lao đẹp nhưng thân ngả tím `#54589D` (dễ trùng
dòng tm03 xanh tím) và chân dồn phía trước; `L1_concept_2.png` đúng màu, đúng bốn chân, nhìn ngang, dễ cắt mảnh nhất nhưng đứng
thẳng ngẩng đầu (chưa ra thế lao); **`L1_concept_3.png` chọn** (thế lao thấp, đầu hạ, thấy hai mắt, há gầm, ngà dài khâu đồng,
màu chàm xám đúng, bốn chân đặt theo góc 3/4 trước: chân trước xa nằm dưới hàm), chép thành `L1_chon.png`. Lỗi nhỏ còn lại: ba
giọt nước rời cạnh đuôi có vệt sáng trắng, lề trên chỉ 30 px; tờ mảnh pha 2 vẽ lại giọt phẳng (đã thêm câu dặn vào prompt).
Vây lưng ra hình mào sóng cuộn có mũ bọt (đẹp, hợp hệ, đổi chi tiết đặc trưng so với vây tròn dạng 1): đã ghi vào prompt.

**Bảng màu dạng 1:** mực `#2B2118`; thân xanh xám đá `#7A93BE`; mõm, cằm, bụng hồng đào nhạt `#F6D5C0`; đốm bọt `#BFD0EA`; vây,
tai vây bạc hà `#86DCC4`, gai vây `#2D8C86`; lòng miệng `#C9506A`, lưỡi `#EE8C9C`; ngà, răng, móng kem `#F8EBD0`; mắt vàng
`#F2C230`; hồn nước ba lam `#2B7FD6`, `#4FB6EE`, `#A6DEF8` + bọt `#F4FCFF`.

**Bảng màu dạng 2:** thân chàm xám đậm `#404C86` (cố ý ngả xám để khác lam tươi của Vây Lam), vằn `#2B3360`, đốm bọt
`#AEB9DE`; mõm, bụng kem cát `#EBD8B2`; vây hình mào sóng xanh két `#1F8A8A`, gai `#165F63`, mũ bọt `#F4FCFF`; giáp đồng `#C28A3E`, gỉ đồng `#4FB3A0`, ngọc kem; ngà ngà voi `#F3E6C8`; mắt hổ phách `#F0A030`; lòng miệng
`#B8405A`, lưỡi `#E27C92`; hồn nước như dạng 1.

So với 13 tướng Thủy đang có (lam trời, xanh két, lam đậm, cam, tím oải hương, xanh bạc hà lục, lam băng, lục rùa) và 9 dòng
khác của lô: chưa ai dùng xanh xám đá + hồng đào; chàm + đồng cũng chưa có.

**Đòn / chiêu (đứng tại chỗ, dạng 2 đổi kiểu):**

| Dạng | attack | cast (`mieng`, `phun`/`het_phun`) | skill |
|---|---|---|---|
| 1 Hà Mã Con | **Ngoạm Nước**: ngửa lấy đà, đớp mạnh tại chỗ; đúng khung đớp, hàm nước (VFX) đớp vào đối thủ (Crunch) | **Súng Nước**: há miệng, nhả ba cục nước nối nhau (Water Gun) | **Ngáp Sóng**: ngáp thật to (há 100°+), một con sóng lăn trên đất từ miệng tới đối thủ (Yawn + Surf nhỏ); sự kiện `gam`, `het_gam` |
| 2 Hà Bá | **Dậm Triều**: chồm hai chân trước lên rồi dậm xuống, sóng xung kích chạy dọc đất tới đối thủ | **Vòi Rồng Nước**: há to giữ 1 s, tia nước dày nén (Hydro Pump), giữ dáng rung hai dáng | **Hà Bá Nuốt Sông**: ngửa gầm, xoáy nước mở dưới chân đối thủ rồi một hàm hà mã bằng nước trồi lên đớp sập (Whirlpool); sự kiện `gam`, `troi`, `het_gam` |

Hiệu ứng (tia, sóng, hàm nước) là lớp VFX của sân, không vẽ trong rig; rig chỉ có xương `mieng` và sự kiện.

## 3. Dự kiến pha 2 (viết lúc pha 1; pha 2 thực tế ở mục 4, đổi sang cách lai)

**Tờ mảnh mỗi dạng** (vẽ đủ phần bị che):
- A: đầu trên (sọ + mõm trên + răng trên, không hàm dưới), hàm dưới rời có nanh/ngà và lòng miệng, mảng lòng miệng, lưỡi, mắt
  mở (tròng + mày) và mí nhắm cho từng mắt, hai tai vây; dạng 2 thêm tấm giáp trán, vòng cổ.
- B: thân (bụng + lưng, vẽ đủ chỗ chân che), bốn chân (gần trước, gần sau, xa trước, xa sau; mỗi chân liền đùi tới bàn, khớp
  tròn), đuôi ngắn; dạng 2 thêm giáp vai.
- C: ba vây buồm rời (dạng 2: bốn vây mào sóng), hồn nước ở đuôi vẽ duỗi (để uốn bằng chuỗi xương; dạng 2 hai mào, tách hai
  mảnh để lệch pha), hai ba giọt nước rời phẳng cho `aura`.
- Dạng 1 chân rất ngắn, chân xa lộ ít: tờ B vẽ chân dài hơn chỗ lộ một chút (phần trên khuất dưới bụng) để bước, nhún không hở.
- Dạng 2 nhìn 3/4 trước: đầu và hàm đè lên chân trước xa; chân trước xa vẽ trọn, đặt sau hàm. Dáng khá rộng (rộng/cao ≈ 1,48
  tính cả đuôi sóng): cần `max_w` hoặc khai chiều cao lớn hơn để không lòi khỏi sân.

**Xương (khoảng 50–60 mỗi dạng):** `root → move → base (nén giãn) → body` (2 đốt hông, ngực) → `head` (hàm trên) → `jaw` (hàm
dưới, khớp ở góc hàm) + `mieng` (trục x chĩa phải) + `tongue` 3 đốt; mắt 2 × (mắt + mí); tai vây 2 × 2 đốt; mỗi vây buồm chuỗi 3
đốt (lò xo); đuôi 3 đốt + hồn nước chuỗi 5 đốt (lò xo, mào tự cuộn như sóng Hải Long, clip `aura` lặp liền); 4 chân × 2 đốt + bàn
chân bám đất (IK); `shadow`. Dạng 2 thêm giáp cứng trên `head`/`body`/vai.

**Lưới:** thân là lưới dày gần đều (đích theo README `quai/`), trọng số hoà theo khoảng cách trong hình; vây, đuôi, hồn nước là
dải B-spline; lòng miệng theo hàm dưới (hàng dưới 100% hàm, màng khoé miệng nối đầu); đồ cứng (ngà, giáp) bám 100%.

**Clip:** `appear` (rơi bịch từ trên xuống, dẹt nảy, lắc nước khỏi người, về idle), `idle` 2,0 s (thở 3%, vây lệch pha, tai
giật, chớp mắt, nhai/táp ở 62–72%), `attack` 0,9 s (đớp ở 0,45 s, hàm dẹt 0,8 đúng khung như con gốc), `cast` 1,0 s, `skill`
1,8 s (dạng 2 dài hơn, rung hai dáng lúc giữ), `hit` 0,6 s (đỉnh 0,07 s), `die` (giật, nhắm mắt, lả, lăn ngửa bốn chân, tan),
`evolve` 2,8 s (dạng 1), `aura` (hồn nước cuộn + giọt).

## 4. Pha 2 đã làm (2026-11-11, concept đã duyệt, cách lai)

**Cách dựng:** thân, đầu trên, tai, vây, đuôi sóng, chân gần, giáp vai, hàm dưới, lòng miệng, giọt nước **cắt thẳng từ concept**
(`tm04_cat.py`, cv2 qua `D:/spine-venv/Scripts/python -I`): vùng loang từ hạt giống kẻ tay, nét mực nâu là tường, nhãn gần nhất,
giới hạn đa giác (vây trên đường lưng, giáp không lấy da chàm, lòng miệng chỉ giữ màu thịt hồng), giọt nước lấy cả cụm liền.
Mỗi lớp mọc thêm dưới lớp trên (vẽ bù TELEA trên ảnh đã thay nét mực bằng màu chính + lát vân sáp thật), thân chỉ mọc trong bao
lồi thân và không mọc vào khoảng miệng, lòng miệng chỉ mọc giữa hai hàm, lớp sau lấy luôn nét viền chung. Tờ GPT M01 (mỗi dạng
một tờ) chỉ dùng mí mắt (nhuộm về màu da quanh mắt); mảng lòng miệng, hai chân xa của tờ chưa cần (chân xa cắt từ concept + vẽ bù).

**Rig** (`tm04.py`, thư viện `quai`): xương root → move → than → hông, ngực → cổ → đầu → mõm, hàm (bản lề ở má), `mieng` (VFX);
tai 2 × 2 đốt, vây 3 hoặc 4 chuỗi (3–4 đốt, lò xo), đuôi sóng 5 đốt (trọng số theo khoảng cách đi trong lưới, cuộn trong clip
`aura`), 4 chân × 2 đốt IK bám đất (dậm, chồm: chân theo thân như cột rồi vung quanh vai, không gập gối), giáp vai cứng, giọt nước
bay trong `aura`. Thân một lưới, trọng số vùng hoà theo khoảng cách đi trong lưới (đầu, cổ, ngực, hông, thân; nửa trước mõm hoà
xương mõm). Lòng miệng: phần dưới theo hàm, mép trên nấp sau đầu. Lưới theo chiều cao (bước 1,5% / 2% H), hở 0 mọi lớp.

**Kết quả:** dạng 2 `inbox/tm04_2/rig/tm04_2.atomik` 290 KB (ĐẠT), 44 xương, 4234 đỉnh, IoU khung 0 / concept 0,968; dạng 1
`inbox/tm04_1/rig/tm04_1.atomik` 377 KB (gộp dạng 2 cho tiến hóa, dưới trần 0,5 MB), riêng dạng 1 3433 đỉnh, IoU 0,983. Mọi clip
nối về khung 0 idle 0,00 px (đo trên đỉnh lưới mọi slot), die khung cuối trống, evolve khung cuối trùng idle dạng 2 0,00 px.
Runtime Spine thật (mo_xe qua khoá chrome) dựng đúng như bộ vẽ Python: `rig/spine_that/`.

**Lệnh:** `D:/spine-venv/Scripts/python -I ArtGen/Spine/tm04_cat.py <k>` (cắt lớp) rồi
`py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm04.py` (dựng dạng 2, dạng 1 + tiến hóa, xuất);
soi khung lớn `py -3 -I ArtGen/Spine/tm04.py show <k> <clip> t1,t2 [tỉ lệ]`.
