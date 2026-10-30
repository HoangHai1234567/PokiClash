# Các hướng phát triển

Mục tiêu người dùng đặt: game đánh nhau, vượt ải để thu phục tướng, ghép với một kiểu puzzle (Block Blast, Block Blast "sập", hoặc kiểu khác hợp hơn), màn hình dọc. Cảm hứng gốc là Pokiwar.

## Pokiwar làm gì (tóm từ research "Match-3 đấu pet" và các trang tin còn sót)

- Webgame của CMN Online (Việt Nam), 2015–2016. Bản di động Poki Mobile ra 5/2020, nay đã ngừng.
- Trận đánh trên bàn xếp ngọc nhiều màu. **Ngọc xếp được quyết định hành động của pet**: tấn công, phòng thủ, xuất chiêu, hồi máu.
- Combo liên tiếp nạp nộ. Đủ nộ thì **gọi pet cấp cao hơn ra trận**.
- Pet có hệ (Nước, Lửa, Đất, Gió…). **Đánh bại thì thu phục được.** Boss mạnh thì khó thu phục.
- Nuôi pet: tiến hóa bằng đá tiến hóa, tiến hóa mở kỹ năng mới.
- Chế độ: Ải Viễn Chinh, đấu trường 1v1, 3v3 và 5v5, đảo đổi đồ.

Chỗ Pokiwar để lại: research ghi ngách "xếp hình đấu pet" gần như bỏ trống. Shuffle ngừng ra nội dung từ 2018, Monster Tales có dấu hiệu bị gỡ, Pokiwar đã ngừng. Tiền của thể loại nằm ở match-3 RPG midcore (Empires & Puzzles, Puzzle & Dragons).

## Bốn hướng

### A. Xếp khối đánh trận (đề xuất làm lõi)

- Bàn 8×8 kiểu Block Blast, mỗi tay 3 khối, kéo thả, không giới hạn giờ.
- **Mỗi khối mang màu một hệ.** Xoá hàng hay cột thì tướng cùng hệ ra đòn. Đây là cách Pokiwar "ngọc quyết định hành động", chuyển sang luật xếp khối.
- Địch đếm lượt (đặt N khối thì địch đánh một lần) và phá bàn: ném đá, đóng băng ô, khoá một khối trong tay.
- Hết chỗ đặt không thua ngay: cả đội bị choáng, mất máu, bàn dọn bớt một phần. Thua khi hết máu.
- Chi tiết: [03_XepKhoi.md](03_XepKhoi.md), [04_ChienDau.md](04_ChienDau.md).

**Vì sao chọn:** Block Blast vốn là game dọc. Bàn vuông nằm gọn nửa dưới màn hình, nửa trên để sân đấu. Người chơi casual đã quen luật, nên chỉ phải học thêm một điều: "màu nào thì tướng đó đánh". Kéo thả không vướng giờ, chơi một tay được.

**Rủi ro:** Block Blast thuần là trò không có kết thúc; ở đây mỗi ải phải kết thúc trong khoảng 2–4 phút. Phải cân sao cho lối "dọn bàn" (sống sót) và "nhắm màu" (gây sát thương) kéo nhau, không cái nào lấn hẳn. Máy tự chơi (xem [08_KyThuat_Unity.md](08_KyThuat_Unity.md)) dùng để đo việc này.

### B. Khối sập (dùng làm chế độ phụ hoặc cơ chế boss)

- Cùng bàn và khối như A, nhưng **có trọng lực**: xoá đường xong, ô lơ lửng rơi xuống, có thể làm đầy đường mới, tức là xoá dây chuyền.
- Dây chuyền cho lại cảm giác combo nối tiếp của Pokiwar mà Block Blast thuần không có.
- Địch đẩy hàng rác từ đáy lên (như Puzzle League), nên áp lực trận nhìn thấy được.
- Khó đọc hơn A: người chơi phải đoán bàn sau khi sập. Nên để làm boss, Tháp, hoặc một chế độ riêng khi người chơi đã quen A.
- Chi tiết: [03_XepKhoi.md](03_XepKhoi.md) mục "Biến thể sập".

### C. Xếp ngọc kiểu Pokiwar, đổi sang dọc

- Bàn ngọc khoảng 6×7, đổi chỗ hai ngọc kề nhau. Ngọc Kiếm đánh, Khiên thủ, Tim hồi, ngọc màu nạp chiêu.
- An toàn, đã có tiền lệ thu lớn (Empires & Puzzles). Nhưng đông đối thủ và ít mới. Chủ đề vẫn là "Pokiwar làm lại", không có gì để quảng cáo khác đi.
- Giữ làm phương án dự phòng nếu bản thử A không vui.

### D. Máy bi làm động cơ, trận tự đánh (kiểu Clash of Critters)

- Puzzle không quyết định trận. Máy bi trả kinh nghiệm cho cả đội, trận vượt ải tự đánh và chỉ là cửa kiểm tra sức mạnh.
- Research máy bi ghi Critters thu khoảng 53,8 triệu USD trong năm tháng. Cũng ghi giữ chân sau ngày 7 yếu, và đi kèm rủi ro pháp lý khi bán bi.
- Hướng này bỏ mất phần "đánh nhau bằng tay" mà người dùng muốn. **Không đề xuất làm lõi.** Phần đáng mượn là máy bi làm chỗ phát thưởng: [07_MayBi.md](07_MayBi.md).

## So sánh nhanh

| | A. Xếp khối đánh trận | B. Khối sập | C. Xếp ngọc | D. Máy bi + tự đánh |
|---|---|---|---|---|
| Hợp màn dọc | rất hợp | rất hợp | hợp | rất hợp |
| Người mới hiểu ngay | cao (luật Block Blast) | trung bình | cao | cao |
| Mới so với thị trường | cao | cao | thấp | trung bình |
| Người chơi quyết định trận | cao | cao | cao | thấp |
| Có sẵn để dùng lại | logic Block Blast ở 2PlayersGame | như A, thêm trọng lực | không | không |
| Rủi ro chính | cân sống sót với sát thương | khó đọc | đông đối thủ | pháp lý, giữ chân |

## Đề xuất

**Đã chốt (2026-10-30): làm bản thử cả A và C, đánh solo 1 tướng đấu 1 địch, rồi chơi so hai bản mới chọn lõi.** Hai bản dùng chung sân đấu, tướng, địch và công thức sát thương; chỉ khác bàn puzzle bên dưới. Xem [10_BanThu_1v1.md](10_BanThu_1v1.md).

1. Bản thử A và C: 1 tướng, 1 địch có kỹ năng phá bàn. Câu hỏi: **bàn nào làm trận đánh vui hơn, và "màu quyết định hành động" có làm việc xếp hay hơn không?**
2. Nếu có, thêm thu phục ([05_VuotAi_ThuPhuc.md](05_VuotAi_ThuPhuc.md)) và nuôi tướng ([06_Tuong_NuoiDuong.md](06_Tuong_NuoiDuong.md)).
3. B vào sau, làm cơ chế của vài boss hoặc chế độ Tháp.
4. Máy bi làm sau cùng, khi đã có thứ để trả thưởng.
