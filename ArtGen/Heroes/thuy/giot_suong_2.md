# Giọt Sương dạng 2 (aola #8 露滴)

Tướng Thủy đầu tiên, dạng 2 trong 3. Tổng quan cả dòng: [giot_suong.md](giot_suong.md). Quy trình chung: [../QUY_TRINH.md](../QUY_TRINH.md).

**Gen concept dạng này sau khi concept dạng 1 được duyệt**, vì prompt đính kèm concept dạng 1 để giữ cùng một con lớn lên.

**Thiết kế do Claude đề xuất, duyệt ở bước concept:** bé kỳ giông dạng 1 lớn lên: mang dày hơn, nụ sen hé nở, tay thành vây có màng, đuôi dài. Dáng ngoài được đổi cho khác bản gốc; tay, chân, khớp giữ đúng rig.

| Bộ phận gốc | Thành | Dáng |
|---|---|---|
| bốn râu mảnh quanh đầu | bốn chùm mang lông vũ hồng san hô | **đổi dáng**: dày, xù, hai chùm trên dài hơn |
| mào năm gai cầu vồng trên cuống | hoa sen hồng trắng hé nở, nhụy vàng, trên cuống xanh | **đổi dáng**: tròn hơn, cỡ như cũ |
| đầu tròn, mảng xanh trên đỉnh | đầu kỳ giông bè ngang, cười há có lưỡi; mảng xanh thành vòng đài sen | **rộng hơn** |
| vỏ sò và ba hạt châu | cổ áo lá sen buộc dây đỏ, ba hạt sen xanh | |
| hai tay kiêm vây sọc cầu vồng | tay xanh mở thành vây màng ba thùy, chóp hồng san hô | giữ dáng |
| đuôi dài sáu khúc, hai thùy cuối | đuôi kỳ giông có vây thấp; hai thùy cuối thành quạt hình cánh sen | khúc đuôi giữ dáng, **hai thùy đổi dáng** |
| thân, hai chân | da xanh, bụng kem, bàn chân có màng | giữ dáng |

Màu như dạng 1: xanh da trời, bụng kem, hồng san hô, xanh lá sen, dây đỏ.

Đường dẫn ảnh tính từ `ArtGen/Heroes/`. **Chỉ dán khối prompt cho GPT, không đính kèm file này.**

## Rig mặt trước #8

Dữ liệu rig: `<aola>/reskin/pet8_parts/`. Bộ ghép: `<aola>/reskin/thuy_8/` (`regions.json`, `groups.json`).

- **Đứng:** 18 khung, 31 mảnh. Bốn râu (13–16), mào (30) và cả đuôi (6–11) đứng yên; đầu và thân nhún cùng một khối; bọt nước (2–5) bay quanh.
- **Trúng đòn:** 15 khung, 16 hình mới. Râu và mào vắng hẳn, thay bằng hình cả cụm (82, 93); đuôi thay bằng hình khác (53…). Lúc ghép phải làm biến thể.
- **Đánh thường:** 43 khung, 19 hình mới; râu, mào, đuôi lại thay bằng hình cả cụm ở nhiều khung.
- **Chiêu:** 28 khung, 12 hình mới; đuôi vẽ lại từng khúc (173–182), mào vắng.

Ảnh rig có đánh số: `refs/thuy/giot_suong_2/Rig_Numbered.png`.

### Giải phẫu từng mảnh

Trái, phải theo **người xem**. Con đứng thẳng, mặt nhìn ra trước.

