// Dựng prefab Sổ Phép (Core/SoPhep.cs, GD_Claude/28_SoPhep.md, người dùng duyệt 2026-11-24), menu "PokiClash/Prefab/Hộp thoại và màn/Sổ Phép":
// - Items/OSoPhep (SoPhepTile): vòng chọn đứt nét, đĩa, viền, viền trong (ô chốt), icon, viên cấp, miếng nền chữ, tên, giá; ClickCatcher cả ô;
// - Dialogs/SoPhep (SoPhepDialog): biến thể tờ giấy gốc HopThoai trải kín màn như cửa hàng, phủ nền tối + chấm sao mờ (người dùng
//   2026-11-27: "nền tối thôi để nổi bật các skill tree, làm dạng cây hoặc graph toả ra nối bằng line"); đầu màn (tên, nét, đá, đã vẽ),
//   trang cuộn dọc 4 chương: băng tên chương toả đường xuống 4 ô xếp vòng cung, 4 ô hội đường về ô chốt, ô chốt nối thân cây sang băng
//   chương sau; bảng đáy tối cố định (vạch màu chương, tên ô, hiệu ứng, 5 nút mặt, giá, Gợi ý / Vẽ / Tẩy sổ); gắn vào UiKit.dialogs;
// - vá Screens/Battle: nút "Lật trang" ở đầu hàng thẻ, bên trái chip "Chọn" (BattleView.p.reroll);
// - vá App.prefab (giao diện sảnh chung LobbyDock, 2026-11-27; trước ở Screens/Hub): icon "pencil" cho thẻ công trình thứ 4 (Sổ Phép, thay chỗ Cây bi đã ẩn).
// Menu "Sổ Phép: chỉ màn sổ" (hoặc cờ Temp/sophep_build.flag) chỉ dựng hai prefab đầu, không vá Battle / Hub (nhiều phiên chung Unity).
// Chữ: tiêu đề Baloo2 Bold màu kem, chữ phụ Pangolin; không dùng chữ đen đậm làm tiêu đề (người dùng 2026-11-27).
// Sprite trắng tô màu ở 03 Art/SoPhep/ui (ArtGen/UI/so_phep/sinh_ui_toi.py).
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using static PokiClash.EditorTools.ShopMenu;

namespace PokiClash.EditorTools
{
    public static class SoPhepMenu
    {
        const string SheetBase = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string TilePath = "Assets/04 Prefabs/Items/OSoPhep.prefab";
        const string DialogPath = "Assets/04 Prefabs/Dialogs/SoPhep.prefab";
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab";
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string UiDir = "Assets/03 Art/SoPhep/ui";
        const string BoldFont = "Assets/03 Art/Fonts/Baloo2-Bold SDF.asset", BodyFont = "Assets/03 Art/Fonts/Pangolin-Regular SDF.asset";
        const float HeaderH = 210, PanelH = 470, Bleed = 30, TopPad = 30, ChapterH = 880;
        const float BannerY = -60, BannerW = 620, BannerH = 104;
        static readonly Vector2[] NodePos = { new Vector2(-390, -290), new Vector2(-130, -340), new Vector2(130, -340), new Vector2(390, -290) };
        static readonly Vector2 CapPos = new Vector2(0, -620);

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Sổ Phép", priority = 72)]
        public static void BuildAll()
        {
            BuildScreen();
            PatchBattle();
            PatchHub();
            AssetDatabase.SaveAssets();
            Debug.Log("[Sổ Phép] Đã dựng " + TilePath + ", " + DialogPath + ", vá nút Lật trang (Battle), icon Sổ Phép (Hub)");
        }

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Sổ Phép: chỉ màn sổ (OSoPhep, SoPhep)", priority = 72)]
        public static void BuildScreenOnly()
        {
            BuildScreen();
            AssetDatabase.SaveAssets();
            Debug.Log("[Sổ Phép] Đã dựng màn sổ: " + TilePath + ", " + DialogPath);
        }

