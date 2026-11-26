# 33. Cân bằng kinh tế sau đảo Casino: giả lập 300 người chơi, kế hoạch đổi số (2026-11-26)

Người dùng dặn 2026-11-26: "việc thêm nhiều tính năng ở đảo casino sẽ ảnh hưởng tới nhiều nguồn thu nhập liên quan đến player progression. Đây
là game iap và xem reward ads nên tôi cần người chơi phải mua iap và phải xem reward ads. Bạn hãy giả lập khoảng 300 người chơi chơi game để tự
cân bằng lại game, thưởng, tỉ lệ, các phần cần thiết để nâng cấp, làm sao để người chơi không được phép có quá nhiều tài nguyên và kích họ mua
các gói iap. Có thể tham khảo clash of critters […] đào thật sâu vào. Sau khi chạy giả lập bạn tự phân tích số liệu thật kĩ rồi cho tôi kế
hoạch thay đổi."

**Trạng thái 2026-11-26 (tối): đợt 1, 2, 3 đã áp vào game** (mục 0). Phần còn lại của file là bản kế hoạch và số đo lúc chưa sửa; "hiện
tại" trong các bảng nghĩa là game trước khi sửa.

## 0. Đã áp vào game (2026-11-26, tối)

Người dùng dặn: "Bạn sau khi đã nghiên cứu đủ thì tự làm theo đề xuất, tôi chỉ gợi ý thôi."

| Việc | Trạng thái | Sửa ở |
|---|---|---|
| 1. Thẻ thừa ở Chợ đen | xong, **số thận trọng hơn bảng 5.1**: 20 bản đổi 1 đá tiềm năng, tối đa 10 đá mỗi ngày; không ra bi | `BlackMarket.SellSpare`, `MarketConfig.copyPerStone / stoneDaily`, `MarketScene` |
| 2–11. Hầm đấu, Câu cá, Quán trọ, Đua | xong, đúng số bảng 5.1 | `ArtGen/Casino/so_lieu/gen_casino.py` → khối `casino` của `balance.json` |
| 12. Trứng trong rương máy bi | xong (bạc 1%, vàng 2,5%) | `balance.json`, golden `pachinko.json` tính lại |
| 13. Đánh lại ải | xong: 10 trận đầu mỗi ngày đủ bi, sau đó 25%; hộp kết quả gắn nhãn "Đã giảm", báo một lần | `Progress.WinStage(…, now)`, `stageBalls.replayFull / replayPct` |
| 14. Bỏ quảng cáo | xong: 8 lượt trao ngay mỗi ngày, hết thì xem như thường; mô tả gói đã đổi theo | `AdGate.UseInstant`, `Ads.Show`, `ads.noAdsInstant` |
| 15. Lọ Bi | xong: cách nhau 3 ngày, ô Lọ Bi ghi "đập lại được sau …" | `Shop.PiggyCanBreak(…, now)`, `piggy.gapDays` |
| 16. Gói Tiếp Sức | xong: dòng "thả bi" chỉ tính là cách miễn phí khi bi đang có đủ lên một cấp | `Offers.FreeFix` |
| 17. Bán đá tiến hóa | xong: "Đá tiến hóa hôm nay" 1,99 USD, "Túi đá tuần" 4,99 USD; Thẻ Phiêu Lưu thêm 1 đá mỗi ngày | `balance.json` |
| 18. Gói Khởi Hành | xong: 2.000 bi, 5 đá | `balance.json` |
| 19. Trứng Khá 0,99 USD | đã bỏ khỏi lưới bán | `balance.json` |
| 20. Vé chọn tướng Hiếm bán lẻ | xong: 2,99 USD, 1 lần mỗi tuần | `balance.json` |
| `34` việc 2. Đường EXP | xong, bản hai đoạn: EXP lên cấp = max(45 × cấp, 9 × cấp^1,54); 20 cấp đầu y như cũ nên hướng dẫn và golden AFK không đổi | `Progress.ExpToNext`, `expLateBase / expLatePow` |
| `34` việc 3 (một phần) | màn thua ghi "địch cấp X, bạn cấp Y: thả khoảng N bi để lên Z cấp"; Gói Tiếp Sức khi đang thiếu cấp thì hơn 70% giá trị là bi | `Offers.GapTo`, `BattleController` |

Chưa làm: việc 21 (giá Thẻ Phiêu Lưu), đợt 4, phương án C; ở `34`: gói bi "vừa đủ số còn thiếu" và bậc gói theo giai đoạn, nạp đầu 3 bậc,
gói 7 ngày; mọi việc của `35`. Nạp đầu 3 bậc và gói tướng theo mốc đã làm ở mục 0.1 (không giãn sức tướng).

**Kiểm:** bộ test EditMode trong Unity 244 ca, 242 đạt; 2 ca hỏng không thuộc phần này (chữ "ĐẶT CƯỢC", "ĐUA TIẾP" của prefab Trường đua
chưa có bản dịch; `PrefabOnlyTests` bắt `HeroUnlockView.cs`, `CardBend.cs`). Đã chụp tour Chợ đen và tour cửa hàng trong trận để soi chữ mới.

**Đo lại trên game đã sửa** (300 người chơi ảo; bảng ở `ArtGen/KinhTe/gia_lap/ket_qua/so_sanh_G30_game_moi.md`, `pha_dao_G90_game_moi.md`,
`tong_hop_G30_game_moi.md`):

| | Trước khi sửa | Game đã sửa |
|---|---|---|
| Người có ra đảo bị vỡ kinh tế (cầm hơn 1 triệu bi) | 150 / 150 | 0 / 150 |
| Chăm, không trả tiền: phá đảo (xong 350 ải) | ngày 33 | ngày 58 |
| Chăm, xem nhiều quảng cáo | ngày 18 | ngày 39 |
| Chăm, chi 15 USD | ngày 18 | ngày 41 |
| Chăm, chi 80 USD | ngày 12 | ngày 24 |
| Chăm, chi 600 USD | ngày 12 | ngày 12 |
| Vừa, không trả tiền | ngày 48 | khoảng ngày 104 |
| Vừa, xem ít quảng cáo | ngày 41 | ngày 81 |
| Vừa, không trả tiền: số lần gặp tường trong 30 ngày đầu | 3 | 57 |
| Chăm, không trả tiền: bi thu mỗi ngày (30 ngày đầu) | 1.752 | 1.188 |
| Gói Tiếp Sức bật, mỗi người không trả tiền trong 30 ngày | 0 lần | 3,5 lần |

Cột "trước khi sửa" của các dòng phá đảo là bộ B90 (game cũ đã bịt đảo Casino); game cũ nguyên trạng thì người ra đảo vỡ ở ngày 5–23.
Số đo chạy trước sửa nhỏ cuối cùng (Gói Tiếp Sức nghiêng về bi). Bộ số cũ cất ở `gia_lap/bo_so/cu_truoc_1126/`.

### 0.1. Ba vòng làm → chạy → rút kinh nghiệm (2026-11-27)

Người dùng dặn: "Chốt theo ý bạn đi. Làm xong lại chạy tiếp rồi rút kinh nghiệm rồi sửa rồi lại chạy."

| Vòng | Làm / đo | Số đo (người không ra đảo, 90 ngày) | Rút ra | Chốt |
|---|---|---|---|---|
| 1 | Đo trước khi làm: gói tướng "đi trước xa" có và không giãn sức tướng theo mốc (4 bộ số, 120 người không trả tiền) | Không giãn sức: người vừa tới 150 / 200 ải sớm 6 ngày, người chăm 1–3 ngày. Có giãn sức: người vừa sớm 9–12 ngày ở giữa game, nhưng người chăm phá đảo **muộn hơn** (71 so với 53 ngày) | Giãn sức chỉ thêm 3–6 ngày đi trước mà phải cân lại cả 350 ải, Đền, Hầm đấu; cuối game còn hại người mua | **Không giãn sức tướng.** Bán tướng mốc sau bằng hệ sao / độ hiếm sẵn có |
| 2 | Làm **Gói Vượt Mốc**: lần đầu qua ải tướng mốc k (k ≥ 3) của một đảo thì chào tướng mốc k + 3 của đảo đó, trọn bộ (mảnh mở khoá + lên sao tới mức cấp người chơi cho phép, bản sao thẻ, đá tiến hóa trên đường); giá tự tính theo giá trị gói (×5): 4,99 USD lúc mới chơi, tới 49,99 USD cho tướng Huyền thoại ở cấp 100; popup ghi lực chiến thật của tướng trong gói cạnh tướng mạnh nhất đang có | Popup bật khoảng 8 lần mỗi người trong 90 ngày; 54 người trả tiền mua 162 lần. Nhịp phá đảo không đổi (chăm chi 80 USD: 23 so với 24 ngày). Lọ Bi: người trả tiền đập 6,6 lần mỗi tháng, 2.188 bi mỗi USD, gói bi 340–900 | Gói Vượt Mốc không làm lệch kinh tế; cùng số tiền thì không nhanh hơn mua bi (cấp vẫn là thứ chặn), giá trị của nó là có tướng sớm. Lọ Bi vẫn rẻ gấp 4–6 lần gói bi | Giữ Gói Vượt Mốc. **Lọ Bi cách 7 ngày** (trước 3) |
| 3 | Làm **nạp đầu 3 bậc chọn một** (ba Gói Khởi Hành 4,99 / 9,99 / 19,99 USD, giá trị ×7 / ×7,9 / ×8, bậc trên kèm vé chọn tướng Hiếm / Sử Thi; mua một gói thì hai gói kia đóng) + Lọ Bi 7 ngày | Lọ Bi còn 3,4 lần đập mỗi tháng. Chăm chi 80 USD phá đảo ngày 25 (trước 23); các nhóm khác không đổi. 0 / 300 người vỡ kinh tế | Ổn. Người chơi ít (1 phiên, 2 trận mỗi ngày) không bao giờ gặp tường dù trả bao nhiêu: thứ chặn họ là thời gian chơi, chưa có gì để bán cho nhóm này | Giữ |

Sửa ở: `Offers.Jump / JumpHero / JumpPower / Build("jump")`, `Progress.PathCost`, `OfferCaps.jump*`; `ShopPack.group`, `Shop.GroupTaken`;
`balance.json` (mẫu `jump`, `launch_2`, `launch_3`, `piggy.gapDays`); `ShopSheet`, `HubShop`, `ShopPage`. Tour chụp:
menu "PokiClash/Thử/Cửa hàng/tour kinh tế…" (`Editor/ShopEconTour.cs`). Test EditMode trong Unity: 248 ca, 246 đạt (2 ca hỏng như trên).
Bảng: `gia_lap/ket_qua/vong1_goi_tuong_gian_suc.md`, `vong2_3_vuot_moc_nap_dau_lo_bi.md`, `tong_hop_J2_nap_dau_lo_bi.md`.

Giới hạn: người chơi ảo có ngân sách cố định theo nhóm, nên giả lập đo được nhịp game, lỗ hổng và giá trị mỗi USD, **không đo được tỉ lệ
người chịu mua**. Việc còn lại chủ yếu là UI mà giả lập không chấm được: ô gói cố định trên máy bi, ×2 EXP, gói sự kiện, lịch xoay 9 ngày
(`35` mục 5.1), đường thưởng sự kiện (mục 5.4), thứ để bán cho người chơi ít.

## Tóm tắt

1. **Game hiện tại vỡ kinh tế với mọi người chơi có ra đảo Casino.** Mục "thu mua thẻ thừa" ở Chợ đen đổi thẻ thừa ra bi, bi thả ra lại ra
   thẻ và trứng: vòng lặp tự nuôi. 150 / 150 người chơi ảo có ra đảo cầm hơn 1 triệu bi; người chăm không trả tiền vỡ ở ngày 5–6, người vừa
   ngày 7–12, người chơi ít ngày 18–23. Phải sửa trước khi phát hành đảo.
