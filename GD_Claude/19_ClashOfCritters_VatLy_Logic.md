# Clash of Critters: vật lý và logic đã lấy được

Soạn 2026-11-16. Gom mọi số vật lý và logic của Clash of Critters mà dự án đã đục hoặc đo được, chủ yếu là máy bi. Phần hiệu ứng, hình,
UI chỉ ghi chỗ tra (mục 6).

**Giới hạn:** logic game nằm trong Lua mã hoá, native lib có NetEase HTProtect. Không phá lớp bảo vệ (đã dừng 2026-11-10). Mọi số dưới
đây đọc từ asset Unity (prefab, ScriptableObject, vật liệu), đo bằng cách chạy lại, hoặc lấy từ số cộng đồng công khai. Chỗ nào là suy
luận thì ghi "đoán".

**Đơn vị:** u = đơn vị world của game đó. Sprite PPU 100, nên 1 u = 100 px thiết kế. Bi đường kính 0,162 u.

## 0. Nguồn

| Nguồn | Ở đâu | Có gì |
|---|---|---|
| Bản đục 0.50.1 | `D:\CrittersRipper` (máy kia) | `analysis/PINBALL_REPORT.md` (hình học bàn, vật lý, hiệu ứng, tiếng, rung theo ô), sơ đồ `table_01.png`, `tools/ps_dump.py` |
| Bản đục 0.51.1 | `D:\Ripper\ClashOfCritters` (máy này) | `Analysis/pinball_serialized_dump.txt` (dump prefab máy bi, config, vật liệu), `script_guid_map.tsv`, `AssetRipper_Export/` |
| Bản tóm đã có | `GD_Claude/07_MayBi.md`, `openspec/changes/update-pachinko-feel/design.md`, `ArtGen/Pachinko/THAM_KHAO_MAY_BI.md`, `ArtGen/Pachinko/refs/ban_duc_*.md` | áp vào máy mình, hiệu ứng, bảng số, mở capsule |
| Code chép lại | `Assets/01 Script/Core/Pachinko.cs` | toàn bộ hình học `table_01` và vật lý, viết lại thành mô phỏng tất định |
| Số cộng đồng | wiki, https://clashofcritters.online/chapters/ | ngưỡng cược, thang chương, tỉ lệ ô công bố trong game |

## 1. Máy bi: vật lý

### 1.1 Bi (`pbsc_pinball.prefab` và `PinballSettingsConfig`)

| Mục | Giá trị | Ghi chú |
|---|---|---|
| Rigidbody2D | Dynamic, khối lượng 1, `GravityScale 0`, `LinearDrag 0.3`, Interpolate, va chạm Continuous | trọng lực do code đặt từ config |
| Collider bi | Circle r 0,1 (prefab); trên bàn r 0,081 | bàn thu bi còn 0,81 |
| Vật liệu bi | không gán, nên lấy mặc định của Unity: ma sát 0,4, nảy 0 | quyết định cách trộn ở 1.2 |
| `gravity` | 2 | chạy thử 2 u/giây² thì bi lơ lửng (trung vị 7 giây, 18 lần chạm đinh). Hiểu là hệ số: **2 × 9,81 = 19,62 u/giây²** |
| `linerDrag` | 0 | config đè số 0,3 của prefab (đoán), bàn mới chạy với cản 0 |
| `minForce`, `maxForce` | 650, 680 | lực phóng ngẫu nhiên trong khoảng này |
| `minVelocity`, `maxVelocity` | 4, 14 u/giây | kẹp tốc mỗi bước |
| Vệt bi | `TrailController` 10 điểm, rộng 0,1, trắng alpha 0,66 → 0 | bản 0.50.1: TrailRenderer 0,3 giây, rộng 0,18 |
| Script trên bi | `Collision2DEvents`, `PinballSettings`, `PinballSyncer` (`mine` / `other`) | `PinballSyncer` có lẽ đồng bộ bi khi xem bàn người khác (đoán) |

### 1.2 Vật liệu và cách trộn

Unity 2D (Box2D) trộn hai vật liệu: **nảy lấy max, ma sát lấy căn của tích**. Bi có ma sát 0,4, nảy 0, nên số thật khi va là:

