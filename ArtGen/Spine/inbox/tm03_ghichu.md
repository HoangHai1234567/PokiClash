# Dòng tm03 (lô 10 tướng mới đảo Thủy): ghi chú pha 1

Đặc tả chung: `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`. Thay suất ải 10 đảo Thủy (Cánh Cụt, thường). Gói prompt:
`ArtGen/Spine/build_tm03.py` → `gui_gpt/tm03_<k>/`; ảnh: `inbox/tm03_<k>/tai_ve/`.

## 1. Con gốc (monster_3230, chỉ học cấu trúc và nhịp, không lấy hình)

Số tổng: Spine 4.2.28, 34 xương, 17 slot (16 lưới, 1 bóng), 216 đỉnh, 4 IK (hai chân), không physics, không sự kiện, 13 clip,
atlas 420 × 332 tỉ lệ 0,75, 0,1 MB.

**Hình thật của con gốc** (đọc atlas): cái "tai xoắn ốc" là **hai con mắt lồi trên đỉnh** (`yanjing`, con ngươi xoắn ốc); cái
"mặt nạ trắng có vằn" là **cái lưỡi** dài buông trước mặt (`shetou2`, 104 px, bám chuỗi 4 xương con của vòm đầu). Cả con là một
cái miệng: vòm đầu xanh (`shenti1`) là hàm trên, thân kem (`shenti2`) là hàm dưới + bụng.

| Mảnh | Là gì | Bám xương |
|---|---|---|
| `shenti1` | vòm đầu xanh vằn tím = hàm trên | bone4, 5, 6 (24 đỉnh) |
| `shenti2` / `shenti3` | thân kem lúc khép / lúc há (đổi hình) | bone4, 5, 8 / bone4, 7, 8 |
| `shenti4` | khối lưng xanh phía sau | bone4, 5 |
| `kouqiang2` / `kouqiang1` | lòng miệng đỏ to (sau thân) / lòng hàm dưới (hiện lúc há) | bone4–6 / bone4, 7 |
| `shetou2` / `shetou1` | lưỡi buông (mặc định) / lưỡi dài 192 px quất (hiện lúc đánh) | chuỗi 4 xương / chuỗi 6 xương |
| `yanjing1`, `yanjing2` | mắt gần, mắt xa | bone9, bone10 (cứng) |
| `tui*1..3` (×2) | đùi, cẳng, bàn chân hai bên | mỗi mảnh một xương, IK |

Cây xương: root → bone2 → bone → bone3 (gốc thân, nhún, lộn) → bone4 (thân) → bone5 (hàm trên) → bone6 (vòm, chuỗi lưỡi buông
bone19–22); bone4 → bone7 (hàm dưới), bone8 (họng/bụng: phồng), chuỗi lưỡi dài bone23–28; chân bone11→12→13→14 và
bone15→16→17→18 với IK đích L1/L2, R1/R2 (bàn chân bám đất).

Clip và nhịp (đọc khoá bằng `mo_xe/nhip.py`):

| Clip | Dài | Diễn |
|---|---|---|
| idle_01 | 1,33 s | **nhún hai lần một vòng** (gốc thân lên 9,7 ở 0,33 và 1,0 s, chân ngược −7,7); thân lắc ±2,2°, hàm trên ±4,6° trễ 0,17 s; **họng phồng 1,8 lần 0,17–0,5 s** (điểm phá nhịp); lưỡi buông vẫy liên hồi 0,47–0,8 s (khoá mỗi 1 khung, 20–30°) |
| skill_01 | 1,17 s | **lưỡi quất**: ngửa hàm trên −24° (0,13–0,3 s), há trong 1 khung (0,37 → 0,40 s), lưỡi dài 6 đốt vung 130° ở gốc, ngọn quất muộn hơn, giữ tới 0,83 s, thu về trong 2 khung; 91% khoá nội suy thẳng |
| skill_02 | 1,0 s | **nhảy đập**: vọt lên 368 ở 0,27 s, đập xuống ở 0,53 s (nghiêng −26°), nảy lại 218, đáp ở 1,0 s |
| skill_03 | 1,27 s | **lao cắn**: lùi −45 (0,07–0,2 s), lao +73 ở 0,3 s há miệng, giữ, về |
| hit_01 / hit_02 | 0,5 / 0,67 s | bật lên 125 và ngửa 47° ở 0,07 s (khung 2), há miệng thè lưỡi / lộn một vòng 360° |
| die_01 | 1,0 s | vọt lên lộn một vòng, đáp ở 0,47 s há miệng thè lưỡi, nảy vài nhịp |
| block, floating, run, stun | 0,5 / 1,5 / 0,87 / 1,33 s | đỡ lùi; bị hất bay lộn; chạy nảy 2 bước; choáng lắc chậm (bezier) |

