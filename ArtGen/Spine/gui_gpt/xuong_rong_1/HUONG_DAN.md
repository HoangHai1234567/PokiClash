# Gói gửi GPT: `xuong_rong` dạng 1 (xương rồng tròn không mặt, tướng đầu tiên đảo Mộc, tên chưa đặt)

Làm 2026-11-12: reskin theo khung part của con gốc `monster_3229`; màu và chi tiết là đề xuất của Claude, chờ người dùng duyệt concept. Ghi chú: `ArtGen/Spine/inbox/xuong_rong_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_1\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/xuong_rong_1/luot_1_concept.txt` (thêm `--note "..."` để sửa nhanh).

Lượt 2 (tờ mảnh theo khung part) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_1\mau\bo_cuc.png` | Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): quả cầu xương rồng lục lam, miệng cười khổng lồ nanh kem lòng đỏ rượu, vành hoa hồng trên đỉnh lệch trái, tay trước nắm ba gai bên trái, tay sau giơ lên bên phải, hai chân ngắn, năm gai kem trên thân. Lấy cách dựng, chỗ đặt, tỉ lệ, thứ tự chồng |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_voi_1\tai_ve\L1_duyet.png` | Cá voi biến dị dạng 1 đã duyệt (1536 × 1024, nền trắng): cá voi lam nhỏ há miệng to, nanh kem. Lấy nét bút rung, vân sáp, tô phẳng, mức chibi mà chiến của dạng 1, cách vẽ miệng và nanh |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_vay_1\tai_ve\L1_duyet.png` | Rồng vây đã duyệt (1536 × 1024, nền trắng): rồng rắn chàm tím có cánh vây. Lấy nét, tô phẳng, tông màu trầm |
| 4 | `C:\Atomik\PokiWar\ArtGen\Islands\refs\world_style.png` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp |

Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/xuong_rong.py bo_cuc`).

## Kiểm

- **Không mặt**: không mắt, mày, mũi; cái miệng cười khổng lồ đầy nanh là cả mặt. Thân là **một quả cầu** xương rồng lục lam có **múi dọc** (nét lục sẫm) và nốt gai kem nhỏ.
- Miệng hình bát, hai khoé vểnh lên; **nanh là gai kem to**, lởm chởm, trên dưới cài nhau; lòng miệng **đỏ rượu** phẳng.
- **Vành hoa hồng** bảy cánh nhọn trên đỉnh lệch trái (không phải mào đỏ). **Năm gai to** trên thân; mỗi nắm tay **ba gai**.
- Tay trước (bên trái người xem) chĩa sang trái; tay sau (bên phải) giơ lên, nấp sau thân; hai chân ngắn dạng rộng, ngón chân kem.
- Mỗi bộ phận có viền mực kín riêng. Tô phẳng: **không** bóng, không mảng sáng tối trên thân, không điểm sáng; nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Vẽ thêm mắt, mũi, mặt | `It has NO face: remove the eyes, eyebrows and nose. The giant fanged mouth is the only feature.` |
| Có bóng, mảng sáng tối, loang màu trên thân | `Flat colour only: remove every shadow, highlight, lighter blotch and gradient; the ball is one even green with thin rib lines; keep the crayon hatching as texture only.` |
| Quá dễ thương, cười hiền | `Make it a cocky little brawler: bigger jagged thorn fangs, a wider grin, the fist raised. Not a sweet mascot.` |
| Quá đáng sợ, quái dị | `Keep it appealing: chubby, compact, clean shapes, no gore, no drool, no cracks.` |
| Thân không tròn, hoặc thành cây xương rồng có nhánh | `The body is ONE round ball (a barrel cactus), almost all mouth; no branches, no column, no pot.` |
| Mào đỏ, tóc, lá | `On top there is only a low crown of magenta-pink pointed cactus-flower petals: no red crest, no hair, no leaves.` |
| Bố cục khác sơ đồ | `Follow image 1 exactly: the front arm at the left reaching left, the back arm raised at the upper right, the mouth slightly right of the middle, the flower crown on the top left.` |
| Răng trắng đều như răng người | `The teeth are big irregular cream cactus THORNS, jagged and interlocking, not neat white teeth.` |

