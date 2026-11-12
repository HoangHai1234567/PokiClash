# Bạch tuộc quái vật (mã làm việc `bach_tuoc`): tướng thứ 5 đảo Thủy theo lời người dùng (2026-11-12)

Tên chưa đặt; mã `bach_tuoc` chỉ để đặt thư mục. Con gốc của rig: `monster_3616` (game tham khảo). **Con này là DẠNG 2**
(`bach_tuoc_2`); dạng 1 chưa có ý. Mỗi dạng tối đa 0,5 MB.
Lưu ý số thứ tự: `ran_sung` (rắn sừng) cũng ghi là "tướng thứ 5 đảo Thủy" (2026-11-11). Chưa hỏi lại người dùng là thay rắn sừng
hay đánh số lại; chỉ ảnh hưởng lúc vào game.

Tệp: `ArtGen/Spine/bach_tuoc.py` (part gốc, thiết kế phẳng theo khung part, sơ đồ bố cục, tờ mảnh), `build_bach_tuoc.py` (gói GPT),
`bach_tuoc_clip.py` (clip riêng ở tầng điều khiển của rig gốc), `bach_tuoc_rig.py` (rig). Gói: `gui_gpt/bach_tuoc_2/`, ảnh về
`inbox/bach_tuoc_2/tai_ve/`.

## 1. Ý người dùng (nguyên văn tóm lại, kèm ảnh chụp `monster_3616`)

- Concept: **bạch tuộc quái vật**.
- `idle`: giống con gốc, sửa một chút cũng được.
- `appear`: **gen thêm một cái hố đất trồi lên (tách 2 layer trước, sau)**; bạch tuộc **đưa các chân lên rồi kéo phần thân lên**.
- Đòn thường: **đấm** vào đối thủ (**kéo dài xúc tu ra**).
- Chiêu mana: **bắn ra một quả bóng mực màu đen**.
- Chiêu cuối: như `skill_04`: **giơ 2 vòi bên ngoài lên uốn uốn kiểu triệu hồi**; quanh bạch tuộc **triệu hồi ra các bạch tuộc mini**
  (bạch tuộc con) **bò tới gần kẻ thù rồi nhảy mạnh vào người kẻ thù**.
- Làm thêm **animation walk**.
- Con này là **dạng 2**; mỗi dạng tối đa **0,5 MB**.

Người dùng không dặn màu, chi tiết. Thiết kế ở mục 3 là **đề xuất của Claude**, chờ duyệt concept.

## 2. Mổ xẻ con gốc `monster_3616` (chỉ học cách tách và nhịp)

