# Gói gửi GPT: dòng `tm01` dạng 1 (Tí Tách)

Lô 10 tướng mới đảo Thủy, dòng 1 (thay suất ải 1, tướng khởi đầu hệ Thủy). Đặc tả: `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`; ghi chú thiết kế: `ArtGen/Spine/inbox/tm01_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm01_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm01_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm01_1/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\canh_cut_1\tai_ve\L1_lien.png` | Cánh Cụt dạng 1 đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi hai chân cầm chảo. Lấy khung, dáng chibi hai chân, nét bút, tô sáp; không chép loài, màu |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\vay_lam_1\tai_ve\L1_lien.png` | Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân, mặt quả quyết. Lấy nét, độ chi tiết, nét mặt |
| 3 | `D:\PokiClash\Assets\03 Art\Fx\no_nuoc.png` | Vụ nước toé đã duyệt (512 × 505, nền trong): mũi nước mập, bọt tròn, lam phẳng. Lấy dáng nước cho mào, đuôi |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.

## Kiểm

- Giọt nước mập đáy tròn, chóp **cuộn sang phải như mào sóng** có viền bọt, không phải chóp nhọn thẳng.
- Có tay ngắn nắm đấm, hai bàn chân ngắn, đuôi giọt toé nhỏ; **băng đô đỏ**, nút sau đầu, hai dải bay sang trái.
- Mảng bụng nhạt hình giọt nước ngược, vài sọc sóng lam đậm trên lưng.
- Mắt to tròng kem, tròng đen xanh chàm, mày xếch, miệng hé thấy lòng miệng và một răng nanh nhỏ: quả quyết, không cười.
- Nhìn sang **phải**, tay chân tách thân, không chéo nhau; không giọt nước, bong bóng bay quanh.
- Tô phẳng: **không** bóng, không điểm sáng (trừ chấm trong mắt), không kiểu thạch trong suốt bóng loáng; nền trắng tinh.

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

## Lượt 2: tờ mảnh rời (pha 2, sau khi concept Tí Tách được duyệt)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm01_1\luot_2_manh.txt`. GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm01_1\tai_ve`.

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm01_1/luot_2_manh.txt --steps M01`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\tm01_1\tai_ve\L1_duyet.png` | Concept dạng 1 đã duyệt (1536 × 1024, nền trắng) |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\hai_long\tai_ve\M01.png` | Tờ mảnh M01 của Hải Long đã duyệt (1536 × 1024): cách bày mảnh rời trên giấy trắng; không chép nội dung |
| 3 | `D:\PokiClash\Assets\03 Art\Fx\no_nuoc.png` | Vụ nước toé đã duyệt (512 × 505, nền trong) |
| 4 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét |

Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ít nhất 60 px, mảnh dài (tay, chân, đuôi, dải) duỗi thẳng, đúng màu concept, tô phẳng không bóng.

- **M01**: thân giọt nước có mào cuộn, sọc, bụng, băng đô có nút, hai mắt + mày, KHÔNG miệng · bốn miệng (hét, há tròn, mím, nghiến răng) · bốn mảng mắt (nhắm mắt gần, nhắm mắt xa, mắt `>` gần, mắt `<` xa) · tay duỗi thẳng có nắm đấm + bàn chân · đuôi duỗi thẳng chóp toé + hai dải băng đô

| Sai | Gửi thêm |
|---|---|
| Vẽ cả con thay vì mảnh rời | `This must be a sheet of separate parts laid flat on white, not a creature. Redraw only the parts listed.` |
| Tay, chân, đuôi, dải vẽ cong | `The limbs, the tail and the ribbons must be drawn perfectly straight, like a ruler.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |
