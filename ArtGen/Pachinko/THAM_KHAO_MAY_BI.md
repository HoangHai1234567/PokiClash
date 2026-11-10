# Máy bi tham khảo (Clash of Critters 0.50.1): bộ phận và toàn bộ hiệu ứng, áp vào máy mình

Soạn 2026-11-06 từ bản đục `D:\CrittersRipper` (đọc prefab, ảnh, clip; logic Lua mã hoá không đọc). Số đo vật lý, âm thanh, rung ở
`D:\CrittersRipper\analysis\PINBALL_REPORT.md`. Phần cấu trúc hạt đã chép vào `MachineFx.cs` từ 2026-11-02
(`GD_Claude/07_MayBi.md`, mục "Hiệu ứng chép").

**Cách chép:** lấy bộ phận, trạng thái, nhịp và cấu trúc hiệu ứng. Hình vẽ lại theo nét đã duyệt của mình. GPT không thấy ảnh của
game đó, prompt không nhắc tên game. Gói prompt: `gui_gpt/bo_moi/` (sinh bằng `build_bo_moi.py`).

**Khác biệt lớn nhất:** máy đó dựng gần như mọi hiệu ứng bằng lớp quầng mềm cộng sáng (glow, flash, circle_glow, add). Luật mình là
tô phẳng, không quầng (`.claude/skills/pokiclash-vfx`). Vì vậy mỗi lớp quầng đổi sang một hình vẽ tay phẳng có viền mực:
- flash, glow → `pk_fx_loe` (hình loé gai);
- circle_hard → `pk_fx_vong_day`;
- "she" → `pk_fx_vach_toc`;
- dot → `pk_fx_cham`.

## 1. Bộ phận

| Bộ phận | Máy đó | Máy mình bây giờ | Làm mới (gói `bo_moi`) |
|---|---|---|---|
| Tủ máy | tủ đỉnh vòm đỏ, chuỗi bóng đèn chấm viền vòm (`desk`, `desk1`), đèn đỉnh 3 mức sáng (`light_top` 1–3, đoán theo cược), dải đèn điện tử | tủ vẽ tay đã duyệt (`pk_than_may`), bóng đèn vẽ liền vào tủ | bóng đèn rời tắt / sáng vàng / sáng hồng (`pk_den_*`), game cho đèn chạy theo cược |
| Nút thả | nút vòm tròn to ở giữa dưới máy, 4 ảnh: thường cam, hết lượt xám, đỏ, kim cương (cược đặc biệt); nhấn: lõm rồi bật, mặt nạ loé; giữ thì vòng sáng nhịp | 2 nút chữ nhật "THẢ BI", "THẢ LIỀN 20" | nút vòm tròn 4 trạng thái (sẵn sàng, nhấn, hết bi, cược lớn), nút thả liền tròn nhỏ 2 trạng thái, bảng nút dưới máy |
| Nút cược | viên tròn vàng (`btn_multi`), tím khi mức cao nhất (`btn_multi_max`) | cột ô giấy ×1…×10 | viên cược tròn: thường, đang chọn, khoá, mức cao nhất |
| Cần phóng | cần lò xo ở mép phải: ống, cần, bi trong ống; nhấn co giãn 0,63 → 1,57 → 0,89 → 1,2 | mây trên ray (`pk_may_tha`), co giãn nửa biên độ | mây nháy mắt khi thả, mây há miệng khi trúng két |
| Đinh | đinh xám (`collider_normal`); bị chạm đổi sang hình sáng (sao cam có nền sáng `collider_mid`, `_backlight`) trong 0,067 giây | đinh nâu xám, chỉ phồng và quầng | đinh sáng vàng có sao trắng (`pk_dinh_sang`) |
| Nấm lớn | vòng tròn có biểu tượng (kẹo, khiên, trứng 3 màu), vòng tiến độ quanh nấm, chạm đủ thì mở thưởng | nấm đỏ chấm trắng, phồng xẹp | nấm sáng (`pk_bumper_sang`); vòng tiến độ không làm (máy mình không có cơ chế này) |
| Nấm đỉnh | nửa vòng cam lún vào vòm (`topball`) | không có (vai nghiêng) | không làm |
| Mái, đáy V | thanh kim loại cong (`baffle_angle`, `baffle_bottom`) | mái và đáy két vàng | tấm két sáng (`pk_ket_sang`) |
| Lò xo | lò xo bật (`emitter_01/02`, bản đỏ) | không có | không làm |
| Ô đáy | nền ô có hoa văn (tím tia toả, cam chấm), ô thẻ giữa, vách ống đỏ, nhãn số; ô sáng khi bi vào | ô màu nhạt gạch chéo, cọc gỗ, nhãn số | lớp sáng ô (`pk_o_sang`, `pk_o_sang_ruong`), game tô màu theo ô |
| Cốc | không có | cốc bạc | cốc sáng (`pk_coc_sang`) |
| Bảng điểm | bảng dưới máy có đèn chấm chạy (`bg_scorebord`, `light_03…13`), hiện thưởng theo 4 bậc | thanh "Rương Vàng" | bảng nút (`pk_bang_nut`) giữ chỗ dưới máy |
| Biển mũi tên | mũi tên đèn (`arrow_bg`) | không có | không làm |
| Tay chỉ | ngón tay hướng dẫn (`pbfx_ui_point_finger`) | không có | bàn tay găng trắng (`pk_tay_chi`) |