Bài học lấy: thân tròn là cái miệng (hàm trên và hàm dưới là hai nửa quả bóng, lòng miệng nằm sau); họng phồng làm điểm phá nhịp;
chuỗi lưỡi trễ theo vòm đầu; nhún hai lần một vòng idle; ra đòn khoá cùng khung, nhanh chậm do khoảng cách khoá; trúng đòn đỉnh ở
khung 2. Không lấy: hình mắt xoắn, lưỡi trắng có vằn, màu xanh tím + tím + hồng, dáng ngồi tròn không đuôi, chiêu lưỡi quất.

## 2. Thiết kế dòng (đề xuất)

Tên dòng **Nòng Xoáy** (dạng 1 Nòng Xoáy, dạng 2 Ếch Lốc). Danh hiệu gợi ý: "Nòng nọc mắt bão".

Lore: nở ra giữa mắt một xoáy nước trong vụng san hô; đuôi lớn lên cuộn tròn như vỏ ốc, nó quay đuôi như chân vịt để khuấy xoáy
và thổi bong bóng. Lớn lên thì đuôi tiêu đi, sức xoáy dồn vào cặp sừng mày xoắn và cái túi kêu khổng lồ: một tiếng ộp phóng ra
những vòng nước xoay. Nó khoác chiếc lá súng của vua đầm cũ làm áo choàng.

Khác các dòng cùng lô (đã đọc ghi chú của họ lúc 01:16): dòng 6 (`tm06`) đã đổi sang kỳ giông (lam xám + cam mơ → chàm + hổ
phách); dòng 1 (`tm01`) dạng 2 có giáp vai vỏ ốc xoắn; dạng 2 của dòng 1, 4, 5, 6, 8 đều chàm đậm. Vì vậy dạng 2 dòng này **không
chàm, không vỏ ốc**: lam cô-ban tươi đốm đen chàm kiểu ếch phi tiêu + vàng chanh nghệ + áo choàng lá súng. Dáng: nòng nọc tròn
đuôi cuộn → ếch sừng bốn chi phục thấp (không ai trong lô có dáng này).

### Bảng màu

| Vùng | Dạng 1 Nòng Xoáy | Dạng 2 Ếch Lốc |
|---|---|---|
| Lưng, đỉnh đầu | cerulean `#3FA9E0` | lam cô-ban đậm tươi `#2457C5` |
| Vằn | lam đậm `#24407F` (vằn cong cuộn móc) | đen chàm `#1A1F3D` (đốm tròn, đốm to cuộn móc xoáy) |
| Bụng, cằm | vàng chanh kem `#F6E28C` | vàng chanh nghệ `#F5CE3A` (cả túi kêu trơn, 2–3 gợn đen chàm ở mép dưới) |
| Đặc trưng | vây đuôi xanh nước nhạt `#9FE1F0` | sừng ngà `#F0E2BE` vòng lam đậm; áo choàng lá súng `#3F8A5A` gân `#6DB37A`; dây sậy `#D8B867`; khoá vàng `#E2A93B` |
| Mắt | hổ phách `#F2B23A`, con ngươi ngang | hổ phách đậm `#F09A2A`, con ngươi ngang, mày nặng |
| Đệm ngón | cam quýt `#F28A3C` | cam `#EE7F38`, vuốt ngắn sẫm |
| Lòng miệng, lưỡi | `#C9506A`, `#E58A9C` | `#B8405A`, lưỡi hồng, răng nhỏ + 2 nanh kem |

