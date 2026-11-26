# 34. Kiếm tiền và làm khó phá đảo: bi → cấp → vượt ải, gói tướng theo mốc (2026-11-26)

Người dùng dặn 2026-11-26, sau `33_CanBangKinhTe.md`:

> "Giờ làm thế nào để kiếm được tiền của người chơi và làm cho người chơi khó phá đảo hơn."
>
> "Quan trọng nhất là người chơi phải có lí do để phải mua gói trong shop, họ cần phải mua thêm bóng để lên cấp nhanh hơn để vượt ải."
>
> "Nếu cần copy tất cả gói iap của chiến thú, có thể cho người chơi có cơ hội unlock được các tướng ở phần cuối map để mạnh hơn, offer có
> thể thay đổi theo mốc người chơi, giả sử mới chơi có thể có gói unlock tướng mốc 3 ở các đảo, về sau cho unlock mốc 6-7 nhưng mốc 9-10
> là các mốc rất đắt để có. Để tạo cho user biết họ nên mua thì phải quảng cáo sức mạnh các tướng sau phải có sức mạnh khác biệt với các
> con đầu. Cần thì tăng gap sức mạnh lên."

**Trạng thái 2026-11-26 (tối):** việc 1, 2 và một phần việc 3 của mục 4 đã áp vào game; bảng việc và số đo lại ở `33_CanBangKinhTe.md`
mục 0. Đường EXP áp bản hai đoạn max(45 × cấp, 9 × cấp^1,54): 20 cấp đầu y như cũ. Phần còn lại của file là bản kế hoạch. Số đo bằng công cụ `ArtGen/KinhTe/gia_lap/` (người chơi ảo chạy lõi game, 90 ngày). Mọi bộ số ở
đây xây trên bộ B của `33` (đã sửa đảo Casino và các chỗ lệch); chưa làm `33` đợt 1–2 thì bi còn thừa, mọi thứ dưới đây không có tác dụng.

"Mốc" trong file này: 10 tướng của mỗi đảo theo thứ tự ải tướng (ải 1, 5, 10, 15, 20, 30, 40, 50, 60, 70).

## Tóm tắt

1. **Đòn chính là đường EXP.** Hiện EXP lên cấp = 45 × cấp. Tường do thiếu cấp quá mỏng: ở cấp 150 thiếu 4 cấp thì chờ khoảng một ngày
   là qua, gói bi 4,99 USD mua được 2,3 cấp. Đổi sang **9 × cấp^1,54** (20 cấp đầu nhanh như cũ, cấp 200 tốn gấp 3,5 lần) thì người không
   trả tiền phá đảo chậm gấp 1,7–2,2 lần, người chơi vừa bắt đầu gặp tường đều (7 → 112 lần mỗi 30 ngày), và trả tiền vẫn đi nhanh gấp 2,5 lần.
2. **Boss mạnh hơn không có tác dụng** (đã đo: 55 ngày so với 55 ngày). Không làm.
3. **Gói tướng theo mốc làm được, nhưng là "cú nhảy" chứ không thay được bi.** Ở từng trận, tướng mốc sau khác biệt rất rõ (ải 12: tướng
   khởi đầu cần cấp 42, tướng mốc 6 thắng 90% ở cấp 22, tướng mốc 9 thắng ở cấp 12). Nhưng tính cả hành trình thì một gói tướng chỉ giúp
   đi trước 4–10 ngày, và chỉ khi đủ ba điều kiện: tướng đi trước người chơi ít nhất 3 mốc, kèm sẵn sao + cấp thẻ + đá tiến hóa, và offer
   đổi theo mốc người chơi đang đứng. Chỉ mở khoá suông (1 sao, thẻ cấp 1) thì tác dụng bằng 0.
4. **Gói của Critters:** mình đã có phần lớn. Thiếu bốn thứ đáng chép: nạp đầu 3 bậc kèm tướng, gói 7 ngày, bán lẻ vé chọn tướng, đường
   thưởng sự kiện.

## 1. Vòng lõi: thiếu cấp → cần bi → mua bi

### 1.1. Vì sao hiện gói bi chưa có lý do

