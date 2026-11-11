# Ghi chú dòng tm07: Liên Kình (cá kỳ lân biển mang hoa sen), ải 40 đảo Thủy (thay Kuba, epic)

Agent dòng 7 (Fable), lô 10 tướng mới đảo Thủy 2026-11-11. Đặc tả chung: `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`.
Con tham khảo: `monster_3244` (Sword x Staff), là **dạng 2** của dòng; quét ở `D:\RefAnimation\SwordxStaff\scan\monster_3244\`.
Chỉ học cấu trúc và nhịp; hình, màu, diễn xuất là của mình, không đính ảnh con gốc vào prompt.

## 1. Mổ xẻ con gốc (đọc `info.json`, `keys.json` bằng `mo_xe/nhip.py`)

### 1.1 Số tổng

| | |
|---|---|
| File | `.skel` Spine 4.2.28 + atlas một trang 448 × 304 (xuất tỉ lệ 0,75), tổng 0,2 MB |
| Xương | 62 (root, all, shadow, xy, 58 xương thân) |
| Slot | 24 (1 lưới chữ nhật `wangge`, 1 bóng, 22 mảnh hình); mọi mảnh là lưới có trọng số, không mảnh cứng |
| Lưới | 329 đỉnh; thân 51 đỉnh / 7 xương, đuôi 31 / 7, mỗi vây 18 / 4, mỗi cánh sen 10–14 / 2–3, mắt và sừng 4 đỉnh |
| Ràng buộc | không IK, không transform, không path, không physics |
| Clip | 10: block 0,5; die 1,0; floating 1,5; hit_01 0,5; hit_02 0,67; idle 1,33; run 0,53; skill_01 1,17; skill_02 1,63; stun 1,33 |
| Sự kiện | không |

### 1.2 Cắt mảnh (22 ảnh)

| Nhóm | Ảnh | Là gì | Bám xương |
|---|---|---|---|
| Thân | `P_shenti` 242 × 185 | cả thân từ gáy tới gốc đuôi, có cả đầu (đầu KHÔNG tách rời thân) | bone22, bone42, bone43, bone14, bone21, tou, bone23 |
| Đuôi | `P_weiba` 123 × 153 | đuôi + vây đuôi dưới | bone43, bone44, bone14..bone18 (chuỗi 7) |
| Vây | `P_chibang1..4` | bốn vây (hai vây ngực, hai vây lưng/bụng) | mỗi vây một chuỗi 4 đốt riêng |
| Miệng | `P_bizui` (ngậm) / `P_zhangzui` (há) | **hai ảnh miệng thay nhau** chứ không có xương hàm; lòng miệng vẽ sẵn trong ảnh há | bone24, bone25 dưới `tou` |
| Mắt | `P_yanjing1` (thường) / `P_yanjing2` (đau) | hai ảnh mắt thay nhau (chớp, nhắm khi trúng đòn) | tou |
| Sừng | `P_jiao` | mảnh chữ nhật, 1 xương | jiao (con của tou) |
| Sen | `P_huaban1..10` + `P_huarui` | 10 cánh rời + 1 nhụy, mỗi cánh một xương gốc + một xương ngọn (`boneNb`) | bone2 (gốc sen) → bone3..13 → bone*b |

Cách cắt đáng học: **mỗi cánh sen là một mảnh riêng có chuỗi 2 đốt** (gốc, ngọn) nên hoa "thở" được và từng cánh rung lệch pha;
**bốn vây mỗi vây một chuỗi 4 đốt** (vây mềm trễ theo thân). Chỗ yếu: đầu dính thân (không quay đầu riêng), miệng há bằng đổi
ảnh (không có xương hàm, không mềm), sừng chỉ 1 xương chữ nhật.

### 1.3 Xương: cây và vai trò

```
root > all > xy > bone (gốc thân, xoay cả con)
  ├─ bone22 > bone42 > bone43 > bone44 > bone45 > bone14 > bone15 > bone16   chuỗi sống lưng → đuôi (7 đốt tới vây đuôi)
  │                              └─ bone48 > bone17 > bone18                   nhánh vây đuôi phụ
  │        ├─ bone30..33 (vây 1), bone34..37 (vây 4)                           hai vây chuỗi 4 đốt mọc từ thân sau
  ├─ bone21 > tou > bone24 > bone25 (miệng), jiao (sừng)                       đầu
  ├─ bone2 > bone3..13 > bone*b                                                sen: 1 gốc, 10 cánh × 2 đốt
  ├─ bone26..29 (vây 2), bone38..41 (vây 3)                                    hai vây chuỗi 4 đốt mọc từ gốc thân
  └─ bone23                                                                    điểm phụ của thân (cằm/cổ)
