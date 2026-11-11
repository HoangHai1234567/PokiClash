# Gói gửi GPT: dòng tm03, dạng 2 (Ếch Lốc)

Lô 10 tướng mới đảo Thủy (đặc tả `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`), pha 1: concept trọn con một ảnh. Ghi chú thiết kế cả dòng: `D:\PokiClash\ArtGen\Spine\inbox\tm03_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm03_2\luot_1_concept.txt`. GPT tự mở ảnh mẫu theo đường dẫn ghi trong file và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm03_2\tai_ve\L1_concept.png` (trùng tên thì `L1_concept_2.png`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm03_2/luot_1_concept.txt` (chạy nền; thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\vay_lam_3\tai_ve\L1_lien.png` | Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): cá voi sát thủ bốn chân xanh lam, phục thấp thế vồ, nhìn sang phải. Lấy khung, thế đứng, thần thái dữ, nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\tm03_1\tai_ve\L1_duyet.png` | Concept dạng 1 đã chọn (1536 × 1024, nền trắng): nòng nọc tròn xanh cerulean, đuôi cuộn xoắn ốc |
| 3 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |

Không đính ảnh con gốc (game khác) hay ảnh chụp trang xem: thiết kế chỉ tả bằng lời.

## Kiểm ảnh

- Ếch sừng to, nặng, **phục thấp bốn chi thế vồ**, nhìn sang phải; không chibi, không mảnh kiểu ninja, không đứng như người.
- Lưng **lam cô-ban** đậm tươi, **đốm tròn đen chàm và vòng gợn đồng tâm** (như giọt rơi xuống mặt nước); **không xoắn ốc nào trên thân, đầu, bụng**; vằn móc chỉ ở cẳng chân; bụng, cằm vàng chanh nghệ trơn.
- Mắt hổ phách con ngươi ngang, mày nặng hạ xuống; **sừng mí mắt nhọn dẹt vuốt thẳng ra sau** (cô-ban, mép sau lam nhạt), không cuộn, không giống sừng cừu Ma Kết.
- Miệng hé **khoé trễ xuống, gầm dữ** (không cười, không nhếch), thấy lòng miệng hồng đậm, lưỡi, hàng răng nhỏ và hai nanh.
- **Túi kêu** vàng trơn phồng dưới cằm (rộng cỡ đầu), chỉ có 2–3 gợn đen chàm ở mép dưới, không xoắn ốc; không che chân trước.
- **Áo choàng lá súng lục lam** (`#2F8A7A`, gân `#5FB8A6`, có khía) phủ vai và lưng, buộc chéo ngực bằng dây sậy vàng rơm, khoá tròn vàng khắc xoắn ốc nhỏ (xoắn ốc duy nhất); băng dây sậy ở cẳng tay trước. Không vỏ ốc, không giáp kim loại.
- Không đuôi; chân trước, chân sau tách nhau bằng khe trắng; tô phẳng, không bóng, nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng trên da | `Flat colour only: remove every shadow, highlight, shine spot and gradient; keep the crayon hatching as texture; only one small catchlight dot in each eye.` |
| Quay sang trái | `Mirror the creature so it faces the viewer's RIGHT.` |
| Mặt cười, vui tươi | `More determined face: heavy lowered brows, focused eyes, mouth slightly open, not a happy grin.` |
| Miệng khép | `Open the mouth slightly so the deep-rose inside of the mouth and the tongue are visible.` |
| Chân tay dính nhau, dính thân | `Leave clear white gaps between the legs and between the legs and the body.` |
| Còn chibi, đầu to | `Not chibi at all: a big heavy grown-up horned frog, the head about one third of its body length, powerful limbs.` |
| Đứng hai chân như người, hoặc mảnh như ninja | `It crouches low on all four limbs like a real frog, heavy and broad, ready to pounce.` |
| Còn đuôi | `No tail: the grown frog has lost its tail.` |

## Lượt 2: tờ mảnh (cách lai: thân chính cắt từ concept, tờ này chỉ cho phần tách / bị che)

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm03_2\luot_2_manh.txt`, các bước M01, M02 (gõ `next` sau mỗi ảnh). GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm03_2\tai_ve`.

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm03_2/luot_2_manh.txt --steps M01,M02`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\tm03_2\tai_ve\L1_concept_3.png` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng) |
| 2 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ (1024 × 1536) |

Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px, đúng cỡ và hình như trên concept, tô phẳng.

- **M01**: thân không bốn chân (nguồn vẽ bù chỗ chân che), lòng miệng có lưỡi, lưỡi duỗi, mí mắt gần nhắm, mí mắt xa nhắm
- **M02**: chân sau xa trọn (cả đùi bị che), chân trước xa trọn (cả cánh tay trên bị che)

| Sai | Gửi thêm |
|---|---|
| Mảnh khác hình, khác cỡ concept | `Draw each part with the same silhouette, proportions and size as on image 1.` |
| Đuôi vẽ cong | `The tail must be a ruler-straight horizontal ribbon, root on the left, tapering to the tip on the right.` |
| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |
