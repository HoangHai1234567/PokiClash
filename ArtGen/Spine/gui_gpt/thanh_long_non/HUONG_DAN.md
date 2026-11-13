# Gói gen concept dạng 1 và dạng 2 của Thanh Long (suất 10 đảo Mộc, boss)

Dạng 3 là rồng trúc bốn cánh đang có (`moc_vuong_1`). Hai file prompt, mỗi file một lượt gen:
- `luot_1_concept_d1.txt`: **rồng con** (đầu to, sừng là hai mầm măng nhú, bốn cánh lá nhỏ xíu, CHƯA có giáp vàng: cổ áo và vai là bẹ măng
  non xanh, giữa ngực một nụ ngọc) → `tai_ve/L1_d1.png`.
- `luot_1_concept_d2.txt`: **rồng thiếu niên** (sừng măng dài chừng 60 % dạng 3, cánh cỡ 2/3, giáp tre chẻ ngà viền vàng mảnh) → `tai_ve/L1_d2.png`.

Ảnh mẫu (GPT tự mở theo đường dẫn):
1. `inbox/thanh_long_non/mau/bo_cuc_d1.png` / `bo_cuc_d2.png` (1536×1024, nền trắng): rig dạng 3 đổi tỉ lệ (dạng 1: đầu ×1,6, sừng 0,3, cánh
   0,35, đuôi 0,5; dạng 2: đầu ×1,2, sừng 0,6, cánh 0,65, đuôi 0,8), chụp khung 0 idle. Cho dáng, chỗ, cỡ từng mảnh; màu, mặt, sừng, giáp còn là
   của dạng 3.
2. `inbox/moc_vuong_1/tai_ve/L1_duyet.png` (1536×1024): concept dạng 3 đã duyệt (bản tối, sừng măng). Cho nét vẽ, dáng dấp họ hàng.

Cách kiểm: chồng lên bố cục phải trùng dáng và chỗ từng mảnh; một mắt; dạng 1 không có giáp vàng; tô phẳng, không bóng; nền trắng.
Câu sửa nhanh: "keep the exact pose and piece positions of image 1"; "flat colour only, no shading, no highlights";
"no gold armour on the hatchling, only green bamboo sheath leaves".
