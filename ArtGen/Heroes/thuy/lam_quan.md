> **BẢN CŨ, không dùng nữa (2026-11-01).** Cách một ảnh cả người đã bị thay bằng cách thay tạo hình trên rig aola: xem `../QUY_TRINH.md` và mẫu `giot_suong_1.md`. File này sẽ được viết lại.

# Lam Quân: Thủy, boss ải 4, Sử thi, 3 dạng

Danh sách, quy tắc chung, sửa nhanh: [../Thuy.md](../Thuy.md). Đường dẫn ảnh trong file này tính từ `ArtGen/Heroes/`.

| Mã ảnh | Tên dạng | Ảnh tham chiếu | Lưu vào |
|---|---|---|---|
| `lam_quan_1` | Lam Quân | `refs/thuy/REF_lam_quan_1.png` | `inbox/HERO_lam_quan_1.png` |
| `lam_quan_2` | Vạn Quân | `refs/thuy/REF_lam_quan_2.png` | `inbox/HERO_lam_quan_2.png` |
| `lam_quan_3` | Hắc Dực Vạn Quân | `refs/thuy/REF_lam_quan_3.png` | `inbox/HERO_lam_quan_3.png` |

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

## `lam_quan_1`: Lam Quân

Đính kèm: `refs/thuy/REF_lam_quan_1.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, BOSS line, stage 1 of 3: a tiny knight cadet.
REF: keep the idea - a small knight in shiny blue armour a bit too big for him, a helmet with a golden crescent crest
and feather plumes, big round eyes, chunky gauntlets and boots.
CHANGE: teal plumes instead of black; he swings a small bronze bell on a rope like a flail instead of the rod; a
short cape cut into wave shapes.
POSE: battle cry with an open mouth, brave and a little clumsy.
```

## `lam_quan_2`: Vạn Quân

Đính kèm: `refs/thuy/REF_lam_quan_2.png`, `inbox/HERO_lam_quan_1.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, BOSS line, stage 2 of 3: the cadet grown into the bell warrior.
REF: keep the idea - a strong warrior in blue and gold plate armour, a helmet with two feather plumes, wielding an
enormous temple bell on a long golden handle like a giant hammer, water streamers around him.
CHANGE: the bell is a bronze East-Asian temple bell with cloud-and-wave relief (not a striped bell); the visor is
open and shows glowing cyan eyes; shoulder guards shaped like breaking waves; teal plumes.
PREVIOUS STAGE: same crescent crest and colours; the wave-cut cape, now longer.
POSE: wide stance, the bell hammer resting on one shoulder.
```

## `lam_quan_3`: Hắc Dực Vạn Quân

Đính kèm: `refs/thuy/REF_lam_quan_3.png`, `inbox/HERO_lam_quan_2.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, BOSS line, stage 3 of 3: the bell warrior's dark-winged form.
REF: keep the idea - the same knight in darker armour with gold trim, a long cape, a horned crest and the great bell
beside him, waves swirling at his feet.
CHANGE: a deep ink-blue cape instead of purple, splitting into two wide fin-like wings like a manta ray; two curved
horns shaped like wave crests; the bell floats at his side wrapped in a chain of flowing water; midnight-blue armour
with gold and teal trim; a light water aura.
PREVIOUS STAGE: same crescent crest, glowing cyan eyes and temple-bell design.
POSE: calm and imposing, one hand open toward the viewer's right.
```
