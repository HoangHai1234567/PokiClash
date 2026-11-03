# Bản web thử: đánh thẻ, máy bi, nuôi tướng

Viết 2026-10-31. Code: `D:\PokiClash\Web` (cách chạy ở `Web/README.md`). Mọi con số là số khởi điểm, đã chạy máy tự chơi nhưng chưa có người thật chơi.

## Đã chốt (2026-10-31)

| Câu hỏi | Người dùng chốt |
|---|---|
| Lõi trận | **Thẻ bài theo "GDD game Pokiwar"**, bỏ xếp khối. Bản xếp khối Unity (`Assets/01 Script/BanThu`) giữ nguyên, không dùng tiếp |
| Nhịp | **Luân phiên**: một bên chọn và đánh xong mới tới bên kia |
| Chiêu, Tuyệt kỹ | **Không tốn lần chọn**, chỉ tốn mana và nộ |
| Nút X ở máy bi | **Mức cược**: ×N tốn N bi mỗi lần thả, thưởng ×N |
| Hình tướng | Hình aola, **chỉ chạy máy local**, không đăng lên mạng |
| Phong cách | Độc, lạ, đẹp, cartoon vẽ tay |
| Bố cục (góp ý sau bản đầu) | Không phải game casual: **chia scene như Clash of Critters**, bỏ kiểu thanh tab chuyển màn |
| Ải | **Một đảo lớn chia 5 vùng hệ**, không khoá vùng nào; vùng sau mạnh hơn hẳn để người mới không đánh nổi. Chạm vùng thì sang scene đảo của hệ đó |
| Bắt đầu | Tặng **một tướng Thủy** (Tiểu Y), nên đảo Thủy là đảo đầu |

Các điểm GDD chưa nói, bản web tự chọn (cần duyệt) ở mục cuối.

## Vòng lõi

1. **Đánh ải**: thắng nhận bi; boss và mini boss rơi mảnh tướng.
2. **Máy bi**: bi ra EXP, hoàn bi, rương (bi, EXP, bản sao thẻ, đôi khi mảnh tướng).
3. **Mạnh lên**:
   - EXP lên **cấp người chơi, cũng là cấp mọi tướng** (+10% chỉ số mỗi cấp);
   - bản sao thẻ nâng cấp thẻ riêng;
   - tổng cấp thẻ mở **tiến hóa sao** (+8% mỗi sao);
   - đủ mảnh thì mở tướng mới.
4. Sang đảo khó hơn. Ải đã qua tự đánh khi vắng (AFK) ra bi, giữ tối đa 12 giờ.

## Phong cách: "Sổ tay phiêu lưu"

- Cả game là một cuốn sổ của trẻ con:
  - giấy kẻ ô có vân;
  - khung nét mực đen **rung nhẹ** (3 filter SVG thay nhau 6 lần mỗi giây, kiểu hoạt hình vẽ tay);
  - tô màu bút sáp gạch chéo;
  - băng keo dán thẻ;
  - con dấu "THẮNG!" đóng mực đỏ.
- Tướng aola hiện như **sticker**: viền trắng rồi viền mực.
- Trúng đòn thì nổ ngôi sao răng cưa có chữ tượng thanh tiếng Việt ("BỐP!", "CHÁT!", "ẦM!!").
- Máy bi vẽ tay: nấm đỏ chấm bi để bật, cốc hứng rương, máng thả hình đám mây đung đưa.
- Bản đồ là trang sổ có đường chấm mực, vẽ nguệch ngoạc ở lề.
- Âm thanh tổng hợp bằng WebAudio (tiếng bụp, tiếng keng), không dùng file.

## Scene và bố cục

Học theo Clash of Critters (bản đục trong `D:/CrittersRipper`): mỗi chức năng là một scene, có scene chính và các nút đưa sang scene khác; bản đồ có nút đánh lớn, thanh thưởng tiến độ, màn mây khi chuyển.

| Scene | Bố cục |
|---|---|
| **Sảnh: đảo lớn** | Ảnh đảo 9:16 phủ kín màn. 5 bảng tên vùng ghi cấp đề nghị, số ải đã qua và độ khó so với cấp người chơi (Dễ, Vừa sức, Khó, Quá mạnh!, Đã chinh phục). Mũi tên nhún chỉ vùng nên đánh. Làng máy bi ở giữa. Trên: cấp (vòng EXP), bi, AFK, Sổ tay. Dưới: 5 nút tròn Tướng, Sổ thẻ, **Máy Bi** (to nhất), Đánh tiếp, Sổ tay |
| **Đảo hệ** | Ảnh đảo hệ phóng to 1,27 lần, cuộn dọc, tự cuộn tới ải đang đánh. 8 ải dọc đường mòn từ bãi dưới lên hang boss (ải 4 mini boss, ải 8 boss), mở lần lượt; tướng đội trưởng đứng ở ải hiện tại. Trên: cấp đề nghị, độ khó, thanh tiến độ có **2 rương mốc** (qua 4 và 8 ải: bi + bản sao thẻ). Dưới: ải tiếp theo, địch, thưởng, nút **Đánh!** |
| Trận, Máy Bi, Tướng, Sổ thẻ, Sổ tay | Scene con có nút quay lại và tên scene; trận có thanh riêng |

**5 đảo** (thứ tự gợi ý Thủy → Hỏa → Kim → Mộc → Thổ, cấp đề nghị 1–7, 6–12, 11–17, 16–22, 21–28):
- mỗi đảo đánh tướng hệ của đảo, rơi mảnh tướng hệ đó;
- hệ đó lại khắc đảo kế tiếp (Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ), nên đi đúng thứ tự thì luôn có tướng khắc hệ;
- đảo Thủy tặng Võ Sư (qua ải 3) và Gia Bỉ (qua ải 6), để từ 1 tướng lên đội 3;
- bi mỗi ải tăng theo đảo (đảo sau gấp mấy lần đảo đầu).

**Ảnh đảo:** 4 ảnh (đảo lớn, Thủy, Hỏa, Kim) đã gen bằng Canva AI theo nét vẽ tay, toạ độ vùng và ải đã chấm theo ảnh. Đảo Mộc, Thổ tạm dùng bản đồ vẽ tay của game. Prompt và link tải: `Web/ArtGen/PROMPTS.md`.

## Trận

### Một hiệp

- Đầu mỗi hiệp, người chơi đi trước (chốt 2026-10-31; trước đó bên có **Tốc** cao hơn đi trước). Mỗi bên đi một lượt. Trận dừng ở 60 hiệp: bên có tổng phần trăm máu cao hơn thắng.
- Mỗi bên mang **1–3 tướng**, một tướng ra sân, còn lại dự bị. Hết tướng là thua.

### Một lượt

1. **Đầu lượt** (trước lần chọn đầu): đổi tướng được một lần.
   - Tướng vào sân nhận đủ mana của lượt.
   - Lượt nào cũng đổi được, không mất gì.
2. **Chọn 5 lần**, mỗi lần 1 trong 3 thẻ rút ngẫu nhiên từ bộ thẻ chung.
   - Trọng số rút: Thường 50, Khá 30, Hiếm 14, Sử thi 5, Huyền thoại 1.
   - Thẻ mở dần theo cấp người chơi.
3. **Xen thẻ riêng** lúc đang chọn (không tốn lần chọn):
   - **Chiêu**: tốn mana, một lần mỗi lượt. **Ra đòn ngay lúc bấm**, không vào hàng thẻ, rồi chọn tiếp (người dùng chốt 2026-11-03, bản Unity; bản web vẫn xếp Chiêu vào hàng). Thẻ đã xếp chỉ chạy cuối lượt nên không làm Chiêu mạnh hơn. Chiêu hạ tướng đối thủ thì hết lúc chọn: thẻ đã xếp chạy rồi hết lượt.
   - **Tuyệt kỹ**: cần đủ 100 nộ và mana. Thay cú đánh thường cuối lượt.
4. **Ra đòn**: thẻ chạy lần lượt theo thứ tự xếp, rồi đánh thường (hoặc Tuyệt kỹ).
5. Hết lượt: buff "lượt này" hết.

### Tài nguyên

- **Mana**: +20 đầu mỗi lượt của mình. Tướng dự bị +10. Tối đa 100.
- **Nộ**:
  - +10 mỗi cú đánh thường trúng;
  - bị đánh: + phần máu mất / máu tối đa × 80;
  - tối đa 100;
  - mỗi tướng giữ nộ riêng, nên đổi tướng là bỏ dở nộ của tướng cũ.

### Thời hạn hiệu ứng

- "**lượt này**": tới hết lượt của mình (buff đánh).
- "**tới lượt sau**": che cả lượt địch kế tiếp (buff thủ).
- Hiệu ứng lên địch đếm theo lượt của địch.

### Trạng thái

- **Bỏng**: mất % máu đầu lượt.
- **Hồi phục**: hồi % máu đầu lượt.
- **Choáng**: lượt sau chỉ chọn 3 thẻ, không Chiêu, không ra đòn.
- **Né**: né trọn cú đánh thường kế tiếp.

### Sát thương

```
sát thương = Công × (1 + buff Công) × hệ số đòn × 100 / (100 + Thủ × (1 + buff Thủ) × (1 − xuyên))
           × khắc hệ × chí mạng (×1,6; gốc 5%) × (1 + sát thương nhận thêm) × ngẫu nhiên 0,92–1,08
```

- Khiên đỡ trước, máu sau.
- **Ngũ hành**: Kim → Mộc → Thổ → Thủy → Hỏa → Kim. Đánh hệ mình khắc ×1,5; đánh hệ khắc mình ×0,75.

### Chỉ số tướng

- Tổng sức mạnh theo **độ hiếm** (Thường 1; Khá 1,1; Hiếm 1,22; Sử thi 1,36; Huyền thoại 1,5).
- 6 chỉ số gốc Aola chỉ quyết "dáng" (trâu hay công cao), lấy căn bậc hai cho đỡ lệch.
- Lý do: chỉ số gốc Aola chênh quá. Gia Bỉ (Thường) mạnh hơn hẳn Võ Sư.
- Cấp +10%, sao +8%.
- Boss: máu ×1,8, công ×1,1.
- Boss ải 8 (2026-11-02): đứng một mình, có thẻ **Tiến Hóa** (xem `12_KeHoach_OpenSpec.md`, mục "Boss tiến hóa").

### Máy địch

- Chấm điểm từng thẻ theo tình huống: máu thấp thì quý thẻ hồi, nộ sắp đầy thì quý thẻ tăng Công.
- Dùng Chiêu ngay khi đủ mana (trừ khi phải để dành mana cho Tuyệt kỹ). Trước 2026-11-03: dùng sau khi đã có thẻ tăng Công.
- Đổi tướng khi tướng đang đánh bị khắc hệ hoặc còn dưới 25% máu.
- Ở các ải đầu, máy chọn "kém" hơn (nhiễu cao), để người mới dễ thở.

## Thẻ riêng, tiến hóa, mảnh

- Mỗi tướng có 3 thẻ riêng: Chiêu, Tuyệt kỹ, Bị động.
- Mở tướng thì có cả 3 thẻ ở cấp 1.
- **Lên cấp thẻ** bằng bản sao (rơi trong rương máy bi): cấp 2/3/4/5 cần 2/4/8/15 bản sao. Mỗi cấp tăng số của thẻ thêm 15%.
- **Tiến hóa sao**: cần tổng cấp 3 thẻ và cấp người chơi.

  | Lên sao | Tổng cấp thẻ | Cấp người chơi |
  |---|---|---|
  | 2 | 5 | 2 |
  | 3 | 8 | 5 |
  | 4 | 11 | 9 |
  | 5 | 15 | 14 |

  Đây là cách hiểu câu "kinh nghiệm để nâng tướng, thẻ để tiến hóa tướng".
- **Mảnh tướng** (10/20/30/50 theo độ hiếm):
  - rơi ở boss, mini boss và vài ải thường;
  - ải boss đã qua còn rơi khi AFK, 8% mỗi giờ;
  - đôi khi có trong rương máy bi;
  - mảnh của tướng đã có đổi thành bản sao thẻ.
- Khởi đầu chỉ có Tiểu Y (Thủy); đảo Thủy tặng Võ Sư và Gia Bỉ.

## Máy bi

- **Mặt máy**:
  - 10 hàng đinh, 3 nấm bật;
  - 3 cốc hứng giữa máy: cốc nhỏ chính giữa ra rương vàng, hai cốc hai bên ra rương bạc;
  - 9 ô đáy, theo thứ tự: rương gỗ, EXP 15, EXP 5, +1 bi, EXP 10, +1 bi, EXP 5, EXP 15, rương gỗ.
