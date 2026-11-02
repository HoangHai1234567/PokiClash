# Heroes: 40 tướng (8 mỗi hệ)

> **BẢN CŨ, không dùng cho tướng nữa (2026-11-01).** Tướng nay làm theo [QUY_TRINH.md](QUY_TRINH.md): thay tạo hình trên rig aola, nét như hình trận aola. Danh sách và prompt từng hệ viết lại như [Thuy.md](Thuy.md). Phần dưới chỉ còn để tra ý tưởng tạo hình.

> **Đang đổi sang cách mới (người dùng chốt 2026-11-01):**
> - mỗi tướng là một dòng tiến hóa, lên sao thì đổi hình;
> - quái thường lấy dòng có 2–4 dạng, boss lấy dòng có 3 dạng trở lên;
> - mỗi prompt đính ảnh tham chiếu của đúng dạng đó.
>
> **Đảo Thủy đã viết lại ở [Thuy.md](Thuy.md), làm trước.** Ảnh chốt style tướng nay là `inbox/HERO_tieu_y_1.png`, thay TG25. Kim, Mộc, Hỏa, Thổ bên dưới vẫn là bản cũ (một ảnh mỗi tướng, chỉ tả bằng chữ); sẽ chọn lại và viết lại theo cách của Thủy.

Hình tướng cho bản phát hành, thay hình giữ chỗ theo hệ. Mỗi tướng một ảnh cả người trên nền trong suốt. Game dùng một ảnh cho sân đấu, thẻ, sổ tướng, trang trại; phía địch lật ngang.

Mỗi hệ có 8 tướng: 2 Thường, 2 Khá, 2 Hiếm, 1 Sử thi, 1 Huyền thoại. Huyền thoại của Kim, Mộc, Thủy, Hỏa theo Tứ Tượng (Bạch Hổ, Thanh Long, Huyền Vũ, Chu Tước); Huyền thoại hệ Thổ là Đại Sư Cà Sa.

**Mọi tướng là thiết kế mới.** Prompt chỉ tả bằng chữ: loài, dáng, màu, đồ cầm, tính cách. Không đính kèm ảnh chụp game khác, không nhắc tên game nào trong prompt.

## Ảnh đính kèm

| Ảnh | Dùng cho | Khi nào |
|---|---|---|
| `../StyleRefs/R1_UI_Cards.png` | Nét viền, gạch sáp của bản web (style đã duyệt) | Mọi lượt |
| `../UIKit/inbox/UI_Buttons.png` | Nét mực đã chốt ở gói UIKit | Khi đã có |
| `inbox/HERO_tieu_y_1.png` | **Tướng chốt style** (gen đầu tiên, theo [Thuy.md](Thuy.md)) | Mọi lượt |

Mỗi hệ nên mở một cuộc trò chuyện mới với GPT (dán lại Tin nhắn mở đầu, đính kèm ảnh chốt style), để nét không trôi dần sau nhiều ảnh.

## Thứ tự gen

1. **Đảo Thủy theo [Thuy.md](Thuy.md)**, bắt đầu bằng `tieu_y_1` (chốt style tướng). Các hệ dưới đây chờ viết lại; nếu vẫn muốn gen bản cũ thì làm theo đợt 2–5.
2. Đợt 1, 8 tướng Thường: TG01, TG02, TG09, TG10, TG25, TG26, TG33, TG34.
3. Đợt 2, 8 tướng Khá.
4. Đợt 3, 8 tướng Hiếm.
5. Đợt 4, 4 Sử thi và 4 Huyền thoại.

## Danh sách ảnh

Mọi ảnh 1024 × 1024, nền trong suốt, lưu vào `inbox/` đúng tên file.

