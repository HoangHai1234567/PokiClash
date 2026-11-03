# Chọn tướng khởi đầu: 5 hệ, công bằng với mọi lựa chọn

Viết 2026-11-03. Người dùng muốn: khi vào game, người chơi chọn 1 trong 5 tướng khởi đầu (mỗi hệ một con), sức ngang nhau, và chọn con nào cũng chơi công bằng.

**Người dùng chốt (2026-11-03):**
- 5 tướng ở mục 2.1, và mỗi con là **tướng mở đầu (ải 1) của đảo cùng hệ**:
  - Kim và Mộc đã đúng (Bu Lông, Nụ Hoa);
  - ải 1 đảo Hỏa đổi từ Bồ Đề sang Sư Tử Lửa;
  - ải 1 đảo Thổ đổi từ Võ Sư sang Thạch Nhân.
- Phần còn lại làm theo đề xuất của kế hoạch.
- **Chốt thêm cùng ngày: ô đội mở theo cấp người chơi**: ô 2 ở cấp 10, ô 3 ở cấp 30 (thay luật B "ô 2 ở ải 3" bên dưới, và thay luật cũ "theo số đảo đã xong"). Xem mục 6.

Hệ quả:
- **Ải 1 mỗi đảo:** nếu tướng đứng đó là tướng người chơi đã chọn thì đấu với bóng của nó; nếu không thì đấu tướng thật và thu phục được.
  - Ải 1 rơi mảnh của tướng đứng đó (ải tướng: chắc chắn 2–4 mảnh lần đầu), kể cả khi là bóng: khi đó là mảnh của chính tướng mình.
- Mục 2.4 cũ (rương mốc) bỏ: 4 tướng không chọn thu phục ở ải 1 đảo cùng hệ.

## 1. Hiện trạng và những chỗ gây lệch

- **Sức tướng chỉ phụ thuộc độ hiếm, cấp, sao** (`Core/HeroStats.cs`). Hệ số theo độ hiếm: Thường 1, Khá 1,1, Hiếm 1,22, Sử thi 1,36, Huyền thoại 1,5.
  - 6 chỉ số gốc chỉ quyết định cách chia sức cho Máu, Công, Thủ (căn bậc hai so với trung bình của chính tướng). Tốc gốc thì cộng thẳng.
  - Vì vậy "ngang sức" nghĩa là cùng độ hiếm và cùng ngân sách thẻ. Tổng 6 số không quan trọng.
  - Tốc hiện không dùng trong trận: bên người chơi luôn đi trước (`Battle.cs`, `first = 0`). Khi đo phát hiện ra điều này nên bỏ tiêu chí Tốc.
- **Khắc hệ rất mạnh:** đánh hệ mình khắc ×1,5, đánh hệ khắc mình ×0,75 (`Elements.Mult`). Trận 1 chọi 1, có đổi tướng.
  - Cùng chỉ số, tướng khắc hệ đối thủ trao đổi sát thương gấp 2 lần tướng trung tính, gấp 4 lần tướng bị khắc.
- **Thứ tự đảo:** Thủy (cấp 1–8, 70 ải) → Hỏa → Kim → Mộc → Thổ.
- **Ô đội:** 1 ô suốt đảo Thủy. Ô 2 mở khi xong 1 đảo, ô 3 khi xong 3 đảo (`Progress.TeamSlotZones`).
- **Tướng khởi đầu bị bỏ ra ngoài ngay từ bây giờ.**
  - Quà ải 3 là Võ Sư (Thổ, khắc Thủy).
  - Số đo ở `14_HeThongAi.md`: trên đảo Thủy, Võ Sư thắng mini boss 72%, còn Giọt Sương chỉ 20%.
  - Đội chỉ có 1 ô, nên từ ải 3 tới hết đảo người chơi sẽ cất Giọt Sương và dùng Võ Sư. Khi có 5 lựa chọn, chọn con nào thì cuối cùng cũng chơi bằng Võ Sư.
