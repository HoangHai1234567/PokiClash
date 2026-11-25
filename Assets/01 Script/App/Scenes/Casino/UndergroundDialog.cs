// Hộp Hầm đấu (Đấu trường ngầm, GD_Claude/29_DaoCasino.md mục 6.5, mốc C4): các bậc hôm nay (bậc Nhà Vô Địch chỉ chủ nhật), mỗi dòng:
// "Bậc · tên đội" (thêm "đã thắng hôm nay"), luật ngày, đội địch (tên, cấp, sao), thưởng thắng lần đầu, nút Đánh (lệ phí) hoặc
// điều kiện mở. Nút "Đổi đội" mở hộp chọn đội dùng chung (Dialogs/ChonDoi). Đánh: trả lệ phí, sang trận (BattleArgs.ug).
// Prefab Dialogs/HamDau (menu "PokiClash/Prefab/Đảo Casino/Hầm đấu: dựng hộp"), các dòng dựng sẵn theo số bậc.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class UndergroundDialog : Dialog
    {
        [Serializable]
        public struct Row
        {
            public GameObject root;
            public TextMeshProUGUI head, rule, foes, reward;
            public SketchButton fight;
        }

        [SerializeField] TextMeshProUGUI title, sub;
        [SerializeField] Row[] rows;
        [SerializeField] SketchButton team;
        [SerializeField] TeamPickerDialog pickerPrefab;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, TextMeshProUGUI subText, Row[] rowList, SketchButton teamBtn, TeamPickerDialog picker)
        {
            title = titleText;
            sub = subText;
            rows = rowList;
            team = teamBtn;
            pickerPrefab = picker;
        }

        public void Show() => Render();

        void Render()
        {
            var s = S;
            var d = D;
            double now = Now;
            var cfg = d.Cfg.casino.underground;
            var today = Underground.TiersToday(d, now);
            title.text = Loc.T("Hầm đấu");
            var names = s.team.Select(h => d.Hero(h)?.name).Where(n => n != null);
            sub.text = Loc.F("Đội của bạn: {0}", string.Join(", ", names)) + "\n" +
                       Loc.T("Đội ngầm đổi lúc 0 giờ. Thắng lần đầu trong ngày có thưởng lớn; thua mất lệ phí.");
            for (int i = 0; i < rows.Length; i++)
            {
                var row = rows[i];
                bool shown = i < cfg.tiers.Count && today.Contains(i);
                row.root.SetActive(shown);
                if (!shown) continue;
                var t = cfg.tiers[i];
                var e = Underground.Entry(d, i, now);
                if (e == null)
                {
                    row.root.SetActive(false);
                    continue;
                }
                bool won = Underground.WonToday(s, d, i, now);
                bool open = Underground.TierOpen(s, d, i);
                int fee = Underground.Fee(s, d, i);
                row.head.text = $"{t.Name} · {e.Name}" + (won ? " · " + Loc.T("đã thắng hôm nay") : "");
                row.head.color = t.weekly ? Theme.RedD : Theme.Ink;
                row.rule.text = Underground.RuleText(e.rule);
                var foes = Underground.TeamLimit(e) == 1 ? e.team.Take(1) : e.team;
                row.foes.text = string.Join(", ", foes.Select(m => Loc.F("{0} cấp {1}, {2} sao", d.Hero(m.hero)?.name ?? m.hero, m.level, m.star)));
                var lead = d.Hero(Underground.Lead(e));
                string reward = Loc.F("Thắng lần đầu: {0} bi + {1} mảnh {2}", Mathf.RoundToInt((float)(fee * cfg.winMult)), t.shards, lead?.name ?? "");
                if (t.items.Count > 0) reward += " + " + string.Join(" + ", t.items.Select(ItemText));
                row.reward.text = reward;
                var b = row.fight;
                if (!open)
                {
                    b.SetText(Loc.F("Cấp {0}", t.level));
                    b.SetRole(BtnColor.Paper);
                    b.Locked = true;
                    b.SetOnClick(() => App.Toasts.Show(Loc.F("Mở ở cấp {0}", t.level), Icon("lock")));
                }
                else if (won && t.weekly)
                {
                    b.SetText(Loc.T("Đã thắng"));
                    b.SetRole(BtnColor.Paper);
                    b.Locked = true;
                    b.SetOnClick(null);
                }
                else
                {
                    b.Locked = false;
                    b.SetText(won ? Loc.F("Đánh lại · {0}", fee) : Loc.F("Đánh · {0} bi", fee));
                    b.SetRole(won ? BtnColor.Paper : BtnColor.Green);
                    int tier = i;
                    b.SetOnClick(() => Fight(tier, e));
                }
            }
            team.SetText(Loc.T("Đổi đội"));
            team.SetOnClick(PickTeam);
        }

        static string ItemText(CasinoItem it)
        {
            switch (it.k)
            {
                case "evo": return Loc.F("{0} đá tiến hóa", it.n);
                case "stones": return Loc.F("{0} đá tiềm năng", it.n);
                case "crystal": return Loc.F("{0} đá tinh", it.n);
                case "balls": return Loc.F("{0} bi", it.n);
                default: return it.n + " " + it.k;
            }
        }

        void Fight(int tier, UgEntry e)
        {
            var s = S;
            var d = D;
            if (s.team.Count == 0)
            {
                PickTeam();
                return;
            }
            if (!Underground.Pay(s, d, tier, Now, out var why))
            {
                App.Toasts.Show(why, Icon("lock"));
                return;
            }
            App.Save.Save();
            var list = s.team.Take(Math.Min(Progress.TeamSlots(s), Underground.TeamLimit(e))).ToList();
            Close();
            App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = 90000 + tier, team = list, ug = new UgRef { tier = tier, day = Casino.Today(Now) } });
        }

        void PickTeam()
        {
            if (!pickerPrefab) return;
            var s = S;
            var d = D;
            var e = Underground.Entry(d, 0, Now);
            var dlg = App.Modals.Open(pickerPrefab);
            dlg.Show(new List<string>(s.team), Progress.TeamSlots(s), e != null ? d.Hero(Underground.Lead(e)) : null, list =>
            {
                if (list != null && list.Count > 0)
                {
                    s.team = list;
                    App.Save.Save();
                }
                Render();
            });
        }
    }
}
