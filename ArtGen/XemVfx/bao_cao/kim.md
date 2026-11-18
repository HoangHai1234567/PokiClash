# Báo cáo VFX hệ Kim (2026-11-18)

Agent hệ Kim. Đã sửa 10 file trong `Assets/01 Script/Game/Battle/` (HatSat, HatKhoang, HatGiao, HatCua, HatHon, HatXich, HatSoi, HatRobot, HatVua, HatPhao). Không đụng `*Bang.cs`, `StageView*.cs`, `HatLua.cs`, `HatNuoc.cs`, `HatMang.cs`, file của hệ khác, JSON, rig, ảnh. Không mở Unity, không commit.

## Cách soát

- **Biên dịch:** `py -3 -I ArtGen/Spine/quai/tho5_game/bien_dich_thu.py Temp/vfx_kim` cho 0 lỗi ở Core, Game, Editor. Hash 10 file trong Assets không đổi suốt lúc làm (`hash_goc.txt`), chép đè xong ghi `hash_moi.txt`.
- **Chạy thử ngoài Unity (mono):** gọi thẳng 30 hàm chiêu, bước mô phỏng 120 Hz, gọi hàm vẽ của mọi hạt mỗi 1/30 s. Kết quả:
  - Không có ngoại lệ trong mã mới. Ngoại lệ còn lại chỉ là `Resources.Load` (cần Unity thật) ở NXichLua, NHonGoi, NSatBan.
  - **Giờ trả về (hợp đồng thời gian) giữ nguyên** ở cả 30 chiêu.
  - Số hạt trước và sau: `ket_qua_truoc.txt`, `ket_qua_sau.txt` (bảng ở cuối báo cáo).
  - Công cụ: `C:\Users\Admin\AppData\Local\Temp\claude\f0d219082acbfb1c\1c647fe5-0a0b-4650-ae2e-8e2bbbbf941c\scratchpad\kim_vfx\chay\` (`Run.exe` đếm hạt, `Xem.exe <mã> <tệp>` xuất nét vẽ).
- **Tờ khung xem trước:** tự vẽ lại từ nét vẽ thật của mã bằng ảnh hạt thật trong `Assets/03 Art/Fx/Hat` (đã có bộ `hat_kr_*`). Nền phẳng, hai tướng là elip giả nên chưa phải ảnh Unity. Đã soi:
  - `to/s_vua_tia2.jpg`, `to/s_robot_cau.jpg`, `to/s_xich_lua.jpg`, `to/s_cua_lien.jpg`, `to/s_hon_kiem.jpg`, `to/s_phao_cau.jpg`;
  - tất cả trong `...\scratchpad\kim_vfx\to\`, vẽ bằng `...\scratchpad\kim_vfx\ve.py`.

  Sau khi soi đã sửa ba lỗi:
  - lõi nổ đặt sát tâm nên thân đối thủ che hết;
  - vòng vàng 0,8 thân trùm đối thủ;
  - vòng có viền mực dày dưới cột lửa và ở chiêu Vong Kỵ.
- **Chưa xem trong Unity, chưa thử trên Android:** phiên chính cần chụp tour để so.

## Bộ hạt KR5 dùng chung (HatRobot.cs, mục "BỘ HẠT KR5 CỦA HỆ KIM")

Mọi hàm dùng ảnh `hat_kr_*` nếu đã nhập, chưa có thì dùng hình cũ (`Km(tên, i)` trả null → `?? S("blob_..")`, không lỗi).

| Hàm | Làm gì |
|---|---|
| `KmKhoi` | **Cụm khói nhiều múi hai tông** (kr_khoi + kr_khoiday: đỉnh nhạt, đáy đậm), một viền mực chung. To gần đủ ngay ở 22 % đời, bay lên, **tách 2 cụm con ở 45 % đời** rồi co. Alpha chỉ cắt 35 % cuối. Tông than đen ngả xám (khói hồn: xanh xám; khói máy: xám nhạt). Đáy còn ánh lửa lúc mới bung. Có tro. |
| `KmNo` | **Nổ KR5:** chớp 1–2 khung (kr_chop, 1/3 vụ nổ) → lưỡi liềm lửa (kr_liem, bật nhanh rồi hãm, lõi nguội kem → vàng → cam, teo thành đốm) cắm trong khối khói hai tông → khói tách cụm bay lên. Kèm vòng cung dẹt không viền trên đất (kr_cung), vệt cháy giữ ~1 s rồi mờ, tia bắn rồi khựng, đá văng một phía (nổ lớn). Nổ lớn: lõi sau tướng, lòi hai bên và trên đầu, chỉ vài lưỡi nhỏ phía trước. Nổ trúng nhỏ: lửa nhỏ phía trước. Ba bảng màu: `luat` lửa đỏ cam, `vtuoi` năng lượng vàng tươi, `hon` lửa hồn. |
| `KmTia` + `KmCham` | **Tia liền khối** (mảng liền HatMang, năm lớp: mực mảnh, cam đỏ `#F0702A` sát viền, cam `#FFA43A`, vàng `#FFD94A`, lõi kem `#FFF6D6` rộng). Đầu tia tới đúng thân đối thủ rồi đứng đó. **Bông va chạm liên tục** (kr_tiadau đổi hình mỗi 2 khung), tia kim loại bắn ngược rồi khựng, vòng va chạm nở, rung nhỏ dồn dập. Hết tia: đuôi rút vào chỗ chạm, bông vỡ to, không cắt phụt. |
| `KmHut`, `RbHut`, `RbHutXa` | **Pha hút:** vệt thuôn (kr_vet) kéo dài theo vận tốc, bay xoắn ốc, nhanh dần (ease-in), hiện dần. Chạm vỏ cầu thì nhập vào cầu, không tắt giữa đường. |
| `KmVong` | Vòng mảnh không viền: co về tâm (pha tụ) hoặc nở (va chạm). `RbVong` nay cũng không viền. |
| `RbCau` | Cầu năng lượng vỏ nhiều múi (kr_cau, hoặc ba múi lệch tâm quay ngược nhau), lõi kem, lớn theo nhịp đập. Bảng tươi. Cung điện không viền. |
| `KmNen` | Cầu nén 1–2 khung ngay trước lúc nhả, rồi `KmChop` chớp. |
| `KmDuoi` | **Đuôi theo quãng bay** (KR5): hạt chia đều theo đường đã đi, nên đuôi liền dù đạn nhanh. Dùng cho cầu, đạn sắt, quả pháo, thiên thạch, vệt móc xích. |
| `KmLuaS`, `KmGiot` | Lưỡi lửa chữ S liền khối (kr_lua, đổi dáng mỗi 2 khung) và giọt tách khỏi ngọn (kr_giot, đầu tròn theo hướng bay). |
| `KmDomCum` | Cụm 3–6 đốm nhỏ lệch cỡ (0,35–0,7 lần đốm cũ) thay đốm lẻ to. |
| `KmTiaLua` | Tia kim loại bắn nhanh (420–800) rồi khựng (cản 8,5). |
| `KmBong`, `KmChop`, `KmCung`, `KmChay` | Bông va chạm, chớp nổ, vòng cung dẹt, vệt cháy. |

