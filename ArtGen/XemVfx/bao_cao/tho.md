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

## Đợt khung vẽ sẵn 2026-11-19 (flipbook, HatFlip.cs)

Bản sửa ở `scratchpad/fb_tho/` (gốc lúc chép ở `scratchpad/fb_tho_base/`), chưa chép vào Assets. Biên dịch thử
(`ArtGen/Spine/quai/tho5_game/bien_dich_thu.py`, chạy từ gốc project): Core, Game, Editor 0 lỗi.

Chung cho cả hệ (file mới `HatFbTho.cs` + các hàm chung trong `HatTho.cs`; chưa nhập ảnh `hat_fb_*` thì mọi chỗ rơi về hạt cũ y như trước):
- `ToCum` (cụm bụi nhiều múi): một khung `khoi` nhuộm bụi đất, cao (2,6 + 0,4 n) R. Có tham số màu (cát cho Sa Tích, Sa Long, Sa Trùng) và
  cờ "giữa không trung" (tâm cụm ở điểm gọi, bỏ 3 khung đầu cho cụm bung quanh điểm).
- `ToNo` (cú trúng): hai cụm bụi hạt → một khung `khoi` sau thân, cao 0,36 tH × √muc, màu theo dăm (cát / đất nung / đá trăng / đất), dời
  0,16 tH về phía kẻ đánh. Ghép thử thấy cụm ngay sau giữa thân bị thân che gần hết. Giữ chớp, vòng va chạm, bông va chạm, chùm dăm.
- `ToKhoiCum` (khói than nổ lớn): một khung `khoi` nhuộm khói than.
- Đuôi bụi (`ToDuoiThang`, `ToTangBay`, `ToLuoiCat`, gò `TrungGo`): cụm `khoi` bước gấp đôi, chồng nhau thành dải.
- Dòng bụi sinh đều (lắc mai, cát bốc, cát xoáy, gồng, lăn, đất rung): `ToBuiFb`, chỉ sinh 40 % số cụm, mỗi cụm to × 1,3.
- Gai / cột đá trồi: khung `gai_sat` nhuộm màu đá (`FbGai`). Chạy ba pha đúng nhịp cũ: lên (khung 4 → 11), giữ (11 → 18), vỡ rơi.
  Bỏ phần nứt đất của khung, vì vết nứt và hố đã có `ToNut` / `ToHo`.
- Nhuộm chỉ làm tối được (Image nhân màu). Khung khói xám nâu ~(124, 109, 102) nhuộm theo gợi ý (200, 170, 130) ra nâu sô-cô-la (soi tờ
  nhuộm thử), nên bụi đất dùng (250, 218, 172), ra nâu đất ~(122, 94, 70). Gai sắt nhuộm (255, 214, 152) ra sa thạch.

### thach_nhan (Thạch Giáp): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: bụi sau gót, bụi chỗ húc ra khung `khoi`. Chớp, dăm, vòng bụi dạng 2 giữ.
- Mana: bụi lắc mai ra `khoi` (40 % số cụm, to hơn). Bụi ở hốc mai lúc sỏi / pha lê rời là cụm giữa không trung. Đuôi bụi của mảnh rig là
  cụm `khoi` bước gấp đôi; mỗi cú găm có bụi `khoi`.
- Chiêu cuối: bụi gồng, bụi ở hốc pha lê, bụi mỗi mảnh mưa ra `khoi`. Giữ mảnh pha lê bay / rơi / cắm (vật rơi, không phải gai trồi).

### lung_vuong (Sa Tích): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: bụi cát ra `khoi` nhuộm cát. Vết cắn giữ.
- Mana: cát bốc quanh áo ra `khoi` nhuộm cát (40 % số cụm). Đuôi cát của phiến là cụm `khoi`. Bụi cú găm nhuộm đỏ đất nung.
- Chiêu cuối: cát xoáy quanh chân đối thủ, bụi dậm ra `khoi` nhuộm cát. Bụi tràn miệng / chân phễu của lốc cát ra `khoi` (40 %).
  Thân lốc cát giữ mảng liền: khung `loc` là lốc năng lượng xanh tím, nhuộm ra lục xỉn.

