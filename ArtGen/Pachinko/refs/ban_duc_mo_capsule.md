# Clash of Critters 0.51.1: hiệu ứng mở capsule thú (số đo từ bản đục)

Nguồn: `D:\Ripper\ClashOfCritters\AssetRipper_Export\ExportedProject\Assets\AssetBundles\` (viết tắt `AB\`). Mọi số dưới đây đọc thẳng từ prefab và clip (Unity YAML). Clip đều là **Legacy Animation** (component `Animation`, không có AnimatorController), 60 fps; Lua bị mã hoá nên **thứ tự gọi clip, đường bay của capsule vào chỗ và nhịp lơ lửng là do Lua (tween) làm, không có trong bản đục**. Phần nào là suy luận sẽ ghi "(suy luận)".

Toạ độ UI: chiều ngang tham chiếu **750** (tính ngược từ `group_btns`: padding 30 + 3 nút 216.667 + 2 khe 20 = 750). Gốc toạ độ các điểm đặt capsule là tâm màn hình (anchor 0.5,0.5).

## 1. Danh sách file của luồng mở

### 1.1 Màn chính: mở 1 đến 5 capsule

| Vai trò | File | Ghi chú |
|---|---|---|
| **Màn mở capsule** (nền mờ, 1–5 chỗ đặt capsule, nút Mở / Mở tất cả / Mở nhóm nữa / Xác nhận) | `AB\e34395bfb1265db6d3c5fc7170a3238d\Res\UI\Prefabs\Common\pbui_common_reward.prefab` | Root có `Canvas` override sort. `anim` có Animation: `anui_common_reward_in`, `_out`, `_none` + `LuaAnimationEventListener` |
| Capsule xanh (khuôn, nhân bản ra từng chỗ) | lồng trong prefab trên: `reward_01/anim/pbui_common_reward_blue` (bản gốc riêng: `AB\a4644650d0b1ac922203c516f3a6615d\Res\UI\Prefabs\Common\pbui_common_reward_blue.prefab`) | Animation: `anui_common_reward_blue` (mặc định), `anui_common_reward_get`, `anui_common_reward_blue_in`, `anui_common_reward_blue_in_new` |
| Capsule tím | `reward_01/anim/pbui_common_reward_purple` (gốc: `AB\5ffc6a9ccdc376785c357c004ef7776e\Res\UI\Prefabs\Common\pbui_common_reward_purple.prefab`) | `anui_common_reward_purple`, `_get`, `anui_common_reward_purple_in`, `anui_common_reward_purple_new` |
| Capsule lục (bản riêng) | `AB\ab5daee96142fe52015806520e4f307e\Res\UI\Prefabs\Common\pbui_common_reward_green.prefab` | `anui_common_reward_greed_new_center` (clip mở, cùng nhịp bản xanh) |
| Clip vào màn | `AB\e34395bfb1265db6d3c5fc7170a3238d\AnimationClip\anui_common_reward_in.anim` | 2.167 s, có event `single` (2.0 s) và `multi` (2.167 s) |
| Clip ra màn / trạng thái rỗng | `AB\e34395bfb1265db6d3c5fc7170a3238d\AnimationClip\anui_common_reward_out.anim`, `anui_common_reward_none.anim` | |
| Clip đặt capsule đóng (reset) | `AB\072a122758a5268497ea3d4624e26d6b\Art\UI\Animation\Login\anui_common_reward_blue_in.anim`, `_purple_in.anim`, `_green_in.anim` | 1 khung, đặt nắp/thân về chỗ, tắt hiệu ứng |
| **Clip mở capsule (chạm)** | cùng thư mục: `anui_common_reward_blue_in_new.anim`, `anui_common_reward_purple_new.anim` | 1.1 s, event `open` ở 0.3 s. Đường dẫn khớp prefab hiện tại |
| Clip mở bản cũ (đường dẫn lệch prefab, chỉ một phần còn ăn) | `anui_common_reward_blue.anim` (0.983 s), `anui_common_reward_purple.anim` (1.45 s) | lắc lâu hơn, có số đo độ hiếm khác nhau (xem mục 4) |
| Clip thu capsule đã mở (biến mất) | `anui_common_reward_get.anim` | 0.4 s |
| Quầng sau capsule thở | `anui_common_reward_bg_loop.anim` | lặp (WrapMode Loop), 6 s |
| Nền tối vào/ra | `anui_common_black_in.anim`, `anui_common_black_out.anim`, `anui_common_black_normal.anim` | 0.083 s |
| Ô capsule thu nhỏ biến mất | `AB\d52a1a2e9d1a42ce8487e89c84c4cecf\Art\UI\Animation\Pet\collection\anui_pet_collecion_cell_out.anim` | 0.05 s |
| Nút hiện | `AB\c0a5fc313389c4ddca0413d7806e2378\Art\UI\Animation\Common\anui_common_button_xlong_in.anim` (+ `_normal`, `_none`) | 0.233 s |
| Animator nút (bấm) | `anui_pinball_btn_battle.controller` | (controller nút chung, không phải luồng capsule) |

### 1.2 Màn tổng kết "mở tất cả"

| Vai trò | File |
|---|---|
| **Bảng tổng kết thú nhận được** (tiêu đề "恭喜获得", lưới cuộn, nút "好的") | `AB\7498c240bcdaf647c9c7c450d8704e10\Res\UI\Prefabs\Common\pbui_a_view_pet_common_openall.prefab` |
| Clip vào bảng | `AB\91eb79317be49388dd673327a72b641d\Art\UI\Animation\PetCatch\anui_a_view_pet_catch_reward_in.anim` (0.367 s) |
| Ô thú trong bảng | `pbui_common_item_pet` (lồng), clip `anui_common_item_pet.anim` (0.667 s), `anui_common_item_pet_out.anim` (0.233 s) cùng thư mục PetCatch |
| Hạt nổ khi ô hiện | `pbvx_a_view_pet_catch_reward_burst` (lồng trong ô) |

### 1.3 Các bản capsule đơn của máy bi (để đối chiếu)

`AB\f7e0abe69e421aa56f457c21db3244ec\Res\UI\Prefabs\Common\pbui_common_reward_pinball_blue.prefab`, `..._green.prefab` (`AB\cc85cb...`), `..._purple.prefab` (`AB\24bbd8...`), gộp trong `pbui_common_reward_pinball_all.prefab` (`AB\9dc86d...`). Một capsule giữa màn, có chữ `x5` (số lượng), clip `anui_common_reward_pinball_blue/green/purple.anim` (1.1 s, event `open` ở 0.317 s), nhịp giống hệt bản `_in_new`. Âm thanh đi kèm: `sfx_pinball_odds_eggopen_bule/purple/close_1..3/collect` (`AB\3b067fc4953187229a93730dd1fa2af1\`).

### 1.4 Không phải luồng capsule (đã loại)

- `pbui_pinball_award_card_*` + `pbvx_pinball_cardout_*` (xanh, tím, vàng, đỏ; double, triple): đây là **thẻ thưởng của máy bi** (lật một thẻ, chạm để nâng hạng "点击升级奖励！", "奖励升级 / 奖励大升级 / 惊喜大升级"), không phải capsule. Bốn màu xanh/tím/vàng/đỏ người chơi nhớ là của thẻ này. Capsule thú chỉ có **xanh dương, lục, tím**.
- `pbui_a_view_pet_catch_*`: màn "bắt thú" (nút bắn, giỏ bắt), chỉ dùng chung bảng tổng kết.
- Không có Timeline (`.playable`) nào cho capsule; Timeline duy nhất có chữ egg là `tlvx_hiddenegg_skunk_fullscreen` (sự kiện chồn hôi ở Homestead, khác luồng).

## 2. Bố cục

### 2.1 Cây prefab màn chính (`pbui_common_reward`)

```
pbui_common_reward  (stretch, Canvas override)
└ anim  [Animation: anui_common_reward_in/out/none, LuaAnimationEventListener]
  ├ pbui_common_black
  │ └ animBG [Animation black_in/normal/out, CanvasGroup]
  │   ├ pbui_common_background_blur  RawImage màu (0,0,0,0.8) + ScreenShot (blur màn chụp, Hidden_FogBlur)
  │   ├ [OFF] img_black   Image (0,0,0,0.8)        (dự phòng khi không blur)
  │   └ [OFF] group_text/txt_hint "点击空白继续" (chạm chỗ trống để tiếp tục), pos (0,100) neo đáy
  └ safe_area [CanvasGroup]
    ├ [OFF] reward_title  pos (0,-107) neo đỉnh, 575x150, chữ "恭喜获得" vàng
    ├ [OFF] reward_01  170x205  (khuôn 1 capsule, Lua nhân bản ra từng điểm)
    │   └ anim [Animation: anui_pet_collecion_cell_out]
    │     ├ pbui_common_reward_blue   (xem 2.3)
    │     ├ [OFF] pbui_common_reward_purple
    │     ├ [OFF] num_count "x2"  neo (1,0), pos (-25,48), xoay -8°
    │     └ [OFF] imgup 92x92 pos (75,111)  (mũi tên "nâng cấp")
    ├ group_reward_5 .. group_reward_1   (điểm đặt, xem 2.2)
    ├ [OFF] pbvx_coloured_ribbon  pos (-4,873) (pháo giấy màu)
    └ group_btns  neo đáy, pos (0,98.25), cao 196.5  [HorizontalLayoutGroup padding 30/30, spacing 20, căn trái-trên, ép giãn ngang]
        ├ [OFF] btn_open        "打开" (Mở)            cao 100
        ├ [OFF] btn_next_group  "再开一组" (Mở nhóm nữa) + giá (icon txui_item_one + số "100")
        ├ [OFF] btn_openall     "开启全部" (Mở tất cả)
        └ [OFF] btn_confirm     "确定" (Xác nhận), preferred 570x100
