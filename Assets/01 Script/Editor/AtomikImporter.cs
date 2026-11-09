// Nhập file .atomik (định dạng animation xương riêng, xuất bằng ArtGen/Spine/atomik.py): "ATMK" + uint16 phiên bản +
// gzip(uint32 dài JSON + JSON + uint32 dài PNG + PNG). Tạo AtomikAsset (asset chính) kèm atlas và material nằm trong file.
// Menu PokiClash/Thử/Atomik: dựng scene thử (mở thêm rồi lưu, đóng; không đổi scene đang mở) và chụp khung để soi.
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using PokiClash.Game;
using UnityEditor;
using UnityEditor.AssetImporters;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.SceneManagement;

namespace PokiClash.EditorTools
{
    // 3 (2026-11-08): nén atlas theo nền tảng đang build (ASTC 8x8 Android/iOS như atlas tướng aola, DXT5 máy tính khi cạnh chia
    // hết cho 4); đọc bản 2 (độ đậm slot, thông tin trận) qua JsonUtility như các trường khác.
    [ScriptedImporter(3, "atomik")]
    public sealed class AtomikImporter : ScriptedImporter
    {
        public override void OnImportAsset(AssetImportContext ctx)
        {
            var bytes = File.ReadAllBytes(ctx.assetPath);
            if (bytes.Length < 6 || Encoding.ASCII.GetString(bytes, 0, 4) != "ATMK")
            {
                ctx.LogImportError($"{ctx.assetPath}: không phải file .atomik");
                return;
            }
            string json;
            byte[] png;
            using (var ms = new MemoryStream(bytes, 6, bytes.Length - 6))
            using (var gz = new GZipStream(ms, CompressionMode.Decompress))
            using (var br = new BinaryReader(gz))
            {
                json = Encoding.UTF8.GetString(br.ReadBytes(br.ReadInt32()));
                png = br.ReadBytes(br.ReadInt32());
            }
            var asset = ScriptableObject.CreateInstance<AtomikAsset>();
            JsonUtility.FromJsonOverwrite(json, asset);
            string nm = string.IsNullOrEmpty(asset.rigName) ? Path.GetFileNameWithoutExtension(ctx.assetPath) : asset.rigName;
            asset.name = nm;
            var tex = new Texture2D(2, 2, TextureFormat.RGBA32, false) { name = nm + "_atlas" };
            tex.LoadImage(png);
            tex.wrapMode = TextureWrapMode.Clamp;
            tex.filterMode = FilterMode.Bilinear;
            var icon = MakeIcon(asset, tex, 128);  // icon trong cửa sổ Project: hình con ở tư thế gốc
            icon.name = nm + "_icon";
            // atlas RGBA32 không nén tốn ~15 lần ASTC (con mận 493 KB so với ~32 KB): nén theo nền tảng; truy cập selectedBuildTarget
            // làm kết quả nhập phụ thuộc nền tảng, đổi nền tảng thì Unity tự nhập lại
            var target = ctx.selectedBuildTarget;
            bool mobile = target == BuildTarget.Android || target == BuildTarget.iOS;
            if (mobile) EditorUtility.CompressTexture(tex, TextureFormat.ASTC_8x8, TextureCompressionQuality.Best);
            else if (tex.width % 4 == 0 && tex.height % 4 == 0) EditorUtility.CompressTexture(tex, TextureFormat.DXT5, TextureCompressionQuality.Best);
            tex.Apply(false, true);
            // Sprites/Default nhân alpha trong shader: hợp atlas alpha thường (không nhân trước)
            var mat = new Material(Shader.Find("Sprites/Default")) { name = nm + "_mat", mainTexture = tex };
            asset.atlas = tex;
            asset.material = mat;
            ctx.AddObjectToAsset("atlas", tex);
            ctx.AddObjectToAsset("material", mat);
            ctx.AddObjectToAsset("icon", icon);
            ctx.AddObjectToAsset("rig", asset, icon);
            ctx.SetMainObject(asset);
        }

