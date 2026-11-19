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

---

## Đợt khung vẽ sẵn (flipbook) 2026-11-19

Bản sửa ở scratchpad `fb_thuy/` (`HatNuoc.cs`, file mới `HatFbThuy.cs`; `HatMang.cs` không đổi), chưa chép vào Assets. Biên dịch thử ngoài
Unity (`bien_dich_thu.py`): Core, Game, Editor 0 lỗi; gộp chung với bản đang làm của phiên Mộc, Thổ cũng 0 lỗi.

**Phần chung (mọi tướng Thủy dùng):**
- `Crown` (mão nước dưới chân) → khung `nuoc_toe`: cao 0,95 × bề ngang mão cũ. Tốc theo đời mão cũ (1,3–2,2; mão mưa nhanh nhất). Bỏ 2 khung
  đầu, trong mờ 0,92 ở lớp trước tướng. Bỏ vành giọt và giọt sụp: khung đã có. Neo dời xuống theo khung vì đáy vũng trong ảnh nhích lên
  0,05–0,13 cao khung, nhờ vậy vũng bám đất.
- `Splash` (toé lớn) → `trung_nuoc` ở thân, cao min(1,3; sc) × tH, có hướng nước tới (tham số mới `dir`, null thì lật ngẫu nhiên),
  kèm `nuoc_toe` dưới chân:
  - bỏ chớp sao kem, khối văng viền mực, cụm bọt viền mực;
  - giữ 1 chùm 2 giọt ra sau, vòng sóng, họa tiết thêm của tướng.
- `CauNuoc` (cầu tụ ở miệng, cầu bay) → khung `cau_nuoc` lặp:
  - cao khung 2,56 × r (thân cầu chiếm ~0,78 khung), lệch pha ngẫu nhiên;
  - giữ nhịp lớn dần, phồng khi vệt nhập, nén 2 khung trước lúc nhả, giãn theo hướng bay;
  - đuôi liền vẫn rải đốt nhưng bỏ viền mực (`DuoiNuoc` thêm tham số `ink`).
- `BackColumn` (cột nước sau lưng) → một `nuoc_toe` cao 1,2 tH ở lớp sau tướng, thay ~22 lưỡi sóng viền mực.
- Chỉ dùng khung khi bảng nước của tướng là lam / ngọc lam (`FbNuoc`: lục > đỏ và lam > đỏ). Nhân màu không đổi được khung lam ra tím /
  lục, nên bảng mực tím (so_ngoc) và tướng hệ khác lỡ rơi vào hàm nước giữ hạt cũ.
- Màu khung giữ nguyên bảng đã duyệt. Chỉ tướng có sắc nước lệch > 15 độ so với bảng chung thì nhân nhẹ (`FbNuocTint`, nay chỉ có
  hai_long).
- Mấy sự kiện hẹn giờ có gọi `Crown` / `Splash` đổi từ `At` / `Every` sang `AtW` / `EveryW`, để chọn khung theo đúng bảng nước của tướng ra
  chiêu khi hai tướng nước đánh nhau. Áp cho: mão lúc sóng dâng và lúc cột phun, mão vòi rồng lúc dựng và lúc sụp, mão cuối loạt thương,
  mão mưa.
- Giữ nguyên:
  - thân tia nước liền (mảng có va chạm) và lá nước ôm thân;
  - con sóng thần mảng, cột phun, thân vòi rồng / lốc;
  - pha tụ vệt xoắn ốc, mũi thương, viên đạn, viên ngọc / bóng mực;
  - nhịp `NuocPulse`, giờ trúng trả về, `HoldNuoc`.
- Soát vị trí bằng bản vẽ PIL theo đúng phép tính `DrawFb` (scratchpad `fb_thuy_mock.py`, ảnh `fb_thuy_mock.jpg`). Đã thấy: bông trúng nằm
  ở mặt trước thân, vệt tia chĩa về người bắn ở cả hai phe; mào sóng đổ trúng đối thủ ở cả hai chiều.

### ti_tach (Tí Tách): đợt khung vẽ sẵn 2026-11-19
- **Đòn thường:** không có hạt trên sân (không có trong `WaterAtk`), không đổi.
- **Mana `n_tia`:**
  - cầu tụ ở miệng là `cau_nuoc`; toé lúc nhả là `trung_nuoc` nhỏ (54) chĩa theo tia;
  - ở chỗ chạm, mỗi nhịp 0,24 s phát một `trung_nuoc` 0,75 tH (lượt đầu ×1,15) nghiêng theo tia, thay bông `kr_tiadau`;
  - khối văng giảm 18 → 7/s, chùm giọt 11 → 6/s, bỏ cụm bọt viền mực; mão dưới chân là `nuoc_toe`; toé cuối là `Splash` khung.
- **Chiêu cuối `n_va`:**
  - `Splash` khung 1,25 có hướng lao tới: thêm `case "n_va"` truyền hướng; trước đây mã này rơi xuống `default`;
  - cột nước sau lưng là `nuoc_toe`; hơi nước, mưa giọt, vệt ướt giữ.

### thach_giai (Thạch Giải): đợt khung vẽ sẵn 2026-11-19
- **Đòn thường:** không đổi (không có hạt).
- **Mana `n_tia`:** như ti_tach.
- **Chiêu cuối `n_cau`:**
  - cầu r 30 tụ ở miệng rồi bay vòng cung là `cau_nuoc`, đuôi liền không viền;
  - toé lúc nhả là `trung_nuoc` 66 theo hướng ném;
  - trúng: `Splash` khung 1,25 theo hướng cầu rơi tới, cùng cột `nuoc_toe` 1,2 tH sau lưng;
  - mưa giọt, vệt ướt giữ.

### ca_den (Hải Đăng): đợt khung vẽ sẵn 2026-11-19
- **Đòn thường:** không đổi.
- **Mana `n_tia`:** như ti_tach.
- **Chiêu cuối `n_tia` dài:** như mana; bông chỗ chạm 0,82 tH. Bảng chàm lệch bảng chung < 15 độ nên khung giữ màu gốc.

### hai_long (Hải Long): đợt khung vẽ sẵn 2026-11-19
- **Đòn thường:** không đổi.
- **Mana `n_tia`:** như ti_tach. Khung nhân nhẹ (0,83; 1; 0,9) về ngọc bích của tướng, nên bọt ngả bạc hà nhạt.
- **Chiêu cuối dạng 1 `n_song`:** con sóng mảng giữ nguyên, lúc tới nơi giao cho khung `song_nuoc`:
  - từ khung 10, tốc 1,25, cao 1,2 tH, trong mờ 0,86;
  - lật theo hướng đổ, neo lùi về phía người ra chiêu 0,36 cao khung cho mào đổ trúng đối thủ;
  - phát sớm 0,08 s, chồng lên lúc mảng sụp;
  - bỏ 18 lưỡi sóng viền mực chồm qua đầu và 5 cụm bọt viền mực tràn hai bên; `Splash` khung theo hướng sóng; mão lúc sóng dâng là `nuoc_toe`.
- **Chiêu cuối dạng 2 `n_xoay`:**
  - lúc cột phun: `nuoc_toe` lớn ở chân, cột húc thân là `trung_nuoc` 1,0 tH xoay cho tia tới từ dưới;
  - lưỡi sóng bắn quanh cột bớt 60 → 26/s; cột nước mảng giữ.
- **Chiêu cuối dạng 3 `n_voi`:** thân vòi mảng giữ; mão lúc dựng là `nuoc_toe`; lúc sụp là `Splash` khung ở lớp sau tướng.