| ID | File | Tướng | Hệ | Độ hiếm |
|---|---|---|---|---|
| TG01 | `HERO_bu_long.png` | Bu Lông | Kim | Thường |
| TG02 | `HERO_phao_hop.png` | Pháo Hộp | Kim | Thường |
| TG03 | `HERO_kiem_linh.png` | Kiếm Linh | Kim | Khá |
| TG04 | `HERO_meo_quyen.png` | Mèo Quyền Sắt | Kim | Khá |
| TG05 | `HERO_bo_cap.png` | Bọ Cạp Đồng | Kim | Hiếm |
| TG06 | `HERO_bo_ngua.png` | Bọ Ngựa Liềm Thép | Kim | Hiếm |
| TG07 | `HERO_soi_linh.png` | Sói Linh Thép | Kim | Sử thi |
| TG08 | `HERO_bach_ho.png` | Bạch Hổ | Kim | Huyền thoại |
| TG09 | `HERO_mam_go.png` | Mầm Gỗ | Mộc | Thường |
| TG10 | `HERO_nu_hoa.png` | Nụ Hoa | Mộc | Thường |
| TG11 | `HERO_kien_binh.png` | Kiến Binh | Mộc | Khá |
| TG12 | `HERO_banh_tet.png` | Hiệp Sĩ Bánh Tét | Mộc | Khá |
| TG13 | `HERO_de_hoa.png` | Dê Hoa | Mộc | Hiếm |
| TG14 | `HERO_giac_long.png` | Giác Long Gỗ | Mộc | Hiếm |
| TG15 | `HERO_phong_linh.png` | Phong Linh | Mộc | Sử thi |
| TG16 | `HERO_thanh_long.png` | Thanh Long | Mộc | Huyền thoại |
| TG17–TG24 | | **Thủy: thay bằng [Thuy.md](Thuy.md)** (8 dòng, 21 ảnh) | Thủy | |
| TG25 | `HERO_heo_lua.png` | Heo Lửa | Hỏa | Thường |
| TG26 | `HERO_dom_lua.png` | Đốm Lửa | Hỏa | Thường |
| TG27 | `HERO_phao_tet.png` | Pháo Tết | Hỏa | Khá |
| TG28 | `HERO_su_tu_lua.png` | Sư Tử Lửa | Hỏa | Khá |
| TG29 | `HERO_bo_de.png` | Võ Tăng Bồ Đề | Hỏa | Hiếm |
| TG30 | `HERO_ho_lua.png` | Hồ Lửa | Hỏa | Hiếm |
| TG31 | `HERO_phap_luan.png` | Thiền Sư Pháp Luân | Hỏa | Sử thi |
| TG32 | `HERO_chu_tuoc.png` | Chu Tước | Hỏa | Huyền thoại |
| TG33 | `HERO_vo_su.png` | Võ Sư | Thổ | Thường |
| TG34 | `HERO_gau_mo.png` | Gấu Thợ Mỏ | Thổ | Thường |
| TG35 | `HERO_soc_da.png` | Sóc Đá | Thổ | Khá |
| TG36 | `HERO_bo_hung.png` | Bọ Hung Cát | Thổ | Khá |
| TG37 | `HERO_thach_nhan.png` | Thạch Nhân | Thổ | Hiếm |
| TG38 | `HERO_sa_than.png` | Sa Thần | Thổ | Hiếm |
| TG39 | `HERO_ky_lan.png` | Kỳ Lân Cát | Thổ | Sử thi |
| TG40 | `HERO_ca_sa.png` | Đại Sư Cà Sa | Thổ | Huyền thoại |

## Tin nhắn mở đầu

```
You are drawing the hero roster of a vertical mobile monster-battle game whose whole look is a hand-drawn kid's
adventure notebook. The attached PROMPTS.md lists 40 heroes (TG01-TG40), each with its own English prompt. I will
name the hero to draw. ONE IMAGE PER REPLY, then stop and wait for "next" or a correction.
Every hero is an ORIGINAL character: do not copy or imitate any existing game, cartoon or anime character.
FRAME (same for all 40): 1024 x 1024, fully transparent background, ONE character, full body, centred, nothing cut
by the edges (keep a 4% margin). The feet (or the lowest body part) rest on an invisible ground line 6% above the
bottom edge. No ground, no cast shadow, no scenery, no text, no letters, no frame, no card.
VIEW: three-quarter view, body and face turned toward the viewer's RIGHT, idle battle-ready pose, both eyes visible.
PROPORTIONS by rarity: Common and Uncommon = chibi, head about 40% of the height, round and soft; Rare = head about
33%; Epic and Legendary = head about 28%, heroic but still cute, a larger silhouette, richer ornaments and a light
aura in the element colour. Higher rarity means more presence, never more clutter: big readable shapes, a clear
face with large expressive eyes; the silhouette must still read at 120 px.
ELEMENT COLOURS (main accent): Metal = silver #B8C4CF with steel blue; Wood = green #6CBF4F; Water = blue #4A90D9
with teal #3FB8A9; Fire = red #E8553F with orange #F39A2D; Earth = gold-ochre #E2A93B with warm brown.
STYLE: hand-drawn storybook cartoon for a vertical mobile game. Bold dark-brown ink outlines (#2B2118), slightly
wobbly like a real pen, colored-pencil and crayon hatching for shading, flat warm colours with light watercolour
washes, subtle paper grain inside the character only, soft light from the top-left. Cheerful, cozy, a little naive,
like a kid's adventure notebook drawn by a professional illustrator. No photorealism, no glossy 3D render, no heavy
gradients.
From the second hero on, match the line weight, colouring and proportions of the attached approved hero exactly.
```

