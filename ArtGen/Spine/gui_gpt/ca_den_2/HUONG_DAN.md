# Gói gửi GPT: dòng `ca_den` dạng 2 (cá đèn lồng dạng 2 (chưa đặt tên))

Tướng thứ 3 đảo Thủy, người dùng lên ý 2026-11-11: cá đèn lồng có chân, đuôi thằn lằn, thân chân đuôi một mảng màu; dạng 2 cùng con, to hơn, chiến hơn. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/ca_den_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\ca_den_2\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_den_2\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ca_den_2/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_den_1\tai_ve\L1_duyet.png` | Cá đèn lồng dạng 1 đã duyệt (1536 × 1024, nền trắng): cá tròn màu chàm, hàm dưới và bụng kem, răng chĩa lên, cần đèn vàng vươn ra trước trán, hai chân, đuôi thằn lằn bên trái |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ech_xanh_1\tai_ve\L1_duyet.png` | Ếch xanh dạng 1 đã duyệt (1536 × 1024, nền trắng): ếch xanh lá tròn, bụng kem, lưỡi đỏ. Chỉ lấy nét bút, vân sáp, cách tô phẳng, độ đơn giản và vẻ quả quyết |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\vay_lam_1\tai_ve\L1_lien.png` | Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Chỉ lấy nét bút, vân sáp, cách tô phẳng |
| 4 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.

## Kiểm

- Cùng con với dạng 1, **cùng dáng đứng và cùng cách xếp các phần**, nhưng **to, nặng, bè hơn hẳn** (chiếm gần hết khung), chàm **đậm hơn**.
- Mặt **dữ hơn**: mí sụp nửa mắt, xếch mạnh, mỗi mắt có một **gờ mày nhọn tù**; khoé miệng trễ hẳn; **năm răng**, hai nanh to. Không ác.
- **Cần đèn dày và dài hơn**, bóng đèn to nặng như chuỳ (chụp chàm có ba gai tù); vẫn không chạm mặt, không phát sáng.
- Vây lưng cao, bốn gai dài; chân to khoẻ, ngón có vuốt ngà tù; đuôi dày dài hơn, có hàng bốn gai tù dọc sống đuôi.
- Thân, chân, đuôi vẫn **một mảng màu liền**; bụng kem trơn.
- Nhìn nghiêng 3/4 sang **phải**; tô phẳng, không bóng, không điểm sáng; viền mực nâu; nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối, điểm sáng trắng trên da, bụng, răng, bóng đèn | `Flat colour only: remove every shadow, highlight, shine spot, darker rim and gradient; keep the crayon hatching as texture only. The only white dot is the tiny one inside each pupil.` |
| Bóng đèn phát sáng, có tia, có quầng | `The lantern bulb is a plain flat warm-yellow shape with an ink outline: remove every glow, ray, halo and sparkle, and any light on the face.` |
| Bóng đèn đè lên mặt hoặc chạm đầu | `Move the lantern bulb up and forward so it hangs in the air in front of the face with at least 50 px of white between the bulb and the head; only the root of the stalk touches the forehead.` |
| Chân hoặc đuôi khác màu thân | `The legs, the feet and the whole tail are exactly the same deep indigo as the upper body: one continuous colour mass, no different colour on them.` |
| Đuôi cá, đuôi có vây hoặc có lửa | `The tail is a plain LIZARD tail: thick at the base, tapering to a pointed tip, curving up to the left; no fin, no flame, no tuft at its end.` |
| Miệng há hoặc cười | `The mouth is CLOSED: one long wide line where the indigo meets the cream lower jaw, corners turned down, with the lower teeth pointing up over the upper lip.` |
| Có tay hoặc bốn chân | `Exactly two legs and no arms: the near leg at the lower-left and the far leg under the belly at the lower-right. Remove every other limb.` |
| Quay sang trái hoặc nhìn thẳng | `Turn the creature three-quarters toward the viewer's RIGHT: pupils look right, the far eye is smaller and partly hidden, the tail is on the left, the lantern arches to the right.` |
| Mặt hiền, cười, quá dễ thương | `Give it a grumpy, stubborn, battle-ready face: heavy upper eyelids slanting down toward the front, mouth corners turned down. Still cute, not scary.` |
| Quá nhiều chi tiết (vảy, mang, sọc) | `Simplify: no scales, no gills, no stripes; only three flat spots on the back.` |
| Dạng 2 chỉ là dạng 1 phóng to, vẫn dễ thương | `Form 2 is a burly fighter, not an enlarged baby: heavier jaw, five teeth with two big fangs, smaller eyes relative to the body, eyelids covering half of each eye with blunt brow ridges, a thicker stalk with a heavy mace-like bulb, a taller back fin, spikes along the tail.` |
| Dạng 2 đổi dáng, đổi chỗ các phần | `Keep exactly the pose and layout of image 1: standing three-quarters to the right on two legs, mouth closed, lantern arching forward, tail curving up on the left.` |
