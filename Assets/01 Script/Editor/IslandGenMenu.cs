// Menu của bộ sinh ải đảo 70 ải (IslandGen.cs):
// - "PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (Thủy, Hỏa, Mộc)": ghi lại các ải của mọi đảo có kế hoạch (IslandGen.All) trong stages.json
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

        [MenuItem("PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (Thủy, Hỏa, Mộc) (stages.json)", priority = 11)]
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
        // (như ProgressionTests), badges.json "stages" (đội địch đền huy hiệu, BadgeTests), potential.json "caveStages" (PotentialTests).
        // Giữ danh sách ô cần so của golden cũ, chỉ tính lại số; các mục khác giữ nguyên.
        [MenuItem("PokiClash/Thử/Tính lại golden theo danh sách tướng (progression, badges, potential)", priority = 302)]
        static void HeroGoldens()
        {
            var d = Load();
            var pg = J.Obj(MiniJson.Parse(R("Golden/progression.json")));
            var stats = new List<object>();
            foreach (var h in d.Heroes)
                foreach (int lv in new[] { 1, 10, 20, 30 })
                    foreach (int star in new[] { 1, 3, 5 })
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
            foreach (var x in J.Arr(bg, "stages"))
            {
                var o = J.Obj(x);
                var z = Keys.ToElem(J.Str(o, "zone"));
                int tier = J.Int(o, "tier"), i = J.Int(o, "i");
                var st = Badges.Stage(d, z, tier, i);
                o["id"] = (double)st.id;
                o["seed"] = (double)Badges.Seed(d, z, tier, i);
                o["kind"] = st.kind == StageKind.Boss ? "boss" : "mini";
                o["enemies"] = st.enemies.Select(e => (object)new List<object> { e.hero, (double)e.level, e.boss }).ToList();
            }
            File.WriteAllText(Data("Golden/badges.json"), IslandGen.Write(bg) + "\n");

            var pt = J.Obj(MiniJson.Parse(R("Golden/potential.json")));
            foreach (var x in J.Arr(pt, "caveStages"))
            {
                var o = J.Obj(x);
                var st = Potential.CaveStage(d, Keys.ToElem(J.Str(o, "zone")), J.Int(o, "tier"));
                o["id"] = (double)st.id;
                o["enemies"] = st.enemies.Select(e => (object)new List<object> { e.hero, (double)e.level, e.boss }).ToList();
            }
            File.WriteAllText(Data("Golden/potential.json"), IslandGen.Write(pt) + "\n");
            AssetDatabase.Refresh();
            Debug.Log($"[Golden] Đã tính lại progression ({stats.Count} chỉ số, {shards.Count} lần rơi mảnh), badges, potential");
        }
    }
}
