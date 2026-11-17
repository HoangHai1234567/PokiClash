# Năm tướng đầu đảo Thổ trên rig game tham khảo (`tho5`)

Bắt đầu 2026-11-17 (máy ổ C, kho `D:\Ripper\SwordxStaff`). Người dùng: "trong bể tướng sword x staff, chọn ra 5 con làm 5 tướng đầu tiên cho
đảo thổ, tướng càng về sau nhìn càng chiến, 5 con cuối tôi tự chọn, phải liên quan đến hệ đất". Claude chọn, người dùng duyệt ("5 con bạn
chọn ổn rồi, lên concept reskin đi, sau đó animation tôi mô tả sau"). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola):
dùng nội bộ, không đăng công khai. Hình là của mình.

Suất đảo Thổ hiện (`IslandGen.Tho`): ải 1 `thach_nhan`, ải 5 `lung_vuong`, ải 10 `cao_da`, ải 15 `ho_khoan`, ải 20 `phu_van`. Chưa bàn thay id,
tên, số dạng; mã dưới đây chỉ là mã làm việc.

| Suất | Ải | Mã làm việc | Con gốc | Là gì | Rig |
|---|---|---|---|---|---|
| 1 | 1 | `cong_da` | `monster_3378` | thú nhỏ tròn cõng khối pha lê, mày cau | 18 hình idle; thân một lưới (body/head/hip), khối pha lê `hair1..5`, hai tấm mày `mml`/`mmr`, mi `yp1/2`, miệng `mt1` đều CỨNG một xương (đổi dáng tự do) |
| 2 | 5 | `than_lan_cat` | `monster_3257` | thằn lằn sừng ngồi rạp, diềm ba tấm | 40 xương, 23 slot, 10 clip; diềm `P_qi01..03` + gai cằm `P_qi04` cứng (bone7..10); atlas nhỏ, ảnh mờ khi phóng |
| 3 | 10 | `thu_da` | `monster_3525` | thú đá hàm to, gai dáng lửa trên lưng | 50 xương, 36 slot, 14 clip; bảy gai (`beijiao1..4`, `jiao1..3`) + `hair1` cứng một xương; hàm `mt1`, lưỡi `shetou` |
| 4 | 15 | `rong_cat` | `monster_3424` | rồng cúi rạp sắp vồ, đá nhọn trên lưng | 56 xương, 40 slot, 10 clip; đá lưng `P_shitou0..6` con của thân (bone4/5), mào `P_qi07..12` + sừng `P_jian01..03` cứng trên đầu; tay GẦN là `P_shoubi01` + `P_shouzhang01` (giữa trái, vẽ trước thân), tay XA `P_shouzhang02` (bên phải, vẽ sau cùng) |
| 5 | 20 | `quy_nui` | `monster_3612` | golem bốn tay nhìn thẳng, một mắt, hai sừng | 52 hình; tay phụ `jixieshouL/R*` con của ngực (bone12), đầu `tou` (bone14), khố `weiqun`, bốn dải `piaodai1..4` |

Mổ: `<SXS>/scan/monster_<số>/info.json`, `att_goc.json`, `att_idle0.json` (chay.py info / att). Ảnh cả con gốc khung 0 idle:
`inbox/<mã>_1/mau/goc_ca_con.png` (`tho5.py ca_con`). Đã so khung xương với các rig đã dùng (Jaccard tên ≤ 0,13): không trùng rig nào.
Không lấy `monster_3421` (golem đá) vì ba đảo đã có kiểu golem; dự phòng: 3380 (cùng rig 3378, màu vàng), 3256, 3459, 3454, 3421.

## Concept lượt 1 (Claude đề xuất hai hướng mỗi con; chờ người dùng chọn)

Script `tho5.py` (ca_con, slot, concept, so_goc, xem), mô tả và hướng ở `tho5_huong.py`. Gói `gui_gpt/<mã>_1/luot_1_concept_<A|B>.txt` +
`HUONG_DAN.md`; ảnh về `inbox/<mã>_1/tai_ve/L1_<k>.png`. Ảnh mẫu 2–3 là tướng đã duyệt (golem lửa, rùa lửa, Thiết Tinh, hươu gỗ, đất nung)
chỉ để lấy nét. Tông đảo: đất, sa thạch, đất son, đất nung, pha lê hổ phách; tránh dung nham phát sáng (Hỏa), kim loại (Kim), rêu (Mộc).
Mọi hướng giữ dáng, chỗ, cỡ từng mảnh; đổi dáng mảnh nhận diện (khối trên lưng, diềm, gai, mào, đầu, sừng).