- **Mỗi hệ có một đảo dễ và một đảo khó:**

  | Chọn hệ | Mạnh ở đảo | Yếu ở đảo |
  |---|---|---|
  | Thổ | Thủy (đảo 1) | Mộc (đảo 4) |
  | Thủy | Hỏa (đảo 2) | Thổ (đảo 5) |
  | Hỏa | Kim (đảo 3) | **Thủy (đảo 1)** |
  | Kim | Mộc (đảo 4) | Hỏa (đảo 2) |
  | Mộc | Thổ (đảo 5) | Kim (đảo 3) |

- **5 tướng ứng viên đang lệch nhau:**
  - Sư Tử Lửa có tuyệt kỹ Sử thi và nội tại Hiếm. Giọt Sương chỉ có chiêu Thường, tuyệt kỹ Khá, nội tại Thường.
  - Thạch Nhân đang dùng y hệt 3 thẻ của Võ Sư.
  - Tốc gốc chênh xa: Bu Lông 10, Thạch Nhân 25, Nụ Hoa 30, Giọt Sương 50, Sư Tử Lửa 55.
- **Công cụ đo đang lạc quan ở đảo Thủy:** `ProgressSim.BestTeam` lấy 3 tướng mạnh nhất mà không xét số ô đã mở. Máy chơi đảo Thủy bằng 3 tướng, trong khi người chơi thật chỉ có 1.

## 2. Thiết kế

### 2.1 Năm tướng khởi đầu

Mỗi tướng là một dòng 3 dạng như Giọt Sương. Hình aola của cả 15 dạng đã có trong project (`Assets/03 Art/Heroes/Resources`), nên chơi thử được ngay trong lúc chờ hình mới.

| Hệ | Tướng | Dòng aola | Độ hiếm: hiện tại → mới | Vai đề xuất |
|---|---|---|---|---|
| Kim | Bu Lông | 76 → 77 → 78 | Thường → **Khá** | khiên, choáng |
| Mộc | Nụ Hoa | 22 → 23 → 24 | Thường → **Khá** | hồi nộ, tuyệt kỹ sớm |
| Thủy | Giọt Sương | 7 → 8 → 9 | Khá (giữ) | hồi máu, giảm công địch |
| Hỏa | Sư Tử Lửa | 4 → 5 → 6 (dòng khởi đầu hệ Lửa của aola) | Khá (giữ) | đốt |
| Thổ | Thạch Nhân | 34 → 35 → 36 | Hiếm → **Khá** | thủ, phản đòn |

Ngân sách chung cho cả 5:
- độ hiếm Khá, 15 mảnh;
- thẻ: chiêu Thường, tuyệt kỹ Khá, nội tại Thường (giống Giọt Sương):
  - Sư Tử Lửa hạ tuyệt kỹ và nội tại;
  - Thạch Nhân làm 3 thẻ mới, không trùng Võ Sư;
  - Bu Lông và Nụ Hoa giữ khung thẻ, chỉnh số;
- Tốc gốc trong khoảng 45–55;
- Máu, Công, Thủ chia khác nhau theo vai, rồi chỉnh bằng bảng vòng tròn (mục 3).

### 2.2 Bốn luật cho đảo đầu

**A. Ải 1 đảo Thủy là Giọt Sương, yếu đi 20%** (theo chốt của người dùng ở đầu file).
- Người chọn Giọt Sương đấu với bóng của nó, như hiện nay.
- Người chọn tướng khác đấu với Giọt Sương thật và thu phục được.
- Sư Tử Lửa đấu Giọt Sương thì bị khắc, nên cần luật D để trận đầu không bất lợi.