Nguồn: `D:\Ripper\SwordxStaff\web\assets\Monster\monster_3616\` (Spine 4.2.28, skel 65 KB, ảnh 872 × 624, tỉ lệ atlas 0,5).
Kết quả quét: `D:\Ripper\SwordxStaff\scan\monster_3616\` (`info.json`, `att_goc.json`, `manh_anh.png`, `manh_dang_goc.png`,
`parts/`, tờ khung `khung/`, `can/`, mẫu điều khiển `sample_dk.json`, bản chép để chạy clip tự viết `lam_clip/`).

- 58 xương, 30 slot, 11 clip, 3.677 khoá. Lưới thưa (6–33 đỉnh mỗi mảnh), mọi mảnh là lưới có trọng số.
- Con gốc **nhìn sang PHẢI** (+x là phía trước): con mắt nhìn về phía ba xúc tu NGẮN; hai xúc tu to lộ mặt dưới ở bên trái là phía
  sau; xúc tu 6 (`bone27..31`) là xúc tu TRƯỚC. Đúng chiều game cần, **không lật** (`bach_tuoc_rig.LAT_X = 1`).
  Tôi đã đoán sai là nó nhìn trái (vì `skill_02` quật xúc tu to về bên trái) và lật cả con trong ba bản concept đầu; người dùng
  2026-11-12: "**hướng mắt bạn ngược rồi, trong game mắt hướng cùng với bên xúc tu ngắn, của bạn gen bị ngược**".
- Ràng buộc: 3 IK hai đốt (`CJ1` trên `bone7, bone8`; `CJ2` trên `bone27, bone28`; `CJ3` trên `bone12, bone13`; mục tiêu là con của
  `bone2`), 8 path constraint (mắt xích `bone39..46` chạy trên đường cong `lujing` gắn `bone3`). Clip bật tắt IK bằng độ trộn
  (skill_02: CJ3 tắt; skill_03, skill_04: CJ2, CJ3 tắt; die: tắt cả; run: đổi giữa chừng).
- Đổi ảnh: chỉ con mắt (3 hình trong slot `P_yanjing1`: mở, lim dim, nhắm). `run_01` có đổi độ trong (chìm xuống đất).

### Bảng mảnh (thứ tự vẽ sau → trước; cỡ là ảnh trong atlas, ngoài rig gấp đôi)

| # | Slot / hình | Cỡ | Là gì | Xương bám |
|---|---|---|---|---|
| 1 | `P_shanhu6` | 70 × 78 | cụm san hô nhỏ sau vỏ, mép trên | bone33 |
| 2 | `P_chuanban2` | 221 × 237 | mặt trong của mảnh tàu (tam giác sẫm sau đầu) | bone32 |
| 3, 4 | `P_shou6_2`, `P_shou6_1` | 109 × 159, 166 × 122 | xúc tu sau (ngọn, gốc) | bone29–31; bone27–30 |
| 5 | `suolian8` | 65 × 67 | mắt xích cuối | bone39 |
| 6 | `P_tou` | 450 × 330 | đầu vòm | bone3–6, bone76 |
| 7 | `P_yanjing1 / 2 / 3` | 53 × 65 | mắt mở / lim dim / nhắm | bone75 |
| 8–10 | `P_shou5_1`, `P_shou4_1`, `P_shou3_1` | ~100 × 135 | ba xúc tu nhỏ ("ngón") dưới đầu | bone24–26; 21–23; 18–20 |
| 11 | `P_shou1_3` | 162 × 112 | khối gốc xúc tu trước (elip trơn) | bone77–79 |
| 12–18 | `suolian7..1` | ~50–67 | bảy mắt xích | bone40–46 (trên đường cong) |
| 19 | `P_chuanban1` | 508 × 396 | mảnh thân tàu (mũ) | bone32 |
| 20–24 | `P_shanhu5..1` | 31–148 | năm cụm san hô trên mũ | bone34–38 |
| 25 | `P_shou1_2` | 161 × 128 | xúc tu 1, đoạn gốc | bone12, 13 |
| 26 | `P_shou2_2` | 109 × 100 | xúc tu 2, đoạn gốc | bone7 |
| 27 | `P_shou1_1` | 129 × 217 | xúc tu 1 (trước nhất), đoạn ngọn có giác hút | bone14–17 |
| 28 | `P_shou2_1` | 161 × 145 | xúc tu 2 (móc trước thân), đoạn ngọn | bone8–11 |

### Cây xương (rút gọn)

```
root → bone2 (dời cả con; mục tiêu IK CJ1..3, shadow) → bone → bone3 (thân: dời, nghiêng)
  ├─ bone4 → bone5 → bone6     đầu (co giãn, nghiêng); bone5: bone32 (mũ → bone33..38, 47: san hô), bone75 (mắt), bone76
  ├─ bone12 → 13 → 14 → 15 → 16 → 17    xúc tu 1 (trước nhất; IK CJ3 trên hai đốt gốc)
  ├─ bone7 → 8 → 9 → 10 → 11            xúc tu 2 (IK CJ1)
  ├─ bone27 → 28 → 29 → 30 → 31         xúc tu 6 (sau; IK CJ2)
  ├─ bone18–20, 21–23, 24–26            ba ngón nhỏ
  ├─ bone77 → 78 → 79                   khối gốc xúc tu trước
  └─ bone48 → bone39..46                xích (8 mắt, chạy trên đường cong)