```

Nút chia đều chiều ngang: 3 nút cùng hiện thì mỗi nút rộng **216.667**, tâm x = 138.3 / 375 / 611.7 (tính từ mép trái); 1 nút "确定" rộng 570 (preferred). Nút hiện bằng `anui_common_button_xlong_in` (mục 3.6). Không có nút "bỏ qua" riêng: chạm chỗ trống ("点击空白继续") để đi tiếp.

### 2.2 Toạ độ chỗ đặt capsule (anchoredPosition, tâm màn hình)

Mỗi `group_reward_N` là RectTransform 630x965, các điểm con 100x100. Toạ độ tuyệt đối = vị trí nhóm + vị trí điểm.

| Số capsule | Nhóm (pos) | Điểm (pos trong nhóm) | Toạ độ tuyệt đối | Hình |
|---|---|---|---|---|
| 1 | (0,12) | (0,16) | (0,28) | giữa |
| 2 | (0,12) | (-170,16), (170,16) | (-170,28), (170,28) | hàng ngang, cách nhau 340 |
| 3 | (0,12) | (-170,144), (170,144), (0,-205) | (-170,156), (170,156), (0,-193) | tam giác ngược: 2 trên, 1 dưới |
| 4 | (0,12) | (-170,144), (170,144), (-180,-205), (170,-205) | (-170,156), (170,156), (-180,-193), (170,-193) | lưới 2x2 (điểm dưới-trái lệch -10, có lẽ sót tay) |
| 5 | (0,114) | 1 (0,324), 2 (-215,41), 3 (-170,-306), 4 (170,-306), 5 (215,41) | (0,438), (-215,155), (-170,-192), (170,-192), (215,155) | **ngũ giác** đỉnh lên trên, đánh số theo chiều kim đồng hồ ngược: đỉnh, trái, dưới-trái, dưới-phải, phải |

Scale các điểm: 1 (không thu nhỏ khi nhiều capsule). Khuôn `reward_01` có pos (0,28) = đúng điểm của 1 capsule. Kích thước một ô capsule: 170x205; bên trong nhóm hình capsule đặt ở `anim` pos (0,-9) 200x200, rồi `#egg_group_pos` pos (0,-100) 200x250 pivot (0.5,0.1) (pivot gần đáy, nên lắc/phóng quanh đáy capsule).

### 2.3 Cây một capsule (`pbui_common_reward_blue`, bản tím khác ở mục 4)

Toạ độ trong `#egg_group` (gốc ~ đáy capsule). Thứ tự vẽ từ dưới lên:

| Nút | pos | size | scale / xoay | Nội dung |
|---|---|---|---|---|
| [OFF] `#img_bg_frameround_in_01` | (0,36) | 1000x1000 | | vòng sóng sau lưng, mat `mtvx_common_reward_flow_01`, màu (0.325,0.517,0.878,0.929) |
| `#egg_glow_back` | (0,34.61) | 200x100 | 0.981 | Animation `anui_common_reward_bg_loop` tự chạy (thở) |
| └ `#img_bg_frameround_01` | (0,0) | 300x320 | 0.85 | quầng sau capsule khi còn đóng, mat `mtvx_common_reward_one_bg_back_color_01`, màu (0.467,0.629,1,0.78) |
| `#group_egg` | (0,0) | | | gốc lắc khi mở |
| └ `#down_egg_group` (thân) | (3,-1) | | CanvasGroup | |
|   └ `#up_egg01` | (0,28.8) | 188x144 | pivot (0.5,0.7) | **thân capsule** `txvx_common_reward_blue_01` |
| └ `#up_egg_group` (nắp) | (3,75) | | CanvasGroup | |
|   ├ `#up_egg01` | (0,70.94) | 190x145.3 | pivot (0.5,1) | **nắp trong suốt** `txvx_common_reward_bg_01` |
|   └ `#up_egg02` | (0,-31.44) | 86x86 | pivot (0.5,0.25), xoay -4.9°, alpha 0.851 | **hình thú in mờ bên trong nắp** `txvx_common_reward_bg_02` |
| `#egg_glow_end_back` | (0,34.61) | 200x100 | CanvasGroup | lớp hiện sau khi mở |
| └ `#back_group` | | | | quầng màu độ hiếm sau thú: 2 lớp `txvx_common_reward_01` 206.5x232: lớp ngoài scale 1.05 màu (0.351,0,1,0.769), lớp trong scale 0.87 màu (0.476,0.846,1,1) |
| └ `pet_group` | (0,-40) | 100x100 | pivot (0.5,0.1) | chỗ gắn thú (`pet_node`, Lua gắn hình thú vào) |
| └ `#front_group` | | | | |
|   ├ `#img_bg_frameround_in_02` | (0,0) | 1000x1000 | 1.05 | vòng sóng loé (mat `mtvx_common_reward_flow_02`, màu (0.325,0.459,0.878,1)) |
|   └ `#img_bg_frameround_02` | (0,53) | 303.5x302 | (1.05,0.84) | quầng `txvx_common_mask_flow_00`, mat `mtvx_common_reward_glow_01`, alpha 0 |
| `#img_bg_frameround_01` | (0,44.15) | 300x300 | | **chớp loé** `txvx_common_mask_flow_00`, mat `mtvx_common_reward_glow_02`, alpha 0 lúc nghỉ |
| `#vx_particle_group` | (0,0) | | scale 0 + `UIParticle` | hạt: `#particle_glow` (pos (0,0.5), sc 2) > `#particle_circle`, `#particle_star`, [OFF] `#particle_line` |

Ngoài ra có `[OFF] img_egg` (bản capsule nguyên khối dùng để lắc, gồm `#img_egg` thân, `#img_egg_02` nắp, `#img_egg_03` hình thú) mà clip mở vẫn điều khiển song song.

**Nắp và thân là 2 mảnh tách**: thân là cái bát đục màu (188x144), nắp là vòm trong suốt (190x148), hình thú mờ (86x86) dán lên nắp. Ghép: tâm nắp cao hơn tâm thân khoảng 74–76 px.

### 2.4 Bảng tổng kết (`pbui_a_view_pet_common_openall`)

- Nền: như trên (blur màn chụp + đen 0.8), `anim` chạy `anui_a_view_pet_catch_reward_in`.
- `reward_title` neo đỉnh pos (0,-172) 575x150; chữ `txt_reward_title` pos (0,-28) "恭喜获得" (vật liệu vàng chuyển động `zh_cn_body_special_gold_move`). `[OFF] text_tis` "所有伙伴获得相同奖励".
- `scroll_reward`: stretch, pos (0,-49.9), sizeDelta (0,-436.3) (trừ 436 px trên dưới), cuộn dọc, đàn hồi 0.1. `content` rộng 656, VerticalLayout + ContentSizeFitter cao theo nội dung.
- `reward_list` **GridLayoutGroup cell 215x215, spacing 0, căn giữa-trên (alignment 1), tự xuống hàng** (constraint Flexible): với 656 px rộng là **3 ô/hàng**.
- Ô thú `pbui_common_item_pet` 170x205: `group_back` scale 0.75 chứa quầng màu (`egg_glow_back_blue`: 2 lớp 300x320 scale 0.85/0.8, mat `one_bg_back_color_01/02`, màu (0.467,0.629,1,0.78) và (0.467,0.535,1,0); `egg_glow_back_purple`: (0.609,0.297,1,0.412) và (0.467,0.535,1,1)), cả hai chạy `anui_common_reward_bg_loop`; `actor_node` scale 1.5 (hình thú); `num_count` "x2" pos (60,-54); `item_new` (nhãn "新" đỏ) pos (59.3,55.7); hạt nổ `pbvx_a_view_pet_catch_reward_burst` scale 1.3.
- `btn_confirm` "好的" neo đáy pos (0,105) 312x100.

## 3. Các pha và thời gian (keyframe)

Ký hiệu: `t:giá trị`, t tính bằng giây từ đầu clip. "EG" = `#egg_group_pos/#egg_group`. Góc là độ quanh trục Z (dương = ngược chiều kim đồng hồ). Giữa các key Unity nội suy theo tangent (đa phần mượt, key "step" ghi rõ).

### 3.1 Vào màn (`anui_common_reward_in`, 2.167 s) + nền tối

| Thời điểm | Việc |
|---|---|
| 0 | `pbui_common_black` alpha 1, `safe_area` alpha 1 (nền blur hiện ngay; `anui_common_black_in` riêng: alpha 0 → 1 trong **0.083 s**) |
| 0.017 → 0.067 | `reward_title` alpha 0 → 1 |
| 0 → 0.167 → 0.333 | `reward_title` y: 20 → -81.9 → -75; scale 2 → 0.95 → 1 (chữ đập xuống, nảy nhẹ) |
| **2.0** | event `OnAnimationEvent("single")` |
| **2.167** | event `OnAnimationEvent("multi")` |

Clip không có key nào cho capsule: **capsule bay vào chỗ và lơ lửng do Lua tween**, không có số trong bản đục. Hai event ở 2.0 / 2.167 s là chỗ Lua bắt đầu thả capsule (1 capsule / nhiều capsule) (suy luận theo tên). Ghi chú: `reward_title` trong prefab đang tắt; clip cũng bật `pbvx_battle_result_win` 0.2 → 2.167 nhưng nút này không có trong prefab (clip dùng chung, đường dẫn hụt).

Thứ duy nhất "thở" có trong clip: `#egg_glow_back` (quầng sau capsule) chạy `anui_common_reward_bg_loop` **lặp 6 s: scale 0.9 (0 s) → 1.0 (1.75 s) → 0.9 (6 s)**, tangent 0 ở các key (ease in-out). Capsule đóng ở trạng thái do clip `_in` (1 khung) đặt:

| Clip đặt | thân `#down_egg_group` pos | nắp `#up_egg_group` pos | tắt |
|---|---|---|---|
| `anui_common_reward_blue_in` | (4,-5), 0°, alpha 1 | (6,69), 0°, alpha 1 | `#egg_glow_end_back`, `#img_bg_frameround_01`, `#vx_particle_group`, `img_egg` |
| `anui_common_reward_purple_in` | (2.2,0.5) | (3.1,73.3) | như trên |
| `anui_common_reward_green_in` | (4,-5) | (3.4,65.8) | như trên |

### 3.2 Chạm: lắc, nứt, mở (`anui_common_reward_blue_in_new` = `purple_new` = `pinball_*`, 1.1 s)

**Lắc (0 → 0.25 s)**, áp cho `EG/#group_egg` (và `img_egg`):

| t | 0 | 0.033 | 0.05 | 0.067 | 0.083 | 0.1 | 0.117 | 0.133 | 0.15 | 0.167 | 0.183 | 0.217 | 0.25 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| góc Z | 0 | **+7.1** | 4.6 | 0 | **-2.5** | 0 | 4.6 | **+7.1** | 4.6 | 0 | **-2.5** | **+7.1** | -2.5 |

Lắc lệch về phía dương (+7.1 / -2.5), chu kỳ ~0.1–0.133 s, 2.5 nhịp. Pivot nhóm ở gần đáy capsule (0.5,0.1) nên capsule lắc như con lật đật.

Scale `#group_egg`: **0:1 → 0.25:0.8 (nén dần trong lúc lắc) → 0.3:1.2 (bật phồng) → 0.333:0.8**.

**Bật nắp (0.3 s)**: event `OnAnimationEvent("open")` ở **0.3 s** (bản máy bi 0.317 s), chỗ Lua phát tiếng mở và gắn thú (suy luận).

| Mảnh | t | pos | góc | scale | alpha |
|---|---|---|---|---|---|
| Nắp `#up_egg_group` | 0 → 0.3 | (5.06,74.37) | -4 | 1.05 | 1 |
| | 0.333 | **(47,274)** (vọt +42,+200 trong 2 khung) | **-45.5** | 1.05 | 1 |
| | 0.35 / 0.367 | | -40.6 / -31.6 | | ảnh bắt đầu mờ ở 0.367 |
| | 0.383 | (44,262) | -26.7 | | |
| | 0.433 | | | | ảnh = 0 |
| | 0.45 | (42,163) (rơi xuống) | | | |
| | 0.467 | | | **0.3** | tắt (IsActive 0) |
| Thân `#down_egg_group` | 0 → 0.3 | (0.8,-2.6) | -2 | 1.05 | 1 |
| | 0.333 | **(26,-166)** (rơi -163 trong 2 khung) | **+25.7** | 1.05 | |
| | 0.35 / 0.367 / 0.383 | (28,-162) ở 0.383 | 22.4 / 16.2 / 12.9 | | mờ dần từ 0.367 |
| | 0.433 | | | | 0 |
| | 0.45 | (27.9,-165.5) | | | |
| | 0.467 | | | 0.3 | tắt |
| Hình thú mờ trên nắp (`img_egg/#img_egg_03`) | 0.333 | (49,229) | -45.5 | | |
| | 0.45 | (42,163) | | 0.3 ở 0.467 | 0.367:1 → 0.433:0 |

Tóm lại: nắp văng lên-phải, nghiêng 45° theo chiều kim đồng hồ; thân rơi xuống-phải, nghiêng 26° ngược chiều; cả hai đi gần hết quãng trong **2 khung (0.033 s)** đầu, sau đó chậm lại, mờ trong 0.367–0.433 và co còn 0.3 trước khi tắt ở 0.467. Không có hình capsule nứt riêng (không có sprite vết nứt); "nứt" chỉ là lắc + nén.

### 3.3 Loé (0.317 s)

| Lớp | Thuộc tính | Key |
|---|---|---|
| `EG/#img_bg_frameround_01` (quầng tròn mềm 300x300, cộng sáng) | alpha | 0:0, 0.3:0, **0.317:1**, 0.45:0 |
| | màu rgb | 0:(1,1,1) → 0.317:(0.373,0.746,1) → 0.5:(0,0.285,1) (trắng → xanh nhạt → xanh đậm) |
| | scale | 0.317:0.98 → **0.5:1.79** |
| `EG/#egg_glow_end_back` | alpha | 0:0, 0.3:0, **0.317:1**; `#back_group` bật ở 0.333 |
| `#front_group/#img_bg_frameround_in_02` (vòng sóng 1000x1000) | alpha | 0:1 … 0.35:1 → **0.433:0** |
| | `vectorValue1.x` (bán kính vòng trong shader, VxAnimationController) | 0:0 (step) → **0.317:1.76** → 0.433:1.68 |
| | `vectorValue1.z` | 0 → 0.433:0.1 (xanh); 0.317:0.18 (tím, lục) |
| | `vectorValue2.w` / `.z` | 0:0.05 → 0.4:0.1 → 0.433:0 / 0 → 0.317:0.01 → 0.433:0 |
| `EG/#vx_particle_group` | IsActive | **0.317: bật** (hạt mục 5) |

### 3.4 Thú nhảy ra (`pet_group`, 0.317 → 1.1 s)

| t | 0.317 | 0.367 | 0.45 | 0.617 | 0.683 | 0.7 | 0.717 | 0.833 | 0.933 | 1.1 |
|---|---|---|---|---|---|---|---|---|---|---|
| pos y | **-40** | 1.5 | **8.4** | 2.2 | | **-40** | | | | |
| scale (x,y) | **(1, 2.5)** | | (1.5,1.5) | | (1,1.067) | | **(1.3,0.9)** | (0.95,1.1) | (1,1) | (1,1) |

Thú bật ra kéo dài theo chiều dọc (1 x 2.5), nảy cao ~48 px, phình 1.5 lúc ở đỉnh, rơi về y -40 ở 0.7 s rồi nén bẹt (1.3 x 0.9) khi chạm đất, nảy lại (0.95 x 1.1), đứng yên ở 0.933 s. (Bản `greed_new_center` chỉ nảy tới y 0.5 ở 0.45 rồi giữ.)