Cấp địch chạy từ 1 (ải 1) tới 195 (ải 70) trên mỗi đảo; thiếu khoảng 10 cấp là thua chắc. Vậy **cấp là thứ chặn phá đảo**, và cấp đến
từ bi (đo được khoảng 9,4 EXP mỗi bi thả, tính cả rương và mốc quà). Vấn đề là mỗi cấp quá rẻ:

| Ở cấp 150, thiếu 4 cấp | Hiện tại (45 × cấp) | Đề xuất (9 × cấp^1,54) |
|---|---|---|
| EXP cần | 27.000 | 80.800 |
| Bi cần thả | khoảng 2.900 | khoảng 8.700 |
| Người chăm không trả tiền chờ | khoảng 1 ngày | khoảng 4 ngày |
| Trả để qua ngay (theo giá gói 19,99 USD) | khoảng 7 USD | khoảng 22 USD |

Chờ một ngày thì không ai mua. Chờ bốn ngày, trong khi một gói 19,99 USD giải quyết ngay, mới là lựa chọn có sức nặng.

### 1.2. Đường EXP đề xuất

`balance.json` → `progression.expBase` 45 → **9**, `expPow` 1,0 → **1,54**.

| Cấp | EXP lên cấp: hiện → đề xuất | Gói 4,99 USD mua được (cấp): hiện → đề xuất | Gói 19,99 USD: hiện → đề xuất |
|---|---|---|---|
| 10 | 450 → 312 | (đầu game nhanh hơn hiện nay) | |
| 30 | 1.350 → 1.694 | 5,7 → 4,5 | 27 → 21 |
| 60 | 2.700 → 4.927 | 3,8 → 2,1 | 18 → 10 |
| 100 | 4.500 → 10.820 | 2,8 → 1,2 | 13 → 5,6 |
| 150 | 6.750 → 20.203 | 2,3 → 0,8 | 11 → 3,6 |
| 195 | 8.775 → 30.261 | 1,7 → 0,5 | 8,3 → 2,4 |

(Gói bi nhân bậc cấp như hiện có: gói 4,99 USD là 550 bi × 1,5 / 2 / 2,5 / 3.) Tổng EXP tới cấp 200 gấp khoảng 2,7 lần.

Sau khi đổi, gói 4,99 USD ở cuối game chỉ còn nửa cấp. Đó là chủ ý: người kẹt tường cuối game phải nhìn sang gói 19,99 và 49,99 USD,
còn gói nhỏ dành cho đầu game. Nếu muốn gói nhỏ vẫn "thấy được" ở cuối game thì nâng hệ số bậc cấp của gói bi (×3 → ×4 từ cấp 130).

### 1.3. Đo 90 ngày: thời gian phá đảo (xong 350 ải), người không ra đảo

| Nhóm | Hiện (bộ B): xong ngày | Đề xuất: xong ngày | Gặp tường / 30 ngày: hiện → đề xuất | Trận thua / 30 ngày |
|---|---|---|---|---|
| Chăm, không trả tiền, không quảng cáo | 33 | **55** | 145 → 434 | 102 → 297 |
| Chăm, xem ít quảng cáo | 25 | 48 | 76 → 370 | 66 → 242 |
| Chăm, xem nhiều quảng cáo | 18 | 38 | 32 → 280 | 42 → 209 |
| Chăm, chi 15 USD / tháng | 18 | 40 | 27 → 277 | 36 → 208 |
| Chăm, chi 80 USD / tháng | 12 | **22** | 1 → 69 | 0 → 44 |
| Chăm, chi 600 USD / tháng | 12 | 12 | 1 → 0 | |
| Vừa, không trả tiền, không quảng cáo | 48 | **khoảng 104** | 7 → 112 | 13 → 61 |
| Vừa, xem ít quảng cáo | 41 | 78 | 0 → 82 | 0 → 53 |
| Vừa, xem nhiều quảng cáo | 40 | 56 | 0 → 28 | 0 → 23 |
| Vừa, chi 15 USD / tháng | 41 | 54 | 0 → 24 | |
| Vừa, chi 80 USD / tháng | 42 | 40 | 0 → 0 | |
| Ít | hơn 200 | hơn 200 | 0 → 0 | |

