// Gán nội dung vào 5 gói tải sau (GD_Claude/27_TaiNoiDungSau.md, người dùng chốt 2026-11-23). Mỗi gói "noi_dung_<hệ>" là một nhóm
// Addressables (nhãn "pack_<hệ>", gói chung một bundle LZ4) có schema Play Asset Delivery kiểu fast-follow: build AAB có bật Split
// Application Binary thì thành asset pack của Play; build APK thường thì bundle vào thẳng StreamingAssets (bản đủ cho tester).
// Lượt đầu (mốc T2, T3) gồm:
//  - Tướng và lính cùng hệ, trừ dòng tướng khởi đầu (heroes.json "starters"): phần hình của dạng (AolaAnim, .atomik, atlas aola,
//    anim.bytes, ảnh riêng <dạng>_tt_*) dời từ Heroes/Resources/<dạng>/ sang Heroes/Forms/<dạng>/ (Addressables không lấy được nội dung
//    trong Resources); chân dung <dạng>_portrait.png ở lại Resources (bản cài). Prefab tướng bỏ trỏ thẳng (AolaActor.SetupPack).
//  - Ảnh đảo, nền trận trong ArtLibrary: tên land_/zone_/be_/battle_<hệ>…, trừ nền ải đầu (battle_<hệ>_c01, _s1), ảnh sảnh (sanh_*) và ảnh
//    nằm trong sprite atlas (atlas còn trong bản cài; chuyển cả atlas theo hệ để sau). ArtImporter.BuildLibrary gọi ArtPack + Mark.
// Các menu nhập tướng (AolaImport, AtomikForms) gọi RestoreHeroes trước (dạng về Resources như cũ) và ApplyHeroes sau.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Text.RegularExpressions;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEditor.AddressableAssets;
using UnityEditor.AddressableAssets.Android;
using UnityEditor.AddressableAssets.Settings;
using UnityEditor.AddressableAssets.Settings.GroupSchemas;
using UnityEngine;
using UnityEngine.AddressableAssets.Android;

namespace PokiClash.EditorTools
{
    public static class ContentPackSetup
    {
        public const string FormsDir = AolaImport.ArtDir + "/Forms";
        const string HeroesJson = "Assets/02 Data/Json/heroes.json";
        const string PrefabDir = "Assets/04 Prefabs/Heroes";
        const string PadRoot = "Assets/PlayAssetDelivery";
        static readonly string[] Elems = ContentPacks.Elems;

        // ---------- dữ liệu tướng ----------

        public sealed class HeroInfo
        {
            public string id, elem;
            public bool starter;
            public List<string> forms = new List<string>();
            public string Pack => starter ? null : elem;
        }

        public static List<HeroInfo> Heroes()
        {
            var data = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(HeroesJson));
            var starters = new HashSet<string>();
            if (data.TryGetValue("starters", out var st) && st is List<object> sl)
                foreach (var x in sl) starters.Add(x as string);
            var all = new List<object>((List<object>)data["heroes"]);
            if (data.TryGetValue("minions", out var mn) && mn is List<object> ml) all.AddRange(ml);
            var res = new List<HeroInfo>();
            foreach (Dictionary<string, object> h in all)
            {
                var hi = new HeroInfo { id = h["id"] as string, elem = h.TryGetValue("elem", out var e) ? e as string : null };
                hi.starter = starters.Contains(hi.id);
                if (h.TryGetValue("forms", out var fs) && fs is List<object> fl)
                    foreach (Dictionary<string, object> f in fl)
                        if (f.TryGetValue("aola", out var a) && a is string s && s.Length > 0) hi.forms.Add(s);
                if (hi.forms.Count == 0 && h.TryGetValue("aola", out var a0) && a0 is string s0 && s0.Length > 0) hi.forms.Add(s0);
                if (!string.IsNullOrEmpty(hi.id)) res.Add(hi);
            }
            return res;
        }

        // ---------- luật ảnh ----------

