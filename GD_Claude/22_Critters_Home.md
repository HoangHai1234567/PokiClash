# Home của Clash of Critters: mổ map, lớp, nước, ánh sáng, và cách áp vào Nhà

Viết 2026-11-20. Nguồn: bản đục 0.50.1 ở `D:\CrittersRipper` (chỉ xem trên máy, không đưa hình của họ vào game, không gửi cho GPT hay Magnific). Phần tính năng (công trình, câu cá, công nghệ, bong bóng, trang trí, đường, mở đất, chế độ xây) đã ghi ở `21_Nha_Home.md`; file này bổ sung phần map và kỹ thuật.

Người dùng chốt 2026-11-20: **làm theo hướng A** (đổi môi trường Nhà theo bộ mảnh ghép kiểu Critters, giữ lưới 72 × 72, luật, công trình, bến tàu), **bỏ quầng sáng** ở ngày đêm, **lấy cách xếp lớp theo render queue** của họ.

## Công cụ, ảnh soi

| Cái gì | Ở đâu |
|---|---|
| Script đọc prefab, giải lưới, ghép toàn cảnh, đọc vật liệu, bóc GLSL | `D:\CrittersRipper\tools\homestead\` (`guidmap.py` dựng bảng GUID; `dump_prefab.py` in cây lớp; `render_map.py` ghép ảnh; `shader_glsl.py` bóc GLSL) |
| Ảnh toàn cảnh, tờ ảnh nước, tờ ô đất khoá, cây lớp, mã GLSL | `D:\CrittersRipper\shots\homestead\` (`map_full.png`, `sea_sheet.jpg`, `region_sheet.jpg`, `root_tree.txt`, `glsl/`) |

- Shader trong bản xuất AssetRipper là vỏ rỗng, nhưng GLSL thật đọc được bằng UnityPy: đặt `FALLBACK_UNITY_VERSION = "2022.3.62f3"`, giải LZ4 `compressedBlob`, tìm chuỗi `#version`. Shader map nằm ở `bundles/1446.bundle`.
- Không đọc được: bảng số (lưới thật, chỗ đặt nhà lúc đầu, giá mở đất, mức zoom), shader trời `Sprites/ParallaxSky`, shader cỏ rải `HomesteadGroundItem` (không thấy trong bundle nào). Trên mạng không có tài liệu.

## 1. Kiểu map

Cả map là một prefab tĩnh `Res/Homestead/Prefab/pbsc_homestead_root_new.prefab`: 346 vật, khoảng 300 lưới cắt sát viền ảnh (đỡ vẽ chồng), không có script.

- **Cao nguyên cỏ ở giữa**: thoi 2:1 bị cắt thẳng hai mũi trái, phải thành lục giác. Mặt cỏ là một đa giác 16 đỉnh tô **một màu** (0,59; 0,70; 0,27), không ảnh.
- **Ba phía trên, trái, phải**: bậc cao hơn, vách đất đỏ nâu, trên vách là rừng (thông, cây tán tròn), đồi, núi. Thác nước 4 khung đổ xuống ao trên vách. Đồ lặt vặt: bảng hiệu, khúc gỗ, lửa trại.
- **Phía nam**: cao nguyên hạ xuống bằng vách thấp, dưới là bãi cát có dừa, đá, sao biển, thuyền phao; rồi biển, có hai đảo nhỏ ngoài khơi. Biển chỉ có ở phía này.
- **Trên cùng**: trời parallax (dải màu trời, đồi xa, đồi gần, mây trôi lệch theo camera, sao ban đêm).
- Hạt gió thổi ngang map (`pbvx_camp_wind`, hai lớp); hạt tuyết theo mùa có sẵn nhưng tắt.

## 2. Chia lớp theo render queue

Môi trường không dùng sorting layer: mọi thứ ở lớp Default, thứ tự vẽ là **render queue của vật liệu**. Công trình, ô đất khoá, trang trí, thác nước ở sorting layer riêng `BuildLayer`, luôn vẽ trên môi trường.

