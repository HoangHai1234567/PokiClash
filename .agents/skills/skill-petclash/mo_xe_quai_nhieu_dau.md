# Mổ xẻ một con quái nhiều đầu có sóng nước (Sword x Staff, monster_3705), 2026-11-10

Tham khảo nội bộ: hình và animation là của nhà phát hành, chỉ học cách làm, không lấy hình. Bản rút ở `D:\Ripper\SwordxStaff`.
Công cụ mổ: `ArtGen/Spine/mo_xe/` (`chay.py info | keys | mesh | sample | sheet` chạy runtime Spine gốc trong Chrome ngầm, tự mở server
tạm; `nhip.py` đọc nhịp từ khoá thật; `phan_tich.py`, `do_chuyen_dong.py` là ví dụ viết riêng cho con này).

## 1. Số tổng

| | |
|---|---|
| File | `.skel` nhị phân Spine 4.2.28: 1,79 MB; atlas một trang 2048 × 1228 (hình vẽ gấp đôi, xuất tỉ lệ 0,5): 1,92 MB. Tổng 3,7 MB |
| Xương | 486 (thân 131, nước 354, gốc 1) |
| Slot | 171: 170 lưới (mesh), 1 mặt nạ cắt. Không có mảnh chữ nhật (region) nào |
| Lưới | 2794 đỉnh, 2600 tam giác cả con. Mảnh lớn nhất (cổ) 43–48 đỉnh, 7 xương, tối đa 3–4 xương mỗi đỉnh |
| Ràng buộc | 2 transform constraint (mắt). Không IK, không path, **không physics** |
| Animation | 18 clip, 94 876 khoá. Chỉ có xoay, dời, co giãn xương + alpha slot + bật tắt hình + 4 clip đổi thứ tự vẽ. **Không deform** |
| Chế độ trộn | tất cả Normal. Không có lớp cộng sáng nào |

Dung lượng: file xương nặng vì khoá, không vì lưới. Mỗi clip khoá khoảng 465 xương (5000–9000 khoá).

## 2. Hình: cắt thành những gì

120 vùng ảnh trong atlas, xếp kiểu ôm sát đa giác (khung bao chồng nhau, tổng diện tích khung bao bằng 122% trang).

| Nhóm (tên gốc) | Là gì | Phần atlas |
|---|---|---|
| `l_*` (52 ảnh) | cuộn sóng rời: mào cuộn, bọt, dải nước | 31% |
| `shenti_01..07` | bảy cái cổ, mỗi cổ vẽ **đủ cả chiều dài** (kể cả đoạn chìm dưới nước), có vảy bụng | 28% |
| `langhua_*` | mảng nước nền: dải mặt nước, mảng tối phía sau | 10% |
| `shenti_zhuangshi1,2` | hai vòng thân cuộn nằm trong nước | 8% |
| `jiao_01..15` | sừng, vây gáy (rời khỏi đầu để xếp lớp trước sau) | 7% |
| `tou_01`, `shange/shagne_*` | đầu chính nhìn thẳng; hàm trên của 6 đầu nghiêng | 8% |
| `xiae_*`, `kouqiang_*`, `shetou_*` | hàm dưới, lòng miệng đỏ, lưỡi chẻ | 7% |
| `yanjing*`, `biyan*`, `yp_*`, `liaoya`, `sd_*` | mắt, mắt nhắm, mí, nanh, giọt nước | 1% |

- Sáu đầu nghiêng là **ba cặp cùng cỡ** (02 và 03, 04 và 05, 06 và 07): ba thiết kế, mỗi thiết kế dùng cho hai bên.
- 95 slot sóng chỉ dùng 52 ảnh: 33 ảnh dùng 2 lần, 4 ảnh dùng 3–4 lần. Sóng là tài nguyên dùng lại.
- Thứ tự vẽ sau → trước: nước nền sau → đầu 07, 06, 05, 04 → hai vòng thân → nước giữa → đầu 03, 02 → sóng giữa → đầu chính 01 →
  sóng trước → giọt. Tức là **đầu và sóng xen kẽ theo chiều sâu**, không phải "cả con rồi tới nước".

## 3. Xương: gắn để làm gì

```
root
├─ bone2 > bone                 nhóm THÂN (131 xương)
│   ├─ 7 chuỗi cổ, mỗi chuỗi 7 đốt (đốt cuối là đầu)
│   │    ├─ 1 xương hàm dưới (hàm + lòng miệng)
│   │    └─ lưỡi 5 đốt + 2 nhánh chẻ × 2 đốt
│   ├─ đầu chính thêm: bone232 (điểm "quay mặt"), 2 xương mắt
│   └─ bone25, bone26: mỗi cái 6 xương điều khiển xếp vòng (hai vòng thân cuộn)
└─ bone129                      nhóm NƯỚC (354 xương)
    ├─ 9 xương mảng nước nền
    ├─ ~90 chuỗi sóng, mỗi chuỗi 2–7 đốt (mỗi cuộn sóng một chuỗi, nhân đôi)
    ├─ bone157: cụm 103 xương sóng quanh cổ chính (co giãn cả cụm được)
    └─ 11 xương giọt nước
```