Bản clip cũ `anui_common_reward_blue` (nhịp khác): `pet_group` scale 0.333:1 → 0.383:1.214 → **0.4:2.0** → 0.417:1.96 → 0.583:1.133 → 0.933:1; `#back_group` 0.317:1 → 0.433:1.249 → 0.65:1.036 → 0.967:1; `#front_group` scale 0:0.2 → 0.25:-0.244 → 0.35:0.2 → 0.417:1.023 (vòng loé lật ra).

### 3.5 Thu capsule đã mở (`anui_common_reward_get`, 0.4 s) và ô biến mất

| Nút | Key |
|---|---|
| root capsule | scale 0:1 → **0.233:0.5** |
| `EG` | alpha 0.233:1 → **0.25:0** |
| `#egg_glow_end_back` | alpha 1 (0 → 0.35) |
| `#img_bg_frameround_in_01` (vòng sau) | `_vector1.x` 0.067:1.65 → 0.233:1.807 → 0.4:1.83 |
| `#vx_particle_group` | tắt |

Ô `reward_01` sau đó chạy `anui_pet_collecion_cell_out`: scale 0:1 → 0.033:0.7 → **0.05:0** (tắt gần như tức thì).

### 3.6 Nút và bảng tổng kết

- Nút (`anui_common_button_xlong_in`, 0.233 s): alpha 0 → 1 trong 0.05 s; scale 0:(0.8,0.8) → 0.117:(1.2,1.2) → 0.233:1.
- Bảng tổng kết vào (`anui_a_view_pet_catch_reward_in`, 0.367 s): nền đen alpha 0 → 1 trong 0.083 s; tiêu đề alpha 0 → 1 trong 0.05 s; chữ tiêu đề scale (x,y): 0:(1.285,2.29) → 0.117:(1.126,2.12) → 0.167:(0.671,1.358) → 0.233:(1.062,0.9) → 0.3:(0.95,1.075) → 0.367:(1,1) (đập, nén ngang, nảy dọc). `group_count` alpha 0.2 → 0.283.
- Mỗi ô thú (`anui_common_item_pet`, 0.667 s):

| Nút | Key |
|---|---|
| `actor_node` (hình thú) | alpha 0:0 → 0.067:1; scale 0:1.522 → **0.083:2.363** → 0.217:1.963 → 0.35:2.0 (scale nghỉ trong prefab 1.5; clip đẩy lên 2.0) |
| `group_back` (quầng màu) | alpha 0.217:0 → 0.267:1 |
| `item_new` (nhãn mới) | alpha 0.25:0 → 0.317:1; scale 0.25:1.151 → 0.35:1.288 → 0.45:1.203 |
| hạt `pbvx_a_view_pet_catch_reward_burst` | bật 0.067 → 0.45; `#vx_burst` bật 0 → tắt 0.667 |

- Ô biến mất (`anui_common_item_pet_out`, 0.233 s): scale 1 → 0.5, alpha 0.167:1 → 0.233:0.
- Khoảng cách thời gian giữa các ô hiện lần lượt: do Lua, không có trong bản đục.

### 3.7 "Mở tất cả" (suy luận từ cấu trúc)

Không có clip riêng cho "mở tất cả". Cấu trúc cho thấy: nút `btn_openall` "开启全部" nằm cạnh `btn_open` "打开" và `btn_next_group` "再开一组" trong `pbui_common_reward`; mỗi capsule là một bản sao độc lập có clip mở riêng, nên "mở tất cả" là Lua cho chạy `*_in_new` trên mọi capsule chưa mở (lệch nhau bao nhiêu thì không đọc được), rồi mở bảng `pbui_a_view_pet_common_openall` liệt kê toàn bộ thú (lưới 3 cột, ô 215). Event `single` / `multi` của clip vào màn khớp hai nhánh: 1 capsule (mở luôn, chạm chỗ trống để tiếp) và nhiều capsule (hiện nút).

### 3.8 Trình tự gợi ý để dựng lại

| Pha | Thời gian |
|---|---|
| Nền blur + đen 0.8 hiện | 0 → 0.083 s |
| (tiêu đề đập xuống, nếu dùng) | 0 → 0.333 s |
| Capsule bay vào chỗ (Lua, tự chọn) | event ở 2.0 s (có thể rút ngắn) |
| Đứng chờ: quầng sau thở 0.9 ↔ 1.0 | chu kỳ 6 s |
| Chạm: lắc + nén | 0 → 0.25 s |
| Bật phồng 1.2, event `open` | 0.3 s |
| Nắp văng / thân rơi | 0.3 → 0.333 s (nhanh), mờ 0.367 → 0.433, tắt 0.467 |
| Loé tròn + vòng sóng + hạt | 0.317 s, loé tắt 0.45, vòng tắt 0.433 |
| Thú nhảy ra, nảy, đứng yên | 0.317 → 0.933 s |
| Clip mở kết thúc | 1.1 s |
| Thu capsule (scale 0.5, mờ) | 0.4 s, ô co về 0 trong 0.05 s |
| Bảng tổng kết vào, từng ô 0.667 s | |

## 4. Khác biệt theo độ hiếm

Capsule thú chỉ có 3 màu: **xanh dương** (thường), **lục**, **tím** (hiếm). Không có capsule vàng hay đỏ (vàng/đỏ là thẻ thưởng máy bi, mục 1.4). Clip mở mới (`_in_new` / `_new` / `greed_new_center` / `pinball_*`) có **cùng nhịp, cùng thời lượng 1.1 s, cùng lắc**; khác nhau ở màu, số lớp quầng và số hệ hạt.

| | Xanh dương | Lục | Tím |
|---|---|---|---|
| Thân capsule | `txvx_common_reward_blue_01` (trung bình rgb 66,82,179) | `txvx_common_reward_pgreen_01` (87,126,71), miệng viền tím | `txvx_common_reward_purple_01` (122,42,179) |
| Nắp, hình thú trên nắp | dùng chung `bg_01`, `bg_02` | chung | chung |
| Quầng khi còn đóng (`#egg_glow_back`) | 1 lớp 300x320 sc 0.85, mat `one_bg_back_color_01` (quầng tròn), màu (0.467,0.629,1,0.78) | 1 lớp, mat `one_bg_back_color_03` (alpha-blend), (0.42,0.549,1,0.384) | **2 lớp**: (0.609,0.297,1,0.412) + lớp 500x500 sc 0.8 mat `one_bg_back_color_02` = **tia sáng toả** (shader volume light, polar mask `txvx_common_mask_flow_03`, màu `_Color2` (0.682,0,1)) |
| Quầng sau thú khi mở (`#back_group`, `txvx_common_reward_01`) | **2 lớp**: sc 1.05 (0.351,0,1,0.769), sc 0.87 (0.476,0.846,1,1) | 2 lớp, sc 0.75 cả nhóm: sc 1.05 (0.157,0.695,0.98,0.769), sc 0.87 (0.584,0.962,1,1) | **3 lớp**: sc 1.15 (0.516,0,1,0.871), sc 1.02 (0.679,0.373,1,0.439), sc 0.83 (0.93,0.467,1,1) |
| Vòng sóng `#img_bg_frameround_in_02` | (0.325,0.459,0.878) | lúc mở đổi sang (0.505,1,0) (máy bi) hoặc (0,0.551,1) (`greed_new_center`) | (0.816,0.327,0.877) |
| `vectorValue1.z` vòng sóng | 0 → 0.1 | 0.18 | 0.18 |
| Màu chớp `#img_bg_frameround_01` lúc 0.317 | (0.373,0.746,1) | (0.562,1,0) (máy bi) / (0,0.762,1) | như xanh (clip dùng chung) |
| Hệ hạt khi mở | 3: glow, circle (halo mờ), star x7; line tắt | glow; star và line tắt | **5 + 1 lặp**: glow (to hơn, đời 0.6), circle_glow, circle (halo rõ), star x6 x2 đợt, line x4 x3 đợt, **particle_loop** sao lấp lánh lặp mãi |
| Lắc (clip cũ `anui_common_reward_blue` / `_purple`) | 0 → 0.267 s, góc 0:1.4, 0.05:2.2, 0.1:9.4, 0.15:2.2, 0.2:9.4, 0.25:3.8, 0.267:0.9 | | **0 → 0.433 s**, góc 0:-2.2, 0.083:3.2, 0.15:-3.3, 0.217:5.5, 0.283:-3.3, 0.35:5.5, 0.383:1.7, **0.4:10.2**, 0.417:4, 0.433:0.9 (cú cuối mạnh nhất); bật nắp muộn hơn 0.117 s; clip dài 1.45 s so với 0.983 s |

Rung màn hình: không có key rung camera hay rung toàn màn trong clip nào của luồng này. Thời gian giữ sau khi mở (trước khi thu) do Lua quyết, không có trong bản đục.

## 5. Hệ hạt

Hạt của capsule nằm trong `#vx_particle_group` có `UIParticle` (Coffee UIParticle) **m_Scale3D = 78** (1 đơn vị hạt ≈ 78 px UI), `IgnoreCanvasScaler` bật. Tất cả `playOnAwake`, không lặp (trừ ghi chú), giả lập Local, scalingMode Local (cỡ nhân thêm scale của chính transform: bản xanh `#particle_glow` và con có scale 2). Bật bằng `m_IsActive` ở 0.317 s trong clip mở. Hình dạng phát "SingleSidedEdge" = đoạn thẳng ngang (bán kính = nửa chiều dài).

### 5.1 Capsule xanh

| Hệ | Đời (s) | Phát | Tốc | Cỡ (đv; ≈px) | Màu theo đời | Vật liệu / blend |
|---|---|---|---|---|---|---|
| `#particle_glow` (quầng loé) | 0.4 | 1 hạt tức thì | 0 | 3 x sc2 (≈468 px), co 0.924 → 0.379 | rgb (0.533,0.786,1) → 0.42:(0.184,0.618,1) → (0.005,0.111,1); alpha 1 đến 42% rồi → 0; màu đầu alpha 0.561 | `mttx_skill_common_glow_add`, tex `txfx_common_glow` (quầng tròn mềm), **cộng (One, Zero → shader Mobile Particles Additive dựng sẵn)** |
| `#particle_circle` (vòng halo) | 0.2 | 1 | 0 | 2 x sc2 (≈312 px), lớn 0.417 → 1 | trắng → (0.184,0.618,1) → (0.005,0.111,1); alpha 1 → 0.985 (63%) → 0 | `mtvx_evolution_halo_blur`, shader vẽ hình tròn thủ tục (`EffectParticleShapeUI`), SrcAlpha + One (**cộng**) |
| `#particle_star` (sao văng) | 0.2–0.4 | 7 hạt, trễ 0.1 s | 1–5 đv/s, hãm `dampen 0.2` | 0.3–1, cỡ theo đời 0.242 → 0.939 (18%) → 0.068 | màu ngẫu nhiên từ dải trắng / (0.571,0.837,1) / (0.573,1,0.939) | `mtvx_uicommon_star_02`, tex `txvx_star_glow` (sao 4 cánh), SrcAlpha / 1-SrcAlpha (thường) |
| [OFF] `#particle_line` | 0.15–0.2 | 4 x 2 đợt cách 0.1 s | 2–5 | 0.3–0.7 x 0.5–1.5 (kéo dài) | như sao | `mtvx_common_light_line` (vệt sáng), render Stretch, cộng |

### 5.2 Capsule tím (thêm lớp)

| Hệ | Đời | Phát | Tốc | Cỡ | Màu | Vật liệu |
|---|---|---|---|---|---|---|
| `#particle_glow` | 0.6 | 1 | 0 | 6 (≈468 px), 0.742 → 1 (18%) → 0.63 → 0.379 | như xanh | glow add |
| `#particle_circle_glow` | 0.3 | 1 x 2 đợt (0.1 s), trễ 0.1 | 0 | 4.8 (≈374 px) 0.417 → 1 | trắng → (0.82,0.184,1) → (0.45,0.004,1) | halo blur, cộng |
| `#particle_circle` | 0.3 | 1 x 2 đợt, trễ 0.1 | 0 | 4 (≈312 px) | như trên | `mtvx_evolution_halo` (vòng nét rõ), cộng |
| `#particle_star` | 0.4–0.6 | 6 x 2 đợt, trễ 0.1 | 5–10, hãm 0.2 | 0.2–0.6 (≈16–47 px) | trắng / vàng (1,0.915,0.316) / hồng (1,0.573,0.989) | `mtvx_star_alphablend` (Mobile Particles Alpha Blended dựng sẵn) |
| `#particle_line` | 0.15–0.25 | 4 x 3 đợt | 2–5 | 0.2–0.3 x 1–2 (scale nút (2,2,1)) | trắng / (0.82,0.573,1) / hồng | light line, Stretch lenScale 1.5, cộng |
| `#particle_loop/#particle_star` (**lặp**) | 0.4–0.6 | 3 hạt/s + 1–3 lúc đầu | 0–1, hãm 0.3 | 0.2–0.6 | trắng / vàng / hồng | `mtvx_uicommon_star_02` |

### 5.3 Hạt nổ ở ô tổng kết (`pbvx_a_view_pet_catch_reward_burst`, ô scale 1.3)

Đơn vị ở đây là đơn vị canvas (không có UIParticle bọc), số giữ nguyên.

| Hệ | Đời | Phát | Tốc | Cỡ | Màu | Vật liệu |
|---|---|---|---|---|---|---|
| `glow2` | 0.3 | 2 | 0 | 1.05, cỡ theo đời x400: 0.181 → 0.843 (23%) → 1 | trắng → vàng (1,0.909,0.344) → (1,0.759,0.165) → cam (1,0.542,0); alpha 1 → 0.42 (29%) → 0 | `mtvx_pinball_glow_03` (quầng tròn) |
| `glow` (tia chấm) | 0.3–0.7 | 6, trễ 0.1 | 11–22, giới hạn tốc giảm dần | 0.23–0.35 x 0.15–0.55, Stretch | (1,0.857,0.307) | `mtvx_common_glow_dot_add` |
| `circle` / `circle2` | 0.3 | 1 / 1 | 0 | 9 / 10, xoay ±30°, 0.214 → 0.813 → 1 | trắng → vàng → cam; tắt ở 86–99% đời | vòng thủ tục, cộng |
| `smoke_tile_small` | 0.45–0.5 | 5 | 1–3 | 0.15–0.7 | trắng, alpha 0.1 → 1 → 0.16 | `mtfx_rob_unbox_smoke_tile` (2 khung khói), alpha-blend |
| `stars` + `starsub` | 0.3–0.5 / 0.1–0.2 | 2–3 x 2 đợt; con 30% sinh hạt chết | 20–300, hãm | 50–100 | trắng / tím (0.599,0.401,1) / vàng / cam | `mtvx_uicommon_star` (sao 4 cánh) |

Ngoài ra 3 `ParticleImage` (hạt nướng sẵn `pbvx_a_view_pet_catch_reward_brust_group_bake_0/1/2`) chồng lên, không đọc được thông số.

### 5.4 Pháo giấy (`pbvx_coloured_ribbon`, tắt sẵn trong prefab, có lẽ bật khi ra thú hiếm)

3 hệ lặp 2 s, đời 4 s / 1.5 s, phát 2–4 hạt/s, rơi y -3 … -12 đv/s, lắc ngang ±1…±4, nhiễu 0.5–1; texture `txvx_rob_earnings_colorpaper` (sheet 2x2 mảnh giấy); màu ngẫu nhiên xanh ngọc (0.502,0.945,0.98) / vàng (1,0.957,0.51) / lục (0.38,0.855,0.655) / hồng (1,0.569,1); cộng.

## 6. Texture: hình dạng

| Texture | Cỡ (px) | Hình |
|---|---|---|
| `AB\3ec31f77db6f6f087dd79942c090e583\Art\UI\Textures\common_reward\txvx_common_reward_blue_01.png` | 188x144 | **Nửa dưới capsule**: cái bát nhìn chéo từ trên, miệng elip thấy lòng trong màu tối, thân bóng có mảng sáng loang; viền xanh đậm dày. Nền trong suốt, thân đục |
| `..._purple_01.png` / `..._pgreen_01.png` | 188x144 | cùng hình, tím / lục (bản lục có viền miệng tím và viền ngoài đen) |
| `..._bg_01.png` | 190x148 | **Nắp vòm** (bán cầu) màu tím-trắng nhạt vẽ giả kính: mảng sáng lớn bên trái, vạch phản chiếu; viền xanh tím, đáy vòm có gờ. Ảnh đục (alpha 255), không trong suốt thật |
| `..._bg_02.png` | 86x86 | **Hình thú cách điệu** (mặt mèo tai nhọn, 2 mắt tròn, miệng cười) màu xanh tím đặc, dán lên nắp ở alpha 0.85 |
| `..._01.png` | 381x381 | quầng tròn trắng mềm (gradient tâm → mép), tô màu bằng `Image.color` |
| `..._design_01.png` | | trắng trống (bản phác) |
| `AB\3f90ef4811eee3736a261e4d72f13930\Art\UI\Textures\VX\txvx_common_mask_flow_00.png` | 128x128 | quầng tròn mềm trên nền đen (không alpha, dùng như mặt nạ cộng sáng) |
| `...\VX\txvx_common__mask_flow_01.png` | 64x64 | quầng tròn xám (mặt nạ cho vòng sóng, lặp x10 / x5 trong shader) |
| `...\VX\txvx_common_mask_flow_03.png` | 16x128 | dải gradient dọc (mặt nạ cực để vẽ tia toả) |
| `AB\e23baf9838cf23ca6dc17996699b30c6\Art\Fx\Texture\txfx_common_glow.png` | 128 | quầng tròn trắng |
| `...\txvx_star_glow.png` | 256 | sao 4 cánh mềm, cánh ngang dài hơn |
| `...\txvx_uicommon_star.png` | 128 | sao 4 cánh nét hơn |
| `...\txvx_common_light_line.png` | 256x128 | vệt sáng nằm ngang, hai đầu nhọn |
| `...\txvx_rob_earnings_colorpaper.png` | 256 | 4 mảnh giấy trắng (2x2): chữ nhật, vòng cong, giọt, tròn |
| `txfx_rob_unbox_smoke2.png` | 128x256 | 2 cụm khói kem (sheet 1x2) |

Capsule **tách 2 mảnh** (thân, nắp) + 1 hình dán (thú trên nắp). Không có ảnh capsule nứt, không có mảnh vỏ vỡ, không có bục đứng, không có ảnh tia toả vẽ sẵn (tia toả của bản tím là shader).

## 7. Hình cần vẽ

Ký hiệu loại: **VẼ** = hình có nét, nhờ GPT vẽ lại theo nét riêng; **CODE** = gradient / quầng mềm / hình học thuần, bên mình sinh bằng code. Cỡ gợi ý lấy đúng cỡ hiển thị trong game (vẽ to gấp 2–4 lần rồi thu nhỏ).

### 7.1 Capsule

