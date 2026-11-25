# Logo game vẽ tay (2026-11-24)

Thay logo tạm `Assets/03 Art/Boot/boot_logo.png` (chụp từ chữ SVG của bản web, 776 x 470).

- Gen bằng Magnific (GPT 2.6, 1k high, nền trong suốt, 3:2, 95 credit/ảnh, 3 phương án một lượt).
- Ảnh mẫu: logo tạm (giữ bố cục "Poki" nhỏ trên, "CLASH" to dưới) và `ArtGen/Islands/refs/world_style.png` (nét bút mực, chì màu, sáp).
- `tai_ve/logo_1..3.png`: ảnh gốc 1536 x 1024.
- `logo_1..3.png`: đã xoá điểm mờ xa vật (GPT 2.6 chừa nền độ đục 1–63) và cắt sát, lề 12 px.
- `so_sanh.png`: ba phương án trên nền giấy và nền tối.
- Tỉ lệ khoảng 1,65 như logo tạm, nên thay file `boot_logo.png` không phải sửa khung trong prefab BootTitle, ChuyenTau.

Nhận xét: 1 có lỗ nhỏ ở viền giấy giữa "Poki" và "CLASH"; 2 có một nét nâu thừa cùng chỗ; 3 viền liền, sạch nhất.

Prompt (rút gọn): chữ "Poki" vàng nhỏ, "CLASH" to mỗi chữ một màu hệ theo thứ tự C xanh nước, L đỏ lửa, A xám bạc, S xanh lá,
H đất cam; viền mực nâu sẫm 10–12 px; chì màu gạch chéo bên trong; hai bút chì bắt chéo hoặc chùm sao sau chữ A; viền giấy kem
18 px mép xé; NO SHADOWS (câu luật chung ArtGen/README.md), không glow, không bóng loáng, không 3D; nền trong suốt.
