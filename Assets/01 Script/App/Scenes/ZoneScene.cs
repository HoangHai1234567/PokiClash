// Đảo hệ (chép zoneScreen của Web/src/view/screens/zone.ts): bản đồ đảo (ArtGen/Islands/compose_islands.py) cuộn dọc.
// Khung thông tin trên (hệ, cấp đề nghị, độ khó, tiến độ, rương mốc, gợi ý hệ khắc), khung ải tiếp theo dưới.
// Trong một đảo ải mở lần lượt. args = Elem, hoặc ZoneArgs (mở luôn hộp chuẩn bị của một ải).
// Prefab màn hình Assets/04 Prefabs/Screens/Zone dùng cho cả 5 đảo: màu biển, ảnh đảo, chữ gán lúc chạy; bệ ải (Items/BeAi),
// chấm ải (Items/ChamAi), vệt đường (Items/VetDuong), địch ải tiếp (Items/DichAi) sinh theo dữ liệu.
// - Đảo 8 ải: bản đồ rộng 1,27 màn, mỗi ải một bệ (ZoneNode) ở điểm ải của ảnh đảo; tướng chính của ải (Teams.StageLead) đứng trên
//   bệ, bảng tên phía ngoài khúc cua. Rương mốc ở 4 và 8 ải.
// - Đảo 70 ải (Islands.IsLong): 10 ải tướng là bệ, ải xen giữa là chấm nhỏ (ZonePip) rải đều giữa hai bệ. Rương mốc mỗi 10 ải, đặt
//   theo tỉ lệ trên thanh tiến độ.
// Chạm bệ hay chấm mở hộp Chuẩn bị trận của đúng ải đó (địch, lực chiến, thưởng); ải chưa mở cũng xem được, chỉ khoá nút Xuất trận
// (người dùng bỏ bảng chặng liệt kê cả chặng, 2026-11-03; Dialogs/BangChang để lại, không mở nữa).
// Nhãn AFK (Items/NhanAfk) dưới ải đội đang AFK (Afk.Stage); hộp chuẩn bị gọi PlaceAfkTag khi người chơi chọn ải AFK khác.
//   - Có bản đồ dài (ZoneDef.path, ArtGen/Islands/build_zone70.py): bản đồ rộng 1,27 màn như đảo 8 ải; đường mòn là tâm con đường
//     cát của ảnh; bệ cỡ thật đặt ở bãi của ảnh (ZoneDef.stops), bảng tên ngược phía địa danh (ZoneDef.plates).
//   - Chưa có: bản đồ rộng 3 màn; đường mòn cong qua các điểm ải của ảnh 8 ải (Catmull-Rom như nét vẽ tay của web), bệ thu nhỏ 0,75.
// Không hiện tướng của người chơi trên bản đồ (người dùng bỏ sticker đội trưởng cạnh ải đang đánh, 2026-11-02).
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ZoneArgs
    {
        public Elem zone;
        public int prep; // số ải cần mở hộp chuẩn bị (0 = không)
    }

    public sealed class ZoneScene : SceneRoot
    {
        public static Elem LastZone = Elem.Thuy;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)] // Play không reload domain
        static void ResetStatics() => LastZone = Elem.Thuy;
        // bản đồ phóng to và cuộn dọc, để ải ở hai đầu không bị khung trên dưới che; đảo 70 ải chưa có bản đồ dài thì phóng to hơn
        // cho đủ chỗ chấm ải
        public const float MK = 1.27f, MKLong = 3f, PadT = 260, PadB = 330;
        // đảo 70 ải: cỡ bệ ải tướng so với đảo 8 ải (đường mòn qua ảnh 8 ải chật nên thu nhỏ; bản đồ dài đủ chỗ cho bệ cỡ thật)
        const float LongNodeScale = 0.75f, PathNodeScale = 1f;

        // rương mốc trên thanh tiến độ: ảnh, nhận chạm, lắc khi mở được
        [Serializable]
        public struct Chest
        {
            public Image image;
            public ClickCatcher click;
            public Wobble wobble;
        }

        [Serializable]
        public struct Parts
        {
            [Header("Bản đồ")]
            public Image sea, map;
            public ScrollRect scroll;
            public RectTransform content, pathLayer, nodeLayer;

            [Header("Khung thông tin")]
            public UiElemTag elem;
            public TextMeshProUGUI level, count, desc;
            public DifficultyTag diff;
            public ZoneProgressBar bar;
            public Chest[] chests;

            [Header("Khung ải tiếp theo")]
            public GameObject next, done;
            public TextMeshProUGUI nextTitle, reward, doneTitle;
            public RectTransform enemies;
            public SketchButton fight;
        }

        [SerializeField] Parts p;
        [SerializeField] ZoneNode nodePrefab;
        [SerializeField] Image dashPrefab;
        [SerializeField] ZoneEnemy enemyPrefab;
        [SerializeField] ZoneChestDialog chestPrefab;
        [Tooltip("Chấm ải xen giữa của đảo 70 ải (Items/ChamAi)")]
        [SerializeField] ZonePip pipPrefab;
        [Tooltip("Bảng chặng của đảo 70 ải (Dialogs/BangChang), không mở nữa")]
        [SerializeField] ZoneChapterDialog chapterPrefab;
        [Tooltip("Biển cuộn theo bản đồ (con đầu của noi_dung, menu Đảo sảnh: ghép ảnh, kéo, mây viền); trống thì chỉ có biển nền")]
        [SerializeField] Image seaScroll;
        [Tooltip("Lớp phần động trên ảnh bản đồ (con của ảnh bản đồ, menu Đảo sảnh: ghép ảnh, kéo, mây viền)")]
        [SerializeField] IslandAnim mapAnim;
        [Tooltip("Nhãn AFK dưới ải đội đang AFK (Items/NhanAfk, menu PokiClash/Prefab/AFK theo ải)")]
        [SerializeField] RectTransform afkTagPrefab;

        Elem zone = Elem.Thuy;
        float mapW, mapH;
        bool entered;
        readonly Dictionary<int, Vector2> afkAt = new Dictionary<int, Vector2>(); // chỗ nhãn AFK của từng ải (id) trên bản đồ
        RectTransform afkTag;

        public override string Title => App.Data.Zone(zone)?.name ?? "Đảo";

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, ZoneNode node, Image dash, ZoneEnemy enemy, ZoneChestDialog chest)
        {
            p = parts;
            nodePrefab = node;
            dashPrefab = dash;
            enemyPrefab = enemy;
            chestPrefab = chest;
        }

        public override void Enter(object args)
        {
            int prep = 0;
            if (args is Elem e) zone = e;
            else if (args is ZoneArgs za)
            {
                zone = za.zone;
                prep = za.prep;
            }
            else zone = LastZone;
            LastZone = zone;
            var z = App.Data.Zone(zone);
            App.Bars.SetTitle(z.name);

            // biển: ảnh biển lặp (sea_tile) nếu có, ảnh đảo trong suốt ngoài bờ nằm trên; chưa có thì màu biển của đảo
            var seaTile = App.Art ? App.Art.Get("sea_tile") : null;
            foreach (var img in new[] { p.sea, seaScroll })
            {
                if (!img) continue;
                if (!seaTile)
                {
                    img.color = Theme.Hex(z.sea);
                    continue;
                }
                img.sprite = seaTile;
                img.type = Image.Type.Tiled;
                img.color = Color.white;
            }
            var sprite = App.Art ? App.Art.Get(z.art) : null;
            float aspect = sprite ? sprite.rect.width / sprite.rect.height : PokiCanvas.RefW / PokiCanvas.RefH;
            mapW = PokiCanvas.RefW * (Islands.IsLong(zone) && !HasPath(z) ? MKLong : MK);
            mapH = mapW / aspect;
            p.content.sizeDelta = new Vector2(0, PadT + mapH + PadB);
            p.map.name = "anh_" + z.art;
            Theme.SetSprite(p.map, sprite);
            p.map.rectTransform.sizeDelta = new Vector2(mapW, mapH);
            if (mapAnim) mapAnim.Bind(z.art);

            entered = true;
            Render();
            if (prep > 0) StartCoroutine(PrepLater(prep));
        }

        IEnumerator PrepLater(int id)
        {
            yield return new WaitForSecondsRealtime(0.25f);
            StagePrep.Open(id);
        }

        public override void Refresh() => Render();

        Vector2 NodePos(Pt pt) => new Vector2((float)pt.x * mapW, -(float)pt.y * mapH); // trong khung ảnh, gốc trên trái

        void Render()
        {
            if (!entered) return;
            var d = App.Data;
            var s = App.Save.Data;
            var z = d.Zone(zone);
            var stages = d.ZoneStages(zone).ToList();
            int prog = s.zones[(int)zone];
            Clear(p.pathLayer);
            Clear(p.nodeLayer);
            afkAt.Clear();
            afkTag = null;
            var focus = Islands.IsLong(zone) ? RenderTrail(z, d, s, stages, prog) : RenderNodes(z, d, s, stages, prog);
            PlaceAfkTag();
            ShowInfo(z, s, prog);
            ShowBottom(z, s);
            StartCoroutine(ScrollToCurrent(focus));
        }

        // đảo 8 ải: mỗi ải một bệ tại điểm ải của ảnh đảo; trả chỗ ải đang đánh (để cuộn tới)
        Vector2 RenderNodes(ZoneDef z, GameData d, SaveData s, List<StageDef> stages, int prog)
        {
            // đường đã đi: nét chấm vàng viền mực nối các ải đã qua tới ải đang đánh
            var pts = z.nodes.Select(NodePos).ToList();
            int last = pts.Count - 1;
            for (int i = 0; i < Mathf.Min(prog, last); i++) Dashes(pts[i], pts[i + 1]);

            // vẽ ải trên cao trước, ải thấp sau (đứng đè lên), cho có chiều sâu
            foreach (int i in Enumerable.Range(0, stages.Count).OrderByDescending(k => pts[k].y))
            {
                var stage = stages[i];
                SpawnNode(d, s, stage, pts[i], PlateSide(pts, i), () => StagePrep.Open(stage.id));
            }
            return pts[Mathf.Min(last, prog)];
        }

        // nhãn AFK dưới ải đội đang AFK (ải chọn hoặc ải tự chọn), nếu ải đó ở đảo này; gọi lại khi người chơi đổi ải AFK
        public void PlaceAfkTag()
        {
            if (!entered || !afkTagPrefab) return;
            var st = Afk.Stage(App.Save.Data, App.Data);
            bool here = st != null && afkAt.ContainsKey(st.id);
            if (!here)
            {
                if (afkTag) afkTag.gameObject.SetActive(false);
                return;
            }
            if (!afkTag)
            {
                afkTag = Ui.Spawn(afkTagPrefab, p.nodeLayer);
                afkTag.name = "nhan_afk";
            }
            afkTag.gameObject.SetActive(true);
            afkTag.anchoredPosition = afkAt[st.id];
            afkTag.SetAsLastSibling();
        }

        // chỗ nhãn AFK: dưới chấm ải, hoặc dưới mặt bệ (bệ cao khoảng 0,62 bề rộng, tâm lệch xuống 0,12)
        static Vector2 PipTag(Vector2 pos) => pos + new Vector2(0, -ZonePip.SizeNow * 0.5f - 30);
        static Vector2 NodeTag(StageDef st, Vector2 pos, float scale) => pos + new Vector2(0, -(ZoneNode.Width(st.kind) * 0.4f + 26) * scale);

        // một bệ ải: tướng chính của ải (boss tiến hóa hiện dạng 1) đứng trên bệ đất của đảo
        ZoneNode SpawnNode(GameData d, SaveData s, StageDef st, Vector2 pt, int side, Action onClick)
        {
            afkAt[st.id] = NodeTag(st, pt, 1);
            bool cleared = Progress.StageCleared(s, st), open = Progress.StageOpen(s, st), current = open && !cleared;
            var en = Teams.StageLead(st, d);
            var node = Ui.Spawn(nodePrefab, p.nodeLayer);
            var pedestal = App.Art ? App.Art.Get($"be_{Keys.Of(zone)}{(st.kind == StageKind.Boss ? "_boss" : "")}") : null;
            node.Bind(st, d.Hero(en.hero), Teams.EnemyFormStar(en), en.level, open, cleared, current, pt, side, pedestal, onClick);
            return node;
        }

        // bảng tên đặt phía ngoài khúc cua của đường (xa hai ải kề), hai đầu đường đặt ngược phía ải kề
        static int PlateSide(List<Vector2> pts, int i)
        {
            float x = pts[i].x;
            float nx = i == 0 ? pts[1].x : i == pts.Count - 1 ? pts[i - 1].x : (pts[i - 1].x + pts[i + 1].x) / 2;
            if (Mathf.Abs(x - nx) < 4) return i % 2 == 0 ? 1 : -1;
            return x > nx ? 1 : -1;
        }

        static void Clear(Transform t)
        {
            for (int i = t.childCount - 1; i >= 0; i--) Destroy(t.GetChild(i).gameObject);
        }

        void Dashes(Vector2 a, Vector2 b)
        {
            var dir = b - a;
            float len = dir.magnitude;
            float ang = Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg;
            for (float t = 36; t < len - 30; t += 60)
            {
                var dash = Ui.Spawn(dashPrefab, p.pathLayer);
                dash.rectTransform.anchoredPosition = a + dir / len * t;
                dash.rectTransform.localEulerAngles = new Vector3(0, 0, ang);
            }
        }

        // ---------- đường mòn của đảo 70 ải ----------

        // điểm trên đường mòn: p theo khung ảnh đảo (gốc trên trái, y hướng xuống), d là quãng đường từ ải 1
        struct TrailPt
        {
            public Vector2 p;
            public float d;
        }

        static Vector2 Flip(Vector2 v) => new Vector2(v.x, -v.y);

        // đường cong qua các điểm ải của ảnh đảo (Catmull-Rom, hai đầu lặp điểm, như rc.curve của bản đồ nét tay), lấy mẫu dày
        // để đo chiều dài
        List<TrailPt> TrailPolyline(ZoneDef z)
        {
            var P = z.nodes.Select(n => new Vector2((float)n.x * mapW, (float)n.y * mapH)).ToList();
            var Q = new List<Vector2> { P[0] };
            Q.AddRange(P);
            Q.Add(P[P.Count - 1]);
            var poly = new List<TrailPt> { new TrailPt { p = P[0], d = 0 } };
            for (int i = 1; i + 2 < Q.Count; i++)
            {
                Vector2 p0 = Q[i - 1], p1 = Q[i], p2 = Q[i + 1], p3 = Q[i + 2];
                var b1 = p1 + (p2 - p0) / 6;
                var b2 = p2 - (p3 - p1) / 6;
                for (int k = 1; k <= 24; k++)
                {
                    float t = k / 24f, u = 1 - t;
                    var x = u * u * u * p1 + 3 * u * u * t * b1 + 3 * u * t * t * b2 + t * t * t * p2;
                    var last = poly[poly.Count - 1];
                    poly.Add(new TrailPt { p = x, d = last.d + Vector2.Distance(x, last.p) });
                }
            }
            return poly;
        }

        static Vector2 PointAt(List<TrailPt> poly, float d)
        {
            int i = 1;
            while (i < poly.Count - 1 && poly[i].d < d) i++;
            var a = poly[i - 1];
            var b = poly[i];
            float t = b.d > a.d ? Mathf.Clamp01((d - a.d) / (b.d - a.d)) : 0;
            return Vector2.Lerp(a.p, b.p, t);
        }

        // quãng đường của từng ải (theo idx - 1): sau mỗi bệ chừa chỗ cho tướng đứng trên bệ (đường đi lên), trước bệ sau chừa
        // nửa mặt bệ; chấm ải rải đều trên phần còn lại, cùng khoảng cách ở mọi chặng
        static float[] TrailLayout(List<StageDef> stages, float len)
        {
            var heads = stages.Where(st => st.tag == StageTag.Hero).ToList();
            float Up(StageDef st) => ZoneNode.HeroHeight(st.kind) * 0.5f * LongNodeScale + 8;
            float Down(StageDef st) => ZoneNode.Width(st.kind) * 0.32f * LongNodeScale + 8;
            int pips = 0;
            float excl = 0;
            for (int c = 0; c + 1 < heads.Count; c++)
            {
                pips += heads[c + 1].idx - heads[c].idx - 1;
                excl += Up(heads[c]) + Down(heads[c + 1]);
            }
            float gap = pips > 0 ? Mathf.Max(0, len - excl) / pips : 0;
            var at = new float[stages.Count];
            float D = 0;
            for (int c = 0; c < heads.Count; c++)
            {
                at[heads[c].idx - 1] = D;
                if (c + 1 >= heads.Count) break;
                int n = heads[c + 1].idx - heads[c].idx - 1;
                float a = D + Up(heads[c]);
                for (int j = 1; j <= n; j++) at[heads[c].idx - 1 + j] = a + gap * (j - 0.5f);
                D = a + gap * n + Down(heads[c + 1]);
            }
            return at;
        }

        // bản đồ dài: có tâm đường và chỗ ải tướng trong dữ liệu (GameData kiểm số chỗ khớp số ải tướng)
        static bool HasPath(ZoneDef z) => z.path.Count > 1 && z.stops.Count > 0;

        // bản đồ dài: đường là chuỗi điểm dày có sẵn (tâm con đường cát của ảnh), chỉ đo chiều dài
        List<TrailPt> PathPolyline(ZoneDef z)
        {
            var poly = new List<TrailPt>();
            foreach (var n in z.path)
            {
                var x = new Vector2((float)n.x * mapW, (float)n.y * mapH);
                float dist = poly.Count == 0 ? 0 : poly[poly.Count - 1].d + Vector2.Distance(x, poly[poly.Count - 1].p);
                poly.Add(new TrailPt { p = x, d = dist });
            }
            return poly;
        }

        // bản đồ dài: ải tướng ở đúng bãi của ảnh (stops theo tỉ lệ chiều dài đường); chấm ải xen giữa rải đều giữa hai bãi, chừa
        // chỗ tướng đứng trên bệ trước và nửa mặt bệ sau như TrailLayout
        static float[] PathLayout(ZoneDef z, List<StageDef> stages, float len)
        {
            var heads = stages.Where(st => st.tag == StageTag.Hero).ToList();
            float Up(StageDef st) => ZoneNode.HeroHeight(st.kind) * 0.5f * PathNodeScale + 8;
            float Down(StageDef st) => ZoneNode.Width(st.kind) * 0.32f * PathNodeScale + 8;
            var at = new float[stages.Count];
            for (int c = 0; c < heads.Count; c++)
            {
                float a = (float)z.stops[c] * len;
                at[heads[c].idx - 1] = a;
                if (c + 1 >= heads.Count) break;
                int n = heads[c + 1].idx - heads[c].idx - 1;
                float from = a + Up(heads[c]), to = (float)z.stops[c + 1] * len - Down(heads[c + 1]);
                float gap = n > 0 ? Mathf.Max(0, to - from) / n : 0;
                for (int j = 1; j <= n; j++) at[heads[c].idx - 1 + j] = from + gap * (j - 0.5f);
            }
            return at;
        }

        // đảo 70 ải: vệt đường tới ải đang đánh, chấm ải xen giữa, bệ ải tướng; trả chỗ ải đang đánh (để cuộn tới)
        Vector2 RenderTrail(ZoneDef z, GameData d, SaveData s, List<StageDef> stages, int prog)
        {
            bool path = HasPath(z) && z.stops.Count == stages.Count(st => st.tag == StageTag.Hero);
            float scale = path ? PathNodeScale : LongNodeScale;
            var poly = path ? PathPolyline(z) : TrailPolyline(z);
            var at = path ? PathLayout(z, stages, poly[poly.Count - 1].d) : TrailLayout(stages, poly[poly.Count - 1].d);
            var pos = at.Select(x => Flip(PointAt(poly, x))).ToList();
            int cur = Mathf.Min(prog, stages.Count - 1); // ải đang đánh, hoặc ải cuối khi đã xong
            if (prog > 0) DashesAlong(poly, at[0], at[cur]);

            // chấm trước, bệ sau (bệ đè lên chấm)
            var heads = new List<int>();
            for (int i = 0; i < stages.Count; i++)
            {
                var st = stages[i];
                if (st.tag == StageTag.Hero)
                {
                    heads.Add(i);
                    continue;
                }
                bool cleared = Progress.StageCleared(s, st), open = Progress.StageOpen(s, st);
                int id = st.id;
                Ui.Spawn(pipPrefab, p.nodeLayer).Bind(st, open, cleared, open && !cleared, pos[i], () => StagePrep.Open(id));
                afkAt[id] = PipTag(pos[i]);
            }
            // bệ trên cao vẽ trước, bệ thấp sau; bảng tên theo dữ liệu (ngược phía địa danh) hoặc phía ngoài khúc cua, lòi ra ngoài màn
            // (bản đồ canh giữa) thì đổi bên
            var hp = heads.Select(i => pos[i]).ToList();
            float left = (mapW - PokiCanvas.RefW) / 2;
            foreach (int k in Enumerable.Range(0, heads.Count).OrderByDescending(k => hp[k].y))
            {
                var st = stages[heads[k]];
                int id = st.id, side = path && k < z.plates.Count && z.plates[k] != 0 ? z.plates[k] : PlateSide(hp, k);
                float tip = hp[k].x - left + side * ZoneNode.PlateReach(st.kind) * scale;
                if (tip < 12 || tip > PokiCanvas.RefW - 12) side = -side;
                var node = SpawnNode(d, s, st, hp[k], side, () => StagePrep.Open(id));
                node.Rect.localScale = Vector3.one * scale;
                afkAt[id] = NodeTag(st, hp[k], scale);
            }
            return pos[cur];
        }

        // vệt đường dọc đường mòn từ ải 1 (quãng from) tới quãng end
        void DashesAlong(List<TrailPt> poly, float from, float end)
        {
            for (float t = from + 36; t < end - 30; t += 60)
            {
                var dir = Flip(PointAt(poly, t + 2)) - Flip(PointAt(poly, t - 2));
                var dash = Ui.Spawn(dashPrefab, p.pathLayer);
                dash.rectTransform.anchoredPosition = Flip(PointAt(poly, t));
                dash.rectTransform.localEulerAngles = new Vector3(0, 0, Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg);
            }
        }

        IEnumerator ScrollToCurrent(Vector2 pt)
        {
            yield return null;
            var view = (RectTransform)p.scroll.transform;
            float viewH = view.rect.height;
            float y = PadT - pt.y; // pt.y âm (từ trên xuống)
            float target = Mathf.Clamp(y - viewH * 0.5f, 0, Mathf.Max(0, p.content.sizeDelta.y - viewH));
            p.content.anchoredPosition = new Vector2(0, target);
        }

        // ---------- khung thông tin và rương mốc ----------

        void ShowInfo(ZoneDef z, SaveData s, int prog)
        {
            int size = Islands.Size(z.id);
            var at = Islands.Chests(z.id);
            p.elem.Set(z.id);
            int next = Progress.NextLevel(s, App.Data, z.id);
            p.level.text = next > 0 ? $"Ải kế cấp {next} · boss cấp {z.levelMax}" : $"Boss cấp {z.levelMax}";
            p.diff.Set(Progress.DifficultyOf(s, App.Data, z));
            p.count.text = $"{prog}/{size} ải";
            p.bar.Set(Theme.Of(z.id), prog / (float)size);
            // rương mốc đặt theo tỉ lệ số ải trên thanh; rương cuối (vàng, to) ở cuối thanh; rương thừa trong prefab thì ẩn
            int canClaim = Progress.ZoneChestReady(s, z.id);
            for (int i = 0; i < p.chests.Length; i++)
            {
                var c = p.chests[i];
                bool shown = i < at.Length;
                c.image.gameObject.SetActive(shown);
                if (!shown) continue;
                int k = i;
                bool got = s.zoneChests[(int)z.id] > i, can = canClaim == i, big = i == at.Length - 1;
                float frac = at[i] / (float)size, sz = at.Length > 2 && !big ? 64 : 84;
                c.image.rectTransform.Place(new Vector2(frac, 0.5f), new Vector2(frac >= 1 ? -30 : 0, 6), new Vector2(sz, sz), new Vector2(0.5f, 0.5f));
                c.image.color = got ? new Color(0.6f, 0.6f, 0.6f, 0.5f) : big ? Color.white : Theme.Hex("#d6dee8");
                c.click.OnClick = () => Claim(k);
                c.wobble.enabled = can;
                if (!can) c.image.rectTransform.localEulerAngles = Vector3.zero;
            }
            p.desc.text = $"{z.sub}. Địch hệ {Elements.Name(z.id)}: dùng tướng hệ {Elements.Name(Progress.CounterOf(z.id))} để khắc.";
        }

        void Claim(int n)
        {
            var d = App.Data;
            var s = App.Save.Data;
            if (Progress.ZoneChestReady(s, zone) != n)
            {
                App.Audio.Play("error");
                App.Toasts.Show(s.zoneChests[(int)zone] > n ? "Đã nhận rương này" : $"Qua {Islands.Chests(zone)[n]} ải của đảo để mở", Icon("chest"));
                return;
            }
            var r = Progress.ClaimZoneChest(s, d, zone, new Rng(Rng.RandomSeed()));
            if (r == null) return;
            App.Save.Save();
            App.Audio.Play("chest");
            App.Modals.Open(chestPrefab).Show(r, s, d);
            Render();
        }

        // ---------- khung ải tiếp theo ----------

        void ShowBottom(ZoneDef z, SaveData s)
        {
            var d = App.Data;
            var next = Progress.NextStage(s, d, zone);
            p.next.SetActive(next != null);
            p.done.SetActive(next == null);
            Clear(p.enemies);
            if (next == null)
            {
                p.doneTitle.text = $"Đã chinh phục {z.name}!";
                return;
            }
            // đảo 70 ải: kèm kiểu ải (Tướng mới, Bầy lính, Cửa ải…)
            string tag = next.tag != StageTag.None ? $" · {ZoneChapterRow.TagText(next)}" : "";
            p.nextTitle.text = $"Ải {next.idx}/{Islands.Size(zone)} · {next.name}{tag}";
            for (int i = 0; i < next.enemies.Count; i++)
            {
                var en = next.enemies[i];
                Ui.Spawn(enemyPrefab, p.enemies).Bind(d.Hero(en.hero), en, i);
            }
            var gift = next.drops.FirstOrDefault(x => x.gift);
            var shards = next.drops.Where(x => !x.gift).Select(x => d.Hero(x.hero).name).Distinct().ToList();
            string extra = gift != null ? $" · {d.Hero(gift.HeroFor(s)).name} gia nhập đội!" : shards.Count > 0 ? $" · rơi mảnh {string.Join(", ", shards)}" : "";
            p.reward.text = $"+{Progress.StageBalls(d, next, true)} bi{extra}";
            int id = next.id;
            p.fight.SetOnClick(() => StagePrep.Open(id));
        }
    }
}
