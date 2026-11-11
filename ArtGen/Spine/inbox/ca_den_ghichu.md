# Dòng cá đèn lồng (mã tạm `ca_den`): tướng thứ 3 đảo Thủy, làm theo ý người dùng (2026-11-11)

Người dùng lên ý tưởng và duyệt concept (chưa đặt tên; mã `ca_den` chỉ để đặt thư mục).
Gói prompt: `ArtGen/Spine/build_ca_den.py` → `gui_gpt/ca_den_<k>/`, ảnh về `inbox/ca_den_<k>/tai_ve/`.

## 1. Ý người dùng (nguyên văn tóm lại)

- Dựa trên con gốc `monster_3233` (game tham khảo). Concept: **cá đèn lồng** (cá có bóng đèn lòi ra) **có chân, đuôi thằn lằn**;
  làm thành **một mảng màu như con gốc**, đừng tách cho khỏi dị. **Mắt, răng có thể làm giống con gốc.**
- `idle`: có thể làm giống con gốc.
- Đánh thường: dùng **bóng đèn quật** vào người đối thủ.
- Chiêu mana: **há mồm bắn nước**, bắn xong **ngậm mồm lại** (tia nước là VFX, rig không vẽ).
- Chiêu cuối: học từ `skill_02` của con gốc: nghiêng người đứng một bên chân rồi dậm chân kia, há mồm kiểu gầm lên; cũng bắn tia
  nước nhưng to hơn, mạnh hơn.
- `appear`: dùng chân **nhảy vào màn hình**.
- `dead`: tuỳ Claude sáng tạo, có thể làm giống con gốc.
- Dạng 2: tương tự nhưng to hơn, chiến hơn. Dung lượng mỗi dạng **0,5 MB**, ít hơn càng tốt.

## 2. Mổ xẻ con gốc `monster_3233` (chỉ học cấu trúc và nhịp, không lấy hình)

Nguồn: `D:\Ripper\SwordxStaff\web\assets\Monster\monster_3233\` (Spine 4.2.28, 0,2 MB). Kết quả quét:
`D:\Ripper\SwordxStaff\scan\monster_3233\` (`info.json`, `keys.json`, `mesh.json`, `keys.txt` = khoá 6 clip dạng đọc được, tờ khung
`khung/<clip>.jpg`). Quét lại: `py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/mo_xe/chay.py info|keys|mesh|sheet ...`.

### Ảnh (atlas 220 × 680, xuất tỉ lệ 0,75; 29 vùng)

| Vùng | Cỡ | Là gì |
|---|---|---|
| `P_shenti1` | 176 × 130 | **nửa trên lúc miệng khép** (đầu, lưng, môi trên) |
| `P_shenti3` | 184 × 125 | **nửa trên lúc miệng há** (môi trên vén lên) |
| `P_shenti2` | 176 × 85 | **hàm dưới + bụng lúc khép** (khối kem tròn) |
| `P_shenti4` | 176 × 71 | **hàm dưới lúc há** (dẹt, thấy mép trong) |
| `P_kouqiang` | 148 × 104 | lòng miệng hồng, **luôn hiện**, nằm sau hai nửa thân |
| `P_yachi1..3` | 23–49 × 29–56 | 3 răng lúc khép (mọc từ hàm dưới chĩa lên, đè lên môi trên) |
| `P_yachi4..8` | 23–50 × 29–60 | 5 răng lúc há (4–6 hàm dưới, 7–8 hàm trên nằm sau thân) |
| `P_yanjing2` + `1` | 62 × 57, 36 × 33 | mắt gần: tròng kem + con ngươi rời (con ngươi có xương riêng để liếc) |
| `P_yanjing4` + `3` | 52 × 56, 16 × 32 | mắt xa (vẽ sau thân) |
| `P_yuqi1` | 88 × 90 | mào vây trên đầu, hai nhánh (3 + 2 đốt) |
| `P_yuqi2` | 90 × 135 | vây lưng sau, hai nhánh (3 + 3 đốt), vẽ sau thân |
| `P_weiba1`, `2` | 95 × 71, 55 × 60 | gốc đuôi, chóp đuôi |
| `P_tuiL1..4`, `P_tuiR1..4` | ≤ 52 × 48 | mỗi chân: đùi, ống, bàn, móng |

**Miệng há = đổi ảnh trong 1 khung** (như con ếch `monster_3230`): tắt `shenti1`, `shenti2`, răng 1–3; bật `shenti3`, `shenti4`,
răng 4–8. Lòng miệng luôn nằm sẵn phía sau nên không cần bật tắt.

### Xương (45) và slot (30)

```
root
└─ bone34 (y −100)
    ├─ bone33 (nhún cả con, chỉ dời y)
    │   └─ bone (tâm thân: dời, nghiêng, lộn cả thân; chân theo qua IK)
    │       ├─ bone5 → bone2 → bone3 → bone4   (chân gần: hông, đùi, ống, bàn; IK R1 + R2)
    │       ├─ bone9 → bone6 → bone7 → bone8   (chân xa; IK L1 + L2)
    │       ├─ bone10 (đáy thân phía sau: nghiêng cả khối)
    │       │   ├─ bone11 (nửa trên / đầu: cúi ngửa)
    │       │   │   ├─ bone19 (môi trên phía trước: nhấc là há)
    │       │   │   ├─ bone26 → bone38 → bone35 (mắt gần → con ngươi)
    │       │   │   ├─ bone27 → bone39 → bone36 (mắt xa → con ngươi)
    │       │   │   ├─ bone20 → 21 → 22 (vây lưng sau, nhánh 1)
    │       │   │   └─ bone28 → 29 → 30, bone31 → 32 (mào vây, hai nhánh)
    │       │   ├─ bone18 (hàm dưới: dời, xoay) → bone37 (**bụng**: phình bằng scale tới 2,2)
    │       │   └─ bone23 → 24 → 25 (vây lưng sau, nhánh 2)
    │       └─ bone12 → 13 → 14 → 15 → 16 → 17 (đuôi 6 đốt)
    ├─ shadow
    ├─ R2 → R1 (đích bàn chân, cổ chân gần)
    └─ L2 → L1 (đích bàn chân, cổ chân xa)
