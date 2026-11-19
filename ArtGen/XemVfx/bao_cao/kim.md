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

## Đợt khung vẽ sẵn 2026-11-19 (flipbook, HatFlip.cs)

Bản sửa ở `scratchpad/fb_kim/` (bản gốc lúc chép ở `fb_kim_base/`), chưa chép vào Assets, chưa soi trong Unity (phiên khác đang dùng). Biên dịch thử
ngoài Unity (`ArtGen/Spine/quai/tho5_game/bien_dich_thu.py`): Core, Game, Editor đều 0 lỗi.

**Hàm dùng chung** (mọi tướng Kim gọi các hàm này đều đổi theo; chưa nhập ảnh khung thì giữ bản hạt):
- File mới `HatFbKim.cs` (partial HatLua): `KmNoFb`, `KmKhoiFb`, `KmLuaFb`, `KmFbMoc`, `KmGaiVong`, `KmCotLuaFb`, `KmCauBam`, `KmBuiFb`.
- `HatRobot.cs`:
  - `KmNo`: lửa đỏ cam / năng lượng vàng. Nổ to (sc ≥ 0,8) ra khung `no`, neo ở đất dưới tâm, SAU tướng, cao 1,6 D (chiêu cuối 1,4–1,55 thân), lật xen kẽ. Nổ nhỏ ra khung `trung_lua` ở tâm, cao 1,5 D (0,5–0,75 thân), nhanh 1,3 lần; loạt tên lửa, nhịp đốt (sc < 0,45) thì một nửa vẽ sau tướng. Bỏ khối khói múi tròn và lưỡi liềm. Giữ chớp 2 khung, vòng cung dẹt, vệt cháy, tia, đá, mảnh. Lửa hồn giữ bản hạt; khói trong đó ra 1–3 khung `khoi` to hơn.
  - `KmKhoi`: cụm khói than / khói hồn (nhiều múi) ra khung `khoi`, cao 3 r, tốc độ theo đời. Không đổi: khói một múi (đuôi đạn, hơi xì), cụm con, khói xám nhạt `KmXam` (khung nâu xám nhân màu không sáng lên được).
  - `KmLuaS` (lửa đỏ cam): ra khung `lua_lap`, mọc, cháy, co tại chỗ. Lửa hồn xanh giữ hạt.

### bo_cap (Thiết Tinh): đợt khung vẽ sẵn 2026-11-19
- Chiêu cuối `n_sat_dap`: 9 cột kim rời → `KmGaiVong`, 5 cụm khung `gai_sat`:
  - nhuộm oải hương `C(228,212,255)` / thép lam `C(212,224,255)`;
  - sau lưng: cụm giữa 1,15 thân, hai cụm bên 0,88; phía trước hai bên: 0,62;
  - bỏ 5 khung nứt, chạy 1,5 lần (đủ cao ~0,17 s, vỡ hết ~0,53 s như cột cũ);
  - dăm 12 → 6, bụi 10 → 4 (khung đã có bụi, vụn);
  - giữ chớp, hai vòng cung, đá, chớp phụ 0,18 s.
- Đòn thường, chiêu mana giữ nguyên: va chạm thép, tinh thể của rig, không có khung tương ứng.

### bo_ngua (Thiết Khoáng): đợt khung vẽ sẵn 2026-11-19
- Chiêu cuối (`KhDap`): vòng cột quặng → `KmGaiVong`, nhuộm theo dạng:
  - dạng 1 quặng sắt `C(196,200,214)` / `C(220,224,236)`;
  - dạng 2 hematit `C(245,140,112)` / `C(226,118,100)`.
- `KhDatToe` khi sc ≥ 0,85 (cắm hố, trồi lên, trồi lần hai, húc từ dưới, cú giáng đòn thường dạng 2): bụi là 2 khung `khoi` nhuộm nâu đất (`KmBuiFb`), sau tướng, thay 6·sc cụm bụi rời. Giữ gợn, cục đất, đá.
- Chiêu mana (các cú găm), đòn thường dạng 1 giữ nguyên.

### doc_giac (Thiết Vệ): đợt khung vẽ sẵn 2026-11-19
- Không đổi (`HatGiao.cs` y nguyên): giáo, kim sắt là vật bay + va chạm thép, không có nổ / lửa / gai đâm lên.

### phi_thuong (Thiết Cưa): đợt khung vẽ sẵn 2026-11-19
- Chiêu cuối:
  - giật dây: khói ra khung `khoi` (qua `KmKhoi`), mỗi lần MỘT cụm to dần (cao ~0,3 → 0,45 → 0,63 thân). Trước là 1 / 2 / 3 cụm cùng chỗ: nhiều khung chồng thành bóng đôi;
  - máy nổ: 2 cụm (0,66 + 0,46 thân, cụm hai lệch ra sau, lên trên) thay 3. Chớp, tia lửa giữ.
