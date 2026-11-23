# Học hiệu ứng (VFX) của Kingdom Rush 5: nổ, lửa, nước, khói

Rút từ bản APK 4.00.54 ngày 2026-11-18. Bản rút đầy đủ nằm ở `D:\Ripper\KingdomRush5` trên máy ổ C.

- **Xem trực quan:** chạy `MO_WEB.bat` trong thư mục này. Trang mở ở http://localhost:8767/fx_viewer/index.html; tab **Đáng học** đi theo đúng thứ tự tài liệu này.
- **Tờ khung đánh số** của từng hiệu ứng: `to_khung\<hệ>__<tên>.jpg`.
- **Số liệu:** `to_khung\so_lieu.json`.

Dữ liệu trang xem và tờ khung không commit; cách sinh lại ở `README.md`.

Hình và code là của Ironhide. Chỉ học cách làm, không chép hình.

## 1. Năm điều quan trọng nhất

1. **Hiệu ứng chính là chuỗi khung vẽ tay, vẽ phẳng 3–5 màu.** Không có shader ánh sáng, không blend cộng trong trận: mọi thứ vẽ bằng alpha thường. Vụ nổ, lửa, nước toé đều là cel-shading phẳng (vùng màu đều, mép cứng); chỉ khói bụi, hơi thở rồng và chấm sáng nhỏ là có mép mềm.
2. **Vẽ "giữ 2 khung":** 30 khung/giây nhưng 1.077/1.590 hoạt ảnh có khung lặp lại, tỉ lệ trung vị 2,0. Thực chất là 15 hình/giây. Tiết kiệm nửa số hình mà chuyển động vẫn "giòn".
3. **Đỉnh tới ngay khung 1–3, tan chiếm nửa sau.** Nổ dài 0,6–0,9 s: chớp 1 khung, bung đầy ở khung 2–4, phần còn lại là khói tách cụm bay lên và mờ dần. Nước toé to nhất ngay khung 1.
4. **Một đòn là chuỗi template nối nhau, mỗi mảnh một việc:** đạn → hạt đuôi → hiệu ứng trúng → decal trên đất → vùng hiệu ứng (payload) → hiệu ứng bám lên địch (mod). Mỗi mảnh là một hoạt ảnh ngắn, ghép lại thành chiêu lớn.
5. **Hệ hạt chỉ "dập" hoạt ảnh vẽ sẵn:** 100/113 hệ hạt dùng hạt có hoạt ảnh, đời hạt đúng bằng độ dài hoạt ảnh (tỉ lệ trung vị 1,0), alpha giữ 255 (95/113), phần lớn không có vận tốc. Hạt sinh ra rồi đứng yên tại chỗ, tự tan theo các khung đã vẽ. Đuôi khói, đuôi lửa của đạn làm hết bằng cách này.

## 2. Ba cách làm hiệu ứng trong game

| Cách | Dùng cho | Số lượng | Ghi chú |
|---|---|---|---|
| Chuỗi khung (`prefix_0001…`) | gần như mọi hiệu ứng trận: nổ, trúng, lửa, nước, khói, đạn | 1.590 hoạt ảnh hiệu ứng | khai báo `{prefix, from, to}` trong `data/animations/*.lua`; mỗi khung là một sprite trong atlas, đã cắt sát và có `trim` |
| Hệ hạt (`particle_system`) | đuôi đạn, khói bốc từ máy, bọt nước, bào tử bay khắp màn | 113 hệ | phát hạt theo nhịp, hạt chạy một hoạt ảnh rồi mất |
| Exoskeleton (xuất từ Adobe Animate) | cảnh lớn, nổ của boss, lửa trại và khói trên map, hiệu ứng màn chơi | khoảng 520 hoạt ảnh | mỗi khung ghi transform (x, y, xoay, co giãn, xiên, alpha) của từng mảnh sprite; một mảnh khói dùng lại nhiều lần, xoay và co khác nhau |

