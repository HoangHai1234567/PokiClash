## Context

Bản web (Web/) là bản thử đã duyệt. Phần logic ở `Web/src/core` không đụng trình duyệt:
- số ngẫu nhiên mulberry32 có hạt giống;
- luật trận, máy chơi;
- tiến trình (cấp, thẻ, sao, mảnh, đảo, AFK);
- vật lý máy bi.

Phần hiển thị ở `Web/src/view`: DOM, canvas, CSS.

Project Unity (6000.0.x, URP, uGUI, Input System, gói MCP for Unity) đã có:
- màn dọc;
- `AolaActor.cs`: đọc `anim.json` của aola, dựng mỗi hình thành một quad theo ma trận Flash;
- `MiniJson.cs`.

Chủ dự án muốn bố cục theo scene như Clash of Critters. Critters dùng các scene chức năng (pinball, world map, pet, build), một hàng nút chính và màn mây khi chuyển.

## Goals / Non-Goals

**Goals:**
- Logic trong Unity cho ra **đúng cùng kết quả** với bản web khi cùng hạt giống, để số đã cân trên web vẫn đúng.
- Mỗi chức năng là một scene Unity riêng, mở và đóng được độc lập. Các dịch vụ dùng chung sống ở scene Boot.
- Bộ UI vẽ tay dùng lại được ở mọi scene, giữ đúng phong cách bản web.
- Thiếu ảnh gen thì không chặn việc làm: có ảnh thay thế.

**Non-Goals:**
- Server, đăng nhập, đồng bộ đám mây.
- Hình tướng mới thay hình aola (việc của art sau).
- Bản địa hoá ngoài tiếng Việt (chuỗi để ở một bảng để sau này dịch).

## Decisions

### Scene Boot giữ dịch vụ, scene chức năng nạp cộng

`Boot.unity` chứa:
- `AppRoot`: `DontDestroyOnLoad`, gồm SaveService, AudioService, SceneRouter, ModalService, ToastService;
- canvas phủ cho màn mây và hộp thoại.

`SceneRouter.Go(scene, args)`:
1. đóng màn mây (0,38 giây);
2. gỡ scene cũ, nạp scene mới bằng `LoadSceneAsync(Additive)`;
3. gọi `IScene.Enter(args)` trên gốc scene mới;
4. mở màn mây.

Mỗi scene có một `SceneRoot` khai báo kiểu thanh trên (`Hud`, `Back`, `None`), tên scene và đích quay lại.

- **Phương án khác: một scene, bật tắt panel.** Bỏ, vì chủ dự án muốn chia scene, và scene riêng dễ chia việc, dễ thử từng phần.

### Logic thuần ở assembly `PokiClash.Core`, chép 1-1 từ TypeScript

- Không dùng `UnityEngine`. Toán dùng `System.Math`, ngẫu nhiên dùng lớp `Rng` chép đúng mulberry32 (phép `Math.imul` → nhân `int` có tràn, `>>>` → `uint`).
- Tên lớp và hàm giữ tương ứng: `Battle`, `Ai`, `Progression`, `Pachinko`, `CardText`, để dễ đối chiếu.
- **Kiểm tra trùng khớp (golden):** `Web/scripts/export_golden.ts` chạy một loạt trận và đợt thả bi với các hạt giống cố định, ghi chuỗi sự kiện và kết quả ra JSON. EditMode test trong Unity chạy lại cùng hạt giống và so từng sự kiện.
- **Phương án khác: viết lại luật trong Unity.** Bỏ, vì mất phần cân bằng đã đo trên web.

### Dữ liệu một nguồn

`Web/scripts/export_data.ts` xuất tướng, thẻ, đảo, ải, cấu hình ra `Assets/02 Data/*.json`. Menu Editor `PokiClash/Nhập dữ liệu` dựng ScriptableObject (`HeroDb`, `CardDb`, `ZoneDb`, `BalanceConfig`) từ JSON.

