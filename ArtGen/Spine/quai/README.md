# Thư viện `quai/`: rig dựng bằng mã cho lô 10 dòng tướng mới đảo Thủy

Tổng quát hoá từ `ArtGen/Spine/hai_long.py` (Hải Long) theo `DAC_TA_LO_THUY.md` mục 5–6. Tờ mảnh GPT → cắt mảnh → lưới tam giác đều
→ trọng số trơn → xương, slot → clip viết bằng hàm thời gian, nướng 30 khung/giây → JSON Spine 4.2 → `.atomik` + `<mã>_game.json`.
Thiếu gì thì viết trong file riêng của dòng (`ArtGen/Spine/<mã>.py`), **không sửa thư viện**; cần sửa thì ghi vào báo cáo.

## 0. Chạy

```python
# ArtGen/Spine/tm01.py   (py -3 -I KHÔNG tự thêm thư mục script vào sys.path)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quai import anh, luoi, trongso, khung, hoat, mieng, tienhoa, xuat, soi
from quai.khung import Dat
from quai.hoat import Clip, K, cv, song, lui, rung, ease, bao, chuoi_song, an_hien, LoXo, DayMem
```

- Chạy việc nặng (dựng, nướng, xuất): `py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm01.py rig 1`.
- Mọi thứ mở Chrome/Edge ngầm chỉ qua `soi.chay_chrome(...)` (tự gọi `khoa.py chrome`).
- Chỉ cần numpy + Pillow: chạy được cả `py -3 -I` (máy này: Python 3.14 có numpy, Pillow, shapely, **không có cv2**) lẫn
  `D:/spine-venv/Scripts/python -I` (có cv2). Delaunay dùng cv2 nếu có, không thì shapely, không nữa thì thuần Python.
- Con thử chạy hết mọi bước: `py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/quai/vi_du.py` (9 s), ra
  `quai/vi_du_ra/dang_1` (rig gộp tiến hóa) và `dang_2`. Đọc `vi_du.py` như mẫu đầy đủ.

## 1. Quy ước

- **Toạ độ rig**: pixel atlas, x phải, **y lên**, gốc ở chân (giữa hai chân trên mặt đất: game lấy làm tâm bóng), con nhìn sang
  **phải**. Ảnh mảnh: pixel ảnh, y xuống; `Dat` đổi ảnh → thế giới rig.
- Ảnh mảnh co về cỡ atlas lúc nạp (`anh.nap_manh(..., ti_le=0.8)`), nên mọi bước lưới tính theo **pixel atlas**.
- Khung xương nên có `root` (gốc, ở chân) → `move` (lao, nhảy, co cả con: game đo độ dời thân trên xương này) → thân...
- Xương miệng tên `mieng` (trục x chĩa hướng nhả): `game.muzzle` lấy vị trí nó ở khung nhả của `cast`.
- Tên clip (game đọc): `appear, idle, attack, cast, skill, hit, die, evolve, aura`.
- Góc dương = ngược kim đồng hồ (y lên). Khoá như Spine: xoay cộng, dời cộng, tỉ lệ nhân, so với dáng gốc.

## 2. Đích lưới (người dùng đòi lưới dày, mịn, đều)

| | mặc định | ghi chú |
|---|---|---|
| Bước viền | 11 px | `luoi_vung(buoc_vien=...)`; mảnh nhỏ (hàm, vây) 8–10 |
| Bước trong | 15 px | `buoc_trong`; lưới tam giác đều, làm mịn Laplace 4 vòng |
| Dải lưới | ≥ 3 cột mỗi đốt, ≥ 5 hàng khi thân dày > 4 bước | `luoi_dai(so_dot, cot_moi_dot=3, buoc=14)` |
| Góc | in góc nhỏ nhất, TB góc nhỏ, % dưới 25° | góc < 25° chỉ còn ở chóp nhọn / đáy khe hẹp của chính hình |
| Hở | 0 px | pixel có hình (alpha > 40) mà không tam giác nào phủ; viền nới 2 px |
| Trọng số | ≤ 4 xương mỗi đỉnh, chuẩn hoá | chuỗi: B-spline bậc hai; vùng: geodesic; 100% chỉ cho đồ cứng thật |

