## Why

Các con số đã có trên bản web đều đo bằng máy tự chơi (`npm run sim`), chưa có người chơi thật thử:
- 23 thẻ chung, 33 thẻ riêng;
- 40 ải, bảng rương, đường cong EXP;
- side meta mới (huy hiệu, tiềm năng, trang trại).

Unity cần cùng bộ công cụ để chỉnh số mà không đoán mò, và để người thử chơi tua nhanh tới phần cần xem. GDD gốc không nói công cụ, nhưng mọi mục "nghĩ thêm sau" của GDD đều cần chỉnh số.

## What Changes

- **Cửa sổ Editor "PokiClash/Cân bằng":**
  - chạy N trận máy tự chơi cho một ải, một đảo, hoặc cả 40 ải;
  - chọn đội, cấp, sao, cấp thẻ, phần cộng side meta;
  - ra bảng tỉ lệ thắng và số hiệp trung bình, xuất CSV.
- **Mô phỏng máy bi:** 6.000 bi, ra tỉ lệ từng ô, EXP và bi hoàn mỗi bi, thẻ mỗi bi, theo mặt máy và bảng rương hiện tại.
- **Mô phỏng tiến độ:**
  - ước cấp người chơi theo số ải đã qua, theo 3 kiểu người chơi (chăm, vừa, ít), tính bi từ ải, AFK, trang trại, máy bi;
  - đối chiếu với cấp đề nghị của từng đảo.
- **Sổ tay, mục "Bảng thử" (chỉ bản dev):** +50 bi, +500 XP, tua AFK 1/8 giờ, mở hết tướng, mở hết ải, +5 bản sao mọi thẻ, +10 đá tiềm năng, tua giờ trang trại.
- **Sổ tay, mục "Chỉnh số" (chỉ bản dev):** sửa các hệ số chính của `BalanceConfig` ngay khi chơi; có nút "Về số gốc".
- **Golden:** kiểm tra định kỳ để Unity và bản web cùng ra một kết quả.
- **Ghi trận:** mỗi trận ghi một dòng (ải, đội, kết quả, số hiệp, thời gian thật, máu còn, tự chơi hay tay) vào CSV, như bản thử Unity cũ (`BanThu/tran.csv`).

## Capabilities

### New Capabilities

- `balance-tools`: máy tự chơi hàng loạt, mô phỏng máy bi và tiến độ, bảng thử và chỉnh số trong bản dev, ghi trận, kiểm tra golden với bản web.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code:** `Editor/Balance` (cửa sổ, xuất CSV); `Game/Notebook` (mục bảng thử, chỉnh số; bọc `POKICLASH_DEV`); `Core/Sim` (chạy trận, mô phỏng tiến độ).
- **File ghi:** `PokiClash/Logs/tran.csv` (ngoài Assets), CSV cân bằng.
- **Phụ thuộc:** `add-card-battle`, `add-hero-roster`, `add-world-islands`, `add-pachinko-machine`. Phần side meta thêm vào khi các change đó xong.
