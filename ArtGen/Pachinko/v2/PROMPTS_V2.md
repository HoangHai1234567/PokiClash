# Màn máy bi bản 2: các tờ mảnh (Magnific GPT 2.6, 1k, quality high, 95 credit/ảnh)

Người dùng chốt 2026-11-20: concept 2 (`concept_man_may_2.png`) + cờ đuôi nheo dưới gờ đế của concept 1. Bố cục, số đèn và nhịp đo từ
bản đục máy bi Clash of Critters (`D:\CrittersRipper\analysis_ui\BAO_CAO_MAY_BI_UI.md`). Không gửi hình của họ: ảnh mẫu chỉ là khung
bố cục mình vẽ (`make_parts_refs.py` → `refs/`), hai concept của mình và `ArtGen/Islands/refs/world_style.png`.

| Tờ | Khổ | Ảnh mẫu (theo thứ tự) | Lưu |
|---|---|---|---|
| Thân máy (vòm đỏ, đèn tắt, sao + cuộn xanh, gờ đế, cờ, chân) | 2:3 | khung_than_may, concept 2, concept 1, world_style | `tai_ve/than_may_v2.png` |
| Bảng số (khung cam vàng, 13+13+2+2 bóng tắt, màn mận trống) | 3:2 | khung_bang_so, concept 2, world_style | `tai_ve/bang_so_v2.png` |
| Chữ số 0–9 + x (vàng, sọc kem, viền nâu) | 3:2 | khung_luoi_so, concept 2, world_style | `tai_ve/chu_so_v2.png` |
| Nút PUSH 4 trạng thái (thường, lún, hết, cược lớn), chung đế | 1:1 | khung_luoi_nut, concept 2, world_style | `tai_ve/nut_push_v2.png` |
| 6 món: viên cược, cược khoá, khay rương, thanh đếm bi, nút liền tắt/bật | 3:2 | khung_luoi_mon, concept 2, world_style | `tai_ve/mon_v2.png` |
| 12 hình sáng trên nền đen (bóng vàng/hồng/trắng, quầng, sao 4 cánh, loé 8 tia, quạt tia, xu, giấy màu, vệt, vòng, sao 5 cánh) | 3:2 | khung_luoi_fx, concept 2, world_style | `tai_ve/fx_sang_v2.png` |
| Nền phòng (không máy, giữa trống) | 2:3 | concept 2, concept 1, world_style | `tai_ve/nen_phong_v2.png` |

Câu kiểu chung: "wobbly dark-brown ink outlines, coloured pencil and wax crayon texture, bright flat colours, one flat colour per area,
chunky cute shapes. No drop shadows, no 3D render, no gradients" (tờ hình sáng được phép quầng mềm, nền đen để đổi sang cộng sáng).

Thân máy nằm SAU bàn bi; góc cam của `Assets/03 Art/Baked/Machine/may_tinh.png` làm trong suốt nên viền đỏ có đèn hiện ra quanh vòm
trời. Cửa sổ trong khung vẽ nhỏ hơn vòm trời 10 px (`refs/cua_so.png` là cửa sổ đúng), bàn thu 0,92 (`refs/bo_cuc_v2.json`).
