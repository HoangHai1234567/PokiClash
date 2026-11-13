# Golem lõi lửa (`golem_lua`): tướng thứ 4 đảo Hỏa

Bắt đầu 2026-11-13 (máy ổ C). Con gốc của rig: `monster_3422` (golem đá gù đi hai chân, gai đỏ, lõi đỏ giữa ngực; game tham khảo, kho
`D:\Ripper\SwordxStaff`), **do người dùng chỉ** (ảnh chụp trang xem, clip `idle_01`). Cùng loạt golem với `monster_3423` (tượng đá giữ
rừng, `tuong_da_ghichu.md`, mục 25 skill). Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng
công khai. Hình là thiết kế của mình. Tên, id game: chưa đặt (`golem_lua` chỉ là mã làm việc).

## 1. Lời dặn của người dùng (2026-11-13)

- "làm tướng 4 đảo hỏa; concept **như trong hình**, kiểu **golem đi bằng 2 chân có lõi lửa**, **lửa thoát ra từ các lỗ trên người** (**gai đỏ
  đổi thành lửa**)".
- appear: "hiện **lõi lửa trước** rồi các **part còn lại bay vào theo đường vòng cung** tạo nên con tướng".
- idle, run: "có thể làm **giống họ**" (`idle_01`, `run_01`).
- Đánh thường: "làm giống **skill_01**: **lao đến dùng tay vả từ trên xuống vào đầu** đối thủ".
- Chiêu cast mana: "**hơi cúi người, há to mồm và phun lửa**, **rung người**, **impact mạnh**" (lửa là VFX; rig đặt xương miệng + sự kiện).
- Chiêu cuối: "làm giống **skill_03**: **nhảy lên co người thành hình tròn**, các **gai lửa dài hơn chút**, **xoay thật nhanh** rồi lao vào đối
  thủ. Bạn làm animation **nhảy lên co người**, làm animation **xoay một chỗ** nối từ animation trước; **việc bay vào nảy ra dùng code**".
- die: "**lõi tắt ngỏm**, các bộ phận cũng **rơi xuống** theo".

## 2. Mổ rig gốc (`<SXS>/scan/monster_3422/`: `info.json`, `att_goc.json`, `att_idle0.json`, `mo/idle0_*.jpg`, `mo/nhom_idle0.jpg`, `parts/`, `khung/`)

64 xương, 91 slot (45 hình × 2 bộ + `shadow`), 11 clip, 3187 khoá. Con nhìn sang PHẢI. **Mọi hình là mảnh CỨNG một xương** (hai gai bám
hai xương 0,5 / 0,5): kiểu "mảnh lơ lửng" như tượng đá (skill mục 25) nhưng thân kín hơn (các tấm đá lớn chồng nhau lấp kín hình bóng).
IK: hai chân (`L1`: P_tuiiL1 → P_tuiiL2, đích `L1`; `R1`: P_tuiiR1 → P_tuiiR2, đích `R1`, mix 1); bốn IK tay `SL1/SL2/SR1/SR2` mặc định
tắt (mix 0). Không transform, path, physics.

Bên GẦN là `R` (trái hình, vẽ trước), bên XA là `L` (phải hình, vẽ sau). Mặt: mặt nạ đầu lâu đá quay ba phần tư sang phải, nằm thấp phía
trước dưới tấm mày; **một mắt** tròn nhỏ (`P_yanjing3`) trong hốc; **hàm dưới riêng** (`P_zuiiba3`, màu phụ, mép dưới có bậc) và **lòng miệng**
(`P_kouqiang3`, đỏ có sọc) nấp sau mặt: há mồm được. Sừng pha lê trên trán (`P_jiao3`) chĩa tới trước, đế có hai núm màu phụ.

