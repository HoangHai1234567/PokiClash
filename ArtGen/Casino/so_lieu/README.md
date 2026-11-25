# Số liệu đảo Casino (GD_Claude/29_DaoCasino.md)

Chạy ngoài Unity (csc + mono đi kèm Unity 6000.0.73f1), Python `py -3 -I`.

| Script | Việc |
|---|---|
| `gen_casino.py` | Sinh khối `casino` của `balance.json` (cá, lịch sự kiện, bàn, cúp, chợ, 14 ngày đội ngầm). `py -3 -I gen_casino.py --apply "<đường dẫn>/Assets/02 Data/Json/balance.json"` rồi menu `PokiClash/Nhập dữ liệu`. Cấp, sao từng đội ngầm đọc từ `ug_levels.json` |
| `build.py run <việc>` | Biên dịch Core từ Assets, chép JSON vào `out/data`, áp `gen_casino.py`, chạy `runner/Program.cs`. Việc: `bj`, `rl`, `slot` (hoàn trả), `race` (đua 3–5 tướng: tỉ lệ về nhất theo cổ vũ và số tướng, lời / lệ phí, số cú húc, số lần mình bị choáng), `ug [n]` (tỉ lệ thắng đội ngầm), `ugcal [n]` (dò cấp đội ngầm theo tỉ lệ thắng mục tiêu, ghi `ug_levels.json`), `fish`, `mk`, `ev`, `save` |
| `build.py tests CasinoTests.cs` | Chạy test NUnit ngoài Unity (`nunit_shim/` thay `TestData`) |
| `tune_slots.py` | Tính chính xác hoàn trả máy quả trên mọi tổ hợp dừng để chọn dải cuộn / bảng trả |
| `kiem_bien_dich.py game editor` | Biên dịch thử assembly Game / Editor theo csproj Unity sinh (file nháp đặt trong `overlay/`; lấy cả file .cs mới chưa có trong csproj) |
| `loc_missing.py [file.cs ...]`, `loc_add.py` | Liệt kê chuỗi chưa dịch của phần Casino; gộp bản dịch tiếng Anh vào `Assets/Resources/Loc/en` |
| `patches.py` | Các sửa nhỏ vào file có sẵn đã áp (để biết đã đổi gì) |
