// Popup gọn (người dùng dặn 2026-11-03: popup ít chữ, nhiều hình; thưởng rõ cái gì, bao nhiêu, độ hiếm; lực chiến từng tướng rõ;
// màn Tướng có đội hình 3 con ở trên). Menu "PokiClash/Prefab/Popup gọn (ô thưởng, đội hình, lực chiến)" dựng (chạy lại thì dựng lại):
// - Items/OThuong (RewardTile): ô thưởng 150 × 190: khung giấy, dải độ hiếm, hình, góc, số lượng, nhãn, tên;
// - Items/DoiThu: viên lực chiến trên đầu đối thủ (PrepFoe.power);
// - Dialogs/ChuanBiTran: dòng "luc_chien" sau khung đối thủ (địch / mức khó / đội bạn), gán ô thưởng;
// - Dialogs/MoRuong, RuongDao: gán ô thưởng (RuongDao: hàng thẻ canh giữa, cao một ô); TranKetQua: hàng "thuong" trước dòng lời khuyên;
// - Items/TheTuong: viên lực chiến cạnh hàng sao (sao thu nhỏ, dời trái);
// - Screens/Heroes: khung "doi_hinh" (TeamLineup) đầu màn, khung cuộn lưới tướng dời xuống dưới.
// "In cây prefab popup" ghi cây RectTransform của các prefab này vào Temp/PopupDump.txt để soát.
using System.IO;
using System.Text;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class PopupUiMenu
    {
        const string TilePath = "Assets/04 Prefabs/Items/OThuong.prefab";
        const string FoePath = "Assets/04 Prefabs/Items/DoiThu.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const string ChestPath = "Assets/04 Prefabs/Dialogs/MoRuong.prefab";
        const string ZoneChestPath = "Assets/04 Prefabs/Dialogs/RuongDao.prefab";
        const string ResultPath = "Assets/04 Prefabs/Dialogs/TranKetQua.prefab";
        const string HeroTilePath = "Assets/04 Prefabs/Items/TheTuong.prefab";
        const string HeroesPath = "Assets/04 Prefabs/Screens/Heroes.prefab";

        // chiều cao khung đội hình đầu màn Tướng
        const float LineupH = 790;

        static ArtLibrary art;

        static Sprite Icon(string n) => art ? art.Icon(n) : null;

        [MenuItem("PokiClash/Prefab/Popup gọn (ô thưởng, đội hình, lực chiến)", priority = 66)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            art = Load<ArtLibrary>();
            Theme.Init(assets); // phông, sprite giấy, viền chữ nướng sẵn
            var kit = assets.prefabs;
            var tile = BuildTile(kit);
            Edit(FoePath, PatchFoe);
            TeamPickerDialog picker = null;
            Edit(PrepPath, root => picker = PatchPrep(root, tile));
            Edit(ChestPath, root => SetRef(root.GetComponent<ChestDialog>(), "tilePrefab", tile));
            Edit(ZoneChestPath, root => PatchZoneChest(root, tile));
            Edit(ResultPath, root => PatchResult(root, tile));
            Edit(HeroTilePath, PatchHeroTile);
            Edit(HeroesPath, root => PatchHeroes(root, kit, picker));
            AssetDatabase.SaveAssets();
            Debug.Log($"[Popup] Đã dựng {TilePath} và sửa DoiThu, ChuanBiTran, MoRuong, RuongDao, TranKetQua, TheTuong, Heroes.");
        }

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));

        static void Edit(string path, System.Action<GameObject> patch)
        {
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                patch(root);
                PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static void SetRef(Object target, string prop, Object value)
        {
            var so = new SerializedObject(target);
            so.FindProperty(prop).objectReferenceValue = value;
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        static Transform Find(Transform t, string name)
        {
            foreach (var c in t.GetComponentsInChildren<Transform>(true))
                if (c.name == name) return c;
            return null;
        }

        // xoá con tên name (dựng lại thì không nhân đôi)
        static void Remove(Transform parent, string name)
        {
            for (int i = parent.childCount - 1; i >= 0; i--)
                if (parent.GetChild(i).name == name) Object.DestroyImmediate(parent.GetChild(i).gameObject);
        }

        static RectTransform Node(Transform parent, string name, params System.Type[] comps)
        {
            var go = new GameObject(name, typeof(RectTransform));
            foreach (var c in comps) go.AddComponent(c);
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        static Image Img(Transform parent, string name, Sprite sprite, Color color, bool sliced = false)
        {
            var img = Node(parent, name, typeof(Image)).GetComponent<Image>();
            Theme.SetSprite(img, sprite);
            img.type = sliced ? Image.Type.Sliced : Image.Type.Simple;
            img.preserveAspect = !sliced;
            img.color = color;
            img.raycastTarget = false;
            return img;
        }

        // vùng nhận chạm trong suốt
        static Image Hit(GameObject go)
        {
            var img = go.GetComponent<Image>();
            if (!img) img = go.AddComponent<Image>();
            img.sprite = null;
            img.color = new Color(1, 1, 1, 0);
            img.raycastTarget = true;
            return img;
        }

        // outline: độ dày viền mực (0,2..0,32, theo material nướng sẵn), 0 là không viền
        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, TextAlignmentOptions align,
            float outline = 0)
        {
            var t = Node(parent, name, typeof(TextMeshProUGUI)).GetComponent<TextMeshProUGUI>();
            t.font = font;
            if (outline > 0)
            {
                var m = Theme.Outlined(font, outline);
                if (m) t.fontSharedMaterial = m;
            }
            t.fontSize = size;
            t.color = color;
            t.alignment = align;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = "";
            return t;
        }

        static HeroPortrait Portrait(UiKit kit, Transform parent, string name)
        {
            var p = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, parent)).GetComponent<HeroPortrait>();
            p.name = name;
            return p;
        }

        // viên "icon + số" xếp ngang, tự co theo số (HorizontalLayoutGroup + ContentSizeFitter); trả chữ số
        static TextMeshProUGUI IconNumber(Transform parent, string name, string icon, float iconSize, float fontSize, Color color, Sprite bg,
            out RectTransform row)
        {
            row = Node(parent, name, typeof(HorizontalLayoutGroup), typeof(ContentSizeFitter));
            if (bg)
            {
                var img = row.gameObject.AddComponent<Image>();
                Theme.SetSprite(img, bg);
                img.type = Image.Type.Sliced;
                img.color = Theme.CardFill;
                img.raycastTarget = false;
            }
            var hl = row.GetComponent<HorizontalLayoutGroup>();
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.spacing = 6;
            hl.padding = bg ? new RectOffset(10, 16, 2, 2) : new RectOffset(0, 0, 0, 0);
            hl.childControlWidth = hl.childControlHeight = true;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            var fit = row.GetComponent<ContentSizeFitter>();
            fit.horizontalFit = ContentSizeFitter.FitMode.PreferredSize;
            var ic = Img(row, "icon", Icon(icon), Color.white);
            var le = ic.gameObject.AddComponent<LayoutElement>();
            le.preferredWidth = le.preferredHeight = iconSize;
            var t = Text(row, "so", Theme.Title, fontSize, color, TextAlignmentOptions.MidlineLeft);
            t.text = "0";
            return t;
        }

        // ---------- ô thưởng ----------

        static RewardTile BuildTile(UiKit kit)
        {
            var root = new GameObject("o_thuong", typeof(RectTransform), typeof(LayoutElement), typeof(RewardTile));
            try
            {
                var rt = (RectTransform)root.transform;
                rt.sizeDelta = new Vector2(RewardTile.W, RewardTile.H);
                var le = root.GetComponent<LayoutElement>();
                le.preferredWidth = RewardTile.W;
                le.preferredHeight = RewardTile.H;

                var frame = Img(root.transform, "khung", Sketch.PanelThin, Theme.CardFill, true);
                frame.rectTransform.Place(new Vector2(0.5f, 1), Vector2.zero, new Vector2(RewardTile.Frame, RewardTile.Frame), new Vector2(0.5f, 1));
                var band = Img(frame.transform, "dai", Sketch.BarFill, Theme.Paper3, true);
                var br = band.rectTransform;
                br.anchorMin = new Vector2(0, 1);
                br.anchorMax = new Vector2(1, 1);
                br.pivot = new Vector2(0.5f, 1);
                br.anchoredPosition = new Vector2(0, -7);
                br.sizeDelta = new Vector2(-16, 30);
                var bandText = Text(band.transform, "chu", Theme.Title, 18, Color.white, TextAlignmentOptions.Center, 0.22f);
                bandText.rectTransform.Stretch(0, 0, 0, 2);
                var icon = Img(frame.transform, "hinh", Icon("ball"), Color.white);
                icon.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -10), new Vector2(92, 92));
                var hero = Portrait(kit, frame.transform, "tuong");
                hero.Rect.anchorMin = hero.Rect.anchorMax = new Vector2(0.5f, 0);
                hero.Rect.anchoredPosition = new Vector2(0, 4);
                var owner = Portrait(kit, frame.transform, "chu_the");
                owner.Rect.anchorMin = owner.Rect.anchorMax = new Vector2(0, 0);
                owner.Rect.anchoredPosition = new Vector2(30, 2);
                var corner = Img(frame.transform, "goc", Icon("shard"), Color.white);
                corner.rectTransform.Place(new Vector2(1, 1), new Vector2(-6, -40), new Vector2(40, 40), new Vector2(1, 1));
                var count = Text(frame.transform, "so", Theme.Title, 36, Color.white, TextAlignmentOptions.BottomRight, 0.3f);
                count.rectTransform.Place(new Vector2(1, 0), new Vector2(-10, 2), new Vector2(136, 48), new Vector2(1, 0));
                count.text = "×1";

                // nhãn trên mép khung (không che dải độ hiếm), tự co theo chữ
                var tagBg = Img(root.transform, "nhan", Sketch.Pill, Theme.Paper2, true);
                tagBg.rectTransform.Place(new Vector2(0, 1), new Vector2(-8, 24), new Vector2(80, 34), new Vector2(0, 1));
                var thl = tagBg.gameObject.AddComponent<HorizontalLayoutGroup>();
                thl.padding = new RectOffset(12, 12, 0, 2);
                thl.childAlignment = TextAnchor.MiddleCenter;
                thl.childControlWidth = thl.childControlHeight = true;
                thl.childForceExpandWidth = thl.childForceExpandHeight = false;
                tagBg.gameObject.AddComponent<ContentSizeFitter>().horizontalFit = ContentSizeFitter.FitMode.PreferredSize;
                var tag = Text(tagBg.transform, "chu", Theme.Title, 20, Theme.Ink, TextAlignmentOptions.Center);

                var caption = Text(root.transform, "ten", Theme.Title, 24, Theme.Ink, TextAlignmentOptions.Center);
                caption.rectTransform.Place(new Vector2(0.5f, 0), Vector2.zero, new Vector2(RewardTile.W + 16, 36), new Vector2(0.5f, 0));
                caption.enableAutoSizing = true;
                caption.fontSizeMin = 16;
                caption.fontSizeMax = 24;
                caption.overflowMode = TextOverflowModes.Ellipsis;

                root.GetComponent<RewardTile>().Setup(new RewardTile.Parts
                {
                    frame = frame, band = band, icon = icon, corner = corner, tagBg = tagBg, hero = hero, owner = owner,
                    bandText = bandText, count = count, tag = tag, caption = caption,
                });
                return PrefabUtility.SaveAsPrefabAsset(root, TilePath).GetComponent<RewardTile>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- hộp Chuẩn bị trận ----------

        // viên lực chiến cạnh nhãn hệ, dưới tên (cấp gộp vào tên, chữ cấp riêng ẩn lúc chạy); nhãn hệ dời trái nhường chỗ; cả hai nằm
        // trên hàng chỉ số (PrepFoe.StatsH, menu "Hộp chuẩn bị: chỉ số địch")
        static void PatchFoe(GameObject root)
        {
            var so = new SerializedObject(root.GetComponent<PrepFoe>());
            ((UiElemTag)so.FindProperty("elem").objectReferenceValue).Rect.anchoredPosition = new Vector2(-62, 40 + PrepFoe.StatsH);
            Remove(root.transform, "luc_chien");
            var num = IconNumber(root.transform, "luc_chien", "sword", 28, 28, Theme.RedD, Sketch.Pill, out var row);
            row.anchorMin = row.anchorMax = new Vector2(0.5f, 0);
            row.pivot = new Vector2(0, 0);
            row.anchoredPosition = new Vector2(-14, 37 + PrepFoe.StatsH);
            row.sizeDelta = new Vector2(140, 38);
            so.FindProperty("power").objectReferenceValue = num;
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        // dòng lực chiến sau khung đối thủ: [đầu lâu] số địch · nhãn mức khó · số đội bạn [đội]; gán ô thưởng; trả hộp chọn đội
        static TeamPickerDialog PatchPrep(GameObject root, RewardTile tile)
        {
            var dlg = root.GetComponent<StagePrepDialog>();
            var foes = Find(root.transform, "doi_thu");
            var body = foes.parent;
            Remove(body, "luc_chien");
            var row = Img(body, "luc_chien", Sketch.PanelThin, Theme.Hex("#fff8e8"), true);
            row.transform.SetSiblingIndex(foes.GetSiblingIndex() + 1);
            row.gameObject.AddComponent<LayoutElement>().preferredHeight = 100;

            var skull = Img(row.transform, "dich", Icon("skull"), Color.white);
            skull.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(26, 0), new Vector2(60, 60), new Vector2(0, 0.5f));
            var foe = Text(row.transform, "so_dich", Theme.Title, 48, Theme.RedD, TextAlignmentOptions.MidlineLeft);
            foe.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(96, 2), new Vector2(240, 76), new Vector2(0, 0.5f));
            foe.text = "0";
            var team = Img(row.transform, "doi", Icon("team"), Color.white);
            team.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-26, 0), new Vector2(60, 60), new Vector2(1, 0.5f));
            var mine = Text(row.transform, "so_doi", Theme.Title, 48, Theme.GreenD, TextAlignmentOptions.MidlineRight);
            mine.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-96, 2), new Vector2(240, 76), new Vector2(1, 0.5f));
            mine.text = "0";
            var pill = Img(row.transform, "muc_kho", Sketch.Pill, Theme.Yellow, true);
            pill.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(190, 64));
            var verdict = Text(pill.transform, "chu", Theme.Title, 34, Color.white, TextAlignmentOptions.Center, 0.28f);
            verdict.rectTransform.Stretch(8, 0, 8, 4);
            verdict.text = "Vừa";

            var so = new SerializedObject(dlg);
            so.FindProperty("tilePrefab").objectReferenceValue = tile;
            so.FindProperty("power.root").objectReferenceValue = row.gameObject;
            so.FindProperty("power.foe").objectReferenceValue = foe;
            so.FindProperty("power.mine").objectReferenceValue = mine;
            so.FindProperty("power.verdict").objectReferenceValue = verdict;
            so.FindProperty("power.verdictBg").objectReferenceValue = pill;
            so.ApplyModifiedPropertiesWithoutUndo();
            return (TeamPickerDialog)so.FindProperty("pickerPrefab").objectReferenceValue;
        }

        // ---------- rương mốc đảo, kết quả trận ----------

        static void PatchZoneChest(GameObject root, RewardTile tile)
        {
            var dlg = root.GetComponent<ZoneChestDialog>();
            var so = new SerializedObject(dlg);
            so.FindProperty("tilePrefab").objectReferenceValue = tile;
            so.ApplyModifiedPropertiesWithoutUndo();
            // hàng thẻ: ô canh giữa, không giãn
            var row = (RectTransform)so.FindProperty("cards").objectReferenceValue;
            var hl = row.GetComponent<HorizontalLayoutGroup>();
            hl.spacing = 18;
            hl.childAlignment = TextAnchor.UpperCenter;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            row.GetComponent<LayoutElement>().preferredHeight = RewardTile.H;
        }

        static void PatchResult(GameObject root, RewardTile tile)
        {
            var dlg = root.GetComponent<BattleResultDialog>();
            var so = new SerializedObject(dlg);
            var tips = (TextMeshProUGUI)so.FindProperty("tips").objectReferenceValue;
            var body = tips.transform.parent;
            Remove(body, "thuong");
            var row = Node(body, "thuong", typeof(HorizontalLayoutGroup), typeof(LayoutElement));
            row.SetSiblingIndex(tips.transform.GetSiblingIndex());
            var hl = row.GetComponent<HorizontalLayoutGroup>();
            hl.spacing = 18;
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = false;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            row.GetComponent<LayoutElement>().preferredHeight = RewardTile.H + 10;
            row.gameObject.SetActive(false);
            so.FindProperty("tilePrefab").objectReferenceValue = tile;
            so.FindProperty("tileRow").objectReferenceValue = row;
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        // ---------- thẻ tướng: lực chiến cạnh hàng sao ----------

        static void PatchHeroTile(GameObject root)
        {
            var so = new SerializedObject(root.GetComponent<HeroTile>());
            var stars = (UiStars)so.FindProperty("p.stars").objectReferenceValue;
            var card = stars.transform.parent;
            // sao thu nhỏ, sang trái; lực chiến bên phải cùng hàng (đáy thẻ, y = 30)
            stars.Rect.anchoredPosition = new Vector2(-70, 30);
            stars.transform.localScale = Vector3.one * 0.82f;
            Remove(card, "luc_chien");
            var num = IconNumber(card, "luc_chien", "sword", 30, 30, Theme.RedD, null, out var row);
            row.anchorMin = row.anchorMax = new Vector2(0.5f, 0);
            row.pivot = new Vector2(0.5f, 0);
            row.anchoredPosition = new Vector2(76, 28);
            row.sizeDelta = new Vector2(130, 40);
            so.FindProperty("p.power").objectReferenceValue = num;
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        // ---------- màn Tướng: đội hình ----------

        static void PatchHeroes(GameObject root, UiKit kit, TeamPickerDialog picker)
        {
            var content = Find(root.transform, "Noi dung");
            var scroll = (RectTransform)Find(content, "cuon");
            Remove(content, "doi_hinh");
            scroll.Stretch(0, LineupH, 0, 0);

            var lineup = Node(content, "doi_hinh", typeof(TeamLineup));
            lineup.SetSiblingIndex(0);
            lineup.anchorMin = new Vector2(0, 1);
            lineup.anchorMax = new Vector2(1, 1);
            lineup.pivot = new Vector2(0.5f, 1);
            lineup.anchoredPosition = Vector2.zero;
            lineup.sizeDelta = new Vector2(0, LineupH);
            Hit(lineup.gameObject); // vùng vuốt
            var bg = Img(lineup, "nen", Sketch.Panel, Theme.Hex("#f6ead0"), true);
            bg.rectTransform.Stretch(24, 10, 24, 6);
            var tape = Img(lineup, "bang_keo", Sketch.Tape, Theme.TapeYellow);
            tape.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, 2), new Vector2(170, 44), new Vector2(0.5f, 1));
            tape.rectTransform.localEulerAngles = new Vector3(0, 0, 357);

            // đầu khung: tên, lực chiến cả đội, nút Đổi đội
            var title = Text(lineup, "tieu_de", Theme.Title, 46, Theme.Ink, TextAlignmentOptions.MidlineLeft, 0);
            title.rectTransform.Place(new Vector2(0, 1), new Vector2(60, -30), new Vector2(280, 64), new Vector2(0, 1));
            title.text = "Đội hình";
            var teamPower = IconNumber(lineup, "luc_chien_doi", "sword", 52, 46, Theme.RedD, Sketch.Pill, out var chip);
            chip.anchorMin = chip.anchorMax = new Vector2(0.5f, 1);
            chip.pivot = new Vector2(0.5f, 1);
            chip.anchoredPosition = new Vector2(30, -26);
            chip.sizeDelta = new Vector2(260, 70);
            var edit = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonSmall.gameObject, lineup)).GetComponent<SketchButton>();
            edit.name = "nut_doi_doi";
            edit.Rect.Place(new Vector2(1, 1), new Vector2(-50, -24), new Vector2(210, 76), new Vector2(1, 1));
            edit.SetText("Đổi đội");
            edit.SetRole(BtnColor.Blue);

            // sân: 3 ô, gốc ở đáy giữa sân
            var stage = Node(lineup, "san");
            stage.Place(new Vector2(0.5f, 1), new Vector2(0, -104), new Vector2(1080, 470), new Vector2(0.5f, 1));
            var spots = new TeamLineup.Spot[3];
            for (int i = 0; i < 3; i++) spots[i] = Spot(kit, stage, i);

            // 4 chỉ số của con giữa: tên, Máu, Công, Thủ, Tốc
            var statsRow = Node(lineup, "chi_so");
            statsRow.Place(new Vector2(0.5f, 1), new Vector2(0, -652), new Vector2(1000, 100), new Vector2(0.5f, 1));
            var focus = Text(statsRow, "ten", Theme.Title, 32, Theme.Ink, TextAlignmentOptions.Center);
            focus.rectTransform.Place(new Vector2(0.5f, 1), Vector2.zero, new Vector2(1000, 42), new Vector2(0.5f, 1));
            string[] icons = { "heart", "sword", "shield", "speed" };
            var stats = new TextMeshProUGUI[4];
            for (int i = 0; i < 4; i++)
            {
                var cell = Node(statsRow, "chi_so_" + icons[i]);
                cell.Place(new Vector2(0.5f, 1), new Vector2((i - 1.5f) * 236, -44), new Vector2(220, 56), new Vector2(0.5f, 1));
                var ic = Img(cell, "icon", Icon(icons[i]), Color.white);
                ic.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(8, 0), new Vector2(48, 48), new Vector2(0, 0.5f));
                stats[i] = Text(cell, "so", Theme.Title, 38, Theme.Ink, TextAlignmentOptions.MidlineLeft);
                stats[i].rectTransform.Place(new Vector2(0, 0.5f), new Vector2(64, 2), new Vector2(156, 56), new Vector2(0, 0.5f));
                stats[i].text = "0";
            }

            // chấm vị trí ở đáy khung
            var dotRow = Node(lineup, "cham");
            dotRow.Place(new Vector2(0.5f, 0), new Vector2(0, 28), new Vector2(120, 18), new Vector2(0.5f, 0));
            var dots = new Image[3];
            for (int i = 0; i < 3; i++)
            {
                dots[i] = Img(dotRow, "cham_" + i, Sketch.InkDot, Theme.Paper3);
                dots[i].rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2((i - 1) * 30, 0), new Vector2(16, 16));
            }

            lineup.GetComponent<TeamLineup>().Setup(new TeamLineup.Parts
            {
                spots = spots, teamPower = teamPower, focusName = focus, stats = stats, dots = dots, edit = edit,
            }, picker);
            SetRef(root.GetComponent<HeroesScene>(), "lineup", lineup.GetComponent<TeamLineup>());
        }

        // một ô đội: vùng chạm, bóng dưới chân, chỗ đứng (tướng aola / chân dung), bảng tên (số thứ tự, tên, lực chiến), ô trống
        static TeamLineup.Spot Spot(UiKit kit, RectTransform stage, int i)
        {
            var root = Node(stage, "o_" + i, typeof(CanvasGroup), typeof(ClickCatcher));
            root.Place(new Vector2(0.5f, 0), new Vector2((i == 0 ? 0 : i == 1 ? 1 : -1) * TeamLineup.Gap, 0), new Vector2(300, 470), new Vector2(0.5f, 0));
            Hit(root.gameObject);
            var shadow = Img(root, "bong", Sketch.InkDot, new Color(Theme.Ink.r, Theme.Ink.g, Theme.Ink.b, 0.16f));
            shadow.preserveAspect = false;
            shadow.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 112), new Vector2(230, 46), new Vector2(0.5f, 0.5f));
            var body = Node(root, "dung");
            body.Place(new Vector2(0.5f, 0), new Vector2(0, 112), new Vector2(300, 360), new Vector2(0.5f, 0));
            var portrait = Portrait(kit, body, "chan_dung");
            portrait.Rect.anchorMin = portrait.Rect.anchorMax = new Vector2(0.5f, 0);
            portrait.Rect.anchoredPosition = Vector2.zero;

            var plate = Img(root, "bang_ten", Sketch.PanelThin, Theme.CardFill, true);
            plate.rectTransform.Place(new Vector2(0.5f, 0), Vector2.zero, new Vector2(270, 104), new Vector2(0.5f, 0));
            var badge = Img(plate.transform, "thu_tu", Sketch.InkDot, Theme.Yellow);
            badge.rectTransform.Place(new Vector2(0, 1), new Vector2(-14, 18), new Vector2(50, 50), new Vector2(0, 1));
            var order = Text(badge.transform, "chu", Theme.Title, 30, Theme.Ink, TextAlignmentOptions.Center);
            order.rectTransform.Stretch(0, 0, 0, 2);
            order.text = (i + 1).ToString();
            var name = Text(plate.transform, "ten", Theme.Title, 28, Theme.Ink, TextAlignmentOptions.Center);
            name.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(8, -6), new Vector2(220, 38), new Vector2(0.5f, 1));
            name.enableAutoSizing = true;
            name.fontSizeMin = 18;
            name.fontSizeMax = 28;
            var power = IconNumber(plate.transform, "luc_chien", "sword", 40, 40, Theme.RedD, null, out var row);
            row.anchorMin = row.anchorMax = new Vector2(0.5f, 0);
            row.pivot = new Vector2(0.5f, 0);
            row.anchoredPosition = new Vector2(0, 6);
            row.sizeDelta = new Vector2(200, 52);

            var empty = Img(root, "trong", Sketch.PanelThin, new Color(1, 1, 1, 0.55f), true);
            empty.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 70), new Vector2(220, 270), new Vector2(0.5f, 0));
            var emptyText = Text(empty.transform, "chu", Theme.Title, 30, Theme.Ink3, TextAlignmentOptions.Center);
            emptyText.rectTransform.Stretch(8, 8, 8, 8);
            emptyText.textWrappingMode = TextWrappingModes.Normal;
            empty.gameObject.SetActive(false);

            return new TeamLineup.Spot
            {
                root = root, body = body, portrait = portrait, click = root.GetComponent<ClickCatcher>(), plate = plate, shadow = shadow,
                order = order, name = name, power = power, empty = empty.gameObject, emptyText = emptyText,
            };
        }

        // ---------- soát ----------

        static readonly string[] DumpPaths =
        {
            TilePath, FoePath, HeroTilePath, PrepPath, ChestPath, ZoneChestPath, ResultPath, HeroesPath,
            "Assets/04 Prefabs/Kit/ChanDung.prefab", "Assets/04 Prefabs/Kit/KhungMong.prefab", "Assets/04 Prefabs/Kit/Chip.prefab",
        };

        [MenuItem("PokiClash/Prefab/In cây prefab popup (Temp/PopupDump.txt)", priority = 200)]
        static void Dump()
        {
            var sb = new StringBuilder();
            foreach (var path in DumpPaths)
            {
                var go = AssetDatabase.LoadAssetAtPath<GameObject>(path);
                sb.AppendLine("== " + path);
                if (go) DumpNode(go.transform, 0, sb);
            }
            var file = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PopupDump.txt"));
            File.WriteAllText(file, sb.ToString());
            Debug.Log("[Popup] Đã ghi " + file);
        }

        static string V(Vector2 v) => $"({v.x:0.##},{v.y:0.##})";

        static void DumpNode(Transform t, int depth, StringBuilder sb)
        {
            sb.Append(new string(' ', depth * 2)).Append(t.name);
            if (!t.gameObject.activeSelf) sb.Append(" [off]");
            if (t is RectTransform r)
                sb.Append($" a={V(r.anchorMin)}-{V(r.anchorMax)} p={V(r.pivot)} pos={V(r.anchoredPosition)} size={V(r.sizeDelta)}");
            if (t.localScale != Vector3.one) sb.Append($" scale={t.localScale.x:0.##}");
            if (t.localEulerAngles.z != 0) sb.Append($" rot={t.localEulerAngles.z:0.#}");
            var tmp = t.GetComponent<TextMeshProUGUI>();
            if (tmp)
                sb.Append($" TEXT[{tmp.font?.name} {tmp.fontSize} {tmp.alignment} '{tmp.text.Replace("\n", "\\n")}' mat={tmp.fontSharedMaterial?.name}]");
            var img = t.GetComponent<Image>();
            if (img) sb.Append($" IMG[{(img.sprite ? img.sprite.name : "-")} {ColorUtility.ToHtmlStringRGBA(img.color)} {img.type}]");
            foreach (var c in t.GetComponents<MonoBehaviour>())
                if (c && !(c is Graphic) && c.GetType().Namespace != null && c.GetType().Namespace.StartsWith("PokiClash"))
                    sb.Append(" <" + c.GetType().Name + ">");
            var le = t.GetComponent<LayoutElement>();
            if (le) sb.Append($" LE[pw={le.preferredWidth} ph={le.preferredHeight} ign={le.ignoreLayout}]");
            var lg = t.GetComponent<HorizontalOrVerticalLayoutGroup>();
            if (lg) sb.Append($" LG[{lg.GetType().Name} sp={lg.spacing} pad={lg.padding.left},{lg.padding.right},{lg.padding.top},{lg.padding.bottom} ctrl={lg.childControlWidth},{lg.childControlHeight} exp={lg.childForceExpandWidth},{lg.childForceExpandHeight} al={lg.childAlignment}]");
            var gl = t.GetComponent<GridLayoutGroup>();
            if (gl) sb.Append($" GRID[cell={V(gl.cellSize)} sp={V(gl.spacing)} {gl.constraint} {gl.constraintCount} al={gl.childAlignment}]");
            sb.AppendLine();
            foreach (Transform c in t) DumpNode(c, depth + 1, sb);
        }
    }
}
