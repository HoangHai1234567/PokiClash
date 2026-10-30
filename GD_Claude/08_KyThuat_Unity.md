# Kỹ thuật (Unity)

Project: `E:\ProjectAtomik\PokiWar`, Unity 6000.0.73f1, URP, Input System, uGUI. Hiện chỉ có `SampleScene`. Cài đặt màn dọc: [02_ManHinhDoc.md](02_ManHinhDoc.md).

## Dùng lại bản Block Blast ở 2PlayersGame

`E:\ProjectAtomik\2PlayersGame\Assets\01Script\MiniGames\BlockBlast\` (thiết kế: `2PlayersGame/openspec/changes/add-block-blast-minigame/design.md`).

**Dùng lại được (phần logic thuần, không phụ thuộc Unity):**

| File | Làm gì | Dùng cho PokiWar |
|---|---|---|
| `BlockBlastBoard.cs` | bàn bitboard `ulong` + mảng màu; kiểm đặt khối, đường đầy | giữ, thêm lớp ô đặc biệt (đá, băng, khiên…) |
| `BlockShape.cs`, `BlockBlastShapeSet.cs` | 41 hình khối | giữ |
| `BlockBlastAdvisor.cs` | tìm nước tốt nhất | gợi ý, và máy tự chơi để cân ải |
| `BlockBlastAutoPlayer.cs`, `BlockBlastProbeSuite.cs` | máy tự chơi hết ván, đo điểm và số lượt | đo tỉ lệ thắng từng ải theo sức mạnh đội |
| `BlockBlastDragModel.cs` | kéo khối: nhấc lên trên ngón, hút vào ô gần nhất | giữ; hợp màn dọc |
| `BlockBlastScoring.cs` | điểm, combo | thay bằng công thức sát thương |

**Không dùng:**

- Hình, hiệu ứng và âm thanh của bản đó chép từ game "1 2 3 4 Player Games" (rip). PokiWar phải làm hình riêng.
- `BasicBlockPicker.cs` chuyển từ mã dịch ngược của game gốc. Nên viết bộ chọn khối mới (đằng nào cũng phải chọn khối theo màu đội) và chỉ giữ ý tưởng: ưu tiên khối tạo đường lúc đầu, rút dần về sau; tay "cứu" khi sắp hết chỗ.
- Asmdef `Game.BlockBlast` tham chiếu `Game.Core` của 2PlayersGame. Chép sang thì bỏ tham chiếu đó.

## Cấu trúc đề xuất

- `Assets/01Script/Puzzle/`: bàn, khối, bộ chọn khối, sập. Thuần C#, có test.
- `Assets/01Script/Battle/`: đội, địch, lượt, sát thương, hiệu ứng. Thuần C#, nhận sự kiện "đã xoá các ô sau" từ Puzzle.
- `Assets/01Script/Meta/`: tướng, thu phục, máy bi, lưu.
- `Assets/01Script/View/`: hiển thị và hoạt cảnh, chỉ nghe sự kiện.
- Dữ liệu tướng, địch, ải là ScriptableObject.

Tách thuần C# để **máy tự chơi chạy được cả trận ngoài Unity**. Mỗi ải chạy vài trăm trận với đội chuẩn của mốc đó, đo tỉ lệ thắng và số lượt trung bình, trước khi người thật chơi. Bản Block Blast cũ đã làm việc này (200 ván mỗi độ khó).

## Hoạt cảnh tướng

- Bộ ghép ở dự án aola xuất `reskin/<tên>/export/anim.json`: vị trí và ma trận từng mảnh theo khung cho 4 animation. Cần một bộ đọc trong Unity dựng mảnh thành `SpriteRenderer` con, rồi chạy theo khung (hoặc đổi sang Spine như `aola/TIEN_DO.md` đề xuất).
- Xem lưu ý bản quyền ở [06_Tuong_NuoiDuong.md](06_Tuong_NuoiDuong.md) trước khi đưa hình đó vào build.

## Các mốc

1. **Bản thử lõi**: bàn 8 × 8 có màu hệ, 3 tướng, 1 địch có ném đá, màn dọc. Câu hỏi: xếp theo màu có vui không.
2. **Một chương**: 5 hệ, chiêu, 10 ải, boss, hết chỗ thành choáng, máy tự chơi đo từng ải.
3. **Thu phục và nuôi**: pha phong ấn, mảnh, danh sách tướng, cấp, sao, tiến hóa, lưu.
4. **Máy bi**.
5. **Bàn sập**, Tháp Viễn Chinh.