Đọc bảng:
- **Khó phá đảo hơn:** người chăm free từ 33 lên 55 ngày, người vừa free từ 48 lên khoảng 104 ngày (ước từ tốc độ 30 ngày cuối).
- **Có lý do mua:** người vừa không trả tiền trước đây gần như không bao giờ kẹt; giờ gặp tường 112 lần mỗi 30 ngày. Người chăm free có
  gần nửa số trận rơi vào lúc kẹt. Đó là những lúc popup "thiếu X cấp, cần Y bi" có nghĩa.
- **Trả tiền thấy khác:** người chăm chi 80 USD mỗi tháng xong ở ngày 22, nhanh gấp 2,5 lần người free. Xem nhiều quảng cáo rút từ 55
  xuống 38 ngày, ngang người chi 15 USD: quảng cáo vẫn là đường "trả bằng thời gian".
- **Hai mức chặn không phải do tiền:** người chi 600 USD dừng ở 12 ngày, người vừa chi 80 USD ở 40 ngày, vì họ chỉ đánh chừng ấy trận
  mỗi ngày. Bán cho họ thứ khác (mục 2, và `33` mục 5.4).
- Người chơi ít (1 phiên, 2 trận mỗi ngày) không đổi gì: họ không kẹt vì cấp.
- Đầu game gần như không chậm đi: cấp ở ngày 7 của người chăm free 71 → 57, người vừa 55 → 48.

**Việc phải soát khi đổi đường EXP** (các mốc mở theo cấp sẽ tới muộn hơn ở nửa sau): ô đội 2 ở cấp 60, ô đội 3 ở cấp 200; tiến hóa cần
cấp 30 / 95 / 150; bậc cấp gói bi 20 / 50 / 90 / 130; cây bi 10 / 25 / 45 / 70; đảo Casino 8–35; Sổ Phép 50. Người chăm free tới cấp 150
ở ngày 60 (trước là khoảng ngày 23). Golden `progression.json` và test tiến trình phải tính lại.

**Muốn khó hơn nữa** thì tăng số mũ; mỗi lần đổi chạy lại `chay.py` 90 ngày để xem bảng trên. Tôi chưa đo mức dốc hơn 1,54.

### 1.4. Boss mạnh hơn: đã thử, không làm

Thêm máu mini boss / boss ×1,8 → ×2,3, công ×1,1 → ×1,25 lên trên đường EXP mới: người chăm free vẫn xong ở ngày 55, người vừa free 104 →
113 ngày, số lần gặp tường gần như không đổi. Người chơi đánh 5 đảo song song nên kẹt một boss thì đi đảo khác, tới lúc quay lại cấp đã đủ.

### 1.5. Bán bi cho đúng lúc

Số liệu chỉ ra chỗ đặt, chưa đo chuyển đổi:
1. **Màn thua và hộp chuẩn bị trận** ghi rõ "Bạn cấp 143, ải này cần khoảng cấp 147: còn thiếu 4 cấp ≈ 8.700 bi", kèm ba lối: chờ (cây
   bi đầy lúc mấy giờ), xem quảng cáo (+N bi), gói bi vừa đủ số còn thiếu. Gói Tiếp Sức hiện có (`26` mục 6.9) đổi nội dung chính thành bi
   theo số cấp còn thiếu.
2. **Bậc gói theo giai đoạn:** dưới cấp 60 đẩy gói 0,99–4,99; cấp 60–130 gói 9,99–19,99; trên 130 gói 19,99–49,99 (bảng 1.2 cho thấy
   gói nào còn mua được trên một cấp).
3. **Lọ Bi, Thẻ Phiêu Lưu, Bỏ quảng cáo** phải theo đúng các chặn của `33` đợt 2, nếu không chúng rẻ hơn gói bi 5 lần và gói bi lại thừa.

## 2. Gói tướng theo mốc

### 2.1. Hiện trạng: tướng mốc sau chưa khác biệt

Sức tướng hiện theo độ hiếm (`HeroStats.RarityPower`), và mốc gắn với độ hiếm như sau:

| Mốc | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Ải | 1 | 5 | 10 | 15 | 20 | 30 | 40 | 50 | 60 | 70 |
| Độ hiếm | Khá | Thường | Khá | Khá | Hiếm | Hiếm | Sử thi | Sử thi | Sử thi | Huyền thoại |
| Hệ số sức hiện tại | 1,10 | 1,00 | 1,10 | 1,10 | 1,23 | 1,23 | 1,38 | 1,38 | 1,38 | 1,76 |
| **Đề xuất** | 1,10 | 1,00 | **1,28** | **1,45** | **1,68** | **1,95** | **2,25** | **2,60** | **3,00** | **3,80** |
| Hơn tướng khởi đầu khoảng (cấp) | 0 | | +5 | +9 | +14 | +19 | +24 | +29 | +34 | +42 |

Hiện tại tướng mốc 3 **bằng đúng** tướng khởi đầu, mốc 6 chỉ hơn 12% (khoảng 4 cấp): bán "gói tướng mốc 3" lúc này là bán thứ không mạnh
hơn. Đề xuất: từ mốc 3, mỗi mốc hơn mốc trước khoảng 15% (bằng khoảng 5 cấp).

Đi kèm bắt buộc: **địch mạnh dần theo mốc.** Từ ải tướng mốc k trở đi, địch mạnh thêm (sức tướng mạnh nhất trước mốc k ÷ sức mốc 1)^0,6.
Không có phần này thì giãn sức chỉ làm game dễ đi. Có phần này, người free vẫn phá đảo trong 52 ngày (so với 55), tức cân bằng tổng thể
không lệch, nhưng ai còn ôm tướng đầu thì tụt lại.

### 2.2. Ở từng trận: khác biệt rất rõ (thứ để quảng cáo)

Tỉ lệ thắng của máy tự đánh, 40 trận mỗi ô, đảo Thủy, bộ đề xuất; mọi tướng 6 sao, thẻ cấp 3:

| Ải (cấp địch) | Tướng | Người chơi kém 30 cấp | kém 20 cấp | kém 10 cấp | bằng cấp |
|---|---|---|---|---|---|
| Ải 12 (42) | mốc 1, khởi đầu | 0% | 0% | 18% | 95% |
| | mốc 3 | 0% | 3% | 60% | 95% |
| | mốc 6 | 15% | 90% | 98% | 100% |
| | mốc 9 | 98% | 100% | 100% | 100% |
| Ải 25 (80) | mốc 1 và mốc 3 | 0% | 0% | 0% | 0% |
| | mốc 6 | 0% | 0% | 0% | 28% |
| | mốc 9 | 0% | 3% | 15% | 90% |
| | mốc 10 | 0% | 20% | 78% | 100% |
| Ải 37 (113) | mốc 6 | 0% | 0% | 0% | 38% |
| | mốc 9 | 0% | 5% | 50% | 93% |
| | mốc 10 | 0% | 28% | 90% | 100% |

Hai điều rút ra:
- Một câu quảng cáo có thật: "Ải này tướng của bạn thắng 18%. Giông Bão (mốc 6) thắng 98%."
- Từ ải 25, tướng 6 sao không đủ dù là mốc nào thấp: giữa game đòi sao bậc Vàng (11 sao trở lên), mà lên bậc cần đá tiến hóa và cấp
  người chơi 95 / 150. **Gói tướng bán ở giữa game phải kèm sao và đá, không thì mua về không dùng được.**

### 2.3. Cả hành trình: gói tướng đáng bao nhiêu ngày

Giả lập phát gói cho mọi người không trả tiền (120 người × 90 ngày), bộ đề xuất 2.1. Tướng là tướng của đảo cùng hệ tướng khởi đầu.

| Thử | Kết quả |
|---|---|
| Chỉ mở khoá (1 sao, thẻ cấp 1): mốc 3 ngày 2, mốc 6 ngày 7 | **không khác gì** (xong ngày 55 so với 52; ải ở ngày 30: 229 so với 230) |
| Gói trọn bộ theo lịch: mốc 3 (3 sao) ngày 2, mốc 6 (6 sao, thẻ 3) ngày 7 | **không khác gì**: người chăm tự tới mốc 6 ở khoảng ngày 15 |
| Thêm mốc 9 (6 sao, thẻ 3) ngày 20 | không nhanh hơn; cuối game còn chậm đi (xem dưới) |
| **Đi trước xa:** mốc 6 ngày 2 + mốc 9 (11 sao, thẻ 4) ngày 7 | người chăm tới 150 ải ở ngày 11 (không gói: 15), 200 ải ngày 22 (25). Người vừa tới 200 ải ngày 32 (37), 300 ải ngày 77 (82) |
| **Đi trước xa:** mốc 6 ngày 2 + mốc 10 (11 sao, thẻ 4) ngày 7 | người chăm: 150 ải ngày 10 (15), 200 ải ngày 19 (25). Người vừa: 200 ải ngày 29 (37), 250 ải ngày 49 (58), 300 ải ngày 72 (82) |