Bảng mảnh bật ở idle (thứ tự vẽ sau → trước; "→" là vai trò trong thiết kế mình):
| thứ tự | slot | ảnh (px) | là gì | xương |
|---|---|---|---|---|
| 1 | `P_yuanzhui2` | 29 × 38 | gai nhỏ sau khuỷu tay xa (gần như khuất) → lửa nhỏ | P_yuanzhui2 |
| 2–4 | `P_tuiiL2`, `P_tuiiL3`, `P_tuiiL1` | | chân XA: khớp gối đỏ, bàn chân, đùi → gối dung nham | P_tuiiL2/L1 |
| 5–8 | `P_kua4`, `P_kua3`, `P_kua2`, `P_kua1` | 34–71 | các khối hông; `kua3` là khối tròn có gai đỏ dưới bụng → lửa | bone2 |
| 9–11 | `P_tuiiR3/R2/R1` | | chân GẦN: bàn chân, khớp gối đỏ, đùi | P_tuiiR2/R1 |
| 13, 15 | `P_shouL3`, `P_shouL4` | 80 × 85, 98 × 100 | cổ tay (màu phụ) + bàn tay đá XA | P_shouL1/L2 |
| 17–21 | `P_shouzhiL5/L6/L4` | | ba vuốt đen tay xa | P_shouzhiL* |
| 22 | `P_yuanzhui1` | 28 × 39 | gai nhỏ trên khuỷu tay gần → lửa nhỏ | P_yuanzhui1 |
| 24, 34 | `P_tiekuai4`, `P_tiekuai3` | | đai nhỏ màu phụ ở hai khớp vai | P_xiongjia3/2 |
| 26 | `P_xiongjia6` | 57 × 99 | tấm ngực phải hẹp (dưới hàm) | P_xiongjia3 |
| 28 | `P_xiongqiang3` | 157 × 162 | **khối cầu đỏ** trong lồng ngực → **lõi lửa** | P_xiongjia1 |
| 30 | `P_qiu2` | 40 × 40 | viên cầu đỏ nhỏ (tim lõi) → tim lõi vàng | P_qiu |
| 32 | `P_xiongqiang4` | 157 × 147 | **vỏ ngực hình chữ C** ôm lõi | P_xiongqiang |
| 36 | `P_xiongjia5` | 106 × 118 | khối ngực trái | P_xiongjia2 |
| 39 | `P_kouqiang3` | 66 × 69 | lòng miệng → họng lửa | P_kouqiang |
| 41 | `P_tou3` | 108 × 166 | mặt nạ đầu lâu | P_tou |
| 43 | `P_jiao3` | 76 × 52 | sừng pha lê trên trán → **lưỡi lửa ở trán** | P_tou |
| 46 | `P_zuiiba3` | 90 × 73 | hàm dưới (màu phụ) | P_kouqiang |
| 49 | `P_jianci13` | 37 × 38 | gai nhỏ sau đầu → lửa nhỏ | P_tou |
| 51, 53 | `P_toujia11`, `P_toujia10` | 94 × 81, 167 × 158 | tấm sau vai gần, **tấm lưng lớn** | P_toujia5, P_jianci4 |
| 54 | `P_dise` | 56 × 61 | tấm đế màu phụ sau đầu | P_dise |
| 56, 58, 60 | `P_jianci17`, `P_jianci16`, `P_jianci15` | | lỗ, **gai đỉnh lưng**, vòng đế → **lưỡi lửa cao trên lưng** | P_jianci4/5 |
| 62 | `P_jianci14` | 23 × 36 | gai nhỏ đỉnh trước → lửa nhỏ | P_jianci6 |
| 64, 66 | `P_toujia9`, `P_toujia8` | 106 × 97, 83 × 139 | tấm đỉnh, **tấm mày** (che trên mặt) | P_toujia2, P_tou |
| 67 | `P_yanjing3` | 19 × 21 | mắt | P_tou |
| 69, 74, 76, 78 | `P_toujia6`, `P_jianci11`, `P_jianci9`, `P_jianci10` | 116 × 120 … | **tấm vai gần** (khối tròn), lỗ, **gai to**, vòng đế → **lưỡi lửa to nhất ở vai** | P_toujia7, P_jianci7 |
| 80 | `P_jiapian2` | 113 × 88 | tấm má hình lưỡi kiếm quét xuống trái | P_toujia2 |
| 81, 83 | `P_shouR1`, `P_shouR2` | 89 × 85, 117 × 116 | cổ tay gần (màu phụ, có gai nhỏ trên đỉnh → lửa) + bàn tay đá GẦN | P_shouR1/R2 |
| 85–89 | `P_shouzhiR3/R2/R1` | | ba vuốt đen tay gần | P_shouzhiR* |

Bộ slot thứ hai (`P_*` số lớn hơn, mặc định trống, cùng ảnh) trên các xương rời con của `bone` (`P_toujia8`, `P_jianci8`, `P_shouR3`,
`P_jianci9`, `P_xiongjia6/7`, `P_qiu2`, `P_toujia9`, `P_jiapian`, `P_shouL3`, `P_shouzhi*4..6`): họ dùng cho `die_01` (văng ra rồi rơi
thành đống). Mình dùng cho `die` (rơi rã) và `appear` (bay vòng cung vào ráp lại), như tượng đá.

Clip của họ (tờ `khung/`):
| clip | dài | nội dung | dùng cho |
|---|---|---|---|
| idle_01 | 1,33 s | đứng gù thở, tay đung đưa | **idle** |
| run_01 | 0,60 s | chạy hai chân | **walk** |
| skill_01 | 1,00 s | giơ tay gần lên cao 0,09–0,27, vả / nện xuống phía trước 0,36, dư lực, về | nền **attack** (thêm lao tới, vả vào đầu) |
| skill_02 | 1,50 s | bật lên cao, nện người xuống đất 0,41–0,55, bật lần hai, nằm bò, về | (tham khảo nhịp rung) |
| skill_03 | 1,33 s | nhảy lên 0,12, **co thành quả cầu, các tấm quay ra ngoài, gai chĩa tứ phía** 0,24–0,61, bung ra rơi xuống 0,73–0,97, đáp | nền **skill** (nhảy co người + vòng xoay) |
| skill_04 | 1,17 s | ngửa người, há miệng (lòng miệng đỏ lộ) 0,53–0,85, gầm, về | nền **cast** (đổi thành hơi cúi, há to phun lửa) |
| block_01, hit_01/02, stun_01 | | | **hit** |
| die_01 | 1,00 s | các mảnh văng tung lên 0,09–0,45, rơi đè thành đống 0,55–0,64, nằm yên | nền **die** (thêm lõi tắt) |

## 3. Concept (đề xuất của Claude, chờ người dùng chọn)

Script: `golem_lua.py` (`mo`, `nhom`, `part_goc`), `golem_lua_bo_cuc.py` (sơ đồ bố cục 1536 × 1024 ở khung 0 idle, 1,056 px / đơn vị rig;
mọi gai đỏ vẽ thành lưỡi lửa bằng mã theo trục gai, dài 1,35–1,75 lần gai; `LAT` lật chiều gai dò ngược), `build_golem_lua.py` (gói
`gui_gpt/golem_lua_1/`; ảnh mẫu: sơ đồ, Voọc Tướng, Mắt lửa bọc giáp đã duyệt, bản đồ).

