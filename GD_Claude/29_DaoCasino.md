# 29. Đảo Casino: máy bi ở giữa, các trò quanh đảo mở dần và theo sự kiện (kế hoạch 2026-11-25)

Viết 2026-11-25. Mới là kế hoạch, chưa làm dòng code nào. Mọi con số là số đầu, đo lại bằng `ProgressSim` trước khi chốt.

## Người dùng dặn (2026-11-25)

> "phần máy bắn bi sẽ thành 1 phần game chính của 1 đảo mới đó là đảo casino, trong cốt truyện đó sẽ là 1 đảo để các thám hiểm gia có đi qua
> thì nghỉ chân ở đấy. Ở đó máy chính và to nhất ở giữa đảo là máy thả bóng, xung quanh sẽ có các mini game khác sẽ unlock từ từ có những cái
> sẽ mở theo event rồi đóng tùy vào event là gì [...]" rồi "đây là 1 tính năng lớn, nên lên plan chi tiết".

| Trò | Lời dặn |
|---|---|
| Máy thả bóng | Máy chính, to nhất, **ở giữa đảo** |
| Blackjack | Đặt cược với dealer **bằng bóng**; cược càng nhiều thì thưởng càng lớn (**mảnh tướng hoặc nhiều bóng hơn**) |
| Đua tướng | Cho các tướng chạy đua |
| Chợ đen | Trade vật phẩm game |
| Câu cá | (chưa dặn thêm) |
| Roulette | Đặt cược, kiểu giống blackjack |
| Slot machine | Chơi cũng mất bóng |
| Underground battle | Tướng đánh ở đấu trường ngầm; **set tướng đổi theo ngày do mình tự đặt**; đánh tướng càng khó quà càng to; **lệ phí là bóng** |
| Khác | "......": còn thêm trò khác. Mục 6.8 có vài đề xuất |
| Mở khoá | Trò mở dần; có trò **mở theo sự kiện rồi đóng** |

**Đổi lời dặn cũ.** Ngày 2026-11-19 người dùng bỏ đảo / tháp máy bi khỏi bản đồ sảnh ("bỏ cái máy pinball đi, không cần có đảo đấy"). Kế hoạch
này **không** đưa máy bi trở lại giữa bản đồ sảnh: đảo Casino là một đảo riêng như Nhà, đi bằng tàu, nằm ở mép bản đồ.

## Đã chốt (2026-11-25)

Người dùng: "ok theo đề xuất hết, làm đi". Cả 12 câu ở mục 14 theo đề xuất:
1. Làm Blackjack, Roulette, Slot nhưng **chỉ mở theo lịch sự kiện**; khai bảng hỏi tuổi đúng thực tế; có cờ theo nước để tắt.
2. Cược **bằng bi trực tiếp**, trần ngày, bậc cược theo cấp.
3. Nút Máy Bi **vẫn vào thẳng máy**; trong máy có nút "Ra đảo".
4. Tên trong truyện: **Bến Lữ Khách**.
5. Cố định: Máy bi, Câu cá, Đua tướng, Chợ đen, Đấu trường ngầm, Quán trọ (+ Bói sao); theo sự kiện: Blackjack, Roulette, Slot (Ném vòng, Đập hũ để sau).
6. Chợ đen chỉ đổi với lái buôn.
7. Đua: tướng của mình chạy, có cổ vũ.
8. Có trần lượt có thưởng mỗi ngày (hết trần vẫn chơi ván tập).
9. Đội ngầm: vòng lặp + ghi đè ngày lễ trong `balance.json`; Claude soạn 2 tuần đầu.
10. Cấp mở như mục 5.1. 11. Lịch 14 ngày như mục 5.2. 12. Gen concept đảo trước để duyệt.

**Concept đảo (2026-11-25): người dùng chọn hướng B, đảo vành khuyên quanh hồ** (`ArtGen/Casino/concept/concept_B_dao_vanh_khuyen.png`):
Tháp Máy Bi trên đảo nhỏ giữa hồ, ba cầu gỗ nối ra vành đảo; quanh vành theo chiều kim đồng hồ từ dưới: bến tàu + bảng lịch (nam),
bến câu thò vào hồ (tây nam), chợ đêm (tây), hang đấu trên đồi đá (tây bắc), trường đua (đông bắc), quán trọ (đông nam), 3 bãi lều xen giữa.

## Tóm tắt

- **Đảo Casino** (tên trong truyện đề xuất: *Bến Lữ Khách*, câu 4) là bến nghỉ chân giữa năm đảo hệ. Giữa đảo là **Tháp Máy Bi**: chính máy bi
  đang có, phóng to thành công trình. Quanh tháp có 5 công trình cố định mở dần theo cấp, và 3 bãi lều nơi các đoàn lữ khách ghé dựng bàn
  chơi theo lịch sự kiện rồi nhổ lều đi. Truyện giải thích luôn chuyện trò mở rồi đóng.
- **Lối vào nhanh giữ nguyên**: nút Máy Bi ở hàng đáy vẫn vào thẳng máy (vòng chơi chính một chạm). Trong máy có nút "Ra đảo": camera lùi từ
  mặt máy ra thành tháp giữa đảo, liền một thế giới, không mờ dần. Từ bản đồ sảnh thì đi tàu như Nhà.
- **Trò cố định** (cần tay nghề hoặc tính toán): Câu cá, Đua tướng, Chợ đen, Đấu trường ngầm. **Trò theo sự kiện** (may rủi): Blackjack,
  Roulette, Slot (câu 5).
- **Tiền cược là bi**, đúng lời dặn, không thêm tiền mới. Có trần mỗi ngày và bậc cược mở theo cấp để máy bi vẫn là chỗ tiêu bi chính.
- "Cược càng nhiều thưởng càng lớn" làm bằng hai lớp: tiền thắng tỉ lệ với tiền cược, và **Hũ bàn** đầy theo số bi đã cược (thắng hay thua
  đều đổ vào). Hũ đầy cho rương bàn; bậc cược cao thì rương có **mảnh tướng khách mời** của sự kiện.
- **Rủi ro lớn nhất là tuổi trên store** (mục 8). Blackjack, Roulette, Slot là "mô phỏng cờ bạc" khi khai bảng hỏi tuổi: Apple xếp 18+ nếu
  thường xuyên, Úc R18+ với mọi mức. Kế hoạch cửa hàng đang nhắm 12+. Phải chốt câu 1 trước mốc C7 (bàn may rủi). Các mốc trước làm được ngay.
- **Mốc** (mục 13): C0 kế hoạch → C1 lõi, dữ liệu, bản lưu, test → C2 đảo hình tạm, lối vào → C3 Câu cá → C4 Đấu trường ngầm → C5 Đua tướng
  → C6 Chợ đen → C7 bàn may rủi và lịch sự kiện → C8 hình thật → C9 cân bằng, thử máy Android. Khoảng 20 ngày làm.
- 12 câu cần chốt ở mục 14. Câu nào cũng có đề xuất.

## 1. Hiện trạng (soi code 2026-11-25)

| Phần | Đang có | Dùng lại cho đảo Casino |
|---|---|---|
| Máy bi | Scene `Machine` (`MachineScene.cs`, 1.441 dòng), lõi `Core/Pachinko.cs` (kết quả chọn trước rồi phát lại), máy bản 3, rương rig AtomSpine, đèn, jackpot (`07_MayBi.md`, `23_MayBi_TraiNghiem.md`) | Giữ nguyên, chỉ thêm nút "Ra đảo" và cảnh lùi camera |
| Sảnh | Bản đồ thế giới 5 đảo hệ, mây che đảo chưa mở (`HubIslands`, `HubFog`), tàu ở bến cạnh đảo Thủy (`PierShip`); hàng nút đáy: Cửa hàng, Tướng, **Máy Bi** (to, số bi), Sổ thẻ, Nhà | Thêm đảo Casino ở mép bản đồ sau mây; nút Máy Bi giữ |
| Nhà | Scene `Home`, lưới thoi isometric 2:1, ngày đêm, đi bằng tàu (`ShipVoyage`, liền thế giới) | Cùng phép chiếu, camera, ngày đêm, chuyến tàu |
| Trận | Trận thẻ bài luân phiên `Core/Battle`, hộp chuẩn bị `StagePrep`; Đền Huy Hiệu sinh trận từ công thức (`Core/Badges.cs`) | Đấu trường ngầm dựng `StageDef` từ bảng đội trong ngày, chạy trận thường |
| Chỉ số tướng | `HeroStats` có `spd` (cộng thẳng + cấp) | Tốc độ đua |
| Câu cá | Ao cá của Nhà: thụ động, ra bi, thẻ, hiếm ra cúp (`balance.json` khối `fish`) | Câu cá trên đảo là trò chủ động, có loài cá, không trùng Ao cá |
| Ngày | `Afk.LocalDay(now, tzMin)`, `SaveService.Now()`; giới hạn quảng cáo theo ngày (`AdGate`) | Mốc ngày cho trần lượt, đội ngầm trong ngày, lịch sự kiện |
| Cửa hàng | Bán bi, Rương Tướng, Offer Engine, popup Hết bi (`26_CuaHang_IAP_QuangCao.md`) | Chặn popup bán bi ở bàn may rủi (mục 8) |
| Tải sau | Play Asset Delivery theo hệ (`27_TaiNoiDungSau.md`) | Đảo Casino thành một gói tải sau riêng |