**B. ~~Mở ô đội 2 ở ải 3~~** (bỏ: người dùng chốt ô đội mở theo cấp, ô 2 ở cấp 10, ô 3 ở cấp 30; mục 6), cùng lúc nhận quà, thay vì đợi xong đảo Thủy.
- Tướng đã chọn luôn ra trận. Gặp địch bất lợi thì đổi sang tướng kia.
- Luật này trả lời câu hỏi mở 17 trong `12_KeHoach_OpenSpec.md`.

**C. Quà ải 3 theo lựa chọn:**
- chọn Thạch Nhân (Thổ) thì nhận ~~Pháo Hộp (Kim, Thường)~~ **Mèo Quyền Sắt (Kim, Khá, trung tính với Thủy)**;
- chọn hệ khác thì nhận Võ Sư như cũ; **Võ Sư lên Khá** (15 mảnh, quà 15 mảnh).
- Đổi sau khi đo: Võ Sư Thường thì người chọn Thạch Nhân có tướng khắc mạnh hơn 10%, dễ hơn hẳn ở ải khó (mini boss 74% so với 45–58%). Cả hai tướng của mọi đội đều Khá thì chênh còn ≤ 12 điểm.

Quà ải 25 hiện là Nụ Hoa. Nụ Hoa thành tướng khởi đầu nên quà này đổi sang Mầm Gỗ (Mộc, Thường).

**D. Tướng đồng hành không bị khắc hệ** (cần chốt).
- Áp cho tướng đã chọn:
  - đánh hệ khắc mình vẫn gây ×1;
  - bị hệ khắc mình đánh cũng chỉ nhận ×1;
  - vẫn được ×1,5 khi mình khắc đối thủ.
- Chỉ tướng đã chọn có luật này. Màn Tướng và trận hiện huy hiệu "Đồng hành".
- Vì sao cần: không có luật D thì mỗi lựa chọn có một đảo mà tướng đồng hành gần như vô dụng, trong đó có Sư Tử Lửa ở đảo Thủy (đảo đầu, 70 ải).
- Phương án thay nếu không muốn thêm luật: màn chọn ghi độ khó đảo đầu (Thạch Nhân: Dễ, Sư Tử Lửa: Khó) và chấp nhận lệch, giống cách thể loại này hay làm.

Đội trên đảo Thủy sau 4 luật:

| Chọn | Tướng khắc đảo Thủy | Tướng trung tính |
|---|---|---|
| Thạch Nhân | Thạch Nhân (Khá) | Mèo Quyền Sắt (Khá, quà ải 3) |
| 4 tướng còn lại | Võ Sư (Khá, quà ải 3) | tướng đã chọn (Khá; Sư Tử Lửa trung tính nhờ luật D) |

Mọi lựa chọn đều có 1 tướng khắc và 1 tướng trung tính, cùng tổng độ hiếm.

Riêng người chọn Thạch Nhân có tướng khắc là Khá (mạnh hơn 10%), nên có thể vẫn hơi dễ hơn. Mục 3 sẽ đo. Nếu chênh quá ngưỡng thì chỉnh quà, ví dụ cho Võ Sư vào sẵn sao 2 với 4 lựa chọn kia.

### 2.3 Các đảo sau

- Mỗi lựa chọn có đúng một đảo lợi thế: Thổ ở đảo 1, Thủy ở đảo 2, Hỏa ở đảo 3, Kim ở đảo 4, Mộc ở đảo 5.
- Nhờ luật D, không lựa chọn nào có đảo bị thiệt.
- Thạch Nhân có lợi thế sớm nhất. Đo tiến độ (mục 3) để chắc chắn nó không nhanh quá ngưỡng.

### 2.4 Bốn tướng không được chọn

Người dùng chốt: thu phục ở ải 1 của đảo cùng hệ (đánh lại ải 1 để gom đủ 15 mảnh). Ví dụ: chọn Sư Tử Lửa thì gặp Giọt Sương thật ở ải 1 đảo Thủy.

### 2.5 Màn chọn tướng

