---
name: vfx-petclash
description: >
  Bộ skill HIỆU ỨNG (VFX) của PokiClash (game pet clash 2D vẽ tay, tô phẳng, hai con đối đầu trên một góc máy cố định). Gồm luật
  dự án (không quầng sáng, không gradient, không che con bị trúng), mười nguyên tắc thiết kế, nhịp ba pha và số đo, màu 5 lớp, hình
  theo hệ, bố cục và thang cỡ, khớp hiệu ứng với animation, kiến trúc hạt chồng lớp + mảng liền trên uGUI, hiệu năng điện thoại,
  quy trình, bảng kiểm, công thức mẫu, lỗi hay gặp, các nguồn tham khảo đã mổ (Kingdom Rush 5, Clash of Critters, Epic Toon FX,
  pixelfx, file mẫu Blender anime FX của CodyWinch), cách dựng VFX bằng Blender (modifier + lớp màu phẳng) rồi render ra khung 2D.
  Dùng TRƯỚC khi thiết kế, làm, sửa hay chấm bất kỳ hiệu ứng nào (chiêu mana, chiêu cuối, đòn thường, trạng thái, tiến
  hóa, hệ mới), rồi mở skill con được chỉ tới. Animation tướng thuộc bộ `animation-petclash`.
---

# vfx-petclash: hiệu ứng cho game kiểu pet clash

Đây là **skill gốc của bộ VFX**. Nó nói **làm gì và vì sao**; ba skill con nói **làm thế nào trong dự án này**.

| Việc | Mở tiếp |
|---|---|
| Luật hình, code hiệu ứng nằm ở đâu, tia chiêu, gói GPT vẽ ảnh hiệu ứng, nhập ảnh, chụp thử | `pokiclash-vfx` |
| Cảm giác đánh: khựng, rung, bật lùi, chớp, hạt có vật lý, biên đạo theo pha, idle theo hệ | `pokiclash-hero-fx` |
| Công thức từng hiệu ứng hạt (bộ Hỏa, Thủy, Mộc…), thêm hệ mới, chuyển vào game, mẫu nổ / lửa / nước / khói | `pokiclash-fx-congthuc` |
| (bộ khác) Animation tướng, rig, clip | `animation-petclash` → `pokiclash-spine-rig` |

> **LUẬT ĐẦU TIÊN (người dùng 2026-11-25): làm FX thì TRA THƯ VIỆN TEMPLATE TRƯỚC.** "Khi người chơi prompt làm fx dùng skill vfx
> thì đầu tiên phải xem trong thư viện template có vfx tương tự không đã rồi hỏi người chơi, nếu không ưng mới phải làm cái khác."
> Trước khi dựng bất kỳ hiệu ứng nào: tìm cái gần nhất trong thư viện (bảng dưới), đưa người dùng xem (đường dẫn, ảnh / trang xem),
> hỏi dùng lại, chỉnh từ cái nào, hay làm mới. Chỉ dựng mới khi người dùng không ưng.
>
> | Thư viện | Có gì |
> |---|---|
> | AtomSpine `examples/vfx/*` | hit-spark, slash, fire-burst, water-splash, leaf-storm, explosion-flipbook, level-up-ring (ops sinh ảnh); water-ball, water-crown-splash, water-tube, water-whip (flipbook Blender) — tờ khung `<tên>_sheet.png` |
> | AtomSpine `atom templates` (vfx) | emitter, beam, trail, flipbook |
> | AtomSpine `refs/` | `blender_anime_fx/` (11 file CodyWinch: nổ, cầu năng lượng, xoáy, lốc), `water_vfx/` (bộ nước Blender + shader trong trận), `water_pack/` (bộ nước theo gói mẫu SrRubfish + NamuFX: công cụ chụp / mổ gói, phân tích từng prefab, đóng atlas, tia Water Laser, mã trong trận) |
> | Bộ trong dự án (`ArtGen/Spine/vfx_blender/`) | lửa (lua_eevee, phun, cầu, nổ, khói, lốc lửa, kim lửa), nước (`nuoc_repo_bl.py`: cầu, cầu vỡ, tia, tia ống, roi, toé thân, toé đất, thương, mạch phun; `song_cuon_bl.py` sóng; lốc nước) — trang xem `vfx_lua_toon/xem/bo_nuoc/bo_nuoc.html` |
> | Trong game | khung `Assets/03 Art/Fx/Hat/hat_fb_*` (bộ lửa, lốc nước), shader nước `PokiClash/UIWaterFx` (tia, cầu, toé, vương miện, vũng, thương, sóng, mạch phun) — ảnh tour `ArtGen/XemVfx/nuoc_shader/xem.html` |
> | Gói nước mẫu trong Assets (2026-11-25) | SrRubfish "Water - Assets for VFX 02" (`Assets/SrRubfish_VFX_02`: 37 prefab, 72 flipbook) + NamuFX "Stylized Water Effect Pack" (`Assets/NamuFX`): ảnh động từng prefab `ArtGen/XemVfx/vfx_goi/xem.html`, mổ xẻ từng lớp `PHAN_TICH.md`; 40 flipbook đã đóng vào atlas game (`nuoc_fb.png`, bảng `NuocFbBang`) — mục "Bộ nước theo gói" bên dưới |

### Bộ nước theo gói mẫu (bản 3, 2026-11-25)

Người dùng: "làm lại vfx nước của game theo asset này, thêm texture vẽ tay nhẹ nhàng của mình vào, quét thật kĩ ... nó có gì mình cũng phải
có như vậy"; "đặc biệt là tia nước ở water laser rất đẹp"; texture "dùng thẳng nhưng nên thay đổi đi chút".

- **Mổ gói trước khi làm** (bắt buộc với gói mới): `Assets/01 Script/Editor/VfxPackShots.cs` chụp từng prefab trong Play (Time.captureFramerate,
  đọc ảnh ở RenderPipelineManager.endContextRendering, lượt dò điểm ảnh rồi khung sát; bật tạm Application.runInBackground vì game tắt
  Run In Background nên Unity nằm nền là Play đứng) + chụp scene demo; `ArtGen/XemVfx/vfx_goi/ghep.py` ra GIF / tờ 12 khung / xem.html;
  YAML từng prefab → lớp, nhịp, đường cong (scratch: mo_goi_vfx.py, mo_duongcong.py, mo_shadergraph.py) → `PHAN_TICH.md`.
- **Gói vẽ bằng một giá trị xám tô qua 2 màu** (LerpTransparencies) + Fresnel cho mesh + vân nhiễu trôi + tan smoothstep theo alpha hạt.
  Game giữ dáng / nhịp / cách ghép lớp, đổi chất: `ArtGen/Spine/nuoc_goi/dong_goi.py` đóng flipbook thành atlas giá trị + alpha (2 flipbook
  / ô: RG, BA; nguồn ghi ở `NGUON.md` để thay trước khi phát hành nếu gói chưa mua), shader `UIWaterFx` chế độ 6 tô dải cel 4 màu của game
  (ranh run nét tay) + vân chì, mép cắt sắc, mờ = ngưỡng mép dâng; chế độ 7 là ống tia 4 lớp (vỏ rách, vỏ, lõi, vệt bọt trôi; vân
  `WaterNoise_Sharp` kéo dài theo thân).
