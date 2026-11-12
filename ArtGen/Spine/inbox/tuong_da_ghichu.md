# Tinh linh tượng đá cổ giữ rừng (`tuong_da`): tướng thứ 3 đảo Mộc

Bắt đầu 2026-11-12. Con gốc của rig: `monster_3423` (game tham khảo, kho `D:\Ripper\SwordxStaff`). Xương, lưới, chuyển động gốc là
của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là thiết kế của mình.

## 1. Lời dặn của người dùng (2026-11-12)

- Concept: tinh linh **tượng đá cổ bảo vệ rừng, bị quấn rêu xanh**. Gen lại các bộ phận **khác đi chút**, theo thiên hướng rừng cây,
  đá rừng hơn; ở giữa có thể là một **lõi pha lê xanh** hoặc lõi gì đó thể hiện **trái tim khu rừng**.
- idle: giống con gốc là ổn. walk: cũng có thể làm giống họ.
- appear: từng bộ phận bay vào xếp thành hình.
- Đánh thường: lao tới đấm vòng một phát.
- Chiêu mana: đưa hai tay lên trước, bắn hai bàn tay vào đối thủ.
- Chiêu cuối: đưa hai tay lên trời, xoè bàn tay tụ một quả cầu năng lượng (**làm thêm fx**: khi tụ có gió / lá bị hút xung quanh vào
  cầu), sau đó hai tay đổ về phía trước kiểu ném vào đối thủ.
- die: lõi tắt ngỏm, chân tay từ đó rụng rời.

Xem hai hướng concept (cùng buổi): **"ưng hướng 2 hơn"** (`gac`: gạc cây, lõi hạt mầm), sửa:
- "chỗ nối vai với tay thay lá thành những **viên đá nhỏ**";
- "phần đầu nhìn bị **giống con gốc quá, đổi kiểu dáng**" (bản nháp giữ mào rộng hai cánh của con gốc, chỉ thêm rêu và gạc).

Màu, chi tiết, tên, số dạng: người dùng chưa dặn. Bảng màu và chi tiết ở mục 3 là **đề xuất của Claude**.

## 2. Mổ rig gốc (`<SXS>/scan/monster_3423/`: `info.json`, `att_goc.json`, `manh_anh.png`, `manh_dang_goc.png`, `parts/`, `khung/`, `sample_dk.json`)

79 xương, 79 slot (39 hình × 2 bộ + `shadow`), 13 clip. Con gốc nhìn sang PHẢI: không lật. Không mặt, không chân, lơ lửng.
**Mọi mảnh là lưới CỨNG bám một xương** (ba dây leo bám hai xương): hình bóng từng mảnh của mình tự do, chỉ cần đúng chỗ, cỡ, thứ tự chồng.
**FK thuần**: bốn IK tay (`SR1/2`, `SL1/2`) mặc định tắt, chỉ `skill_01_X`, `skill_02` bật.

Cây xương:
- `bone` → `bone31` → `bone2` (THÂN: vòng ngực dưới `P_shenti02` + vỏ sau `P_shenti03`); con của `bone2`: ba chóp đá `bone24–26`
  (`P_shitou01–03`), pha lê lõi `bone27` (`P_shuijing`), khoá `bone43` (`P_zhuangshi`).
- `bone2` → `bone3` → `bone4` (ngực trên) → `bone30` (vòng ngực trên `P_shenti01` + dây leo), `bone5` (quả cầu cổ `P_qiu`) → `bone6`
  (mào đầu `P_tou`), `bone44` (đai vai).
- Tay GẦN (R của họ, bên TRÁI người xem, vẽ trước thân): `bone44` → `bone7` → `bone17` (bắp tay vô hình; con: tấm vai `bone28`
  = `P_jianjiaR01/02` + dây leo + lá, ba pha lê nhỏ `bone36–38`) → `bone18` (tảng cẳng tay `P_shoubiR01` + đai `R02`) → `bone19` (bàn
  tay) → ngón `bone20, 21, 22` → `bone23`.
- Tay XA (L, bên phải, vẽ sau thân): `bone9` → `bone10` (tấm vai `bone29`, bốn pha lê nhỏ `bone39–42`) → `bone11` → `bone12` → ngón
  `bone13, 14, 15` → `bone16`.
- **Bộ mảnh thứ hai** (slot `P_*2..`, mặc định trống, cùng ảnh): mỗi mảnh / cụm một xương rời là con của `bone`, đặt cao hơn bộ chính
  811,4 đơn vị; 30 cụm (vai + dây leo một cụm; cẳng tay + đai một cụm, bàn tay là con cẳng tay, ngón là con bàn tay). Họ dùng cho
  `die_01` (nổ tung lên rồi rơi thành đống). Mình dùng cho `td_die` và `td_appear`.

Thứ tự vẽ (sau → trước): vai xa (mặt trong), bàn tay xa, cẳng tay xa + đai, pha lê nhỏ xa, ngón xa, tấm vai xa, dây leo, chóp đá to,
vỏ ngực sau, PHA LÊ LÕI, vòng ngực dưới, vòng ngực trên, dây leo, hai chóp nhỏ, khoá, lá, vai gần (mặt trong), pha lê nhỏ gần, tấm
vai gần, dây leo, ngón gần, bàn tay gần, cẳng tay gần + đai, quả cầu cổ, mào đầu.

Clip của họ: `idle_01` 2 s (cả khối nhấp nhô ~45 đơn vị, tay đung đưa), `run_01` 1,07 s (chúi tới, tay so le), `skill_01_1..3 / X`
1,23 s (giơ hai tay nện xuống), `skill_02` 1,5 s (nhảy lên, vung tay gần), `skill_03` 1,47 s (bay lên, nện hai tay), `hit_01/02`,
`block_01`, `stun_01`, `die_01` 1 s.

## 3. Concept (đề xuất của Claude)

Script: `ArtGen/Spine/tuong_da.py` (`part_goc`, `bo_cuc [pha_le|gac]`), `build_tuong_da.py` (gói `gui_gpt/tuong_da_1/`).
Sơ đồ bố cục = khối từng mảnh của rig làm trơn mạnh, tô phẳng theo nhóm màu của mình (không đính ảnh con gốc).

Bảng màu: đá tượng kem xám `#C4BEA6` (mặt trong `#8C8878`), đá tảng rừng nâu xám `#6E685C`, rêu `#629C48`, dây leo / lá `#46803E`,
rễ và gạc nâu `#805836`, lõi lục tươi `#40CE8C` (nét / mặt đậm `#1E9668`), mực `#2B2118`.

Lượt 1, hai hướng (`inbox/tuong_da_1/so_hai_huong.png`):
- `pha_le` (`tai_ve/L1_pha_le.png`): lõi pha lê lục thoi, mào đá khắc hình lá, mảnh pha lê nhỏ ở khớp tay.
- `gac` (`tai_ve/L1_gac.png`): hai nhánh gạc cây trên mào, lõi là hạt mầm lục có mầm hai lá và rễ bám vòng ngực, lá bay ở khớp tay.
  **Người dùng chọn hướng này**, kèm hai chỗ sửa (mục 1).

Lượt 1b (vẽ lại y hệt `L1_gac.png`, chỉ đổi đầu và bảy chiếc lá → bảy viên đá nhỏ nâu xám), hai kiểu đầu cho người dùng chọn:
`luot_1b_dau_tru.txt` → `tai_ve/L1b_tru.png` (khối trụ đá cụt), `luot_1b_dau_vom.txt` → `tai_ve/L1b_vom.png` (vòm đá tròn). Gạc mọc
từ rêu trên đỉnh đầu mới. Tờ so: `inbox/tuong_da_1/so_dau.png`.

Bài học: người dùng nói "gen lại các bộ phận khác đi chút" mà tôi vẫn để mào đầu (mảnh dễ nhận nhất của con gốc) nguyên hình bóng trên
sơ đồ → bị trả "phần đầu giống con gốc quá". Mảnh cứng một xương thì đổi hẳn dáng ngay từ sơ đồ, nhất là mảnh làm nên bóng dáng cả con.

## 4. Clip (dựng ở tầng điều khiển của rig gốc: `tuong_da_clip.py`)

Xem thử trên rig gốc (hình của họ, nội bộ): `<SXS>/scan/monster_3423/lam_clip/xem/xem.html` (`tuong_da_clip.py song`: trang sống 60
khung/giây, nút từng clip, tốc độ 1× / 0,5× / 0,25×; vòng tròn lục = chỗ và cỡ quả cầu năng lượng; dòng "lõi" = độ sáng lõi).

Vì rig là FK thuần và mảnh cứng, script tự tính động học thuận (`fk`) và đặt xương theo toạ độ THẾ GIỚI (`Dang.dat`, `tay()`: đặt gốc
và góc tảng cẳng tay so với ngực; bắp tay vô hình quay một phần theo, tấm vai quay ít hơn). `td_die`, `td_appear` dùng bộ mảnh thứ
hai: mỗi cụm một phép dời + quay quanh tâm cụm so với chỗ ở khung 0 idle (`roi_tu_do`), script tính ngược ra biến đổi riêng.

| clip | dài | nội dung | sự kiện |
|---|---|---|---|
| td_idle | 2,0 s lặp | nguyên idle_01 + nhịp đập của lõi (xương `bone27` phồng 6% hai nhịp mỗi giây) | |
| td_walk | 1,07 s lặp | nguyên run_01 | |
| td_attack | 1,40 s | thu người, kéo tảng tay gần ra sau lên cao 0–0,20; LAO 0,20–0,46; đấm VÒNG 0,46–0,58: tảng tay quét từ sau, xuống thấp qua trước thân (phóng 1,16 lúc gần ống kính), móc lên ngang ngực phía trước; khựng tới 0,78; nhảy lùi về 1,12 | trung 0,58 |
| td_cast | 1,90 s | hai cẳng tay đưa lên chĩa về trước 0,36 (tay gần thấp phía trước, tay xa bên phải); gồng rung, kéo lùi; bắn CẢ TẢNG CẲNG TAY gần 0,56, xa 0,66 (tảng đá + đai rễ + bàn tay; tấm vai giật ngược); tới đích sau 0,16 s, ghim 0,12 s, lộn một vòng bay về 0,36 s, lắp lại | tu 0,36; phun g 0,56; phun x 0,66; trung 0,72 / 0,82; ve 1,20 / 1,30 |
| td_skill | 2,80 s | hai tay giơ lên trời, xoè ngón 0,42; tụ cầu tới 1,50 (người rung mạnh dần, nhấp nhô, tay dang dần, pha lê nhỏ bị hút lên); ngả sau 1,66; đổ hai tay về trước ném 1,80; dư lực tới 2,20; thu về | tu 0,42; day 1,50; nem 1,80; trung 1,98 |
| td_appear | 2,30 s | lõi hạ xuống trước (0–0,34); từng cụm bay vào (hiện dần 0,09 s, vọt quá rồi khớp): ngực dưới, ngực trên, chóp đá, khoá, quả cầu cổ, mào đầu 0,92, vai, cẳng tay, bàn tay, ngón, pha lê nhỏ; 1,52 ráp xong đổi về bộ chính, gồng một nhịp (tay bung, xoè ngón, lõi phồng) | loi 0; ghep dau 0,92; xong 1,52 |
| td_hit | 0,5 s | nguyên hit_01 | |
| td_die | 1,70 s | giật ngửa, lõi chập chờn rồi TẮT 0,34; các mảnh xệ xuống; rụng dần từ 0,42: chóp đá, ngón, pha lê, bàn tay, cẳng tay, khoá, vai, ngực, lõi, quả cầu cổ lăn đi, mào đầu 0,84 úp lên đống; nằm yên từ ~1,3 | tat 0,34; roi 0,44; cham_dat 0,90; cham_dat dau 1,26 |

Kênh riêng cho rig của mình (`<scan>/kenh_rieng.json`): `loi` 0..1 (đổi hình lõi sáng / tắt), `cau` (bán kính 0..1, x, y thế giới: chỗ
gắn VFX cầu năng lượng), `ban` (quãng bay 0..1 của hai bàn tay; trên rig gốc xem thử là 620 đơn vị, vào game phải đặt bàn tay lên
xương `fly_*` để game co theo khoảng cách đối thủ), `bay` (cung lao đòn thường trên xương `move`: tới trước 430).

