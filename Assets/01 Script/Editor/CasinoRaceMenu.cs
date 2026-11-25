// Scene Trường đua của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.3, mốc C5; mỗi trò một scene). Menu
// "PokiClash/Prefab/Đảo Casino/Trường đua: dựng scene" (chạy lại được): Screens/CasinoRace (lần đầu chép từ Screens/Cave, thay bằng
// RaceScene), scene CasinoRace + Build Settings; giao diện: hàng cúp, dòng tin, đường hôm nay, sân dựng sẵn 5 làn (RaceScene chia lại theo
// số tướng 3–5; 3 dải chặng, vạch xuất phát, vạch đích), mỗi làn một tướng (chân dung UiKit.portrait trong khung nhún, sao choáng xoay,
// vụt nổ, chữ nổi, số hạng), dòng tường thuật, tướng đang chọn, Chọn tướng, Đua, Cổ vũ (vòng sáng), tấm kết quả có bảng xếp hạng cả đoàn.
// Nền sân là dải màu tạm, C8 thay hình đường đua.
// Cờ Temp/casino_race_build.flag (dựng), Temp/casino_race_tour.flag (vào Play, đua một lượt tự cổ vũ, chụp Temp/PokiShots/casino_dua/).
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class CasinoRaceMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/CasinoRace.prefab";
        const string BaseScreenPath = "Assets/04 Prefabs/Screens/Cave.prefab";
        const string ScenePath = "Assets/00 Scenes/CasinoRace.unity";
        const string PickerPath = "Assets/04 Prefabs/Dialogs/ChonDoi.prefab";
        const int Lanes = 5;
        const float FieldY = -14, FieldH = 980; // sân: từ dưới nút Nhận quà tuần tới trên dòng tường thuật

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        static RectTransform N(Transform p, string n, params System.Type[] t) => HomeSceneMenu.Node(p, n, t);
        static RectTransform At(RectTransform rt, Vector2 a, Vector2 pos, Vector2 size, Vector2 pivot) => HomeSceneMenu.At(rt, a, pos, size, pivot);
        static Image Img(Transform p, string n, Sprite s, Color c, bool ray = false, bool sliced = false) => HomeSceneMenu.Img(p, n, s, c, ray, sliced);
        static TextMeshProUGUI Txt(Transform p, string n, float size, Color c) => HomeSceneMenu.Text(p, n, size, c);
        static UiKit Kit => AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));

        [MenuItem("PokiClash/Prefab/Đảo Casino/Trường đua: dựng scene", priority = 74)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            if (!File.Exists(ScreenPath))
            {
                if (!AssetDatabase.CopyAsset(BaseScreenPath, ScreenPath)) { Debug.LogError("[Đảo Casino] Không chép được " + BaseScreenPath); return; }
                AssetDatabase.ImportAsset(ScreenPath);
            }
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                root.name = "CasinoRace";
                var scene = root.GetComponent<RaceScene>();
                RectTransform content;
                if (!scene)
                {
                    var old = root.GetComponent<SceneRoot>();
                    PokiCanvas view = null;
                    content = null;
                    if (old)
                    {
                        var so = new SerializedObject(old);
                        view = so.FindProperty("view").objectReferenceValue as PokiCanvas;
                        content = so.FindProperty("content").objectReferenceValue as RectTransform;
                        Object.DestroyImmediate(old);
                    }
                    scene = root.AddComponent<RaceScene>();
                    scene.SetupView(view ? view : root.GetComponentInChildren<PokiCanvas>(true), content);
                }
                else content = scene.Content;
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!nen || !safe) { Debug.LogError("[Đảo Casino] Screens/CasinoRace thiếu Canvas/Nen hoặc Canvas/An toan/Khung."); return; }
                foreach (Transform c in nen) c.gameObject.SetActive(c.name == "nen_hai_ben");
                if (nen.Find("nen_hai_ben")?.GetComponent<Image>() is Image si) { si.sprite = null; si.color = Theme.Hex("#8cc96a"); }
                foreach (Transform c in safe.Cast<Transform>().ToList()) if (c != content) Object.DestroyImmediate(c.gameObject);
                if (content) foreach (Transform c in content.Cast<Transform>().ToList()) Object.DestroyImmediate(c.gameObject);

                var page = HomeSceneMenu.Fill(N(safe, "duong_dua"));
                // trên: cúp
                var cupRow = N(page, "cup", typeof(HorizontalLayoutGroup));
                At(cupRow, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 8), new Vector2(1060, 84), new Vector2(0.5f, 1));
                var hl = cupRow.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = 8; hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false; hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var cups = new SketchButton[5];
                for (int i = 0; i < cups.Length; i++) cups[i] = HomeSceneMenu.Button(assets, cupRow, "cup_" + i, "?", BtnColor.Paper, new Vector2(204, 80));
                var card = Img(page, "the", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.95f), false, true);
                At(card.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 100), new Vector2(1040, 120), new Vector2(0.5f, 1));
                var info = Txt(card.transform, "tin", 26, Theme.Ink);
                At(info.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -10), new Vector2(1000, 44), new Vector2(0.5f, 1));
                info.enableAutoSizing = true; info.fontSizeMin = 16; info.fontSizeMax = 26;
                var track = Txt(card.transform, "duong", 28, Theme.BlueD);
                At(track.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -62), new Vector2(1000, 44), new Vector2(0.5f, 1));
                var claim = HomeSceneMenu.Button(assets, page, "nhan_tuan", Loc.T("Nhận quà tuần"), BtnColor.Yellow, new Vector2(360, 90));
                At((RectTransform)claim.transform, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 230), new Vector2(360, 90), new Vector2(0.5f, 1));

                // sân: 3 dải chặng, vạch xuất phát / đích, 5 làn dựng sẵn (RaceScene chia lại theo số tướng)
                var kit = Kit;
                var outline = Theme.Outlined(Theme.Bold, 0.3f);
                var fieldImg = Img(page, "san", Sketch.PanelThin, Theme.Hex("#c99a64"), false, true);
                var field = fieldImg.rectTransform;
                At(field, new Vector2(0.5f, 0.5f), new Vector2(0, FieldY), new Vector2(1020, FieldH), new Vector2(0.5f, 0.5f));
                var segs = new Image[3];
                for (int i = 0; i < 3; i++)
                {
                    var sg = Img(field, "chang_" + i, null, Color.white);
                    sg.rectTransform.anchorMin = new Vector2(i / 3f, 0);
                    sg.rectTransform.anchorMax = new Vector2((i + 1) / 3f, 1);
                    sg.rectTransform.offsetMin = new Vector2(i == 0 ? 10 : 2, 10);
                    sg.rectTransform.offsetMax = new Vector2(i == 2 ? -10 : -2, -10);
                    segs[i] = sg;
                }
                var start = Img(field, "vach_xuat_phat", null, new Color(1, 1, 1, 0.75f));
                At(start.rectTransform, new Vector2(0, 0.5f), new Vector2(70, 0), new Vector2(6, FieldH - 20), new Vector2(0.5f, 0.5f));
                // vạch đích ca rô: hai cột ô đen trắng
                var finish = N(field, "vach_dich");
                At(finish, new Vector2(1, 0.5f), new Vector2(-70, 0), new Vector2(24, FieldH - 20), new Vector2(0.5f, 0.5f));
                for (int k = 0; k < 2 * (int)((FieldH - 20) / 30); k++)
                {
                    int col = k % 2, row = k / 2;
                    var sq = Img(finish, "o_" + k, null, (col + row) % 2 == 0 ? Theme.Ink : Color.white);
                    At(sq.rectTransform, new Vector2(0.5f, 1), new Vector2(col == 0 ? -6 : 6, -row * 30f), new Vector2(12, 30), new Vector2(0.5f, 1));
                }
                var lanes = new RaceScene.Lane[Lanes];
                float laneH = (FieldH - 20) / Lanes, top = (FieldH - 20) / 2;
                for (int i = 0; i < Lanes; i++)
                {
                    var ln = new RaceScene.Lane();
                    if (i > 0)
                    {
                        var line = Img(field, "ke_" + i, null, new Color(1, 1, 1, 0.55f));
                        At(line.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, top - laneH * i), new Vector2(1000, 4), new Vector2(0.5f, 0.5f));
                        ln.line = line.rectTransform;
                    }
                    float y = top - laneH * (i + 0.5f) - laneH * 0.28f;
                    var bottom = new Vector2(0.5f, 0);
                    // token: chân tướng; body: khung nhún / lắc / lao (con của token)
                    ln.token = N(field, "tuong_" + i);
                    At(ln.token, new Vector2(0, 0.5f), new Vector2(70, y), new Vector2(10, 10), new Vector2(0.5f, 0));
                    ln.body = N(ln.token, "than");
                    At(ln.body, bottom, Vector2.zero, new Vector2(10, 10), bottom);
                    ln.portrait = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, ln.body)).GetComponent<HeroPortrait>();
                    ln.portrait.name = "chan_dung";
                    At(ln.portrait.Rect, bottom, new Vector2(0, -110 * HeroArt.FootY), new Vector2(110f * HeroArt.W / HeroArt.H, 110), bottom);
                    foreach (var g in ln.portrait.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
                    ln.face = new SerializedObject(ln.portrait).FindProperty("body").objectReferenceValue as Image;
                    // sao choáng: vòng 3 sao xoay, dẹt thành elip (khung ngoài bóp dọc)
                    ln.stars = N(ln.body, "sao_choang");
                    At(ln.stars, bottom, new Vector2(0, 104), new Vector2(10, 10), new Vector2(0.5f, 0.5f));
                    ln.spin = N(ln.stars, "xoay");
                    At(ln.spin, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(10, 10), new Vector2(0.5f, 0.5f));
                    for (int k = 0; k < 3; k++)
                    {
                        float ang = k * Mathf.PI * 2 / 3;
                        var st = Img(ln.spin, "sao_" + k, Sketch.Star, Theme.Yellow);
                        At(st.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(Mathf.Cos(ang) * 40, Mathf.Sin(ang) * 14), new Vector2(46, 46), new Vector2(0.5f, 0.5f));
                    }
                    ln.stars.gameObject.SetActive(false);
                    // vụt nổ chỗ trúng (trước tướng)
                    ln.burst = Img(ln.body, "vut_no", Sketch.Burst, new Color(1f, 0.85f, 0.25f));
                    At(ln.burst.rectTransform, bottom, new Vector2(28, 55), new Vector2(120, 120), new Vector2(0.5f, 0.5f));
                    ln.burst.gameObject.SetActive(false);
                    // tên dưới chân
                    ln.name = Txt(ln.token, "ten", 22, Theme.Ink);
                    At(ln.name.rectTransform, new Vector2(0.5f, 0), new Vector2(0, -2), new Vector2(240, 28), new Vector2(0.5f, 1));
                    ln.name.textWrappingMode = TextWrappingModes.NoWrap;
                    // chữ nổi (Choáng! Vấp! Né! Gió thuận!)
                    ln.pop = Txt(ln.token, "chu_noi", 34, Theme.RedD);
                    At(ln.pop.rectTransform, bottom, new Vector2(56, 60), new Vector2(260, 44), new Vector2(0, 0.5f));
                    ln.pop.alignment = TextAlignmentOptions.MidlineLeft;
                    ln.pop.textWrappingMode = TextWrappingModes.NoWrap;
                    if (outline) ln.pop.fontSharedMaterial = outline;
                    ln.pop.gameObject.SetActive(false);
                    // số hạng khi về đích
                    ln.badge = Img(ln.token, "hang", Sketch.Dot, Theme.Yellow);
                    At(ln.badge.rectTransform, bottom, new Vector2(-55, 60), new Vector2(58, 58), new Vector2(0.5f, 0.5f));
                    var bo = Img(ln.badge.transform, "vien", Sketch.Ring, Theme.Ink);
                    HomeSceneMenu.Fill(bo.rectTransform);
                    ln.badgeText = Txt(ln.badge.transform, "so", 34, Theme.Ink);
                    HomeSceneMenu.Fill(ln.badgeText.rectTransform);
                    ln.badge.gameObject.SetActive(false);
                    lanes[i] = ln;
                }
                // tường thuật dưới sân
                var talkBg = Img(page, "tuong_thuat", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.95f), false, true);
                At(talkBg.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, FieldY - FieldH / 2 - 10), new Vector2(1020, 70), new Vector2(0.5f, 1));
                var talk = Txt(talkBg.transform, "chu", 28, Theme.Ink);
                At(talk.rectTransform, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(980, 60), new Vector2(0.5f, 0.5f));
                talk.enableAutoSizing = true; talk.fontSizeMin = 18; talk.fontSizeMax = 28;

                // dưới: tướng, chọn tướng, đua, cổ vũ
                var heroCard = Img(page, "tuong_minh", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.95f), false, true);
                At(heroCard.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 190), new Vector2(1040, 76), new Vector2(0.5f, 0));
                var hero = Txt(heroCard.transform, "chu", 28, Theme.Ink);
                HomeSceneMenu.Fill(hero.rectTransform);
                var pick = HomeSceneMenu.Button(assets, page, "chon_tuong", Loc.T("Chọn tướng"), BtnColor.Paper, new Vector2(400, 130));
                At((RectTransform)pick.transform, new Vector2(0.5f, 0), new Vector2(-250, 40), new Vector2(400, 130), new Vector2(0.5f, 0));
                var go = HomeSceneMenu.Button(assets, page, "dua", Loc.T("Đua"), BtnColor.Green, new Vector2(460, 130));
                At((RectTransform)go.transform, new Vector2(0.5f, 0), new Vector2(230, 40), new Vector2(460, 130), new Vector2(0.5f, 0));
                var ringImg = Img(page, "vong_sang", Sketch.Round, new Color(1f, 0.85f, 0.3f, 0.75f));
                At(ringImg.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 105), new Vector2(170, 170), new Vector2(0.5f, 0.5f));
                ringImg.gameObject.SetActive(false);
                var cheer = HomeSceneMenu.Button(assets, page, "co_vu", Loc.T("Cổ vũ!"), BtnColor.Yellow, new Vector2(170, 170));
                At((RectTransform)cheer.transform, new Vector2(0.5f, 0), new Vector2(0, 105), new Vector2(170, 170), new Vector2(0.5f, 0.5f));
                var cheerText = Txt(page, "co_vu_chu", 38, Color.white);
                At(cheerText.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 290), new Vector2(980, 60), new Vector2(0.5f, 0)); // trên dòng tướng
                if (outline) cheerText.fontSharedMaterial = outline;

                // kết quả
                var res = Img(page, "ket_qua", null, new Color(0.1f, 0.08f, 0.06f, 0.55f), true);
                HomeSceneMenu.Fill(res.rectTransform);
                var rc = Img(res.transform, "giay", Sketch.PanelThin, Theme.Paper, true, true);
                At(rc.rectTransform, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(880, 840), new Vector2(0.5f, 0.5f));
                var rTitle = Txt(rc.transform, "hang", 60, Theme.Ink);
                At(rTitle.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -40), new Vector2(800, 80), new Vector2(0.5f, 1));
                var rInfo = Txt(rc.transform, "thuong", 32, Theme.Ink2);
                At(rInfo.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -128), new Vector2(800, 110), new Vector2(0.5f, 1));
                var rowsBg = Img(rc.transform, "bang", Sketch.PanelThin, Theme.Paper2, false, true);
                At(rowsBg.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -250), new Vector2(800, 300), new Vector2(0.5f, 1));
                var rRows = new TextMeshProUGUI[Lanes];
                for (int i = 0; i < Lanes; i++)
                {
                    rRows[i] = Txt(rowsBg.transform, "dong_" + i, 28, Theme.Ink);
                    At(rRows[i].rectTransform, new Vector2(0.5f, 1), new Vector2(0, -14 - i * 56), new Vector2(760, 52), new Vector2(0.5f, 1));
                    rRows[i].enableAutoSizing = true; rRows[i].fontSizeMin = 18; rRows[i].fontSizeMax = 28;
                    rRows[i].alignment = TextAlignmentOptions.MidlineLeft;
                }
                var again = HomeSceneMenu.Button(assets, rc.transform, "dua_lai", Loc.T("Đua lại"), BtnColor.Green, new Vector2(300, 110));
                At((RectTransform)again.transform, new Vector2(0.5f, 0), new Vector2(-170, 40), new Vector2(300, 110), new Vector2(0.5f, 0));
                var done = HomeSceneMenu.Button(assets, rc.transform, "xong", Loc.T("Xong"), BtnColor.Paper, new Vector2(300, 110));
                At((RectTransform)done.transform, new Vector2(0.5f, 0), new Vector2(170, 40), new Vector2(300, 110), new Vector2(0.5f, 0));
                res.gameObject.SetActive(false);

                var picker = AssetDatabase.LoadAssetAtPath<GameObject>(PickerPath)?.GetComponent<TeamPickerDialog>();
                scene.Setup(cups, info, track, talk, claim, field, segs, lanes, hero, pick, go, cheer, ringImg.rectTransform, cheerText, res.gameObject, rTitle,
                    rInfo, rRows, again, done, picker);
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            MakeScene();
            AssetDatabase.SaveAssets();
            Debug.Log("[Đảo Casino] Đã dựng " + ScreenPath + ", " + ScenePath);
        }

        static void MakeScene()
        {
            if (!File.Exists(ScenePath))
            {
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
                var prev = SceneManager.GetActiveScene();
                SceneManager.SetActiveScene(scene);
                ((GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(ScreenPath))).name = SceneIds.CasinoRace;
                SceneManager.SetActiveScene(prev);
                EditorSceneManager.SaveScene(scene, ScenePath);
                EditorSceneManager.CloseScene(scene, true);
            }
            else
            {
                var scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Additive);
                foreach (var go in scene.GetRootGameObjects())
                    if (PrefabUtility.IsPartOfPrefabInstance(go))
                        PrefabUtility.RevertPrefabInstance(PrefabUtility.GetOutermostPrefabInstanceRoot(go), InteractionMode.AutomatedAction);
                EditorSceneManager.SaveScene(scene);
                EditorSceneManager.CloseScene(scene, true);
            }
            var list = EditorBuildSettings.scenes.ToList();
            if (list.All(x => x.path != ScenePath))
            {
                list.Add(new EditorBuildSettingsScene(ScenePath, true));
                EditorBuildSettings.scenes = list.ToArray();
            }
        }

        // ---------- chụp thử ----------

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_dua");

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(ShotDir);
            foreach (var f in Directory.GetFiles(ShotDir, "*.jpg")) File.Delete(f);
            try
            {
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 75);
                s.balls = Mathf.Max(s.balls, 3000);
                foreach (var h in App.Data.Heroes.Where(h => !h.minion).Take(8)) s.Hero(h.id).owned = true;
                Casino.Of(s).intro = true;
                App.Router.Go(SceneIds.CasinoRace, Casino.Race);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.CasinoRace) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(1.2f);
                App.Modals.CloseAll();
                yield return Shot("1_truoc_dua");
                var sc = Object.FindAnyObjectByType<RaceScene>();
                sc.GetComponentsInChildren<SketchButton>(true).First(b => b.name == "dua").SimulateClick();
                int cheered = -1;
                float t1 = Time.realtimeSinceStartup;
                bool mid = false, stunShot = false;
                while (sc.Game != null && !sc.Game.done && Time.realtimeSinceStartup - t1 < 40)
                {
                    int k = Race.CheerSeg(sc.Game);
                    if (k >= 0 && k != cheered && Race.SinceSegStart(sc.Game) >= 0.98)
                    {
                        cheered = k;
                        sc.GetComponentsInChildren<SketchButton>(true).First(b => b.name == "co_vu").SimulateClick();
                    }
                    if (!mid && Time.realtimeSinceStartup - t1 > 7)
                    {
                        mid = true;
                        yield return Shot("2_dang_dua");
                    }
                    if (!stunShot && sc.Game.events.Any(e => e.kind == RaceEv.Hit))
                    {
                        stunShot = true;
                        yield return Shot("2b_danh_0");
                        yield return new WaitForSecondsRealtime(0.12f);
                        yield return Shot("2b_danh_1");
                        yield return new WaitForSecondsRealtime(0.2f);
                        yield return Shot("2b_danh_2");
                        yield return new WaitForSecondsRealtime(0.4f);
                        yield return Shot("2b_danh_3");
                    }
                    yield return null;
                }
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot("3_ket_qua");
                var g = sc.Game;
                if (g != null)
                    Debug.Log($"[Thử] Đua: {g.runners.Count} tướng, {g.events.Count(e => e.kind == RaceEv.Hit)} cú trúng, " +
                              $"{g.events.Count(e => e.kind == RaceEv.Trip || e.kind == RaceEv.Dodge)} hụt / né, hạng mình {Race.PlaceOf(g) + 1}, {g.t:F1} giây");
                Debug.Log("[Thử] Xong Trường đua: " + Path.GetFullPath(ShotDir));
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
            var build = Flag("casino_race_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                Build();
                return;
            }
            var tour = Flag("casino_race_tour.flag");
            if (File.Exists(tour) && !tourRunning)
            {
                if (!EditorApplication.isPlaying)
                {
                    if (!EditorApplication.isPlayingOrWillChangePlaymode) EditorApplication.isPlaying = true;
                    return;
                }
                Application.runInBackground = true; // Unity nằm nền thì vòng game đứng
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