- **Mã:** `HatNuocGoi.cs` — `NFbS` / `NFbPhat` (phát trọn flipbook theo đời hạt, như UV module 0→1), `NLaser` (tia kiểu Water Laser, cùng hợp
  đồng giờ với tia cũ, gọi từ `NTiaKhung`), `GSplash` / `GTrung` / `GToe` / `GCrownDat` (khối dùng chung, `NuocGoi = true` bật thay khối
  shader bản 2), `GCauThem` (cầu), `GSongThem` / `GSongDo` (sóng), `GCotPhun` (mạch phun), `GMuaDat` (mưa). Hướng gốc của từng flipbook
  (toé ngang / trượt / gai về +x, khối cuộn `CauVong` về −x, `ToeTrung` chéo lên phải, `ToeNgangC` về −x) phải soi bằng tờ khung trước khi xoay.
- Tour thử: menu "PokiClash/Thử/Tướng/Đảo Thủy/nước shader: tia Water Laser (...)" và "... 4 tướng tia, cầu ..." (+ Hàn Ngạc sóng / mưa);
  bật trước "PokiClash/Thử/Play chạy cả khi Unity nằm nền".

**Ranh giới với bộ Animation:**
- **VFX:** tia, đạn, vụ nổ, hạt, mọi thứ bay ra khỏi thân tướng.
- **Animation:** thân và phụ kiện dính thân. Rig chỉ để lại xương miệng / `muzzle` và sự kiện trong clip cho VFX bám vào.

Tài liệu đi kèm trong thư mục này:
- `VFX_KNOWLEDGE_BASE.md`: bộ kiến thức VFX game 2D người dùng đưa vào (2026-11-10), có nhãn độ tin cậy cho từng ý. Mục 7–8 của
  nó (Spine, shader, particle của engine) là kiến thức chung: dự án không dùng Spine runtime, không dùng shader phát sáng.
- `nghien_cuu_thiet_ke.md`: đối chiếu các nguyên tắc với nguồn gốc, số đo nhịp, hình theo hệ.
- `nghien_cuu_hieu_nang.md`: chi phí uGUI, vẽ đè, lưới tự dựng, ảnh hạt, rác bộ nhớ, cách đo.
- `hoc_kr5_vfx.md`: học hiệu ứng nổ, lửa, nước, khói của Kingdom Rush 5 (vẽ phẳng 3–5 màu, không shader, gần luật dự án nhất):
  đỉnh ở khung 1–3, đòn ghép từ đạn → đuôi → trúng → decal → payload → mod, hạt chỉ "dập" hình tự tan. Nhịp "giữ 2 khung" của họ
  KHÔNG dùng nữa: người dùng muốn mượt (mục 1c).
- `hoc_water_vfx_abitofgamedev.md`: mổ repo Unity water_vfx (cầu nước, cụm toé, tia ống, roi nước): một ngưỡng tan mỗi hạt ×
  mặt nạ mềm vẽ tay × nhiễu lệch ngẫu nhiên; cụm toé 6 lớp có số nhịp; tia hai ngưỡng (hiện từ miệng, tan từ miệng); vũng đọng.
- `blender_anime_fx.md`: làm VFX anime bằng **Blender** (modifier biến dạng + lớp vỏ Emission màu phẳng, núm điều khiển là Empty +
  driver) rồi render ra khung 2D cho AtomSpine; học từ 11 file mẫu CodyWinch (2026-11-24, bản lưu ở repo AtomSpine
  `refs/blender_anime_fx/`). Kèm bảng các cách đã thử cho phun lửa và bị chê (vẽ numpy, tờ GPT, video Kling, vỡ Voronoi).
  Khối lửa / khói / nổ / cầu năng lượng lớn: đọc file này trước. Mục 13 = bộ nước: tan theo ngưỡng × mặt nạ mềm (`nuocbl.mask_mat`,
  `mat_na_nuoc.py`), cụm toé 6 lớp + vũng decal, tia hai ngưỡng, sóng cuộn và bài học góc nhìn (mào cuộn úp lên mặt sóng đang thấy).

Khi các quy tắc xung đột: **luật của dự án (mục 1) > đọc được trong trận > hiệu năng > đẹp > chi tiết.**

## 1. Luật của dự án đè lên kiến thức chung

Kiến thức VFX ngoài kia phần lớn viết cho game có ánh sáng. Dự án này vẽ tay, tô phẳng. Đọc tài liệu chung thì đổi như sau:

| Tài liệu chung nói | Dự án làm |
|---|---|
| Lõi sáng cộng dồn (Additive), quầng sáng (glow), bloom | **Không dùng.** Thay bằng hình phẳng màu kem hoặc màu nhạt nhất của hệ, có viền mực, hiện 1–2 khung (xem `pokiclash-hero-fx` mục 2). Ngoại lệ: màn Máy bi và mở rương |
| Gradient, bóng đổ, ánh phản chiếu | Mỗi vùng một màu đều; nét chì gạch chéo chỉ là vân. Không bóng |
| Đỉnh sáng trắng tuyệt đối ở điểm va chạm | Chớp nổ hình sao gai / nước toé màu kem trong 0,1–0,14 s, nhỏ hơn thân đối thủ |
| Hiệu ứng làm bằng Spine (slot, sequence, clipping) | Ảnh hiệu ứng trong clip `.atomik` chỉ còn cho đòn đánh thường. Chiêu mana và chiêu cuối do **lớp hạt trên sân** vẽ (`HatLua`, `HatNuoc`, `HatMang`); clip chỉ còn động tác (`skill_nofx`, `cast_nofx`) |
| ParticleSystem, VFX Graph, shader dissolve | Chưa dùng; muốn thêm phải hỏi người dùng. Hạt là Image trong hàng chờ, chạy theo đồng hồ sân |
| Hiệu ứng dựng bằng lưới 3D / shader ăn mòn | Dựng **offline trong Blender** (modifier + lớp vỏ Emission phẳng, View Standard, nền trong, không bloom), render 24 khung/giây, vào game dạng tờ khung qua AtomSpine (`blender_anime_fx.md`, từ 2026-11-24) |
| Hit flash bằng shader | `_Flash` của shader sticker (đã có), 1–3 khung |
| Hiệu ứng che cả nhân vật ở đỉnh | **Không che con bị trúng.** Vụ nổ nhỏ hơn thân nó; khối nước lớn phủ lên thì làm trong mờ 0,8–0,86 |
| Tránh hiệu ứng dạng ảnh tĩnh trượt | Từ 2026-11-10 chuẩn mốc là hạt chồng lớp phẳng (`ArtGen/Spine/chuan_fx`), không làm hiệu ứng bằng một ảnh tĩnh |

Luật khác phải nhớ: viền mực nâu `#2B2118`; mã chạy không sinh GameObject (`PrefabOnlyTests`); hình và chuyển động aola không
đăng công khai; số chỉnh của người dùng (`adjust.json`) không tự đổi; làm ở Unity, bản web chỉ khi được yêu cầu; người dùng chấm
trên điện thoại Android.

### 1b. Người dùng chấm cả game ngày 2026-11-18 (bắt buộc từ nay)

