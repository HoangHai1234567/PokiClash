// Màn Nhà (GD_Claude/21_Nha_Home.md, mốc H2). Menu "PokiClash/Prefab/Nhà và side meta/Nhà: dựng màn" (chạy lại được, dựng lại các lớp):
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
        // biển kiểu Clash of Critters (GD_Claude/22 mục 4): shader PokiClash/UIHomeSea, ảnh sinh bằng ArtGen/Home/sea/make_home_sea.py
        const string SeaMatPath = "Assets/03 Art/Home/home_sea.mat";
        const string SeaMaskPath = "Assets/03 Art/Baked/Home/home_sea.png";
        const string SeaFlowPath = "Assets/03 Art/Baked/Home/home_sea_flow.png";
        const string SeaCausticPath = "Assets/03 Art/Baked/Home/home_sea_caustic.png";
        const string RiverPath = "Assets/03 Art/Baked/Home/home_river.png"; // thác, suối: vệt nước chảy
        // mặt nạ tự sáng của công trình (home_e_<def>.png, ArtGen/Home/night/home_emit.py), shader PokiClash/UIIslandEmit của đèn đêm sảnh
        const string EmitMatPath = "Assets/03 Art/Home/home_emit.mat";
        const string GlowItemPath = "Assets/04 Prefabs/Items/HinhDong.prefab";
        const string ArtDir = "Assets/03 Art/Home/";
        const string ScenePath = "Assets/00 Scenes/Home.unity";
        const string GridMatPath = "Assets/03 Art/Home/home_grid.mat"; // lưới phát sáng chế độ xây (shader PokiClash/UIHomeGrid)
        const string SelectMatPath = "Assets/03 Art/Home/home_select.mat"; // vật đang chọn sáng nhẹ (shader PokiClash/UIHomeSelect)
        // quái đi lại trên bản đồ: dùng lại thú, hạt, hộp chọn tướng của Trang trại (menu "PokiClash/Prefab/Nhà và side meta/Trang trại: cảnh thật")
        const string PetPath = "Assets/04 Prefabs/Items/ThuTrangTrai.prefab";
        const string FxPath = "Assets/04 Prefabs/Items/HatTrangTrai.prefab";
        const string PickerPath = "Assets/04 Prefabs/Dialogs/ChonTuongTrangTrai.prefab";
        static readonly string[] PropNames = { "hoe", "can", "basket", "bread", "hammer", "sack", "apple", "carrot", "dust", "spark", "smoke", "heart" };
        const float CW = 96;

        [MenuItem("PokiClash/Prefab/Nhà và side meta/Nhà: dựng màn", priority = 64)]
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
            var baseSprite = ImportSprite(ArtDir + "home_base.png", 4096); // 2210 x 1225 (ArtImporter cũng nhập 4096)
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
                var meta0 = new HomeScene.ArtMeta
                {
                    id = kv.Key, sprite = sp, pivot = piv.Count >= 2 ? new Vector2((float)(double)piv[0], (float)(double)piv[1]) : new Vector2(0.5f, 0),
                    foot = (float)J.Num(m, "foot", sp.rect.width), cells = J.Int(m, "cells"),
                };
                arts.Add(meta0);
                // mặt nạ tự sáng cùng khung ảnh công trình: home_b_<def> → home_e_<def>
                if (kv.Key.StartsWith("home_b_"))
                {
                    var esp = ImportSprite(ArtDir + "home_e_" + kv.Key.Substring(7) + ".png", 1024);
                    if (esp)
                    {
                        var em = meta0;
                        em.id = "home_e_" + kv.Key.Substring(7);
                        em.sprite = esp;
                        arts.Add(em);
                    }
                }
            }
            var tileSprite = TileSprite();
            var trees = TreeSprites();
            var tileArt = TileArt();
            var water = SeaMat() ?? WaterMat();
            var glowSprite = AssetDatabase.LoadAssetAtPath<Sprite>("Assets/03 Art/Islands/Anim/anim_glow.png");

            var obj = BuildObj();
            var tile = BuildImageItem(TilePath, "NhaOLat", tileSprite);
            var cloud = BuildImageItem(CloudPath, "NhaMay", null);
            var treeItem = BuildImageItem(TreePath, "NhaCay", null);
            var glowItem = AssetDatabase.LoadAssetAtPath<GameObject>(GlowItemPath)?.GetComponent<Image>() ?? cloud;

            // bản đồ: ảnh nền phóng sao cho thoi đồng cỏ rộng grid ô x 96 px (72 ô, ArtGen/Home/base/compose_base72.py)
            float s = (float)(J.Int(baseMeta, "grid", 48) * CW / J.Num(baseMeta, "diamondW", 1460));
            var worldSize = new Vector2((float)J.Num(baseMeta, "w") * s, (float)J.Num(baseMeta, "h") * s);
            var topArr = J.Arr(baseMeta, "top");
            var gridTop = new Vector2((float)(double)topArr[0] * s, (float)(double)topArr[1] * s);

            if (!BuildScreen(assets, baseSprite, worldSize, gridTop, J.Int(baseMeta, "grid", 72), obj, tile, glowItem, cloud, arts.ToArray(), glowSprite, treeItem, trees, tileArt, water)) return;
            AssetDatabase.SaveAssets();
            HomeSeaOutMenu.Patch(); // biển ngoài ảnh nền như sảnh (lớp bien_ngoai, nen_hai_ben), 2026-11-27
            MakeScene();
            Debug.Log($"[Nhà] Đã dựng {ScreenPath} (bản đồ {worldSize.x:0} x {worldSize.y:0} px, {arts.Count} ảnh), {ObjPath}, {TilePath}, {CloudPath}, scene {ScenePath}.");
        }

        // ---------- ảnh ----------

        internal static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));

        internal static Sprite ImportSprite(string path, int max)
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

        // ảnh dữ liệu (không sRGB, không mip, không nén): mặt nạ bờ kẹp mép; nhiễu, vân lặp
        static Texture2D DataTex(string path, bool repeat, int max)
        {
            if (!File.Exists(path)) return null;
            AssetDatabase.ImportAsset(path);
            var ti = (TextureImporter)AssetImporter.GetAtPath(path);
            var wrap = repeat ? TextureWrapMode.Repeat : TextureWrapMode.Clamp;
            if (ti.sRGBTexture || ti.mipmapEnabled || ti.textureCompression != TextureImporterCompression.Uncompressed ||
                ti.textureType != TextureImporterType.Default || ti.wrapMode != wrap || ti.maxTextureSize != max)
            {
                ti.textureType = TextureImporterType.Default;
                ti.sRGBTexture = false;
                ti.mipmapEnabled = false;
                ti.alphaSource = TextureImporterAlphaSource.FromInput;
                ti.wrapMode = wrap;
                ti.filterMode = FilterMode.Bilinear;
                ti.textureCompression = TextureImporterCompression.Uncompressed;
                ti.maxTextureSize = max;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Texture2D>(path);
        }

        // biển kiểu Clash of Critters (GD_Claude/22 mục 4) trên ảnh nền: thiếu shader hoặc ảnh thì về sóng mực cũ (UIInkWater)
        static Material SeaMat()
        {
            var shader = Shader.Find("PokiClash/UIHomeSea");
            var mask = DataTex(SeaMaskPath, false, 2048);
            var flow = DataTex(SeaFlowPath, true, 256);
            var caustic = DataTex(SeaCausticPath, true, 512);
            if (!shader || !mask || !flow || !caustic)
            {
                Debug.LogWarning("[Nhà] Chưa có shader PokiClash/UIHomeSea hoặc ảnh biển (ArtGen/Home/sea/make_home_sea.py): dùng sóng mực cũ.");
                return null;
            }
            var mat = AssetDatabase.LoadAssetAtPath<Material>(SeaMatPath);
            if (!mat)
            {
                mat = new Material(shader);
                AssetDatabase.CreateAsset(mat, SeaMatPath);
            }
            mat.shader = shader;
            mat.SetTexture("_SeaTex", mask);
            mat.SetTexture("_FlowTex", flow);
            mat.SetTexture("_CausticTex", caustic);
            var river = DataTex(RiverPath, false, 2048);
            if (river) mat.SetTexture("_RiverTex", river);
            // biển như sảnh (người dùng 2026-11-27): ảnh biển lát của sảnh, lặp theo cỡ ảnh nền (UIHomeSea _TileST)
            var tileSea = AssetDatabase.LoadAssetAtPath<Texture2D>("Assets/03 Art/Islands/sanh_bien.png");
            if (tileSea) mat.SetTexture("_TileTex", tileSea);
            else Debug.LogWarning("[Nhà] Thiếu " + RiverPath + ": thác, suối chưa chảy.");
            EditorUtility.SetDirty(mat);
            return mat;
        }

        // mặt nạ tự sáng công trình: dùng shader đèn đêm của sảnh, sáng thêm ít hơn (cửa sổ nhỏ, đứng gần)
        static Material EmitMat()
        {
            var shader = Shader.Find("PokiClash/UIIslandEmit");
            if (!shader)
            {
                Debug.LogWarning("[Nhà] Chưa có shader PokiClash/UIIslandEmit: công trình chưa sáng đèn ban đêm.");
                return null;
            }
            var mat = AssetDatabase.LoadAssetAtPath<Material>(EmitMatPath);
            if (!mat)
            {
                mat = new Material(shader);
                mat.SetFloat("_Boost", 0.45f);
                mat.SetFloat("_Shimmer", 0.3f);
                AssetDatabase.CreateAsset(mat, EmitMatPath);
            }
            mat.shader = shader;
            EditorUtility.SetDirty(mat);
            return mat;
        }

        static Material GridMat()
        {
            var shader = Shader.Find("PokiClash/UIHomeGrid");
            if (!shader) return null;
            var mat = AssetDatabase.LoadAssetAtPath<Material>(GridMatPath);
            if (!mat)
            {
                mat = new Material(shader);
                AssetDatabase.CreateAsset(mat, GridMatPath);
            }
            mat.shader = shader;
            EditorUtility.SetDirty(mat);
            return mat;
        }

        static Material SelectMat()
        {
            var shader = Shader.Find("PokiClash/UIHomeSelect");
            if (!shader)
            {
                Debug.LogWarning("[Nhà] Chưa có shader PokiClash/UIHomeSelect: vật đang chọn chỉ nhún, không sáng.");
                return null;
            }
            var mat = AssetDatabase.LoadAssetAtPath<Material>(SelectMatPath);
            if (!mat)
            {
                mat = new Material(shader);
                AssetDatabase.CreateAsset(mat, SelectMatPath);
            }
            mat.shader = shader;
            EditorUtility.SetDirty(mat);
            return mat;
        }

        // số trong bong bóng của vật (Cây bi: số bi đang có), con của "bong"; HomeObject tự xếp icon trái, số phải
        static TextMeshProUGUI BubbleCount(Transform bubble)
        {
            var t = Text(bubble, "so", 40, Theme.Ink, TextAlignmentOptions.MidlineLeft);
            t.textWrappingMode = TextWrappingModes.NoWrap;
            At(t.rectTransform, new Vector2(0, 0.5f), new Vector2(70, 2), new Vector2(80, 64), new Vector2(0, 0.5f));
            t.gameObject.SetActive(false);
            return t;
        }

        // Vá prefab có sẵn, không dựng lại cả màn (người dùng 2026-11-22: chọn vật nhún + sáng nhẹ, số bi trên đầu Cây bi):
        // tạo home_select.mat, thêm chữ số vào bong bóng Items/NhaVat, gắn vật liệu chọn vào Screens/Home. Chạy lại được.
        [MenuItem("PokiClash/Prefab/Nhà và side meta/Nhà: chọn vật sáng + số bi Cây bi", priority = 65)]
        public static void PatchSelect()
        {
            Theme.Init(Load<UiAssets>());
            var mat = SelectMat();
            var obj = PrefabUtility.LoadPrefabContents(ObjPath);
            try
            {
                var ho = obj.GetComponent<HomeObject>();
                var bong = obj.transform.Find("bong");
                if (!ho || !bong) Debug.LogError("[Nhà] " + ObjPath + " thiếu HomeObject hoặc nút \"bong\".");
                else
                {
                    var so = bong.Find("so")?.GetComponent<TextMeshProUGUI>() ?? BubbleCount(bong);
                    ho.SetupCount(so);
                    PrefabUtility.SaveAsPrefabAsset(obj, ObjPath);
                }
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(obj);
            }
            var screen = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                var scene = screen.GetComponentInChildren<HomeScene>(true);
                if (!scene) Debug.LogError("[Nhà] " + ScreenPath + " thiếu HomeScene.");
                else
                {
                    scene.SetupSelect(mat);
                    PrefabUtility.SaveAsPrefabAsset(screen, ScreenPath);
                }
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(screen);
            }
            AssetDatabase.SaveAssets();
            Debug.Log($"[Nhà] Đã vá {ObjPath} (số trong bong bóng), {ScreenPath} (vật liệu chọn {(mat ? SelectMatPath : "trống")}).");
        }

        // ---------- dựng nút ----------

        internal static RectTransform Node(Transform parent, string name, params System.Type[] types)
        {
            var go = new GameObject(name, new[] { typeof(RectTransform) }.Concat(types).ToArray());
            go.layer = LayerMask.NameToLayer("UI");
            var rt = (RectTransform)go.transform;
            if (parent) rt.SetParent(parent, false);
            return rt;
        }

        internal static RectTransform Fill(RectTransform rt)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            return rt;
        }

        internal static RectTransform At(RectTransform rt, Vector2 anchor, Vector2 pos, Vector2 size, Vector2 pivot)
        {
            rt.anchorMin = rt.anchorMax = anchor;
            rt.pivot = pivot;
            rt.anchoredPosition = pos;
            rt.sizeDelta = size;
            return rt;
        }

        internal static Image Img(Transform parent, string name, Sprite s, Color c, bool raycast = false, bool sliced = false)
        {
            var img = Node(parent, name, typeof(CanvasRenderer), typeof(Image)).GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = c;
            img.type = sliced ? Image.Type.Sliced : Image.Type.Simple;
            img.raycastTarget = raycast;
            return img;
        }

        internal static TextMeshProUGUI Text(Transform parent, string name, float size, Color color, TextAlignmentOptions align = TextAlignmentOptions.Center)
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

        internal static SketchButton Button(UiAssets assets, Transform parent, string name, string label, BtnColor color, Vector2 size)
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
            var count = BubbleCount(bubble.transform);
            bubble.gameObject.SetActive(false);
            root.GetComponent<HomeObject>().Setup(img, label, bubble, icon);
            root.GetComponent<HomeObject>().SetupCount(count);
            HomeCrittersMenu.AddBubbleRing(bubble.transform, root.GetComponent<HomeObject>()); // vòng tiến độ, chạm để thu
            return Save<HomeObject>(root.gameObject, ObjPath);
        }

        static Image BuildImageItem(string path, string name, Sprite s)
        {
            var img = Img(null, name, s, Color.white);
            At(img.rectTransform, new Vector2(0, 1), Vector2.zero, new Vector2(192, 96), new Vector2(0.5f, 0.5f));
            return Save<Image>(img.gameObject, path);
        }

        // ---------- màn hình ----------

        static bool BuildScreen(UiAssets assets, Sprite baseSprite, Vector2 worldSize, Vector2 gridTop, int grid, HomeObject obj, Image tile, Image glowItem,
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
                // lưới phát sáng của chế độ xây: trên ô lát, dưới công trình; HomeScene bật, chỉnh số lúc chạy
                var gridImg = Img(world, "luoi", null, Color.white);
                Fill(gridImg.rectTransform);
                gridImg.material = GridMat();
                gridImg.enabled = false;
                if (!gridImg.material) Debug.LogWarning("[Nhà] Chưa có shader PokiClash/UIHomeGrid: chế độ xây chưa có lưới sáng.");
                // lớp môi trường kiểu Critters (bảng HomeScene.Layers): đồ ven biển, cỏ rải, vách cao nguyên, môi cỏ (GD_Claude/22 mốc A5); cây rìa
                var catLayer = Fill(Node(world, "cat"));
                Fill(Node(world, "co_rai"));
                var wallLayer = Fill(Node(world, "vach"));
                Fill(Node(world, "moi_co"));
                float terraceH = BuildKit(wallLayer, catLayer);
                var rim = Fill(Node(world, "rung_nen"));
                var objs = Fill(Node(world, "vat"));
                var fxLayer = Fill(Node(world, "hat")); // hạt của quái (bụi, tim, tia lửa), cùng khung với lớp vật
                BuildWind(fxLayer);
                var clouds = Fill(Node(world, "may", typeof(CanvasGroup)));
                // mây che rìa: từng đám rời (người dùng 2026-11-19: mây tách riêng, tàu đi qua thì toả ra, thấy rõ thuyền; mây Nhà cùng loại mây
                // đảo), CloudRing của phiên sảnh lo trôi, toả quanh tàu; chuyến tàu qua mây mang theo lúc chụp màn. Nằm dưới lớp sáng tối
                // (DayNight.clouds nhân CloudTint, rồi nhuộm theo giờ cùng cảnh như sảnh); tàu chèn ngay trên lớp mây
                var cloudGroup = clouds.GetComponent<CanvasGroup>();
                cloudGroup.blocksRaycasts = false;
                cloudGroup.interactable = false;
                var cloudImgs = BuildClouds(clouds, worldSize, gridTop.x); // gridTop.x: mũi trên và mũi dưới (bến) cùng hoành độ
                clouds.gameObject.AddComponent<CloudRing>().Setup(cloudImgs, 290);
                // sáng tối dùng chung với các đảo (DayNight, DayCycle theo giờ máy): nhuộm, tia nắng; mặt nạ tự sáng công trình ở lớp "tu_sang"
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
                // biển ngoài ảnh (nền khung, hai bên màn rộng) tối theo đêm như sảnh; biển trong ảnh tối qua shader sóng (_PokiNight)
                var outside = new[] { khungImg as Graphic, Find("nen_hai_ben")?.GetComponent<Image>() }.Where(g => g).ToArray();
                dn.Setup(tint, rays, lamps, AssetDatabase.LoadAssetAtPath<GameObject>(GlowItemPath)?.GetComponent<Image>(),
                    AssetDatabase.LoadAssetAtPath<TextAsset>("Assets/03 Art/Islands/island_anim.json"), "home", null, outside);
                var dso = new SerializedObject(dn);
                var cArr = dso.FindProperty("clouds");
                cArr.arraySize = cloudImgs.Length;
                for (int i = 0; i < cloudImgs.Length; i++) cArr.GetArrayElementAtIndex(i).objectReferenceValue = cloudImgs[i];
                dso.ApplyModifiedPropertiesWithoutUndo();
                if (!mul || !raysMat) Debug.LogWarning("[Nhà] Chưa có day_multiply.mat / day_rays.mat (menu PokiClash/Sáng tối của các đảo): Nhà chưa nhuộm theo giờ.");
                var lights = Fill(Node(world, "tu_sang")); // mặt nạ tự sáng công trình (đêm), trên lớp nhuộm

                // kéo, phóng to thu nhỏ nhẹ: LandView của màn Đảo (bỏ HubPan cũ)
                var oldPan = khung.GetComponent<HubPan>();
                if (oldPan) Object.DestroyImmediate(oldPan);
                var landView = khung.GetComponent<LandView>();
                if (!landView) landView = khung.gameObject.AddComponent<LandView>();
                var vso = new SerializedObject(landView);
                vso.FindProperty("maxZoom").floatValue = 1.25f;
                vso.ApplyModifiedPropertiesWithoutUndo();
                scene.SetupMap(landView, world, ground, tap, tiles, objs, lights, clouds, gridTop, obj, tile, glowItem, cloud, arts, glowSprite, treeItem, trees, tileArt);
                var props = new Sprite[System.Enum.GetValues(typeof(FarmProp)).Length];
                for (int i = 0; i < PropNames.Length; i++) props[i] = AssetDatabase.LoadAssetAtPath<Sprite>("Assets/03 Art/Farm/props/farm_" + PropNames[i] + ".png");
                var pet = AssetDatabase.LoadAssetAtPath<GameObject>(PetPath)?.GetComponent<FarmPet>();
                var fxItem = AssetDatabase.LoadAssetAtPath<GameObject>(FxPath)?.GetComponent<FarmFx>();
                var picker = AssetDatabase.LoadAssetAtPath<GameObject>(PickerPath)?.GetComponent<FarmPickerDialog>();
                if (!pet || !fxItem || !picker) Debug.LogWarning("[Nhà] Thiếu " + PetPath + " / " + FxPath + " / " + PickerPath + ": chưa có quái đi lại hoặc hộp chọn tướng.");
                scene.SetupPets(fxLayer, pet, fxItem, props, picker);
                scene.SetupGrid(gridImg);
                // bến tàu ở mũi dưới (bến vẽ trên nền: ArtGen/Home/base/ben_nha.txt): tàu đậu bên phải cầu, mũi hướng lên (vừa từ nam tới),
                // rời bến đi thẳng xuống biển dưới mép ảnh cho lớp mây nhận. Toạ độ local của lớp kéo (neo trên trái): (x, -y) px bản đồ
                var tip = gridTop + new Vector2(0, grid * CW / 2); // mũi dưới đảo (góc ô grid, grid; ô cao CW / 2)
                Vector2 L(Vector2 m) => new Vector2(m.x, -m.y);
                var pier = ShipBuild.Pier(world, L(tip + new Vector2(205, 240)), Vector2.up,
                    new[] { L(tip + new Vector2(215, 470)), L(tip + new Vector2(240, 800)) }, null, 1f, 520);
                scene.SetupPier(pier);
                scene.SetupEnv(rim, EmitMat(), terraceH);
                scene.SetupSelect(SelectMat());
                OrderLayers(world); // tàu trên lớp mây, dưới lớp sáng tối: theo bảng queue

                BuildUi(assets, scene, safe);
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
                return true;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // bộ mảnh môi trường (GD_Claude/22 mốc A5): vách cao nguyên dọc hai cạnh trên đảo (giữa các khối đồi vẽ sẵn) và đồ ven biển trên dải
        // cát; ảnh, điểm neo, chỗ đặt (px bản đồ, gốc trên trái) tính sẵn bằng ArtGen/Home/kit/import_kit.py vào home_kit.json. Trả chiều cao
        // vách (bậc cao: cây rìa đứng trên đó), 0 nếu chưa có bộ mảnh.
        static float BuildKit(RectTransform wallLayer, RectTransform catLayer)
        {
            var path = ArtDir + "home_kit.json";
            if (!File.Exists(path))
            {
                Debug.LogWarning("[Nhà] Chưa có home_kit.json (ArtGen/Home/kit/import_kit.py): chưa có vách, đồ ven biển.");
                return 0;
            }
            var kit = J.Obj(MiniJson.Parse(File.ReadAllText(path)));
            var pieces = J.Obj(kit, "pieces");
            var sprites = new Dictionary<string, Sprite>();
            int n = 0;
            foreach (var (layerName, layer) in new[] { ("vach", wallLayer), ("cat", catLayer) })
            {
                foreach (var o in J.Arr(kit, layerName))
                {
                    var e = J.Obj(o);
                    var id = J.Str(e, "id");
                    if (id == null) continue;
                    if (!sprites.TryGetValue(id, out var sp)) sprites[id] = sp = ImportSprite(ArtDir + id + ".png", 1024);
                    if (!sp) continue;
                    var piv = J.Arr(J.Obj(pieces, id), "pivot");
                    float sc = (float)J.Num(e, "scale", 1);
                    var img = Img(layer, id + "_" + n++, sp, Color.white);
                    var rt = img.rectTransform;
                    rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                    rt.pivot = new Vector2((float)(double)piv[0], (float)(double)piv[1]);
                    rt.sizeDelta = sp.rect.size * sc;
                    rt.anchoredPosition = new Vector2((float)J.Num(e, "x"), -(float)J.Num(e, "y"));
                    if (J.Bool(e, "flip")) rt.localScale = new Vector3(-1, 1, 1); // cạnh "/" dùng bản lật ngang
                }
            }
            return (float)J.Num(kit, "H", 0);
        }

        // lá, cánh hoa bay theo gió (GD_Claude/22 mốc A4; ảnh ArtGen/Home/wind/make_leaves.py): Image dựng sẵn, HomeWind dời lúc chạy
        static void BuildWind(RectTransform fxLayer)
        {
            var look = Enumerable.Range(1, 4).Select(i => ImportSprite(ArtDir + "home_leaf_" + i + ".png", 64)).Where(s => s).ToArray();
            if (look.Length == 0)
            {
                Debug.LogWarning("[Nhà] Thiếu home_leaf_*.png (ArtGen/Home/wind/make_leaves.py): chưa có lá bay.");
                return;
            }
            var gio = Fill(Node(fxLayer, "gio"));
            var imgs = new List<Image>();
            var rnd = new System.Random(3);
            // 120 lá trên bản đồ 7000 x 4200 px: khoảng 6 lá mỗi màn (Critters giữ vài trăm hạt gió cùng lúc trên cả map)
            for (int i = 0; i < 120; i++)
            {
                var sp = look[i % look.Length];
                var img = Img(gio, "la_" + i, sp, Color.white);
                var rt = img.rectTransform;
                rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                rt.pivot = new Vector2(0.5f, 0.5f);
                float k = 1.7f + (float)rnd.NextDouble() * 0.8f;
                rt.sizeDelta = sp.rect.size * k;
                imgs.Add(img);
            }
            gio.gameObject.AddComponent<HomeWind>().Setup(imgs.ToArray());
        }

        // xếp các lớp con của lớp kéo theo render queue (HomeScene.Layers, học Clash of Critters): uGUI vẽ theo thứ tự anh em; nút lạ
        // (không có trong bảng) giữ nguyên ở cuối và báo
        static void OrderLayers(RectTransform world)
        {
            var q = HomeScene.Layers.ToDictionary(l => l.name, l => l.queue);
            var kids = world.Cast<Transform>().ToList();
            foreach (var k in kids.Where(k => !q.ContainsKey(k.name))) Debug.LogWarning("[Nhà] Lớp " + k.name + " không có trong bảng queue HomeScene.Layers.");
            var sorted = kids.OrderBy(k => q.TryGetValue(k.name, out var v) ? v : int.MaxValue).ThenBy(k => k.GetSiblingIndex()).ToList();
            for (int i = 0; i < sorted.Count; i++) sorted[i].SetSiblingIndex(i);
        }

        // vành mây theo bốn mép bản đồ: mỗi đám một ảnh neo giữa lớp mây (CloudRing đặt anchoredPosition mỗi khung). Hình mây vẽ tay của
        // đảo vùng đất (land_thuy_may_1 / 2 xen kẽ, như sảnh và dải mây chuyến tàu; người dùng 2026-11-19: mây Nhà và mây đảo cùng loại),
        // không trong (alpha 1), không material. Cỡ cho đều mây sảnh trên màn (sảnh 340–440 đơn vị; Nhà zoom 0,56–1,25 nên rộng 380–540
        // px bản đồ), hai hàng so le cho kín rìa; hàng trong ở mép dưới chừa chỗ cuối bến tàu (mũi dưới) cho khỏi che cầu.
        static readonly string[] CloudArt = { "Assets/03 Art/Islands/land_thuy_may_1.png", "Assets/03 Art/Islands/land_thuy_may_2.png" };

        internal static Image[] BuildClouds(RectTransform layer, Vector2 size, float pierX) // đảo Casino dùng lại (CasinoSceneMenu)
        {
            var look = CloudArt.Select(AssetDatabase.LoadAssetAtPath<Sprite>).Where(s => s).ToArray();
            var list = new List<Image>();
            if (look.Length == 0)
            {
                Debug.LogWarning("[Nhà] Thiếu hình mây land_thuy_may_1/2: chưa có mây rìa.");
                return list.ToArray();
            }
            var rnd = new System.Random(7);
            float R(float lo, float hi) => lo + (float)rnd.NextDouble() * (hi - lo);
            var spots = new List<Vector2>();
            const float Step = 300;
            int nx = Mathf.CeilToInt(size.x / Step), ny = Mathf.CeilToInt(size.y / Step);
            float hx = size.x / nx / 2, hy = size.y / ny / 2;
            for (int i = 0; i <= nx; i++)
            {
                float x = i * size.x / nx;
                spots.Add(new Vector2(x, -20));
                spots.Add(new Vector2(x + hx, 120));
                spots.Add(new Vector2(x, size.y + 10));
                if (Mathf.Abs(x + hx - pierX) > 300) spots.Add(new Vector2(x + hx, size.y - 110));
            }
            for (int i = 1; i < ny; i++)
            {
                float y = i * size.y / ny;
                spots.Add(new Vector2(-30, y));
                spots.Add(new Vector2(110, y + hy));
                spots.Add(new Vector2(size.x + 30, y));
                spots.Add(new Vector2(size.x - 110, y + hy));
            }
            foreach (var p0 in spots)
            {
                var p = p0 + new Vector2(R(-40, 40), R(-30, 30));
                var sp = look[list.Count % look.Length];
                var img = Img(layer, "may_" + list.Count, sp, Color.white);
                img.material = null;
                float w = R(380, 540);
                var rt = img.rectTransform;
                rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(w, w * sp.rect.height / sp.rect.width);
                rt.localScale = new Vector3(rnd.Next(2) == 0 ? 1 : -1, 1, 1);
                rt.anchoredPosition = new Vector2(p.x - size.x / 2, size.y / 2 - p.y);
                list.Add(img);
            }
            return list.ToArray();
        }

        // lớp giao diện nha_ui: kiểu Clash of Critters (vòng nút, hàng nút icon, tấm xây có tab), dựng ở HomeCrittersMenu (2026-11-22)
        static void BuildUi(UiAssets assets, HomeScene scene, RectTransform safe) => HomeCrittersMenu.BuildUi(assets, scene, safe);

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
            // giữ bản lưu của người dùng (người dùng tự thử Nhà): xong tour trả lại Nhà, cấp, tướng đã có
            var keepHome = s.home;
            int keepLevel = s.level;
            var keepOwned = App.Data.Heroes.Take(6).Select(h => (h.id, s.Hero(h.id).owned)).ToList();
            foreach (var h in App.Data.Heroes.Take(6)) s.Hero(h.id).owned = true; // đủ 3 tướng để mở Nhà
            s.home = null; // bản lưu thử: dựng lại Nhà theo số liệu hiện tại (khoảnh đầu, đường đất)
            if (s.home == null && s.level < 10) s.level = 10;
            App.Router.Go(SceneIds.Home);
            // từ sảnh sang Nhà đi bằng chuyến tàu qua mây (vài giây): chờ màn Nhà thành màn hiện tại rồi chờ tàu cập bến
            HomeScene home = null;
            for (float t = 0; t < 25 && !(home && App.Router.CurrentRoot == home); t += 0.25f)
            {
                yield return new WaitForSecondsRealtime(0.25f);
                home = Object.FindFirstObjectByType<HomeScene>();
            }
            for (float t = 0; t < 10 && PierShip.Active && PierShip.Active.Busy; t += 0.25f) yield return new WaitForSecondsRealtime(0.25f);
            yield return new WaitForSecondsRealtime(2.5f);
            if (!home) Debug.LogWarning("[Nhà] Tour: không vào được màn Nhà");
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
                yield return new WaitForSecondsRealtime(0.25f);
                Shot("2a_luoi_lan"); // lưới đang lan ra từ giữa khung nhìn (GD_Claude/22 mốc A4)
                yield return new WaitForSecondsRealtime(0.55f);
                Shot("2_khay_xay");
                yield return new WaitForSecondsRealtime(1f);
                // dời công trình: ở chế độ xây chạm kho để nhấc lên, chạm đất thấp hơn 6 ô để đổi chỗ, chụp, rồi Đặt
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
                        if (lv) lv.Show((Vector2)cellTop.Invoke(home, new object[] { hb.gx + 1f, hb.gy + 6f }), 1f, 0); // máy cố định giữa chỗ cũ và chỗ mới
                        yield return new WaitForSecondsRealtime(0.3f);
                        onTap.Invoke(home, new object[] { cellTop.Invoke(home, new object[] { hb.gx + 2f, hb.gy + 2f }) });
                        yield return new WaitForSecondsRealtime(0.4f);
                        onTap.Invoke(home, new object[] { cellTop.Invoke(home, new object[] { hb.gx + 1.5f, hb.gy + 8.5f }) });
                        yield return new WaitForSecondsRealtime(0.6f);
                        Shot("9_doi");
                        yield return null; // ảnh chụp ở cuối khung: chờ chụp xong rồi mới làm bước sau
                        yield return null;
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
                var cellAt = home.GetType().GetMethod("CellTop", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
                Vector2 At(float gx, float gy) => (Vector2)cellAt.Invoke(home, new object[] { gx, gy });
                var c0 = At(58, 60); // giữa khoảnh đầu, sát biển (thấy sóng)
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
                foreach (var (tx, ty, id) in new[] { (21, 27, "water"), (22, 27, "water"), (21, 28, "water"), (22, 28, "sand"), (23, 27, "sand"), (24, 28, "stone"), (24, 29, "stone") })
                    plog.Append($" {tx},{ty} {id}={Home.Paint(sv, App.Data, tx, ty, id)}");
                home.Refresh();
                plog.Append(" | công trình:");
                foreach (var b in sv.home.buildings) plog.Append($" {b.def}@{b.gx},{b.gy}");
                Debug.Log(plog.ToString());
                if (view) view.Show(At(45, 56), 1.25f, 0);
                yield return new WaitForSecondsRealtime(0.8f);
                Shot("7_o_lat");
                yield return new WaitForSecondsRealtime(0.5f);
                // sóng vỗ bờ: hai ảnh cùng góc máy cách 1,2 giây (bờ biển phải bến)
                if (view) view.Show(At(70, 62), 1f, 0);
                yield return new WaitForSecondsRealtime(0.8f);
                Shot("8_song_a");
                yield return new WaitForSecondsRealtime(1.2f);
                Shot("8_song_b");
                yield return new WaitForSecondsRealtime(0.5f);
                // quái: chụp quái dạo quanh làng; thả một con vào xưởng gỗ (giao việc); mở hộp chọn tướng của ruộng
                {
                    const System.Reflection.BindingFlags F = System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance;
                    var t = home.GetType();
                    var main = App.Save.Data.home.buildings.Find(x => x.def == "main");
                    if (view && main != null) view.Show(At(main.gx + 6, main.gy + 8), 1f, 0);
                    yield return new WaitForSecondsRealtime(2.5f);
                    Shot("11_quai_dao");
                    yield return null;
                    yield return null;
                    var petDict = t.GetField("pets", F)?.GetValue(home) as System.Collections.Generic.Dictionary<string, FarmPet>;
                    var toLocal = t.GetMethod("ToLocal", F);
                    var saw = App.Save.Data.home.buildings.Find(x => x.def == "sawmill");
                    var roam = petDict?.Values.FirstOrDefault(p => p.State == FarmPet.Mode.Roam || p.State == FarmPet.Mode.Walk);
                    Debug.Log($"[Nhà] Quái trên bản đồ: {petDict?.Count ?? -1} con, dạo {petDict?.Values.Count(p => p.Spot < 0 && p.State != FarmPet.Mode.Sleep) ?? -1}");
                    if (roam && saw != null && toLocal != null)
                    {
                        bool ok = home.PetDropped(roam, (Vector2)toLocal.Invoke(home, new object[] { At(saw.gx + 2, saw.gy + 2) }));
                        Debug.Log($"[Nhà] Thả {roam.Hero} vào xưởng gỗ: {(ok ? "được" : "KHÔNG được")}, ô 1 = {saw.slots[0].hero}");
                        if (view) view.Show(At(saw.gx + 2, saw.gy + 4), 1f, 0);
                        yield return new WaitForSecondsRealtime(1.5f);
                        Shot("12_tha_quai");
                        yield return null;
                        yield return null;
                    }
                    var field = App.Save.Data.home.buildings.Find(x => x.def == "field");
                    var picker = t.GetMethod("Picker", F);
                    if (picker != null && field != null)
                    {
                        picker.Invoke(home, new object[] { field.id, 0 });
                        yield return new WaitForSecondsRealtime(0.8f);
                        Shot("13_chon_tuong");
                        yield return null;
                        yield return null;
                        App.Modals.CloseAll();
                        yield return new WaitForSecondsRealtime(0.3f);
                    }
                }
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
                        yield return null; // ảnh chụp ở cuối khung: chờ chụp xong rồi mới làm bước sau
                        yield return null;
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pe, UnityEngine.EventSystems.ExecuteEvents.pointerUpHandler);
                        UnityEngine.EventSystems.ExecuteEvents.Execute(tapC.gameObject, pe, UnityEngine.EventSystems.ExecuteEvents.endDragHandler);
                        yield return new WaitForSecondsRealtime(0.4f);
                        Shot("10_tha");
                        yield return null; // ảnh chụp ở cuối khung: chờ chụp xong rồi mới làm bước sau
                        yield return null;
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
                // đêm: mặt nạ tự sáng cửa sổ Nhà chính, không quầng (GD_Claude/22 mốc A3); biển đêm ven bến
                {
                    var lv = so.FindProperty("landView").objectReferenceValue as LandView;
                    var ct = home.GetType().GetMethod("CellTop", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
                    var mainB = Home.Main(App.Save.Data.home);
                    if (lv && ct != null && mainB != null)
                    {
                        // bộ mảnh A5 ban trưa: vách cao nguyên cạnh trên phải, thác nước chảy (hai ảnh cách 0,6 giây). Bản lưu thử: mở hết ô
                        // rừng cho cây khỏi che (cuối tour trả bản lưu thật)
                        var hs = App.Save.Data.home;
                        int nl = Home.LotsPerSide(App.Data.Cfg.home);
                        for (int lot = 0; lot < nl * nl; lot++)
                            if (!hs.lots.Contains(lot)) hs.lots.Add(lot);
                        home.Refresh();
                        DayCycle.Override = 12f;
                        lv.Show((Vector2)ct.Invoke(home, new object[] { 40f, 4f }), 0.8f, 0);
                        yield return new WaitForSecondsRealtime(0.8f);
                        Shot("16_vach");
                        yield return new WaitForSecondsRealtime(0.4f);
                        var fallAt = new Vector2(3555, 760); // thác vẽ trên ảnh nền (px bản đồ)
                        lv.Show(fallAt, 1.25f, 0);
                        yield return new WaitForSecondsRealtime(0.8f);
                        Shot("17_thac_a");
                        yield return new WaitForSecondsRealtime(0.6f);
                        Shot("17_thac_b");
                        yield return new WaitForSecondsRealtime(0.4f);
                        DayCycle.Override = 21f;
                        lv.Show((Vector2)ct.Invoke(home, new object[] { mainB.gx + 3f, mainB.gy + 3f }), 1.25f, 0);
                        yield return new WaitForSecondsRealtime(1.2f);
                        Shot("14_dem_nha");
                        yield return new WaitForSecondsRealtime(0.4f);
                        lv.Show((Vector2)ct.Invoke(home, new object[] { 66f, 66f }), 1f, 0);
                        yield return new WaitForSecondsRealtime(0.8f);
                        Shot("15_dem_bien");
                        yield return new WaitForSecondsRealtime(0.4f);
                    }
                }
                DayCycle.Override = null;
            }
            s.home = keepHome;
            s.level = keepLevel;
            foreach (var (id, owned) in keepOwned) s.Hero(id).owned = owned;
            App.Save.Save();
            Debug.Log("[Thử] Xong Nhà (đã trả bản lưu)");
            tourStart = 0;
            EditorApplication.isPlaying = false;
        }
    }
}
