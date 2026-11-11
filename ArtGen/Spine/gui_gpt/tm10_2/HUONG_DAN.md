# Gói gửi GPT: dòng Hải Long, dạng 1 và 2 (`tm10`)

Dạng 3 của dòng là Hải Long Ngũ Đầu đã duyệt (`inbox/hai_long/tai_ve/L1_duyet.png`). Pha 1 chỉ gen concept trọn con cho hai dạng đầu; gen dạng 2 trước (đính dạng 3), chọn xong chép bản chọn thành `inbox/tm10_2/tai_ve/L1_duyet.png`, chạy lại `build_tm10.py` để có prompt dạng 1 (đính cả dạng 2 và 3).

| Dạng | Tên | File prompt (chỉ gửi GPT đường dẫn này) | GPT lưu ảnh vào |
|---|---|---|---|
| 1 | Hải Long Nhi | `D:\PokiClash\ArtGen\Spine\gui_gpt\tm10_1\luot_1_concept.txt` | `D:\PokiClash\ArtGen\Spine\inbox\tm10_1\tai_ve\L1_concept.png` |
| 2 | Hải Long Tam Thủ | `D:\PokiClash\ArtGen\Spine\gui_gpt\tm10_2\luot_1_concept.txt` | `D:\PokiClash\ArtGen\Spine\inbox\tm10_2\tai_ve\L1_concept.png` |

Claude tự gen: `py -3 -I gen.py gui_gpt/tm10_<k>/luot_1_concept.txt` (chạy nền, khoảng 2 phút một ảnh; sửa nhanh thêm `--note "..."`).

## Ảnh mẫu

| Ảnh | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 (dạng 1) | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 (dạng 1) | `D:\PokiClash\ArtGen\Spine\inbox\thuong_lam_3\tai_ve\L1_lien.png` | Rồng băng Thương Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): lấy nét bút, vân sáp, mức chi tiết; không chép dáng |
| 3 (dạng 1) | `D:\PokiClash\ArtGen\Spine\inbox\hai_long\tai_ve\L1_duyet.png` | Concept Hải Long Ngũ Đầu dạng 3 đã duyệt (1536 × 1024, nền trắng): năm đầu rồng xanh ngọc trồi lên từ sóng |
| 4 (dạng 1) | `D:\PokiClash\ArtGen\Spine\inbox\tm10_2\tai_ve\L1_duyet.png` | Concept dạng 2 đã chọn (1536 × 1024, nền trắng): rồng biển trẻ ba đầu |

## Kiểm concept

- **Dạng 1 (Hải Long Nhi)**: Rồng biển con MỘT đầu, chibi (đầu ~40% chiều cao), mắt to tròn màu hổ phách, mõm ngắn, hai nanh nhỏ; vảy xanh ngọc nhạt #6ED3BF, bụng kem nhạt, sừng mới nhú tròn, bờm hồng san hô ba lọn, râu cụt; thân chữ S một khúc trồi từ vũng nước nhỏ, vây đuôi hồng san hô nhô lên bên phải; nước ít.
- **Dạng 2 (Hải Long Tam Thủ)**: Rồng biển trẻ BA đầu (đầu giữa to hơn 20%), xanh ngọc #45B8A4 nhạt hơn dạng 3, bụng kem vàng, vây và bờm san hô ngắn, sừng vàng THẲNG không nhánh, không ngọc trán, chỉ đầu giữa có râu ngắn; nước ít và thấp hơn dạng 3; vòng thân trái, chóp đuôi phải.
- Chung: con vật nhìn sang **phải** người xem, miệng hé thấy lòng miệng hồng; đầu không che nhau, không che đuôi; sóng trước che chỗ thân mọc ra.
- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), không quầng; nền trắng tinh; không chữ, không đường đất.
- Dạng 1 phải **chibi** (đầu to, mắt to), dạng 2 **không** chibi (mõm dài, mắt sắc); dạng 3 phải trông khác hẳn hai dạng trước (đậm màu hơn, năm đầu, gạc phân nhánh, ngọc trán, bờm lớn).

## GPT vẽ sai thì gửi thêm (cùng chat)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |
| Vẽ đủ năm đầu hoặc chép ảnh 3 | `Do not redraw image 3: this is a YOUNGER form with exactly the number of heads described.` |
| Dạng 2 vẫn chibi | `Not chibi: adult proportions, long snout, head about one fifth of the creature's height, sharp eyes.` |
| Dạng 1 không chibi | `Chibi hatchling: the head is about 40% of the creature's height, eyes big and round.` |
| Quay sang trái | `Every head must face the viewer's RIGHT.` |
| Nhiều nước quá | `Much less water: a small ring of two or three little waves only.` |