| Chỗ bị chê | Phải làm |
|---|---|
| Tia, chưởng: cuối tia cụt lủn, không va chạm với địch | Đầu tia tới tận thân đối thủ. Ở chỗ chạm có bông va chạm liên tục theo hệ: nước toé mão ngược về người bắn, lửa bung, mảnh văng, vòng va chạm. Tia đập vào thân thì loe hoặc tạt theo thân. Đối thủ chớp và giật. Hết tia thì đuôi đứt từ gốc, phần còn lại bay nốt rồi vỡ, không cắt phụt |
| Khói rải rác, chưa thành cụm, chưa mềm | Sinh thành cụm nhiều múi chồng lên nhau (to, vừa, nhỏ), mép mềm (được phép alpha mềm ở mép cho khói), bay lên, tách cụm rồi mới mờ. Hai tông phẳng: đỉnh nhạt, đáy đậm |
| Lửa rời rạc; dung nham là cầu tròn cứng | Lửa liền khối, lưỡi chữ S có giọt tách. Dung nham là khối chảy có giọt kéo, mép gợn, khe nứt vỏ |
| Hút khí / lửa quanh để tụ cầu xấu | Hạt bị hút là vệt thuôn bay xoắn vào tâm, tăng tốc dần, hiện dần lúc sinh, nhập vào cầu. Có 1–2 vòng co về tâm. Cầu lớn theo nhịp đập, là khối cuộn nhiều múi. Trước khi nhả, cầu nén 1–2 khung rồi chớp |
| Nổ, sóng âm chưa đẹp; nước, lửa chưa như Kingdom Rush | Theo `hoc_kr5_vfx.md`: chớp 1–2 khung → lưỡi liềm lửa trong khói hai tông → khói tách cụm bay lên; vòng cung dẹt trên đất. Sóng âm là dải cung dày thuôn hai đầu |
| Gai lá, gai sắt đâm lên (Cầu Gai, người cây, măng trúc Rồng Trúc, cột tinh thể Thiết Tinh / Thiết Khoáng) xấu (2026-11-19) | Làm lại theo style mục 1c, chạy theo tờ khung 12 khung: đất nứt → gai phóng lên (giãn dài ở khung bung, đất văng) → giữ, lắc nhẹ → gãy hoặc rút, vụn rơi. Gai lá cong thuôn, một tông lục, gân lá bằng nét chì. Gai sắt / tinh thể nhiều mặt sắc cạnh, một tông, cạnh mặt bằng nét chì (không mặt sáng / tối, không vệt sáng: "bỏ bóng ánh sáng" 2026-11-19). Đã có bộ 24 khung `ArtGen/Spine/vfx_gen/khung_chi/gai_la`, `gai_sat`, `gai_bang` |
| Vụ nổ nằm dưới địch, không thấy rõ (2026-11-19, xem bản khung vẽ sẵn trong game) | Nổ (`no`, `trung_lua`, cột `nham`) vẽ ở lớp **TRƯỚC** tướng (Front), không đặt sau lưng đối thủ cho "khỏi che". Neo ở chân / thân, dời 0,1–0,2 thân về phía người ra chiêu, cho nhanh hơn chút để không trùm lâu. Gai đâm lên cũng phải có 2–3 cụm Front hai bên chân (±0,5–0,7 thân, cao 0,6–0,9); cụm sau lưng chỉ làm nền, đủ cao để ló lên trên vai |
| Cầu lửa, tên lửa… thiếu vệt khói (2026-11-19) | Mọi vật bay cháy (cầu lửa, tên lửa, đạn pháo, thiên thạch, tảng đá bay, móc xích lửa) kéo **vệt khói đuôi**: `HatLua.FbKhoiDuoi` (cụm khung `khoi` nhỏ 0,2–0,35 thân, ~26 cụm/giây, rải trên cả đoạn vừa bay, tan ~0,5 s, lớp dưới vật bay; tảng đá nhuộm bụi đất). Bỏ đuôi khói cũ, không để hai vệt. Giữ dưới 120 hạt (loạt nhiều đạn thì thưa hoặc chỉ một phần số đạn kéo khói). Vệt phải là KHÓI: cụm khói chồng sát nhau, xám nâu, mềm. KHÔNG dùng dải mảng liền màu than: người dùng chê "phải là khói chứ không phải tô đen". Cụm rời cách quãng cũng bị chê là rải rác |
| Tia năng lượng / nước "nhìn vẫn chưa đã" (2026-11-19): ống thẳng đặc, một bề dày, chỗ trúng nhỏ | Dựng tia bằng `HatLua.TiaFb` (`HatTiaFb.cs`) qua 4 pha: tụ → phóng → dội → tắt (chi tiết ngay dưới bảng) |
| Màu tối, không hợp theme; đốm lửa đơn lẻ và to quá | **Màu tươi**, hợp sân cát sáng, trời xanh, chì sáp tươi. Ví dụ lửa: kem `#FFF6D6`, vàng `#FFD94A`, cam `#FFA43A`, cam đỏ `#F0702A`; nước: kem `#F2FBFF`, lam nhạt `#9FE0FF`, lam `#4EB6F2`, lam đậm `#2B7FD0`. Đốm nhỏ, đi theo cụm 3–6 lệch cỡ. Chỉ khói than là tối |

Bộ hình hạt kiểu Kingdom Rush (`hat_kr_*`, sinh bằng `ArtGen/Spine/hat_kr.py`) có sẵn dáng cho các chỗ trên. Soi từng tướng
trước / sau ở trang `ArtGen/XemVfx/MO_WEB.bat`: chụp bằng menu "PokiClash/Thử/Hiệu ứng mọi tướng: chụp bản TRƯỚC / SAU", dựng lại
bằng `ArtGen/XemVfx/xay_trang.py`.

**Sóng âm** (người dùng 2026-11-19: "làm đơn giản thôi ... vài nét vẽ tay tô chì màu xám nhạt"):
- Mỗi cung là 2–3 nét chì xám nhạt song song, không viền mực (`hat_kr_songchi_*`, `ArtGen/Spine/hat_songchi.py`; hàm `SongChi` trong `HatSongChi.cs`).
- Mỗi lần gầm 3–4 cung. Cung nở dần từ miệng tới mặt trước thân đối thủ rồi mờ.
- Không vòng tròn ở miệng, không dải cung hai màu.
- Không dùng shader bẻ cong: trên uGUI phải render cả sân ra texture mới bẻ được, nặng trên điện thoại.

### 1c. Style mục tiêu cho lửa, nước, nổ, khói, năng lượng (người dùng chọn 2026-11-19, bắt buộc)

> **CẬP NHẬT CUỐI 2026-11-19 (đè bảng "chất liệu game" bên dưới cho khung vẽ sẵn):** người dùng so bản gen gốc với bản làm phẳng + vân chì: "tôi nhìn thấy bản cũ đẹp hơn … có thể dùng bản gốc luôn cũng được". Khung FX vào game là BẢN GEN GỐC (cắt, tách nền, đủ màu RGBA), giữ mảng chuyển màu, khối, quầng của bản gen; không gom màu, không vân chì, không giảm 255 màu. Tia nước phải "mềm mại, 3D, tươi sáng". `chi_phang.py` chỉ để so.

**Lời dặn, theo thứ tự:**
1. Người dùng gửi 4 gói hình vector VFX hoạt hình: "đổi kiểu lửa/nước/nổ trong game theo link ảnh tôi gửi, rút ra kiểu style này", "tôi muốn vfx mượt hơn nữa nghĩa là có thể tăng frame lên".
2. Xem bộ 15 hiệu ứng 24 khung gen theo các gói đó, họ sửa lại: **"đẹp nhưng texture chưa hợp với style game, kiểu chì vẽ, bỏ bóng ánh sáng đi"**.

Kết quả là **dáng và chuyển động lấy từ ảnh mẫu, chất liệu là của game**.

**Nguồn:**
- Bốn gói ở thư mục Downloads: `comic-explosive-fire-cloud-game-effect-vector`, `water-splash-vfx-animation-cartoon-sprite-sheet`, `green-ui-vfx-tornado-energy-with-flame-game`, `explosion-set`.
- Bản thu nhỏ: `ArtGen/StyleRefs/vfx_mau/`. Hình stock của bên thứ ba: không commit, không chép nguyên vào game khi chưa rõ giấy phép.

