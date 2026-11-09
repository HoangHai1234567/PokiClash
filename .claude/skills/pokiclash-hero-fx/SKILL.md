---
name: pokiclash-hero-fx
description: >
  Cải tiến hiệu ứng idle, đánh nhau và animation của tướng PokiClash: khựng lúc trúng (hit-stop), rung, bật lùi, chớp màu,
  hạt có vật lý (tia văng, mảnh vỡ, bụi, than, khói, hạt tụ lực), biên đạo đòn theo pha, idle "sống" theo hệ, hạt trong
  .atomik (beast.py) và hạt trên sân (StageView, pool Image hoặc ParticleSystem qua UIParticle). Học từ pixelfx (MIT), các
  skill VFX Unity và bộ GameFeel. Dùng khi làm cho tướng đánh "có lực" hơn, thêm hạt, sửa idle đứng im, chỉnh nhịp đòn, chiêu.
---

# Hiệu ứng và cảm giác đánh của tướng (2026-11-09)

Skill này nói **làm sao cho tướng đánh có lực, đứng có hồn**. Luật hình, tia chiêu mana, gói vẽ ảnh hiệu ứng nằm ở skill
`pokiclash-vfx`; rig, clip .atomik nằm ở skill `pokiclash-spine-rig` (mục 13, 15, 16). Đọc hai skill đó trước, skill này chỉ thêm
phần cảm giác.

## 0. Luật không được phá

- **Hình:** vẽ tay, viền mực nâu `#2B2118`, tô phẳng chì sáp. **Không glow, không additive, không bloom, không gradient.** Mọi
  công thức "ánh sáng" học từ nơi khác phải đổi thành **hình phẳng, màu phẳng, alpha** (mục 2).
- **Engine:** hiệu ứng trận là ảnh rời trên uGUI canvas, chạy theo **đồng hồ sân** `StageView.Clock`, không theo
  `Time.deltaTime`. Dự án **chưa dùng ParticleSystem**; thêm ParticleSystem hay gói UIParticle phải hỏi người dùng trước (mục 9).
- **Code runtime:** `PrefabOnlyTests` cấm `new GameObject`, `AddComponent`, `new Material`, `new Texture2D`, `Sprite.Create`,
  `Ui.Rect/Img` trong mã chạy (trừ `AolaActor.cs`, `AolaSticker.cs`). Hạt mới: prefab dựng bằng menu editor, sinh bằng `Ui.Spawn`,
  giữ trong pool, bật tắt bằng SetActive, nhuộm bằng `Image.color`.
- **Hiệu ứng không che con bị trúng:** vụ nổ trúng nhỏ hơn thân nó. Hiệu ứng lửa, lá, nước phẳng thì to bằng **khoảng nửa** cỡ
  hiệu ứng có glow tương đương và tô nhạt (ghi nhớ "flat-fx-sizing").
- **Ảnh mới không trùng tên ảnh Fallback** (`fx_glow`...), không thì thư viện ảnh tráo vào mọi prefab.
- Tướng vẽ lại phải có **chuyển động phụ**: mây, vòng, đồ bay, tai, đuôi, lửa không được đứng im (ghi nhớ "hero-secondary-motion").
- Người dùng chấm trên **điện thoại Android** (bản Build thường): soi trong editor xong vẫn phải thử trên máy.

## 1. Nguồn đã đọc và lấy gì

| Nguồn | Ở đâu | Lấy gì |
|---|---|---|
| **pixelfx** (patch-gg, MIT; lõi hạt chuyển từ Sprite Fusion của Hugo Duprez, lõi diễn chuyển từ Hollow Crown, đều MIT) | `E:\ProjectAtomik\_ref\pixelfx` (máy ổ D: `D:\_ref\pixelfx`). `src/core/sim.js` (hạt), `src/core/act.js` (diễn), `src/fx/moves/*.js` (đòn trọn vẹn), `docs/AUTHORING.md` (thước đo) | cách diễn quanh hiệu ứng (lấy đà, khựng, rung, con bị đánh bật lò xo), 12 kiểu hạt có vật lý, biên đạo theo pha. **Không lấy hình**: toàn pixel art có lớp sáng cộng dồn |
| Skill `game-feel` (gamedev-skills/awesome-gamedev-agent-skills, Apache-2.0) | github | bảng mức đòn (rung kiểu trauma, khựng, số hạt), 5–8 phản hồi nhỏ trong ~100 ms |
| Skill `scenario-unity-vfx` (scenario-labs/skills, MIT) | github | nhịp từng lớp hiệu ứng, ngân sách hạt điện thoại, đo overdraw thay vì đếm hạt. Bỏ phần "additive glow" |
| ParticleEffectForUGUI / UIParticle (mob-sakai, MIT, v4.14.2) | github | cách cho ParticleSystem vẽ trong canvas (mục 9) |
| Bộ GameFeel của người dùng | `E:\ProjectAtomik\GameFeel\game-feel-guide.md` mục 4–5, `FeedbackKit/` | thời lượng, easing, squash, flash, hitstop "chậm 90% thay vì đứng hẳn", không cộng dồn |
| Celeste (mã nguồn), Sakurai (hitstop), Eiserloh GDC 2016 (rung kiểu trauma), LoL VFX style guide | xem mục 12 | số cụ thể cho khựng, squash, rung |

## 2. Đổi "ánh sáng" sang luật vẽ tay

pixelfx dựng sức mạnh bằng ánh sáng (lõi trắng nóng, quầng, ánh lên sàn). Game mình làm bằng **hình và nhịp**:

| pixelfx làm | Mình làm |
|---|---|
| khung "hero" trắng 1–2 khung lúc nổ | **hình nổ phẳng màu kem `#F4EEDC` hoặc vàng nhạt có viền mực**, 1–2 khung (0,03–0,06 s), rồi đổi sang hình nổ thường |
| quầng sáng quanh tia, ánh lên sàn | **vòng phẳng mỏng có viền** nở ra rồi tan; vệt bóng màu đậm của hệ trên sàn (alpha 0,3–0,5), không phát sáng |
| tia lửa sáng có đuôi | **vệt kéo dài theo vận tốc** (sprite thuôn có viền mực, co giãn theo tốc độ), 2 màu phẳng: đầu nhạt, đuôi đậm |
| khói, hơi mờ trong suốt | cụm tròn tô phẳng màu khói, **alpha phẳng 0,4–0,7**, nở to và nhạt dần (được: chỉ đổi alpha, không gradient) |
| lửa nguội dần theo dải màu | 3–4 **hình rời** theo dải màu phẳng (vàng → cam → đỏ → khói), đổi hình theo tuổi hạt |
| "lines and light, not fills" | **đường và hình nhỏ, không mảng lớn**: vệt, vòng, mảnh, chấm có viền; tránh khối màu bão hoà to che người |

## 3. Chọn tầng làm

| Hiệu ứng gắn với... | Làm ở | Vì sao |
|---|---|---|
| dáng, nhịp clip của chính tướng (cầu tụ ở miệng, vệt cào, vòng tụ lực, than bay ở bờm, nổ ở chỗ đối thủ qua xương `far`) | **.atomik** (`ArtGen/Spine/beast.py`, slot hiệu ứng) | vẽ vào ảnh sticker nên hiện ở mọi màn: trận, hộp chi tiết, đội hình; khớp khung tuyệt đối |
| trạng thái trận (trúng đòn, chí mạng, khựng, rung, bật lùi, bụi chân trên sân, số sát thương) | **StageView** (runtime) | biết ai đánh ai, mạnh bao nhiêu; chạy theo đồng hồ sân |
| nhiều hạt nhỏ có vật lý lúc chạy (tia văng, mảnh, than) | **pool Image trên sân** (mặc định, theo mẫu `MachineFx`), hoặc **ParticleSystem + UIParticle** nếu người dùng đồng ý | xem mục 9 |

Đừng đặt ParticleSystem vào thế giới riêng của tướng (camera sticker ở x=10000): shader viền sticker sẽ viền luôn hạt, và camera
chỉ vẽ lại khi hình đổi.

## 4. Một cú đánh có lực: bảng theo mức

Mỗi cú trúng = **5–8 phản hồi nhỏ cùng lúc** trong ~100 ms: khựng, rung, con bị đánh bật lùi và chớp, hạt văng, chữ số, tiếng.
Thời gian ở bảng là **giây thật**; sân chạy 1,3× lúc đánh thường, 1× lúc chiêu, nên quy đổi trước khi đặt vào clip.

| Mức | Dùng cho | Khựng (hit-stop) | Rung (trauma 0–1) | Bật lùi | Chớp | Hạt |
|---|---|---|---|---|---|---|
| nhẹ | đòn thường của lính, đòn hụt sức | 0–0,03 s | 0,15 | 0,04 H | 0,05 s | 0–4 |
| vừa | đòn thường của tướng | 0,05–0,08 s | 0,35 | 0,08 H | 0,06–0,08 s | 6–12 |
| nặng | chí mạng, đòn nện, đòn lao | 0,10–0,14 s | 0,6 | 0,12 H | 0,08 s + hình nổ kem 1 khung | 15–25 |
| tuyệt kỹ | chiêu cuối, boss | 0,14–0,20 s | 0,8 | 0,15 H | 0,1 s + hình nổ kem 2 khung | 20–40 |

(H = chiều cao con bị đánh.) Số lấy từ pixelfx (`stop` 0,02–0,2 s, `shake` 0,06–0,38 s), skill game-feel, Celeste (`Freeze(.05)`
khi lướt, `.1` khi nổ) và Smash (khựng cả hai con, tối đa ~0,3–0,5 s; game mình nhẹ hơn nhiều).

- **Khựng:** dừng **cả hai con và hiệu ứng của cú đó**, không dừng UI. Không cộng dồn: lấy `max(còn lại, mới)`. Hai cú liền nhau
  trong 0,2 s thì cú sau khựng một nửa. Có thể dùng "chậm 90%" (dt × 0,1) thay vì đứng hẳn cho đòn vừa (GameFeel). Sakurai: con
  bị đánh rung ngang tại chỗ trong lúc khựng mạnh hơn con đánh, rung giảm dần.
- **Rung kiểu trauma (Eiserloh):** `trauma += mức` (chặn ở 1), giảm 1,2–1,5 mỗi giây; độ lệch = `tối đa × trauma²`, tối đa khoảng
  12 × 8 đơn vị sân (khung 1080 rộng); hướng lệch lấy từ noise mượt (sin lệch tần số 1,7 / 2,3), **không random mỗi khung**. Đòn có
  hướng thì đẩy màn 4–6 đơn vị theo hướng đánh, hồi ×0,85 mỗi khung (camera bump) thay cho rung ngẫu nhiên. Rung nhẹ không cắt rung
  mạnh đang chạy.
- **Bật lùi:** đẩy con bị đánh ra xa phía kẻ đánh trong 0,06 s (ease-out), về chỗ trong 0,25–0,35 s, vượt nhẹ 5–10%. Nghiêng lò xo
  như bia rơm pixelfx: `ω += xung; ω += (−60·θ − 3,4·ω)·dt; θ` chặn ±8° (xung 0,03–0,08 rad). Nén lúc trúng: (1,1; 0,9) về 1 trong
  0,18 s.
- **Chớp:** `_Flash` của shader sticker (đã có trong `StickerOutline.shader`) lên trắng kem 1–3 khung rồi tắt; đòn theo hệ thì sau đó
  phủ màu hệ nhạt 0,1 s (lửa cam, băng xanh nhạt, độc xanh lá). Không nhấp nháy quá 3 lần/giây.
- **Lấy đà trước, khựng lúc chạm, theo đà sau:** 80% "đọc" của cú đánh nằm trước lúc chạm.

## 5. Biên đạo theo pha

Mọi hiệu ứng lớn đi qua: **tụ lực** (hạt bay vào, vòng co lại) → **phát** (1–2 khung hình nổ kem, vệt, nổ) → **lan** → **đọng**
(lấp lánh, than âm ỉ) → **tan dài**. Nhiều sự kiện nhỏ, mỗi cái khác cỡ, tốc, giờ, đời. Đỉnh rơi vào **1/4 đầu** đời hiệu ứng.

| Clip (.atomik) | Dài (giây sân) | Nhịp |
|---|---|---|
| idle | 2,0 (lặp, liền mạch) | thở 3%, phụ kiện lệch pha, một điểm phá nhịp ở 62–72%; hạt idle theo `cycle` (mục 7) |
| hit | 0,6 | bật ở 0,07 s (ease-out), giữ, về; hạt văng ngay lúc 0 |
| attack | 1,0 | lấy đà 0,3 s **ngược chiều** cú đánh, ra đòn 2–3 khung (0,08–0,12 s), khựng 0,1 s, theo đà vượt rồi về; trúng ở 0,40–0,52 s |
| cast | 1,0 | tụ ở miệng hoặc vũ khí 0,15–0,55 s (hạt bay vào, cầu to dần), giật ngược lúc bắn |
| skill | 1,6–1,9 | tụ lực 0,4–0,6 s, phát, 1–3 nhịp trúng, tan 0,4 s; boss có tờ hiệu ứng thứ hai |
| evolve | 2,8 | gồng, lốc tụ, đổi dạng lúc lốc đậm nhất, nổ, gầm, hoà về khung đầu idle dạng sau |

