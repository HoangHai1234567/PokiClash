# tm02: ghi chú dòng "Thạch Giải" (cua ẩn sĩ cõng nhà đá), lô 10 tướng mới đảo Thủy

Đặc tả chung: `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`. Dòng 2, thay suất ải 5 đảo Thủy (Tiểu Y, common). Con gốc tham khảo:
`monster_3227` (Sword x Staff), là dạng 1. Việc: vẽ lại dạng 1 (khác hẳn), thêm dạng 2 (dạng cuối).

## 1. Con gốc monster_3227 (chỉ học cấu trúc và nhịp, không lấy hình)

Đọc từ `D:\RefAnimation\SwordxStaff\scan\monster_3227\info.json, keys.json, mesh.json`, atlas `.png` và ảnh chụp trang xem.

**Số:** Spine 4.2.28; 39 xương; 18 slot (17 lưới + slot bóng trống); 153 đỉnh, 123 tam giác; 10 clip, 2140 khoá; 0,1 MB
(`.skel` 32 KB + atlas 364 × 224 xuất tỉ lệ 0,75, 62 KB). 10 IK: 4 cho chân (mix 1, bàn chân bám đất), 6 cho càng (mix 0, chỉ
bật trong clip choáng). Không physics, không transform, không sự kiện, không deform.

**Dáng:** nhìn thẳng, đối xứng trái phải. Thân là một tảng đá màu be có hốc tối, một mắt đỏ trong hốc; hai cặp chân bò; hai
càng lớn hình lưỡi hái màu băng xanh nhạt.

**Cắt mảnh** (17 hình):
- `P_sheniti`: thân đá cả khối (8 đỉnh, 1 xương: cứng hẳn).
- Chân `shou1`, `shou2` mỗi bên: đoạn trên 11–12 đỉnh bám 2 xương (bẻ ở khớp), đoạn dưới 8 đỉnh 1 xương. Chuỗi 3 xương + IK.
- Càng `shou3` mỗi bên: cánh tay `L3/R3` (1 xương) + **hai lưỡi càng rời `L1`, `L2` cùng gốc** ở xương cổ tay (bone17 / bone21):
  kìm mở khép bằng xoay hai lưỡi ngược chiều nhau.
- Mắt `yanjing1` (mở) / `yanjing2` (nhắm, dấu X) đổi hình ở cùng slot, trên xương `bone22` (dời 1–8 đơn vị = liếc, rung).
- Lưới rất thưa: gần như mọi mảnh là cứng, chỉ mềm ở khớp chân.

**Cây xương:**
```
root → bone18 (đất: đích IK 4 chân L1 L2 R1 R2, bóng, đích càng SL*/SR*)
         └ bone23 (nhún) → bone (tâm thân: dời, xoay cả con) → bone2 (đá, xoay 90°)
                                                                ├ bone22 (mắt)
                                                                ├ càng: bone15 → bone16 → bone17 → 2 lưỡi (và đối xứng bone19..21)
                            └ 4 chân: bone3..5, bone6..8, bone9..11, bone12..14 (con của bone, IK về đích trên bone18)
```

**Clip và nhịp** (đọc khoá bằng `mo_xe/nhip.py`):

| Clip | Dài | Nhịp |
|---|---|---|
| `idle_01` | 1,33 s | thân nhún −21,7 hai lần một vòng (đáy ở 0,33 và 1,0 s); càng thở trễ (vai cực trị 0,17 / 0,5 s, cổ tay 0,33 / 1,0 s); hai lưỡi kìm bập mở–khép trong 0,23 s đầu vòng (điểm phá nhịp); 86% bezier |
| `skill_01` (đòn) | 1,0 s | lấy đà 0–0,33 s: thân lùi 137 về sau (trái) và ngửa 32°, càng cuộn ra sau; **ra đòn trong 1 khung** (khung 10 → 11: càng quất 150°, lưỡi kìm 69° → −13°), thân dội về; giữ có trôi 0,37–0,70 s; về ở 1,0 s; 85% nội suy thẳng |
| `skill_02` (chiêu) | 1,63 s | tụ: thân run nhún −30 / −22 mỗi 3 khung (0–0,4 s); bật ở 0,5 s; giữ **rung hai dáng mỗi 2 khung** 0,83–1,37 s (−35,9 / −20,6), mắt rung theo; về ở 1,63 s |
| `hit_01` | 0,5 s | khung 0 đã là dáng bị đánh (thân đẩy về sau 112, ngửa −20°), đỉnh ở khung 2 (0,07 s), về 0,5 s; mắt đổi hình nhắm |
| `hit_02` | 0,67 s | bị hất lên (y +113) rồi rơi |
| `die_01` | 1,0 s | nhắm mắt, bật lên 185 rồi lật nghiêng 39°, rơi, nằm, chân co |
| `block_01` 0,5 s; `floating_01` 1,5 s (bị hất bay); `run_01` 0,53 s; `stun_01` 1,33 s (bật IK càng, choáng) | | |

