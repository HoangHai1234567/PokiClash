# Bùn Ngoạm Nhi (`quai_bun_non`): dạng 1 của tướng 8 đảo Thổ (ải 50, id `ho_kim_cuong`)

Dạng 2 = quái bùn (`quai_bun`, ghi chú `quai_bun_ghichu.md`). Rig, lưới, chuyển động gốc là của nhà phát hành game tham khảo
(`monster_3668`): chỉ dùng nội bộ, không đăng công khai.

## 1. Lời dặn (2026-11-17)

- "ok cho vào game, làm dạng 1 đi" (sau khi duyệt rig quái bùn lượt sửa 3).
- Hỏi rig dạng 1 → người dùng chọn **"Cùng rig 3668"** (đổi tỉ lệ ngay trên rig quái bùn, như Giác Mộc Non / Thanh Long dạng 1). Kho Sword x Staff
  không có dạng trước của 3668 (3664–3667, 3670: thú lửa, pha lê, rồng pha lê, gã xích; tờ `scratchpad .../ke/ke.jpg`).
- Tên: "tùy bạn đặt, đặt dễ hiểu là được" → tướng **Bùn Ngoạm** (danh hiệu "Quái bùn nuốt chửng"), dạng 1 **Bùn Ngoạm Nhi**. Thẻ: Đấm Bùn Trồi /
  Nuốt Chửng / Thân Bùn / Bùn Tái Tạo (boss). Phần vào game của dạng 2 do một agent làm (mục "Vào game" trong `quai_bun_ghichu.md`).

## 2. Tỉ lệ (tỉ lệ trước, concept sau)

`mo_xe/atomik_bocuc.py` trên `quai_bun_1/rig/quai_bun.atomik`, tờ `quai_bun_non/mau/so_ab.jpg`, `so_cd.jpg` (A–D):
- Chọn D (`mau/ti_le.json`): thân `bone2` 0,8; đầu `bone5` 1,45 (gồm đầu thường bone6 và hàm khổng lồ bone63); tay gần `bone7`, tay xa `bone19`
  0,85; dải bùn lưng `bone50`, `lujing_04` 0,4. Khối tròn be dưới miệng là HÀM DƯỚI (thuộc đầu) nên to theo đầu.
- Bố cục cho concept: `mau/bo_cuc.png` 1536×1024, khung nhìn cố định (−760, −80) → (760, 933) đơn vị rig (1,01 px / đơn vị).
- Soi da cũ ở dáng gắt (`mau/soi_d.jpg`): khi dựng rig dạng 1 phải sửa thêm: tay co giãn `G_*` (chuỗi fly, không thuộc bone19) và nắm đấm khổng
  lồ `nam_ngam` (con của far) còn cỡ người lớn; quả bóng `bong` (con của move) không co theo thân; hàm khổng lồ × 1,45 × `HA_TO` 1,7 quá to; hàm
  dưới ở appear thõng dài.

## 3. Concept lượt 1 (Magnific GPT 2.6, 1k high, 95 credit / ảnh, 2 ảnh = 190 credit)

`quai_bun_non.py concept` → `gui_gpt/quai_bun_non/luot_1_concept_A.txt`, `_B.txt` + `HUONG_DAN.md`; ảnh 1 = `mau/bo_cuc.png`, ảnh 2 = concept dạng 2
`quai_bun_1/tai_ve/L1_duyet.png`.
- A `tai_ve/L1_A.png`: bùn non sô-cô-la sáng hơn, mắt hổ phách to cau mày, hai sừng cuội nhú, răng cuội sữa thưa, nắm tay ba viên sỏi, ba giọt bùn
  ngắn trên lưng. IoU với bố cục 0,861.
- B `tai_ve/L1_B.png`: như A nhưng đội nửa VỎ TRỨNG ĐÁ CUỘI vỡ răng cưa trên đầu (lớn lên mảnh vỏ thành hai sừng đá), không sừng. IoU 0,885.
- Tờ chọn `mau/chon_concept.jpg` (A, B, dạng 2). Chờ người dùng chọn.

**Người dùng chọn A (2026-11-17)** → `tai_ve/L1_duyet.png`.

## 4. Mảnh (`quai_bun_non.py manh` → prompt, `cat` → `inbox/quai_bun_non/manh/`)

