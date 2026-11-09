---
name: pokiclash-spine-rig
description: >
  Rig xương và làm animation cho nhân vật 2D từ ảnh (ảnh GPT vẽ hoặc một ảnh liền bất kỳ): cắt mảnh, khớp vị trí, dựng xương,
  mảnh cứng, một lưới hay nhiều lớp lưới có trọng số (uốn mềm, không hở khớp), viết animation (đứng, đánh, trúng đòn, chiêu,
  nhảy, đi/chạy), dựng khung soi, GIF, trang Spine Web Player; xuất JSON Spine 4.2 và định dạng riêng .atomik chạy trong Unity
  của PokiClash (importer + runtime AtomikPlayer). Dùng khi người dùng muốn rig xương / làm animation từ một hình, sửa hở
  khớp, uốn tóc, áo, đuôi, hoặc đưa animation vào Unity bằng .atomik.
---

# Rig xương từ ảnh và định dạng .atomik (thử nghiệm)

Làm 2026-11-07 để đo khả năng rig tự động. **Không thay quy trình chính của game** (vẽ đè lên rig aola, xem CLAUDE.md mục
Hình tướng). Mọi thứ ở đây là thử nghiệm cho tới khi người dùng chốt khác. Ngoại lệ người dùng yêu cầu 2026-11-08: Rồng Giọt
(dạng 1 dòng Giọt Sương) vào game bằng .atomik, xem mục 10.

## 0a. Tiêu chí bắt buộc cho tướng .atomik (người dùng chốt 2026-11-09, soát trước khi báo xong)

Hình, dạng tiến hóa:
- **Chibi chỉ ở dạng 1.** Dạng sau tỉ lệ trưởng thành, dữ dần: đầu nhỏ lại, mắt xếch, nanh, móng, thế sẵn sàng đánh.
- **Dạng cuối khác hẳn dạng trước** chứ không chỉ thêm chi tiết: đổi màu chủ đạo (đậm hơn), thêm giáp/đồ/phụ kiện, đổi chi tiết đặc
  trưng (râu, đuôi, sừng) và **đổi dáng** (bóng dáng nhìn đã biết là con khác). Vẫn giữ vài nét nhận ra cùng dòng.
- Con dài dẹt thì co cho vừa sân (`max_w`); không để lòi khỏi mép màn.

Animation:
- **Không có gì đứng im:** mây, đồ bay, vòng quanh tướng phải chuyển động; phụ kiện bay quanh dùng clip lặp `aura` (liền qua mọi clip).
- Thân dài (rồng, rắn, đuôi to) **nhiều xương, uốn sóng** (`spine`); **tóc, bờm, râu nhiều xương có lò xo** (`soft`), tách lớp riêng nếu
  lắc làm nhoè phần khác (`sep`).
- **Bắn từ miệng thì phải há miệng:** tách hàm dưới thành vùng `jaw` (xương `jaw` con của đầu, khớp ở góc hàm); đòn, chiêu nhả từ
  miệng tự há theo nhịp (`beast.jaw_open`).

Đòn và chiêu:
- **Đòn đánh xa đứng một chỗ bắn**, không lao lên nhả chiêu; chỉ giật nhẹ ngược chiều khi bắn (cổ, thân vươn là đủ).
- **Không một màu**: tránh để cả loạt tướng "lao lên húc rồi lộn". Phần lớn chiêu đứng tại chỗ (tia, xoáy, mưa đạn, cột trồi, sóng
  âm, triệu hồi...); chỉ dòng có lore lao húc (dê, bò, tê giác) mới lao.
- **Mỗi dạng một chiêu khác, mạnh dần**: dạng sau to hơn, nhiều nhát hơn, dữ dội hơn (khựng, rung, chớp màn tăng theo dạng),
  thường đổi cả kiểu chiêu chứ không chỉ phóng to (`*_form`, `attack`/`skill`/`motion` theo dạng).
- Chiêu lấy ý từ lore con vật và chiêu Pokémon cùng hệ (Thủy: Hydro Pump, Whirlpool, Surf, Icicle Crash; Mộc: Leaf Storm, Solar
  Beam, Frenzy Plant, Petal Blizzard; Hỏa: Flamethrower, Fire Spin, Eruption, Heat Wave...), học nhịp Critters (skill
  `pokiclash-hero-fx` mục 1b).
- Hạt nhỏ (lá...) vẽ không viền sticker (`game.plain`).

## 0. Trước khi làm

- **Giấy phép:** code repo `spine-animation-ai` là PolyForm Noncommercial (không dùng thương mại). Runtime `spine-unity` đòi
  giấy phép Spine Editor. Vì vậy đưa vào game thì dùng **định dạng riêng `.atomik`** (mục 9), không dùng runtime Spine.
- **Bản quyền ảnh:** ảnh lấy trên mạng (nhân vật của hãng khác: Snorlax, Agnes Tachyon...) chỉ để thử. Để ngoài PokiWar, trong
  `<ProjectAtomik>/spine-animation-ai/work/<tên>/`. Không commit, không publish artifact. Ngoại lệ do người dùng yêu cầu: con mận
  trong `Assets/05 Atomik Thu/` (scene thử Unity), không commit thư mục đó.
- **Repo và Python:** repo clone cạnh PokiWar: `E:\ProjectAtomik\spine-animation-ai` (máy kia: clone cạnh project, hoặc biến
  môi trường `SPINE_AI`). venv riêng `.venv` có `opencv-python Pillow numpy`. Chạy bằng `<repo>/.venv/Scripts/python -I`.
  Không cần API key (bước Gemini của repo không dùng).
- Chỉ dùng lại 3 thứ của repo: `make_atlas.pack`, `build_spine_json._convert_timeline` (đổi khoá sang dạng 4.2), Spine Web
  Player. Bộ rig dáng người của repo không hợp con thú chibi; dùng công cụ ở `ArtGen/Spine/`.

## 1. Chọn cách

| Cách | Khi nào | Lệnh |
|---|---|---|
| **A. GPT vẽ hình trọn con + tờ mảnh** | tướng mới, muốn mảnh sạch có đầu khớp tròn | `build.py` → `gen.py` → `rig.py all` |
| **B. Một ảnh, mảnh cứng** | ảnh nét viền rõ, chuyển động nhẹ | `rig.py one1 <mã>` |
| **C. Một ảnh, một lưới có trọng số** | con gọn, ít lớp chồng (khuyên dùng) | `mesh.py <mã>` |
| **D. Một ảnh, nhiều lớp lưới** | áo choàng, tay áo, đuôi chồng lên thân, chân | `mesh.py <mã>` (spec có `pieces`) |

Người dùng nghĩ "rig" là làm từ **một ảnh liền**: đưa một ảnh thì đi thẳng B/C/D, không bắt GPT vẽ tờ mảnh.

Ảnh dễ rig: đứng thẳng hoặc nghiêng nhẹ, tay chân tách khỏi thân, không chéo nhau, nền trắng. Dáng chữ T là dễ nhất.

Chọn đa giác vùng: kẻ lưới toạ độ lên ảnh (bước 10–25 px, phóng 2–3x, số mỗi 50/100 px, chữ bằng `arial.ttf`), cắt cận từng
vùng khó rồi đọc toạ độ. Sau mỗi lần dựng, soi bản đồ vùng tô màu (mục 6).

## 2. Cách A: GPT vẽ (ArtGen/Spine)

- `build.py <mã>` sinh gói `ArtGen/Spine/gui_gpt/<mã>/`: `luot_1_tong.txt` (hình trọn con dáng dễ rig, 1024x1536) và
  `HUONG_DAN.md`. `luot_2_tach_manh.txt` (2 tờ: nhóm đầu, nhóm thân; mỗi mảnh vẽ đủ phần bị che, đầu khớp thừa ~30 px tròn,
  cách nhau ≥ 60 px) **chỉ sinh khi đã có** `inbox/<mã>/L1_duyet.png`. File prompt theo luật ArtGen của CLAUDE.md (ảnh mẫu
  đường dẫn tuyệt đối, mục SAVE dạng `save it as a PNG to <path>` để `gen_codex.py` dò được chỗ lưu).
- `gen.py <file prompt>`: gọi Codex qua `ArtGen/Heroes/tools/gen_codex.py`, giữ chung khoá `ArtGen/Heroes/inbox/.codex.lock`
  với các lô tướng. Chạy nền. Hết hạn mức thì hỏi giờ có lại bằng
  `codex.exe exec --skip-git-repo-check -s read-only -- "Reply ok."` (exe trong `%TEMP%\pokiclash_codex_path.txt`): lỗi trả
  về có "try again at <giờ>". Báo người dùng, đừng chờ mù.
- `rig.py cut <mã>`: cắt tờ mảnh theo `SPEC[<mã>]["sheets"]`. Mẩu rời sát mảnh lớn (< 45 px) tự gộp. **Đếm sai số mảnh thì
  dừng**, in khung từng mảnh.
