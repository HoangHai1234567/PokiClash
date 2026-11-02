// Chạy animation tướng xuất từ dự án aola (reskin/<tên>/export/anim.json). CHỈ TRONG EDITOR HOẶC BẢN DEV (define
// POKICLASH_DEV): hình gốc của Baitian. PNG đọc thẳng từ ổ đĩa lúc chạy, không chép vào Assets (PreBuildCheck chặn).
// Mỗi hình là một quad, đỉnh tính từ ma trận Flash của khung (có cả nghiêng), nên một Transform thường không đủ.
// Mọi thứ sinh lúc chạy của hình aola (GameObject, Mesh, Texture2D, Sprite, Material) gói trong file này (ngoại lệ của
// test chặn prefab).
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEngine;
using UnityEngine.Rendering;

namespace PokiClash.Game
{
    public sealed class AolaActor : MonoBehaviour
    {
        // mỗi hình: sprite, a, b, c, d, tx, ty, alpha, nhân r g b, cộng r g b (0..1), sáng cộng (blend add/screen: 1)
        const int Cols = 15;

        sealed class Clip
        {
            public readonly List<float[][]> Frames = new(); // mỗi hình Cols số như trên
            public Vector2 Anchor;                          // tâm bóng dưới chân ở khung đầu, điểm khớp giữa các clip
        }

        public const string Idle = "1_1", Hit = "1_2", Attack = "1_4", Skill = "1_6";

        static readonly Dictionary<string, Texture2D> TexCache = new();
        static readonly Dictionary<string, Sprite> PortraitCache = new();
        static Material material, additive;

        readonly Dictionary<string, Clip> clips = new();
        readonly List<Texture2D> textures = new();
        readonly List<(MeshRenderer r, Mesh m, Vector3[] v, Color[] c)> pool = new();
        MaterialPropertyBlock block;
        float fps = 25, unit = 0.01f, time;
        int shadowSprite = -1;
        bool flip, loop = true;
        int sortBase, shown = -1;
        string current = Idle;
        Transform placeholder;

        public bool HasAnim => clips.Count > 0;
        public float Duration(string clip) => clips.TryGetValue(clip, out var c) ? c.Frames.Count / fps : 0.3f;

        // Thư mục reskin: biến môi trường AOLA_RESKIN, hoặc (Editor) EditorPrefs "PokiClash.AolaReskin" (menu PokiClash/Đặt
        // thư mục aola); EditorPrefs trống thì tự tìm trên các ổ đĩa một lần (FindReskin) rồi ghi vào EditorPrefs.
        public const string PrefKey = "PokiClash.AolaReskin";
#if UNITY_EDITOR
        static string foundDir;
        static bool searched;

        public static void ForgetDir()
        {
            searched = false;
            foundDir = null;
        }
#endif

        // Chỉ lúc Play: prefab và test EditMode (Editor, không Play) không được gắn sprite đọc từ đĩa; lúc đó ô tướng để trống.
        public static string ReskinDir => Application.isPlaying ? FindDir() : null;

        // Thư mục reskin bất kể đang Play hay không (menu PokiClash/Tự tìm thư mục aola).
        public static string FindDir()
        {
#if UNITY_EDITOR || POKICLASH_DEV
            var env = Environment.GetEnvironmentVariable("AOLA_RESKIN");
            if (!string.IsNullOrEmpty(env)) return env;
#endif
#if UNITY_EDITOR
            if (searched) return foundDir;
            searched = true;
            var pref = UnityEditor.EditorPrefs.GetString(PrefKey, "");
            foundDir = !string.IsNullOrEmpty(pref) && Directory.Exists(pref) ? pref : FindReskin();
            if (foundDir != null) UnityEditor.EditorPrefs.SetString(PrefKey, foundDir);
            return foundDir;
#else
            return null;
#endif
        }

#if UNITY_EDITOR
        // Thư mục reskin của AolaRipper: dưới một thư mục gốc ổ đĩa tên bắt đầu bằng "Aola", sâu tối đa 4 cấp, có thư mục
        // con chứa export/anim.json.
        public static string FindReskin()
        {
            foreach (var drive in DriveInfo.GetDrives())
            {
                if (drive.DriveType != DriveType.Fixed || !drive.IsReady) continue;
                string[] tops;
                try { tops = Directory.GetDirectories(drive.RootDirectory.FullName, "Aola*"); }
                catch (Exception) { continue; }
                foreach (var top in tops)
                {
                    var hit = SearchReskin(top, 4);
                    if (hit != null) return hit.Replace('\\', '/');
                }
            }
            return null;
        }

        static string SearchReskin(string dir, int depth)
        {
            try
            {
                var r = Path.Combine(dir, "reskin");
                if (Directory.Exists(r))
                    foreach (var sub in Directory.GetDirectories(r))
                        if (File.Exists(Path.Combine(sub, "export", "anim.json"))) return r;
                if (depth <= 0) return null;
                foreach (var sub in Directory.GetDirectories(dir))
                {
                    var hit = SearchReskin(sub, depth - 1);
                    if (hit != null) return hit;
                }
            }
            catch (Exception) { }
            return null;
        }
#endif

        // Chân dung tĩnh (reskin/<tên>/export/portrait.png, tools/portrait_png.py của AolaRipper): khung 4:5 như HeroArt,
        // chân ở giữa và cách đáy HeroArt.FootY. Bản phát hành hoặc chưa xuất: null.
        public static Sprite Portrait(string aolaName)
        {
#if !(UNITY_EDITOR || POKICLASH_DEV)
            return null;
#else
            if (string.IsNullOrEmpty(aolaName)) return null;
            var root = ReskinDir;
            if (root == null) return null;
            if (PortraitCache.TryGetValue(aolaName, out var s) && s) return s;
            var t = LoadTexture(Path.GetFullPath(Path.Combine(root, aolaName, "export", "portrait.png")));
            s = t ? Sprite.Create(t, new Rect(0, 0, t.width, t.height), new Vector2(0.5f, HeroArt.FootY), 100) : null;
            if (s) s.name = "aola_" + aolaName;
            PortraitCache[aolaName] = s;
            return s;
#endif
        }

        // Nạp tướng theo tên thư mục aola (HeroDef.aola). Bản phát hành luôn trả false: gọi UsePlaceholder.
        public bool LoadHero(string aolaName, float height, bool flipX, int sorting)
        {
            var root = ReskinDir;
            return root != null && !string.IsNullOrEmpty(aolaName) && Load(Path.Combine(root, aolaName), height, flipX, sorting);
        }