| Xương | Để làm gì | Vì sao làm vậy |
|---|---|---|
| Cổ 7 đốt | uốn chữ S, sóng uốn chạy từ đầu xuống gốc (đầu dẫn, xem 6b) | Idle: mỗi đốt xoay 10–45° so với đốt cha, đốt nọ trễ đốt kia khoảng 5 khung (0,17 s). Ít đốt hơn thì cổ gãy khúc; lưới 44 đỉnh chia 7 xương là vừa đủ mượt |
| Gốc cổ | **dời cả cổ xuống dưới mặt nước** | Xuất hiện, chết, lặn: không co cổ mà dời cả chuỗi 1000–1700 đơn vị, phần dưới nước do mặt nạ cắt che |
| Hàm dưới | há miệng | Chiêu lớn há 60–90° trong 1–2 khung |
| Lưỡi 9 xương mỗi đầu | lưỡi chẻ thè ra, vẫy | 63 xương chỉ cho lưỡi: đắt, và chỉ thấy vài khung. Chỗ này tiết kiệm được |
| bone232 + 2 transform constraint | đầu chính "quay mặt" giả 3D | Lưới đầu chia trọng số giữa xương đầu và bone232; mắt đi theo bone232 27,5% theo một trục. Dời bone232 là mặt lệch đi, mắt trượt ít hơn mũi: thấy như đầu xoay |
| 12 xương vòng thân | hai vòng thân phập phồng | Mỗi vòng 6 điểm điều khiển quanh vòng, không phải chuỗi |
| Chuỗi sóng 2–7 đốt | cuộn sóng trườn, mào cuộn gập lại | Sóng không chạy khung hình: một ảnh, uốn bằng xương |
| Xương chủ `bone129` | co giãn cả vùng nước | Chỉ dùng khi xuất hiện (0,16 → 1) |

## 3b. Lưới và trọng số: vì sao cổ họ cong mềm, không gập (mổ lần ba, 2026-11-10)

Đọc từng đỉnh của lưới (`chay.py mesh`). Lưới cổ `shenti_02`: 44 đỉnh, 7 xương, xếp thành **cột 3 đỉnh** (mép trên, giữa, mép
dưới), mỗi đốt hai cột: một cột ở khớp, một cột ở giữa đốt.

| Cột nằm ở | đốt trước | đốt này | đốt sau |
|---|---|---|---|
| giữa đốt | 0,15 | **0,70** | 0,15 |
| khớp giữa hai đốt | 0,50 | 0,50 | |
| hai đầu mút của dải | | 1,00 | |

**Không đỉnh nào (trừ hai đầu mút) bám cứng một đốt.** Ngay giữa đốt vẫn chia 15% cho mỗi đốt kề. Đây gần đúng là hàm cơ sở
B-spline bậc hai (0,75 / 0,125 / 0,125 ở giữa, 0,5 / 0,5 ở nút): vị trí mỗi cột là trung bình trơn của ba đốt, nên chuỗi xương
gãy khúc bao nhiêu thì lưới vẫn ra **đường cong liên tục cả hướng**. Lưỡi (`shetou`) chia y hệt. Nếu cho cột giữa đốt bám 100%
(cách tôi làm lúc đầu) thì mỗi đốt là một khúc cứng và mỗi khớp là một chỗ gập, dù có tăng lên 14 đốt.

Thêm hai điều từ lưới miệng:
- **Hàm dưới (`xiae`) là lưới hai xương:** nửa sau (cổ họng) bám xương cổ sát đầu, nửa trước bám xương hàm, hai đỉnh ở giữa chia
  đôi. Há miệng thì da cổ họng giãn ra, không hở ở bản lề.
- **Lòng miệng (`kouqiang`) bám xương hàm**, nằm sau hàm trên: hàm hạ xuống thì lộ dần ra, mép trên luôn khuất sau đầu.

## 4. Nước: có bị đầu kéo theo không

**Không.** Không xương nước nào là con của cổ hay đầu (kiểm cả 95 slot sóng và 11 giọt: mọi tổ tiên đều đi thẳng về `bone129`).
Nước là một hệ riêng, chạy vòng lặp của nó.

- **Băng chuyền sóng:** mỗi cuộn sóng hiện ra (alpha 0 → 1), dâng lên, mào tự cuộn lại, trôi nhẹ khoảng 50 đơn vị rồi tan (alpha → 0); chi tiết ở cuối mục này.
  Chu kỳ **1,33 s** (40 khung), hiện 1,27 s, tắt 0,07 s rồi nhảy về chỗ sinh.
- **Mỗi cuộn có một bản sao lệch nửa chu kỳ** (0,5–0,67 s) trên chuỗi xương riêng, cùng ảnh: lúc bản này tan thì bản kia đang
  đậm, nên không bao giờ thấy "hết sóng". Đó là lý do 95 slot mà chỉ 52 ảnh, và 354 xương nước.
- Đầu lặp theo chu kỳ 2,67 s; idle dài 5,33 s = 4 vòng sóng, 2 nhịp đầu.
- **Vòng nước được chép vào mọi clip.** Clip dài đúng 2,67 s (gầm, choáng, chiêu 2, 3) có nước y hệt idle từng khung. Clip ngắn
  hơn (đánh 1,83 s, trúng đòn 0,5 s, chết 2 s) nước bắt đầu ở pha khác: lúc đổi clip nhờ trộn tư thế che.