Thêm hai công cụ phụ khai báo trong template:
- **Tween:** đổi thuộc tính theo mốc thời gian. Có 246 tween alpha, 50 tween scale, 24 tween offset.
- **Timed:** xoá thực thể khi hoạt ảnh chạy xong một lượt.

## 3. Một đòn ghép từ nhiều mảnh

Ví dụ bom của tháp Tricannon cấp 4 (`tower_tricannon_bomb_4`):

| Mảnh | Template | Làm gì | Số |
|---|---|---|---|
| Đạn | `tower_tricannon_bomb_4` | một sprite tĩnh bay parabol, quay theo quỹ đạo | `flight_time` 1,03 s, `g` −900 |
| Đuôi | `tower_tricannon_bomb_4_trail` | dập cụm khói nhỏ dọc đường bay | 70 hạt/giây, đời 0,9–1 s, hoạt ảnh hạt 6 khung chạy 15 khung/giây, xoay ngẫu nhiên 360°, lệch vị trí ±1 |
| Trúng | `explosion_big_KR5` | vụ nổ 21 khung | neo (0,5; 0,1): gốc nổ ở chân |
| Đất | `decal_bomb_crater_KR5` | hố bom trên đất | giữ 1 s, mờ dần tới 2,5 s, scale 1,2 |

Bom lửa của tháp Flamespitter (`bullet_tower_flamespitter_skill_bomb`) thêm hai mảnh:
- **Payload:** sinh ngọn lửa cháy trên đất cùng mod cháy lên mọi địch trong vùng.
- **Mod cháy:** `mod_burning_tower_flamespitter` gắn hoạt ảnh `fire_small` lặp lên người địch trong 3 s.

Trong 207 đạn có:
- 103 đạn có đuôi hạt;
- 135 đạn có hiệu ứng trúng;
- 56 đạn có decal;
- 35 đạn có payload.

Thời gian bay trung vị 0,83 s (p25–p75: 0,73–1,03 s).

**Tia và luồng thở** không phải đạn bay. Đó là **một hoạt ảnh kéo dãn từ nguồn tới đích**: xoay về đích, `scale.x = khoảng cách / image_width` (`scripts.ray5_simple`). Luồng thở của rồng đá quý là hoạt ảnh `hero_evil_dragon_breath_idle` dài 42 khung (1,4 s) kéo dãn như vậy.

## 4. Nhịp

| Hệ | Số hoạt ảnh | Khung trung vị (p25–p75) | Thời lượng trung vị |
|---|---|---|---|
| Nổ | 159 | 18 (10–24) | 0,60 s |
| Lửa | 170 | 18 (8–40) | 0,60 s |
| Nước | 110 | 10,5 (1–24) | 0,35 s |
| Khói, bụi | 62 | 17,5 (13–29) | 0,58 s |
| Tất cả hiệu ứng | 1.590 | 15 (8–26) | 0,50 s |

- **Giữ 2 khung ở mọi hệ:** tỉ lệ khung chạy / hình vẽ là 1,9–2,0.
- **Hiệu ứng trúng nhỏ chỉ 0,33 s.** Ví dụ nước trúng của rồng cây: 10 khung, 5 hình.
- **Nổ lớn 0,6–1,0 s.** Ví dụ nổ kỹ năng tháp lùn: 28 khung, 0,93 s.
- **Có báo trước** cho đòn đánh xuống đất: cột lửa của Flamespitter mở **lỗ trên đất 12 khung (0,4 s)** rồi mới phun.

## 5. Nổ

Tờ khung: `to_khung\no__*.jpg`. Mẫu chuẩn: `explosion_big` (18 khung) và `explosion_KR5_big` (21 khung).

