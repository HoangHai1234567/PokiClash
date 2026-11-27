# 36. Tranh thẻ bài (gen lại bằng GPT)

Người dùng 2026-11-27: "lên concept gen lại ảnh các thẻ bài bằng gpt", rồi giao Claude tự quyết các lựa chọn.

## 1. Hiện trạng

- **Người chơi thấy 241 thẻ:**
  - 75 thẻ chung (khối `pool`, 5 độ hiếm);
  - 151 thẻ riêng của 50 tướng (Chiêu, Tuyệt kỹ, Bị động, thêm thẻ Tiến Hóa của boss);
  - 15 bị động boss (`traits`).

  Ngoài ra có 90 thẻ của 30 quái lính (`minions`). Nguồn: `Assets/02 Data/Json/cards.json`.
- **Hình trên thẻ chỉ là một icon** 128 px trong ô tròn 156 px (`UiCard.Bind`, prefab `Kit/The` 320 × 464, `TheMini` 200 × 292). Icon lấy qua `ArtLibrary.Icon`: ưu tiên ảnh gen `icon_<tên>`, không có thì dùng icon SVG của bản web (`03 Art/Fallback/Icons`). Gói icon GPT cũ (`ArtGen/Icons`, IC1–IC5) chưa gen lần nào.
- **241 thẻ chỉ có 43 icon:** khiên dùng cho 25 thẻ, đá cho 15, vết nứt cho 14, nên nhiều thẻ trông giống hệt nhau.

## 2. Đã chọn (Claude, 2026-11-27)

| Câu hỏi | Chọn | Lý do |
|---|---|---|
| Hướng | **B**: vẽ tranh riêng cho 75 thẻ chung; thẻ riêng, bị động boss, thẻ quái dùng hình tướng có sẵn | thẻ trông như thẻ sưu tầm mà không bắt GPT vẽ đúng 50 tướng đang làm lại (.atomik) |
| Bỏ | A (chỉ làm lại icon): thẻ vẫn là "icon trong vòng tròn". C (tranh riêng mọi thẻ, khoảng 330 tranh): tướng đổi là tranh lệch, tốn gấp bốn | |
| Cách gen | Claude gọi GPT 2.6 qua Magnific (1k high, 95 credit một tấm, dưới trần 100); vẫn có file prompt theo luật ArtGen để người dùng tự gửi GPT khi muốn | |
| Nét | chì sáp như tướng (`world_style.png` + concept tướng `L3_1.png`), tô phẳng, không bóng, không quầng sáng | đồng bộ với tướng, khác hẳn icon vector |
| Khung thẻ | giữ khung vẽ bằng code, chỉ đổi ô tranh | |

## 3. Mặt thẻ mới

- **Ô tranh** chữ nhật 16:10, khoảng 280 × 175 trên thẻ thường (thẻ mini khoảng 175 × 109), thay ô tròn 156 px. Game tự vẽ viền mực quanh ô. Tên, mô tả, dải màu độ hiếm, băng keo theo loại thẻ giữ nguyên.
- **Thẻ chung: nhìn tranh là hiểu, hoặc đoán được thẻ làm gì** (người dùng dặn 2026-11-27, sau bản đầu vẽ nhiều chân thú). Gần như không có thú.
  - Mỗi tranh ghép từ một bộ ký hiệu chung, thẻ nào cũng vẽ giống nhau, khớp icon chỉ số của game:

    | Ý | Hình |
    |---|---|
    | máu | tim đỏ |
    | hồi máu | dấu cộng xanh lá |
    | máu còn ít | thanh máu đỏ |
    | mana | giọt nước xanh |
    | nộ | lửa cam |
    | công | kiếm thép |
    | thủ | khiên xanh |
    | khiên chắn | bong bóng xanh nhạt |
    | tăng | mũi tên xanh lá chĩa lên |
    | giảm | mũi tên đỏ chĩa xuống |
    | kéo dài nhiều lượt | đồng hồ cát |
    | choáng | sao vàng quanh đầu |
    | độc | bọt xanh lá và bọt hình đầu lâu |
    | thẻ khác trong tay | lá bài trơn |

  - **Địch luôn là một hình nộm rơm** (đầu bao bố mắt khâu, cắm trên cọc gỗ). Thẻ làm gì địch (đánh, đốt, độc, choáng, phá giáp, hút mana) thì vẽ lên hình nộm. Thẻ chỉ giúp mình thì không vẽ hình nộm.
  - Một ý chính to rõ (60–70% ô), có chút động (vệt bay, tia, bụi). Thú hay bộ phận thú chỉ vẽ khi tên thẻ cần, ví dụ cặp nanh của Cắn Xé.
  - Nền: giấy kem, một mảng gạch chì màu nhạt sau vật chính.
  - Cảnh từng thẻ ở `ArtGen/Cards/canh_the_chung.json`, bộ ký hiệu ở `build.py` (mục VISUAL LANGUAGE).
- **Thẻ riêng, bị động boss, thẻ quái** (256 thẻ): không gen tranh. Ô tranh hiện chân dung chủ thẻ (`HeroPortrait`, tự đổi theo dạng sao).
  - Nền là vệt màu theo loại thẻ: Chiêu xanh dương, Tuyệt kỹ hồng, Bị động xanh lá, trùng màu băng keo hiện nay.
  - Góc thẻ có icon chiêu nhỏ.

## 4. Gói gen

- `ArtGen/Cards/build.py` sinh vào `gui_gpt/`:
  - lưới `bo_cuc_<k>.png`;
  - `luot_01.txt` … `luot_09.txt`: mỗi lượt một tấm 1536 × 1024, lưới 3 × 3 ô 464 × 290, thẻ theo thứ tự khối `pool`;
  - `HUONG_DAN.md`.

  Lượt 1 chốt nét. Lượt 2–9 thêm tấm lượt 1 đã duyệt làm ảnh mẫu thứ tư.
