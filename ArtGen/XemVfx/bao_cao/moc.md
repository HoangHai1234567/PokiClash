# Báo cáo VFX hệ MỘC (2026-11-18)

File đã sửa (đã chép vào `Assets/01 Script/Game/Battle/`): `HatMoc.cs`, `HatDa.cs`, `HatVoi.cs`, `HatLoc.cs`, `HatCoVuong.cs`, `HatChim.cs`,
`HatRong.cs`, `HatGiac.cs`, `HatKiem.cs`.
- Biên dịch (`bien_dich_thu.py`): Core, Game, Editor đều 0 lỗi, cả lúc thay từ `Temp/vfx_moc` lẫn lúc dựng lại từ Assets sau khi chép.
- Hash bản gốc: `hash_goc.txt`; hash bản mới: `hash_moi.txt`.
- Kiểu xuống dòng giữ như bản gốc: LF cho 6 file, CRLF cho HatRong, HatGiac, HatKiem.

Chưa mở Unity, chưa chụp ảnh SAU. Phần "mong thấy" dưới đây là điều cần soi ở ảnh SAU, chưa được kiểm.

## 0. Bộ đồ dùng chung mới (đầu `HatMoc.cs`), mười tướng cùng dùng

| Mảnh | Làm gì | Ảnh hạt |
|---|---|---|
| `MocSang()` | Gọi ở đầu mọi chiêu Mộc. Đổi bảng màu của tướng sang bản tươi trong `MocTuoi`: lá #7BD34A, lục #3FAE3A, đậm sát viền #2A7F2E, kem #FAFFE0. Gạc Đá, Lộc Phong giữ lục ngọc; Giác Mộc giữ hổ phách nhưng tươi hơn | — |
| `Chop` | Chớp nổ 1–2 khung, màu kem lõi chanh, viền mực, nhỏ hơn thân đối thủ | `kr_chop`, dự phòng `burst` |
| `BuiCum` | Cụm bụi / phấn nhiều múi, hai tông (đỉnh nhạt, đáy đậm). To gần đủ ngay khung đầu, phình nhẹ, rồi tách thành 3 cụm con. Cụm con toả ra, bay lên, nhỏ dần rồi mới mờ | `kr_khoi` + `kr_khoiday`, `kr_khoinho`; dự phòng `sblob` hai lớp |
| `CungDat` | Vòng cung dẹt trên đất, đứt 3–5 đoạn, không viền, nở nhanh, mỏng dần | `kr_cung`, dự phòng mảng liền |
| `VetDat` | Vết trên đất: vệt sẫm dẹt + vết nứt, giữ ~1 s rồi mờ trong 0,5 s | `ell` + `crack` |
| `VetPut`, `TiaVunCum` | Vệt thuôn đầu tròn đuôi nhọn. Tia vụn nhỏ (dày 3–4,6) đi theo cụm 2–5 vệt lệch cỡ, không đứng lẻ | `kr_vet`, dự phòng `needle` |
| `LaRoi` | Lá rơi lượn qua lại, co dần, không tắt phụt | `leaf` |
| `BongPut`, `BongVa` | Bông va chạm. Thân bông neo ở điểm chạm, gai toé về phía con bắn. `BongVa` là hai bông xoè chữ V (±50°), đổi dáng mỗi 2 khung | `kr_tiadau`, dự phòng `crown` |
| `TiaMoc` | Tia năng lượng của bộ Mộc, chi tiết ở mục 1 | mảng liền + các ảnh trên |
| `MLiem` | Lưỡi liềm mảng liền, dày giữa thuôn nhọn hai đầu, dùng được trên mặt đất (squash) | — |
| `MuiNang`, `Liem`, `NoCau` | Nổ cầu năng lượng theo mẫu KR5, chi tiết ở mục 4 | `kr_luakhoi`, `kr_liem` |
| `NenNha` | Ngay trước lúc nhả, cầu nén lại (×0,7) trong 1–2 khung, rồi bật to ×1,25 cùng lúc chớp | — |
| `DanhTrung` (Action, StageView chưa gán) | Hook cho đối thủ chớp + giật nhẹ mỗi nhịp trúng của tia, luồng lá, sóng âm, nổ. Chưa gán thì code chạy như không có. Đề xuất gán ở mục cuối | — |

Đồ dùng ở `HatDa.cs` (cầu chung của Gạc Đá, Lộc Phong, Giác Mộc):
- **`CauLa` (quả cầu):** khối nhiều múi cuộn. Dùng `kr_cau` xoay hai lớp; dự phòng bốn múi quay quanh tâm. Lõi vàng chanh rộng, tâm kem. Cầu đập theo nhịp tim nhanh dần, 2,2 → 8,7 nhịp/giây, mỗi nhịp phồng 12 % rồi xẹp.
- **`GatherLa` (pha hút):**
  - Vệt gió và lá bay xoắn ốc vào tâm, cả đám cùng một chiều xoáy, nhanh dần (ease-in).
  - Vệt gió dùng `kr_vet`, không viền, thân kem, nửa đầu đậm hơn. Lá có mũi theo hướng bay.
  - Hạt hiện dần lúc sinh, tới tâm thì co lại nhập vào cầu.
  - Mật độ tăng từ 0,35 lên 1,65 lần tới lúc nhả. Có hai vòng co về tâm (`VongCo`).
- **Hạt hút của Giác Mộc (`NangHut`, ở `HatGiac.cs`):** vệt năng lượng tự lái về tâm, nhanh dần, chạm thì nhập vào cầu.

Ảnh `hat_kr_*` đã nhập. Đã đo khung từng ảnh (khung vuông 384, hình chiếm ~90 %) để đặt cỡ và neo đúng:
- `kr_vet`: đầu ở +x, độ dày theo từng ảnh.
- `kr_tiadau`: thân ở 22 % bề ngang khung.
- `kr_songam`: lồi về +x, dây cung 90 % chiều cao khung, giữa dày 16 % bề ngang.
- `kr_cung`: đã vẽ sẵn dẹt, nên không ép dẹt thêm.

Ảnh nào thiếu thì code tự quay về hình cũ.

## 1. Lộc Phong (`bom_la`): `n_cau_tia`, `n_cau_mom` / `n_cau_mom1` (`HatLoc.cs`)

**Lỗi ở ảnh TRƯỚC (`mana_NN`):**
- 06–09: tụ cầu là một vòng mảnh to và một quả cầu nhỏ.
- 10–19: tia là tia nước `NTia` nhuộm lục lam: có bọt trắng, có lưỡi sóng. Chỗ chạm toé nước, che mặt Cua Kìm (16–21).
- 19→20: tia cắt phụt.
- 20–25: giọt nước rơi lại, sai hệ.

**Đã sửa:**
- **`NCauTia`:** bỏ hẳn `NTia`, thay bằng `TiaMoc`.
  - Thân tia 5 lớp, lõi vàng chanh + kem rộng 56 % bề dày. Mép gợn chạy dọc dòng, đầu tia tròn.
  - Có vệt kem chảy trong thân, lá xoắn quanh thân (nửa sau vẽ sau tướng).
  - Đầu tia dừng ở MẶT TRƯỚC thân đối thủ (`ChamThan`, lùi 0,16 tH khỏi tâm thân).
  - Ở chỗ chạm:
    - chớp `Chop`;
    - bông chữ V đổi dáng mỗi 2 khung;
    - vòng va chạm mỗi 0,12 s;
    - tia vụn và mẩu lá toé ngược theo cụm;
    - bụi cụm dưới chân đối thủ;
    - `DanhTrung` mỗi nhịp.
  - Khi tắt: tia thon dần từ gốc tới ngọn (0,14 s), vỡ thành 9 mảnh năng lượng và lá rơi lượn, bông co lại sau cùng. Cuối cùng `LaNo` nhỏ.
  - Cầu: `NenNha` nén ngay trước khung bắn, `Chop` ở khung bắn.
  - Giờ trúng giữ đúng công thức cũ: `L + max(0,03, (quãng − 30)/1150)`.
- **`NCauMom`:**
  - Pha hút dùng `GatherLa` mới; bụi cụm bay lên dưới chân.
  - "Đầy" chỉ còn một vòng sáng; lúc gật đầu cầu nén rồi chớp (`Chop` ở `cNga`).
  - Đuôi lá + tia vụn lúc bay.
  - Trúng: `NoCau(1,7)` + màn chớp như cũ; nhịp toé thứ hai ở SAU thân.
  - Giờ trúng không đổi.

**Mong thấy ở ảnh SAU:**
- Tia lục ngọc lõi chanh sáng, không bọt nước.
- Đầu tia tới mép thân cua, có bông hình chữ V toé về phía hươu.
- Cuối tia gầy dần rồi vỡ vụn, không mất phụt.

**Còn lo:**
- Agent Thủy đã viết lại `NTia`, nhưng Lộc Phong không còn gọi `NTia`, nên không có hai bông va chạm chồng nhau.
- Tia hơi mảnh ở dạng 1 (hw 0,055 × chiều cao lớn hơn giữa hai con).

## 2. Giác Mộc (`moc_tinh`): `n_giac_tia`, `n_giac_tim`, đòn `n_giac_dam` (`HatGiac.cs`)

**Lỗi ở ảnh TRƯỚC:**
- Mana (`mana_NN`):
  - 04–11: cầu như đồng xu nâu xỉn, vòng mảnh, ít lá.
  - 12–21: tia mảnh màu kaki, trông như cây gậy.
  - Chỗ chạm chỉ có sao nhỏ đè lên mặt cua (14, 18) và vòng mảnh (15).
  - 21→22: tia mất phụt.
- Chiêu cuối (`ult_NN`):
  - 10, 18: vòng kem mảnh rất to quanh con ra chiêu.
  - 22–33: tia như tấm ván gỗ (viền nâu cam, lõi be), mũi nhọn đâm vào cua.
  - 33–34: thân tia trượt vào cua như khúc gỗ bay.
  - 35: chớp che mặt cua.
  - 36–37: vòng kem to + cục bọt trắng trên mặt.

**Đã sửa:**
- **`NGiacTia`:**
  - Tia dùng `TiaMoc` (hw 0,05, trước là 0,042). Giờ trúng giữ `quãng/2600`.
  - Năng lượng từ tim lên đỉnh sừng chuyển sang `NangHut`, mật độ tăng dần.
  - Cầu `NenNha` + `Chop` ở khung bắn. Hết tia: `LaNo` 0,75.
- **`NGiacTim`:**
  - Nhịp tim: `VongVa` + chớp nhỏ ở các nhịp sau. Năng lượng hút vào tim bằng `NangHut`.
  - Vòng co sát vào tim trước lúc bắn; chớp `Chop` to ở khung bắn.
  - Tia `TiaMoc`: hw 0,11, bông ×1,4, có bông chập chờn ở gốc (quả tim).
  - Dọc đường tia có bụi cụm và lá bị thổi.
  - Ở chỗ trúng: `DatNut` + vết nứt hổ phách giữ 1,2 s.
  - Hết tia: `NoCau(1,35)`. Đã bỏ các chớp lặp đè lên mặt cua.
- **`NGiacDam`:**
  - Dậm: `CungDat` + vết nứt hổ phách (ảnh `crack` nhuộm hổ phách) + bụi cụm.
  - Năm chỗ đất bật, mỗi chỗ để lại vết nứt hổ phách giữ ~1 s, thành một đường nứt chạy tới đối thủ.
  - Tia vụn hổ phách nhỏ, theo cụm.
  - Trúng: chớp nhỏ ở trước, khối toé sau thân, vòng cung dẹt.
