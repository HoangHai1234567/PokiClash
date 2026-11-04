// Hộp Chuẩn bị trận hiện rõ chỉ số địch (người dùng dặn 2026-11-04: "chưa thể hiện được rõ công/thủ/máu/sức mạnh của địch").
// Menu "PokiClash/Prefab/Hộp chuẩn bị: chỉ số địch" dựng (chạy lại thì dựng lại, không dời chồng):
// - Items/DoiThu (PrepFoe): khối "chi_so" ở đáy ô, 3 hàng to Máu, Công, Thủ (icon tim, kiếm, khiên; số của địch; không so với tướng
//   người chơi, người dùng dặn), gán PrepFoe.stats; tên, nhãn hệ, lực chiến, dòng ghi chú dời lên PrepFoe.StatsH (chân dung do PrepFoe
//   đặt lúc chạy);
// - Dialogs/ChuanBiTran: khung "doi_thu" cao FrameH + PrepFoe.StatsH; gán chữ đầu mục "Đối thủ" vào StagePrepDialog.foeTitle (ghi luật
//   tiến hóa khi địch tiến hóa trong trận).
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class PrepStatsMenu
    {
        const string FoePath = "Assets/04 Prefabs/Items/DoiThu.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const float FrameH = 360; // khung đối thủ trừ phần hàng chỉ số (chân dung 250–270 đặt trên hàng chỉ số)
        const float RowH = 42, RowW = 210, IconS = 40;
        static readonly string[] Icons = { "heart", "sword", "shield" };
        static readonly string[] Rows = { "mau", "cong", "thu" };

        static ArtLibrary art;

        [MenuItem("PokiClash/Prefab/Hộp chuẩn bị: chỉ số địch", priority = 67)]
        static void Build()
        {
            Theme.Init(Load<UiAssets>()); // phông, sprite giấy, viền chữ nướng sẵn
            art = Load<ArtLibrary>();
            Edit(FoePath, PatchFoe);
            Edit(PrepPath, PatchPrep);
            AssetDatabase.SaveAssets();
            Debug.Log($"[Chuẩn bị] Đã thêm hàng Máu, Công, Thủ vào {FoePath}; khung đối thủ {PrepPath} cao {FrameH + PrepFoe.StatsH}.");
        }

        static void PatchFoe(GameObject root)
        {
            // tên, chữ cấp cũ, nhãn hệ, lực chiến, dòng ghi chú: chỗ cũ (Popup gọn) dời lên StatsH; đặt tuyệt đối nên chạy lại không dời chồng
            var so = new SerializedObject(root.GetComponent<PrepFoe>());
            float up = PrepFoe.StatsH;
            Rt(so, "heroName").anchoredPosition = new Vector2(0, 74 + up);
            Rt(so, "level").anchoredPosition = new Vector2(60, 40 + up);
            Rt(so, "elem").anchoredPosition = new Vector2(-62, 40 + up);
            Rt(so, "boss").anchoredPosition = new Vector2(0, 10 + up);
            var power = Rt(so, "power");
            if (power) ((RectTransform)power.parent).anchoredPosition = new Vector2(-14, 37 + up);

            Remove(root.transform, "chi_so");
            var block = Node(root.transform, "chi_so");
            block.Place(new Vector2(0.5f, 0), new Vector2(0, 18), new Vector2(RowW, RowH * 3), new Vector2(0.5f, 0)); // chừa viền đáy khung
            var arr = so.FindProperty("stats");
            arr.arraySize = Rows.Length;
            for (int i = 0; i < Rows.Length; i++)
            {
                var row = Node(block, "hang_" + Rows[i]);
                row.Place(new Vector2(0.5f, 0), new Vector2(0, (Rows.Length - 1 - i) * RowH), new Vector2(RowW, RowH), new Vector2(0.5f, 0));
                Img(row, "icon", Icon(Icons[i]), Color.white).rectTransform
                    .Place(new Vector2(0, 0.5f), Vector2.zero, new Vector2(IconS, IconS), new Vector2(0, 0.5f));
                var value = Text(row, "so", Theme.Title, 38, Theme.Ink2, TextAlignmentOptions.MidlineLeft);
                value.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(IconS + 12, 2), new Vector2(RowW - IconS - 12, RowH), new Vector2(0, 0.5f));
                value.text = "0";
                arr.GetArrayElementAtIndex(i).objectReferenceValue = value;
            }
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        static void PatchPrep(GameObject root)
        {
            var foes = Find(root.transform, "doi_thu");
            foes.GetComponent<LayoutElement>().preferredHeight = FrameH + PrepFoe.StatsH;
            // chữ đầu mục ngay trước khung đối thủ
            var title = foes.parent.GetChild(foes.GetSiblingIndex() - 1).GetComponent<TextMeshProUGUI>();
            if (!title || !title.text.StartsWith("Đối thủ"))
            {
                Debug.LogError("[Chuẩn bị] Không thấy chữ \"Đối thủ\" ngay trước khung doi_thu");
                return;
            }
            var so = new SerializedObject(root.GetComponent<StagePrepDialog>());
            so.FindProperty("foeTitle").objectReferenceValue = title;
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        // ---------- công cụ ----------

        static Sprite Icon(string n) => art ? art.Icon(n) : null;

        // RectTransform của tham chiếu prop trong component (chữ, nhãn hệ, GameObject)
        static RectTransform Rt(SerializedObject so, string prop)
        {
            var o = so.FindProperty(prop).objectReferenceValue;
            return o is GameObject go ? (RectTransform)go.transform : o is Component c ? (RectTransform)c.transform : null;
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

        static void Remove(Transform parent, string name)
        {
            for (int i = parent.childCount - 1; i >= 0; i--)
                if (parent.GetChild(i).name == name) Object.DestroyImmediate(parent.GetChild(i).gameObject);
        }

        static RectTransform Node(Transform parent, string name)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        static Image Img(Transform parent, string name, Sprite sprite, Color color)
        {
            var img = Node(parent, name).gameObject.AddComponent<Image>();
            Theme.SetSprite(img, sprite);
            img.preserveAspect = true;
            img.color = color;
            img.raycastTarget = false;
            return img;
        }

        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, TextAlignmentOptions align)
        {
            var t = Node(parent, name).gameObject.AddComponent<TextMeshProUGUI>();
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