Việc của rig mình sau này: đầu mới hẹp hơn mào cũ (đổi tâm, không ảnh hưởng clip); bảy viên đá nhỏ thay pha lê nhỏ (cùng xương);
lõi hai hình (sáng, tắt); bàn tay trên `fly_*` cho chiêu mana; xương `cau` cho VFX.

## 5. Mảnh và rig (2026-11-12, sau khi người dùng chốt đầu kiểu A: "tôi thích A hơn" → `tai_ve/L1_duyet.png` = `L1b_tru.png`)

Trình tự: `build_tuong_da.py` (năm file `luot_2_manh_A..E.txt`) → `gen.py` từng tờ → `tuong_da_manh.py lam` → `tuong_da_clip.py mau`
(qua `khoa.py chrome`) → `tuong_da_rig.py` (qua `khoa.py nang`) → `mo_xe/thu_xem.py <rig/xem.html>`.

- **Năm tờ "đúng chỗ, đúng cỡ"** (mỗi tờ vẽ lại concept, chỉ giữ vài mảnh KHÔNG chồng nhau, vẽ đủ phần khuất; ~70 giây một tờ):
  A đầu + tấm vai xa (vẽ đủ nửa khuất sau ngực) + chóp đá to (vẽ đủ đỉnh); B vòng ngực đứng (vành kín, lỗ giữa trắng) + hai khối lòng
  bàn tay; C đai dưới (vành bầu dục kín, vách trong sẫm) + hai rễ nâu; D hạt mầm (trứng kín, không rễ); E quả cầu cổ, tấm vai gần,
  khoá, hai tảng cẳng tay + đai rễ (không bàn tay), hai chóp nhỏ, bảy viên đá nhỏ.
- **Cắt** (`tuong_da_manh.py`): nền = trắng thông ra mép + lỗ trắng kín lớn; mỗi cụm liền là một mảnh, gán tên theo tâm ước chừng.
  Đai dưới ra hai mảnh cùng xương `bone2`: `dai_sau` (cả vành, vẽ sau hạt mầm) và `dai_truoc` (phần dưới y = 628 + hai rễ, vẽ đè
  trước vòng ngực đứng). Mười viên đá ngón tay lấy thẳng từ concept: vùng màu đá khép kín bởi nét mực, dựng đủ bằng bao lồi, tô chỗ
  khuất, kẻ lại viền. Lõi tắt (`loi_tat`) = hạt mầm đổi màu xám đá bằng mã.
- **Rig** (`tuong_da_rig.py`): đủ xương của họ (cả bộ rời thứ hai); mỗi mảnh là ô cứng một xương, đặt theo chỗ trên concept (khung
  concept khớp hệ rig gốc bằng bình phương tối thiểu trên tám mốc); mỗi mảnh thêm một slot `~2` trên xương rời bộ hai (die, appear).
  Thứ tự vẽ: bàn tay xa, ngón xa, cẳng tay xa, đá nhỏ xa, vai xa, chóp to, đai sau, lõi, vòng ngực đứng, đai trước, hai chóp nhỏ,
  khoá, đá nhỏ gần, vai gần, bàn tay gần, ngón gần, cẳng tay gần, đầu, quả cầu cổ.
  Nắm tay bay của chiêu mana: bản sao lòng bàn tay + ngón trên `nam_g/x` (con của `fly_g/x`, con của root), `far` = chỗ đối thủ;
  `game.far = ["cast"]`. Xương `cau` (con của root): chỗ và cỡ quả cầu năng lượng cho VFX.

Sửa trong lúc cắt (2026-11-12):
- Lòng bàn tay Codex vẽ to và thấp hơn chỗ nó nấp trong concept (thò dưới các ngón): co cả mảnh về khung đo trên concept (`BAN_KHUNG`).
- Vòng ngực đứng Codex vẽ tròn đều nên đáy thò dưới đai: ép dọc cả mảnh cho đáy về y = 712 (`NGUC_DAY`).
- Ngón tay dựng bằng bao lồi từ concept ra viền mảnh, méo: thay bằng CON DẤU là viên đá tròn `da_g2` của tờ E (xoá nét mặt cắt), mỗi
  ngón một cỡ / góc xoay; tâm và số ngón (bốn mỗi tay) dò trên concept. Bài học: viên tròn bị che thì mượn một viên tròn kín Codex
  đã vẽ, đừng tự kẻ viền.
