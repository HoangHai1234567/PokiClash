// Dựng prefab bệ ải Items/BeAi (ZoneNode) từ mảnh kit: vầng sáng, bệ, chân dung (kit ChanDung), vùng chạm, bảng tên (kit KhungMong)
// có huy hiệu số (kit Nut_Tron), khoá, dấu qua, vương miện, tên tướng, cấp (chữ chép từ khung ải tiếp theo của Screens/Zone).
// Gán làm nút ải của Screens/Zone (thay Items/NutAi cũ). Cỡ và chỗ đặt tính lúc chạy trong ZoneNode.Bind.
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class ZoneNodeMenu
    {
        const string ZonePath = "Assets/04 Prefabs/Screens/Zone.prefab";
        const string NodePath = "Assets/04 Prefabs/Items/BeAi.prefab";
        const string GlowPath = "Assets/03 Art/Islands/be_glow.png";

        [MenuItem("PokiClash/Prefab/Bệ ải (BeAi)", priority = 63)]
        static void Build()
        {
            var kit = AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));
            var zoneAsset = AssetDatabase.LoadAssetAtPath<GameObject>(ZonePath).GetComponent<ZoneScene>();
            var zso = new SerializedObject(zoneAsset);
            var titleTpl = (TextMeshProUGUI)zso.FindProperty("p.nextTitle").objectReferenceValue;
            var smallTpl = (TextMeshProUGUI)zso.FindProperty("p.level").objectReferenceValue;

            var root = new GameObject("be_ai", typeof(RectTransform), typeof(ZoneNode));
            try
            {
                var glow = NewImage("vang_sang", root.transform, AssetDatabase.LoadAssetAtPath<Sprite>(GlowPath));
                var pulse = glow.gameObject.AddComponent<Pulse>();
                pulse.amount = 0.12f;
                pulse.period = 1.3f;
                var pedestal = NewImage("be", root.transform, null);
                var hero = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, root.transform)).GetComponent<HeroPortrait>();
                hero.name = "tuong";
                foreach (var img in hero.GetComponentsInChildren<Image>(true)) img.raycastTarget = false;
                var hit = NewImage("cham", root.transform, null);
                hit.color = new Color(1, 1, 1, 0);
                hit.raycastTarget = true;
                var hitClick = hit.gameObject.AddComponent<ClickCatcher>();

                var plate = ((GameObject)PrefabUtility.InstantiatePrefab(kit.panelThin.gameObject, root.transform)).GetComponent<Image>();
                plate.name = "bang_ten";
                plate.raycastTarget = true;
                var plateClick = plate.gameObject.AddComponent<ClickCatcher>();
                var badge = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonRound.gameObject, plate.transform)).GetComponent<SketchButton>();
                badge.name = "so_ai";
                var lockIcon = NewImage("khoa", badge.transform, null);
                var check = NewImage("da_qua", badge.transform, null);
                var crown = NewImage("vuong_mien", badge.transform, null);
                var heroName = Text(titleTpl, plate.transform, "ten_tuong", 28);
                var level = Text(smallTpl, plate.transform, "cap", 21);

                root.GetComponent<ZoneNode>().Setup(new ZoneNode.Parts
                {
                    glow = glow, glowPulse = pulse, pedestal = pedestal, hero = hero, hit = hit, hitClick = hitClick,
                    plate = plate, plateClick = plateClick, badge = badge, lockIcon = lockIcon, check = check, crown = crown,
                    heroName = heroName, level = level,
                });
                var prefab = PrefabUtility.SaveAsPrefabAsset(root, NodePath).GetComponent<ZoneNode>();

                var contents = PrefabUtility.LoadPrefabContents(ZonePath);
                try
                {
                    var so = new SerializedObject(contents.GetComponent<ZoneScene>());
                    so.FindProperty("nodePrefab").objectReferenceValue = prefab;
                    so.ApplyModifiedPropertiesWithoutUndo();
                    PrefabUtility.SaveAsPrefabAsset(contents, ZonePath);
                }
                finally
                {
                    PrefabUtility.UnloadPrefabContents(contents);
                }
                Debug.Log($"[Đảo] Đã dựng {NodePath} và gán làm nút ải của {ZonePath}.");
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static Image NewImage(string name, Transform parent, Sprite sprite)
        {
            var img = new GameObject(name, typeof(RectTransform), typeof(Image)).GetComponent<Image>();
            img.transform.SetParent(parent, false);
            img.sprite = sprite;
            img.raycastTarget = false;
            img.preserveAspect = true;
            return img;
        }

        // chữ một dòng, canh trái, chép phông và viền từ chữ có sẵn
        static TextMeshProUGUI Text(TextMeshProUGUI from, Transform parent, string name, float size)
        {
            var t = Object.Instantiate(from.gameObject, parent, false).GetComponent<TextMeshProUGUI>();
            t.name = name;
            foreach (var c in t.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            t.enableAutoSizing = true;
            t.fontSizeMax = size;
            t.fontSizeMin = size * 0.6f;
            t.alignment = TextAlignmentOptions.MidlineLeft;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = "";
            return t;
        }
    }
}
