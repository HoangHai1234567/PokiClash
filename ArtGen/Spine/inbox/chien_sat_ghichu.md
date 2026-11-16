# Chiến binh sắt (`chien_sat`): tướng 2 đảo Kim

Bắt đầu 2026-11-16 (máy ổ C). Con gốc của rig: `monster_3348` (hiệp sĩ băng: mũ tròn kín, mào lông, khiên bông tuyết, giáo mũi tinh thể; game
tham khảo, kho `D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `skill_01_1`). Xương, lưới, chuyển động gốc là của nhà
phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là của mình. Suất 2 đảo Kim = ải 5, id game hiện là **`doc_giac`** (Độc
Giác Thép, 1 dạng). Mã làm việc `chien_sat`. Tên, số dạng: chưa đặt.

## 1. Lời dặn của người dùng (2026-11-16)

- "làm tướng thứ 2 đảo kim; **concept chiến binh sắt, bỏ icon bông tuyết đi**".
- "**idle / walk** có thể làm giống con gốc, sửa đi chút".
- appear: "làm nó **nhảy vào sàn đấu**".
- Đánh thường: "**dùng giáo đâm** đối thủ".
- Chiêu mana: "**ném giáo vào người** đối thủ".
- Chiêu cuối: "**dơ giáo lên triệu hồi các mũi kim sắt**, sau đó **dậm mạnh giáo xuống đất**, các mũi kim giáo lao vào người đối thủ (**làm
  animation người thôi, các mũi kim code làm**)".
- die: "làm **gục xuống**".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3348/`: `info.json`, `att_goc.json`, `att_idle0.json`, `khung/`, `mo/`, `parts/`)

43 xương, 24 slot (21 hình đang bật; `wuqi_02`, `wuqi_03` là hai bản sao giáo ẩn, cùng ảnh `wuqi_01`), 17 clip, 4 626 khoá. Ràng buộc: IK
`wuqi_02` (xương giáo `wuqi_01` theo đích `wuqi_04`), IK hai chân (`xiaotui_l_02`, `xiaotui_r_02`, bend −1), transform `dun_03`, `hujing_03`,
`st_05`… (mix âm, kéo mảnh theo thân). Con nhìn sang PHẢI. `_l` = bên GẦN (trái hình), `_r` = bên XA. Script mổ: `chien_sat.py` (`mo`, `nhom`,
`part_goc`; dùng lại hàm của `hoa_ho.py`). Tờ: `mo/idle0_0.jpg` (từng part), `mo/nhom_idle0.jpg` (theo nhóm), `parts/_tong.jpg`.

| thứ tự | slot | ảnh vùng (px) | đỉnh | là gì | xương |
|---|---|---|---|---|---|
| 0 | `datui_r_01` | 35×55 | 13 | đùi XA (đen, áo lót) | xiaotui_r_01 0,51 + datui_r_01 0,49 |
| 2 | `xiaotui_r_01` | 37×47 | 11 | ống chân + ủng XA | xiaotui_r_01 / _02 |
| 3 | `bozi_01` | 77×64 | 4 | cổ (bầu dục đen) | st_03 |
| 4 | `dabi_r_01` | 47×36 | 8 | bắp tay cầm giáo (đen) | dabi_r_01 |
| 5 | `datui_l_01` | 41×47 | 11 | đùi GẦN (đen) | datui_l_01 |
| 6 | `xiaotui_l_01` | 37×47 | 10 | ống chân + ủng GẦN | xiaotui_l_02 / _01 |
| 7 | `dang_01` | 36×35 | 4 | đũng (đen) | dang_01 |
| 8 | `hujian_r_01` | 51×43 | 4 | giáp vai bên giáo (viền trắng) | hujian_r_01 |
| 9 | `xiaobi_r_02` | 55×48 | 13 | cẳng tay + bao tay cầm giáo | xiaobi_r_02 |
| 10 | `xiaobi_r_01` | 20×35 | 4 | lòng bàn tay sau cán giáo | sizhi_01 |
| 11 | `wuqi_01` | 64×310 | 4 | GIÁO cả cây (mũi tinh thể, búp lông, cán, chuôi) | wuqi_01 (IK) |
| 14 | `guan_01` | 122×130 | 22 | MÀO lông cong (trắng / lam) | guan_01..04 + hujing_03/04 |
| 15 | `tou_01` | 111×122 | 30 | khối cầu sau mũ (lam sẫm) | hujing_01 0,94 |
| 16 | `sizhi_01` | 31×39 | 4 | ngón tay trước cán giáo | sizhi_02 |
| 17 | `damz_01` | 20×19 | 4 | ngón cái | damz_01 |
| 18 | `qunbai_01` | 92×48 | 23 | váy giáp ngắn | st_01 / qunbai_01 / st_04 / st_02 |
| 19 | `st_01` | 78×65 | 23 | giáp ngực | st_03 0,60 + st_02 0,34 |
| 20 | `hujian_l_01` | 63×57 | 4 | giáp vai bên khiên | hujian_l_01 |
| 21 | `qizi_01` | 58×97 | 24 | VẠT ÁO (cờ) có bông tuyết, chuỗi xương | qizi_01..03 + st_06 |
| 22 | `hujing_01` | 153×119 | 30 | MẶT NẠ mũ (khe xanh băng) + đĩa tròn bên trái | hujing_02 0,93 |
| 23 | `dun_01` | 144×184 | 28 | KHIÊN (bông tuyết, dải kính trên) | dun_02 0,91 |