**Phạm vi:**
- Mục này đè lên dòng "viền mực" ở mục 1 cho lửa, nước, nổ, khói, năng lượng: **không viền mực ngoài**.
- Luật "không quầng sáng, không gradient" của mục 1 **vẫn giữ**.
- Hình tướng vẫn theo luật cũ.

| Thành phần | Lấy từ ảnh mẫu (dáng, nhịp) | Chất liệu game (bắt buộc) |
|---|---|---|
| Chung | Hình vector mềm, cụm múi, nhiều khung trung gian | **Tô phẳng**: mỗi vùng một màu đều. **Vân chì màu** gạch chéo −38 độ phủ lên (như hạt `hat_*` và tranh bản đồ). **Không** mảng sáng bầu dục, đáy tối, chuyển màu, quầng mềm, điểm sáng trắng. Không viền mực ngoài. |
| Lửa | Lưỡi nhọn sắc nhiều ngọn quặp, vệt kéo theo hướng bay, tia chớp mảnh toả từ tâm | Các **lớp màu phẳng** bảng "hoa": đỏ `#E8452E` (mép), cam `#FFA43A`, vàng `#FFD94A`, kem `#FFF6D6` (chỉ lõi / chớp). Mép rõ, không quầng. |
| Nổ (tờ mẫu 9 khung) | (1) cụm múi phồng; (2–3) chớp sao ở tâm; (4) thành nấm có thân, đất toé hai bên; (5) nguội, còn đốm đỏ trong khói; (6–7) khói; (8–9) vỡ thành mảnh khuyết hình lưỡi liềm rồi tan | Lửa như trên, khói như dưới, đốm than là mảng đỏ / cam phẳng. |
| Khói | Cụm múi tròn chồng nhau, đi theo luồng lửa, tan thành mảnh khuyết | **Một tông** nâu xám (`#8C7C74`). Múi ra bằng **nét chì trong** sẫm hơn màu nền ~30 %, không bằng mảng tối. Tan dần bằng alpha. |
| Nước (tờ mẫu 16 khung) | Sóng dâng, cuộn mào, vỡ thành mảng rồi giọt, còn vũng mỏng | **4 mảng lam phẳng** theo thứ tự của bản mẫu: lam đậm `#1D5FD2` ở đỉnh, lưng → lam `#2F8FE8` → xanh trời `#35BFEA` → ngọc lam `#45DFD0` ở chân. Người dùng chê một màu "nhạt nhẽo", 2026-11-19. Mảng có mép rõ, không chuyển màu mịn. Bọt trắng ở mào và ngọn, chấm bọt nhỏ. Không vệt sáng mảnh. |
| Năng lượng, lốc | Dải xoắn tương phản lục sẫm – lục chanh – ngọc lam, vệt tím | Dải màu phẳng. Không lõi phát sáng, không hạt sáng. |
| Tinh thể, lá, gai | Cụm gai phóng lên, giữ, gãy / rút | Một tông cho thân, cạnh và mặt bằng nét chì. Bụi đất là mảng nhạt riêng. |
| Màu | Tươi, bão hoà cao | Tông phải đủ đậm để không chìm trên nền trận sáng. |

**Cách làm bộ khung (2026-11-19, thư mục `ArtGen/Spine/vfx_gen/`):**
1. Gen tờ 6 × 4 = 24 khung bằng GPT 2.6 qua Magnific (1k high, 3:2, 95 credit), dùng ảnh mẫu style. Tách nền bằng Magnific (3 credit).
2. `cat_khung.py` cắt theo mảng liền: khung lấn ô bên vẫn đủ hình. Cùng một hộp cho mọi khung, nên điểm neo đứng yên. Script cũng gỡ nền ô cờ giả lẫn trong chỗ trong mờ.
3. (Bỏ từ cuối 2026-11-19: chỉ để so.) `chi_phang.py` làm phẳng:
   - phân họ màu, về màu đích gần nhất;
   - vệt sáng lấy màu vùng quanh, bỏ quầng lửa;
   - thêm nét chì trong cho khói, tinh thể, lá;
   - phủ vân chì.
   - Hình nhiều dải xoắn (lốc nước / lửa / cát, 2026-11-19) thì dùng **bảng màu tự lấy** (k-means 5–6 màu từ chính bản gen, `auto_k`).
     - Bảng cố định gộp mất dải sáng / tối, ra trầm. Người dùng chê vòi rồng cũ "màu hơi trầm".
     - Dải mảnh thì mép rõ (`hard_alpha`): làm mờ alpha sẽ thành nửa trong suốt.
     - Vân chì nhạt hơn (`tex_k` 0,6).
4. Xem `vfx_gen/xem/chi.html`.

**Tia vẽ sẵn** (`HatLua.TiaFb`, `HatTiaFb.cs`):
- **Tụ:** cầu đầu nòng lớn dần.
- **Phóng:** đầu tia vươn tới đích trong ~0,1 giây, đoạn đầu phình.
- **Dội:**
  - thân tia là nhiều ĐOẠN vẽ sẵn (đầu đuôi thon) trôi liên tục từ miệng tới đích, chồng 2/3 lên nhau;
  - bề dày phập phồng ~8 lần / giây, gợn ngang;
  - bông va chạm lặp ở thân địch, lật theo hướng tia.
- **Tắt:** ngừng nhả, đuôi tia rời miệng rồi bay nốt vào đích.

**Bộ da tia:**

| Bộ da | Dùng cho |
|---|---|
| `DaTiaMoc` | Lá |
| `DaTiaNuoc` | Nước |
| `DaTiaLua` | Lửa |
| `DaTiaVang` | Mặt Trời, hổ phách |

**Số đo:**
- Bề dày: mana ~0,22 thân người bắn, chiêu cuối 0,28.
- Giữ giờ chạm cũ: `tTu = giờ chạm − thời gian vươn` (quãng / 2600, kẹp 0,07–0,14).
- `nongK` / `trungK` chỉnh cỡ đầu nòng / bông trúng theo chiêu.

**Mượt** (người dùng 2026-11-19):
- **Bỏ luật "giữ 2 khung"** học từ Kingdom Rush: hạt cập nhật và đổi hình **mỗi khung**.
- Hiệu ứng chạy theo tờ khung (flipbook) phải có nhiều khung trung gian: toé, nổ 12–20 khung, chạy 24–30 khung/giây (tờ mẫu nước toé có 16 khung).
- Hạt đổi hình theo tuổi thì chồng mờ sang hình kế (cross-fade) hoặc dùng nhiều bước hình hơn, không nhảy cụt.
- Vị trí, cỡ, góc đi theo đường cong êm, không giật.

**Trong game (2026-11-19):**
- Khung ở `Assets/03 Art/Fx/Hat/hat_fb_<tên>_NN.png`, xuất bằng `vfx_gen/xuat_fb.py` (giảm 255 màu, 336 khung ~2,7 MB).
- Phát bằng `HatFlip.cs`:
  - `Fb(fx, neo, cao, …)`: một lượt, hoặc lặp với `life`;
  - `FbFly(fx, từ, tới, cao, tốc độ, onHit, …, khoi)`: vật bay tự xoay / lật;
  - `FbKhoiDuoi`: vệt khói đuôi;
  - `HasFb`: chưa nhập ảnh thì quay về hạt cũ.
