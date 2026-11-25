# Hình đảo Casino theo lớp (C8, người dùng dặn 2026-11-25: "gen đảo trống rồi gen riêng các công trình lên đó, đặt lên")

Hướng B (`../concept/concept_B_dao_vanh_khuyen.png`). Magnific GPT 2.6 1k high (95 credit / tờ), phóng classic 2k (72 credit / tờ).

| Tờ | Cách gen |
|---|---|
| `dao_trong_1k.png` → `dao_trong_2k.jpg` | Vẽ lại đúng concept B, bỏ mọi công trình; chỗ công trình để bãi trống (quảng trường tròn, hẻm lát đá, bãi cỏ, bờ cát); giữ đường đua đất |
| `cong_trinh_1k.png` → `cong_trinh_2k_nen_trang.jpg` | Cũng concept B nhưng chỉ giữ công trình, đúng chỗ đúng cỡ, nền trong suốt (GPT trả RGBA). Bản phóng 2k trải lên nền trắng, kênh trong suốt lấy lại từ bản 1k |
| `leu_1k.png` | 3 lều sự kiện (bài, vòng xoay, máy quả) gen rời; `xu_ly_2k.py` thu bằng 1,25 lần bãi cọc và đặt chân lều vào giữa bãi |

- `tach_cong_trinh.py [1k|2k]`: cắt từng công trình theo cụm điểm ảnh (khung `KHUNG` theo bản 1k), ghép thử.
- `xu_ly_2k.py`: bản 2k + lều + ghép thử (`ghep_thu_2k.png`, `ghep_thu_2k_leu.png`), chép vào `Assets/03 Art/Casino`
  (`casino_dao.png`, `casino_ct_<id>.png`, `casino_art.json`). Sau đó menu `PokiClash/Prefab/Đảo Casino/Đảo: dựng màn`.
- Trong game: đảo trống hiện 1:1 (2048 x 1360), công trình là Image đúng khung, xếp theo đáy; lều bật khi sự kiện của lều đang mở
  (`CasinoScene.ShowBooth`), không thì cọc bãi. Điểm chạm lấy khung từ ảnh công trình.
