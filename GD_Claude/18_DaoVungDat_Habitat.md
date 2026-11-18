# Đảo vùng đất: kéo hai chiều, mỗi tướng một habitat

Viết 2026-11-13. **Rà lại 2026-11-18** theo bản đục Clash of Critters (sảnh nhà, bản đồ chương, bản đồ thế giới) vì người dùng dặn làm đảo Thủy mới "giống Clash of Critters". Mới là kế hoạch, chưa làm dòng code nào.

## Người dùng đã chốt

| Ngày | Câu hỏi | Chốt |
|---|---|---|
| 2026-11-13 | Kiểu bản đồ đảo | Bỏ cuộn dọc. Mỗi đảo là **một vùng đất kéo được hai chiều** như sảnh chính của Clash of Critters |
| 2026-11-13 | Habitat | Mỗi ải tướng (10 mỗi đảo) có **một habitat 3x3 hoặc 4x4** hợp với tướng đó, **đặt cố định**, người chơi không xếp |
| 2026-11-13 | Ải chưa mở | **Không che**: habitat và tướng hiện đủ màu, chỉ khoá ở bảng tên và nút Xuất trận |
| 2026-11-13 | Tác dụng | **Chỉ để nhìn**. Thiết kế sao cho sau này dễ thêm boss mới vào đảo |
| 2026-11-13 | Cách làm | Làm thử đảo Thủy trước, từ từ. Viết kế hoạch trước, gen ảnh sau |
| 2026-11-18 | Mẫu | Làm **giống Clash of Critters** |
| 2026-11-18 | Dáng đảo | **Một đảo rộng ngang**, cảm hứng Dragon City (habitat) và Kingdom Rush 5 (bản đồ vùng) |
| 2026-11-18 | Vùng | **Mỗi boss làm chủ một phần đảo có môi trường riêng** |
| 2026-11-18 | Đường (sửa cùng ngày) | **Chỉ một đường**, đi vòng quanh đảo qua từng boss, không đi thẳng lên. Ải mở theo thứ tự như luật hiện tại (bỏ ý mạng đường) |
| 2026-11-18 | Animation | Mỗi habitat có hiệu ứng động riêng; tướng chạy idle, thỉnh thoảng đánh (attack) cho đẹp |
| 2026-11-18 | Bố cục (chốt) | Giữ **đảo 10 vùng** (nhiều môi trường, chi tiết hơn); **một đường lượn tự nhiên, đi thẳng vào môi trường từng boss**, không lách qua; **habitat bệ tròn viền đá**. Concept chốt `concept_F_sua_duong_2.png` |
| 2026-11-18 | Sóng | Sóng đập bờ động. Bản thử shader `song_thu.html` |

## Rà lại 2026-11-18: những chỗ đã cũ

| Mục | Plan 2026-11-13 | Nay |
|---|---|---|
| Tướng đảo Thủy | Bảng habitat dùng lô cũ (Giọt Sương … Lam Quân) | Lô 2026-11-11: Tí Tách, Thạch Giải, Hải Đăng, Sò Ngoạm, Bát Trảo, Giông Bão, Thôn Kình, Uyên Xà, Hàn Ngạc, Hải Long. **Cả 10 đã có rig `.atomik`**, nên không cần sticker tạm |
| Gen ảnh | "Chưa gen ảnh được" | Gen được qua Magnific (GPT 2.6, 1k high 95 credit, trần 100 mỗi ảnh) hoặc gói file prompt cho GPT |
| Nền đảo | GPT vẽ vài khối nền lớn, ghép dọc | **Ghép từ bộ mảnh** như sảnh của Critters (mục "Critters dựng ra sao") |
| Nước | Vẽ trong ảnh nền, gợn bằng `IslandAnim` | **Shader nước** trên mesh viền bờ, như Critters |
| Câu 2 cũ (lưới thoi hay vuông) | Đề xuất thoi | Critters dùng lưới thoi (`IsometricGridRenderer`, `IsoGridMap`), nên chốt **thoi** theo lời dặn "giống Critters" |
| Code | | Chưa có gì (`RenderLand`, `ZoneHabitat` chưa tồn tại), M0 và M1 chưa làm |

## Critters dựng ra sao (bản đục 0.51.1, `D:\Ripper\ClashOfCritters`)

Chỉ học cách dựng, không chép hình. Không gửi ảnh của họ cho GPT, prompt không nhắc tên game.

### Sảnh nhà (homestead): mẫu cho vùng đất

| Phần | Họ làm | Asset |
|---|---|---|
| Nền | **Không phải một ảnh.** Ghép từ mảng cỏ lớn mép lượn (rộng 1024 px), mảng cát bờ biển, ao, hồ dưới thác | `bgdecoration_connectinggrass_01–03`, `prospect_sand_01–06`, `pond`, `waterfall_pool` |
| Địa hình cao | Atlas cao nguyên nhiều cỡ: mặt trên cỏ, vách đất nâu đỏ có vân, có bậc thang, thác nhỏ | `bgdecoration_hills_atlas` (2048) |
| Cây | Khoảng 10 kiểu (thông, cọ, cây tán tròn, cột đá phủ cỏ), đặt rời từng cây | `bgdecoration_trees_atlas` |
| Đồ lặt vặt dưới đất | Cỏ con, hoa, sỏi gói chung một texture. Code rải theo dữ liệu, nên hàng trăm món chỉ tốn một lần vẽ | `grounditem_packedtex_0`, `HomesteadGroundData`, `HomesteadGroundItemDrawer` |
| Ngoài rìa | Dải phong cảnh xa (thung lũng có sông), núi xa, mây, đá, sao biển, thuyền phao | `bgdecoration_background_01–02`, `mountain_07–09`, `cloud_06`, `rubberboat`, `starfish` |
| Công trình, trang trí | Ảnh nền cộng phần động Spine (suối nước nóng: vòng gợn, hơi nước, tượng gấu; nhà tập). Có cả **trang trí theo trận boss chương** (phế tích) | `homestead_decoration_hotspring_159`, `homestead_gym_341`, `decoration_bossbattle1geruins_337`, `bossbattle6gefeixu_335` |
| Lưới | Lưới thoi, chỉ hiện lúc xếp đặt. Thú đi lại trên lưới bằng tìm đường | `IsometricGridRenderer`, `HomesteadGridController`, `ColorGridRendererController`, `IsoGridMap`, `IsoGridPahFinder` |
| Mở đất | Hiệu ứng mở rộng 3x3, đặt 1x1; trang trí "vùng chưa mở" | `pbfx_camp_expand_3x3`, `pbfx_camp_build_1x1`, `decoration_cannotunlockarea4_303` |
| Camera | Cinemachine trực giao, có khung giới hạn; chạm công trình thì lướt tới | `pbsc_homestead_camera` (`camera_focus_rect`) |

### Bản đồ chương: mẫu cho đường ải

- Mỗi chương một ảnh dọc 1334 × 1875: đường cát rộng lượn chữ S, cao nguyên hai bên, mây là lớp rời. Phần này mình đã học từ trước (`ArtGen/Islands/PROMPTS.md`, mục "Học từ bản đồ Clash of Critters").
- Nút ải là sprite rời, hai cỡ (boss lớn, ải thường nhỏ), hai trạng thái: xám là chưa qua, xanh là đã qua (`worldmap_levelnode_large/small` và bản `_clear`).
- **Xe của người chơi chạy trên đường** từ nút này sang nút kế, có tiếng xe, tông zombie đứng trên đường (`world_car_01/02` vẽ 5 góc nhìn, `sfx_worldmap_car_start/loop/end/ram_zombie`, `pbfx_map_zombiehit`).
- Qua ải: nút lật (`pbfx_map_stage_flip`), sao và tiền bay ra (`pbfx_map_stagebonus_stars/credits`).
- Thanh thưởng tiến độ ở trên, thưởng boss hai bên (`group_topreward`, `bossreawrd_left/right_cell`).

### Bản đồ thế giới nhuộm màu (mapdye)

