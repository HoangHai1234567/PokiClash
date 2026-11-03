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

## Đảo Thủy 70 ải: sàn đấu theo chặng, mini boss, boss (2026-11-03)

Thay nền `battle_thuy` (một ảnh vẽ bằng code cho cả đảo) bằng bộ nền theo chặng. Gói gửi GPT sinh bằng `build_thuy.py` vào `gui_gpt/thuy/` (file prompt từng lượt, bố cục `bo_cuc_<mã>.png`, `HUONG_DAN.md`); ảnh mẫu địa danh cắt từ bản đồ dài `../Islands/zones/thuy70/zone_thuy70.png` vào `refs/thuy/`. Mục trên (B1–B5, 1024 × 1024) là bộ cũ theo hệ, chưa gen.

| Mã | Nền | Ải | Cảnh |
|---|---|---|---|
| `c01`–`c09` | thường, mỗi chặng một nền | 1–19, 21–29 … 61–69 | Ban ngày, địa danh của chặng nhỏ ở xa bên trái. `c01` chốt nét, mọi lượt sau lấy nó làm ảnh mẫu |
| `m20` | mini boss Ma Kết | 20 | Mỏm hải đăng, hoàng hôn trước bão |
| `m30` | mini boss Vây Lam | 30 | Khe thác bạc buổi sáng sương, hai thác kẹp bệ địch |
| `m40` | mini boss Kuba | 40 | Rạn ngọc lúc chạng vạng, sò khổng lồ ngậm ngọc |
| `m50` | mini boss Thương Lam | 50 | Hồ gương đêm trăng, hai bệ đứng trong nước |
| `m60` | mini boss Huyền Vũ | 60 | Đền rùa cổ lúc chạng vạng, sương hồn xanh |
| `b70a`, `b70b`, `b70c` | boss Lam Quân, Vạn Quân, Hắc Dực | 70 | Đấu trường đá cổ giữa biển, hồ xoáy sau lưng boss; 3 bản cùng bố cục: hoàng hôn bão, bão nổi, đêm bão |
| `fxm`, `fxb` | sheet phần động | 20–60, 70 | Nền trong suốt, lưới 4 × 3 và 3 × 2 |

**Khung:** GPT vẽ 1536 × 1024; game lấy khúc giữa 1192 × 1024 (x 172..1364) thu về khung sân 1080 × 928. Bố cục đặt hai bệ đúng chỗ đứng trong code (`StageView.Pos`: địch (316, 472), phe mình (784, 836) khung 1080), chừa chỗ hai bảng máu (trên phải, dưới trái), chừa thân tướng (cao 300 × 1,18 và 352 px khung).

**Mini boss, boss đầu tư hơn ở:** địa danh gần và to; giờ, thời tiết riêng; bệ địch là bệ nổi có mặt bên (ý từ `be_thuy_boss.png`); phần động riêng. Bố cục khoanh nét đứt hồng chỗ phải để trống cho phần động.

### Phần động (code làm sau khi có ảnh)

| Nền | Phần động | Ảnh | Chuyển động |
|---|---|---|---|
| `c01`–`c09` | bọt, gợn ở mép nước, suối; lấp lánh | `anim_foam`, `anim_ripple`, `anim_sparkle` (có sẵn) | Như phần động bản đồ đảo, vài vật mỗi nền |
| `m20` | tia đèn hải đăng | `fxm` 1 | Quay qua lại quanh đèn, trong suốt một nửa |
| | sóng vỗ đá, bụi nước; mưa | `anim_wave`, `anim_foam`; vệt vẽ bằng code | Bọt bắn theo nhịp; mưa xiên rơi đều |
| `m30` | nước chảy trên hai thác; sương chân thác; cầu vồng | `fxm` 3, 4, 2 | Vệt trượt xuống lặp; sương trôi ngang, mờ dần; cầu vồng hiện rồi tắt chậm |
| `m40` | quầng sáng ngọc; bong bóng; lấp lánh | `fxm` 5, 6, 7, `anim_sparkle` | Quầng phập phồng; bong bóng nổi lên, vỡ |
| `m50` | bóng hai tướng dưới nước; đom đóm; gợn tròn; vệt trăng | lật hình tướng; `fxm` 8, 10, 9 | Bóng lật dọc, mờ, gợn sóng nhẹ; gợn tròn loang khi tướng bị đánh |
| `m60` | vòng phù văn trên bệ địch; cửa đền, mắt tượng sáng; đốm hồn; lá rơi | `fxm` 11, 12, `anim_leaf` | Vòng sáng phập phồng, bừng lên khi boss dùng Tuyệt kỹ; đốm hồn bay lên |
| `b70a`–`c` | xoáy nước; đinh ba | `fxb` 1, 2 | Xoáy bị ép dẹt, quay chậm (dạng 3 quay nhanh); đinh ba nhấp nhô, quầng sáng |
| | sóng cuộn, vòi rồng ở chân trời; mây bão; mưa; sét | `fxb` 6, 5, 4, 3 | Dạng 1 sóng; dạng 2 thêm mưa, vòi rồng, mây trôi; dạng 3 thêm sét kèm chớp màn |

