# Màn Hang Tiềm Năng: ảnh nền và icon thưởng (2026-11-27)

Người dùng dặn: làm lại màn Hang Tiềm Năng, ít chữ nhưng đủ thông tin, học Hầm đấu và võ đường huy hiệu của Clash of Critters, phần
thưởng đặt trên thanh tiến độ bằng icon. Code: `Assets/01 Script/App/Scenes/CaveScene.cs`, menu dựng `Editor/CaveStageMenu.cs`
("PokiClash/Prefab/Nhà và side meta/Hang Tiềm Năng: dựng sân khấu").

## Đã gen (Magnific GPT 2.6, 1k high)

| File | Là gì | Prompt | Credit |
|---|---|---|---|
| `nen_hang_1k.png` | nền hang 9:16 (752 × 1344): trần thạch nhũ, bảng đá trống, vòm có cầu thang xuống, bệ đá sáng, tiền cảnh tối | `luot_1_nen.txt` | 95 |
| `nen_hang_2k.jpg` | bản phóng classic 2k (preset Art, subtle), 1144 × 2048 | | 72 |
| `icon_thuong_1k.png` | 3 icon trên nền xanh phẳng: đá tiềm năng, đá tinh, đá tiến hóa | `luot_2_icon.txt` | 95 |

Tổng 262 credit. Ảnh mẫu: nền Hầm đấu (`ArtGen/Casino/ham_dau/nen_ham_dau_1k.png`), bản đồ thế giới, icon túi đá tiến hóa của cửa hàng.

## Đưa vào Unity

`py -3 -I dua_vao_unity.py` ghi vào `Assets/03 Art/Cave/`:

- `hang_nen.jpg`: nền dùng trong game, ArtImporter nhập 2048 (luật `/Cave/hang_nen`);
- `hang_da_tiem_nang.png`, `hang_da_tinh.png`, `hang_da_tien_hoa.png`: icon cắt khỏi nền xanh, 192 px vuông;
- `hang.json`: số đo trên ảnh 2k (bảng đá, lòng vòm, mặt bệ, màu đáy).

**Gen lại nền thì phải đo lại** bảng đá (`TabX0..TabY1` trong `CaveStageMenu.cs`), lòng vòm (`Gate`) và chỗ đứng (`Stand`) trong
`CaveScene.cs`, rồi chạy lại menu dựng.

Chữ tiếng Anh của màn: `py -3 -I loc_hang.py` (chỉ thêm khoá chưa có vào `Assets/Resources/Loc/en/ui.json`).

## Soát

Cờ `Temp/cave_stage_tour.flag` cho Unity vào Play, mở Hang, chụp vào `Temp/PokiShots/hang/` (vào màn, tầng đã qua, tầng khoá, đang chạy
ra, hộp chi tiết, cuối tuần chưa chọn / chọn Hỏa, hết lượt, vừa vượt tầng, hộp chuẩn bị trận) và ghi `log.txt`. Bản lưu sao lưu đầu
tour, trả lại cuối tour.
