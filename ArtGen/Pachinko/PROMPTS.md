# Pachinko: máy bi

Hình cho scene Máy Bi (spec `pachinko-machine`). Vật lý và vị trí đinh, ô do code quyết, nên ảnh chỉ là:
- **thân máy:** mặt chơi trống, code đặt đinh và vẽ ô lên trên;
- **các bộ phận rời:** đinh, nấm, cốc, máng, bi;
- **rương cỡ lớn:** cho hộp mở rương.

Khung máy trong code là 460 × 680 (tỉ lệ khoảng 0,68), gần đúng khổ 1024 × 1536 của GPT.

**Mặt máy đổi ngày 2026-11-02** (change `update-pachinko-feel`): cốc vàng nhỏ giữa máy thay bằng **két vàng**. Két có mái chữ ^ chừa khe ở đỉnh, một đinh gác trên khe, đáy chữ V có hai cọc. Dưới đáy két là **ô vàng khuất**, nên đáy máy có 11 ô. Ảnh bố cục mới là `../StyleRefs/R2b_MayBi_KetVang.png`; `R2_UI_Machine.png` là bố cục cũ, chỉ dùng để xem nét.

## Thân máy: gói file prompt (thay P1, 2026-11-04)

Thân máy giờ là tủ đỉnh vòm có bóng đèn, đầu máy có rãnh cho **thanh kinh nghiệm** (vòng cấp bên trái, hốc nút tỉ lệ bên phải). Bố cục học từ máy tham khảo; xem `GD_Claude/07_MayBi.md`, mục "Thanh kinh nghiệm và số theo cược".

- Gói sinh bằng `build.py` vào `gui_gpt/than_may/`: `luot_1_than_may.txt` (file gửi GPT) và `HUONG_DAN.md` (ảnh mẫu, chỗ lưu, cách soi, câu sửa nhanh).
- Ảnh bố cục `refs/bo_cuc_than_may.png` vẽ đúng khung máy trong game. Toạ độ từng phần (px ảnh và px khối máy) ghi ở `refs/bo_cuc_than_may.json`.
- GPT lưu vào `tai_ve/than_may.png`. Duyệt bằng `build.py --duyet`, rồi chạy menu Unity `PokiClash/Prefab/Máy bi: thân máy vẽ tay`. Ảnh đầu đã vào game ngày 2026-11-04.

P2–P4 dưới đây đã thành file prompt trong cùng gói (2026-11-04), lấy thân máy đã duyệt làm ảnh mẫu nét: `luot_2_bo_phan.txt` (12 bộ phận mặt máy), `luot_3_hieu_ung.txt` (P4 rút còn 6 hình game đang dùng), `luot_4_ruong.txt` (6 rương đóng và mở). Các mục P2–P4 bên dưới giữ để biết lịch sử. Ba tờ đã vào game ngày 2026-11-04. Duyệt lại bằng `build.py --duyet bo_phan|hieu_ung|ruong`, rồi trong Unity chạy `PokiClash/Dựng lại danh mục ảnh` và `PokiClash/Prefab/Máy bi: ảnh bộ phận`.

## Ảnh đính kèm

| Ảnh | Dùng cho |
|---|---|
| `../StyleRefs/R2b_MayBi_KetVang.png` | Bố cục máy hiện tại (ảnh tĩnh Unity vẽ từ code): vai nghiêng, 10 hàng đinh, 3 nấm, 2 cốc bạc, két vàng, 11 ô |
| `../StyleRefs/R2_UI_Machine.png` | Nét vẽ bản web (bố cục cũ) |
| `../UIKit/inbox/UI_Buttons.png` | Style đã chốt |
| `../guides/G_Sheet4x3.png`, `../guides/G_Sheet3x2.png` | Lưới đánh số |

Chỉ đính ảnh của dự án mình (quy tắc ở `../README.md`). Hiệu ứng P4 mô tả bằng chữ, không đính ảnh hay nhắc tên game khác.

## Danh sách ảnh

