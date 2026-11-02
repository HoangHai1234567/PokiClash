# Giọt Sương dạng 1 (aola #7 滴滴)

Tướng Thủy đầu tiên, dạng 1 trong 3. Tổng quan cả dòng: [giot_suong.md](giot_suong.md). Quy trình chung: [../QUY_TRINH.md](../QUY_TRINH.md).

**Thiết kế do Claude đề xuất, duyệt ở bước concept:** một bé **kỳ giông** (axolotl) nước, thay cho con giọt nước. Dáng ngoài được đổi cho khác bản gốc (người dùng dặn 2026-11-01); tay, chân, khớp giữ đúng rig.

| Bộ phận gốc | Thành | Dáng |
|---|---|---|
| đầu giọt nước, đỉnh nhọn | đầu kỳ giông bè ngang, đỉnh tròn, miệng rộng | **rộng hơn**, hết đỉnh nhọn |
| hai vây tai hình sừng | hai chùm mang lông vũ hồng san hô, mỗi chùm 3 nhánh | **đổi dáng**: xoè 3 nhánh, có thể dài hơn |
| chóp giọt nước | nụ sen hồng trắng | **đổi dáng**, cỡ như cũ |
| vòng lá chanh trên đầu | vòng đài sen xanh | |
| vỏ sò ở ngực | yếm lá sen buộc dây đỏ | |
| đuôi sọc cầu vồng | đuôi kỳ giông có vây cao | **to hơn** |
| thân, hai tay, hai chân | da xanh, bụng kem, bàn tay bốn ngón, bàn chân có màng | **giữ dáng** |

Màu chính xanh da trời, bụng kem, điểm hồng san hô và xanh lá sen.

Đường dẫn ảnh tính từ `ArtGen/Heroes/`. **Chỉ dán khối prompt cho GPT, không đính kèm file này.** Bản gửi GPT (chỉ có prompt, ảnh đính kèm, chỗ lưu; không tên game): [giot_suong_1_gpt.md](giot_suong_1_gpt.md), trích từ file này; sửa prompt ở đây thì tạo lại bản đó.

## Rig mặt trước #7

Dữ liệu rig: `<aola>/reskin/pet7_parts/`. Bộ ghép: `<aola>/reskin/thuy_7/` (`regions.json`, `groups.json`).

- **Đứng:** 24 khung, 20 mảnh. Gần như mỗi mảnh cử động riêng; hai vây tai (3, 4) đứng yên.
- **Trúng đòn:** 18 khung, 12 hình mới. Mặt hoảng và vây tai đổi hình (58, 64, 66, 68, 140–150); vây tai gốc vắng hẳn. Lúc ghép phải làm biến thể.
- **Đánh thường:** 50 khung, 6 hình mới; thân dáng khác ở khung 25–39 (138, 140).
- **Chiêu:** 38 khung, 13 hình mới; có 4 quầng mờ (155–161).

Ảnh rig có đánh số: `refs/thuy/giot_suong_1/Rig_Numbered.png`.

### Giải phẫu từng mảnh

Trái, phải theo **người xem**. Con đứng thẳng, mặt nhìn ra trước, hơi chéo.