Không trùng 13 tướng Thủy đang có (lam + trắng, lam nhạt, tím oải hương, lục + mòng két, cam, lục rùa, vàng cam bạch tuộc): cặp
lam + vàng chanh/vàng nghệ + cam ngón là riêng của dòng này.

### Dạng 1: Nòng Xoáy (chibi)

Nòng nọc vừa nhú chân: thân là một quả bóng tròn mập (đầu liền thân), lưng cerulean có vằn lam đậm cuộn móc, bụng vàng chanh. Hai
mắt ếch lồi to trên đỉnh, tròng hổ phách con ngươi ngang, mí dày hạ xuống cho mặt quả quyết. Miệng rộng hé thấy lòng miệng hồng và
chóp lưỡi. Hai chân sau ngắn mới nhú, hai chân trước tí hon, đệm ngón cam. Đặc trưng: **đuôi vây cuộn xoắn ốc 2,5 vòng** dựng sau
mông như ngọn dương xỉ / vỏ ốc.

### Dạng 2: Ếch Lốc (dạng cuối)

Ếch sừng trưởng thành to, nặng, **phục thấp bốn chi thế vồ**: chân trước thẳng chống rộng, đùi sau to gập. Màu đổi sang lam
cô-ban đậm tươi, đốm xoáy đen chàm (kiểu ếch phi tiêu). Đổi đặc trưng: mất đuôi, thay bằng **sừng mày cuộn xoắn** và **túi kêu
vàng phồng** (ộp ra vòng nước xoáy; trên túi không vẽ xoắn ốc, chỉ gợn). Thêm đồ: **áo choàng lá súng** phủ vai và lưng, dây sậy buộc chéo ngực, khoá vàng khắc xoắn ốc, băng
dây sậy ở cẳng tay. Miệng hé có răng nhỏ và hai nanh. Giữ: mắt ếch hổ phách con ngươi ngang, bụng vàng, vằn cuộn móc, đệm ngón cam.

### Đòn, chiêu (đứng tại chỗ, dạng sau mạnh hơn và đổi kiểu)

| | Dạng 1 Nòng Xoáy | Dạng 2 Ếch Lốc |
|---|---|---|
| `attack` | **Bọt Nước** (Bubble): ngửa nhẹ lấy đà 0,3 s, phồng họng, há miệng nhả 3 bong bóng; sự kiện `trung` | **Thủy Chưởng**: nhổm thân, rút tay gần ra sau (đà ngược), đẩy chưởng tới (thân vươn ≤ 0,15H, không lao), viên đạn nước xoắn ốc từ lòng bàn tay; `trung` |
| `cast` | **Đuôi Xoáy** (Water Pulse): đuôi cuộn chặt lấy đà rồi bung quất qua đầu ra trước, vòng nước xoay bay ra từ ngọn đuôi; `phun`, `het_phun`, xương `mieng` ở ngọn đuôi | **Ộp Âm Ba** (Hyper Voice / Bubble Beam): túi kêu phồng 1,6 lần, há miệng ộp, 3 vòng sóng nước toả tới đối thủ kèm chuỗi bong bóng; giữ 0,9 s rung hai dáng; `phun`, `het_phun`, `mieng` ở miệng |
| `skill` | **Xoáy Bong Bóng** (Whirlpool nhỏ): đuôi quay như chân vịt, nhún đập bụng, xoáy nước nhỏ mở dưới chân đối thủ cuốn bong bóng rồi rơi (`vortex` sức 1); `xoay`, `het_xoay` | **Đại Hải Lốc** (Maelstrom): chồm hai chân trước lên, túi kêu phồng, đập hai tay xuống đất; xoáy lớn mở dưới chân đối thủ, cột nước xoắn dâng nuốt, nổ cuối, mưa giọt (`vortex` sức 3); `dam`, `gam`, `het_gam` |