        // dir = reskin/<tên>; height = chiều cao dáng đứng (đơn vị thế giới); flip = lật ngang
        public bool Load(string dir, float height, bool flipX, int sorting)
        {
            flip = flipX;
            sortBase = sorting;
#if !(UNITY_EDITOR || POKICLASH_DEV)
            return false;
#else
            string path = Path.Combine(dir, "export", "anim.json");
            if (!File.Exists(path)) return false;
            try
            {
                var root = (Dictionary<string, object>)MiniJson.Parse(File.ReadAllText(path));
                fps = Convert.ToSingle(root["fps"]);
                foreach (var sp in (List<object>)root["sprites"])
                    textures.Add(LoadTexture(Path.GetFullPath(Path.Combine(dir, (string)sp))));
                foreach (var kv in (Dictionary<string, object>)root["clips"])
                {
                    var clip = new Clip();
                    foreach (List<object> frame in (List<object>)((Dictionary<string, object>)kv.Value)["frames"])
                    {
                        var pics = new float[frame.Count][];
                        for (int i = 0; i < frame.Count; i++)
                        {
                            var row = (List<object>)frame[i];
                            var f = new float[Cols];
                            for (int k = 0; k < 8; k++) f[k] = Convert.ToSingle(row[k]);
                            f[8] = f[9] = f[10] = 1;
                            // hiệu ứng: tint [nhân r g b, cộng r g b (0..255)], blend (mã SWF: 8 cộng, 4 screen)
                            if (row.Count > 8 && row[8] is Dictionary<string, object> fx)
                            {
                                if (fx.TryGetValue("tint", out var tv) && tv is List<object> tint && tint.Count >= 6)
                                    for (int k = 0; k < 6; k++) f[8 + k] = Convert.ToSingle(tint[k]) / (k < 3 ? 1f : 255f);
                                if (fx.TryGetValue("blend", out var bv))
                                {
                                    int b = Convert.ToInt32(bv);
                                    f[14] = b == 8 || b == 4 ? 1 : 0;
                                }
                            }
                            pics[i] = f;
                        }
                        clip.Frames.Add(pics);
                    }
                    clips[kv.Key] = clip;
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning($"[Aola] Không đọc được {path}: {e.Message}");
                clips.Clear();
                return false;
            }
            if (!clips.ContainsKey(Idle)) { clips.Clear(); return false; }

            // bóng dưới chân (thường là hình vẽ trước tiên của khung đầu dáng đứng); mọi clip khớp nhau ở tâm bóng
            int shadow = FindShadow();
            shadowSprite = shadow;
            foreach (var clip in clips.Values) clip.Anchor = AnchorOf(clip, shadow);
            float top = float.MaxValue;
            foreach (var p in clips[Idle].Frames[0])
                foreach (var q in Corners(p)) top = Mathf.Min(top, q.y);
            unit = height / Mathf.Max(1f, clips[Idle].Anchor.y - top);
            loadedHeight = height;

            block = new MaterialPropertyBlock();
            Play(Idle, true);
            return true;
#endif
        }

        // Bóng: hình xám không màu, nửa trong suốt, bè ngang, trong 3 hình đầu của khung đầu dáng đứng (có con vẽ quầng
        // trước bóng, như 2955). Bóng trong 79 dạng đã xuất: độ bão hòa 0, alpha 75–130, rộng/cao từ 1.75 (677); hình xám khác
        // đều đục (alpha ≥ 240). Không có thì -1.
        int FindShadow()
        {
            var frame = clips[Idle].Frames[0];
            for (int i = 0; i < Mathf.Min(3, frame.Length); i++)
            {
                int s = (int)frame[i][0];
                if (textures[s] && IsShadow(textures[s])) return s;
            }
            return -1;
        }

        static bool IsShadow(Texture2D t)
        {
            if (t.width < t.height * 1.5f) return false;
            var px = t.GetPixels32();
            long n = 0, alpha = 0, sat = 0;
            for (int i = 0; i < px.Length; i += 5)
            {
                var c = px[i];
                if (c.a <= 10) continue;
                n++;
                alpha += c.a;
                sat += Mathf.Max(c.r, Mathf.Max(c.g, c.b)) - Mathf.Min(c.r, Mathf.Min(c.g, c.b));
            }
            return n > 0 && sat / n < 8 && alpha / n < 170;
        }

        Vector2 AnchorOf(Clip clip, int shadow)
        {
            var frame = clip.Frames[0];
            foreach (var p in frame)
                if ((int)p[0] == shadow && textures[shadow] != null)
                {
                    var t = textures[shadow];
                    return Map(p, t.width / 2f, t.height / 2f);
                }
            // không có bóng: lấy giữa đáy của khung đầu
            float minX = float.MaxValue, maxX = float.MinValue, maxY = float.MinValue;
            foreach (var p in frame)
                foreach (var q in Corners(p)) { minX = Mathf.Min(minX, q.x); maxX = Mathf.Max(maxX, q.x); maxY = Mathf.Max(maxY, q.y); }
            return new Vector2((minX + maxX) / 2, maxY);
        }

        // ma trận Flash: x' = a x + c y + tx, y' = b x + d y + ty (điểm ảnh, y hướng xuống)
        static Vector2 Map(float[] p, float x, float y) => new(p[1] * x + p[3] * y + p[5], p[2] * x + p[4] * y + p[6]);

        IEnumerable<Vector2> Corners(float[] p)
        {
            var t = textures[(int)p[0]];
            if (t == null) yield break;
            yield return Map(p, 0, 0);
            yield return Map(p, t.width, 0);
            yield return Map(p, t.width, t.height);
            yield return Map(p, 0, t.height);
        }

        static Texture2D LoadTexture(string path)
        {
            if (TexCache.TryGetValue(path, out var t) && t) return t; // ảnh đã bị huỷ (thoát Play) thì đọc lại
            if (File.Exists(path))
            {
                t = new Texture2D(2, 2, TextureFormat.RGBA32, true) { wrapMode = TextureWrapMode.Clamp, filterMode = FilterMode.Trilinear };
                if (!t.LoadImage(File.ReadAllBytes(path))) t = null;
            }
            TexCache[path] = t;
            return t;
        }

        // PokiClash/PetPart (màu cộng, blend cộng); thiếu shader thì Sprites/Default (chỉ có phần nhân màu)
        static Material Mat(bool add)
        {
            var m = add ? additive : material;
            if (m) return m;
            var sh = Shader.Find("PokiClash/PetPart");
            if (sh)
            {
                m = new Material(sh);
                m.SetFloat("_SrcBlend", (float)BlendMode.SrcAlpha);
                m.SetFloat("_DstBlend", (float)(add ? BlendMode.One : BlendMode.OneMinusSrcAlpha));
            }
            else m = new Material(Shader.Find("Sprites/Default") ?? Shader.Find("Universal Render Pipeline/2D/Sprite-Unlit-Default"));
            if (add) additive = m;
            else material = m;
            return m;
        }

        // không có hình aola: một khối màu thay chỗ
        public void UsePlaceholder(float height, Color color, int sorting)
        {
            var tex = Texture2D.whiteTexture;
            var go = new GameObject("tam");
            go.transform.SetParent(transform, false);
            var sr = go.AddComponent<SpriteRenderer>();
            sr.sprite = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), new Vector2(0.5f, 0f), tex.width);
            sr.color = color;
            sr.sortingOrder = sorting;
            go.transform.localScale = new Vector3(height * 0.6f, height, 1);
            placeholder = go.transform;
        }

