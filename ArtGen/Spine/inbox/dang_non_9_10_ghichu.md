# Dạng non của suất 9 (Giác Mộc, `moc_tinh`) và dạng 1, 2 của suất 10 (Thanh Long, `thanh_long`), đảo Mộc

Bắt đầu 2026-11-13 (máy ổ C). Người dùng: "tạo thêm dạng 1 cho tướng thứ 9 và dạng 1/2 cho tướng thứ 10"; chọn hướng: suất 9 "thú non chibi",
suất 10 "con non → thiếu niên → boss" (dạng 3 giữ rồng trúc `moc_vuong_1`).

## Cách dựng bố cục (máy C không có dữ liệu quét `scan/monster_3804`, `monster_3709`)

Đổi tỉ lệ xương NGAY TRÊN `.atomik` trong game (dạng lớn), chụp khung bằng runtime Spine thật:
- `mo_xe/atomik_spine.py`: `.atomik` → Spine 4.2 JSON + atlas (một vùng cả trang) + png (đúng nghĩa AtomikPose: xoay, dời cộng; tỉ lệ nhân;
  lưới có trọng số cùng khuôn; `noScale` → inherit noScale; `sa` → alpha; mặt nạ → clipping).
- `mo_xe/atomik_bocuc.py <atomik> <tỉ lệ.json> <ra.png> [clip] [giây] [--khung x0,y0,x1,y1] [--an slot,..]`: nhân scaleX/Y dáng gốc ở xương
  gốc từng cụm (`{"xương": k}` hoặc `{"xương": {"s": k, "dx": .., "dy": ..}}`), chụp Chrome ngầm.
- Đã soi các clip gắt bằng da cũ trước khi gen (suất 9: skill mở ngực, attack, cast, appear, die; suất 10: skill 3 khung, fly, attack, appear):
  không rách. Suất 10 dạng 1 clip `fly`: hai chân sau duỗi ra sau lộ dài (dạng 3 có cánh / đuôi che) → lúc dựng rig co chân sau trong `fly`.

## Tỉ lệ

- Suất 9 non (`giac_moc_non/mau/ti_le.json`): thân `bone2` 0,85; đầu `bone24` 1,5; bốn chân `bone6, bone15, bone31, bone52` 0,8; chuỗi lá lưng
  `timao_*` 0,5; xương lưng `lujin_bozi_3_1..10` 0,7; hạ cả con `bone` dy −150.
- Suất 10 dạng 1 (`thanh_long_non/mau/ti_le_d1.json`): đầu `all6` 1,6; sừng `jiao, jiao2` 0,3; bốn gốc cánh `all63, all127, all38, all155` 0,35;
  đuôi `all9, all16` 0,5; hạ thân `all2` dy −25 (chân ngắn lại; bàn chân là con của `all`, không theo thân).
- Suất 10 dạng 2 (`ti_le_d2.json`): đầu 1,2; sừng 0,6; cánh 0,65; đuôi 0,8; `all2` dy −10.

## Concept (người dùng chốt 2026-11-13: "suất 9 dạng A; suất 10 dạng 1 và 2 ổn đấy")

- Gói: `build_giac_moc_non.py` → `gui_gpt/giac_moc_non/`; `build_thanh_long_non.py` → `gui_gpt/thanh_long_non/`.
- Ảnh: `giac_moc_non/tai_ve/L1_nu.png` (**chọn**), `L1_mam.png` (bỏ); `thanh_long_non/tai_ve/L1_d1.png`, `L1_d2.png` (chọn cả hai).
- Trang so: `inbox/dang_non_xem_concept.html`.

## Rig (dựng thẳng trên .atomik dạng sau, `mo_xe/atomik_dang.py`)

- `mo_xe/atomik_dang.py`: tính tư thế chép `AtomikPose.cs` (khớp runtime Spine thật: khung ôm trùng, IoU hình bóng 0,99), bộ vẽ tam giác,
  `scale_bones`, `recolor` (dời màu Lab theo cặp màu cũ → mới, giữ vân chì sáp, px mực giữ), `add_regions` + `set_quad` (thay mảnh bằng ô cứng
  cắt từ concept, nới atlas), `sway` (khoá đung đưa tự viết, khép vòng từng clip), `gop_tien_hoa` (dạng sau bản nhẹ atlas × 0,5, slot ẩn sẵn
  `fade` 1; clip `evolve` 3 s: dạng trước gồng rung rồi mờ 1,05–1,35 s, dạng sau hiện, lớn dần, chạy đoạn cuối idle và dừng ĐÚNG khung 0 idle
  của nó: đo lệch 0,000). Atlas lưu bảng màu 256 (như `xuat.ghi_spine`). `mo_xe/cat_concept.py`: cắt bộ phận khỏi concept (vùng kín ngăn bởi nét
  mực, nằm ≥ 70 % trong đa giác, + nét mực ôm). `mo_xe/to_khung.py`, `mo_xe/kiem_dang.py`, `mo_xe/chong_vien.py`: soi.
- **Giác Mộc Non** (`giac_moc_non.py` → `giac_moc_non/rig/`): đầu liền nụ sừng = ô cứng `dau` trên bone65; bốn lá mào cắt từ concept thành ô
  cứng trên bốn xương MỚI `la_0..3` (con bone65; rig gốc để mào trên chuỗi cổ, lúc cúi đầu gốc lá lệch tới ~200 px so với đầu) + đung đưa
  ±4,5°; `mieng` dời về đỉnh nụ sừng; lá lục sẫm → lục non, thân sáng ấm hơn. 546 xương, 944 KB, cao 1148 (dạng 2: 1287).
- **Thanh Long dạng 1, 2** (`thanh_long_non.py` → `thanh_long_non/rig_d1/`, `rig_d2/`): sọ + hàm trên `tou_01` (all8), hàm dưới `tou_02`
  (all13; hàm há tới 57° ở cast / skill), hai sừng (jiao, jiao2), mắt nhắm `biyan` (vẽ bằng mã, vân lông lấy cạnh mắt) cắt từ concept; đường
  miệng dò theo nét mực, hàm chờm 10 px sau sọ (không khe); bỏ `tou_04`, dạng 1 bỏ lá trán `tou_05`. Dạng 1: giáp vàng → bẹ măng xanh, đốt cổ
  và vòng ống chân → kem ngà; dạng 2: giáp → tre ngà viền vàng. Mỗi file ~1,2 MB, 1024 xương (mang dạng sau cho evolve).
- Clip gốc giữ nguyên (chỉ đổi tỉ lệ xương): nối về idle như bản gốc; bước dời mỗi khung cùng cỡ bản gốc.

## Vào game (`quai/doi_dang_non_9_10.py`, chạy lại không đổi thêm)

- `Resources/giac_moc_1` = Giác Mộc Non (trước là bản sao giac_moc_2); `Resources/moc_vuong_d1`, `moc_vuong_d2` (mới) = Thanh Long dạng 1, 2;
  `heroes.json` aola của dạng 1, 2 Thanh Long; `RosterTests` assert ba thư mục.
- Unity: "Gắn dạng .atomik" → `moc_tinh: prefab giữ 2 dạng (giac_moc_1, giac_moc_2)`, `thanh_long: prefab giữ 3 dạng (moc_vuong_d1,
  moc_vuong_d2, moc_vuong_1)`. Golden chạy lại: không đổi.
- **Chưa:** xem trong trận (Unity máy C đang kẹt biên dịch HatGiac / HatRong, cần mở lại Editor); EditMode test chưa chạy lại; `fly` dạng 1 Thanh
  Long chân sau duỗi lộ dài; chưa chỉnh `size`; `game.height` dạng 2 Thanh Long chưa nhân hệ số như dạng 3 (`CAO_KHAI`).

## Sửa sau khi người dùng xem (2026-11-13): "dạng 1 chân bị stretch ra khi bay", "miệng bị lỗi ở chiêu cuối", "dạng 2 cũng có lỗi tương tự"

- **Chân giãn khi bay**: bàn chân (target2, target4, all43, all46) là con của `all`, tách thân; clip `fly` kéo bàn ra xa sau. `atomik_dang.clamp_legs`
  (chỉ clip `fly`; clip chạm đất không đụng để chân không nhấc khỏi đất): khoảng cách hông (all30, all19, all44, all41) → bàn ≤ 1,06 × lớn nhất ở
  idle, ghi lại khoá dời 30 khung/giây. `fly` vẫn khép vòng (lệch 0).
- **Miệng**: tách đôi cái miệng vẽ ngậm thành sọ + hàm (hai bản đầu) ra mép cắt nham nhở, hàm thành mảnh vụn, chấm lòng miệng lọt qua lỗ. Đổi hẳn:
  đầu NGẬM = cả đầu concept (một ô trên all8), đầu HÁ = GPT vẽ lại đúng đầu đang gầm (`gui_gpt/thanh_long_non/luot_2_ha_mieng_d<k>.txt` →
  `tai_ve/L2_ha_d<k>.png`, khớp đầu ngậm bằng tương quan pha quanh mắt: lệch < 0,5 px). Hình `tou_01_ha` cho cả hai slot sọ; `doi_dau_ha`:
  mọi clip, xương hàm all13 của rig gốc há quá 12° thì đổi sang đầu há (giữ đúng lúc nào slot sinh đôi hiện). Ẩn hẳn `tou_02, tou_03, tou_04`.
  `cat_concept.cat(..., mot_khoi=False, them=đỏ)`: lòng miệng đỏ sẫm không bị coi là mực.