- `rig.py place <mã>`: khớp từng mảnh vào ảnh trọn con (SQDIFF có mặt nạ trên Lab, dò tỉ lệ + góc + vị trí, 3 tầng). Mảnh lớn
  nhất mỗi tờ dò tỉ lệ cả tờ (0.35–2.8), mảnh khác dò quanh đó; mảnh trái/phải giới hạn theo nửa người. Ra `so_ghep.png` + IoU.
- `rig.py build <mã>`: khớp xương = tâm vùng giao giữa mảnh con và mảnh cha.

## 3. Cách B: một ảnh, mảnh cứng (`rig.py one1`)

Spec trong `rig.py` (mẫu `SPEC["snorlax"]`): `base`, `src`, `fg` (ngưỡng sáng, ngưỡng bão hoà của nền), `dark_thr`.
`one`: mỗi mảnh `{poly, excl, keep, minus, cap, cap_keep, inpaint}`:
- `excl`: giành pixel trước (đầu → tay → thân); mảnh không excl (bụng, tai, chân) được chồng.
- `keep: "light"/"dark"`: chỉ lấy lớp màu đó. `minus`: đa giác trừ ra.
- `cap: (mảnh cha, r)`: phần chồng lấn r px vào mảnh cha, mờ dần; `cap_keep` chỉ lấy màu lông.
- `inpaint`: vẽ bù lớp màu đó trong mảnh (chỗ bị mảnh khác che).
`draw`: thứ tự vẽ sau → trước. `root`: gốc (giữa hai chân, mặt đất). `bones`: `(xương, cha, mảnh, (x, y) khớp)`.

## 4. Cách C và D: lưới có trọng số (`mesh.py`) — uốn mềm, không hở

Chung:
- Lưới: điểm viền cách đều `step_edge` (đầu danh sách = hull, mọi khối rời) + lưới điểm trong `step_in`, Delaunay
  (`cv2.Subdiv2D`), bỏ tam giác có trọng tâm hoặc trung điểm cạnh ra ngoài hình.
- `bones`: `(xương, cha, (x, y) khớp)` hoặc thêm phần tử thứ 4 `{"inherit": "noScale"}`.
- `labels` = vùng của từng xương, ưu tiên theo thứ tự (vùng trước giành pixel trước):
  - `(xương, đa giác hoặc danh sách đa giác, lọc)`; lọc là `None`, `"dark"`/`"light"` (theo `dark_thr`) hoặc `("lt", 80)` /
    `("gt", 150)` (độ sáng trung bình).
  - Nhiều vùng cho một xương: đặt tên `"xương#ghi chú"` (vd. `root#shoes` cho giày với lọc khác quần tất).
  - Vùng cuối là `body` phủ cả ảnh để không pixel nào thiếu vùng.
- Trọng số: `w = exp(-(khoảng cách tới vùng / sigma)^2)`, giữ 4 xương nặng nhất, chuẩn hoá. `sigma` theo xương: tóc 8, tai 6,
  vải áo 16–18, thân 14, chân 4, vũ khí 5.
- `"geodesic": True`: khoảng cách đi trong hình, không nhảy qua khe trắng (lưỡi dao sát mép mũ vài px).
- `"smooth_labels": 5`: mỗi pixel theo vùng chiếm đa số trong ô 5x5, dải mảnh 1–2 px nhập về vùng bên cạnh (dải mảnh không
  phủ lưới được, để lộ nền thành đường kẻ).
- Thứ tự vẽ tam giác theo `layer` của vùng (tay vẽ sau cùng để đè lên bụng).
- Vũ khí, đồ cứng: gộp vào vùng xương bàn tay, sigma nhỏ để bám 100%, đi cứng không cong.
- Thân dẹp giãn làm méo tay, vũ khí: xương tay con của thân đặt `noScale`.
- Thêm xương khuỷu để tay cong; bụng có xương riêng để nảy.

Cách D thêm `pieces` (mỗi lớp một slot, một lưới, xếp sau → trước), mẫu `MESH["tachyon"]`:
- `{"name", "labels": [...] hoặc "rest", "into": [vùng], "px": n}`. `rest` = mọi vùng không thuộc lớp khác.
- Lớp nằm dưới **mọc thêm** n px dưới mép các vùng `into` (vùng của lớp đè lên nó). Dải đó được inpaint từ màu của chính lớp,
  nên khi lớp trên đung đưa không lộ nền. Ví dụ Tachyon: đuôi (mọc 22 px dưới vạt áo), chân (mọc 16 px dưới áo, thân),
  thân + áo + đầu (mọc 18 px dưới tay áo trái), tay áo trái trên cùng.
- `fh`, `gif_scale`: cỡ khung và GIF cho ảnh lớn. `detail: {times, boxes}`: ra `chi_tiet.png` cận cảnh tỉ lệ gốc từng vùng ở
  vài thời điểm (soi tóc, áo, đuôi).
- Tóc, đuôi lọc theo độ sáng: ngưỡng phải đủ rộng cho cả vệt sáng (Tachyon: `("lt", 165)`). Ngưỡng hẹp (120) đẩy highlight
  sang lớp thân, chúng đứng yên khi tóc/đuôi lay và lộ thành mảng, đường cắt.
- Chân (quần tất): ngưỡng chặt `("lt", 80)` và đa giác bám dáng chân, nếu không lớp chân ăn sang lót áo tím, nút áo.
- `bg_holes` (khe trắng nằm lọt giữa vùng được kê thì coi là nền) có trong code nhưng **đang không dùng**: thử với đuôi
  Tachyon thì xoá được khe nhưng mất luôn lọn ngọn mảnh (lưới không phủ được), để lại vết khuyết. Khe hẹp giữa lọn tạm để lấp.

Giới hạn: lưới chỉ kéo giãn ảnh có sẵn. Vai giơ quá ~50° cộng khuỷu ~25° là tay gập đè lên đầu; chỗ bị che không tự có hình.
Mái tóc trước mặt không cho động (mặt, mắt méo).

## 5. Animation

- Viết trong `<mã>_anims()` (rig.py) hoặc hàm trong `ANIMS` (mesh.py). `tl([(t, góc, curve)])` cho **rotate**,
  `tl2([(t, x, y, curve)])` cho **translate/scale**. Dùng nhầm `tl` cho translate là sai cả JSON (lỗi đã gặp).
- `curve` gắn với đoạn **kết thúc** ở khoá đó: `E` êm hai đầu, `EO` bật nhanh rồi chậm (đánh trúng), `EI` chậm rồi nhanh
  (lao vào), `None` thẳng. `_convert_timeline` đổi sang bezier tuyệt đối của 4.2.
- Vòng lặp nhiều phần phụ (idle tóc, áo, đuôi): hàm `wave(amp, phase)` (sin khép kín 8 khoá), trễ pha tăng dần từ gốc ra ngọn
  (tóc gốc 0.7, ngọn 1.3; đuôi 0.6 → 1.3 → 2.0), biên độ tăng dần ra ngọn (đuôi 4° → 7° → 10°).
- Xương setup không xoay. Góc dương = ngược kim (y lên). Tay trái người xem chĩa sang trái: góc âm là giơ lên; tay phải: dương.
- Chém bằng dao cầm dựng: kết thúc thấp trước bụng thì bàn tay xoay ~120°; 60–90° thì lưỡi dao quét ngang qua mặt.
- Con của `root` đã đi theo `root` (nhảy): **đừng cộng thêm** độ cao cho chân, chỉ co nhẹ.
- Bộ chuẩn: `idle` (lặp, thở; phần phụ lắc trễ pha; chớp mắt hoặc giật tai), `attack`/`slash` (lấy đà → đánh → dư lực → về),
  `hit`, `jump`/`skill` (ngồi → bật → rơi → dẹp nảy), `walk`/`run`.
- Khoá đầu = khoá cuối với vòng lặp; dẹp-giãn khi lấy đà và chạm đất; phần phụ trễ 0.1–0.2 s.

## 6. Soi trước khi báo (bắt buộc)

- `khung.png` (9 khung mỗi animation) và `anim_<tên>.gif`: bộ dựng khung Python riêng (`rig.render`, `rig.draw_pose`,
  `mesh.make_draw`, `mesh.make_draw_multi`). Soi: hở khớp, mảnh lệch, mất mảnh, cắt khung.
- `luoi.png`: lưới + màu trọng số + khớp (cách D: mỗi lớp một ô, nền xám để thấy dải vẽ bù).
- Bản đồ vùng tô màu (dựng tạm từ `mesh.label_map`): soi vùng ăn lẹm (chân lấy lót áo, đuôi lấy dây đeo ống nghiệm...).
- So khung t=0 với ảnh gốc ở tỉ lệ gốc: phải trùng khít. Đường kẻ mảnh, mảng lạ ở t=0 là lỗi vùng, không phải animation.
- Trang xem `rig/index.html`, `rig_mesh/index.html`: server tĩnh `.claude/launch.json` cấu hình `spine-work` (cổng 8771, phục vụ
  `spine-animation-ai/work`), `preview_start` rồi tới `http://localhost:8771/<tên>/rig_mesh/index.html`. Kiểm bằng JS
  `Object.entries(players).map(([k,p])=>[k,!!p.skeleton])`; ảnh lớn tải tới ~10 s. Spine player ghim `4.2.119`.
- Gửi người dùng khung, GIF, ảnh so sánh bằng SendUserFile; nói rõ cái gì chưa ổn.

## 7. Lỗi đã gặp và cách tránh

- Nền ô cờ "giả trong suốt" in vào pixel: mặt nạ nền theo vùng sáng nối mép ảnh, gọt 1 px + làm mượt (blur 1.6, ngưỡng 0.5).
- Ảnh webp: nền không còn đúng 255 (nén); đọc bằng Pillow rồi lưu `src.png`.
- Đa giác đầu ăn lẹm vai: kẻ sát mép đầu, để vai cho tay.
- Vẽ bù ra màu xám, vệt chữ V: nới vùng vẽ bù 2 px, phần ngoài tô màu trung vị trước khi inpaint.
- Phần chồng của tay quét vệt sẫm: bán kính ~9 px, chỉ lấy màu lông.
- `Subdiv2D` trả float32: làm tròn điểm theo bước 0.25 trước khi chèn.
- In tiếng Việt: `sys.stdout.reconfigure(encoding="utf-8")` (`-I` bỏ qua `PYTHONIOENCODING`); vẽ chữ Việt lên ảnh dùng
  `ImageFont.truetype("C:/Windows/Fonts/arial.ttf")`.
- Heredoc Bash nuốt `\\`: script có regex, đường dẫn Windows thì sửa bằng Edit/Write.

## 8. Tệp

- `ArtGen/Spine/build.py` (gói prompt), `gen.py` (Codex có khoá), `rig.py` (cắt, khớp, dựng, mảnh cứng, khung, trang xem,
  animation, `pose` có `noScale`), `mesh.py` (lưới một lớp `main`, nhiều lớp `main_multi`, nhãn vùng, trọng số, animation các
  con thử), `atomik.py` (xuất .atomik).
- Đầu ra: `<base>/rig/` (mảnh cứng), `<base>/rig_mesh/` (lưới: `<mã>_mesh.json/.atlas/.png`, `luoi.png`, `khung.png`,
  `chi_tiet.png`, GIF, `index.html`).
- Con đã chạy: Giọt Sương dữ liệu giả (scratchpad), `work/snorlax` (mảnh cứng + một lưới), `work/man_kiem` (một lưới, hai dao,
  idle/jump/slash), `work/tachyon` (4 lớp, 23 xương, idle tóc/áo/đuôi). Đều chỉ để thử.

## 9. Định dạng riêng .atomik (Unity của PokiClash, không cần runtime Spine)

**File:** `"ATMK"` + uint16 phiên bản (1) + gzip( uint32 dài JSON + JSON utf-8 + uint32 dài PNG + PNG atlas ). Con mận 213 KB.
JSON đúng khuôn `JsonUtility` (chỉ mảng, không từ điển):
- `rigName, version, ppu` (100 pixel = 1 đơn vị Unity);
- `bones[]: {name, parent, x, y, rot, sx, sy, noScale}`;
- `slots[]` (thứ tự vẽ sau → trước): `{name, bone, att}` (att = chỉ số hình mặc định, -1 trống);
- `atts[]: {slot, name, uvs[] (UV Unity của atlas, gốc dưới trái), tris[], wInfo[]}`; wInfo mỗi đỉnh `n, n x (xương, x, y, w)`
  theo xương ở tư thế gốc. Mảnh cứng, lưới không trọng số đều đổi về dạng này (một xương, trọng số 1);
- `anims[]: {name, dur, tls[], sk[]}`; `tls: {bone, type, keys[]}`: type 0 xoay sải 7 `[t, v, kiểu, c1..c4]`, 1 dời và 2 tỉ lệ
  sải 12 `[t, x, y, kiểu, 8 số]`; kiểu 0 thẳng, 1 bậc, 2 bezier (điểm điều khiển tuyệt đối như Spine 4.2, curve trên khoá i áp
  cho đoạn i → i+1); `sk: {slot, times[], atts[]}` đổi hình (chớp mắt).

**Xuất:** `py -3 -I ArtGen/Spine/atomik.py <tên>.json <tên>.atlas <ra>.atomik --name <tên>`. Đọc JSON Spine 4.2 bất kỳ do bộ rig
sinh (region, mesh có/không trọng số, rotate/translate/scale, attachment), atlas kiểu cũ (xy/size) hoặc `bounds`.

**Unity** (namespace `PokiClash.Game`, `PokiClash.EditorTools`):
- `Assets/01 Script/Game/Atomik/AtomikAsset.cs`: ScriptableObject + các lớp dữ liệu (khuôn JSON ở trên), `FindClip`.
- `AtomikPlayer.cs` (`[ExecuteAlways]`, cần MeshFilter + MeshRenderer): tính xương mỗi khung (xoay cộng, dời cộng, tỉ lệ nhân
  như Spine; `noScale`), da trên CPU, một Mesh một lần vẽ, tam giác theo thứ tự slot. API: `Play(clip, loop)` (trộn tư thế
  `mixTime` 0.12 s), `Sample(clip, t)`, `Done`, `Time01`, `speed`. Chỉ tạo Mesh lúc chạy (luật `PrefabOnlyTests`: không
  `new GameObject`, `AddComponent`, `new Material`, `new Texture2D` trong mã runtime).
- `AtomikDemo.cs`: scene thử, OnGUI nút đổi clip từng con (clip không lặp xong thì về idle), thanh tốc độ; tự xếp theo khung
  (màn dọc xếp cột, màn ngang xếp hàng, camera ôm vừa).
- `Assets/01 Script/Editor/AtomikImporter.cs`: `[ScriptedImporter(3, "atomik")]` tạo asset chính kèm atlas (nén theo nền tảng,
  xem bản 2 dưới), material `Sprites/Default` (nhân alpha trong shader, hợp atlas alpha thường) và **icon 128x128 vẽ con ở tư thế gốc**
  (thumbnail của `AddObjectToAsset`, hiện trong cửa sổ Project). Đổi cách nhập thì tăng số phiên bản importer để nhập lại.
- Menu `PokiClash/Thử/Atomik: dựng scene con mận (idle, nhảy, chém)`: dựng `Assets/05 Atomik Thu/AtomikMan.unity` bằng scene
  additive (lưu rồi đóng, không đổi scene đang mở), chụp 9 khung mỗi clip vào `Temp/AtomikShots/<tên>_khung.png` để so với
  khung Python (render bằng `RenderPipeline.SubmitRenderRequest`, đặt con ở xa mọi thứ của scene đang mở).

**Quy trình đưa code vào editor dùng chung** (đã chạy 2026-11-07):
1. Viết trong scratchpad, typecheck bằng dotnet: chép `PokiClash.Core/Game/Editor.csproj`, đường dẫn tuyệt đối, file scratch
   **thay** file cùng tên đã có trong csproj (không thì trùng định nghĩa), `dotnet build ... -v q`.
2. Đọc `mcpforunity://editor/state` qua MCP HTTP (`127.0.0.1:8090/mcp`). Đang Play thì hỏi người dùng rồi `manage_editor stop`:
   thêm `.cs` mới lúc Play làm hỏng biên dịch cho mọi session.
3. Chép file vào Assets một lệnh, `refresh_unity mode=force`, chờ hết compile, `read_console` lỗi, kiểm `.rsp` có file mới.
4. Chạy menu qua `execute_menu_item`. Mở scene: `manage_scene load` với `name` + `path` (thư mục), sau khi chắc scene đang mở
   không bẩn (`get_active` → `isDirty`). Đưa cửa sổ Unity lên trước bằng `WScript.Shell.AppActivate(pid)` để editor chạy khung.
5. Báo các session PokiWar khác (ListAgents + SendMessage) khi đã dừng Play, refresh, thêm script.
6. Xem xong muốn chạy game thì mở lại `Assets/00 Scenes/Boot.unity` rồi Play.

**Bản 2 (2026-11-08):** `anims[].sa: {slot, keys[]}` độ đậm slot (timeline `alpha` của Spine 4.2, sải 7 như xoay) cho hiệu ứng hiện,
tan; `game` (tuỳ chọn) thông tin trận khi rig là dạng tướng: `fps, height, hitClips, hitTimes, lunge, stay, muzzle, beam,
beamStyle, move, shadow` (`atomik.py ... --game <tệp.json>`, hoặc `convert(..., game=dict)`). Phần tính tư thế và dựng lưới tách
ra `Game/Atomik/AtomikPose.cs`, dùng chung cho `AtomikPlayer` và `AolaActor`. Importer bản 3 nén atlas theo nền tảng (ASTC 8x8
Android/iOS như atlas tướng aola, DXT5 máy tính khi cạnh chia hết cho 4; `pack` của `spine_compat.py` làm tròn cạnh lên bội 8).

**Còn thiếu:** vệt chém dạng lưới; bẻ đỉnh lưới (deform), màu tint, thứ tự vẽ đổi theo clip; nhiều trang atlas.

## 10. Dạng tướng .atomik trong game (Rồng Giọt thay Giọt Nước, 2026-11-08, máy ổ D)