- Chạy 24 khung/giây, chồng mờ khung kế.
- Mỗi hệ có file hàm dùng chung riêng: `HatFbHoa`, `HatFbThuy`, `HatFbMoc`, `HatFbKim`, `HatFbTho`.
- Sau khi thêm ảnh, chạy menu "Sàn đấu: hạt lửa" và "Hộp chi tiết tướng: hạt lửa".
- Nhân màu (`tint`) chỉ làm tối đi. Muốn bụi be sáng, nổ năng lượng vàng, nổ lá xanh thì gen bộ khung riêng.

**Cách làm trong code:**
- Lửa, nước, nổ, khói, năng lượng theo style này thì **bỏ lớp mực** (bản đặc vẽ dưới).
- Ảnh hạt giữ vân chì: ảnh xám vân chì rồi nhuộm, hoặc khung flipbook đã tô sẵn. Không vẽ gradient.
- Không thêm ảnh quầng sáng.

## 2. Mười nguyên tắc thiết kế

1. **Hiệu ứng là phản hồi cho người chơi, không phải trang trí.** Cần rõ thì bớt hiệu ứng.
2. **Kiểm đủ ba thứ: hình, màu, nhịp.** Bỏ màu đi mà vẫn nhận ra hệ nào thì hình đã đúng (mục 5).
3. **Tách hiệu ứng thành phần tử và hỏi từng cái:** nó là chính hay phụ, hút bao nhiêu chú ý, hiện và tan lúc nào, có gây nhiễu không.
4. **Thiết kế cho đúng góc máy của game:** ta ở dưới phải, địch ở trên trái. Chiêu phải đẹp theo cả hai chiều bắn.
5. **Chốt nhịp bằng hình đơn giản trước, chi tiết sau.** Dựng bản xem trước Python, soi tờ 12 khung, rồi mới trau chuốt.
6. **Ngắn.** Hiệu ứng dài che trận đấu. Thời lượng cũng nói lên độ quan trọng.
7. **Ba pha: lấy đà, đỉnh, tan** (mục 3). Đỉnh nên tới sớm, trong khoảng một phần tư đầu của phần sau lúc nhả (gợi ý của VFX
   Apprentice; bản hướng dẫn của Riot không ghi con số này, xem `nghien_cuu_thiet_ke.md` mục 1).
8. **Không dùng đường cong tuyến tính.** Bắn mạnh rồi hãm; nở nhanh rồi co chậm.
9. **So le.** Các phần tử không cùng bật, cùng tắt; mỗi hạt khác cỡ, tốc, giờ, đời.
10. **Một màu chủ đạo, tối đa ba sắc** trong một khung hình (không tính mực và trắng).

## 3. Nhịp

### 3.1 Ba pha

| Pha | Đặc điểm | Trong dự án |
|---|---|---|
| Lấy đà (anticipation) | ngắn, báo trước | hạt hút vào, vòng co lại, cầu lớn dần ở miệng, mây tụ, xoáy dưới chân. Chạy **trong lúc tướng lấy đà** |
| Đỉnh (climax) | nhiều phần tử nhất, tương phản và bão hòa cao nhất | chớp toé 0,1–0,14 s + vành hạt toả đều + rung + khựng |
| Tan (dissipation) | tương phản thấp, mờ, ngắn nhưng không cắt cụt | khói tan dần bay lên, bọt co lại, giọt rơi loang vòng, vũng nước |

Dẫn mắt bằng lấy đà, dồn hết vào đúng khoảnh khắc người chơi chờ, rồi cho mắt thời gian nghỉ.

### 3.2 Hai kiểu nhịp

- **Xung (impulse):** có một đỉnh. *Tức thì* (bỏ lấy đà: đòn thường, tia lửa trúng) hoặc *dồn dần* (tụ rồi nổ: chiêu lớn).
- **Nhịp (rhythm):** dao động, không có đỉnh: lửa bờm, aura, mưa, khiên, hồi máu.
- Ghép được: cầu nước = nhịp (tụ) → xung (ném) → nhịp (bay) → xung (vỡ).
- **Nhịp nhanh hơn nhịp tim đọc là hung hăng, chậm hơn đọc là thân thiện.** Hồi máu, buff dưới 60 nhịp/phút (số có nguồn); đòn
  đánh thì nhanh hơn nhịp tim (nguồn không cho số).
- Hiệu ứng tức thì vẫn cần **đoạn ra**: giảm dần trước khi mất.

### 3.3 Số dùng trong dự án (giây sân)

| Loại | Lấy đà | Bay / giữ | Đỉnh | Tan |
|---|---|---|---|---|
| Trúng đòn thường | 0 | 0 | chớp 0,1–0,14 | hạt 0,3–0,5 |
| Đạn, cầu (mana) | bằng giờ trúng của clip bắn (0,5–0,6) | 0,2–0,55 | chớp + toé | 0,5–1,3 |
| Tia, luồng phun | bằng giờ trúng của clip | giữ 0,9–1,25, tướng giữ dáng nhả | toé liên tục mỗi 0,24 | 0,4–0,6 |
| Chiêu cuối tại chỗ đối thủ (mưa, xoáy, vòi rồng) | bằng giờ trúng của clip chiêu (0,9–1,3) | 0,6–1,65 | nhịp 3–4 lần hoặc một cú lớn | 0,4–1,0 |
| Tiến hóa | 1,2–1,6 | lốc đậm nhất lúc đổi dạng | nổ, gầm | hoà về idle dạng mới; clip 2,8 |

Mốc ngoài để so (nguồn ở ba file `nghien_cuu_*.md`):
- Đòn nhanh của Pokémon GO dài 0,5 s, trúng ở 60% clip; chiêu tụ lực trúng ở 60–90% clip.
- Hiệu ứng 2D: lấy đà 0,1–0,25 s, chớp 0,03–0,1 s, bung 0,1–0,3 s, tan 0,3–1 s; lấy đà cộng va chạm không quá 1/3 tổng. Trúng
  nhỏ 0,2–0,5 s, chiêu 0,5–1 s, nổ có khói 0,8–2 s.
- Khung va chạm 1–3 khung; dài hơn đọc thành đổi cảnh.
- Kingdom Rush 5 (`hoc_kr5_vfx.md`): hiệu ứng trung vị 0,5 s; nổ 0,6–1,0 s; nước trúng nhỏ 0,33 s; họ vẽ giữ 2 khung (15 hình/giây)
  nhưng dự án KHÔNG theo, người dùng muốn mượt hơn (mục 1c: mỗi khung đổi hình, toé / nổ 12–20 khung ở 24–30 khung/giây); đỉnh ở khung 1–3; nổ của chiêu lấy đà 2 khung bằng cục chớp nhỏ; đòn đánh xuống đất báo trước 0,4 s (lỗ, vết nứt trên đất).
- Khựng 60–120 ms, dài hơn thì giống giật máy; game đối kháng khựng 9–14 khung. Dự án khựng 0,03–0,2 s (`pokiclash-hero-fx` mục 4).
- Đòn nhiều nhịp chỉ khựng ở nhịp đầu và nhịp cuối. Chớp màn không quá 3 lần mỗi giây.

## 4. Màu và sáng tối trong luật tô phẳng

- Mỗi hiệu ứng một bảng 5 lớp: **mực, đậm, giữa, nhạt, sáng nhất**. Hạt xám vân chì nhuộm bằng `Image.color`.
  - Lửa: lớp sáng ở **chân** (lõi), nguội dần theo tuổi hạt. Nước: lớp sáng dồn về **ngọn** (bọt ở mào sóng), không nguội.