| Queue | Lớp | Nội dung |
|---|---|---|
| 2501 | nền cỏ, biển | đa giác màu phẳng; biển là một tấm 75 × 19 đơn vị |
| 2502 | bãi cát | 6 mảng cát lớn |
| 2504 | trời | một tấm 78 × 26 đơn vị |
| 2506 | cỏ rải | 30 khối 18 × 18 ô; mỗi khối 49 thoi 6 × 6 ô chồng nửa nhau, cùng in một mảng cụm cỏ và hoa vàng (lặp mà không thấy đường nối) |
| 2990 | vách đất | 11 mảnh |
| 2992 | môi cỏ | 49 miếng phủ mép vách |
| 2994–2997 | đồi, núi, đá | atlas 2048 |
| 2998 | cây | 157 cây từ 5 hình (lật, phóng) trong atlas 1024 |
| BuildLayer | công trình | công trình, ô đất khoá, trang trí, thác nước, thú |

Điểm hay: cây nền, vách, đồi không cần xếp theo chiều sâu mỗi khung (đã cố định bằng queue); chỉ lớp công trình mới xếp.

## 3. Kích thước, lưới, camera

- Lưới thoi 2:1: một ô rộng 1 đơn vị, cao 0,5; ảnh 100 px mỗi đơn vị, tức ô 100 × 50 px (mình 96 × 48).
- Cao nguyên 69,7 × 52,4 đơn vị (khoảng 7.000 × 5.200 px); cả map kể cả trời, biển khoảng 96 × 93 đơn vị. Diện tích ước 9.800 ô, gần gấp đôi 72 × 72 của mình (bề ngang gần bằng nhau, họ cao hơn vì không cắt mũi trên dưới).
- Công trình: gốc ở mũi dưới chân thoi; ảnh rộng đúng N đơn vị, đặt cao hơn gốc N/4 (2×2: 0,5; 4×4: 1; 6×6: 1,5; 8×8: 2).
- Ô đất khoá là một món trang trí 8 × 8 ô (ảnh 798 × 628 px): 4 kiểu mở được (thông; cây tán tròn; đá rêu lẫn thông; lẫn lộn), 1 kiểu "chưa mở được" (gốc cây cụt, đá). Dọn rừng là gỡ món đó.
- Lưới khi xây (`IsometricGridRenderer`): lan ra từ ô giữa 100 ô/giây khi hiện; hai kiểu nét: trắng liền độ trong 0,59 dày 0,02; gạch ngắn đầu tròn xanh nõn (0,86; 0,99; 0,56) viền xanh lá, dày 0,03. Chân công trình phủ xanh hoặc đỏ, độ trong 0,5.
- Camera: Cinemachine, nhìn thẳng, không xoay; cỡ mặc định 4,5; bám mục tiêu, trễ 0,25, vùng mềm 0,8; giới hạn trong khung `camera_focus_rect`; rung màn 0,2 giây, tắt dần 0,7 giây.

## 4. Shader biển (`UEP/Interface/2DWater`, biến thể có mép và ảnh phụ)

Ảnh vào:
- mặt nạ bờ 1024 × 256: R dải mờ rộng, G dải vừa, B dải sắc sát bờ (trắng phía đất);
- ảnh phụ 512 × 512, lặp 3 × 2: R tô sẫm vùng nước sâu, G mạng vân sáng dưới nước;
- nhiễu dòng chảy 128 × 128, RG.

```
n    = nhiễu(uv xoay 0,61 rad, lặp 2, trôi _Time.x × (1, 4)) - 0,5      // _Time.x = giây / 20
bot  = mặt_nạ.B (uv + nhiễu_khác × 0,01)                                 // vạch bọt sát bờ
R, G = mặt_nạ.RG (uv + n × 0,055)
màu  = trộn(sâu, sóng, R)
màu  = trộn(màu, mép, giữ_0_1(G − bot))                                   // dải sáng ven bờ
màu  = trộn(màu, sâu_tối, ảnh_phụ.R)
màu += ảnh_phụ.G(uv × (3,2) + n.x × 0,3) × màu_vân × (1 − giữ_0_1(R² − bot − mép))
ra   = trộn(màu, bọt, bot)
```

Màu: sâu (0,10; 0,46; 0,63), sóng (0,16; 0,75; 0,85), mép (0,27; 0,77; 0,85), bọt (0,61; 1; 0,86), sâu tối (0,11; 0,32; 0,55), vân (0,04; 0,05; 0,06, cộng thêm).