- Sau màn giới thiệu (`IntroDialog`, nút "Bắt đầu!"), mở hộp "Chọn bạn đồng hành". Hộp bắt buộc, không đóng được.
- 5 thẻ tướng, mỗi thẻ có:
  - hình động, tên, hệ;
  - vai, một dòng;
  - "Khắc: … · Bị khắc: …";
  - 3 thẻ chiêu, mô tả lấy từ `CardText`.
- Chạm thẻ để xem lớn. Nút "Chọn" hỏi lại một lần, rồi nhận tướng, đội là [tướng đó], vào sảnh.
- Không đổi lại được. Sổ tay bản dev có nút "Chọn lại tướng khởi đầu" để thử.
- Bản lưu cũ đã có Giọt Sương thì coi như đã chọn Giọt Sương, không hiện màn chọn.

## 3. Đo và tiêu chí đạt

Thêm menu `PokiClash/Cân bằng nhanh/Tướng khởi đầu (ghi CSV vào Logs)`. Trước khi đo, sửa `ProgressSim.BestTeam`: lấy đúng số ô đã mở (`Progress.TeamSlots`), ưu tiên tướng khắc hệ đảo đang đánh.

| Bảng | Cách đo | Đạt khi |
|---|---|---|
| Vòng tròn | 5 tướng đấu nhau từng cặp, cùng cấp, sao, cấp thẻ; ở cấp 1, 4, 8; 200 trận mỗi cặp, đổi bên đi trước | Tỉ lệ thắng trung bình của mỗi tướng 50% ± 5. Mỗi cặp trung tính (không khắc nhau) 40–60% |
| Đảo Thủy | 70 ải × 5 lựa chọn. Đội theo luật mục 2.2, tính theo những gì người chơi có ở ải đó. Cấp bằng cấp địch, sao theo cấp như `14_HeThongAi.md`, 100 trận mỗi ải | Ở mỗi kiểu ải, 5 lựa chọn chênh nhau tối đa 10 điểm %, và cách cột Võ Sư của `14_HeThongAi.md` (độ khó đảo đang thiết kế) không quá 10 điểm |
| Tiến độ | ProgressSim 30 ngày × 3 kiểu người chơi × 5 lựa chọn | Kiểu "vừa": ngày xong đảo Thủy chênh tối đa 1 ngày, số ải qua ở ngày 30 chênh tối đa 10% |
| Đảo bị khắc | 8 ải mỗi đảo Hỏa, Kim, Mộc, Thổ, đội 2 ô | Ở đảo của hệ khắc mình, tướng đồng hành không kém một tướng Khá trung tính quá 5 điểm % |

Núm chỉnh, theo thứ tự:
1. chỉ số và thẻ của 5 tướng (bảng vòng tròn);
2. quà ải 3;
3. sức địch đảo Thủy, vì từ ải 3 người chơi đã có 2 tướng:
   - trước hết bỏ phần "−20% mỗi con" của nhóm 3 con (lý do cũ là người chơi chỉ có 1 tướng);
   - rồi chỉnh % cường hóa từng kiểu ải;
4. cấp địch.

## 4. Các bước làm

**Bước 0. Đo hiện trạng** (không đổi gameplay)
- Viết menu đo, sửa `BestTeam`.
- Chạy cả 4 bảng với luật hiện tại (1 ô, quà Võ Sư) và 5 tướng như dữ liệu hiện tại. Kết quả là số gốc để so.

**Bước 1. Dữ liệu 5 tướng**
- `heroes.json`: `starters` gồm 5 id; độ hiếm, chỉ số, mảnh.
- `cards.json`: 15 thẻ theo ngân sách ở mục 2.1.
- Chạy menu `PokiClash/Nhập dữ liệu`, chỉnh cho tới khi bảng vòng tròn đạt.