        static readonly Regex ArtName = new Regex(@"^(land|zone|be|battle)_(thuy|hoa|kim|moc|tho)(_|$)");
        static HashSet<string> atlasPacked;

        // hệ của gói chứa ảnh ở path (ArtLibrary), null = bản cài
        public static string ArtPack(string path)
        {
            if (string.IsNullOrEmpty(path) || !Enabled) return null;
            string dir = Path.GetDirectoryName(path)?.Replace('\\', '/');
            if (dir != ArtImporter.ArtDir + "/Islands" && dir != ArtImporter.ArtDir + "/BattleBG") return null;
            string name = Path.GetFileNameWithoutExtension(path);
            var m = ArtName.Match(name);
            if (!m.Success) return null;
            string elem = m.Groups[2].Value;
            if (name == $"battle_{elem}_c01" || name == $"battle_{elem}_s1") return null; // nền ải đầu (trận đầu không cần mạng)
            if (AtlasPacked().Contains(path)) return null;
            return elem;
        }

        // ảnh nằm trong một sprite atlas (đọc danh sách packables của mọi .spriteatlasv2, thư mục thì lấy mọi ảnh bên trong)
        static HashSet<string> AtlasPacked()
        {
            if (atlasPacked != null) return atlasPacked;
            atlasPacked = new HashSet<string>();
            foreach (var guid in AssetDatabase.FindAssets("t:SpriteAtlasAsset").Concat(AssetDatabase.FindAssets("glob:\"*.spriteatlasv2\"")).Distinct())
            {
                string ap = AssetDatabase.GUIDToAssetPath(guid);
                if (!ap.EndsWith(".spriteatlasv2") || !File.Exists(ap)) continue;
                foreach (Match g in Regex.Matches(File.ReadAllText(ap), @"guid: ([0-9a-f]{32})"))
                {
                    string p = AssetDatabase.GUIDToAssetPath(g.Groups[1].Value);
                    if (string.IsNullOrEmpty(p)) continue;
                    if (AssetDatabase.IsValidFolder(p))
                        foreach (var t in AssetDatabase.FindAssets("t:Texture2D", new[] { p })) atlasPacked.Add(AssetDatabase.GUIDToAssetPath(t));
                    else atlasPacked.Add(p);
                }
            }
            return atlasPacked;
        }

        // Tắt cả cơ chế (bản cài mang hết như trước): menu "Gỡ gói". Ghi trong EditorPrefs của máy, mặc định bật.
        public static bool Enabled
        {
            get => !EditorPrefs.GetBool("PokiClash.ContentPacks.Off", false);
            set => EditorPrefs.SetBool("PokiClash.ContentPacks.Off", !value);
        }

        // ---------- Addressables ----------

        static AddressableAssetSettings Settings()
        {
            var s = AddressableAssetSettingsDefaultObject.GetSettings(true);
            // build nội dung cùng lúc build game (nút Build và PokiBuild)
            s.BuildAddressablesWithPlayerBuild = AddressableAssetSettings.PlayerBuildOption.BuildWithPlayer;
            EnsurePad(s);
            return s;
        }

        // như menu "Init Play Asset Delivery" của Addressables for Android, không hỏi
        static void EnsurePad(AddressableAssetSettings s)
        {
            if (s.InitializationObjects.FindIndex(i => i is PlayAssetDeliveryInitializationSettings) < 0)
                s.AddInitializationObject(PadAsset<PlayAssetDeliveryInitializationSettings>("InitObjects"));
            if (s.DataBuilders.FindIndex(b => b is BuildScriptPlayAssetDelivery) < 0)
                s.AddDataBuilder(PadAsset<BuildScriptPlayAssetDelivery>("DataBuilders"));
        }

