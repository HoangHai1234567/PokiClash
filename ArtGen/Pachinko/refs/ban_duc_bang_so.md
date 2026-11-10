# Clash of Critters 0.51.1 — Bảng số LED, thanh cấp, icon bay, ánh sáng máy pinball (số đo)

Nguồn: `D:\Ripper\ClashOfCritters\AssetRipper_Export\ExportedProject\Assets\AssetBundles\<hash>\...` (dưới đây ghi đường dẫn bỏ phần `AssetBundles/<hash>/`). Chỉ đọc YAML (prefab, anim, mat, png). Logic Lua mã hoá, nên phần "ai gọi clip nào, lúc nào" là suy luận từ tên + cấu trúc, ghi rõ chỗ suy luận.

Quy ước đơn vị:
- Mặt máy là **world-space SpriteRenderer** (không phải uGUI): prefab `Res/Runtime/Pinball/Prefab/Table/pbsc_pinball_table_01.prefab` → con `pbsc_pinballtable_background_01` (bản riêng `Res/Pinball/Prefab/Table/pbsc_pinballtable_background_01.prefab`). Sprite PPU = 100, nền máy `txsc_pinball_bg.png` 1334×1875 px = 13.34 đơn vị; UI canvas cũng chuẩn 1334 rộng ⇒ **1 đơn vị world = 100 px thiết kế**. Khi dựng lại bằng uGUI cứ nhân 100.
- Clip ghi `t:giá trị`, thời gian giây. `~a/b` = tiếp tuyến vào/ra (khác 0 ⇒ cong), `~step` = bậc thang (IsActive). Không ghi = tuyến tính/phẳng (tiếp tuyến 0, tức ease in-out kiểu Unity "auto/flat").
- `m_StopTime` của AssetRipper luôn = 1 nên **độ dài thật = mốc cuối (maxkey)**, ghi ở cột "dài".
- Màu (r,g,b,a) 0–1.

---

## 1. Bảng điểm / bảng số LED (scoreboard)

### 1.1 Vị trí và cấu trúc

Đường dẫn trong prefab bàn: `pbsc_pinball_table_01/anim/background/pbsc_pinballtable_background_01/pbsc_pinball_light_top/Background_scorebord`.

| Nút | Vị trí local | Scale | Thành phần | Ghi chú |
|---|---|---|---|---|
| `pbsc_pinball_light_top` | (-0.01, 0.13) | 2 | Animation: `anfx_background_shine_group_level_1/2/3`, `anfx_background_launch_prompt_in/out`; AnimationController | Nhóm "đèn" của cả máy. Clip level_1/2/3 chỉ đặt tham số shader, không có keyframe chạy; theo `AnimationController` chúng là trạng thái máy `idle` / `card` / `event` (xem 1.6b, 3.2), không phải cấp máy. |
| └ `Background_scorebord` | (-0.009, 2.67) | 0.5 (net 1) | SR `txsc_pinball_bg_scorebord.png` (577×178), mat `mtvx_background_shine_scoreboard_combine`, order 9; Animation `anfx_background_scorebord_hit` | Khung bảng LED. Tâm world y = 0.13+2×2.67 = **5.47 đv ≈ 547 px trên tâm bàn**, rộng **577×178 px**. |
| ── `pbvx_pinball_result_board_collect_01` [tắt sẵn] | 0 | (1,1,2) | EffectLifeCycleData, BattleEffectHelper | Hiệu ứng "thu" số (LED vọt lên). |
| ──── `fx_glow` | (0.021, 0.127) | (0.917, 0.963) | SR `txsc_pinball_bg_scorebord_light_05.png` (448×130), mat `mtvx_background_trigger_get_glow_06` (additive), màu (0.95,0.461,0.087), order 20; Animation `anfx_background_scorebord_hit01` | Viền sáng quanh màn LED ≈ 411×125 px. |
| ────── `fx_glow01` [tắt] | 0 | 1 | như trên | lớp sáng phụ |
| ────── `fx_r01…fx_r05` [tắt] | (0.032, 0) | (0.75, 0.7) | SR `txsc_pinballtable_electronic_03…07.png` (512×128), mat `..._get_glow_07` (additive), order 10; r02 màu (1,1,1,0.51), r03 màu (1,0,0,0.51) | 5 khung hình LED "phun" (xem 1.4). Cỡ hiện ≈ 384×90 px. |
| ── `pbvx_pinball_result_board_out_04` [tắt sẵn] | 0 | (1,1,2) | EffectLifeCycleData, BattleEffectHelper | Hiệu ứng "nổ"/gợn LED khi ra kết quả. |
| ──── `fx_glow_1` | (0.021, 0.127) | (0.917, 0.963) | SR light_05, mat `_get_glow_06`, màu (1,0.509,0.129); Animation `anfx_background_scorebord_hit02` | |
| ────── `fx_r_tl` | (0,-0.038) | (0.9, 0.608) | SR + `UIFlipbookController` (isLoop 0, mat `mtvx_pinballtable_electronic_01`) | Flipbook 16 khung LED (xem 1.5). |
| ────── `fx_r01` | 0 | 0.186 | SR `..._light_09.png` (560×426) | vòng chấm LED nhỏ ≈ 104×79 px |
| ────── `fx_r02` / `fx_r03` | (0,-0.016) | 0.188 / (0.230,0.188) | SR `..._light_010.png` (1037×558) | ngoặc chấm 2 bên ≈ 195×105 / 239×105 px |
| ────── `fx_r04/05/06` (mỗi cái 2 con `_1`, `_2` đối xứng, scale x âm) | x = ±1.066 / ±1.175 / ±1.251 (nhân scale cha ≈ ±98 / ±108 / ±115 px) | 0.235 | SR `..._light_011/012/013.png` (261×537) | 3 cặp ngoặc chấm dời dần ra ngoài |
| `shine_level_down_combine` (anh em của scorebord) | (0, 0.464) | 0.5 | SR `txsc_pinball_bg_dark_2.png` (637×912), mat `mtvx_background_shine_level_down_combine`, order 0 | Lớp tối/đèn chạy phía dưới mặt máy. |
| `txt_score` (con của background, **[tắt]**) | RectTransform (0, 5.6), 3.49×1.3 | 1 | TextMeshPro (world) "0", font `txui_font_pinball_number` (sprite font), fs 7 (auto 4–7), căn giữa, mat `zh_cn_body_special_gold_light_01` | Chỗ chữ số trên bảng LED: y = 5.6 đv (sát tâm bảng 5.47), khung chữ **349×130 px**. Prefab để tắt; Lua bật/ghi số. |

Ảnh nguồn (chỉ mô tả hình):
- `txsc_pinball_bg_scorebord.png` 577×178, nền trong suốt: khung bo tròn dài màu vàng cam có **26 bóng đèn chấm** chạy quanh viền (≈ 10 trên, 10 dưới, 3 mỗi bên), lòng màn hình đỏ sẫm có lưới chấm LED nhỏ, hai bên là hai ống/khớp xanh dương có nắp đỏ, dải đế xanh đậm bên dưới. Có viền nâu sẫm.
- `light_03.png` 404×136: **chỉ các quầng sáng vàng** của 26 bóng (tất cả sáng), trong suốt — làm `_ShapeTex`.
- `light_04.png` 404×136: cùng bố cục nhưng **bóng xen kẽ**: một bóng sáng quầng vàng, một bóng chấm xám tối — làm `_FlashTex` (bản đồ nhấp nháy, xem 3.x shader FlashTex). ⇒ đèn chạy viền là 2 nhóm bóng sáng luân phiên.
- `light_05.png` 448×130: chỉ một đường viền chữ nhật bo góc trắng mảnh (quầng nhẹ) — viền sáng màn LED, tô màu bằng vertex color.
- `light_09.png` 560×426: khối chấm LED hình vòng (bánh rán) màu vàng có quầng cam, lỗ giữa.
- `light_010.png` 1037×558: hai ngoặc chấm LED vàng `( )` trên nền cam đặc (khối sáng dày, không trong suốt ở giữa).
- `light_011/012/013.png` 261×537: một ngoặc chấm LED `)` dọc 4 cột chấm, quầng cam mềm (3 bản hơi khác độ cong).
- `txsc_pinballtable_electronic_03…07.png` 512×128: chấm LED vàng/cam tạo hình **kim tự tháp phun lên** (03), to hơn (04), **tách sang hai góc trên** (05), (06), chỉ còn hai góc trên (07). Quầng đỏ hồng mềm quanh chấm. Nền trong suốt.

### 1.2 Đèn chấm viền bảng (đèn chạy) — material `mtvx_background_shine_scoreboard_combine`

`Art/UI/Materials/pinball/mtvx_background_shine_scoreboard_combine.mat`, shader `UEP/Interface/FlashTex(Combine)` (thân shader bị strip, chỉ còn khai báo; nghĩa tham số lấy từ chú thích tiếng Trung trong Properties):

| Tham số | Giá trị mặc định (mat) | Nghĩa |
|---|---|---|
| `_ShapeTex` | light_03, ST (1.428, 1.309, -0.218, -0.225) | hình đèn (mọi bóng) — ST co về giữa ⇒ 404×136 phủ đúng vùng bóng trong sprite 577×178 |
| `_FlashTex` | light_04, cùng ST | bản đồ nhấp nháy (bóng nào sáng theo nhịp) |
| `_FlashColorMode` | 1 (dùng màu đơn) | |
| `_MainColor` | (1, 0.714, 0.406) | màu nền đèn (cam nhạt) |
| `_FlashColor` | (1, 0.886, 0.381) | màu lúc chớp (vàng) |
| `_FlashPower` | 22.7 | cường độ chớp |
| `_TimeSpeed` | 0.2 | tốc độ thời gian |
| `_TimeOffset` | 2.07 | lệch pha |
| `_SpaceTime` | 1.2 | khoảng cách giữa các đợt |
| `_FlashRange` | 0.4 | độ rộng khối chớp |
| `_FlashSmooth` | 0.001 | mép khối chớp (≈ cứng, bật/tắt gọn) |
| `_FlashRegionAmount` | 1 | số khối chớp |
| Blend | AlphaBlend (Src 5 / Dst 10) | |