| Mã | A | B |
|---|---|---|
| `cong_da` | chũi lông nâu đất cõng TẢNG ĐÁ TRÒN hoa cương, khe hổ phách; sỏi tròn; sừng mày đá ngắn | thú đất nung đỏ cõng THÁP BA PHIẾN SA THẠCH; mảnh sa thạch dẹt; gai tai nhọn |
| `than_lan_cat` | thằn lằn vàng cát, diềm BA PHIẾN SA THẠCH mép vỡ thẳng; mắt hổ phách | thằn lằn đỏ đất nung, VƯƠNG MIỆN NĂM GAI THẠCH NHŨ; mắt vàng |
| `thu_da` | sa thạch nâu, gai thành MŨI PHA LÊ HỔ PHÁCH thẳng cạnh; hàm kem năm răng; hai sừng đá kem | đất son vàng vằn nâu, gai thành PHIẾN ĐÁ PHIẾN XÁM đầu tròn |
| `rong_cat` | vàng cát vằn nâu, đá lưng thành CỘT SA THẠCH, mào bốn vây đá, sừng hổ phách | đỏ nâu hẻm núi, CỘT BAZAN sáu cạnh, mào ba lưỡi đá, sừng ngà |
| `quy_nui` | titan hoa cương, LÕI NGỰC PHA LÊ HỔ PHÁCH, đầu đá như đỉnh núi một mắt, sừng đá kem | đất nâu sẫm vằn vàng son, đầu MŨ ĐÁ HÌNH ĐẦU BÒ một mắt, sừng ngà |

Trang so: `inbox/tho5_xem_concept.html` (`tho5.py xem`); độ khớp hình bóng `tho5.py so_goc <mã>` → `mau/_so_goc.png`.

Codex đạt lượt đầu cả 10 ảnh (78–162 s mỗi ảnh, 2026-11-17 09:58–10:15). IoU hình bóng với con gốc: `cong_da` A 0,886 / B 0,915;
`than_lan_cat` A 0,878 / B 0,865; `thu_da` A 0,862 / B 0,816; `rong_cat` A 0,878 / B 0,905; `quy_nui` A 0,826 / B 0,913. Claude soi: mọi chi
dính thân, đúng hướng con gốc. Lưu ý khi đưa duyệt: `than_lan_cat` A diềm đá lẫn vằn đầu (khó đọc thành ba phiến); `quy_nui` A mắt lim dim
(kém dữ hơn B); `thu_da` B u đầu thành núm đá xám giống phiến lưng; `than_lan_cat` B vẽ bảy gai thay vì năm.

**Người dùng TRẢ cả lượt A, B** (2026-11-17): "tướng thứ 2 ảnh bị lỗi rồi, ngoài ra ảnh bạn gen ra bị giống con gốc quá, tự lên concept gần
giống thôi".
- Lỗi tướng 2 là ảnh CON GỐC mình dựng sai: `hoa_ho.luoi` (và `mo_xe/to_manh.py` dòng ~117) đổi chỗ rộng / cao với hình REGION xoay 90° trong
  atlas, trong khi atlas Spine 4 ghi `bounds` theo cỡ CHƯA xoay và `to_manh.nap` đã gỡ xoay ảnh → mắt `P_yanjing01` của `monster_3257` bẹp
  thành một khe dẹt, concept vẽ theo cái mắt hỏng đó. Sửa riêng trong `tho5.luoi_sua` (không đụng `hoa_ho` dùng chung); dựng lại `goc_ca_con`
  đúng như trang xem (hai mắt to tròng đỏ). Bốn con kia không có hình region xoay 90°. Con nào khác dùng `hoa_ho.luoi` mà có region xoay 90°
  cũng dính lỗi này (chưa soát).
- "Giống con gốc quá": lượt A, B giữ nguyên hình bóng mọi mảnh (IoU 0,82–0,92), chỉ đổi màu và mảnh nhô ra.

## Concept lượt 1, hướng C và D (tự thiết kế, chỉ gần giống con gốc)

`tho5.py concept2`, nội dung ở `tho5_huong2.py`. Ảnh 1 chỉ còn là mẫu DÁNG và BỐ CỤC CHI ("use it ONLY for the pose and the body plan");
thân và chân giữ cỡ gần như cũ (để còn lắp lên lưới của rig), còn đầu, mặt, mảnh lưng, sừng, diềm, mào là thiết kế mới; prompt cấm rõ các nét
nhận diện cũ (khối lục giác, tấm mày, màng diềm hồng, gai dáng lửa, một mắt hốc thoi, sừng bò).

| Mã | C | D |
|---|---|---|
| `cong_da` | TATU con, mai đá bốn tấm, hốc đá vỡ lộ cụm hổ phách | CHUỘT CHŨI vuốt đào, lưng xoè bảy gai đá như nhím |
| `than_lan_cat` | thằn lằn sừng: mõm rõ, vương miện sáu sừng đá, cổ áo ngắn ba phiến | thằn lằn giáp: mày giáp đá, ÁO CHOÀNG phiến đất nung dựng như mũ trùm |
| `thu_da` | CHÓ LỬNG ĐẤT hai nanh vểnh, mặt nạ vằn, sống lưng năm tảng sa thạch | CÓC TÊ GIÁC một sừng đá trên mõm, ba cụm pha lê hổ phách trên lưng |
| `rong_cat` | rồng ĐÀO CÁT sừng xẻng trên mõm, lưng phiến sa thạch như núi bàn | rồng GIÁP ĐÁ vai và sống lưng, hai sừng dài vuốt sau, sừng mũi hổ phách |
| `quy_nui` | VƯỢN NÚI ĐÁ bốn tay, mặt khỉ đột hai mắt, vương miện gai đá, mạch hổ phách | QUỶ ĐẤT sừng cừu xoắn, da đất cơ bắp, giáp sa thạch vai và nắm đấm |