Giữ của con gốc (theo lời "concept như trong hình"): dáng golem gù nhìn phải, mặt nạ đầu lâu nhỏ thấp phía trước dưới tấm mày, một mắt,
hàm dưới riêng, vỏ ngực chữ C ôm lõi, tấm vai tròn có vòng đế, hai tay dài bàn tay đá ba vuốt chạm đất, hai chân ngắn có khớp gối.
Đổi: **mọi gai đỏ → lưỡi lửa phụt ra từ lỗ có vòng viền** (to nhất ở vai gần, cao nhất trên lưng, một lưỡi ở trán thay sừng), **khối cầu đỏ →
lõi lửa** vòng màu đồng tâm, **khớp gối → dung nham**, lòng miệng → họng lửa; chất liệu và màu của mình; rãnh khắc của mình (mỗi tấm nhiều
nhất một rãnh, mật độ như con gốc). Tránh tông đã dùng ở đảo Hỏa: đá nâu đỏ gạch (`quy_lava`), đá vỏ chai đen tím (`mat_lua`), giáp cháy
đen (`cung_lua`).

Ba hướng chất liệu:
- `da_tro` **A · đá tro núi lửa**: đá xám tro ấm #B2A79A, mảng phụ (vòng lỗ lửa, cổ tay, hàm, đai) than chì #3F3B46, vuốt đen than.
- `sat_lo` **B · sắt lò rèn**: sắt xám xanh #5C616C có vài đinh tán trên ba tấm lớn, mảng phụ đồng thau #B57438, vuốt sắt đen.
- `da_cat` **C · đá sa thạch**: đá vàng cát #C9AE84, mảng phụ nâu than #4A3A36, vuốt nâu đen.

Lượt 1: cả ba ra dùng được ngay (111–158 s mỗi ảnh): `golem_lua_1/tai_ve/L1_da_tro.png`, `L1_sat_lo.png`, `L1_da_cat.png`; trang so
`inbox/golem_lua_xem_concept.html`, đã mở cho người dùng chọn 2026-11-13. Soi: đúng bố cục sơ đồ, nhìn phải, một mắt vàng dưới tấm mày,
hàm riêng; đủ 8 lưỡi lửa từ vòng lỗ (vai gần to nhất, đỉnh lưng cao nhất, trán chĩa ra trước); gối dung nham; tô phẳng, không quầng.
Khác ý: **lõi lửa vẽ thành một đĩa tròn có hình ngọn lửa bên trong** (như huy hiệu) chứ không phải các vòng lửa đồng tâm; họng lửa giữa
mặt và hàm gần như không lộ; vài mẩu lửa rời lơ lửng cạnh lưỡi lửa (A, C); đùi chân gần như khuất, chỉ còn gối + bàn chân. Các chỗ này sửa
được ở lượt mảnh.

## 4. Kế hoạch rig và clip (sau khi concept được duyệt)

- Mảnh cứng một xương đặt theo concept (như tượng đá); mọi xương của họ, IK chân nướng qua `chay.py sample` (trường `l`).
- Mảnh gen "đúng chỗ, đúng cỡ" theo nhóm không chồng nhau (skill mục 25); lưỡi lửa là mảnh riêng mỗi lỗ, thêm lay lửa (2–3 đốt hoặc đổi
  hình), chiêu cuối phóng dài lưỡi lửa.
- Mảnh thêm: **lõi tắt** (than nguội) và **mắt tắt** cho die, appear; lòng miệng / họng lửa to hơn cho cast.
- appear: lõi lửa hiện giữa không trung (nhỏ → bùng), rồi từng mảnh bay vòng cung từ ngoài vào đúng chỗ (bộ slot rời), lửa bùng lên ở các lỗ.
- attack: `skill_01` + lao tới (`lunge`), giơ tay gần cao, vả từ trên xuống ĐẦU đối thủ (đỉnh lao = lúc vả), khựng, lùi về.
- cast: hơi cúi người (thay dáng ngửa của `skill_04`), há to hàm, rung người; xương `mieng` ở họng, sự kiện `phun` / `het_phun`; lửa phun là VFX.
- skill: tách hai clip theo lời dặn: `skill` (nhảy lên, co thành quả cầu theo `skill_03` 0–0,4 s, lưỡi lửa dài ra) và `skill_xoay` (lặp, xoay
  nhanh tại chỗ trong dáng cầu, nối khớp từ khung cuối clip trước). Phần lao vào, nảy ra do code; clip đáp / bung ra về idle nếu cần.
- die: `die_01` (bộ slot rời) + lõi tắt dần, lửa ở các lỗ lụi; mảnh rơi đè thành đống, mờ dần.
- VFX ngoài rig: phun lửa từ miệng (cast), vệt lửa xoáy quanh quả cầu (skill), bụi đá + tia lửa lúc vả và lúc mảnh rơi.

## 5. Mảnh và rig (người dùng chọn A, 2026-11-13: "tôi thích dạng A, lưu ý kĩ, phần lửa bốc ra cũng phải có animation uốn lượn nhẹ nhàng")

`L1_duyet.png` = `L1_da_tro.png`. Concept GPT vẽ to hơn sơ đồ ~1,24 lần nên khung concept ↔ rig khớp bằng bình phương tối thiểu trên tâm
mảnh (bỏ các mảnh gộp: đầu, hông, họng, lõi, tấm đỉnh): ~1,26 px / đơn vị con gốc.

