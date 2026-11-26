# Simulation: nhật ký các vòng giả lập kinh tế PokiClash

Ghi lại từng vòng chạy giả lập 300 người chơi ảo (2026-11-26 và 2026-11-27), kinh nghiệm khi chạy, bài học về kinh tế game và hướng cải
thiện. Viết cho người sẽ chạy vòng tiếp theo: đọc file này trước khi mở máy giả lập.

- Máy giả lập: `ArtGen/KinhTe/gia_lap/` (cách dùng ở `README.md` trong đó). Bảng kết quả: `ArtGen/KinhTe/gia_lap/ket_qua/`.
- Kế hoạch và số đo đầy đủ: `../33_CanBangKinhTe.md` (cân bằng, mục 0 và 0.1 là việc đã áp vào game), `../34_KiemTien_KhoPhaDao.md`
  (đường EXP, gói tướng theo mốc), `../35_Critters_KichBanGaMua.md` (kịch bản chào bán của Clash of Critters).

## 1. Máy giả lập trong một trang

- Biên dịch thẳng lõi game (`Assets/01 Script/Core`) ngoài Unity rồi cho người chơi ảo gọi đúng luật thật: ải, AFK, cây bi, ruộng Nhà,
  máy bi, cửa hàng và bộ máy ưu đãi, quảng cáo thưởng, đảo Casino. Chỉ có "người chơi làm gì" là giả định.
- 300 người = 3 mức chơi × 5 nhóm tiền × (không ra đảo / ra đảo thận trọng / ra đảo máu me), mỗi ô 5–10 người.

| Mức chơi | Mỗi ngày | | Nhóm tiền | Xem quảng cáo | Chi trong 30 ngày |
|---|---|---|---|---|---|
| Chăm | 6 phiên × 5 trận | | F0 | không | 0 |
| Vừa | 3 phiên × 3 trận | | FA | ít (tối đa 6 lượt) hoặc nhiều (tối đa 25 lượt) | 0 |
| Ít | 1 phiên × 2 trận, nghỉ 1 ngày trong 5 | | P1 / P2 / P3 | 10 / 15 / 10 lượt | 15 / 80 / 600 USD |

- Chạy: `py -3 -I chay.py <bộ số> --n 6 --ngay 90`, rồi `tong_hop.py`, `so_sanh.py`, `pha_dao.py`, `moc_ai.py`. 300 người × 30 ngày mất
  khoảng 2 phút, × 90 ngày khoảng 5 phút, tối đa 6 tiến trình.
- Bộ số (`bo_so/<tên>.py`) là một hàm sửa bản sao `balance.json`. Luật chưa có trong game thì giả lập trước trong khối `sim` (`SimRules`).

## 2. Các vòng đã chạy

"Phá đảo" là xong 350 ải. Số ngày là trung vị của nhóm người không ra đảo, trừ khi ghi khác.

### 2.1. Ngày 2026-11-26: tìm bệnh, thử thuốc trên bản sao số liệu