Một hiệu ứng đứng một mình trông như cái nhãn dán; **thân tướng phải diễn quanh nó** (pixelfx "acts").

## 6. Hạt có vật lý (đổi từ `pixelfx/src/core/sim.js`)

Đơn vị dưới đây theo **H** (chiều cao tướng) và giây sân. pixelfx: tướng cao 38 px, trọng lực 950 px/s² ≈ 25 H/s², tia văng
80–260 px/s ≈ 2–7 H/s. Hạt hiện có trong `beast.burst()` (0,5–1 H/s, trọng lực 1,6 H/s²) **chậm và lơ lửng quá**: nhanh lên, thêm cản.

| Kiểu | Chuyển động | Hình (vẽ tay, tô phẳng) | Dùng cho |
|---|---|---|---|
| **tia văng** | 2–5 H/s, cản 2,2/s, trọng lực 0,45 × 10–20 H/s², nảy sàn 1 lần (vận tốc dọc × −0,45, ngang × 0,7) | vệt thuôn có viền, dài theo tốc độ (tối đa ~0,1 H), 2 màu | trúng đòn, kim loại, lửa |
| **mảnh vỡ** | 1,5–4 H/s, trọng lực 10–20 H/s², nảy 1 lần (× 0,25) rồi nằm, mờ sau 0,5 s | mảnh đá, băng, gỗ, pha lê; xoay tròn ±200–400°/s | nện đất, vỡ giáp, chiêu đá |
| **bụi** | 0,3–0,8 H/s, cản 4/s, nở 1,5–2 lần, alpha `k^1,3` | cụm tròn phẳng màu đất nhạt | chân lao, đáp đất, trượt |
| **khói** | bay lên 0,1–0,2 H/s, lắc ngang sin, cản 1,2–1,6/s, sống 0,8–2 s | 2–3 cụm tròn chồng nhau, nhạt dần về xám | sau nổ lửa, than tắt |
| **lửa** | bay lên, cản 3–5/s, lắc; chết thì có thể để lại khói | 3–4 hình theo dải màu, đổi theo tuổi | bờm, đuôi, phun lửa |
| **than (ember)** | bay lên 0,2–0,5 H/s, lượn sin, cản 1,6/s, sống 1–2 s | chấm lửa nhỏ có viền | idle hệ Lửa, sau nổ |
| **tụ lực (streak)** | bay **vào** tâm, tốc nhân e^(3t) | vệt chấm thuôn | lúc tụ chiêu, cầu ở miệng |
| **bông, lá, cánh hoa** | rơi chậm 0,1–0,3 H/s, lượn sin, cản 2,2/s | lá, hoa, tuyết, lông | idle Mộc, chiêu hoa, băng |
| **lấp lánh** | đứng yên, nhấp nháy 2–3 nhịp | sao 4 cánh phẳng | kim loại, ngọc, thánh |

- **Mọi hạt khác nhau** (cỡ, tốc, giờ trễ, đời) bằng số giả ngẫu nhiên có hạt giống: cùng một clip luôn ra cùng một hình.
- **Nhanh vào, chậm ra:** tung mạnh rồi cản; kết thúc bằng co nhỏ hoặc tan, không biến mất cái rụp.
- **Có lưu dấu:** mảnh vỡ, vết cháy nằm lại 0,5–1,5 s trên sàn rồi mới tan, không che con đang đứng.
- **Chiều sâu:** vòng dưới chân là elip; **nửa xa vẽ sau thân, nửa gần vẽ trước** (hoặc chỉ nửa xa nếu ảnh đặc).
- **Ngân sách:** mỗi cú trúng ≤ 25 hạt Image, cả sân ≤ 120 hạt sống; mỗi tướng idle ≤ 6 hạt. ParticleSystem: ≤ 100 hạt mỗi
  emitter, mỗi chiêu 5–8 draw call. Đo **overdraw** (ảnh to chồng nhau), không chỉ đếm hạt; thử 6 tướng đánh cùng lúc.

### 6b. Sét giật thật, ảnh hiệu ứng sinh bằng thuật toán (Thanh Long, 2026-11-09)

