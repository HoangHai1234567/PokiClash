# Báo cáo VFX hệ Hỏa (2026-11-18)

File đã sửa trong `Assets/01 Script/Game/Battle/`:
- `HatLua.cs`, `HatNhan.cs`, `HatNham.cs`, `HatPhap.cs`;
- `HatDat.cs`, `HatHo.cs`, `HatNuiLua.cs`, `HatRua.cs`.

Biên dịch (`bien_dich_thu.py`, đọc thẳng từ Assets): Core, Game, Editor đều 0 lỗi. Bản gốc và hash nằm ở `Temp/vfx_hoa/goc/`.

Kiểm tra đã làm:
- **Không mở Unity.**
- Chạy lớp hạt bằng mono ngoài Unity (bộ chạy thử ở scratchpad). Không có ảnh nên mỗi nét vẽ ra một elip. Cách này chỉ soi được chỗ đặt, nhịp, số hạt, số Image; **chưa soi được hình thật**. Phiên chính cần chụp tour trong Unity.

## Thay đổi chung (HatLua.cs, khối "BỘ HỎA 2026-11-18")

Các hàm mới đều tên `Hoa…`, chỉ tướng Hỏa gọi. Các hàm `Explode`, `Smoke`, `Ember`, `CauNo`, `Ring`, `Tongue`, `LoiCau` và bảng `"lua"` giữ nguyên, vì hệ Kim và Thổ đang mượn. `AtkLao`, `CastLao` không đụng.

**Màu tươi:**
- Bảng mới `"hoa"`: đỏ tươi E8452E, cam FFA43A, vàng FFD94A, kem FFF6D6. Vòng và tàn lửa dùng cam đỏ F0702A.
- 9 tướng Hỏa chuyển sang `"hoa"`; thêm dòng `Themes` cho `su_tu_lua`.
- `"vang"` (Hỏa Cung) làm tươi hơn.
- Dung nham (`"nham"`, mảng `Lava`, vũng, vết bắn): vỏ nâu đỏ ấm 8A3A22, lõi cam vàng.

**Khói thành cụm, `HoaKhoi`:**
- Mỗi cụm là một khối nhiều múi: ảnh `kr_khoi` cộng bóng đáy `kr_khoiday`; chưa có ảnh thì 3–4 múi sblob.
- Hai tông (đáy đậm, đỉnh nhạt), chung một viền mực. Viền mực nhạt đi trước phần ruột.
- To gần đủ ngay (12 % đời), bay lên và nhanh dần.
- Ở 48 % đời tách thành 3 cụm nhỏ (`kr_khoinho`) toả ra, có tro, rồi mới mờ.
- Màu đen than ngả xám. Khói nổ còn lõi lửa nguội ở đáy.
- Khói đuôi đạn, `HoaDuoiKhoi`: sinh theo **quãng bay** (KR5), các cụm chồng mép nhau nên đuôi liền dù đạn nhanh.

**Nổ kiểu KR5, `HoaNo`:**
- Cục chớp nhỏ 2 khung, rồi chớp sao gai (`kr_chop`).
- Khối khói hai tông sau lưng con bị trúng, xoè hình quạt lên trên và sang hai bên để ló ra quanh viền thân (đặt giữa tâm thì bị thân che hết, đã soi thấy).
- Lưỡi liềm lửa (`kr_liem`, style `"liem"`) cong ra ngoài, teo thành đốm.
- 1–2 lưỡi lửa chữ S, tia văng hai đợt cách 0,1 s, cụm tàn lửa.
- Biết chân thì thêm vòng cung dẹt trên đất (`HoaCung`, `kr_cung`, không viền mực). Nổ từ cỡ 0,8 có thêm vệt cháy (`HoaVetChay`, giữ khoảng 1 s rồi mờ).
- `HoaCauNo` thay `CauNo` cho tướng Hỏa: `HoaNo` cộng quạt lửa theo hướng bay, phần lớn sau lưng.

**Lửa liền khối:**
- Style `"krl"`: lưỡi chữ S `kr_lua`, co lớp quanh chân theo điểm neo (0,5; 0,9).
- `HoaLuoi`: đổi hạt sang `"krl"` và bỏ khói lẻ, tàn lẻ khi chết. Đây là nguồn chính của "chấm đen rải rác".
- `HoaLuaBam`: lửa bám chỗ trúng, dùng `kr_luachum` + `kr_luachuml`, kèm giọt lửa tách bay lên.

