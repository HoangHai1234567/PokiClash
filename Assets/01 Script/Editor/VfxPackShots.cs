// Chụp từng prefab của gói VFX nước (SrRubfish Water VFX 02 + NamuFX Stylized Water) để soi dáng + nhịp trước khi làm lại bộ nước
// trong game (người dùng 2026-11-25: "làm lại vfx nước của game theo asset này ... quét thật kĩ").
// Chạy khi đang Play: Time.captureFramerate cố định → mỗi khung đúng 1/Fps giây (hạt và texture trôi theo _Time của shader),
// đọc ảnh camera chụp ngay sau khi render (RenderPipelineManager.endContextRendering). Ảnh: Temp/PokiShots/vfx_goi/<gói>_<prefab>/f_###.png, góc máy ngang hơi chúc
// xuống như sân đấu. Ghép GIF + trang xem: ArtGen/XemVfx/vfx_goi/ghep.py.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering;
using Object = UnityEngine.Object;

namespace PokiClash.EditorTools
{
    public static class VfxPackShots
    {
        const string OutRoot = "Temp/PokiShots/vfx_goi";
        const int Fps = 24, W = 480, H = 300;
        static readonly Vector3 Origin = new Vector3(9000, 0, 0);
        static readonly string[] Dirs = { "Assets/SrRubfish_VFX_02/Prefabs", "Assets/NamuFX/StylizedWaterEffects/Prefabs" };

        static Queue<string> todo;
        static GameObject inst;
        static Camera cam;
        static RenderTexture rt;
        static Texture2D read;
        static int frame, total, done, rw = W, rh = H;
        static bool capturing, pendingNext, bgPrev, sceneMode, probing, restart;
        static int bx0, by0, bx1, by1;
        static GameObject cur;
        static string waitScene;
        static string dir;

        [MenuItem("PokiClash/Thử/VFX gói nước: chụp mọi prefab Rubfish + NamuFX (đang Play)")]
        static void All() => Begin(null);

        [MenuItem("PokiClash/Thử/VFX gói nước: chụp riêng Water Laser (đang Play)")]
        static void Laser() => Begin("WaterLaser");

        // 4 scene demo của Rubfish (Timeline ghép Cast → MainLaser → Impact...): chụp qua camera demo, khung 16:9, tối đa 12 s
        [MenuItem("PokiClash/Thử/VFX gói nước: chụp 4 scene demo Rubfish (đang Play)")]
        static void Demos() => Begin(null, true);

        // game tắt Run In Background (PlayerSettings): Unity nằm nền (người dùng không thao tác) thì vòng game đứng → tour không chạy.
        // Bật tạm cho lần Play này (chỉ giá trị lúc chạy, không đổi ProjectSettings; thoát Play là về như cũ)
        [MenuItem("PokiClash/Thử/Play chạy cả khi Unity nằm nền (tạm, tới khi thoát Play)")]
        static void ChayNen()
        {
            Application.runInBackground = true;
            Debug.Log("[VfxPackShots] runInBackground = true (tới khi thoát Play)");
        }

        public static void Begin(string filter, bool scenes = false)
        {
            if (!EditorApplication.isPlaying)
            {
                Debug.LogError("[VfxPackShots] cần đang Play");
                return;
            }
            var paths = scenes
                ? AssetDatabase.FindAssets("t:Scene", new[] { "Assets/SrRubfish_VFX_02/DemoScene" }).Select(g => "scene:" + AssetDatabase.GUIDToAssetPath(g)).OrderBy(p => p).ToList()
                : AssetDatabase.FindAssets("t:Prefab", Dirs.Where(AssetDatabase.IsValidFolder).ToArray())
                .Select(AssetDatabase.GUIDToAssetPath)
                .Where(p => filter == null || p.Contains(filter))
                .Where(p => !p.Contains("Viewer") && !p.Contains("--Env--"))
                .OrderBy(p => p).ToList();
            sceneMode = scenes;
            rw = scenes ? 640 : W;
            rh = scenes ? 360 : H;
            todo = new Queue<string>(paths);
            done = 0;
            rt = new RenderTexture(rw, rh, 24, RenderTextureFormat.ARGB32) { antiAliasing = 4 };
            read = new Texture2D(rw, rh, TextureFormat.RGB24, false);
            var cg = new GameObject("vfx_goi_cam") { hideFlags = HideFlags.DontSave };
            Object.DontDestroyOnLoad(cg); // chế độ scene: nạp scene Single không được xoá camera chụp
            cam = cg.AddComponent<Camera>();
            cam.orthographic = true;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.45f, 0.46f, 0.48f, 1);
            cam.nearClipPlane = 0.1f;
            cam.farClipPlane = 600;
            cam.targetTexture = rt;
            cam.enabled = true; // tự render mỗi khung; đọc ảnh ở endContextRendering
            Time.captureFramerate = Fps; // mỗi khung đúng 1/Fps giây game (hạt + _Time của shader)
            bgPrev = Application.runInBackground;
            Application.runInBackground = true; // game tắt Run In Background → Unity nằm nền là Play đứng; bật tạm, xong trả lại
            EditorApplication.isPaused = false;
            Unhook();
            RenderPipelineManager.endContextRendering += OnEnd;
            Application.onBeforeRender += OnBefore;
            EditorApplication.playModeStateChanged += OnMode;
            pendingNext = true;
            Debug.Log($"[VfxPackShots] bắt đầu {paths.Count} prefab");
        }

        // Unity giãn nhịp EditorApplication.update khi cửa sổ không được tương tác → không dựa vào update / Step;
        // việc dựng prefab mới làm trong onBeforeRender (giữa vòng game), đọc ảnh ngay sau khi các camera render xong.
        static void OnBefore()
        {
            if (waitScene != null)
            {
                var sc = UnityEngine.SceneManagement.SceneManager.GetActiveScene();
                if (sc.path != waitScene || !sc.isLoaded) return;
                waitScene = null;
                SetupDemo();
                return;
            }
            if (restart)
            {
                restart = false;
                if (inst) Object.DestroyImmediate(inst);
                Spawn();
                return;
            }
            if (!pendingNext) return;
            pendingNext = false;
            if (inst) Object.DestroyImmediate(inst);
            inst = null;
            Next();
        }

        static void OnEnd(ScriptableRenderContext ctx, List<Camera> cams)
        {
            if (!capturing || !inst && !sceneMode || !cam || !cams.Contains(cam)) return;
            RenderTexture.active = rt;
            read.ReadPixels(new Rect(0, 0, rw, rh), 0, 0);
            read.Apply();
            RenderTexture.active = null;
            if (probing) Probe();
            else File.WriteAllBytes(Path.Combine(dir, $"f_{frame:000}.png"), read.EncodeToPNG());
            frame++;
            if (frame >= total)
            {
                capturing = false;
                if (probing)
                {
                    probing = false;
                    Tighten();
                    restart = true; // dựng lại prefab, chụp thật với khung sát
                }
                else
                {
                    done++;
                    pendingNext = true;
                }
            }
        }

        // lượt dò: gộp khung các điểm ảnh khác nền qua mọi khung (quầng / sóng xung kích gần trong suốt không làm phình khung)
        static void Probe()
        {
            var px = read.GetPixels32();
            var bg = (Color32)cam.backgroundColor;
            for (int y = 0; y < rh; y += 2)
            for (int x = 0; x < rw; x += 2)
            {
                var c = px[y * rw + x];
                if (Mathf.Abs(c.r - bg.r) + Mathf.Abs(c.g - bg.g) + Mathf.Abs(c.b - bg.b) < 40) continue;
                if (x < bx0) bx0 = x;
                if (x > bx1) bx1 = x;
                if (y < by0) by0 = y;
                if (y > by1) by1 = y;
            }
        }

        static void Tighten()
        {
            if (bx1 < bx0 || by1 < by0) return;
            float vx = (bx0 + bx1 + 2) * 0.5f / rw, vy = (by0 + by1 + 2) * 0.5f / rh;
            float hw = 2 * cam.orthographicSize, ww = hw * rw / rh;
            float bw = (bx1 - bx0 + 3) / (float)rw * ww, bh = (by1 - by0 + 3) / (float)rh * hw;
            var c = cam.ViewportToWorldPoint(new Vector3(vx, vy, 300));
            cam.orthographicSize = Mathf.Max(0.25f, Mathf.Max(bh / 2, bw / 2 / ((float)rw / rh)) * 1.12f);
            cam.transform.position = c - cam.transform.forward * 300;
            File.AppendAllText(Path.Combine(dir, "info.txt"), $"tight=({bx0},{by0})-({bx1},{by1}) ortho={cam.orthographicSize:0.00}\n");
        }

