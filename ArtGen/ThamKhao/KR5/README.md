# Kingdom Rush 5: học hiệu ứng (nổ, lửa, nước, khói)

Hiệu ứng trận của Kingdom Rush 5 vẽ phẳng 3–5 màu, mép cứng, không shader, không cộng sáng. Đây là nguồn tham khảo gần luật tô
phẳng của PokiClash nhất. Thư mục này có ba thứ: tài liệu phân tích, trang xem, và script dựng lại dữ liệu từ bản rút.

| File | Là gì |
|---|---|
| `HOC_VFX_KR5.md` | Phân tích: ba cách làm hiệu ứng, chuỗi mảnh của một đòn, nhịp, nổ, lửa, nước, khói, số đo hệ hạt, decal, tween, lớp vẽ, đổi sang luật dự án |
| `MO_WEB.bat` | Mở trang xem (cổng 8767) |
| `fx_viewer/index.html` | Trang xem. Bốn tab: **Đáng học** (28 mẫu chọn sẵn có ghi chú); **Thư viện hình** (3.226 hình, lọc theo hệ và nguồn); **Hệ hạt và tổ hợp** (chạy đúng code hạt và tween của game); **Chiêu của đơn vị** (ghép thân + đạn + trúng theo thời điểm bắn) |
| `tools/` | Script đọc bản rút và dựng dữ liệu (xem dưới) |

Bài học đã chuyển thành luật trong skill:
- `.claude/skills/vfx-petclash/hoc_kr5_vfx.md`;
- `pokiclash-hero-fx` mục 1c;
- `pokiclash-fx-congthuc` mục 2b.

## Bản quyền: phần nào không commit

Hình, số template và tờ khung rút từ game là của Ironhide. Chúng chỉ để học trên máy, **không commit, không đăng công khai** (kể
cả artifact), giống `Assets/Epic Toon FX` và ảnh aola trong `BanThu/`. Các mục sau đã có trong `.gitignore`:
- `fx_viewer/data.json`, `fx_viewer/sheets/` (khoảng 430 MB), `fx_viewer/exo/`;
- `to_khung/` (tờ khung đánh số);
- `build_log.txt`.

Repo chỉ giữ code, trang xem và tài liệu chữ.

## Dựng lại dữ liệu

Cần bản rút Kingdom Rush 5 (thư mục có `lua_src`, `images/sprites`, `apk_unpacked`). Máy ổ C có sẵn ở `D:\Ripper\KingdomRush5`.
Máy khác thì chép thư mục đó sang.

```
py -3 -I tools/build_fx_viewer.py D:/Ripper/KingdomRush5     # khoảng 2 phút: data.json, sheets/, exo/
py -3 -I tools/contact_sheets.py                              # tờ khung đánh số vào to_khung/ (thêm no,lua,nuoc,khoi để chọn nhóm)
MO_WEB.bat                                                     # mở trang xem
```

| Script | Làm gì |
|---|---|
| `luamini.py` | Bộ chạy Lua thu gọn viết bằng Python (máy không có Lua). Chỉ tính bảng dữ liệu, không đọc ghi file, không chạy code game |
| `kr5_templates.py` | Nạp `components`, `templates`, `game_templates`: 2.102 template đã gộp kế thừa và số balance |
| `build_fx_viewer.py` | File mỏng, gọi `fx_build.py` (để tiến trình con của multiprocessing không nạp lại dữ liệu); `sheet_worker.py` gói mỗi hoạt ảnh thành một tấm cắt sát |
| `contact_sheets.py` | Tờ khung đánh số trên nền xám giữa, ghi mép mềm % và màu chính; vẽ được cả exoskeleton bằng biến đổi affine |

## Tham số URL của trang xem

| Tham số | Giá trị |
|---|---|
| `tab` | `learn`, `lib`, `tpl`, `unit` |
| `q` | chữ cần tìm |
| `tag` | hệ, vd. `no,lua,nuoc,khoi` |
| `open` | khoá của mục cần mở thẳng, vd. `a:explosion_big`, `x:explosionDef\|idle`, tên template, tên đơn vị |
| `atk` | số thứ tự đòn |
| `t` | giây cần tua tới rồi dừng |
| `bg` | `dark`, `grass`, `light`, `check` |
| `boxes` | `1` để bật khung từng mảnh |

Dùng để chụp soi bằng Chrome headless, vd.
`chrome --headless=new --virtual-time-budget=7000 --screenshot=x.png "http://127.0.0.1:8767/fx_viewer/index.html?tab=tpl&open=tower_tricannon_bomb_4&t=1.45"`.

## Giới hạn

- Cảnh chiêu dựng gần đúng từ template:
  - thân chạy hoạt ảnh của đòn;
  - ở `shoot_time` sinh đạn;
  - đạn tới đích thì sinh hiệu ứng trúng, decal, payload, mod.

  Đường đi thật, số mục tiêu và hiệu ứng do script sinh thêm thì không có.
- Màu nhuộm (`color`) và shader riêng của sprite chưa vẽ. Vài hoạt ảnh ghép tên theo cỡ (`size_names`) chưa dò ra.
- Thư viện còn lẫn thân vài nhân vật (nhiều nhất là tướng robot).
