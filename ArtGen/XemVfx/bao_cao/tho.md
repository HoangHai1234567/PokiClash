# Báo cáo VFX hệ THỔ (2026-11-18)

Đã sửa: `HatTho.cs`, `HatThach.cs`, `HatThoTinh.cs`, `HatBun.cs`, `StageViewThoTinh.cs`. `StageViewNuot.cs` giữ nguyên. Biên dịch thử
(`bien_dich_thu.py Temp/vfx_tho`): Core, Game, Editor đều 0 lỗi. Không mở Unity, chưa chụp bản SAU: phiên chính chụp rồi so.

Hợp đồng thời gian giữ nguyên: mọi hàm `N...` trả đúng giờ trúng như cũ, mốc rig giữ nguyên, mảnh rig bay (`fly_*` / `far`) vẫn do game lái.
Ý tưởng từng chiêu giữ nguyên, chỉ đổi cách vẽ.

## A. Đổi chung (mọi tướng Thổ dùng, nằm trong `HatTho.cs`)

| Lời chê | Đã làm |
|---|---|
| Màu tối, xám, bẩn | Bảng màu mới: bụi be `#E8C99A`, cát `#D9A866`, nâu đất `#A86B3C`, viền đậm `#7A4A26`, hổ phách `#FFB23A`, ngọc lam `#4FD6C8` (`HatThach`). Màu hạt dùng ảnh đặt sáng hơn một nấc vì ảnh xám ~236 nhân màu còn ~0,93. Đá đổi từ xám sang be ấm. Bùn sáng hơn một nấc. |
| Khói, bụi rải rác, không thành cụm | `ToBui` viết lại: mỗi hạt là một cụm nhiều múi (`kr_khoi`, dự phòng `foam`), hai tông phẳng (đỉnh be sáng, đáy đậm: `kr_khoiday`, dự phòng lớp đậm lót dưới). To gần đủ trong 18 % đời, bay lên, cụm to tách thành 3 cụm nhỏ ở 42 % đời, mờ ở 35 % cuối. `ToCum`: một cụm chồng nhiều múi to/vừa/nhỏ có chung viền mực. `ToKhoi` / `ToKhoiCum`: khói than đen → xám, cùng dáng cụm, tách cụm, có tro. Các luồng bụi 22–50 hạt/giây hạ còn 8–20 hạt/giây nhưng cụm to hơn, nên khói liền thành khối. |
| Hạt lẻ to, đơn lẻ | Sỏi nhỏ hơn và đi theo chùm lệch cỡ (`ToSoiCum`: 3 viên to/vừa/nhỏ bay cùng nhau). Sỏi có mặt sáng nhỏ để đọc ra khối đá, nảy một lần rồi nằm. |
| Tia, đạn cụt lủn, không va chạm | `ToNo` viết lại theo KR5: chớp kem giữ đủ 2 khung (`kr_chop`), vòng va chạm mảnh không viền, **bông va chạm** toé ngược hướng đòn (`kr_tiadau`, dự phòng chùm gai `tuft`), chùm dăm chếch về phía kẻ đánh, một cụm bụi sau thân (không che con bị trúng). Mọi cú trúng giờ truyền hướng đòn. |
| Đối thủ chỉ giật ở cú đầu | `HatLua.ThoNhip` + `StageViewThoTinh.ThoCuPhu`: ở **mỗi cú phụ** của chiêu nhiều cú (sỏi/pha lê găm, phiến găm, lưỡi cát, thiên thạch, mưa pha lê, ba đấm, nghiến, xé, cột trồi), đối thủ chớp và giật nhẹ ra xa kẻ đánh trong 0,12 s, mạnh dần theo `Power`. Cú chính vẫn do `StageView.Hurt`. Phần này chỉ dời ảnh và chớp, không đổi cỡ ảnh. |
| Đạn không có đuôi | `ToTangBay` (tảng đá): đuôi bụi liền rải theo quãng vừa bay (KR5), dăm vụn rơi. Tới nơi tảng **vỡ** thành 4–6 khối nhỏ văng ngược, nảy một lần rồi nằm (`ToTangVo`). `ToLuoiCat`: đuôi cát liền; tới nơi lưỡi ép dẹt, loe ngang rồi tan trong 0,12 s, không tắt phụt; lưỡi dừng ở mặt trước thân. `ToPhaLe`: khối nhọn mập hơn, có hai bóng mờ (vệt tốc độ), chạm thì vỡ thành 2–3 mảnh rơi xuống đất. `ToDuoiThang`: đuôi bụi cho mảnh của rig bay thẳng; đuôi theo u² của giờ nên luôn ở sau mảnh. |
| Sóng, nổ chưa đẹp | `ToVong` không còn vòng sprite viền mực: thay bằng 3–4 cung elip dẹt **không viền** trên đất, nở nhanh, mỏng dần, khe rộng dần (đứt đoạn), thêm dải cát đậm bên trong để nổi trên nền cát. `ToHo`: hố/vệt nện trên đất (elip nâu trong vành be), giữ ~1 s rồi mờ. `ToNut`: vết nứt thon dần, hai nhánh rẽ, mép be bị hất, giữ ~1 s rồi mờ 0,5 s (trước đây 0,5 s). |
| Pha tụ xấu (yêu cầu bổ sung) | `ToHut` viết lại: hạt bị hút là **vệt** kéo dài theo vận tốc (`kr_vet`, dự phòng `streakg`) hoặc sỏi xoay (35 %), bay **xoắn ốc** vào tâm, nhanh dần (f^2), hiện dần lúc sinh, co lại nhập vào tâm lúc tới. `ToVongCo`: vòng mảnh không viền co về tâm. Mật độ tụ tăng dần tới lúc nhả. Cầu tụ lớn theo nhịp đập, nén 0,06 s, rồi chớp lúc nhả. |