```

Thứ tự vẽ sau → trước: bóng, mắt xa, vây lưng sau, chân xa (4), chóp đuôi, gốc đuôi, lòng miệng, răng hàm trên (lúc há), nửa
trên há, nửa trên khép, mắt gần, răng hàm dưới, hàm dưới há, hàm dưới khép, mào vây, chân gần (4).
3 ràng buộc transform: hai mắt và mào vây đi theo môi trên 30 % theo chiều dọc (há miệng thì mắt, mào nhô theo).

### Lưới và trọng số

- Rất thưa: thân 24–27 đỉnh mỗi nửa, chân 6–10 đỉnh mỗi khúc (cứng theo một xương), răng 6–10 đỉnh.
- Nửa trên: phía sau bám `bone11` (đầu) và `bone12` (gốc đuôi), vành môi trước bám `bone19`.
- Hàm dưới + bụng: mép sau bám `bone10`, `bone12`; mặt trước bám `bone18` (hàm); tâm bụng bám `bone37` → scale `bone37` là bụng
  phồng mà mép không đổi.
- Lòng miệng: nửa trên theo `bone19`, nửa dưới theo `bone18` → há ra thì tấm hồng **giãn** lấp khe.
- Đuôi: gốc đuôi chia cho `bone10`, `12`, `13`, `14` (liền với thân, không lộ khớp); chóp đuôi cho `15`, `16`, `17`.
- Vây: dải lưới theo chuỗi 2–3 đốt. Không physics, không sự kiện. Deform chỉ dùng 1–2 khoá lúc đổi ảnh miệng.

### Mẹo diễn chính

1. **`idle_01`** (32 khung, 1,07 s): `bone` nhún **2 lần** mỗi vòng (lên 21 px ở khung 8 và 24), `bone33` trôi lên xuống **1 lần**
   (−5,5 → +8), thân nghiêng 1,6° → −6,6° một lần → hai tầng lệch nhịp nên không đều như máy. Chân IK bám đất nên thân nhún là gối
   co duỗi. Đuôi 6 đốt: mỗi đốt 2 cực trị mỗi nửa vòng, **đốt sau trễ đốt trước 4 khung**, biên độ lớn dần ra chóp (7° → 18° → 13°
   → 30° → 44° → 57°). Vây cũng vậy (trễ 4 khung, ±15..20°). **Điểm phá nhịp**: con ngươi liếc đi ở khung 4, giữ tới 16, về khung 20.
2. **`skill_02`** (45 khung, 1,5 s; chiêu cuối sẽ học):
   - 0–4 (0,13 s): bàn chân gần lùi ra sau 102 px (bước trụ), thân dời (−118, +58), ngả ra sau; bụng bắt đầu phình (1 → 1,95).
   - 4–6: thân ngả hẳn **57°**, dời (−186, +119); **chân xa nhấc cao** (bàn chân lên +221, xoay 77°).
   - 6–15 (0,3 s, **giữ**): thân trôi chậm tới 61°, chân xa lên +272; bụng **rung mỗi khung** 1,93 ↔ 2,21 (gồng); đuôi, vây
     trôi về dáng nghỉ.
   - 15–17 (**2 khung**): dậm. Khung 16 chân xa cắm đất (quá đà +43 px), thân bật về (2, 12), 11°; khung 17 thân chúi tới
     (−85, −6), −11°, bụng về 1, **đổi ảnh há miệng**, môi trên bật (+31, +15), hàm dưới tụt (−32, −3).
   - 17–31 (0,47 s, **gầm**): hai dáng đổi nhau **mỗi khung** (hàm dưới ±3 px và 2,5°, môi trên ±5 px và −4°), thân nảy mỗi 2
     khung (y 24 ↔ 1, rồi 20 ↔ 13); đuôi, vây quất mỗi 2 khung (đuôi chóp 81° ↔ 33°).
   - 31–36: khép miệng (đổi ảnh khung 34–36), chân trụ bước về (khung 33–36), thân nảy quá đà (+16, +35).
   - 36–45: lắng, đuôi và vây tắt dần.
3. **`skill_01`** (36 khung): nhảy vọt khỏi màn (thân +531 px ở khung 12, lộn −111°) rồi rơi đè, nảy. Không dùng cho đòn nào của
   mình; nửa sau (rơi, bẹp, nảy khung 18–36) là mẫu cho cú tiếp đất của `appear`.
4. **`generate_01`** (24 khung, 0,8 s; mẫu `appear`): khung 0 thu nhỏ 0,14, khung 3 đã ở cao +393 (chân co lên +188, +158), khung
   8 đỉnh +438, khung 12 rơi +328 và lộn −52°, khung 14 còn +69, **khung 16 chạm đất**, 18–22 nảy +23 / +27 / +13, 24 về.
   Miệng há suốt lúc bay, khép khi chạm đất (khung 18).
5. **`die_01`** (30 khung): miệng há cả clip; khung 0 bị hất nghiêng −52°, khung 2–12 bay lên +245 px, khung 15 rơi xuống thấp
   hơn mặt đất 33 px, **nằm nghiêng −25°**, 15–27 nảy tắt dần (thân ±5°, hàm dưới lắc), con ngươi **quay vòng** (172° → 297°), đuôi
   duỗi ra đất.
6. **`hit_01`** (15 khung): khung 0 đã lệch (−20, +10) −25°; khung 2 bị hất (−97, +128) 92°, miệng há, chân xa văng lên +275;
   khung 6–10 rơi về, 12–15 chạm đất.
7. Khoá gần như toàn đường thẳng; nhịp giật 1–2 khung ở lúc ra đòn, 3–6 khung lúc nảy về.

### Clip (12)

`idle_01` 1,07 s; `skill_01` 1,2 s (nhảy đè); `skill_02` 1,5 s (dậm chân gầm); `skill_02X` 1,33 s (bản nháp của họ);
`generate_01` 0,8 s; `hit_01` 0,5 s; `hit_02` 0,67 s; `die_01` 1,0 s; `block_01` 0,5 s; `floating_01` 1,5 s; `run_01` 0,53 s;
`stun_01` 1,33 s.

| Clip của mình | Học từ | Ghi chú |
|---|---|---|
| `idle` | `idle_01` | nhún 2 lần + trôi 1 lần, đuôi trễ từng đốt, con ngươi liếc; **thêm**: cần đèn đung đưa trễ pha, bóng đèn lắc như quả lắc |
| `attack` | mới | cần đèn ngả ra sau lấy đà (thân ngả theo), **quật qua đầu xuống phía trước** trong 2 khung, cần giãn 1,15 ở khung nhanh nhất, bóng đèn đập, khựng, cần nảy dư lực, thu về. Sự kiện `trung` |
| `cast` | nửa sau `skill_02` (đổi ảnh há) | ngửa nhẹ lấy hơi, bụng phình, chồm tới há miệng, giữ há rung nhẹ tới hết tia, **ngậm lại** rồi mới về. Sự kiện `phun`, `het_phun`; xương `mieng` |
| `skill` | `skill_02` | bước trụ, ngả 57° đứng một chân, chân kia nhấc cao, bụng phình rung; dậm 2 khung; há miệng gầm, giữ rung; ngậm; lắng. Sự kiện `dam`, `phun`, `het_phun` |
| `appear` | `generate_01` + nửa sau `skill_01` | **nhảy bằng chân từ ngoài màn vào** theo cung (không thu phóng), chân co lúc bay, duỗi đón đất, bẹp, nảy 2 lần; đèn và đuôi văng trễ. Sự kiện `cham_dat` |
| `hit` | `hit_01` | |
| `die` | `die_01` | đề xuất: bị hất, rơi nằm nghiêng, miệng há, chân giật, **cần đèn rũ xuống đất và bóng đèn tắt** (đổi sang ảnh bóng đèn xám), con ngươi quay vòng |
| `evolve` | chưa có ý của người dùng | hỏi khi tới bước clip |

## 3. Thiết kế của mình (dạng 1)

- Dáng: cá tròn mập, đầu liền thân, gần như chỉ có đầu và miệng. Nửa trên màu chàm; nửa dưới trước là **hàm dưới + bụng kem** tròn
  trơn. **Đường miệng = ranh chàm / kem**, hô hàm dưới (đúng kiểu cá đèn lồng), ba răng ngà mọc từ hàm dưới chĩa lên.
- **Một mảng màu**: thân, hai chân, bàn chân và cả đuôi cùng một màu chàm, liền nhau (ý người dùng).
- Cần đèn: mọc từ trán, cong ra phía trước như cần câu, cuối cần là bóng đèn vàng tròn; bóng đèn **tô phẳng, không phát sáng**
  (luật tô phẳng). Bóng đèn và 2/3 cần nằm trên nền trắng, không đè mặt (dễ cắt, dễ quật).
- Mắt: tròn lồi to, tròng kem, con ngươi tròn đen to + một chấm trắng nhỏ (luật dự án), mí chàm sụp 1/3 cho vẻ lì, quả quyết.
- Khác con gốc: loài (cá đèn lồng), màu (chàm thay lam), cần đèn thay mào vây vàng, đuôi thằn lằn trơn thay đuôi lửa lục, một vây
  lưng nhỏ + một vây bên, mắt có con ngươi đen và mí.
- Màu (Claude đề xuất, người dùng chưa chốt): thân `#4C5FC4`, đốm `#34428F`, kem `#F4EBCB`, răng `#FBF6E6`, đèn `#FFD75A`,
  màng vây `#9BA8F2`. Chọn chàm để khác Tí Tách (lam nhạt), Vây Lam (lam) và ếch (lục); vàng của đèn là điểm nhấn duy nhất.
- Dạng 2 (nháp trong `build_ca_den.py`): cùng dáng, cùng bố cục; hàm nặng hơn, 5 răng (2 nanh to), gờ mày, cần đèn dày dài, bóng
  đèn to như chuỳ (chụp có gai tù), vây lưng cao 4 gai, vuốt ngà, hàng gai tù dọc đuôi, chàm đậm hơn.

## 4. Dự kiến rig (làm sau khi concept được duyệt)

- Ảnh cần thêm (lượt 2, cùng khung, đính concept đã duyệt): **dáng há miệng** (nửa trên vén môi, hàm dưới tụt, lòng miệng, răng
  lúc há); phần khuất của chân gần, chân xa, gốc đuôi, gốc cần đèn; **bóng đèn tắt** (xám) cho `die` nếu người dùng đồng ý.
  Thân khép, mắt, vây, đuôi, cần đèn cắt thẳng từ concept (cách lai, `pokiclash-spine-rig` mục 21).
- Xương: `root → move (code dời) → nhun → than (dời, nghiêng) → day → dau (cúi ngửa) → moi_tren, mat ×2 (+ con ngươi), vay_lung
  3 đốt, can_den 6–7 đốt → bong_den; ham_duoi → bung (phình); vay_ben 2 đốt; duoi 6 đốt; mieng (chỗ và hướng nhả cho VFX)`;
  hai chân IK bám đích bàn chân (đùi, ống, bàn).
- Cần đèn: dải lưới chia trọng số kiểu B-spline (không đỉnh nào bám cứng một đốt); mô phỏng lò xo rồi nướng khoá cho idle, hit,
  appear; đòn quật thì đặt dáng tay (đầu mút dẫn, đốt gốc trễ).
- Dung lượng: con gốc 0,2 MB. Của mình: atlas thu ~0,5 lần, bảng 256 màu; nướng 30 khung/giây lọc RDP; đích ≤ 0,35 MB mỗi dạng.

## 5. Lượt gen

- 2026-11-11 `ca_den_1/tai_ve/L1_concept.png` (bản chính): đúng đặc tả (một mảng màu, hô hàm dưới ba răng, cần đèn không đè mặt,
  không phát sáng, tô phẳng). Vây bên to, đè lên đùi chân gần; gốc đuôi dính sát chân gần nên chân gần chỉ lộ ống và bàn.
- 2026-11-11 `ca_den_1/tai_ve/L1_concept_2.png` (`--note` vây bên nhỏ đặt cao, chân gần lộ hẳn, đuôi mọc từ lưng): hai chân rõ,
  đuôi tách khỏi chân, vây bên nhỏ trên má; con vật nhỏ hơn trong khung (thân ~640 × 520). Claude đề xuất bản này (dễ cắt, dễ
  rig chân IK và đuôi, đúng bố cục chân của con gốc để học `skill_02`).
