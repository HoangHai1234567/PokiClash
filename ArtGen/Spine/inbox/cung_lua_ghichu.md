# Quỷ lửa bắn cung (`cung_lua`): tướng thứ 3 đảo Hỏa

Bắt đầu 2026-11-13 (máy ổ C). Con gốc của rig: `monster_3357` (hiệp sĩ cung thủ mũ trụ chùm lông lửa, game tham khảo, kho
`D:\Ripper\SwordxStaff`), **do người dùng chỉ**. Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không
đăng công khai. Tên, id game: chưa đặt (`cung_lua` chỉ là mã làm việc).

## 1. Lời dặn của người dùng (2026-11-13)

- "làm tướng thứ 3 đảo hỏa; concept tôi muốn làm là **quỷ lửa bắn cung** (con gốc là hiệp sĩ lửa)".
- "**idle/walk** có thể làm giống con gốc". appear: "tướng **nhảy vào sàn đấu**".
- Đánh thường: "**bắn 1 mũi tên** vào kẻ địch".
- Chiêu cast: "**bắn 3 mũi tên cùng lúc** (giống `skill_02` nhưng **dáng không phải ngửa lên trời**)".
- Chiêu cuối: "**bắn liên tục 3 mũi tên thường** sau đó **nhảy lên không kéo 1 mũi tên năng lượng lửa phát sáng**, **hold** 1 chút để tụ lửa
  rồi bắn, **impact mạnh, shake cam**".
- die: "**rụng cung, quỵ gối nằm xuống**".

## 2. Lịch sử trong ngày (các hướng đã bỏ; file của chúng đã xoá theo lời người dùng)

1. Ba lượt concept tự dựng (lượt 1 nhiều chi tiết → "không đẹp, ít chi tiết thôi"; lượt 2 tối giản; lượt 3 theo ảnh gợi ý cung thủ giáp cháy người
   dùng đưa → chọn bản mũ nhỏ, sửa nhiều vòng về cung, dây, mỏ mũ, gạc, đầu tên → duyệt "L6").
2. Rig dựng trên L6 (mảnh theo hình bóng trơn của part + mảnh tự do) → người dùng gửi lại ảnh con gốc: "làm animation dựa trên con này, cho tôi
   concept mới". (L6 lệch dáng con gốc: mũ nhỏ, lửa bung, cung và tên đặt chỗ khác.)
3. Concept bám con gốc (lượt 7): chọn **A** (mũ to ba khe dọc sáng, một ngọn lửa đúng dáng chùm lông, hai sừng nhỏ, giáp cháy đen, hai vết nứt
   lửa); cung GPT vẽ lỗi → gen hai cách đặt cung; "ok cứ làm tiếp đi". Bản A (cung như con gốc) giữ ở `cung_lua_1/mau/concept_A.png` làm mẫu màu, nét.
4. Rig thứ hai (mảnh theo khung part nhưng tờ hướng dẫn chỉ là HÌNH BÓNG TRƠN, mũ gộp, cung dùng lại của L6 và dời xương dây) → "**xấu quá, tôi nghĩ
   bạn nên xóa hết đi làm lại từ đầu, xem con gốc tách như nào thì mình tách và gen như thế**".

Bài học: hình bóng trơn làm GPT tô mảnh thành cục, mất cấu trúc (khe mặt nạ, đai giáp, vây cung); muốn "y hệt con gốc" thì đưa GPT chính các mảnh
gốc và chỉ đổi da (skill `pokiclash-spine-rig` mục 23).

## 3. Mổ rig gốc (`<SXS>/scan/monster_3357/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample.json`, `mo/`, `parts/`, `khung/`)

56 xương, 32 slot, 10 clip; 31 hình trên 24 vùng ảnh. Con nhìn sang PHẢI. `zuo*` = bên GẦN (trái hình), `you*` = bên XA.