Codex đạt lượt đầu cả 10 (65–101 s, 10:24–10:39). IoU hình bóng với con gốc (thấp hơn lượt A, B là đúng ý): `cong_da` C 0,846 / D 0,764;
`than_lan_cat` C 0,808 / D 0,799; `thu_da` C 0,641 / D 0,706; `rong_cat` C 0,773 / D 0,707; `quy_nui` C 0,631 / D 0,686. Claude soi: đúng
dáng, đúng hướng, mọi chi dính thân, nhìn ra con khác. `thu_da` C (thân gấu dài hơn) và `quy_nui` C, D (vai, nắm đấm to hơn) lệch tỉ lệ thân
nhiều nhất: lúc chia mảnh phải nắn về khung part của rig (hoặc đổi tỉ lệ xương), nói trước với người dùng.

**Người dùng chọn (2026-11-17): 1C 2D 3D 4D 5C** → `tai_ve/L1_duyet.png` mỗi con:
- `cong_da` C: tatu con, mai đá bốn tấm, cụm hổ phách trên đỉnh;
- `than_lan_cat` D: thằn lằn mũ giáp đá, áo choàng phiến đất nung;
- `thu_da` D: cóc tê giác đất nung, sừng đá trên mõm, ba cụm pha lê hổ phách;
- `rong_cat` D: rồng giáp sa thạch, hai sừng dài vuốt sau, sừng mũi hổ phách;
- `quy_nui` C: vượn núi đá bốn tay mặt khỉ đột, vương miện gai đá, mạch hổ phách chéo ngực (lệch tỉ lệ rig nhiều: vai, nắm đấm to hơn).

## Đề xuất animation (Claude, 2026-11-17; CHỜ người dùng duyệt)

Người dùng: "bạn dựa vào bộ skill anim và vfx, thử tự sáng tạo xem các animation cần thiết dựa trên con gốc". Nội dung đầy đủ (dài, nguồn,
diễn, VFX, ghi chú rig) ở `tho5_anim.py`; trang so concept + tờ khung clip gốc cạnh từng clip: `inbox/tho5_xem_anim.html`. Tờ khung clip gốc:
`<SXS>/scan/monster_<số>/khung/` (3612: `khung5/`).

Clip gốc đọc được: 3378 `skill_01_1` húc đầu văng khối nhỏ, `skill_02` bật nhảy khối bay quanh rồi đáp; 3257 `skill_01` chồm đớp thè lưỡi,
`skill_02` xoè diềm há miệng dọa; 3525 `skill_01_1` chồm giáng cằm, `skill_02_1` há hàm, `skill_03` cuộn tròn (đổi ảnh quả cầu mờ) bật lên nện;
3424 `skill_01` đứng lên chém vuốt, `skill_02` dang tay lao rạp hai vuốt, `skill_03` giơ hai tay nện đất (đá lưng bật ra 0,74 s); 3612
`skill_01` liên hoàn đấm bốn tay 2,17 s, `skill_02` hai nắm đấm quá đầu nện đất, `skill_03` nhảy xoay nện, `skill_04` lao húc rồi móc lên.

| Ải | Đánh thường | Chiêu mana | Chiêu cuối | Vào sân |
|---|---|---|---|---|
| 1 tatu | húc đầu | lắc mai văng chùm sỏi | rụt mai gồng, bắn pha lê lên trời, MƯA PHA LÊ hổ phách | mai rơi nảy, chân mõm bật ra |
| 5 thằn lằn | chồm đớp | ba phiến áo choàng bay găm rồi về lắp (code lái) | dậm, LỐC CÁT trùm đối thủ | bấu mép gò cát trồi lên |
| 10 cóc tê giác | giáng sừng | phun tảng đá | cuộn tròn LĂN NỆN (ảnh cuộn tròn riêng) | lăn vào cuộn tròn, bung ra |
| 15 rồng | chém vuốt | ba lưỡi cát trăng khuyết | nện đất, CỘT SA THẠCH trồi ba nhịp | vuốt bấu đất trồi lên, gầm |
| 20 vượn | liên hoàn ba đấm | nện đất, sóng chấn | tụ TẢNG ĐÁ KHỔNG LỒ, bốn tay ném | nhảy xuống nện đất, đấm ngực bốn tay |

Idle mỗi con một trò: hắt xì bụi, liếm mắt, túi họng + khịt bụi, cào đất, gãi đầu bằng tay phụ. Chưa có bộ hạt Thổ riêng: dùng lại phần đá,
bụi của `HatDa`, `HatKhoang` và công thức hạt (`pokiclash-fx-congthuc` mục 5: lưỡi, lốc, cầu đổi sang cát / đá).

## Làm (người dùng 2026-11-17: "làm đi", rồi "chia multiagent làm cùng lúc đi")

Claude chính làm suất 1 `cong_da`; bốn agent làm suất 2–5, mỗi con ghi chú riêng ở `inbox/<mã>_ghichu.md` (than_lan_cat, thu_da, rong_cat,
quy_nui), script `<mã>_manh.py`, `<mã>_rig.py`, rig ra `inbox/<mã>_1/rig/`.

### Suất 1 `cong_da` (tatu)

