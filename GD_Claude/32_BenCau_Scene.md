# 32. Bến câu: scene riêng, nhân vật chính đứng câu, shader nước, thả câu tương tác (kế hoạch 2026-11-26)

Kế hoạch đảo: `29_DaoCasino.md` (mục 6.2 luật câu cá). Concept: `ArtGen/Casino/ben_cau/`.

## Người dùng dặn (2026-11-26)

> "phần câu cá tôi muốn bạn làm giống trong clash of critters" → "tôi chỉ cần bạn copy phần game play và màn chơi thôi, còn khi chơi vẫn giữ
> logic hiện tại" → (xem bản đầu) "tôi muốn bạn làm chỉn chu hơn, gen thẳng 1 scene riêng, có người đứng câu cá có animation, có shader nước,
> thả câu có tương tác..."

Đã chốt (người dùng chọn theo đề xuất):
1. **Người câu là nhân vật chính** (cậu thám hiểm đã duyệt, `ArtGen/Story/duyet/nhan_vat.png`): người chơi tự câu, như Critters để thú của
   người chơi đứng câu.
2. **Góc nhìn sau lưng, chếch trên**: cậu đứng cuối bến gỗ ở đáy màn, quay lưng 3/4, quăng lên hồ phía trên; thấy bóng cá dưới mặt nước.
3. **Kéo ngắm rồi thả**: giữ và kéo trên mặt nước để chọn chỗ thả (vạch đường bay), thả tay thì cậu vung cần, phao bay theo dây. Ba vùng Gần bờ /
   Xa bờ / Rạn đá vẽ ngay trên hồ thay cho 3 nút; vùng chưa mở có khoá. Sau đó giật và thanh vùng vàng như Critters (mục 6.2 của `29`).

Logic giữ nguyên: `Core/Casino/Fishing.cs` (mồi, chỗ câu, chọn cá, cần câu, Sổ Cá, bán cá, Cá Vua, `Ticks`, `SizeClass`).

## 1. Cảnh

- Dọc 2:3, vẽ tay như `ArtGen/Islands/refs/world_style.png`: nét mực nâu hơi rung, chì màu + sáp màu, tô phẳng.
- Đáy màn: cuối bến gỗ (dưới hàng nút); giữa: hồ rộng, thoáng (vùng chơi); trên: bờ xa có rạn đá, đèn lồng, cờ, lều, xa xa đỉnh Tháp Máy Bi.
- **Gen theo lớp** (như Nhà, đảo Casino): (1) nền không có nhân vật, mặt hồ để màu phẳng; (2) mặt nạ nước (hồ, độ sâu: gần bờ / giữa / rạn
  đá) để shader vẽ; (3) lớp trước: cọc bến, lau sậy, lá súng (đè lên nước, lắc nhẹ).
- Ba vùng câu là ba dải trên hồ: Gần bờ (nước nông sát bến), Xa bờ (nước sâu giữa hồ), Rạn đá (quanh đá phía trên).

## 2. Nhân vật chính đứng câu

- Rig AtomSpine (.atomik) như Lão Mực (`31`, `ArtGen/Casino/dealer/rig/`), luật `animation-humanoid` + `animation-petclash`.
- Cần câu là mảnh riêng gắn tay, **dây câu do code vẽ** (đường cong có vật lý từ đầu cần tới phao), không vẽ trong rig.
- Clip: `idle` (cầm cần, thở, tóc / áo choàng lay), `ngam` (giữ dáng kéo cần ra sau theo hướng ngắm), `quang` (vung cần, sự kiện thả dây),
  `cho` (đợi, liếc, gãi đầu khi lâu), `giat` (giật cần), `keo` (ghì cần cong, nhún theo nhịp trúng vùng vàng), `trung` (quay lại giơ cá),
  `hut` (xụ vai). Cần câu cong theo lực kéo (chuỗi xương).
- Tờ dáng: `ArtGen/Casino/ben_cau/dang_cau.png` (8 dáng, nhìn sau lưng, dáng 7 quay mặt lại).

## 3. Shader nước

- Dựa trên bộ đã có: `UIHomeSea` (biển Nhà kiểu Critters: dải màu theo độ sâu, vạch bọt sát bờ, vân sáng trôi), `UIFlowWater`, `UIInkWater`.
  Viết `UIPondWater`: mặt nạ độ sâu → bậc màu phẳng; vân sóng nét chì trôi chậm; vạch bọt quanh bờ, cọc bến, đá; **gợn tròn** tại phao (tham
  số vị trí, thời gian: khi rơi, khi cá rỉa, khi giật), vệt sóng theo bóng cá, bắn nước khi phao rơi / cá vùng.