```

### Clip của họ (11)

`idle_01` 4,0 s (thở, ba xúc tu lớn xê dịch bằng mục tiêu IK, chớp mắt); `run_01` 4,53 s (nhún rồi **chìm xuống đất** 0,6 → 2,5,
**trồi lên** 2,76, vọt lên không 2,96, rơi về); `skill_01` 1,83 (nhổm cao rồi dập xuống); `skill_02` 1,83 (xúc tu 1 giơ lên rồi
quật xuống trước mặt); `skill_03` 1,9 (co xúc tu 1 trước mặt 0,5 → 0,77 rồi quét hai bên 0,83 → 1,03); `skill_04` 2,0 (giơ xúc tu 1
và 6 lên 0,22 → 0,67, bổ xuống 0,89); `hit_01` 0,5; `hit_02` 0,67; `die_01` 1,0 (mũ sập xuống); `stun_01` 1,33; `block_01` 0,5.

## 3. Thiết kế (đề xuất của Claude, chờ duyệt)

### Bản 1 (bị trả 2026-11-12)

Bạch tuộc tím mực `#5B4A8C`, đội mảnh vỏ ốc khổng lồ màu xương thay mảnh thân tàu của con gốc, san hô đen, xích neo rỉ, một mắt.
Người dùng xem concept (`tai_ve/_bo/L1_concept_ban1_tim_vo_oc.png`) rồi dặn:
- "**không nhất thiết phải thiết kế có cả phần tàu ở trên đâu, bạn có thể bỏ phần đấy, phần xúc tu cũng có thể làm khác đi**";
- "**đổi màu khác đi, màu tím này không đẹp, thử phối đúng màu hồng đỏ giống bạch tuộc bình thường xem**".

### Bản 2: bạch tuộc hồng đỏ, đầu trần

| Phần | Con gốc | Của mình |
|---|---|---|
| Da | lam | **hồng đỏ san hô** `#D45C4E`, đốm đỏ sẫm `#B03E3A` trên đỉnh và sau đầu, trên lưng xúc tu |
| Trên đầu | mảnh thân tàu gỗ + san hô + xích (19 part) | **bỏ hết**; thêm **mào ba gai thịt** đỏ sẫm `#8A2C30` sau đỉnh đầu (part của mình) |
| Mắt | nhìn nghiêng: **một mắt** cam giữa vòm đầu, trong vành hốc mắt tròn | **giữ đúng cách dựng đó**: một mắt vàng `#F4C84A`, **con ngươi ngang** lệch về phía trước, mí đỏ sẫm, vành hốc mắt tròn + bướu nhỏ; thêm một **gờ mày** đỏ sẫm (nếp da thuôn hai đầu) dốc về phía trước |
| Mồm | không có | **không có** (bóng mực phụt từ dưới mép trước của đầu, sau xúc tu trước: xương `mieng`) |
| Mặt dưới xúc tu | hồng, giác hút hồng sẫm | **kem** `#F7E4D2`, giác hút hồng cam `#ECAA96` có tâm sẫm |
| Hướng | nhìn phải (mắt hướng về phía xúc tu ngắn) | **giữ nguyên**, không lật |

Bảng màu ở `bach_tuoc.PAL` và `build_bach_tuoc.PALETTE` (đổi thì sửa cả hai). Part bỏ: `bach_tuoc.BO`; gai: `bach_tuoc.GAI`. Xương của phần đã bỏ (`bone32–48` trừ `bone75–79`) không vào rig (`bach_tuoc_rig.BO_XUONG`).
**Bản 2 lượt đầu bị trả (2026-11-12)**: tôi đã tự thêm mắt thứ hai (nhìn chéo ra trước) và một cái phễu phụt mực trên má. Người dùng
(kèm ảnh con gốc): "**hướng mặt/mắt sai rồi, xem lại con gốc, chỉ thấy 1 bên mắt, không có mồm**". Sửa: bỏ mắt xa (`MAT_XA = None`),
bỏ phễu; mặt dựng như con gốc (bảng trên). Concept gen lại từ bản nháp `L1_concept_2.png` với khối KEEP IDENTICAL / CHANGE chỉ sửa
mặt (`build_bach_tuoc.REVISE`) → `L1_concept_3.png`.

**Bản 3 bị trả (2026-11-12)**: hướng mắt ngược (xem mục 2). Sửa: bỏ lật ngang ở sơ đồ và rig; con ngươi, mí, gờ mày hướng về +x;
mào gai dời ra sau đầu (trên trái, `GAI`); concept gen lại từ bản nháp 3 đã lật ngang bằng mã (`mau/nhap_3_lat_ngang.png`) với khối
KEEP / CHANGE chỉ sửa hướng mắt và chỗ đặt mào → `L1_concept_4.png`. Clip: đấm đổi sang xúc tu 6 về +x, cast chúi về +x, walk bò về +x.

"Xúc tu làm khác đi": mới đổi màu, đốm, giác hút; hình bóng từng xúc tu vẫn theo part của rig (đổi hình bóng thì phải nới khung part).

## 4. Concept

- Sơ đồ bố cục `inbox/bach_tuoc_2/mau/bo_cuc.png` (`bach_tuoc.py bo_cuc`): mỗi part là hình bóng kín của nó tô phẳng theo thiết kế
  của mình (`thiet_ke`: chỉ lấy hình bóng, ranh mặt trên / mặt dưới xúc tu và chỗ đặt giác hút), đặt đúng chỗ dáng gốc, lật ngang;
  thêm mào gai, mắt xa.
- File prompt: `gui_gpt/bach_tuoc_2/luot_1_concept.txt` → `tai_ve/L1_concept.png` (bản 2 lượt đầu: gờ mày bị vẽ thành hai thanh chữ
  nhật như sơ đồ), `L1_concept_2.png` (gen lại với `--note`: gờ mày là nếp da thuôn hai đầu, dữ hơn, gai to hơn, mụn gai, sẹo).
  Ảnh mẫu: sơ đồ, rồng vây đã duyệt (nét), cá voi dạng 2 đã duyệt (mức dữ của dạng 2), bản đồ.
- Bài học: hình trên sơ đồ vẽ bằng nét thẳng (gờ mày = đoạn thẳng dày) thì GPT chép nguyên thành thanh chữ nhật; chi tiết hữu cơ
  phải vẽ cong, thuôn ngay trên sơ đồ hoặc dặn rõ trong prompt.

## 4b. Hố đất (appear)

`gui_gpt/bach_tuoc_2/luot_2_ho_dat.txt` → `tai_ve/H01.png` (một ảnh cả hố, lòng hố đen phẳng). `bach_tuoc.py cat_ho` tách hai lớp:
`manh/ho_sau.png` (lòng hố + vành sau + hai đầu), `manh/ho_truoc.png` (vành trước: đất nằm dưới đường ngang qua tâm lòng hố), và
`manh/ho.json` (elip lòng hố). Rig: `ho_sau` vẽ đầu tiên, `ho_truoc` vẽ sau thân; **mặt nạ cắt** (slot `cat`, xương `cat_x`) giữ phần
trên mặt đất + lòng hố nên thân ở dưới đất không lộ. Mặt nạ của `.atomik` luôn bật và phải LỒI: đáy là đoạn giữa nửa dưới elip miệng
hố, hai bên đi theo tiếp tuyến ra xa (để ngọn vòi úp xuống đất quanh hố vẫn thấy), vách dựng đứng; ở dáng gốc xương `cat_x` nằm
sâu 3.000 và phóng 12 lần (không cắt gì), clip appear thu về đúng cỡ cho tới lúc thân vọt lên cao nhất.

## 5. Clip (dựng ở tầng điều khiển của rig gốc, `bach_tuoc_clip.py`)