- 120 chương là 120 mảnh đất trên một biển chung, có đảo, thuyền, mây và chim bay qua (`pbvx_mapdye_cloudnbird`).
- Mảnh chưa qua tô xám (`imgplotgray`), qua rồi mới tô màu (`imgplot`), có clip đổi màu (`anui_battle_mapdye_base_change`, `clear_inout`).
- Mỗi mảnh có các trạng thái khoá, đang đánh (hai thanh kiếm), xong; kèm sao, cấp, mặt người chơi.
- Nước là mesh viền theo bờ (337 đỉnh) cộng shader. Shader có màu nền, màu sóng, màu mép, màu bọt, và texture nhiễu trôi (`mtui_water_worldmap`, `txui_mapdye_water_noise_1–3`).
- Chuyển cảnh bằng mây (`pbui_mapdye_cloud_loading`).

## Áp vào đảo Thủy

| # | Critters | Mình |
|---|---|---|
| 1 | Sảnh ghép từ mảnh | **Vùng đất ghép mảnh, không vẽ liền.** Gồm nền đa giác (đất, cát, nước nông) do code vẽ, cao nguyên, cây, đồ kể chuyện, đồ lặt vặt; tất cả đặt theo dữ liệu `land`. Thêm boss chỉ cần đặt thêm. Mỗi ảnh gen nhỏ, dưới 100 credit. Cây đung đưa riêng từng cây. Cả 5 đảo dùng chung một khung code, chỉ thay bộ mảnh theo hệ |
| 2 | Nước bằng shader | Shader nước **nét vẽ tay** (`PokiClash/InkWater`, shader mới) trên mesh viền bờ: nền xanh tô phẳng, gạch chì trôi chậm, viền bọt quanh bờ và quanh chân habitat. Không bóng loáng, không điểm sáng (luật UI). Đảo Thủy nhiều nước nhất nên làm shader này trước |
| 3 | Công trình có phần động Spine | Habitat = ảnh chân đế và cảnh, phần động tách riêng (`IslandAnim` hoặc rig `.atomik` nhỏ), tướng đứng trên điểm định sẵn. Habitat boss to như "phế tích trận boss" |
| 4 | Đồ lặt vặt vẽ một lần | Một texture gói (cỏ con, hoa, sỏi, vỏ sò, sao biển), rải bằng code theo hạt giống cố định, gộp thành một mesh |
| 5 | Phong cảnh xa, mây, chim | Ngoài rìa là biển xa có bóng 4 đảo kia, thuyền, mây và chim bay qua, thay vành mây kín |
| 6 | Lưới thoi chỉ hiện khi xếp | Lưới thoi ngầm, không bao giờ vẽ (habitat cố định) |
| 7 | Chạm thì camera lướt tới | Chạm habitat: camera lướt cho habitat vào giữa, rồi mở hộp chuẩn bị |
| 8 | Xe chạy trên đường | **Tướng đồng hành** của người chơi đứng ở ải đang đánh, thắng thì chạy theo đường tới ải kế. Rig chưa có clip đi, nên làm nhảy cóc bằng code hoặc thêm clip đi (câu 7) |
| 9 | Zombie trên đường bị tông | Lính của ải xen giữa đứng trên chấm; qua ải thì lính ngã, chấm lật sang dấu đã qua |
| 10 | Thanh thưởng tiến độ | Rương mốc (mỗi 10 ải) hiện thành thanh tiến độ ở khung trên |
| 11 | Nhuộm màu chương | **Cần chốt (câu 6):** nền đoạn chưa qua để nét chì chưa tô (giấy kem, nét nâu), qua rồi màu loang dần theo đường. Habitat và tướng vẫn đủ màu như đã chốt. Hợp với kiểu sổ tay vẽ tay của game |

## Hướng 2026-11-18: đảo rộng chia vùng

**Concept chốt:** `ArtGen/Islands/land_thuy/concept/concept_F_sua_duong_2.png`. Đây là bản `concept_E_vung_mot_duong_1.png` được GPT sửa riêng phần đường. Bố cục: `refs/layout_vung2.png`, sinh bằng `make_layout_vung2.py`. Các bản đã bỏ: mạng đường (`concept_C_*`), xoắn ốc (`concept_D_*`).

So với bản mạng đường, 4 vùng giữ chỗ (1, 5, 30, 70); 6 vùng còn lại đổi chỗ để một đường đi đúng thứ tự mà không cắt chéo qua chính nó.

- Một đảo rộng khoảng 3 màn ngang × 1,7 màn dọc, kéo hai chiều.
- **10 vùng cảnh**, mỗi vùng do một tướng ải làm chủ, habitat nằm giữa vùng. Ải xen giữa của vùng là cờ nhỏ quanh habitat: ải 2–4 thuộc vùng ải 5, ải 6–9 thuộc vùng ải 10, …, ải 61–69 thuộc vùng ải 70.
- **Một đường lượn tự nhiên, đi thẳng vào giữa vùng của từng boss** tới trước habitat rồi mới đi tiếp; không đi vòng ngoài vùng, không rẽ nhánh. Lộ trình:
  - bến → bãi biển → đầm → hải đăng → cầu ván → rạn san hô → tàu đắm;
  - từ tàu đắm xuống rừng theo thác, qua cầu → tháp mưa;
  - từ tháp mưa xuống bậc đá → vịnh kình → vực hang → vùng băng → đền rồng. Đường kết thúc ở đền.
- Càng đi càng khắc nghiệt: bờ biển nắng ở đầu, núi băng và đền rồng ở cuối.
- Ải mở theo thứ tự như luật hiện tại; chỉ đổi phần hiển thị. Code vẽ đường theo `path`, không vẽ đường trong ảnh nền.
- Mỗi vùng có môi trường riêng nên bộ mảnh chia theo vùng (cây, đá, nền), không còn một bộ chung cho cả đảo.

| Vùng | Ải | Cấp địch ải tướng | Môi trường | Habitat |
|---|---|---|---|---|
| Bãi Biển Nắng (bến vào) | 1 | 1 | cát vàng, cọ, vũng triều | võ đài đá, cọc tập |
| Đầm Lá Súng | 2–5 | 18 | lau sậy, ao lá súng, gỗ rêu | ao lá súng |
| Mũi Đá Hải Đăng | 6–10 | 35 | ghềnh xám, vách biển, mòng biển | hải đăng |
| Rạn San Hô | 11–15 | 51 | nước nông xanh ngọc, san hô, cồn cát | rạn sò khổng lồ |
| Vịnh Tàu Đắm | 16–20 | 66 | vịnh tối, cột buồm gãy, thùng gỗ | xác tàu nửa chìm |
| Cao Nguyên Giông (giữa đảo) | 21–30 | 94 | đồi xanh sẫm, cột đá, mây mưa | tháp gọi mưa |
| Vịnh Kình | 31–40 | 120 | vách xanh xám, xương cá voi | vòm xương |
| Vực Hang | 41–50 | 146 | đá tím than, khe sâu, nấm phát sáng | miệng hang biển |
| Vùng Băng | 51–60 | 171 | đồng tuyết, vách băng, hồ đóng băng | đầm băng |
| Đền Rồng (bờ bắc, giữa) | 61–70 | 195 | đền đổ nát trên vách, vịnh xoáy nước, thác | bậc đền |

Vị trí trên đảo (concept F): bãi biển (đáy giữa), đầm (tây nam), mũi hải đăng (bờ tây), rạn san hô (góc tây bắc), vịnh tàu đắm (bờ bắc), cao nguyên giông (giữa đảo), vịnh kình (đông nam), vực hang (bờ đông), vùng băng (đông bắc), đền rồng (bờ bắc, giữa).

## Hình dung cũ: một đường (thay bằng bản đồ vùng từ 2026-11-18)