### han_ngac (Hàn Ngạc): đợt khung vẽ sẵn 2026-11-19
- **Đòn thường:** không đổi.
- **Mana `n_loc`:** phễu lốc mảng giữ (khung `loc` là năng lượng lục, không hợp lốc nước); mão lúc dựng là `nuoc_toe`; lúc sụp là `Splash`
  khung.
- **Chiêu cuối `n_song`:** như hai_long dạng 1.
- **Chiêu cuối `n_mua`:** mão nhỏ 3,5/s là `nuoc_toe` chạy nhanh (2,2). Mây, mưa giọt, vòng sóng, vệt ướt giữ.

### ha_ba (Sò Ngoạm): đợt khung vẽ sẵn 2026-11-19
- **Đòn thường:** không đổi.
- **Mana `n_ngoc`:**
  - cầu tụ ở miệng lúc phồng người là `cau_nuoc`; toé lúc phụt là `trung_nuoc` 0,46 tH theo hướng phụt;
  - viên ngọc và đuôi giữ; trúng là `Splash` khung 0,85 theo hướng ngọc bay.
- **Chiêu cuối `n_va`:** như ti_tach.

### so_ngoc (Bát Trảo): đợt khung vẽ sẵn 2026-11-19
- **Không đổi gì** (mana `n_muc`, chiêu cuối `n_va`). Bảng mực đen tím: khung lam nhân màu không ra tím, nên `FbNuoc` trả false và mọi chỗ
  giữ hạt cũ.
- Muốn đồng bộ thì cần bộ khung mực riêng (toé mực, cầu mực), hoặc khung xám để nhuộm.

### giong_bao (Giông Bão): đợt khung vẽ sẵn 2026-11-19
- **Đòn thường `n_dan`:**
  - toé đầu gậy là `trung_nuoc` nhỏ (42) theo hướng bắn;
  - đạn trúng là `trung_nuoc` 0,82 tH theo hướng đạn, thay chớp sao, khối văng và cụm bọt viền mực;
  - viên đạn và đuôi liền giữ; giờ trúng giữ đúng khung trúng của clip.
- **Mana `n_tia`:** như ti_tach.
- **Chiêu cuối `n_thuong`:** mỗi mũi trúng là `trung_nuoc` 0,58 tH, tốc 1,55, nghiêng theo hướng mũi lao (tối đa ±35 độ). Mão cuối là
  `nuoc_toe`. Mũi thương, pha tụ giữ.

### uyen_xa (Uyên Xà): đợt khung vẽ sẵn 2026-11-19
- **Đòn thường:** không đổi.
- **Mana `n_tia`:** như ti_tach.
- **Chiêu cuối `n_va`:** như ti_tach. Vệt chém đuôi sừng vẫn chưa có (ngoài phạm vi).

### lien_kinh (Thôn Kình): đợt khung vẽ sẵn 2026-11-19
- **Đòn thường:** không đổi.
- **Mana `n_va`:** như chiêu cuối của ti_tach. Mảnh tinh thể đen (`WExtra`) giữ.
- **Chiêu cuối `n_tia` dài:** như ca_den.

### Chỗ còn ngờ (đợt khung vẽ sẵn)
- Chưa chạy trong Unity, chưa xem ảnh thật. Cỡ tính từ hộp hình đo trên khung và bản vẽ PIL.
- Tia đang dội: các lượt `trung_nuoc` theo nhịp chồng 2–3 lượt (mỗi lượt ~0,6 s). Nếu rối, chỉ phát ở nhịp chẵn (0,48 s).
- `song_nuoc` chồng lên con sóng mảng đang sụp 0,08 s. Hai kiểu nước có thể lộ chỗ giao; khi đó cho mảng sụp nhanh hơn hoặc phát khung muộn hơn.
- Toé chiêu cuối (`n_va`, `n_cau`) gồm `trung_nuoc` 1,25 tH và mão 0,93 tH chồng nhau, che gần hết thân ~0,2 s ở đỉnh. Nếu che mặt lâu thì
  hạ `Mathf.Min(1.3f, sc)` trong `Splash`.
