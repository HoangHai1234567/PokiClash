# Islands: sảnh (đảo lớn ghép từ đảo rời) và 5 bản đồ đảo hệ

Nền của scene Hub và 5 scene đảo hệ (spec `world-map`, `zone-stages`).

**Style:** vẽ tay trên giấy như bộ asset game đang dùng:
- vùng đất tô bút chì gạch chéo, để lộ giấy kem;
- nét mực nâu sẫm hơi rung;
- đồ vật là icon vẽ tay mập, dễ thương;
- nhìn gần thẳng từ trên xuống như bản đồ vẽ trong sổ.

**Ảnh mốc đã duyệt (2026-11-02), ở `refs/`:**
- `world_style.png`: nét và mức đơn giản ("rất đẹp, đúng style");
- `world.png`: mức địa hình, cách chừa chỗ cho phần động ("nhìn rất tốt").

**Lịch sử (2026-11-02):**
- Lần đầu ra kiểu bản đồ chiến thuật fantasy, quá rối, giống game khác: bỏ.
- Bản đơn giản đúng style; người dùng muốn thêm địa hình và tách phần động để làm chuyển động.
- Sảnh tách thành quần đảo rời có đảo nhỏ cho công trình: người dùng bỏ. Phải **gen đảo rời nhưng ghép liền khối** như ban đầu, nối tự nhiên như `refs/world.png`, để sau này gắn thêm đảo. Ảnh đảo nhỏ (`refs/tach_roi/`) không dùng.
- Người dùng muốn kéo được sảnh, ra rìa thì hiện mây che (chuẩn bị cho đảo sau), và bấm đảo thì vào bản đồ ghép từ đảo gen của hệ đó: đã làm (mục trên). Mục Z (bản đồ đảo hệ gen riêng) để dành khi muốn bản đồ đảo hệ giàu địa hình hơn.
- Bản đồ đảo hệ: người dùng thấy thiếu địa hình, đường ải đi thẳng dọc lên không đẹp. Học bố cục bản đồ của Clash of Critters, viết lại mục Z.

## Thư mục

| Chỗ | Chứa |
|---|---|
| `pieces/` | Đảo gen rời (`isle_<hệ>.png`, `isle_lang.png`) và biển lặp `SEA_Tile.png`: nguồn để ghép sảnh |
| `inbox/` | Ảnh để menu `PokiClash/Nhập ảnh ArtGen` chép vào game: `ANIM_Sheet.png` (cắt thành `anim_<tên>`) |
| `zones/` | Bản đồ đảo hệ GPT trả về (`zone_<hệ>.png`, khổ 2:3): Claude cắt dải 9:16 rồi mới đưa vào game. `zones/thuy70/`, `zones/moc70/`: ảnh bản đồ dài đảo Thủy, đảo Mộc 70 ải (`tai_ve/` ảnh GPT trả về, `doan_<k>.png` đoạn đã duyệt) |
| `gui_gpt/zone_thuy_70/`, `gui_gpt/zone_moc_70/` | Gói gửi GPT bản đồ dài đảo Thủy, đảo Mộc 70 ải (3 lượt, `HUONG_DAN.md`), sinh bằng `build_zone70.py`, `build_zone70_moc.py` |
| `refs/` | Ảnh mốc, ảnh không dùng nữa (`tach_roi/`) |
| `../guides/` | Ảnh bố cục bản đồ đảo hệ `L_zone_<hệ>.png`, toạ độ ải dự kiến `zone_nodes.json` |

Menu nhập chép **mọi** file trong `inbox/` của mọi gói, nên chỉ để trong `inbox/` những ảnh sẽ vào game nguyên trạng.

## Sảnh và bản đồ đảo hệ: ghép từ đảo rời (đã dựng 2026-11-02)

Script [compose_islands.py](compose_islands.py) (chạy `py -3 -I ArtGen/Islands/compose_islands.py` từ thư mục PokiWar) ghi vào `Assets/03 Art/Islands/`:
- **`world.png`** (1480 × 2320: khung sảnh 1080 × 1920 cộng lề 200 mỗi phía, trong suốt ngoài bờ):
  - mỗi vùng là một đốm đất (bảng `REGIONS`), đất liền là hợp các đốm bo mềm thành một dáng đảo;
  - bờ rung ba tầng (vịnh, khúc lượn, răng cưa);
  - ranh giới vùng cong tay;
  - ruột mỗi vùng lấy từ đảo gen tương ứng;
  - rìa cát, viền mực, bọt, đá ven bờ, đảo đá ngoài khơi;
  - lối nét đứt từ làng vào từng vùng, 4 bãi tròn cho công trình.