- Máng thả đung đưa trái phải. Chạm hoặc giữ để thả, tối đa **20 bi mỗi đợt**.
- **Nút ×N** (×1, ×2 ở cấp 3, ×3 ở cấp 5, ×5 ở cấp 8, ×10 ở cấp 12): tốn N bi mỗi lần thả, mọi thưởng ×N.
  - Rương ×N ra N lần số thẻ, mỗi thẻ rút riêng (theo GDD).
- **Mốc Huyền thoại**: thả đủ 300 bi thì chắc chắn nhận Đại Sư Cà Sa. Sau đó thẻ Huyền thoại trong rương vàng chỉ 0,01%.
- **Tỉ lệ đo bằng mô phỏng** 6.000 bi (in trong game ở nút "Tỉ lệ"):

| Ô | Tỉ lệ |
|---|---|
| Rương vàng (cốc giữa) | ≈ 3 % |
| Rương bạc (2 cốc) | ≈ 6 % |
| Rương gỗ (2 ô mép) | ≈ 8,5 % |
| EXP 15 | ≈ 23 % |
| EXP 10 | ≈ 22 % |
| EXP 5 | ≈ 30 % |
| +1 bi | ≈ 8 % |

- Kỳ vọng mỗi bi ở ×1 (tính cả rương):
  - 9,6 EXP;
  - hoàn 0,33 bi;
  - 0,09 bản sao thẻ.
- Tính ra mỗi bi thực tiêu ra khoảng 14 EXP.
- **Rương**:

  | Rương | Bi | EXP | Thẻ | Mảnh |
  |---|---|---|---|---|
  | Gỗ | 55% | 35% | 10% (1 thẻ) | — |
  | Bạc | 30% | 30% | 35% (2 thẻ) | 5% |
  | Vàng | 20% | 20% | 50% (3 thẻ) | 10% |

  Thẻ trong rương là bản sao thẻ riêng của tướng đã có.

## Số đo máy tự chơi

Máy chơi cả hai bên, 50 trận mỗi ô (`npm run sim -- battle`). Mỗi đảo đánh bằng một đội khắc hệ, sao và cấp thẻ tăng dần theo đảo. Người thật thường chơi tốt hơn máy.

| Đảo | Đội thử | Ải thường ở cấp đề nghị | Boss ở cấp cao nhất của khoảng đề nghị |
|---|---|---|---|
| Thủy (1–7) | Tiểu Y, Võ Sư, Gia Bỉ; 1 sao | ải 1–6: 82–100% từ cấp 4 | 44% ở cấp 7, 70% ở cấp 9 |
| Hỏa (6–12) | Y Trạch, Tiểu Y, Võ Sư; 2 sao, thẻ 2 | ải 1–6: 62–100% | 56% ở cấp 12 |
| Kim (11–17) | Pháp Luân, Bồ Đề, Y Trạch; 2 sao, thẻ 2 | gần 100% | 80% ở cấp 17 |
| Mộc (16–22) | Hắc Dực, Vạn Quân, Lam Quân; 3 sao, thẻ 3 | 94–100% | 94% ở cấp 22 |
| Thổ (21–28) | Sứ Giả, Gia Bỉ, Hắc Dực; 3 sao, thẻ 3 | ải 5–7: 36–90% | boss Đại Sư Cà Sa là bức tường cuối, đã hạ cấp, cần đo lại |

- **Vào đảo sau sớm thì thua**: ở cấp 1, đảo Hỏa đã báo "Quá mạnh!" (địch cấp 6–11).
- **Độ dài trận**: 2–6 hiệp ở các đảo đầu, 8–12 hiệp ở đảo Thổ. Đảo Thổ dài vì Đại Sư Cà Sa tự hồi máu; nên rút ngắn khi chỉnh tiếp.

## Bản web tự chọn (cần duyệt)

GDD chưa nói những điểm dưới đây, bản web tạm chọn như sau:

1. **Bên đi trước**: bên có Tốc cao hơn đi trước mỗi hiệp. Hoặc: người chơi luôn đi trước.
2. **Cấp chung**: cấp người chơi là cấp mọi tướng (theo GDD). Tướng mới mở cũng mạnh ngay.
3. **Thẻ chung không nâng cấp**; chỉ thẻ riêng của tướng lên cấp bằng bản sao.
4. **Tiến hóa = sao**, mở bằng tổng cấp thẻ. Không đổi hình, vì dòng tiến hóa aola được tách thành tướng riêng (Lam Quân → Vạn Quân → Hắc Dực là 3 tướng riêng, mở bằng mảnh).
5. **Đổi tướng không mất gì**, mỗi lượt một lần, chỉ trước lần chọn đầu.
6. **Choáng**: lượt sau chỉ chọn 3 thẻ, không Chiêu, không ra đòn (không mất cả lượt).
7. **Thẻ bị động** của thẻ chung chưa có. GDD nhắc "thẻ chỉ kích khi dưới 15% máu": bản web đặt ở thẻ riêng (Phật Tâm, Cánh Đêm).
8. **Bi chỉ kiếm bằng chơi** (đánh ải, AFK, hoàn bi). Nút ×2 AFK giả lập quảng cáo, không có cửa hàng.

## Chưa làm

- Huy hiệu tộc hệ, đá tiềm năng, trang trại (side meta trong GDD).
- Cửa hàng, gói nạp, quảng cáo thật.
- Nhật ký trận chi tiết; xuất số liệu trận ra file như bản Unity `tran.csv`.
- Hình mặt sau cho tướng phe mình (đang dùng mặt trước lật ngang).
- Clip đánh của mặt trước Aola lao sang phải-xuống, nên địch đặt trên-trái. Đòn của phe mình được nắn lại hướng lao cho trúng địch; vài tướng bắn từ xa thì chỉ nhún tới.

## Bảng số (sinh từ dữ liệu: `npx tsx scripts/gen_doc.ts`)

### Tướng (chỉ số ở cấp 1, 1 sao)

| Tướng | Hệ | Độ hiếm | Máu | Công | Thủ | Tốc | Mảnh mở | Chiêu | Tuyệt kỹ | Bị động |
|---|---|---|---|---|---|---|---|---|---|---|
| Võ Sư | Thổ | Thường | 627 | 188 | 50 | 46 | 10 | **Thiết Quyền** (30 mana): Gây 120% Công sát thương. +10 nộ. | **Bách Liệt Quyền** (100 nộ + 40 mana): Đánh 5 lần, mỗi lần 50% Công. | **Da Đồng**: Vào trận: +15% Thủ cả trận. |
| Võ Tăng Bồ Đề | Hỏa | Hiếm | 705 | 247 | 60 | 126 | 20 | **Liên Hoa Hỏa** (35 mana): Gây 100% Công sát thương. Đốt địch 3 lượt (5% máu mỗi lượt). | **Hỏa Dực Phần Thiên** (100 nộ + 40 mana): Gây 260% Công sát thương. Đốt địch 3 lượt (8% máu mỗi lượt). | **Lửa Thiền**: Mỗi đòn đánh thường: 30% cơ hội đốt địch 2 lượt (5% máu mỗi lượt). |
| Thiền Sư Pháp Luân | Hỏa | Sử thi | 768 | 255 | 76 | 131 | 30 | **Pháp Luân Chuyển** (40 mana): Gây 130% Công sát thương. Hút 20 mana của địch. | **Đại Pháp Luân** (100 nộ + 50 mana): Gây 220% Công sát thương. Làm địch choáng. | **Thiền Định**: Đầu mỗi lượt: +10 mana. |
| Đại Sư Cà Sa | Thổ | Huyền thoại | 866 | 279 | 83 | 125 | 50 | **Khói Hương** (40 mana): Hồi 25% máu. Xoá hiệu ứng xấu. | **Kim Cang Pháp Tướng** (100 nộ + 50 mana): Gây 300% Công sát thương. Khiên bằng 30% máu tối đa. | **Phật Tâm**: Lần đầu gục: hồi sinh với 35% máu (boss không hồi sinh). |
| Gia Bỉ | Mộc | Thường | 593 | 182 | 55 | 113 | 10 | **Hạt Giống** (25 mana): Hồi 7% máu đầu mỗi lượt, 3 lượt. Gây 60% Công sát thương. | **Rừng Gai** (100 nộ + 35 mana): Gây 210% Công sát thương. Địch −20% Thủ 2 lượt. | **Quang Hợp**: Đầu mỗi lượt: +8 nộ. |
| Sứ Giả Gia Bỉ | Mộc | Hiếm | 689 | 237 | 65 | 93 | 20 | **Nanh Gió** (35 mana): Đánh 2 lần, mỗi lần 75% Công. | **Phong Mộc Sứ** (100 nộ + 45 mana): Gây 240% Công sát thương. +30% Công trong 2 lượt. | **Nhanh Nhẹn**: Vào trận: 15% né đòn đánh thường cả trận. |
| Lam Quân | Kim | Thường | 581 | 196 | 52 | 49 | 10 | **Chuông Đồng** (30 mana): Gây 100% Công sát thương. 30% cơ hội: Làm địch choáng. | **Hồng Chung** (100 nộ + 40 mana): Gây 230% Công sát thương. Địch −20% Thủ 2 lượt. | **Vỏ Thép**: Vào trận: khiên bằng 12% máu tối đa. |
| Vạn Quân | Kim | Hiếm | 709 | 234 | 65 | 89 | 20 | **Đại Chùy** (40 mana): Gây 160% Công sát thương. | **Vạn Quân Lôi Chung** (100 nộ + 45 mana): Gây 280% Công sát thương. Làm địch choáng. | **Giáp Trụ**: Vào trận: giảm 12% sát thương cả trận. |
| Hắc Dực Vạn Quân | Kim | Sử thi | 779 | 264 | 72 | 101 | 30 | **Hắc Dực Trảm** (40 mana): Gây 150% Công sát thương, hút 30% thành máu. | **Hắc Vũ Thiên Chung** (100 nộ + 50 mana): Gây 320% Công sát thương, xuyên 50% Thủ. | **Cánh Đêm**: Lần đầu máu dưới 50%: +25% Công cả trận. |
| Tiểu Y | Thủy | Thường | 472 | 214 | 54 | 41 | 10 | **Bọt Nước** (25 mana): Gây 90% Công sát thương. Địch −15% Công 1 lượt. | **Vòi Rồng Nhỏ** (100 nộ + 35 mana): Gây 200% Công sát thương. Hồi 15% máu. | **Mát Lành**: Đầu mỗi lượt: hồi 4% máu. |
| Y Trạch | Thủy | Hiếm | 645 | 245 | 67 | 81 | 20 | **Đinh Ba** (35 mana): Gây 140% Công sát thương. Địch −20% Thủ 2 lượt. | **Hải Long Quyển** (100 nộ + 45 mana): Gây 250% Công sát thương. Hồi 25% máu. | **Thủy Triều**: Mỗi lần bị đánh: +8 mana. +4 nộ. |

