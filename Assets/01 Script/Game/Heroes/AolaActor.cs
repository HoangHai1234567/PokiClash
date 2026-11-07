// Diễn viên tướng aola: component gốc của prefab tướng (Assets/04 Prefabs/Heroes/<id>.prefab, mỗi prefab một dòng tiến hóa,
// forms theo thứ tự dạng). Hình, chân dung, animation là asset AolaAnim trong Assets/03 Art/Heroes/Resources/<dạng>/, nhập từ
// AolaRipper bằng menu PokiClash/Tướng/Nhập hình tướng aola (Editor/AolaImport); atlas nạp khi nạp dạng. Hình gốc của
// Baitian, chỉ dùng trong bản thử.
// Mỗi hình là một quad, đỉnh tính từ ma trận Flash của khung (có cả nghiêng), nên một Transform thường không đủ. Mọi hình của
// một dạng nằm chung một atlas. Quad, Mesh, Material sinh lúc chạy gói trong file này (ngoại lệ của test chặn prefab).
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using PokiClash.Core;
using PokiClash.UI;
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
            public bool farReady, hasFar;                   // FarOf đã tính; clip có hiệu ứng vẽ ở xa (chỗ đối thủ của bản gốc)
            public Vector2 farCenter;                       // tâm vùng hiệu ứng ở xa (điểm clip so với Anchor, y xuống)
            public Vector2? farAt;                          // anim.json "far_center": tâm vùng xa khai sẵn (điểm clip, y xuống)
        }

        // Hiệu ứng ở xa (người dùng 2026-11-03: Tiểu Y thiếu animation so với bản gốc): đòn bắn từ xa của aola vẽ đạn bay và vụ nổ
        // ở chỗ đối thủ đứng trong trận gốc, cách chân 3-7 lần chiều cao dáng đứng, ngoài khung camera của sticker (±1,7 lần).
        // Hình có tâm cách chân (về phía trước) quá FarStart lần chiều cao là hiệu ứng ở xa: không tính vào cú lao của thân; khi
        // có FarTarget (chỗ đối thủ trên sân), hình từ FarRamp lần chiều cao trở ra được kéo dần về đó (tâm vùng xa trùng FarTarget).
        const float FarStart = 1.5f, FarRamp = 1f;

        // animation đã đọc của một dạng, dùng chung cho mọi diễn viên cùng dạng
        sealed class Data
        {
            public string source;
            public float fps = 25, top; // top: mép trên khung đầu dáng đứng (điểm clip)
            public readonly Dictionary<string, Clip> clips = new();
            public readonly HashSet<string> lunge = new(); // clip ngoài đòn đánh cũng lao tới đối thủ (anim.json "lunge")
            public Vector2? muzzle; // chỗ bắn tia ở khung trúng của clip bắn (điểm clip, anim.json "cast")
            public float beam = 1; // cỡ tia của dạng này
            public string beamStyle; // anim.json "cast.tia": ảnh tia riêng (tia_bang, tia_xoay, tia_trieu: 3 boss cuối đảo Thủy), rỗng = tia nước thường
            public bool manaClip; // anim.json "mana": "clip": chiêu mana phát clip CHIÊU riêng (boss làm riêng), không bắn tia
            public HashSet<int> idleSprites; // hình có trong dáng đứng (thân): không bao giờ là hiệu ứng ở xa
        }

        // 1_5 (bắn): clip ngắn của chiêu bắn tia (aola tools/anim_moi.py dựng), chỉ dạng có khai "cast" mới có
        public const string Idle = "1_1", Hit = "1_2", Attack = "1_4", Cast = "1_5", Skill = "1_6";

        static readonly Dictionary<AolaAnim, Data> Cache = new();
        static readonly Dictionary<string, Clip> NoClips = new();
        static readonly Vector2[] Quad = new Vector2[4];
        static Material material, additive;

        [SerializeField] AolaAnim[] forms = new AolaAnim[0]; // các dạng theo thứ tự tiến hóa (HeroDef.forms)

        AolaAnim anim;
        Texture2D atlas;
        Data data;
        Dictionary<string, Clip> clips = NoClips;
        readonly List<(MeshRenderer r, Mesh m, Vector3[] v, Vector2[] u, Color[] c)> pool = new();
        MaterialPropertyBlock block;
        float fps = 25, unit = 0.01f, time;
        int shadowSprite = -1;
        bool flip, loop = true;
        int sortBase, shown = -1;
        string current = Idle;
        Transform placeholder;

        public AolaAnim[] Forms => forms;

        // không vẽ bóng dưới chân (màn boot: luật UI không vẽ bóng); đổi thì vẽ lại khung
        bool hideShadow;
        public bool HideShadow
        {
            get => hideShadow;
            set
            {
                hideShadow = value;
                shown = -1;
            }
        }
        public bool HasAnim => clips.Count > 0;
        public float Duration(string clip) => clips.TryGetValue(clip, out var c) ? c.Frames.Count / fps : 0.3f;

        // Dùng khi nhập (Editor).
        public void Setup(AolaAnim[] heroForms) => forms = heroForms;

        // Prefab tướng có dạng tên form (HeroForm.aola), tra trong UiAssets.heroes. Chưa nhập: false.
        public static bool Find(string form, out AolaActor prefab, out int formIndex)
        {
            prefab = null;
            formIndex = -1;
            var lib = Theme.Assets ? Theme.Assets.heroes : null;
            return lib && lib.Find(form, out prefab, out formIndex);
        }

        // Chân dung tĩnh của dạng (tools/portrait_png.py của AolaRipper): khung 4:5 như HeroArt, chân ở giữa và cách đáy
        // HeroArt.FootY. Chưa nhập: null.
        public static Sprite Portrait(string form) => Find(form, out var p, out int i) && p.forms[i] ? p.forms[i].LoadPortrait() : null;

        // Nạp dạng thứ i của prefab. height = chiều cao dáng đứng (đơn vị thế giới); flip = lật ngang
        public bool LoadForm(int i, float height, bool flipX, int sorting) =>
            i >= 0 && i < forms.Length && Load(forms[i], height, flipX, sorting);

        public bool Load(AolaAnim a, float height, bool flipX, int sorting)
        {
            flip = flipX;
            sortBase = sorting;
            var tex = a ? a.LoadAtlas() : null;
            var d = tex ? Parse(a) : null;
            if (d == null) return false;
            anim = a;
            atlas = tex;
            clips = d.clips;
            data = d;
            fps = d.fps;
            shadowSprite = a.shadow;
            motion.Clear();
            unit = height / Mathf.Max(1f, clips[Idle].Anchor.y - d.top);
            loadedHeight = height;
            block = new MaterialPropertyBlock();
            Play(Idle, true);
            return true;
        }

        // anim.json (gzip) → các clip; mọi clip khớp nhau ở tâm bóng dưới chân (AolaAnim.shadow, tìm lúc nhập)
        static Data Parse(AolaAnim a)
        {
            if (Cache.TryGetValue(a, out var d) && d.source == a.source) return d;
            try
            {
                string text;
                using (var z = new GZipStream(new MemoryStream(a.anim.bytes), CompressionMode.Decompress))
                using (var sr = new StreamReader(z)) text = sr.ReadToEnd();
                var root = (Dictionary<string, object>)MiniJson.Parse(text);
                d = new Data { source = a.source, fps = Convert.ToSingle(root["fps"]) };
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
                    d.clips[kv.Key] = clip;
                }
                d.manaClip = root.TryGetValue("mana", out var mc) && Convert.ToString(mc) == "clip";
                // tâm hiệu ứng ở xa khai sẵn (aola anim_moi.py "far"): đạn bay dọc đường không kéo tâm lệch về phía con bắn
                if (root.TryGetValue("far_center", out var fcv) && fcv is Dictionary<string, object> fcs)
                    foreach (var kv in fcs)
                        if (d.clips.TryGetValue(kv.Key, out var fc) && kv.Value is List<object> fp && fp.Count >= 2)
                            fc.farAt = new Vector2(Convert.ToSingle(fp[0]), Convert.ToSingle(fp[1]));
                if (root.TryGetValue("lunge", out var lv) && lv is List<object> ls)
                    foreach (var n in ls) d.lunge.Add(Convert.ToString(n));
                if (root.TryGetValue("cast", out var cv) && cv is Dictionary<string, object> cast &&
                    cast.TryGetValue("muzzle", out var mv) && mv is List<object> mz && mz.Count >= 2)
                {
                    d.muzzle = new Vector2(Convert.ToSingle(mz[0]), Convert.ToSingle(mz[1]));
                    if (cast.TryGetValue("beam", out var bv)) d.beam = Convert.ToSingle(bv);
                    if (cast.TryGetValue("tia", out var tv)) d.beamStyle = Convert.ToString(tv);
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning($"[Aola] Không đọc được animation {a.name}: {e.Message}");
                return null;
            }
            if (!d.clips.TryGetValue(Idle, out var idle) || idle.Frames.Count == 0) return null;
            foreach (var clip in d.clips.Values) clip.Anchor = AnchorOf(a, clip);
            d.top = float.MaxValue;
            foreach (var p in idle.Frames[0])
                if (Corners(a, p))
                    foreach (var q in Quad) d.top = Mathf.Min(d.top, q.y);
            Cache[a] = d;
            return d;
        }

        static Vector2 AnchorOf(AolaAnim a, Clip clip)
        {
            var frame = clip.Frames.Count > 0 ? clip.Frames[0] : new float[0][];
            if (a.shadow >= 0 && a.shadow < a.sizes.Length)
                foreach (var p in frame)
                    if ((int)p[0] == a.shadow)
                    {
                        var s = a.sizes[a.shadow];
                        return Map(p, s.x / 2f, s.y / 2f);
                    }
            // không có bóng: lấy giữa đáy của khung đầu
            float minX = float.MaxValue, maxX = float.MinValue, maxY = float.MinValue;
            foreach (var p in frame)
                if (Corners(a, p))
                    foreach (var q in Quad) { minX = Mathf.Min(minX, q.x); maxX = Mathf.Max(maxX, q.x); maxY = Mathf.Max(maxY, q.y); }
            return maxY > float.MinValue ? new Vector2((minX + maxX) / 2, maxY) : Vector2.zero;
        }

        // ma trận Flash: x' = a x + c y + tx, y' = b x + d y + ty (điểm ảnh, y hướng xuống)
        static Vector2 Map(float[] p, float x, float y) => new(p[1] * x + p[3] * y + p[5], p[2] * x + p[4] * y + p[6]);

        // 4 góc hình (trên trái, trên phải, dưới phải, dưới trái) theo cỡ gốc, ghi vào Quad; hình rỗng: false
        static bool Corners(AolaAnim a, float[] p)
        {
            int s = (int)p[0];
            if (s < 0 || s >= a.sizes.Length) return false;
            var z = a.sizes[s];
            if (z.x <= 0 || z.y <= 0) return false;
            Quad[0] = Map(p, 0, 0);
            Quad[1] = Map(p, z.x, 0);
            Quad[2] = Map(p, z.x, z.y);
            Quad[3] = Map(p, 0, z.y);
            return true;
        }

        // PokiClash/PetPart (màu cộng, blend cộng); thiếu shader thì Sprites/Default (chỉ có phần nhân màu)
        static Material Mat(bool add)
        {
            var m = add ? additive : material;
            if (m) return m;
            // bản build chỉ có shader nào được material tham chiếu: lấy qua UiAssets.petPart, Editor thì tìm theo tên cũng được
            var sh = Theme.Assets && Theme.Assets.petPart ? Theme.Assets.petPart.shader : Shader.Find("PokiClash/PetPart");
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
                    if ((int)p[0] == shadowSprite || FarPiece(c, p, out _)) continue;
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

        // clip có cú lao kéo tới đối thủ (AolaSticker.Lunge): đòn đánh luôn có; clip khác khi anim.json khai "lunge"
        public bool Lunges(string clip) => clip == Attack || data != null && data.lunge.Contains(clip);

        // chiêu mana phát clip CHIÊU riêng thay vì bắn tia (số ít boss làm riêng, anim.json "mana": "clip")
        public bool ManaUsesClip => data != null && data.manaClip;

        // kiểu tia riêng của dạng (anim.json "cast.tia", StageView chọn ảnh tia cùng tên); null = tia nước thường
        public string BeamStyle => data?.beamStyle;

        // chiêu bắn tia: chỗ bắn so với tâm bóng dưới chân của clip đứng (điểm clip, y xuống) và cỡ tia của dạng; không khai: false
        public bool Beam(out Vector2 muzzle, out float scale)
        {
            muzzle = default;
            scale = 1;
            if (data?.muzzle == null || !clips.ContainsKey(Cast)) return false;
            muzzle = data.muzzle.Value - clips[Idle].Anchor;
            scale = data.beam;
            return true;
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

        // hình p của clip c là hiệu ứng ở xa (hình không có trong dáng đứng, tâm quá FarStart lần chiều cao về phía trước: thân
        // của con lao cận chiến không tính); rel: tâm hình so với Anchor (điểm clip, y xuống, trước mặt là +x)
        bool FarPiece(Clip c, float[] p, out Vector2 rel)
        {
            rel = default;
            if (data == null) return false;
            if (data.idleSprites == null)
            {
                data.idleSprites = new HashSet<int>();
                if (clips.TryGetValue(Idle, out var idle))
                    foreach (var f in idle.Frames)
                        foreach (var q in f)
                            data.idleSprites.Add((int)q[0]);
            }
            if (data.idleSprites.Contains((int)p[0]) || !Corners(anim, p)) return false;
            rel = (Quad[0] + Quad[1] + Quad[2] + Quad[3]) * 0.25f - c.Anchor;
            return rel.x > FarStart * IdleHeightPx;
        }

        Clip FarOf(Clip c)
        {
            if (c.farReady) return c;
            c.farReady = true;
            float x0 = float.MaxValue, y0 = float.MaxValue, x1 = float.MinValue, y1 = float.MinValue;
            foreach (var f in c.Frames)
                foreach (var p in f)
                    if (FarPiece(c, p, out var r))
                    {
                        x0 = Mathf.Min(x0, r.x);
                        x1 = Mathf.Max(x1, r.x);
                        y0 = Mathf.Min(y0, r.y);
                        y1 = Mathf.Max(y1, r.y);
                    }
            c.hasFar = x1 >= x0;
            if (c.hasFar) c.farCenter = c.farAt.HasValue ? c.farAt.Value - c.Anchor : new Vector2((x0 + x1) / 2, (y0 + y1) / 2);
            return c;
        }

        public bool HasFar(string clip) => HasAnim && clips.TryGetValue(clip, out var c) && FarOf(c).hasFar;

        // chỗ đối thủ so với chân (chiều cao dáng đứng; trước mặt là +x, lên là +y): hiệu ứng ở xa vẽ về đó; null: như bản gốc
        Vector2? farTarget;

        public void SetFarTarget(Vector2? t)
        {
            if (t == farTarget) return;
            farTarget = t;
            shown = -1;
        }
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
            bool far = farTarget.HasValue && FarOf(clip).hasFar;
            float hp = IdleHeightPx, r0 = FarRamp * hp;
            for (int i = 0; i < pool.Count; i++)
            {
                var (r, m, v, u, c) = pool[i];
                if (i >= pics.Length || (hideShadow && (int)pics[i][0] == shadowSprite) || !Corners(anim, pics[i])) { r.enabled = false; continue; }
                var p = pics[i];
                // hiệu ứng ở xa: kéo dần về chỗ đối thủ (đạn bay giữa đường co lại theo)
                var sh = Vector2.zero;
                if (far && data.idleSprites != null && !data.idleSprites.Contains((int)p[0]))
                {
                    float d = (Quad[0].x + Quad[1].x + Quad[2].x + Quad[3].x) * 0.25f - clip.Anchor.x;
                    if (d > r0 && clip.farCenter.x > r0)
                    {
                        float w = Mathf.Clamp01((d - r0) / (clip.farCenter.x - r0));
                        sh = w * (new Vector2(farTarget.Value.x * hp, -farTarget.Value.y * hp) - clip.farCenter);
                    }
                }
                for (int k = 0; k < 4; k++)
                {
                    float x = (Quad[k].x + sh.x - clip.Anchor.x) * unit, y = -(Quad[k].y + sh.y - clip.Anchor.y) * unit;
                    v[k] = new Vector3(flip ? -x : x, y, 0);
                }
                // chỗ hình trong atlas, góc theo thứ tự như Quad (ảnh trong Unity gốc dưới trái)
                var uv = anim.uvs[(int)p[0]];
                u[0] = new Vector2(uv.xMin, uv.yMax);
                u[1] = new Vector2(uv.xMax, uv.yMax);
                u[2] = new Vector2(uv.xMax, uv.yMin);
                u[3] = new Vector2(uv.xMin, uv.yMin);
                var col = new Color(p[8], p[9], p[10], p[7]);
                c[0] = c[1] = c[2] = c[3] = col;
                m.vertices = v;
                m.uv = u;
                m.colors = c;
                m.RecalculateBounds();
                r.sharedMaterial = Mat(p[14] > 0);
                block.SetTexture("_MainTex", atlas);
                block.SetColor("_Add", new Color(p[11], p[12], p[13], 0));
                r.SetPropertyBlock(block);
                r.sortingOrder = sortBase + i;
                r.enabled = true;
            }
        }

        (MeshRenderer, Mesh, Vector3[], Vector2[], Color[]) NewQuad()
        {
            var go = new GameObject("hinh");
            go.transform.SetParent(transform, false);
            var m = new Mesh();
            var v = new Vector3[4];
            var u = new Vector2[4];
            var c = new Color[4];
            // đỉnh theo thứ tự góc trên trái, trên phải, dưới phải, dưới trái của ảnh; UV đặt theo hình mỗi khung (Render)
            m.vertices = v;
            m.uv = u;
            m.triangles = new[] { 0, 1, 2, 0, 2, 3 };
            go.AddComponent<MeshFilter>().sharedMesh = m;
            var r = go.AddComponent<MeshRenderer>();
            r.sharedMaterial = Mat(false);
            return (r, m, v, u, c);
        }

        void OnDestroy()
        {
            foreach (var q in pool)
                if (q.m) Destroy(q.m);
        }
    }
}