- **`sea_tile.png`:** biển lặp từ `SEA_Tile`, trộn mép cho liền.
- **`zone_<hệ>.png`** (1372 × 1500, trong suốt ngoài bờ):
  - bản đồ đảo hệ: đảo gen của hệ đó phóng 1,25 lần, thêm con đường cát tô bút chì qua 8 ải (bảng `ZONE_NODES`, né landmark);
  - toạ độ 8 ải ghi ra `../guides/zone_nodes.json`, đã chép vào `ZONES[].nodes` ở `Web/src/core/data/stages.ts`;
  - bản web vẫn vẽ màn đảo theo khung 9:16 nên đường ải trên web dồn vào giữa.

Đưa vào prefab bằng menu Unity `PokiClash/Prefab/Đảo sảnh: ghép ảnh, kéo, mây viền` ([HubWorldMenu.cs](../../Assets/01%20Script/Editor/HubWorldMenu.cs)):
- **Sảnh:**
  - lớp `keo` kéo được (`HubPan`: kéo trong giới hạn 340 mỗi phía, quá thì nặng tay rồi bật về, thả thì trôi theo đà);
  - biển lặp rộng, ảnh đảo có lề;
  - vành mây quanh rìa: ra rìa mới thấy, che chỗ cho các đảo sau;
  - bảng vùng, làng, công trình giữ chỗ cũ.
- **Màn đảo hệ:** biển lặp cuộn theo bản đồ.

Chép ảnh mới đè cùng tên rồi chạy lại menu là đủ.

**Thêm vùng (đảo) mới:**
1. Gen một ảnh theo mẫu W bên dưới, lưu vào `pieces/isle_<tên>.png`.
2. Thêm một dòng vào `REGIONS` (tâm, bán kính) sát mép khối đất để đốm mới dính liền, và một dòng `ZONE_NODES` nếu đảo có ải.
3. Chạy lại script và menu, thêm bảng vùng vào prefab sảnh.
4. Đất lấn ra ngoài lề thì tăng `MARGIN` (script) và `Margin`, `Pan` (menu), dời vành mây (`LandL/R/T`).

### Ảnh đính kèm cho W

`refs/world.png` (mẫu vùng), `refs/world_style.png` (nét).

### W: Một vùng (đảo rời) (`pieces/isle_<tên>.png`)

Đã có (2026-11-02): `isle_thuy`, `isle_hoa`, `isle_kim`, `isle_moc`, `isle_tho`, `isle_lang`, `SEA_Tile`.

Script chỉ lấy ruột đảo (khoảng 70% giữa), nên đồ vật quan trọng phải nằm gọn ở giữa.

```
1024 x 1024, fully TRANSPARENT background (no sea), in exactly the style of the attached approved map world.png
(simple hand-drawn notebook map, coloured pencil hatching on cream paper, wobbly dark-brown ink outlines, chunky
cute doodles), outlines and hatching about twice as bold as in that map because it will be shown at about 80 %.
One rounded island of the [ELEMENT] element filling about 85 % of the canvas, with a full coastline (thin sandy
rim, wobbly ink coastline, thin white foam scribble), nothing touching the canvas edge. The game cuts out the
middle 70 % of the island and joins it to the other regions, so keep the landmark and every important object
inside that middle part; the outer ring is plain hatched ground with a few grass tufts or rocks.
On the island: [CONTENT]
Leave out the moving parts (added later as animated sprites): no smoke, no flames, no gears, no bells, no
whirlpool, no breaking wave crests. No text, no creatures, no people.
```

## Phần động (A1, `inbox/ANIM_Sheet.png`)

Đã có và đã dựng (2026-11-02):
- `compose_islands.py` cắt sheet thành `Assets/03 Art/Islands/Anim/anim_<tên>.png`.
- Chỗ đặt khai báo trong `ISLE_ANIM` (đảo gen của sảnh) và `ZONE_ANIM` (bản đồ đảo hệ), toạ độ ảnh gốc. Sông dung nham và suối dò theo màu (suối Kim khai báo tay), sóng lấy ngẫu nhiên ngoài biển.
- Script ghi ra `Assets/03 Art/Islands/island_anim.json`; `IslandAnim` (Unity) đọc file này và cho chuyển động.
- Gen lại một đảo thì sửa toạ độ trong hai bảng trên, chạy lại script và menu `Đảo sảnh: ghép ảnh, kéo, mây viền`.
- Tắt "nét vẽ rung" trong cài đặt (hoặc chụp ảnh tĩnh) thì phần động đứng yên.

