# Quy trình gen hình tướng (thay tạo hình trên rig aola)

Chốt 2026-11-01 sau khi ảnh `tieu_y_1` gen theo cách cũ bị chê "không đúng theme game". Nội dung rút từ các file md của AolaRipper; đọc bản gốc khi cần chi tiết:
- `CLAUDE.md`, `AGENT.md`, `TIEN_DO.md`;
- `reskin/BAI_HOC.md`, nhất là mục 6–8;
- prompt mẫu của 4 thầy tu: `reskin/monk_*/PROMPTS.md`, `GEN.md`, `MB6_GEN.md`.

AolaRipper nằm ở `D:\Aola-20261029T161238Z-1-001\Aola\AolaRipper\AolaRipper` (gọi tắt là `<aola>`).

## 1. Theme của tướng

- **Tướng là sinh vật kiểu thú nuôi đánh nhau** (pet), như Yabi của aola. Không vẽ người kiểu anime hay tranh minh hoạ.
- **Nét theo hình trận aola**, giống 4 thầy tu đang có trong game:
  - viền đều;
  - màu viền là sắc đậm, hơi xỉn của chính màu nó bao, không đen, không một màu nâu cho mọi chỗ;
  - tô phẳng 2–3 tông, cel shading một lớp, điểm sáng nhỏ.
- **Không dùng nét sổ tay vẽ tay** (bút chì, sáp, giấy) cho tướng. Nét đó chỉ dành cho UI.

## 2. Nguyên tắc

- **Mỗi tướng là một dòng tiến hóa của aola.**
  - Quái thường lấy dòng có 2–4 dạng, boss lấy dòng có từ 3 dạng.
  - Mỗi dạng của dòng là một con riêng trong aola.
  - Lên sao thì đổi sang dạng sau.
- **Giữ animation của con gốc, thay toàn bộ hình.**
  - Chỉ con vector (`<aola>/raw/flash/fightassets/pet<id>.swf`) làm được. Con chỉ có ảnh render sẵn (`fightassets/bitmap/...`) thì không.
  - Mảnh mới đắp lên mảnh cũ ở mọi khung của 4 animation: đứng, trúng đòn, đánh thường, chiêu.
- **Sinh vật mới phải khác hẳn con gốc, nhưng tay chân phải trùng rig:**
  - cùng số tay, chân, tai, đuôi;
  - khớp vai, cổ, hông ở cùng chỗ;
  - mỗi chi chĩa cùng hướng, đầu nào nối với gì giữ nguyên.

  Đổi loài, màu, chất liệu, đồ đeo; giữ khung.
- **Dáng ngoài được đổi, và nên khác bản gốc** (người dùng dặn 2026-11-01). Mỗi mảnh vẫn xoay quanh khớp cũ, nên chia hai loại:
  - **đổi dáng:** đầu, tai, mào, đuôi, vây, phụ kiện. Viền theo concept, to hơn hoặc khác hình được; chỉ **đầu khớp** (gốc tai, mép nối đuôi, đáy mào) phải ở nguyên chỗ. Đầu to ra thì vẫn phải phủ cổ và đỡ mào;
  - **giữ viền:** thân, tay, chân. Thân phải phủ kín vai, hông; tay chân đổi cỡ nhiều sẽ lệch khớp.

  Mảnh cần to ra thì khai `frame` trong `groups.json` (thêm mảnh bên cạnh vào khung) để ảnh mẫu có chỗ trống quanh nó. Dáng người (Tiểu Y, Lam Quân) cũng đổi theo cách này.
- **Bản quyền:**
  - chuyển động là của Baitian;
  - ảnh mẫu gửi GPT là hình gốc, nên kết quả là hình phái sinh.

  Người dùng đã tự quyết dùng (2026-11-01). Không đăng công khai.

## 3. Các bước cho một dạng

