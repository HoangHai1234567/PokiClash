# Giả lập kinh tế 300 người chơi (GD_Claude/33_CanBangKinhTe.md)

Chạy ngoài Unity (csc + mono đi kèm Unity 6000.0.73f1), Python `py -3 -I`. Lõi game biên dịch thẳng từ `Assets/01 Script/Core`
(đúng như trên đĩa, không overlay), dữ liệu lấy từ `Assets/02 Data/Json`. Không ghi gì vào `Assets`.

| File | Việc |
|---|---|
| `runner/EconSim.cs` | Một người chơi ảo: ải, AFK, cây bi, ruộng Nhà, máy bi, cửa hàng + Offer Engine, quảng cáo thưởng, đảo Casino. Luật gọi thẳng lõi game; "người chơi làm gì" là giả định (lớp `Persona`, các hàm `WantOffer`, `Shopping`, `CasinoVisit`) |
| `runner/Program.cs` | `Make(id)`: 300 người = 3 mức chơi × 5 nhóm tiền × (không ra đảo / có ra đảo) × 10. Ghi `out/res/<bộ số>/p<id>.json` |
| `bo_so/<tên>.py` | Một bộ số: hàm `patch(b)` sửa dict `balance.json`. Khối `b["sim"]` là luật cần sửa code game, runner giả lập trước (`SimRules`) |
| `build.py` | Biên dịch Core + runner, sinh `out/data/<bộ số>/` |
| `chay.py <bộ số> ... [--lam-lai]` | Chạy 300 người mỗi bộ, tối đa 6 tiến trình (giới hạn CPU người dùng dặn 2026-11-26), chạy tiếp được |
| `tong_hop.py <bộ số> ...` | Bảng theo nhóm: tiến độ, bi theo nguồn, đảo theo trò, mảnh, đá, quảng cáo, IAP, điểm nghẽn, popup |
| `so_sanh.py <bộ số> ...` | So các bộ số cạnh nhau |
| `pha_dao.py <bộ số> ...` | Thời gian xong 350 ải (bộ chạy 90 ngày) |
| `ket_qua/` | Bảng của các lượt chạy (2026-11-26: trước khi sửa game; `*_G30_*`, `*_G90_*`: game đã sửa 2026-11-26) |
| `kiem_test.py [--nhap <thư mục>]` | Chạy bộ test NUnit của game ngoài Unity (file test cần UnityEngine thì bỏ) |
| `tinh_golden.py [--nhap <thư mục>]` | Tính lại golden rương máy bi, AFK, trang trại... bằng đúng mã `Editor/GoldenFixtureMenu.cs` |
| `kiem_app.py [--nhap <thư mục>]` | Biên dịch thử assembly Game + Editor ngoài Unity (bản nháp đè file cùng đường dẫn) |
| `kiem_dich.py [--nhap <thư mục>]` | Soát đủ bản dịch tiếng Anh cho chuỗi `Loc.T/F` và tên, mô tả gói |
| `unity_mcp.py`, `unity_cho.py`, `unity_test.py` | Gọi Unity qua cầu nối MCP cổng 8080: trạng thái, refresh khi rảnh, chờ biên dịch (đọc Editor.log), chạy test EditMode |

**Từ 2026-11-26 game đã mang các sửa của GD_Claude/33 đợt 1–3 và đường EXP hai đoạn (GD_Claude/34).** `goc` nay là game đã sửa; các bộ số
dưới đây viết cho game TRƯỚC khi sửa, đã cất vào `bo_so/cu_truoc_1126/` (kết quả của chúng còn ở `out/res/<tên>/` và `ket_qua/`, muốn chạy
lại phải lấy Assets ở commit 655e6e75). Kết quả thô của `goc` cũ đã bị chạy đè ngày 2026-11-27 (bảng của nó còn ở `ket_qua/tong_hop_goc.md`,
`so_sanh*.md`); đừng chạy `chay.py goc --lam-lai`, đặt bộ số tên riêng cho mỗi lượt. Bộ không sửa gì, mỗi bộ là game tại một thời điểm:
`G30_game_moi`, `G90_game_moi` (sau đợt sửa 2026-11-26), `J1_vuot_moc` (thêm Gói Vượt Mốc), `J2_nap_dau_lo_bi` (thêm nạp đầu 3 bậc, Lọ Bi
7 ngày: game hiện tại). Bộ thí nghiệm vòng 1 (gói tướng có / không giãn sức): `H1_goi_khong_gian`, `H2_gian_moc`, `H3_gian_moc_goi`.
`moc_ai.py <bộ số> ...` in ngày tới từng mốc số ải; `sim.exe jump goc` (chạy trong `out/`) in Gói Vượt Mốc theo cấp và mốc.
Các luật trước đây runner tự mô phỏng (`sim.replayFull`, `noAdsInstant`, `piggyGapDays`, `reliefFix`) nay là luật thật trong lõi, runner gọi thẳng.

Bộ số 30 ngày cũ (GD_Claude/33): `goc` (game hiện tại), `A_khoa_ban_the` (chỉ tắt bán thẻ thừa), `B_de_xuat` (đề xuất), `C_siet_them` (B + siết bi thụ động 25%).

Bộ số 90 ngày cũ (GD_Claude/34, chạy với `--ngay 90`): `B90` (mốc), `D_exp_doc` (EXP 9 × cấp^1,54), `E_boss_manh` (D + boss mạnh, không có tác dụng),
`K0_gian_moc` (D + sức tướng theo mốc + địch theo mốc), `K*` / `L*` (K0 + giả lập gói tướng; chỉ cần nhóm không trả tiền: `--nhom 0,1`).
`pha_dao.py <bộ số> ...` in thời gian xong 350 ải; `sim.exe dbg <bộ số> <đảo>` in tỉ lệ thắng từng ải theo tướng mốc và cấp.

Thử nghiệm sức theo mốc cần luật chưa có trong game: `build.py` vá BẢN SAO Core trong `stage/` (`stage_patch`: `HeroStats.HeroMult`), không đụng Assets;
bộ số có hàm `patch_stages` thì sửa cả bản sao `stages.json`.

Lưu ý:
- Người chơi ảo cầm quá 1 triệu bi thì coi là vỡ kinh tế: dừng người đó, ghi `brokenDay`. Trần 300 giây CPU mỗi người (`timedOut`).
- Rương mốc quà và rương vòng nấm của máy bi không nhân mức cược (như `MachineScene`); runner từng nhân nhầm, làm bi phình giả.
- Chưa mô phỏng: Đền Huy Hiệu, Hang Tiềm Năng (đá cộng gần đúng theo cấp, `ProgressSim.SideEvo`), công trình Nhà ngoài cây bi và ruộng (dùng mô hình trang trại cũ), bỏ game giữa chừng.