- Đã bỏ `GiacTiaSang` (tia cũ) và `GiacLoi`.

**Mong thấy ở ảnh SAU:**
- Tia hổ phách tươi, lõi kem chanh rộng, mép gợn.
- Bông chữ V ở mép thân cua.
- Hết tia thì gầy từ gốc rồi vỡ, sau đó nổ cầu nhiều múi ở sau thân.
- Đòn thường để lại vệt nứt sáng trên đất.

**Còn lo:**
- Chiêu cuối dày, nhiều lớp.
- Lúc nổ `NoCau` đỉnh khoảng 36 hạt sống: chiêu cuối được phép nặng hơn, nhưng cần đo.

## 3. Rồng Trúc (`thanh_long`): `n_rong_gam`, `n_rong_van`, đòn `n_rong_dam` (`HatRong.cs`)

**Lỗi ở ảnh TRƯỚC (`mana_NN`):**
- 07–14: sóng âm là cung móng ngựa dày đều, không thuôn, giống cầu vồng.
- Sóng bay qua và trùm kín mặt cua (09–14), mờ tại chỗ.
- Bụi lấm tấm.

**Đã sửa:**
- **`SongAmMoc` (mới) cho `NRongGam`:**
  - Dải cung dày giữa thuôn nhọn hai đầu, lồi về phía bay.
  - Nở từ 0,12 casterH lên 0,8 tH, bề dày giảm 40 % theo quãng.
  - Tới mặt trước thân đối thủ (lùi 0,22 tH) thì bẹt ra, mỏng hẳn rồi tan trong 0,1 s, không trùm mặt.
  - Đợt chẵn và lẻ đảo màu kem / lục tươi. Dùng `kr_songam`, dự phòng `MLiem`.
  - Mỗi đợt tới nơi: `DanhTrung`, vòng va chạm nhỏ, tia vụn toé ngược.
  - Lấy hơi bằng `GatherLa`. Bụi cụm và lá bị thổi dọc đất.
  - Giờ trúng giữ như cũ: `s0 + quãng/980`. Đợt đầu bung ở mặt trước thân, sớm hơn ~0,03 s.
  - `SongAm` cũ giữ nguyên vì Bạch Viêm Hổ (`HatHo.cs`) còn dùng.