## Kim (Metal)

### TG01 — Bu Lông, Thường (`inbox/HERO_bu_long.png`)

```
Metal, Common. A tiny round toy robot the size of a teapot: an egg-shaped steel-blue body with a cream belly plate,
stubby arms ending in round clamp hands, short legs with rubber feet, big round headphones with small antenna nubs,
a visor face with two large friendly glowing cyan eyes, one big bolt on top of its head like a tuft of hair. Curious
and eager, one hand raised to wave.
```

### TG02 — Pháo Hộp, Thường (`inbox/HERO_phao_hop.png`)

```
Metal, Common. A small boxy robot built like a battered orange toolbox riding on two short caterpillar treads: a
square face screen with two big round eyes and a toothy grin, a carrying handle on top like a hat, rivets and a
few dents, two chunky arms that end in little round cannon barrels with silver rings, a tiny exhaust pipe puffing a
curl of smoke. Mischievous, arms raised ready to fire.
```

### TG03 — Kiếm Linh, Khá (`inbox/HERO_kiem_linh.png`)

```
Metal, Uncommon. A living sword spirit floating upright, point down: a broad silver blade with a pale-blue glowing
groove, a golden cross-guard shaped like two small wings, a round blue gem in the pommel. On the cross-guard sits a
small round face with big determined eyes; two ribbon-like steel tassels act as arms. Instead of feet, the tip
hovers just above the ground line over a small swirl of wind. Proud and brave.
```

### TG04 — Mèo Quyền Sắt, Khá (`inbox/HERO_meo_quyen.png`)

```
Metal, Uncommon. A small cat in a cosy mech suit: a yellow-and-white helmet with pointed cat ears and a green gem
on the forehead, a round white face with big blue eyes peeking through the open visor, a navy chest plate, short
legs in armoured boots, and two HUGE white robot boxing fists, each bigger than its head, with little yellow speed
sparks around them. Boxer stance, puffed-up and brave.
```

### TG05 — Bọ Cạp Đồng, Hiếm (`inbox/HERO_bo_cap.png`)

```
Metal, Rare. A mechanical scorpion of red-bronze armour plates with teal glass joints, low and wide on six pointed
legs, two big pincers raised, a segmented tail curling high over its back and ending in a crystal stinger, a small
domed head with two glowing green eyes and a confident smirk, a little desert dust at its feet. Guarding, ready to
strike.
```

### TG06 — Bọ Ngựa Liềm Thép, Hiếm (`inbox/HERO_bo_ngua.png`)

```
Metal, Rare. A slim mechanical praying mantis standing upright: steel-blue armour with white trim, two great
crescent scythe blades as forearms raised in a swordsman's guard, a triangular head with large round red eyes and
two short antennae, thin jointed legs, folded translucent wing plates on its back. Cool and focused, like a duelist.
```

### TG07 — Sói Linh Thép, Sử thi (`inbox/HERO_soi_linh.png`)

```
Metal, Epic. A sleek armoured wolf in a low prowling stance: a body of steel-blue plates edged with gold, a golden
face mask with a sharp visor, claws like silver blades, glowing ice-blue eyes, and a mane and long tail made of cold
blue spirit flame flowing backward. Proud and fierce, still a little cute. Light silver-blue aura.
```

