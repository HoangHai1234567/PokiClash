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

        // thử tia năng lượng kiểu Water Laser (2026-11-25, HatTiaLaser.ELaser): Lộc Phong (mana, lục ngọc), Giác Mộc (mana + chiêu cuối, hổ phách),
        // Thổ Tinh (tia nhiệt trong chiêu cuối); ảnh ở Temp/PokiShots/thuy_fx
        [MenuItem("PokiClash/Thử/Tướng/tia năng lượng kiểu Water Laser (Lộc Phong, Giác Mộc, Thổ Tinh) (đang Play)", priority = 130)]
        static void ThuTiaNl() => ThuyFxTour.TryOnly("bom_la", "moc_tinh", "giap_nham");

        // như trên nhưng sân chạy chậm 0,4× (soi từng pha tia: tụ, phóng, phình, dội, tắt; tia nhiệt Thổ Tinh chỉ ~0,3 s)
        [MenuItem("PokiClash/Thử/Tướng/tia năng lượng kiểu Water Laser, chạy chậm 0,4× (đang Play)", priority = 131)]
        static void ThuTiaNlCham() => ThuyFxTour.TryOnlyCham(0.4f, "bom_la", "moc_tinh", "giap_nham");

        // như trên trong hộp chi tiết tướng (ô xem, đích ảo trước mặt): Chiêu rồi Mana
        [MenuItem("PokiClash/Thử/Tướng/tia năng lượng kiểu Water Laser trong hộp chi tiết tướng (đang Play)", priority = 132)]
        static void ThuTiaNlXem() => ThuyFxTour.TryViewerOnly("bom_la", "moc_tinh", "giap_nham");

        // riêng chiêu cuối Thổ Tinh (Mặt Trời thẳng trên vỏ đá + tia nhiệt), tốc thường rồi chậm 0,4×
        [MenuItem("PokiClash/Thử/Tướng/Thổ Tinh: chiêu cuối Mặt Trời + tia nhiệt (đang Play)", priority = 134)]
        static void ThuThoTinh() => ThuyFxTour.TryOnly("giap_nham");

        [MenuItem("PokiClash/Thử/Tướng/Thổ Tinh: chiêu cuối Mặt Trời + tia nhiệt, chạy chậm 0,4× (đang Play)", priority = 135)]
        static void ThuThoTinhCham() => ThuyFxTour.TryOnlyCham(0.4f, "giap_nham");

        // chiêu nước mới theo gói mẫu (2026-11-25, HatNuocChieu.cs): các tướng Thủy đã đổi chiêu; tốc thường và chậm 0,4×
        static readonly string[] ChieuMoi = { "ti_tach", "thach_giai", "ca_den", "giong_bao", "lien_kinh", "uyen_xa", "han_ngac", "hai_long" };

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/chiêu nước mới (đạn, bong bóng, bom, mưa, lốc...) (đang Play)", priority = 136)]
        static void ThuChieuMoi() => ThuyFxTour.TryOnly(ChieuMoi);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/chiêu nước mới, chạy chậm 0,4× (đang Play)", priority = 137)]
        static void ThuChieuMoiCham() => ThuyFxTour.TryOnlyCham(0.4f, ChieuMoi);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/chiêu nước mới trong hộp chi tiết tướng (đang Play)", priority = 139)]
        static void ThuChieuMoiXem() => ThuyFxTour.TryViewerOnly(ChieuMoi);

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/chiêu nước mới: Uyên Xà + Hàn Ngạc (đang Play)", priority = 138)]
        static void ThuChieuMoiUxHn() => ThuyFxTour.TryOnly("uyen_xa", "han_ngac");

        // Play từ cảnh Boot mà KHÔNG đóng / đổi cảnh đang mở (2026-11-25: người dùng mở cảnh demo của gói để xem mẫu, có thay đổi chưa lưu; Play
        // thường chạy cảnh demo nên tour thử không có App). Đặt tạm EditorSceneManager.playModeStartScene = Boot rồi vào Play; về Edit Mode thì
        // trả lại null (cờ SessionState + đăng ký lại sau mỗi lần nạp lại script, vì vào Play có thể nạp lại domain)
        const string BootPath = "Assets/00 Scenes/Boot.unity", CoBoot = "PokiClash.PlayTuBoot";

        [MenuItem("PokiClash/Thử/Play từ cảnh Boot (giữ cảnh đang mở)", priority = 142)]
        public static void PlayTuBoot()
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode) return;
            var boot = AssetDatabase.LoadAssetAtPath<SceneAsset>(BootPath);
            if (!boot)
            {
                Debug.LogError("[Play từ Boot] Không thấy " + BootPath);
                return;
            }
            UnityEditor.SceneManagement.EditorSceneManager.playModeStartScene = boot;
            SessionState.SetBool(CoBoot, true);
            EditorApplication.isPlaying = true;
        }

        [InitializeOnLoadMethod]
        static void DangKyTraLai()
        {
            EditorApplication.playModeStateChanged -= TraLai;
            EditorApplication.playModeStateChanged += TraLai;
        }

        static void TraLai(PlayModeStateChange s)
        {
            if (s != PlayModeStateChange.EnteredEditMode || !SessionState.GetBool(CoBoot, false)) return;
            UnityEditor.SceneManagement.EditorSceneManager.playModeStartScene = null;
            SessionState.SetBool(CoBoot, false);
        }

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/Thôn Kình: cầu ma thủy (đang Play)", priority = 140)]
        static void ThuCauMa() => ThuyFxTour.TryOnly("lien_kinh");

        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/Thôn Kình: cầu ma thủy, chạy chậm 0,4× (đang Play)", priority = 141)]
        static void ThuCauMaCham() => ThuyFxTour.TryOnlyCham(0.4f, "lien_kinh");

        // cầu ma đổi màu cho hệ khác (2026-11-25): Gạc Đá, Lộc Phong (lục, chiêu cuối), Hỏa Quy (đỏ cam, chiêu cuối)
        [MenuItem("PokiClash/Thử/Tướng/Cầu ma đổi màu: Gạc Đá, Lộc Phong, Hỏa Quy (đang Play)", priority = 142)]
        static void ThuCauMaHe() => ThuyFxTour.TryOnly("gac_da", "bom_la", "nguu_quyen");

        [MenuItem("PokiClash/Thử/Tướng/Cầu ma đổi màu: Gạc Đá, Lộc Phong, Hỏa Quy, chạy chậm 0,4× (đang Play)", priority = 143)]
        static void ThuCauMaHeCham() => ThuyFxTour.TryOnlyCham(0.4f, "gac_da", "bom_la", "nguu_quyen");

        // riêng Hỏa Quy (cầu ma màu lửa): trận chạy chậm + hộp chi tiết tướng
        [MenuItem("PokiClash/Thử/Tướng/Cầu ma đổi màu: Hỏa Quy, chạy chậm 0,4× (đang Play)", priority = 146)]
        static void ThuCauMaRuaCham() => ThuyFxTour.TryOnlyCham(0.4f, "nguu_quyen");

        [MenuItem("PokiClash/Thử/Tướng/Cầu ma đổi màu: Hỏa Quy, hộp chi tiết tướng (đang Play)", priority = 147)]
        static void ThuCauMaRuaXem() => ThuyFxTour.TryViewerOnly("nguu_quyen");

        // chém lửa Viêm Đao, tia lửa năng lượng Tiểu Quỷ Lava / Hỏa Nhãn (2026-11-25)
        [MenuItem("PokiClash/Thử/Tướng/Chiêu đổi màu Hỏa: Viêm Đao, Tiểu Quỷ Lava, Hỏa Nhãn (đang Play)", priority = 144)]
        static void ThuHoaDoiMau() => ThuyFxTour.TryOnly("giap_long", "su_tu_lua", "hoa_nhan");

        [MenuItem("PokiClash/Thử/Tướng/Chiêu đổi màu Hỏa: Viêm Đao, Tiểu Quỷ Lava, Hỏa Nhãn (+ Hỏa Quy), chạy chậm 0,4× (đang Play)", priority = 145)]
        static void ThuHoaDoiMauCham() => ThuyFxTour.TryOnlyCham(0.4f, "giap_long", "su_tu_lua", "hoa_nhan", "nguu_quyen");

        // soát tia nước bảng 0 sau khi shader có bảng màu (Giông Bão, chiêu mana)
        [MenuItem("PokiClash/Thử/Tướng/Đảo Thủy/nước shader: soát tia Water Laser Giông Bão (đang Play)", priority = 133)]
        static void ThuTiaGb() => ThuyFxTour.TryOnly("giong_bao");

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