Số của con thử: thân elip 300×200 → 367 đỉnh, 648 tam giác, góc nhỏ nhất 33°, TB 55°, 0% dưới 25°, hở 0; đầu thật của Hải Long
(547×387, sừng, răng) → 524 đỉnh, 823 tam giác, TB góc nhỏ 50°, 3,9% dưới 25° (ở chóp sừng, khe răng), hở 0.

## 3. API

### `anh` — cắt mảnh, mặt nạ, loang màu, hình giữ chỗ
- `doc_to(path, nguong_sang=236, dien_tich_min=900, gop_px=40) -> To`: loang nền trắng từ mép (giấy trắng khép kín trong mảnh như
  tròng mắt, răng vẫn giữ), bỏ sợi 1 px, tách cụm 8 hướng, mẩu nhỏ cách mảnh lớn < `gop_px` nhập vào. `To.manh`: list dict
  `x0, y0, x1, y1, dt, ids`. `to_moi_nhat(thu_muc, "M01")`: ảnh mới nhất của bước (M01.png, M01_2.png...).
- `gan_theo_o(to, [["dau", "ham", None], ["than", "duoi", "chan"]])` → `{tên: mảnh}` theo ô lưới đã dặn GPT (in mảnh thừa);
  `gan_theo_thu_tu(manh, ten, khoa="x"|"y"|"dt")`; tự viết hàm gán riêng nếu bố cục lạ.
- `luu_manh(to, ten, thu_muc, duc={"vong": "tam"})` → lưu `<tên>.png`; `duc`: đục lòng giấy trắng khép kín: `"tam"`, `[(fx, fy)]`
  (tỉ lệ khung mảnh), hoặc `("tu_dong", diện tích)` (chỉ đục vùng phẳng như giấy). `duc_long(im, ...)` dùng riêng được.
- `to_soi(thu_muc, ten)` → `_soi.png` mọi mảnh trên nền xám.
- `nap_manh(thu_muc, {tên: (hình, w, h, màu)}, ti_le=0.8, ti_le_rieng={"luoi": 0.6})` → `{tên: PIL}`: cắt sát, co về cỡ atlas,
  loang màu ra vùng trong suốt; thiếu ảnh thì vẽ hình giữ chỗ `gia(hinh, w, h, mau)` (`tron, bo, dai, giot, mat, mi, ham, mieng,
  chan, luoi, ong`) để dựng rig song song lúc chờ gen.
- Mặt nạ: `gian, co, mo_mo, lam_mo, thanh_phan, nen_tu_mep, lap_lo, bao_loi, to_da_giac`.

### `luoi` — lưới
- `luoi_vung(im, buoc_vien=11, buoc_trong=15, vien=2, lap=4, tol=1.0, lo_min=None, ten="", buoc_theo_cao=None) -> Luoi`: hình bất
  kỳ (lỗ, nhiều cụm). Lỗ nhỏ hơn (0,8·bước trong)² thì lưới phủ qua (độ trong của ảnh vẫn giữ khe). `buoc_theo_cao=H` (chiều cao
  con, px atlas): bước viền 1,5% H, bước trong 2% H (đè hai bước kia; H = 400 → 6 / 8 px).
- `luoi_dai(im, so_dot, cot_moi_dot=3, hang=None, truc=None, vien=2, buoc=14, mu=False, buoc_theo_cao=None) -> Luoi`: dải dọc
  trục. `truc` mặc định: ngang qua giữa hình, gốc bên trái (GPT vẽ duỗi thẳng nằm ngang). Chân vẽ đứng: `truc=[(w/2, 0), (w/2, h)]`.
  Trục cong: danh sách điểm. `L.s` (độ dài dọc trục mỗi đỉnh), `L.khop(n)` (n+1 khớp chia đều trục, toạ độ ảnh: đặt xương),
  `L.truc[1][-1]` (dài trục).
  - `mu=True` (hoặc `"hai"`; `"dau"` chỉ gốc; `"ngon"` chỉ ngọn): **mũ tròn hai đầu** cho ống có chỏm tròn (tay mập, xúc tu, càng,
    thân sâu): cột mút lùi vào cỡ nửa bề dày, phần chỏm lòi qua cột mút phủ bằng lưới vùng đều **dùng chung đỉnh** với cột mút (liền,
    không khe), đỉnh mũ có `L.s` theo vị trí chiếu lên trục nên `trongso.chuoi(L.s, L.truc[1][-1] / n, ...)` giữ nguyên và tự theo
    đốt mút; có mũ thì số hàng tăng cho ô gần vuông (dải ngắn dày). `L.khop(n)`, `L.hang` vẫn như cũ.
  - `buoc_theo_cao=H`: bước dọc và ngang 2% H, bước viền mũ 1,5% H.
  - Đo trên ống 220×90, trục khai tay: không mũ hở 20 px; có mũ hở 0, góc nhỏ nhất 30°, 0% dưới 25°.