## 3. Concept đã gen (pha 1)

Dạng 1 (`inbox/tm03_1/tai_ve/`, 3 lần gen, tối đa theo đặc tả):
- **`L1_concept.png` (chọn):** nghiêng 3/4 sang phải, mí hạ chữ V mặt quả quyết, miệng hé thấy lòng miệng + lưỡi, con ngươi ngang,
  lưng cerulean vằn lam đậm cuộn móc, bụng vàng chanh, đuôi cuộn xoắn ốc có vây nhạt, đệm ngón cam; bốn chân tách nhau bằng khe
  trắng (dễ rig nhất). Điểm yếu: chân hơi dài, đứng bốn chân như thằn lằn hơn là nòng nọc; pha 2 vẽ tờ mảnh có thể rút ngắn chân trước.
- `L1_concept_2.png`: thân nòng nọc mập nhất, vây đuôi rộng, chân trước tí hon dính bụng; nhưng mắt lim dim trông chán, không chiến.
- `L1_concept_3.png`: mặt gần như chính diện, miệng há to như đang hét, trông hài; không đạt hướng 3/4 sang phải.
Cả ba: tô phẳng, không bóng, không điểm sáng trên da, nền trắng (253–254).

Dạng 2 (`inbox/tm03_2/tai_ve/`, 2 lần gen, ảnh mẫu: Vây Lam dạng 3 lấy thế vồ, concept dạng 1 đã chọn, bản đồ lấy nét):
- **`L1_concept_2.png` (chọn):** ếch sừng phục thấp bốn chi nhìn sang phải, lam cô-ban đốm xoáy đen chàm, bụng vàng, túi kêu trơn
  có ba gợn ở mép dưới, sừng xoắn ngà vòng lam, áo choàng lá súng có khía, dây sậy chéo ngực + khoá vàng xoắn ốc, băng sậy cẳng tay,
  răng + hai nanh, vuốt sẫm, đệm ngón cam, không đuôi; khung 1248 × 702, lề ≥ 141 px; bốn chi tách nhau. Điểm yếu: khoé miệng cong
  lên hơi như cười nhếch; tờ đầu ở pha 2 dặn miệng mím quả quyết.
- `L1_concept.png`: cùng thiết kế, sừng to hơn, mặt cau dữ hơn; nhưng vẽ quá to (lề 52 px < 60 px dặn) và **túi kêu tròn vàng có
  xoắn ốc đen giữa ngực**, dễ gợi một dòng ếch nổi tiếng có bụng xoắn ốc, nên không chọn.
- File prompt `gui_gpt/tm03_2/luot_1_concept.txt` đã sửa theo bản chọn (túi kêu trơn có gợn, khung nhỏ hơn) để pha 2 dùng đúng mô tả.

Tờ so sánh: `inbox/tm03_2/so_sanh_concept.png` (hàng trên bản chọn, hàng dưới bản khác).

Khác con gốc: con gốc là quả bóng tròn ngồi im, không đuôi, mắt xoắn ốc hồng nhạt, lưỡi trắng có vằn buông trước mặt như mặt nạ,
xanh tím vằn tím, nhìn chéo. Dòng này: nòng nọc có **đuôi cuộn xoắn ốc** (chủ đề xoắn chuyển từ mắt sang đuôi), mắt hổ phách con
ngươi ngang, lưỡi nằm trong miệng, cerulean + vàng chanh + cam, đứng bốn chân nghiêng 3/4 sang phải; dạng 2 (con gốc không có) là
ếch sừng phục thấp có đồ (lá súng, dây sậy, sừng xoắn, túi kêu).

## 4. Dự kiến pha 2 (chỉ làm khi được báo "đã duyệt")

Cách dựng như Hải Long (`pokiclash-spine-rig` mục 20): concept làm mốc, GPT vẽ tờ mảnh rời vẽ đủ phần bị che, rig dựng bằng mã
(`ArtGen/Spine/tm03.py`), JSON Spine 4.2 → `.atomik`, lưới tam giác gần đều, trọng số B-spline cho chuỗi, hoà theo khoảng cách
đi trong hình cho vùng; tối đa 4 xương mỗi đỉnh.