2. **Khoá lỗ đó rồi thì đảo vẫn làm thu nhập bi gấp 3,5–4 lần.** Thủ phạm là Hầm đấu (thắng trả 2,5 lần lệ phí, mỗi ngày 5 trận, lệ phí nhân
   bậc cấp): +2.300–2.800 bi mỗi ngày, hơn mọi nguồn free khác cộng lại. Câu cá và Quán trọ thêm 700–800 bi mỗi ngày. Bàn may rủi (Blackjack,
   Roulette, Slot) gần như không ảnh hưởng gì: cược quá nhỏ so với thu nhập.
3. **Kinh tế nền (không ra đảo) đúng nhịp đã thiết kế**, có vài chỗ lệch: trứng trong rương máy bi cho gấp khoảng 9 lần số mảnh so với trước
   khi đổi sang trứng; gói Bỏ quảng cáo 4,99 USD thành +1.500 bi mỗi ngày mãi mãi; Lọ Bi rẻ gấp 5 lần gói bi và mua lại được vô hạn; Gói Tiếp
   Sức không bao giờ bật; IAP gần như không bán đá tiến hóa, thứ người chơi kẹt nhiều nhất.
4. **Bộ số đề xuất (bộ B)** đưa đảo về +11% bi so với người không ra đảo, không còn ai vỡ, tiến độ nền giữ nguyên. Chi tiết ở mục 5.
5. **Muốn người chơi mua nhiều hơn thì siết bi không phải đòn chính.** Thiếu thứ Clash of Critters có: chỗ tiêu bi không đáy (đường thưởng sự
   kiện 3 ngày tốn khoảng 330.000 bi) và chỗ tiêu dài hạn (745 bản sao mỗi con, 9.600 ải). Ở mình, người chi 600 USD chạm trần cấp 200 ở
   ngày 3, người chăm xem nhiều quảng cáo xong cả 350 ải ở ngày 19. Mục 5.4 đề xuất ba việc cho phần này.

## 1. Cách giả lập

Công cụ: `ArtGen/KinhTe/gia_lap/` (README ở đó). Biên dịch thẳng lõi game `Assets/01 Script/Core` ngoài Unity và gọi đúng các hàm của game:
`Progress`, `Pachinko`, `Afk`, `Trees`, `Shop`, `Offers`, `Eggs`, `AdGate`, `Casino` và sáu trò của đảo. Tỉ lệ thắng ải lấy từ máy tự đánh
(`Sim.Stage`) cộng mức "người giỏi hơn máy", như `ProgressSim` đang có.

**300 người** = 3 mức chơi × 5 nhóm tiền × 2 (không ra đảo / có ra đảo) × 10 người, 30 ngày. Cặp "không đảo / có đảo" dùng chung hạt giống.

| Mức chơi | Phiên / ngày | Trận / phiên | Ngày có chơi |
|---|---|---|---|
| Chăm | 6 | 5 | 100% |
| Vừa | 3 | 3 | 95% |
| Ít | 1 | 2 | 80% |

| Nhóm tiền | Quảng cáo | Tiền (trần 30 ngày) | Mua gì (giả định) |
|---|---|---|---|
| F0 | không xem | 0 | |
| FA | nửa xem ít (tối đa 6 lượt / ngày), nửa xem nhiều (tối đa 25) | 0 | |
| P1 chi ít | tối đa 10 | 15 USD | Quà Nhập Môn, Thẻ Tuần, có người mua Thẻ Phiêu Lưu, gói ≤ 1,99 |
| P2 chi vừa | tối đa 15, mua Bỏ quảng cáo | 80 USD | thêm Gói Khởi Hành, Quỹ, Lọ Bi khi đầy, Chuỗi Quà tới 2,99, ưu đãi tới 9,99 |
| P3 chi lớn | như P2 | 600 USD | gần như mọi thứ, bổ sung bi 2 lần / ngày, trứng ×10 hằng tuần |

Người ra đảo chia đôi: **thận trọng** (chỉ cược mức có lợi: đua 100 bi, bàn 10 ván bậc thấp, hầm đấu chỉ đánh đội yếu hơn mình) và **máu me**
(đua 500 bi, chơi hết lượt bàn ở bậc cao nhất, mua mọi thứ ở Chợ đen).

**Bốn bộ số** (300 người mỗi bộ): `goc` game hiện tại; `A` chỉ tắt bán thẻ thừa; `B` đề xuất; `C` = B + siết bi thụ động 25%.

**Giới hạn, đọc số phải nhớ:**
- Mua gì, xem quảng cáo nào là **giả định của tôi**, không phải dự báo doanh thu. Số dùng được là "mỗi USD / mỗi lượt xem mua được bao nhiêu
  tiến độ" và "người không trả tiền kẹt ở đâu".
- Chưa mô phỏng Đền Huy Hiệu, Hang Tiềm Năng (đá cộng gần đúng theo cấp như `ProgressSim.SideEvo`), công trình Nhà ngoài cây bi và ruộng,
  người chơi bỏ game.
- Mỗi ô chỉ 5–10 người: chênh dưới khoảng 10% giữa hai ô chưa nói được gì.
- Người chơi ảo luôn thả hết bi mỗi phiên và nâng cấp ngay khi đủ.

## 2. Game hiện tại đo được gì

### 2.1. Lỗ vỡ kinh tế: bán thẻ thừa ở Chợ đen

`BlackMarket.SellSpare`: mỗi bản sao thừa (thẻ đã cấp 5) bán 6 bi × bậc cấp (tới ×3), không trần. Mỗi bi thả ra khoảng 0,08 bản sao từ
rương, cộng 0,08 mảnh từ trứng rương; mảnh của tướng đã 20 sao lại đổi thành bản sao. Khi đủ thẻ cấp 5, một bi thả thu về hơn một bi.

| Mức chơi | Kiểu ra đảo | Số người vỡ (F0 + FA) | Ngày vỡ, trung vị (sớm nhất – muộn nhất) |
|---|---|---|---|
| Chăm | thận trọng | 10 / 10 | 5 (4–6) |
| Chăm | máu me | 10 / 10 | 6,5 (4–10) |
| Vừa | thận trọng | 10 / 10 | 7 (6–10) |
| Vừa | máu me | 10 / 10 | 11,5 (8–14) |
| Ít | thận trọng | 10 / 10 | 18,5 (16–21) |
| Ít | máu me | 10 / 10 | 23 (16–30) |

