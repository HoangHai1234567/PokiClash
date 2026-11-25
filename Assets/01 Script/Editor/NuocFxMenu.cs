// Đặt sẵn HIỆU ỨNG NƯỚC BẰNG SHADER vào prefab (người dùng 2026-11-24 chọn "c": toàn bộ bộ nước trong trận chạy bằng shader).
// - Nhập texture Assets/03 Art/Fx/Nuoc (ArtGen/Spine/nuoc_shader/tao_texture.py): nuoc_nhieu dữ liệu tuyến tính lặp, nuoc_matna một kênh.
// - Tạo material Assets/03 Art/Fx/Nuoc/UIWaterFx.mat (shader PokiClash/UIWaterFx, _MaskTex = atlas mặt nạ).
// - Mỗi lớp hạt (HatDat, HatSau, HatTruoc) của Screens/Battle và Dialogs/ChiTietTuong có con "NuocFx" (HatNuocFx) ngay sau "Mang";
//   Canvas chứa lớp hạt bật kênh TexCoord1 + TexCoord2 (tham số hình đi theo đỉnh). Chạy lại không tạo trùng.
// Chạy sau menu "Sàn đấu: hạt lửa (bộ Hỏa)" / "Hộp chi tiết tướng: hạt lửa" (cần lớp hạt có sẵn).
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class NuocFxMenu
    {
        const string Dir = "Assets/03 Art/Fx/Nuoc";
        const string NoisePath = Dir + "/nuoc_nhieu.png", MaskPath = Dir + "/nuoc_matna.png", MatPath = Dir + "/UIWaterFx.mat";
        // bản 3 (2026-11-25, gói mẫu SrRubfish + NamuFX): atlas flipbook giá trị + alpha và texture vân lặp (ArtGen/Spine/nuoc_goi/dong_goi.py)
        const string FbPath = Dir + "/nuoc_fb.png", VetPath = Dir + "/nuoc_vet.png";
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab", DetailPath = "Assets/04 Prefabs/Dialogs/ChiTietTuong.prefab";

        [MenuItem("PokiClash/Prefab/Trận/Sàn đấu: nước shader (bộ Thủy)", priority = 65)]
        public static void Build()
        {
            var noise = Tex(NoisePath, false);
            var mask = Tex(MaskPath, true);
            if (!noise || !mask)
            {
                Debug.LogError($"[Nước shader] Thiếu {NoisePath} hoặc {MaskPath} (chạy py -3 -I ArtGen/Spine/nuoc_shader/tao_texture.py).");
                return;
            }
            var mat = Mat(mask);
            if (!mat) return;
            int n = 0;
            n += Wire(BattlePath, root =>
            {
                var st = root.GetComponentInChildren<StageView>(true);
                if (!st) return null;
                var so = new SerializedObject(st);
                return new[] { so.FindProperty("hatFloor").objectReferenceValue as RectTransform, so.FindProperty("hatBack").objectReferenceValue as RectTransform,
                    so.FindProperty("hatFront").objectReferenceValue as RectTransform };
            }, mat, noise);
            n += Wire(DetailPath, root =>
            {
                var hv = root.GetComponentInChildren<HeroViewer>(true);
                if (!hv) return null;
                var so = new SerializedObject(hv);
                return new[] { so.FindProperty("hatFloor").objectReferenceValue as RectTransform, so.FindProperty("hatBack").objectReferenceValue as RectTransform,
                    so.FindProperty("hatFront").objectReferenceValue as RectTransform };
            }, mat, noise);
            Debug.Log($"[Nước shader] Đã đặt NuocFx vào {n} lớp hạt (Battle + ChiTietTuong), material {MatPath}.");
        }

        // thử nhanh trong trận: 3 tướng Thủy đủ tia / cầu / thương / toé (Thạch Giải, Giông Bão, Tí Tách), ảnh ở Temp/PokiShots/thuy_fx
        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/nước shader: 4 tướng tia, cầu, thương, toé, sóng, mạch phun (đang Play)", priority = 128)]
        static void Thu3() => ThuyFxTour.TryOnly("thach_giai", "giong_bao", "ti_tach", "hai_long", "han_ngac"); // + Hàn Ngạc: sóng / mưa

        // thử riêng tia nước kiểu Water Laser (bản 3, HatNuocGoi.NLaser): các tướng có tia mana
        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/nước shader: tia Water Laser (Giông Bão, Tí Tách, Hải Đăng, Uyên Xà) (đang Play)", priority = 129)]
        static void ThuTia() => ThuyFxTour.TryOnly("giong_bao", "ti_tach", "ca_den", "uyen_xa");

        static Texture2D Tex(string path, bool single)
        {
            var imp = AssetImporter.GetAtPath(path) as TextureImporter;
            if (!imp) return null;
            var want = single ? TextureImporterType.SingleChannel : TextureImporterType.Default;
            var alpha = single ? TextureImporterAlphaSource.None : TextureImporterAlphaSource.FromInput; // A của nhiễu = vân chì vẽ tay
            if (imp.textureType != want || imp.sRGBTexture || imp.textureCompression != TextureImporterCompression.Uncompressed || imp.alphaSource != alpha
                || imp.wrapMode != (single ? TextureWrapMode.Clamp : TextureWrapMode.Repeat) || imp.mipmapEnabled != !single)
            {
                imp.textureType = want;
                if (single)
                {
                    var ts = new TextureImporterSettings();
                    imp.ReadTextureSettings(ts);
                    ts.singleChannelComponent = TextureImporterSingleChannelComponent.Red;
                    imp.SetTextureSettings(ts);
                }
                imp.sRGBTexture = false;
                imp.alphaSource = alpha;
                imp.textureCompression = TextureImporterCompression.Uncompressed;
                imp.wrapMode = single ? TextureWrapMode.Clamp : TextureWrapMode.Repeat;
                imp.filterMode = FilterMode.Bilinear;
                imp.mipmapEnabled = !single;
                imp.npotScale = TextureImporterNPOTScale.None;
                imp.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Texture2D>(path);
        }

        // chỉ nạp lại texture + material (không sửa prefab): sau khi chạy lại dong_goi.py
        [MenuItem("PokiClash/Prefab/Trận/Nước shader: nạp atlas flipbook gói mẫu (không sửa prefab)", priority = 66)]
        public static void NapAtlas()
        {
            var mask = Tex(MaskPath, true);
            var mat = mask ? Mat(mask) : null;
            Debug.Log(mat ? $"[Nước shader] Đã nạp {FbPath}, {VetPath} vào {MatPath}." : "[Nước shader] Thiếu mặt nạ / shader.");
        }

        // dữ liệu tuyến tính: atlas flipbook (không lặp, không mip, ô sát nhau) / vân lặp (lặp, có mip); Android nén ASTC 4x4
        static Texture2D DataTex(string path, bool repeat)
        {
            var imp = AssetImporter.GetAtPath(path) as TextureImporter;
            if (!imp) return null;
            var wrap = repeat ? TextureWrapMode.Repeat : TextureWrapMode.Clamp;
            var and = imp.GetPlatformTextureSettings("Android");
            if (imp.textureType != TextureImporterType.Default || imp.sRGBTexture || imp.wrapMode != wrap || imp.mipmapEnabled != repeat
                || imp.alphaSource != TextureImporterAlphaSource.FromInput || imp.alphaIsTransparency || !and.overridden || and.format != TextureImporterFormat.ASTC_4x4)
            {
                imp.textureType = TextureImporterType.Default;
                imp.sRGBTexture = false;
                imp.alphaSource = TextureImporterAlphaSource.FromInput;
                imp.alphaIsTransparency = false;
                imp.wrapMode = wrap;
                imp.filterMode = FilterMode.Bilinear;
                imp.mipmapEnabled = repeat;
                imp.npotScale = TextureImporterNPOTScale.None;
                imp.maxTextureSize = 2048;
                imp.textureCompression = TextureImporterCompression.Uncompressed;
                and.overridden = true;
                and.maxTextureSize = 2048;
                and.format = TextureImporterFormat.ASTC_4x4;
                imp.SetPlatformTextureSettings(and);
                imp.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Texture2D>(path);
        }

        static Material Mat(Texture2D mask)
        {
            var sh = Shader.Find("PokiClash/UIWaterFx");
            if (!sh)
            {
                Debug.LogError("[Nước shader] Chưa có shader PokiClash/UIWaterFx (Assets/03 Art/Shaders/UIWaterFx.shader).");
                return null;
            }
            var mat = AssetDatabase.LoadAssetAtPath<Material>(MatPath);
            if (!mat)
            {
                mat = new Material(sh) { name = "UIWaterFx" };
                AssetDatabase.CreateAsset(mat, MatPath);
            }
            mat.shader = sh;
            mat.SetTexture("_MaskTex", mask);
            var fb = DataTex(FbPath, false);
            var vet = DataTex(VetPath, true);
            if (fb) mat.SetTexture("_FbTex", fb);
            if (vet) mat.SetTexture("_VetTex", vet);
            mat.SetVector("_FbStops", new Vector4(0.2f, 0.42f, 0.74f, 0));
            // bản 2 (nổi khối + vân chì): đặt lại số đã lưu trong material về số chốt của shader
            mat.SetFloat("_VolK", 0.14f);
            mat.SetVector("_Stops", new Vector4(0.36f, 0.66f, 0, 0));
            mat.SetFloat("_Rim", 0.84f);
            EditorUtility.SetDirty(mat);
            AssetDatabase.SaveAssets();
            return mat;
        }

        static int Wire(string path, System.Func<GameObject, RectTransform[]> layers, Material mat, Texture2D noise)
        {
            var root = PrefabUtility.LoadPrefabContents(path);
            int n = 0;
            try
            {
                var ls = layers(root);
                if (ls == null)
                {
                    Debug.LogError($"[Nước shader] {path}: không thấy StageView / HeroViewer.");
                    return 0;
                }
                foreach (var layer in ls)
                {
                    if (!layer) continue;
                    var t = layer.Find("NuocFx") as RectTransform;
                    if (!t)
                    {
                        var go = new GameObject("NuocFx", typeof(RectTransform), typeof(CanvasRenderer), typeof(HatNuocFx));
                        t = (RectTransform)go.transform;
                        t.SetParent(layer, false);
                    }
                    t.anchorMin = t.anchorMax = new Vector2(0, 1);
                    t.pivot = new Vector2(0.5f, 0.5f);
                    t.anchoredPosition = Vector2.zero;
                    t.sizeDelta = new Vector2(8000, 8000);
                    t.localScale = Vector3.one;
                    t.localRotation = Quaternion.identity;
                    var mang = layer.Find("Mang");
                    t.SetSiblingIndex(mang ? mang.GetSiblingIndex() + 1 : 0);
                    var fx = t.GetComponent<HatNuocFx>();
                    fx.raycastTarget = false;
                    fx.material = mat;
                    var so = new SerializedObject(fx);
                    so.FindProperty("noise").objectReferenceValue = noise;
                    so.ApplyModifiedPropertiesWithoutUndo();
                    var cv = layer.GetComponentInParent<Canvas>(true);
                    if (cv) cv.additionalShaderChannels |= AdditionalCanvasShaderChannels.TexCoord1 | AdditionalCanvasShaderChannels.TexCoord2;
                    n++;
                }
                PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            return n;
        }
    }
}