| Mảnh | Là gì | Hai đầu, hướng |
|---|---|---|
| 1 | bóng dưới chân | giữ |
| 2 | vệt nhỏ cạnh tay trái | bỏ |
| 3 | vây tai phải | gốc ở **đầu dưới trái** (dính đầu), chóp chĩa **lên** |
| 4 | vây tai trái | gốc ở **đầu phải** (dính đầu), chóp chĩa **lên trái** |
| 14 | đầu tròn to, có vòng lá chanh hình lưỡi liềm gần đỉnh | |
| 18, 19 | mắt phải, mắt trái | nhìn ra trước |
| 15, 16 | má hồng phải, trái | |
| 17 | miệng | |
| 20 | chóp giọt nước trên đỉnh đầu | đáy cắm vào đầu; chóp **cong lên, sang trái** |
| 10 | thân hình giọt nước | đầu nhọn ở **trên** (cổ), bụng tròn ở **dưới** |
| 11 | vỏ sò trên ngực | |
| 12 | bắp tay trái | đầu **trên** là vai, đi xuống trái |
| 13 | cẳng tay và bàn tay trái | bàn tay tròn ở **đầu dưới**, vòng lá chanh ở cổ tay |
| 6 | bắp tay phải | đầu **trên** là vai, đi xuống phải |
| 5 | cẳng tay và bàn tay phải | bàn tay ở **đầu dưới**, vòng lá chanh ở cổ tay |
| 7 | đuôi, sau thân, phía dưới trái | mép thẳng rộng ở **phải** là chỗ nối thân (khuất sau thân); chóp **cong lên** ở trên trái |
| 8 | chân trái | hông ở **trên**, bàn chân nhọn ở **dưới**, chĩa xuống hơi sang trái |
| 9 | chân phải | hông ở **trên**, bàn chân ở **dưới**, chĩa xuống hơi sang trái |

### Chỗ nào được đổi dáng

Mỗi mảnh vẫn cử động quanh khớp cũ, nên **đầu khớp phải ở nguyên chỗ**; phần còn lại của mảnh đổi được.

| Mảnh | Đổi dáng | Phải giữ |
|---|---|---|
| đầu (14) | rộng ra hai bên, đỉnh tròn | mép dưới vẫn phủ cổ; đỉnh vẫn đỡ nụ sen; mắt, má, miệng ở chỗ cũ (mảnh riêng) |
| mang (3, 4) | dáng chùm 3 nhánh, dài hơn được | gốc ở chỗ cũ, khuất sau đầu |
| nụ sen (20) | dáng nụ, cỡ như cũ | đáy ở chỗ cũ trên đỉnh đầu |
| đuôi (7) | to hơn, có vây cao | mép nối thân ở bên phải, khuất sau thân |
| thân, tay, chân | không | giữ viền cũ: thân phải phủ vai, hông; tay chân to quá sẽ lệch khớp |

Ảnh mẫu N02 (đầu) và N07 (đuôi) có khung rộng hơn mảnh (`frame` trong `groups.json`) để có chỗ vẽ to ra.

### Ảnh và chỗ lưu

| # | Gen gì | Đính kèm (theo thứ tự) | Lưu ảnh GPT vào |
|---|---|---|---|
| 0 | Concept | `refs/thuy/giot_suong_1/Silhouette.png`, `refs/thuy/giot_suong_1/RegionMap.png` | `inbox/giot_suong_1/Concept.png` |
| 1 | N01 hai chùm mang | `refs/thuy/giot_suong_1/orig/N01.png`, concept | `inbox/giot_suong_1/orig_parts/N01.png` |
| 2 | N02 đầu và mặt | `.../orig/N02.png`, concept | `.../orig_parts/N02.png` |
| 3 | N03 nụ sen | `.../orig/N03.png`, concept | `.../orig_parts/N03.png` |
| 4 | N04 thân và yếm | `.../orig/N04.png`, concept | `.../orig_parts/N04.png` |
| 5 | N05 tay trái | `.../orig/N05.png`, concept | `.../orig_parts/N05.png` |
| 6 | N06 tay phải | `.../orig/N06.png`, concept | `.../orig_parts/N06.png` |
| 7 | N07 đuôi | `.../orig/N07.png`, concept | `.../orig_parts/N07.png` |
| 8 | N08 hai chân | `.../orig/N08.png`, concept | `.../orig_parts/N08.png` |

- Mỗi ảnh một lần gen. **Gen concept trước**, chờ Claude soi và duyệt, rồi mới gen 8 nhóm.
- Gen lại concept thì lưu `Concept_v2.png`, `_v3`… rồi báo bản nào được chọn. Gen lại nhóm thì ghi đè cùng tên.
- **Kiểm chung trước khi lưu ảnh nhóm:**
  - giữ khung vuông, vật nằm đúng chỗ như ảnh mẫu (chồng lên để so);
  - đầu khớp của mảnh ở đúng chỗ cũ; đầu nào của chi là gì đúng như ghi ở mục đó;
  - nền trắng trơn, không chữ.