- Luật: tô phẳng, không quầng sáng, không chuyển màu mềm (luật UI, `vfx-petclash`); hằng màu viết trong shader đổi `GammaToLinearSpace`.

## 4. Thả câu tương tác

- Giữ ngón trên hồ: vạch chấm cong từ đầu cần tới điểm ngắm, vòng đích nhấp nháy; vùng dưới đích sáng viền (Gần bờ / Xa bờ / Rạn đá), vùng
  khoá hiện ổ khoá và "Nâng cần câu". Cậu kéo cần ra sau theo hướng ngắm (clip `ngam`).
- Thả: clip `quang`, phao bay theo đường cong, dây duỗi ra; rơi xuống bắn nước + gợn tròn; dây võng (vật lý chuỗi điểm).
- Chờ: bóng cá bơi lại, rỉa phao (phao nhấp, gợn nhỏ), cắn thì phao chìm (gợn lớn), nút "GIẬT!".
- Kéo: cá lớn ra thanh vùng vàng như bản Critters; dây căng, cần cong, bóng cá giãy, nước bắn theo nhịp; mỗi nhịp trúng kéo cá lại gần.
- Trúng: cá vọt khỏi nước (cung bay) vào tay cậu, clip `trung`, thẻ kết quả. Sổng: dây chùng, bóng cá lao đi, clip `hut`.

## 5. Mốc

| Mốc | Việc | Duyệt |
|---|---|---|
| **B0** | Concept cảnh (2 phương án) + tờ dáng nhân vật | người dùng chọn |
| B1 | Gen lớp cảnh (nền, mặt nạ nước, lớp trước) | ảnh ghép |
| B2 | Tờ mảnh nhân vật (nhìn sau lưng) + cần câu, rig, 8 clip | GIF / trang xem |
| B3 | Shader `UIPondWater` + gợn, bắn nước | GIF |
| B4 | Scene mới trong Unity: ngắm, thả, dây, chờ, giật, kéo, kết quả nối lõi | tour chụp + quay |
| B5 | Âm thanh (bắn nước, quay guồng, cá vùng), soát máy thật | |

## Tiến độ

- 2026-11-26: B0 xong (3 tờ, 285 credit): `canh_A.png` (dừa, chòi lá, hồ rộng), `canh_B.png` (cây tán tròn, cờ trên lan can bến, đá viền
  bờ), `dang_cau.png` (8 dáng nhìn sau lưng). Trang xem `ArtGen/Casino/ben_cau/xem.html`. Chờ người dùng chọn cảnh.
- 2026-11-26: người dùng chọn **cảnh A**, dặn "update atomspine mới nhất rồi làm qua atomspine". AtomSpine 0.2.3 đã là bản mới nhất
  (`c:\Atomik\AtomSpine` = origin/main, runtime Unity 0.2.3 = CLI); build thêm Studio web (`npm run build -w @atomspine/studio`).
  Bộ skill trong project mới hơn bản đi kèm AtomSpine nên không cài đè.
- **B1**: `nen_A.png` (nền sạch, bỏ người, cần, phao, bóng cá). `nuoc/lam_nuoc.py` → `Assets/03 Art/Casino/BenCau/ben_cau_nen.png`,
  `ben_cau_nuoc.png` (R nước, G khoảng cách bờ, B vùng câu theo khoảng cách tới chỗ đứng (512, 1300): Gần bờ < 400, Xa bờ < 790,
  còn lại Rạn đá).
- **B2 bản rig 1** (`ArtGen/Casino/ben_cau/rig/`, AtomSpine project `atom/`):
  - `goc_rig.png`: tờ gốc nhìn sau lưng, không viền, tỉ lệ như cảnh A. Bản đầu `goc_rig_v1_dai.png` chân dài nên bỏ.
  - `phu.png`: đầu quay lại cười, cần câu, nắm tay có lỗ, tay xoè.
  - `chuan_bi.py`, `cat_phu.py` cắt mảnh, vẽ bù phần bị che.
  - `dung_rig.py`: 33 xương, 14 slot, IK chân (ủng đứng yên), IK tay trái bám cán cần, cần 4 đốt uốn, xương `dau_can` cho game nối dây.
  - `hoat_anh.py`: 9 clip — idle, ngam, quang (`tha`), cho, giat (`giat`), keo, nhip, trung (`ca_len`), hut. Mỗi khoá khai cổ tay
    phải + góc cần, script tự giải IK; áo choàng, chỏm tóc dùng lò xo / sóng.
  - `xem.py`: GIF trên nền, trang `rig/xem/xem_rig.html`. Chưa vẽ viền: theo luật, viền vẽ bằng Paint sau khi chốt animation.
  - Tổng credit tới đây: 285 + 95 × 4 = 665.
