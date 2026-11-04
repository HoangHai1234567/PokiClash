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
  - Mỗi đảo khoảng 40 cấp: Thủy 1–40, Hỏa 41–80, Kim 81–120, Mộc 121–160, Thổ 161–200.
  - Đảo Thủy: `1 + 39 × ((ải − 1) / 69)^0,85` làm tròn, lên nhanh hơn một chút ở đầu đảo. Ải 5 cấp 4, ải 10 cấp 8, ải 20 cấp 14, ải 30 cấp 20, ải 50 cấp 30, ải 70 cấp 40. Cứ 1–2 ải lên 1 cấp.
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

Hình 6 lính đã nhập thành prefab (`Assets/04 Prefabs/Heroes/linh_*.prefab`, nén ASTC). Toàn bộ test EditMode qua (86).

## Còn lại

1. **Chạy lại `Quét nhịp`** (ProgressSim) để xem nhịp ngày với 70 ải.
2. **Ảnh đảo Thủy mới: xong (2026-11-03).** Bản đồ dài 1024 × 4288 ghép từ 3 đoạn GPT (`ArtGen/Islands/PROMPTS.md`, mục "Đảo Thủy 70 ải"), đã vào game: chấm ải cách nhau 92 px khung 1080 (trước khoảng 30 px), bệ tướng cỡ thật, 10 địa danh sát bãi ải tướng. Đảo khác muốn 70 ải thì làm bản đồ dài theo cùng cách.
3. **Bốn đảo còn lại:** chọn 10 tướng, 3 loại lính mỗi đảo. Bộ sinh 70 ải (`islands.ts`) hiện chỉ có ở web; danh sách ải trong Unity là dữ liệu đã sinh sẵn. Làm đảo mới thì chép bộ sinh sang Unity (menu Editor ghi `stages.json`), hoặc dùng web nếu người dùng cho.
4. **Bản lưu:** bản lưu cũ có `zones.thuy = 8` nay thành 8/70. Số ải toàn cục của đảo sau đổi (Hỏa từ 71), nhưng chỉ ảnh hưởng `clears`, chưa chỗ nào đọc.

Câu hỏi còn mở ghi ở `12_KeHoach_OpenSpec.md`, mục "Câu hỏi còn mở" (15–20).