| Mảnh | Là gì | Hai đầu, hướng |
|---|---|---|
| 1 | bóng dưới chân | giữ |
| 2–5 | bọt nước bay quanh | giữ (hiệu ứng) |
| 15 | râu dài trái | gốc ở **đầu dưới phải** (dính đầu), chóp chĩa **lên trái** |
| 16 | râu ngắn trái | gốc ở **đầu phải**, chóp chĩa **sang trái** |
| 13 | râu dài phải | gốc ở **đầu dưới**, chóp chĩa **lên** |
| 14 | râu ngắn phải | gốc ở **đầu trái**, chóp chĩa **sang phải** |
| 30 | mào năm thùy trên cuống vàng chanh | cuống ở **dưới**, cắm vào đỉnh đầu; năm thùy xoè lên và sang trái |
| 24 | đầu tròn | |
| 25 | mảng xanh đậm trên đỉnh đầu | ngay dưới cuống mào |
| 26 | vệt sáng trên đầu | |
| 27, 31 | mắt trái, mắt phải | nhìn ra trước |
| 28 | miệng há thè lưỡi | |
| 19 | thân hình giọt | đầu hẹp ở **trên** (cổ, khuất dưới đầu), bụng tròn ở **dưới** |
| 29 | vỏ sò trên ngực | |
| 22, 23, 17 | ba hạt châu ở cổ (trái, giữa trái, phải) | |
| 21 | tay trái kiêm vây, nằm **trên** thân | vai ở **đầu trên phải** (cạnh hạt châu); tay đi xuống rồi xoè thành vây ba thùy chĩa **sang trái** |
| 12 | tay phải kiêm vây, nằm **sau** thân | vai ở **đầu trên**; buông xuống, cong sang phải; vây ba thùy ở **đầu dưới**, chĩa xuống |
| 6 | khúc đuôi gốc | đầu **trên phải** nối thân (khuất sau thân, dưới vây tay trái); đi xuống trái |
| 7 | khúc đuôi cong | vòng ở bên trái, quay xuống rồi sang phải |
| 8 | khúc đuôi dọc mặt đất | đi sang phải |
| 9 | khúc đuôi cuối | quay xuống ở bên phải |
| 11, 10 | hai thùy vây cuối đuôi (trên, dưới) | gốc ở **phải** (nối khúc 9), chóp chĩa **sang trái** |
| 20 | chân trái | hông ở **trên**, bàn chân nhọn ở **dưới**, chĩa thẳng xuống |
| 18 | chân phải | hông ở **trên**, bàn chân ở **dưới**, mũi cong sang trái |

### Chỗ nào được đổi dáng

| Mảnh | Đổi dáng | Phải giữ |
|---|---|---|
| râu (13–16) | thành chùm mang dày, xù; hai chùm trên dài hơn được | gốc ở chỗ cũ, khuất sau đầu |
| mào (30) | hoa sen hé nở, tròn hơn | cuống ở chỗ cũ trên đỉnh đầu |
| đầu (24) | rộng ra hai bên, đỉnh tròn | đỉnh đỡ cuống sen; mép dưới phủ cổ; mắt, miệng ở chỗ cũ (mảnh riêng) |
| hai thùy cuối đuôi (10, 11) | quạt hình cánh sen, to hơn chút | gốc nối khúc 9 ở chỗ cũ |
| thân, hai tay vây, hai chân, khúc đuôi 6–9 | không | giữ viền: các khúc đuôi phải nối liền nhau |

Ảnh mẫu N03 (đầu) có khung rộng hơn mảnh (`frame` trong `groups.json`) để có chỗ vẽ to ra.

### Ảnh và chỗ lưu

| # | Gen gì | Đính kèm (theo thứ tự) | Lưu ảnh GPT vào |
|---|---|---|---|
| 0 | Concept | `refs/thuy/giot_suong_2/Silhouette.png`, `refs/thuy/giot_suong_2/RegionMap.png`, concept dạng 1 đã duyệt (`inbox/giot_suong_1/Concept.png`) | `inbox/giot_suong_2/Concept.png` |
| 1 | N01 bốn chùm mang | `refs/thuy/giot_suong_2/orig/N01.png`, concept dạng 2 | `inbox/giot_suong_2/orig_parts/N01.png` |
| 2 | N02 hoa sen | `.../orig/N02.png`, concept dạng 2 | `.../orig_parts/N02.png` |
| 3 | N03 đầu và mặt | `.../orig/N03.png`, concept dạng 2 | `.../orig_parts/N03.png` |
| 4 | N04 thân, cổ áo, hạt sen | `.../orig/N04.png`, concept dạng 2 | `.../orig_parts/N04.png` |
| 5 | N05 tay vây trái | `.../orig/N05.png`, concept dạng 2 | `.../orig_parts/N05.png` |
| 6 | N06 tay vây phải | `.../orig/N06.png`, concept dạng 2 | `.../orig_parts/N06.png` |
| 7 | N07 đuôi | `.../orig/N07.png`, concept dạng 2 | `.../orig_parts/N07.png` |
| 8 | N08 hai chân | `.../orig/N08.png`, concept dạng 2 | `.../orig_parts/N08.png` |