Tính cả nhóm trả tiền: 150 / 150 người có ra đảo vỡ. Chi tiết: `ArtGen/KinhTe/gia_lap/ket_qua/tong_hop_goc.md`.

### 2.2. Đảo Casino sau khi khoá lỗ đó (bộ A)

Bi mỗi ngày của người không trả tiền, không xem quảng cáo (F0), trung bình 30 ngày:

| Mức chơi | Không ra đảo | Ra đảo thận trọng | Ra đảo máu me |
|---|---|---|---|
| Chăm | 1.752 | 6.126 (×3,5) | 3.354 (×1,9) |
| Vừa | 1.016 | 4.131 (×4,1) | 1.718 (×1,7) |
| Ít | 498 | 2.099 (×4,2) | 603 (×1,2) |

Hệ quả: người chăm F0 ra đảo thận trọng chạm cấp 200 và xong 350 ải ở **ngày 15** (không ra đảo: cấp 186 ở ngày 30). Người vừa F0 chạm cấp
200 ở ngày 19 (không ra đảo: cấp 143 ở ngày 30). Luật 5 của `29_DaoCasino.md` ("không kiểu nào lên cấp nhanh hơn quá 10%") vỡ hoàn toàn.

Từng trò (người chăm, F0 + FA, bi mỗi ngày):

| Trò | Thận trọng: bỏ ra → nhận | Ròng | Máu me: bỏ ra → nhận | Ròng | Nhận xét |
|---|---|---|---|---|---|
| **Hầm đấu** | 1.853 → 4.633 | **+2.780** | 958 → 2.382 | +1.424 | thắng 135 / 135 trận khi chỉ đánh đội yếu hơn; kèm 22 mảnh và 3,4 đá tiến hóa mỗi ngày |
| Câu cá | 0 → 466 | +466 | 0 → 501 | +501 | 10 mồi free, giá cá nhân bậc cấp; bằng cả vườn cây bi |
| Quán trọ | 0 → 304 | +304 | 0 → 353 | +353 | 3 việc × 30–40 bi × bậc cấp |
| Đua | 498 → 604 | +106 | 1.974 → 1.633 | −341 | cược 100 nhận về 1,2 lần; cược 500 nhận về 0,8 lần |
| Blackjack + Roulette + Slot | 89 → 93 | +3 | 2.213 → 2.174 | −39 | hoàn trả 0,95–1,0 trên số cược nhỏ: không phải nguồn, cũng không phải chỗ tiêu |
| Hũ bàn | | +2 | | +5 | 2 mảnh khách mời mỗi ngày ở bậc cao |
| Chợ đen (mua) | 20 → 6 | −14 | 607 → 6 | −601 | chỗ tiêu bi thật duy nhất: 6,5 mảnh mỗi ngày, khoảng 92 bi mỗi mảnh |

Mảnh từ đảo chỉ bằng 4–7% các nguồn khác, đá tiến hóa 8–18%: phần này đúng luật 3 của `29`. Vấn đề của đảo là **bi**.

### 2.3. Kinh tế nền (không ra đảo)

| Nhóm | Cấp ngày 7 / 14 / 30 | Ải ngày 30 | Bi thu / ngày | Chạm cấp 200 | Xong 350 ải |
|---|---|---|---|---|---|
| Chăm F0 | 72 / 111 / 186 | 344 | 1.752 | chưa | 4 / 10 người ở ngày 30 |
| Chăm FA xem nhiều | 99 / 157 / 200 | 350 | 3.620 | ngày 20 | ngày 19 |
| Chăm P1 (14 USD) | 106 / 162 / 200 | 350 | 3.596 | ngày 20 | ngày 19 |
| Chăm P2 (80 USD) | 163 / 200 / 200 | 350 | 7.315 | ngày 10 | ngày 12 |
| Chăm P3 (600 USD) | 200 / 200 / 200 | 350 | 25.022 | **ngày 3** | ngày 12 |
| Vừa F0 | 57 / 86 / 143 | 239 | 1.016 | chưa | chưa |
| Vừa FA xem nhiều | 84 / 129 / 200 | 251 | 2.267 | ngày 27 | chưa |
| Vừa P2 | 157 / 200 / 200 | 260 | 5.921 | ngày 11 | chưa |
| Ít F0 | 33 / 60 / 98 | 50 | 498 | chưa | chưa |

Bi của người chăm F0: ải 738, cây bi + Nhà 827, quà free 187. Của người vừa F0: ải 202, cây + Nhà 657, quà 157.

- Nhịp này khớp mốc cũ ("vừa tới cấp 200 khoảng ngày 46"). Tôi không đề xuất đổi đường cong EXP hay giá lên sao.
- **Mảnh từ trứng rương máy bi lấn át mọi nguồn**: người chăm F0 nhận 6.109 mảnh / 30 ngày từ máy, so với 335 từ ải và 237 từ AFK. Người chi
  600 USD nhận 1.575 mảnh từ IAP và 25.477 từ máy. Lý do: ngày 2026-11-23 dòng "1–2 mảnh" (rương bạc 4,6%) và "2–4 mảnh" (rương vàng 8,8%)
  đổi thành 1 trứng = 12–16 mảnh, tức khoảng 9 lần. Trứng đó là Thường / Khá nên không lấn Hiếm trở lên, nhưng làm gói Trứng Khá 0,99 USD vô
  nghĩa (người chăm F0 nhận 5 quả mỗi ngày) và mọi tướng Thường, Khá của người chăm ra đảo lên 20 sao trong 30 ngày.
- **Đánh lại ải cho đủ bi, không giới hạn**: ải sâu cho tới 70 bi mỗi trận thắng. Người chăm sau khi kẹt hoặc xong nội dung cày 1.000–1.700 bi
  mỗi ngày từ đây.
- **Trần cấp 200**: bi chủ yếu ra EXP; chạm trần thì bi mất gần hết tác dụng (EXP thừa chỉ góp tối đa 7 nét Sổ Phép).

### 2.4. Quảng cáo thưởng

| Nhóm | Lượt xem / ngày | Bi từ quảng cáo / ngày | So với thu nhập F0 | Mảnh / ngày |
|---|---|---|---|---|
| Chăm, xem ít | 6 | 531 | +30% | 17 |
| Chăm, xem nhiều | 25 | 1.311 | +75% | 35 |
| Vừa, xem ít | 6 | 494 | +49% | 21 |
| Vừa, xem nhiều | 21 | 1.260 | +124% | 43 |
| Ít, xem nhiều | 8 | 768 | +154% | 28 |

- Mỗi lượt xem đáng 52–88 bi (6 lượt đầu đáng nhất). Chỗ được dùng nhiều: thưởng ải ×2 (3,9 lượt / ngày), bi miễn phí (3,8), hái ×2, tăng
  tốc AFK, nâng rương (2,2 mỗi chỗ).
- Quảng cáo đang làm đúng việc: xem nhiều thì tiến độ gần bằng người chi 14 USD. Giữ nguyên 12 chỗ đặt và trần.
- **Lệch: gói Bỏ quảng cáo (4,99 USD, một lần).** Người mua nhận khoảng 20 lượt trao ngay mỗi ngày = **1.520–1.620 bi mỗi ngày mãi mãi**, mà
  không còn xem quảng cáo nào (mất luôn doanh thu quảng cáo của nhóm chịu chi). Đây là gói hời nhất game, hơn mọi gói bi cộng lại.

### 2.5. IAP: mỗi USD mua được gì

| Gói | Bi / USD | Mảnh / USD | Ghi chú |
|---|---|---|---|
| Thẻ Phiêu Lưu (4,99) | 2.251 | 2,8 | chưa tính cây bi ×1,5; với người vừa là +60% thu nhập cả tháng |
| **Lọ Bi (4,99)** | **2.163** | | người chi lớn đập 28 lần / 30 ngày: lọ đầy lại ngay vì họ thả 40.000 bi mỗi ngày |
| Quỹ Phiêu Lưu (9,99) | 1.595 | 39 | |
| Thẻ Tuần (1,99) | 1.286 | | |
| Ưu Đãi Bất Ngờ | 984 | 3,9 | |
| Gói Đồng Hành / Sắp Lên Sao | 680–774 | 8 | |
| Chuỗi Quà | 463 | 9,3 | |
| **Gói Khởi Hành (4,99)** | **357** | 8,3 | gói một lần đầu đời mà kém hơn cả ưu đãi thường ngày |
| Quà Nhập Môn (0,99) | 303 | 38 | |
| Bổ sung bi (4,99 / 9,99) | 191 / 428 | | |
| Gói bi (0,99 → 99,99) | 176 → 450 (lần đầu ×2) | | |
| Trứng Hiếm hôm nay (0,99) | | 13,9 | |
| 10 Trứng Sử Thi / Huyền Thoại | | 7,0 / 3,5 | |

- Gói 4,99 USD bi (550 bi × bậc cấp) bằng khoảng **1,1 ngày** thu nhập của người vừa F0, 0,5 ngày của người chăm xem quảng cáo. Clash of
  Critters: gói 4,99 USD bằng 0,9–1,4 ngày phần thu cố định (mục 3). Mức giá bi gốc của mình **đang đúng tầm**, không cần đổi.
- **Đá tiến hóa gần như không mua được**: 0–0,6 đá mỗi USD. Người chi 600 USD nhận 9 đá từ IAP trên tổng 1.925 (phần lớn từ rương máy bi).
  Trong khi đó người chơi kẹt đá (có tướng tới mốc tiến hóa, đủ cấp, thiếu đá) ở 168 / 180 phiên với người chăm F0, 74 / 83 phiên với người vừa.
- Lọ Bi rẻ gấp 5 lần gói bi và mua lại được ngay: không ai có lý do mua gói bi.

### 2.6. Người chơi kẹt ở đâu

| Nhóm (không ra đảo) | Trận thua / 30 ngày | Lần gặp tường (ải kế thắng dưới 30%) | Trận phải đánh lại ải cũ |
|---|---|---|---|
| Chăm F0 | 302 | 370 | 255 / 900 |
| Chăm FA | 179 | 154 | 380 / 900 |
| Chăm P2 | 1 | 3 | (xong nội dung ngày 12) |
| Vừa F0 | 9 | 3 | 3 / 250 |
| Vừa FA | 2 | 0 | 0 |
| Ít | 1 | 0 | 0 |

- **Chỉ người chăm mới thấy thiếu.** Họ đánh 30 trận mỗi ngày, vượt trước cấp của mình, gặp tường liên tục: đây là nhóm sẽ xem quảng cáo và mua.
- **Người vừa và ít không bao giờ kẹt**: tiến độ của họ bị chặn bởi số trận họ chịu đánh, không phải tài nguyên. Bi thêm không giúp họ đi
  nhanh hơn, nên gói bi không có lý do với họ. Thứ bán được cho nhóm này là sưu tầm (tướng Hiếm trở lên) và tiện lợi.
- **Gói Tiếp Sức bật 0 lần** trên 300 người × 30 ngày, dù người chăm F0 thua 302 trận. `Offers.FreeFix` coi "còn ≥ 20 bi để thả" là còn cách
  miễn phí, mà sau trận nào người chơi cũng có hơn 20 bi.
- Popup bán: người F0 thấy khoảng 30 cái trong 30 ngày (1 mỗi ngày), trần cho phép 4 mỗi ngày. Không cần nới trần; cần bật đúng lúc.

## 3. Clash of Critters phân bổ tài nguyên thế nào

Bản đầy đủ có nguồn: `GD_Claude/research_notes/Kinh te Clash of Critters.md`. Phần shop đã mổ ở `26` mục 1.

