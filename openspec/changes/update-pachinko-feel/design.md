## Context

Bản quét máy bi Critters (`D:\CrittersRipper\analysis\PINBALL_REPORT.md`) cho số liệu và cách làm. Phần lấy về:
- **Mặt máy:** cốc hiếm có mái ^ và khe hẹp ở đỉnh, đinh gác ngay trên khe; ô hiếm nhất khuất dưới đáy cốc; năm ô đáy gần bằng nhau.
- **Vật lý:** nảy 0,8–0,9, trọng lực thấp, lực cản, tốc độ kẹp.
- **Hiệu ứng:**
  - mỗi nút có danh sách "flow" chạy khi chạm;
  - chỉ ô hiếm nhất có chậm thời gian, rung camera, hoan hô, chặn phóng;
  - tiếng đinh có tối đa 2 tiếng cùng lúc, cách 0,1 giây, ba biến thể, pitch ±0,15;
  - rung chạm đinh chặn 35 ms; rung, tiếng và độ dài hiệu ứng tăng theo giá trị ô.

Phần logic và tỉ lệ thật của họ nằm trong Lua mã hoá, không đọc và không dùng.

Máy bi của mình (`add-pachinko-machine`) dùng vật lý tự viết, chép từ web sang C#, đo tỉ lệ bằng mô phỏng 6.000 bi, so golden. Đổi vật lý hay mặt máy làm tỉ lệ đổi, nên phải chỉnh lại cho kinh tế mỗi bi không đổi.

## Goals / Non-Goals

**Goals:**
- Tỉ lệ từng loại ô và kinh tế mỗi bi giữ như mặt máy cũ: 9,4 EXP, hoàn 0,32 bi, 0,086 thẻ mỗi bi ở ×1.
- Web và Unity ra cùng từng bi (golden khớp tuyệt đối, không chỉ dưới 1 điểm).
- Cảm giác chia bậc theo giá trị thật.

**Non-Goals:**
- Chép hình, tiếng, prefab FX hay toạ độ bàn của Critters.
- Bán bi, hệ số cược mới.
- Hiệu ứng mới cho bản web: web giữ vai trò nguồn số và bản thử; chỉ vẽ két cho đúng.

## Decisions

### Vật lý: chép vật liệu của máy tham khảo, giữ trọng lực đủ cao

Lượt đầu (bảng dưới) chọn nảy vừa phải. Sau đó chủ dự án bảo "copy hiệu ứng và vật lý của game đó sang", nên chép vật liệu của
máy tham khảo, đổi theo đường kính bi (bi ở đó 0,162 u, ở đây 18, nên 1 u = 111):

| Mục | Máy tham khảo | Ở đây |
|---|---|---|
| Nảy | 0,8 mọi thứ (nấm đỉnh 0,9) | 0,8 mọi thứ |
| Ma sát | tường, vách, nấm lớn 0,22; đinh, mái, đáy V 0 | tường, trần, vai, vách, nấm, cọc 0,22; đinh, mái, đáy két 0. Ma sát bớt tốc tiếp tuyến tới 0,22 × xung pháp tuyến, không quá 1/3 (bi tròn lăn được) |
| Ngưỡng nảy | va dưới 1 u/giây không nảy | dưới 111 |
| Bi va bi | không nảy (vật liệu mặc định) | không nảy |
| Cản | 0,3 | 0,3 |
| Lệch ngẫu nhiên | không | không |
| Trọng lực | 2 u/giây² (222) | **1.100** |
| Kẹp tốc | 4–14 u/giây (444–1.556) | **150–525** (trần gấp 3,5 sàn như máy đó) |

Chép nguyên trọng lực và kẹp tốc thì bi bay trung vị 9,3 giây, 45% số bi quá 10 giây. Mặt máy này có khoảng 85 đinh trên 26 × 38
đường kính bi; máy đó có 22 đinh trên 33 × 50. Bi tốc tối thiểu cao lại trọng lực thấp nên nảy lên trần rồi lơ lửng ở nửa trên.
Đã quét trọng lực 450–1.400 và sàn tốc 150–444: chọn trọng lực 1.100, kẹp 150–525. Bay trung vị 4,9 giây, p90 7 giây, 0,3% số bi
quá 10 giây. Muốn bi bồng bềnh đúng như máy đó thì phải đổi cả mặt máy sang ít đinh to (chưa làm).

