# Báo cáo VFX hệ Thủy (2026-11-18)

File đã sửa: `Assets/01 Script/Game/Battle/HatNuoc.cs` (bản làm việc và bản gốc: `Temp/vfx_thuy/`, hash gốc ở `hash_goc.txt`).
`HatMang.cs` không đổi. Biên dịch thử (`bien_dich_thu.py Temp/vfx_thuy`): Core, Game, Editor đều 0 lỗi. Chưa mở Unity, chưa chụp ảnh SAU.

Không đổi: chữ ký hàm công khai, bảng định tuyến `PlayNuoc`, `NuocAtHit`, `HoldNuoc`, `DanTravel`, `NgocTravel`, các hàm dùng chung
với hệ khác (`BurstFlash`, `Foam`, `RingN`, `Ripple`, `WExtra`, `MFill`/`MBand`/`MRibbon`/`MGrow`/`MSolid`, `Crescent`, `WF`, `CrownF`).
Thêm một trường công khai mới `HatLua.NuocPulse` (chưa ai gắn, xem đề xuất).

## Phần chung (dùng cho mọi tướng Thủy)

| Việc | Hàm (HatNuoc.cs) | Đã làm |
|---|---|---|
| Màu tươi | `WDefault`, `WThemes` của 10 tướng | Bảng nước tươi `#2B7FD0 / #4EB6F2 / #9FE0FF / kem`; mỗi tướng giữ sắc riêng nhưng nâng sáng, bão hoà. `thach_giai` bỏ lam xám tạm của cua. `so_ngoc`: mực đen, toé tím tươi `(98,64,162) (186,142,246)`, bọt tím rất nhạt; vệt bóng mực `MucB` tím tươi |
| Hình hạt mới có dự phòng | `KN`, `SK`, mọi chỗ vẽ | `SK("kr_mao_", i) ?? hình cũ`; chưa nhập `hat_kr_*` thì vẽ bằng hình cũ, không lỗi |
| Pha tụ | `Gather` (viết lại), `RingCo`, `CauNuoc` (mới) | Vệt nước thuôn (`kr_vet`, dự phòng giọt kéo dài) hiện dần, bay xoắn ốc vào tâm, nhanh dần (ease-in), dài theo tốc, đầu đậm đuôi nhạt; vẽ dưới cầu nên nhập vào cầu, chết đúng lúc tới tâm và làm cầu phồng (`pulse`); mật độ tăng dần (0,3 → 1,5 lần); 2 vòng nước co về tâm ở 0,42 s và 0,2 s trước lúc nhả. Cầu: khối `kr_khoinuoc` đổi hình mỗi 2 khung (sóng sánh) + lõi cuộn `kr_cau` quay + đốm kem `kr_dom` khớp khung + dải đậm ở đáy; đập nhịp; nén 2 khung (0,8×, bè 1,14) ngay trước lúc nhả rồi toé (`KrHit`) |
| Toé kiểu Kingdom Rush | `Splash` (viết lại), `KrHit`, `Khoi`, `Crown` (viết lại, bản cũ thành `CrownCu`), `VanhGiot` | Đỉnh ngay khung đầu, tan bằng vỡ: chớp sao kem 0,1 s (`kr_chop`, dự phòng nước toé nhìn thẳng) → 5–8 khối nước văng đều (đốm kem, dải đậm ở đáy) → giọt thuôn → chấm; mão nước dưới chân to nhất khung đầu, đục lỗ ở 30% đời (`kr_maolo`), sụp từ 50% và vỡ thành giọt từ các ngọn; vành giọt elip trên đất (`kr_vanh`); giọt văng theo chùm 2–3 giọt lệch cỡ; bỏ vành 8 lưỡi sóng và 5 bọt lẻ |
| Vệt ướt | `Puddle` (viết lại) | Loang 0,14 s, giữ nguyên tới 62% đời (≥ 1,5 s, tức giữ ~0,9 s) rồi mờ, không co, không viền mực, vài chấm ướt quanh |
| Giọt nhỏ hơn | `DrawDrop`, `PutGiot` | Cỡ 2,6 → 2,3 lần; dùng `kr_giot` (đầu tròn +x) nếu có, mưa nhanh thì kéo dài theo tốc |
| Bọt thành cụm | `BotCum` (mới) | 3 múi lệch cỡ chung một viền mực, bay cùng nhau, nở rồi co mượt; `hoi = true` là hơi nước (`kr_khoi`, `kr_khoinho`), không viền, trong mờ 0,62, bay lên. Thay `Foam` lẻ trong các chiêu Thủy (NSong, NXoay, NVoi, NThuong, NDan, NVa…) với nhịp sinh thấp hơn 2,5–3 lần |
| Đuôi đạn liền | `DuoiNuoc`, `RaiDuoi` (mới), `CauNuoc(tail)` | Đốt đuôi đứng yên rồi co, sinh theo QUÃNG đạn vừa đi trong mỗi bước (không theo xác suất mỗi khung), các đốt chung lớp nên hoà thành một dải một viền |
| Màu theo tướng khi hẹn giờ | `InW`, `AtW`, `EveryW` | Sự kiện hẹn giờ của các chiêu đã viết lại chạy với bảng màu của tướng ra chiêu (hai tướng nước đánh nhau không lẫn màu) |

