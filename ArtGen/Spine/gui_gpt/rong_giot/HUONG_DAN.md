# Rồng Giọt (dạng 1 mới của dòng Giọt Sương, định dạng .atomik)

Thay Giọt Nước (`thuy_7`, hình aola) bằng tướng vẽ mới, rig xương riêng, xuất `.atomik` (người dùng chọn 2026-11-07).
Claude gọi Codex bằng `ArtGen/Heroes/tools/gen_codex.py`; người dùng không phải gửi tay.

## Lượt 1: concept trọn con, dáng dễ rig
- File prompt: `D:\PokiClash\ArtGen\Spine\gui_gpt\rong_giot\luot_1_tong.txt`
- Ảnh mẫu Codex mở:
  - image 1 `D:\PokiClash\ArtGen\Heroes\refs\style_anchor.png`: Giọt Sương dạng 1 đã duyệt, 1143x1376, nền trắng (chỉ lấy nét bút, vân chì sáp, độ chi tiết).
  - image 2 `D:\PokiClash\ArtGen\Islands\refs\world_style.png`: bản đồ vẽ tay 1024x1536, nền biển xanh (chỉ lấy nét mực nâu và tô chì sáp).
  - image 3 `D:\PokiClash\ArtGen\Heroes\refs\style\style_sheet.png`: tờ 8 tướng aola, 1536x1024 (chỉ học cách thiết kế gọn, mắt to).
  - image 4 `D:\PokiClash\Assets\03 Art\Heroes\Resources\thuy_9\thuy_9_portrait.png`: Sương Long (dạng 3 của dòng), 512x512, nền trắng (chỉ lấy họ màu).
- Lưu: `D:\PokiClash\ArtGen\Spine\inbox\rong_giot\tai_ve\L1_full.png`
- Kiểm: đủ người, không cắt mép; tay tách thân, chân không chéo; kiếm, đuôi, cánh không chạm tay; tô phẳng, không bóng, không điểm sáng (trừ chấm mắt); mặt quả quyết.
- Câu sửa nhanh: "Arms must not touch the body." / "Flat colour only: no shine spots, no shading, no shadow under the feet." / "Wings must not touch the arms or the ears."

## Lượt 2: tách mảnh (2 ảnh)
- File prompt: `D:\PokiClash\ArtGen\Spine\gui_gpt\rong_giot\luot_2_tach_manh.txt`
- Bước A `L2a_head_pieces.png`: đầu, đầu nhắm mắt, đầu hét, mào, 2 tai (6 mảnh). Bước B `L2b_body_pieces.png`: 2 cánh, thân, đuôi, kiếm, 2 cánh tay, 2 nắm tay, 2 đùi, 2 bàn chân (13 mảnh). Cùng thư mục `D:\PokiClash\ArtGen\Spine\inbox\rong_giot\tai_ve`.
- Kiểm: đủ 6 và 13 mảnh, không mảnh nào chạm nhau, chỗ khớp có đầu tròn thừa ra.

## Sau đó
Claude cắt mảnh, khớp vào ảnh lượt 1, dựng xương, làm animation (đứng, trúng đòn, đánh, bắn tia, chiêu cuối, tiến hóa) với hiệu ứng nước sẵn có của dòng Giọt Sương, xuất `.atomik`, nối vào game.
