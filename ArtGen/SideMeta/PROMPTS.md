# SideMeta: Trang trại, Đền Huy Hiệu, Hang Tiềm Năng

Nền và vật phẩm cho ba scene side meta (spec `hero-farm`, `element-badges`, `potential-stones`). Như ảnh đảo:
- game đặt các chỗ tương tác (chỗ làm, bệ huy hiệu, tầng hang) lên ảnh nền bằng toạ độ;
- ảnh cần để trống đúng các chỗ đó;
- ảnh mới thì Claude chấm lại toạ độ.

## Ảnh đính kèm

| Ảnh | Dùng cho |
|---|---|
| `../Islands/inbox/world.png` | Style và góc nhìn của thế giới |
| `../guides/G_Island_2x3_SafeBand.png` | Dải giữa 9:16 giữ lại trên màn |
| `../guides/G_Sheet4x3.png` | Lưới 4 × 3 đánh số |

## Danh sách ảnh

| ID | File (lưu vào `inbox/`) | Khung | Nền | Vẽ gì |
|---|---|---|---|---|
| S1 | `farm.png` | 1024 × 1536 | đặc | Đảo trang trại có 8 chỗ làm |
| S2 | `badge_shrine.png` | 1024 × 1536 | đặc | Đền trên núi có 5 bệ huy hiệu |
| S3 | `potential_cave.png` | 1024 × 1536 | đặc | Hang pha lê 4 tầng |
| S4 | `badges.png` | 1536 × 1024 | trong suốt | 5 khung huy hiệu theo bậc, 5 biểu tượng hệ, 2 món phụ |
| S5 | `potential.png` | 1536 × 1024 | trong suốt | 5 viên đá theo độ hiếm, khung ô tiềm năng, đồ phụ |

## Tin nhắn mở đầu

```
You are painting side-feature scenes for a vertical mobile monster-battle game, same world and style as the
attached world.png (hand-drawn storybook cartoon, dark ink outlines, crayon hatching, watercolour, paper grain,
high three-quarter top-down view, light from the top-left). Scenes are 1024 x 1536 and get cropped to the central
9:16 band of the attached guide; keep the top 8 % and bottom 12 % calm because game UI covers them. The game places
interactive markers on the empty spots described in each prompt, so leave those spots clear and flat. No text, no
characters, no UI. ONE IMAGE PER REPLY in order S1 to S5, then wait for "next".
```

## S1 — Trang trại (`inbox/farm.png`)

> **Thay bằng gói mới (2026-11-10):** `build_farm.py` sinh `gui_gpt/farm/` (sơ đồ bố cục, nền cảnh, tấm đồ nghề, `HUONG_DAN.md`); ảnh lưu `farm/tai_ve/`, đưa vào Unity bằng `import_farm.py`. Prompt S1 dưới đây là bản cũ, không dùng.

```
A small cozy farm island in a turquoise sea. Eight clearly separated empty work spots arranged in a gentle zigzag
from bottom to top, each a flat patch of ground with a small fence or rim and nothing standing on it: two vegetable
fields (tilled brown soil rows), two duck ponds (round little ponds with reeds), two orchard plots (soft grass with a
small fruit tree at the back edge), one bread-oven yard (a round clay oven at the back edge), one tool-workshop yard
(a small open shed at the back edge). A red barn and a windmill in the upper area, a dirt path linking all spots.
```
**Sửa nhanh:** `Same farm; the eight spots more clearly separated and empty on top, path visible between them.`

## S2 — Đền Huy Hiệu (`inbox/badge_shrine.png`)

```
A mountain shrine on a floating rock above clouds: stone steps climbing from the bottom to a small golden pagoda at
the top. Halfway up, five empty stone altars arranged in a wide arc, each altar a round pedestal with a soft glow in
one element colour: silver (metal), green (wood), blue (water), red (fire), gold (earth). The tops of the altars
must be empty (the game puts the badges there). Prayer flags in five colours, small lanterns.
```
**Sửa nhanh:** `Same shrine; the five altars bigger, evenly spaced in an arc, tops empty.`

## S3 — Hang Tiềm Năng (`inbox/potential_cave.png`)

```
A crystal cave seen in a vertical cut-away: four levels stacked from bottom to top, each level a wide flat ledge
with an empty round door frame at its centre. The crystals grow bigger and glow stronger going up: bottom level pale
teal crystals (easy), second level green and blue crystals, third level purple crystals, top level fiery orange and
violet crystals with sparks (nightmare). A winding rope ladder links the levels. Leave the door frames empty.
```
**Sửa nhanh:** `Same cave; the four ledges clearly separated, doors empty, difficulty readable by crystal colour.`

## S4 — Huy hiệu (`inbox/badges.png`)

**Đính kèm thêm:** `../Icons/inbox/IC_ElementsStats.png`

```
12 items on a transparent background, 1536 x 1024, one per cell of the attached 4 x 3 grid:
1-5 five EMPTY round badge frames for the five tiers, each with a different border and ribbon: 1 bronze, 2 silver,
3 gold, 4 jade green, 5 diamond with sparkles (the centre of each is empty);
6-10 five element emblems that sit in the centre of a badge, matching the element icons in IC_ElementsStats.png:
6 metal ingot (silver), 7 leaf (green), 8 water drop (blue), 9 flame (red), 10 mountain (gold);
11 a greyed-out locked badge silhouette with a padlock; 12 a soft golden glow ring.
```
**Sửa nhanh:** `Same items; frames with empty centres so the emblem fits inside, tiers clearly different.`

## S5 — Đá tiềm năng (`inbox/potential.png`)

```
12 items on a transparent background, 1536 x 1024, one per cell of the attached 4 x 3 grid:
1-5 five faceted potential stones by rarity: 1 grey, 2 green, 3 blue, 4 purple with sparkles, 5 orange-gold
with strong glow;
6 an empty hexagonal potential slot frame (cream inside, ink border);
7 the same slot frame locked with a padlock;
8 a small toggle lock icon (open padlock);
9 a small pile of stones (resource icon);
10 two curved arrows forming a circle (re-roll);
11 a sparkle burst;
12 a crystal cluster (cave icon).
```
**Sửa nhanh:** `Same items; the five stones clearly different in colour and glow, simple shapes.`

## Sau khi có ảnh

Claude chấm toạ độ:
- 8 chỗ làm trên `farm`;
- 5 bệ trên `badge_shrine`;
- 4 cửa trên `potential_cave`.

Cắt S4, S5 thành sprite, lưu vào `Assets/03 Art/SideMeta/`.
