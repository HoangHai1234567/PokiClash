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

## Đảo Mộc 70 ải: 8 nền dùng chung, khổ dọc có trời dư (2026-11-05)

Người dùng dặn nền trận đảo Mộc tiết kiệm dung lượng, dùng lại tuỳ nền. Gói gửi GPT sinh bằng `build_moc.py` vào `gui_gpt/moc/` (file prompt từng lượt, bố cục `bo_cuc_<mã>.png`, `HUONG_DAN.md`); ảnh GPT lưu vào `moc/tai_ve/`, bản duyệt `moc/<mã>.png`.

**Dùng lại:** 8 nền thay cho 17 nền của đảo Thủy (ước khoảng 5,6 MB thay cho 11,9 MB, ASTC 6×6 cỡ 1080 × 1528).

| Mã | Nền | Ải dùng | Ghi chú |
|---|---|---|---|
| `c12` | Bờ Rêu + Đồng Hoa Sáng | 1–9 | Chốt nét đảo Mộc; ảnh mẫu là nền Bãi Vỏ Sò đảo Thủy bản cao (`troi/c01.png`) |
| `c34` | Đồi Nấm + Rừng Dây Leo | 10–19 | Bệ là mặt gốc cây cưa |
| `c05` | Hang Nanh Gió | 20 (mini boss Phong Linh), 21–29 | Chiều lộng gió |
| `c06` | Thung Lũng Lá | 30 (mini boss Gió Lốc), 31–39 | Chiều vàng, hồ lá sen |
| `c07` | Vách Vuốt Rồng | 40 (mini boss Long Vuốt), 41–49 | Sáng sương |
| `c08` | Rừng Trúc Ngọc | 50 (mini boss Thỏ Hoàng), 51–59 | Chạng vạng, đèn đá |
| `c09` | Hang Pha Lê Lục | 60 (mini boss Mộc Tinh), 61–69 | Trong cửa hang, pha lê sáng |
| `b70` | Cây Thần Ngàn Năm | 70 (boss Thanh Long, 3 dạng) | Dạng 2, 3: game phủ tối dần, thêm mây bão, mưa, sét |
| `fx` | sheet 3 × 2 | | Lốc lá, cánh hoa, lá trúc, tia nắng, vòng phù văn lá, hạt bồ công anh |

- Chặng có mini boss vẽ một nền có giờ, thời tiết riêng và địa danh to nhưng đủ sáng cho ải thường; bệ địch là bệ nổi thấp có mặt bên cho mọi địch ở chặng đó. Ải mini boss: game phủ màu tối nhẹ, thêm phần động mạnh hơn.
- Phần động dùng lại ảnh có sẵn: `Islands/Anim` (anim_leaf, anim_wind, anim_sparkle), `BattleBG/Anim` (san_firefly, san_wisp, san_glow, san_mist, san_bolt, san_cloud). Sheet `fx` chỉ vẽ món chưa có.

**Khổ:** GPT vẽ dọc 1024 × 1536 một lượt. 880 px dưới (y 656..1536) là khung sân 1080 × 928 thu về bề ngang 1024; phía trên là trời, tán cây dư cho máy dài, nên không cần lượt nối trời như `build_troi.py`. Game lấy y 87..1536 phóng về 1080 × 1528 (`--duyet` ghi sẵn bản này: `moc/cao_<mã>.png`). Hai chỗ đứng, khung thân tướng, bảng máu đổi từ số của `build_thuy.py` sang khổ dọc.

**Ảnh địa danh:** đoạn bản đồ dài đảo Mộc nào đã duyệt (`../Islands/build_zone70_moc.py`) thì `build_moc.py` cắt địa danh trong đoạn đó (`refs/moc/`) và thêm vào file prompt của nền có địa danh ấy. Chưa có thì dùng bản đồ Mộc 8 ải cũ.

