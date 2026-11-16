# Tinh linh đuôi máy cưa (`cua_xich`): tướng 4 đảo Kim

Bắt đầu 2026-11-16 (máy ổ C). Con gốc của rig: `monster_3374` (sinh vật nhỏ đầu tròn quay phải dưới mũ trùm sẫm, một mắt hổ phách, sừng nhọn
trái trên, ba tinh thể tím sau đầu, thân tròn nhỏ, chân que, đuôi mang tấm vỏ + đĩa bánh răng răng tinh thể; game tham khảo, kho
`D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `skill_03_1`). Xương, lưới, chuyển động gốc là của nhà phát hành game
đó (như aola): dùng nội bộ, không đăng công khai. Hình là của mình. Suất 4 đảo Kim = ải 15 ("Tháp Canh Thép", `IslandGen.cs` Plan Kim), id game
hiện là **`phi_thuong`**. Mã làm việc `cua_xich`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-16)

- "làm dạng 4 đảo kim" (= tướng thứ 4); "concept **tinh linh đuôi máy cưa**".
- appear: "làm nó **kéo 1 dây trên người để khởi động máy cưa ở đuôi**".
- idle / walk: "làm **giống họ, sửa đi chút cho khác**".
- Đánh thường: "**lao vào húc** đối thủ".
- Chiêu mana: "dùng **đuôi cưa quật** đối thủ".
- Chiêu cuối: "**kéo thêm dây kéo nhiều lần** nữa, **cưa quay nhanh hơn và to ra chút**, có hiệu ứng thêm vào kiểu **hút khí xung quanh**,...
  sau đó dùng đuôi **cưa liên tục** đối thủ (kiểu đối thủ bị attack liên tục), có hiệu ứng **tia lửa bắn ra**".
- die: "làm giống họ".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3374/`: `info.json`, `att_goc.json`, `att_idle0.json`, `khung/`, `mo/`, `parts/`; script `cua_xich.py`
mo / nhom / part_goc)

29 xương, 23 slot (20 hình bật ở idle 0), 15 clip, 3 418 khoá. Ràng buộc: **IK hai chân** (`bone22` → xương `bone3`/`bone4` chân GẦN, `bone23` →
`bone5`/`bone6` chân XA, bend 1), **3 transform** (`bone21` → xương `bone21` theo `bone22`, `erduo` → tai phải `bone11`, `yanjing` → mắt
`bone13`; đều mix nhỏ, kéo nhẹ theo chân trụ). Con nhìn sang PHẢI. Không path, không physics, không đổi thứ tự vẽ trong clip.

Cây xương chính: `root` → `bone` → `bone2` (TÂM THÂN, idle nhún / xoay) → `bone19` (THÂN; lưới thân) → `bone7` (ĐẦU; lưới mặt, mũ, tinh thể,
tai đều bám bone7 0,6–0,96) → `bone8` (sừng trái), `bone9` (tai phải), `bone10` (tinh thể), `bone11` (MẮT con ngươi), `bone20`, `bone21`;
`bone19` → `bone12..14` (TAY TRÁI 3 đốt), `bone15..17` (TAY PHẢI 3 đốt), `bone18` (ĐUÔI gốc) → `bone26` (đuôi khúc 2) → `bone25` (TÂM ĐĨA CƯA:
quay đĩa). Chân gần: `bone2` → `bone3` → `bone4` (+ `run` mang đùi gân); chân xa: `bone2` → `bone5` → `bone6`. `bone24` (đích IK, con của
`bone`) nhiều clip dời nó làm cú lao.

