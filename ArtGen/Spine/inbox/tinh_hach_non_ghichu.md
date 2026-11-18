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
**Người dùng chọn A (2026-11-18, máy C: "làm A")** → `tai_ve/L1_duyet.png` (= `L1_A.png`).

## 4. Mảnh (máy C, 2026-11-18; `tinh_hach_non.py can | manh | manh_bong | cat`)

- Căn concept A lên bố cục (`mau/can.json`, tờ `mau/_can.jpg`): px bố cục = 1,04 · px concept + (−25, −31,1); IoU thân 0,934, cả con 0,916
  (chưa căn 0,876). `tf()` = px concept A → bố cục → rig dạng 1 (`canvas_map` của bố cục).
- Đo màu: da concept A (84, 62, 67) trùng da mảnh dạng 2 (80–90, 62–68, 67–74) → thân, hai tay, móng, lòng miệng DÙNG LẠI mảnh dạng 2
  (co theo xương như bố cục), không đổi màu.
- Gen lại (Magnific GPT 2.6, 1k high, 95 credit / tờ, 285 credit; gói `gui_gpt/tinh_hach_non/luot_2_*.txt` + `HUONG_DAN_luot_2.md`): `M_N1`
  đầu (diềm năm nụ, mắt tròn, hai nanh trên, không hàm dưới / lòng miệng) + đuôi một lưỡi; `M_N2` hàm dưới (ba răng sữa) + ba mầm tinh thể và
  hai nụ (chân kéo dài ~18 px dưới sống lưng); `M_bong` quả cầu chiêu cuối vẽ lại cho con non (quả cầu dạng 2 mang mặt người lớn, rừng tinh thể
  dày, đuôi ba lưỡi): mặt con non, ~10 gai tinh thể ngắn, đuôi một lưỡi. Mảnh trùng chỗ concept (soi chồng).
- Ba thiên thạch cắt thẳng từ concept (cụm rời viền kín). `manh/dat.json`: hộp px concept A. Hàm mới mép dưới phía sau dài hơn concept (như hàm
  dạng 2), nằm đè đầu cẳng tay xa cùng màu.

## 5. Rig (`TH_DANG=non py -3 -I tinh_hach_rig.py` → `rig/`)

- Cùng script dạng 2: xương của họ nhân `ti_le.json` ngay sau khi dựng (`ap_ti`; lưu ý `sk.the_gioi()` không đối số chỉ trả bản chép W0 cũ,
  phải `the_gioi(khung.Pose())`). Mảnh dạng 2 gắn trong `Khung2` (tạm trả tỉ lệ về gốc, điểm gắn theo hệ xương nên co theo xương); mảnh mới
  gắn thẳng theo concept A trên bộ xương đã co (`gan_moi`: lưới gộp của họ da hoá lại bằng W0 mới, `att_co`). Xương riêng đặt theo concept
  A: đuôi `DUOI_J_NON`, chân mầm `Y_CHAN_MAM` 330 px, quỹ đạo theo hộp thân + đầu của bố cục (tâm (81, 816), bán trục 939 × 244: đầu to nên bề
  ngang gần bằng dạng 2), quả cầu × 0,9 (giữ phép thu của ảnh dạng 2 cho ảnh mới). Bỏ slot tinh thể vắt vai (concept A không có; xương giữ cho
  clip). Ba thiên thạch: sự kiện `phong` / `no` / `tro_lai` cắt theo số thiên thạch.
- **Sửa chiều há hàm (cả dạng 2)**: đo hộp slot theo giờ, attack 0,40 (pha "há to") hàm xoay LÊN chui vào đầu (hộp hàm chồng hộp đầu 240 đv,
  hàm khuất sau đầu), cú đớp thì lại hé: góc dương của `all10` là KHÉP. `HA = -1` nhân vào mọi khoá `all10` (idle, rũ mình, attack, gầm cast /
  skill / appear). Sau sửa: há to lộ lòng miệng, không hở nền. Bản dạng 2 trong game CHƯA xuất lại.
