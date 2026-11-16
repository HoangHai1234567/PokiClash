# Tinh linh quặng sắt (`quang_sat`): tướng 3 đảo Kim

Bắt đầu 2026-11-16 (máy ổ C). Con gốc của rig: `monster_3371` (khối vỏ trắng như mũ, dải mặt tối hai mắt bầu dục xanh lơ, ba tinh thể tím hồng
trên đầu, hai tinh thể làm tay lơ lửng; game tham khảo, kho `D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip
`idle_01`). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là của mình. Suất 3
đảo Kim = ải 10 ("Rừng Lưỡi Liềm", `IslandGen.cs` Plan Kim), id game hiện là **`bo_ngua`**. Mã làm việc `quang_sat`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-16)

- "tướng thứ 3 đảo kim; concept **tinh linh quặng sắt**, **chủ ý làm biểu cảm mắt như con gốc**".
- appear: "tướng đang **nằm đất ngủ, mở mắt và bay lên**".
- idle / walk: "có thể làm **giống con gốc, sửa đi chút**, nhưng phải **để ý animation mắt**".
- Đánh thường: "tướng **lao vào húc** đối thủ".
- Chiêu mana: "**phóng 2 tay vào người đối thủ rồi thu lại** (kết hợp animation và code điều khiển tay)".
- Chiêu cuối: "tướng **chui xuống đất** rồi làm 1 animation **đất bị trồi lên do đào đất** (chuỗi chũi trong phim hoạt hình) **tới vị trí
  địch** rồi tướng **trồi lên húc tướng địch từ dưới lên** (animation húc từ dưới lên dùng `skill_01_2`)".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3371/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample_goc.json` 12 clip 30 khung/giây,
`keys.json`, `khung/`, `mo/`, `parts/`; script `quang_sat.py` mo / nhom / part_goc)

19 xương, 14 slot (8 hình bật ở idle 0), 12 clip, 1183 khoá. Không IK, không path; **2 transform** nhỏ (`longdan_1`: xương mắt cha `longdan_5`
theo `longdan_10` mix 0,05; `longdan_10`: `longdan_11` theo `longdan_10` mix −0,5: kéo nhẹ tinh thể đầu khi thân méo). Con nhìn sang PHẢI
(hơi nghiêng). Mọi hình là LƯỚI (4–40 đỉnh); atlas có vùng xoay 90 / 270 (`quang_sat._luoi` vá như `tinh_sat_2`). Ảnh mẫu 1536 × 1024:
2,408 px / đơn vị.

Cây xương: `root` → `all` → `longdan_2` (TÂM THÂN) → `longdan_9` (thân, xoay ~105°) → `longdan_10` (đỉnh thân; lưới thân bám 9 + 10),
`longdan_5` (cha hai mắt) → `longdan_16` (mắt trái), `longdan_17` (mắt phải); `longdan_2` → `longdan_7` → `longdan_8` (TAY TRÁI, hai đốt);
`longdan_2` → `longdan_12` → `longdan_0` (TAY PHẢI, hai đốt). `all` → `longdan_4`, `longdan_6`, `longdan_13/14/15` (xương của bản sao ẩn).

| thứ tự vẽ (idle) | slot | ảnh vùng (px) | đỉnh | là gì | xương |
|---|---|---|---|---|---|
| 1 | `longdan_0` | 48×84 | 4 | TAY PHẢI: tinh thể ngắn mảnh dưới phải, sát mép vỏ (SAU thân) | longdan_0 |
| 3 | `longdan_9` | 224×182 | 40 | THÂN: vỏ trắng + dải mặt tối (đỉnh lõm chữ V, đáy răng cưa) + hai hạt tím trên góc mặt + hai đường ráp | longdan_9 0,98 + longdan_10 |
| 4 | `longdan_8` | 20×31 | 4 | MẮT PHẢI (bầu dục xanh lơ, nhỏ hơn); hình phụ `longdan_6` 31×31 = `<` | longdan_17 |
| 5 | `longdan_7` | 24×32 | 4 | MẮT TRÁI (to hơn chút); hình phụ `longdan_5` 43×34 = `>` | longdan_16 |
| 6 | `longdan_4` | 97×116 | 8 | tinh thể TO giữa đỉnh (trước thân) | longdan_9 / 10 / 11 |
| 8 | `longdan_3` | 69×85 | 8 | tinh thể trên TRÁI | longdan_9 / 10 / 11 |
| 10 | `longdan_2` | 47×77 | 7 | tinh thể trên PHẢI | longdan_9 / 10 / 11 |
| 12 | `longdan_1` | 103×89 | 4 | TAY TRÁI: tinh thể dài dưới trái (TRƯỚC thân, vẽ cuối) | longdan_8 |
| ẩn | `longdan_6`, `_5`, `_10`, `_11`, `_12` | | | bản sao tay / tinh thể đầu trên xương con của `all`: `skill_02` cho văng ra | longdan_6 / 4 / 15 / 13 / 14 |