| # | Hình | Tên gốc | Cỡ hiển thị (px) | Mô tả, trạng thái | Nền | Loại |
|---|---|---|---|---|---|---|
| 1 | Thân capsule (nửa dưới) | `txvx_common_reward_<blue/pgreen/purple>_01` | 188x144 (scale 1.05) | Bát nửa cầu nhìn chéo từ trên, thấy miệng elip và lòng trong tối; có mảng sáng trên thân. **3 bản màu**: xanh dương, lục, tím (bên mình có thể thêm vàng, đỏ nếu cần). Pivot quay ở (0.5,0.7) | trong suốt, thân đục | VẼ |
| 2 | Nắp capsule (nửa trên) | `txvx_common_reward_bg_01` | 190x148 (pivot (0.5,1), đáy nắp chồng miệng bát) | Vòm bán cầu giả kính, màu nhạt, mảng sáng lớn, gờ ở đáy vòm. Dùng chung mọi màu (hoặc vẽ thêm bản theo màu) | trong suốt, thân đục (vẽ giả trong) | VẼ |
| 3 | Hình dán trên nắp | `txvx_common_reward_bg_02` | 86x86, xoay -4.9°, alpha 0.85 | Biểu tượng thú (mặt thú cách điệu), 1 màu đặc; game mình thay bằng biểu tượng riêng | trong suốt | VẼ |
| 4 | Capsule nứt | (không có) | | Game gốc không có; nếu muốn thêm thì 1 lớp vết nứt phủ lên thân + nắp | trong suốt | VẼ (tuỳ chọn) |
| 5 | Mảnh vỡ vỏ | (không có) | | Game gốc không có (nắp/thân văng nguyên khối) | | không cần |

Capsule ghép: nắp đặt trên thân, tâm nắp cao hơn tâm thân ~74 px (ở cỡ 188 px).

### 7.2 Nền, quầng, tia, loé

| # | Hình | Tên gốc | Cỡ | Mô tả | Loại |
|---|---|---|---|---|---|
| 6 | Nền tối | (RawImage) | toàn màn | Ảnh chụp màn hình làm mờ + phủ đen alpha 0.8 | CODE |
| 7 | Quầng sau capsule (đứng chờ) | mat `one_bg_back_color_01` (+ tex `mask_flow_00`) | 300x320 x0.85 | Quầng tròn mềm màu theo độ hiếm, thở 0.9 ↔ 1.0 / 6 s | CODE |
| 8 | Tia toả sau capsule tím | mat `one_bg_back_color_02` (polar mask `mask_flow_03` + noise) | 500x500 x0.8 | Các tia sáng toả từ tâm (shader volume light) | CODE (hoặc VẼ 1 hình tia nếu muốn có nét) |
| 9 | Quầng màu sau thú | `txvx_common_reward_01` | 206.5x232, 2–3 lớp scale 0.83–1.15 | Quầng tròn trắng mềm, tô màu theo độ hiếm | CODE |
| 10 | Chớp loé tròn | `txvx_common_mask_flow_00` + mat `glow_02` | 300x300, phóng 0.98 → 1.79 | Đĩa sáng mềm cộng sáng, trắng → xanh | CODE |
| 11 | Vòng sóng | `txvx_common__mask_flow_01` + shader dissolve | 1000x1000 | Vòng sáng lan ra, mờ dần | CODE (vẽ vòng bằng shader hoặc ảnh vòng gradient) |
| 12 | Vòng halo (hạt) | shader thủ tục | 312–374 px | Vòng tròn mảnh / mờ, lớn dần | CODE |
| 13 | Quầng loé (hạt) | `txfx_common_glow` | ≈468 px | Quầng tròn mềm | CODE |

### 7.3 Hạt có hình

| # | Hình | Tên gốc | Cỡ texture | Mô tả | Loại |
|---|---|---|---|---|---|
| 14 | Sao lấp lánh 4 cánh | `txvx_star_glow` / `txvx_uicommon_star` | 256 / 128 | Sao 4 cánh, cánh ngang dài hơn; game gốc là sao mềm phát sáng. Muốn hợp nét vẽ tay thì cho GPT vẽ 1 sao 4 cánh có viền | VẼ (hoặc CODE nếu giữ kiểu mềm) |
| 15 | Vệt sáng | `txvx_common_light_line` | 256x128 | Vệt ngang nhọn hai đầu, mềm | CODE |
| 16 | Chấm sáng kéo dài | `txvx_common_glow_dot` | 128 | Chấm tròn mềm (dùng Stretch) | CODE |
| 17 | Khói | `txfx_rob_unbox_smoke2` | 128x256 (2 khung) | 2 cụm khói tròn màu kem | VẼ |
| 18 | Pháo giấy | `txvx_rob_earnings_colorpaper` | 256 (2x2) | 4 mảnh giấy trắng (chữ nhật, cong, giọt, tròn), tô màu bằng hạt | VẼ (đơn giản, có thể CODE) |

### 7.4 Giao diện

| # | Hình | Tên gốc | Cỡ | Mô tả | Loại |
|---|---|---|---|---|---|
| 19 | Nút dài (Mở / Mở tất cả / Mở nhóm nữa / Xác nhận / Được) | sprite 9-slice trong atlas `Common` + hoạ tiết kim cương `mtui_pattern_diamond` | 216.667x100 (3 nút) / 570x100 / 312x100 | Nền nút bo góc, có lớp hoạ tiết kim cương mờ bên trong; trạng thái normal, disable (xám) | VẼ (9-slice) |
| 20 | Biểu tượng giá ở nút "Mở nhóm nữa" | `txui_item_one` | 80x80 | Biểu tượng vật phẩm tiền mở | VẼ |
| 21 | Nhãn "mới" | 9-slice đỏ (atlas Common) | cao 32 | Viên thuốc đỏ (1,0.005,0.005) chữ "新" | VẼ hoặc CODE (bo góc) |
| 22 | Mũi tên nâng cấp | `imgup` (atlas Common) | 92x92 | Mũi tên lên | VẼ |
| 23 | Ô thú trong bảng tổng kết | (không có khung) | 170x205, ô lưới 215 | Game gốc không vẽ khung ô: chỉ có quầng màu (mục 9) + hình thú + số "x2" | CODE (quầng) |
| 24 | Chữ tiêu đề "Chúc mừng nhận được" | font + vật liệu vàng chuyển động | 575x150 | Chữ vàng viền | dùng font, không vẽ |

### 7.5 Không có trong luồng capsule

Bục đứng, thẻ theo độ hiếm, khung ô thưởng có viền, tia toả vẽ sẵn: **không có** trong luồng mở capsule thú. Thẻ xanh / tím / vàng / đỏ thuộc luồng thẻ thưởng máy bi (`pbui_pinball_award_card_*`, mặt sau `img_card_back_<blue/purple/gold/red>` 326x454 trong atlas `DemoPinball`, hiệu ứng `pbvx_pinball_cardout_*`); nếu cần sẽ đo riêng.
