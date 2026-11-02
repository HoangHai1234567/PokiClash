> **BẢN CŨ, không dùng nữa (2026-11-01).** Cách một ảnh cả người đã bị thay bằng cách thay tạo hình trên rig aola: xem `../QUY_TRINH.md` và mẫu `giot_suong_1.md`. File này sẽ được viết lại.

# Cánh Cụt: Thủy, quái thường, Thường, 2 dạng

Danh sách, quy tắc chung, sửa nhanh: [../Thuy.md](../Thuy.md). Đường dẫn ảnh trong file này tính từ `ArtGen/Heroes/`.

| Mã ảnh | Tên dạng | Ảnh tham chiếu | Lưu vào |
|---|---|---|---|
| `canh_cut_1` | Cánh Cụt Con | `refs/thuy/REF_canh_cut_1.png` | `inbox/HERO_canh_cut_1.png` |
| `canh_cut_2` | Đầu Bếp Cánh Cụt | `refs/thuy/REF_canh_cut_2.png` | `inbox/HERO_canh_cut_2.png` |

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

## `canh_cut_1`: Cánh Cụt Con

Đính kèm: `refs/thuy/REF_canh_cut_1.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, stage 1 of 2: a baby penguin.
REF: keep the idea - a round baby penguin with a bright blue back, cream face and belly, orange beak and feet, a red
scarf, hugging a fish, a few ice crystals around it.
CHANGE: the scarf is a red-and-white striped knitted scarf with a pompom end; a tuft of three little feathers on top
of the head; it hugs a small silver fish by the tail; pink blush on the cheeks.
POSE: standing proud but a bit shy, flippers around the fish.
```

## `canh_cut_2`: Đầu Bếp Cánh Cụt

Đính kèm: `refs/thuy/REF_canh_cut_2.png`, `inbox/HERO_canh_cut_1.png`, `inbox/HERO_tieu_y_1.png`.

```
Water hero, stage 2 of 2: the penguin grown into a chubby head cook.
REF: keep the idea - a big round penguin cook in a white chef hat and a red scarf, carrying a plate of steaming food
in one flipper.
CHANGE: the plate becomes a steaming bowl of fish noodle soup on a small wooden tray; a ladle in the other flipper;
a cream apron with a blue wave pattern; no small companion at its feet.
PREVIOUS STAGE: keep the striped scarf, the three-feather tuft (poking out from under the chef hat) and the colours.
POSE: chest out, proud smile, offering the bowl.
```
