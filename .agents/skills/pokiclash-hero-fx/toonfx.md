# Học từ Epic Toon FX (đọc 2026-11-10)

Bộ Asset Store của Archanor VFX, nằm ở `Assets/Epic Toon FX/` (557 MB, 1302 prefab 3D, 24 prefab 2D). Thư mục đã ghi vào `.gitignore`:
**chỉ để đọc cách làm**. Không commit, không tham chiếu từ prefab hay code của game, không chép ảnh của họ vào `Assets/03 Art`.
Material gốc là Built-in. Muốn xem chạy thì nhập gói `Upgrade/Epic Toon FX URP.unitypackage` (đè material trong thư mục đó).
Scripts demo của họ biên dịch chung Assembly-CSharp; nếu gây lỗi test hay build thì xoá thư mục `Demo/Scripts`.

Công cụ (thư mục `tools/` của skill này):
- `ps_dump.py "<gốc>" ra.jsonl`: đọc mọi prefab ra JSONL (khoảng 25 s cho cả bộ);
- `ps_show.py ra.jsonl <tên prefab>...`: in công thức từng emitter;
- `ps_stats.py ra.jsonl`: phân vị số theo loại lớp.

Cả ba dùng được cho bản đục Clash of Critters (`D:\Ripper\ClashOfCritters\AssetRipper_Export\ExportedProject\Assets`).

## 1. Số chung

- Mỗi hiệu ứng trung vị **3 emitter**, 90% có từ 5 emitter trở xuống. Không cần nhiều lớp: mỗi lớp một vai rõ ràng.
- Module dùng nhiều nhất: cỡ theo tuổi (4058), màu theo tuổi (3967), **cản (Limit Velocity dampen, 3067)**, xoay theo tuổi (1684),
  chạy khung (970). Noise chỉ 163, sub-emitter 218: phần lớn sức sống đến từ **đường cong cỡ, màu và cản**, không phải vật lý phức tạp.
- 57% lớp là cộng sáng (glow). Mình đổi theo bảng ở mục 2 của `SKILL.md`: quầng thành vòng phẳng hoặc bỏ, lõi trắng thành hình kem.
- Ảnh hạt toàn **trắng xám, nhuộm bằng màu theo tuổi**. Đúng cách `fire.py` làm: một ảnh xám, nhiều màu.
- Đơn vị: nhân vật demo cao khoảng 2 đơn vị, nên **1 đơn vị ETFX ≈ 0,5 H** (ước lượng). Tốc 18 đơn vị/s ≈ 9 H/s.
- **Cản dampen d** là phần vận tốc bị cắt mỗi bước, khoảng mỗi 1/30 s (ước lượng, chưa đo). Đổi sang cản mũ: `k ≈ −30·ln(1−d)`.
  d = 0,09 ≈ 2,8/s; 0,15 ≈ 4,9/s; 0,2 ≈ 6,7/s; 0,25 ≈ 8,6/s. Hạt **bắn rất nhanh rồi khựng lại**: đây là cảm giác "toon".

## 2. Phân vị theo loại lớp (nhóm Combat, không lặp; p25/p50/p75)

| Lớp | Đời (s) | Tốc (đv/s) | Cỡ (đv) | Trọng lực | Cản d | Số bắn | Dáng cỡ theo tuổi | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| tia văng, mảnh, giọt | 0,30/0,40/0,53 | 12/18/25 | 0,05/0,07/0,12 | 0/0,6/1 | 0,2 | 12/15/25 | co (228/244) | 79% kéo dài theo vận tốc; alpha giữ tới 83% đời |
| gai (spike) | 0,20/0,25/0,30 | 2/6/13 | 0,15/0,19/0,30 | 0 | 0,15–0,25 | 8/12/15 | co | 99% kéo dài, ảnh tam giác cong `triangle_curve`, `wave3` |
| vòng sóng | 0,25/0,30/0,35 | 0 | 1,5/2,2/4 | 0 | 0,09 | 1–2 | nở 0,3–0,5 → 1 | alpha giảm đều 1 → 0 |
| quầng (glow) | 0,25/0,30/0,40 | 0 | 2,75/4/5 | 0 | 0,09 | 1 | co 1 → 0,3–0,7 | cộng sáng; mình không dùng |
| khói, mây, bụi | 0,55/0,70/0,85 | 6/11/12 | 0,7/1,1/1,5 | −0,3/−0,1/0 (bay lên) | 0,2 | 6/12/21 | **co** (192/232) | 69% dùng tờ 2x2 chọn khung ngẫu nhiên; alpha giữ tới 90% |
| lõi lửa, nổ | 0,25/0,30/0,38 | 0/3/18 | 0,6/1,2/1,3 | 0 | 0,15 | 1/6/9 | nở hoặc co | 53% chạy tờ khung ăn mòn |

- **Mọi lớp của một cú trúng bắn cùng lúc ở 0 s** (trễ trung vị 0). Các lớp tách nhau bằng **đời và tốc**, không bằng giờ bắt đầu:
  gai 0,25 s, vòng 0,3 s, tia 0,4 s, khói 0,7 s. Clash of Critters thì trễ lớp phụ 0,15 s. Cả hai đều dùng được: trễ cho cú nặng
  có "dư âm", không trễ cho cú nhanh.
- **Alpha gần như không dùng để tan**: giữ đậm tới 80–90% đời, hạt biến mất bằng **co cỡ về 0** hoặc **tờ khung ăn mòn**.

## 3. Tờ khung ăn mòn: cách "tan" của hoạt hình phẳng

Các tờ `explosion_round_3x3`, `fire2_6x3`, `splat02_flat_3x3`, `nova_6x3`, `lightning_v2_3x3` có cùng một kiểu:

- hình phẳng trắng (tròn, lưỡi lửa, vệt toé, vòng, sét);
- mỗi khung bị **một hình tròn lệch tâm cắn dần từ một phía**: tròn đặc → tròn thủng → lưỡi liềm → cung mảnh → hết;
- đường "frame over time" thường giữ khung 0 tới 15–30% đời rồi mới chạy (`fot c[0.18:0 → 1:1]`): **hình đứng nguyên một nhịp rồi mới tan**.

Áp vào game mình: `fire.erode_frames(seed, n)` sinh ruột xám và viền mực đã giãn theo đúng hình bị cắn. Bản thử là khói phun lửa
(`ERODE=1 py -3 -I phun_lua_thu.py <ra>`, GIF `ArtGen/Spine/chuan_fx/phun_lua_an_mon.gif`). Hai điều đã soi:
- dừng ở **lưỡi liềm còn dày** (khung 3/5), rồi co về 0 trong 15% cuối. Cung mảnh hơn chỉ còn viền mực, trông như nét gạch;
- hạt nhỏ (dưới khoảng 6 đơn vị sân) bị cắn cũng chỉ còn viền: cho hạt nhỏ co thay vì cắn.

## 4. Công thức mẫu (đã đọc, đổi sang luật vẽ tay)

**Phun lửa Toony** (`FlamethrowerToonyFire`, lặp, 5 emitter):
- **lõi lửa:** tờ ăn mòn 3x3, đời 0,33 s, tốc 34, cỡ 0,9–1,2, cỡ 0 → 1 tới 89% đời, màu vàng → cam, khung chạy từ 18% đời;
- **khói đi cùng luồng:** tờ mây 2x2, đời 0,5–1,1 s, tốc 22–32, trọng lực −0,6 (bay lên), cỡ 0 → 0,84 ở 40% → 0. Màu cam → đỏ (33%)
  → xám (72%): **chính hạt lửa nguội thành khói**, xoay chậm dần;
- **than:** vệt kéo dài, đời 0,4–1,2 s, trọng lực −0,5, màu trắng → vàng → đỏ, cản 0,15;
- **chớp ở miệng:** chấm kéo dài 4 lần, đời 0,25 s, cỡ 0,27 → 0,83 → 0;
- **quầng:** bỏ.

→ Bản chuẩn mốc của mình cũng làm như vậy: lõi xếp lớp co theo tuổi, khói từ hạt chết. Lấy thêm: khói **bay cùng luồng** từ đầu
(màu đổi theo tuổi), không chỉ sinh khi hạt lửa chết.

**Đấm hoạt hình** (`ToonFightAction`, 3 emitter, cả cú chỉ 0,2 s):
- **vệt "grab":** lưỡi liềm sáng 1 cái, đời 0,15–0,2 s, cỡ 0,42 → 1, alpha 0 → 1 ở 15% → 0;
- **tia hút vào:** 10 tia bắn ở **0,05 s**, xuất phát trên mặt cầu bán kính 0,73 với **tốc âm (−6 đến −9)**, tức là bay vào tâm; đời 0,1–0,15 s;
- **gai đấm:** 5 tam giác kéo dài, tốc −2, cỡ 0 → 1.

→ Đòn đánh thường của mình: cú trúng 0,15–0,25 s, tia **hút vào** tâm thay vì bung ra. Đọc là "lực dồn vào điểm chạm".

**Trúng tròn** (`RoundHitRed`): 8 lưỡi cong `wave3` kéo dài, đời 0,15–0,25 s, cỡ 0,73 → 1, màu trắng → cam. Thêm 12 gai mảnh đời
0,3–0,45 s, tốc 6–9, **giữ cỡ tới 47% đời rồi co**, cản 0,2, màu trắng → đỏ.

**Chí mạng kiếm** (`SwordHitRedCritical`, 5 emitter):
- 25 tia `line_sharp` kéo dài 16 lần, gần như đứng yên, cỡ nở rồi co, đời 0,3 s;
- 12 gai cong tốc 10–13, cản 0,3;
- 15 tia nhỏ trọng lực 0,5;
- 2 vòng nở 0,47 → 1, màu trắng → cam → đỏ.

**Chém kiếm** (`SwordSlashThick`):
- mảnh cung (mesh) **quay nhanh rồi chậm dần**: tốc quay 19 rad/s giảm về 0;
- đời 0,3 s, cỡ 0,88 → 1. **Lớp tối phía dưới** (màu đỏ nâu, alpha) sống 0,15 s, lớp sáng phía trên 0,3 s;
- 15 hạt trên cung 202°.

→ Vệt chém của mình là cung có viền mực, quay 0,15–0,3 s; lớp mực dưới tắt trước, lớp màu tan sau.

**Nổ cầu lửa mềm** (`ExplosionFireballSoftFire`):
- lõi cỡ 0,22 → 1 trong 0,3 s;
- 18 tia: tốc 8–16, trọng lực −0,2 (bay lên), noise (cường độ 1, tần số 0,5), màu vàng nhạt → cam → đỏ, giữ đậm tới 88% đời;
- 6 khói: đời 0,6–1 s, cỡ 0,45 → 1, trọng lực −0,5, màu cam → nâu sẫm, xoay chậm dần, chọn khung ngẫu nhiên.

**Vòng lửa nova** (`NovaFireRed`, 7 emitter):
- 17 lưỡi lửa ăn mòn;
- 65 tia bắn trên vòng tròn bán kính 2;
- 12 khói bung ngang (tốc 22–24) và 12 khói bay lên (trọng lực −0,8), màu cam → nâu đỏ → xám;
- 1 vòng nở 0,32 → 1, đời 0,45 s.

**Chữ tượng thanh** (`KaPow`):
- chữ cỡ 0,25 (ở 12% đời) → 1 (51%) → 0,92, alpha vào trong 11% đời, giữ tới 82%, nghiêng dần 0,6 rad, đời 0,35 s;
- 35 gai tốc 8–14, 25 sọc.

→ Chữ "BÙM" của mình có thể nở theo đường cong này.

**Tụ lực** (`MagicChargeYellow`, lặp):
- 90 vệt/s xuất phát trên mặt cầu bán kính 2,2 với **tốc −9** (bay vào tâm), đời 0,2–0,4 s, alpha vào ở 53% đời;
- 70 chấm/s tốc −6, cỡ 0 → 1 ở 16% → 0.

**Buff** (`MagicBuffYellow`):
- 5 vệt dài phóng lên (kéo dài 3 lần), tốc 9–15, cỡ 0,27 → 0,94 → 0;
- 25 chấm.

