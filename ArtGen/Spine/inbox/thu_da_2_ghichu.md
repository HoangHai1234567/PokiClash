# Tê Thiềm DẠNG 2 (`thu_da_2`, tướng 3 đảo Thổ, ải 10) — rig `monster_3526`

Người dùng 2026-11-17: "làm thêm dạng 2 cho 3 con đầu", chọn rig 3526 (dạng tiến hoá của 3525 trong game gốc, có clip `evolution_01`), duyệt
concept `tai_ve/L1_duyet.png` (= L1_A): "ok concept 3 con kia ổn rồi làm đi". Agent riêng làm (song song tatu, thằn lằn).
Hình gốc Sword x Staff chỉ dùng nội bộ, không đăng công khai.

## 1. Quét

`<SXS>/scan/monster_3526/`: `info.json` (54 xương, 48 slot, 13 clip), `att_goc.json`, `att_idle0.json`, `sample_goc.json` (13 clip, 30
khung/giây), `khung/`, `khung2/` (tờ khung), `mo/idle0_0.jpg` (tờ mổ từng part). IK hai chân sau (all40, all41) và transform đã nướng vào
khung `l`. Thứ tự vẽ đổi nhẹ ở skill_01..04, block (eo, đai, gai lưng): bỏ qua.

Bố cục rig: lom khom, tay GẦN (all8→all9→all10→all11, bàn + ba ngón all12..17) chống đất bên phải; tay XA all7→all18 ôm KHỐI GAI
(`wuqi_*` trên all19 dài 480; hai gai phụ trên all45 `wuqi_010/011`, all46 `wuqi_11/012`, xoay riêng tới 78° ở skill_01, skill_03, die);
đầu all6 (to_01 đầu, to_02 gai má, jiao_01 sừng đỉnh, mắt yanjing_01/02, mày meimao), hàm xương `bone` (xiaba_01/02, lưỡi shetou trên
all22/23); cổ bozi_01 (all5), bướu bozi_02 (all36); thân shenti_01, eo yao, đai yaodai_01..03; hai chân sau all27..29 / all30..32; đuôi
all34→all35→all39→all44. Không có slot nhắm mắt, không đổi hình.

## 2. Mảnh (`thu_da2_manh.py`, ảnh `inbox/thu_da_2/manh/`)

Concept duyệt đứng bốn chân, IoU hình bóng với con gốc chỉ 0,555 → vẽ lại trên bố cục rig trước:

| Ảnh | Nguồn | Nội dung | Kết quả |
|---|---|---|---|
| `tai_ve/C0.png` | Codex | CONCEPT TRÊN RIG: con đã duyệt theo đúng dáng, chỗ, cỡ từng mảnh của 3526 (khối gai thành cụm lăng trụ hổ phách, tay gần thành chân trước vuốt kem, tay xa thành vai ôm cụm pha lê) | IoU hình bóng 0,895 (căn a 0,97, dời 9, 3 px) |
| `M_T1.png` | Magnific 95 credit | thân + cổ + đầu + hàm liền (giữ 3 pha lê mọc liền thân, đầu) | đầu / hàm |
| `M_T2.png` | Codex | chân trước gần (vai, cẳng, bàn, ba ngón vuốt, 2 pha lê), vai xa, đuôi | dùng |
| `M_T3.png`, `M_T4.png`, `M_T5.png` | Magnific 3 × 95 credit | tờ pha lê theo toạ độ + hai chân sau | GPT chọn sai pha lê theo toạ độ (vẽ thừa con cao nhất, thiếu vài con): chỉ lấy sừng kem `to_02`, pha lê đỉnh đầu `jiao_01`, hai pha lê gối, hai chân sau, bản vẽ đủ của gai phụ `wuqi_010` (T4), `wuqi_11` (T3) |
| `M_T6.png` | Magnific 95 credit | thân KHÔNG đầu, không hàm, cổ + bướu vẽ đủ chỗ đầu che | thân, cổ (khỏi vá, khỏi lộ vệt khi đầu ngửa) |

