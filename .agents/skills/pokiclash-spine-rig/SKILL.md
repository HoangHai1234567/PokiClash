---
name: pokiclash-spine-rig
description: >
  Rig xương Spine 4.2 và làm animation cho một nhân vật 2D từ ảnh (ảnh GPT vẽ hoặc một ảnh liền bất kỳ), thử nghiệm với repo
  spine-animation-ai: cắt mảnh, khớp vị trí, dựng xương, mảnh cứng hoặc một lưới có trọng số (uốn mềm, không hở khớp),
  viết animation (đứng, đánh, trúng đòn, chiêu, đi/chạy), dựng khung soi, GIF, trang Spine Web Player. Dùng khi người dùng
  muốn rig xương / làm animation Spine từ một hình, thử khả năng rig tự động, hoặc sửa hở khớp, uốn cong chi.
---

# Rig Spine từ ảnh (thử nghiệm)

Làm 2026-11-07 để đo khả năng rig tự động. **Không thay quy trình chính của game** (vẽ đè lên rig aola, xem CLAUDE.md mục
Hình tướng). Mọi thứ ở đây là thử nghiệm cho tới khi người dùng chốt khác.

## 0. Trước khi làm

- **Giấy phép:** code repo `spine-animation-ai` là PolyForm Noncommercial (không dùng thương mại). Đưa Spine vào Unity cần
  runtime `spine-unity`, runtime này đòi giấy phép Spine Editor. Nói rõ với người dùng trước khi tính chuyện đưa vào game. Nếu
  muốn dùng thật, phương án là nạp JSON vào bộ animation tự viết của game (AolaActor) thay vì runtime Spine.
- **Bản quyền ảnh:** ảnh lấy trên mạng (nhân vật của hãng khác) chỉ để thử. Để ngoài PokiWar, trong
  `<ProjectAtomik>/spine-animation-ai/work/<tên>/`. Không commit, không publish artifact.
- **Repo và Python:** repo clone cạnh PokiWar: `E:\ProjectAtomik\spine-animation-ai` (máy kia: clone cạnh project, hoặc đặt biến
  môi trường `SPINE_AI`). Có venv riêng: `.venv` với `opencv-python Pillow numpy`. Mọi lệnh dưới đây chạy bằng
  `<repo>/.venv/Scripts/python -I`. Không cần API key nào (bước Gemini của repo không dùng).
- Repo chỉ được dùng lại 3 thứ: `make_atlas.pack`, `build_spine_json._convert_timeline` (đổi khoá sang dạng 4.2), trình xem
  Spine Web Player. Bộ rig dáng người của repo không hợp con thú chibi; dùng công cụ của mình ở `ArtGen/Spine/`.

## 1. Chọn cách

| Cách | Khi nào | Lệnh |
|---|---|---|
| **A. GPT vẽ hình trọn con + tờ mảnh** | tướng mới, muốn mảnh sạch có đầu khớp tròn | `build.py` → `gen.py` → `rig.py all` |
| **B. Một ảnh liền, mảnh cứng** | ảnh có nét viền rõ (chibi), chuyển động nhẹ | `rig.py one1 <mã>` |
| **C. Một ảnh liền, một lưới có trọng số** | muốn khớp uốn mềm, không hở (khuyên dùng) | `mesh.py <mã>` |

Người dùng nghĩ "rig" là làm từ **một ảnh liền**: nếu họ đưa một ảnh, đi thẳng B/C, không bắt GPT vẽ tờ mảnh.

Ảnh dễ rig: đứng thẳng hoặc nghiêng nhẹ, tay chân tách khỏi thân, không chéo nhau, nền trắng. Dáng chữ T là dễ nhất.

## 2. Cách A: GPT vẽ (ArtGen/Spine)

- `build.py <mã>` sinh gói `ArtGen/Spine/gui_gpt/<mã>/`: `luot_1_tong.txt` (hình trọn con dáng dễ rig, 1024x1536) và
  `HUONG_DAN.md`. `luot_2_tach_manh.txt` (2 tờ: nhóm đầu, nhóm thân; mỗi mảnh vẽ đủ phần bị che, đầu khớp thừa ~30 px tròn,
  cách nhau ≥ 60 px) **chỉ sinh khi đã có** `inbox/<mã>/L1_duyet.png` (Claude chép ảnh lượt 1 đã duyệt về đó).
  File prompt theo luật ArtGen của CLAUDE.md (ảnh mẫu đường dẫn tuyệt đối, mục SAVE dạng `save it as a PNG to <path>` để
  `gen_codex.py` dò được chỗ lưu).