        static void BuildScreen()
        {
            EnsureBorder("sp_bang.png");
            EnsureBorder("sp_bang_vien.png");
            BuildDialog(BuildTile());
        }

        // Temp/sophep_build.flag: biên dịch xong và không Play thì dựng màn sổ một lần rồi xoá cờ (Unity dùng chung nhiều phiên)
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void HookFlag() => EditorApplication.update += PollFlag;

        static void PollFlag()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            var flag = System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, "../Temp/sophep_build.flag"));
            if (!System.IO.File.Exists(flag)) return;
            System.IO.File.Delete(flag);
            BuildScreenOnly();
        }

        // ---------- tài nguyên ----------

        static Sprite UiSprite(string file) => AssetDatabase.LoadAllAssetsAtPath($"{UiDir}/{file}").OfType<Sprite>().FirstOrDefault();

        // băng bo tròn cắt 9 ô, viền 40 px
        static void EnsureBorder(string file)
        {
            var ti = AssetImporter.GetAtPath($"{UiDir}/{file}") as TextureImporter;
            if (!ti) return;
            var b = new Vector4(40, 40, 40, 40);
            if (ti.spriteBorder == b) return;
            ti.spriteBorder = b;
            ti.SaveAndReimport();
        }

        static TMP_FontAsset Font(string path) => AssetDatabase.LoadAssetAtPath<TMP_FontAsset>(path);

        // chữ theo mẫu của hộp chuẩn bị ải, đổi sang phông chỉ định (Baloo2 Bold / Pangolin), material mặc định của phông (không viền)
        static TextMeshProUGUI Txt(TextMeshProUGUI tpl, Transform parent, string name, string fontPath, float size, TextAlignmentOptions align, Color color)
        {
            var t = Text(tpl, parent, name, size, align, color);
            var f = Font(fontPath);
            if (f)
            {
                t.font = f;
                t.fontSharedMaterial = f.material;
            }
            t.fontStyle = FontStyles.Normal;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            return t;
        }

        static Image Sliced(string name, Transform parent, string file, Color c, float ppuMul = 1)
        {
            var img = Img(name, parent, UiSprite(file), c);
            img.type = Image.Type.Sliced;
            img.pixelsPerUnitMultiplier = ppuMul;
            return img;
        }

        // ---------- ô ----------

        static SoPhepTile BuildTile()
        {
            var (_, hintTpl) = Templates();
            var root = Rt("OSoPhep", null, typeof(CanvasRenderer), typeof(Image), typeof(ClickCatcher)).gameObject;
            try
            {
                var rt = (RectTransform)root.transform;
                var hit = root.GetComponent<Image>();
                hit.color = new Color(1, 1, 1, 0); // nhận chạm cả ô (đĩa và chữ)
                var sel = Img("vong_chon", rt, UiSprite("sp_vong_chon.png"), Color.white);
                var disc = Img("dia", rt, UiSprite("sp_dia.png"), SoPhepColors.DiscOpen);
                var ring = Img("vien", rt, UiSprite("sp_vong.png"), SoPhepColors.RingOpen);
                var ring2 = Img("vien_trong", rt, UiSprite("sp_vong.png"), SoPhepColors.RingOpen);
                var icon = Img("icon", rt, Icon("pencil"), Color.white);
                icon.preserveAspect = true;
                var badge = Sliced("vien_cap", rt, "sp_bang.png", SoPhepColors.Bg, 2.2f);
                var badgeRing = Sliced("vien_cap_net", rt, "sp_bang_vien.png", SoPhepColors.RingOpen, 2.2f);
                var level = Txt(hintTpl, rt, "cap", BoldFont, 22, TextAlignmentOptions.Center, SoPhepColors.Cream);
                var plate = Sliced("nen_chu", rt, "sp_bang.png", SoPhepColors.Bg, 1.4f);
                var title = Txt(hintTpl, rt, "ten", BoldFont, 30, TextAlignmentOptions.Center, SoPhepColors.Cream);
                title.enableAutoSizing = true;
                title.fontSizeMin = 22;
                title.fontSizeMax = 30;
                var sub = Txt(hintTpl, rt, "gia", BodyFont, 25, TextAlignmentOptions.Center, SoPhepColors.Muted);
                foreach (var g in root.GetComponentsInChildren<Graphic>(true))
                    if (g != hit) g.raycastTarget = false;
                var t = root.AddComponent<SoPhepTile>();
                t.Setup(disc, ring, ring2, sel, icon, badge, badgeRing, plate, title, sub, level, root.GetComponent<ClickCatcher>());
                t.SetSize(SoPhepTile.Size, false);
                sel.gameObject.SetActive(false);
                return PrefabUtility.SaveAsPrefabAsset(root, TilePath).GetComponent<SoPhepTile>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- màn ----------

        static void BuildDialog(SoPhepTile tilePrefab)
        {
            var kit = Kit;
            var (_, hintTpl) = Templates();
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "SoPhep";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(1080, false, true);
                var sheet = view.Sheet;
                foreach (var f in sheet.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(f);
                foreach (var l in sheet.GetComponents<LayoutGroup>()) Object.DestroyImmediate(l);
                sheet.anchorMin = Vector2.zero;
                sheet.anchorMax = Vector2.one;
                sheet.pivot = new Vector2(0.5f, 0.5f);
                sheet.offsetMin = new Vector2(-Bleed, -Bleed);
                sheet.offsetMax = new Vector2(Bleed, Bleed);
                view.SetFlat(true);
                var tape = sheet.Find("bang_keo");
                if (tape) tape.gameObject.SetActive(false);
                var page = Rt("noi_dung", sheet);
                page.Stretch(Bleed, Bleed, Bleed, Bleed);
                page.SetAsLastSibling();
                // nền tối phủ tờ giấy, chấm sao mờ lát lặp
                var dark = Img("nen_toi", page, null, SoPhepColors.Bg);
                dark.rectTransform.Stretch(-Bleed, -Bleed, -Bleed, -Bleed);
                var dots = Img("cham_sao", page, UiSprite("sp_cham.png"), SoPhepColors.Dots);
                dots.type = Image.Type.Tiled;
                dots.rectTransform.Stretch(-Bleed, -Bleed, -Bleed, -Bleed);
                var body = Rt("an_toan", page, typeof(SafeArea));
                body.Stretch();
                var cr = (RectTransform)view.Close.transform;
                cr.anchorMin = cr.anchorMax = new Vector2(1, 1);
                cr.pivot = new Vector2(0.5f, 0.5f);
                cr.anchoredPosition = new Vector2(-Bleed - 64, -Bleed - 70);

                // đầu màn
                var title = Txt(hintTpl, body, "tieu_de", BoldFont, 58, TextAlignmentOptions.MidlineLeft, SoPhepColors.Cream);
                title.rectTransform.Place(new Vector2(0, 1), new Vector2(44, -14), new Vector2(600, 110), new Vector2(0, 1));
                title.text = "Sổ Phép";
                var points = Chip(body, hintTpl, "net", new Vector2(44, -128), 250, Icon("pencil"));
                var stones = Chip(body, hintTpl, "da", new Vector2(310, -128), 340, Icon("shard"));
                var progress = Txt(hintTpl, body, "da_ve", BodyFont, 28, TextAlignmentOptions.MidlineRight, SoPhepColors.Muted);
                progress.rectTransform.Place(new Vector2(1, 1), new Vector2(-40, -128), new Vector2(360, 64), new Vector2(1, 1));

                // trang cuộn
                var scrollGo = Rt("cuon", body, typeof(CanvasRenderer), typeof(Image), typeof(ScrollRect)).gameObject;
                var srt = (RectTransform)scrollGo.transform;
                srt.Stretch(0, HeaderH, 0, PanelH);
                scrollGo.GetComponent<Image>().color = new Color(1, 1, 1, 0);
                var scroll = scrollGo.GetComponent<ScrollRect>();
                scroll.horizontal = false;
                scroll.vertical = true;
                scroll.movementType = ScrollRect.MovementType.Elastic;
                scroll.scrollSensitivity = 30;
                var viewport = Rt("khung", scrollGo.transform, typeof(RectMask2D));
                viewport.Stretch();
                var content = Rt("trang", viewport);
                content.anchorMin = new Vector2(0, 1);
                content.anchorMax = new Vector2(1, 1);
                content.pivot = new Vector2(0.5f, 1);
                content.anchoredPosition = Vector2.zero;
                content.sizeDelta = new Vector2(0, TopPad + SoPhepDialog.Chapters * ChapterH);
                scroll.viewport = viewport;
                scroll.content = content;

                int n = SoPhepDialog.Chapters, per = SoPhepDialog.PerChapter, lpc = SoPhepDialog.LinesPerChapter;
                var chLabels = new TextMeshProUGUI[n];
                var chTitles = new TextMeshProUGUI[n];
                var chNeeds = new TextMeshProUGUI[n];
                var chRims = new Image[n];
                var chGroups = new CanvasGroup[n];
                var tiles = new SoPhepTile[n * per];
                var lines = new Image[n * lpc];
                var bannerBottom = new Vector2(0, BannerY - BannerH / 2 + 4);
                for (int ch = 0; ch < n; ch++)
                {
                    var block = Rt("chuong_" + (ch + 1), content);
                    block.anchorMin = new Vector2(0, 1);
                    block.anchorMax = new Vector2(1, 1);
                    block.pivot = new Vector2(0.5f, 1);
                    block.anchoredPosition = new Vector2(0, -TopPad - ch * ChapterH);
                    block.sizeDelta = new Vector2(0, ChapterH);
                    var group = Rt("o_chuong", block, typeof(CanvasGroup));
                    group.Stretch();
                    // đường trước (nằm dưới ô và băng): băng → 4 ô, 4 ô → ô chốt, ô chốt → băng chương sau
                    for (int j = 0; j < per - 1; j++)
                    {
                        lines[ch * lpc + j] = Line(group, "duong_toa_" + (j + 1), bannerBottom, NodePos[j]);
                        lines[ch * lpc + per - 1 + j] = Line(group, "duong_hoi_" + (j + 1), NodePos[j], CapPos);
                    }
                    var trunk = Line(group, "than_cay", CapPos, new Vector2(0, -ChapterH + BannerY + BannerH / 2 - 4));
                    trunk.gameObject.SetActive(ch + 1 < n);
                    lines[ch * lpc + lpc - 1] = trunk;

                    // ô: 4 ô thường xếp vòng cung, ô chốt to ở dưới
                    for (int j = 0; j < per; j++)
                    {
                        var t = ((GameObject)PrefabUtility.InstantiatePrefab(tilePrefab.gameObject, group)).GetComponent<SoPhepTile>();
                        bool cap = j == per - 1;
                        t.name = cap ? "o_chot" : "o_" + (j + 1);
                        t.SetSize(cap ? SoPhepTile.CapSize : SoPhepTile.Size, cap);
                        var r = t.Rect;
                        r.anchorMin = r.anchorMax = new Vector2(0.5f, 1);
                        r.anchoredPosition = cap ? CapPos : NodePos[j];
                        tiles[ch * per + j] = t;
                    }

                    // băng tên chương (trên đầu các đường)
                    var banner = Sliced("bang_chuong", block, "sp_bang.png", SoPhepColors.Plate);
                    banner.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, BannerY), new Vector2(BannerW, BannerH), new Vector2(0.5f, 0.5f));
                    var rim = Sliced("vien", banner.transform, "sp_bang_vien.png", SoPhepColors.Chapter(ch));
                    rim.rectTransform.Stretch();
                    var lab = Txt(hintTpl, banner.transform, "so_chuong", BoldFont, 24, TextAlignmentOptions.Center, SoPhepColors.Chapter(ch));
                    lab.characterSpacing = 12;
                    lab.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 20), new Vector2(BannerW - 60, 34));
                    var ct = Txt(hintTpl, banner.transform, "ten_chuong", BoldFont, 38, TextAlignmentOptions.Center, SoPhepColors.Cream);
                    ct.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -14), new Vector2(BannerW - 60, 50));
                    var need = Txt(hintTpl, block, "dieu_kien", BodyFont, 27, TextAlignmentOptions.Center, SoPhepColors.Coral);
                    need.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, BannerY - BannerH / 2 - 30), new Vector2(900, 40), new Vector2(0.5f, 0.5f));

                    chLabels[ch] = lab;
                    chTitles[ch] = ct;
                    chNeeds[ch] = need;
                    chRims[ch] = rim;
                    chGroups[ch] = group.GetComponent<CanvasGroup>();
                }

                // bảng đáy cố định
                var panel = Img("bang_day", body, null, SoPhepColors.Panel);
                var prt = panel.rectTransform;
                prt.anchorMin = new Vector2(0, 0);
                prt.anchorMax = new Vector2(1, 0);
                prt.pivot = new Vector2(0.5f, 0);
                prt.offsetMin = new Vector2(-Bleed, -Bleed);
                prt.offsetMax = new Vector2(Bleed, PanelH);
                var panelRim = Img("vach_mau", prt, UiSprite("sp_net.png"), SoPhepColors.Gold);
                panelRim.rectTransform.anchorMin = new Vector2(0, 1);
                panelRim.rectTransform.anchorMax = new Vector2(1, 1);
                panelRim.rectTransform.pivot = new Vector2(0.5f, 0.5f);
                panelRim.rectTransform.anchoredPosition = Vector2.zero;
                panelRim.rectTransform.sizeDelta = new Vector2(0, 12);
                var inner = Rt("noi_dung_bang", prt);
                inner.Stretch(Bleed, 0, Bleed, Bleed);
                var selName = Txt(hintTpl, inner, "ten_o", BoldFont, 46, TextAlignmentOptions.MidlineLeft, SoPhepColors.Cream);
                selName.rectTransform.Place(new Vector2(0, 1), new Vector2(40, -22), new Vector2(1000, 62), new Vector2(0, 1));
                var selDesc = Txt(hintTpl, inner, "hieu_ung", BodyFont, 31, TextAlignmentOptions.TopLeft, SoPhepColors.Soft);
                selDesc.rectTransform.Place(new Vector2(0, 1), new Vector2(40, -90), new Vector2(1000, 110), new Vector2(0, 1));
                selDesc.textWrappingMode = TextWrappingModes.Normal;
                selDesc.enableAutoSizing = true;
                selDesc.fontSizeMin = 22;
                selDesc.fontSizeMax = 31;
                var facesRow = Rt("mat", inner, typeof(HorizontalLayoutGroup));
                facesRow.Place(new Vector2(0.5f, 1), new Vector2(0, -206), new Vector2(1000, 76), new Vector2(0.5f, 1));
                var hl = facesRow.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = 10;
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var faces = new SketchButton[SoPhepDialog.MaxFaces];
                for (int i = 0; i < faces.Length; i++)
                {
                    var b = Ui.Spawn(kit.buttonSmall, facesRow);
                    b.name = "mat_" + i;
                    b.Rect.sizeDelta = new Vector2(186, b.Rect.sizeDelta.y);
                    b.SetText("");
                    b.SetRole(BtnColor.Paper);
                    faces[i] = b;
                }
                var selCost = Txt(hintTpl, inner, "gia", BodyFont, 32, TextAlignmentOptions.Center, SoPhepColors.Gold);
                selCost.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -292), new Vector2(980, 48), new Vector2(0.5f, 1));
                selCost.enableAutoSizing = true;
                selCost.fontSizeMin = 22;
                selCost.fontSizeMax = 32;
                var suggest = Ui.Spawn(kit.buttonSmall, inner);
                suggest.name = "nut_goi_y";
                suggest.Rect.Place(new Vector2(0, 0), new Vector2(34, 30), new Vector2(220, suggest.Rect.sizeDelta.y), new Vector2(0, 0));
                suggest.SetRole(BtnColor.Paper);
                suggest.SetText("Gợi ý");
                var draw = Ui.Spawn(kit.buttonNormal, inner);
                draw.name = "nut_ve";
                draw.Rect.Place(new Vector2(0.5f, 0), new Vector2(0, 24), new Vector2(340, draw.Rect.sizeDelta.y), new Vector2(0.5f, 0));
                draw.SetRole(BtnColor.Green);
                draw.SetText("Vẽ");
                var reset = Ui.Spawn(kit.buttonSmall, inner);
                reset.name = "nut_tay_so";
                reset.Rect.Place(new Vector2(1, 0), new Vector2(-34, 30), new Vector2(220, reset.Rect.sizeDelta.y), new Vector2(1, 0));
                reset.SetRole(BtnColor.Red);
                reset.SetText("Tẩy sổ");

                view.Close.transform.SetAsLastSibling();
                var dlgComp = root.AddComponent<SoPhepDialog>();
                dlgComp.Setup(new SoPhepDialog.Parts
                {
                    points = points, stones = stones, progress = progress, scroll = scroll, chapterLabels = chLabels, chapterTitles = chTitles,
                    chapterNeeds = chNeeds, chapterRims = chRims, chapterGroups = chGroups, tiles = tiles, lines = lines, panelRim = panelRim,
                    selName = selName, selDesc = selDesc, selCost = selCost, faces = faces, draw = draw, suggest = suggest, reset = reset,
                    icons = NodeIcons(),
                });
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, DialogPath).GetComponent<SoPhepDialog>();
                kit.dialogs.RemoveAll(x => !x || (x is SoPhepDialog && x != dlg));
                if (!kit.dialogs.Contains(dlg)) kit.dialogs.Add(dlg);
                EditorUtility.SetDirty(kit);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // icon vẽ riêng của từng ô theo thứ tự ô trong balance.json (03 Art/SoPhep/<id>.png, gen bằng GPT qua Magnific: ArtGen/UI/so_phep)
        static Sprite[] NodeIcons()
        {
            var json = System.IO.File.ReadAllText(System.IO.Path.Combine(Application.dataPath, "02 Data/Json/balance.json"));
            var cfg = PokiClash.Core.BalanceConfig.FromJson(PokiClash.Core.J.Obj(PokiClash.Core.MiniJson.Parse(json)));
            return cfg.sophep.nodes.Select(n => AssetDatabase.LoadAllAssetsAtPath($"Assets/03 Art/SoPhep/{n.id}.png").OfType<Sprite>().FirstOrDefault()).ToArray();
        }

        // ô số liệu nhỏ ở đầu màn: viên tối, icon, chữ kem
        static TextMeshProUGUI Chip(RectTransform parent, TextMeshProUGUI tpl, string name, Vector2 pos, float w, Sprite icon)
        {
            var chip = Sliced(name, parent, "sp_bang.png", SoPhepColors.Plate, 1.6f);
            chip.rectTransform.Place(new Vector2(0, 1), pos, new Vector2(w, 64), new Vector2(0, 1));
            var ic = Img("icon", chip.transform, icon, Color.white);
            ic.preserveAspect = true;
            ic.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(10, 0), new Vector2(50, 50), new Vector2(0, 0.5f));
            var t = Txt(tpl, chip.transform, "so", BoldFont, 30, TextAlignmentOptions.MidlineLeft, SoPhepColors.Cream);
            t.rectTransform.Stretch(68, 2, 16, 2);
            return t;
        }

        // đường nối hai điểm (toạ độ trong khối chương, gốc giữa trên): dải mép mềm sp_net, màu do SoPhepDialog tô theo trạng thái
        static Image Line(RectTransform parent, string name, Vector2 a, Vector2 b)
        {
            var img = Img(name, parent, UiSprite("sp_net.png"), SoPhepColors.LineOpen);
            var rt = img.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 1);
            rt.pivot = new Vector2(0.5f, 0.5f);
            var d = b - a;
            rt.anchoredPosition = (a + b) / 2;
            rt.sizeDelta = new Vector2(d.magnitude, 12);
            rt.localEulerAngles = new Vector3(0, 0, Mathf.Atan2(d.y, d.x) * Mathf.Rad2Deg);
            return img;
        }

        static void PatchBattle()
        {
            var kit = Kit;
            var contents = PrefabUtility.LoadPrefabContents(BattlePath);
            try
            {
                var view = contents.GetComponentInChildren<BattleView>(true);
                var so = new SerializedObject(view);
                var qCount = (TextMeshProUGUI)so.FindProperty("p.qCount").objectReferenceValue;
                var qHead = (RectTransform)so.FindProperty("p.qHead").objectReferenceValue;
                if (!qCount || !qHead)
                {
                    Debug.LogError("[Sổ Phép] Không thấy p.qCount / p.qHead trong " + BattlePath);
                    return;
                }
                var old = qHead.Find("nut_lat_trang");
                if (old) Object.DestroyImmediate(old.gameObject);
                // chip "Chọn" có thể là chữ trong một viên: lấy khung ngoài cùng nằm trong qHead
                RectTransform chip = qCount.rectTransform;
                while (chip.parent && chip.parent != qHead) chip = (RectTransform)chip.parent;
                var btn = Ui.Spawn(kit.buttonSmall, qHead);
                btn.name = "nut_lat_trang";
                var brt = btn.Rect;
                brt.anchorMin = chip.anchorMin;
                brt.anchorMax = chip.anchorMax;
                brt.pivot = new Vector2(1, 0.5f);
                float left = chip.anchoredPosition.x - chip.rect.width * chip.pivot.x;
                float midY = chip.anchoredPosition.y + chip.rect.height * (0.5f - chip.pivot.y);
                brt.sizeDelta = new Vector2(250, Mathf.Max(56, chip.rect.height + 4));
                brt.anchoredPosition = new Vector2(left - 14, midY);
                btn.SetRole(BtnColor.Orange);
                btn.SetText("Lật trang ×1");
                btn.gameObject.SetActive(false);
                so.FindProperty("p.reroll").objectReferenceValue = btn;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, BattlePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // thẻ công trình nằm trong App.prefab (giao diện sảnh chung LobbyDock, 2026-11-27)
        static void PatchHub()
        {
            var contents = PrefabUtility.LoadPrefabContents(LobbyDockMenu.AppPath);
            try
            {
                var hub = contents.GetComponentInChildren<LobbyDock>(true);
                if (!hub)
                {
                    Debug.LogError("[Sổ Phép] App.prefab chưa có LobbyDock (menu \"Sảnh chung: dời ...\")");
                    return;
                }
                var so = new SerializedObject(hub);
                var arr = so.FindProperty("buildings");
                if (arr == null || arr.arraySize < 4)
                {
                    Debug.LogError("[Sổ Phép] Hub không có đủ 4 thẻ công trình");
                    return;
                }
                var b = (HubBuilding)arr.GetArrayElementAtIndex(3).objectReferenceValue;
                if (!b) return;
                if (b.Badge) return; // thẻ đã thành huy hiệu (menu "Nút sảnh: huy hiệu", 2026-11-27): giữ ảnh huy hiệu
                b.SetIcon(Icon("pencil"));
                EditorUtility.SetDirty(b);
                PrefabUtility.SaveAsPrefabAsset(contents, LobbyDockMenu.AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