**Dạng 1 (khoảng 32 xương):**
- Tờ M01 (thân, đầu): vòm đầu + lưng + môi trên (khoét chỗ mắt); hàm dưới + cằm + bụng; mảng lòng miệng hồng; lưỡi duỗi thẳng;
  mắt gần, mắt xa (tròn lồi, mí mở); hai mí nhắm; chân sau: đùi, cẳng, bàn chân màng; một chân trước tí hon (dùng lại hai bên).
- Tờ M02 (đuôi): **đuôi vẽ duỗi thẳng nằm ngang** (~1300 px, gốc mập bên trái, vây quanh, vằn lam đậm ngang). Xương 10 đốt dài
  ngắn dần ra ngọn; dáng nghỉ xoay cộng dồn 30° → 60° mỗi đốt thành xoắn ốc 2,5 vòng như concept; cuộn chặt / bung duỗi được
  (cast quất, skill quay chân vịt, hit sóng từ ngọn về gốc). Lưới dải 10 đốt, mỗi đốt hai cột 3 đỉnh, trọng số B-spline.
- Xương: root, move, body (nén giãn), belly (phồng họng: điểm phá nhịp như con gốc), head (vòm, ngửa khi há), jaw (bản lề góc
  miệng phía sau; lòng miệng bám hàm dưới), mieng (trục x chĩa phía trước), lưỡi 3 đốt (lò xo), eye_n, eye_f (nảy lệch pha), mí,
  tail1..10, chân sau 2 × (đùi, cẳng, bàn IK bám đất), chân trước 2.

**Dạng 2 (khoảng 48 xương):**
- Tờ M01 (đầu): đầu trên (sọ, mày, môi trên, răng trên); hàm dưới có răng dưới; lòng miệng; lưỡi duỗi thẳng; **túi kêu tách riêng**
  (tròn, để phồng bằng tỉ lệ); hai sừng xoắn rời; hai mí nhắm.
- Tờ M02 (thân, chi): thân (lưng + bụng, khớp vai, hông đầu tròn); chân trước vẽ liền cả chi gần / xa + bàn tay màng; đùi sau to,
  cẳng + bàn chân dài gần / xa.
- Tờ M03 (đồ): áo choàng lá súng vẽ trọn cả tấm (phần bị thân che cũng vẽ), dây sậy chéo ngực vẽ thẳng (dải để uốn), khoá
  vàng, hai băng dây sậy cẳng tay.
- Xương: root, move, hip, spine1..3, chest, neck, head, jaw, sac (tỉ lệ), mieng, lưỡi 4 đốt, sừng 2 (lò xo nhẹ), chân trước 2 ×
  (vai, cẳng, bàn IK), chân sau 2 × (đùi, cẳng, bàn IK), áo choàng lá súng lưới 3 × 2 xương (lò xo, mép lá gợn khi nhảy, đập),
  dây sậy 4 đốt, khoá cứng, băng sậy cứng theo cẳng tay.

**Clip** (mục 5 đặc tả; nhịp theo `skill-petclash` 7.1):
- `appear`: dạng 1 bật ra từ một bong bóng (khung đầu trống, tụ lại 0 → 1,1 → 1), đuôi bung từ cuộn chặt; dạng 2 nhảy vào khung
  đáp nặng, nện đất, ộp một tiếng (túi phồng). Kết thúc đúng khung 0 `idle`.
- `idle`: dạng 1 2,0 s: thở, nhún hai lần (học con gốc), đuôi cuộn / nhả nhẹ trễ pha, mắt nảy lệch pha, phá nhịp phồng họng 0,35 s
  + chớp mắt; dạng 2 2,4 s: thở nặng, túi kêu phập phồng nhỏ, dây tảo đung đưa, phá nhịp ộp nhẹ + chớp mắt.
