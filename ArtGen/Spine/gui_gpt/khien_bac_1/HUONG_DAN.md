# khien_bac: tướng .atomik đảo Kim (rig từ một ảnh liền)

Đảo Kim, ải 20. Gốc aola: 784→785: mũ sắt lam trắng có mặt nhỏ ló ra → hiệp sĩ khiên lớn lam, ngọc lục, chữ thập vàng, giáo. Thú mặc giáp (không dạng người), chỉ dạng 1 chibi, càng tiến hóa càng dữ, ngầu, đẹp. Claude gọi Codex bằng `ArtGen/Spine/gen.py <file prompt>`; người dùng muốn tự gửi thì chỉ cần đưa GPT đường dẫn file prompt (GPT tự mở ảnh mẫu và tự lưu).

## Dạng 1: Khiên Sắt Tí Hon (bốn chân; chibi (đầu ~45%))
- Thiết kế: tatu con, mai tròn lam trắng như mũ sắt có đinh vàng, mặt ló dưới vành mai, chân ngắn.
- File prompt: `D:\PokiClash\ArtGen\Spine\gui_gpt\khien_bac_1\luot_1_lien.txt`.
- Ảnh mẫu theo thứ tự:
  1. `D:\PokiClash\ArtGen\Spine\inbox\de_hoa_1\tai_ve\L1_lien.png`: cừu hoa lông kem bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy khung, dáng, nét.
  2. `D:\PokiClash\ArtGen\Spine\inbox\moc_tinh_2\tai_ve\L1_lien.png`: sói xám pha lê lục bảo bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy nét, tô.
  3. `D:\PokiClash\ArtGen\Islands\refs\world_style.png`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.
- Lưu: `D:\PokiClash\ArtGen\Spine\inbox\khien_bac_1\tai_ve\L1_lien.png` (trùng tên thì `L1_lien_2.png`, `_3`...).

## Dạng 2: Vệ Sĩ Khiên Bạc (đứng hai chân, khiên bên phải, giáo sau; dạng cuối, không chibi (đầu ~25%))
- Thiết kế: tatu vệ sĩ đứng hai chân, giáp bạc lam từ dải mai, mũ đầu có vây lam, khiên lớn hình mũi tên ngọc lục chữ thập vàng, giáo ba mũi cán vàng.
- File prompt: `D:\PokiClash\ArtGen\Spine\gui_gpt\khien_bac_2\luot_1_lien.txt`.
- Ảnh mẫu theo thứ tự:
  1. `D:\PokiClash\ArtGen\Spine\inbox\nguu_quyen_3\tai_ve\L1_lien.png`: bò quyền thủ đứng hai chân, tay tách thân (đảo Hỏa); 1536x1024, nền trắng; lấy khung, dáng, nét.
  2. `D:\PokiClash\ArtGen\Spine\inbox\de_hoa_1\tai_ve\L1_lien.png`: cừu hoa lông kem bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy nét, tô.
  3. ảnh dạng 1 đã duyệt của dòng này (`D:\PokiClash\ArtGen\Spine\inbox\khien_bac_1`, L1_duyet.png hoặc tai_ve/L1_lien.png); 1536x1024, nền trắng; giữ loài, mặt, dấu hiệu.
  4. `D:\PokiClash\ArtGen\Islands\refs\world_style.png`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.
- Lưu: `D:\PokiClash\ArtGen\Spine\inbox\khien_bac_2\tai_ve\L1_lien.png` (trùng tên thì `L1_lien_2.png`, `_3`...).

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