Prompt đã dùng (để gen lại hoặc gen thêm sheet):

```
1024 x 1024 sprite sheet, fully TRANSPARENT background, same style as the attached world.png (same ink outline,
same pencil hatching, same colours). 16 separate objects, one per cell of the attached numbered 4 x 4 grid (256 px
cells), each about 190-210 px and centred in its cell, nothing crossing a cell edge, no ground and no shadow under
them. These objects will be animated in the game, so draw each one complete and on its own. In grid order:
1 a big round smoke puff; 2 a small round smoke puff; 3 a flame leaning a little to the left; 4 the same flame
leaning a little to the right, taller; 5 three tiny glowing lava sparks and embers; 6 a big bronze gear seen flat,
perfectly round, 8 teeth, hole in the middle; 7 a smaller silver gear seen flat, 6 teeth; 8 a bronze bell with a
small loop on top; 9 a whirlpool spiral seen from above, perfectly round; 10 a golden trident standing upright;
11 a breaking wave crest; 12 three short white curved ripple strokes; 13 a white foam splash; 14 a four-pointed
sparkle star; 15 one green leaf, slightly curled; 16 a soft wind swirl.
```

| Vật | Ảnh | Chuyển động |
|---|---|---|
| Khói núi lửa | 1, 2 | Sinh ở miệng núi, bay lên, nở to, mờ dần |
| Dung nham | 5 | Đốm lửa chạy dọc sông dung nham, nhấp nháy; thỉnh thoảng bắn tia ở miệng núi |
| Lửa | 3, 4 | Lật qua lại giữa 2 hình, phồng nhẹ |
| Suối | 12, 13 | Gợn nước chạy dọc suối; bọt ở cửa suối, chân thác |
| Bánh răng | 6, 7 | Xoay đều, hai bánh ngược chiều |
| Chuông | 8 | Lắc quanh móc treo, nghỉ rồi lắc tiếp |
| Xoáy nước | 9, 10 | Xoáy xoay chậm; đinh ba nhấp nhô |
| Sóng | 11 | Nổi lên trên biển, trôi ngang rồi mờ |
| Lấp lánh | 14 | Nhấp nháy trên nước, chuông đồng, mái vàng |
| Lá rơi | 15 | Rơi lắc lư từ cây thần |
| Gió | 16 | Hiện, trôi, mờ ở hang Nanh Gió |

Mọi lớp động dùng hiệu ứng nét rung sẵn có của UI; dừng ở chế độ chụp ảnh tĩnh; giữ vài chục vật trên màn.

## Bản đồ đảo hệ (Z1–Z5)

**Đã có (2026-11-02), đang dùng:** `zones/zone_<hệ>.png`, 1024 × 1536, nền trong suốt.
- Mỗi ảnh là một đảo dọc, con đường đi từ bãi dưới lên hang boss, mỗi ải một vòng tròn kem trên đường.
- `compose_islands.py`:
  - cắt sát đảo, chừa lề để đảo vừa kín bề ngang màn (màn đảo hiện ảnh rộng 1,27 màn, đảo chiếm 77% ảnh);
  - dò các vòng tròn làm toạ độ ải theo thứ tự từ dưới lên;
  - ghi `Assets/03 Art/Islands/zone_<hệ>.png` và `../guides/zone_nodes.json`.
- Toạ độ đã chép vào `ZONES[].nodes` ở bản web, xuất JSON, nhập Unity. Nút ải của game phủ đúng lên vòng tròn.
- Gen lại một đảo: giữ cùng kiểu, lưu đè vào `zones/`, chạy script rồi menu `Đảo sảnh: ghép ảnh, kéo, mây viền`, chép lại toạ độ ải vào bản web.
- Vòng tròn phải là đĩa kem đặc, viền mực, cỡ đều nhau (script lọc theo màu kem, độ tròn, diện tích). Số vòng dò được là số ải.

**Nhiều ải hơn (ví dụ 12):**
- Ảnh: xin GPT 12 vòng tròn trên cùng một đường (khổ 1024 × 1536 vẫn đủ: khoảng cách vòng 110 px thay vì 160). Cần dài hơn nữa thì gen nhiều đoạn nối dọc như đảo Thủy 70 ải (mục dưới).
- Game: hiện cố định 8 ải mỗi đảo. Phải sửa ở bản web rồi chép sang Unity:
  - dữ liệu ải (`STAGES`), kiểm tra `GameData` (`Số ải trên … = 8`);
  - chuỗi "x/8 ải" và thanh tiến độ (ZoneScene, HubZone);
  - đảo xong (`ZoneDone`), mở Đền Huy Hiệu (`BadgesOpen`);
  - rương mốc `ZONE_CHEST_AT = [4, 8]`;
  - cân bằng cấp đề nghị, rơi đồ.