- **B2 bản rig 2** (người dùng xem Studio: "tay lỗi nhiều, không cần show tay cầm cần"):
  - hai tay cầm cần ở phía trước người nên khuất sau áo choàng; cánh tay khép vào, chỉ lộ tay áo ở vai; nắm tay ẩn;
  - cần gắn điểm cầm `cam` (con của ngực) thay vì bàn tay, đặt sao cho cán bần và guồng luôn khuất sau đầu / mũ trùm;
  - bỏ IK tay trái;
  - mảnh thân áo vẽ bù thu hẹp (trước đó lòi mảng kem cạnh áo choàng khi áo lắc);
  - clip `trung` bỏ vẫy tay, giữ quay mặt cười + nhảy cẫng + giơ cần.
- **B2 bản rig 3** (người dùng: "phần tay không cần cử động, tay vẫn bị tách và cụt, bạn cứ gen 2 tay bình thường thôi, khi câu lắc
  người như này là ổn rồi", "không cần animation phần tay"):
  - gen `goc_tay_cam.png` (95 credit), giữ nguyên người, chỉ đổi hai tay sang dáng cầm cần trước ngực: thấy tay áo và khuỷu, bàn tay
    khuất. Thân trùng tờ cũ (IoU 0,992, không lệch) nên dùng làm tờ gốc;
  - hai tay là mảnh cứng gắn ngực, phần dưới mép áo choàng vẽ bù. Bỏ xương tay và bàn tay, không còn khoá tay nào;
  - giữ nguyên lắc người, cần, áo, đầu. Rig còn 27 xương, 12 slot. Tổng credit: 760.
  - Lưu ý: Studio đang chạy thì `atom do` ghi vào project trong bộ nhớ của Studio.
- 2026-11-26: người dùng **chốt animation** ("ok chốt, làm tiếp shader nước và scene"). Viền mực nhân vật (Paint AtomSpine) chưa vẽ.
- **B3 + B4 bản 1** (scene Unity):
  - Rig: `atom export atomik --profile mobile --atlas-cap 1024` → `Assets/03 Art/Casino/BenCau/cau_ca.bytes` (628 KB, atlas 344 × 1032),
    chạy bằng `AtomikGraphic` của runtime AtomSpine (gán asset lúc chạy, như dealer).
  - Shader `Assets/03 Art/Shaders/UIPondWater.shader` (material `ben_cau_nuoc.mat`), vẽ trên nền trong mặt nạ nước:
    - lăn tăn;
    - bóng cá (6 con: 1 cắn câu + 5 bơi);
    - vệt sóng trôi;
    - bọt vỗ bờ;
    - gợn tròn elip (4 nguồn);
    - vùng câu lúc ngắm: vạch đứt ở ranh, vùng chỉ tô vàng, vùng khoá phủ xám gạch.
  - `FishingPanel` viết lại, giữ thanh vùng vàng, kết quả, Sổ Cá, logic:
    - kéo ngắm trên hồ (vạch chấm cong, vòng đích, tên vùng / khoá);
    - quăng theo sự kiện `tha`, phao bay cung, rơi bắn nước + gợn;
    - cá bơi lại rỉa phao; giật; kéo, mỗi nhịp `nhip` có nước bắn, phao bị kéo về;
    - trúng: `ca_len`, cá vọt bay về đầu cần;
    - sổng: `hut`, dây chùng.
  - `FishingLine` (dây cong bậc hai, võng theo trạng thái), `AimArea` (chạm / kéo / nhả).
  - `CasinoFishingMenu` dựng cây cảnh mới; 3 nút chỗ câu bỏ (vùng nằm trên mặt hồ). Đồ nhỏ vẽ bằng `ArtGen/Casino/ben_cau/lam_do.py`
    (phao, giọt nước, cá trắng tô màu hệ); mặt nạ nước cho code `ben_cau_nuoc_cpu.bytes`.
  - Tour đầu: chạy đúng các bước. Lỗi: điểm ngắm mặc định Gần bờ nằm sau lưng cậu, phao bị che. Sửa: không thả phao vào khung người
    che (`Body`), điểm ngắm mặc định ra hai bên, phao bị kéo về mép bên chứ không về giữa bến.
  - Tour lại 16:20: chạy trọn 3 lượt và Sổ Cá. Ảnh ở `ArtGen/Casino/ben_cau/scene_tour/`, trang xem `xem_scene.html`.
  - Điểm ngắm mặc định Gần bờ đổi thành (700, 1060), vì bản cũ (730, 1000) lọt ra ngoài ranh nên nhãn hiện "Xa bờ". Đã chép vào Assets,
    Unity biên dịch sạch.
- **Bản 2** (người dùng: "shader nước chưa có, nước quá tĩnh không có tương tác với mồi câu / dây câu", "phao nhìn tĩnh quá không có
  độ 3d chồi lên thụt xuống", "cách chơi phải giống như clash of critters", "căn 1 thanh chạy rồi tap đúng lúc"):
  - Cách chơi như Critters: bỏ kéo ngắm.
    - Chọn chỗ bằng 3 nút trên (khoá theo cấp cần). Chạm CÂU (hoặc mặt nước) là quăng tới chỗ ngẫu nhiên trong vùng đó, trong phần
      nền nhìn thấy trên màn hẹp.
    - Cá cắn thì chạm GIẬT, rồi luôn qua thanh chạy: `max(1, Ticks)` nhịp, cá nhỏ 1 nhịp.
  - Shader bản 2:
    - lăn tăn hai tầng (2,6 px);
    - vệt sáng chì màu chạy theo sóng;
    - vệt sóng dày hơn;
    - quanh phao (`_Bob`): nước sẫm, vòng nước bám, 3 gợn toả liên tục, khúc xạ;
    - vệt rẽ nước chữ V (`_Wake`) khi phao bị kéo;
    - 8 gợn sự kiện.
    - Lỗi đã gặp: ảnh mặt nạ 1024 × 1536 bị Unity giãn lên 1024 × 2048 (NPOT) nên shader lấy cỡ đó, mọi thứ code đặt lệch dọc ×1,33
      (gợn, phao rơi xuống đất). Sửa: `_PlateSize` cố định + nhập mặt nạ `npotScale = None`.
  - Phao 3D:
    - hai lớp RectMask2D cắt theo mặt nước (trên rõ, dưới tô xanh mờ);
    - lò xo dọc (rơi cắm sâu rồi nảy, rỉa nhấp, cắn chìm hẳn, nhịp kéo bật lên);
    - nghiêng theo sóng, vận tốc và dây căng;
    - lúc bay tắt mask.
  - Âm thanh: thêm `splash`, `plop`, `bloop`, `reel` vào `Core/SfxSynth.cs`.
  - Đêm cho nước: bỏ khỏi shader vì đất không tối theo; làm sau cùng lớp đêm cả cảnh.
- **Bản 3** (người dùng: "bỏ phần nâng cấp cần đi, khi thả câu thì cho người chơi thả random trên hồ câu", "có cá thì không cần ấn giật
  nữa"):
  - lõi `Fishing.Spots` trả đủ 3 chỗ, `KingAvailable` bỏ điều kiện cấp cần; test `CauCa_Moi_SoCa_DuBo` đổi (rạn đá mở sẵn);
  - giao diện bỏ nút Nâng, chữ cấp cần, 3 nút chỗ câu;
  - chạm CÂU: phao rơi ngẫu nhiên trên hồ (phần nhìn thấy, ngoài chỗ người che); vùng phao rơi là chỗ câu. Lượt đầu đời rơi vào Gần bờ;
  - cá cắn: phao chìm, "!", 0,35 giây sau tự vào thanh chạy; bỏ cửa sổ giật (biteWindow không dùng nữa).
- **Hình cá** (người dùng: "các con cá gen vài con đi, càng hiếm càng dị và đẹp, tối ưu dung lượng, gen bằng gpt"):
  - 5 tờ Magnific GPT 2.6 (1k high, 95 credit / tờ, tổng 475), mỗi hệ một tờ 7 con theo thứ tự độ hiếm, kèm Cá Vua:
    `ArtGen/Casino/ben_cau/ca/to_<hệ>.png`. Tờ Thủy làm mẫu, 4 tờ sau lấy tờ Thủy làm ảnh mẫu thứ hai.
  - Ba tờ trả nền trong suốt dù prompt xin nền hồng; `cat_ca.py` xử cả hai.
  - `cat_ca.py`: tách nền, khử viền hồng, gán loài theo vị trí. Ra `Assets/03 Art/Casino/BenCau/Ca/<id>.png`: cạnh dài 256 px
    (Cá Vua 320), 8 bit 160 màu, cả 35 con 645 KB. Unity nhập Sprite, `maxTextureSize` 256 (Cá Vua 512), không mipmap, nén ASTC.
  - Trong game: thẻ kết quả (cá to hơn vòng màu), Sổ Cá (chưa bắt là bóng đen), cá vọt khỏi nước.
  - Lỗi đã gặp: Image cũ mang sprite chấm Sketch nên dùng material giải mã, thay sprite cá vào thì cá bị xám. Sửa: gán qua
    `Theme.SetSprite` (đổi cả material).
  - Còn làm:
    - viền mực nhân vật (Paint AtomSpine);
    - âm thanh (bắn nước, quay guồng);
    - hình cá thật (C8);
    - đêm (`_PokiNight`);
    - soát trên máy thật. Dựng lại bằng `dung_rig.py` (init --force) phải tắt
    Studio trước.
