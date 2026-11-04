// Dựng thanh kinh nghiệm trên đầu máy bi vào Screens/Machine (phần đã có thì chỉ gán lại tham chiếu):
// - "thanh_kinh_nghiem" (MachineExpBar) trong khối máy, ngay trên mép trên máy, chừa nút "Tỉ lệ" bên phải;
//   gồm thanh kit Thanh loại EXP và vòng cấp chép từ thanh trên của App (vòng, cung EXP, đĩa, chữ "CẤP" và số cấp);
// - "lop_bay": lớp phủ cả khối máy, nằm trên cùng, cho sao EXP bay từ ô lên thanh (hạt là Items/HatMayBi).
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using PokiClash.UI;

namespace PokiClash.EditorTools
{
    public static class MachineExpBarMenu
    {
        const string MachinePath = "Assets/04 Prefabs/Screens/Machine.prefab";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const string BarPath = "Assets/04 Prefabs/Kit/Thanh.prefab";
        const string ItemPath = "Assets/04 Prefabs/Items/HatMayBi.prefab";
        const string BlockPath = "Canvas/An toan/Khung/Noi dung/khoi_may";

        // khối máy 1080 × 1530 (gốc trên trái): máy từ x 144,4 rộng 791,2, mép trên y 100; nút "Tỉ lệ" ở góc trên phải (x từ 866)
        static readonly Vector2 Pos = new Vector2(144, -4), Size = new Vector2(696, 92);
        const float BadgeScale = 0.78f, BarX = 62, BarH = 50;

        [MenuItem("PokiClash/Prefab/Máy bi: thanh kinh nghiệm", priority = 63)]
        public static void Build()
        {
            var item = AssetDatabase.LoadAssetAtPath<GameObject>(ItemPath);
            var barPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(BarPath);
            if (!item || !barPrefab)
            {
                Debug.LogError($"[Máy bi] Thiếu {ItemPath} hoặc {BarPath} (chạy menu \"Máy bi: hạt hiệu ứng\" trước)");
                return;
            }
            var contents = PrefabUtility.LoadPrefabContents(MachinePath);
            var app = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                var block = contents.transform.Find(BlockPath);
                if (!block)
                {
                    Debug.LogError("[Máy bi] Không thấy " + BlockPath + " trong " + MachinePath);
                    return;
                }
                var root = block.Find("thanh_kinh_nghiem") as RectTransform;
                bool built = false;
                if (!root)
                {
                    root = BuildBar(block, barPrefab, app);
                    if (!root) return;
                    built = true;
                }
                var layer = block.Find("lop_bay") as RectTransform;
                if (!layer)
                {
                    var go = new GameObject("lop_bay", typeof(RectTransform));
                    layer = (RectTransform)go.transform;
                    layer.SetParent(block, false);
                    layer.Stretch();
                }
                layer.SetAsLastSibling();

                var view = root.GetComponent<MachineExpBar>();
                var bar = root.GetComponentInChildren<UiBar>(true);
                var badge = root.Find("vong_cap") as RectTransform;
                var arc = badge ? badge.Find("cung_exp")?.GetComponent<Image>() : null;
                TextMeshProUGUI lv = null;
                if (badge)
                    foreach (var t in badge.GetComponentsInChildren<TextMeshProUGUI>(true))
                        if (t.name == "so_cap") lv = t;
                view.Setup(bar, arc, lv, badge, layer, item.GetComponent<Image>());
                EditorUtility.SetDirty(view);

                var scene = contents.GetComponent<MachineScene>();
                var so = new SerializedObject(scene);
                so.FindProperty("p.expBar").objectReferenceValue = view;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, MachinePath);
                Debug.Log($"[Máy bi] {(built ? "Dựng" : "Gán lại")} thanh kinh nghiệm trong {MachinePath}" + (lv ? "" : " (không thấy chữ số cấp)"));
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(app);
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        static RectTransform BuildBar(Transform block, GameObject barPrefab, GameObject app)
        {
            var top = app.GetComponentInChildren<TopBars>(true);
            var ring = top ? top.transform.Find("Hud/vong_cap") : null;
            if (!ring)
            {
                Debug.LogError("[Máy bi] Không thấy vòng cấp Hud/vong_cap của thanh trên trong " + AppPath);
                return null;
            }
            // chữ số cấp của thanh trên (TopBars.lvText): nhớ đường đi theo thứ tự con (hai chữ cùng tên "chu") để đặt tên cho bản chép
            var lvRef = new SerializedObject(top).FindProperty("lvText").objectReferenceValue as TextMeshProUGUI;
            var lvPath = new System.Collections.Generic.List<int>();
            for (var t = lvRef ? lvRef.transform : null; t && t != ring; t = t.parent) lvPath.Insert(0, t.GetSiblingIndex());

            var go = new GameObject("thanh_kinh_nghiem", typeof(RectTransform), typeof(MachineExpBar));
            var root = (RectTransform)go.transform;
            root.SetParent(block, false);
            root.Place(new Vector2(0, 1), Pos, Size, new Vector2(0, 1));
            // ngay sau mặt máy: dưới nút và lớp bay
            var machine = block.Find("May");
            if (machine) root.SetSiblingIndex(machine.GetSiblingIndex() + 1);

            var barGo = (GameObject)PrefabUtility.InstantiatePrefab(barPrefab, root);
            barGo.name = "thanh_exp";
            var bar = barGo.GetComponent<UiBar>();
            var bso = new SerializedObject(bar);
            bso.FindProperty("kind").enumValueIndex = (int)UiBar.Kind.Exp;
            bso.ApplyModifiedPropertiesWithoutUndo();
            bar.SetKind(UiBar.Kind.Exp);
            ((RectTransform)barGo.transform).Place(new Vector2(0, 0.5f), new Vector2(BarX, 0), new Vector2(Size.x - BarX, BarH), new Vector2(0, 0.5f));

            var badge = (RectTransform)Object.Instantiate(ring.gameObject, root).transform;
            badge.name = "vong_cap";
            var le = badge.GetComponent<LayoutElement>();
            if (le) Object.DestroyImmediate(le);
            badge.Place(new Vector2(0, 0.5f), new Vector2(124 * BadgeScale / 2, 0), new Vector2(124, 124), new Vector2(0.5f, 0.5f));
            badge.localScale = Vector3.one * BadgeScale;
            badge.SetAsLastSibling();
            Transform num = lvPath.Count > 0 ? badge : null;
            foreach (int i in lvPath) num = num && i < num.childCount ? num.GetChild(i) : null;
            if (num) num.name = "so_cap";
            return root;
        }
    }
}
