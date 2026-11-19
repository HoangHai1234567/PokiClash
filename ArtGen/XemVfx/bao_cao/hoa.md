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

## Đợt khung vẽ sẵn 2026-11-19 (flipbook, bản chép ở scratchpad `fb_hoa/`, chưa vào Assets)

Thay phần thân chính của các hàm `Hoa…` dùng chung bằng khung vẽ sẵn của `HatFlip.cs`. Hàm mới ở file mới `HatFbHoa.cs` (partial `HatLua`). Chưa nhập ảnh khung (`HasFb` false) thì mọi chỗ rơi về hạt cũ.

| Hàm chung | Nay là | Bỏ |
|---|---|---|
| `HoaNo` (thêm tham số `huong`) | `trung_lua` ở thân, trước tướng, lật theo hướng đòn (0,6–1,1 thân). Từ sc ≥ 0,85 thêm `no` neo chân, **sau lưng** con bị trúng (1,1–2,1 thân, bỏ 2,5 khung đầu cho phồng nhanh), vệt cháy dưới chân. sc nhỏ: một cụm `khoi` muộn 0,12 s | chớp sao gai, khối khói múi, lưỡi liềm, lưỡi chữ S, vòng cung dẹt |
| `HoaCauNo` | `HoaNo` có hướng | quạt lưỡi lửa |
| `HoaChop` | 4–5 khung đầu của `trung_lua` (sao lửa bung), cắt ở ~0,15 s | sao gai viền mực |
| `HoaKhoi` | `khoi`, khung 2,3 R, chạy hết 24 khung trong đúng `life`, trôi chậm hơn | múi `kr_khoi` / `sblob` + 3 cụm con |
| `HoaTuCau` (thêm `huong`) | cầu đang tụ là `cau_lua` đứng yên: mũi chúc xuống, đuôi lửa bốc lên, ngả về phía đối thủ. Giữ vệt hút xoắn ốc, vòng co, chớp lúc nhả (che chỗ đổi sang cầu bay) | khối `HoaCau` |
| Cầu bay (`Fireball`, `NNuiCau`, `NCauMieng`, `NCauSung`, `NCauPhap`) | `HoaFbCau`: `cau_lua` bám đường cong, mũi theo hướng đi, khung cao 4 R | chuỗi lưỡi lửa đuôi, lưỡi lửa liếm quanh cầu |
| `HoaDuoiKhoi` | vẫn theo quãng, cụm 0,8 lần, sống 0,3–0,42 s | dải khói dài từ miệng tới đích |
| `HoaLuaBam` | `lua_lap` 2,8 r, nhỏ dần nửa sau | chùm `kr_luachum` + giọt tách |
| `BigBurst` (thêm `fromSide`, `PlayUlt` truyền vào) | cột lửa = 3 cụm `lua_lap` (hai cụm cao sau lưng, một cụm thấp trước chân) | ~40 lưỡi chữ S |
| `Eruption` (thêm `co`: mana 1,45, chiêu cuối 1,65) | `nham` neo chân, sau lưng, phát sớm 0,15 s cho khung phun trùng 0,42 s; giữ vết nứt báo trước, vài giọt sủi, vòng cung, vệt cháy, 4 giọt lệ, 3 đá | cột `krn`, hố `Crater`, 16 giọt lệ, chớp đất, khói cụm |
| `NeedleHit` | `trung_lua` 50 đơn vị, xoay theo hướng kim | chớp + 3 lưỡi lửa |

Giữ nguyên:
- tia, luồng lửa có va chạm: `Breath`, `TiaMat`, `HoaBong`;
- sóng âm `SongChi`;
- vệt chém, vệt vuốt (`VetLua`);
- kim lửa (`KimLua`), vòng lửa xoáy của `QuyenXoay`, vệt lửa lăn của `NCauLan`, sóng nhiệt mặt đất của `NHoGam`;
- tia văng, cụm tàn lửa, mảnh theo chủ đề, dăm đá, bụi;
- mọi móc `NuocPulse` / `HoaTrung` / `Shake`, mọi giờ trả về (đo lại ngoài Unity: không đổi).

