# ung_thep: tướng .atomik đảo Kim (rig từ một ảnh liền)

Đảo Kim, ải 60. Gốc aola: 1696→1697: ưng máy bạc cam, cánh lông pha lê bạc hà, đuôi tím, móng vàng. Thú mặc giáp (không dạng người), chỉ dạng 1 chibi, càng tiến hóa càng dữ, ngầu, đẹp. Claude gọi Codex bằng `ArtGen/Spine/gen.py <file prompt>`; người dùng muốn tự gửi thì chỉ cần đưa GPT đường dẫn file prompt (GPT tự mở ảnh mẫu và tự lưu).

## Dạng 1: Ưng Thép Con (chim đứng hai chân, cánh dang; chibi (đầu ~45%))
- Thiết kế: ưng con tròn lông bạc, mũ mặt cam, mỏ vàng, cánh nhỏ lông pha lê bạc hà, đuôi tím ba lông.
- File prompt: `D:\PokiClash\ArtGen\Spine\gui_gpt\ung_thep_1\luot_1_lien.txt`.
- Ảnh mẫu theo thứ tự:
  1. `D:\PokiClash\ArtGen\Spine\inbox\mi_nhi_2\tai_ve\L1_lien.png`: chim đứng hai chân, cánh dang (đảo Thủy); 1536x1024, nền trắng; lấy khung, dáng, nét.
  2. `D:\PokiClash\ArtGen\Spine\inbox\de_hoa_1\tai_ve\L1_lien.png`: cừu hoa lông kem bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy nét, tô.
  3. `D:\PokiClash\ArtGen\Islands\refs\world_style.png`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.
- Lưu: `D:\PokiClash\ArtGen\Spine\inbox\ung_thep_1\tai_ve\L1_lien.png` (trùng tên thì `L1_lien_2.png`, `_3`...).

## Dạng 2: Ưng Thép (bay, cánh xoè sau vai; dạng cuối, không chibi (đầu ~25%))
- Thiết kế: ưng thép lớn đang bay, giáp bạc cam, mũ đầu cam có mào, cánh sáu lông pha lê bạc hà dài như lưỡi dao, đuôi tím chẻ ba dài, móng vàng.
- File prompt: `D:\PokiClash\ArtGen\Spine\gui_gpt\ung_thep_2\luot_1_lien.txt`.
- Ảnh mẫu theo thứ tự:
  1. `D:\PokiClash\ArtGen\Spine\inbox\gio_loc_2\tai_ve\L1_lien.png`: rồng chuồn chuồn bay lơ lửng (đảo Mộc); 1536x1024, nền trắng; lấy khung, dáng, nét.
  2. `D:\PokiClash\ArtGen\Spine\inbox\de_hoa_1\tai_ve\L1_lien.png`: cừu hoa lông kem bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy nét, tô.
  3. ảnh dạng 1 đã duyệt của dòng này (`D:\PokiClash\ArtGen\Spine\inbox\ung_thep_1`, L1_duyet.png hoặc tai_ve/L1_lien.png); 1536x1024, nền trắng; giữ loài, mặt, dấu hiệu.
  4. `D:\PokiClash\ArtGen\Islands\refs\world_style.png`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.
- Lưu: `D:\PokiClash\ArtGen\Spine\inbox\ung_thep_2\tai_ve\L1_lien.png` (trùng tên thì `L1_lien_2.png`, `_3`...).

## Kiểm
- Thú, không mặt người; mặt quả quyết, mắt nhìn sang phải; nhìn nghiêng 3/4 sang phải.
- Dạng 1 chibi; dạng sau đầu nhỏ hẳn, dáng chiến, ngầu hơn dạng trước rõ rệt.
- Tô phẳng: giáp, kim loại, pha lê mỗi mảng một màu, không đốm sáng, không phản chiếu, không phát sáng.
- Chân tách nhau có khe trắng, tay và vũ khí tách thân, đuôi không vắt qua thân, cánh không đè đầu.
- Khung 1536x1024, con cao khoảng 720 px, chừa lề trắng; không đường đất, không bóng dưới chân.

## Câu sửa nhanh (gửi kèm `--note`)
- "Flat colour only: no shine spots, no metallic gradients, no reflections, no glow on the armour."
- "Not chibi: make the head much smaller (about a quarter of its height), longer limbs, a fiercer face."
- "Keep white gaps between the legs and between each arm, weapon and the body; the tail must not cross the body."
- "More determined face: lowered brows, firm mouth, not a happy grin."