- Màu chàm ra tươi hơn mã đã ghi (gần `#3F4FC8`).
- 2026-11-11 **người dùng chọn bản 1** → `L1_duyet.png` = `L1_concept.png`.
- 2026-11-11 `ca_den_2/tai_ve/L1_concept.png` (dạng 2): cùng bố cục dạng 1, to nặng, chàm đậm, 5 răng, gờ mày, vây lưng cao, bóng
  đèn to có chụp gai, gai đuôi, móng ngà. **Người dùng duyệt 2026-11-11** → `L1_duyet.png`.

## 6. Rig dạng 1 (2026-11-11, `ArtGen/Spine/ca_den.py`)

Không nhờ GPT vẽ mảnh nào: mọi lớp cắt thẳng từ concept, phần khuất tô lại bằng vân sáp lát từ chỗ sạch cùng màu (tô phẳng nên
làm được bằng mã). Lệnh: `ca_den.py cat 1` rồi `quai/khoa.py nang -- ca_den.py rig 1`. Ra `inbox/ca_den_1/manh/` và `rig/`.

- **Lớp** (sau → trước): `chan_xa` (mọc thêm 80 px dưới bụng) · `mieng` (lòng miệng tô bằng mã, giãn giữa môi và hàm) · `luoi` (u
  lưỡi, theo hàm, khép miệng thì khuất sau môi trên) · `than` (**một lưới liền**: đầu, lưng, vây lưng, vây bên, chân gần, đuôi;
  chỗ răng tô lại thành môi, tròng mắt xoá con ngươi, gốc cần đèn kẻ lại nét đỉnh đầu) · `nguoi_g/x` (con ngươi tròn đủ) ·
  `vanh_g/x` (viền + mí mắt đè lên con ngươi: con ngươi trượt, quay được mà không cần mặt nạ cắt) · `ham` (bụng kem + răng) · `den`.
- **Miệng há bằng uốn lưới**, không đổi ảnh như con gốc: `dau` ngửa 17° (môi trên nhấc), `ham` hạ 8°, lòng miệng nằm sau giãn theo
  cả hai. Trọng số là hàm của vị trí (bán kính và góc quanh khoé miệng, độ sâu dưới đường miệng), dùng chung cho lớp thân, hàm,
  lòng miệng nên ba lớp không hở ở khoé.
- **Chân không có xương đùi, ống**: bàn chân là xương con của `move` (bám đất), phần ống là lưới giãn giữa thân và bàn chân;
  `theo_than()` cho bàn chân đi theo thân khi nhảy, nhấc chân.
- 34 xương, 10 slot, 3433 đỉnh, 7 clip, **`.atomik` 197 KB** (đích 300, trần 500). Nối clip: khung cuối và khung đầu mọi clip lệch
  khung 0 idle 0 px (`khop_dau` hoà 0,15 s đầu từ dáng idle có độ trễ lò xo: trước đó cần đèn lệch 14 px). `game.height` = đỉnh vây
  lưng (393 px), không tính cần đèn, để thân to ngang các tướng khác.
- Clip: `appear` 1,0 s (chạm đất 0,43) · `idle` 2,13 s · `attack` 1,0 s (trúng 0,43; `move` lao 0,3 H) · `cast` 1,2 s (phun 0,5,
  hết 0,9) · `skill` 1,6 s (dậm 0,53, phun 0,57, hết 1,1) · `hit` 0,5 s · `die` 1,33 s (nằm sấp, cần đèn đổ ra trước, mờ dần).
- Lỗi đã gặp: mép mực / kem pha ra màu nâu bị phân lớp nhầm thành "chàm" (chặn bằng điều kiện ngả lam); đường miệng dò nhầm cả nét
  đáy bụng ở cột có chân xa (cùng màu chàm) làm lệch trọng số hàm; lòng miệng theo vành hàm 100 % thì lòi dưới bụng (cho theo đúng
  trọng số lớp hàm); dải mọc thêm của thân dưới bụng dính theo bàn chân gần; cuộn đuôi sát thân làm lưới tự đè (đốm).
- **Dạng 2 và tiến hóa** (cùng ngày): `ca_den.py cat 2`, rồi `ca_den.py all` = dựng dạng 2 (252 KB), dựng bản nhẹ của dạng 2 (ảnh
  0,6 lần, lưới thưa 1,8 lần) và gộp vào dạng 1 cho clip `evolve` 2,8 s (dạng 1 gộp: 68 xương, 289 KB; khung cuối lệch khung 0 idle
  dạng 2: 0 px). Dạng 2 dùng chung mọi clip, chậm 1,1 lần. Riêng dạng 2: bảng màu phân lớp riêng (`MAU_K`, chàm đậm hơn), chân xa
  lấy theo ô quanh bàn chân (ngón chia nhiều cụm, có móng ngà), đường miệng lấy từ mép trên bụng kem theo cột (dò theo nét mực thì
  lẫn nét đáy bụng), răng nanh chìa ra ngoài viền đầu thì lớp thân không tô môi và không giữ nét răng ở phần ngoài viền.
- **Há miệng tròn** (người dùng dặn 2026-11-11 sau khi xem web: "hướng mặt khi mở miệng làm như con gốc, miệng mở ra đỡ trống, chỉ
  thấy mỗi thịt đỏ"): vẫn uốn lưới, không đổi ảnh. Thêm xương `moi_g` (môi trên vồng lên đều, 0,09 bề dài miệng, giới hạn theo
  khoảng trống tới đáy mắt lấy chỗ hẹp nhất quanh đó: để vồng tự do thì môi nhọn hoắt giữa hai mắt) và `ham_g` (vành hàm võng xuống
  ở giữa 0,28 bề dài miệng, răng dưới và lưỡi đi theo); giảm góc `dau` 17° → 11°, `ham` 8° → 4°. Thêm hàng **răng trên** (mảnh
  `rang_tren`, chân răng nấp sau môi, thân răng nấp sau hàm lúc khép), **họng sẫm** giữa lòng miệng, lưỡi to hơn.
