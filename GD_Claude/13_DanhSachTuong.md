# Danh sách 40 tướng theo hệ (chốt chọn 2026-10-31)

Người dùng chốt (2026-10-31):
- 8 tướng mỗi hệ, tổng 40;
- chọn lại theo hệ gốc của aola;
- hình mới gen bằng prompt chữ (gói `ArtGen/Heroes`).

Người dùng chốt thêm (2026-11-01):
- **mỗi tướng là một dòng tiến hóa**, lên sao thì đổi hình;
- quái thường lấy dòng có 2–4 dạng, boss lấy dòng có 3 dạng trở lên;
- được gen dựa trên hình aola;
- **cách gen** (chốt lại cùng ngày, sau khi ảnh `tieu_y_1` bị chê "không đúng theme game"):
  - thay tạo hình trên rig vector của aola, giữ animation;
  - sinh vật mới khác hẳn con gốc nhưng tay chân trùng rig;
  - tướng là sinh vật kiểu thú nuôi, nét như hình trận aola;
  - quy trình ở `ArtGen/Heroes/QUY_TRINH.md`;
- **tướng Thủy đầu tiên là dòng khởi đầu hệ Nước của aola** (7 滴滴 → 8 露滴 → 9 露西亚, tên trong game là Giọt Sương), thay Tiểu Y làm tướng khởi đầu.

Đảo Thủy đã chọn lại theo luật này. **Hình tướng làm lại 2026-11-02** (`ArtGen/Heroes/QUY_TRINH.md`, gói gửi GPT sinh bằng `ArtGen/Heroes/build.py`): bỏ mọi file prompt tướng cũ (`Thuy.md`, `PROMPTS.md`, `thuy/*.md`); vẫn vẽ đè lên rig của dòng aola dưới đây. Kim, Mộc, Hỏa, Thổ bên dưới vẫn là danh sách cũ, chờ chọn lại.

**File này ghi nguồn aola, chỉ để đối chiếu nội bộ. Không đính kèm cho GPT, không đưa lên mạng.**

## Cách chọn

- **Hệ:** lấy theo trường hệ của `pmDataMap` (cột 16) trong `AolaRipper/lists/h5_data/pmdatalist.json`.

  | Hệ aola (mã) | Hệ game |
  |---|---|
  | Cơ khí (8) | Kim |
  | Cỏ (11) | Mộc |
  | Nước (10; 25 là Nước đời sau) | Thủy |
  | Lửa (9) | Hỏa |
  | Đất (5) | Thổ |