Ghi chú về ảnh:
- `kr_cung` đã vẽ dẹt sẵn trong khung vuông (nét chiếm 0,9 × 0,36): vẽ theo khung vuông, không ép dẹt thêm.
- `kr_vet` là nét mảnh ngang giữa khung vuông: dài theo tốc độ, dày chặn ở 2,6 lần cỡ.

Màu (người dùng: "tươi, hợp sân cát biển sáng"):
- Năng lượng: `RbNang`, `RbChopC`, `VmVang` đổi sang cam đỏ / cam / vàng / kem tươi (trước ngả nâu).
- Chớp sắt `SatChopC`: viền mực chung `#2B2118`, thép lam sáng hơn (trước viền chàm sẫm).
- Sắt pháo, quặng, đất, bụi của Thiết Khoáng nâng sáng và bão hòa. Khói than giữ đen ngả xám.
- Chớp màn tia Mặt Trời: alpha 0,4 → 0,24 (cả màn bạc màu).

## Từng tướng

### Nhật Vương (kim_nghe, HatVua.cs) — trọng tâm

- **Lỗi ở ảnh TRƯỚC:**
  - mana 11–15: tia ghép từ lưỡi lửa rời, màu cam nâu tối, mảnh;
  - mana 12–14: vòng to trùm đối thủ;
  - mana 13–15: khối nổ vàng đục che kín đối thủ;
  - mana 16: tia tắt phụt;
  - mana 17–23: khói thành chấm đen rời rạc, đốm lẻ;
  - ult 21–27: màn tối nhật thực (giữ nguyên ý tưởng);
  - ult 30: thiên thạch đuôi lửa hạt rời.
