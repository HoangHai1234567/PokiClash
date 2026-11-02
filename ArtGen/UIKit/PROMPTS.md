# UIKit: bộ giao diện vẽ tay — CHỐT STYLE

Bộ khung, nút, thanh, thẻ, hộp thoại cho mọi scene (spec `ui-theme`). Unity cắt từng món ra sprite 9-slice: phần giữa phẳng để kéo giãn, viền và góc giữ nguyên.

## Ảnh đính kèm

| Ảnh | Dùng cho |
|---|---|
| `../StyleRefs/R1_UI_Cards.png` | Nét viền, gạch sáp, băng keo đã duyệt trên bản web |
| `../StyleRefs/R3_UI_Modal.png` | Hộp thoại, con dấu, nút |
| `../guides/G_Sheet3x2.png` | Lưới 3 × 2 đánh số |

## Danh sách ảnh

| ID | File (lưu vào `inbox/`) | Khung | Nền | Vẽ gì |
|---|---|---|---|---|
| U1 | `UI_Buttons.png` | 1536 × 1024 | trong suốt | 6 nút trơn: đỏ, xanh lá, xanh dương, vàng, tím, giấy — **CHỐT STYLE** |
| U2 | `UI_Panels.png` | 1536 × 1024 | trong suốt | 6 khung: tờ giấy hộp thoại, bảng tên, giấy kẻ dòng, dải thông tin, bong bóng thoại, ô thẻ nhỏ |
| U3 | `UI_CardFrames.png` | 1536 × 1024 | trong suốt | 6 khung thẻ: Thường, Khá, Hiếm, Sử thi, Huyền thoại, mặt sau |
| U4 | `UI_Bars.png` | 1536 × 1024 | trong suốt | Khung thanh, 4 phần đầy (máu, mana, nộ, EXP), chip tài nguyên |
| U5 | `UI_Discs.png` | 1536 × 1024 | trong suốt | 6 đĩa nút tròn: xanh lá, xanh dương, vàng to, hồng cam, tím, vòng huy hiệu cấp |
| U6 | `UI_Stamps.png` | 1536 × 1024 | trong suốt | Khung con dấu đỏ, băng rôn đỏ, băng rôn giấy, khiên VS, 4 mẩu băng keo, mảnh mây chuyển scene |
| U7 | `UI_Logo.png` | 1536 × 1024 | trong suốt | Logo chữ "PokiClash" |
| U8 | `UI_Paper.png` | 1024 × 1024 | đặc | Nền giấy kem có lưới kẻ ô xanh nhạt, lặp liền 4 cạnh |

**Thứ tự:** U1 → U2 → U3 → U4 → U5 → U6 → U7 → U8.

## Tin nhắn mở đầu

```
You are drawing the user-interface kit of a vertical mobile monster-battle game whose whole look is a hand-drawn
kid's adventure notebook (attached screenshots R1_UI_Cards.png and R3_UI_Modal.png show the approved look: cream
paper, wobbly dark-brown ink outlines, crayon hatching, hard offset shadows, tape strips). The attached PROMPTS.md
lists 8 images (U1–U8), each with its own English prompt. Work IN ORDER, ONE IMAGE PER REPLY, starting with U1,
then stop and wait for "next" or a correction. Never write any text or letters on UI pieces (the game writes
Vietnamese text itself), except the logo in U7.
STYLE: hand-drawn storybook cartoon for a vertical mobile game. Bold dark-brown ink outlines (#2B2118), slightly
wobbly like a real pen, colored-pencil and crayon hatching for shading, flat warm colours with light watercolour
washes, subtle cream paper grain, soft light from the top-left. No photorealism, no glossy 3D, no heavy gradients.
```

## U1 — Nút trơn (`inbox/UI_Buttons.png`) — CHỐT STYLE

**Đính kèm:** `G_Sheet3x2.png`

```
Six blank game buttons on a fully transparent background, 1536 x 1024, one per cell of the attached numbered
3 x 2 grid, nothing crossing a cell: 1 red #E8553F, 2 green #6CBF4F, 3 blue #4A90D9, 4 yellow #F7C948,
5 purple #9A6AD6, 6 cream paper #FBF4E2. Each is a wide rounded rectangle about 400 x 150 px with slightly
uneven hand-drawn corners, a thick 6 px dark-brown ink outline, diagonal crayon hatching lighter stripes across
the fill, a darker band on the bottom 35 % (pressed-edge shading), and a HARD offset shadow (solid #2B2118,
8 px right and 10 px down, no blur). The middle part must be plain so the button can stretch horizontally.
No text, no icons.
```
**Sửa nhanh:** `Keep the same six buttons; outlines thicker and more wobbly, middle area flatter so it can stretch, no text.`

## U2 — Khung (`inbox/UI_Panels.png`)

**Đính kèm:** `G_Sheet3x2.png`, `UI_Buttons.png` (U1 đã duyệt)

```
Six blank UI frames on a transparent background, 1536 x 1024, one per cell of the attached 3 x 2 grid, same ink
and crayon style as UI_Buttons.png:
1 a large cream paper sheet for dialogs (about 440 x 300) with a strip of translucent yellow tape at the top centre,
  hand-drawn uneven border, hard offset shadow;
2 a small rounded name plaque (about 400 x 110), cream fill, ink border;
3 a lined notebook paper panel (about 440 x 300) with faint blue horizontal ruling and a red margin line on the
  left, ink border on the top edge only;
4 a thin information strip (about 460 x 90), cream, rounded;
5 a white speech bubble (about 380 x 200) with a small tail at the bottom-left;
6 a small square slot tile (about 200 x 240) with a dashed ink border (an empty card slot).
No text.
```
**Sửa nhanh:** `Same six frames; borders cleaner at the edges so they can be 9-sliced, keep the hand-drawn wobble.`

