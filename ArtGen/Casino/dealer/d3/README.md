# D3: lều Đêm Bài có Lão Mực (GD_Claude/31 mốc D3, 2026-11-26)

Hình (Magnific GPT 2.6 1k high, ảnh mẫu `../A_canh_ban_bai.png` + `ArtGen/Islands/refs/world_style.png`; 95 + 95 + 72 = 262 credit):

| File | Là gì |
|---|---|
| `nen_leu_bai_1k.png` → `nen_leu_bai_2k.jpg` | nền lều nhìn từ ghế người chơi, dọc 9:16, KHÔNG có dealer, nỉ trống, khay chip ở mép bàn sau; phóng classic 2k (Art) |
| `do_ban_1k.png` | tờ đồ bàn nền trắng: lưng bài, mặt bài trắng, cỗ bài, 4 chip đơn, 2 chồng chip |
| `tach_lop.py` | tách nền 2k thành `nen_leu_bai.jpg` (cả ảnh) và `ban_leu_bai.png` (vành bàn + khay + nỉ, đè hông Lão Mực); đường cắt bám mép trên nét mực, đo tay (bảng `TOP`); `tach_lop_xem.png` để soi |
| `cat_do_ban.py` | cắt tờ đồ bàn ra `do_ban/*.png` (nền trong suốt) |
| `dua_vao_unity.py` | chép vào `Assets/03 Art/Casino/Leu/bj_*` (lớp bàn cắt từ hàng 840, bài / chip thu về ~2 lần cỡ hiện) và rig `../atom/export/lao_muc.atomik` → `Assets/03 Art/Casino/Dealer/lao_muc.bytes` |
| `loc_d3.py` | bản dịch tiếng Anh câu thoại mới (chỉ thêm khoá vào `Resources/Loc/en/ui.json`); `--thieu` in chuỗi còn thiếu |
| `lam_gif.py` | ghép khung lượt chụp (`Temp/PokiShots/casino_bj_dealer/`) thành `van_bai.gif` + `van_bai_to.jpg` |

Bố cục bàn (khớp `CasinoTablesMenu.BuildBlackjack` và `../rig/clip_d3.py`): sân khấu 1080 x 1920, ảnh nền rộng 1080 (0,944 lần ảnh 2k), mép trên
ở y −150, nên mép bàn sau (y 900 trong ảnh 2k) ở y −1000; Lão Mực tỉ lệ 0,79, gốc rig ở y −1395 (mép bàn rig y 500). Điểm sân khấu (x, y) ↔ rig
(x / 0,79, 500 − (−y − 1000) / 0,79). Ô cược (0, −1300) trùng `CHIP` (0, 120) của clip D2 nên `take` / `pay` không phải nướng lại.

Rig: slot `la_cam` (lá trên tay phải) thêm bằng `../rig/them_la_bai.py`; clip chia bài ở `../rig/clip_d3.py` (`deal`, `deal_self`, `peek`,
`reveal`, `bust_self`), nướng bằng `../rig/hoat_anh.py`, xem bằng `../rig/xem_d2.py <clip>` (ra `../d2/`).