- `luoi_o(w, h, cot, hang, u0, u1, v0, v1)`: lưới ô (đỉnh đặt bằng công thức, như lòng miệng).
- `Luoi`: `pts, tris, nh (hull), nb, n, canh(), ke(), goc(), thong_ke(), in_tk(), ho`.

### `trongso` — trọng số (list dict `{xương: w}` mỗi đỉnh)
- `chuoi(L.s, dai_dot, ten_dot, cha=None, cha_hoa=1.0)`: B-spline bậc hai (giữa đốt 0,75 + 0,125 mỗi đốt kề, ở khớp 0,5/0,5).
  `cha`: gốc chuỗi hoà vào xương cha như một đốt ảo (gốc đuôi mềm vào thân); `dai_dot` một số hoặc list.
- `chuoi_chieu(Q_the_gioi, J_the_gioi, ten_dot, cha)`: lưới vùng bất kỳ, chiếu đỉnh lên đường khớp.
- `chuoi_geo(L, J_anh, ten_dot, cha)`: theo khoảng cách đi trong lưới từ khớp gốc (đuôi cuộn, râu xoắn vẽ cong).
- `vung(L, [(xương, vùng), ...], dai_hoa=20, mac_dinh=None)`: vùng theo thứ tự ưu tiên; vùng = đa giác (toạ độ ảnh), list đa giác,
  mặt nạ bool, `("diem", [(x, y)])`, mảng chỉ số đỉnh. Ranh hai vùng 0,5/0,5, hoà theo khoảng cách đi trong lưới (không nhảy khe).
  Sâu trong một vùng thì về 100% xương đó: muốn cả mảng mềm thì tăng `dai_hoa` (vd. nửa bề rộng vùng).
- `theo_truc(Q, p0, p1, a, b, u0, u1)`: hai xương hoà dọc trục. `cung(n, xuong)`: đồ cứng thật (vỏ, sừng, đá).
- `tron((hệ_số, W1), (hệ_số, W2))`, `nhan(W, hệ_số)`, `chuan(W, toi_da=4)`, `lam_tron(L, W, lan=2, giu=None)`,
  `kiem(W, ten, cho_cung=("dau",))` (in số xương tối đa, số đỉnh bám cứng 100% theo xương), `dijkstra(L, nguon)`.

### `khung` — xương, slot, hình
- `Sk(ten)`; `sk.xuong(ten, cha, x, y, goc=0, dai=0, sx=1, sy=1, the_gioi=False, khong_ti_le=False)`: `the_gioi=True` thì x, y, góc là
  thế giới rig. `sk.chuoi(ten, cha, [J0..Jn])` → `[ten0..]` (đốt i ở Ji chĩa tới Ji+1). `sk.goc_tg(b)`, `sk.the_gioi(P)`.
- `sk.anh(ten, im)`; `sk.slot(ten, xuong, hinh=None, an=False, truoc=None)` (thứ tự gọi = thứ tự vẽ sau → trước; `an=True`: ẩn mặc
  định, clip bật bằng `P.alpha`).
- `sk.luoi_gan(slot, anh, L, W, dat=Dat(...) | the_gioi=V, ten=None)`: lưới có trọng số. **Toạ độ gắn = nghịch đảo ma trận thế
  giới dáng gốc của từng xương** × toạ độ đỉnh, nên xương (hay cha) có tỉ lệ khác 1, lật âm, xoay vẫn đúng.