- Gói tướng tốt nhất đo được cho **đi trước 4–6 ngày với người chăm, 5–10 ngày với người vừa**. Sau đó lợi thế mòn dần vì cấp vẫn là thứ
  chặn: tướng mạnh hơn bằng 10 cấp chỉ là 10 cấp đó, còn mỗi ngày người chơi vẫn phải lên cấp để đi tiếp.
- Trong giả lập, người chăm nhận tướng mốc 9 / 10 còn **xong muộn hơn** (61–69 ngày so với 52): người chơi ảo dồn hết đá tiến hóa cho
  tướng vừa mua (đang đứng ở mốc tiến hóa cần 120 đá và cấp 150), bỏ đói các tướng khác. Đây là cách nuôi của người chơi ảo, người thật có
  thể khác, nhưng rủi ro là thật: **bán tướng mà không bán kèm đá thì người mua bị kẹt**.

### 2.4. Vậy bán gói tướng thế nào

Gói tướng là sản phẩm "nhảy cóc", bi là sản phẩm "đi đều". Ba luật rút từ số đo:

1. **Luôn đi trước ít nhất 3 mốc** so với mốc cao nhất người chơi đã qua ở đảo đó. Đây chính là "offer thay đổi theo mốc người chơi".
2. **Trọn bộ:** tướng + mảnh tới bậc sao hợp với chỗ người chơi đang đứng + bản sao thẻ + đá tiến hóa cho lần tiến hóa kế.
3. **Kèm bằng chứng sức mạnh** ngay trên gói (2.5).

| Người chơi đang ở | Gói | Có gì | Giá đề xuất | Căn cứ giá |
|---|---|---|---|---|
| Mới chơi (chưa qua ải 10) | Tướng mốc 3, chọn 1 trong 5 đảo | 3 sao, thẻ cấp 2 | 0,99–1,99 USD | +5 cấp lúc mỗi cấp còn rẻ; chủ yếu là gói nạp đầu |
| Đã qua mốc 3 | Tướng mốc 6 | 6 sao, thẻ cấp 3, 20 đá | 9,99 USD | đi trước 3 mốc ≈ +14 cấp |
| Đã qua mốc 4–5 | Tướng mốc 7–8 | 6 sao, thẻ cấp 3, 55 đá | 19,99 USD | |
| Đã qua mốc 6 | Tướng mốc 9 | 11 sao, thẻ cấp 4, 120 đá | 49,99 USD | 4–8 ngày × khoảng 2.000 bi thả mỗi ngày ≈ 8.000–16.000 bi ≈ 25–50 USD bi |
| Đã qua mốc 7 | Tướng mốc 10 (Huyền thoại) | 11 sao, thẻ cấp 4, 120 đá | 99,99 USD | 6–10 ngày; "rất đắt" như lời dặn |

- Mỗi mốc có 5 tướng (5 đảo): một gói cho chọn 1 trong 5, hoặc bán theo đảo đang kẹt (tướng khắc hệ đảo đó).
- Mua xong, chuỗi gói kế tự mở cho đúng tướng đó (đã có khung: Gói Đồng Hành, Gói Sắp Lên Sao, `26` mục 6.9): mảnh lên sao, đá tiến hóa.
  Đây mới là chỗ thu lâu dài của gói tướng.
- Người free vẫn có tướng đó khi tự đi tới ải của nó. Gói chỉ bán thời gian.

### 2.5. Quảng cáo sức mạnh

