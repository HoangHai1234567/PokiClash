---
name: pokiclash-fx-congthuc
description: >
  Sổ công thức hiệu ứng hạt chồng lớp phẳng của PokiClash (bộ Hỏa 2026-11-10): cách làm từng loại lửa (tròn, nhọn, xoắn,
  dung nham), khói, tro, vòng lửa, phun lửa, cầu lửa, cầu dung nham, kim lửa, lốc xoáy, nổ, thiên thạch, dung nham phun, lên cấp;
  cách thêm hệ mới (Thủy, Mộc, Kim, Thổ...) và chiêu mới trên fxlib.py. Dùng khi làm, sửa, soi bất kỳ hiệu ứng nào, hoặc khi mở
  rộng sang hệ khác.
---

# Sổ công thức hiệu ứng (fxlib)

> Skill gốc: `skill-petclash` (nguyên tắc thiết kế, nhịp clip, khớp animation với hiệu ứng, hiệu năng, bảng kiểm; kèm bộ
> `VFX_KNOWLEDGE_BASE.md` và ba file ghi chú nghiên cứu). Đọc nó trước, rồi quay lại đây làm chi tiết.

Đọc kèm: skill `pokiclash-vfx` (luật hình, vẽ tay, tô phẳng) và `pokiclash-hero-fx` (cảm giác đánh; mục 0b, 0c là lịch sử và
lỗi đã gặp). Sổ này trả lời: **muốn làm hiệu ứng X thì dựng thế nào, số bao nhiêu, tránh lỗi gì.**

**Đã bỏ (người dùng 2026-11-10): aura lửa, sóng nhiệt, kiểu lửa anime.** Không làm lại, không thêm vào bộ mới khi người dùng
chưa yêu cầu. Code của chúng đã gỡ khỏi `bo_hoa.py`, `fxlib.py`, `fire.py`.

Chuẩn mốc (người dùng chốt 2026-11-10): hiệu ứng là **hạt có vật lý vẽ chồng lớp màu phẳng**. Không làm kiểu sprite tĩnh trượt,
nở, mờ. Mọi hiệu ứng soi bằng GIF và tờ 12 khung, so với `ArtGen/Spine/chuan_fx/bo_hoa/*.gif` (trang xem `xem.html`).

## 1. Bộ khung

| File | Vai trò |
|---|---|
| `ArtGen/Spine/fxlib.py` | Thư viện, gồm các phần dưới đây |
| ↳ `Sim` | Lịch: `at(t, fn)` (một lần), `every(t0, t1, nhịp hoặc hàm(s, x), fn)` (luồng; x là tuổi luồng 0..1), `periodic(chu kỳ, n, fn(s, rng, j))` (lặp liền mạch); trạng thái `shake()`, `flash`, `hero_fx` (nhuộm, chớp tướng) |
| ↳ hạt dựng sẵn | `flame` (style, pal, heat), `smoke`, `ash`, `ember`, `spark`, `heat`, `ring` |
| ↳ vật liệu | `mat_flame`, `mat_smoke`, `mat_sprite`, `mat_ring` |
| ↳ còn lại | `Stage` (sân + tướng thật cắt nền), `run` / `save` (GIF và tờ khung) |
| `ArtGen/Spine/fire.py` | Ảnh hạt sinh bằng thuật toán: `blob` / `blob_solid`, `hook`, `tongue`, `curl`, `needle`, `streak`, `ember`, `ash`, `star4`, `lava_rock`, `lava_crack`, `ring`, `ellipse_solid`, `erode_frames` |
| `ArtGen/Spine/bo_hoa.py` | Mọi công thức bộ Hỏa (bảng `EFFECTS`): `py -3 -I bo_hoa.py <thư mục ra> [tên ...]` |
| `ArtGen/Spine/build_hat.py` | Gói GPT vẽ hình hạt (H01–H07); `--nhap` cắt về `hat_gpt/`, `Art.GPT` tự dùng thay hình thuật toán |

Hệ toạ độ là khung sân 540 × 464 (y xuống) như `StageView`:
- chân phe mình `ME` (392, 418), địch `FOE` (158, 236);
- `H` = 150 là chiều cao tướng chuẩn;
- miệng và thân lấy từ `stage_geo()` (đo ảnh tướng thật).

**Nhóm vẽ** (thứ tự chồng): `FLOOR` (dưới đất) → `BACK` (sau tướng) → `HERO` → `FRONT`. Trong mỗi nhóm, lớp xếp: khói 10–11 →
lửa 20–24 → cung, vòng 26–35 → hạt trên cùng 39–45.

## 2. Nguyên tắc chung (áp mọi công thức)

1. **Chồng lớp phẳng.** Mỗi hạt vẽ ở nhiều lớp: mực (ảnh trắng đặc, nở thêm 4–5 đơn vị) rồi các màu từ ngoài vào lõi.
   - Lớp trong nhỏ hơn và co nhanh hơn theo tuổi (`flame_radii`: kem hết ở 40% đời, vàng 68%, cam 95%; `heat` > 1 thì nóng lâu hơn).
   - Hạt cùng lớp hoà thành một khối, chỉ một viền mực ngoài.
   - Ảnh hạt là ảnh xám có vân chì, nhuộm bằng màu (`Image.color` nhân màu).
2. **Màu theo tuổi = nhiệt độ:** kem → vàng → cam → đỏ → khói. Bảng màu ở `PAL` (`lua`, `xoan`, `nham`, `lam`).
3. **Bắn nhanh, cản mạnh** (Epic Toon FX): tia văng khoảng 9 H/s, cản 5–8/s, "bắn rồi khựng". Hạt tan bằng co cỡ hoặc alpha
   phẳng ở 20–30% cuối, không biến mất cái rụp.
