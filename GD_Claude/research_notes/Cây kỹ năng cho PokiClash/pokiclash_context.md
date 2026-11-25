# Bối cảnh tiến trình của PokiClash: chỗ nào hợp để thêm cây kỹ năng

Ghi chú nghiên cứu cục bộ (chỉ đọc file trên đĩa), 2026-11-24. Nguồn là tài liệu `D:/PokiClash/GD_Claude/*.md`, code `D:/PokiClash/Assets/01 Script/Core/*.cs` và dữ liệu `D:/PokiClash/Assets/02 Data/Json/*.json`. Số dòng ghi theo bản đọc hôm nay; "≈" là số dòng ước theo đầu mục. Nhiều con số trong GD được ghi kèm ngày đo; số mới nhất thắng số cũ, chỗ nào hai nguồn lệch nhau thì ghi rõ.

## 1. Vòng chơi lõi là gì (trận thẻ bài, đảo/ải, máy bi, Nhà, Cây bi, cửa hàng/trứng, tướng tiến hóa, thẻ riêng)?

### Takeaway
Vòng lõi: đánh ải (trận thẻ bài luân phiên) → nhận bi → thả bi vào máy bi (pachinko) → ra EXP và rương → lên cấp tài khoản (cũng là cấp của mọi tướng), nâng thẻ, lên sao, tiến hóa tướng → đánh ải khó hơn. Xung quanh vòng này có thu nhập thụ động (Cây bi, công trình ở Nhà, AFK) và các side meta (Đền Huy Hiệu, Tiềm năng/Hang, Nhà).

