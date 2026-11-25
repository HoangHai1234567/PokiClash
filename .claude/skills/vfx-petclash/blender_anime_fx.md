# VFX anime bằng Blender, render ra khung 2D

Học từ bộ 11 file mẫu "Anime Style FX Workflow" của CodyWinch (Gumroad `b3dfxdemo`, người dùng mua và đưa vào 2026-11-24;
tutorial YouTube `fE-uDqBpXxI`, 24 phút). Bản lưu nội bộ: repo AtomSpine `refs/blender_anime_fx/` (chỉ dùng tham khảo nội bộ,
không phát hành lại). Công cụ đọc file: `refs/blender_anime_fx/tools/` (`doc_blend.py`, `tom_tat.py`, `render_thu.py`).

## 1. Khi nào dùng

- Khối lửa, khói, nổ, cầu năng lượng, lốc, phun lửa: thứ cần **khối liền, mép đẹp, chuyển động mượt, dài ngắn tuỳ ý**.
- Thay cho các cách đã thử và bị chê ngày 2026-11-23 (mục 8).
- Đường đi: script `bpy` dựng cảnh (chạy nền `blender.exe -b --disable-autoexec -P x.py`) → render chuỗi PNG nền trong 24 khung/giây
  → AtomSpine `att.seq` (slot tờ khung) → `.atomik` → game. Chỉnh thông số rồi render lại không tốn credit.

## 2. Nguyên lý (cả 11 file đều vậy)

- **Không render texture.** Hình do modifier biến dạng và cắt lưới; màu do **nhiều lớp vỏ (shell) chồng nhau**, mỗi lớp một vật liệu
  **Emission màu phẳng** (không đèn, không bóng). Hợp sẵn luật tô phẳng của dự án.
- **Texture chỉ dùng làm trọng số đỉnh**: Vertex Weight Edit lấy texture Clouds / Voronoi (toạ độ = một Empty) đổi thành trọng số nhóm
  đỉnh, rồi trọng số đó điều khiển Displace (phồng) và Mask (khoét lỗ).
- **Mọi núm animation là Empty** nối qua driver: dời / phóng Empty là đổi vân, độ phồng, ngưỡng ăn mòn. Không key từng modifier.
- **Lớp ngoài đẩy xa hơn một chút** (Displace hằng 0,1 / 0,2 / 0,3) để các lớp không chồng mặt nhau; **ngưỡng Mask lệch nhau theo lớp**
  (var, var−0,1, var−0,2) nên khi ngưỡng tăng, các lớp bong lần lượt như lột vỏ.

## 3. Chuỗi modifier chuẩn (Cloudy Explosion 2.8, giá trị thật trong file)

Một khối lập phương 8 đỉnh, cùng chuỗi cho 4 lớp; khác nhau ở vật liệu, ngưỡng và lớp đẩy cuối:

| # | Modifier | Thiết lập |
|---|---|---|
| 1 | Subsurf | 6 (render 5–6) |
| 2 | Cast | Sphere, factor 1 → thành quả cầu nhiều đỉnh |
| 3 | Vertex Weight Edit "Texture" | nhóm `Texture`, default 0, falloff Custom Curve đảo (0→1, 1→0), mask texture **Clouds** (scale 0,25, Soft, depth 2), map Object = Empty `Overall Disp` |
| 4 | Vertex Weight Edit "Fine Texture" | nhóm `Fine Texture`, use_add, texture Clouds **Voronoi F1** (scale 0,1, contrast 3), Empty `Fine Texture` (scale 0,1) |
| 5 | Vertex Weight Mix ×3 | chép `Texture` sang `Disp`, `Mask`, `Edge Smooth` (mix SET, ALL) |
| 6 | Vertex Weight Mix "Fine Texture Add" | `Mask` += `Fine Texture` × 0,1 (lớp lõi × 1) → mép lỗ có răng nhỏ |
| 7 | Vertex Weight Edit "Mask Threshold" | nhóm `Mask`, use_remove, ngưỡng = driver `Melt Back.z − (0 / 0,1 / 0,2)` |
| 8 | Vertex Weight Edit "Edge Smooth Threshold" | như trên, lệch thêm −0,05 |
| 9 | Displace | theo nhóm `Disp`, mid 0, strength = driver `Disp Amount.scale.y` |
| 10 | Subsurf | 1 |
| 11 | Displace | như 9, strength /2 → mặt sủi bọt, "mây" hơn |
| 12 | Mask | nhóm `Mask`, invert → khoét lỗ |
| 13 | Smooth | factor 1, **35 lần** → mép lỗ tròn, hết răng cưa của lưới vuông |
| 14 | Displace | hằng 0,1 / 0,2 / 0,3 theo lớp (tách lớp) |

Lớp (trong → ngoài): `Center` (vật liệu Highlight: Layer Weight Facing → ColorRamp → Emission = viền sáng), `Smoke` cam, `Fire` cam đen,
`Fire Bloom` đen. Animation 60 khung / 24 fps: `Overall Disp` scale −3,45 → −4,91 (vân nở), `Disp Amount` scale 0,49 → 3,26 (khối phồng),
`Melt Back` z 0,57 → 0,88 (ăn mòn, lột lớp). Không key gì khác.

## 4. Sáu mẫu, mỗi mẫu dạy một chiêu

| Mẫu | Chiêu học được |
|---|---|
| Cloudy Explosion | chuỗi chuẩn mục 3: nổ mây lột 4 lớp kem → cam → nâu → đen |
| Blue Puffy Explosion | cụm khói chạy dọc **Curve** (Displace X theo nhóm `Curve` + Curve modifier), **Remesh** trước Subsurf, 3 Displace chồng, Decimate + Smooth 25; điều khiển bằng **xương Armature** (`Main Cloud Move`, `Main Cloud Peel` → driver ngưỡng `1 − var*−1`); tia lửa = lưới 15 đỉnh kéo dài bằng Displace X/Z (key strength −68 → giá trị cuối) qua **Lattice** |
| Directional Explosion (chỉ 2.79) | nổ có hướng bằng **Warp** (Warp From → Warp To, strength 0,7–1,25 theo lớp); texture **Voronoi Distance** (0,25; tia lửa 0,02); lớp nền bất động Smooth 100; Empty `Main Disp` trôi y 5,7 → 33,5 làm vân chạy |
| Energy Ball | thân đen + lớp năng lượng hồng bên dưới; Mask lớp ngoài theo ngưỡng `Energy Threshold.z` (0,72 → 0,57) → gân năng lượng lộ dần qua khe |
| Swirling Energy | một lưới **Master Deform** (ẩn) gánh biến dạng: Displace ×3 → **Simple Deform Twist** (góc = driver) → Displace X → **Curve** theo BezierCircle; các lớp màu bám theo bằng **Surface Deform**, mỗi lớp Mask riêng (Voronoi + Clouds, mix DIF) |
| Twisting Effect | nét xoắn: Warp (strength = driver `Motion Ctrl.scale − 1`, 0,73 → 7,09) + **Lattice chạy theo Curve**; vật liệu Geometry/ramp |

## 5. Render cho game (luật dự án)

- `Emission` màu phẳng, **View Transform = Standard** (file mẫu Cloudy dùng Filmic làm lệch màu; không dùng), **Film Transparent**.
- **Không Bloom / Glare** (luật không quầng). Bản 2.8 dùng Eevee bloom cho đẹp; Blender 4.2+ đã bỏ bloom Eevee, càng không cần.
- Camera **Orthographic** đúng góc sân đấu; cỡ khung vừa hiệu ứng, 24 khung/giây, PNG RGBA.
- Xem nhanh: **Workbench**, Lighting Flat, Color = Material (lấy màu Emission gán vào `diffuse_color`). Nhẹ, an toàn cho máy
  (máy D từng sập khi render nặng: chạy từng lượt, ảnh nhỏ trước).
- Màu theo bảng của hệ (`SKILL.md` mục 1b, 1c): Hỏa kem `#FFF6D6`, vàng `#FFD94A`, cam `#FFA43A`, cam đỏ `#F0702A`; than / tàn đỏ sẫm `#5C1628`.

## 6. Áp vào PokiClash

- **Phun lửa (kiểu clip firebreath)**: lưới phễu (cylinder vuốt nhọn về miệng, hoặc cầu kéo dài theo +X) thay cho cube+Cast; Empty vân
  trôi dọc +X; 4 lớp kem / vàng / cam / cam đỏ, lớp ngoài cùng đỏ sẫm; `Melt Back` tăng → lửa thủng lỗ rồi **còn lại các đảo lưới rời =
  mảnh tàn** (đúng kiểu clip giây 19,3–19,8, không khói); cho mảnh rơi bằng Displace hướng −Z có trọng số tăng theo thời gian hoặc key
  vị trí lưới. Cục cuộn đầu luồng = cầu dùng chuỗi mục 3.
- **Nổ trúng, nổ nấm**: chuỗi mục 3 (lột lớp), thêm Warp cho nổ có hướng (Directional), Curve cho cụm khói chạy (Blue Puffy).
- **Cầu năng lượng, chiêu xoáy**: Energy Ball, Swirling Energy (đổi màu theo hệ).
- Mỗi hiệu ứng một file `.py` dựng cảnh từ đầu (không sửa tay file .blend), để agent chỉnh số rồi render lại.

## 7. Blender 5.2 với file cũ (đã thử 2026-11-24)

- File 2.79 / 2.8 mở được; modifier, texture cổ (Clouds, Voronoi), driver giữ nguyên.
- Mở bằng `--disable-autoexec` (file tải về có thể chứa script).
- Hành động (action) từ 4.4 là nhiều lớp: đọc fcurve qua `action.layers[].strips[].channelbags[].fcurves` nếu `action.fcurves` không có.
- **Đường dẫn ra phải tuyệt đối**: đường dẫn tương đối được tính theo thư mục chạy của Blender (đã lỡ ghi ra `C:\render\`).

## 8. Các cách đã thử cho phun lửa và bị chê (2026-11-23)

| Cách | Kết quả |
|---|---|
| Vẽ bằng numpy (nhiễu + ăn mòn + dải màu) | "đúng nhưng không đẹp": nét máy, múi thành chùm bong bóng |
| GPT 2.6 vẽ tờ 24 khung kèm ảnh khung dáng | GPT tô lại đúng hình khung dáng, mất style |
| Khung GPT + video Kling 2.5 | hình đẹp nhưng như **chất lỏng** (giọt chảy, đứt thành giọt) nếu không dặn rõ FIRE + negative liquid; Kling không tự tắt luồng; dáng méo (chuỗi cục cổ thắt) |
| Vỡ mảnh bằng Voronoi cắt từ khung cuối | như kính vỡ, mảnh còn ruột lửa: sai |

Kết luận: khối lửa cần **hình học thật đổi theo thời gian** (Blender, mục 2–6), không phải ảnh tĩnh cắt ra hay video AI khó điều khiển.

## 9. Bộ lửa đã dựng (2026-11-24, máy D, `ArtGen/Spine/vfx_blender/`)

Thư viện `fxbl.py` (lớp vỏ, gradient Blend gắn Empty, `standard_stack`, `two_tone`, `shatter_group`, render Workbench).
Mỗi hiệu ứng một script, chạy `blender.exe -b --factory-startup --python <x>_blender.py -- <thư mục ra tuyệt đối> [--save x.blend]`:

| Script | Hiệu ứng | Điểm chính |
|---|---|---|
| `phun_blender.py` | phun lửa 2 s | nửa cầu nắn phễu; Empty `Mep` (gradient mép đầu) vươn ra 0,7 s → **bùng từ từ** (người dùng chê bản phóng to 0,2 s là "instant thành cục"); ngưỡng riêng từng lớp theo phân vị trọng số (`do_trong_so.py`); cắt đuôi bằng Mask riêng nhóm P (+0,4W) để mép xé chung mọi lớp |
| `cau_blender.py` | cầu lửa bay, lặp 16 khung | đầu cầu + đuôi thuôn ngóc lên; gradient đuôi làm nguội và xé ngọn; lặp bằng **xoay Empty vân đúng 360° quanh trục bay** |
| `no_blender.py` | nổ trúng 1,1 s | sao phẳng kem/vàng 3 khung; cầu phồng nhanh rồi chậm; ngưỡng lột lớp; GN vỡ mảnh toả tròn (`radial=1`) |
| `kim_blender.py` | mũi kim lửa, lặp 12 khung | thoi mũi nhọn, đuôi nguội |
| `loc_blender.py` | lốc xoáy lửa, lặp 16 khung | cầu kín nắn phễu, `two_tone` (vách sau màu nguội), vân kéo dài + nghiêng, Simple Deform Twist 2,6 |
| `lua_blender.py` | lửa cháy, lặp 16 khung | 3 lưỡi lửa (giữa cao, hai bên nghiêng); lặp bằng xoay vân quanh trục ngang X → mặt trước vân chạy lên |

Bài học khi dựng: lớp trong cần ngưỡng mặc định cao hơn lớp ngoài, nếu không mép cắt lòi màu lớp trong (đỏ sẫm); gradient cắt quá gắt cho
mép phẳng như dao cắt, nới rộng để vân xé thành ngọn; lớp có Decimate / Smooth ít có mép khác các lớp khác nên dễ lòi ra; GN vỡ mảnh phải
lấy hướng theo **tâm đảo lưới** (Accumulate Field theo Island Index), lấy theo từng đỉnh thì mảnh bị xé giãn; trong thư mục render cũ còn
khung cũ thì tờ xem bị lẫn, mỗi lần thử ra thư mục mới. Ghép vào AtomSpine: `vfx_lua_toon/build_bl.py` (cầu lửa → nổ, kim ×3, lốc, lửa
cháy, thiên thạch); trang xem `vfx_lua_toon/xem/bo_lua_blender.html`.

### 9b. Vòng sửa 2 (2026-11-24): khói, cầu lửa, kim lửa, lửa cháy

- **Mọi hiệu ứng lửa phải có khói** (người dùng: "tất cả các fx này đều thiếu khói"; lần trước chê khói của video Kling là chê
  *kiểu*, không phải chê có khói). `khoi_blender.py`: cụm 6 múi (to, vừa, nhỏ) nửa cầu, 3 lớp nâu xám `#B9AAA0 / #8C7C74 / #5F534D`,
  gradient đứng khoét lớp nhạt ở đáy → đỉnh nhạt đáy đậm; đặc lúc đầu (ngưỡng thấp), thủng + tách cụm (GN, trọng lực âm = bay lên)
  ở nửa sau. AtomSpine rải nhiều cụm sau lửa (`at=back`): bốc từ thân lửa, **vệt khói đuôi liền** (16 cụm chồng sát nhau dọc đường
  bay; 8 cụm thành chuỗi hạt rời → sai), cụm khói khi nổ, khói đỉnh lốc / lửa cháy (lửa cháy lặp: cụm vượt cuối clip quấn về đầu bằng
  `seq once,<khung>` lúc 0). Ghép: `vfx_lua_toon/build_bl2.py` → dự án sạch `atom_bl/` (Studio cổng 4782).
- **Cầu lửa**: bản "đầu cầu + một đuôi nón" bị chê (trứng có đuôi). Bản đạt: lõi cầu + 5 lưỡi lửa mọc từ nửa sau, toả nhẹ, kéo về
  sau, cong lên; gradient Dau (ADD) cho đầu nóng kem, gradient đuôi làm chót lưỡi nguội đỏ.
- **Kim lửa = kiểu Twisting Effect** (người dùng chỉ định): một lưới kín hình gai nón nhọn (rộng nhất gần đuôi), mặt cắt dẹt 0,62 +
  Simple Deform Twist trục X 5 rad (viền ngoài xoắn), dải xoắn ốc hai màu gán theo **từng mặt lưới** (pha = góc quanh trục/2π·số dải
  + k·x) vàng / đỏ cam, mũi kem, Decimate 0,45 (mặt gãy), vân ăn mòn làm con của mũi kim (xoay theo) chỉ xé đuôi; xoay 360° mỗi chu kỳ.
- **Lửa cháy**: khối 3 lưỡi rộng bị chê (khối vuông). Bản đạt: lưỡi chân tròn (bán kính 0 ở chân), thân thon, đường giữa uốn chữ S,
  4 lưỡi, cả cụm lắc lư bằng Simple Deform BEND trục Y (góc ±0,22, về 0 cuối chu kỳ).
- Xem file mẫu: `ref_codywinch/TAT_CA_6_hieu_ung.blend` gộp 6 hiệu ứng mẫu thành 6 Scene (`gop_ref.py`); render vật liệu gốc bằng
  `render_eevee.py`.
- **Cầu lửa (chốt 2026-11-24)**: người dùng muốn "một quả cầu cháy phát sáng tròn, không đuôi; đuôi lửa đậm và khói làm thành trail
  gắn vào cầu". `cau_blender.py`: cầu tròn + 7 lưỡi ngắn dài ngắn không đều quanh viền, lõi kem vàng (gradient Blend SPHERICAL), đỏ chỉ
  ở viền. `duoi_blender.py`: hạt đuôi lửa đậm (5 lớp, nguội trong ~0,5 s) nằm trước cụm khói 3 lớp → lộ khói, phồng, bay lên, tách cụm.
  AtomSpine (`build_bl2.py` `fly_keys` + `fire_trail`): quả cầu bay theo k khoá thẳng mô phỏng t², mỗi 16 px nó đi qua thả một hạt
  đuôi ngay sau (`at=back`) → vệt liền, dính vào cầu, sát cầu là lửa, xa dần thành khói. Dùng cho thiên thạch.

## 10. Lốc xoáy theo mẫu Tornado của CodyWinch (người dùng đưa 2026-11-24)

Hai file (bản 2.79 / 2.80) ở repo AtomSpine `refs/blender_anime_fx/`: `Updated and Simplified Tornado` (dễ học: mỗi lớp một lưới)
và `RG Simplicity 2018 Challenge Tornado` (cùng ý nhưng nhét vào một quả cầu). Ảnh: `preview_tornado.png`.

| Thành phần | Cách làm trong mẫu |
|---|---|
| Lớp màu | lưới riêng cho Shadow (tối), Orange (thân), Highlight (kem); mỗi lớp trừ trọng số Mask theo `LayerN` (Vertex Weight Mix SUB, hằng 1 / 0,6 / 0,45) rồi Mask → lớp ngoài thủng nhiều hơn, lộ dải tối bên trong |
| Dáng phễu | **Lattice** cao (scale 2,69) nắn bằng **chuỗi Warp**: mỗi cặp Empty From/To ở đáy / giữa / đỉnh với scale X/Y khác nhau (đỉnh 4,3 → loe rộng, giữa 0,23 → eo, đáy 1,96 → chân xoè); một Empty giữa có **F-curve modifier NOISE** trên vị trí → lốc lắc lư ngẫu nhiên. Lưới đi qua Warp "Layering" (scale 0,6) rồi Lattice |
| Dải xoắn | texture Clouds **VORONOI_F1** scale 2 (ô tròn) gắn Empty **trôi lên** (z −2,4 → 12,7 trong 144 khung) + **Simple Deform Twist 4π** (12,57) trục Z → ô tròn kéo thành dải xoắn chạy lên |
| Khói, tia, sét | lưới riêng, Lattice riêng (khói chân xoè 2,25, đỉnh 1,0), xoắn ít hơn (π – 3,84): khói = Clouds VORONOI_F2 kéo dài theo Z, ngưỡng 0,1; tia đỏ = texture VORONOI distance contrast 3, ngưỡng 0,4 → đốm nhỏ; sét xanh = Clouds VORONOI_F2_F1 contrast 3, ngưỡng 0,7 → nét mảnh theo viền ô |
| Mọc lên / tắt | Warp "Raise" (Empty To cao 5,26) đẩy lưới lên; Warp "Thin" (Empty To scale 0,0,1) có **bán kính ảnh hưởng key 3 → 75** ở khung 96–132 → cả lốc ép về trục thành một đường rồi mất; cường độ texture Mask / Thin key giảm cùng lúc |
| Vật liệu | Emission màu phẳng; camera dời dần (dolly) |

Áp vào PokiClash: lốc lửa một lượt ~2 s (không cần lặp): mọc từ đất → xoay, dải xoắn chạy lên, lắc → ép về trục rồi tắt; lớp tối = đỏ sẫm
`#6E1A2A`, thân = cam, sáng = kem / vàng; tia = đỏ / vàng; khói nâu xám do AtomSpine rải thêm. Script: `vfx_blender/loc_blender.py`.

### 10b. Đã dựng theo mẫu (2026-11-24, sau lần đẩy repo)

- `loc_blender.py` v3: 3 lưới thân (tối đỏ sẫm trong cùng, cam ngưỡng 0,5, kem 0,8 + gradient đỉnh ADD 0,1), lưới tia (VORONOI distance,
  ngưỡng 0,62) và vệt mảnh (Clouds VORONOI_F2_F1, nhóm khởi đầu 1 + invert → W = 1 − giá trị, ngưỡng 0,86); dáng eo / loe / xoè bằng
  hàm bán kính trên lưới; vân trôi lên; Twist 4π (tia π); BEND lắc; Goc scale Z 0,06 → 1 (mọc), X/Y → 0,02 ở 1,94 s (ép về trục) cùng
  ngưỡng lên 1,05. Bản dải màu gán theo mặt + quay tròn + vòng chân (trước đó) bị thay.
- `lua_blender.py` v6: **ngọn lửa lồng nhau**: lớp đỏ = cả cụm 5 lưỡi; cam / vàng / kem = cùng cụm thu nhỏ 0,82 / 0,62 / 0,4 từ gốc,
  đẩy ra trước; vân kéo dọc (Empty scale 0,45 × 1,7); gần như không dùng đỏ sẫm. Bản vân đốm tròn bị chê "chưa đẹp".
- **Lốc chốt (2026-11-24)**: người dùng cho **dùng thẳng file mẫu đã mua** ("copy thẳng của nó đổi texture sang kiểu cartoon game của
  mình cũng được vì đây là asset tôi mua rồi"). `loc_tu_mau.py` mở `Updated and Simplified Tornado 280.blend`, giữ nguyên rig, đổi vật
  liệu sang màu phẳng, ẩn Plane / Cube / Smoke, camera trực giao ngang (ortho 10,8, 320×400, tâm z 5,3), Workbench; lấy khung 41→135 bước
  2 (48 khung, 2 s). Bảng **rực cháy**: Shadow `#E0302A`, Orange `#FF9A26`, Highlight `#FFE14D`, Red Sparks `#FFD94A`, Blue Lightning
  `#FFF6D6` (bản Shadow đỏ sẫm `#6E1A2A` bị chê "ngả sang sắc nâu"). Mọc lên làm trong AtomSpine (scale xương chân 0,08 → 1 trong 0,28 s).
  Với các hiệu ứng khác cũng có thể lấy thẳng file mẫu rồi đổi màu theo cách này.
- **Gió cuốn quanh lốc (2026-11-24)**: người dùng muốn "gió cuốn theo tia lửa, bụi tro khói quay quanh, giống con gốc". `loc_tu_mau.py
  --gio`: bật lại lớp **Smoke gốc** (nâu xám `#9A8A80`, vệt khói bụi xoắn, xoè ở chân), 7 **dải gió** mảnh (bề rộng 0,12–0,2, vuốt nhọn hai
  đầu, cung 110–170°, **xoắn dốc lên** 1,5 đơn vị dọc cung, nghiêng ±15–28°, mỗi dải quay một tốc độ; vòng tròn nằm ngang đều bị đọc thành
  sọc trang trí → sai), **tàn lửa / tro bay vòng** bằng GN (Points + Random theo Index: bán kính, cao, góc, tốc độ; cao = (h0 + v·t) mod H,
  bán kính nở theo cao, Instance Ico Sphere; Map Range theo Scene Time thu nhỏ về 0 khi lốc tắt); khung rộng ortho 16, 480×440.

## 11. Lửa toon bằng shader: "Procedural Cartoon Flames in Blender" (Blender Box, youtube RDrswNZYiCo, người dùng đưa 2026-11-24)

Bài (đọc phụ đề bằng yt-dlp): icosphere kéo thành giọt nước + Subsurf 3 + **Displace texture Voronoi** (size 1,3, contrast 0,3) gắn Empty
trôi (driver `#frame/10`) → lửa phập phồng. Vật liệu Eevee: **Voronoi (Distance) → ColorRamp tuyến tính (0 → 0,76) → ColorRamp
CONSTANT** (ngưỡng 70–90 %) → **Invert** → hệ số Mix Shader (Emission / Transparent, Alpha Clip) → lửa đặc có lỗ tròn sắc mép. Ba cỡ
Voronoi (4 / 8 / 16) trộn **Soft Light** (hệ số 1); **Gradient texture** (Mapping xoay Y −90°) trộn vào để lửa mỏng dần về đỉnh; driver
trôi Mapping Z mỗi cỡ một tốc độ (`#frame/-15`, `-30`, `-60`). Nhân bản lưới thu nhỏ / xoay, mỗi bản một màu (đỏ, cam, vàng, trắng).

Đã áp cho **cầu lửa** (`vfx_blender/cau_eevee.py`): 4 cầu lồng nhau đỏ 1,06 / cam 0,96 / vàng 0,8 / kem 0,6 (ngưỡng constant 0,97 /
0,82 / 0,64 / 0,30; đỏ ngoài cùng thưa nhất để cầu "phát sáng"), Voronoi 3 / 6 / 1,6 (bản 8 / 16 / 4 cho lỗ quá mịn trên cầu bán kính 1),
Displace 0,3–0,5; gradient theo X cho phía sau thủng nhiều hơn; **lặp liền** bằng keyframe xoay Mapping (số vòng nguyên mỗi chu kỳ) và
xoay Empty Displace thay cho driver trôi; Eevee, Emission 1, View Standard, nền trong, KHÔNG bloom (bài bật bloom, dự án cấm quầng).
Workbench không render được lỗ trong suốt từ shader → cách này phải dùng Eevee (ảnh nhỏ, an toàn).

Đã áp cho **lửa cháy** (`vfx_blender/lua_eevee.py`): 4 giọt lửa (icosphere kéo phần trên thành ngọn, **gốc đặt ở chân** — để giữa thân
thì Simple Deform Bend gãy lưới thành đường cắt ngang), lớp kem ngoài cùng dùng **gradient ngược** (đặc ở đỉnh) → vệt trắng nóng ở
ngọn như thành quả của bài; trộn 3 cỡ Voronoi bằng **Mix thường + ColorRamp kéo giãn tương phản** (0,3 → 0,8) trước khi nhân gradient
đứng (hệ số 0,5) — trộn Soft Light làm giá trị dồn một khoảng hẹp nên ngưỡng cắt chạy theo gradient thành đường thẳng.
**Lửa cháy bản chốt** (người dùng: "chưa giống video gốc"; so khung 227 s của bài): **MỘT khối giọt lửa bầu** (không phải đống lửa
3 ngọn), lớp ngoài → trong: kem 1,24 (dải đặc ở đỉnh z 0,6→2,1, kéo cao ×1,18, Displace 0,75 → vệt trắng rách ở ngọn và hai vai),
vàng 1,10 (đặc ở chân), đỏ cam `#F0702A` 1,05 (đốm, ngưỡng 0,73, NẰM TRƯỚC thân cam), cam 1,0 (thân đặc, ngưỡng 0,4, thủng ở đỉnh), lõi
vàng 0,84 (lấp lỗ cam ở chân). Bài học:
- **Xoay riêng từng lớp phải nhỏ** (≤ 25°): xoay lớn đưa phần bên của một lớp ra trước → nửa ngọn một màu, đường chia dọc.
- **Đường cắt NGANG thẳng** = chỗ vân bão hoà (ramp kéo giãn chạm 1) → ranh giới chỉ còn do gradient theo cao → đường đồng mức
  ngang. Sửa: cộng Noise (cỡ 2,2, ×1,1 − 0,55) vào trục Z trước Map Range, ramp kéo giãn rộng hơn (0,22 → 0,9).
- **Lỗ kéo dọc như bài**: Mapping Scale (1, 1, 0,6) — Mapping co TRƯỚC rồi mới xoay, ô Voronoi tròn đều nên lỗ luôn dọc theo Z vật dù
  xoay quanh X để vân trôi lên.
- Khói lửa cháy (AtomSpine): cụm nhỏ (0,17) bốc từ ngọn vệt trắng; cụm to bằng nửa ngọn lửa bị thành cột khói lấn át.
**Phun lửa**: người dùng chỉ muốn "một vài fx khói khi lửa bắt đầu tan ở loanh quanh khu vực điểm cuối" → bản chốt: 5 cụm ở **vùng gần
cuối luồng** (65–85 % chiều dài từ miệng, mép trên thân lửa, KHÔNG ở chót), giờ 1,02–1,4 s, thấy rõ từ khung 29 (1,2 s) như người dùng
chỉ; bản rải khói dọc thân lửa bị chê (che hết đầu luồng).

## 12. Đưa bộ lửa Blender vào game (2026-11-24, người dùng: "thay các fx vừa làm vào game", auto mode qua đêm)

- Xuất: `ArtGen/Spine/vfx_lua_toon/xuat_game.py` → `Assets/03 Art/Fx/Hat/hat_fb_<tên>_NN.png`, thu về ~250–300 px (phun 512 ngang),
  nhân alpha trước khi thu. GHI ĐÈ tên cũ để giữ GUID: `no` (26), `khoi` (25), `lua_lap` (24), `cau_lua` (24), `loc_lua` (48); tên mới
  `phun` (47), `kim_lua` (12), `duoi_lua` (27). `vfx_gen/xuat_fb.py` đã bỏ các tên bị thay (chạy nó không đè lại khung GPT cũ).
  Cầu lửa và lửa cháy render lại thành vòng 24 khung (1 s) cho trùng số ảnh cũ.
- Bảng `HatLua.Fbs` (HatFlip.cs) thêm `k` (khung vẽ cao k × h: khung mới lấp đầy khung hơn, khỏi sửa từng chỗ gọi; cầu 0,6, nổ 0,75) và
  `cy` (tâm cụm khói trên neo: 0,28). `DrawFb` thêm `sx` (giãn dọc trục ngang, cho phun lửa đủ dài tới đích mà không dày thêm).
- Cầu tròn không đuôi → `DuoiLua` (thả hạt "duoi_lua" theo QUÃNG bay) gắn ở `FbFly("cau_lua")`, `HoaFbCau` (bay), `FbCauBam`,
  `KmCauBam`, đạn núi lửa (chỉ viên kéo khói, bước 0,7 r: loạt 16 viên). Cầu đang tụ cũng là cầu tròn. Số chốt sau khi soi ảnh chụp
  trong trận: hạt cao 3,6 r, r chặn ≤ 30 đơn vị, bước 0,45 r (≥ 6), tốc độ khung 1,5 (~0,75 s), lớp SAU tướng (Back). Bản đầu (5 r,
  0,9 s, lớp trước) thành cột khói xám phủ cả sân và che tướng mình.
- Bẫy khi thử: tour menu gọi ngay lúc vừa vào Play thì không chạy (App chưa khởi tạo) → chờ log ổn định rồi mới gọi; refresh MCP
  `scope=scripts` có thể không nạp .cs đã sửa (`refresh_triggered: false`) → dùng `scope=all, mode=force` và so giờ
  `Library/ScriptAssemblies/PokiClash.Game.dll`; tour chi tiết tướng xoá thư mục ảnh của tour trận (chép ra trước).
- Phun lửa: `BreathFb` (HatFbHoa.cs) — một khung neo miệng, xoay theo hướng, mép đầu lúc dài nhất = khoảng cách − 0,35 bông chạm, dày tối
  đa 0,95 thân; bắt đầu 0,1 s, chạy nhanh hơn để luồng đứt khỏi miệng đúng `BreathHold`; 5 cụm khói ở vùng 62–78 % chiều dài.
- Lốc: khung một lượt → `HoaFbLoc` phát co giãn đúng t0..t1 (không lặp), cao 1,8 thân, giãn ngang 1,45, lớp trước cùng pha mờ 0,55.
- Kim lửa: `KimLua` vẽ khung "kim_lua" (dài 1,5 LEN, lúc bay giãn 1,3). Thiên thạch: `MeteorFb` (cầu tròn + vệt + "no" lớn + 6 cụm khói).
- Sau khi xuất: menu "Sàn đấu: hạt lửa (bộ Hỏa)" và "Hộp chi tiết tướng: hạt lửa + nút Mana" (nhập lại ~1300 ảnh hạt, ~5 phút: chờ log
  `[Hạt lửa]` trong Editor.log, MCP báo timeout là bình thường).