### TG08 — Bạch Hổ, Huyền thoại (`inbox/HERO_bach_ho.png`)

```
Metal, Legendary. The White Tiger guardian of the West: a large white tiger with charcoal-grey stripes, ornate
silver-and-gold armour plates on its shoulders, forelegs and forehead, a crown-like crest of small silver blades, a
long tail ending in a crescent of light, crystal claws. Majestic stance, one front paw raised, calm fierce eyes.
Silver-white wind streaks curl behind it.
```

## Mộc (Wood)

### TG09 — Mầm Gỗ, Thường (`inbox/HERO_mam_go.png`)

```
Wood, Common. A tiny wooden sprite: a smooth acorn-brown bulb body with a face, two big green leaves sprouting from
the top of its head, little twig arms, stubby root feet, a thin vine wrapped around its belly like a belt, rosy
cheeks and big shy eyes. It holds a small glowing seed with both hands.
```

### TG10 — Nụ Hoa, Thường (`inbox/HERO_nu_hoa.png`)

```
Wood, Common. A round flower-bud creature: a soft ball of curly coral-orange petals forms its head and body, a pale
cream face with big happy curved eyes and a small smile, two little leaf hands, tiny leaf feet, a short green stem
tail ending in a curled tendril. Bouncy and cheerful, mid-hop.
```

### TG11 — Kiến Binh, Khá (`inbox/HERO_kien_binh.png`)

```
Wood, Uncommon. A little soldier ant standing upright: a glossy dark-green body in three round segments, a round
silver knight helmet with a red plume and two antennae poking out, four small arms (two hold a long wooden spear
with a leaf-shaped blade, two rest on its hips), a leaf shield strapped on its back. Proud guard pose, chin up.
```

### TG12 — Hiệp Sĩ Bánh Tét, Khá (`inbox/HERO_banh_tet.png`)

```
Wood, Uncommon. A little hero shaped like a Vietnamese leaf-wrapped rice cake: a short cylinder body wrapped in
glossy green banana leaves and tied with thin bamboo strings, a dark-green leaf hood and cape, a black hero mask
over big brave eyes, stubby arms holding a short bamboo staff, tiny feet. One loose leaf end flutters like a scarf.
Heroic pose. No letters anywhere.
```

### TG13 — Dê Hoa, Hiếm (`inbox/HERO_de_hoa.png`)

```
Wood, Rare. A graceful ram standing on four legs: a fluffy fleece made of soft pale-green leaves and moss, white
legs with small gold hoof cuffs, two big curled horns of polished wood, a crown of pink flowers between the horns,
a small gold bell on its chest, a gentle smile and big kind eyes. A few petals drift around it.
```

### TG14 — Giác Long Gỗ, Hiếm (`inbox/HERO_giac_long.png`)

```
Wood, Rare. A sturdy four-legged horned dragon-beast, like a small rhino-dragon: a thick body of lime and moss-green
scales, a big curved horn of dark bark on its nose and two smaller horns behind, bark armour plates along its back
with a few fresh leaves sprouting, a short thick tail with a leaf tip, strong claws. Head low, ready to charge,
determined eyes.
```

### TG15 — Phong Linh, Sử thi (`inbox/HERO_phong_linh.png`)

```
Wood, Epic. A tall forest spirit general: a slender figure in a long skirt of layered green leaves, a pale-green
face with a golden leaf-shaped mask over the eyes, long hair of leaves, small orange blossoms at the hips, swirls of
green wind around her open hands. Behind her floats a large ring of woven vines and wood like a halo. Serene and
powerful. Light green aura.
```

### TG16 — Thanh Long, Huyền thoại (`inbox/HERO_thanh_long.png`)

```
Wood, Legendary. The Azure Dragon guardian of the East: a strong green dragon standing on its hind legs, emerald
scales with a jade-white belly, two big wings with dark-green membranes, golden horns and claws, a teal gem on its
forehead and chest, a mane of leaf-shaped fins, a ring of spinning green leaves around its waist. Powerful and
proud, slightly smiling, wings half open.
```

## Thủy (Water)

Đã viết lại theo dòng tiến hóa: xem [Thuy.md](Thuy.md) (8 dòng, 21 ảnh, có ảnh tham chiếu).

