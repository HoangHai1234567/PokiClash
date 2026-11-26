# Tranh thẻ chung: gói gửi GPT

Kế hoạch: `GD_Claude/36_TranhThe.md`. Sinh lại gói: `py -3 -I ArtGen/Cards/build.py`.

## Cách gửi

Mỗi lượt chỉ gửi GPT **đường dẫn một file prompt**. GPT tự mở ảnh mẫu và tự lưu ảnh vào `ArtGen/Cards/tai_ve/`.

| Lượt | File prompt | Thẻ | Lưu vào |
|---|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Cards\gui_gpt\luot_01.txt` | Mài Vuốt, Giáp Gỗ, Băng Gạc, Hít Thở, Gầm Gừ, Ném Đá, Cắn Xé, Nhảy Lùi, Đứng Tấn | `tai_ve/luot_01.png` |
| 2 | `D:\PokiClash\ArtGen\Cards\gui_gpt\luot_02.txt` | Hạt Dẻ, Bình Thuốc, Bánh Bao Thịt, Liều Mạng, Thủ Thế, Tĩnh Tâm, Phóng Lông, Tung Cát, Đấm Kép | `tai_ve/luot_02.png` |
| 3 | `D:\PokiClash\ArtGen\Cards\gui_gpt\luot_03.txt` | Trăng Khuyết, Cuồng Nộ, Phá Giáp, Búa Tạ, Hút Máu, Đốt Lửa, Suối Trong, Sấm Rền, Gương Đôi | `tai_ve/luot_03.png` |
| 4 | `D:\PokiClash\ArtGen\Cards\gui_gpt\luot_04.txt` | Mắt Ưng, Lông Phượng, Bùa Choáng, Hoà Khí, Áo Choàng Ma, Dồn Sức, Nghịch Thiên, Thiên Mệnh, Kim Độc | `tai_ve/luot_04.png` |
| 5 | `D:\PokiClash\ArtGen\Cards\gui_gpt\luot_05.txt` | Gai Nhọn, Vùng Dậy, Mai Rùa, Chuỗi Đòn, Đồng Lòng, Tích Lực, Bôi Bùn, Khắc Chế, Cướp Lửa | `tai_ve/luot_05.png` |
| 6 | `D:\PokiClash\ArtGen\Cards\gui_gpt\luot_06.txt` | Nén Giận, Dưỡng Sinh, Độc Tiễn, Kết Liễu, Khiên Gai, Tường Thành, Xuyên Phá, Mầm Xanh, Tàn Lửa | `tai_ve/luot_06.png` |
| 7 | `D:\PokiClash\ArtGen\Cards\gui_gpt\luot_07.txt` | Hút Linh, Đập Khiên, Ngũ Hành Hộ Thể, Bộc Độc, Hồi Liên Hoàn, Cắt Mạch, Bối Thủy, Bão Cát, Phong Ấn | `tai_ve/luot_07.png` |
| 8 | `D:\PokiClash\ArtGen\Cards\gui_gpt\luot_08.txt` | Huyết Tế, Thuận Thiên, Vạn Độc, Khai Nhãn, Giáp Gương, Độc Long, Bão Liên Hoàn, Khắc Tinh, Lưỡi Hái | `tai_ve/luot_08.png` |
| 9 | `D:\PokiClash\ArtGen\Cards\gui_gpt\luot_09.txt` | Ngũ Hành Quy Nhất, Thiên Hộ, Huyết Long | `tai_ve/luot_09.png` |

## Ảnh mẫu trông thế nào

- `ArtGen/Islands/refs/world_style.png` (1024 × 1536): bản đồ 5 vùng hệ vẽ tay, viền nâu rung, gạch chì màu trên giấy kem. Chỉ lấy cách vẽ.
- `ArtGen/Spine/inbox/dat_nung_1/tai_ve/L3_1.png` (1536 × 1024, nền trắng): concept tướng đất nung cầm kiếm, tô phẳng chì sáp. Chỉ lấy cách tô.
- `ArtGen/Cards/gui_gpt/bo_cuc_<k>.png` (1536 × 1024, nền trắng): k ô xám 464 × 290 đánh số 1…k, chỗ đặt từng tranh.
- Từ lượt 2: `ArtGen/Cards/tai_ve/luot_01.png`, tấm lượt 1 đã duyệt, để giữ nét đồng đều.

## Cách kiểm

- Đủ số ô, đúng chỗ, mỗi ô một tranh có viền mực, khe trắng giữa các ô, không hình nào lấn ra khe.
- Tranh đúng thứ tự thẻ (ô 1 = thẻ đầu tiên trong bảng trên).
- **Nhìn là đoán được thẻ làm gì** (người dùng dặn 2026-11-27): tim = máu, dấu cộng xanh = hồi, giọt xanh = mana, lửa cam = nộ, kiếm = công, khiên xanh = thủ, bong bóng xanh nhạt = khiên chắn, mũi tên xanh lên = tăng, mũi tên đỏ xuống = giảm, đồng hồ cát = nhiều lượt, sao quanh đầu = choáng, bọt xanh lá + đầu lâu = độc; địch luôn là hình nộm rơm.
- Gần như không có thú: không chân, lông, móng, mặt thú (trừ khi cảnh ghi rõ, như cặp nanh của Cắn Xé).
- Nhìn thu nhỏ còn đọc được: ý chính to, rõ.
- Không chữ, không số; không bóng đổ, không quầng sáng, không bóng loáng; tô phẳng.

## Câu sửa nhanh (gửi GPT kèm file prompt)

- Lệch ô: `Same pictures, but put each one exactly inside its rectangle from image 3, with white gutters between them.`
- Bóng, sáng: `Same pictures, but flat colours only: no shading, no glow, no shine spots, no drop shadows.`
- Nhỏ, rối: `Same pictures, but make each main subject bigger and simpler, readable at 280 x 175 px.`
- Có chữ: `Same pictures, with no text, letters or numbers anywhere.`
