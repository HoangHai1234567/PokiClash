// Tia nước của chiêu bắn (StageView.Beam) và hiệu ứng đi kèm:
// - prefab Items/TiaNuoc (thân tia) và Items/AnhHieuUng (ảnh rời, đổi ảnh lúc dùng), chép từ Items/TranVong (StageFx có Image);
// - ảnh Assets/03 Art/Fx/: tia_nuoc, no_nuoc, giot_nuoc, vong_song, lap_lanh (ArtGen/Heroes/build_fx.py --xuat cắt nền ảnh GPT);
// - gán vào StageView của Screens/Battle.prefab (mở nội dung prefab, chỉ đổi các trường beamFx, imageFx, beamSplash, beamDrops,
//   beamRipple, beamSparkle). Chạy lại thì cập nhật ảnh.
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class BeamFxMenu
    {
        const string RingPath = "Assets/04 Prefabs/Items/TranVong.prefab";
        const string BeamPath = "Assets/04 Prefabs/Items/TiaNuoc.prefab";
        const string ImagePath = "Assets/04 Prefabs/Items/AnhHieuUng.prefab";
        const string ArtDir = "Assets/03 Art/Fx/";
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab";

        [MenuItem("PokiClash/Prefab/Sàn đấu: tia nước của chiêu bắn", priority = 62)]
        static void Build()
        {
            var beamArt = Art("tia_nuoc");
            if (!beamArt)
            {
                Debug.LogError($"[Tia nước] Thiếu ảnh {ArtDir}tia_nuoc.png (chạy py -3 -I ArtGen/Heroes/build_fx.py --xuat).");
                return;
            }
            var beamFx = MakeFx(BeamPath, "TiaNuoc", beamArt, new Vector2(0, 0.5f));
            var imageFx = MakeFx(ImagePath, "AnhHieuUng", null, new Vector2(0.5f, 0.5f));
            if (!beamFx || !imageFx) return;
            var battle = PrefabUtility.LoadPrefabContents(BattlePath);
            try
            {
                var stage = battle.GetComponentInChildren<StageView>(true);
                if (!stage)
                {
                    Debug.LogError("[Tia nước] Screens/Battle không có StageView.");
                    return;
                }
                var so = new SerializedObject(stage);
                so.FindProperty("beamFx").objectReferenceValue = beamFx;
                so.FindProperty("imageFx").objectReferenceValue = imageFx;
                so.FindProperty("beamSplash").objectReferenceValue = Art("no_nuoc");
                so.FindProperty("beamDrops").objectReferenceValue = Art("giot_nuoc");
                so.FindProperty("beamRipple").objectReferenceValue = Art("vong_song");
                so.FindProperty("beamSparkle").objectReferenceValue = Art("lap_lanh");
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(battle, BattlePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(battle);
            }
            Debug.Log($"[Tia nước] {BeamPath}, {ImagePath} và ảnh {ArtDir} đã gán vào StageView của {BattlePath}.");
        }

        // ảnh trong Assets/03 Art/Fx nhập thành Sprite (không mipmap); thiếu: null
        static Sprite Art(string name)
        {
            string path = ArtDir + name + ".png";
            var imp = AssetImporter.GetAtPath(path) as TextureImporter;
            if (!imp) return null;
            if (imp.textureType != TextureImporterType.Sprite || imp.mipmapEnabled)
            {
                imp.textureType = TextureImporterType.Sprite;
                imp.spriteImportMode = SpriteImportMode.Single;
                imp.mipmapEnabled = false;
                imp.alphaIsTransparency = true;
                imp.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        // prefab StageFx có Image chép từ Items/TranVong (giữ CanvasGroup, StageFx), ảnh và điểm neo theo dùng
        static StageFx MakeFx(string path, string name, Sprite sprite, Vector2 pivot)
        {
            if (!AssetDatabase.LoadAssetAtPath<GameObject>(path) && !AssetDatabase.CopyAsset(RingPath, path))
            {
                Debug.LogError($"[Tia nước] Không chép được {RingPath} thành {path}.");
                return null;
            }
            var go = PrefabUtility.LoadPrefabContents(path);
            try
            {
                go.name = name;
                var fx = go.GetComponent<StageFx>();
                var img = fx ? fx.Image : null;
                if (!img)
                {
                    Debug.LogError($"[Tia nước] {path} không có StageFx.Image.");
                    return null;
                }
                img.sprite = sprite;
                img.color = Color.white;
                img.type = Image.Type.Simple;
                img.preserveAspect = false;
                img.raycastTarget = false;
                ((RectTransform)go.transform).pivot = pivot;
                PrefabUtility.SaveAsPrefabAsset(go, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(go);
            }
            return AssetDatabase.LoadAssetAtPath<StageFx>(path);
        }
    }
}