| | Clash of Critters | PokiClash hiện tại | Rút ra |
|---|---|---|---|
| Bi free cố định / ngày | 950–1.100 (cây 800 + quà 60 + nhiệm vụ 90) | vừa F0: 1.016 | cùng tầm |
| Gói 4,99 USD | 900–1.440 bi = 0,9–1,4 ngày | 550 × bậc cấp = 1,1 ngày | cùng tầm, giữ |
| Bi từ ải thường | **0** (bỏ từ 8/2025), chỉ boss mỗi 10 ải | mỗi trận thắng, đánh lại không giới hạn | giảm dần khi đánh lại (5.2) |
| Vốn để cược ×N | 60–90 lần mức cược | ×10 cần 700 bi (70 lần) | đã giống |
| Chỗ tiêu bi lớn nhất | đường thưởng sự kiện 150 bậc ≈ 330.000 bi, 3 ngày một kỳ, hoàn 12%; người free tới bậc 40–50 | không có | **thiếu** (5.4) |
| Chỗ tiêu dài hạn | 745 bản sao mỗi con (≈ 3.000 USD), 9.600 ải, cấp 3.600 | 480 mảnh mỗi tướng, 350 ải, cấp 200 | nông hơn nhiều (5.4) |
| Thứ bán chính | Wishbox 4–5 USD = 1 bản sao **tự chọn** | trứng ngẫu nhiên trong bậc, vé chọn tướng không bán lẻ | bán thứ đang nghẽn (5.3) |
| Thẻ tháng | 19,99 USD: +20% bi cố định, giá trị thật là 27 Wishbox | 4,99 USD: +60% bi cho người vừa | mình rẻ và hời hơn hẳn; thử 9,99 khi có số đo (`26` câu 11) |
| Tiền cao cấp | gem chỉ mua bằng tiền | không có | giữ |
| Quảng cáo thưởng | không có, người chơi xin | 12 chỗ | lợi thế của mình |
| Tường | có, đã phải nới chương 19–23 | chỉ người chăm gặp | xem 5.5 |

Ba điều họ làm mà mình chưa: (1) bi luôn có chỗ tiêu nhờ sự kiện xoay vòng, người chơi được dạy "tích bi cho sự kiện"; (2) tiến độ không có
đáy, nên người chi lớn không bao giờ hết thứ để mua; (3) ải thường không cho bi, bi chỉ đến từ thời gian (cây) và tiền.

## 4. Mục tiêu cân

| | Mục tiêu | Hiện tại (A) | Bộ B |
|---|---|---|---|
| M1 | Không kiểu chơi nào vỡ kinh tế | 150 người vỡ (bộ gốc) | 0 |
| M2 | Bi ròng từ đảo ≤ 15% thu nhập người không ra đảo | +200–300% | +11% (người chơi ít: +18%) |
| M3 | Ra đảo không lên cấp nhanh hơn quá khoảng 10% | chăm: cấp 200 ở ngày 15 so với cấp 186 ở ngày 30 | ngày 14: +14%; ngày 30: +8–10% |
| M4 | Tiến độ nền giữ nhịp đã duyệt | | lệch dưới 3% |
| M5 | Không gói nào hời tới mức làm các gói khác vô nghĩa | Bỏ quảng cáo, Lọ Bi | đã chặn |
| M6 | Thứ người chơi kẹt thì mua được | đá tiến hóa không mua được | đề xuất 5.3 (chưa đo) |

## 5. Kế hoạch đổi

### 5.1. Đợt 1: sửa đảo Casino (bắt buộc trước khi phát hành đảo)

Số ở `balance.json`, khối `casino`; riêng việc 1 phải sửa code.

| # | Chỗ | Hiện tại | Đề xuất | Vì sao |
|---|---|---|---|---|
| 1 | Chợ đen, thu mua thẻ thừa (`BlackMarket.SellSpare`, `market.copySell`) | 6 bi × bậc cấp mỗi bản sao, không trần | **không đổi ra bi nữa**: 10 thẻ thừa → 1 đá tiềm năng, tối đa 20 đá mỗi ngày | vòng lặp vô hạn (2.1) |
| 2 | Hầm đấu `underground.winMult` | 2,5 | **1,0** (thắng hoàn lệ phí, thua mất) | thưởng của Hầm đấu là mảnh và đá, không phải bi |
| 3 | Hầm đấu, mảnh mỗi bậc `tiers[].shards` | 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 10 | 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5 | 22 mảnh mỗi ngày gồm cả tướng Sử thi, Huyền thoại, nhiều hơn mọi gói trứng |
| 4 | Hầm đấu, đá tiến hóa | 1 đá ở mỗi bậc từ Lục Bảo (5 bậc) | bậc Lục Bảo, Kim Cương đổi thành 4 và 5 đá tiềm năng; 3 bậc trên cùng giữ 1 đá | 150 đá mỗi tháng là +37% nguồn đá |
| 5 | Câu cá `fishing.price` | 3, 6, 12, 30, 80 | 1, 1, 2, 6, 15 | 471 bi mỗi ngày từ mồi free |
| 6 | Câu cá, thưởng loài mới `fishing.first` | 10, 15, 25, 50, 100 | 3, 5, 8, 15, 30 | |
| 7 | Cá Vua `fishing.king` | 150 bi | 50 bi (mảnh, đá giữ) | |
| 8 | Quán trọ, bi mỗi việc | 30 / 40; xong cả ba: 60 bi + 5 mồi | 6 / 8; xong cả ba: 10 bi + 3 mồi | 305 bi mỗi ngày |
| 9 | Đua `race.oddsLow` (nhất / nhì / ba ở cược nhỏ) | 18% / 20% / 24% (nhận về 1,18) | 13,5% / 17% / 23,5% (nhận về 0,98) | cược nhỏ đang lãi chắc; `oddsHigh` giữ như người dùng đặt |
| 10 | Lễ Hội Đua `mult` | ×1,5 phần lời | ×1,25 | cược nhỏ trong lễ hội còn lãi 9%, đủ là sự kiện |
| 11 | Cúp đua tuần, bi | 120 / 200 / 300 | 40 / 66 / 100 | |