        // Vẽ tư thế gốc (không animation) lên ảnh vuông size x size: dựng đỉnh như AtomikPlayer, tô từng tam giác theo thứ tự slot,
        // lấy mẫu atlas, vẽ ở 2x rồi thu nhỏ cho mịn.
        static Texture2D MakeIcon(AtomikAsset a, Texture2D tex, int size)
        {
            int nb = a.bones.Length;
            var wa = new float[nb]; var wb = new float[nb]; var wc = new float[nb];
            var wd = new float[nb]; var wx = new float[nb]; var wy = new float[nb];
            for (int i = 0; i < nb; i++)
            {
                var b = a.bones[i];
                float r = b.rot * Mathf.Deg2Rad, cs = Mathf.Cos(r), sn = Mathf.Sin(r);
                float la = cs * b.sx, lb = -sn * b.sy, lc = sn * b.sx, ld = cs * b.sy;
                if (b.parent < 0) { wa[i] = la; wb[i] = lb; wc[i] = lc; wd[i] = ld; wx[i] = b.x; wy[i] = b.y; continue; }
                int p = b.parent;
                float pa = wa[p], pb = wb[p], pc = wc[p], pd = wd[p];
                if (b.noScale)
                {
                    float n0 = Mathf.Sqrt(pa * pa + pc * pc), n1 = Mathf.Sqrt(pb * pb + pd * pd);
                    if (n0 > 1e-6f) { pa /= n0; pc /= n0; }
                    if (n1 > 1e-6f) { pb /= n1; pd /= n1; }
                }
                wa[i] = pa * la + pb * lc; wb[i] = pa * lb + pb * ld;
                wc[i] = pc * la + pd * lc; wd[i] = pc * lb + pd * ld;
                wx[i] = wa[p] * b.x + wb[p] * b.y + wx[p];
                wy[i] = wc[p] * b.x + wd[p] * b.y + wy[p];
            }
            var pos = new System.Collections.Generic.List<Vector2>();
            var uv = new System.Collections.Generic.List<Vector2>();
            var tri = new System.Collections.Generic.List<int>();
            foreach (var s in a.slots)
            {
                if (s.att < 0) continue;
                var att = a.atts[s.att];
                int off = pos.Count, k = 0, n = att.uvs.Length / 2;
                for (int v = 0; v < n; v++)
                {
                    int cnt = (int)att.wInfo[k++];
                    float x = 0, y = 0;
                    for (int j = 0; j < cnt; j++, k += 4)
                    {
                        int bi = (int)att.wInfo[k];
                        float bx = att.wInfo[k + 1], by = att.wInfo[k + 2], w = att.wInfo[k + 3];
                        x += (wa[bi] * bx + wb[bi] * by + wx[bi]) * w;
                        y += (wc[bi] * bx + wd[bi] * by + wy[bi]) * w;
                    }
                    pos.Add(new Vector2(x, y));
                    uv.Add(new Vector2(att.uvs[2 * v], att.uvs[2 * v + 1]));
                }
                foreach (var t in att.tris) tri.Add(t + off);
            }
            int S = size * 2;
            var px = new Color[S * S];
            if (pos.Count > 0)
            {
                Vector2 mn = pos[0], mx = pos[0];
                foreach (var q in pos) { mn = Vector2.Min(mn, q); mx = Vector2.Max(mx, q); }
                float scale = S * 0.92f / Mathf.Max(mx.x - mn.x, mx.y - mn.y, 1e-3f);
                var ctr = (mn + mx) * 0.5f;
                Vector2 Map(Vector2 q) => (q - ctr) * scale + new Vector2(S * 0.5f, S * 0.5f);
                for (int t = 0; t + 2 < tri.Count; t += 3)
                {
                    Vector2 p0 = Map(pos[tri[t]]), p1 = Map(pos[tri[t + 1]]), p2 = Map(pos[tri[t + 2]]);
                    float den = (p1.y - p2.y) * (p0.x - p2.x) + (p2.x - p1.x) * (p0.y - p2.y);
                    if (Mathf.Abs(den) < 1e-6f) continue;
                    int x0 = Mathf.Max(0, Mathf.FloorToInt(Mathf.Min(p0.x, Mathf.Min(p1.x, p2.x))));
                    int x1 = Mathf.Min(S - 1, Mathf.CeilToInt(Mathf.Max(p0.x, Mathf.Max(p1.x, p2.x))));
                    int y0 = Mathf.Max(0, Mathf.FloorToInt(Mathf.Min(p0.y, Mathf.Min(p1.y, p2.y))));
                    int y1 = Mathf.Min(S - 1, Mathf.CeilToInt(Mathf.Max(p0.y, Mathf.Max(p1.y, p2.y))));
                    for (int yy = y0; yy <= y1; yy++)
                        for (int xx = x0; xx <= x1; xx++)
                        {
                            float cx = xx + 0.5f, cy = yy + 0.5f;
                            float l0 = ((p1.y - p2.y) * (cx - p2.x) + (p2.x - p1.x) * (cy - p2.y)) / den;
                            float l1 = ((p2.y - p0.y) * (cx - p2.x) + (p0.x - p2.x) * (cy - p2.y)) / den;
                            float l2 = 1 - l0 - l1;
                            if (l0 < -1e-4f || l1 < -1e-4f || l2 < -1e-4f) continue;
                            var u = uv[tri[t]] * l0 + uv[tri[t + 1]] * l1 + uv[tri[t + 2]] * l2;
                            var c = tex.GetPixelBilinear(u.x, u.y);
                            ref var d = ref px[yy * S + xx];
                            float oa = c.a + d.a * (1 - c.a);
                            if (oa > 1e-5f) d = new Color((c.r * c.a + d.r * d.a * (1 - c.a)) / oa,
                                                        (c.g * c.a + d.g * d.a * (1 - c.a)) / oa,
                                                        (c.b * c.a + d.b * d.a * (1 - c.a)) / oa, oa);
                        }
                }
            }
            var outPx = new Color[size * size];  // thu nhỏ 2x (trung bình có trọng số alpha)
            for (int y = 0; y < size; y++)
                for (int x = 0; x < size; x++)
                {
                    Color sum = Color.clear;
                    float aSum = 0;
                    for (int j = 0; j < 2; j++)
                        for (int i = 0; i < 2; i++)
                        {
                            var c = px[(2 * y + j) * S + 2 * x + i];
                            sum += new Color(c.r * c.a, c.g * c.a, c.b * c.a, 0);
                            aSum += c.a;
                        }
                    outPx[y * size + x] = aSum > 1e-5f ? new Color(sum.r / aSum, sum.g / aSum, sum.b / aSum, aSum / 4) : Color.clear;
                }
            var icon = new Texture2D(size, size, TextureFormat.RGBA32, false) { alphaIsTransparency = true };
            icon.SetPixels(outPx);
            icon.Apply();
            return icon;
        }
    }

