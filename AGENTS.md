# AGENTS.md (PokiClash)

Trả lời bằng tiếng Việt. Quy tắc chung (auto mode, manual mode, git) nằm ở AGENTS.md cá nhân của người dùng.

- Tổng quan và tiến độ: `GD_Claude/README.md`, `GD_Claude/12_KeHoach_OpenSpec.md`.
- **Làm ở Unity** (người dùng dặn 2026-11-03): số liệu sửa thẳng ở Unity (`Assets/02 Data/Json` rồi menu `PokiClash/Nhập dữ liệu`, hoặc code C#). Bản web `Web/` chỉ làm khi người dùng yêu cầu; không chạy script xuất của web vào Assets.

## Gen ảnh theo file prompt (`ArtGen/**`, người dùng dặn 2026-11-03)

Từ 2026-11-07 Claude gọi Codex bằng `codex exec` (`ArtGen/Heroes/tools/gen_codex.py`); người dùng cũng có thể dán đường dẫn file prompt vào Codex desktop. Cả hai cách đều như nhau:

- **Mỗi lượt là một file prompt (tiếng Anh).** Đọc hết file, mở từng ảnh mẫu theo đường dẫn đầy đủ ghi ở đầu file (`image N = <đường dẫn>: <là gì>`; khi chạy bằng `codex exec` các ảnh này cũng được đính kèm đúng thứ tự), vẽ bằng công cụ gen ảnh, rồi **tự lưu ảnh đúng chỗ mục SAVE ghi**. Trùng tên thì thêm `_2`, `_3`… Không sửa, dời, xoá file nào khác.
- File nhiều bước (lượt nhóm mảnh): mỗi bước một ảnh, lưu đúng tên bước. Khi lệnh chạy bảo vẽ những bước nào thì vẽ đúng những bước đó rồi dừng.
- Không hỏi lại giữa chừng; vẽ xong và lưu xong mới trả lời, câu trả lời chỉ cần đường dẫn ảnh đã lưu.
- **Mọi file prompt đều tự đủ**: không cần mở file khác hay đọc chat.
- **UI không vẽ bóng** (người dùng dặn 2026-11-03): không bóng đổ, bóng lệch cứng, bóng dưới chân hay in xuống nền.

## Hình tướng (người dùng chốt 2026-11-02, bắt buộc)

Đọc `ArtGen/Heroes/QUY_TRINH.md` trước khi làm bất cứ gì với hình tướng.

- **Vẽ đè lên rig vector của aola** (giữ animation aola): con mới khác hẳn con gốc nhưng tay chân trùng rig (cùng số, chỗ, khớp, hướng); đầu, tai, mào, đuôi, phụ kiện đổi dáng tự do, chỉ giữ đầu khớp; thân, tay, chân giữ viền. Vũ khí vẽ riêng thành mảnh thêm, gắn vào tay khi ghép.
- **Nét vẽ tay của game** như ảnh mốc bản đồ `ArtGen/Islands/refs/world_style.png`: vẽ tay trên giấy bằng bút mực (viền nâu sẫm `#2B2118` hơi rung), tô bằng chì màu và sáp màu, nét gạch chéo lộ rõ; vẽ đẹp, không nguệch ngoạc, không bóng loáng kiểu số. **Thiết kế** học từ tướng aola ("style pokemon": dáng gọn mập, mắt to, ít chi tiết), không chép con nào.
- **Tô phẳng, không bóng, không ánh sáng** (người dùng dặn 2026-11-04, mọi tướng): mỗi vùng một màu đều, nét chì sáp chỉ là vân; không mảng sáng tối, không bóng đổ, không điểm sáng trắng, không bóng loáng, không quầng sáng; chỉ chừa một chấm sáng nhỏ trong mắt.
- **Tướng là sinh vật kiểu thú nuôi**, có **vẻ "chiến"**: mặt quả quyết, thế sẵn sàng đánh; dễ thương, không linh vật vui tươi, không đáng sợ. Ngoại lệ dạng người: dòng Tiểu Y (thần biển), dòng Mi Nhi (tiên cá chơi đàn).
- **Viền trắng giấy xé** quanh tướng do game vẽ (shader), không vẽ.
- Prompt sinh từ `ArtGen/Heroes/build.py` vào `ArtGen/Heroes/gui_gpt/<mã>/`; ảnh lưu vào `ArtGen/Heroes/inbox/<mã>/tai_ve/`.
- **Bản quyền:** hình và chuyển động aola là của Baitian; người dùng đã tự quyết dùng làm nền và đính làm mẫu; không đăng công khai.