- **38 mảnh, 8 tờ "đúng chỗ, đúng cỡ"** (`golem_lua_manh.py build` → `gui_gpt/golem_lua_1/luot_2_manh_A..H.txt`, cắt `golem_lua_manh.py lam`):
  31 mảnh đá (đầu = mặt + tấm mày một mảnh vì cùng xương `P_tou`; hông 4 khối một mảnh vì cùng `bone2`; ngực trái = đai + khối), 3 vòng lỗ
  rỗng giữa (vai, đỉnh lưng, trán) vẽ TRƯỚC lửa, 7 lưỡi lửa vẽ đủ gốc chui vào lỗ. Lửa nhỏ (đỉnh, sau đầu, cổ tay, hông) nằm SAU tấm của
  nó, cổ lỗ vẽ liền tấm với lòng lỗ tô màu lửa. Bỏ các part con gốc gần như khuất: `P_toujia11`, `P_xiongjia6`, `P_tiekuai4`, `P_dise`,
  `P_yuanzhui1/2`. `mat_tat`, `loi_tat` đổi màu bằng mã.
- Codex hết hạn mức lúc 13:13 (mở lại 14:53): tiến trình tách `cho_gen.py` (scratchpad) chờ tới 14:55 rồi chạy `chay_hoa.py` 8 tờ.
- **Rig** (`golem_lua_rig.py`, chạy thử bằng mảnh tạm `golem_lua_manh.py tam` + `GL_MANH=inbox/golem_lua_1/manh_tam`): đủ 64 xương của họ +
  root + move + 7 × 3 đốt lửa + `mieng` (họng, con của hàm) + `far`; IK chân nướng qua mẫu khung `l`. Mảnh đá cứng một xương; lưỡi lửa là lưới
  (`luoi_vung`), trục lấy trên chính ảnh mảnh (`truc_lua`: gốc gần chỗ chui vào lỗ, hai điểm giữa, ngọn), gốc bám xương mảnh (đứng yên trong
  lỗ), thân chia mượt cho 3 đốt (`trong_so_lua`). `lua_lay`: sóng chạy gốc → ngọn (đốt sau trễ 0,95 rad, biên độ 2,6° → 7,4°) + họa âm bậc 2
  + phập phồng dài 5%, lò xo `LoXo` (150/110/80); tham số `w` để pha hai kiểu lửa ở chỗ nối.
- Clip: `appear` (2,3 s: lõi hiện giữa không trung → 13 cụm bay cung Bezier vào, khựng khi ráp → mắt sáng → lửa bùng), `idle` (4 s = 3
  vòng idle_01; lõi phập phồng, vòng cuối "hắt lửa": lửa dài 1,22, đầu gật), `walk` (run_01, lửa ngả sau), `hit`, `attack` (skill_01 giãn
  giờ + lao 300, trúng 0,55), `cast` (skill_04 bỏ phần ngửa → cúi tới, hàm há ×1,3, rung; tu 0,20 / phun 0,50 / het_phun 1,50), `skill`
  (1,0 s: thụp, bật, cuộn thành cầu; lửa dài 1,4), `skill_xoay` (11/30 s, quay bone3 đúng 720°, 65°/khung; không đặt loop để bước khép vòng
  không chép khung 0 vào khung cuối), `skill_ve` (29/30 s: bung, đáp, về idle; quay bù cho khung cuối đứng thẳng), `die` (lõi chập chờn tắt,
  mắt tắt, lửa lụi, 14 cụm rơi nảy, tan). Nối: skill → xoay 0 px, vòng xoay 0 px, xoay → ve 0 px; mọi clip khác về idle 0 px.
- `quai/xuat.py`: thêm tham số tuỳ chọn `khong_khop=()` (clip không lặp mà không hoà về idle) cho `skill`, `skill_xoay`.
- Bẫy đã gặp: biến độ dài clip trùng tên trong cùng `lam_clip` (die gán lại `X_DUR`, `skill_xoay` đọc lúc chạy → quay chậm 5 lần); độ dài
  clip không chia hết 1/30 s thì khung cuối nướng rơi trước giờ cuối.

### 5b. Mảnh thật và rig xuất (2026-11-13 chiều)

- 8 tờ về lượt đầu (75–128 s / tờ, 13:30–13:44 sau khi người dùng báo có hạn mức lại). Ghép so concept lệch 8,5–9% điểm (`manh/_so_ghep.png`).
- Sửa bằng mã trong `golem_lua_manh.lam`: đục lòng vòng lỗ SAU `manh_rgba` (hàm đó tự lấp lỗ kín < 4000 px); lõi phóng ×1,28 cho lấp kín
  khe vỏ ngực (Codex vẽ lõi nhỏ hơn khe → lộ vệt trắng lưỡi liềm); họng cắt theo hình mặt + hàm lúc nghỉ; tấm má về SAU đầu (đè mắt);
  vòng trán dời (+16, −36) cho mép dưới viền trên mắt như mày cau (Codex vẽ trùng chỗ mắt), gốc lửa trán cắt phần tràn quanh mắt và nấp
  sau nửa trái vòng; lửa cổ tay dời (+35, +4) vào đúng lỗ (`DOI`).
- **Mảnh nguội** (`_nguoi`, 9 cái): vùng màu lửa (lòng lỗ, gối, cổ vòng trán) của tấm đá đổi sang than tro, cắt sát, slot ngay trên tấm,
  ẩn mặc định. die: hiện cùng lúc lõi tắt; appear: mảnh bay vào nguội, bừng sáng lúc lửa bùng (1,52 s).
- cast: hàm mở bằng 0,6 lần của họ (mảnh hàm mình to hơn hàm gốc: mở như họ thì hàm xoay dựng đứng, rời mặt); cúi tới bone2 −4°, ngực
  −12°, đầu −5°.
