// Toàn bộ dữ liệu game (tướng, thẻ, đảo, ải, cấu hình) nạp từ JSON xuất bởi Web/scripts/export_data.ts.
// Một nguồn: sửa ở web rồi xuất lại, menu "PokiClash/Nhập dữ liệu" dựng ScriptableObject từ cùng JSON này.
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

        public GameData Index()
        {
            heroById = Heroes.ToDictionary(h => h.id);
            cardById = Pool.Concat(Innate).ToDictionary(c => c.id);
            stageById = Stages.ToDictionary(s => s.id);
            return this;
        }

        // ---------- đọc JSON ----------

        public static GameData FromJson(string heroesJson, string cardsJson, string zonesJson, string stagesJson, string balanceJson)
        {
            var d = new GameData();

            var h = J.Obj(MiniJson.Parse(heroesJson));
            foreach (var x in J.Arr(h, "heroes")) d.Heroes.Add(ParseHero(J.Obj(x)));
            foreach (var x in J.Arr(h, "starters")) d.Starters.Add((string)x);
            d.LegendMilestoneHero = J.Str(h, "legendMilestoneHero");

            var c = J.Obj(MiniJson.Parse(cardsJson));
            foreach (var x in J.Arr(c, "pool")) d.Pool.Add(ParseCard(J.Obj(x)));
            foreach (var x in J.Arr(c, "innate")) d.Innate.Add(ParseCard(J.Obj(x)));

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
            };
            foreach (var x in J.Arr(o, "enemies"))
            {
                var e = J.Obj(x);
                s.enemies.Add(new StageEnemy { hero = J.Str(e, "hero"), level = J.Int(e, "level"), boss = J.Bool(e, "boss") });
            }
            foreach (var x in J.Arr(o, "drops"))
            {
                var e = J.Obj(x);
                s.drops.Add(new StageDrop
                {
                    hero = J.Str(e, "hero"), chance = J.Num(e, "chance"), min = J.Int(e, "min"), max = J.Int(e, "max"), gift = J.Bool(e, "gift"),
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
            Expect(Heroes.Count, 40, "Số tướng");
            Expect(Pool.Count, 23, "Số thẻ chung");
            Expect(Innate.Count, 120, "Số thẻ riêng");
            Expect(Zones.Count, 5, "Số đảo");
            Expect(Stages.Count, 40, "Số ải");
            if (Cfg == null) err.Add("Thiếu cấu hình cân bằng");

            bool In01(Pt p) => p.x >= 0 && p.x <= 1 && p.y >= 0 && p.y <= 1;
            foreach (var z in Zones)
            {
                Expect(z.nodes.Count, 8, $"Số ải trên {z.name}");
                for (int i = 0; i < z.nodes.Count; i++)
                    if (!In01(z.nodes[i])) err.Add($"{z.name}: toạ độ ải {i + 1} {z.nodes[i]} ngoài 0–1");
                if (!In01(z.world)) err.Add($"{z.name}: toạ độ trên đảo lớn {z.world} ngoài 0–1");
            }
            foreach (var h in Heroes)
            {
                foreach (var id in new[] { h.skill, h.ult, h.passive })
                    if (Card(id) == null) err.Add($"{h.name}: thiếu thẻ {id}");
                if (h.stats.Length != 6) err.Add($"{h.name}: cần 6 chỉ số gốc");
                if (h.forms.Length < 1 || h.forms.Length > 3) err.Add($"{h.name}: cần 1–3 dạng, có {h.forms.Length}");
            }
            if (Cfg != null && Cfg.formStars.Length != 2) err.Add($"Mốc đổi dạng: có {Cfg.formStars.Length}, cần 2");
            foreach (var s in Stages)
            {
                foreach (var e in s.enemies)
                    if (Hero(e.hero) == null) err.Add($"Ải {s.id}: địch {e.hero} không có");
                foreach (var dr in s.drops)
                    if (Hero(dr.hero) == null) err.Add($"Ải {s.id}: rơi {dr.hero} không có");
            }
            foreach (var id in Starters)
                if (Hero(id) == null) err.Add($"Tướng khởi đầu {id} không có");
            return err;
        }
    }
}