4. **Khói** (người dùng dặn): than đen ngả dần sang xám, có tro tán (`ash`), tan dần, bay lên hết, không vụt tắt, không giật.
   - Mỗi cụm một hình cố định; cỡ nở tới đỉnh ở 27% đời rồi co mượt; alpha trơn; xoay chậm dần. Không ăn mòn, không đổi khung.
   - Khói đòn trúng ở `BACK`, ít và nhỏ.
   - Khói đuôi đạn: sinh ≥ 100/s, `r0` ≥ 9, bảng `SMOKE_FIRE`. Thưa thì thành chuỗi bóng đen.
5. **Không che con bị trúng:** nổ trúng thường nhỏ hơn thân, ở `FRONT`. Nổ lớn (thiên thạch, lốc) đặt lõi ở `BACK` ôm viền thân,
   chỉ vài hạt nhỏ ở `FRONT`.
6. **Chớp, nhuộm tướng giữ nét viền** (`hero_fx`, chỉ nhuộm phần sáng hơn 70). Rung bằng `shake` (trauma, giảm dần).
7. **Mọi thứ đổi liên tục:** góc làm tròn 3°, alpha 40 nấc. Vòng, cung, hơi nóng vẽ theo pixel (`ringpx`, `arcpx`, `haze`) để
   viền mực không phóng to theo ảnh.
8. **Lặp liền mạch** (vòng lửa): dùng `periodic`; hạt con lấy `q.rng` của hạt mẹ; hàm vẽ chỉ phụ thuộc tuổi hạt.

## 3. Kiểu lửa (`mat_flame` style)

| Kiểu | Hình hạt | Dùng | Ghi chú |
|---|---|---|---|
| `tron` | `blob` tròn méo, kéo dài theo vận tốc (`stretch_k`) | phun lửa chuẩn mốc, nổ, lõi cầu | mềm, khối liền |
| `nhon` | `hook`: giọt nhọn ngọn quặp nhẹ, ngọn chĩa theo (vận tốc × 0,55 + lên × 0,45) | lửa bốc, ngọn mép | lõi to (0,9 / 0,78 / 0,6), heat 1,6–1,8, lõi dồn về đáy; ngọn quặp gắt thì thừa sợi mảnh |
| `xoan` | khối `blob` đỏ + lưỡi `xhook` cam + vòng `curl` cam | phong cách trang trí phương Đông | bảng `xoan` sáng; màu đỏ bầm thì thành khối thịt |
| **`luoi`** | `flame_lobes`: lưỡi lửa kiểu tranh tướng (chân tròn mập, thân cong, 2–3 ngọn quặp), vân chì **sẫm hơn nền** (gạch chéo thấy rõ) | **mặc định cho chiêu phun** (người dùng 2026-11-10: lửa phun phải hợp nét tướng, nét game) | ngọn ngả ngược hướng bay và lên; sọc 0,8 / 0,6 / 0,38 to để thấy sọc màu như đuôi Huyễn Viêm; đầu luồng r0 13–16, 95 hạt/s, không thì luồng đứt quãng. Cụm tròn `tron` cho phun trông như bong bóng số, bị chê |
| `nham` | `blob`, kéo dài mạnh | cột dung nham, bọt | vỏ nâu đá chỉ khi `p.cool`; giọt rời dùng `lava_drop_draw` (mục 5) |

Thêm kiểu mới:
1. Vẽ hình trong `fire.py` (xám vân chì `_mask_to(m, False)` + bản đặc `_mask_to(m, True)`; ngọn chĩa LÊN).
2. Thêm vào `Art.get` và bảng `PAL`.
3. Thêm nhánh trong `mat_flame`, rồi một cột ở `kieu_lua` để so.

## 4. Công thức từng hiệu ứng (`bo_hoa.py`)

### Phun lửa `make_phun(style, pal)` (1,9 s)

- **Tụ, 0–0,28 s:** than bay vào miệng (tốc × e^3t), cầu lửa nở ở miệng.
- **Phun, 0,28–1,18 s:**
  - 72 hạt/s; đầu luồng ×1,5 trong 0,1 s; tắt dần 0,16 s cuối;
  - nón 12°, tốc 1200–1400, cản 1,8, đời 0,40–0,52;
  - cỡ 7–10 → 28–36, nở theo quãng bay nên luồng loe thành hình nón; nổi −320; rối sin vuông góc tăng theo tuổi.
- **Chạm mặt trước thân** (cách tâm 34): cắt 92% tốc dọc, tạt ngang 15–32%, bỏ lực nổi, đời còn 0,10–0,16, không nở thêm.
- **Khói và tia:** khói từ mép trên luồng 14/s ở `BACK`; tia văng ra từ mép; trúng thì bắn 2 đợt tia cách 0,1 s.

### Cầu lửa `cau_lua` (1,7 s)

- **Tụ, 0–0,3 s:** than hút vào miệng.
- **Bay, 0,45 s, vòng cung nhẹ:**
  - **lõi:** 150 hạt/s đời 0,12–0,18 **bám theo quả cầu** (`upd` đặt lại vị trí theo đường bay + lệch nhỏ), heat 1,9;
  - **đuôi lửa:** 60/s, đời 0,14–0,22, co nhanh;
  - **khói đuôi:** đứng tại chỗ, 110/s, r 9 → 15–19, `SMOKE_FIRE`; kèm tia văng ngược.
- **Trúng:** `explode(s, c, 0.85)`.

Lỗi đã gặp: lõi bị bỏ lại sau thì quả cầu dài như que.

