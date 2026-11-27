# Mùa Noel ở sảnh (2026-11-27)

Người dùng: "tạo ra các mùa cho game, hiện đang là mùa đông giáng sinh: nhạc Giáng sinh ở màn đảo chính, tuyết rơi, tuyết phủ lên một số
phần trên đảo, thi thoảng ông già Noel bay qua bay lại".

Sau đó cùng ngày: "làm thêm tuyết cho đảo Casino", "làm cho cả loading".

Code: `Assets/01 Script/App/Season.cs` (mùa theo ngày, Noel 20/11 → 6/1), `App/Scenes/HubSeason.cs` (HubSeason tự gắn vào sảnh,
VoyageSeason tự gắn vào chuyến tàu qua mây / màn tải), `App/SnowFall.cs`, `App/Scenes/SantaFlyby.cs`, `AudioService` (sảnh →
`Season.HubMusic`, màn tải → `Season.LoadMusic`: trong mùa phát luôn bài sảnh của mùa cho nhạc nối liền). Thử: menu `PokiClash/Thử/Mùa/...`
(ép mùa, cho ông già Noel bay ngay, tour chụp màn tải + sảnh `Temp/PokiShots/mua_noel/`: ảnh 00–02 màn tải, 10–15 sảnh).

Gắn với thế giới (người dùng: "đừng để kiểu UI, khi drag cam thì vị trí cũng phải thay đổi"): ở sảnh tuyết rơi và ông già Noel dời theo
độ dời lớp bản đồ HubPan kéo (bông tuyết có thị sai: lớp gần 1,15–1,3, lớp xa 0,8–0,95; tuyết lặp vô hạn); ở chuyến tàu tuyết trôi theo
camera (qc).

