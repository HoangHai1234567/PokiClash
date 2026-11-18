// Màn Nhà (GD_Claude/21_Nha_Home.md, mốc H2). Menu "PokiClash/Prefab/Nhà: dựng màn" (chạy lại được, dựng lại các lớp):
// - nhập ảnh Assets/03 Art/Home (đưa vào bằng ArtGen/Home/import_home.py, có home_art.json: điểm neo, bề ngang chân thoi), tạo ảnh ô lát
//   home_tile.png (chân thoi trắng, viền mực);
// - prefab mục Items/NhaVat (HomeObject), Items/NhaOLat, Items/NhaMay;
// - Screens/Home: lần đầu chép từ Screens/Farm (giữ canvas, thanh trên, khung), thay FarmScene bằng HomeScene, gỡ cảnh trang trại; dựng
//   the_gioi (nền + chạm, ô lát, vật, sáng tối dùng chung DayNight của các đảo, đèn, mây), HubPan kéo; giao diện: dòng tài nguyên, gợi ý,
//   bảng chọn, khay, hàng nút (Xây, Lát ô, Tự xếp, Thu hết, Ra đảo);
// - scene Assets/00 Scenes/Home.unity (bản sao prefab màn hình) và Build Settings.
// Chạy không cần bấm (Unity dùng chung nhiều session): Temp/home_build.flag → biên dịch xong, không Play thì dựng một lần rồi xoá cờ.
// Temp/home_tour.flag → vào Play, mở Nhà, chụp ảnh Temp/PokiShots/home_*.png (thường, xây, lát), rồi Stop.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HomeSceneMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/Home.prefab";
        const string FarmScreenPath = "Assets/04 Prefabs/Screens/Farm.prefab";
        const string ObjPath = "Assets/04 Prefabs/Items/NhaVat.prefab";
        const string TilePath = "Assets/04 Prefabs/Items/NhaOLat.prefab";
        const string CloudPath = "Assets/04 Prefabs/Items/NhaMay.prefab";
        const string TreePath = "Assets/04 Prefabs/Items/NhaCay.prefab";
        const string WaterMatPath = "Assets/03 Art/Home/home_water.mat";
        const string DistPath = "Assets/03 Art/Baked/Home/home_dist.png";
        const string GlowItemPath = "Assets/04 Prefabs/Items/HinhDong.prefab";
        const string ArtDir = "Assets/03 Art/Home/";
        const string ScenePath = "Assets/00 Scenes/Home.unity";
        const float CW = 96;

        [MenuItem("PokiClash/Prefab/Nhà: dựng màn", priority = 64)]
        public static void Build()
        {
            // số liệu Nhà (khối "home" của balance.json) vào BalanceConfig.asset: lúc chạy game đọc asset này, không đọc JSON
            if (!DataImporter.Run(false)) Debug.LogError("[Nhà] Nhập dữ liệu lỗi (xem lỗi [Dữ liệu] ở trên): Nhà sẽ thiếu số liệu.");
            var assets = Load<UiAssets>();
            Theme.Init(assets);
            var metaPath = ArtDir + "home_art.json";
            if (!File.Exists(metaPath))
            {
                Debug.LogError("[Nhà] Thiếu " + metaPath + " (chạy ArtGen/Home/import_home.py).");
                return;
            }
            var meta = J.Obj(MiniJson.Parse(File.ReadAllText(metaPath)));
            var baseMeta = J.Obj(meta, "home_base");
            var baseSprite = ImportSprite(ArtDir + "home_base.png", 2048);
            if (!baseSprite || baseMeta == null)
            {
                Debug.LogError("[Nhà] Thiếu home_base.png hoặc khối home_base trong home_art.json.");
                return;
            }
            var arts = new List<HomeScene.ArtMeta>();
            foreach (var kv in meta)
            {
                if (kv.Key == "home_base") continue;
                var m = J.Obj(kv.Value);
                var sp = ImportSprite(ArtDir + kv.Key + ".png", 1024);
                if (!sp) continue;
                var piv = J.Arr(m, "pivot");
                arts.Add(new HomeScene.ArtMeta
                {
                    id = kv.Key, sprite = sp, pivot = piv.Count >= 2 ? new Vector2((float)(double)piv[0], (float)(double)piv[1]) : new Vector2(0.5f, 0),
                    foot = (float)J.Num(m, "foot", sp.rect.width), cells = J.Int(m, "cells"),
                });
            }
            var tileSprite = TileSprite();
            var trees = TreeSprites();
            var tileArt = TileArt();
            var water = WaterMat();
            var glowSprite = AssetDatabase.LoadAssetAtPath<Sprite>("Assets/03 Art/Islands/Anim/anim_glow.png");

            var obj = BuildObj();
            var tile = BuildImageItem(TilePath, "NhaOLat", tileSprite);
            var cloud = BuildImageItem(CloudPath, "NhaMay", null);
            var treeItem = BuildImageItem(TreePath, "NhaCay", null);
            var glowItem = AssetDatabase.LoadAssetAtPath<GameObject>(GlowItemPath)?.GetComponent<Image>() ?? cloud;

            // bản đồ: ảnh nền phóng sao cho thoi đồng cỏ rộng 48 ô x 96 px
            float s = (float)(J.Int(baseMeta, "grid", 48) * CW / J.Num(baseMeta, "diamondW", 1460));
            var worldSize = new Vector2((float)J.Num(baseMeta, "w") * s, (float)J.Num(baseMeta, "h") * s);
            var topArr = J.Arr(baseMeta, "top");
            var gridTop = new Vector2((float)(double)topArr[0] * s, (float)(double)topArr[1] * s);

            if (!BuildScreen(assets, baseSprite, worldSize, gridTop, obj, tile, glowItem, cloud, arts.ToArray(), glowSprite, treeItem, trees, tileArt, water)) return;
            AssetDatabase.SaveAssets();
            MakeScene();
            Debug.Log($"[Nhà] Đã dựng {ScreenPath} (bản đồ {worldSize.x:0} x {worldSize.y:0} px, {arts.Count} ảnh), {ObjPath}, {TilePath}, {CloudPath}, scene {ScenePath}.");
        }

        // ---------- ảnh ----------

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));

        static Sprite ImportSprite(string path, int max)
        {
            if (!File.Exists(path)) return null;
            AssetDatabase.ImportAsset(path);
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (ti && (ti.textureType != TextureImporterType.Sprite || ti.maxTextureSize != max || ti.mipmapEnabled))
            {
                ti.textureType = TextureImporterType.Sprite;
                ti.spriteImportMode = SpriteImportMode.Single;
                ti.mipmapEnabled = false;
                ti.alphaIsTransparency = true;
                ti.maxTextureSize = max;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        // chân thoi trắng 2:1 (tô màu theo loại ô lúc chạy), viền mực mờ
        static Sprite TileSprite()
        {
            var path = ArtDir + "home_tile.png";
            if (!File.Exists(path))
            {
                const int W = 192, H = 96;
                var tex = new Texture2D(W, H, TextureFormat.RGBA32, false);
                var px = new Color32[W * H];
                for (int y = 0; y < H; y++)
                for (int x = 0; x < W; x++)
                {
                    float u = Mathf.Abs(x + 0.5f - W / 2f) / (W / 2f), v = Mathf.Abs(y + 0.5f - H / 2f) / (H / 2f);
                    float dd = u + v; // 1 = mép thoi
                    byte a = (byte)(dd <= 1 ? 255 : 0);
                    byte c = (byte)(dd > 0.94f && dd <= 1 ? 150 : 255); // viền mực nhạt
                    px[y * W + x] = new Color32(c, c, c, a);
                }
                tex.SetPixels32(px);
                File.WriteAllBytes(path, tex.EncodeToPNG());
                Object.DestroyImmediate(tex);
            }
            return ImportSprite(path, 256);
        }

        // cây rời: atlas home_trees.png (ArtGen/Home/trees/pack_trees.py) cắt thành nhiều sprite theo home_trees.json
        static HomeScene.TreeArt[] TreeSprites()
        {
            const string png = "Assets/03 Art/Baked/Home/home_trees.png", js = "Assets/03 Art/Baked/Home/home_trees.json"; // Baked: ArtImporter không ép về một sprite
            if (!File.Exists(png) || !File.Exists(js)) return new HomeScene.TreeArt[0];
            var meta = J.Obj(MiniJson.Parse(File.ReadAllText(js)));
            int H = J.Int(meta, "h");
            var items = J.Arr(meta, "items").Select(J.Obj).ToList();
            AssetDatabase.ImportAsset(png);
            var ti = (TextureImporter)AssetImporter.GetAtPath(png);
            ti.textureType = TextureImporterType.Sprite;
            ti.spriteImportMode = SpriteImportMode.Multiple;
            ti.mipmapEnabled = false;
            ti.alphaIsTransparency = true;
            ti.maxTextureSize = 2048;
#pragma warning disable 618
            ti.spritesheet = items.Select(m =>
            {
                var piv = J.Arr(m, "pivot");
                return new SpriteMetaData
                {
                    name = J.Str(m, "name"), alignment = (int)SpriteAlignment.Custom,
                    rect = new Rect(J.Int(m, "x"), H - J.Int(m, "y") - J.Int(m, "h"), J.Int(m, "w"), J.Int(m, "h")),
                    pivot = new Vector2((float)(double)piv[0], (float)(double)piv[1]),
                };
            }).ToArray();
#pragma warning restore 618
            ti.SaveAndReimport();
            var sprites = AssetDatabase.LoadAllAssetsAtPath(png).OfType<Sprite>().ToDictionary(sp => sp.name);
            return items.Where(m => sprites.ContainsKey(J.Str(m, "name"))).Select(m =>
            {
                var piv = J.Arr(m, "pivot");
                return new HomeScene.TreeArt
                {
                    id = J.Str(m, "name"), group = J.Str(m, "group"), sprite = sprites[J.Str(m, "name")],
                    pivot = new Vector2((float)(double)piv[0], (float)(double)piv[1]),
                };
            }).ToArray();
        }

        // ô lát: Assets/03 Art/Home/tiles/*.png (ArtGen/Home/tiles/make_tiles.py)
        static HomeScene.NamedSprite[] TileArt()
        {
            var dir = ArtDir + "tiles/";
            if (!Directory.Exists(dir)) return new HomeScene.NamedSprite[0];
            return Directory.GetFiles(dir, "*.png").Select(f => f.Replace('\\', '/')).Select(f => new HomeScene.NamedSprite
            {
                id = Path.GetFileNameWithoutExtension(f), sprite = ImportSprite(f, 256),
            }).Where(t => t.sprite).ToArray();
        }

        // sóng vỗ bờ như đảo Thủy: shader PokiClash/UIInkWater vẽ ảnh nền kèm ảnh khoảng cách tới bờ (ArtGen/Home/make_home_dist.py)
        static Material WaterMat()
        {
            var shader = Shader.Find("PokiClash/UIInkWater");
            if (!shader || !File.Exists(DistPath)) return null;
            AssetDatabase.ImportAsset(DistPath);
            var ti = (TextureImporter)AssetImporter.GetAtPath(DistPath);
            if (ti.sRGBTexture || ti.mipmapEnabled || ti.textureCompression != TextureImporterCompression.Uncompressed || ti.textureType != TextureImporterType.Default)
            {
                ti.textureType = TextureImporterType.Default;
                ti.sRGBTexture = false;
                ti.mipmapEnabled = false;
                ti.alphaSource = TextureImporterAlphaSource.None;
                ti.wrapMode = TextureWrapMode.Clamp;
                ti.filterMode = FilterMode.Bilinear;
                ti.textureCompression = TextureImporterCompression.Uncompressed;
                ti.maxTextureSize = 2048;
                ti.SaveAndReimport();
            }
            var mat = AssetDatabase.LoadAssetAtPath<Material>(WaterMatPath);
            if (!mat)
            {
                mat = new Material(shader);
                AssetDatabase.CreateAsset(mat, WaterMatPath);
            }
            mat.shader = shader;
            mat.SetTexture("_DistTex", AssetDatabase.LoadAssetAtPath<Texture2D>(DistPath));
            EditorUtility.SetDirty(mat);
            return mat;
        }

        // ---------- dựng nút ----------

        static RectTransform Node(Transform parent, string name, params System.Type[] types)
        {
            var go = new GameObject(name, new[] { typeof(RectTransform) }.Concat(types).ToArray());
            go.layer = LayerMask.NameToLayer("UI");
            var rt = (RectTransform)go.transform;
            if (parent) rt.SetParent(parent, false);
            return rt;
        }

        static RectTransform Fill(RectTransform rt)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            return rt;
        }

        static RectTransform At(RectTransform rt, Vector2 anchor, Vector2 pos, Vector2 size, Vector2 pivot)
        {
            rt.anchorMin = rt.anchorMax = anchor;
            rt.pivot = pivot;
            rt.anchoredPosition = pos;
            rt.sizeDelta = size;
            return rt;
        }

        static Image Img(Transform parent, string name, Sprite s, Color c, bool raycast = false, bool sliced = false)
        {
            var img = Node(parent, name, typeof(CanvasRenderer), typeof(Image)).GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = c;
            img.type = sliced ? Image.Type.Sliced : Image.Type.Simple;
            img.raycastTarget = raycast;
            return img;
        }

        static TextMeshProUGUI Text(Transform parent, string name, float size, Color color, TextAlignmentOptions align = TextAlignmentOptions.Center)
        {
            var t = Node(parent, name, typeof(CanvasRenderer), typeof(TextMeshProUGUI)).GetComponent<TextMeshProUGUI>();
            t.font = Theme.Bold;
            t.fontSize = size;
            t.color = color;
            t.alignment = align;
            t.textWrappingMode = TextWrappingModes.Normal;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = "";
            return t;
        }

        static T Save<T>(GameObject root, string path) where T : Component
        {
            try
            {
                return PrefabUtility.SaveAsPrefabAsset(root, path).GetComponent<T>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static SketchButton Button(UiAssets assets, Transform parent, string name, string label, BtnColor color, Vector2 size)
        {
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(assets.prefabs.buttonSmall.gameObject, parent)).GetComponent<SketchButton>();
            b.name = name;
            b.SetRole(color);
            b.SetText(label);
            ((RectTransform)b.transform).sizeDelta = size;
            return b;
        }

        // ---------- prefab mục ----------

        static HomeObject BuildObj()
        {
            var root = Node(null, "NhaVat", typeof(HomeObject));
            At(root, new Vector2(0, 1), Vector2.zero, new Vector2(384, 384), new Vector2(0.5f, 0));
            var img = Img(root, "hinh", null, Color.white);
            Fill(img.rectTransform);
            // nhãn và bong bóng nổi trên đỉnh ảnh
            var label = Text(root, "nhan", 30, Theme.Ink);
            At(label.rectTransform, new Vector2(0.5f, 1), new Vector2(0, 10), new Vector2(320, 44), new Vector2(0.5f, 0));
            var outline = Theme.Outlined(Theme.Bold, 0.25f);
            if (outline) label.fontSharedMaterial = outline;
            label.color = Color.white;
            label.gameObject.SetActive(false);
            var bubble = Img(root, "bong", Sketch.Pill, new Color(1f, 0.98f, 0.92f, 0.97f), false, true);
            At(bubble.rectTransform, new Vector2(0.5f, 1), new Vector2(0, 8), new Vector2(84, 84), new Vector2(0.5f, 0));
            var icon = Img(bubble.transform, "icon", null, Color.white);
            icon.preserveAspect = true;
            Fill(icon.rectTransform).offsetMin = new Vector2(14, 14);
            icon.rectTransform.offsetMax = new Vector2(-14, -14);
            bubble.gameObject.SetActive(false);
            root.GetComponent<HomeObject>().Setup(img, label, bubble, icon);
            return Save<HomeObject>(root.gameObject, ObjPath);
        }

        static Image BuildImageItem(string path, string name, Sprite s)
        {
            var img = Img(null, name, s, Color.white);
            At(img.rectTransform, new Vector2(0, 1), Vector2.zero, new Vector2(192, 96), new Vector2(0.5f, 0.5f));
            return Save<Image>(img.gameObject, path);
        }

        // ---------- màn hình ----------

        static bool BuildScreen(UiAssets assets, Sprite baseSprite, Vector2 worldSize, Vector2 gridTop, HomeObject obj, Image tile, Image glowItem,
            Image cloud, HomeScene.ArtMeta[] arts, Sprite glowSprite, Image treeItem, HomeScene.TreeArt[] trees, HomeScene.NamedSprite[] tileArt,
            Material water)
        {
            if (!File.Exists(ScreenPath))
            {
                if (!AssetDatabase.CopyAsset(FarmScreenPath, ScreenPath))
                {
                    Debug.LogError("[Nhà] Không chép được " + FarmScreenPath + " sang " + ScreenPath);
                    return false;
                }
                AssetDatabase.ImportAsset(ScreenPath);
            }
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                root.name = "Home";
                RectTransform Find(string n) => root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == n);
                // thay FarmScene bằng HomeScene, giữ canvas và vùng nội dung của SceneRoot
                var scene = root.GetComponent<HomeScene>();
                if (!scene)
                {
                    var farm = root.GetComponent<FarmScene>();
                    PokiCanvas view = null;
                    RectTransform content = null;
                    if (farm)
                    {
                        var so = new SerializedObject(farm);
                        view = so.FindProperty("view").objectReferenceValue as PokiCanvas;
                        content = so.FindProperty("content").objectReferenceValue as RectTransform;
                        Object.DestroyImmediate(farm);
                    }
                    scene = root.AddComponent<HomeScene>();
                    scene.SetupView(view ? view : root.GetComponentInChildren<PokiCanvas>(true), content);
                }
                var nen = root.transform.Find("Canvas/Nen") as RectTransform;
                var khung = Find("khung_anh");
                var safe = root.transform.Find("Canvas/An toan/Khung") as RectTransform;
                if (!nen || !khung || !safe)
                {
                    Debug.LogError("[Nhà] Screens/Home thiếu Canvas/Nen, khung_anh hoặc Canvas/An toan/Khung.");
                    return false;
                }
                foreach (Transform c in nen) c.gameObject.SetActive(c == khung || c.name == "nen_hai_ben");
                var sides = Find("nen_hai_ben");
                if (sides && sides.GetComponent<Image>() is Image si)
                {
                    si.sprite = null;
                    si.color = Theme.Hex("#4fa7e3"); // màu biển ngoài ảnh
                    si.raycastTarget = false;
                }
                // gỡ cảnh trang trại (keo + ảnh nền farm), dựng thế giới Nhà
                foreach (var n in new[] { "keo", "the_gioi" })
                {
                    var old = khung.Find(n);
                    if (old) Object.DestroyImmediate(old.gameObject);
                }
                var oldFrame = Find("anh_nen_farm_bg");
                if (oldFrame) Object.DestroyImmediate(oldFrame.gameObject);
                var khungImg = khung.GetComponent<Image>();
                if (khungImg)
                {
                    khungImg.sprite = null;
                    khungImg.color = Theme.Hex("#4fa7e3");
                }

                var world = Node(khung, "the_gioi");
                At(world, new Vector2(0, 1), Vector2.zero, worldSize, new Vector2(0, 1)); // LandView neo trên trái
                var ground = Img(world, "nen", baseSprite, Color.white, true);
                Fill(ground.rectTransform);
                if (water) ground.material = water; // sóng vỗ bờ
                else Debug.LogWarning("[Nhà] Chưa có shader UIInkWater hoặc " + DistPath + ": chưa có sóng.");
                var tap = ground.gameObject.AddComponent<HomeTap>();
                var tiles = Fill(Node(world, "o_lat"));
                var objs = Fill(Node(world, "vat"));
                // sáng tối dùng chung với các đảo (DayNight, DayCycle theo giờ máy): nhuộm, tia nắng; đèn công trình ở lớp "den"
                var dayRoot = Fill(Node(world, "sang_toi"));
                var mul = AssetDatabase.LoadAssetAtPath<Material>("Assets/03 Art/Islands/day_multiply.mat");
                var raysMat = AssetDatabase.LoadAssetAtPath<Material>("Assets/03 Art/Islands/day_rays.mat");
                var tint = Img(dayRoot, "nhuom", null, Color.white);
                Fill(tint.rectTransform);
                tint.material = mul;
                var rays = Img(dayRoot, "nang", null, new Color(1, 1, 1, 0));
                Fill(rays.rectTransform);
                rays.material = raysMat;
                var lamps = Fill(Node(dayRoot, "den_dao"));
                var dn = dayRoot.gameObject.AddComponent<DayNight>();
                dn.Setup(tint, rays, lamps, AssetDatabase.LoadAssetAtPath<GameObject>(GlowItemPath)?.GetComponent<Image>(),
                    AssetDatabase.LoadAssetAtPath<TextAsset>("Assets/03 Art/Islands/island_anim.json"), "home");
                if (!mul || !raysMat) Debug.LogWarning("[Nhà] Chưa có day_multiply.mat / day_rays.mat (menu PokiClash/Sáng tối của các đảo): Nhà chưa nhuộm theo giờ.");
                var lights = Fill(Node(world, "den"));
                var clouds = Fill(Node(world, "may"));

                // kéo, phóng to thu nhỏ nhẹ: LandView của màn Đảo (bỏ HubPan cũ)
                var oldPan = khung.GetComponent<HubPan>();
                if (oldPan) Object.DestroyImmediate(oldPan);
                var landView = khung.GetComponent<LandView>();
                if (!landView) landView = khung.gameObject.AddComponent<LandView>();
                var vso = new SerializedObject(landView);
                vso.FindProperty("maxZoom").floatValue = 1.25f;
                vso.ApplyModifiedPropertiesWithoutUndo();
                scene.SetupMap(landView, world, ground, tap, tiles, objs, lights, clouds, gridTop, obj, tile, glowItem, cloud, arts, glowSprite, treeItem, trees, tileArt);

                BuildUi(assets, scene, safe);
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
                return true;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static void BuildUi(UiAssets assets, HomeScene scene, RectTransform safe)
        {
            foreach (var n in new[] { "hang_nut", "nha_ui", "cuon", "trang" })
            {
                var old = safe.Find(n);
                if (!old) continue;
                if (n == "hang_nut" || n == "nha_ui") Object.DestroyImmediate(old.gameObject);
                else old.gameObject.SetActive(false);
            }
            var ui = Fill(Node(safe, "nha_ui"));
            ui.SetAsLastSibling();
            var paper = new Color(1f, 0.98f, 0.92f, 0.95f);

            // dòng tài nguyên dưới thanh trên
            var resBg = Img(ui, "tai_nguyen", Sketch.Pill, paper, false, true);
            At(resBg.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -SceneRoot.BarHeight - 4), new Vector2(1020, 60), new Vector2(0.5f, 1)); // dưới thanh trên
            var res = Text(resBg.transform, "chu", 26, Theme.Ink);
            Fill(res.rectTransform).offsetMin = new Vector2(16, 0);
            res.rectTransform.offsetMax = new Vector2(-16, 0);
            res.enableAutoSizing = true;
            res.fontSizeMin = 18;
            res.fontSizeMax = 26;

            // hàng nút ở đáy
            var bar = Node(ui, "hang_nut_nha", typeof(HorizontalLayoutGroup));
            At(bar, new Vector2(0.5f, 0), new Vector2(0, 24), new Vector2(1040, 120), new Vector2(0.5f, 0));
            var hl = bar.GetComponent<HorizontalLayoutGroup>();
            hl.spacing = 10;
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = false;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            var sz = new Vector2(196, 110);
            var bBuild = Button(assets, bar, "xay", "Xây", BtnColor.Green, sz);
            var bPaint = Button(assets, bar, "lat", "Lát ô", BtnColor.Yellow, sz);
            var bAuto = Button(assets, bar, "tu_xep", "Tự xếp", BtnColor.Blue, sz);
            var bHarvest = Button(assets, bar, "thu", "Thu hết", BtnColor.Orange, sz);
            var bSail = Button(assets, bar, "ra_dao", "Ra đảo", BtnColor.Red, sz);

            // gợi ý trên hàng nút
            var hintBg = Img(ui, "goi_y", Sketch.PanelThin, paper, false, true);
            At(hintBg.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 154), new Vector2(1020, 64), new Vector2(0.5f, 0));
            var hint = Text(hintBg.transform, "chu", 24, Theme.Ink);
            Fill(hint.rectTransform).offsetMin = new Vector2(16, 4);
            hint.rectTransform.offsetMax = new Vector2(-16, -4);
            hint.enableAutoSizing = true;
            hint.fontSizeMin = 16;
            hint.fontSizeMax = 24;

            // khay (chế độ xây, lát): lưới nút nhỏ
            var tray = Node(ui, "khay", typeof(GridLayoutGroup));
            At(tray, new Vector2(0.5f, 0), new Vector2(0, 228), new Vector2(1040, 250), new Vector2(0.5f, 0));
            var gl = tray.GetComponent<GridLayoutGroup>();
            gl.cellSize = new Vector2(200, 112);
            gl.spacing = new Vector2(8, 8);
            gl.childAlignment = TextAnchor.LowerCenter;
            gl.startCorner = GridLayoutGroup.Corner.LowerLeft;
            gl.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            gl.constraintCount = 5;
            tray.gameObject.SetActive(false);

            // bảng chọn (công trình, ô rừng, bóng ma)
            var panel = Img(ui, "bang", Sketch.Panel, paper, true, true);
            At(panel.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 228), new Vector2(1020, 420), new Vector2(0.5f, 0));
            var title = Text(panel.transform, "tieu_de", 36, Theme.Ink, TextAlignmentOptions.Left);
            At(title.rectTransform, new Vector2(0, 1), new Vector2(32, -20), new Vector2(950, 50), new Vector2(0, 1));
            var body = Text(panel.transform, "noi_dung", 26, Theme.Ink2, TextAlignmentOptions.TopLeft);
            At(body.rectTransform, new Vector2(0, 1), new Vector2(32, -78), new Vector2(950, 200), new Vector2(0, 1));
            body.enableAutoSizing = true;
            body.fontSizeMin = 18;
            body.fontSizeMax = 26;
            var row = Node(panel.transform, "nut", typeof(HorizontalLayoutGroup));
            At(row, new Vector2(0.5f, 0), new Vector2(0, 22), new Vector2(980, 110), new Vector2(0.5f, 0));
            var rl = row.GetComponent<HorizontalLayoutGroup>();
            rl.spacing = 14;
            rl.childAlignment = TextAnchor.MiddleCenter;
            rl.childControlWidth = rl.childControlHeight = false;
            rl.childForceExpandWidth = rl.childForceExpandHeight = false;
            var bsz = new Vector2(230, 100); // bốn nút: Thu, Giao tướng, Lên cấp, Dời
            var a = Button(assets, row, "a", "Thu", BtnColor.Orange, bsz);
            var b = Button(assets, row, "b", "Giao tướng", BtnColor.Blue, bsz);
            var c = Button(assets, row, "c", "Lên cấp", BtnColor.Green, bsz);
            var dBtn = Button(assets, row, "d", "Dời", BtnColor.Purple, bsz);
            panel.gameObject.SetActive(false);

            scene.SetupUi(res, hint, bBuild, bPaint, bAuto, bHarvest, bSail, tray, assets.prefabs.buttonSmall, panel.rectTransform, title, body, a, b, c, dBtn);
        }

        // ---------- scene, Build Settings ----------

        static void MakeScene()
        {
            if (!File.Exists(ScenePath))
            {
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
                var prev = SceneManager.GetActiveScene();
                SceneManager.SetActiveScene(scene);
                var screen = AssetDatabase.LoadAssetAtPath<GameObject>(ScreenPath);
                ((GameObject)PrefabUtility.InstantiatePrefab(screen)).name = SceneIds.Home;
                SceneManager.SetActiveScene(prev);
                EditorSceneManager.SaveScene(scene, ScenePath);
                EditorSceneManager.CloseScene(scene, true);
            }
            var list = EditorBuildSettings.scenes.ToList();
            if (list.All(x => x.path != ScenePath))
            {
                list.Add(new EditorBuildSettingsScene(ScenePath, true));
                EditorBuildSettings.scenes = list.ToArray();
            }
        }

        // ---------- chạy không cần bấm menu ----------

        static double nextPoll, tourStart;
        static string Flag(string n) => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/" + n));

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            if (!EditorApplication.isPlayingOrWillChangePlaymode)
            {
                if (File.Exists(Flag("home_build.flag")))
                {
                    File.Delete(Flag("home_build.flag"));
                    Build();
                }
                else if (File.Exists(Flag("home_tour.flag")))
                {
                    File.Delete(Flag("home_tour.flag"));
                    SessionState.SetBool("HomeTour", true);
                    tourStart = EditorApplication.timeSinceStartup;
                    EditorApplication.isPlaying = true;
                }
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 120)
            {
                Debug.LogWarning("[Nhà] Tour quá 120 giây: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("HomeTour", false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool("HomeTour", false);
                BootTitle.Dismiss();
                App.I.StartCoroutine(Tour());
            }
        }

        // mở Nhà, chụp: thường, xây (khay + bóng ma), lát ô; rồi Stop
        static IEnumerator Tour()
        {
            var dir = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots"));
            Directory.CreateDirectory(dir);
            var s = App.Save.Data;
            foreach (var h in App.Data.Heroes.Take(6)) s.Hero(h.id).owned = true; // đủ 3 tướng để mở Nhà
            s.home = null; // bản lưu thử: dựng lại Nhà theo số liệu hiện tại (khoảnh đầu, đường đất)
            if (s.home == null && s.level < 10) s.level = 10;
            App.Router.Go(SceneIds.Home);
            yield return new WaitForSecondsRealtime(4f);
            var home = Object.FindFirstObjectByType<HomeScene>();
            void Shot(string n)
            {
                ScreenCapture.CaptureScreenshot(Path.Combine(dir, $"home_{n}.png"));
                Debug.Log("[Thử] Nhà: chụp " + n);
            }
            Shot("1_thuong");
            yield return new WaitForSecondsRealtime(1f);
            if (home)
            {
                var so = new SerializedObject(home);
                (so.FindProperty("btnBuild").objectReferenceValue as SketchButton)?.SimulateClick();
                yield return new WaitForSecondsRealtime(0.8f);
                Shot("2_khay_xay");
                yield return new WaitForSecondsRealtime(1f);
                // dời công trình: ở chế độ xây chạm kho (35,30) để nhấc lên, chạm đất ở (36,38) để đổi chỗ, chụp, rồi Đặt
                {
                    const System.Reflection.BindingFlags F = System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance;
                    var t = home.GetType();
                    var cellTop = t.GetMethod("CellTop", F);
                    var onTap = t.GetMethod("OnTap", F);
                    var place = t.GetMethod("PlaceGhost", F);
                    var hb = App.Save.Data.home.buildings.Find(x => x.def == "storage");
                    var lv = so.FindProperty("landView").objectReferenceValue as LandView;
                    if (cellTop != null && onTap != null && place != null && hb != null)
                    {
                        if (lv) lv.Show((Vector2)cellTop.Invoke(home, new object[] { 35f, 36f }), 1f, 0); // máy cố định giữa chỗ cũ và chỗ mới
                        yield return new WaitForSecondsRealtime(0.3f);
                        onTap.Invoke(home, new object[] { cellTop.Invoke(home, new object[] { hb.gx + 2f, hb.gy + 2f }) });
                        yield return new WaitForSecondsRealtime(0.4f);
                        onTap.Invoke(home, new object[] { cellTop.Invoke(home, new object[] { 36.5f, 38.5f }) });
                        yield return new WaitForSecondsRealtime(0.6f);
                        Shot("9_doi");
                        yield return new WaitForSecondsRealtime(0.5f);
                        place.Invoke(home, null);
                        yield return new WaitForSecondsRealtime(0.6f);
                        Debug.Log($"[Nhà] Dời kho: giờ ở {hb.gx},{hb.gy}");
                        Shot("9_doi_xong");
                        yield return new WaitForSecondsRealtime(0.5f);
                    }
                    else Debug.LogWarning("[Nhà] Tour dời: không tìm thấy CellTop / OnTap / PlaceGhost / kho");
                }
                (so.FindProperty("btnBuild").objectReferenceValue as SketchButton)?.SimulateClick();
                (so.FindProperty("btnPaint").objectReferenceValue as SketchButton)?.SimulateClick();
                yield return new WaitForSecondsRealtime(0.8f);
                Shot("3_lat_o");
                yield return new WaitForSecondsRealtime(1f);
                (so.FindProperty("btnPaint").objectReferenceValue as SketchButton)?.SimulateClick();
                // tia nắng phải đi theo bản đồ khi kéo (shader UISunRays tính theo toạ độ ảnh): ép trưa, chụp, kéo 400 px, chụp
                var view = so.FindProperty("landView").objectReferenceValue as LandView;
                DayCycle.Override = 12f;
                var c0 = new Vector2(2300, 1500); // giữa khoảnh đầu, sát biển (thấy sóng)
                if (view) view.Show(c0, 1f, 0);
                yield return new WaitForSecondsRealtime(0.8f);
                Shot("4_nang_a");
                yield return new WaitForSecondsRealtime(0.5f);
                if (view) view.Show(c0 + new Vector2(400, 0), 1f, 0);
                yield return new WaitForSecondsRealtime(0.8f);
                Shot("5_nang_b");
                yield return new WaitForSecondsRealtime(0.5f);
                if (view) view.Show(c0, view.MinZoom, 0); // thu nhỏ hết cỡ
                yield return new WaitForSecondsRealtime(0.8f);
                Shot("6_thu_nho");
                yield return new WaitForSecondsRealtime(0.5f);
                // lát thử vài ô cạnh nhau để soi mép nối
                var sv = App.Save.Data;
                sv.home.wood = 200;
                sv.home.ore = 50;
                var plog = new System.Text.StringBuilder("[Nhà] Lát thử:");
                foreach (var (tx, ty, id) in new[] { (14, 16, "water"), (15, 16, "water"), (14, 17, "water"), (15, 17, "sand"), (16, 16, "sand"), (13, 17, "stone"), (13, 18, "stone") })
                    plog.Append($" {tx},{ty} {id}={Home.Paint(sv, App.Data, tx, ty, id)}");
                home.Refresh();
                plog.Append(" | công trình:");
                foreach (var b in sv.home.buildings) plog.Append($" {b.def}@{b.gx},{b.gy}");
                Debug.Log(plog.ToString());
                if (view) view.Show(new Vector2(2040, 1060), 1.25f, 0);
                yield return new WaitForSecondsRealtime(0.8f);
                Shot("7_o_lat");
                yield return new WaitForSecondsRealtime(0.5f);
                // sóng vỗ bờ: hai ảnh cùng góc máy cách 1,2 giây (bờ biển phải bến)
                if (view) view.Show(new Vector2(2900, 2150), 1f, 0);
                yield return new WaitForSecondsRealtime(0.8f);
                Shot("8_song_a");
                yield return new WaitForSecondsRealtime(1.2f);
                Shot("8_song_b");
                yield return new WaitForSecondsRealtime(0.5f);
                // nhấn giữ rồi kéo (sự kiện chạm giả đi đúng đường HomeTap): chạm kho thấy nút Dời; giữ 0,6 s nhấc lên, kéo 4 ô, thả, Đặt;
                // kéo đất trống thì bản đồ phải trôi (HomeTap chuyển cho LandView)
                {
                    const System.Reflection.BindingFlags F = System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance;
                    var t = home.GetType();
                    var cellTop = t.GetMethod("CellTop", F);
                    var place = t.GetMethod("PlaceGhost", F);
                    var tapC = so.FindProperty("tap").objectReferenceValue as HomeTap;
                    var hb = App.Save.Data.home.buildings.Find(x => x.def == "storage");
                    var es = UnityEngine.EventSystems.EventSystem.current;
                    if (tapC && hb != null && cellTop != null && place != null && es && view)
                    {
                        var groundRt = (RectTransform)tapC.transform;
                        var ray = groundRt.GetComponentInParent<GraphicRaycaster>();
                        var cam = ray ? ray.eventCamera : null;
                        Vector2 Map(float gx, float gy) => (Vector2)cellTop.Invoke(home, new object[] { gx, gy });
                        Vector2 Scr(Vector2 m)
                        {
                            var r = groundRt.rect;
                            return RectTransformUtility.WorldToScreenPoint(cam, groundRt.TransformPoint(new Vector3(r.xMin + m.x, r.yMax - m.y, 0)));
                        }
                        UnityEngine.EventSystems.PointerEventData Ev(Vector2 m) => new UnityEngine.EventSystems.PointerEventData(es)
                        {
                            pointerId = 7, position = Scr(m), pressPosition = Scr(m), button = UnityEngine.EventSystems.PointerEventData.InputButton.Left,
                            pointerPressRaycast = new UnityEngine.EventSystems.RaycastResult { module = ray },
                        };
                        view.Show(Map(hb.gx + 2f, hb.gy + 2f), 1f, 0);
                        yield return new WaitForSecondsRealtime(0.4f);
                        // chạm: bảng có nút Dời
                        var tp = Ev(Map(hb.gx + 2.5f, hb.gy + 2.5f));
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, tp, UnityEngine.EventSystems.ExecuteEvents.pointerDownHandler);
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, tp, UnityEngine.EventSystems.ExecuteEvents.pointerUpHandler);
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, tp, UnityEngine.EventSystems.ExecuteEvents.pointerClickHandler);
                        yield return new WaitForSecondsRealtime(0.5f);
                        Shot("10_bang_doi");
                        yield return new WaitForSecondsRealtime(0.4f);
                        // giữ rồi kéo
                        var from = new Vector2(hb.gx + 2.5f, hb.gy + 2.5f);
                        var to = from + new Vector2(-4, 0);
                        int ox = hb.gx, oy = hb.gy;
                        var pe = Ev(Map(from.x, from.y));
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pe, UnityEngine.EventSystems.ExecuteEvents.pointerDownHandler);
                        yield return new WaitForSecondsRealtime(0.65f);
                        bool lifted = tapC.Grabbing;
                        for (int k = 1; k <= 8; k++)
                        {
                            var c = Vector2.Lerp(from, to, k / 8f);
                            pe.position = Scr(Map(c.x, c.y));
                            if (k == 1) UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pe, UnityEngine.EventSystems.ExecuteEvents.beginDragHandler);
                            else UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pe, UnityEngine.EventSystems.ExecuteEvents.dragHandler);
                            yield return null;
                        }
                        yield return new WaitForSecondsRealtime(0.3f);
                        Shot("10_keo");
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pe, UnityEngine.EventSystems.ExecuteEvents.pointerUpHandler);
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pe, UnityEngine.EventSystems.ExecuteEvents.endDragHandler);
                        yield return new WaitForSecondsRealtime(0.4f);
                        Shot("10_tha");
                        place.Invoke(home, null);
                        yield return new WaitForSecondsRealtime(0.4f);
                        Debug.Log($"[Nhà] Giữ kéo: nhấc {(lifted ? "được" : "KHÔNG được")}, kho {ox},{oy} → {hb.gx},{hb.gy}");
                        // kéo đất trống: bản đồ phải trôi
                        string before = view.Describe();
                        var g0 = new Vector2(hb.gx - 6f, hb.gy + 6f);
                        var pg = Ev(Map(g0.x, g0.y));
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pg, UnityEngine.EventSystems.ExecuteEvents.pointerDownHandler);
                        for (int k = 1; k <= 6; k++)
                        {
                            pg.position = Scr(Map(g0.x, g0.y)) + new Vector2(30 * k, 0);
                            if (k == 1) UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pg, UnityEngine.EventSystems.ExecuteEvents.beginDragHandler);
                            else UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pg, UnityEngine.EventSystems.ExecuteEvents.dragHandler);
                            yield return null;
                        }
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pg, UnityEngine.EventSystems.ExecuteEvents.pointerUpHandler);
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pg, UnityEngine.EventSystems.ExecuteEvents.endDragHandler);
                        yield return new WaitForSecondsRealtime(0.2f);
                        Debug.Log($"[Nhà] Kéo đất trống: trước {before} | sau {view.Describe()}");
                    }
                    else Debug.LogWarning("[Nhà] Tour giữ kéo: thiếu tap / kho / EventSystem / LandView");
                }
                DayCycle.Override = null;
            }
            Debug.Log("[Thử] Xong Nhà");
            tourStart = 0;
            EditorApplication.isPlaying = false;
        }
    }
}
