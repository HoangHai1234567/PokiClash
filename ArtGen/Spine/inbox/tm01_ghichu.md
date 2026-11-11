# Dòng tm01: ghi chú pha 1 (2026-11-11)

Lô 10 tướng mới đảo Thủy, dòng 1: thay suất ải 1 (Thủy Long, uncommon), **tướng khởi đầu hệ Thủy**. Đặc tả chung:
`ArtGen/Spine/quai/DAC_TA_LO_THUY.md`. Gói prompt: `ArtGen/Spine/build_tm01.py` → `gui_gpt/tm01_<k>/`.

## 1. Con gốc monster_3211 (chỉ học cấu trúc, nhịp; không lấy hình)

Giọt nước xanh mập nhìn thẳng, không chân tay, mắt trắng cau có, hai vây nhỏ hai bên, chóp nhọn trên đỉnh, tô bóng kiểu thạch.
Spine 4.2.28, 0,1 MB; atlas một trang 376 × 308 (xuất tỉ lệ 0,75).

**Mảnh (7 vùng ảnh):** thân `F_SM_shenti1` (254 × 244, gồm cả mặt, chóp), hai vây `shenti2/3` (59 × 54), bốn bộ nét mặt
`P_SM_bq01..04` là ảnh chữ nhật thay nhau trên một slot (bq01 mắt cau có, bq02 mắt nhắm `> <`, bq03 mắt `^ v`, bq04 mắt xoáy
chóng mặt), kèm giọt mồ hôi / nước mắt vẽ chung trong ảnh nét mặt. Mặt là hình dán lên thân, không có hàm, không có lòng miệng.

**Xương (15):**
```
root
├─ bone (y −50)  → bone2 (gốc nén giãn cả con) → bone8 (trục lắc ở đáy, dài 43)
│                    → bone3 (tâm thân y +107: nén giãn, dời thân) ─┬─ bone7 (nét mặt)
│                                                                   ├─ bone14, bone15 (hai vây)
│                                                                   └─ bone4 → bone4b (chóp 2 đốt)
│   └─ bone5 → bone6 → bone16, bone17 (bản sao hai vây để văng ra lúc chết / bị hất)
└─ shadow
```
**Lưới:** 5 lưới, 65 đỉnh. Thân 26 đỉnh 27 tam giác, bám 4 xương (bone2, bone3, bone4, bone4b), tối đa 3 xương một đỉnh; vây 8–12
đỉnh bám cứng một xương. Không IK, không physics, không sự kiện.

**Clip (10):**

| Clip | Dài | Diễn |
|---|---|---|
| idle_01 | 1,33 s (40 khung) | thân nén giãn (0,9; 1,1) ở khung 10 ↔ (1,1; 0,9) khung 30; lắc đáy ±5°; chóp 2 đốt lệch 5 khung (đốt 1 đỉnh ở khung 5/25, đốt 2 ở 10/30, biên độ 32°); vây ±20° |
| skill_01 | 1,0 s | đòn thường: thân nhảy lên lùi (khung 10, co 0,6), vây quay 278° lấy đà, khung 12→13 lao xuống chạm, giữ rung nhẹ khung 13–21 (thân dời ±15 mỗi khung), về khung 30. 92% nội suy thẳng |
| skill_02 | 1,17 s | chiêu: phồng hai lần (tỉ lệ 1,6 ở khung 10 và 20), bật cao 108 (khung 23), **khung 27 dẹp kéo (0,4; 3,1)** = smear, khung 28 chạm đất (1,5), nhún về |
| hit_01 | 0,5 s | khung 0 đã là dáng bị đánh (co x 0,6, nghiêng −31°), mắt `> <` tới 0,33 s, không lấy đà |
| hit_02 | 0,67 s | bị hất: cả con bay lên 209, vây đổi sang bản sao bay ra rồi trở về |
| die_01 | 1,0 s | hất lên, vây văng (bản sao bay 300–650 đơn vị, mờ dần 0,83→1), thân **dẹp thành vũng** (0,4; 0,2) ở khung cuối |
| block_01 | 0,5 s | co lại (0,65), vây khép che |
| floating_01 | 1,5 s | bay lên 176, lơ lửng |
| run_01 | 0,57 s | nảy lò cò |
| stun_01 | 1,33 s | lắc lư ±17°, mắt xoáy |