- Mảnh `cong_da_manh.py` (đúng chỗ, đúng cỡ trên concept; cách quang_sat): M1 thân tròn đủ (không mắt, mày, miệng, tai), M2 mai bốn tấm có hốc
  trống ở đỉnh, M3 pha lê + ba sỏi + hai tai + đuôi, M4 ba chân, F1 tròng trắng hai mắt + miệng, F2 hai con ngươi + hai mày, M5 phần thân LỘ RA
  trên concept (viền đỉnh đầu chạy trước chân tai). Codex đạt lượt đầu mọi tờ (56–67 s). Ghép lại IoU hình bóng 0,980.
- Concept lớp: lưng < mai < tai < mặt, nên thân hai lớp cùng lưới: `body` (M1, sau mai) và `body_truoc` (M5, sau tai, cắt ở y concept 790 mờ
  dần 30 px). Tai `mml`/`mmr` thay hai tấm mày của họ; chân giữa `footl1` lùi ra sau mai (họ vẽ trước khối pha lê) để đùi không nổi lên mai;
  sỏi phải `hair4` ra trước mai. `hair5`, `footr2` không có trên concept: mượn ảnh `hair1`, `footl1` (tối hơn) đặt ở chỗ part gốc.
- Rig `cong_da_rig.py`: 38 xương, 20 slot, `.atomik` ~0,12 MB, cao 308. Clip: appear (mai rơi nảy, thân hiện, chân bật ra, rũ mình, cau mày),
  idle (idle_01 + hít hít, hắt xì 1,42 s), walk, attack (skill_01_1 + lao 0,5 cao, húc 0,40), cast (skill_02 + lắc mai 0,36–0,66, ban 0,50),
  skill (rụt vào mai: chân co, hạ sát đất, mai không méo; rung 0,30–0,80; ban_troi 0,86; mưa 1,20; trúng 1,50), hit, die (lật ngửa 95°, đặt
  điểm thấp nhất xuống đất, mờ). Nheo mắt = co dọc `head2`. Góc nhảy lớn ở bàn chân (all12/14/15, tới 82°/khung) là của họ (đo trên mẫu gốc).
- Lỗi đã sửa: mai che kín mặt (thêm lớp `body_truoc`); rụt mai bóp dẹt cả mai (đổi sang co chân + hạ thân); lật ngửa lún dưới đất.
- Ba lớp quanh mặt dựng KHÔNG vệt nối (`cong_da_rig.lop_than`): mai (`hair3`) KHOÉT mọi chỗ thân lộ ra trên concept (M5, co 3 px: GPT vẽ trọn mai
  xuống tới bụng); thân `body` = M1 nhưng vùng M5 lấy đúng điểm ảnh M5; lớp mặt `body_truoc` = M5 chỉ ở vùng đầu (x concept > 690, mờ tới 722).
  Mép mai trong 70 px quanh thân lộ ra biến dạng hoà dần theo lưới thân (`MEP_MAI`): mai bám xương đầu, thân bám nhiều xương, đầu xoay là mép mai
  trượt khỏi thân, lộ viền. Chân giữa ra SAU thân (đùi GPT vẽ trọn lộ ra trên bụng). Mai có hình thứ hai `hair3_tron` (nguyên vẹn) dùng lúc rơi
  ở appear (thân còn ẩn). Hắt xì: đầu xoay ít (±4°), bù bằng ngả cả con + nhún.
- Bản xuất 2026-11-17: 38 xương, 20 slot, 21 hình, 1348 đỉnh, 8 clip, 11 sự kiện, `.atomik` 166 KB (đạt); mọi clip nối về khung 0 idle 0,00 px,
  appear khung đầu trống, die khung cuối trống; `thu_xem.py` (đường dẫn tuyệt đối) chạy đủ 8 clip. Trang xem `inbox/cong_da_1/rig/xem.html`.
  Chưa làm: VFX trên sân (chùm sỏi, pha lê lên trời / mưa, bụi, phụt hắt xì), vào game (heroes.json, thay suất ải 1 `thach_nhan`?).
- **Người dùng xem lượt 1 (2026-11-17): "idle bị giật, hơi xấu, không mềm mại"; "tôi chưa tưởng tượng 2 chiêu mana và cuối là sẽ đánh như
  nào"; "đầu ghép bị lỗi, hở 1 chút ở dưới".** Sửa:
  - Hở dưới = viền đôi ở bụng (M1 thò dưới M5): thân tròn chỉ giữ chỗ dưới mai (mai vẽ trọn co 4 px) hoặc trong M5.
  - Idle viết lại: bỏ idle_01 + hắt xì (nheo bằng co `head2` trông xấu); sóng tròn chu kỳ 2 s lệch pha (thở 1,6 / 2 %, đầu trễ 0,14 s, mai
    0,24 s, sỏi 0,28–0,40 s, đuôi hai nhịp), trò nhỏ: mũi hít, tai phải giật, mắt liếc. Bước mỗi khung ~1 px (cũ 4,9), khép vòng 0,14 px.
  - Chiêu mana: ba viên sỏi rời mai THẬT bay găm vào đối thủ rồi về lắp lại (far + fly_a/b/c + bay_*, như quang_sat; xuất `far=("cast",)`),
    lắc mai trước khi phóng, mai nảy đón từng viên. Sự kiện ran 0,28; phong 0,46 / 0,52 / 0,58; trung 0,66; ve 1,00 / 1,06 / 1,12.
  - Chiêu cuối: cụm pha lê có xương riêng `pha_le` (con của `hair`, mảnh cứng), vọt lên khỏi khung ở ban_troi 0,86, hốc mai trống, mọc lại ở
    moc 1,66; mưa pha lê (mua 1,20, trung 1,50) là VFX.
  - Bản xem trước có đối thủ + VFX hạt phẳng (`tho5_fx.py`, khung rig thật lật quay về địch ở chỗ phe mình, xương far đặt đúng giữa thân địch;
    hạt Thổ: dăm đá nảy một lần, bụi đất, sỏi, mảnh pha lê lăng trụ viền mực): `inbox/tho5_fx/xem.html` (cong_da_cast / skill / attack.gif).
  - Bản xuất: 46 xương, 23 slot, 24 hình, 8 clip, 17 sự kiện, `.atomik` 164 KB.

