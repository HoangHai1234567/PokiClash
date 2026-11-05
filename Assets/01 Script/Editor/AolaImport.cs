// Nhập hình tướng aola vào project thành prefab tướng, nén luôn lúc nhập (người dùng chốt 2026-11-02: không để hình chỉ bên
// AolaRipper). Nguồn: thư mục reskin của AolaRipper (FindDir); dạng nào cần lấy theo Assets/02 Data/Json/heroes.json.
// - Mỗi dạng → Assets/03 Art/Heroes/Resources/<dạng>/ (atlas và chân dung nạp khi cần bằng Resources.Load, xem AolaAnim):
//   - <dạng>_atlas.png: mọi hình mảnh, thu nhỏ về độ nét thật sự dùng rồi xếp chung một atlas (nén ASTC 8x8 trên Android, iOS).
//     Tướng được vẽ vào RenderTexture tối đa 1024 điểm cho khung 3,4 lần chiều cao dáng đứng (AolaSticker), nên dáng đứng cao
//     tối đa ~301 điểm; hình mảnh chỉ cần đủ nét cho mức đó, hình không có trong dáng đứng thu thêm (OtherScale); không mipmap,
//     xếp sát không làm tròn cỡ lên lũy thừa 2. Ma trận trong anim.json
//     giữ nguyên: AolaAnim.sizes ghi cỡ gốc của từng hình.
//   - <dạng>_portrait.png: chân dung (sprite, gốc ở chân), lưu PortraitSide x PortraitSide kéo giãn từ khung 4:5 (HeroPortrait
//     hiện lại đúng 4:5): Unity không nén ASTC ảnh có mipmap mà cạnh không là lũy thừa 2 (384x480 ra RGBA32, 960 KB mỗi ảnh);
//   - <dạng>_anim.bytes: anim.json gzip (bỏ danh sách đường dẫn hình);
//   - <dạng>.asset: AolaAnim trỏ tới ba thứ trên, kèm hình bóng dưới chân tìm sẵn.
// - Mỗi tướng → Assets/04 Prefabs/Heroes/<id>.prefab: AolaActor giữ các dạng theo thứ tự (Inspector hiện chân dung các dạng,
//   AolaActorEditor). Prefab đã có thì chỉ cập nhật danh sách dạng.
// - Danh mục → Assets/02 Data/HeroModels.asset, gắn vào UiAssets.heroes.
// Dạng đã nhập mà bản nguồn không đổi (thời điểm sửa anim.json, hình mảnh, chân dung) thì bỏ qua. Dạng không còn tướng nào dùng
// thì chỉ báo, không xoá.
// Dấu nguồn tính theo giờ sửa file nên khác nhau giữa hai máy: bản trong project kéo về qua git (nhập ở máy kia, có thể có phần
// bổ sung máy này chưa có) bị menu nhập thường đè bằng nguồn máy này. Menu "Nhập dạng aola có nguồn mới hơn" chỉ nhập dạng có
// nguồn sửa sau lần ghi asset trong project.
using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text.RegularExpressions;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public sealed class AolaImportPostprocessor : AssetPostprocessor
    {
        // đổi số khi cách nhập ảnh đổi: Unity nhập lại mọi ảnh tướng, nặng (2: atlas ASTC 8x8, chân dung vuông có mipmap ASTC 6x6;
        // 3: chân dung ASTC 8x8). Chỉ đổi mức nén chân dung thì dùng menu "Nhập lại chân dung tướng (mức nén chân dung)", đừng tăng số.
        public override uint GetVersion() => 3;

        // mức nén chân dung trên Android, iOS (người dùng 2026-11-04: 8x8 làm chân dung mờ, vỡ khối, nhất là bóng sẫm tướng trên bệ ải
        // chưa mở; so trong game bằng menu "Chân dung: thay thử mức nén", 5x5 sạch, 4x4 gần như ảnh gốc)
        public const TextureImporterFormat PortraitFormat = TextureImporterFormat.ASTC_5x5;

        void OnPreprocessTexture()
        {
            if (!assetPath.StartsWith(AolaImport.ArtDir + "/")) return;
            var ti = (TextureImporter)assetImporter;
            bool portrait = assetPath.EndsWith("_portrait.png");
            ti.textureType = portrait ? TextureImporterType.Sprite : TextureImporterType.Default;
            // atlas vẽ vào RenderTexture 1024 gần đúng cỡ đã thu nhỏ: không cần mipmap (bớt 1/3); chân dung hiện từ ô nhỏ trong UI
            ti.mipmapEnabled = portrait;
            ti.alphaIsTransparency = true;
            ti.wrapMode = TextureWrapMode.Clamp;
            ti.filterMode = FilterMode.Bilinear;
            ti.npotScale = TextureImporterNPOTScale.None;
            ti.maxTextureSize = portrait ? 512 : AolaImport.MaxAtlas;
            ti.textureCompression = TextureImporterCompression.Compressed;
            if (portrait)
            {
                var s = new TextureImporterSettings();
                ti.ReadTextureSettings(s);
                s.spriteMode = (int)SpriteImportMode.Single;
                s.spriteAlignment = (int)SpriteAlignment.Custom;
                s.spritePivot = new Vector2(0.5f, HeroArt.FootY);
                s.spritePixelsPerUnit = 100;
                s.spriteMeshType = SpriteMeshType.FullRect;
                ti.SetTextureSettings(s);
            }
            // dung lượng build (người dùng 2026-11-03: bản Android 60-70 MB): atlas ASTC 8x8 (2 bit mỗi điểm, tướng vẽ qua
            // RenderTexture gần 1:1 nên mờ nhẹ ở viền khó thấy). Chân dung PortraitFormat: hiện từ 100 tới 400 điểm qua mipmap, ở mức
            // mipmap nửa một khối 8x8 phủ 16x16 điểm ảnh gốc nên vỡ khối; 5x5 khoảng 226 KB mỗi ảnh (8x8 87 KB, 6x6 158 KB, 4x4 350 KB)
            SetPlatforms(ti, portrait ? PortraitFormat : TextureImporterFormat.ASTC_8x8);
        }

        public static void SetPlatforms(TextureImporter ti, TextureImporterFormat format)
        {
            foreach (var platform in new[] { "Android", "iPhone" })
            {
                var p = ti.GetPlatformTextureSettings(platform);
                p.overridden = true;
                p.maxTextureSize = ti.maxTextureSize;
                p.format = format;
                ti.SetPlatformTextureSettings(p);
            }
        }
    }

    public static class AolaImport
    {
        public const string ArtDir = "Assets/03 Art/Heroes";
        public const string ResDir = ArtDir + "/Resources";
        public const string PrefabDir = "Assets/04 Prefabs/Heroes";
        public const string LibraryPath = "Assets/02 Data/HeroModels.asset";
        const string HeroesJson = "Assets/02 Data/Json/heroes.json";
        public const int MaxAtlas = 4096;
        const int Padding = 4; // chừa giữa các hình trong atlas (lọc song tuyến, khối ASTC)
        const float PxPerHeight = 1024f / 3.4f;
        const float Margin = 1f;
        // hình không có trong dáng đứng (tư thế đánh, hiệu ứng chiêu): chạy nhanh, thu thêm. Bỏ lần nhập đầu (×1,25, không thu
        // thêm, PackTextures làm tròn lên lũy thừa 2) ra 516 triệu điểm ảnh; nay khoảng 144 triệu (ASTC 6x6 ~64 MB).
        const float OtherScale = 0.7f;
        // hình khung con của mảnh tự chạy (subframes.py bên AolaRipper, chars/c<id>_<k>.png: tóc, lốc nước, vệt chém, tia nổ):
        // mỗi hình chỉ hiện vài khung rồi đổi, nên thu thêm; khung con có trong dáng đứng nhìn lâu hơn nên thu nhẹ hơn
        const float SubIdleScale = 0.85f, SubOtherScale = 0.7f;
        static readonly Regex SubFrame = new Regex(@"[\\/]c\d+_\d+\.png$");
        public const int PortraitSide = 512; // chân dung lưu vuông (lũy thừa 2, có mipmap mới nén được)
        const string Version = "2"; // đổi khi cách nhập đổi, để nhập lại mọi dạng
        const string StandMark = "tam-"; // đầu dấu nguồn của dạng vẽ lại đang tạm mang hình gốc goc_<id>

        // ---------- thư mục reskin của AolaRipper ----------

        // Biến môi trường AOLA_RESKIN, hoặc EditorPrefs "PokiClash.AolaReskin" (menu PokiClash/Đặt thư mục aola); trống thì tự
        // tìm trên các ổ đĩa một lần (FindReskin) rồi ghi vào EditorPrefs.
        public const string PrefKey = "PokiClash.AolaReskin";
        static string foundDir;
        static bool searched;

        public static void ForgetDir()
        {
            searched = false;
            foundDir = null;
        }

        public static string FindDir()
        {
            var env = Environment.GetEnvironmentVariable("AOLA_RESKIN");
            if (!string.IsNullOrEmpty(env)) return env;
            if (searched) return foundDir;
            searched = true;
            var pref = EditorPrefs.GetString(PrefKey, "");
            foundDir = !string.IsNullOrEmpty(pref) && Directory.Exists(pref) ? pref : FindReskin();
            if (foundDir != null) EditorPrefs.SetString(PrefKey, foundDir);
            return foundDir;
        }

        // Thư mục reskin: dưới một thư mục tên bắt đầu bằng "Aola" (không phân biệt hoa thường) nằm cạnh thư mục project hoặc ở
        // gốc ổ đĩa, sâu tối đa 4 cấp, có thư mục con chứa export/anim.json.
        public static string FindReskin()
        {
            var parent = Path.GetDirectoryName(Path.GetDirectoryName(Application.dataPath));
            var tops = new List<string>();
            if (parent != null)
                try { tops.AddRange(Directory.GetDirectories(parent, "Aola*")); }
                catch (Exception) { }
            foreach (var drive in DriveInfo.GetDrives())
            {
                if (drive.DriveType != DriveType.Fixed || !drive.IsReady) continue;
                try { tops.AddRange(Directory.GetDirectories(drive.RootDirectory.FullName, "Aola*")); }
                catch (Exception) { }
            }
            foreach (var top in tops)
            {
                var hit = SearchReskin(top, 4);
                if (hit != null) return hit.Replace('\\', '/');
            }
            return null;
        }

        static string SearchReskin(string dir, int depth)
        {
            try
            {
                var r = Path.Combine(dir, "reskin");
                if (Directory.Exists(r))
                    foreach (var sub in Directory.GetDirectories(r))
                        if (File.Exists(Path.Combine(sub, "export", "anim.json"))) return r;
                if (depth <= 0) return null;
                foreach (var sub in Directory.GetDirectories(dir))
                {
                    var hit = SearchReskin(sub, depth - 1);
                    if (hit != null) return hit;
                }
            }
            catch (Exception) { }
            return null;
        }

        // ---------- nhập ----------

        [MenuItem("PokiClash/Tướng/Nhập hình tướng aola thành prefab", priority = 50)]
        static void MenuImport() => ImportAll(false);

        [MenuItem("PokiClash/Tướng/Nhập lại hết hình tướng aola", priority = 51)]
        static void MenuReimport() => ImportAll(true);

        [MenuItem("PokiClash/Tướng/Nhập dạng aola có nguồn mới hơn bản trong project", priority = 52)]
        static void MenuImportNewer() => ImportAll(false, true);

        // dạng có bản xuất kèm hình khung con (subframes.py): nhập lại hết, kể cả khi nguồn không đổi (cách thu nhỏ khung con đổi)
        [MenuItem("PokiClash/Tướng/Nhập lại dạng aola có hình khung con (mảnh tự chạy)", priority = 53)]
        static void MenuImportSub() => ImportAll(false, subOnly: true);

        [MenuItem("PokiClash/Tướng/Xếp lại atlas tướng đã nhập (không đọc nguồn)", priority = 54)]
        static void MenuRepack() => Repack();

        // Nhập lại mọi chân dung theo AolaImportPostprocessor.PortraitFormat, không đụng atlas (không tăng GetVersion: tăng thì nhập lại
        // mọi ảnh tướng). Ghi mức nén vào .meta của từng chân dung nên máy kia kéo git về cũng tự nhập lại chân dung.
        [MenuItem("PokiClash/Tướng/Nhập lại chân dung tướng (mức nén chân dung)", priority = 55)]
        static void MenuReimportPortraits()
        {
            var paths = AssetDatabase.FindAssets("t:Texture2D", new[] { ResDir }).Select(AssetDatabase.GUIDToAssetPath)
                .Where(x => x.EndsWith("_portrait.png")).ToList();
            int changed = 0;
            try
            {
                AssetDatabase.StartAssetEditing();
                foreach (var path in paths)
                {
                    var ti = (TextureImporter)AssetImporter.GetAtPath(path);
                    if (ti.GetPlatformTextureSettings("Android").format == AolaImportPostprocessor.PortraitFormat
                        && ti.GetPlatformTextureSettings("iPhone").format == AolaImportPostprocessor.PortraitFormat) continue;
                    AolaImportPostprocessor.SetPlatforms(ti, AolaImportPostprocessor.PortraitFormat);
                    ti.SaveAndReimport();
                    changed++;
                }
            }
            finally
            {
                AssetDatabase.StopAssetEditing();
            }
            Debug.Log($"[Tướng] Chân dung {AolaImportPostprocessor.PortraitFormat}: nhập lại {changed}/{paths.Count} ảnh.");
        }

        // Xếp lại atlas đã có trong project bằng Pack: cắt từng hình theo uvs từ PNG atlas trong project (bản chưa nén), xếp lại, ghi
        // PNG và uvs. Không đọc nguồn AolaRipper nên dùng được cho dạng nhập ở máy khác; không đổi dấu nguồn, anim, chân dung.
        public static string Repack()
        {
            long before = 0, after = 0;
            int done = 0, same = 0;
            var guids = AssetDatabase.FindAssets("t:AolaAnim", new[] { ResDir });
            try
            {
                AssetDatabase.StartAssetEditing();
                try
                {
                    for (int k = 0; k < guids.Length; k++)
                    {
                        var a = AssetDatabase.LoadAssetAtPath<AolaAnim>(AssetDatabase.GUIDToAssetPath(guids[k]));
                        if (!a || a.uvs == null || a.uvs.Length == 0 || string.IsNullOrEmpty(a.res)) continue;
                        if (EditorUtility.DisplayCancelableProgressBar("Xếp lại atlas tướng", $"{a.name} ({k + 1}/{guids.Length})", (float)k / guids.Length))
                            throw new OperationCanceledException();
                        var png = Path.Combine(Application.dataPath, "..", ResDir, a.res + "_atlas.png");
                        if (!File.Exists(png)) continue;
                        var src = new Texture2D(2, 2, TextureFormat.RGBA32, false);
                        if (!src.LoadImage(File.ReadAllBytes(png)))
                        {
                            UnityEngine.Object.DestroyImmediate(src);
                            continue;
                        }
                        int W = src.width, H = src.height;
                        var all = src.GetPixels32();
                        UnityEngine.Object.DestroyImmediate(src);
                        var parts = new Texture2D[a.uvs.Length];
                        for (int i = 0; i < parts.Length; i++)
                        {
                            var u = a.uvs[i];
                            int x = Mathf.RoundToInt(u.x * W), y = Mathf.RoundToInt(u.y * H);
                            int w = Math.Max(1, Mathf.RoundToInt(u.width * W)), h = Math.Max(1, Mathf.RoundToInt(u.height * H));
                            var px = new Color32[w * h];
                            for (int row = 0; row < h; row++) Array.Copy(all, (y + row) * W + x, px, row * w, w);
                            parts[i] = new Texture2D(w, h, TextureFormat.RGBA32, false);
                            parts[i].SetPixels32(px);
                        }
                        var uvs = new Rect[parts.Length];
                        var atlas = Pack(parts, uvs, out _);
                        foreach (var t in parts) UnityEngine.Object.DestroyImmediate(t);
                        before += (long)W * H;
                        if (!atlas || (long)atlas.width * atlas.height >= (long)W * H)
                        {
                            after += (long)W * H;
                            same++;
                            if (atlas) UnityEngine.Object.DestroyImmediate(atlas);
                            continue;
                        }
                        after += (long)atlas.width * atlas.height;
                        Write(png, atlas.EncodeToPNG());
                        UnityEngine.Object.DestroyImmediate(atlas);
                        a.uvs = uvs;
                        EditorUtility.SetDirty(a);
                        done++;
                        if (k % 10 == 9) GC.Collect();
                    }
                }
                finally
                {
                    AssetDatabase.StopAssetEditing();
                }
                AssetDatabase.SaveAssets();
                EditorUtility.DisplayProgressBar("Xếp lại atlas tướng", "Nén ảnh...", 0.95f);
                AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
                var summary = $"[Tướng aola] Xếp lại {done} atlas ({same} giữ nguyên): {before / 1e6:0.0} → {after / 1e6:0.0} triệu điểm ảnh " +
                              $"(ASTC 8x8 {before / 4 / 1048576f:0.0} → {after / 4 / 1048576f:0.0} MB).";
                Debug.Log(summary);
                return summary;
            }
            catch (OperationCanceledException)
            {
                Debug.LogWarning("[Tướng aola] Đã dừng xếp lại atlas; atlas đã xếp xong vẫn giữ, chạy lại menu để xếp tiếp.");
                AssetDatabase.SaveAssets();
                AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
                return "đã dừng";
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }

        // Batchmode: Unity -batchmode -projectPath <dự án> -executeMethod PokiClash.EditorTools.AolaImport.Batch [-force]
        public static void Batch()
        {
            int code = 0;
            try { ImportAll(Environment.GetCommandLineArgs().Contains("-force")); }
            catch (Exception e)
            {
                Debug.LogException(e);
                code = 1;
            }
            EditorApplication.Exit(code);
        }

        // Trả tóm tắt (cũng in ra Console). newerOnly: chỉ nhập dạng có nguồn sửa sau lần ghi anim trong project; subOnly: chỉ
        // nhập (luôn nhập) dạng có hình khung con.
        public static string ImportAll(bool force, bool newerOnly = false, bool subOnly = false)
        {
            var reskin = FindDir();
            if (string.IsNullOrEmpty(reskin) || !Directory.Exists(reskin))
            {
                Debug.LogError("[Tướng aola] Không tìm thấy thư mục reskin của AolaRipper (menu PokiClash/Tự tìm thư mục aola).");
                return "không có thư mục reskin";
            }
            MoveIntoResources();
            var heroes = ReadHeroes();
            var forms = heroes.SelectMany(h => h.forms).Distinct().ToList();
            var made = new List<string>();
            var missing = new List<string>();
            var stands = new List<string>();
            var kept = new List<string>();
            var log = new List<string>();
            long before = 0, after = 0, pixels = 0;
            try
            {
                // 1. ghi file ảnh và animation của các dạng đổi (nhập một lượt ở bước 2)
                var pending = new List<(string form, Pending p)>();
                AssetDatabase.StartAssetEditing();
                try
                {
                    for (int i = 0; i < forms.Count; i++)
                    {
                        var form = forms[i];
                        if (EditorUtility.DisplayCancelableProgressBar("Nhập hình tướng aola", $"{form} ({i + 1}/{forms.Count})", (float)i / forms.Count))
                            throw new OperationCanceledException();
                        var dir = Path.Combine(reskin, form);
                        var old = AssetDatabase.LoadAssetAtPath<AolaAnim>(AnimPath(form));
                        var mark = "";
                        if (!File.Exists(Path.Combine(dir, "export", "anim.json")))
                        {
                            // máy này không có bản vẽ lại nhưng asset đã nhập từ bản vẽ lại ở máy khác (dấu không có StandMark): giữ,
                            // không đè bằng hình gốc
                            if (old && !string.IsNullOrEmpty(old.source) && !old.source.StartsWith(StandMark) && old.anim)
                            {
                                kept.Add(form);
                                continue;
                            }
                            // dạng đang vẽ lại (<hệ>_<id>) chưa xuất: tạm lấy hình gốc goc_<id> cùng rig; xuất xong thì dấu bản đổi, tự nhập lại
                            var id = Regex.Match(form, @"^[a-z]+_(\d+)$");
                            var stand = id.Success ? Path.Combine(reskin, "goc_" + id.Groups[1].Value) : null;
                            if (stand == null || !File.Exists(Path.Combine(stand, "export", "anim.json")))
                            {
                                missing.Add(form);
                                continue;
                            }
                            dir = stand;
                            mark = StandMark;
                            stands.Add($"{form} ← {Path.GetFileName(stand)}");
                        }
                        var stamp = mark + Stamp(dir, out long sourceTicks);
                        if (subOnly)
                        {
                            if (!HasSubframes(dir)) continue;
                        }
                        else if (newerOnly)
                        {
                            if (old && old.anim && sourceTicks <= ProjectTicks(form)) continue;
                        }
                        else if (!force && old && old.source == stamp && old.anim && old.LoadAtlas()) continue;
                        var p = Write(dir, form, stamp, out string note);
                        before += p.bytesBefore;
                        after += p.bytesAfter;
                        pixels += p.pixels;
                        if (note != null) log.Add($"{form}: {note}");
                        pending.Add((form, p));
                    }
                }
                finally
                {
                    AssetDatabase.StopAssetEditing();
                }
                // 2. nhập (nén ASTC theo AolaImportPostprocessor) rồi dựng AolaAnim
                EditorUtility.DisplayProgressBar("Nhập hình tướng aola", "Nén ảnh...", 0.9f);
                AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
                foreach (var (form, p) in pending)
                {
                    var a = AssetDatabase.LoadAssetAtPath<AolaAnim>(AnimPath(form));
                    bool fresh = !a;
                    if (fresh) a = ScriptableObject.CreateInstance<AolaAnim>();
                    a.Setup($"{form}/{form}", AssetDatabase.LoadAssetAtPath<TextAsset>($"{ResDir}/{form}/{form}_anim.bytes"),
                        p.sizes, p.uvs, p.shadow, p.stamp);
                    if (fresh) AssetDatabase.CreateAsset(a, AnimPath(form));
                    else EditorUtility.SetDirty(a);
                    made.Add(form);
                }
                AssetDatabase.SaveAssets();

                // 3. prefab tướng và danh mục
                EditorUtility.DisplayProgressBar("Nhập hình tướng aola", "Prefab tướng...", 0.95f);
                var prefabs = new List<AolaActor>();
                foreach (var h in heroes)
                {
                    var anims = h.forms.Select(f => AssetDatabase.LoadAssetAtPath<AolaAnim>(AnimPath(f))).ToArray();
                    if (anims.All(x => !x)) continue;
                    prefabs.Add(SavePrefab(h.id, anims));
                }
                var lib = AssetDatabase.LoadAssetAtPath<HeroModels>(LibraryPath);
                if (!lib)
                {
                    lib = ScriptableObject.CreateInstance<HeroModels>();
                    AssetDatabase.CreateAsset(lib, LibraryPath);
                }
                lib.Setup(prefabs.ToArray());
                EditorUtility.SetDirty(lib);
                foreach (var guid in AssetDatabase.FindAssets("t:UiAssets"))
                {
                    var ui = AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(guid));
                    if (!ui || ui.heroes == lib) continue;
                    ui.heroes = lib;
                    EditorUtility.SetDirty(ui);
                }
                AssetDatabase.SaveAssets();

                var used = new HashSet<string>(forms);
                var stale = Directory.Exists(ResDir)
                    ? Directory.GetDirectories(ResDir).Select(Path.GetFileName).Where(f => !used.Contains(f)).ToList()
                    : new List<string>();
                var summary = $"[Tướng aola] {prefabs.Count}/{heroes.Count} prefab tướng, {forms.Count - missing.Count}/{forms.Count} dạng có hình; " +
                              $"nhập mới {made.Count} dạng (hình mảnh {before / 1048576f:0.0} MB PNG gốc → atlas {after / 1048576f:0.0} MB PNG, " +
                              $"{pixels / 1e6:0.0} triệu điểm ảnh, ASTC 8x8 khoảng {pixels * 16 / 64 / 1048576f:0} MB).";
                if (missing.Count > 0) summary += $"\nChưa xuất anim.json bên AolaRipper: {string.Join(", ", missing)}";
                if (stands.Count > 0) summary += $"\nChưa có hình vẽ lại, tạm dùng hình gốc aola: {string.Join(", ", stands)}";
                if (kept.Count > 0) summary += $"\nMáy này không có bản vẽ lại, giữ hình đã nhập từ máy khác: {string.Join(", ", kept)}";
                if (stale.Count > 0) summary += $"\nDạng không còn tướng nào dùng (chưa xoá): {string.Join(", ", stale)}";
                foreach (var l in log) Debug.LogWarning("[Tướng aola] " + l);
                Debug.Log(summary);
                return summary;
            }
            catch (OperationCanceledException)
            {
                Debug.LogWarning("[Tướng aola] Đã dừng giữa chừng; chạy lại menu để nhập tiếp.");
                return "đã dừng";
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }

        static string AnimPath(string form) => $"{ResDir}/{form}/{form}.asset";

        // bản nhập đầu (2026-11-02) ghi thẳng vào Heroes/<dạng>: dời vào Resources, giữ GUID
        static void MoveIntoResources()
        {
            if (!AssetDatabase.IsValidFolder(ArtDir)) AssetDatabase.CreateFolder("Assets/03 Art", "Heroes");
            if (!AssetDatabase.IsValidFolder(ResDir)) AssetDatabase.CreateFolder(ArtDir, "Resources");
            foreach (var dir in AssetDatabase.GetSubFolders(ArtDir))
            {
                var name = Path.GetFileName(dir);
                if (name == "Resources") continue;
                var err = AssetDatabase.MoveAsset(dir, $"{ResDir}/{name}");
                if (!string.IsNullOrEmpty(err)) Debug.LogWarning($"[Tướng aola] Không dời được {dir}: {err}");
            }
        }

        sealed class HeroEntry
        {
            public string id;
            public List<string> forms = new();
        }

        static List<HeroEntry> ReadHeroes()
        {
            var root = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(HeroesJson));
            var list = new List<HeroEntry>();
            // lính ải (minions.ts) cùng dạng tướng, nằm ở mảng "minions" nếu bản xuất có; prefab theo id lính
            var all = ((List<object>)root["heroes"]).Concat(root.TryGetValue("minions", out var m) && m is List<object> ms ? ms : new List<object>());
            foreach (Dictionary<string, object> h in all)
            {
                var e = new HeroEntry { id = (string)h["id"] };
                if (h.TryGetValue("forms", out var fs) && fs is List<object> forms)
                    foreach (Dictionary<string, object> f in forms)
                        if (f.TryGetValue("aola", out var a) && a is string s && s.Length > 0) e.forms.Add(s);
                if (e.forms.Count == 0 && h.TryGetValue("aola", out var a0) && a0 is string s0 && s0.Length > 0) e.forms.Add(s0);
                if (e.forms.Count > 0) list.Add(e);
            }
            return list;
        }

        // giờ ghi anim của dạng trong project (lần nhập ở máy này, hoặc lúc git kéo về), 0 nếu chưa có
        static long ProjectTicks(string form)
        {
            var f = new FileInfo(Path.Combine(Application.dataPath, "..", ResDir, form, form + "_anim.bytes"));
            return f.Exists ? f.LastWriteTimeUtc.Ticks : 0;
        }

        // dấu bản nguồn: thời điểm sửa và cỡ của anim.json, chân dung, mọi hình mảnh; ticks: thời điểm sửa mới nhất
        static string Stamp(string dir, out long ticks)
        {
            var anim = Path.Combine(dir, "export", "anim.json");
            var json = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(anim));
            long t = 0, n = 0;
            void Add(string f)
            {
                var fi = new FileInfo(f);
                if (!fi.Exists) return;
                t = Math.Max(t, fi.LastWriteTimeUtc.Ticks);
                n += fi.Length;
            }
            Add(anim);
            Add(Path.Combine(dir, "export", "portrait.png"));
            foreach (var s in (List<object>)json["sprites"]) Add(Path.GetFullPath(Path.Combine(dir, (string)s)));
            ticks = t;
            return $"v{Version}-{t}-{n}";
        }

        // bản xuất có hình khung con: thư mục hình mảnh (của hình đầu tiên) có subframes.json
        static bool HasSubframes(string dir)
        {
            var json = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(Path.Combine(dir, "export", "anim.json")));
            if (!(((List<object>)json["sprites"]).FirstOrDefault() is string first)) return false;
            var chars = Path.GetDirectoryName(Path.GetFullPath(Path.Combine(dir, first)));
            return chars != null && File.Exists(Path.Combine(chars, "subframes.json"));
        }

        sealed class Pending
        {
            public string stamp;
            public Vector2[] sizes;
            public Rect[] uvs;
            public int shadow = -1;
            public long bytesBefore, bytesAfter, pixels;
        }

        // Ghi <dạng>_atlas.png, <dạng>_portrait.png, <dạng>_anim.bytes; note: ghi chú nếu atlas bị ép nhỏ.
        static Pending Write(string dir, string form, string stamp, out string note)
        {
            note = null;
            var animPath = Path.Combine(dir, "export", "anim.json");
            var json = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(animPath));
            var paths = ((List<object>)json["sprites"]).Select(s => Path.GetFullPath(Path.Combine(dir, (string)s))).ToList();
            var clips = (Dictionary<string, object>)json["clips"];
            var p = new Pending { stamp = stamp, sizes = new Vector2[paths.Count], uvs = new Rect[paths.Count] };

            // hình gốc
            var src = new Texture2D[paths.Count];
            for (int i = 0; i < paths.Count; i++)
            {
                if (!File.Exists(paths[i])) continue;
                var bytes = File.ReadAllBytes(paths[i]);
                p.bytesBefore += bytes.Length;
                var t = new Texture2D(2, 2, TextureFormat.RGBA32, false);
                if (!t.LoadImage(bytes))
                {
                    UnityEngine.Object.DestroyImmediate(t);
                    continue;
                }
                src[i] = t;
                p.sizes[i] = new Vector2(t.width, t.height);
            }

            // độ phóng lớn nhất mỗi hình được vẽ ra, quy ra điểm RenderTexture lớn nhất (dáng đứng cao PxPerHeight)
            var idleFrames = clips.TryGetValue(AolaActor.Idle, out var idleObj) ? (List<object>)((Dictionary<string, object>)idleObj)["frames"] : null;
            double top = double.MaxValue, bottom = double.MinValue;
            if (idleFrames != null && idleFrames.Count > 0)
                foreach (List<object> row in (List<object>)idleFrames[0])
                {
                    var z = p.sizes[Convert.ToInt32(row[0])];
                    double b = Convert.ToDouble(row[2]), d = Convert.ToDouble(row[4]), ty = Convert.ToDouble(row[6]);
                    foreach (var (x, y) in new[] { (0f, 0f), (z.x, 0f), (0f, z.y), (z.x, z.y) })
                    {
                        double py = b * x + d * y + ty;
                        top = Math.Min(top, py);
                        bottom = Math.Max(bottom, py);
                    }
                }
            double k = bottom > top ? PxPerHeight / Math.Max(1, bottom - top) * Margin : 1;
            var need = new double[paths.Count];
            foreach (var clip in clips.Values)
                foreach (List<object> frame in (List<object>)((Dictionary<string, object>)clip)["frames"])
                    foreach (List<object> row in frame)
                    {
                        int s = Convert.ToInt32(row[0]);
                        double a = Convert.ToDouble(row[1]), b = Convert.ToDouble(row[2]), c = Convert.ToDouble(row[3]), d = Convert.ToDouble(row[4]);
                        need[s] = Math.Max(need[s], Math.Max(Math.Sqrt(a * a + b * b), Math.Sqrt(c * c + d * d)) * k);
                    }
            var inIdle = new HashSet<int>();
            if (idleFrames != null)
                foreach (List<object> frame in idleFrames)
                    foreach (List<object> row in frame)
                        inIdle.Add(Convert.ToInt32(row[0]));
            for (int i = 0; i < need.Length; i++)
            {
                bool idle = inIdle.Contains(i);
                if (!idle) need[i] *= OtherScale;
                if (SubFrame.IsMatch(paths[i])) need[i] *= idle ? SubIdleScale : SubOtherScale;
            }

            // bóng dưới chân: trong 3 hình đầu của khung đầu dáng đứng, tâm nằm ở 30% dưới của khung (2026-11-05: goc_215 có vệt gió
            // xám bè ngang ngang lưng bị nhận nhầm làm bóng, điểm neo chân lên lưng nên con bị phóng to, lệch xuống)
            if (idleFrames != null && idleFrames.Count > 0)
            {
                var first = (List<object>)idleFrames[0];
                for (int i = 0; i < Math.Min(3, first.Count); i++)
                {
                    var row = (List<object>)first[i];
                    int s = Convert.ToInt32(row[0]);
                    var z = p.sizes[s];
                    double cy = Convert.ToDouble(row[2]) * z.x / 2 + Convert.ToDouble(row[4]) * z.y / 2 + Convert.ToDouble(row[6]);
                    if (src[s] && IsShadow(src[s]) && cy >= top + 0.7 * (bottom - top))
                    {
                        p.shadow = s;
                        break;
                    }
                }
            }

            // thu nhỏ rồi xếp atlas (hình không dùng tới hoặc hỏng thành 1 điểm trong suốt); không vừa MaxAtlas thì thu thêm
            // mọi hình rồi xếp lại
            Texture2D[] small = null;
            Texture2D atlas = null;
            double extra = 1;
            for (int round = 0; round < 6 && !atlas; round++)
            {
                if (small != null)
                    foreach (var t in small)
                        if (t && !src.Contains(t)) UnityEngine.Object.DestroyImmediate(t);
                small = new Texture2D[paths.Count];
                for (int i = 0; i < paths.Count; i++)
                {
                    var t = src[i];
                    double s = Math.Min(1, need[i] * extra);
                    if (!t || s <= 0)
                    {
                        small[i] = new Texture2D(1, 1, TextureFormat.RGBA32, false);
                        small[i].SetPixel(0, 0, Color.clear);
                        small[i].Apply();
                        continue;
                    }
                    int nw = Math.Max(1, (int)Math.Round(t.width * s)), nh = Math.Max(1, (int)Math.Round(t.height * s));
                    small[i] = nw < t.width || nh < t.height ? Shrink(t, nw, nh) : t;
                }
                atlas = Pack(small, p.uvs, out int needH);
                if (!atlas)
                {
                    extra *= Math.Sqrt((double)MaxAtlas / needH) * 0.97;
                    note = $"atlas không vừa {MaxAtlas}, mọi hình thu thêm còn {extra:0.00}";
                }
            }
            if (!atlas) throw new Exception($"{form}: không xếp được atlas");
            var outDir = Path.Combine(Application.dataPath, "..", ResDir, form);
            Directory.CreateDirectory(outDir);
            var png = atlas.EncodeToPNG();
            p.bytesAfter = png.Length;
            p.pixels = (long)atlas.width * atlas.height;
            Write(Path.Combine(outDir, form + "_atlas.png"), png);

            // chân dung: khung 4:5 kéo giãn thành PortraitSide x PortraitSide
            var portraitSrc = Path.Combine(dir, "export", "portrait.png");
            if (File.Exists(portraitSrc))
            {
                var t = new Texture2D(2, 2, TextureFormat.RGBA32, false);
                if (t.LoadImage(File.ReadAllBytes(portraitSrc)))
                {
                    var s = Resize(t, PortraitSide, PortraitSide);
                    Write(Path.Combine(outDir, form + "_portrait.png"), s.EncodeToPNG());
                    if (s != t) UnityEngine.Object.DestroyImmediate(s);
                }
                UnityEngine.Object.DestroyImmediate(t);
            }

            // animation: bỏ đường dẫn hình (AolaAnim giữ cỡ và chỗ trong atlas), nén gzip
            json.Remove("sprites");
            var text = System.Text.Encoding.UTF8.GetBytes(MiniJson.Write(json));
            using (var o = new FileStream(Path.Combine(outDir, form + "_anim.bytes"), FileMode.Create))
            using (var z = new GZipStream(o, System.IO.Compression.CompressionLevel.Optimal))
                z.Write(text, 0, text.Length);

            foreach (var t in src.Concat(small).Distinct())
                if (t) UnityEngine.Object.DestroyImmediate(t);
            UnityEngine.Object.DestroyImmediate(atlas);
            return p;
        }

        // Xếp hình bằng MaxRects (thử vài chiều rộng quanh căn diện tích, mỗi chiều rộng tìm chiều cao nhỏ nhất xếp vừa, lấy atlas
        // nhỏ nhất); cỡ atlas không làm tròn lên lũy thừa 2 (ASTC không cần, PackTextures làm tròn nên phí gần nửa). Xếp theo hàng
        // như trước chỉ lấp được 79% atlas (2026-11-04: 196,6 triệu điểm ảnh cho 154,5 triệu điểm hình và lề).
        // Không vừa MaxAtlas: null, needH là chiều cao cần nếu rộng MaxAtlas.
        static Texture2D Pack(Texture2D[] tex, Rect[] uvs, out int needH)
        {
            int n = tex.Length;
            var ws = tex.Select(t => t.width + Padding).ToArray();
            var hs = tex.Select(t => t.height + Padding).ToArray();
            long area = 0;
            int maxW = 1, maxH = 1;
            for (int i = 0; i < n; i++)
            {
                area += (long)ws[i] * hs[i];
                maxW = Math.Max(maxW, ws[i]);
                maxH = Math.Max(maxH, hs[i]);
            }
            var order = Enumerable.Range(0, n).OrderByDescending(i => Math.Max(ws[i], hs[i])).ThenByDescending(i => ws[i] * hs[i]).ToArray();
            var pos = new (int x, int y)[n];
            var tryPos = new (int x, int y)[n];
            bool Fits(int w, int h)
            {
                var bin = new MaxRects(w, h);
                foreach (int i in order)
                {
                    if (!bin.Insert(ws[i], hs[i], out var r)) return false;
                    tryPos[i] = (r.x, r.y);
                }
                return true;
            }
            int W = 0, H = 0;
            double side = Math.Sqrt(area);
            foreach (var f in new[] { 0.85, 0.92, 1.0, 1.08, 1.17, 1.3 })
            {
                int w = Ceil4(Math.Min(MaxAtlas, Math.Max(maxW, (int)Math.Ceiling(side * f))));
                int lo = Ceil4(Math.Max(maxH, (int)(area / w))), hi = MaxAtlas;
                if (lo > hi || W > 0 && (long)w * lo >= (long)W * H) continue;
                if (!Fits(w, hi)) continue;
                while (hi - lo > 4)
                {
                    int mid = Ceil4((lo + hi) / 2);
                    if (mid >= hi) break;
                    if (Fits(w, mid)) hi = mid;
                    else lo = mid;
                }
                if (W > 0 && (long)w * hi >= (long)W * H) continue;
                Fits(w, hi);
                Array.Copy(tryPos, pos, n);
                W = w;
                H = hi;
            }
            // không vừa: chiều cao cần ước theo diện tích, luôn quá MaxAtlas để vòng gọi thu nhỏ thêm
            needH = W > 0 ? H : Math.Max(MaxAtlas + 64, (int)Math.Ceiling(area * 1.15 / MaxAtlas));
            if (W == 0) return null;
            var px = new Color32[W * H];
            for (int i = 0; i < n; i++)
            {
                var t = tex[i];
                var s = t.GetPixels32();
                int ox = pos[i].x + Padding / 2, oy = pos[i].y + Padding / 2;
                for (int y = 0; y < t.height; y++) Array.Copy(s, y * t.width, px, (oy + y) * W + ox, t.width);
                uvs[i] = new Rect((float)ox / W, (float)oy / H, (float)t.width / W, (float)t.height / H);
            }
            var atlas = new Texture2D(W, H, TextureFormat.RGBA32, false);
            atlas.SetPixels32(px);
            atlas.Apply();
            return atlas;
        }

        static int Ceil4(int v) => (v + 3) & ~3;

        // MaxRects (Jukka Jylänki 2010): giữ mọi ô trống tối đa, đặt hình vào ô có cạnh ngắn còn thừa ít nhất; không xoay hình
        sealed class MaxRects
        {
            readonly List<RectInt> free = new();
            readonly List<RectInt> split = new();

            public MaxRects(int w, int h) => free.Add(new RectInt(0, 0, w, h));

            public bool Insert(int w, int h, out RectInt r)
            {
                r = default;
                int bestShort = int.MaxValue, bestLong = int.MaxValue;
                foreach (var f in free)
                {
                    if (f.width < w || f.height < h) continue;
                    int dw = f.width - w, dh = f.height - h;
                    int s = Math.Min(dw, dh), l = Math.Max(dw, dh);
                    if (s > bestShort || s == bestShort && l >= bestLong) continue;
                    bestShort = s;
                    bestLong = l;
                    r = new RectInt(f.x, f.y, w, h);
                }
                if (bestShort == int.MaxValue) return false;
                Place(r);
                return true;
            }

            // cắt mọi ô trống chạm hình thành tối đa bốn ô quanh nó, bỏ ô mới nằm gọn trong ô khác (ô cũ với nhau đã gọn từ trước)
            void Place(RectInt u)
            {
                split.Clear();
                for (int i = free.Count - 1; i >= 0; i--)
                {
                    var f = free[i];
                    if (u.x >= f.xMax || u.xMax <= f.x || u.y >= f.yMax || u.yMax <= f.y) continue;
                    free.RemoveAt(i);
                    if (u.x > f.x) split.Add(new RectInt(f.x, f.y, u.x - f.x, f.height));
                    if (u.xMax < f.xMax) split.Add(new RectInt(u.xMax, f.y, f.xMax - u.xMax, f.height));
                    if (u.y > f.y) split.Add(new RectInt(f.x, f.y, f.width, u.y - f.y));
                    if (u.yMax < f.yMax) split.Add(new RectInt(f.x, u.yMax, f.width, f.yMax - u.yMax));
                }
                for (int i = 0; i < split.Count; i++)
                {
                    var a = split[i];
                    bool inside = false;
                    for (int j = 0; j < split.Count && !inside; j++)
                        inside = j != i && Contains(split[j], a) && (!split[j].Equals(a) || j < i);
                    for (int j = 0; j < free.Count && !inside; j++)
                        inside = Contains(free[j], a);
                    if (!inside) free.Add(a);
                }
            }

            static bool Contains(RectInt a, RectInt b) => b.x >= a.x && b.y >= a.y && b.xMax <= a.xMax && b.yMax <= a.yMax;
        }

        // Bóng: hình xám không màu, nửa trong suốt, bè ngang. Bóng trong 79 dạng đã xuất: độ bão hòa 0, alpha 75–130, rộng/cao
        // từ 1.75 (677); hình xám khác đều đục (alpha ≥ 240).
        static bool IsShadow(Texture2D t)
        {
            if (t.width < t.height * 1.5f) return false;
            var px = t.GetPixels32();
            long n = 0, alpha = 0, sat = 0;
            for (int i = 0; i < px.Length; i += 5)
            {
                var c = px[i];
                if (c.a <= 10) continue;
                n++;
                alpha += c.a;
                sat += Mathf.Max(c.r, Mathf.Max(c.g, c.b)) - Mathf.Min(c.r, Mathf.Min(c.g, c.b));
            }
            return n > 0 && sat / n < 8 && alpha / n < 170;
        }

        // ghi file, thử lại khi Unity còn giữ file (Win32 1224: đang ánh xạ vào bộ nhớ lúc băm hay xem trước ảnh vừa đổi)
        static void Write(string path, byte[] bytes)
        {
            for (int i = 0; ; i++)
                try
                {
                    File.WriteAllBytes(path, bytes);
                    return;
                }
                catch (IOException) when (i < 20)
                {
                    GC.Collect();
                    GC.WaitForPendingFinalizers();
                    System.Threading.Thread.Sleep(150);
                }
        }

        static Texture2D Shrink(Texture2D t, int nw, int nh) => Scaled(t, nw, nh, ImageScale.Down);

        // đổi cỡ bất kỳ (mỗi chiều thu nhỏ hoặc phóng to); cùng cỡ thì trả lại t
        static Texture2D Resize(Texture2D t, int nw, int nh) =>
            nw == t.width && nh == t.height ? t : Scaled(t, nw, nh, ImageScale.Resize);

        static Texture2D Scaled(Texture2D t, int nw, int nh, Func<byte[], int, int, int, int, byte[]> scale)
        {
            var px = t.GetPixels32();
            var rgba = new byte[px.Length * 4];
            for (int i = 0; i < px.Length; i++)
            {
                rgba[i * 4] = px[i].r;
                rgba[i * 4 + 1] = px[i].g;
                rgba[i * 4 + 2] = px[i].b;
                rgba[i * 4 + 3] = px[i].a;
            }
            var o = scale(rgba, t.width, t.height, nw, nh);
            var res = new Texture2D(nw, nh, TextureFormat.RGBA32, false);
            var cols = new Color32[nw * nh];
            for (int i = 0; i < cols.Length; i++) cols[i] = new Color32(o[i * 4], o[i * 4 + 1], o[i * 4 + 2], o[i * 4 + 3]);
            res.SetPixels32(cols);
            res.Apply();
            return res;
        }

        // Prefab tướng: AolaActor ở gốc giữ các dạng.
        static AolaActor SavePrefab(string id, AolaAnim[] forms)
        {
            Directory.CreateDirectory(Path.Combine(Application.dataPath, "..", PrefabDir));
            var path = $"{PrefabDir}/{id}.prefab";
            bool exists = File.Exists(Path.Combine(Application.dataPath, "..", path));
            var root = exists ? PrefabUtility.LoadPrefabContents(path) : new GameObject(id);
            try
            {
                var actor = root.GetComponent<AolaActor>(); // Editor trả "null giả" khi thiếu component: không dùng ??
                if (!actor) actor = root.AddComponent<AolaActor>();
                // bản nhập đầu có con xem trước trỏ thẳng tới chân dung (kéo mọi chân dung vào bộ nhớ lúc mở game): bỏ
                var pv = root.transform.Find("xem_truoc");
                if (pv) UnityEngine.Object.DestroyImmediate(pv.gameObject);
                actor.Setup(forms);
                PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                if (exists) PrefabUtility.UnloadPrefabContents(root);
                else UnityEngine.Object.DestroyImmediate(root);
            }
            return AssetDatabase.LoadAssetAtPath<AolaActor>(path);
        }
    }
}
