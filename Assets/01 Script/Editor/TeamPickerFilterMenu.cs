// Hàng lọc và xếp của bể tướng (hộp chọn đội, Dialogs/ChonDoi; người dùng nhờ 2026-11-06). Menu "PokiClash/Prefab/Hộp chọn đội: lọc theo
// hệ, xếp" dựng (chạy lại thì dựng lại) hàng "loc" giữa tiêu đề và khung cuộn:
// - 7 nút tròn sticker 64 px: Tất cả (icon đội), Thủy, Hỏa, Kim, Mộc, Thổ (icon hệ), Khắc (mũi tên lên: tướng khắc địch chính);
// - nút viên "Xếp: lực chiến" bên phải (bấm đổi vòng lực chiến, sao, hệ).
// Gán vào TeamPickerDialog.SetupFilters; logic lọc, xếp, tô màu ở TeamPickerDialog.
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class TeamPickerFilterMenu
    {
        const string PickerPath = "Assets/04 Prefabs/Dialogs/ChonDoi.prefab";
        const float ChipSize = 64, IconSize = 40, RowH = 72;
        static readonly string[] ElemIcons = { "e_thuy", "e_hoa", "e_kim", "e_moc", "e_tho" };

        [MenuItem("PokiClash/Prefab/Hộp chọn đội: lọc theo hệ, xếp", priority = 66)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            var art = Load<ArtLibrary>();
            Theme.Init(assets);
            var kit = assets.prefabs;
            var root = PrefabUtility.LoadPrefabContents(PickerPath);
            try
            {
                var dlg = root.GetComponent<TeamPickerDialog>();
                var content = Find(root.transform, "noi_dung");
                var title = Find(root.transform, "tieu_de");
                if (!dlg || !content || !title)
                {
                    Debug.LogError("[Đội] ChonDoi thiếu noi_dung hoặc tieu_de.");
                    return;
                }
                var old = content.Find("loc");
                if (old) Object.DestroyImmediate(old.gameObject);

                var row = new GameObject("loc", typeof(RectTransform), typeof(HorizontalLayoutGroup), typeof(LayoutElement));
                row.transform.SetParent(content, false);
                row.transform.SetSiblingIndex(title.GetSiblingIndex() + 1);
                var hl = row.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = 8;
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var rowLe = row.GetComponent<LayoutElement>();
                rowLe.preferredHeight = RowH;
                rowLe.minHeight = RowH;

                var all = Chip(kit, art, row.transform, "loc_tat_ca", "team", out _);
                var elems = new SketchButton[ElemIcons.Length];
                var icons = new Image[ElemIcons.Length];
                for (int i = 0; i < ElemIcons.Length; i++) elems[i] = Chip(kit, art, row.transform, "loc_" + ElemIcons[i], ElemIcons[i], out icons[i]);
                var counter = Chip(kit, art, row.transform, "loc_khac", "up", out _);

                var gap = new GameObject("khe", typeof(RectTransform), typeof(LayoutElement));
                gap.transform.SetParent(row.transform, false);
                gap.GetComponent<LayoutElement>().preferredWidth = 10;

                var sort = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonTiny.gameObject, row.transform)).GetComponent<SketchButton>();
                sort.name = "nut_xep";
                sort.SetText("Xếp: lực chiến");
                sort.SetRole(BtnColor.Paper);
                sort.FitWidth();

                dlg.SetupFilters(rowLe, all, elems, icons, counter, sort);
                EditorUtility.SetDirty(dlg);
                PrefabUtility.SaveAsPrefabAsset(root, PickerPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            AssetDatabase.SaveAssets();
            Debug.Log($"[Đội] Đã dựng hàng lọc theo hệ và nút xếp trong {PickerPath}.");
        }

        // nút tròn sticker 64 px có icon giữa (nhãn chữ tắt)
        static SketchButton Chip(UiKit kit, ArtLibrary art, Transform parent, string name, string iconName, out Image icon)
        {
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonRound.gameObject, parent)).GetComponent<SketchButton>();
            b.name = name;
            var rt = b.Rect;
            rt.sizeDelta = new Vector2(ChipSize, ChipSize);
            var le = b.GetComponent<LayoutElement>() ?? b.gameObject.AddComponent<LayoutElement>();
            le.preferredWidth = le.preferredHeight = ChipSize;
            le.minWidth = le.minHeight = ChipSize;
            if (b.Label)
            {
                b.Label.text = "";
                b.Label.gameObject.SetActive(false);
            }
            b.SetRole(BtnColor.Paper);
            var go = new GameObject("icon", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(rt, false);
            ((RectTransform)go.transform).Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(IconSize, IconSize));
            icon = go.GetComponent<Image>();
            Theme.SetSprite(icon, art ? art.Icon(iconName) : null);
            icon.preserveAspect = true;
            icon.raycastTarget = false;
            return b;
        }

        static Transform Find(Transform t, string name)
        {
            if (t.name == name) return t;
            foreach (Transform c in t)
            {
                var r = Find(c, name);
                if (r) return r;
            }
            return null;
        }

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));
    }
}