Ảnh hạt mới đều có dự phòng (`SK(mới, cũ)`), chưa nhập vẫn chạy. Đã dùng: `kr_khoi(s)`, `kr_khoiday`, `kr_chop(s)`, `kr_tiadau(s)`,
`kr_vet(s)`, `kr_songam(s)`, `kr_nham(s)`, `kr_nhamgiot(s)`. Chưa dùng: `kr_cung` (vì chưa biết ảnh đã dẹt sẵn hay chưa nên dùng cung vẽ
mảng), `kr_cau` (cầu tụ của Thổ là tảng đá `DrawTang`), `kr_khoinho`, `kr_liem`, `kr_luakhoi`. Hướng ảnh tôi giả định: `kr_tiadau`,
`kr_vet`, `kr_nhamgiot`, `kr_songam` chĩa về +x; `kr_nham` dựng đứng, giọt kéo xuống dưới. Ảnh vẽ khác hướng thì sửa góc ở `ToBong`,
`ToHut`, `DrawBunGiot`, `DrawBunCuc`, `TtSongGam`.

## B. Từng tướng

Ảnh TRƯỚC: `Temp/PokiShots/vfx_all/truoc/<tướng>/`. Tôi soi kỹ (phóng to) Thạch Giáp mana/ult, Tê Thiềm mana, Sa Long mana, Thiên
Thạch Thú ult, Thổ Tinh ult, Bùn Ngoạm ult, Hạt Dẻ mana. Các chiêu còn lại chỉ xem tờ khung nhỏ hoặc đọc code: chỗ đó tôi ghi "suy từ code".

### thach_nhan — Thạch Giáp (`HatTho.cs`)
- **Lỗi ở TRƯỚC:**
  - mana_04–10: bụi lắc mai là các chấm nâu xám rải rác trên mai;
  - mana_06–12: cú găm chỉ là chớp nhỏ, vài đốm dăm sẫm, cục bụi nâu tối dính lên mặt đối thủ;
  - ult_09–14: pha lê vọt lên mảnh như que cỏ;
  - ult_13–24: mỗi cú mưa trúng để lại chấm nâu bẩn khắp mặt đối thủ, mảnh cuối cắm đất gần như không thấy.
