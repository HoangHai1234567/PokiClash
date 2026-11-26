// Lều Hội Máy Quả của đảo Casino (GD_Claude/29 mục 6.7, GD_Claude/31 mốc D5): dựng Screens/CasinoSlot (SlotScene) + scene.
// Menu "PokiClash/Prefab/Đảo Casino/Lều Máy Quả: dựng scene" (chạy lại được; menu dựng 3 lều của CasinoTablesMenu gọi Build() ở đây).
// Phần chung (bản gọn: nút thông tin + bảng gập) do CasinoTablesMenu.Make / Common dựng.
// Sân khấu 1080 x 1920 dưới Canvas/Nen, mọi vật neo mép trên giữa (x từ giữa, y xuống dưới), số đo ở ArtGen/Casino/may_qua/bo_cuc.json:
//   nền Leu/sl_nen.jpg 1144 x 2048 hiện rộng 1080 (0,944 lần), mép trên ở y 0; mép quầy (đường thẳng ngang trên ảnh) ở y 1137;
//   Lão Mực: rig tỉ lệ 0,60, gốc (350, 1437), lớp thân nằm trong khung cắt y 0..1137 (chân khuất sau quầy), lớp tay vẽ trên cùng;
//   máy quả "Háu Ăn": rig Assets/03 Art/Casino/MayQua/may_qua.bytes tỉ lệ 0,90, gốc (−160, 1452) (trên thảm đỏ; màn 1:2 chỉ thấy x ±480 nên cả máy lẫn Lão Mực nằm gọn trong đó);
//   ô cuộn (SlotReels): con của lớp vẽ máy, lòng ba cuộn theo px ảnh rig (ArtGen/Casino/may_qua/atom/geo.json "reel").
// ĐỔI tỉ lệ / chỗ đặt hai rig thì sửa bo_cuc.json và nướng lại clip sl_pull của Lão Mực (tay bám núm cần theo bố cục này).
// Cờ Temp/casino_sl_build.flag (dựng), Temp/casino_sl_tour.flag (vào Play, ép lều mở hôm nay trong bộ nhớ, quay thử trượt / trúng /
// jackpot bằng hạt giống dò trước, chụp Temp/PokiShots/casino_sl/; bản lưu sao lưu, trả lại).
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class CasinoSlotMenu
    {
        const string LeuDir = "Assets/03 Art/Casino/Leu/";
        const string DealerRigPath = "Assets/03 Art/Casino/Dealer/lao_muc.bytes";
        const string MachineRigPath = "Assets/03 Art/Casino/MayQua/may_qua.bytes";
        // = ArtGen/Casino/may_qua/bo_cuc.json
        const float NenK = 1080f / 1144f, QuayY = 1137;
        const float MayX = -160, MayY = 1452, MayS = 0.90f;
        const float DealerX = 350, DealerY = 1437, DealerS = 0.60f;
        // lòng ba cuộn trên ảnh rig 1024 x 1536 (px): cột (x0, x1), hàng trên / dưới
        static readonly float[,] Cols = { { 275, 418 }, { 433, 571 }, { 588, 726 } };
        const float ReelTop = 605, ReelBot = 935;
        const int BallCount = 44;

        static readonly Vector2 Top = new Vector2(0.5f, 1), Bottom = new Vector2(0.5f, 0), Mid = new Vector2(0.5f, 0.5f);

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        static RectTransform N(Transform p, string n, params Type[] t) => HomeSceneMenu.Node(p, n, t);
        static RectTransform At(RectTransform rt, Vector2 a, Vector2 pos, Vector2 size, Vector2 pivot) => HomeSceneMenu.At(rt, a, pos, size, pivot);
        static Image Img(Transform p, string n, Sprite s, Color c, bool ray = false, bool sliced = false) => HomeSceneMenu.Img(p, n, s, c, ray, sliced);
        static Sprite LeuSprite(string n) => AssetDatabase.LoadAssetAtPath<Sprite>(LeuDir + n);

        static TextMeshProUGUI Txt(Transform p, string n, float size, Color c)
        {
            var t = HomeSceneMenu.Text(p, n, size, c);
            t.enableAutoSizing = true;
            t.fontSizeMin = size * 0.6f;
            t.fontSizeMax = size;
            return t;
        }

        static SketchButton Btn(UiAssets a, Transform p, string n, BtnColor c, Vector2 anchor, Vector2 pos, Vector2 size)
        {
            var b = HomeSceneMenu.Button(a, p, n, "?", c, size);
            At((RectTransform)b.transform, anchor, pos, size, anchor);
            return b;
        }

        [MenuItem("PokiClash/Prefab/Đảo Casino/Lều Máy Quả: dựng scene", priority = 78)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var art = Load<ArtLibrary>();
            CasinoTablesMenu.Make<SlotScene>(assets, SceneIds.CasinoSlot, "#3d2452", (scene, page) => BuildSlot(assets, art, scene, page));
            AssetDatabase.SaveAssets();
        }

        static void BuildSlot(UiAssets assets, ArtLibrary art, SlotScene scene, RectTransform page)
        {
            var outline = Theme.Outlined(Theme.Bold, 0.3f);
            var nen = page.root.Find("Canvas/Nen") as RectTransform;
            var oldStage = nen.Find("san_khau");
            if (oldStage) Object.DestroyImmediate(oldStage.gameObject);
            var stage = N(nen, "san_khau");
            At(stage, Mid, Vector2.zero, new Vector2(SlotScene.StageW, SlotScene.StageH), Mid);

            var bg = Img(stage, "nen_leu", LeuSprite("sl_nen.jpg"), Color.white);
            At(bg.rectTransform, Top, Vector2.zero, new Vector2(1080, 2048 * NenK), Top);

            // Lão Mực: lớp thân trong khung cắt tới mép quầy (chân khuất sau quầy vẽ sẵn trên nền)
            var clip = N(stage, "cat_quay", typeof(RectMask2D));
            At(clip, Top, Vector2.zero, new Vector2(1080, QuayY), Top);
            var dealerPos = new Vector2(DealerX, -DealerY);
            var dBack = N(clip, "lao_muc_sau", typeof(DealerLayer));
            At(dBack, Top, dealerPos, new Vector2(1000, 1400), new Vector2(0.5f, 0));

            // máy quả: một lớp vẽ cả rig; ô cuộn là con của lớp (vẽ đè lên lòng cuộn trống của ảnh máy)
            var mLayer = N(stage, "may_qua", typeof(DealerLayer));
            At(mLayer, Top, new Vector2(MayX, -MayY), new Vector2(1000, 1400), new Vector2(0.5f, 0));
            float reelW = (Cols[2, 1] - Cols[0, 0]) * MayS, reelH = (ReelBot - ReelTop) * MayS, cellH = reelH / 3f;
            float reelCx = (Cols[0, 0] + Cols[2, 1]) / 2f;
            var root = N(mLayer, "cuon", typeof(SlotReels));
            At(root, Bottom, Vector2.zero, new Vector2(reelW, reelH), Mid);
            var wins = new Image[9];
            var cells = new Image[3 * SlotReels.Rows];
            // khung sáng ô thắng nằm DƯỚI hình (nền ô đổi vàng)
            for (int c = 0; c < 3; c++)
            {
                float w = (Cols[c, 1] - Cols[c, 0]) * MayS, x = ((Cols[c, 0] + Cols[c, 1]) / 2f - reelCx) * MayS;
                for (int row = 0; row < 3; row++)
                {
                    var win = Img(root, $"thang_{c}_{row}", Sketch.PanelThin, Theme.Yellow, false, true);
                    At(win.rectTransform, Mid, new Vector2(x, reelH / 2f - (row + 0.5f) * cellH), new Vector2(w - 8, cellH - 8), Mid);
                    win.gameObject.SetActive(false);
                    wins[c * 3 + row] = win;
                }
            }
            for (int c = 0; c < 3; c++)
            {
                float w = (Cols[c, 1] - Cols[c, 0]) * MayS, x = ((Cols[c, 0] + Cols[c, 1]) / 2f - reelCx) * MayS;
                var col = N(root, "cot_" + c, typeof(Image), typeof(Mask));
                At(col, Mid, new Vector2(x, 0), new Vector2(w, reelH), Mid);
                col.GetComponent<Image>().raycastTarget = false;
                col.GetComponent<Mask>().showMaskGraphic = false;
                for (int k = 0; k < SlotReels.Rows; k++)
                {
                    var cell = Img(col, $"o_{c}_{k}", LeuSprite("sl_bt_7.png"), Color.white);
                    cell.preserveAspect = true;
                    // ô vuông (ảnh biểu tượng vuông 200 x 200; ảnh nhoè 200 x 380 kéo dọc bằng tỉ lệ của SlotReels)
                    cell.preserveAspect = false;
                    float cs = Mathf.Min(w * 0.8f, cellH * 0.9f);
                    At(cell.rectTransform, Mid, new Vector2(0, reelH / 2f - (k - 0.5f) * cellH), new Vector2(cs, cs), Mid);
                    cells[c * SlotReels.Rows + k] = cell;
                }
            }

            var dFront = N(stage, "lao_muc_truoc", typeof(DealerLayer));
            At(dFront, Top, dealerPos, new Vector2(1000, 1400), new Vector2(0.5f, 0));

            // bi phun (hiệu ứng): pool Image, mặc định ẩn
            var fly = N(stage, "bay");
            At(fly, Top, Vector2.zero, Vector2.zero, Top);
            var balls = new Image[BallCount];
            var ballSp = art ? art.Icon("ball") : null;
            for (int i = 0; i < balls.Length; i++)
            {
                var b = Img(fly, "bi_" + i, ballSp, Color.white);
                b.preserveAspect = true;
                At(b.rectTransform, Mid, Vector2.zero, new Vector2(46, 46), Mid);
                b.gameObject.SetActive(false);
                balls[i] = b;
            }

            var machineHolder = N(stage, "may_qua_rig");
            At(machineHolder, Top, Vector2.zero, Vector2.zero, Top);
            var machine = machineHolder.gameObject.AddComponent<DealerRig>();
            machine.Setup(AssetDatabase.LoadAssetAtPath<TextAsset>(MachineRigPath), mLayer.GetComponent<DealerLayer>(), null, MayS);
            var dealerHolder = N(stage, "lao_muc");
            At(dealerHolder, Top, Vector2.zero, Vector2.zero, Top);
            var dealer = dealerHolder.gameObject.AddComponent<DealerRig>();
            dealer.Setup(AssetDatabase.LoadAssetAtPath<TextAsset>(DealerRigPath), dBack.GetComponent<DealerLayer>(), dFront.GetComponent<DealerLayer>(), DealerS);

            var symbols = Enumerable.Range(0, 9).Select(i => LeuSprite($"sl_bt_{i}.png")).ToArray();
            var blurred = Enumerable.Range(0, 9).Select(i => LeuSprite($"sl_bt_{i}_nhoe.png")).ToArray();
            root.GetComponent<SlotReels>().Setup(machine, root, cells, wins, symbols, blurred, cellH, reelH / 2f);

            // chữ trên sân khấu: kết quả + các đường thắng, dưới chân bục
            var banner = Txt(stage, "ket_qua", 44, Theme.Yellow);
            At(banner.rectTransform, Top, new Vector2(0, -1596), new Vector2(1000, 56), Mid);
            if (outline) banner.fontSharedMaterial = outline;
            var lines = Txt(stage, "duong", 26, Color.white);
            At(lines.rectTransform, Top, new Vector2(40, -1664), new Vector2(600, 76), Mid);
            if (outline) lines.fontSharedMaterial = outline;

            // bong bóng thoại của Lão Mực: trên đầu, bên phải (đầu Lão Mực ở y 600..860)
            var bubble = Img(stage, "bong_bong", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.97f), false, true);
            At(bubble.rectTransform, Top, new Vector2(316, -470), new Vector2(300, 150), Mid);   // mép phải 466: màn 1:2 cắt từ ±480
            var bubbleText = Txt(bubble.transform, "chu", 25, Theme.Ink);
            HomeSceneMenu.Fill(bubbleText.rectTransform);
            bubbleText.rectTransform.offsetMin = new Vector2(18, 10);
            bubbleText.rectTransform.offsetMax = new Vector2(-18, -10);
            bubble.gameObject.SetActive(false);

            // nút (khung an toàn, neo đáy); góc trái dưới đã có nút "thông tin" của phần chung ở (16, 184)
            var quick = Btn(assets, page, "quay_nhanh", BtnColor.Paper, Bottom, new Vector2(-350, 40), new Vector2(300, 120));
            var spin = Btn(assets, page, "quay", BtnColor.Green, Bottom, new Vector2(150, 40), new Vector2(600, 130));
            var pays = Btn(assets, page, "bang_tra", BtnColor.Paper, new Vector2(1, 0), new Vector2(-16, 184), new Vector2(214, 84));
            ((RectTransform)pays.transform).pivot = new Vector2(1, 0);
            scene.Setup(stage, fly, machine, dealer, root.GetComponent<SlotReels>(), balls, bubble.rectTransform, bubbleText, lines, banner, spin, quick, pays);
        }

        // ---------- chụp thử ----------

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_sl");

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            if (!tex) yield break;
            File.WriteAllBytes(Path.Combine(ShotDir, name + ".jpg"), tex.EncodeToJPG(84));
            Object.DestroyImmediate(tex);
        }

        // hạt giống cho lượt quay kế tiếp ra kết quả mong muốn (0 trượt, 1 trúng đường thường, 2 jackpot, 3 ba Rương, 4 hai cuộn đầu khớp)
        static uint FindSeed(SlotsConfig c, int bet, int want)
        {
            for (uint seed = 1; seed < 400000; seed++)
            {
                var sp = Slots.Round(c, bet, 0, new Rng(seed)).spins[0];
                bool jackpot = sp.badgeLines > 0 || sp.payout >= bet * 20;
                bool ok = want == 0 ? sp.payout == 0 && sp.freeWon == 0 && sp.chests < 2
                    : want == 1 ? sp.payout > 0 && !jackpot && sp.freeWon == 0 && sp.lines.Count == 1
                    : want == 2 ? jackpot && sp.freeWon == 0
                    : sp.freeWon > 0;
                if (ok) return seed;
            }
            return 1;
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(ShotDir);
            foreach (var f in Directory.GetFiles(ShotDir, "*.jpg")) File.Delete(f);
            var cfg = App.Data.Cfg.casino;
            CasinoEvent added = null;
            try
            {
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 60);
                s.balls = Mathf.Max(s.balls, 50000);
                Casino.Of(s).intro = true;
                Casino.MarkSeen(s, "howto:" + Casino.Slot);
                Casino.MarkSeen(s, "free:" + Casino.Slot);
                string today = DateTime.Now.ToString("yyyy-MM-dd");
                added = new CasinoEvent { id = "tour_" + Casino.Slot, name = "Hội Máy Quả", booth = Casino.Slot, start = today, end = today };
                cfg.events.Add(added);
                App.Router.Go(SceneIds.CasinoSlot, SceneIds.CasinoSlot);
                float t0 = Time.realtimeSinceStartup;
                while ((App.Router.Busy || App.Router.Current != SceneIds.CasinoSlot) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                yield return new WaitForSecondsRealtime(0.5f);
                App.Modals.CloseAll();
                yield return Shot("00_vao_leu");
                yield return new WaitForSecondsRealtime(2.2f);
                App.Modals.CloseAll();
                yield return Shot("01_cho");
                var sl = Object.FindAnyObjectByType<SlotScene>();
                if (!sl) { Debug.LogError("[Thử] Không thấy SlotScene"); yield break; }
                int bet = Casino.Bet(s, App.Data, cfg.slots, 0);
                string[] names = { "truot", "trung", "jackpot", "ruong" };
                // mốc chụp (giây sau khi bấm Quay): với tay, giật cần, cuộn chạy, cuộn 1 dừng, cuộn 3 dừng, rồi kết quả
                float[][] marks =
                {
                    new[] { 0.28f, 0.47f, 0.56f, 0.66f, 0.9f, 1.25f, 1.36f, 1.8f, 2.3f, 2.9f, 3.5f },
                    new[] { 0.36f, 1.0f, 1.7f, 3.0f, 3.2f, 3.55f, 4.15f },
                    new[] { 0.44f, 2.0f, 3.3f, 3.8f, 4.1f, 4.3f, 4.55f, 4.9f, 5.3f, 5.9f, 6.7f },
                    new[] { 1.0f, 2.5f, 3.2f, 3.7f, 4.7f },
                };
                for (int k = 0; k < names.Length; k++)
                {
                    sl.SeedForTest(FindSeed(cfg.slots, bet, k));
                    sl.SpinForTest();
                    float start = Time.time;
                    for (int m = 0; m < marks[k].Length; m++)
                    {
                        while (Time.time - start < marks[k][m]) yield return null;
                        yield return Shot($"{k + 1}{m:00}_{names[k]}_{marks[k][m]:0.00}".Replace(',', '.'));
                    }
                    float tw = Time.realtimeSinceStartup;
                    while (sl.Spinning && Time.realtimeSinceStartup - tw < 40) yield return null;
                    yield return new WaitForSecondsRealtime(0.6f);
                    App.Modals.CloseAll();
                    yield return Shot($"{k + 1}99_{names[k]}_xong");
                    yield return new WaitForSecondsRealtime(0.8f);
                }
                var info = sl.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "thong_tin");
                if (info)
                {
                    info.SimulateClick();
                    yield return new WaitForSecondsRealtime(0.5f);
                    yield return Shot("900_thong_tin");
                    info.SimulateClick();
                }
                var paysBtn = sl.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(b => b.name == "bang_tra");
                if (paysBtn)
                {
                    paysBtn.SimulateClick();
                    yield return new WaitForSecondsRealtime(0.6f);
                    yield return Shot("901_bang_tra");
                    App.Modals.CloseAll();
                }
                Debug.Log("[Thử] Xong lều Máy Quả: " + Path.GetFullPath(ShotDir));
            }
            finally
            {
                if (added != null) cfg.events.Remove(added);
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
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
            var build = Flag("casino_sl_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                Build();
                return;
            }
            var tour = Flag("casino_sl_tour.flag");
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
            if (tourRunning && EditorApplication.timeSinceStartup - tourStart > 240)
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
