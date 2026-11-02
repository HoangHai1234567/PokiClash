# Giọt Sương dạng 3 (aola #9 露西亚)

Tướng Thủy đầu tiên, dạng 3 trong 3 (dạng cuối). Tổng quan cả dòng: [giot_suong.md](giot_suong.md). Quy trình chung: [../QUY_TRINH.md](../QUY_TRINH.md).

**Gen concept dạng này sau khi concept dạng 2 được duyệt**, vì prompt đính kèm concept dạng 2 để giữ cùng một con lớn lên.

**Thiết kế do Claude đề xuất, duyệt ở bước concept:** kỳ giông lớn thành **thủy long sen** cổ dài, bốn chân, mặt hiền kiểu kỳ giông, ba chùm mang lông vũ, quạt đuôi hình cánh sen. Dáng ngoài được đổi cho khác bản gốc; chân, cổ, khớp giữ đúng rig.

| Bộ phận gốc | Thành | Dáng |
|---|---|---|
| ba cặp lông mào chóp cầu vồng | ba chùm mang lông vũ hồng san hô | **đổi dáng**: xù, to hơn |
| đầu đội mũ xanh đậm có lưỡi trai nhọn | đầu thủy long mõm tròn rộng, cười hiền, hàm dưới kem; hết mũ | **đổi dáng** |
| chuỗi hạt châu, mặt dây vỏ sò | chuỗi hạt sen xanh trên dây đỏ, mặt dây là đài sen | |
| cổ, thân | da xanh, cổ họng và bụng kem, lưng xanh đậm có đốm nhạt | giữ dáng |
| bốn chân, vành vàng chanh, vuốt đỏ | chân xanh, cổ chân bọc lá sen, bàn chân màng ngón hồng san hô | giữ dáng |
| đuôi, hai thùy vây cuối | đuôi lưng xanh đậm bụng kem, vây thấp; hai thùy thành quạt cánh sen to | đuôi giữ dáng, **hai thùy đổi dáng** |

Màu như dạng 1, 2: xanh da trời, bụng kem, hồng san hô, xanh lá sen, dây đỏ; thêm xanh đậm ở lưng.

Đường dẫn ảnh tính từ `ArtGen/Heroes/`. **Chỉ dán khối prompt cho GPT, không đính kèm file này.**

## Rig mặt trước #9

Dữ liệu rig: `<aola>/reskin/pet9_parts/`. Bộ ghép: `<aola>/reskin/thuy_9/` (`regions.json`, `groups.json`).

- **Đứng:** 22 khung, 19 mảnh. Con bốn chân đứng nghiêng, nhìn sang phải. Đuôi (14) đứng yên, hai thùy vây (15, 16) quẫy mạnh; đầu đi cùng mắt; chuỗi hạt đi cùng mặt dây; ba đốm (17–19) bay quanh.
- **Trúng đòn:** 16 khung, 6 hình mới; đuôi và mắt đổi hình, đốm vắng. Lúc ghép phải làm biến thể.
- **Đánh thường:** 49 khung, 6 hình mới; thân (123, 129) và đầu (127) đổi hình ở khung 5–46.
- **Chiêu:** 42 khung, 14 hình mới; đuôi vẽ lại nhiều khung, chân trước gần (92) và mắt (134) đổi hình; có 2 quầng lớn (69, 75).

Ảnh rig có đánh số: `refs/thuy/giot_suong_3/Rig_Numbered.png`.

### Giải phẫu từng mảnh

Trái, phải theo **người xem**. Con đứng bốn chân, thân nghiêng, đầu ở trên cao bên phải, nhìn sang phải; đuôi kéo dài sang trái.

