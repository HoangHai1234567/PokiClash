// Kết trận Hang Tiềm Năng (BattleController gọi khi trận có CaveRef; 2026-11-17 tách khỏi BattleController để side meta tự sửa):
// thắng thì đá của lượt (còn lượt), thưởng lần đầu (đá, đá tinh, đá tiến hóa) và mở tầng sau; lượt đầu trong ngày ở tầng cao có đá tinh;
// thua không mất lượt. Nút: "Tầng sau »" (vừa mở), "Đánh tiếp" / "Đánh lại", "Về Hang".
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public static class CaveResult
    {
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        public static IEnumerator Run(Battle b, CaveRef cave, StageDef stage, List<string> team, BattleResultDialog resultPrefab)
        {
            var s = App.Save.Data;
            var d = App.Data;
            var cfg = d.Cfg;
            bool win = b.winner == 0;
            s.stats.battles++;
            CaveWin cw = null;
            if (win)
            {
                s.stats.wins++;
                cw = Potential.WinCave(s, cfg, cave.day, cave.tier);
            }
            App.Save.Save();
            App.Audio.Play(win ? "win" : "lose");
            var ct = cfg.cave.tiers[cave.tier];
            var m = App.Modals.Open(resultPrefab, mandatory: true);
            m.Show(win, $"Hang · Tầng {cave.tier + 1}: {ct.name} · {Elements.Name(cave.zone)}", 38,
                $"{b.round} hiệp · gây {b.dmgDealt[0]} sát thương");
            int left = Potential.CaveLeft(s, cfg, cave.day);
            if (cw != null)
            {
                if (cw.stones > 0) m.Reward().Item(Icon("rock"), $"×{cw.stones}", "Đá tiềm năng", Rarity.Epic);
                if (cw.firstStones > 0) m.Reward().Item(Icon("rock"), $"×{cw.firstStones}", "Đá tiềm năng", Rarity.Epic).Tag("Lần đầu", Theme.Yellow);
                if (cw.crystals > 0) PotentialPanel.CrystalTile(m.Reward(), cw.crystals).Tag(cw.first && ct.firstCrystals > 0 ? "Lần đầu" : "Hôm nay", Theme.Yellow);
                if (cw.evo > 0) m.Reward().EvoStones(cw.evo).Tag("Lần đầu", Theme.Yellow);
                string note = cw.stones > 0 ? "" : "Hết lượt hôm nay: không có đá của lượt. ";
                if (cw.first && cave.tier + 1 < cfg.cave.tiers.Count) note += $"Mở tầng {cave.tier + 2}: {cfg.cave.tiers[cave.tier + 1].name}. ";
                m.Tips(note + $"Còn {Mathf.Max(0, left)} lượt hôm nay · có {s.potentialStones} đá, {s.potentialCrystals} đá tinh");
            }
            else
                m.Tips($"Thua không mất lượt (còn {Mathf.Max(0, left)} lượt). Chọn tướng khắc hệ {Elements.Name(cave.zone)}, khai phá tiềm năng hoặc thử tầng dễ hơn.");
            int up = cave.tier + 1;
            if (cw != null && cw.first && up < cfg.cave.tiers.Count && Potential.CaveCanEnter(s, cfg, cave.day, up))
            {
                var nextRef = new CaveRef { zone = cave.zone, tier = up, day = cave.day };
                m.Button("Tầng sau »", BtnColor.Green, 230,
                    () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = Potential.CaveStage(d, cave.zone, up).id, team = team, cave = nextRef }));
            }
            if (Potential.CaveCanEnter(s, cfg, cave.day, cave.tier))
                m.Button(win ? "Đánh tiếp" : "Đánh lại", win ? BtnColor.Paper : BtnColor.Green, 220,
                    () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stage.id, team = team, cave = cave }));
            m.Button("Về Hang", BtnColor.Paper, 220, () => App.Router.Go(SceneIds.Cave));
            yield return new WaitForSecondsRealtime(0.12f);
            App.Audio.Play("stamp");
        }
    }
}
