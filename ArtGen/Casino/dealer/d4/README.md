# D4: lều Vòng Xoay Ngũ Hành có Lão Mực (GD_Claude/31 mốc D4, 2026-11-26)

Người dùng: "làm phần roulette đi, làm kĩ, lấy nhân vật đen kia vào, làm việc thả bóng nhìn thật và có vật lý hơn nhưng mình phải kiểm soát
được tỉ lệ ra".

## Ô ra do lõi chọn, vật lý chỉ diễn

- `Roulette.Spin` chọn ô (`Roulette.Pick`): 26 ô đều nhau, hoặc theo `casino.roulette.weights` (26 số) nếu đặt trong `balance.json`
  (qua `ArtGen/Casino/so_lieu/gen_casino.py`). Hoàn trả ghi trong Cách chơi tính theo đúng trọng số (`Roulette.RtpRange`).
- `Core/Casino/RouletteBall.cs` mô phỏng viên bi (bi tì vách đường chạy, ma sát lăn + cản khí, rời vách khi lực ly tâm không thắng nổi dốc,
  xoáy xuống sườn dốc, va 8 mấu chắn, lên mâm đang quay, nảy qua vách ngăn 26 ô, bị mặt mâm "bắt", lắc trong ô rồi nằm yên).
  `RouletteBall.Plan(vị trí, góc mâm, ...)` thử các cú thả với lực thả ngẫu nhiên trong khoảng tự nhiên (10,4–12,6 rad/s) tới khi mô phỏng
  cho bi nằm đúng ô lõi chọn (lệch tối đa 3 ô thì lùi pha mâm đúng số ô đó: bánh xe đối xứng theo từng ô nên đường đi y nguyên), rồi ghi
  lại đường đi (120 mẫu/giây) cho màn phát lại. Không có khung nào kéo bi.
- Đo (`sim/chay.py stats`, 4.000 cú thả tự do + 1.040 cú theo ô chọn): bi luôn nằm yên; mỗi cú 4,6–7,5 giây (rời vách ~3,6 giây,
  ~4,7 vòng, ~1,2 lần va mấu, 0–6 lần nảy qua vách); `Plan` trung bình 9 cú thử, nhiều nhất 68, ~4 ms; sai ô: 0.

## File

| File | Là gì |
|---|---|
| `bo_cuc_nen.png` | phác khối bố cục gửi làm ảnh mẫu 1 (lều 1/3 trên, mép bàn + khay chip, nỉ 2/3 dưới) |
| `nen_leu_xoay_1k.png` → `nen_leu_xoay_2k.jpg` | nền lều nhìn từ ghế người chơi (Magnific GPT 2.6 1k high 95 credit, ảnh mẫu 2 là nền lều Đêm Bài; phóng classic 2k Art 72 credit) |
| `tach_lop.py` | tách thành `nen_leu_xoay.jpg` + `ban_leu_xoay.png` (thanh gỗ mép bàn + khay + nỉ, đè hông Lão Mực); cung mép bàn đo tay; `tach_lop_xem.jpg` |
| `ve_banh_xe.py` | vẽ bánh xe bằng mã, đúng hình học của mô phỏng (`RouletteWheel`): `ra/rl_chao.png` (lòng chảo chiếu nghiêng), `rl_vanh_truoc.png` (nửa vành gần, đè lên bi), `rl_mam.png` (mâm 26 ô nhìn từ trên, game xoay + ép dẹt), `rl_truc.png`, `rl_bi.png`, `banh_xe.json`; `xem_banh_xe.png` để soi |
| `sim/chay.py`, `sim/Harness.cs`, `sim/xem_bi.py` | đo và soi mô phỏng bi ngoài Unity (`stats`, `dump <ô> <hạt giống>` rồi `xem_bi.py [gif]`) |
| `ma/` | mã của mốc: `RouletteBall.cs`, `RouletteScene.cs`, `CasinoRouletteTour.cs`, khối `BuildRoulette`, test; `va_ma.py overlay / apply / clean` vá từng đoạn vào file dùng chung |
| `dua_vao_unity.py` | chép hình vào `Assets/03 Art/Casino/Leu/rl_*`, rig vào `Assets/03 Art/Casino/Dealer/lao_muc.bytes` |
| `loc_d4.py` | bản dịch tiếng Anh chuỗi mới (chỉ thêm khoá) |
| `lam_gif.py` | ghép khung lượt chụp (`Temp/PokiShots/casino_rl_dealer/`) thành `vong_xoay.webp` + `vong_xoay_to.jpg` |
| `rl_*.gif`, `rl_*_to.png`, `lon/` | ảnh duyệt 5 clip mới của Lão Mực (`../rig/clip_d4.py`) |

## Bố cục (khớp `RouletteScene` và `CasinoTablesMenu.BuildRoulette`)

Sân khấu 1080 x 1920, gốc mép trên giữa. Ảnh nền 1144 x 2048 hiện đúng cỡ, mép trên ở y +105 nên hàng 755 của ảnh (mép bàn) ở y −650.
Lão Mực tỉ lệ 0,70, gốc rig y −1000: sân khấu (x, y) ↔ rig (x / 0,7, 500 − (−y − 650) / 0,7). Ô gom chip (0, −916) = `CHIP` của rig, khay
(116, −678): `take`, `pay` dùng nguyên. Bảng cược x ±450, y −775..−1250 (góc Sao Vàng, hàng đầu 5 cửa Số, cột đầu 5 cửa Hệ, 25 ô đơn).
Bánh xe: tâm mặt phẳng ô (0, −1500), bán kính vành 320; chiếu x = R·x, y = R·(0,6·y + 0,8·(độ cao + độ nảy + bán kính bi)).
Mâm quay ngược chiều kim đồng hồ, bi chạy theo chiều kim đồng hồ, vào đường chạy ở góc 40°.
