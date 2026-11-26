// Vá bộ bài tráo vào Screens/Battle theo luật prefab (2026-11-27; trước đó DraftDeck tự dựng lớp, khung viền, material lúc chạy):
// - material viền the_aura_Rare / _Epic / _Legend trong Assets/03 Art/Shaders: chép material gốc the_aura, thông số ở DraftDeck.StyleAura;
// - prefab mục Items/VienHiemThe: Image không nhận chạm, cỡ DraftDeck.AuraSize (DraftDeck sinh từ pool, gán material theo độ hiếm);
// - DraftDeck trên ô thẻ chọn (p.offer của BattleView); lớp "bo_bai" (con đầu) và "la_bay" (con cuối) trong ô thẻ chọn; lớp "vien_hiem_the"
//   ngay trước hàng thẻ (p.qRow) trong cùng cha.
// Chạy lại được nhiều lần: tìm lớp theo tên, ghi đè material và prefab mục (giữ GUID).
using PokiClash.Core;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class DraftDeckMenu
    {
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab";
        const string AuraItemPath = "Assets/04 Prefabs/Items/VienHiemThe.prefab";
        const string BaseMatPath = "Assets/03 Art/Shaders/Resources/the_aura.mat";
        static string MatPath(Rarity r) => $"Assets/03 Art/Shaders/the_aura_{r}.mat";

        [MenuItem("PokiClash/Prefab/Trận/Bộ bài tráo: lớp + viền độ hiếm", priority = 80)]
        public static void Build()
        {
            var mats = BuildMats();
            if (mats == null) return;
            var aura = BuildAuraItem();
            PatchBattle(aura, mats);
        }

        static Material[] BuildMats()
        {
            var baseMat = AssetDatabase.LoadAssetAtPath<Material>(BaseMatPath);
            if (!baseMat)
            {
                Debug.LogError("[Bộ bài] Không thấy material gốc " + BaseMatPath);
                return null;
            }
            var mats = new Material[3];
            for (int i = 0; i < 3; i++)
            {
                var r = (Rarity)((int)Rarity.Rare + i);
                var path = MatPath(r);
                var m = AssetDatabase.LoadAssetAtPath<Material>(path);
                if (!m)
                {
                    m = new Material(baseMat) { name = "the_aura_" + r };
                    AssetDatabase.CreateAsset(m, path);
                }
                else
                {
                    m.shader = baseMat.shader;
                    m.CopyPropertiesFromMaterial(baseMat);
                }
                DraftDeck.StyleAura(m, r);
                EditorUtility.SetDirty(m);
                mats[i] = m;
            }
            AssetDatabase.SaveAssets();
            return mats;
        }

        static Image BuildAuraItem()
        {
            var go = new GameObject("vien", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image)) { layer = 5 };
            try
            {
                var rt = (RectTransform)go.transform;
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = DraftDeck.AuraSize;
                var img = go.GetComponent<Image>();
                img.raycastTarget = false;
                img.color = new Color(0, 0, 0, 0); // DraftDeck nâng dần độ đậm khi lật thẻ
                return PrefabUtility.SaveAsPrefabAsset(go, AuraItemPath).GetComponent<Image>();
            }
            finally
            {
                Object.DestroyImmediate(go);
            }
        }

        static void PatchBattle(Image aura, Material[] mats)
        {
            var contents = PrefabUtility.LoadPrefabContents(BattlePath);
            try
            {
                var view = contents.GetComponentInChildren<BattleView>(true);
                if (!view)
                {
                    Debug.LogError("[Bộ bài] Không thấy BattleView trong " + BattlePath);
                    return;
                }
                var so = new SerializedObject(view);
                var offer = so.FindProperty("p.offer").objectReferenceValue as RectTransform;
                var qRow = so.FindProperty("p.qRow").objectReferenceValue as RectTransform;
                if (!offer || !qRow || !(qRow.parent is RectTransform host))
                {
                    Debug.LogError("[Bộ bài] Thiếu p.offer / p.qRow (hoặc hàng thẻ không có cha) trong " + BattlePath);
                    return;
                }

                var deck = offer.GetComponent<DraftDeck>();
                if (!deck) deck = offer.gameObject.AddComponent<DraftDeck>();

                var deckL = Layer(offer, "bo_bai");
                deckL.anchorMin = deckL.anchorMax = new Vector2(0.5f, 1);
                deckL.pivot = new Vector2(0.5f, 0.5f);
                deckL.SetSiblingIndex(0);

                var fly = Layer(offer, "la_bay");
                Stretch(fly, offer.pivot);
                fly.SetAsLastSibling();

                var auraL = Layer(host, "vien_hiem_the");
                Stretch(auraL, host.pivot);
                int qi = qRow.GetSiblingIndex();
                auraL.SetSiblingIndex(auraL.GetSiblingIndex() < qi ? qi - 1 : qi);

                var dso = new SerializedObject(deck);
                dso.FindProperty("deckLayer").objectReferenceValue = deckL;
                dso.FindProperty("auraHost").objectReferenceValue = auraL;
                dso.FindProperty("flyHost").objectReferenceValue = fly;
                dso.FindProperty("auraPrefab").objectReferenceValue = aura;
                var arr = dso.FindProperty("auraMats");
                arr.arraySize = mats.Length;
                for (int i = 0; i < mats.Length; i++) arr.GetArrayElementAtIndex(i).objectReferenceValue = mats[i];
                dso.ApplyModifiedPropertiesWithoutUndo();

                if (!deck.Baked) Debug.LogError("[Bộ bài] Vá xong mà DraftDeck vẫn thiếu tham chiếu");
                PrefabUtility.SaveAsPrefabAsset(contents, BattlePath);
                Debug.Log("[Bộ bài] Đã vá " + BattlePath + ": DraftDeck, bo_bai, la_bay, vien_hiem_the, " + AuraItemPath + ", 3 material viền");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        static RectTransform Layer(Transform parent, string name)
        {
            if (parent.Find(name) is RectTransform found) return found;
            var go = new GameObject(name, typeof(RectTransform)) { layer = parent.gameObject.layer };
            var rt = (RectTransform)go.transform;
            rt.SetParent(parent, false);
            return rt;
        }

        static void Stretch(RectTransform rt, Vector2 pivot)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = pivot;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
        }
    }
}
