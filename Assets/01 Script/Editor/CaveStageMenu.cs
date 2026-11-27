// Màn Hang Tiềm Năng bản sân khấu (CaveScene, người dùng 2026-11-27: ít chữ, đủ thông tin, thưởng bằng icon trên thanh tiến độ; tham
// khảo Hầm đấu và võ đường huy hiệu của Clash of Critters). Menu "PokiClash/Prefab/Nhà và side meta/Hang Tiềm Năng: dựng sân khấu"
// (chạy lại được) dựng lại Screens/Cave tại chỗ: giữ canvas và CaveScene, bỏ trang giấy cũ (bàn gỗ, trang, khung cuộn, hàng tầng).
// - Sân khấu dưới Canvas/Nen (rộng 1080, neo mép trên, cao bằng ảnh nền 1144 x 2048 thu về bề ngang 1080; CaveScene dời xuống theo tai
//   thỏ): lớp trần (màu trần hang, phủ phần lộ ra phía trên), ảnh nền (Assets/03 Art/Cave/hang_nen.jpg, ArtGen/Cave/dua_vao_unity.py),
//   thanh tiến độ (đầu thanh: hệ boss, đá đang có; rãnh + phần đã qua; 10 nút tầng: vòng, lõi, icon thưởng, số, dấu tích, số tầng, vùng
//   chạm; mũi tên tầng đang xem), bảng đá (tên tầng, 3 ô thưởng lần đầu, dấu Đã qua, vùng chạm), vùng vuốt, đôi địch (2 chỗ đứng: chân
//   dung tĩnh, chỗ gắn sticker, thẻ cấp), ổ khoá + chữ điều kiện, thẻ "chọn hệ boss", hai mũi tên.
//   Số đo bảng đá trên ảnh 2k chép từ Assets/03 Art/Cave/hang.json, nhân K ra đơn vị sân khấu.
// - Khung an toàn (vùng nội dung mới "hang"): hàng 5 hệ (nút kit, icon hệ, chữ thứ), thẻ lượt, nút "+1 lượt" (hang_them_luot), nút chính
//   (vao_tang_i), thẻ thưởng mỗi trận thắng. Tên nút giữ như bản cũ cho PlayTour (chon_kim, vao_tang_0, hang_them_luot).
// Phần màn dài hơn ảnh tô màu đáy ảnh. Dựng xong xoá Items/TangHang (hàng tầng bản cũ), mở scene Cave gỡ phần đè của bản sao prefab.
// Cờ Temp/cave_stage_build.flag (dựng), Temp/cave_stage_tour.flag (vào Play, mở Hang, chụp: vào màn, tầng đã qua, tầng khoá, hộp chi
// tiết, cuối tuần chọn hệ, hết lượt, về sau khi vượt tầng, hộp chuẩn bị trận; bản lưu sao lưu, trả lại). Ảnh Temp/PokiShots/hang/.
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
    public static class CaveStageMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/Cave.prefab";
        const string ScenePath = "Assets/00 Scenes/Cave.unity";
        const string OldRowPath = "Assets/04 Prefabs/Items/TangHang.prefab";
        const string ArtDir = "Assets/03 Art/Cave/";

        // ảnh nền 2k và số đo trên ảnh (hang.json): bảng đá trống trên vòm
        const float ImgW = 1144, ImgH = 2048, K = 1080f / ImgW;
        const float TabX0 = 265, TabY0 = 388, TabX1 = 868, TabY1 = 550;
        const string TopHex = "#4c4264", BottomHex = "#342a49";
        // thanh tiến độ (khung an toàn, không phóng theo sân khấu; y tính từ đỉnh thanh): đỉnh thanh, cao, dòng đầu, tâm nút, số tầng,
        // mũi tên, khoảng nút
        const float BandTop = 152, BandW = 1048, BandH = 228, HeadY = 28, NodeY = 138, NumY = 204, MarkY = 70, NodeGap = 104;
        const int Nodes = 10;
        // bệ: vùng vuốt, mũi tên, ổ khoá, thẻ chọn hệ (y sân khấu)
        const float SwipeTop = 560, SwipeH = 860, ArrowY = 1040, ArrowX = 476, LockY = 1120, LockTextY = 1250, PickY = 1180;
        // dải đáy (khung an toàn, tính từ đáy): hàng hệ, hàng nút
        const float TabsY = 14, TabsH = 166, TabW = 192, TabH = 148, TabGap = 204, RowY = 204;
        static readonly Color Cream = new Color32(0xff, 0xf6, 0xdf, 0xff);

        static readonly Vector2 Top = new Vector2(0.5f, 1), Bottom = new Vector2(0.5f, 0), Mid = new Vector2(0.5f, 0.5f),
            LeftTop = new Vector2(0, 1), Left = new Vector2(0, 0.5f);

        static RectTransform N(Transform p, string n, params System.Type[] t) => HomeSceneMenu.Node(p, n, t);
        static RectTransform At(RectTransform rt, Vector2 a, Vector2 pos, Vector2 size, Vector2 pivot) => HomeSceneMenu.At(rt, a, pos, size, pivot);
        static Image Img(Transform p, string n, Sprite s, Color c, bool ray = false, bool sliced = false) => HomeSceneMenu.Img(p, n, s, c, ray, sliced);
        static TextMeshProUGUI Txt(Transform p, string n, float size, Color c) => HomeSceneMenu.Text(p, n, size, c);

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        static TextMeshProUGUI Auto(TextMeshProUGUI t, float min)
        {
            t.enableAutoSizing = true;
            t.fontSizeMin = min;
            t.fontSizeMax = t.fontSize;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            return t;
        }

        // chữ sáng viền mực (tiêu đề, số trên nền tối)
        static TextMeshProUGUI Light(Transform p, string n, float size, Material outline, TMP_FontAsset font = null)
        {
            var t = Txt(p, n, size, Color.white);
            if (font) t.font = font;
            if (outline) t.fontSharedMaterial = outline;
            return t;
        }

        // ảnh nền phủ cả màn: ArtImporter nhập 2048 (luật "/Cave/hang_nen"); ảnh vào Assets trước khi có luật thì nhập lại
        static Sprite Big(string file)
        {
            string path = ArtDir + file;
            if (AssetImporter.GetAtPath(path) is TextureImporter ti && ti.maxTextureSize < 2048)
                AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        static Sprite Art(string file)
        {
            string path = ArtDir + file;
            var s = AssetDatabase.LoadAssetAtPath<Sprite>(path);
            if (s || !File.Exists(path)) return s;
            AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        static Image Icon(Transform p, string n, Sprite s, float size)
        {
            var img = Img(p, n, s, Color.white);
            img.preserveAspect = true;
            img.rectTransform.sizeDelta = new Vector2(size, size);
            return img;
        }

        // vùng nhận chạm trong suốt
        static ClickCatcher Hit(Transform p, string n, Vector2 size)
        {
            var img = Img(p, n, null, new Color(1, 1, 1, 0), true);
            At(img.rectTransform, Mid, Vector2.zero, size, Mid);
            return img.gameObject.AddComponent<ClickCatcher>();
        }

        // đĩa kem viền mực chứa một icon (icon hệ, icon thưởng): icon màu luôn rõ dù nền tối hay nền màu
        static Image Badge(Transform p, string n, Vector2 pos, float size, Sprite icon, float iconSize)
        {
            var ring = Img(p, n, Sketch.Dot, Theme.Ink);
            At(ring.rectTransform, Mid, pos, new Vector2(size, size), Mid);
            var disc = Img(ring.transform, "loi", Sketch.Dot, Cream);
            At(disc.rectTransform, Mid, Vector2.zero, new Vector2(size - 10, size - 10), Mid);
            var ic = Icon(ring.transform, "icon", icon, iconSize);
            At(ic.rectTransform, Mid, Vector2.zero, new Vector2(iconSize, iconSize), Mid);
            return ic;
        }

        // một nút tầng (lõi sáng để icon màu đọc rõ trên thanh tối, người dùng 2026-11-27 chê bản lõi tối): vòng mực, lõi (tô theo trạng
        // thái), icon thưởng to, thẻ trắng số món, huy hiệu xanh đã qua, số tầng dưới nút, vùng chạm
        static CaveScene.Node Node(Transform parent, int i, Sprite check, Material outline)
        {
            var root = N(parent, "tang_" + i);
            At(root, Top, new Vector2((i - (Nodes - 1) / 2f) * NodeGap, -NodeY), new Vector2(96, 96), Mid);
            var ring = Img(root, "vien", Sketch.Dot, Theme.Ink);
            At(ring.rectTransform, Mid, Vector2.zero, new Vector2(94, 94), Mid);
            var disc = Img(root, "loi", Sketch.Dot, Color.white);
            At(disc.rectTransform, Mid, Vector2.zero, new Vector2(82, 82), Mid);
            var icon = Icon(root, "icon", null, 70);
            At(icon.rectTransform, Mid, new Vector2(0, 3), new Vector2(70, 70), Mid);
            var tag = Img(root, "the_so", Sketch.Pill, Color.white, false, true);
            At(tag.rectTransform, Mid, new Vector2(26, -32), new Vector2(64, 38), Mid);
            var count = Auto(Txt(tag.transform, "so", 30, Theme.Ink), 18);
            count.font = Theme.Title;
            HomeSceneMenu.Fill(count.rectTransform);
            count.rectTransform.offsetMin = new Vector2(4, 1);
            count.rectTransform.offsetMax = new Vector2(-4, -1);
            var done = Img(root, "da_qua", Sketch.Dot, Theme.Ink);
            At(done.rectTransform, Mid, new Vector2(32, 32), new Vector2(38, 38), Mid);
            var doneFill = Img(done.transform, "loi", Sketch.Dot, Cream); // dấu tích xanh trên đĩa kem
            At(doneFill.rectTransform, Mid, Vector2.zero, new Vector2(30, 30), Mid);
            var tick = Icon(done.transform, "dau", check, 28);
            At(tick.rectTransform, Mid, new Vector2(1, 0), new Vector2(28, 28), Mid);
            var num = Light(root, "so_tang", 30, outline, Theme.Title);
            num.textWrappingMode = TextWrappingModes.NoWrap;
            At(num.rectTransform, Mid, new Vector2(0, -(NumY - NodeY)), new Vector2(80, 36), Mid);
            var click = Hit(root, "cham", new Vector2(NodeGap, 170));
            click.GetComponent<RectTransform>().anchoredPosition = new Vector2(0, -20);
            return new CaveScene.Node
            {
                root = root, ring = ring, disc = disc, icon = icon, countTag = tag.gameObject, done = done.gameObject, count = count, num = num,
                click = click
            };
        }

        // chỗ đứng một địch trên bệ: gốc ở chân (CaveScene đặt lại), chân dung tĩnh, chỗ gắn sticker, thẻ cấp dưới chân
        static CaveScene.Spot Spot(UiKit kit, Transform squad, int i, Sprite bossIcon, Color paper)
        {
            var root = N(squad, i == 0 ? "boss" : "phu");
            At(root, Top, new Vector2(i == 0 ? -90 : 292, i == 0 ? -1322 : -1196), Vector2.zero, Mid);
            var por = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, root)).GetComponent<HeroPortrait>();
            por.name = "chan_dung";
            var prt = por.Rect;
            prt.anchorMin = prt.anchorMax = prt.pivot = Bottom;
            foreach (var g in por.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
            var body = N(root, "than");
            At(body, Mid, Vector2.zero, Vector2.zero, Mid);
            float w = i == 0 ? 168 : 124;
            var tag = Img(root, "the_cap", Sketch.Pill, paper, false, true);
            At(tag.rectTransform, Mid, new Vector2(0, -10), new Vector2(w, 48), Top);
            float textX = 14;
            if (i == 0)
            {
                var bi = Icon(tag.transform, "icon_boss", bossIcon, 34);
                At(bi.rectTransform, Left, new Vector2(12, 0), new Vector2(34, 34), Left);
                textX = 50;
            }
            var text = Auto(Txt(tag.transform, "cap", 28, Theme.Ink), 18);
            text.font = Theme.Title;
            text.alignment = TextAlignmentOptions.Midline;
            At(text.rectTransform, Left, new Vector2(textX, 0), new Vector2(w - textX - 12, 40), Left);
            return new CaveScene.Spot { root = root, body = body, portrait = por, tag = tag.gameObject, tagText = text };
        }

        static SketchButton Arrow(UiKit kit, Transform p, string n, string label, float x)
        {
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonRound.gameObject, p)).GetComponent<SketchButton>();
            b.name = n;
            b.SetRole(BtnColor.Paper);
            if (b.Label) b.SetText(label);
            At(b.Rect, Top, new Vector2(x, -ArrowY), new Vector2(96, 96), Mid);
            return b;
        }

        [MenuItem("PokiClash/Prefab/Nhà và side meta/Hang Tiềm Năng: dựng sân khấu", priority = 63)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var kit = assets.prefabs;
            var art = Load<ArtLibrary>();
            Sprite Ic(string n) => art ? art.Icon(n) : null;
            var nenSp = Big("hang_nen.jpg");
            var stoneSp = Art("hang_da_tiem_nang.png");
            var crystalSp = Art("hang_da_tinh.png");
            var evoSp = Art("hang_da_tien_hoa.png");
            if (!nenSp || !stoneSp || !crystalSp || !evoSp)
            {
                Debug.LogError("[Hang] Thiếu ảnh ở " + ArtDir + " (chạy ArtGen/Cave/dua_vao_unity.py).");
                return;
            }
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                var scene = root.GetComponent<CaveScene>();
                if (!scene) { Debug.LogError("[Hang] " + ScreenPath + " không có CaveScene."); return; }
                var view = scene.View ? scene.View : root.GetComponentInChildren<PokiCanvas>(true);
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!nen || !safe) { Debug.LogError("[Hang] " + ScreenPath + " thiếu Canvas/Nen hoặc Canvas/An toan/Khung."); return; }
                // bỏ trang giấy cũ: mọi lớp nền trừ nen_hai_ben (tô màu đáy ảnh), mọi thứ trong khung an toàn
                foreach (Transform c in nen.Cast<Transform>().ToList())
                    if (c.name != "nen_hai_ben") Object.DestroyImmediate(c.gameObject);
                if (nen.Find("nen_hai_ben")?.GetComponent<Image>() is Image side)
                {
                    side.sprite = null;
                    side.color = Theme.Hex(BottomHex);
                }
                foreach (Transform c in safe.Cast<Transform>().ToList()) Object.DestroyImmediate(c.gameObject);

                var paper = new Color(1f, 0.98f, 0.92f, 0.96f);
                var outline = Theme.Outlined(Theme.Title, 0.22f);
                var outlineBold = Theme.Outlined(Theme.Bold, 0.25f);
                float stageH = ImgH * K;

                // ---------- sân khấu ----------
                var stage = N(nen, "san_khau");
                At(stage, Top, Vector2.zero, new Vector2(1080, stageH), Top);
                var ceil = Img(stage, "tran", null, Theme.Hex(TopHex));
                At(ceil.rectTransform, Top, Vector2.zero, new Vector2(1080, 600), Bottom); // phủ phần lộ ra trên đỉnh ảnh khi dời theo tai thỏ
                var bg = Img(stage, "nen_hang", nenSp, Color.white);
                At(bg.rectTransform, Top, Vector2.zero, new Vector2(1080, stageH), Top);

                // ---------- khung an toàn (vẽ đè sân khấu): thanh tiến độ trên, dải đáy dưới ----------
                var page = HomeSceneMenu.Fill(N(safe, "hang"));

                // thanh tiến độ: nằm trong khung an toàn nên không phóng theo sân khấu (sân khấu phóng cho vừa chiều cao màn)
                var band = Img(page, "thanh_tien_do", Sketch.PanelThin, new Color(0.13f, 0.11f, 0.21f, 0.92f), false, true);
                At(band.rectTransform, Top, new Vector2(0, -BandTop), new Vector2(BandW, BandH), Top);
                // đầu thanh: huy hiệu hệ boss + "Boss hệ …" (trái), đá tiềm năng, đá tinh trong thẻ sáng (phải)
                var headElem = Badge(band.transform, "he", Vector2.zero, 50, null, 38);
                var headBadge = (RectTransform)headElem.transform.parent;
                At(headBadge, LeftTop, new Vector2(38, -HeadY), new Vector2(50, 50), Mid);
                var headText = Auto(Light(band.transform, "he_chu", 34, outline, Theme.Title), 22);
                headText.alignment = TextAlignmentOptions.MidlineLeft;
                At(headText.rectTransform, LeftTop, new Vector2(72, -HeadY), new Vector2(560, 50), Left);
                TextMeshProUGUI Res(string n, Sprite icon, float cx)
                {
                    var pill = Img(band.transform, n, Sketch.Pill, Cream, false, true);
                    At(pill.rectTransform, LeftTop, new Vector2(cx, -HeadY), new Vector2(150, 44), Mid);
                    var ic = Icon(pill.transform, "icon", icon, 54);
                    At(ic.rectTransform, Left, new Vector2(-14, 0), new Vector2(54, 54), Left);
                    var num = Auto(Txt(pill.transform, "so", 30, Theme.Ink), 18);
                    num.font = Theme.Title;
                    num.alignment = TextAlignmentOptions.MidlineLeft;
                    At(num.rectTransform, Left, new Vector2(46, 0), new Vector2(98, 40), Left);
                    return num;
                }
                var stones = Res("da", stoneSp, BandW - 272);
                var crystals = Res("tinh", crystalSp, BandW - 96);
                float x0 = -(Nodes - 1) / 2f * NodeGap;
                var rail = Img(band.transform, "ray", Sketch.Pill, new Color(0.05f, 0.04f, 0.09f, 0.95f), false, true);
                At(rail.rectTransform, Top, new Vector2(0, -NodeY), new Vector2((Nodes - 1) * NodeGap + 24, 24), Mid);
                var fill = Img(band.transform, "ray_da_qua", Sketch.Pill, Theme.Yellow, false, true);
                At(fill.rectTransform, Top, new Vector2(x0, -NodeY), new Vector2(0, 16), Left);
                var nodeRoot = N(band.transform, "nut");
                HomeSceneMenu.Fill(nodeRoot);
                var check = Ic("check");
                var nodes = new CaveScene.Node[Nodes];
                for (int i = 0; i < Nodes; i++) nodes[i] = Node(nodeRoot, i, check, outline);
                var marker = Icon(band.transform, "dang_xem", Ic("down"), 34);
                At(marker.rectTransform, Top, new Vector2(x0, -MarkY), new Vector2(34, 34), Mid);

                // bảng đá: tên tầng, thưởng lần đầu, dấu Đã qua
                var tablet = N(stage, "bang_da");
                At(tablet, Top, new Vector2(((TabX0 + TabX1) / 2 - ImgW / 2) * K, -(TabY0 + TabY1) / 2 * K), new Vector2((TabX1 - TabX0) * K, (TabY1 - TabY0) * K), Mid);
                var tabletTap = Hit(tablet, "cham", tablet.sizeDelta);
                var floorName = Auto(Txt(tablet, "ten_tang", 44, Color.white), 26);
                floorName.font = Theme.Title;
                if (outline) floorName.fontSharedMaterial = outline;
                At(floorName.rectTransform, Top, new Vector2(0, -12), new Vector2(tablet.sizeDelta.x - 56, 60), Top);
                var prizes = new CaveScene.Prize[3];
                for (int i = 0; i < prizes.Length; i++)
                {
                    var pr = N(tablet, "thuong_" + i);
                    At(pr, Mid, new Vector2((i - 1) * 132, -32), new Vector2(140, 60), Mid);
                    var pic = Icon(pr, "icon", null, 58);
                    At(pic.rectTransform, Left, new Vector2(4, 0), new Vector2(58, 58), Left);
                    var pn = Auto(Txt(pr, "so", 34, Theme.Hex("#4a2c17")), 20);
                    pn.font = Theme.Title;
                    pn.alignment = TextAlignmentOptions.MidlineLeft;
                    At(pn.rectTransform, Left, new Vector2(64, 0), new Vector2(76, 44), Left);
                    prizes[i] = new CaveScene.Prize { root = pr, icon = pic, count = pn };
                }
                var firstLabel = Auto(Txt(tablet, "lan_dau", 28, Theme.Hex("#6b4a2e")), 18);
                firstLabel.alignment = TextAlignmentOptions.MidlineRight;
                At(firstLabel.rectTransform, Mid, new Vector2(-200, -32), new Vector2(120, 44), new Vector2(1, 0.5f));
                firstLabel.text = Loc.T("Lần đầu");
                var passed = Txt(tablet, "da_qua", 40, Theme.Hex("#5fc24f"));
                passed.font = Theme.Title;
                if (outline) passed.fontSharedMaterial = outline;
                At(passed.rectTransform, Mid, new Vector2(0, -32), new Vector2(300, 54), Mid);
                passed.rectTransform.localEulerAngles = new Vector3(0, 0, 5);
                passed.gameObject.SetActive(false);

                // vùng vuốt phủ bệ (dưới mũi tên, thẻ)
                var swipeImg = Img(stage, "vuot", null, new Color(1, 1, 1, 0), true);
                At(swipeImg.rectTransform, Top, new Vector2(0, -SwipeTop), new Vector2(1080, SwipeH), Top);
                var swipe = swipeImg.gameObject.AddComponent<SwipeArea>();

                // đôi địch: tướng phụ (sau) vẽ trước, boss vẽ sau cùng
                var squad = N(stage, "doi_dich", typeof(CanvasGroup));
                At(squad, Top, Vector2.zero, Vector2.zero, Top);
                var squadCg = squad.GetComponent<CanvasGroup>();
                squadCg.blocksRaycasts = squadCg.interactable = false;
                var spots = new CaveScene.Spot[2];
                spots[1] = Spot(kit, squad, 1, null, paper);
                spots[0] = Spot(kit, squad, 0, Ic("boss"), paper);

                // ổ khoá + điều kiện mở (tầng chưa mở)
                var lockRoot = N(stage, "khoa");
                At(lockRoot, Top, Vector2.zero, Vector2.zero, Top);
                var lockIc = Icon(lockRoot, "icon", Ic("lock"), 120);
                At(lockIc.rectTransform, Top, new Vector2(0, -LockY), new Vector2(120, 120), Mid);
                var lockBg = Img(lockRoot, "the", Sketch.Pill, paper, false, true);
                At(lockBg.rectTransform, Top, new Vector2(0, -LockTextY), new Vector2(420, 62), Mid);
                var lockText = Auto(Txt(lockBg.transform, "chu", 30, Theme.Ink), 18);
                HomeSceneMenu.Fill(lockText.rectTransform);
                lockText.rectTransform.offsetMin = new Vector2(20, 4);
                lockText.rectTransform.offsetMax = new Vector2(-20, -4);
                lockRoot.gameObject.SetActive(false);

                // thẻ chọn hệ (cuối tuần chưa chọn)
                var pick = Img(stage, "chon_he_goi_y", Sketch.Pill, paper, false, true);
                At(pick.rectTransform, Top, new Vector2(0, -PickY), new Vector2(560, 72), Mid);
                var pickText = Auto(Txt(pick.transform, "chu", 30, Theme.Ink), 18);
                HomeSceneMenu.Fill(pickText.rectTransform);
                pickText.rectTransform.offsetMin = new Vector2(20, 4);
                pickText.rectTransform.offsetMax = new Vector2(-20, -4);
                pickText.text = Loc.T("Chọn hệ boss ở hàng dưới");
                pick.gameObject.SetActive(false);

                var prev = Arrow(kit, stage, "truoc", "<", -ArrowX);
                var next = Arrow(kit, stage, "sau", ">", ArrowX);

                // ---------- dải đáy ----------
                // hàng hệ: ô nút trơn (không sọc) tô màu hệ lúc chạy, icon hệ trên đĩa kem viền mực, chữ thứ sáng viền mực (người dùng
                // 2026-11-27 chê icon mờ trên nền sọc tối)
                var tabsBg = Img(page, "hang_he", Sketch.PanelThin, new Color(0.13f, 0.11f, 0.21f, 0.92f), false, true);
                At(tabsBg.rectTransform, Bottom, new Vector2(0, TabsY), new Vector2(BandW, TabsH), Bottom);
                var tabs = new CaveScene.Tab[5];
                for (int k = 0; k < tabs.Length; k++)
                {
                    var tbg = Img(tabsBg.transform, "chon_" + k, Sketch.PanelThin, Color.white, true, true);
                    At(tbg.rectTransform, Mid, new Vector2((k - 2) * TabGap, 0), new Vector2(TabW, TabH), Mid);
                    var ic = Badge(tbg.transform, "he", new Vector2(0, 20), 96, null, 70);
                    var lb = Auto(Light(tbg.transform, "thu", 30, outline, Theme.Title), 20);
                    At(lb.rectTransform, Mid, new Vector2(0, -48), new Vector2(TabW - 14, 40), Mid);
                    var b = tbg.gameObject.AddComponent<SketchButton>();
                    b.Setup(tbg, lb, false, Sketch.PanelThin, Sketch.PanelThin, outline, null);
                    b.SetColor(Color.white);
                    tabs[k] = new CaveScene.Tab { button = b, icon = ic, label = lb };
                }
                var go = HomeSceneMenu.Button(assets, page, "vao_tang_0", Loc.T("Vượt"), BtnColor.Green, new Vector2(340, 124));
                At(go.Rect, Bottom, new Vector2(0, RowY), new Vector2(340, 124), Bottom);
                // thẻ lượt thắng còn hôm nay
                var winsBg = Img(page, "luot", Sketch.Pill, paper, false, true);
                At(winsBg.rectTransform, Bottom, new Vector2(-372, RowY + 26), new Vector2(264, 72), Bottom);
                var winsIc = Icon(winsBg.transform, "icon", Ic("fist"), 42);
                At(winsIc.rectTransform, Left, new Vector2(16, 0), new Vector2(42, 42), Left);
                var wins = Auto(Txt(winsBg.transform, "chu", 30, Theme.Ink), 18);
                wins.font = Theme.Title;
                wins.alignment = TextAlignmentOptions.MidlineLeft;
                At(wins.rectTransform, Left, new Vector2(64, 0), new Vector2(186, 48), Left);
                var ad = HomeSceneMenu.Button(assets, page, "hang_them_luot", Loc.T("+1 lượt"), BtnColor.Yellow, new Vector2(264, 100));
                At(ad.Rect, Bottom, new Vector2(-372, RowY + 12), new Vector2(264, 100), Bottom);
                ad.gameObject.SetActive(false);
                // thẻ thưởng mỗi trận thắng: "Thắng" + đá (+ đá tinh trận thắng đầu ngày ở tầng cao)
                var winBg = Img(page, "thuong_thang", Sketch.Pill, paper, false, true);
                At(winBg.rectTransform, Bottom, new Vector2(380, RowY + 26), new Vector2(296, 72), Bottom);
                var winLabel = Auto(Txt(winBg.transform, "nhan", 27, Theme.Ink2), 18);
                winLabel.alignment = TextAlignmentOptions.MidlineLeft;
                At(winLabel.rectTransform, Left, new Vector2(18, 0), new Vector2(86, 40), Left);
                winLabel.text = Loc.T("Thắng");
                var wsIc = Icon(winBg.transform, "icon_da", stoneSp, 48);
                At(wsIc.rectTransform, Left, new Vector2(100, 0), new Vector2(48, 48), Left);
                var winStones = Auto(Txt(winBg.transform, "da", 30, Theme.Ink), 18);
                winStones.font = Theme.Title;
                winStones.alignment = TextAlignmentOptions.MidlineLeft;
                At(winStones.rectTransform, Left, new Vector2(148, 0), new Vector2(60, 44), Left);
                var wcIc = Icon(winBg.transform, "icon_tinh", crystalSp, 42);
                At(wcIc.rectTransform, Left, new Vector2(206, 0), new Vector2(42, 42), Left);
                var winCrystal = Auto(Txt(winBg.transform, "tinh", 30, Theme.Ink), 18);
                winCrystal.font = Theme.Title;
                winCrystal.alignment = TextAlignmentOptions.MidlineLeft;
                At(winCrystal.rectTransform, Left, new Vector2(248, 0), new Vector2(46, 44), Left);

                scene.SetupView(view, page);
                scene.SetupBand(stage, nodes, fill.rectTransform, marker.rectTransform, headBadge.gameObject, headElem, headText, stones, crystals);
                scene.SetupTablet(tablet, floorName, passed, firstLabel, prizes, tabletTap);
                scene.SetupStage(squad, squadCg, spots, lockRoot.gameObject, lockText, pick.gameObject, swipe, prev, next);
                scene.SetupBottom(winsBg.gameObject, wins, ad, go, winBg.gameObject, winStones, wcIc.gameObject, winCrystal, tabs);
                scene.SetupIcons(stoneSp, crystalSp, evoSp);
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            RevertScene();
            // hàng tầng bản cũ (CaveTierRow đã bỏ)
            if (File.Exists(OldRowPath)) AssetDatabase.DeleteAsset(OldRowPath);
            AssetDatabase.SaveAssets();
            Debug.Log("[Hang] Đã dựng sân khấu " + ScreenPath);
        }

        // scene Cave: gỡ phần đè của bản sao prefab (các lần nướng cũ) để prefab mới hiện đúng
        static void RevertScene()
        {
            if (!File.Exists(ScenePath)) return;
            var open = SceneManager.GetSceneByPath(ScenePath);
            bool wasOpen = open.IsValid() && open.isLoaded;
            var scene = wasOpen ? open : EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Additive);
            foreach (var go in scene.GetRootGameObjects())
                if (PrefabUtility.IsPartOfPrefabInstance(go))
                    PrefabUtility.RevertPrefabInstance(PrefabUtility.GetOutermostPrefabInstanceRoot(go), InteractionMode.AutomatedAction);
            EditorSceneManager.SaveScene(scene);
            if (!wasOpen) EditorSceneManager.CloseScene(scene, true);
        }

        // ---------- chụp thử ----------

        static string ShotDir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "hang");

        static IEnumerator Wait(string id)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != id) && Time.realtimeSinceStartup - t0 < 30) yield return null;
        }

        static IEnumerator Settle(CaveScene sc, float secs, float extra)
        {
            float t0 = Time.realtimeSinceStartup;
            while (sc && !sc.SquadReady && Time.realtimeSinceStartup - t0 < secs) yield return null;
            yield return new WaitForSecondsRealtime(extra);
        }

        static void Log(StreamWriter w, string line)
        {
            w.WriteLine(line);
            w.Flush();
        }

        static IEnumerator Run()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(ShotDir);
            foreach (var f in Directory.GetFiles(ShotDir, "*.jpg")) File.Delete(f);
            var log = new StreamWriter(Path.Combine(ShotDir, "log.txt"), false, new System.Text.UTF8Encoding(false));
            var cfg = App.Data.Cfg;
            int wdIdx = -1, wdOld = 0;
            try
            {
                var s = App.Save.Data;
                s.level = Mathf.Max(s.level, 60);
                s.caveFloor = 3; // 3 tầng đã qua, tầng 4 đang chờ vượt, từ tầng 5 khoá
                int day = Afk.Today(Game.SaveService.Now());
                s.cave = new CaveDay { day = day, wins = 0, pick = Elem.Thuy };
                App.Router.Go(SceneIds.Cave);
                yield return Wait(SceneIds.Cave);
                var sc = Object.FindAnyObjectByType<CaveScene>();
                yield return Settle(sc, 8, 1.2f);
                Log(log, $"vào màn: tầng đang xem {sc.Current + 1} (đợi 4); sân khấu dời theo tai thỏ {sc.Inset:0} (Editor đợi 0)");
                yield return Shot("1_vao_hang");
                sc.JumpForTest(0);
                yield return new WaitForSecondsRealtime(0.4f);
                yield return Settle(sc, 8, 0.8f);
                yield return Shot("2_tang_da_qua");
                sc.JumpForTest(6);
                yield return new WaitForSecondsRealtime(0.4f);
                yield return Settle(sc, 8, 0.8f);
                yield return Shot("3_tang_khoa");
                sc.StepForTest(1);
                yield return new WaitForSecondsRealtime(0.25f);
                yield return Shot("4_dang_chay_ra");
                yield return Settle(sc, 8, 0.6f);
                sc.JumpForTest(3);
                yield return new WaitForSecondsRealtime(0.4f);
                yield return Settle(sc, 8, 0.6f);
                sc.DetailForTest();
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot("5_chi_tiet");
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.3f);
                // cuối tuần (giả: hôm nay thành ngày tự chọn, chưa chọn hệ): thẻ chọn hệ, cả 5 ô hệ sáng; rồi chọn Hỏa
                wdIdx = Potential.WeekdayOf(day);
                wdOld = cfg.cave.weekday[wdIdx];
                cfg.cave.weekday[wdIdx] = -1;
                s.cave = new CaveDay { day = day, wins = 0, pick = null };
                sc.Refresh();
                yield return new WaitForSecondsRealtime(0.4f);
                yield return Shot("6_cuoi_tuan_chua_chon");
                var hoa = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).FirstOrDefault(b => b.name == "chon_hoa");
                Log(log, "nút chon_hoa: " + (hoa ? "có" : "KHÔNG"));
                hoa?.SimulateClick();
                yield return new WaitForSecondsRealtime(0.4f);
                yield return Settle(sc, 8, 0.8f);
                yield return Shot("7_cuoi_tuan_chon_hoa");
                cfg.cave.weekday[wdIdx] = wdOld;
                wdIdx = -1;
                // hết lượt thắng: thẻ lượt thành nút +1 lượt (nếu có quảng cáo) hoặc "Hết lượt"
                s.cave = new CaveDay { day = day, wins = cfg.cave.winsPerDay };
                sc.JumpForTest(1);
                yield return new WaitForSecondsRealtime(0.4f);
                yield return Settle(sc, 8, 0.6f);
                yield return Shot("8_het_luot");
                // vượt tầng 4 lần đầu rồi về như vừa xong trận: rãnh vàng chạy tới tầng 5, xem tầng 5
                s.cave = new CaveDay { day = day, wins = 0 };
                var cw = Potential.WinCave(s, cfg, day, 3);
                Log(log, $"thắng tầng 4: lần đầu {cw.first}, đá {cw.Total}, đá tinh {cw.crystals}, đá tiến hóa {cw.evo}; caveFloor {s.caveFloor}");
                App.Router.Go(SceneIds.Cave, new CaveBack { tier = 3, won = true });
                yield return Wait(SceneIds.Cave);
                sc = Object.FindAnyObjectByType<CaveScene>();
                yield return new WaitForSecondsRealtime(0.55f);
                yield return Shot("9_vua_vuot_dang_chay");
                yield return Settle(sc, 8, 1.2f);
                Log(log, $"về sau khi vượt: tầng đang xem {sc.Current + 1} (đợi 5)");
                yield return Shot("10_vua_vuot_xong");
                var go = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).FirstOrDefault(b => b.name == "vao_tang_4");
                Log(log, "nút vao_tang_4: " + (go ? "có" : "KHÔNG"));
                go?.SimulateClick();
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot("11_chuan_bi_tran");
                App.Modals.CloseAll();
                Log(log, "xong");
                Debug.Log("[Thử] Xong Hang Tiềm Năng: " + Path.GetFullPath(ShotDir));
            }
            finally
            {
                if (wdIdx >= 0) cfg.cave.weekday[wdIdx] = wdOld;
                log.Dispose();
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
            var build = Flag("cave_stage_build.flag");
            if (!EditorApplication.isPlayingOrWillChangePlaymode && File.Exists(build))
            {
                File.Delete(build);
                Build();
                return;
            }
            var tour = Flag("cave_stage_tour.flag");
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
