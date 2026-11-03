// AFK theo ải (người dùng chọn 2026-11-03: ải đã thắng có nút AFK). Menu "PokiClash/Prefab/AFK theo ải (nút, nhãn trên đảo)"
// dựng (chạy lại thì dựng lại):
// - Items/NhanAfk: nhãn trên bản đồ đảo dưới ải đội đang AFK: viên giấy màu rương AFK, đồng hồ, chữ "AFK", nhịp nhẹ;
//   gán vào Screens/Zone (ZoneScene.afkTagPrefab);
// - Dialogs/ChuanBiTran: nút "nut_afk" ("AFK ải này", cùng loại nút kit với Xuất trận, hẹp hơn) đứng trước Xuất trận trong hàng
//   nút cuối; gán StagePrepDialog.afkBtn;
// - Dialogs/Afk: nút "afk_doi_ai" ("Đổi ải", cùng loại nút kit với Nhận mảnh) sau nút Nhận mảnh; gán AfkPanel p.change.
// Chữ nhãn chép phông và viền từ tiêu đề hộp Chuẩn bị trận.
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class AfkStageMenu
    {
        const string TagPath = "Assets/04 Prefabs/Items/NhanAfk.prefab";
        const string ZonePath = "Assets/04 Prefabs/Screens/Zone.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const string AfkPath = "Assets/04 Prefabs/Dialogs/Afk.prefab";

        // cỡ nhãn trên bản đồ, cỡ nút AFK ở hộp chuẩn bị (Xuất trận 400 × 128)
        static readonly Vector2 TagSize = new Vector2(128, 52);
        const float PrepAfkW = 340;

        [MenuItem("PokiClash/Prefab/AFK theo ải (nút, nhãn trên đảo)", priority = 67)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            var art = Load<ArtLibrary>();
            Theme.Init(assets); // phông, sprite giấy, viền chữ nướng sẵn
            var kit = assets.prefabs;
            var pso = new SerializedObject(AssetDatabase.LoadAssetAtPath<GameObject>(PrepPath).GetComponent<StagePrepDialog>());
            var titleTpl = (TextMeshProUGUI)pso.FindProperty("p.title").objectReferenceValue;

            var tag = BuildTag(kit, art, titleTpl);
            Edit(ZonePath, root => SetRef(root.GetComponentInChildren<ZoneScene>(true), "afkTagPrefab", tag));
            Edit(PrepPath, root => PatchPrep(root, kit));
            Edit(AfkPath, root => PatchAfk(root, kit));
            AssetDatabase.SaveAssets();
            Debug.Log($"[AFK] Đã dựng {TagPath}; gán vào Zone; thêm nút AFK ải này (ChuanBiTran) và Đổi ải (Afk).");
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

        static RectTransform BuildTag(UiKit kit, ArtLibrary art, TextMeshProUGUI titleTpl)
        {
            var root = (GameObject)PrefabUtility.InstantiatePrefab(kit.panelThin.gameObject);
            try
            {
                root.name = "nhan_afk";
                var rt = (RectTransform)root.transform;
                rt.anchorMin = rt.anchorMax = new Vector2(0, 1); // như chấm ải: gốc trên trái của khung ảnh đảo
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = TagSize;
                var bg = root.GetComponent<Image>();
                bg.color = AfkPanel.ChestColor;
                bg.raycastTarget = false;

                var icon = new GameObject("dong_ho", typeof(RectTransform), typeof(Image)).GetComponent<Image>();
                icon.transform.SetParent(root.transform, false);
                icon.sprite = art ? art.Icon("clock") : null;
                icon.preserveAspect = true;
                icon.raycastTarget = false;
                icon.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(8, 0), new Vector2(40, 40), new Vector2(0, 0.5f));

                var t = Object.Instantiate(titleTpl.gameObject, root.transform, false).GetComponent<TextMeshProUGUI>();
                t.name = "chu";
                foreach (var c in t.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
                foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
                t.gameObject.SetActive(true);
                t.enableAutoSizing = false;
                t.fontSize = 30;
                t.color = Color.white;
                t.alignment = TextAlignmentOptions.Center;
                t.textWrappingMode = TextWrappingModes.NoWrap;
                t.overflowMode = TextOverflowModes.Overflow;
                t.raycastTarget = false;
                t.text = "AFK";
                t.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(46, 2), new Vector2(TagSize.x - 52, TagSize.y), new Vector2(0, 0.5f));

                var pulse = root.AddComponent<Pulse>();
                pulse.amount = 0.06f;
                pulse.period = 1.4f;
                return PrefabUtility.SaveAsPrefabAsset(root, TagPath).GetComponent<RectTransform>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // nút mới cùng loại nút kit với nút mẫu (Xuất trận, Nhận mảnh), đặt cùng hàng; tên trùng thì xoá cái cũ trước
        static SketchButton SiblingButton(UiKit kit, SketchButton like, string name)
        {
            var row = like.transform.parent;
            var old = row.Find(name);
            if (old) Object.DestroyImmediate(old.gameObject);
            var src = PrefabUtility.GetCorrespondingObjectFromSource(like);
            if (!src) src = kit.buttonBig;
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(src.gameObject, row)).GetComponent<SketchButton>();
            b.name = name;
            var size = like.Rect.sizeDelta;
            b.Rect.sizeDelta = size;
            var le = b.GetComponent<LayoutElement>();
            if (!le) le = b.gameObject.AddComponent<LayoutElement>();
            var likeLe = like.GetComponent<LayoutElement>();
            le.preferredWidth = size.x;
            le.preferredHeight = likeLe ? likeLe.preferredHeight : size.y;
            if (b.Label)
            {
                var l = like.Label;
                if (l) b.Label.fontSize = l.enableAutoSizing ? l.fontSizeMax : l.fontSize;
                b.Label.enableAutoSizing = true;
                b.Label.fontSizeMax = b.Label.fontSize;
                b.Label.fontSizeMin = b.Label.fontSize * 0.6f;
                b.Label.textWrappingMode = TextWrappingModes.NoWrap;
            }
            return b;
        }

        static void SetWidth(SketchButton b, float w)
        {
            b.Rect.sizeDelta = new Vector2(w, b.Rect.sizeDelta.y);
            b.GetComponent<LayoutElement>().preferredWidth = w;
        }

        static void PatchPrep(GameObject root, UiKit kit)
        {
            var prep = root.GetComponent<StagePrepDialog>();
            var so = new SerializedObject(prep);
            var go = (SketchButton)so.FindProperty("p.go").objectReferenceValue;
            var b = SiblingButton(kit, go, "nut_afk");
            SetWidth(b, PrepAfkW);
            b.transform.SetSiblingIndex(go.transform.GetSiblingIndex()); // đứng trước Xuất trận
            b.SetText("AFK ải này");
            b.SetRole(BtnColor.Blue);
            b.gameObject.SetActive(false); // hộp bật khi ải đã thắng
            so.FindProperty("afkBtn").objectReferenceValue = b;
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        static void PatchAfk(GameObject root, UiKit kit)
        {
            var panel = root.GetComponent<AfkPanel>();
            var so = new SerializedObject(panel);
            var claim = (SketchButton)so.FindProperty("p.claim").objectReferenceValue;
            var b = SiblingButton(kit, claim, "afk_doi_ai");
            b.transform.SetSiblingIndex(claim.transform.GetSiblingIndex() + 1);
            b.SetText("Đổi ải");
            b.SetRole(BtnColor.Blue);
            so.FindProperty("p.change").objectReferenceValue = b;
            so.ApplyModifiedPropertiesWithoutUndo();
        }
    }
}