- **Đã sửa:**
  - `NGiapSoi`: bụi lắc mai còn 13 cụm/giây (cụm to, liền). Mỗi mảnh rig có đuôi bụi `ToDuoiThang` từ hốc tới mặt trước thân. Cú găm có hướng. Đáp đất bằng `ToCum`.
  - `NGiapHuc`: cú húc có hướng, bụi cụm.
  - `NGiapMua`: pha lê vọt to 30×12, có chớp ở hốc. Mảnh mưa to 30×13, mảnh cuối 56×24, vỡ thành mảnh rơi xuống đất. Cú cuối có hố. Mỗi mảnh mưa trúng làm đối thủ giật (`ThoNhip`).
- **Mong thấy ở SAU:** mana có vệt bụi theo mảnh; mỗi cú găm có bông va chạm, vòng mảnh, chùm dăm và đối thủ giật. Ult có pha lê hổ phách tươi, mưa trúng rõ, mảnh cuối vỡ, hố và vết nứt nằm lại.
- **Còn lo:** đường bay thật của mảnh rig có thể vồng; đuôi bụi đi thẳng từ hốc tới thân nên có thể lệch nhẹ khỏi mảnh.

### lung_vuong — Sa Tích (`HatTho.cs`; suy từ code, chưa phóng to ảnh)
- **Lỗi ở TRƯỚC (suy từ code):** cát bốc 26–34 chấm/giây nhỏ quanh áo; cú găm phiến đất nung dùng `ToNo` cũ (chấm dăm, bụi nâu tối).
- **Đã sửa:**
  - `NTichPhien`: cát bốc thành cụm, mật độ tăng dần tới lúc phóng. Mỗi phiến có đuôi cát. Cú găm có hướng, màu đất nung tươi. Đối thủ giật ở mỗi phiến.
  - `NTichLoc`: cát xoáy quanh chân đối thủ thành cụm (nửa trước, nửa sau). Cú dậm có hố và `ToCum`. Lốc cát giữ nguyên, bớt mảnh bay quanh (50 → 36/giây).
- **Còn lo:** chỗ phiến rời áo lấy theo điểm giữa áo ở 0,45 s, không phải từng phiến, nên đuôi có thể lệch vài đơn vị.

### cao_da — Tê Thiềm (`HatTho.cs`)
- **Lỗi ở TRƯỚC:**
  - mana_04–09: hạt hút là chấm tròn sẫm rời rạc;
  - mana_10–13: tảng đá xám xỉn, vệt sau tảng là đốm lẻ;
  - mana_14–19: trúng chỉ có chớp nhỏ và vài cục sẫm, tảng biến mất ngay.
- **Đã sửa:**
  - `NThiemPhun`, pha tụ: vệt bụi/sỏi xoắn ốc vào miệng, dày dần. Hai vòng co về miệng. **Tảng đá thành hình trong miệng**, lớn dần theo nhịp đập, nén 0,06 s rồi chớp lúc nhả.
  - `NThiemPhun`, pha bay và trúng: tảng bay có đuôi bụi liền, tới mặt trước thân thì vỡ 4–5 khối nằm lại đất. Bông va chạm theo hướng bay.
  - `NThiemLan`: bụi lăn thành cụm. Cú nện có hướng và hố.
  - `NThiemDam2`, `NThiemBo2`: cú đâm, cú bổ có hướng. Cú bổ có hố. Bụi gồng thành cụm.
- **Mong thấy ở SAU:** pha tụ có vệt cong xoắn vào miệng và tảng phập phồng lớn dần; tảng bay kéo vệt bụi be; chạm thì vỡ, đá nằm lại.
- **Còn lo:** tảng tụ vẽ ở lớp trước tướng, có thể che môi dưới lúc há; nếu xấu thì đổi `cau.group` sang `Back`.