### Cầu dung nham `cau_nham` (2,2 s)

- **Bay:** vòng cung cao 115 (không chạm mép trên).
- **Quả cầu** vẽ riêng: viền mực, đỏ, cam, vàng, kem, và 3 vảy đá trôi quanh mặt; có bọt lửa nham nhỏ.
- **Dọc đường:** nhỏ giọt `lava_drop` 16/s rơi xuống đất; khói đuôi 100/s.
- **Trúng:** 22 giọt toé (±60°, 180–380), 16 cụm nham sau lưng, 5 đá (`rock`), `crater`, khói ở `BACK`, tia 2 đợt.

### Dung nham phun `dung_nham` (2,1 s)

- **0–0,42 s:** khe nứt (`lava_crack`) nở; giọt nhỏ sủi.
- **0,42 s:** rung 0,6, chớp 0,18, `crater(R=30)`; giọt to 8–12 bắn 2 đợt (14 + 8, ±32°, 320–560); 6 đá văng nảy.
- **Cột:** cụm `nham` 90/s phía sau lưng đối thủ (`BACK`). Khói ít.

**Giọt dung nham** (`lava_drop_draw`):
- cầu chính + 2 cục đuôi nhỏ dần theo hướng bay (giọt lệ), bảng `LAVA`, lõi sáng to;
- 30% giọt có vảy đá;
- chạm đất thì `lava_splat`: vũng dẹt nguội dần + vương miện 2–4 giọt bắn lên.

**Miệng hố** (`crater`):
- khe nứt, vũng (`lava_pool`);
- viền 13 cục đá trên elip 1,55R × 0,5R (nửa gần to hơn);
- 4 vảy đá trôi trên vũng;
- bong bóng phồng lên rồi vỡ bắn 2 giọt (7/s), khói mảnh.

Miệng hố trơn hay giọt nhỏ quá thì không đọc ra dung nham.

### Vòng lửa `fire_ring` / `vong_lua` (lặp 2 s)

- **Dải lửa liền:** 84 cụm lửa đứng yên rải dày trên elip (rx ≈ 0,46 bề ngang tướng, ry 16).
  - Mỗi cụm kéo dài theo tiếp tuyến (×1,6), phập phồng lệch pha.
  - Lõi to (0,86 / 0,68 / 0,44) để lõi vàng gộp thành một đường.
  - Nửa xa vẽ ở `BACK`, nửa gần ở `FRONT`.
- **Lưỡi liếm:** 80 lưỡi `nhon` (heat 1,8) mỗi chu kỳ liếm lên từ dải.
- Thêm hơi nóng mảnh (`fxlib.heat`: nét lượn kem không viền), than.

Người dùng chê bản "lửa mọc lên trên một hình tròn": vòng phải **là lửa**.

### Lốc xoáy lửa `loc_xoay` (2,7 s)

- **Hút vào chân:** than từ vòng 1,1 H, có thành phần tiếp tuyến.
- **Phễu:** hạt `tron` bay vòng.
  - Góc = φ + 9·tuổi; độ cao = vy·tuổi; bán kính 16 → 74 theo độ cao.
  - Elip dẹt 0,3; nửa sau ở `BACK`, nửa trước ở `FRONT` và nhỏ hơn; cỡ tăng theo độ cao.
- **Dải cung xoáy** (`arcpx`): bắt buộc, không có thì không đọc ra xoáy.
  - Đoạn cung 110–190° bay lên, loe theo phễu, quay theo chiều xoáy, dày nhất ở giữa đời.
  - Cắt thành hai nửa elip: nửa trên ở `BACK`, nửa dưới ở `FRONT`.
- **Phụ:** vệt `streak` bay vòng, đá bay vòng, khói `SMOKE_FIRE` thoát ở đỉnh.
- **Chiều cao:** khoảng 1,2 H (đối thủ đứng ở y 236, cao hơn thì vượt mép trên).

### Kim lửa `kim_lua` (2,2 s)

- **Hiện:** 7 kim (`needle`, dài 58) lần lượt mỗi 0,07 s thành vòng cung trên đầu con ra chiêu, nở bật 1,25 → 1, kèm phụt lửa.
- **Lơ lửng:** nhấp nhô, chĩa vào điểm đích (lệch ngẫu nhiên trong thân), lửa `nhon` liếm quanh.
- **Phóng:** từ 0,78 s, mỗi 0,09 s một kim, tốc 1500.
  - Đuôi là vệt `spark` kéo dài theo hướng bay; dùng chuỗi cụm lửa thì thành hạt cườm.
  - Trúng: chớp kem nhỏ, 3 cụm lửa, 5 tia, đối thủ chớp lên, rung 0,14.

### Nổ `explode` / `no_lua` (1,5 s)

- **Mở màn:** chớp kem có viền 2 khung (0,42H × cỡ).
- **Lõi:** 12×cỡ cụm `tron` heat 1,6, toả 140–280, cản 4,5.
- **Phụ:** 8 lưỡi `nhon` nhanh; vòng kem mảnh dần; tia 2 đợt cách 0,1 s.
- **Tan:** khói ở `BACK` sau 0,14 s, tro.
- Nhỏ hơn thân con bị trúng.

### Thiên thạch `thien_thach` (2,3 s)

- **Báo trước:** bóng dưới chân to dần.
- **Đá lao xuống:** đường bay mũ 1,6 trong 0,75 s; áo lửa sinh 100/s ngược hướng bay, lửa trùm đầu ở `BACK`, khói đuôi dày, tia.
- **Trúng:**
  - rung 0,9, chớp 0,45;
  - lõi 24 cụm toả nửa trên ở `BACK`, 12 lưỡi nhọn, lửa tạt sát đất phía trước (nhỏ);
  - 2 vòng sóng (dày 9 → 1,5);
  - 8 đá nảy, tia 2 đợt;
  - vành khói 16 cụm sát đất (`BACK`), nấm khói 6 cụm;
  - tro, khe nứt.