| Clip game | Nguồn | Diễn |
|---|---|---|
| `idle` | `idle_01` | nguyên |
| `appear` 2,75 s | tự dựng | thân nằm sâu 980 đơn vị dưới đất, giữ dáng nghỉ. **Hai tay chống** là hai xúc tu DÀI riêng (ảnh `tai_ve/V01.png` → `manh/voi.png`, dải lưới 10 đốt `vt*`, `vp*`, vẽ sau thân, trong mặt nạ cắt; bạch tuộc 8 tay, rig lộ 6, đây là hai tay khuất): vươn lên khỏi hố 0,28 → 0,7, ngoe nguẩy; lấy đà rồi **vung đập xuống mặt đất hai bên miệng hố** 0,86 → 1,00 (`bam_dat`); **ngọn bám yên một chỗ**, đoạn ngọn nằm bẹt chĩa ra ngoài; gồng 1,00 → 1,20; **chống đẩy** thân vọt lên 1,20 → 1,62 quá đà 120 (tay ngắn lại thì vồng cao như khuỷu); thân rơi về chỗ, nhún; **thu tay** 1,86 → 2,44 (người dùng: "2 xúc tu thêm kia nên làm thêm 1 đoạn thu nó lại sau khi xuất hiện, thu vào trong sau đầu"): ngọn nhấc khỏi đất, cong lên vào trong, rồi cả tay TRƯỢT vào sau đầu (gốc tay trượt sang bên kia đầu nên tay giữ chiều dài, ngọn khuất sau cùng; `VOI_TRONG`). Tay chạy dọc đường cong bậc ba tính từng khung (`bach_tuoc_rig.tay_chong`), giãn / co bằng DỜI xương con. Lịch sử: (1) vòi vẫy trên không rồi thân tự bật → "phải để các xúc tu chạm đất nữa thì mới đẩy được cơ thể lên"; (2) kéo dài xúc tu ngắn của thân 2,5 lần cho chạm đất → "nhìn hơi xấu, bị gãy mesh nhiều" (lưới của họ 20–30 đỉnh, vẽ ở dáng cuộn); (3) tay riêng dải lưới |
| `attack` 1,15 s | `skill_03` co giãn thời gian | đấm bằng xúc tu TRƯỚC (xúc tu 6) về +x. Lấy đà: thân ngả sau, xúc tu 6 co lên cao (0 → 0,34); đấm: duỗi thẳng ra trước chếch lên 23°, vươn dài ~2,5 lần (0,34 → 0,44, `trung` 0,44); giữ 0,54; rút về |
| `cast` 1,5 s | `skill_01` | hít phồng (nhổm, ngả sau, đầu phồng) 0 → 0,48; phụt 0,62 (`phun`): dập ra trước, đầu xẹp, nhắm mắt; về. Bóng mực là VFX |
| `skill` 3,1 s | `skill_04` | giơ xúc tu 1 và 6 (0 → 0,5); múa gọi tới 1,65 (sóng gốc → ngọn, hai vòi lệch pha, vươn cao 1,3 lần, nhắm mắt); `trieu_hoi` × 4 (0,62 / 0,92 / 1,22 / 1,52); bổ xuống 1,77 (`lenh`); năm bạch tuộc con (ba trước, hai sau thân) bò ba nhịp 0,52 s rồi nhảy bổ 0,24 s vào đối thủ, `trung` 2,58 → 2,86 |
| `walk` 1,2 s lặp | tự dựng trên dáng nghỉ | ba mục tiêu IK lần lượt nhấc – vươn – bám – kéo, thân nhô, ba ngón gợn sóng |
| `hit`, `die` | `hit_01`, `die_01` | nguyên |

Bài học khi viết clip con này:
- **Tỉ lệ xương cộng dồn xuống con cháu**: đặt tỉ lệ dọc 2 lần trên cả 5 đốt của một xúc tu là ngọn dài gấp 2⁵. Muốn vươn dài chỉ đặt
  ở XƯƠNG GỐC của chuỗi (lúc chuỗi đang thẳng thì dài đều); thêm tối đa một nấc ở giữa.
- Xương cha có tỉ lệ lệch trục thì con xoay sẽ bị xô nghiêng: gập ngọn lúc đang kéo dài ra thành gai nhọn (xúc tu 2 ở appear) →
  chuỗi đang kéo dài chỉ ngả ở gốc, hoặc gập ít.
- Vươn dài phải bắt đầu SAU khi chuỗi đã chĩa đúng hướng, không thì khung giữa chừng quét một vòng qua đầu.
- **Kéo dài ở đúng đốt**: hai đốt gốc của xúc tu 1 (`bone12, 13`) và xúc tu 2 gập vuông với đoạn ngọn; đặt tỉ lệ dọc ở đó thì
  đoạn ngọn bị xô dẹt thành sợi. Hoặc duỗi thẳng cả chuỗi trước (đấm, appear), hoặc đặt tỉ lệ ở đốt gốc của ĐOẠN NGỌN (`bone14`,
  `bone29` trong skill).
- **Slot chỉ dùng trong một clip phải ẩn TRƯỚC đoạn hoà cuối clip**: bộ xuất hoà 0,2 s cuối mỗi clip về khung 0 idle (`khop_idle`), tức
  kéo xương về tư thế gốc. Hai tay chống còn hiện tới sát cuối appear nên mấy khung cuối chúng duỗi thẳng thò ra mờ mờ sau đầu (người
  dùng: "có mấy frame bị lỗi"). Mốc ẩn (`P_THU_HET` + trễ) phải sớm hơn `P_DUR − 0,2`; `bach_tuoc_clip` có `assert` giữ điều này.
- **Góc nối liền kết thúc lệch ±360**: xúc tu của appear vung qua đầu rồi về dáng nghỉ theo ngả khác; sau khi `unwrap`, khoá cuối lệch
  một vòng so với idle, bước hoà cuối clip (`khop_idle`) quay nó thêm một vòng (xúc tu văng xuống đất 0,2 s cuối). `bach_tuoc_rig` trả
  bội 360 bằng một bước nhảy lúc cả con còn ẩn (`QUAY_AN`), clip khác thì in cảnh báo.
- `mo_xe.html` thêm: `sample` xuất `k` (độ trộn, chiều gập từng IK); `extra` nhận `iks: {tên: [[t, độ trộn, chiều gập]]}`.

## 5b. Mảnh và rig (2026-11-12, concept `L1_concept_4.png` = `L1_duyet.png`, người dùng: "ok ổn")

Lệnh: `bach_tuoc.py nhom_part` → `build_bach_tuoc.py` → `gen.py luot_3_part_Q1..Q4.txt`, `luot_3_bach_tuoc_con.txt` → `bach_tuoc.py cat_part
Q1 Q2 Q3 Q4` → `cat_con` → `can_mau` → `so_part` → `quai/khoa.py nang -- bach_tuoc_rig.py` → `mo_xe/chay.py sheet` (runtime Spine thật).

- **Tờ hướng dẫn** (`mau/part_Q1..Q4.png`): mỗi part của rig một ô đúng khung ảnh vùng (× 2; part nhỏ × 4), trong ô là hình bóng kín tô
  phẳng bằng mã (`thiet_ke`): đốm và sẹo trên đầu đặt theo concept đã duyệt (`DOM_DAU`, `SEO`: đọc toạ độ trên concept, đổi về thế
  giới của rig), vành hốc mắt, gờ mày; xúc tu: ranh da / kem và chỗ giác hút lấy theo part gốc; ba gai mào là ô của mình.
- **Bo chỗ bị khung cắt** (`bong`): làm trơn hình bóng trên ảnh đã đệm viền trống → góc cắt thẳng thành bo tròn, hết mấu nhọn ở chỗ nối;
  đầu bo mạnh (σ 13 × z) vì mép phải vòm đầu bị khung cắt thẳng ~70 đơn vị (con gốc che bằng xích, của mình lộ).
- **Kết quả cắt**: 14 part IoU 0,95–0,99 với hình bóng; ba gai 0,76–0,83 (GPT vẽ gai thon hơn; gai là ô cứng 4 đỉnh nên không khuyết).
- **Cân màu** (`can_mau`): mỗi tờ Codex tô đỏ một sắc hơi khác (lệch tới 14 mức ở kênh đỏ giữa các ngón); lấy trung vị màu da của đầu
  làm chuẩn, cộng độ lệch vào điểm da và điểm kem của từng mảnh xúc tu. Màu da sau cân (249, 89, 70) khớp concept (249, 92, 74).
- **Mắt** phóng 1,35 lần quanh tâm (`MAT_TI`) cho gần kín vành hốc mắt như concept; ba hình mắt là ba slot bật bằng độ đậm.
- **Idle**: biên độ xoay của `bone14..17` (ngọn xúc tu to phía sau) giảm còn 50% (`GIAM`): ở 45–86 độ lưới thưa của ngọn tự gập thành
  mép răng cưa; con gốc cũng vậy nhưng mép mũ tàu che mất. Kiểm bằng runtime Spine thật phóng vào chỗ đó (`rig/spine_that/can2/idle.jpg`).
- **Bạch tuộc con**: `tai_ve/C01.png` → `manh/con.png`; năm slot `con0..4` trên xương `fly_c0..4` (+ xương con `c<i>` nhún, xoay), `far` ở
  (640, 150). `game.far = ["skill"]`.
- **Hố**: lớp sau chờm 8 px xuống dưới đường tách (hai lớp chỉ giáp mép thì hở một vạch nền mảnh ở hai đầu hố).
- **Số đo sau khi thêm hai tay chống**: 73 xương, 27 slot, 899 đỉnh, 1.307 tam giác, 11.684 khoá, atlas 984 × 1056, `.atomik` **251 KB**.
- **Số đo (bản trước)**: 53 xương, 25 slot, 325 đỉnh, 347 tam giác, 8 clip (`appear, idle, walk, attack, cast, skill, hit, die`), 10.642 khoá, atlas
  960 × 1056, `.atomik` **229 KB** (trần 500 KB). Mọi clip không lặp nối về khung 0 idle lệch 0 px; appear khung đầu trống; die khung cuối
  trống. Trang xem: `rig/xem.html` (mở bằng file://).
- **Chưa làm**: vào game (Unity: chép `.atomik` + chân dung, `heroes.json`, gắn prefab); dạng 1; VFX bóng mực; tinh chỉnh cú lao của đòn
  thường theo quãng thật trong trận.

## 5c. Dạng 1: con non (2026-11-12, người dùng: "làm dạng 2" → hỏi lại → "Dạng 1, con non"; concept "ok duyệt")

Cùng rig, cùng lưới, cùng clip với dạng 2; chọn dạng bằng biến môi trường `BT_DANG=1` (mặc định 2) cho `bach_tuoc.py`,
`build_bach_tuoc.py`, `bach_tuoc_rig.py`. Thư mục `inbox/bach_tuoc_1/`, gói `gui_gpt/bach_tuoc_1/`.

| | Dạng 1 (con non) | Dạng 2 |
|---|---|---|
| Da | hồng san hô nhạt `#EE7C6C` (đo trên mảnh: 253, 124, 104) | hồng đỏ `#D45C4E` (249, 89, 70) |
| Đầu | to hơn: xương `bone5`, `bone76` phóng 1,13 | như con gốc |
| Xúc tu | ngắn, mảnh hơn: xương gốc từng xúc tu thu 0,84 (ba ngón 0,9) | như con gốc |
| Mắt | rất to (`MAT_TI` 1,62), vành hốc mắt bán kính 128, mí mỏng, gờ mày nhỏ | `MAT_TI` 1,35, vành 96, mí và gờ mày nặng |
| Mào | hai gai nhỏ mới nhú | ba gai |
| Đốm, sẹo | năm đốm, không sẹo | mười đốm, một sẹo |
| Chiêu cuối | 3 bạch tuộc con | **6** (người dùng 2026-11-12: "dạng 2 gọi nhiều bạch tuộc mini hơn (6 con)"; ba con trước, ba con sau / dưới thân) |
| `appear` | **nhảy vào** từ phía sau 1,25 s (người dùng: "dạng 1 appear làm nó nhảy vào là được"): vòng cung từ −0,8 chiều cao, đáp bẹp người + chớp mắt (`cham_dat` 0,46), nảy nhẹ một nhịp, nhún tắt dần; rig dạng 1 không mang hố, mặt nạ cắt, tay chống (`CO_HO`) | trồi lên từ hố, hai tay chống đẩy, thu tay sau đầu (2,75 s) |
| Cỡ trên sân | chiều cao khai = chiều cao đo × 1,2 (vẽ nhỏ lại) | chiều cao đo |

- **Concept**: sơ đồ bố cục dựng từ chính rig dạng 1 (`BT_DANG=1 bach_tuoc_rig.py bo_cuc <mau/bo_cuc.png>`: đã có tỉ lệ xương mới), ảnh 1
  là concept dạng 2 đã duyệt. `L1_concept.png` nét quá mảnh → gen lại với `--note` (nét đậm ~7 px như dạng 2, một vành hốc mắt) →
  `L1_concept_2.png` = `L1_duyet.png`.
- **Mảnh**: 4 tờ Q như dạng 2 (16 mảnh; IoU 0,94–0,99, hai gai 0,85–0,88), `can_mau`. Hố đất, bạch tuộc con, xúc tu dài dùng chung
  ảnh của dạng 2 (`TAI_CHUNG`); `cat_voi`, `cat_con` cân màu da về da đầu của dạng đang dựng.
- **Clip `evolve`** (`bach_tuoc_rig.tien_hoa`, `quai/tienhoa.py`): gộp bản NHẸ của dạng 2 (`BT_NHE=1`: ảnh 0,36 px / đơn vị, không hố,
  không tay chống, không bạch tuộc con; dựng ở tiến trình con rồi nạp bằng pickle vì cấu hình dạng đọc lúc nạp module). Con non thu
  người, đầu phồng, rung; đổi dạng ~1,2 s; dạng 2 hiện lớn hơn 1,17 lần, phồng đầu, hoà về khung 0 idle của nó.
- **Số đo dạng 1** (sau khi đổi appear sang nhảy vào): 92 xương, 36 slot, 602 đỉnh, 9 clip, atlas 960 × 1056, `.atomik` **225 KB** (gồm bản nhẹ dạng 2). Dạng 2 (6 bạch tuộc con): 75 xương, 28 slot, 903 đỉnh, 8 clip, **254 KB**.

## 5d. Vào game (2026-11-12, người dùng: "ổn rồi, thay thế vào game đi")

- **Suất**: tướng thứ 5 đảo Thủy = suất ải 20, id `so_ngoc` (Sò Ngọc; rig cũ `tm05`). (Suy từ bảng suất ở `quai/VAO_GAME.md`: suất 4
  là sò đột biến, suất 7 là cá voi đều khớp số thứ tự người dùng gọi; rắn sừng tuy từng gọi "thứ 5" nhưng đã vào suất ải 50 `uyen_xa`.)
- **Chép tay**: `inbox/bach_tuoc_<k>/rig/bach_tuoc_<k>.atomik` → `Assets/03 Art/Heroes/Resources/so_ngoc_<k>/so_ngoc_<k>.atomik`,
  `chan_dung.png` → `so_ngoc_<k>_portrait.png` (k = 1, 2). `quai/da_nhan.json` đã trỏ suất `so_ngoc` sang `bach_tuoc`.
- **Chiêu trong trận**: `StageView.WaterFx["so_ngoc"] = ("n_muc", {"n_va", "n_va"})`; `HatNuoc`: mã mới `n_muc` (bóng mực đen, dùng lại
  đường bay của viên ngọc `NNgoc` với cờ `muc`), `WThemes["so_ngoc"]` màu mực. Bạch tuộc con do rig lo (`game.far = ["skill"]`).
- **Đã biên dịch thử, chưa xem trong trận**: hai sửa đổi C# biên dịch sạch bằng trình biên dịch của chính Unity (`NetCoreRuntime/dotnet.exe`
  + `DotNetSdkRoslyn/csc.dll`, tệp `Library/Bee/artifacts/1900b0aE.dag/PokiClash.Game.rsp` với `-out` đổi ra thư mục tạm; cách này dùng
  được cả khi Editor đang mở). Không có cầu MCP tới Editor nên chưa xem trong trận. Việc cần làm trong Unity: bấm vào cửa sổ để Refresh, vào trận ải 20 đảo Thủy xem cỡ tướng, cú đấm, bóng mực, bạch tuộc con, nút Tiến hóa.
