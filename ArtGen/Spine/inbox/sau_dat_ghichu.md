# Sâu đất khổng lồ (`sau_dat`): tướng 7 đảo Thổ

Bắt đầu 2026-11-17 (máy ổ C, kho `D:\Ripper\SwordxStaff`). Con gốc của rig: **`monster_3643`** (rồng rắn trắng trồi lên giữa kén năm cánh
tím, mười tua đen đầu thoi trên đầu, tua trắng cong quanh thân, bốn tấm vỏ đen phía trước, đế pha lê lam; game tham khảo), **do người dùng
chỉ** (ảnh chụp trang xem, clip `skill_03`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng
công khai. Hình là của mình. Suất 7 đảo Thổ = ải 40 "Ruộng Bậc Thang" (`IslandGen.cs` Plan Tho), id game hiện là **`rua_nui`** (Rùa Núi).
Mã làm việc `sau_dat`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-17)

- "làm tướng thứ 7 đảo thổ; concept **sâu đất khổng lồ như ảnh**, tham khảo **baron trong lol** và **sâu cát trong dune**".
- "animation **xuất hiện** làm nó **chui từ dưới đất lên**".
- "các chiêu còn lại bạn **tự sáng tạo dựa theo con gốc**, miễn là **độc đáo, lạ, epic và đẹp**".
- "**gen qua magnific**"; "các ảnh bộ phận khi gen **không được quá 100 credit**, nếu quá hỏi tôi".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3643/`: `info.json`, `att_goc.json`, `att_idle0.json`, `khung/` tờ khung 11 clip, `mo/idle0_*.jpg`
tờ mổ từng part)

219 xương, 61 slot (60 hình bật ở idle 0), 11 clip, 12 193 khoá. Hầu hết hình là lưới có trọng số trên chuỗi xương.

Cây xương: `root → bone2 → bone` (gốc cả con, 14 nhánh) → `bone6 > 7 > 8 > 9 > 10 > 11` (THÂN / CỔ, chuỗi sáu xương) → `bone16` (ĐẦU) →
`bone12` (sọ trên `P_shange`) + `bone13` (HÀM DƯỚI `P_xiae_01/02`) + `bone14/15/17` (mắt, gai mõm) + `bone18..22` (mào `P_jiao_01..04`, sừng
`P_jiao_08`) + `bone85` (ba tua sau gáy `P_hounao_01..03`) + `bone84` (MƯỜI TUA ĐẦU `A_chuxu_01..010`, mỗi tua chuỗi 5–9 xương). Từ thân:
`bone23..29` (tua `P_chuxu_11`), `bone30..37` (tua `P_chuxu_09`). Từ `bone`: chuỗi `bone38..62`, `bone93..118` (tua trắng quanh chân),
`bone131` (9 nhánh: năm cánh tím `P_shitou_05..09` + bốn tấm vỏ đen `P_shitou_01..04`, mỗi tấm chuỗi 3–4 xương), `bone3/4/5` (đế pha lê
`P_dizuo_01..03`, cứng), `bone153/154` (hai móng đen sát đất `P_xiazhi_01/02`, cứng).

Nhóm part (thứ tự vẽ từ sau ra trước): móng đất `P_xiazhi` → cánh tím `P_shitou_05..09` → tua `P_chuxu_09..11` → vỏ đen sau `P_shitou_04` →
tua gáy `P_hounao` → mười tua đầu `A_chuxu` → thân `P_bozi_01..10` (khúc vòng đốt bụng) → mào, sọ, hàm, mắt → tua trước `P_chuxu_01..08` +
vỏ đen trước `P_shitou_01..03` → đế pha lê `P_dizuo`.

Clip gốc: `idle_01` / `run_01` / `XXXX` 2 s (đứng chỗ, tua đầu đung đưa, kén thở; con này KHÔNG đi), `skill_01` 1,23 s (ngửa đầu ra sau rồi
lao đầu đớp xuống phía trước 0,55, kén xoè), `skill_02` 1,67 s (vươn thân cao 0,19–0,93, giáng đầu xuống 1,11, gầm), `skill_03` 2 s (thụt
thấp vào kén 0,22–0,44, vươn thẳng cổ ngửa đầu gầm 0,67–1,56, cánh mở rộng), `block_01`, `hit_01/02`, `stun_01`, `die_01` 1,33 s (đầu gục,
cánh xoè bẹt ra hai bên).

## 3. Concept lượt 1 (Claude đề xuất ba hướng, chờ người dùng chọn)

Script `sau_dat.py` (ca_con, slot, concept, so_goc; dùng lại `tho5.py`). Gói `gui_gpt/sau_dat_1/luot_1_concept_<A|B|C>.txt` + `HUONG_DAN.md`.
Ảnh mẫu: 1 = con gốc (chỉ lấy dáng, bố cục, chỗ mảnh to), 2 = rồng giáp sa thạch, 3 = vượn núi (tướng Thổ đã duyệt, lấy nét). Gen trực tiếp
bằng công cụ Magnific trong phiên (GPT 2.6, 1k high, 3:2, 95 credit / ảnh, `simulate_cost` xác nhận), ~1 phút mỗi ảnh, ảnh về 1536 × 1024
→ `inbox/sau_dat_1/tai_ve/L1_<k>.png`. Trang so: `inbox/sau_dat_xem_concept.html`.

| Hướng | Nội dung | IoU hình bóng |
|---|---|---|
| A sâu cát (Dune) | đầu húc ba vòng giáp sa thạch, MIỆNG TRÒN nhiều vòng răng kem, lòng đỏ đất nung, mắt hổ phách; thân vòng đốt vàng cát bụng kem; mào ba tấm quạt; mười râu roi nâu đầu ngạnh hổ phách; phiến sau lưng là ĐÁ PHÂN TẦNG; tảng đất nâu khe hổ phách; tua hồng như giun con; gò cát + hổ phách | 0,675 |
| B Baron đất | đầu mai NÂU TÍM ĐẤT, vương miện bốn sừng kem, hàm dưới HAI NGÀ lớn; thân đỏ đất nung bụng kem; gai roi nâu tím đầu móc; phiến sau lưng là NỬA HỐC ĐÁ lòng pha lê hổ phách; tấm bazan; tua gai xương kem | 0,665 |
| C giun đất giáp đá | thân thịt hồng có ĐAI YÊN, vảy đá phiến; đầu MÕM XẺNG đá phiến; mào ba vảy ngói; râu đất son có đốt đầu hạt hổ phách; phiến là tảng đất vỡ nhiều lớp | 0,645 |

Claude soi: cả ba đúng dáng, đầu bên phải chĩa phải hơi xuống, một mắt, mọi mảnh dính thân, nằm đúng khung con gốc (IoU ngang các concept Thổ
đã duyệt lượt C/D). Lưu ý khi đưa duyệt: A đầu to và thấp hơn đầu rig một chút, miệng tròn quay về phía người xem; B màu nâu tím ngoài bảng
màu đảo Thổ (gợi Baron và con gốc); C miệng hơi giống cười, đầu giống thằn lằn hơn sâu.

**Người dùng chọn A (2026-11-17)** → `tai_ve/L1_duyet.png` (sâu cát: đầu húc ba vòng giáp sa thạch, miệng tròn vòng răng, thân vòng đốt vàng cát).

## 4. Đề xuất animation (Claude, 2026-11-17; người dùng đã giao tự sáng tạo)

| Clip | Dựa trên | Diễn | VFX (lớp riêng, không vẽ vào rig) |
|---|---|---|---|
| Vào sân ~2,2 s | die_01 chạy ngược + skill_03 | đất rung, đế đá vụn hiện trước; năm phiến đâm lên từng phiến (từ nằm bẹt dựng dậy), tảng trước trồi; đầu sâu phá đất vọt thẳng lên (cổ vươn hết cỡ như skill_03 0,67 s), đá rơi khỏi đầu, há miệng gầm, mười râu bung xoè; hạ về dáng idle | vết nứt, bụi đất phụt, dăm đá nảy, đá rơi từ đầu |
| Idle 2 s | idle_01 | tua đung đưa như gốc + trò riêng: há miệng "nếm" không khí, râu dò như râu côn trùng, phiến thở lệch pha | vài hạt cát rơi khỏi thân |
| Đánh thường "Đớp nghiền" | skill_01 | ngửa đầu ra sau, lao đớp xuống phía trước | vết cắn vòng răng, dăm đá |
| Chiêu mana "Gai ngầm" (Baron) | skill_02 | vươn cao, quật mười râu cắm xuống đất phía trước | dưới chân địch trồi ba gai đá đầu ngạnh hất tung địch rồi lún lại |
| Chiêu cuối "Miệng sa mạc" (Dune) | skill_03 + xương far | thụt sâu vào đất tới khi mất hẳn, phiến khép lại; gò đất chạy ngầm tới địch; CẢ ĐẦU VÀ THÂN trồi lên ngay dưới chân địch (code lái xương far), há miệng vòng răng đớp khép, rung màn hình; lặn xuống, trồi lại chỗ cũ | gò đất chạy, cột cát phụt, vòng nứt, rung |
| Trúng đòn / choáng / đỡ | hit_01/02, stun_01, block_01 | giữ của họ | |
| Chết | die_01 | đầu gục, thân chìm dần xuống đất, phiến đổ sập vào | bụi, đá lăn |
| Đi | (họ không có) | lặn xuống, gò đất chạy, trồi lên; hoặc dùng idle nếu game không cần | |

## 5. Mảnh (2026-11-17; mọi ảnh gen qua Magnific GPT 2.6 1k high, 95 credit / ảnh, mỗi tờ đạt lượt đầu)

- **Bố cục `L2_bocuc` (bỏ)**: GPT vẽ lại gần y concept, không theo bố cục part của rig (IoU 0,677 như concept): không dùng.
- **Khung part** (`sau_dat_part.py`, tờ hướng dẫn = hình bóng kín part gốc × z, tô theo thiết kế): R mười râu (vẽ THẲNG đứng, ngạnh hổ
  phách ở mũi thoi trên cùng), T mười bốn tua giun, S1 năm phiến phân tầng, S2 bốn tảng + ba cụm đế + hai phiến dẹt sát đất (`P_xiazhi`
  của họ là rễ chẻ nhánh: đổi thành bao lồi, phiến đá dẹt). IoU ≥ 0,9 trừ `A_chuxu_06/07` 0,86 / 0,84 (dải mảnh), `P_shitou_07` 0,89.
- **Liền** cổ + thân (`P_bozi_01..10`, gồm hai vòng giáp sau đầu `01/04`): một tờ hình bóng hợp (sườn vàng cát, cột bụng kem, cổ áo sa
  thạch); vòng đốt để GPT vẽ (vạch bằng mã ra hình nêm ở chỗ thân cong: bỏ). Nướng vào khung từng part qua lưới, KHÔNG cắt theo hình bóng
  part gốc (mép xẻ răng cưa của họ làm lộ khe khi các khúc trượt).
- **Mảnh cứng đầu** (`sau_dat_cung.py`, "đúng chỗ" trên concept, bốn lượt K1–K4): `dau`→`P_shange`, `ham`→`P_xiae_01`, `mieng`→`P_xiae_02`,
  `may` (gờ mày)→`P_jiao_08`, `nanh1/2`→`P_jiao_07/09` (bám HÀM), `maoA/B/C`→`P_jiao_03/02/01`, `vong` (vòng giáp thứ hai)→`P_jiao_04`;
  mắt `P_jiao_05` cắt thẳng từ concept (không bị che). Ngà trái GPT vẽ chạm đáy vòng giáp: tách theo vòng tròn quanh ngà (`TACH`).
  **`P_jiao_06` (gai nhỏ trên mõm của họ) tạm ẩn**: concept không có.

## 6. Rig + clip (`sau_dat_rig.py` → `inbox/sau_dat_1/rig/`; `SD_GOC=1`: da gốc → `rig_goc/`)

Đủ 219 xương của họ + `move`, `fly_sau` (con của root, trùng chỗ `bone` tĩnh; CHA MỚI của chuỗi thân `bone6..`: cả con sâu lặn / trồi /
chạy tới đối thủ, game co quãng như xương `fly*`), `far` (1850, 450), `mieng` (con của sọ `bone12`). Part khung + thân: nguyên lưới của họ;
mảnh cứng: lưới dày, đỉnh bám như part gốc nguồn. Thứ tự vẽ cụm đầu: mào → vòng giáp → lòng miệng → hàm → ngà → đầu → gờ mày → mắt (chèn
ngay sau khúc thân cuối). **Lót thân** `than_lot`: cả ảnh thân liền một lưới SAU mọi khúc cổ (đỉnh bám như lưới hợp các part thân gốc), che
khe chữ V dưới hàm lúc vươn cao (con gốc che bằng hàm, lưỡi mào của họ). **Mặt nạ đất** `cat_dat` (chữ nhật trên y = −16, mọi slot): phần
dưới đất bị giấu khi chui lên / lặn.

| clip | dài | nguồn | diễn | sự kiện |
|---|---|---|---|---|
| appear | 2,10 | skill_03 | đế đá trồi, năm phiến đâm lên lệch nhịp (co giãn gốc chuỗi), bốn tảng, tua mọc; sâu phá đất vọt lên (fly_sau −1350 → 0, vượt 7 %), ngửa đầu gầm há hàm, rung | nut 0,02 · troi 0,50 · gam 1,08 |
| idle | 2,00 | idle_01 | như họ + há miệng "nếm" không khí hai nhịp 1,05–1,75 | |
| walk | 2,00 | run_01 | (họ không đi; run_01 = idle) | |
| attack | 1,30 | skill_01 | ngửa ra sau, lao đớp xuống, rung | lao 0,36 · trung 0,56 |
| cast | 1,85 | skill_02 | vươn cao há hàm, GIÁNG đầu xuống đất, rung | vuon 0,20 · nen 1,06 · gai 1,14 · trung 1,20 |
| skill | 2,75 | skill_03 + skill_02 | thụt, LẶN (0,30–0,62), chạy ngầm tới đối thủ (đến 1,02), TRỒI dưới chân đối thủ há to, ĐỚP 1,34, lặn lại (1,62–1,90), trồi về chỗ cũ (1,96–2,30); tổ phiến ở nhà đứng trống | lan 0,30 · ngam 0,62 · troi 1,02 · can / trung 1,34 · lan 1,62 · ve 1,96 |
| hit | 0,50 | hit_01 | | |
| die | 1,78 | die_01 | gục, thân chìm xuống đất, phiến xoè bẹt, mờ | |

Bản xuất 2026-11-17: 223 xương, 61 slot, 60 hình, 2 742 đỉnh, 8 clip, 16 sự kiện, `.atomik` 693 KB (trần 1 MB); mọi clip về khung 0 idle
0,00 px, appear khung đầu trống, die khung cuối trống; `thu_xem` chạy đủ 8 nút. Góc nhảy lớn nhất ở 60 khung/giây (runtime thật): idle 13°,
die 29°, hit 37°, appear 48°, attack 54°, cast 57° (hàm lúc giáng), skill 83° (ngọn tua gáy lúc trồi vọt); không có cú quay ngược.
Còn biết: lúc vươn cao hết cỡ (cast 0,5–0,9 s) vạch vòng đốt lệch nhau vài px ở chỗ hai khúc cổ gặp nhau (giới hạn của cách nướng liền vào
part); chiều cao game 1 142 (không tính râu). Chưa làm: VFX (gai đá, gò đất chạy ngầm, cột cát, bụi, vết cắn), vào game (heroes.json, thay
suất `rua_nui`?), tên, số dạng.

### Sửa sau lượt xem đầu (người dùng 2026-11-17: "rig đầu ghép lỗi bị hở rồi, phần hàm dưới cũng lệch, 2 nanh dưới nhìn như lỗi layer,
### phần khoang miệng trong cũng nên rig xương stretch theo hàm há mồm")

- **Hở đầu, hàm lệch**: mảnh cứng đặt theo toạ độ concept, mà concept vẽ trên KHUNG 0 IDLE (goc_ca_con dựng từ att_idle0); tôi gắn chúng
  như thể ở DÁNG GỐC. Ở rig này hai dáng lệch 30–90 đơn vị ở các part đầu (sọ 45, hàm 33, mào 50–60), mỗi xương một kiểu → mỗi mảnh trượt
  một kiểu. Sửa: `gan_theo_goc(..., att_tu=att_idle0)`: trọng tâm β tính trên lưới part gốc ở khung 0 idle, điểm gắn bằng đỉnh dáng gốc;
  khoảng lệch ngoài lưới đổi qua afin của tam giác gần nhất.
- **Ngà**: mảnh ngà trái tách hỏng (vòng tròn cắt xén mũi ngà, dính mẩu vòng giáp) → tách theo ĐƯỜNG MỰC chung (`tach_muc`: bỏ mực thì
  ngà, hốc ngà, vòng giáp là vùng màu rời; mực chia cho bên gần hơn) + gọt gai mực. Ngà vẽ TRƯỚC đầu và hàm (hốc ngà vàng đất là thiết kế
  concept); để sau hàm thì hàm che mất cả ngà.
- **Lòng miệng co giãn**: `mieng_gian`: nửa trên bám sọ bone12, nửa dưới bám hàm bone13, hoà dần theo khoảng cách có dấu tới đường môi
  (qua khớp hàm và tâm miệng) → há miệng thì lòng miệng giãn, không trượt nguyên khối.
- Bản xuất: 223 xương, 61 slot, 2 727 đỉnh, `.atomik` 693 KB; mọi clip nối idle 0,00 px.

### Sửa lần hai (người dùng 2026-11-17: "vẫn lỗi, gửi lại ảnh concept lên đây", rồi "bạn dùng cách nào cũng được, gen thêm cũng được")

- Đo: mảnh cứng đã nằm đúng chỗ cắt (lệch < 1 px ở khung 0 idle) nhưng CHÍNH các mảnh GPT K1–K4 vẽ lệch concept: một vòng giáp chữ C mảnh
  thay hai vòng xếp sát (khe sau đầu, râu lộ qua), vành đầu thành vành khăn hẹp mất má, ngà + hốc ngà dịch trái ~60 px. Trang so cùng
  khung: `inbox/sau_dat_xem_so.html` (`sau_dat_so.py`: concept | rig | chồng).
- Cách lai (`sau_dat_dau.py`): cụm đầu không bị gì che trên concept → CẮT THẲNG theo mảng kín giữa nét mực (`mau/_vung_dau.png`): `dau` =
  hai vòng giáp + vành đầu + má + gờ mày + mắt + răng trên (lòng miệng khoét), `ham` = thân hàm + răng dưới, `nanh1/2` = hai ngà (trước
  đầu, cùng xương hàm). Chỗ bị che: đuôi hàm dưới má lấy mảnh hàm K2; má dưới chỗ ngà che tô màu má. Ẩn `P_jiao_04/08/05` (đã gộp vào đầu).
  Mảnh K cũ giữ ở `manh/cung/<tên>_k.png`. Không tốn credit.
- Bản xuất: 223 xương, 58 slot, 2 581 đỉnh, `.atomik` 680 KB; mọi clip nối idle 0,00 px.

### Sửa lần ba (người dùng 2026-11-17, ảnh lúc ngửa đầu gầm: "đoạn há to mồm này lỗi, rig thêm xương phần hàm trên để nó nối với hàm dưới")

- Lỗi: hàm dưới xoay ra xa còn vành miệng trên (mảnh đầu) đứng yên; góc miệng phía trước không có gì nối hai hàm → lòng miệng kéo xiên,
  lòi ra ngoài đầu. Thêm nữa: clip gốc đã mở hàm tới 38° (skill_02), tôi còn cộng 16–26° → gần 60°.
- `vanh_mem`: quanh nửa TRƯỚC miệng, đầu (bone12), hàm (bone13), lòng miệng dùng CHUNG một trường trọng số: trên đường môi bám sọ, dưới
  bám hàm, góc miệng nửa nọ nửa kia (chuyển trong ±0,55 R0), mờ dần ra ngoài bán kính 1,15–1,9 R0 và về phía khớp hàm (R0 ≈ 105 đơn vị).
  Há thì vành tròn kéo giãn, góc miệng vẫn liền. Phần há tự cộng giảm còn 4–12°.
- Soi runtime thật: chiêu mana 0,6–1,3 s, vào sân 0,74–1,3 s (gầm), đớp: miệng là vòng tròn liền, lòng miệng gọn trong vành.
- Bản xuất: `.atomik` 681 KB; mọi clip nối idle 0,00 px.

### Sửa lần bốn (người dùng 2026-11-17, ảnh cận dưới ngà lúc ngửa đầu há to: "đoạn này vẫn bị hở")

- Khe hình nêm ở góc miệng PHÍA SAU (má, gần khớp hàm): `vanh_mem` chỉ phủ nửa trước miệng. Mở rộng: chặn phía sau từ −2,0 R0 (hết ở
  −1,2 R0), bán kính 1,45–2,4 R0 → má quanh khớp hàm cũng giãn theo hàm, góc sau liền.
- Mảng vàng đất lọt trong lòng miệng gần ngà trái: phần tô màu má lấp chỗ ngà che (sau_dat_dau.py) lấn vào lòng miệng → chỉ tô điểm gần
  vùng má 234 hơn lòng miệng / răng.
- Soi trên nền hồng sẫm (lộ mọi khe) ở vào sân 0,9 / 1,05 / 1,2, chiêu mana 0,74 / 0,88, chiêu cuối 1,2: không còn khe; runtime thật khớp.

### Đánh thường và chiêu cuối bản epic (người dùng 2026-11-17: "chiêu mana ổn, chiêu đánh thường và chiêu cuối làm epic hơn chút nữa")

| clip | dài | diễn | sự kiện |
|---|---|---|---|
| attack "Đớp nghiền" | 1,52 | ngả ra sau lấy đà (fly_sau +7°, lùi 35), há rộng −16°, râu xoè ngược −18°, gồng run 0,42–0,54; PHÓNG 0,54–0,65 (chúi −9°, tới 50); ĐỚP sập hàm +5°, nén thân, rung 9; LẮC NGHIẾN hai nhịp (đầu ±11°, cổ ±5°, tắt dần) tới 1,00; bật về có vượt | lao 0,54 · trung 0,65 · nghien 0,75 |
| skill "Miệng sa mạc" | 3,45 | ngửa cổ GẦM (há −10°, rung); LẶN CẮM ĐẦU chéo xuống (dáng giáng, fly_sau −35°, trượt tới 140) 0,50–0,80; chạy ngầm, đổi dáng dần sang thế ngóc đầu; PHÁ ĐẤT dưới chân đối thủ 1,25 (vươn dài sx 0,93 / sy 1,12, há ngửa −16°), TREO run run 1,42–1,55; GIÁNG ĐẦU NGOẠM 1,62 (hàm sập, nén, rung 12); LẮC NGHIẾN (đầu ±12°) tới 1,98; lặn về (hoà dáng); trồi ở nhà 2,35–2,70, GẦM lần hai | gam 0,32 · lan 0,50 · ngam 0,80 · troi 1,25 · can / trung 1,62 · nghien 1,72 · lan 1,98 · ve 2,35 · gam 2,72 |

- IMPACT: attack (khựng 0,13 s, rung 0,85), skill (0,30 s, rung 1,6, chớp màn).
- **Khoá giật của clip gốc**: `skill_03` khung 17 → 20 đầu quay ngược rồi bật 121° trong một khung (họ che bằng hiệu ứng) → `LAM_MUOT`
  nội suy đều. skill_01 / skill_02 cổ quay ~50°/khung trong 2–3 khung là cú đánh nhanh thật: giữ, nhưng đừng nén quá 2 lần (cú phóng
  0,08 s làm cổ quay 118°/khung → giãn 0,11 s). Đổi giữa hai clip nguồn thì HOÀ dáng (`pha`) trong lúc ẩn, đừng nhảy dáng ở mốc.
- Bước xoay lớn nhất mỗi khung 60 hình/giây (đầu, cổ, mào, hàm): vào sân 34°, đánh thường 63° (khung đớp), chiêu mana 78° (hàm lúc
  giáng, giữ như bản đã duyệt), chiêu cuối 54° (khung ngoạm). `.atomik` 700 KB; mọi clip nối idle 0,00 px; thu_xem đủ 8 nút.

## 7. Vào game (người dùng 2026-11-17: "ok cho vào game, tạo thêm fx nếu cần rồi làm dạng 1 của tướng này")

- Suất `rua_nui` (giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ; không đổi bản lưu): `quai/doi_sau_dat.py` (heroes.json, cards.json),
  `doi_sau_dat.py chep` → `Assets/03 Art/Heroes/Resources/sau_dat_1/`. Tên: Rùa Núi → **Sa Trùng** "Sâu cát khổng lồ", dòng "Dòng Sa
  Trùng", dạng 1 "Sa Trùng Nhi"; thẻ Gai Ngầm (crack), Miệng Sa Mạc (fang), Giáp Vòng Đốt (shield). Bỏ hẳn `rua_nui_1/2` cũ.
- Hiệu ứng (`HatTho.cs`, mục cuối; mã `n_trung_*` trong `HatNuoc.cs`; `StageView.ThoFx` / `ThoAtk`; `HatVoi.AtkLao` có `n_trung_dop`):
  `NTrungDop` (đánh thường: bụi phụt lúc lao, cát văng lúc đớp, hai nhịp nghiến), `NTrungGai` (chiêu mana: gò đất chạy ngầm + vết
  nứt, gai sa thạch đầu hổ phách trồi dưới chân đối thủ), `NTrungMieng` (chiêu cuối: gầm, lặn, gò chạy, phá đất, ngoạm, nghiến,
  lặn về, trồi, gầm lần hai). Mốc lấy đúng giây rig nhân `k = lead / hitTime`.
- Theo đối thủ: `fly_sau` / `fly_dat` lái bằng `AolaActor.FarAtomik`; xương `far` ở 0,45 H (StageView nhắm thân giữa đối thủ).
  Lớp cắt đất `cat_dat` bám `fly_dat` nên mép đất cắt đúng ở chân đối thủ khi trồi lên.
- Kiểm: tour "Đảo Thổ: riêng Sa Trùng (sao 6)" và "Sa Trùng ở PHE ĐỊCH" (ThoFxTour.cs) chạy đúng hai phía; golden không đổi;
  110/110 test; biên dịch 0 lỗi.
- Còn nhỏ: đòn đánh thường kéo cả ổ đất theo tướng (hành vi lao của game); vết nứt `ToNut` vẽ thành vạch chéo dài.

## 8. Dạng 1 "Sa Trùng Nhi" (`sau_dat_non`; người dùng: "bạn nên tự nghĩ 1 mini version, cùng rig")

- Cùng xương, lưới, clip dạng 2: `SD_DANG=non py -3 -I sau_dat_rig.py` (→ `inbox/sau_dat_non/rig/sau_dat_non.atomik`).
  Tỉ lệ `TI_NON` (nhân ở xương gốc chuỗi): thân bone6 0,82; đầu bone16 1,12; mào, râu, phiến, cục đất, giun rễ 0,6–0,8.
  Ẩn `BO_NON`: ba phiến đá lớn ngoài cùng và hai khối đá đáy (`A_chuxu_07..010`, `P_shitou_06/07`).
- Bố cục: `sau_dat_non.py bocuc` → `mau/bocuc.png` (khung 0 idle, da dạng 2; `bocuc.json` s 0,6586 cx −1,554 cy 597,67).
- Concept lượt 1 (`sau_dat_non.py concept`; Magnific GPT 2.6 1k high, 95 credit / ảnh; ảnh mẫu bố cục + concept dạng 2):
  - **A** giữ màu dạng 2 nhạt hơn, vòng giáp đầu tròn mềm, mắt hổ phách to, răng thưa nhỏ, hai ngà tù → trùng hình bóng bố cục
    **0,964** (chỉ hụt ở mõm trước).
  - **B** thân hồng giun non, đầu kem, răng sữa vòng tròn, ngà gần như không có, râu đầu hạt → 0,920, **mất 2/5 râu** (rig vẫn có
    xương râu: phải ẩn hoặc vẽ lại).
  - Tờ so: `sau_dat_non/mau/so_concept.png`; chồng hình bóng `mau/so_A.png`, `so_B.png` (đỏ = bố cục có mà concept không).
- **Người dùng chọn B** (2026-11-17). Da (`sau_dat_non_da.py`, không gen thêm ảnh nào, 0 credit):
  - `khop`: dựng rig dạng 1 mặc da dạng 2, lấy đỉnh lưới từng mảnh đầu ở px khung concept dạng 2 ↔ px bố cục (= px concept B). Mỗi mảnh
    là một phép affine gần tuyệt đối (sai ≤ 0,3 px; hàm 5 px vì vành mềm) → `mau/_khop_dau.npz`.
  - `dau`: vùng kín giữa nét mực của B (`mau/_vung_dau.png`): sọ {221, 255, 286, 396, răng trên}, hàm {534, 514, răng dưới}, nụ ngà
    579 / 596, mào 89 / 211 / 334, lòng miệng = vùng đất nung (tự dò). Mực chia cho nhóm gần nhất (sọ / hàm chung đường môi; tấm mào
    giữ TRỌN nét ở mép chung để kín viền). Lỗ kín không phải lòng miệng lấp hết (con ngươi to hơn 80 px). Sọ dưới nụ ngà tô màu mặt.
    Nắn ngược từng mảnh về khung concept dạng 2 qua lưới của nó (LinearND trên cặp đỉnh, ngoài lưới dùng affine) → rig gắn y dạng 2.
    Lòng miệng: đĩa dạng 2 đổi sang đất nung, XÉN trong hình bóng đầu B (mõm B nhỏ hơn, đĩa cũ lòi ra ngoài).
  - `than`: P_bozi_* + ảnh lót N_L đổi màu bằng mã (bụng kem → kem hồng, thân cát → hồng giun, vạch vòng đốt) giữ từng nét.
  - `rau`: thân râu nâu nhạt; dải hổ phách dưới khấc → thân râu (chỉ còn hạt ở ngọn), xoá vạch sẫm lẻ ở mép dải cũ.
  - Tua, phiến, tảng, gò cát giữ ảnh dạng 2 (B vẽ y như vậy). Rig ẩn thêm `A_chuxu_01 / 06` (B ba râu).
  - Lỗi đã sửa khi soi: con ngươi thủng; lòng miệng lộ trắng (nét gạch sẫm trong miệng làm thủng mặt nạ xén); tấm mào độn màu phẳng
    lộ ra lúc ngửa đầu (bỏ độn, thay bằng viền kín); đốm cam lẻ dọc thân râu.
- Rig: `SD_DANG=non py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/sau_dat_rig.py` (da dạng 1 đọc ở
  `inbox/sau_dat_non/manh/{part,cung}` + `tai_ve/N_L.png`, thiếu thì lấy dạng 2; `SD_DA2=1` mặc da dạng 2) → `sau_dat_non.atomik`
  626 KB, mọi clip nối idle 0,00 px. Tờ so rig ↔ concept: `mau/_so_rig_B.png`; cận đầu các dáng há: `mau/_can_da1.png`.
- Vào game: `quai/doi_sau_dat.py dang_1` (gộp clip tiến hoá bằng `doi_tho5_dang2.th` → `sau_dat_non_th.atomik` 871 KB, chép
  Resources/sau_dat_non, heroes.json dạng 1 = sau_dat_non cỡ 0,85). Unity: Nhập dữ liệu, Gắn dạng (prefab rua_nui: sau_dat_non,
  sau_dat_1). Hiệu ứng dùng chung với dạng 2 (bảng ThoFx / ThoAtk kẹp theo dạng; cỡ theo chiều cao tướng). Tour mới: "riêng Sa Trùng
  Nhi (sao 1, dạng 1)", "TIẾN HOÁ Sa Trùng". Golden không đổi, 110/110 test, biên dịch 0 lỗi. Ảnh trận: `mau/_game_{danh,mana,ult}.jpg`,
  tiến hoá `mau/_game_tienhoa.jpg`.