Người dùng chọn: tướng mới "rồng con giọt nước" thay dạng 1 dòng Giọt Sương (`thuy_7`), gen bằng Codex, có clip tiến hóa nối vào
nút Tiến hóa. Mẫu để làm dạng khác:
- **Gói prompt** `ArtGen/Spine/build_rong_giot.py` (concept trọn con dáng dễ rig không cần ảnh thiết kế: đính ảnh mốc style,
  bản đồ, tờ mẫu thiết kế aola, dạng lớn của dòng; lượt 2 hai tờ mảnh: đầu, đầu nhắm mắt, đầu hét, mào, 2 tai / 2 cánh, thân,
  đuôi, kiếm, tay, nắm tay, đùi, bàn chân). Gọi `py -3 -I ArtGen/Spine/gen.py <file prompt> [--note ...]`. Mục SAVE phải viết
  đúng `save it as a PNG to <đường dẫn>` (cả từng bước), không thì `gen_codex.py` báo "không có mục SAVE".
- **Rig** `ArtGen/Spine/rong_giot.py cut | place [mảnh ...] | build` (venv có opencv, máy ổ D: `D:/spine-venv/Scripts/python -I`):
  - mảnh xanh trơn giống nhau nên `rig.place` dò tự do lạc 8/17 mảnh: dò quanh tâm đọc trên ảnh kẻ lưới (`HINT`), giới hạn góc
    (`ROT`), đặt tay mảnh khó (`FIXED`); `place <mảnh>` chỉ dò lại mảnh đó;
  - nắm tay cầm kiếm GPT vẽ rỗng ở giữa, bộ cắt lấp thành trắng: `fix_parts` tô lòng nắm màu cán kiếm;
  - tay xa và tay cầm kiếm nằm sau thân (vai không lộ cục tròn), nắm tay và kiếm trước thân.
- **Dựng** `ArtGen/Spine/rong_giot_build.py`: xương `root → move (cú lao, cú nhảy) → core (tâm thân: lộn, xoay, thu nhỏ) → hip →
  body → chest (chỉ mảnh thân: thở, dẹp giãn)`, đầu/tay/cánh/đuôi con của body, chân con của hip, `shadow` con của move (theo cú
  lao, dời ngược độ cao khi nhảy). **Không dùng noScale** khi có clip thu nhỏ cả con: noScale giữ nguyên cỡ đầu, tay. Hiệu ứng là
  slot riêng dùng lại 8 ảnh FX dòng Giọt Sương (`ArtGen/Heroes/inbox/giot_suong_fx/tai_ve`), lưu nhỏ trong atlas rồi phóng bằng
  cỡ attachment; xương hiệu ứng là con của move (không theo core). Cỡ rig: dáng đứng 340 điểm (sticker vẽ tối đa ~301).
  Ra `inbox/rong_giot/rig/` (`khung.png`, `anim_*.gif`, `xuong.png`, `<mã>_game.json`), `.atomik` và chân dung (khung 4:5, chân
  cách đáy 6%, lưu vuông 512, không bóng) vào `Assets/03 Art/Heroes/Resources/rong_giot/`.
- **Clip** tên chữ trong file, `AolaActor` đổi: idle (1_1), hit (1_2), attack (1_4), cast (1_5), skill (1_6), evolve. Khung 0 mọi
  clip là dáng nghỉ. Khung trúng khai trong `game.hitTimes`; cú lao đo trên xương `move` (attack luôn lao, clip khác khai `lunge`);
  đỉnh lao phải là lúc chém (độ dời x lúc chém lớn hơn độ cao lúc nhảy, vì trận xoay cả quỹ đạo cho đỉnh trỏ vào đối thủ); chỗ
  bắn tia = mũi kiếm ở khung trúng của cast (`muzzle`).
- **Unity**:
  - `AolaAnim.atomik` trỏ rig; `AolaActor.Load` thấy atomik thì vẽ một Mesh bằng `AtomikPose`, trả `FrameCount`, `HitFrame`,
    `Disp`, `Lunges`, `Beam` theo `game`, nên trận, sticker, hộp chi tiết, đội hình chạy như dạng aola;
  - `heroes.json` đổi `aola` của dạng sang tên thư mục (`rong_giot`), menu `PokiClash/Nhập dữ liệu`, rồi
    `PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng` (Editor/AtomikForms: dựng `<dạng>.asset`, cập nhật prefab tướng). **Không
    chạy menu nhập aola thường** để gắn (nó nhập lại dạng aola từ AolaRipper máy này); menu đó bỏ qua dạng có atomik;
  - `HeroViewer`: dạng cũ có clip `evolve` thì đổi dạng phát clip đó trên sticker cũ, giữ khung cuối tới khi sticker dạng mới xong,
    clip gọi trong lúc đó chạy sau;
  - soi: `PokiClash/Tướng/Chụp thử dạng .atomik (mọi clip)` (Library/PokiHeroShots/<id>_atomik_<dạng>.png, Editor.log in khung
    trúng, đỉnh lao, chỗ bắn tia), tour `PokiClash/Thử/Giọt Sương ra trận...` và `PokiClash/Thử/Giọt Sương tiến hóa...` (đang Play
    từ Boot, ảnh Temp/PokiShots/gs_combat, gs_tien_hoa).
- Máy không có repo `spine-animation-ai`: `rig.py` tự dùng `spine_compat.py` (`_convert_timeline`, `pack` viết lại, cùng cách dùng).
- Rồng Giọt (mảnh cứng, xoay cả người, khoá thưa) bị người dùng chê: thay bằng Thủy Long, mục 11.

## 11. Thủy Long: rig lưới trọng số, animation mềm, tiến hóa nối liền (2026-11-08, cách làm chuẩn cho tướng .atomik)

Người dùng dặn: animation mềm, hạn chế xoay cả người, để ý tiểu tiết, rig xương kỹ, tiến hóa phải hiện ra dạng sau (không giật);
đổi sang Spine là để mượt, không làm kiểu cũ. Tướng: long chiến binh 3 dạng, chiến, không cute.
- **Gói prompt** `ArtGen/Spine/build_thuy_long.py`: concept dạng k đính concept đã duyệt các dạng trước; 3 tờ mảnh (A: đầu liền cổ,
  đầu nhắm mắt, đầu gầm, mào; B: **tay, chân vẽ liền cả chi** từ vai tới cổ tay, hông tới cổ chân + nắm tay, bàn chân; C: thân, đuôi,
  áo choàng, vũ khí, giáp vai, vải trước).
- **Khớp mảnh vào concept** (`thuy_long.py place k`): so khớp màu tự do lệch về mảnh nhỏ (chuẩn hoá theo diện tích, mảnh nhỏ lọt
  vào vùng xanh trơn), nên: mảnh gọn có nét riêng dò ±12% quanh **tỉ lệ ước theo khung bao** (`HINT` x, y, ô, tỉ lệ); mảnh dài xanh trơn
  (tay, chân, vũ khí) đặt theo **hai đầu khớp đọc trên concept** (`TWO`: hai đầu đường dài nhất trong mảnh, bỏ phần đầu tròn);
  mảnh vẽ khác concept (mào, vải, áo choàng) đặt tay (`FIXED`). Soi `rig/so_ghep.png`.
- Sau khi cắt: `fix_grip` (tô lòng nắm tay), `fix_stubs` (GPT tô đầu tròn khớp xanh nhạt, ghép lộ chấm nhạt ở mắt cá: tô khối
  tròn nhạt gọn về màu da).
- **Rig** (`longrig.py`, `thuy_long.build_rig`): lưng 3 đốt, cổ + đầu 2 đốt (mặt nhắm mắt, mặt gầm lấy trọng số theo bản đồ của
  đầu chính), mào 3, tay 2 đoạn + nắm tay cứng, chân 2 đoạn + bàn chân cứng (IK), đuôi 4, vải 3, áo choàng 4, giáp vai cứng trên
  cánh tay trên, vũ khí cứng trên bàn tay. Mảnh chuỗi: geodesic từ đầu khớp chia đều n đoạn, trọng số hoà quanh khớp, đoạn đầu
  hoà nửa vào xương cha (vai, hông mềm). Soi `rig/luoi.png` (lưới, màu trọng số, xương).
- **Animation** viết bằng hàm thời gian (`curve` khoá có đường cong), nướng 30 khung/giây: chân giải IK (bàn chân bám đất, bước
  lao có nhấc cong); chuỗi mềm chạy lò xo đuổi theo dáng động học (độ cứng giảm ra ngọn; vải cứng hơn đuôi kẻo bay ngang như cờ);
  khoá dày lược RDP. Mọi dao động idle bằng 0 ở t = 0. Không xoay cả người: cong lưng chia 3 đốt (`bend`), dời hông, bước chân.
  **Vũ khí theo góc thế giới** (`aim`: tự tính góc cổ tay): giơ vũ khí lệch sang phải đầu, không dựng trước mặt (đại đao tay cầm
  giữa ngực phải giơ cánh tay ít hơn, đao nghiêng phải). Hiệu ứng: `fx_on` (hiện, đậm dần, tan dần), cột nước = ảnh tia nước xoay
  90°, lấp lánh và bong bóng gắn mũi vũ khí.