Thứ tự vẽ đổi trong clip: tay phải ra TRƯỚC thân ở `block_01`, `skill_01_2` (đầu clip), `skill_01_3` (từ khung 13), `skill_02` (từ khung 3).

**Mắt (người dùng dặn để ý):** hai mắt là hai mảnh cứng trên xương riêng, cùng cha `longdan_5` (xoay ~107°, nên `sx` của nó là chiều DỌC mắt).
- chớp: `longdan_5` sx 1 → 0,55 → 0,1 → 0,55 → 1 (idle khung 54–57);
- liếc / nheo MỘT mắt: `longdan_17` (mắt phải) sx 1 → 0,44 (idle khung 65–68), giữ tới khung 96, mở lại 98;
- nheo hai mắt lấy đà: `longdan_5` sx 0,58 (skill_01_1, skill_01_2 khung 4–12; skill_01_3 khung 2–24);
- `block_01`: hai mắt dẹt ngang (sx 0,71, sy 1,16), `longdan_5` sx 0,51;
- nhắm `>` `<` (đổi hình `longdan_5` / `longdan_6`): hit (khung 3–10), stun, die, floating (tới khung 38), skill_02 (khung 7–42).

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho (dự kiến) |
|---|---|---|---|
| `idle_01` | 6,67 | nhún, tay đung đưa, chớp mắt, nheo một mắt | **idle** (sửa chút) |
| `run_01` | 0,53 | nảy lắc lư, hai tay chèo | **walk** |
| `skill_01_1` | 1,07 | nheo mắt, ngả ra sau, BẬT chéo lên phải (0,48) húc, rơi về | **attack** (lao húc) |
| `skill_01_2` | 1,07 | thu tay, nheo mắt, BẬT THẲNG lên cao (0,48–0,68), rơi về | **chiêu cuối** (đoạn trồi lên húc từ dưới) |
| `skill_01_3` | 1,07 | bật lên, hai tay vung ra trước / sau, rơi | nguồn dáng vươn tay (chiêu mana) |
| `skill_02` | 1,60 | nhắm `> <`, co người, rồi vỡ tung, các mảnh văng, biến mất (1,45) | không dùng (có thể lấy đoạn co người) |
| `floating_01` | 1,83 | bị hất tung, lộn, rơi, mở mắt | nguồn ý cho appear (đoạn mở mắt bay lên) |
| `hit_01`, `hit_02`, `block_01`, `stun_01`, `die_01` | | | **hit** = hit_01, **die** = die_01 |

## 3. Concept lượt 1 (Claude đề xuất ba hướng; người dùng chọn C)

Gói `gui_gpt/quang_sat_1/` (`quang_sat_da.py ca_con`, `concept`). Ảnh mẫu 1 = hình cả con gốc `mau/goc_ca_con.png` (khung 0 idle; khung bao
từng part trong `.json`, ghi vào prompt); ảnh 2 = tinh linh tinh thể sắt (tướng 1 đảo Kim, nét + cách tô kim loại); ảnh 3 = tượng đá giữ rừng
(cách tô đá). Mọi hướng giữ dáng, chỗ, cỡ từng mảnh và GIỮ NGUYÊN đôi mắt bầu dục + dải mặt tối (lời dặn "biểu cảm mắt như con gốc"):
- (chưa có ảnh: Codex từ chối hai lần "hệ thống an toàn", có lẽ vì bản này giữ sát hình con gốc nhất) `tai_ve/L1_A.png` **đá xám + quặng sắt gỉ**: tinh thể thành cục quặng thô đầu bằng (giữ chỗ, cỡ, độ nghiêng), sắt xám sẫm có mảng gỉ cam; mắt
  xanh lơ; hai núm trán là hạt gỉ.
