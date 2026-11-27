# 37. Giả lập round test UA: 30 ngày đầu của một chiến dịch nhỏ

Kế hoạch 2026-11-27. **Trạng thái: chờ người dùng nhắn "chạy"** (người dùng dặn: làm xong các việc nhỏ khác thì nhắn mới chạy).
Chưa sửa code, chưa chạy gì.

## 1. Mục tiêu

Round test đầu: chi ít tiền quảng cáo, vài trăm đến vài nghìn install, đo retention, CPI, tỉ lệ nạp, ROAS. Giả lập trước để:

1. **Biết trước khoảng số sẽ thấy** (P10 / P50 / P90): CPI, D1 / D3 / D7 / D14 / D30, tỉ lệ nạp, ARPDAU, ROAS D0–D30, LTV D90 / D180,
   theo thị trường và ngân sách.
2. **Chọn ngân sách test**: cần bao nhiêu install để số đo đủ tin.
3. **Đặt ngưỡng đi tiếp / sửa / dừng** trước khi chạy, không đặt sau khi thấy số.
4. **Chỉ ra chỗ gãy**: retention tụt ở ngày nào, ứng với tường ải nào, hết nội dung gì (lấy từ lõi game).
5. **Sau test**: nạp số D1–D7 thật, hiệu chỉnh, dự báo D30 / D90 / D180, chấm độ chính xác của chính mô hình.

Độ chính xác kỳ vọng (ước lượng, chưa đo; "trúng" = số thật trong ±20% quanh dự báo):

| Lúc dự báo | Retention D1–D30 | Tỉ lệ nạp | ROAS D30 | Luật game (tường, hết nội dung, kinh tế) |
|---|---|---|---|---|
| Trước test (chỉ có số ngành) | 30–40% | ~25% | 10–20% | ~90% |
| Sau test, có D1–D7 thật | 65–75% | 50–60% | 40–50% (ngân sách $2k) | ~90% |

Lý do ROAS thấp: test nhỏ thì chính số đo thật cũng nhiễu. Đã tính (4.000 lần, game giả định D1 30%, D7 9%, D30 3%, nạp 2,3%,
ARPPU 30 ngày $8 đuôi dài, CPI $1,35): $1.000 / 740 install / ~17 người nạp → D1 ±9%, D7 ±19%, D30 ±35%, **ROAS D30 ±110%**;
$2.000 → ±7 / ±14 / ±24 / ±87%; $5.000 → ±4 / ±9 / ±16 / ±58%. Round 1 nên quyết bằng retention và tỉ lệ nạp, không bằng ROAS.

## 2. Số liệu đầu vào (prior)

PokiClash nằm giữa RPG (thu thập, nuôi tướng, đánh ải) và casual / casino (máy bi, đảo Casino). Lấy bảng RPG làm tâm, Puzzle / Casino
làm biên. Việt Nam không có trong bảng retention của AppsFlyer: dùng Indonesia làm đại diện Đông Nam Á.

| Chỉ số (Android, người từ quảng cáo) | Việt Nam | Đông Nam Á (ID / PH) | Brazil | Mỹ | Nguồn |
|---|---|---|---|---|---|
| CPI RPG | $1,35 | $1,07 / $1,12 | $0,87 | $8,95 | AppsFlyer Q3 2026 |
| CPI Strategy / Puzzle (biên) | $0,62 / $0,22 | $0,88 / $0,26 (ID) | $1,09 / $0,49 | $11,17 / $4,81 | AppsFlyer Q3 2026 |
| D1 / D7 RPG | (lấy ID) | 31,8% / 9,3% (ID) | 23,3% / 6,9% | 29,3% / 10,1% | AppsFlyer Q3 2026 |
| D1 / D7 Puzzle (biên trên) | (lấy ID) | 33,6% / 10,4% (ID) | 29,2% / 9,2% | 29,2% / 11,1% | AppsFlyer Q3 2026 |
| Tỉ lệ nạp 30 ngày RPG | (lấy ID) | 2,33% (ID) | 2,45% | 7,69% | AppsFlyer Q3 2026 |
| D30 (cả ngành) | trung vị 0,7–0,8%, top 25% 1,6–1,8%, top 1% 13–15% | | | | GameAnalytics 2026 |
| ROAS F2P | D7 15–25%, D30 40–60%; IAP hoà vốn 90–180 ngày | | | | Playio, Liftoff (blog nhà quảng cáo) |

