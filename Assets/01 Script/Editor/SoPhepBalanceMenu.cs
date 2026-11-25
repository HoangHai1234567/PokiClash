// Đo Sổ Phép (GD_Claude/28_SoPhep.md, ngân sách người dùng duyệt 2026-11-24: cả sổ không quá +3 cấp tương đương, không nâng địch):
// - "Sổ Phép: đo ngân sách cấp tương đương": mỗi đảo 3 ải (25, 50, 70), đội mẫu của đảo (simTeams) ở cấp của ải với sao, thẻ của người
//   chơi "vừa" (Teams.EnemyStar, EnemyCard); tỉ lệ thắng không sổ ở cấp L, L+2, L+4, L+6, L+8 và có sổ ở cấp L (sổ người "vừa" có ở
//   cấp đó: vẽ theo đường gợi ý bằng nét của cấp L, đá đủ, chúa tể từ cấp 185); số cấp tương đương = điểm cắt nội suy.
// - "Sổ Phép: so hai mặt của ô chọn": sổ đầy (cấp 200, mọi chương), mỗi ô chọn đổi lần lượt từng mặt, tỉ lệ thắng trung bình 5 ải cuối
//   đảo và 5 ải giữa đảo; mặt nào thua xa ở mọi chỗ thì phải sửa số.
// - "Sổ Phép: nhịp 60 ngày có / không sổ": ProgressSim ba kiểu người chơi, ProgressSim.SoPhepOn bật / tắt.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class SoPhepBalanceMenu
    {
        const int N = 150;

        static GameData Load()
        {
            string R(string f) => File.ReadAllText(Path.Combine(Application.dataPath, "02 Data/Json", f));
            return GameData.FromJson(R("heroes.json"), R("cards.json"), R("zones.json"), R("stages.json"), R("balance.json"));
        }

        // đội mẫu ở cấp level, sao và thẻ của người chơi "vừa" ở cấp đó; book: sổ (bản sao) hoặc null
        static SaveData Player(GameData d, List<string> team, int level, SoPhepState book)
        {
            var s = Sim.Setup(d, team, level, Teams.EnemyStar(level), Teams.EnemyCard(level), team[0]);
            if (book != null) s.sophep = Clone(book);
            return s;
        }

        static double Win(GameData d, SaveData s, StageDef st, List<string> team) => Sim.Stage(d, s, st, N, 1000, team).WinRate;

        [MenuItem("PokiClash/Cân bằng nhanh/Sổ Phép: đo ngân sách cấp tương đương (ghi Console)", priority = 30)]
        static void Budget()
        {
            var d = Load();
            var cfg = d.Cfg;
            var sb = new StringBuilder();
            var deltas = new List<double>();
            var drop = new Dictionary<string, List<double>>(); // cấp tương đương mất đi khi bỏ riêng từng ô
            var t0 = DateTime.Now;
            try
            {
                int k = 0;
                foreach (var z in Elements.All)
                {
                    var team = cfg.SimTeamOf(z)?.team;
                    if (team == null || team.Count == 0) continue;
                    foreach (int idx in new[] { 25, 50, 70 })
                    {
                        if (EditorUtility.DisplayCancelableProgressBar("Sổ Phép", $"{z} ải {idx}", k++ / 15f)) throw new OperationCanceledException();
                        var st = d.ZoneStages(z).FirstOrDefault(x => x.idx == idx);
                        if (st == null) continue;
                        int L = Teams.StageLead(st, d).level;
                        if (L < cfg.sophep.openLevel) continue; // chưa có sổ ở cấp này
                        // cấp gốc: hạ dần cấp đội mẫu tới khi không sổ chỉ thắng ≤ 70% (đo ở vùng tỉ lệ thắng còn nhạy)
                        int Lb = L;
                        double w0b = Win(d, Player(d, team, Lb, null), st, team);
                        while (w0b > 0.7 && Lb > L - 40 && Lb > 1)
                        {
                            Lb = Math.Max(1, Lb - 3);
                            w0b = Win(d, Player(d, team, Lb, null), st, team);
                        }
                        if (w0b > 0.7)
                        {
                            sb.Append($"  {z} ải {idx} (cấp {L}): đội mẫu vẫn thắng {w0b:P0} ở cấp {Lb}, bỏ qua\n");
                            continue;
                        }
                        // sổ của người chơi ở cấp L (nét của cấp L), đánh ở cấp gốc Lb
                        var book = Book(d, L);
                        double w1 = Win(d, Player(d, team, Lb, book), st, team);
                        var curve = new List<double> { w0b };
                        for (int i = 1; i <= 6; i++) curve.Add(Win(d, Player(d, team, Math.Min(cfg.maxLevel, Lb + 2 * i), null), st, team));
                        double eq = Eq(curve, w1);
                        deltas.Add(eq);
                        int spent = SoPhep.Spent(new SaveData { sophep = book }, cfg);
                        sb.Append($"  {z} ải {idx} (cấp ải {L}, đo ở cấp {Lb}, sổ {spent} nét): không sổ {w0b:P0}, có sổ {w1:P0}; " +
                                  $"không sổ +2…+12 cấp: {string.Join("/", curve.Skip(1).Select(w => w.ToString("P0")))} → ≈ +{eq:0.0} cấp{(eq >= 12 ? " (trở lên)" : "")}\n");
                        // bỏ riêng từng ô đang vẽ
                        foreach (var id in book.lv.Keys.ToList())
                        {
                            var less = Clone(book);
                            less.lv.Remove(id);
                            double wl = Win(d, Player(d, team, Lb, less), st, team);
                            double eql = Eq(curve, wl);
                            if (!drop.TryGetValue(id, out var lst)) drop[id] = lst = new List<double>();
                            lst.Add(eq - eql);
                        }
                    }
                }
                var top = drop.Select(kv => (id: kv.Key, v: kv.Value.Average(), n: kv.Value.Count)).OrderByDescending(x => x.v);
                sb.Append("Bỏ riêng từng ô (cấp tương đương mất đi, trung bình các ải đo được):\n");
                foreach (var x in top) sb.Append($"  {cfg.sophep.Node(x.id)?.Name ?? x.id} (mặt {SoPhepFace(cfg, x.id)}): {x.v:+0.0;-0.0;0.0} cấp ({x.n} ải)\n");
                Debug.Log($"[Sổ Phép] Ngân sách (trần đề xuất +3 cấp): trung bình +{(deltas.Count > 0 ? deltas.Average() : 0):0.0} cấp, lớn nhất +{(deltas.Count > 0 ? deltas.Max() : 0):0.0}; " +
                          $"{N} trận mỗi ô, {(DateTime.Now - t0).TotalSeconds:0} giây\n" + sb);
            }
            catch (OperationCanceledException)
            {
                Debug.Log("[Sổ Phép] Đo ngân sách: đã dừng.\n" + sb);
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }

        // sổ người chơi có ở cấp level theo đường gợi ý (đá đủ, chúa tể từ cấp 185, nét EXP đủ ở cấp tối đa)
        static SoPhepState Book(GameData d, int level)
        {
            var s = SaveData.New(d, 0);
            s.level = level;
            s.evoStones = 9999;
            s.sophep = new SoPhepState { expPoints = level >= d.Cfg.maxLevel ? d.Cfg.sophep.expPoints : 0 };
            if (level >= 185) s.zones[0] = Islands.Size(Elements.All[0]);
            SoPhep.AutoBuy(s, d.Cfg);
            return s.sophep;
        }

        static SoPhepState Clone(SoPhepState b) => new SoPhepState
        {
            lv = new Dictionary<string, int>(b.lv), face = new Dictionary<string, int>(b.face), stones = b.stones, expPoints = b.expPoints,
        };

        static string SoPhepFace(BalanceConfig cfg, string id)
        {
            var n = cfg.sophep.Node(id);
            if (n == null || n.FaceCount <= 1) return "-";
            int f = 0;
            foreach (var step in cfg.sophep.path)
                if (step.StartsWith(id + ":") && int.TryParse(step.Substring(id.Length + 1), out var x)) f = x;
            return n.FaceName(f);
        }

        // số cấp tương đương: chỗ tỉ lệ thắng w cắt đường không sổ (curve[i] ở +2i cấp), nội suy tuyến tính; trần 12
        static double Eq(List<double> curve, double w)
        {
            if (w <= curve[0]) return 0;
            for (int i = 1; i < curve.Count; i++)
                if (w <= curve[i])
                {
                    double a = curve[i - 1], b = curve[i];
                    return 2 * (i - 1) + 2 * (b > a ? (w - a) / (b - a) : 1);
                }
            return 2 * (curve.Count - 1);
        }

        [MenuItem("PokiClash/Cân bằng nhanh/Sổ Phép: so hai mặt của ô chọn (ghi Console)", priority = 31)]
        static void Faces()
        {
            var d = Load();
            var cfg = d.Cfg;
            var sb = new StringBuilder();
            var t0 = DateTime.Now;
            try
            {
                var picks = cfg.sophep.nodes.Where(n => n.FaceCount > 1 && n.kind != "deco").ToList();
                int k = 0;
                foreach (var n in picks)
                {
                    var res = new List<string>();
                    for (int f = 0; f < n.FaceCount; f++)
                    {
                        if (EditorUtility.DisplayCancelableProgressBar("Sổ Phép", $"{n.id} mặt {f}", k++ / (float)picks.Sum(x => x.FaceCount)))
                            throw new OperationCanceledException();
                        double mid = 0, end = 0;
                        int cm = 0, ce = 0;
                        foreach (var z in Elements.All)
                        {
                            var team = cfg.SimTeamOf(z)?.team;
                            if (team == null || team.Count == 0) continue;
                            foreach (int idx in new[] { 50, 70 })
                            {
                                var st = d.ZoneStages(z).FirstOrDefault(x => x.idx == idx);
                                if (st == null) continue;
                                int L = Teams.StageLead(st, d).level;
                                var book = Book(d, d.Cfg.maxLevel); // sổ đầy
                                var s = Player(d, team, Math.Max(L - 12, 1), book);
                                SoPhep.SetFace(s, cfg, n.id, f);
                                double w = Win(d, s, st, team);
                                if (idx == 70)
                                {
                                    end += w;
                                    ce++;
                                }
                                else
                                {
                                    mid += w;
                                    cm++;
                                }
                            }
                        }
                        res.Add($"{n.FaceName(f)} giữa đảo {mid / Math.Max(1, cm):P0}, cuối đảo {end / Math.Max(1, ce):P0}");
                    }
                    sb.Append($"  {n.Name}: {string.Join(" | ", res)}\n");
                }
                Debug.Log($"[Sổ Phép] Hai mặt của ô chọn ({N} trận mỗi ô, {(DateTime.Now - t0).TotalSeconds:0} giây)\n" + sb);
            }
            catch (OperationCanceledException)
            {
                Debug.Log("[Sổ Phép] So hai mặt: đã dừng.\n" + sb);
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }

        [MenuItem("PokiClash/Cân bằng nhanh/Sổ Phép: nhịp 60 ngày có và không có sổ (ghi Console)", priority = 32)]
        static void Pace()
        {
            var sb = new StringBuilder();
            var t0 = DateTime.Now;
            var cache = new Dictionary<string, double>();
            bool keep = ProgressSim.SoPhepOn;
            try
            {
                foreach (bool on in new[] { false, true })
                {
                    ProgressSim.SoPhepOn = on;
                    var d = Load();
                    sb.Append(on ? "Có sổ:\n" : "Không sổ:\n");
                    foreach (var p in ProgressSim.DefaultProfiles())
                    {
                        if (EditorUtility.DisplayCancelableProgressBar("Sổ Phép", $"{(on ? "có" : "không")} sổ: {p.name}", on ? 0.5f : 0)) throw new OperationCanceledException();
                        int full = -1, spent30 = 0;
                        var r = ProgressSim.Run(d, p, 60, 1, 8, cache, null, null, (day, s) =>
                        {
                            if (full < 0 && SoPhep.Spent(s, d.Cfg) >= SoPhep.Total(d.Cfg)) full = day;
                            if (day == 30) spent30 = SoPhep.Spent(s, d.Cfg);
                        });
                        int top = Array.FindIndex(r.level, l => l >= d.Cfg.maxLevel);
                        int income = Math.Max(1, r.ballsFromStages + r.ballsFromTrees + r.ballsFromFarm);
                        sb.Append($"  {p.name}: cấp ngày 30/45/60 = {r.level[30]}/{r.level[45]}/{r.level[60]}; cấp 200: {(top < 0 ? "chưa" : "ngày " + top)}; " +
                                  $"bi ải {100 * r.ballsFromStages / income}%; ải {r.cleared[60]}; thắng {r.wins}/{r.battles}" +
                                  (on ? $"; sổ ngày 30: {spent30} nét; đầy sổ: {(full < 0 ? "chưa" : "ngày " + full)}" : "") + "\n");
                    }
                }
                Debug.Log($"[Sổ Phép] Nhịp 60 ngày ({(DateTime.Now - t0).TotalSeconds:0} giây; mục tiêu: vừa cấp 200 ~ngày 45, bi ải ≥ 25%, ít ≥ cấp 80 ngày 30)\n" + sb);
            }
            catch (OperationCanceledException)
            {
                Debug.Log("[Sổ Phép] Nhịp: đã dừng.\n" + sb);
            }
            finally
            {
                ProgressSim.SoPhepOn = keep;
                EditorUtility.ClearProgressBar();
            }
        }
    }
}