- `attack`, `cast`, `skill`: theo bảng mục 2; dạng 2 lấy đà dài hơn, giữ chiêu rung hai dáng.
- `hit`: không lấy đà, đỉnh 0,07 s, đuôi / dây tảo sóng từ ngọn về gốc, mí nhắm.
- `die`: giật, nhắm mắt, lật ngửa bụng (ếch lật ngửa, chân duỗi), lưỡi thè, giữ một nhịp, tan; khung cuối trống.
- `evolve` (dạng 1): đuôi quay nhanh tạo lốc, cuộn chặt, gồng, đổi dạng lúc lốc đậm nhất, Ếch Lốc bật ra, ộp gầm, hoà về khung 0
  `idle` dạng 2.
- `aura` (tuỳ): dạng 2 vòng gợn nước nhỏ dưới chân chạy liền qua mọi clip.

Dung lượng đích ≤ 0,3 MB mỗi dạng (atlas bảng 256 màu, cạnh bội 8, lọc RDP, dùng lại hình: chân trước, mí, chân sau lật bằng tỉ lệ).

## 5. Pha 2 đã làm (2026-11-11, cách lai theo DAC_TA mục 5)

Lựa chọn (điều phối ủy quyền): dạng 1 `L1_duyet.png` (điều phối duyệt); dạng 2 gen lại lần cuối theo góp ý (không xoắn ốc trên thân,
sừng mí vuốt sau thay sừng cừu, lá súng lục lam, khoé miệng dữ) → **chọn `inbox/tm03_2/tai_ve/L1_concept_3.png`** (đạt cả danh sách).

Tệp:
- `ArtGen/Spine/build_tm03.py`: lượt 1 concept, lượt 2 tờ mảnh (`gui_gpt/tm03_<k>/luot_2_manh.txt`, HUONG_DAN cập nhật).
- `ArtGen/Spine/tm03_lai.py` (`nhan` bản đồ vùng trên concept, nét mực là tường; `cat`, `dat`, `lai` gọi `tm03_ghep.py`), chạy bằng
  `D:/spine-venv/Scripts/python -I` (cần cv2).
- `ArtGen/Spine/tm03_ghep.py`: cắt tờ GPT, dò mảnh GPT trên concept (SQDIFF, phủ kín có ràng buộc, khớp đường xoắn đuôi), dựng lớp
  thân cắt từ concept + vẽ bù, mí nhắm cắt theo đĩa mắt.
- `ArtGen/Spine/tm03.py`: rig, clip, xuất (`rig 1`, `rig 2`, `all` = dạng 2 rồi dạng 1 gộp tiến hóa). Chạy qua `quai/khoa.py nang`.
- Ra: `inbox/tm03_<k>/lai/` (lớp, bản đồ vùng), `inbox/tm03_<k>/manh/` (mảnh GPT), `inbox/tm03_<k>/rig/` (đủ bộ theo DAC_TA).

Dạng 1 Nòng Xoáy:
- Thân (quả bóng, mắt, môi) cắt từ concept, lỗ miệng đục; đáy bóng và chỗ chân che vẽ bù bằng quả bóng GPT khớp lại theo bóng dáng
  nửa dưới (IoU 0,92), dải đáy y > 742 lấy hẳn từ GPT, hoà 14 px trong vùng bụng vàng.
- Đuôi: ảnh GPT duỗi thẳng, lưới dải 24 đốt (1792 đỉnh), dáng gốc **cuộn theo đường xoắn khớp từ concept** (tối ưu ngẫu nhiên IoU +
  phạt khe giữa các vòng: 0,933), khớp chia theo góc quay; vòng trong vẽ đè vòng ngoài.
