# Máy bi (gacha kiểu pachinko)

Tóm từ research đã có: `ClashMaster/reports/Máy bi Critters và ClashMaster.md` và `ClashMaster/research_notes/Máy bi Critters và ClashMaster/`. Phần cuối là áp vào game này.

Số đo từ bản đục 0.50.1 (hình học bàn, vật lý bi, hiệu ứng, âm thanh, rung theo từng ô): `D:\CrittersRipper\analysis\PINBALL_REPORT.md`, sơ đồ `table_01.png`. Phần đã áp vào máy bi của game (két vàng, vật lý và hiệu ứng chép, phản hồi chia bậc): change `update-pachinko-feel`, mục "Vật lý chép" và "Hiệu ứng chép" ở cuối file này.

## Clash of Critters làm gì

- Máy bi nằm **ngoài trận**, theo dòng Coin Master (máy slot xã hội). Thả bi, bi dội qua đinh rồi rơi vào ô.
- Mặt máy và tỉ lệ (game tự hiện khi chạm vào máy): khoảng 95 % bi rơi vào ô candy, 3,3 % ô thẻ, 1,7 % ô jackpot (cướp hoặc thăm trại người khác). Hai nấm bật trên cùng đổ thanh; thanh đầy cho một sinh vật ngẫu nhiên hoặc một khiên.
- Candy **tự nâng cấp cả đội**. Trận thủ thành tự đánh, chỉ là cửa kiểm tra đội đã đủ mạnh chưa.
- Lilith chọn máy bi vì bi va nhau khi rơi, nên một lần thả thành một chuỗi sự kiện chứ không ra kết quả ngay như rương.
- Tiền nằm ở **vòi bi**: cây bi hồi chậm, hệ số cược ×1–×100 (đổi cỡ cược, không đổi giá trị mỗi bi), hết bi thì hiện gói giảm giá. Tỉ lệ ô cố định và công khai.
- Kết quả: research ghi khoảng 45,6 triệu USD trong bốn tháng đầu (ước tính AppMagic). Nhưng giữ chân sau ngày 7 yếu, và đánh giá trên App Store chuyển dần sang chê tiến độ chậm.

Những móc tâm lý có bằng chứng tốt nhất (research mục "Mười cái móc"): gần như lần nào cũng trúng; thỉnh thoảng trúng hiếm; cú nào cũng được ăn mừng, kể cả khi thực chất là lỗ; thanh tiến độ sắp đầy. Bán bi tức là bán lượt quay, dạng game đã thua những vụ kiện lớn ở Mỹ (Big Fish Casino dàn xếp 155 triệu USD).

## Khác ClashMaster ở chỗ nào

Research kết luận máy bi kiểu Critters đặt sai chỗ ở ClashMaster, vì bot ĐÁNH lên cấp theo bộ bài của người chơi: cả đội mạnh lên thì đối thủ cũng mạnh lên.

**Game này thì khác:** ải có địch cấp cố định ([05_VuotAi_ThuPhuc.md](05_VuotAi_ThuPhuc.md)), nên sức mạnh từ máy bi có tác dụng thật, đúng như ở Critters. Vòng "bi → mạnh lên → qua ải khó hơn → thêm bi" chạy được. Vì thế phải cẩn thận theo chiều ngược lại: máy quá hào phóng thì tay nghề xếp khối không còn quan trọng.

## Đề xuất: máy bi Thu phục

- **Chỗ đặt:** một tab riêng ở menu dưới. Máy đứng dọc gần cả màn hình, bi rơi từ trên xuống.
- **Bi từ đâu:** 1 bi mỗi ải thắng, +2 khi đạt 3★ lần đầu, +3 khi thu phục được tướng, nhiệm vụ ngày. Không hồi theo giờ.
- **Mặt máy:**

| Ô | Tỉ lệ (đề xuất, đo lại bằng mô phỏng) | Trả |
|---|---|---|
| Hai ô ngoài | khoảng 60 % | vàng hoặc kinh nghiệm |
| Hai ô giữa | khoảng 33 % | đá tiến hóa, hệ ngẫu nhiên |
| Ô tâm | khoảng 6 % | mảnh của một tướng đã gặp trong ải |
| Ô vàng nhỏ ở tâm | khoảng 1 % | **quả cầu phong ấn**: thêm 2 lượt cho lần phong ấn kế tiếp |

- **Một thanh "hũ sắp đầy"**: mỗi bi đổ một nấc, bắt đầu đã có sẵn vài nấc. Đầy hũ thì chắc chắn được 10 mảnh của một tướng tự chọn trong số tướng đã gặp.
- **Không mở tướng chưa gặp.** Tướng mới đến từ thu phục; máy chỉ giúp nuôi. Thu phục vẫn là lý do để vượt ải.
- **Canh lúc thả:** một mái chèo đung đưa trên đỉnh. Thả đúng lúc thì bi dễ vào giữa hơn một chút. Ghi rõ tác dụng này trên máy.
- **Tiếng và hiệu ứng tỉ lệ với giá trị thật:** ô vàng chỉ kêu nhỏ; ô hiếm mới có kèn. Research ghi đây là cách chữa đã được chứng minh cho việc "lỗ mà tưởng thắng".
- **In tỉ lệ lên mặt máy.** Apple buộc công bố tỉ lệ cho mọi thứ ngẫu nhiên bán bằng tiền.
- **Thả nhiều bi một lúc** (×5, ×10) chỉ để nhanh, không nhân thưởng, không cần giữ bi mới mở.

