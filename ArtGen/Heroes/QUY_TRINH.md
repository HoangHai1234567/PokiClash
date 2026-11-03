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
- **Không vẽ bóng** (người dùng dặn 2026-11-03, luật chung ở `ArtGen/README.md`):
  - áp cho concept, mảnh, vũ khí và hiệu ứng: không bóng đổ, không bóng dưới chân, không bóng in xuống nền;
  - bóng chì gạch chéo bên trong hình vẫn giữ;
  - `build.py` (`NO_SHADOWS`, gắn vào RENDER và LINE) và `build_fx.py` tự chèn câu này vào mọi file prompt.

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
- `<aola>`: máy này `E:\ProjectAtomik\aola` (có `reskin/pet<id>_parts` của 83 dạng và `reskin/thuy_7` đã ghép; `regions.json`, `groups.json` của #7, #8, #9 chỉ có ở máy kia, ảnh rig dựng từ đó đã có trong `refs/thuy/giot_suong_1..3`); máy kia `D:\Aola-20261029T161238Z-1-001\Aola\AolaRipper\AolaRipper`.

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
  - `luot_1_concept.txt`: ảnh mẫu là bóng xám, bản đồ vùng, tờ mẫu thiết kế (`refs/style/style_sheet.png`, 8 tướng aola, dựng bằng `tools/make_refs.py`), ảnh mốc nét vẽ (bản đồ); dạng 2, 3 của một dòng đính thêm concept đã duyệt của dạng 1 (khoá `prev` trong `FORMS`: giữ màu, mũ, mặt, giáp, nét để cả dòng ra cùng một con lớn lên); GPT lưu `inbox/<mã>/tai_ve/concept.png`;
  - `luot_2_nhom_manh.txt` (chỉ dựng khi đã có concept duyệt): ảnh mẫu là ảnh gốc từng nhóm và concept đã duyệt; GPT vẽ một nhóm mỗi lượt theo thứ tự (2 nhóm gen thử trước, chờ soi), lưu mỗi nhóm thành `inbox/<mã>/tai_ve/<Nxx>.png`;
  - `HUONG_DAN.md`: tiếng Việt, file prompt từng lượt, đường dẫn và mô tả từng ảnh mẫu, kiểm từng ảnh, câu sửa nhanh.
- Người dùng chỉ gửi GPT đường dẫn file prompt (dặn 2026-11-03). File prompt mở đầu bằng danh sách ảnh mẫu kèm đường dẫn đầy đủ (GPT tự mở), rồi chỗ GPT tự lưu ảnh; trùng tên thì GPT thêm `_2`, `_3`.
- Đường dẫn trong gói tính từ chỗ đặt `build.py`, nên chạy được trên cả hai máy.
- Thư mục `1_concept/`, `2_nhom_manh/` trong gói cũ là cách kéo thả trước đây, không dùng nữa.
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
- `variants`: hình biến thể thay một hay nhiều mảnh (ví dụ một hình chứa cả hai tai lúc vẫy tai); `drop_chars` (mặt hoảng, mắt nhắm), `keep_chars` (hiệu ứng). Liệt kê biến thể bằng cách đếm hình không có ở khung đứng đầu rồi xem từng hình. Có con (như #8) thay đuôi, vây, mào bằng biến thể ngay ở clip đứng, nên phải soi cả clip đứng.
  - hình chứa nhiều mảnh rời mỗi mảnh xoay riêng (bốn vây của #8): thêm `"split": true` để mỗi mảnh khớp riêng tâm, góc, cỡ; khớp khung bao chung làm mảnh rời khỏi chỗ.
  - biến thể khác dáng hẳn (thân đuôi uốn của #8): khớp khung bao với `squash` lớn hơn (2,6); muốn đẹp hơn thì cho GPT vẽ lại từng biến thể.
  - biến thể vẽ lại một mảnh, cùng cỡ nhưng xoay trong khung (đầu, thân, chân, đuôi của #9 lúc đánh, chiêu): `"local": true` để khớp theo khung riêng của hình (giữ góc xoay); hình dài mảnh hơn mảnh gốc thì thêm `"squash"`. Khớp khung bao chung làm mất góc xoay (chân thành cột dựng đứng, vây phồng tròn).
- Mảnh vẽ lại sau khi ghép: lượt 3 (`luot_3_ve_lai.txt`, khoá `redo` trong `FORMS`), GPT lưu `<mã>_ve_lai.png`; bộ ghép lấy ảnh mới nhất của mỗi nhóm.

Chạy `py -3 -I tools/ghep_nhom.py reskin/<hệ>_<id>`:
1. tách nền trắng nối với mép, mép nửa trong suốt tính lại từ độ trắng;
2. khớp ảnh mẫu nhóm với mảnh gốc ở khung đứng đầu (tỉ lệ, độ dời; in IoU, cần gần 1);
3. nhóm nhiều mảnh: chia ảnh theo vùng mảnh gốc gần nhất, chồng một dải ở khớp;
4. dựng lại mọi khung của 4 clip, gắn mảnh thêm; ra `sprites/`, `export/anim.json`, `ghep_log.json`.

Sau đó:
- `tools/portrait_png.py reskin/<hệ>_<id>` cho chân dung;
- **soi**: `tools/so_sanh_reskin.py <hệ>_<id> goc_<id> <ảnh> 6` (mỗi clip 6 khung, hàng trên gốc, hàng dưới mới) và phóng to vài khung xem khuỷu, hông, cổ, chỗ cầm vũ khí; không còn hình cũ lọt vào;
- đổi `aola` của dạng đó sang `<hệ>_<id>` ở `Assets/02 Data/Json/heroes.json` rồi menu `PokiClash/Nhập dữ liệu` (làm ở Unity, người dùng dặn 2026-11-03; bản web chỉ sửa khi được yêu cầu); nhập lại hình thành prefab như dưới;
- chụp trong game (menu `PokiClash/Thử/Thanh tiến hóa: chụp hộp chi tiết ở các mốc`).

Bộ ghép này thay cho trình chỉnh sửa cũ (`so_sanh.html`, `adjust.json`) của máy kia; muốn chỉnh tay thì sửa `ghep.json` (góc, độ dài kiếm, độ chồng khớp) rồi chạy lại.

Hình ghép chỉ có ở máy đã ghép (repo aola không mang `reskin/<hệ>_<id>` sang máy kia): ghép xong phải nhập lại thành prefab ở máy đó (menu `PokiClash/Tướng/Nhập hình tướng aola thành prefab`), xem `Library/PokiHeroShots/<tướng>.png` (menu `PokiClash/Tướng/Chụp thử prefab tướng`), rồi commit `Assets/03 Art/Heroes/Resources/<hệ>_<id>/`. Máy không có thư mục ghép thì bộ nhập giữ hình đã nhập, không đè bằng hình gốc.

**Animation viết lại (người dùng dặn 2026-11-03: ghép xong thì sửa animation cho khác bản gốc aola).** `tools/anim_moi.py` dựng lại clip theo khớp từ dáng đứng đầu: mỗi mảnh xoay quanh khớp nối với mảnh cha (khớp tự tìm ở chỗ chồng lên mảnh cha, mảnh chồng nhiều như bắp tay thì ghi `pivot` tay), gốc dời, xoay, co giãn (co ngang qua 0 để xoay người), vệt mờ theo vũ khí, đưa mảnh lên trên trong vài khung. Cấu hình `reskin/<hệ>_<id>/anim_moi.json`; `ghep_nhom.py` tự chạy nó sau khi ghép (ghép lại không mất). Giọt Sương (2026-11-03):
- dạng 1 đánh: giơ kiếm dựng bên mặt (không giơ qua đầu: đầu to, tay ngắn nên che mặt), lao tới, chém bổ xuống;
- dạng 2 đánh: giơ kiếm lên trước, lao tới, chém chéo xuống;
- dạng 3 đánh: lao tới, xoay người (lật ngang) quất đuôi lưỡi kiếm (đuôi là một mảnh cứng nối thấp sau lưng, vung qua đầu kiểu bọ cạp thì quét ngang qua ngực);
- cả ba: clip đứng và trúng đòn mới; clip chiêu giữ bản gốc. Khung lao xa nhất (game lấy làm lúc trúng đòn) trùng nhát chém: 19, 19, 20.
- thử: menu `PokiClash/Thử/Clip đánh Giọt Sương: chụp các dạng (đang Play)`.

**Trong trận (người dùng dặn 2026-11-03):**
- con đang ra đòn nằm trên con kia (StageView.Play);
- clip CHIÊU (1_6) chỉ dùng cho tuyệt kỹ; khoá `"lunge": true` trong anim_moi.json thì trận kéo nó lao tới đối thủ như đòn đánh. Giọt Sương: dạng 1 lao tới xoay vòng chém, dạng 2 lao tới chém bổ, dạng 3 lao tới xoay người quật đuôi lưỡi kiếm (đòn đánh thường dạng 3 đổi thành vồ tới dậm hai chân trước);
- chiêu dùng mana bắn tia: **mặc định của mọi tướng, quái thường và phần lớn mini boss** (người dùng: chỉ số ít boss làm riêng, khai `"mana": "clip"` trong anim_moi.json thì phát clip CHIÊU). Dạng có clip bắn `1_5` (20 khung, trúng ở khung 12) + khoá `"cast"` (mảnh, điểm chỗ bắn, khung, cỡ tia) thì dùng đúng clip và chỗ bắn đó; không có thì đứng nhún về phía đối thủ, tia từ trước ngực, cỡ to dần theo dạng (0,7 tới 1,4; một dạng: 1; boss ×1,2). StageView.Beam phóng prefab `Items/TiaNuoc` (ảnh `Assets/03 Art/Fx/tia_nuoc.png` do `build_fx.py --xuat` cắt từ ảnh GPT FX09, menu `PokiClash/Prefab/Sàn đấu: tia nước của chiêu bắn`); tướng hệ khác tạm nhuộm màu hệ tới khi có ảnh tia riêng từng hệ;
- hiệu ứng vẽ tay của tuyệt kỹ: gói GPT `gui_gpt/giot_suong_fx/` (`build_fx.py`); clip có hiệu ứng nhưng chưa có ảnh thì để `"fx_off": true`;
- thử: menu `PokiClash/Thử/Giọt Sương ra trận: đánh, bắn tia, chiêu cuối ở 3 dạng (đang Play)`.

## 7. Viền trắng giấy xé (Unity, chưa làm)

- Đã có shader `PokiClash/StickerOutline` (`Assets/03 Art/Shaders/StickerOutline.shader`): tướng aola render ra RenderTexture (`AolaSticker`), shader vẽ viền trắng rồi viền mực quanh **cả hình**.
- Kiểu giấy xé: thêm nhiễu theo vị trí để bề rộng viền trắng lồi lõm, mép răng cưa nhỏ, có thể thêm bóng mờ dưới giấy.
- Nếu muốn **viền giấy quanh từng mảnh** (kiểu con rối giấy, lộ mép trắng ở khớp): nướng vào từng PNG mảnh khi xuất (nới alpha, mép răng cưa), không làm bằng shader trên cả hình.

## 8. Thư mục

| Đường dẫn | Chứa gì |
|---|---|
| `ArtGen/Heroes/build.py` | Bảng các dạng, prompt, bộ sinh gói |
| `ArtGen/Heroes/gui_gpt/<mã>/` | Gói gửi GPT: `luot_1_concept.txt`, `luot_2_nhom_manh.txt`, `HUONG_DAN.md` (sinh ra, không sửa tay) |
| `ArtGen/Heroes/refs/<hệ>/<mã>/` | Ảnh rig: bóng xám, bản đồ vùng, rig đánh số, `orig/Nxx.png` |
| `ArtGen/Heroes/refs/style/` | Tờ mẫu thiết kế từ hình aola (`style_sheet.png`); `parts_example.png` của cách bộ mảnh rời, không dùng nữa |
| `ArtGen/Heroes/tools/` | `make_refs.py` (tờ mẫu), `explode.py` |
| `ArtGen/Heroes/inbox/<mã>/tai_ve/` | Ảnh GPT tự lưu (`concept.png`, `<Nxx>.png`), Claude chưa duyệt |
| `ArtGen/Heroes/inbox/<mã>/concept_duyet.png` | Concept đã duyệt |
| `ArtGen/Heroes/refs/style_anchor.png` | Ảnh mốc style: concept Giọt Sương dạng 1 đã chốt |
| `ArtGen/Heroes/inbox/<mã>/Concept*.png` | Concept của các lần trước, không dùng nữa |