Còn thiếu, tra lúc chạy (bước B4): eCPM quảng cáo thưởng theo thị trường; ARPPU 30 ngày theo thị trường (mới có D90 IAP ARPPU
midcore $9,80 toàn cầu của AppsFlyer); đường retention D14 / D30 theo thể loại. Không tra được thì để prior rộng và ghi rõ.

Mọi prior là một khoảng (phân phối), không phải một số. Ví dụ D1 Đông Nam Á: tâm 30%, P10–P90 khoảng 20–40%.

## 3. Cách làm: hai lớp

### Lớp A: máy giả lập lõi (đã có, `ArtGen/KinhTe/gia_lap/`)

Chạy bộ số mới `T0_round_test` (không sửa gì, là game lúc chạy, ghi mã commit): 300 người × 90 ngày, khoảng 5 phút ở 6 tiến trình.
Mỗi người ra một quỹ đạo từng ngày nếu **không bỏ game**: cấp, ải, ngày kẹt, tường, bi, quảng cáo, USD.

Thêm vài trường mỗi ngày vào JSON kết quả (sửa `runner/EconSim.cs`, `Program.cs`, không đụng `Assets`): số trận thua, có qua ải mới
không, có gặp tường không, hết bi / hết việc để làm, số popup gạ mua, số cơ hội quảng cáo. Đã có sẵn: `level`, `cleared`, `adsCum`,
`usdCum`, `sessionsCum` theo ngày.

### Lớp B: `chien_dich.py` (mới, Python thuần, vài giây mỗi kịch bản)

1. **Install**: N = ngân sách / CPI. CPI = prior thị trường × hệ số video quảng cáo (log-normal, P10–P90 ×0,5–×2).
2. **Gán người**: mỗi install lấy quỹ đạo của một ô lớp A theo tỉ trọng, không chạy lại lõi:
   - mức chơi chăm / vừa / ít: prior 15 / 35 / 50%;
   - nhóm tiền theo tỉ lệ nạp của thị trường: người không trả tiền ~97–98% (Đông Nam Á) / ~92% (Mỹ), chia trong người nạp
     P1 / P2 / P3 khoảng 70 / 25 / 5%. (Lớp A chia đều 300 người thành 5 nhóm tiền, nên phải đặt lại trọng số.)
3. **Bỏ game**: xác suất bỏ mỗi ngày = đường nền × hệ số sự kiện.
   - Đường nền: power-law / Weibull khớp prior D1 / D7 / D30 của thị trường.
   - Hệ số sự kiện lấy từ quỹ đạo lớp A: số ngày liền không qua ải mới, thua liên tiếp, hết việc để làm trong phiên. Đây là giả định
     yếu nhất, để prior rộng (×1 đến ×3 khi kẹt 3 ngày) và báo độ nhạy riêng.
   - Bỏ game không đổi những ngày trước đó, nên cắt quỹ đạo 90 ngày tại ngày bỏ là đúng, không cần đưa xác suất bỏ vào lõi.
4. **Nạp tiền**: thời điểm và món mua theo quỹ đạo lớp A (nạp đầu, Vượt Mốc, gói lúc gặp tường), tổng tiền co theo ARPPU prior của
   thị trường (log-normal đuôi dài, có cá voi). Người không nạp thì không mua.
5. **Quảng cáo**: số quảng cáo mỗi ngày từ lớp A × eCPM thị trường.
6. **Hai tầng ngẫu nhiên**: (a) rút một bộ prior (1.000 lần), (b) trong mỗi bộ rút từng install (nhiễu mẫu của N người). Kết quả là
   P10 / P50 / P90 cho từng chỉ số từng ngày.