- **Tên** (2026-11-12, người dùng xác nhận suất `so_ngoc` là đúng, bảo "đổi đi" phần tên; Claude đặt, người dùng có thể đổi): tướng **Bát Trảo**,
  danh hiệu "Bạch tuộc quái vật gọi bầy", dòng "Dòng Bát Trảo", dạng **Trảo Nhi** / **Bát Trảo**; thẻ **Bóng Mực** (chiêu mana), **Gọi Bầy**
  (chiêu cuối), **Túi Mực** (bị động). Sửa `Assets/02 Data/Json/heroes.json`, `cards.json`, `quai/tuong_moi_thuy.py`, và sửa thẳng chuỗi tên
  trong `HeroDb.asset`, `CardDb.asset`. Golden không chứa tên nên không đổi. Con ngươi dạng 1 lệch phải: người dùng "thấy ổn rồi".
- **Chưa đổi**: id nội bộ (`so_ngoc`, `so_ngoc_skill|ult|pas`), biểu tượng thẻ (bubble, fang, moon). `appear`, `die`, `walk` chưa được game
  phát (StageView tự làm ra sân / chết; xem `VAO_GAME.md` mục 6).

## 6. Việc ngoài rig (VFX, game)

- **Bóng mực** của chiêu mana: VFX. Rig có xương `mieng` và sự kiện `phun`.
- **Bạch tuộc con** của chiêu cuối: đặt TRONG rig trên xương `fly*` (cơ chế có sẵn của game: `AolaActor.FarAtomik` dời xương `far`
  tới đối thủ và các xương `fly*` theo phần quãng đã đi), để người dùng xem được trọn chiêu trên trang xem. (Lựa chọn của Claude; nếu
  người dùng muốn để lớp VFX lo thì bỏ nhóm slot `con*`.)

## 7. Bản quyền

Xương, lưới, chuyển động (và hình bóng từng part) là của nhà phát hành game gốc; hình vẽ là của mình. Dùng nội bộ, không đăng công
khai, kể cả artifact (như aola).