**Bước 2. Luật đảo đầu**
- `Core/SaveData.cs`:
  - thêm trường `starter`;
  - `New` không cho tướng nào;
  - `FillMissingHeroes` chỉ coi `starter` là đã có. Hiện code dùng `Starters.Contains`: để nguyên thì người chơi mới có luôn cả 5 tướng.
- `Core/Progress.cs`:
  - thêm `ChooseStarter`;
  - `TeamSlots` mở ô 2 ở ải 3 đảo Thủy;
  - `WinStage` trao quà theo tướng đã chọn.
- `Core/Types.cs`, `GameData.cs`, `stages.json`:
  - quà có bản thay theo tướng đã chọn, ví dụ `"alt": {"thach_nhan": "phao_hop"}`;
  - quà ải 25 thành `mam_go`.
- `Core/Battle/Teams.cs`: ải bóng lấy tướng đã chọn; thêm `Member.partner`.
- Luật D: viết một hàm khắc hệ chung có tính luật D. Hiện có 5 chỗ gọi `Elements.Mult` riêng:
  - `Battle.cs` (sát thương và máy chọn tướng thay);
  - `BattleAi.cs`;
  - `SwapCard.cs`;
  - `TeamPickerDialog.cs`.
- `StagePrepDialog.cs`, `ZoneScene.cs`:
  - dòng "Mặt nước in bóng …" và tướng đứng trên bệ ải 1 lấy theo tướng đã chọn;
  - ô 2 ghi điều kiện mở mới.
- `stages.json` đảo Thủy: chỉnh sức địch tới khi bảng đảo Thủy đạt. Cập nhật golden `islands.json` và `14_HeThongAi.md`.

**Bước 3. Màn chọn và bản lưu**
- Hộp `Dialogs/ChonTuong`:
  - là biến thể của `HopThoai`, ô tướng là prefab trong `Items/`;
  - mở sau `IntroDialog`, và mở mỗi khi bản lưu chưa có `starter`.
- Bản lưu lên v5. Bước chuyển v4 → v5 gán `starter` là Giọt Sương nếu đã có, không thì là tướng đầu tiên đã có.
- Sổ tay:
  - "Xoá dữ liệu" đưa về màn chọn, sửa câu "chỉ có Giọt Sương";
  - bản dev thêm nút "Chọn lại tướng khởi đầu".

**Bước 4. Test và vòng thử**
- Test:
  - bản lưu mới có 0 tướng; chọn xong có đúng 1, đội là [tướng đó], ở dạng 1 (`RosterTests`);
  - chuyển v4 → v5 (`SaveTests`);
  - ải 1 là bóng đúng tướng, kiểm cả 5 lựa chọn (`IslandTests`);
  - quà theo lựa chọn; ô 2 mở ở ải 3;
  - luật D. `BattleGoldenTests` giữ nguyên vì trận không có tướng đồng hành thì không đổi;
  - thử nhanh cân bằng: vòng tròn ít trận, hạt giống cố định, kiểm độ chênh.
- Golden:
  - Bu Lông là địch ở ải 1, 3, 5 đảo Kim; Nụ Hoa ở ải 1, 3, 5, 7 đảo Mộc;
  - lên Khá thì hai con này mạnh thêm 10% ở đó, nên phải sửa golden liên quan và xem lại độ khó các ải đó.
- Vòng thử:
  - thêm `PokiClash/Thử/Chọn tướng khởi đầu`: chụp màn chọn, rồi với từng tướng chụp hộp chuẩn bị ải 1 và trận ải 1;
  - sửa `PlayTour`, `PopupTour` (đang mở khoá cứng Giọt Sương).
- Chạy hết test EditMode.

**Bước 5. Hình** (làm song song từ bước 1)
- Trong lúc chờ, dùng hình aola đã có (`goc_4`–`6`, `goc_22`–`24`, `goc_34`–`36`, `goc_76`–`78`).
- 4 dòng × 3 dạng = 12 dạng, theo `ArtGen/Heroes/QUY_TRINH.md`, gói prompt sinh bằng `ArtGen/Heroes/build.py`. Giọt Sương đang làm dạng 2.
- Đủ dạng thì đổi animation cho khác aola, như kế hoạch của Giọt Sương.