### Suất 2–5 (agent) và bản xem trước chiêu

Ghi chú chi tiết từng con: `inbox/<mã>_ghichu.md`. Claude chính nối mỗi rig vào `tho5_fx.py` (bảng `DUNG`: dựng rig, đặt `far` ở giữa thân địch
bằng cách thay tạm `sk.xuong` lúc rig tự thêm xương far; không sửa file rig của agent) và viết công thức VFX xem trước (bảng `CONG_THUC`):
- `than_lan_cat`: cast = ba phiến găm (mảnh gốm vỡ, bụi), skill = dậm chân + LỐC CÁT (`loc_cat`: thân phễu cát + dải xoáy chạy lên vẽ bằng
  `fx.polys` một khối rồi mới làm trong, mảnh gốm xoay quanh, bụi tràn miệng / chân phễu), attack = vết cắn hai cung.
- `thu_da`: cast = bụi + sỏi hút vào `mieng`, phun TẢNG ĐÁ vồng (`tang_da`); skill khai lunge: bản xem trước đổi độ dời `move` (+x) sang hướng
  tới địch (`Tuong.khung(lao=True)`), bụi khi cuộn xoay, vệt bụi khi lăn, nện lớn; attack = giáng sừng. Quả cầu cuộn tròn to ~1,15 thân
  (agent hỏi có thu nhỏ không).
- `quy_nui`: cast = nện đất → SÓNG CHẤN (`song_chan`: cụm đá góc cạnh trồi rồi lún nối nhau tới địch); skill = tảng đá lớn dần giữa hai tay phụ
  (theo `mieng`, bán kính rig 70 → 220 × 1,8 cho ra "khổng lồ"), hút đá từ đất, hai nhịp nện gồng, ném vồng, nện + mưa đá nhỏ; attack = ba
  nhịp.
- `rong_cat`: mốc giờ nằm cục bộ trong `lam_clip` nên đọc từ sự kiện của clip (`_ev`); cast = ba LƯỠI CÁT trăng khuyết dày (`luoi_cat`,
  R 40–50) bay từ `mieng`; skill = hút cát về vuốt, nện + VẾT NỨT lan tới địch (`vet_nut`), ba CỘT SA THẠCH (`cot_da`, vẽ ở lớp SAU địch để
  không che con bị trúng), cột 3 to nhất hất địch lên; attack = ba vệt vuốt.
Trang: `inbox/tho5_fx/xem.html` (mọi GIF), tờ soi `<mã>_<clip>_soi.png`. Cả 5 con xong rig + 8 clip + bản xem trước chiêu (2026-11-17).

Câu hỏi còn mở (gom từ agent): thay suất ải 1 / 5 / 10 / 15 / 20 (`thach_nhan`, `lung_vuong`, `cao_da`, `ho_khoan`, `phu_van`)? tên, số dạng;
quả cầu cuộn tròn của `thu_da` to ~1,15 thân (thu nhỏ?); `thu_da` chết lật ngửa hay gục sấp như con gốc; walk của `rong_cat` dùng run_01 khá
nhanh; `than_lan_cat` xoè phiến ở cast dựng khá đứng.

## Vào game (người dùng 2026-11-17: "cho vào game đi")

Claude tự quyết (người dùng đổi được): giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ của năm suất cũ; mỗi tướng 2 dạng cùng trỏ một rig (3 → 2
như suất Hỏa, Kim đã đổi hình), cỡ lớn dần theo ải; tên, danh hiệu, tên thẻ, biểu tượng thẻ mới:

| Suất | Tên | Danh hiệu | Rig | Cỡ | Thẻ (mana / cuối / nội tại) |
|---|---|---|---|---|---|
| `thach_nhan` ải 1 | Thạch Giáp | Tatu mai đá hổ phách | `cong_da_1` | 0,88 / 1,0 | Văng Sỏi / Mưa Hổ Phách / Mai Đá |
| `lung_vuong` ải 5 | Sa Tích | Thằn lằn áo choàng đất nung | `than_lan_cat_1` | 0,9 / 1,04 | Phiến Gốm Bay / Lốc Cát / Áo Phiến Gốm |
| `cao_da` ải 10 | Tê Thiềm | Cóc tê giác đất nung | `thu_da_1` | 0,92 / 1,08 | Phun Đá / Lăn Nện / Sừng Đá |
| `ho_khoan` ải 15 | Sa Long | Rồng giáp sa thạch | `rong_cat_1` | 0,94 / 1,1 | Lưỡi Cát / Cột Sa Thạch / Giáp Gai |
| `phu_van` ải 20 | Sơn Viên | Vượn núi đá bốn tay | `quy_nui_1` | 0,96 / 1,14 | Chấn Địa / Cự Thạch / Da Đá Núi |