```
     biển xa: bóng 4 đảo kia, thuyền, mây, chim
   ┌──────────────────────────────────┐
   │  (ô dự trữ)        ◆ Xoáy Đền Rồng │   ◆ habitat 4x4 (boss ải 70)
   │       ◆ Đầm Băng    ┊             │   ◇ habitat 3x3
   │  ◆ Hang Vực ┄┄┄┄┄┄┄┄┘             │   ┄ đường mòn, chấm là ải xen giữa
   │       ┊        ◇ Vịnh Xương Kình  │   ▲ cao nguyên, ♣ cây (mảnh rời)
   │  ◇ Đầm Mưa ┄┄┄┄┄┄┘   (ô dự trữ)   │   ≈ nước (shader)
   │       ┊    ◇ Xác Tàu Đắm          │
   │  ◇ Rạn Sò Khổng Lồ ┄┘   ≈≈≈       │
   │       ┊   ◇ Ngọn Hải Đăng          │
   │  ◇ Bãi Đá Cua ┄┘                  │
   │      ◇ Võ Đài Mưa  (bến vào)       │
   └──────────────────────────────────┘
          biển
```

- Vùng đất khoảng **1,6–2 màn ngang × 2–2,5 màn dọc** (khung 1080 × 1920), chốt khi dựng bố cục.
- Nhìn chéo từ trên xuống. **Lưới thoi ngầm** ô 2:1, khoảng 140 × 70 px khung 1080, chỉ để xếp chỗ. Habitat 3x3 rộng khoảng 420 px (40% bề ngang màn), 4x4 khoảng 560 px.
- Đường mòn đi từ bến ở đáy lên habitat boss. Ải xen giữa là chấm dọc đường, rương mốc vẫn mỗi 10 ải.
- Nền không có địa danh, mọi địa danh nằm trong habitat. Thêm boss là đặt habitat lên **ô dự trữ** rồi nối đường.

### Mở rộng thêm boss

- Mỗi đảo chừa sẵn **3–4 ô dự trữ** cỡ 4x4: đất trống có bụi cây, đá (mảnh rời, gỡ được).
- Thêm boss gồm: một mục `habitats` trong `zones.json`, ải trong `stages.json`, ảnh habitat, một nhánh đường. Đường do code vẽ.
- Hết ô dự trữ thì nới rìa đất ra và đặt thêm mảnh. Nền ghép mảnh nên không phải gen lại gì.

## Habitat

### Thành phần

1. **Chân đế** thoi 3x3 hoặc 4x4, đất theo hệ, mép tự nhiên hòa vào nền.
2. **Cảnh**: đá, cây, nước, công trình, theo nét tay của game (`ArtGen/Islands/refs/world_style.png`). Nước trong habitat (vũng, hồ) để trống thành vùng trong suốt có mặt nạ, shader `InkWater` tô bên dưới để nước cả đảo cùng một kiểu.
3. **Chỗ tướng đứng**: một điểm định sẵn. Tướng là rig `.atomik` (cả 10 tướng Thủy đã có).
4. **Lớp động** tách riêng: đọc bằng `IslandAnim` (mỗi habitat một khoá trong `island_anim.json`); món lớn (vỏ sò mở khép, đèn quét) làm rig `.atomik` nhỏ.
5. **Bảng tên**: huy hiệu số ải, tên tướng, cấp. Dùng lại phần bảng tên của `ZoneNode`.

### Trạng thái

| Trạng thái | Hiển thị |
|---|---|
| Chưa mở | Habitat và tướng đủ màu, tướng ở thế canh giữ. Huy hiệu có khoá. Chạm vẫn mở hộp chuẩn bị, nút Xuất trận khoá |
| Đang đánh | Vầng sáng nhịp dưới chân đế, mũi tên nhún trên đầu tướng. Camera lướt tới đây khi vào đảo. Tướng đồng hành đứng ở chân đường trước habitat |
| Đã qua | Dấu qua trên huy hiệu, cắm một lá cờ nhỏ trong habitat. Tướng đổi sang idle thả lỏng hơn (đề xuất, cần duyệt) |

### Habitat đảo Thủy theo lô tướng mới (đề xuất, cần duyệt từng cái)

| Ải | Tướng (id) | Habitat | Cỡ | Ý tưởng động |
|---|---|---|---|---|
| 1 | Tí Tách, võ sĩ giọt mưa (`ti_tach`) | Võ Đài Mưa: sàn đá tròn cạnh vũng triều, cọc gỗ tập võ | 3x3 | mưa lất phất trên võ đài, vũng gợn; cọc gỗ lắc khi tướng đấm |
| 5 | Thạch Giải (`thach_giai`; hình trong game là ếch xanh lưỡi dài, dữ liệu còn ghi "cua ẩn sĩ") | Đầm Lá Súng: lá súng, đá rêu, cỏ lác | 3x3 | lá súng dập dềnh, chuồn chuồn; tướng thè lưỡi đớp |
| 10 | Hải Đăng, cá đèn lồng vực sâu (`ca_den`) | Ngọn Hải Đăng trên mỏm đá | 3x3 | đèn quét vòng, nhịp cùng đèn lồng trên đầu tướng; mòng biển bay qua |
| 15 | Sò Ngoạm, sò lưỡi dài (`ha_ba`) | Rạn Sò Khổng Lồ | 3x3 | sò lớn mở khép, ngọc lấp lánh; bọt nổi |
| 20 | Bát Trảo, bạch tuộc gọi bầy (`so_ngoc`) | Xác Tàu Đắm nửa chìm | 3x3 | thùng gỗ nhấp nhô, bạch tuộc con thò ra rồi lặn |
| 30 | Giông Bão (`giong_bao`; hình là pháp sư mũ trùm cầm gậy) | Tháp Gọi Mưa: tháp đá nhỏ, mây giông trên đỉnh | 3x3 | mưa rơi, chớp nhỏ; tướng giơ gậy gọi mưa |
| 40 | Thôn Kình, cá voi đuôi đá (`lien_kinh`) | Vịnh Xương Kình: vòm xương cá voi, đá hình đuôi | 3x3 | phun nước, sóng trong vịnh |
| 50 | Uyên Xà, rắn đèn vực sâu (`uyen_xa`) | Hang Vực: miệng hang biển tối, đèn sinh học | 4x4 | đốm sáng lập lòe, nước rút vào hang |
| 60 | Hàn Ngạc, cá sấu băng (`han_ngac`) | Đầm Băng: tảng băng trôi, nhũ băng | 4x4 | băng trôi dập dềnh, hơi lạnh bốc |
| 70 | Hải Long, rồng biển nhiều đầu (`hai_long`) | Xoáy Đền Rồng: đền đổ nát bên xoáy nước | 4x4 (có thể 5x5) | xoáy nước xoay (đã có trong `IslandAnim`), sương bay |

Mini boss mạnh (ải 50, 60) và boss dùng 4x4 để nhìn là biết càng vào sâu càng to.

**Concept 2026-11-18** (GPT 2.6 qua Magnific, chỉ để hình dung, không phải ảnh dùng trong game): `ArtGen/Islands/land_thuy/concept/`.
- `concept_A_toan_dao.png`: toàn đảo, đủ 10 habitat, ô dự trữ, bến.
- `concept_B_mot_man.png`: một màn điện thoại, có nhuộm màu (câu 6), tướng đồng hành, lính trên chấm, UI.
- Prompt nằm cạnh ảnh; ảnh mẫu do `make_refs.py` dựng.
- Nét mới thấy từ concept: mỗi habitat đặt trên một cao nguyên bậc thềm, vách gạch nâu, nên cao nguyên là món chính trong bộ mảnh.
- `concept_C_dao_vung_1.png`, `concept_C_dao_vung_2.png`: bản đồ vùng (hướng hiện tại). Bản 1: habitat là bệ tròn viền đá, kiểu chuồng thú. Bản 2: habitat là bệ vuông lát đá theo lưới thoi; nhiều thác, sông chia vùng hơn.

## Animation

Ba lớp, mỗi lớp một nhịp để không đơn điệu:

1. **Nền**: shader nước, cây đung đưa lệch pha từng cây, mây và chim bay qua, sóng vỗ bờ.
   - **Sóng đập bờ** (người dùng dặn 2026-11-18). Bản thử chạy được: `ArtGen/Islands/land_thuy/concept/song_thu.html`, sinh bằng `make_song.py <ảnh> <html>`.
   - Script dò biển (vùng xanh lơ nối ra mép ảnh) và tính khoảng cách tới bờ thành texture: kênh R là khoảng cách, kênh G là chỗ được vẽ sóng; mây và thuyền không bị dính bọt.
   - Shader vẽ vạch bọt trắng có viền mực chạy dần vào bờ, lệch theo nhiễu để không đều. Sát bờ có nước tràn lên, rút ra theo nhịp; lúc sóng lên cao nhất thì tung bụi nước. Đá ngoài biển có vòng sóng riêng.
   - Trong Unity viết lại thành `InkWater` với cùng texture khoảng cách, tính sẵn từ mặt nạ biển khi dựng đảo.
2. **Habitat** (người dùng dặn 2026-11-18): mỗi habitat có hiệu ứng động riêng, chạy liên tục, lệch pha nhau (bảng dưới).
3. **Tướng** (người dùng dặn 2026-11-18): rig `.atomik` thật của cả 10 tướng Thủy đều có sẵn clip `idle`, `attack`, `appear`, `hit`, nên không phải làm clip mới.
   - `idle` lặp liên tục.
   - **Thỉnh thoảng tung `attack`**: mỗi tướng sau 8–15 giây ngẫu nhiên đánh một lần rồi về `idle`. Hai habitat cùng trong khung nhìn không đánh cùng lúc (cách nhau ít nhất 2 giây).
   - Đánh trên đảo chỉ diễn thân. Tia, đạn của chiêu không bắn ra (`attack` là đòn thường), chỉ thêm một chùm hạt nhỏ theo hệ ở đúng sự kiện trúng của clip (bọt nước, tia nước), theo luật lớp VFX.
   - `appear`: khi ải vừa mở (qua ải trước) thì tướng của ải mới diễn ra sân một lần, camera lướt tới.
   - Chạm vào tướng: đánh ngay một lần (`attack`), câu 4 chốt mở hộp chuẩn bị lúc nào.
   - Ải vừa qua: tướng đổi sang idle thả lỏng (chậm hơn, không đánh nữa), cắm cờ, rồi tướng đồng hành chạy tới ải kế.

| Ải | Habitat | Hiệu ứng động của habitat |
|---|---|---|
| 1 | võ đài đá bãi biển | sóng liếm bờ, vũng triều gợn, cọc tập rung khi tướng đánh, lá cọ đung đưa |
| 5 | ao lá súng | lá súng dập dềnh, cỏ lác đung đưa, chuồn chuồn bay vòng, gợn tròn trên mặt ao |
| 10 | hải đăng | đèn quay quét vòng, mòng biển đậu bay, sóng đập ghềnh tung bọt |
| 15 | rạn sò | sò lớn mở khép chậm, ngọc lấp lánh (đổi màu, không quầng sáng), bọt nổi, san hô lắc |
| 20 | xác tàu đắm | thùng gỗ nhấp nhô, cờ rách bay, sóng vỗ thân tàu |
| 30 | tháp gọi mưa | mây mưa trôi tại chỗ, mưa rơi, chớp nhỏ nháy, vũng nước gợn, cột đá đổi màu hoa văn |
| 40 | vịnh xương kình | thác đổ, nước trong vịnh gợn, bọt quanh vòm xương |
| 50 | vực hang | nấm phát sáng nhấp nháy theo nhịp thở (đổi màu), giọt nước rơi, nước rút vào miệng hang |
| 60 | vùng băng | tảng băng trôi dập dềnh, tuyết rơi nhẹ, hơi lạnh bốc |
| 70 | đền rồng | hồ xoáy nước xoay (đã có trong `IslandAnim`), thác đổ xuống sườn núi, sương bay |

Cách làm: món nhỏ lặp (gợn, sóng, lá, mưa, tuyết) dùng `IslandAnim` và hạt chồng lớp; món lớn có khớp (sò mở khép, đèn hải đăng quay, xoáy nước) làm rig `.atomik` nhỏ; nước dùng shader `InkWater`. Mọi hiệu ứng theo luật tô phẳng: không quầng sáng, không bóng đổ, "phát sáng" thể hiện bằng đổi màu.

Hạt (bọt, mưa, lấp lánh) làm theo chuẩn hạt chồng lớp (skill `pokiclash-hero-fx`, `skill-petclash`), không dùng hình tĩnh lật khung.

**Máy yếu**: chỉ chạy rig và hạt của habitat nằm trong khung nhìn cộng một lề. Ngoài khung thì dừng hẳn. Mỗi lúc thấy khoảng 3–4 habitat.

## Camera và thao tác

- Kéo hai chiều bằng `HubPan`, giới hạn theo cỡ vùng đất, ra rìa là biển xa và dây chun.
- Vào đảo: camera đặt sẵn ở ải đang đánh, rồi lướt nhẹ để người chơi thấy là kéo được.
- Nút **"Ải tiếp"** ở khung dưới: lướt camera về ải đang đánh.
- Chạm habitat: lướt camera cho nó vào giữa rồi mở hộp chuẩn bị. Chạm chấm ải xen giữa vẫn mở hộp chuẩn bị như bây giờ.
- Phóng to thu nhỏ bằng hai ngón: bản đầu chưa làm.
- Khung thông tin trên (thêm thanh rương mốc) và khung ải kế dưới giữ như cũ.

## Dữ liệu (`Assets/02 Data/Json/zones.json`)

Thêm cho mỗi đảo (đảo nào chưa có thì màn đảo chạy kiểu cũ):

```json
"land": {
  "size": [2160, 4320],            // px khung 1080
  "cell": [140, 70],               // ô thoi
  "origin": [1080, 300],           // gốc lưới
  "ground": [                      // đa giác nền, code vẽ, dưới lên trên
    { "kind": "sand",  "poly": [[x, y], ...] },
    { "kind": "grass", "poly": [[x, y], ...] }
  ],
  "water": [ { "kind": "lagoon", "poly": [[x, y], ...] } ],   // mesh shader InkWater
  "pieces": [ { "art": "thuy_cliff_02", "at": [x, y], "flip": false, "sway": 0 } ],
  "scatter": { "set": "thuy_ground", "seed": 70, "density": 0.6 },
  "path": [[x, y], ...],           // tâm đường mòn
  "reserve": [[gx, gy, 4], ...]    // ô dự trữ
},
"habitats": [
  { "stage": 1, "cell": [6, 30], "size": 3, "art": "hab_thuy_01",
    "stand": [0.5, 0.55], "plate": 1, "anim": "hab_thuy_01" }
]
```

- `pieces` do script M0 sinh thô, sau đó chỉnh trong Editor bằng menu dựng (kéo thả rồi ghi lại JSON). Không đặt tay từng toạ độ trong JSON.
- `GameData` kiểm: mỗi ải tướng có đúng một habitat; habitat không chồng nhau và không chồng ô dự trữ; nằm trong vùng đất.
- Chỉ đổi phần hiển thị, không đổi luật. Golden `zones.json` không có `path`, `stops`, nên không phải sửa golden. Vẫn chạy test Unity sau khi nhập dữ liệu.
- `path`, `stops`, `plates` cũ giữ lại tới khi cả 5 đảo chuyển xong.

## Code

