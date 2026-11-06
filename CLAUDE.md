# CLAUDE.md (PokiClash)

Trả lời bằng tiếng Việt. Quy tắc chung (auto mode, manual mode, git) nằm ở CLAUDE.md cá nhân của người dùng.

- Tổng quan và tiến độ: `GD_Claude/README.md`, `GD_Claude/12_KeHoach_OpenSpec.md`.
- **Làm ở Unity** (người dùng dặn 2026-11-03): chỉ làm bản web `Web/` khi người dùng yêu cầu. Số liệu sửa thẳng ở Unity (`Assets/02 Data/Json` rồi menu `PokiClash/Nhập dữ liệu`, hoặc code C#); golden trong `Assets/02 Data/Golden` là bản chụp lần xuất web cuối, đổi luật thì sửa golden và test bên Unity.

## File prompt gen ảnh (`ArtGen/**`, người dùng dặn 2026-11-02, đổi 2026-11-03)

- **Người dùng chỉ gửi GPT đường dẫn một file prompt**: mỗi lượt gen là một file (tiếng Anh). GPT tự mở ảnh mẫu theo đường dẫn ghi trong file và tự lưu ảnh vào chỗ file chỉ. Trong chat chỉ đưa người dùng đường dẫn file prompt. Không bắt kéo thả, không chép ảnh mẫu vào thư mục gói.
- **File prompt mở đầu bằng danh sách ảnh mẫu theo thứ tự** (`image 1 = <đường dẫn đầy đủ>: <là gì>`):
  - đường dẫn tuyệt đối trên máy đang chạy, không ghi đường dẫn tương đối hay "…/";
  - script sinh gói tính đường dẫn từ chỗ đặt nó, không ghi cứng ổ đĩa (hai máy khác ổ).
- Ngay sau đó là mục **SAVE**: đường dẫn đầy đủ để GPT lưu ảnh (trùng tên thì thêm `_2`, `_3`…), dặn không sửa, dời, xoá file khác. Lượt nhiều ảnh thì mỗi bước ghi chỗ lưu riêng.
- Lượt cần ảnh chưa có (sinh ở lượt trước) thì chưa dựng file prompt của lượt đó. Claude dựng khi duyệt xong lượt trước.
- **Mọi file prompt đều tự đủ**: GPT và người dùng không phải mở file khác hay đọc chat mới biết dùng ảnh nào, lưu đâu.
- **UI không vẽ bóng** (người dùng dặn 2026-11-03): không bóng đổ, bóng lệch cứng, bóng dưới chân hay in xuống nền; bóng chì gạch chéo bên trong hình vẫn giữ. **Tướng** (concept, mảnh, vũ khí, hiệu ứng, mặt tướng) theo luật 2026-11-04: tô phẳng, không bóng, không ánh sáng (xem mục Hình tướng). Câu dán vào prompt ở `ArtGen/README.md`, mục "Luật chung".
- Kèm `HUONG_DAN.md` (tiếng Việt) cho người dùng: file prompt từng lượt; từng ảnh mẫu trông như thế nào (nội dung chính, cỡ ảnh, nền); chỗ lưu; cách kiểm; câu sửa nhanh.
- Mẫu:
  - `ArtGen/Heroes/build.py`, sinh gói `ArtGen/Heroes/gui_gpt/<mã>/`;
  - `ArtGen/Islands/build_zone70.py`, sinh gói `ArtGen/Islands/gui_gpt/zone_thuy_70/`.

## Hình tướng (người dùng chốt 2026-11-02, bắt buộc)

Đọc `ArtGen/Heroes/QUY_TRINH.md` trước khi làm bất cứ gì với hình tướng (có lịch sử các hướng đã bị bỏ trong ngày).

- **Vẽ đè lên rig vector của aola** (giữ animation aola): con mới khác hẳn con gốc nhưng tay chân trùng rig (cùng số, chỗ, khớp, hướng); đầu, tai, mào, đuôi, phụ kiện đổi dáng tự do, chỉ giữ đầu khớp; thân, tay, chân giữ viền. Vũ khí vẽ riêng thành mảnh thêm, gắn vào cẳng tay khi ghép. Chỉ con vector (`fightassets/pet<id>.swf`) làm được.
- **Nét vẽ tay của game** như ảnh mốc bản đồ `ArtGen/Islands/refs/world_style.png`: hình vẽ tay trên giấy bằng bút mực (viền nâu sẫm hơi rung), tô bằng chì màu và sáp màu; vẽ đẹp, không nguệch ngoạc, không bóng loáng kiểu số. **Thiết kế** học từ tướng aola ("style pokemon": dáng gọn mập, mắt to, ít chi tiết), không lấy nét bóng của aola, không chép con nào.
- **Tô phẳng, không bóng, không ánh sáng** (người dùng dặn 2026-11-04, mọi tướng): mỗi vùng một màu đều, nét chì sáp chỉ là vân; không mảng sáng tối, không bóng đổ, không điểm sáng trắng, không bóng loáng, không quầng sáng; chừa một chấm sáng nhỏ trong mắt.
- **Tướng là sinh vật kiểu thú nuôi**, có **vẻ "chiến"**: mặt quả quyết, thế sẵn sàng đánh; dễ thương, không linh vật vui tươi, không đáng sợ. Ngoại lệ dạng người: dòng Tiểu Y là thần biển Poseidon (người dùng chốt 2026-11-04); dòng Mi Nhi là tiên cá chơi đàn (người dùng chốt 2026-11-06).
- **Viền trắng giấy xé** quanh tướng do game vẽ (shader `PokiClash/StickerOutline` thêm mép xé), GPT không vẽ.
- **Mỗi tướng là một dòng tiến hóa của aola** (`GD_Claude/13_DanhSachTuong.md`), lên sao thì đổi dạng; mỗi dạng dùng rig của đúng con aola ứng với nó.
- **Viết prompt:** xem từng mảnh trong ngữ cảnh, ghi giải phẫu (là gì, hai đầu nối gì, chĩa hướng nào; trái, phải theo người xem); nói rõ đầu nào của mỗi chi là gì và cái gì không được vẽ; độ dày viền ghi bằng pixel cho từng nhóm theo tỉ lệ phóng của ảnh mẫu; không nhắc tên game.
- **Gói gửi GPT** sinh bằng `ArtGen/Heroes/build.py` vào `ArtGen/Heroes/gui_gpt/<mã>/`: `luot_1_concept.txt` (concept trên rig), `luot_2_nhom_manh.txt` (từng nhóm mảnh). Dùng hình aola làm ảnh mẫu được (người dùng cho phép). GPT tự lưu ảnh vào `ArtGen/Heroes/inbox/<mã>/tai_ve/`.
- **Ghép xong phải tự chụp trang so sánh và soi từng chi** trước khi báo. Đếm "đủ mảnh" không thay được việc xem.
- **Không tự đổi số chỉnh của người dùng** (`reskin/<tên>/adjust.json`).
- **Rig và bộ ghép:** AolaRipper, máy này `E:\ProjectAtomik\aola` (thư mục `Aola*` cạnh project), máy kia `D:\Aola-20261029T161238Z-1-001\Aola\AolaRipper\AolaRipper` (`reskin/pet<id>_parts`, `reskin/<hệ>_<id>`). Python `py -3 -I`, in chữ Trung thì `sys.stdout.reconfigure(encoding="utf-8")`; FFDec chạy bằng Java (OpenJDK của Unity nếu máy không có). Chi tiết ở `AGENT.md` của AolaRipper.
- **Bản quyền:** hình và chuyển động aola là của Baitian; người dùng đã tự quyết dùng làm nền và đính làm mẫu cho GPT; không đăng công khai, kể cả artifact.