- Xuất: 103 xương, 28 slot, 4670 đỉnh, 9 clip, 29 sự kiện, `.atomik` 348 KB (đạt đích 0,4 MB); mọi clip nối về khung 0 idle 0,00 px, idle khép
  vòng 1,2 px; `kiem`: chỉ còn cú vồ lao attack 0,47 s và góc 36–46°/khung ở die (clip die_01 gốc), như dạng 2. Cao (game.height) 1474 (dạng 2:
  1595; đầu to nên đỉnh diềm cao). Trang `rig/xem.html` chạy đủ 8 clip (`thu_xem`); runtime Spine thật `rig/that/*.jpg` khớp bộ vẽ Python.
- Tiến hoá (`tinh_hach_non.py th`): dạng 2 bản nhẹ (Resources/tinh_hach_1) × 1,106 (cỡ 0,92 / 1,10), `rig/tinh_hach_non_th.atomik` 600 KB,
  tờ `rig/khung_evolve.png`. Thiên thạch của dạng 2 trong rig gộp không chạy aura (đứng ở dáng gốc tới khi game đổi sang sticker dạng 2).

## 6. Vào game (người dùng 2026-11-18 xem rig + tiến hoá: "cho vào game đi")

- `quai/doi_tinh_hach_non.py`: `heroes.json` khối `cu_phu` dạng 1 = "Thiên Thạch Thú Non" (tên tạm), aola `tinh_hach_non`, cỡ 0,92 (aola /
  size chung của tướng theo dạng 1); dạng 2 giữ `tinh_hach_1` 1,1. Ải 60 đã có `"evo": true`. Chép `rig/tinh_hach_non_th.atomik` (bản gộp
  tiến hoá, 600 KB) + chân dung vào `Resources/tinh_hach_non/`. Xoá `Resources/cu_phu_1`, `cu_phu_2` (không còn tham chiếu GUID nào).
- Hiệu ứng (`HatThach.cs`): bộ số theo dạng `ThtDang` (ThtD2 = số cũ; ThtD1 đo bằng `ArtGen/Spine/tinh_hach_do_hat.py`, script đo lại đúng từng
  số bảng dạng 2): điểm xoa tay, điểm xoáy, ba chỗ phóng, bảng tâm quả cầu theo giờ, bán kính cầu 0,337; `muc` 0,75 (nổ, rung, chớp, vành lửa
  nhẹ hơn dạng 2). Mã `n_thach_xoay1`, `n_thach_cau1` (HatNuoc.PlayNuoc), `StageView.ThoFx` cu_phu theo dạng; đòn thường `n_thach_vo` dùng chung.
- `RosterTests`: assert forms cu_phu = tinh_hach_non, tinh_hach_1. `ThachFxTour`: chú thích, menu sao 1 = dạng 1.
- Biên dịch thử ngoài Unity (Game, Editor, Tests: 0 lỗi; script scratchpad `csc_game.py` đọc csproj Unity sinh). Unity (dừng Play với sự đồng ý
  của người dùng): refresh, Nhập dữ liệu (57 tướng, 350 ải), Gắn dạng (`cu_phu: prefab giữ 2 dạng (tinh_hach_non, tinh_hach_1)`, rig gộp 228
  xương, 10 clip), EditMode 122/123 (hỏng PrefabOnlyTests do UI/Kit NumberTicker / UiMotion có từ commit 5f403ea9, không liên quan),
  chụp thử `Library/PokiHeroShots/cu_phu_atomik_1.png`: đủ clip, evolve ra dạng 2. Golden không chạy lại (chỉ đổi hình).

## 7. Việc tiếp

1. ~~Tour trận~~ (11:11, sau khi phiên Thạch Đế trả Unity): `Temp/PokiShots/tho_fx/cu_phu_1sao_*.jpg` (16 khung đòn thường, 30 mana, 40 chiêu
   cuối): tia đá toé giữa hai bàn tay lúc xoa, ba thiên thạch kéo lửa lao trúng đối thủ; chiêu cuối bụi bung lúc cuộn, cầu vọt lên, lao xuống
   trùm lửa, nổ trên đối thủ, nảy về: lửa / bụi bám đúng quả cầu dạng 1.
2. Hỏi người dùng: xuất lại dạng 2 với chiều há hàm đã sửa (`HA = -1`)? Nếu có: `py -3 -I tinh_hach_rig.py` → `quai/doi_tinh_hach.py chep`, rồi
   `tinh_hach_non.py th` (gộp lại dạng 2 mới vào bản tiến hoá) → `doi_tinh_hach_non.py`, Unity Gắn dạng.