        static T PadAsset<T>(string sub) where T : ScriptableObject
        {
            string dir = $"{PadRoot}/{sub}";
            if (!AssetDatabase.IsValidFolder(PadRoot)) AssetDatabase.CreateFolder("Assets", "PlayAssetDelivery");
            if (!AssetDatabase.IsValidFolder(dir)) AssetDatabase.CreateFolder(PadRoot, sub);
            string path = $"{dir}/{typeof(T).Name}.asset";
            var a = AssetDatabase.LoadAssetAtPath<T>(path);
            if (a) return a;
            a = ScriptableObject.CreateInstance<T>();
            AssetDatabase.CreateAsset(a, path);
            return a;
        }

        static AddressableAssetGroup Group(AddressableAssetSettings s, string elem)
        {
            string name = ContentPacks.PackName(elem);
            var g = s.FindGroup(name);
            if (!g)
                g = s.CreateGroup(name, false, false, false, null, typeof(BundledAssetGroupSchema), typeof(ContentUpdateGroupSchema),
                    typeof(PlayAssetDeliverySchema));
            var b = g.GetSchema<BundledAssetGroupSchema>();
            b.BundleMode = BundledAssetGroupSchema.BundlePackingMode.PackTogether;
            b.Compression = BundledAssetGroupSchema.BundleCompressionMode.LZ4;
            b.IncludeInBuild = true;
            b.BuildPath.SetVariableByName(s, AddressableAssetSettings.kLocalBuildPath);
            b.LoadPath.SetVariableByName(s, AddressableAssetSettings.kLocalLoadPath);
            var pad = g.GetSchema<PlayAssetDeliverySchema>() ?? g.AddSchema<PlayAssetDeliverySchema>();
            pad.AssetPackDeliveryType = DeliveryType.FastFollow;
            s.AddLabel(ContentPacks.Label(elem), false);
            return g;
        }

        // đưa asset vào gói elem với địa chỉ address (đã ở nhóm khác thì dời)
        public static void Mark(string path, string elem, string address)
        {
            string guid = AssetDatabase.AssetPathToGUID(path);
            if (string.IsNullOrEmpty(guid)) return;
            var s = Settings();
            var g = Group(s, elem);
            var e = s.FindAssetEntry(guid);
            if (e == null || e.parentGroup != g) e = s.CreateOrMoveEntry(guid, g, false, false);
            if (e.address != address) e.SetAddress(address, false);
            foreach (var other in Elems)
                if (other != elem && e.labels.Contains(ContentPacks.Label(other))) e.SetLabel(ContentPacks.Label(other), false, false, false);
            e.SetLabel(ContentPacks.Label(elem), true, true, false);
        }

        // bỏ asset khỏi mọi gói (về bản cài)
        public static void Unmark(string path)
        {
            var s = AddressableAssetSettingsDefaultObject.Settings;
            if (!s) return;
            string guid = AssetDatabase.AssetPathToGUID(path);
            if (!string.IsNullOrEmpty(guid) && s.FindAssetEntry(guid) != null) s.RemoveAssetEntry(guid, false);
        }

        static void Save()
        {
            var s = AddressableAssetSettingsDefaultObject.Settings;
            if (s) s.SetDirty(AddressableAssetSettings.ModificationEvent.BatchModification, null, true, true);
            AssetDatabase.SaveAssets();
        }

        // ---------- tướng ----------

        static string ResDir(string form) => $"{AolaImport.ResDir}/{form}";
        static string PackDir(string form) => $"{FormsDir}/{form}";

        // thư mục đang chứa AolaAnim của dạng (Forms nếu đã dời, không thì Resources)
        public static string FormDir(string form) =>
            File.Exists($"{PackDir(form)}/{form}.asset") ? PackDir(form) : ResDir(form);

        static bool Portrait(string file, string form) => Path.GetFileName(file) == form + "_portrait.png";

        static void EnsureFolder(string path)
        {
            if (AssetDatabase.IsValidFolder(path)) return;
            string parent = Path.GetDirectoryName(path).Replace('\\', '/');
            EnsureFolder(parent);
            AssetDatabase.CreateFolder(parent, Path.GetFileName(path));
        }