| thứ tự | slot | ảnh (px) | là gì | xương |
|---|---|---|---|---|
| 1 | `jiandai` | 112 × 125 | ống tên sau lưng (ba đuôi tên ló miệng ống) | bone34 |
| 2–4 | `youdabi`, `youxiaobi`, `youjianjia` | | bắp tay, cẳng tay, tấm vai XA | bone21, 22, 29 |
| 5 | `gongjian_02` | 187 × 130 | DÂY CUNG (lưới 14 đỉnh, ba xương bone31 / 32 / 33) | |
| 6 | `gongjian_01` | 233 × 176 | CUNG: hai nhánh cong nối ở tay cầm, mỗi nhánh một vây | xương `gongjian_01` |
| 7 | `tofa` | 174 × 184 | CHÙM LÔNG mũ (lưới 28 đỉnh, chuỗi bone4..8) → ngọn lửa | |
| 8–9 | `youshou_01/02` | | bàn tay XA hai lớp | bone36, bone24 |
| 10 | `to_01` | 109 × 119 | vòm sau mũ (lưới 6 đỉnh, bone3b 0,98) → thêm hai sừng | |
| 11–15 | `youdatui`, `youjiao`, `pigu`, `zuodatui`, `zuojiao` | | đùi, ủng hai chân, hông | |
| 16–17 | `yao`, `xiong` | | váy giáp (28 đỉnh), giáp ngực (13 đỉnh) | |
| 18 | `zuodabi` | | bắp tay GẦN | bone19 |
| 19 | `jian` (+ `jian3..6` bản sao ẩn) | 142 × 59 | MŨI TÊN ngắn đầu to | bone27; 37, 38, 39, 47 |
| 21 | `to_02` | 130 × 107 | MẶT NẠ mũ (ba khe + một khe hẹp, viền) | bone3b |
| 25 | `zuojianjia` | | tấm vai GẦN | bone28 |
| 26, 28 | `zuoshou_01/02` (+ `_03/_04`) | | bàn tay GẦN hai lớp | bone25, 26 |
| 30 | `zuoxiaobi` (+ `zuoxiaobi2`) | 66 × 65 | bao tay GẦN to có vết nứt | bone20 |

Họ ĐỔI THỨ TỰ VẼ lúc giương cung (khung 3 của `skill_01`): dây, cung, hai lớp bàn tay xa, mũi tên ra trước thân.

**Bẫy công cụ:** atlas có vùng `rotate: 90/270`; `to_manh.nap` đã quay ảnh về chiều gốc nên khung tứ giác của hình region dùng `bounds` w × h nguyên
(đã sửa trong `cung_lua.py luoi()`; `mat_lua.py`, `quy_lava.py` chép cùng mã cũ).

Clip của họ: `idle_01` 6,67 s; `run_01` 0,67 s; `skill_01` 1,0 s (rút tên, giương, buông 0,40); `skill_02` 1,5 s (ba tên chĩa lên trời); `hit_01/02`,
`block_01`, `stun_01`, `floating_01`; `die_01`.

## 4. Reskin (cách đang làm, 2026-11-13)

- `cung_lua_da.py to`: hai tờ MẢNH GỐC cắt theo lưới, phóng 2,5–5 lần (`mau/goc_A.png`: chùm lông, mặt nạ mũ, vòm sau mũ + hai sừng vẽ thêm bằng
  mã trong khung nới lên 0,62 bề cao, cung, mũi tên, ống tên; `mau/goc_B.png`: 13 mảnh thân tay chân + 4 mảnh bàn tay) + prompt
  `gui_gpt/cung_lua_1/luot_1_da_A.txt`, `luot_1_da_B.txt`: ảnh 1 tờ mảnh gốc, ảnh 2 concept A (màu, chất liệu, nét), ảnh 3 Voọc Tướng (nét). GPT giữ
  hình bóng, chỗ, cỡ, đường cấu trúc; đổi da: giáp cháy nâu đen, mảng sẫm, lửa ba màu phẳng, khe mũ vàng sáng; bỏ lam xám, viền vàng, chữ S.
- `cung_lua_da.py cat`: cắt theo ô → `manh/<vùng>.png` cỡ ảnh vùng × 2, giữ trong hình bóng gốc nới 3 px; dây cung đổi màu bằng mã.
- `cung_lua_rig.py`: mỗi hình của họ một hình của mình, NGUYÊN lưới (đỉnh, tam giác, uv, trọng số; điểm gắn theo ma trận dáng gốc trong
  `att_goc.json`); dáng gốc của rig mình = khung 0 idle của họ; thứ tự vẽ của họ + năm slot `_t` cho lúc giương cung. Thử bằng DA GỐC
  (`CL_MANH`, `CL_RA`): clip bắn ra y hệt con gốc.

## 5. Kết quả reskin (2026-11-13)

- Tờ da: `tai_ve/D_A.png` (94 s), `D_B.png`, đều đạt lượt đầu. Độ khớp hình bóng với mảnh gốc: 0,91–0,98 (thấp nhất `jian` 0,91, `zuoshou_02` 0,91).
  Tờ so: `manh/_so_A.png`, `_so_B.png`. Mảnh: `manh/<vùng>.png` (24 vùng, cỡ ảnh vùng × 2).
- Rig: 69 xương, 44 slot (31 của họ + 5 bản `_t` + 2 mũi tên xoè + mũi tên nặng + cung rơi + 4 mũi tên bay), 284 đỉnh; chiều cao game 322;
  `.atomik` 195 KB. Mọi clip nối về idle lệch 0 px. Góc nhảy lớn nhất giữa hai khung 91° (cú bật tay của `skill_01` của họ).
- Clip: `idle`, `walk`, `hit` = nguyên của họ; `attack` = `skill_01` + mũi tên bay (buông 0,40, trúng 0,56); `cast` 1,65 s (ngắm ngang, giữ dây,
  ba mũi xoè ±9°, buông 1,0); `skill` 3,05 s (ba phát 0,30 / 0,56 / 0,82, bật lên 0,62 chiều cao, giữ tụ lửa 1,36–2,05, bắn, rơi, đáp 2,48);
  `appear` 1,35 s (nhảy vào, đáp 0,46); `die` 1,75 s (rụng cung 0,22, quỵ gối, đổ sấp 1,12, mờ dần).
- **Mũi tên lửa năng lượng của chiêu cuối** (người dùng 2026-11-13: "mũi tên cuối trong chiêu cuối nên là 1 mũi tên lửa năng lực rực cháy, khác với
  mũi tên thường"): mảnh rời, con gốc không có. `cung_lua_da.py ten_lua` → `gui_gpt/cung_lua_1/luot_2_ten_lua.txt` (ảnh mẫu: tờ `D_A.png` lấy nét và cách
  vẽ lửa) → `tai_ve/T_LUA.png` (đạt lượt đầu: cả mũi tên bằng lửa, lõi vàng nhạt, đầu tên lưỡi lửa, lửa quấn thân kéo ra sau, đuôi ba lưỡi lửa; tô phẳng,
  không quầng sáng) → `cung_lua_da.py ten_lua_cat` → `manh/ten_lua.png` + `ten_lua.json` (chỗ đuôi tì dây, mũi; trục lấy theo mũi thật vì GPT vẽ lệch
  trục 14 px). Rig: xương `nang` (con của xương mũi tên đang kéo bone38, gốc ở đuôi tên tì dây), slot `ten_nang`, dài 1,45 lần mũi tên thường; trong
  `skill` nhen lên từ 0,45 lúc bật nhảy, lớn dần khi kéo dây, bập bùng 9 Hz mạnh dần lúc giữ, phình thêm 16 % trong 0,14 s trước khi buông; mũi tên
  bay thứ tư (`bay_3`) dùng cùng hình. `.atomik` 222 KB. Quầng sáng, vệt lửa, nổ trúng vẫn là việc của lớp VFX.
- **Lửa của mũi tên cháy liên tục** (người dùng: "mũi tên lửa bạn cũng nên làm animation cho riêng nó, lửa cháy liên tục"): bỏ ô cứng + xương `nang`;
  mũi tên lửa là MỘT lưới 22 × 8 (slot `ten_nang`, vẫn ở chỗ mũi tên đang kéo trong thứ tự vẽ) trên `ten_3` (con của `fly_3`): cùng một hình cho lúc
  trên dây (clip đặt `ten_3` theo đuôi tên tì dây và hướng mũi tên của bone38 sau khi thân đã vào dáng) và lúc bay (game lái `fly_3`). Xương lửa con của
  `ten_3`: `l_t0..4` / `l_d0..4` (năm cặp lưỡi lửa trên / dưới thân, gốc ở thân tên), `l_duoi` (đuôi lửa), `l_dau` (đầu tên). Trọng số: lõi thân
  (|y| nhỏ) cứng theo `ten_3`, ra xa thân thì theo xương lưỡi lửa gần nhất (nội suy dọc thân). `lua_chay()`: mỗi lưỡi phập phồng dài ngắn ±22 %, lay ±8°,
  trượt về sau, sóng chạy từ mũi về đuôi (4,5 Hz + hài 1,7 lần), hai phía lệch pha; đuôi quẫy ±7°; mạnh dần lúc tụ lửa (0,7 → 1,3), lúc bay 1,3.
  Lúc buông, góc mũi tên xoay dần từ hướng trên dây sang hướng bay trong 30 % quãng đầu; đuôi tên dừng trước đích 0,6 thân tên (mũi xuyên tâm đối thủ).
  81 xương, 43 slot, 452 đỉnh; `.atomik` 233 KB. Soi runtime thật 1,5–2,2 s: `rig/that/skill.jpg`.
- So với con gốc cùng khung (runtime Spine thật): `rig/so_sanh_goc.jpg` (idle, walk, attack, hit: dáng trùng từng khung).
- Xem: `rig/xem.html`; tờ khung `rig/that/*.jpg`.

## 6. Vào game (2026-11-13, người dùng: "việc tên bay là do code làm, ghép vào trong game đi rồi gen tiếp dạng 1")

- **Suất**: tướng thứ 3 đảo Hỏa = id `kim_su` (giữ id, chỉ số, thẻ, số mảnh, 3 dạng). `Assets/02 Data/Json/heroes.json` khối `kim_su`:
  `name` "Hỏa Cung", `title` "Quỷ lửa bắn cung", `line` "Dòng Hỏa Cung", `aola` `cung_lua_2`; từ 15:15 là HAI dạng: "Hỏa Cung Nhi" `cung_lua_1` 0,92 và "Hỏa Cung" `cung_lua_2` 1,1 (trước đó tạm ba dạng cùng `cung_lua_2`). `cards.json`: chỉ đổi TÊN ba thẻ (`kim_su_skill` "Tam Tiễn", `kim_su_ult` "Hỏa Tiễn Phá Không",
  `kim_su_pas` "Mắt Lửa"), hiệu ứng thẻ giữ nguyên. **Tên là Claude tạm đặt, chờ người dùng chốt.** `Resources/kim_su_1..3` cũ để yên (không dùng).
- **Rig**: `Assets/03 Art/Heroes/Resources/cung_lua_2/` (`cung_lua_2.atomik`, `_portrait.png`). `game.json`: stay / far / farAim = attack, cast,
  skill; `hitTimes` 0,5787 / 1,1787 / 2,2453; chiêu cuối khựng 0,22, rung 1,0, bật lùi 0,18, chớp `#ffb04066`.
- **Tên bay do game lái**: xương `far` + `fly_0..3` (`AolaActor.FarAtomik`), `farAim` xoay mũi tên theo hướng bay thật.
- **Hiệu ứng** (`StageView.FireFx["kim_su"] = ("ten", "no_lon")`): chiêu mana = `HatLua.TenNo` (ba chớp nổ nhỏ so le ở thân đối thủ lúc ba
  mũi tên tới, không thêm đạn); chiêu cuối = nổ lớn sẵn có. Chưa có vệt lửa theo tên, quầng tụ lửa (mục 7).
- **Lỗi chỉ lộ trong game, đã sửa**: (1) mảnh "ma" mờ 50 % ở khung đổi lớp cung / tên → `quai/hoat.py` xuất bật tắt trọn thành bậc;
  (2) mũi tên mờ lơ lửng trước mặt lúc game giữ dáng ở khung trúng → khung tới đích trùng khung mẫu, `trung` sau đó 0,012 s, xương bay ở
  lại đích (`GIU_DICH`, `TRE_TRUNG` trong `cung_lua_rig.py`). Ghi vào skill `pokiclash-spine-rig` (mục vật bay).
- **Đã chạy trong Unity**: Nhập dữ liệu, Gắn dạng .atomik (prefab `04 Prefabs/Heroes/kim_su.prefab`), tính lại golden islands / roster /
  cardtext / zones, EditMode 102 / 103 (hỏng `PrefabOnlyTests.MaRuntime_KhongSinhDoVat` ở `UI/Kit/NumberTicker.cs`, `UiMotion.cs`, không
  thuộc việc này). Tour thử: menu "PokiClash/Thử/Đảo Hỏa: riêng Hỏa Cung, đòn thường, chiêu mana, chiêu cuối (đang Play)"
  (`Editor/HoaFxTour.cs`), ảnh ở `Temp/PokiShots/hoa_fx`; tờ đã soi: `inbox/cung_lua_1/trong_game/*.jpg`.
- Lúc nhảy ở chiêu cuối, đỉnh đầu chui sau bảng máu đối thủ (tướng đứng bên người chơi): chưa chỉnh, chờ người dùng xem.

## 6b. Dạng 1 (non), 2026-11-13

- Cùng rig, cùng clip: `CL_DANG=non py -3 -I ArtGen/Spine/cung_lua_rig.py ...` (`TI_LE`: `bone3` × 1,17 = cả đầu + chùm lửa, `bone4` × 0,70 =
  chùm lửa; không đụng tay, chân, cung). Tên xuất `cung_lua_1`, thư mục `inbox/cung_lua_1/non/` (`mau`, `tai_ve`, `manh`, `rig`).
- Bố cục: `non/mau/bo_cuc.png` (lệnh `bo_cuc`). Concept: `py -3 -I ArtGen/Spine/cung_lua_non.py concept` →
  `gui_gpt/cung_lua_1/non_luot_1_concept.txt` → `non/tai_ve/C1.png` (sừng cụt, chùm lửa nhỏ hai màu, giáp trơn chưa nứt lửa, cung trơn).
  **Chờ người dùng duyệt.** Trang xem: `non/xem_concept.html`.
- Người dùng duyệt C1: "dạng 1 ổn, làm đi".
- **Chuyển da** (`py -3 -I ArtGen/Spine/cung_lua_non.py da`, rồi `cat`): dạng 1 chỉ khác dạng 2 ở NĂM mảnh, các mảnh còn lại dùng nguyên
  ảnh dạng 2 (không cho GPT vẽ lại cả tờ: khớp nối đã khít khỏi lệch).
  - `xiong` (ngực), `zuoxiaobi` (găng lớn), `gongjian_01` (cung): bỏ vết nứt / vân lửa BẰNG MÃ (`bo_lua`: mỗi điểm lửa lấy điểm cùng mảng
    ở cách đó một khoảng dời, giữ được vân chì sáp, không nhoè như inpaint).
  - `tofa` (chùm lửa): ba màu → hai màu bằng mã (`lua_hai_mau`: đỏ cam → cam, cam → vàng).
  - `to_01` (vòm mũ + sừng): gen lại riêng, tờ S (`gui_gpt/cung_lua_1/non_luot_2_sung.txt` → `non/tai_ve/D_S.png`), hai mẩu sừng cụt; cắt
    bằng đúng bộ cắt của dạng 2. So: `non/mau/_so_manh.png`, `non/mau/_so_sung.png`.
- **Rig**: `CL_DANG=non py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/cung_lua_rig.py` → `non/rig/cung_lua_1.atomik`
  (162 xương, 86 slot, 9 clip, 298 KB). Gộp rig dạng 2 cho tiến hóa (`quai/tienhoa.py`; dạng 2 dựng ở tiến trình riêng, lệnh `nhe`); 20 / 25
  ảnh của dạng 2 trùng dạng 1 nên dùng chung (atlas 201 KB thay vì gấp đôi).
- **Clip `evolve`** (2,8 s): ý "quỷ con bắt lửa". Dạng 1 thụp xuống gồng, run; chùm lửa nhỏ bùng to hai nhịp tới cỡ chùm lửa dạng 2
  (`bone4` × 1 / 0,70 × 1,12, giật 9 Hz); đổi dạng lúc lửa to nhất; dạng 2 ưỡn lên gầm, chùm lửa bùng quá cỡ (`n_bone4` × 1,26–1,34)
  rồi lắng. Khung cuối trùng khung 0 idle dạng 2 (lệch 0,00 px).
- **Vào game**: `Resources/cung_lua_1/`; `heroes.json` `kim_su` còn HAI dạng (0,92 / 1,1, như Nham Thần; tên dạng 1 "Hỏa Cung Nhi" tạm
  đặt). Golden: islands, roster, cardtext, zones, progression, badges, potential tính lại; `sim.json` đổi một ô (đảo Hỏa ải 10: 21 → 20
  hiệp, vì boss ải đó tiến hóa một lần thay vì hai). EditMode 102 / 103 (vẫn chỉ hỏng `PrefabOnlyTests` ở mã UI).
- **Soi**: `Library/PokiHeroShots/kim_su_atomik_1.png` (menu "Chụp thử dạng .atomik": idle, hit, attack, cast, skill, evolve qua
  `AolaActor`), chép ở `inbox/cung_lua_1/trong_game/dang_1_moi_clip.jpg`; trang xem `non/rig/xem.html`.

## 6c. Chốt vào game (2026-11-13, người dùng: "ổn rồi cho vào game")

- **Tên dạng theo quy ước `<id>_<k>`** (thay các tên tạm `cung_lua_1`, `cung_lua_2` ở mục 6 và 6b): `heroes.json` `kim_su` có hai dạng
  `kim_su_1` ("Hỏa Cung Nhi", 0,92) và `kim_su_2` ("Hỏa Cung", 1,1). Rig chép bằng `py -3 -I ArtGen/Spine/quai/vao_game.py` theo
  `quai/da_nhan.json` (dòng `kim_su`: `non/rig/cung_lua_1.atomik` → `Resources/kim_su_1/`, `rig/cung_lua_2.atomik` → `Resources/kim_su_2/`,
  giữ `.meta` cũ). Đã xoá `Resources/cung_lua_1`, `Resources/cung_lua_2` (thư mục tạm) và `Resources/kim_su_3` (dạng 3 cũ, không còn dùng).
- Xuất lại rig thì chạy lại `vao_game.py` rồi refresh Unity (không chép tay).
- Cảnh báo của `vao_game.py --kiem`: `game.shadow 'shadow' không có slot đó` (rig không mang slot bóng của con gốc; game tự vẽ bóng). Vô hại.
- Unity: Nhập dữ liệu, Gắn dạng (prefab `kim_su` trỏ `kim_su_1`, `kim_su_2`), golden tính lại, EditMode 102 / 103 (chỉ hỏng `PrefabOnlyTests`).
- **Thử trong Play** (menu mới ở `Editor/GiotSuongCombatTour.cs`):
  - "PokiClash/Thử/Đảo Hỏa: Hỏa Cung ra trận ở 2 dạng (đang Play)" → `Temp/PokiShots/hoa_cung_combat` (sao 1 và sao 5: đánh, bắn, chiêu cuối,
    địch đánh, địch bắn). Dạng 1 chạy đủ, tên bay tới đối thủ, mũi tên lửa ở chiêu cuối.
  - "PokiClash/Thử/Hỏa Cung tiến hóa: clip evolve của dạng .atomik (đang Play)" → `Temp/PokiShots/hoa_cung_tien_hoa` (2 sao → 3 sao:
    `kim_su_1` → `kim_su_2`, clip evolve chạy trong hộp chi tiết, hết clip là dạng 2 đứng nghỉ).
  - Tờ đã soi: `inbox/cung_lua_1/trong_game/dang_1_ra_tran.jpg`, `tien_hoa_trong_game.jpg` (ảnh nhỏ 223 × 397 vì cửa sổ Game đang nhỏ).
- Chưa commit (người dùng chưa bảo).

## 7. Việc tiếp

1. Người dùng xem, dặn sửa (sừng thêm vào vòm mũ là phần duy nhất không có ở con gốc: bỏ thì gen lại riêng mảnh `to_01`).
2. VFX: vệt tên lửa, tụ lửa trên mũi tên nặng, nổ trúng mạnh, bụi lúc đáp đất.
3. Người dùng chốt tên tướng, tên ba thẻ, số dạng (2 hay 3) của dòng.