| Bộ số | Hỏi gì | Đo được | Quyết định |
|---|---|---|---|
| `goc` (30 ngày) | Game lúc đó ra sao | 150 / 150 người có ra đảo cầm hơn 1 triệu bi. Người chăm vỡ ở ngày 5–6, người vừa ngày 7–12, người ít ngày 18–23. Thủ phạm: bán thẻ thừa ở Chợ đen đổi ra bi, bi thả ra lại ra thẻ | Phải bịt trước khi phát hành đảo |
| `A_khoa_ban_the` | Bịt lỗ đó rồi thì đảo còn lệch không | Người ra đảo thận trọng vẫn thu gấp 3,5–4 lần bi (chăm F0: 1.752 → 6.126 mỗi ngày). Hầm đấu thắng trả 2,5 lần lệ phí: +2.780 bi mỗi ngày. Câu cá +466, Quán trọ +304. Bàn may rủi (Blackjack, Roulette, Slot) gần như bằng 0 | Sửa Hầm đấu, Câu cá, Quán trọ, Đua; giữ nguyên bàn may rủi |
| `B_de_xuat` | Bộ sửa đề xuất có đưa đảo về mức an toàn không | 0 / 300 vỡ. Đảo thận trọng +178 bi mỗi ngày, đảo máu me −242. Gói Tiếp Sức từ 0 lên 3 lần bật mỗi người. Bi của người chi 600 USD từ 25.022 xuống 16.039 mỗi ngày (chặn Lọ Bi, Bỏ quảng cáo) | Lấy làm nền |
| `C_siet_them` | Cắt 25% bi thụ động (cây bi, ruộng) có tạo lý do mua không | Mọi người chậm khoảng 10%, nhưng người vừa vẫn hầu như không kẹt (8 → 14 lần gặp tường trong 30 ngày) | Không làm |
| `B90`, `D_exp_doc` (90 ngày) | Đường EXP dốc dần (9 × cấp^1,54) làm khó tới đâu | Chăm F0 phá đảo ngày 33 → 55; vừa F0 ngày 48 → khoảng 104; chi 80 USD ngày 12 → 22; chi 600 USD vẫn ngày 12 | Làm |
| `E_boss_manh` | Boss mạnh hơn có làm khó thêm không | 55 ngày so với 55 ngày | Không làm |
| `K0`, `K3`–`K10`, `L6`–`L10` | Giãn sức tướng theo mốc và phát gói tướng | Chỉ mở khoá tướng (1 sao, thẻ cấp 1): không khác gì. Gói trọn bộ đi trước xa: người chăm sớm 4–6 ngày, người vừa 5–10 ngày | Để lại đo tiếp ở vòng 1 |
| `M_tong_hop` | Gộp mọi đề xuất (thêm nạp đầu 3 bậc, gói sự kiện, ×2 EXP, Lọ Bi xoay 9 ngày) | Nhịp như `D`; người chi 80 USD chậm đi (ngày 22 → 26) vì Lọ Bi bị giới hạn | Tham khảo |

### 2.2. Tối 2026-11-26: đưa vào game thật rồi đo lại

Người dùng dặn tự làm theo đề xuất. Đã áp `33` đợt 1–3 và đường EXP hai đoạn max(45 × cấp, 9 × cấp^1,54) vào `Assets`.

| Bộ số | Đo được |
|---|---|
| `G30_game_moi` | 0 / 300 vỡ. Chăm F0: cấp ngày 30 từ 186 xuống 110, bi thu mỗi ngày 1.752 → 1.188. Vừa F0 gặp tường 3 → 57 lần trong 30 ngày. Gói Tiếp Sức bật 3,5 lần mỗi người không trả tiền |
| `G90_game_moi` | Phá đảo: chăm F0 ngày 58, chăm xem nhiều quảng cáo ngày 39, chi 15 USD ngày 41, chi 80 USD ngày 24, chi 600 USD ngày 12; vừa F0 khoảng ngày 104. Khớp dự đoán của `D` và `M` |

### 2.3. Ngày 2026-11-27: ba vòng làm → chạy → rút kinh nghiệm → sửa

| Vòng | Bộ số | Làm / hỏi gì | Đo được | Rút ra và chốt |
|---|---|---|---|---|
| 1 | `H1_goi_khong_gian`, `H2_gian_moc`, `H3_gian_moc_goi` | Trước khi làm gói tướng: có cần giãn sức tướng theo mốc không | Không giãn: người vừa tới 150–200 ải sớm 6 ngày, người chăm 1–3 ngày. Có giãn: người vừa sớm 9–12 ngày ở giữa game, nhưng người chăm phá đảo muộn hơn (ngày 71 so với 53) | Không giãn sức: lợi thêm 3–6 ngày mà phải cân lại cả 350 ải, cuối game còn hại người mua |
| 2 | `J1_vuot_moc` | Làm Gói Vượt Mốc trong game thật (tướng đi trước 3 mốc, trọn bộ, giá tự tính ×5 giá trị) | Popup bật khoảng 8 lần mỗi người trong 90 ngày; 54 người mua 162 lần. Nhịp phá đảo không đổi. Lộ ra: Lọ Bi được đập 6,6 lần mỗi tháng, 2.188 bi mỗi USD, trong khi gói bi chỉ 340–900 | Giữ gói. Lọ Bi cách 3 ngày → 7 ngày |
| 3 | `J2_nap_dau_lo_bi` | Làm nạp đầu 3 bậc chọn một; Lọ Bi 7 ngày | Lọ Bi còn 3,4 lần đập mỗi tháng. Chi 80 USD phá đảo ngày 25 (trước 23). 0 / 300 vỡ | Giữ. Đây là trạng thái game hiện tại |

