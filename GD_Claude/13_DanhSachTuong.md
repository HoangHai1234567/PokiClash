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

Đảo Thủy đã chọn lại theo luật này. **Hình tướng làm lại 2026-11-02** (`ArtGen/Heroes/QUY_TRINH.md`, gói gửi GPT sinh bằng `ArtGen/Heroes/build.py`): bỏ mọi file prompt tướng cũ (`Thuy.md`, `PROMPTS.md`, `thuy/*.md`); vẫn vẽ đè lên rig của dòng aola dưới đây. Mộc, Hỏa, Kim chọn lại 2026-11-05; Thổ chọn lại 2026-11-06.

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

### Kim (chọn lại 2026-11-05 theo 10 hình người dùng gửi)

Người dùng gửi 10 hình aola cho đảo Kim, thứ tự trái sang phải là thứ tự ải tướng (1, 5, 10, 15, 20, 30 … 70). Mỗi hình lấy cả dòng tiến hóa chứa nó. Tên, độ hiếm, thẻ là tạm; độ hiếm tăng theo ải như đảo Mộc, Hỏa. Kế hoạch ải: `Editor/IslandGen.cs`, `IslandGen.Kim`.

| Ải | Id game | Tên | Danh hiệu | Độ hiếm | Nguồn (dạng 1 → 2 → 3) | Trạng thái |
|---|---|---|---|---|---|---|
| 1 | `bo_cap` | Bọ Cạp Đồng | Đuôi pha lê cát đỏ | Thường (từ Hiếm) | 676 水晶小蝎 → 677 绿岩石蝎 → 678 赤砂巨蝎 | giữ, thẻ mới |
| 5 | `doc_giac` | Độc Giác Thép | Ngựa một sừng giáp bạc | Thường | 656 铠甲独角兽 (1 dạng) | mới |
| 10 | `bo_ngua` | Bọ Ngựa Liềm Thép | Song liềm kiếm khách | Khá (từ Hiếm) | 683 螳螂小宝 → 684 利刃螳螂 → 685 巨镰螳螂 | giữ, thẻ mới |
| 15 | `phi_thuong` | Phi Thương | Kỵ sĩ máy song thương | Khá | 835 兰亚 → 836 兰亚斯特 | mới |
| 20 | `khien_bac` | Khiên Bạc | Vệ sĩ khiên bạc | Hiếm | 784 铁盾豆丁 → 785 银盾卫士 | mới |
| 30 | `chien_than` | Chiến Thần | Pháo thủ giáp vàng | Hiếm | 1083 小战灵 → 1084 战武巨神 | mới, bị động boss |
| 40 | `thiet_phu` | Thiết Phủ | Người thiếc rìu bén | Sử thi | 1533 铁皮人 → 1534 利斧铁皮人 | mới |
| 50 | `tam_kiem` | Tam Kiếm | Giáp vương ba kiếm | Sử thi | 1223 小备 → 1224 阿备 → 1225 刘备 | mới, bị động boss |
| 60 | `ung_thep` | Ưng Thép | Thợ săn trời cánh pha lê | Sử thi | 1696 猎小空 → 1697 猎空 (aola gắn nhãn BOSS, hệ aola 2) | mới |
| 70 | `kim_nghe` | Kim Nghê | Thần thú giáp lửa lam | Huyền thoại | 1840 克亚 → 1841 克里亚斯 (2 dạng, aola không có siêu tiến hóa) | mới, boss tiến hóa |