```

### 1.4 Nhịp từng clip (đọc khoá thật)

| Clip | Dài | Diễn gì, khoá ở đâu |
|---|---|---|
| `idle_01` | 1,33 s (40 khung) | 100% bezier, **mỗi xương đúng 2 cực trị một vòng**. Chuỗi thân khoá lệch khung: bone22 ở 11/31, bone42 ở 1/21, bone43 ở 11/31, bone44 ở 21, bone14 ở 1/21, bone15 ở 6/26, bone16 ở 11/31 → sóng chạy dọc thân ra đuôi. Biên độ thân 6–9°, đuôi 12–19°. Đầu `tou` chỉ −5 → −1° (gần đứng yên). 10 cánh sen mỗi cánh 4 khoá, rung lệch pha. Không có điểm phá nhịp (không chớp mắt) |
| `skill_01` (đòn) | 1,17 s | 71% thẳng. 0 → 0,30 s: cả con ngả ra sau và nhấc lên (gốc dời −76, +113; xoay +31°), đuôi quật ngược (bone14 94° → 117° ở 0,43); **0,43 → 0,47 s (1 khung): bổ xuống**, gốc xoay 31 → −4°, đầu −14 → +20°, đuôi 117 → 67°; giữ có trôi tới 0,83; về bằng khoá bậc ở 1,17. Đúng mẫu "lấy đà ngược chiều → chạm 1 khung → giữ có trôi → về" |
| `skill_02` (chiêu) | 1,63 s | 91% thẳng. Gốc thân **xoay 0 → 430° (lộn một vòng)** trong 0,8 s kèm vòng tròn dời (bán kính ~200); miệng há 0 → 0,83 s rồi ngậm; **gốc sen `bone2` tách khỏi lưng** (dời 139, xoay −137°) rồi ở 0,83–0,87 s bay vọt đi (dời −364) và co về 0,1 ở 1,27 s; 10 cánh mờ dần 0,13 → 1,63. Tức là: lộn người ném cả bông sen làm đạn, hoa hiện lại khi về idle. Ta **không** lộn (đòn lộn đã bị người dùng bỏ), nhưng ý "sen là vũ khí" giữ lại theo cách khác (xem mục 3) |
| `hit_01` | 0,5 s | khung 0 đã là dáng bị đánh (bone22 +28°, không lấy đà), đổi ảnh mắt thường → mắt đau suốt 0 → 0,43; sóng chạy ngược: bone42 đỉnh 55° ở 0,07, bone43 đỉnh 51° ở 0,17, bone44 đỉnh 23° ở 0,33; về bằng khoá bậc ở 0,5 |
| `hit_02` | 0,67 s | như hit_01, dài hơn một chút |
| `die_01` | 1,0 s | 0 → 0,37 s: vọt lên 300 đơn vị, xoay 67° (ngửa bụng); 0,37 → 0,63: rơi xuống −61; 0,63 → 1,0: cánh sen mờ dần; miệng há suốt. Không có đoạn "lả đi giữ một nhịp" |
| `block`, `floating`, `run`, `stun` | | không cần cho game ta |

Kết luận lấy sang: idle hai khoá một vòng lệch khung theo chuỗi; đòn bổ 1 khung + giữ có trôi; trúng đòn không lấy đà, sóng ngược
từ ngọn về gốc; mỗi cánh sen một chuỗi riêng lệch pha; vây chuỗi 4 đốt. Cái ta làm khác: đầu tách khỏi thân (xương cổ 2 đốt), hàm
dưới là xương thật (há theo nhịp, lòng miệng đi theo hàm), mí mắt là mảng phủ, chết có đoạn lả đi, có đệm nước chạy vòng lặp
riêng, sự kiện cho VFX.

## 2. Thiết kế dòng

**Tên dòng: Liên Kình** (sen + cá voi). Dạng 1 **Kình Nụ**, dạng 2 **Liên Kình**. Danh hiệu: "Kình ngư cõng sen thiêng".

Lore: giống cá voi một ngà sống ở đầm sen dưới đáy biển; nụ sen trên lưng mọc từ lúc mới nở, nở bung khi con vật trưởng thành;
ngà vàng mọc dài theo tuổi, là "thương" của nó. Thú nuôi kiểu Pokémon: quả quyết, gan lì, không linh vật.

| Vùng | Dạng 2 Liên Kình (dạng cuối, epic, làm trước) | Dạng 1 Kình Nụ (bé con, chibi) |
|---|---|---|
| Lưng, sườn | chàm `#3A4A9C` | lam phấn `#8FA7E6` |
| Bụng, cổ họng | ngà `#F4ECD8`, 4–5 rãnh họng | kem `#F7F0DF`, 2–3 rãnh |
| Sen | nở to bằng đầu: cánh ngoài đỏ thắm `#D9443A`, cánh trong hồng `#EE8A80`, đài vàng `#E8B64A` | nụ khép cao nửa đầu: hồng nhạt `#F3B5AE`, chóp đỏ, đế chàm |
| Ngà | dài bằng bề ngang đầu, vàng `#E8B64A`, rãnh xoắn mực | cụt một phần ba đầu, vàng nhạt `#F1D27A` |
| Phụ kiện | mào trán vàng hình cánh sen, 3 vòng vàng gốc đuôi | một chấm vàng trên trán |
| Vây, đuôi | vây chèo to viền đỏ, vây lưng cao vuốt sau, vây đuôi xoè hai thuỳ chóp đỏ, sọc ngà dưới | vây bé, vây đuôi nhỏ, dải đỏ mỏng |
| Mắt | hẹp, sắc, mống cyan `#45CFE0` | to tròn, mống cyan, mày cau |
| Miệng | hé, răng nhọn nhỏ hai hàm, lòng miệng đỏ rượu `#8B2F45` | hé, hai răng nhọn tí |
| Nước | đệm sóng thấp dưới bụng (1/5 ảnh), ba lam `#1E68BE` `#3A96E2` `#8CD0F6`, bọt trắng | vũng tròn nhỏ (1/6 ảnh) |
| Tỉ lệ | đầu ~1/4 thân, thân dài chữ S nhẹ, ngực ngẩng | đầu ~45%, thân hạt đậu |