### cao_da (Tê Thiềm): đợt khung vẽ sẵn 2026-11-19
- Đòn thường (giáng sừng / đâm pha lê): bụi ra `khoi`; giữ chớp, dăm, mảnh pha lê bật.
- Mana: đuôi bụi tảng đá ra `khoi`; bụi ở miệng lúc nhả là cụm giữa không trung. Giữ hút xoắn ốc, vòng co, tảng đá, đá vỡ.
- Chiêu cuối dạng 1 (lăn): bụi toé lúc xoay và vệt bụi đường lăn ra `khoi` (40 %).
- Chiêu cuối dạng 2 (bổ): ba cột pha lê ra `gai_sat` nhuộm hổ phách, nghiêng như cũ, trồi 0,07 s, giữ 0,3 s, vỡ 0,18 s. Khung tự vỡ mảnh nên
  bỏ cú nổ dăm lúc cột tan. Bụi gồng ra `khoi`.

### ho_khoan (Sa Long): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: bụi cú vuốt nhuộm cát. Giữ ba vệt vuốt.
- Mana: lưỡi cát trăng khuyết giữ (mảng liền). Đuôi cát ra `khoi` nhuộm cát. Lúc vỡ: hai cụm cát `khoi` thay ba cụm hạt.
- Chiêu cuối (cả hai dạng): cột sa thạch ra `gai_sat` nhuộm sa thạch, đúng nhịp cũ (lên 0,12 s, giữ, vỡ 0,25 s), đỉnh cao bằng cột cũ.
  Bụi chân cột có sẵn trong khung nên bỏ hai cụm bụi hạt. Giữ dăm, hố, hút cát, vòng co, vết nứt. Mất hai vạch son trên thân cột.

### phu_van (Sơn Viên): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: bụi ba cú đấm ra `khoi`.
- Mana: sóng chấn mỗi nhịp một cụm `gai_sat` nhuộm đá nâu be, lớn dần về phía đối thủ, so le trước / sau, lật xen kẽ (trồi 0,08 s, giữ
  0,1 s, vỡ 0,16 s). Bỏ cụm bụi hạt từng nhịp, giữ sỏi bắn và cú hất cuối.
- Chiêu cuối: bụi chỗ đá bứt khỏi đất, đuôi bụi tảng khổng lồ ra `khoi`. Thêm một cụm bụi `khoi` to 0,95 tH sau lưng đối thủ lúc tảng vỡ.
  Giữ tảng, hút, vòng co, đá vỡ, mưa đá nhỏ.

### hat_de (Cổ Vương): đợt khung vẽ sẵn 2026-11-19
- Hàm mới trong `HatCoVuong.cs`:
  - `CvBui`: cụm bụi `khoi` nhuộm đất, cao 2,8 r, thay `BuiCum` (của `HatMoc.cs`);
  - `CvSo`: số cụm còn ~2/3, mỗi cụm to × 1,2;
  - `CvDaNo`: bản `ThachNo` (của `HatChim.cs`) với bụi là một cụm `khoi` to 0,5 tH sau thân.
- Đòn thường hai dạng, mana (nện, rễ trồi: cụm bụi ở nhịp chẵn), chiêu cuối (gồng, cột cắm, bắt cột): mọi cụm bụi qua `CvBui`.
- Giữ rễ (`Re` / `ReQuan`): khung `gai_la` là lá xanh, không phải rễ gỗ. Giữ lá, tảng rêu, dăm, chớp, vòng cung đất, vết đất, bóng báo
  trước, `DanhTrung`.

### rua_nui (Sa Trùng): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: bụi tổ, bụi cú đớp và nghiến ra `khoi` nhuộm cát. Giữ vết cắn.
- Mana: ba gai đá đầu ngạnh ra `gai_sat` nhuộm sa thạch, nghiêng như cũ (khung xoay ngược kim nên đổi dấu góc), đúng nhịp (trồi 0,08 s,
  giữ, lún 0,2 s). Cụm gai rộng gần bằng cao, nên hai gai bên dời từ ±0,55 ra ±0,68 tH để gai lớp trước không đè thân đối thủ.
  Mất ngạnh hổ phách ở mũi.
- Chiêu cuối: đất phụt, gò chạy ngầm (bước gấp đôi) ra `khoi` nhuộm cát.

### ho_kim_cuong (Bùn Ngoạm): đợt khung vẽ sẵn 2026-11-19
- Mọi cụm bụi ra `khoi` nhuộm đất: cú trúng, đáp, phụt bùn, gò bùn, mũi gai (nửa số), rút gai (60 %), ra sân (hai cụm thay ba).
- Giữ toàn bộ bùn (cục, giọt, toé, vương miện, vết): khung `nuoc_toe` nhuộm nâu ra lục xỉn.