## Hỏa (Fire)

### TG25 — Heo Lửa, Thường (`inbox/HERO_heo_lua.png`)

```
Fire, Common. A round little wild piglet: a dark reddish-brown bristly body, a short mane of flame running from its
head down its back in red, orange and yellow, a big pink snout, two tiny tusks, bright teal eyes with a stubborn
frown, short legs pawing the ground ready to charge, a curly tail with a spark on the tip.
```

### TG26 — Đốm Lửa, Thường (`inbox/HERO_dom_lua.png`)

```
Fire, Common. A cheerful fire spirit shaped like a plump drop of flame: a glowing yellow-orange body, a big happy
open-mouthed smile and curved closed eyes, a curling flame tuft on top, two tiny flame hands, a swirl of red flame
around its base like a skirt, a few sparks floating around. Warm and bouncy.
```

### TG27 — Pháo Tết, Khá (`inbox/HERO_phao_tet.png`)

```
Fire, Uncommon. A trio of little red firecracker creatures bundled together: three red paper tubes with gold bands
and gold swirl patterns standing side by side, each with its own funny face (one grinning, one shouting, one
sleepy), stubby arms and feet, their fuses braided together on top into one wick with a sparkling star at the tip.
A few gold confetti stars around. No letters or characters on the paper.
```

### TG28 — Sư Tử Lửa, Khá (`inbox/HERO_su_tu_lua.png`)

```
Fire, Uncommon. A young lion cub with a big fluffy mane made of flames (yellow near the face, red at the tips),
bright red-orange fur, a cream muzzle and belly, big golden eyes, a tail tipped with a flame tuft. It sits up on its
hind legs with its chest puffed out, trying hard to look scary. Little embers float around.
```

### TG29 — Võ Tăng Bồ Đề, Hiếm (`inbox/HERO_bo_de.png`)

```
Fire, Rare. A young warrior monk: shaved head, a saffron-red blindfold whose two long ends flutter upward like tall
flame-shaped ribbons, an orange monk robe with a plum-red sash, cream cloth wraps on the forearms and shins, a chain
of large brown prayer beads across the shoulders, straw sandals. Behind his shoulders spread two big wings shaped
like bodhi leaves made of red and golden flame. He hovers just above the ground in a calm fighting stance.
```

### TG30 — Hồ Lửa, Hiếm (`inbox/HERO_ho_lua.png`)

```
Fire, Rare. A sleek fire fox on four legs: golden-orange fur that turns into flame at the edges, three long flaming
tails curling behind it, a cream chest, dark socks with smoky wisps, ears tipped with flame, sharp amber eyes and a
sly grin. One front paw raised mid-step.
```

### TG31 — Thiền Sư Pháp Luân, Sử thi (`inbox/HERO_phap_luan.png`)

```
Fire, Epic. A tall serene zen master monk: shaved head, a golden lotus crown with flame-like points, wide flowing
orange robes with plum-red outer layers and gold cloud trims, cream sleeves and leg wraps, sandals. One hand raised
in a calm gesture, the other guiding a large golden dharma wheel wreathed in flames that floats beside him; a few
golden sutra plates float around him; long robe ribbons flutter. Light orange aura.
```

### TG32 — Chu Tước, Huyền thoại (`inbox/HERO_chu_tuoc.png`)

```
Fire, Legendary. The Vermilion Bird guardian of the South: a majestic phoenix with a slender neck, crimson and
orange feathers, a golden crest of flame plumes on its head, huge half-raised wings whose feathers turn into flame at
the tips, long flowing tail plumes in red, gold and a touch of violet, golden talons. Standing proudly, embers
drifting upward.
```

## Thổ (Earth)

### TG33 — Võ Sư, Thường (`inbox/HERO_vo_su.png`)

```
Earth, Common. A chibi boy monk boxer: a shaved round head, a plum-red headband with three wooden prayer beads on
the front whose two long tails stand straight up behind his head like tall pointed ears, a big confident grin, an
orange monk outfit with a plum-red sash, a string of wooden beads around the neck, cream cloth wraps on the hands
and shins. Boxing guard, fists up in front of the chest, knees bent, left foot forward.
```

