// Hạt chồng lớp phẳng trên sân đấu (HatLua, bộ Hỏa 2026-11-10):
// - ảnh Assets/03 Art/Fx/Hat/hat_*.png (ArtGen/Spine/xuat_hat.py) nhập thành Sprite không mipmap;
// - prefab Items/HatLua (một Image trắng, không bắt chạm) chép từ Items/HatMayBi;
// - trong StageView của Screens/Battle: ba lớp chứa cùng cấp với lớp tướng: HatDat, HatSau (ngay trước lớp tướng), HatTruoc (ngay
//   sau lớp tướng), mỗi lớp một Canvas con (dựng lại riêng, không kéo cả sân), neo như lớp hiệu ứng; gán hatPrefab, hatFloor,
//   hatBack, hatFront, hatSprites. Chạy lại thì cập nhật ảnh, không tạo trùng lớp.
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HatLuaMenu
    {
        const string ArtDir = "Assets/03 Art/Fx/Hat";
        const string SrcPrefab = "Assets/04 Prefabs/Items/HatMayBi.prefab";
        const string HatPrefab = "Assets/04 Prefabs/Items/HatLua.prefab";
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab";

        [MenuItem("PokiClash/Prefab/Sàn đấu: hạt lửa (bộ Hỏa)", priority = 63)]
        public static void Build()
        {
            var sprites = ImportSprites();
            if (sprites.Length == 0)
            {
                Debug.LogError($"[Hạt lửa] Thiếu ảnh {ArtDir}/hat_*.png (chạy py -3 -I ArtGen/Spine/xuat_hat.py).");
                return;
            }
            var prefab = MakePrefab();
            if (!prefab) return;
            var battle = PrefabUtility.LoadPrefabContents(BattlePath);
            try
            {
                var stage = battle.GetComponentInChildren<StageView>(true);
                if (!stage)
                {
                    Debug.LogError("[Hạt lửa] Screens/Battle không có StageView.");
                    return;
                }
                var so = new SerializedObject(stage);
                var actors = so.FindProperty("actorLayer").objectReferenceValue as RectTransform;
                var fx = so.FindProperty("fxLayer").objectReferenceValue as RectTransform;
                if (!actors || !fx)
                {
                    Debug.LogError("[Hạt lửa] StageView thiếu actorLayer hoặc fxLayer.");
                    return;
                }
                var parent = actors.parent;
                var floor = Layer(parent, "HatDat", fx);
                var back = Layer(parent, "HatSau", fx);
                var front = Layer(parent, "HatTruoc", fx);
                int ai = actors.GetSiblingIndex();
                floor.SetSiblingIndex(ai);
                back.SetSiblingIndex(ai + 1);
                front.SetSiblingIndex(actors.GetSiblingIndex() + 1);
                var van = ImportVan();
                Mang(floor, van);
                Mang(back, van);
                Mang(front, van);
                so.FindProperty("hatPrefab").objectReferenceValue = prefab;
                so.FindProperty("hatFloor").objectReferenceValue = floor;
                so.FindProperty("hatBack").objectReferenceValue = back;
                so.FindProperty("hatFront").objectReferenceValue = front;
                var arr = so.FindProperty("hatSprites");
                arr.arraySize = sprites.Length;
                for (int i = 0; i < sprites.Length; i++) arr.GetArrayElementAtIndex(i).objectReferenceValue = sprites[i];
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(battle, BattlePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(battle);
            }
            Debug.Log($"[Hạt lửa] {sprites.Length} ảnh, prefab {HatPrefab}, lớp HatDat/HatSau/HatTruoc đã gán vào StageView của {BattlePath}.");
        }

        const string DetailPath = "Assets/04 Prefabs/Dialogs/ChiTietTuong.prefab";

        // hộp chi tiết tướng: lớp hạt trong khung cắt ô xem (HatDat, HatSau đầu, HatTruoc cuối; neo giữa đáy ô, HeroViewer co theo
        // cỡ ô) và nút thứ 5 "Mana" (chép nút Chiêu, đặt sau nó; HeroDetailDialog.ClipIds[4] = Cast). Chạy lại không tạo trùng.
        [MenuItem("PokiClash/Prefab/Hộp chi tiết tướng: hạt lửa + nút Mana", priority = 64)]
        public static void BuildDetail()
        {
            var sprites = ImportSprites();
            var prefab = sprites.Length > 0 ? MakePrefab() : null;
            if (!prefab)
            {
                Debug.LogError("[Hạt lửa] Thiếu ảnh hạt hoặc prefab Items/HatLua.");
                return;
            }
            var root = PrefabUtility.LoadPrefabContents(DetailPath);
            try
            {
                var viewer = root.GetComponentInChildren<HeroViewer>(true);
                var dlg = root.GetComponentInChildren<HeroDetailDialog>(true);
                if (!viewer || !dlg)
                {
                    Debug.LogError("[Hạt lửa] ChiTietTuong thiếu HeroViewer hoặc HeroDetailDialog.");
                    return;
                }
                var vso = new SerializedObject(viewer);
                var box = vso.FindProperty("box").objectReferenceValue as RectTransform;
                if (!box)
                {
                    Debug.LogError("[Hạt lửa] HeroViewer chưa có box.");
                    return;
                }
                var floor = Holder(box, "HatDat");
                var back = Holder(box, "HatSau");
                var front = Holder(box, "HatTruoc");
                floor.SetSiblingIndex(0);
                back.SetSiblingIndex(1);
                front.SetAsLastSibling();
                var van = ImportVan();
                Mang(floor, van);
                Mang(back, van);
                Mang(front, van);
                vso.FindProperty("hatPrefab").objectReferenceValue = prefab;
                vso.FindProperty("hatFloor").objectReferenceValue = floor;
                vso.FindProperty("hatBack").objectReferenceValue = back;
                vso.FindProperty("hatFront").objectReferenceValue = front;
                var arr = vso.FindProperty("hatSprites");
                arr.arraySize = sprites.Length;
                for (int i = 0; i < sprites.Length; i++) arr.GetArrayElementAtIndex(i).objectReferenceValue = sprites[i];
                vso.ApplyModifiedPropertiesWithoutUndo();

                var dso = new SerializedObject(dlg);
                var clips = dso.FindProperty("p.clips");
                var skillBtn = clips.arraySize > 2 ? clips.GetArrayElementAtIndex(2).objectReferenceValue as UI.SketchButton : null;
                if (!skillBtn)
                {
                    Debug.LogError("[Hạt lửa] Không thấy nút Chiêu (p.clips[2]).");
                    return;
                }
                if (clips.arraySize < 5)
                {
                    var go = Object.Instantiate(skillBtn.gameObject, skillBtn.transform.parent);
                    go.name = "nut_Mana";
                    go.transform.SetSiblingIndex(skillBtn.transform.GetSiblingIndex() + 1);
                    var label = go.GetComponentInChildren<TMPro.TextMeshProUGUI>(true);
                    if (label) label.text = "Mana";
                    clips.arraySize = 5;
                    clips.GetArrayElementAtIndex(4).objectReferenceValue = go.GetComponent<UI.SketchButton>();
                }
                dso.ApplyModifiedPropertiesWithoutUndo();
                // vừa hàng: thu bề rộng nút nếu năm nút tràn hàng
                var row = (RectTransform)skillBtn.transform.parent;
                var hl = row.GetComponent<HorizontalLayoutGroup>();
                int n = row.childCount;
                if (hl && n > 0)
                {
                    float per = (row.rect.width - hl.padding.horizontal - hl.spacing * (n - 1)) / n;
                    foreach (Transform c in row)
                    {
                        var le = c.GetComponent<LayoutElement>();
                        if (!le || per <= 0) continue;
                        if (le.preferredWidth > per) le.preferredWidth = per;
                        if (le.minWidth > per) le.minWidth = per;
                    }
                }
                PrefabUtility.SaveAsPrefabAsset(root, DetailPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            Debug.Log($"[Hạt lửa] Hộp chi tiết {DetailPath}: lớp hạt trong ô xem, nút Mana.");
        }

        // ô vân chì lặp của mảng nước liền (ArtGen/Spine/xuat_hat.py): ảnh thường, lặp, không mipmap
        static Texture2D ImportVan()
        {
            const string path = ArtDir + "/van_chi.png";
            var imp = AssetImporter.GetAtPath(path) as TextureImporter;
            if (!imp)
            {
                Debug.LogWarning($"[Hạt lửa] Thiếu {path}: mảng nước liền sẽ tô màu trơn.");
                return null;
            }
            if (imp.textureType != TextureImporterType.Default || imp.wrapMode != TextureWrapMode.Repeat || imp.mipmapEnabled
                || imp.npotScale != TextureImporterNPOTScale.None || imp.maxTextureSize > 128)
            {
                imp.textureType = TextureImporterType.Default;
                imp.wrapMode = TextureWrapMode.Repeat;
                imp.mipmapEnabled = false;
                imp.npotScale = TextureImporterNPOTScale.None;
                imp.alphaSource = TextureImporterAlphaSource.None;
                imp.maxTextureSize = 128;
                imp.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Texture2D>(path);
        }

        // mảng nước liền (HatMang): con ĐẦU của lớp hạt (dưới mọi hạt cùng lớp), gốc ở góc trên trái của lớp như các Image hạt
        static void Mang(RectTransform layer, Texture2D van)
        {
            var t = layer.Find("Mang") as RectTransform;
            if (!t)
            {
                var go = new GameObject("Mang", typeof(RectTransform), typeof(CanvasRenderer), typeof(HatMang));
                t = (RectTransform)go.transform;
                t.SetParent(layer, false);
            }
            t.anchorMin = t.anchorMax = new Vector2(0, 1);
            t.pivot = new Vector2(0.5f, 0.5f);
            t.anchoredPosition = Vector2.zero;
            t.sizeDelta = new Vector2(8000, 8000);
            t.localScale = Vector3.one;
            t.localRotation = Quaternion.identity;
            t.SetSiblingIndex(0);
            var m = t.GetComponent<HatMang>();
            m.raycastTarget = false;
            var mso = new SerializedObject(m);
            mso.FindProperty("van").objectReferenceValue = van;
            mso.ApplyModifiedPropertiesWithoutUndo();
        }

        static RectTransform Holder(RectTransform box, string name)
        {
            var t = box.Find(name) as RectTransform;
            if (!t)
            {
                var go = new GameObject(name, typeof(RectTransform));
                t = (RectTransform)go.transform;
                t.SetParent(box, false);
            }
            t.anchorMin = t.anchorMax = t.pivot = new Vector2(0.5f, 0);
            t.anchoredPosition = Vector2.zero;
            t.sizeDelta = Vector2.zero;
            t.localScale = Vector3.one;
            t.localRotation = Quaternion.identity;
            return t;
        }

        static RectTransform Layer(Transform parent, string name, RectTransform like)
        {
            var t = parent.Find(name) as RectTransform;
            if (!t)
            {
                var go = new GameObject(name, typeof(RectTransform));
                t = (RectTransform)go.transform;
                t.SetParent(parent, false);
            }
            t.anchorMin = like.anchorMin;
            t.anchorMax = like.anchorMax;
            t.pivot = like.pivot;
            t.anchoredPosition = like.anchoredPosition;
            t.sizeDelta = like.sizeDelta;
            t.localScale = Vector3.one;
            t.localRotation = Quaternion.identity;
            if (!t.GetComponent<Canvas>()) t.gameObject.AddComponent<Canvas>();
            return t;
        }

        static Sprite[] ImportSprites()
        {
            if (!Directory.Exists(ArtDir)) return new Sprite[0];
            var paths = Directory.GetFiles(ArtDir, "hat_*.png").Select(p => p.Replace('\\', '/')).OrderBy(p => p).ToArray();
            foreach (var path in paths)
            {
                var imp = AssetImporter.GetAtPath(path) as TextureImporter;
                if (!imp) continue;
                bool dirty = imp.textureType != TextureImporterType.Sprite || imp.mipmapEnabled || imp.spriteImportMode != SpriteImportMode.Single
                             || !imp.alphaIsTransparency || imp.maxTextureSize > 512;
                if (!dirty) continue;
                imp.textureType = TextureImporterType.Sprite;
                imp.spriteImportMode = SpriteImportMode.Single;
                imp.mipmapEnabled = false;
                imp.alphaIsTransparency = true;
                imp.maxTextureSize = 512;
                imp.SaveAndReimport();
            }
            return paths.Select(AssetDatabase.LoadAssetAtPath<Sprite>).Where(s => s).ToArray();
        }

        static Image MakePrefab()
        {
            if (!AssetDatabase.LoadAssetAtPath<GameObject>(HatPrefab) && !AssetDatabase.CopyAsset(SrcPrefab, HatPrefab))
            {
                Debug.LogError($"[Hạt lửa] Không chép được {SrcPrefab} thành {HatPrefab}.");
                return null;
            }
            var go = PrefabUtility.LoadPrefabContents(HatPrefab);
            try
            {
                go.name = "HatLua";
                var img = go.GetComponent<Image>();
                if (!img)
                {
                    Debug.LogError($"[Hạt lửa] {HatPrefab} không có Image.");
                    return null;
                }
                img.sprite = null;
                img.color = Color.white;
                img.type = Image.Type.Simple;
                img.preserveAspect = false;
                img.raycastTarget = false;
                var rt = (RectTransform)go.transform;
                rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                rt.pivot = new Vector2(0.5f, 0.5f);
                PrefabUtility.SaveAsPrefabAsset(go, HatPrefab);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(go);
            }
            return AssetDatabase.LoadAssetAtPath<Image>(HatPrefab);
        }
    }
}