## 2. Cốt truyện và không khí

- **Bến Lữ Khách** nằm trên đường biển giữa năm đảo hệ. Thám hiểm gia nào đi qua cũng ghé nghỉ chân: sửa thuyền, đổi đồ, kể chuyện, thử vận.
- Tháp Máy Bi do những đoàn thám hiểm đầu tiên dựng; bi thả xuống là "bi phiêu lưu" mà cả quần đảo dùng làm tiền.
- Mỗi trò cố định có một chủ quán thường trú, gốc từ một đảo hệ:

  | Trò | Chủ quán (sinh vật kiểu thú nuôi, thiết kế sau) | Gốc |
  |---|---|---|
  | Bến câu | ông câu già, mũ rơm, kiên nhẫn | Thủy |
  | Trường đua | trọng tài cầm cờ, nói to | Hỏa |
  | Chợ đen | lái buôn đội mũ trùm, mắt sáng trong bóng tối | Kim |
  | Hầm đấu | ông trùm đấu trường, to lớn, vết sẹo | Thổ |
  | Quán trọ | bà chủ quán, giữ bảng nhiệm vụ, dẫn chuyện | Mộc |
  | Chủ bến | người chào đón lần đầu, đưa lịch lữ khách | trung lập |

- Bàn may rủi do **đoàn lữ khách ghé bến** dựng lều: tới thì cờ đuôi nheo, đèn lồng, nhạc; hết hạn thì nhổ lều đi. Lịch ghé dán trên bảng gỗ ở bến.
- Không khí: hội chợ bến cảng hơn là sòng bạc tối tăm. Ban ngày nhộn nhịp, ban đêm đèn lồng, đèn tháp máy bi sáng nhất đảo (ngày đêm theo giờ
  thật như Nhà, `DayCycle`). Nét vẽ tay bút mực, chì màu như `ArtGen/Islands/refs/world_style.png`, UI không bóng.

## 3. Bố cục đảo

Đảo cố định, không xây, không dời (khác Nhà). Dùng **isometric 2:1 như Nhà** để dùng chung camera, ngày đêm, cách gen hình theo lớp (đảo nền
trống trước, công trình là ảnh rời đặt lên). Cỡ khoảng 2 × 1,5 màn, kéo hai chiều, thu phóng 0,5–1,2 lần.

```
                 [Hầm Đấu: cửa hang dưới đồi]          ← bắc
                        |
   [Chợ đen: hẻm lều]   |        [Trường đua: vòng quanh đồi]
          \             |              /
     [Lều 1]   ── [THÁP MÁY BI] ──   [Lều 2]
          /         (quảng trường)      \
   [Bến câu: cầu gỗ]    [Lều 3]     [Quán trọ]
                        |
                [Bến tàu + bảng lịch lữ khách]          ← nam, tàu cập ở đây
```

| Chỗ | Trạng thái |
|---|---|
| Tháp Máy Bi | luôn mở (mở cùng máy bi trong hướng dẫn người mới) |
| 5 công trình cố định | **khoá**: giàn giáo phủ vải, bảng gỗ "Mở ở cấp N"; **mở**: có chủ quán đứng cửa, phần động (cờ, khói, nước); **có việc**: bong bóng trên mái (cá cắn câu, đội ngầm mới, hàng mới) |
| 3 bãi lều | **trống**: bãi cỏ có cọc; **sắp tới**: bảng "Đoàn X ghé sau 2 ngày"; **đang mở**: lều dựng, đồng hồ bút chì đếm ngược |
| Bến tàu | tàu về sảnh, bảng lịch lữ khách (sự kiện đang mở và 2 sự kiện kế) |

## 4. Lối vào và chuyển cảnh

- **Hàng nút đáy sảnh**: nút **Máy Bi** giữ chỗ và vẫn vào thẳng máy (hướng dẫn người mới không đổi, vòng chơi chính một chạm). Chấm trên nút
  thêm dấu sự kiện khi có lều đang mở mà người chơi chưa vào (câu 3).
- **Máy → đảo**: nút "Ra đảo" ở góc màn máy (hiện khi đảo đã mở). Camera lùi: chụp màn máy, thu nhỏ dần vào đúng mặt Tháp Máy Bi giữa đảo, quanh
  tháp hiện quảng trường rồi cả đảo. Ngược lại khi chạm tháp. Làm theo cách `ShipVoyage` (dải thế giới, camera bám), không mờ dần.
- **Sảnh → đảo**: đảo Casino nằm ở mép bản đồ sau mây; mở thì mây dạt, chạm đảo thì tàu đi (`ShipVoyage`, `PierShip`). Đảo → sảnh: tàu ở bến nam.
- Vào máy từ đảo thì nút quay lại của máy về đảo; vào từ sảnh thì về sảnh (`SceneRouter` nhớ màn trước).
- Thanh trên ở đảo: bi, mồi câu (khi ở Bến câu).

## 5. Mở khoá và lịch sự kiện

### 5.1. Mở dần theo tiến độ

Cấp đối chiếu: Nhà mở sau ải 2, Hang Tiềm Năng cấp 30, Sổ Phép cấp 50, cấp tối đa 200 ("vừa" tới cấp 200 khoảng ngày 46).

| Thứ | Điều kiện (đề xuất) | Lý do |
|---|---|---|
| Tháp Máy Bi | như hiện nay (sau trận thắng đầu, `Tutorial`) | không đổi hướng dẫn |
| **Đảo** (nút Ra đảo, mây dạt trên bản đồ) | cấp 8 | sau chuỗi hướng dẫn bắt buộc; người chơi đã quen máy |
| Câu cá | cùng lúc mở đảo | trò nhẹ, ít ảnh hưởng kinh tế, làm quà mở đảo |
| Đua tướng | cấp 15 và có ít nhất 4 tướng | cần đủ tướng để chọn theo địa hình |
| Bàn may rủi (lều) | cấp 20, rồi theo lịch | sau khi có thu nhập bi ổn định |
| Chợ đen | cấp 25 | túi đồ đã đủ thứ để đổi |
| Đấu trường ngầm | cấp 35 | sau Hang Tiềm Năng; đội đã đủ mạnh để đội ngầm có ý nghĩa |
| Quán trọ (nhiệm vụ đảo) | cùng lúc mở đảo | mục 6.8 |

### 5.2. Lịch sự kiện

- **Dữ liệu**: khối `casino.events` trong `balance.json`. Mỗi sự kiện: `id`, tên, lều mở (`blackjack`, `roulette`, `slot`, sau này thêm), cách lặp
  (`cycle: {periodDays, offsetDays, lengthDays}`) hoặc ngày cố định (`start`, `end`), **tướng khách mời** (mảnh trong Hũ bàn), hệ số (ví dụ
  "Lễ hội đua: thưởng đua ×1,5", "Tuần Cá Vua"), trang trí (cờ, đèn lồng theo chủ đề).
- **Lịch mặc định chạy không cần máy chủ**: tính từ ngày (vòng 14 ngày):

  | Ngày trong vòng | Sự kiện | Mở |
  |---|---|---|
  | 1–3 | Đêm Bài | lều Blackjack |
  | 5–7 | Vòng Xoay Ngũ Hành | lều Roulette |
  | 9–11 | Hội Máy Quả | lều Slot |
  | 12–14 | Lễ Hội Đua | thưởng Trường đua ×1,5, cúp tuần thêm quà |
  | 4, 8 | (nghỉ) | bảng báo đoàn kế tiếp, tạo mong chờ |

  Ngày lễ (Tết, Giáng sinh, Halloween) ghi đè bằng ngày cố định. Sau này Remote Config ghi đè cả lịch (cùng mốc S5 của cửa hàng).
- **Giờ**: theo chốt câu 9 của cửa hàng: giờ mạng khi có; không có mạng thì dùng giờ máy nhưng không mở sự kiện mới. Mốc ngày là
  `Afk.LocalDay`. Sự kiện hết giờ thì lều nhổ thật, không hồi lại ngay (đồng hồ thật, nguyên tắc 1 của `26`).
- **Bảng lịch lữ khách** ở bến: sự kiện đang mở (đếm ngược), 2 sự kiện kế (ngày tới), tướng khách mời. Chấm đỏ khi sự kiện mới mở.

## 6. Từng trò

Luật chung cho mọi trò có cược bi:
- **Bậc cược** mở theo cấp; số bi mỗi bậc nhân theo 5 bậc cấp người chơi như gói bi (×1, ×1,5, ×2, ×2,5, ×3 ở cấp 1/20/50/90/130, `26` mục 4.2).
- **Trần mỗi ngày** cho trò có thưởng (số ván, số lần nhận thưởng). Hết trần vẫn chơi được bằng "ván tập" không cược, không thưởng (câu 8).
- **Tỉ lệ công khai**: bàn may rủi có nút "Tỉ lệ" (bảng trả, tỉ lệ hoàn trả RTP) như máy bi. **Không làm suýt trúng giả** (giữ chốt `23`).
- Mọi kết quả sinh bằng `Rng` có hạt giống lưu lại (tua lại được, chống sửa bản lưu đơn giản, test được ngoài Unity).

### 6.1. Tháp Máy Bi

Máy bi đang có, không đổi luật. Chỉ thêm: nút "Ra đảo", cảnh lùi camera, và trong lúc có sự kiện thì đèn vòm đổi màu theo chủ đề sự kiện.

### 6.2. Câu cá (Bến câu)

**Chơi**, một ngón, màn dọc:
1. **Quăng**: vuốt lên, độ dài vuốt là lực quăng. Xa bờ thì cá to và hiếm hơn nhưng khó kéo hơn.
2. **Chờ**: phao nhấp nhô; cá cắn thì phao chìm, có 0,6 giây để chạm "Giật". Hụt thì mất mồi.
3. **Kéo**: thanh dọc có vùng xanh. Giữ ngón thì vùng xanh nổi lên, thả thì chìm; giữ con cá trong vùng xanh để đầy thanh kéo. Cá vùng vẫy
   theo kiểu của loài (cá hiếm giật mạnh, đổi hướng nhanh). Thanh kéo đầy là bắt được, cạn là sổng.

**Cá**: 30 loài, 6 mỗi hệ, 5 độ hiếm (Thường … Huyền thoại); mỗi con có cỡ ngẫu nhiên (S, M, L, kỷ lục). Ba chỗ câu: gần bờ, xa bờ, rạn đá
(mở theo cấp cần câu). Loài theo chỗ và theo giờ (một số loài chỉ cắn ban đêm, dùng `DayCycle`).

**Mồi**: 10 mồi miễn phí mỗi ngày; thêm từ nhiệm vụ quán trọ, mua bằng bi ở Chợ đen. Không hồi theo giờ (không thể lực).

**Thưởng**:
- Bán cá ở Chợ đen lấy bi (giá theo độ hiếm × cỡ).
- **Sổ Cá**: bắt lần đầu mỗi loài có bi; đủ 6 loài một hệ được 5 mảnh tướng hệ đó và cúp trang trí cho Nhà (dùng lại `cup_fish`); kỷ lục cỡ có
  huy hiệu.
- **Cá Vua** (một con mỗi tuần, cao điểm khi có "Tuần Cá Vua"): cá rất khó, được gọi **một tướng phụ kéo**: tướng khắc hệ cá thì vùng xanh to hơn
  25%. Thưởng: mảnh tướng, đá tiến hóa. Cho tướng có việc ngoài trận.
- Cần câu nâng 5 cấp bằng bi (vùng xanh to hơn, mở chỗ câu xa bờ, rạn đá).

**Khác Ao cá của Nhà**: Ao cá thụ động, ra bi và thẻ; Bến câu chủ động, có loài, Sổ Cá, Cá Vua. Không đổi Ao cá.

### 6.3. Đua tướng (Trường đua)