- `cat.py <lượt> [--file luot_NN_2.png]`: cắt từng ô, giữ viền mực rung GPT vẽ, trắng ngoài viền thành trong suốt, xuất `ArtGen/Cards/cat/<id>.png` cỡ 448 × 280 RGBA.
  - Ô GPT vẽ cao hơn khuôn (lượt 9) thì cắt giữa còn tỉ lệ 1,45 rồi dán lại dải viền trên và dưới.
- `xem_the.py <lượt>`: dựng mặt thẻ mẫu cỡ thật (cũ và mới) vào `ArtGen/Cards/xem/luot_NN.png` để duyệt.
- `chep_vao_game.py [--kiem]`: chép `cat/` vào `Assets/03 Art/Cards/tranh_<id>.png`.
  - Không đặt tên `card_`: `ArtImporter` cắt 9 mảnh mọi ảnh `card_*`.

## 5. Tiến độ

| Việc | Trạng thái |
|---|---|
| Lượt 1 (Mài Vuốt … Đứng Tấn) | bản đầu `tai_ve/luot_01.png` bị chê nhiều thú. **Bản 2 `tai_ve/luot_01_2.png`** theo bộ ký hiệu, người dùng duyệt 2026-11-27 ("ok ổn làm hết đi rồi thay vào game") |
| Lượt 2–9 (66 thẻ còn lại) | **xong 2026-11-27** (`tai_ve/luot_02.png` … `luot_09.png`, mặt thẻ mẫu `xem/`). Cả bộ tốn 10 × 95 = 950 credit |
| Đưa vào Unity | **2026-11-27**: 75 ảnh `Assets/03 Art/Cards/tranh_<id>.png`, `ArtLibrary.CardArt`, `UiCard` (ô tranh `p.tranh`), menu `PokiClash/Thẻ: thêm ô tranh` (`Editor/CardArtMenu.cs`) sửa prefab `Kit/The`, `Kit/TheMini`. Đã chụp kiểm không cần Play bằng menu `PokiClash/Thử/Thẻ: chụp mặt thẻ có tranh` (`Temp/PokiShots/the_tranh.png`). Chưa thử trong trận khi Play. Xem mục 6 |
| Thẻ riêng dùng chân dung | **chưa làm**: chưa có ảnh chân dung tĩnh cho tướng .atomik (`HeroFaces` trống, `HeroPortrait` chỉ có ảnh aola, `AolaSticker` là rig sống quá nặng cho cả trăm thẻ). Cần nướng một ảnh chân dung mỗi dạng tướng trước |
| 43 icon cùng nét (góc thẻ riêng, Sổ thẻ, rương) | chưa dựng gói; làm sau khi đủ tranh thẻ chung |

Ghi chú nét:
- Giọt mana Hít Thở còn vệt sáng trắng (nhỏ).
- Nhảy Lùi (giày có cánh, mũi tên bay trượt) là tranh khó đoán nhất.
- Thiên Mệnh (lượt 4 ô 8): kiếm bổ đôi đầu hình nộm, trông như hai đầu. Nếu người dùng chê thì gen lại riêng.

## 6. Trong Unity

1. **Ảnh:** `Assets/03 Art/Cards/tranh_<id>.png`, 448 × 280 RGBA, đã có sẵn viền mực.
   - Nhập theo luật chung của `ArtImporter`: sprite, ASTC 6x6, khoảng 56 KB một thẻ, 75 thẻ khoảng 4,2 MB.
   - Muốn nhẹ hơn thì thêm luật ASTC 8x8 cho `/Cards/` (khoảng 2,3 MB), nhưng nét chì sẽ kém hơn; chưa làm.
   - Ảnh nguồn PNG nặng khoảng 21 MB trong repo.
2. **Danh mục:** menu `PokiClash/Dựng lại danh mục ảnh` đưa ảnh vào `ArtLibrary.art`. Tra bằng `ArtLibrary.CardArt(id)`, không cảnh báo khi thiếu.
3. **Prefab:** menu `PokiClash/Thẻ: thêm ô tranh` (chạy lại được).
   - Thêm `o_tranh` (Image 272 × 170, mini 170 × 106) ngay sau `o_hinh`, mặc định tắt.
   - Dời `mo_ta` xuống 266–410 px tính từ đỉnh (mini nhân 0,625).
   - Nối `UiCard.p.tranh`.
4. **`UiCard.Bind`:** thẻ có tranh thì tắt `o_hinh` (ô tròn và icon) và bật `o_tranh`; không có thì giữ như cũ. Thẻ khoá làm mờ cả tranh.
   - **Hàng thẻ trong trận** (ô `TranO`, `BattleView.RenderQueue`, sửa 2026-11-27 sau khi người dùng báo thẻ chọn mới mà lên hàng lại thành icon cũ): thẻ có tranh thì ô dùng tranh, `QueueTile.FitIcon` nới ô hình thành 100 × 76 (tranh giữ tỉ lệ, khoảng 100 × 62); thẻ không tranh giữ icon 76 × 76. Ô bay lên đầu tướng chép cả cỡ. Menu chụp thử có thêm một hàng ô.
5. **Còn lại:**
   - Thẻ riêng, bị động boss, thẻ quái dùng chân dung: cần nướng chân dung tĩnh mỗi dạng tướng trước (mục 5).
   - Soát bằng tour `UiFullAudit`: Sổ thẻ, chọn thẻ trong trận, rương, chi tiết thẻ.
   - Golden không đổi vì không đổi luật.