**Bước 6. Thử trên điện thoại**
- Bản Build thường.
- Chơi 10 ải đầu với từng tướng (dùng nút "Chọn lại" của bản dev).

Thứ tự làm: bước 0, chốt các câu ở mục 5, rồi bước 1 → 2 → 3 → 4 → 6. Bước 5 chạy song song.

## 5. Câu đã chốt

Người dùng chốt 2026-11-03: dùng 5 tướng ở mục 2.1 và đặt mỗi con ở ải 1 đảo cùng hệ; các câu còn lại làm theo đề xuất (ô 2 ở ải 3, luật D, quà theo lựa chọn, quà ải 25 là Mầm Gỗ). Quà của người chọn Thạch Nhân đổi sang Mèo Quyền Sắt và Võ Sư lên Khá sau khi đo (mục 2.2 C).

## 6. Đã làm (2026-11-03)

### Dữ liệu chốt

| Tướng | Chỉ số gốc (công, thủ, công phép, thủ phép, máu, tốc) | Chiêu (Thường) | Tuyệt kỹ (Khá) | Nội tại (Thường) |
|---|---|---|---|---|
| Giọt Sương | 50, 50, 50, 50, 50, 50 | 90% Công, địch −15% Công 1 lượt (25 mana) | 200% Công, hồi 15% máu (35 mana) | đầu lượt hồi 5% máu |
| Sư Tử Lửa | 55, 50, 45, 50, 50, 55 | 90% Công, đốt 3 lượt 6% (30 mana) | 220% Công, đốt 3 lượt 7% (35 mana) | đòn thường 35% đốt 2 lượt 5% |
| Bu Lông | 55, 60, 75, 40, 75, 10 | 100% Công, 15% choáng (30 mana) | 200% Công, địch −20% Thủ 2 lượt (40 mana) | vào trận khiên 6% máu |
| Nụ Hoa | 40, 45, 50, 40, 45, 30 | hồi 7% máu 3 lượt, 70% Công (25 mana) | 230% Công, địch −20% Thủ 2 lượt (35 mana) | đầu lượt +10 nộ |
| Thạch Nhân | 70, 95, 40, 85, 95, 25 | Ném Đá: 100% Công, khiên 10% (30 mana) | Núi Lở: 220% Công, địch −20% Công 2 lượt (40 mana) | Da Đá: giảm 8% sát thương cả trận |

- Cả 5 và Võ Sư: Khá, 15 mảnh. Bu Lông, Nụ Hoa, Thạch Nhân đổi độ hiếm nên mạnh hơn hoặc yếu hơn 10% khi là địch ở đảo Kim, Mộc, Thổ (8 ải cũ, chưa quy độ hiếm).
- **Ô đội theo cấp** (`Progress.SlotLevels` = 1, 10, 30). Tướng tặng tự vào đội nếu còn ô trống.
- Đảo Thủy từ ải 4: cộng thêm cường hóa theo kiểu ải (Bầy lính, Cường hóa, Tướng và lính, Lính tinh nhuệ, Hai tướng, Cửa ải +0,15; mini boss +0,10; boss +0,05; Tướng mới giữ nguyên). Lý do: Võ Sư lên Khá nên đội 1 tướng mạnh hơn thiết kế cũ; dò bằng máy tự chơi cho bằng cột Võ Sư cũ.
  - Bản trước (ô 2 ở ải 3, đội 2 tướng) cộng +0,25 tới +0,50; đã bỏ khi đổi sang ô theo cấp.
- Ải 1 mỗi đảo: tướng khởi đầu cùng hệ, chắc chắn rơi 2–4 mảnh lần đầu (đánh lại 50%).