Bàn may rủi, Hũ bàn, giá Chợ đen: **giữ nguyên**. Sau các đổi trên, người ra đảo máu me lỗ 240–300 bi mỗi ngày (đua cược 500, mua chợ):
đảo thành chỗ tiêu bi nhẹ cho người thích cược, đúng ý "cược càng cao tỉ lệ thắng càng thấp".

### 5.2. Đợt 2: bịt các chỗ lệch của kinh tế nền

| # | Chỗ | Hiện tại | Đề xuất | Sửa ở |
|---|---|---|---|---|
| 12 | Trứng trong rương máy bi | bạc 4,6% Trứng Thường; vàng 8,8% Trứng Khá | bạc **1%**, vàng **2,5%**; phần trọng số dư chuyển sang dòng EXP | `pachinko.chests` |
| 13 | Đánh lại ải đã qua | luôn đủ bi | **10 trận đầu mỗi ngày đủ bi, sau đó 25%**; ải mới không đổi | `Progress.WinStage` + đếm theo ngày trong bản lưu |
| 14 | Bỏ quảng cáo | mọi lượt trao ngay | **8 lượt trao ngay mỗi ngày**, các lượt sau vẫn xem được như thường | `AdGate` / `Ads` |
| 15 | Lọ Bi | đập lại ngay khi đủ 40% | **cách nhau ít nhất 3 ngày** (đồng hồ hiện trên lọ) | `Shop.PiggyCanBreak` |
| 16 | Gói Tiếp Sức | không bao giờ bật | "còn cách miễn phí" chỉ tính lên sao, tiến hóa, nâng thẻ; không tính dòng "thả bi" | `Offers.FreeFix` |

Việc 12 đổi lời dặn 2026-11-23 ("cho rương máy bi rơi trứng đi"): trứng vẫn rơi, hiếm hơn. Sau khi đổi, mảnh từ máy vẫn gấp khoảng 2 lần
trước ngày 23.

### 5.3. Đợt 3: gói bán (chưa đo bằng giả lập, số đầu)

| # | Việc | Đề xuất |
|---|---|---|
| 17 | Bán đá tiến hóa | Gói "Đá tiến hóa hôm nay": 5 đá 1,99 USD, 1 lần mỗi ngày; "Túi đá tuần": 15 đá + 1 Trứng Sử Thi 4,99 USD, 1 lần mỗi tuần. Thẻ Phiêu Lưu thêm 1 đá mỗi ngày. Người chăm F0 kiếm khoảng 12 đá mỗi ngày, một tướng cần 195 |
| 18 | Gói Khởi Hành | 1.200 → 2.000 bi, 2 → 5 đá tiến hóa: phải là gói hời thứ hai sau Quà Nhập Môn, hiện kém hơn ưu đãi thường ngày |
| 19 | Trứng Khá 0,99 USD (`egg_1`) | bỏ khỏi lưới bán; máy bi và quảng cáo đã cho bậc Thường, Khá. Cửa hàng chỉ bán từ Hiếm |
| 20 | Vé chọn tướng | bán lẻ 1 vé Hiếm mỗi tuần 2,99 USD (hiện không bán lẻ): học Wishbox, người chơi trả cho đúng con mình nuôi |
| 21 | Thẻ Phiêu Lưu | giữ 4,99 USD lúc ra mắt; khi có số đo thật thử 9,99 (`26` câu 11): với người vừa nó là +60% thu nhập |

### 5.4. Đợt 4: cho bi và tiền có chỗ tiêu không đáy (cần kế hoạch riêng)

Đây là phần quyết định "kích mua", và siết số không thay được.

1. **Đường thưởng sự kiện của Bến Lữ Khách** (học đường 150 bậc của Critters). Mỗi sự kiện 3 ngày (Đêm Bài, Vòng Xoay, Hội Máy Quả, Lễ Hội
   Đua) có một đường 60 bậc, điểm = bi đã thả ở máy + bi đã cược ở lều; thưởng là mảnh tướng khách mời, trứng Hiếm / Sử Thi, đá, trang trí
   Nhà. Mốc theo số đo của bộ B (bi thả mỗi kỳ 3 ngày): vừa F0 khoảng 4.900, chăm FA khoảng 13.600, P2 khoảng 32.000, P3 khoảng 78.000. Đặt
   bậc 15 ở 5.000 điểm, bậc 30 ở 14.000, bậc 45 ở 32.000, bậc 60 ở 80.000. Bi mua thêm có ích cả khi đã chạm trần cấp; Hũ bàn nhập vào đây.
2. **Sau trần cấp 200**: EXP thừa hiện chỉ góp tối đa 7 nét Sổ Phép. Đổi thành "rương mốc" mỗi 9.000 EXP (bằng một cấp ở cấp 200), không
   trần, ra mảnh tướng đang nuôi và đá. Người chi lớn chạm trần ngày 3, người chi vừa ngày 10, người xem quảng cáo chăm chỉ ngày 20.
3. **Nội dung sau 350 ải**: người chăm xong ở ngày 12–25 (F0: sau ngày 30). Tháp vô tận hoặc ải tuần đã có ý ở `09_CheDoKhac.md`, `20_TangDayNoiDung.md`.

### 5.5. Phương án C (siết bi thụ động 25%): đo rồi, **đề xuất chưa làm**

Cây bi 4 → 3 bi mỗi giờ, chứa 96 → 72; ruộng Nhà 2 → 1,5 bi mỗi giờ.

| Nhóm (không ra đảo) | Cấp ngày 30: B → C | Ải ngày 30 | Trận thua | Lần gặp tường |
|---|---|---|---|---|
| Chăm F0 | 181 → 165 | 332 → 293 | 281 → 289 | 391 → 446 |
| Vừa F0 | 145 → 128 | 236 → 216 | 11 → 28 | 8 → 14 |
| Vừa FA | 192 → 176 | 260 → 256 | 1 → 1 | 0 → 0 |
| Ít F0 | 97 → 84 | 48 → 46 | 1 → 1 | 0 → 0 |