**Lý do đặt `no` sau lưng:**
- Quả nổ cao 1,2–1,8 thân, phần lửa + khói kéo khoảng 0,8 s. Đặt trước tướng thì che kín con bị trúng, trái luật "không che lâu".
- Đặt sau, con bị trúng hiện rõ trước quả nổ. `trung_lua` ở trước lo phần "trúng".
- Muốn trùm trước thì đổi hằng `NoNhom` trong `HatFbHoa.cs`.

**Hạt sống tối đa** (mô phỏng ngoài Unity, bản mới / bản cũ):

| Mã | Mới / cũ |
|---|---|
| cau | 26 / 55 |
| tia_mat | 36 / 45 |
| quyen_xoay | 83 / 111 |
| phun | 44 / 44 |
| n_cau_lan | 65 / 88 |
| n_nham_va | 25 / 42 |
| ten | 28 / 67 |
| no_lon | 26 / 74 |
| phun_nham, dat_trao | 23 / 97 |
| n_kim_phap | 63 / 78 |
| n_cau_phap | 44 / 88 |
| n_dat_dam | 31 / 101 |
| n_ho_va | 22 / 21 |
| n_ho_gam | 45 / 61 |
| n_ho_anh | 41 / 114 |
| n_nui_huc | 30 / 42 |
| n_nui_cau | 60 / 81 |
| n_nui_ten | 76 / 157 |
| n_cau_rua | 30 / 52 |
| n_cau_sung | 47 / 73 |

Mỗi khung vẽ sẵn tính là 1 hạt, vẽ 1–2 Image.

**Hệ khác:** không ảnh hưởng.
- Các hàm đã đổi chỉ tướng Hỏa gọi (đã dò mọi file).
- Kim (Quỷ Xích, Thần Cơ, Pháo Giáp, Nhật Vương) và Thổ (Thiên Thạch Thú) chỉ mượn `Flame` / `Tongue` / `Spark` / `Ember` / `Ash` / `Ring` / `Rock` / `Extra` / `BuiDap` / `BuiTro` / `Explode`: không đổi.
- `Meteor`, `Tornado`, `LavaBall`, `Needles` không tướng nào dùng: để nguyên.

### su_tu_lua (Tiểu Quỷ Lava): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: không có mã hạt (không có trong `HoaAtk`), không đổi.
- Mana `cau`: cầu tụ ở miệng là `cau_lua` đuôi bốc lên; cầu bay `cau_lua`; khói đuôi ngắn; trúng là `trung_lua` + `no` 1,17 thân sau lưng. Bỏ lưỡi liếm, chuỗi lưỡi đuôi, quạt lửa.
- Chiêu cuối `phun_nham`: `nham` 1,65 thân sau lưng đối thủ, giữ vết nứt báo trước, vòng cung, vệt cháy.

### hoa_nhan (Hỏa Nhãn): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: không có mã hạt, không đổi.
- Mana `tia_mat`: giữ tia và bông va chạm (đã có va chạm). Chớp ở con ngươi và chỗ chạm đổi sang `trung_lua` cắt ngắn. Khói thành `khoi`. Nổ kết là `trung_lua` lật theo hướng tia.
- Chiêu cuối `quyen_xoay`: giữ vòng lửa xoáy. Năm nhát đầu là `trung_lua`, lật xen kẽ theo hai nắm tay. Nhát cuối có thêm `no` 1,3 thân sau lưng. Khói là `khoi`.

### kim_su (Hỏa Cung): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: không có mã hạt, không đổi.
- Mana `ten`: mỗi mũi tên một `trung_lua` lật theo hướng tên, bỏ quạt ba lưỡi. Lửa bám chỗ găm là `lua_lap`. Khói là `khoi`.
- Chiêu cuối `no_lon`: cột lửa là 3 cụm `lua_lap`, nổ là `no` 1,43 thân + `trung_lua` lật theo phía ra chiêu, nổ phụ là `trung_lua`. Giữ vòng cung, vết nứt.
- Lưu ý: khung vẽ sẵn tô sẵn màu lửa đỏ cam, bảng `"vang"` của tướng này không còn áp lên nổ và lửa (gần như cùng màu).