    public static class AtomikMenu
    {
        const string Dir = "Assets/05 Atomik Thu";
        const string RigPath = Dir + "/man_kiem.atomik";
        const string ScenePath = Dir + "/AtomikMan.unity";
        static readonly Color Paper = new Color(0.98f, 0.965f, 0.925f);

        [MenuItem("PokiClash/Thử/Atomik: dựng scene con mận (idle, nhảy, chém)")]
        public static void BuildScene()
        {
            var rig = AssetDatabase.LoadAssetAtPath<AtomikAsset>(RigPath);
            if (rig == null) { Debug.LogError($"[Atomik] không thấy {RigPath}"); return; }
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
            var root = new GameObject("Atomik");
            SceneManager.MoveGameObjectToScene(root, scene);
            var camGo = new GameObject("Camera");
            camGo.transform.SetParent(root.transform, false);
            camGo.transform.localPosition = new Vector3(0, 1.9f, -10);
            var cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            cam.orthographicSize = 2.9f;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = Paper;
            cam.nearClipPlane = 0.1f;
            cam.farClipPlane = 50f;
            string[] clips = { "idle", "jump", "slash" };
            var players = new AtomikPlayer[clips.Length];
            for (int i = 0; i < clips.Length; i++)
            {
                var go = new GameObject("ManKiem_" + clips[i]);
                go.transform.SetParent(root.transform, false);
                go.transform.localPosition = new Vector3((i - 1) * 3.4f, 0, 0);
                go.AddComponent<MeshFilter>();
                go.AddComponent<MeshRenderer>().sharedMaterial = rig.material;
                var p = go.AddComponent<AtomikPlayer>();
                p.asset = rig;
                p.clip = clips[i];
                p.loop = true;
                players[i] = p;
            }
            var demo = root.AddComponent<AtomikDemo>();
            demo.players = players;
            demo.cam = cam;
            string shot = Capture(root, cam, players[1], rig);
            root.transform.position = Vector3.zero;
            EditorSceneManager.SaveScene(scene, ScenePath);
            EditorSceneManager.CloseScene(scene, true);
            AssetDatabase.Refresh();
            Debug.Log($"[Atomik] đã dựng {ScenePath} ({rig.bones.Length} xương, {rig.anims.Length} clip); khung chụp: {shot}");
        }

        // Chụp 9 khung mỗi clip bằng một con (để xa mọi thứ của scene đang mở), ghép thành một ảnh trong Temp/AtomikShots.
        static string Capture(GameObject root, Camera cam, AtomikPlayer p, AtomikAsset rig)
        {
            var others = root.GetComponentsInChildren<AtomikPlayer>().Where(x => x != p).ToArray();
            foreach (var o in others) o.gameObject.SetActive(false);
            var oldPos = p.transform.localPosition;
            string oldClip = p.clip;
            p.transform.localPosition = Vector3.zero;
            root.transform.position = new Vector3(10000, 10000, 0);
            float oldSize = cam.orthographicSize;
            var oldCam = cam.transform.localPosition;
            cam.orthographicSize = 2.3f;
            cam.transform.localPosition = new Vector3(0, 1.95f, -10);
            const int W = 300, H = 300, N = 9;
            var rt = new RenderTexture(W, H, 24, RenderTextureFormat.ARGB32) { antiAliasing = 4 };
            var sheet = new Texture2D(W * N, H * rig.anims.Length, TextureFormat.RGB24, false);
            var read = new Texture2D(W, H, TextureFormat.RGB24, false);
            cam.targetTexture = rt;
            for (int a = 0; a < rig.anims.Length; a++)
                for (int i = 0; i < N; i++)
                {
                    p.Sample(rig.anims[a].name, rig.anims[a].dur * i / (N - 1));
                    RenderCam(cam, rt);
                    RenderTexture.active = rt;
                    read.ReadPixels(new Rect(0, 0, W, H), 0, 0);
                    read.Apply();
                    sheet.SetPixels(i * W, (rig.anims.Length - 1 - a) * H, W, H, read.GetPixels());
                }
            RenderTexture.active = null;
            cam.targetTexture = null;
            Object.DestroyImmediate(rt);
            Object.DestroyImmediate(read);
            string dir = Path.GetFullPath("Temp/AtomikShots");
            Directory.CreateDirectory(dir);
            string path = Path.Combine(dir, rig.rigName + "_khung.png");
            File.WriteAllBytes(path, sheet.EncodeToPNG());
            Object.DestroyImmediate(sheet);
            // trả lại như cũ
            cam.orthographicSize = oldSize;
            cam.transform.localPosition = oldCam;
            p.transform.localPosition = oldPos;
            p.Sample(oldClip, 0);
            foreach (var o in others) o.gameObject.SetActive(true);
            return path;
        }

        static void RenderCam(Camera cam, RenderTexture rt)
        {
            var req = new RenderPipeline.StandardRequest { destination = rt };
            if (RenderPipeline.SupportsRenderRequest(cam, req)) RenderPipeline.SubmitRenderRequest(cam, req);
            else cam.Render();
        }
    }
}
