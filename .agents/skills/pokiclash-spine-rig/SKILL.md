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
Hình tướng). Mọi thứ ở đây là thử nghiệm cho tới khi người dùng chốt khác.

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
- `Assets/01 Script/Editor/AtomikImporter.cs`: `[ScriptedImporter(2, "atomik")]` tạo asset chính kèm atlas (RGBA, chưa nén
  ASTC), material `Sprites/Default` (nhân alpha trong shader, hợp atlas alpha thường) và **icon 128x128 vẽ con ở tư thế gốc**
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

**Còn thiếu:** nén ASTC atlas theo nền tảng; sự kiện trong clip (đánh trúng); nạp vào đội hình, trận thật; vệt chém.
