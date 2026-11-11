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
using System.Threading.Tasks;
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
            public int? hitAt;                              // anim.json "hit": khung trúng khai sẵn (đòn xa thân bay nhảy nhiều, anim_thuy.py)
            public bool stay;                               // anim.json "stay": clip đứng tại chỗ, không kéo lao tới đối thủ dù thân dời xa
            public float? farRamp;                          // anim.json "far_ramp": x (điểm clip) hình ở xa được kéo trọn về đối thủ; mặc định tâm vùng xa
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
        // evolve: clip tiến hóa (chỉ dạng .atomik có), HeroViewer phát trước khi đổi sang dạng kế tiếp
        public const string Idle = "1_1", Hit = "1_2", Attack = "1_4", Cast = "1_5", Skill = "1_6", Evolve = "evolve";
        // clip ra sân, chết: chỉ rig .atomik lô quái Thủy (2026-11-11) có; hộp chi tiết có nút xem (trận chưa gọi)
        public const string Appear = "appear", Die = "die";
        // nửa sau của chiêu cuối hai clip (Tí Tách 2026-11-11): "skill" hết ở dáng đang bay, "skill_land" rơi xuống, bẹp, nảy;
        // cung nhảy giữa hai clip do code tính (AolaSticker.Jump)
        public const string SkillLand = "skill_land";

        // Dạng .atomik (AolaAnim.atomik, 2026-11-08): rig xương riêng vẽ bằng một Mesh; clip đặt tên chữ trong file
        static string AtkName(string clip) =>
            clip == Idle ? "idle" : clip == Hit ? "hit" : clip == Attack ? "attack" : clip == Cast ? "cast" : clip == Skill ? "skill" : clip;

        static readonly Dictionary<AolaAnim, Data> Cache = new();
        // đọc trước (Prewarm): animation đang đọc ở luồng phụ và atlas đang nạp không chặn; chỉ luồng chính đụng các bảng này.
        // Giữ tối đa WarmMax dạng chưa dùng tới (mở nhiều hộp chi tiết mà không tiến hóa thì dạng cũ nhất bị bỏ, khỏi phình bộ nhớ).
        const int WarmMax = 6;
        static readonly Dictionary<AolaAnim, Task<Data>> Pending = new();
        static readonly Dictionary<AolaAnim, ResourceRequest> AtlasWarm = new();
        static readonly List<AolaAnim> WarmOrder = new();
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

        // dạng .atomik: rig, tư thế, một Mesh cho cả con (sinh lúc chạy như các quad aola)
        AtomikAsset atk;
        AtomikPose apose;
        int atkMove = -1, atkShadow = -1;
        int atkFar = -1;               // xương "far": hiệu ứng ở chỗ đối thủ (dáng gốc ở chỗ đối thủ mặc định trước mặt)
        int[] atkFly = new int[0];     // xương "fly*": đạn bay từ thân tới far
        int atkAura = -1;              // clip lặp "aura" (mây bay vòng quanh Thanh Long...): phủ lên mọi clip theo đồng hồ liên tục
        MeshRenderer atkRenderer;
        Mesh atkMesh;
        // hạt vẽ không viền sticker (game.plain: hạt lá bay, lá văng; người dùng dặn bỏ viền trắng ở hạt lá, 2026-11-09). Khi nơi hiện
        // bật SplitFx (AolaSticker), các slot này dựng thành lưới riêng đặt cao FxLift trên actor; camera thứ hai của sticker chụp lưới
        // đó ra ảnh riêng, hiện không qua shader viền. Không bật (chụp thử trong Editor...): vẽ chung một lưới như cũ.
        public const float FxLift = 1000f;
        public bool SplitFx;
        public bool HasPlainFx => atk != null && atkPlain != null;
        bool[] atkPlain;
        AtomikPose.SkinPass passMain, passFx;
        MeshRenderer atkFxRenderer;
        Mesh atkFxMesh;
        Vector3[] av;
        Vector2[] au;
        Color32[] ac;

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
        public bool HasAnim => clips.Count > 0 || atk != null;
        // tăng mỗi lần hình trên màn đổi (khung khác, đổi chỗ hình xa, bật tắt bóng): sticker chỉ cho camera chụp lại khi số này đổi
        public int Version { get; private set; }
        public float Duration(string clip) => HasClip(clip) ? FrameCount(clip) / fps : 0.3f;

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
            if (a && a.atomik) return LoadAtomik(a, height);
            atk = null;
            atkPlain = null;
            if (atkRenderer) atkRenderer.enabled = false;
            if (atkFxRenderer) atkFxRenderer.enabled = false;
            var tex = a ? a.LoadAtlas() : null;
            if (a && AtlasWarm.Remove(a)) WarmOrder.Remove(a); // atlas nạp trước đã vào tay diễn viên
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

        // Dạng .atomik: một Mesh cho cả con, đỉnh tính từ xương mỗi khung (AtomikPose); gốc toạ độ rig ở chân như tâm bóng của aola.
        // Trận vẫn chạy theo khung (fps của rig, mặc định 25), khung trúng và cú lao đọc từ AtomikAsset.game.
        bool LoadAtomik(AolaAnim a, float height)
        {
            var rig = a.atomik;
            if (rig.bones == null || rig.bones.Length == 0 || rig.FindClip("idle") < 0) return false;
            anim = a;
            atk = rig;
            atlas = rig.atlas;
            data = null;
            clips = NoClips;
            shadowSprite = -1;
            apose = new AtomikPose(rig);
            av = new Vector3[apose.maxVerts];
            au = new Vector2[apose.maxVerts];
            ac = new Color32[apose.maxVerts];
            var g = rig.game;
            fps = g != null && g.fps > 0 ? g.fps : 25;
            atkMove = rig.FindBone(g != null ? g.move : "move");
            atkShadow = rig.FindSlot(g != null ? g.shadow : "shadow");
            atkFar = rig.FindBone("far");
            atkAura = rig.FindClip("aura");
            atkPlain = null;
            if (g != null && g.plain != null)
                foreach (var sn in g.plain)
                {
                    int si = rig.FindSlot(sn);
                    if (si < 0) continue;
                    atkPlain ??= new bool[rig.slots.Length];
                    atkPlain[si] = true;
                }
            passMain = apose.NewPass();
            passFx = apose.NewPass();
            var fly = new List<int>();
            for (int i = 0; i < rig.bones.Length; i++)
                if (rig.bones[i].name != null && rig.bones[i].name.StartsWith("fly")) fly.Add(i);
            atkFly = fly.ToArray();
            motion.Clear();
            float h = g != null && g.height > 0 ? g.height : AtomikTop();
            unit = height / Mathf.Max(1f, h);
            loadedHeight = height;
            block = new MaterialPropertyBlock();
            foreach (var q in pool) q.r.enabled = false;
            if (!atkRenderer)
            {
                var go = new GameObject("atomik");
                go.transform.SetParent(transform, false);
                atkMesh = new Mesh { name = "atomik_" + rig.rigName };
                atkMesh.MarkDynamic();
                go.AddComponent<MeshFilter>().sharedMesh = atkMesh;
                atkRenderer = go.AddComponent<MeshRenderer>();
            }
            Play(Idle, true);
            return true;
        }

        // đỉnh cao nhất của dáng đứng (pixel rig) khi rig chưa ghi game.height
        float AtomikTop()
        {
            apose.Sample(atk.FindClip("idle"), 0);
            apose.World();
            int n = apose.Skin(av, au, ac, 1, false, -1, out _);
            float top = 1;
            for (int i = 0; i < n; i++) top = Mathf.Max(top, av[i].y);
            return top;
        }

        int AtkClip(string clip) => atk != null ? atk.FindClip(AtkName(clip)) : -1;

        // Rig .atomik tự diễn đoạn giữ chiêu (clip có sự kiện kết thúc giữ "het_*": lô quái Thủy 2026-11-11, rung hai dáng, giữ có trôi):
        // sân và hộp chi tiết không ghìm giờ clip ở khung nhả nữa. Ghìm cứng làm cả con đứng im giữa chiêu (người dùng: "chiêu bị khựng").
        public bool SelfHold(string clip)
        {
            int ci = AtkClip(clip);
            var ev = ci >= 0 ? atk.anims[ci].ev : null;
            if (ev == null) return false;
            foreach (var e in ev)
                if (e != null && e.name != null && e.name.StartsWith("het_")) return true; // het_phun, het_gam, het_bung...
            return false;
        }

        // giờ (giây) của sự kiện `name` trong clip .atomik (vd. "cham_dat" của clip ra sân: sân rung màn lúc tướng nện đất); -1: không có
        public float EventTime(string clip, string name)
        {
            int ci = AtkClip(clip);
            var ev = ci >= 0 ? atk.anims[ci].ev : null;
            if (ev == null) return -1;
            foreach (var e in ev)
                if (e != null && e.name == name) return e.t;
            return -1;
        }

        // rig xương vẽ theo thời gian liên tục (mượt ở mọi tốc độ khung màn hình), không theo bậc 25 khung như hình aola
        float shownTime = -1, shownAura = -1;

        void RenderAtomik()
        {
            if (apose.Stale) // file .atomik vừa nhập lại khi Editor đang Play: dựng lại theo rig mới (clip, giờ do nơi gọi đặt lại)
            {
                string c = current;
                float tm = time;
                bool lp = loop;
                if (!anim || !anim.atomik || !LoadAtomik(anim, loadedHeight)) return;
                current = c;
                time = tm;
                loop = lp;
                shownTime = -1;
            }
            int ci = AtkClip(current);
            float t = ci >= 0 ? Mathf.Min(time, atk.anims[ci].dur) : 0;
            // clip lặp "aura" chạy theo giờ game (không theo clip): mây bay liền qua các lần đổi clip, kể cả khi clip chính đứng khung
            float ta = atkAura >= 0 ? Mathf.Repeat(Application.isPlaying ? Time.time : 0f, Mathf.Max(1e-3f, atk.anims[atkAura].dur)) : 0f;
            if (shown >= 0 && Mathf.Abs(t - shownTime) < 1e-4f && Mathf.Abs(ta - shownAura) < 1e-4f) return;
            shown = 1;
            shownTime = t;
            shownAura = ta;
            Version++;
            apose.Sample(ci, t);
            if (atkAura >= 0 && atkAura != ci) apose.Overlay(atkAura, ta);
            if (farTarget.HasValue && HasFar(current)) FarAtomik();
            apose.World();
            bool split = SplitFx && atkPlain != null;
            int hs = hideShadow ? atkShadow : -1;
            int nv = apose.Skin(passMain, split ? atkPlain : null, false, av, au, ac, unit, flip, hs, out bool trisChanged);
            FillMesh(atkMesh, nv, trisChanged, passMain.Tris);
            block.SetTexture("_MainTex", atlas);
            block.SetColor("_Add", Color.clear);
            ShowMesh(atkRenderer);
            if (split)
            {
                if (!atkFxRenderer)
                {
                    var go = new GameObject("atomik_fx");
                    go.transform.SetParent(transform, false);
                    go.transform.localPosition = new Vector3(0, FxLift, 0);
                    atkFxMesh = new Mesh { name = "atomik_fx_" + atk.rigName };
                    atkFxMesh.MarkDynamic();
                    go.AddComponent<MeshFilter>().sharedMesh = atkFxMesh;
                    atkFxRenderer = go.AddComponent<MeshRenderer>();
                }
                int nf = apose.Skin(passFx, atkPlain, true, av, au, ac, unit, flip, -1, out bool fxChanged);
                FillMesh(atkFxMesh, nf, fxChanged, passFx.Tris);
                ShowMesh(atkFxRenderer);
            }
            else if (atkFxRenderer) atkFxRenderer.enabled = false;
        }

        void FillMesh(Mesh m, int nv, bool trisChanged, int[] tris)
        {
            if (trisChanged)
            {
                m.Clear();
                m.SetVertices(av, 0, nv);
                m.SetUVs(0, au, 0, nv);
                m.SetColors(ac, 0, nv);
                m.SetTriangles(tris, 0, true);
            }
            else
            {
                m.SetVertices(av, 0, nv);
                m.SetColors(ac, 0, nv);
                m.RecalculateBounds();
            }
        }

        void ShowMesh(MeshRenderer r)
        {
            r.sharedMaterial = Mat(false);
            r.SetPropertyBlock(block);
            r.sortingOrder = sortBase;
            r.enabled = true;
        }

        // hiệu ứng ở xa của rig .atomik (chiêu đứng tại chỗ gọi gai đất, sét, đạn bay): xương "far" (con của root) dời từ dáng gốc
        // tới chỗ đối thủ; xương "fly*" (con của root) dời theo phần quãng đã bay từ chỗ xuất phát tới far
        void FarAtomik()
        {
            var fb = atk.bones[atkFar];
            float h = atk.game != null && atk.game.height > 0 ? atk.game.height : 1;
            float ox = farTarget.Value.x * h - fb.x, oy = farTarget.Value.y * h - fb.y;
            apose.Nudge(atkFar, ox, oy);
            foreach (int b in atkFly)
            {
                float x0 = atk.bones[b].x, span = fb.x - x0;
                float w = span > 1 ? Mathf.Clamp01((apose.LocalX(b) - x0) / span) : 1;
                apose.Nudge(b, ox * w, oy * w);
            }
        }

        // độ dời thân của clip .atomik: xương move (pixel rig, y xuống như điểm clip aola), làm mượt 5 khung như MotionOf
        Motion AtomikMotion(string name)
        {
            int ci = AtkClip(name);
            if (ci < 0) return null;
            int n = FrameCount(name);
            var d = new Vector2[n];
            Vector2 b0 = default;
            for (int i = 0; i < n; i++)
            {
                apose.Sample(ci, i / fps);
                apose.World();
                var p = apose.BonePos(atkMove);
                var v = new Vector2(p.x, -p.y);
                if (i == 0) b0 = v;
                d[i] = v - b0;
            }
            shown = -1; // tư thế trong apose đã bị đè: khung sau dựng lại
            var m = new Motion { disp = new Vector2[n] };
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
                if (m.disp[i].magnitude > best)
                {
                    best = m.disp[i].magnitude;
                    bi = i;
                }
            }
            m.peak = bi;
            var g = atk.game;
            int hi = g?.hitClips != null ? Array.IndexOf(g.hitClips, AtkName(name)) : -1;
            m.hit = hi >= 0 && g.hitTimes != null && hi < g.hitTimes.Length
                ? Mathf.Clamp(Mathf.RoundToInt(g.hitTimes[hi] * fps), 0, n - 1)
                : Mathf.FloorToInt(n * (name == Skill ? 0.55f : 0.6f));
            return m;
        }

        // anim.json (gzip) → các clip; mọi clip khớp nhau ở tâm bóng dưới chân (AolaAnim.shadow, tìm lúc nhập)
        static Data Parse(AolaAnim a)
        {
            if (Cache.TryGetValue(a, out var d) && d.source == a.source) return d;
            if (Pending.TryGetValue(a, out var task))
            {
                // đã đọc trước ở luồng phụ (Prewarm): xong thì lấy ngay, chưa xong thì chờ nốt phần còn lại
                Pending.Remove(a);
                if (!AtlasWarm.ContainsKey(a)) WarmOrder.Remove(a);
                try { d = task.Result; }
                catch (Exception) { d = null; }
            }
            else d = Read(a, a.anim ? a.anim.bytes : null, a.name);
            if (d != null) Cache[a] = d;
            return d;
        }

        static AolaAnim FormAsset(string form) =>
            Find(form, out var p, out int i) && i >= 0 && i < p.forms.Length && p.forms[i] ? p.forms[i] : null;

        static bool Parsed(AolaAnim a) => Cache.TryGetValue(a, out var d) && d.source == a.source;

        // Đọc trước dạng sắp hiện: giải nén và đọc anim.json ở luồng phụ (vài trăm KB, trên luồng chính mất cỡ trăm ms ở điện
        // thoại), nạp atlas không chặn. Hộp chi tiết gọi cho dạng của sao kế tiếp (bấm Tiến hóa không khựng), hộp chọn đội cho tướng
        // vừa chọn. Đã đọc hoặc chưa nhập: bỏ qua.
        public static void Prewarm(string form)
        {
            var a = FormAsset(form);
            if (!a || !a.anim || Parsed(a) || Pending.ContainsKey(a)) return;
            var bytes = a.anim.bytes;
            string name = a.name;
            Pending[a] = Task.Run(() => Read(a, bytes, name));
            // giữ yêu cầu nạp để atlas không bị gỡ trước khi dùng; Resources.Load sau đó lấy ngay (chưa xong thì chờ nốt)
            if (!string.IsNullOrEmpty(a.res) && !AtlasWarm.ContainsKey(a)) AtlasWarm[a] = Resources.LoadAsync<Texture2D>(a.res + "_atlas");
            WarmOrder.Remove(a);
            WarmOrder.Add(a);
            while (WarmOrder.Count > WarmMax)
            {
                var old = WarmOrder[0];
                WarmOrder.RemoveAt(0);
                Pending.Remove(old);
                AtlasWarm.Remove(old);
            }
        }

        // Dạng đã sẵn để dựng sticker không phải đọc file trên luồng chính (animation đã đọc, atlas nạp xong); chưa thì bắt đầu đọc
        // trước (Prewarm) và trả false: nơi gọi hiện chân dung tĩnh, hỏi lại mỗi khung. Dạng chưa nhập: true (TryCreate trả null ngay).
        public static bool Ready(string form)
        {
            var a = FormAsset(form);
            if (!a || !a.anim) return true;
            if (!Parsed(a))
            {
                if (!Pending.TryGetValue(a, out var task))
                {
                    Prewarm(form);
                    if (!Pending.TryGetValue(a, out task)) return true;
                }
                if (!task.IsCompleted) return false;
            }
            return !AtlasWarm.TryGetValue(a, out var req) || req.isDone;
        }

        // anim.json (gzip) → Data. Chạy được ở luồng phụ: chỉ đọc trường của AolaAnim, không gọi API Unity, không dùng mảng Quad chung.
        static Data Read(AolaAnim a, byte[] bytes, string name)
        {
            if (bytes == null) return null;
            var quad = new Vector2[4];
            Data d;
            try
            {
                string text;
                using (var z = new GZipStream(new MemoryStream(bytes), CompressionMode.Decompress))
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
                // đòn xa viết lại của đảo Thủy (tools/anim_thuy.py, 2026-11-07): thân bay lên, lộn, dậm mà vẫn là đòn đứng tại chỗ
                if (root.TryGetValue("hit", out var hv) && hv is Dictionary<string, object> hits)
                    foreach (var kv in hits)
                        if (d.clips.TryGetValue(kv.Key, out var hc)) hc.hitAt = Convert.ToInt32(kv.Value);
                if (root.TryGetValue("stay", out var sv) && sv is List<object> stays)
                    foreach (var n in stays)
                        if (d.clips.TryGetValue(Convert.ToString(n), out var sc)) sc.stay = true;
                // hình bên trái tâm vùng xa (giữa con bắn và đối thủ) cũng được kéo trọn từ điểm này: hiệu ứng bao quanh đối thủ không méo
                if (root.TryGetValue("far_ramp", out var rv) && rv is Dictionary<string, object> ramps)
                    foreach (var kv in ramps)
                        if (d.clips.TryGetValue(kv.Key, out var rc)) rc.farRamp = Convert.ToSingle(kv.Value);
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
                Debug.LogWarning($"[Aola] Không đọc được animation {name}: {e.Message}");
                return null;
            }
            if (!d.clips.TryGetValue(Idle, out var idle) || idle.Frames.Count == 0) return null;
            foreach (var clip in d.clips.Values) clip.Anchor = AnchorOf(a, clip, quad);
            d.top = float.MaxValue;
            foreach (var p in idle.Frames[0])
                if (Corners(a, p, quad))
                    foreach (var q in quad) d.top = Mathf.Min(d.top, q.y);
            return d;
        }

        static Vector2 AnchorOf(AolaAnim a, Clip clip, Vector2[] quad)
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
                if (Corners(a, p, quad))
                    foreach (var q in quad) { minX = Mathf.Min(minX, q.x); maxX = Mathf.Max(maxX, q.x); maxY = Mathf.Max(maxY, q.y); }
            return maxY > float.MinValue ? new Vector2((minX + maxX) / 2, maxY) : Vector2.zero;
        }

        // ma trận Flash: x' = a x + c y + tx, y' = b x + d y + ty (điểm ảnh, y hướng xuống)
        static Vector2 Map(float[] p, float x, float y) => new(p[1] * x + p[3] * y + p[5], p[2] * x + p[4] * y + p[6]);

        // 4 góc hình (trên trái, trên phải, dưới phải, dưới trái) theo cỡ gốc, ghi vào Quad (luồng chính); hình rỗng: false
        static bool Corners(AolaAnim a, float[] p) => Corners(a, p, Quad);

        // như trên, ghi vào mảng q riêng (đọc ở luồng phụ không được đụng Quad chung)
        static bool Corners(AolaAnim a, float[] p, Vector2[] q)
        {
            int s = (int)p[0];
            if (s < 0 || s >= a.sizes.Length) return false;
            var z = a.sizes[s];
            if (z.x <= 0 || z.y <= 0) return false;
            q[0] = Map(p, 0, 0);
            q[1] = Map(p, z.x, 0);
            q[2] = Map(p, z.x, z.y);
            q[3] = Map(p, 0, z.y);
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
            if (!HasClip(clip)) clip = Idle;
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
        public int FrameCount(string clip)
        {
            if (atk != null)
            {
                int ci = AtkClip(clip);
                return ci < 0 ? 0 : Mathf.Max(1, Mathf.RoundToInt(atk.anims[ci].dur * fps));
            }
            return clips.TryGetValue(clip, out var c) ? c.Frames.Count : 0;
        }

        public bool HasClip(string clip) => atk != null ? AtkClip(clip) >= 0 : clips.ContainsKey(clip);

        sealed class Motion
        {
            public Vector2[] disp; // dịch chuyển thân so với khung đầu (điểm ảnh clip, y xuống), đã làm mượt 5 khung
            public int peak, hit;
        }

        readonly Dictionary<string, Motion> motion = new();

        // chép AolaAnim.prepare() của bản web: khung lao xa nhất là đỉnh lao; trúng đòn ở đỉnh lao, hoặc 60% clip (55% với chiêu)
        Motion MotionOf(string name)
        {
            if (motion.TryGetValue(name, out var m)) return m;
            if (atk != null)
            {
                m = AtomikMotion(name);
                if (m != null) motion[name] = m;
                return m;
            }
            if (!clips.TryGetValue(name, out var c)) return null;
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
            m.hit = c.hitAt.HasValue ? Mathf.Clamp(c.hitAt.Value, 0, n - 1)
                : best > 60 ? bi : Mathf.FloorToInt(n * (name == Skill ? 0.55f : 0.6f));
            motion[name] = m;
            return m;
        }

        // clip có cú lao kéo tới đối thủ (AolaSticker.Lunge): đòn đánh luôn có; clip khác khi anim.json khai "lunge"
        public bool Lunges(string clip)
        {
            if (atk != null)
            {
                var g = atk.game;
                string an = AtkName(clip);
                if (g?.stay != null && Array.IndexOf(g.stay, an) >= 0) return false;
                return clip == Attack || g?.lunge != null && Array.IndexOf(g.lunge, an) >= 0;
            }
            return !(clips.TryGetValue(clip, out var c) && c.stay) && (clip == Attack || data != null && data.lunge.Contains(clip));
        }

        // clip đứng một chỗ: sân KHÔNG tự nhún tới đối thủ (người dùng 2026-11-09: đòn bắn xa không cần lao lên, đứng một chỗ bắn).
        // Rig .atomik: clip khai "stay", hoặc clip có hiệu ứng bay tới chỗ đối thủ ("far": đạn, sét, cột trồi) mà không khai lao.
        public bool Stays(string clip)
        {
            if (atk == null) return clips.TryGetValue(clip, out var c) && c.stay;
            var g = atk.game;
            string an = AtkName(clip);
            if (g?.stay != null && Array.IndexOf(g.stay, an) >= 0) return true;
            bool lunge = g?.lunge != null && Array.IndexOf(g.lunge, an) >= 0;
            return !lunge && g?.far != null && Array.IndexOf(g.far, an) >= 0;
        }

        // chiêu mana phát clip CHIÊU riêng thay vì bắn tia (số ít boss làm riêng, anim.json "mana": "clip")
        public bool ManaUsesClip => data != null && data.manaClip;

        // kiểu tia riêng của dạng (anim.json "cast.tia", StageView chọn ảnh tia cùng tên); null = tia nước thường
        public string BeamStyle => atk != null ? (string.IsNullOrEmpty(atk.game?.beamStyle) ? null : atk.game.beamStyle) : data?.beamStyle;

        // cảm giác trúng của clip (.atomik khai impact*, skill pokiclash-hero-fx): khựng (giây thật), rung (trauma 0..1), bật lùi
        // (theo chiều cao đối thủ), chớp cả màn (màu hex, rỗng = không). Dạng aola, rig không khai: false.
        public bool Impact(string clip, out float stop, out float shake, out float push, out string flash)
        {
            stop = shake = push = 0;
            flash = null;
            var g = atk != null ? atk.game : null;
            if (g == null || g.impactClips == null) return false;
            int i = Array.IndexOf(g.impactClips, AtkName(clip));
            if (i < 0) return false;
            if (g.impactStop != null && i < g.impactStop.Length) stop = g.impactStop[i];
            if (g.impactShake != null && i < g.impactShake.Length) shake = g.impactShake[i];
            if (g.impactPush != null && i < g.impactPush.Length) push = g.impactPush[i];
            if (g.impactFlash != null && i < g.impactFlash.Length) flash = g.impactFlash[i];
            return true;
        }

        // chiêu bắn tia: chỗ bắn so với tâm bóng dưới chân của clip đứng (điểm clip, y xuống) và cỡ tia của dạng; không khai: false
        public bool Beam(out Vector2 muzzle, out float scale)
        {
            muzzle = default;
            scale = 1;
            if (atk != null)
            {
                var g = atk.game;
                if (g?.muzzle == null || g.muzzle.Length < 2 || !HasClip(Cast)) return false;
                muzzle = new Vector2(g.muzzle[0], -g.muzzle[1]); // rig y lên, gốc ở chân → điểm clip y xuống
                scale = g.beam > 0 ? g.beam : 1;
                return true;
            }
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

        public bool HasFar(string clip) => atk != null
            ? atkFar >= 0 && atk.game?.far != null && Array.IndexOf(atk.game.far, AtkName(clip)) >= 0
            : HasAnim && clips.TryGetValue(clip, out var c) && FarOf(c).hasFar;

        // chỗ đối thủ so với chân (chiều cao dáng đứng; trước mặt là +x, lên là +y): hiệu ứng ở xa vẽ về đó; null: như bản gốc
        Vector2? farTarget;

        public void SetFarTarget(Vector2? t)
        {
            if (t == farTarget) return;
            farTarget = t;
            shown = -1;
        }
        float loadedHeight = 1;

        // Hiện clip ở giây t (sân đấu, ô xem tướng): rig .atomik dựng đúng thời điểm đó; hình aola lấy khung floor(t·fps) như cũ.
        public void ShowTime(string clip, float t, bool loopClip)
        {
            if (!HasAnim) return;
            if (!HasClip(clip)) clip = Idle;
            int n = Mathf.Max(1, FrameCount(clip));
            if (atk == null)
            {
                int i = Mathf.FloorToInt(t * fps);
                ShowFrame(clip, loopClip ? ((i % n) + n) % n : Mathf.Clamp(i, 0, n - 1));
                return;
            }
            if (clip != current) shown = -1;
            current = clip;
            loop = false;
            float len = n / fps;
            time = loopClip ? Mathf.Repeat(t, len) : Mathf.Clamp(t, 0, len);
            Render();
        }

        public void ShowFrame(string clip, int fi)
        {
            if (!HasAnim) return;
            if (!HasClip(clip)) clip = Idle;
            if (clip != current) shown = -1;
            current = clip;
            loop = false;
            time = (Mathf.Clamp(fi, 0, FrameCount(clip) - 1) + 0.5f) / fps;
            Render();
        }

        void Update()
        {
            if (!HasAnim || Manual) return;
            time += Time.deltaTime;
            int count = FrameCount(current);
            if (time * fps >= count)
            {
                if (loop) time %= count / fps;
                else { Play(Idle, true); return; }
            }
            Render();
        }

        void Render()
        {
            if (atk != null)
            {
                RenderAtomik();
                return;
            }
            var clip = clips[current];
            int f = Mathf.Min((int)(time * fps), clip.Frames.Count - 1);
            if (f == shown) return;
            shown = f;
            Version++;
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
                    float end = clip.farRamp.HasValue ? Mathf.Min(clip.farRamp.Value - clip.Anchor.x, clip.farCenter.x) : clip.farCenter.x;
                    if (d > r0 && end > r0)
                    {
                        float w = Mathf.Clamp01((d - r0) / (end - r0));
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
            if (atkMesh) Destroy(atkMesh);
            if (atkFxMesh) Destroy(atkFxMesh);
        }
    }
}
