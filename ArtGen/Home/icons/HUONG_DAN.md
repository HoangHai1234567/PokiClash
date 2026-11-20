# Icon công trình màn Nhà

Hai lượt, mỗi lượt một file prompt (GPT tự mở ảnh mẫu theo đường dẫn trong file, tự lưu ảnh):

| Lượt | File prompt | Lưu vào | Cỡ |
|---|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Home\icons\icons_A.txt` | `D:\PokiClash\ArtGen\Home\icons\tai_ve\icons_A.png` | 1024 x 1024, lưới 4 x 4 |
| 2 | `D:\PokiClash\ArtGen\Home\icons\icons_B.txt` | `D:\PokiClash\ArtGen\Home\icons\tai_ve\icons_B.png` | 1536 x 1024, lưới 4 x 3 |

Ảnh mẫu:
- `world_style.png`: mốc nét vẽ (bút mực nâu sẫm, chì màu, sáp màu), cảnh đảo.
- `refs/buildings_A.png`: 15 công trình đang có trên đảo (ảnh trong `Assets/03 Art/Home/home_b_*.png`), mỗi ô một số, nền trắng, 1200 x 1200; ô 16 trống (hàng rào gỗ, GPT tự vẽ).
- `refs/buildings_style.png`: ghế, xích đu, giếng, cây bi (mẫu nét và góc cho đồ trang trí), 1200 x 300.
- `refs/grid_4x4.png`, `refs/grid_4x3.png`: lưới ô đánh số xám nhạt trên nền trắng.

Kiểm: mỗi ô đúng một món, đúng thứ tự, không chữ số, không bóng đổ, không món nào tràn sang ô bên.
Câu sửa nhanh: `Same icons, same order; each icon fully inside its own cell, simpler shapes, thicker outlines, no shadows.`

Cắt: `py -3 -I ArtGen/Home/icons/build_icons.py cat` rồi Unity "PokiClash/Dựng lại danh mục ảnh".