Đã chuẩn bị (ngoài Assets, chờ phiên assets-15 trả Unity):
- `quai/doi_tho5.py [--kiem]` sửa từng khối heroes.json, cards.json (thử trên bản sao: đúng, chạy lại không đổi); `doi_tho5.py chep` chép
  `<mã>.atomik` + chân dung vào `Resources/<mã>/`.
- `quai/tho5_game/HatTho.cs`: hiệu ứng hạt của 15 chiêu (mã `n_giap_*`, `n_tich_*`, `n_thiem_*`, `n_long_*`, `n_vien_*`), chuyển từ
  `tho5_fx.py`; mốc theo rig, chỗ miệng / vuốt / tay / mai đo trên rig (`scratch do_diem.py`) vì lớp hạt không đọc xương. Không dùng ảnh đá,
  vết nứt có mạch dung nham (`hat_rock_*`, `hat_crack_*`) và chớp nước `BurstFlash`; khối lớn (lưỡi cát, lốc cát, cột, gai sóng chấn, vết nứt)
  là mảng liền.
- `quai/tho5_game/vao_game.py [--kiem | --ra <thư mục>]`: chép HatTho.cs, chèn case vào `HatNuoc.PlayNuoc`, mã đòn thường vào `HatVoi.AtkLao`,
  bảng `ThoFx` / `ThoAtk` + nhánh `Elem.Tho` vào `StageView` (sửa từng chỗ). `quai/tho5_game/bien_dich_thu.py <thư mục>`: biên dịch thử Core +
  Game bằng Roslyn của Unity với bản đã sửa (2026-11-17: 0 lỗi).
- Sau khi đổi, không tướng nào dùng 15 dạng cũ `thach_nhan_1..3`, `lung_vuong_1..3`, `cao_da_1..3`, `ho_khoan_1..3`, `phu_van_1..3`: xoá
  sau khi "Gắn dạng" dựng lại prefab (luật bỏ hẳn tướng cũ).
- Tên ải còn theo tướng cũ (`IslandGen.Tho`: "Hang Lửng", "Đồi Ngọc Lục", "Mỏ Pha Lê", "Đền Phù Văn"): chưa đổi, hỏi người dùng.

**Đã vào game (2026-11-17, ~14:30–15:10, sau khi assets-15 trả Unity):** `vao_game.py` (HatTho.cs, case PlayNuoc, AtkLao, bảng ThoFx/ThoAtk
+ nhánh Elem.Tho trong StageView), `doi_tho5.py` + `chep`; Unity: biên dịch sạch, Nhập dữ liệu, Gắn dạng (5 prefab giữ 2 dạng rig mới), Đảo
70 ải sinh lại (stages.json đổi 9 tỉ lệ rơi), Nhập lại, golden ngoài Unity (`regold.sh --apply` của assets-15: roster, battles, sim đổi) →
tbuild 110/110, EditMode 122/123 (hỏng duy nhất PrefabOnlyTests cũ, NumberTicker/UiMotion). Tour `ThoFxTour` (menu "Đảo Thổ: cả 5 tướng"),
ảnh `Temp/PokiShots/tho_fx/`: mọi chiêu chạy; sửa sau soi: cột sa thạch cuối cao 1,45 × đối thủ, hai cột nhỏ ±0,62 × đối thủ (đều lớp sau),
lốc cát rộng +35 %. Xoá 15 thư mục dạng cũ (`Resources/<id>_1..3` của 5 suất; kiểm không còn tham chiếu GUID). Tên ải vẫn theo tướng cũ.

## Dạng 2 của ba con đầu (người dùng 2026-11-17: "làm thêm dạng 2 cho 3 con đầu đi")

Trong kho không có dạng tiến hoá rõ của 3378, 3257 (các số kề chỉ là bản đổi màu, cùng rig). Tờ ứng viên `inbox/tho5_dang2_ung_vien.png`;
**người dùng chọn**: Thạch Giáp (tatu) → `monster_3528` (đống pha lê trên bốn chân pha lê, thân tím, đuôi xoắn); Sa Tích (thằn lằn) →
`monster_3530` (thằn lằn gai ngồi xổm); Tê Thiềm (cóc) → `monster_3526` (dạng tiến hoá của 3525 trong game gốc, có clip `evolution_01`).

- Quét vào `<SXS>/scan/monster_<số>/`: `info.json` (3528: 33 xương, 18 slot, 14 clip; 3530: 58 xương, 46 slot, 10 clip; 3526: 54 xương,
  48 slot, 13 clip), `att_goc.json`, `att_idle0.json`, tờ khung `khung/<clip>.jpg`.