- Thứ tự vẽ bàn tay: lòng bàn tay → tảng cẳng tay → ngón (đầu cụt của tảng cẳng tay đóng vai mu bàn tay như concept; lòng bàn tay
  chỉ lộ khi nắm tay bay đi).
- Tách rễ nâu của đai phải so R − G (đá kem cũng có R − B lớn): bản đầu bắt nhầm cả vành đai thành "rễ".

Kết quả `inbox/tuong_da_1/rig/` (bản đầu): 81 xương, 74 slot (32 mảnh × 2 bộ + 10 slot nắm tay bay), 296 đỉnh, 8 clip (appear, idle,
walk, attack, cast, skill, hit, die), atlas 632 × 656, `.atomik` 157 KB; nạp lại `.atomik` lệch ≤ 0,23 px; mọi clip nối về idle 0 px,
appear khung đầu trống, die khung cuối trống; `xem.html` chạy (thu_xem: đủ 8 nút, không lỗi JS); runtime Spine thật dựng attack, cast,
skill (`rig/that/`). Chiều cao game 281 (đỉnh rêu trên đầu, không tính gạc). Khung concept khớp hệ rig gốc 1,362 px / đơn vị, lệch mốc
12–47 px (bố cục concept giữ nguyên, không ép từng mảnh về chỗ mảnh của họ).
Đã soi bằng bộ vẽ Python: idle cận, tờ khung cast, skill, appear, die. CHƯA soi cận từng khung attack, walk, hit trên hình của mình.

Người dùng xem rig (2026-11-12), gửi ảnh chụp cả tảng cẳng tay gần: **"chiêu bắn ý tôi là bắn cả phần này nữa chứ không chỉ ngón tay"**
→ thứ bay đi là cả tảng cẳng tay + đai rễ + lòng bàn tay + ngón (bản đầu chỉ bắn lòng bàn tay + ngón). Sửa: `tuong_da_clip.py` (xem
thử dời xương `bone18` / `bone11`; tấm vai giật ngược lúc rời, nảy lúc lắp), `tuong_da_rig.py` (`TAY_BAY` = xương cẳng tay, bản sao
bay gồm `ban`, `cang`, `ng_*`; rig thành 76 slot). Về thì lộn đúng một vòng (−360°) để khớp hướng lúc lắp lại.

Người dùng xem rig sau khi sửa chiêu mana (2026-11-12): **"con này ổn đấy, rất tốt"**. Rig và clip dạng này coi như được duyệt. Cách làm đã ghi vào skill pokiclash-spine-rig mục 25.

## 5b. Hai dạng, tên, suất (người dùng chốt 2026-11-12)

- "thay vào, thay tên id luôn cho phù hợp"; tên "bạn tự đặt"; "làm 2 dạng thôi, con vừa rồi là dạng 2, lát nữa bạn làm dạng 1"; chỉ số và
  thẻ chép theo Dê Hoa.
- Claude đặt: id **gac_da**, tên **Gạc Đá**, danh hiệu "Tượng cổ giữ rừng", dòng "Dòng Gạc Đá"; dạng 1 **Mầm Đá** (gac_da_1), dạng 2
  **Gạc Đá** (gac_da_2). Thay hẳn de_hoa (Dê Hoa, ba dạng) ở suất thứ ba đảo Mộc (ải 10 "Đồi Nấm").
- Thư mục làm việc: con đã duyệt chuyển sang inbox/tuong_da_2, gui_gpt/tuong_da_2 (rig tuong_da_2.atomik); mọi script đọc dạng ở biến
  môi trường **TD_DANG** (1 | 2, mặc định 2).