### ho_khoan — Sa Long (`HatTho.cs`)
- **Lỗi ở TRƯỚC:**
  - mana_07–11: lưỡi cát màu xám xỉn, đuôi là chấm sẫm lẻ;
  - mana_11→12: lưỡi tắt phụt khi chạm, cú trúng chỉ có sao nhỏ và đốm nâu.
- **Đã sửa:**
  - `NLongLuoi`: lưỡi dừng ở mặt trước thân, có đuôi cát liền. Chạm thì ép dẹt, loe, tan. Bông va chạm theo hướng bay. Chỗ vuốt phóng có cụm bụi. Đối thủ giật ở mỗi lưỡi.
  - `NLongCot`, `NLongCot1`: gồng hút cát thành vệt xoắn ốc, có 2–3 vòng co về vuốt. Cú nện có hố. Chân cột sa thạch có cụm bụi hai bên, chùm dăm và hố.
  - `NLongVuot`: cú vuốt có hướng.
- **Mong thấy ở SAU:** lưỡi cát kem cát tươi kéo vệt bụi, đập vào thân thì bẹp ra thành cát, đối thủ giật từng nhát.

### phu_van — Sơn Viên (`HatTho.cs`; suy từ code)
- **Lỗi ở TRƯỚC (suy từ code):** tảng khổng lồ lớn đều, không nhịp; đá hút là chấm tròn; tảng tới nơi tắt phụt; sóng chấn có bụi chấm lẻ.
- **Đã sửa:**
  - `NVienTang`: tảng lớn theo nhịp đập, nén 0,06 s trước khi ném. Có 3 vòng co về tảng. Đá hút là vệt và sỏi xoay theo đường vồng, dày dần. Lúc ném có chớp. Tảng bay có đuôi bụi, tới nơi vỡ 6 khối. Có hố. Mưa đá nhỏ rơi xuống đất.
  - `NVienChan`: cú nện có chớp, hố và cụm bụi. Mỗi gai của sóng chấn có cụm bụi và sỏi xen kẽ. Cú hất cuối có hướng.
  - `NVienDam`: ba cú đấm có hướng, đối thủ giật cả hai cú đầu.

### hat_de — Hạt Dẻ (KHÔNG có mã trong `ThoFx`)
- **Lỗi ở TRƯỚC:** mana_05–11 là tia **nước xanh lam kèm lá** (tia cũ của `StageView.Beam`), sai hệ hoàn toàn và cụt ở đầu.
- **Đã sửa:** không sửa được trong các file tôi được phép (hat_de không có trong `ThoFx`, rơi về tia cũ). Xem đề xuất 1.

### rua_nui — Sa Trùng (`HatTho.cs`; suy từ code)
- **Đã sửa:**
  - `TrungPhut`: đất phụt có chớp nhỏ, hố, chùm dăm, hai cụm bụi nhiều múi bốc lên.
  - `TrungGo`: gò chạy ngầm rải bụi theo quãng, thành vệt liền thay cho chấm.
  - `NTrungGai`: cú giáng có chớp, hố và cụm bụi.
  - `NTrungDop`, `NTrungMieng`: cú đớp, cú ngoạm có hướng; ngoạm có hố. Hai nhịp nghiến làm đối thủ giật.

### ho_kim_cuong — Bùn Ngoạm (`HatBun.cs`)
- **Lỗi ở TRƯỚC:** ult_11–30 có hàng chục chấm bùn và đá tròn sẫm rải khắp quanh quả bóng (22 gai, mỗi gai 3 hạt).
- **Đã sửa:**
  - `DrawBunCuc` mới: cục bùn là khối nhão kéo dài theo vận tốc, có hai giọt đuôi nối liền chung viền mực, rung nhão (`kr_nham` nếu có). Không còn cầu tròn.
  - `DrawBunGiot`: giọt kéo theo vận tốc (`kr_nhamgiot` nếu có).
  - `BunNo`: ít cục mà to, mỗi cục bay kèm giọt nhỏ thành chùm. Thêm vòng va chạm và cụm bụi.
  - Mũi gai: chỉ một cụm bụi đá; dăm và giọt mỗi loại chỉ ở 1/3 số gai.
  - `BunPhut`, `BunBui`: bụi bằng `ToCum`.
  - `BunGo`: bụi rải theo quãng.
