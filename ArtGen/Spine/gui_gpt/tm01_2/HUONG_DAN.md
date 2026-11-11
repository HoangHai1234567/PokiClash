# Gói gửi GPT: dòng `tm01` dạng 2 (Sóng Thần)

Lô 10 tướng mới đảo Thủy, dòng 1 (thay suất ải 1, tướng khởi đầu hệ Thủy). Đặc tả: `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`; ghi chú thiết kế: `ArtGen/Spine/inbox/tm01_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm01_2\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm01_2\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm01_2/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\vay_lam_3\tai_ve\L1_lien.png` | Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): cá mập xanh đậm dạng cuối, dữ. Lấy nét, độ dữ của dạng cuối |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\lam_quan_2\tai_ve\L1_lien.png` | Lam Quân dạng 2 đã duyệt (1536 × 1024, nền trắng): kỳ lân lam mang chuông, giáp. Lấy cách vẽ giáp, vải đơn giản |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\tm01_1\tai_ve\L1_duyet.png` | Tí Tách dạng 1 đã chọn (1536 × 1024, nền trắng): giữ họ màu, mào sóng, băng đô đỏ, mắt; không chép tỉ lệ chibi |
| 4 | `D:\PokiClash\Assets\03 Art\Fx\no_nuoc.png` | Vụ nước toé đã duyệt (512 × 505, nền trong): dáng nước cho bờm sóng, găng nước, chóp đuôi |
| 5 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.

## Kiểm

- Thú rồng kỳ giông nước đứng hai chân thế tấn, đầu khoảng 28% chiều cao, **không chibi**, **không thân người lực sĩ** (không cơ ngực, cơ bụng, vai người); cả thân nghiêng 3/4 sang phải; bóng dáng khác hẳn dạng 1.
- Màu chủ đạo **chàm đậm**, sọc và bờm lam sáng, ngực bụng bọt nhạt.
- Bờm ba mào sóng cuộn ra sau, khăn đỏ hai dải dài, găng nước trên cẳng tay, giáp vỏ ốc ở vai gần và ống chân, đai đỏ có ngọc hình giọt nước.
- Mắt sắc, nanh, miệng hé gầm thấy lòng miệng; dữ, chiến, không đáng sợ.
- Nhìn sang **phải**, tay chân tách thân, không chéo; đuôi dài có chóp mào sóng bên trái.
- Tô phẳng: không bóng, không điểm sáng (trừ chấm mắt), không quầng; nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng | `Flat colour only: remove every shadow, highlight, shine spot and gradient; keep the crayon hatching as texture only.` |
| Thành thạch trong suốt bóng loáng | `The body is an opaque flat aqua colour with crayon texture, not glassy jelly: no reflections, no transparency, no shine.` |
| Quay sang trái | `Mirror the creature so it faces the viewer's RIGHT.` |
| Tay dính thân, chéo nhau | `Keep both arms apart from the body with a thin white gap; nothing crosses the face.` |
| Có giọt, bong bóng bay quanh | `Remove every loose drop, bubble and splash around the creature; only the creature on pure white.` |
| Dạng 2 vẫn chibi | `Not chibi at all: adult proportions, the head about one quarter of the total height, tall lean warrior body.` |
| Dạng 2 thành người lực sĩ, nhìn thẳng | `Much less human: no human chest muscles, abs, shoulders or hands; the build of an upright water-dragon newt beast; turn the whole body to a true three-quarter side view facing the viewer's right.` |

## Lượt 2: tờ mảnh rời (pha 2, sau khi concept Sóng Thần được duyệt)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm01_2\luot_2_manh.txt`, 2 bước M01, M02, gõ `next` sau mỗi ảnh. GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm01_2\tai_ve`.

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm01_2/luot_2_manh.txt --steps M01,M02`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\tm01_2\tai_ve\L1_duyet.png` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng) |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\hai_long\tai_ve\M01.png` | Tờ mảnh M01 của Hải Long đã duyệt (1536 × 1024): cách bày mảnh rời trên giấy trắng; không chép nội dung |
| 3 | `D:\PokiClash\Assets\03 Art\Fx\no_nuoc.png` | Vụ nước toé đã duyệt (512 × 505, nền trong) |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét |

Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ít nhất 60 px, mảnh dài (tay, chân, đuôi, dải) duỗi thẳng, đúng màu concept, tô phẳng không bóng.

- **M01**: đầu phần trên (sọ đủ, mắt mở, mày, mõm trên có nanh, vây má, băng đô có nút; không hàm, không bờm, không dải) · hàm dưới có lòng miệng và nanh · mảng lòng miệng + mí mắt nhắm · hai mào sóng của bờm (to, nhỏ) · hai dải khăn duỗi thẳng · đuôi duỗi thẳng có chóp mào sóng
- **M02**: thân (không đầu, tay, chân, đuôi, giáp vai, dải đai) · một cánh tay duỗi thẳng vai → cổ tay có găng nước + vây · nắm đấm · bàn tay xoè đẩy · một chân duỗi thẳng hông → cổ chân có giáp vỏ sò · bàn chân ba ngón · giáp vai vỏ ốc · dải đai thả

| Sai | Gửi thêm |
|---|---|
| Vẽ cả con thay vì mảnh rời | `This must be a sheet of separate parts laid flat on white, not a creature. Redraw only the parts listed.` |
| Tay, chân, đuôi, dải vẽ cong | `The limbs, the tail and the ribbons must be drawn perfectly straight, like a ruler.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |

## Lượt 3: chân liền cả chi + đuôi chóp to (sau lần soi của Claude điều phối)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm01_2\luot_3_chan.txt`. GPT lưu `D:\PokiClash\ArtGen\Spine\inbox\tm01_2\tai_ve\M03.png`. Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm01_2/luot_3_chan.txt`.

- **M03**: chân liền cả chi (đùi to, gối, ống chân, bọc vỏ sò), hai đầu tròn kín, không bàn chân · đuôi duỗi thẳng có chóp mào sóng to như concept
- Kiểm: đùi to rõ ràng (gần gấp đôi ống chân), hai đầu chân tròn kín không có nắp ống; đuôi chóp cuộn to; tô phẳng.
