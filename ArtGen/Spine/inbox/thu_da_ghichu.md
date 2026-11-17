# Cóc tê giác pha lê (`thu_da`): tướng 3 đảo Thổ (ải 10)

Bắt đầu 2026-11-17 (máy ổ C, kho `D:\Ripper\SwordxStaff`), một trong năm agent người dùng cho chạy song song ("chia multiagent làm cùng lúc
đi"; ghi chú chung `inbox/tho5_ghichu.md`). Con gốc của rig: `monster_3525` (thú đá xám bốn chân, hàm trắng to, gai dáng lửa; game tham khảo).
Xương, lưới, chuyển động gốc là của nhà phát hành game đó (như aola): dùng nội bộ, không đăng công khai. Hình là của mình. Suất 3 đảo Thổ =
ải 10, id game hiện là `cao_da` (chưa bàn thay). Mã làm việc `thu_da`. Tên, số dạng: chưa đặt.

Concept người dùng chọn: hướng D (`thu_da_1/tai_ve/L1_duyet.png`): cóc tê giác da đất nung, sừng đá kem trên mõm, hàm kem năm răng tù, ba
cụm pha lê hổ phách trên lưng, hai mảng nâu sẫm, chân mập vuốt kem. Animation theo đề xuất đã duyệt (`tho5_anim.py` mục thu_da).

## 1. Mổ rig gốc (`<SXS>/scan/monster_3525/`: `info.json`, `att_goc.json`, `att_idle0.json`, `sample_goc.json` 14 clip 30 khung/giây, `khung/`)

50 xương, 36 slot, 14 clip; **8 IK** cho bốn chân (mẫu khung `l` của runtime đã nướng IK vào biến đổi riêng: rig của mình FK). Cây:
`root → bone → bone2 → bone39 → bone3` (ngực) `→ bone13` (cổ) `→ bone12` (ĐẦU) `→ bone23` (vùng hàm, ngực dưới) `→ bone40` (HÀM DƯỚI `mt1`);
`bone39 → bone14` (lưng, hông). Chân: trước gần `bone4 → 5 → 6 → 7` (`lhand3/1/2`), trước xa `bone8 → 9 → 10 → 11` (`rhand2/1/3`), sau gần
`bone15 → 16 → 17 → 18` (`lleg1/2`), sau xa `bone19 → 20 → 21 → 22` (`rleg1/2`). Gai: `beijiao4` (bone28), `hair1` (bone27), `jiao3` (bone26)
con của đầu; `beijiao3` (bone32), `beijiao1` (bone29), `jiao1` (bone31), `jiao2` (bone30), `beijiao2` (bone33) con của lưng. Mắt `eyes2..5`
(bone34/35/38), mắt nhắm `eyes1` (bật ở hit, block, die). Slot `xz` (bone2): ảnh QUẢ CẦU MỜ chỉ bật ở skill_03 (0,3 → 0,9 s) trong khi `bone2`
quay −1080° (ba vòng) cho cả thân xoay dưới quả cầu.

Clip của họ: `idle_01` 7,67 s (nhịp thở 1,333 s lặp ba lần rồi một lần ngẩng đầu ở ~4,5 s); `run_01` 0,73; `skill_01_1` 1,07 (chồm, nhấc
chân gần, giáng cằm ~0,47); `skill_02_1` 1,2 (há hàm 0,4 → 0,9); `skill_03` 1,87 (co mình 0,2, cuộn cầu xoay 0,3 → 0,9, bung trên không 1,0,
đáp 1,24); `die_01` 1,0 (gục sấp, nhắm mắt); `hit_01` 0,5.

## 2. Mảnh (`thu_da_manh.py`; gói `gui_gpt/thu_da_1/luot_2_T1..T5.txt`)

- **Căn concept** lên hình con gốc (`can`): co 0,88 quanh tâm khung, dời (27, 15) px, đáy chân trùng đáy chân con gốc; IoU hình bóng 0,81.
  Mọi mảnh cắt ở px concept rồi qua phép căn mới vào thế giới rig (`tf().c2w`).
- **T1 thân liền** (Codex lượt đầu, 66 s): thân + đầu + hàm + bụng một ảnh, không mắt, sừng, chân, pha lê. Chia theo CỤM MÀU khép kín bởi
  nét mực (`chia_than`): đầu → `head1`; hàm + 4 răng → `mt1`; lưng + mảng nâu → `1chest` / `hip1` (theo vùng part gốc gần nhất, chồng mép
  26 px, mép cắt của mảnh vẽ sau mờ dần); bụng → `chest3` / `chest1` / `body1`. Nét mực chỗ đầu giáp lưng thuộc đầu; lưng lấn 22 px vào dưới
  đầu (màu điểm lưng gần nhất, tránh mép ngoài 12 px) để đầu gật không hở. Chia theo hình part gốc (cách đầu) cắt đôi hàm, răng rơi vào đầu:
  bỏ.
- **Mắt** cắt thẳng từ concept (`eyes2`: tròng vàng + con ngươi + vành mực, không lấy nét mày); **mắt nhắm** `eyes1` vẽ bằng mã trên khuôn mắt
  (mí trên dày + nét mí khép).
- **T2 ba chân** (Codex lượt đầu): chia khúc theo DẢI DỌC (`chia_chan`: ranh giới hai khúc kề = giữa đoạn chồng dọc của hai part gốc, tính theo tỉ lệ
  chiều cao chân gốc rồi áp lên chân của mình; chia theo hình part gốc cắt sai bàn chân vì concept lệch chỗ). Chân xa sau `rleg1/2` = ảnh chân
  gần sau tối 14 %, DỜI tới chỗ chân xa của họ (+tâm part gốc), chỉ ló dưới bụng khi bước.
- **T3, T4 bảy pha lê + sừng** (Codex lượt đầu): A2 → `beijiao4`, A1 → `hair1`, A3 → `jiao3` (con của đầu); B1 → `beijiao3`, B2 → `jiao1`, C1 →
  `beijiao1`, C2 → `jiao2` (con của lưng); `beijiao2` bỏ. Sừng mũi `sung`: mảnh thêm cứng trên `bone12`, vẽ ngay sau `head1`.
- **T5** (Codex lượt đầu): QUẢ CẦU cuộn tròn (lưng đất nung, ba cụm pha lê chĩa ra, sừng ló bên phải) → slot `xz` trên xương `bong`; LÒNG MIỆNG +
  lưỡi → slot `shetou`.
- Ghép lại mọi mảnh theo thứ tự vẽ (`thu_da_manh.py ghep` → `manh/_ghep.png`): **IoU hình bóng với concept 0,981**.



## 3. Rig (`thu_da_rig.py` → `inbox/thu_da_1/rig/`, không theo git)

54 xương (đủ xương của họ + `move`, `day`, `tam`, `bong`, `mieng`), 29 slot, 2019 đỉnh, 2780 tam giác, 8 clip, 9201 khoá, 17 sự kiện; `.atomik`
240 KB (đạt, đích 0,3 MB), atlas 768 × 848, ảnh 0,62 px / đơn vị, chiều cao 725. Mọi clip nối về khung 0 idle lệch 0 px; appear khung đầu trống,
die khung cuối trống; `.atomik` nạp lại khớp bộ vẽ Python (khung 0 lệch 0,07 px). Trang `rig/xem.html` chạy đủ 8 clip (`mo_xe/thu_xem.py`).

- **Gắn mảnh**: mỗi slot là lưới phủ hình, đỉnh biến dạng như điểm tương ứng trên lưới cùng slot của họ (`trong_so_goc`, điểm ngoài lưới kéo
  theo cạnh gần nhất). **Nhóm cùng bề mặt dùng CHUNG một trường trọng số theo vị trí** (`truong_chung`: pha các lưới của họ theo khoảng cách
  tới từng mảnh, σ 18 đơn vị): đầu + lưng + hông; ba mảnh bụng; từng chân. Hai mảnh chồng nhau ở cùng điểm biến dạng y hệt → một đường viền,
  không khe (áp góp ý tatu của người dùng). Hàm `mt1` đứng riêng để há; bụng sát hàm pha về hàm (100 % ở mép, tắt dần trong 50 đơn vị) cho
  mép dưới hàm không lộ vạch đôi. Lòng miệng: nửa trên bám đầu, nửa dưới bám hàm, giữa pha dần → giãn theo độ há, không lộ nền. Mắt nhắm bám
  đúng lưới mắt mở (`eyes1` của họ bám 100 % `bone34`, `eyes2` nửa `bone34` nửa `bone38`: bám theo của họ thì lệch ở hit).
- **Đã soi** (cận ~1,1 px / đơn vị, cận ×2 ở hàm, cổ, chân): idle 0 / 1,0, attack 0,5 (giáng), cast 0,3 / 0,8 (há to nhất), hit 0,2, die, skill,
  appear, walk. Lỗi đã sửa: khe sáng chỗ đầu nối lưng khi đầu gật (lưng lấn dưới đầu + trường chung), mẩu lưng thò trên đầu, vạch đôi mép
  dưới hàm, khấc khoé miệng, khe góc sau miệng khi há, mắt nhắm lệch, xương nhảy 124° lúc đổi quả cầu ↔ thân, pha lê rơi kéo cả `move` (slot
  bám move: phải lái xương gai), góc pha lê quấn ±180° (quay vọt 360° giữa hai khung).
- **Đo** (`thu_da_rig.py kiem`): còn các bước xoay lớn CỦA HỌ (attack 0,47 s cú giáng: chân xa 62–68°, bàn chân xa dời 0,53 chiều cao / khung;
  appear 0,9–1,13 và skill 1,73: đoạn bung ra trên không của skill_03; hit 0,03; cast 0,5 chân gần 46°); đoạn đổi quả cầu ↔ thân nhảy khi thân
  đang ẩn (không thấy). Idle: xoay lớn nhất 0,52° / khung (đầu lúc khịt), gia tốc nhỏ.

| clip | dài | nguồn | diễn |
|---|---|---|---|
| appear | 1,75 | tự dựng + skill_03 1,0 → 1,87 | quả cầu hiện dần, LĂN vào từ phía sau (−0,85 chiều cao, lăn không trượt), nảy một lần, bung ra trên không, đáp, há miệng gầm, đứng |
| idle | 4,0 lặp | idle_01 khung 0 + sóng | thở 1,8 % chu kỳ 2 s (đáy thân), ngực / lưng ngược pha, đầu trễ 0,1 s ±1°, hàm hé, túi họng trễ 0,22 s, bảy pha lê lắc ±1,4° trễ 0,15–0,36 s; vòng hai: túi họng phồng to hơn, KHỊT MŨI (đầu ngẩng 3°, chớp mắt) |
| walk | 0,73 lặp | run_01 | |
| attack | 1,15 | skill_01_1 | chồm nửa thân trước, nhích tới 0,2 chiều cao, GIÁNG sừng / cằm xuống đất (bẹp 10 %, nheo mắt), lùi về |
| cast | 1,50 | skill_02_1 kéo dài | há hàm êm, đầu ngửa, giữ rung hai dáng (tụ), PHUN: đầu giật tới, thân lùi, rồi khép hàm |
| skill | 2,50 | skill_03 + tự dựng | co mình, đổi QUẢ CẦU (bật 1,12), xoay tại chỗ nhanh dần 2 vòng (nhún), LAO vồng tới đối thủ (0,95 chiều cao, game nắn quãng), NỆN (bẹp 16 %), nảy vồng về chỗ, chạm đất, bung ra đáp đất, gầm |
| hit | 0,5 | hit_01 | mắt nhắm như họ |
| die | 1,72 | die_01 đầu + tự dựng | giật, nhắm mắt, LẬT NGỬA (172°), bảy pha lê bật khỏi lưng rơi xuống đất nảy một lần, bốn chân đạp tắt dần, mờ 0,4 s |

## 4. Sự kiện và VFX dự kiến (rig không vẽ VFX; game: hitTimes attack 0,50 / cast 0,92 / skill 1,20; muzzle (369, 394); lunge: skill; stay: cast)

| clip | giây | sự kiện | VFX dự kiến (hệ Thổ: đá góc cạnh, bụi tròn nâu nhạt → be, sỏi, dăm pha lê hổ phách) |
|---|---|---|---|
| appear | 0,70 | cham_dat | quả cầu chạm đất cuối đường lăn: vòng bụi thấp, vài viên sỏi lăn (bụi theo vệt lăn suốt 0 → 0,70) |
| appear | 0,86 | bung | bung ra khỏi dạng cầu: phụt bụi tròn, dăm đất văng |
| appear | 1,10 | cham_dat | thân đáp: vòng bụi |
| idle | 3,05 | khit | hai phụt bụi nhỏ ở lỗ mũi, bay ra trước rồi tan |
| attack | 0,50 | trung | khung giáng: chớp sao gai kem, vết nứt ngắn trên đất trước mặt, đá văng 6–10 mảnh, vòng bụi; trúng đối thủ: dăm đá, bật lùi (khựng 0,08, rung 0,5) |
| cast | 0,12 | tu | 0,12 → 0,86: bụi + đá vụn xoáy hút vào miệng (`mieng`), một tảng đá lớn dần trong miệng |
| cast | 0,92 | phun | tảng đá rời miệng bay vòng cung tới đối thủ, đuôi bụi; vỡ tung trên người nó: đá vụn, dăm pha lê, bụi (cảm giác trúng theo lúc đạn chạm) |
| skill | 0,32 | cuon | phụt bụi lúc cuộn |
| skill | 0,36 | xoay | 0,36 → 0,86: quả cầu xoay tại chỗ, sỏi + bụi tóe ra SAU (ngược hướng lao), đất dưới chân rung |
| skill | 0,86 | lao | bật đi: nổ bụi sau lưng, vệt bụi theo đường lao |
| skill | 1,20 | trung | NỆN đối thủ: chớp màn kem, vòng sóng đất, pha lê vỡ toé vòng (dăm hổ phách), đá rơi nảy một lần, bụi tan dài (khựng 0,18, rung 1,0) |
| skill | 1,64 | cham_dat | quả cầu nảy về chạm đất: vòng bụi |
| skill | 1,70 | bung | bung ra: phụt bụi |
| skill | 1,96 | cham_dat | thân đáp: vòng bụi nhỏ |
| die | 0,36 | lat | bắt đầu lật |
| die | 0,42 | rung_pl | pha lê bật khỏi lưng: dăm hổ phách nhỏ |
| die | 0,78 | cham_dat | lưng chạm đất: vòng bụi |

Chưa có bộ hạt Thổ riêng: dùng lại phần đá, bụi của `HatDa`, `HatKhoang` khi vào game.

## 5. Việc tiếp / câu hỏi mở

1. Người dùng xem `rig/xem.html` (Claude chính làm bản xem trước có đối thủ + VFX cho cả năm con).
2. Hỏi: thay suất `cao_da` (ải 10)? tên, số dạng (đang một dạng)? Lật ngửa lúc chết (đề xuất đã duyệt) hay gục sấp như con gốc?
3. Quả cầu to cỡ 1,15 chiều cao thân (theo cỡ quả cầu của họ × 0,92): thu nhỏ nếu thấy to.
4. Vào game: VFX theo bảng mục 4, heroes.json, menu Unity.
