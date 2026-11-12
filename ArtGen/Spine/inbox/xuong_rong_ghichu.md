# Xương rồng tròn (`xuong_rong`): tướng đầu tiên đảo Mộc

Bắt đầu 2026-11-12. Con gốc của rig: `monster_3229` (game tham khảo, kho `D:\Ripper\SwordxStaff`). Xương, lưới, chuyển động gốc là
của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình.

## 1. Lời dặn của người dùng (2026-11-12)

- Concept: quái vật xương rồng **thân tròn, không mặt**. Đây là dạng 1; dạng 2 to hơn, chiến hơn chút, form người vẫn vậy.
- idle: giống họ nhưng sửa đi một chút.
- Đánh thường: nhảy tới đối thủ (rig làm bật nhún, **bay là code làm**) rồi há thật to mồm cắn.
- Chiêu mana: gồng rồi phóng dài các gai trên cơ thể, dài hẳn ra, đâm tứ tung (xem `skill_02` họ làm gai dài ra kiểu gì).
- Chiêu cuối: thu chân tay vào trong, nhảy lên nhẹ rồi phồng to cơ thể lên chút, gai dài ra nhọn hơn, xoay liên tục rồi tông thẳng
  vào đối thủ, tông xong bị bật ngược về chỗ cũ (rig làm phồng, nhảy lên, đáp đất; bay, đối thủ, bật ngược là code).
- Thêm `walk`. `appear` trồi từ đất lên.
- Sửa sau khi xem bản đầu (cùng ngày):
  - cắn: há to hơn, **lố một chút rồi đớp mạnh**;
  - chiêu mana: gồng = đứng bằng hai chân, **hai tay giơ lên trời rồi lập tức đưa vòng xuống dưới vào giữa** kiểu gồng cơ thể lên,
    gai dài ra hẳn (bản 2,6–3,4 lần "vẫn ít");
  - **tay bên phải (tay sau) thõng xuống, A pose**, không nhất thiết giơ lên như con gốc;
  - xem bản A pose (`L1_apose.png`): "cảm giác như có phần môi ở trên, **bỏ line vẽ môi đi**" → `L1_khong_moi.png` (lượt 1c): không
    nét môi, không dải môi, múi dọc chạy tiếp tới mép miệng. Part vành môi (`P_zuichun`) của mình vì thế chỉ có viền mực ở mép lỗ
    miệng, mép ngoài hoà vào thân (đúng như part của họ), và phải mang cả đoạn múi dọc nằm trong vùng nó phủ;
  - "trước khi làm cho tôi xem concept đã": chưa dựng tờ mảnh, rig khi concept A pose chưa được duyệt.