| Khung | Chuyện gì xảy ra |
|---|---|
| 1 (hoặc 1–3) | **Chớp:** một cục tròn vàng, lõi kem xoáy, nhỏ bằng 1/3 vụ nổ. Bản KR5 giữ cục nhỏ 2 khung rồi phình ở khung 3 |
| 2–5 | **Bung:** khói nâu đã to gần đủ ngay khung đầu. Lửa là **các lưỡi liềm vàng cong ra ngoài** cắm trong khói. Dưới đất có **vòng cung vàng** (sóng xung kích) nằm dẹt |
| 6–11 | **Lửa co thành đốm:** lưỡi liềm teo thành chấm vàng rải khắp khối khói. Khói tách thành **cụm tròn riêng**, bay lên. Vòng cung dưới đất mỏng dần, dạt ra ngoài |
| 12–18 | **Tan:** các cụm khói nhỏ dần, mờ dần bằng alpha. Dưới đất còn **vệt bóng xám dẹt** rồi mất |

**Khói nổ vẽ hai tông phẳng:** đỉnh mỗi cụm sáng hơn, đáy tối hơn, vùng màu đều, không gradient. Các cụm có cỡ to, vừa, nhỏ xen nhau, không đều.

Biến thể:
- **`fireball_explosion` (18 khung, mép mềm chỉ 36%):** cầu lửa phồng ở khung 2–4, gồm lõi kem, vàng, viền cam đậm. Ở khung 5–8 cầu vỡ thành cục, khói xám đen hiện ra phía sau. Ở khung 9–12 lửa chỉ còn lưỡi liềm và đốm trên nền khói (lửa bị "ăn" dần). Khói tan ở khung 15–18.
- **`tower_dwarf_skill_main_explosion_idle` (28 khung):** thêm lớp phụ:
  - **sao 4 cánh lấp lánh** rải quanh;
  - **mảnh đá đen có tàn đỏ** văng ra một phía;
  - **lõi lửa nguội dần** từ vàng sang cam rồi đỏ nâu, ngay trong khối khói.
- **Nổ lửa lan (`dwarven_flamespitter…_explosion`):** một vụ nổ ở tâm, cộng **vòng 20–30 ngọn lửa nhỏ** mọc quanh trong cùng khung. Đốm lửa tắt dần từ ngoài vào trong.
- **`explosionDef` (exo, nổ độc xanh):**
  - khung 2–4 có quầng trắng mềm (chớp);
  - **vòng bụi xám dẹt nở ra** trên đất;
  - khối xanh có lỗ đen bên trong;
  - giọt văng lên rồi rơi;
  - vòng cung xanh dưới đất là thứ còn lại lâu nhất.

## 6. Lửa

Tờ khung: `to_khung\lua__*.jpg`.

- **Lửa lặp cực rẻ:** `fire_small`, `fire_medium`, `fire_large` mỗi bản 10 khung = **5 hình**, lặp 0,33 s.
  - **Bốn màu phẳng:** cam đậm ở viền, cam, vàng, kem ở lõi.
  - **Hình:** một lưỡi cong chữ S cộng 2–3 giọt lửa tách rời bay phía trên. Mỗi hình đổi hẳn dáng, không nội suy.
  - **Dùng nhiều bản đặt cạnh nhau, lệch pha** (`random_ts`) nên không thấy lặp.
- **Cháy trên người địch:** mod gắn một `fire_small` lặp suốt 3 s, đặt theo điểm `mod_offset` của từng con.
- **Cột lửa (`dwarven_flamespitter_tower_scorching_torches_fx_idle`, 36 khung, 1,2 s):** chia làm năm đoạn.

  | Khung | Chuyện gì xảy ra |
  |---|---|
  | 1–12 | báo trước: lỗ trên đất mở ra |
  | 13–14 | bông lửa nhỏ nở ở miệng lỗ |
  | 15–16 | một tia mảnh như mũi giáo phóng lên |
  | 17–20 | cột đầy, có dải lửa xoắn quanh thân |
  | 21–36 | cột đứt thành các lưỡi lửa rời bay lên rồi tan; tàn đỏ trên đất tắt; lỗ khép lại |