| thứ tự vẽ | slot | ảnh vùng (px) | là gì | xương |
|---|---|---|---|---|
| 1 | `weiba_04` | 80×98 | tấm lưng vỏ cưa (sẫm, sau) | bone26 |
| 2 | `weiba_03` | 45×54 | gốc đuôi (sẫm) | bone18 0,81 + bone26 0,19 |
| 3 | `juzi_04` | 111×110 | ĐĨA CƯA: đĩa sẫm 8 răng tinh thể | bone25 |
| 4 | `juzi_03` | 69×78 | cung mờ (vệt quay của đĩa) | bone26 |
| 5 | `weiba_02` | 28×30 | mẩu nối nhỏ | bone26 |
| 6 | `weiba_01` | 83×95 | VỎ CƯA trước (tấm thuôn có trục vòng vàng) | bone26 |
| 7 | `youxiaotui2` | 50×66 | cẳng chân XA | bone6 |
| 8 | `youdatui2` | 47×47 | đùi XA | bone5 |
| 9 | `shenti` | 118×114 | THÂN tròn xám nhạt | bone19 |
| 10 | `youshou` | 43×59 | tay PHẢI (găng sẫm) | bone15/16/17 |
| 11 | `zuoshou` | 49×50 | tay TRÁI (găng sẫm, giữa bụng) | bone12/13/14 |
| 12 | `zuoxiaotui2` | 46×68 | cẳng chân GẦN | bone4 |
| 13 | `zuodatui2` | 59×59 | đùi GẦN: vòm gân (hình phụ `youdatui` ở skill_03, tắt ở run) | run |
| 14 | `zuodatui3` | | bản sao đùi gần (bật ở run, transform, transmit) | run |
| 15 | `youerduo` | 68×106 | gai sẫm sau đầu bên phải | bone9 / bone7 |
| 16 | `to_01` | 173×173 | MẶT: cầu xám nhạt + ba sọc sẫm | bone7 0,96 |
| 17 | `yanjing_01` | 59×65 | lòng MẮT vàng nhạt | bone7 0,94 |
| 18 | `yanjing_02` | 39×52 | tròng cam (hình phụ `yanjing_03` = mắt nhắm: hit, stun, die, floating) | bone11 |
| 19 | `to_02` | 173×158 | MŨ TRÙM sẫm (mép trước cắt nửa trên con mắt) | bone7 0,96 |
| 20 | `tofa` | 164×200 | BA TINH THỂ sau đầu + một tinh thể hồng nhỏ | bone10 0,51 + bone7 0,45 |
| 21 | `zuoerduo` | 101×100 | SỪNG trái trên (sẫm, lót tím) | bone7 0,63 + bone8 0,31 |
| 22 | `jingkuai` | 61×99 | mảnh tinh thể (chỉ bật 0,467–0,5 s ở skill_01) | bone25 |

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho (dự kiến) |
|---|---|---|---|
| `idle_01` | 7,00 | nhún, nghiêng đầu, đuôi đung đưa | **idle** (sửa chút) |
| `run_01` | 0,53 | chạy nảy | **walk** |
| `skill_01` | 1,27 | lấy đà, BẬT lao chúi đầu tới (0,42–0,7), về | **attack** (lao húc) |
| `skill_02` | 1,33 | rướn, chúi tới, đuôi quét xuống trước | nguồn dáng |
| `skill_03_1` | 0,73 | quay người, ĐUÔI quét NGANG tới trước (0,08–0,49) | **cast** (quật đuôi) / chiêu cuối |
| `skill_03_2` | 0,73 | ĐUÔI vung qua đầu, bổ xuống trước | **cast** / chiêu cuối (nhát cưa) |
| `skill_03_3` | 0,73 | ĐUÔI quét xuống dưới trước mặt | chiêu cuối (nhát cưa) |
| `die_01` | 1,00 | lảo đảo, ngã nghiêng, mắt nhắm (đĩa quay chậm dần 360°) | **die** |
| `hit_01`, `hit_02`, `bolck_01`, `stun_01`, `floating_01`, `transform_01`, `transmit_01` | | | **hit** = hit_01 |

Đĩa cưa (`bone25`, chỉ số 27) họ đã cho quay sẵn: idle −2 520° / 7 s (1 vòng / giây, đều), run và skill_01 một vòng mỗi clip, skill_02
tăng tốc tới −719°, **skill_03_1/2/3 quay ~−5 825° trong 0,7 s** (~22 vòng / giây, gần như bật ngay ở 0,033 s), hit quay ngược −210° rồi về,
die quay chậm dần 360°. Mẫu khung 30 / giây: `sample_goc.json` (13 clip); khoá: `keys.json` (9 clip).

## 3. Concept lượt 1 (Claude đề xuất ba hướng, chờ người dùng chọn)

Gói `gui_gpt/cua_xich_1/` (`cua_xich_da.py ca_con`, `concept`). Ảnh mẫu 1 = hình cả con gốc `mau/goc_ca_con.png` (khung 0 idle; khung bao từng
part trong `.json`, ghi vào prompt); ảnh 2 = chiến binh sắt (nét, cách tô thép), ảnh 3 = tinh linh tinh thể sắt (mặt kim loại). Mọi hướng giữ
dáng, chỗ, cỡ từng mảnh, con mắt duy nhất bị mép mũ cắt nửa trên, không miệng; đĩa → **lưỡi cưa tròn** 14 răng móc cùng chiều; ba sọc mặt →
khe thông gió; **thêm một mảnh: tay cầm dây giật chữ T** ở bụng ngay dưới tay trái, dây ngắn chui vào lỗ ở bụng (appear kéo dây này).
- `tai_ve/L1_A.png` **cam máy công cụ**: mũ trùm đổi dáng thành mũ bảo hộ cam có vành cứng che nửa trên mắt; sừng trái → ống xả đen ngắn; ba
  tinh thể + gai → bốn vây thép hình răng cưa móc ngược; vỏ cưa cam.