**Đã gen, duyệt đủ 9 ảnh (2026-11-05).** Ghi chú duyệt: bệ GPT vẽ to hơn bố cục khoảng 20%, bệ gần cao hơn khoảng 20 px (chân tướng vẫn trên mặt bệ, xuất theo khúc cắt chuẩn); `c05` miệng hang to hơn dặn, nanh phải ở sau nửa trái thân địch (chấp nhận); sheet `fx` có quầng trắng mờ quanh mỗi món, `--xuat` lọc theo màu (giữ nét mực và vùng có màu, cụm tơ bồ công anh giữ nguyên).

**Đưa vào game:**
1. `py -3 -I ArtGen/BattleBG/build_moc.py --xuat [thư_mục_thử]`: lưu `Assets/03 Art/BattleBG/battle_moc_<khoá>.png` cho 8 nền (bản cao 1080 × 1528), cắt sheet `fx` thành `BattleBG/Anim/san_<tên>`, gộp 17 khoá `moc_*` vào `arena_fx.json` (`sky`, `use` cho khoá mượn ảnh, `tint` màu phủ, `fx`). Không xoá khoá đảo khác; `build_thuy.py --xuat` cũng đã sửa để chỉ thay khoá `thuy_*`.
2. Code: `StageView.ArenaArt` coi khoá có `use` trong `arena_fx.json` như có ảnh, `ApplyArena` lấy ảnh theo `use` và phủ `tint` lên ảnh nền (boss dạng 2, 3 là khoá `moc_s70_2`, `moc_s70_3` mượn ảnh `moc_s70`). `ArenaAnim` cho lá rơi, quầng sáng, phù văn, đốm hồn, sương nhận `img` riêng (cánh hoa, lá trúc, tia nắng, vòng phù văn lá, hạt bồ công anh).
3. Unity: refresh, menu `PokiClash/Dựng lại danh mục ảnh`; thử bằng menu chụp sàn đấu.

## Đảo Hỏa 70 ải: 8 nền dùng chung, mỗi nền một giờ riêng (2026-11-05)

Người dùng dặn như đảo Mộc: tiết kiệm dung lượng, dùng lại nếu được, nhưng vẫn độc đáo, khác biệt. Gói sinh bằng `build_hoa.py` (sinh từ `build_moc.py`: cùng khuôn, cùng số đo khung, khác dữ liệu nền, ảnh mẫu và chữ) vào `gui_gpt/hoa/`; ảnh GPT lưu vào `hoa/tai_ve/`, bản duyệt `hoa/<mã>.png`.

| Mã | Nền | Ải dùng | Giờ, thời tiết |
|---|---|---|---|
| `c12` | Bến Đá Đen + Suối Dung Nham | 1–9 | Sáng trong. Chốt nét đảo Hỏa; ảnh mẫu nét là `moc/c12.png`, màu lấy đoạn 1 bản đồ dài đảo Hỏa |
| `c34` | Rừng Than Hồng + Sườn Núi Khói | 10–19 | Chiều hanh hổ phách; bệ là mặt đá dung nham nguội |
| `c05` | Lò Lửa Thiền | 20 (mini boss, đang tạm Hồ Lửa), 21–29 | Chạng vạng xanh, sân đá tu viện |
| `c06` | Chùa Liên Hoa | 30 (mini boss Hồng Liên), 31–39 | Bình minh hồng, hồ dung nham lá sen đá |
| `c07` | Lò Rèn Gai Thép | 40 (mini boss Giáp Long), 41–49 | Trưa u ám xám thép |
| `c08` | Rừng Lửa Ảo | 50 (mini boss Huyễn Viêm), 51–59 | Chạng vạng tím, trăng lưỡi liềm |
| `c09` | Hang Hồng Ngọc | 60 (mini boss Hỏa Tinh), 61–69 | Đêm trăng tròn, ngoài cửa hang (đảo Mộc ở trong hang) |
| `b70` | Miệng Núi Lửa | 70 (boss Lân Hỏa, 3 dạng) | Hoàng hôn đỏ thẫm; dạng 2, 3 game phủ tối đỏ, thêm mây tro, tro rơi, sét |
| `fx` | sheet 3 × 2 | | Vảy tro, bọt dung nham nổ, vòng phù văn lửa, chùm tia lửa, lửa ma tím, cục dung nham bay |