## 2. Toàn bộ hiệu ứng máy bi (36 prefab `Res/Fx/Prefab/Ui/*pinball*`)

Số: đời (giây), số hạt, tốc (u/giây; bi máy đó 0,162 u), trọng lực. "Glow" là lớp quầng mềm.

### Bi và nút

| Prefab | Lúc | Gồm | Máy mình |
|---|---|---|---|
| `pbvx_pinball_shoot_fire` | phóng bi | lửa 0,15 (cỡ 0,4–0,7), glow 0,15, 1 chấm 0,1–0,3 | có (`Launch`, khói); thêm loé nhỏ, chấm |
| `fxpb_demo_ui_pinball_trail` | bi bay | vệt đuôi 0,3 giây | có (`TrailGraphic`) |
| `pbvx_pinball_button_pressing` | đang giữ nút | lặp: vòng + glow, 10 vòng/giây, mỗi vòng 0,2 giây, cỡ 3 | **thêm:** vòng đứt nhịp quanh nút khi giữ để thả liên tục |
| `pbvx_special_pinball_button_in` | bật cược đặc biệt | 1,8 giây hạt hút vào nút (50 + 30 hạt/giây, tốc −10…−5), quầng, tam giác; giây thứ 2 nổ: 3 sao, 2 sao to, 2 chấm, 16 tam giác, vòng, 15 loé | **thêm:** khi mở mức cược mới (×5, ×10): chấm và tam giác hút vào nút rồi nổ loé, sao, tam giác |
| `pbvx_special_pinball_button_loop` | đang ở cược đặc biệt | sao lấp lánh 5 hạt/giây | **thêm:** lấp lánh rỗng quanh nút khi đang cược lớn |

### Mặt máy

| Prefab | Lúc | Gồm | Máy mình |
|---|---|---|---|
| clip `anvx_pinball_collider_small` | chạm đinh | đổi hình sáng, phồng 1,15 → 1, quầng 1,10 → 0,68 trong 0,067 giây | có (`PegHit`); thêm đổi hình `pk_dinh_sang` |
| `fxpb_demo_ui_pinball_ringhit_orange` | chạm vòng, cốc | loé 0,2 (cỡ 0,7), vòng 0,1, 10 chấm 0,2–0,4, 10 sao 0,4–0,6 (trọng lực 0,3) | có (`RingHit`); chấm đổi sang `pk_fx_cham` |
| `pbvx_pinball_collider_big_hit` | chạm nấm | 2 glow 0,15 (cỡ 3 và 1,75), 1 hạt phóng to 0,19 (1,62) | có (`BumperHit`); thêm đổi hình `pk_bumper_sang` |
| `pbvx_pinball_collider_big_activate` | nấm đổi biểu tượng | clip trứng vào, lặp, ra | không (máy mình không có nấm tiến độ) |
| `pbvx_pinball_collider_pet_gain` | nấm cộng tiến độ | sao lõi 0,3 (2,2), vòng 0,2, glow 0,3, sao 20 hạt/giây, 5 vạch nhỏ | để dành: sao EXP bay về thanh kinh nghiệm |
| `pbvx_pinball_collider_pet_get` | nấm đầy, nhận thưởng | vòng cỡ 90, glow 100 rồi 200, 7 + 5 sao tốc 6–12 | để dành: lên cấp máy (thanh EXP đầy) |
| `pbvx_pinball_triggeron_mid`, `_mid02` | bi vào ô | 3 glow 0,1–0,3, 6 sao tốc 60 → 15 bị hãm, 6 vạch "she" 0,07–0,18 | có (`SlotHit`); thêm lớp sáng ô `pk_o_sang`, vạch đổi sang `pk_fx_vach_toc` |
| `pbfx_demo_pinball_slotactive` | ô thưởng sáng | glow 0,7 (cỡ 2), 3 sao tốc 3–6 | **thêm:** ô rương sáng `pk_o_sang_ruong` + 3 sao |
| `pbvx_pinball_jackpot` | ô jackpot | vòng 0,24, 2 quầng 0,35, 4 tia, 3 sao (trễ 0,05), 1 sao nảy (trễ 0,1), sao lõi | có (`Jackpot`, két vàng); thêm két sáng, mây há miệng, loé |
| `pbvx_pinball_snow` | trang trí mùa đông | 4 lớp tuyết rơi chậm, đời 9–12 giây | không làm (theo mùa) |

