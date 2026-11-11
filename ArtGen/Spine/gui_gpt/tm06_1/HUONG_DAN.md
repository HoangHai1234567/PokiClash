# Gói gửi GPT: dòng Giông Bão, dạng 1 Giông Mưa (`tm06_1`)

Lô 10 tướng mới đảo Thủy, dòng 6 (thay suất ải 30, Vây Lam, hiếm). Thiết kế: kỳ giông con chibi xanh đá mưa, bụng cam mơ, ba lá mang san hô mỗi bên, đốm kem như giọt mưa, đuôi có vây; cõng quả bầu hồ lô vàng rơm nút gỗ, dây đeo chàm chéo ngực, tua kem.

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm06_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu theo đường dẫn ghi trong file và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm06_1\tai_ve\L1_concept_4.png` (trùng tên thì `L1_concept_2.png`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm06_1/luot_1_concept.txt` (chạy nền, khoá Codex chung).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\canh_cut_1\tai_ve\L1_lien.png` | Cánh Cụt dạng 1 đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi xanh ngọc cầm chảo, đứng hai chân. Lấy bố cục, dáng tách tay chân, nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\lam_quan_1\tai_ve\L1_lien.png` | Lam Quân dạng 1 đã duyệt (1536 × 1024, nền trắng): sư tử con chibi xanh lam bờm mây kem, há miệng. Lấy nét, vân sáp, mặt quả quyết |
| 3 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |

Không đính ảnh con gốc của game tham khảo; mọi ảnh mẫu là tướng của dự án.

## Kiểm

- Kỳ giông (đuôi dài, đầu dẹt rộng, mang lông chim), **không** ra ếch / cóc / nòng nọc; không mỏ, không đĩa, không lá trên đầu.
- Chibi đầu khoảng 45%; mặt quả quyết (mày hạ), không cười toe; nhìn sang **phải**.
- Màu: thân xanh đá mưa, bụng cam mơ, ba lá mang san hô mỗi bên, đốm kem, vây đuôi lam nhạt.
- Quả bầu hồ lô vàng rơm, nút gỗ nâu, tua kem, dây chàm chéo ngực; bầu ở sau lưng phía trái, không che đầu, mang, tay.
- Hai chân tách nhau có khe trắng, tay tách thân, đuôi không chéo chân; miệng hé thấy lòng miệng.
- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh, không đường đất.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `gen.py ... --note "..."`)

| Sai | Gửi thêm |
|---|---|
| Ra ếch, cóc | `It must be a salamander: a long thick tail, a wide flat head, feathery gill fronds; not a frog or a toad.` |
| Có bóng, mảng sáng tối, điểm sáng | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |
| Đồ trên lưng che đầu, mang | `Move the carried object lower and further back so it never covers the head or the gill fronds.` |
| Tay chân dính thân, chéo nhau | `Leave white gaps between the legs and between each arm and the body; nothing crosses.` |
| Nhìn sang trái | `The creature must face the viewer's RIGHT.` |