Sét là **chuyển động**, không phải một ảnh: tia gấp khúc đổi dáng gần như mỗi khung, có nhánh, chớp tắt. Ảnh GPT vẽ một tia sét
rồi trượt xuống là "sét tĩnh" (người dùng chê). Cách làm trong `.atomik`:

- `ArtGen/Spine/lightning.py` vẽ bằng thuật toán theo luật vẽ tay (tô phẳng vàng, vân chì gạch chéo, lõi kem, viền mực):
  `bolt()` (đường gấp khúc `_zig`: đỉnh lệch luân phiên, dốc ≥ ~42°, rải đều; nhánh, nhánh con; `leader_frac` = tia dẫn),
  `crackle()` (tia điện nhỏ), `clod()` (đất, sỏi), `scorch()` (vết cháy nứt), `puff()` (bụi), `storm_cloud()` (mây giông từ ảnh
  mây sẵn có). Xem tờ thử: `py -3 -I lightning.py <ra.png>`. Ảnh sinh ra đều cắt viền trong suốt (`beast._crop`) cho atlas gọn.
- **Slot nhiều ảnh** (`beast.MULTI`): một slot mang nhiều att, `P.att[slot] = "<slot>_<att>"` đổi dáng theo khung (bake 30 khung/giây).
- Khai trong `beasts_cfg` khoá `juice`:
  - `"lightning": {"strikes": [(giây so với nhát chính, lệch ngang theo H)...], "height", "cloud", "crackle", "caster"}`: chiêu
    `storm` chuyển sang `skill_lightning` (dài 2,0 s), tắt các ảnh cũ ở chỗ đối thủ có vẽ sẵn sét tĩnh (`ff_big`, `ff_big2`,
    `ff_ground`, `fp*`);
  - nhịp chớp ở `BOLT_MAIN` / `BOLT_PRE` (khung → dáng, độ đậm; thiếu khung = tắt): 2 khung tia dẫn, giữ dáng đầu 2 khung (trùng lúc
    khựng), rồi mỗi khung một dáng, tắt xen giữa, nhạt dần;
  - `"phys"` là danh sách nhóm (`img` `"@dirt"` = cục đất sinh ra; `kind` leaf/spark/debris; `n`, `size`, `speed`, `life`, `ang`),
    nhóm đầu cũng văng ở đòn thường; `"phys_pre"` cho từng nhát phụ. Đời hạt tự cắt trước cuối clip (`ctx.clip_dur`);
  - idle `{"img": "@crackle", "kind": "crackle"}`: tia điện lách tách theo pha (nối vòng liền);
  - `"impact"` thêm phần tử thứ 4 là màu chớp cả màn hex 8 số (`"#fff6c98c"`: kem, alpha 0,55) → `AtomikGame.impactFlash` →
    `StageView.Flash` (alpha của màu được tính).
- Thứ tự vẽ: vết cháy, bụi, tia sét, mây giông (đè đầu tia), tia điện, hạt. Mây ở `height` H trên đất dưới chân đối thủ, không vượt
  khung camera sticker (3,4 H, dịch lên tối đa 0,8 H).
- Soi nhanh không cần Unity: `xem_set.py` (scratchpad của phiên) vẽ clip đã nướng khung rộng cao, lưới nhiều cột.

## 7. Idle "sống" theo hệ

Idle đứng yên một chỗ là lỗi. Mỗi tướng có ít nhất: thở, phụ kiện lệch pha, một điểm phá nhịp, và **1 lớp hạt nhẹ theo hệ**:

| Hệ | Hạt idle | Phụ kiện động |
|---|---|---|
| Lửa | 2–4 than bay lên lượn từ bờm, đuôi | ngọn lửa ở bờm, đuôi lắc nhanh lệch pha (chu kỳ 0,5–0,8 s), lửa nhỏ co giãn 5% |
| Thủy | 2–3 bọt nổi lên rồi vỡ, giọt rơi | sóng, vây, râu uốn chậm |
| Mộc | 1–3 lá, cánh hoa rơi lượn | lá trên người rung, dây leo đung đưa |
| Thổ | sỏi nhỏ, bụi rơi khi nhún | mảnh đá trên người nảy nhẹ |
| Kim | 1–2 lấp lánh trên giáp, ngọc | vật kim loại lắc ít, cứng |
| Boss | thêm vòng hệ dưới chân (nửa xa sau thân), xoay chậm, alpha 0,4–0,6 | hiệu ứng bay quanh có quỹ đạo riêng |