## 3. Kinh nghiệm khi chạy giả lập

**Dựng máy**
- Gọi thẳng lõi game, đừng viết lại công thức. Mọi lệch giữa máy và game là lỗi giả lập, không phải phát hiện.
- Lỗi máy đã gặp: nhân mức cược vào rương mốc quà và rương vòng nấm của máy bi (game không nhân), làm bi phình giả. Thấy số quá đẹp hoặc
  quá xấu thì soát máy trước khi tin.
- Kinh tế có vòng lặp thì giả lập chạy mãi không dừng: đặt ngưỡng "vỡ" (cầm hơn 1 triệu bi thì dừng người đó, ghi ngày vỡ) và trần giờ CPU
  mỗi người. Trần phải tính bằng giờ CPU, không bằng đồng hồ: máy ngủ giữa chừng làm 6 người bị đánh dấu quá giờ oan.
- Chia nhóm người chơi ảo phải độc lập với nhau. Lần đầu nhóm "xem ít / xem nhiều quảng cáo" trùng cách chia "thận trọng / máu me" nên hai
  yếu tố lẫn vào nhau, phải chạy lại.

**Chạy và so**
- Mỗi lượt một tên bộ số riêng, gắn với một trạng thái game. Tôi đã lỡ chạy `goc --lam-lai` sau khi game đổi và đè mất kết quả thô của
  game cũ (bảng tổng hợp còn, số từng người thì mất).
- Mỗi ô chỉ 5–10 người nên nhiễu khoảng ±4 ngày ở mốc phá đảo: cùng một game, hai lượt chạy cho 58 và 54 ngày vì thêm một popup làm đổi
  dãy số ngẫu nhiên. Chênh dưới 4 ngày thì chưa kết luận được.
- So "trước / sau" phải cùng số ngày chạy. Bộ 30 ngày và bộ 90 ngày không so thẳng với nhau.
- Câu hỏi về lợi ích thì chỉ cần chạy nhóm không trả tiền (`--nhom 0,1`), nhanh gấp đôi.
- Đo cả số lần mỗi popup bật. Gói Tiếp Sức bật 0 lần trên 300 người là thứ không ai thấy nếu chỉ nhìn tiến độ.

**Đưa đề xuất vào game**
- Luật mới: giả lập trước trong `SimRules`, đo, rồi mới viết vào lõi. Khi luật đã vào lõi thì xoá phần giả lập, cho máy gọi luật thật, và
  chạy lại để xác nhận số khớp dự đoán (vòng `G` khớp `D` và `M`).
- Thứ tự an toàn: sửa → biên dịch thử ngoài Unity → test NUnit ngoài Unity → soát bản dịch → mới cho Unity nạp → nhập dữ liệu → test
  trong Unity → tour chụp màn có chữ mới. Cả chuỗi có script trong `gia_lap/` (`kiem_app.py`, `kiem_test.py`, `kiem_dich.py`, `unity_*.py`).
- Script sửa nhiều file phải chạy được lại sau khi dừng giữa chừng. Một lần script dừng ở file thứ tư, chạy lại thì file đầu bị sửa hai
  lần (khai báo trùng); bắt được nhờ bước biên dịch thử ngoài Unity.
