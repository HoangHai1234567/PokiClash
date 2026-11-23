// Màn Tướng: độ hiếm rõ, lọc và xếp (người dùng dặn 2026-11-17, GD_Claude/20_TangDayNoiDung.md, dòng E). Menu
// "PokiClash/Prefab/Hộp thoại và màn/Màn Tướng: độ hiếm, lọc và xếp" sửa prefab (chạy lại thì dựng lại, không nhân đôi):
// - Items/TheTuong (HeroTile): giấy lót "giay" trong thẻ (thẻ thành khung ngoài tô màu độ hiếm, HeroTile lùi giấy vào Theme.RarityInset px),
//   đường chỉ khâu chuyển vào giấy; chữ độ hiếm thành viên "nhan_hiem" (màu độ hiếm, chữ trắng viền mực); vương miện "vuong_mien" ở mép
//   trên (Huyền thoại, thở nhẹ; băng keo ẩn); dải hệ, tên thu vào trong giấy;
// - Screens/Heroes (HeroesScene): hàng "loc_xep" giữa khung đội hình và lưới: nút tròn Tất cả + 5 hệ, nút viên xếp, nút tròn mũi tên đảo
//   chiều; chữ "chu_trong" khi lọc hệ chưa có tướng; khung cuộn dời xuống, lề trên lưới chừa chỗ vương miện;
//   bảng tên 3 ô đội hình (TeamLineup): giấy lót, vương miện góc trên phải;
// - Items/OChonDoi (PrepRosterCell): giấy lót trong khung, vương miện giữa mép trên; Dialogs/ChonDoi: lề trên lưới chừa chỗ vương miện;
// - Dialogs/ChuanBiTran (StagePrepDialog): 3 ô đội: giấy lót, vương miện góc trên phải; gán chữ đầu mục "Phần thưởng" (rewardTitle,
//   đánh lại trận Đền Huy Hiệu đổi thành "Sao trận").
// Chạy SAU các menu dựng lại những prefab này từ đầu: "Popup gọn (ô thưởng, đội hình, lực chiến)" (dựng lại khung đội hình, khung cuộn),
// "Hộp chọn đội: ô tướng, khung cuộn" (dựng lại OChonDoi), "Bộ UI Sa Bàn" (chỉ khâu). Chạy các menu đó thì chạy lại menu này.
// Màu, độ dày khung, chữ nhãn: Theme (RarityBand, RarityInset, RarityHatch, RarityLabel); logic lọc / xếp: HeroesScene.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HeroRarityMenu
    {
        const string TilePath = "Assets/04 Prefabs/Items/TheTuong.prefab";
        const string HeroesPath = "Assets/04 Prefabs/Screens/Heroes.prefab";
        const string CellPath = "Assets/04 Prefabs/Items/OChonDoi.prefab";
        const string PickerPath = "Assets/04 Prefabs/Dialogs/ChonDoi.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";

        // hàng lọc / xếp: cao, cỡ nút tròn, cỡ icon; lề trên lưới tướng (chừa vương miện hàng đầu)
        const float RowH = 92, ChipSize = 72, IconSize = 44, GridTop = 56;
        static readonly string[] ElemIcons = { "e_thuy", "e_hoa", "e_kim", "e_moc", "e_tho" }; // theo TeamPickerDialog.FilterOrder

        static ArtLibrary art;

        static Sprite Icon(string n) => art ? art.Icon(n) : null;

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Màn Tướng: độ hiếm, lọc và xếp", priority = 67)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            art = Load<ArtLibrary>();
            Theme.Init(assets); // phông, sprite giấy, viền chữ nướng sẵn
            var kit = assets.prefabs;
            Edit(TilePath, PatchTile);
            Edit(HeroesPath, root => PatchHeroes(root, kit));
            Edit(CellPath, PatchCell);
            Edit(PickerPath, PatchPicker);
            Edit(PrepPath, PatchPrep);
            AssetDatabase.SaveAssets();
            Debug.Log("[Tướng] Đã dựng khung độ hiếm (TheTuong, đội hình, OChonDoi, ChuanBiTran) và hàng lọc / xếp màn Tướng.");
        }

        // ---------- thẻ tướng ----------

        static void PatchTile(GameObject root)
        {
            var so = new SerializedObject(root.GetComponent<HeroTile>());
            var card = (Image)so.FindProperty("p.card").objectReferenceValue;
            var band = (Image)so.FindProperty("p.band").objectReferenceValue;
            var rarity = (TextMeshProUGUI)so.FindProperty("p.rarity").objectReferenceValue;
            var nameText = (TextMeshProUGUI)so.FindProperty("p.name").objectReferenceValue;
            if (!card || !band || !rarity)
            {
                Debug.LogError("[Tướng] TheTuong thiếu thẻ, dải hệ hoặc chữ độ hiếm.");
                return;
            }
            var ct = card.transform;
            float w = Theme.RarityInset(Rarity.Common, 1, 7);

            // giấy lót: đầu tiên trong thẻ (dưới mọi thứ), chỉ khâu của thẻ chuyển vào giấy
            Remove(ct, "giay");
            var paper = Img(ct, "giay", Sketch.Panel, Theme.CardFill, true);
            paper.transform.SetSiblingIndex(0);
            paper.rectTransform.Stretch(w, w, w, w);
            paper.pixelsPerUnitMultiplier = 1.3f;
            var stitch = ct.Find("chi_khau");
            if (stitch && stitch.TryGetComponent<Image>(out var src))
            {
                // tên "chi_khau" như menu Bộ UI Sa Bàn đặt: chạy lại menu đó thì nó chỉnh lại sợi này, không thêm sợi mới
                var st = Img(paper.transform, "chi_khau", src.sprite, src.color, false);
                st.type = src.type;
                st.fillCenter = src.fillCenter;
                st.material = src.material;
                st.pixelsPerUnitMultiplier = src.pixelsPerUnitMultiplier;
                st.preserveAspect = false;
                st.rectTransform.Stretch(16, 16, 16, 16);
                stitch.gameObject.SetActive(false);
            }

            // dải hệ, tên, hàng sao, lực chiến thu vào trong giấy (khung Huyền thoại dày nhất: giấy lùi 22, nét mực giấy tới khoảng 30)
            var br = band.rectTransform;
            br.anchoredPosition = new Vector2(0, -30);
            br.sizeDelta = new Vector2(-64, 96);
            if (nameText) nameText.rectTransform.sizeDelta = new Vector2(248, nameText.rectTransform.sizeDelta.y);
            var stars = (UiStars)so.FindProperty("p.stars").objectReferenceValue;
            if (stars) stars.Rect.anchoredPosition = new Vector2(-62, 30);
            var power = (TextMeshProUGUI)so.FindProperty("p.power").objectReferenceValue;
            if (power) ((RectTransform)power.transform.parent).anchoredPosition = new Vector2(66, 28);

            // nhãn độ hiếm: viên màu độ hiếm, chữ trắng viền mực, đúng chỗ chữ độ hiếm cũ (đáy phải, cạnh nhãn hệ)
            var oldPill = ct.Find("nhan_hiem");
            if (oldPill)
            {
                rarity.transform.SetParent(ct, false);
                Object.DestroyImmediate(oldPill.gameObject);
            }
            var pill = Img(ct, "nhan_hiem", Sketch.Pill, Theme.Of(Rarity.Epic), true);
            pill.pixelsPerUnitMultiplier = 1.8f;
            pill.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(50, 74), new Vector2(140, 38), new Vector2(0.5f, 0));
            pill.transform.SetSiblingIndex(rarity.transform.GetSiblingIndex());
            rarity.transform.SetParent(pill.transform, false);
            rarity.rectTransform.Stretch(10, 1, 10, 3);
            rarity.font = Theme.Title;
            var outlined = Theme.Outlined(Theme.Title, 0.22f); // cỡ viền có sẵn (như dải độ hiếm của ô thưởng)
            if (outlined) rarity.fontSharedMaterial = outlined;
            rarity.color = Color.white;
            rarity.alignment = TextAlignmentOptions.Center;
            rarity.enableAutoSizing = true;
            rarity.fontSizeMin = 14;
            rarity.fontSizeMax = 22;
            rarity.textWrappingMode = TextWrappingModes.NoWrap;
            rarity.text = Theme.RarityLabel(Rarity.Epic);

            // vương miện (Huyền thoại) đè mép trên giữa thẻ, chỗ băng keo; thở nhẹ
            Remove(ct, "vuong_mien");
            var crown = Crown(ct, new Vector2(0.5f, 1), new Vector2(0, 12), 78, new Vector2(0.5f, 0.5f));

            var tape = ct.Find("bang_keo");
            so.FindProperty("p.paper").objectReferenceValue = paper;
            so.FindProperty("p.rarityPill").objectReferenceValue = pill;
            so.FindProperty("p.crown").objectReferenceValue = crown;
            so.FindProperty("p.tape").objectReferenceValue = tape ? tape.gameObject : null;
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        // ---------- màn Tướng: hàng lọc / xếp, bảng tên đội hình ----------

        static void PatchHeroes(GameObject root, UiKit kit)
        {
            var scene = root.GetComponent<HeroesScene>();
            var content = Find(root.transform, "Noi dung");
            var scroll = content ? (RectTransform)Find(content, "cuon") : null;
            if (!scene || !content || !scroll)
            {
                Debug.LogError("[Tướng] Heroes thiếu HeroesScene, \"Noi dung\" hoặc khung cuộn \"cuon\".");
                return;
            }
            var lineupRt = (RectTransform)Find(content, "doi_hinh");
            float top = lineupRt ? lineupRt.sizeDelta.y : 790;

            Remove(content, "loc_xep");
            var row = Node(content, "loc_xep", typeof(HorizontalLayoutGroup));
            row.SetSiblingIndex(lineupRt ? lineupRt.GetSiblingIndex() + 1 : content.childCount - 1);
            row.anchorMin = new Vector2(0, 1);
            row.anchorMax = new Vector2(1, 1);
            row.pivot = new Vector2(0.5f, 1);
            row.anchoredPosition = new Vector2(0, -top);
            row.sizeDelta = new Vector2(0, RowH);
            var hl = row.GetComponent<HorizontalLayoutGroup>();
            hl.padding = new RectOffset(40, 40, 6, 6);
            hl.spacing = 10;
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = false;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;

            var all = Chip(kit, row, "loc_tat_ca", "team", out _);
            var elems = new SketchButton[ElemIcons.Length];
            var icons = new Image[ElemIcons.Length];
            for (int i = 0; i < ElemIcons.Length; i++) elems[i] = Chip(kit, row, "loc_" + ElemIcons[i], ElemIcons[i], out icons[i]);

            var gap = Node(row, "khe", typeof(LayoutElement));
            gap.GetComponent<LayoutElement>().preferredWidth = 18;

            var sort = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonTiny.gameObject, row)).GetComponent<SketchButton>();
            sort.name = "nut_xep";
            sort.SetText(HeroesScene.SortNames[0]);
            sort.SetRole(BtnColor.Paper);
            sort.FitWidth();
            var dir = Chip(kit, row, "nut_chieu", "down", out var dirIcon);

            // khung cuộn dời xuống dưới hàng; lề trên lưới chừa vương miện hàng đầu
            scroll.Stretch(0, top + RowH, 0, 0);
            var grid = scroll.GetComponentInChildren<GridLayoutGroup>(true);
            if (grid) grid.padding = new RectOffset(grid.padding.left, grid.padding.right, (int)GridTop, grid.padding.bottom);

            // chữ khi lọc hệ chưa có tướng (không cuộn theo lưới)
            Remove(scroll, "chu_trong");
            var empty = Text(scroll, "chu_trong", Theme.Title, 40, Theme.Ink3, TextAlignmentOptions.Center);
            empty.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -140), new Vector2(900, 150), new Vector2(0.5f, 1));
            empty.textWrappingMode = TextWrappingModes.Normal;
            empty.text = "Chưa có tướng hệ Mộc";
            empty.gameObject.SetActive(false);

            scene.SetupFilters(all, elems, icons, sort, dir, dirIcon, empty);
            EditorUtility.SetDirty(scene);

            // bảng tên 3 ô đội hình
            var lineup = lineupRt ? lineupRt.GetComponent<TeamLineup>() : null;
            if (!lineup)
            {
                Debug.LogWarning("[Tướng] Heroes chưa có khung đội hình (chạy menu Popup gọn trước): bỏ qua bảng tên.");
                return;
            }
            var lso = new SerializedObject(lineup);
            var spots = lso.FindProperty("p.spots");
            for (int i = 0; i < spots.arraySize; i++)
            {
                var sp = spots.GetArrayElementAtIndex(i);
                var plate = (Image)sp.FindPropertyRelative("plate").objectReferenceValue;
                if (!plate) continue;
                var pt = plate.transform;
                Remove(pt, "giay");
                Remove(pt, "vuong_mien");
                var paper = Img(pt, "giay", Sketch.PanelThin, Theme.CardFill, true);
                paper.transform.SetSiblingIndex(0);
                float pw = Theme.RarityInset(Rarity.Common, 0.7f, 5);
                paper.rectTransform.Stretch(pw, pw, pw, pw);
                paper.pixelsPerUnitMultiplier = 1.4f;
                // góc trên phải bảng tên, nhô lên trên mép (ô số thứ tự ở góc trên trái)
                var crown = Crown(pt, new Vector2(1, 1), new Vector2(-30, -14), 58, new Vector2(0.5f, 0));
                sp.FindPropertyRelative("paper").objectReferenceValue = paper;
                sp.FindPropertyRelative("crown").objectReferenceValue = crown;
            }
            lso.ApplyModifiedPropertiesWithoutUndo();
        }

        // ---------- hộp chọn đội ----------

        static void PatchCell(GameObject root)
        {
            var cell = root.GetComponent<PrepRosterCell>();
            var so = new SerializedObject(cell);
            var bg = (Image)so.FindProperty("bg").objectReferenceValue;
            if (!bg)
            {
                Debug.LogError("[Tướng] OChonDoi thiếu khung.");
                return;
            }
            Remove(bg.transform, "giay");
            var paper = Img(bg.transform, "giay", Sketch.PanelThin, Theme.CardFill, true);
            paper.transform.SetSiblingIndex(0);
            float w = Theme.RarityInset(Rarity.Common, 0.6f, 3);
            paper.rectTransform.Stretch(w, w, w, w);
            paper.pixelsPerUnitMultiplier = 1.9f;
            Remove(root.transform, "vuong_mien");
            // giữa mép trên (ô số thứ tự góc trên trái, mũi tên khắc hệ góc trên phải)
            var crown = Crown(root.transform, new Vector2(0.5f, 1), new Vector2(0, 2), 42, new Vector2(0.5f, 0.5f));
            cell.SetupRarity(paper, crown);
            EditorUtility.SetDirty(cell);
        }

        // lưới trong khung cuộn: lề trên chừa vương miện của hàng đầu (mép khung nhìn mờ dần 18)
        static void PatchPicker(GameObject root)
        {
            var kho = Find(root.transform, "kho");
            var grid = kho ? kho.GetComponent<GridLayoutGroup>() : null;
            if (!grid)
            {
                Debug.LogWarning("[Tướng] ChonDoi chưa có lưới kho: bỏ qua lề trên.");
                return;
            }
            grid.padding = new RectOffset(grid.padding.left, grid.padding.right, 26, grid.padding.bottom);
        }

        // ---------- hộp chuẩn bị trận: 3 ô đội ----------

        static void PatchPrep(GameObject root)
        {
            var so = new SerializedObject(root.GetComponent<StagePrepDialog>());
            var slots = so.FindProperty("p.slots");
            for (int i = 0; i < slots.arraySize; i++)
            {
                var sl = slots.GetArrayElementAtIndex(i);
                var bg = (Image)sl.FindPropertyRelative("bg").objectReferenceValue;
                if (!bg) continue;
                var t = bg.transform;
                Remove(t, "giay");
                Remove(t, "vuong_mien");
                var paper = Img(t, "giay", Sketch.PanelThin, Theme.Hex("#eaf6df"), true);
                paper.transform.SetSiblingIndex(0);
                float w = Theme.RarityInset(Rarity.Common, 0.7f, 5);
                paper.rectTransform.Stretch(w, w, w, w);
                paper.pixelsPerUnitMultiplier = 1.4f;
                paper.gameObject.SetActive(false);
                // góc trên phải (chip cấp ở góc trên trái)
                var crown = Crown(t, new Vector2(1, 1), new Vector2(10, 12), 56, new Vector2(1, 1));
                sl.FindPropertyRelative("paper").objectReferenceValue = paper;
                sl.FindPropertyRelative("crown").objectReferenceValue = crown;
            }
            // chữ đầu mục "Phần thưởng": anh em của khung ô thưởng
            var rewards = (RectTransform)so.FindProperty("p.rewards").objectReferenceValue;
            TextMeshProUGUI rewardTitle = null;
            if (rewards && rewards.parent)
                foreach (Transform c in rewards.parent)
                    if (c.TryGetComponent<TextMeshProUGUI>(out var t) && t.text.Trim() == "Phần thưởng") rewardTitle = t;
            if (!rewardTitle) Debug.LogWarning("[Tướng] ChuanBiTran: không thấy chữ \"Phần thưởng\" cạnh khung ô thưởng, đánh lại Đền Huy Hiệu giữ đầu mục cũ.");
            so.FindProperty("rewardTitle").objectReferenceValue = rewardTitle;
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        // ---------- dựng ----------

        // vương miện Huyền thoại (icon crown), tắt sẵn, thở nhẹ (bộ UI Sa Bàn: thở, không ánh sáng)
        static GameObject Crown(Transform parent, Vector2 anchor, Vector2 pos, float size, Vector2 pivot)
        {
            var img = Img(parent, "vuong_mien", Icon("crown"), Color.white);
            img.rectTransform.Place(anchor, pos, new Vector2(size, size), pivot);
            var mo = img.gameObject.AddComponent<UiMotion>();
            mo.breath = true;
            mo.breathAmount = 0.06f;
            mo.breathPeriod = 2.6f;
            img.gameObject.SetActive(false);
            return img.gameObject;
        }

        // nút tròn sticker có icon giữa (nhãn chữ tắt), như hàng lọc của hộp chọn đội
        static SketchButton Chip(UiKit kit, Transform parent, string name, string iconName, out Image icon)
        {
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonRound.gameObject, parent)).GetComponent<SketchButton>();
            b.name = name;
            var rt = b.Rect;
            rt.sizeDelta = new Vector2(ChipSize, ChipSize);
            var le = b.GetComponent<LayoutElement>();
            if (!le) le = b.gameObject.AddComponent<LayoutElement>();
            le.preferredWidth = le.preferredHeight = ChipSize;
            le.minWidth = le.minHeight = ChipSize;
            if (b.Label)
            {
                b.Label.text = "";
                b.Label.gameObject.SetActive(false);
            }
            b.SetRole(BtnColor.Paper);
            icon = Img(rt, "icon", Icon(iconName), Color.white);
            icon.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(IconSize, IconSize));
            return b;
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

        static Transform Find(Transform t, string name)
        {
            foreach (var c in t.GetComponentsInChildren<Transform>(true))
                if (c.name == name) return c;
            return null;
        }

        // xoá con trực tiếp tên name (dựng lại thì không nhân đôi)
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

        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, TextAlignmentOptions align)
        {
            var t = Node(parent, name, typeof(TextMeshProUGUI)).GetComponent<TextMeshProUGUI>();
            t.font = font;
            t.fontSize = size;
            t.color = color;
            t.alignment = align;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = "";
            return t;
        }
    }
}