Khác con gốc ở đâu: con gốc xanh ngọc có vân xoắn sáng, bụng trắng, sen hồng phấn, sừng xám, mắt bé kiểu chibi, bốn vây lá. Của
mình: chàm + ngà + đỏ thắm + vàng (không màu nào trùng), không vân xoắn, ngà vàng xoắn kiểu kỳ lân biển thật, sen đỏ nở có đài
vàng, mào trán và vòng vàng kiểu giáp, mắt hẹp quả quyết, răng nhọn, vây viền đỏ, vây lưng cao, có đệm nước. Dạng 1 là nụ sen khép
+ ngà cụt + màu nhạt + chibi, con gốc không có dạng này.

So với 13 tướng Thủy đang có: không trùng Vây Lam (lam hoàng gia + cyan), Thương Lam (băng), Kuba (cam đỏ + pha lê băng), Ma Kết
(lục + trắng + cam), Tám Tay (vàng cam + vòng lam), Hải Long (xanh ngọc + kem vàng + san hô), Lam Quân (đồng), Cánh Cụt (băng
trắng). Màu đỏ thắm của sen là điểm nhận diện; chàm lệch tím nên không lẫn lam.

## 3. Đòn, chiêu từng dạng (đứng tại chỗ; rig chỉ để chỗ bám, VFX lớp sân làm sau)

| | Dạng 1 Kình Nụ | Dạng 2 Liên Kình |
|---|---|---|
| `attack` đòn thường | **Phun Nước (Water Gun)**: lùi nhẹ, há miệng phụt một viên nước nhỏ; sự kiện `trung` lúc đạn rời miệng, xương `mieng` | **Ngà Thương (Horn Attack / Razor Shell)**: cổ rụt lấy đà 0,3 s rồi đầu + ngà đâm tới trong 1 khung (giãn ngà 1,15), bay ra một lưỡi nước hình lưỡi liềm từ mũi ngà; xương `mui_nga` ở chóp ngà cho VFX; giữ có trôi, về |
| `cast` chiêu bắn | **Bong Bóng Sen (Bubble)**: ngửa đầu tụ, há miệng nhả 3 bong bóng có cánh sen; `phun`, `het_phun` | **Thủy Pháo (Hydro Pump)**: ngực nén, hàm há to, luồng nước dày từ miệng 0,9–1,2 s, thân rung hai dáng, sen rung theo luồng; `phun`, `het_phun`, xương `mieng` trục x chĩa hướng nhả |
| `skill` chiêu cuối | **Nụ Bung (Petal Blizzard nhỏ)**: nụ sen trên lưng phồng lên 0,5 s rồi bật mở ngắn, bắn cánh hoa rơi như mưa lên đối thủ (kiểu `rain`), nụ khép lại; sự kiện `bung`, `het_bung`; xương `nu` | **Liên Hoa Hải Triều (Surf + Petal Blizzard)**: ngẩng cao, sen xoè hết cỡ 0,6 s (từng cánh mở lệch pha), đuôi quật xuống đệm nước → sóng lớn mang cánh sen đỏ dâng dưới đối thủ (VFX `vortex`/`wave` + cánh hoa rơi); thân gồng rung hai dáng, há miệng gầm; `gam`, `song`, `het_gam`; xương `sen` (tâm đài) và `duoi` cho VFX bám |
| `hit` | bật lùi, mắt nhắm (mí), sóng ngược thân → đuôi, nụ lắc | như trên, ngà chúi xuống, cánh sen rung mạnh |
| `die` | giật, nhắm mắt, lả đi ngửa bụng giữ một nhịp, nụ héo cụp, chìm vào vũng, nước tan | giật, nhắm mắt, lả đi, cánh sen rụng từng cánh (mờ dần lệch giờ), đổ nghiêng xuống đệm nước toé, chìm, nước tan |
| `evolve` (dạng 1) | gồng, nụ sen phồng to, lốc nước bọc; đổi dạng lúc lốc đậm nhất; dạng 2 bung sen nở, gầm | |
| `aura` | vũng nước lăn tăn, 2 cuộn nhỏ lệch nửa chu kỳ | đệm sóng chạy liền, 3–4 cuộn + dải gợn; cánh sen khẽ rung |

