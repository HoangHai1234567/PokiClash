# Quy trình gen hình tướng (2026-11-02)

Người dùng chốt (2026-11-02), sau nhiều lần đổi trong ngày:
- **vẫn vẽ đè lên rig vector của aola** để giữ animation aola;
- **nét vẽ tay của game** như ảnh mốc bản đồ, **thiết kế** học từ tướng aola;
- tướng có **vẻ "chiến"**;
- **viền trắng kiểu giấy xé** quanh tướng do game vẽ (shader), GPT không vẽ.

Mọi file prompt tướng cũ (`PROMPTS.md`, `Thuy.md`, `thuy/*.md`) đã xoá; prompt nay sinh từ `build.py`.

## 1. Phong cách

- **Tướng là sinh vật kiểu thú nuôi đánh nhau**, không phải người.
- **Nét vẽ** lấy từ `ArtGen/Islands/refs/world_style.png`:
  - viền mực nâu sẫm `#2B2118` dày đều, hơi rung như bút thật;
  - tô phẳng màu ấm, bóng bằng chì màu gạch chéo, vài điểm sáng trắng nhỏ;
  - họa sĩ vẽ tay đẹp: không nguệch ngoạc kiểu trẻ con, không quá chi tiết;
  - không bóng loáng kiểu số, không chuyển sắc, không 3D.
- **Thiết kế** học từ tướng aola (người dùng gọi là "style pokemon"): dáng gọn mập, đọc được khi nhỏ, mắt to, hình đơn giản, ít chi tiết. Không lấy nét bóng loáng của aola, không chép con nào.
- **Vẻ "chiến"**: mày xếch xuống, cười tự tin lộ răng nanh nhỏ, thế sẵn sàng đánh; dễ thương, không linh vật vui tươi, không đáng sợ.
- **Viền trắng giấy xé**: game vẽ bằng shader (mục 7). Prompt dặn GPT không vẽ viền trắng.

Lịch sử 2026-11-02 (để khỏi lặp lại):
- nét vector bóng như hình gốc: "không giống style game";
- nét trẻ con vẽ vở nháp: "xấu";
- nét số bóng loáng kiểu sprite: "mất style vẽ tay";
- bỏ rig, vẽ bộ mảnh rời: người dùng quay lại rig cũ;
- kỳ giông, cá chép: bỏ; Giọt Sương dạng 1 là tinh linh nước hiệp sĩ tập sự.

**Concept đầu tiên được chốt** (2026-11-02): Giọt Sương dạng 1, `inbox/giot_suong_1/concept_duyet.png` (bản giáp ngực trơn, găng giáp bạc, kiếm chắn tay vàng). Chép thành **ảnh mốc style** `refs/style_anchor.png`: concept các tướng sau đính thêm ảnh này (lấy nét và độ chi tiết, không lấy thiết kế).

## 2. Rig

- **Mỗi tướng là một dòng tiến hóa của aola** (`GD_Claude/13_DanhSachTuong.md`); mỗi dạng vẽ đè lên rig của đúng con aola ứng với dạng đó. Chỉ con vector (`fightassets/pet<id>.swf`) làm được.
- **Con mới khác hẳn con gốc, nhưng tay chân trùng rig**: cùng số chi, khớp cùng chỗ, chi chĩa cùng hướng, đầu nào nối với gì giữ nguyên.
- Hai loại nhóm:
  - **đổi dáng** (đầu, tai, mào, đuôi, phụ kiện): viền theo concept, to hơn được; chỉ đầu khớp ở nguyên chỗ;
  - **giữ viền** (thân, tay, chân): giữ viền hình gốc, lấy màu, chi tiết, nét từ concept.
- **Vũ khí, đồ cầm tay**: vẽ riêng thành một mảnh thêm (không có ảnh gốc); bàn tay vẽ nắm chuôi. Claude gắn mảnh vào mảnh cẳng tay khi ghép, nên vũ khí đi theo tay ở mọi khung. Animation vẫn là của con gốc: con gốc không chém thì kiếm chỉ đi theo tay.
- Ảnh rig của mỗi dạng ở `refs/<hệ>/<mã>/`: `Silhouette.png`, `RegionMap.png`, `Rig_Numbered.png`, `orig/Nxx.png` (hình gốc từng nhóm, vuông 1024, nền trắng, đúng chỗ trên rig). Dựng bằng công cụ AolaRipper (`part_map.py`, `region_map.py`, `orig_refs.py` theo `regions.json`, `groups.json` ở `<aola>/reskin/<hệ>_<id>/`).
- `<aola>`: máy này `E:\ProjectAtomik\aola` (có `reskin/pet<id>_parts` của 83 dạng; chưa có `thuy_7` với `regions.json`, `groups.json`, phải dựng lại trước khi ghép); máy kia `D:\Aola-20261029T161238Z-1-001\Aola\AolaRipper\AolaRipper`.

