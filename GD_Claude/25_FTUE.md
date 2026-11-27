# FTUE: dẫn người chơi mới vào game, mỗi lần một thứ

Viết 2026-11-22. Người dùng dặn: quét kỹ game, thiết kế FTUE chuẩn để người chơi tiếp cận không bị ngợp, có "cách chơi", giới thiệu từng thứ một, rồi viết kịch bản. Chưa sửa code. Số liệu lấy từ code và JSON ngày 2026-11-22.

## Tóm tắt

- **Hôm nay người mới gặp gì:**
  - hộp giới thiệu 4 khung chữ (chữ đã cũ);
  - hộp chọn tướng dồn cả hệ khắc lẫn 3 thẻ chiêu;
  - một sảnh hiện đủ 5 nút đáy, 4 công trình và nút AFK.
  - Trong trận chỉ có 3 bong bóng gợi ý, tự tắt sau 4,2 giây.
  - Không có gì dẫn tới máy bi, trong khi EXP chỉ đến từ máy bi và ải 2 đã là địch cấp 6.
- **Đề xuất:**
  - một chuỗi bắt buộc ngắn (khoảng 8 phút), đi trọn vòng lõi một lần: chọn tướng → trận 1 → máy bi → lên cấp → nâng thẻ → trận 2 khắc hệ;
  - sau đó chỉ còn gợi ý theo lúc ("lần đầu X xảy ra"), mỗi lần một thứ;
  - nút và công trình chỉ hiện khi tới lượt.
- **Cần làm:**
  - một bộ hướng dẫn chung: lớp phủ khoanh vùng bằng nét bút chì, ghi chú giấy, cờ trong bản lưu;
  - móc viết sẵn kết quả cho trận 1–2 và 13 bi đầu;
  - sửa vài chỗ cũ: chữ hộp giới thiệu, hộp lên cấp, mẹo màn tải.
- 9 câu cần chốt ở mục 9, mỗi câu có đề xuất.

## 1. Người mới thấy gì hôm nay

1. **Màn tải** chuyến tàu (ít nhất 2,4 giây): mẹo ngẫu nhiên trong 7 câu, có câu về khắc hệ và về Nhà, dù người mới chưa gặp cả hai.
2. **Sảnh:** mây phủ cả 5 đảo. Sau 0,5 giây hiện hộp `GioiThieu` 4 khung và nút "Bắt đầu!".
3. **Chọn tướng khởi đầu** (bắt buộc): 5 tướng; chạm một tướng thì hiện hệ, khắc, bị khắc, 3 thẻ.
4. **Mây tan** ở đảo cùng hệ với tướng đã chọn, camera lướt tới. Không có gì chỉ phải làm gì tiếp, chỉ có mũi tên nhún ở đảo gợi ý.
5. **Vào ải 1:** đảo → chạm ải 1 → hộp Chuẩn bị (ô đội 1, hai ô khoá "cấp 60") → Xuất trận.
6. **Trận gương** với bóng của chính tướng mình (yếu 20%). Bong bóng "chọn thẻ", "Chiêu", "Tuyệt kỹ" hiện 4,2 giây rồi tự tắt, chỉ ở trận đầu, không dừng trận.
7. **Thắng:** hộp kết quả có "Máy bi (n)", "Ải tiếp »", "Đánh lại", tên đảo. Về sảnh thì mây tan nốt 4 đảo.

### Chỗ gây ngợp hoặc sai

| # | Chỗ | Vì sao là vấn đề |
|---|---|---|
| V1 | Hộp giới thiệu 4 khung | Bắt đọc trước khi chơi. Chữ cũ: "Bạn có Tiểu Y hệ Thủy", "Xen Chiêu và Tuyệt kỹ vào hàng thẻ" (nay Chiêu ra đòn ngay) |
| V2 | Hộp chọn tướng | Hệ khắc, bị khắc, 3 thẻ chiêu hiện ra trước khi người chơi biết thẻ là gì |
| V3 | Sảnh hiện hết | 5 nút đáy, 4 công trình (bản phác chì khi khoá), nút AFK ghi "AFK" dù chưa có gì: 10 chỗ để chạm, chỉ 1 chỗ cần chạm |
| V4 | Gợi ý trong trận | Chỉ 3 câu, tự tắt, không dừng trận, không ép làm. Không giải thích hàng thẻ chạy cuối lượt, nộ, khắc hệ |
| V5 | 22 thẻ chung mở ngay ở cấp 1 | Có thẻ khó hiểu: Liều Mạng (tự mất máu), Gai Nhọn (phản đòn), Kim Độc, Cuồng Nộ (đổi Thủ lấy Công), Vùng Dậy (theo máu đã mất). Cấp 2–6 gần như không mở thẻ mới, nên hộp "Lên cấp" ít khi có gì để khoe |
| V6 | Không có đường tới máy bi | EXP chỉ đến từ máy bi và rương; thắng ải chỉ ra bi, mảnh, đá. Người chơi không biết phải thả bi mới lên cấp |
| V7 | Dốc cấp ngay đầu | Bản lưu mới ở cấp 1, có 10 bi. Đảo Thủy: ải 2 địch cấp 6, ải 3 cấp 11, ải 5 cấp 18. Người chưa vào máy bi sẽ thua ở ải 2–3 mà không biết vì sao |
| V8 | Hộp thua | Chỉ một dòng mẹo. Không có nút tới chỗ làm mạnh lên, không nói "thua không mất gì" |
| V9 | Tướng tặng ở ải 3 đảo Thủy | Tê Thiềm (Thổ, khắc Thủy) vào kho mà không vào đội, vì ô 2 mở ở cấp 60. Không có gì gợi ý đổi tướng. Chú thích ở `Progress.cs:464` còn ghi ô 2 mở cùng lúc nhận quà |
| V10 | Hộp lên cấp | Dòng "×N" luôn trống (cược nay mở theo số bi). Không báo tính năng mới mở: cây bi 2, Hang, tiến hóa đều mở cùng lúc ở cấp 30 |
| V11 | Không có trang "Cách chơi" | Sổ tay chỉ có cài đặt. Quên luật thì không có chỗ xem lại |
| V12 | Không đo | Không biết người chơi bỏ ở bước nào |

### Đã có, dùng lại được

- Mây che đảo mở theo tiến trình (`HubIslands`): có hoạt cảnh lướt camera, chặn chạm (`CloudCover.Block`). Cờ `TutorialDone` đang là chỗ giữ, hiện nghĩa là "đã thắng một ải bất kỳ".
- Bộ thu hút chú ý: `UiHint` (bong bóng), `Bob`, `Pulse`, chấm đỏ, số trên nút, toast.
- `InkPath` vẽ dần nét mực (mũi tên, vòng khoanh). Cùng ảnh bút chì của màn sa bàn, nó làm được con trỏ đúng chất sổ tay.
- Máy bi chọn kết quả trước rồi mới phát đường bi (`Board.odds`), nên viết sẵn được kết quả những bi đầu mà đường bi vẫn là vật lý thật.
- Cờ trong bản lưu: `intro`, `starter`, `stats.battles`, `extra[...]`. Khoá lạ trong `extra` được giữ nguyên khi lưu, nên thêm cờ hướng dẫn không cần đổi phiên bản bản lưu.
- Nút "Tự chơi" trong trận.

## 2. Nguyên tắc

1. **Chơi trước, đọc sau.** Mỗi bước là một hành động. Mỗi lời chỉ một câu, khoảng 12 chữ. Không có hộp chữ dài nào trước trận đầu.
2. **Mỗi lần một thứ.** Mỗi bước chỉ khoanh một chỗ. Chưa tới lượt thì không hiện: ẩn hẳn, không để mờ.
3. **Vào trận đầu trong 90 giây** kể từ lúc mở game.
4. **Chỉ ép làm trong vòng lõi đầu** (chặng A–C, khoảng 8 phút). Sau đó là gợi ý mềm: khoanh, nhún, bỏ qua được.
5. **Theo lúc, không theo lịch.** Gợi ý gắn với "lần đầu X xảy ra" (lần đầu đủ nộ, lần đầu gặp 2 địch, lần đầu có đá tiềm năng). Người chơi đi đường nào cũng gặp đúng lúc.
6. **Không thua trong chuỗi bắt buộc.** Trận 1–2 khoá thua ngầm; máy bi lần đầu có kết quả viết sẵn. Lần thua đầu tiên sau đó được đỡ (chặng E).
7. **Thật thà.** Không giả "suýt trúng". Nói rõ cược ×N chỉ nhanh hơn, không lời hơn (đúng luật ở `07_MayBi.md`).
8. **Mỗi tính năng mở là một khoảnh khắc riêng:** một hộp, một câu, một nút "Đi xem". Nhiều thứ mở cùng lúc thì xếp hàng, mỗi lần vào sảnh mở một.
9. **Bước nào xong là lưu ngay.** Tắt game giữa chừng thì vào lại đúng bước, không lặp bước đã xong.
10. **Có chỗ xem lại:** trang "Cách chơi" trong Sổ tay, mỗi trang mở khi đã học xong phần đó.

## 3. Lịch giới thiệu: mỗi thứ vào lúc nào

Chặng A–C là chuỗi bắt buộc của phiên đầu. Từ D trở đi là gợi ý theo lúc. Cột "Bước" trỏ tới kịch bản ở mục 4.