- `tai_ve/L1_B.png` **vạch cảnh báo vàng đen**: mũ lam thép mép trên thành hàng 5 răng cưa; sừng → lưỡi thép cong; ba tinh thể → ống xả đen;
  vỏ cưa vàng ba vạch đen; tròng đỏ cam.
- `tai_ve/L1_C.png` **thép súng + đồng đỏ**: mũ kiểu mặt nạ hàn (mép trước thẳng ngang, một đai đồng); sừng → vây đồng ngắn; ba tinh thể →
  tinh thể hổ phách hình tia lửa gãy khúc; vỏ cưa đồng.

Kết quả (Codex, lượt đầu cả ba): độ khớp hình bóng với con gốc A 0,862 / B 0,858 / C 0,879 (`mau/_so_goc.png`); mắt, thân, chân, đuôi
đúng chỗ, chân dính thân, một mắt bị mép mũ cắt nửa trên. Cả ba bản vẽ dây giật nối từ tay cầm sang TAY PHẢI thay vì chui vào bụng
(`mau/_can_bung.png`): sửa ở bước mảnh (vẽ riêng tay cầm + dây). Trang xem: `inbox/cua_xich_xem_concept.html`.

Người dùng (lượt 1 → lượt 2): "làm nó mang tính **sinh vật hoang dã** hơn, có **quặng sắt trên đầu**, **đuôi cưa cũng nên làm giống con gốc**".
Bỏ cả ba hướng máy móc.

## 3b. Concept lượt 2 (`cua_xich_da.py concept2`, gói `gui_gpt/cua_xich_1/luot_2_concept_<D|E|F>.txt`)

Chung: không mũ, ống, khe, bu lông; mũ trùm thành mai / bờm tự nhiên; ba tinh thể + gai sau → quặng sắt; găng tay → chân thú ba vuốt; mắt
đồng tử dọc; ba sọc mặt giữ như vằn thú; ĐUÔI giữ đúng dáng con gốc (tấm vỏ thuôn có trục + vòng mảnh, đĩa 8 răng vuông), chỉ đổi màu; dây
giật ngắn từ lỗ giữa bụng tới vòng cầm dưới tay trái, không chạm tay phải.
- `L1_D.png` mai đá sẫm mép vảy, sừng cong lót gỉ cam, quặng thành CỘT lục giác đầu gỉ cam (nhìn như tinh thể cột hơn là cục quặng); lỗ dây
  nằm sát cằm, đọc như cái miệng ngậm dây. Khớp 0,934.
- `L1_E.png` mai nâu gỉ (dáng gần y mũ gốc), sừng màu cát, quặng hematit bong bóng (nhìn như khói đen / chùm nho); không thấy dây. Khớp 0,958.
- `L1_F.png` BỜM LÔNG xù than chì phủ đúng vùng mũ, mép trước cắt nửa trên mắt; sừng ngà; quặng thành cục thô gỉ đỏ mặt xám sắt (đọc ra quặng);
  vòng cầm dưới chân trái, dây chui vào lỗ ở bụng đúng lời dặn. Khớp 0,940. **Claude đề xuất F.**
Tờ so: `mau/_so_gocDEF.png`, cận bụng `mau/_can_bung_DEF.png`.

Người dùng chọn **D**: "làm D nhưng bạn **sửa lại đầu / mặt đi chút cho đỡ giống con gốc**".

## 3c. Lượt 3: sửa đầu / mặt bản D (`cua_xich_da.py sua_dau`, gói `luot_3_dau_<D1|D2|D3>.txt`)

KEEP / CHANGE trên `L1_D.png` (ảnh 1), ảnh 2 = con gốc chỉ để biết phải đi xa khỏi nó. Giữ nguyên đuôi, thân, chân, chân thú, vòng dây, ba
cột quặng + cục quặng nhỏ, con mắt, màu, nét. Ba kiểu để chọn; mọi kiểu dời lỗ dây xuống thấp giữa hai chân (bản D lỗ sát cằm như miệng):
- `L1_D1.png` đổi mai + sừng: mai thành ba đốt giáp kiểu tê tê, đốt trước là gờ mày dày; bỏ mũi nhọn chạy xuống má phải; sừng ngắn dày quặp
  về trước như móc; vằn mặt thành hai vạch gỉ cam chéo.