## Lượt 1b: A pose (2026-11-12)

Người dùng xem bản nháp `L1_concept.png` và dặn: tay bên phải (tay sau) thõng xuống kiểu A pose, không cần giơ lên như con gốc. Lượt này vẽ lại y hệt bản nháp, chỉ đổi tay sau.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_1\luot_1b_apose.txt`. Ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_1\tai_ve\L1_apose.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_1\tai_ve\L1_concept.png` | Bản nháp concept (1536 × 1024, nền trắng): xương rồng cầu lục, miệng cười nanh kem lòng đỏ rượu, vành hoa hồng, tay sau còn giơ lên bên phải trên |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_1\mau\bo_cuc.png` | Sơ đồ bố cục dáng mới (1536 × 1024, nền trắng): như trên nhưng tay sau thõng xuống bên phải quả cầu, nắm tay ngang nửa dưới thân |

Kiểm: mọi thứ ngoài tay sau trùng bản nháp; tay sau thõng bên phải, nắm tay lộ hẳn ngoài quả cầu, đủ ba gai; hai gai thân bên phải (trên, dưới) còn nguyên; vẫn không có mặt.

## Lượt 1c: bỏ nét môi (2026-11-12)

Người dùng xem bản A pose: "cảm giác như có phần môi ở trên, bỏ line vẽ môi đi". Lượt này vẽ lại y hệt `L1_apose.png`, chỉ bỏ nét mực lượn phía trên miệng (nét làm thành vành môi trên); múi dọc của thân chạy tiếp xuống tới mép miệng.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_1\luot_1c_bo_moi.txt`. Ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_1\tai_ve\L1_khong_moi.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_1\tai_ve\L1_apose.png` | Bản A pose (1536 × 1024, nền trắng): xương rồng cầu lục, miệng cười nanh kem lòng đỏ rượu, vành hoa hồng, hai tay nắm ba gai; phía trên miệng có nét mực lượn làm thành vành môi trên |

Kiểm: không còn nét môi, không dải môi; da thân chạy thẳng tới mép lỗ miệng, múi dọc chạy tiếp tới mép miệng; mọi thứ khác trùng bản A pose; vẫn không có mặt.

## Lượt 2: ba tờ mảnh theo khung part (2026-11-12, sau khi người dùng duyệt `L1_duyet.png`)

Mỗi tờ một file prompt; ảnh 1 là concept đã duyệt, ảnh 2 là tờ hướng dẫn (hình bóng phẳng từng part đúng khung ảnh vùng của rig, dựng bằng `py -3 -I ArtGen/Spine/xuong_rong.py nhom_part`). Codex lưu `N_A.png`, `N_B.png`, `N_C.png` vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_1\tai_ve`.

| Tờ | File prompt | Tờ hướng dẫn (1536 × 1024, nền trắng) trông như thế nào |
|---|---|---|
| A | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_1\luot_2_manh_A.txt` | Ba hình lớn: quả cầu lục có múi dọc và nốt gai (trái), vành da quanh lỗ miệng chỉ viền mực ở mép lỗ (giữa), khối đỏ rượu lòng miệng (phải) |
| B | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_1\luot_2_manh_B.txt` | Mười hai hình: hàm nanh trên, hàm nanh dưới (kem), vành hoa bảy cánh hồng, chín khúc tay chân lục, trong đó hai bàn chân có ngón kem |
| C | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_1\luot_2_manh_C.txt` | Mười một gai nón kem mỗi gai một hướng, một gai dài và một gai kim rất dài nằm ngang chĩa sang phải, một ụ đất nâu |

Kiểm (Claude tự làm): `xuong_rong.py cat_part <tờ>` in IoU từng ô với hình bóng (dưới 0,9 thì gen lại tờ đó), `xuong_rong.py so_part` vẽ tờ so (đỏ = thiếu, xanh lá = thừa).