Clip trạng thái máy idle/card/event (`Art/Fx/Animation/anfx_background_shine_group_level_*.anim`, chỉ 1 mốc t=0, đặt tham số cho `Background_scorebord`):

| Cấp | `_TimeSpeed` | `_FlashRange` | `_FlashSmooth` | `_FlashRegionAmount` | `_SpaceTime` | `_TimeOffset` | `_FlashPower` |
|---|---|---|---|---|---|---|---|
| level_1 | 0.45 | 0.2 | 0.01 | 0.6 | (giữ 1.2) | 1 | (22.7) |
| level_2 | 1.2 | 0.2 | 0.05 | 1 | 1 | 1 | (22.7) |
| level_3 (wrap=2 loop) | 1 | 0.25 | 0.02 | **4.66** (nhiều khối chạy cùng lúc) | (giữ) | 1.11 | 5 |

Đọc ra nhịp: cấp 1 một khối chớp chạy chậm (chu kỳ ≈ SpaceTime/TimeSpeed ≈ 2.7 s); cấp 2 nhanh gấp ~2.7 lần (≈ 0.8–1 s/vòng); cấp 3 có ~4–5 khối chạy cùng lúc, mép cứng. Hiệu ứng nhìn: bóng xen kẽ bật/tắt chạy quanh khung. Dựng lại: 2 nhóm Image bóng (chẵn/lẻ) + quét một "khối sáng" chạy theo chỉ số bóng, hoặc đơn giản nhấp nháy luân phiên chẵn/lẻ mỗi ~0.25–0.4 s (cấp 1), nhanh dần theo cấp.

### 1.3 Clip "nảy" khung bảng khi cộng số — `anfx_background_scorebord_hit`

`Art/Fx/Animation/anfx_background_scorebord_hit.anim` (60 fps) — gắn trên `Background_scorebord`, chạy mỗi lần bảng nhận số (suy luận từ tên "hit").

| t | localPosition y | (= px, nhân scale cha 2 ×100) |
|---|---|---|
| 0 | 2.670 | 0 |
| 0.033 | 2.689 | **+3.8 px** |
| 0.067 | 2.670 | 0 |
| 0.083 | 2.670 | (giữ) |

⇒ Khung bảng **giật lên 3.8 px trong 2 khung hình rồi về trong 2 khung** (tổng 0.083 s). Không có scale, không đổi màu khung.

### 1.4 "Thu" số lên thanh cấp — `pbvx_pinball_result_board_collect_01` + clip `anfx_background_scorebord_hit01`

Prefab `Res/Fx/Prefab/Ui/pbvx_pinball_result_board_collect_01.prefab` (bản gắn sẵn [tắt] trong bàn). Clip `Art/Fx/Animation/anfx_background_scorebord_hit01.anim` (60 fps) trên `fx_glow`, dài **0.65 s**, cuối có **Animation Event t=0.65 `OnAnimationEvent("scorebord_hit01")`** ⇒ Lua dùng sự kiện này để cho số bay lên thanh cấp/cộng EXP (suy luận).

Viền sáng `fx_glow` (light_05, additive) — nhấp nháy 3 lần:

| t | 0 | 0.1 | 0.167 | 0.283 | 0.35 | 0.467 | 0.533 | 0.65 |
|---|---|---|---|---|---|---|---|---|
| alpha | 0 | 0 | **1** | 0 | **1** | 0 | **1** | 0 |
| màu | (0.95,0.46,0.087) | (1,0.524,0) | (0.95,0.46,0.087) | (1,0.524,0) | … | | | |

`fx_glow01`: alpha 0 → 0.459 (t 0.067) → 0 (0.233) → 0.459 (0.3), màu (0.95,0.46,0.087).

Chuỗi khung LED "phun lên" (bật/tắt bậc thang, mỗi khung **≈ 0.083 s = 5 frame@60**), chạy **2 lượt**:

| Khung | Lượt 1 bật | Lượt 1 tắt | Lượt 2 bật | Lượt 2 tắt | alpha |
|---|---|---|---|---|---|
| r01 (electronic_03, kim tự tháp thấp) | 0.067 | 0.15 | 0.30 | 0.383 | 0 → 0.51 (đi lên trong lúc bật) |
| r02 (04, kim tự tháp cao) | 0.15 | 0.233 | 0.383 | 0.467 | 0.314 |
| r03 (05, tách hai góc, màu đỏ (1,0,0)) | 0.233 | 0.333 | 0.467 | 0.533 | 0.314 |
| r04 (06) | 0.333 | 0.417 | 0.533 | 0.60 | 0.314 → 0.235 |
| r05 (07, chỉ còn góc trên) | 0.417 | 0.467 | 0.60 | 0.65 | 0.235 → 0 |

⇒ Nhìn: chấm LED dồn từ đáy màn lên đỉnh rồi tràn ra hai góc trên (hướng lên thanh cấp nằm phía trên), lặp 2 lần, kèm viền màn chớp 3 lần; hết 0.65 s thì phát event cho số bay đi.

### 1.5 "Nổ"/gợn LED — `pbvx_pinball_result_board_out_04` + `anfx_background_scorebord_hit02` + flipbook

Clip `Art/Fx/Animation/anfx_background_scorebord_hit02.anim` (60 fps), dài **0.933 s**:

| Nút | bật | tắt | Hình |
|---|---|---|---|
| fx_r01 | 0.067 | 0.133 | vòng chấm nhỏ (light_09) |
| fx_r02 | 0.133 | 0.20 | ngoặc ( ) hẹp (light_010) |
| fx_r03 | 0.20 | 0.267 | ngoặc ( ) rộng hơn |
| fx_r04 | 0.267 | 0.333 | cặp ngoặc ±98 px |
| fx_r05 | 0.333 | 0.40 | cặp ngoặc ±108 px |
| fx_r06 | 0.40 | 0.483 | cặp ngoặc ±115 px; alpha 1 → 0 trong 0.433–0.483 |

⇒ Gợn LED lan từ giữa ra hai mép, **mỗi bước 0.067 s (4 frame@60)**, 6 bước.

Viền `fx_glow_1` (light_05): alpha 0.392 → **0.926** (0.217) → 0.392 (0.467) → 0.926 (0.683) → **0** (0.933); màu dao động (0.95,0.46,0.087) ↔ (1,0.524,0) cùng nhịp (chu kỳ 0.467 s).

Flipbook `fx_r_tl`: material `Art/UI/Materials/pinball/mtvx_pinballtable_electronic_01.mat`, shader `UI/Uep/PGameCustom/UIFlipBook`: `_Texture = txsc_pinballtable_electronic_01.png` (2048×2048), `_FlipbookConfig = (3, 6, 1, 0)` ⇒ lưới **3 cột × 6 hàng, dùng 16 ô**, `_Speed = 15` fps, `_Loop = 0`, `_Blend = 2` (cộng, Src 5 / Dst 1 — nền đen = trong suốt). Thời lượng ≈ 16/15 = **1.07 s**, chơi một lần. Nội dung 16 khung (nền đen): khối LED tròn vàng-cam nhỏ → to dần → tách thành hai ngoặc + một khối giữa → khối giữa phình thành thanh dài đầy màn → tách đôi → nảy khối tròn giữa → cuối cùng vỡ thành hạt kim cương đỏ/xanh lấp lánh rồi tắt. (Ô khung ≈ 682×341 px; trong ảnh có màu xanh lá/đỏ/xanh dương ở mép là mã kênh, không phải màu hiển thị chính.)

### 1.6 Chữ số trên bảng và chữ "+N" bật lên

Không có clip "đếm số" nào (không key `m_text`); con số tăng dần do Lua ghi text từng khung. Các prefab chữ liên quan:

**a) `Res/UI/Prefabs/DemoPinball/pbui_pinball_score.prefab`** (uGUI, có lẽ phủ đúng chỗ bảng LED hoặc góc trên phải):
- gốc anchor (1,1), pos (-101.8, -176.2), size 200×80;
- `img_bg` 600×240 scale 0.3 (= 180×72 hiện), Image sliced, không sprite;
- `txt_num` "9999", căn phải (pivot 1,0.5, pos -36), scale 3.333 (bù lại scale 0.3 của cha ⇒ chữ cỡ thật **64**), TMP `zh_cn_body`, mat `zh_cn_body_special_gold_light_01` (mặt chữ vân vàng `txvx_fonts_material_gold_02`, viền đen 0.6, FaceDilate 0.6, glow ngoài 0.05), màu (1, 0.973, 0.775);
- `popup_pos` (2.6, 30) — chỗ sinh chữ "+N".

**b) `pbui_pinball_add_impact.prefab`** — chữ "+1" bật ra trên bảng mỗi lần cộng. Clip `AnimationClip/anui_pinball_add_impact.anim` (30 fps), dài **0.567 s**:

| t | 0 | 0.1 | 0.167 | 0.233 | 0.367 | 0.467 | 0.567 |
|---|---|---|---|---|---|---|---|
| scale gốc | **0** | **1.513** | 0.752 | 0.889 | (giữ 0.889) | | |
| anchoredPos.y | 0 (tiếp tuyến 271 ⇒ bắn nhanh) | | 32.3 (tiếp 107) | | | **41.2** | |
| txt alpha | 1 | | | | 1 | | **0** |

TMP fs 38, mat gold_light_01, màu (1,0.973,0.775). ⇒ Bật từ 0 vọt quá 1.51 trong 0.1 s, nén về 0.75, nảy 0.89; trôi lên 41 px (nhanh đầu, chậm cuối); mờ dần 0.367→0.567.

**c) `fxpb_demo_pinball_number.prefab`** (bản demo cũ "+50") — clip `AnimationClip/fxan_demo_pinball_number.anim` (30 fps):

