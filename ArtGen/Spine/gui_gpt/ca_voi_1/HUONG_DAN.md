# Gói gửi GPT: dòng `ca_voi` dạng 1 (cá voi biến dị dạng 1)

Tướng thứ 7 đảo Thủy, làm 2026-11-11 theo ý người dùng: cá voi biến dị không có mặt, bỏ sừng, chót đuôi là đá đen dưới biển. Dạng 2 bám con gốc, dạng 1 là cá voi con. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/ca_voi_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\ca_voi_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_voi_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ca_voi_1/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_voi_2\tai_ve\L1_duyet.png` | Cá voi biến dị dạng 2 đã duyệt (1536 × 1024, nền trắng): cá voi lam sẫm không mặt, miệng quả trứng 10 nanh kem rất to, hai vây ngực làm chân có móng đá, đuôi dài kết thúc bằng vây đuôi đá đen |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_voi_1\mau\bo_cuc.png` | Sơ đồ bố cục dạng 1 tự vẽ bằng mã (1536 × 1024, nền trắng): hình phẳng cá voi hình nêm quay phải, không mặt, miệng quả trứng có khoé nhọn, nanh kem rất to đan cài, hàm trên lam sẫm, hàm dưới trắng băng có dải sóng lam, hai vây ngực làm chân có móng đá, đuôi dài thon dần và vây đuôi đá đen hai thuỳ. Lấy cách dựng, bố cục, tỉ lệ |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ti_tach_1\tai_ve\L1_duyet.png` | Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam mắt bầu dục. Chỉ lấy nét bút rung, vân sáp, tô phẳng |
| 4 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\so_gai_2\tai_ve\L1_duyet.png` | Sò đột biến dạng 2 đã duyệt (1536 × 1024, nền trắng): sò gai chàm, vành cam, nanh kem. Lấy cách vẽ nanh, lòng miệng phẳng |
| 5 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự vẽ (`py -3 -I ArtGen/Spine/ca_voi_bo_cuc.py`).

## Kiểm

- Cùng con, cùng cách dựng với dạng 2 nhưng là **cá voi con**: thân ngắn mũm mĩm, đầu to, màu lam nhạt hơn; nhỏ hơn hẳn trong khung.
- Vẫn **không có mặt**; miệng quả trứng có khoé nhọn, lòng miệng hai tông hồng (trên sẫm, dưới nhạt).
- Chỉ **sáu nanh sữa** (ba trên, ba dưới), ngắn mập, không chạm nhau; lộ nhiều lòng miệng.
- Hai vây ngực làm chân chống, ngắn mập; **mấu vây ôm gốc móng đá**, không khoanh trắng.
- Đuôi ngắn thon dần, trơn; chót là **vây đuôi đá đen nhỏ hai thuỳ**; một mẩu đá nhỏ trên lưng đuôi.
- Dải môi trên lam nhạt, dải sóng bụng, lỗ phun, ba con hà nhỏ, hai rãnh họng.
- Tô phẳng, không bóng, không sọc trắng, nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Có mắt, mũi hoặc nét mặt | `Remove every eye, nose and face mark: the creature has NO face at all, only the giant round mouth.` |
| Có bóng, mảng sáng tối, điểm sáng, lòng miệng tối dần | `Flat colour only: remove every shadow, highlight, shine spot and gradient; the inside of the mouth is one flat coral colour; keep the crayon hatching as texture only.` |
| Có lưỡi, họng, nước dãi trong miệng | `The inside of the mouth is completely empty: one flat coral area, no tongue, no throat, no drool.` |
| Nanh hàng trên đè lên nanh hàng dưới | `The two rows of fangs interlock like a zipper but never touch: keep a zigzag band of mouth colour at least 15 px wide between the upper fangs and the lower fangs.` |
| Nanh nhỏ, đều tăm tắp, hiền | `Make the ten fangs HUGE, fat, curved and crooked, each a different size, covering about half of the mouth opening, like the teeth of a deep-sea predator.` |
| Miệng tròn như cái đĩa | `The mouth opening is a tilted egg shape with a long sharp pointed back corner reaching left into the body, as in the layout guide; inside: dark plum roof above, coral floor below.` |
| Thiếu chi tiết, trông sơ sài | `Add every listed detail: the thick upper-lip band, barnacles, scars, blowhole, throat grooves, the two wave crests on the belly band, the kite-shaped thigh with a pointed knee and ankle band, the tail rings and the faceted rock shards with a vein.` |
| Có sừng, vây lưng | `Remove horns and the dorsal fin.` |
| Còn sọc, khoanh trắng ở đuôi hoặc vây; còn vết sẹo, vân sáng | `Remove every white or pale ring, band, stripe, scar and vein line from the tail, the flippers, the head and the rock: these parts are plain flat colour.` |
| Đuôi ngắn cụt | `Make the tail long and whale-like: a tail stock that tapers smoothly over about 380 px before the rock fluke, as in the layout guide.` |
| Móng rời khỏi vây (có khoanh hoặc khe hở) | `The three knuckle lobes at the end of each flipper overlap and wrap the roots of the three rock claws: one continuous limb, no band, no gap.` |
| Đá đuôi bóng loáng như đá quý, hoặc tròn như sỏi | `The rock fluke is matte black sea rock: two angular slabs with straight broken edges and flat dark-grey facets, no sparkle, no shine.` |
| Quay sang trái hoặc nhìn nghiêng hẳn (không thấy lòng miệng) | `Three-quarter view facing the viewer's RIGHT and a little toward the viewer: we look straight into the round open mouth, tail at the left.` |
| Bốn chân | `Only two flipper-legs are visible: the near flipper under the middle of the body and the lower part of the far flipper beside the chin.` |
| Dạng 1 không khác dạng 2 mấy | `Make form 1 a small chubby calf: much shorter body, big round mouth end, lighter blue, only six short milk fangs and a small rock fluke.` |