- **Má bên kia** (người dùng dặn tiếp: "phần bên kia phải nhìn thấy má bên kia chứ không phải thịt đỏ, xem lại ảnh gốc"): mảnh `ma_xa`
  ở đầu mút miệng (mép phải), trước lòng miệng, sau lớp thân và lớp hàm; chàm ở trên, kem ở dưới, nét mực dọc mép trong; rộng 0,29
  bề dài miệng ở hai đầu, 0,62 lần đó ở giữa (mép trong cong). Khép miệng thì nấp hết; há thì giãn giữa đầu môi và đầu vành hàm
  (cùng hàm trọng số `w_khe` với lòng miệng), bịt mép phải của hốc miệng như con gốc. Dạng 1 gộp 322 KB, dạng 2 281 KB.
- **Há miệng = đổi ảnh, như con gốc** (người dùng xem bản uốn lưới có má bên kia vẫn chê "chắp vá, gen lại đi; của họ hai hàm
  trên dưới khít luôn ở mép bên kia"). Lượt 2 của gói GPT: `gui_gpt/ca_den_<k>/luot_2_ha_mieng.txt` (sinh bằng `build_ca_den.py`,
  hàm `build_ha`): vẽ lại ĐÚNG concept, chỉ đổi miệng thành hốc tròn khép kín, hai môi gặp nhau ở cả hai mép, có má bên kia, răng
  trên, lưỡi, họng → `tai_ve/M01.png`. GPT giữ phần còn lại trùng concept (đo lệch pha: dưới 0,4 px ở dạng 1, dưới 0,7 px ở dạng
  2) nên không phải khớp lại. `ca_den.py cat` cắt mảnh `ha` = hốc miệng + răng + hàm và bụng kem (đặc) + vành môi quanh hốc (mờ dần
  vào da chàm của lớp thân trong 50 px) + má bên kia và mọi chỗ lớp thân khép bị khuyết (đặc). Slot `ha` nằm ngay trên lớp thân,
  dưới mắt; một lưới, trọng số: trên vòm môi theo `dau`, dưới vành hàm theo `ham` / `bung`, trong hốc hoà (răng dưới, lưỡi theo
  hàm; răng trên theo môi). `mo(P, m)`: m < 0,55 vẫn uốn lưới bản khép (táp miệng, hé miệng); m ≥ 0,55 thì bật `ha`, tắt `ham`,
  `mieng`, `luoi`, `rang_tren`, `ma_xa`, và xoay `dau` / `ham` theo (m − 1) để rung lúc gầm. Dạng 1 gộp 389 KB, dạng 2 337 KB.
  Còn sót: ở dạng 2, mép môi của lớp thân khép thò ra ngoài viền má của hình há vài px bên phải (nét đôi nhỏ).
- Chưa làm: bóng đèn tắt lúc chết (người dùng chưa trả lời).

## 7. Vào game (2026-11-11)

Người dùng chốt: suất **ải 10 đảo Thủy**, thay dòng Nòng Xoáy. **Dòng Hải Đăng**, tướng `ca_den` tên Hải Đăng, danh hiệu "Cá đèn lồng
vực sâu"; dạng 1 **Lồng Đèn** (`ca_den_1`), dạng 2 **Hải Đăng** (`ca_den_2`); thẻ chiêu mana **Vòi Nước**, chiêu cuối **Thủy Pháo**, bị
động giữ Vụng San Hô; **id nội bộ đổi `nong_xoay` → `ca_den`**. Chỉ số, độ hiếm, số và hiệu ứng thẻ giữ của Nòng Xoáy.

Đã làm ngoài Unity (`ArtGen/Spine/quai/doi_ca_den.py`, chạy lại không đổi gì thêm):
- `heroes.json`, `cards.json`, `stages.json` (id + tên), `balance.json` (`saveVersion` 6 → 7); 7 golden chỉ đổi id (roster, zones,
  islands, cardtext, badges, potential, progression: golden không chứa tên).
