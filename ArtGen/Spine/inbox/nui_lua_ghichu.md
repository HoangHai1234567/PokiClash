# Khủng long núi lửa (`nui_lua`): tướng thứ 10 (cuối) đảo Hỏa, FINAL BOSS

Bắt đầu 2026-11-14 (máy ổ D). Con gốc của rig: `monster_3654` (thú đá bốn chân, lưng mọc ống núi lửa; game tham khảo, kho
`D:\RefAnimation\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `idle_01`). Xương, lưới, chuyển động gốc là của nhà phát hành
game đó (như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình. Suất 10 đảo Hỏa = ải 70 ("Miệng Núi Lửa", `IslandGen.Plan Hoa`),
id game **`lan_hoa`** (đang là Lân Con / Lân Ngàn Năm / Thánh Lân, `lan_hoa_1..3`, boss `lan_hoa_boss`). Mã làm việc `nui_lua`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-14)

- "tướng cuối cùng đảo hỏa; concept **khủng long núi lửa như con gốc**".
- "**idle và walk làm như con gốc**, sửa đi 1 chút cũng được".
- Đánh thường: "**lao vào húc đối thủ**".
- Chiêu mana: "**há mồm ra tụ 1 quả cầu lửa rồi bắn**".
- Chiêu cuối: "làm giống **skill_04**, **bẻ các đỉnh núi lửa trên lưng theo các hướng khác nhau**, bắn ra các viên **đạn lửa bay kiểu vòng cung random
  nhưng vẫn lao vào người đối thủ kiểu homing missile** (đạn bay thế nào là **làm bằng code**)".
- "**die làm giống họ**".
- "con này **final boss**, cần làm **thật đẹp, hoành tráng, impact**, thêm **fx khói ở đỉnh các núi lửa trên lưng**".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3654/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample.json` 13 clip 30 khung/giây, `khung/`, `mo/`, `parts/`)

75 xương, 59 slot (58 hình, đều là lưới, hầu hết bám CỨNG một xương), 13 clip, 3 590 khoá. Con **nhìn sang PHẢI**, đầu cúi gằm ở dưới phải. Ảnh atlas
0,500 px / đơn vị rig; dáng idle x −535..555, y −21..994. Script mổ: `nui_lua.py` (`mo`, `nhom`, `part_goc`; dùng lại hàm của `hoa_ho.py`).

Ràng buộc: 8 IK chân (`L1..L4`, `R1..R4`; đã nướng thành FK qua mẫu khung `l`), không transform, không path, không physics. 10 xương không thừa hưởng
xoay của cha (inherit 2: `bone27..29`, `bone45`, `bone49`, `bone52`, `bone56`, `bone62`): rig mình tính góc riêng từ ma trận thế giới. **Không clip nào
đổi thứ tự vẽ, không clip nào đổi hình.** Họ có 6 cụm khói `P_yan_01..06` (mỗi cụm một chuỗi 3–4 xương) và mắt `P_yanjing_02` nhưng KHÔNG bật ở clip nào.

Bảng nhóm part (số = thứ tự vẽ sau → trước):
| nhóm | slot | là gì, bám xương nào |
|---|---|---|
| ống núi lửa | 15 slot `P_jiao_01..16` (không có 05) | mỗi ống một lưới cứng. Lưng sau: `09` (bone40), `10` (bone41), to và cao nhất. Giữa: `02` (bone39), `01` (bone38). Xa, sau đỉnh núi: `15`, `14`, `13` (bone42, 43, 44). Mông: `03`, `04` (bone30, 31), `06`, `07` (bone33, 34), `08` (bone11, theo đùi sau gần). Đầu: `11` (bone9 = hàm trên), `12`, `16` (bone7 = đầu) |
| đỉnh núi lưng | 20–26 `P_beijia_01..07` | các phiến đá đen lớn giữa lưng (bone26..29, bone3, bone5/6); `P_beijia_07` dùng lại ảnh `P_beijia_05` |
| bụng | 19 `P_duzi` (lưới 26 đỉnh, 5 xương sống bone3..bone6b: mảng đỏ, chỉ lộ khe) + 30–35 `P_duzi_01..06` (sáu tảng đá sườn, bone3..bone6) | |
| đầu | 36 `P_shagne_1` (hàm trên + sọ, có vẽ sẵn hai ống; bone9 0,71 + bone8 0,29), 37 `P_xiae_1` + 28 `P_xiae_2` (hàm dưới gần / xa, bone8), 29 `P_houlong` (họng sáng, bone8) | bone7 = đầu (cha của hai hàm), bone8 = hàm dưới, bone9 = hàm trên; cổ là bone6b |
| chân trước gần | 52–57 `P_qiantuiR1..5` + `P_jiaozhi_01` (ba móng) | `R5` (bone37) và `R1` có vẽ sẵn ống núi lửa |
| chân sau gần | 41–44, 51 `P_houtuiR1..5` | bàn là trụ đá đầu đỏ, không móng |
| chân trước xa | 14–17 `P_qiantuiL_01..03` + `P_jiaozhi_02` | |
| chân sau xa | 5–7 `P_houtuiL_01..03` | gần như khuất |

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho |
|---|---|---|---|
| `idle_01` | 4,00 | thở, các ống lắc nhẹ | **idle** |
| `run_01` | 0,80 | chạy tại chỗ | **walk** |
| `skill_01_1` | 1,33 | lùi lấy đà 0–0,47 (thân lùi 207), lao tới 0,47–0,60 (thân tới +184), về | **attack** (húc) |
| `skill_01_2` | 1,33 | rạp xuống 0,12–0,48, chồm dựng lên 0,61–0,73, đáp | (chưa dùng) |
| `skill_01_3` | 1,33 | nhún tại chỗ | (chưa dùng) |
| `skill_02` | 1,67 | ngả ra sau, chân trước duỗi 0,30–0,76; dộng thấp 0,91; về | **cast** (thân) |
| `skill_03` | 2,00 | dựng đứng hai chân sau 0,36–0,73; dộng xuống 0,91; về | **appear** (đoạn dộng) |
| `skill_04` | 3,00 | gồng thấp 0,27; nhô 0,55–0,82; gồng 1,09; nhô 1,36–1,64; **dộng xuống và BẺ các ống** 1,91 (ống lưng sau `bone39..41` ngả +60..80° ra sau, ống xa `bone42..44` ngả ra trước, `bone30/31` ±20°); giữ tới ~2,6; về | **skill** |
| `hit_01/02`, `block_01`, `stun_01` | | giật lùi; `hit_02` há mồm to nhất (61°) | **hit** = hit_01 |
| `die_01` | 1,00 | chồm lên rồi đổ sập, các ống xoè ra | **die** + tan 0,45 |

Độ há mồm = xoay `bone9` − `bone8`: đứng 28–42°, lớn nhất 61° (`hit_02`). Đầu con gốc cúi gằm (`bone7` −62°): muốn "há mồm bắn cầu lửa" phải NGẨNG đầu.

## 3. Rig thử trên DA GỐC (không phụ thuộc màu; chỉ để soi clip trong máy, KHÔNG đưa vào game)

`NL_GOC=1 py -3 -I nui_lua_rig.py` → `inbox/nui_lua_1/rig_goc/` (`xem.html`, `khung_<clip>.png`, `.atomik` 152 KB): 109 xương (75 của họ + `move`,
`mieng`, 15 `ong_<nn>`, 16 `khoi_<nn>_<j>`), 68 slot, 534 đỉnh. Mỗi slot dùng NGUYÊN lưới của họ. Chiều cao 1015 (không tính khói).

Xương thêm: `mieng` (con của `bone7`, giữa hai hàm trước họng, trục x chĩa ra mõm): chỗ tụ cầu lửa; `ong_<nn>` (miệng từng ống `P_jiao_<nn>`, đặt
theo trục chính của lưới ống, trục x chĩa dọc ống ra ngoài): chỗ nhả khói, chỗ bắn đạn; `khoi_<nn>_<j>` (con của `ong_<nn>`): cụm khói.

Clip (8 + aura), mỗi clip là co giãn giờ MỘT clip nguồn + kênh riêng trên `move`, hai hàm, cổ, từng ống (không làm chân rời đất):
- `idle` 4,0 s = idle_01; `walk` 0,8 s = run_01; `hit` 0,5 s = hit_01; `die` 1,45 s = die_01 + tan (khói tắt trong 0,25 s đầu).
- `attack` 1,15 s = skill_01_1: lùi lấy đà 0–0,16 rồi ghìm tới 0,40 (đầu cúi thêm 9°); lao húc 0,40–0,50 (`huc` = `trung` 0,50; đầu hất 16°, thân dồn
  theo chiều húc 1 khung); rung, về. Sân tự kéo cả con lao tới đối thủ (attack không nằm trong `stay`).
- `cast` 1,85 s = skill_02 đoạn ngả ra sau + NGẨNG đầu (cổ `bone6b` +14°, đầu `bone7` +30°) + HÁ mồm (hàm trên +20°, hàm dưới −24°, rung 1,4°):
  `tu` 0,30 (bắt đầu tụ), giữ trôi tới `nha` = `trung` 1,05 (chồm nhẹ, đầu giật, cả thân giật lùi 34), ngậm mồm, về. `game.muzzle` = `mieng` lúc nhả.
- `skill` 3,46 s = skill_04: gồng hai nhịp như họ (nén còn 1,28 s); dộng + bẻ ống `be` 1,52; GIỮ dáng bẻ, bắn 16 phát cách 0,07 s từ 1,62 tới 2,84
  (sự kiện `ban`, chuỗi = số ống, mỗi phát ống đó co dọc 2 khung rồi bật quá đà; thứ tự `BAN` trong script); `het_ban` 2,84; về. Các ống nhỏ họ để
  yên (`bone33`, `34`, `38`...) được bẻ thêm mỗi ống một hướng (`BE_THEM`). Há mồm gầm trong lúc bắn. `trung` = phát đầu (1,62): đạn bay do code.
- `appear` 1,30 s = đoạn dộng của skill_03: rơi từ trên xuống (1,15 chiều cao, gia tốc), `dap_dat` 0,32, nén 1 khung, đứng dậy.
- `aura` 2,4 s lặp: 16 cụm khói ở 8 ống lớn (`KHOI`: 09, 10, 02 mỗi ống 3 cụm; 14, 15, 13 hai cụm; 01, 03 một cụm): trôi dọc trục ống, nở, xoay,
  mờ dần. Ảnh khói hiện là cụm mây giữ chỗ; có ảnh của mình thì đặt `inbox/nui_lua_1/manh/khoi.png`.

Nối: appear, attack, cast, skill, hit về idle 0,00 px; idle khép vòng 0,55 px; walk 3,8 px (bước thường 33,6).

