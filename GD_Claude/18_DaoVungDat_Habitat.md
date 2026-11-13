# Đảo vùng đất: kéo hai chiều, mỗi tướng một habitat

Viết 2026-11-13. Kế hoạch, chưa làm. Chưa gen ảnh được, nên bước đầu làm bằng hình tạm.

## Người dùng đã chốt (2026-11-13)

| Câu hỏi | Chốt |
|---|---|
| Kiểu bản đồ đảo | Bỏ cuộn dọc. Mỗi đảo là **một vùng đất kéo được hai chiều** như sảnh chính của Clash of Critters |
| Habitat | Mỗi ải tướng (10 mỗi đảo) có **một habitat 3x3 hoặc 4x4** hợp với tướng đó, **đặt cố định**, người chơi không xếp |
| Ải chưa mở | **Không che**: habitat và tướng hiện đủ màu, chỉ khoá ở bảng tên và nút Xuất trận |
| Tác dụng | **Chỉ để nhìn**. Thiết kế sao cho sau này dễ thêm boss mới vào đảo |
| Cách làm | Làm thử đảo Thủy trước, từ từ. Viết kế hoạch trước, gen ảnh sau |

## Hiện trạng

- [ZoneScene.cs](../Assets/01%20Script/App/Scenes/ZoneScene.cs): bản đồ dài một ảnh liền (3 ảnh GPT ghép dọc, `ArtGen/Islands/build_zone70.py`), rộng 1,27 màn, cuộn dọc. Ải tướng là bệ (`ZoneNode`) đặt theo `stops` trên đường mòn `path`; ải xen giữa là chấm (`ZonePip`).
- **Địa danh của từng chặng vẽ chết trong ảnh nền.** Muốn thêm boss là phải gen lại cả đoạn bản đồ. Đây là chỗ phải đổi đầu tiên.
- Đã có sẵn để dùng lại:
  - `HubPan`: kéo, dây chun, trôi theo đà, phân biệt chạm với kéo;
  - `IslandAnim`: phần động đọc từ `island_anim.json` (gợn nước, lá rơi, khói, xoáy…);
  - `ZonePip`, `StagePrep`, nhãn AFK, rương mốc;
  - trang trại (`FarmScene`) là mẫu cảnh thật kéo được, có thú cử động bằng code.

## Hình dung

```
          mây viền
   ┌──────────────────────────────┐
   │   (ô dự trữ)      ◆ Xoáy Nước │   ◆ habitat 4x4 (boss ải 70)
   │        ◇ Đền Rùa   ┊          │   ◇ habitat 3x3
   │   ◇ Hồ Gương ┄┄┄┄┄┄┘          │   ┄ đường mòn, chấm là ải xen giữa
   │       ┊          ◇ Rạn Ngọc   │
   │   ◇ Thác Bạc ┄┄┄┄┄┄┘  (ô dự trữ)
   │       ┊    ◇ Hải Đăng          │
   │  ◇ Làng Vỏ Ốc ┄┄┄┘            │
   │       ┊   ◇ Cầu Gỗ Rêu         │
   │ ◇ Vũng San Hô ┄┘               │
   │      ◇ Bãi Vỏ Sò  (bến vào)    │
   └──────────────────────────────┘
          biển
```

- Vùng đất khoảng **1,6–2 màn ngang × 2–2,5 màn dọc** (khung 1080 × 1920), chốt khi dựng bố cục. Lớn hơn một màn theo cả hai chiều để có cảm giác "đi khám phá", nhưng không rộng tới mức lạc.
- Nhìn chéo từ trên xuống. Có một **lưới thoi ngầm** (ô 2:1, khoảng 140 × 70 px khung 1080) chỉ để xếp chỗ, **không vẽ ô ra**. Habitat 3x3 rộng khoảng 420 px (40% bề ngang màn), 4x4 khoảng 560 px.
- Đường mòn đi từ bến ở đáy lên habitat boss. Ải xen giữa là chấm dọc đường như bây giờ, rương mốc vẫn mỗi 10 ải.
- **Tách nền và habitat**:
  - nền chỉ có đất, cỏ, nước, đường mòn và trang trí nhỏ, không có địa danh;
  - mọi địa danh nằm trong habitat (ảnh rời).
  - Thêm boss là đặt thêm habitat lên **ô dự trữ** và nối đường, không đụng tới ảnh nền.

### Mở rộng thêm boss

- Mỗi đảo chừa sẵn **3–4 ô dự trữ** cỡ 4x4 trên nền: đất trống có bụi cây, đá, không ghi gì.
- Thêm boss gồm: một mục `habitats` trong `zones.json`, ải trong `stages.json`, ảnh habitat, một nhánh đường mòn. Đường mòn vẽ bằng code (giống đường mòn kiểu web cũ) hoặc là ảnh nhánh rời. Vì vậy ảnh nền vẽ **không có đường**, hoặc chỉ có trục chính.
- Hết ô dự trữ thì nới vành mây ra, thêm một khối nền ghép vào rìa (nền chia khối ngay từ đầu, xem mục Ảnh).

## Habitat

### Thành phần

1. **Chân đế** thoi 3x3 hoặc 4x4, đất theo hệ, mép tự nhiên hòa vào nền (không phải viên gạch vuông vức).
2. **Cảnh**: đá, cây, nước, công trình. Vẽ theo nét tay của game (`ArtGen/Islands/refs/world_style.png`).
3. **Chỗ tướng đứng**: một điểm định sẵn trong habitat. Tướng là rig `.atomik` nếu có, chưa có thì dùng sticker cử động bằng code như `FarmPet`.
4. **Lớp động** tách riêng: nước, lá, cờ, đèn… đọc bằng `IslandAnim` (mỗi habitat một khoá trong `island_anim.json`).
5. **Bảng tên**: huy hiệu số ải, tên tướng, cấp. Dùng lại phần bảng tên của `ZoneNode`.

### Trạng thái

| Trạng thái | Hiển thị |
|---|---|
| Chưa mở | Habitat và tướng đủ màu, tướng ở thế canh giữ. Huy hiệu có khoá. Chạm vẫn mở hộp chuẩn bị, nút Xuất trận khoá |
| Đang đánh | Vầng sáng nhịp dưới chân đế, mũi tên nhún trên đầu tướng. Camera lướt tới đây khi vào đảo |
| Đã qua | Dấu qua trên huy hiệu, cắm một lá cờ nhỏ trong habitat. Tướng đổi sang idle thả lỏng hơn (đề xuất, cần duyệt) |

### Cỡ và ý tưởng cho đảo Thủy (đề xuất, cần duyệt)

| Ải | Habitat | Tướng | Cỡ | Ý tưởng động |
|---|---|---|---|---|
| 1 | Bãi Vỏ Sò | Giọt Sương | 3x3 | sóng liếm bờ, vỏ sò mở khép; tướng nhảy qua vũng nước |
| 5 | Vũng San Hô | Tiểu Y | 3x3 | san hô đung đưa, bọt nổi; tướng cầm đinh ba khuấy nước |
| 10 | Cầu Gỗ Rêu | Cánh Cụt | 3x3 | suối chảy dưới cầu; tướng trượt bụng trên cầu rồi đứng dậy |
| 15 | Làng Vỏ Ốc | Mi Nhi | 3x3 | khói bếp, rèm cửa bay; tướng gảy đàn, nốt nhạc bay lên |
| 20 | Ngọn Hải Đăng | Ma Kết | 3x3 | đèn quét vòng, mòng biển bay qua |
| 30 | Thác Bạc | Vây Lam | 3x3 | thác đổ, bụi nước lấp lánh; tướng nhảy vọt khỏi hồ |
| 40 | Rạn Ngọc Trai | Kuba | 3x3 | trai mở ra lộ ngọc, lấp lánh |
| 50 | Hồ Gương | Thương Lam | 4x4 | mặt hồ in bóng, gợn khi tướng chạm nước |
| 60 | Đền Rùa Cổ | Huyền Vũ | 4x4 | cột đền phủ rêu, đèn đá lập lòe; tướng rụt cổ rồi thò ra |
| 70 | Xoáy Nước Đinh Ba | Lam Quân | 4x4 (có thể 5x5) | xoáy nước xoay, đinh ba nhấp nhô (đã có trong `IslandAnim`) |