- **Đã sửa:**
  - `NVuaTia`:
    - tia liền khối `KmTia` bảng tươi, lõi kem rộng (nửa bề rộng 0,09 thân), dày dần sau mỗi hành tinh (`sizeFn`);
    - vẽ ở lớp Sau tướng nên đi xuyên các hành tinh của rig;
    - đầu tia tới phần trên thân đối thủ, `KmCham` va chạm liên tục, tia lửa văng hai bên thân tia;
    - đuôi rút vào chỗ chạm, bông vỡ to;
    - chớp mỗi hành tinh nhỏ lại;
    - nổ Mặt Trời `VmNoVang` → `KmNo` vtuoi: lõi sau lưng, vòng va chạm nhỏ nhạt thay vòng 0,8 thân;
    - vòng cung dẹt hai đợt, khói cụm.
  - `VmTu`: hút xoắn ốc vào Mặt Trời, vòng co.
  - `NVuaAn`: đường lửa vtuoi, chớp ở chân thay chớp 0,9 thân, bông va chạm, cụm đốm, khói cụm.
  - `NVuaNhat`:
    - đốm quỹ đạo nhỏ lại;
    - đuôi thiên thạch theo quãng bay (lưỡi lửa + khói cụm liền);
    - `VmNoLua` → `KmNo` luat;
    - cú cuối thêm đợt nổ sau lưng thay CauNo trùm kín;
    - cụm đốm, khói cụm.
- **Mong thấy ở ảnh SAU:**
  - tia vàng kem sáng, liền, từ Mặt Trời xuống đỉnh đầu đối thủ, bông toé liên tục ở chỗ chạm;
  - nổ có khói than lòi quanh thân, vòng cung trên cát, vết nứt;
  - khói thành cụm bay lên tách dần.
- **Còn lo:**
  - Mặt Trời và đoạn tia là hình của rig (không đổi màu được ở lớp hạt): tia hạt vẽ sau tướng có thể nằm dưới "đoạn tia" của rig. Nếu đoạn tia rig vẫn tối, cần tắt nó ở rig (`quai/doi_vua_may.py`).
  - Chỗ chạm đặt ở 0,28 tH trên tâm thân: tướng thấp dẹt có thể thấy bông hơi cao.

### Thần Cơ (thiet_phu, HatRobot.cs)

- **Lỗi ở ảnh TRƯỚC:**
  - mana 03–15: cầu nhỏ trơn, hạt hút gần như không thấy, vòng viền đen;
  - mana 16–20: đuôi cầu là chuỗi cục cam;
  - mana 21–26: chớp + cầu lửa trùm kín đối thủ;
  - mana 27–30: khói chấm đen lẻ;
  - ult 09–20: đuôi tên lửa là chuỗi bóng xám rời;
  - ult 24–26: nổ cuối che kín;
  - ult 27–35: khói lẻ.
- **Đã sửa:**
  - `NRobotBan`, `NRobotCau`: cầu nhiều múi theo nhịp đập; vệt xoắn ốc nhập cầu (dày dần); vòng co về cầu ở mỗi nhịp nạp; nén trước khi nhả; đuôi liền theo quãng bay; nổ `KmNo` vtuoi 1,6 (lõi sau lưng) + bông va chạm + vòng cung hai đợt; ít đá hơn.
  - `RbTen`: khói cụm liền theo quãng bay (bước 0,7 thân tên lửa).
  - `RbNoTen` → `KmNo` luat nhỏ.
  - `NRobotTen`: ba đợt `KmNo` luat; cụm đốm ở lõi ngực.
  - `RbHoiXi`, `RbPhut`: khói xám cụm.
- **Mong thấy:** tờ xem trước `s_robot_cau.jpg` đã thấy cầu gai xoáy, vệt xoắn ốc, đuôi liền, khói cụm lòi quanh đối thủ rồi tách.
- **Còn lo:** chiêu cuối đỉnh 137 hạt (trước 340).

### Pháo Giáp (ung_thep, HatPhao.cs)

- **Lỗi ở ảnh TRƯỚC:**
  - mana 10–20: vệt khói các quả pháo là chuỗi bóng xám;
  - mana 16–20: nổ khói chấm;
  - ult 12–21: cầu có vòng viền đen;
  - ult 24–27: vòng to + chớp che đối thủ.