Hướng: lấy đà lùi sang trái, trúng đòn bị đẩy sang trái, tức con gốc đánh sang phải.

**Học:** chân IK bám đất để thân nặng nhún mà chân không trượt; kìm hai lưỡi rời cùng gốc (bập kìm là điểm phá nhịp rẻ, rõ);
ra đòn 1 khung + giữ có trôi; giữ chiêu bằng rung hai dáng; trúng đòn không lấy đà, đổi hình mắt nhắm.
**Không lấy:** hình, màu, thiết kế; thân là đá có hốc tối một mắt; dáng nhìn thẳng đối xứng; lưới thưa một xương.

## 2. Thiết kế dòng

**Tên đề xuất:** dòng **Thạch Giải** (thạch = đá, giải = cua). Dạng 1 **Thạch Giải**, dạng 2 **Thạch Thành Giải** (cua thành đá).

**Lore:** cua ẩn sĩ con gác vũng triều, cõng một tảng đá bazan rỗng làm nhà; bướng, lì, không lùi bước. Lớn lên nó đổi nhà
thành cả một cột đá biển lởm chởm có san hô mọc thành vương miện, càng búa bọc đá thành găng: một "pháo đài di động".

**Chỉ giữ của con gốc:** chủ đề "giáp xác mang đá trên lưng". Khác ở mọi thứ còn lại:

| | Con gốc 3227 | Thạch Giải |
|---|---|---|
| Loài, ý | thân chính là tảng đá có hốc tối | cua ẩn sĩ: đá là **nhà cõng trên lưng**, thân cua ló ra từ cửa đá |
| Góc nhìn | nhìn thẳng, đối xứng | nghiêng 3/4 nhìn sang phải, **lệch hai bên** (một càng búa to, một càng nhỏ) |
| Mắt | một mắt đỏ trong hốc tối | hai mắt hổ phách trên cuống ngắn, nắp mí giáp cau có |
| Màu | đá be, càng băng xanh nhạt | vỏ lam xám (slate), đá bazan xám than, điểm hồng san hô, hà kem, rong xanh |
| Càng | hai lưỡi hái băng dài | càng búa khối tròn đầu ngón sẫm + kìm nhỏ |
| Chi tiết khác | | hai râu dài hồng san hô, miệng có mảnh hàm nhỏ, túm rong trên đá |

**Khác Kuba** (cua pha lê đã có trên đảo): Kuba đỏ cam, pha lê xanh mọc trên mai, hai mắt tròn trắng to, hai càng tròn bằng nhau,
bụng kem, đứng thẳng như cua thường. Thạch Giải không có pha lê, không đỏ cam, không đối xứng, đá là nhà rời có cửa, bóng dáng
"tảng đá to bên trái + cua ló ra bên phải".

**Bảng màu** (không trùng 13 tướng Thủy đang có: chưa tướng nào dùng lam xám slate làm màu chính, chưa ai có đá bazan + điểm
hồng san hô):

| Vùng | Dạng 1 | Dạng 2 |
|---|---|---|
| Vỏ cua (đầu, càng, chân) | lam xám `#6A8BBB` | giáp chàm đậm `#3D5486`, viền gai trắng ngà `#EFE6D2` |
| Mặt dưới, khớp | lam bọt nhạt `#BFE6E2` | lam lục `#7DCBC4` |
| Đầu ngón càng, mũi chân | xanh than `#2E3B57` | gần đen `#232C44` |
| Nhà đá | bazan xám than `#4B5160`, vết nứt `#7A8290` | bazan đen lam `#3A3D48`, vân tầng `#6E7280` |
| Điểm nhấn | hà kem `#F4EEDC`, mảng san hô hồng `#EE8C8C`, rong `#5DB34F` | hà `#EFE6D2`, vương miện san hô đỏ `#D9545F`, rong biển sẫm `#3F8F5A` |
| Râu | hồng san hô `#E98A86` | đỏ san hô đậm `#C84B4B` |
| Mắt | hổ phách `#F2B33D` | hổ phách `#F0A030`, đồng tử dọc |
| Lòng miệng | hồng sẫm `#C2505E` | `#B8405A` |
| Viền | mực nâu `#2B2118` | mực nâu `#2B2118` |