| Thứ | Giới thiệu khi | Bước |
|---|---|---|
| Chọn tướng đồng hành | mở game lần đầu | A2–A5 |
| Đảo, ải, hộp Chuẩn bị | sau khi chọn tướng | A6–A9 |
| Chọn 1 trong 3 thẻ, 5 lần mỗi lượt | trận 1, lượt 1 | B1–B2 |
| Hàng thẻ chạy cuối lượt, rồi đánh thường | trận 1, sau lần chọn thứ 5 | B3 |
| Chiêu (mana) | trận 1, lượt 2 | B5 |
| Bi | kết quả trận 1 | B8 |
| Thả bi, EXP, cấp chung của mọi tướng | máy bi lần 1 | C1–C3 |
| Lên cấp, thẻ mới vào bộ | lên cấp 2 (viết sẵn) | C4 |
| Rương, bản sao thẻ | rương đầu (viết sẵn) | C5–C6 |
| Nâng cấp thẻ riêng | ngay sau rương đầu | C8–C10 |
| 4 đảo còn lại | về sảnh sau khi nâng thẻ | C11 |
| Khắc hệ ×1,5 | trận 2, ở đảo của hệ mình khắc | C12–C14 |
| Tuyệt kỹ (nộ) | lần đầu đủ nộ (bảo đảm có ở trận 2) | C15 |
| Mảnh, thu phục | kết quả trận 2 | C16 |
| Nhiều địch, hiệu ứng, choáng, địch tiến hóa | lần đầu mỗi thứ | D1–D5 |
| Tự chơi | trận thứ 3 | D6 |
| Sổ thẻ | về sảnh sau trận 2 (2026-11-24) | C18–C19 |
| Nhà: Nhà chính, ruộng vườn, xưởng gỗ, kho | sau Sổ thẻ, mở sau ải thứ 2 (2026-11-24) | C20–C25 |
| Cửa hàng | về sảnh sau khi đi hết Nhà (2026-11-24) | C26 |
| Rương mốc đảo | lần đầu tới ải 10 | D8 (D9 Sổ thẻ bỏ 2026-11-23) |
| Địch hơn cấp, lần thua đầu | lần đầu mỗi thứ | E1–E2 |
| Cây bi (từ 2026-11-23 đến cùng Nhà) | vào Nhà lần đầu, trong chuỗi bắt buộc từ 2026-11-24 | G3a–G3d |
| AFK | phiên 2 | F1–F3 |
| Mốc Huyền thoại, nấm tiến độ, cược | máy bi lần 2 trở đi | F4–F7 |
| Chọn tướng theo hệ địch (1 ô đội) | lần đầu có tướng khắc ải kế | F8 |
| Thu phục bằng mảnh, lên sao | lần đầu đủ mảnh | F9–F10 |
| Nhà (phần còn lại) | sau chuỗi bắt buộc (G1–G2 đã dời vào C20–C21) | G4–G10 |
| Tiềm năng, tiến hóa, Hang, cây bi 2–5, Đền, ô đội 2 và đổi tướng | theo điều kiện mở | H |

## 4. Kịch bản

Ký hiệu:
- **Ép**: phủ tối cả màn, chừa đúng chỗ cần chạm (khoanh bút chì). Chạm chỗ khác không có tác dụng.
- **Gợi ý**: khoanh và nhún, không chặn. Tự tắt khi người chơi làm, hoặc sau 6 giây không làm.
- **Chú thích**: một ghi chú giấy cạnh chỗ đó, không chặn, tự tắt.
- `{tuong}` là tên tướng đồng hành, `{he}` là hệ của nó; `{he2}`, `{tuong2}` là hệ và tướng của đảo mình khắc.
- **Lời:** phần lớn là ghi chú giấy, giọng người dẫn, ngắn. Ở 4 khoảnh khắc lớn (A6, C11, C17, G3), chân dung tướng đồng hành ló ra nói; lời nói đặt trong ngoặc kép.

### Chặng A: Mở game (0:00–1:30)

| # | Màn | Khi | Làm nổi | Lời | Người chơi | Kiểu |
|---|---|---|---|---|---|---|
| A1 | Màn tải | mở lần đầu | — | Mẹo cố định: "Thắng ải lấy bi, thả bi vào máy để mạnh lên." | chờ | — |
| A2 | Sảnh | tàu cập bến dưới | trang giấy giữa màn | **Sổ Tay Phiêu Lưu**. "Năm hòn đảo, năm hệ. Chọn một người bạn để lên đường." | Bắt đầu! | Ép |
| A3 | Hộp chọn tướng | sau A2 | 5 tướng đứng động | "Chọn bạn đồng hành." | chạm một tướng | Ép |
| A4 | Hộp chọn tướng | chạm tướng | tướng lớn diễn đòn đánh | tên, hệ, một chữ vai | Chọn, hoặc xem con khác | — |
| A5 | Hộp xác nhận | Chọn | — | "Đi cùng {tuong} nhé? Bạn sẽ gặp lại 4 bạn kia trên các đảo." | Đi thôi! | Ép |
| A6 | Sảnh | sau A5 | mây tan đảo {he}, camera lướt tới | "Đảo {he} là nhà mình. Đi nào!" | — | — |
| A7 | Sảnh | sau A6 | khoanh đảo {he} | "Chạm đảo để vào." | chạm đảo | Ép |
| A8 | Đảo | vào đảo | khoanh bệ ải 1 | "Ải 1. Chạm để xem đối thủ." | chạm | Ép |
| A9 | Hộp Chuẩn bị | mở | khoanh "Xuất trận" | "Mặt nước in bóng {tuong}. Đánh bại bóng của chính mình!" | Xuất trận | Ép |

Ghi chú:
- A2 thay hộp `GioiThieu` 4 khung (V1).
- A3–A4: mỗi ô tướng chỉ còn hình động, tên, icon hệ và một chữ vai. Bỏ dòng "Khắc / Bị khắc" và 3 thẻ (V2); những thứ này xem ở hộp chi tiết tướng, khi người chơi đã biết thẻ là gì. Vai đề xuất, dựa theo thẻ hiện có:

  | Tướng | Hệ | Vai | Lý do (thẻ) |
  |---|---|---|---|
  | Tí Tách | Thủy | Bền bỉ | Súng Nước giảm Công địch; Mưa Rào hồi 15% máu; nội tại hồi 5% mỗi lượt |
  | Tiểu Quỷ Lava | Hỏa | Thiêu đốt | chiêu, tuyệt kỹ, nội tại đều đốt |
  | Thiết Tinh | Kim | Phá giáp | Mưa Tinh Thể giảm Thủ địch; Thiết Tinh Dập 30% choáng |
  | Cầu Gai | Mộc | Hồi phục | Gồng Gai hồi máu; Lăn Gai hồi theo lượt |
  | Thạch Giáp | Thổ | Phòng thủ | Văng Sỏi tạo khiên; nội tại Mai Đá giảm sát thương |

- A9: hộp Chuẩn bị lần đầu ẩn hai ô đội khoá (cấp 60 còn quá xa) và dòng so lực chiến. Chỉ còn đối thủ, thưởng và Xuất trận.
- Mục tiêu thời gian: mở game tới A9 trong 90 giây (màn tải 2,4 giây, A2–A9 khoảng 7 chạm).

### Chặng B: Trận 1, trận gương (1:30–4:00)

Học: chọn thẻ, hàng thẻ, lượt địch, Chiêu. Tuyệt kỹ để sang trận 2.

| # | Khi | Làm nổi | Lời | Người chơi | Kiểu |
|---|---|---|---|---|---|
| B1 | màn VS xong, lượt 1 của mình | 3 thẻ | "Lượt của bạn! Chọn 1 trong 3 thẻ." | chọn một thẻ bất kỳ | Ép |
| B2 | thẻ bay vào hàng | hàng thẻ, chữ 1/5 | "Thẻ xếp vào hàng. Mỗi lượt chọn 5 lần." | chọn tiếp | Chú thích |
| B3 | chọn đủ 5 | hàng thẻ | "Hàng thẻ chạy lần lượt, rồi {tuong} đánh thường." | xem | Chú thích |
| B4 | tới lượt địch | băng chữ giữa sân | "Lượt địch" | xem | — |
| B5 | lượt 2, đủ mana cho Chiêu | nút Chiêu, thanh mana | "Đủ mana! Chiêu ra đòn ngay, không tốn lần chọn." | chạm Chiêu | Ép |
| B6 | Chiêu xong | 3 thẻ | "Chọn tiếp nhé." | chọn tiếp | Chú thích |
| B7 | thắng | con dấu "Thắng!" | — | — | — |
| B8 | hộp kết quả | ô bi | "Bi! Thả bi vào Máy Bi để lên cấp." | chạm "Máy bi (13)" | Ép |

Bảo đảm (chỉ ở trận này, khi cờ hướng dẫn chưa xong):
- Lần rút đầu tiên có sẵn: Ném Đá, Mài Vuốt, Băng Gạc (đánh, tăng Công, hồi máu: ba kiểu dễ hiểu nhất). Các lần sau rút trong bộ thẻ dễ (câu 3).
- Khoá thua ngầm: máu tướng mình không xuống dưới 20%. Bóng đã yếu 20% và máy chọn kém, nên thường không cần tới.
- Ẩn "Tự chơi". Nút Tuyệt kỹ chưa hiện cho tới khi nộ đầy. Nếu nộ đầy ngay trong trận 1 thì chạy C15 tại đây.
- B8: hộp kết quả lần đầu làm mờ "Ải tiếp", "Đánh lại" và tên đảo, chỉ chừa "Máy bi".
- Mảnh của tướng mình (2–4) và 1 đá tiến hóa vẫn hiện trong hộp kết quả nhưng không khoanh; để tới chặng F.
- Không cần viết sẵn mana: Chiêu của cả 5 tướng tốn 25–30, mỗi lượt +20 mana, nên lượt 2 luôn đủ (40).

### Chặng C: Vòng lõi đầu (4:00–9:00)