Clip của họ (tờ `khung/`):
| clip | dài | động tác | dùng cho (dự kiến) |
|---|---|---|---|
| `idle_01` | 3,73 | thở, mào đung đưa | **idle** |
| `run_01` | 0,67 | chạy | **walk** |
| `skill_01_1` | 1,00 | thu giáo, ĐÂM NGANG tới (0,22–0,33), rút về | **attack** |
| `skill_01_2` | 1,00 | xoay giáo, ngả người, GIƠ GIÁO lên cao (0,44) | nguồn dáng giơ giáo (chiêu cuối, ném) |
| `skill_01_3` | 1,00 | vung giáo qua đầu, bổ xuống | nguồn dáng ném |
| `skill_02` | 1,20 | KHIÊN giơ lên đầu, giáo CẮM xuống đất trước mặt (0,40–0,93) | **skill** (đoạn dậm giáo) |
| `open_01` | 2,23 | bật lên cao (giáo ẩn), lộn, đáp xuống, cầm giáo | **appear** (nhảy vào sàn) |
| `die_01` | 1,00 | lảo đảo, đổ sấp, khiên úp | **die** |
| `hit_01`, `hit_02`, `block_01`, `stun_01`, `floating_01`, `liedown_01`, `standup_*`, `salute_01` | | | **hit** = hit_01 |

## 3. Concept (Claude đề xuất ba hướng, CHỜ người dùng chọn)

Gói `gui_gpt/chien_sat_1/` (`chien_sat_da.py ca_con`, `concept`). Ảnh mẫu 1 = hình cả con gốc `mau/goc_ca_con.png` (khung 0 idle, 1,918 px /
đơn vị; khung bao từng part trong `.json`); ảnh 2 = concept Quỷ lửa bắn cung (nét, cách tô giáp); ảnh 3 = tinh linh tinh thể sắt (tướng 1 đảo
Kim). Giữ dáng, chỗ, cỡ từng mảnh; bỏ bông tuyết ở khiên và vạt áo.
- `tai_ve/L1_A.png` **thép xám + đỏ thẫm** (giữ hình bóng mọi mảnh): mào chùm lông ngựa đỏ cùng dáng quạt, khiên thép núm sắt 4 đinh, vạt đỏ trơn,
  mũi giáo sắt hình lá, tua đỏ, khe mặt nạ tối.
- `tai_ve/L1_B.png` **gang sẫm + đồng thau**: mào ĐỔI DÁNG thành ba bản thép cong xếp lớp; khiên gang viền đồng, mũi giáo đồng nổi giữa; vạt xanh
  than; khe hổ phách.
- `tai_ve/L1_C.png` **bạc sáng + đồng đỏ**: mào ĐỔI DÁNG thành chùm 5 kim sắt xoè quạt (gợi chiêu kim sắt); khiên sắt sẫm, ba kim bạc xoè; vạt
  đồng đỏ; khe tối.