Mini boss mạnh (ải 50, 60) và boss dùng 4x4 để nhìn là biết càng vào sâu càng to.

## Animation

Ba lớp, mỗi lớp một nhịp để không đơn điệu:

1. **Nền**: sóng ngoài biển, gợn suối, lá bay. Dùng lại `IslandAnim`.
2. **Habitat**: mỗi cái 2–4 món động riêng (bảng trên).
3. **Tướng**:
   - idle thở liên tục;
   - **trò riêng** cứ 6–12 giây một lần, lệch nhịp giữa các habitat để không cùng lúc;
   - chạm vào tướng thì phản ứng ngắn (nhún, gầm, một nhịp của chiêu) rồi mới mở hộp chuẩn bị, hoặc chạm lần hai mới mở (cần chốt);
   - ải vừa qua: màn cắm cờ ngắn khi quay về bản đồ.

Hạt (bọt, lấp lánh, nốt nhạc) làm theo chuẩn hạt chồng lớp (skill `pokiclash-hero-fx`, `skill-petclash`), không dùng hình tĩnh lật khung.

**Máy yếu**: chỉ chạy rig và hạt của habitat nằm trong khung nhìn cộng một lề. Ngoài khung thì dừng hẳn, lúc kéo tới mới bật lại. Mỗi lúc thấy được khoảng 3–4 habitat.

## Camera và thao tác

- Kéo hai chiều bằng `HubPan`, giới hạn theo cỡ vùng đất, ra rìa là vành mây và dây chun.
- Vào đảo: camera đặt sẵn ở ải đang đánh, rồi lướt nhẹ để người chơi thấy là kéo được.
- Nút **"Ải tiếp"** ở khung dưới: lướt camera về ải đang đánh.
- Chạm chấm ải xen giữa vẫn mở hộp chuẩn bị như bây giờ.
- Phóng to thu nhỏ bằng hai ngón: bản đầu chưa làm.
- Khung thông tin trên và khung ải kế dưới giữ như cũ.

## Dữ liệu (`Assets/02 Data/Json/zones.json`)

Thêm cho mỗi đảo (đảo nào chưa có thì màn đảo chạy kiểu cũ):

```json
"land": {
  "art": "land_thuy",            // ảnh nền (hoặc danh sách khối nền)
  "size": [2160, 4320],          // px khung 1080
  "cell": [140, 70],             // ô thoi
  "origin": [1080, 300],         // gốc lưới trên ảnh nền
  "path": [[x, y], ...],         // tâm đường mòn, tỉ lệ 0..1 của ảnh nền
  "reserve": [[gx, gy, 4], ...]  // ô dự trữ
},
"habitats": [
  { "stage": 1, "cell": [6, 30], "size": 3, "art": "hab_thuy_01",
    "stand": [0.5, 0.55], "plate": 1, "anim": "hab_thuy_01" }
]
```

- `GameData` kiểm: mỗi ải tướng có đúng một habitat; habitat không chồng nhau và không chồng ô dự trữ; nằm trong vùng đất.
- Chỉ đổi phần hiển thị, không đổi luật. Golden `zones.json` không có `path`, `stops` nên không phải sửa golden. Vẫn chạy test Unity sau khi nhập dữ liệu.
- `path`, `stops`, `plates` cũ giữ lại cho tới khi cả 5 đảo chuyển xong.

## Code