- **Dạng 1 "Mầm Đá"** (thiết kế là đề xuất của Claude, chờ duyệt concept): cùng rig, cùng clip, mỗi mảnh nằm quanh đúng chỗ dạng 2. Đầu
  tròn to như chum đá, không gạc mà một mầm hai lá; hạt mầm chưa nảy; tấm vai còn 3/4, một mảng rêu, không dây leo; cẳng tay 80%, một
  vòng rễ mảnh; bốn viên đá nhỏ. Prompt gui_gpt/tuong_da_1/luot_1_concept.txt (ảnh mẫu: concept dạng 2), ảnh
  inbox/tuong_da_1/tai_ve/L1_concept.png (lượt đầu, 75 giây, đạt điểm kiểm). Tờ so: inbox/tuong_da_1/so_hai_dang.html.

## 5c. Dạng 1 xong, chuẩn bị vào game (2026-11-12, người dùng: "dạng 1 duyệt")

- Dạng 1: năm tờ mảnh (toạ độ đo lại trên concept dạng 1, build_tuong_da.py MANH1, TD_DANG=1), cắt ra 29 mảnh, ghép so concept lệch
  2,7% điểm. Rig TD_DANG=1: cùng xương, cùng clip; gộp bản nhẹ của dạng 2 (TD_NHE=1, ảnh 0,44 px / đơn vị) làm clip evolve (Mầm Đá
  thụp xuống gồng, lõi phồng → tan → Gạc Đá hiện, ưỡn, bung tay → về idle): khung cuối trùng khung 0 idle dạng 2 (0,00 px).
  inbox/tuong_da_1/rig: 162 xương, 146 slot, 9 clip, .atomik 183 KB; xem.html chạy đủ 9 nút. Chiều cao game dạng 1 = 301, dạng 2 = 281
  (đỉnh rêu trên đầu; cỡ trong trận do size 0,92 / 1,1 của heroes.json).
- Script đổi dữ liệu: quai/doi_gac_da.py (--kiem chạy được: 15 file; CHƯA ghi). Đọc saveVersion hiện tại N, thêm bước [N] =
  MigrateGacDa, nâng N + 1 (không ghi cứng: phiên tinh linh cũng đổi hoa_nhuy → mam_u bằng doi_mam_u.py, đã hẹn họ chạy trước).
- VFX soạn sẵn ngoài Assets: inbox/tuong_da_2/HatDa_nhap.cs.txt (partial HatLua): NDaVa (hai tảng tay nện trúng: đá vụn, bụi; mã
  n_da_va, phát từ đầu clip kèm lead), NCauLa (chiêu cuối, mã n_cau_la: GatherLa hút lá + sợi gió + vòng co về cầu, CauLa quả cầu ba
  lớp có lá bay quanh, cầu theo tay rồi bay tới, LaNo lúc trúng). Còn phải thêm: case trong HatNuoc.PlayNuoc, dòng StageView.MocFx
  { "gac_da", ("n_da_va", new[] { "n_cau_la", "n_cau_la" }) }, dòng WThemes gac_da (lục ngọc 30,150,104 / 64,206,140 /
  170,236,196; họa tiết giap màu đá).
- ĐANG CHỜ: người dùng đang tự Play trong Unity Editor (14:37) nên chưa phiên nào ghi vào Assets. Thứ tự đã hẹn: phiên tinh linh
  (assets-56) đổi mam_u trước, nhắn "xong, Unity rảnh", rồi tới Gạc Đá.

## 5d. ĐÃ VÀO GAME (2026-11-12 chiều): id gac_da thay de_hoa, hai dạng, VFX

Sau khi phiên tinh linh đổi mam_u xong ([7], saveVersion 8), tới lượt Gạc Đá:
- quai/doi_gac_da.py (ghi thật, 15 file): heroes / cards / stages / balance.json, Golden (chỉ id; phần "migrate" của roster.json GIỮ
  de_hoa vì là đầu ra của riêng bước v3: bản đầu đổi nhầm, RosterTests.DiChuyenBanLuuV3 hỏng, đã sửa script), IslandGen Intro(10),
  SaveData: Migrations[8] = MigrateGacDa (GacDaMap de_hoa → gac_da), saveVersion 9, CoreGoldenTests 9, da_nhan.json.
