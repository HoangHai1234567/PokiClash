# Gói gen: quái bùn (`quai_bun`), tướng 8 đảo Thổ (ải 50)

Con gốc của rig: `monster_3668` (game tham khảo). Ảnh part gốc trên các tờ D_* là của game đó: chỉ dùng trong máy, không đăng công khai. Ghi chú: `ArtGen/Spine/inbox/quai_bun_ghichu.md`.

## Lượt 1: concept (xong, người dùng chọn A → `tai_ve/L1_duyet.png`)

## Lượt 2: mảnh (Claude tự gen bằng Magnific GPT 2.6, 1k high, 95 credit / tờ: `py -3 -I ArtGen/Spine/gen_magnific.py <file>`)

Tờ T* (đúng chỗ, đúng cỡ trên concept): ảnh mẫu duy nhất là concept duyệt `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\L1_duyet.png` (1536 × 1024, nền trắng, quái bùn nâu quay phải). Mỗi tờ vài mảnh không chạm nhau, vẽ đủ phần bị che.

- **T1** (than): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\quai_bun_1\luot_2_T1.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\M_T1.png`.
- **T2** (vai_gan, tay_xa_tren): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\quai_bun_1\luot_2_T2.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\M_T2.png`.
- **T3** (dau, tay_xa_duoi): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\quai_bun_1\luot_2_T3.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\M_T3.png`.
- **T4** (ham, tay_gan): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\quai_bun_1\luot_2_T4.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\M_T4.png`.
- **T5** (long_mieng): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\quai_bun_1\luot_2_T5.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\M_T5.png`.

Tờ D_* (theo khung part gốc): ảnh 1 = tờ part gốc cắt theo lưới (hình cel số xám lam, đầu xúc tu hồng, lòng miệng xanh sáng), ảnh 2 = concept duyệt (lấy màu, chất liệu), ảnh 3 = vượn núi đá (lấy nét).

- **D_P** (hai lòng bàn tay + 16 đốt ngón (phóng 2,4 lần); ảnh 1 = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\mau\goc_P.png`): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\quai_bun_1\luot_2_D_P.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\D_P.png`.
- **D_X** (chín xúc tu (phóng 1,7 lần); ảnh 1 = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\mau\goc_X.png`): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\quai_bun_1\luot_2_D_X.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\D_X.png`.
- **D_V** (tay co giãn: bắp tay, nắm đấm, ống cẳng tay (phóng 1,75 lần); ảnh 1 = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\mau\goc_V.png`): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\quai_bun_1\luot_2_D_V.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\D_V.png`.
- **D_H** (đầu hàm khổng lồ skill_04 + khung mắt, mắt; ảnh 1 = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\mau\goc_H.png`): file prompt `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\quai_bun_1\luot_2_D_H.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\quai_bun_1\tai_ve\D_H.png`.

Kiểm: tờ T: mảnh trùng chỗ, cỡ với concept (`quai_bun_manh.py ghep`), phần che vẽ đủ, viền kín, đầu không mắt; tờ D: mỗi part trùng hình bóng part gốc (`cat` in IoU, dưới 0,9 thì gen lại), không còn xám lam / hồng / xanh sáng; nền trắng tinh.

Câu sửa nhanh: "every part must stay at exactly the same place and size as in image 1"; "flat colour only, no shading"; "no pink, no cyan: mud brown, grey stones, amber inside only".
