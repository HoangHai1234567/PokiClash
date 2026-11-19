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

## Đợt khung vẽ sẵn (flipbook) 2026-11-19

Bản sửa ở thư mục làm việc `fb_moc/` (scratchpad của phiên), chưa chép vào `Assets/`. Biên dịch thử ngoài Unity: Core, Game, Editor đều 0 lỗi.

**Chung:**
- File mới `HatFbMoc.cs` (partial `HatLua`), chỉ chiêu Mộc gọi:
  - `MocGaiFb`: gai lá `gai_la`. Đỉnh phóng (khung 8) rơi đúng giờ hẹn, nên giờ trúng cũ giữ nguyên và khung nứt đất hiện trước một nhịp. Pha giữ (khung 9–16) kéo dài được; cuối đời mờ 0,08 s.
  - `MocLocFb`: lốc `loc` lặp sau lưng con đang gồng. Nở từ 40 % trong 0,18 s, mờ dần 0,2 s lúc tắt.
  - `MocKhoiFb`: khung `khoi` nhuộm ra bụi đất (`MocBuiFbC` = 255, 236, 204), có trôi và hãm.
  - `MocBuiHaiBen`: hai cụm hai bên cú dậm / nện, thêm một cụm giữa nếu cần. Thay 3–6 cụm `BuiCum`.
- Chỗ nào cũng giữ đường cũ khi chưa nhập ảnh (`HasFb` / trả null).
- Đồ dùng chung với hệ khác giữ nguyên: `BuiCum`, `Bui`, `Spike`, `Shard`, `ThachNo`, `CungDat`, `VetDat`, `GatherLa`, `Chop`, `LaRoi` (`HatCoVuong.cs` và các hệ Kim, Hỏa đang dùng). Chỉ đổi chỗ gọi trong chiêu Mộc và các hàm chỉ Mộc dùng: `NoCau`, `DatNut`, `CotLa`, `DaNo`.
- Không đụng tia `TiaMoc` (kể cả bụi dưới chân lúc tia chạm), sóng âm `SongChi`, quả cầu `CauLa`, hút xoắn `GatherLa`, lá vỡ `LaNo`, chớp, sét.
- Không dùng `no`: khung lửa nhuộm lục ra nâu bùn (ảnh thử `fb_moc_xem/tint_no.jpg`). Không dùng `lua_*`, `nuoc_*`, `cau_*`.

### mam_u (Mầm Ú): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: không có hiệu ứng riêng.
- Mana `n_la`: giữ nguyên (luồng lá, không có khung lá).
- Chiêu cuối `n_la_va`: bốn cụm `BuiCum` dưới chân đối thủ thành hai cụm khói nhuộm đất. `LaNo` giữ.

### tien_la (Cầu Gai): đợt khung vẽ sẵn 2026-11-19
- Mana `n_gai`:
  - Hàng gai chạy tới chân đối thủ: 4 `Tuft` thành 4 cụm `gai_la` chính lớn dần, thêm 3 cụm nhỏ chen giữa lệch sang bên kia, trễ nửa nhịp. Đỉnh phóng trùng nhịp cụm cũ (gọi + 0,07 s). Vẽ ở Back.
  - Vòng gai quanh đối thủ: `Tuft` + 5 `Spike` thành 4 cụm cao so le sau lưng (1,05–1,3 tH, đỉnh lệch nhau 0–0,08 s) và 2 cụm thấp hai bên phía trước (0,4 tH, không che mặt). Gai giữ ~0,4 s rồi gãy rụng lá ngay trong khung, nên bỏ đợt "gai rút" bằng dăm.
  - Bụi thành khói nhuộm đất.
  - Giữ: dăm gai hút lúc gồng, `GaiNo` (chớp, khối toé, dăm), nhịp rung và dăm theo từng gai, cung đất, vết đất, giờ trúng.
- Chiêu cuối `n_gai_va`: `Tuft` thành 3 cụm `gai_la` so le sau lưng (bỏ khung nứt vì gọi đúng khung chạm). Bụi thành khói.

### long_vuot (người cây): đợt khung vẽ sẵn 2026-11-19
- Mana `n_gai_va` và chiêu cuối `n_la_va` dùng chung hàm với Cầu Gai và Mầm Ú: gai quất trúng có 3 cụm gai lá bật sau lưng đối thủ, bụi thành khói.

