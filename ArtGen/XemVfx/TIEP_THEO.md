# Đợt sửa VFX mọi tướng (2026-11-18): đang dừng giữa chừng, việc tiếp theo

Người dùng bảo tạm dừng ngày 2026-11-18 để về nhà làm tiếp. File này ghi đủ để phiên sau làm tiếp mà không cần đọc lại chat.

## Người dùng muốn gì
- Tách skill thành hai bộ (Animation, VFX), đẩy lên https://github.com/HoangHai1234567/SkillForClaude.
- Chia agent dùng bộ skill VFX cải thiện toàn bộ VFX của game.
- Làm một trang web để xem từng tướng.
- Chỉ test tướng rig `.atomik` / Spine (50 tướng). Bảy tướng Thổ còn hình aola (vo_su, gau_mo, soc_da, bo_hung, sa_than, ky_lan, ca_sa) bỏ qua.
- Góp ý của người dùng trong đợt (đã thành luật ở `.claude/skills/vfx-petclash/SKILL.md` mục 1b):
  - tia cụt, không va chạm;
  - khói rải rác, chưa thành cụm, chưa mềm;
  - lửa và dung nham tròn cứng;
  - nổ, sóng âm xấu;
  - tụ cầu xấu;
  - màu tối, phải tươi hơn;
  - đốm lửa đơn lẻ và to.

## Đã xong
1. **Skill:** `skill-petclash` cũ tách làm hai bộ.
   - Bộ Animation: `animation-petclash` (gốc) + `pokiclash-spine-rig`.
   - Bộ VFX: `vfx-petclash` (gốc) + `pokiclash-vfx`, `pokiclash-hero-fx`, `pokiclash-fx-congthuc`.
   - Mọi chỗ trỏ cũ đã đổi; `.agents/skills` đã đồng bộ.
   - Đã đẩy lên SkillForClaude (commit `91f6a10`). **Mục 1b của `vfx-petclash` thêm SAU lần đẩy đó: chưa có trên GitHub.**
2. **Bộ hình hạt kiểu Kingdom Rush:** `ArtGen/Spine/hat_kr.py`.
   - Xuất 172 ảnh `Assets/03 Art/Fx/Hat/hat_kr_*.png` (bản vân + bản đặc nở sẵn khoảng 6 px).
   - Tờ xem `ArtGen/Spine/hat_kr/xem.png`.
   - Đã nhập Unity và chạy menu gán ảnh ("Sàn đấu: hạt lửa (bộ Hỏa)", "Hộp chi tiết tướng: hạt lửa + nút Mana").
   - Quy ước điểm co lớp của từng hình: `bao_cao/` hoặc báo cáo agent hình (tóm trong skill khi làm tiếp).
3. **Năm agent theo hệ đã sửa code**, mỗi file biên dịch 0 lỗi ngoài Unity. Báo cáo từng tướng (lỗi ở ảnh trước, đã sửa gì, mong thấy gì, chỗ còn lo, đề xuất) ở `bao_cao/hoa.md`, `thuy.md`, `moc.md`, `kim.md`, `tho.md`.

   | Hệ | File đã sửa |
   |---|---|
   | Hỏa | `HatLua`, `HatNhan`, `HatNham`, `HatPhap`, `HatDat`, `HatHo`, `HatNuiLua`, `HatRua` |
   | Thủy | `HatNuoc` (tia `NTia` mới, toé, đuôi, tụ cầu) |
   | Mộc | `HatMoc`, `HatDa`, `HatVoi`, `HatLoc`, `HatCoVuong`, `HatChim`, `HatRong`, `HatGiac`, `HatKiem` |
   | Kim | `HatSat`, `HatKhoang`, `HatGiao`, `HatCua`, `HatHon`, `HatXich`, `HatSoi`, `HatRobot`, `HatVua`, `HatPhao` |
   | Thổ | `HatTho`, `HatThach`, `HatThoTinh`, `HatBun`, `StageViewThoTinh` |

   Khuôn của script sinh `HatHon` / `HatXich` (`ArtGen/Spine/ky_nguyen_hat_cs.py`, `quy_xich_hat_cs.py`) đã cập nhật theo bản mới.
4. **`StageView.cs` (phiên chính sửa):**
   - Móc `FoePulse`: mỗi nhịp trúng phụ, con bị trúng chớp trắng và giật lùi. Gắn vào `NuocPulse`, `DanhTrung`, `HoaTrung`. Trường `nuocTarget` đặt trước mỗi `PlayNuoc` / `PlayMana` / `PlayUlt`.
   - Thêm dòng FireFx `su_tu_lua` = ("cau", "phun_nham").
