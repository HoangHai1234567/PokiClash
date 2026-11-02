## Why

Chủ dự án (2026-10-31, khi trả lời câu hỏi còn mở): AFK cho quá nhiều bi, "giảm việc nhận được từ AFK đi, học hỏi việc cây sinh pinball trong Clash of Critters"; trang trại đầu game cho quá ít bi, "xem Clash of Critters".

Đo trước khi đổi (mô phỏng 30 ngày): AFK ra 4 + 0,8 bi/giờ cho mỗi ải đã qua (36 bi/giờ khi qua 40 ải), "Nhận ×2" không giới hạn; người chơi "vừa" nhận 51.050 bi AFK so với 5.822 bi từ ải. Trang trại đầu game 19–55 bi/ngày vì ca làm chỉ 2–5 giờ.

Cây bi của Critters (theo các trang hướng dẫn): tối đa 8 cây trong trại, mở dần theo cốt truyện; mỗi cây chứa 50 bi, đầy sau khoảng 8–10 giờ; đầy thì ngừng; người chơi vào hái. Ngoài cây không có thu nhập AFK từ trận.

## What Changes

- **Cây bi** (công trình mới trên sảnh, cạnh Trang trại):
  - 5 cây: cây 1 mở khi qua ải 1, cây 2–5 khi qua boss Đảo Thủy, Hỏa, Kim, Mộc;
  - mỗi cây 5 bi/giờ, chứa tối đa 50, đầy thì ngừng;
  - "Hái" lấy bi mọi cây, giữ phần lẻ; "Hái ×2" qua quảng cáo `tree_double`, 3 lần/ngày;
  - chấm đỏ khi có cây đầy.
- **AFK** thôi ra bi theo giờ: chỉ còn mảnh tướng boss (8% mỗi giờ), rương AFK, tăng tốc ×2. Bỏ "Nhận ×2" và chỗ quảng cáo `afk_double`; nút "Nhận" thành "Nhận mảnh".
- **Thẻ Phiêu Lưu:** cây bi ×1,5 (cả tốc độ lẫn sức chứa, vì người hái 2 lần/ngày luôn chạm trần) thay cho "AFK ×1,5"; khay 5 ô và rương mở 1 giờ giữ nguyên.
- **Trang trại, ca dài như cây:**
  - ca làm 8 giờ, +1 giờ mỗi sao;
  - kho mỗi chỗ giữ tối đa 10 giờ sản lượng;
  - năng suất gốc 2 bi/giờ, bỏ phần tăng theo cấp, giữ phần độ hiếm, sao, hợp hệ;
  - nghỉ 15–60 phút giữ công thức (ca 8 giờ nên thực tế là 60 phút).
- **Đường cong cấp** (`expBase`, `expPow`) đưa vào cấu hình. Số chưa đổi.
- **Công cụ:** menu `PokiClash/Cân bằng nhanh/Quét nhịp: EXP lên cấp, cây bi, trang trại` (3 kiểu người chơi × 30 ngày với nhiều tổ hợp hệ số).

## Capabilities

### New Capabilities

- `ball-trees`: cây bi trên sảnh, mở theo tiến độ, ra bi đều, đầy thì ngừng, hái tay, hái ×2 qua quảng cáo.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. Thay đổi so với add-afk-rewards (bỏ bi theo giờ, bỏ Nhận ×2), add-hero-farm (số ca, kho, năng suất), add-monetization-hooks (tree_double thay afk_double; Thẻ Phiêu Lưu tác động cây) ghi ở What Changes. -->

## Impact

- **Web:** `src/core/trees.ts`, `data/trees.ts` (mới); `afk.ts`, `data/ads.ts`, `data/farm.ts`, `progression.ts`; hộp AFK của web có thêm mục Cây bi; golden `trees.json` (mới), `afk.json`, `ads.json`, `farm.json`.
- **Unity:**
  - mới: `Core/Trees.cs`, `App/TreePanel.cs`, `Tests/TreesTests.cs`;
  - sửa: `Core/Afk.cs`, `AdGate.cs`, `BalanceConfig.cs`, `SaveData.cs` (khoá `trees`, không cần bước di chuyển), `ProgressSim.cs`, `Progress.cs`; `App/AfkPanel.cs`, `TopBars.cs`, `Scenes/HubScene.cs`; công cụ và test.
- **Nhịp tiến độ chưa đạt mục tiêu** (người chơi "vừa" xong 5 đảo khoảng ngày 21): xem `tasks.md` mục 4.