## 3. Viết prompt

- Xem từng mảnh trong ngữ cảnh, ghi bảng giải phẫu: mảnh là gì, hai đầu nối gì, chĩa hướng nào; trái, phải theo người xem.
- Concept: mục **KEEP FROM THE RIG** (số phần, chỗ khớp, hướng chi, cỡ thân tay chân) và **CHANGE** (từng vùng thành gì).
- Nhóm: nói rõ đầu nào của chi là gì ("TOP end = shoulder", "hand at the BOTTOM end") và cái **không được vẽ**. Hình mảnh cũ thắng cách hiểu thông thường.
- **Độ dày viền theo pixel từng nhóm**: ảnh mẫu mỗi nhóm phóng một tỉ lệ khác nhau, ghi chung một tỉ lệ thì ghép xong viền lệch nhau.
  - tỉ lệ phóng = cỡ vật trong `orig/Nxx.png` ÷ cỡ vùng đó trong `RegionMap.png`;
  - viền đích ≈ 0,85% chiều cao cả con trong `RegionMap.png` (khoảng 3 px khi con cao 350 px trong game);
  - số px = viền đích × tỉ lệ phóng. Rig #7: N01, N02 khoảng 10 px; N07 khoảng 25 px; N03–N06, N08 khoảng 28 px; mảnh kiếm vẽ riêng khoảng 18 px.
- Không nhắc tên game nào trong prompt.

## 4. Gói gửi GPT

- `build.py` giữ bảng `FORMS` (thiết kế, giải phẫu, prompt concept, prompt từng nhóm, mảnh thêm, thứ tự gen thử) và sinh `gui_gpt/<mã>/`:
  - `1_concept/`: `00_instructions.txt` + bóng xám, bản đồ vùng, tờ mẫu thiết kế (`refs/style/style_sheet.png`, 8 tướng aola, dựng bằng `tools/make_refs.py`), ảnh mốc nét vẽ (bản đồ);
  - `2_nhom_manh/`: `00_instructions.txt` + ảnh gốc từng nhóm + concept đã duyệt; GPT vẽ một nhóm mỗi lượt theo thứ tự (2 nhóm gen thử trước, chờ soi);
  - `HUONG_DAN.md`: tiếng Việt, đường dẫn đầy đủ và mô tả từng ảnh, kiểm từng ảnh, câu sửa nhanh.
- Người dùng mở thư mục con, chọn hết file, kéo vào ChatGPT, gửi. GPT chỉ dùng được ảnh mẫu khi ảnh đính thẳng vào tin nhắn, nên không gộp vào PDF hay zip.
- Ảnh GPT trả về để vào `inbox/<mã>/tai_ve/`, không cần đổi tên; Claude nhận ra từng ảnh qua hình.
- Đính hình aola cho GPT: người dùng cho phép ("cứ đính hình vào", 2026-11-02).

## 5. Claude duyệt

**Concept** ("duyệt concept <mã>"):
- nét vẽ tay như bản đồ, không bóng loáng; thiết kế gọn, không chép con aola nào; vẻ chiến;
- đủ, đúng chỗ như rig: số chi, khớp, hướng chi, bàn tay ở đầu dưới;
- duyệt xong: lưu `inbox/<mã>/concept_duyet.png`, chạy lại `build.py` để gói lượt 2 có concept.

**Nhóm** ("soi thử <mã>" cho 2 nhóm đầu, rồi "ghép <mã>"):
- chồng ảnh lên `orig/Nxx.png`: vật đúng chỗ, đầu khớp đúng chỗ cũ, bàn tay bàn chân đúng đầu;
- nét như concept, viền dày gần số đã ghi; nền trắng, không viền trắng quanh mảnh.

## 6. Ghép (Claude)