Codex: 2 ảnh (C0, T2; T3–T5 gửi Codex lúc hết hạn mức: 0 ảnh). Magnific: 5 ảnh × 95 credit = 475 credit (gen_magnific.py 1k high).

Cách cắt:
- `cat T1`: ĐẦU = vùng loang từ giữa mặt (1000, 520) chặn bởi nét mực, lấp lỗ, + viền mực 10 px + pha lê sát đầu; khuyết đáy đầu (chỗ răng)
  lấp màu da. HÀM DƯỚI = dải kem + răng nhô lên + lòng miệng ngay dưới đầu (thịt trong miệng thuộc hàm dưới). Thân, cổ: từ T6, chia
  shenti_01 / yao / bozi_01 / bozi_02 theo part gốc gần nhất (dải chồng 22 px, mảnh vẽ sau mờ dần).
- `cum`: CỤM PHA LÊ lấy thẳng từ C0: mặt pha lê = cụm điểm hổ phách tách bởi nét mực, gán cho mảnh gốc phủ nhiều nhất; ba gai phụ thành
  mảnh riêng (thêm bản vẽ đủ từ tờ), còn lại (all19 + gai lưng) thành MỘT mảnh `wuqi_01` (vẽ trước nhất của khối, y hệt C0; chỗ gai phụ là lỗ,
  gai phụ vẽ sau lấp vào). `wuqi_02..06`, `wuqi_011`, `shenti_02/03` bỏ.
- `mat`: mắt cắt từ C0 (`yanjing_02`), mắt nhắm vẽ bằng mã (`mat_nham`); `luoi`: lòng miệng tối + lưỡi hồng vẽ bằng mã (`shetou`).
- Ghép (`ghep`): IoU hình bóng với C0 0,833 (lệch ở hai chân sau: C0 đặt chân sau xa lệch trái so với rig).

## 3. Rig (`thu_da2_rig.py` → `inbox/thu_da_2/rig/thu_da_2.atomik`)

57 xương (đủ xương họ + move, day, tam, mieng), 32 slot, 1956 đỉnh, 2772 tam giác, 8 clip, 12 sự kiện; `.atomik` 323 KB (dưới trần 0,5 MB),
atlas 856 × 1032; chiều cao dáng đứng 755. Mọi clip nối về khung 0 idle lệch 0,00 px; idle khép vòng 0,92 px; không khung nào quấn 360°
(đo ở 60 khung/giây: xoay > 40° / khung chỉ có ở ngón tay, chân trong hit, die, appear, attack: có sẵn trong clip gốc).

- Thứ tự lớp: MẮT, MẮT NHẮM, HÀM DƯỚI vẽ ngay SAU đầu (họ vẽ trước đầu vì ảnh đầu của họ có lỗ mắt, hàm nấp sau đầu; đầu mình kín, răng mình
  đứng trước môi trên). Còn lại theo thứ tự của họ.
- Trọng số: nhóm cùng bề mặt (đầu + cổ + bướu + thân + eo; chân trước + bàn + ngón; từng chân sau) chung trường trọng số; cổ trước sát hàm đi
  theo hàm; đỉnh lưới thân nằm trong hình đầu / hàm đi theo hẳn đầu / hàm (khỏi lộ mép khi đầu xoay); lòng miệng nửa trên bám đầu, nửa dưới
  bám hàm, phủ hết khe miệng tới mép trước hàm.
- Ẩn: shadow, wuqi_02..06, wuqi_011, shenti_02/03, youdabi_02, meimao, yanjing_01, xiaba_02, yaodai_01..03, shouji.

## 4. Clip (giây clip; game nhận hitTimes attack 0,55 / cast 0,95 / skill 1,12; lunge: skill (attack lao mặc định); stay: cast)

