// Dựng hộp chọn đội Dialogs/ChonDoi (biến thể tờ giấy gốc HopThoai, TeamPickerDialog): tiêu đề, lưới kho tướng,
// dòng gợi ý (khắc hệ, ô đội còn khoá), nút "Xong". Chữ chép từ hộp Chuẩn bị trận. Gán vào ChuanBiTran (pickerPrefab) cùng hai chữ
// đầu mục đội hình (teamTitle, teamHint). Chạy lại thì dựng lại; cuối cùng chạy luôn phần ô tướng, khung cuộn dưới đây.
// Menu "Hộp chọn đội: ô tướng, khung cuộn" (2026-11-06, người dùng: sửa ô chọn tướng; 78 tướng làm tờ giấy dài quá màn, mất tiêu đề và
// nút Xong): dựng ô Items/OChonDoi (PrepRosterCell: khung giấy, dải màu hệ sau chân dung, sao, tên, lực chiến, tròn số thứ tự góc trên
// trái, mũi tên khắc hệ trong góc trên phải) và bọc lưới "kho" của ChonDoi vào khung cuộn "cuon" (5 cột, mép trên dưới mờ dần;
// TeamPickerDialog chỉnh cao khung vừa màn). Sửa thẳng prefab ChonDoi nên tham chiếu từ ChuanBiTran, màn Tướng giữ nguyên.
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class TeamPickerMenu
    {
        const string SheetPath = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const string PickerPath = "Assets/04 Prefabs/Dialogs/ChonDoi.prefab";
        const string CellPath = "Assets/04 Prefabs/Items/OChonDoi.prefab";

        // ô chọn đội: 5 cột vừa khung 838 của tờ giấy 940 (5 × 154 + 4 × 12 + lề 2 × 10)
        const float CellW = 154, CellH = 210, GapX = 12, GapY = 16, PortraitH = 136;
        const int Cols = 5;
        // dải màu hệ sau chân dung: lề trong, cao
        const float BandPad = 7, BandH = 124;

        [MenuItem("PokiClash/Prefab/Hộp chọn đội (ChonDoi)", priority = 64)]
        static void Build()
        {
            var kit = AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));
            var prep = AssetDatabase.LoadAssetAtPath<GameObject>(PrepPath).GetComponent<StagePrepDialog>();
            var pso = new SerializedObject(prep);
            var titleTpl = (TextMeshProUGUI)pso.FindProperty("p.title").objectReferenceValue;
            var hintTpl = (TextMeshProUGUI)pso.FindProperty("p.hint").objectReferenceValue;
            var cell = (PrepRosterCell)pso.FindProperty("cellPrefab").objectReferenceValue;

            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetPath));
            try
            {
                root.name = "ChonDoi";
                root.GetComponent<ModalSheet>().Configure(940, false, false);
                // khung nội dung dưới tờ giấy (như ChuanBiTran): cột dọc, giãn ngang
                var sheet = Find(root.transform, "to_giay");
                if (!sheet)
                {
                    Debug.LogError("[Đội] HopThoai không có to_giay.");
                    return;
                }
                var content = new GameObject("noi_dung", typeof(RectTransform), typeof(VerticalLayoutGroup)).transform;
                content.SetParent(sheet, false);
                var vl = content.GetComponent<VerticalLayoutGroup>();
                vl.spacing = 14;
                vl.childControlWidth = vl.childControlHeight = true;
                vl.childForceExpandWidth = true;
                vl.childForceExpandHeight = false;

                var title = Text(titleTpl, content, "tieu_de", 64);
                title.alignment = TextAlignmentOptions.Center;
                title.text = "Chọn đội";

                var gridGo = new GameObject("kho", typeof(RectTransform), typeof(GridLayoutGroup), typeof(LayoutElement));
                gridGo.transform.SetParent(content, false);
                var grid = gridGo.GetComponent<GridLayoutGroup>();
                grid.cellSize = new Vector2(136, 160);
                grid.spacing = new Vector2(14, 16);
                grid.childAlignment = TextAnchor.UpperCenter;
                var gridLe = gridGo.GetComponent<LayoutElement>();
                gridLe.preferredHeight = 176;

                var hint = Text(hintTpl, content, "goi_y", 80);
                hint.alignment = TextAlignmentOptions.Center;
                hint.textWrappingMode = TextWrappingModes.Normal;
                hint.text = "Mũi tên xanh: khắc hệ của địch. Mũi tên đỏ: bị khắc.";

                var row = new GameObject("hang", typeof(RectTransform), typeof(HorizontalLayoutGroup), typeof(LayoutElement));
                row.transform.SetParent(content, false);
                var hl = row.GetComponent<HorizontalLayoutGroup>();
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                row.GetComponent<LayoutElement>().preferredHeight = 120;
                var done = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonBig.gameObject, row.transform)).GetComponent<SketchButton>();
                done.name = "nut_Xong";
                done.SetText("Xong");
                done.SetRole(BtnColor.Green);

                root.AddComponent<TeamPickerDialog>().Setup(title, hint, (RectTransform)gridGo.transform, gridLe, done, cell);
                var picker = PrefabUtility.SaveAsPrefabAsset(root, PickerPath).GetComponent<TeamPickerDialog>();

                // gán vào hộp Chuẩn bị trận
                var contents = PrefabUtility.LoadPrefabContents(PrepPath);
                try
                {
                    var so = new SerializedObject(contents.GetComponent<StagePrepDialog>());
                    so.FindProperty("pickerPrefab").objectReferenceValue = picker;
                    var head = Find(contents.transform, "dau_doi");
                    var texts = head.GetComponentsInChildren<TextMeshProUGUI>(true);
                    so.FindProperty("teamTitle").objectReferenceValue = texts[0];
                    so.FindProperty("teamHint").objectReferenceValue = texts.Length > 1 ? texts[1] : null;
                    so.ApplyModifiedPropertiesWithoutUndo();
                    PrefabUtility.SaveAsPrefabAsset(contents, PrepPath);
                }
                finally
                {
                    PrefabUtility.UnloadPrefabContents(contents);
                }
                Debug.Log($"[Đội] Đã dựng {PickerPath} và gán vào {PrepPath}.");
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
            BuildScroll();
        }

        // ---------- ô tướng, khung cuộn ----------

        [MenuItem("PokiClash/Prefab/Hộp chọn đội: ô tướng, khung cuộn", priority = 65)]
        static void BuildScroll()
        {
            var assets = Load<UiAssets>();
            var art = Load<ArtLibrary>();
            Theme.Init(assets); // phông, sprite giấy, viền chữ nướng sẵn
            var cell = BuildCell(assets.prefabs, art);

            var root = PrefabUtility.LoadPrefabContents(PickerPath);
            try
            {
                var dlg = root.GetComponent<TeamPickerDialog>();
                var gridRt = (RectTransform)Find(root.transform, "kho");
                if (!gridRt)
                {
                    Debug.LogError("[Đội] ChonDoi không có lưới kho.");
                    return;
                }
                // khung cuộn cũ (dựng lại): đưa lưới ra trước rồi xoá khung
                var old = Find(root.transform, "cuon");
                Transform content = old ? old.parent : gridRt.parent;
                int index = old ? old.GetSiblingIndex() : gridRt.GetSiblingIndex();
                gridRt.SetParent(content, false);
                if (old) Object.DestroyImmediate(old.gameObject);
                var gridLe = gridRt.GetComponent<LayoutElement>();
                if (gridLe) Object.DestroyImmediate(gridLe);

                var scrollGo = new GameObject("cuon", typeof(RectTransform), typeof(ScrollRect), typeof(LayoutElement));
                var scrollRt = (RectTransform)scrollGo.transform;
                scrollRt.SetParent(content, false);
                scrollRt.SetSiblingIndex(index);
                var viewLe = scrollGo.GetComponent<LayoutElement>();
                viewLe.preferredHeight = 2 * CellH + GapY + 28;

                // khung nhìn: cắt mép, mép trên dưới mờ dần (báo còn cuộn được), nền trong suốt nhận kéo ở khe giữa các ô
                var view = new GameObject("khung_nhin", typeof(RectTransform), typeof(RectMask2D), typeof(Image)).GetComponent<RectTransform>();
                view.SetParent(scrollRt, false);
                view.Stretch();
                view.GetComponent<RectMask2D>().softness = new Vector2Int(0, 18);
                var viewImg = view.GetComponent<Image>();
                viewImg.color = new Color(1, 1, 1, 0);
                viewImg.raycastTarget = true;

                gridRt.SetParent(view, false);
                gridRt.anchorMin = new Vector2(0, 1);
                gridRt.anchorMax = new Vector2(1, 1);
                gridRt.pivot = new Vector2(0.5f, 1);
                gridRt.anchoredPosition = Vector2.zero;
                gridRt.sizeDelta = new Vector2(0, CellH + 28);
                var grid = gridRt.GetComponent<GridLayoutGroup>();
                grid.cellSize = new Vector2(CellW, CellH);
                grid.spacing = new Vector2(GapX, GapY);
                grid.padding = new RectOffset(10, 10, 14, 14);
                grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
                grid.constraintCount = Cols;
                grid.childAlignment = TextAnchor.UpperCenter;
                for (int i = gridRt.childCount - 1; i >= 0; i--) Object.DestroyImmediate(gridRt.GetChild(i).gameObject);

                var scroll = scrollGo.GetComponent<ScrollRect>();
                scroll.viewport = view;
                scroll.content = gridRt;
                scroll.horizontal = false;
                scroll.vertical = true;
                scroll.movementType = ScrollRect.MovementType.Elastic;
                scroll.elasticity = 0.08f;
                scroll.scrollSensitivity = 40;

                dlg.SetupScroll(scroll, gridRt, viewLe, cell);
                EditorUtility.SetDirty(dlg);
                PrefabUtility.SaveAsPrefabAsset(root, PickerPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            AssetDatabase.SaveAssets();
            Debug.Log($"[Đội] Đã dựng {CellPath} và khung cuộn trong {PickerPath}.");
        }

        // ô chọn đội 154 × 210 (y tính từ mép trên): dải hệ 7..131 có chân dung đứng ở đáy dải, sao ở 143, tên 152..180, lực chiến 180..204
        static PrepRosterCell BuildCell(UiKit kit, ArtLibrary art)
        {
            var root = new GameObject("OChonDoi", typeof(RectTransform), typeof(ClickCatcher), typeof(PrepRosterCell));
            try
            {
                var rt = (RectTransform)root.transform;
                rt.sizeDelta = new Vector2(CellW, CellH);

                var frame = Img(root.transform, "khung", Sketch.PanelThin, Theme.CardFill, true);
                frame.rectTransform.Stretch();
                frame.pixelsPerUnitMultiplier = 1.6f;
                frame.raycastTarget = true; // nhận chạm cho ClickCatcher ở gốc

                var band = Img(root.transform, "dai_he", Sketch.PanelFlat, new Color(1, 1, 1, 0.35f), true);
                var br = band.rectTransform;
                br.anchorMin = new Vector2(0, 1);
                br.anchorMax = new Vector2(1, 1);
                br.pivot = new Vector2(0.5f, 1);
                br.anchoredPosition = new Vector2(0, -BandPad);
                br.sizeDelta = new Vector2(-2 * BandPad, BandH);

                var portrait = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, root.transform)).GetComponent<HeroPortrait>();
                portrait.name = "chan_dung";
                var pr = portrait.Rect;
                pr.anchorMin = pr.anchorMax = new Vector2(0.5f, 1);
                pr.pivot = new Vector2(0.5f, HeroArt.FootY);
                pr.anchoredPosition = new Vector2(0, -(BandPad + BandH - 4));
                pr.sizeDelta = new Vector2(PortraitH * HeroArt.W / HeroArt.H, PortraitH);

                var stars = ((GameObject)PrefabUtility.InstantiatePrefab(kit.stars.gameObject, root.transform)).GetComponent<UiStars>();
                stars.name = "sao";
                stars.SetSize(22);
                stars.Rect.anchorMin = stars.Rect.anchorMax = new Vector2(0.5f, 1);
                stars.Rect.pivot = new Vector2(0.5f, 0.5f);
                stars.Rect.anchoredPosition = new Vector2(0, -143);
                stars.Set(1, 5);

                var heroName = Text(root.transform, "ten", Theme.Title, 24, Theme.Ink, TextAlignmentOptions.Center);
                heroName.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -152), new Vector2(CellW - 18, 28), new Vector2(0.5f, 1));
                heroName.enableAutoSizing = true;
                heroName.fontSizeMin = 13;
                heroName.fontSizeMax = 24;
                heroName.overflowMode = TextOverflowModes.Ellipsis;
                heroName.text = "Tên tướng";

                var power = IconNumber(root.transform, "luc_chien", Icon(art, "sword"), 22, 22, Theme.RedD, out var powerRow);
                powerRow.anchorMin = powerRow.anchorMax = new Vector2(0.5f, 0);
                powerRow.pivot = new Vector2(0.5f, 0);
                powerRow.anchoredPosition = new Vector2(0, 6);
                powerRow.sizeDelta = new Vector2(120, 26);

                // mũi tên khắc hệ: trong góc trên phải, chỉ lấn mép 6 (không đè ô bên cạnh)
                var arrow = Img(root.transform, "khac", Icon(art, "up"), Color.white, false);
                arrow.rectTransform.Place(new Vector2(1, 1), new Vector2(6, 6), new Vector2(46, 46), new Vector2(1, 1));
                arrow.gameObject.SetActive(false);

                // thứ tự ra trận: tròn xanh, số trắng viền mực, góc trên trái
                var badge = Img(root.transform, "thu_tu", Sketch.Round, Theme.Green, false);
                badge.rectTransform.Place(new Vector2(0, 1), new Vector2(-6, 6), new Vector2(48, 48), new Vector2(0, 1));
                var badgeText = Text(badge.transform, "so", Theme.Title, 30, Color.white, TextAlignmentOptions.Center, 0.25f);
                badgeText.rectTransform.Stretch(0, 0, 0, 3);
                badgeText.text = "1";
                badge.gameObject.SetActive(false);

                var c = root.GetComponent<PrepRosterCell>();
                c.Setup(frame, portrait, heroName, arrow, root.GetComponent<ClickCatcher>());
                c.SetupPick(PortraitH, band, stars, power, badge.gameObject, badgeText);
                return PrefabUtility.SaveAsPrefabAsset(root, CellPath).GetComponent<PrepRosterCell>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- thử (đang Play) ----------

        // mở hộp chọn đội với địch hệ Hỏa (có mũi tên), chụp đầu và cuối khung cuộn; mở lại với 3 ô, chọn thêm 2 con, chụp.
        // Không bấm Xong nên đội trong bản lưu giữ nguyên. Ảnh Temp/PokiShots/chon_doi_*.png (không xoá ảnh khác).
        [MenuItem("PokiClash/Thử/Hộp chọn đội: chụp ô tướng, khung cuộn (đang Play)", priority = 116)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Đội] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(TryRun());
        }

        static System.Collections.IEnumerator TryRun()
        {
            var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(PickerPath).GetComponent<TeamPickerDialog>();
            var d = App.Data;
            var s = App.Save.Data;
            var foe = d.Heroes.FirstOrDefault(h => h.elem == PokiClash.Core.Elem.Hoa);
            var team = s.team.Where(h => s.Hero(h)?.owned == true).ToList();
            int open = PokiClash.Core.Progress.TeamSlots(s);
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.3f);

            var dlg = App.Modals.Open(prefab);
            dlg.Show(team, open, foe, null);
            yield return new WaitForSecondsRealtime(0.6f);
            yield return TryShot("1_dau");
            var scroll = dlg.GetComponentInChildren<ScrollRect>();
            if (scroll)
            {
                scroll.verticalNormalizedPosition = 0;
                yield return new WaitForSecondsRealtime(0.3f);
                yield return TryShot("2_cuoi");
            }
            dlg.Close();
            yield return new WaitForSecondsRealtime(0.4f);

            dlg = App.Modals.Open(prefab);
            dlg.Show(team.Take(1).ToList(), 3, foe, null);
            yield return new WaitForSecondsRealtime(0.5f);
            var cells = dlg.GetComponentsInChildren<PrepRosterCell>();
            foreach (var c in cells.Skip(2).Take(2))
            {
                c.GetComponent<ClickCatcher>().OnClick?.Invoke();
                yield return new WaitForSecondsRealtime(0.15f);
            }
            yield return new WaitForSecondsRealtime(0.3f);
            yield return TryShot("3_ba_o");
            dlg.Close();
            Debug.Log($"[Đội] Đã chụp hộp chọn đội ({cells.Length} ô) vào {PlayTour.ShotDir}/chon_doi_*.png");
        }

        static System.Collections.IEnumerator TryShot(string name)
        {
            yield return new WaitForEndOfFrame();
            System.IO.Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            System.IO.File.WriteAllBytes(System.IO.Path.Combine(PlayTour.ShotDir, $"chon_doi_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));

        static Sprite Icon(ArtLibrary art, string n) => art ? art.Icon(n) : null;

        static Transform Find(Transform t, string name)
        {
            foreach (var c in t.GetComponentsInChildren<Transform>(true))
                if (c.name == name) return c;
            return null;
        }

        // chữ chép từ chữ có sẵn (phông, viền), giãn ngang theo cột, cao h
        static TextMeshProUGUI Text(TextMeshProUGUI from, Transform parent, string name, float h)
        {
            var t = Object.Instantiate(from.gameObject, parent, false).GetComponent<TextMeshProUGUI>();
            t.name = name;
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            var le = t.GetComponent<LayoutElement>();
            if (!le) le = t.gameObject.AddComponent<LayoutElement>();
            le.preferredHeight = h;
            t.gameObject.SetActive(true);
            return t;
        }

        static Image Img(Transform parent, string name, Sprite sprite, Color color, bool sliced)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var img = go.GetComponent<Image>();
            Theme.SetSprite(img, sprite);
            img.type = sliced ? Image.Type.Sliced : Image.Type.Simple;
            img.preserveAspect = !sliced;
            img.color = color;
            img.raycastTarget = false;
            return img;
        }

        // outline: độ dày viền mực (0,2..0,32, theo material nướng sẵn), 0 là không viền
        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, TextAlignmentOptions align,
            float outline = 0)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(TextMeshProUGUI));
            go.transform.SetParent(parent, false);
            var t = go.GetComponent<TextMeshProUGUI>();
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

        // viên "icon + số" xếp ngang, canh giữa, tự co theo số; trả chữ số
        static TextMeshProUGUI IconNumber(Transform parent, string name, Sprite icon, float iconSize, float fontSize, Color color, out RectTransform row)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(HorizontalLayoutGroup), typeof(ContentSizeFitter));
            go.transform.SetParent(parent, false);
            row = (RectTransform)go.transform;
            var hl = go.GetComponent<HorizontalLayoutGroup>();
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.spacing = 4;
            hl.childControlWidth = hl.childControlHeight = true;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            go.GetComponent<ContentSizeFitter>().horizontalFit = ContentSizeFitter.FitMode.PreferredSize;
            var ic = Img(row, "icon", icon, Color.white, false);
            var le = ic.gameObject.AddComponent<LayoutElement>();
            le.preferredWidth = le.preferredHeight = iconSize;
            var t = Text(row, "so", Theme.Title, fontSize, color, TextAlignmentOptions.MidlineLeft);
            t.text = "0";
            return t;
        }
    }
}
