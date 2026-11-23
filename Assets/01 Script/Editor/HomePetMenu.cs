// Vầng sáng đêm của thú (FarmPet.Parts.aura; người dùng 2026-11-20: tướng ở màn Nhà "buổi đêm làm chúng phát sáng nhẹ"): ảnh anim_glow
// cộng sáng (UIAdditive), con đầu của "than" (sau "lat": sau lưng tướng, nhún nghiêng theo thân), tắt sẵn; FarmPet bật khi màn Nhà
// (UseRig) vào chạng vạng, màu hệ pha trắng, thở nhẹ. FarmSceneMenu.BuildPet gọi MakeAura khi dựng lại prefab; menu dưới vá prefab
// Items/ThuTrangTrai đang có mà không dựng lại cả cảnh Trang trại.
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HomePetMenu
    {
        const string PetPath = "Assets/04 Prefabs/Items/ThuTrangTrai.prefab";
        const string GlowPath = "Assets/03 Art/Islands/Anim/anim_glow.png";
        const string AddPath = "Assets/Resources/UIAdditive.mat";

        // dựng ảnh vầng sáng làm con đầu của body (gốc ở chân)
        public static Image MakeAura(RectTransform body)
        {
            var go = new GameObject("vang_sang", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
            var rt = (RectTransform)go.transform;
            rt.SetParent(body, false);
            rt.SetAsFirstSibling();
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = new Vector2(0, FarmPet.Height * 0.42f);
            rt.sizeDelta = new Vector2(FarmPet.Height * 1.7f, FarmPet.Height * 1.45f);
            var img = go.GetComponent<Image>();
            img.sprite = AssetDatabase.LoadAssetAtPath<Sprite>(GlowPath);
            img.material = AssetDatabase.LoadAssetAtPath<Material>(AddPath);
            img.raycastTarget = false;
            img.color = new Color(1, 1, 1, 0);
            go.SetActive(false);
            if (!img.sprite || !img.material) Debug.LogWarning("[Nhà] Thiếu " + GlowPath + " hoặc " + AddPath + " cho vầng sáng thú");
            return img;
        }

        [MenuItem("PokiClash/Prefab/Nhà và side meta/Nhà: vầng sáng đêm cho thú (ThuTrangTrai)", priority = 64)]
        static void Patch()
        {
            var root = PrefabUtility.LoadPrefabContents(PetPath);
            try
            {
                var pet = root.GetComponent<FarmPet>();
                var so = pet ? new SerializedObject(pet) : null;
                var body = so?.FindProperty("p.body").objectReferenceValue as RectTransform;
                if (!body)
                {
                    Debug.LogError("[Nhà] " + PetPath + " thiếu FarmPet / p.body");
                    return;
                }
                var old = body.Find("vang_sang");
                if (old) Object.DestroyImmediate(old.gameObject);
                so.FindProperty("p.aura").objectReferenceValue = MakeAura(body);
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(root, PetPath);
                Debug.Log("[Nhà] Đã gắn vầng sáng đêm vào " + PetPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }
    }
}