| Việc | Chỗ |
|---|---|
| Kiểu đảo mới: dựng nền, mảnh, nước, habitat, đường, chấm, camera | `ZoneScene` thêm nhánh `RenderLand` (đảo có `land`); nhánh cũ giữ nguyên |
| Nền đa giác: tô texture gạch chì lát, viền mực rung | `LandGround.cs` mới (mesh dựng từ `ground`) |
| Nước | shader `PokiClash/InkWater` mới, mesh từ `water` và từ mặt nạ nước của habitat |
| Đồ lặt vặt | `LandScatter.cs`: rải theo hạt giống, gộp một mesh |
| Mảnh rời (cây, đá, cao nguyên) | sắp theo y chân (dưới đè trên), cây đung đưa bằng shader đỉnh hoặc xoay nhẹ |
| Habitat: chân đế, cảnh, tướng, bảng tên, trạng thái, chạm | `ZoneHabitat.cs` mới, prefab `Items/Habitat`, dựng bằng menu Editor như `BeAi` |
| Tướng đồng hành chạy tới ải kế, lính trên chấm, chấm lật | `ZoneWalker.cs` mới; `ZonePip` thêm trạng thái lật |
| Kéo hai chiều | `HubPan` nhận giới hạn theo cỡ nội dung; thêm hàm lướt tới một điểm |
| Bật tắt theo khung nhìn | `ZoneHabitat` tự dừng rig, hạt, `IslandAnim` khi ra ngoài khung |
| Kiểm dữ liệu | `GameData` (mục Dữ liệu) |

UI là prefab nướng sẵn (`PrefabOnlyTests`). Mảnh nền theo dữ liệu thì dựng lúc vào màn đảo từ pool hoặc nướng theo đảo bằng menu; chốt khi làm M1. Không làm bản web (`Web/`).

## Ảnh

Gen qua Magnific (1k high, 95 credit mỗi ảnh, trần 100) hoặc gói file prompt cho GPT theo luật trong `CLAUDE.md` (mỗi lượt một file, ảnh mẫu đường dẫn đầy đủ, mục SAVE, `HUONG_DAN.md`). Script gói: `ArtGen/Islands/build_land.py`, sinh `ArtGen/Islands/gui_gpt/land_thuy/`.

| Lượt | Nội dung | Số ảnh |
|---|---|---|
| 0 | **Ảnh bố cục** do script vẽ: lưới thoi, chân đế, ô dự trữ, đường, bờ, nước, chỗ cao nguyên và cây. Làm ảnh mẫu cho mọi lượt sau | 0 (script) |
| 1 | **Tờ cây và đá** Thủy: cọ, bụi nhiệt đới, dương xỉ, cột đá rêu, đá bờ biển, mỗi món rời, đúng cỡ trên lưới. Chốt nét cùng habitat ải 1 | 1 |
| 2 | **Habitat ải 1** (Võ Đài Mưa) làm mẫu: khung thoi đúng cỡ, hình tướng Tí Tách để cảnh hợp cỡ, ô chỗ tướng đứng; không vẽ tướng, không vẽ nước (chừa vùng nước) | 1 |
| 3 | Cao nguyên và vách (ghềnh đá, vách san hô) nhiều cỡ | 1–2 |
| 4 | Đồ kể chuyện (thuyền, lưới, thùng, biển chỉ đường không chữ, đèn lồng) và đồ lặt vặt (vỏ sò, sao biển, sỏi, cỏ con, hoa) | 1–2 |
| 5 | Texture lát: gạch chì cỏ, cát, giấy kem (nếu nhuộm màu). Script làm cho lát liền | 1–2 |
| 6 | Biển xa: dải chân trời có bóng 4 đảo, thuyền, mây | 1 |
| 7 | 9 habitat còn lại, **từng cái, duyệt xong cái trước mới dựng file prompt cái sau** | 9 |
| 8 | Món động lớn tách riêng (vỏ sò, đèn hải đăng…) khi cần rig | 3–5 |

Khoảng 20–25 ảnh, tính cả gen lại thì khoảng 2.000–3.000 credit cho đảo Thủy. Các đảo sau dùng lại khung, chỉ thay bộ mảnh (khoảng 6 ảnh) và 10 habitat.

Luật vẽ chung vẫn giữ: nét bút mực nâu sẫm hơi rung, chì màu và sáp màu, **không bóng đổ, không in bóng xuống nền**, tô phẳng.

## Các bước

| Mốc | Việc | Cần ảnh gen? |
|---|---|---|
| M0 | **Xong 2026-11-18.** Bố cục đảo Thủy (đường, 10 habitat, 60 chấm đúng cỡ và chỗ thật), khối `land` trong `zones.json` | Không |
| M1 | **Xong 2026-11-18.** Chạy trong Unity, nền tạm là concept chốt đã xoá thú và cờ; rig thật 10 tướng (idle, thỉnh thoảng attack, chạm thì đánh), một đường, kéo hai chiều, camera lướt, bảng tên, sóng shader | Không |
| M2 | Chốt nét: tờ cây và đá, habitat ải 1; đặt vào M1, chụp so | Có (2 ảnh) |
| M3 | Đủ bộ mảnh Thủy, shader nước hoàn chỉnh, rải đồ lặt vặt, biển xa | Có (khoảng 5 ảnh) |
| M4 | 9 habitat còn lại, từng cái; hiệu ứng động từng habitat (bảng ở mục Animation) | Có (khoảng 12 ảnh) |
| M5 | Nét bản đồ chương: tướng đồng hành chạy tới ải kế, lính trên chấm, chấm lật, thanh rương mốc; nhuộm màu nếu chốt | Không |
| M6 | 4 đảo còn lại: dùng lại khung, thay bộ mảnh và habitat | Có |
| Sau | Thêm boss mới vào ô dự trữ | Có |

### Kết quả M0, M1 (2026-11-18)

**Nền tạm.** Concept chốt `concept_F_sua_duong_2.png`, GPT xoá thú trên các bệ và cờ trên đường (`ArtGen/Islands/land_thuy/nen/nen_trong_1.png`). Phóng 2 lần bằng máy, vì phóng bằng AI tính giá theo bậc, có thể tới 180 credit, quá trần. Biển trên, dưới được đắp thêm bằng mảng biển lấy từ chính ảnh (mở rộng ảnh bằng Magnific tốn 130 credit, quá trần). Mục đích: đền rồng ở mép trên kéo xuống được dưới khung thông tin, mép ảnh khuất dưới hai khung.

**M0** (`ArtGen/Islands/land_thuy/m0/`):
- `diem_tho.py`: tâm 10 bệ, bên bảng tên, điểm chạm và điểm dẫn.
- `do_duong.py`: dò tâm con đường cát bằng đường đi rẻ nhất (Dijkstra) trên mặt nạ màu đường, đã che lòng bệ; vượt được cầu gỗ, cầu ván, bậc đá → `duong.json`.
- `build_land.py`: vùng đất 4800 × 3329 px khung 1080, rải chấm, vẽ `bo_cuc_m0.png`. `--xuat` ghi:
  - `Assets/03 Art/Islands/land_thuy.png` (2688 × 1864);
  - `Assets/03 Art/Baked/Islands/land_thuy_dist.png`;
  - khối `land` của đảo Thủy trong `zones.json`.
- Chấm ải 104 px, ải đang đánh 128 px (lần đầu 72/92 trông nhỏ, đã tăng). Chấm rải đều trên phần đường ngoài vòng đá và khung thân tướng; khúc chật thì so le hai bên đường.
- **Đường vẽ sẵn trong ảnh ngắn ở khúc 40 → 50** (9 chấm, so le khoảng 85 px một chấm), khúc 5 → 10, 10 → 15 cũng phải so le. M3 vẽ đường bằng code thì kéo dài các khúc này (thêm khúc lượn lên núi tím).

