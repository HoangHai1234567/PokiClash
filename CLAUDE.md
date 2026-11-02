# CLAUDE.md (PokiClash)

Trả lời bằng tiếng Việt. Quy tắc chung (auto mode, manual mode, git) nằm ở CLAUDE.md cá nhân của người dùng.

- Tổng quan và tiến độ: `GD_Claude/README.md`, `GD_Claude/12_KeHoach_OpenSpec.md`.
- Bản web `Web/` là nguồn số liệu: sửa web, xuất JSON và golden, rồi chép sang C#.

## File prompt gen ảnh (`ArtGen/**`, người dùng dặn 2026-11-02)

- **Ghi đủ mọi ảnh đính kèm ngay trong file prompt:**
  - đường dẫn đầy đủ trên máy (tuyệt đối, ví dụ `E:\ProjectAtomik\PokiWar\ArtGen\...`), không ghi đường dẫn tương đối hay "…/";
  - ảnh trông như thế nào: nội dung chính, cỡ ảnh, nền;
  - gửi ở bước nào, là ảnh thứ mấy;
  - ảnh chưa có thì ghi "chưa có" và bước nào sinh ra nó.
- Mỗi bước ghi lại danh sách đính kèm theo thứ tự kèm mô tả, và chỗ lưu ảnh trả về (đường dẫn đầy đủ), ngay ở bước đó.
- **Phần gửi GPT mở đầu bằng danh sách ảnh đính kèm theo thứ tự** (`image 1 = <tên file>: <là gì>`), để GPT và người dùng đối chiếu được.
- **Mọi file prompt đều tự đủ**: không bắt người dùng mở file khác hay đọc chat mới biết đính kèm ảnh nào. Trong chat chỉ chỉ tới file và mục, không chép lại danh sách ảnh.
- **Người dùng chỉ kéo thả file**: mỗi lượt gen là một thư mục gồm ảnh đánh số đúng thứ tự và `00_instructions.txt` (GPT đọc rồi vẽ), kèm `HUONG_DAN.md` cho người dùng. GPT chỉ dùng được ảnh mẫu khi ảnh đính thẳng vào tin nhắn, nên không gộp ảnh vào PDF hay zip.
- Mẫu: `ArtGen/Heroes/gui_gpt/<mã>/` (sinh bằng `ArtGen/Heroes/build.py`).

## Hình tướng (người dùng chốt 2026-11-02, bắt buộc)

Đọc `ArtGen/Heroes/QUY_TRINH.md` trước khi làm bất cứ gì với hình tướng (có lịch sử các hướng đã bị bỏ trong ngày).

- **Vẽ đè lên rig vector của aola** (giữ animation aola): con mới khác hẳn con gốc nhưng tay chân trùng rig (cùng số, chỗ, khớp, hướng); đầu, tai, mào, đuôi, phụ kiện đổi dáng tự do, chỉ giữ đầu khớp; thân, tay, chân giữ viền. Vũ khí vẽ riêng thành mảnh thêm, gắn vào cẳng tay khi ghép. Chỉ con vector (`fightassets/pet<id>.swf`) làm được.
- **Nét vẽ tay của game** như ảnh mốc bản đồ `ArtGen/Islands/refs/world_style.png` (viền mực nâu sẫm hơi rung, tô phẳng màu ấm, bóng chì màu gạch chéo; vẽ đẹp, không nguệch ngoạc, không bóng loáng kiểu số); **thiết kế** học từ tướng aola ("style pokemon": dáng gọn mập, mắt to, ít chi tiết), không lấy nét bóng của aola, không chép con nào.
- **Tướng là sinh vật kiểu thú nuôi**, có **vẻ "chiến"**: mặt quả quyết, thế sẵn sàng đánh; dễ thương, không linh vật vui tươi, không đáng sợ.
- **Viền trắng giấy xé** quanh tướng do game vẽ (shader `PokiClash/StickerOutline` thêm mép xé), GPT không vẽ.
- **Mỗi tướng là một dòng tiến hóa của aola** (`GD_Claude/13_DanhSachTuong.md`), lên sao thì đổi dạng; mỗi dạng dùng rig của đúng con aola ứng với nó.
- **Viết prompt:** xem từng mảnh trong ngữ cảnh, ghi giải phẫu (là gì, hai đầu nối gì, chĩa hướng nào; trái, phải theo người xem); nói rõ đầu nào của mỗi chi là gì và cái gì không được vẽ; độ dày viền ghi bằng pixel cho từng nhóm theo tỉ lệ phóng của ảnh mẫu; không nhắc tên game.
- **Gói gửi GPT** sinh bằng `ArtGen/Heroes/build.py` vào `ArtGen/Heroes/gui_gpt/<mã>/` (concept trên rig, rồi từng nhóm mảnh); đính hình aola làm mẫu được (người dùng cho phép). Ảnh GPT trả về ở `ArtGen/Heroes/inbox/<mã>/tai_ve/`.
- **Ghép xong phải tự chụp trang so sánh và soi từng chi** trước khi báo. Đếm "đủ mảnh" không thay được việc xem.
- **Không tự đổi số chỉnh của người dùng** (`reskin/<tên>/adjust.json`).
- **Rig và bộ ghép:** AolaRipper, máy này `E:\ProjectAtomik\aola` (thư mục `Aola*` cạnh project), máy kia `D:\Aola-20261029T161238Z-1-001\Aola\AolaRipper\AolaRipper` (`reskin/pet<id>_parts`, `reskin/<hệ>_<id>`). Python `py -3 -I`, in chữ Trung thì `sys.stdout.reconfigure(encoding="utf-8")`; FFDec chạy bằng Java (OpenJDK của Unity nếu máy không có). Chi tiết ở `AGENT.md` của AolaRipper.
- **Bản quyền:** hình và chuyển động aola là của Baitian; người dùng đã tự quyết dùng làm nền và đính làm mẫu cho GPT; không đăng công khai, kể cả artifact.
