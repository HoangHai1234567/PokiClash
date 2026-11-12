# Voi rừng cõng vườn (`voi_rung`): tướng thứ 5 đảo Mộc (suất ải 20, id game `phong_linh`, 2 dạng)

Bắt đầu 2026-11-12. Người dùng đưa ý "voi ma mút hệ cây" (kèm ảnh một con voi ma mút phủ cỏ của game khác làm gợi ý) và giao
Claude **tự làm trọn**: concept, chia mảnh, gen, rig xương, lưới, đỉnh. Lúc đầu ghi nhầm "đảo Thủy", người dùng sửa lại: **đảo Mộc**.

Không có file Spine gốc nào cho con này (game gợi ý là 3D): **xương, lưới, trọng số, clip đều tự dựng** bằng thư viện `quai/`.
Hình là thiết kế của mình, không chép con gợi ý: không đính ảnh của nó vào prompt nào, không lấy các nét riêng của nó (lớp cỏ dài
phủ kín đầu và thân, sừng / ngà đá xám, vòng đá ở cổ chân, thân nâu).

## 0. TRẠNG THÁI 2026-11-12 14:30: người dùng TRẢ concept ("tạm dừng, concept này xấu quá")

Đã dừng hàng gen mảnh (chưa ảnh mảnh nào về), đã bỏ `L1_duyet.png`; `L1.png` giữ làm bản bị trả. Mục 1–2 dưới đây là bản bị
trả, chờ người dùng cho hướng concept mới. Mục 3–4 (bộ cắt, rig, clip trong `voi_rung.py`) mới chạy trên mảnh thử cắt từ sơ đồ;
dùng lại được khi có concept mới (sửa `CFG`).

Nhận định của Claude: bản này ra kiểu hình minh hoạ voi thiếu nhi vì sơ đồ bố cục tự vẽ bằng hình khối cứng (nhìn ngang thuần,
các khối tròn, chi tiết dán lên) và GPT bám sát sơ đồ; mất hẳn khối nặng, dáng gù, lớp phủ rậm của một con ma mút.

## 0b. Concept bản 2 (2026-11-12 chiều): hai hướng, chờ người dùng chọn

Người dùng gửi thêm bốn ảnh con gợi ý và dặn: "bạn cứ vẽ theo con tôi gửi, chuyển thành 2d nhưng sửa đi 1 chút". Claude KHÔNG làm
bản chép sửa nhẹ (nhân vật của game khác) và không đính các ảnh đó vào prompt; giữ những thứ làm nó đẹp (khối to lù lù, lưng gù cao
hơn đầu, góc ba phần tư, lớp áo rậm xếp tầng rủ che trán, mắt nhỏ dữ ló dưới mái, chân cột ngắn, vòi to dài), đổi chi tiết nhận
diện: chất liệu và màu áo, màu da, ngà mọc từ khoé miệng (không sừng đá trên trán), thứ mọc trên u vai (không gai đá), không vòng
đá cổ chân, mắt không đỏ. Không đính sơ đồ hình khối, GPT tự dựng hình theo lời (`build_voi_rung.py`, `HUONG`):
- `duong_xi` → `tai_ve/L2_duong_xi.png`: áo dương xỉ lục sẫm, da đá lam, ngà rễ gỗ màu mật, cụm nấm cam, mắt hổ phách.
- `lieu_hoa` → `tai_ve/L2_lieu_hoa.png`: áo liễu rủ lục vàng điểm hoa hồng, da bạch dương kem, ngà cành gỗ sẫm, bụi hoa, mắt lục lam.
Người dùng duyệt một hướng rồi mới viết lượt 2 (mảnh) và sửa `CFG`, cách chia mảnh trong `voi_rung.py` (dáng ba phần tư: áo là
lớp riêng xếp tầng, không còn tai lá / mũ vỏ cây / cây nhỏ).

## 0c. Người dùng CHỐT hướng `duong_xi`, dặn "lấy con này nhưng bỏ nấm đi" (2026-11-12 14:45)

- Lượt 1b (`gui_gpt/voi_rung_2/luot_1b_bo_nam.txt` → `tai_ve/L3.png`): vẽ lại y hệt, bỏ ba cây nấm (đỉnh u vai khép bằng lá), tầng
  áo dưới cùng tô phẳng lục tươi. Khít bản đã chọn → chép thành **`tai_ve/L1_duyet.png`** (concept đã duyệt).