        static int MoveFiles(string from, string to, Func<string, bool> pick)
        {
            if (!AssetDatabase.IsValidFolder(from)) return 0;
            int n = 0;
            foreach (var f in Directory.GetFiles(from))
            {
                if (f.EndsWith(".meta")) continue;
                string file = f.Replace('\\', '/');
                if (!pick(file)) continue;
                EnsureFolder(to);
                string dst = $"{to}/{Path.GetFileName(file)}";
                string err = AssetDatabase.MoveAsset(file, dst);
                if (string.IsNullOrEmpty(err)) n++;
                else Debug.LogError($"[Gói] Không dời được {file} → {dst}: {err}");
            }
            if (Directory.Exists(from) && !Directory.EnumerateFileSystemEntries(from).Any()) AssetDatabase.DeleteAsset(from);
            return n;
        }

        // Tướng ngoài dòng khởi đầu: dời hình sang Forms, gán gói, bỏ trỏ thẳng trong prefab. Dòng khởi đầu: trả về Resources, trỏ thẳng.
        [MenuItem("PokiClash/Tải sau/Gán gói tướng", priority = 141)]
        public static string ApplyHeroes()
        {
            if (!Enabled) return RestoreHeroes();
            var s = Settings();
            int moved = 0, marked = 0, packed = 0, base_ = 0;
            foreach (var h in Heroes())
            {
                string pack = h.Pack;
                foreach (var form in h.forms)
                {
                    if (pack == null) moved += MoveFiles(PackDir(form), ResDir(form), f => true);
                    else moved += MoveFiles(ResDir(form), PackDir(form), f => !Portrait(f, form));
                }
            }
            foreach (var h in Heroes())
            {
                string pack = h.Pack;
                foreach (var form in h.forms)
                {
                    string dir = FormDir(form);
                    if (!AssetDatabase.IsValidFolder(dir)) continue;
                    foreach (var f in Directory.GetFiles(dir))
                    {
                        if (f.EndsWith(".meta")) continue;
                        string file = f.Replace('\\', '/');
                        string fn = Path.GetFileNameWithoutExtension(file);
                        bool want = file.EndsWith($"/{form}.asset") || file.EndsWith($"/{form}_atlas.png") || fn.StartsWith(form + "_tt_");
                        if (pack == null || !want) Unmark(file);
                        else
                        {
                            Mark(file, pack, file.EndsWith(".asset") ? form : fn);
                            marked++;
                        }
                    }
                }
                // prefab
                string pp = $"{PrefabDir}/{h.id}.prefab";
                if (!File.Exists(pp)) continue;
                var root = PrefabUtility.LoadPrefabContents(pp);
                var actor = root.GetComponent<AolaActor>();
                if (actor)
                {
                    if (pack == null)
                    {
                        var anims = h.forms.Select(f => AssetDatabase.LoadAssetAtPath<AolaAnim>($"{ResDir(f)}/{f}.asset")).ToArray();
                        if (!string.IsNullOrEmpty(actor.Pack) || actor.Forms.Length != anims.Length || anims.Where((a, i) => actor.Forms[i] != a).Any())
                        {
                            actor.Setup(anims);
                            PrefabUtility.SaveAsPrefabAsset(root, pp);
                        }
                        base_++;
                    }
                    else
                    {
                        var keys = h.forms.ToArray();
                        actor.SetupPack(keys, pack);
                        PrefabUtility.SaveAsPrefabAsset(root, pp);
                        packed++;
                    }
                }
                PrefabUtility.UnloadPrefabContents(root);
            }
            var lib = AssetDatabase.LoadAssetAtPath<HeroModels>(AolaImport.LibraryPath);
            if (lib)
            {
                lib.Setup(lib.heroes); // bỏ bảng tra cũ
                EditorUtility.SetDirty(lib);
            }
            Save();
            string msg = $"[Gói] Tướng: {packed} tướng vào gói, {base_} tướng ở bản cài (dòng khởi đầu); dời {moved} file, {marked} asset trong gói.";
            Debug.Log(msg);
            return msg;
        }