- `L1_D2.png` đổi mặt: mõm ngắn tròn dưới phải mắt (chấm mũi, miệng ngậm, một nanh trắng), gờ mày có khấc nhíu; mũi nhọn mai dừng trên mõm;
  vằn gỉ cam.
- `L1_D3.png` cả hai.

Ghi chú cho bước rig: lưỡi cưa nằm trên xương riêng `bone25` (quay được, phóng to được cho chiêu cuối); tay cầm dây giật là mảnh thêm (ô cứng
bám thân theo trọng số da), dây là dải lưới co giãn từ lỗ ở bụng tới tay cầm; tay trái (`bone12..14`) phải nắm tay cầm khi kéo (skill mục 26).

Kết quả lượt 3 (2026-11-16): mỗi kiểu có hai bản (một phiên khác gen `L1_D1/D2/D3.png` lúc 11:42–11:46, phiên này gen `_2` lúc 11:47–11:51).
Khớp hình bóng với D 0,94–0,975, với con gốc 0,89–0,90 (D là 0,917). Cả sáu bản đã dời lỗ dây xuống thấp giữa hai chân, đuôi, thân, chân giữ
nguyên. Tờ so: `mau/_so_D123.png`, cận đầu: `mau/_can_dau_D123.png`.
- `L1_D3.png` **Claude đề xuất**: mai ba đốt, sừng móc, mõm ngắn có nanh, gờ mày khấc nhíu rõ nhất; vằn gỉ thành hai ô vuông (chưa xéo).
- `L1_D3_2.png` mai bốn đốt tròn như mũ len, còn sót hai vạch xám của vằn cũ.
- `L1_D2_2.png` giữ mai D, mõm dài kiểu thằn lằn, gờ mày khấc, vằn xéo đúng. `L1_D2.png` mõm tròn nhưng miệng cong như cười, mai thêm dải
  sẫm (gần như bóng).
- `L1_D1.png`, `L1_D1_2.png` không mõm, má tròn, hiền hơn; `_2` còn vệt mờ mai cũ trên đỉnh đầu.
Ghi chú rig: mõm (D2, D3) thò ra ngoài khung mặt `to_01` gốc → làm mõm thành mảnh cứng bám `bone7` hoặc nới lưới mặt.

Lỗi máy (2026-11-16): `gen_codex.py` gọi `codex exec` không đóng stdin; chạy từ tiến trình có stdin là ống mở thì codex treo, không log, hết
giờ (M1, M2 `quang_sat_2`). Đã thêm `stdin=subprocess.DEVNULL`.

## 4. Mảnh theo concept D3 (người dùng chốt D3 2026-11-16: "làm theo bạn đề xuất"; `tai_ve/L1_duyet.png` = bản chép `L1_D3.png`)

`cua_xich_manh.py` (`can`, `soi`, `to`, `cat [K|R]`). Căn concept lên hình con gốc chỉ đo phần dưới y 300 (thân, đuôi, chân; đầu cố ý đổi
dáng): a 1,005, dời −1, 0 px, IoU phần dưới 0,947 (`mau/can.json`); viền từng part gốc chồng lên concept: `mau/_part_tren_concept.png`.
Atlas của họ đều 0,75 px / đơn vị rig (`DPU`); ảnh mảnh của mình = ảnh vùng × 2.

Con gốc là các mảnh chồng nhau, mảnh nào cũng có viền riêng (không có bề mặt liền nào chạy qua nhiều part) nên KHÔNG cần tờ thân liền:
- **K** (giữ hình bóng gốc, tờ = mảnh gốc phóng 3,3–5): `K1` đĩa (8 răng vuông), tấm lưng, vỏ cưa (trục gỉ), thân (lỗ dây ở chỗ concept
  (782, 808) đổi vào ô thân), gốc đuôi, mấu nối, bốn khúc chân (đùi gần vòm gân); `K2` hai tay (vuốt ngà trong hình bóng găng), lòng
  mắt, tròng (đồng tử dọc), mắt nhắm `>` (`yanjing_03`). Ra `tai_ve/D_K1.png`, `D_K2.png`.
