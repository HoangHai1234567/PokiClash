// Lần đầu biên dịch: tạo scene bản thử (Assets/00 Scenes/BanThu.unity) và đổi project sang màn dọc. Không đụng scene đang mở.
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace PokiWar.BanThu.EditorTools
{
    [InitializeOnLoad]
    static class BanThuSetup
    {
        const string ScenePath = "Assets/00 Scenes/BanThu.unity";

        static BanThuSetup()
        {
            EditorApplication.delayCall += Run;
        }

        static void Run()
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode) return;
            if (!File.Exists(ScenePath)) CreateScene();
            Portrait();
        }

        [MenuItem("PokiWar/Mở scene bản thử")]
        static void Open()
        {
            if (!File.Exists(ScenePath)) CreateScene();
            if (EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo()) EditorSceneManager.OpenScene(ScenePath);
        }

        [MenuItem("PokiWar/Tạo lại scene bản thử")]
        static void Recreate() => CreateScene();

        // máy tự chơi trong Play mode, để soi màn hình giữa trận
        [MenuItem("PokiWar/Tự chơi A (xếp khối)")] static void AutoA() => Auto(0);
        [MenuItem("PokiWar/Tự chơi A có sập")] static void AutoASap() => Auto(1);
        [MenuItem("PokiWar/Tự chơi C (xếp ngọc)")] static void AutoC() => Auto(2);

        [MenuItem("PokiWar/Đổi tướng (khi đang Play)")]
        static void NextHero()
        {
            var game = Object.FindFirstObjectByType<BanThuGame>();
            if (Application.isPlaying && game) game.NextHero();
        }

        static void Auto(int mode)
        {
            var game = Object.FindFirstObjectByType<BanThuGame>();
            if (!Application.isPlaying || !game) { Debug.LogWarning("[BanThu] Mở scene bản thử và bấm Play trước."); return; }
            game.StartAuto(mode);
        }

        // Game view cỡ 1080 × 1920 (API nội bộ của Unity, đọc bằng reflection)
        [MenuItem("PokiWar/Game view 1080x1920")]
        static void PortraitGameView()
        {
            try
            {
                var asm = typeof(Editor).Assembly;
                var sizesType = asm.GetType("UnityEditor.GameViewSizes");
                var instance = typeof(ScriptableSingleton<>).MakeGenericType(sizesType).GetProperty("instance").GetValue(null);
                var groupType = (GameViewSizeGroupType)sizesType.GetProperty("currentGroupType").GetValue(instance);
                var group = sizesType.GetMethod("GetGroup").Invoke(instance, new object[] { (int)groupType });
                var gt = group.GetType();
                int count = (int)gt.GetMethod("GetTotalCount").Invoke(group, null), index = -1;
                for (int i = 0; i < count; i++)
                {
                    var size = gt.GetMethod("GetGameViewSize").Invoke(group, new object[] { i });
                    var st = size.GetType();
                    if ((int)st.GetProperty("width").GetValue(size) == 1080 && (int)st.GetProperty("height").GetValue(size) == 1920 &&
                        st.GetProperty("sizeType").GetValue(size).ToString() == "FixedResolution") { index = i; break; }
                }
                if (index < 0)
                {
                    var sizeType = asm.GetType("UnityEditor.GameViewSize");
                    var kind = asm.GetType("UnityEditor.GameViewSizeType");
                    var ctor = sizeType.GetConstructor(new[] { kind, typeof(int), typeof(int), typeof(string) });
                    var size = ctor.Invoke(new[] { System.Enum.Parse(kind, "FixedResolution"), 1080, 1920, "Dọc 1080x1920" });
                    gt.GetMethod("AddCustomSize").Invoke(group, new[] { size });
                    index = count;
                }
                var gameViewType = asm.GetType("UnityEditor.GameView");
                var view = EditorWindow.GetWindow(gameViewType);
                gameViewType.GetMethod("SizeSelectionCallback", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.NonPublic |
                                       System.Reflection.BindingFlags.Instance).Invoke(view, new object[] { index, null });
                Debug.Log("[BanThu] Game view: 1080x1920.");
            }
            catch (System.Exception e)
            {
                Debug.LogWarning("[BanThu] Không đặt được cỡ Game view, chọn tay 1080x1920: " + e.Message);
            }
        }

        static void CreateScene()
        {
            var active = SceneManager.GetActiveScene();
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
            SceneManager.SetActiveScene(scene);

            var camGo = new GameObject("Main Camera") { tag = "MainCamera" };
            var cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            cam.orthographicSize = 8;
            cam.transform.position = new Vector3(0, 0, -10);
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.10f, 0.11f, 0.16f);
            new GameObject("BanThu").AddComponent<BanThuGame>();

            EditorSceneManager.SaveScene(scene, ScenePath);
            if (active.IsValid()) SceneManager.SetActiveScene(active);
            EditorSceneManager.CloseScene(scene, true);

            var list = EditorBuildSettings.scenes.Where(s => s.path != ScenePath).ToList();
            list.Insert(0, new EditorBuildSettingsScene(ScenePath, true));
            EditorBuildSettings.scenes = list.ToArray();
            Debug.Log("[BanThu] Đã tạo " + ScenePath + ". Mở nó (menu PokiWar → Mở scene bản thử), chọn Game view 1080x1920 rồi bấm Play.");
        }

        static void Portrait()
        {
            if (PlayerSettings.defaultInterfaceOrientation == UIOrientation.Portrait) return;
            PlayerSettings.defaultInterfaceOrientation = UIOrientation.Portrait;
            PlayerSettings.allowedAutorotateToPortrait = true;
            PlayerSettings.allowedAutorotateToPortraitUpsideDown = false;
            PlayerSettings.allowedAutorotateToLandscapeLeft = false;
            PlayerSettings.allowedAutorotateToLandscapeRight = false;
            PlayerSettings.defaultScreenWidth = 1080;
            PlayerSettings.defaultScreenHeight = 1920;
            Debug.Log("[BanThu] Đã đổi project sang màn dọc (Portrait).");
        }
    }
}