| Vật liệu | Ma sát / nảy | Gắn vào | Khi va với bi |
|---|---|---|---|
| `bouncer_mat_Red` | 0 / 0,8 | 22 đinh, mái cốc, đáy V | nảy 0,8, trơn |
| `bouncer_mat_topball` | 0 / 0,9 | nấm đỉnh | nảy 0,9, trơn |
| `bouncer_mat_Green` | 0,121 / 0,8 | hai nấm lớn (trứng, khiên) | nảy 0,8, ma sát √(0,121 × 0,4) = **0,22** |
| `bouncer_mat_Orange` | 0,121 / 0,8 | khung vòm, 4 vách ô | nảy 0,8, ma sát 0,22 |
| `floor_mat` | 0 / 0,5 | cảm biến ô (trigger) | không va, chỉ báo vào ô |
| `wall_mat`, `bouncer_mat` | 0,248 / 0,903; 0,121 / 1 | không thấy dùng trên bàn `table_01` | |

- Bi va bi: nảy max(0, 0) = 0, tức không nảy.
- Va chậm hơn 1 u/giây theo pháp tuyến thì không nảy (ngưỡng nảy mặc định của Physics2D).

### 1.3 Hình học bàn `table_01`

Toạ độ world (u), y lên. Khung rộng khoảng 5,49 u, cao 8,17 u (33 × 50 đường kính bi).

| Bộ phận | Hình | Chỗ |
|---|---|---|
| Khung vòm | `EdgeCollider2D` 26 điểm, offset (−0,18; 0,55) | x −2,78…2,71, y −3,39…4,78; vòm tròn ở trên, hốc nhọn ở trên phải (chỗ làn phóng nối vào) |
| 22 đinh | tròn r 0,15 | hàng y 3,89 / 3,5 / 2,9 / 2,5 / 1,9 / 1,2 / 0,8 / 0,45 / 0 / −0,55 / −1,2, đối xứng quanh x 0 (bảng đủ ở `Pachinko.cs`, `PegsU`) |
| Nấm đỉnh | tròn r 0,35 (prefab r 0,4 × 0,875, lệch y 0,23) | (−0,033; 4,916), lún nửa vào vòm |
| Hai nấm lớn | tròn r 0,55 | (±1,65; 1,985); trái: nấm trứng, phải: nấm khiên |
| Mái cốc thẻ | 4 thanh 0,19 × 0,53 | (±0,495; −0,052) nghiêng 69,1°; (±0,828; −0,267) nghiêng 52° |
| Cốc thẻ | cảm biến 0,80 × 1,21 | tâm (0,012; −0,832), dưới mái |
| Đáy chữ V | 2 thanh 0,18 × 0,70 và 0,18 × 0,63, 3 núm r 0,09–0,13 | dưới cốc, y khoảng −1,2…−1,4 |
| 4 vách ô | thân là hộp rộng 0,2279, cao 1,397–1,427 (đỉnh y −2,019); nắp tròn r 0,1111 tâm y −2,0101 | x −1,7529 / −0,5749 / 0,5681 / 1,7311 (nắp lệch +0,0004) |
| 5 ô đáy | cảm biến chữ nhật | tâm x −2,343 / −1,165 / −0,005 / 1,150 / 2,317, y −2,756; rộng 1,024 (ô giữa 1,15), cao 1,402 (ô giữa 1,15) |
| Camera | trực giao, nửa cao 6,67 u | |
| Da va chạm | `defaultContactOffset` 0,01 (Physics2DSettings) | Box2D bọc hộp và edge thêm 0,01 u, hình tròn không |
| Bước vật lý | Fixed Timestep 0,016 (TimeManager); Physics2D 8 vòng vận tốc, 3 vòng vị trí, velocityThreshold 1 | |

Ô giữa nằm khuất dưới đáy V. Bi chỉ vào được khi chui ngang qua khe giữa đáy V và đầu vách.

### 1.4 Phóng bi

- Nút PUSH: bi chạy lên làn ngoài mép phải, ra bàn ở hốc trên phải.
- Tốc lúc ra bàn = lực × 0,016 (một bước vật lý, khối lượng 1) = **10,4–10,9 u/giây**.
- Vị trí và hướng ra bàn không có trong asset (nằm trong Lua). Hình bàn dựng lại từ sprite (2026-11-19) cho thấy miệng ống ở góc
  trên phải, giữa đầu ray trong và chỗ vòm bắt đầu, tiếp tuyến với vòm.
  - Bi ra ống lăn ép vòm lên đỉnh, đâm gờ đỉnh (`topball`, nhô dưới vòm 0,21 u), rồi rơi ngẫu nhiên.
  - Bản chép: ra ở (1,814; 3,947), hướng 141,3° (song song đoạn khung 0 → 1); làn là đường hình chạy đều 22 u/giây.
  - 100 % bi chạm gờ đỉnh. Bản cũ phóng ngang 180° từ (1,90; 3,875) chỉ 6 % chạm.