| t | 0 | 0.067 | 0.133 | 0.6 | 0.667 | 1.23 |
|---|---|---|---|---|---|---|
| fontSize | 20 | **70** | 50 | 50 | 10 | 10 |
| pos.y | 0 (tiếp 331) | | | **71** | | |
| active | 1 | | | | 0 (tắt) | |

**d) `pbui_pinball_add_money.prefab`** (số tiền + icon kẹo bay lên, dùng chung kiểu "cộng"): `group_money` 427×38, `txt_num` fs 38 mat gold_light_01, `img_icon` 50×50 `txui_item_candy_one.png` đặt bên trái chữ (pivot 1,0.5). Các clip (`Art/UI/Animation/PinBall/`):

| Clip | scale group_money | pos.y | khác |
|---|---|---|---|
| `anui_pinball_add_money` (dài 0.6 s, hạt tới 1 s) | 0:0.3 → 0.067:**1.5** → 0.167:1 → 0.5:1 → 0.6:0.3 | 0.133:0 (tiếp 288) → 0.533:**54** | tắt ở 0.6; hạt `pbvx_rob_earnings_particles` bật 0.033–1.0 |
| `anui_pinball_add_money_02` | như trên | như trên | không hạt |
| `anui_pinball_add_money_long` (1.4 s) | 0:0.3 → 0.2:1.5 → 0.9:1.5 → 0.967:1 → 1.3:1 → 1.4:0.3 | 0.3:-5.4 → 0.5:5.3 → 0.833:5.3 → 0.933:0 (tiếp 288) → 1.333:54 | hạt 0–1.8 |
| `anui_pinball_camp_out` (60 fps, 1.08 s) | 0:0.5 → 0.05:1.3 → 0.15:1 → 1:1 → 1.083:0.4 | 0:0 (tiếp 183) → 1:61.3 | |

Bản `_big`: group_money scale 1.5 sẵn.

### 1.7 Chuỗi sự kiện bảng số (tổng hợp, suy luận thứ tự)

1. Bi rơi vào ô kẹo → ô sáng (mục 2) → số kẹo cộng vào bảng: Lua tăng text trên bảng (đếm dần), mỗi lần cộng chạy `anfx_background_scorebord_hit` (khung giật +3.8 px, 0.083 s) và sinh `pbui_pinball_add_impact` "+N" tại `popup_pos` (0.567 s).
2. Hết lượt bi (bảng "chốt kết quả"): bật `pbvx_pinball_result_board_out_04` (gợn LED 0.48 s + viền chớp tới 0.93 s + flipbook LED 1.07 s). Có thêm `pbvx_pinball_result_board_out_01/02/03` là hạt flash ngoài bảng (mục 3.4) theo độ lớn kết quả.
3. Bật `pbvx_pinball_result_board_collect_01` (LED phun lên 2 lượt + viền chớp 3 lần, 0.65 s) → event `scorebord_hit01` → số bay lên thanh cấp (icon/hạt bay — mục 2) → thanh cấp chạy fill (1.8).

### 1.6b Bổ sung: chữ số thật trên bảng LED là `txt_score` + sprite font

Trong `pinball_serialized_dump.txt`, `BackgroundController` (gốc `pbsc_pinballtable_background_01`) có:
- `scoreTextController` → `TextController` trên **`txt_score`** (`text` = TMP world, `isSpriteFont 0`, `minFigure 0`, **`namePrefix: h`**);
- `addScoreAnimation` → Animation của `Background_scorebord` (clip `scorebord_hit`, mục 1.3);
- `backgroundAnimationController` → AnimationController trên `pbsc_pinball_light_top`, khoá `idle` / `card` / `event` / `prompt_in` / `prompt_out` = clip level_1 / level_2 / level_3 / launch_prompt_in / launch_prompt_out. ⇒ "level_1/2/3" thật ra là **trạng thái máy: thường / đang ra thẻ / đang sự kiện** (đèn nhanh dần).

`txt_score` dùng `m_spriteAsset` = `Res/UI/Fonts/txui_font_pinball_number.asset` (atlas `txui_font_pinball_number.png`, mỗi glyph ≈ 29–43 × 54–56 px). Atlas có **2 bộ chữ**: tiền tố `c` = chữ cam-vàng viền nâu đậm; tiền tố `h` = chữ **xanh dương → tím** (gradient dọc) viền sáng. Mỗi bộ gồm `0–9`, `B K M T W` (hậu tố số lớn) và `万/亿` giản thể (`wanj`, `yij`) + phồn thể (`wanf`, `yif`). Bảng LED dùng bộ **`h`** (TextController ghép sprite theo tên `h0…h9`). ⇒ **Số trên bảng = chữ sprite xanh-tím cao ≈ 55 px gốc, khung 349×130 px, căn giữa, rút gọn K/M/B/T**. Đếm tăng dần do TextController/Lua ghi text từng khung (không có clip đếm).

### 1.8 Thanh cấp (EXP bar) phía trên bảng

Prefab `Art/UI/Prefabs/Pinball/pbui_pinball_level_bar.prefab`, dùng trong `Res/UI/Prefabs/Common/pbui_pet_level_exp_view.prefab` (nạp vào nút `pbui_pet_level_exp` của `Res/UI/Prefabs/DemoPinball/pbui_a_view_pinball_mainview.prefab`).

Cấu trúc (uGUI, neo đỉnh màn, cao 105 px, rộng = màn − 23 px):

| Nút | Rect | Hình / mat | Ghi chú |
|---|---|---|---|
| `pbui_pinball_level_bar` | anchor (0,1)–(1,1), pos (5.8,-7), size (-23,105), pivot (0.5,1) | CanvasGroup | |
| `pbui_common_slider` (Slider) | pos (18,3), size (-80, **66**) | | Thanh cao 66 px. |
| `#Background_2` | full | `txui_common_bg_round_32` sliced, màu (0.153,0.204,0.322), mat `battle_popup_water` (UI/Default + tex) | Nền xanh đen bo tròn. |
| `#Background` | inset 1.5 px | `txui_common_bg_round_32`, màu (0.099,0.118,0.16), mat `mtui_pattern_dot_full_chess_mask _prograss_1` (ShapeFlow, chấm caro) | Lòng rãnh tối có hoa văn chấm mờ. |
| `Fill` | inset 5 px mỗi bên | `txui_mainview_bg_round_corner` sliced, màu vertex (0.503,0.856,0.896), mat **`mtui_pattern_strip_orange`** | Phần đầy. |
| `Fill/#anim/particle` | neo mép phải fill, pos (35,0) | UIParticle scale 10 ([tắt], clip `grow_b` bật) | Hạt ở đầu thanh lúc tăng. |
| `Fill/#anim/pos` (CanvasGroup α 0) | neo mép phải fill, pos (50,0) | | Đầu sáng của thanh. |
| └ `bg1` | 61×180, pos (-52.4,0), scale (0, 0.8) | `txvx_pinball_slider_fill_glow_01.png` (60×128, quầng trắng mềm dọc), mat `txvx_pinball_slider_fill_glow_01` (cộng Src5/Dst1) | Quầng dọc ở mép đầu thanh. |
| └ `bg2` | 76×53, pos (-51.2,0), pivot (0.76,0.5), scale (0.4,1) | `txvx_pinball_slider_fill_glow_02.png` (64×44, quầng trắng mềm) | Lõi sáng đầu thanh. |
| `img_level_bg_animation` | 112×111 tại x 37.9 (mép trái), scale 1.04 | `txui_pinball_level_bg` (atlas) + Animation `anui_common_fly_item_hit` | Huy hiệu cấp bên trái — **đích của icon bay**. |
| `num_level` | 62×50 tại (40,1) | TMP "1" fs 40 + `UIShadow` đen (0,-2) | |
| `num_exp` | tại x 96 | TMP "10/30" fs 29 | |
| `group_small_level/pbui_small_level_template` | 58×55 | icon hệ `txui_common_pet_element_fire.png` 80×80 ×0.85, `txui_pinball_level_small_01`, mũi tên `txui_common_element_up` 36×33 | Mốc nhỏ trên thanh. |

Material vằn của Fill — `Art/UI/Materials/mtui_pattern_strip_orange.mat`, shader `UEP/Interface/ShapeFlow` (vẽ hoa văn bằng toán, không texture): `_Strip=1` (sọc), `_CellSize=30`, `_StripWidth=0.512`, `_Rotation=35°`, `_FlowDir=-54`, `_Speed=0` (**sọc đứng yên**), `_SizeScaler=1.64`, `_FillRate=0.086`, `_SmoothStepValue=0.01`, `_BackgroundColor=(1,0.741,0.252)` (cam vàng), `_PointColor=(1,0.843,0.149)` (vàng). ⇒ Fill là **sọc chéo 35° vàng/cam, ô 30 px, sọc ~51%, không cuộn**; màu vertex (0.503,0.856,0.896) nhân vào (Lua có thể đổi màu theo hệ).

Material quầng đầu thanh `Art/UI/Materials/pinball/txvx_pinball_slider_fill_glow_01.mat` (UIDefaultEx biến thể chấm): `_Dot=1`, `_CellSize=10`, `_BreathParam=(60,0,1,1)` (thở/nháy nhanh), `_FillRate=0.5`, `_PointColor` trắng, cộng.

Clip trạng thái đầu thanh (`Art/UI/Animation/Common/anui_common_slider_color_*.anim`, 60 fps):

| Clip | `pos` CanvasGroup α | `bg1` α | `bg1` scale | `bg2` scale | hạt đầu thanh |
|---|---|---|---|---|---|
| `none` | 1 → **0 trong 0.117 s** | 1 → 0 (0.117) | | | |
| `grow_b` (tăng nhiều) | 1 | 1 | (1,1) | (1,1) | bật ở 0.0167 |
| `grow_s` (tăng ít) | 1 | 1 | (0.5,0.8) | (0.4,1) | tắt |
| `close` | 0 | 0 | | | tắt |