| # | Màn | Khi | Làm nổi | Lời | Người chơi | Kiểu |
|---|---|---|---|---|---|---|
| C1 | Máy bi | vào lần đầu | nút PUSH | "Chạm để thả một bi." | chạm | Ép |
| C2 | Máy bi | bi rơi ô EXP | thanh EXP, vòng cấp | "Kinh nghiệm! Cấp của bạn là cấp của mọi tướng." | xem | Chú thích |
| C3 | Máy bi | sau C2 | nút PUSH | "Giữ nút để thả liền." | giữ hoặc chạm | Gợi ý |
| C4 | Hộp Lên cấp | đủ 45 EXP (bi thứ 5) | con dấu "Cấp 2" | "Mọi tướng mạnh hơn. Thẻ mới vào bộ: {thẻ}." | Tiếp | Ép |
| C5 | Máy bi | bi rơi cốc thẻ (viết sẵn), rương bay vào khay | rương trong khay (đang lắc nhắc mở) | "Rương! Chạm để mở." | chạm, mở | Ép |
| C6 | Mở rương | rương bật | 2 bản sao thẻ Chiêu | "Đủ 2 bản sao: nâng cấp được Chiêu." | Nhận | Ép |
| C7 | Máy bi | hết đợt thả sau khi mở rương đầu (không ép thả hết bi, người dùng 2026-11-23) | nút quay lại | "Về sảnh nâng Chiêu cho {tuong}. Bi còn lại thả lúc nào cũng được." | quay lại hoặc thả tiếp | Gợi ý |
| C8 | Sảnh | về sảnh | nút Tướng (hiện lần đầu, có số 1) | "Nâng cấp Chiêu cho {tuong}." | chạm Tướng | Ép |
| C9 | Màn Tướng | vào | thẻ tướng đồng hành | — | chạm | Ép |
| C10 | Chi tiết tướng | mở | thẻ Chiêu, nút "Lên cấp 2" | "Chiêu cấp 2: mạnh thêm 15%." | Lên cấp | Ép |
| C11 | Sảnh | quay lại sảnh | mây tan 4 đảo (hoạt cảnh có sẵn) | "Bốn đảo nữa! Mỗi đảo có một bạn đang chờ." | — | — |
| C12a | Sảnh | sau C11 (2026-11-27) | hộp Tương khắc dạng bài học: vòng 5 hệ vẽ dần từ hệ {he}, hai dòng KHẮC / BỊ KHẮC | "Trước mỗi trận, xem hệ địch và mang tướng khắc nó!" | Hiểu rồi! | Ép |
| C12 | Sảnh | sau C12a | khoanh đảo {he2} | "Đảo {he2}: {he} khắc {he2}, đòn của bạn ×1,5." | chạm đảo | Ép |
| C13 | Hộp Chuẩn bị, ải 1 đảo {he2} | mở | mũi tên khắc hệ cạnh đối thủ | "Mũi tên xanh: bạn khắc địch." | Xuất trận | Ép |
| C14 | Trận 2 | đòn đầu trúng | số sát thương kèm dấu "KHẮC!" | "Khắc hệ: ×1,5!" | — | Chú thích |
| C15 | Trận 2 | lần đầu đủ nộ và mana | nút Tuyệt kỹ, thanh nộ | "Nộ đầy! Tuyệt kỹ thay cú đánh thường cuối lượt." | chạm | Ép |
| C16 | Kết quả trận 2 | thắng | ô mảnh {tuong2} (vd. 3/15) | "Gom đủ 15 mảnh để thu phục {tuong2}." | — | Chú thích |
| C18 | Sảnh | về sảnh sau trận 2 | nút Sổ thẻ (hiện ra lúc này) | "Sổ thẻ: mọi thẻ của mọi tướng. Chạm để xem." | chạm (cờ đánh ở `CardsScene.Enter`) | Ép |
| C19 | Sổ thẻ | vào được 2,5 giây, không mở hộp thẻ | nút quay lại | "Xem xong thì về sảnh." | — | Gợi ý 8 giây |
| C20 | Sảnh | sau C18 | giữa màn, chân dung tướng đồng hành | "**Nhà đã mở!** Tướng làm việc ở Nhà ra bi và gỗ, cả khi bạn vắng." | chạm | Lời |
| C21 | Sảnh | sau C20 | nút Nhà ở hàng đáy (người dùng 2026-11-27: không khoanh con tàu) | "Chạm nút Nhà để về Nhà." Về sảnh giữa chừng: "Về Nhà đặt Cây bi nhé." | chạm (cờ đánh ở `HomeScene.Enter`) | Ép |
| C22 | Nhà | tàu cập bến, chế độ thường | Nhà chính, khoanh sáng | "Đây là Nhà của bạn. Tướng làm việc ở đây, cả khi bạn vắng." | chạm đâu cũng qua | Lời có khoanh |
| C23 | Nhà | sau C22 | Ruộng rau (không có thì Vườn cây) | "Ruộng và vườn: tướng làm ở đây ra bi." | chạm | Lời có khoanh |
| C24 | Nhà | sau C23 | Xưởng gỗ (không có thì Kho) | "Xưởng gỗ ra gỗ, Kho giữ gỗ. Gỗ dùng để xây và nâng cấp." | chạm | Lời có khoanh |
| G3a–G3d | Nhà | sau C24 | Xây → Cây bi → Đặt → chạm cây | như chặng G | — | Ép |
| C25 | Nhà | sau G3d | nút về sảnh (tàu) | "Về sảnh xem có gì mới!" | — | Gợi ý 10 giây |
| C26 | Sảnh | đã đi hết Nhà | nút Cửa hàng (hiện ra lúc này), khoanh sáng | "**Cửa hàng đã mở!** Quà miễn phí mỗi ngày, bi và rương." | chạm đâu cũng qua | Lời có khoanh |
| C17 | Sảnh | sau C26 | giữa màn | "Giờ bạn tự đi nhé. Quên luật thì mở Sổ tay, mục Cách chơi." | chạm | Lời |

Bảo đảm:
- **13 bi đầu** (10 bi có sẵn và 3 bi của ải 1) có kết quả viết sẵn: EXP 10, EXP 10, EXP 5, EXP 10, EXP 10 (lên cấp 2 ở bi thứ 5), rồi cốc thẻ (rương bạc). Các bi sau theo bảng tỉ lệ thường. Đường bi vẫn là vật lý thật, vì `Board.odds` vốn đã chọn ô trước rồi mới phát đường bi.
- **Rương đầu:** rương bạc có đúng 2 bản sao thẻ Chiêu của tướng đồng hành (thẻ cấp 2 cần 2 bản sao, `cardReq`).
- **C4:** hộp chỉ có thẻ mới để khoe nếu cấp 2 có thẻ mở (câu 3). Không đổi bộ thẻ thì dòng "Thẻ mới" ẩn, chỉ còn "Mọi tướng mạnh hơn".
- **C8:** nút Tướng ẩn tới bước này (mục 5).
- **C9–C10:** hộp chi tiết tướng lần đầu làm mờ mọi thứ trừ thẻ Chiêu và nút lên cấp. Nút Tiềm năng và Tiến hóa ẩn tới khi tới lượt (chặng H).
- **C11:** giữ hoạt cảnh mây tan 4 đảo (hiện chạy ngay khi vào sảnh sau trận thắng đầu) tới sau C10, để mỗi lần vào sảnh chỉ có một việc.
- **C12:** khoanh đảo của hệ mà tướng mình khắc (Thủy → Hỏa, Hỏa → Kim, Kim → Mộc, Mộc → Thổ, Thổ → Thủy), thay mũi tên đảo gợi ý ở bước này. Ải 1 các đảo đều cấp 1 nên trận này dễ.
- **C15:** trận 2 rút sẵn Gầm Gừ (+15 nộ) ở lượt 2 và lượt 3 để nộ đầy trong trận. Chưa đầy thì C15 chạy ở trận sau. Đã học Tuyệt kỹ ở trận 1 thì bỏ bước này.
- Trận 2 cũng khoá thua ngầm như trận 1.
- Sau C17, chuỗi bắt buộc xong (cờ `ftue.core`). "Tự chơi" hiện từ trận 3.
- **Sau trận 2 (người dùng 2026-11-24):** Sổ thẻ mở ngay, chỉ bắt chạm vào; rồi giới thiệu Nhà và các thứ trong Nhà qua loa (Nhà chính, ruộng vườn, xưởng gỗ, kho, Cây bi), rồi mới mở Cửa hàng. Lời chào C17 dời xuống cuối.
  - Nhà mở sau ải thứ 2 (`Home.OpenStages`), bỏ điều kiện 3 tướng của trang trại cũ; nút Nhà ở sảnh hiện từ C20.
  - "Lời có khoanh" (`Guide.SayAt`): nền tối quanh chỗ khoanh, vòng mực; chạm đâu cũng qua, chạm trúng chỗ khoanh không bấm xuống công trình hay nút (vòng khoanh chặn chạm ở chế độ này).
  - Đặt Cây bi (G3a–G3d) thuộc chuỗi bắt buộc, không tắt bằng công tắc "Gợi ý" (`Tutorial.IsCore` gồm mã `g3*`). Cây đã hái hết trước khi kịp dẫn thì coi G3d là xong.
  - Khoảnh khắc "Nhà đã mở" cũ sau chuỗi (`g1`, `g2`) bị bỏ qua khi C20 chạy.
  - Code: `HubScene.TutorStep`, `CardsScene.Enter`, `HomeScene.Tutor` (`Intro`), `Tutorial.Shows` (Sổ thẻ sau trận 2, Nhà từ C20, Cửa hàng khi `HomeToured`).

### Chặng D: Trong trận và trên đảo, theo lúc (phiên 1 trở đi)

Mỗi dòng chạy đúng một lần, khi điều kiện xảy ra lần đầu.