Trong .atomik: hạt idle phải **liền mạch khi lặp**. Dùng kiểu `cycle` của pixelfx: hạt i có pha `(t/D + i/n) mod 1`, vị trí,
alpha là hàm của pha (sinh ở pha 0, tan hết trước pha 1). Không dùng hạt "bắn một lần" trong idle.

## 8. Animation tướng: nguyên tắc diễn

- **Lấy đà ngược chiều cú đánh**, đổi dáng lớn ở khung ra đòn (bóng dáng khác hẳn), **khựng lúc chạm**, theo đà vượt quá rồi về.
- **Dáng "snap":** dáng ra đòn nhảy tới ngay (không nội suy) ở khung ra đòn; pixelfx giữ dáng tay chân theo **bước 12 khung/giây**
  (vị trí chân vẫn mượt) cho cảm giác vẽ tay. Thử cho đòn đánh, chiêu: lượng tử hoá góc xoay xương thân, tay theo 1/12 s, giữ dời
  `move` mượt; soi rồi mới áp cả loạt.
- **Nén giãn giữ thể tích:** đòn thường (0,9; 1,09); nện, đáp nặng tới (0,85; 1,15); Celeste nhảy (0,6; 1,4), đáp (1,6; 0,4) là mức
  cực, game mình dùng nhẹ hơn. Hồi về 1 trong 0,18–0,3 s.
- **Phụ kiện trễ và ngược chiều** thân (đuôi trễ 0,05 s mỗi đốt, tai 0,06 s, chuông 0,1 s), biên độ lớn dần ra ngọn.
- **Con đánh vẫn hơi động lúc khựng** (Sakurai) để không chết hình; con bị đánh rung ngang.
- **Đòn khác kiểu nhau** giữa các dòng (không toàn "nhảy lên rồi ra chiêu"): xem bảng kiểu đòn, chiêu ở `beasts_cfg_hoa.py`,
  `beasts_cfg.py` (`_STYLE`).

## 9. Hạt trên sân: pool Image (mặc định) hay ParticleSystem

**Mặc định: pool Image theo mẫu `MachineFx`** (`Assets/01 Script/Game/Machine/MachineFx.cs`: `struct Hat` trong `List<Hat>`, kho
`Stack<Image>` nới bằng `Ui.Spawn` prefab `Items/HatMayBi`, `Emit`, `Update(dt)` có trọng lực, cản, đường cỡ, màu, kéo dãn). Viết
lớp hạt sân giống vậy, cho chạy bằng **dt của đồng hồ sân** (đứng khi khựng), ảnh lấy từ `ArtLibrary` hoặc trường trên StageView.
Ưu: tất định, không thêm gói, tuân `PrefabOnlyTests`. Nhược: mỗi Image dời làm canvas dựng lại: để hạt trên **sub-canvas riêng**.

**ParticleSystem qua UIParticle** (mob-sakai/ParticleEffectForUGUI, MIT, `com.coffee.ui-particle` v4.14.2, chạy Unity 6) **chỉ khi
người dùng đồng ý thêm gói**:
- cài bằng git URL `https://github.com/mob-sakai/ParticleEffectForUGUI.git#<tag>` hoặc OpenUPM; vẽ qua CanvasRenderer nên theo thứ
  tự sibling, CanvasGroup, Mask;
- material **`UI/Default`** (alpha blend). **Không** `UI/Additive` dù tài liệu gợi ý; ảnh vẽ tay gom vào **một atlas**, dùng Texture
  Sheet Animation chế độ Sprites, đổi hình ngẫu nhiên mỗi hạt (Random Start Frame) hoặc chạy 12 khung/giây cho kiểu vẽ tay;
- UIParticle không đặt chung GameObject với ParticleSystem; bật mesh sharing khi nhiều hiệu ứng giống nhau;
- chạy theo đồng hồ sân: tắt tự chạy, mỗi khung gọi `ps.Simulate(dtSân, true, false, false)`; khựng thì không gọi (hoặc
  `Pause()` rồi `Play()`), đừng trông vào `timeScale = 0` (Play không chạy khi timeScale 0);