### cu_phu (Thiên Thạch Thú): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: bụi ra `khoi`. Giữ vết cắn, mảnh tinh thể.
- Mana:
  - mỗi thiên thạch có một khung `cau_lua` bám đúng đường bay của bản sao (`FbCauBam`, lớp sau, cao 0,4 casterH), thay dòng 95 cụm lửa/giây;
  - viên trúng có `trung_lua` sau thân (0,7 tH, viên cuối 0,95 tH; bay sang trái thì lật), thay nổ lửa nhỏ / ba lưỡi lửa;
  - khói đuôi ra `khoi` nhuộm than (40 %);
  - giữ tia ma sát, hút xoắn, vòng co.
- Chiêu cuối:
  - bụi cuộn người (ba cụm thay năm) và bụi quay ra `khoi`;
  - lao xuống: một `cau_lua` bám tâm quả cầu, cao 4 × bán kính cầu (lõi vàng nấp sau quả cầu, vành lửa ló quanh, đuôi ngược hướng lao). Thay
    mười lưỡi lửa bùng và dòng 70–190 cụm lửa/giây;
  - nổ: `no` 1,7 tH sau lưng đối thủ (chân ở mặt đất) + `nham` 0,9 tH ở lớp đất, lệch về phía mình. Thay nổ lưỡi lửa, sáu lưỡi nhọn, lửa tạt,
    cột lửa;
  - khói than: chỉ giữ hai cụm thấp (ra `khoi`), vì khung nổ đã có nấm khói;
  - nổ phụ ra `trung_lua`;
  - giữ chớp, sóng đất, hố, vết nứt, dăm, mảnh tinh thể, tia, tro, than; nảy về: khói ra `khoi`.

### giap_nham (Thổ Tinh): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: bụi ra `khoi`; bụi cú nện nhuộm tím nhạt đá trăng.
- Mana: bụi đất rung (40 %), bụi đế mảnh (60 %, tím nhạt), vệt bụi mảnh bay (bước gấp đôi), bụi cú cắm ra `khoi`. Giữ sóng gầm `SongChi`,
  mảnh bay.
- Chiêu cuối:
  - thiên thạch lửa: đuôi là `cau_lua` bám đường bay (lớp trước, dưới hòn đá); thiên thạch bụi giữ dải đuôi bụi;
  - bụi bám (nửa số), bụi phì khi ép (40 %) ra `khoi`;
  - ba nổ phụ ra `trung_lua`, toé ra xa tâm nổ;
  - khói đen ra `khoi` nhuộm than đậm (~73, 61, 56): ~35–40 % số cụm, cao 2,2 bán kính cũ, trong 0,88, chạy chậm, mỏng dần 0,5 s cuối, để
    đối thủ hiện mờ dần sau khói;
  - giữ nguyên cầu lửa, mây nấm (người dùng đã duyệt), mặt trời, tia nhiệt + bông va chạm (tia đã có va chạm), cột lửa, lưỡi lửa văng,
    45 hòn đá văng.