- `sk.manh(slot, anh, Dat(...), ten=None, xuong=None)`: mảnh cứng (region; xương lệch tỉ lệ thì tự thành lưới 4 đỉnh).
- `sk.cat(slot, den_slot, da_giac_the_gioi)`: mặt nạ cắt (lồi; runtime cắt trên CPU, chỉ dùng khi cần trồi/chìm).
- `sk.diem(ten, xuong, x, y)`, `sk.su_kien(ten, mo_ta)`, `sk.tom_tat()`.
- `Dat(x, y, goc=0, ti=1, neo=(0.5, 0.5), lat=False)`: điểm neo (tỉ lệ ảnh) của ảnh tới (x, y) rig; `lat`: lật ngang (một hình cho
  hai bên). `dat.ra(pts, w, h)`, `dat.mot(p, w, h)`.
- `Pose`: `P.rot(b, độ)`, `P.move(b, dx, dy)`, `P.scale(b, sx, sy)`, `P.alpha[slot] = 0..1`, `P.att[slot] = "tên hình" | None`.

### `mieng` — miệng, mắt
- `long_mieng(sk, slot, anh, dau, ham, ban_le, mui, cot=5, hang=3, tren=(...), duoi=-0.31, doc=(-0.08, 1.0), q_tren=(0, .35, .8, 1, 1))`:
  lòng miệng thuộc hàm dưới (hàng dưới 100% hàm; hàng trên chỉ bám đầu sát bản lề). `ban_le`, `mui`: điểm thế giới. Slot lòng miệng
  đứng **trước** slot hàm và slot đầu (vẽ sau chúng). Chỉnh `tren`/`duoi` (tỉ lệ dài bản lề → mõm) cho khép miệng thì nấp hết.
- `ham_hai_xuong(Q, ban_le, mui, xuong_co, xuong_ham, u0=-0.12, u1=0.15)`: hàm dưới hai xương (cổ họng giãn, bản lề không hở).
- `fit_lid(dau, mi, hat=(x, y) | mat=mask, tranh=mask_go_may, hop=(x0, y0, x1, y1))` → `(cx, cy, góc, tỉ lệ, còn hở)`; in
  "còn hở N px" (phải 0) rồi soi ảnh cận. `dat_mi(dat_dau, dau, kq)` → `Dat` cho `sk.manh(slot_mi, ...)`.

### `hoat` — animation
- Đường cong: `ease(u, "io"|"out"|"in"|"back"|"sin"|"hold"|"lin")`, `K((t, v), (t, v, "out"), ...)` → Track, `cv(t, keys)` số,
  `song(t, chu_ky, pha)`, `lui(t, D)` (giờ lùi: dao động trong clip không lặp tính ở `t - D` thì khung cuối trùng khung 0 idle),
  `rung(t, t0, t1, moi=2)` (rung hai dáng ±1 đổi mỗi 2 khung), `bao(t, t0, t1, vao, ra)`.
- `chuoi_song(P, dot_goc_ra_ngon, t, chu_ky, bien_do, tre=0.17, nguoc_dau=False, ngon_dan=True, bao_giua=False)`: đầu dẫn thân theo
  (cổ), `ngon_dan=False` cho đuôi quẫy (gốc dẫn), `nguoc_dau` hai đốt kề ngược dấu, `bao_giua` biên độ lớn nhất giữa chuỗi.
- `ik_hai_doan(sk, P, dui, cang, dich)`: chân bám đất (gọi cuối hàm dáng, đích = bàn chân dáng gốc theo `move`).
- `an_hien(P, slot, t, [(t0, t1)])`: mí chớp, nhắm.
- `Clip(ten, dur, fn(t, P), loop=False, ev=[(t, tên, chuỗi)], trung=None, mem=[LoXo|DayMem], post=None)`. `gio_trung()`: `trung`
  hoặc sự kiện `trung/can/phun/nha/gam/ban` đầu tiên → `game.hitTimes`.
- `LoXo(dot, k=(300, 240, 190, 150), damp=0.55, maxang=12)`: chuỗi mềm đuổi theo dáng động học (như `longrig.Springs`, viết lại vì
  longrig cần cv2 và cấu trúc rig khác). `DayMem(dot, k0=0.2, k1=0.035, zeta=0.5, luc=f(t, đốt)->(ax, ay), lim=(20, 32))`: dây
  Verlet của Hải Long (râu, lưỡi rũ theo trọng lực), khớp chặn góc mềm bằng tanh.