Ba ảnh đã về, đạt lượt đầu. Soát: hình bóng mọi mảnh (trừ mào B, C) trùng con gốc, chỉ dày hơn bằng nét mực (`chien_sat_1/mau/_so_goc.png`; IoU
mặt nạ ~0,80 là do bông tuyết, vạt áo trắng của con gốc bị tính là nền); hai chân, tay cầm giáo dính thân; không còn bông tuyết; tô phẳng. Mào C xoè
rộng hơn mào gốc sang trái (mảnh lưới 4 xương, gắn kiểu `gan_goc` được). Trang xem: `inbox/chien_sat_xem_concept.html`.

**Người dùng chọn A** (2026-11-16) → `tai_ve/L1_duyet.png`.

## 4. Đổi da theo khung part + rig (2026-11-16)

- `chien_sat_da.py to`: hai tờ MẢNH GỐC cắt theo lưới (`mau/goc_A.png`: mào, mặt nạ + đĩa, vòm sau mũ, khiên, vạt áo, giáo NẰM NGANG mũi chĩa
  phải; `mau/goc_B.png`: ngực, váy giáp, hai giáp vai, cẳng tay, hai ống chân, hai đùi, đũng, bắp tay, cổ, ba mảnh bàn tay phóng 5,5) + prompt
  `gui_gpt/chien_sat_1/luot_2_da_A.txt`, `_B.txt` (màu đo trên concept A). Codex đạt lượt đầu (`tai_ve/D_A.png`, `D_B.png`, ~100 s mỗi tờ).
- `chien_sat_da.py cat`: cắt theo ô (giáo xoay lại), độ khớp hình bóng 0,89–0,98 (`manh/_so_A.png`, `_so_B.png`; đo trên hình gốc LẤP KÍN, vì
  bông tuyết / khung trắng của con gốc trùng màu nền); vá chỗ hụt CHỈ sát mép (5 px), không vá cả vùng (tua giáo cố ý hẹp hơn búp lông cũ).
- `chien_sat_rig.py` (mẫu `cung_lua_rig.py`): 48 xương (43 của họ + `move`, `mui_giao`, `far`, `fly_0`, `ten_0`), 28 slot (21 của họ + 4 bản `_t`
  bàn tay trước mặt nạ cho open_01 + `wuqi_02/03` + `giao_bay`), 315 đỉnh, NGUYÊN lưới của họ. Dựng thử bằng da gốc (`CS_GOC=1` → `rig_goc/`)
  trùng con gốc. `.atomik` 185 KB, chiều cao game 402, mọi clip nối về idle 0 px, không bước góc nào gần 360° ở 60 khung/giây (lớn nhất 65°: bắp
  tay lúc đâm, đúng nhịp của họ).
- **Hai cây giáo của con gốc**: `wuqi_01` dựng đất (xương gốc, IK) chỉ dùng ở idle / block / stun; MỌI clip đòn dùng `wuqi_02` gắn tay (xương
  `wuqi_03` con của nắm tay `sizhi_01`). Hai cây trùng nhau ở khung 0 idle (lệch 0,2 px). Bước hoà 0,2 s cuối về idle phải ĐỔI BẬC hai slot này
  ở khung cuối (trộn độ đậm thì hiện hai cây giáo mờ chồng nhau): làm trong `main()` của rig, không sửa `hoat.khop_cuoi` dùng chung.
- Clip:
  | clip | dài | cách làm |
  |---|---|---|
  | idle | 3,73 | idle_01 + mào lông lay thêm (2 nhịp / vòng, trễ pha) |
  | walk | 0,67 | run_01 (cầm giáo chĩa tới chạy) + mào lay |
  | hit | 0,50 | hit_01 |
  | attack | 1,00 | skill_01_1 (thu giáo, đâm) + lao tới 0,55 chiều cao, đỉnh lao = khung mũi giáo xa nhất; `dam` 0,40, `trung` 0,43 |
  | cast | 1,60 | ném giáo: lấy đà chậm (dáng thu giáo, ngả ra sau, tay giơ cao, giáo đặt góc thế giới 22°), run, phóng; `nem` 0,90 giáo gắn tay tắt, `giao_bay` (neo 62 % thân giáo) bay tới `far` trong 0,2 s (game co quãng, `farAim` xoay theo hướng bay), `trung` 1,11; tay không về thế; `moc` 1,22 giáo mọc lại trong tay (nở vượt nhẹ) |
  | skill | 2,45 | `giuong` → giơ giáo dựng cao (skill_01_2 0,44 s) 0,42; giữ, run, `trieu_hoi` 0,42 (VFX sinh kim sắt trên đầu); nhón lấy đà 1,25–1,42; DẬM giáo cắm đất (skill_02 0,45 s, khiên giữ trước người thay vì giơ lên đầu) `dam_dat` 1,52, thụp người, mào giật; `phong_kim` 1,58 (code phóng kim); `trung` 1,82; về thế |
  | appear | 1,55 | open_01 đoạn bay (lộn trên không) + dời từ ngoài trái vào, cầm giáo giơ chếch lên suốt lúc bay, `dap_dat` 0,95, đứng vào thế |
  | die | 1,45 | die_01 (lảo đảo, đổ sấp, khiên úp) + mờ dần 0,32 s cuối; `nga` 0,70 |