**Hồi máu** (`HealOnceBurst`): 6 dấu cộng (tờ 9x1 chạy 4 vòng), cỡ nảy (1 → 0,69 → 0,93 → 0,73 → 0,84), bay lên chậm.
8 chấm nhỏ xoay nhanh chậm dần.

**Lên cấp** (`LevelupNovaYellow`):
- 125 chấm trên vòng tròn, cỡ **nhấp nháy** (0 → 1 → 0,28 → 0,91 → 0);
- tia xoay quỹ đạo (orbital 2) với nhịp sinh giảm dần;
- vòng nở 0,32 → 1 trong 1 s.

**Choáng** (`StunnedCirclingStars`): 3 sao/s chạy vòng (vận tốc z theo đường cong −1 → 1 → −1), cỡ 0,3 → 1 ở 26% đời, xoay chậm dần.

**Sét đánh** (`LightningStrikeSharpBlue`):
- tia dọc tờ 3x3 kéo dài 8 lần, đời 0,1–0,25 s;
- 4 tia ngắn ở chỗ đánh;
- 16 tia văng trọng lực 2;
- 1 vòng 0,15 s.

**Chết thành hồn lửa** (`SoulFireDeath`):
- hồn bay lên có noise và vệt đuôi;
- 8 + 23 mây sẫm bung ra (màu cam → trắng ở 28% đời), co về 0;
- lưỡi lửa ăn mòn, trọng lực −1,5;
- 12 giọt văng;
- quầng bắn 2 lần (0 s và 0,12 s).

**Khói trắng** (`SmokeBurstWhite`): 16 mây/s nón 7°, đời 0,6 s, cỡ 0 → 1 ở 51% → 0, alpha vào ở 10% giữ tới 68%, xoay chậm dần.

**Sao bung 2D** (`StarBurst2D`, bộ 2D):
- 8 sao tốc 4–16, trọng lực 0,7, giữ cỡ 0,8 → 1 tới 77% đời rồi co về 0, **xoay nhanh dần** (0,12 → 1 × 12,6 rad/s);
- 43 tia nhỏ.

## 5. Thủ pháp rút ra (áp cho mọi hiệu ứng)

1. **Bắn nhanh, cản mạnh** (d 0,15–0,25): hạt bung ra rồi khựng lại tại chỗ, không trôi lơ lửng.
2. **Màu theo tuổi = nhiệt độ:** trắng/kem → vàng → cam → đỏ → nâu, xám. Mọi tia, lửa, khói đều đi một chiều nguội dần.
3. **Cỡ theo tuổi:**
   - lõi, vòng, khói lúc nở: 0,2–0,45 → 1;
   - tia, gai: giữ rồi co về 0 (giữ tới 40–50% đời);
   - khói hoạt hình: 0 → đỉnh ở 40–50% → 0.
4. **Tan bằng co hoặc ăn mòn,** alpha chỉ cắt ở 10–20% cuối đời.
5. **Xoay ngẫu nhiên lúc sinh, tốc quay giảm dần theo tuổi** (đường cong 1 → 0): khói, mây, sao, chém đều vậy. Sao bung thì ngược lại, quay nhanh dần.
6. **Tốc âm từ mặt cầu** (hút vào tâm) cho tụ lực và cú đấm. Tốc dương từ tâm cho nổ.
7. **Tờ mây 2x2 chọn khung ngẫu nhiên** (frame over time = hằng ngẫu nhiên 0..1): mỗi hạt một dáng mà chỉ một ảnh.
8. **Lớp tối dưới lớp sáng:** chém có lớp tối sống ngắn hơn. Mình dùng lớp mực dưới, như bản chuẩn mốc.
9. **Khói đi cùng luồng:** một emitter khói bay cùng hướng với lửa, màu từ cam sang xám. Không có cảm giác hai hiệu ứng rời nhau.
10. **Ít emitter, mỗi lớp một vai:** chớp (0,15–0,25 s), gai, vòng (0,3 s), tia (0,4 s), khói (0,7 s).
