# Nền banner popup ưu đãi kiểu mới (2026-11-27)

Popup gói học bố cục Clash of Critters (`App/Shop/OfferPopup.cs`, GD_Claude/26 mục 15). Đầu popup là banner chì sáp hai mảng màu xé chéo
và tia nắng, hoa văn mờ theo chủ đề. Gen bằng Magnific GPT 2.6, 2:1, 1k high (95 credit / ảnh, 4 ảnh), ảnh mẫu là
`ArtGen/Islands/refs/world_style.png` (nét game) và `Assets/03 Art/Shop/v2/goi2_nhap_mon.png` (nét hình gói).

| Tệp | Màu | Hoa văn | Dùng cho |
|---|---|---|---|
| `nen_hong` | hồng kẹo / xanh ngọc | bi, sao | Quà Nhập Môn, Gói Trở Lại, gói khác |
| `nen_xanh` | xanh trời / vàng | máy bay giấy, la bàn | Gói Khởi Hành 3 bậc |
| `nen_tim` | tím / vàng cam | vương miện, ngọc | gói tướng (Vượt Mốc, Đồng Hành, Sắp Lên Sao, Đảo Mới) |
| `nen_cam` | đỏ cà chua / cam | tia sét, lửa | Ưu Đãi Nóng, Bất Ngờ, Tiếp Sức |

- `tai_ve/`: ảnh gốc 1536 × 768. `out/`: thu về 1024 × 512, chép vào `Assets/03 Art/Shop/pop/pop_nen_<màu>.png`.
- Câu lệnh (đổi màu và hoa văn theo bảng): "Wide game UI banner BACKGROUND only, 2:1, full bleed ... hand-drawn on paper, wobbly dark-brown ink
  lines, colored pencil and wax crayon fill ... FLAT colors, no gradients, no lighting, no shadows ... split by one bold diagonal zigzag tear line
  from the lower-left to the upper-right ... sunburst rays ... sparse doodle pattern ... keep the middle and the bottom fifth calm ... No characters,
  no text, no frame".