- Nước **không phản ứng** với đòn: đầu quật xuống mặt nước, sóng vẫn chạy như cũ. Liên hệ duy nhất là thứ tự vẽ và mặt nạ.

### Một cuộn sóng sống thế nào (đọc khoá chuỗi `l_60 … l_65`, mổ lần bốn 2026-11-10)

Lần đầu tôi ghi "sóng trườn ngang 250–600 đơn vị": **sai**. Đọc khoá thì gốc chuỗi sóng chỉ dời khoảng **50 đơn vị** cả đời
(cuộn sóng dài cỡ 250). Cái làm sóng "mềm" là **chính nó tự cuộn**:

| khung của vòng 40 | gốc chuỗi (dời) | đốt 2 | đốt 3 | đốt 4 | đốt 5 | đốt 6 | chuyện gì |
|---|---|---|---|---|---|---|---|
| 10 (sinh) | (28, 0) | 8° | −3° | **−24°** | −18° | −10° | sóng còn duỗi, nằm thấp, alpha 0 → 1 |
| 30 | (0, 46) | 31° | 17° | 15° | 7° | 13° | dâng lên 46 đơn vị, bắt đầu cuộn |
| 40 | (22, 45) | 29° | 30° | 28° | 12° | 16° | trôi tới, cuộn thêm |
| 49 (tan) | (53, 46) | 27° | 43° | **39°** | 16° | 20° | mào cuộn chặt nhất, alpha → 0; khung sau nhảy về dáng sinh (khoá kiểu bậc) |

- Mỗi cuộn sóng là **một ảnh trên chuỗi 5–7 xương đặt dọc sống lưng sóng** (từ chân, lên lưng, vào tới đầu móc). Cả đời sóng các
  đốt cùng xoay một chiều: đốt gần mào đi 63°, tức là **mào tự cuộn lại** trong lúc sóng dâng.
- Nửa đầu đời: dâng thẳng lên. Nửa sau: trôi ngang chậm và cuộn chặt dần. Không có đoạn nào "trượt như tấm bìa".
- Bố cục: hàng chục cuộn đủ cỡ (từ vòi nước cao bằng nửa cổ tới cuộn xoắn tí hon) xếp dày quanh chỗ từng cổ trồi lên; một dải
  sóng dài quét ngang phía trước; dưới cùng là hàng gợn sóng lăn tăn. Lúc đổi vòng các cuộn mờ chồng lên nhau nên nước như sôi.

## 5. Mặt nạ cắt: mẹo trồi lên và chìm xuống

Slot đầu tiên `zhezhao` là một đa giác cắt 9 đỉnh, cắt từ slot 1 tới slot 105 (mọi đầu, cổ, nước sau), **không cắt sóng trước**.
Mặc định tắt; chỉ bật trong clip xuất hiện, chết, và một chiêu lặn. Cách dùng: dời gốc cổ xuống dưới mép cắt, phần dưới mép biến
mất, sóng trước (không bị cắt) phủ lên đường cắt. Cắt chạy trên CPU nên chỉ bật khi cần.

## 6. Từng clip diễn thế nào

| Clip | Dài | Diễn |
|---|---|---|
| `generate_01` xuất hiện | 4,33 s | 0–1 s: vũng nước nở từ 0,16 lên 1 (co giãn `bone129`), sóng hiện dần (bật hình từng slot). 2,0–3,1 s: các đầu trồi lên **lần lượt, mỗi đầu cách nhau 0,1–0,4 s** (thứ tự 4, 5, 3, 2, 1, 7), tốc độ đỉnh 4500–8500 đơn vị/giây. Cuối: gầm, về dáng idle |
| `idle_01` | 5,33 s | Xương chủ đứng yên. Mỗi đầu đung đưa 120–340 đơn vị (7–20% chiều cao con), lệch pha nhau; gốc cổ không dời; tốc độ đỉnh 160–460/giây |
| `skill_01` đòn đánh | 1,83 s | Các đầu ngả ra sau rồi đầu chính bổ xuống ở **0,57 s (31% clip)**, tốc độ 6100/giây (gấp 27 lần idle); các đầu khác bổ theo, lệch 0,50–0,67 s |
| `skill_03` chiêu lớn | 2,67 s | Tụ 1,2 s (đầu chính há miệng, các đầu chụm lại). **1,27–1,40 s: cả bảy đầu quật toả ra**, đi 700–1100 đơn vị trong 1–2 khung (tới 32 000/giây), hàm há 60–90°. Rồi thu về trong 1 s |
| `hit_01` trúng đòn | 0,5 s | **Khung 0 đã là dáng bị đánh** (tốc độ lớn nhất ở khung đầu, không lấy đà), mắt nhắm, mí sụp; hồi về trong 0,5 s |
| `die_01` chết | 2 s | Bật mặt nạ cắt. Các đầu giãy rồi **gốc cổ dời xuống 1400–1700**, từng đầu chìm lệch nhau; mắt nhắm. Sóng vẫn chạy tới hết |

Khung 0 của clip không phải dáng idle: runtime trộn tư thế lúc đổi clip.