| # | Khi lần đầu | Chỗ | Lời | Kiểu |
|---|---|---|---|---|
| D1 | mở hộp Chuẩn bị ải có từ 2 địch | dòng đối thủ | "Đối thủ có 2 con, ra sân từng con. Hạ hết mới thắng." | Chú thích |
| D2 | một hiệu ứng mới hiện trên tướng (bỏng, độc, choáng, hồi phục, khiên, né) | icon hiệu ứng | ví dụ "Bỏng: mất máu đầu mỗi lượt." Chạm icon nào cũng xem được | Chú thích |
| D3 | tướng mình bị choáng | thanh chọn thẻ | "Bị choáng: mất trọn lượt này." | Chú thích |
| D4 | mở hộp Chuẩn bị ải có địch tiến hóa (ải 5) | đầu mục đối thủ | "Còn 25% máu thì tiến hóa, hồi đầy máu." | Chú thích |
| D5 | địch tiến hóa trong trận | sân | "Tiến hóa! Dạng cuối thì không hồi nữa." | Chú thích |
| D6 | bắt đầu trận thứ 3 | nút Tự chơi (hiện lần đầu) | "Tự chơi: máy đánh thay bạn, tắt lúc nào cũng được." | Gợi ý |
| D7 | thẻ Hiếm trở lên hiện lần đầu | thẻ đó | "Thẻ viền tím: hiếm hơn, mạnh hơn." | Chú thích |
| D8 | tới ải 10 một đảo | rương trên thanh tiến độ đảo | "Mỗi 10 ải có một rương mốc." | Gợi ý |
| D9 | ~~lên cấp có thẻ mới~~ | — | bỏ 2026-11-23: không bắt xem sổ thẻ; nút Sổ thẻ tự hiện từ cấp 3, không khoanh | — |
| D10 | địch có bị động riêng (mốc 30–70) | dòng ghi chú đối thủ | tên bị động; chạm để xem | Chú thích |
| D11 | vào màn Tướng sau chuỗi bắt buộc (2026-11-27) | nút vòng 5 chấm trên thẻ tướng đồng hành | "Chạm vòng 5 chấm: xem tướng này khắc hệ nào, sợ hệ nào." | Gợi ý 7 giây |
| D12 | mở hộp Chuẩn bị, đội có tướng bị tướng chính của địch khắc (trừ tướng đồng hành) | ô đội của tướng đó | "{tuong} bị hệ {x} khắc: đánh ×0,75, chịu đòn ×1,5. Chạm ô để đổi sang tướng hệ {y}." | Gợi ý 8 giây |
| D13 | mở hộp chọn đội sau chuỗi bắt buộc | nút vòng 5 chấm ở ô đầu | "Chạm vòng 5 chấm để xem tướng khắc hệ nào, sợ hệ nào." | Gợi ý 6 giây |

### Chặng E: Bức tường cấp và lần thua đầu

Đây là chỗ người mới dễ bỏ nhất. Ải 2 cấp 6, ải 3 cấp 11, ải 5 cấp 18, trong khi chuỗi bắt buộc xong ở khoảng cấp 2–3.

| # | Khi lần đầu | Chỗ | Lời | Kiểu |
|---|---|---|---|---|
| E1 | mở hộp Chuẩn bị ải có địch hơn mình từ 3 cấp | dòng cảnh báo (đã có), thêm 3 nút nhỏ | "Địch cấp {x}, bạn cấp {y}. Lên cấp ở Máy Bi, hoặc đánh ải dễ ở đảo khác." Nút: Máy Bi, Đảo dễ nhất, Tướng | Gợi ý |
| E2 | thua lần đầu | hộp thua | con dấu "Thua rồi", rồi "Thua không mất gì. Mạnh hơn bằng:" và 3 nút lớn: Máy Bi (n), Tướng, Ải dễ hơn | — |
| ~~E3~~ | bỏ 2026-11-23: cây bi dời vào Nhà, hướng dẫn hái chuyển thành G3d | — | — | — |
| E4 | sau lần hái đầu | — | "Hết bi thì sang đảo khác, hoặc lát nữa quay lại hái." | Chú thích |

- E1: "Đảo dễ nhất" là đảo có ải kế cấp thấp nhất (`RecommendedZone`). Trong phiên đầu, đó thường là ải 1 của một đảo chưa đánh (cấp 1): vừa có bi, vừa có mảnh một tướng khởi đầu khác.
- E2 thay dòng mẹo của hộp thua (V8).
- Cây bi lần đầu có sẵn 10 bi để lần hái đầu đã tay (câu 8). Từ 2026-11-23 cây mở cùng Nhà, nên bơm 10 bi lúc vào Nhà (G3d).

### Chặng F: Phiên 2 (quay lại) và ngày 1–2

| # | Khi lần đầu | Chỗ | Lời | Kiểu |
|---|---|---|---|---|
| F1 | vào sảnh khi AFK đã có mảnh hoặc rương | nút AFK (hiện từ đây) | "Lúc bạn vắng, {tuong} vẫn đánh ải {n}: ra mảnh và rương." | Gợi ý |
| F2 | mở hộp AFK lần đầu | rương AFK | "Rương AFK đếm đủ giờ thì mở được." | Chú thích |
| F3 | mở hộp Chuẩn bị của một ải đã qua có rơi mảnh, khác ải đang AFK | nút "AFK ải này" | "Cho AFK ở ải rơi mảnh tướng bạn muốn." | Gợi ý |
| F4 | vào máy bi lần 2 | thanh mốc Huyền thoại | "Thả đủ 300 bi: nhận Thổ Tinh, tướng Huyền thoại!" | Gợi ý |
| F5 | vòng nấm lần đầu quá 12/25 | vòng nấm | "Bi chạm nấm 25 lần: nấm trái ra rương bạc, nấm phải ra 5 bi." | Chú thích |
| F6 | vào máy bi khi có từ 40 bi | viên cược | "Cược ×2: tốn 2 bi mỗi lần, thưởng ×2. Nhanh hơn, không lời hơn." | Gợi ý |
| F7 | lần đầu có 150 bi (mở ×3) | viên cược | toast có sẵn "Mở cược ×3", nút nhún | — |
| F8 | có 2 tướng; ải kế có địch mà tướng thứ hai khắc, còn tướng trong đội không khắc | hộp Chuẩn bị, ô đội | "Địch hệ {x}. {tuong2} hệ {y} khắc {x}, nên cho vào đội: chạm ô đội nếu muốn đổi." Khoanh ô đội, không ép (người dùng 2026-11-27: chỉ gợi ý, không bắt đổi) | Gợi ý (một lần, 8 giây) |
| F9 | lần đầu thu phục tướng bằng mảnh | hộp "Thu phục!" | tướng mới chào; "Cho vào đội ở hộp Chuẩn bị hoặc màn Tướng." | — |
| F10 | lần đầu đủ mảnh lên sao | chấm đỏ ở Tướng, rồi nút Lên sao | "Mảnh dư dùng để lên sao: mạnh thêm." | Gợi ý |
| F11 | qua mốc Huyền thoại (thanh đổi sang mốc quà) | thanh mốc quà | "Từ giờ, cứ thả đủ bi là có quà." | Chú thích |

- **F8** thường chạy ở ải 4 đảo Thủy, ngay sau quà Tê Thiềm ở ải 3 (Thổ, khắc Thủy).
  - Người chọn Thạch Giáp nhận Thiết Cưa (Kim, trung tính), trong khi tướng đồng hành của họ đã khắc Thủy, nên với họ F8 chạy muộn hơn, ở đảo khác.
  - Trước cấp 60, đây là cách duy nhất người chơi học "đội 1 ô: chọn tướng theo hệ địch", nên ép một lần.
- **F9:** cần kiểm game đã có hộp thu phục chưa. Chưa có thì làm, dùng lại hộp nhận tướng của mốc Huyền thoại.

### Chặng G: Nhà (từ 2026-11-24 mở sau ải thứ 2, phần đầu nằm trong chuỗi bắt buộc C20–C25)

| # | Khi | Chỗ | Lời | Kiểu |
|---|---|---|---|---|
| ~~G1~~ | dời thành C20 (2026-11-24) | — | — | — |
| ~~G2~~ | dời thành C21 | — | — | — |
| G3 | tàu cập bến Nhà lần đầu | camera lướt tới Nhà chính (có sẵn, cờ `dockIntro`), rồi C22–C24 | — | — |
| G3a | có cây bi chờ đặt, chế độ thường | nút Xây | "Cây bi đã về Nhà! Bấm Xây để đặt cây." | Ép, lặp tới khi đặt xong |
| G3b | đang xây, chưa chọn gì | thẻ Cây bi đầu khay ("Miễn phí") | "Chọn Cây bi. Đặt cây không tốn gì." | Ép, lặp |
| G3c | bóng ma Cây bi | bóng ma (nút Đặt cạnh nó) | "Kéo cây tới chỗ bạn thích, rồi bấm Đặt." | Gợi ý 30 giây, lặp |
| G3d | đặt xong (tự về chế độ thường), cây có bi | Cây bi | "Chạm cây để hái bi. Mỗi cây ra {n} bi mỗi giờ, chứa được {cap}." (số lấy từ balance.json) | Ép |
| G4 | sau G3 | Ruộng rau, ô thẻ tướng | "Giao một tướng làm Ruộng rau: ra bi." | Ép |
| G5 | sau G4 | Xưởng gỗ | "Xưởng gỗ ra gỗ để xây và nâng cấp." | Gợi ý |
| G6 | lần đầu có đồ chờ thu | bong bóng trên công trình | "Chạm bong bóng để thu." | Gợi ý |
| G7 | lần đầu đủ điều kiện nâng Nhà chính (cấp 10, 60 gỗ) | Nhà chính | "Nâng Nhà chính: mở thêm công trình và đất." | Gợi ý |
| G8 | lần đầu có ô rừng dọn được | biển "Dọn được" | "Dọn rừng để có thêm đất." | Gợi ý |
| G9 | lần đầu vào chế độ xây | khay công trình | "Giữ để nhấc, kéo để dời." | Chú thích |
| G10 | lần đầu tàu về sảnh | con tàu | "Chạm tàu để ra đảo đánh tiếp." | Gợi ý |

Trang trí, điểm đẹp, ô lát: không gợi ý, để người chơi tự khám; có ghi trong trang "Nhà" của Cách chơi.