- **R** (đổi dáng, gen đúng chỗ đúng cỡ trên concept; mảnh đầu chồng nhau nên mỗi tờ một mảnh đầu): `R1` hai đốt mai trước (gờ mày khấc,
  thay `to_02`) + vòng dây giật (mảnh mới) + sợi dây thẳng nằm ngang ở góc trống (dải lưới co giãn khi kéo); `R2` đốt mai sau (mảnh mới,
  bám như `to_02`); `R3` sừng móc (thay `zuoerduo`, bám bone7 + bone8 như họ); `R4` mặt có mõm + nanh + hai vằn gỉ, KHÔNG mắt (thay
  `to_01`); `R5` bốn cột quặng (thay `tofa`).
- Mã: vệt quay mờ của đĩa (`juzi_02`) đổi màu từ hình của họ (`vet_quay`).
- Bỏ: `youerduo` (gai sau đầu: D3 không có, vùng đó là mai + quặng), `jingkuai` (tinh thể loé ở skill_01; VFX làm ngoài rig).

Thứ tự vẽ dự kiến ở đầu (sau → trước): quặng (dời lên TRƯỚC mặt trong danh sách slot = nằm sau mặt) → thân, chân, đùi gần → mặt → vòng dây
→ tay (tay trước mặt như D3) → lòng mắt → tròng → mai sau → sừng → mai trước. Dây: từ lỗ bụng tới vòng; appear tay trái nắm vòng kéo ra
(skill mục 26: vật theo tay, dây là dải lưới giữa lỗ và vòng).

Kết quả mảnh (2026-11-16): 7 tờ Codex đạt lượt đầu (K1, K2, R1–R5) + R6 (hai tay). Mảnh K khớp hình bóng 0,90–0,98. Tay giữ hình bóng găng
gốc thì SAI: găng của họ to, mặt họ vẽ đè nửa trên; D3 vẽ tay nhỏ TRƯỚC mặt ôm đáy mặt → gen lại hai tay thành mảnh đổi dáng `R6`
(`tay_trai`, `tay_phai`, gắn theo lưới găng `zuoshou` / `youshou`). Ghép khung 0 idle với concept: IoU 0,976 (`rig/ghep.png`).

## 5. Rig + clip (`cua_xich_rig.py`; `inbox/cua_xich_1/rig/`, không theo git; `CX_GOC=1` dựng bằng da gốc ra `rig_goc/`)

33 xương (29 của họ + `move`, `far`, `vong_g`, `day_g`), 23 slot, 2 883 đỉnh; `.atomik` 280 KB; chiều cao game 375; mọi clip nối về
khung 0 idle 0 px; đo runtime thật 60 khung / giây: không xương nào quay ngược một vòng (lớn nhất 62° / khung ở xương dây lúc giật).
- Mảnh K: nguyên lưới của họ. Mảnh đổi dáng: lưới dày trên ảnh mình, mỗi đỉnh gắn như điểm tương ứng trên lưới part họ (`gan_theo_goc`).
- Thứ tự vẽ của mình: ... thân, chân, quặng, mặt, dây, vòng, tay phải, tay trái, lòng mắt, tròng, mai sau, sừng, mai trước.
- Vòng dây: xương `vong_g` (con của thân) treo ở bụng; giật thì `vong_g` và tay trái (`bone12`) dời cùng một vectơ thế giới (`keo`).
  Bám vòng vào tay qua trọng số thì lúc quay người (skill_03) tay trái chạy lên cạnh sừng, dây kéo chéo mặt.
- Dây: dải lưới trên MỘT xương `day_g` (gốc ở lỗ bụng); mỗi khung `day_dat` xoay day_g về đáy vòng và giãn trục x. Dải bám hai đầu bằng
  trọng số tuyến tính thì bề ngang không xoay theo: kéo ngang là dải bẹp thành sợi chỉ.
- Lúc quay người (skill_03, u 0,05–0,55) ẩn vòng + dây (bụng ra sau, vòng lộ dưới mõm như khuyên mũi).

