// Đảo hệ (chép zoneScreen của Web/src/view/screens/zone.ts): bản đồ đảo (ArtGen/Islands/compose_islands.py) rộng 1,27 màn, cuộn dọc, 8 ải dọc đường.
// Khung thông tin trên (hệ, cấp đề nghị, độ khó, tiến độ, 2 rương mốc, gợi ý hệ khắc), khung ải tiếp theo dưới.
// Trong một đảo ải mở lần lượt. args = Elem, hoặc ZoneArgs (mở luôn hộp chuẩn bị của một ải).
// Prefab màn hình Assets/04 Prefabs/Screens/Zone dùng cho cả 5 đảo: màu biển, ảnh đảo, chữ gán lúc chạy; bệ ải (Items/BeAi),
// vệt đường (Items/VetDuong), địch ải tiếp (Items/DichAi) sinh theo dữ liệu.
// Mỗi ải là một bệ (Items/BeAi, ZoneNode): tướng chính của ải (Teams.StageLead) đứng trên bệ, bảng tên phía ngoài khúc cua.
// Không hiện tướng của người chơi trên bản đồ (người dùng bỏ sticker đội trưởng cạnh ải đang đánh, 2026-11-02).
using System;
using System.Collections;
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
        // bản đồ phóng to và cuộn dọc, để ải ở hai đầu không bị khung trên dưới che
        public const float MK = 1.27f, PadT = 260, PadB = 330;

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
        [Tooltip("Biển cuộn theo bản đồ (con đầu của noi_dung, menu Đảo sảnh: ghép ảnh, kéo, mây viền); trống thì chỉ có biển nền")]
        [SerializeField] Image seaScroll;
        [Tooltip("Lớp phần động trên ảnh bản đồ (con của ảnh bản đồ, menu Đảo sảnh: ghép ảnh, kéo, mây viền)")]
        [SerializeField] IslandAnim mapAnim;

        Elem zone = Elem.Thuy;
        float mapW, mapH;
        bool entered;

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
            mapW = PokiCanvas.RefW * MK;
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

            // đường đã đi: nét chấm vàng viền mực nối các ải đã qua tới ải đang đánh
            var pts = z.nodes.Select(NodePos).ToList();
            for (int i = 0; i < Mathf.Min(prog, 7); i++) Dashes(pts[i], pts[i + 1]);

            string key = Keys.Of(zone);
            // vẽ ải trên cao trước, ải thấp sau (đứng đè lên), cho có chiều sâu
            foreach (int i in Enumerable.Range(0, stages.Count).OrderByDescending(k => pts[k].y))
            {
                var st = stages[i];
                var pt = pts[i];
                bool cleared = Progress.StageCleared(s, st), open = Progress.StageOpen(s, st), current = open && !cleared;
                var stage = st;
                var en = Teams.StageLead(st, d);
                int side = PlateSide(pts, i);
                var node = Ui.Spawn(nodePrefab, p.nodeLayer);
                var pedestal = App.Art ? App.Art.Get($"be_{key}{(st.kind == StageKind.Boss ? "_boss" : "")}") : null;
                node.Bind(st, d.Hero(en.hero), Teams.EnemyFormStar(en), en.level, open, cleared, current, pt, side, pedestal, () =>
                {
                    if (!Progress.StageOpen(App.Save.Data, stage))
                    {
                        App.Toasts.Show($"Qua ải {stage.idx - 1} của {z.name} trước đã", Icon("lock"));
                        return;
                    }
                    StagePrep.Open(stage.id);
                });
            }

            ShowInfo(z, s, prog);
            ShowBottom(z, s);
            StartCoroutine(ScrollToCurrent(pts[Mathf.Min(7, prog)]));
        }

        // bảng tên đặt phía ngoài khúc cua của đường (xa hai ải kề), hai đầu đường đặt ngược phía ải kề
        static int PlateSide(System.Collections.Generic.List<Vector2> pts, int i)
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
            p.elem.Set(z.id);
            p.level.text = $"Cấp đề nghị {z.levelMin}–{z.levelMax}";
            p.diff.Set(Progress.DifficultyOf(z, s.level, prog >= 8));
            p.count.text = $"{prog}/8 ải";
            p.bar.Set(Theme.Of(z.id), prog / 8f);
            int canClaim = Progress.ZoneChestReady(s, z.id);
            for (int i = 0; i < p.chests.Length; i++)
            {
                int k = i;
                bool got = s.zoneChests[(int)z.id] > i, can = canClaim == i;
                var c = p.chests[i];
                c.image.color = got ? new Color(0.6f, 0.6f, 0.6f, 0.5f) : i == 0 ? Theme.Hex("#d6dee8") : Color.white;
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
                App.Toasts.Show(s.zoneChests[(int)zone] > n ? "Đã nhận rương này" : $"Qua {Progress.ZoneChestAt[n]} ải của đảo để mở", Icon("chest"));
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
            p.nextTitle.text = $"Ải {next.idx}/8 · {next.name}";
            for (int i = 0; i < next.enemies.Count; i++)
            {
                var en = next.enemies[i];
                Ui.Spawn(enemyPrefab, p.enemies).Bind(d.Hero(en.hero), en, i);
            }
            var gift = next.drops.FirstOrDefault(x => x.gift);
            string extra = gift != null ? $" · {d.Hero(gift.hero).name} gia nhập đội!" : next.drops.Count > 0 ? $" · rơi mảnh {string.Join(", ", next.drops.Select(x => d.Hero(x.hero).name))}" : "";
            p.reward.text = $"+{Progress.StageBalls(d, next, true)} bi{extra}";
            int id = next.id;
            p.fight.SetOnClick(() => StagePrep.Open(id));
        }
    }
}
