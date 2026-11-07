# Thử rig Spine: Giọt Sương (dạng 1)

Mục đích: xem bộ công cụ `spine-animation-ai` rig xương và làm animation từ hình GPT vẽ được tới đâu.
Đây là thử nghiệm riêng, không thay quy trình vẽ đè lên rig aola.

## Lượt 1: hình trọn con, dáng đứng dễ rig
- File prompt (gửi GPT đúng đường dẫn này): `E:\ProjectAtomik\PokiWar\ArtGen\Spine\gui_gpt\giot_suong\luot_1_tong.txt`
- Ảnh mẫu GPT sẽ mở:
  - image 1 `E:\ProjectAtomik\PokiWar\ArtGen\Heroes\inbox\giot_suong_1\concept_duyet.png`: Giọt Sương bản đã duyệt, 1143x1376, nền trắng, đứng nghiêng sang phải, tay phải cầm kiếm, có bóng loáng (chỉ lấy thiết kế).
  - image 2 `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png`: bản đồ vẽ tay 1024x1536, nền biển xanh (chỉ lấy nét mực nâu và tô chì sáp).
- GPT lưu ảnh vào: `E:\ProjectAtomik\PokiWar\ArtGen\Spine\inbox\giot_suong\tai_ve\L1_full.png`
- Kiểm:
  - đủ người, không bị cắt mép; ảnh dọc 1024x1536; nền trắng;
  - hai tay tách khỏi thân (có khoảng trắng), hai chân không chéo nhau, kiếm và đuôi không đè lên tay, chân;
  - tô phẳng, không bóng loáng, không bóng đổ dưới chân; viền nâu đều.
- Câu sửa nhanh:
  - "Arms must not touch the body: leave clear white space between each arm and the torso."
  - "Flat colour only: no shine spots, no shading, no shadow under the feet."
  - "Keep the whole sword blade clear of the legs."

## Lượt 2: tách mảnh (2 ảnh)
- Chưa có: Claude dựng file này sau khi duyệt ảnh lượt 1.
- Bước A lưu `L2a_head_pieces.png` (đầu, đầu nhắm mắt, mào, 2 cánh), bước B lưu `L2b_body_pieces.png` (thân, đuôi, kiếm, 2 cánh tay, 2 nắm tay, 2 đùi, 2 ủng), cùng thư mục `E:\ProjectAtomik\PokiWar\ArtGen\Spine\inbox\giot_suong\tai_ve`.
- Kiểm: đủ 5 và 11 mảnh, không mảnh nào chạm nhau, chỗ khớp có đầu tròn thừa ra.

## Sau đó
Claude cắt mảnh, khớp vị trí với ảnh lượt 1, dựng xương Spine 4.2, làm animation (đứng thở, đánh, trúng đòn, chiêu) và mở trang xem thử.