- Xương cho VFX: `mui_giao` (mũi giáo gắn tay: chỗ gọi kim lúc giơ, chỗ cắm đất lúc dậm), `far` (tâm đối thủ), `fly_0`/`ten_0` (giáo bay).
  Impact: attack (0,05; 0,25; 0,07), skill (0,22; 1,0; 0,18; chớp `#e8eef666`).
- Soi: `rig/khung_*.png`, runtime thật `rig/that/*.jpg`, cận khớp `rig/can/*.jpg`; trang xem `rig/xem.html`.

## 5. Việc tiếp

1. (xong) Người dùng xem trang xem: "OK ỔN, làm dạng 2 của tướng này" (2026-11-16).
2. Hỏi: thay suất `doc_giac` (Độc Giác Thép, 1 dạng)? tên, số dạng (có làm dạng non trên cùng rig không)?
3. Vào game: VFX kim sắt của chiêu cuối (sinh quanh / trên đầu theo `trieu_hoi`, lao vào đối thủ theo `phong_kim`, nổ mảnh sắt khi trúng), vệt
   đâm, chớp mọc giáo; heroes.json, menu Unity.

## 6. Dạng 2 (dạng tiến hóa), 2026-11-16

- Cùng rig, cùng clip: `CS_DANG=2 py -3 -I ArtGen/Spine/chien_sat_rig.py ...` (tên xuất `chien_sat_2`, thư mục `inbox/chien_sat_2/`: `mau`, `tai_ve`,
  `manh`, `rig`). `TI_LE`: `hujing_01` × 0,82 (cả mũ, gốc ở cổ: bớt chibi), `guan_01` × 1,32 (mào, tính trên mũ đã thu: thật ~1,08 so dạng 1),
  `hujian_l_01`, `hujian_r_01` × 1,6 (giáp vai; bị khiên và tay che gần hết nên phần "khác hẳn" phải nằm ở thiết kế). Không đụng chân, tay,
  khiên, giáo: chân chạm đất; giáo dựng đất phải trùng giáo gắn tay ở khung 0 idle.
- Bố cục: `mau/bo_cuc.png` (`chien_sat_rig.py bo_cuc`, da dạng 1), `mau/bo_cuc_khung.png` (đặt vào khung 1536 × 1024).
- Concept: `py -3 -I ArtGen/Spine/chien_sat_da.py concept2` → `gui_gpt/chien_sat_2/luot_1_concept_<A|B|C>.txt` → `tai_ve/L1_<A|B|C>.png`:
  A thép đen + vàng + đỏ thẫm (mào hai lớp, khe hổ phách, vai một gai, khiên núm gai, giáo hai cánh); B thép xám thẫm + bạc + đỏ (cánh thép trên
  mũ thay đĩa tròn, vai hai lớp, khiên núm + bốn đinh, giáo dài to bản); C gang xanh + đồng thau + đỏ (sống thép trên đỉnh mũ, vai hai gai, khiên
  mép trên ba mấu, giáo có ngạnh). Phần thêm (gai, cánh, sống, mũi giáo to) sẽ là mảnh cứng / khung nới trên đúng xương mảnh nó gắn.
- Ba ảnh đạt lượt đầu (`chien_sat_2/tai_ve/L1_A|B|C.png`). Khớp bố cục rig (`chien_sat_2/mau/_so_bo_cuc.png`): IoU A 0,80 (lớp mào đen lấn
  rộng sang trái + gai vai to), B 0,92, C 0,91; thân, khiên, chân, tay cầm giáo trùng chỗ; cả ba vẽ mũi giáo to và dài hơn (khung giáo phải
  nới lên). Trang xem: `inbox/chien_sat_2_xem_concept.html`.