### Đảo Thủy 70 ải: bản đồ dài 3 đoạn (2026-11-03)

**Vì sao:** đảo Thủy có 70 ải (10 ải tướng, 60 ải xen giữa) mà vẫn chạy trên ảnh 8 ải. Game phải phóng ảnh 3 lần nên ảnh nhòe, đường chỉ dài khoảng 3.000 px khung 1080, chấm ải cách nhau khoảng 30 px. Ảnh mới cần đường dài khoảng 7.300 px khung 1080 để chấm ải cách nhau khoảng 92 px và bệ tướng về cỡ thật.

**Bản đồ:**
- 3 ảnh GPT 1024 × 1536 xếp dọc. Hai đoạn kề chồng nhau 160 px: đoạn trên vẽ lại dải đỉnh của đoạn dưới, bố cục của nó có dán sẵn dải đó. Cả bản đồ 1024 × 4288.
- Màn đảo hiện bản đồ rộng 1,27 màn như đảo 8 ải, nên ảnh không bị nhòe.
- Đất phủ kín bề ngang. Biển chỉ có ở bãi xuất phát dưới đáy và dải mép trên.
- Đường cát rộng 104 px. Mỗi chặng là một nửa chữ S, lần lượt lượn trái, phải, nên mọi ải tướng nằm ở chỗ đường cắt qua giữa bản đồ.
- Mỗi ải tướng có một bãi tròn trên đường. Địa danh của chặng đứng sát bãi; 10 địa danh theo tên chặng ở `GD_Claude/14_HeThongAi.md`.
- Không vẽ vòng tròn ải: game đặt bệ tướng và chấm ải lên đường.
- Không địa danh, hồ, suối nào chạm dải nối.

**Script** [build_zone70.py](build_zone70.py) (chạy `py -3 -I ArtGen/Islands/build_zone70.py` từ thư mục gốc dự án):
- dựng bố cục cả bản đồ `../guides/L_zone70_thuy.png`;
- ghi toạ độ dự kiến `../guides/zone70_thuy.json`: đường, 10 ải tướng, chỗ và phía của địa danh, theo tỉ lệ 0..1 của bản đồ ghép;
- dựng gói `gui_gpt/zone_thuy_70/`: mỗi lượt một file prompt `luot_<k>.txt` kèm bố cục `bo_cuc_<k>.png`, và `HUONG_DAN.md`. File prompt ghi đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh (`zones/thuy70/tai_ve/doan_<k>.png`).
- Sửa độ cao ải tướng ở `STAGE_Y`, khoảng cách chấm ở `GAP`; script báo khi chặng cần biên độ quá lớn hoặc địa danh chạm dải nối.

**Làm lần lượt:**
1. Người dùng gửi GPT đường dẫn `luot_1.txt`; GPT lưu ảnh vào `zones/thuy70/tai_ve/doan_1.png`.
2. Claude soi rồi chạy `--duyet 1` (tự lấy ảnh mới nhất `tai_ve/doan_1*.png`, hoặc ghi rõ đường dẫn ảnh). Lệnh lưu `zones/thuy70/doan_1.png` và dựng `luot_2.txt`, `bo_cuc_2.png`; bố cục đoạn 2 có dán sẵn dải đỉnh đoạn 1.
3. Lặp lại cho đoạn 2 và đoạn 3.

**Ghép** (`--ghep`, đã chạy 2026-11-03, ra `zones/thuy70/zone_thuy70.png` 1024 × 4288):
- GPT giữ nguyên dải dán, nên 3 đoạn nối khít từng pixel. Lỗi chỉ còn ở mép dải dán bên trong đoạn trên: một vạch đổi màu, và mép đường lệch 4–20 px.
- Script nắn mép đường ở 64 hàng phía trên mép dải cho khớp mép đường bên dưới, kéo màu 48 hàng phía trên về màu dưới mép dải, rồi trộn nhẹ 4 hàng quanh mép.
- Tâm đường GPT vẽ lệch đường dự kiến trung bình 3 px, 95% điểm dưới 9 px (đo vuông góc với đường), nên game dùng thẳng đường dự kiến trong `../guides/zone70_thuy.json`.

