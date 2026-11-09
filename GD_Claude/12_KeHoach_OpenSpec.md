# Kế hoạch làm game trong Unity (OpenSpec)

Viết 2026-10-31, sau khi chủ dự án duyệt bản web (luật trận, bố cục scene, phong cách). Plan chi tiết nằm ở `openspec/` (OpenSpec 1.3, schema `spec-driven`). Mỗi change có:
- `proposal.md`: vì sao, đổi gì, ảnh hưởng;
- `design.md`: quyết định, rủi ro, câu hỏi mở;
- `tasks.md`: danh sách việc;
- `specs/*/spec.md`: yêu cầu và tình huống kiểm thử.

Kiểm tra: `openspec validate --all --strict`. Hiện cả 12 change hợp lệ.

## Lộ trình

| Mốc | Change | Nội dung | Phụ thuộc | Việc |
|---|---|---|---|---|
| 0 | `setup-unity-foundation` | Scene Boot và scene chức năng, màn mây, thanh trên và thanh quay lại, bộ UI vẽ tay, phông tiếng Việt, lưu, dữ liệu một nguồn từ web, quy ước ảnh, aola chỉ trong bản dev | — | 35 |
| 1 | `add-card-battle` | Luật trận thẻ bài (chép từ web), hồi sinh, máy địch, màn trận, hộp kết quả | 0 | 24 |
| 2 | `add-hero-roster` | 11 tướng, cấp chung, mảnh, thẻ riêng lên cấp bằng bản sao, tiến hóa sao, scene Tướng và Sổ thẻ | 0 | 12 |
| 3 | `add-world-islands` | Sảnh đảo lớn 5 vùng, scene đảo hệ 8 ải, rương mốc, chuẩn bị trận, thưởng ải | 0, 1, 2 | 19 |
| 4 | `add-pachinko-machine` | Máy bi vật lý, cược ×N, rương, mốc Huyền thoại, bảng tỉ lệ | 0, 2 | 14 |
| 5 | `add-afk-rewards` | AFK ra bi và mảnh, rương AFK có giờ mở, tăng tốc ×2 | 2, 3 | 10 |
| 6 | `add-balance-tools` | Máy tự chơi hàng loạt, mô phỏng máy bi và tiến độ, bảng thử, chỉnh số, ghi trận, golden | 1–4 | 11 |
| 7 | `add-element-badges` | Đền Huy Hiệu: chuỗi 5/10 trận boss theo hệ, +5%…+20% cho tướng cùng hệ | 1, 2, 3 | 11 |
| 8 | `add-potential-stones` | Đá tiềm năng, 4 ô mỗi tướng, khai phá có khoá ô, Hang Tiềm Năng | 1, 2, 3, 4 | 11 |
| 9 | `add-hero-farm` | Trang trại 8 chỗ, năng suất và thời lượng theo sức tướng, nghỉ ngơi | 2, 3, 5 | 9 |
| 10 | `add-monetization-hooks` | Quảng cáo thưởng và IAP qua lớp móc, giới hạn mỗi ngày, không bán bi | 0 | 8 |
| 11 | `add-ball-trees` | Cây bi trên sảnh thay bi AFK, trang trại ca dài, đường cong cấp vào cấu hình (chốt 2026-10-31) | 5, 9, 10 | 14 |
| 12 | `convert-to-prefabs` | Mọi thứ là prefab và asset làm sẵn (kể cả UI), runtime không sinh gì; nướng một lần bằng code dựng cũ rồi xoá code dựng | 0–11 | 31 |
| 13 | `update-pachinko-feel` | Máy bi học Clash of Critters: vật lý bồng bềnh, két vàng có mái và ô vàng khuất (11 ô, kinh tế mỗi bi giữ nguyên), web và Unity trùng từng bit, phản hồi hình, tiếng, rung chia bậc, chậm và rung màn cho rương vàng, prompt FX, nút Rung trong Sổ tay (chốt 2026-11-02) | 4, 12 | 21 |

Mốc 0–4 là vòng lõi chơi được (đánh ải → bi → máy bi → nuôi tướng). Mốc 5–6 làm vòng lõi bền và đo được. Mốc 7–9 là side meta của GDD. Mốc 10 làm song song được với mốc 5 trở đi.

## Đối chiếu GDD gốc

| Mục trong "GDD game Pokiwar" | Change |
|---|---|
| Core loop: đánh ải nhận bi → pachinko → nâng tướng → quái cao cấp hơn | `add-world-islands`, `add-pachinko-machine`, `add-hero-roster` |
| Boss, mini boss có cơ hội ra mảnh tướng | `add-world-islands` (thưởng ải) |
| AFK ải đã qua: bi hoặc mảnh tướng (tỉ lệ thấp), khai thác reward | `add-afk-rewards`, `add-monetization-hooks` |
| Mỗi bên 1–3 tướng; đầu lượt được đổi tướng (địch cũng thế) | `add-card-battle` |
| Chọn 1 trong 3 thẻ, 5 lần; các thẻ ví dụ (+10% công, +15% máu, hi sinh máu lấy công, hồi 30%, +10 mana, +10% thủ, hi sinh thủ lấy +100% công, +10 nộ) | `add-card-battle` (23 thẻ chung) |
| 1–3 thẻ nội tại mỗi tướng: chiêu (mana), ultimate (đầy nộ + mana), bị động (luôn có, hoặc khi dưới x% máu) | `add-card-battle`, `add-hero-roster` |
| Thẻ có độ hiếm; mở tướng thì có thẻ cấp 1; nâng thẻ bằng cách thu thập | `add-hero-roster` (hero-cards) |
| AFK cũng ra thẻ nhưng hiếm hơn; mở rương, ×2 tốc độ bằng reward hoặc IAP | `add-afk-rewards`, `add-monetization-hooks` |
| Cuối lượt thẻ chạy lần lượt, rồi đánh thường; có ultimate thì ra ultimate thay đòn thường | `add-card-battle` |
| Kết thúc khi một bên hết tướng, không còn hồi sinh (thẻ hồi sinh) | `add-card-battle` (hồi sinh) |
| 5 hệ Ngũ hành xung khắc | `add-card-battle`, `add-world-islands` |
| Máy pachinko: hạt EXP (cấp người chơi = cấp tướng), thẻ để tiến hóa, ô rương, tối đa 20 hoặc 30 bi một lần, nút X nhân thưởng, thẻ ×X khác nhau, Huyền thoại lần đầu ở mốc bi rồi cực hiếm | `add-pachinko-machine`, `add-hero-roster` |
| Side meta: huy hiệu hệ (thắng 5 hoặc 10 ải boss, +5% cho tướng cùng hệ, càng về sau càng khó) | `add-element-badges` |
| Side meta: đá tiềm năng (từ hòm pachinko, 4 ô mỗi tướng, khai phá tốn đá, hiếm ra ít, side quest đánh boss cày đá phải tự chơi) | `add-potential-stones` |
| Side meta: trang trại (8 tướng, năng suất và thời lượng theo sức tướng, nghỉ 15–60 phút, không dính tới ải) | `add-hero-farm` |
| Bố cục scene kiểu Clash of Critters, đảo lớn chia hệ, phong cách vẽ tay (chốt sau bản web) | `setup-unity-foundation`, `add-world-islands` |

## Đã chốt (2026-10-31)

- Người chơi luôn đi trước mỗi hiệp.
- Phật Tâm đổi thành hồi sinh 35% máu (chủ dự án để Claude quyết).
- Ô tiềm năng mở theo sao; chỗ làm trang trại mở theo cấp.
- Hang Tiềm Năng 3 lượt thắng mỗi ngày, +1 bằng quảng cáo (chủ dự án để Claude quyết).
- Không bán bi, đá tiềm năng, lượt quay máy bi.