- **Ứng viên:** 819 con có hình trận render sẵn (`raw/flash/fightassets/bitmap/`), gom thành khoảng 420 dòng tiến hóa. Chọn theo:
  - hình dáng khác nhau giữa các tướng;
  - đọc được ở cỡ nhỏ;
  - hợp hệ;
  - không lấy nhân vật lịch sử (bỏ dòng 刘备 #1223–1225) hay chủ đề lễ hội nước ngoài.
- **Độ hiếm mỗi hệ:** 2 Thường, 2 Khá, 2 Hiếm, 1 Sử thi, 1 Huyền thoại.
- **Huyền thoại** của Kim, Mộc, Thủy, Hỏa theo Tứ Tượng: Bạch Hổ (Tây, Kim), Thanh Long (Đông, Mộc), Huyền Vũ (Bắc, Thủy), Chu Tước (Nam, Hỏa). Thổ giữ Đại Sư Cà Sa.
- **Ngoại lệ:** 4 thầy tu giữ ở Thổ và Hỏa dù dòng thỏ gốc là Cỏ, vì đã reskin thành thiết kế riêng.
- **Hình mới:** prompt chỉ giữ ý tưởng (loài, vai trò, màu chính). Chi tiết đổi khác, không đính ảnh aola, không nhắc tên game.

## Danh sách

"Nguồn" là id thú trong aola, kèm dạng tiến hóa (→). Cột "Ảnh" là mã trong `ArtGen/Heroes/PROMPTS.md` cũ (đã bỏ 2026-11-02).

### Kim

| Id game | Tên | Danh hiệu | Độ hiếm | Nguồn | Trạng thái | Ảnh |
|---|---|---|---|---|---|---|
| `bu_long` | Bu Lông | Người máy tí hon | Thường | 76 盼盼 (76 → 77 → 78) | mới | TG01 |
| `phao_hop` | Pháo Hộp | Hộp sắt bắn đạn | Thường | 1889 小弹 → 1890 弹弹 | mới | TG02 |
| `kiem_linh` | Kiếm Linh | Thanh kiếm biết bay | Khá | 1617 太白之剑 | mới | TG03 |
| `meo_quyen` | Mèo Quyền Sắt | Nắm đấm nghìn cân | Khá | 1176 圆手机械猫 → 1177 百万巨拳猫 | mới | TG04 |
| `bo_cap` | Bọ Cạp Đồng | Đuôi pha lê cát đỏ | Hiếm | 678 赤砂巨蝎 (676 → 677 → 678) | mới | TG05 |
| `bo_ngua` | Bọ Ngựa Liềm Thép | Song liềm kiếm khách | Hiếm | 685 巨镰螳螂 (683 → 684 → 685) | mới | TG06 |
| `soi_linh` | Sói Linh Thép | Lửa lạnh giáp xanh | Sử thi | 2176 灵小狼 → 2177 灵狼 | mới | TG07 |
| `bach_ho` | Bạch Hổ | Thần thú phương Tây | Huyền thoại | 1911 炽燎天 (chỉ lấy dáng thú mặc giáp) | mới | TG08 |

### Mộc

| Id game | Tên | Danh hiệu | Độ hiếm | Nguồn | Trạng thái | Ảnh |
|---|---|---|---|---|---|---|
| `mam_go` | Mầm Gỗ | Hạt giống nhút nhát | Thường | 2373 圣诞小树人 (bỏ chủ đề Giáng sinh) | mới | TG09 |
| `nu_hoa` | Nụ Hoa | Bông nở lăn tròn | Thường | 22 小花苞 (22 → 23 → 24) | mới | TG10 |
| `kien_binh` | Kiến Binh | Lính gác giáo lá | Khá | 216 兵蚁 | mới | TG11 |
| `banh_tet` | Hiệp Sĩ Bánh Tét | Hiệp khách gói lá | Khá | 494 → 496 dòng bánh ú lá (đổi thành bánh tét) | mới | TG12 |
| `de_hoa` | Dê Hoa | Sừng gỗ vương miện hoa | Hiếm | 868 阿瑞斯角羊 (866 → 867 → 868) | mới | TG13 |
| `giac_long` | Giác Long Gỗ | Sừng vỏ cây xung trận | Hiếm | 2392 木小龙 → 2393 木角龙 | mới | TG14 |
| `phong_linh` | Phong Linh | Linh tướng gió lá | Sử thi | 943 小风灵 → 944 风之灵将 | mới | TG15 |
| `thanh_long` | Thanh Long | Thần thú phương Đông | Huyền thoại | 1219 格非 → 1220 利爪格非 | mới | TG16 |

### Thủy (chọn lại 2026-11-01 theo dòng tiến hóa)

Hệ Nước của aola có khoảng 100 dòng nhiều dạng. Dòng gốc dài nhất chỉ 3 dạng; 4 dạng trở lên chỉ có khi tính dạng siêu tiến hóa. Tiêu chí chọn như các hệ khác, thêm điều kiện số dạng.

| Id game | Tướng | Danh hiệu | Vai | Độ hiếm | Số dạng | Trạng thái |
|---|---|---|---|---|---|---|
| `tieu_y` | Tiểu Y | Bé con sóng nước | Quái thường | Thường | 2 | giữ; `y_trach` thành dạng 2 |
| `canh_cut` | Cánh Cụt | Đầu bếp xứ băng | Quái thường | Thường | 2 | mới |
| `giot_suong` | Giọt Sương | Giọt nước hóa rồng | **Tướng khởi đầu** (thay `tieu_y`) | chưa chốt (đang là Khá) | 3 | mới; dạng 1 đã tách rig (`reskin/pet7_parts`, `reskin/thuy_7`), có prompt |
| `tam_tay` | Tám Tay | Pháo thủ bong bóng | Quái thường | Khá | 2 | mới; thay 306 八爪鱼 (chỉ 1 dạng) |
| `ca_ngua` | Cá Ngựa | Lính gác rạn san hô | Quái thường | Hiếm | 3 | mới |
| `map_rang` | Mập Răng Cưa | Răng cưa biển sâu | Quái thường | Hiếm | 3 | mới |
| `lam_quan` | Lam Quân | Tiểu tướng chuông đồng | **Boss ải 4** | Sử thi | 3 | giữ, **Kim → Thủy**; `van_quan`, `hac_duc` thành dạng 2, 3 |
| `huyen_vu` | Huyền Vũ | Thần thú phương Bắc | **Boss ải 8** | Huyền thoại | 3 | mới |

| Mã ảnh | Tên dạng | Nguồn aola |
|---|---|---|
| `tieu_y_1` | Tiểu Y | 1319 小伊 |
| `tieu_y_2` | Y Trạch | 1320 伊泽 |
| `canh_cut_1` | Cánh Cụt Con | 1691 小当家 |
| `canh_cut_2` | Đầu Bếp Cánh Cụt | 1692 企企当家 |
| `giot_suong_1` | Giọt Nước | 7 滴滴 |
| `giot_suong_2` | Tiên Sương | 8 露滴 |
| `giot_suong_3` | Sương Long | 9 露西亚 |
| `tam_tay_1` | Tám Tay Bong Bóng | 1053 泡泡章鱼 |
| `tam_tay_2` | Tám Tay Pháo Thủ | 1054 泡泡炮章鱼 |
| `ca_ngua_1` | Cá Ngựa Tân Binh | 181 海马小兵 |
| `ca_ngua_2` | Cá Ngựa Song Đao | 182 海马刀客 |
| `ca_ngua_3` | Cá Ngựa Tướng Quân | 183 海马剑士 |
| `map_rang_1` | Cá Mập Con | 31 大嘴鲨 |
| `map_rang_2` | Mập Răng Cưa | 32 巨齿鲨 |
| `map_rang_3` | Vua Cá Mập | 33 鲨鱼王 |
| `lam_quan_1` | Lam Quân | 1831 蓝钧 |
| `lam_quan_2` | Vạn Quân | 1832 万钧 |
| `lam_quan_3` | Hắc Dực Vạn Quân | 2955 黑翼·万钧 (siêu tiến hóa của 1832, mã hệ 25) |
| `huyen_vu_1` | Rùa Ngọc | 713 灵龟 |
| `huyen_vu_2` | Rùa Biển Ngọc | 714 海灵龟 |
| `huyen_vu_3` | Huyền Vũ | 715 远古灵龟 |

Ảnh tham chiếu `ArtGen/Heroes/refs/thuy/REF_<mã ảnh>.png` là khung đứng đầu tiên của hình trận aola, phóng to trên nền trắng.

Ứng viên đã xem nhưng không lấy:
- cá nóc 16–18;
- cua 73–75, 452–454, 1313–1315;
- cá voi 537–539;
- dê biển 758–760;
- song ngư 829–831;
- người đá sóng 1211–1213.

Dòng 929–931 là Triệu Vân (nhân vật lịch sử) nên bỏ.

### Hỏa

| Id game | Tên | Danh hiệu | Độ hiếm | Nguồn | Trạng thái | Ảnh |
|---|---|---|---|---|---|---|
| `heo_lua` | Heo Lửa | Bờm lửa húc liều | Thường | 205 小火猪 (205 → 206 → 207) | mới, **chốt style** | TG25 |
| `dom_lua` | Đốm Lửa | Ngọn lửa tươi cười | Thường | 2419 小火星 → 2420 小火团 | mới | TG26 |
| `phao_tet` | Pháo Tết | Ba đầu nổ đùng | Khá | 1370 小爆 → 1371 三头爆 | mới | TG27 |
| `su_tu_lua` | Sư Tử Lửa | Bờm lửa nhỏ | Khá | 4 吉拉 (4 → 5 → 6) | mới | TG28 |
| `bo_de` | Võ Tăng Bồ Đề | Cánh lửa liên hoa | Hiếm | `monk_500` (reskin của 500) | giữ | TG29 |
| `ho_lua` | Hồ Lửa | Ba đuôi hỏa hồ | Hiếm | 307 利飞 | mới | TG30 |
| `phap_luan` | Thiền Sư Pháp Luân | Người xoay bánh xe pháp | Sử thi | `monk_2010` (reskin của 2010) | giữ | TG31 |
| `chu_tuoc` | Chu Tước | Thần thú phương Nam | Huyền thoại | 506 烈焰凤凰 (và dòng 276 → 278) | mới | TG32 |

### Thổ

| Id game | Tên | Danh hiệu | Độ hiếm | Nguồn | Trạng thái | Ảnh |
|---|---|---|---|---|---|---|
| `vo_su` | Võ Sư | Quyền thủ áo vải | Thường | `monk_boxer` (reskin của 1) | giữ | TG33 |
| `gau_mo` | Gấu Thợ Mỏ | Thợ đào hầm | Thường | 373 工程伊尼 | mới | TG34 |
| `soc_da` | Sóc Đá | Má phồng đầy sỏi | Khá | 825 阿地力 → 826 阿地力斯 | mới | TG35 |
| `bo_hung` | Bọ Hung Cát | Lăn cầu cát vàng | Khá | 210 圣甲虫 | mới | TG36 |
| `thach_nhan` | Thạch Nhân | Núi đá biết đi | Hiếm | 36 震天石人 (34 → 35 → 36) | mới | TG37 |
| `sa_than` | Sa Thần | Hộ vệ sa mạc | Hiếm | 1000 阿努比斯 | mới | TG38 |
| `ky_lan` | Kỳ Lân Cát | Bờm cát hoàng kim | Sử thi | 90 沙麒麟 (88 → 89 → 90) | mới | TG39 |
| `ca_sa` | Đại Sư Cà Sa | Kim cang hộ pháp | Huyền thoại | `monk_2217` (reskin của 2217) | giữ | TG40 |

**Tướng khởi đầu (2026-11-03, `15_TuongKhoiDau.md`):** Giọt Sương, Sư Tử Lửa, Bu Lông, Nụ Hoa, Thạch Nhân, mỗi con đứng ở ải 1 đảo cùng hệ. Cả 5 cùng Võ Sư đổi sang Khá (Bu Lông, Nụ Hoa, Võ Sư từ Thường; Thạch Nhân từ Hiếm), nên số tướng mỗi độ hiếm của Kim, Mộc, Thổ trong bảng trên không còn đúng 2-2-2-1-1.

### Bỏ khỏi danh sách

| Id game | Tên | Lý do |
|---|---|---|
| `gia_bi` | Gia Bỉ | Gốc là hệ U linh (mã 13), không thuộc 5 hệ |
| `su_gia` | Sứ Giả Gia Bỉ | Gốc là Nước, cùng dòng tên với Gia Bỉ; Thủy đã đủ 8 |
| `y_trach` | Y Trạch | Không còn là tướng riêng: thành dạng 2 của `tieu_y` |
| `van_quan`, `hac_duc` | Vạn Quân, Hắc Dực Vạn Quân | Không còn là tướng riêng: thành dạng 2, 3 của `lam_quan` |

## Việc còn lại (chưa làm)

Dữ liệu game vẫn là 11 tướng cũ. Đổi sang 40 tướng là một change riêng, làm ở web trước rồi chép sang Unity:

1. **Tướng:** thêm 31 tướng mới vào `Web/src/core/data/heroes.ts`, bỏ `gia_bi` và `su_gia`, đổi hệ của Lam Quân, Vạn Quân, Hắc Dực sang Thủy. Chỉ số gốc lấy theo cách cũ (6 chỉ số aola, cột 4–9).
2. **Thẻ riêng:** mỗi tướng mới cần chiêu, tuyệt kỹ, nội tại (93 thẻ).
3. **Ải:** sửa địch và boss của 5 đảo.
   - Đảo Kim mất Vạn Quân và Hắc Dực.
   - Đảo Mộc mất Gia Bỉ và Sứ Giả.
4. **Kiểm tra:** xuất lại golden, chạy lại máy tự chơi và quét nhịp.
5. **Bản lưu:** chuyển tướng, mảnh, thẻ của `gia_bi` và `su_gia` sang tướng khác (hoặc đổi ra bi).
6. **Hình aola trong Editor** (làm 2026-11-02): đã xuất animation gốc (4 clip mặt trước) và chân dung của 79 dạng thuộc 36 dòng ở bảng trên, ra `reskin/goc_<id>/export/anim.json` và `portrait.png` bằng `tools/goc_batch.py` của AolaRipper. Bảng tướng → các dạng: `reskin/pokiclash_lines.json`, gồm cả 4 thầy tu. Dòng lấy theo chuỗi tiến hóa của `pmDataMap` (cột 26), nên có thêm 2374 (dạng 2 của 2373). Khi dữ liệu có 40 tướng, `aola` của mỗi dạng lấy từ file này.
   - Máy thứ hai (`E:\ProjectAtomik\aola`, 2026-11-02): bản trên chưa push nên xuất lại cả 83 dạng (40 dòng, gồm 4 thầy tu) bằng `tools/goc_batch.py` và `tools/portrait_png.py` viết lại; `reskin/pokiclash_lines.json` lấy từ `HeroDb.asset`. Unity tự tìm thư mục `Aola*` nằm cạnh thư mục project (ngoài gốc ổ đĩa như trước).
7. **Dạng tiến hóa** (thêm 2026-11-01):
   - `HeroDef` thêm danh sách dạng: tên, ảnh, cỡ trên sân, sao bắt đầu.
   - Đề xuất mốc: dòng 2 dạng đổi ở sao 3; dòng 3 dạng đổi ở sao 3 và sao 5.
   - Tên tướng hiện theo dạng; sổ tướng hiện cả dòng.
8. **Dạng của địch:**
   - Địch thường lấy dạng theo sao (sao = 1 + cấp ÷ 6), nên trên đảo Thủy hầu hết là dạng 1.
   - ~~Boss nên có dạng cố định~~. Người dùng chốt khác (2026-11-02): boss ải 8 vào trận ở dạng 1 rồi tiến hóa trong trận (thẻ Tiến Hóa, xem `12_KeHoach_OpenSpec.md` mục "Boss tiến hóa"). Mini boss ải 4 vẫn lấy dạng theo sao.
9. **Ải đảo Thủy:** đổi địch 8 ải theo 8 dòng mới.
   - Tên ải 8 "Xoáy Nước Đinh Ba" hợp Y Trạch; nếu boss là Huyền Vũ thì đổi tên.
   - Boss ải 8 rơi mảnh dòng nào là việc cân bằng, chốt khi làm dữ liệu.
10. **Bản lưu:** gộp mảnh, thẻ, sao của `y_trach` vào `tieu_y`; của `van_quan`, `hac_duc` vào `lam_quan`.
11. **Các hệ khác:** chọn lại theo luật dòng tiến hóa, dựng ảnh rig (`refs/<hệ>/<mã>/`) rồi thêm dạng vào bảng `FORMS` của `ArtGen/Heroes/build.py`.

**Tên phiên âm:** Tiểu Y, Y Trạch, Lam Quân, Vạn Quân là phiên âm Hán-Việt tên gốc. Nên đổi tên trước khi phát hành.
