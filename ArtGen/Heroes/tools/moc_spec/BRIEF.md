# Viết đặc tả dạng tướng đảo Mộc (moc_spec)

Mục tiêu: với mỗi dạng được giao, viết mục `F(...)` vào file `ArtGen/Heroes/tools/moc_spec/<file>.py` (danh sách `SPEC`),
rồi chạy `py -3 -I ArtGen/Heroes/tools/lo_moc.py <mã> ...` (ở `E:\ProjectAtomik\PokiWar`) để kiểm và dựng ảnh rig. Đặc tả này
sinh prompt cho Codex vẽ concept và vẽ từng nhóm mảnh đè lên rig aola, rồi bộ ghép thay hình từng mảnh, nên chia nhóm sai thì
ghép hỏng.

## Đọc trước

- `ArtGen/Heroes/tools/lo_moc.py`: docstring của `G` (nhóm) và `F` (dạng).
- Mẫu đã làm: `ArtGen/Heroes/tools/moc_spec/a01_tien_la.py` (Tiên Lá dạng 1, rig #648).
- `ArtGen/Heroes/QUY_TRINH.md` dòng 1–35 (phong cách) và 201–227 (rig, viết prompt).

## Xem rig

- `py -3 -I C:/Users/vnhom/AppData/Local/Temp/claude/76a695ae60f8c005/925a1e50-4cc2-4def-aa01-b0296ee08041/scratchpad/rigview.py <id> <ảnh ra.png> [cao]`:
  trái là khung đứng đầu màu thật, phải là `part_map` đánh số; in mỗi mảnh: số, `c` (id hình), khung bao (đơn vị clip), số điểm ảnh.
  Ghi ảnh ra vào thư mục scratch của bạn, rồi mở bằng Read.
- Mảnh khó nhận (nhỏ, chồng nhau): `py -3 -I E:/ProjectAtomik/aola/tools/part_context.py E:/ProjectAtomik/aola/reskin/pet<id>_parts/front_idle <thư mục ra> --cols 6 --cell 260`
  (mỗi ô: cả con mờ, mảnh đó tô đậm viền đỏ). Có thể mở thêm `E:/ProjectAtomik/aola/reskin/pet<id>_parts/front_idle/part_NN.png`.
- Hình gốc đủ con: `E:/ProjectAtomik/aola/reskin/goc_<id>/export/portrait.png`.

## Luật chia nhóm

- Mỗi mảnh đúng một vai: trong một nhóm, `keep` (giữ hình gốc: chỉ bóng xám hình elip dưới chân, thường là mảnh 1, phải xem
  lại), hoặc `drop` (bỏ hẳn: hiệu ứng aola không hợp thiết kế mới như quầng sáng, vệt xoáy, vòng quỹ đạo, hạt lấp lánh).
  Hiệu ứng thuộc thiết kế mới (mây của rồng, vòng gió...) thì làm một nhóm vẽ lại. `lo_moc.py` báo mảnh chưa có vai.
- Nhiều rig có mảnh 2 (hoặc một mảnh to nằm sau cùng) là lớp viền đen của cả con: cho vào `drop`.
- Nhóm = vùng concept: 4–10 nhóm mỗi dạng, mỗi nhóm một loại phần (đầu có mặt; thân; hai tay; hai chân; đuôi; cánh; tai, sừng,
  mào; đồ cầm tay; hiệu ứng). Mảnh đầu tiên của `parts` là mảnh chính.
- **Mặt:** nhóm đầu vẽ luôn mặt. Mắt, con ngươi, miệng, má, lông mày cũ nằm trên đầu thì ghi vào `parts` (để ảnh gốc có chỗ
  mắt) và vào `hide` (ghép thì ẩn).
- `kind="giu"` (giữ viền) cho thân, tay, chân, đầu; `kind="doi"` (đổi dáng) cho tai, sừng, mào, tóc, đuôi, cánh, vây, phụ kiện,
  đồ cầm, hiệu ứng, kèm `joint` (đầu khớp giữ chỗ, viết tiếng Anh: "base of the horn (on the head)").
- **Tay chân trùng rig:** cùng số chi, khớp cùng chỗ, chi chĩa cùng hướng. Ghi rõ đầu nào của chi là gì.
- **Hai mảnh chung một `c`** (rigview in ra): chỉ được cùng `drop`, cùng `keep`, cùng `hide`, hoặc cùng một nhóm (cặp tai, cặp
  chân giống nhau). `lo_moc.py` báo lỗi nếu khác.
- Trái, phải theo người xem (viewer-left / viewer-right).

## Viết chữ

- Tiếng Anh cho mọi chuỗi gửi Codex (`intro`, `stance`, `attitude`, `colours`, `avoid`, `en`, `old`, `new`, `joint`); tiếng
  Việt cho `design_vi`, `vi`. Không nhắc tên game nào.
- `intro`: dạng 1 "a ... , the first stage of a three-stage Wood evolution line"; dạng sau "the SECOND stage of a three-stage
  Wood evolution line whose first stage is image 6: ..." (dòng 2 dạng thì "two-stage"; Thỏ Hoàng chỉ 1 dạng).
- `old`: hình gốc của nhóm trông ra sao (hình dạng, màu, vị trí). `new`: thiết kế mới của phần đó, cụ thể màu, chất liệu, cái
  gì không vẽ. Mắt mới đặt đúng chỗ mắt cũ, "brows angled down" cho vẻ chiến; chỉ một chấm sáng nhỏ trong mắt.
- `avoid`: các nét của thiết kế gốc aola phải tránh (màu, vật, kiểu dáng gốc).
- Tướng là sinh vật kiểu thú nuôi, vẻ "chiến" (mày xếch, cười tự tin, thế sẵn sàng đánh), dễ thương, không đáng sợ; tô phẳng
  không bóng (khối RENDER chung tự chèn, không cần viết).
- Thiết kế mới phải khác hẳn con gốc và đúng bản người dùng đã duyệt (được giao bên dưới). Dạng sau giữ màu, mặt, chất liệu của
  dạng 1 (cùng một con lớn lên), `prev="<mã dạng 1>"`.
- `name` (tên dạng), `stage` ("ải N đảo Mộc, dạng k/m") được giao bên dưới.

## anim (cho khuôn animation)

`anim=dict(root=<mảnh thân>, head=<mảnh đầu>, swing=[mảnh vung khi đánh: tay cầm vũ khí, vuốt, đuôi quật], wob=[mảnh đung
đưa lúc đứng: tai, đuôi, cánh, râu, lá], fly=[mảnh bay rời, không dính thân: quả cầu, tấm bay, mây rời], cast=(<mảnh>, fx, fy)
(chỗ bắn tia mana: điểm theo tỉ lệ khung bao mảnh đó, thường là miệng, tay, quả cầu), parent={<mảnh>: <mảnh cha>})`.
`parent`: mặc định mọi mảnh nhóm (trừ mảnh ẩn) nối vào `root`, mảnh cùng nhóm đầu nối vào `head`. Ghi `parent` cho mảnh nối
chỗ khác: tai, sừng, tóc, mào, râu nối vào đầu; cẳng tay vào bắp tay, bàn tay vào cẳng tay; bàn chân vào ống chân; chóp đuôi
vào đuôi; đồ cầm vào bàn tay. Mảnh `fly` có cha null, không cần ghi. Chỉ dùng số mảnh không bị ẩn.

## Kiểm xong mới báo

1. `py -3 -I ArtGen/Heroes/tools/lo_moc.py <mã>` chạy không lỗi.
2. Mở `ArtGen/Heroes/refs/moc/<mã>/RegionMap.png`: không còn chỗ xám (mảnh sót), vùng đúng phần.
3. Mở vài `ArtGen/Heroes/refs/moc/<mã>/orig/Nxx.png`: nhóm đúng là phần đã ghi.
4. Không chạy `gen_codex.py`, không sửa file nào khác ngoài file moc_spec được giao, không git.

Báo lại: mã đã xong, mỗi dạng một dòng các nhóm (mã, tên, mảnh), cảnh báo chung hình, mảnh lạ hay điều bạn không chắc.
