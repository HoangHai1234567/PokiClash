// Dựng nền móng của project bằng menu (chạy lại được, kết quả như nhau):
//   PokiClash/Cài đặt/1. Nhập TMP Essentials   — shader và TMP Settings của TextMeshPro (một lần)
//   PokiClash/Cài đặt/2. Dựng tất cả           — phông TMP, material nét rung, UiAssets, dữ liệu, danh mục ảnh,
//                                                 scene còn thiếu (Boot + scene chức năng), Build Settings, khung Game view.
// Scene đã có thì giữ nguyên: nội dung là prefab (Assets/04 Prefabs), chỉnh trong Editor (change convert-to-prefabs).
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TextCore.LowLevel;

namespace PokiClash.EditorTools
{
    public static class ProjectSetup
    {
        public const string SceneDir = "Assets/00 Scenes";
        const string FontDir = "Assets/03 Art/Fonts";
        const string ShaderDir = "Assets/03 Art/Shaders";
        const string UiAssetsPath = "Assets/02 Data/UiAssets.asset";

        // mọi dấu tiếng Việt, để nạp sẵn vào atlas phông và để test
        public const string VietSample =
            "ĂÂĐÊÔƠƯăâđêôơư àảãáạ ằẳẵắặ ầẩẫấậ èẻẽéẹ ềểễếệ ìỉĩíị òỏõóọ ồổỗốộ ờởỡớợ ùủũúụ ừửữứự ỳỷỹýỵ " +
            "ÀẢÃÁẠ ẰẲẴẮẶ ẦẨẪẤẬ ÈẺẼÉẸ ỀỂỄẾỆ ÌỈĨÍỊ ÒỎÕÓỌ ỒỔỖỐỘ ỜỞỠỚỢ ÙỦŨÚỤ ỪỬỮỨỰ ỲỶỸÝỴ " +
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 .,:;!?()[]+-−×%/·•…–\"'";

        [MenuItem("PokiClash/Cài đặt/1. Nhập TMP Essentials", priority = 0)]
        public static void ImportTmpEssentials()
        {
            if (AssetDatabase.IsValidFolder("Assets/TextMesh Pro/Resources") && TMP_Settings.instance != null)
            {
                Debug.Log("[Cài đặt] TMP Essentials đã có.");
                return;
            }
            var pkg = UnityEditor.PackageManager.PackageInfo.FindForAssembly(typeof(TMP_Settings).Assembly);
            var path = pkg != null ? Path.Combine(pkg.resolvedPath, "Package Resources", "TMP Essential Resources.unitypackage") : null;
            if (path == null || !File.Exists(path))
            {
                Debug.LogError("[Cài đặt] Không tìm thấy TMP Essential Resources.unitypackage trong gói ugui.");
                return;
            }
            AssetDatabase.ImportPackage(path, false);
            Debug.Log("[Cài đặt] Đã nhập TMP Essentials. Chạy tiếp \"2. Dựng tất cả\".");
        }

        [MenuItem("PokiClash/Cài đặt/2. Dựng tất cả", priority = 1)]
        public static void BuildAll()
        {
            if (Shader.Find("TextMeshPro/Distance Field") == null)
            {
                Debug.LogError("[Cài đặt] Chưa có shader TextMeshPro: chạy \"1. Nhập TMP Essentials\" trước.");
                return;
            }
            AssetDatabase.Refresh();
            var ui = BuildUiAssets();
            if (!DataImporter.Run(true)) return;
            var art = ArtImporter.BuildLibrary();
            BuildScenes(ui, art);
            UpdateBuildSettings();
            GameViewSizes.EnsureAll();
            FastPlayMode();
            AssetDatabase.SaveAssets();
            Debug.Log("[Cài đặt] Xong: mở Assets/00 Scenes/Boot.unity rồi bấm Play.");
        }

        // Vào Play nhanh: không reload domain (vẫn reload scene). Static của mã runtime được trả về trong các hàm
        // [RuntimeInitializeOnLoadMethod(SubsystemRegistration)] ResetStatics (App, MachineScene, ZoneScene, NotebookDev, SafeArea).
        [MenuItem("PokiClash/Cài đặt/3. Play không reload domain", priority = 2)]
        public static void FastPlayMode()
        {
            EditorSettings.enterPlayModeOptionsEnabled = true;
            EditorSettings.enterPlayModeOptions = EnterPlayModeOptions.DisableDomainReload;
            AssetDatabase.SaveAssets();
            Debug.Log("[Cài đặt] Vào Play không reload domain (vẫn reload scene).");
        }