### Thưởng (bảng điểm, thẻ)

| Prefab | Lúc | Gồm | Máy mình |
|---|---|---|---|
| `pbvx_pinball_result_board_out_01` | thưởng bậc 1 | loé 0,2, glow 0,2 | có (`ChestHit` gỗ) |
| `_out_02` | bậc 2 | + vòng, vòng cứng, sao, sao to | có (gỗ, bạc) |
| `_out_03` | bậc 3 | + 6 tia tốc 10–20, sao to hơn | có (vàng) |
| `_out_04` | bậc 4 | clip `scorebord_hit02` | không |
| `pbvx_pinball_result_board_collect_01` | bảng nhận thưởng | clip lặp `scorebord_hit01` 0,68 giây | không |
| `pbvx_pinball_award_card_out` | thẻ bay ra | chớp tròn 0,1 (cỡ 5), glow 0,25 (7), 8 chấm (trọng lực 0,5), 1 sao to 3 → 1 | **thêm:** rương bay vào khay |
| `pbvx_pinball_award_card_muti` | nhiều thẻ | vạch 0,15 tốc 12, glow 0,15 (5), 3 sao | **thêm:** thả liền nhận nhiều rương |
| `pbvx_pinball_card_out_glow` | thẻ sáng | clip | thay bằng tia toả `pk_fx_tia_toa` xoay chậm sau rương |
| `pbvx_pinball_cardout_blue` | mở thẻ xanh | chớp 0,2 (10) ×2, tròn 0,3 (6, trễ 0,1), vòng 0,25 (7) ×2, glow, 8 chấm (tốc 5–10, trọng lực 1), 5 sao (3–6) | **thêm:** mở rương gỗ |
| `_cardout_purple`, `_purple_in` | mở thẻ tím | như xanh + 6 + 2 tia tốc 5–10 | **thêm:** mở rương bạc |
| `_cardout_gold` | mở thẻ vàng | như tím | **thêm:** mở rương vàng + dây giấy, tia toả |
| `_cardout_red` | mở thẻ đỏ | như tím | không (mình có 3 bậc rương) |

### Buff, chế độ phụ

| Prefab | Lúc | Gồm | Máy mình |
|---|---|---|---|
| `pbvx_pinball_buff_double_in` | bật buff x2 | 10 sao nhỏ, 2 sao to, 3 tam giác sáng (cỡ 7), sao lặp | để dành: Rương Vàng đầy hoặc lên cấp máy |
| `pbvx_pinball_buff_red_card_in` | bật buff thẻ đỏ | quầng cỡ 20, 15 loé cứng, 13 sao, 30 vạch tốc 5–15 | để dành |
| `pbvx_pinball_buff_halloween` | buff mùa lễ | dơi bay hai bên, kẹo rơi, quầng, sao | không làm (theo mùa) |
| `pbvx_pinball_frenzyball_change_*` (4 prefab) | chế độ bi điên | vạch tốc dày (tốc 40–100), vòng, sao trên nút | không làm (máy mình không có chế độ này) |

## 3. Nhịp chung học được

- Một hiệu ứng là một lần nổ ngắn rồi hết, 0,1–0,5 giây. Chỉ nút đang giữ và cược đặc biệt mới lặp.
- Thứ tự lớp trong một lần nổ: chớp hoặc quầng (0,1–0,2 giây) → vòng lan (0,2–0,3) → chấm, sao văng có trọng lực (0,4–0,8).
- Độ lớn đi theo giá trị: đinh chỉ đổi hình; ô thường 3 lớp; ô hiếm có thêm sao, tia; jackpot, thẻ vàng có đủ lớp, chậm thời gian, rung.
- Mọi bậc dùng chung một bộ hình: bậc cao chỉ thêm lớp (tia, sao to) và đổi màu. Vì vậy 12 hình mới đủ cho mọi bộ trên.

## 4. Đã nối vào game (2026-11-06)