- **Tiến hóa nối liền**: rig dạng k gộp rig dạng k+1 (`merge_next`, xương `n_` dưới xương `evo` co theo tỉ lệ chiều cao hai dạng,
  slot vẽ sau). Clip `evolve`: dạng k nện vũ khí, nước dâng lốc, đổi dạng ngắn (0,3 s) lúc lốc phía trước đậm nhất, dạng sau lớn dần,
  nước vỡ, gầm, rồi `post` hoà về đúng khung đầu clip idle dạng sau. Các clip trận trên rig gộp ẩn slot `n_`. HeroViewer giữ khung
  cuối tới khi sticker dạng mới xong: hai hình trùng khít nên không giật.
- **Game**: `AolaActor.ShowTime` vẽ .atomik theo thời gian liên tục (60 khung/giây màn hình), hình aola vẫn theo bậc 25 khung.
- Lệnh: `D:/spine-venv/Scripts/python -I ArtGen/Spine/thuy_long.py cut k | place k [mảnh] | rig k | all | show k clip t1,t2 [follow]`
  (`show` dựng khung lớn từ `rig/baked.pkl`, khỏi nướng lại). `all` dựng dạng 3 trước (dạng k cần dạng k+1 cho tiến hóa).

## 12. Tướng .atomik từ MỘT ảnh liền (cách chuẩn từ 2026-11-08 sáng: Thủy Long sửa lỗi, Tám Tay)

Người dùng chê bản ghép tờ mảnh (mục 11): lỗi nhiều (khe trắng giữa đầu, mào, cổ; nắm tay vẽ lệch; viền sticker thắt vòng), dặn
"không cần tách nhiều bộ phận, gen liền cũng được". Từ đây **chỉ gen concept trọn con một ảnh**, rig thẳng từ ảnh đó.
- **Ảnh**: dáng rig được (mục 1): tay chân tách thân, chân không chéo, **vũ khí không vắt qua người** (vũ khí dài dựng bên phải
  người), không đường đất. Gói prompt mẫu: `build_tam_tay.py` (tướng mới, đính Thủy Long dạng 1 làm mốc nét), `build_thuy_long.py
  luot_1_lien` (vẽ lại concept đã duyệt, chỉ đổi tư thế).
- **Bộ dựng chung** `ArtGen/Spine/thuy_long_lien.py` (tướng khác cấu hình lại như `tam_tay.py`: `CFG`, `LAYERS`, `JD`, `MARKD`,
  `OVERRIDE`, `CLAMP`, `CHAINS`, `PARENT`, `LINEAR_Y`, `FULL_SHEET`, `WARM_FIX`):
  - nền: trắng nối mép ảnh; xoá nét đất mảnh (trên dưới đều trắng); khe trắng kín > 3000 px là nền;
  - **vùng từng phần**: loang đều 1 px mỗi bước từ hạt giống trong vùng màu, **nét mực (độ sáng TB < 72) là tường**; watershed
    loang dọc theo nét mực nên kéo viền chân theo vải (đã bỏ). Hạt giống: mảnh khớp cũ co 8 px (nếu có) hoặc đường xương / đa
    giác kẻ tay đọc trên ảnh kẻ lưới (`JD` khớp, `MARKD` hạt giống). Pixel chưa có nhãn lấy **nhãn gần nhất**
    (`fill_nearest`, đừng giãn ảnh lấy nhãn số lớn: xúc tu này nuốt xúc tu kia). Lọc đa số 7x7, bỏ mẩu < 500 px; `OVERRIDE` ép
    vùng, `CLAMP` giới hạn phần trong đa giác (vải ăn sang dải chân thì khi vải bay kéo theo dải chân);
  - **ít lớp** (sau → trước), ví dụ: đuôi, tay sau, chân sau, chân trước, mào/bờm (lớp riêng: chung lưới với đầu thì mào lắc xé gáy),
    thân + đầu (Tám Tay: đầu lớp riêng vì râu xúc tu buông trước ngực), vải, tay trước + vũ khí + giáp vai. Áo choàng lộ rời rạc:
    dựng **cả tấm** (bao lồi ∩ hình), phần khuất lát vân sáp thật của áo choàng;
  - lớp dưới **mọc thêm** n px dưới các lớp trên, vẽ bù từ màu chính lớp (TELEA), mép mượt, kẻ nét mực dọc mép (lúc nghỉ khuất);
  - trọng số: phần chuỗi theo khoảng cách đi trong hình từ khớp đầu, khớp giữa lấy đúng khớp kẻ (`chain_w`), hoà quanh khớp và vào
    xương cha; phần cứng (nắm tay, bàn chân, vũ khí, giáp vai) 100% một xương hoặc chia (giáp vai to: 65% ngực);
  - súng, pháo: góc vũ khí theo **trục nòng** (`JD[k]["axis"]`), không theo tay cầm → miệng nòng, kẻo tia nước bay chếch.
- **Lò xo**: mào/bờm dài và áo choàng cứng hơn và giới hạn góc văng (`maxang` trong `longrig.Springs`), kẻo bờm văng ngang thành dải.
- **Soi** (bắt buộc): `rig_lien/nhan.png` (bản đồ vùng trên ảnh), `lop.png` (từng lớp, dải vẽ bù), khung lớn `show` ở các pha
  nhanh nhất (lao, bắn, trúng đòn): tìm sợi viền bị lớp khác kéo theo, mẩu vũ khí dính chân, mảng vẽ bù lộ ra.
- Clip dùng chung tên xương nên tướng thiếu mào, vải, áo choàng vẫn chạy: `clean()` bỏ khoá của xương, slot, hình không có.
- Lệnh: `D:/spine-venv/Scripts/python -I ArtGen/Spine/thuy_long_lien.py nhan k | rig k | all | show k clip t1,t2 [follow]`;
  Tám Tay `ArtGen/Spine/tam_tay.py` cùng lệnh (`all` dựng dạng 2 trước).
- Unity: `heroes.json` đổi `aola` của dạng, menu `PokiClash/Nhập dữ liệu`, `PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng`.
  Nạp lại `.atomik` khi Editor đang Play: `AtomikPose.Stale` báo, `AolaActor` dựng lại (trước đó văng IndexOutOfRange mỗi khung).

## 13. Thú huyền thoại rig đơn giản kiểu Clash of Critters (đảo Thủy, 2026-11-08 chiều)

Người dùng dặn:
- thú huyền thoại hơi chibi kiểu Pokémon, style cũ (bút mực, sáp màu, tô phẳng);
- dạng sau dữ hơn nhưng không quá; hạn chế dạng người;
- animation đơn giản, ít khớp, hiệu ứng bù vào; càng gần boss cuối càng đẹp.

Các bước:
- **Concept:** `ArtGen/Spine/build_beasts.py [id]`. Ảnh 1536x1024, ảnh mẫu nét là 2 concept chibi đã duyệt cùng bản đồ thế giới. Dạng k > 1 đính ảnh các dạng trước. Gen bằng `gen.py`; dạng chưa có ảnh dạng trước thì chưa dựng.
- **Rig:** `beast.py <id> grid|nhan|rig|all|show <k>`, cấu hình từng dạng ở `beasts_cfg.py`.
  - Xương: root, move (lao, nhảy), shadow, ground (bàn chân bám đất), base (ở đất: nghiêng, nén giãn), body (một khối), head (cứng), phụ kiện cứng (`ear*`, `wing*`, `claw*`, `arm*`, `bell*`, `tuft*`), đuôi một chuỗi 1-3 đốt.
  - Chân (phần tên `leg*`): nửa trên theo body, bàn chân theo ground, chân tự giãn, co; không IK.
  - Đầu liền thân (chim, cá mập) dùng kind `("soft", "body", "head", p0, p1)`.
  - Đạo cụ cứng theo xương tay: `("rigid", "arm_f")`.
- **Clip:** khoá tay, không lò xo. Chuyển động phụ (đuôi, tai, chuông) trễ, ngược chiều độ nghiêng thân.
  - idle 2 s: nhún nén 3%, đuôi trễ từng đốt, tai ngược pha, một cú giật tai.
  - Đòn đánh kiểu lao (pounce, ram, bite, claw, smack, slam): lao 0,55H, trận kéo tới 72% quãng.
  - Đòn đánh kiểu xa (song, breath, roar): dời dưới 0,2H, trận tự nhún tới.
  - Mọi đòn: lấy đà 0,3 s, ra đòn 0,12 s, khựng 0,1 s.
  - cast: tụ cầu ở miệng (điểm `mouth` là chỗ bắn tia).
  - skill leap, dash hoặc summon: cả ba đều lướt tới để hiệu ứng lớn rơi đúng chỗ đối thủ. Phải có `lunge: ["skill"]`.
  - evolve: lốc nước, đổi dạng, khung cuối khớp idle dạng sau.
