// Ảnh: (1) mọi PNG/JPG trong Assets/03 Art (trừ ảnh nướng sẵn Baked/) tự đặt kiểu Sprite, không mipmap, nén ASTC trên Android;
// (2) menu "PokiClash/Nhập ảnh ArtGen": đọc ArtGen/<gói>/inbox/. Ảnh sheet (bảng Sheets bên dưới, theo PROMPTS.md của gói)
//     được cắt theo lưới thành từng ảnh, gọt mép trong suốt; ảnh đơn chép nguyên tên. Ảnh không có nền trong suốt thì
//     cắt nền trắng nối với mép. Đặt viền 9-slice cho ảnh khung (btn_, panel_, card_, bar_, chip_...), dựng lại ArtLibrary.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public sealed class ArtPostprocessor : AssetPostprocessor
    {
        void OnPreprocessTexture()
        {
            if (!assetPath.StartsWith(ArtImporter.ArtDir + "/")) return;
            // mặt máy bi nướng sẵn là ảnh màu thường (không mã hoá kênh như Baked/Sketch): nén ASTC 6x6 như ảnh gen (RGBA32 920x1360
            // tốn 4,8 MB, nén còn 0,55 MB); cách nhập khác giữ như lúc nướng
            if (assetPath.StartsWith(ArtImporter.BakedDir + "/Machine/"))
            {
                var mi = (TextureImporter)assetImporter;
                foreach (var platform in new[] { "Android", "iPhone" })
                {
                    var p = mi.GetPlatformTextureSettings(platform);
                    p.overridden = true;
                    p.maxTextureSize = 2048;
                    p.format = TextureImporterFormat.ASTC_6x6;
                    mi.SetPlatformTextureSettings(p);
                }
                return;
            }
            // ảnh nướng sẵn khác (sprite giấy/mực mã hoá kênh cho shader) tự đặt cách nhập lúc nướng: không ép cỡ, không nén
            if (assetPath.StartsWith(ArtImporter.BakedDir + "/")) return;
            // hình tướng aola: AolaImportPostprocessor đặt cách nhập (atlas có mipmap, chân dung có gốc ở chân)
            if (assetPath.StartsWith(AolaImport.ArtDir + "/")) return;
            var ti = (TextureImporter)assetImporter;
            ti.textureType = TextureImporterType.Sprite;
            ti.spriteImportMode = SpriteImportMode.Single;
            ti.mipmapEnabled = false;
            ti.alphaIsTransparency = true;
            ti.wrapMode = TextureWrapMode.Clamp;
            ti.filterMode = FilterMode.Bilinear;
            ti.npotScale = TextureImporterNPOTScale.None;
            // thân máy bi (ArtGen/Pachinko/build.py --duyet) cao 1394 px: nhập ở 2048 để giữ nét
            bool big = assetPath.Contains("/Fallback/") && !assetPath.Contains("/Icons/") || assetPath.Contains("/Islands/") || assetPath.Contains("/BattleBG/")
                || assetPath.Contains("/Pachinko/pk_than_may");
            ti.maxTextureSize = big ? 2048 : 1024;
            if (assetPath.EndsWith("/Islands/world.png")) ti.maxTextureSize = 4096; // đảo lớn sảnh có lề cho kéo: 1480 x 2320
            // bản đồ đảo hệ: bản đồ dài đảo 70 ải cao 4288 (ArtGen/Islands/build_zone70.py), nhập ở 4096 (gần đủ nét, máy nào cũng
            // đọc được); ảnh đảo 8 ải dưới 2048 không đổi
            if (assetPath.Contains("/Islands/zone_")) ti.maxTextureSize = 4096;
            // mặt tướng màn VS (ArtGen/BattleIntro, 384 x 384, mỗi dạng tướng một ảnh, hơn trăm ảnh): ASTC 8x8 cho nhẹ APK
            bool face = assetPath.Contains("/BattleIntro/Resources/HeroFaces/");
            if (face) ti.maxTextureSize = 512;
            var astc = face ? TextureImporterFormat.ASTC_8x8 : TextureImporterFormat.ASTC_6x6;
            var android = ti.GetPlatformTextureSettings("Android");
            android.overridden = true;
            android.maxTextureSize = ti.maxTextureSize;
            android.format = astc;
            ti.SetPlatformTextureSettings(android);
            var ios = ti.GetPlatformTextureSettings("iPhone");
            ios.overridden = true;
            ios.maxTextureSize = ti.maxTextureSize;
            ios.format = astc;
            ti.SetPlatformTextureSettings(ios);
        }
    }

    public static class ArtImporter
    {
        public const string ArtDir = "Assets/03 Art";
        public const string BakedDir = ArtDir + "/Baked";
        public const string LibraryPath = "Assets/02 Data/ArtLibrary.asset";
        static string ArtGenDir => Path.GetFullPath(Path.Combine(Application.dataPath, "../ArtGen"));

        static readonly string[] SlicePrefixes = { "btn_", "panel_", "frame_", "bar_", "chip_", "card_", "ribbon_" };

        // Sheet nhiều món: tên file trong inbox -> (số cột, số hàng, tên từng ô theo thứ tự trái sang phải, trên xuống dưới).
        // Tên icon trùng mã icon trong code (CardDef.icon...), lưu thành icon_<tên>. Ô tên rỗng thì bỏ.
        public sealed class Sheet
        {
            public int cols, rows;
            public string prefix;
            public string[] names;
        }

        public static readonly Dictionary<string, Sheet> Sheets = new Dictionary<string, Sheet>
        {
            // ArtGen/UIKit
            ["UI_Buttons"] = new Sheet { cols = 3, rows = 2, names = new[] { "btn_red", "btn_green", "btn_blue", "btn_yellow", "btn_purple", "btn_paper" } },
            ["UI_Panels"] = new Sheet { cols = 3, rows = 2, names = new[] { "panel_sheet", "panel_plaque", "panel_lined", "panel_info", "panel_bubble", "panel_slot" } },
            ["UI_CardFrames"] = new Sheet { cols = 3, rows = 2, names = new[] { "card_common", "card_uncommon", "card_rare", "card_epic", "card_legend", "card_back" } },
            ["UI_Bars"] = new Sheet
            {
                cols = 4, rows = 3,
                names = new[] { "bar_frame", "bar_hp", "bar_mana", "bar_rage", "bar_exp", "bar_shield", "chip_res", "chip_elem", "dot_red", "badge_level", "ring_select", "slot_dashed" },
            },
            ["UI_Discs"] = new Sheet { cols = 3, rows = 2, names = new[] { "disc_green", "disc_blue", "disc_yellow", "disc_coral", "disc_purple", "disc_small" } },
            ["UI_Stamps"] = new Sheet { cols = 3, rows = 2, names = new[] { "stamp_frame", "ribbon_red", "ribbon_paper", "vs_shield", "tapes", "cloud_wipe" } },
            // ArtGen/Icons
            ["IC_Resources"] = new Sheet
            {
                cols = 4, rows = 4, prefix = "icon_",
                names = new[]
                {
                    "ball", "exp", "shard", "stone", "chest_wood", "chest_wood_open", "chest_silver", "chest_silver_open",
                    "chest_gold", "chest_gold_open", "clock", "map", "team", "cards", "gear", "pencil",
                },
            },
            ["IC_ElementsStats"] = new Sheet
            {
                cols = 4, rows = 4, prefix = "icon_",
                names = new[] { "e_kim", "e_moc", "e_thuy", "e_hoa", "e_tho", "heart", "sword", "def", "speed", "mana", "stat_rage", "star", "starOff", "lock", "check", "boss" },
            },
            ["IC_PoolCardsA"] = new Sheet
            {
                cols = 4, rows = 4, prefix = "icon_",
                names = new[] { "claw", "shield", "bandage", "drop", "flame", "rock", "potion", "bun", "skull", "bubble", "lotus", "fist2", "rage", "fang", "crack", "torch" },
            },
            ["IC_PoolCardsB"] = new Sheet
            {
                cols = 4, rows = 4, prefix = "icon_",
                names = new[] { "mirror", "eye", "bolt", "yinyang", "ghost", "phoenix", "crown", "fist", "wheel", "sun", "incense", "seed", "leaf", "wind", "feather", "bell" },
            },
            ["IC_InnateFarmStatus"] = new Sheet
            {
                cols = 4, rows = 4, prefix = "icon_",
                names = new[]
                {
                    "hammer", "helmet", "wing", "moon", "wave", "trident", "revive", "farm_field", "farm_pond", "farm_orchard",
                    "farm_oven", "farm_workshop", "st_burn", "st_stun", "st_regen", "st_evade",
                },
            },
            // ArtGen/Islands: phần động của sảnh và đảo hệ
            ["ANIM_Sheet"] = new Sheet
            {
                cols = 4, rows = 4, prefix = "anim_",
                names = new[]
                {
                    "smoke_big", "smoke_small", "flame_a", "flame_b", "embers", "gear_big", "gear_small", "bell",
                    "whirlpool", "trident", "wave", "ripple", "foam", "sparkle", "leaf", "wind",
                },
            },
        };

        // ảnh đơn đổi tên khi nhập (còn lại giữ tên file)
        static readonly Dictionary<string, string> Rename = new Dictionary<string, string>
        {
            ["UI_Logo"] = "logo",
            ["UI_Paper"] = "paper_tile",
        };

        [MenuItem("PokiClash/Nhập ảnh ArtGen", priority = 11)]
        public static void ImportInbox()
        {
            int n = 0;
            if (Directory.Exists(ArtGenDir))
                foreach (var pack in Directory.GetDirectories(ArtGenDir))
                {
                    var inbox = Path.Combine(pack, "inbox");
                    if (!Directory.Exists(inbox)) continue;
                    var dst = Path.Combine(Application.dataPath, "03 Art", Path.GetFileName(pack));
                    foreach (var f in Directory.GetFiles(inbox).Where(IsImage))
                    {
                        Directory.CreateDirectory(dst);
                        var name = Path.GetFileNameWithoutExtension(f);
                        if (Sheets.TryGetValue(name, out var sheet)) n += CutSheet(f, sheet, dst);
                        else
                        {
                            CopyTrimmed(f, Path.Combine(dst, (Rename.TryGetValue(name, out var rn) ? rn : name) + ".png"));
                            n++;
                        }
                    }
                }
            AssetDatabase.Refresh();
            ApplySlices();
            BuildLibrary();
            Debug.Log($"[Ảnh] Đã nhập {n} ảnh từ ArtGen/*/inbox.");
        }

        // Cắt sheet theo lưới đều, gọt phần trong suốt quanh mỗi món (chừa 4 px).
        public static int CutSheet(string file, Sheet sheet, string dst)
        {
            var tex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
            tex.LoadImage(File.ReadAllBytes(file));
            if (!HasAlpha(tex)) KnockOutWhite(tex);
            int cw = tex.width / sheet.cols, ch = tex.height / sheet.rows, made = 0;
            for (int i = 0; i < sheet.names.Length && i < sheet.cols * sheet.rows; i++)
            {
                if (string.IsNullOrEmpty(sheet.names[i])) continue;
                int c = i % sheet.cols, r = i / sheet.cols;
                int x0 = c * cw, y0 = tex.height - (r + 1) * ch; // ô đánh số từ trên xuống, texture tính từ dưới lên
                var px = tex.GetPixels(x0, y0, cw, ch);
                int minX = cw, minY = ch, maxX = -1, maxY = -1;
                for (int y = 0; y < ch; y++)
                    for (int x = 0; x < cw; x++)
                        if (px[y * cw + x].a > 0.04f)
                        {
                            minX = Mathf.Min(minX, x);
                            maxX = Mathf.Max(maxX, x);
                            minY = Mathf.Min(minY, y);
                            maxY = Mathf.Max(maxY, y);
                        }
                if (maxX < 0) continue; // ô trống
                minX = Mathf.Max(0, minX - 4);
                minY = Mathf.Max(0, minY - 4);
                maxX = Mathf.Min(cw - 1, maxX + 4);
                maxY = Mathf.Min(ch - 1, maxY + 4);
                int w = maxX - minX + 1, h = maxY - minY + 1;
                var cut = new Texture2D(w, h, TextureFormat.RGBA32, false);
                cut.SetPixels(tex.GetPixels(x0 + minX, y0 + minY, w, h));
                cut.Apply();
                File.WriteAllBytes(Path.Combine(dst, (sheet.prefix ?? "") + sheet.names[i] + ".png"), cut.EncodeToPNG());
                Object.DestroyImmediate(cut);
                made++;
            }
            Object.DestroyImmediate(tex);
            return made;
        }

        // có điểm trong suốt ở 4 góc thì coi như ảnh đã có nền trong suốt
        static bool HasAlpha(Texture2D t)
        {
            int w = t.width - 1, h = t.height - 1;
            return t.GetPixel(0, 0).a < 0.98f || t.GetPixel(w, 0).a < 0.98f || t.GetPixel(0, h).a < 0.98f || t.GetPixel(w, h).a < 0.98f;
        }

        static bool IsImage(string f)
        {
            var e = Path.GetExtension(f).ToLowerInvariant();
            return e == ".png" || e == ".jpg" || e == ".jpeg";
        }

        // Ảnh gen thường có nền trắng: biến điểm gần trắng nối với mép thành trong suốt (tô loang từ 4 cạnh).
        static void CopyTrimmed(string from, string to)
        {
            var tex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
            tex.LoadImage(File.ReadAllBytes(from));
            bool islandOrBg = from.Replace('\\', '/').Contains("/Islands/") || from.Replace('\\', '/').Contains("/BattleBG/") ||
                              from.Replace('\\', '/').Contains("/Hub/");
            if (!islandOrBg && !HasAlpha(tex)) KnockOutWhite(tex);
            File.WriteAllBytes(to, tex.EncodeToPNG());
            Object.DestroyImmediate(tex);
        }

        static void KnockOutWhite(Texture2D tex)
        {
            int w = tex.width, h = tex.height;
            var px = tex.GetPixels32();
            bool White(Color32 c) => c.a > 0 && c.r > 238 && c.g > 238 && c.b > 238;
            var seen = new bool[w * h];
            var q = new Queue<int>();
            for (int x = 0; x < w; x++)
            {
                q.Enqueue(x);
                q.Enqueue((h - 1) * w + x);
            }
            for (int y = 0; y < h; y++)
            {
                q.Enqueue(y * w);
                q.Enqueue(y * w + w - 1);
            }
            int cleared = 0;
            while (q.Count > 0)
            {
                int i = q.Dequeue();
                if (seen[i]) continue;
                seen[i] = true;
                if (!White(px[i])) continue;
                px[i].a = 0;
                cleared++;
                int x = i % w, y = i / w;
                if (x > 0) q.Enqueue(i - 1);
                if (x < w - 1) q.Enqueue(i + 1);
                if (y > 0) q.Enqueue(i - w);
                if (y < h - 1) q.Enqueue(i + w);
            }
            if (cleared == 0) return;
            tex.SetPixels32(px);
            tex.Apply();
        }

        // ảnh khung: viền 9-slice = 28% cạnh ngắn (chỉnh tay trong Sprite Editor nếu cần)
        static void ApplySlices()
        {
            foreach (var guid in AssetDatabase.FindAssets("t:Texture2D", new[] { ArtDir }))
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                var name = Path.GetFileNameWithoutExtension(path);
                if (path.Contains("/Fallback/") || !SlicePrefixes.Any(name.StartsWith)) continue;
                var ti = (TextureImporter)AssetImporter.GetAtPath(path);
                if (ti.spriteBorder.sqrMagnitude > 0) continue;
                ti.GetSourceTextureWidthAndHeight(out int w, out int h);
                float b = Mathf.Round(Mathf.Min(w, h) * 0.28f);
                ti.spriteBorder = new Vector4(b, b, b, b);
                ti.SaveAndReimport();
            }
        }

        // Danh mục ảnh theo tên file: ảnh gen (mọi thư mục trừ Fallback), ảnh thay thế, icon thay thế. Ảnh thay thế đã có ảnh gen
        // cùng tên (icon: "icon_<tên>") thì đổi sang ảnh gen trong mọi prefab rồi bỏ khỏi danh mục, để bản build không mang cả hai.
        [MenuItem("PokiClash/Dựng lại danh mục ảnh", priority = 12)]
        public static ArtLibrary BuildLibrary()
        {
            var lib = AssetDatabase.LoadAssetAtPath<ArtLibrary>(LibraryPath);
            if (!lib)
            {
                lib = ScriptableObject.CreateInstance<ArtLibrary>();
                AssetDatabase.CreateAsset(lib, LibraryPath);
            }
            lib.art.Clear();
            lib.fallback.Clear();
            lib.icons.Clear();
            foreach (var guid in AssetDatabase.FindAssets("t:Sprite", new[] { ArtDir }))
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                var sprite = AssetDatabase.LoadAssetAtPath<Sprite>(path);
                // ảnh trong Resources (mặt tướng, nền màn VS: ArtGen/BattleIntro) nạp khi cần, không vào danh mục
                if (!sprite || path.StartsWith(BakedDir + "/") || path.StartsWith(AolaImport.ArtDir + "/") || path.Contains("/Resources/")) continue;
                var e = new ArtLibrary.Entry { name = Path.GetFileNameWithoutExtension(path), sprite = sprite };
                if (path.Contains("/Fallback/Icons/")) lib.icons.Add(e);
                else if (path.Contains("/Fallback/")) lib.fallback.Add(e);
                else if (!path.Contains("/Fonts/")) lib.art.Add(e);
            }
            SwapFallbackInPrefabs(lib);
            var gen = new HashSet<string>(lib.art.Select(e => e.name));
            int dropped = lib.fallback.RemoveAll(e => gen.Contains(e.name)) + lib.icons.RemoveAll(e => gen.Contains("icon_" + e.name));
            lib.Invalidate();
            EditorUtility.SetDirty(lib);
            AssetDatabase.SaveAssets();
            Debug.Log($"[Ảnh] Danh mục: {lib.art.Count} ảnh gen, {lib.fallback.Count} ảnh thay thế, {lib.icons.Count} icon thay thế " +
                      $"(bỏ {dropped} ảnh thay thế đã có ảnh gen).");
            return lib;
        }

        public const string PrefabDir = "Assets/04 Prefabs";

        // Prefab mang sẵn sprite lúc nướng (thường là ảnh thay thế). Có ảnh gen cùng tên (icon: "icon_<tên>") thì thay trong mọi
        // prefab; khung giữ tỉ lệ ảnh (AspectRatioFitter cạnh Image) đổi theo ảnh mới. Phần thuộc prefab lồng mà chưa bị ghi đè
        // thì để prefab gốc của nó đổi.
        public static void SwapFallbackInPrefabs(ArtLibrary lib)
        {
            if (!lib) return;
            var gen = lib.art.Where(e => e.sprite).GroupBy(e => e.name).ToDictionary(g => g.Key, g => g.First().sprite);
            var swap = new Dictionary<Sprite, Sprite>();
            foreach (var e in lib.fallback)
                if (e.sprite && gen.TryGetValue(e.name, out var s) && s != e.sprite) swap[e.sprite] = s;
            foreach (var e in lib.icons)
                if (e.sprite && gen.TryGetValue("icon_" + e.name, out var s) && s != e.sprite) swap[e.sprite] = s;
            if (swap.Count == 0) return;

            int files = 0, images = 0;
            foreach (var guid in AssetDatabase.FindAssets("t:Prefab", new[] { PrefabDir }))
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                var root = PrefabUtility.LoadPrefabContents(path);
                int changed = 0;
                foreach (var img in root.GetComponentsInChildren<UnityEngine.UI.Image>(true))
                {
                    if (!img.sprite || !swap.TryGetValue(img.sprite, out var to)) continue;
                    if (PrefabUtility.IsPartOfPrefabInstance(img))
                    {
                        var src = PrefabUtility.GetCorrespondingObjectFromSource(img);
                        if (src && src.sprite == img.sprite) continue;
                    }
                    img.sprite = to;
                    var fit = img.GetComponent<UnityEngine.UI.AspectRatioFitter>();
                    if (fit) fit.aspectRatio = to.rect.width / to.rect.height;
                    changed++;
                }
                if (changed > 0)
                {
                    PrefabUtility.SaveAsPrefabAsset(root, path);
                    files++;
                    images += changed;
                }
                PrefabUtility.UnloadPrefabContents(root);
            }
            Debug.Log($"[Ảnh] Đổi ảnh thay thế sang ảnh gen: {images} ô ảnh trong {files} prefab.");
        }
    }
}