**Đốm lửa, `HoaTan`:** cụm 3–6 đốm lệch cỡ, nhỏ bằng 0,5–0,7 lần cỡ cũ, thay các đốm `Ember` đơn lẻ.

**Dung nham:**
- Giọt là giọt lệ kéo dài theo tốc độ (`kr_nhamgiot`, đầu tròn đi trước), không còn chuỗi ba cầu tròn.
- Cột dung nham dùng style `"krn"`: cụm mềm `kr_nham`, giọt kéo tuột lại sau, nguội dần về màu vỏ.

**Tụ cầu, `HoaTuCau` + `HoaHut` + `HoaVongCo` + `HoaCau`:**
- Hạt bị hút là vệt thuôn (`kr_vet`), hiện dần từ trong suốt, bay xoắn ốc vào tâm và nhanh dần (ease-in), chạm vành cầu thì nhập vào. Mật độ tăng dần tới lúc nhả.
- Có hai vòng co về tâm.
- Cầu là **một hạt** khối lửa nhiều múi cuộn (`kr_luakhoi`, hoặc `kr_cau`; chưa có ảnh thì lõi + 6 múi lửa quanh vành). Đổi khung 15 hình/giây, lớn dần, đập khoảng 4 nhịp/giây.
- 0,07 s trước lúc nhả cầu nén còn 0,78, rồi chớp.
- Cầu một hạt này thay chùm `LoiCau` (khoảng 13 hạt × 5 lớp).

**Va chạm của tia và luồng, `HoaBong`:** bông lửa `kr_tiadau`, gốc toé đặt đúng chỗ chạm (điểm neo 0,055; 0,5), toé ngược về phía người bắn. Đổi khung mỗi 2 khung sân, cỡ đập.

**Ảnh `kr_*`:**
- Có ảnh thì dùng, chưa có thì quay về hình cũ.
- Bản đặc vẽ thêm 3 đơn vị vì đã nở sẵn viền.
- `kr_vet`, `kr_nhamgiot`, `kr_cung` tính lại khung theo phần ảnh chiếm trong khung (ảnh nằm ngang hoặc đã dẹt sẵn).

**Móc chớp + giật:**
- Mã `"n_"` gọi `NuocPulse?.Invoke(k)` (đi qua `PlayNuoc`).
- Mã không qua `PlayNuoc` gọi `HoaTrung?.Invoke(chỗ, k)`. Móc này mới thêm và **chưa ai gắn**, xem đề xuất 1.

**Số hạt sống lớn nhất / số Image lớn nhất** (đo bằng bộ chạy thử, không có ảnh):

| Chiêu | Trước | Sau |
|---|---|---|
| tia_mat | 74 / 210 | 41 / 154 |
| cầu lửa mặc định | 96 / 295 | 55 / 243 |
| phun | 71 / 186 | 49 / 218 |
| dat_trao | 138 / 830 | 97 / 344 |
| quyen_xoay | 172 / 431 | 111 / 355 |
| n_cau_sung | 165 / 444 | 74 / 300 |
| n_ho_anh | 207 / 527 | 114 / 388 |
| n_dat_dam | 135 / 794 | 101 / 352 |
| n_nui_ten | 412 / 966 | 159 / 594 |

`n_nui_ten` là chiêu cuối của boss cuối nên còn vượt 120 hạt.

## Từng tướng

### Tiểu Quỷ Lava (su_tu_lua): cầu lửa mặc định (`HatLua.Fireball`)

**Lỗi ở ảnh TRƯỚC:**
- Cầu nhỏ, tròn, màu hồng nâu (mana_05–10).
- Đuôi khói là chuỗi hạt xám nâu (09–12).
- Nổ gồm sao và vòng nâu, lửa vụn, khói tan nhanh và rải rác (12–18).
- Chiêu cuối không có hạt nào (FireFx thiếu dòng). Thân tướng nhảy ra khỏi khung, bị cắt (ult_06–21).

**Đã sửa:**
- Tụ bằng `HoaTuCau`: vệt xoắn ốc, vòng co, cầu nhiều múi đập, nén, chớp.
- Lưỡi lửa liếm quanh cầu.
- Lúc bay: cầu nhiều múi, đuôi lưỡi chữ S, khói đuôi theo quãng.
- Lúc trúng: `HoaCauNo` (0,85), có vòng cung và vệt cháy dưới chân.
- Dòng Themes riêng, màu tươi.