        // Trả mọi dạng về Resources và trỏ thẳng như trước (các menu nhập tướng gọi trước khi chạy). Không xoá nhóm Addressables.
        public static string RestoreHeroes()
        {
            int moved = 0, fixedPrefabs = 0;
            if (AssetDatabase.IsValidFolder(FormsDir))
                foreach (var d in Directory.GetDirectories(FormsDir))
                {
                    string form = Path.GetFileName(d);
                    foreach (var f in Directory.GetFiles(d))
                        if (!f.EndsWith(".meta")) Unmark(f.Replace('\\', '/'));
                    moved += MoveFiles($"{FormsDir}/{form}", ResDir(form), f => true);
                }
            foreach (var h in Heroes())
            {
                string pp = $"{PrefabDir}/{h.id}.prefab";
                if (!File.Exists(pp)) continue;
                var root = PrefabUtility.LoadPrefabContents(pp);
                var actor = root.GetComponent<AolaActor>();
                if (actor && !string.IsNullOrEmpty(actor.Pack))
                {
                    actor.Setup(h.forms.Select(f => AssetDatabase.LoadAssetAtPath<AolaAnim>($"{ResDir(f)}/{f}.asset")).ToArray());
                    PrefabUtility.SaveAsPrefabAsset(root, pp);
                    fixedPrefabs++;
                }
                PrefabUtility.UnloadPrefabContents(root);
            }
            var lib = AssetDatabase.LoadAssetAtPath<HeroModels>(AolaImport.LibraryPath);
            if (lib)
            {
                lib.Setup(lib.heroes);
                EditorUtility.SetDirty(lib);
            }
            Save();
            string msg = $"[Gói] Trả tướng về bản cài: dời {moved} file, {fixedPrefabs} prefab trỏ thẳng lại.";
            Debug.Log(msg);
            return msg;
        }

        // chạy một menu nhập tướng với dạng ở chỗ cũ (Resources), xong gán gói lại
        public static void Around(Action run)
        {
            RestoreHeroes();
            try { run(); }
            finally { ApplyHeroes(); }
        }

        // Prefab còn nướng sẵn ảnh của gói (ảnh xem trước trong Editor; lúc chạy code gán lại, vd. ảnh bản đồ đảo "anh_zone_<hệ>" của
        // Zone.prefab): bỏ trỏ để bản cài không kéo ảnh theo (ContentPackTests.BaseDoesNotDependOnPacks).
        [MenuItem("PokiClash/Tải sau/Bỏ ảnh của gói nướng sẵn trong prefab", priority = 142)]
        public static int ClearBakedPackSprites()
        {
            var s = AddressableAssetSettingsDefaultObject.Settings;
            if (!s) return 0;
            var packPaths = new HashSet<string>(s.groups.Where(g => g && g.Name.StartsWith("noi_dung_")).SelectMany(g => g.entries).Select(e => e.AssetPath));
            int n = 0;
            foreach (var guid in AssetDatabase.FindAssets("t:Prefab", new[] { ArtImporter.PrefabDir }))
            {
                string pp = AssetDatabase.GUIDToAssetPath(guid);
                if (!AssetDatabase.GetDependencies(pp, false).Any(packPaths.Contains)) continue;
                var root = PrefabUtility.LoadPrefabContents(pp);
                int c = 0;
                foreach (var img in root.GetComponentsInChildren<UnityEngine.UI.Image>(true))
                {
                    if (!img.sprite || !packPaths.Contains(AssetDatabase.GetAssetPath(img.sprite))) continue;
                    Debug.Log($"[Gói] Bỏ ảnh {img.sprite.name} nướng sẵn ở {pp} ({img.name})");
                    img.sprite = null;
                    c++;
                }
                if (c > 0) PrefabUtility.SaveAsPrefabAsset(root, pp);
                PrefabUtility.UnloadPrefabContents(root);
                n += c;
            }
            return n;
        }

        // ---------- ảnh hạt (mốc T4) ----------