- Đòn thường, chiêu mana (tia lửa cưa, dăm thép) giữ nguyên.

### khien_bac (Quỷ Xích): đợt khung vẽ sẵn 2026-11-19
- Chiêu cuối:
  - trói (`KmNo` 0,45): `trung_lua`;
  - cột lửa: thân cột (~90 lưỡi lửa rời) → 3 khung `lua_lap` chồng sâu sau lưng (`KmCotLuaFb`). Chân 0 / 0,27 / 0,5, cao 0,6 / 0,52 / 0,46 chiều cao cột, mọc dần từ dưới lên;
  - nổ chân cột: `no` ở dạng 2, `trung_lua` ở dạng 1;
  - mép trước, lửa liếm vòng xích (`KmLuaS`): `lua_lap`;
  - khói đỉnh cột, khói lúc thả: `khoi`;
  - bốn nhịp đốt: `trung_lua`.
- Giữ: vệt lửa + khói một múi lúc quay xích, lửa dọc xích, vòng xích, giọt, cụm đốm, vòng cung, khe nứt.
- Đòn thường, chiêu mana giữ nguyên.
- `HatXich.cs` là file sinh tự động: đoạn sửa trong `XqCotLua` phải chép vào `ArtGen/Spine/quy_xich_hat_cs.py` (xem cuối mục).

### chien_than (Sói Giáp): đợt khung vẽ sẵn 2026-11-19
- Không đổi (`HatSoi.cs` y nguyên): búa, gió, bụi, va chạm thép, không có khung tương ứng.

### thiet_phu (Thần Cơ): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: cầu trúng (`KmNo` 0,55) ra `trung_lua`.
- Chiêu mana:
  - nổ 1,6 ra `no` cao ~1,44 thân, sau tướng;
  - đợt hai 0,7 ra `trung_lua`;
  - khói muộn ra `khoi`.
- Chiêu cuối:
  - 7 tên lửa ra `trung_lua` (nhỏ, một nửa sau tướng);
  - ba đợt cuối: 1,55 ra `no`; 0,8 ra `no` (dạng 1 ra `trung_lua`); 0,6 ra `trung_lua`;
  - khói muộn ra `khoi`.
- Giữ: cầu năng lượng, hạt hút, đuôi, thân tên lửa + khói xám, hơi xì, cột năng lượng `RbCot`, sóng đất, nứt, đá.

### tam_kiem (Vong Kỵ): đợt khung vẽ sẵn 2026-11-19
- `HatHon.cs` không sửa (file sinh tự động). Đổi qua hàm chung:
  - khói của nổ hồn (hồn cuối chiêu mana, nhát bổ chiêu cuối) ra 1–3 khung `khoi` to, nhuộm xám xanh `C(170,225,205)`, thay 3–5 cụm;
  - khói hồn muộn sau nhát bổ ra `khoi` xám xanh.
- Lửa hồn xanh (lưỡi liềm, lưỡi lửa, aura) giữ hạt: nhuộm khung lửa cam ra xanh xỉn.

### ung_thep (Pháo Giáp): đợt khung vẽ sẵn 2026-11-19
- `HatPhao.cs` không sửa. Đổi qua hàm chung:
  - đạn sắt trúng ra `trung_lua`;
  - 15 tên lửa chiêu mana ra `trung_lua` nhỏ (một nửa sau tướng), nổ cuối 0,95 ra `no`;
  - chiêu cuối: nổ 1,8 ra `no` ~1,55 thân, đợt hai ra `trung_lua`;
  - khói muộn ra `khoi`.
- Giữ: khói họng pháo, đuôi đạn (xám nhạt), cầu năng lượng, sét, giật điện.

### kim_nghe (Nhật Vương): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: đường lửa dọc đất là cụm `lua_lap` nhỏ (~0,2 thân), cứ ba nhịp một cụm (~23 cụm/giây), mọc, cháy, co tại chỗ, thay lưỡi lửa rời. Tia, bụi giữ.
- Chiêu mana: nổ mặt trời 1,25 ra `no` (~1,24 thân, sau tướng); khói muộn ra `khoi`. Tia liền khối + va chạm (`KmTia`, `KmCham`) giữ nguyên.
- Chiêu cuối:
  - ba thiên thạch: khung `cau_lua` bám theo thiên thạch của rig (`KmCauBam`): sau tướng, cao 0,7 tH·sc, chỉ trong lúc thiên thạch hiện, hướng theo đường rơi thẳng của rig. Thay lưỡi lửa của đuôi; khói một múi, tia giữ;
  - nổ: `no` (hai cú đầu dạng 1 sc 0,68 ra `trung_lua`), đợt nổ sau cú cuối ra `no`;
  - khói muộn ra `khoi`.