- Mã Python có dấu `\` không đặt trong heredoc của Bash (bị hỏng), ghi ra file rồi chạy.
- Tour chạm tới bản lưu phải sao lưu đầu tour và trả lại trong `finally`. Menu tour gọi lúc game chưa vào Play xong thì bị bỏ qua, phải
  kiểm log rồi gọi lại.

## 4. Bài học về kinh tế game

1. **Mọi thứ đổi ra tiền chính phải có trần hoặc không đổi ra tiền chính.** Thẻ thừa → bi → thả máy → thẻ là vòng tự nuôi, vỡ trong 5 ngày.
   Giờ thẻ thừa đổi đá tiềm năng, có trần ngày.
2. **Trò phụ không trả lãi bằng tiền chính.** Hầm đấu thắng chắc mà trả 2,5 lần lệ phí thì lớn hơn mọi nguồn miễn phí cộng lại. Thưởng
   của trò phụ nên là mảnh, đá.
3. **Bàn may rủi không phải vấn đề.** Cược nhỏ so với thu nhập, hoàn trả 0,95–1,0: không phải nguồn, cũng không phải chỗ tiêu.
4. **Đòn bẩy là giá của mỗi cấp, không phải lượng bi phát ra.** Khoảng 70% bi của người không trả tiền là thụ động (cây bi, Nhà: 904 trên
   1.311 mỗi ngày). Cắt 25% phần đó chỉ làm chậm 10% và không sinh tường; đổi đường EXP thì người vừa gặp tường nhiều gấp 7 lần
   (8 → 57 lần trong 30 ngày đầu).
5. **Địch mạnh hơn không làm game khó hơn** khi thứ chặn là cấp: boss mạnh hơn cho đúng số ngày phá đảo cũ.
6. **Một dòng thưởng đổi đơn vị có thể lệch gấp 9.** "1–2 mảnh" thành "1 trứng" (12–16 mảnh) làm trứng rương máy bi lấn mọi nguồn mảnh.
7. **Một gói quá hời làm các gói khác vô nghĩa.** Bỏ quảng cáo 4,99 USD từng là +1.500 bi mỗi ngày mãi mãi; Lọ Bi rẻ gấp 4–6 lần gói bi.
   Soát "bi mỗi USD" của mọi gói sau mỗi lần đổi số.
8. **Ưu đãi phải được kiểm là có bật.** Điều kiện "còn cách miễn phí" quá rộng làm Gói Tiếp Sức không bao giờ hiện.
9. **Bán tướng: mở khoá suông không có giá trị.** Gói tướng chỉ có tác dụng khi đi trước ít nhất 3 mốc và kèm đủ mảnh, thẻ, đá. Kể cả
   vậy, cùng số tiền nó không nhanh hơn mua bi: thứ nó bán là có tướng sớm.
10. **Giãn sức tướng toàn cục là con dao hai lưỡi:** người mua tướng mốc cuối dồn đá cho nó rồi kẹt, phá đảo muộn hơn người không mua.
11. **Đá tiến hóa là nút kẹt thật** (người chăm không trả tiền kẹt đá 101 trên 180 phiên), trước đó lại không mua được. Thứ gì là nút
    kẹt thì phải có gói bán đúng thứ đó.
12. **Trả tiền phải thấy nhanh hơn rõ.** Hiện tại so với người chăm không trả tiền: chi 15 USD nhanh gấp 1,4; 80 USD gấp 2,4; 600 USD
    gấp 4,8.
13. **Người chơi ít bị chặn bởi thời gian, không bởi sức mạnh.** Họ không bao giờ gặp tường dù trả bao nhiêu, nên mọi gói "mạnh lên"
    vô nghĩa với họ, mà theo giả định dân số đây là nhóm đông nhất (50%).

## 5. Giả lập chưa trả lời được gì

- **Tỉ lệ người chịu mua.** Người chơi ảo có ngân sách cố định theo nhóm; thêm gói chỉ đổi họ mua gì, không đổi họ chi bao nhiêu.
- **Bỏ game.** Không ai bỏ dù kẹt bao lâu, nên không biết đường EXP mới làm mất bao nhiêu người.
- **Giao diện.** Ô gói đặt ở đâu, popup có khó chịu không: phải xem bằng mắt và số thật.
- Chưa mô phỏng: Đền Huy Hiệu, Hang Tiềm Năng (đá cộng gần đúng), công trình Nhà ngoài cây bi và ruộng.
- Người chơi ảo chưa biết mua Vé chọn tướng Hiếm, nên gói đó chưa có số.

## 6. Hướng cải thiện

**Máy giả lập**

| Việc | Vì sao |
|---|---|
| Bảng mục tiêu tự chấm sau mỗi lượt (không ai vỡ; chăm F0 phá đảo 50–70 ngày; vừa F0 90–120 ngày; không gói nào hơn gói bi quá 3 lần về bi mỗi USD; mỗi ưu đãi bật ít nhất 1 lần mỗi người) | Hiện phải đọc bảng bằng mắt; có bảng chấm thì mỗi lần đổi số biết ngay lệch chỗ nào |
| Người chơi ảo mua theo nhu cầu (đang kẹt gì thì cân gói đó theo giá trị) thay cho ngân sách cứng | Để giả lập phân biệt được gói có lý do mua với gói không |
| Xác suất bỏ game theo số ngày liền không qua ải mới | Đo được cái giá của việc làm khó |
| Tăng lên 20–30 người mỗi ô, hoặc cố định hạt giống theo người để hai bộ số so từng cặp | Giảm nhiễu ±4 ngày |
| Thêm chỉ số "ngày gặp tường đầu tiên" và "số ngày kẹt dài nhất" | Tuần đầu là lúc giữ người chơi; hiện chỉ có tổng số lần gặp tường |
| Lưu kết quả kèm mã commit của game | Không lặp lại việc đè mất kết quả của game cũ |
| Mô phỏng Đền Huy Hiệu, Hang Tiềm Năng, Nhà | Ba nguồn đá và bi đang tính gần đúng |
| Khi có người chơi thật: chỉnh số phiên, số trận, tỉ lệ xem quảng cáo, tỉ lệ mua theo số thật | Mọi kết luận hiện dựa trên giả định về hành vi |

**Game** (xếp theo thứ tự nên làm)

| Việc | Ghi chú |
|---|---|
| Gói 7 ngày | Gần như chỉ thêm dữ liệu (đã có kiểu gói nhận theo ngày) |
| Thứ để bán cho người chơi ít | Hướng nghĩ: thứ đổi thời gian lấy tiến độ (càn quét ải đã qua, AFK dài hơn), không phải thứ mạnh lên |
| Gói bi "vừa đủ số còn thiếu" ngay trên màn thua | Màn thua đã ghi thiếu mấy cấp và bao nhiêu bi; còn thiếu nút mua đúng số đó |
| Ô gói cố định trên màn máy bi | Critters bán nhiều nhất ở màn máy bi; mình chưa có gì ở đó |
| Vật phẩm ×2 EXP máy bi | Tạo lý do thả thật nhiều bi ngay, tức lý do mua bi |
| Gói theo sự kiện và lịch xoay 9 ngày | Đã có lịch sự kiện 14 ngày của Bến Lữ Khách |
| Đường thưởng sự kiện, rương sau trần cấp 200 | Chỗ tiêu bi không đáy cho người đã chạm trần (chi 600 USD chạm trần ở ngày 6) |
| Số bi ở dòng "thiếu cấp" thêm dấu ngăn nghìn | "270000" khó đọc |

Mỗi việc trên làm theo đúng vòng đã dùng: viết bộ số hoặc sửa game → chạy 300 người → so với lượt trước → sửa → chạy lại, và ghi thêm
một dòng vào mục 2 của file này.

## 7. File liên quan

| Ở đâu | Là gì |
|---|---|
| `ArtGen/KinhTe/gia_lap/` | Máy giả lập, bộ số (`bo_so/`), bảng kết quả (`ket_qua/`), script kiểm và gọi Unity |
| `ArtGen/KinhTe/gia_lap/bo_so/cu_truoc_1126/` | Bộ số viết cho game trước khi sửa (chạy lại cần code ở commit `655e6e75`) |
| `ket_qua/so_sanh_G30_game_moi.md`, `pha_dao_G90_game_moi.md` | Game trước và sau đợt sửa 2026-11-26 |
| `ket_qua/vong1_goi_tuong_gian_suc.md`, `vong2_3_vuot_moc_nap_dau_lo_bi.md`, `tong_hop_J2_nap_dau_lo_bi.md` | Ba vòng ngày 2026-11-27 |
| `Assets/01 Script/Editor/ShopEconTour.cs` | Tour chụp Gói Vượt Mốc, nạp đầu 3 bậc, Lọ Bi |