**Đưa vào game** (`--xuat`, đã chạy 2026-11-03), sau đó chạy menu Unity `PokiClash/Nhập dữ liệu`:
- `Assets/03 Art/Islands/zone_thuy.png`: biển nối với mép trên và mép dưới làm trong suốt để lộ biển lặp của game; suối, hồ, vịnh giữ nguyên. Unity nhập ở 4096 (`ArtImporter`: ảnh `Islands/zone_*`).
- Khoá `zone_thuy` trong `Assets/03 Art/Islands/island_anim.json`: xoáy nước và đinh ba ở hồ xoáy, bọt chân thác, lấp lánh và gợn ở hồ, đầm, vũng, gợn chạy dọc hai suối, sóng ngoài biển và trong vịnh.
- Đảo `thuy` trong `Assets/02 Data/Json/zones.json`:
  - `nodes`: 10 ải tướng;
  - `path`: tâm đường, mỗi 32 px;
  - `stops`: chỗ ải tướng theo tỉ lệ chiều dài đường;
  - `plates`: bên đặt bảng tên, chọn bên chồng ít lên địa danh hơn.
- Màn đảo (`ZoneScene`): đảo có `path` thì bản đồ rộng 1,27 màn, đường mòn theo `path`, bệ cỡ thật ở `stops`; chấm ải rải đều giữa hai bệ (92 px khung 1080).
- `compose_islands.py` thấy `zones/thuy70/zone_thuy70.png` thì không đè ảnh, phần động và toạ độ ải của đảo Thủy.

### Đảo Mộc 70 ải: bản đồ dài 3 đoạn (2026-11-05)

Cùng khuôn đảo Thủy (cỡ 1024 × 4288, 3 đoạn chồng 160 px, đường cát 104 px, cùng độ cao 10 ải tướng). Script [build_zone70_moc.py](build_zone70_moc.py) dùng lại phần chung của `build_zone70.py` (không sửa file đó), gói ở `gui_gpt/zone_moc_70/`, ảnh ở `zones/moc70/`, bố cục `../guides/L_zone70_moc.png`, toạ độ `../guides/zone70_moc.json`. Lệnh như đảo Thủy: `--duyet k`, `--ghep`, `--xuat`.

Khác đảo Thủy:
- Đường lượn sang trái trước (soi gương), để hai đảo không trùng dáng.
- Nước: biển ở bờ rêu đáy và dải mép trên; suối chạy ngang, cầu gỗ quấn dây leo ngay trước ải 15 (chặng 4); hồ lá sen có lạch ra mép (chặng 6).
- Địa danh theo tên chặng ở `GD_Claude/14_HeThongAi.md`: đá rêu và thuyền rêu, đồng hoa chuông, đồi nấm, cầu dây leo, hang nanh đá, hồ lá sen, vách vết vuốt, rừng trúc và miếu, hang pha lê lục, cây thần sau bãi đấu boss.
- Ảnh mẫu lượt 1: đoạn 1 bản đồ dài đảo Thủy đã duyệt (lấy nét và cách dựng; nét bản đồ đảo đã chốt ở đó), bản đồ Mộc 8 ải cũ (lấy màu, dáng đồ vật). Lượt 2, 3 thêm bản đồ cũ để GPT thấy dáng hang nanh, cây thần.
- `--xuat` thay `Assets/03 Art/Islands/zone_moc.png` (bản đồ 8 ải cũ), ghi khoá `zone_moc` trong `island_anim.json` (lá rơi, gió ở hang nanh, lấp lánh ở đồng hoa, hang pha lê, miếu cây thần, gợn hồ, sóng, gợn dọc suối và lạch), đường trong `zones.json`. `compose_islands.py` thấy `zones/moc70/zone_moc70.png` thì không đè đảo Mộc.
- `zone70_moc.json` cũng là nguồn cắt ảnh địa danh cho gói nền trận đảo Mộc (`../BattleBG/build_moc.py`).