Bài học lấy về: con tròn mềm thì **nén giãn lớn là diễn xuất chính** (thân là lưới bám nhiều xương, không phải mảnh cứng);
chóp, vây là chuỗi ngắn trễ pha; nét mặt đổi theo clip; chết dẹp thành vũng. Lưới con gốc thưa (26 đỉnh thân) nên nén mạnh sẽ gãy
góc: bản của mình lưới dày theo đặc tả.

## 2. Thiết kế dòng (đề xuất)

**Tên dòng:** Tí Tách (dạng 1) → Sóng Thần (dạng 2). Tên khác nếu muốn: Giọt Bão → Hải Triều; Tí Tách → Thủy Quyền.

**Lore:** giọt mưa đầu mùa rơi xuống biển, mang theo tiếng "tí tách" và một nắm đấm bé xíu; quấn băng đô đỏ tập võ, lớn lên
thành võ sĩ thủy triều, mỗi cú đấm là một con sóng. Băng đô đỏ là điểm nhận ra cả dòng (tướng khởi đầu cần một dấu hiệu dễ nhớ).

**Bảng màu:**

| Vai | Dạng 1 | Dạng 2 |
|---|---|---|
| chủ đạo | lam ngọc sáng `#35BFE6` | chàm đậm `#2C3E9E` |
| sọc sóng, mào | lam đại dương `#1F5DB5` (sọc) | lam ngọc `#35BFE6` (sọc, bờm, vây, găng nước) |
| bụng, viền bọt | bọt nhạt `#D6F2FA` (không để trắng giấy) | bọt nhạt `#D6F2FA` |
| điểm nhấn | băng đô đỏ cà chua `#E2483A`, nút `#A8302A` | khăn, đai đỏ `#E2483A` / `#A8302A`; giáp vỏ ốc kem cát `#F1DDB0` sọc đỏ |
| mắt | tròng kem `#FBF6EA`, con ngươi chàm `#1C3A7A` | như dạng 1, mắt hẹp lại |
| lòng miệng | hồng sẫm `#B8405A` | hồng sẫm `#B8405A` |

So 13 tướng Thủy đang có: Tiểu Y lam trời + kem, Cánh Cụt xanh két + cam, Vây Lam lam hoàng gia + trắng, Lam Quân lam + kem +
vàng, Thương Lam lam băng nhạt, Mi Nhi tím oải hương, Ma Kết xanh bạc hà + san hô, Kuba cam + pha lê, Huyền Vũ lục + lam, Tám Tay
vàng đất, Hải Long ngọc lam + kem vàng + san hô. Không con nào là lam ngọc sáng + đỏ cà chua, hay chàm + lam ngọc + đỏ.

**Dạng 1, Tí Tách (chibi):** cả con là một giọt nước mập đáy tròn; chóp không nhọn thẳng mà **cuộn sang phải như mào sóng**
viền bọt. Lưng vài sọc sóng lam đậm, bụng mảng bọt hình giọt nước ngược. Mắt to tròng chàm, mày xếch, miệng hé hét trận có một
răng nanh. Băng đô đỏ thắt sau đầu, hai dải ngắn bay sau. Tay ngắn nắm đấm, hai bàn chân ngắn, đuôi giọt toé nhỏ. Dáng võ sĩ
tí hon: nắm tay gần giơ trước, nghiêng tới.

**Dạng 2, Sóng Thần (dạng cuối):** võ sĩ thủy triều dạng **thú rồng kỳ giông nước** đứng hai chân thế tấn (không thân người
lực sĩ), đầu ~1/4 chiều cao, mõm dài, thân tròn chắc hơi chồm, chân thú có vuốt. Màu đổi sang chàm đậm, bụng bọt nhạt, sọc
sóng lam ngọc. Mào giọt nước lớn thành **bờm mào sóng** chồng lớp cuộn ra sau; vây tai lam ngọc; băng đô thành khăn đỏ hai dải
dài; găng nước xoáy bọc cẳng tay, vây nhỏ ngoài cẳng tay, nắm đấm có vuốt kem; giáp vỏ ốc xoắn ở vai, vỏ sò ở hai ống chân;
đai đỏ dải thả trước, khoá ngọc hình giọt nước (nét của dòng); đuôi dài chóp mào sóng. Mắt hẹp sắc, nanh, miệng há gầm. Thế
tấn: chân gần trước, chân xa sau, nắm đấm gần đưa thẳng tới, tay xa kéo về sau.