- Gen xong concept thì nhắn Claude "duyệt concept giot_suong_1"; gen xong 8 nhóm thì nhắn "ghép giot_suong_1".

### 0. Concept

**Kiểm trước khi lưu:**
- nhìn qua là thấy con khác hẳn bóng xám: đầu bè, đỉnh tròn, mang xoè nhánh, đuôi vây to;
- vẫn đủ và đúng chỗ: hai tay buông, bàn tay ở **đầu dưới**; hai chân thẳng xuống, bàn chân ở dưới; đuôi ở dưới trái, chóp cong lên; hai chùm mang ở hai bên đầu; nụ sen trên đỉnh, cong sang trái;
- không thêm tay, cánh, sừng;
- không còn đầu giọt nước, vỏ sò, sọc cầu vồng;
- không màu vùng, không chữ.

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

### Khung MB5 dùng cho 8 nhóm

Hai kiểu khung, mỗi nhóm ghi rõ dùng kiểu nào (đã dán sẵn trong từng prompt).

- **Giữ viền** (thân, tay, chân): khung MB5 nguyên văn.
- **Đổi dáng** (mang, đầu, nụ sen, đuôi): giữ chỗ, góc và đầu khớp, nhưng lấy viền theo concept.

### 1. N01 hai chùm mang (đổi dáng)

**Kiểm:** gốc mỗi chùm ở đúng chỗ gốc cũ (trái: đầu dưới phải; phải: đầu dưới trái); ba nhánh xoè lên và ra ngoài; không vẽ đầu.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two fin-shaped ears on the sides of a head (the head is not shown). The viewer-left one points up and to the left, its base (where it joins the head) at its lower RIGHT end. The viewer-right one points up, its base at its LOWER left end. Redraw THESE two pieces as the two gill fans of image 2 (the approved concept): each one grows from its base end and splits into three feathery coral-pink frond branches with deeper pink feathering, spreading up and out; they may be longer and wider than the old fins.
Do NOT draw: a head, rainbow stripes, a smooth horn shape.

FRAMING: the same square canvas; each piece keeps its place, angle and direction from image 1, and its base end stays exactly where the old base is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be a different shape and bigger, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 2. N02 đầu và mặt (đổi dáng)

**Kiểm:** đầu bè rộng hơn hình mẫu, đỉnh tròn; mép dưới ở ngang mép dưới cũ (phủ cổ); đỉnh ở ngang đỉnh cũ; mắt, má, miệng đúng chỗ cũ; không có mang, không có nụ sen.

