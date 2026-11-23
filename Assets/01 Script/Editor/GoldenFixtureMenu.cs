// Menu "PokiClash/Thử/Golden và tự chạy/Tính lại golden theo tướng mẫu của test (rương, AFK, trang trại, tiềm năng, đền)": tính lại các golden mà test dựng
// bản lưu bằng vài tướng mẫu cố định. Viết 2026-11-16 khi bỏ 31 tướng cũ không còn suất đảo (SaveCodec.BoTuongCu): tướng mẫu đổi sang
// tướng thay cùng hệ, nên các kết quả rơi thẻ, mảnh, năng suất... đổi theo. Giữ đầu vào của golden cũ (thao tác, thời điểm, hạt giống,
// ô khoá, giữ mới / giữ cũ...), tướng cũ trong đầu vào đổi theo bảng trên, rồi tính lại kết quả bằng code Unity đúng như test chạy:
// - progression.json "drops"                      ProgressionTests.TheRoiTuRuong_KhopBanWeb
// - pachinko.json "chest"                          PachinkoTests.MoRuong600Lan_KhopBanWeb
// - afk.json "steps"                               AfkTests.ChayLaiTungBuoc_KhopBanWeb
// - farm.json "open", "formula", "steps"           FarmTests.CongThuc_VaTungBuoc_KhopBanWeb
// - potential.json "spins", "members", "fights"    PotentialTests (khai phá 60 lần, phần cộng đầu trận, 6 trận thật)
// - badges.json "stats", "steps"                   BadgeTests (chỉ số có huy hiệu, tiến độ đền)
// Tướng mẫu ở đây phải trùng tướng mẫu trong các test đó. Golden phụ thuộc danh sách tướng (progression "stats"/"shards", badges
// "stages"/"fights", potential "caveStages") do menu "Tính lại golden theo danh sách tướng" (IslandGenMenu) tính.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class GoldenFixtureMenu
    {
        const double H = 3600000;
        static readonly string[] SlotKey = { "skill", "ult", "passive" };

        // tướng khởi đầu của bản lưu mẫu (TestData.OldStarter; trước 2026-11-16 là Giọt Sương)
        const string Starter = "ti_tach";

        static string Data(string f) => Path.Combine(Application.dataPath, "02 Data", f);
        static Dictionary<string, object> Load(string f) => J.Obj(MiniJson.Parse(File.ReadAllText(Data(f))));
        static void Save(string f, Dictionary<string, object> o) => File.WriteAllText(Data(f), IslandGen.Write(o) + "\n");

        // pachinko.json xuất từ web viết liền một dòng (JSON.stringify không thụt): giữ nguyên kiểu đó
        static void SaveCompact(string f, Dictionary<string, object> o) => File.WriteAllText(Data(f), MiniJson.Write(o) + "\n");

        // tướng cũ trong đầu vào golden đổi sang tướng thay (cùng bảng với bước gộp bản lưu v10 -> v11)
        static string M(string id)
        {
            if (id == null) return null;
            foreach (var (from, to) in SaveCodec.BoTuongCu)
                if (from == id) return to;
            foreach (var (from, to) in SaveCodec.BoThoCu) // 7 tướng Thổ cũ, 2026-11-19
                if (from == id) return to;
            return id;
        }

        static double N(object x) => Convert.ToDouble(x);

        [MenuItem("PokiClash/Thử/Golden và tự chạy/Tính lại golden theo tướng mẫu của test (rương, AFK, trang trại, tiềm năng, đền)", priority = 303)]
        public static void Run()
        {
            var d = GameData.FromJson(File.ReadAllText(Data("Json/heroes.json")), File.ReadAllText(Data("Json/cards.json")),
                File.ReadAllText(Data("Json/zones.json")), File.ReadAllText(Data("Json/stages.json")), File.ReadAllText(Data("Json/balance.json")));
            Progression(d);
            Chest(d);
            AfkSteps(d);
            FarmSteps(d);
            PotentialAll(d);
            BadgesAll(d);
            AssetDatabase.Refresh();
            Debug.Log("[Golden] Đã tính lại theo tướng mẫu: progression drops, pachinko chest, afk, farm, potential, badges stats/steps");
        }

        // ---------- thưởng ----------

        static List<object> CardDrop(PokiClash.Core.Progress.CardDrop c) =>
            new List<object> { c.hero, SlotKey[(int)c.slot], c.card, Keys.Of(c.rarity) };

        // thưởng rương như golden web: ["card", tướng, ô, thẻ, độ hiếm], ["shards", tướng, n, mở, đổi], ["exp", n, lên cấp], ["stones"], ["balls", n],
        // ["evo", n] (đá tiến hóa, 2026-11-17), ["egg", khoá túi, n] (trứng capsule, 2026-11-23)
        static object RewardTree(Reward g)
        {
            switch (g.k)
            {
                case RewardKind.Card:
                    return new List<object> { "card", g.drop.hero, SlotKey[(int)g.drop.slot], g.drop.card, Keys.Of(g.drop.rarity) };
                case RewardKind.Shards:
                    return new List<object> { "shards", g.res.hero, (double)g.res.n, g.res.unlocked, (double)g.res.converted };
                case RewardKind.Exp:
                    return new List<object> { "exp", (double)g.n, (double)g.ups };
                case RewardKind.Stones:
                    return new List<object> { "stones" };
                case RewardKind.Balls:
                    return new List<object> { "balls", (double)g.n };
                case RewardKind.EvoStones:
                    return new List<object> { "evo", (double)g.n };
                case RewardKind.Egg:
                    return new List<object> { "egg", g.id, (double)g.n };
                default:
                    throw new InvalidOperationException("Loại thưởng chưa có trong golden: " + g.k);
            }
        }

        // ---------- progression.json "drops" ----------

        static void Progression(GameData d)
        {
            var pg = Load("Golden/progression.json");
            var s = SaveData.New(d, 0, Starter);
            foreach (var id in new[] { "cao_da", "so_ngoc", "giap_long", "giap_nham" }) s.Hero(id).owned = true;
            var r = new Rng(77);
            int n = J.Arr(pg, "drops").Count;
            var drops = new List<object>();
            for (int i = 0; i < n; i++)
            {
                var drop = PokiClash.Core.Progress.RollCardDrop(s, d, (Rarity)r.Int(0, 4), r);
                drops.Add(drop == null ? null : CardDrop(drop));
            }
            pg["drops"] = drops;
            Save("Golden/progression.json", pg);
        }

        // ---------- pachinko.json "chest" ----------

        static void Chest(GameData d)
        {
            var pk = Load("Golden/pachinko.json");
            var c = J.Obj(pk, "chest");
            var s = SaveData.New(d, 0, Starter);
            foreach (var id in new[] { "cao_da", "tien_la", "so_ngoc" }) s.Hero(id).owned = true;
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            var r = new Rng(11);
            foreach (var x in J.Arr(c, "opens"))
            {
                var o = J.Obj(x);
                var got = Pachinko.OpenChest(s, d, Pachinko.FromKey(J.Str(o, "kind")), J.Int(o, "x"), r);
                o["r"] = got.Select(RewardTree).ToList();
            }
            var save = J.Obj(c, "save");
            save["level"] = (double)s.level;
            save["exp"] = (double)s.exp;
            save["balls"] = (double)s.balls;
            SaveCompact("Golden/pachinko.json", pk);
        }

        // ---------- afk.json ----------

        static object ClaimTree(AfkClaim c) => c == null ? null : new Dictionary<string, object>
        {
            ["hours"] = c.hours, ["stage"] = (double)c.stage,
            ["shards"] = c.shards.Select(x => (object)new List<object> { x.hero, (double)x.n, x.unlocked, (double)x.converted }).ToList(),
        };

        static void AfkSteps(GameData d)
        {
            var g = Load("Golden/afk.json");
            var cfg = d.Cfg;
            double t0 = J.Num(g, "t0");
            var s = SaveData.New(d, (long)t0);
            foreach (var id in new[] { "cao_da", "tien_la" }) s.Hero(id).owned = true;
            var rng = new Rng(21);
            foreach (var x in J.Arr(g, "steps"))
            {
                var st = J.Obj(x);
                switch (J.Str(st, "op"))
                {
                    case "tick": st["r"] = Afk.Tick(s, cfg, J.Num(st, "t")); break;
                    case "pending":
                    {
                        var p = Afk.Pending(s, cfg, J.Num(st, "t"));
                        st["r"] = new Dictionary<string, object> { ["hours"] = p.hours, ["full"] = p.full };
                        break;
                    }
                    case "boost": st["r"] = Afk.Boost(s, cfg, J.Num(st, "t")); break;
                    case "claim": st["r"] = ClaimTree(Afk.Claim(s, d, J.Num(st, "t"), J.Int(st, "mult"), rng)); break;
                    case "stage": st["r"] = ClaimTree(Afk.SetStage(s, d, J.Int(st, "id"), J.Num(st, "t"), rng)); break;
                    case "open":
                    {
                        var got = Afk.OpenChest(s, d, J.Num(st, "t"), rng, J.Bool(st, "early"));
                        st["r"] = got?.Select(RewardTree).ToList();
                        break;
                    }
                    case "ad":
                    {
                        var p = J.Str(st, "kind") == "open" ? AdGate.AfkChestOpen : AdGate.AfkBoost;
                        int day = J.Int(st, "day");
                        bool used = AdGate.Use(s, cfg, day, p);
                        st["r"] = new List<object> { used, (double)AdGate.Left(s, cfg, day, p) };
                        break;
                    }
                    case "travel": Afk.Travel(s, J.Num(st, "ms")); break;
                    case "zone": s.zones[(int)Keys.ToElem(J.Str(st, "zone"))] = J.Int(st, "n"); break;
                }
                var a = J.Obj(st, "afk");
                a["hours"] = s.afk.hours;
                a["lastTick"] = s.afk.lastTick;
                a["boostUntil"] = s.afk.boostUntil;
                a["chestAcc"] = s.afk.chestAcc;
                a["chests"] = s.afk.chests.Select(v => (object)v).ToList();
                a["chainAt"] = s.afk.chainAt;
                a["stage"] = (double)s.afk.stage;
                // giờ mở rương tính ở thời điểm của bước (bước không có "t" như ad, zone, travel: như test, J.Num trả 0)
                st["times"] = Afk.ChestTimes(s, cfg, J.Num(st, "t"))
                    .Select(t => (object)new Dictionary<string, object> { ["start"] = t.start, ["ready"] = t.ready }).ToList();
                st["balls"] = (double)s.balls;
                st["exp"] = (double)s.exp;
                st["level"] = (double)s.level;
                st["afkSince"] = (double)s.afkSince;
            }
            Save("Golden/afk.json", g);
        }

        // ---------- farm.json ----------

        static void FarmSteps(GameData d)
        {
            var g = Load("Golden/farm.json");
            var s = SaveData.New(d, 0, Starter);
            foreach (var id in new[] { "cao_da", "tien_la", "so_ngoc", "nguu_quyen" }) s.Hero(id).owned = true;
            s.level = 9;
            s.Hero("so_ngoc").star = 6; // Bạc 1★ = 3 sao cũ (trang trại tính theo sao cũ, StarTier.Legacy)
            double t0 = J.Num(g, "t0");
            g["open"] = (double)Farm.SpotsOpen(d.Cfg, s.level);
            foreach (var x in J.Arr(g, "formula"))
            {
                var o = J.Obj(x);
                string h = M(J.Str(o, "hero"));
                o["hero"] = h;
                o["hours"] = Farm.Hours(s, d, h);
                o["rest"] = Farm.RestMin(s, d, h);
                int n = J.Arr(o, "rates").Count;
                o["rates"] = Enumerable.Range(0, n).Select(i => (object)Farm.Rate(s, d, h, i)).ToList();
            }
            foreach (var x in J.Arr(g, "steps"))
            {
                var o = J.Obj(x);
                double now = t0 + J.Num(o, "t") * H;
                var a = J.Get(o, "a");
                string b = M(J.Str(o, "b"));
                if (b != null) o["b"] = b;
                switch (J.Str(o, "op"))
                {
                    case "tick": o["r"] = Farm.Tick(s, d, now); break;
                    case "place": o["r"] = Farm.Place(s, d, now, (int)N(a), b); break;
                    case "remove": o["r"] = Farm.Remove(s, d, now, (int)N(a)); break;
                    case "harvest": o["r"] = (double)Farm.Harvest(s, d, now); break;
                    case "boost": o["r"] = Farm.Boost(s, d, now); break;
                    case "travel": Farm.Travel(s, N(a) * H); break;
                    case "auto":
                        o["r"] = Farm.Auto(s, d, now).Select(e => (object)new List<object> { (double)e.spot, e.hero }).ToList();
                        break;
                }
                var f = s.farm;
                var wf = J.Obj(o, "farm");
                wf["lastTick"] = f.lastTick;
                wf["boostUntil"] = f.boostUntil;
                wf["spots"] = f.spots.Select(sp => (object)new Dictionary<string, object>
                {
                    ["hero"] = sp.hero, ["energy"] = sp.energy, ["stock"] = sp.stock,
                }).ToList();
                wf["rest"] = f.rest.ToDictionary(kv => kv.Key, kv => (object)N(kv.Value));
                o["balls"] = (double)s.balls;
            }
            Save("Golden/farm.json", g);
        }

        // ---------- potential.json ----------

        static List<object> Lines(PotLine[] a) =>
            a?.Select(x => x == null ? null : (object)new Dictionary<string, object> { ["k"] = Potential.Key(x.k), ["r"] = (double)x.r }).ToList();

        // bản lưu của PotentialTests.FightSave
        static SaveData FightSave(GameData d)
        {
            var s = SaveData.New(d, 0, Starter);
            s.level = 6;
            s.Hero("cao_da").owned = true;
            s.team = new List<string> { Starter, "cao_da" };
            s.Hero(Starter).potential = new[] { new PotLine { k = PotKind.Rage, r = 3 }, new PotLine { k = PotKind.Crit, r = 4 }, new PotLine { k = PotKind.Atk, r = 2 }, null };
            s.Hero("cao_da").potential = new[] { new PotLine { k = PotKind.Mana, r = 2 }, new PotLine { k = PotKind.Lifesteal, r = 3 }, null, null };
            return s;
        }

        static object ModsTree(StatMods m) => m == null ? null : new Dictionary<string, object>
        {
            ["hpPct"] = m.hpPct, ["atkPct"] = m.atkPct, ["defPct"] = m.defPct, ["spd"] = m.spd,
        };

        static void PotentialAll(GameData d)
        {
            var g = Load("Golden/potential.json");
            var cfg = d.Cfg;
            var s = SaveData.New(d, 0, Starter);
            s.Hero(Starter).star = 8; // sao tổng (2026-11-17): 4 ô như PotentialTests
            s.Hero("cao_da").owned = true;
            s.Hero("cao_da").star = 3; // 2 ô
            s.potentialStones = 300;
            var rng = new Rng(41);
            foreach (var x in J.Arr(g, "spins"))
            {
                var o = J.Obj(x);
                string hero = M(J.Str(o, "hero"));
                o["hero"] = hero;
                var locks = J.Arr(o, "locks").Select(v => (bool)v).ToList();
                o["cost"] = (double)Potential.SpinCost(s, cfg, hero, locks);
                var res = Potential.Spin(s, cfg, hero, locks, rng);
                o["res"] = Lines(res);
                if (res != null) Potential.Keep(s, hero, J.Bool(o, "keepNew"));
                o["stones"] = (double)s.potentialStones;
                o["pot"] = Lines(s.Hero(hero).potential);
            }

            var fs = FightSave(d);
            g["members"] = Teams.Player(fs, null, d).members.Select(m => (object)new Dictionary<string, object>
            {
                ["hero"] = m.heroId, ["mods"] = ModsTree(m.mods),
                ["start"] = m.start == null ? null : new Dictionary<string, object>
                {
                    ["mana"] = m.start.mana, ["rage"] = m.start.rage, ["crit"] = m.start.crit, ["lifesteal"] = m.start.lifesteal,
                },
            }).ToList();
            foreach (var x in J.Arr(g, "fights"))
            {
                var o = J.Obj(x);
                var team = Teams.Player(fs, null, d);
                team.ai = true;
                var b = Battle.Create(d, team, Teams.Enemy(AtLevel(d.Stage(J.Int(o, "stage")), J.Int(o, "foeLevel")), d), (uint)J.Num(o, "seed"), 6, 6);
                var f0 = b.sides[0].fighters[0];
                o["start"] = new Dictionary<string, object>
                {
                    ["mana"] = f0.mana, ["rage"] = f0.rage,
                    ["buffs"] = f0.buffs.Select(bf => (object)new List<object> { Keys.Of(bf.stat), bf.v, (double)bf.left }).ToList(),
                };
                BattleSim.Run(b);
                o["winner"] = (double)b.winner;
                o["round"] = (double)b.round;
            }
            Save("Golden/potential.json", g);
        }

        // như TestData.AtLevel: bản sao của ải với mọi địch ở cấp lv
        static StageDef AtLevel(StageDef st, int lv)
        {
            var c = new StageDef { id = st.id, zone = st.zone, idx = st.idx, name = st.name, kind = st.kind, tag = st.tag, chapter = st.chapter, drops = st.drops };
            foreach (var e in st.enemies) c.enemies.Add(new StageEnemy { hero = e.hero, level = lv, boss = e.boss, evo = e.evo, buff = e.buff });
            return c;
        }

        // ---------- badges.json ----------

        static void BadgesAll(GameData d)
        {
            var g = Load("Golden/badges.json");
            var cfg = d.Cfg;
            // BadgeTests.StatSave
            var s = SaveData.New(d, 0);
            foreach (var id in new[] { "cao_da", "tien_la", "so_ngoc", "giap_long" }) s.Hero(id).owned = true;
            s.badges[(int)Elem.Thuy].tier = 2;
            s.badges[(int)Elem.Hoa].tier = 5;
            foreach (var x in J.Arr(g, "stats"))
            {
                var o = J.Obj(x);
                var h = d.Hero(M(J.Str(o, "hero")));
                o["hero"] = h.id;
                var m = Teams.MemberOf(s, h.id, d);
                o["mods"] = ModsTree(m.mods);
                var st = HeroStats.Compute(cfg, h, 9, 2, false, m.mods);
                o["stats"] = new Dictionary<string, object> { ["hp"] = N(st.hp), ["atk"] = N(st.atk), ["def"] = N(st.def), ["spd"] = N(st.spd) };
            }

            // BadgeTests.TienDo_MoDen_LenBac_Ruong_KhopBanWeb
            var t = SaveData.New(d, 0, Starter);
            t.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            t.zones[(int)Elem.Kim] = Islands.MiniAt(Elem.Kim);
            var rng = new Rng(31);
            var steps = J.Arr(g, "steps");
            var first = J.Obj(steps[0]);
            first["temple"] = Badges.TempleOpen(t);
            first["lines"] = d.Zones.Select(z => (object)Badges.LineOpen(t, z.id)).ToList();
            for (int k = 1; k < steps.Count; k++)
            {
                var o = J.Obj(steps[k]);
                var z = Keys.ToElem(J.Str(o, "zone"));
                var r = Badges.Win(t, d, z, rng);
                o["gain"] = (double)(r?.balls ?? 0);
                o["tierDone"] = (double)(r?.tierDone ?? 0);
                o["chest"] = r != null && r.tierDone > 0 ? Pachinko.Key(r.chest) : null;
                o["rewards"] = r == null ? new List<object>() : r.rewards.Select(w => w.k == RewardKind.Card
                    ? (object)new List<object> { "card", w.drop.hero, w.drop.card }
                    : new List<object> { w.k == RewardKind.Balls ? "balls" : w.k == RewardKind.Exp ? "exp" : w.k == RewardKind.Stones ? "stones" : w.k.ToString(), (double)w.n }).ToList();
                var cur = Badges.Current(t, cfg, z);
                o["cur"] = cur == null ? null : new Dictionary<string, object> { ["tier"] = (double)cur.Value.tier, ["i"] = (double)cur.Value.i };
                o["balls"] = (double)t.balls;
                o["exp"] = (double)t.exp;
                o["level"] = (double)t.level;
                o["badges"] = d.Zones.ToDictionary(zz => Keys.Of(zz.id), zz => (object)new Dictionary<string, object>
                {
                    ["tier"] = (double)t.badges[(int)zz.id].tier, ["won"] = (double)t.badges[(int)zz.id].won,
                });
            }
            Save("Golden/badges.json", g);
        }
    }
}