**Chơi** (người dùng đổi 2026-11-25: "random 3-5 tướng mỗi lane chạy đua nhau, trên đường chạy tướng có thể đánh nhau cho vui vui, có tướng
bị choáng stun, nó cũng kiểu random ai về nhất cho vui thôi"):
- Mỗi cuộc đua ngẫu nhiên **3–5 tướng**, mỗi tướng một làn: tướng của người chơi + tướng ngẫu nhiên của các thám hiểm gia khác. Đường đua đổi
  theo ngày: 3 chặng, mỗi chặng một địa hình theo hệ, hiện trước khi chọn tướng.
- **Tốc độ** chỉ lệch nhẹ theo chỉ số (tốc, sao, cấp: vài %), địa hình cùng hệ ×1,06, bị khắc ×0,96; dao động mỗi chặng ±8% lớn hơn, nên về
  nhất phần lớn là **hên xui**.
- **Đánh nhau**: tướng đang chạy, hết hồi chiêu (2,6 giây), có tướng khác cách ≤ 9 đơn vị thì mỗi giây 55% cơ hội lao vào húc tướng gần nhất
  (ưu tiên phía trước). Trúng (72%): đối thủ **choáng** 1,3 giây (đứng yên, sao xoay trên đầu). Hụt: kẻ húc vấp ngã 0,6 giây. Đối thủ đang có
  khiên cổ vũ: né, kẻ húc vấp. Trung bình gần 7 cú trúng mỗi cuộc, mình bị choáng khoảng 2 lần.
- **Gió thuận**: thỉnh thoảng một tướng được +30% tốc trong 1 giây.
- **Cổ vũ**: mỗi chặng một lần, vòng sáng co về khớp nút: Tuyệt +9% tốc 1,5 giây và **khiên né một cú húc** (0,9 giây), Tốt +6%, Hụt 0.
  Tướng máy cũng cổ vũ theo độ giỏi của hạng cúp.
- Mô phỏng 30 nhịp mỗi giây, tất định theo hạt giống và lần chạm; lõi ghi sự kiện (húc trúng, vấp, né, gió, về đích) để giao diện diễn.

**Hạng cúp** (mở theo cấp): Đồng, Bạc, Vàng, Kim Cương, Huyền Thoại; lệ phí theo bậc cấp. Thưởng = lệ phí × hệ số hạng × số tướng (nhất 0,55,
nhì 0,3, ba 0,1): ai cũng như nhau thì trung bình gần hoà vốn, đông tướng thì thưởng nhất to hơn. Điểm cúp 3 / 2 / 1 cho top 3; đủ 10 điểm một
hạng trong tuần thì nhận quà tuần, tuần sau đếm lại.

**Cân** (đo 4000 cuộc mỗi kiểu, `build.py run race`): không cổ vũ về nhất 21% (lời 0,83× lệ phí), cổ vũ Tốt 22% (0,86×), cổ vũ Tuyệt 31%
(1,05×); 3 tướng nhất 27–39%, 5 tướng 16–24%. Cuộc đua dài khoảng 22 giây.

**Hình**: rig tướng chưa có clip chạy. Tướng là chân dung **nhảy cóc** (nhún, nghiêng, bóp giãn do code); lao vào đối thủ khi húc, vụt nổ chỗ
trúng, lắc lư và tối màu khi choáng, chữ nổi cạnh tướng. Bụi, lửa, nước theo hệ và hình đường đua để C8; clip chạy riêng cho từng tướng để sau.

### 6.4. Chợ đen

Game chạy không máy chủ nên **đổi với lái buôn**, không đổi giữa người chơi (câu 6).

- **6 ô hàng**, đổi mới lúc 0 giờ, 8 giờ, 16 giờ. Làm mới sớm tốn 20, 40, 80 bi (tối đa 5 lần mỗi ngày). Ban đêm thêm 2 ô hàng hiếm.
- Loại ô:

  | Loại | Ví dụ | Giá |
  |---|---|---|
  | Đổi đồ thừa | bản sao thẻ thừa, mảnh của tướng đã tối đa sao → bi hoặc đá | 30–50% giá gốc |
  | Mảnh tướng đã gặp | 5 mảnh tướng X | 130–160% giá gốc, không may rủi |
  | Đá | 1 đá tiến hóa / đá tinh | 150–200% giá gốc, 1 lần mỗi ngày |
  | Đồ Nhà | trang trí hiếm, bản vẽ | bi |
  | Mồi câu | 5 mồi | bi |
  | Túi hàng lậu | túi ngẫu nhiên | bi; **công bố tỉ lệ** (là hộp may rủi) |

- Giá gốc lấy từ bảng "bi quy đổi" của cửa hàng (`26` mục 4.2), nên chợ không phá giá gói bán.
- Bán cá ở đây.

### 6.5. Đấu trường ngầm (Hầm đấu)

**Chơi**: trận thẻ bài thường (`Core/Battle`, `StagePrep`), nền riêng "hầm đấu".

- **Mỗi ngày 5 bậc**: Đá, Đồng, Bạc, Vàng, Huyền Thoại. Mỗi bậc một đội địch **do mình đặt**: tướng, cấp, sao, thẻ, kèm **luật ngày**
  (ví dụ "hệ Hỏa +20% công", "không Tuyệt kỹ", "máu gấp đôi", "chỉ 1 tướng mỗi bên") đi qua `BattleStart` như tiềm năng, đặc tính hệ.
- Cấp địch cố định theo dữ liệu, không theo cấp người chơi (ví dụ Đá 20, Đồng 45, Bạc 80, Vàng 120, Huyền Thoại 170). Bậc mở theo cấp người chơi.
- **Lệ phí** 30 / 80 / 200 / 500 / 1.200 bi (× bậc cấp), trả lúc bấm Đánh.
- **Thưởng thắng lần đầu trong ngày**: 2,5 lần lệ phí + mảnh của tướng chủ lực đội địch (1 / 2 / 3 / 5 / 8) + đá ở bậc Vàng trở lên. Thắng lại
  cùng ngày: hoàn lệ phí + quà nhỏ. Thua: mất lệ phí.
- **Chủ nhật**: thêm bậc "Nhà Vô Địch" (đội boss tuần), thưởng khung chân dung, trang trí.

**Dữ liệu đội ngầm** (`casino.underground` trong `balance.json`):
- `week[0..6]`: 7 ngày lặp, mỗi ngày 5 bậc `{name, rule, enemies: [{hero, level, star, cards}], rewardHero}`;
- `dates["2026-12-24"]`: ghi đè ngày lễ, ngày sự kiện;
- menu `PokiClash/Nhập dữ liệu` kiểm (tướng có tồn tại, cấp, luật hợp lệ) và **chạy thử bằng máy tự đánh** (`Sim.Stage`) để báo tỉ lệ thắng của đội
  mẫu mỗi bậc, giống cân Đền Huy Hiệu.
- Claude soạn sẵn 2 tuần đầu, người dùng sửa (câu 9). Sau này Remote Config đổi đội không cần ra bản mới.

### 6.6. Blackjack (lều Đêm Bài)

**Luật** (theo luật quen thuộc để ai biết blackjack chơi được ngay):
- Chia từ "hộp bài vô hạn" (trộn lại mỗi ván, không đếm bài được). Bài 52 lá, chất là 4 trong 5 hệ (đổi hình, không đổi luật).
- Dealer dừng ở 17 mềm. Blackjack trả 3:2, thắng thường 1:1, hoà trả lại. Gấp đôi (double) với hai lá bất kỳ; tách (split) một lần; không bảo
  hiểm, không đầu hàng. Nhà cái lợi khoảng 0,5% nếu chơi đúng chiến thuật cơ bản, người mới khoảng 2–4%.
- **Bậc cược**: 10 / 25 / 50 / 100 bi (× bậc cấp); bậc 3, 4 mở theo cấp. Trần 30 ván mỗi ngày.

**Cược càng nhiều thưởng càng lớn**:
- Tiền thắng tỉ lệ với tiền cược (lớp 1).
- **Hũ bàn** (lớp 2): mỗi bi đã cược đổ vào hũ (thắng hay thua đều đổ), như thanh nấm của máy bi. Hũ đầy cho rương bàn theo **bậc cược cao nhất đã
  dùng khi hũ đầy**:

  | Bậc cược | Rương bàn |
  |---|---|
  | 1 | bi |
  | 2 | bi + bản sao thẻ |
  | 3 | 2–3 mảnh tướng khách mời + bi |
  | 4 | 5 mảnh tướng khách mời, có lúc ra đá tiến hóa |

- Hũ hoàn lại khoảng 3–5% giá trị số bi đã cược (đo lại). Nhờ vậy chơi nhiều vẫn tiến dần tới mảnh tướng dù hên xui từng ván.
- **Tướng khách mời** đổi theo sự kiện, là một tướng trong bể của Rương Tướng.

**Người mới**: ván đầu không mất bi, có gợi ý "nên rút / nên dừng" theo chiến thuật cơ bản; trang "Cách chơi" (`HowToDialog`).

### 6.7. Roulette (lều Vòng Xoay Ngũ Hành) và Slot (lều Hội Máy Quả)

**Roulette**: bánh xe 26 ô = 5 hệ × số 1–5, cộng một ô **Sao Vàng** (thay ô 0).

| Cửa | Thắng khi | Trả | Hoàn trả |
|---|---|---|---|
| Hệ | rơi vào 1 trong 5 ô của hệ đó | 4:1 | 96,2% |
| Số | rơi vào 1 trong 5 ô cùng số | 4:1 | 96,2% |
| Ô đơn | đúng một ô | 24:1 | 96,2% |
| Sao Vàng | ô Sao Vàng | 24:1 + mảnh tướng khách mời | 96,2% + mảnh |

Đặt tối đa 5 chip mỗi vòng, bậc chip như Blackjack. Trần 30 vòng mỗi ngày. Có Hũ bàn.

**Slot**: 3 cuộn × 3 hàng, 5 đường. Biểu tượng: 5 ngọc hệ, bi, huy hiệu tướng, Sao (thay mọi biểu tượng), Rương (3 cái ở đâu cũng được: 5 lượt
miễn phí). Ba huy hiệu tướng khách mời trên đường giữa: thưởng lớn (×100 cược + mảnh tướng). Hoàn trả mục tiêu 95%, đo bằng mô phỏng 1 triệu
lượt trong test. Trần 50 lượt mỗi ngày; không tự quay; có "quay nhanh" (bỏ bớt animation). Có Hũ bàn.

**Cuộn dừng ở đâu**: kết quả chọn theo bảng trọng số như máy bi, rồi xếp hình trên cuộn **theo đúng phân bố thật** của từng cuộn. Không cố ý đặt
biểu tượng lớn ngay trên, dưới đường thắng (đó là suýt trúng giả).

### 6.8. Đề xuất thêm (cho phần "......")

| Trò | Ý | Cố định hay sự kiện |
|---|---|---|
| **Quán trọ** | Bảng 3 nhiệm vụ đảo mỗi ngày (câu 5 cá, đua 2 lần, thắng 1 trận ngầm…), thưởng bi, mồi, mảnh; bà chủ quán dẫn chuyện, kể tin các đảo hệ. Nối các trò với nhau | cố định |
| **Ném vòng** | Ném vòng vào tượng tướng trên kệ xoay (tay nghề, canh lúc); mỗi lượt tốn bi, trúng tượng nào nhận mảnh tướng đó | sự kiện |
| **Đập hũ hệ** | Hũ trồi lên theo hệ, chạm đúng hũ khắc hệ được đổi màu; 30 giây một lượt, điểm đổi quà | sự kiện |
| **Bói sao** | Mỗi ngày lật 1 lá miễn phí: hệ may mắn hôm nay (+10% thưởng trò của hệ đó) | cố định, rất nhẹ |

## 7. Kinh tế

**Dòng bi sau khi có đảo**:

| | Trò |
|---|---|
| Nguồn bi | ải, cây bi, Nhà, cửa hàng (như cũ); thêm: bán cá, thắng đua, thắng ngầm, nhiệm vụ quán trọ |
| Chỗ tiêu bi | máy bi (chính, như cũ); thêm: lệ phí đua và ngầm, phần lời nhà cái ở bàn may rủi, mồi, làm mới chợ, cần câu |
| Đổi bi ra sức mạnh | máy bi (chính); thêm: Hũ bàn ra mảnh khách mời, chợ bán mảnh giá cao, thưởng ngầm ra mảnh tướng |

**Luật cân**:
1. **Máy bi vẫn là chỗ đổi bi ra sức mạnh lợi nhất.** Giá trị mỗi bi ở bàn may rủi (tính cả Hũ bàn) và ở chợ phải thấp hơn ở máy bi, để không ai
   bỏ máy đi cày blackjack.
2. Trò may rủi lỗ nhẹ (hoàn trả 95–99% cộng Hũ bàn). Trò tay nghề (câu, đua, ngầm) lãi nhẹ nếu chơi tốt và đúng sức.
3. Mảnh tướng từ đảo Casino mỗi tuần có trần, khoảng 30% số mảnh từ các nguồn khác của người chơi vừa.
4. Trần lượt mỗi ngày (mục 6) giữ tổng số bi qua bàn may rủi khoảng 1–1,5 lần thu nhập bi một ngày.
5. Đo bằng `ProgressSim` thêm ba kiểu chơi đảo (không chơi, vừa, nhiều): cấp và số mảnh ở ngày 7, 30; tổng bi qua đảo; không kiểu nào lên cấp
   nhanh hơn người không chơi đảo quá 10%.

## 8. Tuổi trên store và pháp lý

Đây là quyết định phải chốt trước khi làm bàn may rủi (câu 1).

- **Apple** (bảng tuổi mới 2025: 4+, 9+, 13+, 16+, 18+; bỏ 12+, 17+): "mô phỏng cờ bạc" ở mức thường xuyên vào 18+; mức ít, nhẹ thấp hơn. Hạn
  điền bảng hỏi mới 31/1/2026.
- **Úc**: từ 9/2024 game có mô phỏng cờ bạc bị xếp **R18+** bất kể mức độ.
- **PEGI / IARC** (Google Play dùng IARC): game có trò casino thường bị nâng tuổi ở châu Âu, có game bị xếp PEGI 18.
- **Kế hoạch cửa hàng đang nhắm 12+** (`26` câu 10). Có Blackjack, Roulette, Slot thì không giữ được, và Apple cũng không còn bậc 12+.
- **Đổi vỏ không thoát được**: blackjack dùng thẻ tướng vẫn là blackjack. Bảng hỏi tuổi phải khai đúng. Đổi tên đảo cũng không đổi kết quả xếp tuổi.
- **Trò không tính là cờ bạc**: Câu cá, Đua tướng (không đặt cửa), Chợ đen (giá cố định), Đấu trường ngầm (lệ phí là phí vào trận có tay nghề),
  Quán trọ. Riêng Túi hàng lậu là hộp may rủi như Rương Tướng: công bố tỉ lệ.
- **Bi mua được bằng tiền thật** (`26`): bi mua được → cược vào may rủi → ra mảnh tướng. Thưởng là đồ trong game, không đổi ra tiền, nên hợp luật
  Google Play và Apple. Nhưng nước coi hộp may rủi trả tiền là cờ bạc (Bỉ) có thể nhìn bàn may rủi cùng cách: dùng chung cờ theo nước trong
  Remote Config với Rương Tướng để tắt lều may rủi ở nước đó.
- **Chơi có trách nhiệm** (hợp nguyên tắc của `26`, giảm rủi ro):
  - ở bàn may rủi **không bật popup Hết bi, Bổ Sung Bi**, không gạ mua bi; hết bi thì chỉ báo và mời đi chỗ khác;
  - mỗi bàn hiện "Hôm nay đã cược / đã thắng"; có trần ngày; không tự quay;
  - hiệu ứng thắng tỉ lệ với số thắng thật (thắng ít thì kêu nhỏ, như máy bi).

## 9. Bản lưu

**Không đổi số phiên bản**: thêm khoá tuỳ chọn `casino` như `home`; bản lưu không có khoá vẫn đọc bình thường.

| Phần | Lưu gì |
|---|---|
| Chung | đã xem truyện mở đảo, trò đã mở, đã xem hướng dẫn từng trò |
| Theo ngày | mã ngày, số ván / lượt / lần nhận thưởng từng trò, tổng đã cược và đã thắng hôm nay |
| Hũ bàn | mức hũ và bậc cược cao nhất từng bàn |
| Câu cá | mồi, cấp cần câu, Sổ Cá (loài → số con, cỡ kỷ lục), Cá Vua tuần này |
| Đua | điểm cúp từng hạng trong tuần, mã tuần |
| Chợ | hạt giống hàng, lần làm mới, ô đã mua trong lượt |
| Ngầm | bậc đã thắng hôm nay, Nhà Vô Địch tuần |
| Sự kiện | sự kiện đã báo, đã nhận quà mở màn |
| Thống kê | tổng đã cược / đã thắng từ trước tới nay (hiện trong Sổ tay) |

## 10. Code

| Việc | Chỗ |
|---|---|
| Luật chung: mở khoá, lịch sự kiện, mốc ngày, trần, Hũ bàn, bậc cược | `Core/Casino.cs` |
| Dữ liệu | khối `casino` trong `Assets/02 Data/Json/balance.json`, đọc bằng `Core/CasinoConfig.cs` qua `BalanceConfig.casino` (như `HomeConfig`); menu `PokiClash/Nhập dữ liệu` kiểm `CasinoConfig.Validate` |
| Từng trò (C# thuần, không phụ thuộc Unity) | `Core/Casino/Blackjack.cs`, `Roulette.cs`, `Slots.cs`, `Race.cs`, `Fishing.cs`, `BlackMarket.cs`, `Underground.cs` |
| Bản lưu | `SaveData.casino` |
| Cảnh đảo | scene `Casino`, `SceneIds.Casino`; `App/Scenes/Casino/CasinoScene.cs`; dùng lại `LandView`, `HubPan`, `DayNight`, `IslandAnim` |
| Màn từng trò | prefab màn toàn màn hình mở trong scene `Casino` (không thêm scene cho mỗi trò): `Screens/Casino/BanBai`, `VongXoay`, `MayQua`, `DuongDua`, `BenCau`, `ChoDen`; Hầm đấu đi qua `StagePrep` → scene `Battle` → về `Casino` |
| Máy → đảo | nút "Ra đảo" trong `MachineScene`; `App/CasinoZoom.cs` (lùi, tiến camera liền thế giới) |
| Sảnh | đảo Casino trên bản đồ (`HubIslandArt`, mây `HubFog`), tuyến tàu (`PierShip`, `ShipVoyage`); chấm sự kiện trên nút Máy Bi |
| Cửa hàng | `Offers`: không bật popup bán bi khi đang ở bàn may rủi; cờ theo nước tắt lều may rủi |
| Chữ | mọi chữ qua `Loc.T` (`24_DaNgonNgu.md`) |
| Test | `Tests/CasinoTests.cs`: hoàn trả Blackjack (chiến thuật cơ bản), Roulette, Slot bằng mô phỏng 1 triệu ván (lệch dưới 0,5%), trần ngày, lịch sự kiện qua mốc ngày và giờ mạng, đua tất định theo hạt giống và lần chạm, bản lưu đọc ghi; chạy ngoài Unity bằng csc + mono |
| Cân | menu `PokiClash/Cân bằng nhanh/Đảo Casino: hoàn trả, dòng bi, mảnh` (`BalanceWindow`) |
| Thử | menu `PokiClash/Thử/Đảo Casino/…` (đang Play): tua ngày, ép sự kiện, mở hết, đủ bi; **sao lưu bản lưu đầu lượt, trả lại cuối lượt** |
| Prefab | menu `PokiClash/Prefab/Đảo Casino/…` theo luật "mọi thứ là prefab" |
| Tải sau | gói tải sau riêng `casino` (khoảng 10–15 MB), tải ngầm sau đảo đầu (`27_TaiNoiDungSau.md`) |

## 11. Hình, âm thanh

**Hình** (gen sau khi chốt kế hoạch; qua Magnific, dưới 100 credit mỗi ảnh, hoặc gói file prompt GPT `ArtGen/Casino/build_casino.py` theo luật
ArtGen trong `CLAUDE.md`):

| Nhóm | Ảnh | Ghi chú |
|---|---|---|
| Đảo nền trống | 1 (bản 2k) | isometric 2:1 như Nhà; gen trước, công trình đặt sau (gen theo lớp) |
| Tháp Máy Bi | 1 | cùng ngôn ngữ với máy bản 3: vòm đỏ, ống vàng, bóng đèn |
| 5 công trình cố định + quán trọ | 6 mở + 6 khoá (giàn giáo phủ vải) | |
| 3 lều sự kiện | 3 + bãi trống | lều bài, lều vòng xoay, lều máy quả |
| Chủ quán | 6 | sinh vật kiểu thú nuôi theo luật hình tướng (tô phẳng, không bóng); đứng yên đợt đầu |
| Màn trò | nền bàn bài, bánh xe, khung máy quả, nền bến câu, 5 nền địa hình đua, nền hầm đấu | |
| Biểu tượng | tờ 9 biểu tượng slot, tờ 30 cá (2 tờ), chip | lá bài dựng bằng code (khung + số + icon hệ) |

Khoảng 45 ảnh, khoảng 4.500 credit. Ngày đêm: đảo nhuộm theo giờ như Nhà, đèn lồng và đèn tháp có lớp sáng đêm.

**Âm thanh**: nền bến cảng ban ngày, nhạc hội chợ ban đêm; tiếng chip, chia bài, bánh xe, cuộn quay, phao, dây câu, cổ vũ đua (dùng `SfxSynth` cho
tiếng ngắn).

## 12. Người mới

- Lần đầu ra đảo: truyện tranh 3 khung (`ComicPanel`): thuyền ghé Bến Lữ Khách, chủ bến chào, chỉ Tháp Máy Bi ("cái máy bạn đã quen") và Bến câu.
- **Lượt câu đầu chắc chắn trúng**, vào Sổ Cá ngay. Các ô khoá hiện bảng "Mở ở cấp N".
- Mỗi trò mới mở: thông báo, chấm đỏ trên đảo và nút Máy Bi, lượt đầu có hướng dẫn (`GuideOverlay`), ván đầu bàn may rủi không mất bi.
- Trang "Cách chơi" cho từng trò. Thêm bước vào `25_FTUE.md` (gợi ý theo lúc, không bắt buộc).

## 13. Các mốc

| Mốc | Việc | Ra gì để duyệt | Ước lượng |
|---|---|---|---|
| **C0** | Kế hoạch này, chốt câu hỏi | file này | |
| **C1** | `CasinoConfig`, `Casino.cs` (mở khoá, lịch, mốc ngày, trần, Hũ bàn), bản lưu, test | test đạt | 1,5 ngày |
| **C2** | Scene `Casino` bằng hình tạm: bố cục, ô khoá / mở / lều, nút Ra đảo và cảnh lùi camera, đảo trên bản đồ + tàu, truyện mở đảo | chạy thử, ảnh chụp | 2,5 ngày |
| **C3** | Câu cá: quăng, giật, kéo, 30 loài (icon tạm), Sổ Cá, mồi, cần câu, Cá Vua | chạy thử | 2 ngày |
| **C4** | Đấu trường ngầm: dữ liệu đội theo ngày, luật ngày, lệ phí, thưởng, Nhà Vô Địch, kiểm bằng máy tự đánh | chạy thử, bảng tỉ lệ thắng | 1,5 ngày |
| **C5** | Đua tướng: mô phỏng, cổ vũ, hạng cúp, quà tuần, tướng nhảy cóc | chạy thử, số thắng theo mô phỏng | 2 ngày |
| **C6** | Chợ đen + Quán trọ (nhiệm vụ đảo) | chạy thử | 1,5 ngày |
| **C7** | Blackjack, Roulette, Slot, Hũ bàn, lịch sự kiện đầy đủ, bảng lịch lữ khách, chặn popup bán bi, cờ theo nước (**sau khi chốt câu 1**) | chạy thử, test hoàn trả | 3 ngày |
| **C8** | Gen hình thật: đảo, công trình, lều, chủ quán, màn trò; ngày đêm | tờ soi hình | 3–4 ngày (gồm chờ duyệt) |
| **C9** | Cân bằng bằng `ProgressSim`, thử máy Android (đọc được, nhịp, hiệu năng), gói tải sau | bảng đo, ảnh máy thật | 1,5 ngày |

Thứ tự: trò tay nghề trước (không dính tuổi store, dùng được ngay), bàn may rủi sau khi chốt câu 1. C3–C6 độc lập với nhau, làm song song được
(nhiều agent biên dịch ngoài Unity, không giành Unity).

## 14. Câu cần chốt

1. **Bàn may rủi và tuổi store** (mục 8): làm Blackjack, Roulette, Slot và nhận tuổi cao hơn (Apple có thể 18+, Úc R18+, PEGI có thể nâng), hay bỏ ba
   bàn này, chỉ giữ trò tay nghề? Đề xuất: **làm, nhưng chỉ mở theo lịch sự kiện** (không thường trực), khai bảng hỏi đúng thực tế, đổi mục tiêu tuổi
   của `26` cho hợp, có cờ theo nước để tắt.
2. **Tiền cược**: bi trực tiếp (theo lời dặn) hay thêm xu riêng của đảo? Đề xuất: **bi trực tiếp**, có trần ngày và bậc cược theo cấp. Thêm xu không
   giảm được rủi ro tuổi mà thêm một loại tiền (`26` nguyên tắc một loại tiền).
3. **Lối vào máy bi**: nút Máy Bi vẫn vào thẳng máy, có nút "Ra đảo" (đề xuất); hay nút đổi thành "Đảo Casino" và vào đảo trước, chạm tháp mới vào máy
   (thêm một chạm cho vòng chơi chính)?
4. **Tên đảo trong game**: "Đảo Casino", hay tên truyện "Bến Lữ Khách" (đề xuất, hợp chất sổ tay phiêu lưu), hay tên khác?
5. **Trò nào cố định, trò nào theo sự kiện**: đề xuất cố định: Máy bi, Câu cá, Đua tướng, Chợ đen, Đấu trường ngầm, Quán trọ; theo sự kiện: Blackjack,
   Roulette, Slot, và các trò lều thêm sau (Ném vòng, Đập hũ).
6. **Chợ đen**: chỉ đổi với lái buôn (đề xuất, chạy không máy chủ); đổi giữa người chơi cần máy chủ, tài khoản, chống gian, để sau?
7. **Đua tướng**: tướng của mình chạy, có nút cổ vũ (đề xuất); hay chỉ đặt cửa cho tướng máy chạy (thêm một trò may rủi)?
8. **Trần lượt mỗi ngày** cho trò có thưởng (bàn may rủi 30–50 ván, mồi 10/ngày, đua có điểm cúp tuần): chốt cũ "không dùng thể lực" có cho phép
   trần kiểu này không? Đề xuất: có, vì không chặn chơi (hết trần vẫn chơi ván tập), chỉ chặn nhận thưởng.
9. **Đội ngầm theo ngày**: lặp 7 ngày + ghi đè ngày lễ trong `balance.json`, Claude soạn 2 tuần đầu rồi người dùng sửa (đề xuất)?
10. **Cấp mở**: đảo cấp 8, Đua 15, lều 20, Chợ 25, Ngầm 35 (mục 5.1)?
11. **Lịch sự kiện mặc định** vòng 14 ngày như mục 5.2?
12. **Hình**: khoảng 45 ảnh, khoảng 4.500 credit Magnific; gen concept đảo trước để duyệt hướng (như Nhà)?

## Nguồn

- Bảng tuổi Apple: [App Store Connect, Age ratings](https://developer.apple.com/help/app-store-connect/reference/age-ratings),
  [Apple: Updated age ratings](https://developer.apple.com/news/?id=ks775ehf), [MacRumors 2025-07-25](https://www.macrumors.com/2025/07/25/apple-overhauls-app-store-age-ratings/).
- Úc R18+ cho mô phỏng cờ bạc: [Neowin](https://www.neowin.net/news/simulated-gambling-triggers-r18-rating-in-australia-for-iphone-apps/).
- Google Play, IARC: [Content ratings](https://support.google.com/googleplay/android-developer/answer/188189),
  [Gambling policy](https://support.google.com/googleplay/android-developer/answer/9877032); ca bị xếp PEGI 18:
  [Kotaku](https://kotaku.com/balatro-luck-landlord-google-play-store-gambling-mobile-1851731303).
- Trong dự án: `07_MayBi.md`, `21_Nha_Home.md`, `23_MayBi_TraiNghiem.md`, `25_FTUE.md`, `26_CuaHang_IAP_QuangCao.md`, `27_TaiNoiDungSau.md`.

## Tiến độ

### C1 xong (2026-11-25): lõi, dữ liệu, bản lưu, test

- **Code** (C# thuần, `Assets/01 Script/Core`):
  - `CasinoConfig.cs`: cấu hình khối `casino` (lớp `[Serializable]` như `HomeConfig`), `Validate(GameData)`; menu `PokiClash/Nhập dữ liệu` gọi kiểm.
  - `Casino.cs`: `CasinoState` (bản lưu khoá `casino`, không đổi số phiên bản), mở theo cấp / số tướng, lịch sự kiện (vòng lặp từ
    `anchor`, ngày cố định đè vòng lặp cùng lều), tướng khách mời theo lần mở, trần lượt theo ngày, bậc cược × `ShopConfig.Band`,
    Hũ bàn, trao thưởng (`*guest`, `*elem:<hệ>`, mồi), Bói sao, Quán trọ, chấm đỏ.
  - `Casino/Blackjack.cs`, `Roulette.cs`, `Slots.cs`, `Race.cs`, `Fishing.cs`, `BlackMarket.cs`, `Underground.cs`.
  - Sửa nhỏ: `RewardKind.Bait`, `SaveData.casino`, `BalanceConfig.casino`.
- **Dữ liệu**: khối `casino` trong `balance.json`, sinh bằng script (cá, lịch, cúp, chợ, 14 ngày × 5 bậc đội ngầm + Nhà Vô Địch chủ nhật).
  Bản dịch tiếng Anh thêm vào `Resources/Loc/en/ui.json`, `names.json`.
- **Số đo** (máy tự chơi, ngoài Unity):

  | Trò | Kết quả |
  |---|---|
  | Blackjack | chiến thuật cơ bản hoàn trả 99,6% (1 triệu ván); người mới "rút tới 15" 94,5% |
  | Roulette | mọi cửa 25/26 = 96,2% |
  | Máy quả | tính chính xác 95,5%; trúng 40% lượt (hai Rương chỉ hoàn cược; bản đầu trúng 98% là kiểu "lỗ mà tưởng thắng", đã bỏ); lượt miễn phí 1,8% |
  | Đua | chọn tướng hợp địa hình trong 6 tướng + cổ vũ khá: Đồng thắng 59% (lời 1,5× lệ phí), Vàng 25% (1,0×), Huyền Thoại 8% (0,5× ở cấp mở hạng); không cổ vũ, chọn bừa thì lỗ. Chỉ số tốc chỉ lệch ±5% để địa hình và cổ vũ quyết định |
  | Đấu trường ngầm | cấp từng đội dò bằng máy tự đánh (đội mẫu 3 tướng Hiếm / Sử thi ở cấp mở bậc): Đá ~80%, Đồng ~70%, Bạc ~55%, Vàng ~40%, Huyền Thoại ~25%, Nhà Vô Địch ~16% |
  | Câu cá | 10 mồi / ngày ở gần bờ: khoảng 100 bi / ngày gồm thưởng lần đầu, 15 loài sau 7 ngày |
- **Test**: `Tests/CasinoTests.cs` 21 test, đạt cả ngoài Unity (csc + mono) và trong Unity. Toàn bộ EditMode trong Unity: `LocTests` báo
  thiếu bản dịch chuỗi mới (đã thêm); còn `PrefabOnlyTests` hỏng ở `HeroUnlockView.cs`, `CardBend.cs` (việc của phiên khác, không thuộc
  phần này). Ngoài Unity, `TutorialTests` và `PachinkoTests` hỏng y hệt trên code trước khi có Casino (bộ chạy ngoài thiếu `TestContext`).

### C2 xong (2026-11-25): màn đảo bằng nền tạm, lối vào từ máy bi

- **Concept đảo** (câu chốt 12): hai tờ Magnific GPT 2.6 ở `ArtGen/Casino/concept/` (A quảng trường giữa đảo, B đảo vành khuyên quanh hồ;
  95 credit mỗi tờ). **Chờ người dùng chọn hướng** trước khi gen nền thật và công trình rời (C8).
- **Màn** `Screens/Casino` + scene `Casino` (Build Settings), dựng bằng menu `PokiClash/Prefab/Đảo Casino/Đảo: dựng màn`
  (`Editor/CasinoSceneMenu.cs`; cờ `Temp/casino_build.flag`): chép từ `Screens/Cave`, thay bằng `CasinoScene`; nền tạm là concept A
  (`Assets/03 Art/Casino/casino_map_tam.png`, nhập 2048) phủ theo chiều cao màn, kéo ngang bằng `HubPan` (giới hạn 0,83 màn, kéo dư 170 / 260).
- **Điểm chạm** `Items/DiemCasino` (`CasinoSpot`): 10 điểm neo theo khung công trình trên ảnh (Tháp Máy Bi, Bến câu, Trường đua, Chợ đen,
  Hầm đấu, Quán trọ, 3 bãi lều, bảng lịch ở bến). Bảng tên có dòng trạng thái ("Mở ở cấp 35", "Cần 4 tướng để mở", "10 mồi",
  "Đổi hàng sau 05:40", "Đêm Bài · còn 05:40", "Vòng Xoay ghé sau 2 ngày"), khoá, chấm đỏ.
- **Hàng nút đáy**: Bói sao (lật hệ may mắn trong ngày), Lịch lữ khách (sự kiện đang mở, khách mời, 2 sự kiện kế), Về sảnh. Lần đầu ra
  đảo hiện truyện mở đảo; trò mới mở báo một lần.
- **Máy bi ↔ đảo**: `SceneIds.Casino`; `MachineScene` có nút "Ra đảo" (hiện khi đảo đã mở, menu `Máy bi: nút Ra đảo`), vào máy từ
  đảo (`args = SceneIds.Casino`) thì nút quay lại về đảo. Chuyển cảnh tạm dùng mây chung; cảnh lùi camera từ mặt máy ra tháp để C8.
- **Trò**: chạm trò đã mở gọi `CasinoGames.Open` (màn từng trò đăng ký vào đây ở C3–C7); chưa có màn thì báo "Trò này đang được dựng".
  Quán trọ, lịch lữ khách tạm dùng hộp thông báo.
- **Chưa làm ở C2**: đảo trên bản đồ sảnh và tuyến tàu (cần hình đảo, làm cùng C8).
- **Kiểm**: lượt chụp `PokiClash/Thử/Đảo Casino/Đảo: chụp màn đảo và máy bi (đang Play)` (cờ `Temp/casino_tour.flag`, sao lưu bản lưu),
  ảnh `Temp/PokiShots/casino/`. Test trong Unity: `CasinoTests`, `LocTests`, `SaveTests` đạt; `PrefabOnlyTests` còn lỗi cũ ở file của
  phiên khác.
- Script số liệu và máy chạy thử ngoài Unity cất ở `ArtGen/Casino/so_lieu/` (README trong đó).

### C8 bước 1 (2026-11-25): hình đảo hướng B theo lớp

Người dùng chọn hướng B, rồi dặn "gen đảo trống rồi gen riêng các công trình lên đó, đặt lên". Làm ở `ArtGen/Casino/lop/` (README trong đó):
- Đảo trống và lớp công trình gen "đúng chỗ đúng cỡ" từ concept B (công trình nằm đúng vị trí trên nền trong suốt), phóng classic 2k,
  cắt từng công trình theo cụm điểm ảnh: tháp, hang, chợ, khán đài + hàng rào đường đua, quán trọ, bến câu, bến tàu, 3 cọc bãi lều.
  3 lều sự kiện gen rời, thu vừa bãi. Tốn 95 × 3 + 72 × 2 = 429 credit (mỗi lần dưới 100).
- Màn đảo dùng hình thật: đảo trống 2048 x 1360 hiện 1:1 (nét), công trình là Image đúng khung, lều bật khi sự kiện của lều đang mở,
  điểm chạm lấy khung từ ảnh công trình. Nền tạm `casino_map_tam.png` đã xoá.
- Lỗi gặp: bản sao prefab trong `Casino.unity` giữ giá trị đè cũ của khung nền (khung từng giãn theo màn) nên lúc chạy khung có chiều cao
  âm, ảnh dùng chất liệu giấy bị bỏ mặt sau thành vô hình. Menu dựng màn giờ trả bản sao trong scene về đúng prefab mỗi lần dựng.
- Còn lại của C8: đèn đêm cho công trình (mặt nạ tự sáng như Nhà), đảo trên bản đồ sảnh + tuyến tàu, cảnh lùi camera từ mặt máy ra tháp,
  hình cá, nền màn câu thật, nền hầm đấu, chủ quán.

### C3 xong bản đầu (2026-11-25): Bến câu

- Scene `CasinoPlay` (`SceneIds.CasinoPlay`, Build Settings) cho các trò tương tác, mỗi trò một tấm dựng sẵn trong `Screens/CasinoPlay`
  (menu `PokiClash/Prefab/Đảo Casino/Trò: dựng màn chơi`, `Editor/CasinoPlayMenu.cs`); `CasinoGames.Open` chuyển sang đây, quay lại về đảo.
- Tấm Bến câu (`FishingPanel`): vuốt lên mặt nước để quăng (thanh lực), chờ phao, chạm khi hiện "!", giữ / thả để kéo vùng xanh theo cá
  (thanh kéo bên phải, vòng kéo đầy là bắt được, cạn là sổng), tấm kết quả (tên, độ hiếm, cỡ, lần đầu / kỷ lục, thưởng, giá bán), Sổ Cá 30 ô
  (loài chưa bắt hiện "???"), mua mồi, bán cá, nâng cần câu, 3 chỗ câu. Lượt câu đầu đời chắc trúng. Cá Vua: tự gọi tướng khắc hệ cá phụ kéo.
- Hình tạm: nền cắt từ concept (khúc hồ có bến câu), cá là chấm màu hệ viền màu độ hiếm, cần câu là thanh gỗ. C8 thay ảnh.
- Lượt chụp `PokiClash/Thử/Đảo Casino/Bến câu: quăng, kéo, Sổ Cá (đang Play)` (cờ `Temp/casino_fish_tour.flag`), ảnh `Temp/PokiShots/casino_cau/`.

### C4 xong bản đầu (2026-11-25): Đấu trường ngầm

- Hộp `Dialogs/HamDau` (`UndergroundDialog`, menu `PokiClash/Prefab/Đảo Casino/Hầm đấu: dựng hộp`, đăng ký vào kit): các bậc hôm nay
  (Nhà Vô Địch chỉ chủ nhật), luật ngày, đội địch (tên, cấp, sao), thưởng thắng lần đầu, nút Đánh (lệ phí) hoặc cấp mở; nút Đổi đội dùng
  hộp chọn đội chung.
- Trận đi qua luồng trận có sẵn như Hang Tiềm Năng: `BattleArgs.ug` (`UgRef`: bậc, ngày lúc bấm Đánh); `BattleController` dựng đội địch
  bằng `Underground.Enemy`, áp luật ngày cho cả hai đội, giới hạn số tướng khi luật "mỗi bên một tướng", ải giả `Underground.Stage`
  (nền theo hệ tướng chủ lực, bậc Vàng trở lên là trận boss), độ epic theo bậc; kết trận `UndergroundResult` (bi, mảnh chủ lực, quà bậc;
  "Đánh lại", "Về Hầm đấu" mở lại hộp trên đảo).
- Lượt chụp: cờ `Temp/casino_ug_tour.flag` (mở hộp, bấm Đánh bậc đầu, chụp trận), ảnh `Temp/PokiShots/casino_ham/`.

### Người dùng dặn thêm (2026-11-25, sau C8 bước 1)

- **Nút giữa thanh dưới (Máy Bi) → tàu đi chếch sang trái ra đảo Casino**, có bến tàu, mây vây quanh, đổi màu theo giờ. Đổi câu chốt 3
  (trước: nút vào thẳng máy). Đảo chưa mở (dưới cấp 8) thì nút vẫn vào thẳng máy bi như cũ (hướng dẫn người mới không đổi).
- **Tách từng công trình** để sau thay hình / bảo trì riêng.
- **Mỗi trò một scene** (trước: scene chung CasinoPlay).

### C8 bước 2 (2026-11-25): chuyến tàu sảnh ↔ đảo, bến, mây, ngày đêm, công trình rời, scene riêng từng trò

- `ShipVoyage`: thêm tuyến Hub → Casino (đi lên, dạt trái 380 đơn vị trong mây) và Casino → Hub (xuôi xuống, dạt phải); dải thế giới vẫn
  dọc như tuyến Nhà nên ảnh hai màn, mây toả quanh tàu vẫn nối liền. Nút giữa thanh dưới của sảnh đi tuyến này.
- Bến tàu đảo: ảnh bến gen lại không có thuyền (đúng chỗ đúng cỡ, `ArtGen/Casino/lop/thay_ben_tau.py`), con tàu của game (`ShipBuild.Pier`)
  đậu ở mặt nước trước đầu trái bến, ra / vào phía nam; chạm tàu là về sảnh. Vành mây rời quanh đảo (`CloudRing`, dùng lại
  `HomeSceneMenu.BuildClouds`, chừa lối ở bến); sáng tối theo giờ (`DayNight` như Nhà). Giao diện đảo có `CanvasGroup` để chuyến tàu ẩn đi.
  Truyện mở đảo, thông báo trò mới chờ tàu cập bến rồi mới hiện.
- Ảnh đảo nối dài 400 px biển ở đáy (`noi_bien.py`, lát mảng thuần biển) để không lộ ranh; khung đảo neo sát dưới thanh trên.
- Mỗi công trình là một vật `ct_<mã>` có `CasinoBuilding` (mã, ảnh), ảnh riêng `casino_ct_<mã>.png`, khung riêng trong `casino_art.json`:
  đổi hình một công trình chỉ cần thay file đó rồi chạy menu dựng màn.
- Bến câu thành scene riêng `CasinoFishing` (`FishingScene`, `Screens/CasinoFishing`, menu `Bến câu: dựng scene`; đổi tên từ CasinoPlay giữ
  GUID); `CasinoGames.SceneOf` chọn scene theo trò. Đua, Blackjack, Roulette, Slot sẽ mỗi trò một scene.
- Lượt chụp chuyến tàu: cờ `Temp/casino_voyage_tour.flag`, ảnh `Temp/PokiShots/casino_tau/`. Các lượt chụp tự đặt
  `Application.runInBackground` (Unity nằm nền thì vòng game đứng).

### C5 xong bản đầu (2026-11-25): Trường đua (scene riêng)

- Scene `CasinoRace` (`RaceScene`, `Screens/CasinoRace`, menu `PokiClash/Prefab/Đảo Casino/Trường đua: dựng scene`, `Editor/CasinoRaceMenu.cs`).
- Hàng 5 hạng cúp (khoá theo cấp), dòng điểm cúp tuần + lượt có thưởng (+ Lễ Hội Đua), đường hôm nay (3 chặng theo hệ, tô màu dải chặng),
  sân 6 làn với chấm tướng màu hệ (tướng mình viền vàng), tướng mặc định là tướng hợp địa hình nhất, Chọn tướng (hộp chọn đội chung, 1 ô),
  Đua (lệ phí; hết lượt có thưởng là đua tập), Cổ vũ (vòng sáng co về khớp nút trong 1 giây: lệch < 0,13 s Tuyệt, < 0,32 s Tốt; quá 1,35 s
  tự tính Hụt), kết quả (hạng, bi, điểm cúp; Đua lại / Xong), Nhận quà tuần.
- Hình tạm (dải màu, chấm); C8 thay hình đường đua, tướng nhảy cóc. Lượt chụp: cờ `Temp/casino_race_tour.flag`, ảnh `Temp/PokiShots/casino_dua/`.

### Sửa sau C8 bước 2 (2026-11-25): mặt nạ ngày đêm, biển hai đảo nối liền

- Người dùng báo "bug mask": lớp tối ban đêm chỉ phủ khung ảnh đảo, kéo bản đồ quá mép thì lộ cạnh. Sửa: lớp `sang_toi` phủ rộng ±3000, vật
  ngoài khung không bị tối hai lần, giới hạn kéo đúng theo cỡ ảnh, đệm (0, 80). Đã kiểm bằng lượt kéo bản đồ.
- Người dùng: "phần biển của 2 đảo phải nối nhau, tôi thấy có sự khác nhau về màu sắc". Sửa: tách biển thành lớp riêng `bien` (tấm vân biển
  dùng chung của chuyến tàu `Ship/tau_bien.png`, lát lặp) đưa vào `DayNight` như biển sảnh nên tối cùng nhịp; ảnh đảo `casino_dao.png` chỉ còn
  đất, chỗ nước trong suốt (`ArtGen/Casino/lop/doi_bien.py`, thay `noi_bien.py`). Đã soi ngày và đêm trong lượt chụp chuyến tàu.

### C5 làm lại (2026-11-25): Trường đua 3–5 tướng, đánh nhau, choáng

- Lõi `Core/Casino/Race.cs` viết lại theo luật mục 6.3 (số tướng ngẫu nhiên, húc / vấp / né / gió, sự kiện `RaceEvent`); `RaceConfig` thay
  `runners`, `place` bằng `minRunners`, `maxRunners`, `fightRate`, `fightRange`, `fightCool`, `hitChance`, `stunSec`, `trip`, `guardSec`,
  `gustRate`, `gust`, `gustSec`, `placeK`. Số trong `balance.json` (`gen_casino.py`). Test: `Dua_TatDinh_3Den5Tuong_DanhNhauChoang`,
  `Dua_Choang_DungYen`, `Dua_LePhi_Thuong_DiemTuan` (22 test Casino đạt ngoài Unity và trong Unity).
- Màn `RaceScene` + `CasinoRaceMenu`: sân cao hơn, dựng sẵn 5 làn, chia lại đều theo số tướng; mỗi làn chân dung tướng (prefab kit) nhảy cóc,
  tên dưới chân (tướng mình đỏ, có ★), sao choáng bay vòng quanh đầu, vụt nổ, chữ nổi Choáng! / Vấp! / Né! / Gió thuận! cạnh tướng (gần đích thì
  sang trái), số hạng khi về đích; vạch xuất phát, vạch đích ca rô; dòng tường thuật dưới sân; trước khi đua hiện 4 làn mẫu (đối thủ là bóng sẫm).
  Kết quả có bảng xếp hạng cả đoàn (húc trúng, bị choáng). Rời màn giữa cuộc đua đã trả lệ phí thì chạy nốt và tính thưởng.
- Lượt chụp chụp thêm chuỗi khung ngay sau cú húc đầu (`2b_danh_0..3`).
