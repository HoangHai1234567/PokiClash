// Toàn bộ dữ liệu game (tướng, lính, thẻ, đảo, ải, cấu hình) nạp từ JSON trong Assets/02 Data/Json.
// JSON là nguồn (lần cuối xuất từ bản web 2026-11-03, từ đó sửa thẳng), menu "PokiClash/Nhập dữ liệu" dựng ScriptableObject từ cùng JSON này.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public sealed class GameData
    {
        public static GameData Current;

        public List<HeroDef> Heroes = new List<HeroDef>();
        public List<CardDef> Pool = new List<CardDef>(); // thẻ chung
        public List<CardDef> Innate = new List<CardDef>(); // thẻ riêng (chiêu, tuyệt kỹ, bị động)
        public List<HeroDef> Minions = new List<HeroDef>(); // lính của ải: Hero(id) tìm được, nhưng không nằm trong Heroes (không thu phục)
        public List<CardDef> MinionCards = new List<CardDef>(); // chiêu, tuyệt kỹ, bị động của lính
        public List<CardDef> Traits = new List<CardDef>(); // bị động boss của ải (StageEnemy.trait), 2026-11-05
        public List<ZoneDef> Zones = new List<ZoneDef>();
        public List<StageDef> Stages = new List<StageDef>();
        public BalanceConfig Cfg;
        public List<string> Starters = new List<string>();
        public string LegendMilestoneHero;
        public Pt Village;

        Dictionary<string, HeroDef> heroById;
        Dictionary<string, CardDef> cardById;
        Dictionary<int, StageDef> stageById;

        public HeroDef Hero(string id) => heroById.TryGetValue(id, out var h) ? h : null;
        public CardDef Card(string id) => cardById.TryGetValue(id, out var c) ? c : null;
        public StageDef Stage(int id) => stageById.TryGetValue(id, out var s) ? s : null;
        public ZoneDef Zone(Elem e) => Zones.FirstOrDefault(z => z.id == e);
        public IEnumerable<StageDef> ZoneStages(Elem e) => Stages.Where(s => s.zone == e);

        // ải thu phục tướng khởi đầu id ở đảo cùng hệ: ải đầu tiên trong ải 1–4 có nó là địch và lần đầu chắc chắn rơi mảnh (không phải quà)
        public StageDef StarterStage(string id)
        {
            var h = Hero(id);
            return h == null ? null : ZoneStages(h.elem).FirstOrDefault(s => s.idx <= 4 && s.enemies.Any(e => e.hero == id)
                && s.drops.Any(dr => dr.hero == id && dr.chance >= 1 && !dr.gift));
        }

        public GameData Index()
        {
            heroById = Heroes.Concat(Minions).ToDictionary(h => h.id);
            cardById = Pool.Concat(Innate).Concat(MinionCards).Concat(Traits).ToDictionary(c => c.id);
            stageById = Stages.ToDictionary(s => s.id);
            Islands.Bind(this);
            return this;
        }

        // ---------- đọc JSON ----------

        public static GameData FromJson(string heroesJson, string cardsJson, string zonesJson, string stagesJson, string balanceJson)
        {
            var d = new GameData();

            var h = J.Obj(MiniJson.Parse(heroesJson));
            foreach (var x in J.Arr(h, "heroes")) d.Heroes.Add(ParseHero(J.Obj(x)));
            foreach (var x in J.Arr(h, "minions")) d.Minions.Add(ParseHero(J.Obj(x)));
            foreach (var x in J.Arr(h, "starters")) d.Starters.Add((string)x);
            d.LegendMilestoneHero = J.Str(h, "legendMilestoneHero");

            var c = J.Obj(MiniJson.Parse(cardsJson));
            foreach (var x in J.Arr(c, "pool")) d.Pool.Add(ParseCard(J.Obj(x)));
            foreach (var x in J.Arr(c, "innate")) d.Innate.Add(ParseCard(J.Obj(x)));
            foreach (var x in J.Arr(c, "minions")) d.MinionCards.Add(ParseCard(J.Obj(x)));
            foreach (var x in J.Arr(c, "traits")) d.Traits.Add(ParseCard(J.Obj(x)));

            var z = J.Obj(MiniJson.Parse(zonesJson));
            foreach (var x in J.Arr(z, "zones")) d.Zones.Add(ParseZone(J.Obj(x)));
            d.Village = ParsePt(J.Get(z, "village"));

            var s = J.Obj(MiniJson.Parse(stagesJson));
            foreach (var x in J.Arr(s, "stages")) d.Stages.Add(ParseStage(J.Obj(x)));

            var b = J.Obj(MiniJson.Parse(balanceJson));
            d.Cfg = BalanceConfig.FromJson(b);

            return d.Index();
        }

        static HeroDef ParseHero(Dictionary<string, object> o)
        {
            var st = J.Arr(o, "stats");
            var h = new HeroDef
            {
                id = J.Str(o, "id"),
                name = J.Str(o, "name"),
                title = J.Str(o, "title"),
                aola = J.Str(o, "aola"),
                elem = Keys.ToElem(J.Str(o, "elem")),
                rarity = Keys.ToRarity(J.Str(o, "rarity")),
                skill = J.Str(o, "skill"),
                ult = J.Str(o, "ult"),
                passive = J.Str(o, "passive"),
                shards = J.Int(o, "shards"),
                line = J.Str(o, "line"),
                size = J.Num(o, "size", 1),
                minion = J.Bool(o, "minion"),
            };
            h.stats = new int[st.Count];
            for (int i = 0; i < st.Count; i++) h.stats[i] = (int)(double)st[i];
            var fs = J.Arr(o, "forms");
            h.forms = new HeroForm[fs.Count];
            for (int i = 0; i < fs.Count; i++)
            {
                var f = J.Obj(fs[i]);
                h.forms[i] = new HeroForm { name = J.Str(f, "name"), aola = J.Str(f, "aola"), size = J.Num(f, "size", 1) };
            }
            return h;
        }

        static CardDef ParseCard(Dictionary<string, object> o)
        {
            var cost = J.Obj(o, "cost");
            var c = new CardDef
            {
                id = J.Str(o, "id"),
                name = J.Str(o, "name"),
                rarity = Keys.ToRarity(J.Str(o, "rarity")),
                kind = Keys.ToKind(J.Str(o, "kind")),
                icon = J.Str(o, "icon"),
                costMana = J.Int(cost, "mana"),
                costRage = J.Int(cost, "rage"),
                trigger = Keys.ToTrigger(J.Str(o, "trigger")),
                hasChance = J.Has(o, "chance"),
                chance = J.Num(o, "chance"),
                below = J.Num(o, "below", 0.3),
                unlock = J.Int(o, "unlock", 1),
                repeat = J.Bool(o, "repeat"),
                flavor = J.Str(o, "flavor"),
                owner = J.Str(o, "owner"),
                effectsJson = MiniJson.Write(J.Get(o, "effects") ?? new List<object>()),
            };
            return c;
        }

        static Pt ParsePt(object v)
        {
            var a = J.Arr(v);
            return a.Count >= 2 ? new Pt((double)a[0], (double)a[1]) : default;
        }

        static ZoneDef ParseZone(Dictionary<string, object> o)
        {
            var lv = J.Arr(o, "level");
            var sky = J.Arr(o, "sky");
            var z = new ZoneDef
            {
                id = Keys.ToElem(J.Str(o, "id")),
                order = J.Int(o, "order"),
                name = J.Str(o, "name"),
                sub = J.Str(o, "sub"),
                levelMin = lv.Count > 0 ? (int)(double)lv[0] : 1,
                levelMax = lv.Count > 1 ? (int)(double)lv[1] : 1,
                art = J.Str(o, "art"),
                skyTop = sky.Count > 0 ? (string)sky[0] : "#ffffff",
                skyBottom = sky.Count > 1 ? (string)sky[1] : "#ffffff",
                ground = J.Str(o, "ground"),
                sea = J.Str(o, "sea"),
                world = ParsePt(J.Get(o, "world")),
            };
            foreach (var p in J.Arr(o, "nodes")) z.nodes.Add(ParsePt(p));
            foreach (var p in J.Arr(o, "path")) z.path.Add(ParsePt(p));
            foreach (var s in J.Arr(o, "stops")) z.stops.Add(Convert.ToDouble(s));
            foreach (var s in J.Arr(o, "plates")) z.plates.Add(Convert.ToInt32(s));
            return z;
        }

        static StageDef ParseStage(Dictionary<string, object> o)
        {
            var s = new StageDef
            {
                id = J.Int(o, "id"),
                zone = Keys.ToElem(J.Str(o, "zone")),
                idx = J.Int(o, "idx"),
                name = J.Str(o, "name"),
                kind = Keys.ToStageKind(J.Str(o, "kind")),
                tag = Keys.ToStageTag(J.Str(o, "tag")),
                chapter = J.Int(o, "chapter"),
            };
            foreach (var x in J.Arr(o, "enemies"))
            {
                var e = J.Obj(x);
                s.enemies.Add(new StageEnemy
                {
                    hero = J.Str(e, "hero"), level = J.Int(e, "level"), boss = J.Bool(e, "boss"), evo = J.Bool(e, "evo"), buff = J.Num(e, "buff"),
                    trait = J.Str(e, "trait"),
                });
            }
            foreach (var x in J.Arr(o, "drops"))
            {
                var e = J.Obj(x);
                s.drops.Add(new StageDrop
                {
                    hero = J.Str(e, "hero"), chance = J.Num(e, "chance"), min = J.Int(e, "min"), max = J.Int(e, "max"), gift = J.Bool(e, "gift"),
                    altFor = J.Str(e, "altFor"), altHero = J.Str(e, "altHero"),
                });
            }
            return s;
        }

        // ---------- kiểm tra ----------

        // Trả về danh sách lỗi (rỗng là ổn). Số lượng mong đợi theo bản web đã duyệt.
        public List<string> Validate()
        {
            var err = new List<string>();
            void Expect(int got, int want, string what)
            {
                if (got != want) err.Add($"{what}: có {got}, cần {want}");
            }
            Expect(Heroes.Count, 88, "Số tướng"); // 40 tướng 8 mỗi hệ, Thủy thêm 5 (2026-11-02), Mộc thêm 7, Hỏa thêm 8, Kim thêm 8 (2026-11-05), Hỏa thêm Ngưu Quyền, Thổ thêm 9 (2026-11-06), Thủy thêm 10 (lô tướng mới 2026-11-11)
            Expect(Pool.Count, 35, "Số thẻ chung"); // 23 của bản web, thêm 12 ở Unity (2026-11-04)
            Expect(Innate.Count, 265, "Số thẻ riêng"); // 88 tướng × 3 + thẻ Tiến Hóa của boss
            Expect(Minions.Count, 30, "Số lính"); // 3 loại lính mỗi đảo 70 ải (5 đảo), mỗi loại 2 bậc
            Expect(MinionCards.Count, 90, "Số thẻ của lính");
            Expect(Zones.Count, 5, "Số đảo");
            Expect(Stages.Count, 350, "Số ải"); // 5 đảo, mỗi đảo 70 ải
            if (Cfg == null) err.Add("Thiếu cấu hình cân bằng");

            bool In01(Pt p) => p.x >= 0 && p.x <= 1 && p.y >= 0 && p.y <= 1;
            foreach (var z in Zones)
            {
                // đảo 70 ải: nodes là các ải tướng; đảo 8 ải: 8 ải
                int heads = ZoneStages(z.id).Count(x => x.tag == StageTag.Hero);
                Expect(z.nodes.Count, heads > 0 ? heads : 8, $"Số ải trên {z.name}");
                for (int i = 0; i < z.nodes.Count; i++)
                    if (!In01(z.nodes[i])) err.Add($"{z.name}: toạ độ ải {i + 1} {z.nodes[i]} ngoài 0–1");
                if (!In01(z.world)) err.Add($"{z.name}: toạ độ trên đảo lớn {z.world} ngoài 0–1");
                // bản đồ dài: đường đủ điểm trong ảnh, mỗi ải tướng một chỗ trên đường (tăng dần) và một bên bảng tên
                if (z.path.Count == 0) continue;
                if (z.path.Count < 2) err.Add($"{z.name}: đường chỉ có {z.path.Count} điểm");
                if (z.path.Any(p => !In01(p))) err.Add($"{z.name}: có điểm đường ngoài 0–1");
                Expect(z.stops.Count, heads, $"Số chỗ ải tướng trên đường {z.name}");
                for (int i = 0; i < z.stops.Count; i++)
                    if (z.stops[i] < 0 || z.stops[i] > 1 || i > 0 && z.stops[i] <= z.stops[i - 1])
                        err.Add($"{z.name}: chỗ ải tướng thứ {i + 1} ({z.stops[i]}) phải trong 0–1 và tăng dần");
                if (z.plates.Count > 0) Expect(z.plates.Count, heads, $"Số bên bảng tên trên {z.name}");
            }
            foreach (var h in Heroes.Concat(Minions))
            {
                foreach (var id in new[] { h.skill, h.ult, h.passive })
                    if (Card(id) == null) err.Add($"{h.name}: thiếu thẻ {id}");
                if (h.stats.Length != 6) err.Add($"{h.name}: cần 6 chỉ số gốc");
                if (h.forms.Length < 1 || h.forms.Length > 3) err.Add($"{h.name}: cần 1–3 dạng, có {h.forms.Length}");
            }
            foreach (var h in Heroes)
                if (h.minion) err.Add($"{h.name}: lính không được nằm trong danh sách tướng");
            foreach (var h in Minions)
                if (!h.minion) err.Add($"{h.name}: thiếu cờ lính");
            if (Cfg != null && Cfg.formStars.Length != 2) err.Add($"Mốc đổi dạng: có {Cfg.formStars.Length}, cần 2");
            // bị động boss: thẻ bị động có kiểu kích hoạt (không dùng "lần đầu gục": boss không hồi sinh), chỉ gắn cho boss của ải
            foreach (var c in Traits)
                if (c.kind != CardKind.Passive || c.trigger == PassiveTrigger.None || c.trigger == PassiveTrigger.Death)
                    err.Add($"Bị động boss {c.id}: phải là thẻ bị động, kích hoạt khác lần đầu gục");
            foreach (var s in Stages)
            {
                foreach (var e in s.enemies)
                {
                    if (Hero(e.hero) == null) err.Add($"Ải {s.id}: địch {e.hero} không có");
                    if (string.IsNullOrEmpty(e.trait)) continue;
                    if (!Traits.Exists(c => c.id == e.trait)) err.Add($"Ải {s.id}: bị động boss {e.trait} không có trong traits");
                    if (!e.boss) err.Add($"Ải {s.id}: bị động boss {e.trait} gắn cho {e.hero} không phải boss");
                }
                foreach (var dr in s.drops)
                {
                    if (Hero(dr.hero) == null || Hero(dr.hero).minion) err.Add($"Ải {s.id}: rơi {dr.hero} không phải tướng");
                    if (string.IsNullOrEmpty(dr.altFor)) continue;
                    if (!Starters.Contains(dr.altFor)) err.Add($"Ải {s.id}: quà thay theo {dr.altFor}, không phải tướng khởi đầu");
                    if (Hero(dr.altHero) == null || Hero(dr.altHero).minion) err.Add($"Ải {s.id}: quà thay {dr.altHero} không phải tướng");
                }
            }
            foreach (var z in Zones)
            {
                var st = ZoneStages(z.id).ToList();
                for (int i = 0; i < st.Count; i++)
                    if (st[i].idx != i + 1) err.Add($"{z.name}: ải thứ {i + 1} mang số {st[i].idx}");
                int tagged = st.Count(x => x.tag != StageTag.None);
                if (tagged > 0 && tagged < st.Count) err.Add($"{z.name}: {st.Count - tagged} ải thiếu kiểu ải");
            }
            // mỗi hệ một tướng khởi đầu, là địch ở chặng đầu (ải 1–4) của đảo cùng hệ và lần đầu chắc chắn rơi mảnh (15_TuongKhoiDau.md).
            // Thường đứng một mình ở ải 1; đảo Mộc (làm lại 2026-11-05) nhường ải 1 cho tướng người dùng chọn, Nụ Hoa đứng ở ải 2
            foreach (var id in Starters)
            {
                var h = Hero(id);
                if (h == null)
                {
                    err.Add($"Tướng khởi đầu {id} không có");
                    continue;
                }
                if (Starters.Count(x => Hero(x)?.elem == h.elem) > 1) err.Add($"Tướng khởi đầu {h.name}: trùng hệ {Elements.Name(h.elem)}");
                if (!ZoneStages(h.elem).Any()) continue;
                if (StarterStage(id) == null)
                    err.Add($"{Zone(h.elem)?.name}: tướng khởi đầu {h.name} phải là địch ở ải 1–4, lần đầu chắc chắn rơi mảnh");
            }
            return err;
        }
    }
}