Idle dạng 2: thân uốn sóng 2 khoá một vòng lệch khung ra đuôi (học con gốc), vây chèo trễ 0,06 s, cánh sen mỗi cánh một pha,
đầu gần đứng yên (mắt nhìn địch); điểm phá nhịp 62–72%: chớp mắt + táp miệng nhẹ. Idle dạng 1: nảy nhỏ (nén giãn 3%), nụ lắc,
chớp mắt đôi.

## 4. Dự kiến pha 2: tờ mảnh và xương

### 4.1 Tờ mảnh GPT (mỗi tờ 1536 × 1024, mảnh rời, vẽ đủ phần bị che)

Dạng 2:
- **M01 đầu**: phần trên đầu (sọ, mày, mào trán, hàm trên có răng; KHÔNG ngà, KHÔNG hàm dưới; gáy vẽ dư để chồng lên cổ); hàm
  dưới rời có răng + dải lòng miệng; mảng lòng miệng; mí mắt nhắm (mảng chàm có nét cong); ngà vẽ rời **thẳng nằm ngang**; mắt
  mở riêng (để chớp bằng đổi hình nếu cần).
- **M02 thân**: thân từ gáy tới gốc đuôi vẽ **duỗi thẳng nằm ngang** (lưng chàm, bụng ngà, rãnh họng, ba vòng vàng), hai đầu tròn;
  đuôi duỗi thẳng rời; vây đuôi xoè rời; vây chèo gần, vây chèo xa (một ảnh, lật); vây lưng.
- **M03 sen**: hàng cánh sau (5 cánh rời), hàng cánh trước (5 cánh rời), đài vàng, 3 cánh rơi rời cho chiêu (có thể để VFX).
- **M04 nước**: dải đệm sóng dài đáy phẳng, 3 cuộn sóng (to, vừa, nhỏ), cụm bọt, vương miện nước toé, 3 giọt, vòng sóng dẹt
  (dùng lại hình sóng của Hải Long `inbox/hai_long/manh/` nếu hợp màu, đỡ gen).

Dạng 1: **M01** đầu to (sọ + hàm trên, hàm dưới rời, lòng miệng, mí nhắm, ngà cụt rời); **M02** thân hạt đậu + đuôi + vây đuôi +
vây chèo + vây lưng; nụ sen: đế chàm, 2 lớp cánh khép rời (để "bung" được), 3 cánh rơi; vũng nước tròn + 2 cuộn nhỏ + giọt.

### 4.2 Xương (ước)

| Nhóm | Dạng 2 | Dạng 1 |
|---|---|---|
| gốc: `root`, `move`, `than` | 3 | 3 |
| sống lưng `sl1..5` (ngực → gốc đuôi) + đuôi `du1..4` + vây đuôi `vd` | 10 | 7 (sl 3, du 3, vd 1) |
| cổ `co1..2`, đầu `dau`, hàm `ham`, ngà `nga` (+ `mui_nga`), `mieng` (VFX), mí (slot) | 7 | 6 |
| vây chèo gần, xa: mỗi vây 3 đốt | 6 | 4 (2 đốt mỗi vây) |
| vây lưng 2 đốt | 2 | 1 |
| sen: `sen` (đài) + 10 cánh × 2 đốt | 21 | nụ: `nu` + 2 lớp cánh × 1 = 3 |
| nước (nhóm riêng, không con của thân): dải 6 xương + 3 cuộn × 3 đốt + toé | 17 | 10 |
| **Tổng** | **≈ 66** (con gốc 62) | **≈ 34** |

Lưới: thân dải 2 cột mỗi đốt, trọng số B-spline (`quai/` khi có); hàm dưới lưới hai xương (cổ họng bám cổ sát đầu, nửa trước bám
hàm); lòng miệng bám hàm (hàng dưới 100%, hàng trên hoà về đầu ở bản lề); mỗi cánh sen lưới 3 × 4 bám chuỗi 2 đốt; vây dải 3 đốt.
Dung lượng đích ≤ 0,3 MB mỗi dạng: atlas 256 màu, cánh sen dùng lại 2–3 hình lật/xoay, sóng dùng lại.

## 5. Nhật ký pha 1

- 2026-11-11: đọc đặc tả, skill, mổ con gốc; viết `build_tm07.py`; gen concept dạng 2 lần 1 (xem mục 6 khi có kết quả).

## 6. Kết quả concept

### Dạng 2 Liên Kình: `inbox/tm07_2/tai_ve/L1_concept.png` (đã chọn, chép thành `L1_duyet.png`), 1 lần gen (01:19)