**Mong thấy:** cầu to rõ, có múi; đuôi lửa liền; khói đuôi thành vệt; nổ có khói hai tông ló quanh đầu đối thủ.

**Còn lo:** chiêu cuối cần dòng FireFx (đề xuất 2).

### Hỏa Nhãn (hoa_nhan): tia_mat, quyen_xoay (`HatNhan.cs`)

**Lỗi ở ảnh TRƯỚC:**
- Lõi tia mảnh, vàng nâu ngả khaki (mana_10–18).
- Đầu tia cắm vào giữa thân, không có bông va chạm; lưỡi lửa trùm mặt đối thủ (12–19).
- Tia biến mất cụt trong 1–2 khung (18 → 20).
- Khói là chấm đen rải rác (16–24).
- Chiêu cuối: lửa xoáy nhỏ, khói xám rải rác (ult_27–36).

**Đã sửa `TiaMat`:**
- Đầu tia dừng ở mặt trước thân, phình tròn (nắp tròn bằng mảng liền, chung viền mực với thân tia).
- Lõi 5 lớp tươi: mực, đỏ, cam, vàng, kem.
- `HoaBong` toé ngược suốt dòng. Lưỡi lửa dạt dọc mặt thân, nửa sau lưng. Khói cụm sau lưng.
- Lưỡi lửa bám tia chỉ mọc trên đoạn tia đã hiện.
- Hết dòng: đuôi rút tới chỗ chạm, tia mảnh dần, vỡ thành lưỡi lửa và khói, nổ nhỏ kết.
- Giờ trúng vẫn là lúc đầu tia chạm thân. `TiaMatHold` vẫn 1,0.

**Đã sửa `QuyenXoay`:** lưỡi xoáy chữ S; mỗi nhát `HoaNo`; nhát cuối có vòng cung và vệt cháy; khói cụm.

**Mong thấy:** đầu tia có "va" rõ, bông lửa đập liên tục; tia rút và vỡ chứ không cắt phụt.

**Còn lo:**
- Đối thủ chỉ chớp một lần lúc hiện sát thương, vì `HoaTrung` chưa gắn (đề xuất 1).
- Kiểm tia ở cả hai chiều bắn và trong ô xem tướng.

### Hỏa Cung (kim_su): ten, no_lon

**Lỗi ở ảnh TRƯỚC:**
- Ba nổ vàng tí xíu, gần trùng chỗ (mana_12–16).
- Chiêu cuối: vòng nâu, cột lửa trùm đối thủ (ult_27–30), khói đen chấm (33–39).

**Đã sửa:**
- `TenNo`: mỗi mũi tên một `HoaNo` nhỏ; quạt lửa theo hướng tên (hai lưỡi bên sau lưng); tia văng ngược; lửa còn bám chỗ găm 0,7 s (`HoaLuaBam`); khói cụm sau đó.
- `PlayMana` truyền thêm chân tướng và chân đối thủ (tham số tuỳ chọn, StageView không đổi).
- `BigBurst` (no_lon): vòng cung và vết nứt báo trước, cột lưỡi chữ S ôm thân (thưa hơn), `HoaNo` ở 0,18 s, nổ phụ 0,34 s, khói cụm. Giờ trả về vẫn 0,18.

**Còn lo:** bảng `"vang"` và khói nâu riêng của tướng này phải xem trên máy.

### Nham Thần (nham_than): phun, n_cau_lan, n_nham_va (`HatNham.cs` + `Breath`)

**Lỗi ở ảnh TRƯỚC:**
- Luồng phun trùm kín mặt đối thủ; cuối luồng cụt, không toé (mana_10–17).
- Khói là chấm đen (14–18).
- Chiêu cuối: vệt lửa lăn thành chuỗi cục (ult_15), chấm khói đen dọc đường (18–21).

**Đã sửa `Breath`:**
- Lửa dừng ở mặt trước thân (0,26 tH), rồi dạt sang hai bên, 55 % sau lưng.
- `HoaBong` cộng lưỡi lửa dạt dọc mặt thân suốt luồng.
- Lấy hơi bằng vệt xoắn vào miệng. Khói cụm 4,5 lần/giây. Lưỡi chữ S.

**Đã sửa `NCauLan`:** vệt lửa `HoaLuoi`, khói đuôi cụm, `HoaNo` 1,2 lúc chạm (thay `Explode` + `Ring`), nhịp `NuocPulse`, bụi bằng `HoaCung`.