- `tai_ve/L1_B.png` **đá cát + hematit đỏ**: khối quặng ĐỔI DÁNG thành cụm khối lập phương (2–3 khối), mặt trước đỏ nâu, mặt trên xám thép;
  mắt hổ phách.
- `tai_ve/L1_C.png` **đá xám lam + từ thạch đen**: khối quặng ĐỔI DÁNG thành tinh thể bát diện sắt đen có một đường gờ bạc; vỏ có ba chấm sắt;
  mắt xanh lơ.

B, C đạt lượt đầu: chồng hình bóng con gốc IoU 0,906 / 0,919 (`mau/_so_goc.png`); thân, dải mặt, mắt trùng chỗ; tay phải của B chờm ra TRƯỚC
mép vỏ (rig để tay phải sau thân ở idle: lúc gen mảnh vẽ đủ khối). Trang xem: `inbox/quang_sat_xem_concept.html`. Người dùng chọn **C**.

## 4. Chốt concept + mảnh (2026-11-16)

Người dùng chọn **C** → `tai_ve/L1_duyet.png` (= `L1_C.png`). Mảnh "đúng chỗ, đúng cỡ" (`quang_sat_manh.py`, gói `gui_gpt/quang_sat_1/luot_2_*`):
M1 thân (vỏ đá + dải mặt, KHÔNG mắt, vẽ đủ vòm dưới các tinh thể), M2 năm tinh thể bát diện (ba trên đầu, hai tay), F2 mắt nhắm `> <` MÀU XANH LƠ
(dải mặt gần đen nên dấu đen của con gốc sẽ không thấy), F3 mắt ngủ (cung cong xuống, cho appear), D1 gò đất + hố (chiêu cuối). Mắt mở cắt thẳng từ
concept (vùng xanh lơ + vành mực, `mat`). Ghép lại so concept: IoU hình bóng **0,979** (`manh/_ghep.png`). GPT vẽ gò, hố to gấp rưỡi lời dặn: rig
thu `K_GO` 0,68, `K_HO` 0,74 (lòng hố 266 × 60 đơn vị, vừa thân chui lọt).

## 5. Rig + clip (`quang_sat_rig.py`; `inbox/quang_sat_1/rig/`, không theo git)

29 xương (19 của họ + `move`, `day` đáy thân, `tam` tâm thân cha của `all`, `far`, `fly_t/p` + `bay_t/p`, `ho`, `go`, `cat_x`), 17 slot, 717 đỉnh,
1 mặt nạ cắt, 8 clip, .atomik **133 KB**; mọi clip nối về idle 0 px. Thân và ba tinh thể đầu: lưới phủ hình, mỗi đỉnh bám như điểm tương ứng trên
lưới của họ (`trong_so_goc`, như `rong_vay_rig.gan_goc`) nên thân rung đúng kiểu thạch của họ (xương `longdan_10` kéo đỉnh thân, trọng số ≤ 0,05).
Tay, mắt: ô 4 đỉnh một xương. Bản sao hai tay của `die_01` (`longdan_6`, `longdan_5`) đặt bằng phép affine khớp uv. Tay phải ra trước thân ở
các khung họ đổi thứ tự vẽ: slot `longdan_0~truoc`. `QS_GOC=1`: chạy bằng da gốc tạm (`manh_goc/`, chỉ để soi trong máy).

| clip | dài | làm gì | sự kiện |
|---|---|---|---|
| appear | 2,36 | nằm bẹp ngủ (mắt ngủ, thở), mở mắt lờ đờ → chớp → mở to, bật bay lên, hạ về | `ngu` 0,2; `cham_dat` 2,18 |
| idle | 6,67 | idle_01 (chớp 1,83, nheo mắt phải 2,2–3,2) + hai tay xoay một vòng như nam châm 4,30–5,10 (nheo mắt) | |
| walk | 0,53 | run_01 | |
| attack | 1,00 | skill_01_1, lao `move` 0,62 chiều cao ở khung húc, bẹp đúng khung chạm | `trung` 0,46 |
| cast | 1,62 | lấy đà kéo hai tay về sau, tay trái phóng 0,40, tay phải 0,467 (bay 0,20), găm 0,24, về 0,30 (tay trái vòng qua đầu), xoay 1 vòng, lắp đúng chỗ tay thật | `phong` t/p, `trung` 0,612, `ve` t/p |
| skill | 3,20 | lấy đà → bật lộn ngược 0,30–0,56 → mũi tinh thể cắm đất `dao` 0,62 (hố mở, mặt nạ cắt) → khuất 0,82 → gò đất nhô 0,88, mũi tinh thể ló như vây → chạy ngầm 1,02–1,80 (`move` 0,9 chiều cao, khai **lunge**: game nắn tới 72 % quãng) → gò phồng → `troi` 1,92: mũi tinh thể phá đất, vọt lên húc `trung` 2,08 (đoạn bật skill_01_2, độ cao tự lái) → rơi `cham_dat` 2,40 → nhảy lùi về 2,56–3,02 | `dao`, `chay`, `troi`, `trung`, `cham_dat` |
| hit | 0,50 | hit_01 (mắt `> <`) | |
| die | 1,45 | die_01 + mờ 0,45 | |