- **Hiệu ứng:** `build_fx_beasts.py`, tờ 1536x1024 chia lưới 3x2 ô 512 px, mỗi ô một hình. `--cat` cắt theo ô ra `inbox/fx/<id>_<tên>.png`.
  - Gắn qua `"fx"` của tướng: `fx_hit`, `fx_hit2` (đòn), `fx_orb`, `fx_charge` (cast), `fx_big` (`"up"` là đáy ở đất), `fx_big2`, `fx_wave`, `fx_ground`, `fx_p` (hạt văng `burst()` có biến thiên).
  - `skill_fx.drop` cho vật rơi từ trên (chuông, tảng băng).
  - Boss cuối thêm tờ thứ hai (`<id>_b`).
- **pixelfx** (`D:/_ref/pixelfx`) là pixel art có lớp sáng cộng dồn. Chỉ học cách diễn: đà ngược chiều, khựng lúc chạm, hạt nhanh vào chậm ra rồi tan. Không lấy glow, luật game vẫn tô phẳng.
- **Bẫy đã gặp:**
  - mảng trắng khép kín lớn (tròng mắt, lông kem, ngọc trai) bị `Q.load` coi là khe nền. `beast.load` trả lỗ về hình nếu có vân hoặc ngả màu (giấy trắng thật là ~254, không vân). `keep`, `drop` ép tay.
  - lưới `mesh_mask` chỉ lấy viền ngoài nên bỏ trống vùng có lỗ (dây đàn mất). Lưới phải dựng trên hình đã lấp lỗ, độ trong của ảnh vẫn giữ khe.
  - tai, đuôi xoay cùng chiều thân làm văng quá đà. Chuyển động phụ phải ngược chiều, trễ.
  - hạt giống chân đặt sát bụng làm chân ăn mất bụng: đặt thấp, gần bàn chân.

## 15. Một lưới liền, chiêu đa dạng (2026-11-09, cách chuẩn từ nay, thay mục 14)

Người dùng chê bản ghép lớp (mục 13, 14) lỗi nhiều: vệt khe, cắt cụt, đuôi nứt. Dặn gen một con nguyên chân tay đuôi, chỉ tách vũ khí, cánh khi thật cần; chiêu không được toàn "nhảy lên rồi ra chiêu".

- **Rig:** `beast.py` có `ONE = True`.
  - Cả con là MỘT lưới (lớp `main`). Trọng số mỗi đỉnh là tổng có trọng của các vùng theo độ thuộc vùng (`membership`: lan 3x3 chỉ trong hình, dải hoà `BLEND` px). Cấu hình vùng, khớp vẫn ở `beasts_cfg.py` như mục 13.
  - Khe giấy trắng giữa hai bộ phận (`drop_gaps`) thành trong suốt, lưới vẫn phủ qua (cắt lưới theo khe làm gốc đuôi rách răng cưa).
  - Đầu xoay nhân `HEADK` 0,55; đuôi idle nhân 0,6; gốc chuỗi hoà vào cha tới 30% chiều dài.
  - Lưới chỉ lấp lỗ nhỏ (`fill_small_holes`, dưới 0,006·H² px rig); khoảng trống lớn (giữa đuôi và thân) để trống, kẻo đuôi lắc kéo tam giác thành vệt sọc. Đàn có dây mảnh giữa các lỗ khai `"mesh_fill": "all"` (Mi Nhi).
  - `cut_gaps`: bỏ tam giác vắt qua chỗ trong suốt mà các đỉnh thuộc hai bộ phận khác hẳn nhau (độ giống trọng số < 0,5), như chóp đuôi sát móng vuốt.
  - Phần trong `"sep"` của dạng thành lớp riêng sau/trước (mọc thêm, loang màu như cũ). Chỉ dùng khi vũ khí, cánh che thân mà phải cử động mạnh.
- **Xương:**
  - `spin` giữa thân (cha của `ground` và `base`): lăn, lật quất đuôi, trượt bụng.
  - `paw`: chân trước (tự chọn `leg_fn`/`leg_f`, khai `"paw"` được) xoay cả chân quanh vai, vẽ trên cùng (đá, vồ quét qua trước vải, thân; lúc đứng không chồng nên không đổi hình).
  - `flyp_<đồ>` (khai `"throw"`): đồ bay ném được, con của `move`.
  - `far` (con của root, dáng gốc trước mặt 0,9H, cao 0,45H), `fp*` hạt, `fly0..4` đạn từ miệng, `flyw` sóng đất.
- **Game:** `game.far` liệt kê clip có hiệu ứng ở xa. `AolaActor.FarAtomik` dời `far` tới tâm thân đối thủ và `fly*` theo quãng đã bay (x so với chỗ xuất phát). Clip đánh xa phải dời `move` dưới 0,15H để trận không coi là lao.
- **Kiểu đòn** (`attack`, theo dạng được): `bite`, `ram`, `claw`, `smash`, `swipe`, `punch`, `kick`, `tailwhip`, `spin`, `song`, `breath`, `roar`, `throw`.
- **Kiểu chiêu cuối** (`skill`): `erupt`, `storm`, `barrage`, `summon_prop`, `shockwave` (đứng tại chỗ, `far`); `charge`, `spin_dash`, `slide`, `combo` (lao, `lunge`). `motion` chọn dáng tụ lực: `stomp`, `roar`, `howl`, `claws`, `wings`, `rear`.
- `game_info` tự tính `lunge`, `far` theo kiểu. Vòng tụ lực kiểu mới chỉ vòng sau, nhạt, không khiên (khiên, vòng trước che kín dáng).
- **Soi:** nền xám (`render(..., bg=(150,150,150))`) để thấy vệt trắng, chỗ hở. Soi khung lúc xoay, lật, trượt và lúc đuôi lắc mạnh nhất.

## 16. Đảo Hỏa: tướng mới từ chữ tới game trong một buổi (2026-11-09, máy ổ E)

Cách mục 15 áp cho 10 dòng, 28 dạng chưa có concept nào (QUY_TRINH mục 19):
- **Gói prompt** `build_hoa.py`: thiết kế chữ (giữ chủ đề dòng aola, mỗi dòng một bảng màu), ảnh mẫu là ảnh liền đã vào game theo kiểu
  dáng (`POSE_REF`; tránh ảnh mẫu cùng loài kẻo Codex chép), luật lửa `FLAMES` (viền khép kín, tối đa 3 dải, không phát sáng,
  không tàn bay). Dạng k chỉ dựng khi đã có ảnh dạng k-1.
- **Cấu hình** riêng một file `beasts_cfg_hoa.py` (nạp cuối `beasts_cfg.py`); hàm `_fx` đặt bộ hiệu ứng lửa thay bộ nước mặc định
  (vòng dưới chân, lốc tụ lực/tiến hóa chỉ vòng sau, sóng cuối chiêu, hạt). Mỗi dạng: soi `nhan.png`, sửa hạt giống chỗ lẹm (sừng mũ
  bị tính vào mào, gốc tai bị tính vào đầu) rồi mới dựng.
- **Hiệu ứng** tờ 3x2 như mục 13; ảnh hình vòng khai trong `HOLLOW` của `build_fx_beasts.py` để xoá lòng giấy trắng khép kín.
- **Dựng thử không đụng Assets:** vá `thuy_long.RES` sang scratchpad (và `fx_img` thay ảnh thiếu bằng FX03) để soi `khung.png`,
  tiến hóa (`show <k> evolve ...`) trước khi có đủ hiệu ứng, rồi chép `Resources/<dạng>/` vào Assets một lần khi Unity rảnh.
- **Gen dài**: `chay_hoa.py <prompt ...>` chạy tách (Start-Process), bỏ qua file đã có ảnh. Lệnh nền của phiên bị ngắt vẫn sống:
  kiểm tiến trình `gen.py` trước khi chạy lại kẻo gen trùng.
- `AtomikForms.Attach` tự dựng prefab cho tướng chỉ có dạng .atomik (chưa từng có hình aola) và thêm vào HeroModels.

## 17. Rồng rắn uốn lượn, mây bay vòng, dạng sau "chiến" (Thanh Long, 2026-11-09 tối)

Người dùng dặn: mây quanh rồng phải bay xung quanh; thêm xương cho thân rồng mềm mại, uốn lượn; dạng 2, 3 chưa đủ chiến, chibi chỉ
ở dạng 1. Học từ aola 1749 (mây nước nhiều cụm chảy vòng trước, sau thân liên tục) và Critters (skill `pokiclash-hero-fx` mục 1b).
- **Concept dạng sau:** `build_thanh_long_chien.py` (ảnh mẫu: dạng 1 lấy nét, một tướng Hỏa dữ lấy thần thái, dạng hiện tại lấy màu,
  bản đồ). Tỉ lệ trưởng thành: đầu chỉ ~1/4 chiều cao, mắt xếch đồng tử dọc, nanh, móng giương; thân rắn chữ S nằm ngang, chân
  tách thân, **không vẽ mây**. Dạng khai `"src": "tai_ve/L1_chien.png"` (`beast.src`) để không đè `L1_duyet.png` cũ.