### 1.5 Số đo khi chạy lại bàn này

| Đo | Kết quả |
|---|---|
| Thời gian bay | trung vị 3,07 giây (phóng dọc vòm; phóng ngang cũ: 2,95 khi bi xoay, 3,1 trước đó) |
| Chạm gờ đỉnh | 100 % bi, khoảng 0,19 giây sau khi ra ống (phóng ngang cũ: 6 %) |
| Chạm đinh | khoảng 10,4 lần mỗi bi |
| Chạm nấm lớn | trái 1,06 lần, phải 1,07 lần mỗi bi (phóng ngang cũ: 1,65 / 0,78) |
| Tỉ lệ vào cốc thẻ nếu để vật lý thuần | 15 % (game công bố 3,3 %); hướng nào cũng 11–22 % |

## 2. Máy bi: logic

### 2.1 Kết quả chọn trước, đường bi phát lại

- Vật lý thuần của chính bàn này cho cốc thẻ 11–22 %, xa số công bố 3,3 %. Bản đục có `PinballRecordSystem` và `PinballReplaySystem`.
- Kết luận (đoán, gần như chắc): **server chọn kết quả trước theo bảng tỉ lệ, client phát một đường bi khớp kết quả đó**.
- Research ghi "bi va nhau khi rơi nên một lần thả thành chuỗi sự kiện". Có bộ phát lại thì va chạm đó vẫn giữ được, vì đường bi là bản ghi.

### 2.2 Tỉ lệ ô (công bố trong game)

| Ô | Thưởng | Tỉ lệ |
|---|---|---|
| 4 ô kẹo (hai ô ngoài, hai ô giữa) | kẹo (EXP chung cả đội); hai ô giữa thêm sự kiện | khoảng 95 % |
| Cốc thẻ dưới mái | thẻ | 3,3 % |
| Ô khuất giữa đáy | jackpot: cướp hoặc thăm trại người khác | 1,7 % |

Số công bố cộng lại 99,6 %. Tỉ lệ cố định, hiện khi chạm vào máy.

### 2.3 Mỗi vật cản là một Entity chạy danh sách flow (khung ECF)

Mỗi nút trên bàn có `Entity` (`uniqueID`, `defID`, `flowNames`), `EffectController` (hiệu ứng theo tên sự kiện), `SoundController`,
`AnimationController`. Lua chạy các flow theo thứ tự khi có sự kiện.

| Nút | `defID` | Flow |
|---|---|---|
| Ô kẹo (`addmoney`, `addbigmoney`, `acvitymoney`) | 103 | `PBHitEndBall` → `PBHitPlayEffect` → `PBHitPlayAnimation` → `PBHitPlaySound` → `PBHitTriggerEvent` |
| Cốc thẻ (`gift`) | 102 | như trên, thêm `PBSettlePlayRandomEventFullTime`, `PBAccumulateBall`, `PBPlayEffect` |

Tên sự kiện trong `EffectController`:
- `Hit`: bi chạm. Đinh, nấm, ô đều có.
- `Settle`: tất toán khi hết đợt, ô sáng thưởng (ô kẹo, cốc, ô cướp).
- `ManualSettle`, `OperatorSettle`, `CustomSettle`, `HideSettle`: chỉ ở nấm trứng, nấm khiên, cốc (vòng tiến độ đầy, nhận thưởng, ẩn).
- Loại hiệu ứng: 0 sinh prefab; 2 chạy clip của nút con; 3 không prefab (đoán là rung); 4 `EventLight` (đèn sự kiện của máy, ở ô cướp).

Mỗi loại vật cản có ID tiếng riêng: đinh 2000008; mái và đáy V 2000007; nấm lớn 2000009.

### 2.4 Nấm tiến độ

