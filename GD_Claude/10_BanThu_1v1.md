# Bản thử 1 đấu 1

Người dùng chốt 2026-10-30:
- làm bản thử **cả A (xếp khối) và C (xếp ngọc)**;
- **1 tướng đánh solo 1 đấu 1 địch**;
- tướng lấy từ các con đã gen trong dự án aola, **chỉ dùng trong bản thử**.

Mục tiêu: chơi hai bản cạnh nhau rồi chọn lõi.

## Một tướng thì màu là hành động

Đội nhiều hệ để sau, nên ở bản thử **màu không phải hệ mà là hành động**, đúng kiểu Pokiwar ("ngọc quyết định tấn công, phòng thủ, xuất chiêu hay hồi phục"). Hai bản dùng chung 4 màu:

| Màu | Hành động khi xoá (A) hoặc khi ghép (C) |
|---|---|
| Đỏ | tướng đánh: sát thương theo số ô |
| Lam | khiên: chặn một phần đòn địch kế tiếp |
| Lục | hồi máu |
| Vàng | nạp nộ; nộ đầy thì chạm chân dung để tung chiêu |

Hệ số đề xuất ban đầu, cùng cho hai bản để so cho công bằng:
- mỗi ô Đỏ: 10 sát thương;
- mỗi ô Lam: 6 khiên;
- mỗi ô Lục: 5 máu;
- mỗi ô Vàng: 10 % nộ;
- combo: × (1 + 0,25 × bậc).

## Hai bàn

| | A. Xếp khối | C. Xếp ngọc |
|---|---|---|
| Bàn | 8 × 8, trống lúc đầu | 7 cột × 7 hàng, đầy ngọc |
| Thao tác | kéo 1 trong 3 khối vào bàn | đổi chỗ 2 ngọc kề nhau |
| Ra đòn | xoá hàng/cột; mỗi ô trong đường xoá làm hành động theo màu | 3 ngọc cùng màu trở lên thẳng hàng |
| Combo | xoá ở lượt liền nhau | ngọc rơi xuống tạo ghép tiếp (dây chuyền) |
| Bất lợi riêng | hết chỗ đặt: choáng, mất 20 % máu, nổ giữa bàn | không còn nước đi: xáo bàn |

Bản A có thể bật **sập** (ô rơi sau khi xoá, như [03_XepKhoi.md](03_XepKhoi.md)) bằng một công tắc, để thử luôn A có trọng lực.

## Phần dùng chung

- **Sân đấu dọc** như [02_ManHinhDoc.md](02_ManHinhDoc.md):
  - địch ở trên;
  - tướng mình ở dưới sân;
  - chân dung tướng có vòng nộ;
  - bàn ở nửa dưới.
- **Địch:**
  - có máu, công và bộ đếm lượt (đề xuất cứ 3 lượt đánh một lần);
  - có một kỹ năng bàn, báo trước một lượt:
    - ở A là ném 3 ô đá;
    - ở C là biến 3 ngọc thành đá.
- **Chiêu tướng:** sát thương lớn và một tác dụng lên bàn. Mỗi tướng một chiêu.
- **Animation từ aola:**

  | Lúc trong trận | Clip aola |
  |---|---|
  | chờ | `1_1` đứng |
  | bị đánh | `1_2` trúng đòn |
  | xoá Đỏ | `1_4` đánh thường |
  | tung chiêu | `1_6` chiêu |

- **Thắng, thua:** địch hết máu là thắng; tướng hết máu là thua. Ghi số lượt và thời gian để so hai bản.

## Tướng có sẵn trong aola

Gốc là dòng 兔小子 của Aola, đã đổi tạo hình. Mới có **mặt trước**.