### nham_than (Nham Thần): đợt khung vẽ sẵn 2026-11-19
- Đòn thường `n_nham_va`: `trung_lua` 0,7 thân ở đỉnh đầu, xoay cho lửa tạt ngược lên về phía bàn tay nện; bỏ nổ nhỏ hạt và ba lưỡi lửa cổ tay. Giữ tia, dăm đá tro, bụi.
- Mana `phun`: giữ luồng phun có va chạm. Chớp và khói tự đổi theo `HoaChop` / `HoaKhoi`.
- Chiêu cuối `n_cau_lan`: giữ vệt lửa lăn (gắn với cầu của rig). Chạm là `no` 1,47 thân + `trung_lua` theo hướng tông; bỏ quạt 6 lưỡi lửa, giữ dăm đá, tia. Nổ phụ là `trung_lua`.

### hong_lien (Viêm Sư): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: không có mã hạt, không đổi.
- Mana `n_kim_phap`: giữ kim lửa. Mỗi kim găm một `trung_lua` nhỏ xoay theo hướng kim.
- Chiêu cuối `n_cau_phap`: giữ phần hút quanh cầu của rig và lưỡi liếm từ cầu của rig. Cầu bay là `cau_lua`, bỏ chuỗi lưỡi đuôi. Chạm là `no` 1,81 thân (dạng 1: 1,47) + `trung_lua`; hai nổ phụ là `trung_lua`.

### giap_long (Viêm Đao): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: không có mã hạt, không đổi.
- Mana `dat_trao`: `nham` 1,45 thân (như `phun_nham`).
- Chiêu cuối `no_lon`: như Hỏa Cung.

### huyen_viem (Viêm Dũng): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: không có mã hạt, không đổi.
- Mana `n_dat_dam`: giữ vệt chém. Mỗi nhát một `trung_lua` xoay theo hướng chém (0,55–0,85 thân), bỏ chớp và hai lưỡi lửa. Nhát bổ kết trùng khung phun của `nham`.
- Chiêu cuối `no_lon`: như Hỏa Cung.

### hoa_tinh (Bạch Viêm Hổ): đợt khung vẽ sẵn 2026-11-19
- Đòn thường `n_ho_va`: giữ ba vệt vuốt. Trúng là `trung_lua` 0,8 thân xoay theo hướng vả. Ba lưỡi lửa trên vết vuốt đổi thành ba cụm `lua_lap` nhỏ.
- Mana `n_ho_gam`: giữ nguyên sóng âm `SongChi`, sóng nhiệt mặt đất, phần gồng.
  - Trúng là `no` 1,34 thân + `trung_lua` theo hướng sóng.
  - Cháy tới hết tiếng gầm là hai cụm `lua_lap` ở chân (cao sau lưng, thấp trước chân); bỏ lưỡi lửa rải trên thân, giữ tia.
- Chiêu cuối `n_ho_anh`: giữ vệt lướt, vệt chém, màn âm bản.
  - Lửa dọc sẹo là một cụm `lua_lap` mỗi sẹo (dạng 1: hai cụm).
  - Nổ ở sẹo là `trung_lua` lật theo sẹo. Nổ lớn là `no` 1,73 thân (dạng 1: 1,47).

### lan_hoa (Hỏa Sơn Long): đợt khung vẽ sẵn 2026-11-19
- Đòn thường `n_nui_huc`: `trung_lua` theo hướng húc, giữ dăm bazan, giọt dung nham, bụi.
- Mana `n_nui_cau`: cầu tụ ở mồm và cầu bay là `cau_lua`, bỏ lưỡi liếm và chuỗi lưỡi đuôi. Chạm là `no` 1,47 thân; nổ phụ là `trung_lua`. Giữ `OngPhut` (khói đổi sang `khoi`).
- Chiêu cuối `n_nui_ten`:
  - đầu và đuôi đạn tầm nhiệt là `cau_lua` (mũi theo đường cong);
  - bỏ chuỗi lưỡi đuôi và cụm khói đuôi (không còn lưỡi lửa nối thì các cụm đứng lẻ thành "khói rải rác");
  - nổ nhỏ (`HoaNoNho`) là `trung_lua` 0,55 thân; nổ cuối là `no`.
  - Hạt sống tối đa 157 → 76.

### nguu_quyen (Hỏa Quy): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: không có mã hạt, không đổi.
- Mana `n_cau_rua`: cầu tụ ở mõm và cầu bay là `cau_lua`. Chạm là `no` 1,2 thân.
- Chiêu cuối `n_cau_sung`:
  - giữ vệt hút từ từng ngọn lửa trên lưng;
  - cầu trên mũi sừng là `cau_lua` đuôi bốc lên, ngả về phía đối thủ, cỡ theo rig;
  - cầu bay là `cau_lua`; bỏ lưỡi liếm và chuỗi lưỡi đuôi;
  - chạm là `no` 1,64 thân (dạng 1: 1,39).

### Còn ngờ (đợt khung vẽ sẵn)
- Đã chụp tờ soi ngoài Unity: ảnh khung thật đặt theo nét vẽ mô phỏng, tướng là khối chữ nhật giả. Chưa soi trong Unity hay trên Android, chưa đo bằng runtime thật.
- Đuôi lửa của cầu đang tụ bốc lên khoảng 1,75 lần đường kính cầu. Với cầu ở mồm (Tiểu Quỷ Lava, Hỏa Sơn Long, Hỏa Quy mana), đuôi có thể chạm mặt tướng. Đã ngả đuôi về phía đối thủ, cần xem trên rig thật.
- `no` sau lưng: với tướng to bề ngang, phần lớn quả nổ bị thân che, chỉ ló quanh viền. `nham` cũng thế (cột dung nham giữa bị thân che).
- Màn âm bản của Bạch Viêm Hổ: `lua_lap` trên sẹo hiện trong lúc màn đảo màu, nên sẽ ra màu đảo. Lưỡi lửa cũ cũng vậy.
- Bảng màu theo tướng (`Th.pal`) không còn áp lên nổ / cầu / lửa vì khung đã tô sẵn: Hỏa Cung `"vang"`. Khói theo chủ đề (`Th.smoke`) cũng không áp lên `khoi`.
- Đòn thường của 7 tướng không có mã hạt (hiệu ứng nằm trong clip hoặc không có), nên chưa có `trung_lua`.

### Cần đổi ở file không thuộc mình (đợt khung vẽ sẵn)
- `StageView.cs` + `HatNuoc.cs` (`PlayNuoc`) + `HatVoi.cs` (`AtkLao`): muốn đòn thường của 7 tướng Hỏa còn lại có lửa trúng đích thì thêm mã chung, ví dụ `n_lua_trung`:
  - thêm vào `HoaAtk`;
  - `PlayNuoc` gọi một hàm mới đặt `HoaFbTrung` ở thân đối thủ đúng `lead`;
  - `AtkLao` nhận mã này cho tướng lao tới.
  - Hàm `HoaFbTrung` đã có trong `HatFbHoa.cs`.
- `Editor/HatLuaMenu.cs` (nhập ảnh, gán `hatSprites`): ảnh `hat_fb_*` phải nằm trong `StageView.hatSprites` và mảng ảnh của ô xem tướng, thì `HasFb` mới true.
- File mới `HatFbHoa.cs` chép vào `Assets/01 Script/Game/Battle/`: Unity tự sinh `.meta`.

### Bổ sung 2026-11-19 chiều: nổ lên lớp trước, vệt khói đuôi
Người dùng xem trong game: "có vài vụ nổ layer nằm dưới địch nên không thấy rõ, các fireball, tên lửa,... nên thêm trail smoke vào".

**Lớp nổ:**
- `NoNhom` (`HatFbHoa.cs`) đổi `Back` → `Front`. Quả nổ `no` và cột dung nham `nham` nay vẽ trước tướng.
- Neo dời `NoLech` = 0,15 thân về phía người ra chiêu.
  - `Eruption` thêm tham số `huong`; `PlayMana` (`dat_trao`), `PlayUlt` (`phun_nham`) và `NDatDam` truyền hướng vào.
  - `trung_lua` vốn đã ở trước tướng.
- Phần bị ảnh hưởng: mọi `HoaNo` từ sc 0,85 (`HoaCauNo`, `BigBurst`, nhát cuối `QuyenXoay`, `NHoGam`, `NCauLan`) và `Eruption`.
- Lưu ý: `nham` 1,45–1,65 thân đặt trước thì che gần hết đối thủ khoảng 0,7 s (lửa rồi khói). Muốn trả riêng `nham` về sau lưng thì đổi `NoNhom` ở dòng `Fb("nham", …)` trong `EruptionFb` thành `Back`.