Ví dụ ở dạng 1 dòng Thủy đầu tiên (#7, `<aola>/reskin/pet7_parts`, `<aola>/reskin/thuy_7`). Chạy từ `<aola>`, Python `py -3 -I`. Thư mục tạm cho Chrome là `C:\Users\ADMIN\AppData\Local\Temp\aola_work`, vì đường dẫn thư mục tạm của phiên Claude quá dài.

1. **Tìm clip mặt trước:** `py -3 -I tools/swf_states.py raw/flash/fightassets/pet<id>.swf`. Lấy 4 id của `pet<id>_1` (đứng, trúng đòn, đánh thường, chiêu).
2. **Xuất SVG bằng FFDec.** Java lấy từ OpenJDK của Unity:
   - `"C:/Program Files/Unity/Hub/Editor/6000.0.73f1/Editor/Data/PlaybackEngines/AndroidPlayer/OpenJDK/bin/java.exe" -jar tools/ffdec/ffdec-cli.jar -selectid <4 id> -format sprite:svg -export sprite reskin/pet<id>_parts/svg raw/flash/fightassets/pet<id>.swf`
   - Nếu lệnh bị chặn thì dừng và nhờ người dùng cấp quyền, không lách.
3. **Đọc rig:**
   - `tools/svg_frames.py <svg> <frames.json> <id>=1_1 <id>=1_2 <id>=1_4 <id>=1_6`
   - `tools/swf_timeline.py <swf> <timeline_front.json> 1`
   - `tools/render_chars.py <svg> <frames.json> <chars> ...`. Hình bị xén thì chạy lại với `--half 1000 --scale 2 --only`.
   - `tools/part_map.py <svg>/DefineSprite_<đứng>/1.svg <front_idle>`
   - `tools/analyze_parts.py <parts> <timeline> <tools> > analysis.txt`
   - `tools/part_context.py <front_idle> <context>`
4. **Hiểu giải phẫu** (bắt buộc, `BAI_HOC.md` mục 8):
   - xem `context/full_numbered.png` và tờ `context_*.png` (mảnh tô đỏ trên thân mờ);
   - gọi đúng chức năng từng mảnh: bắp tay hay cẳng tay, đùi hay ống chân, bàn tay ở đầu nào;
   - mảnh khó đoán thì xem nó đi cứng với nhóm nào (`analysis.txt`);
   - ghi **bảng giải phẫu** (mảnh, là gì, hai đầu, hướng; trái, phải theo người xem) vào file tướng.
5. **Concept:**
   - viết `regions.json` (vùng theo bộ phận), chạy `tools/region_map.py <front_idle> <regions.json> <ra>/<id>_Front` để được bóng xám và bản đồ vùng;
   - prompt concept coi bóng xám là **rig**, không phải dáng để tô theo: mục KEEP (số chi, chỗ khớp, hướng chi, cỡ thân tay chân) và mục CHANGE (viền mới từng vùng), mẫu ở `thuy/giot_suong_1.md` (hai chân), `thuy/giot_suong_3.md` (bốn chân);
   - chờ người dùng duyệt.
6. **Ảnh mẫu nhóm:**
   - viết `groups.json`: nhóm theo chi hoặc bộ phận, `draw`, `keep`, `drop`; nhóm đổi dáng to ra thì thêm `frame`;
   - chạy `tools/orig_refs.py <reskin> <parts>` để được ảnh mẫu `refs/orig/<mã>.png`: hình gốc của nhóm, vuông 1024, nền trắng, đúng khung.
7. **Gen từng nhóm (MB5):**
   - mỗi lần đính kèm ảnh mẫu nhóm (ảnh 1) và concept đã duyệt (ảnh 2);
   - GPT vẽ đè giữ khung;
   - nét và màu theo hình gốc, không theo concept.
8. **Ghép:**
   - chạy `place_parts_2217.py` (đọc chung `groups.json`), rồi `place_variants.py` (hình biến thể ở trúng đòn, đánh thường, chiêu), rồi `build_page_2217.py`;
   - khai `rebuild` trong `groups.json` để trình chỉnh sửa (`mo_chinh_sua.bat`) ghép lại được.
9. **Soi:**
   - tự chụp `so_sanh.html#1_<trạng thái>@<khung>` của cả 4 animation;
   - so từng chi với concept: đầu nào là bàn tay, bàn chân, ngón cái ở đâu, lớp nào che lớp nào;
   - liệt kê mảnh cũ còn sót.

   Đếm "đủ mảnh" không thay được việc xem.
10. **Đưa vào game:**
    - người dùng chỉnh trong trình chỉnh sửa rồi bấm Lưu, được `export/anim.json`; Unity đọc file này (`AolaActor`);
    - không tự đổi số người dùng đã chỉnh (`adjust.json`).

Thư mục: rig và bộ ghép nằm ở `<aola>/reskin/`. Prompt, ảnh đính kèm và ảnh GPT trả về nằm ở `ArtGen/Heroes/`:
- `refs/<hệ>/<mã>/`: ảnh đính kèm;
- `inbox/<mã>/`: ảnh GPT trả về.

Lúc ghép, Claude chép ảnh từ `inbox/` sang `<aola>/reskin/<tên>/inbox/`.

## 4. Quy tắc viết prompt (người dùng dặn, bắt buộc)

- **Nói rõ từng chi:**
  - đầu nào là gì ("TOP end = shoulder", "BOTTOM end = hand");
  - mũi chân chĩa đâu, ngón cái phía nào;
  - cái **không được vẽ** ("Do NOT put the hand at the top", "NO sleeve").
- **Hình mảnh cũ thắng cách hiểu thông thường.** Lá hẹp ở vai thì bảo "cuống ở đầu hẹp", không bảo "lá mũi nhọn".
- **Nhóm gen là các mảnh của cùng một chi hoặc bộ phận.** Mảnh chỉ nằm gần (vòng hông sau nắm tay) không vào nhóm tay.
- **Mảnh nhỏ trong khối lớn mà bị thay hình ở vài khung** (mắt chớp, mặt hoảng): để khối lớn mang luôn phần đó, bỏ mảnh nhỏ (`drop`). Muốn giữ cử động riêng thì phải gen thêm hình biến thể.
- **Vũ khí, phụ kiện đổi dáng:** không bắt bám viền cũ. Vật xuyên qua nhiều mảnh (trượng qua tay) chỉ vẽ ở một mảnh.
- **Khung MB5** dùng nguyên văn, chỉ đổi bảng màu viền. Nhóm **giữ viền** (thân, tay, chân):

```
FRAMING: the same square canvas; every piece keeps its place, size, angle and direction from image 1, so the drawing can be put back on the old puppet. Where image 2 shows this part in another pose or outline, follow image 1: take only colours and details from image 2.
LINE AND COLOUR: match image 1's drawing style, not the concept's: an outline about 1.5-2% of the piece's size, in a darker shade of each fill (...), never black; flat fills with 2-3 tones; no gradients, no texture.
Plain white background. Only this group. No text.
```

  Nhóm **đổi dáng** thay câu FRAMING, nêu tên đầu khớp của mảnh (base end, joint edge…):

```
FRAMING: the same square canvas; the piece keeps its place, angle and direction from image 1, and its <joint end> stays exactly where it is, so the drawing can be put back on the old puppet. The outline follows image 2, not image 1: it may be a different shape and bigger, but stays inside the square with a clear white margin.
```

## 5. Ghép và kiểm (bẫy đã gặp)

- **Nền trắng:** chỉ xoá phần trắng nối với mép ảnh, không xoá mọi điểm gần trắng (thủng chỗ sáng). Phóng ảnh RGBA thì nhân trước alpha, dùng bilinear.
- **Chiều chi:** chồng ảnh gen lên hình gốc trước khi ghép, xem bàn tay, bàn chân có ở đúng đầu không.
- **Thứ tự lớp của SWF có thể sai với vật mới:** dùng `raise` hoặc `lower` trong `groups.json`.
- **Mảnh tự chạy** (áo choàng, lửa có timeline riêng): tô lại màu, hoặc vẽ cả tờ lưới một lần (`grid_2217.py`).
- **Hiệu ứng** (vệt chém, quầng): giữ, hoặc tô lại theo màu hệ (`recolor`).