⇒ Khi fill đang chạy: đầu thanh có quầng (bg1 61×180) + lõi (bg2); dừng thì tắt dần 0.117 s. Tốc độ chạy fill do Lua (không có clip).

Hạt đầu thanh (`Fill/#anim/particle`, UIParticle scale 10 ⇒ 1 đơn vị hạt ≈ 10 px):

| Hệ | dài | phát | đời | tốc | cỡ | màu | mat (blend) |
|---|---|---|---|---|---|---|---|
| `mtfx_glow_hhn_0001 (2)` sao | 1.1 s, world space | 50/s, cầu r 1.8 | 0.2–0.4 | 2–4 | 2–3 (×2, nhấp nhô theo đời) | start (1,0.8,0.54)…trắng; theo đời vàng (1,0.73,0) → trắng, α 1 → 0.73 | `mtvx_common_star_02` (`txvx_star_glow.png`, alpha, MainColor ×1.41) |
| `mtfx_glow_hhn_0001 (1)` chấm | 1 s | 40/s | 0.2–0.4 | 0 | 10×30 (dẹt dọc; node scale 0.185) | (0.87,0.89,0.43) → (1,0.78,0.23), α 0.78 → 0 | `mtvx_common_dot_light_01` (`txfx_mask_hhn_0002_m.png`, cộng) |

Các clip khác của thanh:
- `Art/UI/Animation/Common/common_fly_item_hit/anui_common_fly_item_hit.anim` (huy hiệu cấp, 60 fps): scale **0.8 → 1.05 (0.033) → 1.0 (0.083) → 0.9 (0.1)**.
- `Art/UI/Animation/Common/pet_level_exp/pet_level_exp_in.anim`: thanh trượt vào: pos.y 26.5 → -31.5 (0.1) → -6.5 (0.183).
- `anui_small_level_template_in`: scale 0.6 → **1.3** (0.067) → 1.082 (0.117) → 1 (0.283); icon α 0 → 1 trong 0.017.
- `anui_small_level_template_out`: scale 1 → 1.3 (0.05); icon α 1 → 0 (0.017–0.083); bật hạt `pbvx_small_level_template_out` 0.017–0.5: `glow` (`mtvx_pinball_glow` = `txfx_common_glow.png` cộng, đời 0.2, cỡ 2.6, cỡ theo đời 0 → 1 (0.057) → 0.69 (0.10) → 0.52, màu trắng → (1,0.75,0.36) → (1,0.58,0.17), α 1 → 1 (0.48) → 0); `ParticlesScale/02` (vòng, cỡ 90, đời 0.2, cỡ 0.25 → 0.69 (0.1) → 1, màu vàng (1,0.78,0) → trắng → (1,0.69,0.14), α 0 → 1 (0.23) → 1 (0.72) → 0); `Particle_up_01/02` (mũi tên ↑ bay lên: 2 hạt, tốc 4–10, đời 0.2–0.6, cỡ 0.15–0.25, giới hạn tốc 0.4 cản 0.3); `Particle_glow_01/02` (`txvx_common_round_21` cộng, cỡ 0.35–0.55, trắng → (1,0.84,0.4)).
- Tiếng (chỉ tên): `sfx_pinball_odds_expbar_up / _jump / _full`; đếm bảng `sfx_pinball_odds_expbag_scoring`, `_expbag_1/2/3`, `_expbag_jump_1/2/3`.

---

## 2. Icon bay khi bi rơi vào ô kẹo

### 2.1 Ô kẹo (trigger) — cấu trúc và cấu hình hiệu ứng

Ô kẹo: `Res/Pinball/Prefab/pbsc_trigger_addmoney.prefab` (ô to `pbsc_trigger_addbigmoney`, ô sự kiện `pbsc_trigger_acvitymoney`; bàn mẫu có `pbsc_trigger_rob`, `pbsc_trigger_gift`). Gốc scale 1.15.
- `imgbg` SR `txsc_pinball_trigger_bg_01` (90×124, ô vòm) order 2; `imgicon` (0,0.156) scale 0.5 = `txui_item_candy_one.png` (180 → 90 px); `txt_ball` TMP world "x10" dùng sprite font cam (`c`).
- `vx_get_01` [tắt]: `bg_flow_01` (`txvx_pinball_cardout_gold_glow.png`, mat `_get_glow_02` DissolveStencil, màu (1,0.392,0.979,0.5)), `glow/alpha` (`txvx_pinball_mask_flow_03.png` 95×132, mat `_get_glow_04`, màu (1,0.8,0.42,0.54)), `glow/add01` (`mask_flow_04` 59×128), `glow/add02` (`mtvx_pinball_botton_normal_glow_mask04.png`), `add03` (`mask_flow_05` 90×124, mat `_get_glow_06` AddEx, màu (1,0,0.584)).
- `EffectController.effectData`:
  - **`Hit`** → sinh `Res/UI/Prefabs/DemoPinball/pbui_pinball_add_money.prefab` (template `Flyout;1`) + effectType 3 (không prefab — có lẽ rung/âm);
  - **`Settle`** → sinh `Res/Fx/Prefab/Ui/pbfx_demo_pinball_slotactive.prefab`.
  - Ô khác dùng `fxpb_demo_ui_pinball_ringhit_orange` (Hit) và `pbvx_pinball_triggeron_mid` (ô giữa).
- AnimationController: `hit` = `anfx_demo_pinball_addmoney`, `times` = `anui_pinball_trigger_times`.

### 2.2 Clip ô khi bi vào — `Art/Fx/Animation/anfx_demo_pinball_addmoney.anim` (30 fps, phần chính 0.4 s)

Icon kẹo (`icon_03_scale`) bóp-giãn:

| t | 0 | 0.067 | 0.1 | 0.133 | 0.167 | 0.2 | 0.233 | 0.267 |
|---|---|---|---|---|---|---|---|---|
| scale (x,y) | 0.714 | **(0.905, 1.439)** giãn dọc | | (1.035, 0.899) bẹt | | | | 1.03 |
| pos.y (đv) | 0.129 | **0.1905** (+6 px) | 0.186 | 0.127 | 0.1905 | 0.178 | 0.166 | 0.159 |

Lớp sáng của icon (`Background_trigger_icon_032`): scale 0.87 → **2.40 (0.067)** → 0.96 (0.2).

Chữ "x10" (`txt_ball`): scale 1.22 → 1.39 (0.067) → 0.8 (0.1) → 1.0 (0.2) → 0.9 (0.333).

Cột sáng phụt lên (`vx_get_01/glow`, bật 0.033–0.4):
- `add02` (cột hẹp): scale (0.242,0.565) → (0.204,0.132) (0.033) → (0.19,0.65) (0.1) → (0.246,**0.971**) (0.267); pos.y 0.596 → 0.137 → 0.395 → 0.703 → 0.971 → **1.024** (phụt lên ≈ 90 px); màu xanh (0,0.4,1) → (0.68,0.33,1), α 0.75 (0.2) → 0 (0.333).
- `add01`: α 1 → 1 → 0.83 (0.2) → 1 (0.233) → 0 (0.267) → 0.35 (0.333) → 0 (0.367); màu xanh-tím.
- `alpha` (nền ấm): α 0 → 0.243 (0.133) → 0; màu (1,0.8,0.42) → trắng.
- `add03`: α 0 → 1 (0.133) → 0 (0.2); màu (0.84,0,1) → (0,0.68,1) → (0.43,0.5,1).
- `bg_flow_01` (dải quét DissolveStencil): bật 0.033–0.4, `_Param.x` 2.01 → 2.81 (0.067) → 2.0 (0.3), `_MaskTex_ST` 20×20 (lưới chấm), α 1 (0.167) → 0.81 (0.2) → 0 (0.3).
- Hạt `pbvx_rob_earnings_particles` bật 0.033.

`anfx_demo_pinball_addmoney_2` (ô gift): như trên, không cột sáng, `bg_flow_01` hồng (1,0.39–0.58,0.98), α 1 → 0 trong 0.033–0.2.

`anui_pinball_trigger_times`: `txt_ball` scale 1.1 → **1.3** (0.033) → 0.7 (0.1) → 0.9 (0.183).

### 2.3 "Icon bay" có trong asset — `pbui_pinball_add_money` + hạt icon kẹo

Prefab sinh ở `root_effect` của ô (y -0.316 đv). Clip `anui_pinball_add_money` (bảng 1.6 d): nhóm [icon kẹo 50×50 + số fs 38 vàng] **bật 0.3 → 1.5 (0.067 s) → 1.0 (0.167 s), bay thẳng lên 54 px trong 0.133 → 0.533 s (đầu nhanh, tiếp tuyến 288 px/s), co 1 → 0.3 trong 0.5 → 0.6 s rồi tắt**.

Hạt **`pbvx_rob_earnings_particles`** = icon kẹo bắn tung:

| Thuộc tính | Giá trị |
|---|---|
| texture | `txui_item_candy_one.png` (mat `mtvx_common_icon_01`, alpha) |
| dài / lặp | 0.2 s, không lặp, tối đa 10 hạt |
| phát | 20/s + burst t0: 3, t0.1: 2, t0.2: 5 |
| hình phát | nón r 0.3, góc 4°, scale (0.5,1) ⇒ phụt thẳng lên |
| đời | 0.5 s |
| tốc đầu | 6–9 |
| **trọng lực** | **5** (vọt lên rồi rơi — parabol) |
| cỡ | 0.4–0.45; theo đời ×2: 0.223 → 0.373 (0.118) → 0.476 |
| xoay | đầu ±60°; theo đời ×12.57: -0.78 → -0.13 (0.26) → -0.02 rad/s |
| α theo đời | 1 → 1 (0.42) → **0 (0.56)** |

**Không có đường cong bay tới đích trong asset**: icon/số từ ô hoặc bảng LED bay lên thanh cấp do Lua (DOTween; class `DoTweenUtils` có trong dll) điều khiển. Chỉ còn vệt đuôi + hạt đi kèm:

### 2.4 Vệt đuôi khi bay (TrailRenderer)

| Prefab | `m_Time` | width × | min vertex dist | gradient theo chiều dài | material |
|---|---|---|---|---|---|
| `Res/Fx/Prefab/Ui/View/pbui_fly_effects01.prefab` (gốc 50×50 scale 0.819; vệt dưới node scale 10) | **0.11 s** | 0.25 | 0 | c0.13 (1,0.855,0.373) → c0.36 (1,0.78,0.156) → c0.73 (1,0.557,0.137); α 0.05: 0.655 → 0.30: 0.314 | `mtfx_fly_effects_trail` (`fxtx_demo_pinball_trail.png`) |
| `Res/Fx/Prefab/Ui/View/pbui_fly_effects02.prefab` | không vệt, 2 hệ hạt world space (dưới) | | | | |
| `Res/Fx/Prefab/Ui/fxpb_demo_ui_pinball_trail.prefab` | 0.3 s | 0.18 | 0.1 | (0.684,1,0.993, α 0.52) → (0.72,0.54,1, α 0) | `fxmt_demo_pinball_trail` |
| `Res/Fx/Prefab/Ui/pbvx_reward_cell_fly_trail.prefab` | 0.15 s | 1 | 0.1 | (1,0.943,0.251) → (1,0.604,0), α 1 | như trên |

`pbui_fly_effects02`:
- sao `mtvx_common_star_01`: dài 0.4 s, 50/s, cầu r 1.8, đời 0.2–0.3, tốc 2–4, cỡ 2–3, màu theo đời (1,0.99,0.84) → (1,0.95,0.36) → (1,0.68,0), α 1 → 1 (0.44) → 0.
- chấm sáng `mtvx_common_dot_light_01` (cộng): dài 0.5, 40/s, đời 0.2–0.4, cỡ 30 → 0, màu (1,0.98,0.49) → (1,0.84,0.23), α 0.22 → 0.

### 2.5 Hiệu ứng tới đích

| Đích | Clip | Mốc scale |
|---|---|---|
| Huy hiệu cấp (thanh EXP) | `Art/UI/Animation/Common/common_fly_item_hit/anui_common_fly_item_hit.anim` | 0: **0.8** → 0.033: **1.05** → 0.083: 1.0 → 0.1: 0.9 |
| Nút bắn `btn_up/img_bottom` | `.../anui_common_pinball_fly_item_hit.anim` | 0: 0.95 → 0.067: 1.0 |
| Thanh năng lượng dưới | `AnimationClip/anui_pinball_bottom_slider_add.anim` | `txt_energy`: 1.3 (0.017) → 1.1 (0.067) → 1.3 (0.117) → 1.1 (0.167) → 1.3 (0.217) → 1 (0.25); `Fill Area` + `#Background_2`: 1.2 → 1.08 (0.05) → 1.2 (0.1) → 1.08 (0.15) → 1.2 (0.2) → 1 (0.25) ⇒ **rung 3 nhịp 0.05 s** |
| Khung bảng LED | `Art/Fx/Animation/anfx_background_scorebord_hit.anim` | y +3.8 px ở 0.033 s, về 0.067 s |

### 2.6 Hạt khi ô sáng / bi chạm

**`pbfx_demo_pinball_slotactive`** (ô "Settle"):

| Hệ | đời | tốc | cỡ | cỡ theo đời | màu theo đời | mat |
|---|---|---|---|---|---|---|
| `main` quầng (burst 1) | 0.7 | 0 | 2 | 0.35 → **1.0 (0.06)** → 0.55 | (1,0.95,0.66) → (1,0.75,0.31) → (1,0.27,0.27); α 1 → 1 (0.57) → 0 | `fxmt_demo_glow_add` (`txfx_common_glow.png`, cộng) |
| `star` (burst 1–3 ×**3 lần cách 0.1 s**) | 0.3–0.7 | 3–6 | 0.3–0.5 | 0.35 → 1 (0.06) → 0 | ngẫu nhiên trắng…(1,0.7,0.4) | `fxmt_demo_pinball_hit_s` (`txvx_star_glow.png`); giới hạn tốc ×6 → 0, cản 0.5 |

**`pbvx_pinball_triggeron_mid`** (ô giữa bật, scale 1.3):

| Hệ | đời | cỡ | cỡ theo đời | màu/α | mat |
|---|---|---|---|---|---|
| `glow` | 0.15 | 2.7 | 0 → 0.79 (0.17) → 0.9 (0.38) → 1 | (1,0.79,0.33) → (1,0.57,0.21) → (0.53,0.36,1) → (0.72,0.19,1); α 1 → 0 | `mtvx_pinball_glow_05` (`txvx_common_halo.png` × mask flow, cộng) |
| `glow2` | 0.15 | 2 | 0.54 → 0.84 → 1 | | `mtvx_pinball_inlight_01` (`txvx_pet_upgrade_light_dot.png`, cộng) |
| `glow3_b` | 0.1 | 0.6 | 0.35 → 0.78 → 1 | | như trên |
| `star` (6 hạt, tốc 15–60, cản 0.7) | 0.2–0.35 | 0.15–0.7 | ×1.83: 0 → 0.99 → 0 | ngẫu nhiên vàng (1,0.84,0.4) / trắng / xanh ngọc (0.61,0.99,0.98) | `mtfx_table_get_star_01` |
| `she` tia (6, nón 90°, Stretch) | 0.07–0.1 | (0.5–1)×(0.2–1.2) | 1 → 0.57 | cam → xanh → tím → cam, α 0 → 1 → 1 → 0 | `mtvx_pinball_inlight_03` (`txvx_common_glow_triangle_light_2.png`) |

**`fxpb_demo_ui_pinball_ringhit_orange`** (bi chạm nấm cam):

| Hệ | đời | cỡ | đặc điểm | mat |
|---|---|---|---|---|
| `hit` | 0.2 | 0.7 (×1.1: 0.71 → 1) | (1,0.91,0.68); trắng → cam (1,0.49,0), α 1 → 1 (0.45) → 0 | `fxmt_demo_pinball_dot_add` (`txfx_common_dot.png`, cộng) |
| `circle` | 0.1 | 1 (0.38 → 1) | burst 1 ×3 lần cách 0.1 s; α 1 → 0 | `fxmt_demo_pinball_circle` (`fxtx_demo_pinball_hitcircle.png`, cộng) |
| `dots` | 0.2–0.4 | 0.05–0.1 | 3–10 hạt, tốc 0–2 | `fxmt_demo_pinball_dot` |
| `stars` | 0.4–0.6 | 0.2–0.3 | 3–10 hạt, trọng lực 0.3, xoay ±360°/s | `fxmt_demo_pinball_star` |

Sao lấp lánh trên ô sáng (`Background_trigger/get_glow/background_trigger_get_particle`): `star` lặp (đời 0.3–0.5, cỡ 0.45–0.6); `star04` lặp (burst 1 ở t0 và t0.5, đời 0.5, cỡ 0.85 ×1.3: 0.69 → 0.88 → 1, sheet 2×2, màu (1,0.85,0.53) → (1,0.73,0), α 0 → 1 (0.4) → 0, mat `_card_glow_color_02` = `txvx_tap_star.png` cộng ×2).

---

## 3. Ánh sáng, gradient của máy

### 3.1 Cơ chế chung: shader `UEP/Interface/FlashTex` và `FlashTex(Combine)` = "đèn chạy theo bản đồ pha"

Mọi đèn chạy của máy (viền bảng LED, dải sao hai bên, mũi tên làn bắn, vòm bóng đèn quanh mặt bàn, biển neon phía sau) đều dùng **một cặp ảnh**:
- `_ShapeTex` (hoặc `_MainTex` ở bản không Combine): **hình lúc đèn SÁNG** (màu thật, nền trong suốt);
- `_FlashTex`: **bản đồ pha xám** cùng bố cục — độ xám mỗi bóng/mỗi chi tiết = thời điểm nó sáng. Ví dụ `light_top_05`: dải sao hai bên xám từ trắng (dưới) → đen (trên) ⇒ sáng chạy **từ dưới lên**; `scorebord_light_04`: bóng xen kẽ xám đậm/sáng ⇒ **hai nhóm luân phiên**; `light_top_07`: vòm bóng xen kẽ; `light_top_08`: mũi tên làn bắn đậm dần lên trên ⇒ chạy lên; `down_light_04`: neon xám đậm trên → nhạt dưới ⇒ quét dọc.
- Shader lấy `t = frac(time × _TimeSpeed + _TimeOffset)` (chu kỳ ~`_SpaceTime`), chỗ nào có giá trị pha trong cửa sổ `[t, t + _FlashRange]` (mép mềm `_FlashSmooth`, lặp `_FlashRegionAmount` lần trên dải 0–1) thì sáng `_FlashColor × _FlashPower`; chỗ khác lấy `_MainColor`. (Thân shader bị strip; đây là cách đọc từ tên + chú thích Properties: 闪烁图 = ảnh nhấp nháy, 闪烁块区间 = độ rộng khối chớp, 闪烁块淡入淡出 = mép mềm, 闪烁块个数 = số khối, 时间间隔 = khoảng thời gian.)

Dựng lại trong uGUI: mỗi bóng/chi tiết là một Image riêng, gán chỉ số pha `p ∈ [0,1]` (thay cho bản đồ xám); mỗi khung tính `t = frac(Time*speed + offset)`, độ sáng = smoothstep cửa sổ quanh `t` (lặp `n` khối) — hoặc viết một shader UI nhỏ đọc ảnh pha xám như game.

### 3.2 Bảng material ánh sáng của máy (gắn vào đâu, tham số)

Tất cả nằm dưới `pbsc_pinballtable_background_01/pbsc_pinball_light_top` (scale 2) trừ khi ghi khác. Đường dẫn mat: `Art/UI/Materials/pinball/`.