Cây bi trong Nhà (người dùng 2026-11-23: gộp thẻ Cây bi của sảnh với cây bi ở Nhà làm một, thêm hướng dẫn đặt cây):
- Cây bi mở cùng Nhà (`Trees.Open` cần `Home.Open`); thẻ Cây bi ở cột sảnh bỏ.
- Cây đã mở mà chưa có chỗ nằm đầu khay Xây, đặt miễn phí, xong ngay (`Home.TreesWaiting`). Có cây chờ đặt thì nút Nhà ở sảnh hiện "!".
- Bản lưu cũ (đã có cây ở sảnh) mở Nhà lần đầu thì cây được đặt sẵn như trước; người chơi mới tự đặt theo G3a–G3d.
- Cây 2–5 (cấp 30, 50, 80, 110) không tự đặt, không dẫn: báo "Thêm một cây bi!" ở sảnh kèm "Về Nhà, bấm Xây để đặt cây mới."
- G3a–G3c lặp: bấm Thôi hay Xong giữa chừng thì lần sau dẫn lại; xong hẳn khi đã đặt cây (cờ `g3t`). G3d cờ `g3h`. Từ 2026-11-24 thuộc chuỗi bắt buộc, không tắt bằng công tắc "Gợi ý".
- Chạm cây trúng cả tán lá, không chỉ ô dưới chân (`HomeScene.HitAt`).
- Code: `HomeScene.Tutor`, `TreeTrayItem`, `HitAt`.
- Thử: menu `PokiClash/Thử/Nhà và side meta/Nhà: hướng dẫn đặt Cây bi, chạm tán lá (đang Play)` (`Editor/HomeTreeTour.cs`). Tour giả người chơi mới vừa mở Nhà, đi G3a → G3d, chụp `Temp/PokiShots/30x_cay_*.png`, chạm một điểm trên tán lá ngoài các ô dưới chân và kiểm số bi tăng, xong trả lại bản lưu.

### Chặng H: Mở dần (ngày 3 trở đi)

Mỗi dòng là một khoảnh khắc mở: hộp nhỏ, hình công trình hay nút, một câu, nút "Đi xem". Nhiều dòng tới cùng lúc thì xếp hàng, mỗi lần vào sảnh mở một.

| Mục | Điều kiện (theo code hiện tại) | Lời | Sau đó |
|---|---|---|---|
| Đá tiềm năng | lần đầu có ít nhất 1 đá | "Đá tiềm năng: mở thêm dòng chỉ số cho tướng." | nút Tiềm năng hiện trong chi tiết tướng, khoanh |
| Đá tiến hóa | lần đầu có đá (ải tướng lần đầu cho 1 đá) | không báo, chỉ hiện số đá trên thanh tiến hóa | — |
| Hang Tiềm Năng | cấp 30 | "Hang Tiềm Năng: đánh boss lấy đá tiềm năng, 3 lượt mỗi ngày." | khoanh Hang trên sảnh |
| Cây bi 2 | cấp 30 | "Thêm một cây bi!" | — |
| Tiến hóa Bạc | cấp 30, sao cuối bậc Đồng, 20 đá | "{tuong} tiến hóa được rồi! Đổi dạng, mạnh hơn hẳn." | khoanh nút Tiến hóa trên thanh tiến hóa |
| Cây bi 3–5 | cấp 50, 80, 110 | "Thêm một cây bi!" | — |
| Đền Huy Hiệu | thắng ải 20 (mini boss đầu) ở một đảo | "Đền Huy Hiệu: thắng chuỗi trận boss, cả hệ mạnh thêm." | khoanh Đền |
| Ô đội 2 | cấp 60 | "Ô đội thứ 2! Mang 2 tướng, đổi được giữa trận." | trận kế, ép một lần ở đầu lượt: "Chạm chân dung để đổi tướng, trước lần chọn đầu. Tướng dự bị +10 mana mỗi lượt." |
| 30 bi mỗi lần thả | cấp 104 | toast | — |
| Ô đội 3 | cấp 200 | "Ô đội thứ 3!" | — |

- Hiện cấp 30 mở 3 thứ cùng lúc (Hang, cây bi 2, tiến hóa). Hàng chờ tách chúng ra ba lần vào sảnh; cách dời số ở câu 7.
- Công trình khoá trên sảnh (Nhà, Đền, Hang) chỉ hiện bản phác khi điều kiện mở đã gần (mục 5).

## 5. Sảnh hiện dần

| Chỗ | Lúc đầu | Hiện khi |
|---|---|---|
| Vòng cấp, chip bi | hiện | — |
| Sổ tay (nút bánh răng trên thanh trên) | hiện | — (có cài đặt) |
| Máy Bi (nút đáy) | ẩn | B8 (nhún, hiện ra) |
| Tướng (nút đáy) | ẩn | C7 (mở xong rương đầu) |
| Cửa hàng (nút đáy, 2026-11-23 thay Đánh tiếp) | ẩn | đi hết Nhà, C26 (2026-11-24) |
| Sổ thẻ (nút đáy) | ẩn | về sảnh sau trận 2, C18 (2026-11-24) |
| Nút AFK (thanh trên) | ẩn | F1 |
| Cây bi | bỏ khỏi sảnh 2026-11-23 | đến cùng Nhà, đặt ở Nhà (G3a–G3d) |
| Nhà (nút đáy từ 2026-11-23; hướng dẫn khoanh nút này, không khoanh tàu) | ẩn | C20 (Nhà mở sau ải thứ 2, 2026-11-24) |
| Hang | ẩn | cấp 20: bản phác "Cấp 30"; cấp 30: mở |
| Đền | ẩn | qua ải 10 một đảo: bản phác "Thắng ải 20"; thắng ải 20: mở |
| Mây che đảo | đã đúng | — |

- Ẩn hẳn thay vì để mờ, để ở phút đầu người chơi chỉ thấy một thứ cần chạm.
- Bản lưu cũ (đã có `starter` và đã đánh) coi các mốc là đã qua theo trạng thái (mục 7).
- Tàu ở bến: chạm tàu cũng về Nhà (lối phụ, hướng dẫn và mẹo lúc tải chỉ nói nút Nhà). Trước khi Nhà mở (chưa qua 2 ải), chạm tàu chỉ ra toast "Qua 2 ải để mở Nhà".

## 6. Trang "Cách chơi" trong Sổ tay

Thêm mục "Cách chơi" vào Sổ tay.
- Mỗi trang có một hình (ảnh chụp có khoanh bút chì) và tối đa 3 dòng.
- Trang mở khi bước tương ứng đã chạy; trang chưa mở hiện "???".
- Mẹo ở màn tải chỉ lấy câu của những trang đã mở.

| Trang | Mở sau | Nội dung |
|---|---|---|
| Vòng chơi | B8 | Thắng ải → bi. Thả bi vào Máy Bi → kinh nghiệm, rương. Lên cấp, nâng tướng → đánh ải khó hơn. |
| Lượt đánh | B3 | Mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ. Thẻ xếp hàng, chạy lần lượt cuối lượt, rồi tướng đánh thường. Bạn luôn đi trước. |
| Chiêu và Tuyệt kỹ | C15 | Mana +20 mỗi lượt. Chiêu tốn mana, ra đòn ngay, mỗi lượt một lần. Nộ tăng khi đánh và khi bị đánh; đầy 100 nộ (và đủ mana) thì Tuyệt kỹ thay cú đánh thường. |
| Khắc hệ | C14 | Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy. Khắc địch: đánh ×1,5, chịu đòn ×0,75. Bị khắc: đánh ×0,75, chịu đòn ×1,5. Trước mỗi trận xem hệ địch, mang tướng khắc nó. Chạm vòng 5 chấm ở ô tướng để xem. Tướng đồng hành không bao giờ chịu thiệt vì hệ. (sửa 2026-11-27) |
| Hiệu ứng | D2 | Bỏng, độc: mất máu đầu lượt. Hồi phục: hồi máu đầu lượt. Choáng: mất trọn lượt. Né: tránh cú đánh thường kế tiếp. Khiên: đỡ trước khi trừ máu. |
| Máy Bi | C3 | Chạm để thả, giữ để thả liền. Ô ra kinh nghiệm, cốc ra rương. Bi chạm nấm đủ 25 lần ra quà. Bảng tỉ lệ ở nút Tỉ lệ. |
| Cược | F6 | ×N tốn N bi mỗi lần thả, mọi thưởng ×N. Mở theo số bi đang có. Chỉ nhanh hơn, không lời hơn. |
| Rương | C6 | Rương gỗ, bạc, vàng: bi, kinh nghiệm, bản sao thẻ, mảnh tướng, đá. |
| Cấp | C4 | Cấp của bạn là cấp của mọi tướng. Kinh nghiệm chỉ đến từ Máy Bi và rương. Lên cấp mở thêm thẻ vào bộ. |
| Đảo và ải | C11 | 5 đảo chơi song song, mỗi đảo 70 ải. Cấp địch là cấp nên có. Ải tướng chắc chắn rơi mảnh; mỗi 10 ải có một rương mốc. |
| Tướng | F10 | Mảnh: thu phục, rồi lên sao. Bản sao thẻ: nâng chiêu, tuyệt kỹ, nội tại. Đá tiến hóa và cấp: tiến hóa, đổi dạng. |
| Đội hình | F8 | Đội 1 ô; cấp 60 thêm ô 2, cấp 200 thêm ô 3. Chọn tướng khắc hệ địch. Có từ 2 ô thì đổi tướng được ở đầu lượt. |
| AFK | F1 | Ải đã qua tự đánh lúc bạn vắng, tối đa 12 giờ: ra mảnh và rương. Chọn ải AFK ở hộp Chuẩn bị. |
| Cây bi | G3a–G3c (đặt xong cây đầu) | Cây bi ở Nhà: mỗi cây 5 bi mỗi giờ, chứa 50, chạm cây để hái. Thêm cây ở cấp 30, 50, 80, 110: đặt bằng nút Xây. |
| Nhà | G4 | Tướng làm việc ra bi, gỗ, quặng. Gỗ và quặng dùng để xây, nâng cấp, dọn rừng. |
| Tiềm năng | H | Đá tiềm năng mở thêm dòng chỉ số. Hang Tiềm Năng ra đá. |
| Đền Huy Hiệu | H | Thắng chuỗi trận boss theo hệ: tướng cùng hệ mạnh thêm. |

## 7. Làm thế nào (kỹ thuật)