## 6b. Nhịp theo khoá thật: mỗi lần xương đổi dáng là vì sao (mổ lần hai, 2026-11-10)

Lần đầu chỉ lấy mẫu khung nên chỉ thấy "đầu đi nhanh cỡ nào". Lần này đọc **khoá người làm animation đặt**
(`chay.py keys` → `nhip.py`): khung nào có khoá, đốt nào lệch đốt nào, dùng đường cong gì. Kết luận lớn nhất:

**Thân chỉ có 700–1100 khoá mỗi clip** (idle 970 khoá cho 131 xương thân; nước 6600). Chất lượng không đến từ nhiều khoá mà từ
**đặt khoá lệch nhau có chủ ý**. Gần như không dùng co giãn (chỉ hàm và đầu chính giãn 1,13–1,23 đúng khung ra đòn), không dời
xương cổ (chỉ dời gốc cổ khi trồi, chìm): mọi thứ là **xoay**.

### Idle: mỗi đốt 2 khoá một vòng, lệch khung nhau → sóng

Khoá xoay cổ đầu chính (độ so với dáng gốc; vòng 80 khung = 2,67 s, đường cong bezier):

| đốt (gốc → đầu) | bone3 | bone4 | bone5 | bone6 | bone7 | bone8 | bone9 (đầu) |
|---|---|---|---|---|---|---|---|
| khung đạt cực trị | 5 / 45 | 0 / 40 | 35 / 75 | 25 / 65 | 35 / 75 | 20 / 60 | 25 / 65 |
| hai cực trị | 0 / −10,7 | −7,3 / 11,5 | 9,8 / −3,0 | −23,8 / 15,5 | −3,7 / 13,8 | 18,8 / −2,5 | −3,0 / −15,5 |
| biên độ | 11° | 19° | 13° | **39°** | 18° | 21° | 13° |

- **Vì sao 2 khoá:** một đốt chỉ cần "ngả bên này, ngả bên kia"; đường bezier lo phần êm. Ít khoá thì sửa nhanh, không rung.
- **Vì sao lệch khung:** đốt gần đầu đạt cực trị trước (khung 20–25), càng về gốc càng muộn (35, 40, 45): **đầu dẫn, thân theo**,
  mỗi đốt trễ khoảng 5 khung (0,17 s). Mắt người đọc thành một làn sóng trườn từ đầu xuống gốc cổ. Cùng khung hết thì cả cổ lắc
  như một cái que.
- **Vì sao dấu ngược nhau giữa hai đốt kề** (bone6 −23,8 trong khi bone8 +18,8; bone9 −15,5 lúc bone6 +15,5): đốt trên xoay bù đốt
  dưới nên **giữa cổ uốn mạnh mà đầu gần như đứng yên và giữ thăng bằng** (mắt vẫn nhìn đối thủ). Đầu trôi theo cổ là con vật vô hồn.
- **Biên độ lớn nhất ở giữa chuỗi**, nhỏ ở gốc (bị nước giữ) và ở đầu (giữ thăng bằng).
- Hai nửa idle (0–80, 80–160) y hệt nhau; cái làm nó không đều là **điểm phá nhịp**: lưỡi thè ra vẫy đúng 0,4 s (khung 30–42, khoá
  mỗi 2 khung, biên độ tới 58°, hàm hé 4° cho lưỡi ra) rồi nằm im cả vòng; điểm "quay mặt" `bone232` giật nhẹ 14 khung. Mỗi đầu
  làm ở giờ khác nhau.
- **Vòng thân:** 6 điểm điều khiển quanh vòng, mỗi điểm 2 cực trị một vòng, **điểm nọ lệch điểm kia 10 khung** (khung 0/40, 30/70,
  20/60...): chỗ phồng chạy quanh vòng, nhìn như thân đang trườn dù ảnh đứng yên.

### Đòn đánh (`skill_01`, 55 khung): dáng → dáng, toàn đường thẳng

90% khoá là nội suy thẳng, mọi đốt khoá **cùng khung**: 0, 6, 15, 17, 18, 21, 28, 37, 47, 55. Nhanh chậm do **khoảng cách giữa các
khoá**, không do đường cong.

| khung | dáng | vì sao |
|---|---|---|
| 0 → 6 (0,2 s) | nhún nhẹ ngược chiều | báo trước: mắt người kịp nhìn sang con này |
| 6 → 15 (0,3 s) | cổ trên cuộn hẳn ra sau (đốt sát đầu +43°, đầu −38°), giữ 4 khung | lấy đà; giữ một nhịp cho người xem "đọc" được dáng |
| 15 → 17 | **khung gãy**: đốt giữa bật trước (+31°), đầu còn ở sau | roi quất: lực đi từ gốc ra ngọn, khớp gãy lần lượt |
| 17 → 18 (1 khung) | chạm: đốt gần đầu đổi dấu trong một khung (32 → −3, 5 → 21) | nhát đánh chỉ 1 khung nên mới "có lực"; hàm giãn 1,13 đúng khung này (smear) |
| 18 → 21 | quá đà rồi dội lại vài độ | khối lượng |
| 21 → 37 (0,53 s) | **giữ có trôi**: mỗi đốt chỉ đổi 3–7° | đủ lâu để thấy cú cắn; đứng im tuyệt đối thì chết hình |
| 37 → 55 | về dáng đứng, khoá cuối kiểu bậc | khung cuối trùng khung đầu idle |

