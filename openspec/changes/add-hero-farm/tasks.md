## 1. Logic (C# thuần)

- [x] 1.1 `Core/Farm.cs` (chép `Web/src/core/farm.ts`, `data/farm.ts`): 8 chỗ theo thứ tự mở (Ao vịt Thủy, Ruộng rau Thổ, Vườn cây Mộc, Lò bánh Hỏa, Xưởng nông cụ Kim, rồi Ao vịt, Ruộng rau, Vườn cây lần hai); năng suất = 1,2 bi/giờ × sức độ hiếm × (1 + 5%·(cấp − 1)) × (1 + 10%·(sao − 1)), đúng hệ ×1,25; giờ làm = 2 + 0,5·(sao − 1) + 0,5·độ hiếm; đồng hồ theo đoạn như AFK (lùi giờ máy thì bỏ qua đoạn đó); kho mỗi chỗ chặn ở 12 giờ sản lượng; thu hoạch lấy phần nguyên, giữ phần lẻ
- [x] 1.2 Rút tướng (nghỉ = giờ làm × 15 phút, kẹp 15–60 phút, rút giữa ca vẫn nghỉ đủ; bi tích vẫn ở chỗ), đặt tướng (chặn tướng đang làm chỗ khác hoặc đang nghỉ), tự xếp (lặp chọn cặp chỗ trống – tướng rảnh có năng suất cao nhất)
- [x] 1.3 Lưu khoá `farm` (giờ tính, hết tăng tốc, 8 chỗ, giờ hết nghỉ của từng tướng). Lúc thêm không cần bước di chuyển: bản lưu cũ thiếu khoá thì tạo mới khi vào. Bộ đếm quảng cáo riêng của trang trại sau đó dồn về `ads` ở bước v2 → v3 (`add-monetization-hooks`). Mở khi có từ 3 tướng; lúc mở có 3 chỗ, chỗ 4–8 mở ở cấp 8, 11, 14, 17, 20
- [x] 1.4 EditMode (`FarmTests`): golden `farm.json` 24 bước (đặt, rút, tính giờ, thu hoạch, tự xếp, tăng tốc, lùi giờ, tua) khớp web từng giá trị; công thức ví dụ trong design (Tiểu Y cấp 5 ở Ao vịt 1,8 bi/giờ, 2 giờ làm, nghỉ 30 phút); hết sức thì ngừng (vắng 8 giờ vẫn chỉ có 2 giờ sản lượng); đang làm hoặc đang nghỉ thì không vào chỗ khác, nghỉ đủ mới vào lại; lưu rồi đọc lại

## 2. Giao diện

- [x] 2.1 Công trình Trang trại trên sảnh: nét chì kèm "Có 3 tướng để mở Trang trại" khi chưa mở; mở thì vào scene `Farm`; chấm đỏ khi có tướng hết sức, kho đầy, hoặc vừa mở mà chưa đặt tướng
- [x] 2.2 Scene Trang trại (`App/Scenes/FarmScene.cs`, `Farm.unity`, đã thêm vào Build Settings): 8 chỗ (icon loại chỗ, hệ hợp, sticker tướng nhún khi làm / ngồi khi hết sức, vòng sức còn, bong bóng bi tích, "Mở ở cấp n" với chỗ khoá), "Thu hoạch (n)", "Tự xếp", "×2 năng suất" (quảng cáo `farm_boost`, 1 giờ). Chưa có ảnh đảo trang trại nên các chỗ xếp lưới 2 cột trên nền trời
- [x] 2.3 Danh sách chọn tướng cho một chỗ (bi/giờ, giờ làm, hợp hệ, "Đang làm ở …", "Nghỉ còn n phút"), tướng đang làm ở chỗ này và nút "Rút ra"
- [ ] 2.4 Thay lưới bằng ảnh đảo trang trại (`ArtGen/SideMeta`) và đặt 8 chỗ theo toạ độ `FARM_SPOTS` khi có ảnh

## 3. Kiểm tra

- [x] 3.1 Công cụ cân bằng: menu `PokiClash/Cân bằng nhanh/Trang trại: bi mỗi ngày so với AFK`; mô phỏng tiến độ 30 ngày có thêm lượt vào trang trại. Số đo (vào 2 / 4 / 8 lần mỗi ngày): đầu game (4 tướng, cấp 9) 19 / 38 / 55 bi so với AFK 201–243; giữa game (8 tướng, cấp 18) 93 / 169 / 230 so với 451–546; cuối game (11 tướng, cấp 28) 252 / 392 / 515 so với 700–850. 30 ngày người chơi "vừa": trang trại 10.952 bi, AFK 51.050, ải 5.822
- [x] 3.2 Play (`PokiClash/Thử/Trang trại: tự xếp, tua giờ, thu hoạch, đổi ca`): tự xếp 4 tướng vào 4 chỗ đã mở, sau 3 giờ thu hoạch 22 bi (giữ phần lẻ), đổi ca Ao vịt (tướng rút ra nghỉ 45 phút, không ảnh hưởng đội), bật ×2 năng suất; console không lỗi