Màu, chi tiết, tên: người dùng chưa dặn. Bảng màu và chi tiết ở mục 3 là **đề xuất của Claude**, chờ duyệt concept.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3229/`: `info.json`, `att_goc.json`, `manh_anh.png`, `manh_dang_goc.png`, `parts/`, `khung/`)

41 xương, 27 slot (26 hình, slot `shadow` trống), 13 clip, atlas 656 × 208 (tỉ lệ 0,75). Con gốc nhìn sang phải: không lật.

Cây xương (tên gốc → vai trò):
- `bone` → `bone3` (hông: nhún, lắc cả con) → `bone4` (chậu) → hai chân IK: `bone5-6-7` (chân trước, bên trái người xem; IK `R1`
  trên bone5, 6 và `R2` trên bone7; mục tiêu `R2 > R1` là con của `bone`), `bone8-9-10` (chân sau; `L2 > L1`).
- `bone4` → `bone11` (đế quả cầu; con: hàm dưới `bone20`, gai dưới phải `bone21`) → `bone12` (quả cầu).
- `bone12` → hàm trên `bone19`; bốn gai thân `bone22–25`; ba xương hoa (mào) `bone29–31`;
  `rotate_02` → `bone13 > 14 > 15` (tay TRƯỚC) → ba gai nắm tay `bone26–28`;
  `rotate_01` → `bone16 > 17 > 18` (tay SAU) → ba gai nắm tay `bone32–34`.

Bảng mảnh theo thứ tự vẽ (sau → trước):

| # | hình | cỡ ảnh | là gì | bám xương |
|---|---|---|---|---|
| 1 | P_ci1 | 32×31 | gai thân mép trái (nấp sau thân) | bone23 |
| 2–3 | P_shouL1, L2 | 52×77, 52×67 | tay sau: khúc tay, nắm tay (nấp sau thân) | bone16–18 |
| 4–6 | P_shouL33, 32, 31 | ~30×30 | ba gai nắm tay sau | bone33, 32, 34 |
| 7 | P_ci11 | 28×26 | gai thân dưới phải | bone21 |
| 8 | P_ci4 | 29×29 | gai thân trên phải (sau thân) | bone25 |
| 9 | P_toufa | 122×63 | mào (của mình: vành hoa), lưới 12 đỉnh bám 4 xương | bone12, 29–31 |
| 10–11 | P_tuiL2, L1 | 50×44, 55×47 | chân sau: bàn chân, đùi (sau thân) | bone8–10, bone4 |
| 12 | P_shenti | 188×177 | quả cầu thân, 18 đỉnh | bone4 + bone12 |
| 13 | P_ci3 | 28×31 | gai thân trên (mặt trước) | bone24 |
| 14 | P_kouqiang | 149×138 | lòng miệng | bone11, 12, 19, 20 |
| 15 | P_xiaya | 125×62 | hàm răng dưới | bone20 |
| 16 | P_shangya | 141×71 | hàm răng trên | bone19 |
| 17 | P_zuichun | 149×138 | vành môi (mép ngoài không viền, hoà vào thân; viền mực ở mép lỗ) | bone11, 12, 19, 20 |
| 18 | P_ci12 | 30×31 | gai thân trên trái (mặt trước) | bone22 |
| 19–20 | P_tuiR2, R1 | 45×48, 59×57 | chân trước: bàn chân, đùi (trước thân) | bone5–7, bone4 |
| 21–23 | P_shouR1, R2, R3 | ~60×65 | tay trước: hai khúc, nắm tay | bone13–15 |
| 24–26 | P_shouR33, 32, 31 | ~28×32 | ba gai nắm tay trước | bone26–28 |

Cách họ làm (đọc khoá `keys.json`):
- **Miệng**: dáng gốc là há; ngậm = DỜI hàm trên `bone19` (−23,7; 3,65) và hàm dưới `bone20` (23,6; −4,27) lại gần nhau; vành
  môi và lòng miệng là lưới bám cả hai hàm nên co theo.
- **Gai dài ra** (`skill_02`): mỗi gai là một ô chữ nhật cứng trên xương riêng; khoá **tỉ lệ dọc xương** 1 → 1,7–2,7 trong 0,17 →
  0,5 s (bề ngang giữ 1), cùng lúc thân vươn, chân trước nhấc, tay vung. 0,5 s tắt hình mọi gai (gai "bắn đi"), 0,7 s bật lại ở
  tỉ lệ 0,2 rồi mọc về 1.
- idle 1,0 s: `bone3` nhún 18 đơn vị và lắc −9° ↔ 8°, hai tay và mào vẫy 2–4 khoá, miệng nhai một nhịp.
- `run_01`: cuộn tròn lăn. `hit_01` 0,5 s, `die_01` 1,0 s dùng lại nguyên.
- Lưới thân bám cả `bone4` (đáy) lẫn `bone12`: muốn quả cầu xoay / phồng mà không méo thì xoay từ `bone4`, không từ `bone11`.

## 3. Concept dạng 1 (đề xuất của Claude, chờ duyệt)

Gói: `ArtGen/Spine/gui_gpt/xuong_rong_1/luot_1_concept.txt` (sinh bằng `build_xuong_rong.py`; sơ đồ bố cục `xuong_rong.py bo_cuc`
→ `inbox/xuong_rong_1/mau/bo_cuc.png`). Ảnh: `inbox/xuong_rong_1/tai_ve/L1_concept.png` (lượt đầu, 81 giây).

Thiết kế: xương rồng thùng tròn lục lam `#569668`, múi dọc nét lục sẫm `#2F6248` có nốt gai kem; không mắt mũi, cái miệng cười
khổng lồ là cả mặt; nanh là gai kem `#EEE2BE` lởm chởm cài nhau; lòng miệng đỏ rượu `#682442` (ruột quả xương rồng); vành hoa
xương rồng hồng `#D6548A` bảy cánh nhọn trên đỉnh (thay mào); hai tay nắm tròn mỗi nắm ba gai; năm gai to trên thân; hai chân ngắn
ngón kem. Khác con gốc: màu thân, múi dọc thay mảng loang, hoa thay mào đỏ, lòng miệng đỏ rượu thay lục sẫm, gai kem vàng.