**Đã gen, duyệt 3 đoạn (2026-11-05).** Khác đảo Thủy, GPT không giữ nguyên dải dán mà vẽ lại: đoạn 2 cùng chỗ, đoạn 3 vẽ dải lùi lên 33 px. Đường lệch bố cục trung bình 6 px ở đoạn 1, 34 px ở đoạn 2 (có khúc 100 px). Vì vậy:
- `--ghep` dò dời dọc của mỗi đoạn trên cho dải chồng khớp, cắt giữa dải chồng, trộn 24 hàng hai bên; ghi `zones/moc70/ghep.json`. Đoạn 3 dời xuống 33 px (33 hàng biển trên cùng lấy hàng đầu của đoạn).
- `--that` dò lại trên bản đồ ghép: tâm đường theo hàng (bắt lại sau cầu), 10 bãi ải là chỗ bề rộng mặt cát đo vuông góc vượt 140 px (đường khoảng 104 px), suối và lạch theo mặt nước; ghi `zones/moc70/that.json` và ảnh soi `soi_that.png`. Địa danh đo tay trên bản đồ ghép (`SPOTS_REAL`).
- `--xuat [thư_mục_thử]` dùng `that.json` (đường dừng ở giữa bãi đấu boss) thay cho đường dự kiến.

Phần dưới là cách cũ (ảnh bố cục `L_zone_*` + prompt nhiều tầng), giữ để tham khảo khi muốn bản đồ giàu địa hình hơn.


### Học từ bản đồ Clash of Critters

Xem bản đồ chương 1 trong bản bóc tách ở `D:\CrittersRipper` (`Res/UI/Textures/BattleBg/chapter1/txsc_worldmap_bg_01.jpg`). Chỉ học bố cục, không chép hình. Prompt không nhắc tên game, không gửi ảnh của họ cho GPT.

- **Đường là nhân vật chính:**
  - rộng (họ khoảng 1/4 bề ngang, mình lấy khoảng 1/7);
  - lượn chữ S lớn qua gần hết bề ngang, từ dưới lên trên;
  - không phải lối mòn mảnh đi thẳng.
- **Đất phủ kín khung:** không thấy viền đảo giữa biển; màn cuộn dọc như đi một chặng đường.
- **Địa hình nhiều tầng:**
  - hai bên đường là cao nguyên, bậc thềm có vách ngắn (mặt trên màu đất, mặt bên gạch đậm hơn), tạo chiều sâu;
  - cây cối mọc dày, sát mép đường làm khung; mặt đường để trống.
- **Đồ vật kể chuyện dọc mép đường:** lửa trại, biển chỉ đường, khúc gỗ, thang, đá, hoa.
- **Lớp rời:** nút ải là sprite (bệ đá) game đặt lên đường; mây là lớp riêng phủ trên.

**Áp vào mình:**
- Giữ nét vẽ tay bút chì: dày nhưng mỗi cây, mỗi tảng đá vẫn là icon mập rõ hình, không vụn.
- Ảnh không vẽ chỗ trống hình tròn. Game đặt 8 nút ải lên đường. Địa danh của từng ải đứng sát bên đường, xen kẽ trái phải.
- Mỗi đảo một dáng đường (ảnh bố cục):
  - Kim gấp khúc như đường lên núi;
  - Thủy, Mộc, Thổ, Hỏa lượn rộng.
  - Đỉnh đường là bãi đấu boss tròn rộng, khúc giữa phình ra cho mini boss.
- Màn đảo phóng ảnh 1,27 lần và cuộn dọc, nên chỉ thấy khoảng 11–89% bề ngang: đường và địa danh nằm trong 15–85%.

### Ảnh bố cục và toạ độ ải

- [make_layouts.py](../guides/make_layouts.py) dựng `../guides/L_zone_<hệ>.png` từ bảng `PATHS` (điểm uốn của đường, màu đất, màu đường).
- Nó cũng tính 8 ải dự kiến đều nhau dọc đường, ghi vào `../guides/zone_nodes.json` theo khung 9:16 của game.
- Dữ liệu ải hiện tại (`ZONES[].nodes`) **chưa đổi**: có ảnh thật thì Claude đặt lại 8 ải trên đường của ảnh (xuất phát từ `zone_nodes.json`), sửa ở `Web/src/core/data/stages.ts`, xuất JSON và golden, rồi chép sang Unity.

### Ảnh đính kèm cho Z

`refs/world.png` (nét) và `../guides/L_zone_<hệ>.png` của đảo đó.

### Mẫu prompt Z

Thay các ô `[...]` bằng khối của từng đảo bên dưới.