- **Sét:**
  - `DrawSet` đọc màu từ `q.stops` nếu có (vàng tươi #FFE840, lõi kem rộng 55 %). Pháo Giáp không gán `stops` nên giữ màu cũ.
  - `SetGiang`: chớp nhỏ ở trước, toé sau thân, tia vụn theo cụm (trước là chớp to che mặt).
- **`DatNut`:** dùng `CungDat` + `BuiCum`.
- **`NRongDam`:** vòng cung dẹt hai lớp, bụi cụm, vết đất. Vòng co báo trước bằng cung dẹt.
- **`NRongVan`:**
  - Kén hút lá bằng `GatherLa`. Kén bung: chớp + khối toé sau thân + phấn cụm.
  - Bão lá nhỏ lại: lá 6–10,5, trước là 7,5–13. Có `DanhTrung` nhịp lúc chém.
  - Sập cánh: cung dẹt, vết đất 1,1 s, bụi cụm.

**Mong thấy ở ảnh SAU:** các lưỡi liềm âm thanh thuôn nhọn hai đầu, nối nhau, to dần và mỏng dần, tan ở mép thân cua; bụi thành cụm.

**Còn lo:** đợt cuối có cung rộng 0,8 tH, hai đầu cung có thể quét qua mép thân con đối thủ to (cua) trong 0,1 s lúc tan.

## 4. Gạc Đá (`gac_da`): `n_da_va`, `n_cau_la` (`HatDa.cs`)

**Lỗi ở ảnh TRƯỚC (`ult_NN`):**
- 05–17: cầu là đĩa lục sẫm phẳng.
- Vệt hút trắng viền mực dày như que xương, bay gần thẳng (12–17).
- Vòng mảnh nhạt rất to (04, 09, 12, 14).
- 20–25: nổ thành đống lá + bọt trắng che mặt cua.

**Đã sửa:**
- **`NCauLa`:**
  - Cầu dùng `CauLa` mới, nhịp tim nhanh dần. Hút bằng `GatherLa` mới.
  - "Đầy" chỉ còn một vòng sáng ở sau.
  - Rời tay: nén + chớp. Đuôi lá + tia vụn.
  - Trúng: `NoCau(1,4)`:
    - chớp ở trước;
    - 5 múi năng lượng ở SAU thân, teo thành đốm;
    - 5 lưỡi liềm;
    - vành lá, tia vụn theo cụm;
    - phấn cụm và bụi cụm tách dần;
    - hai vòng cung dẹt, vết đất 1 s;
    - lá rơi lượn.
- **`NDaVa`, `DaNo`:** chớp nhỏ ở trước, khối toé sau thân, dăm đá nhỏ hơn, bụi cụm, vòng cung dẹt, vết đất. Đá sáng hơn một nấc.
- Giờ trúng không đổi.

**Mong thấy ở ảnh SAU:**
- Cầu gồ ghề cuộn, lõi chanh, đập phập phồng.
- Vệt gió thuôn xoắn vào cầu; cầu khựng nén rồi loé lúc ném.
- Nổ có múi lớn sau cua, mặt cua không bị che.

## 5. Lâm Tượng (`phong_linh`): `n_voi_phun`, `n_dam_rung` / `n_dam_rung1`, đòn `n_hat_nga` (`HatVoi.cs`)

**Lỗi ở ảnh TRƯỚC (`ult_NN`):**
- 15–21: lá rải rác, bụi lấm tấm, không thấy sóng đất.
- 21–22: chỉ có vòng + lá ở đối thủ.

**Đã sửa:**
- **`NVoiPhun`:**
  - Hít bằng `GatherLa`.
  - Hai nhịp phụt có `Chop` + phấn cụm. Lá nhỏ hơn.
  - Ở mặt trước thân đối thủ: bông chữ V liên tục, tia vụn màu mật, `DanhTrung` mỗi nhịp.
- **`SongDat` (mới) cho `NDamRung`:**
  - Một cung của vòng elip trên đất, tâm ở chỗ dậm, dày giữa thuôn hai đầu.
  - Lục + chanh, không viền.
  - Bán kính lớn tới chân đối thủ đúng lúc trúng, nở rộng và mỏng dần, cùng nhịp với các cột lá.
- **Dậm:** hai lớp cung dẹt, vết đất, bụi cụm lớn tách dần.
- **`CotLa`:** cung dẹt nhỏ + bụi cụm.
- **Trúng:** `LaNo`, cung dẹt, vết đất, bụi cụm, `DanhTrung`.
- **`NHatNga`:** bụi cụm, cung dẹt, chớp nhỏ ở trước + toé sau thân.
- **`Bui` giữ nguyên** vì 13 file hệ khác đang dùng.

**Mong thấy ở ảnh SAU:** một làn sóng lục chạy trên đất từ chân voi tới chân đối thủ, các cột lá phụt dọc theo, bụi thành cụm mềm.

## 6. Mầm Ú (`mam_u`): `n_la`, `n_la_va`; Cầu Gai (`tien_la`): `n_gai`, `n_gai_va`; người cây (`long_vuot`): `n_gai_va`, `n_la_va` (`HatMoc.cs`)

**Lỗi ở ảnh TRƯỚC (đã soi lướt, `mana`/`ult` 06–36):**
- Luồng lá thưa.
- Chỗ chạm chỉ có vài lá. Cú húc có bọt trắng kiểu nước (`mam_u/ult_12`).
- Chớp ở trước che mặt.

**Đã sửa:**
- **`NLa`:**
  - Hít bằng `GatherLa`. Lá 80/giây, cỡ 6–10,5 (trước là 72/giây, 7,5–12,5).
  - Phấn cụm thay bọt nước ở mồm.
  - Ở mặt trước thân: bông chữ V liên tục, tia vụn theo cụm, `DanhTrung`.
- **`LaNo` (dùng chung cả bộ):**
  - Chớp nhỏ ở trước, khối toé ở SAU thân.
  - Vành lá đều góc, lá 3,6–6,4. Tia vụn theo cụm.
  - Phấn cụm sau lưng tách dần; vòng cung dẹt. Không còn bọt trắng.
- **`NLaVa`, `NGaiVa`:** bụi cụm, cung dẹt, vết đất.
- **`NGai`:**
  - Dăm gai hút xoắn vào thân, mật độ tăng dần.
  - Cụm gai trồi có bụi cụm.
  - Trúng: vết đất + bụi cụm, `DanhTrung`.
- **`GaiNo`:** chớp nhỏ ở trước + khối toé sau thân + phấn cụm.
- **Màu lá:** lục giữa và lục tươi (trước là lục đậm, trông tối).

**Mong thấy ở ảnh SAU:** lá tươi hơn, chỗ chạm có bông toé, không có bọt trắng.

## 7. Cổ Vương (`gio_loc`): `n_re_troi`, `n_tru_giang` / `n_tru_giang1`, đòn `n_tru_dap` / `n_vuong_huc` (`HatCoVuong.cs`, `HatChim.cs`)

**Lỗi ở ảnh TRƯỚC:** cột cắm (`ult_16–21`) có vòng tối và bụi be lấm tấm; chớp ở trước che đầu đối thủ.

**Đã sửa:**
- Bụi thành cụm ở mọi chỗ; vòng cung dẹt hai lớp; vết đất 0,9–1,1 s.
- Gồng của `NTruGiang`: lá + vệt gió hút xoắn vào lõi (`GatherLa`).
- Ba nhịp siết của `NReTroi`: chớp nhỏ ở trước, toé sau thân, `DanhTrung`.
- `ThachNo` (`HatChim.cs`): chớp nhỏ ở trước, toé sau thân, bụi cụm.
- Lá rơi lượn (`LaRoi`).
- `ThachU`, `SoiGio` không đổi vì bộ Thổ và Kim đang dùng.

## 8. Voọc Tướng (`tho_hoang`): `n_kiem_rut`, `n_kiem_ao` (`HatKiem.cs`)

**Lỗi ở ảnh TRƯỚC:**
- Bụi lấm tấm.
- Tia vụn của nhát chém to (6–9).
- `ult_30`: sáu vệt nổ lại chồng thành ngôi sao kem to che mặt. Chưa sửa, xem mục cuối.

**Đã sửa:**
- `ChemToe`: chớp kem chanh nhỏ (`Chop`), tia vụn nhỏ theo cụm, lá nhỏ hơn, `DanhTrung`.
- Bụi cụm ở cú biến mất, hiện lại, chốt; cung dẹt; vết đất; lá rơi lượn.
- `LaLieu` và `VetChem` không đổi vì Bạch Viêm Hổ dùng chung.

## 9. Nhịp, ngân sách, hợp đồng thời gian

- **Hợp đồng thời gian:** mọi hàm trả về giờ trúng như cũ (công thức giữ nguyên). Tia giữ đúng `dur` cũ (0,88 / 1,0), nên `HoldNuoc` vẫn khớp. Ngọn tia mất hẳn ở `dur + 0,04`.
- **Đỉnh trong 0,1 s đầu:** chớp 0,06–0,09 s; bông bật quá cỡ ×1,2 trong 0,05 s; cụm bụi to gần đủ trong 20 % đời.
- **Tan bằng vỡ:** cụm tách, tia vỡ mảnh, múi teo thành đốm, lá rơi lượn.
- **Ngân sách:**
  - Tia mana ở chỗ chạm khoảng 22–25 hạt sống: toé 11 lần/giây × 3 vệt, bụi 3 lần/giây.
  - `LaNo` ở hệ số 1,5: khoảng 22 hạt.
  - `NoCau` (chỉ chiêu cuối): đỉnh khoảng 36.
  - Luồng lá `NLa` vẫn đông (~40 lá sống), như bản người dùng đã đòi "nhiều lá".
  - Cụm bụi tách 1 → 3 nhưng thay cho 3–4 hạt `Bui` cũ, và phải sau 0,3–0,4 s mới tách.
- **Không sinh GameObject mới:** chỉ thêm `P` vào hàng chờ như code cũ. Mảng liền đi qua `HatMang` có sẵn.

## Đề xuất sửa file chung (chưa làm, phiên chính quyết)

1. **`StageView.cs`, gán hook `DanhTrung`** khi dựng `HatLua` (cạnh `Shake = ...`), ví dụ:
   ```csharp
   DanhTrung = (pos, muc) => { /* tìm con đứng gần pos nhất; chớp _Flash 1–2 khung + bật lùi nhẹ (0,04–0,08 H × muc), KHÔNG hiện số, KHÔNG khựng */ }
   ```
   - Tia, luồng lá, vòi phun, sóng âm, nổ cầu đã gọi sẵn ở từng nhịp trúng (mức 0,25–1).
   - Chưa gán thì đối thủ chỉ chớp + giật một lần ở giờ trúng như cũ. Yêu cầu "đối thủ chớp + giật liên tục" chỉ xong khi hook này được gán.
   - Chạy được cả ở `HeroViewer` (null thì bỏ qua).
2. **`HatNuoc.cs`, đưa bảng `MocTuoi` (đầu `HatMoc.cs`) vào `WThemes`**, rồi bỏ `MocTuoi`, `MocSang` và các lời gọi `MocSang()`. Hiện `MocSang` tra ngược `WThemes` để thay `wth` bằng bản tươi, mỗi tướng chỉ dựng một lần.
3. **Agent Hỏa:** `HatHo.cs` (Bạch Viêm Hổ) còn dùng `SongAm` cũ (móng ngựa dày đều, bay xuyên đối thủ). Có thể đổi sang kiểu `SongAmMoc` (`HatRong.cs`) với bảng màu lửa.
4. **Các hệ khác:** `Bui` (`HatVoi.cs`) giữ nguyên vì 13 file khác dùng. Muốn bụi thành cụm thì gọi `BuiCum(pos, vel, r, life, group, mau, tach)`.
5. **`VetChem` / `LaLieu` (dùng chung với `HatHo.cs`):** loạt nổ lại của Voọc Tướng (`tho_hoang/ult_30`) chồng 6 vệt thành ngôi sao kem che mặt. Đề xuất lệch tâm các vết ra mép thân, hoặc thu `day` của vệt khi nổ lại. Chưa đổi vì đụng Bạch Viêm Hổ.
6. **Ảnh `hat_kr_khoi*`, `hat_kr_khoinho*` có mép mờ (blur)**, lệch luật "không gradient". Nếu người dùng chê "mờ" thì cần vẽ lại mép cứng.
7. **Tour chụp lại 10 tướng.** Khung cần soi:
   - tia: khung đầu tia chạm và 3–4 khung cuối tia (`bom_la`, `moc_tinh` mana và chiêu cuối);
   - sóng âm (`thanh_long` mana);
   - pha tụ cầu (`gac_da`, `bom_la` chiêu cuối);
   - sóng đất (`phong_linh` chiêu cuối).