**Khác con gốc:** con gốc là khối thạch nhìn thẳng, không chân tay, bóng loáng, mắt trắng trống, chóp nhọn thẳng, hai vây.
Của mình: nhìn nghiêng 3/4 sang phải, có tay nắm đấm, chân, đuôi, chóp cuộn mào sóng, mắt có con ngươi, miệng có lòng miệng và
nanh, băng đô đỏ, sọc sóng, bụng hình giọt; tô phẳng chì sáp, không bóng. Dạng 2 không có ở con gốc.

## 3. Đòn, chiêu (ý từ chiêu Pokémon hệ nước; phần lớn đứng tại chỗ; hiệu ứng là lớp VFX trên sân)

| Dạng | attack | cast | skill (chiêu cuối) |
|---|---|---|---|
| 1 Tí Tách | **Bong Bóng** (Bubble): phồng má (nén), nhổ chuỗi ba bong bóng từ miệng; đứng tại chỗ, giật lùi nhẹ | **Súng Nước** (Water Gun): ngửa người kéo cao (giãn), chồm tới dẹp, phun tia từ miệng, giữ 0,6 s | **Mưa Rào** (Rain Dance): giơ hai nắm đấm lên trời, mào cuộn bật, thân rung hai dáng; mây nhỏ tụ trên đầu đối thủ trút mưa giọt 3 nhịp |
| 2 Sóng Thần | **Thủy Quyền** (Liquidation): đấm thẳng tại chỗ, nắm đấm nước từ găng bay tới đối thủ | **Vòi Rồng Nước** (Hydro Pump): kéo hai tay về hông tụ nước, đẩy hai lòng bàn tay ra, cột nước dày, giữ 1,0 s rung hai dáng | **Sóng Thần** (Surf): ngửa gầm (há miệng, bờm xoè), đấm xuống đất, sóng lớn dâng sau đối thủ rồi đổ ập |

Chỗ bám VFX: dạng 1 xương `mieng` ở môi (trục x chĩa tới); dạng 2 `mieng` ở nắm tay trước (attack), `mieng` giữa hai lòng bàn
tay (cast), `mieng_dau` ở miệng (gầm). Sự kiện: `trung`, `phun`, `het_phun`, `gam`, `het_gam`, `mua` (dạng 1), `dap_dat`, `song`
(dạng 2).

## 4. Dự kiến pha 2 (chỉ làm sau khi duyệt)

**Dạng 1, tờ mảnh** (một tờ 1536 × 1024, vẽ đủ phần bị che):
thân giọt liền mặt (không mắt, không miệng: mắt, miệng là mảnh riêng để chớp và há) · mào cuộn (rời, đầu khớp tròn) · mắt mở ·
mắt nhắm (mí, cho chớp và trúng đòn) · mắt `> <` (trúng đòn mạnh, chết) · hàm dưới có lòng miệng + răng nanh hàm trên vẽ liền
thân · tay gần, tay xa (một hình lật được) · hai bàn chân (một hình) · đuôi toé · nút băng đô + hai dải.

**Dạng 1, xương (~26):** `root → move → base` (nén giãn ở đất) `→ body0, body1, body2` (thân là lưới dày bám 3 xương dọc + `side_l,
side_r` để phồng hai bên) `→ crest1..3` (mào chuỗi 3 đốt, lò xo) · `face` (mắt, miệng trượt theo thân giả xoay) `→ jaw`, `mieng` ·
`arm_f, arm_b` (1 đốt + nắm tay cứng) · `foot_f, foot_b` (bám đất) · `tail1..3` · `band_k` (nút) `→ band_a1..3, band_b1..3` (dải
lò xo) · `shadow`. Lưới thân dày đều (đích theo README thư viện), trọng số trơn kiểu B-spline dọc thân; nén giãn kiểu con gốc
(0,9; 1,1) ở idle, (0,6–1,6) ở chiêu.