- **Mây bay vòng = clip lặp `aura`** (không khoá trong clip trận: đổi clip là mây giật về chỗ cũ):
  - ảnh mây cắt từ concept cũ bằng `cat_may.py` → `inbox/fx/thanh_long_may<k>_<i>.png`; mây vẽ sẵn trong ảnh dạng 1 bỏ khỏi lưới
    bằng `"erase": [(x, y)...]` (bỏ cả mảng liền chứa điểm);
  - `"orbit"` (theo dạng): `clouds` [(ảnh, cỡ theo H, đuôi mây "r"/"l")], `period` 8 s, `ph` (lệch pha đầu, tránh mây nằm đúng điểm
    quay đầu lúc giây 0), `rx` (theo bề dài con), `ry`, `cy`, `depth`;
  - mỗi cụm một xương `jo<i>` (con của move) hai slot `jo<i>b` (sau thân, nửa vòng xa) / `jo<i>f` (trước thân, nửa vòng gần), mặc định
    trống; aura bật hình theo nửa vòng. Hai đầu vòng mây lật ngang qua bề rộng ~0 (như xoay trong không gian), đổi slot đúng lúc đó
    nên không lộ chỗ nối; đuôi mây luôn kéo sau hướng bay;
  - runtime `AtomikPose.Overlay(ci, t)` phủ clip `aura` lên clip chính (xương cộng, hình theo khoá, độ đậm nhân); `AolaActor` chạy
    theo `Time.time` (liền qua mọi clip; Editor không Play thì đứng ở giây 0), `AtomikPlayer` theo đồng hồ riêng. Rig gộp tiến hóa:
    mây dạng sau (`n_jo*`) ẩn bằng độ đậm 0 ở clip trận, hiện cùng dạng sau trong `evolve`; mây dạng cũ tan cùng dạng cũ;
  - bản soi (`khung.png`, GIF, `baked.pkl` của `show`) đã ghép aura cùng giây như runtime (`beast.with_aura`).
- **Thân rắn nhiều xương** (`beast.serpent_clip`): xương `body` ở giữa thân; chuỗi `body` (nửa trước, `fw1..3`) từ giữa lên cổ, chuỗi
  `back` (nửa sau, `bk1..3`) từ giữa về hông, đuôi 4 đốt, bờm là chuỗi riêng `hair1..2` (tên `hair`, đừng đặt `mane*`: bị cả vòng tai
  lẫn vòng đuôi lắc chồng). Chuỗi đo khoảng cách từ xương đầu chuỗi trong vùng của nó, nên gốc chuỗi phải ở **một đầu** vùng (đặt ở
  giữa vùng thì phía bên kia bị tính như ngọn chuỗi). `"parent"`: đầu theo `fw3`, chân trước theo `fw2/fw3`, chân sau theo `bk2/bk3`.
  - `"spine": {"bones": [đầu ... chóp đuôi], "amp": [...], "coil_neck/back/tail", "paddle"}`: sóng chạy từ đầu xuống đuôi (pha tăng
    0,8 mỗi đốt, biên độ tăng ra đuôi); "nâng" dương = đầu xa thân nhấc lên (tự đổi dấu theo hướng xương); đầu xoay bù 80% góc cổ (mắt
    vẫn nhìn đối thủ); chân bơi lệch pha. Clip không lặp chạy số vòng sóng nguyên, biên độ riêng hoà vào/ra hai đầu clip nên khớp
    khung 0 idle. Dáng cuộn - bung theo nhịp đòn: attack/cast cuộn lấy đà rồi bung lúc nhả đạn; skill chồm cổ cao, bung khi sét giáng;
    hit cuộn chữ C ngược; idle 4 s = 2 vòng sóng. Xương thuộc spine bị loại khỏi `tail_bones` (khỏi lắc chồng).
- **Con dài dẹt:** game co tướng theo `game.height` nên rồng dài ~2 lần cao lòi khỏi mép sân. `"max_w": 1.42` (tỉ lệ rộng/cao tối đa)
  → khai chiều cao lớn hơn cho con vẽ nhỏ lại; tiến hóa dùng chiều cao hiệu dụng nên không giật cỡ.
- Soi: `dung_thu.py` (scratchpad, vá `thuy_long.RES`) dựng không đụng Assets; tour `PokiClash/Thử/Đảo Mộc: Thanh Long ra trận ở 3 dạng`
  (đang Play, ảnh `Temp/PokiShots/thanh_long_combat`) thấy mây bay thật.
- **Dạng cuối phải khác hẳn dạng trước** (người dùng: "dạng 2 và 3 chưa khác nhau lắm"): đổi cả màu (xanh lam đậm thay ngọc lam), thêm
  giáp, đồ (ngọc sấm), đổi chi tiết (râu, chóp đuôi hình tia sét) và **đổi dáng** (chồm dựng chữ S thay vì nằm ngang): nhìn bóng dáng
  đã biết là con khác. Gói `build_thanh_long_chien.py b3` → `tai_ve/L1_chien_b.png`. Dáng dựng hẹp (rộng/cao ~1,3) nên khỏi co.
- **Bờm, râu nhiều xương có lò xo** (người dùng: "thêm xương vào tóc cho mềm mại hơn"): bờm 3–4 đốt, râu 2–3 đốt; khoá `"soft"`
  (`beast.springs_of` → `longrig.Springs`: đuổi theo dáng động học, trễ, vượt nhẹ; `k` từng đốt 380 → 180, `damp` 0,6, `maxang` 10°;
  mềm hơn nữa thì lúc đánh lộ phần vẽ bù). Bờm chung lưới với sừng thì lò xo kéo nhoè sừng: tách `"sep": {"hair": "back", "rau":
  "front"}` (bờm lớp sau đầu, sừng đè lên; râu lớp trước), `"sep_grow": 24` (bờm vẽ bù dưới đầu), `"main_grow": 14–16` (lưới chính vẽ
  bù dưới râu, râu lắc không lộ lỗ). Hạt giống bờm đừng chạm lông gáy (nhãn gần nhất kéo cả mảng lông sau đầu vào bờm).
- **Hạt lá không viền sticker** (người dùng: "bỏ shader viền trắng ở các particle lá"): `beast.plain_slots` khai `game.plain` = slot
  hiệu ứng vẽ trước thân có ảnh lá (`leaf`/`leaves`). Runtime: `AolaActor.SplitFx` (AolaSticker bật) dựng các slot đó thành lưới riêng
  đặt cao `FxLift` 1000 trên actor; `AolaSticker.MakeFxLayer` thêm camera, RT, ảnh con cùng khung, shader `StickerOutline` với
  `_Plain = 1` (không viền). Slot sau thân giữ chung ảnh có viền (tách ra thì bị vẽ đè lên thân). Đã dựng lại Tiên Lá, Thỏ Hoàng,
  Mộc Tinh để có danh sách này. Chụp thử trong Editor (`AtomikForms.Shot`) không bật SplitFx nên vẫn một lưới như cũ.
- **Chiêu mỗi dạng một khác, dạng sau dữ hơn** (người dùng: "chiêu của dạng 1, 2, 3 đang giống nhau... càng dạng sau chiêu sét
  càng dữ dội, càng to"): `beast.form_cfg` cho khoá `"<tên>_form": {dạng: ...}` trong `juice` đè khoá chung (dict trộn, còn lại
  thay): `lightning_form`, `impact_form`, `phys_form`, `phys_pre_form`; `"motion"` theo dạng (`{1: "claws", 2: "roar", 3: "rear"}`).
  Tham số sét mới: `w_main`/`w_pre` (dày nét), `br_main`/`br_pre` (số nhánh), `wide_main` (bề ngang ảnh nhát chính), `main_scale`,
  `main_hold` (khung giữ thêm của cột sét), `clouds` [(dx, cỡ)], `cloud_stay`, `caster_r`/`caster_size`, `ring_pre`/`ring_main`,
  `dur`, `t_up`, `hit`, `seed`, `up` (tia bắn ngược lên trời từ ngọc: `bone`, `at` điểm trên ảnh concept, `height`, `win`; clip có
  `post` bù góc thế giới để tia luôn dựng đứng). Thanh Long: dạng 1 một tia mảnh, một mây nhỏ (1,7 s); dạng 2 ba nhát, hai mây (2 s);
  dạng 3 ngọc bắn tia lên trời, ba mây giông, năm nhát dồn dập rồi cột sét dày gần gấp đôi, 7 nhánh, giữ thêm 12 khung, khựng 0,2 s,
  rung 1,0, chớp màn mạnh, 24 hạt lá đất (2,5 s). Tướng nhiều nhát sét làm .atomik nặng hơn (mỗi nhát 5–8 ảnh tia).

## 18. Chiêu đa dạng theo dạng, đứng một chỗ bắn, há miệng (cả 3 đảo, 2026-11-09 tối)

Người dùng chê chiêu "một màu, toàn lao lên húc rồi lộn", dặn sáng tạo hơn (lore, Pokémon), đòn bắn xa đứng một chỗ, bắn từ mồm
thì há mồm. Đã áp cho 29 dòng Thủy, Mộc, Hỏa (Kim do phiên khác làm):
- **Kiểu chiêu đứng tại chỗ mới** (`beast.py`, cùng `FAR_SKILL`): `beam` (đạn nối đuôi thành dòng từ miệng, chỗ trúng chớp liên
  hồi), `vortex` (vòng xoáy dưới chân đối thủ quay nhanh dần, cột xoáy, hạt bay vòng, nổ cuối), `rain` (từng viên rơi chéo quanh
  đối thủ; dạng cuối thêm khối lớn rơi), `nova` (vòng bùng quanh thân theo nhịp + sóng đất tới đối thủ), `orbit` (đạn hiện ra bay
  vòng quanh thân rồi phóng lần lượt), `line_erupt` (cột trồi nối nhau dọc đất tới đối thủ, slot `fll*` trên xương `flyl*`: game
  dời theo quãng như đạn `fly*`). Độ mạnh `power_of`: dạng 1 = 1, dạng cuối = 3 (số viên, cỡ, độ dài, nổ cuối tăng theo).