- **Mong thấy ở SAU:** bùn nhão có đuôi giọt, chạm đất bẹp thành vết; quanh quả bóng bớt chấm lẻ.

### cu_phu — Thiên Thạch Thú (`HatThach.cs`)
- **Lỗi ở TRƯỚC:**
  - ult_04: bụi cuộn người là cụm nâu xám tối;
  - ult_11–13: sỏi là chấm tròn sẫm rải khắp bãi cát;
  - ult_15–16: lửa xé gió là nhiều lưỡi lửa to rời rạc như lá cam ("đốm lửa đơn lẻ và to quá");
  - ult_18–22: nổ trùm kín mặt đối thủ, vòng nâu dày;
  - ult_24–34: khói là chuỗi đốm đen rời bay thành hàng.
- **Đã sửa:**
  - Mana: pha tụ là vệt ngọc lam/hổ phách xoắn ốc, dày dần, hai vòng co, chớp lúc phóng. Đuôi thiên thạch là nhiều cụm lửa nhỏ dày hoà thành dải liền (chỉ 25 % là lưỡi), khói đuôi bằng `ToKhoi`. Viên trúng tới mặt trước thân, có hướng. Viên thường chỉ có 3 lưỡi lửa nhỏ sau thân; viên cuối nổ lửa nhỏ sau thân (trước đây nổ ở lớp trước).
  - Ult, áo lửa: cụm nhỏ (r 9–16) dồn ở mặt trước quả cầu, 22 % là lưỡi.
  - Ult, nổ: chớp kem 2 khung. Khối lửa sau lưng đối thủ, bỏ nổ lớp trước và vành 20 lưỡi lửa to. Cột lửa phần lớn ở sau. Thay vòng sprite viền mực bằng 2 sóng đất cung dẹt. Có hố và vết nứt giữ ~1 s. Dăm thành 4 chùm. Khói than là 4 cụm nhiều múi (thấp lan ngang, cao bốc lên), tách dần.
  - Ult, phần còn lại: bụi cuộn, quay, vọt, đáp đều dùng `ToCum` và hố.
- **Mong thấy ở SAU:** sao chổi lửa liền một khối; nổ to nhưng đối thủ vẫn lộ rõ; khói đen thành cụm bốc lên rồi tách.
- **Còn lo:** `Explode` là hàm của bộ Hỏa (lưỡi lửa `luoi`), tôi chỉ đổi cỡ và lớp.

### giap_nham — Thổ Tinh (`HatThoTinh.cs` + `StageViewThoTinh.cs`)
- **Lỗi ở TRƯỚC:**
  - ult_14–22: đuôi lửa thiên thạch là que mảnh nâu đỏ tối;
  - ult_32–37: tia nhiệt hẹp, màu cam đỏ tối, đầu tia cụt ngang trên vỏ đá, không có bông va chạm ("tia beam bắn xuống nhìn màu hơi tối");
  - ult_36–41: vòng sóng đứng là vòng tròn viền mực dày (một vòng cam nâu khổng lồ phủ cả sân);
  - ult_39–43: dăm đá tím là hàng chục chấm rải khắp, cột lửa là chuỗi cầu đỏ tròn.