### Chiêu giữ (`skill_05`, `skill_06`): nén lâu, bung 2 khung, rung hai dáng

- Nén 0,3–0,9 s: các đầu cụp xuống chụm lại (đốt giữa −28°, −32°), rồi vặn dần lên dáng lấy đà (đốt sát đầu 50° → 68° trong 0,3 s).
- Bung trong **2 khung** (khung 29 → 31): hàm 0 → −53 → −96°.
- **Giữ 0,83 s bằng hai dáng đổi nhau MỖI KHUNG** (khung chẵn một dáng, khung lẻ một dáng; mỗi đốt lệch 2–3°, hàm lệch 6°). Vì
  thế chiêu này có 2500 khoá thân. Đây là cách vẽ "gồng, rung" rẻ nhất: không cần đường cong, không cần nhiễu.
- Tia, đạn không nằm trong rig: rig chỉ diễn thân, hiệu ứng là file khác.

### Trúng đòn (`hit_01`, 15 khung): sóng chạy ngược từ đầu về gốc

| khung | đốt sát đầu | đốt giữa | gốc |
|---|---|---|---|
| 0 | đã lệch sẵn một ít | | |
| 2 (0,07 s) | **đỉnh** (+25°, đầu −28°) | mới −7° | +6° |
| 6 (0,2 s) | đang về (20°, −12°) | **đỉnh** (−17°, +25°) | +7° |
| 10 → 15 | về | về | về |

Không có lấy đà (bị đánh thì không chuẩn bị). Lực vào đầu trước nên đầu đạt đỉnh ở khung 2, đốt giữa khung 6, gốc gần như không
nhúc nhích: **sóng chạy từ ngọn về gốc và tắt dần**, ngược với đòn đánh. Mắt đổi sang hình nhắm trong lúc này.

### Xuất hiện, chết

- Gốc cổ dời xuống 1025 (đầu chính) / 1518 (đầu bên) dưới mặt nạ cắt. Đầu bên trồi trong **10 khung (0,33 s)**, đầu chính trong
  **30 khung (1 s)**: con to, quan trọng thì chậm và sau cùng.
- Lên tới nơi không dừng ngay: gốc cổ lắc tắt dần, khoá mỗi 5 khung (18°, 9°, 7°, 3°, 12°, 9°, 1°).

## 7. Vì sao họ rig như vậy, và chỗ nào cải thiện được

Họ chọn **toàn xương, khoá tay, không vật lý, không deform**: chạy được trên mọi runtime Spine cũ, kết quả y hệt mọi máy, hoạ sĩ
kiểm soát từng khung. Giá phải trả là số xương và số khoá.

| Chỗ | Cải thiện |
|---|---|
| Vòng nước chép vào cả 18 clip (hơn nửa số khoá) | Tách nước thành **một clip lặp riêng phát chồng** (track thứ hai; ở `.atomik` là clip `aura`). File nhỏ đi khoảng một nửa, nước liền qua mọi lần đổi clip |
| 63 xương lưỡi, khoá tay mọi clip | Lưỡi, râu, bờm: lò xo lúc dựng (`longrig.Springs`) hoặc physics của Spine 4.2; hoặc bỏ lưỡi nếu con không cần |
| Nước không phản ứng với đầu | Thêm lớp phản ứng: đầu bổ xuống thì vương miện nước toé ở chỗ chạm, sóng quanh đó nẩy lên; trồi lên thì vòng sóng loang. Giữ băng chuyền làm nền |
| Đầu hai bên cùng thiết kế nhưng lưu ảnh riêng | Dùng một ảnh, lật bằng tỉ lệ âm của xương |
| Mỗi cuộn sóng một bản sao trên chuỗi xương riêng | Giữ (mẹo đúng), nhưng chuỗi 2–3 đốt là đủ cho cuộn nhỏ |
| Cắt bằng đa giác | Giữ cho trồi / chìm. Runtime không có cắt (`.atomik`) thì co ngắn cổ về gốc và che bằng sóng trước |

## 8. Muốn làm một con cùng kiểu: cần gen gì, tách ảnh thế nào

Con nhiều cổ chồng nhau **không rig được từ một ảnh liền** (cổ sau bị che, lúc vươn ra sẽ thiếu hình). Phải có mảnh rời vẽ đủ:

1. **Concept trọn con** (một ảnh): chốt dáng, màu, số đầu, kiểu nước. Chỉ để làm mốc, không cắt từ ảnh này.
2. **Tờ đầu:** mỗi thiết kế đầu gồm phần trên (sọ + hàm trên, sừng liền hoặc rời), **hàm dưới rời có lòng miệng**, và phần gáy
   vẽ dư để chồng lên cổ. Đầu nghiêng chỉ cần 1–2 thiết kế, lật cho hai bên.
3. **Tờ cổ:** cổ vẽ **duỗi thẳng, đủ dài kể cả đoạn dưới nước**, hai đầu tròn; 1 cổ to (đầu chính) + 1 cổ nhỏ dùng lại. Vẽ
   thẳng thì lưới là một dải chia đốt đều, uốn bằng xương; vẽ cong sẵn thì lúc uốn ngược chiều vân vảy bị nhăn.
