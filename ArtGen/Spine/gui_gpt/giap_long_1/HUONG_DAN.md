# giap_long: tướng .atomik đảo Hỏa (rig từ một ảnh liền)

Đảo Hỏa, ải 40. Làm theo cách hai đảo Thủy, Mộc: thú huyền thoại hơi chibi kiểu Pokémon, style cũ, dạng sau dữ hơn nhưng không quá, hạn chế dạng người. Claude gọi Codex bằng `ArtGen/Spine/gen.py <file prompt>`; người dùng muốn tự gửi thì chỉ cần đưa GPT đường dẫn file prompt (GPT tự mở ảnh mẫu và tự lưu).

## Dạng 1: Giáp Long Con (bốn chân)
- Thiết kế: rồng giáp con: thân đỏ thẫm, giáp thép xám xanh trên đầu (một sừng thép ở mõm), lưng, vai; mào lửa sau mũ, chóp đuôi lửa.
- File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Spine\gui_gpt\giap_long_1\luot_1_lien.txt`.
- Ảnh mẫu theo thứ tự:
  1. `E:\ProjectAtomik\PokiWar\ArtGen\Spine\inbox\de_hoa_1\tai_ve\L1_lien.png`: cừu hoa lông kem bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy khung, dáng, nét.
  2. `E:\ProjectAtomik\PokiWar\ArtGen\Spine\inbox\moc_tinh_2\tai_ve\L1_lien.png`: sói xám pha lê lục bảo bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy nét, tô.
  3. `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.
- Lưu: `E:\ProjectAtomik\PokiWar\ArtGen\Spine\inbox\giap_long_1\tai_ve\L1_lien.png` (trùng tên thì `L1_lien_2.png`, `_3`...).

## Dạng 2: Giáp Long (bốn chân)
- Thiết kế: rồng giáp lửa: giáp thép kín, gai thép lớn chóp đỏ lửa dọc lưng, vai, đuôi; mũ giáp hai sừng thép; bờm lửa dọc cổ; vuốt đỏ.
- File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\Spine\gui_gpt\giap_long_2\luot_1_lien.txt`.
- Ảnh mẫu theo thứ tự:
  1. `E:\ProjectAtomik\PokiWar\ArtGen\Spine\inbox\de_hoa_1\tai_ve\L1_lien.png`: cừu hoa lông kem bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy khung, dáng, nét.
  2. `E:\ProjectAtomik\PokiWar\ArtGen\Spine\inbox\moc_tinh_2\tai_ve\L1_lien.png`: sói xám pha lê lục bảo bốn chân (đảo Mộc); 1536x1024, nền trắng; lấy nét, tô.
  3. ảnh dạng 1 đã duyệt của dòng này (`E:\ProjectAtomik\PokiWar\ArtGen\Spine\inbox\giap_long_1`, L1_duyet.png hoặc tai_ve/L1_lien.png); 1536x1024, nền trắng; giữ loài, màu, mặt.
  4. `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png`: bản đồ thế giới vẽ tay, 1024x1536; chỉ lấy nét bút mực, chì sáp.
- Lưu: `E:\ProjectAtomik\PokiWar\ArtGen\Spine\inbox\giap_long_2\tai_ve\L1_lien.png` (trùng tên thì `L1_lien_2.png`, `_3`...).

## Kiểm
- Thú, không mặt người; mặt quả quyết, mắt nhìn sang phải; nhìn nghiêng 3/4 sang phải.
- Tô phẳng: không bóng, không điểm sáng, không phát sáng; lửa là mảng màu có viền mực khép kín, tối đa ba dải màu, không để giấy trắng; không tàn lửa, khói bay quanh.
- Chân tách nhau có khe trắng, tay tách thân, đuôi không vắt qua thân, cánh không đè đầu, sừng.
- Khung 1536x1024, con cao khoảng 720 px, chừa lề trắng; không đường đất, không bóng dưới chân.
- Dạng sau cùng loài, cùng màu, cùng dấu hiệu dạng trước.

## Câu sửa nhanh (gửi kèm `--note`)
- "Flat colour only: no shine spots, no shading, no glow; the flames do not light up the body."
- "Close every flame with a dark-brown ink outline and fill it with flat crayon colour, never white paper; no floating sparks or embers."
- "Keep white gaps between the legs and between each arm and the body; the tail must not cross the body."
- "More determined face: lowered brows, firm mouth, not a happy grin."
