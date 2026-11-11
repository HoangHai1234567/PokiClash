# Lượt 2 (tờ mảnh) dạng 1 Hải Long Nhi

Mỗi tờ một file prompt, chỉ gửi GPT đường dẫn file:

| Tờ | File prompt | GPT lưu vào | Kiểm |
|---|---|---|---|
| M01 | `D:\PokiClash\ArtGen\Spine\gui_gpt\tm10_1\luot_2_M01.txt` | `D:\PokiClash\ArtGen\Spine\inbox\tm10_1\tai_ve\M01.png` | đầu (trên, mắt to), hàm dưới, lòng miệng; mí mắt, lưỡi, hai râu cụt |
| M02 | `D:\PokiClash\ArtGen\Spine\gui_gpt\tm10_1\luot_2_M02.txt` | `D:\PokiClash\ArtGen\Spine\inbox\tm10_1\tai_ve\M02.png` | thân-cổ duỗi thẳng (1300 × 230), chóp đuôi có vây hồng san hô |

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py <file prompt>` (hoặc `chay_hoa.py` chạy tách). Mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px, tô phẳng; đầu là PHẦN TRÊN (không hàm, không cổ); cổ THẲNG như thước.

| Sai | Gửi thêm |
|---|---|
| Cổ vẽ cong | `The necks must be perfectly straight horizontal tubes, like a ruler, both ends rounded.` |
| Đầu dính hàm hoặc cổ | `The head part is the UPPER part only: no lower jaw, no neck; the lower jaw is its own separate part.` |
| Có gạc phân nhánh / ngọc | `Straight plain horns, no branches, no pearl: this is the younger form.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |
