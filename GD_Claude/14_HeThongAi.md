# Hệ thống ải mới: 70 ải mỗi đảo, 10 tướng mỗi đảo

Viết 2026-11-02. Chủ dự án chốt hướng; bản thử chạy ở đảo Thủy trên web (`Web/`). Unity vẫn dùng 8 ải mỗi đảo cho tới khi chép sang.

## Vì sao

Mỗi đảo một tướng mới thì không đủ nội dung cho người chơi cày. Hướng mới: mỗi đảo dài 70 ải và có 10 tướng. Các ải xen giữa dùng lại tướng đã gặp, ở dạng mạnh hơn hoặc theo nhóm, cùng một loại quái mới là **lính**.

## Luật

- **Ải tướng** (ra mắt tướng mới): 1, 5, 10, 15, 20, rồi cứ 10 ải một tướng: 30, 40, 50, 60, 70.
  - Ải 1: người chơi đánh với **bóng của chính tướng khởi đầu** (Giọt Sương, yếu đi 20%).
    - Từ 2026-11-03 (`15_TuongKhoiDau.md`): ải 1 luôn là Giọt Sương; người chọn tướng khởi đầu khác đấu với Giọt Sương thật và thu phục được (rơi 2–4 mảnh).
  - Ải 5, 10, 15: tướng mới, cường hóa +15%.
  - Ải 20–60: tướng mới là mini boss.
  - Ải 70: boss đảo, tiến hóa trong trận (thẻ Tiến Hóa như boss ải 8 cũ).
  - **Tiến hóa trong trận ở ải 5–60** (người dùng dặn 2026-11-04): tướng mới của ải tướng cũng tiến hóa hết dòng như boss ải 70 (cờ `evo` trong `stages.json`):
    - vào trận ở dạng 1;
    - máu cả dòng cộng lại bằng 1,5 lần, chia cho các dạng theo tỉ lệ 1 : 2 (: 3);
    - Công các dạng trước kém 10% mỗi dạng;
    - máu dưới 25% thì lên dạng sau và hồi đầy máu.
    - Mini boss tiến hóa lấy máu ×0,7 như boss ải 70, thay cho ×0,95.
    - Ải 1 (bóng tướng khởi đầu) không tiến hóa.
    - Đòn kết liễu (đánh hoặc bỏng) giáng vào tướng còn dạng sau, kể cả khi nó đang trên 25% máu: chừa 1 máu rồi tiến hóa ngay, không gục (người dùng dặn 2026-11-04).
  - Hộp Chuẩn bị trận (người dùng dặn 2026-11-04):
    - hiện to Máu, Công, Thủ khi vào trận của từng địch, kèm lực chiến;
    - không so với tướng người chơi, vì dễ hiểu lầm;
    - tướng tiến hóa chỉ hiện dạng đầu; đầu mục ghi "còn 25% máu thì tiến hóa, hồi đầy máu"; lực chiến tính cả dòng.
- **Chặng**: từ một ải tướng tới trước ải tướng sau. Tên chặng là tên địa danh, ví dụ ải 23 là "Ngọn Hải Đăng 4".
- **Ải xen giữa** trộn 3 kiểu:
  - tướng đã gặp được **cường hóa** (+% Máu và Công, Thủ cộng một nửa);
  - **nhóm 2–3 con** (tướng và lính, hai tướng, bầy lính);
  - **lính**: quái không thu thập được, chỉ để gây khó.

### Mẫu ải xen giữa

H là tướng của chặng này, P là tướng chặng trước, Q là tướng hai chặng trước. M và N là hai loại lính khác nhau, xoay vòng theo số ải. Tướng khởi đầu của người chơi chỉ xuất hiện ở ải 1.

| Vị trí trong chặng | Chặng ngắn (5 ải: 5–9, 10–14, 15–19) | Chặng dài (10 ải: 20–29 … 60–69) |
|---|---|---|
| +1 | Bầy lính: M, N | Bầy lính: M, N |
| +2 | Cường hóa: H +12% | Cường hóa: H +12% |
| +3 | Tướng và lính: P, M | Tướng và lính: P, M |
| +4 | **Cửa ải**: H +15%, M | Bầy lính: M, N, M (mỗi con −20%) |
| +5 | | Hai tướng: H, Q |
| +6 | | Cường hóa: H +25% |
| +7 | | Lính tinh nhuệ: N +40%, M |
| +8 | | Tướng và lính: H, M, N (mỗi con −20%) |
| +9 | | **Cửa ải**: H +10%, P +10% |

Chặng đầu (ải 2–4) chỉ có lính, để tập: 1 cua; 2 cua (mỗi con −25%); 1 cua +25%.

Nhóm 3 con bị yếu đi 20% mỗi con: người chơi chỉ mang 1 tướng suốt đảo đầu (ô đội 2 mở khi xong đảo), phải đánh lần lượt cả 3 con.

**Đổi 2026-11-03 (Unity, `15_TuongKhoiDau.md`):**
- Ô đội mở theo cấp người chơi: ô 2 ở cấp 10, ô 3 ở cấp 30. Đánh đúng cấp đảo Thủy (1–8) thì vẫn chỉ 1 tướng.
- Võ Sư lên Khá, nên từ ải 4 mọi địch đảo Thủy được cộng thêm cường hóa: +0,15 cho Bầy lính, Cường hóa, Tướng và lính, Lính tinh nhuệ, Hai tướng, Cửa ải; mini boss +0,10; boss +0,05; Tướng mới giữ nguyên. Nhờ vậy Võ Sư một mình vẫn có tỉ lệ thắng như bảng số đo dưới.

## Đảo Thủy

### 10 tướng

7 tướng chính là 7 hình aola người dùng gửi cho đảo Thủy (theo session hình aola): Mi Nhi, Ma Kết, Vây Lam, Kuba, Thương Lam, Huyền Vũ, và Vạn Quân (dạng 2 của Lam Quân, người dùng gắn nhãn BOSS). Thêm Giọt Sương ở ải 1, và hai tướng Thường (Tiểu Y, Cánh Cụt) cho chặng đầu. Thứ tự xếp theo độ hiếm.

| Ải | Chặng | Tướng | Độ hiếm (tạm) | Loại ải |
|---|---|---|---|---|
| 1 | Bãi Vỏ Sò | Giọt Sương (bóng của tướng khởi đầu) | Khá | thường, −20% |
| 5 | Vũng San Hô | Tiểu Y | Thường | thường, +15% |
| 10 | Cầu Gỗ Rêu | Cánh Cụt | Thường | thường, +15% |
| 15 | Làng Vỏ Ốc | Mi Nhi | Khá | thường, +15% |
| 20 | Ngọn Hải Đăng | Ma Kết | Hiếm | mini boss |
| 30 | Thác Bạc | Vây Lam | Hiếm | mini boss |
| 40 | Rạn Ngọc Trai | Kuba | Sử thi | mini boss |
| 50 | Hồ Gương | Thương Lam | Sử thi | mini boss |
| 60 | Đền Rùa Cổ | Huyền Vũ | Huyền thoại | mini boss |
| 70 | Xoáy Nước Đinh Ba | Lam Quân → Vạn Quân → Hắc Dực | Sử thi | boss tiến hóa |

Không có suất trên đảo: Tám Tay, Cá Ngựa, Mập Răng Cưa (Thủy hiện có 13 tướng).

Tướng tặng: Võ Sư ở ải 3 (Thổ, khắc Thủy), Nụ Hoa ở ải 25. Từ 2026-11-03: Võ Sư lên Khá; người chọn Thạch Nhân nhận Mèo Quyền Sắt thay Võ Sư; quà ải 25 là Mầm Gỗ (Nụ Hoa thành tướng khởi đầu).

### Lính (6 loại, `Web/src/core/data/minions.ts`)

Mỗi loại có 2 bậc; từ ải 35, bậc 2 thay bậc 1. Cua có từ chặng đầu, cá nóc từ ải 10, song ngư từ ải 20. Hình là dạng aola gốc chưa có trong danh sách tướng (`reskin/goc_<id>`), chỉ dùng trong bản thử.

| Lính | Hình aola | Vai | Bị động |
|---|---|---|---|
| Cua Kìm, Cua Pháo | 1313 蟹小拳, 1314 炮炮蟹 | trâu | giảm 15% / 20% sát thương nhận |
| Cá Nóc, Cá Nóc Điện | 16 闪光河豚, 17 电击河豚 | phản đòn | bị đánh có 30% / 35% gây bỏng; Cá Nóc Điện có chiêu choáng 15% |
| Song Ngư Con, Song Ngư | 829 小双鱼, 830 双鱼灵 | nhanh | né 12% / 15%, chiêu đánh thêm một đòn |

Lính yếu hơn tướng cùng cấp: Máu ×0,85, Công ×0,9, Thủ ×0,9 (`MINION_POWER`).

### Cấp và sức địch

- **Cấp địch là cấp người chơi cần có; thang cấp 1–200** (người dùng dặn 2026-11-04, học Clash of Critters). Chi tiết và số đo: mục "Thang cấp 1–200" bên dưới.
  - **5 đảo chơi song song** (người dùng sửa 2026-11-05): đảo nào cũng từ cấp 1 lên gần cấp 200, boss cuối mỗi đảo 190–200. Chi tiết: mục "5 đảo song song" bên dưới.
  - Cách cũ (2026-11-04, hiểu sai): mỗi đảo một dải 40 cấp nối tiếp, Thủy 1–40, Hỏa 41–80, Kim 81–120, Mộc 121–160, Thổ 161–200.
  - Mọi địch trong một ải cùng cấp. Cấp không bao giờ giảm khi sang ải sau.
  - Các đảo 8 ải (tạm) đổi cấp từng địch tuyến tính từ khoảng cấp cũ sang khoảng mới.
  - Trước đây: ải 1 cấp 1, ải 10 cấp 2, ải 15–29 cấp 3, rồi mỗi 10 ải +1, tới ải 70 cấp 8; độ khó trong chặng chỉ nhờ % cường hóa.
- **"Lv" của địch là sức thật**: ở hệ thống mới, mọi tướng địch quy về sức của độ hiếm Khá, nên Huyền Vũ cấp 7 không mạnh hơn tướng Khá cấp 7. Tướng của người chơi vẫn mạnh theo độ hiếm. Không quy như vậy thì từ ải 20, tướng Hiếm, Sử thi, Huyền thoại cùng cấp thắng gần như mọi trận.
- Boss so với hệ thống cũ (máu ×1,8, công ×1,1): mini boss còn máu ×1,71, công ×1,05; boss tiến hóa máu ×0,7 so với boss cũ (`ENEMY_NORM` ở `islands.ts`).

### Thưởng

| Thưởng | Số |
|---|---|
| Bi mỗi ải | 1 bi (ải 1–35), 2 bi (ải 36–70); trước 2026-11-04 tính theo cấp địch |
| Bi thêm lần đầu qua | ải tướng +2, mini boss +4, boss +8 |
| Rương mốc | mỗi 10 ải (7 rương): 4, 5 … 9 bi và 1–2 thẻ; rương ải 70 có 15 bi, 4 thẻ |
| Mảnh: ải tướng | chắc chắn rơi mảnh tướng mới: thường 2–4, mini boss 3–5, boss 4–6 |
| Mảnh: ải xen giữa | mỗi tướng trong ải rơi 1–2 mảnh. Tỉ lệ theo độ hiếm: Thường 30%, Khá 25%, Hiếm 20%, Sử thi 15%, Huyền thoại 10%. Cửa ải ×1,5. Lính không rơi mảnh |

Đánh lại ải: mảnh rơi theo luật cũ (tỉ lệ ×0,8, ải chắc chắn rơi còn 50%).

## Số đo (máy tự chơi, `npm run sim -- island 100`)

Bảng dưới đo trên web với cấp địch cũ (1–8). Số đo với thang cấp mới nằm ở mục "Thang cấp 1–200".

Người chơi mang 1 tướng, cấp bằng cấp địch của ải. Sao theo kịp cấp (sao 2 từ cấp 2, sao 3 từ cấp 5), cấp thẻ bằng sao. Bảng là tỉ lệ thắng trung bình theo kiểu ải; người thật thường thắng nhiều hơn máy.

| Kiểu ải | Võ Sư (Thổ, khắc đảo) | Giọt Sương (Thủy, không khắc) |
|---|---|---|
| Ải tướng thường (1, 5, 10, 15) | 100% | 84% |
| Bầy lính | 91% | 63% |
| Cường hóa | 92% | 49% |
| Tướng và lính | 78% | 36% |
| Lính tinh nhuệ | 78% | 32% |
| Mini boss (20–60) | 72% | 20% |
| Hai tướng | 69% | 17% |
| Cửa ải | 62% | 16% |
| Boss ải 70 | 61% | 29% |

Trong một chặng, độ khó lên xuống kiểu răng cưa: đầu chặng dễ, cửa ải khó nhất, rồi tới tướng mới. Tướng không khắc hệ đảo thì cần hơn địch 1–2 cấp.

Tiến độ: qua lần đầu cả đảo được 137 bi từ ải và 54 bi từ rương, khoảng 1.760 EXP, đủ lên cấp 7. Chưa tính cây bi, trang trại, rương máy bi, đánh lại. Đánh lại một ải được 1–2 bi.

## Thang cấp 1–200 (Unity, 2026-11-04)

### Người dùng yêu cầu

- Người dùng chơi thử thấy Tiểu Y ở ải 5 và ải 8 đều Lv1.
- Họ muốn cấp địch là cấp người chơi cần có, như Clash of Critters: ở cấp 145 thì đang ở đảo 6. Game chia theo độ sâu cấp trong từng đảo, không chia theo đảo.
- Đảo đầu (Thủy) phải chơi 5–7 ngày; đảo sau lâu hơn, vì độ khó tăng dần.
- Cấp tối đa 200. Phải chơi liên tục ít nhất 1 tháng đến 45 ngày mới đạt.
- Tính lại toàn bộ chỉ số tướng theo cấp.

### Clash of Critters (theo trang tổng hợp chapter của cộng đồng)

- 120 chương, mỗi chương 80 ải, boss ở ải 10, 20 … 80.
- Cấp địch tăng đều khoảng 0,3–0,4 cấp mỗi ải:
  - chương 1 từ cấp 7 lên 36;
  - chương 2 từ 39 lên 62;
  - chương 6 khoảng 146–170;
  - chương 12 khoảng 306–330;
  - chương 72 khoảng 1.900.
- Cấp tài khoản lên nhờ máy bi; cấp tướng bằng cấp tài khoản, giống game mình.
- Nguồn: https://clashofcritters.online/chapters/. Logic trong bản rip (`D:\CrittersRipper`) mã hóa, không đọc được số.

### Đã đổi

| Chỗ | Cũ | Mới |
|---|---|---|
| Cấp tối đa | 30 | 200 |
| Sức theo cấp (`HeroStats`) | `1 + 0,1 × (cấp − 1)` | `1,03^(cấp − 1)`, nhân dồn (`lvStep` 0,03): mỗi cấp mạnh thêm 3% ở mọi cấp. Cấp 40: ×3,2; cấp 200: ×360 |
| Thủ trong trận (`Battle`) | sát thương × 100 / (100 + Thủ) | 100 nhân thêm hệ số cấp của người đánh: hai bên cùng cấp thì Thủ giảm sát thương như nhau ở mọi cấp. Không đổi thì ở cấp cao Thủ chặn gần hết sát thương |
| Lực chiến | như trên | tính Thủ theo cấp của chính tướng |
| Sao, cấp thẻ của địch (`Teams`) | 1 + cấp/6, thẻ 1 + cấp/5 | bằng người chơi bình thường ở cùng cấp: sao 2/3/4/5 ở cấp 7/23/50/96 (mốc lên sao của người chơi), thẻ 2/3/4/5 ở cấp 8/18/28/45 (số đo `ProgressSim`) |
| Địch đảo 70 ải (`Islands.LevelNorm`) | | Máu, Công ×0,8: bù cho sao và thẻ của địch nay ngang người chơi, để % cường hóa từng kiểu ải giữ như thiết kế |
| % cường hóa đảo Thủy (từ ải 4) | | Bầy lính −0,05, Cường hóa −0,15, Lính tinh nhuệ −0,05, Mini boss −0,15 (chặn ở 0), Hai tướng −0,05, Cửa ải +0,05, Boss +0,10 |
| EXP lên cấp sau | 40 × cấp^1,35 | 45 × cấp: cấp 40 cần tổng 35.100 EXP, cấp 200 cần 895.500 |
| Bi mỗi ải đảo 70 ải | theo cấp địch | theo số ải: 1 bi (ải 1–35), 2 bi (ải 36–70), đảo sau thêm 2 mỗi đảo |
| Ô đội | 2 ở cấp 10, 3 ở cấp 30 | 2 ở cấp 60, 3 ở cấp 200 |
| Mốc lên sao (`starLevel`) | 1, 2, 5, 9, 14 | 1, 7, 23, 50, 96 |
| Cược máy bi ×2/×3/×5/×10 | cấp 3/5/8/12 | cấp 12/23/40/80 |
| Rơi tối đa 30 bi/lần | cấp 15 | cấp 104 |
| Chỗ trang trại thêm | cấp 8/11/14/17/20 | cấp 40/70/96/120/144 |
| Thẻ chung mở theo cấp (`unlock`) | 1–10 | 1–60 |
| Đền Huy Hiệu | cấp đầu đảo + 3/bậc + 0,5/trận | + 20/bậc + 3/trận (`levelPerFight`) |
| Hang Tiềm Năng | cấp 6/12/18/24 | cấp 29/80/128/173 |
| Đảo gợi ý, nhãn Khó | cận dưới − 3 | cận dưới − 15 (`Progress.LevelSlack`) |
| Cảnh báo ở hộp Chuẩn bị trận | thiếu từ 3 cấp | thiếu từ 3 cấp: "Địch cấp X, bạn cấp Y: nên lên thêm cấp" |

Các mốc theo cấp đổi từ thang cũ theo vị trí trên các đảo:
- cấp cũ 8, 12, 17, 22, 28 (cuối Thủy … Thổ) thành 40, 80, 120, 160, 200;
- giữa các mốc thì nội suy (`relevel200.py` trong lần làm này).

**Người dùng chốt (2026-11-04):**
- ô đội 3 giữ ở cấp 200;
- người chơi "vừa" đạt cấp 200 ở ngày 57 là được;
- cả 5 đảo đều làm thành 70 ải, nhưng các đảo sau chưa vội: hoàn thiện đảo Thủy cho chuẩn rồi mới sang đảo sau.

### Số đo (máy tự chơi trong Core)

Tỉ lệ thắng đảo Thủy khi người chơi bằng cấp địch: sao, thẻ như địch; đội theo luật tướng khởi đầu, 1 ô vì ô 2 mở ở cấp 60; 100 trận mỗi ải; 5 lựa chọn tướng khởi đầu.

| Kiểu ải | Mục tiêu | Bằng cấp | Thiếu 3 cấp | Thiếu 6 cấp | Thiếu 10 cấp |
|---|---|---|---|---|---|
| Ải tướng mới | 100% | 99% | | | |
| Bầy lính | 91% | 92–96% | 83% | 67% | 33% |
| Cường hóa | 92% | 93% | 87% | 73% | 43% |
| Tướng và lính | 78% | 77–86% | 55% | 38% | 8% |
| Lính tinh nhuệ | 78% | 82–88% | 62% | 47% | 12% |
| Mini boss | 72% | 70–71% | 38% | 18% | 6% |
| Hai tướng | 69% | 72–75% | 52% | 32% | 7% |
| Cửa ải | 62% | 62–63% | 23% | 8% | 1% |
| Boss ải 70 | 61% | 67–71% | 44% | 26% | 17% |

Các cột thiếu cấp chỉ tính các ải có địch từ cấp 15 trở lên, lấy trung bình 5 lựa chọn tướng khởi đầu.

Nhịp cả game (`ProgressSim` 60 ngày, máy + 15%, tướng khởi đầu Giọt Sương; ngày xong đảo):

| Kiểu người chơi | Thủy | Hỏa | Kim | Mộc | Thổ | Cấp 200 |
|---|---|---|---|---|---|---|
| Chăm (6 lần × 5 trận/ngày) | 5 | 10 | 18 | 27 | 36 | ngày 42 |
| Vừa (3 × 3) | 8 | 13 | 26 | 37 | 49 | ngày 57 |
| Ít (1 × 2) | 35 | 44 | | | | cấp 83 ở ngày 60 |

- Người chơi "vừa" bị giới hạn bởi số trận: 9 trận mỗi ngày thì 70 ải cần ít nhất 8 ngày.
- Người chơi "chăm" bị cấp chặn: đánh lại ải cũ 1.664 trên 1.800 trận. Họ qua được ải có địch cao hơn mình khoảng 5–10 cấp, nhờ thắng 30–40% rồi đánh nhiều lần.
- Đảo Hỏa còn 8 ải tạm nên chỉ mất 5 ngày. Khi làm thành 70 ải, đảo sau sẽ lâu hơn đều.
- Các đảo 8 ải chưa chỉnh lại độ khó cho thang mới: người chơi qua được địch cao hơn mình khoảng 20 cấp.

Cách đo lại: dự án console biên dịch thẳng `Assets/01 Script/Core`. `Sim.StarterIsland` cho tỉ lệ thắng; `ProgressSim.Run` cho nhịp ngày.

Còn mở:
- Bốn đảo sau cần thành 70 ải. Cần chọn tướng và lính cho từng đảo, như `14_HeThongAi.md` mục "Còn lại".
- Bản lưu cũ giữ cấp đang có (tính theo đường EXP cũ) và chỉ dùng cho máy thử.

## 5 đảo song song (2026-11-05)

### Người dùng sửa

- "Các tướng ở từng mốc nhìn chung ở 5 đảo này level/sức mạnh có chênh lệch nhưng cũng chỉ ngang ngang nhau thôi, nghĩa là người chơi có thể chinh phục 5 đảo cùng 1 lúc chứ không phải lần lượt từng đảo."
- Ví dụ của người dùng với cấp tối đa 200: boss cuối Thủy 195, Hỏa 198, Mộc 190, Kim 200.
- Phiên 2026-11-04 hiểu câu "ở cấp 145 thì đang ở đảo 6… chia theo độ sâu cấp trong từng đảo" thành 5 dải 40 cấp nối tiếp. Nghĩa đúng: cấp tăng theo độ sâu trong mỗi đảo.

### Cấp