| Clip | Dài | Gốc | Diễn | Sự kiện |
|---|---|---|---|---|
| appear | 2,05 | skill_03 | rơi từ trên xuống (hiện dần 0,1 s), đáp nảy, múa khối pha lê, về idle | cham_dat 0,34 |
| idle | 6,0 | idle_01 | thở; ĐẶT khối pha lê nằm ngang sau lưng rồi vác lại (1,5–3,3); chớp mắt 0,95 và 4,35; khịt mũi 5,2 | khit 5,2 |
| walk | 0,8 | run_01 | | |
| attack | 1,10 | skill_01 nén | hạ khối ngang, nhún (0,34 lao), LAO tới (0,32 cao, nảy nhẹ) ĐÂM mũi pha lê (0,55), hai gai phụ bật, giữ, rút về | lao 0,34; trung 0,55 |
| cast | 1,55 | evolution_01 | trộn từ idle sang dáng đứng ngả ra sau, khối vắt sau lưng (0–0,35), HÁ HÀM tụ + rung hai dáng (0,35–0,89), PHUN (0,95: đầu giật tới, hàm sập nửa, thân giật lùi 0,05 cao), chồm về | tu 0,30; phun 0,95 |
| skill | 2,50 | skill_04 + skill_01 | chồm giơ khối (0–0,5), GỒNG giữ trên đầu rung (0,5–0,96), NHẢY tới (rời đất 0,96, đỉnh 0,18 cao, lao 0,85 cao) BỔ khối xuống trước mặt (1,12), quá đà, nảy về (1,62), vung khối ra sau lưng (1,62–1,86), GẦM (1,86–2,20), về | gong 0,50; nhay 0,96; trung 1,12; cham_dat 1,62; gam 1,86 |
| hit | 0,5 | hit_01 | nhắm mắt 0,03–0,30 | |
| die | 1,4 | die_01 | khối văng ra sau, ngã sấp (chạm đất 0,62), nhắm mắt, mờ 1,0–1,4 | cham_dat 0,62 |

Chọn chiêu cuối BỔ KHỐI thay cuộn tròn lăn của dạng 1: rig dạng 2 có sẵn khối gai to vung được (không cần ảnh quả cầu), cú bổ từ trên đầu
xuống + nhảy tới nặng và rõ lực hơn; vẫn giữ "lao tới nện" của dạng 1. Chiêu mana giữ ý dạng 1 (há hàm tụ đá, phun tảng đá) nhưng to hơn,
dáng đứng ngả ra sau gầm. Đánh thường đổi từ giáng sừng sang đâm mũi pha lê (động tác mạnh nhất có sẵn của rig).

## 5. Vị trí để viết hiệu ứng game (đơn vị chiều cao dáng đứng; x về phía đối thủ, y lên; gốc ở chân lúc đứng)

- cast `mieng` (chỗ nhả tảng đá) t = 0,1 → 1,3 bước 0,1: (0.421, 0.478), (0.356, 0.541), (0.293, 0.583), (0.282, 0.603), (0.277, 0.600),
  (0.275, 0.605), (0.272, 0.621), (0.268, 0.627), (0.263, 0.632), (0.265, 0.609), (0.331, 0.561), (0.399, 0.521), (0.432, 0.471).
  Lúc phun (0,95) ≈ (0.264, 0.62). Game meta `muzzle` (khung nhả cast, px rig): (151.68, 426.18).
- attack: mũi khối pha lê t = 0,35 (0.515, 0.267), t = 0,55 (0.852, 0.205) (tính cả quãng lao 0,32 của rig; game nắn tới 72 % quãng).
- skill: `day` (đáy thân, theo cú nhảy của rig, quãng 0,85) t = 0,9 → 1,7 bước 0,1: (0.150, 0.045), (0.205, 0.173), (0.823, 0.114),
  (1.030, 0.045), (0.941, 0.139), (0.668, 0.203), (0.363, 0.175), (0.186, 0.070), (0.180, 0.045). Mũi khối pha lê t = 0,9 (0.148, 0.825)
  (giơ trên đầu), t = 1,12 (1.321, −0.073) (cắm đất trước mặt: ≈ 0,3–0,47 cao trước thân ở đỉnh nhảy), t = 1,3 (1.259, 0.052).
  Trong game cú nhảy được nắn tới 72 % quãng tới đối thủ ⇒ cú bổ rơi đúng chân / thân đối thủ.
