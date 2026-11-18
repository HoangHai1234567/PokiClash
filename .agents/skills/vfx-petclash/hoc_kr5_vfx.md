# Học hiệu ứng của Kingdom Rush 5 (đục máy 2026-11-18)

Nguồn: bản APK 4.00.54. Bản rút đầy đủ ở `D:\Ripper\KingdomRush5` (máy ổ C). Trong repo: `ArtGen/ThamKhao/KR5/`. Chỉ xem trên
máy, không lấy hình, không đăng công khai: hình và code của Ironhide. Dữ liệu ảnh của trang xem đã `.gitignore`.

Xem ở đâu:
- **Trang xem:** `ArtGen/ThamKhao/KR5/MO_WEB.bat` (http://localhost:8767/fx_viewer/index.html).
  - Tab **Đáng học**: 28 mẫu chọn sẵn theo bốn hệ, có ghi chú.
  - Tab **Thư viện hình**: 3.226 hình, lọc theo hệ.
  - Tab **Hệ hạt và tổ hợp**: chạy đúng code hạt và tween của game.
  - Tab **Chiêu của đơn vị**: ghép thân + đạn + trúng.

  Chưa có dữ liệu thì chạy `py -3 -I ArtGen/ThamKhao/KR5/tools/build_fx_viewer.py D:/Ripper/KingdomRush5` (khoảng 2 phút).
- **Phân tích đầy đủ:** `ArtGen/ThamKhao/KR5/HOC_VFX_KR5.md`.
- **Tờ khung đánh số:** `ArtGen/ThamKhao/KR5/to_khung/<hệ>__<tên>.jpg` (nổ `no`, lửa `lua`, nước `nuoc`, khói `khoi`). Sinh bằng
  `tools/contact_sheets.py`.
- **Tìm mẫu cho hiệu ứng mới:** vào tab Thư viện, lọc hệ, mở mẫu, tua từng khung (◀ ▶, 0,1×), bật "bóng khung kề" để thấy hình
  đổi giữa hai khung. Bảng màu và % mép mềm ở cột phải. Chụp soi tự động dùng tham số `t=` (README của thư mục).

Game này hợp để học vì hiệu ứng trận của họ **vẽ phẳng, mép cứng, 3–5 màu, không shader, không cộng sáng**: gần luật tô phẳng của
dự án hơn mọi nguồn đã đọc. Khác dự án ở ba chỗ:
- họ không viền mực, mép là màu đậm của chính hiệu ứng;
- khói bụi và hơi thở rồng có mép mềm;
- hiệu ứng chính là ảnh khung vẽ tay, không dựng bằng hạt.

## 1. Năm điều lấy về

1. **Giữ 2 khung.** Họ chạy 30 khung/giây nhưng 2/3 hoạt ảnh hiệu ứng có mỗi hình lặp 2 khung (tỉ lệ trung vị 2,0), tức 15
   hình/giây. Áp cho hạt của dự án: đổi hình hạt (tờ hình rời theo tuổi) mỗi 2 khung sân. Chuyển động giòn hơn, không "trôi".
2. **Đỉnh tới ngay khung 1–3, tan chiếm nửa sau.**
   - Nổ: chớp 1 khung (0,03 s); khói và lửa đã to gần đủ ở khung 2; nửa sau là khói tách cụm, bay lên, mờ.
   - Nước toé: hình to nhất ngay khung 1, không lấy đà.
   - Nổ của chiêu lớn có lấy đà 2 khung bằng một cục chớp nhỏ trước khi phình.
3. **Một đòn = chuỗi mảnh nối nhau:** đạn → hạt đuôi → hiệu ứng trúng → decal trên đất → vùng (payload: lửa cháy trên đất) →
   hiệu ứng bám lên địch (mod: lửa lặp trên người 3 s). Mỗi mảnh một việc, một thời điểm. Trong 207 đạn: 103 có đuôi hạt, 135 có
   hiệu ứng trúng, 56 có decal, 35 có payload.
4. **Hạt chỉ "dập" hình tự tan.** Có 113 hệ hạt:
   - 100 hệ là hạt có hoạt ảnh 6–15 khung, đời hạt đúng bằng độ dài hoạt ảnh;
   - alpha giữ nguyên ở 95 hệ;
   - chỉ 14 hệ có vận tốc.

   Hạt sinh ra rồi đứng yên tại chỗ, tự tan theo hình đã vẽ: khói vỡ vụn, lửa nguội vàng → cam → đỏ, giọt nhỏ dần thành chấm.

   Hạt đuôi chia đều theo quãng đạn vừa đi trong tick, nên đuôi liền dù đạn nhanh.
5. **Tan bằng vỡ ra, không chỉ mờ.**
   - Khói: khối → 3–5 cụm nhỏ → sỏi.
   - Nước: khối bị đục lỗ ở giữa → sụp → giọt → chấm.
   - Lửa: lưỡi liềm → đốm.
   - Alpha chỉ cắt ở 30–40% cuối.

## 2. Số đo

| Hệ | Khung trung vị | Thời lượng trung vị | Mẫu đáng xem |
|---|---|---|---|
| Nổ | 18 | 0,60 s (nổ lớn 0,7–1,0) | `explosion_big`, `explosion_KR5_big`, `fireball_explosion`, `tower_dwarf_skill_main_explosion_idle` |
| Lửa | 18 (lặp: 10 = 5 hình) | 0,60 s (lặp 0,33) | `fire_large`, `dwarven_flamespitter_tower_scorching_torches_fx_idle` |
| Nước | 10,5 | 0,35 s (toé lớn 0,63) | `fx_water_splash_big`, `hero_dragon_arborean_water_hit_fx_idle` |
| Khói, bụi | 17,5 | 0,58 s | `tower_build_dust`, `rocket_gunners_tower_take_off_fx_idle` |

**Hạt:**
- Trung vị 30 hạt/giây, đời 0,5 s.
- Đuôi đạn 30–70 hạt/giây, xoay ngẫu nhiên 360°, lệch vị trí ±1–5.
- Khói bốc 6–10 hạt/giây, đi lên khoảng nửa thân mỗi giây.
- Bong bóng 1–4 hạt/giây, bay lên chậm, vỡ bằng co cỡ về 0,05.

**Đạn:** thời gian bay trung vị 0,83 s (0,73–1,03).

**Tia và luồng thở:** một hoạt ảnh kéo dãn từ miệng tới đích, xoay về đích, `scale.x = khoảng cách / bề rộng ảnh`. Luồng thở dài 1,4 s.

**Decal:** hố bom, vết cháy giữ 1–2 s rồi mờ trong 0,5–1,5 s.

**Tween hay dùng:**
- bật cỡ 1 → 1,2 → 1 trong 0,1 s;
- phình 1 → 1,7 → 2 trong 0,53 s;
- thở 1,01 ↔ 0,99 mỗi 0,8 s;
- trôi lên xuống ±10 nội suy sine, mỗi đoạn 1 s.

**Lớp:**
- decal dưới mọi nhân vật;
- nổ và lửa trên đất xếp theo y cùng nhân vật (gốc nổ ở chân, neo y 0,1);
- đuôi đạn, rồi hiệu ứng trúng, rồi đạn ở trên cùng.

## 3. Từng hệ

**Nổ** (`explosion_big`, 18 khung):

| Khung | Chuyện gì xảy ra |
|---|---|
| 1 | cục chớp vàng lõi kem xoáy, bằng 1/3 vụ nổ |
| 2–5 | khói nâu hai tông (đỉnh nhạt, đáy đậm, vùng phẳng) đã to; lửa là các **lưỡi liềm vàng cong ra ngoài** cắm trong khói; **vòng cung vàng dẹt** trên đất |
| 6–11 | lưỡi liềm teo thành đốm vàng rải trong khói; khói tách cụm to, vừa, nhỏ, bay lên; vòng cung mỏng dần, dạt ra |
| 12–18 | cụm nhỏ dần, mờ dần; vệt bóng xám dẹt trên đất rồi mất |

Lớp phụ của nổ lớn:
- sao 4 cánh lấp lánh;
- đá đen có tàn đỏ văng một phía;
- lõi lửa nguội vàng → cam → đỏ nâu ngay trong khói;
- vòng 20–30 ngọn lửa nhỏ mọc quanh tâm (nổ lửa lan);
- vòng bụi xám dẹt nở trên đất.

**Lửa:**
- **Lửa lặp:** 5 hình, 4 màu phẳng (cam đậm viền, cam, vàng, kem lõi). Mỗi hình một lưỡi chữ S cộng 2–3 giọt tách bay phía trên; mỗi hình đổi hẳn dáng. Dùng nhiều bản lệch pha.
- **Cột lửa (1,2 s):**
  1. lỗ trên đất báo trước 0,4 s;
  2. bông lửa ở miệng lỗ;
  3. mũi giáo mảnh phóng lên;
  4. cột đầy, có dải xoắn;
  5. cột đứt thành lưỡi rời bay lên rồi tan; lỗ khép.

**Nước:**
- **Toé (`fx_water_splash_big`, 0,63 s):**
  1. khung 1 là mão nước gồm các lưỡi nhọn có vệt sáng trên lưng;
  2. khung 5–10 khối bị đục lỗ từ trong;
  3. sụp xuống, giọt rơi;
  4. trên đất còn một vành giọt hình elip.
- **Nước trúng nhỏ (0,33 s, 5 hình):** sao → 6–8 khối văng → giọt → giọt nhỏ → chấm. Mỗi khối có 1–2 đốm kem bên trong và vành đậm ở đáy.
- **Vẽ trắng để nhuộm:** một bản toé trắng xám dùng cho nhiều màu nước.

**Khói:**
- **Hai họ:** khói nổ mép cứng hai tông; bụi (xây tháp, phóng) mép mềm, to nhất ngay khung 1, phình nhẹ, mờ trong 0,4–0,6 s.
- **Hạt khói đuôi:** cụm đen lõi đỏ, vỡ vụn trong 15 khung.
- **Khói lửa trại:** hai cụm lệch nửa chu kỳ, lõi cam ở đáy, xám ở đỉnh.

## 4. Đổi sang luật dự án

| KR5 | Dự án |
|---|---|
| Ảnh khung vẽ tay cho hiệu ứng chính | Giữ **hạt chồng lớp phẳng** (`chuan_fx`). Chỉ lấy nhịp, cách chia pha, hình dáng từng pha |
| Mép là màu đậm của chính nó | Giữ viền mực `#2B2118`; thêm **dải đậm sát viền** (lớp đậm của bảng 5 lớp) |
| Khói nổ nâu | Khói **đen than ngả xám, có tro** (luật dự án). Lấy cách tách cụm to vừa nhỏ, hai tông phẳng đỉnh nhạt đáy đậm |
| Bụi, hơi thở, chớp có mép mềm | Không gradient, không quầng: cụm phẳng alpha 0,4–0,7 mờ cả khối |
| Vòng cung sóng xung kích dẹt | Elip phẳng **không viền**, nở nhanh, mỏng dần, đứt thành 3–5 cung, ở lớp đất |
| Khói đòn trúng to | Đòn trúng thường vẫn theo luật: khói ở `BACK`, ít và nhỏ. Khói to, sớm chỉ cho nổ của chiêu |

Công thức đã đổi sang hạt: `pokiclash-fx-congthuc` mục 2b. Ghi chép theo kiểu Clash of Critters: `pokiclash-hero-fx` mục 1c.