- Kết quả `golem_lua_1/rig/`: 88 xương, 49 slot, 1628 đỉnh, 10 clip, atlas 1208 × 1176, `.atomik` 472 KB; chiều cao game 543. Nạp lại
  lệch ≤ 0,56 px; mọi clip về idle 0 px (trừ skill / skill_xoay: kết thúc ở dáng cầu, nối nhau 0 px); appear khung đầu trống, die khung
  cuối trống. Góc nhảy runtime thật 60 khung/giây: lửa lúc đang ẩn (appear, die) tới 152°; vuốt tay lúc vả 83°, gầm 64°; còn lại ≤ 65°.
  Trang `rig/xem.html` (thu_xem: đủ 10 clip), tờ runtime `rig/that/`. Đã mở cho người dùng xem.

CHƯA làm: code game cho chiêu cuối (bay vào, nảy ra bằng `skill_xoay` lặp, kết bằng `skill_ve`), VFX (lửa phun từ họng ở xương `mieng`,
vệt lửa quanh quả cầu, bụi đá lúc vả / mảnh rơi), tên, id, suất 4 đảo Hỏa, dạng 2.

### 5c. Lỗ lửa hai lớp (người dùng 2026-11-13: "những lỗ lửa bạn tách 2 layer 1 trên 1 dưới thì lửa mới ở giữa lỗ được chứ")

Bản trước lửa nằm sau cả vòng (vòng lớn) hoặc sau cả tấm có cổ lỗ (lửa nhỏ): trông như lửa mọc sau vòng. Nay `golem_lua_manh.tach_vanh`:
- Thứ tự mỗi lỗ: **nửa vành sau** (phía lửa bay ra) → **lửa** → **nửa vành trước**. Vòng lớn (vai, đỉnh lưng, trán): cắt đôi vòng theo
  đường qua tâm vuông góc hướng lửa (gốc → ngọn) thành `<vòng>_sau` / `<vòng>_truoc`; nửa trước chờm qua đường cắt 4 px (khỏi khe hở một
  điểm ảnh lộ lòng lỗ khi thu nhỏ / vẽ lưới). Cổ lỗ vẽ liền tấm (tấm đỉnh, sau đầu, cổ tay, hông): lửa lên TRƯỚC tấm; nửa trước cổ lỗ (điểm
  màu than quanh lòng lỗ, phía trước) tách thành `<tấm>_vanh` vẽ sau lửa; lòng lỗ trên tấm tô một màu cam.
- Gốc lửa thò ra trước mép trước của vành (trong bề ngang vành) bỏ; lửa đè lên đai vành sau sát đường cắt (vòng lớn) bỏ; nét mực khép đáy
  lửa trong miệng lỗ tô màu lõi lửa (khỏi vệt ngang).
- Bốn lửa nhỏ bản đầu rộng 95–136 px mà miệng lỗ Codex vẽ trên tấm chỉ 42–78 px (gen ở hai tờ khác nhau, lệch nhau 15–54 px): gen lại
  một tờ N (`golem_lua_manh.py lua_nho` → `luot_2_manh_N.txt` → `M_N.png`, 78 s) gốc hẹp đúng bề rộng miệng lỗ, loe dần lên; lúc cắt dời
  mỗi lửa cho gốc trùng tâm lòng lỗ, ghi `goc_lua` vào `dat.json` (rig đặt chuỗi xương lửa theo điểm này).
- Lửa hông về sau khối ngực (trước đó bị vỏ ngực che mất).
Kết quả: 56 slot, `.atomik` 474 KB, atlas 1312 × 1320; nối clip như cũ.

### 5d. Chiêu cuối theo cơ chế tông thẳng của trận (2026-11-13, 14:27)

Thay ba clip `skill` / `skill_xoay` / `skill_ve` (mục 5) bằng HAI clip theo cơ chế sẵn có `AolaSticker.Jumps` / `Rams` (như Cầu Gai), khỏi viết
code trận mới: `skill` (1,0 s: thụp, bật, cuộn thành cầu; khung trúng = cuối clip, game coi là lúc rời đất) và `skill_land` (2,03 s: sự kiện
`tong` ở 0 → Rams; cầu xoay đúng 6 vòng trong 32/30 s lúc code cho bay gần ngang tới thân đối thủ, chạm ở 0,50 s (bẹp nhẹ, lửa bùng), đứng
0,16 s, bật về theo vòng cung; rồi bung người, đáp, về idle). `skill` cuối → `skill_land` đầu 0 px; `skill_land` cuối → idle 0 px.
`golem_lua_1_game.json`: hitClips attack 0,55 / cast 0,50 / skill 0,967 / skill_land 0,50; lunge attack; stay cast; impact attack + skill.
Kết quả `rig/`: 88 xương, 56 slot, 9 clip (appear, idle, walk, hit, attack, cast, skill, skill_land, die), `.atomik` 477 KB.
Dòng "CHƯA làm: code game cho chiêu cuối" ở mục 5b hết hiệu lực.

## 6. Vào game (người dùng 2026-11-13: "cho vào game"): suất 4 đảo Hỏa (ải 15 "Sườn Núi Khói"), GIỮ id `nham_than`