### Lên cấp `len_cap` (1,9 s)

- **0–0,25 s:** tụ than xoắn vào thân.
- **0,3 s:** chớp tướng, 2 vòng sóng.
- **Cột lửa:** `nhon` heat 1,7, 110/s giảm dần, không khói.
- **Sao xoắn:** 40/s bay vòng lên (nửa sau `BACK`).
- **0,98 s:** bung 14 sao + than + tro sáng.

### Bảng kiểu lửa `kieu_lua` (lặp 2 s)

4 cột: `tron`, `nhon`, `xoan`, dung nham (giọt phun và rơi về vũng). Dùng để so kiểu mới.

## 5. Thêm hệ mới (Thủy, Mộc, Kim, Thổ, Lôi…)

1. **Bảng màu** trong `PAL` (viền → lõi, phẳng). Khói, bụi thì thêm dải như `SMOKE_DARK`: hơi nước dùng kem trắng; bụi đất dùng nâu
   nhạt → be.
2. **Hình hạt** riêng nếu cần: giọt nước, lá, mảnh đá, tia điện…
   - Vẽ trong `fire.py` (hoặc file mới cùng quy ước: xám vân chì + bản đặc, ngọn chĩa LÊN) và thêm vào `Art.get`.
   - Hoặc làm gói GPT theo mẫu `build_hat.py`.
3. **Ánh xạ công thức Hỏa sang hệ mới:** giữ biên đạo (nhịp, pha, nhóm vẽ), đổi hạt và màu.
   - phun lửa → vòi nước hoặc luồng lá;
   - cầu lửa → cầu nước có đuôi bọt;
   - vòng lửa → vòng sóng, vòng gai;
   - lốc → lốc nước, lốc lá;
   - kim lửa → kim băng, gai gỗ;
   - dung nham → bùn, đá vụn;
   - khói → hơi nước, bụi.
4. **Một file mỗi bộ** (`bo_thuy.py`…) cùng khung `EFFECTS` + `main`, xuất vào `chuan_fx/bo_<hệ>/` kèm `xem.html`.
5. **Soi ít nhất 3 vòng** bằng tờ 12 khung (đọc ảnh), sửa lỗi tệ nhất trước. Ghi mỗi lỗi mới và cách sửa vào sổ này.

### 5b. Bộ Thủy (bản xem trước 2026-11-10, chưa vào game)

`ArtGen/Spine/bo_thuy.py` (GIF ở `chuan_fx/bo_thuy/`, trang `xem.html`), 12 hiệu ứng: tụ nước, tia nước, cầu nước, lưỡi nước,
thương nước, bong bóng, sóng thần, mưa rào, xoáy nước rồi mạch phun, vòi rồng, khiên nước, suối hồi phục.

- **Nét nước của game** (ảnh đã duyệt `Assets/03 Art/Fx/tia_nuoc`, `no_nuoc`, `xoay_nuoc`): lưỡi sóng mập có **mào cuộn**, bọt trắng
  ở mào, sọc xanh đậm / xanh trời / xanh nhạt chạy theo dòng, giọt lệ.
- **Hình hạt do GPT vẽ** (người dùng: "cần gì gọi gpt gen"): gói `hat_nuoc` trong `build_hat.py` (N01 sóng cuộn, N02 giọt, N03
  vương miện nước và nước toé, N04 bọt; xám vân chì, không viền, lưới 2 × 2).
  - Gen tự động: `py -3 -I gen.py gui_gpt/hat_nuoc/luot_1_hat.txt --steps N01,N02,N03,N04` (qua Codex, 4 ảnh khoảng 10 phút, GPT
    làm đúng ngay lượt đầu).
  - Nhập: `py -3 -I build_hat.py --nhap hat_nuoc` → `hat_gpt/wave_*`, `drop_*`, `crown_*`, `foam_*` (đặt giữa khung vuông có lề).
  - Hình tạm khi chưa có ảnh GPT: `water.py`. Bộ mới đăng ký hình qua `fx.Art.EXTRA` và `fx.Art.GPT`.
- **Khác lửa ở đâu:**
  - Lưỡi sóng `draw_wave`: lớp sáng dồn về **ngọn** (bọt ở mào), lửa thì lõi ở chân. Lớp không "nguội" theo tuổi, chỉ co ở cuối.
  - Bảng `W`: mực, (30,104,190), (58,150,226), (140,208,246), bọt (244,252,255).
  - Thay khói bằng **bọt** (`foam`: cụm trắng viền mực, đời ngắn). Thay tia văng bằng **giọt** (`drop`: rơi có trọng lực, chạm đất
    loang vòng nhỏ `plop`).
  - Lúc trúng: `splash` = chớp nước toé chồng lớp (`burst_flash`) + vành lưỡi sóng rải đều + giọt vòng cung + bọt + **vương miện
    nước** mọc từ đất (`crown`, đáy bám đất, cao lên rồi lún) + `ripple`.
  - Vòng sóng: dải xanh dày có viền + vòng bọt trắng mảnh không viền. Vòng mảnh có viền mực thì thành vòng đen (`ring(ink=False)`).
