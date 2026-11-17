// Menu của bộ sinh ải đảo 70 ải (IslandGen.cs):
// - "PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (5 đảo)": ghi lại các ải của mọi đảo có kế hoạch (IslandGen.All) trong stages.json
//   (đánh lại id toàn cục), rồi chạy "Nhập dữ liệu". Sửa kế hoạch đảo (tướng, tên chặng, lính, đỉnh cấp, cường hóa) trong IslandGen.cs
//   rồi chạy menu này. Cấp đảo trong zones.json ([1, đỉnh]) sửa tay cho khớp levelMax của kế hoạch.
// - "PokiClash/Thử/Tính lại golden islands, roster, cardtext, zones": ghi 4 golden phụ thuộc dữ liệu ải, tướng, thẻ từ code hiện tại.
//   sim.json và battles.json tính lại bằng menu "Tính lại golden sim, tướng trên nút ải" (GoldenRecalcMenu).
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class IslandGenMenu
    {
        static string Data(string f) => Path.Combine(Application.dataPath, "02 Data", f);
        static string R(string f) => File.ReadAllText(Data(f));
        static GameData Load() =>
            GameData.FromJson(R("Json/heroes.json"), R("Json/cards.json"), R("Json/zones.json"), R("Json/stages.json"), R("Json/balance.json"));

        [MenuItem("PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (5 đảo) (stages.json)", priority = 11)]
        static void Regen()
        {
            var d = Load();
            string sj = R("Json/stages.json");
            foreach (var p in IslandGen.All) sj = IslandGen.ApplyToStages(sj, p, d);
            File.WriteAllText(Data("Json/stages.json"), sj);
            AssetDatabase.Refresh();
            DataImporter.Import();
            Debug.Log($"[Đảo] Đã sinh lại {IslandGen.All.Length} đảo 70 ải và nhập dữ liệu");
        }

        [MenuItem("PokiClash/Thử/Tính lại golden islands, roster, cardtext, zones", priority = 301)]
        static void Goldens()
        {
            var d = Load();
            File.WriteAllText(Data("Golden/islands.json"), IslandGen.IslandsGolden(d));
            File.WriteAllText(Data("Golden/roster.json"), IslandGen.RosterGolden(d, R("Golden/roster.json")));
            File.WriteAllText(Data("Golden/cardtext.json"), IslandGen.CardTextGolden(d));
            File.WriteAllText(Data("Golden/zones.json"), IslandGen.ZonesGolden(d, R("Golden/zones.json")));
            AssetDatabase.Refresh();
            Debug.Log("[Golden] Đã tính lại islands.json, roster.json, cardtext.json, zones.json");
        }

        // Golden phụ thuộc danh sách tướng (thêm, bớt tướng hay đổi độ hiếm, chỉ số): progression.json "stats", "shards", "shardEnd"
        // (như ProgressionTests), badges.json "stages" (đội địch đền huy hiệu, BadgeTests) và "fights" (5 trận thật, từ 2026-11-11),
        // potential.json "caveStages" (PotentialTests).
        // Giữ danh sách ô cần so của golden cũ, chỉ tính lại số; các mục khác giữ nguyên.
        [MenuItem("PokiClash/Thử/Tính lại golden theo danh sách tướng (progression, badges, potential)", priority = 302)]
        static void HeroGoldens()
        {
            var d = Load();
            var pg = J.Obj(MiniJson.Parse(R("Golden/progression.json")));
            var stats = new List<object>();
            foreach (var h in d.Heroes)
                foreach (int lv in new[] { 1, 10, 20, 30 })
                    foreach (int star in new[] { 1, 6, 20 }) // sao tổng (bậc sao 2026-11-17): Đồng 1★, Bạc 1★, Kim Cương 5★
                        foreach (bool boss in new[] { false, true })
                        {
                            var s = HeroStats.Compute(d.Cfg, h, lv, star, boss);
                            stats.Add(new Dictionary<string, object>
                            {
                                ["id"] = h.id, ["lv"] = (double)lv, ["st"] = (double)star, ["boss"] = boss,
                                ["hp"] = s.hp, ["atk"] = s.atk, ["def"] = s.def, ["spd"] = s.spd,
                            });
                        }
            pg["stats"] = stats;
            // rơi mảnh ngẫu nhiên như ProgressionTests.ManhTuong (hạt giống 5, số lần như golden cũ)
            var save = SaveData.New(d, 0);
            var rng = new Rng(5);
            var shards = new List<object>();
            for (int k = J.Arr(pg, "shards").Count; k > 0; k--)
            {
                string hero = d.Heroes[rng.Int(0, d.Heroes.Count - 1)].id;
                int n = rng.Int(1, 6);
                var res = PokiClash.Core.Progress.AddShards(save, d, hero, n, rng);
                shards.Add(new List<object> { hero, (double)n, res.unlocked, (double)res.converted });
            }
            pg["shards"] = shards;
            pg["shardEnd"] = d.Heroes.Select(h =>
            {
                var p = save.Hero(h.id);
                return (object)new List<object>
                {
                    h.id, p.owned, (double)p.shards, (double)p.skill.copies, (double)p.ult.copies, (double)p.passive.copies,
                };
            }).ToList();
            File.WriteAllText(Data("Golden/progression.json"), IslandGen.Write(pg) + "\n");

            var bg = J.Obj(MiniJson.Parse(R("Golden/badges.json")));
            // đội địch đền: dựng lại đủ mọi trận của 5 dãy (2026-11-17: 10 bậc, số trận mỗi bậc đổi), kèm cường hóa của địch
            var bstages = new List<object>();
            foreach (var zd in d.Zones.OrderBy(zz => zz.order))
                for (int tier = 1; tier <= Badges.MaxTier(d.Cfg); tier++)
                    for (int i = 1; i <= Badges.Count(d.Cfg, tier); i++)
                    {
                        var st = Badges.Stage(d, zd.id, tier, i);
                        bstages.Add(new Dictionary<string, object>
                        {
                            ["zone"] = Keys.Of(zd.id), ["tier"] = (double)tier, ["i"] = (double)i, ["id"] = (double)st.id,
                            ["seed"] = (double)Badges.Seed(d, zd.id, tier, i), ["kind"] = st.kind == StageKind.Boss ? "boss" : "mini",
                            ["enemies"] = st.enemies.Select(e => (object)new List<object> { e.hero, (double)e.level, e.boss, e.buff }).ToList(),
                        });
                    }
            bg["stages"] = bstages;
            // 5 trận đánh thật bậc Đồng hệ Thủy, đúng như BadgeTests.ChiSoCoHuyHieu_VaTranThat_KhopBanWeb (bản lưu StatSave, cấp 9, đội có
            // tướng khởi đầu, địch ở cấp foeLevel như TestData.AtLevel): bên thắng, số hiệp. Đối thủ đền chọn theo danh sách tướng cùng hệ
            // nên thêm tướng Thủy là đổi (lô 10 tướng mới 2026-11-11)
            var fs = SaveData.New(d, 0);
            foreach (var id in new[] { "vo_su", "tien_la", "so_ngoc", "giap_long" }) fs.Hero(id).owned = true;
            fs.badges[(int)Elem.Thuy].tier = 2;
            fs.badges[(int)Elem.Hoa].tier = 5;
            fs.level = 9;
            fs.team = new List<string> { "ti_tach", "so_ngoc", "giap_long" };
            foreach (var x in J.Arr(bg, "fights"))
            {
                var o = J.Obj(x);
                int i = J.Int(o, "i"), foeLv = J.Int(o, "foeLevel");
                var src = Badges.Stage(d, Elem.Thuy, 1, i);
                var stage = new StageDef
                {
                    id = src.id, zone = src.zone, idx = src.idx, name = src.name, kind = src.kind, tag = src.tag, chapter = src.chapter, drops = src.drops,
                };
                foreach (var e in src.enemies) stage.enemies.Add(new StageEnemy { hero = e.hero, level = foeLv, boss = e.boss, evo = e.evo, buff = e.buff });
                var team = Teams.Player(fs, null, d);
                team.ai = true;
                var b = Battle.Create(d, team, Teams.Enemy(stage, d), Badges.Seed(d, Elem.Thuy, 1, i), 9, System.Math.Max(9, stage.enemies[0].level));
                BattleSim.Run(b);
                o["winner"] = (double)b.winner;
                o["round"] = (double)b.round;
            }
            File.WriteAllText(Data("Golden/badges.json"), IslandGen.Write(bg) + "\n");

            var pt = J.Obj(MiniJson.Parse(R("Golden/potential.json")));
            // đội địch Hang: dựng lại đủ mọi tầng của 5 hệ (2026-11-17: 10 tầng), kèm cường hóa của địch
            var cstages = new List<object>();
            foreach (var zd in d.Zones.OrderBy(zz => zz.order))
                for (int tier = 0; tier < d.Cfg.cave.tiers.Count; tier++)
                {
                    var st = Potential.CaveStage(d, zd.id, tier);
                    cstages.Add(new Dictionary<string, object>
                    {
                        ["zone"] = Keys.Of(zd.id), ["tier"] = (double)tier, ["id"] = (double)st.id,
                        ["enemies"] = st.enemies.Select(e => (object)new List<object> { e.hero, (double)e.level, e.boss, e.buff }).ToList(),
                    });
                }
            pt["caveStages"] = cstages;
            File.WriteAllText(Data("Golden/potential.json"), IslandGen.Write(pt) + "\n");
            AssetDatabase.Refresh();
            Debug.Log($"[Golden] Đã tính lại progression ({stats.Count} chỉ số, {shards.Count} lần rơi mảnh), badges, potential");
        }
    }
}