- **Bảng đòn/chiêu từng dạng**: khối `_REDESIGN` trong `beasts_cfg.py` (giữa phần Hỏa và phần Kim), ghi ý lore/Pokémon từng dòng.
  Còn 9/72 dạng chiêu lao (dê, bò, cuộn giáp, cánh cụt trượt bụng, liên hoàn vuốt ở dạng 1). Đòn "lộn" (spin, tailwhip) đã bỏ.
- **Cảm giác trúng mặc định theo dạng** (`game_info`, tướng không khai `impact`): khựng, rung, bật lùi tăng theo dạng, dạng cuối chớp
  màn.
- **Đứng một chỗ bắn**: `attack_range` chỉ giật lùi; trận (`StageView`) không tự nhún tới đối thủ với clip `far`/`stay` của rig
  .atomik (`AolaActor.Stays`, `AolaSticker.Stays`). Trước đó đòn đánh không khai lao vẫn bị đẩy tới 35% quãng.
- **Há miệng**: vùng `jaw` + xương `jaw` ở góc miệng phía sau, `"jaw": {"open": độ}`; `beast.jaw_clip` há theo nhịp (đòn phun/hót/
  gầm, chiêu mana, chiêu gầm, trúng đòn), tiến hóa thì dạng sau há khi gầm. Gắn nhanh bằng `_add_jaw(id, dạng, đa giác, khớp, độ)`
  trong `beasts_cfg.py`. Bẫy: cằm không có nét mực ngăn với má thì hạt giống nhỏ không loang được (há thành khối vuông): đa giác
  phải **phủ trọn hàm dưới, cằm**; răng trắng giáp hàm và đầu bị coi là khe giấy (lỗ khi há): `drop_gaps` giữ khe giáp vùng `jaw`.
  Mỏ quặp khép kín (Phong Linh 2) bỏ qua. Điểm `mouth` cũ lệch (trên má, vây) thì sửa cho đạn ra đúng miệng.
- **Bẫy đã sửa 2026-11-10 (phiên Kim phát hiện):** `P.rot/scale/move` gọi theo **tên slot** mà slot nằm trên xương tên khác (đạn `fl*` trên
  `fly*`, vệt `jt*` trên `flyt*`, `fl_wave` trên `flyw`, `fll*` trên `flyl*`, và `ff_*` trước đây chung xương `far`) bị `Q.clean` bỏ
  khi xuất: đạn không xoay, không co giãn, hiệu ứng ở chỗ đối thủ đứng yên một cỡ, vật "rơi từ trời" không rơi. Nay
  `longrig.Pose.alias` (đặt trong `build_rig`) quy tên slot về xương riêng của nó, và mỗi `ff_*` có xương riêng con của `far` (vòng loang,
  hình đứng đặt ở đất). Viết clip mới: gọi theo tên xương hay tên slot đều được, trừ slot chung xương (`fx_ring_b/f` → `fx_ring`).

## 19. Đảo Kim: chibi chỉ dạng 1, thú mặc giáp (2026-11-09 tối, máy ổ D)

Cách mục 16 áp cho 10 dòng, 22 dạng (QUY_TRINH mục 20); gói `build_kim.py`, cấu hình `beasts_cfg_kim.py` (nạp cuối `beasts_cfg.py`).
- **Tỉ lệ theo dạng** (`STAGE` trong gói): dạng 1 chibi đầu khoảng 45%, dạng giữa 30%, dạng cuối 25%; ảnh mẫu dạng trước dặn "to,
  khỏe, ngầu hơn, đừng chép tỉ lệ thân". Ảnh ra vẫn chibi thì `gen.py --note "Not chibi at all ... head about one quarter"`.
- **Aola dạng robot, người lính** thì đổi thành thú mặc giáp giữ màu, chi tiết (nhím, tatu, cú, heo rừng, linh miêu).
- **Mặt nạ đồ trắng:** lông, chùm lông trắng gần màu giấy hở viền thì `close_fill` (x0, y0, x1, y1, r); viền giáp trắng khép kín bị
  thành lỗ thì `keep`; lòng bàn chân giữa các móng thì mỗi bàn một hộp r=14, đáy ngay trên mép bàn chân.
- **Chọn chi đánh:** chân không đặt tên `leg_f*` thì `limb(paw → arm_f → claw_f)` dùng càng (Bọ Cạp); `hover` đọc theo dạng
  (`style_of`), Chiến Thần chỉ dạng 2 bay.
- **Tờ hiệu ứng bị công cụ vẽ ảnh của Codex chặn** khi tả lưỡi thép, gai, giáo: tả bằng tấm kim loại, dải bạc, vệt cong, mảnh pha
  lê. Ảnh hiệu ứng chưa gen thì `_tam_thoi()` cuối `beasts_cfg_kim.py` tạm dùng ảnh tờ chung cùng vai trò (vào game được ngay).
- **Codex hết hạn mức** (`chay_hoa.log`: "usage limit", chờ 10 phút, thử lại mãi): báo người dùng giờ mở lại; runner tách
  (Start-Process) vẫn sống và tự gen khi có hạn mức.
- **Soát theo mục 0a, 18:** khối `_REDESIGN_KIM` trong `beasts_cfg_kim.py` (mỗi dạng một chiêu; 17/20 đứng tại chỗ). Kiểm bằng
  `<id>_game.json` của từng dạng (`far` / `lunge`). Trước 2026-11-10 lệnh xoay, co, dời theo tên slot (`fl*`, `ff_*`, `fll*`) bị bỏ
  (đạn không xoay, vật rơi không rơi); phiên khác đã sửa gốc (`Pose.alias`, mỗi `ff_*` một xương con của `far`), dựng lại là
  hưởng. Ảnh đạn dài phải chĩa sang phải (code xoay theo hướng bay). Tờ khung dạng chưa cuối có 6 hàng (thêm
  `evolve`), mỗi hàng 300 px: cắt hàng chiêu theo số hàng thật.

## 14. Gen bộ phận SAU khi rig (đảo Mộc, 2026-11-08 tối; đã bỏ, xem mục 15)

Người dùng dặn: gen một con hoàn chỉnh, rig xương, sau đó mới gen thêm bộ phận phục vụ animation. Lý do: loang màu phần bị che làm "ghép lệch".

Các bước:
1. **Concept:** đảo Mộc lấy theo concept đã duyệt của từng dạng (`ArtGen/Heroes/inbox/<id>_<k>/concept_duyet.png`), vẽ lại ở dáng rig được bằng `ArtGen/Spine/build_moc.py`. Dạng sau đính dạng trước (`L1_duyet.png` nếu Claude đã chọn bản gen lại).
2. **Rig:** cấu hình vùng, khớp ở `beasts_cfg.py`, soi `nhan.png`.
3. **Gen bộ phận:** `build_parts.py <id> <k>` sinh `gui_gpt/<mã>/duoi1.txt`, `duoi2.txt` kèm ảnh hướng dẫn (phần cần xoá tô hồng).
   - Lớp dưới 1: xoá mọi lớp trước thân, vẽ đủ thân.
   - Lớp dưới 2: xoá cả thân, vẽ đủ phần sau thân (chân xa, đuôi, cánh xa).
   - GPT vẽ trên đúng khung 1536x1024.
4. **Dựng:** `beast.py <id> all` tự lấy ảnh lớp dưới:
   - căn bằng ECC nhưng giữ "không dời" nếu căn không tốt hơn hẳn; dời quá 8 px thì bỏ phép căn; tương quan dưới 0,4 thì bỏ ảnh;
   - lớp thân dùng lớp dưới 1, các lớp sau thân dùng lớp dưới 2;
   - dải mọc thêm rộng gấp 3 lấy hình GPT; chỗ GPT bỏ trắng vẫn loang màu, nên không bao giờ hở.

Bẫy:
- Khe giấy trắng nhỏ (dưới 3000 px) giữa hai bộ phận thì `drop_gaps` bỏ khỏi hình. Lòng mắt, răng chỉ giáp một bộ phận nên giữ.
- Mây, bờm, chùm đuôi trắng viền hở: không lấp được bằng code (lấp ra khối vuông). Dặn GPT tô kem `#F4EEDC` hoặc xanh xám nhạt `#DDE9EE` và khép viền, rồi gen lại.
- Codex từ chối ảnh lớp dưới: gửi lại với `--note` ("harmless cartoon art edit of our own game character...").
- Con bay: `"hover": True` ở tướng, `"ground"` đặt dưới thân. Idle nhấp nhô, bóng co theo.