- Chia mảnh (Claude tự chia; mỗi ảnh gen "đúng chỗ, đúng cỡ" từ concept, `luot_2_<mảnh>.txt`):

| Ảnh | Mảnh | Ghi chú |
|---|---|---|
| `B01` | `ao` | cả khối áo lá của thân (u vai, lưng, sườn, tầng dưới lục tươi); vẽ bù phần bị đầu và ngà che |
| `H01` | `dau` | mái lá + mặt + mắt + **vòi liền mặt** (một ảnh); vẽ bù chỗ ngà gần che |
| `T01` | `nga_g`, `nga_x` | ngà gần (cuộn to, túm rêu ở gốc) và ngà xa vẽ đủ phần bị vòi che |
| `G01` | `chan_1`, `chan_2`, `chan_4`, `duoi` | ba chân vẽ đủ phần bị áo che (lên tới y ≈ 600) + đuôi |

  Dựng bằng mã / dùng lại: `chan_3` (chân nhỏ khuất giữa = ảnh `chan_2` thu 0,62), `bung` (khối da nấp sau tấm áo, lộ ra khi vạt áo
  bay hay thân chồm), `mi` (mí mắt nhắm: phủ lòng mắt bằng màu da + một nét mực).
  Thứ tự vẽ: bụng, đuôi, chân 3, chân 1, chân 2, chân 4, ngà xa, áo, đầu + vòi, mí, ngà gần.
- Rig (`voi_rung.py`, đã chạy thử trên mảnh cắt thô từ concept: 31 xương, ~3400 đỉnh, 7 clip, 175 KB):

```
root → move ─┬─ than ─┬─ hong ── duoi0..2,  ao0_0 → ao0_1 (vạt áo sau)
             │        ├─ ao1_0 → ao1_1 (vạt giữa),  chom (chỏm lá trên u vai)
             │        └─ nguc ─┬─ ao2_0 → ao2_1 (vạt trước)
             │                 └─ dau ─┬─ voi0..8 ── mieng (chóp vòi: chỗ nhả cho VFX)
             │                         └─ mai (túm lá rủ bên phải mặt)
             └─ ban_1..ban_4 (bốn bàn chân bám đất; ống chân tự giãn co giữa thân và bàn chân)
```

  Áo: một lưới; trên mức `ao_y` bám hông / thân / ngực, dưới đó chuyển dần sang ba vạt rủ (mỗi vạt 2 đốt có lò xo) nên áo đung
  đưa như váy lá; chỏm lá có xương riêng. Đầu: đường cắt gốc vòi chia đỉnh (phía chóp bám chuỗi 9 đốt), tam giác vòi vẽ sau.
  Ngà cứng theo đầu. Clip như mục 4 (bỏ tai / cây; thêm áo bay, xù lá).

## 0d. KẾT QUẢ rig dạng 2 (2026-11-12 15:25): chờ người dùng xem

`py -3 -I ArtGen/Spine/voi_rung.py cat` rồi `rig` → `inbox/voi_rung_2/manh/` (`so_ghep.png`, `to_manh.png`), `inbox/voi_rung_2/rig/`
(`xem.html`, `voi_rung_2.atomik` 229 KB, `khung_<clip>.png`, `spine_that/<clip>.jpg` = tờ khung bằng runtime Spine thật, `chan_dung.png`).
31 xương, 11 slot, ~5200 đỉnh, 7 clip; mọi clip nối về idle lệch 0 px; ghép dáng nghỉ so concept: thiếu ~7500 px, thừa ~2700 px
(rìa 1–2 px, tầng lá dưới cùng GPT vẽ bù hơi khác, mép áo gọt sau đầu).

Lỗi tự soi ra và đã sửa (mỗi dòng là một bài học):
- **Vòi ăn vào lá mái**: nửa mặt phẳng "phía chóp vòi" của đường cắt kéo dài lên trên, nuốt cả lá mái bên phải mặt → điểm lá (lục)
  và điểm nằm trên đầu mút đường cắt không tính là vòi; đường cắt đặt DƯỚI túm lá.