- Mỗi ảnh một lần gen. **Gen concept trước**, chờ Claude soi và duyệt, rồi mới gen 8 nhóm.
- Gen lại concept thì lưu `Concept_v2.png`, `_v3`… rồi báo bản nào được chọn. Gen lại nhóm thì ghi đè cùng tên.
- **Kiểm chung trước khi lưu ảnh nhóm:**
  - giữ khung vuông, vật nằm đúng chỗ như ảnh mẫu (chồng lên để so);
  - đầu khớp của mảnh ở đúng chỗ cũ; đầu nào của chi là gì đúng như ghi ở mục đó;
  - nền trắng trơn, không chữ.
- Gen xong concept thì nhắn Claude "duyệt concept giot_suong_2"; gen xong 8 nhóm thì nhắn "ghép giot_suong_2".

### 0. Concept

**Kiểm trước khi lưu:**
- nhìn là biết cùng con với concept dạng 1, lớn hơn;
- khác hẳn bóng xám: đầu bè, mang xù, hoa sen thay mào gai, quạt đuôi cánh sen;
- vẫn đủ và đúng chỗ: tay trái xoè vây sang **trái**; tay phải buông, vây ở **đầu dưới**; hai chân thẳng xuống; đuôi đi xuống trái, vòng, chạy dọc đất sang phải, quay xuống, quạt cuối chĩa **trái**; bốn chùm mang quanh đầu; hoa sen trên cuống ở đỉnh;
- không thêm tay, cánh, sừng;
- không còn sọc cầu vồng, vỏ sò, hạt châu;
- không màu vùng, không chữ.

```
Character concept for a 2D cut-out animation game. Draw ONE original creature, the second evolution stage of a water pet for a cute creature-collecting battle game, in the same front view and pose as image 1, on a plain light grey background. Image 3 is the approved first stage of the same creature: keep its species, colours, face and lotus theme, and make it a little older, longer and more elegant. An original design that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one head with four growths on its sides (two long ones pointing up, two short ones pointing sideways) and one crest on a short stem on top, one small body, two arms that end in fins, two legs, one long tail; no wings, no extra limbs;
- every joint where it is: the neck hidden under the bottom of the head; the shoulders at the top of the body beside the neck; the hips under the body; the tail coming out from behind the body at the left, under the viewer-left arm; the four growths starting at the sides of the head; the crest stem standing on top of the head;
- every limb pointing the same way: the viewer-left arm goes down from the shoulder and opens into a wide fin pointing LEFT; the viewer-right arm hangs down to the right with its fin at the BOTTOM end, pointing down; the legs go straight down with the feet at the BOTTOM; the tail runs down to the left, curls, runs right along the ground, turns down, and ends in two fin lobes pointing LEFT;
- the body, arms, legs and tail about the size and shape of regions 4, 6, 7, 8, 9 and 10; the whole figure about the same height.

CHANGE (the new outline, region by region):
1 the four growths: four feathery gill fronds like an axolotl's gills, coral pink with deeper pink feathering, thicker and fluffier than the thin shapes in image 1, the two upper ones longer.
2 crest: a half-open pink-and-white lotus flower with layered pointed petals and a yellow centre, on a short green stem; about the size of region 2 but rounder, not a fan of spikes.
3 head: a wide young-axolotl head, wider than region 3 at both sides, with a rounded top; smooth sky-blue skin, a paler cream lower face, big round dark-blue eyes with white highlights, a wide happy open smile with a small pink tongue. A ring of small green lotus sepals where the stem meets the head.
4 body: a soft sky-blue body with a cream belly patch, narrow at the neck.
5 at the neck and chest: a round green lotus-leaf collar tied with a red string, and three small green lotus seeds as beads at the neck.
6 viewer-left arm: TOP end = shoulder, a short sky-blue arm that opens into a webbed fin of three soft lobes pointing LEFT; pale aqua webbing, coral-pink lobe tips.
7 viewer-right arm: TOP end = shoulder, it hangs down to the right, a webbed fin of three soft lobes at the BOTTOM end pointing down; same colours.
8 tail: a long smooth sky-blue tail with a low soft fin along its top, along the same path as region 8; at the end a fan of two lotus-petal-shaped fin lobes pointing LEFT, pale pink fading to coral pink at the tips.
9 and 10 legs: two short legs, hip at the TOP, small webbed feet at the BOTTOM.

STYLE: clean 2D cartoon game art for a cut-out rig. Crisp outlines of even weight; each outline is a darker shade of the colour it surrounds, never pure black. Flat colours with one level of cel shading and small highlights. No painterly texture, no pencil or crayon hatching, no large gradients, no motion blur. Every part clearly separated by its outline.

AVOID: a water-drop or teardrop head, a fan of spikes on the head, rainbow-striped fins, feelers or tail, a sea shell, pearls, bubbles, human features, clothes, weapons, extra limbs, text, labels, numbers, the region colours, frames, background scenery, a second view.
```