```
Image 1 is one group of a 2D cut-out animation puppet (the old design): a big round water-drop head with a face (two eyes, two cheeks, a mouth) and a lime crescent band near the top. Redraw THIS group as the head of image 2 (the approved concept): a wide baby-axolotl head, smooth sky-blue skin and a paler cream lower face, wider than the old head at both sides and with a rounded top instead of the point; the big round dark-blue eyes with white highlights, the pink cheeks and the wide smile exactly where the old eyes, cheeks and mouth are; a ring of small green lotus sepals where the lime crescent is.
Keep the bottom edge of the head at the same height as the old one (the neck goes under it) and the top at about the same height (a crest stands on it).
Do NOT draw: the gill fronds, the lotus bud, a neck, a body, a water-drop shine.

FRAMING: the same square canvas; the head keeps its place, angle and direction from image 1, and the eyes, cheeks and mouth stay exactly where they are, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be wider, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 3. N03 nụ sen (đổi dáng)

**Kiểm:** đáy nụ ở mép dưới cũ (chỗ cắm vào đầu), chóp nhọn cong lên sang trái, cỡ như cũ.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): a water-drop crest; its lower edge sits in the head and its pointed tip curls up to the upper left. Redraw THIS piece as the closed pink-and-white lotus bud of image 2 (the approved concept): overlapping petals, the base along the old lower edge, the pointed tip curling up and to the left like the old tip, about the same size.
Do NOT draw: a water drop, a head, leaves below the bud.

FRAMING: the same square canvas; the piece keeps its place, angle and direction from image 1, and its base stays exactly where the old lower edge is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1, and stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 4. N04 thân và yếm (giữ viền)

**Kiểm:** cổ hẹp ở trên, bụng tròn ở dưới, viền như cũ; yếm lá sen đúng chỗ vỏ sò; không có tay chân.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a small body shaped like a drop (narrow neck end at the TOP, round belly at the bottom) and a sea shell on the chest. Redraw THESE pieces as the body of image 2 (the approved concept): the body becomes the soft sky-blue belly with a cream belly patch, same outline; the shell becomes the small round green lotus-leaf bib tied with a red string, same place and size.
Do NOT draw: arms, legs, a head, a sea shell.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 5. N05 tay trái (giữ viền)

**Kiểm:** vai ở đầu trên phải, bàn tay ở **đầu dưới**; vòng dây đỏ ở chỗ vòng lá chanh.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a thin arm. Its TOP end (upper right) is the shoulder; it runs down to the left; the round hand is at the BOTTOM end, with a lime band at the wrist. Redraw THESE pieces as the viewer-left arm of image 2 (the approved concept): smooth sky-blue skin, a small four-fingered hand at the BOTTOM end with the fingers curled in, a thin red string bracelet where the lime band is.
Do NOT put the hand at the top. Do NOT draw: a sleeve, claws, a body.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 6. N06 tay phải (giữ viền)

**Kiểm:** vai ở đầu trên trái, bàn tay ở **đầu dưới**; vòng dây đỏ ở cổ tay.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a thin arm. Its TOP end (upper left) is the shoulder; it runs down and curves to the right; the round hand is at the BOTTOM end, with a lime band at the wrist. Redraw THESE pieces as the viewer-right arm of image 2 (the approved concept): smooth sky-blue skin, a small four-fingered hand at the BOTTOM end with the fingers curled in, a thin red string bracelet where the lime band is.
Do NOT put the hand at the top. Do NOT draw: a sleeve, claws, a body.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 7. N07 đuôi (đổi dáng)

**Kiểm:** mép nối thân vẫn ở **bên phải**, đúng chỗ mép thẳng cũ; chóp cong lên ở trên trái; vây cao, đuôi to hơn hình mẫu.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): a tail. The wide straight edge on the RIGHT is where it joins the body (hidden behind it); it sweeps to the left and its tip curls UP at the upper left, with orange and green stripes at the tip. Redraw THIS piece as the big axolotl tail of image 2 (the approved concept): sky-blue, a tall soft fin along its top and bottom edges, the fin edges and the tip coral pink; bigger than the old tail.
The joint end stays on the RIGHT, exactly where the old straight edge is; the tip still curls up at the upper left.
Do NOT draw: rainbow stripes, a body, legs.

FRAMING: the same square canvas; the piece keeps its place, angle and direction from image 1, and its joint edge stays exactly where it is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be bigger, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 8. N08 hai chân (giữ viền)

**Kiểm:** hông ở **đầu trên**, bàn chân ở **đầu dưới**, ngón chĩa xuống hơi sang trái ở cả hai chân.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two short legs. Each one has its hip at the TOP (the wide end) and its foot at the BOTTOM (the narrow pointed end, pointing down and slightly to the left). Redraw THESE two pieces as the two stubby legs of image 2 (the approved concept): sky-blue skin, small webbed feet at the BOTTOM ends with three tiny toes pointing down and slightly to the left.
Do NOT put the feet at the top. Do NOT draw: a body, a tail, shoes.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```