Soi: quay phải, đầu ngẩng, thân chữ S nhẹ, vây đuôi xoè trọn ở trái; ngà vàng xoắn đứng rời; sen đỏ nở hai lớp cánh + đài vàng
đứng giữa lưng không đè đầu/đuôi; vây lưng viền đỏ bên trái sen, vây chèo xa ló sau lưng bên phải sen; miệng hé thấy lòng đỏ rượu
và răng nhọn hai hàm, hàm dưới là hình riêng; mắt hẹp cyan một chấm sáng, mào trán vàng; thân chàm, bụng ngà có rãnh họng, không
vân xoắn; ba vòng vàng gốc đuôi; đệm sóng thấp ba lam + bọt, giọt bay; tô phẳng, nền trắng, không chữ.
Điểm chưa như dặn: **vây chèo gần đè lên bụng** (không có khoảng trắng tách) — chấp nhận vì pha 2 vẽ tờ mảnh rời, concept chỉ
làm mốc; khi lấy mốc từ concept phải vẽ bù phần bụng sau vây. Ngà hơi dài hơn bề ngang đầu (đẹp, giữ).

### Dạng 1 Kình Nụ: `inbox/tm07_1/tai_ve/L1_concept.png` (đã chọn, chép thành `L1_duyet.png`), 1 lần gen (153 s)

Soi: chibi thân hạt đậu, đầu chiếm gần hết thân, quay phải; mắt to tròn cyan, mày cau, miệng hé hai răng nhọn + lòng đỏ rượu;
ngà cụt vàng nhạt có nét xoắn; nụ sen **khép** hồng nhạt chóp đỏ trên đế chàm, vây lưng nhỏ viền đỏ sau nụ; vây đuôi nhỏ xoè trọn
bên trái; vây chèo gần nhỏ viền đỏ đè lên bụng; bụng kem có rãnh; vũng nước tròn nhỏ ba lam + bọt, hai giọt; màu lam phấn nhạt hơn
dạng 2 rõ; tô phẳng, nền trắng. Nhận ra cùng dòng với dạng 2 (ngà, sen, cyan, viền đỏ, bụng ngà).
Thiếu nhỏ (pha 2 vẽ bù trên tờ mảnh): không thấy vây chèo xa; không có chấm vàng trên trán.

Cả hai dạng đạt ngay lần gen đầu nên không gen bản khác (tiết kiệm hạn mức Codex chung của 10 dòng); người dùng muốn bản khác
thì `py -3 -I gen.py gui_gpt/tm07_<k>/luot_1_concept.txt --note "..."` (câu sửa nhanh ở `gui_gpt/tm07_2/HUONG_DAN.md`).

Pha 1 dừng ở đây (chưa gen tờ mảnh, chưa rig), chờ người dùng duyệt concept.

## 7. Pha 2 (bắt đầu 2026-11-11 02:00, concept đã duyệt)

Tệp: `tm07.py` (cắt tờ, rig hai dạng, 8 clip + aura, tiến hóa gộp, soi), `tm07_khop.py` (khớp mảnh vào concept tự động),
`build_tm07.py` (thêm tờ mảnh M01–M03 dạng 2, M01–M02 dạng 1). Nước: dùng lại mảnh sóng đã cắt của Hải Long
(`inbox/hai_long/manh`: wave_a/c/d/e, curl_s1..3, foam, band, drop) nên không gen tờ nước.

### Cách dựng dạng 2
- Thân: tờ GPT vẽ ống **duỗi thẳng** (M02), `luoi_dai` 6 đốt (58 cột × 14 hàng) rồi **uốn theo đường cong Catmull-Rom** đọc từ
  concept (`duong`, `uon_dai`); xương: `than` ở ngực, chuỗi `bk0..3` về gốc đuôi, `fw0..1` tới gáy; trọng số B-spline theo s.
  GPT hai lần vẫn vẽ ống dài mảnh (1444 × 347 thay vì 1000 × 420) → co dày riêng `ky` cho dày gáy = 360 px concept (`DAY_THAN`),
  và cắt nắp ống (đĩa ngà GPT vẽ ở hai đầu, `cat_nap`), cuống vẽ đè lên thân.
- Cuống đuôi: dải 3 đốt uốn theo đường từ gốc đuôi tới chân vây đuôi (vị trí vây theo khớp tự động); vây đuôi mảnh cứng.
- Đầu: lưới vùng (gáy hoà vào `fw1`), **hàm dưới neo ở khoé miệng của đầu**: hình hàm GPT vẽ chếch sẵn ~10° nên góc đặt = góc
  bản lề→mõm − độ chếch; tỉ lệ hàm = dài miệng / dài hàm trong hình; hàm lưới hai xương (`ham_hai_xuong`), lòng miệng theo hàm
  (`long_mieng`, duoi −0.34), mí `fit_lid` còn hở 0 px. Ngà mảnh cứng trên xương `nga` + `mui_nga` (VFX lưỡi nước liềm), `mieng`
  trục x chĩa hướng nhả, `lo_tho` cho tia nước lỗ thở (slot `phun_lo` ẩn, hiện ở điểm phá nhịp idle).
- Sen: hàng cánh sau = 1 lưới, 5 cột trọng số `vung` = 5 xương `cs0..4` (chân cánh hoà về `sen`); hàng trước 4 xương `ct0..3`;
  đài mảnh cứng; 3 cánh rời (`cr0..2`, ẩn) bay ra lúc chiêu cuối và chết.