- `quai/doi_nham_than.py` (chạy lại không đổi gì): heroes.json khối `nham_than` forms 3 → 2: dạng 1 **Nham Con** (`nham_than_1`, cỡ 0,92),
  dạng 2 **Nham Thần** (`nham_than_2`, cỡ 1,1); CẢ HAI dạng tạm dùng chung rig `golem_lua_1.atomik` cho tới khi có dạng 1 riêng. Tên, danh
  hiệu "Chúa tể dung nham", chỉ số, độ hiếm, số mảnh, id thẻ giữ. cards.json: `nham_than_ult` "Biển Dung Nham" → **"Cầu Lửa Lăn"** (tên
  Claude đặt); "Phun Nham", "Thân Nham" giữ. `StageView.FireFx` nham_than ("nham", "thien_thach") → ("phun", "no_lon"). Không đổi id nên
  không có bước chuyển bản lưu, saveVersion giữ (sao cao tự dừng ở dạng cuối: HeroDef.FormIndex).
- Phiên đầu bị tắt nhầm lúc 14:30 sau khi chạy script và chép rig + chân dung vào Resources/nham_than_1, 2. Phiên sau (assets-f6) làm nốt
  qua cầu nối MCP 8080 (đã báo các phiên khác, Unity không Play): `manage_asset delete` Resources/nham_than_3 → refresh → "Nhập dữ liệu"
  (88 tướng; HeroDb nham_than 2 dạng) → "Gắn dạng .atomik" (prefab nham_than còn 2 dạng) → "Đảo 70 ải: sinh lại" (stages.json không đổi)
  → golden islands / roster / cardtext / zones (chỉ roster đổi: số dạng nham_than 3 → 2, sao dạng cuối 2 → 1) → golden theo danh sách
  tướng (không đổi) → golden sim + `golden_ghep.py` (sim: 1 ải đổi, hoa 85 = ải 15 đảo Hỏa; leads, battles không đổi).
- EditMode 102/103 (chỉ hỏng PrefabOnlyTests.MaRuntime_KhongSinhDoVat có từ trước: UI/Kit NumberTicker, UiMotion).
- `Editor/HoaFxTour.cs`: thêm menu "PokiClash/Thử/Đảo Hỏa: riêng Nham Thần, chiêu mana, chiêu cuối (đang Play)".
- Bản sao lưu trước khi đổi (golden, HeroDb, prefab, thư mục nham_than_3): scratchpad của phiên assets-f6, `sao_luu/`; nham_than_3 còn
  trong git.

### 6b. Soi trong trận và sửa (2026-11-13, phiên assets-f6)

Tour "PokiClash/Thử/Đảo Hỏa: riêng Nham Thần, chiêu mana, chiêu cuối (đang Play)" (ảnh `Temp/PokiShots/hoa_fx/nham_than_*`; bản trước khi
sửa: `Temp/PokiShots/hoa_fx_nham_than`). Chạy đúng cơ chế: cast đứng tại chỗ phun lửa ("phun") từ xương `mieng`; chiêu cuối cuộn thành cầu,
code cho bay tới thân đối thủ, nổ lớn ("no_lon"), bật về, bung người, đáp.
- **Bung người văng ra ngoài màn** (sửa ở rig): đoạn skill_03 0,63–1,0 tay, lưng, lửa vươn ra SAU tới 295 đơn vị (0,54 × chiều cao) so với dáng
  đứng; con của người chơi đứng sát mép phải nên gần nửa thân bị màn hình cắt. `golem_lua_rig.py` `lui(t)`: dời `move` tới trước 300 đơn vị
  theo đúng nhịp cú bật về của code (JumpStay 0,16 + JumpBack 0,42, smoothstep: quãng về vẫn một chiều), giữ tới 1,30 s rồi tan dần tới 1,95 s:
  cầu bật về tới cách chỗ cũ 300, bung người ở đó, rơi, trượt lùi nốt về chỗ. Đo lại: từ lúc về tới, mép sau vượt dáng đứng nhiều nhất 3 đơn vị
  (trước 295). Nối clip như cũ (skill → skill_land 0 px, skill_land → idle 0 px); `.atomik` 477 KB. Đã chép lại vào Resources/nham_than_1, 2,
  Gắn dạng, chạy lại tour: thân nằm trọn trong màn.
- **Màu hạt lửa**: `HatLua.Themes["nham_than"]` bảng "nham" (nâu đỏ sẫm, của Nham Thần cũ) → "lua" (đỏ cam lõi vàng như lưỡi lửa trên rig),
  mảnh văng "giap" đổi sang màu đá tro (178, 167, 154).
- Luồng lửa xuất phát ở họng, ngay TRƯỚC lõi ngực (họng nằm giữa mặt và lõi: hàm mở xuống sau): đúng xương `mieng`, không sửa.
- "Chụp thử dạng .atomik": `Library/PokiHeroShots/nham_than_atomik_1/2.png` đủ idle, hit, attack, cast, skill. EditMode 102/103 (như trước).
- CHƯA: dạng 1 riêng (hai dạng đang chung một rig nên lên sao không đổi hình, chưa có clip `evolve`); VFX riêng (vệt lửa quanh quả cầu lúc lăn,
  bụi đá lúc vả / lúc đáp); chưa xem đòn thường, appear, die trong trận (tour chỉ chạy mana + chiêu cuối); chưa thử Android; chưa commit.
  Rig xuất trước khi phiên cung_lua sửa `quai/hoat.py` (khoá alpha thành bậc): lần xuất lại sau sẽ dùng bản mới.

## 7. Dạng 1 "Nham Con" (người dùng 2026-11-13: "làm dạng 1 và vfx riêng đi"), mã làm việc `golem_lua_non`

