// Trận: mặt địch ở góc trên trái sân và dấu X cho tướng gục (người dùng chốt 2026-11-03).
// - Items/TranMatDich (FoeFace): khung giấy mảnh của kit, chân dung (kit) trong ô có mặt nạ (lúc chạy HeroArt.FitHead phóng cho
//   đầu lấp ô), dấu X đỏ (ẩn). Luôn dựng lại.
// - Items/TranDongDoi (TeamSlot, hàng đội phía dưới): thêm dấu X đỏ "dau_x", không mờ theo ô (CanvasGroup riêng bỏ qua ô cha).
// - Screens/Battle: hàng "hang_dich" trong lớp bảng của sân (StageView.plateLayer), neo góc trên trái; gán BattleView.p.foeRow,
//   p.foePrefab.
// Hai prefab sau đã có phần này thì để nguyên (prefab dùng chung với các phiên khác); xoá dau_x / hang_dich để dựng lại.
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class FoeRowMenu
    {
        const string FacePath = "Assets/04 Prefabs/Items/TranMatDich.prefab";
        const string SlotPath = "Assets/04 Prefabs/Items/TranDongDoi.prefab";
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab";
                const float Size = 88, Gap = 10, Margin = 20;
        static readonly Color Red = new Color32(0xe8, 0x55, 0x3f, 0xff), Ink = new Color32(0x2b, 0x21, 0x18, 0xff);

        [MenuItem("PokiClash/Prefab/Trận: mặt địch góc trên, dấu X tướng gục", priority = 65)]
        public static void Build()
        {
            var kit = AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));
            var face = BuildFace(kit);
            PatchSlot();
            PatchBattle(face);
        }

        static FoeFace BuildFace(UiKit kit)
        {
            var root = new GameObject("TranMatDich", typeof(RectTransform));
            try
            {
                var rt = (RectTransform)root.transform;
                rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(Size, Size);

                var bg = ((GameObject)PrefabUtility.InstantiatePrefab(kit.panelThin.gameObject, rt)).GetComponent<Image>();
                bg.name = "nen";
                bg.raycastTarget = false;
                Stretch(bg.rectTransform, 0);

                var mask = new GameObject("khung", typeof(RectTransform), typeof(RectMask2D)).transform as RectTransform;
                mask.SetParent(rt, false);
                Stretch(mask, 6);

                var por = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, mask)).GetComponent<HeroPortrait>();
                por.name = "chan_dung";
                var prt = por.Rect;
                prt.anchorMin = prt.anchorMax = new Vector2(0.5f, 0.5f); // FitHead đặt cỡ, chỗ lúc chạy
                var porImg = (Image)new SerializedObject(por).FindProperty("body").objectReferenceValue;
                foreach (var g in por.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;

                var cross = Cross(rt, Size);
                cross.SetActive(false);

                var ff = root.AddComponent<FoeFace>();
                ff.Setup(bg, por, porImg, cross);
                var saved = PrefabUtility.SaveAsPrefabAsset(root, FacePath).GetComponent<FoeFace>();
                Debug.Log("[Trận] Dựng " + FacePath);
                return saved;
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static void PatchSlot()
        {
            var contents = PrefabUtility.LoadPrefabContents(SlotPath);
            try
            {
                var slot = contents.GetComponent<TeamSlot>();
                var rt = (RectTransform)contents.transform;
                if (rt.Find("dau_x")) return; // đã có
                var cross = Cross(rt, Mathf.Min(rt.rect.width, rt.rect.height) * 0.85f);
                var cg = cross.AddComponent<CanvasGroup>();
                cg.ignoreParentGroups = true; // ô gục mờ 50%, dấu X vẫn rõ
                cg.blocksRaycasts = false;
                cross.SetActive(false);
                var so = new SerializedObject(slot);
                so.FindProperty("cross").objectReferenceValue = cross;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, SlotPath);
                Debug.Log("[Trận] Thêm dấu X vào " + SlotPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        static void PatchBattle(FoeFace face)
        {
            var contents = PrefabUtility.LoadPrefabContents(BattlePath);
            try
            {
                var view = contents.GetComponentInChildren<BattleView>(true);
                var stage = contents.GetComponentInChildren<StageView>(true);
                var layer = stage.PlateLayer;
                if (layer.Find("hang_dich")) return; // đã có (ô mặt địch dựng lại cùng đường dẫn, prefab vẫn trỏ đúng)
                var row = new GameObject("hang_dich", typeof(RectTransform), typeof(HorizontalLayoutGroup)).transform as RectTransform;
                row.SetParent(layer, false);
                row.anchorMin = row.anchorMax = row.pivot = new Vector2(0, 1);
                row.anchoredPosition = new Vector2(Margin, -Margin);
                row.sizeDelta = new Vector2(Size * 3 + Gap * 2, Size);
                var hl = row.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = Gap;
                hl.childAlignment = TextAnchor.UpperLeft;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var so = new SerializedObject(view);
                so.FindProperty("p.foeRow").objectReferenceValue = row;
                so.FindProperty("p.foePrefab").objectReferenceValue = face;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, BattlePath);
                Debug.Log("[Trận] Dựng hàng mặt địch hang_dich trong " + BattlePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // dấu X đỏ viền mực phủ giữa ô (hai vạch chéo), không nhận chạm
        static GameObject Cross(RectTransform parent, float size)
        {
            var x = new GameObject("dau_x", typeof(RectTransform)).transform as RectTransform;
            x.SetParent(parent, false);
            Stretch(x, 0);
            for (int i = 0; i < 2; i++)
            {
                var bar = new GameObject("gach_" + (i + 1), typeof(RectTransform), typeof(CanvasRenderer), typeof(Image), typeof(Outline));
                var img = bar.GetComponent<Image>();
                img.color = Red;
                img.raycastTarget = false;
                var o = bar.GetComponent<Outline>();
                o.effectColor = Ink;
                o.effectDistance = new Vector2(2.5f, -2.5f);
                var brt = (RectTransform)bar.transform;
                brt.SetParent(x, false);
                brt.anchorMin = brt.anchorMax = new Vector2(0.5f, 0.5f);
                brt.sizeDelta = new Vector2(size * 0.95f, Mathf.Max(8, size * 0.13f));
                brt.localEulerAngles = new Vector3(0, 0, i == 0 ? 45 : -45);
            }
            return x.gameObject;
        }

        static void Stretch(RectTransform rt, float inset)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.offsetMin = new Vector2(inset, inset);
            rt.offsetMax = new Vector2(-inset, -inset);
        }
    }
}