- Vây chèo gần/xa cùng một hình (dải 3 đốt, LoXo); vây lưng lưới vùng + `chuoi_chieu` 2 đốt.
- Nước: nhóm xương `nuoc > song` riêng; 8 cuộn sóng × 2 bản sao lệch nửa chu kỳ (chuỗi 4 đốt trên sống lưng `SPINES`, trọng số
  B-spline × độ gần), dải nước trước 8 xương nhấp nhô, 4 giọt; mặt nạ cắt ở y = 34 cho thân chìm/trồi; clip `aura` 3,2 s.

### Khớp mảnh vào concept (`tm07_khop.py`, theo yêu cầu Claude điều phối)
Phân lớp màu (làm mờ hộp 2 px trước để gộp vân chì sáp), tương quan FFT theo từng lớp cho mọi (tỉ lệ × góc) quanh ước lượng,
điểm = độ chính xác tô (trừ phạt rơi vào nền) + tỉ lệ nét mực trùng nét concept (giãn 1 px) − tiên nghiệm yếu; thô 1/4 rồi tinh
1/2. Tự kiểm bằng vùng cắt từ chính concept (co 1,6, xoay −9°): tìm lại s 0,614 / 0,625, r 8° / 9°, tâm lệch 1 px.
Mảnh chồng cùng màu (các lớp sen, hàm) dễ trôi → khoá cửa sổ hẹp quanh ước lượng và canh các lớp sen theo tâm đài; thân, cuống lấy
tỉ lệ theo độ dài đường cong (không theo khớp). Kết quả `inbox/tm07_2/khop.json`, `so_ghep.png`.

### Số đo dạng 2 (lần 4, 03:10)
135 xương · 40 slot · 3475 đỉnh · 5298 tam giác · 8 clip · 7350 khoá · `.atomik` 367 KB (json 531 + png 238, atlas 944 × 984,
SC 0,72) — dưới trần 0,5 MB, trên đích 0,3 MB (nước chiếm phần lớn: 16 cuộn + dải). Nối clip trên đỉnh lưới đã da hoá (gồm lò
xo): appear/attack/cast/skill/hit về khung 0 idle 0,00 px, idle khép vòng 1,03 px, die khung cuối trống. `.atomik` nạp lại lệch
khung 0 0,07 px, giữa clip ≤ 3,2 px (RDP). Mí còn hở 0 px. IoU mặt nạ khung 0 idle / concept = 0,61 (xem mục 8).
Runtime Spine thật (`spine_that/*.jpg`, qua khoá chrome) dựng y như bộ vẽ Python.

### Dạng 1 Kình Nụ (tờ M01, M02 về 03:22; rig xong 03:55)
- Cắt tờ, khớp tự động: đầu, thân, nụ, vây, ngà. Mảnh cùng màu lam phấn (đầu, thân) khớp trôi → khoá cửa sổ hẹp quanh ước lượng từ
  concept; thân đặt theo concept (lưng đỡ nụ ở y≈330, bụng 780), hạt đậu GPT vẽ dài hơn concept nên kéo cao 1,2; hàm bé tỉ lệ 1,6 dài
  miệng (miệng bé rất nhỏ). Mí: mặt nạ mống cyan (`mat_cyan`, cyan (69,207,224) mà không dính da lam phấn) → còn hở 0 px.
- Rig: thân lưới vùng 3 vùng (hong, than, nguc) + đầu lưới vùng (gáy hoà `nguc`), cuống đuôi 3 đốt uốn cong tới chân vây đuôi, vây chèo
  2 đốt, vây lưng 2 đốt, nụ: đế + 2 lớp cánh (xương `nu_s`, `nu_t` tách ra khi bung) + 3 cánh rời; nước 6 cuộn × 2 + dải + giọt.
- Tiến hóa: `tienhoa.gop` (slot mặt nạ phải đặt trên xương riêng `goc_cat`, không trên root, vì gop đổi root dạng sau thành `evo`);
  dạng 2 trong rig gộp dựng lại với ảnh co 0,5 (`SC_GOP`), nước thưa, lưới thưa 1,25 (trừ cánh sen) vì chỉ hiện ở clip evolve 2,8 s;
  ảnh nước luôn nạp ở một tỉ lệ để hai dạng dùng chung vùng atlas (xương bù tỉ lệ `he`). evolve: dạng 1 gồng (nụ phồng 60 %, ngửa,
  há), đổi dạng 1,27 s, dạng 2 hiện 1,12–1,45 s, gầm + sen xoè 2,0 s, hoà về khung 0 idle dạng 2 lệch 0,00 px.