### Cited Findings
- GDD gốc: "Đánh ải nhận ball, dùng ball để chơi pachinko dropball, nhận thưởng từ đó để nâng cấp pet, lên level pet => đi săn các quái cao cấp hơn"; boss/mini boss có cơ hội rơi mảnh tướng; ải đã qua thì AFK được — [GDD game Pokiwar L5](<D:/PokiClash/GD_Claude/GDD game Pokiwar 409be130bc608044bfafe24dd01b8ff9.md>)
- Trang "Cách chơi" trong game: "Thắng ải → bi. Thả bi vào Máy Bi → kinh nghiệm, rương. Lên cấp, nâng tướng → đánh ải khó hơn." — [25_FTUE.md L352](<D:/PokiClash/GD_Claude/25_FTUE.md>)
- Lõi đổi từ xếp khối (Block Blast) sang **thẻ bài** theo GDD từ 2026-10-31: mỗi lượt chọn 1 trong 3 thẻ, chọn 5 lần, đánh luân phiên; Chiêu và Tuyệt kỹ không tốn lượt chọn, chỉ tốn mana và nộ — [README.md L41-49](<D:/PokiClash/GD_Claude/README.md>); [cfg.picks 5, cfg.offer 3 trong balance.json](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Lộ trình Unity: mốc 0–4 là vòng lõi chơi được (đánh ải → bi → máy bi → nuôi tướng), mốc 5–6 làm vòng lõi bền và đo được, mốc 7–9 là side meta của GDD (Huy hiệu, Tiềm năng, Trang trại), mốc 11 là Cây bi — [12_KeHoach_OpenSpec.md L11-30](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- **5 đảo chơi song song**, mỗi đảo 70 ải (350 ải), cấp địch tăng theo độ sâu trong từng đảo; boss cuối: Thủy 195, Hỏa 198, Kim 200, Mộc 190, Thổ 196 — [14_HeThongAi.md ≈L231-244](<D:/PokiClash/GD_Claude/14_HeThongAi.md>)
- Ải tướng ở ải 1, 5, 10, 15, 20 rồi mỗi 10 ải; ải xen giữa có tướng cường hóa, nhóm 2–3 con, lính không thu thập được — [12_KeHoach_OpenSpec.md ≈L348](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- Máy bi: chạm để thả, giữ để thả liền; ô ra EXP, cốc ra rương; chạm nấm đủ 25 lần ra quà; cược ×N tốn N bi mỗi lần thả, thưởng ×N ("chỉ nhanh hơn, không lời hơn") — [25_FTUE.md L357-358](<D:/PokiClash/GD_Claude/25_FTUE.md>)
- Nhà (thay Trang trại từ 2026-11-18): đảo giáp biển, xây công trình, giao tướng làm việc ra bi/gỗ/quặng, mở ô rừng theo cấp người chơi và cấp Nhà chính; Cây bi dời vào Nhà — [21_Nha_Home.md L5-17, L103-131](<D:/PokiClash/GD_Claude/21_Nha_Home.md>)
- Cửa hàng: bán bi, trứng (5 bậc theo độ hiếm, nở 12–16 mảnh của một tướng), vé chọn tướng, gói định kỳ; trứng còn rơi từ rương máy bi — [26_CuaHang_IAP_QuangCao.md L208-224, L684-700](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>)
- Mỗi tướng là một dòng tiến hóa (2–3 hình), lên sao/tiến hóa thì đổi hình; mỗi tướng có 3 thẻ riêng (chiêu, tuyệt kỹ, nội tại) nâng cấp bằng bản sao thẻ — [12_KeHoach_OpenSpec.md L75-79](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>); [Progress.cs L27, L62-87](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>)
- Tướng nhận được (khởi đầu, tặng, đủ mảnh, mốc Huyền thoại) luôn ở sao 1, dạng 1 — [12_KeHoach_OpenSpec.md L260-263](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)

### Inferences
- Mọi đường tiến trình cuối cùng quy về sức mạnh trong trận thẻ bài, và **cấp tài khoản là trục chính** (EXP chỉ đến từ máy bi và rương). Cây kỹ năng gắn vào cấp/EXP sẽ chạm thẳng vào vòng lõi. Gắn vào tài nguyên side meta thì chạm vòng lõi ít hơn.
- Máy bi là "cái phễu" chính: mọi thu nhập thụ động đổ ra bi, bi thành EXP. Cây kỹ năng mà có nút kinh tế (thêm bi, thêm EXP) sẽ làm lệch thẳng các mục tiêu nhịp đã cân rất kỹ (mục 2).

### Gaps
- Chưa đọc `07_MayBi.md` và `11_BanWeb_TheBai.md` trọn bài, chỉ trích phần kinh tế mỗi bi. Luật trận chi tiết (thứ tự thẻ chạy, hồi sinh) lấy từ trang "Cách chơi", chưa soát với `Battle.cs`.

## 2. Đang có những lớp tiến trình nào? Mỗi lớp tốn gì, cho gì, nhanh tới đâu?

### Takeaway
Có bảy lớp đang chạy: cấp tài khoản 1–200 (cũng là cấp tướng), sao/tiến hóa của từng tướng (20 sao trong 4 bậc, hiện theo số hình), cấp 3 thẻ riêng (1–5), Tiềm năng (6 ô ngẫu nhiên), Đền Huy Hiệu (5 dãy × 10 bậc), ô đội (1/60/200), Nhà (10 cấp Nhà chính, công trình cấp 1–7). Thêm vào đó là thu nhập thụ động (Cây bi, AFK theo ải, quảng cáo, quà ngày). Mục tiêu nhịp chốt 2026-11-24: người chơi "vừa" đạt cấp 200 khoảng ngày 46. Tướng mạnh nhất tối đa sao khoảng ngày 58 (số đo 11-17).

### Cited Findings
**Cấp tài khoản (= cấp mọi tướng)**
- "Cấp của bạn là cấp của mọi tướng. Kinh nghiệm chỉ đến từ Máy Bi và rương. Lên cấp mở thêm thẻ vào bộ." — [25_FTUE.md L360](<D:/PokiClash/GD_Claude/25_FTUE.md>); GDD: "Cấp của người chơi sẽ chính là cấp của tướng" — [GDD L19](<D:/PokiClash/GD_Claude/GDD game Pokiwar 409be130bc608044bfafe24dd01b8ff9.md>)
- Cấp tối đa 200; EXP lên cấp kế = `expBase × lv^expPow` = 45 × cấp (`expPow` 1,0); tổng tới cấp 200 là 895.500 EXP — [balance.json progression](<D:/PokiClash/Assets/02 Data/Json/balance.json>); [Progress.cs L29](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>); [14_HeThongAi.md ≈L161-180](<D:/PokiClash/GD_Claude/14_HeThongAi.md>)
- Sức theo cấp nhân dồn `1,03^(cấp−1)` (`lvStep` 0,03): cấp 40 ×3,2, cấp 200 ×360 — [HeroStats.cs L2-3, L48](<D:/PokiClash/Assets/01 Script/Core/HeroStats.cs>); [14_HeThongAi.md ≈L165](<D:/PokiClash/GD_Claude/14_HeThongAi.md>)
- Ở cấp tối đa, EXP thừa bị chặn (`s.exp = Math.Min(s.exp, ExpToNext(...))`), không đổi ra thứ gì — [Progress.cs L36-43](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>)
- Thẻ chung (75 thẻ) mở dần theo cấp ở 45 mốc riêng biệt: dày ở cấp 1–13, thưa từ cấp 60 (62, 68, 75, 78, 85, 95, 100, 110, 120, 130, 140, 150, 160, 175, 190) — [cards.json pool, trường unlock](<D:/PokiClash/Assets/02 Data/Json/cards.json>)
- Nhịp chốt 2026-11-24 (người dùng duyệt "dời bi từ cây sang trận"): "chăm" cấp 200 ngày 33, "vừa" ngày 46 (bi ải 26% tổng bi, khoảng 46 bi mỗi trận thắng), "ít" cấp 87 ở ngày 30. Mục tiêu: "vừa" khoảng ngày 45, bi ải ≥ 25%, "ít" ≥ cấp 80 ngày 30 — [12_KeHoach_OpenSpec.md ≈L464-468](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- Ba kiểu người chơi của mô phỏng: Chăm 6 lần × 5 trận/ngày, Vừa 3 × 3, Ít 1 × 2 (không xem quảng cáo) — [ProgressSim.cs L47-51](<D:/PokiClash/Assets/01 Script/Core/ProgressSim.cs>)

**Sao và tiến hóa (từng tướng)**
- Thang 20 sao tổng: Đồng 1–5, Bạc 6–10, Vàng 11–15, Kim Cương 16–20. Lên sao trong bậc tốn **mảnh của chính tướng**. Tiến hóa (sao cuối bậc → bậc sau) tốn **đá tiến hóa** và cần cấp người chơi — [StarTier.cs L1-15](<D:/PokiClash/Assets/01 Script/Core/StarTier.cs>); [Progress.cs L89-188](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>)
- Giá mảnh (tướng Khá) theo bậc: Đồng 4/6/8/12, Bạc 14/18/22/26, Vàng 28/34/40/48, Kim Cương 40/50/60/70 (tổng 480), nhân theo độ hiếm 0,8/1/1,15/1,3/1,5. Tiến hóa 20/55/120 đá, cần cấp 30/95/150 — [20_TangDayNoiDung.md L99-100](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>); [balance.json progression.shardCost/evoStones/evoLevel](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Hệ số sao: `tierPower` 1 / 1,25 / 1,55 / 1,9 × (1 + 0,025 × sao trong bậc). Mỗi sao +2,5%, mỗi lần tiến hóa +11–14%; tối đa ×2,09 — [20_TangDayNoiDung.md L31, L98](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>); [HeroStats.cs L38-44](<D:/PokiClash/Assets/01 Script/Core/HeroStats.cs>)
- **Bậc theo dạng** (2026-11-19): số bậc hiện ra = số hình của dòng. Tướng 2 dạng chỉ có Đồng, Bạc, tiến hóa một lần (20 đá); bên trong vẫn là thang 20 sao — [StarTier.cs L44-52](<D:/PokiClash/Assets/01 Script/Core/StarTier.cs>); [20_TangDayNoiDung.md L27-39](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Số đo nhịp sao (ProgressSim 60 ngày, đo 2026-11-17, trước khi có "bậc theo dạng" và trước lần cân 11-24), ngày tướng mạnh nhất đạt mốc: Chăm Bạc 1 ngày 5, Vàng 1 ngày 19, KC 1 ngày 38, KC 5 ngày 58; Vừa 8/21/37/58; Ít Bạc 1 ngày 25 — [20_TangDayNoiDung.md L110-116](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Mảnh của tướng đã tối đa sao đổi thành bản sao thẻ — [Progress.cs L258-271](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>)

**Thẻ riêng của tướng (chiêu, tuyệt kỹ, nội tại)**
- Mỗi thẻ lên cấp bằng bản sao: `cardReq` [0, 2, 4, 8, 15], `cardMax` 5, tức 29 bản sao mỗi thẻ, 87 mỗi tướng; độc lập với sao — [balance.json progression](<D:/PokiClash/Assets/02 Data/Json/balance.json>); [Progress.cs L64-81](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>)
- Sức thẻ mỗi cấp: `cardLvStep` 0,15; thẻ cấp 5 ×1,6 — [balance.json cfg](<D:/PokiClash/Assets/02 Data/Json/balance.json>); [14_HeThongAi.md ≈L299](<D:/PokiClash/GD_Claude/14_HeThongAi.md>)
- Bản sao thẻ đến từ rương máy bi, rương mốc đảo, rương AFK, mảnh dư; rương chỉ ra thẻ của tướng đã có — [Progress.cs L217-247](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>); [12_KeHoach_OpenSpec.md L65](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)

**Tiềm năng (Potential) + Hang Tiềm Năng**
- 6 ô mỗi tướng, mở ở sao tổng 1, 3, 6, 8, 11, 16. Khai phá tốn đá tiềm năng (1 đá mỗi ô quay, khoá tối đa 3 ô, mỗi ô khoá +2 đá), kết quả chờ chọn giữ mới/giữ cũ. Đá tinh thay phần đá: mọi ô ra từ Hiếm trở lên — [Potential.cs L1-11](<D:/PokiClash/Assets/01 Script/Core/Potential.cs>); [balance.json potential](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- 10 loại dòng: Công/Thủ/Máu % (trần 30%), chí mạng, hút máu, mana đầu trận, nộ đầu trận, khiên đầu trận, giảm sát thương, né. Có 3 bộ (Cuồng Chiến, Kiên Thành, Phong Ảnh) cho thưởng khi đủ 3/5 dòng cùng nhóm. Tốc bị bỏ (trọng số 0) — [balance.json potential](<D:/PokiClash/Assets/02 Data/Json/balance.json>); [20_TangDayNoiDung.md L123, L157-160](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Hang Tiềm Năng mở ở cấp 30; 10 tầng (cấp 29–195); 3 lượt thắng mỗi ngày (+1 bằng quảng cáo); boss theo thứ trong tuần; thắng tầng mới thì có đá tinh/đá tiến hóa — [Progress.cs L431-433](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>); [balance.json cave](<D:/PokiClash/Assets/02 Data/Json/balance.json>)

**Đền Huy Hiệu (Badges)**
- Mở khi thắng mini boss đầu (ải 20) của một đảo bất kỳ. 5 dãy theo hệ × 10 bậc (Đồng … Thần Thoại), 78 trận mỗi dãy, địch cấp 66–205. Mỗi trận chấm 1–3 sao, cứ 30 sao một mốc quà — [Badges.cs L1-10](<D:/PokiClash/Assets/01 Script/Core/Badges.cs>); [20_TangDayNoiDung.md L120-122](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Thưởng: tướng cùng hệ +5%…+16% Máu/Công/Thủ theo bậc cao nhất; bậc 6–10 cộng thêm cho cả đội (0,5–2%). Đặc tính hệ từ bậc 4/6/8/10: Kim "Lưỡi Kim" chí mạng, Mộc "Nhựa Sống" hút máu, Thủy "Màng Nước" khiên đầu trận, Hỏa "Hỏa Nộ" nộ đầu trận, Thổ "Giáp Đất" giảm sát thương — [balance.json badges](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Đo năm 2026-10-31: huy hiệu +20% nâng tỉ lệ thắng ở cấp đề nghị thấp nhất Thủy 49% → 69%, Thổ 59% → 73% — [12_KeHoach_OpenSpec.md L187-192](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- Gộp lại: side meta (huy hiệu + tiềm năng) ở mức "vừa" bằng khoảng +4–5 cấp ở ải đảo, mức trần khoảng +13–14 cấp — [20_TangDayNoiDung.md L125](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)

**Ô đội**
- Ô đội mở theo cấp người chơi: `SlotLevels = {1, 60, 200}` (1 tướng lúc đầu, ô 2 ở cấp 60, ô 3 ở cấp 200); có từ 2 ô thì đổi tướng được ở đầu lượt — [Progress.cs L331-345](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>); [25_FTUE.md L363](<D:/PokiClash/GD_Claude/25_FTUE.md>). Các bản cũ (mở theo số đảo đã xong; 1/10/30) đã bị thay — [12_KeHoach_OpenSpec.md ≈L301-306](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>); [15_TuongKhoiDau.md ≈L255](<D:/PokiClash/GD_Claude/15_TuongKhoiDau.md>)
- Ải từ cấp 60 được cộng thêm cường hóa để bù ô đội thứ 2 — [14_HeThongAi.md ≈L246-262](<D:/PokiClash/GD_Claude/14_HeThongAi.md>)

**Nhà (Home)**
- Nhà chính 10 cấp, cấp người chơi cần: 0/10/25/40/60/80/100/125/150/175; giá từ 60 gỗ tới 3.200 gỗ + 1.100 quặng; mở công trình, chỗ tướng (4 → 14), đội thợ (1 → 2) — [balance.json home.levels](<D:/PokiClash/Assets/02 Data/Json/balance.json>); [21_Nha_Home.md L133-153](<D:/PokiClash/GD_Claude/21_Nha_Home.md>)
- Công trình làm ra đồ: Ruộng rau (Thổ), Vườn cây (Mộc) ra bi; Xưởng gỗ (Mộc) ra gỗ; Ao cá (Thủy) ra bi, thẻ chiêu thường, cúp; Mỏ (Thổ) ra quặng và ít đá tiến hóa; Lò rèn (Kim) rèn quặng thành đá tiềm năng (5 quặng/đá), cấp cao ra đá tinh; Bếp (Hỏa) làm bánh cho tướng hết nghỉ. Mỗi công trình nâng cấp 1–7 — [21_Nha_Home.md L103-131](<D:/PokiClash/GD_Claude/21_Nha_Home.md>); [balance.json home.orePerStone 5, evoPerOre 0,008](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Chỗ ra bi không phình: 3 chỗ lúc đầu, thêm ở cấp 40, 70, 96, 120, 144 — [21_Nha_Home.md ≈L150](<D:/PokiClash/GD_Claude/21_Nha_Home.md>); [balance.json farm.spotLevels](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Trang trí có điểm đẹp: mốc 10/30/60/100/160 cho quà một lần, tướng nghỉ nhanh hơn 5% mỗi bậc; "Điểm đẹp không đụng tới sức mạnh trong trận" — [21_Nha_Home.md L164-173](<D:/PokiClash/GD_Claude/21_Nha_Home.md>)

**Thu nhập thụ động, AFK, quảng cáo**
- Cây bi (chốt 2026-11-24): 4 bi/giờ, chứa 96 (đủ 24 giờ), cây 2–5 mở ở cấp 10/25/45/70 — [balance.json trees](<D:/PokiClash/Assets/02 Data/Json/balance.json>); [12_KeHoach_OpenSpec.md ≈L466](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>). Lệch: trang "Cách chơi" và tài liệu Nhà còn ghi 5 bi/giờ, chứa 50, mở ở cấp 30/50/80/110 (số cũ) — [25_FTUE.md L365](<D:/PokiClash/GD_Claude/25_FTUE.md>); [21_Nha_Home.md ≈L127](<D:/PokiClash/GD_Claude/21_Nha_Home.md>)
- Bi ải (chốt 2026-11-24): 1 + 1 mỗi ải sâu hơn (ải 70: 70 bi); lần đầu thắng boss +24, mini boss +12, ải tướng +2 — [Progress.cs L293-303](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>); [balance.json stageBalls](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- AFK theo ải: tối đa 12 giờ; mỗi giờ 40% ra 1 mảnh của tướng rơi ở ải đó; rương AFK 3 giờ/rương, khay 4, mở sau 2 giờ; tăng tốc ×2 trong 2 giờ — [balance.json afk](<D:/PokiClash/Assets/02 Data/Json/balance.json>); [12_KeHoach_OpenSpec.md ≈L370-377](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- Trần quảng cáo thưởng mỗi ngày: tree_double 3, afk_chest_open 4, afk_boost 3, farm_boost 3, cave_extra 1, home_speed 3, free_balls 5, free_egg 1, battle_retry 3, win_double 5, chest_upgrade 3, daily_gift 1 — [balance.json ads.limits](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Quỹ Phiêu Lưu (gói trả tiền) là một **dải thưởng theo mốc cấp** (cấp 10, 15, 20, 25…; phần free 100 bi, phần trả tiền bi, trứng, đá tiến hóa); kế hoạch có làm pass (mốc S6) — [balance.json shop.fund](<D:/PokiClash/Assets/02 Data/Json/balance.json>); [26_CuaHang_IAP_QuangCao.md L11-25](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>)

### Inferences
- **Không có cấp riêng của từng tướng**: cấp là cấp tài khoản. Trục riêng của tướng là sao/tiến hóa, cấp thẻ và tiềm năng. Cây kỹ năng "theo tướng" sẽ thành trục riêng thứ tư.
- Sau cấp 60, phần lớn lần lên cấp chỉ cho +3% chỉ số, vì từ cấp 60 tới 200 chỉ còn khoảng 15 mốc mở thẻ chung (Ô 3 ở cấp 200, Nhà cấp 9–10 ở 150/175). Các lần lên cấp giữa và cuối game "trống" phần thưởng có tính chọn lựa.
- Sau khoảng ngày 46 (cấp 200), EXP từ máy bi thành vô dụng (bị chặn). Rương máy bi vẫn ra bản sao thẻ, trứng, đá nên bi vẫn còn chút giá trị, nhưng trục cấp đã hết.
- Mọi lớp hiện có đều là **chỉ số cộng thẳng hoặc quay ngẫu nhiên** (tiềm năng). Chưa lớp nào cho người chơi **chọn một trong nhiều nhánh** để đổi cách chơi.

### Gaps
- Không tìm thấy số đo nhịp sao/tiến hóa sau lần cân 2026-11-24 và sau "bậc theo dạng" (11-19). Bảng ngày Bạc/Vàng/KC ở trên có thể đã cũ.
- Chưa đọc `Home.cs` và `Trees.cs` để biết Kho, Giếng, Cối nước làm sức chứa/năng suất ra sao trong code. Số Nhà lấy từ GD và `balance.json`.

## 3. Tiền tệ, tài nguyên và chỗ tiêu: đồng nào thiếu chỗ tiêu, giai đoạn nào trống?

### Takeaway
Tài nguyên đang có: bi, EXP, mảnh tướng (theo tướng), bản sao thẻ (theo thẻ), đá tiến hóa, đá tiềm năng, đá tinh, gỗ, quặng, bánh, trứng. **Không có vàng/xu, cũng không có tiền cứng (kim cương).** Có ba chỗ dư rõ: EXP sau cấp 200 (bị bỏ), đá tiến hóa (nguồn tính cho 195 đá mỗi tướng nhưng tướng 2 dạng chỉ cần 20), và bản sao thẻ/mảnh của tướng đã tối đa. Chỗ tiêu vô hạn duy nhất đang có là quay tiềm năng.

### Cited Findings
- Các trường trong bản lưu: `level`, `exp`, `balls`, `ballsSpent`, `heroes` (mỗi tướng `owned`, `shards`, `star`, 3 thẻ `lv`/`copies`), `potentialStones`, `evoStones`, `potentialCrystals`, `caveFloor`, `badgeGifts` — [SaveData.cs L13-21, L70-89](<D:/PokiClash/Assets/01 Script/Core/SaveData.cs>). Nhà thêm `wood`, `ore`, `bread` — [Home.cs ≈L46-47, L69](<D:/PokiClash/Assets/01 Script/Core/Home.cs>)
- "Chưa thêm tiền cứng (kim cương)": bán thẳng bằng tiền thật, vật phẩm là bi, trứng, vé chọn tướng — [26_CuaHang_IAP_QuangCao.md ≈L222-224](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>). GD ban đầu có "vàng + kinh nghiệm" để lên cấp, nay code không có vàng — [06_Tuong_NuoiDuong.md ≈L16](<D:/PokiClash/GD_Claude/06_Tuong_NuoiDuong.md>); [SaveData.cs L70-89](<D:/PokiClash/Assets/01 Script/Core/SaveData.cs>)
- Bảng giá gốc (bi quy đổi): 1 mảnh Thường…Huyền thoại = 8/10/15/25/45; 1 đá tiến hóa 150, đá tiềm năng 25, đá tinh 100; $0,99 = 100 bi quy đổi — [26_CuaHang_IAP_QuangCao.md L226-244](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>)
- Chốt: đá tiềm năng, đá tinh không bán lẻ (chỉ có trong gói); "Mọi thứ bán được đều kiếm được bằng chơi, chỉ chậm hơn" — [12_KeHoach_OpenSpec.md L59](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>); [26_CuaHang_IAP_QuangCao.md L196-206](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>)
- **Bi**: nguồn là ải, Cây bi, ruộng/vườn/ao ở Nhà, rương, quà nấm máy bi, Đền, cửa hàng; chỗ tiêu là máy bi (và mua đồ trang trí) — [26_CuaHang_IAP_QuangCao.md L212](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>); [21_Nha_Home.md L166](<D:/PokiClash/GD_Claude/21_Nha_Home.md>)
- Kinh tế mỗi bi ở ×1: khoảng 8,4–8,8 EXP, bi hoàn 0,30–0,34, bản sao thẻ 0,07–0,09 — [07_MayBi.md L92, L116-117](<D:/PokiClash/GD_Claude/07_MayBi.md>)
- **EXP**: chỉ từ máy bi và rương; bị chặn ở cấp 200 — [25_FTUE.md L360](<D:/PokiClash/GD_Claude/25_FTUE.md>); [Progress.cs L42](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>)
- **Đá tiến hóa**: từ lần đầu qua ải tướng 1 / mini boss 3 / boss 8; qua lại mini boss 10%, boss 25%; rương mốc đảo 28 mỗi đảo; rương máy bi bạc/vàng; rương AFK; Đền/Hang; mỏ ở Nhà. "Đá tiến hóa mỗi tướng dùng ít đi (2 dạng: 20 đá thay vì 195; 3 dạng: 75; 1 dạng: 0), nguồn đá đang tính cho 195 đá mỗi tướng nên sẽ dư. Chưa chỉnh nguồn đá (chờ người dùng quyết)" — [20_TangDayNoiDung.md L38, L101-105](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Hiện có 44/50 tướng 2 dạng, 5 tướng 3 dạng, 1 tướng 1 dạng — [heroes.json, đếm `forms`](<D:/PokiClash/Assets/02 Data/Json/heroes.json>)
- **Đá tiềm năng / đá tinh**: nguồn là rương máy bi (bạc 8% 1–2 đá, vàng 12% 2–4 đá), rương AFK 5%, Hang, Đền, Lò rèn; chỗ tiêu là quay tiềm năng (lặp vô hạn) — [balance.json pachinko.chests, afk.chest](<D:/PokiClash/Assets/02 Data/Json/balance.json>); [Potential.cs L165-205](<D:/PokiClash/Assets/01 Script/Core/Potential.cs>)
- **Mảnh tướng**: mở khoá (15 mảnh với tướng Khá), lên sao; tướng đã 20 sao thì mỗi mảnh thành một bản sao thẻ ngẫu nhiên — [Progress.cs L258-282](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>); [heroes.json shards](<D:/PokiClash/Assets/02 Data/Json/heroes.json>)
- **Bản sao thẻ**: nâng thẻ tới cấp 5. `GiveCard` cứ cộng `copies`, rương bốc cả thẻ của tướng đã đủ cấp 5, mà ở cấp tối đa `CardReq` trả `int.MaxValue` — [Progress.cs L64-72, L228-247](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>)
- **Gỗ, quặng**: "chỉ dùng trong nhà (xây, nâng cấp, dọn rừng, trang trí), không đổi ra bi" — [21_Nha_Home.md L182-188](<D:/PokiClash/GD_Claude/21_Nha_Home.md>)
- Bi thụ động: khoảng 300/ngày đầu game, 700–1.100/ngày cuối game — [26_CuaHang_IAP_QuangCao.md ≈L240-244](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>)

### Inferences
- **Chỗ tiêu đang thiếu (theo code và GD):** (1) EXP sau cấp 200, khoảng từ ngày 33–46 trở đi; (2) đá tiến hóa dư vì phần lớn tướng chỉ tiến hóa một lần (20 đá); (3) bản sao thẻ của thẻ cấp 5 và mảnh của tướng tối đa (sau khi đổi ra bản sao thẻ). Một cây kỹ năng mua bằng một hoặc nhiều thứ trong số này sẽ tạo chỗ tiêu mà không cần nguồn mới.
- Gỗ, quặng sẽ dư sau Nhà cấp 10 (cấp người chơi 175) và công trình cấp 7; khi đó chỉ còn trang trí để tiêu. Đây là chỗ tiêu phụ có thể dùng, nhưng GD nói rõ Nhà không đụng tới sức mạnh trong trận.
- Nếu thêm một đơn vị riêng cho cây kỹ năng (ví dụ "điểm sổ phép"), nên lấy nó từ chỗ đang dư (EXP thừa, đá dư, bản sao dư), đừng mở nguồn mới làm lệch nhịp đã chốt.

### Gaps
- Không tìm thấy số đo đá tiến hóa còn dư thực tế sau "bậc theo dạng". GD ghi "chưa chỉnh nguồn đá", chưa có ProgressSim cho việc này.
- Chưa xác minh trong code việc chỉ trao thẻ của tướng chưa tối đa (đọc `RollCardDrop`: không thấy lọc theo cấp thẻ; kết luận "bản sao dư" là suy từ code, chưa đo).

## 4. Tướng và hệ được dựng thế nào (5 hệ, vai, độ hiếm, luật thẻ, chỉ số, StatMods)?

### Takeaway
Hiện có 50 tướng, 10 mỗi hệ. Độ hiếm rải theo suất ải (Thường → Huyền thoại ở boss ải 70). Trận đánh dùng Máu/Công/Thủ (Tốc đã bỏ), mana +20 mỗi lượt, nộ 100 để tung Tuyệt kỹ, khắc hệ ×1,5/×0,75. Không có trường "vai" chính thức; vai chỉ là ghi chú thiết kế. Phần cộng của side meta đi qua hai đường: `StatMods` (% Máu/Công/Thủ) và `BattleStart` (hiệu ứng đầu trận).

### Cited Findings
- `heroes.json` có 50 tướng: kim 10, mộc 10, thủy 10, hỏa 10, thổ 10. Độ hiếm: common 5, uncommon 15, rare 10, epic 15, legend 5. Trường: id, name, title, aola, elem, rarity, stats[6], skill, ult, passive, shards, line, size, forms. **Không có trường vai** — [heroes.json](<D:/PokiClash/Assets/02 Data/Json/heroes.json>). Lệch nguồn: `13_DanhSachTuong.md` ghi tựa "40 tướng"; bộ nhớ dự án ghi "78 tướng" — [13_DanhSachTuong.md L1](<D:/PokiClash/GD_Claude/13_DanhSachTuong.md>)
- Độ hiếm theo suất ải: ải 1, 5 Thường; 10, 15 Khá; 20, 30 Hiếm; 40, 50, 60 Sử thi; ải 70 Huyền thoại — [20_TangDayNoiDung.md L43](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>). `RarityPower` 1 / 1,1 / 1,23 / 1,38 / 1,76 — [HeroStats.cs L32](<D:/PokiClash/Assets/01 Script/Core/HeroStats.cs>)
- Enum: `Elem {Kim, Moc, Thuy, Hoa, Tho}`, `Rarity {Common…Legend}`, `CardKind {Pool, Skill, Ult, Passive}`, `CardGroup {Atk, Def, Heal}`, `PassiveTrigger {None, Start, TurnStart, LowHp, OnAttack, OnHit, Death}`, `StatusId {Burn, Stun, Regen, Evade, Poison}` — [Types.cs L9-40](<D:/PokiClash/Assets/01 Script/Core/Types.cs>)
- Khắc hệ: Thủy > Hỏa > Kim > Mộc > Thổ > Thủy; đánh hệ mình khắc ×1,5, hệ khắc mình ×0,75; tướng đồng hành không bao giờ chịu thiệt vì hệ — [Elements.cs L25-37](<D:/PokiClash/Assets/01 Script/Core/Elements.cs>); [25_FTUE.md L355](<D:/PokiClash/GD_Claude/25_FTUE.md>)
- Luật trận: mana +20 mỗi lượt; Chiêu tốn mana, ra đòn ngay, mỗi lượt một lần; nộ tăng khi đánh và khi bị đánh; đầy 100 nộ (và đủ mana) thì Tuyệt kỹ thay cú đánh thường. Hiệu ứng: bỏng, độc, hồi phục, choáng (mất trọn lượt), né, khiên — [25_FTUE.md L353-356](<D:/PokiClash/GD_Claude/25_FTUE.md>); [balance.json cfg: manaPerTurn 20, maxMana 100, maxRage 100, rageOnAttack 10, rageOnHit 80, critBase 0,05, critMult 1,6, shieldCap 0,6, maxRounds 60](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Thẻ: 75 thẻ chung (Thường 19, Khá 20, Hiếm 17, Sử thi 12, Huyền thoại 7); 151 thẻ riêng (50 chiêu, 50 tuyệt kỹ, 51 nội tại); 90 thẻ lính; 15 bị động boss (`traits`) — [cards.json](<D:/PokiClash/Assets/02 Data/Json/cards.json>)
- Rút thẻ: 3 thẻ khác nhau từ **mọi thẻ chung đã mở theo cấp**, nặng theo độ hiếm (`poolWeight` 50/30/14/5/1); thẻ đã chọn không ra lại trong lượt trừ thẻ `repeat`. Không có xây bộ bài — [Battle.cs L277-295](<D:/PokiClash/Assets/01 Script/Core/Battle/Battle.cs>); [balance.json poolWeight](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Cơ chế thẻ mới (2026-11-17): độc cộng dồn (lan khi gục, kích nổ), phản đòn, kết liễu, combo theo nhóm thẻ, cộng hưởng hệ, khắc hệ, cường hóa thẻ kế, chặn hồi máu, liều theo máu đã mất, đập khiên — [20_TangDayNoiDung.md L129-131](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Chỉ số: Máu = hpBase × √(máu gốc/tb) × m; Công = atkBase × √(max(công, công phép)/tb) × m; Thủ = defBase × √(tb(thủ, thủ phép)/tb) × m; m = độ hiếm × cấp × sao. `StatMods` {hpPct, atkPct, defPct, spd} nhân thêm. Lực chiến = 2·√(máu hiệu dụng × Công), chỉ để hiện — [HeroStats.cs L1-75](<D:/PokiClash/Assets/01 Script/Core/HeroStats.cs>)
- Tốc bị bỏ khỏi chỗ hiện và tiềm năng vì "trận, máy chọn thẻ, trang trại đều không dùng tốc"; `Stats.spd` giữ trong Core để golden không đổi — [20_TangDayNoiDung.md L157-160](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Phần cộng side meta: `Potential.Mods(s,d,h)` gộp huy hiệu (hệ + cả đội) và tiềm năng/bộ vào `StatMods`; `Potential.Start(s,d,hero)` gộp hiệu ứng đầu trận của tiềm năng, bộ và đặc tính hệ — [Potential.cs ≈L216-243](<D:/PokiClash/Assets/01 Script/Core/Potential.cs>)
- **Trận rất ngắn**: mỗi bên khoảng 2 lượt, địch gần như không đánh thường (0,26 lần/trận). Vì vậy bị động kiểu "đánh thường" hay "đầu lượt" hầu như không chạy; bị động có tác dụng là "bị đánh", "máu thấp", "vào trận" — [14_HeThongAi.md ≈L300](<D:/PokiClash/GD_Claude/14_HeThongAi.md>). Ghi chú khác cho trận Thổ dài 7,3–8,1 hiệp — [12_KeHoach_OpenSpec.md ≈L422](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- Vai chỉ là ghi chú: 5 tướng khởi đầu (đều Khá, 15 mảnh) có vai đề xuất Bu Lông "khiên, choáng", Nụ Hoa "hồi nộ, tuyệt kỹ sớm", Giọt Sương "hồi máu, giảm công địch", Sư Tử Lửa "đốt", Thạch Nhân "thủ, phản đòn" — [15_TuongKhoiDau.md L61-80](<D:/PokiClash/GD_Claude/15_TuongKhoiDau.md>). FTUE dùng nhãn kiểu chơi "Bền bỉ", "Thiêu đốt", "Phòng thủ" — [25_FTUE.md L136-140](<D:/PokiClash/GD_Claude/25_FTUE.md>)
- Địch đảo 70 ải quy về sức tướng Khá cùng cấp; sao và cấp thẻ của địch bám người chơi "vừa" ở cùng cấp — [HeroStats.cs L29-31](<D:/PokiClash/Assets/01 Script/Core/HeroStats.cs>); [14_HeThongAi.md ≈L167](<D:/PokiClash/GD_Claude/14_HeThongAi.md>)

### Inferences
- Vì trận chỉ khoảng 2 lượt, nút cây kỹ năng nào kích hoạt **lúc vào trận, khi bị đánh, khi máu thấp, hoặc đổi cách rút/chọn thẻ** sẽ thấy rõ. Nút "mỗi đầu lượt" hay "khi đánh thường" gần như không có tác dụng. Không dùng Tốc.
- Người chơi không có quyền xây bộ bài, nên "thao túng bộ rút" (bỏ nhóm thẻ, tăng nhóm Công/Thủ/Hồi, thêm lượt đổi thẻ, thêm 1 thẻ trong lượt chọn) là khoảng trống lựa chọn rõ nhất mà chưa hệ nào đụng tới. `CardGroup {Atk, Def, Heal}` có sẵn trong code để làm việc này.
- Vai không có trong dữ liệu, nên cây theo tướng hoặc theo vai phải gắn tag mới vào `heroes.json`, hoặc suy vai từ 3 thẻ riêng.
- Địch bám sức người chơi "vừa", nên sức cộng từ cây kỹ năng phải tính vào kỳ vọng đó. Không thì ải dễ đi (hoặc phải nâng địch, và lựa chọn của người chơi mất nghĩa).

### Gaps
- Chưa đọc `Battle.cs` trọn bài để liệt kê mọi điểm móc (hook) của hiệu ứng thẻ; `BattleStart` mới biết qua chú thích.
- Chưa có số liệu "tỉ lệ dùng" từng thẻ chung hay từng nhóm thẻ trong trận thật.

## 5. Có những móc cốt truyện nào (cậu bé thuần thú sư, sổ phép, bút chì phép, màn mở khoá vẽ tướng vào sổ, đền, chòm sao…)?

### Takeaway
Hình tượng "sổ và bút chì" đã thấm khắp game: nhân vật chính thuần phục sinh vật bằng cách vẽ chúng vào sổ phép; bìa sổ có sao năm màu hệ; dây chéo ngực cài 5 bút chì 5 màu hệ; tướng mới được bút chì vẽ lên trang sổ; vùng đảo mới được bút chì tô màu; Sổ tay có các trang "Cách chơi" mở dần ("???" khi chưa mở). Thêm Đền Huy Hiệu (5 bệ), Hang Tiềm Năng (tầng có tên), tượng boss ở Nhà và "mỗi đảo một chúa tể".

### Cited Findings
- Nhân vật chính (chốt 2026-11-23): cậu bé thuần thú sư khoảng 11 tuổi, cầm **sổ phép** (bìa da nâu, góc đồng, **sao năm màu hệ**) và **bút chì phép** to cỡ cẳng tay dùng như đũa phép; **thuần phục sinh vật bằng cách vẽ chúng vào sổ**; dây chéo ngực cài **5 bút chì 5 màu hệ**; "Phép thuật vẽ bằng nét chì màu, không phát sáng" — [25_FTUE.md L523](<D:/PokiClash/GD_Claude/25_FTUE.md>)
- Lời dẫn của cậu: "Sổ phép đưa mình tới đây... Năm hòn đảo, năm hệ. Phải tìm một bạn đồng hành đã!"; "Bốn đảo nữa!..." — [25_FTUE.md L525](<D:/PokiClash/GD_Claude/25_FTUE.md>)
- Cốt truyện mở đầu, 6 khung: đêm bão, thuyền bị cuốn vào xoáy mây năm màu → tỉnh dậy ở thế giới lạ → rừng sương → "Những người bạn mới" (5 tướng đồng hành) → "Mỗi đảo một chúa tể" (bóng chúa tể núi lửa) → "Đi chinh phục thôi!" — [25_FTUE.md L504-521](<D:/PokiClash/GD_Claude/25_FTUE.md>)
- Màn mở khoá tướng (làm lại 2026-11-24 tối): trang sổ phép (giấy viền mực, dòng kẻ, lề đỏ) trượt lên, **bút chì lần theo viền tướng**, gạch chì, tô sáp màu, rồi tướng bật ra khỏi trang, diễn chiêu cuối, sao trắng bắn ra, ruy băng "TƯỚNG MỚI!" — [26_CuaHang_IAP_QuangCao.md ≈L752-770](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>)
- Mở vùng đảo sau khi hạ boss: mây tan, **bút chì bay vào ngoáy dọc đường, màu loang theo nét bút**; vùng khoá vẽ bằng nét phác chì kèm ghi chú bút chì ("Đừng vào khi mưa!", "Hang rồng?"); có cảnh rò qua mây như "đền Giông Mưa" ở đảo Thủy — [18_DaoVungDat_Habitat.md L415-470](<D:/PokiClash/GD_Claude/18_DaoVungDat_Habitat.md>)
- Sổ tay có mục "Cách chơi": mỗi trang mở khi bước hướng dẫn tương ứng đã chạy, **trang chưa mở hiện "???"** — [25_FTUE.md L343-348](<D:/PokiClash/GD_Claude/25_FTUE.md>)
- Đền Huy Hiệu: scene riêng với **5 bệ theo hệ**; huy hiệu 10 bậc (Đồng, Bạc, Vàng, Ngọc, Kim Cương, Hồng Ngọc, Lục Bảo, Tử Tinh, Nhật Nguyệt, Thần Thoại) — [12_KeHoach_OpenSpec.md L187-192](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>); [balance.json badges.tiers](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Hang Tiềm Năng có tầng có tên: Cửa Hang, Hành Lang Rêu, Suối Ngầm, Vách Thạch Anh, Hồ Phát Sáng, Rừng Nhũ Đá, Mạch Dung Nham, Điện Pha Lê… — [balance.json cave.tiers](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Nhà: thắng boss ải 70 của một đảo thì được **tượng nhỏ của boss** để trang trí; bộ trang trí theo hệ — [21_Nha_Home.md L164-173](<D:/PokiClash/GD_Claude/21_Nha_Home.md>)
- Ý tưởng màn boot: A sa bàn giấy pop-up, B **ấn Ngũ Hành**, C **bìa sổ chiến thuật**; cả ba vẽ vòng khắc (đã làm A) — [README.md L32](<D:/PokiClash/GD_Claude/README.md>); [16_ManBoot.md ≈L21-47](<D:/PokiClash/GD_Claude/16_ManBoot.md>)
- Popup cửa hàng theo chất "sổ tay phiêu lưu": popup là tờ giấy, nhãn là sticker, đồng hồ viết bút chì — [26_CuaHang_IAP_QuangCao.md L206](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>)

### Inferences
- Móc tự nhiên nhất cho cây kỹ năng cấp tài khoản là **"Sổ phép"**: mỗi trang hoặc mỗi chương là một nhánh, nút mở bằng hoạt ảnh bút chì vẽ và tô sáp (dùng lại `InkStroke`, shader `UIPencilDraw` của màn mở khoá). Trang khoá hiện "???" như Sổ tay, nên người chơi đã quen mẫu này.
- **5 bút chì 5 màu hệ** và **sao năm màu trên bìa** là sẵn hình cho 5 nhánh theo hệ (hoặc "chòm sao" vẽ chì trên bìa sổ). Phải tránh trùng Đền Huy Hiệu, nơi đã có phần cộng theo hệ (mục 8).
- Không tìm thấy lore về "chòm sao" hay "đền trên đảo" dành cho kỹ năng. "Mỗi đảo một chúa tể", tượng boss và đền Giông Mưa có thể làm cổng mở nhánh (hạ chúa tể → mở trang sổ của hệ đó).

### Gaps
- Không thấy tài liệu cốt truyện dài hơn 6 khung mở đầu (không có tên thế giới, phe phái, nguồn gốc sổ phép). Ngoài các câu hướng dẫn, nhân vật chính chưa có kỹ năng hay vai trò trong trận.
- Chưa rõ nhân vật chính có hiện trong trận hay ở sảnh không (chỉ thấy chân dung ở lớp phủ hướng dẫn).

## 6. Ràng buộc UI và luật dự án; GD đã có hay đã bỏ ý "cây kỹ năng / thiên phú / talent" nào chưa?

### Takeaway
Ràng buộc chính: màn dọc 1080×1920; nét vẽ tay mực nâu, giấy kẻ ô, sáp màu; không bóng, không quầng sáng; mọi thứ (kể cả UI) là prefab nướng sẵn, runtime không sinh gì; logic thuần C# trong `Core` có golden/test; chữ tiếng Việt bọc `Loc`. Không tài liệu hay code nào nhắc "cây kỹ năng", "thiên phú", "talent", "skill tree", "mastery". Ý gần nhất là "sao mở thêm hiệu ứng cho chiêu" (GD cũ) và "tiến hóa mở kỹ năng mới" (Pokiwar).

### Cited Findings
- Bộ UI "Sa Bàn": mặt bàn gỗ, trang giấy kẻ ô có lề đỏ, mực nâu #2b2118, sáp màu gạch chéo, băng keo washi, sticker viền trắng; **"Không bóng đổ, không bóng lệch, không ánh sáng. Tách lớp bằng viền mực."**; chữ Baloo 2 và Pangolin; hiệu ứng ít: thở, nảy khi nhấn, nhún tại chỗ — [17_BoUI.md L1-19](<D:/PokiClash/GD_Claude/17_BoUI.md>)
- Mọi thứ là prefab, kể cả UI; runtime không sinh gì; code dựng cũ đã xoá, prefab là nguồn gốc; mỗi hộp thoại là biến thể của `Dialogs/HopThoai`; phần có số lượng theo dữ liệu mà dựng sẵn cố định thì phải thêm tay khi dữ liệu tăng — [12_KeHoach_OpenSpec.md L234-245, ≈L493](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>); test `PrefabOnlyTests` và menu dựng trong `Editor/` — [20_TangDayNoiDung.md L87](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Game view `PokiClash 1080x1920`, màn hình dọc — [12_KeHoach_OpenSpec.md L87](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>); [README.md L3](<D:/PokiClash/GD_Claude/README.md>)
- `Core` là logic thuần (không UnityEngine), có golden và test EditMode; đổi luật thì tính lại golden — [12_KeHoach_OpenSpec.md L90-93](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>); [20_TangDayNoiDung.md L88](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Tìm "thiên phú|cây kỹ năng|talent|skill tree|mastery" trong `GD_Claude` và `Assets/01 Script`: không có kết quả nào liên quan (chỉ ra "kỹ năng bàn" của hướng xếp khối cũ) — tìm kiếm cục bộ ngày 2026-11-24
- Ý tiền lệ: GD cũ "Sao: … mỗi sao tăng chỉ số và có mốc mở thêm hiệu ứng cho chiêu"; "Tiến hóa đổi hình, nâng trần cấp, mở chiêu mạnh hơn" — [06_Tuong_NuoiDuong.md ≈L14-18](<D:/PokiClash/GD_Claude/06_Tuong_NuoiDuong.md>). Pokiwar: "tiến hóa mở kỹ năng mới" — [01_HuongPhatTrien.md L11](<D:/PokiClash/GD_Claude/01_HuongPhatTrien.md>). Hướng xếp khối cũ (đã bỏ) có "bị động chủ lực kiểu leader skill của Puzzle & Dragons" — [04_ChienDau.md L8](<D:/PokiClash/GD_Claude/04_ChienDau.md>)
- Ý đã bỏ hoặc đã chốt chặn:
  - bỏ lõi xếp khối — [README.md L41-51](<D:/PokiClash/GD_Claude/README.md>);
  - bỏ Tốc — [20_TangDayNoiDung.md L157-160](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>);
  - không làm "suýt trúng" ở máy bi — [23_MayBi_TraiNghiem.md L16-17](<D:/PokiClash/GD_Claude/23_MayBi_TraiNghiem.md>);
  - chưa có tiền cứng — [26_CuaHang_IAP_QuangCao.md ≈L222](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>);
  - không bán lẻ đá tiềm năng, đá tinh — [12_KeHoach_OpenSpec.md L59](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>);
  - trần popup 2 mỗi lần vào, 4 mỗi ngày — [26_CuaHang_IAP_QuangCao.md L196-206](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>);
  - "Hiệu ứng huy hiệu trong trận: để sau" — [12_KeHoach_OpenSpec.md L69](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>);
  - AFK thôi ra bi, thay bằng Cây bi — [12_KeHoach_OpenSpec.md L72](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>);
  - Trang trại thay bằng Nhà — [21_Nha_Home.md L5-17](<D:/PokiClash/GD_Claude/21_Nha_Home.md>).
- Thông tin hiển thị: chỉ số và lực chiến từ 1000 ghi dạng gọn (3.3k, 602k) qua `NumFmt.Short`; độ hiếm có khung/màu riêng — [20_TangDayNoiDung.md L47-51, L140-144](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)

### Inferences
- Cây kỹ năng phải dựng như một prefab màn (và một prefab nút lặp ở `Items/`), có menu dựng trong `Editor/`. Nếu số nút theo dữ liệu mà prefab dựng sẵn cố định thì đổi dữ liệu phải sửa tay prefab, nên **chọn số nút cố định mỗi trang/nhánh** sẽ khớp luật "chỉ prefab".
- Đường nối, nút sáng, quầng "đã mở" kiểu cây kỹ năng thường gặp sẽ phạm luật không quầng sáng. Phải tách lớp bằng viền mực, tô sáp khi mở, nét chì chấm khi khoá.
- Logic cây nên nằm trong `Core` (thuần C#), đi qua `StatMods`/`BattleStart` có sẵn, kèm golden mới. Đổi chỉ số mặc định thì làm lệch golden trận hiện có (tướng không có mods phải khớp từng bit với bản web, theo chú thích `HeroStats.cs` L58).

### Gaps
- Bộ nhớ dự án có luật bố cục "phần dưới cố định mọi cỡ máy, phần trên co giãn, không thanh tab", nhưng không thấy trong GD đã đọc, nên chưa trích dẫn được. Chưa đọc `17_BoUI.md` mục Unity (L54-117).

## 7. Câu hỏi mở hoặc việc còn dở nào trong 12_KeHoach_OpenSpec.md (và GD liên quan) dính tới tiến trình dài hạn?

### Takeaway
Các câu hỏi mở dính tới tiến trình: nhịp (đã chốt cấp 200 khoảng ngày 46 nhưng còn đo thô phần Nhà), trang trại/Nhà có ra EXP không, đá tiến hóa dư sau "bậc theo dạng", chỉ số lệch giữa màn Tướng và trận khi có huy hiệu/tiềm năng, và sau cấp 200 chưa có nội dung tiến trình nào được thiết kế.

### Cited Findings
- Câu 1 "Nhịp tiến độ": lịch sử từ mục tiêu "xong 5 đảo ngày 21" tới thang 1–200 (2026-11-04: "vừa" cấp 200 ngày 57 là được), rồi 2026-11-24 chốt "vừa" khoảng ngày 46. "Mô phỏng vẫn dùng mô hình trang trại cũ cho bi của ruộng vườn ở Nhà (gần đúng)" — [12_KeHoach_OpenSpec.md ≈L453-468](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- Nhận định cũ trong câu 1: "Sức mạnh chủ yếu đến từ sao tiến hóa và cấp thẻ… vì thẻ đến từ rương máy bi" (đo trước thang 200) — [12_KeHoach_OpenSpec.md ≈L458](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- Câu 2: "**Trang trại** có ra thêm EXP không?" (chưa trả lời) — [12_KeHoach_OpenSpec.md ≈L469](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- Câu 14: màn Tướng và trận tính chỉ số khác nhau khi tướng có huy hiệu, tiềm năng ("Lệch chỉ số: màn Tướng 1039/471/119, trận 1191/357/95") — [12_KeHoach_OpenSpec.md ≈L494](<D:/PokiClash/GD_Claude/12_KeHoach_OpenSpec.md>)
- Đá tiến hóa dư sau "bậc theo dạng", chờ người dùng quyết — [20_TangDayNoiDung.md L38](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Mục tiêu độ khó: không max (Kim Cương 5★) được tướng nào trước khoảng ngày 45–60 — [20_TangDayNoiDung.md L25](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Đền bậc 10 địch cấp 205; Hang tầng cuối khoảng cấp 195; Đền 78 trận mỗi dãy (390 trận cho 5 dãy) là nội dung cày dài nhất hiện có — [20_TangDayNoiDung.md L120-124, L155](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Chế độ khác mới ở dạng đề xuất (đấu trường cùng hạt giống, boss tuần, Tháp), "làm sau khi lõi vượt ải đã vui" — [09_CheDoKhac.md L1-24](<D:/PokiClash/GD_Claude/09_CheDoKhac.md>)
- Kế hoạch cửa hàng còn pass (S6) và Quỹ theo mốc cấp; 11 câu cần chốt ở mục 11 — [26_CuaHang_IAP_QuangCao.md L577-607](<D:/PokiClash/GD_Claude/26_CuaHang_IAP_QuangCao.md>)
- Đã ghi: Nhà mở sau ải 2 có trong mô phỏng nhịp; mỏ đá tiến hóa ở Nhà sẽ đổi nhịp tiến hóa, cần đo lại — [21_Nha_Home.md L185](<D:/PokiClash/GD_Claude/21_Nha_Home.md>)

### Inferences
- Không có câu hỏi mở nào nói về "nội dung sau cấp 200" hay "điểm/tài nguyên thừa ở cuối game". Cây kỹ năng có thể đóng vai trò này, và đồng thời giải câu "đá tiến hóa dư".
- Câu 14 (lệch chỉ số) là rủi ro kỹ thuật: thêm một nguồn `StatMods` nữa thì phải sửa chỗ lệch này trước, không thì số hiện ở màn Tướng và trong trận càng khác nhau.

### Gaps
- Chưa đọc các `openspec/changes/*/design.md` (câu hỏi gốc trước khi gom). Chưa đọc mục 11 của `26_CuaHang_IAP_QuangCao.md` (11 câu cần chốt).

## 8. Phân tích khoảng trống: cây kỹ năng (cấp tài khoản, theo tướng, theo hệ, theo thẻ) đặt ở đâu thì thêm được lựa chọn mà không trùng hệ đã có?

### Takeaway
Khoảng trống lớn nhất là **lựa chọn có tính chất** (đổi cách chơi), vì mọi lớp hiện có chỉ cộng chỉ số hoặc quay ngẫu nhiên, và **chỗ tiêu cho tài nguyên dư** ở giữa và cuối game (EXP sau cấp 200, đá tiến hóa, bản sao thẻ). Hướng ít trùng nhất: cây **cấp tài khoản "Sổ phép"** tác động lên luật rút/chọn thẻ, mana/nộ đầu trận, đổi tướng, khắc hệ. Hướng thứ hai: **nhánh chọn của thẻ riêng ở cấp 5** để tiêu bản sao dư. Cây **theo hệ** trùng mạnh với Đền Huy Hiệu. Cây **theo tướng** trùng Tiềm năng và rất tốn nội dung.

### Cited Findings
(Các dữ kiện nền đã dẫn nguồn ở mục 2–7. Mục này so mỗi dạng cây với hệ đang có.)
- Phần cộng % Máu/Công/Thủ theo hệ đã có ở Đền Huy Hiệu (+5…16%, đặc tính hệ ở bậc 4/6/8/10) — [balance.json badges](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Phần cộng theo tướng (Công/Thủ/Máu %, chí mạng, hút máu, mana/nộ/khiên đầu trận, giảm sát thương, né) đã có ở Tiềm năng 6 ô + 3 bộ — [balance.json potential](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Thẻ riêng chỉ có trục cấp 1–5 (×1,6), không có nhánh — [Progress.cs L64-81](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>); [balance.json cfg.cardLvStep](<D:/PokiClash/Assets/02 Data/Json/balance.json>)
- Rút thẻ chung là ngẫu nhiên trên mọi thẻ đã mở, không xây bộ — [Battle.cs L277-295](<D:/PokiClash/Assets/01 Script/Core/Battle/Battle.cs>)
- Trận khoảng 2 lượt; móc "vào trận / bị đánh / máu thấp" mới có tác dụng — [14_HeThongAi.md ≈L300](<D:/PokiClash/GD_Claude/14_HeThongAi.md>)
- Ô đội 2 ở cấp 60, ô 3 ở cấp 200; đổi tướng đầu lượt chỉ có từ 2 ô — [Progress.cs L331-345](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>); [25_FTUE.md L363](<D:/PokiClash/GD_Claude/25_FTUE.md>)
- EXP bị chặn ở cấp 200 — [Progress.cs L42](<D:/PokiClash/Assets/01 Script/Core/Progress.cs>). Đá tiến hóa dư — [20_TangDayNoiDung.md L38](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>)
- Side meta "vừa" ≈ +4–5 cấp, trần ≈ +13–14 cấp — [20_TangDayNoiDung.md L125](<D:/PokiClash/GD_Claude/20_TangDayNoiDung.md>). Địch bám sức người chơi "vừa" — [14_HeThongAi.md ≈L167](<D:/PokiClash/GD_Claude/14_HeThongAi.md>)
- Nhà không đụng tới sức mạnh trong trận (điểm đẹp); gỗ, quặng chỉ dùng trong nhà — [21_Nha_Home.md L164-188](<D:/PokiClash/GD_Claude/21_Nha_Home.md>)

### Inferences
**A. Cây cấp tài khoản ("Sổ phép" của nhân vật chính): ít trùng nhất, đề xuất chính**
- Điểm lấy từ lần lên cấp (lấp các cấp 60–200 đang trống) và từ EXP thừa sau cấp 200 (kiểu "paragon", cho EXP máy bi giá trị trở lại). Có thể thêm đá tiến hóa dư làm giá cho nút lớn.
- Nút nên **đổi luật**, không cộng % chỉ số (để khỏi trùng Huy hiệu/Tiềm năng): thêm 1 lần đổi bộ 3 thẻ mỗi lượt; chọn nhóm thẻ ưu tiên (Công/Thủ/Hồi, có sẵn `CardGroup`); +mana hoặc nộ đầu trận (lưu ý tiềm năng cũng có dòng mana/nộ đầu trận, nên chọn dạng khác như "Tuyệt kỹ sớm hơn khi máu thấp"); tướng dự bị nhận mana (`benchMana` có sẵn); hệ số khắc hệ; hồi sinh, đổi tướng.
- Hợp cốt truyện (bút chì vẽ, trang "???"), hợp luật prefab nếu mỗi trang có số nút cố định.
- Rủi ro: ảnh hưởng mọi trận, nên phải đưa vào `ProgressSim`/`Sim` và nâng kỳ vọng sức địch, không thì lệch mục tiêu "vừa" cấp 200 ngày 46. Nút kinh tế (thêm bi, thêm EXP) là nguy hiểm nhất cho nhịp.

**B. Nhánh của thẻ riêng ở cấp 5 (theo thẻ): ít trùng, tiêu bản sao dư**
- Khi thẻ lên cấp 5, mở lựa chọn 1 trong 2 biến thể (ví dụ chiêu thêm choáng hoặc thêm hút máu). Giá là bản sao thẻ dư hoặc mảnh dư. Đây là đúng ý cũ "sao mở thêm hiệu ứng cho chiêu" và "tiến hóa mở kỹ năng mới".
- Rủi ro: 151 thẻ riêng × 2 biến thể là nhiều việc nội dung và cân bằng. Có thể chỉ làm cho Tuyệt kỹ, hoặc chỉ cho tướng Sử thi/Huyền thoại.

**C. Cây theo hệ (5 bút chì màu): trùng nhiều với Đền Huy Hiệu**
- Đền đã cho % chỉ số theo hệ và đặc tính hệ. Muốn làm thì nhánh hệ chỉ nên chứa nút **đội hình/cộng hưởng** (khi đội có 2–3 tướng cùng hệ hay khác hệ), mà ô 2 mở ở cấp 60, ô 3 ở cấp 200, nên giá trị chỉ đến muộn. Hoặc gộp vào Đền như một "trang sổ" mở theo bậc huy hiệu, để khỏi thêm một hệ thứ hai.

**D. Cây theo tướng: trùng Tiềm năng, tốn nội dung**
- Tiềm năng đã là "build theo tướng" (dòng ngẫu nhiên). 50 tướng × cây riêng là việc rất lớn, mà người chơi chỉ mang 1–3 con. Nếu muốn có, nên làm khung cây chung theo vai (cần thêm trường vai vào `heroes.json`) thay vì cây riêng từng con.

**Giai đoạn trống mà cây có thể lấp**
- Giữa game (cấp 60–200, khoảng ngày 15–46 với người chơi "vừa"): lên cấp gần như chỉ +3%.
- Cuối game (sau cấp 200 / ngày 46 với "vừa", ngày 33 với "chăm"): EXP vô dụng, tiến hóa xong phần lớn (tướng 2 dạng), chỉ còn Đền bậc cao, Hang, quay tiềm năng, trang trí.
- Đầu game (cấp 1–30) đã dày (thẻ mở mỗi cấp, FTUE, Nhà mở sau ải 2), nên **chưa nên mở cây trước khoảng cấp 30–60**. Hang mở ở cấp 30, ô 2 ở cấp 60 là hai mốc có thể dùng làm cổng.

### Gaps
- Chưa có dữ liệu người chơi thật (retention, chỗ bỏ game). "Giai đoạn trống" ở đây suy từ cấu trúc phần thưởng và mô phỏng, chưa có số đo cảm nhận.
- Chưa đo mức sức mạnh mà một cây tài khoản được phép thêm. Gợi ý ngân sách chỉ có thể suy từ con số side meta (≈ +4–5 cấp ở mức "vừa"), chưa có quyết định của người dùng.
- Không biết người dùng muốn cây làm "đồ tiêu tài nguyên", "lựa chọn build", hay "cốt truyện/sưu tầm". Mỗi mục đích dẫn tới một dạng cây khác nhau.