```
Vertical 1024 x 1536 zone map for a vertical mobile game, drawn in the style of the attached approved map
world.png (hand-drawn notebook map, coloured pencil hatching on cream paper, wobbly dark-brown ink outlines,
chunky cute doodles) but RICHER, like a hand-drawn adventure map. Follow the attached layout sketch exactly: the
land fills the whole canvas (no island outline), only the strip of beach and sea at the bottom where the journey
starts.
THE ROAD: keep the road of the sketch on exactly the same path and width, a clean [ROAD] ribbon with a wobbly ink
edge, with the small round widening in the middle and the big round open arena at the top. Nothing stands on the
road or in the arena: the game places stage markers along it.
TERRAIN: [GROUND] ground. On both sides of the road the land is built from raised plateaus and terraces with short
cliff faces (top face in the ground colour, side face in darker hatching), separated by lower ground, so the map
has depth. Dense clusters of [VEGETATION] fill the rest and frame the road edges closely. [WATER] Small props
along the road edges: [PROPS]. Dense, but every tree, rock and prop is a chunky doodle with a clear silhouette;
no tiny noisy details, no isometric 3D, no realistic rendering.
STOPS: 8 landmarks stand right BESIDE the road, evenly spaced from the bottom to the top, alternating left and
right: [STOPS] The 4th stands next to the middle widening (mini-boss). The 8th is the boss lair right behind the
top arena, the biggest landmark.
Moving things are added later as animated sprites, so do NOT draw: [LEAVE OUT]. No text, no signs with letters,
no creatures, no people.
```

### Z1: Đảo Thủy (`zones/zone_thuy.png`, bố cục `L_zone_thuy.png`)

```
[ROAD] = pale sand
[GROUND] = light green grass and pale sand
[VEGETATION] = palm trees, round tropical bushes, big ferns, coral rocks near the water
[WATER] = A winding blue river runs from a waterfall down to small lagoons and crosses the road once under a
mossy wooden bridge; a few tide pools.
[PROPS] = big shells, a beached rowboat, fishing nets on poles, crates, a wooden signpost, little lanterns
[STOPS] = 1 a beach of big pastel seashells; 2 a cove of pink and orange coral; 3 the mossy wooden bridge over
the river; 4 a white-and-red lighthouse on rocks; 5 a few snail-shell cottages; 6 a silver waterfall falling into
a pool; 7 a round mirror-like lake; 8 a round rocky basin of calm deep-blue water (the whirlpool and trident are
added later).
[LEAVE OUT] = whirlpool, trident, foam splashes, breaking waves
```

### Z2: Đảo Hỏa (`zones/zone_hoa.png`, bố cục `L_zone_hoa.png`)

```
[ROAD] = ash-grey stone
[GROUND] = dark red-brown volcanic
[VEGETATION] = black dead trees, trees with glowing orange ember leaves, thorny shrubs, black boulders, red
crystals
[WATER] = A glowing orange lava river crosses the road once under a stone bridge.
[PROPS] = stone lanterns, empty braziers, obsidian rocks, little vent holes in the ground, prayer flags without
writing
[STOPS] = 1 a black-rock pier on the beach; 2 a lava stream with round stepping stones; 3 a lotus temple with red
roofs and an unlit lamp; 4 a big round stone furnace with an empty opening; 5 a grove of ember-leaf trees; 6 a
stone gate shaped like a spoked wheel; 7 a smoky slope with vent holes; 8 a volcano with a golden wheel on its rim
and a clear crater.
[LEAVE OUT] = smoke, flames, sparks
```

### Z3: Đảo Kim (`zones/zone_kim.png`, bố cục `L_zone_kim.png`)

```
[ROAD] = light cobblestone
[GROUND] = grey stone and silver-blue rock with patches of pale grass; the zigzag road climbs a mountain, so the
plateaus are stepped mountain ledges
[VEGETATION] = dark pine trees, grey boulders, clusters of silver crystal ore
[WATER] = A grey-blue mountain stream crosses the road once under an iron bridge.
[PROPS] = rails with mine carts, crates, iron lamp posts, chains, barrels
[STOPS] = 1 a small iron harbour crane; 2 two round flat stone bases side by side (the gears are added later);
3 a steel watchtower; 4 a small roof on four posts with an empty space under it (the bell is added later); 5 a mine
entrance with a mine cart; 6 a foundry chimney beside a pot of glowing molten metal; 7 a nest of black metal
feathers on a crag; 8 a bell tower with two dark wings and an empty arch (the bell is added later).
[LEAVE OUT] = gears, bells, smoke, sparks
```

### Z4: Đảo Mộc (`zones/zone_moc.png`, bố cục `L_zone_moc.png`)