Game: `lunge = [skill]` (đường đào dùng sẵn `AolaSticker.Lunge`, không cần code mới), `far = farAim = [cast]` (tay bay dùng sẵn
`AolaActor.FarAtomik`), `stay = [cast]`, `span` 3,8. Mọi dời dọc của chiêu cuối (bật, cắm, vọt, nhảy về) đặt ở `day`, KHÔNG ở `move` (game nắn
cả vectơ `move` theo quãng tới đối thủ: dời dọc trong `move` sẽ bị phóng theo).

Soát: tờ khung bộ vẽ Python (`soi_*.png`), runtime Spine thật (`rig/that/`, cận đoạn chui / trồi `rig/that_can/skill.jpg`: mặt nạ cắt đúng),
đo giật (`quang_sat_rig.py kiem`). Đã sửa: (1) idle: `hoat.dong_vong` hoà các khung cuối về khung 0 làm hai tay quay NGƯỢC trọn một vòng sau
trò xoay → `nuong_idle` giữ +360 ở khung cuối (360 ≡ 0); (2) cast: bản sao tay hết đường về rơi từ 360° về 0 giữa hai khung (runtime nội suy
lúc alpha còn bật) → giữ dáng cuối khi đã ẩn; (3) chiêu cuối: đổi dáng dưới đất ở 0,88 s (hai khung kề đều ẩn), không ở khung thân còn hiện.
Còn lại là chuyển động cố ý: cú vọt khỏi hố ~0,6 chiều cao / khung, tay xoay 40–60° / khung lúc bay về, đoạn quăng tay của nguồn ở attack.

Ảnh động (giả lập phần game: lunge, far với đối thủ đứng xa 1,9 chiều cao): `inbox/quang_sat_1/_xem_dong.py` → `rig/dong/*.webp`; trang xem
`inbox/quang_sat_xem_rig.html`. **CHỜ người dùng xem.**

## 6. Việc tiếp

1. (xong) Người dùng xem rig dạng 1: "ổn rồi".
2. Hỏi: thay suất `bo_ngua` (ải 10) không đè `bo_ngua_1..3` cũ? tên, số dạng?
3. Vào game: script đổi tướng (như `quai/doi_nui_lua.py`), heroes.json, menu Unity; VFX theo sự kiện: bụi đất toé ở `dao`, vệt đất / đất vụn
   theo gò ở `chay` (bám xương `go`), đất nổ + mảnh đá văng ở `troi`, tia va chạm khi tay găm (`trung` của cast), Zzz ở `ngu` (appear).

## 7. DẠNG 2 (2026-11-16)

Người dùng: "**ổn rồi, làm dạng 2 của nó**". Hỏi 3 câu: rig → "**tự nghĩ**"; dòng **2 dạng** (dạng 2 là dạng cuối); đòn, chiêu **như dạng 1,
mạnh hơn**. Ứng viên trong kho: `monster_3372` (số liền sau, cùng bộ tinh thể tím: dạng người trùm mũ, mặt nạ có mắt, gậy mũi tinh thể; 48 xương,
3 IK, 12 transform; clip đâm gậy, giơ gậy bổ), `monster_3373` (vòm tối, mặt tinh thể xanh há to, sừng hồng, hai vây dính thân, KHÔNG mắt; 24
xương), `monster_3381` (thú bờm tinh thể tím). Claude chọn **dựng dạng 2 trên CHÍNH rig `monster_3371`**: đòn húc / phóng hai tay / chui đất cần
hai tay rời + thân vòm; đôi mắt (người dùng chủ ý giữ) là nét nhận dòng. Bóng dáng phải khác hẳn dạng 1 (luật 0a): vỏ giáp nặng hơn, to hơn
chút, mày giáp chữ V, chỏm đầu và hai tay đổi dáng; dải mặt + hai mắt giữ y dạng 1.