**Dạng 2, tờ mảnh** (hai tờ): A: đầu phần trên (sọ, mõm, hàm trên có nanh, khăn quanh trán, vây tai) · hàm dưới có lòng miệng ·
đầu nhắm mắt (hoặc mảng mí) · bờm mào sóng (2–3 mảnh rời chồng lớp) · hai dải khăn · đuôi duỗi thẳng có chóp mào sóng · dải đai
thả. B: thân (ngực, bụng bọt, đai, ngọc giọt) · cánh tay trên ×2 · cẳng tay có găng nước + vây ×2 · nắm đấm ×2 · bàn tay xoè
(cho cast) · đùi, ống chân có giáp vỏ sò, bàn chân ×2 · giáp vai vỏ ốc.

**Dạng 2, xương (~50):** `root → move → hip → spine1..3 → neck → head → jaw, mieng_dau`; bờm 2–3 mào × 3 đốt lò xo; khăn 2 dải × 4
đốt; dải đai 3 đốt; tay 2 đoạn + nắm tay (hai tay, `mieng` ở nắm tay trước, `mieng_cast` giữa hai lòng bàn tay); chân 2 đoạn + bàn
chân (IK bám đất); đuôi 5 đốt (chuỗi B-spline, chóp mào sóng); giáp vai cứng trên cánh tay trên.

**Tiến hóa:** rig dạng 1 gộp dạng 2 (`pokiclash-spine-rig` mục 11): Tí Tách nén lại, nước dâng lốc, đổi dạng lúc lốc đậm nhất,
Sóng Thần bung ra, đấm, gầm, về khung 0 idle dạng 2.

**Clip đủ bộ** theo đặc tả mục 5 (`appear, idle, attack, cast, skill, hit, die, evolve` cho dạng 1; dạng 2 không có evolve).
`die` dạng 1 học con gốc: giật, nhắm mắt `> <`, lả, rồi dẹp thành vũng nước và tan.

## 5. Concept đã gen

Tờ xem chung: `ArtGen/Spine/inbox/tm01_dong.png`.

| Dạng | Chọn (chép thành `L1_duyet.png`) | Bản khác | Nhận xét |
|---|---|---|---|
| 1 | `inbox/tm01_1/tai_ve/L1_concept.png` | (không, lần 1 đạt) | đúng thiết kế, tô phẳng, nhìn phải; khe trắng mảnh giữa má và tay gần (khe tách, không phải điểm sáng); tay xa chỉ là cục tròn nhỏ |
| 2 | `inbox/tm01_2/tai_ve/L1_concept_2.png` | `inbox/tm01_2/tai_ve/L1_concept.png` | lần 1 thân người lực sĩ, gần như nhìn thẳng (lệch luật "thú nuôi", khó rig thế đánh); lần 2 thêm `--note` (thú rồng kỳ giông, nghiêng 3/4 thật) đạt; câu sửa đã đưa hẳn vào `build_tm01.py` |

Số lần gen: dạng 1 một lần, dạng 2 hai lần (trần 3).

## 6. Pha 2 (2026-11-11, sau khi Claude điều phối báo đã duyệt)

Mã: `ArtGen/Spine/tm01.py` (cắt tờ, lệnh), `tm01_rig.py` (dạng 2), `tm01_rig1.py` (dạng 1 + tiến hóa), `tm01_chung.py` (hàm riêng của
dòng: đổi toạ độ concept → rig, đặt mảnh duỗi thẳng, trọng số nội suy theo lưới thân, ảnh so ghép). Gói tờ mảnh: `build_tm01.py`
lượt 2 (`gui_gpt/tm01_<k>/luot_2_manh.txt`). Lệnh:

    py -3 -I ArtGen/Spine/tm01.py cat 2 | cat 1          cắt tờ vào inbox/tm01_<k>/manh/
    py -3 -I ArtGen/Spine/tm01.py ghep 2 | ghep 1        ảnh so ghép dáng đứng với concept
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm01.py rig 2
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm01.py rig 1   (dựng lại dạng 2 trong bộ nhớ để gộp)

