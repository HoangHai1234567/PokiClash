// Thẻ bài (GD_Claude/36, 2026-11-27): thêm ô tranh 16:10 (o_tranh) vào prefab Kit/The và Kit/TheMini, ngay sau ô tròn o_hinh, dời mô
// tả xuống cho vừa chữ (thẻ Huyền thoại 4-5 dòng), nối UiCard.p.tranh. Chạy lại được: đã có o_tranh thì chỉ đặt lại cỡ, chỗ.
// Tranh: Assets/03 Art/Cards/tranh_<mã thẻ>.png (ArtGen/Cards/chep_vao_game.py), vào danh mục bằng "PokiClash/Dựng lại danh mục ảnh".
// Chụp thử không cần Play: "PokiClash/Thử/Thẻ: chụp mặt thẻ có tranh" dựng tạm vài thẻ trên canvas ẩn → Temp/PokiShots/the_tranh.png.
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class CardArtMenu
    {
        const string ThePath = "Assets/04 Prefabs/Kit/The.prefab";
        const string MiniPath = "Assets/04 Prefabs/Kit/TheMini.prefab";
        // thẻ thường 320 x 464: ô tranh 272 x 170 từ 92 px dưới đỉnh (chỗ ô tròn cũ), mô tả 266..410 px dưới đỉnh
        static readonly Vector2 ArtSize = new Vector2(272, 170);
        const float DescTop = 266, DescBottom = 410;

        [MenuItem("PokiClash/Thẻ: thêm ô tranh", priority = 40)]
        public static void Run()
        {
            Patch(ThePath, 1f);
            Patch(MiniPath, 0.625f); // mini 200 x 292
            AssetDatabase.SaveAssets();
        }

        static void Patch(string path, float k)
        {
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                var card = root.GetComponent<UiCard>();
                var oHinh = root.transform.Find("o_hinh") as RectTransform;
                var moTa = root.transform.Find("mo_ta") as RectTransform;
                if (!card || !oHinh || !moTa)
                {
                    Debug.LogError($"[Thẻ] {path}: thiếu UiCard / o_hinh / mo_ta, không sửa.");
                    return;
                }
                var t = root.transform.Find("o_tranh") as RectTransform;
                if (!t)
                {
                    var go = new GameObject("o_tranh", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                    go.layer = oHinh.gameObject.layer;
                    t = (RectTransform)go.transform;
                    t.SetParent(root.transform, false);
                }
                t.SetSiblingIndex(oHinh.GetSiblingIndex() + 1);
                t.anchorMin = t.anchorMax = new Vector2(0.5f, 1);
                t.pivot = new Vector2(0.5f, 1);
                t.anchoredPosition = oHinh.anchoredPosition;
                t.sizeDelta = ArtSize * k;
                t.localScale = Vector3.one;
                var img = t.GetComponent<Image>();
                img.raycastTarget = false;
                img.preserveAspect = false;
                img.type = Image.Type.Simple;
                t.gameObject.SetActive(false); // UiCard.Bind bật khi thẻ có tranh

                float h = ((RectTransform)root.transform).rect.height;
                float top = DescTop * k, bottom = DescBottom * k;
                moTa.sizeDelta = new Vector2(moTa.sizeDelta.x, bottom - top - h);
                moTa.anchoredPosition = new Vector2(moTa.anchoredPosition.x, h / 2 - (top + bottom) / 2);

                var so = new SerializedObject(card);
                so.FindProperty("p.tranh").objectReferenceValue = img;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(root, path);
                Debug.Log($"[Thẻ] {path}: ô tranh {t.sizeDelta.x:0.#} x {t.sizeDelta.y:0.#}, mô tả {top:0.#}..{bottom:0.#} px dưới đỉnh.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // ---------- chụp thử (không Play) ----------

        [MenuItem("PokiClash/Thử/Thẻ: chụp mặt thẻ có tranh", priority = 140)]
        public static void Shot()
        {
            // bảng sprite giấy, material, danh mục ảnh: lúc chạy App gán; ở Editor gán tạm từ asset (như ShopMenu)
            if (!BakedArt.Current)
            {
                var g = AssetDatabase.FindAssets("t:BakedArt").FirstOrDefault();
                if (g != null) BakedArt.Current = AssetDatabase.LoadAssetAtPath<BakedArt>(AssetDatabase.GUIDToAssetPath(g));
            }
            if (!Theme.Kit)
            {
                var g = AssetDatabase.FindAssets("t:UiAssets").FirstOrDefault();
                if (g != null) Theme.Init(AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(g)));
            }
            var lib = AssetDatabase.LoadAssetAtPath<ArtLibrary>("Assets/02 Data/ArtLibrary.asset");
            var oldLib = ArtLibrary.Current;
            ArtLibrary.Current = lib;
            lib.Invalidate();
            var db = AssetDatabase.LoadAssetAtPath<CardDb>("Assets/02 Data/CardDb.asset");
            // chữ mô tả thẻ (CardText) đọc GameData.Current: lúc chạy App dựng; ở Editor dựng tạm như test AssetDuLieu_KhopJson
            if (GameData.Current == null)
                GameDb.Build(AssetDatabase.LoadAssetAtPath<HeroDb>("Assets/02 Data/HeroDb.asset"), db,
                    AssetDatabase.LoadAssetAtPath<ZoneDb>("Assets/02 Data/ZoneDb.asset"),
                    AssetDatabase.LoadAssetAtPath<BalanceConfigAsset>("Assets/02 Data/BalanceConfig.asset"));
            var the = AssetDatabase.LoadAssetAtPath<GameObject>(ThePath);
            var mini = AssetDatabase.LoadAssetAtPath<GameObject>(MiniPath);
            CardDef Pool(string id) => db.pool.First(c => c.id == id);
            var innate = db.innate.First(c => c.HasCost);

            const int W = 1120, H = 1660;
            var rt = new RenderTexture(W, H, 24);
            var root = new GameObject("_chup_the") { hideFlags = HideFlags.HideAndDontSave };
            try
            {
                var cam = new GameObject("cam").AddComponent<Camera>();
                cam.transform.SetParent(root.transform);
                cam.orthographic = true;
                cam.clearFlags = CameraClearFlags.SolidColor;
                cam.backgroundColor = Theme.Hex("#f3ebd6");
                cam.targetTexture = rt;
                cam.cullingMask = ~0;
                var canvas = new GameObject("canvas", typeof(RectTransform)).AddComponent<Canvas>();
                canvas.transform.SetParent(root.transform);
                canvas.renderMode = RenderMode.ScreenSpaceCamera;
                canvas.worldCamera = cam;
                canvas.planeDistance = 10;
                Transform Put(GameObject prefab, CardDef c, int lv, float x, float y, string locked = null)
                {
                    var go = Object.Instantiate(prefab, canvas.transform, false);
                    go.hideFlags = HideFlags.HideAndDontSave;
                    var rtf = (RectTransform)go.transform;
                    rtf.anchorMin = rtf.anchorMax = new Vector2(0, 1);
                    rtf.anchoredPosition = new Vector2(x, -y);
                    var lb = ArtLibrary.Current ? ArtLibrary.Current.Icon(c.icon) : null;
                    go.GetComponent<UiCard>().Bind(c, lv, lb, locked);
                    return go.transform;
                }
                // hàng 1: thẻ chung có tranh; hàng 2: Huyền thoại chữ dài, thẻ riêng (ô tròn), thẻ khoá; hàng 3: thẻ mini
                Put(the, Pool("mai_vuot"), 1, 200, 262);
                Put(the, Pool("nem_da"), 1, 560, 262);
                Put(the, Pool("ket_lieu"), 3, 920, 262);
                Put(the, Pool("nghich_thien"), 1, 200, 762);
                Put(the, innate, 2, 560, 762);
                Put(the, Pool("guong_doi"), 1, 920, 762, "Mở ở cấp 12");
                Put(mini, Pool("hit_tho"), 1, 160, 1330);
                Put(mini, Pool("bao_cat"), 1, 400, 1330);
                Put(mini, Pool("thien_ho"), 1, 640, 1330);
                Put(mini, innate, 1, 880, 1330);
                Canvas.ForceUpdateCanvases();
                cam.Render();
                var prev = RenderTexture.active;
                RenderTexture.active = rt;
                var tex = new Texture2D(W, H, TextureFormat.RGB24, false);
                tex.ReadPixels(new Rect(0, 0, W, H), 0, 0);
                tex.Apply();
                RenderTexture.active = prev;
                var dir = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots"));
                Directory.CreateDirectory(dir);
                var file = Path.Combine(dir, "the_tranh.png");
                File.WriteAllBytes(file, tex.EncodeToPNG());
                Object.DestroyImmediate(tex);
                Debug.Log("[Thẻ] Đã chụp " + file);
            }
            finally
            {
                Object.DestroyImmediate(root);
                rt.Release();
                Object.DestroyImmediate(rt);
                ArtLibrary.Current = oldLib;
            }
        }
    }
}
