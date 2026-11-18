# Thiên Thạch Thú Non (`tinh_hach_non`): dạng 1 của tướng 9 đảo Thổ (ải 60, id `cu_phu`)

Dạng 2 = thú thiên thạch `tinh_hach` (rig `monster_3806`, ghi chú `tho9_ghichu.md`, đã vào game 2026-11-17, hai dạng đang trỏ chung
`Resources/tinh_hach_1`). Rig, lưới, chuyển động gốc là của nhà phát hành game tham khảo: chỉ dùng nội bộ, không đăng công khai.

## 1. Lời dặn (2026-11-18, máy D)

- "làm dạng 1 cho tướng thứ 9 đảo thổ" (lúc đầu nói nhầm đảo Mộc; suất 9 Mộc đã có Giác Mộc Non từ 11-13).
- Chọn **"Cùng rig 3806"** (đổi tỉ lệ ngay trên rig, như Bùn Ngoạm Nhi / Giác Mộc Non) và **"Claude tự nghĩ 2 hướng"** concept
  (Magnific GPT 2.6, 1k high, 95 credit / ảnh, trần dưới 100).

## 2. Tỉ lệ (`tinh_hach_non.py bocuc`, dựng thẳng trên `Resources/tinh_hach_1/tinh_hach_1.atomik` bằng `mo_xe/atomik_dang.py`, không Chrome)

Máy D không có `scan/monster_3806` (rig dạng 2 dựng ở máy C), nên bố cục chụp từ `.atomik` trong game.

- Thử A, B, C (`mau/so_ti_le.jpg`). Đầu `all6` to thì hàm `all10` to theo, chạm đất → hàm đặt riêng nhỏ lại.
- **Chọn B** (`mau/ti_le.json`): đầu `all6` 1,5; hàm `all10` 0,65 (thật = 0,98); khúc thân sau `all7` 0,8; sống lưng `all4` 0,9; tay
  `dabi_r`, `dabi_l` 0,8; đuôi `duoi0` 0,6; rừng tinh thể `tt_sau`, `tt_truoc` 0,5; tinh thể vắt vai `tt_nam_g` 0,55; năm thiên thạch
  `dao_*` (+ bóng mờ `dao_g1/g2_*`) 0,6; hạ `all3` dy −155,8 cho móng tay gần chạm đất như dạng 2. Cao idle 1274 (dạng 2: 1769).
- Soi dáng gắt bằng da cũ (attack, cast, skill cuộn người, appear, hit, die): không rách lưới.
- Bố cục `mau/bo_cuc.png` 1536×1024, lề 1,24, 0,646 px / đơn vị; khung từng slot ở `mau/bo_cuc_khung.json`. Không vẽ thiên thạch bay /
  quả cầu (concept tự vẽ ba thiên thạch theo lời, ở chỗ trắng `THIEN_THACH`).

## 3. Concept lượt 1 (`tinh_hach_non.py concept`; gói `gui_gpt/tinh_hach_non/`, gen thẳng bằng công cụ Magnific trong phiên, 190 credit)

Ảnh mẫu 1 = bố cục, 2 = concept dạng 2 đã duyệt (`tinh_hach_1/tai_ve/L1_duyet.png`). Chung: da đá vỏ chai đen mềm hơn, hai mạch hổ phách
mảnh; đầu to tròn, mõm ngắn, một mắt hổ phách tròn cau mày; mào năm nụ hổ phách thấp; tay ngắn ba móng; ba thiên thạch nhỏ bay
(dạng 2 có năm cụm).

| Hướng | Ảnh | Nội dung | IoU với bố cục |
|---|---|---|---|
| A · mầm tinh thể | `tai_ve/L1_A.png` | lưng nhú ba mầm tinh thể (ngọc lam cao giữa, hai hổ phách hai bên) + hai nụ nhỏ dọc sống lưng; đuôi một lưỡi ngọc lam | 0,876 |
| B · vỏ thiên thạch | `tai_ve/L1_B.png` | lưng đội vỏ thiên thạch xám nâu rỗ ba hố, nứt răng cưa (GPT vẽ khe nứt hổ phách, ba chóp ngọc lam nằm trên mép vỏ chứ không lọt qua khe); đuôi nụ ngọc lam | 0,883 |

Tờ chọn `mau/chon_concept.jpg` (bố cục, A, B có viền bố cục đỏ chồng lên, dạng 2). Claude soi: cả hai đúng dáng, chi dính thân, ba thiên
thạch không chạm thân, tô phẳng, không bóng. Thân vẫn khá giống dạng 2 (cơ bắp), con non chủ yếu nhờ đầu to, tay ngắn, lưng ít tinh thể.
Đề xuất **A** (mầm tinh thể lớn thành rừng tinh thể: nối với dạng 2 rõ nhất; vỏ của B là mảnh mới phải tự dựng xương cho lúc cuộn người).
**Chờ người dùng chọn** → `tai_ve/L1_duyet.png`.

## 4. Việc tiếp (sau khi chọn)

1. Mảnh: đo màu, chỉ gen lại chỗ khác hẳn dạng 2 (đầu + mào, lưng tinh thể / vỏ, đuôi, ba thiên thạch); mảnh còn lại đổi màu từ dạng 2.
2. Rig dạng non trên `.atomik` dạng 2 (`atomik_dang`: `scale_bones` theo `ti_le.json`, thay mảnh, ẩn 2/5 thiên thạch, co quỹ đạo nguyên tử,
   co quả cầu `bong` của chiêu cuối, dời `mieng`), clip `evolve` (`gop_tien_hoa`).
3. Vào game: `Resources/tinh_hach_non`, forms trong `heroes.json` (dạng 1 tên tạm "Thiên Thạch Thú Non"), Unity: Nhập dữ liệu, Gắn dạng,
   golden, test.