- **Bảng theo tướng** chứ không chỉ theo hệ (`Themes`, `WThemes`): lửa tím hồng cho cáo, vàng kim cho sư tử; nước băng cho chim
  cánh cụt, tím lam cho chim đàn. Thêm một họa tiết riêng (mảnh tinh thể, cánh sen, sao, mảnh băng) văng ra lúc trúng.
- Màu hệ nhất quán cả game: Hỏa cam đỏ lõi vàng; Thủy lam và trắng bọt; Mộc lục tươi; Kim vàng nhạt, xám thép; Thổ nâu, vàng đất;
  băng lam nhạt; điện vàng; độc lục tím đục.
- Chính đậm đặc và rõ nhất; phụ (bọt nhỏ, giọt, tro) nhỏ, có thể đặc; phụ **lớn** (khói, màng khiên) phải nhạt hoặc trong hơn.
- Hiệu ứng lên **chính tướng mình** (hồi máu, buff) dùng màu sáng khác tông thân nó, ít hình. Lưỡi sóng xanh đậm phủ lên tướng
  xanh là rối (lỗi đã gặp).
- Vài chấm trắng nhỏ trên mảng đậm làm hình sống hơn: bọt trên lưng sóng, sọc bọt trượt quanh vòi rồng.
- Vòng mảnh có viền mực thì thành vòng đen: vòng mảnh vẽ không viền.

## 5. Hình theo hệ (bỏ màu vẫn phải nhận ra)

| Hệ | Hình chính | Chuyển động | Thay cho khói / tia văng |
|---|---|---|---|
| Hỏa | lưỡi lửa vẽ tay, ngọn quặp 2–3 nhánh | bay lên, liếm, ngọn ngả ngược hướng bay | khói mây cuộn đen → xám + tro; tia văng |
| Thủy | lưỡi sóng mập có mào cuộn; khối liền (sóng, cột, phễu) | chảy, đổ, toé rồi rơi theo trọng lực | bọt trắng; giọt lệ rơi loang vòng; vương miện nước |
| Băng | mảnh nhọn góc cạnh, tinh thể | bắn thẳng, cắm, vỡ vụn | mảnh băng xoay; hơi lạnh mỏng |
| Điện | đường gấp khúc dốc, có nhánh | đổi dáng mỗi khung, chớp tắt | tia lách tách ngắn |
| Thổ | khối đá góc cạnh, vết nứt | trồi lên, rơi nặng, nảy một lần rồi nằm | bụi tròn nhạt; sỏi |
| Mộc | lá, dây leo cong, cánh hoa | mọc, quấn, rơi lượn | lá bay; phấn hoa |
| Kim | lưỡi mảnh, sao bốn cánh, vòng | chém thẳng, loé, đứng yên nhấp nháy | lấp lánh; mảnh kim loại |
| Độc | bong bóng, giọt nhão | sủi, nổ lụp bụp, nhỏ giọt | khói thấp bò ngang |

- **Phép thử hình bóng:** tô đen cả hiệu ứng vẫn phải nhận ra nó là gì. Một phần tử chính (ít nhất 1/4 bề ngang), 2–3 phần tử
  phụ; trong mỗi nhóm có to, vừa, nhỏ; tránh đối xứng.
- Tròn và cong đọc là an toàn (hồi máu, bong bóng, khiên); tam giác và gai đọc là nguy hiểm, tốc độ, hướng; vuông đọc là vững.
- Lửa: dựng bằng nét chữ S, khoét bằng nét chữ C, đỉnh là móc; gốc dày thon dần, luôn đi lên; tránh khối đều.
- Nước: chỉ cạnh tròn; gợn, bong bóng, bọt đi cùng hướng dòng nhưng khác cỡ; càng xa tâm càng vỡ nhỏ. Màn nước toé cao nhất
  ngay đầu, **rách từ đáy**, mỗi mảnh bay theo cung riêng, nhỏ dần, tách vụn rồi mất; giọt không tắt phụt.
- Sét: gai sắc, khung chớp, không cho sét "bò" ngang màn.
- Nét mảnh và sắc đọc là đòn nhanh, xuyên. Mảnh hình học vỡ ra đọc là sóng xung kích. Khối dày viền ổn định đọc là khiên.
- Mép trước của đạn sắc và rõ nhất; đuôi thô, thưa dần.
- **Khối lớn không dựng được bằng hạt rời** (trông như đám bóng bay loạn). Thân vòi rồng, con sóng, lưỡi chém, cột phun là
  **mảng liền**; hạt chỉ làm mép, bọt, giọt (`pokiclash-fx-congthuc` mục 5b, 5c).
- Khối nhẵn thì cứng: chia đoạn và cho lắc lệch pha (vòi rồng = 8 vòng dẹt), cho điểm viền rung nhẹ theo thời gian.

## 6. Bố cục và thang độ quan trọng

- **Thang cỡ:** hạt idle < buff, khiên < đòn thường < chiêu mana < chiêu cuối; dạng 1 < dạng 2 < dạng 3. Chiêu thấp không bao giờ
  to bằng chiêu cuối (bản của Riot chia 6 bậc, bậc cao nhất mới được dải màu rộng nhất và cỡ lớn).
- **Chính – phụ:** phần tử mang tín hiệu trận (đạn, điểm trúng) rõ nhất, viền mực đủ; phần tử phụ nhỏ hơn, thưa hơn.
- **Thưa – dày:** định chỗ tụ, chỗ thưa trước khi rải. Vành hạt nổ rải **đều quanh tâm** như cánh hoa, không dồn cục.
- **Chiều sâu:** vòng dưới chân là elip; nửa xa vẽ sau tướng, nửa gần vẽ trước. Ba lớp: đất, sau tướng, trước tướng.
- **Giới hạn khung:** phía trên đối thủ chỉ còn khoảng một chiều cao tới mép sân; mây, phễu phải tự hạ khi sát mép.
- **Không che:** không che con bị trúng, thanh máu, bảng thẻ. Cỡ hiệu ứng phẳng bằng khoảng nửa cỡ hiệu ứng có quầng sáng tương đương.

## 7. Khớp animation với hiệu ứng

Đây là phần dễ sai nhất và người dùng đã nhắc nhiều lần.

1. **Dựng dáng tướng trước, canh hiệu ứng theo dáng.** Clip có một khung nhả (`hitTimes` trong `.atomik`).
2. **Pha lấy đà của hiệu ứng chạy cùng lúc tướng lấy đà.** Bộ Thủy: `StageView.PreFx` phát hiệu ứng ngay khi clip bắt đầu, truyền
   `lead` = giờ tới khung nhả; nước nhả đúng khung đó. (Bộ Hỏa phát ở khung nhả; chiêu có pha tụ dài nên chuyển sang cách này.)
3. **Tướng giữ dáng nhả tới khi dòng hiệu ứng gần xong** rồi mới về đứng: tia và luồng phun giữ hết dòng; thương, kim giữ tới mũi
   cuối phóng đi; cầu giữ tới lúc rời miệng; mưa, vòi rồng giữ gần hết (`HoldOf`, `HoldNuoc`).
4. **Cảm giác trúng đi theo lúc hiệu ứng chạm đối thủ**, không theo khung nhả: khựng, rung, bật lùi, số sát thương đều chờ đạn tới
   (`impactAt`, `fxHitAt`, `BattlePlayer` chờ `travel`).
5. **Chọn hiệu ứng khớp động tác có sẵn của từng dạng.** Dạng lao tới thì hiệu ứng nổ đúng lúc chạm; dạng gọi trời thì vật rơi từ
   trên; dạng dậm chân thì thứ gì đó trồi lên hoặc lan trên đất. Không ép một hiệu ứng cho mọi dạng.
