# Tướng và nuôi dưỡng

## Một tướng có gì

| Thuộc tính | Ghi chú |
|---|---|
| Hệ | 1 trong 5 hệ Ngũ hành; quyết định ô màu nào làm tướng ra đòn |
| Phẩm | Thường, Hiếm, Sử thi, Huyền thoại |
| Máu, công | cộng vào máu đội; công nhân với số ô xoá |
| Chiêu | một chiêu đánh hoặc một chiêu bàn ([04_ChienDau.md](04_ChienDau.md)) |
| Bị động chủ lực | chỉ có tác dụng khi đứng đầu đội |
| Dòng tiến hóa | 2–4 dạng |

## Ba trục mạnh lên

1. **Cấp**: vàng + kinh nghiệm (từ ải, từ máy bi). Trần cấp theo bậc tiến hóa.
2. **Sao**: mảnh từ thu phục trùng hoặc thu phục hụt. Mỗi sao tăng chỉ số và có mốc mở thêm hiệu ứng cho chiêu.
3. **Tiến hóa**: đá tiến hóa theo hệ, như Pokiwar. Tiến hóa đổi hình, nâng trần cấp, mở chiêu mạnh hơn.

Gom lại thì mỗi tướng cần: thu phục một lần để có, mảnh để lên sao, đá để tiến hóa, vàng và kinh nghiệm để lên cấp. Mỗi thứ từ một nguồn riêng, để phần thưởng nào cũng có chỗ dùng.

## Nguồn hình tướng

Dự án aola đang thay tạo hình dòng 兔小子 của Aola (Baitian): võ sư (dạng 1), đại sư cà sa (#2217, dạng 6), võ tăng Bồ Đề (#500), thiền sư Pháp Luân (#2010). Bộ ghép xuất animation cho Unity (`reskin/<tên>/export/anim.json`, 4 animation: đứng, trúng đòn, đánh, chiêu).

- **Rất khớp dòng tiến hóa**: mỗi dạng của dòng Aola là một bậc tiến hóa, đã cùng khung xương và cùng nhịp animation.
- **Rất khớp bố cục dọc**: trận Aola có mặt trước (phía địch) và mặt sau (phía mình). Hiện mới làm mặt trước, đủ cho tướng địch và tướng hoang. Tướng phe mình cần mặt sau, hoặc dùng mặt trước lật ngang nếu chấp nhận nhìn chéo.
- **Đã chốt (2026-10-30): chỉ dùng trong bản thử.** Trước khi phát hành phải làm hình và chuyển động mới.
- **Lý do (rủi ro bản quyền):** `aola/AGENT.md` ghi hình Aola "chỉ để tham khảo… không đưa vào game", và `TIEN_DO.md` ghi chưa quyết dùng bản thay tạo hình cho game. Mảnh hình mới do GPT vẽ đè lên hình gốc, còn chuyển động là dữ liệu gốc của Baitian. Trước khi phát hành phải quyết: dùng nguyên, chỉ dùng làm mẫu để làm lại animation, hay làm mới hoàn toàn.

## Số tướng cho bản đầu

- Bản thử: 5 tướng phe mình (mỗi hệ một), 6 địch.
- Bản ra mắt nhỏ: 25–30 tướng (mỗi hệ 5–6), 3 chương.
- Pokémon Shuffle và Empires & Puzzles có hàng trăm tướng. Không cần đuổi số đó; cần đủ để mỗi chương có tướng mới để thu phục.