Cách dựng:
- Dạng 2: đầu (hàm hai xương, lòng miệng theo hàm dưới, mí `fit_lid` hở 0 px), thân lưới vùng bám chuỗi lưng 3 đốt + cổ, tay và chân
  2 đoạn (mảnh vẽ duỗi thẳng, trọng số B-spline chiếu lên khớp, khuỷu/gối mềm), nắm tay và bàn tay xoè đổi hình trong một slot, chân
  IK bám đất + bàn chân giữ phẳng, đuôi 6 đốt (lò xo trên sóng), hai mào 3 đốt lò xo, hai dải băng đô dây mềm có gió, dải đai lò xo.
  Mảnh GPT vẽ thành "miệng ống" ở chỗ luôn bị che (cổ trên thân, cổ chân dưới chân) được xén khi nạp (`XEN2`).
- Dạng 1: thân một lưới dày (365 đỉnh), mào cuộn nằm trong lưới thân bám chuỗi 3 đốt; nén giãn ở xương `day` (đáy) như con gốc.
  Bốn miệng (hét, há tròn, mím, nghiến răng) đổi hình trong một slot; mí nhắm và mắt `> <` cho từng mắt; tất cả là hình dán lên thân,
  trọng số nội suy từ lưới thân nên nén giãn cùng thân. Tay 2 đốt (nắm liền), đuôi 4 đốt, hai dải băng đô dây mềm.
- Tiến hóa: `tienhoa.gop` + `clip_tien_hoa`; dạng 2 hiện ra ngay trong dáng khung 0 idle của nó rồi gầm; khung cuối lệch 0,00 px.
- Chết: cả hai dạng tan thành vũng nước (dạng 2 lúc đầu đổ ngửa nhưng một chân đá lên trời, đã đổi).

Đặt mảnh vào concept (bổ sung theo DAC_TA mục 5, bài học dòng 9): không đoán hệ số tay.
- Bước 1 (`tm01_khop.py`, chỉ dạng 2): dò từng mảnh theo màu (vị trí, góc, tỉ lệ; điểm rơi ra nền phạt) → `inbox/tm01_2/khop.json`.
- Bước 2 (`tm01_sil.py`, lệnh `sil 2|1`): dò cả con theo bóng dáng: một hàm bố trí chung (`bo_tri2`, `bo_tri1`) dùng cho cả dò lẫn
  dựng; tay chân hai đoạn gập theo dáng đứng; mục tiêu IoU mặt nạ − chi phí màu; giới hạn: dời ±40 px rig, góc ±25°, mảnh hình
  phức tạp (đầu, mào, giáp, bàn chân, dải đai) giữ tỉ lệ đều 0,8–1,25, tỉ lệ dọc/ngang và độ dày 0,85–1,3 (chân, đuôi tới 1,45).
  Lần dò không giới hạn đạt 0,85 nhưng làm chân béo ×2,7, đuôi ×1,6, đầu méo: đã bỏ.
- Dao động idle trừ giá trị ở giây 0 nên khung 0 idle = dáng concept.
- Kết quả IoU khung 0 idle / concept (`rig/so_concept.png`, ảnh khác biệt `rig/so_concept_iou.png`): dạng 1 **0,921**; dạng 2
  **0,829** (dưới đích 0,85: chóp đuôi cuộn và đùi gần trên tờ mảnh GPT nhỏ hơn concept; ép thêm phải kéo méo hình vẽ).