### Số đo cuối (04:00)
| | dạng 2 Liên Kình | dạng 1 Kình Nụ (rig gộp tiến hóa) | con gốc 3244 |
|---|---|---|---|
| xương / slot | 136 / 40 | 226 / 72 (gồm dạng 2 co) | 62 / 24 |
| đỉnh / tam giác | 5228 / 8507 (thân 2872, nước 2308) | 8286 / 13573 (thân 2946) | 329 / 322 |
| đỉnh thân / chiều cao | 5,35 (cao 536, bước 8 / 10,7) | 7,03 (cao 419, bước 6,3 / 8,4) | |
| khoá | 6116 | 6721 | 4214 |
| `.atomik` | 412 KB (json 661 + png 237, atlas 944 × 984) | 507 KB (json 935 + png 252, atlas 992 × 992) | 190 KB |
| hở lưới | 0 px mọi mảnh | 0 px mọi mảnh | |
| mí | hở 0 px | hở 0 px | |
| nối clip (đỉnh lưới, có lò xo) | 0,00 px mọi clip; idle khép 1,03 px; die trống | 0,00 px; idle khép 0,44; evolve 0,00 | |
| `.atomik` nạp lại | khung 0 lệch 0,07 px; giữa clip ≤ 7,8 px (RDP tol 0,3° / 0,6) | 0,09 px; ≤ 2,7 px | |
| IoU khung 0 idle / concept | 0,617 | 0,736 | |
Cả hai dưới trần 0,5 MB, trên đích 0,3 MB (nước dùng lại kiểu Hải Long chiếm ~45 % đỉnh; rig dạng 1 gánh thêm dạng 2 cho evolve).

IoU chưa tới 0,85: (1) nước là đệm sóng dựng bằng mảnh Hải Long (cao, rộng hơn vũng trong concept: cố ý để sóng chạy); (2) dạng 2:
GPT hai lần vẽ ống thân dài mảnh (1444 × 347) dù dặn 1000 × 420 → thân uốn theo đường cong concept nhưng mỏng hơn ở giữa (đã co dày
riêng gáy 360 px); sen đứng trên lưng bị thân che chân nên nhỏ hơn concept; (3) dạng 1: bóng dáng khớp (0,74), lệch còn lại là nước và
chỗ nối thân – đầu. Lượt gen M02 lần 3 (prompt ghi "ngắn mập, dài gấp 2,5 lần dày") vẫn đang xếp hàng Codex lúc viết; về thì
`cat 2` + `tm07_khop.py 2` + `all` dùng được ngay.

### Đã soi / chưa soi
Đã xem: tờ khung 8 clip + evolve (bộ vẽ Python) cả hai dạng; cận miệng há (cast, skill), ngà lúc đâm, mí lúc trúng đòn, khớp đuôi,
sen lúc chiêu, vây idle; `luoi.png`, `uon_thu.png`; runtime Spine thật (`spine_that/*.jpg`: dạng 2 idle/attack/cast/skill/hit,
dạng 1 idle/evolve/skill/attack) khớp bộ vẽ. Chưa xem ở tốc độ thật (chưa mở `xem.html`), chưa chạy trong Unity.

Còn lại / nên sửa: khớp mảnh cùng màu chồng nhau vẫn phải khoá cửa sổ tay; thân dạng 2 muốn đúng concept cần tờ M02 vẽ đúng tỉ lệ;
lòng miệng dạng 1 nhỏ (miệng bé); vây đuôi dạng 1 nối với cuống ngắn hơi lộ khe khi quẫy mạnh.

## 8. Làm lại theo CÁCH LAI (Claude điều phối trả lại 04:10; xong 05:40)

Lý do trả: so_concept dạng 2 IoU 0,617 — thân thành ống thẳng đầu cụt, cuống rời có khe, vây như que, sen bị che chân, đầu gắn vào ống.
Cách mới (`tm07_lien.py` cắt, `tm07_dung.py` dựng; tm07.py chỉ còn clip, nước, xuất):
- **Thân chính cắt thẳng từ concept** thành MỘT mảnh liền: thân + đầu + cuống + vây đuôi + vây lưng (+ lỗ ngà, lỗ hàm). Vùng = lớp
  màu (bảng màu dòng, làm mờ 1 px) + đa giác đọc trên concept kẻ lưới; nét mực lấy nhãn gần nhất (giãn lặp 12 px); nước = lớp lam +
  bọt trắng dưới mặt nước (+ hộp giọt), nới 5 px. Vụn < 3000 px (thân) / < 300 px (mảnh) bỏ.
- Cũng cắt từ concept (concept vẽ đủ): ngà, hàm dưới, vây chèo gần, vây chèo xa (phần ló), hai lớp sen + đài (dạng 1: đế nụ + nụ).
  GPT chỉ còn: mí mắt, 3 cánh rời, tia lỗ thở, lớp cánh nụ phụ (dạng 1, chỉ hiện lúc bung). Lòng miệng: tô đỏ rượu thẳng vào lỗ hàm +
  lỗ miệng của mảnh thân (há hàm là lộ đúng hình lỗ, không tràn ra ngoài mõm như mảng GPT sau thân); mảng GPT nhỏ chỉ dự phòng.
- Chỗ khuất vá bằng ô vân lát lấy từ chính concept (lưng / bụng theo đường ranh), kẻ lại nét mực ở mép vá; không loang màu.
- Lưới thân: `luoi_vung` bước 8 / 10,7 (dạng 2) và 6,3 / 8,4 (dạng 1) = 1,5 % / 2 % chiều cao; trọng số = vùng mềm (ngà, đầu, vây
  đuôi, cuống, vây lưng, thân; `trongso.vung` hoà 34–60 px) × chuỗi B-spline chiếu lên sống lưng (6 đốt), cuống (3 / 2 đốt), vây
  lưng (2 đốt) (`chuoi_chieu`) → thân uốn liền như cá bơi (`uon_thu.png`), không khe ở cuống, đầu liền thân.