- `SaveData.cs`: `ThuyV6` trỏ `canh_cut` → `ca_den`; thêm bước **v6 → v7** `MigrateCaDenV6` gộp `nong_xoay` vào `ca_den`.
  `CoreGoldenTests.cs`: `saveVersion` 7. `IslandGen.cs` (ải 10). `StageView.WaterFx`: `ca_den` = `n_tia` cho chiêu mana và chiêu cuối
  hai dạng (tia nước, chiêu cuối to hơn 1,25). `HatNuoc.WThemes`: `ca_den` màu chàm.
- `quai/tuong_moi_thuy.py`, `golden_thuy.py`, `vao_game.py`, `da_nhan.json`; `vao_game.py` đã chép `.atomik` + chân dung vào
  `Assets/03 Art/Heroes/Resources/ca_den_1`, `ca_den_2`.

- **Giữ miệng há theo tia nước của game** (phiên assets-7e báo: `HatNuoc` `n_tia` chảy 0,88 s thật kể từ `phun`; người dùng đã chê Tí
  Tách ngậm miệng khi nước còn phun): `cast` và `skill` giữ há tới `phun` + 0,94 s (`GIU_TIA`, hàm `chen` chèn khung đứng vào cuối
  đoạn giữ). Dạng 1: `cast` 1,8 s (phun 0,5, hết 1,47), `skill` 2,07 s (phun 0,57, hết 1,53). Dạng 1 gộp 391 KB, dạng 2 339 KB.

**Đã chạy trong Unity (13:25–13:40)** bằng script Editor tạm đọc file lệnh trong `Temp/` (đã gỡ sau khi dùng; máy chủ MCP không
khởi động được vì bị hệ thống quyền chặn; `AppActivate` không đủ để Unity lấy tiêu điểm, phải `SetForegroundWindow` kèm nhấn Alt):
- `PokiClash/Nhập dữ liệu`: 88 tướng, 265 thẻ riêng, 350 ải; `HeroDb`, `CardDb`, `ZoneDb` đã có `ca_den`.
- `PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng`: dựng `ca_den_1.asset`, `ca_den_2.asset`, prefab `ca_den` (2 dạng), thêm vào
  HeroModels. (Menu này ghi lại trường `source` của mọi `<dạng>.asset` .atomik: khác biệt một dòng mỗi file, vô hại.)
- `PokiClash/Tướng/Chụp thử dạng .atomik (mọi clip)`: `Library/PokiHeroShots/ca_den_atomik_1.png`, `_2.png` đúng hình (đứng, trúng
  đòn, quật đèn có lao 124 px, bắn nước, chiêu cuối, tiến hóa); tia ở (136, 120) / (161, 142) px rig.
- **EditMode test: 102 qua, 1 hỏng** (`PrefabOnlyTests.MaRuntime_KhongSinhDoVat`: `UI/Kit/NumberTicker.cs`, `UiMotion.cs` có
  `AddComponent`; hai file này không đổi từ 2026-11-06, không liên quan lần đổi này).

**Còn lại:**
1. (Xong 2026-11-11, người dùng cho phép) Đã xoá hình cũ: `Resources/nong_xoay_1`, `nong_xoay_2`, prefab `nong_xoay` và mục của nó
   trong `HeroModels.asset` (16 file đều có trong git, lấy lại được). `nong_xoay` chỉ còn trong `SaveData.cs` (bước chuyển bản lưu).
2. Chưa vào trận thật (ải 10 đảo Thủy) xem cỡ, tia nước ra đúng miệng, khung đổi ảnh khép → há, ra sân, chết.
Lưu ý phiên khác: chạy `vao_game.py` không tham số chép mọi dòng trong `da_nhan.json` (lần chạy của phiên này đã chép luôn rig ếch
vào `thach_giai_1`, `thach_giai_2`; phiên assets-47 cũng tự chép cùng nội dung).
  Mới soi tờ khung và ảnh cận, **chưa xem ở tốc độ thật** (trang `rig/xem.html`).