- Đo màu (k-means từng vai trò): màu concept dạng 1 gần TRÙNG màu mảnh dạng 2 (bùn #884D30 / #824C30, bụng #B3774A / #AC774B, đá, lòng miệng)
  → không đổi màu; mọi mảnh dạng 2 chép nguyên, ảnh part theo khung gốc dùng chung (`quai_bun_1/manh/part_can`).
- Gen lại 3 tờ (Magnific GPT 2.6 1k high, 95 credit / tờ, 285 credit; gói `gui_gpt/quai_bun_non/luot_2_*.txt` + `HUONG_DAN_luot_2.md`):
  `tai_ve/M_dau.png` (đầu = hàm trên, sừng nhú, răng sữa trên, bỏ mắt), `M_ham.png` (bụng be + răng sữa dưới), `M_bong.png` (quả bóng dạng 2 vẽ lại
  mặt con non: mắt to, sừng nhú, tay ba viên sỏi; IoU viền với quả bóng cũ 0,961). Đầu / hàm đặt chồng concept trùng khít (`mau/_so_dau_ham.jpg`).
- Mắt mở cắt thẳng từ concept; mắt nhắm dựng bằng mã (tô da + nét mí), như dạng 2.
- Đầu, hàm, mắt cắt trên khung concept dạng 1 rồi QUY VỀ KHUNG CONCEPT DẠNG 2: px dạng 1 → đơn vị rig (`atomik_dang.canvas_map(KHUNG)`, lề 1,06:
  0,953 px / đơn vị) → nghịch đảo biến đổi cây đầu `bone5` ở khung 0 idle (`mau/T_idle0.json`: × 1,16, dời (−67, −200)) → px dạng 2
  (`quai_bun_1/mau/goc_ca_con.json`). Rig nhân tỉ lệ thì mảnh phóng lại đúng chỗ concept.

## 5. Rig dạng non (`QB_DANG=non py -3 -I quai_bun_rig.py` → `inbox/quai_bun_non/rig/`)

- Cùng script với dạng 2 (`NON`): mảnh ở `quai_bun_non/manh`; sau khi dựng nhân tỉ lệ dáng gốc theo `mau/ti_le.json` + hai cổ tay `bone10`,
  `bone22` 0,78 (nắm sỏi nhỏ) + nắm đấm khổng lồ `nam_ngam` 0,7; quả bóng `bong` 0,8, cục đất `cuc` 0,82 (co quanh tâm, hạ cho đáy chạm đất; độ
  lún khi bẹp nhân theo `K_BONG`, `K_CUC`); hàm khổng lồ `HA_TO` 1,35, `HA_NHO` 1,25 (đầu đã × 1,45).
- Tay co giãn (chuỗi `all2…`, gắn vào fly, chuyển động theo toạ độ thế giới của con gốc): mỗi khung dời theo vai mới (`bone19` của rig đã nhân
  tỉ lệ, cùng dáng), co `K_TAY_CO` 0,68 quanh vai, pha theo phần quãng vai → far nên nắm đấm vẫn tới đúng far; tay mảnh / nắm nhỏ × 0,68.
- Hàm to thụt sâu hơn mép mặt nạ đất ở appear (gầm), skill (nhổ), die (−46 / −80 / −41 đv): ba clip đó hạ mặt nạ thêm `H_CAT_NON` 100 (cast
  giữ nguyên vì tay cắm xuống đất). Đo lại: mọi clip ≥ +20 đv trên đường cắt.
- Xuất: 187 xương, 83 slot, 25 sự kiện, cao 694 (dạng 2: 1020), `.atomik` 503 KB (dưới trần). Runtime thật (`rig/that/*.jpg`): mọi clip đúng;
  60 khung/giây bước xoay lớn nhất trên slot đang hiện như dạng 2 (skill 81°, attack 73°: các cú vụt có sẵn). `thu_xem` đủ 8 clip.
- Clip `evolve` (thử, cỡ tạm 0,92 / 1,12; scratch `thu_th.py`, như `doi_tho5_dang2.th`): `rig/quai_bun_non_th.atomik` 748 KB (mang dạng 2 bản
  nhẹ: vượt trần 0,5 MB như Giác Mộc Non 944 KB), tờ `rig/khung_evolve.png`: dạng 1 gồng, mờ 1,05–1,35 s, dạng 2 hiện, lớn dần, dừng ở khung 0
  idle dạng 2.

## 6. Việc tiếp

1. Chờ agent đưa dạng 2 vào game xong (cỡ dạng 2 nó chọn) → gộp lại `evolve` với cỡ thật → `Resources/quai_bun_non/` (bản `_th`), forms 2 dạng
   ("Bùn Ngoạm Nhi" / "Bùn Ngoạm") trong `heroes.json`, hiệu ứng theo dạng (HatTho / bảng ThoFx, ThoAtk theo dạng), Unity: Nhập dữ liệu, Gắn
   dạng, golden (số dạng 1 → 2), test, tour.