### Khung MB5 dùng cho 8 nhóm

- **Giữ viền** (thân, hai tay vây, hai chân): khung MB5 nguyên văn.
- **Đổi dáng** (mang, hoa sen, đầu): giữ chỗ, góc và đầu khớp, lấy viền theo concept.
- **Đuôi** (N07): các khúc giữ viền, chỉ hai thùy cuối đổi dáng.

### 1. N01 bốn chùm mang (đổi dáng)

**Kiểm:** gốc mỗi chùm ở đúng chỗ gốc cũ; hai chùm trên chĩa lên, hai chùm dưới chĩa ngang ra ngoài; không vẽ đầu.

```
Image 1 is four pieces of a 2D cut-out animation puppet (the old design): four thin feelers on the sides of a head (the head is not shown). Viewer-left: a long one pointing up and to the left, its base (where it joins the head) at its lower RIGHT end, and a short one pointing left, its base at its RIGHT end. Viewer-right: a long one pointing up, its base at its LOWER end, and a short one pointing right, its base at its LEFT end. Redraw THESE four pieces as the four gill fronds of image 2 (the approved concept): feathery, coral pink with deeper pink feathering, each one growing from its base end to its tip; thicker and fluffier than the old feelers, and the two long ones may be longer.
Do NOT draw: a head, rainbow stripes, thin smooth spikes.

FRAMING: the same square canvas; each piece keeps its place, angle and direction from image 1, and its base end stays exactly where the old base is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be a different shape and bigger, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 2. N02 hoa sen (đổi dáng)

**Kiểm:** cuống xanh ở đúng chỗ cuống cũ, mép dưới; hoa tròn, cánh nhọn xếp lớp, cỡ như mào cũ.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): a crest on top of a head: a short stem at the BOTTOM (it stands on the head) and five long rainbow-tipped lobes fanning up and to the left. Redraw THIS piece as the half-open pink-and-white lotus flower of image 2 (the approved concept): layered pointed petals around a yellow centre, on a short green stem; the stem stays exactly where the old stem is; the flower about the same size as the old crest but rounder, leaning a little to the left like the old crest.
Do NOT draw: a head, spikes, rainbow stripes, leaves.

FRAMING: the same square canvas; the piece keeps its place, angle and direction from image 1, and its stem stays exactly where the old stem is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1, and stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 3. N03 đầu và mặt (đổi dáng)

**Kiểm:** đầu bè rộng hơn hình mẫu, đỉnh tròn; mép dưới ở ngang mép dưới cũ (phủ cổ); đỉnh ở ngang đỉnh cũ; mắt, miệng đúng chỗ cũ; vòng đài sen ở chỗ mảng xanh trên đỉnh; không có mang, không có hoa sen.

```
Image 1 is one group of a 2D cut-out animation puppet (the old design): a round head with a face (two eyes, an open mouth with a tongue), a dark-blue patch on top and a small shine. Redraw THIS group as the head of image 2 (the approved concept): a wide young-axolotl head, smooth sky-blue skin and a paler cream lower face, wider than the old head at both sides, with a rounded top; the big round dark-blue eyes with white highlights and the wide open smile with a small pink tongue exactly where the old eyes and mouth are; a ring of small green lotus sepals where the dark-blue patch is.
Keep the bottom edge of the head at the same height as the old one (the neck goes under it) and the top at about the same height (the flower stem stands on it).
Do NOT draw: the gill fronds, the lotus flower, a neck, a body.

