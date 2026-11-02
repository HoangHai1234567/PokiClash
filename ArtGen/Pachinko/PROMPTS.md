# Pachinko: máy bi

Hình cho scene Máy Bi (spec `pachinko-machine`). Vật lý và vị trí đinh, ô do code quyết, nên ảnh chỉ là:
- **thân máy:** mặt chơi trống, code đặt đinh và vẽ ô lên trên;
- **các bộ phận rời:** đinh, nấm, cốc, máng, bi;
- **rương cỡ lớn:** cho hộp mở rương.

Khung máy trong code là 460 × 680 (tỉ lệ khoảng 0,68), gần đúng khổ 1024 × 1536 của GPT.

## Ảnh đính kèm

| Ảnh | Dùng cho |
|---|---|
| `../StyleRefs/R2_UI_Machine.png` | Bố cục máy của bản web: vai nghiêng, 10 hàng đinh, 3 nấm, 3 cốc, 9 ô |
| `../UIKit/inbox/UI_Buttons.png` | Style đã chốt |
| `../guides/G_Sheet4x3.png`, `../guides/G_Sheet3x2.png` | Lưới đánh số |

## Danh sách ảnh

| ID | File (lưu vào `inbox/`) | Khung | Nền | Vẽ gì |
|---|---|---|---|---|
| P1 | `PK_Cabinet.png` | 1024 × 1536 | trong suốt quanh máy | Thân máy có mặt chơi trống |
| P2 | `PK_Parts.png` | 1536 × 1024 | trong suốt | 12 bộ phận rời |
| P3 | `PK_ChestsBig.png` | 1536 × 1024 | trong suốt | 3 rương đóng và mở, cỡ lớn |

**Thứ tự:** P1 → P2 → P3.

## Tin nhắn mở đầu

```
You are drawing a vertical pachinko machine for a mobile game whose look is a hand-drawn kid's adventure notebook
(attached UI_Buttons.png and R2_UI_Machine.png show the approved style and the current layout drawn by code). The
game places pegs, bumpers, cups and slot labels itself, so the cabinet must have an EMPTY play area. No text, no
numbers, no characters. ONE IMAGE PER REPLY in order P1 to P3, then wait for "next".
```

## P1 — Thân máy (`inbox/PK_Cabinet.png`)

```
1024 x 1536, transparent background around the machine. A cute tall pachinko cabinet seen straight from the front:
a thick warm wooden and cream frame with rounded top corners, doodled decorations (little stars, a pink ball emblem
at the top centre), crayon hatching and a hard offset shadow. Inside: one big flat cream play area with a faint dot
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
with white dots seen from above; 3 a small wooden half-round bump that sticks out of a wall; 4 a small golden cup
with a tiny chest emblem; 5 a small silver cup with a tiny chest emblem; 6 a thin wooden slot divider post with a
round top; 7 a cute white cloud with two dot eyes holding nothing (the ball launcher); 8 a pink ball with a white
band; 9 a blue ball; 10 a golden ball; 11 a small yellow star-burst flash; 12 a soft yellow rectangular glow.
Same ink and crayon style as the cabinet.
```
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

## Sau khi có ảnh

Claude ghép thân máy với khung 460 × 680 của code (đo mép trong mặt chơi), cắt bộ phận, lưu vào `Assets/03 Art/Pachinko/`.