### Thẻ chung

| Thẻ | Độ hiếm | Mở ở cấp | Tác dụng |
|---|---|---|---|
| Mài Vuốt | Thường | 1 | +25% Công lượt này. |
| Giáp Gỗ | Thường | 1 | Giảm 20% sát thương tới lượt sau. |
| Băng Gạc | Thường | 1 | Hồi 8% máu. |
| Hít Thở | Thường | 1 | +15 mana. |
| Gầm Gừ | Thường | 1 | +15 nộ. |
| Ném Đá | Thường | 1 | Gây 45% Công sát thương. |
| Bình Thuốc | Khá | 1 | Hồi 18% máu. |
| Bánh Bao Thịt | Khá | 1 | +12% máu tối đa cả trận. |
| Liều Mạng | Khá | 1 | Mất 25% máu đang có. +50% Công lượt này. |
| Thủ Thế | Khá | 1 | Khiên bằng 12% máu tối đa. |
| Tĩnh Tâm | Khá | 1 | +30 mana. |
| Đấm Kép | Khá | 2 | Cuối lượt đánh thêm một cú 50% Công. |
| Cuồng Nộ | Hiếm | 1 | +100% Công lượt này. −30% Thủ trong 2 lượt địch. |
| Hút Máu | Hiếm | 3 | Hút 50% sát thương thành máu lượt này. |
| Phá Giáp | Hiếm | 1 | Địch −30% Thủ 2 lượt. |
| Đốt Lửa | Hiếm | 3 | Đốt địch 3 lượt (6% máu mỗi lượt). |
| Gương Đôi | Hiếm | 5 | Thẻ kế tiếp chạy 2 lần. |
| Mắt Ưng | Hiếm | 5 | +50% chí mạng lượt này. |
| Bùa Choáng | Sử thi | 7 | Làm địch choáng. |
| Hoà Khí | Sử thi | 7 | +30 mana. +30 nộ. |
| Áo Choàng Ma | Sử thi | 7 | Né trọn đòn đánh kế tiếp. |
| Nghịch Thiên | Huyền thoại | 10 | Máu dưới 50%: hồi 40% máu, +60% Công lượt này. Không thì: +30% Công lượt này. |
| Thiên Mệnh | Huyền thoại | 10 | Đòn đánh lượt này bỏ qua Thủ, ×1,5. |

