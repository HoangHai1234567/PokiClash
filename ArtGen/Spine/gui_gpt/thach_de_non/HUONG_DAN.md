# Gói gen: Tiểu Thổ Tinh (`thach_de_non`), dạng 1 tướng 10 đảo Thổ (ải 70, id `giap_nham`)

Rig: `monster_3802` (game tham khảo) đổi tỉ lệ. Ảnh mẫu 1 mang lưới / da dựng từ rig đó: chỉ dùng trong máy, không đăng công khai.

## Lượt 1: concept dạng 1, hai hướng (2026-11-18)

Người dùng: "ok cho vào game đi rồi gen dạng 1 của nó". Dựng trên cùng rig (như Thiên Thạch Thú Non), Claude đề xuất hai hướng. Ảnh 1 là bố cục dạng non (tỉ lệ đã đổi trên rig, còn mang da dạng 2); ảnh 2 là concept dạng 2 đã duyệt để giữ nhận diện.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thach_de_non\mau\bo_cuc.png` | Bố cục dạng non: rig Thổ Tinh đổi tỉ lệ (thân trên 0,74, đầu net ~1,27, nắm đấm nhỏ, sáu lưỡi trăng ngắn, ba vệ tinh), còn mang da dạng 2, nền trắng 1536×1024, con nhìn sang phải. Giữ dáng, chỗ, cỡ từng bộ phận |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thach_de_1\tai_ve\L1_duyet.png` | Concept dạng 2 (Thổ Tinh, B2Y) đã duyệt: lõi hành tinh đá kẻ dải, nắm đấm mặt trăng, vỏ vai và lưỡi trăng đá trăng có hố, mặt nạ thú sừng trăng mắt hổ phách nanh kem, vệ tinh bay quanh. Lấy chất liệu, màu, nét bút, vân sáp; không lấy tỉ lệ người lớn |

- **Hướng A** (hành tinh non: lõi hành tinh nhỏ, chỉ bốn dải rộng (kem, vàng đất, đỏ gạch) và MỘT hố tròn lớn; sáu lưỡi trăng ngắn mập như nụ; đầu to, sừng trăng ngắn, mắt to cau mày, nanh sữa): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\thach_de_non\luot_1_concept_A.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thach_de_non\tai_ve\L1_A.png` (trùng tên thì `_2`, `_3`…).
- **Hướng B** (trăng non nứt vỏ: lõi hành tinh còn bọc trong VỎ ĐÁ TRĂNG nứt như vỏ trứng (nửa trên vỏ xám tím có hố, khe nứt răng cưa ngang lộ dải hành tinh bên trong); trên lưng là sáu mảnh vỏ vỡ dựng đứng thay cho lưỡi trăng; lớn lên vỏ vỡ hết thành hành tinh có lưỡi trăng): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\thach_de_non\luot_1_concept_B.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thach_de_non\tai_ve\L1_B.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py <file prompt>` (Codex). Bản được chọn chép thành `L1_duyet.png` cùng thư mục.

Kiểm: đúng dáng, chỗ, cỡ từng bộ phận như ảnh 1 (hành tinh giữa, đầu to phía trước bên phải, nắm đấm to thấp bên trái, nắm đấm nhỏ bên phải, vỏ vai trên mỗi nắm đấm, sáu lưỡi / mảnh trên lưng, ba vệ tinh); rõ là cùng loài với ảnh 2; mắt to, mặt quả quyết; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng, chỉ một chấm sáng trong mỗi mắt; nền trắng tinh; không viền sticker.

Câu sửa nhanh: "too many details: simplify"; "remove the shading / highlights / glow, flat colour only"; "keep every part at the same place and size as image 1"; "make the head rounder and the eyes bigger, keep the determined frown".

## Lượt 2: hai tờ mảnh dạng 1 (2026-11-18)

Người dùng chọn B ("làm B") → `L1_duyet.png`. Nắm đấm, vỏ vai, chân, vệ tinh, bàn tay xoè dùng lại mảnh dạng 2; gen lại đầu non (tách hàm), lõi bọc vỏ, sáu mảnh vỏ, vẽ cùng cỡ mảnh dạng 2 tương ứng.

- **Tờ N1**: đầu non trọn (ngậm), đầu non bỏ hàm (hàng nanh trên), hàm dưới kèm lòng miệng, hai nanh sữa rời. File prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\thach_de_non\luot_2_manh_N1.txt`; ảnh lưu `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thach_de_non\tai_ve\M_N1.png`. Ảnh mẫu: 1 = concept B, 2 = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thach_de_1\manh\dau.png`. Kiểm: đủ 5 mảnh rời, viền kín.
- **Tờ N2**: lõi hành tinh bọc vỏ nứt (đĩa trọn, không gì che), sáu mảnh vỏ vỡ dựng đứng. File prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\thach_de_non\luot_2_manh_N2.txt`; ảnh lưu `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thach_de_non\tai_ve\M_N2.png`. Ảnh mẫu: 1 = concept B, 2 = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thach_de_1\manh\hanh_tinh.png`, 3 = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\thach_de_1\manh\luoi_1.png`. Kiểm: đủ 7 mảnh rời, viền kín.
