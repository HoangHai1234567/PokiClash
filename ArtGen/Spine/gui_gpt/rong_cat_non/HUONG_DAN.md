# Gói GPT: Sa Long DẠNG 1 (dạng nhỏ, `rong_cat_non`), rig `monster_3529`

Con gốc của rig: `monster_3529` (game tham khảo). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng công khai.

## Lượt 1: concept dạng nhỏ (2026-11-17)

Người dùng: "làm thử dạng 1 của tướng thứ 4 đảo thổ" (gen qua Magnific, trần < 100 credit / ảnh), chọn rig này. Bản hiện có (`rong_cat_1`) thành dạng 2.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\mau\goc_ca_con.png` | Con gốc 3529 khung 0 idle: thằn lằn rồng non bốn chân đang bước, đầu ngẩng bên phải mào gai dài, gai dọc lưng, đuôi dài có gai bên trái (chỉ lấy DÁNG và chỗ các chi) |
| 2 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_1\tai_ve\L1_duyet.png` | Sa Long dạng cuối đã duyệt (L1_duyet.png): giữ loài, mặt, màu, chất liệu |
| 3 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rua_lua_1\tai_ve\L1_duyet.png` | Rùa golem lửa (tướng đảo Hỏa) đã duyệt: lấy nét bút, vân sáp, cách tô phẳng một con thú đá nặng |
| 4 | `C:\Atomik\PokiWar\ArtGen\Spine\inbox\huou_go_2\tai_ve\L1_duyet.png` | Hươu gỗ (tướng đảo Mộc) đã duyệt: lấy nét bút, vân sáp, cách tô da thú có vài mảng / vằn phẳng |

- Gen: `py -3 -I ArtGen/Spine/gen_magnific.py C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_cat_non\luot_1_concept.txt` (95 credit, 1k high) hoặc gửi GPT đường dẫn đó; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\tai_ve\L1_A.png`. Bản được chọn chép thành `L1_duyet.png`.

Kiểm: cùng dáng bước, cùng chỗ đầu, chân, đuôi như ảnh 1; màu nâu bụi, mắt vàng, sừng mũi hổ phách nhỏ, hai sừng đá ngắn, phiến sa thạch nhỏ; mọi chi dính thân; mắt có chấm trắng; nét bút mực rung, vân sáp, tô phẳng, không bóng; nền trắng tinh.

## Lượt 2: mảnh đúng chỗ, đúng cỡ trên concept duyệt (2026-11-17, agent dạng 1)

Ảnh mẫu duy nhất (ảnh 1) = `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\tai_ve\L1_duyet.png`: concept duyệt (1536 × 1024, nền trắng). Mỗi tờ vài mảnh không chạm nhau, đúng chỗ, đúng cỡ, vẽ đủ phần bị che. Mắt Claude cắt thẳng từ concept, mắt nhắm dựng từ mặt nạ mắt. Gen: `py -3 -I ArtGen/Spine/gen_magnific.py <file>` (95 credit / tờ).

- **T1** (than): chỉ gửi đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_cat_non\luot_2_T1.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\tai_ve\M_T1.png`.
- **T2** (dau, duoi): chỉ gửi đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_cat_non\luot_2_T2.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\tai_ve\M_T2.png`.
- **T3** (chan_gan, tay_xa): chỉ gửi đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_cat_non\luot_2_T3.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\tai_ve\M_T3.png`.
- **T4** (tay_gan, pa, pc): chỉ gửi đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_cat_non\luot_2_T4.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\tai_ve\M_T4.png`.
- **T6** (dau_tren): chỉ gửi đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_cat_non\luot_2_T6.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\tai_ve\M_T6.png`.
- **T7** (ham): chỉ gửi đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_cat_non\luot_2_T7.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\tai_ve\M_T7.png`.
- **T5** (chan_xa, pb): chỉ gửi đường dẫn `C:\Atomik\PokiWar\ArtGen\Spine\gui_gpt\rong_cat_non\luot_2_T5.txt`; ảnh lưu vào `C:\Atomik\PokiWar\ArtGen\Spine\inbox\rong_cat_non\tai_ve\M_T5.png`.

Kiểm: từng mảnh trùng chỗ, cỡ với concept (`rong_cat_non_manh.py ghep`); phần bị che vẽ đủ, viền kín; đầu không còn mắt; nền trắng tinh.