- **Đã sửa:**
  - `TtTia`: lõi kem rộng (bốn lớp cam / vàng / vàng kem / kem). Chân tia đặt đúng mặt trên vỏ đá và **loe** ôm vỏ. Kết thúc bằng **rút từ trên xuống**. Chỗ chạm có 3 nhịp bông va chạm + vòng va chạm, và lưỡi lửa nhỏ liếm ra hai bên.
  - `TtDuoi`: đuôi lửa lõi kem rộng, ngoài cam thay đỏ.
  - `TtSongGam`: sóng gầm thành lưỡi liềm thon hai đầu, một viền mực (`kr_songam` nếu có), thay dải đều hai viền.
  - Nổ, sóng: thay vòng sprite bằng 2 sóng đất cung dẹt không viền + 2 vòng đứng mảnh không viền. Có hố 0,55 tH.
  - Nổ, hạt: dăm thành 6 chùm (trước 40 hạt lẻ). Lưỡi lửa nhỏ hơn (12). Cột lửa là lưỡi vuốt lên thay cầu tròn. Ba tiếng nổ phụ dùng lưỡi nhỏ. Khói than bằng `ToKhoi` (ít hạt hơn, cụm to, 30 % tách). Bụi lan bằng 4 `ToCum`.
  - `TtNen`: cú nện có hướng, hố, cụm bụi, chùm dăm.
  - `TtManhBay`: vệt bụi theo quãng. Cú cắm có vòng va chạm và bông va chạm (màu đá trăng).
  - Mỗi hòn đá bám vỏ: một cụm bụi, sỏi chỉ 50 %.
- **Giữ nguyên:** cầu lửa, mây nấm, ẩn và hiện đối thủ (người dùng đã duyệt).
- **Còn lo:** chiêu cuối vẫn nặng (~190 hạt lúc nổ, bản cũ ~230) vì 45 hòn vỏ đá văng là ý tưởng chiêu. Muốn nhẹ thì bớt `TtDaVang` hoặc khói.

## C. Ngân sách hạt
- Cú trúng thường (`ToNo` 1,0): khoảng 19 hạt.
- Cú nặng (`ToNo` 2,8): khoảng 29 hạt.
- Mưa pha lê Thạch Giáp: khoảng 11 hạt mỗi mảnh.
- Mana Thiên Thạch Thú lúc đông nhất: khoảng 110 hạt (bản cũ ~200).
- Chiêu cuối Thổ Tinh và Thiên Thạch Thú vẫn vượt 120 lúc nổ (luật cho phép chiêu cuối nặng hơn chút); xem mục còn lo của từng tướng.

## D. Đề xuất sửa file chung (tôi không sửa)
1. **hat_de (Hạt Dẻ) đang bắn tia nước xanh của `StageView.Beam`.** Cần thêm dòng vào `ThoFx` (StageView.cs) và một nhánh trong
   `HatNuoc.PlayNuoc`. Tôi chưa viết hàm cho Hạt Dẻ vì chưa có mốc rig, cần người làm có rig `hat_de_1/2` đo giờ trúng. Đề xuất ý: "hạt dẻ
   đá" (cầu đá bay vồng, `ToTangBay` + `ToNo`), hoặc tia đất cát lõi kem chạm thân có bông va chạm.

2. `StageView.Beam` (tia ảnh tĩnh) còn là đường lùi cho mọi tướng không có mã: nên nhuộm màu theo hệ, hoặc cấm dùng cho hệ Thổ.
3. `HatLua.Explode`, `Smoke` (bộ Hỏa) vẫn vẽ khói bằng `sblob`. Khi có `kr_khoi` nên cho `DrawSmoke` dùng `SK("kr_khoi_", "sblob_")` để
   khói các hệ đồng bộ. Bụi chung `Bui` (`HatVoi.cs`) cũng nên đổi như `ToBui`.
4. Nếu ảnh `kr_cung` là vòng đã dẹt sẵn: có thể thay mảng cung trong `ToVong` bằng ảnh đó (một dòng `Put`), nhưng cần biết hướng và độ dẹt của ảnh.
5. Bùn Ngoạm ra sân (`BunRaSan`) dùng chung vật liệu nên đã đẹp theo; `StageViewNuot.cs` không cần đổi.
