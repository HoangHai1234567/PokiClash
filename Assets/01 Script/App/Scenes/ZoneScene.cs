// Đảo hệ (chép zoneScreen của Web/src/view/screens/zone.ts): ảnh đảo phóng 1,27 lần, cuộn dọc, 8 ải dọc đường mòn.
// Khung thông tin trên (hệ, cấp đề nghị, độ khó, tiến độ, 2 rương mốc, gợi ý hệ khắc), khung ải tiếp theo dưới.
// Trong một đảo ải mở lần lượt. args = Elem, hoặc ZoneArgs (mở luôn hộp chuẩn bị của một ải).
// Prefab màn hình Assets/04 Prefabs/Screens/Zone dùng cho cả 5 đảo: màu biển, ảnh đảo, chữ gán lúc chạy; nút ải (Items/NutAi),
// vệt đường (Items/VetDuong), sticker đội trưởng (Items/DoiTruongDao), địch ải tiếp (Items/DichAi) sinh theo dữ liệu.
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
        [SerializeField] HeroPortrait leaderPrefab;
        [SerializeField] ZoneEnemy enemyPrefab;
        [SerializeField] ZoneChestDialog chestPrefab;

        Elem zone = Elem.Thuy;
        float mapW, mapH;
        bool entered;

        public override string Title => App.Data.Zone(zone)?.name ?? "Đảo";

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, ZoneNode node, Image dash, HeroPortrait leader, ZoneEnemy enemy, ZoneChestDialog chest)
        {
            p = parts;
            nodePrefab = node;
            dashPrefab = dash;
            leaderPrefab = leader;
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

            p.sea.color = Theme.Hex(z.sea);
            var sprite = App.Art ? App.Art.Get(z.art) : null;
            float aspect = sprite ? sprite.rect.width / sprite.rect.height : PokiCanvas.RefW / PokiCanvas.RefH;
            mapW = PokiCanvas.RefW * MK;
            mapH = mapW / aspect;
            p.content.sizeDelta = new Vector2(0, PadT + mapH + PadB);
            p.map.name = "anh_" + z.art;
            Theme.SetSprite(p.map, sprite);
            p.map.rectTransform.sizeDelta = new Vector2(mapW, mapH);

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

            string lead = s.team.FirstOrDefault(t => s.Hero(t)?.owned == true) ?? "tieu_y";
            for (int i = 0; i < stages.Count; i++)
            {
                var st = stages[i];
                var pt = pts[i];
                bool cleared = Progress.StageCleared(s, st), open = Progress.StageOpen(s, st), current = open && !cleared;
                var stage = st;
                var node = Ui.Spawn(nodePrefab, p.nodeLayer);
                node.Bind(st, open, cleared, current, pt, Icon(st.kind == StageKind.Boss ? "boss" : "crownSm"), () =>
                {
                    if (!Progress.StageOpen(App.Save.Data, stage))
                    {
                        App.Toasts.Show($"Qua ải {stage.idx - 1} của {z.name} trước đã", Icon("lock"));
                        return;
                    }
                    StagePrep.Open(stage.id);
                });
                if (current)
                {
                    // sticker đội trưởng đứng cạnh ải đang đánh (nhún nhờ Bob có sẵn trên prefab)
                    var side = pt.x > mapW / 2 ? -1 : 1;
                    var por = Ui.Spawn(leaderPrefab, p.nodeLayer);
                    por.Bind(d.Hero(lead), 160);
                    var rt = por.Rect;
                    rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                    rt.anchoredPosition = pt + new Vector2(side * 120, 10);
                    if (side < 0) rt.localScale = new Vector3(-1, 1, 1);
                }
            }

            ShowInfo(z, s, prog);
            ShowBottom(z, s);
            StartCoroutine(ScrollToCurrent(pts[Mathf.Min(7, prog)]));
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