| Chỗ | Làm gì | Ghi chú |
|---|---|---|
| Màn thua (từ lần thua thứ 2 ở một ải) | "Tướng của bạn thắng ải này 18%. Với Giông Bão: 98%" + nút gói | số thật: lõi đã có `Sim.Stage`, chạy 20 trận máy tự đánh ngay trên máy người chơi |
| Mini boss, boss | boss chính là tướng mốc đó; sau khi bị nó đánh bại: "Muốn nó về đội?" | người chơi vừa tự thấy nó mạnh |
| Dùng thử | cho mượn tướng mốc sau đánh 1 trận ở ải đang kẹt, mỗi ngày 1 lần (có thể đổi bằng quảng cáo) | thắng xong mới hiện gói |
| Thẻ gói | lực chiến của tướng trong gói đặt cạnh lực chiến tướng chủ lực hiện có; "ngang +14 cấp" | |
| Bản đồ đảo | habitat của tướng mốc sau hiện bóng + lực chiến, chạm vào ra gói | |

### 2.6. Việc và rủi ro của phần gói tướng

- Code: hệ số sức theo từng tướng (thêm trường trong `heroes.json`, `HeroStats` đọc thay bảng độ hiếm; `Islands.EnemyMods` và `Badges`
  quy sức địch theo trường mới); `buff` của địch theo mốc trong `stages.json`; loại gói "tướng trọn bộ" trong `ShopConfig`; `Offers` chọn
  mốc theo tiến độ từng đảo; màn thua gọi `Sim.Stage` để ra câu so sánh.
- Đổi sức tướng là đổi cân bằng của cả 350 ải, Đền Huy Hiệu, Hầm đấu: phải tính lại golden và đo lại. Giả lập cho thấy tổng thể không lệch
  (52 so với 55 ngày) nhưng mới đo trên người không trả tiền.
- Người chơi sẽ phải đổi tướng chủ lực theo mốc, tướng khởi đầu thành yếu ở giữa game. Nếu muốn giữ tướng khởi đầu dùng được tới cuối
  (luật `15_TuongKhoiDau.md`) thì phải cho nó đường riêng (ví dụ hệ số tăng theo bậc tiến hóa).

## 3. Chép gói IAP của Clash of Critters

Số của họ: `research_notes/Kinh te Clash of Critters.md`. Giá gốc của họ khoảng 180 bi / USD; của mình 100 bi × bậc cấp (150–300 từ cấp 20).

| Gói của Critters | Của họ | Mình đang có | Việc |
|---|---|---|---|
| Nạp đầu, chọn 1 trong 3 bậc, không mua bù | 4,99 / 9,99 / 19,99 USD: 1.000 / 3.000 / 6.400 bi + candy + Capsule + **1 thú** + khung | Quà Nhập Môn 0,99 + Gói Khởi Hành 4,99 | **thêm**: nạp đầu 3 bậc, mỗi bậc kèm tướng mốc 3 / 5 / 6 trọn bộ; giữ Quà Nhập Môn làm cửa vào |
| Gói 7 ngày | ≈ 4,99 USD: 1.440 bi + 3 Wishbox + 20 Capsule, nhận dần 7 ngày | chưa (`26` S5) | **làm** |
| Thẻ tuần | 4,99 USD | Thẻ Tuần 1,99 | có |
| Thẻ tháng | 19,99 USD: 5.900 bi + 27 Wishbox / 30 ngày | Thẻ Phiêu Lưu 4,99 | có; thử 9,99 khi có số đo |
| Quỹ trưởng thành | 7.000 bi + 30 Wishbox theo cấp | Quỹ Phiêu Lưu 9,99 | có; kéo mốc quỹ dài tới cấp 150 theo đường EXP mới |
| Gói chuỗi | 4,99 → 9,99 → 19,99… | Chuỗi Quà | có |
| Heo đất | có | Lọ Bi | có (chặn 3 ngày, `33`) |
| Bổ sung bi khi hết | 3 bậc | Bổ sung bi | có |
| Ưu đãi bất ngờ 10 giờ | 1 món lớn | Ưu Đãi Bất Ngờ 2–3 giờ | có |
| **Wishbox** (tự chọn bản sao) | 4–5 USD mỗi hộp; 25 hộp 99,99 | vé chọn tướng, không bán lẻ | **bán lẻ**: 1 vé 2,99; 10 vé 24,99 |
| Gói thú mới tăng tỉ lệ | theo đợt | Gói Tướng Tuần | có |
| Gói tự chọn 2 món | ≈ 9,99 USD | chưa | sau |
| Đường thưởng sự kiện 150 bậc | chỗ tiêu bi lớn nhất của họ | chưa | **làm** (`33` mục 5.4) |
| Vòng quay trả tiền, VIP, Club | có | không làm (đã chốt ở `26`) | giữ |
| Quảng cáo thưởng | không có | 12 chỗ | lợi thế của mình |

