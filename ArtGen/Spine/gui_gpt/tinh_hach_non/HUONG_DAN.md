# Gói gen: Thiên Thạch Thú Non (`tinh_hach_non`), dạng 1 tướng 9 đảo Thổ (ải 60, id `cu_phu`)

Rig: `monster_3806` (game tham khảo) đổi tỉ lệ. Ảnh mẫu 1 mang lưới / da dựng từ rig đó: chỉ dùng trong máy, không đăng công khai.

## Lượt 1: concept dạng 1, hai hướng (2026-11-18, Magnific GPT 2.6, 1k high, 95 credit / ảnh)

Người dùng: "làm dạng 1 cho tướng thứ 9 đảo thổ", chọn dựng trên cùng rig 3806 và để Claude tự nghĩ hai hướng. Ảnh 1 là bố cục dạng non (tỉ lệ đã đổi trên rig, còn mang da dạng 2); ảnh 2 là concept dạng 2 đã duyệt để giữ nhận diện.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Spine\inbox\tinh_hach_non\mau\bo_cuc.png` | Bố cục dạng non: rig thú thiên thạch đổi tỉ lệ (đầu to 1,5 lần, hàm nhỏ, tay ngắn, đuôi ngắn, rừng tinh thể thu nhỏ), còn mang da dạng 2, nền trắng 1536×1024, con nhìn sang phải, không có thiên thạch bay. Giữ dáng, chỗ, cỡ từng bộ phận |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\tinh_hach_1\tai_ve\L1_duyet.png` | Concept dạng 2 (Thiên Thạch Thú, hướng D2) đã duyệt: da đá vỏ chai đen mạch hổ phách, rừng trụ tinh thể ngọc lam + hổ phách trên lưng, năm cụm tinh thể bay. Lấy chất liệu, màu, nét bút, vân sáp; không lấy tỉ lệ người lớn |

- **Hướng A** (mầm tinh thể: lưng chỉ nhú BA mầm tinh thể ngắn mập (ngọc lam cao nhất ở giữa, hai mầm hổ phách thấp hai bên) + hai nụ nhỏ dọc sống lưng; đuôi kết bằng MỘT lưỡi tinh thể ngọc lam nhỏ (dạng 2 là cả rừng tinh thể, đuôi ba lưỡi)): file prompt `D:\PokiClash\ArtGen\Spine\gui_gpt\tinh_hach_non\luot_1_concept_A.txt`; ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tinh_hach_non\tai_ve\L1_A.png` (trùng tên thì `_2`, `_3`…).
- **Hướng B** (vỏ thiên thạch: lưng đội một VỎ THIÊN THẠCH tròn nứt (đá xám nâu rỗ ba bốn hố nhỏ, như mai rùa / vỏ trứng), nứt một đường răng cưa trên đỉnh, lộ ba chóp tinh thể ngọc lam (lớn lên vỏ vỡ thành rừng tinh thể); đuôi kết bằng một nụ tinh thể ngọc lam khép): file prompt `D:\PokiClash\ArtGen\Spine\gui_gpt\tinh_hach_non\luot_1_concept_B.txt`; ảnh lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tinh_hach_non\tai_ve\L1_B.png` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen_magnific.py <file prompt>` (hoặc gọi thẳng công cụ Magnific trong phiên). Bản được chọn chép thành `L1_duyet.png` cùng thư mục.

Kiểm: đúng dáng, chỗ, cỡ từng bộ phận như ảnh 1 (đầu to bên phải, hàm hé, thân gù, tay gần bên trái chống đất, tay xa vươn dưới đầu, đuôi ngắn bên trái); rõ là cùng loài với ảnh 2 (da đá đen mạch hổ phách, tinh thể ngọc lam + hổ phách); một mắt, mặt quả quyết; đủ ba thiên thạch nhỏ bay không chạm thân; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng, chỉ một chấm sáng trong mắt; nền trắng tinh; không viền sticker.

Câu sửa nhanh: "too many details: simplify"; "remove the shading / highlights / glow, flat colour only"; "keep every part at the same place and size as image 1"; "make the head rounder and the eye bigger, keep the determined frown".