- **Đạn lửa:** quả cầu có hoạt ảnh 20 khung. Đuôi là hệ hạt dập 50 hạt/giây; mỗi hạt là 8 khung (0,27 s) lửa vàng → cam → đỏ rồi mất.
- **Luồng thở:** hai kiểu.
  - Rồng đá quý thở mây đỏ mềm có tia lách tách. Mây trôi về phía đích, phình to, rồi tan tại chỗ trong nửa sau.
  - Rồng xương thở mây độc (`hero_dragon_bone_breath_idle`, 42 khung).

## 7. Nước

Tờ khung: `to_khung\nuoc__*.jpg`.

- **Toé không có lấy đà:** khung 1 đã là hình to nhất.
  - Đó là một **mão nước gồm các lưỡi nhọn** chĩa lên, có vệt sáng trên lưng lưỡi.
  - Sau đó **khối nước bị đục lỗ từ trong ra** (khung 5–10), sụp xuống, vỡ thành giọt.
  - Giọt rơi xuống, và trên mặt đất còn **một vành giọt hình elip**.
  - Ví dụ `fx_water_splash_big`: 19 khung, 0,63 s.
- **Vẽ trắng để nhuộm:** `hermit_toad_tower_splash_run` vẽ trắng xám, dùng lại cho nhiều màu nước. Phía sau có vài **cụm sương tròn mềm** hiện ở giữa đời.
- **Nước trúng nhỏ (`hero_dragon_arborean_water_hit_fx_idle`, 5 hình, 0,33 s):**
  1. bông nước hình sao;
  2. vỡ thành 6–8 khối tròn văng ra;
  3. thành giọt;
  4. giọt nhỏ hơn;
  5. chấm.

  Mỗi khối và mỗi giọt có **1–2 đốm sáng màu kem bên trong** và một **vành tối ở đáy**. Toàn bộ là màu phẳng.
- **Đuôi đạn nước:** 14 hạt/giây; mỗi hạt 9 khung là chùm giọt có quầng mềm, nhỏ dần thành chấm. Hạt quay theo hướng đạn (`track_rotation`).
- **Bong bóng:** hệ hạt 1–4 hạt/giây, bay lên chậm 3–11 đơn vị/giây, cỡ 0,5–1,4. Hạt "vỡ" bằng cách co về 0,05 trong đời hạt.

### Nước trên map và trong màn (soi 2026-11-23, cho sảnh PokiClash)

Dựng lại khung exo từ `map_viewer/scene.json`. Nền sông, thác vẽ tĩnh; phần động là lớp chồng lên.

| Món | Cách làm | Số đo |
|---|---|---|
| Sóng sông `WavesRiver` | nét bọt trắng hình lưỡi liềm (2 hình), xoay theo dòng, dẹt (sx 0,42, sy 0,28), trôi xuôi, mỗi nét vẽ chồng 3 lần (alpha 1 + 0,25 + 0,25) | 156–225 nét / khung; đời 40 khung (1,3 s): alpha 0 → 1 → 0, cỡ 0,42 → 0,54, trôi ~10 đơn vị / giây |
| Gợn quanh đá `RockRipples` | vòng cung quanh đá phía xuôi dòng, nở ra rồi mờ, có bóng đá tĩnh | 66 khung; cỡ 1,25 → 1,45, alpha 0,05 → 1 → 0, lệch pha |
| Sóng biển ven bờ `Sea` | nét sóng (2 hình) chạy chậm về bờ, nở, mờ | 56 khung; cỡ 0,71 → 0,91, alpha 0 → 0,8 → 0 |
| Lấp lánh `WaterSparks` | cụm đốm mềm (8 hình, cặp tối / sáng) đổi hình tại chỗ | đổi mỗi 6 khung (5 lần / giây) |
| Thác (màn 1, 2, 4) | tấm nước vẽ 9 khung, vệt sáng trôi xuống; chân thác: cụm bọt cuộn 20 khung + vòng gợn 16 khung | 9 khung ở 30 khung / giây: vòng 0,3 s |

Áp vào sảnh PokiClash (`ArtGen/Islands/sanh_moi/nuoc_dong.py`, `GD_Claude/16_ManBoot.md`):
- không vẽ lại thác: shader vẽ nét bọt chồng lên nét vẽ nền, theo trường dòng chảy;
- bản cuộn chính ảnh theo hai pha làm thác nhoà, mất vệt sắc, nên đã bỏ;
- bọt chân thác giữ đục rồi co lại mà tan; mờ dần cả đời thì trông như bong bóng xà phòng.

## 8. Khói và bụi

Tờ khung: `to_khung\khoi__*.jpg`.

- **Hai họ khói:**
  - **Khói nổ** là cel-shading hai tông, mép cứng (phần 5).
  - **Khói bụi** mép mềm. Bụi xây tháp `tower_build_dust` dài 12 khung, 0,4 s, mép mềm 89%: một dải cụm tròn chồng nhau, đỉnh sáng đáy tối, khung 1 đã to nhất, phình nhẹ và mờ dần.
- **Khói tan bằng cách vỡ ra, không chỉ mờ:**
  - Bụi phóng tên lửa (`rocket_gunners_tower_take_off_fx_idle`, 17 khung) mở đầu bằng vòng cung trắng trên đất cộng khối bụi.
  - Khối bụi rồi **vỡ thành nhiều cụm nhỏ**, cụm thành sỏi, mờ dần.
  - Hạt khói đuôi (`Blaze_humitodeatras_run`, 15 khung) là cụm khói đen có lõi lửa đỏ; nó vỡ thành vụn rồi mất.
- **Khói bốc liên tục:** hệ hạt 6–10 hạt/giây, vận tốc 20–25 đơn vị/giây, hướng chếch lên 120°, xoay ngẫu nhiên. Mỗi hạt tự tan trong 0,9–1 s.
- **Khói lửa trại trên map (`SmokeBonfireDef`, exo):** 39 khung, 1,3 s, lặp. Hai cụm khói lệch pha nửa chu kỳ; mỗi cụm có lõi cam ở đáy, xám ở đỉnh, bốc lên, phình ra, mờ dần.

## 9. Hệ hạt: số đo

Port nguyên văn trong `fx_viewer\index.html` (lớp `PSys`, theo `systems.lua`).

| Tham số | Trung vị (p25–p75) | Nhận xét |
|---|---|---|
| Tốc độ phát | 30 hạt/giây (14–50) | đuôi nổ, lửa 30–70; khói 4–10; bong bóng 1–4 |
| Đời hạt | 0,5 s (0,33–0,95) | bằng độ dài hoạt ảnh của hạt |
| Hạt có hoạt ảnh | 100 / 113 | `animated = true, loop = false`, `animation_fps` 15–30 |
| Alpha theo đời | `{255}` ở 95 / 113 | tan đã vẽ trong khung |
| Có vận tốc | 14 / 113 | còn lại đứng yên tại chỗ dập |
| Xoay ban đầu ngẫu nhiên | 53 / 113 | thường ±45° hoặc ±180° |
| Vùng phát | 61 / 113 | ±1–5 đơn vị cho đuôi; tới 1300 × 10 cho bào tử cả màn |
| Scale theo đời | 0,9 → 1,1 (hay gặp nhất); 1 → 1,5; 1 → 0,05 (bong bóng vỡ) | ít dùng |

Cách sinh hạt dọc đường bay: hệ hạt bám theo đạn, chia đều số hạt cần sinh trên đoạn đạn vừa đi trong tick (`stepx = (pos − last_pos) / count`). Vì thế đuôi liền mạch dù đạn bay nhanh.

