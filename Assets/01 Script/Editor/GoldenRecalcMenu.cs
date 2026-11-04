// Tính lại số của hai golden phụ thuộc luật trận và dữ liệu ải, sau khi đổi luật bên Unity (CLAUDE.md: đổi luật thì sửa golden):
// - sim.json: bảng mọi ải × 5 mức cấp, đúng cách SimTests.BangAi_KhopTungO_VoiBanWeb tính (đội mẫu từng đảo, số trận n của golden);
// - roster.json "leads": tướng và sao (dạng) đứng trên nút ải, đúng cách RosterTests.TuongTrenNutAi_KhopBanWeb tính;
// - battles.json, battle_events.json: 200 trận cố định hạt giống chạy lại như BattleGoldenTests (kết quả, chuỗi sự kiện, ảnh chụp cuối;
//   các trận chi tiết so từng sự kiện).
// Menu "PokiClash/Thử/Tính lại golden sim, tướng trên nút ải (Temp/GoldenRecalc.json)" ghi số mới ra Temp/GoldenRecalc.json; ghép
// vào golden bằng script (chỉ đổi ô khác, giữ định dạng file), rồi chạy lại test. Dùng lần đầu 2026-11-04 khi bật tiến hóa ở ải tướng.
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class GoldenRecalcMenu
    {
        static string DataDir => Path.Combine(Application.dataPath, "02 Data");

        [MenuItem("PokiClash/Thử/Tính lại golden sim, tướng trên nút ải (Temp/GoldenRecalc.json)", priority = 300)]
        static void Run()
        {
            string R(string f) => File.ReadAllText(Path.Combine(DataDir, f));
            var d = GameData.FromJson(R("Json/heroes.json"), R("Json/cards.json"), R("Json/zones.json"), R("Json/stages.json"), R("Json/balance.json"));
            var g = J.Obj(MiniJson.Parse(R("Golden/sim.json")));
            int n = J.Int(g, "n");

            var zones = new List<object>();
            foreach (var zx in J.Arr(g, "zones"))
            {
                var zone = d.Zone(Keys.ToElem(J.Str(J.Obj(zx), "zone")));
                var levels = Sim.Levels(zone);
                var tm = d.Cfg.SimTeamOf(zone.id);
                var stages = new List<object>();
                foreach (var st in d.ZoneStages(zone.id))
                {
                    var cells = new List<object>();
                    foreach (int lv in levels)
                    {
                        var c = Sim.Stage(d, Sim.Setup(d, tm.team, lv, tm.star, tm.card), st, n);
                        cells.Add(new Dictionary<string, object> { ["win"] = (double)c.win, ["rounds"] = c.rounds });
                    }
                    stages.Add(new Dictionary<string, object> { ["id"] = (double)st.id, ["cells"] = cells });
                }
                zones.Add(new Dictionary<string, object> { ["zone"] = Keys.Of(zone.id), ["stages"] = stages });
            }

            var leads = new List<object>();
            foreach (var st in d.Stages)
            {
                var en = Teams.StageLead(st, d);
                leads.Add(new Dictionary<string, object> { ["id"] = (double)st.id, ["hero"] = en.hero, ["star"] = (double)Teams.EnemyFormStar(en) });
            }

            // 200 trận cố định hạt giống (BattleGoldenTests): kết quả, chuỗi sự kiện, ảnh chụp cuối; các trận đầu so từng sự kiện
            var battles = new List<object>();
            var detail = new List<object>();
            var bj = J.Arr(J.Obj(MiniJson.Parse(R("Golden/battles.json"))), "battles");
            int nDetail = J.Arr(J.Obj(MiniJson.Parse(R("Golden/battle_events.json"))), "battles").Count;
            for (int i = 0; i < bj.Count; i++)
            {
                var entry = J.Obj(bj[i]);
                var teams = J.Arr(entry, "teams");
                var unlock = J.Arr(entry, "unlock");
                var battle = Battle.Create(d, Team(J.Obj(teams[0])), Team(J.Obj(teams[1])), (uint)J.Num(entry, "seed"),
                    (int)(double)unlock[0], (int)(double)unlock[1]);
                var log = new List<BattleEvent>();
                var b = BattleSim.Run(battle, 0.15, log);
                battles.Add(new Dictionary<string, object>
                {
                    ["seed"] = J.Num(entry, "seed"), ["winner"] = (double)b.winner, ["round"] = (double)b.round, ["turns"] = (double)b.turns,
                    ["events"] = (double)log.Count, ["kinds"] = string.Join(",", log.ConvertAll(e => e.TypeKey)),
                    ["dmg"] = new List<object> { b.dmgDealt[0], b.dmgDealt[1] }, ["last"] = BattleEvent.SnapDict(log[log.Count - 1].snap),
                });
                if (i < nDetail) detail.Add(log.ConvertAll(e => (object)e.ToDict()));
            }

            var outPath = Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/GoldenRecalc.json"));
            File.WriteAllText(outPath, MiniJson.Write(new Dictionary<string, object>
            {
                ["sim"] = zones, ["leads"] = leads, ["battles"] = battles, ["detail"] = detail,
            }, true));
            Debug.Log($"[Golden] Đã tính lại {d.Stages.Count} ải (sim n={n}, tướng trên nút ải), {battles.Count} trận ({detail.Count} trận chi tiết): {outPath}");
        }

        // đội trong battles.json (như BattleGoldenTests.Team)
        static TeamSetup Team(Dictionary<string, object> o)
        {
            var t = new TeamSetup { name = J.Str(o, "name"), ai = J.Bool(o, "ai") };
            foreach (var x in J.Arr(o, "members"))
            {
                var m = J.Obj(x);
                var cl = J.Obj(m, "cardLv");
                t.members.Add(new Member
                {
                    heroId = J.Str(m, "heroId"), level = J.Int(m, "level"), star = J.Int(m, "star"), boss = J.Bool(m, "boss"), evo = J.Bool(m, "evo"),
                    cardSkill = J.Int(cl, "skill"), cardUlt = J.Int(cl, "ult"), cardPassive = J.Int(cl, "passive"),
                });
            }
            return t;
        }
    }
}
