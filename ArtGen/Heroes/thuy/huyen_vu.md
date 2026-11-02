> **BẢN CŨ, không dùng nữa (2026-11-01).** Cách một ảnh cả người đã bị thay bằng cách thay tạo hình trên rig aola: xem `../QUY_TRINH.md` và mẫu `giot_suong_1.md`. File này sẽ được viết lại.

# Huyền Vũ: Thủy, boss ải 8, Huyền thoại, 3 dạng

Danh sách, quy tắc chung, sửa nhanh: [../Thuy.md](../Thuy.md). Đường dẫn ảnh trong file này tính từ `ArtGen/Heroes/`.

| Mã ảnh | Tên dạng | Ảnh tham chiếu | Lưu vào |
|---|---|---|---|
| `huyen_vu_1` | Rùa Ngọc | `refs/thuy/REF_huyen_vu_1.png` | `inbox/HERO_huyen_vu_1.png` |
| `huyen_vu_2` | Rùa Biển Ngọc | `refs/thuy/REF_huyen_vu_2.png` | `inbox/HERO_huyen_vu_2.png` |
| `huyen_vu_3` | Huyền Vũ | `refs/thuy/REF_huyen_vu_3.png` | `inbox/HERO_huyen_vu_3.png` |

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

## `huyen_vu_1`: Rùa Ngọc

Đính kèm: `refs/thuy/REF_huyen_vu_1.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, BOSS line, stage 1 of 3: a baby crystal turtle.
REF: keep the idea - a baby sea turtle with a domed shell studded with a few crystals, a small golden crown-shaped
crest, big eyes, a pearl floating above its head.
CHANGE: the crystals are teal and white instead of green; a tiny dark-blue baby snake curls around the rim of the
shell, peeking out; the pearl is white with a blue swirl; cream skin with pale blue spots.
POSE: crawling forward, curious.
```

## `huyen_vu_2`: Rùa Biển Ngọc

Đính kèm: `refs/thuy/REF_huyen_vu_2.png`, `inbox/HERO_huyen_vu_1.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, BOSS line, stage 2 of 3: the turtle grown into a great sea turtle.
REF: keep the idea - a large sea turtle on four broad flippers, a shell topped with crystal spikes.
CHANGE: teal and white crystal spikes instead of amber; a carved wave rune on top of the shell instead of the
starfish; the dark-blue snake is now longer, coiled around the shell with its head resting on top; the pearl is now
set in the forehead.
PREVIOUS STAGE: same eyes and skin spots; the crown crest, now bigger.
POSE: low and steady, head raised.
```

## `huyen_vu_3`: Huyền Vũ

Đính kèm: `refs/thuy/REF_huyen_vu_3.png`, `inbox/HERO_huyen_vu_2.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, BOSS line, stage 3 of 3: the ancient tortoise guardian of the North.
REF: keep the idea - an ancient tortoise standing upright, a domed armoured shell, a wise old face with a long white
beard, a big wooden club, a rope belt.
CHANGE: the dark-blue serpent coils around the shell and rests its head on the tortoise's shoulder; the shell is
dark teal with gold rings and wave patterns; the club is a carved wooden oar; the rope belt is navy and white
instead of red; a light water aura.
PREVIOUS STAGE: same eyes, crown crest, forehead pearl and crystal accents.
POSE: standing firm, oar planted, calm and fierce.
```
