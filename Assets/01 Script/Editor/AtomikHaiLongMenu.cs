// Scene thử và ảnh khung của rig Hải Long Ngũ Đầu (.atomik bản 3: có mặt nạ cắt và sự kiện). Rig xuất bằng
// ArtGen/Spine/hai_long.py (chép sang Assets/05 Atomik Thu/hai_long.atomik). Scene dựng thêm rồi lưu, đóng: không đổi scene đang mở.
using System.IO;
using PokiClash.Game;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.SceneManagement;

namespace PokiClash.EditorTools
{
    public static class AtomikHaiLongMenu
    {
        const string Dir = "Assets/05 Atomik Thu";
        const string RigPath = Dir + "/hai_long.atomik";
        const string ScenePath = Dir + "/AtomikHaiLong.unity";
        static readonly Color Back = new Color(0.36f, 0.376f, 0.408f);
        // khung nhìn theo pixel rig (tâm x, tâm y, rộng, cao), trùng với tờ khung Spine để so từng khung
        static readonly Vector4 View = new Vector4(-20, 470, 1900, 1500);

        [MenuItem("PokiClash/Thử/Atomik: dựng scene Hải Long (7 clip) và chụp khung")]
        public static void BuildScene()
        {
            var rig = AssetDatabase.LoadAssetAtPath<AtomikAsset>(RigPath);
            if (rig == null) { Debug.LogError($"[Atomik] không thấy {RigPath} (chạy ArtGen/Spine/hai_long.py rig)"); return; }
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
            var root = new GameObject("AtomikHaiLong");
            SceneManager.MoveGameObjectToScene(root, scene);
            float ppu = Mathf.Max(1e-3f, rig.ppu);
            var camGo = new GameObject("Camera");
            camGo.transform.SetParent(root.transform, false);
            camGo.transform.localPosition = new Vector3(View.x / ppu, View.y / ppu, -10);
            var cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            cam.orthographicSize = View.w / ppu * 0.5f;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = Back;
            cam.nearClipPlane = 0.1f;
            cam.farClipPlane = 50f;
            var go = new GameObject("HaiLong");
            go.transform.SetParent(root.transform, false);
            go.AddComponent<MeshFilter>();
            go.AddComponent<MeshRenderer>().sharedMaterial = rig.material;
            var p = go.AddComponent<AtomikPlayer>();
            p.asset = rig;
            p.clip = "dung";
            p.loop = true;
            var demo = root.AddComponent<AtomikDemo>();
            demo.players = new[] { p };
            demo.cam = cam;
            demo.idleClip = "dung";
            demo.fixedCamera = true;
            string shots = Capture(root, cam, p, rig);
            root.transform.position = Vector3.zero;
            p.Sample("dung", 0);
            EditorSceneManager.SaveScene(scene, ScenePath);
            EditorSceneManager.CloseScene(scene, true);
            AssetDatabase.Refresh();
            int nm = rig.masks != null ? rig.masks.Length : 0, ne = 0;
            foreach (var c in rig.anims) ne += c.ev != null ? c.ev.Length : 0;
            Debug.Log($"[Atomik] đã dựng {ScenePath}: {rig.bones.Length} xương, {rig.slots.Length} slot, {rig.anims.Length} clip, {nm} mặt nạ cắt, " +
                      $"{ne} sự kiện; khung chụp ở {shots}");
        }

        // Mỗi clip một ảnh 5 x 2 khung (cùng giờ, cùng khung nhìn với tờ khung Spine của ArtGen/Spine/mo_xe/chay.py sheet n=10).
        static string Capture(GameObject root, Camera cam, AtomikPlayer p, AtomikAsset rig)
        {
            root.transform.position = new Vector3(10000, 10000, 0);   // xa mọi thứ của scene đang mở
            const int W = 520, H = 420, N = 10, Cols = 5;
            float ppu = Mathf.Max(1e-3f, rig.ppu), oldSize = cam.orthographicSize;
            cam.orthographicSize = Mathf.Max(View.w / ppu * 0.5f, View.z / ppu * 0.5f * H / W);
            var rt = new RenderTexture(W, H, 24, RenderTextureFormat.ARGB32) { antiAliasing = 4 };
            var read = new Texture2D(W, H, TextureFormat.RGB24, false);
            cam.targetTexture = rt;
            string dir = Path.GetFullPath("Temp/AtomikShots/hai_long");
            Directory.CreateDirectory(dir);
            foreach (var c in rig.anims)
            {
                int rows = (N + Cols - 1) / Cols;
                var sheet = new Texture2D(W * Cols, H * rows, TextureFormat.RGB24, false);
                for (int i = 0; i < N; i++)
                {
                    p.Sample(c.name, Mathf.Min(c.dur * i / (N - 1), c.dur - 1e-4f));   // khung cuối: sát cuối clip (đúng D thì clip lặp quay về 0)
                    var req = new RenderPipeline.StandardRequest { destination = rt };
                    if (RenderPipeline.SupportsRenderRequest(cam, req)) RenderPipeline.SubmitRenderRequest(cam, req);
                    else cam.Render();
                    RenderTexture.active = rt;
                    read.ReadPixels(new Rect(0, 0, W, H), 0, 0);
                    read.Apply();
                    sheet.SetPixels((i % Cols) * W, (rows - 1 - i / Cols) * H, W, H, read.GetPixels());
                }
                File.WriteAllBytes(Path.Combine(dir, c.name + ".png"), sheet.EncodeToPNG());
                Object.DestroyImmediate(sheet);
            }
            RenderTexture.active = null;
            cam.targetTexture = null;
            Object.DestroyImmediate(rt);
            Object.DestroyImmediate(read);
            cam.orthographicSize = oldSize;
            return dir;
        }
    }
}