- Hai nấm lớn có vòng tiến độ (`CircularProgressBarController`) và số đếm.
- Bi chạm nấm thì cộng nấc. Đầy thì ra một sinh vật ngẫu nhiên (nấm trứng) hoặc một khiên (nấm khiên).
- Mỗi ngày nhận tối đa vài lần ("2/3", có đếm ngược).

### 2.5 Cược theo số bi đang có

- Hệ số ×1…×100: thả một bi tốn N bi, thưởng × N.
- Ngưỡng (wiki): ×1, ×2 luôn mở; ×3 từ 240 bi; ×5 từ 360; ×10 từ 600–720; ×20 từ 1.200; … ×100 từ 7.200 bi đang có.
- Tụt dưới ngưỡng thì mất mức đó. Ở mức cao nhất, bảng cược ghi "mốc tiếp theo: mở khi có 8000 bi".
- Ở cược đặc biệt thì nút đổi sang bản kim cương, có hiệu ứng hút vào nút rồi nổ, lấp lánh lặp khi đang giữ mức đó.

### 2.6 Nguồn bi

- 8 cây bi trên sảnh, hồi chậm, hái từng cây.
- Đang có từ 420 bi trở lên thì không hái được.
- Hết bi thì hiện gói giảm giá. Tiền của game nằm ở vòi bi.

### 2.7 Trạng thái máy, bảng số, thanh cấp

- Đèn máy có 3 trạng thái: `idle` / `card` / `event` (clip `shine_group_level_1/2/3`); đèn chạy nhanh dần theo trạng thái. Thêm `launch_prompt_in/out` (nhắc bấm phóng).
- Bi vào ô kẹo: ô sáng, kẹo hiện số rồi bay lên. Bảng số LED đếm tăng, mỗi lần cộng thì khung bảng giật 0,083 giây và bật chữ "+N" (0,567 giây).
- Hết đợt: bảng "chốt" (gợn LED 0,48 giây, flipbook 1,07 giây) → "thu" (LED phun 0,65 giây) → số bay về thanh cấp → thanh chạy.
- Thứ tự tiếng: số nhảy → cộng điểm (0,33 giây) → thanh lên (2,1 giây) → thanh đầy (trễ 0,55 giây). Thanh đầy có rung `ExpbarFull`.
- Số trên ô (`txt_ball`) đổi theo mức cược; ô thẻ, ô cướp ghi "x10".

### 2.8 Phản hồi chia bậc theo giá trị

- **Chỉ ô hiếm nhất** mới có chậm thời gian, rung camera, tiếng hoan hô và chặn phóng (không cho thả bi mới trong lúc đó).
- Tiếng đinh: tối đa 2 tiếng cùng lúc, cách nhau ít nhất 0,1 giây, 3 biến thể, cao độ ±0,15.
- Rung chạm đinh: chặn 35 ms giữa hai lần.
- Rung, tiếng và độ dài hiệu ứng tăng theo giá trị ô.
- Rung camera (Cinemachine Impulse trên camera bàn): dài 0,2 giây, hướng (0, −1) (giật xuống), envelope giữ 0,2 giây rồi tắt 0,7 giây, listener gain 0,015 (rung rất nhỏ).

## 3. Ngoài máy bi

### 3.1 Thang chương và cấp (số cộng đồng)

- 120 chương, mỗi chương 80 ải, boss ở ải 10, 20 … 80.
- Cấp địch tăng khoảng 0,3–0,4 cấp mỗi ải: chương 1 từ 7 lên 36, chương 2 từ 39 lên 62, chương 6 khoảng 146–170, chương 12 khoảng 306–330, chương 72 khoảng 1.900.
- Cấp tài khoản lên nhờ máy bi (kẹo). Cấp tướng bằng cấp tài khoản. Trận thủ thành tự đánh, chỉ là cửa kiểm tra đội đã đủ mạnh chưa.

### 3.2 Bảng tiến trình

Đọc được tên bảng (`UnitLevel`, `UnitAttrLevel`, `UnitFeedLevel`, `UnitStar`, `UnitEvolution`, `Pet`, `Stage`…), nội dung mã hoá.
Muốn số thì đo trong game (chụp màn thú ở nhiều cấp, thanh EXP) hoặc dùng số cộng đồng.

### 3.3 Nhịp clip thú trong trận (33 thú, `gpuAnimData`)