        // ---------- phông và material ----------

        static UiAssets BuildUiAssets()
        {
            var ui = AssetDatabase.LoadAssetAtPath<UiAssets>(UiAssetsPath);
            if (!ui)
            {
                ui = ScriptableObject.CreateInstance<UiAssets>();
                AssetDatabase.CreateAsset(ui, UiAssetsPath);
            }
            ui.title = MakeFont("Baloo2-ExtraBold", 90, 2048);
            ui.bold = MakeFont("Baloo2-Bold", 90, 1024);
            ui.body = MakeFont("Pangolin-Regular", 90, 2048);
            ui.kit = MakeMaterial("UIKit", 1);
            ui.plain = MakeMaterial("UIPlain", 0);
            ui.sticker = MakeSticker();
            EditorUtility.SetDirty(ui);

            // phông mặc định của TMP: Pangolin (LiberationSans không có dấu tiếng Việt)
            var settings = TMP_Settings.instance;
            if (settings != null && ui.body != null)
            {
                var so = new SerializedObject(settings);
                var p = so.FindProperty("m_defaultFontAsset");
                if (p != null)
                {
                    p.objectReferenceValue = ui.body;
                    so.ApplyModifiedPropertiesWithoutUndo();
                }
            }
            return ui;
        }

        static TMP_FontAsset MakeFont(string file, int sampling, int atlas)
        {
            var assetPath = $"{FontDir}/{file} SDF.asset";
            var fa = AssetDatabase.LoadAssetAtPath<TMP_FontAsset>(assetPath);
            if (!fa)
            {
                var font = AssetDatabase.LoadAssetAtPath<Font>($"{FontDir}/{file}.ttf");
                if (!font)
                {
                    Debug.LogError($"[Cài đặt] Thiếu phông {FontDir}/{file}.ttf");
                    return null;
                }
                fa = TMP_FontAsset.CreateFontAsset(font, sampling, sampling / 10, GlyphRenderMode.SDFAA, atlas, atlas, AtlasPopulationMode.Dynamic, true);
                fa.name = Path.GetFileNameWithoutExtension(assetPath);
                AssetDatabase.CreateAsset(fa, assetPath);
                fa.atlasTextures[0].name = fa.name + " Atlas";
                AssetDatabase.AddObjectToAsset(fa.atlasTextures[0], fa);
                fa.material.name = fa.name + " Material";
                AssetDatabase.AddObjectToAsset(fa.material, fa);
            }
            // nạp sẵn mọi dấu tiếng Việt vào atlas (TryAddCharacters báo nhầm "thiếu" với ký tự đã có, nên dùng HasCharacters)
            if (!fa.HasCharacters(VietSample, out uint[] missing, false, true) && missing != null && missing.Length > 0)
                Debug.LogWarning($"[Cài đặt] {fa.name} thiếu ký tự: {new string(missing.Select(c => (char)c).ToArray())}");
            EditorUtility.SetDirty(fa);
            return fa;
        }

        static Material MakeMaterial(string name, float encoded)
        {
            var path = $"{ShaderDir}/{name}.mat";
            var m = AssetDatabase.LoadAssetAtPath<Material>(path);
            var shader = Shader.Find("PokiClash/UIInkBoil");
            if (!m)
            {
                m = new Material(shader) { name = name };
                AssetDatabase.CreateAsset(m, path);
            }
            m.shader = shader;
            m.SetFloat("_Encoded", encoded);
            m.SetFloat("_BoilAmp", encoded > 0 ? 1.6f : 1.2f);
            EditorUtility.SetDirty(m);
            return m;
        }

        static Material MakeSticker()
        {
            const string path = ShaderDir + "/Sticker.mat";
            var m = AssetDatabase.LoadAssetAtPath<Material>(path);
            var shader = Shader.Find("PokiClash/StickerOutline");
            if (!m)
            {
                m = new Material(shader) { name = "Sticker" };
                AssetDatabase.CreateAsset(m, path);
            }
            m.shader = shader;
            EditorUtility.SetDirty(m);
            return m;
        }