4. **Tờ nước:** 6–10 cuộn sóng rời (to, vừa, nhỏ; mào cuộn trái và phải), 1–2 dải mặt nước dài, mảng nước nền, vương miện
   nước toé, giọt. Sóng vẽ đứng riêng, đáy phẳng hoặc thuôn để chồng lên nhau.
5. Phụ kiện động: râu, bờm, vây vẽ rời nếu muốn chúng trễ theo đầu.

Dựng: cổ là lưới dải 7 đốt; đầu cứng theo đốt cuối, hàm một xương; hai nhóm xương gốc tách nhau (thân, nước); sóng là băng
chuyền hai bản sao lệch nửa chu kỳ; lớp vẽ xen kẽ đầu sau → nước giữa → đầu trước → sóng trước.

## 9. Con đã dựng theo cách này: Hải Long Ngũ Đầu (2026-11-10, bản 3)

Rồng biển năm đầu, dựng bằng `ArtGen/Spine/hai_long.py` (`cat` cắt mảnh, `rig` dựng tất cả), gói GPT `build_hai_long.py`
(1 concept + 7 tờ mảnh: đầu và hàm; cổ, vòng thân, đuôi; cuộn sóng; mặt nước và nước toé; M05 mí mắt và các mảnh tia nước; M06
lưỡi; M07 hình nước đợt hai: vòi nước cao, cuộn xoắn, dải sóng dài, dải gợn sóng). Ra `inbox/hai_long/rig/`: `hai_long.json/.atlas/.png` (Spine 4.2) và `xem.html` (trang xem một file, bấm đúp là mở; mẫu
`xem_spine_mau.html`). Số: **482 xương (thân 193, nước 288), 122 slot, 3317 đỉnh, 7 clip, khoảng 64 nghìn khoá, 2,98 MB** (json 2,24 + atlas bảng 256
màu 0,74). Clip: xuất hiện 4,8 s, đứng 3,2 s, tấn công 1,6 s, chiêu gầm 3,2 s, chiêu phun nước 3,2 s, trúng đòn 0,8 s, chết 4,0 s.

Giữ từ con gốc: hai nhóm xương gốc tách nhau (thân, nước), băng chuyền sóng hai bản sao lệch nửa chu kỳ, lớp vẽ xen kẽ, mặt nạ
cắt, hàm một xương, **trọng số lưới kiểu B-spline (mục 3b)** và **các luật nhịp ở mục 6b**. Cách áp từng luật khi dựng bằng mã:

| Luật của con gốc | Làm bằng mã |
|---|---|
| Dải lưới không đỉnh nào bám cứng một đốt | `chain_weights`: hàm cơ sở B-spline bậc hai theo vị trí dọc dải (giữa đốt 0,75 / 0,125 / 0,125, khớp 0,5 / 0,5), dùng cho cổ, râu, đuôi, lưỡi. Đây là thứ sửa hết các chỗ "gập nhẹ" trên thân |
| Đầu dẫn, thân theo | Mỗi khung chỉ cho vị trí và góc **đầu**; cổ 14 đốt giải theo đường Bezier từ chỗ trồi tới gáy, đoạn thừa trượt thẳng xuống dưới mặt nước (mặt nạ cắt luôn bật). Điểm điều khiển phía gáy trễ 0,085 s nên cổ quất theo sau đầu |
| Mỗi đốt lệch pha, giữa cổ uốn mạnh, đầu đứng yên | Cộng một **sóng ngang chạy dọc cổ** vào đường cong: `biên độ × sin(π s) × sin(2π·1,15·s + ωt)`; `sin(π s)` tắt ở chỗ trồi và ở gáy nên đầu không xê dịch. Biên độ 22, giảm còn 40% khi đang ra đòn |
| Cổ vào đầu từ dưới sau | góc tới = góc đầu + 40–85°, bờm che chỗ nối; cho cổ đi theo hướng mõm ra cổ hình số 7 |
| Phần mềm trễ theo, biên độ lớn dần ra ngọn | Râu 6 đốt **mô phỏng dây mềm rồi nướng** (`rope`): mỗi đốt là lò xo kéo về dáng nghỉ so với đốt trước, cứng 0,20 ở gốc → 0,035 ở ngọn, giảm chấn 0,5, có gió hình sin chạy dọc sợi. Mỗi khớp chỉ gập tối đa 20–32° (nén bằng tanh) |
| Thịt trong miệng đi theo hàm dưới (rig mẫu: `kouqiang` bám 100% xương hàm) | Lòng miệng là lưới 5×3: **hàng dưới bám xương hàm 100%**; hàng trên chỉ bám đầu ở sát bản lề (thành màng khoé miệng), ra phía mõm thì theo hàm luôn (0 / 0,35 / 0,8 / 1 / 1) và mỏng dần. Há miệng thì cả mảng thịt hạ xuống cùng hàm; hàm trên không giữ lại mảng thịt nào. Phía trước giữa hai hàm là khoảng trống |
| Vòng thân: điểm điều khiển lệch khung | Vòng thân là lưới 8×5 với 5 điểm điều khiển dọc vòm, mỗi điểm trễ 0,9 rad; đuôi là dải 6 đốt quẫy sóng lớn dần ra vây |
| Khung ra đòn giãn 1,13 | Xương đầu co giãn (1,15; 0,92) đúng khung cắn, khung sau (0,96; 1,04), rồi về 1 |
| Rung hai dáng lúc giữ chiêu | Hai dáng đổi nhau mỗi 2 khung (15 lần/giây: bản 30 khung/giây đổi mỗi khung thì máy 60 Hz không thấy rõ), lệch ±5–6 đơn vị, ±1,2–1,6°, hàm ±3° |
| Điểm phá nhịp trong idle | Mỗi đầu chớp mắt một lần mỗi vòng và táp miệng một cái 0,45 s, giờ riêng từng đầu; thủ lĩnh chớp đôi |
| Mắt nhắm khi trúng đòn, chết | Mảng mí mắt (slot riêng, bật tắt bằng alpha). `fit_lid` dò góc, tỉ lệ, độ lệch để mí **phủ kín** con mắt (bao lồi cụm cam nới 5 px cho hết viền mực), ít lòi ra ngoài đầu nhất và nhỏ nhất; in ra số điểm còn hở (phải là 0) |
| Sóng dâng tại chỗ và tự cuộn mào, không trượt ngang | Mỗi cuộn sóng là lưới 5×5 bám chuỗi 4 đốt đặt trên **sống lưng** của hình (bảng `SPINES`: đường từ chân sóng lên mào vào đầu móc, ghi tay theo ảnh có kẻ lưới). Đời sóng: dâng 24% chiều cao trong nửa đầu, các đốt xoay cùng chiều uốn của sống lưng từ −0,55 tới +1 lần (8° / 18° / 26° / 20°), trôi 46 đơn vị, alpha vào 16% đầu và ra 16% cuối. Điểm lưới xa sống lưng (ngọn sóng phụ, chân sóng) bám xương gốc |
| Nước dày, đủ cỡ, quanh từng cổ | 23 cuộn × 2 bản sao lệch nửa chu kỳ, bốn lớp: sau mọi cổ (vòi nước cao, sóng lớn), giữa hai nhóm đầu, trước cổ (cuộn xoắn nhỏ, cụm bọt), dải sóng dài quét hai bên |
| Mào dải nước uốn sóng | Dải mặt nước và dải gợn sóng là lưới bám 8 xương xếp dọc dải (trọng số B-spline theo x, hàng đáy bám gốc); các xương nhấp nhô lệch pha 0,8 rad nên sóng chạy dọc mào |
| Tia, đạn không nằm trong rig | Xem dưới |

**Tia nước, đạn, vụ nổ thuộc lớp VFX của game, không vẽ trong rig** (người dùng dặn 2026-11-10, sau khi tôi đã dựng tia trong rig
rồi phải bỏ). Rig chỉ diễn thân và nước dưới chân, và để lại cho VFX:
- xương `mieng_<đầu>` ở môi mỗi đầu, trục x chĩa theo hướng nhả (VFX bám vị trí và góc);
- sự kiện trong clip: `phun` (chuỗi = tên đầu, lúc đầu đó bắt đầu phun), `het_phun`, `can` (khung cắn trúng), `gam` / `het_gam`,
  `troi` (đầu trồi khỏi nước), `roi_nuoc` (đầu đập xuống nước);
- clip `chieu_phun` giải lặp góc từng đầu để trục `mieng_` chĩa đúng điểm `TGT` (chỗ đối thủ, đang ghi cứng trong rig).
Các mảnh tia nước đã vẽ (tờ M05: hai tia, vụ nổ, loa nước, ba vệt nước) nằm ở `inbox/hai_long/manh/`, để dành cho VFX.

**Clip chết** (người dùng dặn: mắt nhắm, đầu ngửa, lè lưỡi): 0,07 s cả năm đầu giật bật, nhắm nghiền mắt → từng đầu lả đi (0,30 /
0,42 / 0,54 / 0,66 s, thủ lĩnh 0,85 s): **ngửa ra sau 62–70°** (mõm chổng lên), hàm trễ 40°, **lưỡi tuồn ra rồi rũ** (dải 5 đốt,
con của xương hàm, vẽ trước hàm và sau đầu; `rope` với trọng lực 30 000 thay cho gió), lắc lư yếu ớt 0,6–0,8 s → cổ hết lực, đầu
đổ ngửa ra sau đập xuống nước (toé đúng chỗ rơi) → nổi lộn ngược nửa giây (cằm chổng lên, lưỡi vắt ra) → chìm → nước tan.

Cái con gốc không có:
- **Nước phản ứng với đầu:** kho 6 vương miện nước, 20 giọt, 3 vòng sóng; clip khai `(giờ, x, y, cỡ, loại)` ở chỗ đầu trồi hay bổ xuống.
- **Nối clip:** mọi clip dài bội số 0,8 s (nửa chu kỳ sóng); dao động tuần hoàn của clip không lặp tính theo giờ lùi `t − D`, nên
  khung cuối trùng khung đầu clip đứng (lệch còn lại chỉ ở ngọn râu, dưới 16°). Khung đầu clip xuất hiện và khung cuối clip chết:
  nước co về 0, thân lùi 500 dưới mặt nạ.