5. **Tour chụp `Assets/01 Script/Editor/VfxAllTour.cs`:** menu "PokiClash/Thử/Hiệu ứng mọi tướng: chụp bản TRƯỚC / SAU (đang Play)", khoảng 35 phút cho 57 tướng.
   - Bản TRƯỚC đã chụp (trước khi agent sửa) ở `Temp/PokiShots/vfx_all/truoc/`, **chỉ có trên máy ổ C** (Temp không vào git, khoảng 1,1 GB).
6. **Trang so sánh** `ArtGen/XemVfx/` (`index.html`, `xay_trang.py`, `MO_WEB.bat`, cổng 8768): đã dựng với bản TRƯỚC. Ảnh `anh/` và `data.json` đã `.gitignore`.
7. Unity biên dịch sạch với toàn bộ thay đổi. Test EditMode 134/135 qua.
   - Ca hỏng: `PrefabOnlyTests.MaRuntime_KhongSinhDoVat`, do `UI/Kit/NumberTicker.cs:21` và `UI/Kit/UiMotion.cs:38` gọi `AddComponent`. Không phải file của đợt này.

## Việc tiếp theo (theo thứ tự)
1. **Báo các phiên khác trước khi dùng Unity**, rồi Play, chạy menu "Hiệu ứng mọi tướng: chụp bản SAU". Xong: `py -3 -I ArtGen/XemVfx/xay_trang.py`, chạy `MO_WEB.bat`, mở cho người dùng.
   - Máy khác không có bản TRƯỚC thì ô "Trước" trống. Muốn so thì chép `ArtGen/XemVfx/anh/truoc/` (khoảng 200 MB) và `Temp/PokiShots/vfx_all/truoc/ds.json` từ máy ổ C sang; không đẩy lên git vì là hình của game khác.
2. **Tự soi từng tướng ở ảnh SAU** trước khi báo, theo mục "mong thấy gì" của báo cáo. Nhất là:
   - đầu tia có chạm thân không (Hỏa Nhãn, tia nước, tia Mộc, tia Mặt Trời của Nhật Vương, tia nhiệt Thổ Tinh);
   - khói có thành cụm không;
   - hướng ảnh `kr_*` sau khi co lớp;
   - sóng âm của Rồng Trúc và hổ.

   Sửa lỗi tệ nhất trước; có thể gửi ảnh SAU cho agent từng hệ làm vòng 2.
3. **Đề xuất còn mở** (chi tiết ở cuối từng file `bao_cao/*.md`):
   - Hạt Dẻ (`hat_de`, Thổ) đang bắn tia nước xanh kèm lá vì chưa có mã trong `ThoFx`, rơi về `StageView.Beam`. Cần chiêu riêng (đo giờ trúng trên rig `hat_de_1/2`).
   - `HatLua` chưa biết `StageView.Power`: hiệu ứng mới chưa mạnh dần theo độ khó trận (luật "combat epic theo độ khó"). Cần thêm một trường và đặt trước mỗi lần phát.
   - Vài chiêu cuối vượt trần 120 hạt sống: Hỏa Sơn Long `n_nui_ten` khoảng 159, Nhật Vương khoảng 148, Thần Cơ khoảng 137, Pháo Giáp chiêu mana khoảng 143, Quỷ Xích khoảng 153, Thổ Tinh khoảng 190. Hỏi người dùng có chấp nhận cho chiêu cuối không; Pháo Giáp muốn giảm thì phải bớt tên lửa (đổi ý tưởng).
   - Voọc Tướng chiêu cuối: sáu vệt nổ lại chồng thành ngôi sao kem che mặt (`HatKiem.cs` `VetChem` / `LaLieu`, dùng chung với `HatHo.cs`).
     - Lưu ý: `tho_hoang` dạng 1 vừa đổi rig thành khỉ con (phiên khác), nên bản TRƯỚC / SAU của tướng này lệch hình.
   - Tiểu Quỷ Lava: rig chiêu cuối nhảy vọt ra khỏi khung, bị cắt (việc của rig).
   - Đưa bảng màu tươi của Mộc (`MocTuoi`) vào `WThemes`, của Kim vào `Themes` / `Pal`, thay cho chỗ đang ghi đè lúc chạy.
   - Gom bộ hạt kiểu KR5 (nổ, khói cụm) thành hàm chung cho mọi hệ (hiện mỗi hệ một bản: `HoaNo…`, bộ hạt Kim trong `HatRobot.cs`, `BuiCum` trong `HatMoc.cs`, cụm bụi trong `HatTho.cs`).
4. **Ghi công thức đã chốt** vào `pokiclash-fx-congthuc` (tia chạm thân, khói cụm, tụ cầu, nổ KR5) sau khi người dùng duyệt ảnh SAU.
5. **Đẩy bản skill mới nhất lên SkillForClaude** (mục 1b của `vfx-petclash` và công thức mới).
6. **Chưa commit gì trong repo PokiClash.** Người dùng chưa bảo commit; hỏi trước.