        public const string HatPackDir = "Assets/03 Art/Fx/HatGoi";
        static string HatAtlas(string elem) => $"{HatPackDir}/hat_{elem}.spriteatlasv2";

        // Chia ảnh hạt theo lần quét HatScanTour (Fx/hat_dung.json): ảnh chỉ tướng cùng một hệ (không phải tướng khởi đầu) dùng thì dời sang
        // Fx/HatGoi/<hệ>/, gói bằng atlas hat_<hệ> (không vào bản build) trong nhóm noi_dung_<hệ>; còn lại (dùng chung, tướng khởi đầu dùng,
        // chưa thấy ai dùng, ảnh hạt mới xuất) ở Fx/Hat, atlas hat của bản cài như cũ. Bỏ ảnh đã dời khỏi các mảng hatSprites trong prefab
        // (StageView, HeroViewer): lúc chạy HatLua.S lấy chúng từ gói đã nạp.
        [MenuItem("PokiClash/Tải sau/Gán gói ảnh hạt (theo lần quét)", priority = 143)]
        public static string ApplyHat()
        {
            if (!File.Exists(HatScanTour.OutPath)) return "[Gói] Chưa quét ảnh hạt (PokiClash/Tải sau/Quét ảnh hạt từng tướng)";
            var heroes = Heroes().ToDictionary(h => h.id);
            var root = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(HatScanTour.OutPath));
            var users = new Dictionary<string, HashSet<string>>(); // tên ảnh → các gói của tướng dùng ("*" = bản cài)
            foreach (var kv in (Dictionary<string, object>)root["heroes"])
            {
                string pack = heroes.TryGetValue(kv.Key, out var h) && Enabled ? h.Pack : null;
                foreach (var o in (List<object>)kv.Value)
                {
                    string n = o as string;
                    if (n == null) continue;
                    if (!users.TryGetValue(n, out var set)) users[n] = set = new HashSet<string>();
                    set.Add(pack ?? "*");
                }
            }
            string Target(string name) =>
                users.TryGetValue(name, out var set) && set.Count == 1 && !set.Contains("*") ? set.First() : null;

            // dời ảnh
            var files = Directory.GetFiles(AtlasMenu.HatDir, "hat_*.png").Select(f => f.Replace('\\', '/')).ToList();
            if (Directory.Exists(HatPackDir))
                files.AddRange(Directory.GetFiles(HatPackDir, "hat_*.png", SearchOption.AllDirectories).Select(f => f.Replace('\\', '/')));
            int toPack = 0, toBase = 0;
            var count = new Dictionary<string, int>();
            var moves = new List<(string from, string to, string elem)>();
            foreach (var f in files)
            {
                string name = Path.GetFileNameWithoutExtension(f);
                string elem = Target(name);
                string dir = elem == null ? AtlasMenu.HatDir : $"{HatPackDir}/{elem}";
                string dst = $"{dir}/{Path.GetFileName(f)}";
                if (elem != null) count[elem] = (count.TryGetValue(elem, out var c) ? c : 0) + 1;
                if (f == dst) continue;
                EnsureFolder(dir); // tạo thư mục trước khối gom (tạo trong khối dễ lỗi)
                moves.Add((f, dst, elem));
            }
            // Gom mọi lần dời vào một đợt: ảnh hạt là nguồn của atlas hat (1247 hình), không gom thì MỖI lần dời Unity dựng lại cả atlas
            // (10-20 giây; lần chạy đầu 2026-11-23 mất cả giờ)
            AssetDatabase.StartAssetEditing();
            try
            {
                foreach (var (f, dst, elem) in moves)
                {
                    if (File.Exists(dst)) AssetDatabase.DeleteAsset(dst); // bản xuất mới trùng tên ở chỗ đích: giữ bản đang dời tới
                    Unmark(f);
                    string err = AssetDatabase.MoveAsset(f, dst);
                    if (!string.IsNullOrEmpty(err)) Debug.LogError($"[Gói] Không dời được {f} → {dst}: {err}");
                    else if (elem == null) toBase++;
                    else toPack++;
                }
            }
            finally
            {
                AssetDatabase.StopAssetEditing();
            }

