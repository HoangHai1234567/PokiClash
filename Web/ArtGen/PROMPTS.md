# PokiClash: ảnh đảo cho sảnh và 5 đảo hệ

> **Bản chính đã chuyển sang `ArtGen/Islands/PROMPTS.md` ở gốc dự án** (đủ hơn: khổ GPT 1024 × 1536, dải an toàn, prompt Z4–Z5, cùng các gói UI, icon, nền trận, máy bi, công trình, side meta). File này giữ lại cho bản web.

Bản web đọc ảnh nền scene ở `Web/public/art/`. Có file thì dùng file; chưa có thì game tự vẽ bản đồ nét tay.

| ID | File (lưu vào `Web/public/art/`) | Khung | Dùng cho |
|---|---|---|---|
| W1 | `world.png` | 9:16 (944 × 1680 trở lên) | Sảnh: đảo lớn chia 5 vùng hệ, làng máy bi ở giữa — **CHỐT STYLE** |
| Z1 | `zone_thuy.png` | 9:16 | Scene Đảo Thủy |
| Z2 | `zone_hoa.png` | 9:16 | Scene Đảo Hỏa |
| Z3 | `zone_kim.png` | 9:16 | Scene Đảo Kim |
| Z4 | `zone_moc.png` | 9:16 | Scene Đảo Mộc |
| Z5 | `zone_tho.png` | 9:16 | Scene Đảo Thổ |

Nhận cả `.png`, `.jpg`, `.webp` (cùng tên). Ảnh phải đúng tỉ lệ 9:16.

## Đã gen bằng Canva (2026-10-31)

Bốn ảnh đã gen bằng Canva AI. Mở từng link, bấm Tải xuống, rồi lưu đúng tên vào `Web/public/art/`:

| File | Link |
|---|---|
| `world.png` | https://www.canva.com/M/MAHZiTqHCPM |
| `zone_thuy.png` | https://www.canva.com/M/MAHZiSLeffw |
| `zone_hoa.png` | https://www.canva.com/M/MAHZiWb6OJY |
| `zone_kim.png` | https://www.canva.com/M/MAHZid4BpR8 |

**Toạ độ đã khớp:**
- 5 vùng trên `world.png` và 8 ải trên đường mòn của 3 đảo trên đều đã chấm theo đúng ảnh này: `ZONES[].world` và `ZONES[].nodes` trong `src/core/data/stages.ts`.
- Đảo Mộc và Thổ chưa gen (Canva báo hết lượt). Hai đảo này đang dùng bản đồ vẽ tay, toạ độ ải tạm.

**Có ảnh mới thì báo Claude** để chấm lại toạ độ ải theo đường mòn trong ảnh.

## Tin nhắn mở đầu (GPT)

```
You are painting map art for a vertical (9:16) mobile monster-battle game: a big world island split into five
elemental regions, and one larger zone island per element. Style for every image: hand-drawn storybook cartoon
illustration, bold dark ink outlines, crayon and watercolour textures, warm paper grain, cheerful saturated colours,
soft light from the top-left, high three-quarter top-down view, clean readable shapes. The game UI is drawn on top
later, so: no text, no labels, no UI, no characters, no logos. Work IN ORDER, ONE IMAGE PER REPLY, starting with W1,
then stop and wait for "next" or a correction.
```

## W1 — Đảo lớn (`world.png`) — CHỐT STYLE

**Đính kèm:** ảnh Canva `world.png` ở trên (nếu muốn giữ bố cục).

```
Vertical 9:16 world map. One big fantasy island floating in a calm turquoise sea, filling most of the frame.
The island is clearly divided into five elemental regions with distinct colours and landmarks:
TOP: red-orange volcano region with lava rivers and smoking peaks;
UPPER-RIGHT: silver-grey metal mountains with bronze bells, iron towers and gears;
UPPER-LEFT: lush green forest with giant round trees and glowing leaves;
LOWER-LEFT: blue water region with lagoons, waterfalls, a lighthouse and coral;
LOWER-RIGHT: golden-brown earth region with sandstone mesas, terraced cliffs and a small golden temple.
In the very centre: a small cozy village plaza with a big pachinko-machine tower where all regions meet.
Keep the five regions roughly at those positions; leave a little calm sea at the top and bottom edges.
```
**Sửa nhanh:** `Keep the same five-region layout; make each region's colour more distinct and the village plaza clearer.`

## Z1–Z5 — Đảo hệ (`zone_<hệ>.png`)

**Đính kèm:** `world.png` đã chốt (để cùng nét vẽ).

Mẫu chung, thay đoạn [REGION]:
```
Vertical 9:16 zone map in exactly the same style as the attached world map: one large [REGION] island seen from a
high three-quarter top-down angle, filling the frame. A clear winding trail starts at a beach or dock at the bottom
centre and climbs in gentle S-curves through the island to the boss lair at the top centre. Leave several small flat
clearings along the trail (the game puts 8 stage markers on it). Keep the top 8 % and bottom 10 % calm (sea or sky).
```

| ID | [REGION] |
|---|---|
| Z1 | `WATER element island in a bright turquoise sea: blue lagoons, turquoise pools, small waterfalls, coral reefs, a white lighthouse, shell-shaped cottages and wooden piers; at the top a giant swirling whirlpool shrine with a trident statue` |
| Z2 | `FIRE element island in a dark warm sea: black volcanic rocks, glowing lava rivers, red-roofed fire temples with lotus-shaped flames, smoking vents and ember trees; at the top a huge erupting volcano crater with a golden flame-wheel temple` |
| Z3 | `METAL element island in a cool blue-grey sea: silver-grey stone mountains, iron bridges, brass gears and pipes, hanging bronze bells, steel watchtowers; at the top a giant bell-tower fortress with a huge bronze bell and dark wing ornaments` |
| Z4 | `WOOD and nature element island in a turquoise sea: lush green forest, giant round trees, mushroom houses, hanging vines, glowing leaves and flower meadows; at the top an enormous ancient spirit tree with a shrine in its roots` |
| Z5 | `EARTH element island in a turquoise sea: golden sandstone mesas, terraced ochre cliffs, desert dunes, rope bridges and small stone pagodas; at the top a grand golden monastery with a giant seated stone guardian` |

**Sửa nhanh:** `Same style as the world map; make the trail wider and clearly visible from the bottom beach to the boss lair, with 8 flat clearings.`

## Tripo (nếu muốn đảo 3D)

Gen đảo 3D bằng Tripo từ ảnh trên, đặt camera nhìn chéo từ trên xuống (khoảng 55°) theo khung dọc 9:16, chụp ra PNG rồi lưu đúng tên như bảng trên. Đường mòn và các vùng phải giữ đúng vị trí, không thì cần chấm lại toạ độ.

**Không dùng ảnh đục từ game khác** (Clash of Critters, Aola) làm ảnh đính kèm, và không nhắc tên game trong prompt.