| Mảnh | Là gì | Hai đầu, hướng |
|---|---|---|
| 1 | bóng dưới chân | giữ |
| 17–19 | đốm nhỏ bay quanh | giữ (hiệu ứng) |
| 13 | cặp lông mào lớn bên trái, nằm trên đầu | gốc ở **đầu dưới phải** (dính sau đầu), chóp chĩa **lên trái** |
| 5 | cặp lông mào trên đỉnh, nằm trên đầu | gốc ở **đầu dưới phải** (cuống vàng chanh trên đỉnh đầu), chóp chĩa **lên trái** |
| 3 | cặp lông mào nhỏ bên phải, nằm **sau** đầu | gốc ở **đầu dưới**, chóp chĩa **lên** |
| 4 | đầu: mũ xanh đậm trùm đỉnh và mõm, lưỡi trai nhọn chĩa sang phải; phần xanh nhạt phía sau, dưới | cổ nối ở **dưới trái** của đầu; mõm chĩa **sang phải** |
| 12 | mắt | trong mảng xanh đậm, nhìn sang phải |
| 7 | cổ dài và thân lớn | đầu cổ ở **trên phải** (khuất dưới đầu); lưng xanh đậm phía trái, ngực xanh nhạt phía phải |
| 11 | chuỗi hạt châu vòng quanh cổ | |
| 10 | mặt dây vỏ sò trên ngực | |
| 9 | chân trước gần, nằm **trên** thân | vai ở **đầu trên** (hẹp, cao trên ngực); thẳng xuống; **đầu dưới** là bàn chân: vành vàng chanh rồi ba vuốt đỏ chĩa xuống |
| 6 | chân trước xa, nằm **sau** thân, bên phải | vai ở **trên**; bàn chân ở **dưới**, vuốt chĩa xuống |
| 8 | chân sau gần, bên trái, xanh đậm, nằm trên thân | hông ở **trên**, bàn chân nhọn ở **dưới**, chĩa xuống |
| 2 | chân sau xa, nằm sau thân, gần như khuất sau chân 9 | hông ở **trên**, bàn chân ở **dưới** |
| 14 | đuôi, nằm trên mép thân | đầu **phải** to, nối thân; thon dần sang trái |
| 15, 16 | hai thùy vây cuối đuôi (trên, dưới) | gốc ở **phải** (nối chóp đuôi), chóp chĩa **sang trái** |

### Chỗ nào được đổi dáng

| Mảnh | Đổi dáng | Phải giữ |
|---|---|---|
| lông mào (3, 5, 13) | chùm mang lông vũ xù, to hơn | gốc ở chỗ cũ |
| đầu (4) | đầu thủy long mõm tròn rộng, hết mũ và lưỡi trai | chỗ nối cổ ở dưới trái; mắt ở chỗ cũ (mảnh riêng) |
| chuỗi hạt, mặt dây (10, 11) | hạt sen, đài sen | chuỗi đi đúng đường cũ; mặt dây treo ở chỗ vỏ sò |
| hai thùy cuối đuôi (15, 16) | quạt hình cánh sen, to hơn | gốc nối chóp đuôi ở chỗ cũ |
| cổ và thân, bốn chân, đuôi (14) | không | giữ viền |

Ảnh mẫu N01 (mào) và N02 (đầu) dùng chung một khung rộng (`frame` trong `groups.json`) để có chỗ vẽ to ra.

### Ảnh và chỗ lưu

| # | Gen gì | Đính kèm (theo thứ tự) | Lưu ảnh GPT vào |
|---|---|---|---|
| 0 | Concept | `refs/thuy/giot_suong_3/Silhouette.png`, `refs/thuy/giot_suong_3/RegionMap.png`, concept dạng 2 đã duyệt (`inbox/giot_suong_2/Concept.png`) | `inbox/giot_suong_3/Concept.png` |
| 1 | N01 ba chùm mang | `refs/thuy/giot_suong_3/orig/N01.png`, concept dạng 3 | `inbox/giot_suong_3/orig_parts/N01.png` |
| 2 | N02 đầu và mắt | `.../orig/N02.png`, concept dạng 3 | `.../orig_parts/N02.png` |
| 3 | N03 cổ và thân | `.../orig/N03.png`, concept dạng 3 | `.../orig_parts/N03.png` |
| 4 | N04 chuỗi hạt sen | `.../orig/N04.png`, concept dạng 3 | `.../orig_parts/N04.png` |
| 5 | N05 chân trước gần | `.../orig/N05.png`, concept dạng 3 | `.../orig_parts/N05.png` |
| 6 | N06 chân trước xa | `.../orig/N06.png`, concept dạng 3 | `.../orig_parts/N06.png` |
| 7 | N07 hai chân sau | `.../orig/N07.png`, concept dạng 3 | `.../orig_parts/N07.png` |
| 8 | N08 đuôi | `.../orig/N08.png`, concept dạng 3 | `.../orig_parts/N08.png` |