### gac_da (Gạc Đá): đợt khung vẽ sẵn 2026-11-19
- Mana `n_da_va`: bụi đá của `DaNo` (hai `BuiCum` mỗi cú) thành một cụm khói sau thân. Bụi chân thành hai cụm. Dăm đá giữ.
- Chiêu cuối `n_cau_la`:
  - Bụi cuốn lên lúc tụ thành khói bay lên, 3,5 cụm/giây.
  - Bụi chân của `NoCau` thành 3 cụm khói.
  - Giữ: cầu, `GatherLa` (người dùng dặn "gió / lá bị hút vào cầu", lốc mọc từ đất không đúng ý), múi năng lượng của `NoCau` (chưa có khung nổ năng lượng lục).

### bom_la (Lộc Phong): đợt khung vẽ sẵn 2026-11-19
- Mana `n_cau_tia`: không đổi (tia có va chạm, cầu, hút).
- Chiêu cuối `n_cau_mom`: bụi cuốn lên thành khói bay lên. `NoCau` như Gạc Đá.

### phong_linh (Lâm Tượng): đợt khung vẽ sẵn 2026-11-19
- Đòn thường `n_hat_nga`: bụi cào đất, chân sau đạp và cú nện thành khói (1, 2 và 2 cụm).
- Mana `n_voi_phun`: không đổi (hạt cây, lá, phấn).
- Chiêu cuối `n_dam_rung` / `n_dam_rung1`:
  - Lúc gồng: lốc `loc` sau lưng voi tới ngay trước cú dậm. Lá cuốn giảm từ 76 xuống 40 lá/giây.
  - Mỗi `CotLa` dọc sóng đất có thêm một cụm `gai_la` phóng lên. Lá bắn lên còn ~40 %. Bụi thành khói.
  - Rễ nâu (5 `Spike`, dạng cuối) thành 5 cụm `gai_la` có thớ gỗ: 3 cao so le sau lưng, 2 thấp hai bên.
  - Bụi dậm và bụi trúng thành khói.
  - Giữ: `SongDat`, cung đất, vết đất, `LaNo`, đất vụn, giờ trúng.

### gio_loc (Linh Điểu): đợt khung vẽ sẵn 2026-11-19
- Giữ nguyên phần phiên sáng nay vừa làm (`NMoDam`, `NLaGam`, `NThachRoi`); chỉ thay bụi và thêm lốc.
- Đòn thường `n_mo_dam`: 6 đốm `Bui` lúc bật thành 2 cụm khói hất ra sau.
- Mana `n_la_gam`: 9 đốm `Bui` lúc quạt thành 3 cụm khói bay về phía đối thủ.
- Chiêu cuối `n_thach_roi`:
  - Lúc gồng: lốc sau lưng chim, tắt sau lúc ngửa cổ gọi. Lá và sợi gió cuốn còn ~55 %. Bụi gồng thành khói.
  - Bụi đuôi tảng đá: `Bui` 46/giây thành khói 18/giây, cỡ theo tảng.
  - Bụi dội xuống đất: 14 `Bui` thành 4 cụm khói.
  - Giữ `ThachNo` (Cổ Vương dùng chung), tảng đá, lá, sợi gió, vòng `Ripple`.

### thanh_long (Rồng Trúc): đợt khung vẽ sẵn 2026-11-19
- Đòn thường `n_rong_dam`: bụi chồm thành 1 cụm khói, dậm thành 3 cụm. `DatNut` mỗi chỗ đất bật là 1 cụm khói. Sét giữ.
- Mana `n_rong_gam`: giữ `SongChi`. Bụi bị thổi thành khói, ít cụm hơn.
- Chiêu cuối `n_rong_van`:
  - Bụi lúc sấp thành khói.
  - Lúc dựng cánh gầm: lốc sau lưng rồng, mờ dần vào kén. Lá cuốn giảm từ 70 xuống 36 lá/giây.
  - Măng nhú báo trước: 4 `Spike` thành 4 cụm `gai_la` nhỏ (hai giữa sau lưng, hai ngoài phía trước), đứng chờ rồi gãy đúng lúc sập cánh.
  - Rừng măng trúc: 7 `Spike` thành 6 cụm `gai_la` so le (4 cao sau lưng, 2 thấp hai bên). Khung nứt đất hiện cùng vòng co báo trước.
  - Bỏ 2 `CotLa` (trùng việc). Lá phun giảm từ 80 xuống 60 lá/giây. Bụi thành khói.
  - Giữ kén, bão lá, vệt chém, sét.