## 10. Decal và tween

- **Decal mờ dần:** giữ 1–2 s rồi mờ trong 0,5–1,5 s.
  - Mốc kết thúc trung vị 1,8 s (p25–p75: 0,67–2,5 s).
  - Hố bom: alpha 255 từ 1 s → 0 ở 2,5 s.
  - Vết cháy của bom lửa: giữ 1 s, mờ tới 2 s.
- **Bật cỡ một nhịp:** scale 1 → 1,2 → 1 trong 0,1 s.
- **Phình lớn:** 1 → 1,7 → 2 trong 0,53 s (nhanh trước, chậm sau).
- **Thở rất nhẹ cho vật đứng yên:** scale 1,01 ↔ 0,99 mỗi 0,8 s, lặp.
- **Trôi lên xuống:** offset y 0 → 10 → 0 → −10, mỗi đoạn 1 s, nội suy sine.

## 11. Lớp vẽ (z)

| z | Dùng cho |
|---|---|
| `Z_DECALS` 1400 | hố bom, vết cháy, vũng nước, vòng dưới chân (luôn dưới nhân vật) |
| `Z_OBJECTS` 3000 | nổ và lửa đặt trên đất, mod cháy: **xếp theo y cùng nhân vật** nên đứng sau con ở gần, trước con ở xa |
| `Z_BULLET_PARTICLES` 3200 | đuôi đạn |
| `Z_EFFECTS` 3300 | hiệu ứng trúng nổi trên mọi nhân vật |
| `Z_BULLETS` 3400 | đạn |

Vụ nổ đặt gốc ở chân (neo y 0,1–0,13) và `sort_y_offset` −2, nên nó xếp lớp như một vật đứng trên đất.

## 12. Màu và ánh sáng

- **Không viền mực.** Mép hiệu ứng là **một màu đậm hơn của chính nó**: lửa viền cam đậm, nước viền lam đậm, khói đáy nâu tối.
- **3–5 màu cho mỗi vùng:**
  - lửa: kem, vàng, cam, cam đậm;
  - nước: kem, lam nhạt, lam, lam đậm;
  - khói nổ: nâu nhạt, nâu đậm.
- **Quầng mềm chỉ dùng nhỏ:**
  - quầng mềm: chấm tàn lửa có quầng hồng, sao lấp lánh, giọt trong đuôi đạn nước;
  - chớp trắng mềm: chỉ ở nổ đặc biệt.

  Khối chính luôn phẳng.
- **Lửa sáng nhất ở lõi và ở đầu đời,** nguội dần: kem → vàng → cam → đỏ nâu → khói.
- **Nước sáng nhất ở đốm bên trong khối, đáy tối.** Nước không nguội.

## 13. Đổi sang luật của PokiClash

