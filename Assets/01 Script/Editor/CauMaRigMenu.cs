// Dựng CẦU MA THỦY bằng PREFAB GỐC của gói (2026-11-25; người dùng: "làm theo hướng A, dùng thẳng prefab của gói, nhưng nên sửa lại 1 chút để nó
// có chất vẽ tay hơn"). Chạy lại không tạo trùng:
//  - RenderTexture Assets/03 Art/Fx/CauMa/cau_ma_rt (512², sRGB, xoá trong suốt) + material UIVeTayRT (shader PokiClash/UIVeTayRT, vân chì
//    nuoc_nhieu);
//  - prefab Assets/04 Prefabs/Fx/CauMaRig: camera phối cảnh FOV 30 nhìn chếch xuống 18° (như camera demo của gói), cách 15 đơn vị (khung ~8 đơn
//    vị: vỏ cầu 2,1 + vệt bay vòng + hạt toả), xoá (0,0,0,0) vào cau_ma_rt, tắt sẵn; hệ hạt FX_PF_MagicWater_OrbLoop lồng prefab, BỎ quầng tối
//    Glow / Mask / 'Mask (đĩa đen khổng lồ phủ sân sáng), ShockWave (shader khúc xạ cần ảnh màn hình, không chạy trên RenderTexture) và
//    RadialImpact (ảnh FX_TX_RadialBurst_03.psd không có kênh alpha: cả tấm hạt có độ hiện → ô vuông xám lúc cầu bừng), mọi hệ
//    không tự chạy (HatLua đẩy theo đồng hồ sân);
//  - lớp hạt TRƯỚC (hatFront) của Screens/Battle và Dialogs/ChiTietTuong: con "CauMaRT" (RawImage + CauMaHien) ngay sau "NuocFx", neo góc trên
//    trái như NuocFx, tắt sẵn.
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class CauMaRigMenu
    {
        const string Dir = "Assets/03 Art/Fx/CauMa";
        const string RtPath = Dir + "/cau_ma_rt.renderTexture", MatPath = Dir + "/UIVeTayRT.mat";
        const string NoisePath = "Assets/03 Art/Fx/Nuoc/nuoc_nhieu.png";
        const string OrbPath = "Assets/SrRubfish_VFX_02/Prefabs/FX_PF_MagicWater_OrbLoop.prefab";
        const string RigPath = "Assets/04 Prefabs/Fx/CauMaRig.prefab";
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab", DetailPath = "Assets/04 Prefabs/Dialogs/ChiTietTuong.prefab";
        public const float CamD = 15, CamPitch = 18, CamFov = 30;

        [MenuItem("PokiClash/Prefab/Trận/Cầu ma thủy: dựng rig prefab gốc + gắn vào sân", priority = 67)]
        public static void Build()
        {
            var orb = AssetDatabase.LoadAssetAtPath<GameObject>(OrbPath);
            var shader = Shader.Find("PokiClash/UIVeTayRT");
            if (!orb || !shader)
            {
                Debug.LogError($"[Cầu ma thủy] Thiếu {OrbPath} hoặc shader PokiClash/UIVeTayRT.");
                return;
            }
            if (!AssetDatabase.IsValidFolder(Dir)) AssetDatabase.CreateFolder("Assets/03 Art/Fx", "CauMa");
            if (!AssetDatabase.IsValidFolder("Assets/04 Prefabs/Fx")) AssetDatabase.CreateFolder("Assets/04 Prefabs", "Fx");

            var rt = AssetDatabase.LoadAssetAtPath<RenderTexture>(RtPath);
            if (!rt)
            {
                rt = new RenderTexture(512, 512, 16, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB)
                    { name = "cau_ma_rt", antiAliasing = 1, useMipMap = false, wrapMode = TextureWrapMode.Clamp, filterMode = FilterMode.Bilinear };
                AssetDatabase.CreateAsset(rt, RtPath);
            }

            var mat = AssetDatabase.LoadAssetAtPath<Material>(MatPath);
            if (!mat)
            {
                mat = new Material(shader) { name = "UIVeTayRT" };
                AssetDatabase.CreateAsset(mat, MatPath);
            }
            mat.shader = shader;
            var noise = AssetDatabase.LoadAssetAtPath<Texture2D>(NoisePath);
            if (noise) mat.SetTexture("_NoiseTex", noise);
            // số chỉnh sau lần chụp đầu (vỏ xoáy thành mảng đặc che đối thủ, mép lấm tấm): giữ màu / độ trong gốc nhiều hơn, run mịn nhẹ
            mat.SetFloat("_GiuGoc", 0.55f);
            mat.SetFloat("_Phang", 0.45f);
            mat.SetFloat("_Run", 0.05f);
            mat.SetFloat("_RunCo", 260);
            mat.SetFloat("_AlphaLo", 0.08f);
            mat.SetFloat("_AlphaHi", 0.5f);
            mat.SetFloat("_AlphaMid", 0.45f);
            mat.SetFloat("_AlphaMax", 0.85f);
            mat.SetFloat("_Hatch", 0.35f);
            EditorUtility.SetDirty(mat);
            // material theo hệ (2026-11-25, người dùng chọn làm cầu ma đổi màu cho Mộc và Hỏa): chép từ bản nước rồi đổi 4 dải, quầng, xoay sắc gốc
            var moc = MatHe("Moc", mat, new Color(0.094f, 0.43f, 0.29f), new Color(0.184f, 0.718f, 0.478f), new Color(0.624f, 0.89f, 0.416f),
                new Color(0.933f, 0.984f, 0.69f), new Color(0.8f, 1f, 0.55f), -50, 0.9f, 1.3f, 0.55f, 0.85f);
            // lửa: đỏ cam đậm, gần như chỉ dải phẳng (giữ 10 % sắc gốc) và đặc (độ hiện dồn bậc 90 %, trần 1). Bản đầu (giữ 35 %, trần 0,95) bị
            // người dùng chê "cầu con này nhìn hơi yếu": vỏ xoáy nhợt màu đào gần trong suốt, lõi trắng
            var hoa = MatHe("Hoa", mat, new Color(0.62f, 0.08f, 0.06f), new Color(0.9f, 0.24f, 0.05f), new Color(1f, 0.52f, 0.08f),
                new Color(1f, 0.84f, 0.36f), new Color(1f, 0.55f, 0.12f), -168, 0.9f, 2f, 0.1f, 1f);
            hoa.SetFloat("_Phang", 0.9f);
            hoa.SetFloat("_AlphaMid", 0.85f);
            hoa.SetFloat("_AlphaLo", 0.05f);
            hoa.SetFloat("_AlphaHi", 0.4f);
            hoa.SetFloat("_Quang", 1.4f);
            var mats = new[] { mat, moc, hoa };

            // ---- prefab rig
            var root = new GameObject("CauMaRig");
            try
            {
                var rig = root.AddComponent<CauMaRig>();
                var camGo = new GameObject("Cam");
                camGo.transform.SetParent(root.transform, false);
                float p = CamPitch * Mathf.Deg2Rad;
                camGo.transform.localPosition = new Vector3(0, CamD * Mathf.Sin(p), -CamD * Mathf.Cos(p));
                camGo.transform.localRotation = Quaternion.Euler(CamPitch, 0, 0);
                var cam = camGo.AddComponent<Camera>();
                cam.clearFlags = CameraClearFlags.SolidColor;
                cam.backgroundColor = new Color(0, 0, 0, 0);
                cam.fieldOfView = CamFov;
                cam.nearClipPlane = 1;
                cam.farClipPlane = 60;
                cam.targetTexture = rt;
                cam.allowHDR = false;
                cam.allowMSAA = false;
                cam.depth = -50;
                cam.enabled = false;

                var o = (GameObject)PrefabUtility.InstantiatePrefab(orb);
                o.transform.SetParent(root.transform, false);
                o.transform.localPosition = Vector3.zero;
                o.transform.localRotation = Quaternion.identity;
                int tat = 0;
                foreach (var t in o.GetComponentsInChildren<Transform>(true))
                {
                    string n = t.name.Trim('\'', ' ');
                    if (t == o.transform) continue;
                    if (n == "Glow" || n == "Mask" || n.StartsWith("ShockWave") || n == "RadialImpact")
                    {
                        t.gameObject.SetActive(false);
                        tat++;
                    }
                }
                foreach (var ps in o.GetComponentsInChildren<ParticleSystem>(true))
                {
                    var m = ps.main;
                    m.playOnAwake = false;
                }
                var goc = o.GetComponent<ParticleSystem>();
                if (!goc) goc = o.GetComponentInChildren<ParticleSystem>(true);
                rig.Setup(cam, goc);
                PrefabUtility.SaveAsPrefabAsset(root, RigPath);
                Debug.Log($"[Cầu ma thủy] Rig {RigPath}: tắt {tat} lớp (quầng tối, sóng chấn khúc xạ).");
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
            var rigAsset = AssetDatabase.LoadAssetAtPath<GameObject>(RigPath).GetComponent<CauMaRig>();

            int dem = 0;
            dem += Wire(BattlePath, r =>
            {
                var st = r.GetComponentInChildren<StageView>(true);
                return st ? new SerializedObject(st).FindProperty("hatFront").objectReferenceValue as RectTransform : null;
            }, mat, rt, rigAsset, mats);
            dem += Wire(DetailPath, r =>
            {
                var hv = r.GetComponentInChildren<HeroViewer>(true);
                return hv ? new SerializedObject(hv).FindProperty("hatFront").objectReferenceValue as RectTransform : null;
            }, mat, rt, rigAsset, mats);
            AssetDatabase.SaveAssets();
            Debug.Log($"[Cầu ma thủy] Đã gắn CauMaRT vào {dem} lớp hạt trước (Battle + ChiTietTuong).");
        }

        // chép material nước sang bản của hệ khác rồi đặt màu (giá trị sRGB như Inspector)
        static Material MatHe(string ten, Material goc, Color shade, Color deep, Color body, Color foam, Color quang, float doiSac, float sacSang,
            float damSac, float giuGoc, float alphaMax)
        {
            string p = $"{Dir}/UIVeTayRT_{ten}.mat";
            var m = AssetDatabase.LoadAssetAtPath<Material>(p);
            if (!m)
            {
                m = new Material(goc) { name = "UIVeTayRT_" + ten };
                AssetDatabase.CreateAsset(m, p);
            }
            else m.CopyPropertiesFromMaterial(goc);
            m.SetColor("_ColShade", shade);
            m.SetColor("_ColDeep", deep);
            m.SetColor("_ColBody", body);
            m.SetColor("_ColFoam", foam);
            m.SetColor("_ColQuang", quang);
            m.SetFloat("_DoiSac", doiSac);
            m.SetFloat("_SacSang", sacSang);
            m.SetFloat("_DamSac", damSac);
            m.SetFloat("_GiuGoc", giuGoc);
            m.SetFloat("_AlphaMax", alphaMax);
            EditorUtility.SetDirty(m);
            return m;
        }

        static int Wire(string path, System.Func<GameObject, RectTransform> layerOf, Material mat, RenderTexture rt, CauMaRig rigAsset, Material[] mats)
        {
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                var layer = layerOf(root);
                if (!layer)
                {
                    Debug.LogError($"[Cầu ma thủy] {path}: không thấy lớp hạt trước.");
                    return 0;
                }
                var t = layer.Find("CauMaRT") as RectTransform;
                if (!t)
                {
                    var go = new GameObject("CauMaRT", typeof(RectTransform), typeof(CanvasRenderer), typeof(RawImage), typeof(CauMaHien));
                    t = (RectTransform)go.transform;
                    t.SetParent(layer, false);
                }
                t.anchorMin = t.anchorMax = new Vector2(0, 1);
                t.pivot = new Vector2(0.5f, 0.5f);
                t.anchoredPosition = Vector2.zero;
                t.sizeDelta = new Vector2(400, 400);
                t.localScale = Vector3.one;
                t.localRotation = Quaternion.identity;
                var nuoc = layer.Find("NuocFx");
                t.SetSiblingIndex(nuoc ? nuoc.GetSiblingIndex() + 1 : 0);
                var img = t.GetComponent<RawImage>();
                img.texture = rt;
                img.material = mat;
                img.raycastTarget = false;
                img.enabled = false;
                t.GetComponent<CauMaHien>().Setup(img, rigAsset, mats);
                PrefabUtility.SaveAsPrefabAsset(root, path);
                return 1;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }
    }
}