### moc_tinh (Giác Mộc): đợt khung vẽ sẵn 2026-11-19
- Đòn thường `n_giac_dam`: bụi co chân thành 1 cụm khói, dậm thành 3 cụm, `DatNut` (5 chỗ + chỗ trúng) thành khói. Vết nứt hổ phách giữ.
- Mana `n_giac_tia`: không đổi (tia).
- Chiêu cuối `n_giac_tim`:
  - Bụi lúc mở ngực thành 2 cụm khói. Bụi cuốn lên thành khói bay lên.
  - Bụi dọc đường tia thành khói (~5,5 cụm/giây).
  - `NoCau` như Gạc Đá.
- Code hiện tại không có gai đâm lên (gợi ý giao việc có nhắc Giác Mộc), nên không thêm gai.

### tho_hoang (Voọc Tướng): đợt khung vẽ sẵn 2026-11-19
- Đòn thường: không có hiệu ứng riêng.
- Mana `n_kiem_rut`: bụi tuột lại lúc lướt thành khói, thưa hơn.
- Chiêu cuối `n_kiem_ao`: bụi lúc biến mất thành 2 cụm khói, lúc hiện lại thành 1, lúc chốt thành 2. Vệt chém, sẹo, sợi gió, lá giữ.

### Còn ngờ (đợt khung vẽ sẵn)
- Bụi mới đậm hơn bụi be cũ, vì khung khói nâu xám nhân màu chỉ tối đi. Cần soi trên nền cát. Nếu tối quá thì cần một bộ khung bụi be riêng.
- Lốc có dải tím và ngọc lam, đặt sau lưng con ra chiêu (cao 1,1–1,25 lần thân). Cần soi xem có lấn hình Rồng Trúc, Linh Điểu không.
- Gai lá xanh thay gai kem của Cầu Gai và rễ nâu của Lâm Tượng, nên đổi màu nhận diện. Nếu người dùng muốn giữ màu cũ thì nhuộm `tint`, nhưng chỉ tối đi được.
- `NoCau` vẫn là múi năng lượng bằng hạt. Đề xuất gen thêm bộ 24 khung "nổ năng lượng lá" (lục, chanh, kem).
- Lúc sập cánh (Vạn Diệp), 0,2 s đầu vẫn ~150 hạt sống, do đuôi bão lá có từ trước. Bản cũ ~230.
- Chưa soi trong Unity. Cần tour chụp lại 10 tướng: hàng gai của Cầu Gai, rừng măng, rễ Lâm Tượng, lốc lúc gồng, bụi.

### Cần đổi ở file không thuộc hệ Mộc
- Chép `HatFbMoc.cs` vào `Assets/01 Script/Game/Battle/`. Unity tự tạo `.meta` và cập nhật csproj.
- `HatCoVuong.cs` (Cổ Vương, nay là hệ Thổ) còn dùng `ThachNo`, `BuiCum`, `Spike` (rễ trồi) kiểu cũ. Agent Thổ có thể gọi `MocGaiFb` / `MocKhoiFb` / `MocBuiHaiBen` của `HatFbMoc.cs` (cùng partial class).
- `HatNuoc.cs`, `PlayNuoc`: `n_gai` / `n_gai_va` vẫn rẽ theo `HasGai` (ảnh gai cũ). Không cần đổi, vì `NGai` còn dùng `Shard` (ảnh `shard_*`).

### Sửa lớp vẽ gai (2026-11-19, sau khi người dùng xem trong game: "có vài vụ nổ layer nằm dưới địch nên không thấy rõ")
- Hàm mới `MocVongGai` (`HatFbMoc.cs`) dựng vòng gai quanh chân đối thủ:
  - Lớp trước (Front): hai cụm to hai bên, lệch ±0,62–0,64 tH, cao 0,78–0,84 tH, đứng chếch trước chân. Thêm một cụm vừa chếch trước chân phía con ra chiêu (±0,4 tH, 0,6 tH), vẽ đè lên.
  - Lớp sau (Back): cụm cao làm nền, to hơn để ló lên trên vai.
  - Không cụm cao nào ngay trước mặt.
- Cầu Gai, mana:
  - Hàng gai chạy tới chuyển sang Front.
  - Vòng gai: cụm sau lưng từ 0,95–1,3 lên 1,25–1,5 tH; hai cụm trước từ 0,4–0,44 lên 0,78–0,84 tH, thêm cụm chếch trước 0,6 tH.