- Slot đáng chú ý: 3528 chân là `jiao_l/r` + `shou_l/r` (bốn trụ pha lê), sáu khối `fangkuai_*`, đầu `tou`, mắt `yankuang` + `yanjin_1`, đuôi
  `weiba_1`, thân `yao`, mầm hai lá `yezi_1/2`; 3530 sừng đầu `jiaol/r`, gai lưng `beici1..6`, gai đuôi `weici1..4`, răng `ya1..4`, mày
  `mml/mmr`, tay `handr_*`, `lhand_*`, chân `footl/r_*`; 3526 tay gần có bàn và ngón (`youdabi_*`, `shouzhang`, `shouzhi_*`), đai lưng
  `yaodai_01..03`, hàm `xiaba_*`, lưỡi `shetou`, sừng `jiao_01`, gai lớn `wuqi_*` (tên gốc là "vũ khí").
- Script `tho5_dang2.py` (ca_con, slot, concept, so_goc), thư mục `inbox/<mã>_2/`, gói `gui_gpt/<mã>_2/luot_1_concept.txt`. Concept GIỮ NHẬN DIỆN
  dạng 1 (ảnh 2 = `L1_duyet.png` dạng 1: loài, mặt, màu, chất liệu, mảnh nhận diện), đặt lên thân và dáng của rig dạng 2 (ảnh 1 chỉ là mẫu
  dáng): tatu mai đá thành núi đá nhiều tấm + ba cụm hổ phách, bốn chân trụ đá; thằn lằn mũ trùm + giáp phiến đất nung khắp thân; cóc gai lửa
  thành cụm pha lê hổ phách, đai lưng da.
- Hạn mức Codex lúc bắt đầu (14:03): khung 5 giờ ~86%, khung tuần ~93% (mỗi ảnh ~1–2% khung 5 giờ, ~0,2–0,25% khung tuần).
- Concept lượt 1 (14:04–14:08, `tai_ve/L1_A.png`): tatu IoU 0,642, thằn lằn 0,581, cóc 0,555. Người dùng: "con đầu tiên chân dài quá nhìn hơi
  dị, sửa lại" → lượt sửa `tho5_dang2.py sua cong_da` (`luot_2_sua_chan.txt`: vẽ lại L1_A, chân tatu ngắn mập, mép mai buông thấp như váy đá
  che nửa trên chân, bàn chân giữ chỗ) → `L1_B.png`. **Người dùng duyệt (14:16): "ok concept 3 con kia ổn rồi làm đi"** → `L1_duyet.png`:
  tatu = L1_B, thằn lằn = L1_A (dù Claude chê giống dạng 1 về dáng, người dùng nhận), cóc = L1_A.
- Làm (14:16): ba agent song song (như lượt dạng 1), mỗi con ghi chú `inbox/<mã>_2_ghichu.md`. Hạn mức lúc giao: khung 5 giờ 94% (đặt lại
  14:51), khung tuần 94%: mỗi con tối đa ~7 ảnh Codex.

### Dạng 2 (+ Sa Long dạng 1) vào game (2026-11-17, agent "đưa dạng 2 vào game")

- `quai/doi_tho5_dang2.py` (bảng `TUONG2`): forms 2 rig — Thạch Giáp Nhi `cong_da_1` 0,88 / Thạch Giáp `cong_da_2` 1,0; Sa Tích Nhi
  `than_lan_cat_1` 0,9 / Sa Tích `than_lan_cat_2` 1,04; Tê Thiềm Nhi `thu_da_1` 0,92 / Tê Thiềm `thu_da_2` 1,08; Sa Long Nhi `rong_cat_non`
  0,85 / Sa Long `rong_cat_1` 1,1. `th <id>` gộp clip `evolve` (atomik_dang.gop_tien_hoa như doi_tinh_sat.th; dạng 1 gồng rung → mờ ở 1,05–1,35 s
  → dạng 2 hiện, lớn dần, dừng ở khung 0 idle dạng 2; slot ẩn giữ ẩn) → `inbox/<dạng 1>/rig/<dạng 1>_th.atomik` + `khung_evolve.png`;
  `chep <id>` chép `_th` thành `Resources/<dạng 1>/<dạng 1>.atomik` + `Resources/<dạng 2>/`; **`lam <id>` = th + chep (chạy lại khi rig sửa)**.
  `_th`: cong_da_1 310 KB, than_lan_cat_1 285 KB, thu_da_1 390 KB (quá đích 0,3 MB, dưới trần 0,5), rong_cat_non 207 KB.
- Hiệu ứng (`quai/tho5_game/HatTho.cs`): hàm cũ thêm tham số dạng (`NGiapHuc/Soi/Mua`, `NTichDop/Phien/Loc`, `NThiemPhun`: `dang = 2`;
  `NLongLuoi`: `dang = 1`; `NLongVuot`: `manh`); hàm mới `NThiemDam2` (đâm mũi khối pha lê), `NThiemBo2` (nhảy bổ khối, ba cột pha lê hổ phách
  lớp sau đối thủ, hai vết nứt), `NLongCot1` (Sa Long non: hút cát về vuốt, nện, vết nứt, cột nhỏ bên hông + cột vừa sau lưng đối thủ cao
  1,2 × đối thủ). Mã: `n_giap_*2`, `n_tich_*2`, `n_thiem_dam2 / phun2 / bo2`, `n_long_vuot1 / luoi1 / cot1`. StageView: `ThoFx` / `ThoAtk`
  thành bảng THEO DẠNG (`vao_game.py` thay khối bảng đợt 1 + 3 nhánh Elem.Tho). Thêm sau thì chỉ thêm mã vào bảng.