| ID | File (lưu vào `inbox/`) | Khung | Nền | Vẽ gì |
|---|---|---|---|---|
| P1 | `PK_Cabinet.png` | 1024 × 1536 | trong suốt quanh máy | Thân máy có mặt chơi trống |
| P2 | `PK_Parts.png` | 1536 × 1024 | trong suốt | 12 bộ phận rời |
| P3 | `PK_ChestsBig.png` | 1536 × 1024 | trong suốt | 3 rương đóng và mở, cỡ lớn |
| P4 | `PK_FX.png` | 1536 × 1024 | trong suốt | 12 hình hiệu ứng (loé, vòng, tia, sao), gần trắng để code tô màu |

**Thứ tự:** P1 → P2 → P3 → P4.

## Tin nhắn mở đầu

```
You are drawing a vertical pachinko machine for a mobile game whose look is a hand-drawn kid's adventure notebook
(attached UI_Buttons.png shows the approved style; R2b_MayBi_KetVang.png shows the current layout drawn by code,
with a golden vault in the lower middle). The game places pegs, bumpers, cups, the vault and slot labels itself, so
the cabinet must have an EMPTY play area. No text, no numbers, no characters. ONE IMAGE PER REPLY in order P1 to P4,
then wait for "next".
```

## P1 — Thân máy (`inbox/PK_Cabinet.png`)

```
1024 x 1536, transparent background around the machine. A cute tall pachinko cabinet seen straight from the front:
a thick warm wooden and cream frame with rounded top corners, doodled decorations (little stars, a pink ball emblem
at the top centre), crayon hatching, no shadow. Inside: one big flat cream play area with a faint dot
pattern, completely empty, its inner edge an ink line; along the top of the play area a thin rail for a launcher;
at the bottom an empty strip about 12 % of the height for the prize slots (just a darker cream band, no dividers).
Proportions of the play area about 460 wide by 680 tall.
```
**Sửa nhanh:** `Same cabinet; play area completely empty and flat, frame thinner so the play area is bigger.`

## P2 — Bộ phận (`inbox/PK_Parts.png`)

**Đính kèm thêm:** `G_Sheet4x3.png`, `PK_Cabinet.png`

```
12 separate parts on a transparent background, 1536 x 1024, one per cell of the attached numbered 4 x 3 grid:
1 a small dark metal peg seen from the front (a round head with a white highlight); 2 a red mushroom bumper cap
with white dots seen from above; 3 a small wooden half-round bump that sticks out of a wall; 4 a golden vault
roof: a shallow upside-down V made of two thick golden planks that do NOT touch at the top (a clear gap between
them), seen from the front; 5 a small silver cup with a tiny chest emblem; 6 a thin wooden slot divider post with a
round top; 7 a cute white cloud with two dot eyes holding nothing (the ball launcher); 8 a pink ball with a white
band; 9 a blue ball; 10 a golden ball; 11 a golden vault floor: a shallow V-shaped golden tray with a small round
knob at each end; 12 a soft yellow rectangular glow.
Same ink and crayon style as the cabinet.
```
Mảnh 2 (nấm) cắt ra lưu `Assets/03 Art/Pachinko/pk_bumper.png`: nấm giờ là hình động, phồng xẹp khi bị chạm; hình tạm cùng tên nằm trong `03 Art/Fallback`. Mảnh 4 và 11 ghép thành két vàng như trong `R2b_MayBi_KetVang.png`: mái ^ ở trên (khe giữa hai tấm rộng khoảng 1,4 lần bi), đáy V ở dưới, hai bên hông để hở.
**Sửa nhanh:** `Same parts; each smaller and simpler, fully inside its cell.`

## P3 — Rương lớn (`inbox/PK_ChestsBig.png`)

**Đính kèm thêm:** `G_Sheet3x2.png`, `../Icons/inbox/IC_Resources.png`

```
Six treasure chests on a transparent background, 1536 x 1024, one per cell of the attached 3 x 2 grid, each about
380 px, matching the chest icons in IC_Resources.png but more detailed: 1 wooden chest closed; 2 wooden chest open
with a soft golden glow and a few sparkles; 3 silver chest closed; 4 silver chest open with glow; 5 golden chest
closed with a red gem lock; 6 golden chest open with strong glow, coins and star sparkles flying out.
```
**Sửa nhanh:** `Same chests; open versions brighter inside, closed versions clearly locked.`

## P4 — Hiệu ứng (`inbox/PK_FX.png`)

**Đính kèm thêm:** `G_Sheet4x3.png`, `PK_Parts.png`

Hiệu ứng là hình tĩnh; code lo phóng to, xoay, mờ dần và tô màu. Mỗi hình gần trắng hoặc vàng rất nhạt, viền mực mảnh hoặc không viền, để một hình dùng được cho nhiều màu (rương gỗ, bạc, vàng). Code dùng như sau:

Ô có tên file thì code đang dùng hình tạm cùng tên trong `Assets/03 Art/Fallback` (vẽ bằng `Web/scripts/draw_machine_fx.py`). Cắt ô đó ra, lưu vào `Assets/03 Art/Pachinko/<tên>.png`, rồi chạy menu "PokiClash/Dựng lại danh mục ảnh". Code tự dùng ảnh gen thay hình tạm. Số hạt, thời gian và màu ghi ở `GD_Claude/07_MayBi.md`, mục "Hiệu ứng chép".

| Ô | Hình | File | Code làm gì |
|---|---|---|---|
| 1 | quầng tròn mềm | `fx_glow` | quầng sau đinh, nấm; quầng ô, rương, jackpot; chấm nhỏ |
| 2 | sao bốn cánh nhỏ | `fx_sparkle` | lấp lánh khi chạm đinh, sao bắn ra ở ô, cốc, rương |
| 3 | cột sáng dọc mềm, đậm ở đáy | (chưa dùng) | sáng ô đáy khi bi rơi vào (0,5 / 1,1 / 1,6 giây theo bậc) |
| 4 | vòng sáng tròn mảnh, rỗng giữa | `fx_ring` | vòng lan khi chạm nấm, vào cốc, rương, jackpot |
| 5 | sao năm cánh mập, viền mực mảnh, trong trắng | `fx_star` | sao bắn và sao lõi của jackpot, sao to của rương |
| 6 | chùm 3–4 đồng xu và lấp lánh | (chưa dùng) | +1 bi, nhạc mừng rương vàng |
| 7 | tia sáng toả tròn (12 tia mảnh) | (chưa dùng) | nền sau rương vàng trong hộp mở rương |
| 8 | 6–8 mảnh giấy màu nhỏ rời nhau | (chưa dùng) | bắn ra khi mở rương vàng |
| 9 | vệt mờ thuôn dài, đầu sáng bên phải | `fx_streak` | tia của jackpot, vệt hướng tâm ở ô, tia rương vàng |
| 10 | đám mây khói nhỏ | `fx_puff` | lúc thả bi từ máng |
| 11 | quầng vàng ôm hình két (mái ^ trên, đáy V dưới) | (chưa dùng) | két sáng khi bi lọt vào |
| 12 | vệt loé chéo ngắn | (chưa dùng) | ánh lướt qua rương trong khay |

```
12 separate visual-effect sprites on a transparent background, 1536 x 1024, one per cell of the attached numbered
4 x 3 grid, each fully inside its cell. They will be scaled, rotated, faded and tinted by code, so draw them almost
white or very pale yellow, soft and simple, with at most a thin ink outline, in the same hand-drawn crayon notebook
style as PK_Parts.png. No text, no characters, no background. 1 a small soft round glow; 2 a small four-pointed
sparkle star; 3 a tall soft vertical light column, brightest at the bottom, fading upward; 4 a thin soft round ring of light,
hollow in the middle; 5 a chubby five-pointed star, white inside with a thin ink outline; 6 a small cluster of three or four
coins with tiny sparkles; 7 radial light rays, twelve thin rays around an empty centre; 8 six to eight small paper
confetti pieces scattered apart; 9 a soft tapered streak, like a motion trail, horizontal; 10 a small puff of cloud
smoke; 11 a soft golden halo shaped like a shallow upside-down V on top and a shallow V below, hollow inside;
12 a short diagonal shine glint.
```
**Sửa nhanh:** `Same effects; paler and softer, thinner outlines, each smaller inside its cell.`

## Sau khi có ảnh

Claude ghép thân máy với khung 460 × 680 của code (đo mép trong mặt chơi), cắt bộ phận, lưu vào `Assets/03 Art/Pachinko/`.