- Cầu Gai chiêu cuối / Long Vuốt mana (`NGaiVa`): ba cụm Back thành hai cụm Back (1,3 và 0,95 tH) và hai cụm Front hai bên (0,72–0,77 tH). Hàm không biết phía con ra chiêu nên không có cụm chếch trước.
- Rồng Trúc, rừng măng: cụm sau lưng từ 0,96–1,25 lên 1,25–1,55 tH; hai cụm trước từ 0,46–0,5 lên 0,83–0,89 tH, thêm cụm chếch trước 0,64 tH.
- Rồng Trúc, măng nhú: hai cụm ngoài (Front) dời ra ±0,52 tH, cao 0,34 tH; hai cụm trong (Back) cao 0,42 tH.
- Lâm Tượng, rễ: cụm sau lưng từ 0,9–1,12 lên 1,15–1,4 tH; hai cụm trước từ 0,44–0,46 lên 0,78–0,84 tH, thêm cụm chếch trước 0,6 tH.
- Lâm Tượng, cột gai dọc sóng đất: chuyển sang Front, trừ cột cuối sát chân đối thủ.
- Lốc không đổi.
- Biên dịch thử: 0 lỗi.

### bom_la (Lộc Phong): tia vẽ sẵn cho mana `n_cau_tia` (2026-11-19)
- Người dùng chê: "các tia năng lượng/nước như này nhìn vẫn chưa đã".
- Có đủ ảnh (`HasTia(DaTiaMoc)`) thì `NCauTia` chạy `NCauTiaFb` (`HatLoc.cs`). `TiaFb` thay thân tia `TiaMoc` + cầu nhỏ `CauLa` + bông trúng. Chưa đủ ảnh thì tia hạt cũ.
- **Cỡ:** bề dày 0,22 casterH (tia cũ 0,11 × chiều cao lớn hơn giữa hai con).
- **Điểm đầu, điểm cuối:** đầu là điểm giữa hai gạc (`mouth`), cuối là mặt trước thân đối thủ (`ChamThan`), như cũ.
- **Tụ:** từ lead − 0,62; cầu xoáy đầu nòng lớn dần. Hạt hút xoắn giữ, với rộng 0,6 casterH.
- **Giờ chạm giữ:** lead + quãng/1150.
  - Lúc phóng = giờ chạm − tVuon (tVuon = quãng/2600, kẹp 0,07–0,14), nên phóng trễ khung bắn của clip ~0,1 s.
  - Chớp nòng dời theo lúc phóng.
  - Giờ trả về không đổi.
- **Dội:** tBan = lead + 0,68 − giờ chạm (mốc tắt cũ). Nhịp trúng như `TiaMoc`:
  - lúc chạm: rung 0,3 + `DanhTrung` 0,7;
  - mỗi 0,12 s tới lead + 0,84: `DanhTrung` 0,3 + rung 0,1;
  - mỗi nhịp một lá bật ngược, xen lá phong đỏ cam và lá xanh;
  - tia vụn 7 cụm/giây, bụi khói dưới chân đối thủ.
- **Tắt:** 6 mảnh năng lượng bay theo hướng tia rồi rơi, kèm lá phong. Đuôi tia tới đích thì `LaNo` 0,7.
- Biên dịch thử: 0 lỗi. Chưa soi trong Unity: khung `tia_moc_trung` chưa có nên trong game vẫn chạy tia cũ.

### moc_tinh (Giác Mộc): tia vẽ sẵn da vàng cho mana và chiêu cuối (2026-11-19)
- Có đủ ảnh (`HasTia(DaTiaVang)`) thì hàm `GiacTiaFb` (`HatGiac.cs`) thay thân tia `TiaMoc`, bông gốc và bông trúng bằng `TiaFb(DaTiaVang)`. Chưa đủ ảnh thì tia hạt cũ.
- **Giữ hợp đồng thời gian của `TiaMoc`:**
  - đầu tia chạm đúng giờ trúng cũ (lead + quãng/2600): lúc phóng = giờ chạm − tVuon, nên lệch khung bắn của clip dưới 0,07 s;
  - nhịp trúng như cũ: lúc chạm rung 0,3·manh + `DanhTrung` 0,7; rồi mỗi 0,12 s tới mốc nhịp cuối `DanhTrung` 0,3 + rung 0,1·manh;
  - đuôi tia bay vào tới đích đúng lúc tia cũ mất hẳn, nên `LaNo` của mana và `NoCau` của chiêu cuối giữ giờ;
  - chớp nòng dời theo lúc phóng;
  - giờ trả về không đổi.