- hai_long: bọt khung ngả bạc hà do nhân màu. Không muốn thì bỏ nhánh nhân màu trong `FbNuocTint`.

### Cần đổi ở file khác (đợt khung vẽ sẵn)
- Không cần đổi `StageView.cs` hay `HatFlip.cs`.
- Khi chép vào Assets: `HatFbThuy.cs` là file mới, Unity tự tạo `.meta`. Ảnh `hat_fb_*` phải nằm trong danh sách sprite của lớp hạt: chạy
  lại menu `PokiClash/Prefab/Sàn đấu: hạt lửa` và `…Hộp chi tiết tướng: hạt lửa + nút Mana`. Chưa có ảnh thì `HasFb` trả false, mọi chỗ về
  hạt cũ.
- Skill `pokiclash-fx-congthuc` mục 5c: ghi thêm cách dùng khung nước, sau khi phiên chính xem ảnh trong trận.

### Lốc nước khung vẽ sẵn "loc_nuoc" (2026-11-19, người dùng chê lốc của Hải Long "màu hơi trầm và chưa hợp lắm")
- **Hàm mới** trong `HatFbThuy.cs`:
  - `LocNuocFb`: khung lặp, chân và cao đổi theo tuổi, giãn ngang, hiện dần / tắt dần, lắc nhẹ ±3 độ, giữ màu khung;
  - `LocNuocBao`: hai lớp lệch pha, lớp sau tướng đặc, lớp trước tướng lật ngang, trong mờ 0,5 và to hơn 4 %;
  - `VeFbGian`: vẽ khung có giãn ngang.
- **`NVoi`** (vòi rồng `n_voi` dạng 3 của hai_long; lốc lướt `n_loc` mana của han_ngac):
  - thân là `LocNuocBao` từ TA, cao 15 % → HT trong 0,22 s, chân theo CcT (lốc lướt tới chân đối thủ);
  - sụp từ T1: co 30 %, tắt 0,35 s;
  - bỏ 8 đĩa mảng viền mực, sọc bọt trượt, lưỡi sóng ở mép, cụm bọt miệng phễu;
  - giữ nước hút vào chân, vòng co, mão `nuoc_toe` lúc dựng, giọt văng, sao của hai_long, cú sụp toé, giờ trả về.
- **`NXoay`** (`n_xoay` dạng 2 của hai_long): cột nước mảng ba lớp và bọt đầu cột thay bằng `LocNuocBao`:
  - vọt lên 1,3 tH trong 0,12 s, xoáy nhanh tốc 1,7, đời 0,66 s như cột cũ;
  - bỏ cụm bọt viền mực trên đầu cột;
  - giữ xoáy đất, mão, bông trúng từ dưới, lưỡi sóng bắn, mưa giọt.
- Chưa nhập khung, hoặc bảng nước không phải lam / ngọc lam (`FbNuoc`): về đĩa / cột mảng cũ.
- Ngờ: phễu khung thon ở dưới (giãn ngang 1,25 / 1,2 vẫn hẹp hơn thân đối thủ to). Lớp trước 0,5 phủ cả đầu suốt ~1,6–2 s của vòi rồng;
  nếu che mặt quá thì hạ còn 0,35.

### Góp ý trong trận 2026-11-19: tia Thôn Kình to, lốc nước to
- **lien_kinh (Thôn Kình), chiêu cuối `n_tia`:** `WTheme.tiaTo = 0.15`.
  - Nửa bề dày lõi tia = 0,15 × casterH, chặn 22–29, tức 2–2,6 lần tia chiêu cuối thường 11 (casterH 176 → 2,4 lần).
  - Mũi tròn, gốc hẹp, đoạn loe, gợn dài theo bề dày (`TiaHW` thêm hệ số `kl`).
  - Cầu tụ và toé lúc nhả ×0,8 kt; vệt sáng, khối văng ×√kt.
  - Bông `trung_nuoc` ở đầu tia, mão, vòng sóng, toé cuối ×(1 + 0,3 (kt − 1)) ≈ 1,4: bông 1,15–1,3 tH, toé cuối sc 1,25.
  - Giờ trúng, nhịp, `NuocPulse` giữ. Tướng khác dùng `n_tia` không đổi (tiaTo = 0 → mọi hệ số = 1).