**M1** (code):
- `Core/Land.cs`: `LandDef`, `LandHab`, đọc JSON, kiểm dữ liệu; `ZoneDef.land`.
- `App/Scenes/ZoneSceneLand.cs`: phần riêng của `ZoneScene` (partial). Bật kéo ngang cho `ScrollRect` lúc chạy, không đổi cây prefab. Dùng lại `BeAi` (không vẽ bệ đất) làm habitat, `ChamAi` to có số làm chấm. Hình tướng là `AolaSticker`, chỉ dựng con trong khung nhìn cộng lề.
- `ZoneNode`: thêm `shadeLocked`, `HeroRect`, `ShowPortraitBody`. `ZonePip`: thêm `Bind` có cỡ, có số. `HeroPortrait.SetBody`.
- Shader `PokiClash/UIInkWater` (`03 Art/Shaders/UIInkWater.shader`), material `03 Art/Islands/land_water_thuy.mat`. Menu `PokiClash/Đảo vùng đất/Dựng nước, ảnh (Thủy)` đặt cách nhập ảnh khoảng cách, tạo material, gán vào `Screens/Zone`. `ArtImporter`: ảnh `/Islands/land_` nhập ở 4096.
- Tour `PokiClash/Thử/Đảo Thủy vùng đất: …` (đang Play) chụp vào `Temp/PokiShots/land/`; bản giữ lại ở `ArtGen/Islands/land_thuy/m1/`, tờ soi `soi_m1.jpg`.

**Đã soi trong Unity:**
- Vào đảo thì camera ở ải đang đánh. Ải vừa mở thì camera lướt từ ải trước tới, tướng ra sân.
- Idle chạy; đòn đánh định kỳ và khi chạm (ếch phóng lưỡi, rồng tung bọt nước tại chỗ).
- Ải chưa mở vẫn đủ màu, có khoá.
- Vệt chấm vàng đánh dấu quãng đường đã đi. Sóng chạy quanh bến, bờ, đá.
- EditMode 133/134 đạt. Bài trượt `PrefabOnlyTests` do `UI/Kit/NumberTicker.cs`, `UiMotion.cs` có sẵn từ commit `5f403ea9`, không do phần này.

**Còn lại sau M1:**
- Vầng sáng dưới habitat đang đánh chưa thấy rõ trên nền.
- Hiệu ứng riêng từng habitat (đèn hải đăng quay, sò mở khép…) để M4.
- Chưa đo trên máy thật (10 RenderTexture khi đi hết đảo).
- Bảng tên một số habitat lòi ra mép ảnh ở rìa đảo.
- Tên ải trong `stages.json` vẫn theo bản đồ cũ ("Ngọn Hải Đăng 5"…).

### Góp ý sau M1 (2026-11-18): đảo sống động, zoom, sáng tối

Người dùng: "đảo nhiều chi tiết nhưng tất cả còn tĩnh, mây, thuyền cũng tĩnh"; "gần quá, cho người chơi zoom ra / vào, vào đảo phải nhìn được toàn đảo"; "nếu được thêm tia nắng dịu và mode tối; mọi đảo kể cả home lấy thời gian sáng tối".

**Phần động** (`ArtGen/Islands/land_thuy/m0/vat_dong.py`, khoá `land_thuy` trong `island_anim.json`):
- Mây (2), hải âu (3), thuyền được cắt khỏi ảnh nền thành hình rời `Islands/land_thuy_*.png`, chỗ cũ vá bằng mảng biển lấy từ chính ảnh.
- `IslandAnim` thêm các kiểu động:
  - `drift`: mây trôi ngang, ra mép này vào lại mép kia; có thêm 3 đám dùng lại hình mây;
  - `glide`: hải âu lượn vòng elip, quay đầu theo hướng bay;
  - `boat`: thuyền dập dềnh, chòng chành, trôi qua lại;
  - `rain`: mưa xiên dưới mây giông, sprite `anim_rain`;
  - `swirl`: xoáy nước không kèm đinh ba.
- Thêm các món có sẵn: bọt chân 8 thác, gợn ở ao và hồ, lấp lánh ở ngọc, băng, nấm, đền; lá rơi ở cọ và rừng; sóng ngoài khơi.

**Camera** (`App/Scenes/LandView.cs`, gắn trên khung cuộn của `Screens/Zone`; đảo vùng đất tắt `ScrollRect`):
- Kéo một ngón, thả tay trôi theo đà, mép có dây chun. Chụm hoặc mở hai ngón (hay lăn chuột) để zoom quanh điểm giữa hai ngón.
- Zoom nhỏ nhất vừa khít toàn đảo (trừ khung trên, khung dưới), lớn nhất 1.
- Vào đảo: zoom vừa phủ kín khung (máy dọc là vừa khít chiều cao đảo, khoảng 0,47), canh ải đang đánh. Người dùng 2026-11-18: "được zoom ra như vậy nhưng khi vào thì không zoom ra nhiều như vậy".
- Biển quanh đảo: tấm biển lặp `Islands/land_thuy_bien.png` (512 px, lặp liền mạch). Lấy từ mảng biển của chính ảnh nền, cùng mật độ điểm ảnh, đặt trên `bien_cuon` tràn ra ngoài bản đồ. Thay biển lặp cũ (có vẽ sóng) vì hai lớp nước không khớp.
- **Vành mây** (người dùng 2026-11-18: "dùng mây che hết phần ảnh xanh lệch tông"):
  - `IslandAnim` kiểu `frame` (khoá `land_thuy.frame`): mây cắt từ ảnh nền phóng to, xếp dọc mép ảnh. Trên, dưới 5 hàng to dần ra ngoài; trái, phải 2 hàng. Dập dềnh chậm. Ngoài cùng là khối màu ruột mây `#fdf5e7` phủ kín.
  - Một hình mây cho cả vành để gộp lệnh vẽ.
  - Ảnh nền đắp thêm biển trái, phải 90 px ảnh gốc, để vành mây không đè vách đảo, bảng tên. Vùng đất thành 5443 × 3329, cỡ đảo giữ nguyên.
- Mây (vành mây, mây trôi) có màu riêng theo giờ, `DayCycle.CloudTint`: chiều ngả xám tím, đêm xanh xám tối hơn đảo. Đảo vẫn sáng.
- Chiều tối giảm nắng: tia nắng lúc chạng vạng chỉ còn 0,3 độ hoàng hôn. Ở màn đảo, ảnh tia nắng co về đúng khung ảnh đảo (phiên Nhà đã sửa shader tính dải nắng theo toạ độ ảnh, kéo bản đồ thì nắng đi theo).
- Chạm habitat thì zoom vào tối thiểu 0,7, lướt tới rồi mở hộp chuẩn bị.
- Zoom xa thì cờ ải (trước là chấm) phóng bù tới 1,8 lần, bảng tên tới 2 lần, để còn đọc được và chạm được.

**Sáng tối** (`DayCycle.cs`, `DayNight.cs`, shader `UIMultiply`, `UISunRays`; menu `PokiClash/Sáng tối/Dựng lớp sáng tối (Zone, Hub)`):
- Theo giờ máy:
  - đêm đủ tối từ 20h tới 4h30;
  - chạng vạng tối dần 17h30 → 20h, sáng dần 4h30 → 6h30;
  - ấm cam nhất quanh 6h và 18h20;
  - tia nắng mạnh dần 7h → 10h, yếu dần 15h → 17h30.
- Lớp `sang_toi` gồm ba phần:
  - `nhuom`: nhân màu cả cảnh;
  - `nang`: tia nắng chéo từ trên trái, trôi chậm, cộng sáng nhẹ;
  - `den`: đèn đêm theo khoá `lights` (đảo Thủy: đèn hải đăng quét vòng, quầng đèn ở đền, tháp mưa, 4 cụm nấm).
- Vị trí lớp:
  - màn đảo: ngay sau lớp phần động của ảnh bản đồ, nên cả 5 đảo đều có (tướng, chấm ải, đường đi nằm trên, không bị tối);
  - sảnh: trên biển, đảo, mây của `anh_nen_world`, dưới `lop_tren`.
- **Đêm** (người dùng 2026-11-18: "tối xung quanh thôi, đảo phải phát sáng, tối quá không nhìn được gì"):
  - đảo chỉ ngả xanh nhẹ (`DayCycle` NightTint 0,66 / 0,72 / 0,93);
  - biển tối thêm (`SeaNight`). Biển trong ảnh đảo tối dần theo khoảng cách tới bờ (shader sóng, `_PokiNight`, đổi sang thang màu tuyến tính cho khớp), sát bờ giữ sáng thành quầng quanh đảo. Tấm biển lặp quanh đảo và biển ở sảnh (`seaDark`) cũng tối theo.
