// Đợt cải thiện giao diện 2026-11-06 (người dùng: "cải thiện UI cùng các màn trong game, các đảo vẫn giữ nguyên"), cùng nét với màn
// mở game "sa bàn". Menu "PokiClash/Prefab/Giao diện: bàn gỗ, trang sổ, tiêu đề băng keo" (chạy lại được, không nhân đôi):
// - màn con Tướng, Sổ thẻ, Sổ tay, Đền Huy Hiệu, Hang, Trang trại: nền là mặt bàn gỗ (ảnh boot_ban_go của màn mở game), trên đó
//   một trang giấy kẻ ô có viền mực và lề đỏ, nằm ngay dưới thanh trên (An toan/Khung/trang, con đầu tiên, sau nội dung);
// - Máy bi: nền mặt bàn gỗ (máy đứng trên bàn), không có trang giấy;
// - nền cũ trong Canvas/Nen chỉ bị tắt (không xoá) để đổi lại được;
// - thanh trên (App.prefab): ô tên màn (Quay lai/ten) thành mảnh băng keo giấy hơi nghiêng.
// Sảnh, đảo và trận không đổi.
using System.IO;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class UiRefreshMenu
    {
        const string ScreensDir = "Assets/04 Prefabs/Screens/";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const string WoodPath = "Assets/03 Art/Boot/boot_ban_go.png";
        public const string TapePath = "Assets/03 Art/Kit/ui_bang_keo_ten.png";
        static readonly string[] PageScreens = { "Heroes", "Cards", "Notebook", "Badges", "Cave" }; // Trang trại là cảnh thật (FarmSceneMenu), không có trang giấy
        static readonly string[] DeskScreens = { "Machine" };

        // trang giấy: cách mép khung 12, đỉnh ngay dưới thanh trên, đáy tràn xuống quá mép màn
        const float PageSide = 12, PageTop = 132, PageBleed = 120;
        static readonly Color Margin = new Color(0.91f, 0.33f, 0.25f, 0.42f); // lề đỏ của vở
        static readonly Color TapeColor = new Color(1f, 0.93f, 0.67f, 0.96f);

        [MenuItem("PokiClash/Prefab/Giao diện: bàn gỗ, trang sổ, tiêu đề băng keo", priority = 69)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            Theme.Init(assets);
            var wood = AssetDatabase.LoadAssetAtPath<Sprite>(WoodPath);
            var tape = TapeSprite();
            if (!wood || !tape)
            {
                Debug.LogError("[Giao diện] Thiếu ảnh mặt bàn gỗ hoặc băng keo tiêu đề.");
                return;
            }
            foreach (var s in PageScreens) PatchScreen(s, wood, true);
            foreach (var s in DeskScreens) PatchScreen(s, wood, false);
            PatchTopBar(tape);
            AssetDatabase.SaveAssets();
            Debug.Log($"[Giao diện] Đã đổi nền {PageScreens.Length + DeskScreens.Length} màn con và ô tên trên thanh trên.");
        }

        // băng keo tiêu đề: 9-slice ngang (hai đầu xé giữ nguyên, phần giữa giãn)
        static Sprite TapeSprite()
        {
            var ti = AssetImporter.GetAtPath(TapePath) as TextureImporter;
            if (!ti) return null;
            var border = new Vector4(44, 0, 44, 0);
            if (ti.spriteBorder != border)
            {
                ti.spriteBorder = border;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(TapePath);
        }

        static void PatchScreen(string screen, Sprite wood, bool page)
        {
            var path = ScreensDir + screen + ".prefab";
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                var bg = root.transform.Find("Canvas/Nen") as RectTransform;
                var frame = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!bg || !frame)
                {
                    Debug.LogError($"[Giao diện] {screen}: không thấy Canvas/Nen hoặc Canvas/An toan/Khung");
                    return;
                }
                // nền giấy cũ (để chép cách lát ô kẻ), rồi tắt mọi nền cũ
                Image oldGrid = null;
                foreach (Transform c in bg)
                {
                    if (c.name == "ban_go") continue;
                    if (c.name == "giay") oldGrid = c.GetComponent<Image>();
                    c.gameObject.SetActive(false);
                }
                var woodImg = Child(bg, "ban_go");
                woodImg.transform.SetAsFirstSibling();
                ((RectTransform)woodImg.transform).Stretch();
                Theme.SetSprite(woodImg, wood);
                woodImg.type = Image.Type.Simple;
                woodImg.color = Color.white;
                woodImg.raycastTarget = false;
                woodImg.gameObject.SetActive(true);

                var old = frame.Find("trang");
                if (!page)
                {
                    if (old) Object.DestroyImmediate(old.gameObject);
                }
                else
                {
                    var sheet = Child(frame, "trang");
                    var rt = (RectTransform)sheet.transform;
                    rt.SetAsFirstSibling();
                    rt.Stretch(PageSide, PageTop, PageSide, -PageBleed);
                    Theme.SetSprite(sheet, Sketch.PanelFlat);
                    sheet.type = Image.Type.Sliced;
                    sheet.color = Theme.Paper;
                    sheet.raycastTarget = false;
                    // ô kẻ xanh nhạt lát kín lòng trang
                    var grid = Child(rt, "o_ke");
                    ((RectTransform)grid.transform).Stretch(6, 6, 6, 6);
                    var gridSprite = oldGrid && oldGrid.sprite ? oldGrid.sprite : Sketch.PaperGrid;
                    Theme.SetSprite(grid, gridSprite);
                    grid.type = Image.Type.Tiled;
                    grid.pixelsPerUnitMultiplier = oldGrid ? oldGrid.pixelsPerUnitMultiplier : 1;
                    grid.color = oldGrid ? oldGrid.color : Color.white;
                    grid.raycastTarget = false;
                    // lề đỏ hai nét của vở
                    for (int i = 0; i < 2; i++)
                    {
                        var line = Child(rt, "le_" + i);
                        var lr = (RectTransform)line.transform;
                        lr.anchorMin = new Vector2(0, 0);
                        lr.anchorMax = new Vector2(0, 1);
                        lr.pivot = new Vector2(0.5f, 0.5f);
                        lr.sizeDelta = new Vector2(3, -12);
                        lr.anchoredPosition = new Vector2(84 + i * 9, 0);
                        Theme.SetSprite(line, Sketch.White);
                        line.color = Margin;
                        line.raycastTarget = false;
                    }
                }
                PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static void PatchTopBar(Sprite tape)
        {
            var root = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                var ten = root.transform.Find("Canvas thanh tren/An toan/Khung/Thanh tren/Quay lai/ten") as RectTransform;
                if (!ten)
                {
                    Debug.LogError("[Giao diện] Không thấy ô tên trên thanh trên (Quay lai/ten)");
                    return;
                }
                var img = ten.GetComponent<Image>();
                Theme.SetSprite(img, tape);
                img.type = Image.Type.Sliced;
                img.color = TapeColor;
                ten.localEulerAngles = new Vector3(0, 0, 1.5f);
                PrefabUtility.SaveAsPrefabAsset(root, AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // con có tên name (có Image), chưa có thì tạo
        static Image Child(Transform parent, string name)
        {
            var t = parent.Find(name);
            if (!t)
            {
                var go = new GameObject(name, typeof(RectTransform), typeof(Image));
                go.transform.SetParent(parent, false);
                t = go.transform;
            }
            var img = t.GetComponent<Image>();
            if (!img) img = t.gameObject.AddComponent<Image>();
            return img;
        }

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));
    }
}
