# Giọt Sương dạng 1: prompt gửi GPT

Mỗi lần gen **một ảnh**: đính kèm đúng các ảnh ghi ở bước đó (theo thứ tự), dán khối prompt của bước đó. Đường dẫn ảnh tính từ `D:\PokiClash\ArtGen\Heroes\`.

**Gen bước 0 (concept) trước**, lưu ảnh rồi nhắn Claude "duyệt concept giot_suong_1". Bước 1–8 chỉ gen sau khi concept đã duyệt; ảnh 2 của mỗi bước là concept đã duyệt.

## Bước 0. Concept

Đính kèm: `refs/thuy/giot_suong_1/Silhouette.png`, rồi `refs/thuy/giot_suong_1/RegionMap.png`.

Lưu vào: `inbox/giot_suong_1/Concept.png` (gen lại thì `Concept_v2.png`, `_v3`…).

```
Character concept for a 2D cut-out animation game. Draw ONE original creature, a baby water pet for a cute creature-collecting battle game, in the same front three-quarter view and pose as image 1, on a plain light grey background. It is the first stage of a Water evolution line. An original design that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one head with two growths on its sides and one crest on top, one small body, two arms, two legs, one tail; no wings, no extra limbs;
- every joint where it is: the neck hidden under the bottom of the head; the shoulders at the top of the body; the hips at the bottom of the body; the tail joining the back of the body at the lower left; the side growths starting at the sides of the head; the crest standing on top of the head;
- every limb pointing the same way: the arms hang down (viewer-left arm down-left, viewer-right arm down-right) with the hands at their LOWER ends; the legs go straight down with the feet at the BOTTOM, toes pointing down and slightly to the left; the tail tip curls UP at the upper left; the side growths point up and out;
- the body, arms and legs about the size and shape of regions 4, 6, 7, 9 and 10; the whole figure about the same height.

CHANGE (the new outline, region by region):
1 the two side growths: two fans of feathery gill fronds like a baby axolotl's gills, THREE frond branches on each side spreading up and out, longer than the shapes in image 1, coral pink with deeper pink feathering.
2 head: a wide baby-axolotl head, clearly wider than tall, broader than region 2 at both sides, with a rounded top (no point), smooth sky-blue skin, a paler cream lower face, big round dark-blue eyes with white highlights on the lower half of the head, soft pink cheeks, a wide happy smile. Where the crest sits, a ring of small green lotus sepals.
3 crest: a closed pink-and-white lotus bud about the size of region 3, its base on top of the head, its pointed tip curling up and to the left.
4 body: a soft round sky-blue belly with a cream belly patch, narrow at the neck.
5 on the chest: a small round green lotus-leaf bib tied with a red string.
6 viewer-left arm: TOP end = shoulder, a small four-fingered hand at the BOTTOM end, a thin red string bracelet at the wrist.
7 viewer-right arm: TOP end = shoulder, a small hand at the BOTTOM end, a thin red string bracelet at the wrist.
8 tail: a big axolotl tail, larger than region 8, with a tall soft fin along its top and bottom edges; its wide end joins the body on the right and its tip curls UP at the upper left; the fin edges and tip coral pink.
9 and 10 legs: two short stubby legs, hip at the TOP, small webbed feet at the BOTTOM, toes pointing down and slightly to the left.

STYLE: clean 2D cartoon game art for a cut-out rig. Crisp outlines of even weight; each outline is a darker shade of the colour it surrounds, never pure black. Flat colours with one level of cel shading and small highlights. No painterly texture, no pencil or crayon hatching, no large gradients, no motion blur. Every part clearly separated by its outline.

AVOID: a water-drop or teardrop head, a head that tapers to a point, horn-shaped fins, a droplet crest, a sea shell, rainbow-striped fins or tail, human features, clothes, weapons, extra limbs, text, labels, numbers, the region colours, frames, background scenery, a second view.
```

## Bước 1. N01 hai chùm mang (đổi dáng)

Đính kèm: `refs/thuy/giot_suong_1/orig/N01.png`, rồi `inbox/giot_suong_1/Concept.png` (bản đã duyệt).

Lưu vào: `inbox/giot_suong_1/orig_parts/N01.png`.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two fin-shaped ears on the sides of a head (the head is not shown). The viewer-left one points up and to the left, its base (where it joins the head) at its lower RIGHT end. The viewer-right one points up, its base at its LOWER left end. Redraw THESE two pieces as the two gill fans of image 2 (the approved concept): each one grows from its base end and splits into three feathery coral-pink frond branches with deeper pink feathering, spreading up and out; they may be longer and wider than the old fins.
Do NOT draw: a head, rainbow stripes, a smooth horn shape.

FRAMING: the same square canvas; each piece keeps its place, angle and direction from image 1, and its base end stays exactly where the old base is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be a different shape and bigger, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

## Bước 2. N02 đầu và mặt (đổi dáng)

Đính kèm: `refs/thuy/giot_suong_1/orig/N02.png`, rồi `inbox/giot_suong_1/Concept.png` (bản đã duyệt).

Lưu vào: `inbox/giot_suong_1/orig_parts/N02.png`.

```
Image 1 is one group of a 2D cut-out animation puppet (the old design): a big round water-drop head with a face (two eyes, two cheeks, a mouth) and a lime crescent band near the top. Redraw THIS group as the head of image 2 (the approved concept): a wide baby-axolotl head, smooth sky-blue skin and a paler cream lower face, wider than the old head at both sides and with a rounded top instead of the point; the big round dark-blue eyes with white highlights, the pink cheeks and the wide smile exactly where the old eyes, cheeks and mouth are; a ring of small green lotus sepals where the lime crescent is.
Keep the bottom edge of the head at the same height as the old one (the neck goes under it) and the top at about the same height (a crest stands on it).
Do NOT draw: the gill fronds, the lotus bud, a neck, a body, a water-drop shine.