Mọi người chậm đi khoảng 10%, nhưng người vừa vẫn hầu như không kẹt (14 lần gặp tường trong 30 ngày), nên không sinh thêm lý do mua. Muốn
người vừa kẹt đều phải cắt 40–50%, rủi ro bỏ game lớn mà giả lập không đo được. Nên phát hành với bộ B, lấy số thật rồi mới quyết.

## 6. Bộ B đo được gì

Người không trả tiền, không xem quảng cáo (F0):

| Nhóm | Bộ | Cấp ngày 7 / 14 / 30 | Ải ngày 30 | Bi thu / ngày | trong đó đảo | Mảnh 30 ngày | Đá 30 ngày |
|---|---|---|---|---|---|---|---|
| Chăm, không ra đảo | A | 72 / 111 / 186 | 344 | 1.752 | | 6.694 | 409 |
| | **B** | 71 / 110 / 181 | 332 | 1.620 | | 2.057 | 360 |
| Chăm, đảo thận trọng | A | 111 / 196 / 200 | 350 | 6.126 | +3.466 | 13.406 | 862 |
| | **B** | 84 / 125 / 200 | 350 | 1.992 | +178 | 2.540 | 524 |
| Chăm, đảo máu me | A | 74 / 132 / 200 | 350 | 3.354 | +1.105 | 10.240 | 635 |
| | **B** | 68 / 100 / 150 | 275 | 1.183 | −242 | 1.981 | 300 |
| Vừa, không ra đảo | A | 57 / 86 / 143 | 239 | 1.016 | | 4.095 | 224 |
| | **B** | 55 / 87 / 145 | 236 | 1.005 | | 1.294 | 222 |
| Vừa, đảo thận trọng | A | 89 / 154 / 200 | 249 | 4.131 | +2.914 | 14.859 | 564 |
| | **B** | 60 / 94 / 157 | 250 | 1.193 | +113 | 1.702 | 281 |
| Vừa, đảo máu me | A | 53 / 86 / 188 | 231 | 1.718 | +685 | 6.840 | 335 |
| | **B** | 42 / 66 / 106 | 167 | 523 | −304 | 1.116 | 132 |
| Ít, không ra đảo | A | 33 / 60 / 98 | 50 | 498 | | 2.086 | 66 |
| | **B** | 30 / 60 / 97 | 48 | 444 | | 607 | 56 |
| Ít, đảo thận trọng | A | 43 / 89 / 199 | 50 | 2.099 | +1.506 | 8.076 | 272 |
| | **B** | 26 / 53 / 99 | 42 | 494 | +78 | 670 | 63 |

- Đảo thận trọng: bi ròng từ đảo còn 78–178 mỗi ngày (khoảng 11% thu nhập nền). Người chăm vẫn nhanh hơn 14% ở ngày 14 vì mảnh và đá Hầm
  đấu làm đội mạnh lên, qua ải nhanh hơn: đó là phần thưởng đúng nghĩa của trò tay nghề.
- Đảo máu me giờ chậm hơn người không ra đảo 17–36% về cấp ở ngày 30. Nếu thấy phạt nặng quá thì nới `oddsHigh` của đua (cược 500 đang nhận về 0,77).
- Tiến độ nền gần như không đổi dù mảnh từ máy giảm hai phần ba: mảnh đó rải vào tướng Thường, Khá ngoài đội.
- Nhóm trả tiền: P1 chạm cấp 200 ngày 19 (trước 20), P2 ngày 10,5, P3 ngày 3. Lọ Bi còn 5,9 lần mỗi người mua trong 30 ngày (trước 16,8),
  1.733 bi mỗi USD. Gói Tiếp Sức bật 3 lần mỗi người F0. Bi thu của P3 còn 16.039 mỗi ngày (trước 25.022) do Lọ Bi và Bỏ quảng cáo bị chặn.

Bảng đủ mọi nhóm: `ArtGen/KinhTe/gia_lap/ket_qua/so_sanh.md`, `tong_hop_B_de_xuat.md`.

## 7. Câu cần chốt

| # | Câu | Đề xuất |
|---|---|---|
| 1 | Làm đợt 1 (11 đổi của đảo Casino) ngay? | có; đây là lỗi chặn phát hành |
| 2 | Thẻ thừa đổi ra gì | đá tiềm năng có trần ngày; hoặc bỏ hẳn mục thu mua |
| 3 | Hầm đấu thắng chỉ hoàn lệ phí (không lãi bi)? | có; nếu muốn có lãi thì tối đa 1,1 |
| 4 | Trứng rương máy bi hiếm lại (việc 12)? Đổi lời dặn 2026-11-23 | có |
| 5 | Đánh lại ải giảm bi sau 10 trận mỗi ngày (việc 13)? | có |
| 6 | Bỏ quảng cáo chỉ trao ngay 8 lượt mỗi ngày; Lọ Bi cách 3 ngày? | có |
| 7 | Đợt 3 (bán đá tiến hóa, nâng Gói Khởi Hành, bỏ Trứng Khá, bán lẻ vé)? | có, số đầu; đo lại bằng giả lập khi làm |
| 8 | Đợt 4 (đường thưởng sự kiện, rương sau trần cấp): lên kế hoạch riêng? | có; đây là phần tạo lý do mua lâu dài |
| 9 | Phương án C (siết bi thụ động)? | chưa; chờ số thật |

## 8. File

- Công cụ: `ArtGen/KinhTe/gia_lap/` (`chay.py <bộ số>` chạy 300 người, `tong_hop.py`, `so_sanh.py`; bộ số ở `bo_so/*.py`).
- Bảng lượt chạy 2026-11-26: `ArtGen/KinhTe/gia_lap/ket_qua/`.
- Nghiên cứu Clash of Critters: `GD_Claude/research_notes/Kinh te Clash of Critters.md`.
- Liên quan: `26_CuaHang_IAP_QuangCao.md` (gói, popup, quảng cáo), `29_DaoCasino.md` mục 7 (luật cân của đảo), `14_HeThongAi.md` (nhịp ải).
