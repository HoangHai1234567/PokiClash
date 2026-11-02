## 1. Logic (C# thuần)

- [x] 1.1 `Core/Badges.cs` (chép `Web/src/core/badges.ts`): mở đền (boss Đảo Thủy), mở dãy (mini boss ải 4 của đảo cùng hệ), tiến độ theo hệ và bậc, sinh đội địch theo công thức (cấp, số tướng, boss, hạt giống và mã trận cố định theo hệ, bậc, trận). Hệ chỉ có 2 tướng thì trận cuối 3 tướng lặp tướng
- [x] 1.2 Thưởng trận (`5 + 2·bậc` bi) và thưởng bậc (rương bạc bậc 1–2, vàng bậc 3–5, mở bằng hộp rương dùng chung); phần cộng `StatMods` theo bậc cao nhất, gắn vào đội người chơi (`Teams.MemberOf`) nên trận ở đảo, thử thách, màn Tướng và công cụ cân bằng đều thấy
- [x] 1.3 Lưu `badges` trong bản lưu (`{hệ: {tier, won}}`). Không cần bước di chuyển phiên bản: khoá mới, bản lưu cũ thiếu khoá thì mọi dãy ở bậc 0
- [x] 1.4 Thêm vào bản web: `src/core/badges.ts`, `data/badges.ts`, `StatMods` trên `Member` và `heroStats`, `npm run sim -- badges`; cấu hình xuất sang `balance.json`, golden `badges.json` (đội địch 200 trận, chỉ số có phần cộng, 5 trận đánh thật, tiến độ có rương)

## 2. Giao diện

- [x] 2.1 Công trình Đền Huy Hiệu trên sảnh: nét chì khi chưa mở, tô màu khi mở, chấm đỏ khi có dãy vừa mở chưa đánh; chạm vào mở scene `Badges`
- [x] 2.2 Scene Đền (`App/Scenes/BadgesScene.cs`, `Badges.unity`): 5 bệ theo thứ tự đảo (huy hiệu bậc cao nhất hoặc bóng mờ, bậc đang đánh n/5 hay n/10 kèm thanh, phần cộng, nút "Thử thách"); dãy chưa mở ghi điều kiện. Huy hiệu vẽ bằng code (huy chương tô màu bậc + biểu tượng hệ) tới khi có ảnh `ArtGen/SideMeta`
- [x] 2.3 Danh sách trận của bậc (đã thắng có dấu tích, trận đang đánh có "Đánh", còn lại khoá), hộp chuẩn bị trận dùng chung với đảo (`StagePrep.OpenBadge`), kết trận riêng: bi, tiến độ, "Trận tiếp »" / "Đánh lại" / "Về Đền"; xong bậc thì hộp huy hiệu rồi mở rương, sau cùng hộp lên cấp
- [x] 2.4 Icon huy hiệu cạnh nhãn hệ ở thẻ tướng và hộp chi tiết; chỉ số trong hộp chi tiết đã gồm phần huy hiệu (ghi ở dòng chú thích dưới bảng)

## 3. Kiểm tra

- [x] 3.1 EditMode (`BadgeTests`): đội địch 200 trận khớp web; chỉ số có phần cộng và 5 trận thật khớp web; tiến độ và rương khớp web; thua không mất tiến độ; phần cộng không cộng dồn; hệ khác không được cộng; lưu rồi đọc lại
- [x] 3.2 Công cụ cân bằng: tab "Huy hiệu" của cửa sổ Cân bằng (và `npm run sim -- badges`, hai bên ra cùng số): tỉ lệ thắng từng bậc ở cấp kỳ vọng, ảnh hưởng huy hiệu lên đảo; tab Trận có thanh chọn bậc huy hiệu cho mọi tướng
- [x] 3.3 Play (`PokiClash/Thử/Đền Huy Hiệu: đánh trọn bậc Đồng hệ Thủy`): mở đền, đánh 5 trận bậc Đồng hệ Thủy, hộp huy hiệu, rương bạc; Tiểu Y máu 849 → 891, công 385 → 404, thủ 98 → 102 (+5%); console không lỗi
- [ ] 3.4 Thay huy hiệu vẽ bằng code bằng ảnh gen (5 hệ × 5 bậc), ảnh nền đền và công trình đền trên sảnh khi `ArtGen/SideMeta`, `ArtGen/Hub` có ảnh
