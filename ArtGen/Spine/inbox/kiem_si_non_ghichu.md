# Voọc Tướng dạng 1: voọc non (`kiem_si_non`), tướng thứ 8 đảo Mộc (`tho_hoang`)

Bắt đầu 2026-11-13 ở máy ổ D (người dùng: "quét tướng thứ 8 đảo mộc và làm dạng 1 cho nó"). Dạng lớn là `kiem_si_1` (ghi chú
`kiem_si_ghichu.md`), trong game đang là dòng 1 dạng. Làm theo skill pokiclash-spine-rig mục "DẠNG KHÁC trên CÙNG rig gốc", như rồng vây non
và Điểu Nhi.

## 1. Quét

Máy D chưa có bản quét `monster_3620` → quét lại vào `<SXS>/scan/monster_3620/` (`SXS = D:/RefAnimation/SwordxStaff`), mỗi lệnh qua
`quai/khoa.py chrome`: `info` → `info.json`; `att` → `att_goc.json`; `att ... "anim=idle_01&t=0"` → `att_idle0.json`; `sample` cả 17 clip,
30 khung/giây → `sample_goc.json`. `kiem_si_rig.py` dựng lại ra JSON trùng bản trong game (`Resources/tho_hoang_1`), atlas chỉ lệch nhỏ do nén
bảng màu. (`<scan>/mo/`, `parts/` không quét lại: chỉ để xem.)

## 2. Tỉ lệ (`kiem_si_non.py`, file riêng: không sửa `kiem_si*.py` của máy kia)

Nạp `kiem_si_rig.dung()` của dạng lớn (mọi mảnh đã gắn ở dáng gốc dạng lớn) rồi nhân tỉ lệ ở xương gốc của cụm SAU khi gắn (`TI`):
- `bone3` × 0,80: cả nửa thân trên quanh hông. Hai tay cùng nắm MỘT thanh kiếm (vỏ là con của bàn tay gần, chuôi là con của vỏ): co riêng từng tay
  hay riêng kiếm thì tay xa trượt khỏi chuôi.
- `bone6` × 1,40 (mũ + đầu, so với thân đã co → đầu ≈ 1,12 lần dạng lớn); `Rh`, `Lq` × 0,85 (bàn chân, giáp ống); lá mào × 0,55; đuôi × 0,85.
- Hạ hông `bone2` 0,14 độ cao hông (đùi là lưới giãn → chân ngắn lại). Chiều cao game 339 (dạng lớn 363).
- Soi bằng da cũ: `rig/soi_skill.png`, `soi_cast.png`, `soi_attack.png`: kiếm vẫn trong tay, không hở ở cỡ thường.
- `kiem_si_non.py bo_cuc` → `mau/bo_cuc.png` (+ `so_ti_le.png` so dạng lớn); `kiem_si_non.py vung` in khung từng mảnh trên bố cục (px).

## 3. Concept lượt 1 (2026-11-13; `build_kiem_si_non.py` → `gui_gpt/kiem_si_non/luot_1_concept_<hướng>.txt`)

Ảnh mẫu: bố cục dạng non + concept dạng lớn. Mảnh giáp, kiếm, áo tơi, chân GIỮ HÌNH (sau đổi màu bằng mã như Điểu Nhi); chỉ đầu, mặt, mũ, mào vẽ mới.
Hai hướng (đề xuất của Claude), cả hai ra đúng bố cục ngay lượt đầu (tờ chồng nét: `mau/_so_concept.png`):
- `cam` **A · voọc con lông cam** (voọc con ngoài đời sinh ra lông cam, lớn mới sẫm): bờm kem, mắt nâu to tròn, mũ bát lục non + hai mầm lá
  chữ V, giáp lục non, kiếm gỗ trong ống tre xanh, chuôi quấn dây kem → `tai_ve/L1_cam.png`.
- `xam` **B · voọc con lông xám tro nhạt**: bờm trắng, mắt hổ phách, nón lá (kasa) thay mũ giáp + một lá non, giáp lục rêu nhạt, kiếm thật vỏ nâu
  → `tai_ve/L1_xam.png` (nón rộng hơn vùng mũ cũ ~40 px về bên phải).

Người dùng không chọn A/B mà đổi hướng (mục 4).

## 4. Concept lượt 2: khỉ voọc con KHÔNG GIÁP (2026-11-13)

Người dùng: "làm dạng 1 chibi cute kiểu con khỉ không giáp cầm kiếm cũ cùn hoặc cành cây thôi, khi có concept phải mở tôi xem".
- Bố cục mới `kiem_si_non.py bo_cuc_tran` → `mau/bo_cuc_tran.png`: ẩn `AN_TRAN` (hai tấm vai, bốn tua, giáp ngực, mũ, hai lá mào, áo tơi `kp_ao`,
  vỏ kiếm dài `k_A_1`, cả kiếm ngắn `k_B_1..3`); lưỡi kiếm dài `k_A_4` (xương `bone51`, nằm sẵn dọc vỏ, mặc định đang bật) lộ ra: một vũ khí trần
  hai tay cùng nắm. Đầu × 1,55 (không mũ thì đầu phải to hơn; mặc định `KS_NON_DAU` nay 1,55; lượt 1 dùng 1,40). Bao tay, giáp ống chân còn
  trên bố cục làm chỗ cho cẳng tay, ống chân lông (prompt dặn vẽ lông).
- Prompt `gui_gpt/kiem_si_non/luot_2_concept_<hướng>.txt` (cùng `build_kiem_si_non.py`), lông cam như hướng A, đai dây leo + váy lá:
  - `kiem_cun`: kiếm sắt cũ mẻ, gỉ, mũi gãy tròn, chuôi + đoạn lưỡi sát kiếm cách quấn vải sờn (tay gần nắm ở đó vì kiếm cùn), kiếm cách gỗ nứt;
    khăn trán xanh hai đuôi bay → `tai_ve/L2_kiem_cun.png`.
  - `canh_cay`: cành cây cong, chuôi quấn dây leo, ngọn chẻ có lá non; một chiếc lá trên đầu → `tai_ve/L2_canh_cay.png`.
- Cả hai ra dùng được ngay lượt đầu (~100 s mỗi ảnh): IoU hình bóng với bố cục 0,73; đuôi, chân, tay, đường vũ khí trùng; đầu + bờm nhỏ hơn bố cục
  một chút (tờ chồng viền `mau/_so_concept2.png`). Trang xem `inbox/kiem_si_non_xem_concept.html` (đã mở cho người dùng).
- Ghi chú cho bước rig: không vỏ thì lúc chiêu mana "rút kiếm" cả vũ khí trượt dọc trục khỏi tay gần (tay gần buông) là đúng ý; khăn trán hai đuôi
  dùng được hai chuỗi xương lá mào (`x_la_to_*`, `x_la_nho_*`, có lò xo); chiêu cuối của dạng lớn rút hai kiếm: dạng 1 chỉ có một vũ khí (tay xa
  trống) hoặc cần thêm món thứ hai.

## 5. Lượt 3: chọn kiếm cũ cùn, lông xám, kiếm TRONG VỎ GỖ (2026-11-13)

- Người dùng chọn `L2_kiem_cun`: "con này nhưng đổi màu lông sang gần giống dạng 1 nhưng nhạt hơn" (hiểu là gần lông than của DẠNG LỚN, nhạt hơn).
  Đổi bằng mã cho giữ y nét (`kiem_si_non_long.py` → `L2_kiem_cun_6f6a63.png`, bản nhạt hơn `_8e8982`). Bẫy: da mặt / tay / chân đo s ≈ 0,48,
  lông s ≈ 0,82; ngưỡng bão hoà đầu tiên 0,32 làm xám luôn mặt, tay, chân → ngưỡng 0,62–0,72.
- Rồi: "kiếm cùn ở trong, bao kiếm ở ngoài bằng gỗ, xem kĩ lại nhé". Bố cục `kiem_si_non.py bo_cuc_bao` (`AN_BAO` = `AN_TRAN` trừ vỏ `k_A_1`; vẽ
  CÙNG hệ toạ độ với `bo_cuc_tran` để khớp ảnh đã chọn). Prompt `luot_3_concept_bao_go.txt`: ảnh 1 bố cục có vỏ, ảnh 2 con đã chọn (lông xám), ảnh 3
  dạng lớn chỉ để xem cách cầm (tay gần nắm vỏ sát miệng, kiếm cách ở miệng vỏ, tay xa nắm chuôi) → `tai_ve/L3_bao_go.png` (96 s, đạt lượt đầu):
  vỏ gỗ trơn có thớ, vết nứt buộc vải sờn, kiếm cách gỗ nứt, chuôi quấn vải sờn; không lộ lưỡi; lông, mặt, khăn, váy lá giữ y.
- Soi: vỏ + kiếm cách + chuôi thẳng một đường, vỏ chui sau cẳng tay gần. Chồng viền bố cục (`mau/_so_concept3.png`, IoU 0,66): đường vỏ concept thấp
  và thoải hơn rig ~50 px ở mũi, cả con nhỏ hơn và lệch trái nhẹ (như lượt 2). Không sao: vỏ / lưỡi / chuôi gen thành thanh nằm ngang rồi đặt theo trục
  kiếm của rig (như dạng lớn), thân gen theo khung part. Mũi vỏ trông như đầu que nứt: lúc gen tờ kiếm dặn mũi vỏ tròn kín.
- Trang xem `inbox/kiem_si_non_xem_concept.html` (đã mở cho người dùng).

## 6. Duyệt L3_bao_go → mảnh, rig, đủ clip, tiến hóa (2026-11-13; người dùng: "duyệt, làm hết 1 lượt đi", "làm cả các animation còn lại giống với dạng 2 ý")

**Mảnh** (`kiem_si_non_manh.py`, ra `inbox/kiem_si_non/manh/` + `dat.json` dạng 1):
- `doi_mau`: chép mảnh dạng lớn; 13 mảnh LÔNG (kp_gu, kp_lung, kp_bung, hai khuỷu, hai bắp tay, kp_than, kp_co, than = hông, đuôi, hai đùi) trung vị
  ~(101, 78, 67) → xám concept (119, 110, 102); 10 mảnh DA (tám part bàn tay, hai bàn chân) → (253, 173, 129). Nhân theo kênh, điểm mực (tối) và
  kem (sáng: chỏm đuôi) giữ nguyên.
- Gen ba tờ (`luot_4_manh_<tờ>.txt`, ~90 s mỗi tờ, đạt ngay lượt đầu): mỗi ô = hình bóng mảnh cũ cùng khung (rig đặt đúng chỗ).
  `N1`: đầu chibi có khăn trán (khung đầu cũ nới lên 110 px; ô có đầu cũ mờ làm mốc mắt / mõm / bờm), hai đuôi khăn (thay hai lá mào: chuỗi xương
  `x_la_to_*`, `x_la_nho_*` có lò xo; gốc ở nút sau đầu, bay ra sau), đai dây leo; `N2`: hai cẳng tay lông, hai ống chân lông (thay bao tay, giáp
  ống: giữ hình bóng nên hai khớp không đổi), váy lá (khung cao sẵn bằng váy đã kéo dài tới `VAY_TREN` nên rig không giãn dọc); `S`: vỏ gỗ, lưỡi cùn,
  chuôi quấn vải + kiếm cách gỗ tròn. IoU: cẳng tay 0,98, ống chân 0,96, váy 0,97, đầu 0,86, đai 0,85, vỏ 0,87, chuôi 0,74 (kiếm cách đổi
  dáng, tua vải thả), lưỡi 0,59.
- **Bẫy kiếm**: rig đặt ảnh kiếm theo trục = đường giữa bề cao ảnh; GPT vẽ lưỡi lệch trục 25 px và dày gần bằng vỏ (85 / 90 px) → lưỡi trong vỏ
  ló ra mép dưới. `can_kiem` (chạy cuối `cat`): dời dọc cho trục về giữa (vỏ, lưỡi, chuôi), ép lưỡi về dày 62 px. Khung kiếm chỉ nới TRÊN DƯỚI
  ĐỀU (nới ngang thì đổi độ dài trục).
- Khung nới: `dat.json` dạng 1 dời gốc affine theo phần nới (`noi`); cẳng tay nới khung thì `kiem_si_non.dung_rig` đổi toạ độ hai khớp `HAI`.

**Rig** (`kiem_si_non.py rig` → `inbox/kiem_si_non/rig/`): `KM.MANH` trỏ mảnh dạng 1, `dung_non` (tỉ lệ mục 2/4, đầu × 1,55, đuôi khăn × 0,85),
chiều cao game = đỉnh sọ trên ảnh đầu (bỏ chỏm tóc) = 241 (dạng lớn 363, có mũ). Bỏ hẳn slot `BO_SLOT` (hai tấm vai, bốn tua, giáp ngực, mũ, áo
tơi, cả kiếm ngắn) TRƯỚC khi dựng clip, để ảnh ảo ảnh chiêu cuối chụp đúng hình khỉ con. Tám clip là clip của dạng 2 (`kiem_si_clip.lam_clip`)
chạy nguyên trên rig dạng 1: appear, idle (có trò bật chuôi), walk, attack (quật cả vỏ), cast (giữ thế, rút lưỡi cùn chém, tra kiếm), skill (rút
kiếm, biến mất, bốn ảo ảnh khỉ con lục, hiện lại, tra kiếm; tay xa trống vì một kiếm), hit, die. Thêm `evolve` 3,0 s: gộp bản NHẸ dạng lớn
(`PXU_NHE` 0,26, bỏ ảo ảnh), khỉ con nhún rung (mặc định của `tienhoa`), dạng lớn hiện ra chạy idle chậm, vươn, ngẩng rồi về đúng khung 0 idle
(lệch 0,00 px; dạng lớn co 0,663 trong rig gộp). 136 xương, 98 slot, 9 clip, `.atomik` 474 KB (dưới trần 0,5 MB).
- Soi: tờ khung Python `rig/khung_<clip>.png`; runtime Spine thật `rig/that/*.jpg` (cả 9 clip) và cận thân `rig/that_can/*.jpg` (idle, attack,
  cast, hit, skill): vai (không còn tấm vai che), hông, cẳng tay nối bàn tay liền; tay ôm đúng vỏ / chuôi; không hở.
- Trang xem `rig/xem.html` (tự chứa, nút từng clip; đã mở cho người dùng).
- Dạng lớn xuất lại là dạng 2 / 2 (`kiem_si_non.py lon2` → `inbox/kiem_si_non/rig_lon/kiem_si_1.atomik`, 501 KB) cho lúc vào game.

## 7. Người dùng trả bản rig đầu (2026-11-13): "chiêu cuối lỗi", "đánh thường lỗi lộ đuôi, chân không nối đúng khớp"

1. **Khối lông bay trên đầu ở chiêu cuối**: ở con gốc `bone31` (nửa cánh trái = áo tơi lá của dạng lớn) và `bone32` (nửa cánh phải = mảng lưng lông
   `kp_lung`) BẬT LÊN như cánh lúc rút hai kiếm / xoay người; dạng lớn có mũ, tấm vai, áo tơi che. Đuôi bám `bone31`. Sửa ở nguồn
   (`kiem_si_non.lam_clip_non`): bỏ hai xương đó khỏi dữ liệu chuyển động của họ (cả clip lẫn ảnh ảo ảnh), bỏ gió trên `bone31`.
2. **Lộ đuôi khi quật kiếm**: (a) cả lưng xoay nên đuôi thõng thành vòng → bù cho gốc đuôi 85 % phần xoay thế giới của `bone31` (đuôi giữ dựng; chết
   thì không bù); (b) gốc đuôi của dạng lớn nằm NGOÀI mép lưng (x = −74, mép `kp_lung` −58; dạng lớn nấp trong áo tơi) → dời cả đuôi (ảnh + chuỗi
   khớp, cùng một phép, `kiem_si_non_manh.DUOI_DOI` dx 110, dy −30 px concept, nghiêng 10°): gốc vào sau mảng lưng (x = −39).