- appear: chạm đất 0,34 tại `day` (0.180, 0.092) (ngay chỗ đứng).

## 6. Bản xem trước chiêu (`tho5_fx_thu_da2.py`, không sửa `tho5_fx.py`)

`inbox/tho5_fx/thu_da2_attack.gif`, `thu_da2_cast.gif`, `thu_da2_skill.gif` (+ `_soi.png`):
- attack: bụi đạp lúc lao, chạm: chớp, dăm hổ phách + đá, 3 mảnh pha lê văng, vòng bụi.
- cast: bụi + sỏi + mảnh pha lê nhỏ xoáy hút vào `mieng` (0,30 → 0,91), phun tảng đá to r 21 (mạch hổ phách) bay vồng 0,40 s, nổ (cham_no 1,6),
  vòng bụi, rung.
- skill: bụi rỉ dưới chân + dăm hổ phách rơi khỏi khối lúc gồng; bụi bật lúc nhảy; BỔ: nổ (cham_no 2,0), vòng bụi lớn, chớp màn, rung, VÒNG 7
  CỘT LĂNG TRỤ PHA LÊ trồi quanh chân đối thủ (phần sau lưng nó vẽ lớp sau); đáp về: vòng bụi; gầm: bụi rung.

## 6b. Sửa theo Claude chính (2026-11-17, người dùng giao tự quyết; GIỮ cả ba hướng: bổ khối, đâm mũi pha lê, idle đặt khối)

- Lỗ trên cụm khi gai phụ xoay: gai phụ (all45, all46) xoay còn 45 % góc gốc; chỗ gai phụ che cụm NẰM TRONG hình bóng cụm có lớp lấp riêng
  (slot `wuqi_02`, vẽ trước gai phụ) — ở bản này chỉ 33 px nên bỏ (gai phụ gần như nằm ngoài cụm); lọc mẩu nét mực rời khỏi mảnh pha lê.
- Hai chân sau nắn về đúng chân rig: chân xa dời 42 px, chân gần 9 px (px C0, đo ở tâm bàn chân; đáy đã trùng), pha lê gối theo chân
  (`thu_da2_manh.py nan`, hộp gốc giữ ở `hop0`).
- Mảnh dính thân ở mọi clip: mảnh một xương của họ nhưng thuộc nhóm cùng bề mặt (vai, cẳng, bàn, ngón chân trước; đùi, cẳng chân sau) nay
  dùng lưới dày + trường trọng số chung (trước gắn cứng từng xương: dải chồng ở khuỷu văng ra thành vệt mờ khi tay giơ ở đòn đánh). ĐẦU tách
  khỏi nhóm (sọ cứng theo xương đầu: hết nhòe má khi ngửa 70° ở chiêu cuối); thân, cổ nằm dưới đầu đi theo đầu. Đuôi, đai lưng (liền trên
  eo), pha lê gối, gai phụ soi ở attack, appear, die, skill, cast, walk, hit, idle: dính thân, không khe, không lộ mép cắt gốc đuôi.
- Đoạn vung khối ra sau ở chiêu cuối kéo thành 0,24 s đều (trước 0,16 s có khung xoay 69–76° / 1/60 s); chiêu cuối dài 2,50 s.

## 7. Lỗi còn lại

- Vài nét rất mờ dưới mép hàm phải khi hàm há trong đòn đánh (phần thân lấn dưới hàm, ở cỡ hiển thị trong game gần như không thấy).
- Đuôi T2 ngắn hơn đuôi gốc (phần bị che trong C0 GPT không vẽ dài ra).

## 8. Đã chốt

Claude chính (người dùng giao tự quyết) GIỮ: chiêu cuối nhảy tới bổ khối pha lê, đánh thường đâm mũi pha lê, idle đặt khối nằm ngang sau lưng.