- Không nhuộm tối gì (người dùng từng chê Mặt Trời, tia tối). Giữ màn nhật thực, Mặt Trời, `RbCot`.

### Chỗ còn ngờ (đợt khung vẽ sẵn)
- Chưa xem trong trận. Chỉ ghép thử thô bằng Python với đối thủ giả để kiểm điểm neo, cỡ, lớp: `scratchpad/kim_fb_soi/soi_kim_fb.jpg`.
- Nhuộm khung chỉ làm tối đi:
  - tinh thể oải hương ra ~(143,137,180), tối hơn `SatTim` cũ ~15 %;
  - khói hồn, bụi đất cũng sẫm hơn bản hạt.
- Khung `no` / `trung_lua` là lửa đỏ cam + khói nâu, nên nổ năng lượng vàng (Thần Cơ, Pháo Giáp, Nhật Vương) giờ ra đỏ cam. Không nhuộm cho khỏi tối; muốn vàng hơn cần bộ khung riêng.
- Hai nổ to sát nhau (Nhật Vương thiên thạch 1–2 cách 0,14 s, các đợt nổ phụ) đã lật xen kẽ, lệch 0,08 D. Vẫn thấy bóng đôi thì đổi đợt phụ sang `trung_lua`.
- Cỡ đá thiên thạch của rig chưa đo: `cau_lua` đặt 0,7 tH·sc (cầu ~0,39 tH·sc).
- Khói đỉnh cột lửa Quỷ Xích 6 cụm/giây ra 6–7 khung `khoi` chồng, có thể dày. Hạ tần suất phải sửa `HatXich.cs` + script sinh.
- Giữ hạt vì chưa có khung hợp: cột năng lượng `RbCot`, lửa móc / dọc xích Quỷ Xích, lửa hồn, khói xám nhạt họng pháo, đuôi đạn.

### Cần đổi ở file không thuộc phiên này
- `ArtGen/Spine/quy_xich_hat_cs.py` (khuôn sinh `HatXich.cs`): trong `XqCotLua`, bọc hai `Every` lưỡi lửa thân cột bằng `if (!KmCotLuaFb(feet, cao, dur)) { … }` như bản sửa. Không thì chạy lại script sẽ mất.
- Khi chép vào Assets: thêm file mới `HatFbKim.cs` cạnh `HatFlip.cs` (Unity tự sinh .meta). `StageView.cs`, `HatFlip.cs` không cần đổi.

## Đợt 2 (2026-11-19): nổ lên lớp trước, vệt khói đuôi, vòng gai to hơn

Người dùng xem trong game: "có vài vụ nổ layer nằm dưới địch nên không thấy rõ, các fireball, tên lửa,... nên thêm trail smoke vào". Phiên chính
soi ảnh chụp: vòng gai chiêu cuối Thiết Tinh / Thiết Khoáng bị thân đối thủ che gần hết. Bản sửa ở `scratchpad/fb_kim/`. Biên dịch thử:
Core, Game, Editor 0 lỗi.

**Nổ lên lớp trước** (`KmNoFb`, `HatFbKim.cs`; mọi tướng gọi `KmNo`):
- `no` (nổ to) và `trung_lua` (nổ nhỏ) đều vẽ TRƯỚC tướng, bỏ chỗ vẽ sau (cả nửa loạt tên lửa nhỏ trước đây vẽ sau).
- Neo như cũ, dời về phía người ra chiêu: 0,2 thân với nổ to, 0,1 thân với nổ nhỏ (cột lửa Quỷ Xích không có hướng: không dời).
- Nổ to vẫn che thân đối thủ ~0,5 s (khung 4–16).

**Vệt khói đuôi** (`FbKhoiDuoi` của `HatFlip.cs`; hàm mới `KmDuoiKhoi` trong `HatFbKim.cs` cho vật bay theo đường hàm giờ). Lớp 18: dưới lưỡi lửa đuôi và thân vật bay.

| Vật bay | Tướng | Cụm khói | Cụm/giây | Lớp |
|---|---|---|---|---|
| Tên lửa (`RbTen`) | Thần Cơ chiêu cuối | 1,4 dài thân (~0,25 thân tướng) | 22, tan nhanh 2,4 | Trước |
| Tên lửa nhỏ | Pháo Giáp chiêu mana | 1,4 × 1,3 dài thân (~0,18–0,2 thân tướng) | ~20 cho 2/3 số quả (dạng 1: cả hai), tan nhanh 2,6 | Trước |
| Đạn sắt, quả pháo vọt lên (`PfDuoi`) | Pháo Giáp | ~3 cỡ đạn | 24 / 17 | Trước |
| Cầu năng lượng bay | Thần Cơ đòn thường, chiêu mana; Pháo Giáp chiêu cuối | 2,4 R; tối đa 0,3 thân | 18 / 22 / 22 | Trước |
| Thiên thạch (sau khung `cau_lua`) | Nhật Vương chiêu cuối | 0,22 thân × cỡ (tối đa 0,3) | 40 (chỉ hiện ~0,17–0,27 s) | Sau |
| Móc xích lửa lúc quay | Quỷ Xích chiêu cuối | 0,24 thân | 22 | Sau |