Chốt thêm khi trả lời câu hỏi còn mở (2026-10-31, lượt 2):
- Choáng: mất trọn lượt (không chọn thẻ, không đổi tướng, không đánh; mana đầu lượt vẫn nhận). Đã sửa ở web và Unity.
- Trận Đảo Thổ dài 10–14 hiệp: chấp nhận.
- Máy bi: 30 bi mỗi đợt từ cấp 15; mốc Huyền thoại khi đã có Đại Sư Cà Sa thì cho 15 bản sao thẻ; chưa thêm thanh "hũ sắp đầy".
- Rương ra thẻ: chỉ cho tướng đã có (giữ như đang làm).
- Bảng tỉ lệ máy bi của web đọc số đo (đã sửa).
- Mở Đền Huy Hiệu sau boss Đảo Thủy: để vậy, chơi thử rồi tính.
- Thử thách huy hiệu: cấp địch tiếp tục tăng theo bậc, không chặn ở cấp 30.
- Hệ chỉ có 2 tướng: sẽ thêm tướng sau. Hiệu ứng huy hiệu trong trận: để sau.
- Giữ 3 kiểu người chơi mặc định của mô phỏng.
- Duyệt các chỗ tự chọn ở tiềm năng (hút máu mọi đòn, Thứ Bảy chọn hệ boss Hang, tướng phụ Hang, rương AFK 1 đá, dải Tiềm năng) và trang trại (lưới tạm, tự xếp theo năng suất, chấm đỏ khi vừa mở, rút giữa ca vẫn nghỉ đủ).
- AFK thôi ra bi theo giờ, học cây sinh bi của Clash of Critters: thêm Cây bi trên sảnh (change `add-ball-trees`). Trang trại đổi sang ca dài như cây.
- Mục tiêu nhịp: người chơi "vừa" xong cả 5 đảo khoảng ngày 21.
- Tướng: 8 mỗi hệ (40 tướng), chọn lại theo hệ gốc aola. Danh sách ở `13_DanhSachTuong.md`, prompt ở `ArtGen/Heroes`. Dữ liệu game chưa đổi (vẫn 11 tướng).
- Tướng (2026-11-01):
  - Mỗi tướng là một dòng tiến hóa, lên sao thì đổi hình.
  - Quái thường lấy dòng 2–4 dạng, boss lấy dòng từ 3 dạng.
  - Prompt đính ảnh tham chiếu aola, GPT vẽ lại theo style riêng và đổi chi tiết.
  - Đảo Thủy xong prompt (`ArtGen/Heroes/Thuy.md`, 21 ảnh); các hệ khác chờ chọn lại. **2026-11-02:** bỏ hết file prompt cũ, làm lại (`ArtGen/Heroes/QUY_TRINH.md`, gói sinh bằng `ArtGen/Heroes/build.py`): vẫn vẽ đè lên rig aola, nét vẽ tay như bản đồ, thiết kế học từ tướng aola, vẻ chiến, viền giấy xé do shader; Giọt Sương dạng 1 là tinh linh nước hiệp sĩ tập sự (rig #7).

## Tiến độ

**Mốc 0 `setup-unity-foundation`: xong (2026-10-31).** 35/35 việc, 18 EditMode test đạt.

Chạy thử trong Unity:
1. Lần đầu (hoặc sau khi đổi dữ liệu web): menu `PokiClash/Cài đặt/1. Nhập TMP Essentials`, rồi `PokiClash/Cài đặt/2. Dựng tất cả`.
2. Mở `Assets/00 Scenes/Boot.unity`, chọn Game view `PokiClash 1080x1920`, bấm Play.
3. Đi thử tự động: `PokiClash/Thử/Đi một vòng các scene (đang Play)`; chụp 3 khung: `PokiClash/Thử/Chụp 3 khung màn hình (đang Play)` (ảnh ở `Temp/PokiShots`).

Mã nguồn:
- `Assets/01 Script/Core`: logic thuần chép từ web, không dùng UnityEngine.
- `App`, `UI`, `Game`: một assembly `PokiClash.Game`.
- `Editor`, `Tests`: công cụ và test.

Dữ liệu ở `Assets/02 Data` (JSON xuất từ web và ScriptableObject). Ảnh ở `Assets/03 Art`: ảnh gen nhập bằng menu `PokiClash/Nhập ảnh ArtGen`; chưa có thì dùng ảnh thay thế trong `Fallback/`.

**Mốc 1 `add-card-battle`: xong (2026-10-31).** 24/24 việc, 23 EditMode test đạt (luật C# khớp web ở 200 trận golden).
- Luật mới, đổi cả ở web: Phật Tâm thành "lần đầu gục: hồi sinh 35% máu"; boss của địch không hồi sinh; trận dừng ở 60 hiệp.
- Vào trận: sảnh → đảo → chạm ải → hộp chuẩn bị → Đánh. Thử nhanh: menu `PokiClash/Thử/Đánh thử ải …` (đang Play).
- Tướng hiện bằng hình aola. **2026-11-02**, chủ dự án chốt "đây là prototype": mọi bản build mang hình tướng, xem được trên máy thật. Ban đầu làm bằng `Editor/AolaDevBuild.cs` (`AllBuilds`); nay thay bằng prefab tướng (mục "Prefab tướng" bên dưới). Trước khi phát hành công khai phải tắt `PreBuildCheck.HeroArtInBuild` (spec `art-assets`).
- Dung lượng build (2026-11-02): bản build ở công ty hơn 300 MB, trong đó 262 MB là gói hình aola (84 dạng, 5.350 PNG) chép vào StreamingAssets mà APK để không nén. Nay bước build `AolaDevBuild`:
  - thu nhỏ mỗi hình mảnh về độ nét RenderTexture thật sự dùng (tướng cao tối đa ~301 điểm trong RT 1024, chừa ×1,25), chỉnh ma trận anim.json theo; điểm ảnh còn 22%, RAM trên máy giảm theo;
  - ghi PNG 256 màu (`Editor/PalettePng.cs`, `ImageScale.cs`, `AolaPngPack.cs`; cache `Library/PokiAolaPng`); lệch màu không thấy bằng mắt;
  - build Android gzip anim.json (17,6 → 1,7 MB).
  - Ước gói aola còn khoảng 25 MB. Kèm theo: bỏ 6 ảnh nền thay thế trùng ảnh gen khỏi `ArtLibrary` và `Zone.prefab` (~5 MB); atlas động hai phông lớn 2048 → 1024 (đã bật nhiều atlas). APK ước từ 103 MB (bản 21:46) còn khoảng 60–65 MB.
  - **Lỗi gây crash, đã sửa 2026-11-02:** Pangolin cũng bị hạ 2048 → 1024 bằng tay mà vùng xếp chữ (`m_FreeGlyphRects`) còn 2047, nên TMP ghi tràn ảnh atlas khi thêm chữ. Unity Editor crash hai lần, và test phông crash ở batchmode. Đã sửa về 1023. `Editor/FontAtlasGuard.cs` tự soát và tự sửa phông lệch mỗi lần Editor nạp code; test phông kiểm trước khi thêm chữ. Sau sửa: 83/83 test EditMode đạt trong Editor.
  - Chưa đổi cấu hình (cắt code, IL2CPP, gỡ package, URP): chủ dự án chốt như vậy là được. Kiểm: menu `PokiClash/Build/Kiểm tra gói tướng (build Android ra Temp)` in cỡ APK và soát đủ file; lần build đầu chậm thêm vài phút để nén.
- **Prefab tướng (2026-11-02, thay hai mục trên):** người dùng chốt hình tướng lấy từ aola phải nhập vào Unity thành prefab tướng và nén luôn, không chỉ để bên AolaRipper.
  - Menu `PokiClash/Tướng/Nhập hình tướng aola thành prefab` (`Editor/AolaImport.cs`) lấy các dạng có trong `heroes.json`.
  - Mỗi dạng ghi vào `Assets/03 Art/Heroes/Resources/<dạng>/`: atlas ASTC 6x6, chân dung, `anim.bytes` gzip, asset `AolaAnim`.
  - Mỗi tướng là prefab `Assets/04 Prefabs/Heroes/<id>.prefab`; danh mục `02 Data/HeroModels.asset` gắn vào `UiAssets.heroes`.
  - Atlas và chân dung nạp khi cần (`Resources.Load`), vì danh mục trỏ thẳng thì mọi ảnh tướng vào bộ nhớ lúc mở game.
  - Nén:
    - hình mảnh thu về độ nét RenderTexture 1024 thật sự dùng; hình không có trong dáng đứng (tư thế đánh, hiệu ứng) thu thêm ×0,7;
    - atlas không mipmap, xếp sát (không làm tròn lên lũy thừa 2).
  - Kết quả: 45 prefab, 95/97 dạng; atlas 175 triệu điểm ảnh, ASTC 6x6 khoảng 74 MB trước khi build nén thêm. Lần nhập thử đầu (×1,25, mipmap, `PackTextures`) ra 516 triệu điểm ảnh.
  - So với gói PNG 256 màu cũ (~25 MB trong APK): APK lớn hơn, nhưng mỗi tướng đang hiện chỉ tốn ~0,45 byte/điểm ảnh bộ nhớ đồ họa, thay vì 4 byte khi giải PNG ra RGBA. Muốn APK nhỏ nữa thì đổi ASTC 6x6 sang 8x8 (bớt ~44%, mép nét mờ hơn).
  - `AolaDevBuild` thôi chép vào StreamingAssets (`Enabled = false`). `AolaDevPack`, `AolaPngPack`, `PalettePng` không còn dùng, chờ chủ dự án quyết xoá.
  - Trước khi phát hành công khai: tắt `PreBuildCheck.HeroArtInBuild`.
  - 2026-11-03: 51 prefab (thêm 6 lính, khoá `minions` trong `heroes.json`), 103/103 dạng có hình. `goc_1692` đã xuất.
  - Dạng vẽ lại `<hệ>_<id>` chưa xuất (`thuy_7`, Giọt Sương dạng 1) thì bộ nhập tạm lấy hình gốc `goc_<id>` cùng rig, tổng kết menu ghi "tạm dùng hình gốc aola". Có `reskin/thuy_7/export/anim.json` thì chạy lại menu, hình vẽ lại tự thay vào.
  - **Mảnh tự chạy (2026-11-04).** Sprite có timeline riêng (tóc, lốc nước, vệt chém, tia nổ) trước bị xuất thành một hình đứng yên. `tools/subframes.py` bên AolaRipper vẽ từng khung con, rồi `export_original.py` xuất lại `anim.json`. Từ nay `goc_batch.py` tự làm bước này. 74 dạng cần làm:
    - Đã vào Unity: `goc_1319`, `goc_1320` (Tiểu Y), cùng 41 dạng nhập ngày 2026-11-04 bằng menu `Nhập dạng aola có nguồn mới hơn bản trong project` (menu nhập thêm `goc_216`, anim không đổi). Đã so: anim trong Unity trùng bản xuất, mảnh thường không lệch; ảnh `Chụp thử prefab tướng` thì dáng đứng giữ nguyên, hiệu ứng đánh và chiêu đổi theo khung con.
    - **Còn 31 dạng chưa vẽ khung con, để làm sau** (người dùng dặn 2026-11-04): Ma Kết `goc_758 759 760`, Vây Lam `546 547 548`, Thương Lam `805 806 807`, Heo Lửa `205 206 207`, Kuba `95 96`, Đốm Lửa `2419 2420`, Pháo Tết `1370 1371`, Sư Tử Lửa `5 6`, Sóc Đá `825 826`, Hồ Lửa `307`, Chu Tước `506`, Gấu Mỏ `373`, Kỳ Lân `90`; lính `1313 1314 17 829 830`.
    - Cách làm: một tiến trình, Chrome 1 luồng (`subframes.py <parts> --threads 1`), không chạy cùng lúc Unity nhập hay biên dịch (cả máy sập 2 lần ngày 2026-11-04). Dạng 758 có hình hiệu ứng rất lớn, lần trước kẹt ở đây: xem trước rồi mới vẽ. Xong thì chạy menu `Nhập dạng aola có nguồn mới hơn bản trong project`.
    - Bản xuất mới có thể ít mảnh hơn bản cũ ở vài khung. Đó là khung con mảnh bị ẩn (SVG trống hoặc `fill-opacity 0`), trước đây vẫn hiện hình khung đầu: đúng, không phải mất mảnh.
    - Giọt Sương dạng 3 (rig pet9) có 1 mảnh tự chạy: khi ghép `thuy_9` nhớ làm bước này.
    - Chân dung: `export/portrait.png` ở AolaRipper ổ D không có bóng dưới chân, bản trong git (có lẽ làm ở máy công ty) có bóng. Dạng nhập lại ở máy này thì mất bóng, đúng luật "tướng không vẽ bóng". Tới 2026-11-04 còn 29 dạng có chân dung có bóng. 13 dạng nằm trong 31 dạng chờ nên sẽ tự hết khi nhập. 16 dạng còn lại phải nhập lại riêng chân dung: `goc_76 77 78 1617 22 23 24 182 183 31 33 4`, `monk_500 2010 boxer 2217`.
  - Ảnh soi từng dạng: menu `PokiClash/Tướng/Chụp thử prefab tướng` ghi vào `Library/PokiHeroShots`.
  - **Đảo Hỏa (2026-11-05): xong, 28/28 dạng đã vào Unity.** Máy ổ D xuất 19 dạng (Khổng Lồ Lửa, Kim Sư, Nham Thần, Hồng Liên, Giáp Long, Huyễn Viêm, Hỏa Tinh). Máy ổ E xuất nốt 9 dạng: Lân Hỏa `goc_1449 1450 2828` và 6 lính `64 65 13 14 291 292`. Sư Tử Lửa `5 6` đã có khung con từ 11-04 ở máy E nên không chạy lại.
  - **Đảo Hỏa, 2026-11-06:** Ngưu Quyền (ải 20, thay Hồ Lửa) mới thêm: `goc_412 413 414` **chưa xuất**. Máy ổ D sập lần 5 khi đang vẽ mảnh tự chạy của pet412 (chỉ 1 Chrome), nên xuất ở máy công ty: `py -3 -I tools/goc_batch.py 412 413 414`, rồi nhập prefab. `reskin/pet412_parts` ở ổ D còn dở (đừng đẩy lên, hoặc xoá trước).
    - Máy ổ D xuất bằng công cụ cũ, vì hai bản sửa lỗi xuất của máy E hôm 11-04 (`merge_timeline` bỏ alpha, tint áp hai lần) chưa đẩy lên git AolaRipper. Máy E xuất lại 19 dạng Hỏa và 23 dạng Mộc máy D xuất cùng ngày: 27 dạng đổi, 25 dạng bỏ tint áp đôi ở hàng khung con, `goc_47` và `goc_593` nhận lại alpha/blend.
    - Nhập bằng menu "nguồn mới hơn": 51 dạng (28 Hỏa, 23 Mộc), prefab mới `khong_lo kim_su nham_than hong_lien giap_long huyen_viem hoa_tinh lan_hoa` và `linh_lo lo2 nam nam2 khi khi2`. EditMode 97/97 đạt.
    - Đã chụp soi (`Chụp thử prefab tướng`): mảnh không lệch, không mất. Cột "lao xa nhất" trống ở vài dạng vì con lao ra khỏi ô chụp, đúng dáng gốc. Hiệu ứng gốc cần người dùng xem: Hồng Liên dạng 1 hóa quả trứng ở chiêu; Nham Con thành bóng tối trong cột sáng (colour transform của SWF, FFDec không vẽ); Lân Con có chữ Hán bằng lửa trên đầu ở chiêu; Lân Ngàn Năm (`goc_1450`) đứng trên vệt đất nứt đỏ đen cả lúc đứng.
    - Công cụ: `goc_batch.py` tự tìm Java (AOLA_JAVA, OpenJDK của Unity, rồi `java` trong PATH) và thư mục tạm theo người dùng; `render_chars.py` đọc được `frames.json` ghi đường dẫn tuyệt đối của máy kia (`D:\...`). Thay đổi ở AolaRipper máy E (gồm cả việc 11-04) chưa commit.
  - **Đảo Kim (2026-11-05): xong, 28/28 dạng đã vào Unity** (22 dạng của 10 tướng, 6 lính; `13_DanhSachTuong.md`, mục Kim). Máy ổ E xuất bằng `goc_batch.py`, một tiến trình, Chrome 1 luồng (người dùng dặn vẽ từng con một). Prefab mới `doc_giac phi_thuong khien_bac chien_than thiet_phu tam_kiem ung_thep kim_nghe`, lính `linh_giap linh_giap2 linh_khien linh_khien2 linh_may linh_may2`. EditMode 99/99 đạt.
  - **Đảo Thổ (2026-11-06): xong, 27 dạng mới đã vào Unity** (21 dạng của 9 tướng mới, 6 lính; Thạch Nhân có sẵn; `13_DanhSachTuong.md`, mục Thổ). Máy ổ D xuất bằng `goc_batch.py` ban đêm, từng con một, Chrome 1 luồng, tiến trình ưu tiên BelowNormal, không sập. Prefab mới `lung_vuong cao_da ho_khoan phu_van hat_de rua_nui ho_kim_cuong cu_phu giap_nham`, lính `linh_khoan linh_khoan2 linh_da linh_da2 linh_ngua linh_ngua2`; menu "nguồn mới hơn": 107/108 prefab (thiếu `nguu_quyen`, goc_412–414 chưa xuất), 203/206 dạng, ASTC 8x8 khoảng 14 MB. Đã chụp soi (`Library/PokiHeroShots`): hình khớp chân dung; dạng 1 Giáp Nham (1273) ở khung trúng đòn của chiêu là một quả cầu đỏ (đoán là chiêu cuộn áo choàng thành cầu, dạng 2 cuộn áo quanh người), chưa xem trong trận. EditMode 99/99 đạt.
    - **Bộ lọc Flash nay có trong game:** `bake_filters.py` bên AolaRipper nướng glow, blur, colour matrix (trước đây Unity bỏ, mất quầng sáng; cả 28 dạng Kim đều dùng, Kim Nghê 1.319 lần đặt glow). Glow tách thành hình quầng nằm dưới hình gốc, hình gốc dùng chung; `AolaImport` thu nhỏ thêm hình quầng (`fx/*_q*.png`, ×0,3) và hình đã mờ (`fx/*_b*.png`, ×0,6). Atlas 28 dạng Kim 58,7 triệu điểm ảnh, ASTC 8x8 khoảng 14 MB (Hỏa 28 dạng không có quầng: 50,4). Lần nướng cả hình đầu tiên ra 80,1.
    - **Mảnh rỗng, mảnh nhân màu hai lần:** FFDec nướng colour transform của lần đặt vào SVG khung, nên mảnh mờ dần hiện ra bị bỏ (đốm sáng chiêu Thiết Phủ 1533, 88 lần đặt; mảnh ở dáng đứng của Nóc Sắt 1061), mảnh có alpha 0,02 ở khung đầu thành vô hình (Kim Nghê 1841). `unbake_cx.py` vẽ lại 126 mảnh; `export_original.py` thôi nhân alpha lần nữa cho hình khung con. Đã so khung với ảnh render sẵn của aola (`fightassets/bitmap`): Kim Nghê, Thiết Phủ, Bọ Cạp 678, Ưng Thép 1696 khớp.
    - **Các đảo khác chưa có bộ lọc:** dạng Thủy, Hỏa, Mộc, Thổ vẫn xuất cách cũ (không quầng sáng, còn lỗi nhân màu). Muốn có thì chạy cho từng dạng `unbake_cx.py`, `export_original.py`, `bake_filters.py`, `portrait_png.py` rồi menu "nguồn mới hơn"; ước atlas tăng khoảng 15–20% (đoán theo Kim so với Hỏa, chưa đo).
    - Chân dung Chiến Giáp (`goc_122`) còn vệt bóng dưới chân: `portrait_png.py` không nhận ra bóng của dạng này.
  - **Bản đồ dài đảo Kim (2026-11-05): xong.** Gói GPT `ArtGen/Islands/gui_gpt/zone_kim_70/` (`build_zone70_kim.py`), 3 đoạn đã duyệt, ghép, dò đường và xuất: `Assets/03 Art/Islands/zone_kim.png` 1024 × 4288, khoá `zone_kim` trong `island_anim.json`, khối `kim` trong `zones.json` (path, stops, plates). Đã Nhập dữ liệu và chạy tour mới "PokiClash/Thử/Đảo Kim 70 ải…" (ảnh `Temp/PokiShots/420–429`): bệ tướng, chấm ải nằm trên đường, bảng chặng, hộp chuẩn bị đúng. Nền trận đảo Kim chưa có (log "Chưa có ảnh 'battle_kim'", dùng ảnh thay thế).
- **Thêm 5 tướng Thủy (2026-11-02):** người dùng chọn 7 hình aola cho kịch bản đảo Thủy. Hai con đã có: 远古灵龟 = Huyền Vũ, 万钧 = Vạn Quân (dạng 2 của Lam Quân, người dùng đánh dấu BOSS). Năm con mới:
  - Mi Nhi (983–984);
  - Ma Kết (758–760);
  - Vây Lam (546–548);
  - Thương Lam (805–807);
  - Kuba (94–96).

  Tên, độ hiếm, chỉ số là tạm; thẻ mượn của Tiểu Y / Y Trạch. Dữ liệu còn 45 tướng (Thủy 13). Xếp tướng vào ải đảo Thủy: session viết lại hệ thống ải đang làm.
- Số đo đảo Thổ và nhịp trận: `openspec/changes/add-card-battle/design.md`, mục "Kết quả đo".

**Mốc 2 `add-hero-roster`: xong (2026-10-31).** 12/12 việc, 31 EditMode test đạt (chỉ số 11 tướng, thẻ rơi từ rương, mảnh khớp web).
- Scene Tướng: lưới 3 cột, chấm đỏ việc chờ, hộp chi tiết có ô xem 4 clip, nâng thẻ, tiến hóa, cho vào/bỏ khỏi đội, nơi rơi mảnh.
- Sổ thẻ: cách xếp thẻ, trọng số rút theo độ hiếm, thẻ khoá theo cấp.
- Sổ tay có "Bảng thử (tua nhanh)" như bản web, chỉ hiện trong Editor và bản Development.
- Đội trống thì hộp chuẩn bị trận không cho Đánh.

**Mốc 3 `add-world-islands`: xong phần code (2026-10-31).** 17/19 việc, 36 EditMode test đạt (thưởng ải, tặng tướng, rương mốc khớp web).
- Sảnh: bảng tên 5 vùng có độ khó và tiến độ, mây trôi, mũi tên đảo gợi ý, Làng Máy Bi, 3 công trình side meta phác chì kèm điều kiện mở, hàng nút tròn, màn giới thiệu lần đầu.
- Đảo hệ: cuộn dọc, 8 ô ải theo trạng thái, nét chấm vàng, sticker đội trưởng, rương mốc, khung ải tiếp theo, hộp chuẩn bị trận (đội 3 ô, kho tướng có mũi tên khắc hệ).
- Còn 2 việc chờ ảnh đảo (Canva và ArtGen/Islands): đưa ảnh vào và soi lại toạ độ.
- Người chơi mới đi trọn Đảo Thủy bằng Tự chơi ×3: thua 10 lần trước khi qua 8 ải khi chỉ thả bi ở máy bi giữ chỗ (10 EXP mỗi bi). Đo lại ở mốc 4 với máy thật: 8 thắng, 2 thua, xong đảo ở cấp 7, đã thả 156 bi.

**Mốc 4 `add-pachinko-machine`: xong (2026-10-31).** 13/14 việc, 41 EditMode test đạt (6.000 bi: tỉ lệ từng ô lệch dưới 1 điểm phần trăm so với web, không bi nào kẹt; 600 lần mở rương khớp từng thưởng).
- Máy vẽ trên uGUI (design ghi camera riêng): khung giấy viền mực; đinh, nấm, cốc, ô vẽ một lần vào texture; bi và hiệu ứng nằm trên canvas con.
- Cột cược ×1…×10 khoá theo cấp; "Thả bi" (chạm hoặc giữ); "Thả liền 20/30"; khay "Rương chờ" (lưu trong bản lưu); thanh mốc 300 bi; bảng "Tỉ lệ" đọc số đo mô phỏng do `export_data.ts` ghi vào `balance.json`.
- Đổi ở web: `maxPerDrop` 20, từ cấp 15 là 30; mốc Huyền thoại khi đã có Đại Sư Cà Sa thì cho 15 bản sao thẻ Huyền thoại.
- Thử: menu `PokiClash/Thử/Máy bi: thả ×1 và ×3, mở rương (đang Play)`. Còn đo FPS trên máy Android thật.

**Mốc 5 `add-afk-rewards`: xong (2026-10-31).** 11/11 việc, 45 EditMode test đạt (golden AFK 42 bước khớp web từng giá trị).
- Logic viết ở web trước (`Web/src/core/afk.ts`, hộp AFK web cũng có rương và tăng tốc), chép sang `Core/Afk.cs`. Bản lưu thêm khoá `afk` (bản lưu cũ tính tiếp từ `afkSince`).
- Đồng hồ theo đoạn: tăng tốc ×2 trong 2 giờ, chặn 12 giờ, lùi giờ máy thì bỏ qua đoạn đó.
- Rương AFK: 3 giờ/rương, khay 4, đếm 2 giờ từng cái, rương kế đếm ngay khi rương trước đếm xong; bộ đếm rương không về 0 khi nhận bi.
- Hộp AFK: Nhận, Nhận ×2, Mở ngay (4 lượt/ngày), Tăng tốc ×2 (3 lượt/ngày, xám khi giờ AFK đã đầy). Quảng cáo qua `IRewardAds`, bản thử là quảng cáo giả lập 3 giây có nút "Bỏ qua".
- Thử: menu `PokiClash/Thử/AFK: tua giờ, nhận, rương, tăng tốc (đang Play)`; Sổ tay có "Tua AFK 1 giờ / 8 giờ".

**Mốc 6 `add-balance-tools`: xong (2026-10-31).** 11/12 việc, 49 EditMode test đạt.
- Cửa sổ Editor `PokiClash/Cân bằng` (không cần Play): tab Trận (một ải / một đảo / 40 ải, đội, cấp, sao, cấp thẻ, phần cộng side meta, CSV), tab Máy bi (độ rộng ô, tỉ lệ, giá trị rương, EXP / bi hoàn / thẻ mỗi bi, cảnh báo bi hoàn > 0,5, ghi tỉ lệ vào asset), tab Tiến độ (3 kiểu người chơi × 30 ngày). Menu `PokiClash/Cân bằng nhanh/...` chạy không mở cửa sổ.
- Bảng 40 ải × 5 mức cấp của Unity khớp từng ô với `npm run sim -- battle` (đã so 50 trận mỗi ô: 200/200 ô trùng; test EditMode so 6 trận mỗi ô với golden `sim.json`). 10.000 trận mất khoảng 7 giây.
- Sổ tay bản dev (Editor và Development Build): Bảng thử, Chỉnh số (16 hệ số, nút − / +, "Về số gốc"), Máy tự chơi 100 trận. Sổ tay cuộn dọc.
- Ghi trận: mỗi trận thêm một dòng vào `Logs/tran.csv` của project (máy thật: `persistentDataPath/Logs`).
- Kiểm tra trước build: file trong `App/Dev` phải bọc kín `#if UNITY_EDITOR || DEVELOPMENT_BUILD`; menu `PokiClash/Biên dịch thử bản phát hành` biên dịch script người chơi không Development.
- Web: `runBattle` nâng giới hạn vòng lặp 400 → 2000 (như golden); đội mẫu theo đảo chuyển vào `src/core/sim.ts` (`SIM_TEAMS`) và xuất sang `balance.json`.
- Mô phỏng tiến độ 30 ngày (máy + 15%, AFK và máy bi theo luật hiện tại): chăm cấp 30 ngày 3, xong cả 5 đảo ngày 3; vừa cấp 30 ngày 7, xong Đảo Thổ ngày 7; ít cấp 27 ngày 14, xong Đảo Thổ ngày 22. Bi AFK chiếm phần lớn (vừa: 51.152 bi AFK so với 5.797 bi từ ải).

**Mốc 7 `add-element-badges`: xong (2026-10-31).** 11/12 việc, 53 EditMode test đạt (đội địch 200 trận thử thách, chỉ số có phần cộng, trận thật và tiến độ khớp web).
- Logic viết ở web trước (`src/core/badges.ts`; web thêm `StatMods` cho chỉ số tướng như Unity), chép sang `Core/Badges.cs`. Bản lưu thêm khoá `badges`.
- Scene `Badges` (đã thêm vào Build Settings): 5 bệ theo hệ, danh sách trận của bậc, hộp chuẩn bị trận dùng chung, kết trận riêng (bi, tiến độ, hộp huy hiệu, rương). Sảnh: Đền tô màu khi mở, chấm đỏ khi có dãy mới. Màn Tướng: icon huy hiệu cạnh nhãn hệ, chỉ số đã gồm phần cộng.
- Công cụ: tab "Huy hiệu" ở cửa sổ Cân bằng và `npm run sim -- badges` (hai bên ra cùng số).
- Đo bằng máy tự chơi (đội mẫu của đảo cùng hệ): trận cuối mỗi bậc (3 tướng, boss là tướng hiếm nhất) gần như không thắng ở cấp kỳ vọng, nhất là dãy Thổ (boss Đại Sư Cà Sa Huyền thoại: bậc Bạc 5–18%, Ngọc 0–4%). Bậc Kim Cương dãy Thổ có địch cấp 33–38, quá cấp tối đa 30. Huy hiệu +20% cho mọi tướng nâng tỉ lệ thắng ở cấp đề nghị thấp nhất: Thủy 49% → 69%, Thổ 59% → 73%.
- Còn ảnh gen huy hiệu, nền đền, công trình đền (huy hiệu đang vẽ bằng code).

**Mốc 8 `add-potential-stones`: xong (2026-10-31).** 11/12 việc, 58 EditMode test đạt (khai phá, trần, hiệu ứng đầu trận, trận thật, Hang khớp web).
- Logic viết ở web trước (`src/core/potential.ts`, `data/potential.ts`; web thêm `BattleStart` trên `Member`), chép sang `Core/Potential.cs`. Bản lưu thêm `potentialStones`, `potential`, `potentialNew` (kết quả chờ chọn), `cave`.
- Rương bạc thêm 8% "1–2 đá", rương vàng 12% "2–4 đá" (dòng cũ giữ trọng số tương đối), rương AFK 5% "1 đá".
- Hộp chi tiết tướng có dải Tiềm năng, mở hộp khoá ô / khai phá / so sánh cũ-mới. Scene `Cave` (đã thêm vào Build Settings): hệ boss theo thứ, 4 tầng, 3 lượt thắng mỗi ngày, "+1 lượt" (quảng cáo giả lập).
- Công cụ: tiềm năng không / trung bình / trần ở tab Trận; menu đo đảo Mộc, Thổ. Đảo Thổ cấp 21: không 62%, trung bình 61%, trần 81%.
- Sửa lỗi: cấu hình mảng lồng và nullable không qua được ScriptableObject (game chạy thì rỗng); đổi sang mảng phẳng, test asset dữ liệu kiểm tra mọi cấu hình side meta.

**Mốc 9 `add-hero-farm`: xong phần code (2026-10-31).** 9/10 việc, 60 EditMode test đạt (golden trang trại 24 bước khớp web).
- Logic viết ở web trước (`src/core/farm.ts`, `data/farm.ts`; web chưa có màn trang trại), chép sang `Core/Farm.cs`. Bản lưu thêm khoá `farm`.
- 8 chỗ, mỗi chỗ hợp một hệ (×1,25); mở khi có 3 tướng, lúc mở 3 chỗ, chỗ 4–8 mở ở cấp 8, 11, 14, 17, 20. Năng suất theo độ hiếm, cấp, sao; giờ làm 2–5 giờ; rút ra nghỉ 15–60 phút; kho mỗi chỗ giữ tối đa 12 giờ sản lượng. Sức làm tách khỏi trận.
- Scene `Farm` (đã thêm vào Build Settings): lưới 8 chỗ (chưa có ảnh đảo), Thu hoạch, Tự xếp, ×2 năng suất 1 giờ (quảng cáo); danh sách chọn tướng có bi/giờ, giờ làm, hợp hệ, nghỉ còn bao lâu. Sảnh: công trình tô màu khi mở, chấm đỏ khi có tướng hết sức hoặc kho đầy.
- Đo: trang trại 19–55 bi/ngày đầu game, 93–230 giữa game, 252–515 cuối game (vào 2–8 lần mỗi ngày), so với AFK 201–850. 30 ngày người chơi "vừa": trang trại 10.952 bi, AFK 51.050, ải 5.822.
- Thử: menu `PokiClash/Thử/Trang trại: tự xếp, tua giờ, thu hoạch, đổi ca (đang Play)`; Sổ tay bản dev có "Tua trang trại 2 giờ".

**Mốc 10 `add-monetization-hooks`: xong phần code (2026-10-31).** 11/12 việc (còn gắn SDK thật), 68 EditMode test đạt.
- Logic viết ở web trước (`src/core/ads.ts`, `data/ads.ts`), chép sang `Core/AdGate.cs`. Mọi quảng cáo đi qua `Ads.Show(chỗ đặt)`: giới hạn mỗi ngày theo spec (Nhận ×2 không giới hạn; Mở ngay 4; Tăng tốc AFK 3; ×2 trang trại 3; +1 lượt Hang 1), xem xong mới trừ lượt, bỏ ngang không trừ, lùi giờ máy không mở lại lượt. Bộ đếm riêng của AFK, trang trại, Hang bỏ đi.
- Bản lưu lên v3 (web và Unity), có bước di chuyển: bộ đếm quảng cáo cũ dồn về `ads`; file `save_v2.json` của bạn sẽ tự chuyển lên v3 khi mở game, bản cũ giữ thành `.bak`.
- Sổ tay có mục "Gói hỗ trợ": Thẻ Phiêu Lưu 30 ngày (bi AFK ×1,5, khay 5 ô, rương mở 1 giờ; mua tiếp thì cộng dồn hạn) và Bỏ quảng cáo (nhận thưởng ngay, vẫn theo giới hạn mỗi ngày). Không bán bi, đá, lượt quay; test rà danh sách gói.
- Quảng cáo giả lập và cửa hàng giả lập chuyển vào `App/Dev` (chỉ Editor và bản Development). Bản phát hành chưa gắn SDK thì nút quảng cáo và mục gói ẩn.
- Thử: menu `PokiClash/Thử/Gói hỗ trợ: Thẻ Phiêu Lưu, hết lượt quảng cáo, Bỏ quảng cáo (đang Play)`; Sổ tay bản dev có "Đặt lại lượt QC", "Bỏ gói đã mua".

**Sau mốc 10: chốt câu hỏi, change `add-ball-trees` (2026-10-31).** 70 EditMode test đạt.
- Choáng mất trọn lượt; golden trận xuất lại, Unity khớp web.
- **Cây bi** trên sảnh (cạnh Trang trại):
  - 5 cây, cây 1 mở khi qua ải 1, cây 2–5 khi qua boss Thủy, Hỏa, Kim, Mộc;
  - mỗi cây 5 bi/giờ, chứa 50, đầy thì ngừng; "Hái", "Hái ×2" (quảng cáo, 3 lần/ngày);
  - Thẻ Phiêu Lưu tăng cây ×1,5 (cả tốc độ và sức chứa).
- **AFK** chỉ còn mảnh tướng, rương AFK, tăng tốc; nút "Nhận mảnh". Bỏ "Nhận ×2".
- **Trang trại:** ca 8 giờ (+1 giờ mỗi sao), kho 10 giờ, 2 bi/giờ gốc, không tăng theo cấp. Đo:

  | Giai đoạn | Trang trại (bi/ngày) | Cây bi (bi/ngày) |
  |---|---|---|
  | Đầu game | 68–149 | 159–215 |
  | Cuối game | 284–537 | 399–539 |

- Đường cong cấp vào cấu hình (`expBase` 40, `expPow` 1,35, chưa đổi số). Menu mới `PokiClash/Cân bằng nhanh/Quét nhịp: EXP lên cấp, cây bi, trang trại`.
- **Nhịp chưa đạt mục tiêu:** người chơi "vừa" vẫn xong 5 đảo ở ngày 6, dù bi thụ động 30 ngày giảm từ 62.002 xuống 37.329. Xem câu hỏi 1.
- Thử: menu `PokiClash/Thử/AFK và cây bi: tua giờ, hái, mảnh, rương, tăng tốc (đang Play)`.

**Mốc 12 `convert-to-prefabs`: xong (2026-11-02).** Chủ dự án: mọi thứ trong game là prefab, kể cả UI, runtime không sinh gì. Đã nướng một lần bằng chính code dựng cũ, code runtime chỉ gán dữ liệu vào tham chiếu kéo thả, rồi xoá code dựng: prefab giờ là nguồn gốc, chỉnh trong Editor.
- Tài nguyên vẽ bằng code đã thành asset ở `Assets/03 Art/Baked`:
  - 27 sprite giấy và mực (5 hình tướng giữ chỗ đã bỏ 2026-11-02: tướng chỉ dùng hình aola, không có thì để trống);
  - nhiễu nét rung, mặt tĩnh máy bi;
  - 18 material chữ viền, 23 tiếng WAV.
- `Assets/04 Prefabs`:
  - `Kit/`: nút 5 cỡ, khung, chip, thanh, nhãn hệ, sao, băng keo, con dấu, gợi ý, thẻ, chân dung, huy hiệu, rương, canvas;
  - `App/App.prefab` (trong `Boot.unity`);
  - `Screens/`: 11 màn, mỗi scene chức năng chỉ chứa prefab màn của nó;
  - `Dialogs/`: tờ giấy gốc `HopThoai` và các biến thể của nó;
  - `Items/`: phần lặp theo dữ liệu.
- Hộp mở từ nhiều nơi nằm trong `UiKit.dialogs`, mở bằng `App.Modals.Open<T>()`.
- `Nhập ảnh ArtGen` tự thay ảnh thay thế bằng ảnh gen cùng tên trong mọi prefab. Có thêm menu riêng `PokiClash/Đổi ảnh thay thế trong prefab`.
- Kiểm:
  - 72 EditMode test đạt, gồm test chặn `PrefabOnlyTests`: quét mã runtime, ngoại lệ duy nhất là hình aola bản dev;
  - `Kiểm tra trước build` và `Biên dịch thử bản phát hành` đạt;
  - vòng `Chạy mọi menu thử` chạy đủ 112 ảnh, không lỗi.
- Ảnh vòng thử so với ảnh trước khi đổi: phần còn lệch đều có lý do ngoài code giao diện:
  - hạt giống máy bi ngẫu nhiên, thẻ rút ngẫu nhiên;
  - AFK theo giờ thật, Hang theo thứ trong tuần;
  - mây trôi, bản lưu trôi giữa các lần chạy.
- Sửa kèm: bộ lọc nhập ảnh `ArtImporter` từng đè lên ảnh nướng.
  - Hậu quả: ép cỡ 1024 nên mặt máy bi mờ; nén ASTC trên Android; nhiễu nét rung thành Clamp nên nét gần như đứng yên; danh mục ảnh lẫn sprite nướng.
  - Nay `ArtImporter` bỏ qua `Baked/`, cách nhập đã đặt lại.
  - Nét rung giờ đúng như bản gốc, nên ảnh chụp từ 2026-11-01 lệch khoảng 1% ở viền giấy.

**Sau mốc 12: thanh mốc tiến hóa (2026-11-02).** Người dùng: lấy đủ các dạng tiến hóa; nhận hoặc thu phục tướng thì ở dạng thấp nhất; hộp chi tiết tướng có một thanh dưới tướng thể hiện các mốc tiến hóa.
- Hình: xuất đủ 83 dạng aola (xem `13_DanhSachTuong.md` mục 6).
- Nhận tướng: tướng chưa có luôn ở sao 1 nên mở khóa (khởi đầu, tặng, đủ mảnh, mốc Huyền thoại) là dạng 1; test `RosterTests.TuongMoiNhan_ODangThapNhat` chặn.
- Hộp chi tiết: `EvolutionStrip` (hàng `thanh_tien_hoa` dưới hàng ô xem của `ChiTietTuong`, dựng bằng menu `PokiClash/Prefab/Thêm thanh tiến hóa vào ChiTietTuong`): mỗi dạng một mốc, chia đều trên thanh (mốc cuối ở cuối thanh: dòng 2 dạng có mốc 2 ở cuối, người dùng chốt), dưới mốc ghi sao bắt đầu (1, 3, 5), chân dung, tên dạng; thanh là tiến độ tới dạng cuối (`EvolutionStrip.Fill`, test `ThanhTienHoa_MocCuoiOCuoiThanh`); dạng chưa tới là bóng sẫm; dòng 1 dạng có dòng ghi chú. Nằm dưới sân khấu của bố cục mới. Chỉ làm ở Unity, bản web chưa có.
- Kiểm: menu `PokiClash/Thử/Thanh tiến hóa: chụp hộp chi tiết ở các mốc (đang Play)` chụp `Temp/PokiShots/evo_*.png` (Giọt Sương sao 1, 3, 5; Tiểu Y sao 4; Kiếm Linh; Huyền Vũ chưa có; lưới Tướng), đã soi đủ; EditMode 82/82 đạt.
- Vào Play không reload domain (người dùng, 2026-11-02; menu `PokiClash/Cài đặt/3. Play không reload domain`, có trong "Dựng tất cả"): bớt khoảng 4,5–5 giây mỗi lần Play, vẫn reload scene. Static runtime có thể đổi được trả về trong `ResetStatics` ([RuntimeInitializeOnLoadMethod(SubsystemRegistration)]) của App, MachineScene, ZoneScene, NotebookDev, SafeArea; thêm static mới thì trả về cùng cách.
- Chụp qua MCP khi Editor không được focus: Unity chỉ chạy khung hình khi có yêu cầu MCP, nên phải gọi đều (ví dụ đọc `editor/state` mỗi giây) trong lúc chờ; `WaitForEndOfFrame` không tới, menu này tự render camera thay vì chụp màn hình.

**Sau mốc 12: hộp chi tiết tướng kiểu sân khấu (2026-11-02).** Người dùng gửi ảnh màn chi tiết tướng của Clash of Critters, muốn học bố cục: tướng là trọng tâm, việc nuôi tướng đẩy vào hộp con. Hộp cũ dài kín màn, thêm thanh tiến hóa là tràn.
- `ChiTietTuong` từ trên xuống:
  - sân khấu rộng hết hộp (cao 620): ô xem 520 (trước 400), 4 nút clip dưới chân; góc trên trái là hệ + tên, sao + huy hiệu + độ hiếm, danh hiệu; góc trên phải là dòng tiến hóa;
  - thanh mốc tiến hóa;
  - hàng 4 chỉ số (icon, nhãn, số), dòng "Ở cấp n, sao m" ở đáy khung;
  - khung mảnh và nơi rơi (tướng chưa có);
  - 3 thẻ riêng cỡ mini; chạm thẻ mở `ChiTietThe` ở cấp hiện tại; dưới thẻ một chỗ chung: nút "Lên cấp n" khi đủ bản sao, không thì thanh bản sao, hoặc "Cấp tối đa";
  - dòng điều kiện tiến hóa (hoặc "Đã tiến hóa tối đa"), hàng nút Tiềm năng (`mo_tiem_nang`, nhịp phồng khi còn kết quả khai phá chưa chọn), Tiến hóa, Cho vào / Bỏ khỏi đội.
- Bỏ: dải Tiềm năng (`PotentialStrip` đã xoá; các ô dòng xem trong hộp Tiềm năng), khung tiến hóa, chữ "Thẻ riêng của tướng".
- `ChiTietThe`: dòng ghi chú nay theo thẻ (thẻ chung "không lên cấp"; thẻ riêng ghi cấp n/5 và cách lên cấp).
- Đổi prefab bằng một menu dựng chạy một lần, đã xoá menu sau khi chạy; prefab là bản gốc. Đã chạy menu thử Tướng và Tiềm năng: không lỗi, ảnh đúng.
- Chưa làm (bước sau): mũi tên ‹ › lướt tướng trong hộp; bong bóng "Tiến hóa được!" trên đầu tướng; hạng chữ cho chỉ số (cần thang ngưỡng, làm ở bản web trước).

**Sau mốc 12: sảnh và đảo hệ vẽ tay (2026-11-02).** Người dùng gen ảnh đảo bằng GPT theo `ArtGen/Islands/PROMPTS.md` (nét bút chì trên giấy như UI).
- **Sảnh:**
  - `ArtGen/Islands/compose_islands.py` ghép 6 đảo gen rời thành một đảo lớn liền khối, bờ tự nhiên (thêm vùng mới: gen một đảo, thêm một dòng);
  - menu `PokiClash/Prefab/Đảo sảnh: ghép ảnh, kéo, mây viền` đưa vào `Screens/Hub`;
  - sảnh kéo được (`HubPan`, quá giới hạn thì bật về), ra rìa là vành mây che chỗ cho các đảo sau.
- **Đảo hệ:**
  - bản đồ dọc GPT gen, đảo kín bề ngang màn, cuộn dọc;
  - script dò vòng tròn ải trên ảnh làm `ZONES[].nodes` (đã chép vào bản web, xuất, nhập); biển lặp cuộn theo bản đồ;
  - bản web vẫn vẽ khung 9:16 nên đường ải trên web dồn vào giữa.
- **Bệ ải** (học ảnh màn ải của một game pet người dùng gửi):
  - mỗi ải là `Items/BeAi` (ZoneNode, dựng bằng menu `PokiClash/Prefab/Bệ ải (BeAi)`), thay nút tròn `Items/NutAi` (đã xoá);
  - bệ đất theo đảo (boss: bệ to, viền đá, vòng vàng; ảnh vẽ bằng script);
  - tướng chính của ải đứng to trên bệ, ải chưa mở là bóng sẫm;
  - bảng tên phía ngoài khúc cua: số ải, khoá, dấu qua, vương miện, tên tướng, cấp;
  - vầng sáng nhịp ở ải đang đánh, tướng mình đứng bên kia bệ.
- Chưa làm:
  - ~~đặt sheet phần động lên sảnh và đảo~~: đã làm (`IslandAnim`, lớp `dong` dưới ảnh đảo sảnh và ảnh bản đồ; khói, lửa, bánh răng, chuông, xoáy nước, bọt, lấp lánh, lá, gió, sóng, đốm lửa chạy dọc dung nham, gợn nước chạy dọc suối);
  - đảo 12 ải (đang cố định 8 ở nhiều chỗ, xem `ArtGen/Islands/PROMPTS.md`);
  - bệ vẽ bằng GPT nếu muốn đẹp hơn.

**Sau mốc 12: ô đội mở theo tiến trình, bể tướng (2026-11-02).** Người dùng chốt:
- lúc đầu chỉ mang 1 tướng;
- đánh tới đảo thứ 2 mở ô 2, tới đảo thứ 4 mở ô 3. Hiểu là: xong 1 đảo (8/8 ải, đảo nào cũng được) mở ô 2, xong 3 đảo mở ô 3.

Đã làm:
- **Luật:** `TEAM_SLOT_ZONES = [0, 1, 3]`, `teamSlots()` trong `Web/src/core/progression.ts`; chép sang `Progress.TeamSlots`. Test `ZoneTests.ODoi_MoTheoSoDaoDaXong`.
- **Vào trận** chỉ mang đủ số ô đã mở (web `battleScreen`, Unity `BattleController`), nên bản lưu cũ có 3 tướng vẫn đúng luật. Nút "Cho vào đội" ở màn Tướng cũng giới hạn theo số ô.
- **Hộp Chuẩn bị trận (Unity):**
  - ô chưa mở hiện "Khoá · xong n đảo", chạm thì báo điều kiện;
  - chạm ô đã mở thì bật bể tướng `Dialogs/ChonDoi` (TeamPickerDialog, dựng bằng menu `PokiClash/Prefab/Hộp chọn đội (ChonDoi)`): chọn một lần đủ đội, số trước tên là thứ tự ra trận, có mũi tên khắc hệ, "Xong" trả đội về;
  - lưới kho tướng cũ trong hộp để ẩn.
- **Bản web:** ô khoá và giới hạn chọn theo số ô; vẫn chọn ngay trong hộp, chưa có bể tướng.
- **Chưa tính:** mô phỏng cân bằng (sim.ts, ProgressSim, cửa sổ Cân bằng) vẫn cho đội 3 tướng, chưa mô phỏng giai đoạn đầu chỉ 1 tướng. Người chơi mới đi Đảo Thủy bằng 1 tướng: cần xem lại độ khó Đảo Thủy (nhất là boss 3 dạng ải 8).
  - Menu thử "Người chơi mới đi trọn Đảo Thủy" sau luật mới (máy tự đánh, 30 lượt): 3 thắng, 27 thua, kẹt ở ải 4 (mini boss), cấp 3. Chờ người dùng chọn cách cân lại.

**Sau mốc 12: boss tiến hóa và tướng trên nút ải (2026-11-02).** Người dùng: các mốc ở màn đảo phải hiện tướng chính đứng ở trên; ải boss chỉ có 1 boss, boss có thẻ tiến hóa riêng (dạng đầu gần chết thì lên dạng sau, hồi máu; dạng đầu yếu, mạnh dần). Làm ở web, xuất JSON và golden, chép sang C#.
- **Tướng trên nút ải:** mỗi nút có tướng chính của ải đứng trên, chân khuất sau mép nút; ải chưa mở thì xám mờ.
  - Chọn tướng (`stageLead` / `Teams.StageLead`): boss; không có thì địch cấp cao nhất; bằng cấp thì độ hiếm cao hơn.
  - Hình theo sao của địch; boss tiến hóa hiện dạng 1 (`enemyFormStar`).
  - Sticker đội trưởng ở ải đang đánh dời ra xa hơn để khỏi đè. Unity dùng lại prefab `DoiTruongDao` (tắt nhún), đặt ở lớp đường.
- **Ải boss (ải 8):** bỏ lính đi kèm, chỉ còn boss có cờ `evo` (`StageEnemy.evo`, `Member.evo`). Mảnh rơi giữ như cũ, kể cả mảnh của lính đã bỏ (Hỏa: Bồ Đề; Kim: Bọ Ngựa). Mini boss ải 4 không đổi.
- **Thẻ Tiến Hóa** (`boss_evo`, thẻ riêng thứ 121, bị động, không theo cấp thẻ): "Khi máu dưới 25%, nếu còn dạng sau: tiến hóa, hồi đầy máu, máu và Công tăng."
  - Kích cả khi dính đòn chí tử (không gục, lên dạng sau). Xoá bỏng, choáng; bị động "máu thấp" của tướng dùng lại được.
  - Sân trận hiện chữ "Tiến hóa!", đổi hình, đổi tên dạng trên bảng tên.
- **Chỉ số theo dạng** (`CFG.bossEvoHp` 1,5, `bossEvoAtk` 0,1):
  - máu các dạng cộng lại bằng 1,5 lần máu boss (gánh phần lính đã bỏ), chia theo tỉ lệ 1 : 2 : … : n. Dòng 3 dạng: ×0,25 / 0,5 / 0,75; dòng 2 dạng: ×0,5 / 1; dòng 1 dạng: ×1,5, không tiến hóa;
  - Công dạng cuối đủ, mỗi dạng trước kém 10%;
  - khi tiến hóa, máu tối đa và Công nhân theo tỉ lệ hai dạng, nên phần cộng từ thẻ (Bánh Bao) vẫn giữ.
- **Hộp chuẩn bị:** boss tiến hóa hiện cả dòng dạng; web có thêm dòng mô tả thẻ.
- **Máy tự chơi** (200 trận mỗi ô; tỉ lệ thắng ải 8 ở 5 mức cấp, trước → sau):

  | Đảo | Boss (số dạng) | Trước | Sau |
  |---|---|---|---|
  | Thủy | Mập Răng Cưa (3) | 0 / 0 / 8 / 43 / 65 | 0 / 0 / 5 / 42 / 69 |
  | Hỏa | Pháp Luân (1) | 1 / 11 / 42 / 68 / 82 | 5 / 13 / 41 / 65 / 81 |
  | Kim | Sói Linh Thép (2) | 28 / 48 / 71 / 86 / 94 | 37 / 53 / 73 / 88 / 94 |
  | Mộc | Giác Long Gỗ (2) | 68 / 81 / 95 / 98 / 100 | 63 / 81 / 91 / 96 / 100 |
  | Thổ | Cà Sa (1) | 9 / 14 / 27 / 41 / 47 | 2 / 2 / 7 / 18 / 16 |

  - Thổ khó hơn hẳn: boss Huyền thoại gánh 1,5 lần máu, còn lính cũ (Võ Sư) rất yếu. Thử hệ số 1,4 thì 4 đảo kia dễ hơn trước mà Thổ chỉ lên 22%, nên giữ 1,5.
- **Còn mở:**
  - Hỏa (Pháp Luân) và Thổ (Cà Sa) là dòng 1 dạng, chưa tiến hóa được; Kim, Mộc chỉ tiến hóa 1 lần. Theo luật "boss lấy dòng từ 3 dạng", khi chọn lại tướng các đảo này thì cơ chế tự chạy đủ.
  - Đảo Thủy đã chọn boss ải 8 là Huyền Vũ (bảng ở `13_DanhSachTuong.md`), dữ liệu vẫn là Mập Răng Cưa (việc 9 của file đó).
  - Mini boss ải 4 có tiến hóa không.
  - Ải 8 Đảo Thủy khi chỉ mang 1 tướng (luật ô đội ở mục trên): Giọt Sương một mình thắng 0% ở cấp 7 và cấp 10, 7% ở cấp 14 (300 trận). Đội 3 tướng (Giọt Sương, Võ Sư, Nữ Hoa) cấp 7 thắng 40%. Lượt thua điển hình: boss dạng cuối dùng Cuồng Nộ (+100% Công), chiêu (645) rồi tuyệt kỹ (1478), vì nộ dồn từ đòn nặng của cả 3 dạng. Cần người dùng chọn cách cân lại cùng với độ khó Đảo Thủy.
- Unity: đã chạy menu `PokiClash/Nhập dữ liệu` (HeroDb, CardDb, ZoneDb, BalanceConfig có thẻ mới, cờ `evo` và 2 hệ số); EditMode 81/81 đạt, gồm `BossTienHoa_TuDang1LenDangCuoi` và `TuongTrenNutAi_KhopBanWeb`. Đã xem trong Unity bằng menu thử mới `PokiClash/Thử/Boss tiến hóa: đảo Thủy, hộp chuẩn bị, trận ải 8`: tướng đứng trên bệ từng nút ải đúng (ải 8 là Cá Mập Con), hộp chuẩn bị hiện 3 dạng, trong trận boss lên 2 dạng, mỗi lần hồi đầy máu (523, 1046, 1569) và đổi hình, đổi tên. Dòng "… ra đòn", "đang chọn thẻ", "Hàng thẻ của …", "Tuyệt kỹ của …" trước lấy tên dòng, nay theo tên dạng (`fighterName` ở web, `Fighter.Name` ở C#). Sau sửa này EditMode 83/83 đạt. Bảng chỉnh số trong Sổ tay của Unity chưa có 2 hệ số mới (prefab nướng theo danh sách khoá).

**Hệ thống 70 ải mỗi đảo, bản thử đảo Thủy trên web (2026-11-02).** Người dùng: mỗi đảo một tướng mới thì không đủ nội dung để cày, nên mỗi đảo có 70 ải và 10 tướng. Ải tướng ở ải 1 (bóng tướng khởi đầu), 5, 10, 15, 20, rồi mỗi 10 ải. Ải xen giữa trộn ba kiểu: tướng cũ cường hóa, nhóm 2–3 con, và lính không thu thập được.
- Chi tiết, số đo: `14_HeThongAi.md`.
- Đảo Thủy có 70 ải; 4 đảo kia vẫn 8 ải.
- 6 loại lính dùng hình aola gốc mới xuất (`goc_1313`, `1314`, `16`, `17`, `829`, `830`).
- Màn đảo web: 10 mốc, chấm ải, bảng chặng.
- Máy đo: `npm run sim -- island`.
- **Đã chép sang Unity (2026-11-03).** Từ nay làm ở Unity, bản web chỉ làm khi người dùng yêu cầu. JSON và golden xuất lần cuối từ web (script ở thư mục tạm, không sửa `Web/`), có lính và `Golden/islands.json`. Màn đảo Unity có đường mòn 10 bệ, 60 chấm, 7 rương, bảng chặng `Dialogs/BangChang`. 86 test EditMode qua. Chi tiết ở mục "Unity" của file 14.
- **Đừng chạy lại `Web/scripts/export_data.ts`, `export_golden.ts` vào Assets:** hai script vẫn xuất 8 ải cũ, sẽ ghi đè mất 70 ải.

**Popup gọn, đội hình màn Tướng, lực chiến (Unity, 2026-11-03).** Người dùng: chạm ô ải chỉ hiện địch và sức mạnh của ải đó; màn Tướng hiện đội ở trên (3 con, con giữa cao hơn, vuốt qua lại); lực chiến từng tướng rõ; popup thưởng ít chữ, nhiều hình (cái gì, bao nhiêu, độ hiếm). Ảnh mẫu từ game gốc: ô tướng ghi Lv và lực chiến, chỉ số là icon kèm số.
- Chạm chấm hay bệ ải (đảo 8 và 70 ải) mở thẳng hộp Chuẩn bị trận của đúng ải đó; ải chưa mở cũng xem được, nút ghi "Chưa mở". Bảng chặng `Dialogs/BangChang` không mở nữa (prefab và code để lại).
- Lực chiến (chỉ để hiện, trận không dùng): `HeroStats.Power` = 2·√(máu × (defK + thủ)/defK × công); boss tiến hóa tính máu cả dòng. Hiện ở thẻ tướng, đội hình, từng đối thủ, dòng so "địch / mức khó / đội bạn" trong hộp chuẩn bị (Dễ ≥ 1,25 lần, Vừa ≥ 0,95, Khó ≥ 0,75, còn lại Rất khó).
- Màn Tướng: khung "Đội hình" (`TeamLineup`): 3 ô đội, tướng aola đứng động, vuốt hay chạm con bên cạnh để xoay, chạm con giữa mở chi tiết; lực chiến đội, nút Đổi đội (hộp ChonDoi), 4 chỉ số có icon của con giữa. Lưới tướng chỉ hiện tướng đã có (xếp theo lực chiến) và tướng chưa mở mà đã có mảnh (bóng sẫm, thanh mảnh); tướng chưa có mảnh nào thì ẩn. Tướng trong đội (tính theo số ô đã mở) tô vàng.
- Ô thưởng dùng chung `Items/OThuong` (`RewardTile`) ở hộp chuẩn bị, mở rương, rương mốc đảo, kết quả trận. Đã xoá 6 prefab dòng thưởng cũ (`ThuongTran`, `ThuongChip`, `ThuongManh`, `ThuongThe`, `TheRuongDao`, `TranThuong`) và class của chúng.
- Dựng prefab bằng menu `PokiClash/Prefab/Popup gọn (ô thưởng, đội hình, lực chiến)`; thử bằng `PokiClash/Thử/Popup gọn: đội hình, chạm ải, ô thưởng (đang Play)` (ảnh `Temp/PokiShots/p_*.png`). EditMode 86/86 đạt.

**Màn VS truyện tranh, dải tuyệt kỹ (Unity, 2026-11-03).** Người dùng: vào trận hiện mặt các tướng hai bên trên dưới, ngăn bằng vạch chéo kiểu showdown, như khung truyện tranh; một nền dùng chung, tướng nào có thì gen thêm ảnh mặt; dùng lại khung đó khi ra tuyệt kỹ, cắt thành hình bình hành ngang màn.
- Màn VS (`BattleIntro`, trong lớp phủ `Screens/Battle`): trang giấy, khung trên đội địch (đỏ), khung dưới đội bạn (xanh), khe chéo viền mực; mỗi tướng một ô mặt `Items/TranVsMat` (`VsFace`: tên, cấp, nhãn BOSS; mặt địch quay trái, phe mình lật quay phải); lực chiến cả đội (như hộp chuẩn bị); khung lời dẫn vàng ghi đảo, ải, tên ải; dấu VS đóng xuống giữa khe, rung. Khung trượt vào theo đường chéo, giữ 1,5 s, tách lên xuống; chạm để bỏ qua. Hình khung tính lúc chạy theo cỡ màn (`PolyGraphic`, `RayGraphic`).
- Tuyệt kỹ (`UltCutIn`): dải hình bình hành ngang giữa sân, cùng kiểu khung; mặt tướng ra chiêu to về phía phe nó, khung "Tuyệt kỹ · tên tướng", tên chiêu chữ to. Trượt vào từ phía phe ra chiêu, giữ 0,6 s, rồi mới phát clip tuyệt kỹ (thay băng rôn tuyệt kỹ cũ).
- Ảnh: nền khung (`vs_nen`, một ảnh tô màu theo phe), dấu VS (`vs_no`), mặt từng dạng tướng (`mat_<aola>`, 384 × 384, nhập ASTC 8x8 cho nhẹ APK) ở `Assets/03 Art/BattleIntro/Resources`, game nạp khi cần, chưa có thì vẽ tạm: tia bằng code, hình nổ của bộ giấy, chân dung phóng cho đầu lấp ô (hộp hình chân dung đo sẵn: `PortraitBoxes`). Gói gửi GPT: `ArtGen/BattleIntro/build.py` (lượt nền, lượt VS, mỗi dòng tiến hóa một file mặt; `--duyet` cắt nền trắng, chép vào Unity).
- Dựng bằng menu `PokiClash/Prefab/Trận: màn VS truyện tranh` (nhập thêm tướng thì chạy lại để đo hộp hình); thử bằng `PokiClash/Thử/Màn VS truyện tranh, dải tuyệt kỹ (đang Play)` (ảnh `Temp/PokiShots/vs_*.png`).

**AFK theo ải (Unity, 2026-11-03).** Người dùng hỏi sao ải đã thắng không có nút AFK, rồi chọn AFK theo ải (web giữ AFK chung).
- Ải đảo đã thắng có nút "AFK ải này" cạnh Xuất trận ở hộp chuẩn bị trận. Ải đang AFK ghi "Đang AFK", chạm thì mở hộp AFK.
- Mỗi lúc đội AFK một ải (`afk.stage` trong bản lưu). Chưa chọn thì tự lấy ải xa nhất đã qua có rơi mảnh.
- Mảnh: mỗi giờ tròn 8% ra 1 mảnh, tướng bốc theo tỉ lệ rơi của ải đó (bỏ tướng tặng); ải không rơi mảnh thì chỉ ra rương.
- Rương AFK, giới hạn 12 giờ, tăng tốc giữ như cũ.
- Đổi ải: mảnh của các giờ tròn đã dồn tính theo ải cũ và nhận luôn, phần giờ lẻ giữ lại.
- Hộp AFK ghi ải đang AFK và tướng rơi mảnh, thêm nút "Đổi ải" (sang đảo của ải đó). Bản đồ đảo có nhãn AFK dưới ải đang AFK.
- Golden `afk.json` tính lại bên Unity: 3 bước nhận đổi mảnh, thêm 6 bước đổi ải. EditMode 95/95 đạt.
- Dựng bằng menu `PokiClash/Prefab/AFK theo ải (nút, nhãn trên đảo)`; thử bằng `PokiClash/Thử/AFK theo ải: nút ở ải đã thắng, nhãn trên đảo (đang Play)` (ảnh `Temp/PokiShots/afk_*.png`).

**Chậm lúc ra đòn, bỏ nấc tốc độ (Unity, 2026-11-04).** Người dùng: tướng ra đòn, bắn chiêu thì giảm tốc độ game để nhìn rõ animation; bỏ nấc ×2, ×3.
- Trận một nhịp: sân chạy ×3 tốc độ gốc aola như nấc ×1 cũ. Đã bỏ nút ×1/×2/×3 ở thanh trên trận, hàng tốc độ ở Sổ tay và khoá `settings.speed` của bản lưu.
- Lúc có tướng chạy clip đánh, cả sân chậm về ×1,3 tốc độ gốc. Lúc bắn tia (đến khi tia tan) và lúc phát clip CHIÊU thì về ×1. Chậm cả hai tướng, chữ nổi, hiệu ứng, rung và chờ giữa các sự kiện (`StageView.Wait`, giây sân). Clip đánh trung bình 1,68 s thành khoảng 1,3 s thật (trước khoảng 0,56 s); chiêu 1,4 s (trước khoảng 0,93 s).
- Clip vừa bắt đầu là chậm ngay, xong clip thì nhanh lại trong khoảng 0,1 s. Số chỉnh ở `StageView`: `AttackPace`, `SkillPace`, `SlowEase`. Thay cho `SkillTime` cũ, vốn chỉ kéo chậm clip chiêu.
- Tour thử trong Editor gọi `BattleController.FastForward(k)` để cả trận, kể cả lúc ra đòn, chạy nhanh gấp k. Chỗ trước đặt ×3 nay dùng `FastForward(2)`, bằng nhịp ×3 cũ lúc không ra đòn.

**Luật rút thẻ: 35 thẻ chung, thẻ đã chọn không ra lại trong lượt (Unity, 2026-11-04).** Người dùng: tăng số thẻ (chọn thêm thẻ mới vào bộ, mỗi lần vẫn hiện 3 thẻ); thẻ đã chọn thì không ra lại trong cùng lượt, có thẻ được ra lại, có thẻ thì không (chọn "theo tác dụng").
- `Battle.DrawOffer` bỏ khỏi bộ rút các thẻ đã nằm trong hàng thẻ của lượt, trừ thẻ có `"repeat": true` trong `cards.json` (`CardDef.repeat`). Sang lượt sau hàng thẻ trống nên mọi thẻ ra lại. Máy chọn theo cùng luật. Trong một lần rút, 3 thẻ vẫn khác nhau như cũ.
- Ra lại được (thẻ nhỏ, cộng dồn không phá cân bằng): Mài Vuốt, Băng Gạc, Hít Thở, Gầm Gừ, Ném Đá, Bình Thuốc, Thủ Thế, Tĩnh Tâm, và 3 thẻ mới Cắn Xé, Phóng Lông, Trăng Khuyết. Mỗi lượt một lần: mọi thẻ Hiếm trở lên, Giáp Gỗ, Bánh Bao Thịt, Liều Mạng, Đấm Kép và các thẻ mới còn lại. Đổi thẻ nào thì sửa cờ trong `cards.json` rồi `Nhập dữ liệu`.
- 12 thẻ mới, dùng hiệu ứng và icon có sẵn. Cấp 1 có 19 thẻ (trước 13):

  | Thẻ | Độ hiếm | Mở ở cấp | Tác dụng | Ra lại |
  |---|---|---|---|---|
  | Cắn Xé | Thường | 1 | Gây 30% Công sát thương, hút 50% thành máu. | có |
  | Nhảy Lùi | Thường | 1 | 25% né đòn đánh thường tới lượt sau. | |
  | Đứng Tấn | Thường | 1 | +30% Thủ tới lượt sau. | |
  | Hạt Dẻ | Thường | 1 | Hồi 3% máu đầu mỗi lượt, 3 lượt. | |
  | Phóng Lông | Khá | 1 | Đánh 3 lần, mỗi lần 20% Công. | có |
  | Tung Cát | Khá | 1 | Địch −20% Công 1 lượt. | |
  | Trăng Khuyết | Khá | 2 | Hút 20 mana của địch. | có |
  | Búa Tạ | Hiếm | 2 | Gây 70% Công sát thương, xuyên 50% Thủ. | |
  | Suối Trong | Hiếm | 3 | Xoá hiệu ứng xấu. Hồi 12% máu. | |
  | Sấm Rền | Hiếm | 4 | Gây 60% Công sát thương. 35% cơ hội: làm địch choáng. | |
  | Lông Phượng | Sử thi | 6 | Hồi 15% máu. Hồi 5% máu đầu mỗi lượt, 3 lượt. | |
  | Dồn Sức | Sử thi | 8 | +40% Công trong 2 lượt. +20 nộ. | |

- Sổ thẻ xếp theo độ hiếm rồi cấp mở. Hộp chi tiết thẻ ghi "ra lại được trong lượt" hoặc "mỗi lượt chọn một lần".
- Số đo (máy tự chơi, đảo Thủy, 300 trận mỗi ải, cách đo như `Editor/StarterBalanceMenu`), trước → sau. Cột Võ Sư là người chọn Giọt Sương, Sư Tử Lửa, Bu Lông hay Nụ Hoa (đều ra trận bằng Võ Sư):

  | Kiểu ải | Võ Sư | Thạch Nhân |
  |---|---|---|
  | Tướng mới | 97 → 97 | 96 → 97 |
  | Bầy lính | 88 → 89 | 94 → 95 |
  | Cường hóa | 90 → 87 | 82 → 77 |
  | Tướng và lính | 73 → 74 | 83 → 83 |
  | Lính tinh nhuệ | 74 → 73 | 81 → 79 |
  | Mini boss | 58 → 58 | 53 → 55 |
  | Hai tướng | 61 → 55 | 62 → 58 |
  | Cửa ải | 61 → 55 | 58 → 57 |
  | Boss ải 70 | 62 → 72 | 64 → 74 |
  | **Cả đảo** | 78 → 76 | 79 → 78 |

  Lượt máy có thẻ lặp: 68% → 38%. Bảng 102 ải × 5 mức cấp (100 trận mỗi ô): mọi ô lệch không quá 3 điểm. Trận dài thêm chút ít, rõ nhất đảo Thổ (7,3 → 8,1 hiệp). Chưa chỉnh sức địch theo số mới.
- Golden tính lại bên Unity bằng Core chạy ngoài Editor: `battles`, `battle_events`, `sim`, `badges` (5 trận), `potential` (6 trận); `cardtext` thêm 12 thẻ. Test mới `TheDaChon_KhongRaLaiTrongLuot_TruTheLapLai`. Bản web không đổi (23 thẻ, thẻ ra lại tự do).

**Hộp Chuẩn bị: đối thủ trái phải, cấp rõ; chân dung nét hơn; tai thỏ (Unity, 2026-11-04).** Người dùng: chân dung bị nén mờ (nhất là bóng sẫm); tướng bên trái, chỉ số bên phải, phóng to tên, hệ…; cấp tướng, địch rõ hơn; thanh trên tránh camera, dải tai thỏ trong suốt hoặc cùng màu UI.
- Mỗi đối thủ một hàng. Ải một địch dùng hàng to `Items/DoiThu`, cao 340: chân dung trái; bên phải là tên, nhãn hệ và lực chiến, dòng ghi chú, 3 hàng Máu, Công, Thủ có chữ. Ải 2–3 địch dùng hàng gọn `Items/DoiThuGon`, cao 180: ghi chú chung hàng với nhãn hệ, chỉ số xếp ngang. Chân dung phóng cho phần có hình (`PortraitBoxes`) vừa ô, nên lính nhỏ không bé tí.
- Chip "Cấp N" cùng kiểu chip cấp trên thanh trên, đặt ở góc chân dung. Chữ đỏ khi địch hơn người chơi quá 2 cấp. Ô đội của hộp cũng có chip cấp.
- Dựng bằng menu `PokiClash/Prefab/Hộp chuẩn bị: ô đối thủ trái phải` (`PrepStatsMenu`). `Popup gọn` không còn đụng `DoiThu`.
- Chân dung tướng ASTC 8x8 → **5x5** (`AolaImportPostprocessor.PortraitFormat`). Mỗi ảnh 87 → 226 KB, 107 ảnh, bản build nặng thêm khoảng 15 MB; atlas giữ 8x8. Ở cỡ 100–250 điểm game lấy mipmap nửa, khối 8x8 phủ 16x16 điểm ảnh gốc nên vỡ khối.
  - Đổi mức thì sửa hằng số rồi chạy menu `PokiClash/Tướng/Nhập lại chân dung tướng (mức nén chân dung)`; không tăng `GetVersion` (tăng thì nhập lại mọi ảnh tướng).
  - Mức nén ghi vào .meta, nên máy kia kéo git về sẽ tự nhập lại.
  - So trong game: menu `Chân dung: thay thử mức nén trên màn đang mở`, ảnh ở `Temp/PokiShots/nen`.
- Tai thỏ: các màn đã nằm trong vùng an toàn và lộ nền dưới camera. Riêng màn trận có dải nâu sẫm, nay nền giấy của thanh trên trận (`Thanh tren tran/nen`) kéo cao thêm 300 để phủ dải đó.
- Thử: menu `PokiClash/Thử/Hộp chuẩn bị: ô đối thủ, cấp, tai thỏ (đang Play)`, ảnh `Temp/PokiShots/cb_*.png`. Vòng này chụp hộp 1, 2, 3 địch; đảo lúc mới qua 2 ải (bóng sẫm); và 6 màn ở khung 1080 × 2400 với tai thỏ giả (`SafeArea.Simulated`).
- Nền trận: gói `ArtGen/BattleBG/gui_gpt/troi` dựng lại cho máy ổ D (`build_troi.py`).
  - 2026-11-05: c02–c09 đã ghép (`--duyet`, đường nối nằm trong vùng trời) và xuất vào game (`build_thuy.py --xuat`), nên đủ 9 chặng. Sau đó m20, m40, m50, m60, b70a cũng vào game.
  - m30 hỏng ở cả hai bản GPT: vẽ lặp mảng rêu và vách ngay trên mép cũ, nên gãy ngang qua vách và hai thác. Ảnh ghép đổi tên thành `troi/m30_hong_noi_gay.png` để game giữ nền cũ. Prompt `11_m30.txt` đã thêm đoạn dặn chỗ nối, chờ gen lại.
  - Còn b70b, b70c (`16_b70b.txt`, `17_b70c.txt`, bám theo b70a đã duyệt).
  - `--xuat` ghi lại cả 27 ảnh không đổi: điểm ảnh y hệt, chỉ khác byte PNG.
- Bố cục theo cỡ máy (người dùng dặn 2026-11-05: phần dưới giữ chắc trên mọi máy cho khỏi dính vào nhau, phần trên co giãn). Màn trận đã theo cách này:
  - bảng dưới cao cố định 880; khung sân 1080 × 928 neo đáy (tướng, bệ, bảng máu theo khung);
  - máy dài hơn 9:16 chỉ thêm trời phía trên; máy tính bảng 3:4 như 9:16, hai bên để nền bàn.
  - Thử bằng menu `Thử/Trận ở 4 cỡ máy: phần dưới cố định, trời co giãn`, ảnh `cb_tran_*.png`.

## Câu hỏi còn mở (gom từ các design.md; đánh số lại sau lượt trả lời 2026-10-31)

1. **Nhịp tiến độ** (mục tiêu: người chơi "vừa" xong 5 đảo khoảng ngày 21). Sau khi có cây bi vẫn là ngày 6. Quét bằng menu `Quét nhịp`:
   - EXP lên cấp ×6: ngày 15;
   - EXP ×2, bi thụ động ×0,5, "Hái ×2" 1 lần/ngày: ngày 13;
   - ở các tổ hợp mạnh tay đó, người chơi "ít" không xong trong 30 ngày.

   Sức mạnh chủ yếu đến từ sao tiến hóa và cấp thẻ: 40–43 lần tiến hóa trong 30 ngày ở mọi tổ hợp, vì thẻ đến từ rương máy bi. Chọn hướng:
   - tăng giá thẻ và tiến hóa (bản sao mỗi cấp thẻ, thẻ mỗi sao);
   - giảm thẻ trong rương;
   - giảm tiếp bi thụ động;
   - hay nhận nhịp nhanh hơn và thêm ải, tướng sau?
   - **2026-11-04:** người dùng chốt thang cấp 1–200 kiểu Clash of Critters: cấp địch là cấp cần đạt, mỗi đảo khoảng 40 cấp, đảo Thủy 5–7 ngày, cấp 200 sau ít nhất 30–45 ngày. EXP lên cấp 45 × cấp. Theo máy: người chơi "chăm" xong Thủy ngày 5 và đạt cấp 200 ngày 42; "vừa" xong Thủy ngày 8 và đạt cấp 200 ngày 57 (`14_HeThongAi.md`, mục "Thang cấp 1–200").
2. **Trang trại** có ra thêm EXP không?
3. **Kiếm tiền:** chọn SDK nào (quảng cáo, IAP)? Giá hai gói?
4. **Kỹ thuật:** chốt Unity 6 bản vá nào? Có cần Addressables cho ảnh đảo không?
5. **Đã chốt 2026-11-02: nhập vào Assets thành prefab tướng (xem mục "Prefab tướng" ở trên).** **Hình aola:** (2026-11-02, người dùng bảo "ghép hình aola các tướng đã chọn vào game, cả animation đánh") giờ Editor lúc Play luôn nạp hình aola từ thư mục reskin (tự tìm trên ổ đĩa), không cần define, không đổi ProjectSettings; bản build vẫn chỉ nạp khi có `POKICLASH_DEV`. Hình vẫn KHÔNG nằm trong Assets vì `PreBuildCheck` và test `KhongCoHinhAolaTrongAssets` chặn hình Baitian trong bản phát hành. Còn hỏi: có muốn nhập hình aola vào Assets để chạy trên máy thật (phải bỏ luật chặn đó, hình Baitian sẽ vào bản build) không?
6. **ProjectSettings:** giữ hay hoàn các thay đổi màn dọc do `BanThuSetup.cs` cũ ghi vào `ProjectSettings.asset`?
7. **Công cụ dev** bọc theo `UNITY_EDITOR || DEVELOPMENT_BUILD` (có cả trong bản Development) thay vì `POKICLASH_DEV` như design ghi, vì define đó gắn với hình aola. Được không?
8. **Máy bi và AFK, các chỗ tự chọn cần duyệt:**
   - máy bi: gộp bản sao cùng thẻ "×n", hộp "Huyền thoại!" sau rương cuối, lên cấp khi rời máy chỉ báo bằng thông báo;
   - AFK: bộ đếm rương không về 0 khi nhận, rương kế đếm khi rương trước đếm xong, khay đầy giữ tiến độ, tăng tốc xám khi đầy giờ, mảnh AFK từ mọi boss đã gặp, tăng tốc 3 lần/ngày.
9. **Kiếm tiền, các chỗ tự chọn cần duyệt:**
   - Thẻ Phiêu Lưu tăng cây bi ×1,5 cả tốc độ lẫn sức chứa (không nhân mảnh, không tác động trang trại và Hang);
   - mua thẻ khi còn hạn thì cộng dồn;
   - Bỏ quảng cáo vẫn trừ lượt mỗi ngày;
   - hết lượt thì nút xám, bỏ hình TV;
   - cửa hàng giả lập mua ngay, không hỏi lại;
   - bản lưu lên v3.
10. **Cây bi, các chỗ tự chọn cần duyệt:**
    - 5 cây (Critters có 8), mở theo boss đảo;
    - "Hái ×2" 3 lần/ngày (Critters không có);
    - hái một lần cho mọi cây (Critters hái từng cây);
    - cây mới mở bắt đầu từ lần tính sau;
    - không có trần kho bi (Critters chặn hái khi đã có 420 bi).
11. **Đã chốt 2026-11-02: nhập hình vào project thành prefab tướng.** **Prefab, hình aola bản dev** (`convert-to-prefabs`): `AolaActor` và `AolaSticker` đọc PNG và json từ thư mục aola ngoài project lúc chạy, tạo quad, material, RenderTexture. Giữ ngoại lệ này (chỉ bản dev, test chặn bỏ qua), hay nhập hình vào project thành asset (loại khỏi bản phát hành)?
12. **Prefab, scene thử cũ `BanThu`:** không chuyển sang prefab (đã bỏ hướng xếp khối). Để nguyên hay xoá?
13. **Prefab, cấu trúc (đã chuyển hết theo cách này):** mỗi hộp thoại là biến thể (prefab variant) của tờ giấy gốc `Dialogs/HopThoai`; mỗi màn là `Screens/<Scene>.prefab`; phần lặp theo dữ liệu là `Items/*.prefab`; tên GameObject giữ tiếng Việt không dấu như cũ. Code nướng đã xoá nên sửa giao diện là sửa prefab. Phần có số lượng theo dữ liệu nhưng dựng sẵn cố định trong prefab (5 đảo ở sảnh, 5 nút cược máy bi, 5 nút chọn hệ ở Hang, 3 ô đội hình) phải thêm tay nếu dữ liệu tăng. Ổn chưa?
14. **Menu thử Tướng** báo "Lệch chỉ số: màn Tướng 1039/471/119, trận 1191/357/95" (có từ trước khi đổi sang prefab): màn Tướng và trận tính chỉ số khác nhau khi tướng có huy hiệu, tiềm năng. Cần xem lại phần nào đúng.

Hệ thống 70 ải mỗi đảo (2026-11-02, bản thử đảo Thủy trên web, `14_HeThongAi.md`):

15. **10 tướng đảo Thủy:** 7 tướng người dùng gửi cùng Giọt Sương (ải 1), Tiểu Y (5), Cánh Cụt (10). Thứ tự theo độ hiếm: Mi Nhi 15, Ma Kết 20, Vây Lam 30, Kuba 40, Thương Lam 50, Huyền Vũ 60, Lam Quân boss ải 70 (vào trận dạng Lam Quân, tiến hóa lên Vạn Quân rồi Hắc Dực). Đúng ý chưa? Huyền Vũ (Huyền thoại) đứng trước boss Sử thi có ổn không?
16. **3 tướng Thủy không có suất trên đảo:** Tám Tay, Cá Ngựa, Mập Răng Cưa. Giữ cho máy bi hoặc sự kiện, đưa sang đảo khác, hay bỏ?
17. **Ô đội:** ô 2 mở khi xong 1 đảo, nên cả 70 ải đảo Thủy chỉ mang 1 tướng. Mở ô 2 sớm hơn (ví dụ ở ải 20 hoặc 30) không? Số đo hiện tính cho 1 tướng.
    - **Đã chốt 2026-11-03** (`15_TuongKhoiDau.md`): ô đội mở theo cấp người chơi, ô 2 ở cấp 10, ô 3 ở cấp 30. Đánh đảo Thủy đúng cấp vẫn chỉ 1 ô; sức địch từ ải 4 chỉnh nhẹ (+0,05 tới +0,15) vì Võ Sư lên Khá.
18. **Sức địch:** ở hệ thống mới, tướng địch mọi độ hiếm quy về sức tướng Khá cùng cấp. Nếu không quy, tướng Hiếm trở lên cùng cấp gần như không thua. Giữ cách này, hay hiện cấp cao hơn cho địch hiếm?
19. **Tướng không khắc hệ đảo:** Giọt Sương (Thủy) đánh đảo Thủy kém Võ Sư (Thổ) 30–50 điểm phần trăm ở mọi kiểu ải khó. Đây là luật khắc hệ có sẵn. Giữ vậy, hay nới cho tướng khởi đầu?
    - **Đã chốt 2026-11-03** (`15_TuongKhoiDau.md`): người chơi chọn 1 trong 5 tướng khởi đầu; tướng đã chọn (tướng đồng hành) không chịu thiệt khi khắc hệ; luôn ra trận cùng tướng tặng khắc đảo.
20. **Nhịp và thưởng:** 5 đảo × 70 ải là 350 ải. Người chơi "vừa" (9 trận/ngày) cần ít nhất 39 ngày chỉ để qua lần đầu, so với mục tiêu ngày 21 (câu 1). Bi mỗi ải giảm còn 1–2 để cả đảo Thủy đưa người chơi lên khoảng cấp 7–8. Các hướng: chấp nhận nhịp dài hơn, tăng số trận mỗi lần vào game trong mô phỏng, hay rút số ải? Đo lại bằng `Quét nhịp` sau khi chép sang Unity. Đền Huy Hiệu giờ mở sau ải 70 đảo Thủy: có cần mở sớm hơn không?
    - **2026-11-04:** bi mỗi ải đảo 70 ải tính theo số ải: 1 bi ở ải 1–35, 2 bi ở ải 36–70. Các đảo 8 ải dời lên cấp 41–200.
21. **Bóng sẫm tướng chưa mở** (2026-11-04): `HeroPortrait` tô nhân màu nâu `#4a3c30`, nên chi tiết bên trong vẫn lờ mờ hiện ra, nhìn đục. Muốn bóng phẳng một màu (chỉ giữ dáng) thì cần một material UI riêng làm sẵn. Làm không?
22. **Ảnh mẫu mặt tướng gửi GPT bị giãn ngang** (session hình aola báo 2026-11-04): `ArtGen/BattleIntro/build.py` tưởng chân dung trong Unity là 384x480, trong khi ảnh lưu vuông 512. Sửa không?

23. **Đã chốt 2026-11-06: ải 20 đảo Hỏa là 火云牛斗士 (Ngưu Quyền, dòng 412 → 414).** Hình 3 dạng chưa xuất (máy sập lúc xuất, xem mục "Prefab tướng").
24. **Đảo Hỏa, tên và thẻ tạm:** Khổng Lồ Lửa, Kim Sư, Nham Thần, Hồng Liên, Giáp Long, Huyễn Viêm, Hỏa Tinh, Lân Hỏa và 6 lính (`13_DanhSachTuong.md`, mục Hỏa); độ hiếm tăng theo ải, thẻ thiên về đốt. Hồng Liên, Huyễn Viêm là phiên âm tên gốc. Duyệt hay đổi?
25. **Tướng Hỏa cũ không có suất trên đảo:** Heo Lửa, Đốm Lửa, Pháo Tết, Võ Tăng Bồ Đề, Thiền Sư Pháp Luân, Chu Tước (Huyền thoại Tứ Tượng cũ). Giữ cho máy bi hoặc sự kiện, đưa sang đảo khác, hay bỏ? (Hồ Lửa đứng tạm ở ải 20 tới 2026-11-06, nay cũng không có suất.)
26. **Xuất hình aola ở máy này:** máy sập 4 lần trong 2 ngày, lần nào cũng lúc Chrome headless vẽ mảnh; có bản ghi lỗi phần cứng mức Fatal (WHEA). Kiểm phần cứng trước (tắt EasyTune/BIOS mặc định, cập nhật BIOS, chạy thử CPU nặng), xuất ở máy công ty, hay chạy lại 1 luồng khi người dùng ngồi máy? Hướng sửa công cụ: giữ một Chrome mở suốt (DevTools) hoặc vẽ SVG không cần Chrome (resvg).
27. **Đảo Kim, thứ tự và boss** (2026-11-05): theo luật "trái sang phải là thứ tự ải", 猎空 (Ưng Thép) đứng ải 60, 克里亚斯 (Kim Nghê) là boss ải 70. Hình 猎空 có nhãn BOSS của aola. Muốn đổi Ưng Thép thành boss ải 70 không? Đổi chỉ cần sửa `IslandGen.Kim`, không phải xuất hình lại. Kim Nghê chỉ có 2 dạng (aola không có siêu tiến hóa), nên boss chỉ tiến hóa một lần.
28. **Đảo Kim, tên, thẻ và lính tạm:** Độc Giác Thép, Phi Thương, Khiên Bạc, Chiến Thần, Thiết Phủ, Tam Kiếm (dòng 刘备, không dùng tên gốc), Ưng Thép, Kim Nghê; Bọ Cạp Đồng xuống Thường, Bọ Ngựa xuống Khá, cả hai thẻ mới; 6 lính Giáp Vệ, Chiến Giáp, Nóc Sắt, Nóc Khiên, Máy Bay Con, Phản Lực (`13_DanhSachTuong.md`, mục Kim). Duyệt hay đổi?
29. **Tướng Kim cũ không có suất trên đảo:** Pháo Hộp, Kiếm Linh, Mèo Quyền Sắt (vẫn là quà ải 3 đảo Thủy khi chọn Thạch Nhân), Sói Linh Thép, Bạch Hổ (Huyền thoại Tứ Tượng cũ). Giữ, đưa sang đảo khác, hay bỏ?
30. **Đảo Thổ, hình ải 50** (2026-11-06): 金刚虎王 là siêu tiến hóa của dòng Hổ Khoan (尖钻虎王, hình ải 15), nên hai hình cùng một dòng. Đang tạm làm tướng riêng 1 dạng (`ho_kim_cuong`, Hổ Kim Cương) như Thỏ Hoàng ở đảo Mộc. Giữ vậy, hay đổi hình ải 50 sang dòng khác (chỉ cần sửa `IslandGen.Tho`, xuất hình dòng mới)?
31. **Đảo Thổ, tên, thẻ và lính tạm:** Lửng Vương, Cáo Đá, Hổ Khoan, Phù Văn, Hạt Dẻ, Rùa Núi, Hổ Kim Cương, Cự Phủ, Giáp Nham và 6 lính Chuột Khoan, Khoan Giáp, Đá Con, Đá Xích, Ngựa Con, Ngựa Rằn (`13_DanhSachTuong.md`, mục Thổ); độ hiếm tăng theo ải như đảo Kim. Giáp Nham (boss) gốc là hệ aola 1, không phải Đất. Cự Phủ tự thân yếu nên ải 60 phải cường hóa thêm +0,55 mới về 67%. Duyệt hay đổi?
32. **Tướng Thổ cũ không có suất trên đảo:** Võ Sư (vẫn là quà ải 3 đảo Thủy), Gấu Thợ Mỏ, Sóc Đá, Bọ Hung Cát, Sa Thần, Kỳ Lân Cát, Đại Sư Cà Sa (vẫn là tướng mốc huyền thoại). Giữ, đưa sang đảo khác, hay bỏ?
33. **Dòng Giọt Sương vẽ lại thành Thủy Long** (2026-11-08, long chiến binh, rig .atomik; người dùng chọn tạo hình và cho đổi tên): tên tạm Thủy Long, danh hiệu "Chiến binh rồng biển", 3 dạng Long Binh (giáo), Long Kỵ Sĩ (kiếm lưỡi nước), Long Tướng (đại đao, áo choàng). Id, chỉ số, thẻ, chiêu vẫn là `giot_suong`; tên thẻ, mô tả chiêu chưa đổi. Duyệt tên hay đổi? Dạng cũ `rong_giot`, `thuy_7..9` không còn ai dùng nhưng vẫn nằm trong Resources (vào bản build) tới khi chạy menu "Xoá dạng aola không còn tướng nào dùng" (xoá file nên chờ người dùng).
34. **Tám Tay vẽ lại thành tướng .atomik** (2026-11-08, cùng tiêu chí Thủy Long: tự thiết kế, chiến, không cute, gen liền một ảnh): bạch tuộc chiến binh, dạng 1 Tám Tay Bong Bóng (mũ nồi đỏ, súng vỏ ốc anh vũ), dạng 2 Tám Tay Pháo Thủ (mũ trụ đồng thợ lặn, pháo vỏ ốc). Giữ 2 dạng, tên, id, chỉ số, thẻ như cũ; chỉ đổi hình (`tam_tay_1`, `tam_tay_2` thay `thuy_1053`, `thuy_1054`). Concept Claude tự duyệt. Duyệt hay sửa thiết kế? Có muốn 3 dạng như Thủy Long không? Dạng cũ `thuy_1053`, `thuy_1054` cũng chờ menu xoá như câu 33.
35. **Học gì từ animation Clash of Critters** (2026-11-08, đã giải 9 con, số đo ở báo cáo trong chat): nhịp đòn của mình (0.9–1.1 s, trúng ở 0.38–0.52 s) và idle 2.4 s đã nằm trong khoảng của họ. Khác biệt có thể học: (a) lắc mào, áo choàng, xúc tu bằng lệch pha khoá tay thay lò xo; (b) đổi hình mặt: chớp mắt 3–6 khung, há miệng đúng khung trúng (cần gen thêm mặt từ ảnh liền); (c) clip chết kiểu hất, treo, rơi 1–2 khung, nằm, và clip thắng trận; (d) đòn ra 2–3 khung, vượt quá thế đứng 7–15°, chân đứng yên. Chọn mục nào để áp vào Thủy Long, Tám Tay?
36. **9 dòng còn lại của đảo Thủy vẽ lại thành thú huyền thoại .atomik** (2026-11-08, người dùng dặn: thú huyền thoại hơi chibi kiểu Pokémon, style cũ, dạng sau dữ hơn nhưng không quá, hạn chế dạng người, animation đơn giản kiểu Critters, hiệu ứng bù vào, càng gần boss cuối càng đẹp). Thiết kế Claude tự duyệt: Tiểu Y cáo nước, Cánh Cụt cánh cụt băng làm bếp, Mi Nhi chim đàn lia ("tiên cầm"), Ma Kết dê biển, Vây Lam cá mập đi bốn chân, Kuba cua pha lê, Thương Lam rồng băng, Huyền Vũ rùa đuôi rắn, Lam Quân Bồ Lao (rồng sư tử chuông đồng). Bỏ hai ngoại lệ dạng người cũ (Tiểu Y Poseidon, Mi Nhi tiên cá). Giữ id, tên, chỉ số, thẻ, số dạng; mã hình mới `<id>_<k>`. Hiểu "dạng tiến hóa sẽ giữ hơn" là "dữ hơn". Cần duyệt: thiết kế từng dòng; cỡ (`size`) giữ như bản aola nên thú bốn chân có thể trông to ngang; Ca Ngựa, Mập Răng Cưa (không có suất trên đảo) chưa làm; dạng aola cũ (`thuy_1319`…`thuy_2955`) còn trong Resources, chờ chạy menu xoá. Đã xong cả 24 dạng (có tiến hóa), `heroes.json` đã đổi, prefab đã gắn, test RosterTests sửa theo mã mới. Kuba dạng 3 Codex vẽ chính diện (giữ). Chưa chạy vòng thử trong trận và EditMode vì Unity đang Play lúc làm. Lưu ý: `BanThuGame.cs` còn dùng `thuy_1319`, `thuy_1320` nên đừng xoá hai dạng này.
37. **10 dòng đảo Mộc vẽ lại thành tướng .atomik** (2026-11-08 tối, người dùng dặn: concept dựa trên tướng đã có; gen một con hoàn chỉnh, rig xương, rồi mới gen thêm bộ phận phục vụ animation). Mỗi dạng vẽ lại theo đúng concept đã duyệt (`ArtGen/Heroes/inbox/<id>_<k>/concept_duyet.png`) ở dáng rig được; sau khi rig, GPT vẽ thêm hai ảnh "lớp dưới" (phần bị che dưới đầu, chân gần, cánh gần; phần sau thân) thay cho loang màu. Đủ 24 dạng có tiến hóa, 11 tờ hiệu ứng lá, hoa, gió, pha lê, sét phẳng (Thanh Long thêm tờ thứ hai). `heroes.json` đổi mã `<id>_<k>`, test RosterTests sửa theo. Thanh Long dạng 1 và 3 gen lại cho mây, bờm tô màu (trắng giấy viền hở không rig được). Cần duyệt: thiết kế (giữ theo concept cũ); Thỏ Hoàng vẫn 1 dạng; dạng aola cũ `goc_*` của Mộc còn trong Resources.
38. **Hai đảo Thủy, Mộc làm lại thành một lưới liền, chiêu đa dạng** (2026-11-09 đêm, người dùng chê bản ghép lớp lỗi nhiều, dặn gen một con nguyên chân tay đuôi, chỉ tách vũ khí, cánh khi cần, chiêu không được toàn nhảy lên rồi ra chiêu; ủy quyền làm hết không hỏi). 48 dạng dựng lại từ đúng ảnh đã duyệt (không gen lại), mỗi con một lưới; mỗi dòng một cặp đòn, chiêu riêng (vồ, đấm, đá, quất đuôi, lăn, ném đồ, đập đồ; gai trồi, vật rơi, loạt đạn, sóng đất, lao húc, trượt bụng, liên hoàn, bàn tay gỗ khổng lồ). Game thêm hiệu ứng ở chỗ đối thủ cho tướng .atomik (`game.far`). Cần duyệt: kiểu đòn, chiêu từng con (QUY_TRINH mục 18); chưa chạy vòng thử trong trận.
39. **10 dòng đảo Hỏa vẽ lại thành tướng .atomik** (2026-11-09, người dùng dặn lên prompt theo cách hai đảo Thủy, Mộc): đảo Hỏa chưa có concept nào đã duyệt nên Claude tự thiết kế, giữ chủ đề, loài của dòng aola người dùng chọn, mỗi dòng một bảng màu (QUY_TRINH mục 19). Gói `ArtGen/Spine/build_hoa.py`. Người dùng duyệt chữ cùng ngày; đã gen đủ 28 dạng và 12 tờ hiệu ứng lửa, rig một lưới, mỗi dòng một cặp đòn/chiêu riêng (`beasts_cfg_hoa.py`, QUY_TRINH mục 19). Ngưu Quyền làm bằng .atomik nên bỏ việc xuất hình aola 412–414. Còn chờ người dùng: xem trong trận; tên 3 dạng Sư Tử Lửa đang trùng nhau; xoá dạng aola cũ `goc_*` của Hỏa khỏi Resources (menu xoá).

## Ảnh cần gen

Gói prompt ở `ArtGen/` (gốc dự án), theo quy trình cũ: đọc `PROMPTS.md`, gen bằng GPT (hoặc Tripo cho đảo 3D), lưu vào `inbox/` của gói. Danh sách gói và thứ tự gen: `ArtGen/README.md`.

Máy bi (`ArtGen/Pachinko`): thân máy, bộ phận, hiệu ứng, rương đã vào game ngày 2026-11-04. Việc còn lại ở `07_MayBi.md`, mục "Việc còn lại".
2026-11-09: mặt máy thay bằng bàn chép y máy tham khảo (vòm, làn phóng phải, 22 đinh, nấm vòng tiến độ, 5 ô, cốc dưới mái), kết quả chọn theo bảng tỉ lệ rồi phát đường bi vật lý; `07_MayBi.md`, mục "Bàn chép y máy tham khảo".