| Tướng | Thư mục | `export/anim.json` |
|---|---|---|
| Võ sư | `aola/reskin/monk_boxer/` | có |
| Đại sư cà sa (#2217) | `aola/reskin/monk_2217/` | có |
| Võ tăng Bồ Đề (#500) | `aola/reskin/monk_500/` | có (xuất 30/10) |
| Thiền sư Pháp Luân (#2010) | `aola/reskin/monk_2010/` | có (xuất 30/10) |

Trong game, địch là tướng đứng sau tướng mình trong danh sách: Đại sư cà sa → Võ sư → Võ tăng Bồ Đề → Thiền sư Pháp Luân → quay lại Đại sư cà sa. Khi đang Play, menu **PokiWar → Đổi tướng** chuyển sang tướng kế tiếp.

`anim.json` gồm:
- 25 khung/giây;
- 4 clip `1_1`, `1_2`, `1_4`, `1_6`;
- mỗi khung là danh sách hình xếp từ sau ra trước, mỗi hình `[chỉ số sprite, a, b, c, d, tx, ty, alpha]`;
- ma trận đi từ điểm ảnh của sprite sang điểm ảnh của clip (gốc trên trái, y hướng xuống);
- `sprites` là đường dẫn PNG tính từ thư mục reskin.

Unity cần một bộ đọc dựng mỗi hình thành một `SpriteRenderer` (lật trục y) và đổi khung theo 25 fps.

**Mặt sau:** tướng phe mình đứng dưới sân lẽ ra quay lưng. Bản thử dùng tạm mặt trước, thu nhỏ, đặt chéo góc dưới trái; địch to hơn ở góc trên phải (bố cục Pokémon). Có cần làm mặt sau hay không thì quyết sau khi chơi thử.

**Bản quyền:** hình chỉ để trong bản thử, không đưa vào build phát hành ([06_Tuong_NuoiDuong.md](06_Tuong_NuoiDuong.md)).

## MCP cho Unity

Đã thêm gói `com.coplaydev.unity-mcp` (MCP for Unity, bản v9.5.3, cùng bản với ClashMaster) vào `Packages/manifest.json`. Người dùng mở Unity để gói tải về, rồi bật MCP trong cửa sổ của gói.

## Đã làm (2026-10-30)

**Chạy:**
1. Mở scene `Assets/00 Scenes/BanThu.unity`, hoặc vào menu **PokiWar → Mở scene bản thử**.
2. Game view chọn 1080x1920 (menu **PokiWar → Game view 1080x1920**).
3. Bấm Play. Ở menu, chọn tướng, chọn bàn, bấm BẮT ĐẦU.

**Đã đổi project:** Default Orientation chuyển sang Portrait, bỏ tự xoay; scene bản thử đứng đầu Build Settings.

**Code** (`Assets/01 Script/BanThu/`, tự dựng mọi thứ lúc chạy, chưa có prefab):

| File | Làm gì |
|---|---|
| `Battle.cs` | trận 1 đấu 1, số máu, sát thương, khiên, nộ, địch đánh và ném đá |
| `BlockBoard.cs` | bàn A: 13 hình gốc tự viết (xoay, lật), chọn khối, xoá đường, sập, choáng |
| `GemBoard.cs` | bàn C: đổi chỗ, ghép, rơi, dây chuyền, đá, xáo khi hết nước |
| `AolaActor.cs` | đọc `anim.json` của aola, mỗi hình một quad theo ma trận Flash; PNG đọc thẳng từ `E:/ProjectAtomik/aola/reskin` lúc chạy, không chép vào Assets |
| `BanThuGame.cs` | màn dọc, menu, HUD, kéo khối, đổi ngọc, lượt, chiêu, kết trận, máy tự chơi |
| `Editor/BanThuSetup.cs` | tạo scene, đổi màn dọc, các mục menu PokiWar |

**Ghi số:**
- Mỗi trận ghi một dòng vào `PokiWar/BanThu/tran.csv`: bàn, kết quả, số lượt, giây, máu còn.
- Cột `may_tu_choi` = 1 là máy chơi. Người chơi thật ra số 0.
- Ảnh tự chụp nằm cạnh file đó (F9 chụp tay).

**Máy tự chơi:**
- Gọi bằng menu PokiWar → Tự chơi A / A có sập / C, khi đang Play.
- Mỗi lần chạy 3 trận, nhanh gấp 4.
- Máy đặt khối ưu tiên xoá đường; ở bàn ngọc thì đổi chỗ ngẫu nhiên trong các nước ghép được.

**Số đã chỉnh sau khi máy chơi** (bản đầu: bàn C thắng sau 8–19 lượt không mất máu, khiên cộng tới 207):
- Địch đánh 55 (trước là 35).
- Khiên tối đa 40.
- Mỗi ô ở bàn C chỉ tính 0,4; ở bàn A có sập tính 0,75.

Kết quả 9 trận máy chơi sau khi chỉnh, đều thắng:

| Bàn | Số lượt | Máu còn |
|---|---|---|
| A | 21–34 | 52–368 |
| A sập | 27–38 | 115–296 |
| C | 18–32 | 291–340 |

Máy chơi kém hơn người nhiều, nên các số này chỉ để ba bàn có độ dài trận gần nhau. Cân thật phải dựa vào số người chơi.

**Chưa làm:**
- Hiệu ứng hoà màu của Aola (cộng sáng, đổi màu, glow) chưa dựng; hình vẫn vẽ kiểu thường.
- Chưa có thu phục, chưa có âm thanh, chưa có hiệu ứng nổ ô (chỉ nháy trắng).
- Không có mặt sau; tướng mình dùng mặt trước.

## MCP

Phiên Claude mở từ thư mục aola không tự thấy MCP của Unity. Server của gói chạy ở `http://127.0.0.1:8090/mcp`; lần này Claude gọi nó trực tiếp qua HTTP để biên dịch, Play, chạy menu và chụp màn hình. Mở phiên Claude mới ngay trong thư mục PokiWar thì công cụ MCP hiện sẵn.

## Các bước làm

1. Đổi project sang màn dọc ([02_ManHinhDoc.md](02_ManHinhDoc.md)), dựng scene trận với sân và chỗ đặt bàn.
2. Bộ đọc `anim.json`, chạy 4 clip của võ sư và đại sư cà sa (một làm tướng, một làm địch).
3. Phần chung: tướng, địch, lượt, sát thương, nộ, chiêu, thắng thua. Thuần C#, có test.
4. Bàn A: chép logic bàn và kéo khối từ 2PlayersGame, viết bộ chọn khối mới theo màu, thêm công tắc sập.
5. Bàn C: bàn ngọc 7 × 7, đổi chỗ, ghép, rơi, dây chuyền, xáo khi hết nước.
6. Màn chọn bản (A, A sập, C), ghi số lượt và thời gian mỗi trận.