6. **Clip do lớp hạt lo thì bỏ ảnh hiệu ứng trong clip** và bỏ luôn khai báo `far`, không thì khung camera sticker dời theo, dạng
   nhỏ bị cắt chân.
7. **Miệng, tay, vũ khí:** điểm phát lấy từ `muzzle` của rig; tia phải ra đúng chỗ đó ở cả hai chiều lật.
8. Khựng dừng cả hai con và hiệu ứng của cú đó; đạn đang bay của đòn khác không dừng theo.

Phía animation của cùng chuyện này (dáng, khung nhả, rig để lại chỗ bám): `animation-petclash` mục 6.

## 8. Kiến trúc hiệu ứng trong game

| Tầng | Dùng cho | Ở đâu |
|---|---|---|
| Ảnh trong clip `.atomik` | đòn đánh thường, chuyển động phụ của chính tướng (than ở bờm, mây quanh thân) | `ArtGen/Spine/beast.py` |
| Hạt chồng lớp trên sân | chiêu mana, chiêu cuối, mọi thứ bay giữa hai con | `HatLua.cs` (Hỏa), `HatNuoc.cs` (Thủy) |
| Mảng liền | thân khối lớn: sóng, cột, phễu, lưỡi chém, lõi tia | `HatMang.cs`, gọi `MFill`, `MBand`, `MRibbon` |
| Sân đấu | khựng, rung, chớp màn, bật lùi, chữ nổi, nền sân bừng lên | `StageView.cs` |

- Ba lớp hạt: đất, sau tướng, trước tướng; mỗi lớp một Canvas con; mảng liền là con đầu của lớp (nằm dưới mọi hạt cùng lớp).
- Mỗi hạt mỗi khung trả các nét vẽ (lớp, ảnh, màu, vị trí, cỡ, góc, alpha); các hạt cùng lớp chồng lên nhau thành **một khối có
  một viền mực**: lớp mực vẽ dưới cùng, rồi màu từ ngoài vào lõi.
- Cấu trúc một chiêu: Spawn → Initialize → Update → Output; chiêu = hàm đặt lịch (`At`, `Every`) trả giờ tới lúc trúng.
- Hiệu ứng có thời điểm không đoán trước (phản ứng khi bị đánh, tan khi hết giờ) để thành hạt riêng, không gắn cứng vào dòng chính.
- Chủ đề theo tướng đặt trước khi phát (`UseTheme`); hạt giữ bảng màu lúc sinh.
- Cùng một chiêu phải chạy được ở hai nơi: sân đấu và ô xem trong hộp chi tiết tướng (`HeroViewer`, đích ảo trước mặt).

## 9. Hiệu năng trên điện thoại

Nguồn và số ở `nghien_cuu_hieu_nang.md`. Chưa có số đo trên máy thật của dự án; các mục dưới là hướng kiểm, không phải kết luận.

- Kẻ giết khung hình trên điện thoại là **vẽ đè**: nhiều ảnh trong suốt to chồng nhau. Giảm nửa số hạt thường trông vẫn y vậy.
- Ngân sách đang dùng: mỗi cú trúng ≤ 25 hạt, cả sân ≤ 120 hạt sống, idle ≤ 6 hạt mỗi tướng. Chiêu cuối hiếm nên được phép nặng hơn.
- Thân khối lớn bằng **một mảng liền** rẻ hơn chồng nhiều hạt to.
- Trên uGUI, mỗi lần đổi `Image.color`, cỡ rect, hay bật tắt là dựng lại lưới của Image đó; bật tắt đắt nhất. Nếu đo thấy nặng:
  đổi cỡ bằng `localScale`, nhuộm bằng `canvasRenderer.SetColor`, ẩn bằng scale 0, hoặc gộp hạt của một lớp vào một lưới.
- Lambda cho từng hạt và nối chuỗi tên ảnh mỗi khung đều cấp phát bộ nhớ: tra ảnh bằng chỉ số, dùng hàm vẽ chung khi tối ưu.
- Ảnh hạt: không mipmap, ASTC 6x6, cỡ bằng cỡ lớn nhất hiện trên màn, cắt sát hình. Tên có tiền tố `hat_` để không trùng ảnh Fallback.
- Đo: bản Development trên máy đích, Profiler mục UI (`Canvas.SendWillRenderCanvases`, `BuildBatch`, GC Alloc), Rendering Debugger
  chế độ Overdraw. Ép tải: 6 tướng ra chiêu nặng nhất cùng lúc.

## 10. Quy trình làm một hiệu ứng hoặc một bộ hệ mới

0. **Tra thư viện template** (bảng "Luật đầu tiên" ở đầu file): đưa người dùng xem cái gần nhất, hỏi dùng lại / chỉnh / làm mới;
   chỉ đi tiếp các bước dưới khi người dùng muốn làm mới (2026-11-25).
1. **Đọc hình tướng** sẽ dùng chiêu (màu, họa tiết, dáng) và động tác clip của từng dạng.
2. **Tìm mẫu:** ảnh hiệu ứng đã duyệt của game, Epic Toon FX (`toonfx.md`, chỉ đọc số), Clash of Critters, Kingdom Rush 5 (trang
   xem có lọc theo hệ, soi từng khung; `hoc_kr5_vfx.md`), tài liệu trong thư mục này.
3. **Viết ba pha và danh sách phần tử** (chính, phụ, nhịp, lớp) trước khi viết mã.
4. **Ảnh hạt:** cần hình mới thì gọi GPT vẽ lưới 2 × 2 xám vân chì không viền (`build_hat.py`), nhập, xuất sang Unity (`xuat_hat.py`).
5. **Bản xem trước Python** (`fxlib.py`, `bo_<hệ>.py`): ra GIF và tờ 12 khung trên nền sân thật với hai tướng thật.
6. **Soi tờ khung ít nhất 3 vòng**, sửa lỗi tệ nhất trước. Đếm "đủ phần tử" không thay được việc xem.
7. **Người dùng xem GIF** (`chuan_fx/<bộ>/xem.html`, mở bằng Edge qua `file:///`).
8. **Chuyển sang C#**, gắn vào bảng chiêu theo tướng và theo dạng, đặt giờ giữ dáng.
9. **Rig:** bỏ ảnh hiệu ứng trong clip do hạt lo, dựng lại `.atomik`.
10. **Tour chụp trong Unity** (báo các phiên khác trước khi biên dịch hoặc Play), soi tờ khung từng tướng từng dạng.
11. **Test EditMode**, rồi thử trên Android. Chỉ chạy trong Editor thì chưa xong.
12. **Ghi công thức và lỗi đã gặp** vào `pokiclash-fx-congthuc`.

## 11. Bảng kiểm trước khi báo xong