- **Core** `Core/Tutorial.cs` (logic thuần, có test):
  - danh sách bước: mã, điều kiện chạy, điều kiện xong, ép hay gợi ý;
  - cờ các bước đã xong lưu ở `SaveData.extra["ftue"]` (danh sách mã), không đổi phiên bản bản lưu;
  - hàm `Pending(save, scene, event)` trả bước cần chạy.
- **Bản lưu cũ:** lúc nạp, bước nào mà trạng thái đã vượt qua (đã có `starter`, `stats.battles > 0`, đã có tướng thứ 3…) thì đánh dấu xong, không chạy lại.
- **Lớp phủ** `Kit/HuongDan`: prefab đặt sẵn trong `App.prefab`, đúng luật "chỉ prefab". Gồm:
  - nền tối có lỗ khoét (material UI làm sẵn, lỗ theo khung chỗ cần chạm);
  - vòng khoanh và mũi tên bằng `InkPath`, bút chì làm con trỏ;
  - ghi chú giấy: mở rộng `UiHint` để không tự tắt ở bước ép;
  - chân dung tướng đồng hành cho 4 khoảnh khắc lớn.
  - Ở bước ép, chạm ngoài lỗ bị nuốt.
- **Mỏ neo:** component `TutorialAnchor` mang một khoá chuỗi, gắn vào chỗ cần khoanh (`hub.may_bi`, `battle.chieu`, `machine.push`…). Lớp phủ tìm chỗ theo khoá, không phụ thuộc đường dẫn GameObject.
- **Trận viết sẵn:**
  - thêm vào `Battle` một kịch bản tuỳ chọn (rút sẵn n lần đầu, khoá thua), chỉ bật khi chặng B, C đang chạy;
  - trận không có kịch bản chạy y như cũ, nên golden và test cân bằng không đổi;
  - `BattleController.Hint` cũ thay bằng bộ hướng dẫn.
- **Máy bi viết sẵn:** hàng kết quả ép cho n bi đầu đưa vào `Board.odds` (vốn đã chọn kết quả trước); rương đầu có nội dung ép.
- **Hộp lên cấp:** bỏ dòng ×N trống; thêm dòng "Mở khoá" theo bảng chặng H. Hàng chờ khoảnh khắc mở nằm ở `HubScene`.
- **Sửa chỗ cũ:** chữ hộp giới thiệu (hoặc thay hẳn bằng A2), chú thích ở `Progress.cs:464`, mẹo màn tải lọc theo trang Cách chơi đã mở.
- **Cài đặt:**
  - Sổ tay giữ công tắc "Gợi ý" (`settings.hints`) cho gợi ý mềm;
  - chuỗi bắt buộc A–C không tắt được ở lần chơi đầu;
  - bản dev có nút "Chạy lại hướng dẫn".
- **Đo:** mỗi bước ghi một dòng (mã bước, bắt đầu hay xong, số giây kể từ lúc mở game) vào `Logs/ftue.csv`, như `tran.csv`. Gắn SDK phân tích sau.
- **Chữ:** bọc `Loc.T` / `Loc.F` như mọi chữ khác (bản tiếng Anh, `24_DaNgonNgu.md`).
- **Thử:** menu `PokiClash/Thử/Hướng dẫn: người chơi mới từ đầu (đang Play)`: xoá bản lưu, đi trọn A–C bằng chạm giả, chụp từng bước.

## 8. Đo đạt hay chưa

| Chỉ số | Mục tiêu |
|---|---|
| Mở game tới vào trận 1 | tối đa 90 giây |
| Xong chuỗi bắt buộc (C17) | ít nhất 90% người mở game |
| Thời gian chuỗi bắt buộc | 6–10 phút |
| Thua trong 3 trận đầu sau chuỗi | tối đa 15% |
| Độ dài phiên đầu | ít nhất 10 phút |
| Quay lại sau 1 ngày (D1) | theo dõi, so trước và sau khi có FTUE |

Bước nào có tỉ lệ bỏ cao bất thường thì xem lại chữ và chỗ khoanh ở bước đó trước tiên.

## 9. Câu cần chốt

1. **Chọn tướng trước hay đánh trận mẫu trước?**
   - (a) Chọn tướng trước, hộp gọn như kịch bản trên. **Đề xuất**, vì:
     - 5 tướng đều Khá, chọn con nào cũng không thiệt (luật đồng hành);
     - trận 1 là trận gương của chính tướng vừa chọn.
   - (b) Đánh một trận mẫu bằng tướng mượn rồi mới chọn: biết luật trước khi chọn, nhưng thêm một trận và phải bỏ con tướng mượn.
2. **Ai dẫn?**
   - (a) Ghi chú bút chì là chính, tướng đồng hành ló ra ở 4 khoảnh khắc lớn (A6, C11, C17, G3). **Đề xuất**: hợp chất "sổ tay phiêu lưu", không phải vẽ thêm nhân vật.
   - (b) Chỉ ghi chú bút chì.
   - (c) Một nhân vật dẫn riêng: cần thiết kế, gen hình, làm animation.
3. **Bộ thẻ lúc đầu.** Hiện 22 thẻ mở ở cấp 1, còn cấp 2–6 gần như không có thẻ mới.
   - (a) Cấp 1 chỉ còn 6 thẻ dễ: Ném Đá, Cắn Xé, Mài Vuốt, Đứng Tấn, Băng Gạc, Hít Thở. Cấp 2–10, mỗi cấp mở 1–2 thẻ: Gầm Gừ, Thủ Thế, Phóng Lông, Hạt Dẻ, Nhảy Lùi, Bình Thuốc, Kim Độc, Tung Cát, Gai Nhọn, Liều Mạng, Vùng Dậy, Cuồng Nộ, Phá Giáp… **Đề xuất**, vì:
     - mỗi lần lên cấp đều có thẻ mới để khoe;
     - người mới không gặp thẻ khó ngay.
     - Cái giá: đổi `unlock` trong `cards.json` thì phải đo lại tỉ lệ thắng các ải đầu và tính lại golden.
   - (b) Giữ nguyên bộ thẻ, chỉ rút sẵn trong trận 1–2.
4. **Khoá thua ngầm ở trận 1–2** (máu không xuống dưới 20%): **đề xuất** có. Không khoá thì trận gương vẫn gần như chắc thắng, nhưng trận 2 gặp tướng thật.
5. **Viết sẵn 13 bi đầu và rương đầu** (rương bạc có 2 bản sao Chiêu): **đề xuất** có. Đường bi vẫn là vật lý thật, chỉ chọn trước ô rơi như mọi bi khác.
6. **Nút, công trình chưa tới lượt: ẩn hay để mờ?** **Đề xuất** ẩn (mục 5). Để mờ thì người mới vẫn thấy 10 thứ.
7. **Cấp 30 mở 3 thứ cùng lúc** (Hang, cây bi 2, tiến hóa Bạc).
   - (a) Giữ số, xếp hàng mỗi lần vào sảnh một khoảnh khắc. **Đề xuất**: không đổi cân bằng.
   - (b) Dời số: cây bi 2 về cấp 25, Hang về cấp 35. Phải đo lại nhịp (`ProgressSim`).
8. **Cây bi lần đầu có sẵn 10 bi** để lần hái đầu ở E3 đã tay: **đề xuất** có. Chỉ thêm 10 bi một lần, không đáng kể so với nhịp chung.
9. **Chuỗi nhiệm vụ người mới:** khoảng 15 mục tiêu cho ngày 1–3, có thưởng nhỏ (thu phục tướng thứ 2, qua ải 5 một đảo, thả 100 bi, nâng thẻ lần đầu, về Nhà…).
   - (a) Làm, sau khi chuỗi bắt buộc chạy ổn: cho người chơi một hướng đi khi gợi ý mềm đã hết. **Đề xuất**; nhưng thưởng bi làm nhịp nhanh hơn nên phải đo.
   - (b) Không làm; chỉ dựa vào mũi tên đảo gợi ý và chấm đỏ.

Ngoài FTUE, lúc quét gặp mấy chỗ cũ nên sửa dù chọn hướng nào:
- chữ hộp giới thiệu;
- chú thích ô đội ở `Progress.cs:464`;
- dòng ×N luôn trống ở hộp lên cấp;
- mẹo màn tải nói về Nhà và khắc hệ khi người mới chưa gặp.

## 10. Đã làm (2026-11-22)

Người dùng bảo "ok làm đi": làm theo đề xuất của câu 1–8; câu 9 (chuỗi nhiệm vụ) để sau khi chuỗi bắt buộc chạy ổn.

### Code

- **Core** `Core/Tutorial.cs`:
  - cờ từng bước ở `SaveData.extra["ftue"]`; bản lưu chưa có cờ mà đã qua ải hoặc đã đánh thì coi như xong hết (`"*"`);
  - `Tutorial.Off` cho tour thử; `BattleFor` (kịch bản trận 1, 2); `MachineOutcomes` (6 bi đầu); `FirstChest` (2 bản sao Chiêu);
  - `SeedTree` (cây bi đầu có sẵn 10 bi); `Shows` (sảnh hiện dần); `NextUnlock` (khoảnh khắc mở); `Pages` (trang Cách chơi).
  - Móc vào: `Battle.script` (rút sẵn thẻ, máu phe mình không dưới 20% ở 5 chỗ trừ máu); `Board.forced` (kết quả ép); `HubIslands.TutorialDone` (4 đảo tan mây sau bước nâng Chiêu); `SaveData.New` của game gọi `Tutorial.Begin`.
  - Trận không có kịch bản, bản lưu cũ chạy y như trước.
- **Lớp phủ:**
  - `App/GuideOverlay.cs` (prefab `Kit/HuongDan` trong `App.prefab`, canvas Screen Space - Overlay thứ tự 500, nằm trên cả màn mở rương thứ tự 400);
  - `App/Guide.cs` (đăng ký chỗ cần khoanh theo khoá, hàng chờ bước, nhật ký `Logs/ftue.csv`).
  - Chỗ cần khoanh bị hộp khác che thì chờ; sang scene khác thì bỏ bước của scene cũ; không thấy chỗ cần khoanh 12 giây thì bỏ, màn xin lại sau (sảnh tự xét lại mỗi 2,5 giây).