### TG34 — Gấu Thợ Mỏ, Thường (`inbox/HERO_gau_mo.png`)

```
Earth, Common. A little brown bear cub miner: a yellow hard hat with a small lamp, round ears poking out, a tan
muzzle, determined eyes, a blue work vest with pockets, a tool belt, dusty boots, holding a big pointed steel hand
drill like a lance. Ready to dig.
```

### TG35 — Sóc Đá, Khá (`inbox/HERO_soc_da.png`)

```
Earth, Uncommon. A chubby ground squirrel: a big round body with soft brown fur, a fluffy cream ruff on its chest
like a scarf, a big striped tail curled up behind, a little orange stone helmet with a diamond-shaped gem, small red
shorts, two big front teeth, cheeks stuffed with pebbles, a cheeky look. Arms crossed.
```

### TG36 — Bọ Hung Cát, Khá (`inbox/HERO_bo_hung.png`)

```
Earth, Uncommon. A round scarab beetle on six legs: a glossy deep-purple dome shell with a gold rim, a head striped
in gold and blue like a little royal headdress, two antennae with curled tips, big cute eyes. It pushes a ball of
golden sand in front of it; little puffs of sand behind.
```

### TG37 — Thạch Nhân, Hiếm (`inbox/HERO_thach_nhan.png`)

```
Earth, Rare. A big chunky rock golem: a body of stacked grey-brown boulders with moss and tiny ferns on the
shoulders, huge stone fists, short thick legs, two glowing orange eyes under a heavy brow, a crack across the chest
glowing faintly gold, a few pebbles orbiting it. Slow but unstoppable stance.
```

### TG38 — Sa Thần, Hiếm (`inbox/HERO_sa_than.png`)

```
Earth, Rare. A tall jackal-headed desert guardian: black fur, long upright ears with gold rings, a gold-and-blue
striped collar and arm bands, a white linen kilt with a gold belt, a tall staff topped with a gold hook. Amber eyes,
calm watchful stance, a small swirl of sand at the feet.
```

### TG39 — Kỳ Lân Cát, Sử thi (`inbox/HERO_ky_lan.png`)

```
Earth, Epic. A sand qilin: a deer-like body with golden-ochre scales and cream stripes, sturdy hooves, two great
curled horns, a regal face with a short beard and kind eyes, a flowing mane and tail of golden sand-flame. Small sand
spirals and floating stones around it. One front hoof raised proudly. Light golden aura.
```

### TG40 — Đại Sư Cà Sa, Huyền thoại (`inbox/HERO_ca_sa.png`)

```
Earth, Legendary. A great master monk in his prime: shaved head, a golden diadem, a short black goatee and sharp
kind eyes, a huge plum-red patchwork kasaya robe with gold borders over orange monk clothes, a big string of wooden
prayer beads, cream hand and leg wraps, sandals. He holds a tall golden monk's staff with jingling rings on top and
thrusts his other palm forward. A halo of golden flame and dust swirls behind him.
```

## Sửa nhanh (dùng cho mọi tướng)

- **Rối, nhiều chi tiết:** `Same hero; simpler big shapes, fewer small details, thicker outlines, must read at 120 px.`
- **Sai hướng:** `Same hero, mirrored: body and face turned toward the viewer's right.`
- **Có nền hoặc bóng:** `Same image on a fully transparent background: no ground, no shadow, no scenery.`
- **Lệch style:** `Match the line weight, crayon shading and proportions of the attached approved hero exactly.`
- **Bóng, giống 3D:** `Flat hand-drawn colouring with crayon hatching; no glossy highlights, no 3D render look.`
- **Bị cắt mép:** `Same hero, smaller in the frame: whole body inside with a 4% margin, feet on the ground line.`

## Sau khi có ảnh

Claude cắt nền còn sót, đặt chân lên cùng một đường đất (6 % từ đáy, khớp `HeroArt.FootY`), lưu vào `Assets/03 Art/Heroes/hero_<id>.png`. Game hiện hình này thay hình giữ chỗ ở sân đấu, thẻ, sổ tướng và trang trại.

Danh sách tướng và các việc dữ liệu đi kèm: `GD_Claude/13_DanhSachTuong.md`. **Không đính kèm file đó cho GPT.**