- **Gốc vòi nhăn gập** khi bẻ gắt (gốc vòi dày gấp ba bề dài một đốt): mọi dáng vòi uốn DẦN từ gốc ra (`V_NGAM`, `V_HIT`, `V_LEN`).
  Góc đích nhảy qua ±180° làm vòi cuộn ngược: tính độ lệch liền dọc chuỗi.
- **Vòi chọc qua mặt đất** lúc lấy đà húc (duỗi thẳng xuống thì dài hơn dáng nghỉ cong) và lúc gục: lấy đà bằng cuộn vòi lên; gục thì
  vòi duỗi nằm ra trước.
- **Nếp gập trong tấm áo**: hai vạt kề nhau lắc NGƯỢC chiều → tam giác bắc qua khe giữa hai mũi lá gập lại, lòi nền. Các vạt lắc
  cùng chiều, chỉ khác biên độ. Vạt ngoài cùng phải nhận trọn phần mép (trọng số không về 0 ở mép).
- **Mép phải khối áo ló ra sau đầu** (phần GPT vẽ bù rộng hơn chỗ đầu che) khi vòi cuộn / đầu cúi: gọt theo cung elip (`ao_cat`),
  kẻ mực mép gọt; đầu dời đi thì thấy một vai áo tròn.
- **Khe giữa các mũi lá lòi nền** khi đầu ngẩng, thân chồm: khối bụng (vẽ bằng mã, màu da + vân sáp lát từ chân) đủ to nấp sau áo.
- **Mí mắt nhắm còn bóng mắt**: phủ cả lòng mắt lẫn viền dưới (không đè lá), kẻ một nét mực theo mép dưới lòng mắt.

Chưa làm: dạng 1 (voi con) và `evolve`; vào game (suất ải 20 `phong_linh`: chép `.atomik` + chân dung, đổi tên, thẻ, `StageView.MocFx`);
VFX (luồng phun từ `mieng`, sóng đất lúc `dam`); chưa xem trong Unity.

## 0e. Người dùng xem rig (2026-11-12 15:30): "animation còn đơn điệu, các animation đánh thì ổn rồi; idle làm vui nhộn hơn chút, tách thêm lớp lá và rig xương vào để gió đung đưa; appear làm kiểu 1 đống lá rồi đầu tay chân sừng chui từ dưới ra"

Làm lại (rig hiện tại: 51 xương, 15 slot, ~5200 đỉnh, `.atomik` 296 KB, mọi clip nối về idle lệch 0 px; đã soi runtime Spine thật):
- **Lượt 3: tách lớp lá** (`build_voi_rung.py`, `LOP`; ảnh mẫu là ảnh mảnh lượt 2, mỗi lớp đúng chỗ đúng cỡ, vẽ đủ phần khuất):
  `C01` `la_day` (tầng lục tươi dưới cùng, vẽ bù lên tới y ≈ 560), `C02` `la_giua` (các lá sẫm có mũi rủ dưới y ≈ 580, vẽ bù lên tới
  y ≈ 400), `C03` `la_tren` (chỏm + các lá to có chấm kem), `H02` `so` (đầu TRỌC liền vòi, mắt vẽ đủ), `F01` `mai` (mái lá của
  đầu). Cả năm ảnh ra đúng ngay lượt đầu. `B01` (khối áo liền) chỉ còn dùng để dựng `loi`: lõi nền lục sẫm phẳng nấp sau ba lớp
  lá (lá lay hở khe thì thấy màu lá sẫm). Thứ tự vẽ: bụng, đuôi, chân 3, 1, 2, 4, lõi, lá đáy, lá giữa, lá trên, ngà xa, sọ + vòi,
  mí, mái lá, ngà gần.
- **Xương lá**: `la_day` 4 vạt × 2 đốt (`d<i>_0/1`), `la_giua` 4 vạt × 2 đốt (`g<i>_0/1`), `la_tren` 3 cụm lá to mỗi cụm một xương
  ở cuống (`t0..2`) + `chom`, mái lá `mu` + 4 lọn rủ (`m0..3`); tất cả có lò xo. Gió (`gio`): sóng sin chạy từ đuôi lên đầu qua các
  vạt, mỗi lớp trễ một nhịp, cộng một hài bậc hai cho đỡ đều. Các vạt cùng lớp lắc CÙNG chiều (ngược chiều thì gập lưới).
