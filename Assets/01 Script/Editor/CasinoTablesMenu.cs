// Ba scene lều lữ khách của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.6–6.7, mốc C7; mỗi trò một scene): CasinoBlackjack (BlackjackScene),
// CasinoRoulette (RouletteScene), CasinoSlot (SlotScene). Menu "PokiClash/Prefab/Đảo Casino/Lều lữ khách: dựng 3 scene" (chạy lại được):
// Screens/<tên> (lần đầu chép từ Screens/Cave, thay bằng scene của lều), scene + Build Settings. Phần chung trên đầu (CasinoTableScene):
// hàng 4 bậc cược, tờ tin (sự kiện, khách mời, hôm nay đã cược / đã thắng, chế độ), Hũ bàn (Kit/bar), nút Cách chơi.
// - Blackjack: hàng 8 lá dealer, 2 tay người chơi (8 lá mỗi tay, tổng, kết quả), dòng kết quả lớn, gợi ý, Chia bài / Rút / Dằn / Gấp đôi / Tách.
// - Roulette: bánh xe 26 ô xếp vòng (mỗi ô là nút đặt chip Ô đơn), viên bi, 5 cửa Hệ, 5 cửa Số, Sao Vàng, Bỏ chip, Quay.
// - Máy quả: khung 3 × 3 ô, dòng đường thắng, Quay, Quay nhanh, Bảng trả.
// Nền tạm màu, lá bài / bánh xe / máy vẽ bằng ô giấy + icon (C8 thay hình thật, diễn để sau).
// Cờ Temp/casino_tables_build.flag (dựng), Temp/casino_tables_tour.flag (vào Play, ép ba lều mở hôm nay trong bộ nhớ, chơi thử mỗi lều,
// chụp Temp/PokiShots/casino_leu/; bản lưu sao lưu, trả lại).
using System;
using System.Collections;
using System.Collections.Generic;
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
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class CasinoTablesMenu
    {
        const string BaseScreenPath = "Assets/04 Prefabs/Screens/Cave.prefab";
        const float W = 1040;
        const float TopY = -SceneRoot.BarHeight - 8;
        const float ContentY = TopY - 80 - 12 - 150 - 12 - 96 - 14; // dưới phần chung

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        static RectTransform N(Transform p, string n, params Type[] t) => HomeSceneMenu.Node(p, n, t);
        static RectTransform At(RectTransform rt, Vector2 a, Vector2 pos, Vector2 size, Vector2 pivot) => HomeSceneMenu.At(rt, a, pos, size, pivot);
        static Image Img(Transform p, string n, Sprite s, Color c, bool ray = false, bool sliced = false) => HomeSceneMenu.Img(p, n, s, c, ray, sliced);
        static readonly Vector2 Top = new Vector2(0.5f, 1), Bottom = new Vector2(0.5f, 0), Mid = new Vector2(0.5f, 0.5f);

        static TextMeshProUGUI Txt(Transform p, string n, float size, Color c, bool auto = true)
        {
            var t = HomeSceneMenu.Text(p, n, size, c);
            if (!auto) return t;
            t.enableAutoSizing = true;
            t.fontSizeMin = size * 0.6f;
            t.fontSizeMax = size;
            return t;
        }

        static SketchButton Btn(UiAssets a, Transform p, string n, string label, BtnColor c, Vector2 anchor, Vector2 pos, Vector2 size)
        {
            var b = HomeSceneMenu.Button(a, p, n, label, c, size);
            At((RectTransform)b.transform, anchor, pos, size, anchor);
            return b;
        }

        [MenuItem("PokiClash/Prefab/Đảo Casino/Lều lữ khách: dựng 3 scene", priority = 77)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var art = Load<ArtLibrary>();
            Make<BlackjackScene>(assets, SceneIds.CasinoBlackjack, "#2f6b4a", (root, page) => BuildBlackjack(assets, art, root, page));
            Make<RouletteScene>(assets, SceneIds.CasinoRoulette, "#5b3a6e", (root, page) => BuildRoulette(assets, art, root, page));
            Make<SlotScene>(assets, SceneIds.CasinoSlot, "#7a4a2a", (root, page) => BuildSlot(assets, art, root, page));
            AssetDatabase.SaveAssets();
        }

        static string ScreenPath(string id) => $"Assets/04 Prefabs/Screens/{id}.prefab";
        static string ScenePath(string id) => $"Assets/00 Scenes/{id}.unity";

        static void Make<T>(UiAssets assets, string id, string bg, Action<T, RectTransform> body) where T : CasinoTableScene
        {
            string path = ScreenPath(id);
            if (!File.Exists(path))
            {
                if (!AssetDatabase.CopyAsset(BaseScreenPath, path)) { Debug.LogError("[Đảo Casino] Không chép được " + BaseScreenPath); return; }
                AssetDatabase.ImportAsset(path);
            }
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                root.name = id;
                var scene = root.GetComponent<T>();
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
                    scene = root.AddComponent<T>();
                    scene.SetupView(view ? view : root.GetComponentInChildren<PokiCanvas>(true), content);
                }
                else content = scene.Content;
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!nen || !safe) { Debug.LogError($"[Đảo Casino] Screens/{id} thiếu Canvas/Nen hoặc Canvas/An toan/Khung."); return; }
                foreach (Transform c in nen) c.gameObject.SetActive(c.name == "nen_hai_ben");
                if (nen.Find("nen_hai_ben")?.GetComponent<Image>() is Image si) { si.sprite = null; si.color = Theme.Hex(bg); }
                foreach (Transform c in safe.Cast<Transform>().ToList()) if (c != content) Object.DestroyImmediate(c.gameObject);
                if (content) foreach (Transform c in content.Cast<Transform>().ToList()) Object.DestroyImmediate(c.gameObject);
                var page = HomeSceneMenu.Fill(N(safe, "leu"));
                Common(assets, scene, page);
                body(scene, page);
                PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            MakeScene(id);
            Debug.Log("[Đảo Casino] Đã dựng " + path + ", " + ScenePath(id));
        }

        // phần chung: bậc cược, tờ tin, Hũ bàn, Cách chơi
        static void Common(UiAssets assets, CasinoTableScene scene, RectTransform page)
        {
            var row = N(page, "bac_cuoc", typeof(HorizontalLayoutGroup));
            At(row, Top, new Vector2(0, TopY), new Vector2(W, 80), Top);
            var hl = row.GetComponent<HorizontalLayoutGroup>();
            hl.spacing = 10; hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = false; hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            var tiers = new SketchButton[4];
            for (int i = 0; i < tiers.Length; i++) tiers[i] = HomeSceneMenu.Button(assets, row, "bac_" + i, "?", BtnColor.Paper, new Vector2(250, 78));
            var paper = new Color(1f, 0.98f, 0.92f, 0.96f);
            var card = Img(page, "tin", Sketch.PanelThin, paper, false, true);
            At(card.rectTransform, Top, new Vector2(0, TopY - 92), new Vector2(W, 150), Top);
            var guest = Txt(card.transform, "su_kien", 26, Theme.BlueD);
            At(guest.rectTransform, Top, new Vector2(0, -8), new Vector2(W - 40, 64), Top);
            var today = Txt(card.transform, "hom_nay", 22, Theme.Ink2);
            At(today.rectTransform, Top, new Vector2(0, -74), new Vector2(W - 40, 32), Top);
            var mode = Txt(card.transform, "che_do", 24, Theme.GreenD);
            At(mode.rectTransform, Top, new Vector2(0, -108), new Vector2(W - 40, 34), Top);
            var kit = assets.prefabs;
            var jar = ((GameObject)PrefabUtility.InstantiatePrefab(kit.bar.gameObject, page)).GetComponent<UiBar>();
            jar.name = "hu_ban";
            jar.SetKind(UiBar.Kind.Shard);
            At((RectTransform)jar.transform, new Vector2(0, 1), new Vector2(40, TopY - 254), new Vector2(620, 40), new Vector2(0, 1));
            var jarText = Txt(page, "hu_qua", 21, Color.white);
            jarText.alignment = TextAlignmentOptions.MidlineLeft;
            At(jarText.rectTransform, new Vector2(0, 1), new Vector2(40, TopY - 298), new Vector2(660, 40), new Vector2(0, 1));
            var help = Btn(assets, page, "cach_choi", "?", BtnColor.Paper, new Vector2(1, 1), new Vector2(-30, TopY - 250), new Vector2(300, 90));
            ((RectTransform)help.transform).pivot = new Vector2(1, 1);
            scene.SetupTable(tiers, today, mode, guest, jar, jarText, help);
        }

        // ---------- Blackjack ----------

        static BlackjackScene.Card Card(Transform p, string n, Vector2 pos, ArtLibrary art)
        {
            var face = Img(p, n, Sketch.PanelThin, Color.white, false, true);
            At(face.rectTransform, new Vector2(0, 1), pos, new Vector2(108, 150), new Vector2(0, 1));
            var rank = Txt(face.transform, "hang", 40, Theme.Ink, false);
            rank.alignment = TextAlignmentOptions.TopLeft;
            At(rank.rectTransform, new Vector2(0, 1), new Vector2(10, -6), new Vector2(80, 50), new Vector2(0, 1));
            var suit = Img(face.transform, "chat", art ? art.Icon("e_kim") : null, Color.white);
            suit.preserveAspect = true;
            At(suit.rectTransform, Mid, new Vector2(8, -16), new Vector2(64, 64), Mid);
            var back = Img(face.transform, "lung", Sketch.PanelThin, Theme.Hex("#8b3a3a"), false, true);
            HomeSceneMenu.Fill(back.rectTransform);
            back.rectTransform.offsetMin = new Vector2(6, 6);
            back.rectTransform.offsetMax = new Vector2(-6, -6);
            var q = Txt(back.transform, "hoi", 54, new Color(1, 1, 1, 0.8f), false);
            HomeSceneMenu.Fill(q.rectTransform);
            q.text = "?";
            back.gameObject.SetActive(false);
            face.gameObject.SetActive(false);
            return new BlackjackScene.Card { root = face.gameObject, face = face, suit = suit, back = back, rank = rank };
        }

        static void BuildBlackjack(UiAssets assets, ArtLibrary art, BlackjackScene scene, RectTransform page)
        {
            var outline = Theme.Outlined(Theme.Bold, 0.3f);
            var dealerTotal = Txt(page, "dealer_tong", 30, Color.white);
            At(dealerTotal.rectTransform, Top, new Vector2(0, ContentY), new Vector2(W, 40), Top);
            var dealerRow = N(page, "dealer");
            At(dealerRow, Top, new Vector2(0, ContentY - 44), new Vector2(W, 150), Top);
            var dealer = new BlackjackScene.Card[8];
            for (int i = 0; i < dealer.Length; i++) dealer[i] = Card(dealerRow, "la_" + i, new Vector2(40 + i * 122, 0), art);
            var banner = Txt(page, "ket_qua", 46, Theme.Yellow);
            At(banner.rectTransform, Top, new Vector2(0, ContentY - 206), new Vector2(W, 60), Top);
            if (outline) banner.fontSharedMaterial = outline;
            var hands = new BlackjackScene.HandUi[2];
            for (int h = 0; h < 2; h++)
            {
                var frame = Img(page, "tay_" + h, Sketch.PanelThin, new Color(1, 1, 1, 0.25f), false, true);
                At(frame.rectTransform, Top, new Vector2(0, ContentY - 276 - h * 262), new Vector2(W, 250), Top);
                var total = Txt(frame.transform, "tong", 26, Color.white);
                total.alignment = TextAlignmentOptions.MidlineLeft;
                At(total.rectTransform, new Vector2(0, 1), new Vector2(30, -8), new Vector2(700, 38), new Vector2(0, 1));
                var result = Txt(frame.transform, "ket_qua", 34, Theme.GreenD);
                result.alignment = TextAlignmentOptions.MidlineRight;
                At(result.rectTransform, new Vector2(1, 1), new Vector2(-30, -6), new Vector2(300, 42), new Vector2(1, 1));
                if (outline) result.fontSharedMaterial = outline;
                var cards = new BlackjackScene.Card[8];
                for (int i = 0; i < cards.Length; i++) cards[i] = Card(frame.transform, "la_" + i, new Vector2(30 + i * 122, -52), art);
                hands[h] = new BlackjackScene.HandUi { root = frame.gameObject, frame = frame, cards = cards, total = total, result = result };
            }
            var hint = Txt(page, "goi_y", 30, Theme.Yellow);
            At(hint.rectTransform, Top, new Vector2(0, ContentY - 810), new Vector2(W, 44), Top);
            if (outline) hint.fontSharedMaterial = outline;
            var deal = Btn(assets, page, "chia_bai", "?", BtnColor.Green, Bottom, new Vector2(0, 40), new Vector2(580, 130));
            float[] xs = { -390, -130, 130, 390 };
            var hit = Btn(assets, page, "rut", "?", BtnColor.Green, Bottom, new Vector2(xs[0], 40), new Vector2(245, 120));
            var stand = Btn(assets, page, "dan", "?", BtnColor.Red, Bottom, new Vector2(xs[1], 40), new Vector2(245, 120));
            var dbl = Btn(assets, page, "gap_doi", "?", BtnColor.Yellow, Bottom, new Vector2(xs[2], 40), new Vector2(245, 120));
            var split = Btn(assets, page, "tach", "?", BtnColor.Blue, Bottom, new Vector2(xs[3], 40), new Vector2(245, 120));
            var hintBtn = Btn(assets, page, "bat_goi_y", "?", BtnColor.Paper, new Vector2(0, 0), new Vector2(30, 190), new Vector2(280, 84));
            ((RectTransform)hintBtn.transform).pivot = new Vector2(0, 0);
            scene.Setup(dealer, dealerTotal, hands, hint, banner, deal, hit, stand, dbl, split, hintBtn);
        }

        // ---------- Roulette ----------

        static void BuildRoulette(UiAssets assets, ArtLibrary art, RouletteScene scene, RectTransform page)
        {
            var outline = Theme.Outlined(Theme.Bold, 0.3f);
            var wheelBg = Img(page, "banh_xe", Sketch.Round, Theme.Hex("#c99a64"));
            var wheel = wheelBg.rectTransform;
            At(wheel, Top, new Vector2(0, ContentY - 4), new Vector2(560, 560), Top);
            var inner = Img(wheel, "long", Sketch.Round, Theme.Hex("#e9d3a8"));
            At(inner.rectTransform, Mid, Vector2.zero, new Vector2(300, 300), Mid);
            var pockets = new RouletteScene.Pocket[Roulette.Pockets];
            for (int i = 0; i < pockets.Length; i++)
            {
                float a = RouletteScene.AngleOf(i) * Mathf.Deg2Rad;
                var pos = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * 238;
                bool starP = i == Roulette.StarPocket;
                var col = starP ? Theme.Yellow : Color.Lerp(Theme.Of(Roulette.ElemOf(i)), Color.white, 0.15f);
                var dot = Img(wheel, "o_" + i, Sketch.Dot, col, true);
                At(dot.rectTransform, Mid, pos, new Vector2(60, 60), Mid);
                var btn = dot.gameObject.AddComponent<Button>();
                btn.transition = Selectable.Transition.None;
                var num = Txt(dot.transform, "so", 28, starP ? Theme.Ink : Color.white, false);
                HomeSceneMenu.Fill(num.rectTransform);
                num.text = starP ? "" : Roulette.NumOf(i).ToString(); // phông không có ★: ô Sao Vàng vẽ hình sao
                if (starP)
                {
                    var st = Img(dot.transform, "sao", Sketch.Star, Theme.Ink);
                    At(st.rectTransform, Mid, Vector2.zero, new Vector2(40, 40), Mid);
                }
                if (outline && !starP) num.fontSharedMaterial = outline;
                var chips = Txt(dot.transform, "chip", 22, Theme.RedD, false);
                At(chips.rectTransform, Mid, new Vector2(0, 0), new Vector2(60, 30), Mid);
                chips.rectTransform.anchoredPosition = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * -44;
                if (outline) chips.fontSharedMaterial = outline;
                chips.gameObject.SetActive(false);
                pockets[i] = new RouletteScene.Pocket { button = btn, dot = dot, num = num, chips = chips };
            }
            var ball = Img(wheel, "bi", Sketch.Dot, Color.white);
            At(ball.rectTransform, Mid, new Vector2(0, 186), new Vector2(34, 34), Mid);
            var ballRing = Img(ball.transform, "vien", Sketch.Ring, Theme.Ink);
            HomeSceneMenu.Fill(ballRing.rectTransform);
            var center = Txt(wheel, "o_ra", 40, Theme.Ink);
            At(center.rectTransform, Mid, Vector2.zero, new Vector2(280, 120), Mid);
            var banner = Txt(page, "ket_qua", 34, Theme.Yellow);
            At(banner.rectTransform, Top, new Vector2(0, ContentY - 574), new Vector2(W, 50), Top);
            if (outline) banner.fontSharedMaterial = outline;
            float rowY = ContentY - 634;
            RouletteScene.Spot Spot(string n, string label, Color col, float x, float y, float w)
            {
                var b = Btn(assets, page, n, label, BtnColor.Paper, Top, new Vector2(x, y), new Vector2(w, 86));
                b.SetColor(col);
                var chips = Txt(page, n + "_chip", 20, Color.white);
                At(chips.rectTransform, Top, new Vector2(x, y - 88), new Vector2(w, 26), Top);
                chips.gameObject.SetActive(false);
                return new RouletteScene.Spot { button = b, chips = chips };
            }
            var elems = new RouletteScene.Spot[5];
            for (int i = 0; i < 5; i++)
            {
                var e = Elements.All[i];
                elems[i] = Spot("he_" + Keys.Of(e), "?", Theme.Of(e), -416 + i * 208, rowY, 196);
            }
            var nums = new RouletteScene.Spot[5];
            for (int i = 0; i < 5; i++) nums[i] = Spot("so_" + (i + 1), "?", Theme.Paper, -416 + i * 208, rowY - 124, 196);
            var star = Spot("sao_vang", "?", Theme.Yellow, 0, rowY - 248, 420);
            var chipLine = Txt(page, "chip", 24, Color.white);
            At(chipLine.rectTransform, Top, new Vector2(0, rowY - 370), new Vector2(W, 36), Top);
            var clear = Btn(assets, page, "bo_chip", "?", BtnColor.Paper, Bottom, new Vector2(-350, 40), new Vector2(300, 120));
            var spin = Btn(assets, page, "quay", "?", BtnColor.Green, Bottom, new Vector2(150, 40), new Vector2(600, 130));
            scene.Setup(wheel, ball.rectTransform, pockets, center, chipLine, banner, elems, nums, star, clear, spin);
        }

        // ---------- Máy quả ----------

        static void BuildSlot(UiAssets assets, ArtLibrary art, SlotScene scene, RectTransform page)
        {
            var outline = Theme.Outlined(Theme.Bold, 0.3f);
            const float cell = 256, gap = 12, pad = 22;
            float frameW = cell * 3 + gap * 2 + pad * 2;
            var frame = Img(page, "may", Sketch.PanelThin, Theme.Hex("#b5413a"), false, true);
            At(frame.rectTransform, Top, new Vector2(0, ContentY - 4), new Vector2(frameW, frameW), Top);
            var cells = new SlotScene.Cell[9];
            for (int r = 0; r < 3; r++)
                for (int row = 0; row < 3; row++)
                {
                    var c = Img(frame.transform, $"o_{r}_{row}", Sketch.PanelThin, Theme.Paper, false, true);
                    At(c.rectTransform, new Vector2(0, 1), new Vector2(pad + r * (cell + gap), -pad - row * (cell + gap)), new Vector2(cell, cell), new Vector2(0, 1));
                    var icon = Img(c.transform, "hinh", art ? art.Icon("star") : null, Color.white);
                    icon.preserveAspect = true;
                    At(icon.rectTransform, Mid, new Vector2(0, 12), new Vector2(160, 160), Mid);
                    var label = Txt(c.transform, "chu", 24, Theme.Ink);
                    At(label.rectTransform, Bottom, new Vector2(0, 10), new Vector2(cell - 20, 32), Bottom);
                    cells[r * 3 + row] = new SlotScene.Cell { frame = c, icon = icon, label = label };
                }
            var banner = Txt(page, "ket_qua", 36, Theme.Yellow);
            At(banner.rectTransform, Top, new Vector2(0, ContentY - frameW - 14), new Vector2(W, 50), Top);
            if (outline) banner.fontSharedMaterial = outline;
            var lines = Txt(page, "duong", 26, Color.white);
            At(lines.rectTransform, Top, new Vector2(0, ContentY - frameW - 70), new Vector2(W, 110), Top);
            var quick = Btn(assets, page, "quay_nhanh", "?", BtnColor.Paper, Bottom, new Vector2(-350, 40), new Vector2(300, 120));
            var spin = Btn(assets, page, "quay", "?", BtnColor.Green, Bottom, new Vector2(150, 40), new Vector2(600, 130));
            var pays = Btn(assets, page, "bang_tra", "?", BtnColor.Paper, new Vector2(0, 0), new Vector2(30, 190), new Vector2(280, 84));
            ((RectTransform)pays.transform).pivot = new Vector2(0, 0);
            scene.Setup(cells, lines, banner, spin, quick, pays);
        }

        static void MakeScene(string id)
        {
            string scenePath = ScenePath(id), screenPath = ScreenPath(id);
            if (!File.Exists(scenePath))
            {
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
                var prev = SceneManager.GetActiveScene();
                SceneManager.SetActiveScene(scene);
                ((GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(screenPath))).name = id;
                SceneManager.SetActiveScene(prev);
                EditorSceneManager.SaveScene(scene, scenePath);
                EditorSceneManager.CloseScene(scene, true);
            }
            else
            {
                var scene = EditorSceneManager.OpenScene(scenePath, OpenSceneMode.Additive);
                foreach (var go in scene.GetRootGameObjects())
                    if (PrefabUtility.IsPartOfPrefabInstance(go))
                        PrefabUtility.RevertPrefabInstance(PrefabUtility.GetOutermostPrefabInstanceRoot(go), InteractionMode.AutomatedAction);
                EditorSceneManager.SaveScene(scene);
                EditorSceneManager.CloseScene(scene, true);
            }
            var list = EditorBuildSettings.scenes.ToList();
            if (list.All(x => x.path != scenePath))
            {
                list.Add(new EditorBuildSettingsScene(scenePath, true));
                EditorBuildSettings.scenes = list.ToArray();
            }
        }

        // ---------- chụp thử ----------

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_leu");

        static IEnumerator Go(string id)
        {
            App.Router.Go(id, id);
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(1.0f);
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(ShotDir);
            foreach (var f in Directory.GetFiles(ShotDir, "*.jpg")) File.Delete(f);
            var cfg = App.Data.Cfg.casino;
            var added = new List<CasinoEvent>();
            try
            {
                var s = App.Save.Data;
                var d = App.Data;
                s.level = Mathf.Max(s.level, 60);
                s.balls = Mathf.Max(s.balls, 20000);
                Casino.Of(s).intro = true;
                // ép ba lều mở hôm nay (chỉ trong bộ nhớ, ngày cố định đè vòng lặp)
                string today = DateTime.Now.ToString("yyyy-MM-dd");
                foreach (var (booth, name) in new[] { (Casino.Blackjack, "Đêm Bài"), (Casino.Roulette, "Vòng Xoay Ngũ Hành"), (Casino.Slot, "Hội Máy Quả") })
                {
                    var e = new CasinoEvent { id = "tour_" + booth, name = name, booth = booth, start = today, end = today };
                    cfg.events.Add(e);
                    added.Add(e);
                }
                // Blackjack: lần đầu hiện Cách chơi, ván đầu miễn phí, rồi một ván có cược
                yield return Go(SceneIds.CasinoBlackjack);
                yield return Shot("1_bj_cach_choi");
                App.Modals.CloseAll();
                var bj = Object.FindAnyObjectByType<BlackjackScene>();
                yield return Shot("2_bj_truoc");
                for (int hand = 0; hand < 2 && bj; hand++)
                {
                    bj.PlayForTest();
                    yield return new WaitForSecondsRealtime(0.4f);
                    if (bj.GameNow != null && bj.GameNow.phase == BjPhase.Player) yield return Shot($"3_bj_van_{hand}");
                    int guard = 0;
                    while (bj.GameNow != null && bj.GameNow.phase == BjPhase.Player && guard++ < 12)
                    {
                        bj.PlayForTest();
                        yield return new WaitForSecondsRealtime(0.2f);
                    }
                    yield return new WaitForSecondsRealtime(0.5f);
                    App.Modals.CloseAll();
                    yield return Shot($"4_bj_ket_qua_{hand}");
                }
                // Roulette
                yield return Go(SceneIds.CasinoRoulette);
                App.Modals.CloseAll();
                var rl = Object.FindAnyObjectByType<RouletteScene>();
                if (rl)
                {
                    rl.BetForTest();
                    yield return new WaitForSecondsRealtime(0.3f);
                    yield return Shot("5_rl_dat_chip");
                    rl.SpinForTest();
                    yield return new WaitForSecondsRealtime(1.0f);
                    yield return Shot("6_rl_dang_quay");
                    float t0 = Time.realtimeSinceStartup;
                    while (rl.Spinning && Time.realtimeSinceStartup - t0 < 10) yield return null;
                    yield return new WaitForSecondsRealtime(0.6f);
                    App.Modals.CloseAll();
                    yield return Shot("7_rl_ket_qua");
                }
                // Máy quả
                yield return Go(SceneIds.CasinoSlot);
                App.Modals.CloseAll();
                var sl = Object.FindAnyObjectByType<SlotScene>();
                if (sl)
                {
                    yield return Shot("8_sl_truoc");
                    for (int k = 0; k < 2; k++)
                    {
                        sl.SpinForTest();
                        yield return new WaitForSecondsRealtime(0.5f);
                        if (k == 0) yield return Shot("9_sl_dang_quay");
                        float t0 = Time.realtimeSinceStartup;
                        while (sl.Spinning && Time.realtimeSinceStartup - t0 < 30) yield return null;
                        yield return new WaitForSecondsRealtime(0.5f);
                        App.Modals.CloseAll();
                        yield return Shot($"10_sl_ket_qua_{k}");
                    }
                    var paysBtn = sl.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "bang_tra");
                    if (paysBtn)
                    {
                        paysBtn.SimulateClick();
                        yield return new WaitForSecondsRealtime(0.6f);
                        yield return Shot("11_sl_bang_tra");
                        App.Modals.CloseAll();
                    }
                }
                Debug.Log("[Thử] Xong Lều lữ khách: " + Path.GetFullPath(ShotDir));
            }
            finally
            {
                foreach (var e in added) cfg.events.Remove(e);
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
            var build = Flag("casino_tables_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                Build();
                return;
            }
            var tour = Flag("casino_tables_tour.flag");
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
            if (tourRunning && EditorApplication.timeSinceStartup - tourStart > 200)
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