- Tên dạng: Bọ Cạp Pha Lê → Bọ Cạp Đá Lục → Bọ Cạp Đồng; Bọ Ngựa Con → Bọ Ngựa Lưỡi Bén → Bọ Ngựa Liềm Thép; Phi Thương Con → Phi Thương; Khiên Sắt Tí Hon → Vệ Sĩ Khiên Bạc; Chiến Linh Con → Chiến Thần; Người Thiếc → Thiết Phủ; Kiếm Sĩ Nhí → Song Kiếm → Tam Kiếm Vương; Ưng Thép Con → Ưng Thép; Nghê Con → Kim Nghê.
- Dòng 刘备 (1223–1225) trước bị loại vì là nhân vật lịch sử; người dùng gửi hình nên lấy, tên trong game là Tam Kiếm, không dùng tên gốc.
- Chỉ số gốc = 6 chỉ số aola của dạng 1 (`pmDataMap` cột 4–9), như đảo Mộc, Hỏa.
- Bu Lông (tướng khởi đầu hệ Kim) nhường ải 1 cho Bọ Cạp Đồng, đứng cùng một lính ở ải 2 (như Nụ Hoa ở đảo Mộc), vẫn thu phục được.
- Siêu tiến hóa chưa lấy: Khiên Bạc 2146 金盾卫士, Ưng Thép 2532 超猎空, Tam Kiếm 2336 昭烈刘备 trở đi, Chiến Thần 6087 (không có rig vector). Huyền thoại Kim theo Tứ Tượng trước là Bạch Hổ; nay boss đảo là Kim Nghê theo hình người dùng gửi.
- Tướng Kim cũ không có suất trên đảo (giữ trong danh sách): `phao_hop`, `kiem_linh`, `meo_quyen` (vẫn là quà ải 3 đảo Thủy khi chọn Thạch Nhân), `soi_linh`, `bach_ho`.
- Đo bằng máy tự chơi (đội Hỏa Khá khắc hệ: Sư Tử Lửa, Kim Sư; bằng cấp; 150 trận mỗi ải, ải tướng 300): cường hóa 93%, 2 địch 76%, 3 địch 84%, mini boss 63–73% (Khiên Bạc 63, Chiến Thần 73, Thiết Phủ 69, Tam Kiếm 69, Ưng Thép 67), boss Kim Nghê 63%.

Lính đảo Kim (dạng aola hệ Cơ khí chưa có trong danh sách tướng; Claude chọn, người dùng chưa duyệt):

| Lính | Bậc 1 | Bậc 2 | Vai |
|---|---|---|---|
| Giáp Vệ / Chiến Giáp | 121 机甲护卫 | 122 机甲战士 | trâu, như cua |
| Nóc Sắt / Nóc Khiên | 1061 铁甲小豚 | 1062 坚甲河豚 | phản đòn, như cá nóc |
| Máy Bay Con / Phản Lực | 949 飞飞机 | 950 喷气飞飞机 | nhanh, như song ngư |

Danh sách Kim cũ (2026-10-31), giữ để đối chiếu:

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

### Mộc (chọn lại 2026-11-05 theo 10 hình người dùng gửi)

Người dùng gửi 10 hình aola cho đảo Mộc, thứ tự trái sang phải là thứ tự ải tướng (1, 5, 10, 15, 20, 30 … 70). Mỗi hình lấy cả dòng tiến hóa chứa nó; Thanh Long (boss) thêm dạng siêu tiến hóa đầu tiên cho đủ 3 dạng. Tên, độ hiếm, thẻ là tạm; độ hiếm tăng theo ải như đảo Thủy.

| Ải | Id game | Tên | Danh hiệu | Độ hiếm | Nguồn (dạng 1 → 2 → 3) | Trạng thái |
|---|---|---|---|---|---|---|
| 1 | `tien_la` | Tiên Lá | Ánh lục giữa rừng | Thường | 648 绿光兽 → 649 绿光小灵 → 650 绿光精灵 | mới |
| 5 | `hoa_nhuy` | Hoa Nhụy | Tiên hoa nhụy đỏ | Thường | 593 三叶兽 → 594 花苞兽 → 595 花蕊精灵 | mới |
| 10 | `de_hoa` | Dê Hoa | Sừng gỗ vương miện hoa | Khá (từ Hiếm) | 866 花羊羊 → 867 木尔羊 → 868 阿瑞斯角羊 | giữ, thẻ mới |
| 15 | `bom_la` | Bờm Lá | Chiến sư rừng xanh | Khá | 911 木叶小兽 → 912 木叶战狮 | mới |
| 20 | `phong_linh` | Phong Linh | Linh tướng gió lá | Hiếm (từ Sử thi) | 943 小风灵 → 944 风之灵将 | giữ |
| 30 | `gio_loc` | Gió Lốc | Rồng gió xé mây | Hiếm | 850 风 → 851 卷风 → 852 碎风 (hệ aola 19) | mới |
| 40 | `long_vuot` | Long Vuốt | Rồng lá vuốt sắc | Sử thi | 1219 格非 → 1220 利爪格非 | mới (dòng của Thanh Long cũ) |
| 50 | `tho_hoang` | Thỏ Hoàng | Chiến giáp hoàng cực | Sử thi | 2010 皇极兔 (siêu tiến hóa của dòng thỏ 1 → 3; 1 dạng) | mới |
| 60 | `moc_tinh` | Mộc Tinh | Thú giáp pha lê lục | Sử thi | 1480 木小诺 → 1481 木星诺 | mới |
| 70 | `thanh_long` | Thanh Long | Thần thú phương Đông | Huyền thoại | 214 青龙幼灵 → 215 青龙灵兽 → 1749 雷霆青龙 (hệ aola 15) | giữ id, đổi dòng |