- Mỗi ảnh một lần gen. **Gen concept trước**, chờ Claude soi và duyệt, rồi mới gen 8 nhóm.
- Gen lại concept thì lưu `Concept_v2.png`, `_v3`… rồi báo bản nào được chọn. Gen lại nhóm thì ghi đè cùng tên.
- **Kiểm chung trước khi lưu ảnh nhóm:**
  - giữ khung vuông, vật nằm đúng chỗ như ảnh mẫu (chồng lên để so);
  - đầu khớp của mảnh ở đúng chỗ cũ; đầu nào của chi là gì đúng như ghi ở mục đó;
  - nền trắng trơn, không chữ.
- Gen xong concept thì nhắn Claude "duyệt concept giot_suong_3"; gen xong 8 nhóm thì nhắn "ghép giot_suong_3".

### 0. Concept

**Kiểm trước khi lưu:**
- nhìn là biết cùng con với concept dạng 2, đã trưởng thành;
- khác hẳn bóng xám: đầu mõm tròn không mũ, mang xù thay lông mào, quạt đuôi cánh sen;
- vẫn đủ và đúng chỗ: bốn chân thẳng xuống, bàn chân ở **dưới**; cổ dài nối đầu ở dưới trái; đầu nhìn sang **phải**; đuôi kéo sang **trái**, quạt cuối chĩa trái;
- không thêm cánh, tay, sừng;
- không còn mũ, lưỡi trai, mỏ, sọc cầu vồng, vỏ sò, hạt châu;
- không màu vùng, không chữ.

```
Character concept for a 2D cut-out animation game. Draw ONE original creature, the third and final evolution stage of a water pet for a cute creature-collecting battle game, in the same side three-quarter view and pose as image 1 (it stands on four legs and looks to the right), on a plain light grey background. Image 3 is the approved second stage of the same creature: keep its species, colours, face and lotus theme, now grown into a graceful long-necked water dragon. An original design that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.

Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do not trace their outline. Viewer-left and viewer-right mean as seen in the picture.

KEEP FROM THE RIG (the animation moves these parts around these joints):
- the same parts, no more, no fewer: one head on a long neck, three growths on the head, a big body, four legs, one long tail; no wings, no arms, no extra limbs;
- every joint where it is: the head on top of the long neck, the neck joining the lower-left side of the head; the growths starting at the top and back of the head; the near front leg starting high on the chest; the far front leg behind the chest at the right; the near hind leg at the left under the back; the far hind leg mostly hidden behind the near front leg; the tail leaving the body at the lower left;
- every limb pointing the same way: all four legs go straight down with the feet at the BOTTOM; the head faces right, its snout pointing right; the growths sweep up and to the left; the tail runs to the left and ends in two fin lobes pointing LEFT;
- the neck, body, legs and tail about the size and shape of regions 3, 5, 6, 7, 8 and 9; the whole figure about the same height.

CHANGE (the new outline, region by region):
1 the three growths: three big feathery gill fronds like an axolotl's gills, coral pink with deeper pink feathering, sweeping up and back from the head; bigger and fluffier than the shapes in image 1.
2 head: a broad, rounded water-dragon head with a gentle axolotl face: a wide rounded snout pointing right, a long happy closed smile, a big dark-blue eye with a white highlight, smooth sky-blue skin with a cream lower jaw; no helmet, no visor, no beak. A ring of small green lotus sepals at the base of the gill fronds.
3 neck and body: smooth sky-blue skin, a cream throat and belly along the front, a deeper blue back with a few small soft lighter spots.
4 necklace: a string of green lotus seeds on a red cord around the neck, with a lotus seed-pod pendant on the chest.
5, 6, 7, 8 legs: sturdy sky-blue legs (the hind legs a deeper blue), a green lotus-leaf cuff above each foot, webbed feet with three coral-pink toes pointing down.
9 tail: a long tapering tail, deep blue on top and cream underneath, with a low soft fin along its top; at the end a big fan of two lotus-petal-shaped fin lobes pointing LEFT, pale pink fading to coral pink at the tips.

STYLE: clean 2D cartoon game art for a cut-out rig. Crisp outlines of even weight; each outline is a darker shade of the colour it surrounds, never pure black. Flat colours with one level of cel shading and small highlights. No painterly texture, no pencil or crayon hatching, no large gradients, no motion blur. Every part clearly separated by its outline.

AVOID: a helmet or hood on the head, a visor, a beak, rainbow-tipped feathers, rainbow stripes, red claws, a sea shell, pearls, human features, clothes, weapons, wings, extra limbs, text, labels, numbers, the region colours, frames, background scenery, a second view.
```

### Khung MB5 dùng cho 8 nhóm

- **Giữ viền** (cổ và thân, bốn chân): khung MB5 nguyên văn.
- **Đổi dáng** (mang, đầu, chuỗi hạt): giữ chỗ, góc và đầu khớp, lấy viền theo concept.
- **Đuôi** (N08): thân đuôi giữ viền, chỉ hai thùy cuối đổi dáng.

### 1. N01 ba chùm mang (đổi dáng)

**Kiểm:** gốc mỗi chùm ở đúng chỗ gốc cũ; hai chùm lớn chĩa lên trái, chùm nhỏ bên phải chĩa lên; không vẽ đầu.

```
Image 1 is three pieces of a 2D cut-out animation puppet (the old design): three pairs of feathers on a head (the head is not shown). The big pair at the lower left and the pair at the top both have their base (where they join the head) at their lower RIGHT end and point up and to the left; the small pair at the right has its base at its BOTTOM end and points up. Redraw THESE three pieces as the three gill fronds of image 2 (the approved concept): feathery, coral pink with deeper pink feathering, each one growing from its base end; bigger and fluffier than the old feathers.
Do NOT draw: a head, rainbow tips, smooth leaf-shaped feathers.

FRAMING: the same square canvas; each piece keeps its place, angle and direction from image 1, and its base end stays exactly where the old base is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be a different shape and bigger, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, navy around deep blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 2. N02 đầu và mắt (đổi dáng)

**Kiểm:** chỗ nối cổ ở **dưới trái** như cũ; mắt đúng chỗ cũ; mõm tròn chĩa sang phải; không còn mũ, lưỡi trai, mỏ; không có mang.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a head at the top of a long neck (the neck is not shown), facing right: a dark-blue helmet-like top with a pointed visor towards the right, a pale aqua part at the back and bottom where the neck joins at the lower LEFT, and one eye in the dark-blue part. Redraw THESE pieces as the head of image 2 (the approved concept): a broad, rounded water-dragon head with a gentle axolotl face, a wide rounded snout pointing right, a long happy smile, smooth sky-blue skin with a cream lower jaw; the big dark-blue eye with a white highlight exactly where the old eye is; a ring of small green lotus sepals on top where the fronds start.
The neck joint stays at the lower LEFT, where the old pale part is.
Do NOT draw: a helmet, a visor, a beak, the gill fronds, a neck.

FRAMING: the same square canvas; the head keeps its place, angle and direction from image 1, and its neck joint and the eye stay exactly where they are, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be a different shape and bigger, but stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, navy around deep blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 3. N03 cổ và thân (giữ viền)

**Kiểm:** đầu cổ ở **trên phải**, viền như cũ; lưng xanh đậm phía trái, cổ họng và bụng kem phía phải; không có chân, đuôi, chuỗi hạt.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): a long neck and a big body. The neck's TOP end (upper right) goes under the head; the body is wide at the bottom; the back on the left is dark blue, the chest on the right pale aqua. Redraw THIS piece as the neck and body of image 2 (the approved concept): smooth sky-blue skin, a cream throat and belly along the front (right side), a deeper blue back (left side) with a few small soft lighter spots, same outline.
Do NOT draw: a head, legs, a tail, a necklace.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, navy around deep blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 4. N04 chuỗi hạt sen (đổi dáng)

**Kiểm:** chuỗi hạt đi đúng đường cũ quanh cổ; mặt dây đài sen ở chỗ vỏ sò, cỡ như cũ.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): a string of round beads going around a neck (the neck is not shown) and a shell pendant on the chest. Redraw THESE pieces as the necklace of image 2 (the approved concept): a string of green lotus seeds on a red cord along the same path as the old beads, and a lotus seed-pod pendant (a green-yellow cone with seed holes on its flat top) where the shell is, about the same size.
Do NOT draw: pearls, a sea shell, a neck, a body.

FRAMING: the same square canvas; the pieces keep their place, angle and direction from image 1: the string follows the old path and the pendant hangs where the old shell is, so the drawing can be put back on the old puppet. The outline of the pendant follows image 2 and stays inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, navy around deep blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 5. N05 chân trước gần (giữ viền)

**Kiểm:** vai ở **đầu trên** (đầu hẹp); bàn chân ở **đầu dưới**, ngón chĩa xuống; cổ chân lá sen ở chỗ vành vàng chanh.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): a long front leg. Its TOP end (the narrow end, high on the chest) is the shoulder; it goes straight down; at the BOTTOM it has a lime band and three red claws pointing down. Redraw THIS piece as the near front leg of image 2 (the approved concept): sky-blue skin, a green lotus-leaf cuff where the lime band is, a webbed foot with three coral-pink toes pointing down at the BOTTOM end.
Do NOT put the foot at the top. Do NOT draw: a body, red claws, stripes.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, navy around deep blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 6. N06 chân trước xa (giữ viền)

**Kiểm:** vai ở **đầu trên**; bàn chân ở **đầu dưới**, ngón chĩa xuống.

```
Image 1 is one piece of a 2D cut-out animation puppet (the old design): a front leg on the far side (behind the body). Its TOP end (the narrow end) is the shoulder; it goes down; at the BOTTOM it has a lime band and three red claws pointing down. Redraw THIS piece as the far front leg of image 2 (the approved concept): sky-blue skin a little darker than the near leg, a green lotus-leaf cuff where the lime band is, a webbed foot with three coral-pink toes pointing down at the BOTTOM end.
Do NOT put the foot at the top. Do NOT draw: a body, red claws, stripes.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, navy around deep blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 7. N07 hai chân sau (giữ viền)

