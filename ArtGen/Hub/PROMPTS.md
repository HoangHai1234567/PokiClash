# Hub: công trình trên sảnh

Công trình đặt lên ảnh đảo lớn, quanh làng máy bi (spec `world-map`, mục "Chỗ đặt công trình side meta"). Mỗi công trình là một sprite rời trên nền trong suốt, để game làm được ba việc:
- nhún nhẹ khi chạm;
- hiện chấm báo;
- vẽ dạng phác chì (khi chưa mở) bằng shader: xám đi và chỉ còn nét.

## Ảnh đính kèm

| Ảnh | Dùng cho |
|---|---|
| `../Islands/inbox/world.png` | Style, góc nhìn, ánh sáng của đảo lớn |
| `../UIKit/inbox/UI_Buttons.png` | Nét mực đã chốt |
| `../guides/G_Sheet3x2.png` | Lưới 3 × 2 đánh số |

## Danh sách ảnh

| ID | File (lưu vào `inbox/`) | Khung | Nền | Vẽ gì |
|---|---|---|---|---|
| H1 | `HUB_Buildings.png` | 1536 × 1024 | trong suốt | 6 công trình |
| H2 | `HUB_Clouds.png` | 1536 × 1024 | trong suốt | 6 cụm mây trôi trên sảnh |

## Tin nhắn mở đầu

```
You are drawing buildings that will be placed on top of the attached world map (world.png), so match its view
angle (high three-quarter top-down), its light from the top-left and its hand-drawn storybook style with dark ink
outlines and crayon hatching. Each building sits on a small round patch of ground and is drawn alone on a fully
transparent background, one per cell of the attached numbered 3 x 2 grid, about 360 px, nothing crossing a cell.
No text, no signs with letters, no characters. ONE IMAGE PER REPLY, H1 then H2.
```

## H1 — Công trình (`inbox/HUB_Buildings.png`)

```
1536 x 1024, six buildings in grid order: 1 HERO HALL: a cozy martial-arts dojo hall with a curved roof and five
small coloured banners (silver, green, blue, red, gold); 2 CARD LIBRARY: a little round library tower with a few
glowing playing cards floating around its roof; 3 FARM: a red barn with a fence, a small windmill and a tiny
vegetable patch; 4 BADGE SHRINE: a small stone pagoda on steps with five glowing orbs around it in the five element
colours (silver, green, blue, red, gold); 5 POTENTIAL CAVE: a rocky cave entrance glowing with purple and teal
crystals; 6 PACHINKO TOWER: a tall cute pachinko cabinet building with round pegs on its face and a big pink ball
on the top.
```
**Sửa nhanh:** `Same six buildings; same angle as the world map, each on a small round ground patch, simpler details.`

## H2 — Mây trôi (`inbox/HUB_Clouds.png`)

```
1536 x 1024, six separate soft white clouds in the same hand-drawn style (dark ink outline, light grey crayon
shading underneath), different sizes and shapes, wider than tall, one per cell of the attached 3 x 2 grid, fully
transparent background. They will drift slowly over the map.
```
**Sửa nhanh:** `Same clouds; softer and lighter shading, outlines thinner.`

## Sau khi có ảnh

Claude cắt, đặt điểm neo ở chân công trình, lưu vào `Assets/03 Art/Hub/`:
- `bld_heroes`, `bld_cards`, `bld_farm`, `bld_badges`, `bld_cave`, `bld_machine`;
- `cloud_1..6`.

Vị trí đặt trên đảo lớn: ba chỗ trống quanh làng (xem prompt I1 của gói Islands).