## Từng tướng

Ảnh TRƯỚC soi bằng tờ khung (cách 2 ảnh): `ti_tach` mana, `ca_den` chiêu cuối, `thach_giai` chiêu cuối, `so_ngoc` mana, `han_ngac` mana.
Các tướng còn lại chưa soi tờ riêng; lỗi suy từ cùng đường code.

### ti_tach (n_tia; chiêu cuối n_va)
- **Lỗi ảnh trước (mana):** 00–04 pha tụ là chấm tròn rải thành vòng ở miệng, thưa; 06 tia mảnh; 08–12 đầu tia dừng ở GIỮA thân cua, chỗ
  chạm chỉ là cụm bọt trắng nhỏ đè lên mặt, không có bông toé, không loe; 14 đuôi tia rút về như cây que nhọn; 16 tia biến, toé xong mới hiện.
- **Đã sửa:** `NTia` viết lại (mục n_tia dưới), `Gather`, `CauNuoc`; chiêu cuối `NVa` dùng `Splash` mới + cụm hơi nước + vệt ướt.
- **Mong thấy ở ảnh sau:** vệt xoắn ốc nhập cầu, cầu nén rồi toé; dòng nước lam nhạt mép lam đậm tới tận mặt trước thân cua; bông toé chĩa về
  phía Tí Tách đổi hình liên tục, lá nước ôm thân, khối văng tạt ngang; hết tia đoạn cuối bay nốt rồi vỡ giọt, vệt ướt dưới chân giữ ~1 s.

### Tia nước `n_tia` (NTia; ti_tach, thach_giai, ca_den, giong_bao, uyen_xa, hai_long mana; ca_den, lien_kinh chiêu cuối)
- Tụ: `Gather` 62 đơn vị, `CauNuoc` r 16 ở miệng, nén 2 khung trước khung nhả, lúc nhả `KrHit` toé về phía trước + cụm bọt.
- Lõi: mảng liền 5 lớp (mực; lam đậm 1,0 = mép; lam 0,8; lam nhạt 0,62 = lõi rộng; sọc kem 0,34 lệch về một bên, gợn chạy theo dòng),
  bề ngang 9,5 (chiêu cuối 11), mép gợn chảy tới, gốc ở miệng hẹp, mũi tròn mập khi đang bay. Thêm vệt sáng không viền lướt trên dòng
  (30/s) và chùm 2 giọt rơi khỏi dòng (9/s). Bỏ 90 lưỡi sóng/s chạy đè lên (viền mực của chúng làm tia thành chuỗi đen trắng ở ảnh trước).
- Chạm: đầu dòng dừng ở **mặt trước thân** (cách tâm 0,24 tH), loe ra ở 36 đơn vị cuối; **lá nước ôm thân** (`LaOm`: cung quanh tâm thân
  ±69°, mặt lồi về phía người bắn, hai sừng ôm ra sau, trong mờ 0,86); **bông toé** `kr_tiadau` chĩa về phía người bắn, to nhất khung
  đầu (1,3×), đổi hình + lệch góc ±9° mỗi 2 khung (dự phòng: vương miện nước nằm nghiêng); khối nước tạt ngang theo thân 18/s, chùm giọt bắn
  ngược 11/s, cụm bọt 5/s; mỗi 0,24 s: vòng sóng dưới chân, mão nhỏ (cách nhịp), rung (0,3 nhịp đầu, 0,08 sau), `NuocPulse`.
- Hết tia: miệng nhỏ giọt + cụm bọt (đứt từ gốc); đoạn còn lại bay tốc 1450 (đuôi tròn), rơi giọt dọc đường; tới nơi `Splash` 0,8 (0,9
  chiêu cuối) + vệt ướt. Không cắt phụt.
- Hợp đồng thời gian: trả `tHit = T0 + dist/1250` (dist ngắn hơn trước ~0,24 tH vì chạm mặt trước thân); `HoldNuoc("n_tia")` giữ nguyên.
- Đã soát hình học bằng bản vẽ PIL (scratchpad `thuy/xem_tia.py`): mũi tròn khi bay, loe + lá ôm thân khi chạm, đuôi tròn khi đứt, đúng
  cả hai chiều bắn.

### thach_giai (n_tia; chiêu cuối n_cau)
- **Lỗi ảnh trước (chiêu cuối):** 00–04 vòng + chấm tụ; 06–18 cầu nhỏ xám lam đục, tròn trơn; 24–26 toé xám tối trùm cua; màu lam xám tạm
  của suất cua cũ.
- **Đã sửa:** màu nước tươi; `NCau` viết lại: `Gather` 90 + `CauNuoc` r 30 sóng sánh, nén rồi toé ở miệng (`KrHit`), bay vòng cung có
  **đuôi liền** (`tail` 0,62), bỏ giọt/bọt/lưỡi sóng rải rác (còn 12 giọt/s), trúng: `Splash` 1,25 mới + cột nước + mưa giọt + vệt ướt 1,5 s.
- **Còn lo:** ếch đứng rất gần cua, cầu bay ngắn; đuôi có thể chỉ thấy rõ ở chặng vòng cung.

### ca_den (n_tia; chiêu cuối n_tia)
- **Lỗi ảnh trước (chiêu cuối):** 02–04 cụm tụ trôi trước bụng (miệng còn ở chỗ khác lúc lấy đà, cầu đặt ở chỗ nhả của khung trúng); 12–20
  tia chàm tím sẫm, lổn nhổn; chỗ chạm cụm bọt trắng che mặt cua; 22–26 toé sau khi tia tắt.
- **Đã sửa:** bảng chàm tươi `(58,100,216) (96,162,248) (178,214,255)`; tia mới (trên).
- **Còn lo:** chỗ tụ vẫn theo chỗ nhả của khung trúng (xem đề xuất 4).

### ha_ba (n_ngoc; chiêu cuối n_va)
- **Lỗi (suy từ code, chưa soi tờ):** không có pha tụ; đuôi là giọt rời theo xác suất; toé = chớp + Splash cũ + 9 giọt + 3 bọt.
- **Đã sửa:** `NNgoc` viết lại: trong lúc phồng người (0,55 s trước khung nhả) vệt nước xoắn ốc nhập cầu nước ở miệng, cầu nén 2 khung rồi
  toé đúng lúc phụt ngọc; ngọc kéo đuôi nước liền; trúng: `Splash` 0,85 mới + vệt ướt. Ngọc dài theo hướng bay.

### so_ngoc (n_muc; chiêu cuối n_va)
- **Lỗi ảnh trước (mana):** 06–08 bóng mực nhỏ, đuôi là chuỗi chấm đen rời; 10 toé đen đục; không có pha tụ.
- **Đã sửa:** như ha_ba (cùng `NNgoc`, `muc = true`): mực xoắn ốc nhập cầu mực ở miệng, đuôi mực liền (đen, lõi tím), toé mực có ánh tím
  tươi, vệt ướt tím.

### giong_bao (n_tia; chiêu cuối n_thuong; đòn thường n_dan)
- **Lỗi (suy từ code):** tia như ti_tach; kim nước không có pha hút nước; mỗi kim trúng = chớp toé + 5 giọt + bọt lẻ; đạn thường có đuôi giọt rời.
- **Đã sửa:** bảng chàm sáng; `NThuong`: thêm `Gather` (0,55 thân) về vòng cung trên đầu trong lúc giơ gậy, mỗi kim hiện kèm cụm bọt, trúng
  dùng `KrHit` 0,34 tH lệch về phía người bắn; `NDan`: toé nhỏ ở đầu gậy, **đuôi liền** theo quãng bay, trúng `KrHit` 0,44 tH + cụm bọt.

### lien_kinh (n_va; chiêu cuối n_tia)
- **Đã sửa:** bảng lam đá sẫm → lam tươi; mana `NVa` (Splash mới, hơi nước thành cụm, vệt ướt); chiêu cuối tia mới.

### uyen_xa (n_tia; chiêu cuối n_va)
- **Đã sửa:** bảng cô-ban sáng hơn; tia mới; chiêu cuối `NVa` mới. Vệt chém riêng của đuôi sừng vẫn chưa làm (ngoài phạm vi).

### han_ngac (n_loc; chiêu cuối n_song / n_mua)
- **Lỗi ảnh trước (mana):** 08–24 phễu lốc xám ngả lục, đục; bọt ở miệng phễu rời rạc; 26 sụp toé nhỏ.
- **Đã sửa:** bảng `(44,106,208) (58,198,218) (178,240,246)`; bọt miệng phễu thành cụm (26/s → 9 cụm/s); sụp dùng `Splash` mới + vệt ướt.
  `NSong`: bọt chân sóng và bọt tràn thành cụm, `Splash`/`Crown`/`Puddle` mới. `NMua`: mão nhỏ 5/s → 3,5/s (mão mới có thêm vành và giọt).

### hai_long (n_tia; chiêu cuối n_song / n_xoay / n_voi)
- **Đã sửa:** ngọc bích tươi hơn; tia mới; `NXoay`: chớp toé ở thân thành `KrHit`, bọt thành cụm, mão mới; `NVoi`: bọt miệng phễu thành cụm.

## Chỗ còn lo
- Chưa chạy trong Unity: chưa thấy ảnh SAU, chưa đếm hạt thật. Ước lượng lúc tia đang dội: ~40 hạt sống (bản cũ ~65); mỗi cú `Splash` 1,25
  khoảng 25–30 hạt rải trong 0,5 s.
- Khung ảnh `hat_kr_*` là ĐOÁN theo quy ước cũ: `kr_mao`/`kr_maolo` chân ở ~96% đáy khung vuông, rộng ~92% khung (`Crown`: hằng 0,92 và
  0,46); `kr_vanh` đã dẹt sẵn (vẽ khung vuông); `kr_tiadau` toé về +x, tâm vẽ lệch 0,22 cỡ về phía người bắn (`NTia`, hạt `hd`); `kr_giot`,
  `kr_vet` đầu tròn ở +x; `kr_dom` khớp đúng khung `kr_khoinuoc` cùng chỉ số. Hình vẽ khác quy ước thì sửa các hằng đó.
- Lá nước ôm thân giả định thân tròn bán kính 0,24 tH quanh `Body`; con rất to / rất dẹt có thể lệch khỏi viền thân.
- `NuocPulse` chưa ai gắn nên đối thủ chưa "chớp + giật" theo từng nhịp tia (chỉ rung màn nhẹ mỗi 0,24 s).
- `HatLoc.cs` (Lộc Phong, hệ Mộc, `n_cau_tia`) gọi `NTia` nên tia lục của nó cũng đổi theo kiểu mới (cùng chữ ký, cùng giờ trúng).

## Đề xuất sửa file chung
1. **StageView (đối thủ chớp + giật suốt dòng tia):** gắn `Hat.NuocPulse = s => { chớp _Flash 2 khung + bật lùi nhẹ (0,04–0,06 H × s) con
   bị trúng }` (cả ô xem tướng nếu muốn). Hiện sân chỉ cho đối thủ giật một lần ở `fxHitAt`.
2. **Sau khi nhập ảnh `hat_kr_*`:** chạy lại hai menu `PokiClash/Prefab/Sàn đấu: hạt lửa` và `…Hộp chi tiết tướng: hạt lửa + nút Mana`
   để ảnh mới vào danh sách sprite của lớp hạt; chưa chạy thì code vẫn vẽ hình cũ.
3. **Báo phiên hệ Mộc:** tia của `bom_la` (HatLoc → NTia) đổi kiểu theo bản này.
4. **Chỗ tụ theo miệng lúc lấy đà:** `StageView.Muzzle` trả chỗ nhả của khung trúng; tướng lấy đà dời miệng (ca_den) thì cầu tụ lơ lửng
   chỗ khác. Nếu `AolaActor` cho điểm bắn theo giờ, truyền `Func<float, Vector2>` vào `PlayNuoc` (hoặc thêm điểm bắn ở khung 0) để cầu đi theo miệng.
5. **Skill `pokiclash-fx-congthuc` mục 5c:** ghi công thức mới (tia chạm mặt trước thân + lá ôm thân + bông toé đổi hình mỗi 2 khung + đuôi
   đứt bay nốt; pha tụ vệt xoắn ốc ease-in nhập cầu + nén 2 khung; toé Kingdom Rush; đuôi đạn theo quãng; bọt cụm; vệt ướt giữ 1 s) sau khi
   phiên chính soi ảnh SAU.
