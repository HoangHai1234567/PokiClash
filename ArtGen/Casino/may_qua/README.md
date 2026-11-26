# Máy quả sống "Háu Ăn" (lều Hội Máy Quả, đảo Casino)

Người dùng dặn 2026-11-26: gen hẳn một máy slot, rig xương để nó nhún, lắc hai bên, jackpot thì nhảy lên lắc; học cách diễn của hoạt hình
ống cao su (kiểu Cuphead); làm bằng AtomSpine. Đã chốt: **hướng B (Háu Ăn)**, **Lão Mực kéo cần**; sau khi xem rig: "làm nốt đi".
Kế hoạch dealer liên quan: `GD_Claude/31_LaoMuc_Dealer.md` mốc D5; lõi trò: `Assets/01 Script/Core/Casino/Slots.cs`.

**Trạng thái (2026-11-26): rig có viền + 12 clip, đã vào game, chạy thử bằng tour trong Unity.** Trang xem: `xem_rig.html` (ảnh chụp trong
game, ảnh động từng clip). Chưa thử máy Android thật.

## Concept (đã duyệt)

`xem.html`: ba hướng, cảnh thử, thử nhịp. `build_concept.py` sinh `concept/luot_1_huong_{A,B,C}.txt`; ảnh `concept/huong_*.png`,
`concept/canh_thu_C.png`; `cat_thu.py` → `thu/may_*.png` (cho phần thử nhịp).

## Hình (Magnific GPT 2.6, 1k high, 95 credit mỗi tờ; nền lều phóng classic 2k 72 credit)

| Tờ | Là gì |
|---|---|
| `rig/L1_goc.png` | bản chuẩn cả con, không viền, nền hồng #FF3AD0, ô cuộn trống (chỉ để đo và so) |
| `rig/L2_than.png` | thân trống đúng chỗ: không mắt, mày, miệng, cần, lò xo, chân |
| `rig/L3_chi.png` | đúng chỗ: sao + lò xo, dải mày, cần + núm, hai chân (vẽ đủ phần khuất) |
| `rig/L4_mat.png` | 8 cặp mắt: trung tính, nhìn xuống, lồi, nhắm chặt, cười nhắm, chớp, buồn, mắt sao |
| `rig/L5_mieng.png` | 6 miệng: cười, nghiến, rớt hàm, chữ o, mếu, cười to |
| `leu/nen_leu_qua_1k.png` → `_2k.jpg` | nền lều 9:16 trống: bục thảm đỏ giữa, quầy bên phải (mép quầy thẳng ngang ở y 1204 px ảnh 2k), thùng bi bên trái |
| `leu/bieu_tuong_1k.png` | 9 biểu tượng cuộn (vẽ lại theo icon của game: lửa, nước, lá, thỏi, đá, bi, vương miện, sao, rương) |

## Script (chạy `py -3 -I <tên>`; đường dẫn tính từ chỗ đặt script)

| Script | Việc |
|---|---|
| `rig/chuan_bi.py` | tách nền, cắt mảnh vào `atom/images/`, dựng lại ống chân, đèn sáng; ghi `atom/geo.json` |
| `rig/ghep_thu.py` | ghép mảnh lại cạnh L1 → `rig/soi/ghep_thu.png` |
| `rig/dung_rig.py` | xương, mảnh, lưới, trọng số (dựng lại project AtomSpine từ đầu); `--luoi`: chỉ dựng lại lưới + trọng số (sau khi vẽ viền) |
| `rig/hoat_anh.py [clip]` | dáng theo giờ + bộ nướng (khối thân trễ, chân ống cao su, lò xo cần / ăng ten) → khoá AtomSpine; nướng `pull` thì ghi `atom/duong_num.json` (đường núm cần) |
| `rig/ve_vien.py [--xem]` | viền mực: nét `paint.stroke` vào lớp `vien` của từng ảnh mảnh (ảnh sạch giữ ở `atom/images_khong_vien/`); xong chạy `dung_rig.py --luoi` |
| `rig/kiem.py` | đọc `.atomik` đã xuất: góc nhảy lớn nhất mỗi khung, lệch khung cuối so với clip nối tiếp |
| `rig/xem.py`, `rig/ghep_luot.py` | tờ khung + GIF từng clip, GIF lượt quay trọn → `xem/` |
| `rig/xem_keo.py` | soi clip `sl_pull` của Lão Mực có bám núm cần không → `xem/keo_can_to.png` |
| `rig/mo_studio.py` | mở AtomSpine Studio cho project `atom/` |
| `leu/dua_vao_unity.py` | chép nền, 9 biểu tượng (`Assets/03 Art/Casino/Leu/sl_*`), rig (`Assets/03 Art/Casino/MayQua/may_qua.bytes`) |
| `loc_may_qua.py` | thêm bản dịch tiếng Anh của chuỗi mới vào `Resources/Loc/en/ui.json` (chỉ thêm khoá) |