Công cụ ở repo aola (`<aola>/tools/`), cấu hình mỗi dạng ở `<aola>/reskin/<hệ>_<id>/ghep.json` (mẫu: `reskin/thuy_7/ghep.json`):
- `groups`: nhóm → mảnh (số theo thứ tự vẽ khung đứng đầu, như `Rig_Numbered.png`), mảnh ẩn (`drop`: mắt, má, miệng cũ khi đầu mới đã vẽ mặt);
- `extra`: mảnh vẽ riêng gắn vào một mảnh (kiếm: `attach`, góc lưỡi, độ dài theo chiều cao con);
- `variants`: hình biến thể thay một hay nhiều mảnh (ví dụ một hình chứa cả hai tai lúc vẫy tai); `drop_chars` (mặt hoảng, mắt nhắm), `keep_chars` (hiệu ứng). Liệt kê biến thể bằng cách đếm hình không có ở khung đứng đầu rồi xem từng hình.

Chạy `py -3 -I tools/ghep_nhom.py reskin/<hệ>_<id>`:
1. tách nền trắng nối với mép, mép nửa trong suốt tính lại từ độ trắng;
2. khớp ảnh mẫu nhóm với mảnh gốc ở khung đứng đầu (tỉ lệ, độ dời; in IoU, cần gần 1);
3. nhóm nhiều mảnh: chia ảnh theo vùng mảnh gốc gần nhất, chồng một dải ở khớp;
4. dựng lại mọi khung của 4 clip, gắn mảnh thêm; ra `sprites/`, `export/anim.json`, `ghep_log.json`.

Sau đó:
- `tools/portrait_png.py reskin/<hệ>_<id>` cho chân dung;
- **soi**: `tools/so_sanh_reskin.py <hệ>_<id> goc_<id> <ảnh> 6` (mỗi clip 6 khung, hàng trên gốc, hàng dưới mới) và phóng to vài khung xem khuỷu, hông, cổ, chỗ cầm vũ khí; không còn hình cũ lọt vào;
- đổi `aola` của dạng đó sang `<hệ>_<id>` ở `Web/src/core/data/heroes.ts`, `Assets/02 Data/Json/heroes.json`, `Assets/02 Data/HeroDb.asset`;
- chụp trong game (menu `PokiClash/Thử/Thanh tiến hóa: chụp hộp chi tiết ở các mốc`).

Bộ ghép này thay cho trình chỉnh sửa cũ (`so_sanh.html`, `adjust.json`) của máy kia; muốn chỉnh tay thì sửa `ghep.json` (góc, độ dài kiếm, độ chồng khớp) rồi chạy lại.

## 7. Viền trắng giấy xé (Unity, chưa làm)

- Đã có shader `PokiClash/StickerOutline` (`Assets/03 Art/Shaders/StickerOutline.shader`): tướng aola render ra RenderTexture (`AolaSticker`), shader vẽ viền trắng rồi viền mực quanh **cả hình**.
- Kiểu giấy xé: thêm nhiễu theo vị trí để bề rộng viền trắng lồi lõm, mép răng cưa nhỏ, có thể thêm bóng mờ dưới giấy.
- Nếu muốn **viền giấy quanh từng mảnh** (kiểu con rối giấy, lộ mép trắng ở khớp): nướng vào từng PNG mảnh khi xuất (nới alpha, mép răng cưa), không làm bằng shader trên cả hình.

## 8. Thư mục

| Đường dẫn | Chứa gì |
|---|---|
| `ArtGen/Heroes/build.py` | Bảng các dạng, prompt, bộ sinh gói |
| `ArtGen/Heroes/gui_gpt/<mã>/` | Gói gửi GPT (sinh ra, không sửa tay) |
| `ArtGen/Heroes/refs/<hệ>/<mã>/` | Ảnh rig: bóng xám, bản đồ vùng, rig đánh số, `orig/Nxx.png` |
| `ArtGen/Heroes/refs/style/` | Tờ mẫu thiết kế từ hình aola (`style_sheet.png`); `parts_example.png` của cách bộ mảnh rời, không dùng nữa |
| `ArtGen/Heroes/tools/` | `make_refs.py` (tờ mẫu), `explode.py` |
| `ArtGen/Heroes/inbox/<mã>/tai_ve/` | Ảnh GPT trả về, chưa đặt tên |
| `ArtGen/Heroes/inbox/<mã>/concept_duyet.png` | Concept đã duyệt |
| `ArtGen/Heroes/refs/style_anchor.png` | Ảnh mốc style: concept Giọt Sương dạng 1 đã chốt |
| `ArtGen/Heroes/inbox/<mã>/Concept*.png` | Concept của các lần trước, không dùng nữa |