Sửa sau lần soi thứ hai của Claude điều phối (2026-11-11):
- Lưới dày theo luật mới: bước viền 1,5%, bước trong 2% chiều cao con (dạng 2: 5,7 / 7,6 px; dạng 1: 4,2 / 5,6 px). Tay chuyển
  sang lưới vùng đều. Nắm tay, bàn tay xoè, bàn chân, giáp vai, mí cũng là lưới dày (bàn chân và nắm tay hoà vào ống chân,
  cẳng tay ở chỗ nối; giáp vai vỏ ốc là đồ cứng thật). Tam giác suy biến (góc 0°) ở mép khe hẹp bỏ đi (`bo_tg_det`). Mọi mảnh hở
  0 px. Dạng 2: 3478 đỉnh, 5619 tam giác, 0,19 MB; dạng 1 gộp dạng 2: 6510 đỉnh, 0,31 MB (dưới trần 0,5).
- Chân gần: gen lại M03 (`gui_gpt/tm01_2/luot_3_chan.txt`): chân liền cả chi, đùi to, hai đầu tròn kín; cổ chân thừa dưới cổ giáp
  xén khi nạp, bàn chân gắn dưới cổ giáp. Chân gần vẽ trước bụng, sau dải đai (đùi ló dưới đai như concept). Cỡ chân theo bề
  rộng giáp vỏ sò đo trên concept (120 / 110 px) + vị trí gối đọc trên concept; độ bè chân gần 1,25. Đuôi M03 (chóp xoè hình
  nấm) thử rồi bỏ, giữ đuôi M01.
- IoU khung 0 idle / concept dạng 2 vẫn 0,829 (dạng 1 0,921). Mảnh GPT khác tỉ lệ concept: ống chân concept ngắn bè (giáp ≈ 0,6
  chiều dài chân, mảnh GPT ≈ 0,34), chóp đuôi cuộn concept to hơn. Lần dò không giới hạn đạt 0,85 nhờ kéo méo (chân ×2,7,
  đuôi ×1,6, đầu méo) nên đã bỏ.

Cách lai cho dạng 2 (Claude điều phối chọn sau vòng soi 2; `ArtGen/Spine/tm01_lai.py`, `tm01_rig.LAI2 = True`, chạy bằng
`D:/spine-venv/Scripts/python -I` vì cần cv2):
- Tách vùng trên concept (hạt giống `HAT`, nét mực là tường, nhãn gần nhất, lọc 7x7): thân, đuôi, chân gần, bàn chân gần, chân xa,
  bàn chân xa, đầu, mào a, mào b, hàm (thuộc lớp đầu); phần tách: tay gần, tay xa, dải băng đô, dải đai. Soi `inbox/tm01_2/nhan_lai.png`.
- Lớp THÂN cắt từ concept (thân, cổ, bụng, đai, hai chân, hai bàn chân, đuôi): chỗ tay / dải đai che dán mảnh GPT thân, đuôi, chân
  đã khớp, chỗ còn thiếu trong bóng thân vẽ bù TELEA, nét viền cũ giáp phần cắt xoá đi, mép vẽ bù giáp nền kẻ nét mực; bên trong
  bóng con đặc hẳn; mọc thêm dưới đầu 12% chiều cao bằng màu loang của thân (đầu ngửa không hở họng).
- Lớp ĐẦU cắt từ concept (đầu, băng đô, nút, vây má, hai mào, răng nanh trên, lòng miệng, hàm dưới): hàm há bằng trọng số của
  chính lưới đầu (vùng hàm dưới bám xương hàm, lòng miệng giãn theo độ cao giữa môi trên và môi dưới, răng trên bám đầu); không
  dùng mảnh hàm và lòng miệng GPT nữa (cắt ra thì thủng lỗ ở chỗ răng trên, lòng miệng GPT lòi vệt đỏ dưới hàm).
- Chân bám đất bằng chuỗi đùi → ống (khớp đọc trên concept `KHOP_CHAN`), IK ngọn ở cổ chân; mào, đuôi dùng khớp của mảnh GPT đã khớp.
- Mảnh GPT còn dùng: hai tay + găng + nắm tay / bàn tay xoè, giáp vai, mí (dò trên lớp đầu concept, hở 0 px), hai dải băng đô,
  dải đai.
- Kết quả: IoU khung 0 idle / concept **0,918**; 3234 đỉnh, 5340 tam giác, mọi lưới hở 0; 0,18 MB; nối clip 0 px. Dạng 1 gộp
  dạng 2 mới: evolve khớp 0,00 px, 0,31 MB.