- Unity (MCP HTTP cổng 8080, gọi bằng script nhỏ mcp.py ở scratchpad): manage_asset move đổi tên prefab de_hoa → gac_da và thư mục
  Resources/de_hoa_1, 2 → gac_da_1, 2 cùng ba file bên trong (công cụ báo lỗi nhưng đã đổi, giữ GUID); xoá Resources/de_hoa_3; chép
  tuong_da_<k>.atomik + chan_dung.png (512) đè lên; refresh; Nhập dữ liệu; Gắn dạng .atomik (prefab gac_da còn hai dạng).
- Golden phụ thuộc số dạng (Dê Hoa ba dạng → Gạc Đá hai dạng): menu "Đảo 70 ải: sinh lại" (stages.json không đổi), "Tính lại golden
  islands, roster, cardtext, zones", "Tính lại golden theo danh sách tướng", "Tính lại golden sim, tướng trên nút ải" rồi
  quai/golden_ghep.py (mới: ghép Temp/GoldenRecalc.json vào sim.json, roster leads, battles.json, battle_events.json; chỉ đổi ô khác):
  sim đảo Mộc ải 220 (ải 10), 4 nút leads (220, 222, 224, 228), 1 trận golden hạt giống 3718467 (boss Gạc Đá tiến hóa một lần).
  Test golden trận đọc file qua biến tĩnh: sau khi ghi golden phải cho Unity nạp lại domain (refresh có biên dịch) rồi mới chạy test.
- EditMode 102/103 (chỉ hỏng PrefabOnlyTests có từ trước).
- VFX: Assets/01 Script/Game/Battle/HatDa.cs (partial HatLua): NDaVa (mã n_da_va: hai cú nện, đá vụn = Shard nhuộm màu đá, bụi), NCauLa
  (mã n_cau_la: GatherLa hút lá + sợi gió + vòng co; CauLa quả cầu ba lớp có hai vòng xoắn và ba lá bay quanh; cầu theo tay rồi bay tới;
  LaNo lúc trúng, lá rơi). HatNuoc.cs: WThemes gac_da (lục ngọc, họa tiết giap màu đá), hai case trong PlayNuoc. StageView.MocFx:
  { gac_da, (n_da_va, [n_cau_la, n_cau_la]) }.
- **Lỗi đã gặp**: hai tảng tay chỉ bay nửa đường. StageView chỉ đặt đích bay (AolaSticker.Far) cho clip Attack và Skill; thêm
   (AolaSticker.Far tự bỏ qua clip không khai far; lúc sửa chỉ gac_da_1, gac_da_2 khai cast trong game.far).
- Lần chạy đầu cầu nhỏ (0,19 chiều cao) và lá thưa: tăng cầu 0,25, lá 70 / giây cỡ 6–10,5, sợi gió dài hơn.
- Soi: menu "PokiClash/Thử/Đảo Mộc: đá và cầu năng lượng Gạc Đá, chiêu mana và chiêu cuối từng dạng (đang Play)" (MocFxTour.TryDa),
  ảnh Temp/PokiShots/thuy_fx/gac_da_*; tờ cắt cận inbox/tuong_da_2/trong_tran.jpg. Đã xem: tên Gạc Đá, thẻ Quyền Đá Bay / Cầu Tim Rừng,
  tảng tay tới đúng đối thủ, cầu tụ – ném – nổ. CHƯA xem: appear, die, evolve, hộp chi tiết tướng trong game; sợi gió còn hơi thô.

## 5d. ĐÃ VÀO GAME (2026-11-12 chiều): id gac_da thay de_hoa, hai dạng, VFX

Sau khi phiên tinh linh đổi mam_u xong ([7], saveVersion 8), tới lượt Gạc Đá:
- `quai/doi_gac_da.py` (ghi thật, 15 file): heroes / cards / stages / balance.json, Golden (chỉ id; phần "migrate" của roster.json GIỮ
  `de_hoa` vì là đầu ra của riêng bước v3: bản đầu đổi nhầm, `RosterTests.DiChuyenBanLuuV3` hỏng, đã sửa script), IslandGen `Intro(10)`,
  SaveData: `Migrations[8] = MigrateGacDa` (`GacDaMap` de_hoa → gac_da), saveVersion 9, CoreGoldenTests 9, da_nhan.json.