1. Ba tờ đã duyệt (`build_bo_moi.py --duyet nut|trang_thai|hieu_ung_2`, 36 ảnh `pk_*` trong `Assets/03 Art/Pachinko`). Bóng đèn vòm
   dò bằng `build_bo_moi.py --den` (15 bóng, `refs/den_vom.json`).
2. Màn Máy bi (menu `PokiClash/Prefab/Máy bi: nút tròn, viên cược, đèn vòm`, code `MachineScene.cs`):
   - nút vòm to giữa dưới máy: sẵn sàng, lún khi giữ (chữ dời theo nắp, vòng đứt nhịp quanh nút), xám khi hết bi, vàng sao khi cược ×5 trở lên;
   - nút thả liền vòm nhỏ (xanh ngọc khi đang thả liền);
   - viên cược tròn: thường, đang chọn, khoá có ổ khoá, mức cao nhất tím;
   - dòng đếm bi sang trái nút; thanh mốc và ô quà xuống một hàng;
   - 15 đèn vòm chạy cứ ba bóng sáng một, nhanh hơn khi cược lớn và khi đang thả, cả dãy nháy khi trúng két.
3. Mặt máy (`MachineBoard.cs`): đinh, u lồi, nấm đổi hình sáng khi chạm; cốc bạc và két sáng khi bi lọt; ô đáy sáng bằng lớp tia tô màu ô;
   mây nháy mắt khi thả, tròn mắt khi trúng két.
4. `MachineFx.cs`: lớp quầng thay bằng loé, vòng dày, vòng đứt, tia toả, chấm. Cỡ còn khoảng một nửa cỡ quầng cũ, tô màu nhạt: hình viền
   mực hiện đủ cỡ nên to bằng quầng mềm là quá to. Rương vàng thêm mảnh tam giác, jackpot thêm dây giấy.
5. Kiểm bằng `PokiClash/Thử/Máy bi: soi hiệu ứng (đang Play)` (thêm khung màn rảnh, đang giữ nút, tia sáng ô, két sáng, mây tròn mắt).

Chưa làm: bảng nút `pk_bang_nut` (hốc không khớp bố cục nút giữa, ảnh nhỏ), bàn tay chỉ `pk_tay_chi` (chưa có bước hướng dẫn),
hiệu ứng mở mức cược mới (hút vào nút rồi nổ), rương bay vào khay, mở rương theo bậc trong hộp mở rương, sao xoáy.

## 5. Bảng số, kẹo bay, ánh sáng, mở rương nhóm (2026-11-10)

Người dùng dặn chép 100 % hiệu ứng máy bi của máy tham khảo: bảng số dưới thanh cấp, icon EXP bay lên, ánh sáng và gradient, mở rương
như mở capsule thú. Số đo màn mở capsule đọc từ bản đục 0.51.1 (`D:\Ripper\ClashOfCritters`): prefab `pbui_common_reward`, clip
`*_in_new` (1,1 giây), bảng tổng kết `pbui_a_view_pet_common_openall`.

- Hình: gói `gui_gpt/bang_so_mo_ruong/` (`build_mo_ruong.py`, gọi Codex bằng `ArtGen/Heroes/tools/gen_codex.py`): `pk_bang_so`,
  `pk_keo_exp`, `pk_keo_exp_nam`, `pk_the_up`, `pk_may_do`, `pk_ruy_bang`, `pk_nut_mo_het`, `pk_ruong_*_nap`, `pk_ruong_*_than`.
- Ánh sáng mềm: `sinh_anh_sang.py` → `pk_g_*` (quầng, vòng, tia, cột, vệt lia, gradient dọc, chấm LED, lấp lánh), vẽ cộng sáng.
- Bảng số `MachineScoreBoard.cs`: chiếm chỗ thanh EXP ở đầu máy, thanh dời lên vòm tủ. Kẹo bay từ ô lên bảng, số đếm tăng; hết đợt
  kẹo bay từ bảng lên đầu thanh (`MachineExpBar.Held`, `Deposit`).
- Mở rương nhóm `MachineChestOpen.cs`: tối đa 5 rương, bố cục và nhịp mở theo bản đục (lắc 0,25 giây, nắp vọt, thân rơi, chớp, vòng
  sóng, thưởng nảy), "Mở tất cả" cách 0,15 giây, bảng tổng kết ô bật 0,667 giây, thẻ úp lật.
- Báo cáo số đo bản đục: `refs/ban_duc_bang_so.md`, `refs/ban_duc_mo_capsule.md`.
- Bản đục không có (nằm trong Lua mã hoá): đường bay capsule vào chỗ, nhịp lơ lửng, độ lệch "mở tất cả": tự đặt.