### Số đo cuối (máy tự chơi; công cụ ở `Editor/StarterBalanceMenu.cs`)

Vòng tròn, tỉ lệ thắng trung bình mỗi tướng (400 trận mỗi cặp): cấp 1: 45–55%; cấp 4: 47–51%; cấp 8: 45–55%. Cặp trung tính 43–55%. **Đạt.**

**Đảo Thủy, ô đội theo cấp (bản chốt).** Đánh đúng cấp địch (1–8) thì chưa tới cấp 10, cả đảo chỉ 1 ô. Đội tốt nhất của mọi lựa chọn là một tướng khắc đảo Khá: Võ Sư (quà ải 3), riêng người chọn Thạch Nhân dùng Thạch Nhân. 200 trận mỗi ải:

| Kiểu ải | Mục tiêu | Giọt Sương, Sư Tử Lửa, Bu Lông, Nụ Hoa (Võ Sư ra trận) | Thạch Nhân |
|---|---|---|---|
| Tướng mới | 100% | 99–100% | 100% |
| Bầy lính | 91% | 88–89% | 94% |
| Cường hóa | 92% | 89% | 81% |
| Tướng và lính | 78% | 73% | 84% |
| Lính tinh nhuệ | 78% | 73% | 80% |
| Mini boss | 72% | 67% | 57% |
| Hai tướng | 69% | 62% | 61% |
| Cửa ải | 62% | 62% | 58% |
| Boss ải 70 | 61% | 65% | 68% |
| **Cả đảo** | 81% | 78% | 79% |

Cả đảo chênh 1 điểm. Đổi lại, trước cấp 10, người chọn Giọt Sương, Sư Tử Lửa, Bu Lông, Nụ Hoa đánh giỏi nhất bằng Võ Sư. Nếu chỉ dùng tướng mình chọn (có luật đồng hành):

| Cấp so với địch | Giọt Sương | Sư Tử Lửa | Bu Lông | Nụ Hoa | Thạch Nhân | Võ Sư |
|---|---|---|---|---|---|---|
| bằng | 25% | 21% | 27% | 23% | 80% | 79% |
| +2 | 60% | 54% | 60% | 57% | 95% | 94% |
| +4 | 81% | 74% | 79% | 78% | 98% | 97% |

Theo mô phỏng tiến độ, người chơi thật thường cao hơn địch đảo Thủy 3–7 cấp (Chăm ngày 1: cấp 7 ở ải 29, địch cấp 3; Vừa ngày 2: cấp 10 ở ải 18), nên vẫn dùng được tướng mình chọn. Cấp 10 (ô 2) tới vào khoảng ải 45 với Chăm (ngày 2), ải 18 với Vừa (ngày 2), ải 12 với Ít (ngày 6).

Bản trước (ô 2 ở ải 3, đã bỏ), 200 trận mỗi ải:

| Kiểu ải | Mục tiêu (cột Võ Sư cũ) | Giọt Sương | Sư Tử Lửa | Bu Lông | Nụ Hoa | Thạch Nhân | Chênh |
|---|---|---|---|---|---|---|---|
| Tướng mới | 100% | 98% | 98% | 99% | 98% | 98% | 1 |
| Bầy lính | 91% | 92% | 91% | 93% | 90% | 95% | 5 |
| Cường hóa | 92% | 90% | 91% | 92% | 89% | 92% | 3 |
| Tướng và lính | 78% | 75% | 73% | 78% | 72% | 77% | 6 |
| Lính tinh nhuệ | 78% | 75% | 74% | 79% | 73% | 78% | 6 |
| Mini boss | 72% | 62% | 66% | 71% | 63% | 74% | 11 |
| Hai tướng | 69% | 69% | 69% | 75% | 69% | 75% | 7 |
| Cửa ải | 62% | 59% | 60% | 65% | 58% | 60% | 8 |
| Boss ải 70 | 61% | 62% | 62% | 68% | 59% | 70% | 12 |
| **Cả đảo** | 81% | 79% | 79% | 83% | 78% | 82% | 5 |