- **Người dùng chọn B** (2026-11-16) → `chien_sat_2/tai_ve/L1_duyet.png`.

### 6b. Mảnh + rig dạng 2 (concept B)

- `py -3 -I ArtGen/Spine/chien_sat_da2.py to` / `cat` (màu đo trên concept B: thép #777A82 / #5E6068, viền bạc #C8CAD0, đỏ #BF2F3A / #95252C):
  - tờ A2, B2: tờ hướng dẫn = CHÍNH mảnh dạng 1 đã xong (`chien_sat_1/manh/`) xếp đúng ô; Codex đổi da + thêm viền bạc, núm gai và bốn đinh
    trên khiên. Độ khớp 0,94–0,99.
  - lượt W1 (cánh thép bên trái mũ + cả cây giáo) và W2 (giáp vai gần hai lớp): gen "đúng chỗ, đúng cỡ" từ concept B, vẽ đủ phần khuất;
    `manh/moi.json` ghi khung trên concept.
  - giữ nguyên ảnh dạng 1: đùi, đũng, bắp tay, cổ, cẳng tay quấn đỏ.
- `chien_sat_rig.py` (`CS_DANG=2`): mảnh cứng mới đặt bằng toạ độ concept → thế giới khung 0 idle (qua `mau/bo_cuc.json`: box + tỉ lệ của
  hình bố cục, rồi phép đặt vào khung 1536 × 1024). Giáo mới căn theo TRỤC + CHUÔI của giáo cũ (không phụ thuộc GPT lệch vài px), dùng cho cả
  ba slot giáo và giáo bay; `mui_giao` dời tới mũi mới. Cánh mũ: slot `canh_mu` sau vòm sau mũ, bám `hujing_02`. Giáp vai gần: concept vẽ nó
  đè lên chỗ dải trên của khiên (dải đó thuộc ảnh khiên, vẽ trước vai) → nâng `NANG_VAI` cho đỉnh nhô quá mép khiên 26 đơn vị (nâng 30,9).
  Ra `chien_sat_2/rig/`: 48 xương, 29 slot, 319 đỉnh, `.atomik` 200 KB, chiều cao game 385; mọi clip nối idle 0 px. Impact mạnh hơn dạng 1:
  attack (0,06; 0,32; 0,08), skill (0,26; 1,25; 0,2; chớp `#f2f4f888`). So khung 0 idle với concept: `chien_sat_2/mau/_ghep_canh_concept.png`.
- **Tiến hóa** (rig dạng 1 gộp dạng 2, `quai/tienhoa.py`; dạng 2 dựng ở tiến trình riêng bằng lệnh `nhe`, ghi kèm khung chiêu cuối dạng 2):
  clip `evolve` 2,8 s: dạng 1 giơ giáo lên trời (động tác giơ của chiêu cuối), gồng run mạnh dần, mào giật; `doi_dang` 1,2 (hai dạng hoà
  1,05–1,45, VFX của game che); dạng 2 hiện đúng dáng giơ giáo của chiêu cuối dạng 2, nhón rồi DẬM giáo (`gam` 1,86), giữ, hoà về khung 0
  idle dạng 2 (lệch 0 px). Độ đậm giáo trong evolve ép lại sau khi nướng: giáo gắn tay suốt clip, đổi sang giáo dựng đất ở khung cuối.
  Rig dạng 1 gộp: 96 xương, 57 slot, `.atomik` 337 KB (6 / 22 ảnh dùng chung). Dạng 2 trong rig gộp co 1,044 (402 / 385).
- Trang xem: `chien_sat_1/rig/xem.html` (dạng 1 + evolve), `chien_sat_2/rig/xem.html` (dạng 2).

## 7. Vào game (2026-11-16, người dùng: "ok cho vào game đi")

- **Suất**: tướng 2 đảo Kim = id `doc_giac` (ải 5, "Cầu Bánh Răng"). Giữ id, chỉ số, hiệu ứng thẻ, số mảnh. Số dạng 1 → 2 (ải tướng thành boss
  tiến hóa) nên phải sinh lại ải + tính lại golden trong Unity. Script dữ liệu `quai/doi_chien_sat.py` (dùng hàm của `doi_phap_lua.py`):
  tên "Thiết Vệ", danh hiệu "Chiến binh sắt khiên giáo", dòng "Dòng Thiết Vệ"; dạng "Thiết Vệ Nhi" `chien_sat_1` 0,92 / "Thiết Vệ"
  `chien_sat_2` 1,1; thẻ Sừng Bạc → **Phóng Giáo** (trident), Phi Mã Xung Trận → **Vạn Kim Sắt** (fang), Giáp Kỵ → **Khiên Thép** (shield).
  **Tên do Claude tạm đặt, chờ người dùng chốt.** `chep`: Resources/chien_sat_1 (rig dạng 1 đã gộp dạng 2 + evolve), chien_sat_2. Không đè
  Resources/doc_giac_1 cũ.
- **Hiệu ứng** (`Assets/01 Script/Game/Battle/HatGiao.cs`, đi đường "n_"): `StageView.KimFx["doc_giac"]` = mana (`n_giao_nem1`,
  `n_giao_nem`), chiêu cuối (`n_kim_sat1` 7 kim, `n_kim_sat` 11 kim); `KimAtk["doc_giac"]` = `n_giao_dam`; `HatVoi.AtkLao` nhận `n_giao_dam`;
  `HatNuoc.PlayNuoc` thêm 5 case, `HoldNuoc` giữ dáng chiêu cuối 0,3 / 0,25 s; `HatLua.Themes["doc_giac"]` tia bạc trắng, mảnh giáp thép.
  Kim sắt vẽ bằng ảnh `needle_0` / `needles_0` sẵn có (viền mực + thân thép + sống bạc). Mốc chiêu cuối theo giờ trúng của clip: hiện lúc
  0,42 / 1,82 lead, dậm đất lead − 0,30, phóng lead − 0,24 (kim đầu chạm đúng lead).
- Biên dịch thử cả assembly Game bằng csc của Unity với bản sửa nằm ngoài Assets (`scratchpad/cs_thu.py`): 0 lỗi. Chèn vào Assets bằng
  `scratchpad/cs_sua.py --that` (chỉ chèn dòng, chạy lại không chèn trùng) SAU khi Unity dừng Play (phiên assets-96 đang chạy tour Thiết Tinh).
- **Đã chạy trong Unity** (phiên assets-96 ghép Thiết Tinh xong thì giao Unity): chèn C# (`cs_sua.py --that`) + `HatGiao.cs`, Nhập dữ liệu
  (88 tướng, 265 thẻ riêng, 350 ải), Gắn dạng .atomik (prefab `04 Prefabs/Heroes/doc_giac.prefab` giữ 2 dạng `chien_sat_1` 9 clip có
  `evolve`, `chien_sat_2` 8 clip), Đảo 70 ải sinh lại, 3 menu golden + `golden_ghep.py`. Golden đổi: islands (ải 5 Kim `evo` true), roster
  (`doc_giac` n 1 → 2, ngưỡng sao, star dẫn đầu), sim (ô kim 145). EditMode 106 / 107 (chỉ hỏng `PrefabOnlyTests` cũ ở `UI/Kit`).
- **Soi trong trận**: menu "PokiClash/Thử/Đảo Kim: riêng Thiết Vệ (dạng 2) / Thiết Vệ Nhi (dạng 1)…" (`Editor/KimFxTour.cs`), ảnh
  `Temp/PokiShots/kim_fx/doc_giac_<1|5>sao_*.jpg`, tờ chép ở `inbox/chien_sat_1/trong_game/`. Đâm: lao tới, chớp sắt chỗ mũi giáo. Ném: giáo bay
  chếch lên theo đúng hướng tới đối thủ (đối thủ đứng cao hơn trên sân), găm nổ, giáo mọc lại trong tay. Chiêu cuối: hai bản kim đầu bị loại
  khi soi: (1) ảnh `needle_0` là giọt nhọn chỉ chiếm 27 % bề ngang khung ảnh → kim thành vệt mảnh; (2) xếp ngang trên đầu mà cùng chĩa về
  đối thủ thì chồng thành dải xám như khói; xếp cột dọc sau lưng thì đè lên mũ, mào. Bản giữ: QUẠT kim xoè quanh tâm sau đầu, cao hơn đỉnh
  mào, mũi chĩa ra ngoài; lúc phóng mỗi kim lùi lấy đà và xoay mũi về đích rồi lao; chỗ găm theo độ cao của kim.