- Có vệt mới thì bỏ chuỗi khói một múi cũ (không để cả hai).
- Pháo Giáp: chỉ 2/3 số tên lửa kéo khói, cho đủ ngân sách hạt (đỉnh ước ~55 cụm khói).
- Không thêm khói: hồn bay Vong Kỵ (lửa hồn, file sinh), tinh thể, kim sắt, giáo, búa (không phải vật cháy).
- Cầu năng lượng kéo khói là tôi tự chọn (yêu cầu ghi "nếu hợp"). Thấy không hợp thì bỏ ba dòng `KmDuoiKhoi` ở `NRobotBan`, `NRobotCau`, `NPhaoCau`.

**Vòng gai to hơn** (`KmGaiVong`, `HatFbKim.cs`):
- Ba cụm sau: giữa 1,35 thân; hai cụm ±0,42 thân cao 1,1, ló trên vai.
- Hai cụm trước 0,9 thân, lệch ±0,6 thân hai bên chân.
- Thêm một cụm thấp 0,5 chếch phía trước (±0,22, bên ngẫu nhiên).
- Không có cụm cao ngay trước mặt. Ghép thử: `scratchpad/kim_fb_soi/soi_kim_fb2.jpg`.

**`HatXich.cs` là file sinh** (`ArtGen/Spine/quy_xich_hat_cs.py`). Trong `NXichLua`, ngay sau `int demQ = 0;` thêm:
```
bool fbKhoi = HasFb("khoi");
if (fbKhoi) At(XqSLua * k, () => KmDuoiKhoi(t => Moc((t - T0) / k), dQuay, 0.24f * casterH * manh, 0.04f * casterH, 22, Back));
```
Và đổi `if (demQ++ % 2 == 0)` thành `if (!fbKhoi && demQ++ % 2 == 0)`.

## Đợt 3 (2026-11-19): tia vẽ sẵn (TiaFb)

Người dùng: "tia năng lượng/nước như này nhìn vẫn chưa đã" (ống thẳng đặc, chỗ trúng nhỏ). Biên dịch thử: Core, Game, Editor 0 lỗi.

- Hệ Kim chỉ có MỘT tia thật: tia Mặt Trời chiêu mana Nhật Vương (`NVuaTia`, `HatVua.cs`). Đã soát:
  - Thần Cơ, Pháo Giáp: cầu năng lượng bay, tên lửa, không có tia thẳng;
  - Thiết Tinh: tinh thể bay;
  - cột năng lượng dựng đứng `RbCot`: giữ;
  - cả 10 tướng đều có mã riêng nên không tướng nào đi tia cũ của `StageView`.
- `NVuaTia`, khi `HasTia(DaTiaVang)`:
  - `TiaFb(DaTiaVang, dinh, cham, 0,22·casterH·manh, …)` gọi lúc Mặt Trời lên đỉnh cột (`tDinh`), nên cầu đầu nòng lớn dần đúng pha tụ ở đỉnh;
  - `tTu = (tBan + lao) − tDinh − tVuon`, `tBan = tTat − (tBan + lao)`: giờ chạm, giờ tắt như cũ;
  - vẽ TRƯỚC tướng, đè lên đoạn tia tối màu của rig;
  - chỗ trúng dời lên đỉnh đầu đối thủ (thân − 0,42 tH; trước là −0,28 vì tia cũ đi sau thân), tia không xuyên mặt.
- Giữ: nhịp `KmNhip` (bỏ nhịp đầu; 0,4 bảy lần/giây; 0,6 lúc tắt), rung theo nhịp, chớp + vòng ở đỉnh lúc bắn, chớp ở từng hành tinh lúc đầu tia đi qua (theo giờ vươn mới), tia lửa văng hai bên thân, tia kim loại bắn ngược ở chỗ trúng (16/giây), nổ mặt trời lúc trúng chính. Giờ trả về không đổi.
- Bỏ khi có khung: `KmTia` (thân tia liền khối), `KmCham` (bông va chạm cũ). Chưa nhập ảnh thì đi đường cũ y nguyên.
- Còn ngờ: tia vẽ trước tướng nên che phần giữa ba hành tinh của rig (trước đây tia đi sau, xuyên qua hành tinh). `TiaFb` dùng một lớp cho cả thân và bông trúng, nên không tách được thân sau / bông trước.
- Không sửa file sinh tự động.
