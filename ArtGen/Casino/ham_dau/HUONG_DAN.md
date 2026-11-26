# Nền scene Hầm đấu (đấu trường ngầm đảo Casino)

Kế hoạch: `GD_Claude/29_DaoCasino.md` mục 6.5 và mục "Hầm đấu: sàn đấu có Lão Mực". Người dùng dặn 2026-11-26: gen nền đúng kiểu đấu
trường ngầm ở đảo cờ bạc, học cách dựng cảnh của hoạt hình ống cao su thập niên 1930, gen bằng GPT.

Đã gen qua Magnific GPT 2.6 (1k high, 9:16), mỗi lượt 95 credit, phóng classic 2k (preset Art, subtle) 72 credit. Tổng 334 credit
(hai lượt gen + hai lần phóng; bản 1 chỉ giữ làm bản lưu).

| Lượt | File prompt | Ảnh mẫu | Ra |
|---|---|---|---|
| 1 | `luot_1_nen.txt` | 1: `ArtGen/Casino/dealer/d3/nen_leu_bai_1k.png` (nền lều Đêm Bài, dọc 752 x 1344, nét chì sáp tô phẳng, viền mực nâu: lấy nét vẽ và họ đồ vật của đảo); 2: `ArtGen/Islands/refs/world_style.png` (bản đồ thế giới, mẫu nét thứ hai) | `nen_ham_dau_1k_ban1.png`: quầy nhà cái rộng và thấp, Lão Mực đứng vào thì bé tí (bỏ, giữ làm ảnh mẫu lượt 2) |
| 2 | `luot_2_quay_cao.txt` | 1: `nen_ham_dau_1k_ban1.png` (ảnh lượt 1: vẽ lại, giữ mọi thứ); 2: nền lều Đêm Bài như trên | `nen_ham_dau_1k.png` (752 x 1344): quầy cao và hẹp vừa dáng Lão Mực. **Bản đang dùng** |

Phóng 2k: `nen_ham_dau_2k.jpg` (1144 x 2048).

## Trong ảnh có gì

- Trên cùng: trần hầm đá vòm, hai xà gỗ, dây cờ bốn chất bài, bốn lồng đèn giấy hai bên.
- Giữa tường sau: **quầy nhà cái** có mái che sọc đỏ kem, lòng quầy màu kem **để trống** (Lão Mực là rig đặt vào lúc chạy), mép quầy là
  một nét mực ngang thẳng trên dải nỉ xanh; mặt trước quầy có bốn chip và một **biển gỗ trống** treo hai móc (game ghi tên bậc lên);
  dưới quầy là cổng song sắt.
- Hai bên quầy: khán đài gỗ đầy khán giả bóng đen mắt trắng, bảng phấn ghi vạch đếm, thùng gỗ, rương.
- Nửa dưới: **sàn cát tròn để trống** (ba tướng đội ngầm đứng ở đây), tường gỗ đá quây có dây thừng và chip.
- Đáy: mép sàn gần người xem và lưng khán giả hàng đầu (mảng tối, nút bấm nằm đè lên).

## Kiểm

- Không chữ, không số, biển gỗ trống; không nhân vật trong quầy, không gì giữa sàn cát.
- Tô phẳng, không bóng đổ, không quầng sáng quanh đèn, không chuyển màu.
- Mép quầy thẳng ngang (lớp quầy cắt theo một hàng pixel); lòng quầy cao ít nhất 18 % chiều cao ảnh.

## Tách lớp động (cổng sắt, khán giả)

`py -3 -I tach_lop.py` đọc `nen_ham_dau_2k.jpg`, ghi `nen_ham_dau_2k_dong.jpg` (nền dùng trong game: lòng cổng trống, khán giả chỉ còn
mảng tối) và thư mục `lop/`: `cong_song.png` (song sắt), `cong_mat_na.png` (lòng vòm), `kg_duoi_0..4.png` (khán giả hàng đầu),
`kg_xa_0..3.png` (khán giả trên khán đài), `lop.json` (khung từng mảnh theo px ảnh 2k). Soát bằng `lop/lop_mat_na.jpg` (mọi mảnh trên
nền hồng), `lop/lop_xem.jpg` (mọi mảnh nhích hết cỡ), `lop/cong_xem.png` (cổng đóng, nền trống, mở nửa, mở hết). Không tốn credit.

## Đưa vào Unity

Chạy `tach_lop.py` trước. `py -3 -I dua_vao_unity.py` ghi `Assets/03 Art/Casino/HamDau/hd_nen.jpg`, `hd_quay.png` (lớp quầy che thân dưới
Lão Mực), các lớp `hd_cong_*.png`, `hd_kg_*.png`, `ham_dau_lop.txt` (khung từng lớp cho menu dựng) và `ham_dau.json` (số đo trên ảnh 2k). **Gen lại nền thì phải đo lại** mép quầy, lòng quầy, biển gỗ (sửa bảng `M` trong
`dua_vao_unity.py` và các hằng số cùng tên ở đầu `Assets/01 Script/Editor/CasinoUgMenu.cs`), rồi chạy menu
`PokiClash/Prefab/Đảo Casino/Hầm đấu: dựng scene`.

## Câu sửa nhanh (gửi kèm ảnh đang dùng làm ảnh mẫu 1)

- Quầy thấp quá: "Make the booth opening taller: it must span from 12 % to 31 % of the picture height."
- Có chữ trên biển / bảng: "Remove every letter and number. The hanging signboard must be completely blank."
- Có quầng sáng quanh đèn: "Remove the glow around the lanterns: flat colour only, no halo, no light cone."
- Sàn cát có đồ vật: "Clear the pit floor: plain pale ochre sand, only one faint chalk ring."