**Kiểm:** hông ở **đầu trên**, bàn chân ở **đầu dưới** ở cả hai chân.

```
Image 1 is two pieces of a 2D cut-out animation puppet (the old design): two hind legs. The viewer-left one (wider, dark blue) has its hip at the TOP and a pointed foot at the BOTTOM pointing down; the narrower one at the right is the far hind leg, hip at the TOP, foot at the BOTTOM. Redraw THESE pieces as the hind legs of image 2 (the approved concept): deeper blue skin, a green lotus-leaf cuff above each foot, webbed feet with coral-pink toes pointing down at the BOTTOM ends.
Do NOT put the feet at the top. Do NOT draw: a body, a tail.

FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, navy around deep blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

### 8. N08 đuôi (thân đuôi giữ viền, thùy cuối đổi dáng)

**Kiểm:** đầu to của đuôi ở **bên phải**, đúng chỗ cũ; thân đuôi viền như cũ; quạt cuối chĩa **sang trái**, gốc ở chỗ cũ, to hơn.

```
Image 1 is three pieces of a 2D cut-out animation puppet (the old design): a long tail and two fin lobes at its end. The tail's wide RIGHT end joins the body; it tapers to the left; the two lobes (upper and lower) have their base at their RIGHT end, at the tail tip, and point LEFT, with red tips. Redraw THESE pieces as the tail of image 2 (the approved concept): deep blue on top and cream underneath, a low soft fin along the top, same outline; the two lobes become a big fan of lotus-petal-shaped fin lobes pointing left, pale pink fading to coral pink at the tips.
Do NOT draw: rainbow stripes, a body, legs.

FRAMING: the same square canvas; every piece keeps its place, angle and direction from image 1, so the drawing can be put back on the old puppet. The tail keeps its outline from image 1. The two lobes keep their base where it is; their outline follows image 2: they may be bigger, but stay inside the square with a clear white margin.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (dark rose around coral pink and lotus pink, dark blue around sky blue, navy around deep blue, dark green around leaf green, warm grey-brown around cream, dark red around red), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```