- **Lốc nước to** (`NVoi`: hai_long `n_voi`, han_ngac `n_loc`; `NXoay`: hai_long `n_xoay`):
  - Cao 1,7 tH, chặn mép trên sân, tối thiểu 1,3 tH (phe địch ở trên sân cỡ 1,63 tH).
  - Giãn ngang 1,9; chân khung hạ 0,1 cao khung dưới chân đối thủ. Theo bề ngang đo trên khung: ngang thân ở ngực trở lên ≥ 1,3 tH, giữa
    thân ~1 tH, chân ~0,7 tH (đoạn phễu thon của khung).
  - Phần chân bù bằng `nuoc_toe` 0,78 tH toé lặp 3,2 lần/s ở gốc lốc (trong mờ 0,75; chỉ `NVoi`, `NXoay` đã có mão 0,85 tH).
  - Lớp trước vẫn mờ 0,5. Bản vẽ soi: scratchpad `fb_thuy_loc_mock2.jpg`.
  - Ngờ: miệng phễu rộng ~2 tH, khung giãn 1,9 lần trông bè. Muốn trùm kín cả chân mà không giãn thì cần gen khung lốc mập ở gốc.
- **Lốc TRÙM `loc_nuoc_bao`** (sau góp ý trên; khung mới có cột xoáy dày, gốc gần rộng bằng miệng):
  - Áp cho lốc bao quanh đối thủ: `n_voi`, `n_xoay` (hai_long) và `n_loc` lúc đã tới nơi (han_ngac).
  - Cao 1,65 tH (`LocBaoCao`: chặn để phần đặc không vượt mép trên sân; phe địch ~1,6 tH); giãn ngang 1,25; chân khung hạ 0,04 cao khung.
  - Theo bề ngang đo trên khung: ngang thân ≥ 1,3 tH, vòng chân ~1,7 tH, nên trùm kín từ chân tới đầu (bản vẽ soi `fb_thuy_bao_mock.jpg`).
  - Bỏ mão bù chân. Lớp trước mờ 0,5.
  - `n_loc`: lúc lướt vẫn là phễu `loc_nuoc` 1,3 tH, giãn 1,25. Tới chân đối thủ thì phễu tắt 0,15 s, lốc trùm hiện 0,15 s, nở từ 70 % cao.
  - Chưa có `loc_nuoc_bao`: về lốc phễu to (giãn 1,9) + mão bù chân; chưa có cả hai: đĩa / cột mảng cũ.

### ti_tach (Tí Tách): thử tia vẽ sẵn cho mana `n_tia` (2026-11-19)
- Cờ mới `WTheme.tiaKhung` chỉ bật cho ti_tach. `PlayNuoc` truyền bề dày `day = clamp(0,22 × casterH, 26, 44)`; casterH 150–176 cho
  ra 33–39, gấp đôi tia mảng cũ (19).
- `NTia` có đủ khung `DaTiaNuoc` thì gọi `NTiaKhung` (`HatFbThuy.cs`), phát `TiaFb(DaTiaNuoc, miệng + 14 theo hướng tia, mặt trước thân đối
  thủ, day, tTu, tBan)`. Chưa có khung: tia mảng cũ.