- `nuong(sk, clip)` → list Pose (khung i ở giây i/30, khung cuối đúng `dur`; clip lặp: khép vòng, khung cuối = khung 0).
- `khop_cuoi(frames, dich, giay=0.25)`: hoà phần lò xo còn dư về khung 0 idle (xuat_het tự làm).
- `thanh_khoa(sk, clip, frames, tol)` → animation JSON + số khoá (RDP từng kênh: xoay 0,15°, dời 0,35, tỉ lệ 0,0025, alpha 0,01;
  độ đậm slot, đổi hình, sự kiện; luôn có khoá ở `dur`). `phu_aura(frames, aura, sk)`: ghép aura cùng giây như runtime.

### `tienhoa` — tiến hóa nối liền
- `gop(skA, skB, tien_to="n_", evo="evo")` → rig gộp M (xương B có tiền tố dưới `evo`; slot B vẽ trên, **ẩn mặc định**, nên clip
  trận của A không phải khoá gì; nướng clip của A trên M vẫn đúng).
- `clip_tien_hoa(M, A, B, idleB0, tiB=hA/hB, fnA=None, fnB=None(t, P, fl), mem=...)` → Clip `evolve` 2,8 s: A gồng, tan
  1,05–1,35 s, B hiện 1,12–1,45 s, co 0,86 → 1, gầm (`fl`), 0,35 s cuối hoà về **đúng khung 0 idle của B**; sự kiện `tu_luc`,
  `doi_dang`, `gam`. `tiB` = chiều cao A / chiều cao B (`soi.chieu_cao`).
- `lech_cuoi(M, frames_evolve, B, idleB0, tiB)` → (px, slot cũ còn hiện, chuỗi) cho báo cáo. `doi_ten_mem`, `doi_ten_clip`,
  `gop_aura(auraA, auraB)`.

### `xuat` — xuất
- `xuat_het(sk, clips, ra_dir, ten, tieu_de, frames=None, dang, so_dang, dung_yen=("cast", "skill"), lao=(), far=(), mieng="mieng",
  beam=1.0, beamStyle="", impact=None, plain=None, cao=None, can=[(tên ảnh, clip, giây, (x, y) | tên xương, bán kính)], ma_goc=3211,
  khop_idle=0.25, noi_them={...})` → chạy hết: nướng, khoá, `<ten>.json/.atlas/.png` (atlas xếp kệ, cạnh bội 8, ảnh trùng chung vùng,
  bảng 256 màu), `<ten>_game.json`, `<ten>.atomik` + nạp lại kiểm, đo nối clip, `khung_<clip>.png` (12 khung, nền xám 150, aura ghép),
  `luoi.png`, ảnh cận, `chan_dung.png` (512, không bóng, bỏ đồ bay của aura), `xem.html`, `so_sanh.md`, `bao_cao.json`; in dung lượng
  so với đích 0,3 MB / trần 0,5 MB (dòng 10: truyền `dich_mb`, `tran_mb`).
- `game.json`: `fps 25, height` (đỉnh khung 0 idle, bỏ slot aura), `hitClips/hitTimes` (attack, cast, skill...), `stay`, `lunge`,
  `far`, `muzzle` (xương `mieng` ở khung nhả cast), `beam, beamStyle, move, shadow`, `impactClips/Stop/Shake/Push/Flash` (mặc định
  mạnh dần theo dạng như beast.py), `plain`. Nhớ: `attack` luôn bị sân kéo lao tới trừ khi có trong `stay`.
- Từng bước: `xep_atlas`, `ghi_spine`, `thong_tin_tran`, `ra_atomik`, `doc_atomik`, `atomik_dinh` (tính đỉnh từ dữ liệu .atomik như
  AtomikPose), `kiem_atomik`, `trang_xem`, `slot_aura`.

### `soi` — soi không cần Chrome
- `Ve(sk, atlas, place)` (sau `ghi_spine`; không truyền thì vẽ từ ảnh mảnh): `ve.ve(P, box, scale, bg, ss=2, luoi=False, xuong=False)`,
  `ve.skin(P)`, `ve.bao(P)`.
- `to_khung(ve, frames, clip, ra, n=12)`, `anh_luoi(sk, ra)`, `anh_can(ve, P, (x, y), r, ra, phong=4)`, `ghep_anh(paths, ra)`,
  `chieu_cao(ve, P, bo)`, `lech(ve, Pa, Pb)`, `chan_dung(ve, P, ra, bo)`.
- `chay_chrome(rig_dir, ten, ra_dir, "anims=attack,cast&n=12&view=cx,cy,w,h")`: tờ khung bằng runtime Spine thật (`mo_xe/chay.py`)
  LUÔN qua `khoa.py chrome`. Che_do `info|keys|mesh|sample` cũng được.

### `sosanh`
- `so_goc(3211)` (số của con gốc từ `D:\RefAnimation\SwordxStaff\scan\monster_<số>\info.json` + dung lượng file gốc),
  `so_sanh(ra_dir, ten, tong, ma)` → `so_sanh.md` (xương, slot, đỉnh, tam giác, khoá, MB, clip, nối clip, lệch .atomik).

## 4. Ví dụ ngắn (đuôi chuỗi + thân vùng)

```python
pc = anh.nap_manh("ArtGen/Spine/inbox/tm01_1/manh", {"than": ("tron", 400, 280, (80, 150, 210)), "duoi": ("dai", 320, 90, (80, 150, 210))}, ti_le=0.8)
sk = khung.Sk("tm01_1")
for n, im in pc.items():
    sk.anh(n, im)
sk.xuong("root"); sk.xuong("move", "root"); sk.xuong("than", "move", 0, 140)
sk.xuong("hong", "than", -90, 140, the_gioi=True)
dat_duoi = Dat(-120, 150, goc=-20, neo=(0.0, 0.5), lat=True)        # ảnh đuôi vẽ ngang gốc bên trái; lật cho ngọn chĩa ra sau
Ld = luoi.luoi_dai(pc["duoi"], 5, ten="duoi")
duoi = sk.chuoi("duoi", "hong", dat_duoi.ra(Ld.khop(5), *pc["duoi"].size))
sk.slot("duoi", duoi[0], "duoi"); sk.slot("than", "than", "than")
sk.luoi_gan("duoi", "duoi", Ld, trongso.chuoi(Ld.s, Ld.truc[1][-1] / 5, duoi, cha="hong", cha_hoa=0.7), dat=dat_duoi)
Lt = luoi.luoi_vung(pc["than"], ten="than")
w, h = pc["than"].size
Wt = trongso.vung(Lt, [("hong", [(0, 0), (0.35 * w, 0), (0.35 * w, h), (0, h)]), ("than", [(0, 0), (w, 0), (w, h), (0, h)])], dai_hoa=50)
sk.luoi_gan("than", "than", Lt, trongso.lam_tron(Lt, Wt), dat=Dat(0, 140))

def idle(t, P):
    P.move("than", 0, 3 * song(t, 2.0))
    chuoi_song(P, duoi, t, 2.0, [3, 4, 6, 8, 10], tre=0.12, ngon_dan=False)

clips = [Clip("idle", 2.0, idle, loop=True, mem=[LoXo(duoi, k=[420, 340, 270, 210, 170])]), ...]   # đủ 8 clip mục 5 đặc tả
xuat.xuat_het(sk, clips, "ArtGen/Spine/inbox/tm01_1/rig", "tm01_1", "Tên dòng dạng 1", dang=1, so_dang=2, ma_goc=3211,
              can=[("can_mieng", "cast", 0.6, "ham", 60)])
```

## 5. Mười bước cho agent dòng

