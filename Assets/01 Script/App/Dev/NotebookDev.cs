#if UNITY_EDITOR || DEVELOPMENT_BUILD
// Sổ tay bản dev (chỉ Editor và bản Development; bước kiểm tra trước build chặn nếu lọt vào bản phát hành):
// - Bảng thử: tua nhanh tới phần cần xem;
// - Chỉnh số: sửa các hệ số chính của BalanceConfig lúc chơi (nút − / +), có hiệu lực ở trận sau, "Về số gốc" nạp lại từ asset;
// - Máy tự chơi: 100 trận một ải với đội và cấp hiện tại (máy chơi cả hai bên), như bản web.
// Giao diện là phần "ban_dev" của prefab Screens/Notebook (NotebookDevPanel giữ tham chiếu); ở đây chỉ gán chữ và việc cho nút.
using System;
using System.Globalization;
using System.Linq;
using System.Reflection;
using PokiClash.Core;
using PokiClash.UI;

namespace PokiClash
{
    public static class NotebookDev
    {
        // khoá trong BalanceConfig, nhãn (như CFG_LABEL của web), bước của nút − / +. Prefab nướng một ô cho mỗi khoá có trong BalanceConfig.
        public static readonly (string key, string label, double step)[] Tunables =
        {
            ("picks", "Số lần chọn mỗi lượt", 1), ("manaPerTurn", "Mana mỗi lượt", 5), ("benchMana", "Mana tướng dự bị", 5),
            ("rageOnAttack", "Nộ khi đánh trúng", 5), ("rageOnHit", "Nộ khi bị đánh (× phần máu mất)", 10),
            ("critBase", "Tỉ lệ chí mạng gốc", 0.01), ("critMult", "Hệ số chí mạng", 0.1), ("defK", "Hằng số thủ", 10),
            ("hpBase", "Máu gốc", 50), ("atkBase", "Công gốc", 10), ("defBase", "Thủ gốc", 5),
            ("lvStep", "Tăng mỗi cấp", 0.01), ("starStep", "Tăng mỗi sao", 0.01), ("cardLvStep", "Tăng mỗi cấp thẻ", 0.01),
            ("bossHp", "Máu boss ×", 0.1), ("bossAtk", "Công boss ×", 0.05),
        };

        // Bảng thử: chữ nút (prefab nướng theo đúng thứ tự này) và việc làm
        public static readonly (string label, Action<SaveData, GameData> fn)[] Tools =
        {
            ("+50 bi", (s, d) => s.balls += 50),
            ("+500 XP", (s, d) =>
            {
                int before = s.level;
                Progress.AddExp(s, 500, d.Cfg);
                if (s.level > before) Dialogs.LevelUp(before, s.level);
            }),
            ("Mở hết tướng", (s, d) =>
            {
                foreach (var h in d.Heroes) s.Hero(h.id).owned = true;
            }),
            ("Mở hết ải", (s, d) =>
            {
                for (int i = 0; i < s.zones.Length; i++) s.zones[i] = 8;
            }),
            ("+5 bản sao", (s, d) =>
            {
                foreach (var h in d.Heroes)
                foreach (var k in Progress.Slots)
                    s.Hero(h.id).Card(k).copies += 5;
            }),
            ("Tua AFK, cây 1 giờ", (s, d) =>
            {
                Afk.Travel(s, 3600000);
                Trees.Travel(s, 3600000);
            }),
            ("Tua AFK, cây 8 giờ", (s, d) =>
            {
                Afk.Travel(s, 8 * 3600000);
                Trees.Travel(s, 8 * 3600000);
            }),
            ("Tua trang trại 2 giờ", (s, d) => Farm.Travel(s, 2 * 3600000)),
            ("+10 đá tiềm năng", (s, d) => s.potentialStones += 10),
            ("Đặt lại lượt QC", (s, d) => AdGate.Of(s).used.Clear()),
            ("Bỏ gói đã mua", (s, d) => s.ent = null),
        };

        static int botStage = -1;
        static string botResult = "";

        // rebuild: Sổ tay gán lại toàn bộ (sau khi bản lưu hoặc số đổi)
        public static void Bind(NotebookDevPanel panel, Action rebuild)
        {
            var p = panel.Refs;
            BindTools(p, rebuild);
            BindTuning(p, rebuild);
            BindBot(p);
        }