        // camera của scene demo (gói không gắn tag MainCamera): chép thông số sang camera chụp, độ dài theo Timeline đang bật (≤ 12 s)
        static void SetupDemo()
        {
            var src = Object.FindObjectsByType<Camera>(FindObjectsSortMode.None).Where(c => c != cam && c.enabled && !c.targetTexture)
                .OrderByDescending(c => c.depth).FirstOrDefault();
            if (src)
            {
                cam.CopyFrom(src);
                cam.targetTexture = rt;
                cam.enabled = true;
            }
            double d = 6;
            foreach (var pd in Object.FindObjectsByType<UnityEngine.Playables.PlayableDirector>(FindObjectsSortMode.None))
                if (pd.isActiveAndEnabled) d = System.Math.Max(d, pd.duration);
            total = Mathf.CeilToInt((float)System.Math.Min(d, 12) * Fps);
            File.WriteAllText(Path.Combine(dir, "info.txt"), $"{UnityEngine.SceneManagement.SceneManager.GetActiveScene().path}\nframes={total} fps={Fps}\ncam={(src ? src.name : "-")}\n");
            frame = 0;
            capturing = true;
        }

        static void Spawn()
        {
            inst = Object.Instantiate(cur, Origin, Quaternion.identity);
            inst.hideFlags = HideFlags.DontSave;
            foreach (var ps in inst.GetComponentsInChildren<ParticleSystem>(true))
                if (ps.main.playOnAwake && ps.gameObject.activeInHierarchy && !ps.isPlaying) ps.Play(false);
            frame = 0;
            capturing = true;
        }

        static void OnMode(PlayModeStateChange m)
        {
            if (m == PlayModeStateChange.ExitingPlayMode) Finish();
        }

        static void Unhook()
        {
            RenderPipelineManager.endContextRendering -= OnEnd;
            Application.onBeforeRender -= OnBefore;
            EditorApplication.playModeStateChanged -= OnMode;
        }

        static void Next()
        {
            while (todo.Count > 0)
            {
                string p = todo.Dequeue();
                if (p.StartsWith("scene:"))
                {
                    waitScene = p.Substring(6);
                    dir = Path.Combine(OutRoot, "demo_" + Path.GetFileNameWithoutExtension(waitScene));
                    Directory.CreateDirectory(dir);
                    foreach (var f in Directory.GetFiles(dir, "f_*.png")) File.Delete(f);
                    UnityEditor.SceneManagement.EditorSceneManager.LoadSceneInPlayMode(waitScene, new UnityEngine.SceneManagement.LoadSceneParameters(UnityEngine.SceneManagement.LoadSceneMode.Single));
                    return;
                }
                var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(p);
                if (!prefab) continue;
                string pack = p.Contains("NamuFX") ? "namu" : "rub";
                dir = Path.Combine(OutRoot, pack + "_" + prefab.name);
                Directory.CreateDirectory(dir);
                foreach (var f in Directory.GetFiles(dir, "f_*.png")) File.Delete(f);
                var b = Measure(prefab);
                Frame(b);
                total = Mathf.CeilToInt(Dur(prefab) * Fps);
                File.WriteAllText(Path.Combine(dir, "info.txt"), $"{p}\nframes={total} fps={Fps}\nbounds={b.center} {b.size}\n");
                cur = prefab;
                bx0 = by0 = int.MaxValue;
                bx1 = by1 = -1;
                probing = true;
                Spawn();
                return;
            }
            Finish();
        }

