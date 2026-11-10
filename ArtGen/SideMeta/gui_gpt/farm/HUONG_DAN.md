# Trang trại: gói gửi GPT

Mỗi lượt gửi GPT (hoặc Codex) **đường dẫn một file prompt**; GPT tự mở ảnh mẫu và tự lưu ảnh.

| Lượt | File prompt | Ảnh lưu vào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\SideMeta\gui_gpt\farm\luot_1_nen.txt` | `C:\Atomik\PokiWar\ArtGen\SideMeta\farm\tai_ve\farm_bg.png` |
| 2 | `C:\Atomik\PokiWar\ArtGen\SideMeta\gui_gpt\farm\luot_2_do_vat.txt` | `C:\Atomik\PokiWar\ArtGen\SideMeta\farm\tai_ve\farm_props.png` |

Hai lượt độc lập, làm lượt nào trước cũng được.

## Ảnh mẫu

- `world_style.png` (1024 × 1536, nền giấy kem): bản đồ đảo vẽ tay đã duyệt, chỉ lấy nét (viền mực nâu hơi rung, chì màu gạch chéo).
- `bo_cuc_farm.png` (1024 × 1536, nền xanh cỏ): sơ đồ bố cục: chuồng đỏ trên trái, cối xay gió trên phải, ao xanh dương, vườn cây xanh đậm,
  bãi cỏ thả thú (bầu dục xanh nhạt ở giữa), đống rơm vàng (chỗ thú ngủ), xưởng xám, lò bánh cam, ruộng nâu sọc; 8 ô kem đánh số là chỗ
  tướng đứng làm việc; đường hồng là dải an toàn (trên 8 %, dưới 12 % bị UI che; 80 px hai bên có máy cắt mất).
- `G_Sheet4x3.png` (1536 × 1024): lưới 4 × 3 đánh số cho tấm đồ nghề.

## Cách kiểm

- **Nền:** đúng chỗ từng khu như sơ đồ; 8 chỗ đứng là đất phẳng trống (không cây, đá, đồ đạc); bãi cỏ giữa trống; không vẽ con vật, người,
  chữ; trên và dưới yên (trời, cỏ).
- **Đồ nghề:** 12 món đúng thứ tự, mỗi món một ô, nền trắng phẳng, không bóng đổ.

## Câu sửa nhanh

- `Same farm; keep the eight work spots and the centre meadow completely empty and flat, follow the layout sketch more exactly.`
- `Same farm; no animals or creatures anywhere, no text.`
- `Same sheet; pure white background, no shadows, one item per cell in the numbered order.`