**Vệt khói đuôi** (`FbKhoiDuoi` của `HatFlip.cs` mới):
- Cầu bay `HoaFbCau`: thêm tham số `khoi`. Điểm nhả sau tâm cầu 2 bán kính (gốc đuôi lửa), lớp Front 27, dưới cầu (34). Cỡ `KhoiCo(R, tH)` = 1,5 R kẹp 0,22–0,35 thân.
  - Áp cho: `Fireball` (Tiểu Quỷ Lava), `NNuiCau` (Hỏa Sơn Long), `NCauMieng` và `NCauSung` (Hỏa Quy), `NCauPhap` (Viêm Sư).
  - Cầu đứng tụ không nhả.
  - `HoaDuoiKhoi` (vệt cũ theo quãng) thôi chạy khi có khung, tránh hai vệt chồng nhau.
- Đạn tầm nhiệt `TenNhiet` (Hỏa Sơn Long chiêu cuối):
  - 0,22 thân (dạng 1: 0,17), 9 cụm/giây, tan nhanh (tốc độ 2,4), lớp 26 dưới đầu đạn;
  - bỏ cụm khói miệng ống của loạt bắn (`OngPhut` thêm `khoi`), vì vệt đã bắt đầu ngay miệng ống.
- Kim lửa `KimLua` (Viêm Sư mana): thêm tham số `khoi`; lúc phóng nhả vệt 0,2 thân, 18/giây, từ chuôi kim.
- Cầu lăn `NCauLan` (Nham Thần chiêu cuối): 5 cụm khói lẻ mỗi giây đổi thành vệt liền 20/giây, 0,35 thân, sau tướng (Back 12).

**Hạt sống tối đa** (mô phỏng ngoài Unity):

| Mã | Hạt sống |
|---|---|
| n_nui_ten | 108 (đã giảm từ 146 bằng vệt thưa và bỏ khói miệng ống) |
| n_kim_phap | 82 |
| n_cau_lan | 71 |
| n_nui_cau | 61 |
| n_cau_sung | 47 |
| cau | 28 |

Giờ trúng không đổi.

### Bổ sung 2026-11-19 tối: lốc lửa vẽ sẵn "loc_lua"
Người dùng chê lốc cũ "màu hơi trầm và chưa hợp lắm".

**Hàm mới `HoaFbLoc`** (`HatFbHoa.cs`):
- Thân lốc là `loc_lua` neo chân, cao vọt lên trong 0,2 s, hiện dần, tắt dần 0,25 s.
- Lốc bao quanh đối thủ có hai lớp:
  - lớp sau (Back) đặc;
  - lớp trước (Front) lệch pha nửa vòng, lật ngang, nhỏ hơn 5 %, mờ 0,55, để vẫn thấy con bị trúng.
- Chưa nhập ảnh thì về đường cũ.
- `FbH` thêm tham số `alpha`.

**Từng chỗ:**
- **hoa_nhan (Hỏa Nhãn), chiêu cuối `QuyenXoay`:**
  - lốc 1,35 thân quanh đối thủ, từ lúc gọi tới hết chuỗi đấm (T1 + 0,1 s);
  - bỏ lưỡi lửa chữ S bay vòng elip, thêm tàn lửa thưa bị cuốn quanh;
  - giữ vòng cung ở chân, sáu nhát nổ, nhịp `HoaTrung`, giờ trả về 0.
  - Hạt sống tối đa 83 → 62.
- **`Tornado` (`loc_xoay`, hiện không tướng nào dùng):**
  - lốc 1,4 thân, từ 0,2 s tới T1 + 0,15 s;
  - bỏ vòng viền mực ở chân, lưỡi lửa bay vòng, dải cung hai nửa, khói hạt cũ;
  - giữ than bị hút vào, vết nứt, tia lửa bay quanh (18/s), đá cuốn, mảnh theo chủ đề, rung, giờ trả về 0,35;
  - khói là cụm `khoi` ở miệng phễu.
  - Hạt sống tối đa 139 → 41.
- Hệ Hỏa không còn lốc nào khác. "phun_xoan" chỉ là mây xoắn bay dọc luồng phun; không tướng nào dùng.

### Bổ sung 2026-11-19 đêm: lốc to hơn, khói Hỏa Sơn Long sẫm và dài, cầu lửa mới "cau_tu" / "cau_bay"