## U3 — Khung thẻ theo độ hiếm (`inbox/UI_CardFrames.png`)

**Đính kèm:** `G_Sheet3x2.png`, `UI_Buttons.png`, `R1_UI_Cards.png`

```
Six blank playing-card frames on a transparent background, 1536 x 1024, one per cell of the attached 3 x 2 grid,
each a portrait card about 300 x 440 like the cards in R1_UI_Cards.png: cream paper body with light crayon
hatching, thick wobbly ink border, hard offset shadow, a coloured top band (about 20 % of the height), a dashed
circle in the upper middle where an icon will go, and a strip of tape on the top edge. Top band colours:
1 common grey #B9B1A3, 2 uncommon green #6CBF4F, 3 rare blue #4A90D9, 4 epic purple #9A6AD6 with small sparkles,
5 legendary orange #F39A2D with a golden inner border and sparkles, 6 the card BACK: red #E8553F with diagonal
cream stripes and a simple doodled dice in the centre. No text.
```
**Sửa nhanh:** `Same six cards; make the rarity colours clearly different, keep the body plain for text.`

## U4 — Thanh và chip (`inbox/UI_Bars.png`)

**Đính kèm:** `G_Sheet4x3.png`, `UI_Buttons.png`

```
Twelve UI pieces on a transparent background, 1536 x 1024, one per cell of the attached numbered 4 x 3 grid:
1 an empty progress-bar frame (long rounded rectangle about 340 x 44, cream inside, ink border);
2 a green health fill strip with diagonal lighter crayon hatching; 3 a blue mana fill strip; 4 an orange rage fill
strip with a soft glow; 5 a purple experience fill strip; 6 a pale blue striped shield overlay strip;
7 a small resource chip (rounded pill about 220 x 70, cream, ink border, hard shadow) with an empty round spot on
the left for an icon; 8 a small element tag pill (about 160 x 50) blank; 9 a tiny red notification dot with ink
border; 10 a round level badge: cream disc with a thick ink ring and an empty groove for an XP arc;
11 a thin yellow highlight ring (for a selected item); 12 a dashed ink circle (empty icon slot).
No text.
```
**Sửa nhanh:** `Same twelve pieces; fill strips flat at both ends so they can be cut to any length.`

## U5 — Đĩa nút tròn (`inbox/UI_Discs.png`)

**Đính kèm:** `G_Sheet3x2.png`, `UI_Buttons.png`

```
Six round button discs on a transparent background, 1536 x 1024, one per cell of the attached 3 x 2 grid, each a
slightly uneven hand-drawn circle about 300 px with thick ink outline, crayon hatching and hard offset shadow, empty
centre for an icon: 1 light green #C9ECB0, 2 light blue #BCD8F5, 3 big yellow #FFE08A (the largest, about 360 px),
4 coral #FFB3A3, 5 lavender #E3D2FF, 6 a small cream round button (about 200 px) for back/close/pause.
No text, no icons.
```
**Sửa nhanh:** `Same discs; centres emptier and flatter, outlines more hand-drawn.`

## U6 — Con dấu, băng rôn, băng keo, mây (`inbox/UI_Stamps.png`)

**Đính kèm:** `G_Sheet3x2.png`, `R3_UI_Modal.png`

```
Six pieces on a transparent background, 1536 x 1024, one per cell of the attached 3 x 2 grid:
1 an empty rubber-stamp frame, a rounded rectangle about 420 x 160 drawn in red stamp ink with a rough grungy
  texture and tilted -9 degrees (text will be added by the game);
2 a long red ribbon banner with folded ends, crayon hatching, ink outline, empty middle;
3 a cream paper ribbon banner, same shape;
4 a shield-shaped "versus" emblem: yellow star burst behind a dark shield, no letters;
5 four tape strips in a row: translucent yellow, blue, pink, green, each with torn ends;
6 a big puffy white cloud mass drawn with ink outline, filling the cell edge to edge on the left side and puffy on
  the right edge (used to wipe the screen between scenes).
No text.
```
**Sửa nhanh:** `Same six pieces; the stamp frame emptier and more grungy, the cloud flatter on its left edge.`

## U7 — Logo (`inbox/UI_Logo.png`)

**Đính kèm:** `UI_Buttons.png`, `UI_Stamps.png`

```
Game logo on a transparent background, 1536 x 1024: the word "PokiClash" in big chunky rounded hand-lettered
letters, white fill with a thick dark-brown ink outline and a hard offset shadow, slightly bouncy baseline; behind
it a small doodled pachinko ball (pink with a white band) and two crossed paper cards; a few crayon sparkles.
Exactly the letters P-o-k-i-C-l-a-s-h, nothing else written.
```
**Sửa nhanh:** `Same logo; letters chunkier and easier to read at small size, check the spelling PokiClash.`

## U8 — Giấy nền lặp (`inbox/UI_Paper.png`)

```
A seamless tileable texture, 1024 x 1024: cream notebook paper #FBF4E2 with faint light-blue square grid lines
every 48 px, subtle paper fibres and grain, very low contrast. Must tile on all four edges. No marks, no text.
```
**Sửa nhanh:** `Lower contrast, lines thinner and lighter, perfectly tileable.`

## Sau khi có ảnh

Claude cắt từng ô theo lưới, xoá nền, đặt viền 9-slice. Lưu vào `Assets/03 Art/UIKit/`:
- `btn_red`, `btn_green`, …;
- `panel_sheet`, `panel_plaque`, …;
- `card_common`, …, `card_back`;
- `bar_frame`, `bar_hp`, …;
- `disc_green`, …;
- `stamp_frame`, `ribbon_red`, `tape_yellow`, `cloud_wipe`;
- `logo`, `paper_tile`.