1. Cắt tờ: `doc_to` → `gan_theo_o` (bố cục đã dặn GPT) → `luu_manh(..., duc=...)` → `to_soi`; soi `_soi.png`.
2. Nạp: `nap_manh(thu_muc, GIU_CHO, ti_le)` (giữ chỗ cho mảnh chưa gen để dựng song song).
3. Đặt mảnh vào rig bằng `Dat` theo concept (đọc toạ độ trên ảnh kẻ lưới); xương bằng toạ độ thế giới (`the_gioi=True`, `chuoi`).
4. Lưới: thân, đầu, mảng lớn `luoi_vung`; cổ, đuôi, râu, lưỡi, chân `luoi_dai` (≥ 3 cột mỗi đốt). Xem dòng in: hở 0, % dưới 25° nhỏ.
5. Trọng số: chuỗi `chuoi(..., cha=...)`; vùng `vung(...)` + `lam_tron`; hàm `ham_hai_xuong`; đồ cứng `cung`; `kiem(...)`.
6. Miệng, mắt: `long_mieng` (slot trước hàm, đầu), `fit_lid` → "còn hở 0 px".
7. Clip: viết `fn(t, P)` cho 8 clip (`appear, idle, attack, cast, skill, hit, die, aura`), dao động trong clip không lặp dùng `lui(t, D)`;
   phần mềm `LoXo` / `DayMem`; sự kiện `trung`, `phun`/`het_phun`, `gam`/`het_gam`; mí `an_hien`.
8. Tiến hóa: dựng dạng sau trước; `gop` + `clip_tien_hoa` + `lech_cuoi` (truyền vào `noi_them`).
9. Xuất: `xuat_het(...)` → đọc dòng in (nối clip 0 px, lệch .atomik khung 0 ≈ 0, dung lượng ĐẠT).
10. Soi (bắt buộc): mở `khung_*.png`, `luoi.png`, ảnh cận miệng há to nhất / khớp / râu ở khung nhanh nhất, `uon thử` (xem
    `vi_du.uon_thu`), rồi một lần `soi.chay_chrome` cho runtime Spine thật. Nói rõ cái chưa xem ở tốc độ thật.

## 6. Đã xong / chưa (2026-11-11)

Đã xong và đã chạy trên con thử (`vi_du.py`, 9 s cả hai dạng):
- Cắt tờ GPT (thử trên tờ thật M01, M04 của Hải Long: 0,13 s/tờ, đục lòng vòng sóng), hình giữ chỗ, loang màu.
- Lưới vùng đều (lỗ, nhiều cụm, hở 0), dải lưới, lưới ô; số liệu in mỗi lưới.
- (thêm theo yêu cầu điều phối) `luoi_dai(mu=True)`: mũ tròn hai đầu nối liền dải, hở 0 ở chỏm; `buoc_theo_cao=H` cho `luoi_vung`
  và `luoi_dai`. Con thử có thêm tay mập (ống hai chỏm tròn, 2 đốt, `mu=True`): hở 0, góc nhỏ nhất 26–34°. Bỏ tam giác diện tích ~0 /
  tai viền góc < 1° (điểm viền thẳng hàng sau khi chèn trung điểm): hình phủ không đổi, hết "góc nhỏ nhất 0°" khi bước nhỏ. Hình giữ
  chỗ mới `gia("ong", ...)`.
- Trọng số: B-spline chuỗi (chiếu, geodesic, theo s của dải), vùng geodesic, theo trục, trộn, ≤ 4 xương, làm trơn, kiểm.
- Sk: xương theo toạ độ thế giới, chuỗi, toạ độ gắn đúng với xương tỉ lệ khác 1 / lật; mảnh cứng, lưới, mặt nạ cắt, điểm, sự kiện.
- Miệng 5×3 thuộc hàm dưới, hàm hai xương, `fit_lid` tổng quát (con thử: còn hở 0 px).
- Animation: nướng 30 khung/giây, LoXo, DayMem, IK hai đoạn, RDP, khép vòng, khớp cuối về idle, sự kiện, độ đậm slot, đổi hình, aura.
- Tiến hóa: gộp rig, clip evolve, đo khung cuối (con thử: 0,00 px).
- Xuất: atlas bảng 256 màu, JSON Spine 4.2, game.json, `.atomik` + nạp lại (khung 0 lệch 0,04–0,08 px; giữa clip ≤ 1,4 px do RDP),
  trang xem một file có aura, chân dung 512, so_sanh.md, bao_cao.json. Runtime Spine thật (mo_xe qua khoá chrome) dựng đúng như bộ vẽ
  Python (`vi_du_ra/dang_1/spine_that/`).
