// Ba scene lều lữ khách của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.6–6.7, mốc C7; mỗi trò một scene): CasinoBlackjack (BlackjackScene),
// CasinoRoulette (RouletteScene), CasinoSlot (SlotScene). Menu "PokiClash/Prefab/Đảo Casino/Lều lữ khách: dựng 3 scene" (chạy lại được):
// Screens/<tên> (lần đầu chép từ Screens/Cave, thay bằng scene của lều), scene + Build Settings. Phần chung (CasinoTableScene) bản gọn:
// nút gập góc trái dưới + bảng giấy gập chứa hàng 4 bậc cược, tờ tin (sự kiện, khách mời, hôm nay đã cược / đã thắng, chế độ), Hũ bàn
// (Kit/bar), nút Cách chơi (Đêm Bài thêm nút Gợi ý).
// - Blackjack: hàng 8 lá dealer, 2 tay người chơi (8 lá mỗi tay, tổng, kết quả), dòng kết quả lớn, gợi ý, Chia bài / Rút / Dằn / Gấp đôi / Tách.
// - Roulette: sân khấu có Lão Mực (GD_Claude/31 mốc D4): bảng cược nỉ 6 x 6 (Sao Vàng, 5 cửa Số, 5 cửa Hệ, 25 ô đơn), 8 chip, bánh xe
//   (lòng chảo, mâm xoay, trục, viên bi, nửa vành gần), Bỏ chip, Quay.
// - Máy quả: khung 3 × 3 ô, dòng đường thắng, Quay, Quay nhanh, Bảng trả.
// Nền tạm màu, lá bài / bánh xe / máy vẽ bằng ô giấy + icon (C8 thay hình thật, diễn để sau).
// Cờ Temp/casino_tables_build.flag (dựng), Temp/casino_tables_tour.flag (vào Play, ép ba lều mở hôm nay trong bộ nhớ, chơi thử mỗi lều,
// chụp Temp/PokiShots/casino_leu/; bản lưu sao lưu, trả lại). Riêng Đêm Bài: Temp/casino_bj_build.flag (dựng), Temp/casino_bj_shots.flag (chụp).
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
            // Máy Quả dựng bằng menu riêng (Editor/CasinoSlotMenu.cs, mốc D5); gọi theo tên để file này không phụ thuộc file đó
            Type.GetType("PokiClash.EditorTools.CasinoSlotMenu")?.GetMethod("Build", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static)?.Invoke(null, null);
            AssetDatabase.SaveAssets();
        }

        static string ScreenPath(string id) => $"Assets/04 Prefabs/Screens/{id}.prefab";
        static string ScenePath(string id) => $"Assets/00 Scenes/{id}.unity";

        internal static void Make<T>(UiAssets assets, string id, string bg, Action<T, RectTransform> body) where T : CasinoTableScene
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

        // phần chung: cả ba lều dùng BẢN GỌN (CommonCompact): một nút gập góc trái dưới + bảng giấy gập
        // (Vòng Xoay, Máy Quả trước; Đêm Bài theo, người dùng 2026-11-26: "cho tất cả vào 1 cái toggle bên trái dưới người chơi")
        static void Common(UiAssets assets, CasinoTableScene scene, RectTransform page) => CommonCompact(assets, scene, page);

        // Dựng RIÊNG lều Đêm Bài (không đụng prefab Vòng Xoay, Máy Quả). Cờ Temp/casino_bj_build.flag.
        [MenuItem("PokiClash/Prefab/Đảo Casino/Lều Đêm Bài: dựng riêng", priority = 78)]
        public static void BuildBlackjackOnly()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var art = Load<ArtLibrary>();
            Make<BlackjackScene>(assets, SceneIds.CasinoBlackjack, "#2f6b4a", (root, page) => BuildBlackjack(assets, art, root, page));
            AssetDatabase.SaveAssets();
        }

        // Phần chung BẢN GỌN (người dùng 2026-11-26: "mấy cái này để trong 1 cái toggle bên trái dưới thôi, không dàn ra như này"):
        // bậc cược, tờ tin (sự kiện, khách mời, hôm nay, chế độ), Hũ bàn, Cách chơi nằm trong MỘT bảng giấy gập; nút gập ở góc trái
        // dưới (Vòng Xoay: trên nút Bỏ chip; Đêm Bài: trên hàng nút, dưới tay bài người chơi) ghi mức cược đang chọn. Bảng mở đè lên góc
        // trái bàn, chọn mức cược xong tự gập. Nằm NGOÀI khối Roulette (khối đó do va_ma.py của Vòng Xoay thay nguyên khối).
        internal static void CommonCompact(UiAssets assets, CasinoTableScene scene, RectTransform page)
        {
            var paper = new Color(1f, 0.98f, 0.92f, 0.98f);
            var kit = assets.prefabs;
            var corner = new Vector2(0, 0);
            var toggle = Btn(assets, page, "thong_tin", "?", BtnColor.Paper, corner, new Vector2(16, 184), new Vector2(214, 84));
            var panel = Img(page, "bang_thong_tin", Sketch.PanelThin, paper, true, true);   // chặn chạm xuống bảng cược phía sau
            At(panel.rectTransform, corner, new Vector2(16, 280), new Vector2(560, 560), corner);
            var row = N(panel.transform, "bac_cuoc", typeof(HorizontalLayoutGroup));
            At(row, Top, new Vector2(0, -16), new Vector2(528, 72), Top);
            var hl = row.GetComponent<HorizontalLayoutGroup>();
            hl.spacing = 8; hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = false; hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            var tiers = new SketchButton[4];
            for (int i = 0; i < tiers.Length; i++) tiers[i] = HomeSceneMenu.Button(assets, row, "bac_" + i, "?", BtnColor.Paper, new Vector2(126, 70));
            var g = Txt(panel.transform, "su_kien", 24, Theme.BlueD);
            At(g.rectTransform, Top, new Vector2(0, -100), new Vector2(520, 84), Top);
            var td = Txt(panel.transform, "hom_nay", 22, Theme.Ink2);
            At(td.rectTransform, Top, new Vector2(0, -190), new Vector2(520, 70), Top);
            var md = Txt(panel.transform, "che_do", 22, Theme.GreenD);
            At(md.rectTransform, Top, new Vector2(0, -264), new Vector2(520, 60), Top);
            var jr = ((GameObject)PrefabUtility.InstantiatePrefab(kit.bar.gameObject, panel.transform)).GetComponent<UiBar>();
            jr.name = "hu_ban";
            jr.SetKind(UiBar.Kind.Shard);
            At((RectTransform)jr.transform, Top, new Vector2(0, -336), new Vector2(480, 38), Top);
            var jt = Txt(panel.transform, "hu_qua", 21, Theme.Ink2);
            At(jt.rectTransform, Top, new Vector2(0, -380), new Vector2(520, 60), Top);
            // Đêm Bài: nút bật / tắt gợi ý nằm cạnh Cách chơi trong bảng (BuildBlackjack lấy theo tên "bat_goi_y")
            bool hintSlot = scene is BlackjackScene;
            var hb = Btn(assets, panel.transform, "cach_choi", "?", BtnColor.Paper, new Vector2(0.5f, 0), new Vector2(hintSlot ? -134 : 0, 18),
                new Vector2(hintSlot ? 254 : 320, 78));
            if (hintSlot) Btn(assets, panel.transform, "bat_goi_y", "?", BtnColor.Paper, new Vector2(0.5f, 0), new Vector2(134, 18), new Vector2(254, 78));
            panel.gameObject.SetActive(false);
            scene.SetupTable(tiers, td, md, g, jr, jt, hb);
            scene.SetupInfo(toggle, panel.rectTransform);
        }

        // ---------- Blackjack: sân khấu có Lão Mực (GD_Claude/31 mục 3, mốc D3) ----------
        // Hình ở Assets/03 Art/Casino/Leu (ArtGen/Casino/dealer/d3/dua_vao_unity.py), rig Assets/03 Art/Casino/Dealer/lao_muc.bytes.
        // Sân khấu 1080 x 1920 (BlackjackScene.StageW/H) dưới Canvas/Nen, mọi vật neo mép trên giữa: ảnh nền 1144 x 2048 hiện rộng 1080
        // (0,944 lần), mép trên ở y −150 nên mép bàn sau (y 900 trong ảnh) rơi đúng y −1000; gốc rig Lão Mực ở y −(1000 + 500 x 0,79).
        const string LeuDir = "Assets/03 Art/Casino/Leu/";
        const string DealerRigPath = "Assets/03 Art/Casino/Dealer/lao_muc.bytes";
        const float NenTop = 150, NenK = 1080f / 1144f, RigScale = 0.79f, RimY = 1000;

        static Sprite LeuSprite(string n) => AssetDatabase.LoadAssetAtPath<Sprite>(LeuDir + n);

        static BlackjackScene.Card Card(Transform p, string n, Vector2 pos, ArtLibrary art)
        {
            var face = Img(p, n, LeuSprite("bj_la_mat.png") ?? Sketch.PanelThin, Color.white);
            At(face.rectTransform, Top, pos, new Vector2(108, 150), Mid);
            var rank = Txt(face.transform, "hang", 40, Theme.Ink, false);
            rank.alignment = TextAlignmentOptions.TopLeft;
            At(rank.rectTransform, new Vector2(0, 1), new Vector2(12, -8), new Vector2(80, 50), new Vector2(0, 1));
            var suit = Img(face.transform, "chat", art ? art.Icon("e_kim") : null, Color.white);
            suit.preserveAspect = true;
            At(suit.rectTransform, Mid, new Vector2(6, -14), new Vector2(62, 62), Mid);
            var back = Img(face.transform, "lung", LeuSprite("bj_la_lung.png") ?? Sketch.PanelThin, Color.white);
            HomeSceneMenu.Fill(back.rectTransform);
            back.gameObject.SetActive(false);
            face.gameObject.SetActive(false);
            return new BlackjackScene.Card { root = face.rectTransform, face = face, suit = suit, back = back, rank = rank };
        }

        static BlackjackScene.Stack ChipStack(Transform p, string n, string sprite, Color label)
        {
            var root = N(p, n, typeof(CanvasGroup));
            At(root, Top, BlackjackScene.BetSpot, new Vector2(76, 90), Mid);
            var img = Img(root, "chong", LeuSprite(sprite), Color.white);
            img.preserveAspect = true;
            HomeSceneMenu.Fill(img.rectTransform);
            // nhãn số bi bên TRÁI chồng chip (chồng chip thắng đặt bên phải chồng cược)
            var t = Txt(root, "so", 24, label);
            t.alignment = TextAlignmentOptions.MidlineRight;
            At(t.rectTransform, new Vector2(0, 0.5f), new Vector2(-8, 0), new Vector2(170, 36), new Vector2(1, 0.5f));
            var outline = Theme.Outlined(Theme.Bold, 0.3f);
            if (outline) t.fontSharedMaterial = outline;
            root.gameObject.SetActive(false);
            return new BlackjackScene.Stack { root = root, img = img, label = t };
        }

        static void BuildBlackjack(UiAssets assets, ArtLibrary art, BlackjackScene scene, RectTransform page)
        {
            var outline = Theme.Outlined(Theme.Bold, 0.3f);
            // nền màn (dưới cả sân khấu): màu sọc lều phía trên ảnh (sau thanh trên)
            var nen = page.root.Find("Canvas/Nen") as RectTransform;
            var oldStage = nen.Find("san_khau");
            if (oldStage) Object.DestroyImmediate(oldStage.gameObject);
            if (nen.Find("nen_hai_ben")?.GetComponent<Image>() is Image si) si.color = Theme.Hex("#2c7a45");
            var stage = N(nen, "san_khau");
            At(stage, Mid, Vector2.zero, new Vector2(BlackjackScene.StageW, BlackjackScene.StageH), Mid);

            var nenSp = LeuSprite("bj_nen.jpg");
            var bg = Img(stage, "nen_leu", nenSp, Color.white);
            At(bg.rectTransform, Top, new Vector2(0, -NenTop), new Vector2(1080, 2048 * NenK), Top);

            // Lão Mực: lớp sau (thân, mặt) rồi mặt bàn, đồ trên bàn, lớp trước (tay)
            var rigHolder = N(stage, "lao_muc");
            At(rigHolder, Top, Vector2.zero, Vector2.zero, Top);
            var rigPos = new Vector2(0, -(RimY + DealerRig.TableY * RigScale));
            DealerLayer Layer(string n)
            {
                var rt = N(stage, n, typeof(DealerLayer));
                At(rt, Top, rigPos, new Vector2(1000, 1400), new Vector2(0.5f, 0));
                return rt.GetComponent<DealerLayer>();
            }
            var back = Layer("lao_muc_sau");

            var banSp = LeuSprite("bj_ban.png");
            var ban = Img(stage, "ban", banSp, Color.white);
            float banTop = 840; // = BAN_TOP của dua_vao_unity.py (px ảnh 2k)
            At(ban.rectTransform, Top, new Vector2(0, -(NenTop + banTop * NenK)), new Vector2(1080, (2048 - banTop) * NenK), Top);

            var deck = Img(stage, "co_bai", LeuSprite("bj_co_bai.png"), Color.white);
            deck.preserveAspect = true;
            At(deck.rectTransform, Top, new Vector2(330, -1092), new Vector2(104, 112), Mid);

            var dealer = new BlackjackScene.Card[8];
            for (int i = 0; i < dealer.Length; i++) dealer[i] = Card(stage, "la_d_" + i, BlackjackScene.DealerRow, art);

            var bet = ChipStack(stage, "chong_cuoc", "bj_chong_do.png", Color.white);
            var win = ChipStack(stage, "chong_thang", "bj_chong_xanh.png", Theme.Yellow);

            var hands = new BlackjackScene.HandUi[2];
            for (int h = 0; h < 2; h++)
            {
                var hr = N(stage, "tay_" + h);
                At(hr, Top, new Vector2(0, BlackjackScene.HandY), Vector2.zero, Mid);
                var cards = new BlackjackScene.Card[8];
                for (int i = 0; i < cards.Length; i++) cards[i] = Card(stage, $"la_{h}_{i}", new Vector2(0, BlackjackScene.HandY), art);
                var marker = Img(stage, "dang_choi_" + h, Sketch.Dot, Theme.Yellow);
                At(marker.rectTransform, Top, new Vector2(0, BlackjackScene.HandY - 104), new Vector2(22, 22), Mid);
                marker.gameObject.SetActive(false);
                hands[h] = new BlackjackScene.HandUi { root = hr, cards = cards, marker = marker };
            }

            var front = Layer("lao_muc_truoc");
            var fly = N(stage, "bay");
            At(fly, Top, Vector2.zero, Vector2.zero, Top);

            var rig = rigHolder.gameObject.AddComponent<DealerRig>();
            rig.Setup(AssetDatabase.LoadAssetAtPath<TextAsset>(DealerRigPath), back, front, RigScale);

            // chữ trên bàn
            var dealerTotal = Txt(stage, "dealer_tong", 28, Color.white);
            At(dealerTotal.rectTransform, Top, new Vector2(-370, BlackjackScene.DealerRow.y), new Vector2(240, 40), Mid);
            if (outline) dealerTotal.fontSharedMaterial = outline;
            var banner = Txt(stage, "ket_qua", 46, Theme.Yellow);
            At(banner.rectTransform, Top, new Vector2(0, -1226), new Vector2(W, 56), Mid);
            if (outline) banner.fontSharedMaterial = outline;
            for (int h = 0; h < 2; h++)
            {
                var total = Txt(stage, "tong_" + h, 26, Color.white);
                At(total.rectTransform, Top, new Vector2(0, BlackjackScene.HandY - 96), new Vector2(460, 36), Mid);
                var result = Txt(stage, "ket_qua_" + h, 32, Theme.Yellow);
                At(result.rectTransform, Top, new Vector2(0, BlackjackScene.HandY + 92), new Vector2(360, 40), Mid);
                if (outline)
                {
                    total.fontSharedMaterial = outline;
                    result.fontSharedMaterial = outline;
                }
                hands[h].total = total;
                hands[h].result = result;
            }
            var hint = Txt(stage, "goi_y", 30, Theme.Yellow);
            At(hint.rectTransform, Top, new Vector2(0, -1648), new Vector2(W, 44), Mid);
            if (outline) hint.fontSharedMaterial = outline;

            // bong bóng thoại của Lão Mực: bên phải đầu, KHÔNG đè mặt (đầu chiếm x −170..+190 của sân khấu; bản đầu đặt x 300 rộng 420 che
            // mất mắt phải và giọt mồ hôi bên đó)
            var bubble = Img(stage, "bong_bong", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.97f), false, true);
            At(bubble.rectTransform, Top, new Vector2(328, -610), new Vector2(300, 140), Mid);   // mép phải 478: màn 1:2 (sân khấu ×1,125) cắt từ ±480
            var bubbleText = Txt(bubble.transform, "chu", 26, Theme.Ink);
            HomeSceneMenu.Fill(bubbleText.rectTransform);
            bubbleText.rectTransform.offsetMin = new Vector2(18, 10);
            bubbleText.rectTransform.offsetMax = new Vector2(-18, -10);
            bubble.gameObject.SetActive(false);

            // nút (khung an toàn, neo đáy)
            var deal = Btn(assets, page, "chia_bai", "?", BtnColor.Green, Bottom, new Vector2(0, 40), new Vector2(580, 130));
            float[] xs = { -390, -130, 130, 390 };
            var hit = Btn(assets, page, "rut", "?", BtnColor.Green, Bottom, new Vector2(xs[0], 40), new Vector2(245, 120));
            var stand = Btn(assets, page, "dan", "?", BtnColor.Red, Bottom, new Vector2(xs[1], 40), new Vector2(245, 120));
            var dbl = Btn(assets, page, "gap_doi", "?", BtnColor.Yellow, Bottom, new Vector2(xs[2], 40), new Vector2(245, 120));
            var split = Btn(assets, page, "tach", "?", BtnColor.Blue, Bottom, new Vector2(xs[3], 40), new Vector2(245, 120));
            var hintBtn = page.Find("bang_thong_tin/bat_goi_y")?.GetComponent<SketchButton>();   // dựng trong bảng gập (CommonCompact)
            scene.Setup(stage, fly, rig, deck.rectTransform, dealer, dealerTotal, hands, bet, win, bubble.rectTransform, bubbleText, hint, banner,
                deal, hit, stand, dbl, split, hintBtn,
                new[] { LeuSprite("bj_chong_do.png"), LeuSprite("bj_chong_xanh.png"), LeuSprite("bj_chong_la.png"), LeuSprite("bj_chong_vang.png") });
        }

        // ---------- Roulette: sân khấu có Lão Mực + bánh xe (GD_Claude/31 mốc D4) ----------
        // Hình ở Assets/03 Art/Casino/Leu/rl_* (ArtGen/Casino/dealer/d4/dua_vao_unity.py; bánh xe vẽ bằng mã ve_banh_xe.py, khớp hình học
        // của mô phỏng viên bi Core/Casino/RouletteBall.cs). Sân khấu 1080 x 1920 (RouletteScene.StageW/H) dưới Canvas/Nen, mọi vật neo
        // mép trên giữa: ảnh nền 1144 x 2048 hiện đúng cỡ (thừa 32 px mỗi bên), mép trên ở y +105 nên hàng 755 của ảnh (mép bàn, giữa
        // khay chip) rơi vào y −650; Lão Mực tỉ lệ 0,70, gốc rig ở y −(650 + 500 x 0,7). Bảng cược y −775..−1250, bánh xe tâm (0, −1500).
        const float RlNenTop = 105, RlBanTop = 680;
        // cỡ và tâm các hình bánh xe (px ảnh, ảnh gấp đôi cỡ hiện): xem Leu/rl_banh_xe.json
        static readonly Vector2 RlChao = new Vector2(1312, 894), RlChaoTam = new Vector2(656, 443.52f), RlTruc = new Vector2(192, 217),
            RlTrucDe = new Vector2(96, 172.7f);
        const float RlMam = 904, RlBi = 62;

        static RouletteScene.Cell RlCell(Transform p, string n, Vector2 pos, Color col, string text, float textSize, Color textCol, Sprite icon,
            Color iconCol, Material outline)
        {
            var frame = Img(p, n, Sketch.PanelThin, col, true, true);
            At(frame.rectTransform, Top, pos, new Vector2(RouletteScene.CellW - 6, (n.StartsWith("so_") || n == "sao_vang" ? RouletteScene.HeadH : RouletteScene.CellH) - 6), Mid);
            if (n.StartsWith("he_") || n == "sao_vang") frame.rectTransform.sizeDelta = new Vector2(RouletteScene.HeadW - 6, frame.rectTransform.sizeDelta.y);
            var btn = frame.gameObject.AddComponent<Button>();
            btn.transition = Selectable.Transition.None;
            btn.targetGraphic = frame;
            if (icon)
            {
                var ic = Img(frame.transform, "hinh", icon, iconCol);
                ic.preserveAspect = true;
                At(ic.rectTransform, Mid, new Vector2(-30, 0), new Vector2(48, 48), Mid);
            }
            var t = Txt(frame.transform, "chu", textSize, textCol, false);
            t.richText = true;
            At(t.rectTransform, Mid, new Vector2(icon ? 30 : 0, 0), new Vector2(icon ? 76 : RouletteScene.CellW - 16, 60), Mid);
            t.text = text ?? "";
            if (outline && textCol == Color.white) t.fontSharedMaterial = outline;
            return new RouletteScene.Cell { root = frame.rectTransform, button = btn, frame = frame, label = t, color = col };
        }

        // Dựng RIÊNG lều Vòng Xoay (không đụng prefab Đêm Bài, Máy Quả: phiên khác đang làm Máy Quả bằng menu riêng).
        // Cờ Temp/casino_rl_build.flag (CasinoRouletteTour.Poll).
        [MenuItem("PokiClash/Prefab/Đảo Casino/Lều Vòng Xoay: dựng riêng", priority = 78)]
        public static void BuildRouletteOnly()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var art = Load<ArtLibrary>();
            Make<RouletteScene>(assets, SceneIds.CasinoRoulette, "#5b3a6e", (root, page) => BuildRoulette(assets, art, root, page));
            AssetDatabase.SaveAssets();
        }

        static void BuildRoulette(UiAssets assets, ArtLibrary art, RouletteScene scene, RectTransform page)
        {
            var outline = Theme.Outlined(Theme.Bold, 0.3f);
            var nen = page.root.Find("Canvas/Nen") as RectTransform;
            var oldStage = nen.Find("san_khau");
            if (oldStage) Object.DestroyImmediate(oldStage.gameObject);
            if (nen.Find("nen_hai_ben")?.GetComponent<Image>() is Image si) si.color = Theme.Hex("#4f2a66");
            var stage = N(nen, "san_khau");
            At(stage, Mid, Vector2.zero, new Vector2(RouletteScene.StageW, RouletteScene.StageH), Mid);

            var bg = Img(stage, "nen_leu", LeuSprite("rl_nen.jpg"), Color.white);
            At(bg.rectTransform, Top, new Vector2(0, RlNenTop), new Vector2(1144, 2048), Top);

            // Lão Mực: lớp sau (thân, mặt) rồi mặt bàn, đồ trên bàn, bánh xe, lớp trước (tay)
            const float S = RouletteScene.RigScale;
            var rigHolder = N(stage, "lao_muc");
            At(rigHolder, Top, Vector2.zero, Vector2.zero, Top);
            var rigPos = new Vector2(0, -(RouletteScene.RimY + DealerRig.TableY * S));
            DealerLayer Layer(string n)
            {
                var rt = N(stage, n, typeof(DealerLayer));
                At(rt, Top, rigPos, new Vector2(1000, 1400), new Vector2(0.5f, 0));
                return rt.GetComponent<DealerLayer>();
            }
            var back = Layer("lao_muc_sau");

            var ban = Img(stage, "ban", LeuSprite("rl_ban.png"), Color.white);
            At(ban.rectTransform, Top, new Vector2(0, RlNenTop - RlBanTop), new Vector2(1144, 2048 - RlBanTop), Top);

            // bảng cược nỉ: góc Sao Vàng, hàng đầu 5 cửa Số, cột đầu 5 cửa Hệ, trong là 25 ô đơn (hàng = hệ, cột = số)
            var grid = N(stage, "bang_cuoc", typeof(CanvasGroup));
            At(grid, Top, Vector2.zero, Vector2.zero, Top);
            var star = RlCell(grid, "sao_vang", RouletteScene.CellPos(RlKind.Star, 0), Theme.Yellow, "?", 30, Theme.Ink, Sketch.Star, Theme.Ink, outline);
            var nums = new RouletteScene.Cell[5];
            for (int i = 0; i < 5; i++)
                nums[i] = RlCell(grid, "so_" + (i + 1), RouletteScene.CellPos(RlKind.Num, i + 1), Theme.Paper2, "?", 38, Theme.Ink, null, Color.white, outline);
            // người dùng 2026-11-26: "để đỏ đen thôi, nhiều màu quá": ô đơn tô ĐỎ / ĐEN đúng màu ô đó trên mâm (vị trí chẵn đỏ, lẻ đen),
            // cửa Hệ nền giấy với biểu tượng hệ tô mực; không tô theo màu hệ nữa
            Color red = Theme.Hex("#cf3b2e"), black = Theme.Hex("#2a2422");
            var elems = new RouletteScene.Cell[5];
            var singles = new RouletteScene.Cell[25];
            for (int e = 0; e < 5; e++)
            {
                var el = Elements.All[e];
                elems[e] = RlCell(grid, "he_" + Keys.Of(el), RouletteScene.CellPos(RlKind.Elem, e), Theme.Paper2, "?", 30, Theme.Ink,
                    art ? art.Icon(CasinoTableScene.ElemIcon(el)) : null, Theme.Ink, outline);
                for (int n = 0; n < 5; n++)
                {
                    int p = e * 5 + n;
                    var col = RouletteWheel.SlotOf(p) % 2 == 0 ? red : black;
                    singles[p] = RlCell(grid, $"o_{p}", RouletteScene.CellPos(RlKind.Single, p), col, (n + 1).ToString(), 40, Color.white, null, Color.white, outline);
                }
            }

            var marker = Img(stage, "danh_dau", Sketch.Star, Theme.Yellow);
            At(marker.rectTransform, Top, RouletteScene.BetSpot, new Vector2(52, 52), Mid);
            marker.gameObject.SetActive(false);

            var chips = new RouletteScene.Chip[8];
            for (int i = 0; i < chips.Length; i++)
            {
                var root = N(stage, "chip_" + i, typeof(CanvasGroup));
                At(root, Top, RouletteScene.BetSpot, new Vector2(52, 52), Mid);
                var img = Img(root, "hinh", LeuSprite("bj_chip_do.png"), Color.white);
                img.preserveAspect = true;
                HomeSceneMenu.Fill(img.rectTransform);
                root.gameObject.SetActive(false);
                chips[i] = new RouletteScene.Chip { root = root, img = img, group = root.GetComponent<CanvasGroup>() };
            }
            var winRoot = N(stage, "chong_thang", typeof(CanvasGroup));
            At(winRoot, Top, RouletteScene.WinSpot, new Vector2(76, 90), Mid);
            var winImg = Img(winRoot, "chong", LeuSprite("bj_chong_do.png"), Color.white);
            winImg.preserveAspect = true;
            HomeSceneMenu.Fill(winImg.rectTransform);
            var winText = Txt(winRoot, "so", 26, Theme.Yellow);
            winText.alignment = TextAlignmentOptions.MidlineLeft;
            At(winText.rectTransform, new Vector2(1, 0.5f), new Vector2(8, 0), new Vector2(200, 36), new Vector2(0, 0.5f));
            if (outline) winText.fontSharedMaterial = outline;
            winRoot.gameObject.SetActive(false);
            var win = new RouletteScene.Stack { root = winRoot, img = winImg, label = winText };

            // bánh xe: lòng chảo đứng yên, mâm xoay (ép dẹt theo góc nhìn), trục, viên bi, nửa vành gần đè lên bi
            var wheel = N(stage, "banh_xe");
            At(wheel, Top, RouletteScene.WheelCenter, Vector2.zero, Mid);
            float k = RouletteScene.WheelR / 640f;   // ảnh vẽ ở R = 640
            Image Part(string n, string sprite, Vector2 size, Vector2 pivotPx)
            {
                var im = Img(wheel, n, LeuSprite(sprite), Color.white);
                At(im.rectTransform, Mid, Vector2.zero, size * k, new Vector2(pivotPx.x / size.x, 1 - pivotPx.y / size.y));
                return im;
            }
            Part("chao", "rl_chao.png", RlChao, RlChaoTam);
            var squash = N(wheel, "mam_khung");
            At(squash, Mid, Vector2.zero, Vector2.zero, Mid);
            squash.localScale = new Vector3(1, RouletteWheel.TiltK, 1);
            var rotor = Img(squash, "mam", LeuSprite("rl_mam.png"), Color.white);
            At(rotor.rectTransform, Mid, Vector2.zero, new Vector2(RlMam, RlMam) * k, Mid);
            Part("truc", "rl_truc.png", RlTruc, RlTrucDe);
            var ball = Img(wheel, "bi", LeuSprite("rl_bi.png"), Color.white);
            At(ball.rectTransform, Mid, Vector2.zero, new Vector2(RlBi, RlBi) * k * 1.2f, Mid);   // bi vẽ to hơn 20 % cho dễ thấy trên điện thoại
            Part("vanh_truoc", "rl_vanh_truoc.png", RlChao, RlChaoTam);

            var front = Layer("lao_muc_truoc");
            var fly = N(stage, "bay");
            At(fly, Top, Vector2.zero, Vector2.zero, Top);
            var flyBall = Img(fly, "bi_bay", LeuSprite("rl_bi.png"), Color.white);
            At(flyBall.rectTransform, Top, Vector2.zero, new Vector2(RlBi, RlBi) * k * 1.2f, Mid);
            flyBall.gameObject.SetActive(false);

            var rig = rigHolder.gameObject.AddComponent<DealerRig>();
            rig.Setup(AssetDatabase.LoadAssetAtPath<TextAsset>(DealerRigPath), back, front, S);

            // dòng chữ trên bàn (giữa khay chip và bảng cược): hướng dẫn đặt chip, rồi ô ra + thắng thua
            var banner = Txt(stage, "ket_qua", 30, Theme.Yellow);
            At(banner.rectTransform, Top, new Vector2(0, -750), new Vector2(900, 40), Mid);
            if (outline) banner.fontSharedMaterial = outline;

            // bong bóng thoại: bên phải đầu Lão Mực, dưới bảng Hũ bàn / Cách chơi, không đè mặt (đầu chiếm x ±150, y −225..−490)
            var bubble = Img(stage, "bong_bong", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.97f), false, true);
            At(bubble.rectTransform, Top, new Vector2(326, -532), new Vector2(296, 132), Mid);   // mép phải 474: màn 1:2 cắt từ ±480
            var bubbleText = Txt(bubble.transform, "chu", 25, Theme.Ink);
            HomeSceneMenu.Fill(bubbleText.rectTransform);
            bubbleText.rectTransform.offsetMin = new Vector2(16, 8);
            bubbleText.rectTransform.offsetMax = new Vector2(-16, -8);
            bubble.gameObject.SetActive(false);

            var clear = Btn(assets, page, "bo_chip", "?", BtnColor.Paper, Bottom, new Vector2(-350, 40), new Vector2(300, 120));
            var spin = Btn(assets, page, "quay", "?", BtnColor.Green, Bottom, new Vector2(150, 40), new Vector2(600, 130));
            scene.Setup(stage, fly, rig, grid.GetComponent<CanvasGroup>(), singles, elems, nums, star, chips, win, wheel, rotor.rectTransform,
                ball.rectTransform, flyBall.rectTransform, marker.rectTransform, bubble.rectTransform, bubbleText, banner, clear, spin,
                new[] { LeuSprite("bj_chip_do.png"), LeuSprite("bj_chip_xanh.png"), LeuSprite("bj_chip_la.png"), LeuSprite("bj_chip_vang.png") },
                new[] { LeuSprite("bj_chong_do.png"), LeuSprite("bj_chong_xanh.png"), LeuSprite("bj_chong_la.png"), LeuSprite("bj_chong_vang.png") });
        }

        // ---------- Máy quả ----------
        // dựng ở Editor/CasinoSlotMenu.cs (mốc D5); BuildSlot bản ô giấy cũ đã bỏ

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

        // bjOnly: chỉ chụp lều Đêm Bài (cờ casino_bj_shots.flag)
        static IEnumerator Run(bool bjOnly)
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
                CasinoGuide.SkipAll(s); // tour: không hiện lời dẫn của Lão Mực (chặn chạm)
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
                var bjInfo = bj ? bj.GetComponentsInChildren<SketchButton>(true).FirstOrDefault(x => x.name == "thong_tin") : null;
                if (bjInfo)
                {
                    bjInfo.SimulateClick();   // mở bảng gập
                    yield return new WaitForSecondsRealtime(0.4f);
                    yield return Shot("2b_bj_thong_tin");
                    bjInfo.SimulateClick();
                    yield return new WaitForSecondsRealtime(0.2f);
                }
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
                if (bjOnly)
                {
                    Debug.Log("[Thử] Xong lều Đêm Bài: " + Path.GetFullPath(ShotDir));
                    yield break;   // finally vẫn chạy: bỏ sự kiện ép, trả bản lưu
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
            var bjBuild = Flag("casino_bj_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(bjBuild))
            {
                File.Delete(bjBuild);
                BuildBlackjackOnly();
                return;
            }
            var tour = Flag("casino_tables_tour.flag");
            var bjTour = Flag("casino_bj_shots.flag");
            if ((File.Exists(tour) || File.Exists(bjTour)) && !tourRunning)
            {
                if (!EditorApplication.isPlaying)
                {
                    if (!EditorApplication.isPlayingOrWillChangePlaymode) EditorApplication.isPlaying = true;
                    return;
                }
                Application.runInBackground = true; // Unity nằm nền thì vòng game đứng
                if (App.I == null || App.Router == null || App.Router.Busy || App.Router.Current == null) return;
                bool bjOnly = !File.Exists(tour);
                File.Delete(tour);
                File.Delete(bjTour);
                tourRunning = true;
                tourStart = EditorApplication.timeSinceStartup;
                App.I.StartCoroutine(TourThenStop(bjOnly));
                return;
            }
            if (tourRunning && EditorApplication.timeSinceStartup - tourStart > 200)
            {
                tourRunning = false;
                EditorApplication.isPlaying = false;
            }
        }

        static IEnumerator TourThenStop(bool bjOnly)
        {
            yield return new WaitForSecondsRealtime(3f);
            yield return Run(bjOnly);
            yield return new WaitForSecondsRealtime(1f);
            tourRunning = false;
            EditorApplication.isPlaying = false;
        }
    }
}