- Xương mới để chui ra / thụt vào: `so` (sọ + vòi, con của `dau`), `nga_g`, `nga_x` (gốc từng ngà).
- **idle 4 s**: nhún nhảy lắc vai – mông nhịp 1 s (hai chân thay nhau nhấc nhẹ) trong 2 s đầu, gió lùa lá suốt, đuôi ve vẩy; 2,2–3,0
  cuộn vòi lên gãi mái lá (các lọn mái nảy theo); 3,1 hắt xì (ngửa lấy hơi, giật xuống, nhắm mắt, lá cả người xù lên; sự kiện `hat_xi`).
- **appear 2,5 s**: đống lá nằm bẹp (thân hạ sát đất, chân thụt vào trong, sọ thu nhỏ nấp dưới mái lá, ngà và đuôi thu về 0), rung
  hai lần (`xao_dong`) → 0,56 đuôi thò ra → 0,72–1,16 đầu chui ra, đội mái lá lên, vòi cuộn rồi duỗi (`chui_ra`) → 1,0 và 1,1 hai ngà
  bật ra → 1,22 hai chân trước đẩy lên, 1,5 hai chân sau, 1,72 đứng dậy dậm (`cham_dat`: sân lắc cam) + rùng mình xù lá, giơ vòi.
- Các clip đánh giữ động tác, thêm lá bay theo (`la`, `xu_la`); die: khuỵu xuống thành đống lá.

## 0f. Đòn đánh thường làm lại + DẠNG 1 (2026-11-12 16:00)

- Người dùng: "đánh thường khi tấn công bạn làm phần chân đạp mạnh lên chứ không move không lên thì nhìn đơn điệu quá" → `attack` 1,2 s:
  chân trước gần cào đất (0,08–0,26), rạp người; chân sau ĐẠP bật (sự kiện `dap` 0,36: bàn chân miết lùi, gót nhấc, rời đất), cả thân
  bay một cung (0,085 H), hai chân trước giơ cao vươn tới; nện xuống đúng `trung` 0,50 cùng cú hất ngà (nén bẹp, lá hất tung), chân sau
  đáp sau một nhịp; nhảy lùi về hai nhịp. Đã soi runtime Spine thật.
- Người dùng: "sau đó làm thêm dạng 1 nữa" (không dặn hình). `build_voi_rung_non.py` → `gui_gpt/voi_rung_1/`, hai hướng ĐỀ XUẤT của
  Claude, chờ người dùng chọn (`inbox/voi_rung_1/xem_concept.html`): `tai_ve/L1_ao_choang.png` (áo choàng lá non ngắn hai tầng, bụng
  và chân trần, mầm xoắn trên đầu), `tai_ve/L1_nam_la.png` (ụ lá non tròn ba tầng như dạng lớn, mầm xoắn trên u vai). Cả hai: chibi
  đầu to, vòi ngắn, ngà mới nhú có túm rêu, lá lục tươi; lá còn bị chuyển màu (sẽ sửa tô phẳng ở lượt gen lại bản được chọn).
- `voi_rung.py` đã chạy nhiều dạng: biến môi trường `VR_DANG` (2 mặc định | 1), `chon(k)`, `CFGS`; `dung(nhe=0.6)` = bản nhẹ của dạng
  2 để gộp; `rig` của dạng 1 gộp dạng 2 (`tienhoa.gop`) và thêm clip `evolve` (voi con co thành ụ lá rung → dạng lớn hiện ra, lá xù
  tung, giơ vòi rống). CHƯA có `CFGS[1]` (chờ concept được duyệt rồi gen mảnh, đọc toạ độ).

## 0g. DẠNG 1 xong (2026-11-12 16:40): người dùng chọn hướng B (`nam_la`)

- Concept: `inbox/voi_rung_1/tai_ve/L1_nam_la.png` → lượt 1b tô phẳng (`luot_1b_to_phang.txt` → `L2.png`: hai tầng trên + mái lá lục
  tươi `#63B04A`, tầng dưới cùng + lá đuôi + mầm lục vàng `#A6D34F`) → `L1_duyet.png`.
- Mảnh và lớp lá: cùng cách chia như dạng 2 (`build_voi_rung_non.py`: `PARTS`, `LOP`; 9 ảnh B01, H01, G01, T01, C01–C03, H02, F01, đều
  ra đúng lượt đầu). Mầm xoắn nằm trong `la_tren`, bám xương `chom` (lắc có lò xo).
- Rig: `VR_DANG=1 py -3 -I ArtGen/Spine/voi_rung.py cat | rig` (bảng số `CFG1`). Cùng bộ clip với dạng 2; `rig` gộp bản nhẹ của dạng 2
  (ảnh 0,6 lần) và thêm `evolve` 2,8 s (voi con rạp xuống co thành ụ lá rung → tan; dạng lớn hiện ra, lá xù tung, giơ vòi rống, hoà về
  khung 0 idle dạng 2; lệch cuối 0 px). `inbox/voi_rung_1/rig/`: 101 xương, 30 slot, ~6500 đỉnh, 8 clip, `.atomik` 367 KB (trần 0,5).
  Chiều cao cho game tính tới đỉnh ụ lá (`y_cao`), không tính mầm xoắn (không thì thân bị thu nhỏ).
- Bài học thêm: mép gọt lớp lá sau đầu (`ao_cat`) của dạng 1 phải chừa phần lá ló trên đỉnh đầu (`ao_cat_y`); mí mắt nhắm lấy bao lồi
  của phần hổ phách (mắt to: phép đóng hình thái không lấp được con ngươi) và màu da ngay quanh mắt.
- Cả hai dạng đã soi bằng runtime Spine thật (`rig/spine_that/<clip>.jpg`) và ảnh cận. CHƯA: vào game (suất ải 20 `phong_linh`), tên,
  thẻ, VFX; chưa xem trong Unity.

## 0h. Người dùng xem cả hai dạng (2026-11-12 ~16:45): "ổn rồi"

Rig và clip của dạng 1, dạng 2 coi như được duyệt. Việc tiếp (chờ người dùng trả lời có vào game ngay không, và tên): vào game ở suất
ải 20 `phong_linh` (giữ id, chỉ số, thẻ, golden; thay rig + chân dung; `StageView.MocFx`), tên tướng / dạng / thẻ, VFX.

## 0i. VÀO GAME (2026-11-12 ~16:20; người dùng: "Vào game ngay", "Dùng tên tôi đề xuất")