- Thử giờ:
  - menu `PokiClash/Thử/Giờ trong game: 10h | 18h20 | 22h | theo giờ máy`;
  - SRDebugger (chạm 3 lần góc trái dưới), tab Options, mục "Sáng tối" (`StompyRobot/SROptions/SROptions.SangToi.cs`): nút "Đổi sáng / chiều / tối" bấm vòng, các nút Sáng (10h), Chiều (18h20), Tối (22h), Theo giờ máy, ô kéo giờ.
- Tour `PokiClash/Thử/Đảo Thủy vùng đất…` chụp toàn đảo ở 3 mốc giờ (mỗi mốc hai ảnh cách 3 giây để thấy mây, thuyền trôi), zoom vừa, hải đăng và vực hang lúc đêm, sảnh ở 3 mốc giờ.
- **Mây sảnh đồng bộ** (người dùng 2026-11-18: "mây ở phần đảo chính của game cũng phải đổi đồng bộ"):
  - vành mây `may_vien` và 3 đám mây trôi của sảnh đổi từ `sk_CloudPuff` (mây nướng mã hoá kênh) sang hình mây vẽ tay của đảo Thủy (`land_thuy_may_1/2`, xen kẽ);
  - mây sảnh nằm trong `DayNight.clouds`, nhân `CloudTint` như mây đảo;
  - menu `PokiClash/Sáng tối/Mây sảnh đồng bộ đảo vùng đất`; `HubWorldMenu` dựng lại cũng dùng hình mới;
  - mây, chim cắt từ ảnh nền (`vat_dong.py`) được khử viền xanh biển dính mép và phóng gấp 4 có làm nét (trước gấp 2), cho mây to ở sảnh không nhòe. Cỡ hiện trên đảo không đổi.

### Cờ ải thay chấm (2026-11-18)

Người dùng: "chia đều các ô ải ra, không cần phải hiện số ở dây, các ô này phải làm nổi bật để người chơi dễ thấy", rồi "có thể đổi sang dạng cờ cũng được".
- **Chia đều**: trước đây điểm mốc của mỗi habitat lấy cứng ở điểm đường gần tâm vòng đá nhất, nên khúc 40 → 50 dồn 9 chấm vào khoảng 85 px một chấm. Nay điểm mốc trượt trong đoạn đường ôm vòng đá (trong 1,6 lần bán kính vòng). Chọn chỗ để phần thưa hơn của hai chặng kề nhau là lớn nhất, lặp 4 lượt. Khoảng cách nhỏ nhất lên 119 px (khúc đầu, vẫn so le), các khúc khác 188–274 px. `ZoneSceneLand.LandLayout` và `build_land.py` (layout) cùng một cách.
- **Cờ** `LandFlag` (prefab `Items/CoAi`, menu `PokiClash/Đảo vùng đất/Dựng cờ ải (CoAi)`):
  - ô đá dưới chân, cán gỗ núm vàng, vải đuôi én phấp phới 6 khung;
  - ảnh vẽ bằng `ArtGen/Islands/land_thuy/m0/ve_co.py`: viền mực nâu hơi rung, vân chì, tô phẳng, không bóng. Vải và ô vẽ trắng để nhuộm, tờ soi ở `m1/soi_co.png`;
  - không số;
  - màu theo trạng thái: chưa mở xanh đậm `#4d72b8`, đã qua vàng `#f4bf3a`, đang đánh đỏ cam `#ff4d3a` (to 128 thay 104, phồng nhịp, bay nhanh nhất). Ô đá nhuộm nhạt cùng màu.
- Cờ và habitat xếp lớp theo chân: cờ dưới habitat đè lên tướng, cờ trên habitat nằm sau tướng.
- Zoom xa thì cờ phóng bù quanh chân như chấm cũ. Đảo 70 ải kiểu cũ vẫn dùng chấm `ChamAi`.
- Tour `PokiClash/Thử/Đảo Thủy vùng đất: cờ ải chia đều, nổi bật` (tiến độ 45): khúc 40–60 gần và vừa, khúc đã qua, khúc chưa mở (mỗi chỗ hai ảnh để thấy vải bay), toàn đảo, đêm.
- **Cờ nằm đúng trên đường** (người dùng 2026-11-18: "phải đặt các mốc đúng nằm trên path di chuyển chứ"): bỏ xếp so le hai bên đường (lối của chấm cũ), chân cờ đặt đúng điểm trên tâm đường, khoảng cách vẫn chia đều.

### Vùng boss (2026-11-18)

Người dùng: "phân section cho đảo, đánh xong 1 boss thì unlock section sau, nếu chưa unlock thì chúng có màu tối đen hẳn và tướng không play animation". Chốt này thay "ải chưa mở vẫn đủ màu" (2026-11-13) ở đảo vùng đất.
- **Vùng k** ứng với habitat k: đoạn đường từ boss k-1 tới boss k cộng bệ boss k (đảo Thủy: vùng 0 là bến và ải 1, vùng 1 ải 2–5, …, vùng 9 ải 61–70). Vùng k mở khi đã qua ải boss k-1 (`LandDef.OpenSections`, `SectionOf`).
- **Ranh giới** (`ArtGen/Islands/land_thuy/m0/vung.py`, gọi từ `build_land.py`):
  - mỗi chỗ trên đất thuộc vùng có đoạn đường gần nhất;
  - khoảng cách tới tâm bệ boss tính 0,32 lần để cảnh quanh bệ thuộc vùng của boss;
  - sông, hồ trong đảo tính là đất.
  - Tờ xem trước: `m0/vung_m0.png` (chia vùng), `m0/xem_khoa.py` (`xem_khoa.png`: phác chì, mây; `--c`: kết hợp). `--xuat` ghi ảnh trường vùng, `secs` (khung, mây), `grid`, `cloud` trong khối `land`.
- **Vẽ vùng khoá** (người dùng 2026-11-18: phủ đen "không đẹp" → "kết hợp cả A và B, mây tan ra, có bút chì vào tô màu section mới", "cho mây che nhiều lên"):
  - **phác chì**: ảnh `phac_vung` (con đầu của ảnh bản đồ, dưới hiệu ứng, sáng tối), shader `PokiClash/UILandSketch`:
    - dựng bản phác từ chính ảnh đảo (nét mực nâu, giấy kem, vân chì), không cần ảnh mới;
    - vùng khoá theo ảnh trường vùng `Baked/Islands/land_thuy_vung.png` và biến toàn cục `_PokiLandOpened`;
  - **mây phủ**: mây vẽ tay `land.cloud` (một hình cho mọi đám), chỗ đặt trong `land.secs[k].clouds`. Khoảng 650 đám cho 10 vùng, che gần kín, khe mây lộ nét phác;
  - hiệu ứng (lấp lánh, mưa, lá) và đèn đêm trong vùng khoá tắt (`IslandAnim.HideWhere`, `DayNight.HideLampsWhere`, lưới vùng thô `land.grid`);
  - tướng vùng khoá xám, đứng một khung; cờ vùng khoá chưa mọc;
  - chạm cờ, tướng vùng khoá thì báo "Hạ <boss> ở ải <n> để mở vùng này".
- **Cảnh mở vùng** (`RevealSection`):
  1. chờ chuyển cảnh xong, khoá mọi thao tác (`CloudCover.Block`);
  2. camera đưa cả vùng vào giữa;
  3. mây tản ra rồi tan (1,1 giây);
  4. bút chì (`Islands/Co/but_chi.png`, vẽ bằng `ve_co.py`) bay vào ngoáy dọc đường, màu loang theo nét bút (`_PokiLandReveal`, 2,6 giây), tô nốt (0,6 giây);
  5. tướng boss diễn ra sân, cờ mọc lên lần lượt từng cái theo đường (nảy từ chân);
  6. nhả khoá.
  - Người dùng 2026-11-18: "lần đầu tiên vào mỗi đảo sẽ có đoạn mở section đầu tiên … lock input bắt người chơi phải xem (mỗi khi unlock section đều bắt người chơi phải xem)".