## Nếu muốn kiếm tiền từ máy

**Đã chốt (2026-10-30): bi chỉ kiếm bằng chơi, không bán bi.** Bảng dưới giữ lại để biết lý do.

| | Bán vẻ ngoài | Bán bi (như Critters) |
|---|---|---|
| Bán gì | mặt máy, bi màu, hiệu ứng | gói bi, gói giảm giá khi hết bi |
| Doanh thu | thấp hơn | cao hơn (Critters là ví dụ) |
| Pháp lý | an toàn | thuộc loại casino xã hội; Úc xếp game mô phỏng cờ bạc R18+ từ 9/2024 |
| Ảnh hưởng tay nghề | không | có: mua bi thành mua sức mạnh qua ải |

Research đề xuất cho ClashMaster là bán vẻ ngoài. Với game này, đề xuất giữ hướng đó, và kiếm tiền ở chỗ khác: thẻ tháng, gói tướng có sẵn, vé ải hằng ngày.

## Vật lý chép

Chủ dự án bảo chép vật lý và hiệu ứng của máy Critters (2026-11-02). Vật liệu chép nguyên, đổi theo đường kính bi: bi ở đó 0,162 u, ở đây 18, nên 1 u = 111.

| Mục | Critters | Máy bi Thu phục |
|---|---|---|
| Nảy | 0,8 (nấm đỉnh 0,9) | 0,8 mọi thứ |
| Ma sát | tường, vách, nấm lớn 0,22; đinh, mái, đáy V 0 | tường, trần, vai, vách, nấm, cọc 0,22; đinh, mái, đáy két 0 |
| Va chậm không nảy | dưới 1 u/giây | dưới 111 |
| Bi va bi | không nảy | không nảy |
| Cản | 0,3 | 0,3 |
| Trọng lực | 2 u/giây² (= 222) | 1.100 |
| Kẹp tốc | 4–14 u/giây (= 444–1.556) | 150–525 |

**Trọng lực và kẹp tốc không chép nguyên.** Mặt máy này dày đinh hơn nhiều: khoảng 85 đinh trên 26 × 38 đường kính bi, máy Critters có 22 đinh trên 33 × 50. Chép nguyên thì bi bay trung vị 9 giây. Muốn bi bồng bềnh đúng như Critters thì phải đổi mặt máy sang ít đinh to.

Lý do và các lần thử ghi ở change `update-pachinko-feel` (design, mục vật lý).

## Hiệu ứng chép

**Phần chép:** cấu trúc hệ hạt (số hạt, đời, tốc, cỡ và màu theo đời, trọng lực, kẹp tốc) lấy từ prefab hiệu ứng của Critters, chi tiết trong `PINBALL_REPORT.md` mục 6.

**Phần của mình:** hình hạt (`fx_*`, sau này là ảnh gen P4). Code ở `Assets/01 Script/Game/Machine/MachineFx.cs`.

**Đơn vị:** cỡ và tốc tính theo u của Critters, đổi ra px như sau:
- hiệu ứng theo bi: 1 u = 191 px canvas;
- hiệu ứng ô: theo bề rộng ô (ô Critters rộng 0,9 u).

| Lúc | Critters | Ở đây |
|---|---|---|
| Bi lăn | TrailRenderer 0,3 giây, rộng 0,18 u, xanh lơ alpha 0,52 → tím trong suốt | dải `TrailGraphic` 0,3 giây, rộng 0,18 u, màu bi alpha 0,6 → 0, mép mềm |
| Chạm đinh | ảnh sáng 1,15 → 1 và quầng 1,10 → 0,68 trong 0,067 giây | như vậy, rồi mờ 0,1 giây, thêm 2 lấp lánh |
| Chạm nấm | nấm 0,90 → 1,18 → 0,89 → 1,05 → 1 trong 0,23 giây; quầng 3 co 0,15 giây, vòng 1,62 lan 0,19 giây, quầng 1,75 (tím) | như vậy, màu đỏ của nấm |
| Thả bi | cần phóng co giãn 0,63 → 1,57 → 0,89 → 1,2; lửa 0,15 giây, quầng, chấm | mây co giãn nửa biên độ; khói, quầng, chấm |
| Rơi vào ô | 3 quầng 0,1–0,15 giây, 6 sao tốc 15–60 bị hãm, 6 vệt "she" 0,07–0,1 giây | như vậy, sao vàng thay xanh lơ |
| Cốc | 10 chấm, 10 sao (trọng lực 0,3), chớp, vòng | như vậy, ở cốc bạc và két |
| Rương | bảng điểm cấp 1–4 (chớp, quầng, vòng, sao; cấp 3 thêm 6 tia tốc 10–20) | gỗ, bạc cấp 2; vàng cấp 3 |
| Jackpot | vòng 0,24 giây, 2 quầng 0,35 giây, 4 tia, 3 sao (trễ 0,05), 1 sao nảy (trễ 0,1), sao lõi | như vậy, ở két hoặc ô khuất |

**Hạt chạy theo giờ máy:** lúc rương vàng làm máy chạy chậm, hạt cũng chậm.

**Lượt thử soi:** `PokiClash/Thử/Máy bi: soi hiệu ứng`. Nó dừng máy và tua giờ hạt để chụp từng mốc.
