# 30 — Bảo mật / Mã hoá bản build (chống đục APK)

Bắt đầu 2026-11-25. Mục tiêu: đối thủ có APK cũng khó "đục" (ảnh, code, tên hàm, chỉ số, save).

> **Nói thẳng:** không có "bất khả xâm phạm". Game chạy trên máy người chơi nên CPU/GPU cuối cùng phải giải mã để chạy — cao thủ dump bộ nhớ vẫn moi được. Mã đối xứng trong app cũng recover được. Mục tiêu thực tế: **nâng rào đủ cao để không đáng công** (kẻ nghiệp dư bỏ cuộc, kẻ giỏi tốn hàng chục giờ mà lợi chẳng bao nhiêu).

## Lõi dùng chung — `PokiCrypt`
`Assets/01 Script/Core/Security/PokiCrypt.cs` (thuần .NET, trong asmdef Core `noEngineReferences`). AES-256-CBC + HMAC-SHA256 (encrypt-then-MAC: sửa 1 byte là hỏng MAC, không giải ra). Khoá dẫn xuất bằng HKDF theo "nhãn" (`texture`/`balance`/`save` khác khoá nhau). Khoá chủ cất dạng 2 mảng XOR (không có literal khoá để grep).

**Test ngoài Unity** (không cần Editor): dùng mono/mcs của Unity
`C:\Program Files\Unity\Hub\Editor\6000.0.73f1\Editor\Data\MonoBleedingEdge\bin\mono.exe` chạy `lib\mono\4.5\mcs.exe` (ref `System.Core.dll`, `System.Security.dll`). Đã pass toàn bộ.

## Trạng thái 5 lớp

| Lớp | Việc | Trạng thái |
|---|---|---|
| Lõi | PokiCrypt (AES+HMAC) | ✅ xong, test pass |
| **4** | Mã hoá + ký **save** (chống sửa coin/gem) | ✅ xong, Unity compile sạch |
| **3** | Mã hoá **chỉ số balance** | ✅ xong + **đã bật** (`bal.enc` đã sinh) |
| **1** | Mã hoá **ảnh hero** (giữ ASTC) | ✅ cơ chế xác nhận trọn 183 ảnh; strip **đang TẮT** |
| **2** | Che **code / tên hàm** (global-metadata + chuỗi) | ⬜ cần tool Obfuz + cấu hình |
| **5** | Chống **repack** (kiểm chữ ký APK) | ⬜ cần keystore phát hành |

**Mọi thứ đã làm đều an toàn ngược** — chưa bật gì thì game chạy y như cũ.

---

## Đã làm — cách hoạt động & cách kiểm

### Lớp 4 — Save
- `Core/Security/SaveCrypt.cs`: `Protect`/`Unprotect` ở ranh giới file (dấu `PKS1:` + Base64). Bản lưu cũ (JSON thô) đọc thẳng; lần lưu sau tự mã hoá.
- Móc trong `Game/Save/SaveService.cs`: `ReadSave()` (giải mã khi đọc), `Protect` khi Save (trên luồng chính). **Không đụng `SaveCodec`** → test không vỡ, tour sao lưu nguyên văn vẫn chạy.
- `SaveCrypt.Context` = ràng buộc theo máy, **mặc định null** (tránh khoá nhầm người chơi khi cài lại). Chỉ bật khi có hệ tài khoản.
- **Kiểm:** chơi → thoát → mở file `persistentDataPath/save_v*.json`: phải thấy `PKS1:...` (không còn số thô). Sửa tay vài ký tự → mở lại game phải báo bản lưu hỏng (không nhận).

### Lớp 3 — Chỉ số balance
- `BalanceConfigAsset` thêm `byte[] enc` + `Resolve()` (ưu tiên enc). `GameDb.Build` dùng `Resolve()`. `DataImporter` sinh enc khi chạy **`PokiClash/Nhập dữ liệu`**.
- Build phát hành: `Editor/Build/SecureBuild.cs` strip `cfg` thô (verify enc giải được trước khi strip). Hook trong `PokiBuild` (chỉ AndroidRelease/IOS).
- **Kiểm:** đã chạy "Nhập dữ liệu" → `bal.enc` đã có. Mở `BalanceConfig.asset` bằng AssetStudio ở bản ship: `cfg` rỗng, chỉ còn blob.

### Lớp 1 — Ảnh hero
- `Core/Security/TexBlob.cs`: codec raw-texture (giữ đúng format, kể cả ASTC).
- `Game/Content/PokiArt.cs`: `LoadTexture/LoadSprite(key)` ưu tiên blob `Resources/enc/<key>.bytes`; không có thì lùi về `Resources.Load`. Đã swap: `AolaAnim.LoadAtlas/LoadPortrait`, `HeroArt.Face`.
- `Editor/Build/ArtEncryptStrip.cs`: bước build sinh blob + dời ảnh gốc ra ngoài Resources (theo khuôn `BuildExclude`: journal + tự khôi phục khi crash; verify từng ảnh giải được trước khi dời; bỏ qua ảnh còn bị GUID tham chiếu). **Mặc định TẮT.**
- **Đã kiểm (session assets-3e, Unity thật):** menu `Bảo mật/Thử mã hoá toàn bộ ảnh hero` → **183 ĐẠT / 0 LỖI**, format `ASTC_5x5×168 + ASTC_8x8×15` (**giữ ASTC**), raw 13.3 MB → blob 13.3 MB (không phình).