- **Số vùng đã diễn** lưu ở `SaveData.extra["landShown"]` (`LandShown`, không thêm trường vào bản lưu):
  - vào đảo thấy vùng đã mở mà chưa diễn thì diễn vùng mới nhất (vùng cũ hơn mở ngay);
  - lần đầu vào đảo diễn vùng 0 (bến, ải 1, tướng Tí Tách);
  - ghi vào bộ nhớ khi diễn xong; lần lưu kế tiếp ghi xuống file (gọi Save ngay làm màn dựng lại).
- Menu `PokiClash/Đảo vùng đất/Dựng cờ ải, vùng boss`. Tour `PokiClash/Thử/Đảo Thủy vùng đất: vùng boss, cờ trên đường, khoá đảo`: tiến độ 0, 23, ranh vùng, lần đầu vào đảo (ghi lớp chắn chạm), mở vùng 21–30, cờ khúc 50–60 và 46, thử nút SRDebugger.
- **SRDebugger, mục "Khoá đảo"** (`StompyRobot/SROptions/SROptions.KhoaDao.cs`, người dùng 2026-11-18: "thêm option lock lại các đảo"):
  - nút "Khoá lại hết đảo" đưa cả 5 đảo về 0 ải đã qua;
  - ô số "Đảo <hệ>: ải đã qua" cho từng đảo;
  - hạ tiến độ thì rương mốc chưa tới coi như chưa nhận, xoá số lần qua của ải bị khoá, đội AFK ở ải bị khoá về tự chọn.
  - đảo vùng đất: đặt lại số vùng đã diễn để vào đảo diễn lại (khoá hết: diễn mở vùng đầu như lần đầu vào đảo; đặt n ải: diễn mở vùng mới nhất).

### Easter egg vùng khoá (2026-11-18)

Người dùng: "làm 1 vài easter egg cho các zone khi bị khóa (khi bị khóa thôi) để kích thích tò mò người chơi", "làm cả 6", rồi "bỏ cái mắt nhìn và thi thoảng để tướng bay lên, thay vào đó làm tướng dùng ultimate skill, thi thoảng thôi … vài lần thôi". Code ở `App/Scenes/ZoneSceneEggs.cs`; hình ở `Islands/Co/trung_*` (`m0/ve_trung.py`); chỗ đặt ở `land.secs[k]` (`vung.py`, hàm `trung`).
- **Boss tung tuyệt kỹ:**
  - mây quanh bệ dạt ra (giữ đục), boss hiện màu thật tung clip `skill` tại chỗ, hiệu ứng ở phía trước, xong mây khép lại, boss về xám;
  - mỗi lần vào đảo nhiều nhất 3 lần: lần đầu sau 10–16 giây, sau đó cách 70–120 giây, chỉ boss đang trong khung.
- **Cảnh rò qua mây** từng vùng (đảo Thủy): đom đóm (đầm), đèn biển quét (hải đăng), bong bóng (san hô), hải âu (xác tàu), sét và mưa (đền Giông Mưa), cá voi phun nước, nấm tím phát sáng, tuyết rơi, xoáy nước (lộ trong khe mây).
- **Chọc mây:**
  - chạm mây thì đám quanh đó dạt ra rồi nảy về (lò xo từng đám, chạm liên tục cộng dồn mượt, mây giữ đục; góp ý "mây tỏa ra vẫn mờ và chưa mượt");
  - lần chạm đầu báo phải hạ boss nào;
  - chọc 7 lần thì boss hắt xì thổi tung mây, quà một lần +3 bi (`extra["landPoke"]`).
- **Rương bí ẩn** (rương gỗ `pk_ruong_go`) ló trong khe mây, sâu trong đất:
  - chạm khi vùng còn khoá: báo "mở vùng này để nhận";
  - vùng mở rồi: rương nảy, chạm nhận 6 + 2k bi (8–24; `extra["landGift"]`).
- **Ghi chú bút chì** (phông Pangolin của game) ở mép vùng, vẽ trên lớp mây cho đọc được, tan khi mây tan: "ộp ộp…?", "Ai thắp đèn?", "Ngọc trai!?", "Xác tàu cũ", "Đừng vào khi mưa!", "Xương… to quá!", "Nấm phát sáng?!", "Lạnh buốt…", "Hang rồng?".
- Tour `PokiClash/Thử/Đảo Thủy vùng đất: easter egg vùng khoá`.

### Tối ưu (2026-11-18)

Người dùng: "tris nhiều quá, batches cũng nhiều so với game 2D". Menu `PokiClash/Thử/Đo hiệu năng đảo vùng đất` tắt lần lượt từng lớp, ghi batches, tris, SetPass vào `Temp/PokiShots/do_hieu_nang.txt`.
- **Camera hình tướng:**
  - camera chỉ được bật hay tắt khi có gọi `Show`, nên tướng thôi được `Show` (ngoài khung, vùng khoá) thì camera kẹt bật, vẽ lại mỗi khung. 10 tướng chiếm 102k / 109k tris;
  - thêm `AolaSticker.Hold()`: khung không `Show` thì tắt camera;
  - zoom dưới 0,7 vẽ tướng 2 khung một lần, dưới 0,5 thì 3 khung.
  - Đo lại: tris 109k → khoảng 19k, verts 61k → 20k.
- **Canvas con:** `lop_may_vung` (mây phủ tĩnh), `lop_tren_may` (easter egg, bút chì), cho canvas chính khỏi phải gộp lại hàng trăm đám mây mỗi khung.
- **Ẩn thứ nằm dưới mây:** ảnh tướng, ảnh hiệu ứng, bảng tên của bệ vùng còn mây phủ ẩn hẳn (mỗi tướng 1–2 RenderTexture riêng, mỗi bảng tên 3–4 lệnh vẽ); hiện khi tung tuyệt kỹ hay khi mây tan.
- **Vùng chạm trong suốt** (cờ, bệ): `cullTransparentMesh`.
- **Sprite Atlas** (menu `PokiClash/Tối ưu/Sprite Atlas đảo (dựng lại)`, bật Sprite Atlas V2 cho project): `Islands/dao_hinh_roi.spriteatlasv2` gồm cờ, easter egg, bút chì, hiệu ứng đảo `anim_*`, mây, chim, thuyền, rương, icon bảng tên bệ. Atlas 2048, không xoay, không gói sát. Chưa gom cả 75 icon (cần texture 4096).

## Câu cần chốt

1. Cỡ vùng đất: khoảng 1,6–2 × 2–2,5 màn có hợp không, hay muốn nhỏ hơn để thấy gần hết đảo?
2. ~~Lưới thoi hay vuông~~: chốt thoi theo Critters (2026-11-18).
3. Ải đã qua: cắm cờ và đổi idle như đề xuất, hay để y nguyên?
4. Chạm tướng: phản ứng rồi mở hộp chuẩn bị luôn, hay chạm lần hai mới mở?
5. Bảng habitat theo lô tướng mới ở trên có cần đổi gì không?
6. Nhuộm màu kiểu Critters: nền đoạn chưa qua để nét chì chưa tô, qua rồi mới tô màu (habitat vẫn đủ màu như đã chốt). Làm hay không?
7. Tướng đồng hành chạy tới ải kế: nhảy cóc bằng code (làm ngay được), hay làm clip đi cho 5 tướng khởi đầu?
8. Nền: code vẽ đa giác tô texture gạch chì lát (đề xuất: rẻ, sửa dễ), hay gen mảng cỏ, mảng cát lớn như Critters (đẹp hơn ở mép, tốn thêm khoảng 4–6 ảnh mỗi đảo)?
9. ~~Luật mở ải với bản đồ vùng~~: chốt một đường, ải mở theo thứ tự như cũ (2026-11-18).
10. ~~Bệ tròn hay vuông~~: chốt bệ tròn viền đá (2026-11-18).
