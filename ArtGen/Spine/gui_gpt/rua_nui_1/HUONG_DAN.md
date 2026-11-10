# rua_nui: tướng .atomik đảo Thổ (rig từ một ảnh liền)

Đảo Thổ, ải 40. Gốc aola: 1203→1204: rùa mầm lục nhạt, mai đất rêu → rùa núi mai là ngọn núi có cây, vuốt pha lê lam. Thú (không dạng người, gốc golem hay người đã đổi thành thú), chỉ dạng 1 chibi, càng tiến hóa càng dữ, ngầu, đẹp. Claude gọi Codex bằng `ArtGen/Spine/gen.py <file prompt>`; người dùng muốn tự gửi thì chỉ cần đưa GPT đường dẫn file prompt (GPT tự mở ảnh mẫu và tự lưu).

## Dạng 1: Rùa Mầm Đá (rùa bốn chân thấp, mai trên lưng; chibi (đầu ~45%))
- Thiết kế: rùa con xanh bạc hà, mầm hai lá trên đầu kèm viên sỏi lam, mai như cục đất nâu phủ rêu, má hồng.
- File prompt: `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rua_nui_1\luot_1_lien.txt`.
- Ảnh mẫu theo thứ tự:
  1. `C:\Atomik\PokiWar\ArtGen\Spine\inbox\giap_long_2\tai_ve\L1_lien.png`: rồng giáp bốn chân thân thấp, đuôi dựng sau (đảo Hỏa); 1536x1024, nền trắng; lấy khung, dáng, nét.
  2. `C:\Atomik\PokiWar\ArtGen\Spine\inbox\de_hoa_1\tai_ve\L1_lien.png`: cừu hoa lông kem bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy nét, tô.
  3. `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.
- Lưu: `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rua_nui_1\tai_ve\L1_lien.png` (trùng tên thì `L1_lien_2.png`, `_3`...).

## Dạng 2: Rùa Núi (rùa bốn chân thấp, mai trên lưng; dạng cuối, không chibi (đầu ~25%))
- Thiết kế: rùa núi to, cổ khỏe, mày xương vàng nâu có mào, mai là ngọn núi vách đá nâu, đỉnh xám tuyết trắng, gờ cỏ và vài cây tròn, vuốt pha lê lam băng.
- File prompt: `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rua_nui_2\luot_1_lien.txt`.
- Ảnh mẫu theo thứ tự:
  1. `C:\Atomik\PokiWar\ArtGen\Spine\inbox\giap_long_2\tai_ve\L1_lien.png`: rồng giáp bốn chân thân thấp, đuôi dựng sau (đảo Hỏa); 1536x1024, nền trắng; lấy khung, dáng, nét.
  2. `C:\Atomik\PokiWar\ArtGen\Spine\inbox\de_hoa_1\tai_ve\L1_lien.png`: cừu hoa lông kem bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy nét, tô.
  3. ảnh dạng 1 đã duyệt của dòng này (`C:\Atomik\PokiWar\ArtGen\Spine\inbox\rua_nui_1`, L1_duyet.png hoặc tai_ve/L1_lien.png); 1536x1024, nền trắng; giữ loài, mặt, dấu hiệu.
  4. `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.
- Lưu: `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rua_nui_2\tai_ve\L1_lien.png` (trùng tên thì `L1_lien_2.png`, `_3`...).

## Kiểm
- Thú, không mặt người; mặt quả quyết, mắt nhìn sang phải; nhìn nghiêng 3/4 sang phải.
- Dạng 1 chibi; dạng sau đầu nhỏ hẳn, dáng chiến, ngầu hơn dạng trước rõ rệt.
- Tô phẳng: đá, giáp, pha lê, rêu mỗi mảng một màu, không đốm sáng, không phản chiếu, không phát sáng.
- Chân tách nhau có khe trắng, tay và vũ khí tách thân, đuôi không vắt qua thân, cánh không đè đầu.
- Khung 1536x1024, con cao khoảng 720 px, chừa lề trắng; không đường đất, không bóng dưới chân.

## Câu sửa nhanh (gửi kèm `--note`)
- "Flat colour only: no shine spots, no metallic gradients, no reflections, no glow on the stone, crystals or runes."
- "Not chibi: make the head much smaller (about a quarter of its height), longer limbs, a fiercer face."
- "Keep white gaps between the legs and between each arm, weapon and the body; the tail must not cross the body."
- "More determined face: lowered brows, firm mouth, not a happy grin."