### Ải

| Đảo | Ải | Tên | Loại | Địch (cấp) | Bi (lần đầu / đánh lại) | Thưởng mảnh (lần đầu) |
|---|---|---|---|---|---|---|
| Đảo Thủy | 1 | Bãi Vỏ Sò | Thường | Tiểu Y 1 | 8 / 3 | — |
| Đảo Thủy | 2 | Vũng San Hô | Thường | Tiểu Y 2 | 8 / 3 | — |
| Đảo Thủy | 3 | Cầu Gỗ Rêu | Thường | Tiểu Y 2, Tiểu Y 3 | 9 / 4 | Võ Sư gia nhập |
| Đảo Thủy | 4 | Ngọn Hải Đăng | Mini boss | Y Trạch 3 (boss) | 12 / 4 | Y Trạch 3–5 (100%) |
| Đảo Thủy | 5 | Làng Vỏ Ốc | Thường | Tiểu Y 4, Y Trạch 4 | 10 / 5 | — |
| Đảo Thủy | 6 | Thác Bạc | Thường | Y Trạch 5, Tiểu Y 5 | 10 / 5 | Gia Bỉ gia nhập |
| Đảo Thủy | 7 | Hồ Gương | Thường | Tiểu Y 5, Y Trạch 5, Tiểu Y 5 | 11 / 6 | Y Trạch 1–2 (30%) |
| Đảo Thủy | 8 | Xoáy Nước Đinh Ba | Boss | Tiểu Y 5, Y Trạch 6 (boss) | 18 / 6 | Y Trạch 4–6 (100%) |
| Đảo Hỏa | 1 | Bến Đá Đen | Thường | Võ Tăng Bồ Đề 6 | 14 / 7 | — |
| Đảo Hỏa | 2 | Suối Dung Nham | Thường | Võ Tăng Bồ Đề 7 | 14 / 7 | — |
| Đảo Hỏa | 3 | Chùa Liên Hoa | Thường | Võ Tăng Bồ Đề 7, Võ Tăng Bồ Đề 8 | 15 / 8 | Võ Tăng Bồ Đề 1–2 (30%) |
| Đảo Hỏa | 4 | Lò Lửa Thiền | Mini boss | Võ Tăng Bồ Đề 9 (boss) | 18 / 8 | Võ Tăng Bồ Đề 3–5 (100%) |
| Đảo Hỏa | 5 | Rừng Than Hồng | Thường | Võ Tăng Bồ Đề 9, Thiền Sư Pháp Luân 8 | 16 / 9 | — |
| Đảo Hỏa | 6 | Cổng Bánh Xe | Thường | Thiền Sư Pháp Luân 10 | 16 / 9 | Thiền Sư Pháp Luân 1–2 (25%) |
| Đảo Hỏa | 7 | Sườn Núi Khói | Thường | Võ Tăng Bồ Đề 9, Thiền Sư Pháp Luân 9, Võ Tăng Bồ Đề 9 | 17 / 10 | — |
| Đảo Hỏa | 8 | Miệng Núi Lửa | Boss | Võ Tăng Bồ Đề 9, Thiền Sư Pháp Luân 11 (boss) | 24 / 10 | Thiền Sư Pháp Luân 4–6 (100%), Võ Tăng Bồ Đề 2–3 (50%) |
| Đảo Kim | 1 | Cảng Sắt | Thường | Lam Quân 11 | 20 / 11 | — |
| Đảo Kim | 2 | Cầu Bánh Răng | Thường | Lam Quân 12 | 20 / 11 | Lam Quân 1–2 (30%) |
| Đảo Kim | 3 | Tháp Canh Thép | Thường | Lam Quân 12, Lam Quân 13 | 21 / 12 | — |
| Đảo Kim | 4 | Gác Chuông Đồng | Mini boss | Vạn Quân 13 (boss) | 24 / 12 | Lam Quân 4–6 (100%) |
| Đảo Kim | 5 | Mỏ Sắt Ngân | Thường | Vạn Quân 15, Lam Quân 15 | 22 / 13 | — |
| Đảo Kim | 6 | Xưởng Đúc Chuông | Thường | Vạn Quân 16 | 22 / 13 | Vạn Quân 1–2 (30%) |
| Đảo Kim | 7 | Tổ Cánh Đêm | Thường | Hắc Dực Vạn Quân 16 | 23 / 14 | Hắc Dực Vạn Quân 1–2 (25%) |
| Đảo Kim | 8 | Thiên Chung Hắc Dực | Boss | Vạn Quân 15, Hắc Dực Vạn Quân 17 (boss) | 30 / 14 | Hắc Dực Vạn Quân 4–6 (100%), Vạn Quân 2–3 (50%) |
| Đảo Mộc | 1 | Bờ Rêu | Thường | Gia Bỉ 16 | 26 / 15 | — |
| Đảo Mộc | 2 | Đồi Nấm | Thường | Gia Bỉ 17 | 26 / 15 | — |
| Đảo Mộc | 3 | Rừng Dây Leo | Thường | Gia Bỉ 17, Gia Bỉ 18 | 27 / 16 | — |
| Đảo Mộc | 4 | Hang Nanh Gió | Mini boss | Sứ Giả Gia Bỉ 18 (boss) | 30 / 16 | Sứ Giả Gia Bỉ 3–5 (100%) |
| Đảo Mộc | 5 | Đồng Hoa Sáng | Thường | Sứ Giả Gia Bỉ 19, Gia Bỉ 19 | 28 / 17 | — |
| Đảo Mộc | 6 | Cây Cổ Thụ Con | Thường | Sứ Giả Gia Bỉ 20 | 28 / 17 | Sứ Giả Gia Bỉ 1–2 (30%) |
| Đảo Mộc | 7 | Thung Lũng Lá | Thường | Gia Bỉ 20, Sứ Giả Gia Bỉ 20, Gia Bỉ 20 | 29 / 18 | — |
| Đảo Mộc | 8 | Cây Thần Ngàn Năm | Boss | Gia Bỉ 20, Sứ Giả Gia Bỉ 22 (boss) | 36 / 18 | Sứ Giả Gia Bỉ 4–6 (100%) |
| Đảo Thổ | 1 | Bãi Cát Vàng | Thường | Võ Sư 21 | 32 / 19 | — |
| Đảo Thổ | 2 | Đồi Đất Nung | Thường | Võ Sư 22 | 32 / 19 | — |
| Đảo Thổ | 3 | Cầu Treo | Thường | Võ Sư 22, Võ Sư 23 | 33 / 20 | — |
| Đảo Thổ | 4 | Võ Đường Đá | Mini boss | Võ Sư 24 (boss) | 36 / 20 | Võ Sư 3–5 (100%) |
| Đảo Thổ | 5 | Ruộng Bậc Thang | Thường | Võ Sư 24, Đại Sư Cà Sa 21 | 34 / 21 | — |
| Đảo Thổ | 6 | Chùa Đá | Thường | Đại Sư Cà Sa 22 | 34 / 21 | Đại Sư Cà Sa 1–2 (20%) |
| Đảo Thổ | 7 | Sân Tượng Đá | Thường | Võ Sư 25, Đại Sư Cà Sa 23, Võ Sư 25 | 35 / 22 | — |
| Đảo Thổ | 8 | Kim Tự Viện | Boss | Võ Sư 24, Đại Sư Cà Sa 23 (boss) | 42 / 22 | Đại Sư Cà Sa 5–8 (100%) |

### Cấp người chơi

| Cấp | EXP lên cấp sau |
|---|---|
| 1 | 40 |
| 2 | 102 |
| 3 | 176 |
| 4 | 260 |
| 5 | 351 |
| 6 | 449 |
| 8 | 663 |
| 10 | 895 |
| 12 | 1145 |
| 15 | 1548 |
| 20 | 2283 |

Nút cược máy bi mở theo cấp: ×1 ở cấp 1, ×2 ở cấp 3, ×3 ở cấp 5, ×5 ở cấp 8, ×10 ở cấp 12.
AFK: 12 bi/giờ khi đã qua 10 ải (4 + 0,8 × tổng số ải đã qua), giữ tối đa 12 giờ.