Màn tải: tuyết rơi trên biển và mây (dưới logo, thanh tải), nhạc Noel. Ông già Noel chỉ bay ở sảnh (người dùng: "chỉ hiện ở màn đảo
chính thôi"; bản bay ở màn tải đã bỏ). Lớp trời của sảnh ẩn khi chuyến tàu chạy (ảnh chụp sảnh làm nền chuyển cảnh không dính ông già Noel).

## Ảnh (Magnific, GPT 2.6 1k high, 95 credit / ảnh)

| File | Là gì |
|---|---|
| `gen/pad_meta.json` | ảnh đảo gốc `sanh_dao_<hệ>.png` đệm nền biển cho đúng tỉ lệ khung GPT (3:2, 2:3, 4:3, 3:4): cỡ khung, chỗ đặt |
| `gen/tuyet_<tên>.png` | GPT vẽ lại đảo có tuyết, ảnh mẫu là ảnh đã đệm (thuy, moc, hoa, tho, casino; Kim vốn có tuyết). Game phủ theo tên ảnh đảo `sanh_dao_<tên>` |
| `gen/noel_sheet.png` | tờ ông già Noel: xe trượt + tuần lộc hai dáng phi, nền trong suốt (ảnh mẫu nét: `ArtGen/Islands/refs/world_style.png`) |
| `tach_tuyet.py` | khớp ảnh GPT về ảnh gốc (ECC affine, lệch < 2 px), lấy điểm tuyết (sáng, ít màu, ảnh gốc chỗ đó chưa trắng) + viền mực của đống tuyết → `out/tuyet_<hệ>.png` cùng cỡ ảnh gốc, `out/xem_<hệ>.jpg` |
| `xuat_noel.py` | thu lớp tuyết về cỡ thật của ảnh GPT, cắt tờ Noel thành 3 mảnh (bỏ quầng trắng mờ GPT vẽ quanh hình) → `Assets/03 Art/Seasons/Resources/Seasons/noel/` |
| `out/xem_sanh_gia_lap.jpg` | ghép thử cả bản đồ ngoài Unity (trái: thường, phải: Noel) |

Lớp tuyết là ảnh RGBA chồng lên ảnh đảo (con đầu của "hinh"), không thay ảnh đảo: phần động, đèn đêm, mặt nạ bấm giữ nguyên toạ độ.

## Màn Nhà và đảo Casino (2026-11-27 chiều)

Người dùng: "các màn home / đảo casino chưa thấy tuyết, làm giống ở phần đảo chính", rồi "làm tuyết phủ lên đảo / cây cối / các building".

- Tuyết rơi: `MapSeason` (trong `HubSeason.cs`) tự gắn vào HomeScene / CasinoScene, lớp trời ngay trên khung bản đồ (Nhà: LandView, Casino:
  HubPan), dời theo bản đồ khi kéo (đo điểm bản đồ giữa khung mỗi khung hình, phóng quanh giữa khung không dời tuyết), ẩn lúc chuyến tàu chạy.
- Tuyết phủ: `App/SeasonSkin.cs` đổi thẳng sprite sang bản có tuyết (không chồng Image, số lượt vẽ không đổi): đổi ở mảng dữ liệu của màn
  (HomeScene.art, treeArt) cho vật dựng sau, và quét Image con mỗi giây. Hết mùa thì trả lại. Bản tuyết phải cùng cỡ texture gốc
  (ArtImporter: thư mục `map/` nhập 2048, `map/home_base.png` 4096).
- Ảnh: `map/dung_to.py` dựng 7 tờ 1536 x 1024 nền xanh (`map/to/`): nền đảo Casino, nền Nhà, 13 công trình Casino (cả lều, cọc bãi),
  công trình Nhà (2 tờ), 15 cây của atlas `home_trees`, vách + đồ ven biển. GPT 2.6 1k high vẽ lại có tuyết (`map/gen/`, 7 x 95 credit).
  `map/tach_map.py` khớp từng ảnh (ECC affine; không hội tụ thì dò nét mực ±12 px), lấy điểm tuyết, lấp viền cỏ sót, viền mực, phóng về cỡ
  gốc rồi ghép lên ảnh gốc → `map/out/noel/<tên texture gốc>.png` (cây: cả atlas), xem `map/out/xem_<tờ>.jpg`. `map/xuat_map.py` kiểm cỡ rồi
  chép vào `Assets/03 Art/Seasons/Resources/Seasons/noel/map/`.
- Sửa ảnh gốc (công trình, cây, nền) thì bản tuyết lệch: dựng lại tờ đó, gen lại, tách, xuất.
- Thử: menu `PokiClash/Thử/Mùa/Chụp tuyết Nhà và Casino` hoặc cờ `Temp/map_season_tour.flag` → `Temp/PokiShots/mua_noel_map/`.

## Nhạc, tiếng

- `ArtGen/Music/noel/bgm_sanh_noel_v1.mp3` (149 s, celesta + chuông xe, 100 BPM; đang dùng) và `_v2.mp3` (105 s, valse hộp nhạc):
  Google Lyria 3 Pro qua Magnific (160 credit / bài), giai điệu tự sáng tác, không dựa bài Giáng sinh có sẵn. Đổi bài: chép đè
  `Assets/03 Art/Audio/Music/bgm_sanh_noel.mp3` rồi menu `PokiClash/Âm thanh/Nạp nhạc và tiếng`.
- `ArtGen/Sfx/noel/chuong_xe_1.mp3`, `_2.mp3` (ElevenLabs qua Magnific): chuông xe lúc ông già Noel bay ngang (`noelBells`, đang dùng bản 1).

## Bản quyền

Ông già Noel kiểu dân gian (áo đỏ viền lông trắng, râu trắng, túi quà) không thuộc ai; tránh hình của một hãng / phim cụ thể. Tuần lộc
mũi nâu, không đặt tên: "Rudolph mũi đỏ" là nhân vật có chủ. Nhạc: không dùng bản thu có sẵn hay bài Giáng sinh hiện đại (All I Want
for Christmas, Last Christmas, Let It Snow...); các bài cổ như Jingle Bells, We Wish You a Merry Christmas đã hết bản quyền phần nhạc,
nhưng bản thu của người khác vẫn có chủ. Bài ở đây do Lyria sáng tác mới.
