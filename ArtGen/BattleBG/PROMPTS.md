# BattleBG: nền trận theo 5 hệ

Nền phần sân đấu của màn trận (spec `battle-presentation`). Sân đấu chiếm phần trên màn: khung 1080 × 928, tỉ lệ khoảng 1,16:1. Ảnh 1024 × 1024 được cắt bớt trên và dưới.

Hai chỗ đứng cố định (xem `G_BattleStage.png`):
- địch: bệ đứng trên-trái, tâm khoảng (30%, 52%);
- phe mình: bệ to hơn dưới-phải, tâm khoảng (75%, 88%).

Tướng là sticker có viền trắng và viền mực, nên nền phải dịu hơn tướng và để trống giữa hai bệ.

## Ảnh đính kèm

| Ảnh | Dùng cho |
|---|---|
| `../Islands/inbox/world.png` | Style và bảng màu của thế giới |
| `../guides/G_BattleStage.png` | Hai vòng hồng là hai bệ đứng; đường xám là chân trời |

## Danh sách ảnh

| ID | File (lưu vào `inbox/`) | Khung | Nền | Vẽ gì |
|---|---|---|---|---|
| B1 | `battle_thuy.png` | 1024 × 1024 | đặc | Đầm phá, sóng, cây dừa — **CHỐT STYLE** |
| B2 | `battle_hoa.png` | 1024 × 1024 | đặc | Đá núi lửa, dung nham xa |
| B3 | `battle_kim.png` | 1024 × 1024 | đặc | Núi thép, chuông đồng xa |
| B4 | `battle_moc.png` | 1024 × 1024 | đặc | Rừng, nấm, hoa |
| B5 | `battle_tho.png` | 1024 × 1024 | đặc | Vách đất vàng, chùa đá xa |

**Thứ tự:** B1 → B2 → B3 → B4 → B5.

## Tin nhắn mở đầu

```
You are painting battle backgrounds for a vertical mobile monster-battle game, same world and style as the attached
world.png (hand-drawn storybook cartoon, dark ink outlines, crayon hatching, watercolour washes, paper grain). Two
fighters (cut-out stickers with white borders) will stand on two round stone or grass platforms exactly where the
pink ellipses are in the attached G_BattleStage.png: a smaller one upper-left (the far enemy) and a larger one
lower-right (the near player). Keep the background calmer and a little lighter than the characters, leave the space
between the two platforms open, horizon around 42 % from the top, sky in the upper part. No characters, no text,
no UI. ONE IMAGE PER REPLY, in order B1 to B5, then wait for "next".
```

## Mẫu prompt (thay [SCENE])

```
1024 x 1024 side three-quarter view battle background. [SCENE]. Two flat round platforms drawn into the ground at
the positions of the attached guide (upper-left smaller, lower-right larger), each with a crayon-hatched rim and a
soft shadow, empty on top. Light from the top-left.
```

| ID | [SCENE] |
|---|---|
| B1 | `A tropical water realm: turquoise lagoon, gentle waves with white foam doodles, small palm trees, coral rocks, a far lighthouse on the horizon, fluffy clouds in a pale blue sky; platforms are sandy islets rimmed with shells` |
| B2 | `A fire realm: dark basalt ground with cracks of glowing lava, a far smoking volcano, ember particles, warm orange-pink dusk sky; platforms are flat black stone discs with glowing seams` |
| B3 | `A metal realm: silver-grey rocky plateau, far iron towers and a huge bronze bell hanging from an arch, gears half buried in the ground, cool pale sky; platforms are riveted steel plates` |
| B4 | `A wood realm: sunny forest clearing, giant round trees in the back, mushrooms and flowers, floating glowing leaves, soft green light; platforms are mossy tree-stump tops` |
| B5 | `An earth realm: golden sandstone mesas, terraced ochre cliffs, a far stone pagoda, desert grass tufts, warm yellow sky; platforms are carved sandstone discs` |

**Sửa nhanh:** `Same scene; calmer and lighter in the middle, platforms exactly at the guide positions, empty on top.`

## Sau khi có ảnh

Claude cắt về tỉ lệ 1,16:1 (bỏ phần trên và dưới), kiểm vị trí hai bệ so với chỗ đứng trong code (`POS` trong `stage.ts`), lưu vào `Assets/03 Art/BattleBG/battle_<hệ>`.