Cùng rig, cùng clip với dạng 2. "Tỉ lệ trước, concept sau" (như Hỏa Nhãn dạng 2): `golem_lua_non.py bo_cuc` xếp lại MẢNH dạng 2 đã cắt
(`golem_lua_1/manh`, toạ độ khung concept) ở tỉ lệ dạng non: lửa lớn co quanh gốc lửa, bàn tay + vuốt co quanh chỗ chạm đất (vuốt co thêm
về gốc vuốt), đầu / mắt phóng quanh tâm; lỗ "tắt" hiện mảnh nguội `_nguoi` và bỏ lưỡi lửa → `golem_lua_non/mau/bo_cuc_<hướng>.png`.
Gói: `build_golem_lua_non.py` → `gui_gpt/golem_lua_non/luot_1_concept_<hướng>.txt` (ảnh mẫu: hình bố cục, concept dạng 2 đã duyệt, Voọc
Tướng, bản đồ). Chung: cùng đá tro + than chì, vuốt cụt tù, mắt hơi to hơn, lõi dịu hơn, đủ mảnh như dạng 2. Ba hướng (đề xuất của Claude):
- `moi_lua` **A · mồi lửa**: giữ khối dáng dạng 2; ba ngọn lửa nhỏ (vai, đỉnh lưng, trán) ×0,55; bốn lỗ còn lại tắt; tay ×0,86, vuốt ×0,72.
- `cuoi_tron` **B · cuội tròn**: chibi: đầu ×1,16, mắt ×1,3, tay ×0,80, vai ×0,92, khối đá tròn như đá cuội; ba ngọn lửa nhỏ ×0,5, lỗ khác tắt.
- `du_lua` **C · đủ lửa nhỏ**: như A nhưng đủ bảy ngọn lửa (lớn ×0,55, nhỏ ×0,6).
Lượt 1 ra cả ba (85–112 s mỗi ảnh): `golem_lua_non/tai_ve/L1_moi_lua.png`, `L1_cuoi_tron.png`, `L1_du_lua.png`; tờ so
`golem_lua_non/so_concept.jpg`; trang so `inbox/golem_lua_non_xem_concept.html`, đã mở cho người dùng chọn. Soi: cả ba giữ bố cục, nhìn phải,
đủ mảnh, vuốt cụt, tô phẳng không quầng; A và B lỗ tắt là lỗ tối có vành than; B mắt to tròn rõ nhất (dễ thương nhất, mày vẫn đè).
**Người dùng chọn A** (2026-11-13) → `golem_lua_non/tai_ve/L1_duyet.png` = `L1_moi_lua.png`.

### 7b. Mảnh và rig dạng 1 (2026-11-13)

- **Cách dựng (quyết định của Claude):** các tấm đá DÙNG LẠI mảnh dạng 2 (cùng thiết kế, đã kiểm ở mọi clip; khỏi gen lại 8 tờ và khỏi lệch
  nét giữa hai dạng); chỉ vẽ mới thứ khác dạng 2 bằng MỘT tờ `gui_gpt/golem_lua_non/luot_2_manh_1.txt` → `tai_ve/M_1.png` (131 s, ra đủ 10
  mảnh ngay lượt đầu): ba ngọn lửa nhỏ gốc hẹp, sáu vuốt cụt, lõi lửa dịu (tim vàng nhỏ).
- `golem_lua_non.py manh` → `golem_lua_non/manh/` (51 mảnh): bàn tay ×0,86 quanh chỗ chạm đất, mắt ×1,15; bốn lỗ tắt: mảnh nguội nướng thẳng
  vào tấm (`dinh`, `dau`, `co_tay_gan`, `hong`), bỏ bốn lưỡi lửa nhỏ và `hong_vanh` (không còn lửa thì chỉ lộ một vệt cong tối dưới khối ngực);
  lửa GPT vẽ to hơn concept → thu ×0,72 quanh đầu gốc, đầu gốc đặt đúng `goc_lua` của dạng 2; vuốt GPT vẽ to (kèm phần "bị bàn tay che") mà rig
  vẽ vuốt TRƯỚC bàn tay → thu về 0,74 chiều cao ô bố cục, ba vuốt rải đều (22 / 52 / 80 % bề ngang bàn tay), 45 % phía trên chờm lên mép dưới
  bàn tay (bản đầu để nguyên cỡ: vuốt như giọt nước treo dưới tay; bản hai đặt theo ô vuốt cũ: dồn cục, một vuốt rời khỏi tay); lõi về đúng cỡ
  và chỗ của lõi dạng 2, `loi_tat` đổi màu bằng mã. Ghép so concept A: `manh/_so_ghep.png` (5,8 % điểm lệch màu: nét tấm đá của hai lần vẽ).
- Rig: `GL_NON=1 golem_lua_rig.py` (cùng script, cùng clip; `GL_DANG` là biến số dạng của golem_lua.py nên dùng tên khác): mảnh ở
  `golem_lua_non/manh`, khung concept ↔ rig lấy của dạng 2 (`MANH_KHOP`). Kết quả `golem_lua_non/rig/`: 76 xương, 51 slot, 399 đỉnh, 9 clip,
  `.atomik` 356 KB, cao game 543; mọi clip về idle 0 px (skill → skill_land nối như dạng 2).