- **Đã sửa:**
  - `PfVet` / `PfDuoi`: đuôi khói cụm liền theo quãng bay; `PfKhoiHong`: cụm khói nhiều múi.
  - `NPhaoBan`: bông + `KmNo` luat.
  - `NPhaoMua`:
    - năm quả: khói thưa, cụm to, ngắn đời;
    - 15 tên lửa: một nửa kéo khói, nửa kia chỉ lửa phụt (ngân sách);
    - nổ cuối `KmNo`.
  - `NPhaoCau`: cầu theo nhịp, hút xoắn ốc, vòng co, nén → chớp; đuôi liền; trúng: bông + `KmNo` vtuoi 1,8 + vòng cung hai đợt (giữ sét giáng và giật điện).
- **Còn lo:** chiêu mana đỉnh 143 hạt (trước 532), vẫn trên 120 vì 15 tên lửa bay cùng lúc.

### Thiết Cưa (phi_thuong, HatCua.cs)

- **Lỗi ở ảnh TRƯỚC:**
  - ult 08–21: khói giật dây là vài chấm xám rất nhỏ;
  - ult 22–31: tia lửa cưa lấm tấm, yếu.
- **Đã sửa:**
  - giật dây: cụm khói than nhiều múi to dần mỗi lần, có tro, tách cụm;
  - máy nổ: chớp nhỏ + ba khối khói to đáy ánh lửa + tia bắn rồi khựng;
  - hút khí: vệt gió xoắn ốc vào đĩa cưa + hai vòng co;
  - `CuTrung`: bông va chạm, tia lửa cưa nhanh rồi khựng, màu kem vàng.
- **Mong thấy:** `s_cua_lien.jpg` đã thấy khói cụm sau đĩa cưa.

### Quỷ Xích (khien_bac, HatXich.cs)

- **Lỗi ở ảnh TRƯỚC:**
  - ult 03–17: vệt lửa và khói lúc quay xích rải rác thành cục rời;
  - ult 22–34: cột lửa lốm đốm hạt;
  - ult 35–44: khói tan thành chấm.
- **Đã sửa:**
  - vệt quay theo **quãng đường móc**: lưỡi lửa + khói cụm liền;
  - lửa trên vòng trói và mép trước cột: lưỡi chữ S có giọt tách (kr_lua);
  - cột lửa: ít lưỡi hơn mà to hơn (một khối, một viền), đỉnh là khói cụm than đáy ánh lửa, giọt lửa, cụm đốm;
  - hai vòng có viền mực dưới chân → vòng cung không viền + vệt cháy;
  - các `Explode` → `KmNo` nhỏ; thả: khói cụm.
- **Còn lo:**
  - Đỉnh 153 hạt (chưa tính 28 mắt xích của vòng trói); trước 306.
  - **File sinh tự động** từ `ArtGen/Spine/quy_xich_hat_cs.py` (xem đề xuất).

### Vong Kỵ (tam_kiem, HatHon.cs)

- **Lỗi ở ảnh TRƯỚC:**
  - ult 18: vòng xanh viền mực quanh kiếm;
  - ult 27–30: chớp hồn 0,9 thân + vòng trùm kín đối thủ.
- **Đã sửa:**
  - hút khí hồn: vệt xanh xoắn ốc vào mép vá + ít lưỡi lửa + vòng co;
  - aura: lưỡi chữ S hồn có giọt;
  - nhát bổ trúng: **nổ hồn** `KmNo` "hon" với khói hồn hai tông, vòng cung dẹt, cột lửa hồn phần lớn sau lưng;
  - mana: hồn cuối nổ hồn `KmNo`;
  - `HonTrung`: bông va chạm, tia khựng;
  - các vòng → không viền.
- **Còn lo:** **file sinh tự động** từ `ArtGen/Spine/ky_nguyen_hat_cs.py`.

### Sói Giáp (chien_than, HatSoi.cs)

- **Lỗi ở ảnh TRƯỚC:** ult 16–40: hiệu ứng nhỏ, gió tụ không thấy.
- **Đã sửa:**
  - tụ lực: vệt gió xoắn ốc vào khiên + vòng co giữa chừng;
  - `SgTrung`: bông va chạm, tia khựng;
  - `SgDat`: vòng cung không viền;
  - húc: chớp 2 khung nhỏ thay chớp 0,62 thân.

### Thiết Tinh (bo_cap, HatSat.cs)