Thay tướng cũ ở **suất 5 đảo Mộc = ải 20, id `phong_linh`** (giữ id, chỉ số, hiệu ứng thẻ, golden, C#):
- Tên (`ArtGen/Spine/quai/doi_ten_lam_tuong.py`, sửa `heroes.json`, `cards.json`; HeroDb / CardDb do menu "Nhập dữ liệu" dựng lại):
  tướng **Lâm Tượng**, danh hiệu "Ma mút cõng rừng", dòng "Dòng Lâm Tượng"; dạng 1 **Tượng Mầm**, dạng 2 **Lâm Tượng**; thẻ mana
  **Vòi Phun** (leaf), chiêu cuối **Dậm Rừng** (crack), bị động **Áo Lá Dày** (shield).
- Rig: chép tay `inbox/voi_rung_<k>/rig/voi_rung_<k>.atomik` → `Assets/03 Art/Heroes/Resources/phong_linh_<k>/phong_linh_<k>.atomik`
  và `chan_dung.png` → `phong_linh_<k>_portrait.png` (bản cũ còn trong git); `quai/da_nhan.json` thêm dòng `phong_linh`.
- Unity (cầu MCP `127.0.0.1:8080/mcp`): refresh (0 lỗi), "PokiClash/Nhập dữ liệu" (88 tướng, 265 thẻ riêng), "Gắn dạng .atomik vào
  prefab tướng" (`phong_linh_1`: 101 xương, 8 clip; `phong_linh_2`: 51 xương, 7 clip; prefab giữ 2 dạng), "Chụp thử dạng .atomik"
  (`Library/PokiHeroShots/phong_linh_atomik_1.png`, `_2.png`: hình đúng ở mọi clip, kể cả evolve), EditMode 103 test: chỉ hỏng
  `PrefabOnlyTests.MaRuntime_KhongSinhDoVat` (có từ trước, không liên quan).
- CHƯA: xem trong trận (Play); `StageView.MocFx` chưa có dòng `phong_linh` nên chiêu mana / chiêu cuối đang dùng hiệu ứng mặc định
  (VFX riêng: luồng phun từ `mieng`, sóng đất lúc `dam`, bụi lúc `dap`); `GD_Claude/13_DanhSachTuong.md` chưa ghi.

## 0k. VFX trong game (2026-11-12 ~17:10; người dùng: "làm vfx đi")

File mới `Assets/01 Script/Game/Battle/HatVoi.cs` (phần `partial` của `HatLua`), đi chung đường bộ Thủy / Mộc (`HatNuoc.PlayNuoc`, mã
`n_*`, phát từ ĐẦU clip kèm `lead` = giờ trúng của clip). Nối: `HatNuoc.cs` thêm 3 `case` + dòng `WThemes["phong_linh"]` (lục sẫm,
lục tươi, lục vàng; sao màu mật), `StageView.MocFx["phong_linh"] = ("n_voi_phun", { "n_dam_rung1", "n_dam_rung" })`, menu thử
`PokiClash/Thử/Đảo Mộc: vòi phun và dậm rừng Lâm Tượng… (đang Play)` (`Editor/MocFxTour.cs`, ảnh `Temp/PokiShots/thuy_fx/`).
Không cần ảnh hạt mới: hạt cây = ảnh giọt (`hat_drop_*`) nhuộm màu mật hai lớp; bụi = ảnh bọt nhuộm be; rễ = ảnh gai (`Spike`) nhuộm
nâu gỗ; lá = `Leaf` của `HatMoc.cs`.
- **`n_voi_phun` (chiêu mana Vòi Phun, `NVoiPhun`)**: hít (0,44 s trước khung nhả: lá và bụi phấn bị hút về chóp vòi) → nhả ở `lead`
  (0,62): luồng HẠT CÂY hẹp, nhanh (48 hạt/giây, tốc 980) + lá cuốn quanh luồng (54 lá/giây, lượn và lật), hai nhịp phụt mạnh (0 và
  0,44 s: thẻ đánh 2 lần) có chớp và bụi ở chóp vòi; hạt chạm thì vỡ bật ngược, lá rách; hết luồng (0,9 s) nổ chùm lá + hạt. Không
  khai `HoldNuoc`: clip `cast` tự giữ dáng ngắm tới 1,56 s.
- **`n_dam_rung` (chiêu cuối Dậm Rừng, `NDamRung`)**: chồm (`lead` − 0,87): vòng dưới chân, lá quanh người cuốn xoáy bay lên, bụi
  chân sau → DẬM ở `lead` (1,42): rung 1, chớp màn, vòng bụi, 14 cụm bụi, đất vụn, 22 lá trên lưng bung ra → sóng đất: 4 cột lá phụt
  lên dọc đường cách nhau 0,07 s → tới chân đối thủ (`lead` + 0,35): nổ lá, vòng, 5 rễ trồi (ba cao sau lưng, hai thấp phía trước),
  bụi, rồi cột lá phun 0,5 s (phần lớn ở `BACK`). `n_dam_rung1` (dạng 1): độ mạnh 0,7, ba cột, không có rễ.
- Đã soi ảnh chụp trong trận (Play từ Boot, tour) cho mana dạng 2 và chiêu cuối cả hai dạng: đủ pha tụ → phát → bay → trúng → tan,
  hiệu ứng ra đúng chóp vòi / chân trước, không lỗi console. Bản đầu luồng hạt và lá gồng còn thưa → tăng mật độ (số ở trên).
- CHƯA: chưa thử Android. (Hiệu ứng đòn đánh thường: xem mục 0l.)

## 0l. Hiệu ứng đòn đánh thường (2026-11-12 ~18:00; người dùng: "bạn làm thêm hiệu ứng đánh thường cũng được")

Mã `n_hat_nga` (`NHatNga` trong `HatVoi.cs`), dùng cho cả hai dạng. Nối: `StageView.MocAtk["phong_linh"]`, `FireAtk` nhận thêm tướng
Mộc, `AtkFx` phát cả khi tướng LAO tới nếu `HatLua.AtkLao(kind)` (trước chỉ phát cho tướng đứng bắn, rig khai `stay`);
`HatNuoc.PlayNuoc` thêm `case "n_hat_nga"`. Ô xem tướng (`HeroViewer`) vẫn đòi `Stays` nên không có hiệu ứng này.
- Nhịp theo clip `attack` (`lead` = giờ trúng 0,50): cào đất `lead` − 0,42…0,30 (bụi nhỏ dưới chân trước) → chân sau đạp `lead` −
  0,14 (rung 0,25, vòng bụi, 9 cụm bụi và 4 đất vụn bắn ra sau) → đang bay: lá trên lưng tuột lại phía sau (60 lá/giây) → nện + hất
  ngà ở `lead` (rung 0,35): vòng bụi dưới thân, bụi và đất vụn ở chân trước, chớp toé ở mũi ngà, 10 lá bật khỏi đối thủ theo hướng hất.
- Sân kéo đỉnh cú lao tới **72 % quãng** tới đối thủ (`AolaSticker.Lunge`): chỗ đáp tính theo số đó. Bản đầu đặt 50 % → vòng bụi nằm
  trơ giữa sân.
- Lúc trúng con đánh ĐÈ lên đối thủ (vẽ trên): bụi đặt ở chỗ chạm sẽ dính lên mặt nó → chỗ chạm chỉ có chớp toé + lá, đặt lệch về
  phía mũi ngà (`foeBody + (dir × 0,15, −0,1) × tH`).
- Tour `ThuyFxTour` chụp thêm `<tướng>_<dạng>_atk_NN.jpg` cho tướng có `FireAtk`. Đã soi cả hai dạng (3 vòng), console không lỗi.

## 1. Thiết kế (của Claude, BỊ TRẢ)

Voi ma mút lùn mập nhìn sang phải, một mắt hổ phách, mày xếch. Điểm riêng:
- da **xám lam** `#8C9CA8` (không nâu);
- hai **tai là hai chiếc lá** lục sẫm `#3F8A45` (tai gần to, che gáy và chỗ nối đầu – thân; tai xa ló sau đầu);
- **mũ vỏ cây** `#7A5638` ôm đỉnh đầu, mép dưới răng cưa;
- hai **ngà kem** `#F2E6C0` cong lên, gốc có **đai vỏ cây**;
- lưng phủ **tấm rêu** `#6FAE4B` mép lượn sóng (không phải cỏ dài, lông rủ), ba hoa vàng `#F4C23C` nhuỵ cam;
- **một cây nhỏ** tán tròn ba quả vàng mọc trên u vai;
- bốn chân cột, mỗi chân ba móng kem; đuôi mảnh chùm ba lá.

Dáng nghỉ dễ rig: bốn chân thẳng tách nhau, vòi buông tự do trước mặt (chóp cong ra trước, không chạm đất), đuôi buông sau.

File: `ArtGen/Spine/voi_rung_bo_cuc.py` (sơ đồ bố cục phẳng tự vẽ, đính cho GPT) → `inbox/voi_rung_2/mau/bo_cuc.png`;
`build_voi_rung.py` → `gui_gpt/voi_rung_2/` (`luot_1_concept.txt`, `luot_2_<mảnh>.txt`, `HUONG_DAN.md`).
Concept: `inbox/voi_rung_2/tai_ve/L1.png` (lượt đầu đã bám sơ đồ, đúng nét, tô phẳng) → Claude tự chép thành `L1_duyet.png`.
Ảnh mẫu nét: xương rồng tròn, tinh linh rừng dạng 3, bản đồ (tượng đá lúc đó đang bị phiên khác gen lại nên không dùng).

## 2. Chia mảnh (tự chia; mỗi ảnh gen "đúng chỗ, đúng cỡ" như concept: `redraw image 1 with ONLY ...`)

| Ảnh | Mảnh | Ghi chú |
|---|---|---|
| `B01` | `than` | thân + tấm rêu + hoa; vẽ bù ngực / vai sau đầu, sườn sau hai chân gần |
| `H01` | `dau` | **đầu liền vòi** một ảnh (cùng màu, nối liền: không gen rời), có mũ vỏ cây, mắt; vẽ bù chỗ ngà và tai che |
| `G01` | `chan_gs`, `chan_gt` | hai chân gần, mỗi chân một hình kín có chỏm tròn |
| `F01` | `chan_xs`, `chan_xt`, `duoi` | hai chân xa vẽ đủ phần khuất + đuôi |
| `E01` | `tai_g`, `nga_g`, `cay` | tai lá gần, ngà gần (đai vỏ kéo dài vào má), cây (thân kéo dài xuống dưới rêu) |

Tai xa và ngà xa **dùng lại ảnh** tai gần / ngà gần (thu nhỏ, đặt sau đầu). Mí mắt nhắm vẽ bằng mã (tô phẳng màu da + một nét mực).
Thứ tự vẽ (sau → trước): tai xa, ngà xa, chân xa sau, chân xa trước, đuôi, cây, thân, chân gần sau, chân gần trước, đầu + vòi, mí,
ngà gần, tai gần.

## 3. Rig (`ArtGen/Spine/voi_rung.py`: `cat`, `rig`, `soi`)

Đơn vị rig = 0,5 px concept; gốc ở giữa bốn chân trên mặt đất; nhìn sang phải.

```
root → move ─┬─ than ─┬─ hong ── duoi0..3
             │        └─ nguc ─┬─ cay0..2
             │                 └─ dau ─┬─ voi0..8 ── mieng (chóp vòi: chỗ nhả cho VFX)
             │                         ├─ tai_g0..2
             │                         └─ tai_x
             └─ ban_gt, ban_gs, ban_xt, ban_xs   (bốn bàn chân: bám đất)
```

- **Thân**: lưới vùng đều, ba vùng `hong` / `than` / `nguc` hoà rộng (thở, chồm).
- **Đầu liền vòi**: một lưới. Đường cắt gốc vòi (`CFG["voi_cat"]`: trán trước → chỗ mép sau vòi gặp cằm) chia đỉnh: phía chóp vòi
  bám chuỗi 9 đốt (B-spline theo vị trí chiếu lên trục vòi, gốc hoà vào `dau`), phía kia bám `dau`. Tam giác vòi xếp vẽ sau tam
  giác mặt (vòi cuộn lên thì đè lên mặt). Bài học: khoanh vòi bằng "ống quanh trục" bỏ sót một mép vòi (mép đó bám đầu, vòi giơ lên
  là bẹp thành vệt); dùng nửa mặt phẳng theo đường cắt thì hết.
- **Chân không có khớp gối**: nửa trên bám `hong` / `nguc`, nửa dưới bám xương bàn chân (con của `move`), giữa hoà: ống chân tự
  giãn co khi thân nhún; chồm lên thì bàn chân trước đi theo ngực (`theo`).
- **Ngà**: cứng theo `dau`. **Tai gần**: chuỗi 3 đốt + lò xo. **Cây**: chuỗi 3 đốt + lò xo. **Đuôi**: chuỗi 4 đốt + lò xo.
  **Vòi**: dáng đặt bằng góc thế giới từng đốt (`voi_toi`: ngắm, hít, giơ cao, cụp) + lò xo nhẹ.

## 4. Clip (đề xuất của Claude; người dùng chưa dặn chiêu)

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| appear | 1,5 s | rơi từ trên xuống, nện đất nén bẹp, giơ vòi rống nhẹ | cham_dat 0,30 |
| idle | 3,0 s lặp | thở, đầu gật chậm, vòi đung đưa, một cú phẩy tai, đuôi ve vẩy, cây lắc, chớp mắt | |
| attack | 1,1 s | lùi rạp cụp vòi → lao tới hất ngà lên (đòn lao của dòng voi) | trung 0,46 |
| cast | 2,0 s | hít hơi cuộn vòi lên → duỗi vòi ngắm thẳng → phun từ chóp vòi, giữ tới hết luồng (đứng tại chỗ) | tu 0,20; phun 0,62; het_phun 1,56 |
| skill | 2,6 s | chồm hai chân trước, giơ vòi rống → dậm mạnh hai chân xuống (đứng tại chỗ; sóng đất / rễ trồi là VFX riêng) | gam 0,55; dam 1,42 |
| hit | 0,6 s | bật ngửa đầu, tai xoè, nhắm mắt | |
| die | 1,7 s | giật ngửa, khuỵu xuống, tan | |

VFX không nằm trong rig (luồng phun từ `mieng`, sóng đất lúc `dam`).