- **Giảm khoá:** nướng 30 khung/giây rồi lọc Ramer–Douglas–Peucker (xoay 0,25°, dời 0,5–0,6). Vẫn gấp nhiều lần số khoá thân của
  con gốc: dựng bằng mã thì khoá dày, đổi lại sửa một tham số là xong cả 7 clip.
- **Atlas bảng 256 màu:** hình tô phẳng có vân chì chịu được, 4 MB còn 0,6 MB, soi cận không thấy khác.

Lỗi đã gặp:
- **Nước trượt ngang như tấm bìa**, ít cuộn, không mềm: bản đầu cho mỗi cuộn sóng 2 xương và dời 200–280 đơn vị. Đọc sai rig
  mẫu vì chỉ lấy mẫu toạ độ; phải đọc khoá của chuỗi sóng mới thấy nó dâng tại chỗ và tự cuộn.
- **Mí mắt hở hai lần:** lần một đặt theo "tâm con ngươi × hệ số"; lần hai có dò nhưng "con mắt" chỉ tính cụm cam đậm, sót phần mống mắt vàng nhạt nên vẫn hở một vệt. Vùng cần phủ phải là cả vùng màu ấm liền với con ngươi; mí tránh đè lên gờ mày; in số điểm còn hở và **soi ảnh cận phóng 4 lần** chứ không tin riêng con số.
- **Cổ gập nhẹ ở từng khớp** dù đã 14 đốt: cột lưới giữa đốt bám 100% một xương. Tăng số đốt không chữa được; phải chia trọng số
  kiểu B-spline (mục 3b). Lỗi này chỉ lộ khi người dùng xem chuyển động; tờ khung thu nhỏ không thấy.
- **Lòng miệng làm sai ba lần** (người dùng dặn ghi lại, 2026-11-10). Lần một: mảng tròn bám xương đầu, há to là mảng tròn lơ lửng. Lần hai: lưới quạt lấp kín cả khe miệng, ngửa đầu lên là một khối thịt đỏ to như cái lều. Lần ba: dải thịt dưới hàm trên bám đầu, há ra thì dải đó ở lại, chìa ra song song với lưỡi, **trông như hai cái lưỡi**. Luật đúng: **thịt trong miệng thuộc về hàm dưới và phải há theo hàm**; chỉ một màng nhỏ ở khoé miệng nối lên đầu. Rig mẫu đã cho thấy điều này từ đầu (lòng miệng bám 100% xương hàm, mục 3b) mà tôi không áp. **Bộ phận bên trong (miệng, mắt): làm đúng như rig mẫu trước, rồi mới nghĩ tới cải tiến; soi ở dáng há to nhất và dáng ngửa đầu.**
- Dựng tia nước trong rig rồi phải bỏ: hỏi trước "cái này thuộc rig hay thuộc VFX" với mọi thứ bay ra khỏi thân.
- Râu mô phỏng quá mềm (cứng 0,016 ở ngọn, không giới hạn góc) bị cú giật trúng đòn vò thành cục: phải cứng hơn và chặn góc từng khớp.
- Lưỡi lúc đầu dài quá và chìa thẳng như que: GPT vẽ to hơn cỡ dặn (473 px thay vì 320) nên phải thu khi nạp (`PSC`), và trọng
  lực phải đủ lớn so với độ cứng (độ võng mỗi đốt ≈ g·dt² / k).
- `hash()` của Python đổi mỗi lần chạy: hạt giống ngẫu nhiên dùng `zlib.crc32`.
- Vận tốc khung đầu của clip không lặp làm phần mềm lệch ngay từ khung 0: cho mô phỏng đứng yên 12 khung ở dáng đầu rồi mới chạy.
- Khoá sóng ngoài `[0, D]` phải giữ lại để nội suy hai mép clip; giọt rơi lọt xuống dưới dải nước thì tắt khi về tới mặt nước.
- Tìm con ngươi theo màu cam dính cả sừng vàng: chỉ nhận cụm nằm trong vùng mặt (56–86% bề rộng, 38–82% bề cao ảnh đầu).
- Xương có tỉ lệ khác 1 (hàm 0,86) mà gắn lưới: toạ độ gắn phải chia cho tỉ lệ đó.

Đã xuất được `.atomik` (2026-11-10): thêm mặt nạ cắt, sự kiện, slot ẩn mặc định vào định dạng và runtime (skill
`pokiclash-spine-rig` mục 9, "Bản 3"); `hai_long.py rig` xuất luôn `hai_long.atomik` (1 MB) và chép sang `Assets/05 Atomik Thu/`.
Unity dựng đúng như Spine ở cả 7 clip (so hình bóng từng khung 0,93–1,00).

Chưa có: lưỡi chỉ dùng trong clip chết; hàm dưới chưa là lưới hai xương như con gốc (bản lề vẫn là mảnh cứng); nước vẫn chép vào
từng clip; chưa đo tốc độ trên điện thoại (482 xương, 3477 đỉnh, tính da và cắt trên CPU mỗi khung); chưa nối vào trận.