```
[ROAD] = warm dirt
[GROUND] = lush green
[VEGETATION] = big round forest trees, giant red mushrooms, hanging vines, ferns, flowers
[WATER] = A winding stream crosses the road once under a log bridge; a small pond.
[PROPS] = logs, stumps, a campfire ring without fire, a wooden signpost, berry bushes, ladders on the terraces
[STOPS] = 1 a shore of mossy rocks; 2 a hill of giant red mushrooms; 3 a vine-covered arch beside the road; 4 a
cave mouth between two fang-shaped rocks; 5 a meadow of glowing flowers; 6 a young round tree with a tiny shrine;
7 a valley of giant leaves; 8 an enormous spirit tree with a little shrine in its roots.
[LEAVE OUT] = falling leaves, wind swirls, sparkles
```

### Z5: Đảo Thổ (`zones/zone_tho.png`, bố cục `L_zone_tho.png`)

```
[ROAD] = pale sand
[GROUND] = golden ochre and sand
[VEGETATION] = cacti, dry bushes, palm trees by an oasis, tumbleweeds
[WATER] = A dry cracked riverbed crosses the road once under a rope bridge; a small oasis pond with palms.
[PROPS] = clay pots, a wooden cart, banners on poles without writing, stone markers, wheat bundles
[STOPS] = 1 a golden beach with a big shell; 2 terracotta hills with kiln-shaped mounds; 3 the rope bridge over
the dry riverbed; 4 a square stone martial-arts yard with wooden training posts; 5 terraced fields; 6 a small
stone temple; 7 a court of stone guardian statues; 8 a grand golden monastery with a giant seated stone guardian.
[LEAVE OUT] = sparkles, dust swirls
```

## Sửa nhanh

| Lỗi | Gửi |
|---|---|
| Ra kiểu bản đồ chiến thuật 3D, quá vụn | `Too detailed and too realistic. Redraw it as a hand-drawn notebook map like the attached world.png: pencil hatching on cream paper, wobbly ink outlines, every tree and rock a chunky doodle with a clear silhouette. Keep the same road and layout.` |
| Bản đồ đảo hệ thưa, thiếu địa hình | `Same layout and road, but richer: more raised plateaus with short cliff faces on both sides of the road, denser clusters of trees framing the road, more small props along the road edges.` |
| Đường lệch bố cục, hẹp lại, có vật trên đường | `Keep the road exactly on the path and width of the attached layout sketch, with the middle widening and the top arena; nothing on the road or in the arena.` |
| Còn vẽ phần động | `Same image, but remove the [smoke / flames / gears / bell / whirlpool / wave crests]; leave their spots as described.` |
| Đảo rời (W): vật quan trọng nằm sát bờ | `Same island, but move the landmark and the important objects into the middle 70 % of the island; the outer ring is plain ground.` |
| Đảo rời (W): nền không trong suốt | `Same island, but fully transparent background outside the foam line.` (Không được thì xin nền trắng phẳng, Claude tách nền.) |
| Biển lặp có đường nối | `Same texture, but seamless: hatching strokes continue across all four edges, no wave mark touching an edge.` (Script cũng tự trộn mép.) |
| Có chữ | `Same image without any text, letters, numbers or signs with writing.` |
| Có sinh vật hoặc người | `Same image without any creatures or people.` |

## Duyệt trước khi lưu

- **Nét:** đặt cạnh `refs/world.png` thấy cùng một người vẽ (viền mực nâu sẫm hơi rung, gạch bút chì, giấy kem).
- **Đảo rời (W):** nền trong suốt; landmark nằm trong 70% giữa; cùng hướng sáng, cùng độ đậm nét với các đảo đã có.
- **Bản đồ đảo hệ (Z):**
  - đặt chồng lên `L_zone_*.png` thì đường trùng dáng và bề rộng;
  - mặt đường, bãi giữa, bãi đỉnh để trống;
  - 8 địa danh theo đúng thứ tự, đứng sát đường;
  - hai bên đường có cao nguyên, vách và cây dày;
  - không phần động.
- **Không:** chữ, sinh vật, người.

## Sau khi có ảnh

- **Đảo rời:** lưu vào `pieces/`, chạy `compose_islands.py`, rồi menu Unity `Đảo sảnh: ghép ảnh, kéo, mây viền`; chụp sảnh soi.
- **Sheet phần động:** đã ở `inbox/`; chạy menu `PokiClash/Nhập ảnh ArtGen`.
- **Bản đồ đảo hệ:** lưu vào `zones/` (không để trong `inbox/`, vì menu nhập sẽ chép nguyên khổ 2:3).
- **Báo Claude để:**
  - cắt dải 9:16 cho bản đồ đảo hệ;
  - đặt lại 8 ải trên đường (sửa dữ liệu ở bản web, xuất, chép sang Unity);
  - dựng lớp phần động;
  - chụp 5 đảo soi.