Tự soi lượt đầu: đạt các điểm kiểm (không mặt, thân cầu có múi và nốt gai, miệng bát nanh cài nhau, hoa bảy cánh, năm gai thân, ba
gai mỗi nắm tay, tô phẳng, nền trắng). Lệch nhỏ: gai ngả vàng hơn mã màu; vành môi có nét mực cả mép ngoài phía trên.

## 4. Clip (dựng ở tầng điều khiển của rig gốc: `xuong_rong_clip.py`)

Xem thử trên rig gốc (hình của họ, nội bộ): `<SXS>/scan/monster_3229/lam_clip/xem/xem.html` (`xuong_rong_clip.py gif`).

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| xr_idle | 2,4 s lặp | hai vòng nhún của idle_01 chậm lại (1,2 s/vòng); vòng hai nghiến răng "tách tách" và xù gai ở 1,92 s | |
| xr_attack | 1,4 s | nhún 0,28; bật 0,36; đang bay ngửa người há LỐ (quả cầu phồng 1,28, giãn dọc 1,4, vọt quá) tới 0,50, giữ rung, hít thêm một nấc; đớp trong MỘT khung 0,633 → 0,667 (chúi 26°, bẹp dọc 0,78, gai xù); ngoạm lắc tới 0,87; bật về 1,13; đáp | trung 0,667 |
| xr_cast | 1,9 s | hai tay giơ lên trời 0,22 (thân vươn), giữ 0,30; quật vòng ra ngoài – xuống – chụm vào giữa 0,44 (gồng: thụp, nghiến răng, rung; tay sau vẽ ra TRƯỚC thân); bung 0,50: gai thân dài 4,6–5,6 lần, gai nắm tay 1,9 lần, thụt ra thụt vào lệch pha tới 1,30; rút, tay buông | phun 0,50; het_phun 1,30 |
| xr_hit, xr_die | 0,5 s; 1,0 s | hit_01, die_01 của họ + A pose | |
| xr_skill | 2,06 s | (bản 2026-11-12 chiều, mục 5d) thu chân tay 0,30; nhún 0,42; NHẢY LÊN KHÔNG, tới đỉnh 0,66 (cao 150) phồng 1,24 lần + gai dài 2,5 lần; lơ lửng XOAY RẤT NHANH TẠI CHỖ 1,25 s (tăng tốc 0,3 s đầu, tới 1800°/s) | phong 0,60; bat 1,91 |
| xr_skill_land | 1,5 s | đang lao xoay đều; chạm 0,14; ghì tới 0,30; bật về theo vòng cung, xoay ngược chậm dần; về chỗ 0,72: bẹp, xẹp, gai rút, chân tay bung | tong 0; cham_dat 0,14; dap 0,72 |
| xr_appear | 2,2 s | trồi từ đất: vành hoa nhú lên, ngó nghiêng; thụt lấy đà; vọt lên 0,90; chạm đất 1,22; rũ đất; gầm | nut_dat 0; troi 0,90; cham_dat 1,22 |
| xr_walk | 0,8 s lặp | lạch bạch tại chỗ: hai chân bước so le, thân lắc và nhún, tay vung ngược nhau, miệng nhóp nhép | |

- Chiêu cuối đi hai clip như Tí Tách (`skill` + `skill_land`, cung bay do `AolaSticker.Jump` tính; mốc `L_CHAM`, `L_GHI`, `L_VE`
  khớp `JumpStay` 0,16 s và `JumpBack` 0,42 s). `Jump` hiện bay theo parabol rơi từ trên xuống: muốn "tông thẳng" phải thêm tuỳ chọn
  cung dẹt ở code game (chưa làm).
- Đòn thường: cung bay đặt lên xương `move` ở rig của mình (`attack_bay`: tới trước 150, đỉnh cao 62 đơn vị con gốc; đỉnh dời =
  lúc cắn) để `AolaSticker.Lunge` kéo tới đối thủ. Appear: `appear_bay` (dời dọc), cần mặt nạ cắt ở mặt đất + ụ đất ở rig mình.
- Lúc cuộn tròn: khúc tay, nắm tay, chân ẩn hẳn; sáu gai nắm tay ở lại mép quả cầu thành gai thân (quả cầu xoay có 11 gai).
- **A pose**: `A_POSE` trong `xuong_rong_clip.py` cộng −36° vào `bone16`, −58° vào `bone17` cho mọi dáng lấy từ clip của họ (khúc
  trên −25°, khúc dưới −63° so với phương ngang, đối xứng tay trước). Dáng vẽ concept và nướng khung part = clip `xr_dang`
  (`<SXS>/scan/monster_3229/att_dang.json`), không còn là `att_goc.json`.
- Lúc gồng, tay sau phải vẽ TRƯỚC thân: clip ghi `draworder` (mo_xe.html đã đọc được); `.atomik` chưa đổi được thứ tự vẽ theo clip
  nên rig của mình phải có bản sao tay sau ở lớp trước, bật tắt theo trường `o` của mẫu.
- Gai kéo dài 5 lần bằng tỉ lệ thì ảnh gai bị kéo nhoè, viền dày lệch: rig của mình nên có một ảnh "gai dài" riêng để đổi hình.
- Há to hơn dáng gốc quá ~0,55 lần quãng ngậm thì vành môi thò khỏi quả cầu: há "thật to" làm bằng phồng cả quả cầu 1,17 lần +
  giãn dọc + ngửa 15°.

## 5. Mảnh và rig (2026-11-12, sau khi người dùng duyệt `L1_khong_moi.png` → `tai_ve/L1_duyet.png`: "ok ổn, bắt đầu làm")

Trình tự: `xuong_rong.py nhom_part` → `build_xuong_rong.py` (ba file `luot_2_manh_A/B/C.txt`) → `gen.py` từng tờ → `xuong_rong.py
cat_part A B C` → `xuong_rong.py moi` → `xuong_rong_clip.py mau` (qua `khoa.py chrome`) → `xuong_rong_rig.py` (qua `khoa.py nang`)
→ `chay.py sheet inbox/xuong_rong_1/rig xuong_rong_1 ...` (runtime Spine thật) → `mo_xe/thu_xem.py <rig/xem.html>`.

- **Ba tờ mảnh** (lượt đầu đều dùng được, IoU 0,90–0,99): A (× 2,8) thân, vành môi, lòng miệng; B (× 4) hai hàm nanh, vành hoa, chín
  khúc tay chân; C (× 6) mười một gai, gai vừa, gai dài, ụ đất. Màu đo trung vị trên concept đã duyệt (`PAL`).
- **Hình bóng của mình** thay hình bóng con gốc ở hai loại part: GAI (nón mập mũi nhọn dọc trục xương gai, `non_gai`; gai của họ tù)
  và VÀNH HOA (bảy cánh xoè quạt dọc cung đáy mào, `canh_hoa`). Gai là ô cứng một xương nên hình bóng tự do; hoa dùng lưới riêng,
  mỗi đỉnh biến dạng như điểm tương ứng trên lưới mào của họ (`gan_rieng` + `gan_goc`). Các part khác lắp nguyên lưới của họ.
- **Vì sao concept đầu có "nét môi"**: `lo_mieng` cũ tìm lỗ miệng bằng phép đóng hình thái bán kính nhỏ hơn lỗ, nên bắt nhầm cái
  khấc ở mép trên vành môi và kẻ viền ở MÉP NGOÀI vành; GPT vẽ theo. Nay tìm lỗ = vùng trống kín không thông ra mép khung.
- **Vành môi không thấy môi** (`xuong_rong.py moi` → `manh/part_moi/`): da vành môi = da thân nướng vào khung vành môi qua lưới hai
  part ở dáng gốc (múi dọc chạy liền qua mép vành), chỉ giữ của Codex nét mực mép lỗ miệng; mép ngoài mờ 5 px; vành dừng cách mép
  thân 9 px (mang theo bản sao viền thân thì lúc há hiện hai đường viền); lòng miệng gọt mép vào 12 px (không thì màu đỏ rượu lộ
  qua dải mép mờ của vành thành vệt trên thân).
- **Gai phóng dài = đổi hình**: mỗi slot gai có thêm hai hình `gai_vua`, `gai_dai` (một ảnh chung, ô chữ nhật trùng trục, gốc, bề
  dài, bề ngang với gai ngắn); chọn theo tỉ lệ dài/ngang của xương gai: dưới 1,45 gai ngắn, dưới 2,8 gai vừa, trên nữa gai dài.
- **Tay sau ra trước thân lúc gồng**: năm slot `truoc_<tên>` (bản sao, ẩn sẵn) bật theo trường `o` của mẫu.
- **Appear**: mặt nạ cắt bám xương `mat_dat` nằm sâu 3000 đơn vị (không cắt gì); chỉ clip appear kéo lên đúng mặt đất, con đứng
  hẳn thì hạ xuống lại (để luôn ở mặt đất thì gai dài, quả cầu xoay bị xén). Ụ đất thấp dẹt (235 × ~47) vẽ trước cùng; vành hoa nhú
  150 đơn vị mới lộ trên ụ. Khung đầu ẩn mọi slot.
- **Há quá dáng gốc**: hai dải răng là mảnh cứng bám hàm, vành môi bám cả bốn xương nên đi ít hơn: há quá ~0,2 quãng ngậm là dải kem
  thò ra ngoài vành. Cú cắn "lố" vì thế làm bằng phồng 1,25 + giãn dọc 1,44 + ngửa 22°, hàm chỉ dời thêm 0,12–0,2.
- Quả cầu xoay nhiều vòng: góc lấy mẫu `unwrap`, chuẩn theo đầu clip (`skill`) hoặc khung cuối (clip hết ở dáng nghỉ) để không có
  bước nhảy 360° giữa hai khoá. `skill` không hoà về idle (hết clip còn đang xoay); năm clip hết ở dáng nghỉ hoà 0,2 s cuối.

Kết quả `inbox/xuong_rong_1/rig/`: 44 xương, 33 slot, 60 hình, 530 đỉnh, 9 clip (appear, idle, walk, attack, cast, skill,
skill_land, hit, die), atlas 1136 × 1280, `.atomik` 268 KB; nạp lại `.atomik` lệch bộ vẽ ≤ 0,17 px; idle khép vòng 0,64 px; trang
`xem.html` chạy (thu_xem: đủ 9 nút clip, không lỗi JS). Đã soi bằng runtime Spine thật: idle cận miệng, attack 0,50–0,67 s, cast, skill,
skill_land, appear, walk, hit, die (`rig/that/*.jpg`). Còn thấy: đùi chân trước lúc co lên trong cú cắn có một vệt gạch ở nếp gấp
lưới (nhỏ, 0,3 s).

## 5b. Dạng 2 (2026-11-12: người dùng xem rig dạng 1 "ok ổn rồi, dạng 2 đâu")

Lời dặn ban đầu: "dạng 2 sẽ to hơn chiến hơn chút nhưng form người vẫn vậy". Làm trên CÙNG rig, cùng khung part, cùng clip (biến môi
trường `XR_DANG=2`: `xuong_rong.py` đổi thư mục sang `inbox/xuong_rong_2`, `xuong_rong_rig.py` áp `TI_LE`):
- tỉ lệ dáng gốc (dọc xương, ngang): năm gai thân 1,45 × 1,15; hai nắm tay 1,18 (gai nắm tay thêm 1,22 × 1,08); ba xương hoa 1,28.
  To hơn cả con là việc của `size` trong `heroes.json`.
