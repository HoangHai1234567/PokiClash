# 28. Sổ Phép (cây kỹ năng cấp tài khoản)

Người dùng 2026-11-24: "nghiên cứu kĩ về skill tree ... tôi muốn thêm skill tree vào game", rồi duyệt cả 14 câu theo đề xuất ("Làm theo bạn
đề xuất"). Báo cáo nghiên cứu: `GD_Claude/reports/Cây kỹ năng cho PokiClash.md`, ghi chú gốc `GD_Claude/research_notes/Cây kỹ năng cho PokiClash/`.

## Đã chốt

| # | Câu | Chốt |
|---|---|---|
| 1 | Cây để làm gì | Lựa chọn lối chơi và chỗ tiêu tài nguyên đang chết; cốt truyện là vỏ |
| 2 | Dạng cây | Một cây tài khoản "Sổ Phép" trước; biến thể Tuyệt kỹ ở thẻ cấp 5 ("Nét Sao") để giai đoạn 2 |
| 3 | Cấp mở | 50 |
| 4 | Nét sau cấp 200 | EXP thừa, 27.000 EXP một nét, tối đa 7; chúa tể là cổng chương 4 |
| 5 | Ô chốt tốn đá tiến hóa | Có: 20 / 30 / 50 (chương 2 / 3 / 4), tổng 100, chỉnh theo số đá dư đo được |
| 6 | Ngân sách sức mạnh | Cả sổ ≤ +3 cấp tương đương |
| 7 | Địch bám sổ | Không |
| 8 | Đặt lại | Miễn phí, ngoài trận, không giới hạn |
| 9 | Ô kinh tế | Không |
| 10 | Bán gì | Chỉ trang trí (Bìa Sổ); không bán nét, không bán lượt tẩy |
| 11 | EXP sau khi đầy sổ | Bỏ như cũ |
| 12 | Lối vào | Thẻ công trình ở rìa làng (chỗ thẻ Cây bi đã ẩn), một bước hướng dẫn khi mở |
| 13 | Câu 14 (lệch chỉ số màn Tướng và trận) | Sửa trước: hoá ra là lỗi của menu thử (so chỉ số gốc với tướng đầu đội), game đã khớp; thêm test |
| 14 | Tên | "Sổ Phép", "nét", 4 chương và 20 ô như dưới |

## Khung

- 4 chương × 5 ô = 20 ô; vẽ đủ cả sổ cần 40 nét và 100 đá tiến hóa.
- Nguồn nét: 3 khi mở sổ (cấp 50), 1 ở mỗi cấp tận cùng 3 và 8 từ 53 tới 198 (30 nét, lệch mốc Quỹ Phiêu Lưu), 7 từ EXP thừa sau cấp 200.
  Nét tính lại từ cấp và số nét EXP đã đổi, không lưu.
- Cổng chương (ghi trên trang khoá): 1 cấp 50; 2 cấp 60 và đã vẽ 4 nét; 3 cấp 100 và đã vẽ 12 nét; 4 hạ một chúa tể (ải cuối một đảo
  bất kỳ) và đã vẽ 22 nét. Ô chốt cần đã vẽ 3 ô khác cùng chương.
- Loại ô: ô cấp (2 cấp, giá 1 rồi 2), ô đơn, ô chọn (hai mặt, đổi mặt tự do không tốn gì), ô chốt (ô chọn lớn, chương 2–4 tốn đá), ô chọn
  1 trong 5 hệ, ô trang trí. Không ô nào cộng % Máu / Công / Thủ, không ô nào cho bi, EXP, AFK, không dùng móc của Tiềm năng (mana, nộ,
  khiên đầu trận) hay móc gần như không chạy trong trận 2 lượt.
- Tẩy sổ miễn phí: hoàn hết nét và đá, giữ mặt đã chọn. Nút Gợi ý vẽ theo đường gợi ý (cũng là đường ProgressSim dùng).

## Hai mươi ô (số ở `balance.json` khối `sophep`, chữ ở `SoPhep.Describe`; số sau 6 lượt đo ngày 2026-11-25)

| Chương | Ô | Loại | Hiệu ứng | Giá |
|---|---|---|---|---|
| 1 Nét Mở Đầu | Lật Trang | cấp | Mỗi trận đổi cả bộ thẻ đang chọn 1 / 2 lần (nút "Lật trang ×N" ở đầu hàng thẻ) | 1 + 2 |
| | Rộng Tay \| Dồn Tay | chọn | Lần chọn đầu mỗi lượt +1 thẻ \| thẻ cùng nhóm với thẻ vừa chọn ×2 trọng số ở lần rút kế | 2 |
| | Giữ Nét | đơn | Một lần mỗi trận: thẻ hiếm nhất bỏ qua ở lần chọn cuối giữ sang lần chọn đầu lượt sau | 1 |
| | Mắt Tinh | đơn | Thẻ Hiếm trở lên ×1,2 trọng số | 1 |
| | Thêm Lá \| Thêm Lượt | chốt | Mỗi lượt chọn 5 lần × 4 thẻ (thêm lựa chọn) \| 6 lần × 2 thẻ (thêm lá, bớt lựa chọn) | 2 |
| 2 Nét Đồng Hành | Mực Chờ | cấp | Tướng dự bị +3 / +6 mana mỗi lượt | 1 + 2 |
| | Vào Sân \| Rút Lui | chọn | Tướng vào sân có khiên 8% máu \| tự đổi thì tướng ra hồi 8% máu | 2 |
| | Tiếp Sức | đơn | Tự đổi tướng: tướng vào nhận 50% mana tướng ra | 1 |
| | Tiếp Nối | đơn | Tướng gục: tướng ra thay có sẵn 25 nộ | 1 |
| | Đổi Vai \| Hợp Lực | chốt | 1 lần mỗi trận đổi tướng cả khi đã chọn thẻ \| tung Tuyệt kỹ thì mỗi tướng dự bị đánh phụ 15% Công | 2 + 20 đá |
| 3 Nét Khắc Chế | Mũi Nhọn \| Lá Chắn | chọn | Đánh hệ mình khắc ×1,5 → ×1,55 \| đánh hệ khắc mình ×0,75 → ×0,8 | 2 |
| | Sổ Tay Chúa Tể | cấp | Trận có boss / mini boss: +1 / +2 lần Lật Trang | 1 + 2 |
| | Nét Cứu | đơn | Lần đầu một tướng dưới 25% máu mỗi trận: hồi 10% | 2 |
| | Tỉnh Táo | đơn | Hết choáng thì miễn choáng tới hết lượt sau | 1 |
| | Vẽ Lại \| Phản Nét | chốt | 1 lần mỗi trận tướng gục sống lại 25% máu và mất lượt kế (không áp boss) \| lần đầu dưới 25% máu: phản 10% sát thương tới hết trận | 2 + 30 đá |
| 4 Nét Chúa Tể | Năm Bút Chì | 1 trong 5 hệ | Đánh địch hệ đã chọn: mỗi lần chọn +1 thẻ | 3 |
| | Trang Cuối | đơn | Lần chọn cuối mỗi lượt hiện 4 thẻ | 2 |
| | Nét Kết | đơn | Đòn của mình để địch (không phải boss) dưới 10% máu thì kết liễu | 2 |
| | Bìa Sổ | trang trí | Màn mở khoá tướng: nét viền mang màu hệ của tướng | 1 |
| | Chữ Ký \| Nét Kép | chốt | Tuyệt kỹ đầu tiên mỗi trận bớt 50% nộ \| thẻ chọn đầu tiên mỗi trận chạy hai lần | 4 + 50 đá |

## Đo (menu "PokiClash/Cân bằng nhanh/Sổ Phép: …", 2026-11-25)

- Cách đo: mỗi đảo ải 25 / 50 / 70, đội mẫu của đảo (`simTeams`) với sao, thẻ của người chơi "vừa"; hạ cấp đội tới khi không sổ chỉ thắng
  ≤ 70%, rồi so với sổ người "vừa" có ở cấp ải (vẽ theo đường gợi ý); số cấp tương đương = chỗ tỉ lệ thắng có sổ cắt đường không sổ ở
  +2…+12 cấp. 150 trận mỗi ô. Máy đánh bên người chơi chỉ dùng Lật Trang khi cả bộ toàn thẻ Thường nên đo thấp hơn người chơi thật.
- Bản đầu (số trong báo cáo): trung bình +5,1 cấp, cuối game tới +12 (Vẽ Lại hồi 30% máu riêng nó +4,1 cấp). Chỉnh 5 lượt (giảm số, không
  nâng địch, theo câu 6–7): bản hiện tại **trung bình +2,4 cấp**; đầu game (9 nét) +1,4…+2,2, giữa (20–23 nét) +1,9…+3,3, cuối (30–32 nét)
  +1,8…+4,0 (trung bình ≈ +3,0). Ô kéo nhiều nhất còn lại: Thêm Lá +0,7 cấp; các ô khác ≤ +0,3.
- Hai mặt của ô chọn (sổ đầy): chênh dưới 3% (sai số ±4%) sau khi Chữ Ký đổi từ "miễn nộ" sang "bớt 50% nộ" (trước đó hơn Nét Kép 8%).
  Vẽ Lại có giá "mất lượt kế" thì máy đánh dùng gần như không lợi (−0,3 cấp): cần xem lại khi có người chơi thật.
- Nhịp 60 ngày (ProgressSim ba kiểu người chơi, 2026-11-25), không sổ → có sổ: chăm cấp 200 ngày 33 → 32, vừa ngày 46 → 45, ít cấp 87
  ngày 30 → 87; bi ải 59 / 26 / 5% → 59 / 27 / 5%; đủ cả ba mục tiêu (vừa ~ngày 45, bi ải ≥ 25%, ít ≥ cấp 80 ngày 30). Sổ ngày 30: chăm
  28 nét, vừa 24, ít 10; đầy sổ: chăm ngày 36, vừa ngày 53, ít chưa tới trong 60 ngày.

## Code

- `Core/SoPhep.cs`: cấu hình (`SoPhepConfig`, nạp từ `balance.json` khối `sophep`), trạng thái lưu (`SaveData.sophep`: cấp từng ô, mặt,
  đá đã trả, nét EXP, EXP đang góp), nguồn nét, cổng, mua, chọn mặt, tẩy, đường gợi ý `AutoBuy`, luật trận `Rules` → `BattleRules`, chữ.
- `Core/Battle/BattleTypes.cs` `BattleRules` + `RuleState` (lượt dùng một-lần-mỗi-trận) trên `Side`; `TeamSetup.rules`; `Teams.Player`
  gắn luật của bản lưu. `Battle.cs`: số thẻ (`OfferSize`), trọng số, thẻ giữ, `Reroll`, số lần chọn, mana dự bị, đổi tướng (khiên, hồi,
  chuyền mana, nộ, đổi giữa lượt), Hợp Lực, khắc hệ, kết liễu, Vẽ Lại, Nét Cứu, Phản Nét (buff Thorns), miễn choáng, Tuyệt kỹ miễn nộ,
  Nét Kép. Đội không có sổ (mọi đội máy, mọi bản lưu cũ) đi đúng đường cũ từng bước: golden trận không đổi.
- `Progress.AddExp`: EXP thừa ở cấp tối đa góp vào sổ (`SoPhep.Bank`).
- `BattleAi`: máy bên người chơi (giả lập) Lật Trang khi cả bộ toàn thẻ Thường.
- `ProgressSim`: vẽ theo đường gợi ý sau bước tiến hóa (`ProgressSim.SoPhepOn`); khoá đệm tỉ lệ thắng có dấu của sổ.
- Giao diện: `App/SoPhepDialog.cs`, `App/SoPhepTile.cs`; màn trận `BattleView.p.reroll` (nút "Lật trang ×N" ở đầu hàng thẻ), hàng thẻ
  thu nhỏ khi hơn 3 lá; sảnh thẻ công trình thứ 4; khoảnh khắc mở `h_sophep` (Tutorial.NextUnlock) → khoanh thẻ Sổ Phép (`h_sophep2`)
  → trong sổ chọn sẵn Lật Trang, khoanh nút Vẽ (`h_sophep3`).
- Prefab: menu "PokiClash/Prefab/Hộp thoại và màn/Sổ Phép" (`Editor/SoPhepMenu.cs`) dựng `Items/OSoPhep`, `Dialogs/SoPhep`, vá
  `Screens/Battle` (nút Lật trang), `Screens/Hub` (icon thẻ công trình).
- Đo: menu "PokiClash/Cân bằng nhanh/Sổ Phép: …" (`Editor/SoPhepBalanceMenu.cs`): ngân sách cấp tương đương, so hai mặt của ô chọn, nhịp
  60 ngày có / không sổ.
- Test: `Tests/SoPhepTests.cs`; câu 14: `PotentialTests.ChiSoManTuong_KhopTrongTran_KhiCoHuyHieuTiemNang`.

## Còn chờ

- Hiệu ứng vẽ khi mua ô (bút chì lần viền như màn mở khoá tướng) chưa làm: hiện chỉ đóng dấu và nảy ô.
- Nút Tuyệt kỹ trong trận chưa hiện số nộ đã bớt của Chữ Ký.
- Giai đoạn 2: "Nét Sao" (biến thể Tuyệt kỹ ở thẻ cấp 5, tiêu bản sao dư).

## Icon

20 icon ô (128 px) gen bằng GPT qua Magnific (model gpt-2-6, nền trong suốt, một tấm lưới 5 × 4, 95 credit, ảnh mẫu là 8 icon của bộ
`Fallback/Icons` để cùng kiểu viền nâu tô phẳng): `ArtGen/UI/so_phep/tai_ve/luoi_icon.png`, cắt bằng `ArtGen/UI/so_phep/cat_icon.py`
(lọc chấm vụn, thu vừa 128 px) vào `Assets/03 Art/SoPhep/<id>.png` (338 KB ảnh gốc, ASTC khi build ~150 KB). Prefab `Dialogs/SoPhep` giữ
mảng icon theo thứ tự ô (`SoPhepDialog.p.icons`), không đụng danh mục ảnh chung; thiếu ảnh thì mượn icon `icon` trong `balance.json`.
Chụp thử: menu "PokiClash/Thử/Sổ Phép: màn sổ và nút Lật trang, chụp (đang Play)" → `Temp/PokiShots/so_phep/`.