7. **D90 / D180**: từ quỹ đạo 90 ngày + đường retention; D180 = D90 × hệ số prior (lấy tỉ lệ D180 / D30 của ngành, 2–2,5 lần).

Tự kiểm trước khi tin kết quả:
- tắt hệ số sự kiện thì lớp B phải tái tạo đúng prior D1 / D7 / D30;
- N rất lớn thì khoảng nhiễu mẫu co về gần 0;
- bảng nhiễu mẫu khớp bảng đã tính ở mục 1;
- tổng USD 30 ngày của người nạp không vượt ngân sách persona của lớp A.

## 4. Kịch bản

- Thị trường: Việt Nam, Đông Nam Á (ID / PH), Brazil, Mỹ. Android (iOS để sau).
- Ngân sách: $1.000, $2.000, $5.000.
- Độ nhạy: retention prior ±; hệ số bỏ game khi kẹt ×1 / ×2 / ×3; CPI ×0,5 / ×2; có / không quảng cáo thưởng lúc test.

## 5. Đầu ra

`ArtGen/KinhTe/gia_lap/ket_qua/round_test_<thị trường>.md` và mục 8 của file này:

- bảng P10 / P50 / P90 theo ngày cho retention, tỉ lệ nạp, ARPDAU, ROAS lũy kế, LTV D90 / D180;
- bảng ngân sách → số install → độ rộng khoảng của từng chỉ số;
- ngưỡng đi tiếp / sửa / dừng (mục 6), chốt bằng phép tính hoà vốn của thị trường đã chọn;
- chỗ gãy: ngày retention tụt mạnh nhất và lớp A cho biết lúc đó người chơi đang kẹt ở đâu;
- **bản dự báo đóng băng** (ngày, mã commit, prior): giữ nguyên để chấm khi có số thật.

## 6. Ngưỡng đi tiếp / sửa / dừng (bản nháp, chốt lại sau khi chạy)

Đông Nam Á, Android, theo bảng ngành ở mục 2:

| Chỉ số | Đi tiếp | Sửa rồi test lại | Dừng / xem lại lõi |
|---|---|---|---|
| D1 | ≥ 30% | 25–30% | < 25% |
| D7 | ≥ 10% | 6–10% | < 6% |
| D30 | ≥ 3% | 1,5–3% | < 1,5% |
| Tỉ lệ nạp 30 ngày | ≥ 2% | 1–2% | < 1% |
| ROAS D30 | chỉ xem, không quyết ở round 1 (ngân sách nhỏ quá nhiễu) | | |

Muốn hoà vốn trong 180 ngày, ROAS D30 cần khoảng 40–50%. Con số này giả định D180 gấp 2–2,5 lần D30, là quy tắc kinh nghiệm, chưa đo
trên game mình.

## 7. Điều kiện để round test thật đo được (ngoài giả lập)

Soát 2026-11-27: `Packages/manifest.json` chưa có SDK đo lường, quảng cáo hay IAP. `ShopService.ShopLog` chỉ ghi file ở bản dev (chừa
chỗ cho Firebase). `Store.Pay` ở bản dev là cửa hàng giả lập. Trước khi chạy test thật phải có:

| Cần | Để làm gì |
|---|---|
| MMP (AppsFlyer hoặc Adjust) | CPI, install, ROAS theo từng chiến dịch, từng video quảng cáo |
| Analytics (Firebase hoặc GameAnalytics) | retention, phiên, phễu |
| Google Play Billing (Unity IAP) | doanh thu nạp thật, gửi sang MMP |
| Mediation quảng cáo thưởng (AppLovin MAX hoặc AdMob) | doanh thu quảng cáo theo người (nếu bật quảng cáo lúc test) |

Sự kiện tối thiểu, đặt tên khớp đầu vào lớp B để hiệu chỉnh được: từng bước FTUE, bắt đầu / thắng / thua ải (kèm số ải), gặp tường,
vào máy bi, mở popup gạ mua, mua (gói, giá), xem quảng cáo (chỗ), bắt đầu / kết thúc phiên, đảo Casino.

Việc này nằm ngoài kế hoạch giả lập; làm khi người dùng chốt ngày chạy test.

## 7b. Các bước khi người dùng nhắn "chạy"

| Bước | Việc | Ghi chú |
|---|---|---|
| B1 | Nhắn phiên quản CPU (assets-a7) trước khi chạy 300 người; tạo `bo_so/T0_round_test.py` (không sửa gì), ghi mã commit | Theo luật ≤ 6 tiến trình |
| B2 | Thêm trường mỗi ngày vào runner; biên dịch; chạy thử 6 người | Không đụng `Assets` |
| B3 | Chạy lớp A: 300 người × 90 ngày | ~5 phút |
| B4 | Tra nốt prior còn thiếu (eCPM, ARPPU theo thị trường); viết `chien_dich_prior.py` (bảng số kèm nguồn) và `chien_dich.py` | |
| B5 | Tự kiểm (mục 3) | Sai thì sửa trước khi báo |
| B6 | Chạy kịch bản + độ nhạy; ghi `ket_qua/`, mục 8 file này, một dòng vào `simulation/README.md`; đóng băng bản dự báo | |
| B7 | Báo người dùng: bảng ngắn, ngưỡng, độ chính xác, ngân sách đề xuất | |
| Sau test | `hieu_chinh.py`: nạp bảng D0–D7 thật (install, còn chơi, người nạp, doanh thu, chi phí), khớp lại đường retention, dự báo D30 / D90 / D180, so với bản đóng băng | Khi có số thật |

Câu nên hỏi người dùng lúc bắt đầu (không chặn; không trả lời thì chạy cả 4 thị trường × 3 ngân sách): thị trường định test, ngân
sách, Android hay cả iOS, có bật quảng cáo thưởng lúc test không.

## 8. Kết quả

(chưa chạy)

## 9. Giới hạn nói trước

- Tỉ lệ chịu mua, bỏ game khi kẹt, CPI theo video quảng cáo là giả định: chúng là đầu vào của mô hình, không phải thứ mô hình đo ra.
- Game đang được các phiên khác sửa (Hang Tiềm Năng, cửa hàng…): kết quả gắn với mã commit lúc chạy.
- Lớp A còn tính gần đúng Đền Huy Hiệu, Hang Tiềm Năng, công trình Nhà (xem `simulation/README.md` mục 5).
- Không có số retention công khai của Clash of Critters, Capybara Go, Legend of Mushroom; chỉ có doanh thu Critters (suy ra ~$2,4 mỗi
  lượt tải, game hit của Lilith, không dùng làm mốc).

## Nguồn

- [GameAnalytics: Mobile and PC Game Benchmarks 2026](https://gamedevreports.substack.com/p/gameanalytics-mobile-and-pc-game)
- [GameAnalytics: Mobile Gaming Benchmarks 2025](https://gamedevreports.substack.com/p/gameanalytics-mobile-gaming-benchmarks)
- [AppsFlyer: Gaming app market benchmarks Q3 2026](https://www.appsflyer.com/?p=549948)
- [Admiral Media: Mobile game marketing benchmarks](https://admiral.media/mobile-game-marketing-benchmarks/)
- [Liftoff: What is a good ROAS? 2026](https://liftoff.ai/?p=35616)
- [Playio: D7 ROAS benchmarks](https://blog.playio.co/d7-roas-benchmarks-mobile-games)
- [Playio: ARPPU và tỉ lệ nạp](https://blog.playio.co/arppu-mobile-games)
- [Liftoff: All LTV models are wrong](https://liftoff.ai/?p=30224)
- [Game Growth Advisor: Soft launch guide](https://gamegrowthadvisor.com/blog/2025-12-16-mobile-soft-launch-complete-guide/)
- [PocketGamer.biz: deltaDNA về thời gian soft launch](https://www.pocketgamer.biz/sponsored-article-deltadna-retention/)
