# Gói gửi GPT: màn VS truyện tranh và dải tuyệt kỹ

Sinh bằng `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\build.py`, đừng sửa tay (chạy lại script sẽ ghi đè).

Trong game (Unity):
- màn VS đầu trận là một trang truyện tranh: khung trên là đội địch (đỏ), khung dưới là đội bạn (xanh), ngăn bằng khe chéo; mỗi tướng một ô mặt, có lực chiến cả đội, chữ VS nổ giữa khe;
- khi ra tuyệt kỹ, khung đó cắt thành dải hình bình hành ngang sân, có mặt tướng ra chiêu và tên chiêu.

Chưa có ảnh thì game vẽ tạm (tia bằng code, hình nổ của bộ giấy, chân dung cắt ngang thân). Có ảnh nào thì game tự dùng ảnh đó.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh (`E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\tai_ve`). Xong một ảnh thì nhắn Claude "duyệt nền", "duyệt vs" hoặc "duyệt mặt <mã tướng>". Claude cắt nền và chép vào game; tự làm được bằng lệnh ở cuối file.

## Lượt 1: nền khung truyện (dùng chung mọi trận, mọi phe)

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\luot_1_nen.txt`. GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\tai_ve\vs_nen.png`. Trong game: đã có trong game.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | bản đồ thế giới của game (1024 × 1536): bốn đảo vẽ tay, viền mực nâu, tô sáp màu: chỉ để học nét |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\refs\man_vs_hien_tai.png` | ảnh chụp màn VS trong game hiện giờ: hai khung chéo đỏ, xanh, tia vẽ tạm bằng code, ô mặt tướng |

Soi: vuông 1024; tia tỏa từ giữa ra bốn mép; giữa trống một vòng tròn to; chỉ màu giấy kem, xám ấm, vài nét mực nâu (game tô đỏ hoặc xanh); không khung viền, không chữ, không nhân vật.

## Lượt 2: dấu VS

File prompt: `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\luot_2_vs.txt`. GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\tai_ve\vs_no.png`. Trong game: đã có trong game.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `E:\ProjectAtomik\PokiWar\ArtGen\Islands\refs\world_style.png` | bản đồ thế giới của game: chỉ để học nét |
| 2 | `E:\ProjectAtomik\PokiWar\ArtGen\StyleRefs\R1_UI_Cards.png` | màn Sổ thẻ bản web (540 × 960): học kiểu chữ tiêu đề tròn, mập, viền mực |

Soi: hình nổ vàng cam viền mực, chữ V S đỏ viền mực, đúng hai chữ; không bóng đổ (luật chung); nền trắng tinh; không chạm mép.

## Mặt tướng (mỗi dòng tiến hóa một file, mỗi dạng một bước)

Ảnh mẫu 1 của mọi file là bản đồ thế giới (học nét); ảnh mẫu 2 trở đi là chân dung từng dạng trong game, phóng 768 × 960 trên nền trắng (`E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\refs\mat`). GPT lưu `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\tai_ve\mat\<aola>.png`. Một file nhiều dạng: GPT vẽ bước 1 rồi dừng; gõ `next` để vẽ bước sau.

Nên làm trước: tướng khởi đầu, tướng và lính đảo Thủy (đang chơi). Tướng sẽ vẽ lại hình (QUY_TRINH của Heroes) thì để sau khi có hình mới rồi chạy lại script (ảnh mẫu lấy theo chân dung trong game lúc đó).

