> **BẢN CŨ, không dùng nữa (2026-11-01).** Cách một ảnh cả người đã bị thay bằng cách thay tạo hình trên rig aola: xem `../QUY_TRINH.md` và mẫu `giot_suong_1.md`. File này sẽ được viết lại.

# Tiểu Y: Thủy, quái thường, Thường, 2 dạng

Danh sách, quy tắc chung, sửa nhanh: [../Thuy.md](../Thuy.md). Đường dẫn ảnh trong file này tính từ `ArtGen/Heroes/`.

| Mã ảnh | Tên dạng | Ảnh tham chiếu | Lưu vào |
|---|---|---|---|
| `tieu_y_1` | Tiểu Y | `refs/thuy/REF_tieu_y_1.png` | `inbox/HERO_tieu_y_1.png` |
| `tieu_y_2` | Y Trạch | `refs/thuy/REF_tieu_y_2.png` | `inbox/HERO_tieu_y_2.png` |

Mở một cuộc trò chuyện mới với GPT cho tướng này: gửi Tin nhắn mở đầu, rồi gen lần lượt từ dạng 1. Dạng sau đính kèm dạng trước đã duyệt. Chỉ dán khối prompt, không đính kèm file này.

## Tin nhắn mở đầu

```
You are drawing the hero roster of a vertical mobile monster-battle game whose whole look is a hand-drawn kid's
adventure notebook. Each hero is an evolution line of 2 or 3 stages and changes its look when it evolves. I will
send one prompt per image, with its attachments. ONE IMAGE PER REPLY, then stop and wait for "next" or a correction.

ATTACHMENTS
- REF (always image 1): a small low-resolution sprite, used only as a rough reference for the creature's idea, body
  plan and pose. Redraw it as a brand-new drawing in our style and apply every listed CHANGE. Do not trace it; do
  not keep its pixel look, its exact colours or its exact costume details.
- PREVIOUS STAGE (from stage 2 on): our approved drawing of the stage before. The new stage must read at a glance as
  the same creature grown up: same eye colour, colour scheme and signature marks, now bigger and stronger.
- STYLE ANCHOR (every image after the first): our first approved hero. Match its line weight, crayon shading,
  colouring and finish exactly.

FRAME (same for every image): 1024 x 1024, fully transparent background, ONE character, full body, centred, nothing
cut by the edges (keep a 4% margin). The feet (or the lowest body part) rest on an invisible ground line 6% above the
bottom edge; a swimming or floating creature hovers just above that line. No ground, no cast shadow, no scenery, no
text, no letters, no numbers, no frame, no card.
VIEW: three-quarter view, body and face turned toward the viewer's RIGHT (mirror the REF if it faces left), idle
battle-ready pose, both eyes visible.
PROPORTIONS by stage: stage 1 = chibi baby, head about 40% of the height, round and soft; stage 2 = head about 33%,
more confident; stage 3 = head about 28%, heroic, a larger silhouette and richer ornaments. Creatures without a
clear head follow the same idea: rounder and softer when young, sleeker and stronger when grown. The final stage of
a BOSS line also gets a light water aura. More presence, never more clutter: big readable shapes, a clear face with
expressive eyes; the silhouette must still read at 120 px.
COLOURS: Water heroes use blue #4A90D9 and teal #3FB8A9 as the main accents, with a few warm accents (gold, coral,
cream) so they never look all blue.
STYLE: hand-drawn storybook cartoon for a vertical mobile game. Bold dark-brown ink outlines (#2B2118), slightly
wobbly like a real pen, colored-pencil and crayon hatching for shading, flat warm colours with light watercolour
washes, subtle paper grain inside the character only, soft light from the top-left. Cheerful, cozy, a little naive,
like a kid's adventure notebook drawn by a professional illustrator. No photorealism, no glossy 3D render, no heavy
gradients.
```

## `tieu_y_1`: Tiểu Y, CHỐT STYLE

Đính kèm: `refs/thuy/REF_tieu_y_1.png`, `../StyleRefs/R1_UI_Cards.png`.

```
Water hero, stage 1 of 2: a small sea kid.
REF: keep the idea - a chibi kid with big spiky white hair, warm tan skin, small blue fin-shaped ears and ribbons of
water swirling around the body.
CHANGE: bright sea-blue eyes; a short blue headband holding the hair up; a sleeveless teal vest with a white wave
pattern and cream knee shorts instead of the dark suit; barefoot; a small wooden toy trident in one hand instead of
the golden weapon.
POSE: crouched and ready to jump, big grin.
```

## `tieu_y_2`: Y Trạch

Đính kèm: `refs/thuy/REF_tieu_y_2.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, stage 2 of 2: the sea kid grown into a young sea lord.
REF: keep the idea - long flowing white hair, warm tan skin, a tall golden trident, and instead of legs the lower
body becomes a spinning column of water.
CHANGE: a confident teenager, no beard; the blue headband becomes a gold circlet with a round blue gem; one
teal-and-gold shoulder guard shaped like a breaking wave and a wave-patterned sash across a bare chest; the
trident's three prongs curl like breaking waves; bubbles and water ribbons around him.
PREVIOUS STAGE: same sea-blue eyes, same fin ears, same white wave pattern.
POSE: trident raised beside him, grinning, hovering on his water column.
```