- **Các màn:**
  - `HubScene`: lời mở đầu thay hộp `GioiThieu`; luồng chọn bước theo trạng thái bản lưu (tắt game giữa chừng vẫn vào đúng bước); nút đáy, công trình hiện dần; khoảnh khắc mở tính năng.
  - `StarterDialog`: bản gọn (tên, hệ, vai, danh hiệu; bản đủ giữ ở `DescribeFull`).
  - `ZoneScene`, `StagePrepDialog`, `BattleController`, `BattleResultDialog`, `MachineScene`, `MachineChestOpen`, `HeroesScene`, `HeroDetailDialog`, `TopBars` (nút AFK ẩn tới F1).
  - `Dialogs.LevelUp`: dòng thứ hai ghi "Mọi tướng mạnh hơn x%" và tính năng vừa mở.
  - `ShipVoyage`: mẹo màn tải lọc theo trang đã mở.
- **Cách chơi:** `App/HowToDialog.cs`, prefab `Dialogs/CachChoi`, dòng "Cách chơi" ở Sổ tay (menu `PokiClash/Prefab/Hộp thoại và màn/Hướng dẫn: hộp Cách chơi, dòng Sổ tay`).
- **Dữ liệu (câu 3):**
  - `cards.json`: cấp 1 còn 6 thẻ (Ném Đá, Cắn Xé, Mài Vuốt, Đứng Tấn, Băng Gạc, Hít Thở);
  - 16 thẻ dời sang cấp 2–10: Gầm Gừ, Thủ Thế 2; Hạt Dẻ, Nhảy Lùi 3; Phóng Lông, Bình Thuốc, Giáp Gỗ 4; Kim Độc, Bánh Bao Thịt 5; Tung Cát, Tĩnh Tâm 6; Gai Nhọn, Vùng Dậy 8; Liều Mạng 9; Cuồng Nộ, Phá Giáp 10.
  - Golden tính lại: `battles`, `battle_events`, `sim` (menu "Tính lại golden sim…" rồi ghép), `potential`, `badges` (menu "theo tướng mẫu", "theo danh sách tướng").
- **Bản tiếng Anh:** 119 chuỗi mới nối vào `Resources/Loc/en/ui.json`.
- **Test:** `Tests/TutorialTests.cs` (10 test). Hai tour cũ có xoá bản lưu (`StarterTour`, `PlayTour.RunThuy`) bật `Tutorial.Off`.
- **Menu thử (đang Play):**
  - `PokiClash/Thử/Hướng dẫn: chơi lại từ đầu, xoá bản lưu` (chép bản lưu cũ ra `.bak_ftue` trước);
  - `…: bỏ qua hết`;
  - `…: người chơi mới, đi hết chuỗi và chụp` (ảnh ở `Temp/PokiShots/huong_dan/`, kèm `nhat_ky.txt`; tự trả bản lưu cũ).

### Khác kịch bản

- C4–C6: máy bi tự mở rương lúc hết đợt thả, và hộp lên cấp hiện sau rương (cách máy bi vốn chạy). Nên thứ tự là: thả bi, màn mở rương ("Rương! Chạm để mở." khoanh trên rương), lên cấp, rồi ghi chú "Bản sao thẻ: nâng cấp Chiêu ở mục Tướng."
- A4: ô tướng trong hộp chọn vẫn là chân dung tĩnh, chưa có hình diễn đòn.
- A9: hai ô đội khoá vẫn hiện.
- E1: chỉ thêm gợi ý chữ, chưa có 3 nút nhỏ. E2: hộp thua thêm câu "Thua không mất gì", nút Máy bi và Tướng.
- C15: Gầm Gừ rút sẵn ở lượt 2–3 của trận 2. Trận kết thúc trước khi nộ đầy thì bước này chạy ở trận sau, lần đầu nộ đầy.
- C10: hộp chi tiết tướng vẫn hiện nút Tiềm năng (chưa ẩn tới khi có đá).
- Chưa làm: D8 (rương mốc), D10, F9 (hộp thu phục riêng; hộp kết quả đã có nhãn "MỞ KHÓA!"), F11, G4–G10 (màn Nhà đang được phiên khác làm lại).

### Kiểm

- EditMode 151/152. Test còn đỏ là `PrefabOnlyTests`, hỏng từ trước: `NumberTicker`, `UiMotion`, `HomeScene` gridMat.
- Tour người chơi mới đi hết A2 → C17, kể cả C15. Ảnh soi từng bước ở `Temp/PokiShots/huong_dan/`.
- Sửa sau khi soi ảnh:
  - lớp phủ chuyển sang canvas Overlay, vì màn mở rương (thứ tự 400) và trận đè lên;
  - nét lót giấy dưới vòng đỏ (khó thấy trên máy bi đỏ);
  - bút chì nhỏ lại, ngòi chĩa vào chỗ khoanh;
  - ghi chú đặt dưới chỗ khoanh khi còn chỗ;
  - ghi chú không gắn chỗ nào thì chờ hộp thoại đóng;
  - ép bấm Chiêu chỉ khi lượt chọn đã vẽ xong;
  - camera sảnh lướt tới đảo cần khoanh (C12), tới con tàu (G2);
  - bảng tên đảo có gốc cỡ 0 thì khoanh theo khung bao các con.

## 11. Cốt truyện mở đầu (2026-11-23, đã làm, có tranh)

Người dùng: "lần đầu vào có thể làm thêm 1 chút hình ảnh cốt truyện như kingdom rush rồi mới vào boot". Đã chốt:
- truyện: lạc vào thế giới lạ có sinh vật kỳ bí, rồi đi chinh phục;
- 1–2 trang, chạm hiện từng khung tranh;
- ít chữ;
- tranh do GPT vẽ theo file prompt.

### Kịch bản (2 trang × 3 khung)

| Khung | Cỡ | Tranh | Chữ (game in, không vẽ) |
|---|---|---|---|
| 1 | ngang 1536×1024 | đêm bão, thuyền buồm nhỏ bị cuốn vào xoáy mây năm màu | Một đêm giông bão... |
| 2 | dọc 1024×1536 | tỉnh dậy trên bãi cát đảo lạ, dấu chân ba ngón to dẫn vào rừng | Tỉnh dậy ở một thế giới lạ. |
| 3 | dọc | rừng sương, mắt sinh vật lấp ló sau lá | (không chữ) |
| 4 | dọc | năm tướng đồng hành ra gặp nhà thám hiểm | Những người bạn mới. |
| 5 | dọc | trên vách đá nhìn bóng chúa tể núi lửa (dáng nui_lua) | Mỗi đảo một chúa tể. |
| 6 | ngang | toàn cảnh năm đảo, thuyền ra khơi | Đi chinh phục thôi! |

Nhân vật chính (người chơi, người dùng chốt 2026-11-23): cậu bé thuần thú sư khoảng 11 tuổi, cầm sổ phép (bìa da nâu, góc đồng, sao năm màu hệ) và bút chì phép to cỡ cẳng tay dùng như đũa phép; thuần phục sinh vật bằng cách vẽ chúng vào sổ. Tóc nâu hạt dẻ có chỏm dựng, băng cá nhân trên má, áo choàng ngắn có mũ màu xanh mòng két, khăn đỏ, dây chéo ngực cài 5 bút chì 5 màu hệ. Không mũ, không ba lô. Phép thuật vẽ bằng nét chì màu, không phát sáng.

Cậu cũng nói lời dẫn trong hướng dẫn (`Guide.SayMe`): câu chào đầu game (a2, "Sổ phép đưa mình tới đây... Năm hòn đảo, năm hệ. Phải tìm một bạn đồng hành đã!") và câu mở các đảo (c11, "Bốn đảo nữa!..."). Chân dung cậu nằm bên trái ghi chú, tướng đồng hành (nếu đã chọn) nhỏ hơn bên phải. Chưa có ảnh `Assets/03 Art/Story/nhan_vat.png` thì lớp phủ hiện như cũ.

### Chạy thế nào

- Lần đầu vào game, khi bản lưu mới chưa chọn tướng và chưa có cờ `a0`, `App.Go` mở cốt truyện trước màn tải con tàu. Mây khép sẵn dưới nó.
- Xem xong hoặc bấm Bỏ qua (Back cũng là bỏ qua): ghi cờ `a0`, lưu, rồi vào màn tải như thường. Bản lưu cũ (`*`) không thấy.
- Màn: trang truyện tranh tràn màn hình (người dùng đổi 2026-11-23: "full screen, cấu trúc như comic panel", bỏ kiểu ảnh dán băng keo trên bàn gỗ).
  - Mỗi trang 3 ô tứ giác ghép kín trang, vách chia xiên, khe giấy 26 px, lề ngoài 22 px, viền mực 7 px. Trang 1: ô ngang trên, hai ô dọc dưới; trang 2: hai ô dọc trên, ô ngang dưới.
  - Vách ngang đặt theo cỡ màn để ô ngang (3:2) và ô dọc (2:3) bị cắt bớt bề ngang như nhau. Mỗi tranh có điểm lấy nét để giữ cậu bé và các tướng khi bị cắt.
  - Trên màn dài 9:19,5 mỗi ô vẫn mất khoảng 30% bề ngang. Ô 4 mất một phần các tướng ở hai mép. Muốn khỏi mất thì vẽ nới tranh lên trên và xuống dưới cho khớp ô.
  - Mỗi chạm hiện một ô: ô nảy ra từ tâm, rồi chữ chạy dần trong khung lời dẫn vàng nhạt viền mực ở góc ô.
  - Tranh đã hiện thì trôi chậm trong ô (phóng 3%, lia 10), mép ô đứng yên.
  - Chạm lúc ô đang hiện thì hiện xong ngay.
  - Hết ô 3 thì trang 2 trượt vào từ phải, giữa hai trang lộ nền mực. Chạm sau ô 6 thì mờ dần, xong.
  - Sau 1,4 giây không chạm thì hiện "Chạm để tiếp tục" (chữ giấy viền mực, giữa đáy).