- Con thử: dạng 1 (gộp tiến hóa) 44 xương, 21 slot, 1949 đỉnh, 3153 tam giác, 3455 khoá, `.atomik` 73 KB; dạng 2: 22 xương,
  1126 đỉnh, 1848 tam giác, 46 KB.

Chưa có / giới hạn:
- Không có sóng nước kiểu Hải Long (băng chuyền cuộn sóng, dải nước, vương miện toé): dòng 10 dùng lại `hai_long.py`
  (`SPINES`, `WAVES`, `wave_inst`, `ribbon`, `animate_water`, `animate_fx`) trong file của mình.
- Không có giải cổ dài theo đường cong (`hai_long.neck_joints`): quái cổ dài chép hàm đó vào file riêng.
- Lưới không chèn đỉnh theo ý (khớp, mép vùng): trọng số trơn nên chưa cần; cần thì thêm điểm vào `L.pts` rồi tự Delaunay.
- Góc < 25° còn ở chóp nhọn và đáy khe hẹp của hình (do hình); chưa có bước cải thiện cạnh (lật cạnh, gộp điểm) sau Delaunay.
- Bộ vẽ Python: tam giác không khử răng cưa từng cạnh (vẽ lớn 2 lần rồi thu); không có màu tint, deform.
- `.atomik` không có: deform, màu tint, thứ tự vẽ đổi theo clip, nhiều trang atlas, IK/transform constraint (nướng sẵn hết vào khoá).
- `AolaActor` chưa nghe sự kiện; `appear`, `die` chưa được game gọi (đã có trong file, Claude điều phối nối vào game).

## 7. Ghi chú từ các agent dòng (Claude điều phối gom, 2026-11-11 sáng)

- **Đo nối clip ở cả khung 0, trên đỉnh `.atomik`** (dòng 5): `xuat_het` chỉ đo khung cuối; khung 0 có thể lệch tới 12 px mà vẫn báo 0.
  Tự đo thêm khung 0 mọi clip so với khung 0 `idle` trên đỉnh đã da hoá (gồm lò xo, dây mềm), như `noi_atomik` trong `tm05_clip.py`.
- `hoat.lui` chỉ khớp khung cuối: dao động nền cần hoà cả đầu clip (trừ giá trị tại t = 0, hoặc cửa sổ sin² như `tm09.py`); lò xo đầu
  clip phải khớp trạng thái idle (đứng yên vài khung ở dáng đầu rồi mới chạy).
- `tienhoa.gop`: slot đặt trên `root` của dạng sau không đổi tên được (`n_root` không có) → slot mặt nạ `cat` của dạng sau đặt trên
  một xương con riêng (vd. `goc_cat`) (dòng 7).
- `mieng.fit_lid(hat=...)` dò mống theo màu điểm hạt, dễ bắt nhầm da cùng tông → truyền `mat=` (mặt nạ mống tự tính theo màu) (dòng 7).
- Soi bằng runtime Spine thật (`mo_xe/chay.py`, spine-player.js): lưới > ~4 nghìn tam giác cùng mặt nạ cắt làm tràn `PolygonBatcher`
  (`RangeError: offset is out of bounds`) hoặc trang không trả JSON (dòng 7, 8) → soi bằng bộ vẽ Python; kiểm thật trong Unity.
  Viewer có `aura` ở track 1 (MixBlend.add) phải `skeleton.setToSetupPose()` trước mỗi lần apply, không thì sóng phình dần (dòng 10).
- So bình phương hiệu màu phải dùng int32 (int16 tràn → trắng thành đỏ) (dòng 7). `cv2.inpaint` lấy màu nét mực ở biên → dải vẽ bù
  nâu đen: tô màu chính lớp (trung vị, bỏ mực) + vân trước, hoặc dán mảnh GPT đã khớp (dòng 9).
- Cách lai (DAC_TA mục 5): ranh giữa hai lớp không có nét mực (đầu–cổ) dùng tường kẻ tay theo CUNG bo má, không đường thẳng; lớp dưới
  mọc thêm ≥ 30–40 px dưới lớp trên và vẽ bù (dòng 9: khe nêm má–cổ, mảng chữ nhật dưới họng).
- Dải thân ở chỗ cong gắt tự gập (bán kính < nửa bề dày) → làm mượt đường giữa tới R ≥ 1,5 × nửa dày (dòng 8).