- Chân GPT ngắn mập (theo dặn), IK bám đất; chân sau xa dời phải 70 px cho hông nấp sau thân khi đuôi nhấc.
- Clip: appear 1,2 · idle 2,0 (nhún 2 lần, đuôi thở, phồng họng, chớp mắt) · attack 0,9 Bọt Nước (`trung` 0,42) · cast 1,1 Đuôi Xoáy
  (đuôi cuộn chặt, vung thành vòm qua lưng, quất ngọn ra trước trên đầu; `phun` 0,55, `het_phun` 0,85; `mieng` ở ngọn đuôi, trục x
  luôn chĩa phải) · skill 1,8 Xoáy Bong Bóng (nhún, nhảy tại chỗ, đáp `gam` 0,95, đuôi quay sóng nhanh, rung hai dáng) · hit 0,6 ·
  die 1,6 (lè lưỡi, lật ngửa ra sau, tan) · evolve 2,8 (đuôi quay tít, gồng, đổi dạng 1,27 s, Ếch Lốc ộp gầm).
Dạng 2 Ếch Lốc:
- Thân + đầu + lá súng + túi kêu + sừng một lưới cắt từ concept; hai chân gần cắt từ concept (lớp riêng); hai chân xa, lòng miệng,
  lưỡi, mí từ GPT; chỗ chân gần che vẽ bù từ "thân không chân" GPT (đúng phần lớp chân che, không nới, để lúc nghỉ không lộ).
- Clip: appear 1,4 (rơi xuống, đáp, ộp) · idle 2,4 (thở, túi kêu phập phồng 2 nhịp, lá súng, sừng lò xo, ộp nhẹ phá nhịp, chớp mắt) ·
  attack 1,0 Thủy Chưởng (lấy đà lùi, tay gần đẩy tới trước ngực, thân vươn ≤ 0,11 H; `trung` 0,46) · cast 1,3 Ộp Âm Ba (túi kêu
  phồng 1,5 lần, ngửa rồi há miệng ộp, rung hai dáng; `phun` 0,62, `het_phun` 1,02; `mieng` ở mép miệng) · skill 2,0 Đại Hải Lốc
  (chồm hai tay lên, đập xuống `gam` 0,98, gầm rung tới `het_gam` 1,5) · hit 0,7 · die 1,8 (túi xẹp, lè lưỡi, lả nghiêng, tan).

Lỗi đã gặp (ghi lại cho dòng khác):
- Ghép mảnh vá đáy bóng theo vùng chân nới ra: viền đáy thành bậc thang (GPT và concept lệch vài px). Sửa: khớp lại bóng GPT theo
  bóng dáng nửa dưới rồi lấy **cả dải đáy** từ một nguồn, hoà trong vùng màu phẳng.
- Đuôi cuộn khớp IoU cao nhưng có khe trắng giữa các vòng và tâm xoắn bé tí bị gãy thành đa giác: thêm phạt lỗ kín, giới hạn bán kính
  trong, tăng số đốt và chia khớp theo góc.
- Vung đuôi bằng một xương gốc: cuộn đuôi chui ra sau thân (slot đuôi sau thân). Sửa: duỗi một phần cuộn + vung gốc ~ −65° thành vòm
  qua lưng (thử nhiều cặp góc trên một ảnh trước khi viết clip).
- Lòng miệng chỉ phủ vừa lỗ: há miệng lộ khe xám trên môi trên. Sửa: phủ thêm 28–45 px phía trên lỗ (nấp sau môi trên), hàng trên
  hoà một phần vào đầu.
- Dạng 2: vá thân quanh chân gần nới 10 px thì vòng vá **lộ ngay lúc nghỉ**; lớp chân thiếu nét viền (mực bị gán cho thân) và có khe
  vụn bên trong. Sửa: lớp chân giữ mực trong 4 px, đóng 5×5 + lấp lỗ + nới 2 px; thân chỉ thay đúng phần lớp chân che.
- IK tay với đích ngoài tầm: tay gập nát. Đích chưởng phải trong tầm với (≈ tổng hai đoạn).
- Chuỗi thay chữ trong mã dùng `str.replace` trúng cả hai dạng có đoạn giống hệt: dạng 2 dùng xương lạ `than`.
- Bản gộp tiến hóa mang nguyên dạng 2 độ phân giải đầy đủ: .atomik 0,57 MB vượt trần. Sửa: bản gộp thu 0,7, lưới thưa 1,5 lần.