- Thỏ Hoàng dùng rig `goc_2010`, cùng rig với Thiền Sư Pháp Luân (`monk_2010`, Hỏa, đã vẽ lại). Siêu tiến hóa sau của 2010 là 3295 传奇终结兔 → 3534; chưa lấy.
- Siêu tiến hóa chưa lấy: Phong Linh 2120 圣域·风灵将, Mộc Tinh 2408 超木星诺.
- Tướng Mộc cũ không có suất trên đảo (giữ trong danh sách, như Tám Tay của đảo Thủy): `mam_go` (quà ải 25 đảo Thủy), `nu_hoa` (tướng khởi đầu, thu phục ở ải 2 đảo Mộc), `kien_binh`, `banh_tet`, `giac_long`.

Lính đảo Mộc (dạng aola hệ Cỏ chưa có trong danh sách tướng):

| Lính | Bậc 1 | Bậc 2 | Vai |
|---|---|---|---|
| Bọ Sừng | 40 小角虫 | 41 木角虫 | trâu, như cua |
| Sâu Uốn / Rắn Gai | 58 扭扭 (con sâu) | 59 扭扭蛇 | phản đòn, như cá nóc |
| Chim Lá / Chim Lưu Ly | 82 木木鸟 | 83 琉璃鸟 | nhanh, như song ngư |

Danh sách Mộc cũ (2026-10-31), giữ để đối chiếu:

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
| `canh_cut` | Cánh Cụt | Đầu bếp xứ băng | Quái thường | Thường | 2 | mới; vẽ lại cả 2 dạng và viết lại animation (2026-11-06): cánh cụt mào tập sự bếp cầm chảo → bếp trưởng khay băng cá nướng có chim non phụ bếp; `reskin/thuy_1691`, `thuy_1692`, đã vào prefab |
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

### Hỏa (chọn lại 2026-11-05 theo 10 hình người dùng gửi)

Người dùng gửi 10 hình aola cho đảo Hỏa, thứ tự trái sang phải là thứ tự ải tướng (1, 5, 10, 15, 20, 30 … 70). Mỗi hình lấy cả dòng tiến hóa chứa nó. Tên, độ hiếm, thẻ là tạm; độ hiếm tăng theo ải như đảo Mộc.

| Ải | Id game | Tên | Danh hiệu | Độ hiếm | Nguồn (dạng 1 → 2 → 3) | Trạng thái |
|---|---|---|---|---|---|---|
| 1 | `su_tu_lua` | Sư Tử Lửa | Bờm lửa nhỏ | Khá | 4 吉拉 → 5 吉拉狮 → 6 爆焰吉拉 (hình gửi là dạng 3) | giữ, tướng khởi đầu |
| 5 | `khong_lo` | Khổng Lồ Lửa | Sừng lửa thân than | Thường | 46 火丁 → 47 火霍仔 → 48 火巨人 | mới |
| 10 | `kim_su` | Kim Sư | Bờm lửa giáp vàng | Khá | 581 火火狮 → 582 烈火狮 → 583 雷欧火狮 | mới |
| 15 | `nham_than` | Nham Thần | Chúa tể dung nham | Khá | 599 格纳 → 600 拉格纳 → 601 拉格纳罗斯 | mới |
| 20 | `nguu_quyen` | Ngưu Quyền | Quyền thủ mây lửa | Hiếm | 412 圈圈牛 → 413 火焰牛仔 → 414 火云牛斗士 | mới (2026-11-06): người dùng thay cho 501 魔焰吉拉 (siêu tiến hóa của chính dòng Sư Tử Lửa); tên dạng Nghé Lửa → Ngưu Lãng Tử → Ngưu Quyền |
| 30 | `hong_lien` | Hồng Liên | Cánh lửa sen đỏ | Hiếm | 776 炎 → 777 绯炎 → 778 红莲 (hệ aola 19) | mới |
| 40 | `giap_long` | Giáp Long | Gai thép lửa đỏ | Sử thi | 1231 鲁迪 → 1232 鲁曼 (hệ aola 16) | mới |
| 50 | `huyen_viem` | Huyễn Viêm | Hồ lửa ảo ảnh | Sử thi | 1295 灵炎 → 1296 幻炎 → 2091 圣域·幻炎 (hình gửi là siêu tiến hóa; người dùng chọn lấy 3 dạng) | mới |
| 60 | `hoa_tinh` | Hỏa Tinh | Thú giáp lửa hồng | Sử thi | 1466 火小诺 → 1467 火星诺 (như Mộc Tinh) | mới |
| 70 | `lan_hoa` | Lân Hỏa | Thần thú ngàn năm | Huyền thoại | 1449 小瑞兽 → 1450 千年瑞兽 → 2828 祥瑞圣兽 (siêu tiến hóa, hệ aola 27) | mới, boss tiến hóa |