- **Thêm theo nhịp trúng:** xen sao lấp lánh (họa tiết của tướng) và lá hổ phách bật ngược; tia vụn hổ phách toé ngược; bụi khói dưới chân đối thủ. Lúc ngừng nhả, 6 mảnh năng lượng bay theo hướng tia.
- **Mana `n_giac_tia`:** bề dày 0,22 casterH. Cầu xoáy đầu nòng thay `CauLa`, bám đỉnh sừng theo clip từ mốc tụ cũ, tới khung bắn thì đứng ở `mouth`. Hút xoắn và năng lượng từ tim giữ; tầm hút 0,6 casterH.
- **Chiêu cuối `n_giac_tim`:** bề dày 0,28 casterH.
  - Cầu xoáy chỉ hiện ~0,3 s ngay trước lúc bắn, để không che quả tim của rig suốt pha tụ.
  - Giữ: nhịp tim, hút, vòng co, chớp màn, tia vụn gốc, bụi và lá dọc tia, nứt đất, `NoCau` cuối.
- **Màu:** da vàng (vàng, cam mép, lõi kem, sao) gần bảng hổ phách của tướng (#D68620 / #FABE3C / #FFE896), tôi thấy không lệch.
- Biên dịch thử: 0 lỗi. Chưa soi trong Unity.

### Cải tiến chiêu mana ba tướng theo trang so sánh (2026-11-19)
- **gio_loc (Linh Điểu), `n_la_gam`** (`HatChim.cs`). Người dùng: "chim lông bay nhìn hơi chán". Nhịp rig giữ nguyên.
  - Lúc vỗ phóng (`LaBungCanh`): chớp nhỏ, vòng gió, quạt 10 lá và 8 sợi gió bung ở cánh.
  - Vệt bám từng lá cánh của rig (`LaCanhVet`): dựng lại đường bay của 10 lá theo công thức `chim_la_rig.py` (đích tản quanh thân đối thủ, cung `vong`, nhịp `ra` / `vao`), cả lúc đi và lúc về. Dọc đường có lá nhỏ xoáy quanh và sợi gió.
  - Chỗ xuất phát trên cánh là ước lượng, nên vệt có thể lệch lá thật ở đoạn đầu.
  - Thêm 4 lông `long_la` (`FbFly`, `LongLaBay`) tới đúng nhịp găm, găm thì lá vụn bật ngược.
  - Mỗi cú găm: `DanhTrung` 0,5 / 0,3 / 0,3 (sân tự thêm bông trắng + nhún) và một bông `tia_moc_trung` nhỏ xoay theo hướng lá. Chưa có khung thì chớp toé cũ.
- **long_vuot (người cây), `n_gai_va`** (`HatMoc.cs`). Người dùng: "cây quật nhẹ nhàng, ít cây, chưa có impact".
  - `NGaiVa` nhận ra người cây qua bảng màu đang dùng (`ThemeLa("long_vuot")`) và chạy `NQuatGai`. Cầu Gai (cũng mã `n_gai_va`) giữ bản cũ.
  - Bốn cây `quat_dat` so le, lệch nhau 0 / 0,09 / 0,16 / 0,23 s, mỗi cây ngả ra ngoài:
    - cây chính lớp trước, lệch ±0,48 tH, cao 1,36 tH;
    - cây phụ lớp trước bên kia, ±0,64 tH, cao 1,18 tH;
    - hai cây sau lưng, cao 1,55 và 1,1 tH.
  - Cây chính: rung 0,5 + `DanhTrung` 1. Cây sau: rung 0,3 + `DanhTrung` 0,45. Mỗi gốc một cụm bụi đất + 3 đá đất văng.
  - Thêm 2 cụm gai lá; dăm gai, cung đất, vết đất, bụi hai bên giữ.
  - Hàm không biết phía con ra chiêu nên bên của cây chính bốc ngẫu nhiên. Muốn đặt đúng phía thì cần tách mã riêng (vd. `n_quat_gai`) ở `StageView.MocFx` + `HatNuoc.PlayNuoc` / `NuocAtHit`, truyền `casterFeet`.
- **tho_hoang (Voọc Tướng), `n_kiem_rut`** (`HatKiem.cs`). Người dùng: "thêm vệt chém không gian vào".
  - Mỗi nhát chém một khung `chem_kg` (`ChemKg`) đè lên đối thủ: nhát rút 1,5 tH, nhát bổ cuối 1,8 tH.
  - Xoay theo hướng nhát chém: vệt trong khung nghiêng 33°, chọn lật hay không cho góc xoay nhỏ nhất.
  - Khựng: `DanhTrung` 0,6 / 0,8 gọi trước `ChemToe`, để bông trắng của sân lấy cỡ lớn. Rung 0,55 / 0,6.
  - Vệt `VetChem`, tia vụn, lá giữ.
- Biên dịch thử: 0 lỗi. Chưa soi trong Unity.