FRAMING: the same square canvas; the head keeps its place, angle and direction from image 1, and the eyes, cheeks and mouth stay exactly where they are, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be wider, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

## Bước 3. N03 nụ sen (đổi dáng)

Đính kèm: `refs/thuy/giot_suong_1/orig/N03.png`, rồi `inbox/giot_suong_1/Concept.png` (bản đã duyệt).

Lưu vào: `inbox/giot_suong_1/orig_parts/N03.png`.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): a water-drop crest; its lower edge sits in the head and its pointed tip curls up to the upper left. Redraw THIS piece as the closed pink-and-white lotus bud of image 2 (the approved concept): overlapping petals, the base along the old lower edge, the pointed tip curling up and to the left like the old tip, about the same size.
Do NOT draw: a water drop, a head, leaves below the bud.

FRAMING: the same square canvas; the piece keeps its place, angle and direction from image 1, and its base stays exactly where the old lower edge is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1, and stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

## Bước 4. N04 thân và yếm (giữ viền)

Đính kèm: `refs/thuy/giot_suong_1/orig/N04.png`, rồi `inbox/giot_suong_1/Concept.png` (bản đã duyệt).

Lưu vào: `inbox/giot_suong_1/orig_parts/N04.png`.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a small body shaped like a drop (narrow neck end at the TOP, round belly at the bottom) and a sea shell on the chest. Redraw THESE pieces as the body of image 2 (the approved concept): the body becomes the soft sky-blue belly with a cream belly patch, same outline; the shell becomes the small round green lotus-leaf bib tied with a red string, same place and size.
Do NOT draw: arms, legs, a head, a sea shell.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

## Bước 5. N05 tay trái (giữ viền)

Đính kèm: `refs/thuy/giot_suong_1/orig/N05.png`, rồi `inbox/giot_suong_1/Concept.png` (bản đã duyệt).

Lưu vào: `inbox/giot_suong_1/orig_parts/N05.png`.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a thin arm. Its TOP end (upper right) is the shoulder; it runs down to the left; the round hand is at the BOTTOM end, with a lime band at the wrist. Redraw THESE pieces as the viewer-left arm of image 2 (the approved concept): smooth sky-blue skin, a small four-fingered hand at the BOTTOM end with the fingers curled in, a thin red string bracelet where the lime band is.
Do NOT put the hand at the top. Do NOT draw: a sleeve, claws, a body.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

## Bước 6. N06 tay phải (giữ viền)

Đính kèm: `refs/thuy/giot_suong_1/orig/N06.png`, rồi `inbox/giot_suong_1/Concept.png` (bản đã duyệt).

Lưu vào: `inbox/giot_suong_1/orig_parts/N06.png`.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a thin arm. Its TOP end (upper left) is the shoulder; it runs down and curves to the right; the round hand is at the BOTTOM end, with a lime band at the wrist. Redraw THESE pieces as the viewer-right arm of image 2 (the approved concept): smooth sky-blue skin, a small four-fingered hand at the BOTTOM end with the fingers curled in, a thin red string bracelet where the lime band is.
Do NOT put the hand at the top. Do NOT draw: a sleeve, claws, a body.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

## Bước 7. N07 đuôi (đổi dáng)

Đính kèm: `refs/thuy/giot_suong_1/orig/N07.png`, rồi `inbox/giot_suong_1/Concept.png` (bản đã duyệt).

Lưu vào: `inbox/giot_suong_1/orig_parts/N07.png`.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): a tail. The wide straight edge on the RIGHT is where it joins the body (hidden behind it); it sweeps to the left and its tip curls UP at the upper left, with orange and green stripes at the tip. Redraw THIS piece as the big axolotl tail of image 2 (the approved concept): sky-blue, a tall soft fin along its top and bottom edges, the fin edges and the tip coral pink; bigger than the old tail.
The joint end stays on the RIGHT, exactly where the old straight edge is; the tip still curls up at the upper left.
Do NOT draw: rainbow stripes, a body, legs.

FRAMING: the same square canvas; the piece keeps its place, angle and direction from image 1, and its joint edge stays exactly where it is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be bigger, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

## Bước 8. N08 hai chân (giữ viền)

Đính kèm: `refs/thuy/giot_suong_1/orig/N08.png`, rồi `inbox/giot_suong_1/Concept.png` (bản đã duyệt).

Lưu vào: `inbox/giot_suong_1/orig_parts/N08.png`.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two short legs. Each one has its hip at the TOP (the wide end) and its foot at the BOTTOM (the narrow pointed end, pointing down and slightly to the left). Redraw THESE two pieces as the two stubby legs of image 2 (the approved concept): sky-blue skin, small webbed feet at the BOTTOM ends with three tiny toes pointing down and slightly to the left.
Do NOT put the feet at the top. Do NOT draw: a body, a tail, shoes.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```