- Tiến hóa: `golem_lua_non_th.py` (mo_xe/atomik_dang.gop_tien_hoa; dạng 2 trong rig gộp × 1,196 = 1,1 / 0,92): `golem_lua_non_th.atomik` 534 KB,
  164 xương, 107 slot, 10 clip. gop_tien_hoa đặt alpha 1 cho MỌI slot trong `evolve` → 22 slot ẩn sẵn (mắt tắt, lõi tắt, mảnh nguội của hai
  rig) phải sửa khoá về 0, không thì lộ lớp nguội đè lên. `kiem_dang.py`: khung cuối evolve ↔ idle 0 của dạng 2 lệch 0,000; trang runtime
  Spine thật `rig/xem_th/golem_lua_non.html` nạp đủ 10 clip; tờ `rig/khung_evolve.png`, `rig/soi_clip.png`.
- Vào game: `golem_lua_non_th.py chep` → `Resources/nham_than_1` (.atomik + chân dung); refresh, "Gắn dạng .atomik" (prefab giữ 2 dạng), "Chụp
  thử" `Library/PokiHeroShots/nham_than_atomik_1.png` (đủ idle, hit, attack, cast, skill, evolve). Tour trận ở 1 sao (menu mới "riêng Nham Con
  (dạng 1)"): ba lửa nhỏ, đòn thường, phun lửa, cầu lăn + hiệu ứng chạy như dạng 2. EditMode 102/103 (như trước). Không đổi dữ liệu, golden.
- CHƯA: xem clip tiến hóa trong màn nâng sao thật; appear / die trong trận; phía địch; Android; chưa commit.

## 8. VFX riêng (2026-11-13): `Assets/01 Script/Game/Battle/HatNham.cs`

- Đi đường "n_" (phát từ đầu clip, có `lead`): `StageView.FireFx` nham_than = ("phun", "n_cau_lan"); bảng mới `StageView.HoaAtk`
  nham_than = "n_nham_va" (nối vào `FireAtk`); `HatLua.AtkLao` nhận "n_nham_va"; `PlayNuoc` thêm hai mã. Chiêu mana giữ "phun".
- `n_cau_lan`: bụi đá lúc bật nhảy và lúc cầu rơi lại; vệt lửa theo quả cầu suốt quãng lăn (chép quỹ đạo AolaSticker.Jump nhánh Rams); chạm:
  chớp nổ lớn + quạt lưỡi lửa theo hướng tông + dăm đá tro + vòng lửa; bật về: than hồng, lửa nhỏ, khói mỏng; đáp đất: vòng bụi, bụi đá, bụi
  trượt. `n_nham_va`: bụi bật khỏi chỗ; nện đầu: chớp toé nhỏ, tia văng + dăm đá hai bên, bụi dưới chân đối thủ bị ép ra.
- Tour ("riêng Nham Thần", nay chụp cả đòn thường `nham_than_danh_*`): soi tờ khung ba lượt; lượt đầu vệt lửa hở một quãng sau quả cầu →
  sinh lửa ngay trong nửa sau quả cầu. Một lần lỗi biên dịch do tự chèn chú thích cuối dòng giữa lời gọi nhiều dòng (đã sửa).
- EditMode 102/103 (như trước). Công thức ghi ở skill pokiclash-fx-congthuc mục 5e.
- CHƯA: xem trong hộp chi tiết tướng (HeroViewer); phía địch (golem đứng trên trái, lăn xuống phải) chưa chụp; chưa thử Android.
- Hộp chi tiết tướng: thêm menu "PokiClash/Thử/Đảo Hỏa: riêng Nham Thần trong hộp chi tiết tướng (đang Play)" (ảnh `hoa_fx/xem_nham_than_*`):
  phun lửa ra đúng họng; chiêu cuối đủ bụi, vệt lửa, chớp nổ ở đích ảo, vòng bụi lúc đáp (trong ô xem tướng không bay nên vệt lửa nằm trong
  quả cầu). Phía địch vẫn chưa chụp.

## 9. Trận thật ải 15 đảo Hỏa (người dùng 2026-11-13: "cho vào game đi")

Bản trong `Resources/nham_than_1`, `nham_than_2` trùng mã băm bản xuất mới nhất (dạng 1 có evolve, dạng 2 đã sửa bung người). Menu mới
"PokiClash/Thử/Đảo Hỏa: trận thật ải 15, Nham Thần hai phía (đang Play)" (`HoaFxTour.RunTran`: ải 85 "Sườn Núi Khói", đội mình một Nham Thần
sao cuối cấp 55, tự đánh nhịp thường, chụp `hoa_fx/tran_<n>.jpg` tới khi hộp kết quả hiện). Chạy hai lượt (thua / thắng, 2 hiệp):
- Màn VS và bảng tên địch: chân dung và tên **Nham Con Lv52** (dạng 1); địch đứng trên trái, nhìn phải, nhỏ hơn dạng 2 của mình.
- **Tiến hóa trong trận**: địch tụt máu tới ngưỡng → "Tiến Hóa", mờ chéo sang Nham Thần, bảng tên đổi thành Nham Thần, máu đầy lại.
- Đòn thường phía địch (lao từ trên trái xuống): vòng bụi ở chỗ bật, chớp toé + số sát thương ở đầu golem mình; phía mình cũng vậy.
- Chiêu mana "Phun Nham" phía mình: luồng lửa từ họng lên địch ở trên trái.
- **Chết**: "Gục!" → lõi và mắt tắt, lửa lụi, các mảnh rơi thành đống rồi tan.
- Bẫy của tour: `ctl.Battle.phase` là trạng thái của LUẬT (tính xong trước khi sân diễn); chờ `App.Modals.Count > 0` mới là hết trận trên màn.
- CHƯA thấy trong trận thật: chiêu cuối (không lượt nào đủ điều kiện ra chiêu trong 2 hiệp; đã soi bằng tour riêng), chiêu của phía địch ở
  dạng 1; Android; chưa commit.