3. **Khớp chân**: ống chân lông (khối viền kín) đè lên đùi → vạch viền ở đầu gối. Theo luật "các khúc NỐI NHAU gen LIỀN rồi cắt": `kiem_si_non.py chan_to`
   (hình bóng đùi + ống chân ở dáng gốc dạng 1, mỗi chân một hình) → gen `luot_5_chan_lien.txt` → `chan_cat` (đùi, ống chân lấy điểm ảnh của tờ qua
   lưới từng mảnh, theo từng tam giác). Bẫy: (a) tờ vẽ 7,4 px / đơn vị (gấp 3 lần mảnh khác) → viền mỏng 1/3 → làm đậm mực 6 px mỗi phía trước khi lấy
   mẫu; (b) hình bóng của mảnh phải lấy từ NGUỒN CỐ ĐỊNH (đùi: ảnh dạng lớn; ống chân: bản sao `manh/_truoc_chan/`), không từ ảnh đang có (lần thử
   cắt đầu đùi đã ghi đè, hoàn tác không lấy lại được).
4. **Mẩu lông thô cạnh hông ở chiêu cuối** (cũng có trong ảnh người dùng chụp): KHÔNG phải mép ảnh mà là lưới đùi GẬP (đùi bám cứng hông ở 30 %
   trên; thế cúi sâu của họ đưa hông xuống gần đầu gối; dạng lớn cũng gập 34 khung, áo tơi che). Thử cắt đầu hông đùi → clip đi lộ mép cắt: bỏ.
   Sửa (`gan_lai_dui`): gắn lại trọng số đùi ở dáng gốc, chuyển mềm suốt chiều dài, đầu đùi chỉ theo hông 0,65 → đếm trên mọi khung: không gập ở
   appear, idle, walk, attack, cast, skill, hit (chỉ còn ở die, lúc đổ ngửa và mờ dần).
5. Bẫy Codex: gọi `gen.py` ở chế độ chạy thường thì `codex exec` chờ stdin, treo tới hết timeout và giữ khoá Codex chung (phiên `moc_vuong` chờ). Luôn
   chạy nền hoặc `< /dev/null`.
- Soi runtime Spine thật sau sửa: `rig/that_v3/*.jpg` (8 clip), cận hông chiêu cuối `rig/that_hong3/skill.jpg`. `.atomik` 466 KB.

**Chưa làm**: vào game (`tho_hoang` 1 dạng → 2 dạng: heroes.json forms, `Resources/tho_hoang_1` = dạng 1 này, `tho_hoang_2` = dạng lớn, chân dung,
ải có `evo`, golden) — chờ người dùng; tên dạng 1 chưa đặt. VFX vệt chém (như dạng lớn) chưa có.

## 8. Vào game (2026-11-13, máy ổ C; người dùng: "ok xuất ra rồi cho vào game")

- Rig dạng 1 dựng lại trên máy C bằng `kiem_si_non.py rig` (thư mục `rig/` không theo git; dữ liệu quét `D:\Ripper\SwordxStaff\scan\monster_3620`
  có sẵn trên máy C). `.atomik` 466 KB, khớp số ở mục 7.
- `quai/doi_kiem_si_non.py` (chạy lại không đổi thêm, `--kiem`): suất `tho_hoang` từ 1 thành 2 dạng: **Voọc Non** (`tho_hoang_1`, 0,92, rig
  `kiem_si_non/rig`, có `evolve`) và **Voọc Tướng** (`tho_hoang_2`, 1,1, `kiem_si_non/rig_lon/kiem_si_1.atomik` = dạng lớn xuất là dạng 2/2:
  xương, lưới, clip y hệt bản cũ, chỉ số trúng đòn mạnh hơn). Tên "Voọc Non" Claude đặt tạm. `stages.json` ải 260 thêm `"evo": true`.
- Unity (MCP cổng 8080): Nhập dữ liệu; "Gắn dạng .atomik vào prefab tướng" → `tho_hoang: prefab giữ 2 dạng`; tính lại golden: `roster.json`
  (n = 2), `islands.json` (ải 260 evo, hpPct), `sim.json` (1 ô ải 260, ghép bằng `golden_thuy.py ghep_sim`).
- **Chưa xong:** Unity trên máy C không thêm `HatGiac.cs`, `HatRong.cs` (pull về lúc Editor đang mở) vào danh sách biên dịch → lỗi CS0103 ở
  `HatNuoc.cs`; cần khởi động lại Editor rồi chạy lại EditMode test (lần chạy trên bản biên dịch cũ: 101/103, hai test hỏng không do đổi này).
  Chưa xem trong trận, chưa có VFX vệt chém cho dạng 1.