| Object (SR sprite, cỡ) | Material / shader | Texture vai trò | Màu | Tham số nhịp (mặc định mat) | Blend |
|---|---|---|---|---|---|
| `Background_scorebord` (scorebord 577×178) | `mtvx_background_shine_scoreboard_combine` / FlashTex(Combine) | Shape = `scorebord_light_03` (26 quầng bóng), Flash = `light_04` (pha xen kẽ) | Main (1,0.714,0.406), Flash (1,0.886,0.381) ×22.7 | speed 0.2, offset 2.07, space 1.2, range 0.4, smooth 0.001, n 1 | Alpha |
| `Background_desk_combine` (`txsc_pinball_desk2.png` 1093×1672 = **khung tủ máy**) | `mtvx_background_shine_level_desk_combine` / FlashTex(Combine) | Shape = `light_top_03` (770×1024: dải sao cam 2 bên, mũi tên xanh 4 góc, vòng 7 sao xanh đỉnh, 2 sao vàng, 12 quầng bóng tím quanh mặt bàn, mũi tên tím làn bắn); Flash = `light_top_05` (pha: dải sao trắng dưới → đen trên) | Flash (1,0.851,0.651) ×20 | speed 0.14, offset 0.1, space 1, range 0.4, smooth 0.11, n 1; ST (1.419,1.633,-0.205,-0.558) | Alpha |
| `Background_desk_combine_glow` (`txsc_pinball_desk1.png` 620×896, màu (1,0.926,0.852)) | `mtvx_background_shine_level_desk_combine_3` / FlashTex(Combine) | Shape = `light_top_06` (**vòm ~80 bóng chấm vàng** quanh mặt bàn, quầng mềm), Flash = `light_top_07` (bóng xen kẽ sáng/tối) | **Main HDR (59.6,53.7,29)** (cực sáng), Flash (1,0.83,0.569) ×20 | speed 2.13, offset 1, **space -1.08** (chạy ngược), range 0.29, smooth 0.12, n 0.98 | Alpha |
| `Background_desk_combine1` + con `..._combine2` (`light_top_08` 138×709, ×0.499, đặt x 1.303 = làn bắn bên phải) | `..._combine01` / `..._combine02` (FlashTex, không Combine) | Main = Flash = `light_top_08` (chuỗi ~25 mũi tên ^ đậm dần lên trên) | Main (1,1,1,0.671), Flash **(0.616,0.259,1.4)** tím HDR ×24.1 (combine02: ×157.3, α SR 0.702) | speed 0.75, offset 0.1/0.93, space 1.76, range 0.12, smooth 0.25/0.2 | **Cộng** |
| `shine_level_down_combine` (`txsc_pinball_bg_dark_2.png` 637×912 = tấm nền tím sẫm có hoa văn biểu tượng heo + sao, sau mặt bàn) | `mtvx_background_shine_level_down_combine` / FlashTex(Combine) | Shape = `down_light_03` (524×736, **biển neon nét tím** hình biểu tượng), Flash = `down_light_04` (pha xám dọc) | Flash (0.582,0.388,1, α 0.145) ×5.87 | speed 1, offset 0, space 1, range 0.05, smooth 0.44, n 0.13 | Alpha |
| `Background_trigger/get_glow/background_trigger_get_01` (`down_light_03`, màu (0.423,0.274,1,0.518)) | `..._down_combine_1` / FlashTex | Flash = `down_light_04` | Flash trắng ×44.3 | speed 1, space 2, range 2.4, smooth 0.3, n 0.13 | Cộng |

Theo trạng thái máy (AnimationController khoá `idle`/`card`/`event` → clip `anfx_background_shine_group_level_1/2/3`, chỉ 1 mốc đặt tham số):

| Object | idle (level_1) | card (level_2) | event (level_3) |
|---|---|---|---|
| `Background_scorebord` | speed 0.45, range 0.2, smooth 0.01, n 0.6, offset 1 | speed 1.2, range 0.2, smooth 0.05, n 1, space 1 | speed 1, range 0.25, smooth 0.02, **n 4.66**, power 5, offset 1.11 |
| `Background_desk_combine` (dải sao, mũi tên) | speed 0.3, range 0.3, smooth 0.36, n 1.03 | speed 0.5, range 0.3, smooth 0.33, n 1 | **speed 2**, range 0.25, smooth 0.51, n 1, offset 0.2 |
| `Background_desk_combine_glow` (vòm bóng) | speed 0.7, range 0.2, smooth 0.001, power 20, space 2.5 | speed 2, range 0.3, space 1 | **speed 4**, range 0.2, space 0.2 |
| `shine_level_down_combine` (neon) | speed 0.8, range 0.05, smooth 1.2, n 1.05, Flash (0.62,0.39,1, α 0.78) | speed 1.2, power 5, n 1.05, offset 10, Flash α 1 | **speed 2.5**, n 1.1, offset 15, Flash **trắng** (1,1,1,1) |

⇒ Nhịp ước lượng (chu kỳ ≈ space / speed): idle — dải sao ~3.3 s/vòng, vòm bóng ~3.6 s, bảng LED ~2.7 s; card — nhanh ×2–3; event — dải sao 0.5 s, vòm bóng 0.05 s/bước (nháy rất nhanh), bảng LED nhiều khối cùng chạy, neon chuyển trắng.

`anfx_background_launch_prompt_in/out` (gợi ý kéo cần bắn): mũi tên làn bắn `Background_desk_combine1` α 0 → 1 trong **0.417 s** (con `combine2` 0 → 0.702); tắt 1 → 0 trong **0.217 s**.

### 3.3 Dải đèn điện tử `mtvx_pinballtable_electronic_01`

Không phải dải đèn chạy viền mà là **flipbook màn LED** của bảng điểm (mục 1.5): `UI/Uep/PGameCustom/UIFlipBook`, `_FlipbookConfig (3 cột, 6 hàng, bắt đầu khung 1)`, 16 khung dùng, `_Speed 15` khung/s, `_Loop 0`, cộng (Src 5 / Dst 1), nền đen. Gắn ở `pbvx_pinball_result_board_out_04/fx_glow_1/fx_r_tl` qua `UIFlipbookController(isLoop 0, color trắng)`. Các ảnh `txsc_pinballtable_electronic_03…07` (512×128) là 5 khung LED rời dùng cho `collect_01` (mục 1.4).

### 3.4 Lớp glow / flash của hiệu ứng (cỡ, màu điển hình)

Hệ hạt của mặt bàn là world-space: **cỡ hạt 1 = 1 đơn vị = 100 px**. Hệ trong UI có UIParticle scale 10 ⇒ cỡ 1 ≈ 10 px (hoặc ×80 ở nhóm frenzyball).

| Hiệu ứng (prefab `Res/Fx/Prefab/Ui/`) | Lớp | Texture / mat | Cỡ (đv) ≈ px | Đời | Màu / α theo đời | Blend |
|---|---|---|---|---|---|---|
| `pbvx_pinball_result_board_out_01` (kết quả nhỏ: chỉ `flash` + `glow`; các lớp khác tắt) | `flash` | `txvx_pinball_result_board_flash.png` 128×64 (khối bo góc vàng nhạt viền cam = hình màn LED) / `mtvx_pinball_result_board_flash` | 4.2 × 1.6 ≈ **420×160 px** (phủ màn LED) | 0.2 | α 0.31 → 1 (0.06) → 0.97 (0.57) → 0 | Cộng |
| | `glow` | `txfx_common_glow.png` 128×128 / `mtvx_pinball_glow_02` | 6×4, ×2 (0.178 → 0.534) ≈ 210–640 px | 0.2 | start (1,0.88,0.33); α 0.31 → 1 (0.12) → 0.97 → 0 | Cộng (legacy) |
| `..._out_02` (vừa) | + `circle` | `mtfx_common_circle_smooth` (vòng mềm vẽ bằng shader) | 4.5 (0.178 → 1) ≈ 80 → 450 px, tốc 5 | 0.2, burst 1 ×2 cách 0.1 s | (1,0.88,0.33); α như trên | Alpha |
| | + `circle_hard` | `mtvx_evolution_halo` (vòng cứng, shader) | 4.2 (0.178 → 1) | 0.2, ×2 | (1,0.67,0) | Cộng |
| | + `stars` / `starsBig` | `txvx_star_glow.png` 256 / `mtvx_star_alphablend` | 0.1–0.5 / 0.5–1, co về 0.3 / 0.14 | 0.2–0.6, trễ 0.1, burst 2–3 × 4–6 lần cách 0.1 s | gradient trắng ↔ vàng (1,0.88,0.02) ↔ cam (1,0.37,0) | Alpha |
| `..._out_03` (lớn) | + `line` tia tốc độ | `txvx_pinball_cardout_speedline.png` / `mtvx_pinball_cashout_speedline` | (0.5–1) × (7–10), Stretch len 2, tốc 10–20 | 0.2–0.5, 6 tia | trắng ↔ xanh (0.02,0.8,1) | Alpha |
| | circle ×1.5 | | | | | |
| `pbvx_pinball_triggeron_mid` | `glow` | `txvx_common_halo.png` × mask flow / `mtvx_pinball_glow_05` | 2.7 (0 → 1) | 0.15 | cam (1,0.79,0.33) → tím (0.72,0.19,1) | Cộng |
| `pbfx_demo_pinball_slotactive` | `main` | `txfx_common_glow.png` / `fxmt_demo_glow_add` | 2 (0.35 → 1 → 0.55) | 0.7 | (1,0.95,0.66) → (1,0.27,0.27) | Cộng |
| `pbvx_small_level_template_out` | `glow` | `txfx_common_glow.png` | 2.6 ×10 px | 0.2 | trắng → (1,0.58,0.17) | Cộng |

⇒ Kiểu điển hình của game: **quầng tròn mềm trắng tô màu vàng-cam (1,0.88,0.33)**, sống **0.15–0.2 s**, cỡ bật nhanh từ ~18–35% lên 100% trong 6–17% đời đầu, α bắt đầu 0.31 → 1 rất nhanh rồi giữ, tắt cuối đời. Glow lớn (trigger, bảng) có ánh tím ở cuối (0.53–0.72, 0.19–0.36, 1).