Concept lượt 1 (`quang_sat_2_da.py concept` → `gui_gpt/quang_sat_2/`, ảnh mẫu duy nhất = concept dạng 1 đã duyệt), ảnh về `inbox/quang_sat_2/tai_ve/`:
- `L1_A.png` giáp thép rèn sẫm + mày giáp thép, hai sừng thép ngắn, vương miện NĂM gai bát diện cao, tay = hai tinh thể ghép như găng;
- `L1_B.png` đá bazan có ba mạch quặng cam phẳng, chùm năm gai hematit đỏ gỉ, tay = cục hematit lởm chởm;
- `L1_C.png` thép xám lam, hai sừng tinh thể cong thành NAM CHÂM MÓNG NGỰA (đầu đỏ / bạc), tay = hai khối cực nam châm đỏ bạc.

Ba ảnh về lượt đầu (không bị từ chối). Soát: dải mặt, hai mắt (dáng, chỗ, cỡ, màu) như dạng 1; hai tay rời thân. A còn chút sáng tối ở mép vòm
(lúc gen mảnh dặn tô phẳng). Tay phải của A, B chờm trước mép thân; rig để tay phải (bên xa) SAU thân như con gốc: lúc gen mảnh vẽ đủ khối, phần
chờm sẽ nấp sau thân. Trang xem: `inbox/quang_sat_2_xem_concept.html`. Claude nghiêng về **B**. **CHỜ người dùng chọn.**
Đề xuất "mạnh hơn" (chờ người dùng chốt cùng concept): đánh thường húc rồi lộn một vòng giáng thêm nhát nữa (2 nhát); chiêu mana phóng hai tay +
năm gai trên đầu cùng bay đâm vào đối thủ (code lái) rồi bay về lắp lại; chiêu cuối chui đất, trồi lên húc, rơi lại xuống hố rồi trồi húc lần
hai mạnh hơn, nhảy về.

### 7b. Chốt concept dạng 2 + mảnh + rig (2026-11-16)

Người dùng chọn **B** → `quang_sat_2/tai_ve/L1_duyet.png` (= `L1_B.png`); không bác các chiêu "mạnh hơn" Claude đề xuất nên làm theo đó.
Mảnh (`quang_sat_2_manh.py`, dùng lại hàm của `quang_sat_manh.py`): M1 thân (vòm bazan, mạch cam, mày đá, hai nụ gỉ, dải mặt KHÔNG mắt),
M2 gai giữa + hai gai ngoài (`gai_t`, `gai_p`: slot THÊM, bám như lưới thân) + hai tay. Màu đỏ tờ M2 sáng hơn concept ~30 kênh đỏ: kéo về đúng
concept (`quang_sat_2_mau.py can`). **Codex hết hạn mức lúc ~12:05 (mở lại 14:00)** nên M3 (hai gai trong) không gen được: cắt thẳng từ concept
(`quang_sat_2_mau.py gai`: gộp các mặt đỏ, khép qua nét gờ, bỏ mạch cam, kẻ lại viền mực kín). Mắt mở cắt từ concept B (lệch dạng 1 ~10 px trái,
12–16 px xuống); mắt nhắm, mắt ngủ, gò, hố lấy của dạng 1 (mắt nhắm / ngủ dời theo mắt mở). Ghép so concept IoU **0,981**.
Trước đó (10:36–11:36) mọi lượt gen của mọi phiên đều hết giờ 20 phút không ảnh: Codex trục trặc / sắp hết hạn mức.

Rig: `QS_DANG=2 quang_sat_rig.py` (cùng script dạng 1, rẽ nhánh theo `DANG`) → `inbox/quang_sat_2/rig/`: 39 xương, 24 slot, 1110 đỉnh,
.atomik **138 KB**. Chiều cao game khai **285** (không tính chùm gai vượt lên; đo cả gai ra 352 thì thân dạng 2 trên sân nhỏ hơn dạng 1), `span` 4,6.
- attack 1,45 s: húc (`huc1` 0,46, VFX) → bật lên lộn một vòng (`tam` −360°) → giáng xuống `trung` 0,92 (khung trúng của game; game chỉ nhận MỘT
  khung trúng mỗi clip) → về. Kết thúc ở −360° ≡ 0 nên KHÔNG hoà về idle (`khong_khop`), lệch khung 0 idle 0,22 px.