## 5. Ánh sáng ngày đêm

Mọi sprite dùng `Sprites/PCustomSprite`, từ khoá chung `DAYNIGHTCYCLE`:

```
sáng = màu_môi_trường + bộ_đệm_sáng.rgb × che_khuất(độ sâu)   // che_khuất = 1 với nền (_DayNightGround)
ra   = ảnh × màu × sáng
ra   = trộn(ra, ảnh × màu_tự_sáng, mặt_nạ_tự_sáng × mức_đêm)   // _EmissiveTex của từng công trình
```

- Màu môi trường đặt chung: ngày gần trắng, đêm xanh sẫm.
- Bộ đệm sáng: tấm ảnh màn hình; mỗi đèn là quầng mềm (`DayNightHaloAnchor`, shader `DayNightHalo` vẽ vào bộ đệm hai đầu ra: màu, độ sâu và độ mạnh). **Mình bỏ phần này** (người dùng chê quầng sáng 2026-11-20).
- Mặt nạ tự sáng: ảnh riêng từng công trình (`*_night_mask.png`: cửa sổ, màn hình, cây xăng).
- Trời có màu sao ban đêm.

## 6. Áp vào Nhà (hướng A)

### Giữ nguyên

Lưới 72 × 72, ô rừng 12 × 12, vòng mở đất, luật và số liệu (`balance.json` khối `home`), công trình và ảnh công trình, ô lát, bến tàu và tàu, mây rìa, cây rời trên ô rừng chưa mở (người dùng chọn 2026-11-18 thay cho khối rừng lặp), chỗ đặt Nhà chính (39, 39) giữa khoảnh 3 × 3 mở sẵn (chỗ đặt nhà của Critters không đọc được).

### Lớp của Nhà theo queue

Màn Nhà là uGUI: trong một Canvas, thứ tự anh em chính là thứ tự vẽ. Bảng queue dưới đây là nguồn duy nhất: bộ dựng prefab tạo các nút lớp theo đúng thứ tự số, code chạy chỉ đặt vật vào đúng nút, không tự đổi thứ tự lớp.

| Queue | Nút | Nội dung |
|---|---|---|
| 100 | `nen` | ảnh nền (đồng cỏ, hồ, suối, mạch quặng, bậc cao) + biển do shader `UIHomeSea` |
| 200 | `cat` | bãi cát, đá, sao biển, thuyền (mảnh rời) |
| 300 | `co_rai` | cụm cỏ, hoa rải lặp |
| 400 | `o_lat` | ô lát |
| 500 | `luoi` | lưới sáng khi xây |
| 600 | `vach` | vách cao nguyên: bậc thấp xuống bãi cát, bậc cao lên rừng |
| 650 | `moi_co` | môi cỏ phủ mép vách |
| 700 | `rung_nen` | cây rìa trên bậc cao (không xếp theo chiều sâu) |
| 800 | `vat` | công trình, cây ô rừng chưa mở, quái (xếp theo chân mỗi lần đổi) |
| 850 | `hat` | hạt quái, gió |
| 900 | `may` | mây rìa |
| 950 | `ben_tau` | tàu ở bến (`ShipBuild.Pier`) |
| 1000 | `sang_toi` | nhuộm theo giờ, tia nắng |
| 1100 | `tu_sang` | mặt nạ tự sáng của công trình (đêm) |

- Cây rìa chuyển từ lớp `vat` sang `rung_nen`: bớt hàng trăm vật phải xếp mỗi lần, giống queue 2998 của họ.
- Tự sáng nằm trên lớp nhuộm: nhuộm làm tối cả cảnh như màu môi trường của họ, mặt nạ vẽ màu đèn phẳng lên trên nên cửa sổ không tối, cùng kết quả với phép trộn tự sáng của họ. Không có quầng.

### Việc

| Mốc | Việc | Cần hình mới |
|---|---|---|
| A1 | Biển: shader `UIHomeSea` theo công thức mục 4, mặt nạ 3 dải sinh từ ảnh nền (`ArtGen/Home/sea/make_home_sea.py`), nhiễu và vân tự sinh (không dùng ảnh của họ), giữ nét chì của biển vẽ tay làm vân giấy | không |
| A2 | Bảng queue trong bộ dựng prefab, dời cây rìa sang `rung_nen` | không |
| A3 | Ngày đêm: bỏ quầng đèn công trình (`HomeScene.NightLights`), thay mặt nạ tự sáng từng công trình | mặt nạ sinh từ ảnh công trình |
| A4 | Lưới xây lan ra từ chỗ chạm như họ; hạt gió | không |
| A5 | Bộ mảnh môi trường: vách bậc thấp phía nam (có bậc thang xuống bến ở mũi dưới), bậc cao có rừng phía bắc, bãi cát và đồ ven biển, cụm cỏ rải, thác nước 4 khung | 3–4 ảnh Magnific (dưới 100 credit mỗi ảnh), nét vẽ tay của game, tô phẳng, không bóng |

### Giả định Claude tự đặt (người dùng đổi được)

1. **Không làm trời parallax**: Nhà có mây rìa che kín bốn phía, trời của họ sẽ bị che; để dành nếu sau này bỏ mây phía bắc.
2. **Biển mềm như họ nhưng giữ vân chì**: màu biển do shader, nhân với độ sáng tối của biển vẽ tay (`_Grain`), nên vẫn thấy nét chì. Có số `_Steps` để chia bậc phẳng nếu người dùng muốn giống nét vẽ tay hơn.
3. **Chưa thay ảnh nền ở A1–A4**: đồng cỏ, hồ, suối, mạch quặng, bậc cao vẫn là ảnh vẽ liền hiện tại; A5 mới đặt mảnh vách, cát, cỏ rải lên trên và vẽ lại phần rìa.

## Tiến độ

- 2026-11-20: mổ xong, viết file này, chép script và ảnh soi.
- 2026-11-20: **A1–A4 xong, đã chạy trong Unity** (biên dịch sạch, menu "Nhà: dựng màn" không cảnh báo, tour chụp `Temp/PokiShots/home_*.png`):
  - **A1 biển**: shader `Assets/03 Art/Shaders/UIHomeSea.shader`, vật liệu `Assets/03 Art/Home/home_sea.mat`; ảnh `Assets/03 Art/Baked/Home/home_sea.png` (mặt nạ 3 dải + vùng biển, nửa cỡ ảnh nền), `home_sea_flow.png` (nhiễu lặp 128), `home_sea_caustic.png` (vân Voronoi lặp 512), sinh bằng `ArtGen/Home/sea/make_home_sea.py` (OpenCV, máy này không có scipy; `--preview` ghép thử ra `ArtGen/Home/sea/preview_sea.png`). Màu xa bờ trùng màu biển ngoài ảnh `#4fa7e3` nên không thấy mép. Bọt và dải mép cắt sắc (`_Crisp` 1), dải màu mềm (`_Steps` 0); chuyển `_Steps` 3 là chia bậc phẳng. Đêm tối dần ra xa bờ như sóng mực cũ. `home_water.mat` (UIInkWater) để nguyên, thiếu ảnh biển thì bộ dựng tự quay về nó.
  - **A2 lớp theo queue**: bảng `HomeScene.Layers`, bộ dựng xếp nút con của `the_gioi` theo bảng (`HomeSceneMenu.OrderLayers`, nút lạ thì báo). Đã có các nút rỗng `cat`, `co_rai`, `vach`, `moi_co` chờ A5; cây rìa sang `rung_nen`, xếp một lần lúc dựng, không còn trong phép xếp mỗi 0,12 giây của lớp vật. Nút đèn đổi tên `den` → `tu_sang`.
  - **A3 đèn đêm**: bỏ quầng `anim_glow`; mặt nạ `Assets/03 Art/Home/home_e_<def>.png` (main, storage, waterwheel: kính cửa sổ đổi màu đèn ấm; kitchen, forge: lửa, than; mine: pha lê, đèn lồng), sinh bằng `ArtGen/Home/night/home_emit.py` (`--xem` ghi tờ soi `soi_emit.png`). Vẽ ở lớp `tu_sang` bằng vật liệu `home_emit.mat` (shader `UIIslandEmit` của đèn đêm sảnh, sáng thêm 0,45, chập chờn 0,3), khung trùng ảnh công trình, công trình đang dời thì đèn ẩn theo.
  - **A4**: lưới chế độ xây lan ra từ ô giữa khung nhìn 36 ô/giây, mép vòng có vệt nét sáng (`UIHomeGrid._Spread`, `HomeScene.StartSpread`). Lá, cánh hoa bay theo gió: 120 ảnh dựng sẵn trong prefab ở `hat/gio`, `App/Scenes/Home/HomeWind.cs` dời (trôi, lắc, lật, vòng lại ở mép), ảnh `home_leaf_1..4.png` vẽ bằng `ArtGen/Home/wind/make_leaves.py`.
  - Tour thêm ảnh `2a_luoi_lan`, `14_dem_nha` (21 giờ), `15_dem_bien`.
- Thấy khi soi, chưa sửa: ở Nhà, đêm chỉ tối nhẹ (ảnh 21 giờ chụp trước khi sửa cũng vậy), nên cửa sổ sáng chưa nổi. Độ tối do `DayNight` dùng chung, phiên đèn đêm sảnh đang sửa file đó.
- 2026-11-20: **A5 xong** (người dùng cho tiêu credit và duyệt hai giả định: không trời parallax, giữ ảnh nền vẽ liền). Hai ảnh Magnific GPT 2.6 3:2 1k high, 95 credit mỗi ảnh (190 credit):
  - khung mẫu `ArtGen/Home/kit/make_kit_refs.py` (`refs/frame_vach.png`, `frame_bien.png`, `hill_style.png` cắt khối đồi trên nền, `beach_style.png`); prompt `ArtGen/Home/kit/kit_vach.txt`, `kit_bien.txt`; ảnh ra `kit_vach_1.png`, `kit_bien_1.png` (nền trong suốt sẵn);
  - `ArtGen/Home/kit/import_kit.py`: cắt mảnh, bỏ quầng alpha thấp, đo lại chân vách và mép cắt trên ảnh (GPT lệch khung vài chục px), xoá 7 px ở đầu hở (GPT viền mực cả mép cắt, để lại thành nét dọc ở mỗi mối nối), nhuộm mặt vách theo màu vách khối đồi vẽ sẵn; tính chỗ đặt vào `Assets/03 Art/Home/home_kit.json`; ảnh `home_k_vach_1..4.png`, `home_k_bien_1..6.png`; soi `kit/preview_kit.png`;
  - vách cao 200 px, chạy ở các ô rừng không phải đồi dọc hai cạnh trên (cạnh trên phải ô 24–60, cạnh trên trái ô 24 tới mũi trái, bản lật ngang), hai đầu nối thẳng vào khối đồi; mũi trái dùng mảnh đầu vách đổ xuống đá. 12 mảnh trong lớp `vach`;
  - cây rìa nâng lên 200 px đứng trên bậc cao (`HomeScene.terraceH`, bộ dựng truyền qua `SetupEnv`);
  - 37 món đồ ven biển (đá, sỏi, sao biển và vỏ sò, thuyền con, khúc gỗ trôi, cỏ bãi biển) rải trên dải cát hai cạnh dưới, chỉ chỗ ảnh nền là cát, tránh bến và cửa suối; lớp `cat`;
  - thác, suối chảy bằng shader thay thác 4 khung của Critters: `home_river.png` (vùng nước trong đảo, hướng chảy, tốc; lòng hồ đứng) sinh cùng `make_home_sea.py`, `UIHomeSea` vẽ vệt bọt trôi theo hướng.
  - Tour thêm ảnh `16_vach`, `17_thac_a`, `17_thac_b` (mở hết ô rừng trên bản lưu thử cho cây khỏi che).
- Khác Critters, cố ý: phía nam không làm vách tụt xuống bãi cát (dải cát vẽ sẵn chỉ rộng khoảng 100 px, vách 200 px sẽ lấp hết cát), giữ bãi thoải có đồ ven biển; không dừa trên dải cát ngoài lưới (cây cao ở lớp `cat` sẽ vẽ dưới công trình sát mép; ô rừng ven biển đã có dừa); lớp `co_rai`, `moi_co` để trống (đồng cỏ vẽ tay đã có cỏ, hoa; môi cỏ vẽ liền trong mảnh vách).