### 3.5 Ô sáng phía dưới mặt bàn (`Background_trigger`) — đèn chạy khi mở

Clip `Art/UI/Animation/PinBall/anui_pinballtable_background_01_background_trigger_open.anim` (30 fps, wrap loop, mẫu 4.1 s; `none` tắt hết và đặt `_Speed` = 5):
- `Background_trigger_bg_flow_03` (mat `mtvx_background_trigger_bg_flow_06`, shader `UEP/Interface/PointExpand`, chấm loang; `_PointColor (1,0.597,0.098)`, nền (1,0.431,0.717, α 0)): `_Speed` **5 → 25** khi mở.
- 4 nhóm hình viền `01`→`02`→`03`→`04` (quầng `light_top_12_6/12_5/12_4`, `trigger_shader_15`, màu tím (0.27–0.49, 0.1–0.25, 0.76–1)): mỗi nhóm sáng **0.167 s**, nối đuôi nhau, **chu kỳ 0.667 s** (đèn chạy 4 bước).
- `card_glow_color02/03/04` (khung thẻ cam/hồng/đỏ): mỗi cái sáng 0.133 s, lệch nhau 0.067 s, chu kỳ 0.667 s.
- Sao nhỏ `xx02/xx03/xx04`: sáng ~0.33 s, chu kỳ 0.7 s, lệch 0.067 s; `xx10…xx13`: bật/tắt 0.233 s xen kẽ (chu kỳ 0.467 s), lệch pha 0.167/0.233/0.4/0.567.
- `background_trigger_get_01` (neon tím, cộng): α 0.30 ↔ 0.315 (gần đứng), **r dao động 0.27 ↔ 1** mỗi ~0.27–0.3 s (tím ↔ hồng), g 0–0.42, b ≈ 1.

Hộp quà (`pbsc_trigger_gift/glow_anim01`, clip `anui_pinball_trigger_gift_glow_in/loop/out`, 30 fps): lớp `01`/`01_alpha` (`txvx_pinball_trigger_gift_glow06.png`, SR tiled 1.28×1.28) cuộn UV `_MainTex_ST.z` 0.5 → -0.5 trong 0.567 s (quét sáng ngang); `02` (glow02) α 0 → 1 (0.2) → 0 (0.367); `03` α 0 → 1 (0.267) → 0 (0.467); `04`, `04_1`, `04_alpha` α 0 → 1 (0.367) → 0 (0.567) ⇒ 3 vòng sáng to dần nối nhau mỗi ~0.1 s. Loop: chu kỳ 1.23 s (02: 0.5–0.9, 03: 0.633–1.07, 04: 0.767–1.17). Out: event `settle` ở 0.467 s, bật `pbvx_pinball_triggeron_mid02` 0.467–0.7.

Nút bắn trên bàn (`Background_startmachine`, cần lò xo): `anfx_demo_pinball_startmachine_normal` (0.367 s): bi `Background_startmachine_ball` scale 0 → 1.25 (0.067) → 1.25 → 1.4 (0.233) → 1.42; y -2.077 → **-1.308** (0.067, nảy lên 77 px ×0.61) → -1.492 → -2.106 (0.2) → -1.922 → -2.059. `pressed_ing` (0.233 s): lò xo `startmachine02` scale y 0.627 → **1.573** (0.067) → 0.887 → 1.2; đầu nút y -2.857 → -2.236 → -2.648 → -2.453 (bật giãn). Hạt `Particle_loop/out` (`txfx_battle_firerat_smoke.png`, `txfx_destory_elect.png`) bật khi nút đỏ (bắn mạnh).

Nút "bắn" UI ở mainview (`btn_up`, 267×205): `vx_normal_glow_group/mask_01` (439×278 ×0.5, `mtvx_pinball_botton_normal_glow_01` FlashTex cộng, Flash HDR 1.61, speed 0.75, space 1.1, smooth 0.2, màu SR (1,0.844,0.241, α 0.1)) + `mask_02` (FlashTex trên chính `txui_pinball_btn_start.png`, Flash 1.11, speed 0.8, range 0.1, α SR 0.1) ⇒ **vệt sáng quét qua nút mỗi ~1.25 s**, rất nhẹ (α 0.1).

---

## 4. Hiệu ứng khác trên màn pinball (chưa có trong báo cáo cũ)

| Thứ | Đường dẫn | Số đo chính |
|---|---|---|
| Đổi bàn | `Art/UI/Animation/PinBall/anui_pinball_table_change.anim` (trên `pbsc_pinball_table_01/anim`) | `nodes` + `background` giữ y 0 tới 0.333 s rồi trượt lên **y 20.55 đv (≈ 2055 px)** lúc 1.0 s (cuộn cả bàn ra khỏi màn). |
| Nút UI vào màn | `AnimationClip/anui_pinball_mainview_button_in.anim` | cột nút trái x -25 → +15 (0.1) → 0 (0.183); phải +25 → -15 → 0; đáy y -127 → +30 → 0; thanh cấp y 58 → -5 → 0 (vượt rồi nảy, 0.183 s). |
| Thanh cấp vào | `pet_level_exp_in` | y 26.5 → -31.5 (0.1) → -6.5 (0.183). |
| Thông báo lên cấp (dưới thanh) | `pbui_pet_level_exp_view/Mask/group_upgrade_notification` + clip `anui_pinball_upgrade_notification_in/out/...` | chưa đo chi tiết (thẻ 435×74 có đầu tướng + chỉ số +ATK/HP/DEF). |
| Va nấm nhỏ | `Art/Fx/Animation/anvx_pinball_collider_small.anim` (30 fps) | `image` 1.15 → 1 trong 0.067 s rồi đổi sang `image2` (bản đã chạm); `backlight` 1.10 → 0.68 trong 0.067 s rồi tắt; hạt bật 0.067. |
| Phần thưởng bạn bè | `AnimationClip/anui_pinball_friend_reward.anim` | scale 0 → 0.41 (0.067) → **1.66** (0.133) → 0.97 (0.2) → 1.04 (0.3) → 1 (0.533) → 1.03 (1.0); α 0 → 1 (0.133) → 1 (0.833) → 0 (1.0). |
| Ra khỏi ô cướp | `Art/Fx/Animation/anvx_rob_pinball_trigger_out.anim` | `img_glow` 5.12 → 0.5 trong 0.233 s; `img_star_glow` 1.5 → 5 trong 0.083–0.433 s, α 1 → 0. |

---

## 5. Hình cần vẽ (để nhờ GPT vẽ lại theo nét riêng)

Quy ước: **[VẼ]** = hình có nét, nên nhờ GPT vẽ; **[CODE]** = gradient / quầng mềm / lưới chấm / bản đồ pha thuần, bên mình sinh bằng code (không cần GPT). Cỡ là cỡ ảnh gốc của game (px); "hiện" = cỡ hiển thị trên màn chuẩn 1334 rộng. Nền: "trong" = nền trong suốt (PNG alpha). Không có ảnh nào của game dùng nền đặc ngoài flipbook LED (nền đen, blend cộng).

### 5.1 Bảng số LED

