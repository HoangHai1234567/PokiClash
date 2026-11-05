// Dựng ô quà ở đầu thanh mốc của máy bi (Screens/Machine; phần đã có thì chỉ đặt lại chỗ và gán lại tham chiếu):
// - thanh mốc "thanh_Rage" (UiBar, mốc Huyền thoại rồi mốc quà) đổi gốc về giữa để nhún đều, ngắn lại chừa chỗ cho ô quà;
// - "o_qua": vòng tròn chép từ vòng cấp của thanh kinh nghiệm (vòng + đĩa giấy), đè lên đầu phải thanh; trong có rương kit
//   "ruong" (quà rương), icon "icon" (bi, XP, sao của mốc Huyền thoại) và số "so" ("+8"); chạm vào báo các mốc kế;
// - thanh mốc cũng chạm được (nút trong suốt), MachineScene gắn cùng hàm.
// Chạy sau menu "Máy bi: thanh kinh nghiệm" (cần vòng cấp để chép).
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class MachineGiftMenu
    {
        const string MachinePath = "Assets/04 Prefabs/Screens/Machine.prefab";
        const string ChestPath = "Assets/04 Prefabs/Kit/Ruong.prefab";
        const string BlockPath = "Canvas/An toan/Khung/Noi dung/khoi_may";

        // chỗ của thanh mốc cũ (neo trên phải khối máy): mép phải cách 60, đỉnh y 1453,6, dài 560, cao 54
        const float Right = 60, Top = 1453.6f, Len = 560, BarH = 54, Badge = 96, ChestW = 70, IconW = 58;

        [MenuItem("PokiClash/Prefab/Máy bi: mốc quà", priority = 65)]
        public static void Build()
        {
            var chestPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(ChestPath);
            if (!chestPrefab)
            {
                Debug.LogError("[Máy bi] Thiếu " + ChestPath);
                return;
            }
            var contents = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                var block = contents.transform.Find(BlockPath) as RectTransform;
                var bar = block ? block.Find("thanh_Rage") as RectTransform : null;
                var ring = block ? block.Find("thanh_kinh_nghiem/vong_cap") as RectTransform : null;
                var dem = block ? block.Find("dem")?.GetComponent<TextMeshProUGUI>() : null;
                if (!bar || !ring || !dem)
                {
                    Debug.LogError("[Máy bi] Không thấy thanh_Rage, thanh_kinh_nghiem/vong_cap hoặc dem trong " + MachinePath + " (chạy menu \"Máy bi: thanh kinh nghiệm\" trước)");
                    return;
                }
                float cy = -(Top + BarH / 2), badgeX = -(Right + Badge / 2);

                // thanh mốc: gốc giữa (nhún đều), từ mép trái cũ tới tâm ô quà
                float barLeft = -(Right + Len), barRight = badgeX;
                bar.Place(new Vector2(1, 1), new Vector2((barLeft + barRight) / 2, cy), new Vector2(barRight - barLeft, BarH), new Vector2(0.5f, 0.5f));
                bar.localScale = Vector3.one;
                var barBtn = bar.GetComponent<Button>();
                if (!barBtn) barBtn = bar.gameObject.AddComponent<Button>();
                barBtn.transition = Selectable.Transition.None;
                // chữ của thanh canh giữa phần không bị ô quà che
                var lbl = bar.Find("so") as RectTransform;
                if (lbl) lbl.offsetMax = new Vector2(-(Badge / 2 + 4), lbl.offsetMax.y);

                // ô quà
                var badge = block.Find("o_qua") as RectTransform;
                if (!badge)
                {
                    badge = (RectTransform)Object.Instantiate(ring.gameObject, block).transform;
                    badge.name = "o_qua";
                    // chỉ giữ vòng và đĩa giấy
                    for (int i = badge.childCount - 1; i >= 0; i--)
                    {
                        var c = badge.GetChild(i);
                        if (c.name != "dia") Object.DestroyImmediate(c.gameObject);
                    }
                }
                badge.SetSiblingIndex(bar.GetSiblingIndex() + 1);
                badge.Place(new Vector2(1, 1), new Vector2(badgeX, cy), new Vector2(124, 124), new Vector2(0.5f, 0.5f));
                badge.localScale = Vector3.one;
                badge.GetComponent<Image>().raycastTarget = true;
                float inner = 124; // con của ô quà tính theo cỡ gốc 124 rồi thu theo Badge
                badge.localScale = Vector3.one * (Badge / inner);

                var chest = badge.Find("ruong") as RectTransform;
                if (!chest)
                {
                    var go = (GameObject)PrefabUtility.InstantiatePrefab(chestPrefab, badge);
                    chest = (RectTransform)go.transform;
                    chest.name = "ruong";
                }
                var ci = chest.GetComponent<ChestIcon>();
                chest.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -2), new Vector2(ChestW * inner / Badge, ChestW * inner / Badge), new Vector2(0.5f, 0.5f));

                var icon = badge.Find("icon") as RectTransform;
                if (!icon)
                {
                    var go = new GameObject("icon", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                    icon = (RectTransform)go.transform;
                    icon.SetParent(badge, false);
                }
                icon.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 4), Vector2.one * IconW * inner / Badge, new Vector2(0.5f, 0.5f));
                var iconImg = icon.GetComponent<Image>();
                iconImg.raycastTarget = false;
                iconImg.preserveAspect = true;
                iconImg.gameObject.SetActive(false);

                var so = badge.Find("so") as RectTransform;
                if (!so)
                {
                    so = (RectTransform)Object.Instantiate(dem.gameObject, badge).transform;
                    so.name = "so";
                }
                so.SetAsLastSibling();
                so.Place(new Vector2(0.5f, 0), new Vector2(0, 32), new Vector2(150, 40), new Vector2(0.5f, 0.5f));
                var soText = so.GetComponent<TextMeshProUGUI>();
                soText.text = "+8";
                soText.alignment = TextAlignmentOptions.Center;
                soText.enableAutoSizing = false;
                soText.fontSize = 30;
                soText.raycastTarget = false;
                so.gameObject.SetActive(false);

                var btn = badge.GetComponent<Button>();
                if (!btn) btn = badge.gameObject.AddComponent<Button>();
                btn.transition = Selectable.Transition.None;

                var scene = contents.GetComponent<MachineScene>();
                var sobj = new SerializedObject(scene);
                sobj.FindProperty("p.giftBadge").objectReferenceValue = badge;
                sobj.FindProperty("p.giftChest").objectReferenceValue = ci;
                sobj.FindProperty("p.giftIcon").objectReferenceValue = iconImg;
                sobj.FindProperty("p.giftCount").objectReferenceValue = soText;
                sobj.FindProperty("p.giftButton").objectReferenceValue = btn;
                sobj.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, MachinePath);
                Debug.Log("[Máy bi] Dựng ô quà mốc trong " + MachinePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