## 4. Concept (đề xuất của Claude, CHỜ người dùng chọn)

Script: `nui_lua_bo_cuc.py` (sơ đồ bố cục 1536 × 1024 ở khung 0 idle, 0,89 px / đơn vị rig, gốc rig ở (767,6; 950,0); mỗi ống tô dải dung nham +
elip miệng núi lửa theo trục ống; mắt ở chỗ `P_yanjing_02`), `build_nui_lua.py` (gói `gui_gpt/nui_lua_1/`; ảnh mẫu: sơ đồ, Golem lửa đã duyệt,
Giác Mộc, bản đồ; toạ độ trong prompt đọc từ `mau/bo_cuc.json`).

Giữ của con gốc (vì mỗi part cứng phải khớp hình bóng lưới của họ): thú bốn chân thấp rộng nhìn phải, đầu cúi thấp, đám ống núi lửa nghiêng trên
lưng, đỉnh núi sẫm ở giữa, hàng đá sườn, hàm dưới màu khác có răng cưa. Của mình: nét bút + chì sáp tô phẳng; cột đá có cạnh với dải dung nham phẳng
mép nhỏ giọt, miệng núi lửa elip có lõi, vết nứt chẻ nhánh; sọ khủng long có gờ mày và MỘT mắt xếch rõ; bảng màu riêng (không đỏ hồng tím như con gốc).
KHÔNG vẽ khói, lửa trong concept (rig và game thêm).

Ba hướng màu:
- `den` **A · bazan đen**: đá than #56505C, đỉnh lưng #36323C, dung nham cam #F07828, lõi vàng #FACC50, hàm dưới + móng ngà #DEC496.
- `do` **B · đá xỉ đỏ**: đá đỏ gạch #A44E3A, đỉnh lưng nâu sẫm #622E2A, dung nham vàng #F8B032, lõi kem #FCE896, hàm dưới + móng than #3C3236.
- `lam` **C · đá phiến lam**: đá xám lam #627088, đỉnh lưng #3C445A, dung nham đỏ cam #EC5C2C, lõi vàng #FAC846, hàm dưới + móng ngà #E2D0AA.

Ảnh về `inbox/nui_lua_1/tai_ve/L1_<hướng>.png`.

## 5. Việc tiếp (sau khi người dùng chọn concept)

1. Mảnh: tờ khung part (hình bóng kín tô phẳng theo lưới của họ, IoU ≥ 0,9) cho 51 part; nhóm: ống lớn / ống nhỏ / đỉnh núi / đá sườn + bụng /
   đầu (sọ có mắt, hai hàm, họng) / bốn chân. Thêm: mắt nhắm (hit, die), ảnh khói của mình, (tuỳ) bản ống "nguội" cho die.