| Clip | Dài |
|---|---|
| Đòn | 0,9–1,3 giây, trúng ở 0,23–0,47 giây (25–45 % clip) |
| Idle | 1,6–4 giây, thường 2–3 giây |
| Chết | 0,7–1,2 giây |
| Đi | 0,4–1,7 giây |

Thân thú nướng thành VAT (vị trí đỉnh mỗi khung), không còn xương. Dạng tiến hóa giữ nguyên nhịp đòn của dạng gốc.

## 4. Đã chép vào PokiClash ra sao

| Mục | Critters | Máy mình (`Core/Pachinko.cs`, từ 2026-11-09; bám Box2D sát hơn từ 2026-11-19) |
|---|---|---|
| Hình học | `table_01` | chép nguyên, 1 u = 78 đơn vị máy, khung 460 × 680; hộp là chữ nhật thật, vách = hộp + nắp tròn, da 0,01 u cho hộp và khung |
| Vật liệu, trọng lực, kẹp tốc, lực phóng | như mục 1 | chép nguyên: trọng lực 2 × 9,81 u/giây², cản 0, kẹp 4–14, lực 650–680 |
| Ma sát | Box2D | tự viết kiểu Box2D có xoay: bi giữ tốc góc (khối lượng 1, tròn đặc I = 0,5 m r², angularDrag 0); xung ma sát = −tốc trượt ở điểm tiếp xúc × m/3, kẹp ± 0,22 × xung pháp tuyến |
| Bước vật lý | Physics2D, 0,016 giây | tự viết, bước 0,016 giây (kẹp tốc một lần đầu bước, tính từ lúc bi ra bàn), 6 bước con, lưới tra nhanh vật cản |
| Bi va bi | có (theo research) | không, để đường bi chỉ phụ thuộc lực phóng |
| Kết quả | chọn trước, phát lại | chọn ô theo `pachinko.odds`, rồi thử lực 650–680 tới khi đường bi thật rơi đúng ô. Lực thử ra ô khác giữ vào kho; lúc rảnh thử sẵn 2 đường mỗi khung. Trung bình 1,9 lần thử, 0,07 ms mỗi lần (mono ngoài Unity 0,34 ms); 6.000 bi không bi nào trượt |
| Tỉ lệ | 95 / 3,3 / 1,7 | 25,3 / 22 / 1,7 / 22 / 25,7 % và cốc 3,3 % (0,4 % thiếu chia vào hai ô ngoài) |
| Nấm tiến độ | trứng ra sinh vật, khiên ra khiên | trái 25 nấc ra Rương bạc, phải 25 nấc ra +5 bi |
| Cược | ×1…×100, theo số bi | ×1, ×2 luôn mở; ×3 từ 150, ×5 từ 300, ×10 từ 700 bi |
| Cây bi | 8 cây, trần 420 bi | 5 cây, không trần |
| Tất định | không rõ | cùng hạt giống ra cùng đường bi; bản web còn vật lý cũ (trước 2026-11-19), không còn trùng Unity |

Bàn cũ trước 2026-11-09 (85 đinh, trọng lực 1.100, kẹp 150–525) ghi ở `07_MayBi.md`, mục "Vật lý chép". Bàn đó không còn đúng.

## 5. Chưa có hoặc không đọc được

- Vị trí, hướng phóng thật; đường bay capsule; nhịp "mở tất cả"; tốc chạy thanh cấp: nằm trong Lua.
- Tỉ lệ thật phía server và cách chọn kết quả: chỉ suy ra từ số công bố và tên hệ thống.
- Bàn bi điên (`pbsc_frenzyball_table_02`) và chế độ frenzy: có asset, chưa đọc vật lý.
- `PINBALL_REPORT.md` bản đủ (tiếng, rung theo từng ô) chỉ có ở máy kia.

## 6. Tra thêm

- Bộ phận và 36 prefab hiệu ứng máy bi: `ArtGen/Pachinko/THAM_KHAO_MAY_BI.md`.
- Bảng số LED, thanh cấp, icon bay, ánh sáng: `ArtGen/Pachinko/refs/ban_duc_bang_so.md`.
- Mở capsule thú: `ArtGen/Pachinko/refs/ban_duc_mo_capsule.md`.
- Hạt hiệu ứng trận: skill `pokiclash-hero-fx`, mục 1b.
- Máy bi Critters về kinh doanh, móc tâm lý, pháp lý: `07_MayBi.md`.