**Dạng 1, Thạch Giải** (chibi): cua ẩn sĩ con, tấm đầu và mắt to, chân ngắn mập; tảng đá tròn sần to hơn thân trước một chút, đáy
không chạm đất; càng búa (phía gần) cầm thấp trước ngực, càng nhỏ giơ cạnh cuống mắt; mặt cau có quả quyết, miệng hé.

**Dạng 2, Thạch Thành Giải** (dạng cuối, trưởng thành): đầu nhỏ (khoảng 1/5 chiều cao), mắt hẹp xếch đồng tử dọc, mảnh hàm thành
hai nanh; giáp chàm viền gai trắng ngà khắp mai và chân; nhà đá thành **cột đá biển bazan đen cao hơn rộng**, ba bốn đỉnh nhọn có
vân tầng, vương miện san hô đỏ phân nhánh như gạc, hai dải rong rủ bên trái; **càng búa bọc găng đá bazan** to bằng cả thân trước,
giơ cao sẵn nện; càng xa thành kìm dài lưỡi cưa. Bóng dáng đổi từ "khối tròn thấp" sang "tháp cao nhọn + càng búa giơ cao".
Giữ để nhận ra cùng dòng: cua ẩn sĩ cõng nhà đá, mắt hổ phách trên cuống, râu hồng đỏ, một càng búa + một càng nhỏ, hà kem.

**Đòn và chiêu** (phần lớn đứng tại chỗ; con nặng cõng đá nên không lao; dạng sau đổi kiểu, mạnh hơn):

| | Dạng 1 Thạch Giải | Dạng 2 Thạch Thành Giải |
|---|---|---|
| `attack` | **Búng Càng** (kiểu tôm gõ mõ): ngả về sau giơ càng búa, bập "tách" một nhát, nhả một viên đạn bọt áp suất bay thẳng (VFX). Đứng tại chỗ, giật lùi nhẹ. Sự kiện `trung`; chỗ phát xương `mieng_cang` (đầu càng) | **Búa Càng** (Crabhammer): giơ găng đá cao quá đầu, lấy đà dài, nện xuống đất tại chỗ: sóng chấn nước + đá vụn chạy dọc đất tới đối thủ (`flyw`). Sự kiện `trung` lúc nện |
| `cast` | **Bọt Nước** (Bubble Beam): ngửa nhẹ tụ, há miệng nhả chuỗi bong bóng nối nhau thành dòng (VFX), giữ dáng tới hết dòng. Sự kiện `phun`, `het_phun`; xương `mieng` (trục x chĩa hướng nhả) | **Pháo Áp Suất** (Hydro Pump kiểu tôm gõ mõ): chĩa càng búa về đối thủ, ngón càng bập liên hồi, mỗi lần bập nhả một luồng nước áp suất nối thành tia; thân rung hai dáng lúc giữ. Sự kiện `phun`, `het_phun`; xương `mieng_cang` (trục x dọc càng) |
| `skill` | **Đá Ngầm Trồi** (Rock Tomb + nước): thụt vào nhà đá tụ lực (đá rung), bật ra nện càng búa xuống đất: hàng cột đá + mạch nước trồi nối nhau dọc đất tới đối thủ (`line_erupt`). Sự kiện `nen`, `troi` | **Xoáy Thạch Thành** (Whirlpool + Stone Edge): cắm bốn chân, nện găng hai lần, vương miện san hô rung; dưới chân đối thủ một xoáy nước cuốn đá vụn quay nhanh dần, cuối cùng một cột đá bazan + cột nước bật lên (`vortex`, `far`). Sự kiện `gam`, `xoay`, `troi`, `het_gam` |

Hiệu ứng (đạn bọt, bong bóng, sóng chấn, cột đá, xoáy) thuộc lớp VFX trên sân, không vẽ trong rig; rig để xương chỗ phát và sự
kiện (đặc tả mục 1, 5).

## 3. Concept (pha 1, đã duyệt 2026-11-11)