- Nhạc chủ đề (`chude`) như màn tải.
- Xem lại: Sổ tay → dòng "Cốt truyện mở đầu" → nút "Xem" (thêm 2026-11-23, menu `PokiClash/Prefab/Hộp thoại và màn/Sổ tay: thêm dòng Cốt truyện`), hoặc Sổ tay → Cách chơi → nút "Xem lại cốt truyện".
- Trong Editor: menu `PokiClash/Thử/Người chơi mới/Cốt truyện mở đầu: xem lại`. Chưa Play thì tự mở `Boot.unity`, vào Play, bỏ màn mở game, chờ màn tải xong rồi mở cốt truyện; bản lưu không đổi.

### Code, prefab

- `App/StoryIntro.cs`: bố cục ô (`Quad`, `Divider`, `Focus`), tính lúc chạy theo cỡ màn (`Layout`).
- `App/ComicPanel.cs`: Graphic vẽ tranh trong tứ giác, phủ kín khung bao, có điểm lấy nét, trôi trong ô.
- `Editor/StoryIntroMenu.cs`:
  - menu `PokiClash/Prefab/Hộp thoại và màn/Cốt truyện mở đầu (CotTruyen)` dựng `Assets/04 Prefabs/Screens/CotTruyen.prefab` (canvas thứ tự 25) và gán `App.storyPrefab`;
  - menu thử `PokiClash/Thử/Người chơi mới/Cốt truyện mở đầu: xem lại` và `…: chạm hết và chụp từng khung` (ảnh ở `Temp/PokiShots/cot_truyen/`).
- `Core/Tutorial.cs`: `Story = "a0"`, `StoryNeeded`.
- `App/App.cs`: `storyPrefab`, nhánh trong `Go()`, `Booting` tính cả cốt truyện, Back = bỏ qua.
- `App/AudioService.cs`: nhạc chủ đề khi cốt truyện mở.
- `App/HowToDialog.cs` và `Editor/GuideMenu.cs`: nút xem lại.
- 6 chuỗi mới nối vào `Resources/Loc/en/ui.json`.

### Tranh

- Gói GPT dựng bằng `ArtGen/Story/build_story.py`, ra thư mục `ArtGen/Story/gui_gpt/`. Mỗi lượt một file prompt, kèm `HUONG_DAN.md`.
- Các lượt:
  - lượt 0: tờ thiết kế nhân vật chính;
  - lượt 1 (sau `--duyet nv`): chân dung bán thân nền trong suốt và khung 2;
  - lượt 2: khung 1 và 3;
  - lượt 3: khung 4, 5, 6.
- Lượt 2 và 3 chỉ dựng sau khi duyệt khung 2 (`--duyet 2`).
- `--nhap` cũng chép chân dung (cắt sát, cạnh dài 512) vào `Assets/03 Art/Story/nhan_vat.png`; rồi chạy menu `PokiClash/Prefab/Hộp thoại và màn/Hướng dẫn người mới (lớp phủ)`.
- `--nhap` thu ảnh về cạnh dài 1024 rồi ghi vào `Assets/03 Art/Story/khung_k.png`. Sau đó chạy lại menu dựng prefab.
- Khung chưa có tranh thì tạm dùng nền trận hoặc bản đồ có sẵn.

### Kiểm (2026-11-23)

- EditMode 151/152. Test đỏ vẫn là `PrefabOnlyTests`, hỏng từ trước.
- Thử như người mới: tạm cất bản lưu, Play. Luồng chạy: cốt truyện, màn tải, sảnh, lời chào a2, hộp chọn tướng. Xong thì trả bản lưu cũ.
- Ảnh soi từng khung ở `Temp/PokiShots/cot_truyen/`.
- Sửa sau khi soi:
  - khung nghiêng làm tranh tràn mép, vì RectMask2D cắt theo hộp thẳng; đổi sang Mask;
  - tranh chừa 12% để trôi;
  - cả cụm khung hạ 45 cho cân trang.
- Hộp chọn tướng: ô mô tả cao 440 để trống lớn trên nút (phiên soát UI báo), hạ còn 190 và căn giữa.

### Tranh và kiểm lần 2 (2026-11-23 đêm)

- Người dùng cho Claude tự gen và tự duyệt. Gen bằng Codex (`ArtGen/Spine/gen.py`).
- Đã có, duyệt ở `ArtGen/Story/duyet/`, nhập vào `Assets/03 Art/Story/`:
  - tờ nhân vật;
  - chân dung nền trong suốt;
  - 6 khung.
- Lệch nhỏ đã chấp nhận:
  - tờ nhân vật chỉ thấy 4 bút chì trên dây chéo;
  - khung 5 vẽ chúa tể màu sẫm chứ không phải bóng đen.
- Cách nhập ảnh do `ArtPostprocessor` đặt (sprite, không mipmap, ASTC 6x6, 1024). Menu cốt truyện không tự đặt nữa.
- Thử như người mới (cất bản lưu, Play): cốt truyện 6 khung, màn tải, câu chào a2 có chân dung cậu bé, tour đi hết A2 → C17. Câu c11: cậu bé bên trái, tướng đồng hành bên phải.
- Sửa thêm: màn Tướng bỏ lọc hệ khi bước C9 còn chờ. Lọc Kim còn nhớ trong PlayerPrefs đã giấu mất ô tướng đồng hành và làm tour kẹt.
- Chữ "Chạm để tiếp tục" của lời dẫn mờ khi nằm đè lên bảng tên đảo (c11): thêm viền mực (material nướng sẵn `vien 25` theo phông).
- Hộp Cách chơi: khung cuộn hạ thấp bằng chiều cao hàng nút, chữ không còn chạy xuống dưới nút "Xem lại cốt truyện" (phiên soát UI báo).

## 12. Khắc hệ là chiến thuật (2026-11-27)

Người dùng dặn: FTUE phải cho người chơi biết khắc hệ rất quan trọng với chiến thuật; ô tướng có một icon, chạm thì hiện popup xung khắc hệ.

Trước đó người chơi chỉ gặp khắc hệ qua câu chữ: khoanh đảo (C12), nút Xuất trận (C13), ghi chú trong trận (C14), F8. Chỉ nghe "×1,5" mà không thấy cả vòng, không biết mặt bất lợi (tướng đồng hành không bao giờ chịu thiệt nên người mới không gặp ×0,75), và không có chỗ xem lại ngay trên ô tướng.

- **Hộp Tương khắc** (`App/ElementWheelDialog`, prefab `Dialogs/TuongKhac`):
  - băng tiêu đề nâu sẫm, chữ kem viền mực; dòng "tên · hệ";
  - vòng 5 hệ theo chiều khắc (Thủy → Hỏa → Kim → Mộc → Thổ → Thủy), mũi tên cung từ hệ khắc tới hệ bị khắc;
  - mũi tên ra khỏi hệ đang xem màu xanh lá, mũi tên vào nó màu đỏ, còn lại màu giấy sẫm. Ba hệ liên quan có vòng sáng (vàng, xanh, đỏ);
  - mũi tên vẽ dần lần lượt, bắt đầu từ mũi tên xanh, vòng một lượt về mũi tên đỏ;
  - hai dòng: KHẮC (hệ mình → hệ bị khắc, "Đánh ×1,5 / Chịu đòn ×0,75") và BỊ KHẮC (hệ khắc mình → hệ mình, "Đánh ×0,75 / Chịu đòn ×1,5"). Số tính bằng `Elements.Mult` có cờ đồng hành, nên tướng đồng hành ghi ×1 ở dòng BỊ KHẮC kèm câu riêng;
  - câu chiến thuật: "Trước mỗi trận, xem hệ địch và mang tướng khắc nó!".
- **Nút vòng 5 chấm** (`Fallback/Icons/tuong_khac.png`, nút tròn giấy `nut_tuong_khac`): thẻ màn Tướng (góc trên phải), ô hộp chọn đội (đáy phải dải hệ), hộp chi tiết tướng (sau nhãn hệ), hộp chọn tướng khởi đầu (cuối hàng tên). Chạm nút chỉ mở hộp, không mở chi tiết hay chọn tướng.
- **FTUE:**
  - C12a: sau C11, hộp Tương khắc dạng bài học (bắt buộc, vẽ chậm, nút "Hiểu rồi!"), rồi mới khoanh đảo mình khắc (C12);
  - D11, D13: gợi ý nút vòng 5 chấm ở màn Tướng và hộp chọn đội;
  - D12: lần đầu đem tướng bị địch khắc vào trận, khoanh ô đó, nói rõ thiệt bao nhiêu và nên đổi sang hệ nào. Đây là chỗ người chơi học mặt bất lợi;
  - trang "Khắc hệ" của Cách chơi viết lại đủ hai chiều.
- Code: `Tutorial` (mã `c27`, `d11`, `d12`, `d13`), `HubScene.TutorStep`, `HeroesScene.RenderGrid`, `TeamPickerDialog.Show`, `StagePrepDialog.TutorTips`.
- Dựng: menu `PokiClash/Prefab/Hộp thoại và màn/Tương khắc: hộp và icon ô tướng`, hoặc cờ `Temp/tuong_khac_build.flag`.
- Test: `TutorialTests.KhacHe_BaiHocBatBuoc_GoiYTheoCongTac_MaKhongTrung`.
- Sửa sau khi người dùng soi (2026-11-27):
  - câu chiến thuật hai dòng lòi ra dưới tờ giấy khi không có nút "Hiểu rồi!": tính lại cao tờ (1326 / 1472) và thu vòng (bán kính 245);
  - tên hệ đặt phía ngoài vòng theo hướng từ tâm ra, không còn bị mũi tên đè (Hỏa, Thổ);
  - người chơi tự chạm nút vòng 5 chấm là coi như đã học: D11, D13 và bài học C12a đánh dấu xong, không dẫn mở lại.