- Mọi đảo dùng một đường cấp: `1 + (đỉnh − 1) × ((ải − 1) / 69)^0,85` làm tròn (`IslandGen.LevelPow`). Mọi địch trong một ải cùng cấp.
- Đỉnh (boss cuối): Thủy 195, Hỏa 198, Kim 200, Mộc 190, Thổ 196. `zones.json` ghi `level` là [1, đỉnh].
- Cấp các mốc ở đảo Thủy: ải 5 cấp 18, ải 10 cấp 35, ải 15 cấp 51, ải 20 cấp 66, ải 30 cấp 94, ải 40 cấp 120, ải 50 cấp 146, ải 60 cấp 171, ải 70 cấp 195. Đảo Mộc thấp hơn 1–5 cấp ở cùng mốc.
- Đảo 8 ải (tạm; từ 2026-11-05 còn Kim, Thổ; từ 2026-11-06 không còn đảo nào): ải i ứng với ải `1 + (i − 1) × 69/7` của đường chung. Địch mạnh nhất của ải lấy cấp đó, địch khác giữ độ lệch cấp cũ trong ải. Chưa chỉnh độ khó.

### Bù ô đội theo cấp

- Từ cấp 60 người chơi có 2 ô đội, từ cấp 200 có 3 ô (`Progress.SlotsAt`). Đảo song song nên ở mọi đảo, ải từ cấp 60 được cộng thêm cường hóa (`IslandGen.Plan.extra`, theo số ô ở cấp của ải). Trước đây chỉ đảo Mộc cộng, vì cả đảo nằm ở cấp 121–160.
- Bảng cộng thêm có 6 nhóm: ải tướng thường, ải 1 địch, 2 địch, 3 địch, mini boss, boss.
- Hệ khắc làm số đo lệch nhiều giữa các đảo. Cùng một bảng thì đảo Thủy (đội Thổ khắc hệ) chỉ thắng mini boss 20%, đảo Mộc (đội Kim) thắng 77%. Vì vậy mỗi đảo dò riêng, với đội 2 tướng Khá khắc hệ, bằng cấp địch, sao và thẻ theo cấp, 150 trận mỗi ải (lệnh `tune` của dự án console).

| Nhóm (2 ô) | Thủy | Hỏa | Mộc | Mục tiêu |
|---|---|---|---|---|
| Ải tướng thường | +0,20 (không có ải nào ≥ cấp 60) | +0,20 | +0,20 | 100% |
| 1 địch (cường hóa) | +0,60 | +0,70 | +1,05 | 92% |
| 2 địch | +0,45 | +0,50 | +0,65 | 76% (trung bình các kiểu) |
| 3 địch | +0,30 | +0,35 | +0,45 | 84% |
| Mini boss | +0,40 | +0,65 | +1,00 | 72% |
| Boss | +0,85 | +0,95 | +0,95 | 61% |

Số đo: Thủy cường hóa 93%, 2 địch 76%, 3 địch 86%, mini boss 72%, boss 59–68%. Mộc cường hóa 92%, 2 địch 74%, 3 địch 84%, mini boss 73%, boss 59–63%. Hỏa (đội Thủy: Giọt Sương, Mi Nhi; 2026-11-05) cường hóa 93%, 2 địch 75%, 3 địch 85%, mini boss 74%, boss 56%. Đảo mới phải dò lại; bảng mặc định là của Mộc.

### Bi, rương, mở công trình

| Chỗ | Cũ (đảo nối tiếp) | Mới (đảo song song) |
|---|---|---|
| Bi mỗi ải | đảo 70 ải 1–2 bi, đảo sau thêm 2 mỗi đảo | `1 + (ải − 1)/14`: 1 bi ở ải 1–14 tới 5 bi ở ải 57–70, như nhau mọi đảo; đảo 8 ải quy số ải về thang 70 |
| Thưởng lần đầu | ải tướng +2, mini boss +4, boss +8 (đảo 8 ải có cách tính riêng) | như cũ, áp cho mọi đảo |
| Rương mốc (7 rương) | 4, 5 … 9 bi, rương cuối 15, đảo sau thêm 5 (rương cuối thêm 10) | 4, 7, 10 … 19 bi (thêm 3 mỗi rương), rương cuối 35 bi |
| Rương đảo 8 ải | 10 và 20 bi, cộng theo thứ tự đảo | 20 và 40 bi |
| Cây bi 2–5 | qua boss Thủy, Hỏa, Kim, Mộc | đạt cấp 30, 50, 80, 110 (`trees.unlockLevels`) |
| Đền Huy Hiệu | qua hết Đảo Thủy | thắng mini boss đầu của một đảo bất kỳ (ải 20; đảo 8 ải là ải 4) |
| Cấp dãy huy hiệu hệ X | cận dưới của Đảo X + 20/bậc + 3/trận | cấp mini boss đầu của Đảo X (`Badges.BaseLevel`) + 20/bậc + 3/trận |
| Hang Tiềm Năng | thắng mini boss Đảo Hỏa | đạt cấp 30 (`Progress.CaveLevel`) |
| Độ khó trên bảng đảo | theo khoảng cấp của đảo | theo ải kế tiếp: hơn từ 10 cấp là Dễ, bằng là Vừa sức, thiếu tới 6 cấp là Khó, thiếu hơn là Quá mạnh |
| Đảo gợi ý | đảo chưa xong đầu tiên theo thứ tự | đảo chưa xong có ải kế tiếp cấp thấp nhất |
| Ải AFK tự chọn | đảo sau trước | ải cấp cao nhất đã qua có rơi mảnh |
| Bảng đảo trên sảnh | "Cấp 1–40 · x/70 ải" | "Ải kế cấp X · x/70 ải" |

Mốc cây bi chọn để người chơi Vừa đạt cấp 200 vào khoảng ngày 57 như đã chốt. Lần đầu thử 40/80/120/160 thì người chơi Vừa mới tới cấp 185 ở ngày 60.

### Nhịp (ProgressSim 60 ngày, tướng khởi đầu Giọt Sương)

Hỏa, Kim, Thổ còn 8 ải nên đo bằng đảo giả 70 ải (kế hoạch Mộc, tướng cùng hệ xếp theo độ hiếm, lính mượn của Thủy/Mộc, đỉnh 198/200/196). Đảo giả không ghi vào dữ liệu. Bảng dưới đo trước khi đảo Hỏa có 70 ải thật (2026-11-05), chưa đo lại.

| Kiểu người chơi | Cấp ngày 7 | 14 | 21 | 30 | 42 | 57 | Xong 5 đảo | Cấp 200 |
|---|---|---|---|---|---|---|---|---|
| Chăm (6 lần × 5 trận) | 41 | 73 | 102 | 136 | 175 | 200 | ngày 46–49 | ngày 51 |
| Vừa (3 × 3) | 37 | 67 | 92 | 123 | 160 | 198 | ngày 53–57 | ngày 58 |
| Ít (1 × 2) | 14 | 25 | 35 | 47 | 64 | 83 | chưa | cấp 86 ở ngày 60 |

- Bi chủ yếu từ cây bi (Vừa: 47.650 bi từ cây, 17.700 từ trang trại, 1.700 từ ải), nên nhịp đổi chủ yếu theo mốc mở cây.
- Chăm chậm hơn trước (cấp 200 ngày 51, trước là 42) vì phải qua 350 ải thay vì 164, và bị cấp chặn (1.359 trận đánh lại).

### Bị động boss ở 5 mốc cuối

Người dùng dặn: mini boss, boss ở 5 mốc cuối (ải 30, 40, 50, 60, 70) có thể có bị động riêng. Không nhất thiết cả 5 con; con có bị động thì giảm chỉ số, con không có thì tăng; boss cuối đảo chắc chắn có.

- Dữ liệu: thẻ ở `cards.json` khoá `traits` (kiểu bị động, `owner` là tướng); địch trong ải mang `trait`. Trong trận chạy sau bị động của tướng, cùng cấp thẻ (địch từ cấp 45 có thẻ cấp 5, ×1,6). Hộp chuẩn bị ghi tên bị động trên dòng ghi chú của đối thủ ("Boss · Hồng Chung Dội · Cường hóa +85%") và mô tả ở dòng thứ hai của đầu mục "Đối thủ" (đầu mục giãn cao theo chữ).
- Trận rất ngắn (mỗi bên khoảng 2 lượt) và địch gần như không đánh thường (0,26 lần mỗi trận), nên bị động kiểu "đánh thường", "đầu lượt" hầu như không chạy. Bị động có tác dụng là "bị đánh", "máu thấp", "vào trận". Các bản thử bỏ đi: Huyền Vũ hút mana khi đánh thường, Lam Quân Công +5% mỗi lượt cộng dồn, Gió Lốc hút nộ khi đánh thường, Lam Quân +nộ khi bị đánh (tuyệt kỹ còn cần mana).
- Con không có bị động: cường hóa +0,10. Con có bị động: dò cường hóa để tỉ lệ thắng bằng con không có (đội 2 tướng Khá khắc hệ, bằng cấp, 300 trận).

| Mốc | Đảo Thủy | Bị động (chữ ở thẻ cấp 5) | Cường hóa thêm | Thắng |
|---|---|---|---|---|
| 30 | Vây Lam | không | +0,10 | 52% |
| 40 | Kuba | Mai Kim Cương: mỗi lần bị đánh 48% cơ hội khiên bằng 11% máu tối đa | −0,05 | 57% |
| 50 | Thương Lam | không | +0,10 | 63% |
| 60 | Huyền Vũ | Thần Quy Hộ Thể: lần đầu máu dưới 50%, khiên bằng 40% máu tối đa, hồi 16% máu | 0 | 62% |
| 70 | Lam Quân (boss) | Hồng Chung Dội: mỗi lần bị đánh 6% cơ hội làm địch choáng | −0,15 | 61% |

| Mốc | Đảo Mộc | Bị động (chữ ở thẻ cấp 5) | Cường hóa thêm | Thắng |
|---|---|---|---|---|
| 30 | Gió Lốc | Gió Cuốn: mỗi lần bị đánh hút 3 mana của địch | −0,15 | 58% |
| 40 | Long Vuốt | không | +0,10 | 65% |
| 50 | Thỏ Hoàng | Hoàng Giáp Hộ Thân: lần đầu máu dưới 50%, xoá hiệu ứng xấu, hồi 16% máu, Thủ +32% 2 lượt | 0 | 60% |
| 60 | Mộc Tinh | không | +0,10 | 56% |
| 70 | Thanh Long (boss) | Long Lân Phản Đòn: mỗi lần bị đánh 24% cơ hội gây 80% Công sát thương | −0,15 | 56% |

- Mini boss 5 mốc cuối nay khó hơn mục tiêu cũ (72%) vì con không bị động được +0,10 và con có bị động dò theo mức đó: thắng 52–65%.
- Huyền Vũ và Thỏ Hoàng tự thân yếu hơn các mini boss khác, nên dù có bị động vẫn giữ cường hóa 0 (không giảm).
- Kim có bị động boss từ 2026-11-05, Thổ từ 2026-11-06 (bảng dưới).

| Mốc | Đảo Hỏa | Bị động (chữ ở thẻ cấp 5) | Cường hóa thêm | Thắng |
|---|---|---|---|---|
| 30 | Hồng Liên | Niết Bàn Hỏa: lần đầu máu dưới 50%, hồi 24% máu, Công +40% 2 lượt | 0 | 70% |
| 40 | Giáp Long | không | +0,10 | 71% |
| 50 | Huyễn Viêm | Ảo Ảnh Hồ Ly: mỗi lần bị đánh 40% cơ hội hồi 8% máu | 0 | 69% |
| 60 | Hỏa Tinh | không | +0,10 | 55% |
| 70 | Lân Hỏa (boss) | Thánh Lân Hộ Thể: lần đầu máu dưới 50%, xoá hiệu ứng xấu, khiên 40% máu tối đa, đốt địch 3 lượt (13% máu mỗi lượt) | −0,15 | 57% |

- Đội Thủy Khá khắc hệ (Giọt Sương, Mi Nhi), bằng cấp, 300 trận. Hồng Liên và Huyễn Viêm tự thân yếu nên dù có bị động vẫn giữ cường hóa 0 (như Huyền Vũ, Thỏ Hoàng). Bản thử bỏ đi: Hồng Liên "mỗi lần bị đánh 48% cơ hội đốt địch" (bỏng quá yếu trong trận ngắn: không giảm vẫn thắng 82%).
- Sửa kèm: chữ thẻ bị động "bị đánh" có tỉ lệ nay ghi tỉ lệ (trước đó thiếu, vd. Cá Nóc "Mỗi lần bị đánh: 30% cơ hội đốt địch…").

| Mốc | Đảo Thổ | Bị động (chữ ở thẻ cấp 5) | Cường hóa thêm | Thắng |
|---|---|---|---|---|
| 30 | Hạt Dẻ | Vỏ Dẻ Hộ Thân: mỗi lần bị đánh 48% cơ hội khiên bằng 10% máu tối đa | 0 | 65% |
| 40 | Rùa Núi | không | +0,35 | 64% |
| 50 | Hổ Kim Cương | Kim Cương Bất Khuất: lần đầu máu dưới 50%, xoá hiệu ứng xấu, khiên 32% máu tối đa, Công +40% 2 lượt | −0,15 | 66% |
| 60 | Cự Phủ | không | +0,55 | 67% |
| 70 | Giáp Nham (boss) | Nham Giáp Chấn Địa: lần đầu máu dưới 50%, xoá hiệu ứng xấu, khiên 48% máu tối đa, làm địch choáng | −0,15 | 59% |

- Đội Mộc Khá khắc hệ (Nụ Hoa, Dê Hoa), bằng cấp, 300 trận. Không dò theo con không bị động như các đảo trước: Rùa Núi, Cự Phủ ở +0,10 thắng 83%, 92% (tự thân yếu), nên mỗi mốc dò tới mục tiêu cố định, mini boss 66%, boss 60% (lệnh `marktune` thêm vào bản chép dự án console ở scratchpad phiên 18b36478). Vẫn đúng luật: con có bị động giảm chỉ số, con không có tăng.

### Code

| File | Đổi |
|---|---|
| `Editor/IslandGen.cs` | Kế hoạch đảo Thủy (`IslandGen.Thuy`, sinh ra trùng khít 70 ải Thủy cũ khi đặt lại cấp cũ), `All`; đường cấp chung, `SlotExtra` và `Plan.extra` 6 nhóm; `Intro.trait`, `Intro.buff`; quà có `altFor`; golden `zones.json` (`ZonesGolden`) |
| `Editor/IslandGenMenu.cs` | Menu `PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (Thủy, Hỏa, Mộc)`; menu golden ghi thêm `zones.json` |
| `Core/Progress.cs` | `SlotsAt`, `NextLevel`, `DifficultyOf(s, d, z)`, `RecommendedZone`, bi ải, rương, `BadgesOpen`, `CaveOpen`, `CaveLevel` |
| `Core/Trees.cs`, `BalanceConfig.cs`, `balance.json` | `trees.unlockLevels` thay `unlockZones` |
| `Core/Badges.cs` | `BaseLevel` |
| `Core/Afk.cs` | ải AFK tự chọn theo cấp |
| `Core/Types.cs`, `GameData.cs`, `Battle/*`, `Game/Data/CardDb.cs`, `GameDb.cs`, `Editor/DataImporter.cs` | `StageEnemy.trait`, `Member.trait`, `Fighter.trait`, `GameData.Traits`, thẻ `traits` trong `CardDb`; bị động boss chạy trong trận; chuỗi rỗng (asset Unity ghi null thành "") là không có |
| `Core/CardText.cs` | Bị động "bị đánh" ghi tỉ lệ |
| `App/Scenes/HubZone.cs`, `HubScene.cs`, `ZoneScene.cs`, `BadgePedestal.cs`, `App/TreePanel.cs`, `PrepFoe.cs`, `StagePrepDialog.cs` | Chữ cấp ải kế, điều kiện mở công trình, cây bi "Đạt cấp X", bị động boss trong hộp chuẩn bị |
| Tests | `ZoneTests` (bi, độ khó, đảo gợi ý, mở công trình), `TreesTests`, `AdsTests`, `IslandTests.BiDongBoss_5MocCuoi`; trận so bản web ở `BadgeTests`, `PotentialTests` ghim cấp địch cũ (`foeLevel` trong golden, `TestData.AtLevel`) |