        // khung bao: mô phỏng hạt ở vài mốc giờ (bản sao tạm), gộp vị trí ± cỡ từng hạt THẬT SỰ ĐƯỢC VẼ (bỏ bộ phát không vật liệu /
        // RenderMode None: gói có bộ phát vô hình sống 5 s bay 5 đơn vị/s làm khung bao Renderer phình ~50 đơn vị) + MeshRenderer thường
        static Bounds Measure(GameObject prefab)
        {
            var off = new Vector3(0, 0, 3000);
            var g = Object.Instantiate(prefab, Origin + off, Quaternion.identity);
            var all = g.GetComponentsInChildren<ParticleSystem>(true);
            var roots = all.Where(ps => !ps.transform.parent || !ps.transform.parent.GetComponentInParent<ParticleSystem>()).ToArray();
            var b = new Bounds();
            bool has = false;
            void Add(Vector3 c, float r)
            {
                var bb = new Bounds(c, Vector3.one * (2 * r));
                if (!has) b = bb;
                else b.Encapsulate(bb);
                has = true;
            }
            var buf = new ParticleSystem.Particle[4000];
            foreach (float t in new[] { 0.08f, 0.2f, 0.35f, 0.55f, 0.8f, 1.1f, 1.5f })
            {
                foreach (var ps in roots) ps.Simulate(t, true, true);
                foreach (var ps in all)
                {
                    var pr = ps.GetComponent<ParticleSystemRenderer>();
                    if (!pr || !pr.enabled || pr.renderMode == ParticleSystemRenderMode.None || !pr.sharedMaterial || !ps.gameObject.activeInHierarchy) continue;
                    float k = 0.5f;
                    if (pr.renderMode == ParticleSystemRenderMode.Mesh && pr.mesh) k = pr.mesh.bounds.center.magnitude + pr.mesh.bounds.extents.magnitude;
                    if (pr.renderMode == ParticleSystemRenderMode.Stretch) k *= Mathf.Max(1, Mathf.Abs(pr.lengthScale));
                    float sc = ps.main.scalingMode == ParticleSystemScalingMode.Shape ? 1 : ps.transform.lossyScale.x;
                    int n = ps.GetParticles(buf);
                    var space = ps.main.simulationSpace;
                    for (int i = 0; i < n; i++)
                    {
                        var q = buf[i];
                        var pos = space == ParticleSystemSimulationSpace.World ? q.position : ps.transform.TransformPoint(q.position);
                        Add(pos, q.GetCurrentSize3D(ps).magnitude * k * Mathf.Abs(sc));
                    }
                }
                foreach (var mr in g.GetComponentsInChildren<MeshRenderer>())
                    if (mr.enabled && mr.sharedMaterial && mr.bounds.size.magnitude < 200) Add(mr.bounds.center, mr.bounds.extents.magnitude);
            }
            Object.DestroyImmediate(g);
            if (!has) b = new Bounds(Origin + off, Vector3.one * 4);
            b.center -= off;
            return b;
        }

        // góc máy: nhìn ngang (theo trục ngắn của khung bao) hơi chúc xuống 18°, vừa khung + lề
        static void Frame(Bounds b)
        {
            bool lookX = b.size.z > b.size.x * 1.3f;
            var rot = Quaternion.Euler(18, lookX ? 90 : 0, 0);
            var fwd = rot * Vector3.forward;
            cam.transform.SetPositionAndRotation(b.center - fwd * 300, rot);
            float horiz = lookX ? b.size.z : b.size.x;
            float vert = b.size.y * Mathf.Cos(18 * Mathf.Deg2Rad) + (lookX ? b.size.x : b.size.z) * Mathf.Sin(18 * Mathf.Deg2Rad);
            cam.orthographicSize = Mathf.Max(0.8f, Mathf.Max(vert / 2, horiz / 2 / ((float)rw / rh)) * 1.18f);
        }

        static float Dur(GameObject prefab)
        {
            float d = 0.6f;
            bool loop = false;
            foreach (var ps in prefab.GetComponentsInChildren<ParticleSystem>(true))
            {
                var m = ps.main;
                if (m.loop) loop = true;
                d = Mathf.Max(d, m.startDelay.constantMax + (m.loop ? 0 : m.duration) + m.startLifetime.constantMax);
            }
            var an = prefab.GetComponentInChildren<Animator>(true);
            if (an && an.runtimeAnimatorController)
                foreach (var c in an.runtimeAnimatorController.animationClips) d = Mathf.Max(d, c.length);
            return Mathf.Clamp(loop ? Mathf.Max(d, 2.0f) : d + 0.15f, 0.6f, 3f);
        }

        static void Finish()
        {
            Unhook();
            capturing = pendingNext = false;
            Application.runInBackground = bgPrev;
            Time.captureFramerate = 0;
            if (inst) Object.DestroyImmediate(inst);
            if (cam) Object.DestroyImmediate(cam.gameObject);
            if (rt)
            {
                rt.Release();
                Object.DestroyImmediate(rt);
            }
            if (read) Object.DestroyImmediate(read);
            inst = null;
            File.WriteAllText(Path.Combine(OutRoot, "xong.txt"), $"{done}\n");
            Debug.Log($"[VfxPackShots] xong {done} prefab → {OutRoot}");
        }
    }
}
