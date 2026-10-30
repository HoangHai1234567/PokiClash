# Bàn xếp khối

Luật bàn cho hướng A ([01_HuongPhatTrien.md](01_HuongPhatTrien.md)). Số trong ngoặc là đề xuất ban đầu, để chỉnh khi thử.

## Luật cơ bản (giữ của Block Blast)

- Bàn 8 × 8. Mỗi tay 3 khối; đặt hết 3 khối mới ra tay mới.
- Kéo khối vào bàn, không xoay. Hàng hoặc cột đầy thì xoá, nhiều đường xoá cùng lúc.
- Combo: xoá ở các lượt liền nhau thì bậc combo tăng. Ba lượt liền không xoá thì về 0 (như Block Blast gốc).
- Bộ 41 hình khối và cách chọn khối theo độ khó lấy ý từ bản port ở 2PlayersGame ([08_KyThuat_Unity.md](08_KyThuat_Unity.md)).

## Thêm cho trận đánh

### Màu là hệ

- **5 hệ Ngũ hành**: Kim, Mộc, Thủy, Hỏa, Thổ. Mỗi khối một màu, cả khối cùng hệ.
- Khắc: Kim → Mộc → Thổ → Thủy → Hỏa → Kim (đánh hệ bị khắc ×1,5, đánh hệ khắc mình ×0,75).
- Tay khối ra màu theo đội: hệ có trong đội ra nhiều hơn (khoảng 80 % khối thuộc hệ của đội). Hệ không có trong đội vẫn ra, xoá vẫn có đòn thường của tướng chủ lực.
- Pokiwar có 4 hệ (Nước, Lửa, Đất, Gió) và có "Đá Ngũ Hành". Ngũ hành hợp với dàn tướng võ tăng, đại sư đang làm ở dự án aola.

### Xoá đường thì ra đòn

1. Xoá xong, đếm số ô của từng hệ trong các đường bị xoá.
2. Tướng mỗi hệ đánh một đòn: sát thương = số ô × công của tướng × hệ số combo × khắc hệ.
3. Mỗi ô bị xoá cũng nạp nộ cho tướng cùng hệ.
4. Hệ số combo đề xuất: 1 + 0,25 × bậc combo. Xoá nhiều đường một lúc cộng thêm (2 đường ×1,3, 3 đường ×1,6, 4 trở lên ×2).
5. Dọn sạch bàn: cả đội nhận một đòn thêm.

Hệ quả cần thử: người chơi sẽ đặt khối theo màu để "dồn" một hệ vào một hàng. Đó chính là quyết định mới so với Block Blast thuần. Nếu nó làm bàn tắc quá nhanh, giảm hệ số khắc hệ trước.

### Ô đặc biệt

Thỉnh thoảng một ô trong khối mang biểu tượng (khoảng 1 ô / 2 tay):

| Ô | Khi bị xoá |
|---|---|
| Khiên | cả đội được khiên chặn đòn địch kế tiếp |
| Tim | hồi máu cả đội |
| Sao | nạp nộ cho mọi tướng |

Đây là phần "ngọc phòng thủ, hồi máu, xuất chiêu" của Pokiwar, gắn vào ô khối.

### Địch phá bàn

Mỗi địch có một hoặc hai kỹ năng bàn, tung khi bộ đếm lượt về 0:

- **Ném đá:** 2–3 ô đá rơi vào ô trống. Đá chỉ mất khi đường chứa nó bị xoá.
- **Đóng băng:** một ô đang có khối bị băng; phải xoá hai lần mới mất.
- **Khoá tay:** một khối trong tay bị khoá một lượt.
- **Đẩy rác (boss):** đẩy cả bàn lên một hàng, thêm một hàng rác có một lỗ ở đáy.

Mỗi kỹ năng báo trước một lượt (biểu tượng trên đầu địch), để người chơi kịp phản ứng.

### Hết chỗ đặt

Block Blast gốc: hết chỗ là hết ván. Ở đây:

- Cả đội **choáng**: mất khoảng 20 % máu tối đa, địch được đánh ngay một đòn.
- Bàn nổ một vùng 4 × 4 ở giữa (hoặc 2 hàng dưới cùng), ra tay mới chắc chắn đặt được (logic "cứu" của bản port).
- Thua khi cả đội hết máu, không phải khi hết chỗ.

## Biến thể sập (hướng B)

- Sau khi xoá, **từng ô** lơ lửng rơi thẳng xuống tới khi chạm đáy hoặc chạm ô khác. Tetris gọi đây là "sticky gravity"; khác với "naive gravity" là để cả hàng trên rơi một khối.
- Rơi xong mà có đường đầy thì xoá tiếp, bậc dây chuyền +1, hệ số đề xuất ×1,5 mỗi bậc. Lặp tới khi bàn đứng yên.
- Khối đặt ở đâu vẫn ở đó cho tới lần xoá kế tiếp, tức là trọng lực chỉ chạy sau khi xoá. Không chuyển thành Tetris có giờ.
- Bàn nên **cao hơn rộng** (8 cột × 10 hàng) để thấy được rơi. Màn dọc có chỗ cho việc này.
- Hợp với boss "đẩy rác từ đáy": rác đẩy lên, người chơi xoá để rác rơi lại.
- Cần nút xem trước: giữ ngón trên ô thì hiện bóng bàn sau khi sập. Không có thì người chơi mới sẽ thấy "may rủi".