**Đã sửa `NNhamVa`:** `HoaNo` 0,42 và vòng cung bụi.

### Viêm Sư (hong_lien): n_kim_phap, n_cau_phap (`HatPhap.cs`)

**Lỗi ở ảnh TRƯỚC:**
- Kim trúng yếu (mana_10–16).
- Lửa bị hút là vụn cam lấm tấm (ult_15–19).
- Vòng nâu to quanh cầu (ult_20–21). Đám khói đen trên cầu là của rig, không phải lớp hạt.

**Đã sửa:**
- Hút bằng `HoaTuCau(veCau: false)` bám cầu của rig, thêm một dòng vệt từ phía dưới.
- `HoaVongCo` thay vòng nâu. Tàn lửa đi theo cụm.
- Cầu bay là `HoaCau` (nhận cỡ của cầu rig); đuôi khói theo quãng; `HoaCauNo` cùng hai `HoaNo` phụ.
- `NeedleHit`: `HoaChop`, lửa toé ngược, khói nhỏ.

**Còn lo:** vệt sinh trên vòng rộng quanh cầu cao nên đôi khi sinh ngoài mép trên sân. Vệt hiện dần nên không giật, nhưng phí hạt.

### Viêm Đao (giap_long): dat_trao, no_lon (`Eruption`, `BigBurst`)

**Lỗi ở ảnh TRƯỚC:**
- Giọt dung nham là cầu tròn cam xếp chuỗi, phủ mặt đối thủ (mana_15–22).
- Cột dung nham thành cục.

**Đã sửa `Eruption`:**
- Báo trước 0,42 s bằng vết nứt và khói mảnh.
- Lúc trào: chớp sát đất, vòng cung, vệt cháy.
- Giọt lệ ít hơn (10 + 6), 70 % rơi phía sau.
- Cột là cụm `"krn"` sau lưng đối thủ, 55 hạt/giây.
- Khói cụm bay lên. Miệng hố bỏ khói lẻ.

### Viêm Dũng (huyen_viem): n_dat_dam, no_lon (`HatDat.cs`)

**Lỗi ở ảnh TRƯỚC:**
- Tướng che đối thủ, vệt chém khó thấy.
- Dung nham là cầu tròn (mana_20–28), khói đen chấm (30).
- Chớp chém dùng `BurstFlash`, là chớp nước lấy bảng màu nước.

**Đã sửa `DatChem`:** `HoaChop`, hai lưỡi lửa toé theo hướng chém, cụm tàn lửa, nhịp `NuocPulse` mỗi nhát. Nhát kết dùng `Eruption` mới.

### Bạch Viêm Hổ (hoa_tinh): n_ho_va, n_ho_gam, n_ho_anh (`HatHo.cs`)

**Lỗi ở ảnh TRƯỚC:**
- Cung sóng âm dày, viền mực nặng, bay xuyên qua đối thủ (mana_08–18).
- Vòng tròn cam, kem to quanh hổ (10–12).
- Chớp vả dùng `BurstFlash` (chớp nước).

**Đã sửa:**
- `HoaSongAm` theo tinh thần `SongAmMoc`: dải cung `kr_songam` dày giữa, thuôn hai đầu; nở và mỏng dần; tới mặt trước thân (0,3 tH) thì bẹt ra rồi tan. Lớp kem và lớp cam đảo nhau mỗi đợt.
- Mỗi đợt tới nơi gọi `NuocPulse(0,3)`.
- Vòng quanh mồm nhỏ lại (0,6 lần chiều cao tướng). Vòng trên đất là `HoaCung`.
- Gồng: vệt xoắn vào ngực.
- Sóng nhiệt: lưỡi chữ S và cụm tàn lửa.
- Lúc trúng: `HoaNo`.
- `NHoVa`: `HoaChop` thay `BurstFlash`.
- `NHoAnh`: `NuocPulse` mỗi lượt chém; sẹo lửa chữ S; `HoaNo` ở các sẹo; `HoaCauNo` lớn; khói cụm.

**Còn lo:** chưa xem kỹ ảnh TRƯỚC của chiêu cuối.

### Hỏa Sơn Long (lan_hoa): n_nui_huc, n_nui_cau, n_nui_ten (`HatNuiLua.cs`)

**Lỗi ở ảnh TRƯỚC:**
- Than tụ là chấm lấm tấm; cầu tròn có vòng nâu (mana_09–10).
- Đuôi khói nâu đậm thành một cột (12–16).
- Nổ có vòng nâu (16).

