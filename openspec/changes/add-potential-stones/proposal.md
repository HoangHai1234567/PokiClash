## Why

GDD gốc, Side Meta: "Thu thập tiềm năng: những đá tiềm năng có thể lấy được từ việc mở hòm pachinko, 1 tướng có thể trang bị 4 tiềm năng. Các tiềm năng sẽ buff chỉ số cho tướng. Mỗi lần cho tướng vào khai phá tiềm năng sẽ mất đá tiềm năng. Những tiềm năng hiếm có tỉ lệ ra sẽ thấp. Cũng có thể build 1 side quest riêng đánh boss cày đá tiềm năng nhưng người chơi sẽ phải chơi chứ không afk."

Tiềm năng thêm một trục nuôi tướng có may rủi nhẹ và có chỗ tiêu tài nguyên lâu dài. Bản web chưa có phần này.

## What Changes

- **Tài nguyên mới:** đá tiềm năng.
  - Nguồn: rương bạc và rương vàng của máy bi (thêm dòng kết quả), Hang Tiềm Năng, rương AFK (hiếm).
- **4 ô tiềm năng mỗi tướng,** mở theo sao: ô 1 ở 1 sao, ô 2 ở 2 sao, ô 3 ở 3 sao, ô 4 ở 4 sao.
- **Khai phá:**
  - tốn đá, quay lại mọi ô đã mở và không khoá;
  - mỗi ô ra một dòng tiềm năng (loại chỉ số và độ hiếm);
  - khoá được tối đa 2 ô, mỗi ô khoá tốn thêm đá;
  - kết quả hiện trước, người chơi chọn "Giữ mới" hoặc "Giữ cũ".
- **Dòng tiềm năng:** 8 loại: Công %, Thủ %, Máu %, Tốc, Chí mạng %, Hút máu %, Mana đầu trận, Nộ đầu trận. Mỗi loại có 5 độ hiếm, tỉ lệ ra Thường 55, Khá 28, Hiếm 12, Sử thi 4,5, Huyền thoại 0,5.
- **Hang Tiềm Năng:**
  - công trình ở rìa làng, scene riêng, mở khi thắng mini boss Đảo Hỏa;
  - 4 tầng độ khó, mỗi lần vào là một trận boss phải tự chơi;
  - thắng ra đá theo tầng;
  - 3 lượt vào mỗi ngày, chỉ trừ lượt khi thắng.
- **Mục "Tiềm năng"** trong hộp chi tiết tướng: 4 ô, nút Khai phá, khoá ô, so sánh trước/sau.

## Capabilities

### New Capabilities

- `potential-stones`: đá tiềm năng và nguồn, 4 ô theo sao, khai phá có khoá ô và chọn giữ, bảng dòng tiềm năng, áp vào chỉ số và trận, Hang Tiềm Năng.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. Bảng rương máy bi đổi theo change này: xem design. -->

## Impact

- **Code:** `Core/SideMeta/Potential` (quay dòng, khoá, áp `mods` và hiệu ứng đầu trận); `Game/Potential` (Hang, mục tiềm năng trong chi tiết tướng).
- **Trận:** hiệu ứng đầu trận (mana, nộ, chí mạng, hút máu) cộng vào lúc dựng tướng (`MakeFighter`).
- **Máy bi:** thêm dòng "đá tiềm năng" vào rương bạc (8%, 1–2 đá) và rương vàng (12%, 2–4 đá). Các dòng cũ giảm tỉ lệ theo; bảng tỉ lệ hiển thị cập nhật theo.
- **Lưu:** `potentialStones`, `heroes[id].potential[4]`, `caveEntries` theo ngày.
- **Ảnh:**
  - icon đá theo 5 độ hiếm, khung ô tiềm năng (`ArtGen/SideMeta`);
  - nền Hang (`ArtGen/SideMeta`); công trình Hang trên sảnh (`ArtGen/Hub`).
- **Phụ thuộc:** `add-hero-roster`, `add-card-battle`, `add-pachinko-machine`, `add-world-islands`.
