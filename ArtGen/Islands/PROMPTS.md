# Islands: đảo lớn (sảnh) và 5 đảo hệ

Nền của scene Hub và 5 scene đảo hệ (spec `world-map`, `zone-stages`).
- Game neo bảng tên vùng lên ảnh đảo lớn, và 8 ô ải lên đường mòn của ảnh đảo hệ, bằng toạ độ trong dữ liệu.
- Ảnh mới thì Claude chấm lại toạ độ.
- Scene đảo hệ phóng ảnh 1,27 lần và cuộn dọc, nên ảnh nên nhiều chi tiết.

## Đã có (Canva AI, 2026-10-31)

Cùng style, toạ độ đã chấm. Mở link → Tải xuống → lưu vào `inbox/`:

| File | Link |
|---|---|
| `world.png` | https://www.canva.com/M/MAHZiTqHCPM |
| `zone_thuy.png` | https://www.canva.com/M/MAHZiSLeffw |
| `zone_hoa.png` | https://www.canva.com/M/MAHZiWb6OJY |
| `zone_kim.png` | https://www.canva.com/M/MAHZid4BpR8 |

Còn thiếu `zone_moc.png` và `zone_tho.png` (Canva hết lượt): gen theo Z4, Z5 dưới đây. Gửi kèm `world.png` của Canva để cùng style. Muốn đồng bộ độ phân giải thì gen lại cả bộ.

## Ảnh đính kèm

| Ảnh | Dùng cho |
|---|---|
| `inbox/world.png` (Canva) | Style và bố cục 5 vùng đã chọn |
| `../StyleRefs/R4_Hub_Sketch.png` | Vị trí 5 vùng và làng (bản vẽ bằng code) |
| `../guides/G_Island_2x3_SafeBand.png` | Dải giữa 9:16 giữ lại trên màn; vùng an toàn trên dưới |

## Danh sách ảnh

| ID | File (lưu vào `inbox/`) | Khung | Nền | Vẽ gì |
|---|---|---|---|---|
| I1 | `world.png` | 1024 × 1536 | đặc | Đảo lớn 5 vùng, làng máy bi giữa — **CHỐT STYLE** (đã có bản Canva) |
| Z1 | `zone_thuy.png` | 1024 × 1536 | đặc | Đảo Thủy (đã có bản Canva) |
| Z2 | `zone_hoa.png` | 1024 × 1536 | đặc | Đảo Hỏa (đã có bản Canva) |
| Z3 | `zone_kim.png` | 1024 × 1536 | đặc | Đảo Kim (đã có bản Canva) |
| Z4 | `zone_moc.png` | 1024 × 1536 | đặc | Đảo Mộc — **cần gen** |
| Z5 | `zone_tho.png` | 1024 × 1536 | đặc | Đảo Thổ — **cần gen** |

**Thứ tự:** Z4 → Z5 (nếu giữ bản Canva); hoặc I1 → Z1…Z5 nếu gen lại cả bộ.

## Tin nhắn mở đầu

```
You are painting map art for a vertical mobile monster-battle game: one big world island split into five
elemental regions, and one larger zone island per element. Match the attached world.png exactly in style:
hand-drawn storybook cartoon, bold dark ink outlines, crayon and watercolour textures, warm paper grain, cheerful
saturated colours, soft light from the top-left, high three-quarter top-down view. The image will be cropped to the
central 9:16 band shown in the attached guide, so keep everything important inside that band, and keep the top 8 %
and bottom 10 % calm (sea or sky) because game UI covers them. No text, no labels, no UI, no characters, no logos.
The attached PROMPTS.md lists the images, each with its own English prompt. Work IN ORDER, ONE IMAGE PER REPLY,
then stop and wait for "next" or a correction.
```

## I1 — Đảo lớn (`inbox/world.png`) — CHỐT STYLE

```
Vertical 1024 x 1536 world map. One big fantasy island floating in a calm turquoise sea, filling the safe band.
Five clearly separated elemental regions with distinct colours and landmarks:
TOP CENTRE: red-orange volcano region with lava rivers and smoking peaks;
UPPER-RIGHT: silver-grey metal mountains with bronze bells, iron towers and gears;
UPPER-LEFT: lush green forest with giant round trees and glowing leaves;
LOWER-LEFT: blue water region with lagoons, waterfalls, a lighthouse and coral;
LOWER-RIGHT: golden-brown earth region with sandstone mesas, terraced cliffs and a small golden temple.
In the very centre: a small cozy village plaza with a tall pachinko-machine tower (a tall cabinet with round pegs
and a pink ball on top) and a few cottages; around the village edge leave three small empty plots for future
buildings (left, right and bottom of the plaza).
```
**Sửa nhanh:** `Same layout; make the five regions' colours more distinct, the village plaza clearer, and leave the three empty plots around it.`

## Z1–Z5 — Đảo hệ

Mẫu chung (thay [REGION]):
```
Vertical 1024 x 1536 zone map, exactly the same style as the attached world.png: one large [REGION] island seen
from a high three-quarter top-down angle, filling the safe band. A clear, wide winding trail starts at a beach or
dock at the bottom centre (about 88 % down) and climbs in gentle S-curves to the boss lair at the top centre
(about 13 % down). Along the trail leave 8 small flat round clearings, evenly spaced, where the game will place
stage markers; the 4th clearing (middle) is a bit larger with a small mini-boss landmark, the 8th is the boss lair.
```

| ID | [REGION] |
|---|---|
| Z1 | `WATER element island in a bright turquoise sea: blue lagoons, turquoise pools, small waterfalls, coral reefs, a white lighthouse near the middle, shell-shaped cottages and wooden piers; boss lair: a giant swirling whirlpool shrine with a golden trident statue` |
| Z2 | `FIRE element island in a dark warm sea: black volcanic rocks, glowing orange lava rivers, red-roofed fire temples with lotus-shaped flames, smoking vents and ember trees; boss lair: a huge erupting volcano crater with a golden flame-wheel temple` |
| Z3 | `METAL element island in a cool blue-grey sea: silver-grey stone mountains, iron bridges, brass gears and pipes, hanging bronze bells, steel watchtowers; boss lair: a giant bell-tower fortress with a huge bronze bell and dark wing ornaments` |
| Z4 | `WOOD and nature element island in a turquoise sea: lush green forest, giant round trees, mushroom houses, hanging vines, glowing leaves and flower meadows, a little wind spirit shrine at the middle clearing; boss lair: an enormous ancient spirit tree with a shrine in its roots` |
| Z5 | `EARTH element island in a turquoise sea: golden sandstone mesas, terraced ochre cliffs, desert dunes, rope bridges and small stone pagodas, a stone martial-arts courtyard at the middle clearing; boss lair: a grand golden monastery with a giant seated stone guardian` |

**Sửa nhanh:** `Same island; make the trail wider and clearly visible from the bottom beach to the boss lair, with 8 flat clearings along it.`

## Sau khi có ảnh

Claude cắt theo dải 9:16 (hoặc giữ 2:3 cho đảo hệ, vì scene cuộn dọc), rồi chấm:
- toạ độ 5 vùng trên `world`;
- 8 điểm ải trên đường mòn của từng đảo.

Cập nhật `ZONES[].world` và `ZONES[].nodes` ở cả `Web/src/core/data/stages.ts` và dữ liệu Unity. Ảnh vào `Assets/03 Art/Islands/`.