Sau khi đổi vật liệu, độ rộng ô và khe két được chỉnh lại (`tune_pachinko.ts`, rồi chọn tay giữa ba bộ lân cận): mọi loại ô lệch
mục tiêu dưới 0,65 điểm. Kinh tế mỗi bi so với số đo trước: EXP −0,3%, bi hoàn −1,7%, thẻ −1,6%.

Lượt đầu (đã thay):

| Thử | Bay trung vị | Ghi chú |
|---|---|---|
| Cũ (nảy 0,5, tường 0,4) | 3,7 giây | |
| Nảy 0,8, trọng lực 700, cản 0,3 | 6,5 giây | quá dài, có bi chạm ngưỡng 14 giây |
| Nảy 0,8, trọng lực 1.000–1.150 | 5,1–5,3 giây | còn dài |
| Nảy 0,65, nấm 0,9, tường 0,7, cản 0,1, kẹp 150–950 | 4,6 giây | chọn ở lượt đầu |
| Hạ trọng lực 850–950 với nảy 0,55–0,62 | 5,0–5,1 giây | nhiều bi lơ lửng trên 10 giây |

Giá trị nằm trong `PHYS` (web) và các hằng `Gravity`, `Drag`, `VMin`, `VMax`, `EPeg`, `Fric`, `VRest`… (C#): giá trị khởi điểm, chỉnh được.

### Hiệu ứng: chép cấu trúc hệ hạt, hình hạt của mình

Số lấy từ prefab hiệu ứng của máy tham khảo: số hạt, đời, tốc, cỡ và màu theo đời, trọng lực, kẹp tốc. Bảng đầy đủ ở
`GD_Claude/07_MayBi.md`, mục "Hiệu ứng chép". Code ở `Game/Machine/MachineFx.cs`.

- **Hình hạt là của mình**, không chép ảnh của họ. Đó là `fx_glow`, `fx_ring`, `fx_sparkle`, `fx_star`, `fx_streak`, `fx_puff` (vẽ bằng `Web/scripts/draw_machine_fx.py`, nằm trong `03 Art/Fallback`). Ảnh gen P4 cùng tên đặt vào `03 Art/Pachinko` sẽ tự thay.
- **Đổi đơn vị:** hiệu ứng theo bi lấy 1 u = 191 px canvas (bi 18 × 1,72 px ứng với 0,162 u). Hiệu ứng ô lấy theo bề rộng ô (ô máy đó 0,9 u); bảng loé rương lấy 0,35 lần.
- **Màu** giữ của họ ở chỗ hợp nền giấy (vàng, cam). Sao ở ô màu xanh lơ thì đổi sang vàng nhạt, nấm lấy màu đỏ của nấm thay cho tím.
- **Hạt UI không có pha cộng màu.** Nền giấy sáng nên vệt bi đặt alpha 0,6 (họ dùng 0,52 trên nền sẫm), chớp trắng đổi sang vàng nhạt.
- **Vệt bi** là `TrailGraphic`: một dải lưới tự dựng (ba làn, mép mờ) qua các điểm mẫu mỗi 0,03 giây. Lúc đầu ghép bằng các đoạn ảnh rời thì bị lên sọc ở chỗ chồng nhau.
- **Nấm thành ảnh động** (`pk_bumper`), ảnh tĩnh mặt máy không vẽ nấm nữa, để nấm phồng xẹp được.
- **Hạt chạy theo giờ máy:** lúc rương vàng làm máy chạy chậm, bộ jackpot cũng chậm theo.
- **Prefab mục mới:** `Items/HatMayBi` (Image) và `Items/VetBiDai` (TrailGraphic), dựng bằng menu `PokiClash/Prefab/Máy bi: hạt hiệu ứng`, nên runtime không sinh đồ vật.

### Két vàng và ô khuất

Két gồm:
- mái hai đoạn từ (230 ± 60, 492) lên (230 ± 12,6, 470), tức khe 25,25 (khoảng 1,4 lần bi);
- đinh gác r 6 ở (230, 446);
- đáy chữ V từ (230 ± 48, 516) xuống (230, 530), hai cọc r 5 ở hai đầu đáy;
- cảm biến chữ nhật 80 × 34 quanh (230, 505).

Hông két để hở, nên thỉnh thoảng bi bật ngang vào được. Đinh trong khung két bị bỏ.

Cảm biến tròn cũ đòi `vy > 0`. Két là chữ nhật: tâm bi lọt vào là tính, vì bi rơi qua khe luôn đi xuống.

Ô vàng khuất (rộng 31) nằm trọn dưới đáy két. Khe giữa đáy két và đầu vách ô khoảng 38 (2,1 lần bi), nên bi chỉ vào khi chui ngang qua đó. Thứ tự 11 ô: gỗ, 15, 5, bi, 10, **vàng**, 10, bi, 5, 15, gỗ.

### Chỉnh độ rộng ô (`scripts/tune_pachinko.ts`)

- Bước 1, cốc: bán kính cốc bạc theo tỉ lệ thuận; khe két theo phần khe trống cho tâm bi (khe − 18).
- Bước 2, ô: tỉ lệ một ô ≈ mật độ × (độ rộng − 18), vì tâm bi chỉ lọt phần ô trừ hai nửa bi ở hai vách. Mỗi vòng nhân phần hiệu dụng theo mục tiêu / đo (mũ 0,7), co giãn chung cho tổng 432, ô tối thiểu 22.
- Hai cách đầu thử đã bỏ: nhân thẳng độ rộng (dao động, ô dưới 18 thì tỉ lệ về 0) và đặt ranh giới theo phân bố x trên đầu vách (vách làm bi dội sang ô bên).
- Tỉ lệ dao động khoảng ±0,5–1 điểm giữa các lần chạy chỉ vì bi va bi (độ lệch chuẩn mẫu khoảng 0,55 điểm cho ô 23% với 6.000 bi). Dừng khi mọi loại lệch dưới 1 điểm.

Kết quả (một lần đo của `export_data.ts`):

| Loại | Cũ | Mới |
|---|---|---|
| Vàng | 3,43% | 3,33% (két 2,2%, ô khuất 1,0%) |
| Bạc | 5,97% | 5,3% |
| Gỗ | 7,47% | 8,67% |
| EXP 15 | 22% | 21% |
| EXP 10 | 22,75% | 23,7% |
| EXP 5 | 29,6% | 29,2% |
| +1 bi | 8,78% | 8,8% |

Kinh tế theo `npm run sim -- pachinko`: 9,39 EXP, hoàn 0,321 bi, 0,086 thẻ mỗi bi (cũ 9,41 / 0,319 / 0,085).

### Web và C# ra cùng từng bit

Trước khi đổi, golden khớp 307/400 bi đầu. Với nảy cao, bi tách sau 5 bi, và vài ô lệch tới 0,86 điểm, sát ngưỡng test. Lần vết từng sự kiện cho thấy chỗ khác đầu tiên ở bit cuối của tốc độ sau va đinh: `Math.cos/sin` của V8 và .NET làm tròn khác nhau.

Góc lệch chỉ trong ±0,18 rad, nên thay bằng đa thức Taylor (sin tới x⁹, cos tới x⁸; sai số dưới 1e-13), viết cùng thứ tự phép tính ở hai bên. Chỉ dùng + − × ÷, là các phép IEEE như nhau trên V8, .NET và Mono. Kết quả: 147.087 sự kiện của 6.000 bi trùng từng bit giữa Node và .NET 9; golden trùng 400/400 bi đầu, cùng số khung và số lần chạm đinh.

Cách kiểm hai bên: `Web/scripts/export_golden.ts` ghi `pachinko.json`; EditMode `PachinkoTests` chạy lại cùng cách thả. Ngoài Unity có thể biên dịch `Core/*.cs` bằng `dotnet` và so (cách làm trong `tasks.md`).

### Ảnh tĩnh mặt máy

Bộ nướng cũ (`Editor/Bake/`) đã xoá theo `convert-to-prefabs`. `scripts/export_board.ts` xuất hình học từ `buildBoard()`, rồi `scripts/draw_machine.py` (PIL, vẽ 4× rồi thu về) vẽ lại cùng nét ảnh cũ: mực (43, 33, 24), đinh có chấm sáng, u tường nâu, nấm đỏ chấm trắng, ô gạch chéo hai mức đậm nhạt, vách đầu tròn. Thêm két vàng và rương trong ô rương. Mặt máy đổi thì chạy lại hai lệnh này.

Prefab nướng sáng ô, nhãn số và 5 rương nhỏ (prefab kit `Ruong`) cho bàn 9 ô. `MachineBoard.Bind` dựng lại theo bàn đang gắn:
- sáng ô: thêm bản sao ảnh đầu nếu thiếu, ảnh thừa tắt;
- nhãn: tìm chữ ở hàng đáy trong nhóm `nhan` theo toạ độ y, đặt lại số, màu, cỡ (13 nếu ô hẹp dưới 30, không thì 17) và vị trí;
- rương nhỏ: một cái giữa mỗi ô rương (cỡ và độ cao của rương ô sẵn có), một cái ở thân mỗi cốc bạc (x·K, −(y+2)·K như bàn cũ), một cái to hơn 1,4 lần giữa két. Ảnh tĩnh không vẽ rương để khỏi trùng.

Đã kiểm bằng lượt thử "PokiClash/Thử/Máy bi" (ảnh `Temp/PokiShots/80–96`): rương cốc vàng cũ không còn, mỗi ô đúng một rương, nhãn giữa ô.

### Cảm giác

| Sự kiện | Hình | Tiếng | Rung |
|---|---|---|---|
| Chạm đinh | loé phồng 1,3 → 1 trong 0,067 giây, mờ 0,25 giây | tối đa 10 lần/giây, 3 cao độ không lặp liền, ±5% cao độ, ±7% to, tối đa 0,6 | rất nhẹ, theo nhịp tiếng |
| Thả bi | | click | nhẹ |
| Ô EXP, +1 bi | sáng ô 0,5 giây, chữ nổi | land / coin | 2 nhịp nhẹ |
| Rương gỗ, bạc | sáng ô 1,1 giây, vòng loé | chest | 3 nhịp, bạc mạnh hơn |
| Rương vàng | chậm 0,3× trong 0,45 giây rồi nhanh dần trong 0,25 giây; mặt máy rung 14 px trong 0,4 giây; vòng loé thứ hai to 1,8; ô sáng 1,6 giây, nhấp nháy 3 lần; chữ to 36 | chest + 3 tiếng xu lên cao dần | ầm tăng dần rồi chốt mạnh |
| Mở rương | lắc gỗ 0,65 / bạc 0,85 / vàng 1,1 giây (vàng lắc mạnh dần) | | gỗ 1 cú, bạc 2 cú, vàng dồn nhịp rồi chốt |
| Lên cấp | | | 2 cú |

Lúc chạy chậm, máng thả ngừng (học "chặn phóng" của ô hiếm), nên bi giữ nút không chồng lên nhau.

Rung (`App/Haptics.cs`):
- Android 8+ dùng `VibrationEffect.createWaveform` có biên độ, mỗi bậc có khoảng chặn riêng.
- Android cũ và iOS chỉ có `Handheld.Vibrate` (một cú dài), nên chỉ dùng ở bậc rương vàng. Rung iOS có cường độ cần plugin native, để sau.
- Bật tắt bằng nút **Rung** trong Sổ tay (`settings.haptics`, mặc định bật, bản lưu cũ thiếu trường này đọc ra bật). Bật lên thì rung thử một cú. Dòng nút thêm vào prefab bằng menu `PokiClash/Prefab/Sổ tay: thêm dòng Rung`: nhân bản dòng "Âm thanh", nút dựng lại từ đúng prefab kit với cùng chỉnh sửa (giữ liên kết kit), gán `NotebookScene.p.haptics`.

## Risks / Trade-offs

- **[Bảng tỉ lệ đổi số]:** vàng 3,43 → 3,33%, gỗ 7,47 → 8,67%… Mỗi lần đo là một mẫu 6.000 bi nên số in lệch mục tiêu tới khoảng 1 điểm. Kinh tế mỗi bi gần như không đổi.
- **[Đợt dài hơn]:** bay trung vị 4,6 giây (cũ 3,7), cộng thêm 0,7 giây chậm khi ra rương vàng (khoảng 3% số bi).
- **[Hai phiên làm song song]:** khi viết change này có phiên khác xuất dữ liệu boss tiến hoá. Chỉ vá khối `pachinko.measured` trong `balance.json` và `Golden/pachinko.json`; JSON và golden khác do phiên kia xuất.

## Open Questions

- Ô vàng khuất có nên cho thưởng lớn hơn rương vàng thường (ví dụ rương vàng ×2) để đúng nghĩa "siêu hiếm" không? Hiện cả két và ô khuất đều ra rương vàng.
