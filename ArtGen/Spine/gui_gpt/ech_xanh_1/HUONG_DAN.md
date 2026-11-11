# Gói gửi GPT: dòng `ech_xanh` dạng 1 (ếch xanh dạng 1 (chưa đặt tên))

Tướng thứ 2 đảo Thủy, người dùng lên ý 2026-11-11: ếch xanh lưỡi đỏ; dạng 2 cùng con, to hơn, chiến hơn. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/ech_xanh_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\ech_xanh_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ech_xanh_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ech_xanh_1/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\vay_lam_1\tai_ve\L1_lien.png` | Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Chỉ lấy nét bút, vân sáp, cách tô phẳng |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\canh_cut_1\tai_ve\L1_lien.png` | Cánh Cụt dạng 1 đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi. Lấy độ đơn giản, tròn trịa, vẻ quả quyết |
| 3 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.

## Kiểm

- Một con **ếch xanh lá tròn như cục bánh**, đầu liền thân không cổ, hơi rộng hơn cao; nửa trên lưng và đầu xanh, nửa dưới phía trước là **bụng kem to tròn, trơn**.
- **Miệng khép** là đường ranh xanh và kem, rất rộng, hai khoé hơi trễ xuống (quả quyết, không cười).
- **Lưỡi đỏ** dẹt thè ra từ miệng, buông thẳng trước bụng như dải ruy băng, có viền mực riêng, đầu lưỡi tròn có khía nhỏ; **không chạm đất, không chạm chân**.
- Hai **mắt ếch lồi** trên đỉnh đầu, tròng vàng nhạt, con ngươi bầu dục ngang nhìn sang phải, mí trên xanh sụp một phần ba; **không có hình xoắn ốc** ở đâu cả.
- **Ba chi lộ ra**: tay gần chống đất phía trước đùi, đùi gần to tròn bên trái dưới với bàn chân màng ba ngón, bàn tay xa ló dưới bụng bên phải. **Chân sau bên kia khuất hẳn** (bên phải chỉ thấy một chi). Không đuôi.
- Vài đốm xanh đậm trên lưng (phía trái trên). Nhìn nghiêng 3/4 sang **phải**, ngồi yên.
- Tô phẳng: **không** bóng, không điểm sáng, không ướt bóng; viền mực nâu; nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng trắng trên da, bụng, lưỡi | `Flat colour only: remove every shadow, highlight, shine spot, darker rim and gradient; keep the crayon hatching as texture only. The only white dot is the tiny one inside each pupil.` |
| Miệng há hoặc cười toe | `The mouth is CLOSED: one long wide line where the green meets the cream belly, corners turned slightly down; the tongue comes out from under the upper lip.` |
| Lưỡi cong, vắt sang bên, chạm đất hoặc chạm chân | `The tongue hangs straight down in front of the belly like a flat ribbon and ends about 90 px above the bottom of the belly; it touches neither the ground nor the feet.` |
| Bên phải thấy hai chi (thừa chân) | `On the far (right) side exactly ONE limb is visible: the small far hand under the belly. Remove the far hind leg completely; it is hidden behind the body.` |
| Mắt có xoắn ốc hoặc bụng có hoa văn | `No spiral or swirl anywhere: plain pale-yellow eyeballs with a horizontal oval pupil; the belly is plain cream with no marks.` |
| Quay sang trái hoặc nhìn thẳng | `Turn the frog three-quarters toward the viewer's RIGHT: pupils look right, the far eye is smaller and partly hidden, the near thigh is at the lower-left.` |
| Mặt hiền, cười, quá dễ thương | `Give it a determined, stubborn, battle-ready face: heavy upper eyelids slanting down toward the nose, mouth corners turned down. Still cute, not scary.` |
| Dạng 2 chỉ là dạng 1 phóng to, vẫn dễ thương | `Form 2 is a burly fighter, not an enlarged baby: broader shoulders and jaw, smaller eyes relative to the body, eyelids covering half of each eye and slanting steeply, blunt brow ridges, a hard scowl, a thick arm, a longer tongue with a heavy club tip.` |
| Dạng 2 đổi dáng, đổi chỗ các phần | `Keep exactly the pose and layout of image 1: sitting three-quarters to the right, mouth closed, tongue hanging straight in front of the belly, near arm planted on the ground, near thigh at the lower-left, far hand at the lower-right.` |
| Có đất, vũng nước, lá sen, ruồi | `Remove everything around the frog: pure white background, no ground, no props.` |