- [ ] Nhìn một cái là hiểu chuyện gì xảy ra, ai đánh ai?
- [ ] Đủ ba pha; pha tụ khớp lúc tướng lấy đà; nhả đúng khung nhả; tan không cụt, không giật?
- [ ] Tướng giữ dáng tới khi dòng hiệu ứng gần xong; đối thủ chỉ giật khi hiệu ứng chạm tới?
- [ ] Bỏ màu vẫn nhận ra hệ? Tô đen cả hiệu ứng vẫn nhận ra hình? Hình hợp nét tranh của chính tướng đó?
- [ ] Tối đa ba sắc, một màu chủ đạo, đúng màu hệ và màu tướng?
- [ ] Không quầng sáng, không cộng sáng, không gradient, không bóng?
- [ ] Không che con bị trúng, thanh máu, bảng thẻ; không vượt mép sân? Chớp màn không quá 3 lần mỗi giây?
- [ ] Cỡ đúng thang: đòn thường < mana < chiêu cuối; dạng sau to hơn dạng trước?
- [ ] Các phần tử so le, không cùng bật cùng tắt; không đường cong tuyến tính?
- [ ] Đỉnh tới trong 0,1 s đầu của pha nhả? Tan bằng vỡ ra (khói tách cụm, nước vỡ giọt, lửa teo thành đốm) rồi mới mờ? Đòn đánh
  xuống đất có báo trước trên đất? (so mẫu Kingdom Rush 5, `hoc_kr5_vfx.md`)
- [ ] Chạy đúng ở cả hai chiều bắn và trong ô xem của hộp chi tiết tướng?
- [ ] Số hạt trong ngân sách; không có ảnh to chồng nhau nhiều lớp?
- [ ] Đã tự xem từng khung chụp trong Unity; test EditMode qua; đã thử Android (hoặc nói rõ là chưa)?

Chấm điểm định lượng (7 nhóm, 20 chỉ tiêu, tổng dưới 85 phải sửa): `VFX_KNOWLEDGE_BASE.md` mục 10.2.

## 12. Công thức mẫu cho game pet, đã đổi sang nét của dự án

| Việc | Cách làm |
|---|---|
| Trúng đòn thường | chớp sao gai màu kem 1–2 khung tại điểm chạm; 3–6 tia văng; vòng mỏng; chớp `_Flash` trên thân 2–4 khung; tối đa hai sắc |
| Chém | mảng trăng khuyết liền, mép trước sắc có dải nhạt, vệt mờ phía sau; tướng lùi vũ khí trước khi chém |
| Chiêu hệ lớn | hạt hút vào tâm + vòng co → chớp, vành hạt toả đều, mảnh theo hệ, rung → khói hoặc bọt tan ngắn |
| Hồi máu, buff | nhịp chậm dưới 60 nhịp/phút; hạt nhẹ bay lên, vòng dâng từ chân lên đầu (nửa sau vẽ sau tướng); màu sáng khác tông thân |
| Khiên | vành dày viền ổn định, màng trong alpha 0,2, phập phồng 2–3%; bị đánh thì loé nhẹ bằng hạt riêng |
| Trạng thái | hạt lặp nhỏ theo pha (bong bóng độc, tinh thể băng, tia điện lách tách), nối vòng liền; nhuộm thân bằng màu hệ nhạt |
| Tiến hóa | dài vì là phần thưởng lớn: thân trắng dần thành hình bóng, hạt hút vào, vòng xoay nhanh dần → hình kem che kín dáng, sóng toả → dạng mới bật ra 0,9 → 1,05 → 1,0, aura màu hệ → lấp lánh rơi, về idle dạng mới. Mốc: Pokémon Emerald khoảng 13 s cho cả cảnh; clip của dự án 2,8 s |
| Chết | chớp cuối → mờ dần kèm vài hạt màu hệ bay lên |

Công thức đã làm thật (lửa, nước) và lỗi đã gặp: `pokiclash-fx-congthuc`.

## 13. Lỗi hay lặp lại

- Làm hiệu ứng bằng một ảnh tĩnh trượt đi. Sét, lửa, nước là **chuyển động**.
- Khói vụt tắt hoặc giật: phải co nhỏ dần và bay lên tới hết.
- Nổ đạt đỉnh chậm (nở dần trong 0,3 s) hoặc chỉ mờ đi tại chỗ: mẫu Kingdom Rush 5 chớp 1 khung, khói và lửa to gần đủ ngay
  khung 2, nửa sau là tách cụm, bay lên, nhỏ dần (`hoc_kr5_vfx.md`).
- Hiệu ứng giật, ít khung (giữ khung, nhảy hình cụt): người dùng muốn mượt (2026-11-19, mục 1c). Hạt đổi hình mỗi khung hoặc chồng mờ
  sang hình kế; tờ khung toé / nổ 12–20 khung.
- Dựng khối lớn bằng hạt rời; hoặc dựng thành một khối nhẵn cứng.
- Hiệu ứng lửa, nước chung chung, không hợp nét của tướng đang ra chiêu.
- Tướng về đứng trong khi luồng phun còn chạy.
- Đối thủ giật lùi lúc tướng vừa nhả, trước khi đạn tới.
- Thân hiệu ứng đặt sau đối thủ nên bị che hết; hoặc đặt trước mà đặc quá nên che đối thủ.
- Hiệu ứng lên mình cùng tông với thân tướng.
- Chỉ đếm prefab, không tự xem ảnh chụp; chỉ xem tờ khung mà nói như đã xem chuyển động.
- Nước, lửa, khói nền làm bằng ảnh trượt ngang: phải là hình tự biến dạng (dâng, cuộn, tan) tại chỗ.

Lỗi của phần animation (rig, lưới, chuỗi xương, miệng): `animation-petclash` mục 8.

## 14. Nguồn tham khảo đã mổ

| Nguồn | Xem ở đâu | Lấy gì | Không lấy |
|---|---|---|---|
| **Kingdom Rush 5** (đục 2026-11-18) | `hoc_kr5_vfx.md`; trang xem `ArtGen/ThamKhao/KR5/MO_WEB.bat` (lọc theo hệ, tua từng khung, hệ hạt chạy đúng code game) | đỉnh khung 1–3, hình từng pha của nổ, lửa, nước, khói, chuỗi mảnh của một đòn, hạt dập hình tự tan | hình (bản quyền Ironhide), nhịp "giữ 2 khung" (dự án muốn mượt) |
| **4 gói VFX vector hoạt hình** người dùng gửi (2026-11-19) | mục 1c; `ArtGen/StyleRefs/vfx_mau/` | **style đích** của lửa, nước, nổ, khói, năng lượng: không viền, 3–4 tông + mảng sáng, nước chuyển màu, lửa có quầng mềm; tờ khung nhiều khung (nước 16, nổ 9) | chép nguyên hình vào game khi chưa rõ giấy phép |
| **Clash of Critters** (đục 2026-11-09) | `pokiclash-hero-fx` mục 1b | mỗi cú trúng 3–4 lớp, lớp phụ trễ 0,15 s, 2 đợt hạt cách 0,1 s, cỡ bật 14% đời | quầng sáng, hình |
| **Epic Toon FX** (Asset Store, `.gitignore`) | `pokiclash-hero-fx/toonfx.md` (công cụ đọc số `tools/ps_*.py`) | phân vị đời, tốc, cản; tờ khung ăn mòn; màu theo tuổi = nhiệt độ | ảnh, prefab |
| **pixelfx** (MIT) | `pokiclash-hero-fx` mục 1, 6 | 12 kiểu hạt có vật lý, cách diễn quanh hiệu ứng | pixel art, lớp sáng cộng dồn |
| **Anime Style FX Workflow** (CodyWinch, 11 file `.blend` + 4 file lốc xoáy, người dùng mua 2026-11-24) | `blender_anime_fx.md`; file ở repo AtomSpine `refs/blender_anime_fx/` (công cụ đọc / render thử trong `tools/`) | chuỗi texture → trọng số đỉnh → Displace + Mask + Smooth; lớp vỏ màu phẳng lột dần theo ngưỡng; núm Empty + driver; Warp, Curve, Lattice, Surface Deform, Simple Deform Twist | bloom Eevee, Filmic; phát hành lại file |
