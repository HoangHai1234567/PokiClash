## 1. Logic (C# thuần)

- [x] 1.1 `Core/Potential.cs` (chép `Web/src/core/potential.ts`, `data/potential.ts`): bảng dòng (8 loại × 5 độ hiếm), quay theo hạt giống (loại đều nhau, độ hiếm 55 / 28 / 12 / 4,5 / 0,5), khoá ô (tối đa 2, chỉ tính ô đã mở và có dòng), giá (ô quay 1 đá, ô khoá +2), cặp cũ/mới (kết quả chờ chọn lưu trong bản lưu), giữ mới / giữ cũ, trần tổng mỗi loại (+40%, Tốc +30, mana và nộ +50)
- [x] 1.2 Công, Thủ, Máu, Tốc vào `StatMods` (cộng chung với huy hiệu) nên thấy ở màn Tướng, trận, công cụ cân bằng; mana và nộ cộng lúc dựng tướng; chí mạng và hút máu thành buff cả trận (`BattleStart` trên `Member`, áp ở `MakeFighter` cả web và Unity). Hút máu dùng buff chung nên tính cho mọi đòn, không chỉ đánh thường
- [x] 1.3 Dòng đá trong rương bạc (8%, 1–2) và vàng (12%, 2–4), các dòng cũ giữ trọng số tương đối; rương AFK thêm 5% "1 đá"; ×N nhân số đá. Tỉ lệ ô của máy không đổi (mặt máy giữ nguyên); bảng "Tỉ lệ" đọc bảng rương mới
- [x] 1.4 Hang: 4 tầng, đội địch (1 boss, 1 tướng phụ cùng hệ, cấp theo tầng), hệ boss theo thứ trong tuần (Thứ Hai Kim … Thứ Sáu Thổ; Thứ Bảy và Chủ nhật người chơi chọn), 3 lượt thắng mỗi ngày (chỉ trừ khi thắng), +1 lượt bằng quảng cáo, thưởng đá
- [x] 1.5 Lưu `potentialStones`, `heroes[id].potential`, `heroes[id].potentialNew`, `cave` (ngày, số lần thắng, đã xem quảng cáo, hệ chọn). Không cần bước di chuyển phiên bản: khoá mới, bản lưu cũ thiếu khoá thì mặc định trống

## 2. Giao diện

- [x] 2.1 Hộp chi tiết tướng có dải "Tiềm năng" (4 ô nhỏ, tổng phần cộng, nút "Khai phá") mở hộp Tiềm năng (`Game/Potential/PotentialPanel.cs`): 4 ô màu theo độ hiếm hoặc "Mở ở n sao", khoá từng ô, số đá, "Khai phá (n đá)" hoặc xám "Cần n đá", tổng; hộp "Kết quả khai phá" so sánh cũ/mới, bắt buộc chọn "Giữ mới" / "Giữ cũ". Dải thay vì mục đầy đủ vì hộp chi tiết đã gần hết chiều cao màn
- [x] 2.2 Công trình Hang Tiềm Năng trên sảnh: nét chì khi chưa mở, mở thì vào scene `Cave`
- [x] 2.3 Scene Hang (`App/Scenes/CaveScene.cs`, `Cave.unity`): hệ boss hôm nay (hoặc hàng chọn hệ cuối tuần), số đá, lượt còn, "+1 lượt" (quảng cáo giả lập); 4 tầng (cấp đề nghị, đá thưởng, boss và tướng phụ, "Vào"); hộp chuẩn bị dùng chung (`StagePrep.OpenCave`); kết trận: đá, lượt còn, "Đánh tiếp" / "Đánh lại" / "Về Hang"

## 3. Kiểm tra

- [x] 3.1 EditMode (`PotentialTests`): tỉ lệ độ hiếm và loại trên 100.000 dòng; 60 lần khai phá có khoá và giữ mới/cũ khớp web; trần tổng; phần cộng và hiệu ứng đầu trận khớp web; 6 trận thật có hiệu ứng đầu trận khớp web; Hang (đội địch, thứ, lượt, đá) khớp web; lưu rồi đọc lại. Golden máy bi và AFK xuất lại với bảng rương mới. Test asset dữ liệu kiểm tra thêm mọi cấu hình side meta qua được ScriptableObject
- [x] 3.2 Công cụ cân bằng: lựa chọn "Tiềm năng mọi tướng" (không / trung bình / trần) ở tab Trận; menu `PokiClash/Cân bằng nhanh/Tiềm năng: đảo Mộc và Thổ`. Đảo Thổ ở cấp 21: không 62%, trung bình 61%, trần 81%
- [x] 3.3 Play (`PokiClash/Thử/Tiềm năng: đá từ máy bi, khai phá, Hang`): 20 rương vàng ra 6–8 đá, khai phá 3 ô tốn 3 đá (giữ mới), khoá 1 ô tốn 4 đá (giữ cũ, dòng không đổi), tướng vào trận có phần cộng, Hang tầng Dễ: thắng +2 đá và trừ 1 lượt, thua không mất lượt; console không lỗi
- [ ] 3.4 Thay icon đá, khung ô tiềm năng, nền Hang, công trình Hang bằng ảnh gen khi có (`ArtGen/SideMeta`, `ArtGen/Hub`)