| KR5 làm | PokiClash làm |
|---|---|
| Chuỗi khung vẽ tay cho hiệu ứng chính | Giữ hướng **hạt chồng lớp phẳng** (`chuan_fx`). Lấy từ KR5 **nhịp và cách chia pha**, không đổi sang ảnh khung |
| Giữ 2 khung (15 hình/giây) | Hạt đổi hình theo tuổi (tờ hình rời) nên đổi hình mỗi 2 khung sân, không mỗi khung: giòn hơn, đỡ "trôi" |
| Mép là màu đậm của chính nó | Giữ **viền mực `#2B2118`** của dự án. Thêm **dải màu đậm sát viền** (lớp đậm trong bảng 5 lớp) như KR5 |
| Khói nổ nâu hai tông | Khói **đen than ngả xám, có tro** (luật dự án). Học cách **tách cụm, cụm to vừa nhỏ, bay lên, nhỏ dần** và hai tông phẳng (đỉnh nhạt, đáy đậm) |
| Khói bụi mép mềm, chớp trắng mềm | **Không gradient, không quầng.** Cụm tròn phẳng, alpha phẳng 0,4–0,7, mờ dần cả khối |
| Lưỡi liềm lửa cắm trong khói, teo thành đốm | Làm được bằng hạt: hạt lưỡi liềm cong ra ngoài, đời 0,2–0,3 s, co thành chấm vàng, chấm trôi theo cụm khói |
| Vòng cung sóng xung kích dẹt trên đất | Elip phẳng không viền (vòng mảnh có viền thành vòng đen), nở nhanh, mỏng dần, đứt thành cung |
| Vệt bóng xám dẹt dưới vụ nổ, hố bom giữ 1 s rồi mờ | Vệt đậm của hệ trên sân (alpha 0,3–0,5) ở lớp đất, giữ 1 s rồi mờ 1–1,5 s |
| Nước toé: đỉnh ở khung 1, đục lỗ từ trong, vỡ thành giọt | Đúng luật "rách từ đáy, vỡ nhỏ dần" đã có. Thêm **đục lỗ ở giữa khối** và **vành giọt elip trên đất** |
| Giọt nước có 1–2 đốm kem bên trong, đáy tối | Đúng luật tô phẳng: đốm kem là chấm phẳng, không bóng loáng |
| Lửa lặp 5 hình, nhiều bản lệch pha | Lửa bám người (trạng thái cháy) và lửa trên đất: ít hình, nhiều bản, `random_ts` khác nhau |
| Hạt đuôi tự tan, đứng yên tại chỗ dập | Đuôi đạn: dập hạt đứng yên, tự đổi hình và co, 30–70 hạt/giây. Đuôi liền vì chia hạt theo quãng đạn vừa đi |
| Báo trước 0,4 s bằng lỗ trên đất | Chiêu đánh xuống đất: vòng hoặc vết nứt hiện trước, khớp lúc tướng lấy đà |
| Đòn ghép từ đạn → đuôi → trúng → decal → payload → mod | Viết chiêu theo đúng chuỗi này: mỗi mảnh một hàm, một thời điểm (đã có `At`, `Every`) |

## 14. Công cụ

| File | Làm gì |
|---|---|
| `tools\luamini.py` | bộ chạy Lua thu gọn bằng Python: chỉ tính bảng dữ liệu, không đọc ghi file |
| `tools\kr5_templates.py` | nạp `components` + `templates` + `game_templates` (2.102 template, có kế thừa và số balance) |
| `tools\build_fx_viewer.py <bản rút>` (+ `fx_build.py`, `sheet_worker.py`) | đọc bản rút, dựng `fx_viewer\data.json`, `fx_viewer\sheets\*.png` (mỗi hoạt ảnh một tấm, cắt sát), `fx_viewer\exo\*.json`. Chạy khoảng 2 phút |
| `tools\contact_sheets.py [no,lua,nuoc,khoi]` | tờ khung đánh số `to_khung\*.jpg` (vẽ được cả exo bằng biến đổi affine) |
| `fx_viewer\index.html` | trang xem: thư viện hình, hệ hạt và tổ hợp, chiêu của đơn vị, đáng học |

Tham số URL của trang xem:
- `?tab=lib|tpl|unit|learn`
- `&q=chữ` (tìm theo tên)
- `&tag=no,lua` (lọc theo hệ)
- `&open=<khoá>` (mở thẳng một mục)
- `&atk=<số đòn>`
- `&t=<giây>` (tua tới giây đó rồi dừng)
- `&bg=dark|grass|light|check`
- `&boxes=1`

Giới hạn:
- Cảnh chiêu dựng gần đúng từ template. Đường đi thật, số mục tiêu và các hiệu ứng do script sinh thêm không có.
- Màu nhuộm (`color`) và shader của sprite chưa vẽ.
- Vài hoạt ảnh tên ghép theo cỡ (`size_names`) chưa dò ra, ví dụ `fx_explosion_water`.
