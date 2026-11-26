// Scene Chợ đen của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.4, mốc C6; mỗi trò một scene). Menu
// "PokiClash/Prefab/Đảo Casino/Chợ đen: dựng scene" (chạy lại được): Screens/CasinoMarket (lần đầu chép từ Screens/Cave, thay bằng
// MarketScene), scene CasinoMarket + Build Settings; giao diện: tờ lái buôn (hình chợ cắt từ đảo, lời lái buôn, đồng hồ đổi hàng), kệ 8 ô
// dựng sẵn (2 hàng × 3 ô ngày, hàng thứ ba 2 ô đêm hoặc bảng báo hàng đêm), mỗi ô: ô thưởng Items/OThuong, ghi chú, nút giá, dấu Đã mua,
// nhãn Hàng đêm; nút Làm mới, Tỉ lệ túi lậu; tờ Thu mua (giỏ cá, bản sao thẻ thừa). Nền tạm màu gỗ, C8 thay hình chợ thật.
// Cờ Temp/casino_market_build.flag (dựng), Temp/casino_market_tour.flag (vào Play, chụp ban ngày, mua một ô, chụp ban đêm giả lập,
// mở Quán trọ trên đảo; chụp Temp/PokiShots/casino_cho/; bản lưu sao lưu, trả lại).
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
    public static class CasinoMarketMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/CasinoMarket.prefab";
        const string BaseScreenPath = "Assets/04 Prefabs/Screens/Cave.prefab";
        const string ScenePath = "Assets/00 Scenes/CasinoMarket.unity";
        const string TilePath = "Assets/04 Prefabs/Items/OThuong.prefab";
        const string MarketArt = "Assets/03 Art/Casino/casino_ct_cho.png";
        const int Cols = 3, Slots = 8;
        const float ShelfW = 1040, Gap = 14, SlotH = 340, TopH = 170;
        static float SlotW => (ShelfW - Gap * (Cols - 1)) / Cols;

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        static RectTransform N(Transform p, string n, params System.Type[] t) => HomeSceneMenu.Node(p, n, t);
        static RectTransform At(RectTransform rt, Vector2 a, Vector2 pos, Vector2 size, Vector2 pivot) => HomeSceneMenu.At(rt, a, pos, size, pivot);
        static Image Img(Transform p, string n, Sprite s, Color c, bool ray = false, bool sliced = false) => HomeSceneMenu.Img(p, n, s, c, ray, sliced);
        static TextMeshProUGUI Txt(Transform p, string n, float size, Color c) => HomeSceneMenu.Text(p, n, size, c);

        static TextMeshProUGUI Auto(TextMeshProUGUI t, float min)
        {
            t.enableAutoSizing = true;
            t.fontSizeMin = min;
            t.fontSizeMax = t.fontSize;
            return t;
        }

        [MenuItem("PokiClash/Prefab/Đảo Casino/Chợ đen: dựng scene", priority = 75)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var tilePrefab = AssetDatabase.LoadAssetAtPath<GameObject>(TilePath);
            if (!tilePrefab || !tilePrefab.GetComponent<RewardTile>()) { Debug.LogError("[Đảo Casino] Thiếu " + TilePath); return; }
            if (!File.Exists(ScreenPath))
            {
                if (!AssetDatabase.CopyAsset(BaseScreenPath, ScreenPath)) { Debug.LogError("[Đảo Casino] Không chép được " + BaseScreenPath); return; }
                AssetDatabase.ImportAsset(ScreenPath);
            }
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                root.name = "CasinoMarket";
                var scene = root.GetComponent<MarketScene>();
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
                    scene = root.AddComponent<MarketScene>();
                    scene.SetupView(view ? view : root.GetComponentInChildren<PokiCanvas>(true), content);
                }
                else content = scene.Content;
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!nen || !safe) { Debug.LogError("[Đảo Casino] Screens/CasinoMarket thiếu Canvas/Nen hoặc Canvas/An toan/Khung."); return; }
                foreach (Transform c in nen) c.gameObject.SetActive(c.name == "nen_hai_ben");
                if (nen.Find("nen_hai_ben")?.GetComponent<Image>() is Image si) { si.sprite = null; si.color = Theme.Hex("#8a6a4f"); }
                foreach (Transform c in safe.Cast<Transform>().ToList()) if (c != content) Object.DestroyImmediate(c.gameObject);
                if (content) foreach (Transform c in content.Cast<Transform>().ToList()) Object.DestroyImmediate(c.gameObject);

                var page = HomeSceneMenu.Fill(N(safe, "cho_den"));
                var paper = new Color(1f, 0.98f, 0.92f, 0.96f);
                var outline = Theme.Outlined(Theme.Bold, 0.3f);

                // trên: tờ lái buôn
                var top = Img(page, "lai_buon", Sketch.PanelThin, paper, false, true);
                At(top.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 8), new Vector2(ShelfW, TopH), new Vector2(0.5f, 1));
                var pic = Img(top.transform, "hinh_cho", AssetDatabase.LoadAssetAtPath<Sprite>(MarketArt), Color.white);
                pic.preserveAspect = true;
                At(pic.rectTransform, new Vector2(0, 0.5f), new Vector2(14, 0), new Vector2(124, TopH - 16), new Vector2(0, 0.5f));
                var talk = Auto(Txt(top.transform, "loi", 28, Theme.Ink), 18);
                talk.alignment = TextAlignmentOptions.MidlineLeft;
                At(talk.rectTransform, new Vector2(0, 1), new Vector2(150, -10), new Vector2(ShelfW - 170, 96), new Vector2(0, 1));
                var info = Auto(Txt(top.transform, "dong_ho", 24, Theme.BlueD), 16);
                info.alignment = TextAlignmentOptions.MidlineLeft;
                At(info.rectTransform, new Vector2(0, 0), new Vector2(150, 12), new Vector2(ShelfW - 170, 44), new Vector2(0, 0));

                // kệ: 8 ô dựng sẵn
                var shelf = N(page, "ke");
                float shelfY = -SceneRoot.BarHeight - 8 - TopH - Gap;
                At(shelf, new Vector2(0.5f, 1), new Vector2(0, shelfY), new Vector2(ShelfW, SlotH * 3 + Gap * 2), new Vector2(0.5f, 1));
                Vector2 SlotPos(int i) => new Vector2(-ShelfW / 2 + SlotW / 2 + (i % Cols) * (SlotW + Gap), -(i / Cols) * (SlotH + Gap));
                // bảng báo hàng đêm (ban ngày thay hàng thứ ba)
                var noteBg = Img(shelf, "bao_hang_dem", Sketch.PanelThin, MarketScene.NightTint, false, true);
                At(noteBg.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -2 * (SlotH + Gap)), new Vector2(ShelfW, SlotH), new Vector2(0.5f, 1));
                var art = Load<ArtLibrary>();
                var moon = Img(noteBg.transform, "trang", art ? art.Icon("moon") : null, Theme.Ink2);
                moon.preserveAspect = true;
                At(moon.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -30), new Vector2(90, 90), new Vector2(0.5f, 1));
                var nightNote = Auto(Txt(noteBg.transform, "chu", 30, Theme.Ink), 18);
                At(nightNote.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 30), new Vector2(ShelfW - 80, 150), new Vector2(0.5f, 0));
                var slots = new MarketScene.Slot[Slots];
                for (int i = 0; i < Slots; i++)
                {
                    var card = Img(shelf, "o_" + i, Sketch.PanelThin, Theme.Paper, false, true);
                    At(card.rectTransform, new Vector2(0.5f, 1), SlotPos(i), new Vector2(SlotW, SlotH), new Vector2(0.5f, 1));
                    var tile = ((GameObject)PrefabUtility.InstantiatePrefab(tilePrefab, card.transform)).GetComponent<RewardTile>();
                    tile.name = "mon";
                    At(tile.Rect, new Vector2(0.5f, 1), new Vector2(0, -14), new Vector2(RewardTile.W, RewardTile.H), new Vector2(0.5f, 1));
                    foreach (var g in tile.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
                    var note = Auto(Txt(card.transform, "ghi_chu", 21, Theme.Ink2), 14);
                    At(note.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -RewardTile.H - 16), new Vector2(SlotW - 20, 32), new Vector2(0.5f, 1));
                    var buy = HomeSceneMenu.Button(assets, card.transform, "mua", "0", BtnColor.Green, new Vector2(SlotW - 50, 76));
                    At((RectTransform)buy.transform, new Vector2(0.5f, 0), new Vector2(0, 12), new Vector2(SlotW - 50, 76), new Vector2(0.5f, 0));
                    var sold = Txt(card.transform, "da_mua", 46, Theme.RedD);
                    At(sold.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 30), new Vector2(SlotW - 20, 64), new Vector2(0.5f, 0));
                    sold.rectTransform.localEulerAngles = new Vector3(0, 0, 8);
                    if (outline) sold.fontSharedMaterial = outline;
                    sold.gameObject.SetActive(false);
                    var tagBg = Img(card.transform, "nhan_dem", Sketch.Pill, Theme.Hex("#3b4a7a"), false, true);
                    At(tagBg.rectTransform, new Vector2(1, 1), new Vector2(-6, -6), new Vector2(118, 38), new Vector2(1, 1));
                    var tag = Auto(Txt(tagBg.transform, "chu", 20, Color.white), 12);
                    HomeSceneMenu.Fill(tag.rectTransform);
                    tagBg.gameObject.SetActive(i >= 6);
                    slots[i] = new MarketScene.Slot { root = card.gameObject, card = card, tile = tile, note = note, sold = sold, tag = tag, buy = buy };
                }

                // nút: làm mới, tỉ lệ
                float rowY = shelfY - (SlotH * 3 + Gap * 2) - 16;
                var restock = HomeSceneMenu.Button(assets, page, "lam_moi", Loc.T("Làm mới"), BtnColor.Yellow, new Vector2(500, 104));
                At((RectTransform)restock.transform, new Vector2(0.5f, 1), new Vector2(-265, rowY), new Vector2(500, 104), new Vector2(0.5f, 1));
                var odds = HomeSceneMenu.Button(assets, page, "ti_le", Loc.T("Tỉ lệ túi lậu"), BtnColor.Paper, new Vector2(500, 104));
                At((RectTransform)odds.transform, new Vector2(0.5f, 1), new Vector2(265, rowY), new Vector2(500, 104), new Vector2(0.5f, 1));

                // dưới: thu mua
                var sell = Img(page, "thu_mua", Sketch.PanelThin, paper, false, true);
                At(sell.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 30), new Vector2(ShelfW, 236), new Vector2(0.5f, 0));
                var sellTitle = Txt(sell.transform, "tieu_de", 30, Theme.Ink);
                At(sellTitle.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -10), new Vector2(ShelfW - 40, 40), new Vector2(0.5f, 1));
                sellTitle.text = Loc.T("Lái buôn thu mua");
                TextMeshProUGUI Line(string n, float y)
                {
                    var t = Auto(Txt(sell.transform, n, 26, Theme.Ink2), 16);
                    t.alignment = TextAlignmentOptions.MidlineLeft;
                    At(t.rectTransform, new Vector2(0, 1), new Vector2(26, y), new Vector2(ShelfW - 400, 80), new Vector2(0, 1));
                    return t;
                }
                SketchButton Btn(string n, float y)
                {
                    var b = HomeSceneMenu.Button(assets, sell.transform, n, Loc.T("Bán"), BtnColor.Green, new Vector2(330, 84));
                    At((RectTransform)b.transform, new Vector2(1, 1), new Vector2(-20, y + 2), new Vector2(330, 84), new Vector2(1, 1));
                    return b;
                }
                var fishText = Line("gio_ca", -56);
                var sellFish = Btn("ban_ca", -56);
                var spareText = Line("the_thua", -146);
                var sellSpare = Btn("ban_the", -146);

                scene.Setup(talk, info, slots, nightNote, restock, odds, fishText, spareText, sellFish, sellSpare);
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
                ((GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(ScreenPath))).name = SceneIds.CasinoMarket;
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

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_cho");

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
                var d = App.Data;
                s.level = Mathf.Max(s.level, 60);
                s.balls = Mathf.Max(s.balls, 5000);
                foreach (var h in d.Heroes.Where(h => !h.minion).Take(8)) s.Hero(h.id).owned = true;
                var st = Casino.Of(s);
                st.intro = true;
                // giỏ có 3 con cá, một thẻ tối đa cấp có bản sao thừa: để tờ thu mua có việc
                var fish = d.Cfg.casino.fishing.fish.Take(3).ToList();
                foreach (var f in fish) st.creel.Add(new CaughtFish { id = f.id, size = f.max });
                var hp = s.Hero(d.Heroes.First(h => !h.minion).id);
                hp.Card(Core.Progress.Slots[0]).lv = d.Cfg.cardMax;
                hp.Card(Core.Progress.Slots[0]).copies = 45;
                // nhiệm vụ quán trọ: xong một việc để thấy nút Nhận
                double now = Game.SaveService.Now();
                var qs = Casino.InnToday(s, d, now);
                if (qs.Count > 0) Casino.Track(s, d, qs[0].kind, qs[0].n, now);
                App.Router.Go(SceneIds.Casino);
                yield return Wait(SceneIds.Casino);
                yield return new WaitForSecondsRealtime(1.2f);
                App.Modals.CloseAll();
                CasinoGames.Open(Casino.Inn, null);
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot("1_quan_tro");
                var inn = Object.FindAnyObjectByType<InnDialog>();
                var claim = inn ? inn.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "hanh_dong" && !b.Locked && b.gameObject.activeInHierarchy) : null;
                if (claim)
                {
                    claim.SimulateClick();
                    yield return new WaitForSecondsRealtime(0.6f);
                    yield return Shot("2_quan_tro_nhan");
                }
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.3f);
                CasinoGames.Open(Casino.Market, null);
                yield return Wait(SceneIds.CasinoMarket);
                yield return new WaitForSecondsRealtime(1.0f);
                App.Modals.CloseAll();
                yield return Shot("3_cho_den");
                var sc = Object.FindAnyObjectByType<MarketScene>();
                if (sc && sc.BuyFirstForTest("shards"))
                {
                    yield return new WaitForSecondsRealtime(0.5f);
                    yield return Shot("4_mua_manh");
                }
                if (sc && sc.BuyFirstForTest("mystery"))
                {
                    yield return new WaitForSecondsRealtime(1.6f);
                    yield return Shot("5_tui_lau");
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                var oddsBtn = sc ? sc.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "ti_le") : null;
                if (oddsBtn)
                {
                    oddsBtn.SimulateClick();
                    yield return new WaitForSecondsRealtime(0.6f);
                    yield return Shot("6_ti_le");
                    App.Modals.CloseAll();
                }
                Debug.Log("[Thử] Xong Chợ đen + Quán trọ: " + Path.GetFullPath(ShotDir));
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
            var build = Flag("casino_market_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                CasinoInnMenu.Build();
                Build();
                return;
            }
            var tour = Flag("casino_market_tour.flag");
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