- **Công thức:**
  - `gather` (tụ): giọt và sóng nhỏ bay trôn ốc vào tâm, vòng nước co lại mỗi 0,22 s. `orb` (cầu): 4 lớp tròn rung, 2 vòng xoắn
    quay bên trong, cụm bọt bám mép dưới.
  - `tia_nuoc`: tụ 0,42 s → **lõi tia liền** (mảng đa giác lượn nhẹ) + lưỡi sóng 90/s chạy đè lên làm mép cuộn, tốc 1150, không
    loe; cầu nguồn ở miệng nhỏ dần; chỗ trúng bọt 22/s, giọt bắn ngược 38/s, vương miện + vòng sóng mỗi 0,24 s; cuối cùng `splash`.
  - `cau_nuoc`: tụ 0,6 s (r 30) → vòng cung 0,55 s, nhỏ giọt, bọt → `splash` 1,25 + cột sóng sau lưng + mưa giọt + vũng nước.
  - `bong_bong`: 10 bong bóng tự lái tới đối thủ, lượn sin, vỡ lần lượt; bong bóng lớn cuối cùng vỡ toé.
  - `luoi_nuoc`: tụ 0,32 s → 2 lưỡi **trăng khuyết liền** (5 lớp đồng tâm, dải bọt trắng ở mép trước), nghiêng ±0,35 rad, tốc 900,
    nở 0,4 → 1 trong 0,07 s; vệt mờ trăng khuyết 34/s đời 0,13 s, giọt, bọt ở hai sừng; trúng: vết chém trắng 0,16 s + `splash`.
  - `thuong_nuoc`: 6 mũi (ảnh giọt kéo dài) tụ thành vòng cung trên đầu tướng cách nhau 0,08 s, nở bật 1,25 → 1, nhỏ giọt; phóng
    lần lượt cách 0,1 s, tốc 1500; mỗi mũi trúng: chớp nước nhỏ + 5 giọt + bọt.
  - `song_than`: tụ dưới chân → **một con sóng liền có mào cuộn** (bảng điểm `SONG`, `SONG2`, `SONG3` theo trục "tới trước, lên
    cao", nối cong bằng `smooth`), cao 0,55 → 1,15 H khi lăn tới, bọt trắng phủ mào và dọc chân sóng, lưỡi sóng nhỏ bắn ở chân;
    tới nơi sóng sụp trong 0,2 s, nước chồm qua đầu, bọt tràn hai bên, mưa giọt, vũng nước.
  - `mua_rao`: 7 cụm mây xám xanh (bọt nhuộm màu) tụ trên đầu đối thủ 0,5 s; mưa 125 giọt/giây rơi 760–940, giọt trúng người toé
    bọt, giọt chạm đất loang vòng; vương miện nhỏ 5/s; vũng nước; hết mưa mây co lại.
  - `xoay_nuoc`: cung nước và lưỡi sóng chạy vòng sát đất siết vào tâm 0,95 s → **cột nước liền** (chân loe, thân thon, đầu xoè,
    bọt trên đầu; trong mờ 0,82) vọt lên 1,3 H trong 0,12 s rồi rút, kèm vương miện, vòng sóng, mưa giọt.
  - `voi_rong` (làm 3 lần): phễu = **8 vòng nước dẹt xếp chồng**, vòng trên to hơn đè vòng dưới, cả chồng lắc ngang lệch pha theo
    độ cao (`sin(7,5t − 5h)`) và nghiêng ±0,16 rad; mỗi vòng 3 màu phẳng + viền mực; cả thân vẽ một cụm trong mờ 0,78 ở TRƯỚC đối
    thủ. Thêm sọc bọt trượt quanh mặt trước, mào sóng văng ở hai mép 30/s, bọt ở miệng phễu, giọt hút vào chân; cuối sụp toé.
  - `khien_nuoc` (lặp 2 s): vành tròn xanh có viền phập phồng 2,5%, màng nước alpha 0,2, vệt bọt trượt trên mặt, lưỡi sóng nhỏ chạy
    quanh vành, bọt nổi bên trong, vòng sóng dưới chân.
  - `suoi_hoi`: 2 dòng giọt **xanh ngọc** xoắn quanh thân từ chân lên đầu, 3 vòng xanh ngọc dâng lên (nửa sau vẽ sau tướng), bong
    bóng, lấp lánh, tướng ửng xanh ngọc 2 nhịp. Hiệu ứng lên chính mình dùng màu sáng, ít hình.
- **Mảng nước liền (2026-11-10):** hạt rời không tạo được khối nước lớn (vòi rồng, sóng thần, lưỡi chém, cột phun): trông như đám
  bóng bay loạn. Dùng **mảng đa giác tô phẳng có vân chì** làm thân, hạt chỉ làm mép, bọt, giọt.
  - `fx.poly(group, layer, pts, col, alpha, grow)`: một mảng (grow > 0 = nở ra làm viền mực).
  - `fx.polys(group, layer, [(pts, col, grow), ...], alpha)`: nhiều mảng vẽ đặc rồi cả cụm mới làm trong. Thân trong mờ **phải**
    dùng cái này; chồng từng `poly` trong mờ thì lớp mực lộ ra, thân tối sầm.
  - `smooth(pts)` nối cong qua các điểm; `water_shape(...)` cho hình lồi (mực, xanh đậm, xanh trời, xanh nhạt thu về tâm). Hình có
    chỗ lõm (sóng cuộn) thì vẽ từng lớp bằng bảng điểm riêng.
  - Cho điểm rung nhẹ theo thời gian (`0,03 × sin`) để nét không cứng.
- **Lỗi đã gặp ở bộ Thủy:**
  - Vòi rồng bản 2 là một phễu nhẵn: cứng, tối, như cái xô. Phải chia vòng và cho lắc lệch pha mới ra lốc.
  - Thân nước đặt SAU đối thủ thì đối thủ to che hết; đặt trước và làm trong mờ 0,75–0,82.
  - Cột nước nhẵn đầu tròn trông như quả trứng: cho chân loe, đầu xoè, thêm bọt.
  - Lưỡi sóng xanh đậm phủ lên tướng xanh (hồi phục) rất rối: hiệu ứng lên mình dùng màu sáng khác tông.
  - Hàm vân chì `_hatch` cần `gap` nguyên.

### 5c. Bộ Thủy trong game (2026-11-10)

Đã chuyển 9 chiêu tấn công (tia, cầu, bong bóng, lưỡi, thương, sóng thần, mưa rào, xoáy rồi mạch phun, vòi rồng) và cú va nước của
chiêu lao tới. Khiên nước, suối hồi phục, tụ nước mới có ở bản Python.

- **File:** `Assets/01 Script/Game/Battle/HatNuoc.cs` (phần `partial` của `HatLua`), `HatMang.cs` (mảng nước liền), bảng
  `StageView.WaterFx`, tour `Editor/ThuyFxTour.cs` (menu `PokiClash/Thử/Đảo Thủy: hạt nước …`, ảnh ở `Temp/PokiShots/thuy_fx/`).
- **Ảnh hạt:** `xuat_hat.py` xuất thêm `hat_wave_*`, `hat_waves_*`, `hat_drop(s)_*`, `hat_foam(s)_*`, `hat_crown(s)_*` và ô vân chì
  lặp `van_chi.png`. Chạy lại hai menu `PokiClash/Prefab/Sàn đấu: hạt lửa` và `…Hộp chi tiết tướng: hạt lửa + nút Mana` để gán ảnh
  và dựng con `Mang` (HatMang) trong mỗi lớp hạt.
- **Mảng nước liền trên uGUI (`HatMang`, một `MaskableGraphic` mỗi lớp hạt, là con ĐẦU nên nằm dưới mọi hạt cùng lớp):** hạt gọi
  `MFill` (đa giác kín, cắt tai nên lõm được), `MBand` (dải kín giữa hai đường cùng số điểm), `MRibbon` (dải hở: lõi tia) lúc vẽ;
  `MGrow` nở đường ra làm viền mực, `MSmooth` nối cong, `MSolid` (mảng đặc có viền), `MNested` (ba lớp lồng nhau).
  - Mép ngoài có viền mờ dần 1,5 px cho khỏi răng cưa (lưới uGUI không khử răng cưa).
  - **Trong mờ:** các lớp phải KHÔNG chồng nhau (vẽ từng dải giữa hai đường lồng nhau) thì alpha mới đều. Vòi rồng: mỗi vòng ba
    dải lồng nhau alpha 0,86; chỗ hai vòng chồng nhau đậm hơn, chấp nhận được.
  - Khung của `Mang` đặt rộng 8000, pivot giữa: khung cỡ 0 bị `RectMask2D` của ô xem tướng loại cả lưới.
- **Phát từ đầu clip, không phải khung trúng (khác bộ Hỏa):** `StageView.PreFx` gọi `PlayNuoc(kind, …, lead)` ngay khi clip bắn hoặc
  clip CHIÊU bắt đầu, `lead` = giờ trúng của clip. Pha tụ nước chạy trong lúc tướng lấy đà, nước nhả đúng khung nhả; hàm trả giờ
  tới lúc trúng, `Beam` / `UltFx` ở khung trúng chỉ trả phần còn lại. Tướng giữ dáng nhả `HoldNuoc(kind)` giây (tia tới khi dòng tắt,
  mưa và vòi rồng gần hết). Cảm giác trúng (khựng, rung, bật lùi) dời tới lúc nước chạm đối thủ (`impactAt`).
- **Chiêu cuối chọn theo DẠNG** cho khớp động tác clip của dạng đó (`beasts_cfg._REDESIGN`): đạn xoay quanh người rồi phóng →
  thương nước; xoáy nhốt → vòi rồng; gọi mưa, vật rơi → mưa rào; sóng lan trên đất → sóng thần; trồi lên dưới chân → xoáy rồi mạch
  phun; phun dòng → tia; loạt đạn → bong bóng; lao tới (trượt, húc, liên hoàn) → cú va nước đúng khung chạm (`n_va`).
- **Rig:** 9 dòng Thủy khai `skill_nofx`, `cast_nofx` trong `beasts_cfg.py` (clip chiêu và clip bắn chỉ còn động tác). Clip đã bỏ
  ảnh thì `game_info` không khai `far` nữa: còn `far` thì khung camera sticker dời về phía đối thủ, dạng nhỏ bị cắt chân.
- **Màu theo tướng:** `WThemes` trong `HatNuoc.cs` (bảng 5 màu nước + họa tiết thêm: mảnh băng, sao). Hạt giữ bảng màu lúc sinh
  (`p.stops`) để hai tướng nước đánh nhau không lẫn màu.
- **Bẫy:** biến tĩnh ở `HatNuoc.cs` không dùng biến tĩnh của `HatLua.cs` lúc khởi tạo (thứ tự giữa hai file `partial` không chắc);
  heredoc dài trong Bash bị cắt, viết script vá bằng công cụ Write rồi chạy.
- **Đạn nước cho đòn đánh thường `n_dan` (2026-11-11, pháp sư nước, suất `giong_bao`):** tướng đứng yên bắn (rig khai `stay` cho
  attack). `HatNuoc.NDan`: một viên nước thon (5 lớp ảnh giọt kéo dài như mũi thương, dài 50, dẹt 0,8) rời chỗ nhả `DanTravel` = 0,13 s
  TRƯỚC khung trúng của clip, đuôi rơi giọt và bọt, chạm thì chớp toé 0,44 tH trong 0,12 s + 6 giọt + 2 bọt (nhỏ hơn chiêu mana).
  Không có pha tụ ở chỗ nhả (lúc lấy đà vũ khí còn ở sau vai). Bảng `StageView.WaterAtk` (mã dòng → mã đạn), `AtkFx` gọi từ `PreFx`
  khi clip là attack; ô xem tướng gọi ở `HeroViewer.PreFx`. Giờ trúng của clip attack trong rig = khung nhả + 0,13 s để đạn chạm
  đúng `game.hitTimes` (sân không phải dời số sát thương, khựng, rung). Chưa xem trong Unity lúc viết.
- **Còn mở:** chưa thử trên Android; `tam_tay`, `giot_suong` (rig dựng bằng script riêng) và 2 tướng chưa có rig vẫn bắn tia cũ.

## 6. Mẫu dựng chiêu mới

```python
def chieu_moi(sim):
    """câu biên đạo: là gì, pha nào (tụ -> phát -> lan -> đọng -> tan), mấy giây, màu, nhóm vẽ."""
    mouth, w, h = sim.geo
    tgt = FOE + np.array([0.0, -0.42 * H])
    sim.every(0.0, 0.3, 40, lambda s, x: fx.ember(s, ...))                  # tụ
    sim.at(0.3, lambda s: s.shake(0.3))                                       # phát
    sim.every(0.3, 0.8, 120, lambda s, x: fx.flame(s, pos, vel, life, r0, r1, "nhon", "lua", heat=1.8))
    sim.at(0.8, lambda s: explode(s, tgt, 0.8))                               # trúng
# thêm vào EFFECTS: "chieu_moi": (chieu_moi, dài, chu_kỳ_lặp_hoặc_None, "Nhãn", True)
```

Soi: `py -3 -I bo_hoa.py <ra> chieu_moi`, rồi đọc `<ra>/chieu_moi_soi.png`. Bảng soi nhanh:

| Thấy | Sửa |
|---|---|
| chuỗi hạt cườm, chuỗi bóng đen | sinh dày hơn, hạt đầu to hơn, đời ngắn hơn, hoặc dùng vệt kéo dài |
| đạn dài như que | lõi bám theo đạn |
| giọt nâu như bùn | lõi to hơn, heat cao hơn, bảng sáng hơn |
| che kín con bị trúng | chuyển lõi ra `BACK`, nhỏ lại, ngắn lại |
| khói giật, vụt tắt | khói theo mục 2.4 |
| vòng nâu dày | dùng `ringpx` / `arcpx` |

## 7. Trong game (Unity, thử 2026-11-10)

**Lớp hạt C#:** `Assets/01 Script/Game/Battle/HatLua.cs`, bản chuyển của `fxlib` và các công thức.
- Mô phỏng theo giây sân (`StageView.Update` gọi `hat.Update(dt)`, chia bước ≤ 1/120 s).
- Mỗi khung gom nét vẽ, xếp theo (nhóm, lớp) rồi gán lần lượt cho Image trong hàng chờ của nhóm, nên thứ tự anh em là thứ tự vẽ.
  Chỉ 3 lớp chứa: `HatDat`, `HatSau` (trước lớp tướng), `HatTruoc` (sau lớp tướng). Mỗi lớp một Canvas con để dựng lại riêng.
- Image sinh bằng `Ui.Spawn(Items/HatLua)`, không tạo GameObject lúc chạy.
- Dải cung lốc xoáy dùng 12 ảnh cung xoay sẵn (`hat_arc_*`), nửa trên và nửa dưới bằng `Image.Filled` dọc. Vòng là ảnh `hat_ring` / `hat_rings`.

**Ảnh và prefab:**
- `py -3 -I ArtGen/Spine/xuat_hat.py` xuất `Assets/03 Art/Fx/Hat/hat_*.png` (ưu tiên ảnh GPT trong `hat_gpt/`).
- Menu `PokiClash/Prefab/Sàn đấu: hạt lửa (bộ Hỏa)` (`Editor/HatLuaMenu.cs`): nhập Sprite, dựng prefab `Items/HatLua`, tạo 3 lớp chứa
  trong `Screens/Battle`, gán vào `StageView` (`hatPrefab`, `hatFloor/Back/Front`, `hatSprites`).

**Gắn chiêu:**
- Bảng `StageView.FireFx` (mã dòng → chiêu mana, chiêu cuối). Tướng Hỏa không có trong bảng: mana là cầu lửa.
- `StageView.Beam` gọi `FireBeam` cho tướng Hỏa, thay tia nước nhuộm màu.
- Chiêu cuối: `BattlePlayer.PlayUlt` phát clip CHIÊU; lúc trúng gọi `StageView.UltFx`, chờ tới lúc hiệu ứng chạm đối thủ rồi mới hiện
  sát thương.

**Soi:**
- Menu `PokiClash/Thử/Đảo Hỏa: hạt lửa chiêu mana, chiêu cuối 9 tướng (đang Play)` (`Editor/HoaFxTour.cs`) chụp vào
  `Temp/PokiShots/hoa_fx/` (720 rộng).
- Unity MCP chạy ở cổng **8080**. Sau khi biên dịch, phải chờ Editor rảnh hẳn rồi mới Play; Play lúc đang nạp lại thì báo "script
  missing".

**Quét nét vẽ tay cả bộ** (người dùng 2026-11-10: "cải tiến animation cùng hiệu ứng cho hợp style game"). Trong game (`HatLua.cs`)
mọi chiêu đã bỏ cụm tròn "bong bóng"; `HatLua.cs` là bản chuẩn, `bo_hoa.py` chưa cập nhật các chiêu ngoài phun.
- **Hình hạt** (`fire.py`): mọi hình nhuộm được dùng `_pencil` (nền 246, nét chì gạch chéo **sẫm** 196, gap 3). Khói là `cloud`
  (5–7 bướu, kiểu mây vẽ tay của game) thay cụm tròn. Chớp nổ là `burst` (sao gai truyện tranh) ba lớp: mực, vàng của bảng, kem 0,6.
- **`Tongue(q, tip, up)`** đổi hạt lửa sang lưỡi `luoi`. `tip` +1: ngọn theo hướng bay (nổ, đuôi đạn, cột lửa); −1: ngả ngược (luồng
  phun, lốc). `up`: phần ngả lên.
- **Nổ** (`Explode`): sao gai 0,13 s + vành 9–11 lưỡi **rải đều góc** (ngẫu nhiên thì dồn cục) + vài lưỡi `nhon` nhanh + vòng + tia.
- **Cầu lửa:** lõi tròn nhỏ (r 17–21) + lưỡi lửa mọc từ thân cầu ngả về sau (cùng lớp nên gộp một viền: dáng sao chổi); khói đuôi 55/s.
- **Thiên thạch:** áo lửa 48 lưỡi/s toả rộng (dày hơn thì thành một khúc), lửa quanh đá cũng là lưỡi; trúng: `Explode` + vành 18 lưỡi
  nửa trên rải đều.
- **Lốc:** phễu 62 lưỡi/s `Tongue(-0.8, 0.6)` + dải cung.
- **Nổ lớn** (`BigBurst`): vòng lửa loang, khe nứt, cột lưỡi lửa vọt lên ôm thân 0,5 s (phần lớn `BACK`), nổ sao gai ở 0,18 s, nổ phụ 0,34 s.
- **Khói "cháy"** (`FireStops`): màu lửa → pha với khói của chủ đề, không qua nâu (tông tím, hồng bị bẩn).
- **Giữ dáng ra chiêu** (`HatLua.HoldOf`): phun 1,22 s, kim 1,35 s (tới khi kim cuối phóng), cầu 0,32 s (tới khi cầu rời miệng).
- Bẫy C#: giá trị mặc định của `Theme` không được trỏ tới biến tĩnh khai báo sau bảng `Themes` (khởi tạo theo thứ tự, ra null).

**Chủ đề theo tướng** (người dùng dặn 2026-11-10: hiệu ứng phải hợp hình từng tướng):
- `HatLua.Themes`: mã dòng → `Theme`.
  - `pal`: bảng `Pal`: tinh, tim, vang, sen, nguu, nham, lua.
  - Màu tia, than, vòng (`spark`, `ember`, `ring`, `ring2`).
  - `smoke`: dải khói. Tông tím, hồng, vàng thì khói ngả theo, khói đen chỉ cho lửa thường.
  - `extra`: họa tiết thêm `tinh_the` (mảnh tinh thể), `canh_sen` (cánh sen lượn), `may` (mây xoắn vàng), `sao` (sao nhấp nháy),
    `giap` (mảnh giáp, đá).
- Gọi `UseTheme(hero.id)` trước `PlayMana` / `PlayUlt`. Tia, than, sao dùng ảnh xám (`hat_streakg_*`, `hat_emberg_*`, `hat_starg_0`)
  nhuộm theo chủ đề.
- Tướng mới hoặc hệ khác: soi chân dung (`Resources/<dạng>/<dạng>_portrait.png`), chọn 4 màu lửa từ màu chủ đạo của con, một họa
  tiết lấy từ chi tiết nổi bật (giáp, cánh, ngọc, mây), rồi thêm một dòng vào `Themes`.

**Chiêu phun giữ dáng** (người dùng dặn): tướng đứng ở khung phun cho hết luồng lửa rồi mới về đứng.
- Trên sân: `Actor.holdAt`, `holdUntil` = `Clock + HatLua.BreathHold` (1,22 s); `Update` kẹp `a.t` ở `holdAt`.
- Trong ô xem tướng: `holdLeft`.

**Clip CHIÊU bỏ ảnh** (người dùng chọn "tắt ảnh trong clip"):
- `beasts_cfg_hoa.py` đặt `skill_nofx = True` cho 9 dòng; `beast.py` `clips_of` → `_strip_fx` tắt mọi slot hiệu ứng ở mọi khung clip
  skill. Dựng lại bằng `beast.build_line(<id>, gif=False)` (khoảng 18 s mỗi dòng, cần `opencv-python-headless`).
- Hiệu ứng tuyệt kỹ giờ chỉ do hạt lo, không chồng chéo.

**Hộp chi tiết tướng** (người dùng chọn gắn cả chiêu mana):
- `HeroViewer` có lớp hạt riêng (`HatDat`, `HatSau`, `HatTruoc` trong khung cắt `o_xem`, neo giữa đáy, co theo cỡ ô).
- **Chiêu** nổ tuyệt kỹ, nút thứ năm **Mana** (clip Cast) bắn chiêu mana, vào một điểm đích ảo trước mặt (cách 210 đơn vị, chừa mép).
- Menu `PokiClash/Prefab/Hộp chi tiết tướng: hạt lửa + nút Mana`. Tour `PokiClash/Thử/Đảo Hỏa: hạt lửa trong hộp chi tiết tướng`.

**Còn mở:**
- Chưa thử trên Android, chưa đo số Image và độ nặng.
- "Nổ lớn" (Hỏa Tinh, Kim Sư, Ngưu Quyền) còn đơn giản so với ba chiêu cuối kia.
