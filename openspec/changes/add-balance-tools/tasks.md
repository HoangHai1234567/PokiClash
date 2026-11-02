## 1. Golden

- [x] 1.1 `Web/scripts/export_golden.ts` gom mọi bộ đối chiếu vào `Assets/02 Data/Golden/`: số ngẫu nhiên, mô tả thẻ, 200 trận (12 trận đủ từng sự kiện), chỉ số và tiến trình, thưởng ải và rương mốc, máy bi, AFK, bảng 40 ải (`sim.json`)
- [x] 1.2 EditMode test đọc golden, báo trận và sự kiện đầu tiên lệch (có từ mốc 1)

## 2. Cửa sổ Cân bằng (`Editor/BalanceWindow.cs`, menu `PokiClash/Cân bằng`)

- [x] 2.1 Tab Trận: một ải / một đảo / cả 40 ải; đội gợi ý theo đảo (như web) hoặc tự chọn 3 tướng, sao, cấp thẻ; 5 mức cấp quanh khoảng đề nghị hoặc tự nhập; phần cộng side meta (% máu, công, thủ); số trận mỗi ô; bảng tô màu; xuất CSV (`Logs/CanBang`)
- [x] 2.2 Tab Máy bi: độ rộng 9 ô sửa được, mô phỏng 6.000 bi, tỉ lệ theo loại và theo chỗ rơi, giá trị rương, EXP / bi hoàn / thẻ mỗi bi; cảnh báo khi bi hoàn > 0,5; ghi tỉ lệ vào asset BalanceConfig (chỉ khi dùng độ rộng gốc; số gốc vẫn do `export_data.ts` đo)
- [x] 2.3 Tab Tiến độ: 3 kiểu người chơi (sửa được) × 30 ngày; cấp theo ngày, ngày chinh phục đảo, ngày đạt cấp đề nghị; đảo chưa xong ghi "NGOÀI TẦM"; xuất CSV. Logic ở `Core/ProgressSim.cs` (AFK, rương AFK, quảng cáo, đánh ải với tỉ lệ máy + 15%, đánh lại khi ải kế quá khó, thả hết bi, nâng thẻ, tiến hóa)
- Thêm: menu `PokiClash/Cân bằng nhanh/...` chạy bảng 40 ải (CSV) và tiến độ 30 ngày (Console) không mở cửa sổ

## 3. Sổ tay bản dev (`App/Dev/NotebookDev.cs`)

- [x] 3.1 Mục "Bảng thử" (+50 bi, +500 XP, tua AFK 1/8 giờ, mở hết tướng/ải, +5 bản sao; xoá dữ liệu ở phần cài đặt). Tua giờ trang trại và +10 đá thêm khi có `add-hero-farm`, `add-potential-stones`. Bọc `#if UNITY_EDITOR || DEVELOPMENT_BUILD` (không dùng `POKICLASH_DEV` vì define đó gắn với hình aola)
- [x] 3.2 Mục "Chỉnh số": 16 hệ số (như bảng của web), nút − / +, số đã đổi tô đỏ, có hiệu lực ở trận sau, "Về số gốc" nạp lại từ asset
- [x] 3.3 Mục "Máy tự chơi" 100 trận với đội và cấp hiện tại, chọn ải bằng « »
- Sổ tay cuộn dọc

## 4. Ghi trận

- [x] 4.1 Ghi `Logs/tran.csv` của project mỗi trận (thời điểm, đảo, ải, đội, cấp, kết quả thắng/thua/bỏ, hiệp, giây thật, máu còn %, tự chơi); máy thật ghi vào `persistentDataPath/Logs`; chỉ Editor và bản Development

## 5. Kiểm tra

- [x] 5.1 Bước kiểm tra trước build: mọi file `App/Dev/*.cs` phải bọc kín; test EditMode cùng điều kiện; menu `PokiClash/Biên dịch thử bản phát hành` (đã chạy: đạt)
- [x] 5.2 Chạy trọn bảng 40 ải và so với `npm run sim -- battle`: 50 trận mỗi ô, 200/200 ô trùng; test EditMode so golden 6 trận mỗi ô
- [ ] 5.3 Phần cộng side meta thật (huy hiệu, đá tiềm năng, trang trại) vào tab Trận và Tiến độ khi các change đó xong