FRAMING: the same square canvas; the head keeps its place, angle and direction from image 1, and the eyes and mouth stay exactly where they are, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be wider, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 4. N04 thân, cổ áo, hạt sen (giữ viền)

**Kiểm:** cổ hẹp ở trên, bụng tròn ở dưới, viền như cũ; cổ áo lá sen đúng chỗ vỏ sò; ba hạt sen đúng chỗ ba hạt châu; không có tay chân.

```
Image 1 is five pieces of a 2D cut-out animation puppet (the old design): a small body shaped like a drop (narrow neck end at the TOP, round belly at the bottom), a sea shell on the chest and three round beads at the neck. Redraw THESE pieces as the body of image 2 (the approved concept): the body becomes the soft sky-blue body with a cream belly patch, same outline; the shell becomes the round green lotus-leaf collar tied with a red string, same place and size; the three beads become three small green lotus seeds, same places.
Do NOT draw: arms, legs, a head, a sea shell, pearls.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 5. N05 tay vây trái (giữ viền)

**Kiểm:** vai ở **đầu trên phải** (đầu hẹp); vây ba thùy chĩa **sang trái**; không có bàn tay ngón.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): an arm that is also a fin. Its TOP end (the narrow end at the upper right) is the shoulder; it runs down and opens into a wide fin of three lobes pointing LEFT, with lime and red stripes on the lobes. Redraw THIS piece as the viewer-left arm of image 2 (the approved concept): a short sky-blue arm from the shoulder at the TOP end, opening into a webbed fin of three soft lobes pointing left, pale aqua webbing and coral-pink lobe tips.
Do NOT put the fin at the top. Do NOT draw: a hand with fingers, claws, a body, rainbow stripes.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 6. N06 tay vây phải (giữ viền)

**Kiểm:** vai ở **đầu trên** (đầu hẹp); vây ba thùy ở **đầu dưới**, chĩa xuống.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): an arm that is also a fin. Its TOP end (the narrow end at the upper left) is the shoulder; it hangs down and curves to the right; at the BOTTOM end it splits into three fin lobes pointing down, with lime and red stripes. Redraw THIS piece as the viewer-right arm of image 2 (the approved concept): a sky-blue arm from the shoulder at the TOP end, a webbed fin of three soft lobes at the BOTTOM end pointing down, pale aqua webbing and coral-pink lobe tips.
Do NOT put the fin at the top. Do NOT draw: a hand with fingers, claws, a body, rainbow stripes.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 7. N07 đuôi (khúc giữ viền, thùy cuối đổi dáng)

**Kiểm:** đầu nối thân ở **trên phải** của khúc gốc; các khúc nối liền, đi đúng đường cũ; quạt cuối chĩa **sang trái**, gốc ở chỗ cũ.

```
Image 1 is six pieces of a 2D cut-out animation puppet (the old design): a long tail in segments. The top segment's upper RIGHT end joins the body (hidden behind it); the tail runs down to the left, curls at the far left, runs right along the ground, turns down at the right, and ends in two fin lobes (upper and lower) whose base is at their RIGHT end and whose red tips point LEFT. Redraw THESE pieces as the tail of image 2 (the approved concept): a smooth sky-blue tail with a low soft fin along its top edge, following exactly the old segments; the two end lobes become a fan of lotus-petal-shaped fin lobes pointing left, pale pink fading to coral pink at the tips.
Do NOT draw: rainbow stripes, a body, legs, gaps between the segments.

FRAMING: the same square canvas; every piece keeps its place, angle and direction from image 1, so the drawing can be put back on the old puppet. The segments keep their outline from image 1 so they still join each other. The two end lobes keep their base where it is; their outline follows image 2: they may be a little bigger, but stay inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 8. N08 hai chân (giữ viền)

**Kiểm:** hông ở **đầu trên**, bàn chân ở **đầu dưới** ở cả hai chân.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two short legs. Each one has its hip at the TOP (the wide end) and its foot at the BOTTOM: the viewer-left one ends in a point pointing straight down, the viewer-right one ends in a foot curling slightly to the left. Redraw THESE two pieces as the two legs of image 2 (the approved concept): sky-blue skin, small webbed feet at the BOTTOM ends with three tiny toes pointing down.
Do NOT put the feet at the top. Do NOT draw: a body, a tail, shoes.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```