---

## ✅ VIỆC CÒN LẠI (bạn làm tiếp)

### A. Chốt Lớp 1 — bật strip + build thử (ưu tiên 1, nhanh)
1. Menu **`PokiClash/Bảo mật/Mã hoá ảnh hero khi build (bật tắt)`** → bật (có dấu ✓).
2. Build 1 bản **AndroidRelease** thử.
3. Kiểm: (a) build chạy xong không lỗi; (b) sau build, 183 ảnh gốc đã được **trả lại** vào Resources (git status sạch phần đó); (c) cài APK, vào trận xem **tướng hiện hình đúng** (atlas + chân dung).
4. Nếu đúng: mở APK bằng AssetStudio → không còn thấy ảnh atlas/portrait tướng (chỉ còn blob `enc/*.bytes` là rác mã hoá). Xong Lớp 1.
> Phần duy nhất chưa test là lúc **dời 183 file thật trong build**. Code theo đúng khuôn `BuildExclude` của mình nên rủi ro thấp, nhưng phải build thử 1 lần để chắc. Nếu hỏng giữa chừng: lần nạp code sau `ArtEncryptStrip` tự trả ảnh về (như `BuildExclude`).

### B. Lớp 2 — Che code / tên hàm (quan trọng nhất còn lại)
Android đã IL2CPP (C# → native, không decompile thẳng). Chỗ còn hở: **`global-metadata.dat`** → Il2CppDumper đọc ra tên class/hàm/field + chuỗi. Giải: dùng obfuscator mã nguồn mở cho IL2CPP (ví dụ **Obfuz**).
1. Cài Obfuz (UPM git URL hoặc package).
2. Bật, theo thứ tự ưu tiên: **(a) mã hoá global-metadata** (giấu tên hàm — thứ quan trọng nhất trên IL2CPP), **(b) mã hoá chuỗi + hằng số** (giấu khoá, resource key).
3. **Đổi tên (rename) làm DÈ DẶT** — whitelist:
   - Mọi field `[Serializable]` / `ScriptableObject` (serialize theo tên field vào `.asset`/prefab → đổi tên là vỡ): `HeroDef`, `CardDef`, `ZoneDef`, `BalanceConfig`, `AolaAnim`, `AtomikAsset`...
   - Save dùng MiniJson theo **chuỗi khoá cứng** (không theo tên field C#) nên đổi tên field C# KHÔNG ảnh hưởng khoá save — an tâm phần này.
   - Các key `Resources.Load("...")` là chuỗi, không phải tên type → đổi tên type không sao, nhưng **đừng để Obfuz đổi/ăn chuỗi** của chúng (hoặc whitelist).
4. Test KỸ sau khi bật (vào trận, lưu/đọc save, nhập liệu, mọi Resources.Load).
> Gọi mình khi bạn ở Unity, mình dựng cấu hình Obfuz + whitelist cùng bạn (dễ sai nếu làm một mình).

### C. Lớp 5 — Chống repack
1. **Tạo keystore phát hành trước** (hiện `AndroidKeystoreName` trống): Player Settings > Publishing Settings. Bắt buộc cho Google Play dù sao.
2. Implement kiểm chữ ký APK lúc chạy: lấy SHA-256 cert của app (PackageManager) so với hash cert phát hành; lệch → APK bị ký lại (đục) → từ chối chạy / gắn cờ. Cần device để test.
> Chưa làm vì phụ thuộc keystore của bạn. Gọi mình khi có keystore.

### D. (Tuỳ) Mở rộng Lớp 3 sang chỉ số khác
`HeroDb`/`CardDb`/`ZoneDb` (chỉ số tướng, thẻ, ải) vẫn đọc được bằng AssetStudio. Mã hoá được theo đúng cách balance, nhưng là refactor boot path (đang đọc list typed, phải chuyển sang giải mã JSON → FromJson) nên cần làm cẩn thận + test. Chưa làm.

---

## Lưu ý
- Khoá đối xứng trong app luôn recover được bởi cao thủ. **Lớp 2 (mã hoá metadata) mới là thứ giấu được chỗ xử lý khoá** của Lớp 1/3/4 → nên làm Lớp 2 để các lớp kia "cứng" hơn.
- Tiến độ/quyết định chi tiết: memory `bao-mat-mahoa-build` của Claude.
- Lệnh test lõi crypto ngoài Unity: xem đầu doc.