| # | Ảnh game | Cỡ / hiện | Hình dạng | Nền | Tách lớp sáng/tắt? | Loại |
|---|---|---|---|---|---|---|
| 1 | `txsc_pinball_bg_scorebord.png` | 577×178 / 577×178 | Khung bảng bo tròn dài vàng-cam, **26 bóng đèn tròn** quanh viền (10 trên, 10 dưới, 3 mỗi đầu), lòng màn hình chữ nhật bo góc đỏ sẫm có lưới chấm LED, 2 khớp ống xanh dương nắp đỏ ở hai đầu, đế xanh đậm | trong | Game vẽ bóng **ở trạng thái tắt/nhạt** trong khung, lớp sáng là ảnh riêng (#2). Nên vẽ khung với **bóng tắt** (bóng màu kem/xám nhạt) | **[VẼ]** |
| 2 | `scorebord_light_03.png` | 404×136 (phủ đúng vùng bóng) | 26 quầng sáng vàng tròn ở đúng tâm 26 bóng | trong | Là lớp "sáng" | **[CODE]** (quầng tròn mềm đặt theo toạ độ bóng). Nếu muốn có nét: vẽ thêm 1 bóng sáng mẫu 32×32 rồi code nhân bản |
| 3 | `scorebord_light_04.png` | 404×136 | Bản đồ pha: bóng xen kẽ sáng/xám | trong | — | **[CODE]** (chỉ số pha mỗi bóng) |
| 4 | `scorebord_light_05.png` | 448×130 / ≈411×125 | Viền chữ nhật bo góc mảnh trắng có quầng — viền màn LED chớp | trong | lớp sáng | **[CODE]** |
| 5 | Màn LED: `electronic_03…07` (512×128), `light_09` (560×426), `light_010` (1037×558), `light_011/012/013` (261×537), flipbook `electronic_01` (2048², 16 khung 682×341) | hiện ≈ 384×90 (khung phun), 104–240 px (gợn) | Các **mẫu ma trận chấm LED** vàng-cam (kim tự tháp phun lên, tách 2 góc; vòng, ngoặc ( ) lan ra; khối tròn → thanh dài → vỡ hạt) | trong (flipbook: đen + cộng) | lớp sáng | **[CODE]** — sinh bằng lưới chấm (bước ≈ 14–16 px, chấm ≈ 10–12 px) + mặt nạ hình học + quầng; không cần GPT |
| 6 | Chữ số bảng: `txui_font_pinball_number.png` (256×512, mỗi glyph ≈ 29–43 × 54–56) | chữ trên bảng cao ≈ 55–70 px | Bộ `h` (xanh dương → tím, viền sáng) dùng cho bảng LED; bộ `c` (cam-vàng viền nâu) dùng cho số "x10" trên ô. Ký tự: `0–9`, `K M B T` (+ `W`, 万/亿 nếu cần) | trong | Không | **[VẼ]** (2 bộ màu; có thể vẽ 1 bộ trắng viền đậm rồi code tô gradient màu) |
| 7 | Chữ "+N" / số cộng: TMP `zh_cn_body` + mat `zh_cn_body_special_gold_light_01` (mặt chữ vân vàng `txvx_fonts_material_gold_02.png` 64×64, viền đen 0.6) | fs 38–64 | Chữ font thường + vân vàng | — | — | **[CODE]** (font của mình + gradient vàng + viền); vân `gold_02` là gradient |
| 8 | `txvx_pinball_result_board_flash.png` | 128×64 / 420×160 | Khối chữ nhật bo góc vàng nhạt viền cam (chớp phủ màn LED) | trong | lớp sáng | **[CODE]** |
| 9 | Glow chung `txfx_common_glow.png` (128²), `txvx_common_halo.png` (128²), vòng `circle_smooth`/`evolution_halo` (shader) | 2–6 đv | Quầng tròn mềm, vòng mềm/cứng | trong | — | **[CODE]** |
| 10 | Sao lấp lánh `txvx_star_glow.png` (256²), `fxtx_demo_pinball_star.png` (128²), `txvx_tap_star.png` (256², sheet 2×2) | 0.1–1 đv | Sao 4 cánh có quầng; sao 5 cánh nhỏ | trong | — | Sao 4 cánh quầng: **[CODE]**; sao 5 cánh có nét: **[VẼ]** (nhỏ, 128²) |

### 5.2 Thanh cấp

| # | Ảnh game | Cỡ / hiện | Hình dạng | Nền | Tách sáng/tắt | Loại |
|---|---|---|---|---|---|---|
| 11 | Rãnh thanh `txui_common_bg_round_32` (sliced, atlas) + mat chấm caro | hiện cao 66 px, dài theo màn | Viên thuốc bo tròn, xanh đen, lòng tối có chấm caro mờ | trong | — | Khung rãnh: **[VẼ]** 9-slice (vd 128×66, viền tay) nếu muốn nét tay; chấm caro: **[CODE]** |
| 12 | Fill `txui_mainview_bg_round_corner` + shader sọc `ShapeFlow` | inset 5 px, cao 56 | Viên thuốc đầy, **sọc chéo 35° vàng (1,0.843,0.149) / cam (1,0.741,0.252)**, ô 30 px, sọc 51% | trong | — | Hình fill: **[VẼ]** 9-slice trơn (hoặc code); sọc: **[CODE]** (texture lặp hoặc shader) |
| 13 | Đầu sáng `txvx_pinball_slider_fill_glow_01.png` (60×128), `_02.png` (64×44) | 61×180, 76×53 | Quầng trắng mềm dọc; lõi sáng | trong | lớp sáng | **[CODE]** |
| 14 | Huy hiệu cấp `txui_pinball_level_bg` (atlas) | hiện 112×111 | Huy hiệu tròn/khiên chứa số cấp (fs 40, đổ bóng đen 2 px — bên mình bỏ bóng theo luật UI) | trong | Không | **[VẼ]** |
| 15 | Mốc nhỏ: icon hệ `txui_common_pet_element_*.png` (80×80), viền mốc `txui_pinball_level_small_01` (54×54), mũi tên `txui_common_element_up.png` (36×33) | 58×55 | Icon hệ tròn; vòng đạt mốc; mũi tên lên xanh | trong | `level_small_01` là trạng thái "đạt" (bật/tắt riêng) | **[VẼ]** |
| 16 | Hạt đầu thanh: sao `txvx_star_glow`, chấm `txfx_mask_hhn_0002_m.png` (64²), `txvx_common_round_21` | 10–30 px | Sao quầng, chấm mềm | trong | — | **[CODE]** |

### 5.3 Icon bay

| # | Ảnh game | Cỡ / hiện | Hình dạng | Nền | Tách | Loại |
|---|---|---|---|---|---|---|
| 17 | Kẹo `txui_item_candy_one.png` (180×180; có `_small` 100×100, `candy_three` 180×180) | 50 px (số cộng), 90 px (trên ô), hạt bắn 40–90 px | Viên kẹo tròn vàng sọc cam, hai đầu giấy gói xoắn cam-hồng, viền nâu đậm, chấm sáng trắng | trong | Không | **[VẼ]** |
| 18 | Vệt đuôi `fxtx_demo_pinball_trail.png` (128²) | rộng ~0.18–0.25 đv | Dải mềm đậm đầu nhạt đuôi | trong | — | **[CODE]** (TrailRenderer/LineRenderer + gradient) |
| 19 | Ô kẹo `txsc_pinball_trigger_bg_01` (90×124), `_bg_02` (89×124), `trigger_icon_01` (74×74), `trigger_icon_02` (24×34) | ×1.15 | Ô hình vòm dưới đáy bàn, icon ô | trong | `bg_01`/`bg_02` = thường/đang sáng | **[VẼ]** |
| 20 | Cột sáng & quét sáng ô: `txvx_pinball_mask_flow_03/04/05` (95×132, 59×128, 90×124), `mtvx_pinball_botton_normal_glow_mask04.png` (260×213), `txvx_pinball_cardout_gold_glow.png` (63×82) | | Cột sáng dọc mềm, khung vòm phát sáng | trong | lớp sáng | **[CODE]** |
| 21 | Hạt va: `txfx_common_dot.png` (64²), `fxtx_demo_pinball_hitcircle.png` (128², vòng), tia `txvx_common_glow_triangle_light_2` | | Chấm mềm, vòng, tia tam giác | trong | — | **[CODE]** |

### 5.4 Lớp sáng của máy

| # | Ảnh game | Cỡ / hiện | Hình dạng | Nền | Tách sáng/tắt | Loại |
|---|---|---|---|---|---|---|
| 22 | Khung tủ `txsc_pinball_desk2.png` (1093×1672) | hiện ≈ 1093×1672 ×0.5×2 | Tủ máy đỏ: vòm đỉnh có 7 sao xanh, 2 góc chữ L xanh có vân mũi tên, 2 cột dải sao cam hai bên, viền vàng quanh mặt bàn, làn bắn bên phải có mũi tên tím, bàn phím caro + nút màu ở đáy, chân tủ | trong (lỗ ở mặt bàn) | Vẽ ở **trạng thái tắt** (sao, mũi tên, bóng màu nhạt) | **[VẼ]** |
| 23 | Lớp sáng trang trí `txvx_pinball_light_top_light_03.png` (770×1024) | phủ khung tủ | Bản **sáng** của: 2 dải sao cam, 4 cụm mũi tên xanh góc, vòng 7 sao xanh đỉnh, 2 sao vàng, chuỗi mũi tên tím làn bắn, 12 quầng bóng tím quanh mặt bàn | trong | là lớp "sáng" của #22 | **[VẼ]** (cùng nét với #22, chỉ các chi tiết sáng, tô sáng hơn) — quầng tím quanh bóng: [CODE] |
| 24 | Bản đồ pha `light_top_05.png`, `light_top_07.png`, `scorebord_light_04`, `down_light_04` | như ảnh sáng | Xám theo thứ tự chạy | trong | — | **[CODE]** (tạo từ alpha của ảnh sáng × gradient dọc / xen kẽ theo chỉ số) |
| 25 | Vòm bóng `light_top_06.png` (620×896) + đế `txsc_pinball_desk1.png` (620×896) | ×0.5×2 | **~80 bóng chấm vàng** chạy theo vòm cửa quanh mặt bàn, quầng mềm | trong | desk1 = bóng tắt (đoán theo cỡ trùng), light_06 = sáng | Bóng tắt: **[VẼ]** (hoặc vẽ 1 bóng mẫu rồi code rải theo đường vòm); quầng sáng: **[CODE]** |
| 26 | Mũi tên làn bắn `light_top_08.png` (138×709) | ×0.5 ≈ 69×354 | ~25 mũi tên ^ xếp dọc cong ở đỉnh | trong | Main = sáng, pha dọc | Hình mũi tên: **[VẼ]** (đơn giản, có thể code); pha: [CODE] |
| 27 | Tấm nền sau mặt bàn `txsc_pinball_bg_dark_2.png` (637×912) | ×0.5×2 | Tấm tím sẫm, hoa văn quả trám, biểu tượng mascot (đầu heo trong đĩa bay) + sao 4 cánh, vòm | **đặc** (phủ kín vùng) | Tắt (tối) | **[VẼ]** |
| 28 | Neon `txvx_pinball_light_down_light_03.png` (524×736) | phủ lên #27 | Nét **neon tím** đúng các đường của biểu tượng #27 (viền, sao, chấm) | trong | lớp sáng của #27 | **[VẼ]** nét (line-art trùng #27) — quầng neon: [CODE] (blur + cộng) |
| 29 | Nền bàn `txsc_pinball_bg.png` / `bg_new.png` (1334×1875), `bg_star.png` (127×129), `bg_ground.png` (1334×492) | | Nền sau máy, sao trang trí, nền đất | trong / đặc | — | **[VẼ]** (ngoài trọng tâm báo cáo) |
| 30 | Nút bắn UI `txui_pinball_btn_start.png` (267×205) + bản `diamond`/`disable` cùng cỡ | 267×205 | Nút bấm lớn | trong | 3–4 trạng thái riêng | **[VẼ]**; vệt quét sáng: [CODE] |

Tóm lại phần GPT cần vẽ: khung bảng LED (bóng tắt), 2 bộ chữ số + K/M/B/T, huy hiệu cấp, mốc nhỏ + mũi tên, rãnh/fill thanh 9-slice (tuỳ), viên kẹo, ô kẹo (2 trạng thái), khung tủ (tắt) + lớp chi tiết sáng tương ứng, đế bóng vòm, mũi tên làn bắn, tấm nền tím + nét neon trùng khớp, nút bắn. Mọi quầng, vòng, glow, vệt, lưới chấm LED, sọc fill, bản đồ pha đèn chạy: sinh bằng code.