        // ---------- scene ----------

        static readonly Dictionary<string, System.Type> Roots = new Dictionary<string, System.Type>
        {
            [SceneIds.Hub] = typeof(HubScene),
            [SceneIds.Zone] = typeof(ZoneScene),
            [SceneIds.Battle] = typeof(BattleScene),
            [SceneIds.Machine] = typeof(MachineScene),
            [SceneIds.Heroes] = typeof(HeroesScene),
            [SceneIds.Cards] = typeof(CardsScene),
            [SceneIds.Notebook] = typeof(NotebookScene),
            [SceneIds.Badges] = typeof(BadgesScene),
            [SceneIds.Cave] = typeof(CaveScene),
            [SceneIds.Farm] = typeof(FarmScene),
        };

        const string AppPrefab = "Assets/04 Prefabs/App/App.prefab";
        const string ScreenDir = "Assets/04 Prefabs/Screens";

        static string ScenePath(string name) => $"{SceneDir}/{name}.unity";

        static void BuildScenes(UiAssets ui, ArtLibrary art)
        {
            MakeScene(SceneIds.Boot, () =>
            {
                var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(AppPrefab);
                if (prefab)
                {
                    PrefabUtility.InstantiatePrefab(prefab);
                    return;
                }
                var go = new GameObject("App");
                var app = go.AddComponent<App>();
                app.heroDb = DataImporter.LoadOrCreate<HeroDb>("HeroDb");
                app.cardDb = DataImporter.LoadOrCreate<CardDb>("CardDb");
                app.zoneDb = DataImporter.LoadOrCreate<ZoneDb>("ZoneDb");
                app.balance = DataImporter.LoadOrCreate<BalanceConfigAsset>("BalanceConfig");
                app.uiAssets = ui;
                app.artLibrary = art;
            });
            foreach (var kv in Roots)
            {
                var type = kv.Value;
                MakeScene(kv.Key, () =>
                {
                    // scene chức năng: bản sao prefab màn hình (canvas, nội dung, tham chiếu sẵn)
                    var screen = AssetDatabase.LoadAssetAtPath<GameObject>($"{ScreenDir}/{kv.Key}.prefab");
                    if (screen) ((GameObject)PrefabUtility.InstantiatePrefab(screen)).name = kv.Key;
                    else new GameObject(kv.Key, type);
                });
            }
        }

        // Dựng scene còn thiếu ở chế độ cộng rồi đóng lại, để không đụng scene người dùng đang mở. Scene đã có thì để yên.
        static void MakeScene(string name, System.Action fill)
        {
            var path = ScenePath(name);
            if (File.Exists(path)) return;
            var open = SceneManager.GetSceneByPath(path);
            if (open.IsValid() && open.isLoaded)
            {
                if (SceneManager.sceneCount == 1)
                {
                    Debug.LogWarning($"[Cài đặt] Scene {name} đang mở một mình, bỏ qua (mở scene khác rồi chạy lại).");
                    return;
                }
                EditorSceneManager.CloseScene(open, true);
            }
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
            var prev = SceneManager.GetActiveScene();
            SceneManager.SetActiveScene(scene);
            fill();
            SceneManager.SetActiveScene(prev);
            EditorSceneManager.SaveScene(scene, path);
            EditorSceneManager.CloseScene(scene, true);
        }

        // Boot đứng đầu, rồi các scene chức năng (SceneIds.Features); gỡ BanThu khỏi build (giữ file và code); giữ các scene khác sau cùng.
        static void UpdateBuildSettings()
        {
            var list = new List<EditorBuildSettingsScene> { new EditorBuildSettingsScene(ScenePath(SceneIds.Boot), true) };
            list.AddRange(SceneIds.Features.Select(n => new EditorBuildSettingsScene(ScenePath(n), true)));
            foreach (var s in EditorBuildSettings.scenes)
            {
                if (list.Any(x => x.path == s.path)) continue;
                if (s.path.EndsWith("/BanThu.unity")) continue;
                list.Add(s);
            }
            EditorBuildSettings.scenes = list.ToArray();
            Debug.Log("[Cài đặt] Build Settings: " + string.Join(", ", list.Select(s => Path.GetFileNameWithoutExtension(s.path))));
        }
    }
}