- Tướng Hỏa phần lớn đỏ, cam: mọi file prompt dặn đất đỏ cam dịu (không đỏ rực), mặt bệ sáng (xám tro, kem, đá nhạt).
- Phần động dùng lại: `Islands/Anim` (anim_smoke_big, anim_smoke_small, anim_flame_a, anim_flame_b, anim_embers, anim_sparkle), `BattleBG/Anim` (san_glow, san_mist, san_wisp, san_firefly, san_petal làm cánh sen, san_cloud, san_bolt). `ArenaAnim` chưa có kiểu khói, lửa: thêm khi xuất.
- Ảnh địa danh: cắt từ bản đồ dài đảo Hỏa đã duyệt đủ 3 đoạn, theo chỗ đo tay (`SPOT_FIX` = `SPOTS_REAL` của `../Islands/build_zone70_hoa.py`), vào `refs/hoa/`.
- `--xuat`: như đảo Mộc, khoá `hoa_*` trong `arena_fx.json`. Bảng phần động từng nền (`FX`) để trống, đo trên ảnh đã duyệt rồi điền.
- **Đã duyệt `c12`** (2026-11-05): đất (251, 138, 99) sáng và dịu hơn đất bản đồ (183, 70, 24); bệ xa đúng chỗ code, bệ gần cao hơn khoảng 20 px (chân tướng vẫn trên mặt bệ, như đảo Mộc); cầu gỗ lấn vào sau chân trái tướng địch một chút (chấp nhận). Đã dựng đủ 8 lượt còn lại; chúng chỉ cần `c12` nên gửi theo thứ tự nào cũng được.
- **Đã gen đủ 9 ảnh (2026-11-05).** Đạt: `c34` (gò lỗ phun vẽ rộng tới x 340, lỗ thứ ba sau chân trái tướng địch: khói chỉ đặt ở hai lỗ trái), `c05`, `c06` (một đèn đá sau thân tướng địch, thân tướng che gần hết), `c09`, `fx` (nền trong suốt, đủ 6 món). `b70`: núi lửa nằm hết ở phần trời (máy 20:9 thấy gần đủ, 9:16 chỉ thấy gờ miệng núi lửa, chấp nhận). **Cần sửa** (`sua_<mã>.txt`, bảng `FIXES`): `c07` lò rèn tràn tới x 440 nên đe, thùng, xích nằm sau lưng tướng địch, đất đỏ rực; `c08`, `b70` bệ xa vẽ cao hơn chỗ đứng 75 và 60 px (chân tướng rơi vào mặt bên bệ). Cả ba đã sửa (`<mã>_2.png`, GPT giữ nguyên phần còn lại) và duyệt.
- **Đã xuất (2026-11-05):** 8 nền `battle_hoa_<khoá>.png` (khoá `c01`, `c03`, `c05`..`c09`, `s70`), sheet cắt thành `Anim/san_ash`, `san_firerune`, `san_foxfire`, `san_lavablob`, `san_lavapop`, `san_sparks`, 17 khoá `hoa_*` trong `arena_fx.json` (giữ 34 khoá đảo khác). Phần động (`FX`) không thêm kiểu mới vào `ArenaAnim`: khói là `wisp` với ảnh khói bản đồ đảo, lửa lò là `glow` với `anim_flame_a`, bọt dung nham là `spout`, tro rơi và cánh sen là `leaf`, tàn lửa, tia lửa, lửa ma, cục dung nham là `wisp`. Thử: menu `PokiClash/Thử/Sàn đấu đảo Hỏa: …` (ảnh 470–499).
- **Đã vào game và chụp thử (2026-11-05):** refresh, `Dựng lại danh mục ảnh` (thêm 14 ảnh), tour 15 ải: mọi chặng đúng nền, tướng đứng trên bệ, mini boss có màu phủ, boss có vòng phù văn lửa. Bỏ sương động ở `hoa_c08`, `hoa_s50` (thành cục mây trắng giữa cảnh hồng tím; ảnh đã vẽ sương).