        // ---------- bảng thử ----------

        static void BindTools(NotebookDevPanel.Parts p, Action rebuild)
        {
            for (int i = 0; i < p.tools.Length && i < Tools.Length; i++)
            {
                var fn = Tools[i].fn;
                p.tools[i].SetOnClick(() =>
                {
                    fn(App.Save.Data, App.Data);
                    App.Save.Save();
                    App.Audio.Play("coin");
                    rebuild();
                });
            }
        }

        // ---------- chỉnh số ----------

        public static string Fmt(double v, double step) =>
            v.ToString(step >= 1 ? "0" : step >= 0.1 ? "0.0#" : "0.00#", CultureInfo.InvariantCulture).Replace('.', ',');

        static void BindTuning(NotebookDevPanel.Parts p, Action rebuild)
        {
            var baseCfg = App.I.balance.cfg;
            foreach (var cell in p.tune)
            {
                var c = cell;
                int at = Array.FindIndex(Tunables, x => x.key == c.key);
                var f = at < 0 ? null : typeof(BalanceConfig).GetField(c.key, BindingFlags.Public | BindingFlags.Instance);
                c.value.transform.parent.gameObject.SetActive(f != null);
                if (f == null) continue;
                double step = Tunables[at].step;
                double Get() => Convert.ToDouble(f.GetValue(App.Data.Cfg));
                double orig = Convert.ToDouble(f.GetValue(baseCfg));
                void Show()
                {
                    double v = Get();
                    c.value.text = Fmt(v, step);
                    c.value.color = Math.Abs(v - orig) > 1e-9 ? Theme.Red : Theme.Ink;
                }
                void Add(int dir)
                {
                    double v = Math.Max(f.FieldType == typeof(int) ? 1 : 0, Math.Round(Get() + dir * step, 4));
                    f.SetValue(App.Data.Cfg, f.FieldType == typeof(int) ? (object)(int)Math.Round(v) : v);
                    Show();
                }
                c.minus.SetOnClick(() => Add(-1));
                c.plus.SetOnClick(() => Add(1));
                Show();
            }
            p.tuneReset.SetOnClick(() =>
            {
                GameData.Current.Cfg = App.I.balance.cfg.Clone();
                rebuild();
            });
        }

        // ---------- máy tự chơi ----------

        public static string BotNote(string team, int level) =>
            $"Máy chơi cả hai bên 100 trận với đội hiện tại ({team}) ở cấp {level}. Người thật thường chơi tốt hơn máy.";

        public static string StageName(GameData d, StageDef st) => $"{d.Zone(st.zone).name} {st.idx}: {st.name}";

        static void BindBot(NotebookDevPanel.Parts p)
        {
            var s = App.Save.Data;
            var d = App.Data;
            var team = s.team.Where(h => s.Hero(h) != null && s.Hero(h).owned).ToList();
            p.botNote.text = BotNote(team.Count > 0 ? string.Join(", ", team.Select(h => d.Hero(h).name)) : "trống", s.level);
            if (botStage < 0)
            {
                var next = Progress.NextStage(s, d, Progress.RecommendedZone(s, d).id);
                botStage = Math.Max(0, d.Stages.IndexOf(next ?? d.Stages[0]));
            }
            void ShowStage() => p.botStage.text = StageName(d, d.Stages[botStage]);
            p.botPrev.SetOnClick(() =>
            {
                botStage = (botStage + d.Stages.Count - 1) % d.Stages.Count;
                ShowStage();
            });
            p.botNext.SetOnClick(() =>
            {
                botStage = (botStage + 1) % d.Stages.Count;
                ShowStage();
            });
            ShowStage();
            p.botResult.text = botResult;
            var outText = p.botResult;
            p.botRun.SetOnClick(() =>
            {
                if (team.Count == 0)
                {
                    App.Toasts.Show("Đội trống");
                    return;
                }
                var c = Sim.Stage(d, s, d.Stages[botStage], 100, (uint)(DateTime.Now.Ticks % 100000), team);
                botResult = $"Thắng {Math.Round(c.WinRate * 100)}% · trung bình {c.AvgRounds:0.0} hiệp".Replace('.', ',');
                outText.text = botResult;
            });
        }
    }
}
#endif