- Tên dạng: Viên Than → Sừng Than → Khổng Lồ Lửa; Sư Con → Liệt Hỏa Sư → Kim Sư; Nham Con → Nham Hỏa → Nham Thần; Đốm Hồng → Phi Viêm → Hồng Liên; Giáp Long Con → Giáp Long; Linh Viêm → Huyễn Viêm → Thánh Huyễn Viêm; Tiểu Hỏa Tinh → Hỏa Tinh; Lân Con → Lân Ngàn Năm → Thánh Lân.
- Chỉ số gốc = 6 chỉ số aola của dạng 1 (`pmDataMap` cột 4–9), như đảo Mộc.
- Siêu tiến hóa chưa lấy: Hỏa Tinh 5329 烈焰奇迹-火星诺 (không có rig vector). Huyền thoại Hỏa theo Tứ Tượng trước là Chu Tước; nay boss đảo là Lân Hỏa theo hình người dùng gửi.
- Tướng Hỏa cũ không có suất trên đảo (giữ trong danh sách, như Tám Tay của đảo Thủy): `heo_lua`, `dom_lua`, `phao_tet`, `bo_de`, `ho_lua`, `phap_luan`, `chu_tuoc` (Hồ Lửa đứng tạm ở ải 20 tới 2026-11-06).
- Hình: 22 dạng mới và 6 lính đã vào Unity thành prefab (2026-11-05, xem `12_KeHoach_OpenSpec.md`, mục "Prefab tướng").

Lính đảo Hỏa (dạng aola hệ Lửa chưa có trong danh sách tướng; người dùng duyệt 2026-11-05):

| Lính | Bậc 1 | Bậc 2 | Vai |
|---|---|---|---|
| Lò Lửa / Lò Quái | 64 小火炉 | 65 火炉怪 | trâu, như cua |
| Nấm Lửa / Quái Nham | 13 炎蘑菇 | 14 熔炎怪 | phản đòn, như cá nóc |
| Khỉ Lửa / Khỉ Hỏa Diệm | 291 火耳猴 | 292 火焰猴 | nhanh, như song ngư |

Danh sách Hỏa cũ (2026-10-31), giữ để đối chiếu:

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

### Thổ (chọn lại 2026-11-06 theo 10 hình người dùng gửi)

Người dùng gửi 10 hình aola cho đảo Thổ, thứ tự trái sang phải là thứ tự ải tướng (1, 5, 10, 15, 20, 30 … 70). Mỗi hình lấy cả dòng tiến hóa chứa nó. Tên, độ hiếm, thẻ là tạm; độ hiếm tăng theo ải như đảo Kim. Kế hoạch ải: `Editor/IslandGen.cs`, `IslandGen.Tho`.