Thứ mình có mà họ không: **gói tướng theo mốc** (mục 2) và quảng cáo thưởng.

## 4. Thứ tự làm

| # | Việc | Loại | Đã đo |
|---|---|---|---|
| 1 | `33` đợt 1–2 (đảo Casino, bán thẻ thừa, trứng rương, Bỏ quảng cáo, Lọ Bi): **xong 2026-11-26** | số + code nhỏ | có |
| 2 | Đường EXP 9 × cấp^1,54; soát các mốc mở theo cấp; tính lại golden: **xong 2026-11-26** (bản hai đoạn) | 2 số + soát | có |
| 3 | Màn thua / chuẩn bị trận ghi "thiếu X cấp ≈ Y bi" + gói vừa đủ; bậc gói theo giai đoạn: **một phần** (dòng ở màn thua, Gói Tiếp Sức nghiêng về bi) | code + UI | chưa (cần số thật) |
| 4 | Nạp đầu 3 bậc, gói 7 ngày, bán lẻ vé: **nạp đầu 3 bậc và vé Hiếm bán lẻ xong** (2026-11-27), gói 7 ngày chưa | dữ liệu + UI | có (`33` mục 0.1) |
| 5 | Sức theo mốc + địch theo mốc + gói tướng trọn bộ + offer theo mốc + quảng cáo sức mạnh: **chốt 2026-11-27 không giãn sức; Gói Vượt Mốc (trọn bộ, theo mốc, ghi lực chiến) xong** | code lõi + cân lại | có (`33` mục 0.1) |
| 6 | Đường thưởng sự kiện, rương sau trần cấp (`33` mục 5.4) | tính năng mới | chưa |

Việc 2 rẻ nhất và tác dụng lớn nhất. Việc 5 đắt nhất (đụng cân bằng cả game) và tác dụng đo được là vừa phải.

## 5. Câu cần chốt

| # | Câu | Đề xuất |
|---|---|---|
| 1 | Đổi đường EXP sang 9 × cấp^1,54? | có; muốn khó hơn thì đo thêm số mũ 1,6–1,7 |
| 2 | Người vừa free phá đảo khoảng 104 ngày, người chăm free 55 ngày: đúng mức muốn chưa? | cho tôi con số mong muốn, tôi dò số mũ |
| 3 | Giãn sức tướng theo mốc như bảng 2.1 (đổi cân bằng cả game)? | có nếu muốn bán gói tướng; không thì gói tướng không có gì để bán |
| 4 | Tướng khởi đầu được phép yếu ở giữa game? | cần chốt; đụng `15_TuongKhoiDau.md` |
| 5 | Thang giá gói tướng 0,99 → 99,99 USD? | số đầu; A/B khi có người chơi thật |
| 6 | Thêm nạp đầu 3 bậc kèm tướng, gói 7 ngày, bán lẻ vé? | có |

## 6. Giới hạn của số đo

- Người chơi ảo mua gì là giả định; giả lập không đo được tỉ lệ người thật chịu mua hay bỏ game khi kẹt. Làm khó hơn chắc chắn tăng số
  người bỏ; mức nào chịu được phải đo thật.
- Phần gói tướng chỉ thử trên người không trả tiền, phát gói theo ngày cố định, tướng cùng hệ tướng khởi đầu. Cách người chơi ảo chọn đội
  và dồn đá là luật đơn giản (mạnh nhất trước).
- Mỗi ô 5–10 người; chênh dưới khoảng 10% chưa nói được gì.
- Đền Huy Hiệu, Hang Tiềm Năng chưa mô phỏng.

Bảng đầy đủ: `ArtGen/KinhTe/gia_lap/ket_qua/pha_dao_90ngay.md`, `goi_tuong_theo_moc.md`. Bộ số: `bo_so/B90.py`, `D_exp_doc.py`,
`K0_gian_moc.py`, `K*.py`, `L*.py`.