**Đã sửa:**
- `NNuiCau`: `HoaTuCau` ở mồm, `HoaCau` bay, đuôi khói theo quãng, `HoaCauNo`. `OngPhut` bớt hạt, khói thành cụm.
- `NNuiTen`:
  - đuôi đạn là lưỡi chữ S, 22/s, khói cụm thưa;
  - đầu đạn dùng `kr_luakhoi` đổi khung;
  - viên thường dùng nổ gọn `HoaNoNho`, viên thứ 4 dùng `HoaNo`;
  - nhịp `NuocPulse`;
  - lúc gồng: cụm tàn lửa và khói cụm.
- `NNuiHuc`: `HoaNo` và vòng cung bụi.

**Còn lo:** chiêu cuối vẫn khoảng 159 hạt sống lúc đông nhất.

### Hỏa Quy (nguu_quyen): n_cau_rua, n_cau_sung (`HatRua.cs`)

**Lỗi ở ảnh TRƯỚC:**
- Dải hút là cột vụn (ult_09–12); cầu nhỏ.
- Nổ có vòng nâu to (ult_21).
- Khói đen thành cục rồi xám rải rác (27–33).

**Đã sửa:**
- `NCauSung`:
  - từng ngọn lửa trên lưng (đúng thứ tự, giờ của clip) nhả vệt xoắn ốc vào cầu, gốc có lưỡi lửa co lại;
  - cầu trên mũi sừng đi qua `HoaTuCau`, bán kính theo rig cộng nhịp đập và cú nén (`HoaNhip`);
  - `HoaVongCo` lúc đầy;
  - lúc bay: `HoaCau` và khói đuôi theo quãng;
  - lúc chạm: `HoaCauNo` và `NuocPulse`.
- `NCauMieng`: `HoaTuCau` ở mõm, `HoaCau` bay, `HoaCauNo`.

## Đề xuất sửa file chung (chưa sửa)

1. **StageView: gắn `hat.HoaTrung = (chỗ, k) => …`.**
   - Việc của móc: chớp trắng và đẩy lùi con đứng gần `chỗ` theo `k`, như `NuocPulse`.
   - Cần cho các mã không qua `PlayNuoc`: tia_mat (nhịp mỗi 0,2 s suốt dòng tia), phun, ten (ba mũi), dat_trao, no_lon, cầu lửa mặc định.
   - Cách khác: cho `PlayMana` / `PlayUlt` ghi phe trúng để `NuocPulse` dùng được.
2. **Tiểu Quỷ Lava:**
   - thêm dòng `FireFx` cho `su_tu_lua`, ví dụ `("cau", "phun_nham")` (nhảy dậm, dung nham trào dưới đối thủ) hoặc `"thien_thach"`;
   - rig chiêu cuối đang nhảy vọt ra khỏi khung sticker, bị cắt (ult_06–21): sửa ở rig.
3. **Độ mạnh theo ải:** `HatLua` không biết `StageView.Power`. Đề xuất StageView đặt một trường (ví dụ `hat.HoaPw = Power(side)`) trước `PlayMana` / `PlayUlt` / `PlayNuoc`. Lúc đó hàm `Hoa…` mới nhân cỡ chớp, số liềm và số tàn theo trường này; hiện chưa làm.
4. **Hệ khác:** có thể chuyển `Explode`, `Smoke`, `CauNo` sang `HoaNo`, `HoaKhoi`, `HoaCauNo` cho đồng bộ nét KR5 (các hàm đó hiện vẫn kiểu cũ).
5. **Ghi vào skill:** cập nhật `pokiclash-fx-congthuc` mục 7 với các công thức mới: khói tách cụm, nổ KR5, tụ cầu xoắn ốc, bông va chạm, khói đuôi theo quãng, điểm neo co lớp `kr_*`.
6. **Soi trong Unity:**
   - chạy tour Hỏa (`HoaFxTour`) chụp bản SAU;
   - xem kỹ: đầu tia Hỏa Nhãn và luồng phun có va ở mặt trước thân không; khói có ló quanh đầu đối thủ không; chiều của `kr_nham` và `kr_lua` sau khi co lớp; sóng âm của hổ;
   - xem trong ô xem tướng và thử trên Android.

`LoiCau` trong `HatRua.cs` nay không còn ai gọi, để lại vì vô hại.