Dự án console để đo (biên dịch `Core/**` và `Editor/IslandGen.cs`): lệnh `apply` (ghi cấp mới vào dữ liệu), `tune` (bù 2 ô), `bosscurve`, `bosstune` (bị động boss), `pace` (nhịp, có đảo giả), `trace` (đếm sự kiện trận). Nằm ở scratchpad của phiên, có thể mất; golden vẫn tính trong Unity.

## Màn đảo (web)

- Đảo 70 ải phóng to bản đồ (×2,2 thay vì ×1,27).
- 10 ải tướng là mốc lớn trên đường mòn, có tướng đứng trên. Ải xen giữa là chấm nhỏ: vàng là đã qua, cam là đang đánh, xám là chưa mở.
- Chạm mốc hoặc chấm thì mở **bảng chặng**: mỗi ải một dòng có kiểu ải, địch, cấp, % cường hóa và bi; chạm dòng thì vào chuẩn bị trận.
- Thanh tiến độ có 7 rương. Khung dưới ghi "Ải 23/70 · Ngọn Hải Đăng 4" kèm nhãn kiểu ải.
- Hộp chuẩn bị trận ghi % cường hóa, "Lính, không thu phục". Ở ải 1 có dòng "Mặt nước in bóng Giọt Sương của bạn".

Đảo khác vẫn 8 ải như cũ. Code chạy được cả hai kiểu.

Thử nhanh: `chay_web.bat`, rồi vào Sổ tay để dùng bảng thử; hoặc mở `?fresh&skipintro&screen=zone&zone=thuy`.

## Code (web)

| File | Nội dung |
|---|---|
| `Web/src/core/data/islands.ts` | Kế hoạch đảo (`ISLANDS`), mẫu ải, cường hóa, `ENEMY_NORM`, hàm sinh 70 ải |
| `Web/src/core/data/minions.ts` | 6 lính, 18 thẻ; đăng ký vào `HERO`, `CARD` để trận dùng như tướng |
| `Web/src/core/data/stages.ts` | Đảo có kế hoạch thì sinh ải, đảo khác dùng 8 ải cũ. Thêm `zoneSize`, `zoneMiniAt`, `ZONE_CHESTS`, `buff`, `tag`, `chapter` |
| `Web/src/core/data/stages_v1.ts` | Cờ "ải cũ" cho `export_data.ts`, `export_golden.ts`: JSON và golden của Unity không đổi (đã đối chiếu từng file) |
| `Web/src/core/progression.ts` | `enemyMods` (cường hóa, lính, quy độ hiếm), bi mỗi ải, rương theo đảo, `zoneDone` |
| `Web/src/view/screens/zone.ts` | Đường mòn mốc và chấm, bảng chặng, nhãn kiểu ải |
| `Web/scripts/sim.ts` | Chế độ `island` |

## Đảo Mộc (làm lại 2026-11-05)

Người dùng gửi 10 hình aola cho đảo Mộc và dặn xếp theo thứ tự trái sang phải. Đảo Mộc thành 70 ải, sinh bằng bộ sinh đã chép sang Unity (`Editor/IslandGen.cs`, menu `PokiClash/Dữ liệu/Đảo Mộc: sinh lại 70 ải`). Danh sách tướng và nguồn aola: `13_DanhSachTuong.md`, mục Mộc.

### 10 tướng

| Ải | Chặng | Tướng | Độ hiếm (tạm) | Loại ải |
|---|---|---|---|---|
| 1 | Bờ Rêu | Tiên Lá | Thường | thường, tiến hóa |
| 5 | Đồng Hoa Sáng | Mầm Ú | Thường | thường, tiến hóa |
| 10 | Đồi Nấm | Dê Hoa | Khá | thường, tiến hóa |
| 15 | Rừng Dây Leo | Bờm Lá | Khá | thường, tiến hóa |
| 20 | Hang Nanh Gió | Phong Linh | Hiếm | mini boss |
| 30 | Thung Lũng Lá | Gió Lốc | Hiếm | mini boss |
| 40 | Vách Vuốt Rồng | Long Vuốt | Sử thi | mini boss |
| 50 | Rừng Trúc Ngọc | Thỏ Hoàng | Sử thi | mini boss (1 dạng, không tiến hóa) |
| 60 | Hang Pha Lê Lục | Mộc Tinh | Sử thi | mini boss |
| 70 | Cây Thần Ngàn Năm | Thanh Long (Thanh Long Con → Thanh Long → Lôi Thanh Long) | Huyền thoại | boss tiến hóa |

- **Tướng khởi đầu Nụ Hoa** mất ải 1, vì người dùng muốn ải 1 là Tiên Lá. Nụ Hoa đứng ở ải 2 cùng một lính, lần đầu chắc chắn rơi 2–4 mảnh như ải 1 cũ. Luật đổi thành "tướng khởi đầu là địch ở ải 1–4 đảo cùng hệ, lần đầu chắc chắn rơi mảnh" (`GameData.StarterStage`, `Validate`, `StarterTests`). Ải bóng (người chơi đấu với bóng tướng mình chọn) vẫn chỉ ở ải 1, nên người chọn Nụ Hoa gặp Nụ Hoa thật ở ải 2.
- Chặng đầu (ải 2–4): Nụ Hoa + lính; bầy lính; cửa ải Tiên Lá + lính. Không có tướng tặng.
- Lính: Bọ Sừng (trâu), Sâu Uốn → Rắn Gai (phản đòn), Chim (nhanh); thẻ chép lính đảo Thủy cùng vai. Loại 2 mở từ chặng 1, loại 3 từ chặng 2; bậc 2 từ ải 35.
- Cấp địch: `121 + 39 × ((ải − 1)/69)^0,85` làm tròn, như đường cong đảo Thủy dời lên 121–160.
- Tướng Mộc cũ không có suất trên đảo: Mầm Gỗ, Kiến Binh, Hiệp Sĩ Bánh Tét, Giác Long Gỗ (giữ trong danh sách, như Tám Tay ở đảo Thủy).
- Toạ độ 10 ải tướng trên ảnh đảo Mộc cũ (8 vòng) chia đều theo đường nối 8 vòng. Đảo Mộc chưa có bản đồ dài, màn đảo dùng bản đồ ×3.

### Sức địch

> Từ 2026-11-05 đảo Mộc nằm ở cấp 1–190 (5 đảo song song) và bảng cộng thêm áp theo số ô đội ở cấp của ải, dò lại theo 6 nhóm: xem mục "5 đảo song song". Phần dưới là số đo lúc đảo Mộc còn ở cấp 121–160.

Mẫu ải và % cường hóa lấy theo đảo Thủy hiện tại (đã chỉnh 2026-11-03/04). Đảo Thủy đo với 1 tướng; ở cấp 121 người chơi có 2 ô đội (ô 2 mở ở cấp 60) và đánh lần lượt hai tướng, nên đảo Mộc cộng thêm vào cường hóa của mọi địch (`IslandGen.Plan.extra`):

| Kiểu ải | Cộng thêm |
|---|---|
| Ải tướng mới thường (1, 5, 10, 15) | +0,20 |
| Ải một địch: cường hóa, mini boss, boss | +0,95 |
| Ải hai địch | +0,65 |
| Ải ba địch | +0,50 |

