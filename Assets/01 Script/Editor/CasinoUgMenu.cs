// Hộp Hầm đấu (UndergroundDialog, GD_Claude/29_DaoCasino.md mục 6.5, mốc C4). Menu "PokiClash/Prefab/Đảo Casino/Hầm đấu: dựng hộp":
// Dialogs/HamDau = bản sao tờ giấy gốc Dialogs/HopThoai (rộng 1000, đặt cỡ cố định), tiêu đề, dòng đội của mình, 6 dòng bậc dựng sẵn
// (tên, luật ngày, đội địch, thưởng, nút Đánh), nút Đổi đội (mở Dialogs/ChonDoi); đăng ký vào UiKit.dialogs để App.Modals.Open<T>() mở.
// Cờ Temp/casino_ug_build.flag (dựng), Temp/casino_ug_tour.flag (vào Play, mở hộp, chụp, bấm Đánh bậc đầu, chụp trận, về đảo, Stop;
// bản lưu sao lưu, trả lại). Ảnh Temp/PokiShots/casino_ham/.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class CasinoUgMenu
    {
        const string SheetBase = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string DialogPath = "Assets/04 Prefabs/Dialogs/HamDau.prefab";
        const string PickerPath = "Assets/04 Prefabs/Dialogs/ChonDoi.prefab";
        const int Rows = 6;

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        [MenuItem("PokiClash/Prefab/Đảo Casino/Hầm đấu: dựng hộp", priority = 73)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var kit = assets.prefabs;
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "HamDau";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(1000, false, false);
                var sheet = view.Sheet;
                foreach (var f in sheet.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(f);
                foreach (var l in sheet.GetComponents<LayoutGroup>()) Object.DestroyImmediate(l);
                sheet.anchorMin = sheet.anchorMax = new Vector2(0.5f, 0.5f);
                sheet.pivot = new Vector2(0.5f, 0.5f);
                sheet.anchoredPosition = new Vector2(0, -30);
                sheet.sizeDelta = new Vector2(1000, 1700);
                var page = HomeSceneMenu.Fill(HomeSceneMenu.Node(sheet, "noi_dung"));
                page.SetAsLastSibling();
                var close = view.Close ? (RectTransform)view.Close.transform : null;
                if (close) close.SetAsLastSibling();

                var title = HomeSceneMenu.Text(page, "tieu_de", 54, Theme.Ink);
                HomeSceneMenu.At(title.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -34), new Vector2(800, 70), new Vector2(0.5f, 1));
                var sub = HomeSceneMenu.Text(page, "doi_minh", 24, Theme.Ink2);
                HomeSceneMenu.At(sub.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -110), new Vector2(900, 80), new Vector2(0.5f, 1));
                sub.enableAutoSizing = true;
                sub.fontSizeMin = 16;
                sub.fontSizeMax = 24;

                var rows = new UndergroundDialog.Row[Rows];
                const float rowH = 206, top = -205;
                for (int i = 0; i < Rows; i++)
                {
                    var panel = HomeSceneMenu.Img(page, "bac_" + i, Sketch.PanelThin, new Color(1f, 0.97f, 0.88f, 1f), false, true);
                    HomeSceneMenu.At(panel.rectTransform, new Vector2(0.5f, 1), new Vector2(0, top - i * (rowH + 8)), new Vector2(940, rowH), new Vector2(0.5f, 1));
                    TextMeshProUGUI T(string n, float size, Color c, float y, float h)
                    {
                        var t = HomeSceneMenu.Text(panel.transform, n, size, c);
                        t.alignment = TextAlignmentOptions.TopLeft;
                        HomeSceneMenu.At(t.rectTransform, new Vector2(0, 1), new Vector2(22, y), new Vector2(640, h), new Vector2(0, 1));
                        t.enableAutoSizing = true;
                        t.fontSizeMin = size * 0.65f;
                        t.fontSizeMax = size;
                        return t;
                    }
                    var head = T("ten", 32, Theme.Ink, -12, 42);
                    var rule = T("luat", 23, Theme.BlueD, -58, 32);
                    var foes = T("doi_ngam", 21, Theme.Ink2, -92, 56);
                    var reward = T("thuong", 21, Theme.GreenD, -150, 50);
                    var fight = HomeSceneMenu.Button(assets, panel.transform, "danh", Loc.T("Đánh"), BtnColor.Green, new Vector2(250, 96));
                    HomeSceneMenu.At((RectTransform)fight.transform, new Vector2(1, 0.5f), new Vector2(-18, 0), new Vector2(250, 96), new Vector2(1, 0.5f));
                    rows[i] = new UndergroundDialog.Row { root = panel.gameObject, head = head, rule = rule, foes = foes, reward = reward, fight = fight };
                }
                var team = HomeSceneMenu.Button(assets, page, "doi_doi", Loc.T("Đổi đội"), BtnColor.Yellow, new Vector2(340, 110));
                HomeSceneMenu.At((RectTransform)team.transform, new Vector2(0.5f, 0), new Vector2(0, 30), new Vector2(340, 110), new Vector2(0.5f, 0));

                var dlgComp = root.AddComponent<UndergroundDialog>();
                var picker = AssetDatabase.LoadAssetAtPath<GameObject>(PickerPath)?.GetComponent<TeamPickerDialog>();
                if (!picker) Debug.LogWarning("[Đảo Casino] Thiếu " + PickerPath + ": nút Đổi đội không mở được hộp chọn đội.");
                dlgComp.Setup(title, sub, rows, team, picker);
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, DialogPath).GetComponent<UndergroundDialog>();
                kit.dialogs.RemoveAll(x => !x || (x is UndergroundDialog && x != dlg));
                if (!kit.dialogs.Contains(dlg)) kit.dialogs.Add(dlg);
                EditorUtility.SetDirty(kit);
                AssetDatabase.SaveAssets();
                Debug.Log("[Đảo Casino] Đã dựng " + DialogPath);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- chụp thử ----------

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_ham");

        static IEnumerator Wait(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(ShotDir);
            foreach (var f in Directory.GetFiles(ShotDir, "*.jpg")) File.Delete(f);
            try
            {
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 120);
                s.balls = Mathf.Max(s.balls, 5000);
                Casino.Of(s).intro = true;
                App.Router.Go(SceneIds.Casino);
                yield return Wait(SceneIds.Casino);
                yield return new WaitForSecondsRealtime(1.2f);
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.4f);
                CasinoGames.Open(Casino.Underground, null);
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot("1_ham_dau");
                var dlg = Object.FindAnyObjectByType<UndergroundDialog>();
                var btn = dlg ? dlg.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "danh" && b.gameObject.activeInHierarchy) : null;
                if (btn)
                {
                    btn.SimulateClick();
                    yield return Wait(SceneIds.Battle);
                    yield return new WaitForSecondsRealtime(3.5f);
                    yield return Shot("2_tran_ngam");
                }
                else Debug.LogWarning("[Thử] Không thấy nút Đánh");
                Debug.Log("[Thử] Xong Hầm đấu: " + Path.GetFullPath(ShotDir));
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(ShotDir, name + ".jpg"), tex.EncodeToJPG(82));
            Object.DestroyImmediate(tex);
        }

        static double nextPoll, tourStart;
        static bool tourRunning;
        static string Flag(string n) => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/" + n));

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            var build = Flag("casino_ug_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                Build();
                return;
            }
            var tour = Flag("casino_ug_tour.flag");
            if (File.Exists(tour) && !tourRunning)
            {
                if (!EditorApplication.isPlaying)
                {
                    if (!EditorApplication.isPlayingOrWillChangePlaymode) EditorApplication.isPlaying = true;
                    return;
                }
                Application.runInBackground = true; // game tắt Run In Background: Unity nằm nền thì vòng game đứng, lượt chụp không chạy
                if (App.I == null || App.Router == null || App.Router.Busy || App.Router.Current == null) return;
                File.Delete(tour);
                tourRunning = true;
                tourStart = EditorApplication.timeSinceStartup;
                App.I.StartCoroutine(TourThenStop());
                return;
            }
            if (tourRunning && EditorApplication.timeSinceStartup - tourStart > 150)
            {
                tourRunning = false;
                EditorApplication.isPlaying = false;
            }
        }

        static IEnumerator TourThenStop()
        {
            yield return new WaitForSecondsRealtime(3f);
            yield return Run();
            yield return new WaitForSecondsRealtime(1f);
            tourRunning = false;
            EditorApplication.isPlaying = false;
        }
    }
}