- `Editor/ThoFxTour.cs`: menu dạng 2 (sao 6), tiến hoá (hộp chi tiết, nút hack, chép GiotSuongCombatTour.Evolve), phe địch (ải mở đầu
  281 / 285 / 290 / 295, tạm cấp 35 trong bộ nhớ lúc Play, tướng Thổ ra đòn từ phía trên sân).
- Unity: biên dịch sạch; Nhập dữ liệu; Gắn dạng (4 prefab giữ 2 dạng rig mới, dạng 1 có 9 clip gồm `evolve`); Đảo 70 ải sinh lại; regold:
  13 golden giống từng byte (số dạng vẫn 2); tbuild 110/110; EditMode 122/123 (hỏng duy nhất PrefabOnlyTests cũ).
- Tour (`Temp/PokiShots/tho_fx/`: `<id>_6sao_*` dạng 2, `ho_khoan_1sao_*` Sa Long non, `tien_hoa/`, `dich_<id>_d2_*` phe địch); tờ soi tổng
  `inbox/tho5_dang2_game_soi.jpg` (scratch `to_soi_d2.py`). Đạt: mọi chiêu chạm đúng khung trúng, không che con bị trúng (khối lớn trong mờ /
  lớp sau), phe địch không tràn mép trên, tiến hoá trong hộp chi tiết mượt (một khung chồng mờ ~0,3 s), tên / hàng dạng / chân dung đúng.
  Sửa sau soi: cột pha lê `NThiemBo2` (cột giữa sau lưng đối thủ 1,4 ×, hai cột bên ±0,7 × — trước bị đối thủ và thân tướng che hết),
  cột `NLongCot1` (cột vừa 1,35 ×, cột nhỏ dời ra phía xa). Bản rig cuối đã chép: cong_da_2 313 KB (hốc pha lê, 2026-11-17 ~16:00).
- Còn: Sa Long dạng 1 chờ bản sửa viền cổ–đầu → `py -3 -I ArtGen/Spine/quai/doi_tho5_dang2.py lam ho_khoan`, refresh Unity, menu "Gắn dạng
  .atomik vào prefab tướng". Lưu ý Unity: `refresh_unity` có thể dời biên dịch sang lúc vào Play (thoát Play giữa tour): chờ dòng "Reloading
  assemblies after finishing script compilation" mới vào Play.

## Việc tiếp

1. ~~Người dùng chọn hướng từng con~~ (xong: 1C 2D 3D 4D 5C).
2. ~~Animation, rig, bản xem trước~~ (xong).
3. Vào game (mục trên).
4. Dạng 2 ba con đầu: concept (đang gen) → người dùng duyệt → nhóm mảnh → rig + clip → VFX → clip `evolve` gộp hai dạng → game.
   Xong rig: `cong_da_2` (287 KB), `than_lan_cat_2` (170 KB); `thu_da_2` đang làm. Câu hỏi agent, người dùng giao Claude tự quyết (2026-11-17):
   Thạch Giáp dạng 2 bay ba cụm pha lê thay sỏi: GIỮ; Sa Tích dạng 2 ngồi xổm thẳng lưng (`L2_tuthe.png`): GIỮ; chiêu cuối Sa Tích dạng 2 đập
   đất hai lần + lốc cát cao hơn: GIỮ (trong game kẹp chiều cao lốc theo mép sân). Người dùng: "con nào xong animation thì cho tôi xem" → trang
   `inbox/tho5_dang2_xem.html`.
5. Sa Long DẠNG 1 (`rong_cat_non`, rig 3529, gen qua Magnific): concept duyệt 2026-11-17 ("duyệt rồi mà làm ngay đi"), agent đang làm mảnh +
   rig; ghi chú `inbox/rong_cat_non_ghichu.md`.

6. **Đã vào game (2026-11-17, ~16:30):** dạng 2 Thạch Giáp (cong_da_2, bản hốc pha lê hai lớp), Sa Tích (than_lan_cat_2, lớp lưng lot), Tê Thiềm (thu_da_2) và Sa Long dạng 1 (rong_cat_non, bản bỏ viền nối cổ–đầu, tách hàm); clip evolve gộp (`quai/doi_tho5_dang2.py lam <id>`), hiệu ứng theo dạng (HatTho.cs, ThoFx/ThoAtk theo dạng), forms "<Tên> Nhi" / "<Tên>". Test: golden không đổi, tbuild 110/110, EditMode 122/123 (PrefabOnly cũ). Người dùng: "tạm ổn, có vài lỗi nhỏ nhưng chấp nhận được". Lỗi nhỏ còn: hai cột bên Tê Thiềm dạng 2 bị thân che một phần khi đánh đối thủ to; Sa Long dạng 1 hai đốm sáng 2–3 px đầu nét chân trước, vân vai / đùi hơi sọc khi phóng to; Tê Thiềm dạng 2 vài nét mờ dưới hàm khi há, đuôi ngắn hơn gốc. Chưa commit.