**1. Lốc trùm kín đối thủ** (người dùng: "lốc xoáy làm to lên cho che hết tướng địch"):
- Áp cho `QuyenXoay` (Hỏa Nhãn chiêu cuối) và `Tornado`.
- `loc_lua` cao 1,7 thân, giãn ngang 1,55. Hàm mới `DrawFbW` trong `HatFbHoa.cs` giãn ngang quanh điểm neo; `FbH` và `HoaFbLoc` có thêm tham số `sx`.
- Ngang phễu: giữa ≈ 1,4 thân, miệng ≈ 2,1 thân, chân ≈ 1,2 thân. Cổ phễu (khoảng 0,5 thân trên chân) vẫn hẹp hơn, ≈ 0,8 thân, vì đó là dáng của khung.
- Lớp trước vẫn mờ 0,55.

**2. Hỏa Sơn Long** (người dùng: "trail smoke sẫm màu hơn chút và trail để lại vệt dài hơn chút nữa"):
- Đạn tầm nhiệt chiêu cuối:
  - vệt khói nhân màu `KhoiSam` (0,6; 0,57; 0,55): xám nâu than;
  - khung chậm 1,1 (cụm sống ≈ 0,8 s, trước 2,4) nên vệt dài;
  - cụm to hơn (0,3 thân) mà thưa hơn (5 cụm/giây/viên).
  - Giọt dung nham ở nổ nhỏ còn một viên trong bốn (trước: mỗi viên chẵn), nhường ngân sách hạt.
  - Hạt sống tối đa 110 (dưới 120).
- Cầu chiêu mana (`NNuiCau`): vệt khói cùng màu sẫm, cùng độ dài. `HoaFbCau` có thêm `khoiTint` và `khoiSpeed`.

**3. Cầu lửa mới** (người dùng chê cầu Hỏa Quy "xấu ... nhìn hơi tĩnh, chiêu mana cũng tĩnh"):
- **Cầu đang tụ = `cau_tu`** (`HoaFbCauTu`, qua `HoaTuCau`):
  - khung tự phồng / co theo nhịp 1 Hz; mã chia cỡ từng khung cho bán kính đo được (bảng `CauTuR`), nên cỡ cầu do mã điều khiển: lớn dần theo pha tụ;
  - phập phồng 7 Hz ±6 % (sửa `HoaTuCau` và `HoaNhip`, trước 4 Hz ±7 %), nén 0,07 s trước lúc nhả như cũ;
  - xoay chậm 35–55 độ/giây;
  - tàn lửa xoắn ốc vào (`HoaTanXoan`, 8–20 hạt/giây);
  - giữ vệt hút xoắn ốc, vòng co, chớp lúc nhả.
- **Cầu bay = `cau_bay`** (`HoaFbCau` khi đã nhập ảnh; khung cao 3,8 bán kính): mũi theo đường cong, vệt khói đuôi như trước.
- Trúng vẫn là `trung_lua` + `no`.
- Chưa nhập ảnh mới thì về `cau_lua`, rồi về hạt cũ.
- **Tướng được đổi:**
  - Hỏa Quy (nguu_quyen): mana `NCauMieng`, chiêu cuối `NCauSung` (cầu trên sừng, cả dạng 1);
  - Tiểu Quỷ Lava (su_tu_lua): mana `Fireball`;
  - Hỏa Sơn Long (lan_hoa): mana `NNuiCau`;
  - Viêm Sư (hong_lien): chiêu cuối `NCauPhap`, chỉ cầu bay (cầu tụ là mảnh của rig).
- Đạn tầm nhiệt Hỏa Sơn Long vẫn dùng `cau_lua` (đạn nhỏ).

### Bổ sung 2026-11-19 khuya: lốc trùm "loc_lua_bao"
- Lốc bao quanh đối thủ (`QuyenXoay` của Hỏa Nhãn, `Tornado`) nay dùng khung `loc_lua_bao`: cột xoáy dày, gốc gần rộng bằng miệng.
- Cỡ: cao 1,65 thân, giãn ngang 1,2. Ngang thân ≈ 1,2 thân, miệng ≈ 1,7 thân; trùm từ chân tới đầu, hết hở cổ phễu.
- Lớp trước vẫn mờ 0,55.
- `HoaFbLoc` thêm tham số `hBao`, `sxBao`. Chưa nhập ảnh `loc_lua_bao` thì về `loc_lua` cao 1,7 thân, giãn 1,55.
- Hạt sống không đổi: `quyen_xoay` 62, `loc_xoay` 43.