- cast 1,85 s: hai tay (0,40 / 0,467) rồi năm gai (0,533 → 0,70, gai giữa cuối) phóng; mỗi mảnh găm 0,24 s rồi bay vòng về, lắp đúng chỗ
  (gai lắp theo `longdan_9`: `REF`). Sự kiện `phong` / `ve` mỗi mảnh (chuỗi = khoá mảnh).
- skill 3,82 s: như dạng 1 tới `troi` 1,92 → húc lần một `huc1` 2,08 → rơi lại xuống hố 2,36 → đất nổ lần hai `troi2` 2,46 → húc lần hai cao hơn
  70 đơn vị `trung` 2,66 → `cham_dat` 3,00 → nhảy lùi 3,16–3,62.
- appear, idle, walk, hit, die như dạng 1. IMPACT mạnh hơn (attack 0,10 / 0,6 / 0,15; skill 0,26 / 1,4 / 0,32, chớp trắng).
Soát: soi bộ vẽ Python, runtime Spine thật (`rig/that_can/skill.jpg`, `rig/that_cast/cast.jpg`), đo giật (chỉ còn vòng lộn 40–60°/khung, mảnh
bay xoay, cú vọt: cố ý). Trang xem: `inbox/quang_sat_2_xem_rig.html`. **CHỜ người dùng xem.**

## 8. Vào game (2026-11-16; người dùng: "bạn cho vào game chưa" → chọn "Làm luôn, Claude đặt tên tạm")

- **Dữ liệu** `quai/doi_quang_sat.py` (dùng lại `doi_phap_lua.py`): suất 3 đảo Kim `bo_ngua` (ải 10 "Rừng Lưỡi Liềm") giữ id, thẻ, chỉ số, hiệu
  ứng thẻ; SỐ DẠNG 3 → 2. Tên tạm (Claude đặt, người dùng đổi được): tướng **Thiết Khoáng** ("Tinh linh quặng sắt chui đất", "Dòng Thiết
  Khoáng"); dạng **Thiết Khoáng Nhi** (`quang_sat_1`, cỡ 0,92) / **Thiết Khoáng** (`quang_sat_2`, cỡ 1,0); thẻ Song Quyền Quặng (fist2; thẻ
  đánh 2 nhát), Độn Thổ Húc (crack), Mắt Dò Mạch (eye, +chí mạng). Tên ải "Rừng Lưỡi Liềm" chưa đổi. `Resources/bo_ngua_*` cũ không đụng.
- `doi_quang_sat.py th`: dạng 1 gộp dạng 2 + clip `evolve` → `inbox/quang_sat_1/rig/quang_sat_1_th.atomik` (197 KB, 68 xương, 9 clip; khung cuối
  khớp idle dạng 2 lệch 0; `rig/khung_evolve.png`). `chep` → `Resources/quang_sat_1/` (bản gộp), `Resources/quang_sat_2/`, chân dung.
- **Code** (chỉ khai bảng, dùng lại hiệu ứng sẵn có): `StageView.KimFx["bo_ngua"]` = mana `n_da_va` (hai cú nổ đá vụn lúc tay găm, HatDa) /
  ult `n_sat_dap1`, `n_sat_dap` (vòng cột tinh thể trồi quanh đối thủ lúc húc từ dưới, HatSat); `KimAtk["bo_ngua"]` = `n_sat_tong`;
  `HatLua.Themes["bo_ngua"]` (tia bạc, than gỉ cam, mảnh quặng đen); `HatNuoc.WThemes["bo_ngua"]` (bụi đất nâu). Không có thì game bắn "tia cũ"
  đè lên tay bay. Tour `Editor/KimFxTour.cs`: hai mục "Đảo Kim: riêng Thiết Khoáng (dạng 2) / Thiết Khoáng Nhi (dạng 1)…".
- **Unity** (cầu MCP 8080): biên dịch sạch → "Nhập dữ liệu" (88 tướng, 265 thẻ riêng) → "Gắn dạng .atomik" (`bo_ngua: prefab giữ 2 dạng
  (quang_sat_1, quang_sat_2)`) → "Đảo 70 ải: sinh lại" (`stages.json` không đổi) → ba menu golden + `golden_ghep.py`: `roster.json` (bo_ngua
  n 3 → 2), `battles.json` 1 trận (hạt 362986235: bo_ngua boss tiến hoá một lần thay vì hai). EditMode **106 / 107** (chỉ `PrefabOnlyTests`
  cũ ở `UI/Kit`).