| Việc | Chỗ |
|---|---|
| Kiểu đảo mới: dựng nền, habitat, đường, chấm, camera | `ZoneScene` thêm nhánh `RenderLand` (đảo có `land`); nhánh cũ giữ nguyên |
| Habitat: chân đế, cảnh, tướng, bảng tên, trạng thái, chạm | `ZoneHabitat.cs` mới, prefab `Items/Habitat`, dựng bằng menu Editor như `BeAi` |
| Kéo hai chiều | `HubPan` nhận giới hạn theo cỡ nội dung; thêm hàm lướt tới một điểm |
| Thứ tự lớp | habitat xếp theo y chân đế (dưới đè trên); tướng, bảng tên trong habitat |
| Bật tắt theo khung nhìn | `ZoneHabitat` tự dừng rig, hạt, `IslandAnim` khi ra ngoài khung |
| Tướng cử động | rig `.atomik` qua `AtomikPlayer` nếu có; chưa có thì cử động sticker như `FarmPet` |
| Kiểm dữ liệu | `GameData` (mục Dữ liệu) |

Không làm bản web (`Web/`).

## Ảnh (khi gen được)

Gói mới `ArtGen/Islands/build_land.py`, sinh `ArtGen/Islands/gui_gpt/land_thuy/`, theo luật file prompt trong `CLAUDE.md` (mỗi lượt một file, ảnh mẫu đường dẫn đầy đủ, mục SAVE, `HUONG_DAN.md`).

1. **Ảnh bố cục** do script vẽ: lưới thoi, chỗ từng habitat, ô dự trữ, đường mòn, nước. Dùng làm ảnh mẫu cho mọi lượt sau.
2. **Nền**: chia khối dọc (như 3 đoạn ghép của bản đồ dài bây giờ), mỗi khối một lượt gen, có dải chồng để ghép liền. Không vẽ địa danh. Chỗ habitat chỉ là đất phẳng.
3. **Habitat**: mỗi cái một lượt. Ảnh mẫu là nét vẽ của game, khung thoi đúng cỡ, hình tướng (để cảnh hợp cỡ và hợp tính cách tướng), ô đánh dấu chỗ tướng đứng. Không vẽ tướng vào habitat. Nền trong suốt.
4. **Món động**: tách riêng thành ảnh nhỏ theo kiểu `Islands/Anim/anim_<tên>` đang có.

Làm và duyệt **từng habitat một**, như làm tướng. Duyệt xong cái trước mới dựng file prompt cái sau.

## Các bước

| Mốc | Việc | Cần ảnh gen? |
|---|---|---|
| M0 | Script vẽ ảnh bố cục đảo Thủy (lưới, 10 habitat, ô dự trữ, đường); người dùng duyệt chỗ đặt | Không |
| M1 | Code chạy trên Thủy bằng **hình tạm**: nền màu và đường vẽ bằng code, chân đế thoi vẽ bằng code, sticker tướng hiện có. Thử kéo, camera, bảng tên, chạm, máy yếu | Không |
| M2 | Gen nền đảo Thủy và **một habitat mẫu** (đề xuất Bãi Vỏ Sò, ải 1) để chốt nét vẽ, cỡ, cách hòa vào nền | Có |
| M3 | 9 habitat còn lại của Thủy, từng cái; lớp động; trò idle riêng của từng tướng | Có |
| M4 | 4 đảo còn lại, mỗi đảo làm lại M0 → M3 | Có |
| Sau | Thêm boss mới vào ô dự trữ | Có |

M0 và M1 làm được ngay, không cần gen ảnh.

## Câu cần chốt

1. Cỡ vùng đất: khoảng 1,6–2 × 2–2,5 màn có hợp không, hay muốn nhỏ hơn để thấy gần hết đảo?
2. Lưới thoi nhìn chéo (kiểu xây nhà) hay lưới vuông nhìn thẳng từ trên xuống? Đề xuất thoi.
3. Ải đã qua: cắm cờ và đổi idle như đề xuất, hay để y nguyên?
4. Chạm tướng: phản ứng rồi mở hộp chuẩn bị luôn, hay chạm lần hai mới mở?
5. Bảng cỡ habitat và ý tưởng động của đảo Thủy ở trên có cần đổi gì không?