### Bổ sung 2026-11-19 khuya: vệt khói LIỀN cho đạn tầm nhiệt Hỏa Sơn Long
Soi ảnh chụp: cụm tròn rời 5 cụm/giây nhìn như chấm khói rải rác. Đổi thành dải liền.
- Hàm mới `HoaVetKhoi` (`HatFbHoa.cs`): dải mảng liền `MRibbon` (có vân chì) theo lịch sử vị trí đuôi đạn, mẫu mỗi 0,03 s, giữ 0,9 s.
  - Màu khói than (95, 85, 80).
  - Rộng 0,16 thân ở sát đạn, mảnh dần về 0,05 thân; đầu dải thon ra từ gốc đuôi lửa; mép gợn nhẹ.
  - Alpha 0,85 → 0 về cuối, chia 7 đoạn nối liền (mỗi đoạn một bậc alpha); điểm cũ trôi lên chậm như khói bốc.
  - Đạn trúng thì vệt còn đọng 0,5 s rồi tan.
  - Pháp tuyến lấy trên ±2 mẫu và giữ cùng chiều, để mép không gấp khúc ở chỗ đường bay gắt.
- Thêm cụm `khoi` nhỏ sẫm, 2,5 cụm/giây, tan nhanh, làm mép bông. Bỏ cụm tròn rời làm chính.
- Mỗi vệt là một hạt. Hạt sống tối đa của `n_nui_ten` là 95 (trước 110).
- Cầu lửa bay (`HoaFbCau`) vẫn dùng vệt cụm `khoi` dày 26 cụm/giây, vốn đã liền. Muốn đồng bộ thì gọi `HoaVetKhoi` trong `HoaFbCau`.

### Bổ sung 2026-11-19 khuya (lần 2): vệt khói THẬT cho đạn tầm nhiệt Hỏa Sơn Long
Người dùng chê dải liền: "trail khói của final boss đảo hỏa phải là khói chứ không phải tô đen như vậy".
- Bỏ hẳn `HoaVetKhoi` (dải `MRibbon` màu than).
- Hàm mới `HoaKhoiDuoi` (`HatFbHoa.cs`): cụm `khoi` nhả dày, rải trên đoạn vừa bay, chồng sát nhau thành vệt bông mềm liền (như vệt cầu lửa bay); mỗi cụm trôi lên chậm.
- Thông số: cụm 0,23 thân, 16 cụm/giây, tốc khung 1,4 (cụm sống khoảng 0,63 s), nhả từ 0,1 s tới 85 % quãng bay.
- Màu `KhoiSam` đổi (0,6; 0,57; 0,55) → (0,72; 0,68; 0,66), alpha khoảng 0,85: sẫm hơn khói thường một nấc, không đen. Vệt khói cầu chiêu mana (`NNuiCau`) cùng tướng cũng dùng màu này.
- Ngân sách: mọi đạn cùng kéo khói thì lên 141 hạt, nên chỉ viên chẵn (8/16, xen kẽ) kéo khói. Hạt sống tối đa của `n_nui_ten` là 104.

### Bổ sung 2026-11-19 khuya (lần 3): vệt khói liền nhả theo quãng đường
Soi ảnh chụp: nhả theo giây (16 cụm/giây) thì đạn bay nhanh nên các cụm cách quãng gần bằng cỡ cụm, thành cụm rời.
- `HoaKhoiDuoi` viết lại: nhả cụm theo QUÃNG ĐƯỜNG. Cứ đạn đi được 0,33 lần cỡ cụm thì đặt một cụm đúng chỗ trên đoạn vừa đi; các cụm chồng 2/3 lên nhau thành vệt bông liền, dù đạn nhanh hay chậm.
  - Cụm 0,23 thân, cỡ chênh ít (0,92–1,08), nên không có cụm nhỏ rời ở mép.
  - Mỗi cụm sống 0,55 s, nở thêm 15 % về cuối, trôi lên chậm, độ đặc 0,8.
  - Nhả từ 0,1 s tới 85 % quãng bay.
  - `FbH` có thêm tham số `tint`.
