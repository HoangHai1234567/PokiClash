> **BẢN CŨ, không dùng nữa (2026-11-01).** Cách một ảnh cả người đã bị thay bằng cách thay tạo hình trên rig aola: xem `../QUY_TRINH.md` và mẫu `giot_suong_1.md`. File này sẽ được viết lại.

# Cá Ngựa: Thủy, quái thường, Hiếm, 3 dạng

Danh sách, quy tắc chung, sửa nhanh: [../Thuy.md](../Thuy.md). Đường dẫn ảnh trong file này tính từ `ArtGen/Heroes/`.

| Mã ảnh | Tên dạng | Ảnh tham chiếu | Lưu vào |
|---|---|---|---|
| `ca_ngua_1` | Cá Ngựa Tân Binh | `refs/thuy/REF_ca_ngua_1.png` | `inbox/HERO_ca_ngua_1.png` |
| `ca_ngua_2` | Cá Ngựa Song Đao | `refs/thuy/REF_ca_ngua_2.png` | `inbox/HERO_ca_ngua_2.png` |
| `ca_ngua_3` | Cá Ngựa Tướng Quân | `refs/thuy/REF_ca_ngua_3.png` | `inbox/HERO_ca_ngua_3.png` |

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

## `ca_ngua_1`: Cá Ngựa Tân Binh

Đính kèm: `refs/thuy/REF_ca_ngua_1.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, stage 1 of 3: a baby seahorse soldier.
REF: keep the idea - a small blue seahorse standing on its curled tail, a long trumpet-shaped snout, a curly crest on
its head, one big round eye.
CHANGE: no bomb and no breathing tube; it carries a round wooden shield with a shell emblem; a little helmet made of
a scallop shell; the crest is coral orange; a cream ridged belly.
POSE: a stiff salute like a new recruit.
```

## `ca_ngua_2`: Cá Ngựa Song Đao

Đính kèm: `refs/thuy/REF_ca_ngua_2.png`, `inbox/HERO_ca_ngua_1.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, stage 2 of 3: the seahorse grown into a twin-blade fighter.
REF: keep the idea - a taller seahorse warrior holding two short blades, a strap across the chest, the curled tail.
CHANGE: no mask and no goggles - a teal bandana over the head with two long tails flowing back; the blades are curved
and shaped like branches of white coral; a leather belt with a small shell pouch.
PREVIOUS STAGE: same blue body, cream belly, coral-orange crest and the scallop-shell helmet, now with cheek guards.
POSE: crouched, blades crossed in front.
```

## `ca_ngua_3`: Cá Ngựa Tướng Quân

Đính kèm: `refs/thuy/REF_ca_ngua_3.png`, `inbox/HERO_ca_ngua_2.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, stage 3 of 3: the seahorse grown into an armoured general.
REF: keep the idea - an armoured seahorse swordsman with broad shoulder guards, a long sword on the back, a flowing
crest like a mane, the curled tail.
CHANGE: blue-teal lacquered armour with gold trim instead of red; the scallop helmet becomes a general's helmet with
a tall coral-orange crest; a long curved sword with a wave pattern on its scabbard; a short cape of teal cloth.
PREVIOUS STAGE: same face and snout; the bandana tails now hang from the helmet.
POSE: one hand on the sword hilt, standing tall on the curled tail.
```