Vì cộng thẳng vào cường hóa, hộp chuẩn bị trận đảo Mộc ghi "Cường hóa" từ +35% (ải tướng thường) tới +120% (cường hóa cuối chặng).

Số đo (máy tự chơi trong Core, 60 trận mỗi ải, bằng cấp địch, sao và thẻ theo cấp):

| Kiểu ải | Mục tiêu (đảo Thủy) | 2 tướng Kim khắc hệ (Bu Lông, Mèo Quyền Sắt) | Thiếu 6 cấp | 1 Kim + 1 trung tính (Bu Lông, Giọt Sương) | 2 trung tính (Giọt Sương, Mi Nhi) |
|---|---|---|---|---|---|
| Ải tướng mới | 100% | 98% | 90% | 89% | 78% |
| Bầy lính | 91% | 87% | 60% | 62% | 27% |
| Cường hóa | 92% | 94% | 80% | 79% | 40% |
| Tướng và lính | 78% | 78% | 45% | 48% | 15% |
| Lính tinh nhuệ | 78% | 75% | 41% | 41% | 10% |
| Mini boss | 72% | 79% | 48% | 39% | 12% |
| Hai tướng | 69% | 75% | 44% | 47% | 11% |
| Cửa ải | 62% | 68% | 32% | 37% | 7% |
| Boss ải 70 | 61% | 63% | 40% | 15% | 3% |

Chỉnh theo đội mạnh nhất (2 tướng khắc đảo), như đảo Thủy chỉnh theo Võ Sư. Người chơi không có 2 tướng Kim sẽ thấy đảo Mộc khó hơn nhiều. Chưa chạy lại `Quét nhịp`.

## Đảo Hỏa (làm lại 2026-11-05)

Người dùng gửi 10 hình aola cho đảo Hỏa, thứ tự trái sang phải là thứ tự ải tướng. Đảo Hỏa thành 70 ải bằng `IslandGen.Hoa` (menu `PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (Thủy, Hỏa, Mộc)`). Danh sách tướng và nguồn aola: `13_DanhSachTuong.md`, mục Hỏa.

| Ải | Chặng | Tướng | Độ hiếm (tạm) | Loại ải |
|---|---|---|---|---|
| 1 | Bến Đá Đen | Sư Tử Lửa (tướng khởi đầu) | Khá | thường, tiến hóa |
| 5 | Suối Dung Nham | Khổng Lồ Lửa | Thường | thường, tiến hóa |
| 10 | Rừng Than Hồng | Kim Sư | Khá | thường, tiến hóa |
| 15 | Sườn Núi Khói | Nham Thần | Khá | thường, tiến hóa |
| 20 | Lò Lửa Thiền | Ngưu Quyền (Nghé Lửa → Ngưu Lãng Tử → Ngưu Quyền) | Hiếm | mini boss |
| 30 | Chùa Liên Hoa | Hồng Liên | Hiếm | mini boss, bị động |
| 40 | Lò Rèn Gai Thép | Giáp Long | Sử thi | mini boss |
| 50 | Rừng Lửa Ảo | Huyễn Viêm | Sử thi | mini boss, bị động |
| 60 | Hang Hồng Ngọc | Hỏa Tinh | Sử thi | mini boss |
| 70 | Miệng Núi Lửa | Lân Hỏa (Lân Con → Lân Ngàn Năm → Thánh Lân) | Huyền thoại | boss tiến hóa, bị động |

- **Ải 1 vẫn là Sư Tử Lửa:** hình ải 1 người dùng gửi (爆焰吉拉) là dạng 3 của dòng Sư Tử Lửa, nên không phải dời tướng khởi đầu như Nụ Hoa ở đảo Mộc. Ải 1 là Sư Tử Lửa thật (không phải bóng như đảo Thủy), lần đầu chắc chắn rơi 2–4 mảnh.
- **Ải 20:** hình người dùng gửi đầu tiên là 魔焰吉拉, siêu tiến hóa của chính dòng Sư Tử Lửa. Hồ Lửa đứng tạm tới 2026-11-06, người dùng thay bằng 火云牛斗士 (Ngưu Quyền, dòng 412 → 414). Đội Thủy thắng mini boss ải 20 76% (200 trận), cửa ải 29 (Ngưu Quyền + Nham Thần) 49%.
- Chặng đầu (ải 2–4): Sư Tử Lửa + lính; bầy lính; cửa ải Sư Tử Lửa + lính. Không có tướng tặng.
- Lính: Lò Lửa → Lò Quái (trâu), Nấm Lửa → Quái Nham (phản đòn), Khỉ Lửa → Khỉ Hỏa Diệm (nhanh); thẻ chép lính đảo Thủy, Mộc cùng vai. Loại 2 mở từ chặng 1, loại 3 từ chặng 2; bậc 2 từ ải 35.
- Cấp: đường chung, đỉnh 198 (ải 5 cấp 19, ải 20 cấp 67, ải 40 cấp 122, ải 70 cấp 198).
- Bù 2 ô và bị động boss: xem mục "5 đảo song song". Tỉ lệ thắng theo kiểu ải (đội Giọt Sương + Mi Nhi, bằng cấp, 100 trận mỗi ải), so với đảo Mộc (đội Bu Lông + Mèo Quyền Sắt):

| Kiểu ải | Hỏa | Mộc |
|---|---|---|
| 1 ô: ải tướng / cửa ải / bầy lính | 89% / 82% / 96% | 81% / 81% / 94% |
| 2 ô: cường hóa | 93% | 93% |
| 2 ô: tướng và lính / hai tướng / cửa ải / lính tinh nhuệ | 81% / 77% / 62% / 68% | 79% / 72% / 61% / 70% |
| 2 ô: bầy lính | 89% | 87% |
| 2 ô: mini boss / boss | 68% / 58% | 65% / 55% |

- Toạ độ 10 ải tướng chia đều theo đường nối 8 vòng của ảnh đảo Hỏa cũ. Đảo Hỏa chưa có bản đồ dài, màn đảo dùng bản đồ ×3.
- Hình 22 dạng tướng mới và 6 lính chưa xuất (máy sập giữa lượt xuất, xem `12_KeHoach_OpenSpec.md`), nên các tướng này chưa có hình trong game.

## Đảo Thổ (làm lại 2026-11-06)

Người dùng gửi 10 hình aola cho đảo Thổ, thứ tự trái sang phải là thứ tự ải tướng. Đảo Thổ thành 70 ải bằng `IslandGen.Tho` (menu `PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (5 đảo)`). Từ đây cả 5 đảo đều 70 ải, 350 ải. Danh sách tướng và nguồn aola: `13_DanhSachTuong.md`, mục Thổ.

| Ải | Chặng | Tướng | Độ hiếm (tạm) | Loại ải |
|---|---|---|---|---|
| 1 | Bãi Đá Cuội | Thạch Nhân (tướng khởi đầu) | Khá | thường, tiến hóa |
| 5 | Hang Lửng | Lửng Vương | Thường | thường, tiến hóa |
| 10 | Đồi Ngọc Lục | Cáo Đá | Khá | thường, tiến hóa |
| 15 | Mỏ Pha Lê | Hổ Khoan | Khá | thường, tiến hóa |
| 20 | Đền Phù Văn | Phù Văn | Hiếm | mini boss |
| 30 | Rừng Sồi Già | Hạt Dẻ | Hiếm | mini boss, bị động |
| 40 | Ruộng Bậc Thang | Rùa Núi | Sử thi | mini boss |
| 50 | Vách Kim Cương | Hổ Kim Cương (1 dạng, siêu tiến hóa của Hổ Khoan) | Sử thi | mini boss, bị động |
| 60 | Lò Gốm Đất Nung | Cự Phủ | Sử thi | mini boss |
| 70 | Kim Tự Viện | Giáp Nham (Đấu Sĩ Nham → Giáp Nham) | Huyền thoại | boss tiến hóa, bị động |

