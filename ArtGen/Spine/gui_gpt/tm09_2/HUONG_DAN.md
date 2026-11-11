# Gói gửi GPT: dòng Hàn Ngạc, dạng 2 (`tm09_2`)

Cá sấu băng vực sâu, dòng tướng mới đảo Thủy (thay suất ải 60). Dạng 2 (trưởng thành) vẽ trước; dạng 1 (con non chibi) vẽ sau khi dạng 2 được chọn và đính dạng 2 làm ảnh mẫu.

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm09_2\luot_1_concept.txt`. GPT lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm09_2\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm09_2/luot_1_concept.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\hai_long\tai_ve\L1_duyet.png` | Hải Long Ngũ Đầu đã duyệt (1536 × 1024, nền trắng): rồng biển năm đầu, lấy nét bút, vân sáp, mức chi tiết |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\vay_lam_3\tai_ve\L1_lien.png` | Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): thú cá mập bốn chân xanh lam, chỉ lấy kiểu dáng đứng và nét |

## Bảng màu của dòng

| Vùng | Mã |
|---|---|
| body2 | `#1F5566` |
| body1 | `#3C8396` |
| plate | `#3F7585` |
| belly | `#D9E6EA` |
| ice | `#E6F1F4` |
| ice_dk | `#9DBAC6` |
| eye | `#F2B544` |
| mouth | `#1B4F66` |
| tongue | `#4A9BB5` |
| teeth | `#F6FBFD` |
| claw | `#2B3F4A` |
| body2_far | `#1A4756` |
| body1_far | `#336F80` |

## Kiểm concept

- Cá sấu bốn chân thấp người, nhìn nghiêng **quay sang phải**, bốn chân rời nhau, đuôi duỗi sang trái rời chân sau, có cổ.
- Tỉ lệ trưởng thành (đầu khoảng 1/4 chiều dài), mắt hổ phách đồng tử dọc, mày gồ, mặt quả quyết.
- Thân xanh petrol sẫm `#1F5566`, tấm bụng xám băng, vảy sừng to ở vai, hông, gáy.
- Hai sừng băng đục lớn cong ra sau rồi vút lên như lưỡi liềm; gờ băng răng cưa dọc sống lưng; đuôi kết thúc bằng chùy 3–4 pha lê băng.
- Băng **đục, tô phẳng, màu `#E6F1F4`**, chỉ có vài nét mực cạnh; không phải pha lê lam trong (kẻo giống Thương Lam, Kuba).
- Miệng hé, răng kem to, lòng miệng xanh thẫm, thấy lưỡi.
- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), không nước, không băng dưới chân, nền trắng tinh.
- Không giống con gốc tham khảo: không thân trắng, không sừng đen, không lòng miệng tím.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `gen.py ... --note "..."`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, băng trong suốt | `Flat colour only: remove every shadow, highlight, gradient and transparency; the ice is an opaque flat pale colour with thin ink facet lines.` |
| Quay sang trái | `The creature must face the viewer's RIGHT.` |
| Chân dính nhau, đuôi dính chân | `Separate the four legs and the tail with white gaps; no leg crosses another.` |
| Miệng ngậm | `The mouth must be half open, showing the inside of the mouth and the tongue between the teeth.` |
| Có nước, băng dưới chân, hơi lạnh | `Nothing around the creature: no water, no ice floor, no mist, no snowflakes.` |
| Dạng 2 vẫn chibi | `Not chibi at all: adult crocodile proportions, head about one quarter of the body length.` |
| Dạng 1 chưa chibi | `Make it a chibi hatchling: head about 45% of the body length, short snout, chubby short legs.` |

## Lượt 2 (tờ mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\tm09_2\luot_2_manh.txt`

Ba bước M01, M02, M03, gõ `next` sau mỗi ảnh; GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm09_2\tai_ve`. Ảnh mẫu thêm: ảnh 4 = concept dạng 2 đã chọn. Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm09_2/luot_2_manh.txt --steps M01,M02,M03`.

Mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px:
- **M01**: đầu trên (sọ, mắt, mõm, răng trên; không hàm dưới, không sừng), hàm dưới (răng dưới, dải lòng miệng), mảng lòng miệng, một sừng băng liềm (gốc trái), lưỡi duỗi thẳng + hai mí nhắm, chùy pha lê đuôi
- **M02**: thân nằm ngang (cổ bên phải, gốc đuôi bên trái; vảy sừng vai hông; không chân, không gờ), đuôi duỗi thẳng (gốc trái), ba mảnh gờ băng đáy phẳng (vai, lưng, hông)
- **M03**: bốn chân đứng hơi gập gối: trước gần, sau gần, trước xa (tối hơn), sau xa (tối hơn); ba móng chĩa phải
- Kiểm: thân và đuôi **thẳng, nằm ngang**, hai đầu tròn; đầu trên không có hàm dưới, không sừng; sừng / chồi gốc bên trái; lưỡi thẳng; băng đục tô phẳng; mảnh không chạm nhau.


## Lượt 3 (thân, đầu vẽ lại bám hình concept): `D:\PokiClash\ArtGen\Spine\gui_gpt\tm09_2\luot_3_than_dau.txt`

Ba bước M08, M09, gõ `next` sau mỗi ảnh; GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm09_2\tai_ve`. Ảnh mẫu thêm: ảnh 4 = concept dạng 2 đã chọn. Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm09_2/luot_3_than_dau.txt --steps M08,M09`.

Mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px:
- **M08**: thân nằm ngang bám đúng hình concept: cổ dày vươn lên bên phải, tấm họng nhạt từ dưới hàm xuống ngực, ngực và bụng sâu, vẽ đủ phần chân che; không đầu, chân, đuôi, gờ
- **M09**: đầu trên bám hình concept, hàm dưới to bản vẽ khép, lòng miệng, lưỡi ngắn, hai mí; ô dưới phải để trống
- Kiểm: thân và đuôi **thẳng, nằm ngang**, hai đầu tròn; đầu trên không có hàm dưới, không sừng; sừng / chồi gốc bên trái; lưỡi thẳng; băng đục tô phẳng; mảnh không chạm nhau.

