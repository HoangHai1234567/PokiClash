// Chạy animation tướng xuất từ dự án aola (reskin/<tên>/export/anim.json). CHỈ DÙNG TRONG BẢN THỬ: hình gốc của Baitian.
// PNG đọc thẳng từ ổ đĩa lúc chạy, không chép vào Assets. Mỗi hình là một quad, đỉnh tính từ ma trận Flash của khung
// (có cả nghiêng), nên một Transform thường không đủ.
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace PokiWar.BanThu
{
    public sealed class AolaActor : MonoBehaviour
    {
        sealed class Clip
        {
            public readonly List<float[][]> Frames = new(); // mỗi hình: sprite, a, b, c, d, tx, ty, alpha
            public Vector2 Anchor;                          // tâm bóng dưới chân ở khung đầu, điểm khớp giữa các clip
        }

        public const string Idle = "1_1", Hit = "1_2", Attack = "1_4", Skill = "1_6";

        static readonly Dictionary<string, Texture2D> TexCache = new();
        static Material material;

        readonly Dictionary<string, Clip> clips = new();
        readonly List<Texture2D> textures = new();
        readonly List<(MeshRenderer r, Mesh m, Vector3[] v, Color[] c)> pool = new();
        MaterialPropertyBlock block;
        float fps = 25, unit = 0.01f, time;
        bool flip, loop = true;
        int sortBase, shown = -1;
        string current = Idle;
        Transform placeholder;

        public bool HasAnim => clips.Count > 0;
        public float Duration(string clip) => clips.TryGetValue(clip, out var c) ? c.Frames.Count / fps : 0.3f;

        // dir = reskin/<tên>; height = chiều cao dáng đứng (đơn vị thế giới); flip = lật ngang
        public bool Load(string dir, float height, bool flipX, int sorting)
        {
            flip = flipX;
            sortBase = sorting;
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
                            var f = new float[8];
                            for (int k = 0; k < 8; k++) f[k] = Convert.ToSingle(row[k]);
                            pics[i] = f;
                        }
                        clip.Frames.Add(pics);
                    }
                    clips[kv.Key] = clip;
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning($"[BanThu] Không đọc được {path}: {e.Message}");
                clips.Clear();
                return false;
            }
            if (!clips.ContainsKey(Idle)) { clips.Clear(); return false; }

            // hình vẽ trước tiên (xa nhất) của khung đầu dáng đứng là bóng dưới chân; mọi clip khớp nhau ở tâm bóng
            int shadow = (int)clips[Idle].Frames[0][0][0];
            foreach (var clip in clips.Values) clip.Anchor = AnchorOf(clip, shadow);
            float top = float.MaxValue;
            foreach (var p in clips[Idle].Frames[0])
                foreach (var q in Corners(p)) top = Mathf.Min(top, q.y);
            unit = height / Mathf.Max(1f, clips[Idle].Anchor.y - top);

            block = new MaterialPropertyBlock();
            Play(Idle, true);
            return true;
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
            if (TexCache.TryGetValue(path, out var t)) return t;
            if (File.Exists(path))
            {
                t = new Texture2D(2, 2, TextureFormat.RGBA32, true) { wrapMode = TextureWrapMode.Clamp, filterMode = FilterMode.Trilinear };
                if (!t.LoadImage(File.ReadAllBytes(path))) t = null;
            }
            TexCache[path] = t;
            return t;
        }

        static Material Mat()
        {
            if (material) return material;
            var sh = Shader.Find("Sprites/Default") ?? Shader.Find("Universal Render Pipeline/2D/Sprite-Unlit-Default");
            material = new Material(sh);
            return material;
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

        void Update()
        {
            if (!HasAnim) return;
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
                var col = new Color(1, 1, 1, p[7]);
                c[0] = c[1] = c[2] = c[3] = col;
                m.vertices = v;
                m.colors = c;
                m.RecalculateBounds();
                block.SetTexture("_MainTex", t);
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
            r.sharedMaterial = Mat();
            return (r, m, v, c);
        }
    }
}