- Unity (MCP HTTP cổng 8080, gọi bằng script nhỏ `mcp.py` ở scratchpad): `manage_asset move` đổi tên prefab de_hoa → gac_da và thư mục
  `Resources/de_hoa_1, 2` → `gac_da_1, 2` cùng ba file bên trong (công cụ báo lỗi nhưng đã đổi, giữ GUID); xoá `Resources/de_hoa_3`; chép
  `tuong_da_<k>.atomik` + `chan_dung.png` (512) đè lên; refresh; Nhập dữ liệu; Gắn dạng .atomik (prefab gac_da còn hai dạng).
- Golden phụ thuộc số dạng (Dê Hoa ba dạng → Gạc Đá hai dạng): menu "Đảo 70 ải: sinh lại" (stages.json không đổi), "Tính lại golden
  islands, roster, cardtext, zones", "Tính lại golden theo danh sách tướng", "Tính lại golden sim, tướng trên nút ải" rồi
  `quai/golden_ghep.py` (mới: ghép `Temp/GoldenRecalc.json` vào sim.json, roster leads, battles.json, battle_events.json; chỉ đổi ô
  khác): sim đảo Mộc ải 220 (ải 10), 4 nút leads (220, 222, 224, 228), 1 trận golden hạt giống 3718467 (boss tiến hóa một lần).
  Test golden trận đọc file qua biến tĩnh: sau khi ghi golden phải cho Unity nạp lại domain (refresh có biên dịch) rồi mới chạy test.
- EditMode 102/103 (chỉ hỏng `PrefabOnlyTests` có từ trước).
- VFX: `Assets/01 Script/Game/Battle/HatDa.cs` (partial HatLua): `NDaVa` (mã `n_da_va`: hai cú nện, đá vụn = `Shard` nhuộm màu đá,
  bụi), `NCauLa` (mã `n_cau_la`: `GatherLa` hút lá + sợi gió + vòng co; `CauLa` quả cầu ba lớp có hai vòng xoắn và ba lá bay quanh; cầu
  theo tay rồi bay tới; `LaNo` lúc trúng, lá rơi). `HatNuoc.cs`: WThemes `gac_da` (lục ngọc, họa tiết `giap` màu đá), hai case trong
  `PlayNuoc`. `StageView.MocFx`: `{ "gac_da", ("n_da_va", new[] { "n_cau_la", "n_cau_la" }) }`.
- **Lỗi đã gặp**: hai tảng tay chỉ bay nửa đường. StageView chỉ đặt đích bay (`AolaSticker.Far`) cho clip Attack và Skill; thêm
  `|| a.clip == Cast` (`AolaSticker.Far` tự bỏ qua clip không khai far; lúc sửa chỉ gac_da_1, gac_da_2 khai cast trong `game.far`).
- Lần chạy đầu cầu nhỏ (0,19 chiều cao) và lá thưa: tăng cầu 0,25, lá 70 / giây cỡ 6–10,5, sợi gió dài hơn.
- Soi: menu "PokiClash/Thử/Đảo Mộc: đá và cầu năng lượng Gạc Đá, chiêu mana và chiêu cuối từng dạng (đang Play)" (`MocFxTour.TryDa`),
  ảnh `Temp/PokiShots/thuy_fx/gac_da_*`; tờ cắt cận `inbox/tuong_da_2/trong_tran.jpg`. Đã xem: tên Gạc Đá, thẻ Quyền Đá Bay / Cầu Tim
  Rừng, tảng tay tới đúng đối thủ, cầu tụ – ném – nổ. CHƯA xem trong game: appear, die, evolve, hộp chi tiết tướng; sợi gió còn hơi thô.

## 6. Việc tiếp

1. Người dùng chơi thử trong Unity: ải 10 đảo Mộc, hộp chi tiết tướng, tiến hóa; chỉnh theo lời họ.
2. Soi trong game các clip appear, die, evolve; VFX phụ (bụi lúc rơi, lúc ráp) nếu người dùng muốn thêm.
3. Tuỳ chọn: gạc cây đung đưa riêng; bàn tay nắm chặt hơn; sợi gió mảnh hơn.
4. Chưa commit (người dùng chưa bảo).