| Ải | Id game | Tên | Danh hiệu | Độ hiếm | Nguồn (dạng 1 → 2 → 3) | Trạng thái |
|---|---|---|---|---|---|---|
| 1 | `thach_nhan` | Thạch Nhân | Núi đá biết đi | Khá | 34 小石怪 → 35 隆咚石 → 36 震天石人 (hình gửi là dạng 3) | giữ, tướng khởi đầu |
| 5 | `lung_vuong` | Lửng Vương | Vua lửng vuốt vàng | Thường | 70 斯多鼠 → 71 斯多恩 → 72 斯多王 | mới |
| 10 | `cao_da` | Cáo Đá | Vuốt đá lục bảo | Khá | 458 亚斯 → 459 亚斯克 → 460 亚帝斯克 | mới |
| 15 | `ho_khoan` | Hổ Khoan | Sừng khoan pha lê | Khá | 485 吉祥虎 → 486 爆竹虎 → 487 尖钻虎王 | mới |
| 20 | `phu_van` | Phù Văn | Khổng lồ đá khắc chữ | Hiếm | 718 小岩兵 → 719 符文岩兵 → 720 符文泰坦 | mới |
| 30 | `hat_de` | Hạt Dẻ | Dũng sĩ khiên hạt dẻ | Hiếm | 927 小兵果果 → 928 勇士果果 | mới, bị động boss |
| 40 | `rua_nui` | Rùa Núi | Mai núi rừng xanh | Sử thi | 1203 石苗龟 → 1204 石峰龟 | mới |
| 50 | `ho_kim_cuong` | Hổ Kim Cương | Hổ vương giáp kim cương | Sử thi | 1380 金刚虎王 (1 dạng, siêu tiến hóa của 487) | mới, bị động boss |
| 60 | `cu_phu` | Cự Phủ | Chiến binh rìu tím | Sử thi | 1209 卡索 → 1210 巨斧卡索 | mới |
| 70 | `giap_nham` | Giáp Nham | Chiến thần giáp vàng | Huyền thoại | 1273 岩斗 → 1274 岩战 (aola gắn nhãn BOSS, hệ aola 1) | mới, boss tiến hóa |

- Tên dạng: Lửng Con → Lửng Võ Sĩ → Lửng Vương; Cáo Con → Cáo Đá → Cáo Đá Lục Bảo; Hổ Cát Tường → Hổ Pháo Hoa → Hổ Khoan Vương; Lính Đá Con → Lính Đá Phù Văn → Cự Thần Phù Văn; Lính Hạt Dẻ → Dũng Sĩ Hạt Dẻ; Rùa Mầm Đá → Rùa Núi; Phủ Con → Cự Phủ; Đấu Sĩ Nham → Giáp Nham.
- **Hình ải 1** (震天石人) là dạng 3 của Thạch Nhân, tướng khởi đầu hệ Thổ, nên Thạch Nhân giữ ải 1 như Sư Tử Lửa ở đảo Hỏa.
- **Hình ải 50** (金刚虎王, aola gắn nhãn siêu tiến hóa) là siêu tiến hóa của dòng Hổ Khoan ở ải 15 (`pmDataMap` cột 27 của 487). Tạm làm tướng riêng 1 dạng như Thỏ Hoàng ở đảo Mộc, chỉ số là 6 chỉ số của chính dạng đó; câu hỏi 30 ở `12_KeHoach_OpenSpec.md`.
- Chỉ số gốc = 6 chỉ số aola của dạng 1 (`pmDataMap` cột 4–9), như đảo Mộc, Hỏa, Kim.
- Thạch Nhân giữ tên ba dạng như cũ (cả ba đều tên Thạch Nhân).
- Tướng Thổ cũ không có suất trên đảo (giữ trong danh sách): `vo_su` (vẫn là quà ải 3 đảo Thủy), `gau_mo`, `soc_da`, `bo_hung`, `sa_than`, `ky_lan`, `ca_sa` (vẫn là tướng mốc huyền thoại `legendMilestoneHero`).
- Đo bằng máy tự chơi (đội Mộc Khá khắc hệ: Nụ Hoa, Dê Hoa; bằng cấp; 150 trận mỗi ải, 5 mốc cuối 300): cường hóa 92%, 2 địch 74%, 3 địch 85%, mini boss 64–67% (Hạt Dẻ 65, Rùa Núi 64, Hổ Kim Cương 66, Cự Phủ 67), boss Giáp Nham 59%.

Lính đảo Thổ (dạng aola hệ Đất chưa có trong danh sách tướng; Claude chọn, người dùng chưa duyệt):

| Lính | Bậc 1 | Bậc 2 | Vai |
|---|---|---|---|
| Chuột Khoan / Khoan Giáp | 1041 豆丁钻钻鼠 | 1042 重装钻钻鼠 | trâu, như cua |
| Đá Con / Đá Xích | 832 小石灵 | 833 岩锁灵 (dòng 3 dạng, lấy 2 dạng đầu) | dội đòn, như cá nóc |
| Ngựa Con / Ngựa Rằn | 297 迷你马 | 298 迷彩马 | nhanh, như song ngư |

Danh sách Thổ cũ (2026-10-31), giữ để đối chiếu:

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
