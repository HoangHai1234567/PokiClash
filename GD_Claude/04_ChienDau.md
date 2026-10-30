# Chiến đấu

Trận đánh nằm ở nửa trên màn hình, chạy theo bàn xếp khối ([03_XepKhoi.md](03_XepKhoi.md)). Người chơi không điều khiển tướng trực tiếp, trừ việc tung chiêu.

## Đội hình

- **Mang 4 tướng vào ải** (đề xuất; Pokiwar có đội 5 và đội 6). Bốn tướng vừa hàng chân dung trên màn dọc, mỗi tướng một hệ hoặc trùng hệ.
- Tướng đầu là **chủ lực**: đánh các ô thuộc hệ không có trong đội, và có một kỹ năng bị động cho cả đội (kiểu leader skill của Puzzle & Dragons).
- Máu là **máu chung của đội**, cộng từ máu từng tướng. Một thanh máu dễ đọc trên màn nhỏ. Bản thử nên thử cả máu riêng từng tướng để so.

## Nhịp lượt

1. Người chơi đặt một khối.
2. Có xoá thì tướng ra đòn (khoảng 0,3 giây mỗi tướng, các tướng nối nhau, không chờ hết hoạt cảnh mới cho kéo tiếp).
3. Bộ đếm của mỗi địch giảm 1. Về 0 thì địch đánh hoặc tung kỹ năng bàn, rồi đếm lại.
4. Lượt sau.

Đòn của tướng không chặn người chơi: khối kế tiếp kéo được ngay khi đòn còn bay. Như vậy nhịp vẫn nhanh như Block Blast.

## Nộ và chiêu

- Nộ nạp từ ô cùng hệ bị xoá, và từ ô Sao.
- Nộ đầy thì chân dung sáng lên; chạm để tung chiêu, lúc nào cũng được, không tốn lượt.
- Chiêu có hai loại:
  - **chiêu đánh**: sát thương lớn, thêm hiệu ứng (bỏng, tê liệt, hút nộ của địch);
  - **chiêu bàn**: tác động lên bàn, ví dụ xoá một cột, đổi màu 6 ô sang hệ mình, phá hết đá, đổi tay khối.
- Chiêu bàn là chỗ tướng khác nhau thật sự về lối chơi, không chỉ về chỉ số. Mỗi tướng nên có đúng một chiêu, dễ nhớ.
- Pokiwar dùng nộ để "gọi pet cấp cao ra trận". Có thể giữ ý đó dưới dạng **hóa thân**: tướng đã tiến hóa, nộ đầy thì đổi sang dạng tiến hóa cao nhất trong 3 lượt. Dạng tiến hóa dùng luôn các dạng của một dòng tướng ([06_Tuong_NuoiDuong.md](06_Tuong_NuoiDuong.md)).

## Địch

- Một ải có 1–3 đợt, mỗi đợt 1–3 địch. Chạm địch để chọn mục tiêu; mặc định đánh con gần chết nhất.
- Mỗi địch có máu, công, hệ, **bộ đếm lượt** (số lượt giữa hai lần ra tay) và 0–2 kỹ năng bàn.
- Boss có thanh máu nhiều tầng. Qua mỗi tầng thì đổi kỹ năng, ví dụ tầng 2 bắt đầu đẩy rác.

## Hiệu ứng trạng thái

| Hiệu ứng | Tác dụng |
|---|---|
| Bỏng | mất máu mỗi lượt, 3 lượt |
| Tê liệt | bộ đếm của địch dừng 1 lượt |
| Phá giáp | nhận thêm 30 % sát thương, 3 lượt |
| Hút nộ | lấy nộ của bên kia |

Pokiwar có cả bốn dạng này (theo trang tin: tê liệt, hồi máu, nhận thêm sát thương, bỏng theo lượt, hút nộ).

## Kết thúc trận

- Thắng: hết địch ở đợt cuối.
- Thua: máu đội về 0. Được hồi sinh 1 lần miễn phí mỗi ải (đề xuất).
- Sao của ải: 1★ thắng, 2★ còn trên 50 % máu, 3★ thắng trong số lượt quy định. Lượt dư cộng vào điểm thu phục ([05_VuotAi_ThuPhuc.md](05_VuotAi_ThuPhuc.md)).