| clip | dài | cách làm | sự kiện |
|---|---|---|---|
| idle | 7,00 | idle_01 + trò riêng: 3,5–4,5 s máy rồ (đĩa thêm 2 vòng, thân, đuôi rung) | |
| walk | 0,53 | run_01 + đuôi lắc theo bước, đĩa 2 vòng / bước | |
| appear | 2,10 | đứng, cưa tắt; giật lần 1 (0,32) máy hắt hơi, đĩa nhích; giật lần 2 (0,92) máy nổ, đĩa quay vọt, thân rung, êm dần | `keo`, `xi`, `keo`, `no` |
| attack | 1,27 | skill_01 (chồm đầu húc) + lao `move` 1,2 chiều cao, đỉnh lao lúc húc | `trung` 0,50 |
| cast | 1,40 | nén người, lao 0,9 chiều cao, quay người quật đuôi (skill_03_1, cú quay 2 khung giãn ra 0,15 s), giữ, quay về | `trung`, `cua` 0,47 |
| skill | 3,90 | giật dây 3 lần nhanh dần (máy rồ dần, đĩa to 1,35 lần), hút khí, lao, quay người, ghì đuôi cưa đẩy tới lui 3 nhịp / giây + rung, 11 nhát cưa; quay về, lùi, đĩa nhỏ lại | `keo` ×3, `no`, `hut`, `lao`, `trung` 1,78, `cua` ×11 |
| hit | 0,50 | hit_01 (mắt nhắm) | |
| die | 1,45 | die_01 + mờ 0,32 s cuối | `nga` |

Trang xem: `inbox/cua_xich_1/rig/xem.html` (đã chạy `mo_xe/thu_xem.py`: 8 nút clip, không lỗi). Tờ khung runtime thật: `rig/that/*.jpg`.

## 6. Việc tiếp

1. Người dùng xem animation.
2. Hỏi: tên, số dạng (có dạng non không); thay suất `phi_thuong` (ải 15).
3. Vào game: VFX hạt chồng lớp (chuẩn `chuan_fx/phun_lua.gif`): khói nhỏ `xi`, khói + rung `no`, hút khí `hut`, tia lửa mỗi `cua`
   (bám xương `bone25` = tâm đĩa), bụi lao; heroes.json, menu Unity.

Người dùng xem bản rig đầu (2026-11-16): "bỏ tay bên kia đi, phần quặng sắt phải ở giữa đầu, nhìn như này bị lệch sang bên kia quá".
Đã sửa: bỏ slot `youshou` (tay phía xa, `BO`); cụm quặng dời −112, +6 px concept (`CHINH_R`: tâm cụm x 966 → tâm mặt tròn x 852), hai cột
phải nấp sau mai chỉ lộ đỉnh. Khung nghỉ IoU với D3 còn 0,795 (do cố ý dời quặng). `.atomik` 277 KB, mọi clip nối idle 0 px.

Lần 2 (2026-11-16, kèm ảnh cận con gốc): "sửa lại phần quặng sắt ở đầu cho chính giữa giống con gốc, xem lại con gốc đi". Dời ngang là sai.
So 5 phương án cạnh con gốc (scratchpad `thu_quang.py`, biến `CX_QUANG="dx,dy,góc,tỉ lệ,cx,cy"`): chọn hạ 55 px + xoay 14° ngược kim quanh
(900, 560) px concept → chân cột nấp sau mai, cột cao giữa đỉnh đầu, hai cột kia xoè dọc gáy như tinh thể của họ (`CHINH_R`).

Lần 3 (2026-11-16): "ở giữa ở đây là giữa theo chiều ngang đầu cơ, bạn nhìn con gốc còn có 1 layer đầu sau nữa". Nguyên nhân thật: đã bỏ
part `youerduo` (mảng sẫm sau tinh thể = mặt xa của mũ). Trả về: tờ `K3` (`tai_ve/D_K3.png`, IoU 0,98, slate sẫm), slot `youerduo` vẽ
ngay TRƯỚC quặng trong danh sách (= nằm sau quặng). Quặng: co 0,85 quanh (930, 480) + hạ 30 px (`CHINH_R`, phương án E trong 4 phương
án E–H) để lớp sau lộ quanh như con gốc; hai lần chỉnh trước (dời ngang; hạ + xoay) bỏ. Mảnh K: kẻ nét mực 2,5 px phía trong mép hình bóng
gốc (`cat_k`) vì lưới của họ xén nửa nét viền. `.atomik` 284 KB, 23 slot.

Lần 4 (2026-11-16): "tai 2 bên không đồng bộ". Cặp tai của họ = `zuoerduo` (gần) + `youerduo` (xa); bên gần của mình là đốt mai sau + sừng
móc mặt dưới gỉ cam, bên xa (K3) là tấm nhọn trơn → không cùng kiểu. Sửa: tai xa = bản LẬT NGANG của (mai_sau + sừng) quanh x 883 px
concept, tối 0,9 (`cua_xich_manh.py tai_xa` → `manh/tai_xa.png`, `moi.json`), gắn theo lưới `youerduo` (đung đưa theo bone9 như tai của
họ), nhích +45, −45 px cho sừng lộ sau quặng (`CHINH_R`; so 5 + 3 phương án cạnh con gốc; biến thử `CX_TAI`, `CX_CHINH`). Tấm K3 giữ
làm dự phòng (`CX_TAI=`). `.atomik` 298 KB.

