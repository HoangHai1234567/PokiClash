# Gói gửi GPT: `xuong_rong` dạng 2 (xương rồng tròn không mặt, to hơn và chiến hơn; cùng rig với dạng 1)

Làm 2026-11-12. Lời dặn của người dùng: "dạng 2 sẽ to hơn chiến hơn chút nhưng form người vẫn vậy". Màu và chi tiết là đề xuất của Claude, chờ duyệt concept. Ghi chú: `ArtGen/Spine/inbox/xuong_rong_ghichu.md`.

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_2\luot_1_concept.txt`. GPT tự mở ảnh mẫu và lưu ảnh vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_2\tai_ve\L1_concept.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/xuong_rong_2/luot_1_concept.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_2\mau\bo_cuc.png` | Hình dạng 1 đã duyệt dựng trên rig với tỉ lệ dạng 2 (1536 × 1024, nền trắng): gai dài hơn, hai nắm tay to hơn, vành hoa cao hơn; màu và chi tiết vẫn của dạng 1. Lấy dáng, cách dựng, chỗ đặt, cỡ từng bộ phận |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_1\tai_ve\L1_duyet.png` | Concept dạng 1 đã duyệt (1536 × 1024, nền trắng). Lấy nét bút, vân sáp, tô phẳng; con mới là chính nó lớn lên |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\ca_voi_2\tai_ve\L1_duyet.png` | Cá voi biến dị dạng 2 đã duyệt (1536 × 1024, nền trắng): mức "dữ" và mật độ chi tiết của một dạng 2 |

## Kiểm

- Cùng dáng, cùng chỗ đặt với ảnh 1: thân cầu, miệng, vành hoa, hai tay (tay sau thõng A pose), hai chân, đủ 5 gai thân + 3 gai mỗi nắm tay. **Không mặt, không môi.**
- Da lục **sẫm hơn**, múi lục rất sẫm; nốt gai thành **gai nhỏ nhọn**; gai lớn **dài, kem trơn một màu** (không mũi hồng, đỏ).
- Nanh **to, dài, lởm chởm hơn**, có nanh dài như ngà; lòng miệng đỏ rượu sẫm.
- Vành hoa bảy cánh **dài nhọn như lưỡi dao**, hồng đỏ sẫm. Nắm tay to như chùy gai.
- Tô phẳng, không bóng, nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)

| Sai | Gửi thêm |
|---|---|
| Vẽ thêm mắt, mũi, môi | `It has NO face and NO lips: remove the eyes, eyebrows, nose and any lip line.` |
| Đổi dáng, đổi chỗ bộ phận | `Follow image 1 exactly for the pose and the placement of every part; only the colours and details change.` |
| Vẫn hiền như dạng 1 | `Make it fiercer: longer jagged fangs, a snarling grin, blade-like petals.` |
| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient.` |

## Lượt 1b: gai kem trơn (2026-11-12)

Người dùng xem bản nháp `L1_concept.png`: "bỏ màu hồng ở gai dạng 2 đi". Lượt này vẽ lại y hệt bản nháp, chỉ bỏ mũi hồng đỏ của các gai lớn (gai kem một màu từ gốc tới mũi).

**Chỉ gửi GPT đường dẫn:** `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_2\luot_1b_gai_kem.txt`. Ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_2\tai_ve\L1_gai_kem.png`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_2\tai_ve\L1_concept.png` | Bản nháp dạng 2 (1536 × 1024, nền trắng): xương rồng cầu lục sẫm, nanh dài, vành hoa lưỡi dao hồng đỏ, gai lớn kem có mũi hồng đỏ |

Kiểm: mọi gai lớn kem trơn, không còn mũi hồng và nét ngăn; mọi thứ khác trùng bản nháp.

## Lượt 2: ba tờ mảnh dạng 2 theo khung part (2026-11-12, sau khi người dùng duyệt `L1_duyet.png`)

Ảnh 1 là concept dạng 2 đã duyệt, ảnh 2 là tờ hướng dẫn (`XR_DANG=2 py -3 -I ArtGen/Spine/xuong_rong.py nhom_part`). Codex lưu `N_A.png`, `N_B.png`, `N_C.png` vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\xuong_rong_2\tai_ve`. Gai lớn, gai dài, ụ đất dùng lại của dạng 1.

| Tờ | File prompt | Tờ hướng dẫn (1536 × 1024, nền trắng) trông như thế nào |
|---|---|---|
| A | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_2\luot_2_manh_A.txt` | Quả cầu lục sẫm có múi dọc và các tam giác kem nhỏ (chỗ gai nhỏ), vành da quanh lỗ miệng chỉ viền mực ở mép lỗ, khối đỏ rượu sẫm lòng miệng |
| B | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_2\luot_2_manh_B.txt` | Hai dải nanh kem của dạng 1 (nanh còn ngắn, quanh có khoảng trắng để vẽ nanh dài ra), vành hoa bảy cánh nhọn như lưỡi dao hồng đỏ |
| C | `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\xuong_rong_2\luot_2_manh_C.txt` | Chín khúc tay chân lục sẫm, hai bàn chân có ngón kem |

Kiểm (Claude tự làm): `XR_DANG=2 xuong_rong.py cat_part` in IoU (tờ A, C dưới 0,9 thì gen lại; tờ B vẽ tự do: soi dải lợi còn đúng chỗ, nanh dài ra đúng phía).