Thứ tự dựng lại từ đầu: `chuan_bi` (xoá `atom/images_khong_vien/` và `atom/images/*.ora` trước) → `dung_rig` → `hoat_anh` → `ve_vien` →
`dung_rig --luoi` → `atom export atomik --atlas-cap 1100` → nướng lại `sl_pull` của Lão Mực (`ArtGen/Casino/dealer/rig/hoat_anh.py sl_pull`,
xuất `--atlas-cap 1200`) → `leu/dua_vao_unity.py` + chép `lao_muc.bytes`.

## Clip và sự kiện của rig máy

`idle` (lặp 4 s), `pull` (0,9; `keo` 0,47) → `spin` (lặp 0,5) → `stop_1`, `stop_2` (0,4; `cach` 0) → `spin` hoặc `tease` (lặp 0,5) →
`stop_3` (0,5) → `lose` (1,2) / `win` (1,6; `nha_bi` 0,20 và 0,84) / `jackpot` (4,0; `no` 0,56, `het_no` 1,40, `dap` 1,50, `nha_bi` 2,0) /
`free` (1,2; `mien_phi` 0,2); `appear` (1,4; `chao` 0,5). Clip một lần kết thúc ở dáng nghỉ (= idle giây 0; ăng ten còn lệch vài độ).

Chỗ bám cho game: xương `tam_d` + `cuon` (khung và tâm ô cuộn), `num` (núm cần), `mieng`, `sao` (chỗ phun bi).

## Trong game

- Bố cục sân khấu: `bo_cuc.json` (máy tỉ lệ 0,90 gốc (−160, 1452); Lão Mực 0,60 gốc (350, 1437); mép quầy y 1137). Màn 1:2 chỉ thấy
  x ±480 nên cả hai nằm trong đó. Đổi bố cục thì sửa hằng số ở `Editor/CasinoSlotMenu.cs` và nướng lại `sl_pull`.
- `Game/Casino/SlotReels.cs`: hình ba cuộn (Image uGUI trong Mask), mỗi khung đặt theo xương `tam_d` / `cuon` của máy.
- **Cuộn chạy nhanh như máy thật** (người dùng dặn 2026-11-26: "khi gạt cần làm 3 row chạy thật nhanh, tạo cảm giác giống slot thật"):
  38 ô / giây (`SlotScene.ReelSpeed`), tăng tốc 0,16 s, hãm 0,26 s cuối, ba cuộn nổ máy lệch nhau 0,05 s, dừng ở 0,85 / 1,30 / 1,80 s
  sau lúc giật cần; từ 9 ô / giây mỗi ô đổi sang hình nhoè dọc `Leu/sl_bt_<k>_nhoe.png` (200 x 380, `leu/dua_vao_unity.py` sinh) nên
  các vệt nối thành dải; tiếng lạch cạch (`peg`) dày lúc ba cuộn cùng chạy, thưa dần khi từng cuộn dừng.
- `App/Scenes/Casino/SlotScene.cs`: máy và Lão Mực đều là `DealerRig` + `DealerLayer`; `pull` của máy và `sl_pull` của Lão Mực phát cùng
  một khung; bi phun là pool Image, rung màn theo sự kiện `dap`.
- `Editor/CasinoSlotMenu.cs`: menu "Lều Máy Quả: dựng scene" (cờ `Temp/casino_sl_build.flag`), tour `Temp/casino_sl_tour.flag` → ảnh
  `Temp/PokiShots/casino_sl/` (trượt, trúng, jackpot, ba Rương bằng hạt giống dò trước).

## Việc còn lại

1. Người dùng chơi thử trên máy Android; chỉnh theo nhận xét (Studio Comment mode cho animation).
2. Âm thanh riêng (tiếng cần, cuộn, bi) đang dùng tiếng sẵn của game.
3. Màn 1:2 cắt vài px mép trái thân máy lúc bẹp ngang.