- Idle: mọi dao động trừ giá trị tại t = 0 (`song0`, `song_than`) để khung 0 idle = dáng gốc (IoU đo ở khung 0 idle).
- Nước thu về cỡ concept (`NUOC_HE` 0,88 / 0,68); dạng 1 là vũng nhỏ.
- Lỗi đã gặp: `tm07_khop.lop` dùng int16 nên bình phương hiệu màu tràn (trắng thành "đỏ", nước thành thân) → int32; mép sóng khử răng
  cưa lẫn lớp khác thành hạt thân → nới mặt nạ nước 5 px; giọt nước vẽ đè thân → hộp giọt chỉ lấy màu lam và vá thân dưới giọt;
  mảng lòng miệng GPT to sau thân thò ra ngoài mõm → tô lòng miệng vào lỗ.

### Số đo cuối (05:40)
| | dạng 2 Liên Kình | dạng 1 Kình Nụ (rig gộp) |
|---|---|---|
| xương / slot | 135 / 36 | 194 / 58 |
| đỉnh / tam giác | 6329 / 10443 (thân 3901, nước còn lại) | 7232 / 11982 (thân 3081) |
| đỉnh thân / chiều cao | 7,27 (cao 536) | 7,35 (cao 419) |
| hở lưới / mí | 0 px mọi mảnh / 0 px | 0 / 0 |
| khoá | 5948 | 5504 |
| `.atomik` | 497 KB (json 780 + png 270, atlas 1144 × 1160) | 509 KB (json 886 + png 250; dạng 2 gộp co 0,45, lưới thưa 1,7, bỏ sóng sau) |
| nối clip (đỉnh lưới) | 0,00 px mọi clip; idle khép 0,91; die trống | 0,00; evolve 0,00 (dạng sau co 1,536 trong rig gộp) |
| `.atomik` nạp lại | khung 0 0,08 px; giữa clip ≤ 2,0 px | 0,09 px; ≤ 2,0 px |
| **IoU khung 0 idle / concept** | **0,865** | **0,900** |

IoU dạng 2 còn 0,865 vì: nước là đệm sóng Hải Long (hình sóng khác, vẫn to hơn concept một chút); phần sóng che chóp vây chèo và bụng
dưới trong concept; mảng lòng miệng; vài mẩu nét sóng còn dính mảnh thân ở mép nước. Phần thân, đầu, sen, vây, đuôi trùng concept.

Trang Spine player (`mo_xe/chay.py`, spine-player.js) KHÔNG dựng được rig lai: `RangeError: offset is out of bounds` ở
`PolygonBatcher.draw` (lưới thân 4,7 k tam giác qua mặt nạ cắt tràn bộ đệm batcher của player). `.atomik` nạp lại và tính đỉnh như
AtomikPose vẫn khớp bộ vẽ Python (≤ 0,09 px khung 0). Bản rig GPT cũ (lưới nhỏ hơn) chạy được trên player.

### Dọn theo soi của Claude điều phối (06:20)
- Lòng miệng: bỏ hẳn mảng GPT sau thân; đỏ rượu tô vào lỗ hàm / lỗ miệng của mảnh thân và kẹp trong bóng dáng concept (`rk &= fg`) → không còn chấm đỏ ngoài mõm (`can3_mom.png`).
- Khe trắng: lấp mọi lỗ kín trong mảnh thân bằng ô vân (896 / 1954 px); đa giác sen bên trái lùi tới 606 px để không cắt viền vây lưng; vùng khuất bụng kéo xuống 850; vá dưới vây chèo (6 px), vây xa (2 px), đế nụ; ô vân lưng đổi sang (880, 500)–(944, 564) (ô cũ dính nền trắng).
- Vây đuôi tách rời lúc attack: vùng `vd` rộng hơn, ưu tiên trước thân (chóp trên-trái trước đó rơi vào chuỗi thân) → `can3_vay_duoi_attack*.png` liền.
- Dạng 1: 488 KB (dạng 2 nhúng co 0,38, lưới thưa 1,6, vây xa cứng; lọc khoá 0,4° / 0,8; bớt một cuộn sóng).
Cuối: dạng 2 IoU 0,857, 503 KB; dạng 1 IoU 0,903, 488 KB; hở 0 cả hai.
- 06:40: không vá dưới vây xa (vẽ sau thân, vá che mất); đa giác vây xa lùi 6 px khỏi lưng. Cuối cùng: dạng 2 IoU 0,859, 499 KB;
  dạng 1 IoU 0,903, 487 KB; hở 0; ảnh cận 3× `can3_*.png` (mõm, gốc sen trái, chóp vây lưng, vây đuôi lúc attack 0,50 / 0,55, vây xa).