- Cỡ theo bộ da: đầu nòng `cau_nuoc` 1,9 day (~63–74), bông `tia_nuoc_trung` 2,9 day (~96–112, ~0,7 tH), đoạn thân cao day / 0,53.
- Thời gian:
  - tTu = tHit − thời gian đầu tia vươn của TiaFb (quãng / 2600, chặn 0,07–0,14), nên giờ chạm vẫn là T0 + quãng / 1250 như tia cũ.
  - tBan = T1 − tHit (T1 = T0 + 0,88); hết tia ở T1 như cũ, `HoldNuoc` không đổi.
  - Đoạn cuối tới đích ở T1 + quãng / tốc trôi (≤ 0,32 s), lúc đó Splash 0,8 + vệt ướt.
- Bỏ: thân mảng, cầu tụ CauNuoc, lá ôm thân, bông trung_nuoc theo nhịp, vệt sáng, toé lúc nhả.
- Giữ:
  - vệt xoắn ốc tụ vào đầu nòng;
  - giọt rơi khỏi mép dòng 6/s (cũ 9);
  - khối văng 4/s + chùm giọt bắn ngược 4/s (cũ 7 + 6);
  - nhịp 0,24 s: NuocPulse, rung, vòng sóng, mão nuoc_toe ở nhịp chẵn;
  - giọt ở miệng lúc tắt, giọt dọc đuôi 14/s.
- Ngờ: tia rời miệng muộn hơn khung nhả của clip ~0,1 s (để giữ giờ chạm). Nếu thấy hụt thì cho tTu = T0 và trả giờ chạm sớm hơn tương ứng.

### Mọi tia nước của tướng Thủy dùng tia vẽ sẵn (2026-11-19)
- Bỏ cờ thử `tiaKhung` của ti_tach. `PlayNuoc` case `n_tia` luôn truyền bề dày tia vẽ sẵn; `NTia` gọi `NTiaKhung` khi có đủ khung
  `DaTiaNuoc` và bảng nước lam / ngọc lam (`FbNuoc`). Bảng mực tím hoặc chưa có khung thì về tia mảng cũ.
- Bề dày theo casterH:
  - mana 0,22 (chặn 26–44);
  - chiêu cuối 0,28 (34–56);
  - chiêu cuối của tướng có `tiaTo` (Thôn Kình) 2,2 × tiaTo = 0,33 casterH (44–68). Đầu nòng 1,9 × day, bông trúng 2,9 × day, tức ~1,1 tH ở casterH 176.
- `NTiaKhung` thêm `kh = clamp(1 + 0,6 (day / 36 − 1), 1, 1,5)`: mão, vòng sóng, rung đầu, toé cuối, vệt ướt to theo bề dày. Toé cuối
  chiêu cuối 0,9 (mana 0,8). Mana ~1, chiêu cuối ~1,2, Thôn Kình ~1,35.
- Tướng / chiêu đổi:
  - mana `n_tia`: ti_tach, thach_giai, ca_den, giong_bao, uyen_xa, hai_long;
  - chiêu cuối `n_tia`: ca_den, lien_kinh (tia to).
- so_ngoc không dùng tia (giữ cũ). Giờ chạm, nhịp NuocPulse, HoldNuoc, giờ trả về như bản Tí Tách.

### Góp ý trang so sánh 2026-11-19 (chiều): gốc tia theo rig, tia / cầu to, bão Hải Long
- **Gốc tia đo trên rig** (.atomik qua `ArtGen/Spine/mo_xe/atomik_dang.py`; script scratchpad `fb_thuy_do_rig.py`, `fb_thuy_bang.py`).
  - Đơn vị: phần chiều cao game, x tới trước, y lên.
  - Ra sân lấy lệch so với chỗ bắn của rig (`mouth` StageView truyền), nên lệch neo hình không ảnh hưởng.
  - Dạng phân bằng độ cao chỗ bắn / casterH.
  - Hàm mới `NTiaNuoc` / `NCauNuoc` (`HatFbThuy.cs`); `PlayNuoc` case `n_tia` / `n_cau` gọi vào đó.
- **ca_den (Hải Đăng), mana + chiêu cuối `n_tia`:**
  - Gốc = tâm vùng lòng miệng đỏ ở dáng há: cast (0,11; 0,33), skill (0,14; 0,31), trung bình hai dạng.
  - Chỗ bắn rig cũ (0,347; 0,305) nằm ở mép phải miệng; gốc cũ (+14 theo hướng) lệch ra trước ~0,25 H.
  - Không cầu đầu nòng (nongK 0), không tụ, phóng ngay ở khung há (giờ chạm = khung há + 0,07–0,14 s, nhịp đập dời theo, trả giờ chạm mới).
  - Bề dày 0,3 casterH (mana) / 0,36 (chiêu cuối), chặn 40–80.
- **thach_giai (Thạch Giải):**
  - Mana `n_tia`:
    - gốc = tâm lòng miệng đỏ: dạng 1 (0,16; 0,62), dạng 2 (0,27; 0,895);
    - bề dày 0,48 casterH (chặn 60–110; độ há đo ~0,45 H);
    - cầu đầu nòng × 0,55, bông trúng × 0,6, để bông lặp không trùm kín con bị trúng suốt lúc dội.
  - Chiêu cuối `n_cau`: bỏ pha tụ (vệt xoắn, cầu lớn dần). Đúng khung ợ cầu hiện ở giữa mồm (dạng 1 (−0,02; 0,59), dạng 2 (−0,01; 0,88)),
    nở 0,06 s rồi bay. Cầu × 1,6 (r 48); toé ở miệng × √1,6. Giờ trúng giữ.
- **giong_bao (Giông Bão), mana `n_tia`:** gốc + cầu đầu nòng bám xương `cau` (quả cầu đầu trượng) theo bảng mỗi 0,05 s của clip cast
  (`GbTruong1` / `GbTruong2`), có cả lúc trượng vung từ sau đầu ra trước. Cầu đầu nòng × 0,75; bề dày 0,22 casterH như các tia mana khác.
- **uyen_xa (Uyên Xà), mana `n_tia`:** gốc + cầu đầu nòng ở trung điểm tâm hai sừng (hình `P_ear01` / `P_ear02`) theo bảng mỗi 0,05 s (`UxSung`,
  trung bình hai dạng). Cầu đầu nòng × 0,8.
- **hai_long (Hải Long), chiêu cuối: bão** (`HaiLongBao`, chỉ khi bảng nước là của hai_long):
  - Lốc phụ: `n_voi` 3, `n_xoay` / `n_song` 2 cột `loc_nuoc` cao 1,1–1,4 tH quanh đối thủ (hai bên, sau lưng, chếch trước).
    - Mọc lệch giờ 0,12 s, trôi lắc nhẹ, kèm `nuoc_toe` ở chân.
    - Cột sau lưng ở lớp sau tướng, cột chếch trước mờ 0,8.
  - Sét `set_danh`: `n_voi` 6, còn lại 4 phát.
    - Phát chính đánh xuyên đầu đối thủ đúng nhịp trúng lớn (giờ trả về của chiêu); một phát nữa vào đối thủ; còn lại quanh sân / chân lốc.
    - Mỗi phát: chớp màn trắng nhạt (alpha 0,12–0,22), rung 0,3–0,5, `trung_trang` ở chỗ trúng.
    - Phát vào đối thủ thêm `NuocPulse`.
  - Chưa làm tối trời / mây.
- Ngờ:
  - Bảng rig đo theo giây clip từ lúc `PlayNuoc` được gọi (đầu clip), như HatRua; clip chạy nhanh / chậm khác thì lệch.
  - Giông Bão rung đầu trượng ±0,03 H mỗi 0,05 s (đúng rig) nên cầu đầu nòng rung theo.
  - Thạch Giải: tia rất dày (~84 đơn vị ở casterH 176).