- sơ đồ bố cục cho concept = hình dạng 1 đã duyệt dựng trên rig với tỉ lệ dạng 2 (`xuong_rong_rig.py bo_cuc`, `XR_MANH` trỏ mảnh
  dạng 1) → `inbox/xuong_rong_2/mau/bo_cuc.png`; gói `gui_gpt/xuong_rong_2/luot_1_concept.txt` (`build_xuong_rong.py build_dang2`).
- đề xuất của Claude (chờ duyệt): da lục sẫm `#2F8A56`, múi `#123F28`; nốt gai thành gai nhỏ nhọn; gai lớn dài, mũi đỏ sẫm
  `#A8234A`; nanh to, dài, lởm chởm, có nanh như ngà; lòng miệng `#701238`; bảy cánh hoa dài nhọn như lưỡi dao, hồng đỏ `#D42A6B`;
  nắm tay to như chùy gai; vẫn không mặt, không môi.
- concept lượt đầu: `inbox/xuong_rong_2/tai_ve/L1_concept.png` (130 giây), tự soi đạt: cùng dáng và chỗ đặt, đủ 5 + 3 + 3 gai.
- người dùng xem: "**bỏ màu hồng ở gai dạng 2 đi**" → lượt 1b `L1_gai_kem.png`: gai lớn kem trơn một màu từ gốc tới mũi, mọi thứ
  khác giữ nguyên (đề xuất mũi gai đỏ sẫm `#A8234A` bỏ hẳn; đã sửa cả prompt lượt 1).
- người dùng "duyệt" → `inbox/xuong_rong_2/tai_ve/L1_duyet.png`.

**Mảnh và rig dạng 2** (`XR_DANG=2 xuong_rong.py nhom_part` → `build_xuong_rong_2.py` → gen → `XR_DANG=2 xuong_rong.py cat_part A B C`
→ `XR_DANG=2 xuong_rong.py moi` → `XR_DANG=2 xuong_rong_rig.py`):
- ba tờ: A thân (gai nhỏ nhọn trên múi), vành môi, lòng miệng; B hai dải nanh + vành hoa; C chín khúc tay chân lục sẫm. Gai lớn,
  gai vừa, gai dài, ụ đất DÙNG LẠI của dạng 1 (kem trơn như nhau; dài hơn là do tỉ lệ xương): `tim_part` tìm ở dạng 2 trước, thiếu
  thì lấy dạng 1.
- **ô nới khung** (`DEM_K`): nanh dạng 2 dài hơn hình bóng răng của họ → ô răng nới 56 px quanh khung ảnh vùng, nền hướng dẫn là
  chính dải răng dạng 1, Codex kéo dài nanh vào khoảng trắng; rig gắn cả ô thành một ô chữ nhật cứng bám xương hàm (`gan_cung`).
  Vành hoa cũng nới 52 px: bản đầu không nới thì hai cánh ngoài chạm mép khung bị cắt cụt thành cạnh thẳng, lòi ra như mảnh
  hồng dẹt lúc hoa lắc → gen lại tờ B (`N_B_2.png`).
- hoa dạng 2 lắc 55 % biên độ của họ (`nhe_hoa`): cánh dài + xương hoa × 1,28 mà lắc đủ biên độ thì cánh bị ép mảnh như kim.
- kết quả `inbox/xuong_rong_2/rig/`: 44 xương, 33 slot, 9 clip, `.atomik` 261 KB; đã soi runtime Spine thật idle (cận), attack, cast,
  skill, appear.