- **Soi trong trận** (tour, cả hai dạng, phía mình quay trái): tên, thẻ hiện đúng; đòn thường lao húc (dạng 2 lộn giáng) có chớp; chiêu mana tay
  (+ năm gai ở dạng 2) bay găm vào đối thủ đúng chỗ, đá vụn, bay về lắp lại; chiêu cuối chui đất, gò đất chạy tới trước mặt đối thủ (game nắn
  quãng), trồi lên húc có chớp + cột tinh thể, nhảy về. Ảnh `Temp/PokiShots/kim_fx/bo_ngua_<1|5>sao_*.jpg`.
- Chưa: tên thật (người dùng), tên ải; VFX riêng cho bụi đất lúc cắm hố (`dao`), vệt đất theo gò (`chay`), đất nổ (`troi`, `troi2`), nhát
  `huc1`; gen lại hai gai trong dạng 2 bằng GPT khi Codex có hạn mức (hiện cắt từ concept).

## 9. Hiệu ứng riêng (2026-11-16; người dùng: "bạn có thể làm thêm hiệu ứng", rồi "không cần check trong play, khi nào xong tôi tự vào xem")

`Assets/01 Script/Game/Battle/HatKhoang.cs` (mới, đi đường "n_" → `HatNuoc.PlayNuoc`), thay các mã mượn ở `StageView.KimFx` / `KimAtk`:
- `n_khoang_huc` (đòn thường; `HatVoi.AtkLao` có mã này): dạng 1 húc: chớp, tia, dăm quặng, bụi. Dạng 2 (nhận ra bằng lead > 0,7 s) thêm
  nhát húc 0,46 rồi cú giáng: chớp lớn, vòng sóng đất, đất toé.
- `n_khoang_ban1` / `n_khoang_ban2` (chiêu mana): một cú nổ dăm quặng mỗi lần một mảnh găm, đúng giờ mảnh tới (dạng 1: 0,600 / 0,667; dạng 2:
  thêm 0,733 / 0,767 / 0,800 / 0,833 / 0,900), cú cuối to hơn có vòng bụi.
- `n_khoang_dao1` / `n_khoang_dao` (chiêu cuối): đất toé lúc cắm hố (0,62), đất phụt theo lúc chui, bụi lúc gò nhô (0,88), đất hất sau gò lúc
  chạy ngầm (1,02–1,80, gò đi theo cú lunge: chân mình → 72 % quãng tới đối thủ), sỏi rung trước khi trồi, đất nổ + vòng sóng lúc trồi (1,92);
  dạng 2: húc lần một (2,08), rơi lại hố (2,36), đất nổ lần hai to hơn (2,46); húc cuối: chớp + VÒNG CỘT QUẶNG riêng (`KhCot`: dạng 1 sắt đen,
  dạng 2 hematit đỏ; thay cột tinh thể lam bạc của Thiết Tinh) + đất toé; bụi lúc rơi đất và lúc nhảy về.
- Màu: bụi NÂU sẫm (`KhBui`; bụi be của bộ khác lẫn vào nền cát), dăm theo dạng. Mốc giờ = mốc sự kiện của rig, co giãn theo lead / khung trúng.
- Rig: giảm chớp trắng màn chiêu cuối (`IMPACT` skill dạng 1 `#ffffff4d`, dạng 2 `#ffffff66`; trước 88 / aa làm màn trắng bệch mấy khung),
  xuất lại hai rig, gộp tiến hoá, chép Resources, gắn lại prefab.
- Biên dịch sạch; EditMode 106 / 107 (chỉ `PrefabOnlyTests` cũ). Một lượt tour trước khi chỉnh cỡ / màu cho thấy hiệu ứng có chạy đúng giờ
  nhưng hạt nhỏ và bụi be khó thấy → đã chỉnh; bản sau chỉnh CHƯA chụp trong Play (người dùng tự xem). Lỗi gặp khi viết: `Every` truyền
  TIẾN ĐỘ 0..1 (số thực), không phải chỉ số hạt; tên trường trùng tên hàm trong partial `HatLua` (CS0102).