        public void Play(string clip, bool loopIt = false)
        {
            if (!HasAnim)
            {
                if (placeholder && clip != Idle) StartCoroutine(Punch());
                return;
            }
            if (!clips.ContainsKey(clip)) clip = Idle;
            current = clip;
            loop = loopIt;
            time = 0;
            shown = -1;
            Render();
        }

        IEnumerator Punch()
        {
            var s = placeholder.localScale;
            for (float t = 0; t < 0.25f; t += Time.deltaTime)
            {
                placeholder.localScale = s * (1 + 0.15f * Mathf.Sin(t / 0.25f * Mathf.PI));
                yield return null;
            }
            placeholder.localScale = s;
        }

        // ---------- màn trận điều khiển khung bằng tay ----------

        public bool Manual; // true: không tự chạy clip trong Update, màn trận gọi ShowFrame
        public float Fps => fps;
        public float Unit => unit; // đơn vị thế giới trên mỗi điểm ảnh clip
        public int FrameCount(string clip) => clips.TryGetValue(clip, out var c) ? c.Frames.Count : 0;
        public bool HasClip(string clip) => clips.ContainsKey(clip);

        sealed class Motion
        {
            public Vector2[] disp; // dịch chuyển thân so với khung đầu (điểm ảnh clip, y xuống), đã làm mượt 5 khung
            public int peak, hit;
        }

        readonly Dictionary<string, Motion> motion = new();

        // chép AolaAnim.prepare() của bản web: khung lao xa nhất là đỉnh lao; trúng đòn ở đỉnh lao, hoặc 60% clip (55% với chiêu)
        Motion MotionOf(string name)
        {
            if (!clips.TryGetValue(name, out var c)) return null;
            if (motion.TryGetValue(name, out var m)) return m;
            int n = c.Frames.Count;
            var raw = new Vector2?[n];
            for (int i = 0; i < n; i++)
            {
                float sx = 0, sy = 0;
                int k = 0;
                foreach (var p in c.Frames[i])
                {
                    if ((int)p[0] == shadowSprite) continue;
                    sx += p[5];
                    sy += p[6];
                    k++;
                }
                raw[i] = k > 0 ? new Vector2(sx / k, sy / k) : (Vector2?)null;
            }
            Vector2 bas = Vector2.zero;
            foreach (var r in raw)
                if (r.HasValue)
                {
                    bas = r.Value;
                    break;
                }
            var d = new Vector2[n];
            var last = Vector2.zero;
            for (int i = 0; i < n; i++) d[i] = last = raw[i].HasValue ? raw[i].Value - bas : last;
            m = new Motion { disp = new Vector2[n] };
            float best = 0;
            int bi = 0;
            for (int i = 0; i < n; i++)
            {
                Vector2 sum = Vector2.zero;
                int k = 0;
                for (int j = Mathf.Max(0, i - 2); j <= Mathf.Min(n - 1, i + 2); j++)
                {
                    sum += d[j];
                    k++;
                }
                m.disp[i] = sum / k;
                float mag = m.disp[i].magnitude;
                if (mag > best)
                {
                    best = mag;
                    bi = i;
                }
            }
            m.peak = bi;
            m.hit = best > 60 ? bi : Mathf.FloorToInt(n * (name == Skill ? 0.55f : 0.6f));
            motion[name] = m;
            return m;
        }