2. Rig da mình (`nui_lua_rig.py` không đặt `NL_GOC`; cần `nui_lua_manh.py` có `zs()`), soi runtime thật, soi cận miệng lúc há to nhất.
3. VFX (C#, ngoài rig; `HatNuiLua.cs` kiểu `HatNham.cs` / `HatRua.cs`, đi đường "n_"):
   - đòn húc: bụi đá lúc bật, chớp toé + dăm đá + tia dung nham lúc chạm, rung mạnh;
   - chiêu mana: hạt lửa hút vào `mieng` + cầu lửa lớn dần trong lúc tụ (0,30 → 1,05), nhả: chớp ở mõm, cầu bay có đuôi lửa khói, nổ lớn ở đối thủ;
   - chiêu cuối: mỗi sự kiện `ban` một viên đạn lửa rời miệng ống đó (toạ độ `ong_<nn>` ở dáng bẻ), bay theo ĐƯỜNG CONG NGẪU NHIÊN rồi bám đích
     (tên lửa tầm nhiệt: vận tốc đầu dọc trục ống + lệch ngẫu nhiên, quay đầu về đích với tốc độ quay tăng dần, đuôi khói + lửa), nổ lần lượt ở đối
     thủ, phát cuối nổ lớn; khói phụt ở miệng ống mỗi phát; rung màn theo loạt;
   - khói đứng: đã có trong rig (aura); xem có cần thêm than hồng bay lên bằng lớp hạt không.
4. Vào game: thư mục Resources mới, `heroes.json` khối `lan_hoa` (không đè `lan_hoa_1..3` cũ), tên, số dạng, thẻ, boss `lan_hoa_boss`: hỏi người dùng.

## 4b. Lượt concept 1 đã về (2026-11-14 12:56)

`tai_ve/L1_den.png` (283 s, có chờ khoá Codex), `L1_do.png` (131 s), `L1_lam.png` (188 s). Trang so `inbox/nui_lua_xem_concept.html`. Cả ba: tô phẳng,
nét bút + vân sáp, không khói, không lửa, không phát sáng; ống có dải dung nham nhỏ giọt + miệng lõi + vết nứt chẻ nhánh; một mắt xếch; hàm dưới
màu khác có răng cưa; hai bàn chân trước ba móng, chân sau đầu nhúng dung nham. Nhận xét của Claude:
- `den` (A): bám sơ đồ nhất (hai ống cao bên trái, đỉnh núi sẫm, ba ống xa, đầu cúi dưới phải), dung nham cam nổi nhất trên đá đen, đọc "núi lửa" rõ
  nhất. Đầu hơi nhỏ, mõm ngắn.
- `do` (B): LỆCH bố cục (thân bè thấp và rộng hơn sơ đồ, đỉnh núi thấp, đầu to ra phía phải); đỏ trên vàng ít tương phản. Chọn thì phải gen lại.
- `lam` (C): bám sơ đồ, đầu khủng long rõ nhất (mõm dài, gờ mày, mắt dữ), đá lam + dung nham đỏ cam lạ mắt, khác hẳn các tướng Hỏa khác; đầu
  ngẩng hơn rig một chút.
CHỜ người dùng chọn (chưa có `L1_duyet.png`). Đề xuất của Claude: A, có thể lấy kiểu đầu của C.

## 6. Bản nháp hiệu ứng và số đo (2026-11-14)

- `inbox/nui_lua_1/HatNuiLua.cs`: BẢN NHÁP ngoài Assets, chưa biên dịch thử (không đặt vào Assets lúc phiên khác đang dùng Unity): `NNuiHuc`
  (n_nui_huc), `NNuiCau` (n_nui_cau), `NNuiTen` (n_nui_ten: đạn tầm nhiệt, đường bay Bézier bậc ba ngẫu nhiên + lắc ngang tắt dần, tăng tốc vào
  đích; đầu đạn là MỘT hạt vẽ riêng, đuôi sinh trong `upd`). Cuối file ghi các chỗ phải nối (PlayNuoc, FireFx, HoaAtk, AtkLao).
- `inbox/nui_lua_1/_do_hat.py`: đo miệng ống lúc bắn (`NuiOngP`, `NuiOngG`), miệng ống dáng đứng, `mieng` lúc tụ / nhả. Đổi clip hay rig thì chạy lại
  rồi chép số vào file C#.
- Khói trong rig (aura) ghép từ ảnh hạt khói của game (`Assets/03 Art/Fx/Hat/hat_ssolid_<i>`, `hat_sblob_<i>`), ba biến thể xám.

## 4c. Lượt 2 concept (2026-11-14 chiều)

Người dùng xem ba hướng màu trên artifact, nói: "A đẹp nhưng nhìn hơi giống con gốc, sáng tạo hơn chút". Con gốc cũng là đá đen, ống đỏ ở
đỉnh, hàm nâu, nên A trùng cả màu lẫn ý. Lượt 2 giữ bảng màu A, đổi THIẾT KẾ (đề xuất của Claude, chờ chọn):

| Mã | Ý | Mảnh thêm ngoài rig |
|---|---|---|
| `giap` | khủng long giáp: mũ xương ngà (sọ trên), khiên hông (`P_houtuiR5`), khiên vai (`P_qiantuiR3`), vảy sườn (`P_duzi_01/02`), hàm dưới đá sẫm răng ngà; ống đầu thành gốc sừng rỗng; mỗi ống là nón núi lửa có vân tầng; đỉnh lưng là miệng núi lửa chính + sông dung nham | đuôi ba đốt + chuỳ xương (sau mông, x 90..380) |
| `sung` | khủng long sừng: hai sừng húc ngà chĩa ra trước rồi vểnh lên (hợp đòn húc); mỗi ống là tháp vòng đá xếp tầng; tảng sườn có núm xương; miệng núi lửa chính | hai sừng (gắn xương đầu bone7) |
| `cot` | cả con dựng bằng cột bazan lục giác; mỗi ống là bó cột so le; đỉnh lưng là vách cột bậc thang | không |

- Sơ đồ: `nui_lua_bo_cuc.py giap|sung|cot` (thêm `vai`, `ong_mau`, `mieng_chinh`, `duoi`, `sung` trong `HUONG`).
- Prompt: `build_nui_lua.py` (khối "Lượt 2": `ong_ve`, `peak`, `flank`, `head`, `them_parts`, `pal` đè lên bản mặc định).
- Ghi nhớ khi dựng rig: đuôi và sừng cần xương mới + lưới riêng + kênh lắc riêng (đuôi theo hông, sừng theo đầu); khung `span` rộng thêm.
- Phần "khối sườn" nhìn thấy thực ra là mảnh gốc chân (`P_houtuiR5`, `P_qiantuiR2..5`), còn `P_duzi_0x` phần lớn bị che.

Kết quả lượt 2 (16:51–16:56, `tai_ve/L1_giap.png`, `L1_sung.png`, `L1_cot.png`; đã đưa lên artifact cùng lượt 1):
- `sung`: ra dáng boss nhất, đầu rõ, sừng hợp đòn húc; hơi nhiều vạch dung nham. ĐỀ XUẤT của Claude.
- `giap`: khác hình bóng con gốc nhất (đuôi chuỳ, mảng ngà), núi lửa rõ; bốn gốc sừng trên đầu rối, mặt hiền hơn.
- `cot`: gọn, lạ, nhưng ít núi lửa, ít khủng long, kém hoành tráng.
- CHỜ người dùng chọn (có thể ghép: sừng + đuôi chuỳ).

## 4d. Người dùng chốt concept (2026-11-14 ~17:00)

- "Ok concept này ổn, lấy con sừng" → `tai_ve/L1_duyet.png` = `L1_sung.png`. Bốn câu hỏi kèm (suất `lan_hoa`, tên / số dạng, `appear`,
  16 phát) người dùng KHÔNG trả lời: giữ các giả định cũ, hỏi lại khi báo cáo.

## 7. Mảnh theo khung part (`nui_lua_manh.py`, prompt `build_nui_lua.py manh`; bắt đầu 17:05)

- Dùng lại bộ máy `hoa_ho_manh.py` (hình bóng, xếp ô, `cat_part`, `so_part`); mọi mảnh là đá cứng nên tất cả đi đường KHUNG PART, không có tờ liền.
- 7 tờ (`mau/part_<tờ>.png` + `.json`): O1 (× 2,1) năm ống lớn; O2 (× 3,3) tám ống nhỏ + `P_jiao_08`, `P_jiao_16` (đá trơn); L (× 2,5) đỉnh
  `P_beijia_03` (miệng núi lửa chính + sông dung nham) + năm phiến lưng (`P_beijia_05` dùng chung cho slot `P_beijia_07`); D (× 3,2) sọ, hàm
  dưới, răng xa, lửa họng, HAI SỪNG, hai bàn móng; B (× 2,7) lòng bụng + sáu vỏ sườn; C1 (× 3,1) hai chân gần; C2 (× 4,2) hai chân xa.
- Thiết kế từng ô vẽ bằng mã (không lấy hoa văn của họ): ống = vành cam + ba giọt + lòng vàng ở đầu miệng (trục lấy từ `bo_cuc.json`, hai
  mảnh chân có ống thì dò lòng miệng màu đào trong ảnh của họ), 1–2 khe dung nham võng; vỏ sườn: mép trong đỏ của họ → dung nham; bàn chân
  sau: đáy nhúng dung nham mép răng cưa; núm xương ngà ở tâm phần không bị che của 4 tảng sườn; sọ: mắt vàng khe dọc vẽ bằng mã ở chỗ
  `P_yanjing_02`, khối lòng miệng sẫm, hai miệng ống trên hai thuỳ sọ (ảnh sọ của họ gồm cả hai ống).
- SỪNG (`sung_gan`, `sung_xa`): hình bóng tự dựng từ đường Bézier trên sơ đồ, đổi sang toạ độ riêng của `bone9` (`mau/sung.json`); rig gắn
  bằng `them_sung` (cứng theo `bone9`; sừng xa vẽ sau mọi mảnh, sừng gần ngay sau `P_xiae_1`).
- Rig thêm `ong_cc` (miệng núi lửa chính, bám xương của `P_beijia_03`) + 3 cụm khói.
- Gen: `chay_hoa.py` chạy nền từ 17:09 (D, O1, O2, L, C1, C2, B).

## 8. Mảnh đã về, rig da mình (2026-11-14 17:09–17:35)

- Gen một lượt 7 tờ (D 98 s, O1 81 s, O2 129 s, L 76 s, C1 208 s, C2 89 s, B 96 s). IoU 0,94–0,99; hai sừng 0,88 và 0,87 (mũi mảnh), nhìn trên
  rig không lệch. Tờ so `mau/so_part.png`.
- Soi rig lần đầu thấy ba lỗi → sửa:
  1. Màu đá lệch giữa các tờ (C1 xanh xám hơn các tờ ống) → `nui_lua_manh.py can_mau`: đưa màu đá trung bình từng tờ về màu của O1 + O2
     (đích ≈ 112, 93, 104), chỉ đụng điểm ảnh họ đá. CHẠY SAU khi cắt xong mọi tờ.
  2. Hai miệng ống trên hai thuỳ sọ trông như hai con mắt → bỏ (thuỳ sọ là đá trơn, gốc sừng).
  3. Núm xương tam giác trông như hình dán → vẽ thành gai xương cong có rãnh ở gốc.
  Sọ + bốn tảng sườn gen lại ở tờ sửa `S` (× 3,5; `cat_part S ep`), `part_S.json` xếp sau nên `zs()` lấy tỉ lệ mới.
- Rig: `py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/nui_lua_rig.py` → `inbox/nui_lua_1/rig/`: 113 xương, 73 slot, 554 đỉnh,
  9 clip, 11793 khoá, atlas 1184 × 1208, `.atomik` 387 KB; nối về idle 0,00 px. Trang `rig/xem.html`.
- Đã soi (bộ vẽ Python, khung tĩnh): idle, attack, cast, skill. Sừng theo đầu, hàm há lộ lửa họng, ống bẻ đúng. `NL_SACH=1` cho khung sạch.
- CHƯA: xem ở tốc độ thật / runtime Spine; đo lại điểm hiệu ứng (`_do_hat.py`) cho `HatNuiLua.cs` (thêm `ong_cc`); vào game; VFX.
- Đã đưa bốn khung tĩnh + concept lên artifact riêng tư (người dùng không xem được file trên máy). CHỜ người dùng xem rồi mới vào game.

## 9. Xem động + dạng 1 (2026-11-14 18:00–)

- Người dùng: "Tôi không xem được animation, không play được" (xem từ thiết bị khác, không mở được `rig/xem.html`) → `inbox/nui_lua_1/_xem_dong.py`
  xuất từng clip thành WebP lặp bằng bộ vẽ Python (`rig/dong/<clip>.webp`; idle ghép 3 vòng × 20 khung/giây để khói khép vòng), đưa lên artifact
  riêng tư cùng link cũ. Chỉ hình tự vẽ; không đưa da gốc, không đưa file rig.
- Người dùng: "**Ok làm dạng 1 đi**" → hiểu là rig dạng lớn được; làm thêm dạng 1 (con non). Suất, tên, `appear`, số phát vẫn chưa được trả lời.
- **Dạng 1 = bản CHIBI vẽ riêng** (mã `nui_lua_non`, `nui_lua_non.py`), đi thẳng đường của hổ con bản chibi (bản ghép da dạng lớn + đầu phóng to của
  hổ đã bị chê). Tỉ lệ đổi trên rig: `NL_DANG=non` trong `nui_lua_rig.py`: đầu `bone7` × 1,5; cổ `bone6b` ngẩng 48° (con gốc cúi gằm; `bone6` còn
  mang hai phiến lưng nên không xoay ở đó); gốc bốn chân `bone10/14/18/22` rút cùng một quãng (chân thấp nhất × 0,8) và `bone3` hạ đúng quãng đó;
  chỉ giữ bốn ống 09, 02, 14, 03 (× 0,6) + miệng núi lửa chính; phiến lưng × 0,82 (`bone26` là con của xương đầu nên bù lại); không sừng; chiêu
  cuối 8 phát. Hình bố cục `inbox/nui_lua_non/mau/bo_cuc_chibi.png` (+ `.json` ghi các số).
- Concept: `nui_lua_non.py concept` → `gui_gpt/nui_lua_non/luot_0_concept_A.txt` (theo bố cục), `_B.txt` (tròn hơn); ảnh mẫu: concept dạng lớn, hình
  bố cục, hổ con chibi đã duyệt, ảnh mốc nét. Thiết kế đề xuất: đá cuội tròn, một mắt to, hàm dưới ngà rời có ba răng sữa, hai nụ sừng ngà, MỘT núi
  lửa nhỏ mập + ba ống nhỏ, bốn chân trụ ngắn. Gen từ 18:2x (nghỉ 20 giây giữa hai tờ cho phiên assets-4c chen khoá Codex).
- Việc tiếp sau khi người dùng chọn: mảnh "đúng chỗ, đúng cỡ" từ concept (như `hoa_ho_non.py manh_prompt`), cắt và lắp bằng lưới riêng bám xương
  của họ (như `hoa_ho_chibi.py`): đầu trên (cứng `bone9`/`bone7`), hàm dưới (`bone8`), thân, núi lửa chính, ba ống (mỗi ống cứng theo xương ống),
  bốn chân (ống co dãn: đỉnh bám thân, bàn bám xương bàn; bài học của hổ con).
- Concept dạng 1 đã về 18:56–18:58: `inbox/nui_lua_non/tai_ve/L1_A.png` (bám bố cục; núi lửa chính to, ống không che đầu, hàm dưới tách rõ; ĐỀ
  XUẤT của Claude), `L1_B.png` (tròn hơn; tảng vai / hông to, một ống đứng ngay trước vai sát đầu, khó tách mảnh hơn). Đã đưa lên artifact
  (mục trên cùng). CHỜ người dùng chọn A / B (chưa có `L1_duyet.png` của dạng 1).

## 10. Dạng 1 bản chibi: mảnh + rig (2026-11-14 19:05–19:30)

- Người dùng chọn "**A**" → `inbox/nui_lua_non/tai_ve/L1_duyet.png` = `L1_A.png`.
- Mảnh "đúng chỗ, đúng cỡ" từ concept (`nui_lua_non.py manh_prompt` → `gui_gpt/nui_lua_non/luot_1_chibi_<tờ>.txt` → `tai_ve/C_DAU`, `C_THAN`, `C_CHAN`
  (bốn chân + ống trước), `C_NUI`, `C_ONG` (ống trái, ống phải)); cả năm tờ đạt ngay lượt đầu. Cắt: `nui_lua_chibi.py cat` → `manh_chibi/` 11
  mảnh + `dat.json`; ghép lại lệch concept 3,7 % điểm (`_ghep.png`). Hàm dưới tách khỏi ảnh đầu theo màu ngà.
- Rig: `NL_DANG=chibi py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/nui_lua_rig.py` → `inbox/nui_lua_non/rig/` (`nui_lua_non`): 93
  xương, 19 slot, 883 đỉnh, 9 clip, `.atomik` 203 KB, cao 793. Dùng bộ lắp của hổ con (`hoa_ho_chibi.lap`) với bảng riêng (`nui_lua_chibi.py`):
  đầu cứng `bone7`; núi lửa chính `bone28`; ba ống cứng theo xương ống của họ (`bone40`, `bone39`, `bone43`: bẻ và giật theo chiêu cuối); thân
  tra trọng số theo lưới bụng `P_duzi`; miệng ống / miệng núi lửa / chỗ tụ cầu lửa đặt theo toạ độ trên concept (`MIENG_ONG`, `MIENG`).
- Ba lỗi thấy khi soi, đã sửa:
  1. CHÂN: bản đầu dùng ba xương + IK gập gối của hổ con → thân rạp (cast, skill) thì trụ đá ngắn gập nhàu, lòi gai. Nay mỗi chân là MỘT mảnh
     cứng trên xương riêng `<slot>_p` (con của `move`): đáy đặt ở chỗ xương bàn chân của họ, nghiêng ≤ 28° về phía hông, hông xa hơn chiều dài
     trụ thì dãn dọc, thân hạ thì đỉnh trụ chui vào thân; `walk` đi theo vòng bước tự viết (`nui_lua_chibi.ik`).
  2. CẰM HAI VIỀN: ảnh đầu còn giữ viền ngoài của hàm → hàm hé là lộ nét thứ hai. Nay ảnh đầu bỏ hàm và viền ngoài của nó, giữ nét môi, tô
     khoang miệng (phía trước sâu hết chiều cao hàm, phía khoé nông).
  3. KHỚP HÀM: bám thẳng `bone8` thì hàm quay quanh gốc đầu, mũi hàm lùi lại lộ vệt cam dưới cằm. Nay hàm có xương riêng `ham_p` ở khớp hàm
     (`HAM_KHOP`), góc = 0,85 × góc `bone8` (chỉ chiều há). Nhớ: `Pose.t[xương] = [dx, dy, dgóc, sx, sy]` (góc ở chỉ số 2).
- Đã soi khung tĩnh: idle, walk, attack, cast, skill, die, appear. Ảnh động 8 clip (`rig/dong/`, `NL_DANG=chibi … _xem_dong.py`) đã lên artifact.
- CHƯA: xem ở tốc độ thật; vào game (cả hai dạng); VFX; tên. Chờ người dùng xem dạng 1.
- **Sửa theo người dùng (2026-11-14 ~20:20, xem ảnh động trên artifact): "Animation die lỗi chân, xuất hiện 2 chân trước bị bẻ ra trước hơi nhiều"**
  (hiểu là nói dạng 1; chưa hỏi lại dạng lớn). Nguyên nhân: trụ chân luôn đứng theo xương bàn chân của họ; lúc thân đổ nghiêng (die) hay đang
  rơi (appear) thì chân rời khỏi thân hoặc choãi theo chân dài của họ. Sửa trong `nui_lua_chibi.ik`: (1) tham số `theo` (0..1): chân đi theo
  thân như gắn cứng vào xương thân (đáy trụ + góc theo `bone3` / `bone5`); `die`: `theo` lên 1 trong 0,18 s; `appear`: 1 lúc đang rơi, về 0
  quanh lúc dộng đất; (2) clip khác: đáy trụ không lệch ngang quá 0,3 chiều dài trụ so với chỗ nghỉ dưới hông, nghiêng tối đa 20°.
  Soi lại khung tĩnh die (10 khung), appear (10), skill (12): chân bám thân. Ảnh động 8 clip xuất lại, đã cập nhật artifact.

## 11. Vào game + dạng 2 (2026-11-15 ~01:00–01:25)

- Người dùng: "**cho vào game đi**", rồi giữa lượt: "**con này cần có dạng 2 nữa, làm dạng 2 đi**". Dòng có BA dạng (khớp ba dạng cũ của
  `lan_hoa`, golden roster không đổi): 1 con non chibi (`nui_lua_non`), 2 thiếu niên (`nui_lua_2`, đang làm), 3 boss hai sừng (`nui_lua_1`).
- **Dữ liệu** `quai/doi_nui_lua.py` (dùng lại `doi_phap_lua.py`): suất `lan_hoa` giữ id, thẻ, chỉ số. Tên Claude đặt (người dùng chưa đặt,
  đã hỏi ba lần): tướng **Hỏa Sơn Long** ("Khủng long núi lửa hai sừng"), dạng **Hỏa Sơn Nhi / Hỏa Sơn Thú / Hỏa Sơn Long**; thẻ Hỏa Cầu
  Phún Viêm (flame), Vạn Viêm Truy Kích (sun), Lõi Dung Nham (torch), thẻ boss Giáp Bazan (shield). Dạng 2 TẠM trỏ `nui_lua_1` cỡ 0,86; có rig
  thì `doi_nui_lua.py chep_2` rồi `dang_2`. Cỡ: 0,85 / 0,86 / 0,92 (1,05 thì dạng lớn tràn mép phải sân). `chep` → `Resources/nui_lua_1`,
  `Resources/nui_lua_non`. Thư mục `lan_hoa_1..3` cũ không đụng.
- **Đòn thường lao thật**: `f_attack` thêm quãng lao trên xương `move` (lùi 0,07 → phóng tới 0,60 chiều cao ở khung húc, giữ 0,14 s, về); sân
  nắn đỉnh lao tới 72 % quãng tới đối thủ (`AolaSticker.Lunge`; trước đó chỉ nhún 35 %). Hai rig đã xuất lại.
- **VFX** `Assets/01 Script/Game/Battle/HatNuiLua.cs` (từ bản nháp + bảng theo dạng: dạng 1 dùng `NuiOngP1 / NuiOngG1 / NuiOngDung1`, 8 phát,
  nổ × 0,78; đo bằng `NL_DANG=chibi … _do_hat.py`). Nối: `HatNuoc.PlayNuoc` (`n_nui_huc`, `n_nui_cau`, `n_nui_cau1`, `n_nui_ten`,
  `n_nui_ten1`), `StageView.FireFx` (`n_nui_cau`, `n_nui_ten`), `HoaUltDang` (`n_nui_ten1`, `n_nui_ten`, `n_nui_ten`), `HoaAtk`
  (`n_nui_huc`), `HatVoi.AtkLao`, `HatLua.Themes["lan_hoa"]` về bảng "lua", `HoaFxTour` (menu "riêng Hỏa Sơn Long", "riêng Hỏa Sơn Nhi (dạng
  1)"). Chiêu mana chưa chọn theo dạng (`FireMana` không nhận dạng): dạng 1 phụt khói ở chỗ ống của dạng lớn; `n_nui_cau1` có sẵn nhưng chưa nối.
- **Unity**: biên dịch không lỗi; "Nhập dữ liệu" (88 tướng), "Gắn dạng .atomik" (lệnh MCP rớt kết nối giữa chừng nhưng chạy xong: có
  `nui_lua_1.asset`, `nui_lua_non.asset`, `lan_hoa.prefab` đổi); EditMode 106 / 107 (lỗi cũ `PrefabOnlyTests` ở `UI/Kit`). Lúc bắt đầu Unity
  đang Play (đã tự thoát khi biên dịch); tôi bật Play để chạy tour rồi thoát.
- **Soi trong trận** (tour, ảnh `Temp/PokiShots/hoa_fx`, cả dạng 3 và dạng 1): húc lao tới đối thủ + chớp toé; cầu lửa tụ ở mồm, bay, nổ; chiêu
  cuối gồng, dộng (vòng bụi), bẻ ống, đạn vòng cung trúng đối thủ. Chưa soi: phía địch (lật), ô xem trong hộp chi tiết tướng, cỡ mới 0,92, trên
  điện thoại. Đuôi đạn (lưỡi lửa + khói) trông như chuỗi hạt nâu: có thể bớt khói nếu người dùng chê.
- **Dạng 2**: `nui_lua_2.py` (tỉ lệ: đầu × 1,22, cổ ngẩng 26°, chân × 0,9, sáu ống 09 10 02 14 13 03 × 0,82, sừng × 0,6; `NL_MA=nui_lua_2`) →
  `inbox/nui_lua_2/mau/bo_cuc_chibi.png` → hai concept `tai_ve/L1_A.png` (nghiêng về dạng lớn, ĐỀ XUẤT) và `L1_B.png` (nghiêng về dạng 1), đã
  lên artifact. CHỜ người dùng chọn. Sau đó: mảnh + lắp như dạng 1 (tổng quát hoá `nui_lua_chibi.py` theo `NL_MA`), `chep_2`, `dang_2`, bảng
  đo cho `HatNuiLua.cs` (`dang == 2`).

## 12. Dạng 2 (Hỏa Sơn Thú): mảnh + rig + chép vào game (2026-11-15 01:35–02:25)

- Người dùng: "tôi ở nhà rồi không cần up lên artifact nữa" (từ đây chỉ đưa đường dẫn cục bộ), rồi "**Làm theo A**" → `inbox/nui_lua_2/tai_ve/L1_duyet.png`.
- Mảnh: `nui_lua_2.py manh_prompt` → `gui_gpt/nui_lua_2/luot_1_manh_<DAU|THAN|CHAN|NUI|ONG1|ONG2>.txt` → `tai_ve/C_*.png` (sáu tờ, đạt ngay);
  `NL_MA=nui_lua_2 py -3 -I nui_lua_chibi.py cat` → `manh_chibi/` 13 mảnh, ghép lại lệch concept 5,1 % điểm.
- `nui_lua_chibi.py` nay dùng chung cho hai dạng theo `NL_MA` (bảng `THU_TU`, `MIENG_ONG`, `TO_ONG`, `KHOI`, `BAN`, `ONG_CHA`, `HAM_KHOP`…);
  `nui_lua_rig.py` chế độ chibi đọc tỉ lệ từ `inbox/<mã>/mau/bo_cuc_chibi.json` và bảng từ `nui_lua_chibi`.
- Rig: `NL_MA=nui_lua_2 NL_DANG=chibi py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/nui_lua_rig.py` → `inbox/nui_lua_2/rig/`
  (`nui_lua_2`): 104 xương, 24 slot, 1295 đỉnh, `.atomik` 292 KB, cao 920; chiêu cuối 12 phát (cc 10 14 09 13 02 × 2), dài 3,18 s.
- Sửa khi soi (áp cho cả dạng 1):
  1. Chân lún dưới đất lúc dộng → đáy trụ không xuống dưới mặt đất quá 6 đơn vị.
  2. THÁP ỐNG VĂNG KHỎI THÂN ở die / skill: bám thẳng xương ống của họ thì quay quanh gốc xương đó (ở xa). Nay mỗi tháp có xương riêng
     `ong_p_<k>` ở CHÂN tháp, con của khúc thân nó đứng lên (`ONG_CHA`: tháp sau → `bone3`/`bone4`, tháp trước → `bone6`), góc và co giãn chép
     từ xương ống của họ ở từng khung; xương miệng ống `ong_<k>` là con của `ong_p_<k>`.
- Đã soi khung tĩnh dạng 2: idle, walk, attack, cast, skill, hit, die, appear. Dạng 1 dựng lại (97 xương) và soi lại die, skill.
- Vào game (file): `doi_nui_lua.py chep` (dạng 1 bản mới), `chep_2` → `Resources/nui_lua_2`, `dang_2` (heroes.json: dạng 2 → `nui_lua_2`, cỡ 0,86).
  `HatNuiLua.cs`: bảng dạng 2 (`NuiOngP2/G2/Dung2`), đo lại dạng 1; `HatNuoc`: `n_nui_ten2`, `n_nui_cau2`; `StageView.HoaUltDang`: `n_nui_ten1`,
  `n_nui_ten2`, `n_nui_ten`; `HoaFxTour`: menu "riêng Hỏa Sơn Thú (dạng 2)" (sao = 3; `formStars` = 3, 5). Unity biên dịch không lỗi.
- **CÒN DỞ (02:25)**: Unity đang ở Play (cảnh Heroes, có vẻ người dùng đang xem) nên CHƯA chạy "PokiClash/Nhập dữ liệu" và "PokiClash/Tướng/Gắn
  dạng .atomik vào prefab tướng" cho dạng 2 + bản dạng 1 mới; chưa chạy test, chưa chạy tour dạng 2. Chờ người dùng dừng Play.
