# Tiểu Thổ Tinh (`thach_de_non`): dạng 1 của tướng 10 đảo Thổ (ải 70, final boss, id `giap_nham`)

Dạng 2 = Thổ Tinh `thach_de` (rig `monster_3802`, ghi chú `thach_de_ghichu.md`, vào game 2026-11-18, hai dạng đang trỏ chung
`Resources/thach_de_1`). Rig, lưới, chuyển động gốc là của nhà phát hành game tham khảo: chỉ dùng nội bộ, không đăng công khai.

## 1. Lời dặn

- 2026-11-18 (máy C): "ok cho vào game đi rồi gen dạng 1 của nó".
- Làm như Thiên Thạch Thú Non (`tinh_hach_non_ghichu.md`): CÙNG rig, đổi tỉ lệ thành con non ngay trên rig dạng 2, Claude đề xuất hai
  hướng concept, người dùng chọn. Tên tạm "Tiểu Thổ Tinh" (`quai/doi_thach_de.py`, `TEN_NON`), người dùng đổi được.

## 2. Tỉ lệ (`thach_de_non.py bocuc`, dựng thẳng trên `inbox/thach_de_1/rig/thach_de_1.atomik` bằng `mo_xe/atomik_dang.py`)

- Thử A, B, C (`mau/so_ti_le.jpg`). **Chọn B** (`mau/ti_le.json`): lõi `bone5` 0,74 (kéo hành tinh, vỏ vai, gai, hai tay nhỏ theo); cổ / đầu
  `bone6` 1,72 (đầu net ~1,27 dạng 2); lưỡi trăng `gai_i` 0,52; vệ tinh `dao_j` 0,7; khối tay `bone10` / `bone18` 1,06 (nắm đấm net 0,78);
  hông `bone` 0,84; hạ `xy` dy −30,2 cho chân chạm đất như dạng 2.
- Con non chỉ SÁU lưỡi trăng (ẩn `P_R_beiji09`, `07`, `04`, `02`), BA vệ tinh (ẩn `ve_3..5`). Bố cục không vẽ hố hành tinh và nửa sau quỹ
  đạo (của clip aura).
- Bố cục `mau/bo_cuc.png` 1536×1024, 1,4828 px / đơn vị; khung từng slot `mau/bo_cuc_khung.json`.

## 3. Concept lượt 1 (`thach_de_non.py concept`; gói `gui_gpt/thach_de_non/`, gen bằng Codex)

Ảnh mẫu 1 = bố cục, 2 = concept dạng 2 đã duyệt (`thach_de_1/tai_ve/L1_duyet.png`). Chung: đầu to tròn, sừng trăng ngắn, mắt hổ phách to
cau mày, nanh sữa; nắm đấm mặt trăng tròn nhỏ ba đốt; vỏ vai nhỏ; ba vệ tinh.

| Hướng | Ảnh | Nội dung |
|---|---|---|
| A · hành tinh non | `tai_ve/L1_A.png` | lõi hành tinh nhỏ bốn dải rộng + một hố lớn; sáu lưỡi trăng ngắn mập như nụ |
| B · trăng non nứt vỏ | `tai_ve/L1_B.png` | lõi còn bọc vỏ đá trăng nứt như vỏ trứng, khe răng cưa lộ dải hành tinh; trên lưng sáu mảnh vỏ vỡ dựng đứng (lớn lên vỏ vỡ hết thành hành tinh có lưỡi trăng) |

Tờ chọn `mau/chon_concept.jpg` (bố cục, A, B có viền bố cục đỏ chồng lên, dạng 2). IoU hình bóng với bố cục: A 0,873, B 0,825.
Claude soi: cả hai đúng dáng, đủ sáu lưỡi / mảnh và ba vệ tinh, tô phẳng, không bóng.
- A: sát bố cục nhất, giữ đúng cơ chế dạng 2 (hố trôi = hành tinh tự quay, lưỡi trăng bay ở chiêu mana); mắt tròn to nên mặt hơi "linh vật".
- B: có điểm nhấn kể chuyện (vỏ trứng đá trăng nứt, lớn lên vỏ vỡ ra hành tinh có lưỡi trăng), mặt dữ gần dạng 2; vỏ và sáu mảnh vỡ là mảnh
  mới (chiêu mana phóng mảnh vỏ thay lưỡi trăng); hành tinh tự quay chỉ còn thấy ở khe nứt.
- Claude đề xuất **B** (độc đáo, nối tiến hoá rõ); A là lựa chọn an toàn.

**Người dùng chọn B (2026-11-18: "làm B")** → `tai_ve/L1_duyet.png` (= `L1_B.png`).

## 4. Mảnh (`thach_de_non.py manh | cat`; gói `gui_gpt/thach_de_non/luot_2_manh_N1|N2.txt`, gen bằng Codex, ra đúng lượt đầu)

- Concept B cùng bảng màu dạng 2 → nắm đấm, cẳng tay, đốt tay, vỏ vai, chân, hông, vệ tinh, bàn tay xoè DÙNG LẠI mảnh dạng 2 (co theo xương).
- Gen lại, vẽ CÙNG CỠ mảnh dạng 2 tương ứng (ảnh mẫu là mảnh dạng 2) để đặt đúng chỗ mảnh cũ trong hệ xương dạng 2:
  `N1` đầu non trọn + đầu non bỏ hàm + hàm dưới kèm lòng miệng + hai nanh sữa; `N2` lõi bọc vỏ nứt (đĩa trọn) + sáu mảnh vỏ vỡ dựng đứng.
  → `manh/non_dau`, `non_dau_tren`, `non_ham`, `non_nanh_1/2`, `non_hanh_tinh`, `non_vo_1..6`.
- Ghép đầu non: `thach_de_dau.py non` (như dạng 2, tham chiếu là đầu non trọn; khoảng dò tỉ lệ ước theo bề ngang). Đầu non: lòng miệng không lòi ra
  ngoài má nên KHÔNG cắt bớt (cắt chỉ đục lỗ trong miệng); có lấp lỗ giấy trắng giữa răng. Tờ so `manh/_dau_so.png`.

## 5. Rig (`TH_DANG=non py -3 -I thach_de_rig.py` → `rig/`)

- Cùng script dạng 2 (cờ `NON`): dựng y như dạng 2 (mảnh gắn theo hệ xương dạng 2; mảnh non_* đặt đúng chỗ mảnh cũ), rồi NHÂN xương theo
  `mau/ti_le.json` và tính lại ma trận dáng gốc: mảnh region / lưới lưu toạ độ theo xương nên co / phóng theo. Lõi bọc vỏ đặt trùng đĩa hành tinh
  (đường kính 2 RHT); bỏ bốn lưỡi (`GAI_AN`), hố, ba vệ tinh; mảnh vỏ ở chỗ lưỡi (bảng `VO_NON`, cao lưỡi × 1,3).
- Clip như dạng 2; chiêu mana phóng SÁU mảnh vỏ (9, 7, 5, 4, 2, 0; `ban` 0,98 + 0,08 j), bán kính lượn theo lõi × 0,74.
- Xuất: 159 xương, 68 slot, 9 clip, 24 sự kiện, `.atomik` 572 KB; mọi clip nối về idle 0,00 px; `kiem`: attack 92° (cú nện của họ), cast 154° ở
  mảnh đang ẩn, skill 42°. Cao 572 (dạng 2: 800). Dạng 2 dựng lại sau khi thêm cờ: JSON trùng từng byte.
- Tiến hoá (`thach_de_non.py th`): gộp dạng 2 bản nhẹ × 0,854 (cỡ 0,92 / 1,10) + clip `evolve` → `rig/thach_de_non_th.atomik` 737 KB, tờ
  `rig/khung_evolve.png`; hố và vệ tinh nửa sau của dạng 2 giữ ẩn (rig gộp không chạy aura).

## 6. Vào game

- `quai/doi_thach_de.py chep_non` (Resources/thach_de_non = bản `_th`) + `dang_1` (dạng 1 "Tiểu Thổ Tinh" → thach_de_non, 0,92). RosterTests.
- VFX dạng 1: bộ số riêng trong `HatThoTinh.cs` (đo `TH_DANG=non thach_de_do_hat.py`), mảnh bay là mảnh vỏ.
- Unity (máy C, 2026-11-18): Nhập dữ liệu, Gắn dạng (prefab giap_nham: thach_de_non → thach_de_1; rig dạng 1 trong game 332 xương, 10 clip kể cả
  evolve), EditMode 133/134 (chỉ `PrefabOnlyTests.MaRuntime_KhongSinhDoVat` hỏng sẵn: NumberTicker / UiMotion). Tour `ThoTinhFxTour` dạng 1, 2.
- Sửa sau tour (`StageViewThoTinh.cs`): ảnh tướng co quanh CHÂN (pivot `AolaSticker.FootV`) nên phải dời LÊN 0,45·H·(1−c) (bản agent dời xuống:
  đối thủ lòi ra dưới quả cầu đá); co thêm một nấc (×1,15 phần co, ~0,32) cho đối thủ bè ngang không lòi mai hai bên. Đã soi lại: nằm gọn trong vỏ.
- Ảnh soi trong game: `inbox/thach_de_non/trong_game_{danh,mana,ult}.jpg` (dạng 2: `inbox/thach_de_1/fx/trong_game_*.jpg`).