- `gen.py <file prompt>`: gọi Codex qua `ArtGen/Heroes/tools/gen_codex.py`, giữ chung khoá `ArtGen/Heroes/inbox/.codex.lock`
  với các lô tướng (chỉ một lệnh Codex mỗi lúc). Chạy nền.
  - Hết hạn mức: log lô khác ghi "hết hạn mức Codex". Hỏi giờ có lại bằng một lệnh nhỏ:
    `codex.exe exec --skip-git-repo-check -s read-only -- "Reply ok."` (đường dẫn exe trong `%TEMP%\pokiclash_codex_path.txt`),
    lỗi trả về có "try again at <giờ>". Báo người dùng, đừng chờ mù.
- `rig.py cut <mã>`: cắt tờ mảnh theo `SPEC[<mã>]["sheets"]` (hàng trên xuống, trái sang phải). Mẩu rời sát mảnh lớn (< 45 px)
  tự gộp. **Đếm sai số mảnh thì dừng**, in khung từng mảnh, không gán bừa tên.
- `rig.py place <mã>`: khớp từng mảnh vào ảnh trọn con (SQDIFF có mặt nạ trên Lab, dò tỉ lệ + góc + vị trí, 3 tầng phân giải).
  Mảnh lớn nhất mỗi tờ dò tỉ lệ cả tờ (0.35–2.8), mảnh khác dò quanh tỉ lệ đó; mảnh trái/phải giới hạn theo nửa người.
  Xuất `rig/so_ghep.png` (gốc | ghép | thiếu đỏ / thừa xanh) và IoU.
- `rig.py build <mã>`: khớp xương = tâm vùng giao giữa mảnh con và mảnh cha (đầu khớp thừa chồng lên nhau).

## 3. Cách B: một ảnh, mảnh cứng (`rig.py one1`)

Spec trong `rig.py` (mẫu `SPEC["snorlax"]`):
- `"base"`, `"src"`: thư mục làm và ảnh gốc. `"fg": (ngưỡng sáng, ngưỡng bão hoà)` cho mặt nạ nền. `"dark_thr"`: ngưỡng sáng
  chia lớp màu `dark`/`light` (để lọc theo màu).
- `"one"`: mỗi mảnh `{poly, excl, keep, minus, cap, cap_keep, inpaint}`, theo thứ tự:
  - `excl`: mảnh giành pixel trước (đầu → tay → thân); mảnh không excl (bụng, tai, chân) được chồng.
  - `keep: "light"/"dark"`: chỉ lấy pixel lớp màu đó (bụng kem, chân kem).
  - `minus`: đa giác trừ ra (chóp tai trừ khỏi đầu).
  - `cap: (mảnh cha, r)`: phần chồng lấn r px vào mảnh cha, mờ dần; `cap_keep` giới hạn theo màu lông.
  - `inpaint: "light"/"dark"`: vẽ bù pixel lớp màu đó trong mảnh (chỗ bị mảnh khác che), ví dụ thân sau bụng.
- `"draw"`: thứ tự vẽ sau → trước. `"root"`: gốc (giữa hai chân, mặt đất). `"bones"`: `(xương, cha, mảnh, (x, y) khớp)`.
- Chọn đa giác: kẻ lưới toạ độ lên ảnh (bước 20 px, phóng 2x) rồi đọc toạ độ; soi `so_ghep.png` sau mỗi lần cắt.

## 4. Cách C: một lưới có trọng số (`mesh.py`) — uốn mềm, không hở

- Lưới: điểm viền cách đều `step_edge` (đặt đầu danh sách = hull) + lưới điểm trong `step_in`, Delaunay (`cv2.Subdiv2D`),
  bỏ tam giác có trọng tâm hoặc trung điểm cạnh ra ngoài hình.
- Trọng số: `labels` = vùng của từng xương (đa giác + lọc màu, ưu tiên theo thứ tự). Mỗi xương
  `w = exp(-(khoảng cách tới vùng / sigma)^2)`, giữ 4 xương nặng nhất, chuẩn hoá. `sigma` ~13 px (bụng 22, đầu 10).
- Thứ tự vẽ tam giác theo `layer` của vùng (tai, chân → thân → bụng → đầu → tay), để tay đè lên bụng khi đập xuống.
- Thêm xương khuỷu (`hand_l/hand_r`) để tay cong được. Bụng có xương riêng để nảy phình.
- Xuất mesh Spine 4.2 có trọng số: `vertices = [số xương, (chỉ số xương, x, y theo xương, w)...]` mỗi đỉnh, `uvs` theo ảnh,
  `hull`, một slot gắn root. Kết cấu = ảnh gốc nền trong suốt.
- Soi `rig_mesh/luoi.png` (lưới + màu trọng số + khớp).
- Giới hạn: lưới chỉ kéo giãn ảnh có sẵn. Vai giơ quá ~50° cộng khuỷu ~25° là tay gập đè lên đầu; chỗ bị che không tự có hình.

## 5. Animation

- Viết trong hàm `<mã>_anims()` (rig.py) hoặc `ANIMS` (mesh.py). `tl([(t, góc, curve)])` cho **rotate**,
  `tl2([(t, x, y, curve)])` cho **translate/scale**. Dùng nhầm `tl` cho translate là sai cả JSON (lỗi đã gặp).
