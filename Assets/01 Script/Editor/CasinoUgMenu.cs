// Scene Hầm đấu của đảo Casino (UndergroundScene, GD_Claude/29_DaoCasino.md mục 6.5; mỗi trò một scene). Bản sàn đấu có Lão Mực
// (người dùng 2026-11-26 lượt 2). Menu "PokiClash/Prefab/Đảo Casino/Hầm đấu: dựng scene" (chạy lại được): Screens/CasinoUnderground
// (lần đầu chép từ Screens/Cave, thay bằng UndergroundScene), scene CasinoUnderground + Build Settings.
// - Sân khấu dưới Canvas/Nen (rộng 1080, neo mép trên, cao bằng ảnh nền 1144 x 2048 thu về bề ngang 1080): ảnh nền hầm đấu
//   (Assets/03 Art/Casino/HamDau/hd_nen.jpg, ArtGen/Casino/ham_dau/dua_vao_unity.py), Lão Mực (DealerRig: lớp sau, lớp quầy hd_quay.png
//   cắt từ nền, lớp trước), chữ tên bậc trên biển gỗ, đội ngầm (3 chỗ đứng), vùng vuốt, hai mũi tên, thẻ số tướng + lực chiến, thẻ luật
//   ngày, hàng chip bậc, bong bóng thoại. Số đo trên ảnh (px ảnh 2k) chép từ ham_dau.json, nhân K ra đơn vị sân khấu.
// - Khung an toàn: thẻ đồng hồ đổi đội (trên trái), dải đáy (đội của mình, Đổi đội, Đánh).
// Phần màn dài hơn ảnh tô màu đáy ảnh (bóng khán giả). Dựng xong xoá hộp cũ Dialogs/HamDau, gỡ ô trống khỏi UiKit.dialogs.
// Cờ Temp/casino_ug_build.flag (dựng), Temp/casino_ug_tour.flag (vào Play, mở Hầm đấu, chụp từng bậc + lời Lão Mực, hộp chi tiết, bậc
// đã thắng, vào trận, về lại sau trận; bản lưu sao lưu, trả lại). Ảnh Temp/PokiShots/casino_ham/.
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
    public static class CasinoUgMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/CasinoUnderground.prefab";
        const string BaseScreenPath = "Assets/04 Prefabs/Screens/Cave.prefab";
        const string ScenePath = "Assets/00 Scenes/CasinoUnderground.unity";
        const string OldDialogPath = "Assets/04 Prefabs/Dialogs/HamDau.prefab";
        const string PickerPath = "Assets/04 Prefabs/Dialogs/ChonDoi.prefab";
        const string ArtDir = "Assets/03 Art/Casino/HamDau/";
        const string DealerRigPath = "Assets/03 Art/Casino/Dealer/lao_muc.bytes";

        // số đo trên ảnh nền 2k (ham_dau.json): mép trên quầy, tâm lòng quầy, lớp quầy, biển gỗ
        const float ImgW = 1144, ImgH = 2048, K = 1080f / ImgW;
        const float RimPx = 693, OpeningCx = 568.5f, CoverX0 = 330, CoverX1 = 814, CoverY1 = 940;
        const float SignX0 = 392, SignY0 = 835, SignX1 = 748, SignY1 = 928;
        const string BottomHex = "#302338";
        const float RigScale = 0.38f; // phần Lão Mực trên mép quầy (~900 px rig) vừa lòng quầy cao ~344
        // sân khấu (đơn vị canvas, gốc mép trên giữa, y âm xuống)
        const float PitTop = 990, PitH = 620, InfoY = 1502, RuleY = 1560, ChipY = 1626, ArrowY = 1280, ArrowX = 478;
        const int Chips = 11, Faces = 3; // 10 bậc thường + Nhà Vô Địch
        // biên độ nhún lớn nhất (đơn vị canvas) của khán giả hàng đầu / trên khán đài (PitCrowd)
        const float CrowdNear = 13, CrowdFar = 6;
        const float W = 1040, MineH = 176, FaceSize = 104;

        static readonly Vector2 Top = new Vector2(0.5f, 1), Bottom = new Vector2(0.5f, 0), Mid = new Vector2(0.5f, 0.5f);

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

        // ảnh phủ cả màn: ArtPostprocessor nhập 2048 (luật "/Casino/HamDau/hd_"); ảnh vào Assets trước khi luật có thì nhập lại
        static Sprite Big(string file)
        {
            string path = ArtDir + file;
            if (AssetImporter.GetAtPath(path) is TextureImporter ti && ti.maxTextureSize < 2048)
                AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        // khung các lớp rời trên ảnh nền 2k (ham_dau_lop.txt của dua_vao_unity.py: "tên x0 y0 x1 y1")
        static System.Collections.Generic.Dictionary<string, Rect> Layers()
        {
            var map = new System.Collections.Generic.Dictionary<string, Rect>();
            string path = ArtDir + "ham_dau_lop.txt";
            if (!File.Exists(path)) return map;
            foreach (var line in File.ReadAllLines(path))
            {
                var p = line.Split(' ');
                if (p.Length < 5) continue;
                float x0 = float.Parse(p[1]), y0 = float.Parse(p[2]), x1 = float.Parse(p[3]), y1 = float.Parse(p[4]);
                map[p[0]] = Rect.MinMaxRect(x0, y0, x1, y1);
            }
            return map;
        }

        // đặt một lớp rời đúng chỗ của nó trên sân khấu (khung px ảnh 2k → đơn vị sân khấu, neo mép trên)
        static Image Piece(Transform stage, string name, Rect box)
        {
            var img = Img(stage, name, Big(name + ".png"), Color.white);
            At(img.rectTransform, Top, new Vector2((box.center.x - ImgW / 2) * K, -box.yMin * K), new Vector2(box.width * K, box.height * K), Top);
            return img;
        }

        // vùng nhận chạm trong suốt
        static Image Hit(Transform p, string n)
        {
            var img = Img(p, n, null, new Color(1, 1, 1, 0), true);
            return img;
        }

        // ô hình tướng đội mình: khung (tô màu hệ lúc chạy), khung cắt lùi vào trong viền, chân dung (UndergroundScene.FitWhole đặt)
        static UndergroundScene.Face Face(UiKit kit, Transform parent, int k)
        {
            var frame = Img(parent, "tuong_" + k, Sketch.PanelThin, Theme.CardFill, false, true);
            At(frame.rectTransform, new Vector2(0, 0.5f), new Vector2(18 + k * (FaceSize + 6), 0), new Vector2(FaceSize, FaceSize), new Vector2(0, 0.5f));
            var mask = N(frame.transform, "khung", typeof(RectMask2D));
            HomeSceneMenu.Fill(mask);
            mask.offsetMin = new Vector2(9, 9);
            mask.offsetMax = new Vector2(-9, -9);
            var art = HomeSceneMenu.Fill(N(mask, "hinh"));
            var por = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, art)).GetComponent<HeroPortrait>();
            por.name = "chan_dung";
            var prt = por.Rect;
            prt.anchorMin = prt.anchorMax = prt.pivot = Mid;
            foreach (var g in por.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
            return new UndergroundScene.Face { root = frame.gameObject, frame = frame, art = art, portrait = por };
        }

        // chỗ đứng một tướng đội ngầm: gốc ở chân (UndergroundScene đặt lại theo số tướng), chân dung tĩnh, chỗ gắn sticker
        static UndergroundScene.Spot Spot(UiKit kit, Transform squad, int i)
        {
            var root = N(squad, "cho_" + i);
            At(root, Top, new Vector2(0, -1420), Vector2.zero, Mid);
            var por = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, root)).GetComponent<HeroPortrait>();
            por.name = "chan_dung";
            var prt = por.Rect;
            prt.anchorMin = prt.anchorMax = prt.pivot = Bottom;
            foreach (var g in por.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
            var body = N(root, "than");
            At(body, Mid, Vector2.zero, Vector2.zero, Mid);
            return new UndergroundScene.Spot { root = root, body = body, portrait = por };
        }

        static SketchButton Arrow(UiKit kit, Transform p, string n, string label, float x)
        {
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonRound.gameObject, p)).GetComponent<SketchButton>();
            b.name = n;
            b.SetRole(BtnColor.Paper);
            if (b.Label) b.SetText(label);
            At(b.Rect, Top, new Vector2(x, -ArrowY), new Vector2(104, 104), Mid);
            return b;
        }

        [MenuItem("PokiClash/Prefab/Đảo Casino/Hầm đấu: dựng scene", priority = 73)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var kit = assets.prefabs;
            var art = Load<ArtLibrary>();
            var nenSp = Big("hd_nen.jpg");
            var quaySp = Big("hd_quay.png");
            var rigFile = AssetDatabase.LoadAssetAtPath<TextAsset>(DealerRigPath);
            if (!nenSp || !quaySp) { Debug.LogError("[Đảo Casino] Thiếu ảnh nền Hầm đấu ở " + ArtDir + " (chạy ArtGen/Casino/ham_dau/dua_vao_unity.py)."); return; }
            if (!rigFile) Debug.LogWarning("[Đảo Casino] Thiếu rig Lão Mực " + DealerRigPath + ": quầy nhà cái để trống.");
            if (!File.Exists(ScreenPath))
            {
                if (!AssetDatabase.CopyAsset(BaseScreenPath, ScreenPath)) { Debug.LogError("[Đảo Casino] Không chép được " + BaseScreenPath); return; }
                AssetDatabase.ImportAsset(ScreenPath);
            }
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                root.name = "CasinoUnderground";
                var scene = root.GetComponent<UndergroundScene>();
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
                    scene = root.AddComponent<UndergroundScene>();
                    scene.SetupView(view ? view : root.GetComponentInChildren<PokiCanvas>(true), content);
                }
                else content = scene.Content;
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!nen || !safe) { Debug.LogError("[Đảo Casino] Screens/CasinoUnderground thiếu Canvas/Nen hoặc Canvas/An toan/Khung."); return; }
                var oldStage = nen.Find("san_khau");
                if (oldStage) Object.DestroyImmediate(oldStage.gameObject);
                foreach (Transform c in nen) c.gameObject.SetActive(c.name == "nen_hai_ben");
                if (nen.Find("nen_hai_ben")?.GetComponent<Image>() is Image si) { si.sprite = null; si.color = Theme.Hex(BottomHex); }
                foreach (Transform c in safe.Cast<Transform>().ToList()) if (c != content) Object.DestroyImmediate(c.gameObject);
                if (content) foreach (Transform c in content.Cast<Transform>().ToList()) Object.DestroyImmediate(c.gameObject);

                var paper = new Color(1f, 0.98f, 0.92f, 0.96f);
                var outline = Theme.Outlined(Theme.Bold, 0.3f);
                float stageH = ImgH * K, rimY = RimPx * K;

                // ---------- sân khấu ----------
                var stage = N(nen, "san_khau");
                At(stage, Top, Vector2.zero, new Vector2(1080, stageH), Top);
                var bg = Img(stage, "nen_ham", nenSp, Color.white);
                At(bg.rectTransform, Top, Vector2.zero, new Vector2(1080, stageH), Top);

                // khán giả trên khán đài hai bên (nhún): nằm ngay trên nền
                var layers = Layers();
                var crowdPieces = new System.Collections.Generic.List<PitCrowd.Piece>();
                foreach (var kv in layers.Where(x => x.Key.StartsWith("hd_kg_xa_")).OrderBy(x => x.Key))
                    crowdPieces.Add(new PitCrowd.Piece { rt = Piece(stage, kv.Key, kv.Value).rectTransform, amp = CrowdFar });

                // Lão Mực: lớp sau (thân, mặt), lớp quầy che thân dưới, lớp trước (tay tì mép quầy)
                float dealerX = (OpeningCx - ImgW / 2) * K;
                var rigHolder = N(stage, "lao_muc");
                At(rigHolder, Top, Vector2.zero, Vector2.zero, Top);
                var rigPos = new Vector2(dealerX, -(rimY + DealerRig.TableY * RigScale));
                DealerLayer Layer(string n)
                {
                    var rt = N(stage, n, typeof(DealerLayer));
                    At(rt, Top, rigPos, new Vector2(1000, 1400), new Vector2(0.5f, 0));
                    return rt.GetComponent<DealerLayer>();
                }
                var back = Layer("lao_muc_sau");
                var cover = Img(stage, "quay", quaySp, Color.white);
                At(cover.rectTransform, Top, new Vector2(((CoverX0 + CoverX1) / 2 - ImgW / 2) * K, -rimY), new Vector2((CoverX1 - CoverX0) * K, (CoverY1 - RimPx) * K), Top);

                // biển gỗ: tên bậc, dấu Đã thắng, vùng chạm xem chi tiết
                var sign = N(stage, "bien");
                At(sign, Top, new Vector2(((SignX0 + SignX1) / 2 - ImgW / 2) * K, -(SignY0 + SignY1) / 2 * K), new Vector2((SignX1 - SignX0) * K, (SignY1 - SignY0) * K), Mid);
                var signHit = Hit(sign, "cham");
                HomeSceneMenu.Fill(signHit.rectTransform);
                var signTap = signHit.gameObject.AddComponent<ClickCatcher>();
                var tierName = Auto(Txt(sign, "ten_bac", 48, Theme.Hex("#4a2c17")), 26);
                tierName.font = Theme.Title;
                tierName.textWrappingMode = TextWrappingModes.NoWrap;
                HomeSceneMenu.Fill(tierName.rectTransform);
                tierName.rectTransform.offsetMin = new Vector2(26, 8);
                tierName.rectTransform.offsetMax = new Vector2(-26, -6);
                // dấu Đã thắng đóng nghiêng đè góc trên phải biển (trên hàng chip của quầy, không bị tướng che)
                var wonStamp = Txt(sign, "da_thang", 44, Theme.RedD);
                wonStamp.font = Theme.Title;
                At(wonStamp.rectTransform, new Vector2(1, 1), new Vector2(-34, 2), new Vector2(300, 60), Mid);
                wonStamp.rectTransform.localEulerAngles = new Vector3(0, 0, 10);
                if (outline) wonStamp.fontSharedMaterial = outline;
                wonStamp.gameObject.SetActive(false);

                var front = Layer("lao_muc_truoc");
                if (rigFile)
                {
                    var rig = rigHolder.gameObject.AddComponent<DealerRig>();
                    rig.Setup(rigFile, back, front, RigScale);
                }

                // cổng sắt: khung mặt nạ theo lòng vòm (nền đã vá trống), song là con, trượt lên để mở
                RectTransform gateBars = null;
                if (layers.TryGetValue("hd_cong_mat_na", out var gateBox) && layers.ContainsKey("hd_cong_song"))
                {
                    var gateMask = Piece(stage, "hd_cong_mat_na", gateBox);
                    gateMask.gameObject.name = "cong";
                    gateMask.gameObject.AddComponent<Mask>().showMaskGraphic = false;
                    var bars = Img(gateMask.transform, "song", Big("hd_cong_song.png"), Color.white);
                    At(bars.rectTransform, Top, Vector2.zero, new Vector2(gateBox.width * K, gateBox.height * K), Top);
                    gateBars = bars.rectTransform;
                }
                else Debug.LogWarning("[Đảo Casino] Thiếu lớp cổng sắt (chạy ArtGen/Casino/ham_dau/tach_lop.py rồi dua_vao_unity.py).");

                // đội ngầm: hai tướng phía sau vẽ trước, tướng chủ lực (chỗ 0) vẽ sau cùng
                var squad = N(stage, "doi_ngam", typeof(CanvasGroup));
                At(squad, Top, Vector2.zero, Vector2.zero, Top);
                var squadCg = squad.GetComponent<CanvasGroup>();
                squadCg.blocksRaycasts = squadCg.interactable = false;
                var spots = new UndergroundScene.Spot[3];
                foreach (int i in new[] { 1, 2, 0 }) spots[i] = Spot(kit, squad, i);

                // khán giả hàng đầu (nhún): trước đội ngầm, sau các nút và thẻ
                foreach (var kv in layers.Where(x => x.Key.StartsWith("hd_kg_duoi_")).OrderBy(x => x.Key))
                    crowdPieces.Add(new PitCrowd.Piece { rt = Piece(stage, kv.Key, kv.Value).rectTransform, amp = CrowdNear });
                var pitCrowd = stage.gameObject.AddComponent<PitCrowd>();
                pitCrowd.Setup(crowdPieces.ToArray());

                // vùng vuốt phủ sàn đấu (dưới mũi tên, chip, thẻ)
                var swipeImg = Hit(stage, "vuot");
                At(swipeImg.rectTransform, Top, new Vector2(0, -PitTop), new Vector2(1080, PitH), Top);
                var swipe = swipeImg.gameObject.AddComponent<SwipeArea>();

                var prev = Arrow(kit, stage, "truoc", "<", -ArrowX);
                var next = Arrow(kit, stage, "sau", ">", ArrowX);

                // thẻ số tướng + lực chiến dưới chân đội
                var info = Img(stage, "the_doi", Sketch.Pill, paper, false, true);
                At(info.rectTransform, Top, new Vector2(0, -InfoY), new Vector2(440, 62), Mid);
                var count = Auto(Txt(info.transform, "so_tuong", 28, Theme.Ink2), 18);
                count.alignment = TextAlignmentOptions.Midline;
                At(count.rectTransform, new Vector2(0, 0.5f), new Vector2(24, 0), new Vector2(180, 44), new Vector2(0, 0.5f));
                var ic = Img(info.transform, "icon_luc_chien", art ? art.Icon("sword") : null, Color.white);
                ic.preserveAspect = true;
                At(ic.rectTransform, new Vector2(0, 0.5f), new Vector2(222, 0), new Vector2(38, 38), new Vector2(0, 0.5f));
                var power = Auto(Txt(info.transform, "luc_chien", 36, Theme.RedD), 22);
                power.font = Theme.Title;
                power.alignment = TextAlignmentOptions.MidlineLeft;
                At(power.rectTransform, new Vector2(0, 0.5f), new Vector2(268, 0), new Vector2(156, 48), new Vector2(0, 0.5f));

                // thẻ luật ngày (chỉ hiện khi bậc có luật)
                var ruleBg = Img(stage, "the_luat", Sketch.Pill, Theme.Hex("#dbe8fb"), false, true);
                At(ruleBg.rectTransform, Top, new Vector2(0, -RuleY), new Vector2(600, 46), Mid);
                var rule = Auto(Txt(ruleBg.transform, "chu", 23, Theme.BlueD), 15);
                HomeSceneMenu.Fill(rule.rectTransform);
                rule.rectTransform.offsetMin = new Vector2(20, 2);
                rule.rectTransform.offsetMax = new Vector2(-20, -2);

                // hàng chip chọn bậc (UndergroundScene căn giữa theo số bậc hôm nay)
                var chips = new UndergroundScene.Chip[Chips];
                for (int i = 0; i < Chips; i++)
                {
                    var cr = N(stage, "chip_" + i);
                    At(cr, Top, new Vector2((i - (Chips - 1) / 2f) * 76, -ChipY), new Vector2(50, 50), Mid);
                    var hit = Hit(cr, "cham");
                    At(hit.rectTransform, Mid, Vector2.zero, new Vector2(72, 72), Mid);
                    var click = hit.gameObject.AddComponent<ClickCatcher>();
                    var ring = Img(cr, "vien", Sketch.Dot, Theme.Ink);
                    At(ring.rectTransform, Mid, Vector2.zero, new Vector2(58, 58), Mid);
                    var dot = Img(cr, "mau", Sketch.Dot, Color.white);
                    At(dot.rectTransform, Mid, Vector2.zero, new Vector2(44, 44), Mid);
                    var star = Img(cr, "da_thang", Sketch.Star, Theme.Yellow);
                    star.preserveAspect = true;
                    At(star.rectTransform, Mid, new Vector2(17, 19), new Vector2(30, 30), Mid);
                    chips[i] = new UndergroundScene.Chip { root = cr, dot = dot, ring = ring, won = star.gameObject, click = click };
                }

                // bong bóng thoại của Lão Mực (bên phải quầy)
                var bubble = Img(stage, "bong_bong", Sketch.PanelThin, new Color(1f, 0.98f, 0.92f, 0.98f), false, true);
                At(bubble.rectTransform, Top, new Vector2(376, -420), new Vector2(312, 196), Mid);
                var bubbleText = Auto(Txt(bubble.transform, "chu", 26, Theme.Ink), 17);
                HomeSceneMenu.Fill(bubbleText.rectTransform);
                bubbleText.rectTransform.offsetMin = new Vector2(18, 12);
                bubbleText.rectTransform.offsetMax = new Vector2(-18, -12);
                bubble.gameObject.SetActive(false);

                // ---------- khung an toàn ----------
                var page = HomeSceneMenu.Fill(N(safe, "ham_dau"));
                var clockBg = Img(page, "dong_ho", Sketch.Pill, new Color(1f, 0.98f, 0.92f, 0.92f), false, true);
                At(clockBg.rectTransform, new Vector2(0, 1), new Vector2(18, -SceneRoot.BarHeight - 4), new Vector2(404, 46), new Vector2(0, 1));
                var clock = Auto(Txt(clockBg.transform, "chu", 22, Theme.BlueD), 15);
                HomeSceneMenu.Fill(clock.rectTransform);
                var fightsBg = Img(page, "luot_danh", Sketch.Pill, new Color(1f, 0.98f, 0.92f, 0.92f), false, true);
                At(fightsBg.rectTransform, new Vector2(0, 1), new Vector2(18, -SceneRoot.BarHeight - 56), new Vector2(404, 46), new Vector2(0, 1));
                var fightsText = Auto(Txt(fightsBg.transform, "chu", 22, Theme.Ink), 15);
                HomeSceneMenu.Fill(fightsText.rectTransform);

                // dải đáy: đội của mình, Đổi đội, Đánh
                var mine = Img(page, "doi_minh", Sketch.PanelThin, paper, false, true);
                At(mine.rectTransform, Bottom, new Vector2(0, 24), new Vector2(W, MineH), Bottom);
                var myFaces = new UndergroundScene.Face[Faces];
                for (int k = 0; k < Faces; k++) myFaces[k] = Face(kit, mine.transform, k);
                float infoX = 18 + Faces * (FaceSize + 6) + 8;
                var myCount = Auto(Txt(mine.transform, "so_tuong", 25, Theme.Ink2), 17);
                myCount.alignment = TextAlignmentOptions.MidlineLeft;
                At(myCount.rectTransform, new Vector2(0, 0.5f), new Vector2(infoX, 28), new Vector2(150, 36), new Vector2(0, 0.5f));
                var myIc = Img(mine.transform, "icon_luc_chien", art ? art.Icon("sword") : null, Color.white);
                myIc.preserveAspect = true;
                At(myIc.rectTransform, new Vector2(0, 0.5f), new Vector2(infoX, -24), new Vector2(34, 34), new Vector2(0, 0.5f));
                var myPower = Auto(Txt(mine.transform, "luc_chien", 32, Theme.Ink), 20);
                myPower.font = Theme.Title;
                myPower.alignment = TextAlignmentOptions.MidlineLeft;
                At(myPower.rectTransform, new Vector2(0, 0.5f), new Vector2(infoX + 40, -24), new Vector2(112, 44), new Vector2(0, 0.5f));
                var team = HomeSceneMenu.Button(assets, mine.transform, "doi_doi", Loc.T("Đổi đội"), BtnColor.Yellow, new Vector2(190, 92));
                At((RectTransform)team.transform, new Vector2(1, 0.5f), new Vector2(-338, 0), new Vector2(190, 92), new Vector2(1, 0.5f));
                var fight = HomeSceneMenu.Button(assets, mine.transform, "danh", Loc.T("Đánh"), BtnColor.Green, new Vector2(312, 124));
                At((RectTransform)fight.transform, new Vector2(1, 0.5f), new Vector2(-14, 0), new Vector2(312, 124), new Vector2(1, 0.5f));

                var picker = AssetDatabase.LoadAssetAtPath<GameObject>(PickerPath)?.GetComponent<TeamPickerDialog>();
                if (!picker) Debug.LogWarning("[Đảo Casino] Thiếu " + PickerPath + ": nút Đổi đội không mở được hộp chọn đội.");
                scene.SetupStage(squad, squadCg, spots, swipe, prev, next, chips, sign, tierName, wonStamp, signTap, info.rectTransform, count, power,
                    ruleBg.gameObject, rule);
                scene.SetupDealer(rigHolder.GetComponent<DealerRig>(), bubble.rectTransform, bubbleText, clock);
                scene.SetupMine(myFaces, myCount, myPower, team, fight, picker);
                scene.SetupLife(gateBars, pitCrowd, fightsText);
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            MakeScene();
            // hộp cũ Dialogs/HamDau (UndergroundDialog đã bỏ): xoá prefab, gỡ ô trống khỏi danh sách hộp của kit
            if (File.Exists(OldDialogPath)) AssetDatabase.DeleteAsset(OldDialogPath);
            if (kit.dialogs.RemoveAll(x => !x) > 0) EditorUtility.SetDirty(kit);
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
                ((GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(ScreenPath))).name = SceneIds.CasinoUnderground;
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

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "casino_ham");

        static IEnumerator Wait(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        // chờ đội trên sàn dựng xong sticker (tối đa secs) rồi chờ thêm cho Lão Mực nói
        static IEnumerator Settle(UndergroundScene sc, float secs, float extra)
        {
            float t0 = Time.realtimeSinceStartup;
            while (sc && !sc.SquadReady && Time.realtimeSinceStartup - t0 < secs) yield return null;
            yield return new WaitForSecondsRealtime(extra);
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
                s.level = Mathf.Max(s.level, 40); // vừa đủ mở Hầm đấu: mọi bậc vẫn đánh được (không khoá theo cấp)
                s.balls = Mathf.Max(s.balls, 5000);
                Casino.Of(s).intro = true;
                CasinoGuide.SkipAll(s); // tour: không hiện lời dẫn của Lão Mực (chặn chạm)
                App.Router.Go(SceneIds.Casino);
                yield return Wait(SceneIds.Casino);
                yield return new WaitForSecondsRealtime(1.2f);
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.4f);
                CasinoGames.Open(Casino.Underground, null);
                yield return Wait(SceneIds.CasinoUnderground);
                var sc = Object.FindAnyObjectByType<UndergroundScene>();
                yield return Settle(sc, 8, 1.6f);
                App.Modals.CloseAll();
                yield return Shot("1_vao_ham");
                Debug.Log("[Thử] Nhạc Hầm đấu: " + App.Audio.CurrentMusic + " (đợi: tran)");
                // lần lượt từng bậc: bậc đầu (dễ), bậc cuối (khó)
                sc.JumpForTest(0);
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Settle(sc, 8, 1.0f);
                yield return Shot("2_bac_dau");
                sc.StepForTest(1);
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Settle(sc, 8, 1.0f);
                yield return Shot("3_bac_hai");
                sc.StepForTest(-1);
                yield return new WaitForSecondsRealtime(0.34f);
                yield return Shot("4_dang_chay_ra");
                yield return new WaitForSecondsRealtime(0.6f);
                sc.JumpForTest(9);
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Settle(sc, 8, 1.0f);
                yield return Shot("5_bac_kho");
                var signTap = sc.GetComponentsInChildren<ClickCatcher>(true).FirstOrDefault(c => c.transform.parent.name == "bien");
                if (signTap)
                {
                    signTap.OnClick?.Invoke();
                    yield return new WaitForSecondsRealtime(0.6f);
                    yield return Shot("6_chi_tiet");
                    App.Modals.CloseAll();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                // đánh giả thắng bậc đầu rồi về lại như vừa xong trận thắng (Lão Mực cay)
                if (Underground.Pay(s, App.Data, 0, Game.SaveService.Now(), out _))
                    Underground.Finish(s, App.Data, 0, true, Game.SaveService.Now(), new Rng(1));
                App.Router.Go(SceneIds.CasinoUnderground, new UgReturn { tier = 0, won = true });
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Wait(SceneIds.CasinoUnderground);
                sc = Object.FindAnyObjectByType<UndergroundScene>();
                yield return Settle(sc, 8, 1.4f);
                yield return Shot("7_ve_sau_thang");
                // giả hết lượt đánh hôm nay: nút Đánh khoá, Lão Mực tiễn khách; rồi trả lại số lượt để vào trận thật
                var st = Casino.Roll(s, App.Data, Game.SaveService.Now());
                int used = st.Play(Casino.Underground);
                st.plays[Casino.Underground] = App.Data.Cfg.casino.underground.daily;
                sc.Refresh();
                sc.StepForTest(1);
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Settle(sc, 8, 1.0f);
                yield return Shot("8_het_luot");
                st.plays[Casino.Underground] = used;
                sc.Refresh();
                yield return new WaitForSecondsRealtime(0.3f);
                sc.FightForTest();
                yield return Wait(SceneIds.Battle);
                yield return new WaitForSecondsRealtime(3.5f);
                yield return Shot("9_tran_ngam");
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
            File.WriteAllBytes(Path.Combine(ShotDir, name + ".jpg"), tex.EncodeToJPG(88));
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
            // cờ nạp lại âm thanh (tiếng khán giả mới): như menu "PokiClash/Âm thanh/Nạp nhạc và tiếng"
            var audio = Flag("casino_ug_audio.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(audio))
            {
                File.Delete(audio);
                AudioImportMenu.Run();
                AssetDatabase.SaveAssets();
                Debug.Log("[Đảo Casino] Nạp lại âm thanh (cờ casino_ug_audio): xong");
                return;
            }
            // cờ nhập lại dữ liệu (balance.json đổi đội ngầm): như menu "PokiClash/Nhập dữ liệu"
            var data = Flag("casino_ug_data.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(data))
            {
                File.Delete(data);
                bool ok = DataImporter.Run(true);
                AssetDatabase.SaveAssets();
                Debug.Log("[Đảo Casino] Nhập lại dữ liệu (cờ casino_ug_data): " + (ok ? "xong" : "LỖI"));
                return;
            }
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