Sửa số thì sửa ở web rồi xuất lại; Unity không sửa tay. Nếu sau này muốn sửa trong Unity thì đảo chiều: Unity xuất JSON cho web. Chỉ một chiều tại mỗi thời điểm.

### Nét mực rung bằng shader UI

Shader `PokiClash/UIInkBoil` dời UV theo một texture nhiễu. Có 3 bộ dời, thay nhau 6 lần mỗi giây (giống 3 filter SVG `boil0..2` của web).

- Áp cho khung, nút, icon; không áp cho chữ nhỏ.
- Tắt trong cài đặt thì dùng bộ dời cố định.

Viền khung dùng Image 9-slice với sprite vẽ tay: lấy từ gói `ArtGen/UIKit`, hoặc ảnh thay thế vẽ bằng code.

### Tướng dạng sticker

Viền trắng rồi viền mực quanh tướng: render tướng vào RenderTexture rồi chạy shader "outline 8 hướng" (thay cho `drop-shadow` của canvas web). Chỉ dựng lại khi khung hình đổi (25 khung/giây).

### Lưu

`SaveData` chép từ `Web/src/core/progression.ts` (`SAVE_VERSION`). Ghi JSON vào `persistentDataPath/save_v{n}.json`, ghi qua file tạm rồi đổi tên.

Khi phiên bản cũ hơn:
- chạy bộ di chuyển nếu có;
- không có thì hỏi người chơi trước khi làm mới (bản thử cho phép làm mới).

### Ảnh và ảnh thay thế

- `ArtLibrary` tìm sprite theo tên (`world`, `zone_thuy`, `btn_red`...) trong `Assets/03 Art`.
- Không có thì gọi bộ vẽ thay thế: chép cách vẽ bản đồ nét tay của `Web/src/view/scenery.ts` sang Texture2D, hoặc dùng khung trơn.
- Toạ độ vùng và ải là tỉ lệ 0–1 theo ảnh, lưu trong `ZoneDb`.

### Animation tướng aola chỉ trong bản dev

Đường dẫn thư mục reskin lấy từ `EditorPrefs`, hoặc biến môi trường `AOLA_RESKIN`.
- Có define `POKICLASH_DEV` thì `AolaActor` đọc PNG từ đĩa lúc chạy.
- Bản phát hành không có define đó: dùng hình giữ chỗ (khối màu theo hệ). Không chép hình aola vào Assets.

## Risks / Trade-offs

- **[Lệch số giữa web và Unity]:**
  - lỗi dịch phép bit của mulberry32;
  - khác thứ tự lặp `Dictionary`;
  - làm tròn số.

  Cách chặn: golden test so từng sự kiện; dùng `List` có thứ tự; làm tròn `Math.Round(x, MidpointRounding.AwayFromZero)` cho khớp `Math.round` của JS (JS làm tròn .5 lên).
- **[Shader rung tốn GPU trên máy yếu]:** có công tắc tắt, mặc định bật; đo ở mốc này trên một máy Android tầm thấp.
- **[Nạp cộng nhiều scene gây giật]:** scene nhẹ, ảnh nén ASTC, nạp trước ảnh đảo kế tiếp trong lúc màn mây đóng.
- **[Hình aola lọt vào build]:** kiểm tra tự động trước khi build: tìm đường dẫn aola và ảnh `pet*_parts` trong Assets; có thì báo lỗi.

## Migration Plan

- BanThu: gỡ khỏi Build Settings; code giữ nguyên, chờ chủ dự án quyết xoá.
- `AolaActor.cs`: tách khỏi BanThu, chuyển sang `Assets/01 Script/Game/Heroes`, sửa đường dẫn cứng `E:/ProjectAtomik/...`.

## Open Questions

- Unity 6 bản vá nào chốt cho cả nhóm? Hiện project là 6000.0.73f1.
- Có cần Addressables cho ảnh đảo lớn (giảm bộ nhớ) không, hay Resources/Sprite Atlas là đủ cho 7 ảnh đảo?
