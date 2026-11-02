# Icons: icon vẽ tay (5 sheet × 16)

Thay bộ icon SVG vẽ bằng code của bản web (`Web/src/view/icons.ts`):
- tài nguyên;
- hệ, chỉ số, trạng thái;
- icon của 23 thẻ chung và 33 thẻ riêng;
- chỗ làm ở trang trại.

Mỗi sheet là lưới 4 × 4 (1024 × 1024), mỗi icon nằm gọn trong ô 256 × 256, cách mép ô khoảng 20 px.

## Ảnh đính kèm

| Ảnh | Dùng cho |
|---|---|
| `../StyleRefs/R1_UI_Cards.png` | Icon trên thẻ của bản web: nét mực dày, tô màu bút sáp |
| `../UIKit/inbox/UI_Buttons.png` | Style đã chốt |
| `../guides/G_Sheet4x4.png` | Lưới 4 × 4 đánh số |

## Danh sách ảnh

| ID | File (lưu vào `inbox/`) | Nội dung |
|---|---|---|
| IC1 | `IC_Resources.png` | Tài nguyên, rương, giao diện — **CHỐT STYLE icon** |
| IC2 | `IC_ElementsStats.png` | 5 hệ, chỉ số, sao, khoá, boss |
| IC3 | `IC_PoolCardsA.png` | 16 thẻ chung đầu |
| IC4 | `IC_PoolCardsB.png` | 7 thẻ chung cuối + 9 thẻ riêng |
| IC5 | `IC_InnateFarmStatus.png` | thẻ riêng còn lại, 5 chỗ làm trang trại, 4 trạng thái |

## Tin nhắn mở đầu

```
You are drawing game icons for a vertical mobile monster-battle game whose look is a hand-drawn kid's adventure
notebook (attached R1_UI_Cards.png and UI_Buttons.png show the approved style). Every sheet is 1024 x 1024 on a
FULLY TRANSPARENT background with 16 separate icons, one per cell of the attached numbered 4 x 4 grid, each icon
centred and about 200 px, nothing crossing a cell, no grid lines, no text, no numbers. Each icon: chunky simple
shape readable at 48 px, thick dark-brown ink outline (#2B2118), flat crayon colour with light hatching, a small
white highlight, no drop shadow (the game adds it). The attached PROMPTS.md lists 5 sheets (IC1–IC5); ONE SHEET PER
REPLY in order, then wait for "next".
```

## IC1 — Tài nguyên (`inbox/IC_Resources.png`) — CHỐT STYLE icon

```
16 icons in grid order: 1 a pink pachinko ball with a white band and a white button; 2 a purple star-shaped
experience bead; 3 a teal crystal shard; 4 a faceted gem stone with a soft inner glow (neutral cream colour, the
game tints it); 5 a closed wooden treasure chest; 6 the same wooden chest open with golden light; 7 a closed
silver chest; 8 the silver chest open; 9 a closed golden chest with a red gem lock; 10 the golden chest open with
sparkles; 11 a round alarm clock; 12 a rolled treasure map with a dashed red path; 13 two little hero silhouettes
side by side (team); 14 two playing cards fanned (blue and yellow, a star on the front one); 15 a gear; 16 a
yellow pencil.
```
**Sửa nhanh:** `Same 16 icons; simpler shapes, thicker outlines, each fully inside its cell.`

## IC2 — Hệ, chỉ số (`inbox/IC_ElementsStats.png`)

```
16 icons in grid order: 1 METAL element: a silver ingot / metal block (silver #B8C4CF); 2 WOOD element: a green
leaf (#6CBF4F); 3 WATER element: a blue water drop (#4A90D9); 4 FIRE element: a red-orange flame (#E8553F);
5 EARTH element: a golden mountain peak (#E2A93B); 6 a red heart (health); 7 a short sword (attack); 8 a blue
shield (defense); 9 a yellow lightning bolt (speed); 10 a blue mana drop with a sparkle; 11 an orange rage flame;
12 a filled golden star; 13 an empty star outline (cream); 14 a padlock; 15 a green check mark; 16 a cute white
skull with dark eyes (boss).
```
**Sửa nhanh:** `Same icons; make the five element icons the most distinct in shape and colour.`

## IC3 — Thẻ chung A (`inbox/IC_PoolCardsA.png`)

```
16 icons in grid order: 1 three red claw scratches; 2 a round wooden shield with a cross; 3 a bandage strip;
4 a blue drop with a small breath swirl; 5 a small growling flame; 6 a grey rock; 7 a pink round potion flask;
8 a steamed meat bun; 9 a skull with red eyes (risky sacrifice); 10 a light blue bubble shield; 11 a pink lotus
flower; 12 two fists side by side; 13 an angry red face with steam; 14 a white fang with a red drip; 15 a cracked
grey shield; 16 a burning torch.
```
**Sửa nhanh:** `Same icons; each one simpler and readable at 48 px.`

## IC4 — Thẻ chung B và thẻ riêng A (`inbox/IC_PoolCardsB.png`)

```
16 icons in grid order: 1 a hand mirror reflecting light; 2 a sharp eagle eye; 3 a paper talisman with a
lightning bolt; 4 a yin-yang disc (white and blue); 5 a purple ghost cloak; 6 a rising phoenix (gold and orange);
7 a golden crown with a red gem; 8 an iron-wrapped fist; 9 a golden dharma wheel; 10 a smiling sun; 11 an incense
burner with grey smoke curls; 12 a sprouting seed; 13 a big green leaf with thorns; 14 a wind swirl; 15 a pale
green feather; 16 a bronze temple bell.
```
**Sửa nhanh:** `Same icons; the bell and the wheel clearly different, all inside their cells.`

## IC5 — Thẻ riêng B, trang trại, trạng thái (`inbox/IC_InnateFarmStatus.png`)

```
16 icons in grid order: 1 a big war hammer; 2 a knight helmet with a red plume; 3 a dark purple bat-like wing;
4 a dark crescent moon with a small star; 5 a curling blue wave; 6 a golden trident; 7 a heart with a glowing halo
(revive); 8 a small vegetable field with rows of carrots and cabbages; 9 a tiny pond with a yellow duck;
10 a small fruit tree with red apples; 11 a round clay bread oven with a loaf; 12 a little workshop with a hammer
and saw; 13 a small orange flame with a drip (burn status); 14 three spinning yellow stars (stun status); 15 a
green plus sign with two leaves (regeneration status); 16 a dashed purple ghost outline (evade status).
```
**Sửa nhanh:** `Same icons; farm icons as tiny cute scenes but still simple, status icons small and bold.`

## Sau khi có ảnh

Claude cắt 80 icon theo lưới, xoá nền, đặt tên theo mã icon trong code. Ví dụ:
- `ball`, `exp`, `shard`, `stone`, `chest_wood`, `chest_wood_open`, …;
- `e_kim`, `e_moc`, `e_thuy`, `e_hoa`, `e_tho`, `heart`, `sword`, …;
- `claw`, `shield`, `bandage`, …, `trident`, `revive`;
- `farm_field`, `farm_pond`, `farm_orchard`, `farm_oven`, `farm_workshop`;
- `st_burn`, `st_stun`, `st_regen`, `st_evade`.

Lưu vào `Assets/03 Art/Icons` thành một Sprite Atlas.