Lần 5 (2026-11-16): "phần đuôi tai bị hở khi cúi đầu". Tai xa là bản lật của dải mai sau = VÒM RỖNG; bên gần lòng vòm có mặt + mai lấp, bên
xa không có gì sau nó → idle 1,6–2,3 s (đầu cúi ~40°) tai đung đưa lệch nhịp đầu, đuôi vòm rời đầu, lộ nền. Sửa trong `tai_xa()`: lấp kín
bao lồi của hình bằng màu đá (trung vị phần tô) + viền mực 4 px trước khi lật → tấm liền, chân luôn nấp sau quặng / mai. Soi cận khung 1,8 s:
hết khe. `.atomik` 303 KB (quá đích 300 KB 3 KB, dưới trần 500 KB).

## 7. Vào game (2026-11-16, người dùng: "ok cho vào game")

- **Suất**: tướng 4 đảo Kim = id `phi_thuong` (ải 15 "Tháp Canh Thép"). Giữ id, chỉ số, hiệu ứng thẻ, số mảnh, SỐ DẠNG 2 (chưa có rig dạng non:
  cả hai dạng trỏ `cua_xich_1`, cỡ 0,92 / 1,1) → stages, golden không đổi. Script `quai/doi_cua_xich.py` (hàm của `doi_phap_lua.py`): tên
  **Thiết Cưa**, danh hiệu "Tinh linh đuôi máy cưa", dòng "Dòng Thiết Cưa"; thẻ Đâm Thương → **Quật Cưa** (wheel), Mưa Thương → **Cưa Liên
  Hồi** (crack), Giáp Lam → **Mai Quặng** (shield). **Tên do Claude tạm đặt, chờ người dùng chốt.** `chep`: `Resources/cua_xich_1/`.
- **Unity** (cầu MCP 127.0.0.1:8080, các phiên khác xác nhận không đụng Unity): refresh, "Nhập dữ liệu" (88 tướng, 265 thẻ riêng, 350 ải),
  "Gắn dạng .atomik" (prefab `phi_thuong` giữ 2 dạng `cua_xich_1`, 8 clip). Menu chạy lâu làm rớt phiên MCP: chờ dòng `[Atomik]` trong
  Editor.log.
- **Hiệu ứng** `Assets/01 Script/Game/Battle/HatCua.cs` (đi đường "n_"): `KimAtk["phi_thuong"] = n_cua_huc` (húc: chớp sắt, tia lửa, dăm thép,
  bụi; thêm vào `HatVoi.AtkLao`), `KimFx["phi_thuong"] = n_cua_quat` (quật đuôi; thêm vào `HatKiem.CastLao` để sân nắn cú lao của cast tới 72 %
  quãng, không có thì con đứng yên còn trận bắn TIA NƯỚC mặc định) / `n_cua_lien` (giật dây: khói ở đĩa, máy nổ: khói to + tia lửa; 1,05–1,5 s
  vệt gió hút vào đĩa + vòng gió co; ghì cưa 11 nhát tia lửa + dăm, nhát cuối mạnh + vòng thép); `Themes["phi_thuong"]` tia lửa vàng cam, vòng
  thép, mảnh đá phiến. Hạt toé ở TÂM ĐĨA = đỉnh lao (72 % quãng) + độ vươn đuôi đo trên rig ở dáng quay người (quật 0,66 / 0,20, ghì 0,68 /
  0,15 chiều cao): rig vươn đuôi nằm ngang còn sân nắn cú lao chéo nên đĩa nằm ngang chân / bụng đối thủ (bản đầu đặt ở thân đối thủ → tia lửa
  toé trên đầu tướng).
- **Bị cắt dọc** ở chiêu cuối (cú lao trong rig + đuôi vươn ~2,2 chiều cao > khung mặc định ±1,7): `cua_xich_rig.py` đo phạm vi ngang xa nhất mọi
  clip, khai `span` 4,68.
