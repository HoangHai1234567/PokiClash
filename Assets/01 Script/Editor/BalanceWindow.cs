// Cửa sổ "PokiClash/Cân bằng": chạy trong Editor, không cần Play (gọi thẳng Core, dữ liệu nạp từ Assets/02 Data/Json).
// - Trận: N trận máy tự chơi cho một ải, một đảo hoặc cả 40 ải; đội, cấp, sao, cấp thẻ, phần cộng side meta; bảng %thắng và
//   số hiệp trung bình; xuất CSV. Đội gợi ý + 5 mức cấp quanh khoảng đề nghị cho ra đúng số của npm run sim -- battle.
// - Máy bi: thả 6.000 bi theo độ rộng ô chọn được; tỉ lệ từng ô, giá trị rương, EXP / bi hoàn / thẻ mỗi bi; cảnh báo bi hoàn > 0,5.
// - Tiến độ: 30 ngày × 3 kiểu người chơi; cấp theo ngày, ngày chinh phục đảo, đảo ngoài tầm.
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;
using PokiClash.Game;
using Progress = PokiClash.Core.Progress;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public sealed class BalanceWindow : EditorWindow
    {
        static readonly string[] Tabs = { "Trận", "Máy bi", "Tiến độ", "Huy hiệu" };
        static string DataDir => Path.Combine(Application.dataPath, "02 Data");
        static string LogDir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Logs/CanBang"));

        int tab;
        Vector2 scroll;
        GameData d;

        [MenuItem("PokiClash/Cân bằng", priority = 20)]
        static void Open() => GetWindow<BalanceWindow>("Cân bằng").minSize = new Vector2(760, 480);

        // chạy nhanh không mở cửa sổ (cùng mã với các tab)
        [MenuItem("PokiClash/Cân bằng nhanh/Tiến độ 30 ngày, 3 kiểu người chơi (ghi Console)", priority = 21)]
        static void QuickProgress()
        {
            var w = CreateInstance<BalanceWindow>();
            try
            {
                w.d = Load();
                w.profiles = ProgressSim.DefaultProfiles();
                w.RunProgress();
                if (w.progress != null) Debug.Log("[Cân bằng] " + w.progressInfo + "\n" + w.ProgressText());
            }
            finally
            {
                DestroyImmediate(w);
            }
        }

        // quét nhịp: 3 kiểu người chơi × 30 ngày với các tổ hợp EXP lên cấp, bi thụ động (cây, trang trại), lượt Hái ×2
        [MenuItem("PokiClash/Cân bằng nhanh/Quét nhịp: EXP lên cấp, cây bi, trang trại (ghi Console)", priority = 26)]
        static void QuickPace()
        {
            void Passive(BalanceConfig c, double k)
            {
                c.trees.perHour *= k;
                c.trees.cap *= k;
                c.farm.@base *= k;
            }
            void TreeDouble(BalanceConfig c, int n) => c.ads.limits.Find(x => x.p == AdGate.TreeDouble).n = n;
            var variants = new (string name, Action<BalanceConfig> set)[]
            {
                ("gốc", c => { }),
                ("EXP ×2", c => c.expBase *= 2),
                ("bi thụ động ×0,5", c => Passive(c, 0.5)),
                ("EXP ×2, bi thụ động ×0,5", c => { c.expBase *= 2; Passive(c, 0.5); }),
                ("EXP ×2, bi thụ động ×0,5, Hái ×2 1 lần/ngày", c => { c.expBase *= 2; Passive(c, 0.5); TreeDouble(c, 1); }),
                ("EXP ×3, bi thụ động ×0,5, Hái ×2 1 lần/ngày", c => { c.expBase *= 3; Passive(c, 0.5); TreeDouble(c, 1); }),
                ("EXP ×2, bi thụ động ×0,35, Hái ×2 1 lần/ngày", c => { c.expBase *= 2; Passive(c, 0.35); TreeDouble(c, 1); }),
            };
            var cache = new Dictionary<string, double>();
            var sb = new StringBuilder();
            var t0 = DateTime.Now;
            try
            {
                for (int i = 0; i < variants.Length; i++)
                {
                    var d = Load();
                    variants[i].set(d.Cfg);
                    sb.Append($"{variants[i].name} (cần {Enumerable.Range(1, d.Cfg.maxLevel - 1).Sum(l => Progress.ExpToNext(l, d.Cfg))} EXP tới cấp {d.Cfg.maxLevel}):\n");
                    foreach (var p in ProgressSim.DefaultProfiles())
                    {
                        if (EditorUtility.DisplayCancelableProgressBar("Quét nhịp", $"{variants[i].name}: {p.name}", i / (float)variants.Length))
                            throw new OperationCanceledException();
                        var r = ProgressSim.Run(d, p, 30, 1, 8, cache);
                        string Day(Elem z) => r.zoneDay[(int)z] < 0 ? "chưa" : "ngày " + r.zoneDay[(int)z];
                        sb.Append($"  {p.name}: Thủy {Day(Elem.Thuy)}, Hỏa {Day(Elem.Hoa)}, Kim {Day(Elem.Kim)}, Mộc {Day(Elem.Moc)}, Thổ {Day(Elem.Tho)}; " +
                                  $"cấp ngày 3/7/14/21/30 = {r.level[3]}/{r.level[7]}/{r.level[14]}/{r.level[21]}/{r.level[30]}; bi ải {r.ballsFromStages}, cây {r.ballsFromTrees}, trang trại {r.ballsFromFarm}, đã thả {r.ballsDropped}; tiến hóa {r.evolves}\n");
                    }
                }
                Debug.Log($"[Cân bằng] Quét nhịp trong {(DateTime.Now - t0).TotalSeconds:0} giây\n" + sb);
            }
            catch (OperationCanceledException)
            {
                Debug.Log("[Cân bằng] Quét nhịp: đã dừng.\n" + sb);
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }

        [MenuItem("PokiClash/Cân bằng nhanh/Bảng 40 ải, 50 trận mỗi ô (ghi CSV vào Logs, CanBang)", priority = 22)]
        static void QuickTable()
        {
            var w = CreateInstance<BalanceWindow>();
            try
            {
                w.d = Load();
                w.scope = 2;
                w.RunBattles(w.d.Zones.OrderBy(z => z.order).ToList());
                if (w.rows == null) return;
                Directory.CreateDirectory(LogDir);
                var path = Path.Combine(LogDir, "bang_40_ai.csv");
                File.WriteAllText(path, w.BattleCsv(), new UTF8Encoding(true));
                Debug.Log($"[Cân bằng] {w.runInfo} Ghi {path}");
            }
            finally
            {
                DestroyImmediate(w);
            }
        }

        static GameData Load()
        {
            string R(string f) => File.ReadAllText(Path.Combine(DataDir, "Json", f));
            return GameData.FromJson(R("heroes.json"), R("cards.json"), R("zones.json"), R("stages.json"), R("balance.json"));
        }

        void OnGUI()
        {
            d = d ?? Load();
            using (new EditorGUILayout.HorizontalScope())
            {
                tab = GUILayout.Toolbar(tab, Tabs, GUILayout.Height(26));
                if (GUILayout.Button("Nạp lại dữ liệu", GUILayout.Width(120), GUILayout.Height(26))) d = Load();
            }
            EditorGUILayout.Space(4);
            scroll = EditorGUILayout.BeginScrollView(scroll);
            if (tab == 0) BattleTab();
            else if (tab == 1) MachineTab();
            else if (tab == 2) ProgressTab();
            else BadgeTab();
            EditorGUILayout.EndScrollView();
        }

        static string Pct(double p) => Math.Floor(p * 100 + 0.5).ToString(CultureInfo.InvariantCulture) + "%"; // làm tròn .5 lên như Math.round của JS

        static Color CellColor(double win) => win >= 0.7 ? new Color(0.55f, 0.85f, 0.5f) : win >= 0.3 ? new Color(0.95f, 0.85f, 0.45f) : new Color(0.95f, 0.55f, 0.5f);

        static string SaveCsv(string name, string csv)
        {
            Directory.CreateDirectory(LogDir);
            var path = EditorUtility.SaveFilePanel("Xuất CSV", LogDir, name, "csv");
            if (string.IsNullOrEmpty(path)) return null;
            File.WriteAllText(path, csv, new UTF8Encoding(true)); // có BOM để Excel đọc đúng tiếng Việt
            Debug.Log("[Cân bằng] Đã ghi " + path);
            return path;
        }

        // ---------- Trận ----------

        sealed class BattleRow
        {
            public ZoneDef zone;
            public StageDef stage;
            public int[] levels;
            public SimCell[] cells;
            public string team;
            public int star, card;
        }

        int scope = 1, stageIdx, zoneIdx, star = 1, card = 1, n = 50;
        bool suggested = true, autoLevels = true;
        readonly int[] heroIdx = { 0, 1, 2 };
        string levelsText = "1, 4, 7, 9";
        float hpB, atkB, defB;
        int badgeAll; // huy hiệu bậc này cho mọi tướng trong đội
        int potPreset; // tiềm năng mẫu cho mọi tướng: 0 không, 1 trung bình, 2 trần
        List<BattleRow> rows;
        string runInfo;

        void BattleTab()
        {
            var stages = d.Stages;
            var zones = d.Zones.OrderBy(z => z.order).ToList();
            scope = EditorGUILayout.Popup("Phạm vi", scope, new[] { "Một ải", "Một đảo", "Cả 40 ải" });
            if (scope == 0) stageIdx = EditorGUILayout.Popup("Ải", stageIdx, stages.Select(st => $"{d.Zone(st.zone).name} {st.idx}: {st.name}").ToArray());
            if (scope == 1) zoneIdx = EditorGUILayout.Popup("Đảo", zoneIdx, zones.Select(z => $"{z.name} (cấp {z.levelMin}–{z.levelMax})").ToArray());

            suggested = EditorGUILayout.ToggleLeft("Đội gợi ý theo đảo (sao, cấp thẻ theo độ sâu của đảo, như npm run sim -- battle)", suggested);
            if (!suggested)
            {
                var names = d.Heroes.Select(h => h.name).ToArray();
                using (new EditorGUILayout.HorizontalScope())
                {
                    EditorGUILayout.PrefixLabel("Đội");
                    for (int i = 0; i < 3; i++) heroIdx[i] = EditorGUILayout.Popup(heroIdx[i], names);
                }
                star = EditorGUILayout.IntSlider("Sao", star, 1, d.Cfg.maxStar);
                card = EditorGUILayout.IntSlider("Cấp thẻ (cả 3 thẻ)", card, 1, d.Cfg.cardMax);
            }
            autoLevels = EditorGUILayout.ToggleLeft("5 mức cấp quanh khoảng đề nghị của đảo (cận dưới − 2 … cận trên + 2)", autoLevels);
            if (!autoLevels) levelsText = EditorGUILayout.TextField("Các cấp (cách nhau dấu phẩy)", levelsText);
            using (new EditorGUILayout.HorizontalScope())
            {
                EditorGUILayout.PrefixLabel("Phần cộng side meta (%)");
                EditorGUIUtility.labelWidth = 40;
                hpB = EditorGUILayout.FloatField("Máu", hpB);
                atkB = EditorGUILayout.FloatField("Công", atkB);
                defB = EditorGUILayout.FloatField("Thủ", defB);
                EditorGUIUtility.labelWidth = 0;
            }
            badgeAll = EditorGUILayout.IntSlider("Huy hiệu mọi hệ (bậc, 0 = không)", badgeAll, 0, Badges.MaxTier(d.Cfg));
            potPreset = EditorGUILayout.Popup("Tiềm năng mọi tướng", potPreset, new[] { "Không", "Trung bình (kỳ vọng 4 dòng)", "Trần (Công ×3 chặn 40%, Máu 16%)" });
            n = EditorGUILayout.IntField("Số trận mỗi ô", Math.Max(1, n));

            using (new EditorGUILayout.HorizontalScope())
            {
                if (GUILayout.Button("Chạy", GUILayout.Height(28))) RunBattles(zones);
                GUI.enabled = rows != null && rows.Count > 0;
                if (GUILayout.Button("Xuất CSV", GUILayout.Width(120), GUILayout.Height(28))) SaveCsv("tran_" + DateTime.Now.ToString("yyyyMMdd_HHmm"), BattleCsv());
                GUI.enabled = true;
            }
            if (runInfo != null) EditorGUILayout.HelpBox(runInfo, MessageType.Info);
            if (rows == null) return;

            foreach (var g in rows.GroupBy(r => r.zone))
            {
                var first = g.First();
                EditorGUILayout.Space(6);
                EditorGUILayout.LabelField($"{g.Key.name} (đề nghị cấp {g.Key.levelMin}–{g.Key.levelMax}) · đội {first.team}, sao {first.star}, thẻ cấp {first.card}", EditorStyles.boldLabel);
                using (new EditorGUILayout.HorizontalScope())
                {
                    GUILayout.Label("ải", GUILayout.Width(220));
                    foreach (var lv in first.levels) GUILayout.Label("cấp " + lv, EditorStyles.miniBoldLabel, GUILayout.Width(90));
                }
                foreach (var r in g)
                    using (new EditorGUILayout.HorizontalScope())
                    {
                        GUILayout.Label($"{r.stage.idx} {r.stage.name}" + (r.stage.kind != StageKind.Normal ? " ◆" : ""), GUILayout.Width(220));
                        foreach (var c in r.cells)
                        {
                            var old = GUI.backgroundColor;
                            GUI.backgroundColor = CellColor(c.WinRate);
                            GUILayout.Box($"{Pct(c.WinRate)} {c.AvgRounds:0.0}h", GUILayout.Width(90));
                            GUI.backgroundColor = old;
                        }
                    }
            }
        }

        void RunBattles(List<ZoneDef> zones)
        {
            var targets = scope == 0 ? new List<StageDef> { d.Stages[stageIdx] }
                : scope == 1 ? d.ZoneStages(zones[zoneIdx].id).ToList()
                : zones.SelectMany(z => d.ZoneStages(z.id)).ToList();
            int[] manual = null;
            if (!autoLevels)
            {
                manual = levelsText.Split(',').Select(x => int.TryParse(x.Trim(), out var v) ? v : 0).Where(v => v > 0).ToArray();
                if (manual.Length == 0) manual = new[] { 1 };
            }
            // phần cộng side meta: % nhập tay cộng thêm phần huy hiệu (bậc chọn cho mọi tướng)
            double bb = Badges.Bonus(d.Cfg, badgeAll);
            var (pt, _) = Sim.PotentialPreset(d.Cfg, potPreset);
            var bonus = new StatMods
            {
                hpPct = hpB / 100.0 + bb + pt[(int)PotKind.Hp], atkPct = atkB / 100.0 + bb + pt[(int)PotKind.Atk],
                defPct = defB / 100.0 + bb + pt[(int)PotKind.Def], spd = pt[(int)PotKind.Spd],
            };
            var start = potPreset > 0 ? new BattleStart { mana = pt[(int)PotKind.Mana], rage = pt[(int)PotKind.Rage], crit = pt[(int)PotKind.Crit], lifesteal = pt[(int)PotKind.Lifesteal] } : null;
            rows = new List<BattleRow>();
            var t0 = DateTime.Now;
            int total = targets.Count, done = 0, battles = 0;
            try
            {
                foreach (var st in targets)
                {
                    var z = d.Zone(st.zone);
                    var levels = manual ?? Sim.Levels(z);
                    List<string> team;
                    int sStar = star, sCard = card;
                    if (suggested)
                    {
                        var tm = d.Cfg.SimTeamOf(z.id);
                        team = tm.team;
                        sStar = tm.star;
                        sCard = tm.card;
                    }
                    else team = heroIdx.Select(i => d.Heroes[i].id).Distinct().ToList();
                    var row = new BattleRow
                    {
                        zone = z, stage = st, levels = levels, cells = new SimCell[levels.Length], star = sStar, card = sCard,
                        team = string.Join(", ", team.Select(h => d.Hero(h).name)),
                    };
                    for (int i = 0; i < levels.Length; i++)
                    {
                        if (EditorUtility.DisplayCancelableProgressBar("Cân bằng", $"{z.name} ải {st.idx}, cấp {levels[i]}", (float)done / total)) throw new OperationCanceledException();
                        var s = Sim.Setup(d, team, levels[i], sStar, sCard);
                        row.cells[i] = Sim.Stage(d, s, st, n, 1000, null, bonus, start);
                        battles += n;
                    }
                    rows.Add(row);
                    done++;
                }
                runInfo = $"{battles} trận trong {(DateTime.Now - t0).TotalSeconds:0.0} giây.";
            }
            catch (OperationCanceledException)
            {
                runInfo = "Đã dừng giữa chừng.";
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }

        string BattleCsv()
        {
            var sb = new StringBuilder("dao,ai,ten,doi,sao,cap_the,cap,so_tran,thang,ti_le_thang,hiep_tb\n");
            foreach (var r in rows)
                for (int i = 0; i < r.levels.Length; i++)
                {
                    var c = r.cells[i];
                    sb.Append(string.Join(",", Keys.Of(r.zone.id), r.stage.idx, Q(r.stage.name), Q(r.team), r.star, r.card, r.levels[i], c.n, c.win,
                        c.WinRate.ToString("0.###", CultureInfo.InvariantCulture), c.AvgRounds.ToString("0.##", CultureInfo.InvariantCulture))).Append('\n');
                }
            return sb.ToString();
        }

        static string Q(string s) => "\"" + s.Replace("\"", "\"\"") + "\"";

        // ---------- Máy bi ----------

        double[] widths;
        int balls = 6000, opens = 20000;
        PachinkoReport report;
        bool reportDefault;

        void MachineTab()
        {
            widths = widths ?? (double[])Board.SlotW.Clone();
            EditorGUILayout.LabelField($"Độ rộng {Board.SlotLayout.Length} ô đáy (trái sang phải): " + string.Join(", ", Board.SlotLayout.Select(Pachinko.Key)), EditorStyles.miniLabel);
            using (new EditorGUILayout.HorizontalScope())
                for (int i = 0; i < widths.Length; i++) widths[i] = EditorGUILayout.DoubleField(widths[i], GUILayout.Width(48));
            double sum = widths.Sum(), need = Board.Right - Board.Left;
            if (Math.Abs(sum - need) > 1e-6) EditorGUILayout.HelpBox($"Tổng độ rộng {sum} khác bề ngang máy {need}: ô cuối sẽ hẹp/rộng lệch.", MessageType.Warning);
            balls = EditorGUILayout.IntField("Số bi", Math.Max(100, balls));
            opens = EditorGUILayout.IntField("Lần mở thử mỗi loại rương", Math.Max(100, opens));
            bool isDefault = widths.SequenceEqual(Board.SlotW);
            using (new EditorGUILayout.HorizontalScope())
            {
                if (GUILayout.Button("Chạy mô phỏng", GUILayout.Height(28)))
                {
                    EditorUtility.DisplayProgressBar("Cân bằng", "Thả bi…", 0.3f);
                    try
                    {
                        report = Sim.Machine(d, isDefault ? null : (double[])widths.Clone(), balls, opens);
                        reportDefault = isDefault;
                    }
                    finally
                    {
                        EditorUtility.ClearProgressBar();
                    }
                }
                if (GUILayout.Button("Về độ rộng gốc", GUILayout.Width(130), GUILayout.Height(28))) widths = (double[])Board.SlotW.Clone();
            }
            if (report == null) return;

            EditorGUILayout.Space(6);
            EditorGUILayout.LabelField($"{report.balls} bi, {report.frames / 60.0:0} giây máy", EditorStyles.boldLabel);
            foreach (SlotKind k in Enum.GetValues(typeof(SlotKind)))
            {
                string ingame = Pct(d.Cfg.Rate(Pachinko.Key(k)));
                EditorGUILayout.LabelField($"  {Pachinko.Key(k),-14} {report.Rate(k) * 100:0.00}%   (bảng tỉ lệ trong game: {ingame})");
            }
            EditorGUILayout.LabelField("Theo chỗ rơi", EditorStyles.miniBoldLabel);
            foreach (var kv in report.byPlace.OrderBy(x => x.Key))
                EditorGUILayout.LabelField($"  {kv.Key,-22} {kv.Value * 100.0 / report.balls:0.00}%");
            EditorGUILayout.LabelField("Giá trị trung bình mỗi rương (×1)", EditorStyles.miniBoldLabel);
            foreach (var kv in report.chestEv)
                EditorGUILayout.LabelField($"  {Pachinko.ChestName(kv.Key)}: {kv.Value.exp:0.0} EXP, {kv.Value.balls:0.00} bi, {kv.Value.cards:0.00} thẻ");
            EditorGUILayout.LabelField($"Mỗi bi ở ×1: {report.expPerBall:0.00} EXP, hoàn {report.backPerBall:0.000} bi, {report.cardsPerBall:0.000} thẻ", EditorStyles.boldLabel);
            EditorGUILayout.LabelField("Bi để lên cấp 2 / 5 / 10: " + string.Join(" / ", new[] { 1, 4, 9 }.Select(l => (Progress.ExpToNext(l, d.Cfg) / report.expPerBall).ToString("0.0"))));
            if (report.backPerBall > 0.5)
                EditorGUILayout.HelpBox($"Bi hoàn mỗi bi {report.backPerBall:0.000} > 0,5: máy gần như tự nuôi, cần giảm ô +1 bi hoặc bi trong rương.", MessageType.Error);

            EditorGUILayout.Space(4);
            GUI.enabled = reportDefault;
            if (GUILayout.Button("Ghi tỉ lệ này vào bảng tỉ lệ trong game (asset BalanceConfig)"))
                WriteRates();
            GUI.enabled = true;
            EditorGUILayout.HelpBox("Số gốc của bảng tỉ lệ do Web/scripts/export_data.ts đo và ghi vào balance.json; \"Nhập dữ liệu\" sẽ ghi đè. " +
                                    "Muốn đổi mặt máy lâu dài thì sửa ở web rồi xuất lại. Chỉ ghi được khi chạy với độ rộng gốc (mặt máy trong game).", MessageType.None);
        }

        void WriteRates()
        {
            var guid = AssetDatabase.FindAssets("t:BalanceConfigAsset").FirstOrDefault();
            if (guid == null)
            {
                Debug.LogError("[Cân bằng] Không thấy asset BalanceConfig");
                return;
            }
            var asset = AssetDatabase.LoadAssetAtPath<BalanceConfigAsset>(AssetDatabase.GUIDToAssetPath(guid));
            asset.cfg.ratesBalls = report.balls;
            asset.cfg.rates = report.count.Select(kv => new SlotRate { k = Pachinko.Key(kv.Key), p = Math.Round((double)kv.Value / report.balls, 4) }).ToList();
            EditorUtility.SetDirty(asset);
            AssetDatabase.SaveAssets();
            Debug.Log("[Cân bằng] Đã ghi tỉ lệ máy bi vào " + AssetDatabase.GetAssetPath(asset));
        }

        // ---------- Huy hiệu ----------

        int badgeN = 12;
        List<string> badgeLines;
        string badgeInfo;

        // tỉ lệ thắng từng bậc (trung bình các trận của bậc, và trận cuối) với đội mẫu của đảo cùng hệ, cấp người chơi = cấp địch trận 1 của bậc
        // + {−2, 0, +3}; rồi tỉ lệ thắng 8 ải ở cấp đề nghị thấp nhất khi mọi tướng có huy hiệu bậc 0 / 3 / 5 (như npm run sim -- badges)
        void BadgeTab()
        {
            badgeN = EditorGUILayout.IntSlider("Số trận mỗi trận thử thách", badgeN, 2, 60);
            if (GUILayout.Button("Chạy", GUILayout.Height(28))) RunBadges();
            if (badgeInfo != null) EditorGUILayout.HelpBox(badgeInfo, MessageType.Info);
            if (badgeLines == null) return;
            foreach (var l in badgeLines)
                EditorGUILayout.LabelField(l, l.StartsWith(" ") ? EditorStyles.label : EditorStyles.boldLabel);
        }

        void RunBadges()
        {
            var cfg = d.Cfg;
            var zones = d.Zones.OrderBy(z => z.order).ToList();
            badgeLines = new List<string>();
            var t0 = DateTime.Now;
            int battles = 0, step = 0, steps = zones.Count * (Badges.MaxTier(cfg) + 1);
            try
            {
                foreach (var z in zones)
                {
                    var tm = cfg.SimTeamOf(z.id);
                    badgeLines.Add($"Dãy {z.name} · đội {string.Join(", ", tm.team.Select(h => d.Hero(h).name))}, sao {tm.star}, thẻ {tm.card}");
                    for (int tier = 1; tier <= Badges.MaxTier(cfg); tier++)
                    {
                        if (EditorUtility.DisplayCancelableProgressBar("Cân bằng", $"{z.name} bậc {tier}", (float)step++ / steps)) throw new OperationCanceledException();
                        int baseLv = Badges.Stage(d, z.id, tier, 1).enemies[0].level;
                        var cells = new[] { -2, 0, 3 }.Select(dl =>
                        {
                            int lv = Math.Max(1, baseLv + dl);
                            var r = Sim.BadgeTier(d, Sim.Setup(d, tm.team, lv, tm.star, tm.card), z.id, tier, badgeN);
                            battles += r.total;
                            return $"cấp {lv}: {Pct((double)r.win / r.total)} (cuối {Pct((double)r.lastWin / badgeN)})".PadRight(30);
                        });
                        badgeLines.Add($"  {Badges.TierName(cfg, tier),-10}{string.Concat(cells)}");
                    }
                }
                badgeLines.Add("Ảnh hưởng lên đảo: tỉ lệ thắng trung bình 8 ải ở cấp đề nghị thấp nhất, mọi tướng có huy hiệu bậc 0 / 3 / 5");
                foreach (var z in zones)
                {
                    if (EditorUtility.DisplayCancelableProgressBar("Cân bằng", $"{z.name}: ảnh hưởng lên đảo", (float)step++ / steps)) throw new OperationCanceledException();
                    var tm = cfg.SimTeamOf(z.id);
                    var cells = new[] { 0, 3, 5 }.Select(tier =>
                    {
                        double bb = Badges.Bonus(cfg, tier);
                        var bonus = new StatMods { hpPct = bb, atkPct = bb, defPct = bb };
                        int win = 0, total = 0;
                        foreach (var st in d.ZoneStages(z.id))
                        {
                            var c = Sim.Stage(d, Sim.Setup(d, tm.team, z.levelMin, tm.star, tm.card), st, badgeN, 1000, null, bonus);
                            win += c.win;
                            total += c.n;
                        }
                        battles += total;
                        return $"bậc {tier} (+{bb * 100:0}%): {Pct((double)win / total)}".PadRight(24);
                    });
                    badgeLines.Add($"  {z.name,-10} cấp {z.levelMin}: {string.Concat(cells)}");
                }
                badgeInfo = $"{battles} trận trong {(DateTime.Now - t0).TotalSeconds:0.0} giây.";
            }
            catch (OperationCanceledException)
            {
                badgeInfo = "Đã dừng giữa chừng.";
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }

        // đảo Mộc và Thổ với tiềm năng không / trung bình / trần cho mọi tướng (đội mẫu, 5 mức cấp, 30 trận mỗi ô)
        [MenuItem("PokiClash/Cân bằng nhanh/Tiềm năng: đảo Mộc và Thổ (ghi Console)", priority = 24)]
        static void QuickPotential()
        {
            var d = Load();
            var lines = new List<string>();
            var t0 = DateTime.Now;
            try
            {
                foreach (var z in d.Zones.Where(z => z.id == Elem.Moc || z.id == Elem.Tho))
                {
                    var tm = d.Cfg.SimTeamOf(z.id);
                    var levels = Sim.Levels(z);
                    lines.Add($"{z.name} (đề nghị {z.levelMin}–{z.levelMax}), đội {string.Join(", ", tm.team)}, sao {tm.star}, thẻ {tm.card}: %thắng trung bình 8 ải theo cấp " + string.Join("/", levels));
                    for (int kind = 0; kind < 3; kind++)
                    {
                        if (EditorUtility.DisplayCancelableProgressBar("Cân bằng", $"{z.name}: tiềm năng {kind}", kind / 3f)) throw new OperationCanceledException();
                        var (pt, name) = Sim.PotentialPreset(d.Cfg, kind);
                        var bonus = new StatMods { hpPct = pt[(int)PotKind.Hp], atkPct = pt[(int)PotKind.Atk], defPct = pt[(int)PotKind.Def], spd = pt[(int)PotKind.Spd] };
                        var start = kind > 0 ? new BattleStart { mana = pt[(int)PotKind.Mana], rage = pt[(int)PotKind.Rage], crit = pt[(int)PotKind.Crit], lifesteal = pt[(int)PotKind.Lifesteal] } : null;
                        var cells = levels.Select(lv =>
                        {
                            int win = 0, total = 0;
                            foreach (var st in d.ZoneStages(z.id))
                            {
                                var c = Sim.Stage(d, Sim.Setup(d, tm.team, lv, tm.star, tm.card), st, 30, 1000, null, kind > 0 ? bonus : null, start);
                                win += c.win;
                                total += c.n;
                            }
                            return Pct((double)win / total);
                        });
                        lines.Add($"  tiềm năng {name,-11}: {string.Join("  ", cells)}");
                    }
                }
            }
            catch (OperationCanceledException)
            {
                lines.Add("Đã dừng giữa chừng.");
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
            Debug.Log($"[Cân bằng] Tiềm năng ({(DateTime.Now - t0).TotalSeconds:0.0} giây)\n" + string.Join("\n", lines));
        }

        // bi mỗi ngày từ trang trại theo số lần vào game (2, 4, 8 lần, rải 8 giờ – 23 giờ; mỗi lần: thu hoạch, rút tướng hết sức, tự xếp),
        // với 3 kho tướng mẫu; so với AFK ải (nhận mỗi lần vào, không quảng cáo) khi xong 1 / 3 / 5 đảo
        [MenuItem("PokiClash/Cân bằng nhanh/Trang trại: bi mỗi ngày so với AFK (ghi Console)", priority = 25)]
        static void QuickFarm()
        {
            var d = Load();
            const double H = 3600000;
            var rosters = new (string name, string[] heroes, int level, int star, int zonesDone)[]
            {
                ("4 tướng, cấp 9, 1 sao (đầu game)", new[] { "giot_suong", "vo_su", "nu_hoa", "ca_ngua" }, 9, 1, 1),
                ("8 tướng, cấp 18, 2 sao (giữa game)", d.Heroes.Take(8).Select(h => h.id).ToArray(), 18, 2, 3),
                ("11 tướng, cấp 28, 4 sao (cuối game)", d.Heroes.Select(h => h.id).ToArray(), 28, 4, 5),
            };
            var lines = new List<string>();
            foreach (var (name, heroes, level, star, zonesDone) in rosters)
            {
                var cells = new[] { 2, 4, 8 }.Select(visits =>
                {
                    var s = SaveData.New(d, 0);
                    foreach (var h in d.Heroes) s.Hero(h.id).owned = heroes.Contains(h.id);
                    foreach (var h in heroes) s.Hero(h).star = star;
                    s.level = level;
                    s.zones = new int[5];
                    for (int z = 0; z < zonesDone; z++) s.zones[(int)d.Zones[z].id] = Islands.Size(d.Zones[z].id); // xong đảo theo thứ tự
                    int farm = 0, tree = 0;
                    const int days = 7;
                    for (int day = 0; day < days; day++)
                        for (int k = 0; k < visits; k++)
                        {
                            double now = (day * 24 + 8 + 15.0 * (k + 0.5) / visits) * H;
                            farm += Farm.Harvest(s, d, now);
                            var f = Farm.Of(s, d.Cfg, now);
                            for (int i = 0; i < f.spots.Count; i++)
                                if (f.spots[i].hero != null && f.spots[i].energy <= 0) Farm.Remove(s, d, now, i);
                            Farm.Auto(s, d, now);
                            tree += Trees.Harvest(s, d.Cfg, now);
                        }
                    return $"vào {visits} lần: trang trại {farm / days} bi/ngày, cây bi {tree / days} bi/ngày";
                });
                lines.Add($"{name}, xong {zonesDone} đảo ({d.Zones.Take(zonesDone).Sum(z => Islands.Size(z.id))} ải): " + string.Join(" · ", cells));
            }
            Debug.Log("[Cân bằng] Trang trại\n" + string.Join("\n", lines));
        }

        [MenuItem("PokiClash/Cân bằng nhanh/Huy hiệu: tỉ lệ thắng từng bậc (ghi Console)", priority = 23)]
        static void QuickBadges()
        {
            var w = CreateInstance<BalanceWindow>();
            try
            {
                w.d = Load();
                w.RunBadges();
                if (w.badgeLines != null) Debug.Log("[Cân bằng] Huy hiệu: " + w.badgeInfo + "\n" + string.Join("\n", w.badgeLines));
            }
            finally
            {
                DestroyImmediate(w);
            }
        }

        // ---------- Tiến độ ----------

        PlayerProfile[] profiles;
        int days = 30, simN = 8;
        List<ProgressReport> progress;
        string progressInfo;

        void ProgressTab()
        {
            profiles = profiles ?? ProgressSim.DefaultProfiles();
            EditorGUILayout.LabelField("Kiểu người chơi (lần vào game mỗi ngày, trận mỗi lần, có xem quảng cáo, người giỏi hơn máy +%)", EditorStyles.miniLabel);
            foreach (var p in profiles)
                using (new EditorGUILayout.HorizontalScope())
                {
                    p.name = EditorGUILayout.TextField(p.name, GUILayout.Width(80));
                    EditorGUIUtility.labelWidth = 60;
                    p.sessions = Math.Max(1, EditorGUILayout.IntField("Lần/ngày", p.sessions));
                    p.battles = Math.Max(0, EditorGUILayout.IntField("Trận/lần", p.battles));
                    p.ads = EditorGUILayout.Toggle("Quảng cáo", p.ads);
                    p.skill = EditorGUILayout.Slider("Giỏi hơn", (float)p.skill, 0, 0.5f);
                    EditorGUIUtility.labelWidth = 0;
                }
            days = EditorGUILayout.IntSlider("Số ngày", days, 1, 90);
            simN = EditorGUILayout.IntSlider("Trận máy đo mỗi lần (ải, cấp, đội)", simN, 2, 40);
            using (new EditorGUILayout.HorizontalScope())
            {
                if (GUILayout.Button("Chạy mô phỏng", GUILayout.Height(28))) RunProgress();
                GUI.enabled = progress != null;
                if (GUILayout.Button("Xuất CSV", GUILayout.Width(120), GUILayout.Height(28))) SaveCsv("tien_do_" + DateTime.Now.ToString("yyyyMMdd_HHmm"), ProgressCsv());
                GUI.enabled = true;
                if (GUILayout.Button("Kiểu mặc định", GUILayout.Width(120), GUILayout.Height(28))) profiles = ProgressSim.DefaultProfiles();
            }
            if (progressInfo != null) EditorGUILayout.HelpBox(progressInfo, MessageType.Info);
            if (progress == null) return;

            var zones = d.Zones.OrderBy(z => z.order).ToList();
            foreach (var r in progress)
            {
                EditorGUILayout.Space(6);
                EditorGUILayout.LabelField($"{r.profile.name}: {r.profile.sessions} lần × {r.profile.battles} trận mỗi ngày{(r.profile.ads ? ", xem quảng cáo" : "")}, giỏi hơn máy +{r.profile.skill * 100:0}%", EditorStyles.boldLabel);
                var sb = new StringBuilder("Cấp theo ngày: ");
                for (int i = 1; i <= r.days; i++) sb.Append(i).Append(':').Append(r.level[i]).Append(i < r.days ? "  " : "");
                EditorGUILayout.LabelField(sb.ToString(), EditorStyles.wordWrappedMiniLabel);
                foreach (var z in zones)
                {
                    int zi = (int)z.id;
                    string conquer = r.zoneDay[zi] >= 0 ? $"chinh phục ngày {r.zoneDay[zi]}" : $"NGOÀI TẦM {r.days} NGÀY";
                    string lvDay = r.zoneLevelDay[zi] >= 0 ? $"đạt cấp boss {z.levelMax} ngày {r.zoneLevelDay[zi]}" : $"chưa tới cấp boss {z.levelMax} (cuối kỳ cấp {r.level[r.days]})";
                    var style = r.zoneDay[zi] >= 0 ? EditorStyles.label : EditorStyles.boldLabel;
                    var old = GUI.contentColor;
                    if (r.zoneDay[zi] < 0) GUI.contentColor = new Color(1f, 0.45f, 0.4f);
                    EditorGUILayout.LabelField($"  {z.name} (đề nghị {z.levelMin}–{z.levelMax}): {conquer}; {lvDay}", style);
                    GUI.contentColor = old;
                }
                EditorGUILayout.LabelField($"  {r.battles} trận, thắng {r.wins} ({(r.battles > 0 ? Pct((double)r.wins / r.battles) : "-")}), đánh lại {r.replays}; " +
                                           $"bi từ ải {r.ballsFromStages}, từ cây bi {r.ballsFromTrees}, từ trang trại {r.ballsFromFarm}; đã thả {r.ballsDropped}; rương AFK {r.afkChests}; nâng thẻ {r.cardUps}, tiến hóa {r.evolves}",
                    EditorStyles.wordWrappedMiniLabel);
            }
        }

        void RunProgress()
        {
            var cache = new Dictionary<string, double>();
            progress = new List<ProgressReport>();
            var t0 = DateTime.Now;
            try
            {
                for (int i = 0; i < profiles.Length; i++)
                {
                    var p = profiles[i];
                    int idx = i;
                    progress.Add(ProgressSim.Run(d, p.Copy(), days, 1, simN, cache, day =>
                    {
                        if (EditorUtility.DisplayCancelableProgressBar("Cân bằng", $"{p.name}: ngày {day}/{days}", (idx + (float)day / days) / profiles.Length))
                            throw new OperationCanceledException();
                    }));
                }
                progressInfo = $"{profiles.Length} kiểu × {days} ngày trong {(DateTime.Now - t0).TotalSeconds:0.0} giây ({cache.Count} ô tỉ lệ thắng, {cache.Count * simN} trận máy).";
            }
            catch (OperationCanceledException)
            {
                progressInfo = "Đã dừng giữa chừng.";
                progress = null;
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
        }

        string ProgressText()
        {
            var sb = new StringBuilder();
            foreach (var r in progress)
            {
                sb.Append($"{r.profile.name} ({r.profile.sessions} lần × {r.profile.battles} trận/ngày{(r.profile.ads ? ", quảng cáo" : "")}): cấp ngày 1/3/7/14/30 = ");
                sb.Append(string.Join("/", new[] { 1, 3, 7, 14, 30 }.Where(i => i <= r.days).Select(i => r.level[i]))).Append("; ");
                foreach (var z in d.Zones.OrderBy(z => z.order))
                {
                    int zi = (int)z.id;
                    sb.Append(z.name).Append(' ').Append(r.zoneDay[zi] >= 0 ? "ngày " + r.zoneDay[zi] : "ngoài tầm").Append(", ");
                }
                sb.Append($"{r.battles} trận thắng {r.wins}, đánh lại {r.replays}; bi ải {r.ballsFromStages}, cây bi {r.ballsFromTrees}, trang trại {r.ballsFromFarm}, đã thả {r.ballsDropped}; rương AFK {r.afkChests}; nâng thẻ {r.cardUps}, tiến hóa {r.evolves}\n");
            }
            return sb.ToString();
        }

        string ProgressCsv()
        {
            var sb = new StringBuilder("kieu,ngay,cap,ai_da_qua\n");
            foreach (var r in progress)
                for (int i = 0; i <= r.days; i++) sb.Append(Q(r.profile.name)).Append(',').Append(i).Append(',').Append(r.level[i]).Append(',').Append(r.cleared[i]).Append('\n');
            return sb.ToString();
        }
    }
}