- module nên dùng: Limit Velocity over Lifetime (cản), Gravity Modifier, Collision kiểu Planes đặt ở đường sàn (Bounce 0,3–0,45,
  Lifetime Loss), Size/Color over Lifetime (alpha giảm, không đổi sáng), Stretched Billboard cho vệt, Sub Emitters (tia chết → khói);
  Limit Velocity và đổi thuộc tính lúc chạy làm mất culling tự động: đặt Max Particles;
- prefab hiệu ứng dựng sẵn bằng menu editor, lấy từ pool, không Instantiate lúc trận.

## 10. Sửa ở đâu trong code

Số dòng tính tới 2026-11-09, có thể lệch; tìm theo tên hàm.

| Việc | Chỗ |
|---|---|
| đồng hồ sân, nhịp chậm lúc đánh | `StageView.Update` (dt = min(0,05, unscaledDeltaTime) × Pace 3 × slow × fast; `AttackPace` 1,3, `SkillPace` 1, `skillHold`) |
| **thêm khựng** | biến `freeze` trong `StageView.Update`: còn khựng thì dt = 0 (hoặc ×0,1) cho tướng, hiệu ứng sân, rung vẫn giảm theo giờ thật; đặt freeze ở chỗ gọi `onHit` |
| khoảnh khắc trúng | `StageView.Update` gọi `onHit` khi `a.t >= HitTime`; `HitTime = HitFrame / Fps` (`AolaSticker`); .atomik lấy `game.hitTimes` (`AolaActor`, làm tròn theo fps); mỗi clip một nhịp trúng |
| phản hồi sát thương | `BattlePlayer` sự kiện Dmg → `StageView.Hurt` (flash 0,16, rung 6/12, clip Hit nếu đang đứng), `Burst` (chữ + 9 tia), `Number`, `Text` |
| rung | `StageView` một số `shake` (Max, giảm 40/s) lắc cả `root` "rung": đổi sang trauma + bump có hướng (mục 4) |
| **bật lùi, nghiêng lò xo** | `StageView.Place`/vòng tướng trong `Update` (đã có né `hop`, lệch lao 985–1019): thêm offset bật lùi và góc lò xo cho actor bị đánh |
| hiệu ứng sân có sẵn | pool `Take`/`AddFx`/`Release`; khối `Pop`, `Drift`, `Spin`, `Ripple`, `Spark`, `Ring`, `Burst`, `Flash`; ảnh gán bởi `Editor/BeamFxMenu.cs` từ `Assets/03 Art/Fx` |
| neo vị trí | `StageView` `Head`/`Body`/`Pos`; điểm bắn tia `AolaSticker`; xương .atomik chưa mở ra ngoài (`AtomikPose.BonePos` có sẵn nếu cần neo hạt theo bờm, vũ khí) |
| nhiều nhịp trúng trong một chiêu | hiện chỉ một; muốn liên hoàn thật thì mở rộng `game.hitTimes` thành danh sách và cho `BattlePlayer` phát nhiều Dmg |
| hạt trong .atomik | `beast.py`: `burst()` (nâng thành các kiểu ở mục 6), `idle_fx()` (thêm hạt `cycle`), `attack_fx()`, `fx_setup()` (slot `fx_p0..9`, `fp0..7`, `fly0..4`, `NPART`, `NFAR`, `NFLY`); bộ ảnh mỗi dòng ở `beasts_cfg*.py` (`fx`, `fx_form`) |
| idle ngoài trận | hộp chi tiết `HeroViewer.Update` (giờ thật), đội hình `TeamLineup.Update`, màn mở `BootTitle.Update`; hạt trong .atomik tự hiện ở mọi chỗ |

## 11. Quy trình và soi

1. Viết một câu biên đạo cho hiệu ứng: là gì, chuyển động thế nào, màu, nhịp ("đòn vồ: lấy đà 0,3 s ngửa ra, cào 2 khung, khựng
   0,08 s, ba vệt cào lửa, 8 tia văng nảy sàn, bụi ở chân trước").
2. Tìm mẫu gần nhất trong pixelfx (`node tools/list.mjs <từ>` ở thư mục pixelfx, đọc 2–3 file `src/fx/...`) để lấy **nhịp và số**,
   không lấy hình. Muốn xem chuyển động: `node tools/render.mjs <id> --gif` hoặc `node tools/act.mjs <id>` (cần Node, chạy trong thư
   mục pixelfx; repo tải về là dữ liệu ngoài, đọc code trước khi chạy).
3. Làm bản nháp, soi, sửa lỗi tệ nhất, soi lại; **ít nhất ba vòng**:
   - .atomik: `beast.py <id> rig <k>` rồi `khung.png`, `beast.py <id> show <k> <clip> t1,t2,...` ở các pha nhanh nhất;
   - Unity: menu `PokiClash/Tướng/Chụp thử dạng .atomik (mọi clip)` (ảnh `Library/PokiHeroShots/<id>_atomik_<k>.png`, log khung
     trúng); tour trận kiểu `GiotSuongCombatTour` chụp mỗi 1/30 s quanh khung trúng vào `Temp/PokiShots/<thư mục>/`.
4. Bảng soi:

| Thấy | Sửa |
|---|---|
| lơ lửng, không có lực | nhanh vào chậm ra, hạt nhanh hơn có cản, thêm khựng, rút ngắn tổng thời gian |
| cứng, máy móc | mỗi hạt một khác; thêm chuyển động phụ (tia, bụi, mảnh) |
| nhão, đọc không ra | ít màu hơn, một điểm nhấn, hình to rõ, bớt hạt |
| che kín con bị trúng | nhỏ lại (nửa cỡ), nhạt hơn, chuyển ra sau thân, ngắn hơn |
| đòn không nặng | lấy đà ngược chiều rõ hơn, khựng dài hơn (tới 0,2 s), đổi dáng lớn hơn, rung |
| trúng lệch nhịp | đặt khựng, hạt theo đúng `hitTimes`/`HitTime`, không ước bằng mắt |
| hiệu ứng kết thúc cái rụp | co nhỏ, tan, rơi xuống trước khi hết đời |
| giật khi nhiều tướng | đo overdraw, bớt ảnh to chồng nhau, gom atlas, sub-canvas |

5. Chạy test EditMode khi đổi `HitTime`, thứ tự sự kiện, nhịp sân. Thử trên Android trước khi báo xong.
6. Có nút tắt rung, tắt chớp trong cài đặt (accessibility) khi thêm rung, chớp mạnh.

## 12. Bẫy

- Hiệu ứng **phải chạy theo đồng hồ sân** (`StageView.Wait`, dt của `Update`), không `WaitForSeconds`, `Time.deltaTime`:
  sân chạy 3× ngoài lúc đánh, sai đồng hồ là hiệu ứng lệch khỏi đòn và không đứng khi khựng.
- Các hệ chạy giờ thật (`BattleController.W`, thẻ bay, biểu tượng trạng thái, `ArenaAnim`, `UltCutIn`) **không** dừng khi khựng:
  khựng chỉ được ngắn (≤ 0,2 s) để chúng không lệch.
- Khựng cộng dồn thành slow-mo kéo dài: dùng max, có giới hạn tổng.
- Rung random mỗi khung nhìn như lỗi; rung không giảm dần gây mệt. Rung cả `root` lắc cả nền: đòn nhỏ chỉ bump có hướng.
- Hạt idle bắn một lần trong clip lặp: nối vòng bị nhảy. Dùng `cycle`.
- Ảnh hình vòng có lòng giấy trắng khép kín lên sân thành đĩa trắng: khai `HOLLOW` khi cắt tờ (`build_fx_beasts.py`).
- Slot hạt trong .atomik có hạn (`NPART` 10, `NFAR` 8, `NFLY` 5): hai đợt hạt chồng giờ nhau thì giành slot; `burst()` đã giữ
  đợt đang bay, đừng xoá điều đó.
- `UiMotion.cs` đang làm hỏng `PrefabOnlyTests` (AddComponent) từ trước: đừng thêm lỗi cùng loại.
- Nguồn tham khảo: pixelfx https://github.com/patch-gg/pixelfx (MIT; font Patch Pixel không thuộc MIT);
  game-feel skill https://github.com/gamedev-skills/awesome-gamedev-agent-skills (Apache-2.0);
  scenario-unity-vfx https://github.com/scenario-labs/skills (MIT); UIParticle https://github.com/mob-sakai/ParticleEffectForUGUI
  (MIT); Celeste https://github.com/NoelFB/Celeste; Sakurai về hitstop https://nintendowire.com/news/2022/12/12/this-week-in-sakurai-12-5-12-11-fine-tuning-hit-stop-and-cheating-the-system/;
  Eiserloh "Juicing your cameras" https://gdcvault.com/play/1023146/Math-for-Game-Programmers-Juicing; LoL VFX style guide
  https://nexus.leagueoflegends.com/en-us/2017/10/dev-leagues-vfx-style-guide/.