### Chỗ còn ngờ (đợt khung vẽ sẵn)
- Chưa xem trong trận. Chỉ ghép thô bằng Python, đối thủ giả, để kiểm điểm neo, cỡ, lớp: `scratchpad/fb_tho_soi/soi_tho_fb.jpg`.
- Bụi nâu đất sẫm hơn bụi be sáng cũ (#E8C99A): nhuộm không làm sáng được. Muốn bụi sáng như cũ phải có khung khói sáng riêng.
- Đá vẽ sẵn ra be xám / khaki, mất chi tiết riêng: vạch son cột Sa Long, ngạnh hổ phách gai Sa Trùng. Cột pha lê Tê Thiềm dạng 2 ra hổ phách
  nâu, tối hơn `ToPhach`.
- Cụm gai vẽ sẵn rộng gần bằng cao (cột cũ hẹp): cột giữa Sa Long 1,45 tH rộng ~1,4 tH (sau lưng đối thủ, không che).
- Cỡ thiên thạch bản sao (mana Thiên Thạch Thú) chưa đo. Sao chổi chiêu cuối dài ~1,8 lần tướng; muốn ngắn thì giảm hệ số `4f * rb` trong
  `ThtCauChieu`.
- `Fb` không hiện dần: cầu lửa bám vật bay bật ra đủ cỡ ngay (chiêu cuối Thiên Thạch Thú có chớp che lúc bật).
- Khói đen Thổ Tinh: nếu đối thủ hiện sớm / muộn so với `TinhHien0..1` thì chỉnh tốc 0,6, `life` 0,75 × đời cũ trong `TtHang`.
- Ứng viên chưa làm: rễ Cổ Vương, lốc cát Sa Tích, bùn (không có khung hợp).

### Cần đổi ở file không thuộc phiên này
- Khi chép vào Assets: thêm file mới `HatFbTho.cs` cạnh `HatFlip.cs` (Unity tự sinh .meta). `StageView.cs`, `HatFlip.cs`, `HatNuoc.cs`
  không cần đổi.
- `ArtGen/Spine/quai/tho5_game/vao_game.py` chép `ArtGen/Spine/quai/tho5_game/HatTho.cs` vào Assets. Bản này đã cũ (1061 dòng, màu tối của
  ngày 11-17): chạy lại thì đè mất mọi đợt sửa sau. Đừng chạy lại, hoặc chép `HatTho.cs` mới vào đó trước.

### Đợt sửa sau khi người dùng xem trong game (2026-11-19): nổ lên lớp trước, vệt khói đuôi
Người dùng: "có vài vụ nổ layer nằm dưới địch nên không thấy rõ, các fireball, tên lửa,... nên thêm trail smoke vào".
Biên dịch thử (từ gốc project): Core, Game, Editor 0 lỗi.
- **Nổ lên lớp trước** (`HatThach.cs`, Thiên Thạch Thú; `nham` giữ lớp đất):
  - chiêu cuối: `no` từ sau lưng đối thủ lên Front. Neo dời 0,2 tH về phía mình, cao 1,6 tH (trước 1,7), tốc 1,25 (~0,8 s) cho khỏi trùm đối thủ lâu;
  - viên thiên thạch mana trúng: `trung_lua` lên Front, neo dời 0,14 tH ngược hướng bay (mặt trước thân);
  - nổ phụ chiêu cuối: `trung_lua` lên Front, dời về phía mình 0,15–0,25 tH và thấp hơn chỗ cũ (cũ ở phía xa, cao ngang đầu).
  - Nổ phụ Thổ Tinh vốn đã ở Front.
- **Vệt khói đuôi** (`FbKhoiDuoi` của `HatFlip.cs`, lớp thấp hơn vật bay; bỏ đuôi khói cũ, không chồng hai vệt):
  - Thiên Thạch Thú mana: mỗi thiên thạch một vệt, cụm 0,24 tH, 30 cụm/giây, giữa đuôi cầu lửa (Back 27, dưới cầu lửa Back 34). Thay dòng
    `ToKhoiFb` thưa.
  - Thiên Thạch Thú chiêu cuối: vệt sau quả cầu lao xuống, cụm 0,32 tH, 26 cụm/giây, 1,8 bán kính sau tâm (Back 27). Thay dòng `ToKhoiFb`.
  - Thổ Tinh chiêu cuối: mỗi thiên thạch lửa một vệt, cụm 0,22 tH, 10 cụm/giây (~8 thiên thạch lửa bay cùng lúc nên thưa), Front 27 dưới
    cầu lửa / hòn đá. Thôi nhả ở 80 % quãng cho khói không đọng trên mặt đối thủ. Thiên thạch bụi giữ dải đuôi bụi.
  - Tảng đá bay `ToTangBay` (Tê Thiềm mana, Sơn Viên chiêu cuối): vệt khói nhuộm bụi đất, cụm 1,6 bán kính (26–55), 26 cụm/giây, Front 27
    dưới tảng. Thay đuôi cụm khói theo quãng; sỏi rơi giữ. Mưa đá nhỏ (r < 8) không kéo khói.
- Vật bay đã có đuôi bụi khung `khoi` từ đợt trước nên không thêm: mảnh rig `ToDuoiThang`, lưỡi cát, mảnh bay Thổ Tinh.
- Còn ngờ: Thổ Tinh lúc đông nhất (thiên thạch + vỏ đá + khói) sát trần 120 hạt; dư thì hạ 10 cụm/giây xuống 6.

### Lốc cát vẽ sẵn (2026-11-19, người dùng chê lốc cũ "màu hơi trầm và chưa hợp lắm")
- Sa Tích chiêu cuối (`ToLocCat` trong `HatTho.cs`; hệ Thổ không còn lốc cát / lốc bụi nào khác):
  - thân lốc là khung `loc_cat` LẶP, hai lớp lệch pha nửa vòng: lớp sau đặc, lớp trước trong 0,5 để đối thủ vẫn lộ trong lốc;
  - đỉnh khung bằng miệng phễu cũ; bề ngang giãn 1,3 lần (ghép thử: phễu của khung hẹp hơn thân đối thủ), tốc 1,3;
  - hiện mượt: cao 35 % → đủ trong 0,22 s, mờ vào 0,15 s, tắt dần 0,35 s cuối;
  - bỏ phễu mảng liền + sáu dải xoắn cũ;
  - giữ mảnh đất nung bay quanh (36 → 22 mảnh/giây vì khung đã có sỏi văng), bụi miệng / chân, cát xoáy quanh chân trước lốc, giờ trả về.
- Chưa nhập ảnh thì về phễu cũ. Biên dịch thử 0 lỗi. Ghép thử: `scratchpad/fb_tho_soi/soi_loc.jpg`.
- To lên (người dùng xem trong trận: "lốc xoáy làm to lên cho che hết tướng địch"):
  - chân lốc hạ 0,34 T dưới chân đối thủ (T = 150 sc ~ thân đối thủ; dạng 2 × 1,15);
  - khung cao 2,05 T, lộ trên chân đối thủ ~1,65 T; không vượt mép trên sân;
  - giãn ngang 1,75 lần: ngang chân ~1,2 T, eo ngang bụng ~0,8–1,2 T, ngực ~1,7 T, miệng ~2,3 T; lớp trước vẫn trong 0,5.
  - Eo khung chỉ ~0,23–0,33 bề ngang (đo 8 khung). Muốn eo ≥ 1,35 T phải giãn ~2,5 lần, vân chì méo quá nên dừng ở 1,75.
  - Ghép thử: `scratchpad/fb_tho_soi/soi_loc2.jpg`. Biên dịch thử 0 lỗi.
- Đổi sang khung `loc_cat_bao` (lốc trùm, cột xoáy dày, gốc gần rộng bằng miệng), ưu tiên khi đã nhập ảnh:
  - không còn khung `loc_cat_bao` thì về `loc_cat` với cỡ của bước trước; không còn khung nào thì về phễu cũ;
  - bỏ hạ chân: chân lốc ngay dưới chân đối thủ (+0,04 T);
  - khung cao 1,7 tH (đỉnh lốc ~1,6 tH), tự hạ khi sát mép trên sân (phe địch ra ~1,64 tH);
  - giãn ngang 1,2 (dạng 2: 1,25): ngang chân / bụng ~1,1–1,25 tH, ngực ~1,5 tH, trùm kín từ chân tới đầu; lớp trước trong 0,5;
  - `ToLocCat` thêm tham số `tH` (`NTichLoc` truyền vào).
  - Ghép thử đúng chỗ hai phe (`StageView.Pos`): `scratchpad/fb_tho_soi/soi_loc3.jpg`. Biên dịch thử 0 lỗi.

### Tia vẽ sẵn (2026-11-19, người dùng: "tia năng lượng/nước như này nhìn vẫn chưa đã")
- Hệ Thổ chỉ có MỘT tia: tia nhiệt chiêu cuối Thổ Tinh (`TtHang`, `HatThoTinh.cs`). Tia đứng từ đáy mặt trời xuống vỏ đá.
  - Có `DaTiaLua` thì dùng `TiaFb`: dày 0,28 casterH, bám mặt trời đang phình và vỏ đang co, tụ 0,2 s (rig) ở đáy mặt trời.
  - Gọi sớm tụ + vươn (quãng / 2600, kẹp 0,07–0,14) để chạm đúng mốc tia cũ `TtSkTia`; dội 0,32 s rig (tới lúc tia cũ bắt đầu rút), đuôi bay nốt.
  - Bỏ thân tia mảng liền `TtTia`, lưỡi lửa liếm, ba `ToBong`. Giữ rung, ba vòng va chạm nhấp, giờ nổ, giờ trả về.
  - Chưa có bộ da thì về tia cũ.
  - Lo: cầu lửa đầu nòng cao 2,3 × bề dày (~110 đơn vị) to hơn mặt trời (~80), sẽ đè nửa dưới mặt trời lúc tụ.
- Không có tia nào khác:
  - Thiên Thạch Thú dùng thiên thạch, Sa Long lưỡi cát, Cổ Vương rễ / cột;
  - mảnh bay, vết vuốt, cột lửa không phải tia.
- Biên dịch thử 0 lỗi.
  - Cầu đầu nòng thu nhỏ: `nongK` = 65 × sc × mo / (2,3 × bề dày), kẹp 0,35–1 (~0,6, cao ~65 đơn vị), nhỏ hơn mặt trời, không còn đè lúc tụ.