(Bản ô 2 ở ải 3: chênh tối đa 10 điểm ở 7/9 kiểu ải, mini boss 11 và boss 12; cả đảo chênh 5 điểm.)

Đảo bị khắc (tướng khởi đầu đánh một mình 8 ải, không / có luật D): Bu Lông ở đảo Hỏa 21% → 47% (tướng trung tính 40–46%); Nụ Hoa ở đảo Kim 18% → 45% (47–50%); Thạch Nhân ở đảo Mộc 25% → 47% (42–47%); Giọt Sương ở đảo Thổ 13% → 28% (24–31%). **Đạt.**

Tiến độ 30 ngày: cả 5 lựa chọn ra **giống hệt nhau** ở cả 3 kiểu người chơi (Vừa: xong Thủy ngày 8, 63 ải ngày 7). Lý do: máy tự chơi gần như thắng mọi trận nhờ bi và EXP từ nguồn khác, nhịp bị giới hạn bởi số trận mỗi ngày. Riêng nhịp chung đang nhanh (Chăm xong mọi đảo ngày 3, cấp 30 ngày 7), là việc của câu hỏi mở 20, không do tướng khởi đầu.

### Code

- `Core`:
  - `SaveData.starter`, `ChooseStarter`; bản lưu v5, bước chuyển v4 → v5 (`MigrateStarterV4`);
  - `New(data, now)` cho test và máy tự chơi chọn sẵn Giọt Sương; game tạo bản lưu chưa chọn (`New(data, now, null)`);
  - `Progress.TeamSlots`, `SlotNeed`, `SlotLevels` (ô đội theo cấp 1, 10, 30); `WinStage` cho tướng tặng vào ô trống;
  - `StageDrop.altFor/altHero/HeroFor` (quà thay);
  - `Elements.Mult(att, def, attPartner, defPartner)`, `Battle.ElemMult`, `Member.partner`, `Fighter.partner` (luật D);
  - `GameData.Validate` kiểm mỗi hệ một tướng khởi đầu ở ải 1;
  - `Sim.StarterTeam/StarterIsland/Duel/StarAt`;
  - `ProgressSim.BestTeam` theo số ô đã mở và hệ của ải.
- `App`:
  - `StarterDialog` (prefab `Dialogs/ChonTuongKhoiDau`, menu `PokiClash/Prefab/Hộp chọn tướng khởi đầu`);
  - sảnh mở hộp sau màn giới thiệu, hoặc mỗi khi bản lưu chưa có tướng khởi đầu;
  - chữ ô đội khoá, quà ải, dòng bóng ở ải 1.
- Editor:
  - menu đo `PokiClash/Cân bằng nhanh/Tướng khởi đầu: …`;
  - vòng thử `PokiClash/Thử/Chọn tướng khởi đầu: …`;
  - `PlayTour` người chơi mới có bước chọn tướng.
- Test: `StarterTests` mới. Golden tính lại bên Unity:
  - `islands`, `sim`, `cardtext`, `zones`, `battles`, `battle_events`, `progression`, `roster`, `badges`, `farm`;
  - mọi chỗ đổi đều do tướng khởi đầu, Võ Sư hoặc sức địch đảo Thủy.

### Chưa làm

- Sổ tay bản dev chưa có nút "Chọn lại tướng khởi đầu": nút bảng thử được nướng sẵn trong prefab Sổ tay. Muốn thử tướng khác thì dùng "Xoá dữ liệu".
- Huy hiệu "Đồng hành" trên màn Tướng và trận: chưa có, mới ghi trong hộp chọn tướng.
- Hình mới cho Bu Lông, Nụ Hoa, Sư Tử Lửa, Thạch Nhân (12 dạng): đang dùng hình aola.
- Thử trên điện thoại.