**Tiến hóa** (`xuong_rong_rig.py tien_hoa`, theo `quai/tienhoa.py`): chạy `xuong_rong_rig.py` (dạng 1) khi đã có mảnh dạng 2 thì rig
dạng 1 gộp bản nhẹ của dạng 2 (ảnh 0,6 lần, xương `n_*` dưới `evo`, co 0,876 = tỉ lệ chiều cao hai dạng) + clip `evolve` 2,8 s: dạng
1 giơ hai tay lên trời gồng, rung; tan 1,05 → 1,35 (sự kiện `doi_dang`); dạng 2 hiện lớn dần, há miệng gầm xù gai (đoạn gầm của
appear), hoà về đúng khung 0 idle dạng 2 (lệch 0,00 px). Rig dạng 1 thành 88 xương, 66 slot, 10 clip, `.atomik` 372 KB.

## 5c. Vào game (2026-11-12; người dùng: thay hình suất ải 1 đảo Mộc, tên Claude tự đặt, thêm cung bay thẳng)

- **Suất**: id giữ `tien_la` (ải 1 đảo Mộc). **Chỉ 2 dạng** (người dùng: "con này 2 dạng thôi"), **cỡ 0,8 / 0,96** (người dùng: "scale
  tướng này trong game còn 0.8"; dạng 2 giữ tỉ lệ to hơn dạng 1 như cũ). `tien_la_1` ← `xuong_rong_1.atomik` (có `evolve`),
  `tien_la_2` ← `xuong_rong_2.atomik`; chân dung `rig/chan_dung.png`. Chép tay vào `Assets/03 Art/Heroes/Resources/tien_la_<k>/`,
  ghi sổ `quai/da_nhan.json`. Thư mục `tien_la_3` đã xoá qua Unity; golden `roster.json` tính lại (`n` 2, `idx` 0,0,1,1,1).
- **Tên (Claude đặt, người dùng có thể đổi)**: tướng **Cầu Gai**, danh hiệu "Xương rồng tròn háu đớp", dòng "Dòng Cầu Gai"; dạng
  **Cầu Gai Nhí**, **Cầu Gai**; thẻ `tien_la_skill` **Gồng Gai**, `tien_la_ult` **Lăn Gai**, `tien_la_pas` **Mọng Nước** (chỉ đổi
  tên; số, hiệu ứng, biểu tượng giữ).
- **Chiều cao game** đo trên thân (`BO_CAO`: bỏ vành hoa, gai) → hai dạng cùng `game.height` 254,7; dạng 2 to hơn thật nhờ `size`,
  và dạng 2 trong rig gộp tiến hóa không phải co (tiB = 1,000).
- **Tông thẳng**: clip `skill_land` có sự kiện `tong` → `AolaSticker.Rams`; `Jump` bay gần ngang, nhanh dần (nhấc 0,1 chiều cao);
  `StageView.Place` đặt chỗ đáp ngang thân đối thủ, 86 % quãng. Tướng nhảy đè cũ (Tí Tách) không đổi.

## 5d. Chiêu cuối bản 2, rung màn, chiêu gai (2026-11-12 chiều)

Người dùng: "chiêu cuối impact hơi nhẹ, kịch bản là nhảy lên không trung, xoay rất nhanh tại chỗ 1-1.5 giây rồi lao vào đối thủ sau đó
như kiểu bị bật theo hướng vòng cung trở lại, shake cam, thêm shake cam vào chiêu cuối của tất cả các tướng"; "chiêu đợi gpt xong thì
gen ảnh".

- **Clip** (`xuong_rong_clip.py`): `S_THU 0,30; S_NHUN 0,42; S_DINH 0,66; S_XOAY 1,25; S_CAO 150; W_MAX −1800°/s`; con ở trên không
  suốt lúc xoay, `skill_land` hạ về mặt đất đúng lúc chạm (`L_CHAM 0,14`), bật về xoay ngược ≥ 620° dừng ở bội 360.
- **Code game**: `AolaSticker.Jump` nhánh bật về của tướng `Rams` vồng cao `0,85 × chiều cao` (tướng nhảy đè cũ 0,4; bản 1,05 bay
  khuất sau bảng máu đối thủ). `StageView.Impact`: **mọi chiêu cuối** rung màn ít nhất `UltShake = 0,62` và khựng `UltStop = 0,06`
  kể cả rig không khai `impactClips`. Rig Cầu Gai khai thêm `IMPACT_K` (dạng 1 skill: khựng 0,17, rung 0,92, đẩy 0,14; dạng 2: 0,20,
  1,0, 0,16 + chớp kem).
- **Chiêu mana "Gồng Gai" = mã `n_gai`** (`Assets/01 Script/Game/Battle/HatMoc.cs`, đi chung đường bộ Thủy: `PlayNuoc`, `WThemes
  ["tien_la"]`, `StageView.MocFx`): lúc gồng dăm gai hút vào thân; khung nhả (rig tự làm gai thân dài 4,6 lần) dăm gai văng quanh
  thân; 4 cụm gai trồi từ đất chạy tới chân đối thủ (cụm sau to hơn), tới nơi một cụm lớn bật lên sau lưng nó + 5 gai dài đâm chéo
  (ba cái cao ở sau lưng, hai cái thấp hai bên phía trước, không che mặt), chớp toé, dăm gai, bụi; gai đứng 0,5 s rồi rút.
  Chiêu cuối: `n_gai_va` phát đúng khung chạm (gai gãy văng, cụm gai dưới chân).
- **Ảnh hạt**: `ArtGen/Spine/gai.py` → `Assets/03 Art/Fx/Hat/hat_thorn_<i>`, `hat_tuft_<i>`, `hat_shard_<i>` (+ bản đặc `…s_<i>`);
  quy ước đặt hình: chiếm tối đa 92 % khung, đáy ở 96 % khung (game cắm đáy xuống đất). Ảnh GPT: gói `gui_gpt/hat_gai/luot_1_hat.txt`
  (`build_hat.py hat_gai`, bước G01 gai, G02 cụm gai, G03 dăm gai) → `gen.py … --steps G01,G02,G03` → `build_hat.py --nhap hat_gai`
  → `gai.py` (tự lấy ảnh GPT trong `hat_gpt/` thay hình thuật toán) → hai menu gán ảnh hạt. Lượt đầu `inbox/hat_gai/tai_ve/G01–G03.png` (171 giây, cả ba dùng
  được ngay) đã nhập và đã chạy lại tour trong trận.
- **Lỗi đã gặp**: gai kem nhạt (244, 230, 188) nhân với ảnh xám vân chì ra xám be, viền mực 5 px: lẫn hẳn vào nền cát → kem vàng ấm
  (255, 238, 164) + viền `GaiInk` 9 px. Cụm gai đầu hàng mọc ngay trong thân con ra chiêu (con to, hai bên đứng gần) → hàng bắt đầu
  từ 36 % quãng. Hai cụm trước chân đối thủ rộng 0,52 chiều cao che mặt nó → 0,4, đứng lệch ±0,52.
- **Unity** (MCP cổng 8080): biên dịch không lỗi; "Nhập dữ liệu"; "Gắn dạng .atomik vào prefab tướng"; hai menu gán ảnh hạt (158
  ảnh); test EditMode 102 / 103 (cái trượt là `PrefabOnlyTests.MaRuntime_KhongSinhDoVat` ở `UI/Kit/NumberTicker.cs`, `UiMotion.cs`:
  có sẵn); tour "PokiClash/Thử/Đảo Mộc: Cầu Gai ra trận ở 2 dạng" (`Temp/PokiShots/cau_gai_combat`) và "…hạt gai Cầu Gai, chiêu
  mana và chiêu cuối từng dạng" (`Temp/PokiShots/thuy_fx`): chiêu cuối đúng kịch bản mới ở cả hai dạng, rung màn có.
- **CÒN THIẾU**: VFX đất văng lúc trồi, lá / chớp lúc tiến hóa; chưa thử trên Android; vệt gạch nhỏ ở đùi chân trước lúc cắn.

## 6. Việc tiếp

1. Người dùng xem trong game (tour ở mục 5d), chốt chiêu cuối bản 2 và chiêu gai.
2. VFX đất văng lúc trồi (`appear`), hiệu ứng lúc tiến hóa.
3. Thử trên Android.