- **Ải 1 vẫn là Thạch Nhân:** hình ải 1 (震天石人) là dạng 3 của Thạch Nhân, như Sư Tử Lửa ở đảo Hỏa. Ải 1 là Thạch Nhân thật, lần đầu chắc chắn rơi 2–4 mảnh.
- **Ải 50:** 金刚虎王 là siêu tiến hóa của dòng Hổ Khoan (ải 15). Tạm làm tướng riêng 1 dạng như Thỏ Hoàng (câu hỏi 30 ở `12_KeHoach_OpenSpec.md`).
- Chặng đầu (ải 2–4): Thạch Nhân + lính; bầy lính; cửa ải Thạch Nhân + lính (như đảo Hỏa). Không có tướng tặng.
- Lính: Chuột Khoan → Khoan Giáp (trâu), Đá Con → Đá Xích (dội đòn: khiên, gai khi bị đánh), Ngựa Con → Ngựa Rằn (nhanh); thẻ chép lính đảo Kim cùng vai, gai đổi từ đốt sang phản sát thương. Dòng chuột hamster 1113 → 1114 xuất thử rồi bỏ (lạc đề), 2172 cũng bỏ (dáng tướng, không giống lính). Loại 2 mở từ chặng 1, loại 3 từ chặng 2; bậc 2 từ ải 35.
- Cấp: đường chung, đỉnh 196 (ải 5 cấp 18, ải 20 cấp 66, ải 40 cấp 121, ải 70 cấp 196).
- Bù 2 ô (`extra`, đội Nụ Hoa + Dê Hoa, 150 trận mỗi ải): cường hóa 0,8 → 92%, 2 địch 0,42 → 74%, 3 địch 0,3 → 85%, mini boss 0,55 → 73%, boss 0,55 → 60%. Tỉ lệ thắng theo kiểu ải (2 ô): cường hóa 92%, tướng và lính 79%, hai tướng 80%, cửa ải 61%, lính tinh nhuệ 74%, bầy lính 90%, mini boss 69%. 1 ô: ải tướng 83%, cửa ải 77%, bầy lính 90%.
- Toạ độ 10 ải tướng chia đều theo đường nối 8 vòng của ảnh đảo Thổ cũ. Đảo Thổ chưa có bản đồ dài, màn đảo dùng bản đồ ×3.

## Unity (chép 2026-11-03)

Từ 2026-11-03 làm ở Unity, bản web chỉ làm khi người dùng yêu cầu. Lần xuất cuối từ web dùng script trong thư mục tạm (không sửa `Web/`): JSON có 102 ải và khoá `minions` ở `heroes.json`, `cards.json`; golden có thêm `islands.json`. Từ nay số liệu sửa thẳng trong `Assets/02 Data/Json` rồi chạy menu `PokiClash/Nhập dữ liệu`.

**Đừng chạy lại `Web/scripts/export_data.ts`, `export_golden.ts` vào `Assets/`:** hai script này vẫn xuất bộ 8 ải cũ, không có lính, sẽ ghi đè mất 70 ải.

| File | Nội dung |
|---|---|
| `Core/Islands.cs` | Cỡ đảo, mini boss đầu, rương mốc theo đảo (điền từ danh sách ải); `EnemyMods` (cường hóa, lính, quy độ hiếm); tên kiểu ải |
| `Core/Types.cs`, `GameData.cs` | `StageTag`, `StageDef.tag`, `chapter`, `StageEnemy.buff`, `HeroDef.minion`; `GameData.Minions`, `MinionCards` (`Hero(id)` tìm được, không nằm trong `Heroes`) |
| `Core/Progress.cs`, `Badges.cs`, `Trees.cs` | Bi ải 70, rương 7 cái, xong đảo theo cỡ đảo, đền và dãy huy hiệu theo cỡ đảo và mini boss đầu |
| `Core/Battle/Teams.cs` | `Enemy(st, d)` gắn phần cộng của địch |
| `App/Scenes/ZoneScene.cs` | Đường mòn, chấm ải, rương theo tỉ lệ. Chạm chấm hay bệ mở hộp chuẩn bị của đúng ải đó, ải khoá cũng xem được (bảng chặng bỏ 2026-11-03). Bản đồ dài (2026-11-03, `ZoneDef.path`, `stops`, `plates`): bản đồ rộng 1,27 màn, đường mòn theo con đường cát của ảnh, bệ ải tướng cỡ thật ở bãi của ảnh, bảng tên ngược phía địa danh. Đảo chưa có bản đồ dài: bản đồ ×3, bệ thu nhỏ 0,75 |
| `ZonePip`, `ZoneChapterRow`, `ZoneChapterDialog` | Prefab `Items/ChamAi`, `Items/DongChang`, `Dialogs/BangChang`, dựng bằng menu `PokiClash/Prefab/Đảo 70 ải (ChamAi, DongChang, BangChang)`. Bảng chặng không mở nữa từ 2026-11-03 |
| `StagePrepDialog`, `PrepFoe`, `ZoneEnemy` | Nhãn kiểu ải, dòng "Mặt nước in bóng…", "Cường hóa +x%", "Yếu hơn x%", "Lính, không thu phục", máu boss tính cả phần cộng. Từ 2026-11-03: lực chiến từng đối thủ, dòng so lực chiến địch / đội bạn, thưởng là ô hình (`RewardTile`), ải khoá chỉ xem |
| `Tests/IslandTests.cs` | So từng ải với golden: kiểu ải, chặng, bi, đội địch, phần cộng khớp từng bit |
| `Editor/PlayTour.cs` | Menu `PokiClash/Thử/Đảo 70 ải: …` chụp màn đảo, hộp chuẩn bị (chạm chấm), trận có lính |
| `Editor/IslandGen.cs`, `IslandGenMenu.cs` (2026-11-05) | Bộ sinh 70 ải chép từ `islands.ts`, với % cường hóa đảo Thủy hiện tại; kế hoạch đảo Thủy, Hỏa, Mộc (`IslandGen.Thuy`, `Hoa`, `Moc`); menu `PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (Thủy, Hỏa, Mộc)`, menu `PokiClash/Thử/Tính lại golden islands, roster, cardtext, zones` |

Hình 6 lính đã nhập thành prefab (`Assets/04 Prefabs/Heroes/linh_*.prefab`, nén ASTC). Toàn bộ test EditMode qua (86).

## Còn lại

1. **Nhịp ngày:** đo lại 2026-11-05 với 5 đảo song song (đảo giả cho Hỏa, Kim, Thổ), xem mục "5 đảo song song". Đo lại khi ba đảo kia có 70 ải thật.
2. **Ảnh đảo Thủy mới: xong (2026-11-03).** Bản đồ dài 1024 × 4288 ghép từ 3 đoạn GPT (`ArtGen/Islands/PROMPTS.md`, mục "Đảo Thủy 70 ải"), đã vào game: chấm ải cách nhau 92 px khung 1080 (trước khoảng 30 px), bệ tướng cỡ thật, 10 địa danh sát bãi ải tướng. Đảo khác muốn 70 ải thì làm bản đồ dài theo cùng cách.
3. **Đảo Kim, Thổ: xong** (Kim 2026-11-05, Thổ 2026-11-06). Còn bản đồ dài cho đảo Thổ (gói GPT như `ArtGen/Islands/build_zone70_kim.py`) và đo lại nhịp ngày với 5 đảo thật.
4. **Bản lưu:** bản lưu cũ có `zones.thuy = 8` nay thành 8/70. Số ải toàn cục của đảo sau đổi (Hỏa từ 71), nhưng chỉ ảnh hưởng `clears`, chưa chỗ nào đọc.

Câu hỏi còn mở ghi ở `12_KeHoach_OpenSpec.md`, mục "Câu hỏi còn mở" (15–20).