| File | Tướng | Hệ | Dạng (aola: trong game?) |
|---|---|---|---|
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\01_giot_suong.txt` | Giọt Sương (khởi đầu) | Thủy | Giọt Nước (`thuy_7`: có); Tiên Sương (`thuy_8`: có); Sương Long (`thuy_9`: có) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\02_bu_long.txt` | Bu Lông (khởi đầu) | Kim | Bu Lông (`goc_76`: chưa); Bu Lông (`goc_77`: chưa); Bu Lông (`goc_78`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\03_nu_hoa.txt` | Nụ Hoa (khởi đầu) | Mộc | Nụ Hoa (`goc_22`: chưa); Nụ Hoa (`goc_23`: chưa); Nụ Hoa (`goc_24`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\04_su_tu_lua.txt` | Sư Tử Lửa (khởi đầu) | Hỏa | Sư Tử Lửa (`goc_4`: chưa); Sư Tử Lửa (`goc_5`: chưa); Sư Tử Lửa (`goc_6`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\05_thach_nhan.txt` | Thạch Nhân (khởi đầu) | Thổ | Thạch Nhân (`goc_34`: chưa); Thạch Nhân (`goc_35`: chưa); Thạch Nhân (`goc_36`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\06_tieu_y.txt` | Tiểu Y | Thủy | Tiểu Y (`goc_1319`: chưa); Y Trạch (`goc_1320`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\07_canh_cut.txt` | Cánh Cụt | Thủy | Cánh Cụt Con (`goc_1691`: chưa); Đầu Bếp Cánh Cụt (`goc_1692`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\08_tam_tay.txt` | Tám Tay | Thủy | Tám Tay Bong Bóng (`goc_1053`: chưa); Tám Tay Pháo Thủ (`goc_1054`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\09_ca_ngua.txt` | Cá Ngựa | Thủy | Cá Ngựa Tân Binh (`goc_181`: chưa); Cá Ngựa Song Đao (`goc_182`: chưa); Cá Ngựa Tướng Quân (`goc_183`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\10_map_rang.txt` | Mập Răng Cưa | Thủy | Cá Mập Con (`goc_31`: chưa); Mập Răng Cưa (`goc_32`: chưa); Vua Cá Mập (`goc_33`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\11_lam_quan.txt` | Lam Quân | Thủy | Lam Quân (`goc_1831`: chưa); Vạn Quân (`goc_1832`: chưa); Hắc Dực Vạn Quân (`goc_2955`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\12_huyen_vu.txt` | Huyền Vũ | Thủy | Rùa Ngọc (`goc_713`: chưa); Rùa Biển Ngọc (`goc_714`: chưa); Huyền Vũ (`goc_715`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\13_mi_nhi.txt` | Mi Nhi | Thủy | Tiểu Mi (`goc_983`: chưa); Mi Nhi (`goc_984`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\14_ma_ket.txt` | Ma Kết | Thủy | Ma Kết Con (`goc_758`: chưa); Ma Kết Sừng Nhọn (`goc_759`: chưa); Ma Kết Thánh Giáp (`goc_760`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\15_vay_lam.txt` | Vây Lam | Thủy | Cá Đốm (`goc_546`: chưa); Cá Song Tiễn (`goc_547`: chưa); Cá Mập Vây Lam (`goc_548`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\16_thuong_lam.txt` | Thương Lam | Thủy | Thương (`goc_805`: chưa); Thương Nhiễm (`goc_806`: chưa); Thương Lam (`goc_807`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\17_kuba.txt` | Kuba | Thủy | Kuba (`goc_94`: chưa); Kuba Vỏ Cứng (`goc_95`: chưa); Kuba Kim Cương (`goc_96`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\18_phao_hop.txt` | Pháo Hộp | Kim | Pháo Hộp (`goc_1889`: chưa); Pháo Hộp (`goc_1890`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\19_kiem_linh.txt` | Kiếm Linh | Kim | Kiếm Linh (`goc_1617`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\20_meo_quyen.txt` | Mèo Quyền Sắt | Kim | Mèo Quyền Sắt (`goc_1176`: chưa); Mèo Quyền Sắt (`goc_1177`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\21_bo_cap.txt` | Bọ Cạp Đồng | Kim | Bọ Cạp Đồng (`goc_676`: chưa); Bọ Cạp Đồng (`goc_677`: chưa); Bọ Cạp Đồng (`goc_678`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\22_bo_ngua.txt` | Bọ Ngựa Liềm Thép | Kim | Bọ Ngựa Liềm Thép (`goc_683`: chưa); Bọ Ngựa Liềm Thép (`goc_684`: chưa); Bọ Ngựa Liềm Thép (`goc_685`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\23_soi_linh.txt` | Sói Linh Thép | Kim | Sói Linh Thép (`goc_2176`: chưa); Sói Linh Thép (`goc_2177`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\24_bach_ho.txt` | Bạch Hổ | Kim | Bạch Hổ (`goc_1911`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\25_mam_go.txt` | Mầm Gỗ | Mộc | Mầm Gỗ (`goc_2373`: chưa); Mầm Gỗ (`goc_2374`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\26_kien_binh.txt` | Kiến Binh | Mộc | Kiến Binh (`goc_216`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\27_banh_tet.txt` | Hiệp Sĩ Bánh Tét | Mộc | Hiệp Sĩ Bánh Tét (`goc_494`: chưa); Hiệp Sĩ Bánh Tét (`goc_495`: chưa); Hiệp Sĩ Bánh Tét (`goc_496`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\28_de_hoa.txt` | Dê Hoa | Mộc | Dê Hoa (`goc_866`: chưa); Dê Hoa (`goc_867`: chưa); Dê Hoa (`goc_868`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\29_giac_long.txt` | Giác Long Gỗ | Mộc | Giác Long Gỗ (`goc_2392`: chưa); Giác Long Gỗ (`goc_2393`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\30_phong_linh.txt` | Phong Linh | Mộc | Phong Linh (`goc_943`: chưa); Phong Linh (`goc_944`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\31_thanh_long.txt` | Thanh Long | Mộc | Thanh Long (`goc_1219`: chưa); Thanh Long (`goc_1220`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\32_heo_lua.txt` | Heo Lửa | Hỏa | Heo Lửa (`goc_205`: chưa); Heo Lửa (`goc_206`: chưa); Heo Lửa (`goc_207`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\33_dom_lua.txt` | Đốm Lửa | Hỏa | Đốm Lửa (`goc_2419`: chưa); Đốm Lửa (`goc_2420`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\34_phao_tet.txt` | Pháo Tết | Hỏa | Pháo Tết (`goc_1370`: chưa); Pháo Tết (`goc_1371`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\35_bo_de.txt` | Võ Tăng Bồ Đề | Hỏa | Võ Tăng Bồ Đề (`monk_500`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\36_ho_lua.txt` | Hồ Lửa | Hỏa | Hồ Lửa (`goc_307`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\37_phap_luan.txt` | Thiền Sư Pháp Luân | Hỏa | Thiền Sư Pháp Luân (`monk_2010`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\38_chu_tuoc.txt` | Chu Tước | Hỏa | Chu Tước (`goc_506`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\39_vo_su.txt` | Võ Sư | Thổ | Võ Sư (`monk_boxer`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\40_gau_mo.txt` | Gấu Thợ Mỏ | Thổ | Gấu Thợ Mỏ (`goc_373`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\41_soc_da.txt` | Sóc Đá | Thổ | Sóc Đá (`goc_825`: chưa); Sóc Đá (`goc_826`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\42_bo_hung.txt` | Bọ Hung Cát | Thổ | Bọ Hung Cát (`goc_210`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\43_sa_than.txt` | Sa Thần | Thổ | Sa Thần (`goc_1000`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\44_ky_lan.txt` | Kỳ Lân Cát | Thổ | Kỳ Lân Cát (`goc_88`: chưa); Kỳ Lân Cát (`goc_89`: chưa); Kỳ Lân Cát (`goc_90`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\45_ca_sa.txt` | Đại Sư Cà Sa | Thổ | Đại Sư Cà Sa (`monk_2217`: chưa) |
| `E:\ProjectAtomik\PokiWar\ArtGen\BattleIntro\gui_gpt\mat\46_linh.txt` | Lính của ải | Thủy | Cua Kìm (`goc_1313`: chưa); Cua Pháo (`goc_1314`: chưa); Cá Nóc (`goc_16`: chưa); Cá Nóc Điện (`goc_17`: chưa); Song Ngư Con (`goc_829`: chưa); Song Ngư (`goc_830`: chưa) |

Soi mặt: đúng con trong ảnh mẫu (màu, tai, sừng, mũ...); đầu và vai, mép dưới cắt ngang ngực; đầu chiếm gần hết chiều cao, đỉnh đầu không chạm mép; quay sang **trái**; mặt quả quyết, sẵn sàng đánh, không dữ; nét vẽ tay như bản đồ; nền trắng tinh, không viền trắng quanh đầu, không bóng đổ (luật chung: UI và tướng không vẽ bóng).

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Nền có màu | `Same image but only cream paper, warm grey and a little dark-brown ink: no other colour.` |
| Nền rối, che mặt tướng | `Same image with fewer, thinner lines and a bigger plain area in the middle.` |
| Nền có khung, viền | `Same image without any frame or border: the lines run off all four edges.` |
| Chữ VS sai, thừa chữ | `Redraw it with exactly two letters, V then S, and nothing else written.` |
| VS chạm mép | `Same sign a little smaller, centred, with white space all around.` |
| Mặt khác con trong ảnh mẫu | `Keep exactly the creature of the reference image: same head shape, colours, ears and markings. Only change the pose to a close-up face.` |
| Mặt quay phải | `Mirror it so the face looks to the viewer's left.` |
| Lấy cả thân, đầu nhỏ | `Closer: only the head and the top of the shoulders, the head filling most of the square.` |
| Mặt dữ quá hoặc ngố | `Same face, but brave and cute: brows a little lowered, a confident small grin.` |
| Bóng loáng kiểu 3D | `Redraw it in the hand-drawn style of image 1: wobbly ink outline, flat colours, pencil hatching, no shine.` |
| Có viền trắng, nền xám | `Same image on a plain pure white background, without a white outline around the head.` |
| Có bóng đổ, bóng lệch, bóng in xuống nền | `Same image without any shadow: no drop shadow, no offset shadow, nothing on the background. Keep only the pencil hatching inside the shapes.` |

## Lệnh (Claude chạy khi bạn nhắn duyệt)

```
py -3 -I ArtGen/BattleIntro/build.py --duyet nen
py -3 -I ArtGen/BattleIntro/build.py --duyet vs
py -3 -I ArtGen/BattleIntro/build.py --duyet mat <aola hoặc mã tướng>
```
Ảnh vào `Assets/03 Art/BattleIntro/Resources/`; mở lại Unity cho nó nhập, vào trận xem.