- **Lỗi ở ảnh TRƯỚC:** ult 20–24: chớp 0,95 thân + màn trắng che kín, vòng có viền.
- **Đã sửa:**
  - chớp nhỏ ở chân, hai vòng cung không viền;
  - `SatTrung` và tông: bông va chạm, tia bạc khựng, chớp nhỏ hơn;
  - màu chớp tươi.

### Thiết Khoáng (bo_ngua, HatKhoang.cs)

- **Lỗi ở ảnh TRƯỚC:** ult 21–30: chớp lớn che, vòng có viền.
- **Đã sửa:**
  - `KhDap`: chớp nhỏ, vòng cung không viền, vệt đất xới;
  - `KhGam`: bông va chạm, tia khựng;
  - màu đất, quặng tươi hơn.

### Thiết Vệ (doc_giac, HatGiao.cs)

- **Lỗi ở ảnh TRƯỚC:** ult 18–21: màn trắng (từ rig); 24: chớp trúng to.
- **Đã sửa:**
  - `GiaoTrung`: bông va chạm, tia khựng, chớp nhỏ hơn (dùng chung cho Quỷ Xích);
  - dậm giáo: chớp nhỏ + vòng cung không viền;
  - vệt sau kim 0,6 → 0,25 mỗi bước con (trước vượt ngân sách vì tính theo bước 120 Hz).

## Số hạt sống tối đa (trước → sau, ngoài Unity, dạng 2)

| Chiêu | Trước | Sau |
|---|---|---|
| n_vua_tia | 169 | 78 |
| n_vua_nhat | 342 | 148 |
| n_vua_an | 85 | 63 |
| n_robot_cau | 191 | 80 |
| n_robot_ten | 340 | 137 |
| n_phao_mua | 532 | 143 |
| n_phao_cau | 232 | 109 |
| n_xich_lua | 306 | 153 (+28 mắt xích) |
| n_hon_kiem | 135 | 105 |
| n_cua_lien | 65 | 77 |
| n_soi_huc | 115 | 117 |
| n_kim_sat | 135 | 99 |

Các chiêu còn lại dưới 90.

## Đề xuất sửa file chung

1. ~~Móc "đối thủ chớp + giật"~~: **đã làm** bằng `HatLua.NuocPulse` có sẵn (xem mục "Việc thêm" bên dưới).
2. **Truyền `StageView.Power(side)` vào HatLua** (vd. `hat.Epic`) để hệ Kim nhân số hạt / cỡ nổ theo độ khó trận. Hiện chỉ nhân theo dạng (`manh`).
3. **`Pal` của HatLua.cs:** tôi thêm `"vtuoi"` (năng lượng tươi) và `"luat"` (lửa đỏ cam) **lúc chạy** bằng `KmPal()`. Nên khai tĩnh trong bảng `Pal`.
4. **Đưa bộ `Km*` (HatRobot.cs) lên file chung** (HatLua.cs hoặc file mới) cho các hệ khác dùng, và thay `Explode` / `CauNo` cũ:
   - hai hàm này vẫn là kiểu chớp to + cầu lửa trùm đối thủ;
   - Kim đã bỏ dùng hẳn.
5. ~~Khuôn của hai script sinh HatHon.cs, HatXich.cs~~: **đã chép** (xem mục "Việc thêm" bên dưới).
6. **Ngân sách:** bốn chiêu (n_vua_nhat, n_robot_ten, n_phao_mua, n_xich_lua) vẫn 137–153 hạt (sân ≤ 120). Đề xuất:
   - một trần cứng ở `HatLua.Add` (bỏ hạt phụ khi > 140); hoặc
   - chấp nhận cho chiêu cuối.
   - n_phao_mua là chiêu mana: muốn dưới 120 thì phải bớt số tên lửa (đổi ý tưởng, cần người dùng).
7. **Themes trong HatLua.cs** cho các tướng Kim (spark, ember, ring của bo_cap, doc_giac, chien_than…) còn tông xám. Tôi đã ghi đè màu tại chỗ, nên nâng sáng ở bảng gốc cho đồng bộ.
8. **Rig:** màn trắng / màn tối ở cú trúng chiêu cuối của Thiết Tinh, Thiết Khoáng, Thiết Vệ đến từ `impactFlash` của rig (ảnh TRƯỚC: bo_cap 20, bo_ngua 27, doc_giac 18–21), không phải lớp hạt. Nên giảm alpha ở rig nếu người dùng thấy bạc màu.

## Việc thêm (theo tin nhắn của phiên chính)

### 1. Chép phần đã sửa vào khuôn hai script sinh