        public int HitFrame(string clip) => MotionOf(clip)?.hit ?? 0;
        public int PeakFrame(string clip) => MotionOf(clip)?.peak ?? 0;
        public Vector2 Disp(string clip, int fi)
        {
            var m = MotionOf(clip);
            return m == null || m.disp.Length == 0 ? Vector2.zero : m.disp[Mathf.Clamp(fi, 0, m.disp.Length - 1)];
        }

        // chiều cao dáng đứng tính bằng điểm ảnh clip (để đổi sang toạ độ sân)
        public float IdleHeightPx => loadedHeight / Mathf.Max(1e-6f, unit);
        float loadedHeight = 1;

        public void ShowFrame(string clip, int fi)
        {
            if (!HasAnim) return;
            if (!clips.ContainsKey(clip)) clip = Idle;
            if (clip != current) shown = -1;
            current = clip;
            loop = false;
            time = (Mathf.Clamp(fi, 0, clips[clip].Frames.Count - 1) + 0.5f) / fps;
            Render();
        }

        void Update()
        {
            if (!HasAnim || Manual) return;
            time += Time.deltaTime;
            var clip = clips[current];
            if (time * fps >= clip.Frames.Count)
            {
                if (loop) time %= clip.Frames.Count / fps;
                else { Play(Idle, true); return; }
            }
            Render();
        }

        void Render()
        {
            var clip = clips[current];
            int f = Mathf.Min((int)(time * fps), clip.Frames.Count - 1);
            if (f == shown) return;
            shown = f;
            var pics = clip.Frames[f];
            while (pool.Count < pics.Length) pool.Add(NewQuad());
            for (int i = 0; i < pool.Count; i++)
            {
                var (r, m, v, c) = pool[i];
                Texture2D t = i < pics.Length ? textures[(int)pics[i][0]] : null;
                if (t == null) { r.enabled = false; continue; }
                var p = pics[i];
                int k = 0;
                foreach (var q in Corners(p))
                {
                    float x = (q.x - clip.Anchor.x) * unit, y = -(q.y - clip.Anchor.y) * unit;
                    v[k++] = new Vector3(flip ? -x : x, y, 0);
                }
                var col = new Color(p[8], p[9], p[10], p[7]);
                c[0] = c[1] = c[2] = c[3] = col;
                m.vertices = v;
                m.colors = c;
                m.RecalculateBounds();
                r.sharedMaterial = Mat(p[14] > 0);
                block.SetTexture("_MainTex", t);
                block.SetColor("_Add", new Color(p[11], p[12], p[13], 0));
                r.SetPropertyBlock(block);
                r.sortingOrder = sortBase + i;
                r.enabled = true;
            }
        }

        (MeshRenderer, Mesh, Vector3[], Color[]) NewQuad()
        {
            var go = new GameObject("hinh");
            go.transform.SetParent(transform, false);
            var m = new Mesh();
            var v = new Vector3[4];
            var c = new Color[4];
            m.vertices = v;
            // đỉnh theo thứ tự góc trên trái, trên phải, dưới phải, dưới trái của ảnh
            m.uv = new[] { new Vector2(0, 1), new Vector2(1, 1), new Vector2(1, 0), new Vector2(0, 0) };
            m.triangles = new[] { 0, 1, 2, 0, 2, 3 };
            go.AddComponent<MeshFilter>().sharedMesh = m;
            var r = go.AddComponent<MeshRenderer>();
            r.sharedMaterial = Mat(false);
            return (r, m, v, c);
        }
    }
}