- Màu `KhoiSam` sáng thêm: (0,8; 0,76; 0,74). Vệt khói cầu chiêu mana của cùng tướng cũng dùng màu này.
- Số viên kéo khói: chọn các viên từ ống chĩa ngược về sau (góc ≥ 100 độ, bay vòng dài), rải đều trong loạt.
  - 4/16 viên (dạng 3), 4/12 viên (dạng 2), 3/8 viên (dạng 1).
  - Hạt sống tối đa: 112 / 116 / 101.
- Nổ nhỏ của đạn (`HoaNoNho`): cụm tàn lửa tan sau 0,45 s (trước sống 0,7–1,2 s), nhường ngân sách cho vệt khói.

### Bổ sung 2026-11-19 khuya: tia vẽ sẵn (TiaFb + DaTiaLua) cho tia mắt Hỏa Nhãn
Người dùng: tia "nhìn vẫn chưa đã" (ống thẳng đặc, chỗ trúng nhỏ).
- Hỏa Nhãn (hoa_nhan), mana `tia_mat`: có `HasTia(DaTiaLua)` thì chạy `TiaMatFb` (HatNhan.cs).
  - Thân là đoạn lửa sợi xoắn trôi liên tục; cầu lửa xoáy ở con ngươi lớn dần trong pha tụ; lửa toé ngược lặp ở mặt trước thân đối thủ.
  - Dày 0,22 chiều cao người bắn: `PlayMana` truyền `casterH` vào `TiaMat` (tham số tuỳ chọn mới).
  - Nối giờ như `NTiaKhung`: tTu = giờ chạm cũ − thời gian vươn, tBan = giờ tắt cũ − giờ chạm; nổ kết lúc đoạn tia cuối bay tới đích.
  - Bỏ: lõi tia mảng liền, chớp và lửa phụt ở con ngươi, lưỡi lửa bám mép tia, chớp + `HoaBong` ở chỗ trúng, lửa dạt dọc thân, tia vỡ lúc rút.
  - Giữ: rung, tia văng, nhịp `HoaTrung` (0,6 lúc chạm, rồi 0,3 mỗi 0,2 s), mảnh theo chủ đề, khói cụm, nổ nhỏ kết, giờ trả về.
  - Hạt sống tối đa 45 → 16.
- Không đổi: luồng phun `Breath` (Nham Thần mana, `HoaBong` ở đó là va chạm của luồng phun). Hệ Hỏa không có tia thẳng nào khác.

### Bổ sung 2026-11-19 khuya: sóng âm Bạch Viêm Hổ rõ hơn, bỏ đốm lửa ở dưới
Người dùng: "phần sóng âm chiêu mana tướng này chưa rõ, tự nhiên thấy mấy đốm lửa spawn ra ở dưới nhìn không đẹp".
- `NHoGam` (Bạch Viêm Hổ, hoa_tinh, mana):
  - Sóng âm: 6 cung cách 0,1 s (dạng nhẹ 5; trước 3–4 cung cách 0,14 s), to hơn (0,3 người bắn → 1,35 thân đối thủ, cung đầu 1,2 lần).
  - Nét dày gấp đôi bằng hàm mới `SongChiDay` (HatHo.cs): hai lớp ảnh cung nét chì lệch 3 %, đặc hơn.
  - Cung bay tới tận mặt trước thân đối thủ (0,12 thân trước tâm; trước dừng ở 0,3).
  - Mỗi cung sau cung đầu tới nơi: bông toé trắng `trung_trang` nhỏ (0,42 thân) ở chỗ chạm, rung nhẹ, nhịp `HoaTrung` 0,3. Cung đầu trùng cú nổ chính.
  - Lúc gầm: ba gợn "méo không khí" là cung chì nhỏ nhạt nở đồng tâm ở miệng.
  - Bỏ sóng nhiệt sát đất (lưỡi lửa và cụm tàn lửa sinh dọc mặt đất), hai cụm `lua_lap` ở chân đối thủ, lửa / tia rải trên thân suốt tiếng gầm.
  - Giữ cú nổ chính (`no` + `trung_lua` + tàn lửa của nó), phần gồng, chớp miệng, vòng cung đất, bụi, khói sau nổ, giờ trả về.
  - Hạt sống tối đa 43 → 29.