- `curve` gắn với đoạn **kết thúc** ở khoá đó: `E` êm hai đầu, `EO` bật nhanh rồi chậm (cú đánh trúng), `EI` chậm rồi nhanh
  (lấy đà lao vào), `None` thẳng. `_convert_timeline` đổi sang bezier tuyệt đối của 4.2.
- Xương setup không xoay (rotation 0). Góc dương = ngược kim (y lên). Tay trái người xem chĩa sang trái: góc âm là giơ lên;
  tay phải: góc dương là giơ lên.
- Con của `root` đã đi theo `root` (nhảy): **đừng cộng thêm** độ cao cho chân, chỉ co nhẹ (lỗi đã gặp: chân bay trốn sau thân).
- Bộ chuẩn: `idle` (lặp, thở; phần phụ như tai, mào, đuôi, cánh lắc trễ pha; chớp mắt bằng đổi attachment), `attack` (lấy đà →
  đánh → dư lực → về), `hit` (bật lùi, nhắm mắt), `skill` (ngồi → bật → bổ/đè → dẹp nảy), `walk`/`run` (lặp).
- Nguyên tắc: khoá đầu = khoá cuối với vòng lặp; dẹp-giãn (scale) khi lấy đà và chạm đất; phần phụ trễ nhịp 0.1–0.2 s.

## 6. Soi trước khi báo (bắt buộc)

- `rig/khung.png` (9 khung mỗi animation) và `anim_<tên>.gif`: bộ dựng khung Python riêng (`rig.render`, `rig.draw_pose`,
  `mesh.make_draw`), không cần trình duyệt. Soi từng hàng: hở khớp, mảnh lệch, mất mảnh, bị cắt khung.
- Trang xem: `rig/index.html` hoặc `rig_mesh/index.html` (5 ô chạy lặp + khung lớn có điều khiển, bật xương). Server tĩnh
  `.claude/launch.json` cấu hình `spine-work` (cổng 8771, phục vụ `spine-animation-ai/work`), mở bằng `preview_start` trong
  Browser pane rồi điều hướng tới `http://localhost:8771/<tên>/rig/index.html`. Kiểm bằng JS:
  `Object.entries(players).map(([k,p])=>[k,!!p.skeleton])`; player tải chậm vài giây, ô trắng lúc đầu chưa phải lỗi.
- Spine player ghim bản `4.2.119` (`rig.PLAYER_VER`); không dùng `@4.2.*`.
- Gửi người dùng ảnh khung, GIF, ảnh so sánh bằng SendUserFile; nói rõ cái gì chưa ổn.

## 7. Lỗi đã gặp và cách tránh

- Nền ô cờ "giả trong suốt" in vào pixel: mặt nạ nền theo vùng sáng nối mép ảnh, rồi gọt 1 px + làm mượt (blur 1.6, ngưỡng 0.5)
  cho hết răng cưa.
- Đa giác đầu ăn lẹm vai: kẻ đa giác đầu sát mép đầu, để vai cho tay.
- Vẽ bù ra màu xám, vệt chữ V: nới vùng vẽ bù 2 px (viền chuyển màu), phần ngoài mảnh tô màu trung vị trước khi inpaint.
- Phần chồng của tay quét vệt sẫm khi giơ: bán kính nhỏ (~9 px), chỉ lấy màu lông (`cap_keep`).
- Mảnh nhỏ bị lọc mất khi cắt tờ: ngưỡng diện tích tương đối thấp (0.0002 ảnh), mẩu thừa gộp theo khoảng cách.
- `Subdiv2D` trả toạ độ float32: làm tròn điểm theo bước 0.25 trước khi chèn để tra lại chỉ số.
- In tiếng Việt trên Windows: `sys.stdout.reconfigure(encoding="utf-8")` (`-I` bỏ qua `PYTHONIOENCODING`); vẽ chữ Việt lên ảnh
  dùng `ImageFont.truetype("C:/Windows/Fonts/arial.ttf")`.

## 8. Tệp

- `ArtGen/Spine/build.py` (gói prompt), `gen.py` (Codex có khoá), `rig.py` (cắt, khớp, dựng, mảnh cứng, khung, trang xem,
  animation), `mesh.py` (một lưới có trọng số).
- Đầu ra: `<base>/rig/` (mảnh cứng: `<mã>.json/.atlas/.png`, `placed/`, `so_ghep.png`, `xuong.png`, `khung.png`, GIF,
  `index.html`), `<base>/rig_mesh/` (lưới: `<mã>_mesh.*`, `luoi.png`, `khung.png`, GIF, `index.html`).
- Ví dụ đã chạy: Giọt Sương dữ liệu giả (cắt từ concept, scratchpad), Snorlax ảnh người dùng gửi
  (`spine-animation-ai/work/snorlax`, chỉ để thử).
