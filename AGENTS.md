# AGENTS.md (PokiClash)

Trả lời bằng tiếng Việt. Quy tắc chung (auto mode, manual mode, git) nằm ở AGENTS.md cá nhân của người dùng.

- Tổng quan và tiến độ: `GD_Claude/README.md`, `GD_Claude/12_KeHoach_OpenSpec.md`.
- Bản web `Web/` là nguồn số liệu: sửa web, xuất JSON và golden, rồi chép sang C#.

## Hình tướng (người dùng dặn 2026-11-01, bắt buộc)

Đọc `ArtGen/Heroes/QUY_TRINH.md` trước khi làm bất cứ gì với hình tướng.

- **Theme:**
  - tướng là sinh vật kiểu thú nuôi đánh nhau (pet), không phải người kiểu anime;
  - nét như hình trận aola và 4 thầy tu trong game: viền đều, màu viền là sắc đậm của chính màu nền, tô phẳng 2–3 tông;
  - nét sổ tay vẽ tay (bút chì, sáp) chỉ dành cho UI, không dùng cho tướng.
- **Mỗi tướng là một dòng tiến hóa của aola**, lên sao thì đổi hình. Quái thường lấy dòng 2–4 dạng, boss lấy dòng từ 3 dạng.
- **Cách gen là thay tạo hình trên rig vector của aola** (giữ animation):
  - sinh vật mới phải khác hẳn con gốc, **nhưng tay chân phải trùng rig** (cùng số, cùng chỗ, cùng khớp, cùng hướng);
  - chỉ con vector (`fightassets/pet<id>.swf`) làm được.
- **Viết prompt:**
  - xem từng mảnh trong ngữ cảnh, ghi bảng giải phẫu (là gì, hai đầu nối gì, chĩa hướng nào; trái, phải theo người xem);
  - prompt nói rõ đầu nào của mỗi chi là gì và cái gì không được vẽ;
  - chia nhóm theo chi hoặc bộ phận.
- **Ghép xong phải tự chụp trang so sánh và soi từng chi** trước khi báo. Đếm "đủ mảnh" không thay được việc xem.
- **Không tự đổi số chỉnh của người dùng** (`reskin/<tên>/adjust.json`).
- **Thư mục:**
  - prompt, ảnh đính kèm, ảnh GPT trả về: `ArtGen/Heroes/` (`thuy/<tướng>.md`, `refs/`, `inbox/`);
  - rig và bộ ghép: AolaRipper `D:\Aola-20261029T161238Z-1-001\Aola\AolaRipper\AolaRipper` (`reskin/pet<id>_parts`, `reskin/thuy_<id>`).
- **Môi trường:**
  - Python: `py -3 -I`; in chữ Trung thì `sys.stdout.reconfigure(encoding="utf-8")`;
  - FFDec chạy bằng OpenJDK của Unity;
  - thư mục tạm cho Chrome: `C:\Users\ADMIN\AppData\Local\Temp\aola_work`.

  Chi tiết ở `AGENT.md` của AolaRipper.
- **Bản quyền:**
  - hình và chuyển động gốc là của Baitian; người dùng đã tự quyết dùng làm nền;
  - không đăng công khai, kể cả artifact;
  - không nhắc tên game trong prompt.