Boss tiến hóa thì đổi nền `b70a` → `b70b` → `b70c` trong lúc chớp trắng của tiến hóa.

### Sau khi có ảnh (đã làm 2026-11-03)

1. Nhắn Claude "duyệt <mã>": `py -3 -I ArtGen/BattleBG/build_thuy.py --duyet <mã>` lưu `thuy/<mã>.png`, vẽ ảnh soi khung `thuy/soi_<mã>.png`, dựng file prompt các lượt đã đủ ảnh mẫu.
2. `py -3 -I ArtGen/BattleBG/build_thuy.py --xuat`: cắt khúc khung game khỏi mỗi nền đã duyệt (`CROP` chung; `CROP_FIX` cho nền mini boss, boss vì mặt bệ nổi thấp hơn), thu về 1080 × 928, lưu `Assets/03 Art/BattleBG/battle_thuy_<khoá>.png` (khoá `c01`..`c09` theo chặng, `s20`..`s70` theo ải, dạng boss sau `s70_2`, `s70_3`); cắt `fxm` thành `BattleBG/Anim/fx_<tên>.png`; ghi phần động và màu trời từng nền vào `BattleBG/Resources/arena_fx.json` (bảng `FX` trong script, toạ độ ảnh GPT). Rồi trong Unity: refresh, menu `PokiClash/Dựng lại danh mục ảnh`; lần đầu thêm menu `PokiClash/Prefab/Sàn đấu: lớp phần động (Screens/Battle)` (dựng lớp `PhanDong` trong prefab màn trận).
3. Code:
   - `StageView.Init(zone, stage)` chọn nền theo ải: `battle_<đảo>_s<ải>`, rồi `battle_<đảo>_c<chặng>`, không có thì `battle_<đảo>`; thử thách huy hiệu và hang dùng nền hệ. Màu trời phần dôi (máy dài) lấy từ json.
   - `ArenaAnim` (lớp ngay trên ảnh nền, dưới tướng) chạy phần động theo json; chiêu và Tuyệt kỹ làm quầng sáng, phù văn, tia đèn bừng lên, xoáy quay nhanh.
   - Boss tiến hóa: `StageView.SetPhase` đổi sang nền `…_s70_2`, `…_s70_3` nếu có (trong lúc chớp trắng).
   - Thử: menu `PokiClash/Thử/Sàn đấu đảo Thủy: chụp nền từng chặng, mini boss, boss (đang Play)`.
4. Đã đủ 19 ảnh (2026-11-03). Boss 70: ba nền dạng 1, 2, 3 đổi theo tiến hóa; sheet `fxb` cắt thành `san_whirlpool`, `san_trident`, `san_bolt`, `san_cloud`, `san_spout`, `san_wave` (dạng 2 thêm mưa, mây bão, vòi rồng; dạng 3 thêm sét). Còn chưa làm: bóng tướng dưới hồ gương (`m50`); nạp nền sàn đấu theo trận (hiện cả 17 nền nằm trong danh mục ảnh, khoảng 7,7 MB, nạp từ lúc mở game).