- Dạng 1 đã duyệt: `inbox/tm02_1/tai_ve/L1_duyet.png` (= `L1_concept_2.png`). Bản khác: `L1_concept.png` (vỏ lam ngô quá rực, một
  chân khuất sau tay càng), `L1_concept_3.png` (mặt sạch nhưng kém dữ, khung sát mép).
- Dạng 2 đã duyệt: `inbox/tm02_2/tai_ve/L1_duyet.png` (= `L1_concept_2.png`, nghiêng 3/4 phải, 4 chân). Bản khác: `L1_concept.png`
  (màu chàm đúng, mắt dữ hơn, nhưng 5 chân, mặt gần nhìn thẳng, nhiều gai).
- Gói prompt: `ArtGen/Spine/build_tm02.py` → `gui_gpt/tm02_<k>/luot_1_concept.txt`, `luot_2_manh.txt`, `HUONG_DAN.md`.

## 4. Pha 2 đã làm (2026-11-11)

**Cách lai** (đặc tả mục 5): mọi lớp **cắt thẳng từ concept** (`tm02_lai.py`, chạy bằng venv có cv2):
- nhãn: nét mực nâu (tối và B − R < 10; xanh than ngón càng, đá bazan không bị coi là mực) là tường; mỗi cụm màu theo đa giác /
  dải (đường giữa + bán kính) chiếm đa số, ưu tiên khối lớn trước để chân, càng, mắt giành phần chồng; cằm ép theo đa giác; san hô,
  rong lọc theo màu;
- nét mực chung: về lớp vẽ TRƯỚC, đồng thời chép vào lớp dưới nếu lớp dưới khai là nằm dưới lớp đó (mỗi lớp giữ trọn viền khi lệch);
- lớp dưới **mọc thêm ≥ 30 px** dưới lớp trên: dải (chân, râu, tay càng, ngón động) mọc theo trục lùi về gốc thành ống liền; vùng
  khác khép mép (đường viền đoán trơn); vẽ bù bằng inpaint màu chính lớp, kẻ nét mực mép phần mọc; nhà đá dưới thân lấp màu lòng
  cửa tối trong một elip (khi thân thụt vào thấy một cái cửa hang tối có viền);
- kiểm ghép lại mọi lớp: **lệch so với concept 0 điểm ảnh** (cả hai dạng);
- **mắt nhắm làm từ chính mắt concept** (tô tròng bằng hạt màu nắp mí thật, giữ viền, kẻ nét mí): **còn hở 0 px**; tờ GPT M01 chỉ
  dùng lòng miệng (mắt nhắm GPT vẽ không khớp nắp mí concept nên để dự phòng).

**Rig** (`tm02.py`, thư viện `quai/`): `root → move → than` (thân cua) và `nha` (nhà đá, cứng 100%), `dau` (mặt, vùng trước thân hoà
mềm), `ham` (môi dưới, lưới hai xương), cuống mắt 2 đốt + mắt (lò xo), râu 6 đốt (lò xo), rong 4 đốt (lò xo), tay càng 2 đốt + lòng
càng `k*` + ngón động `n*` (dạng 2: ngón là lớp riêng; dạng 1: một lớp liền, ngón bẻ bằng trọng số vùng), 4 chân × 3 đốt (IK hai
đoạn, bàn giữ góc), san hô 5 nhánh (dạng 2). **Mặt nạ cắt** (lồi) bên phải mép trong vành cửa: thân, mắt, càng thụt vào nhà thì biến
mất sau vành (hit thụt nửa, skill dạng 1 thụt rồi bật ra, die thụt hẳn, appear ló ra, evolve). Xương chỗ phát: dạng 1 `mieng` (miệng,
cast Bọt Nước) + `mieng_cang` (khe càng búa, attack Búng Càng); dạng 2 `mieng` (miệng càng búa, cast Pháo Áp Suất) + `mieng_mom`.
Lưới theo chiều cao (`buoc_theo_cao`), dải có mũ tròn; dải nào còn hở thì chuyển lưới vùng + trọng số B-spline chiếu lên trục.
Idle: mọi dao động bằng 0 ở khung 0 (khung 0 idle = dáng concept); clip không lặp: nền idle nhân bao 0 → 1 → 0, khung 0 khớp đúng khung
0 idle cả phần lò xo (`khop_dau`), khung cuối hoà về idle (thư viện).

