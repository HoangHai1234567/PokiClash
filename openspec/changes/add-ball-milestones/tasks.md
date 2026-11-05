## 1. Học máy tham khảo

- [x] 1.1 Đọc bản đục Critters: `pbui_pinball_multi_popup` ("mốc tiếp theo: mở khi có 8000 bi"), `pbui_pinball_level_bar` (mốc nhỏ dọc thanh), `pbui_drop_egg_tips` (trứng 2/3, đếm ngược), clip `anui_pinball_bottom_slider_add` (nền và phần đầy cùng nhún). Ngưỡng cược theo bi lấy từ wiki và guide.
- [x] 1.2 Dựng lại ảnh các phần đó từ prefab và sprite: `D:\CrittersRipper\analysis\ui_shots\` (`sheet.png`), script `analysis/uirender.py`, `analysis/shots.py`. Chỉ để tham khảo, không đăng.

## 2. Luật (Core)

- [x] 2.1 `XStep.balls` thay `lv`, `Progress.XAllowed` theo bi đang có, `Progress.XBest`.
- [x] 2.2 `GiftStep`, `BalanceConfig.gifts`; `Pachinko.GiftNow/GiftAt/GiftCredit/GiftAdd/GiftName`; bản lưu `gift`, `giftTier`.
- [x] 2.3 `ProgressSim` tính mốc quà (rương mốc mở ngay như rương ô).
- [x] 2.4 `balance.json`: `xSteps` (×3 150, ×5 300, ×10 700), `pachinko.gifts` (5 mốc). Ngoài Unity (`dotnet`): ngưỡng và vòng mốc đúng, bản lưu đọc ghi giữ mốc.

## 3. Màn Máy bi (Unity)

- [x] 3.1 `MachineScene`: nút cược khoá theo bi (mờ, "n bi", chạm báo), mở thêm mức thì báo và nhún, tụt ngưỡng thì hết đợt về mức cao nhất còn mở; hộp "Lên cấp!" bỏ dòng mở nút.
- [x] 3.2 Thanh mốc: mốc Huyền thoại rồi mốc quà, ô quà (rương kit hoặc icon + số), nhận quà (đứng đầy, nhún, loé, quà bay), chạm báo ba mốc kế; bảng tỉ lệ ghi mốc quà và ngưỡng cược.
- [x] 3.3 `MachineExpBar`: khung `khung_thanh` nhún theo dáng Critters, chữ nhún thêm; `FlyIcon`, `Burst` cho mốc quà (hạt từ kho `Items/HatMayBi`, không sinh đồ vật).
- [x] 3.4 `ArtGen/Pachinko/cat_ranh.py` cắt rãnh → `pk_ranh_exp.png`; menu "Máy bi: thân máy vẽ tay" dựng `khung_thanh`; menu mới "Máy bi: mốc quà" dựng `o_qua`. Đã chạy cả hai menu.

## 4. Kiểm

- [x] 4.1 Test `CuocMoTheoSoBiDangCo`, `MocQua_SauHuyenThoai_TinhTheoBiVaVongLai`. EditMode 99/99 đạt.
- [x] 4.2 Tour Play "PokiClash/Thử/Máy bi: mốc quà, cược theo số bi": ảnh `Temp/PokiShots/140–152`. Thấy rõ ×3 khoá "150 bi" và báo khi chạm; mở ×3 khi đủ bi; rãnh nhún cùng thanh; rương mốc bay vào khay; ô quà đổi sang "+8"; nhận bi và XP; tụt ngưỡng về ×2; báo ba mốc kế. Console không lỗi.
- [ ] 4.3 Thử trên điện thoại Android: chữ "n bi" trên nút cược nhỏ (cột đã thu 0,82) có đọc được không; ô quà và số "+120" có rõ không; nhịp nhún rãnh khi "Thả liền" có dày quá không.
- [ ] 4.4 Chủ dự án chốt số: ngưỡng cược (150/300/700), bảng mốc quà (30–80 bi, có cần mốc ngắn hơn cho người mới không).

## 5. Để sau

- [ ] 5.1 Bản web (`Web/src/core`) vẫn mở cược theo cấp. Chỉ làm khi chủ dự án dặn.
- [ ] 5.2 Mốc nhỏ dọc thanh kinh nghiệm như thanh cấp Critters (icon hệ, tới mốc thì thưởng). Chưa làm vì chưa có thưởng theo hệ.