- **Soi trong trận**: menu "PokiClash/Thử/Đảo Kim: riêng Thiết Cưa…" (`Editor/KimFxTour.cs`), ảnh `Temp/PokiShots/kim_fx/phi_thuong_1sao_*.jpg`,
  tờ chép ở `inbox/cua_xich_1/trong_game/` (`tran_danh|mana|ult.jpg`, cận `can_mana.jpg`, `can_ult.jpg`). Lần 3 đạt: húc tới, quật đuôi tới
  đối thủ tia lửa ở đĩa, chiêu cuối ghì cưa ở chân / bụng đối thủ.
- EditMode 104 / 107: hỏng `PrefabOnlyTests` cũ (UI/Kit) và 2 test do khối `tam_kiem` trong heroes.json đã bị phiên khác đổi (ky_nguyen_2,
  2 dạng; golden chưa tính lại) — đã báo phiên assets-4d.

## 8. Dạng 2 (người dùng 2026-11-16 sau khi dạng 1 vào game: "làm dạng 2 của tướng này")

Kho tham khảo không có dạng tiến hóa của con gốc (chỉ monster_3374 có mảnh `juzi` = cưa; 3373 / 3375 là con khác) → dạng 2 trên CÙNG rig
(skill "DẠNG KHÁC trên CÙNG rig gốc"): `CX_DANG=2 cua_xich_rig.py` (thư mục `inbox/cua_xich_2/`, tên xuất `cua_xich_2`). Tỉ lệ ở xương gốc từng
bộ phận (`TI_LE`, đè bằng `CX_TL`): thân `bone19` 1,12, đầu `bone7` 0,82, gốc đuôi `bone18` 1,12 (cả chuỗi đuôi + đĩa), gốc tay `bone12`,
`bone15` 0,9. Toạ độ gắn của mảnh mới (moi.json, att_idle0) tính trong bộ xương KHÔNG đổi tỉ lệ (`sk_c`) để mảnh co / phóng cùng xương; dạng 1
không đổi (TI_LE rỗng). Chưa có da dạng 2 thì dựng bằng da dạng 1.
- Bố cục: `mau/bo_cuc.png` (dạng 2), `mau/bo_cuc_d1.png` (dạng 1), đặt vào khung: `bo_cuc_khung.png`, `bo_cuc_d1_khung.png`; tờ so `_so_d1_d2.png`.
- Concept lượt 1 (`cua_xich_da2.py concept`, gói `gui_gpt/cua_xich_2/`): ảnh 1 bố cục dạng 2, ảnh 2 dạng 1 trong game, ảnh 3 concept D3 (chỉ nét).
  Ba hướng: A "quặng gỉ dữ" (sắt đen viền gỉ, 5 cột quặng đầu gỉ đỏ, sừng dài cong, mõm hai nanh, răng đĩa to); B "thép nung" (thép súng, mép
  đốt mai răng cưa, quặng thành thỏi đầu cam đỏ nung, răng đĩa đầu cam); C "thép lam bạc" (mai lam viền bạc, quặng lam đầu bạc, sừng bạc).
  Chờ người dùng chọn.
  Kết quả: B, C đạt lượt đầu (khớp bố cục 0,929 / 0,930; `mau/_so_ABC.png`, trang `inbox/cua_xich_2_xem_concept.html`). A bị kiểm duyệt đầu
  ra của công cụ vẽ ảnh chặn; đã đổi chữ màu "rust-red" → "rust-orange" trong `luot_1_concept_A.txt`, gen lại thì Codex hết hạn mức (mở lại
  19:01). Chờ người dùng chọn.
- Người dùng (lượt 1 → 2): "tôi thích B hơn nhưng nhìn chưa đủ khác biệt, phải to hơn và chiến hơn". Rig to hơn: `TI_LE` thân 1,22, đầu 0,8,
  đuôi cưa 1,3, tay 0,88, chân `bone3` / `bone5` 1,25 (bàn chân tụt đất → nâng `bone2` lên (k − 1) × chiều cao hông so với đáy cẳng chân =
  20,5 đơn vị); bố cục mới `mau/bo_cuc.png`, chiều cao game 402 (dạng 1: 372). Hướng `B2` (`cua_xich_da2.py concept B2`): như B + sừng thú
  húc to chĩa tới, mày khấc chữ V, hai nanh to, thỏi quặng cao to, mép mai răng cưa sắc, thân hai đốt giáp răng cưa, vuốt dài. Codex hết
  hạn mức tới 19:01: tác vụ nền tự gen B2 hai lần lúc 19:02 (`tai_ve/L1_B2.png`, `L1_B2_2.png`).