- `ArtGen/Spine/ky_nguyen_hat_cs.py` (HatHon.cs) và `ArtGen/Spine/quy_xich_hat_cs.py` (HatXich.cs): khuôn `KHUNG` nay chứa toàn bộ phần đã sửa. Giữ CRLF như file gốc.
- Cách dựng: tự động bằng `...\scratchpad\kim_vfx\doi_khuon.py`.
  - So khuôn cũ với bản sinh để tìm vùng chỗ trống (`@BANG@`, `@S_LEAD@`…, `/*BANG*/`, `/*LAY*/`).
  - So bản sinh với bản mới để lấy phần sửa.
  - Phần sửa không đè vào vùng chỗ trống nào.
- **Kiểm:**
  - Trước khi đổi, khuôn cũ sinh ra đúng từng byte bản HEAD.
  - Sau khi đổi, chạy script với `RA` trỏ ra thư mục nháp (`...\scratchpad\kim_vfx\sinh\`, qua `sinh_nhap.py`, không ghi Assets). Bản sinh khớp từng byte với `HatHon.cs`, `HatXich.cs` mới, chỉ khác CRLF: script vốn ghi LF, file trong Assets là CRLF, như trước đây.
  - Hash hai file .cs trong Assets không đổi sau khi chạy script.

### 2. Đối thủ chớp và giật theo nhịp (`HatLua.NuocPulse`)

- **Hàm chung `KmNhip(k)`** (HatRobot.cs) gọi `NuocPulse?.Invoke(k)`.
  - Có chặn dày: hai nhịp nhẹ (k < 0,9) cách nhau dưới 0,08 s thì bỏ nhịp sau, để loạt tên lửa hay giật điện không thành nhấp nháy liên hồi.
  - Cú trúng chính (giờ trả về của hàm chiêu) do StageView lo, nên không gọi trùng ở đó.
- **Nhịp tia (`KmCham`):** nhịp đầu k = `dau` (mặc định 1) lúc đầu tia chạm; sau đó khoảng 7 nhịp/giây k = 0,4; tia vỡ cuối k = 0,6.
- **Từng chiêu** (chạy ngoài Unity, giờ:k):

| Chiêu | Nhịp | Ghi chú |
|---|---|---|
| Nhật Vương tia | 1,37:0,4 · 1,51:0,4 · 1,63:0,6 | Đầu tia chạm 1,22, chỉ 0,02 s trước cú trúng chính 1,24, nên bỏ nhịp đầu |
| Nhật Vương thiên thạch | 1 · 0,5 · 0,4 | Thiên thạch 1, thiên thạch 2, đợt nổ sau cú cuối |
| Thần Cơ tên lửa | 0,4 (quả thứ ba 0,6) | Quả đầu là cú trúng chính; nổ cuối 0,9, đợt hai 0,4; chiêu mana đợt nổ thứ hai 0,4 |
| Pháo Giáp chiêu mana | 0,4 / 0,6 | 15 tên lửa, chặn dày còn 6 nhịp; nổ cuối 0,7 |
| Pháo Giáp chiêu cuối | 0,5, rồi 0,35 | Nổ đợt hai 0,5; giật điện 0,35 mỗi nhịp (8 lần/giây) |
| Thiết Cưa chiêu cuối | 0,4 · cuối 0,8 | Nhát 2–10: 0,4; nhát cuối 0,8 |
| Quỷ Xích chiêu cuối | 0,8 · 0,6 · 0,4 | Trói 0,8; cột lửa 0,6; nhịp đốt 2–4: 0,4 |
| Vong Kỵ chiêu mana | 0,4 · cuối 0,8 | Hồn 2…n: 0,4; hồn cuối 0,8 |
| Thiết Tinh chiêu mana | 0,4 · cuối 0,8 | Viên 2…: 0,4; viên cuối 0,8 |
| Thiết Khoáng | 0,4 · cuối 0,8 · húc 1 | Chiêu mana mảnh 2…: 0,4, mảnh cuối 0,8; chiêu cuối dạng 2 húc lần một 1 |
| Thiết Vệ chiêu cuối | 0,4 · cuối 0,8 | Kim 2…: 0,4; kim cuối 0,8 |

- Số hạt không đổi, giờ trả về không đổi: `ket_qua_nhip.txt`.
- Lần biên dịch cuối 0 lỗi (Core, Game, Editor); đã chép đè 10 file vào Assets, hash ở `hash_moi2.txt`.
