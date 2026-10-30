# Máy bi (gacha kiểu pachinko)

Tóm từ research đã có: `ClashMaster/reports/Máy bi Critters và ClashMaster.md` và `ClashMaster/research_notes/Máy bi Critters và ClashMaster/`. Phần cuối là áp vào game này.

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