Kết quả, soi, việc còn lại: xem báo cáo pha 2 và `inbox/tm02_<k>/rig/so_sanh.md`.

## 5. Dự kiến pha 2 lúc pha 1 (đã thay bằng cách lai ở mục 4)

Dựng như Hải Long (`pokiclash-spine-rig` mục 20): concept chỉ làm mốc; GPT vẽ tờ mảnh rời vẽ đủ phần bị che; rig bằng mã ra JSON
Spine 4.2 rồi `.atomik` (`ArtGen/Spine/tm02.py`, dùng thư viện `quai/` khi xong).

**Tờ mảnh dạng 1** (mỗi tờ 1536 × 1024, mảnh rời nhau ≥ 60 px):
- M01 nhà và thân: tảng đá nhà vẽ trọn (cả phần sau thân cua, cửa đá là lỗ tối); **vành trước cửa đá** rời (để thân cua thụt vào
  nằm sau vành, hoặc dùng mặt nạ cắt bản 3); thân trước + tấm đầu (không cuống mắt, râu, càng, chân; phần sau vẽ dư để lùi vào đá);
  mảnh hàm dưới có lòng miệng; túm rong 3 dải vẽ duỗi thẳng.
- M02 mặt: hai cuống mắt + mắt mở (vẽ duỗi), mí nhắm phủ kín mắt (to, nhỏ), một râu duỗi thẳng (dùng cho hai râu), nắp mí giáp.
- M03 càng: càng búa = cánh tay trên, cẳng, lòng càng liền ngón cố định, **ngón động rời**; càng nhỏ cùng cách.
- M04 chân: một chân gần 3 đốt duỗi thẳng, một chân xa (dùng lại, lật bằng tỉ lệ âm cho 4 chân).

**Xương dạng 1** (ước 52; con gốc 39): `root → move → ground` (4 đích IK chân) `→ base` (nhún) `→ body` (thân cua: ló ra / thụt
vào nhà) và `shell` (nhà đá, cứng 100%, trễ nhún nửa nhịp); `head`; cuống mắt mỗi bên 2 đốt + mắt (lò xo); râu mỗi bên 5 đốt
(dây mềm nướng, gió sin); `jaw` + `mieng`; càng búa: vai, cánh, cẳng, lòng, ngón + `mieng_cang`; càng nhỏ 5; 4 chân × 3 (IK 2
xương + đốt chót); rong 3 dải × 3 đốt (dây mềm). Lưới: thân, cuống mắt, râu, rong, chân là dải lưới trọng số B-spline (không
cột nào bám 100% một đốt); nhà đá, lòng càng là đồ cứng.

**Dạng 2** (ước 64): như dạng 1, thêm tháp đá (cứng), vương miện san hô 3–4 nhánh (cứng, lắc trễ nhẹ), rong 2 dải × 4 đốt, găng đá
cứng trên lòng càng búa, càng xa lưỡi cưa, gai giáp đi theo từng đốt chân.

**Clip** (nhịp theo `skill-petclash` 7.1 và con gốc; dạng 2 lấy đà dài hơn, nặng hơn):
- `appear`: tảng đá rơi xuống đất nảy một lần (bụi), cua ló mắt ra trước, rồi bật càng, về khung 0 `idle`.
- `idle` 2,0 s (dạng 2: 2,4 s): nhún hai lần một vòng, nhà đá trễ nửa nhịp; cuống mắt, râu, rong lệch pha; điểm phá nhịp: kìm
  nhỏ bập hai cái (học con gốc), chớp mắt một lần ở giờ khác.
- `attack` 0,9 s / 1,1 s; `cast` 1,0 s / 1,6 s; `skill` 1,7 s / 2,0 s; `hit` 0,6 s (khung 0 đã bị đẩy, đỉnh 0,07 s, mắt nhắm,
  cuống mắt cụp, thân thụt nửa vào nhà); `die`: giật, nhắm mắt, cua thụt hẳn vào nhà, tảng đá lắc lư giữ một nhịp rồi lăn nghiêng,
  tan, khung cuối trống.
- `evolve` (dạng 1): thụt vào nhà, đá rung nứt, lốc nước; đổi dạng lúc lốc đậm nhất; tháp đá dạng 2 trồi lớn, cua bật ra giơ găng gầm,
  khung cuối trùng khung 0 `idle` dạng 2.
- `aura` (tuỳ): vài bong bóng nhỏ trôi lên từ cửa đá.