            // atlas theo hệ trong gói (ảnh đơn lẻ không gán: nằm trong atlas thì Addressables kéo theo)
            foreach (var e in Elems)
            {
                string dir = $"{HatPackDir}/{e}";
                bool any = Directory.Exists(dir) && Directory.GetFiles(dir, "hat_*.png").Length > 0;
                if (!any)
                {
                    if (File.Exists(HatAtlas(e))) AssetDatabase.DeleteAsset(HatAtlas(e));
                    continue;
                }
                string ap = AtlasMenu.Pack(HatAtlas(e), new List<UnityEngine.Object> { AssetDatabase.LoadAssetAtPath<DefaultAsset>(dir) }, 8, true, false);
                if (ap != null) Mark(ap, e, "hat_" + e);
                foreach (var f in Directory.GetFiles(dir, "hat_*.png"))
                    Mark(f.Replace('\\', '/'), e, Path.GetFileNameWithoutExtension(f));
            }

            // mảng hatSprites trong prefab: chỉ giữ ảnh của bản cài (Fx/Hat)
            int cut = 0;
            foreach (var guid in AssetDatabase.FindAssets("t:Prefab", new[] { ArtImporter.PrefabDir }))
            {
                string pp = AssetDatabase.GUIDToAssetPath(guid);
                if (!File.ReadAllText(pp).Contains("hatSprites")) continue;
                var go = PrefabUtility.LoadPrefabContents(pp);
                int c = 0;
                foreach (var comp in go.GetComponentsInChildren<MonoBehaviour>(true))
                {
                    if (!comp) continue;
                    var so = new SerializedObject(comp);
                    var arr = so.FindProperty("hatSprites");
                    if (arr == null || !arr.isArray) continue;
                    for (int i = arr.arraySize - 1; i >= 0; i--)
                    {
                        var o = arr.GetArrayElementAtIndex(i).objectReferenceValue;
                        string p = o ? AssetDatabase.GetAssetPath(o) : null;
                        if (o && p.StartsWith(AtlasMenu.HatDir + "/")) continue;
                        arr.GetArrayElementAtIndex(i).objectReferenceValue = null;
                        arr.DeleteArrayElementAtIndex(i);
                        c++;
                    }
                    so.ApplyModifiedPropertiesWithoutUndo();
                }
                if (c > 0) PrefabUtility.SaveAsPrefabAsset(go, pp);
                PrefabUtility.UnloadPrefabContents(go);
                cut += c;
            }
            Save();
            string msg = $"[Gói] Ảnh hạt: dời {toPack} ảnh vào gói, {toBase} về bản cài; trong gói: " +
                         string.Join(", ", Elems.Select(e => $"{e} {(count.TryGetValue(e, out var n) ? n : 0)}")) + $"; bỏ {cut} ảnh khỏi mảng hatSprites của prefab.";
            Debug.Log(msg);
            return msg;
        }

        // trả mọi ảnh hạt về Fx/Hat (Gỡ gói). Mảng hatSprites dựng lại bằng menu Prefab/Sàn đấu: hạt lửa, Hộp chi tiết tướng: hạt lửa.
        static void RestoreHat()
        {
            if (!Directory.Exists(HatPackDir)) return;
            AssetDatabase.StartAssetEditing(); // gom: không dựng lại atlas hat sau mỗi lần dời (xem ApplyHat)
            try
            {
                foreach (var f in Directory.GetFiles(HatPackDir, "hat_*.png", SearchOption.AllDirectories))
                {
                    string src = f.Replace('\\', '/');
                    Unmark(src);
                    string dst = $"{AtlasMenu.HatDir}/{Path.GetFileName(src)}";
                    if (File.Exists(dst)) AssetDatabase.DeleteAsset(dst);
                    AssetDatabase.MoveAsset(src, dst);
                }
            }
            finally
            {
                AssetDatabase.StopAssetEditing();
            }
            foreach (var e in Elems)
                if (File.Exists(HatAtlas(e)))
                {
                    Unmark(HatAtlas(e));
                    AssetDatabase.DeleteAsset(HatAtlas(e));
                }
        }

        // ---------- menu ----------

        [MenuItem("PokiClash/Tải sau/Gán gói (tướng + ảnh đảo + ảnh hạt)", priority = 140)]
        public static void ApplyAll()
        {
            Enabled = true;
            atlasPacked = null;
            ApplyHeroes();
            ArtImporter.BuildLibrary(); // ảnh đảo, nền trận (ArtPack + Mark trong vòng dựng danh mục)
            ClearBakedPackSprites();
            Debug.Log(ApplyHat());
            Debug.Log("[Gói] Xong. Xem cỡ từng gói: PokiClash/Tải sau/Xem trước gói.");
        }

        [MenuItem("PokiClash/Tải sau/Gỡ gói (bản cài mang hết như trước)", priority = 160)]
        public static void RevertAll()
        {
            Enabled = false;
            RestoreHeroes();
            RestoreHat();
            ArtImporter.BuildLibrary();
            var s = AddressableAssetSettingsDefaultObject.Settings;
            if (s)
                foreach (var e in Elems)
                {
                    var g = s.FindGroup(ContentPacks.PackName(e));
                    if (!g) continue;
                    foreach (var entry in g.entries.ToList()) s.RemoveAssetEntry(entry.guid, false);
                }
            Save();
            Debug.Log("[Gói] Đã gỡ: mọi nội dung về bản cài (bật lại bằng PokiClash/Tải sau/Gán gói).");
        }

        // cỡ từng gói (ảnh: cỡ lưu thật ở nền đang chọn; asset khác: cỡ file), ghi Temp/PokiShots/tai_sau.txt
        [MenuItem("PokiClash/Tải sau/Xem trước gói", priority = 150)]
        public static string Preview()
        {
            var s = AddressableAssetSettingsDefaultObject.Settings;
            var sb = new StringBuilder($"Gói tải sau ({(Enabled ? "bật" : "TẮT")}), nền {EditorUserBuildSettings.activeBuildTarget}\n");
            var storage = typeof(Editor).Assembly.GetType("UnityEditor.TextureUtil")?.GetMethod("GetStorageMemorySizeLong", BindingFlags.Static | BindingFlags.Public);
            long total = 0;
            foreach (var e in Elems)
            {
                var g = s ? s.FindGroup(ContentPacks.PackName(e)) : null;
                if (!g)
                {
                    sb.AppendLine($"  {e}: chưa có nhóm");
                    continue;
                }
                long bytes = 0;
                int n = 0;
                var deps = new HashSet<string>();
                foreach (var entry in g.entries)
                    foreach (var d in AssetDatabase.GetDependencies(entry.AssetPath, true)) deps.Add(d);
                foreach (var d in deps)
                {
                    if (d.EndsWith(".cs") || d.EndsWith(".shader")) continue;
                    var tex = AssetDatabase.LoadAssetAtPath<Texture2D>(d);
                    if (tex && storage != null) bytes += (long)storage.Invoke(null, new object[] { tex });
                    else if (File.Exists(d)) bytes += new FileInfo(d).Length;
                    n++;
                }
                total += bytes;
                sb.AppendLine($"  {ContentPacks.PackName(e)}: {g.entries.Count} mục, {n} asset kể cả phụ thuộc, ~{bytes / 1048576.0:0.0} MB trước nén");
            }
            sb.AppendLine($"  tổng ~{total / 1048576.0:0.0} MB trước nén");
            Directory.CreateDirectory(PlayTour.ShotDir);
            File.WriteAllText(Path.Combine(PlayTour.ShotDir, "tai_sau.txt"), sb.ToString());
            Debug.Log("[Gói] " + sb.ToString().Replace("\n", " | "));
            return sb.ToString();
        }
    }
}
