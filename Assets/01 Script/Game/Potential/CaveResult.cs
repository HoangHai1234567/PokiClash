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
            Haptics.Play(win ? Haptic.Win : Haptic.Lose);
            var ct = cfg.cave.tiers[cave.tier];
            var m = App.Modals.Open(resultPrefab, mandatory: true);
            m.Show(win, Loc.F("Hang · Tầng {0}: {1} · {2}", cave.tier + 1, ct.Name, Elements.Name(cave.zone)), 38,
                Loc.F("{0} hiệp · gây {1} sát thương", b.round, b.dmgDealt[0]));
            int left = Potential.CaveLeft(s, cfg, cave.day);
            if (cw != null)
            {
                if (cw.stones > 0) m.Reward().Item(Icon("rock"), $"×{cw.stones}", Loc.T("Đá tiềm năng"), Rarity.Epic);
                if (cw.firstStones > 0) m.Reward().Item(Icon("rock"), $"×{cw.firstStones}", Loc.T("Đá tiềm năng"), Rarity.Epic).Tag(Loc.T("Lần đầu"), Theme.Yellow);
                if (cw.crystals > 0) PotentialPanel.CrystalTile(m.Reward(), cw.crystals).Tag(cw.first && ct.firstCrystals > 0 ? Loc.T("Lần đầu") : Loc.T("Hôm nay"), Theme.Yellow);
                if (cw.evo > 0) m.Reward().EvoStones(cw.evo).Tag(Loc.T("Lần đầu"), Theme.Yellow);
                string note = cw.stones > 0 ? "" : Loc.T("Hết lượt hôm nay: không có đá của lượt. ");
                if (cw.first && cave.tier + 1 < cfg.cave.tiers.Count) note += Loc.F("Mở tầng {0}: {1}. ", cave.tier + 2, cfg.cave.tiers[cave.tier + 1].Name);
                m.Tips(note + Loc.F("Còn {0} lượt hôm nay · có {1} đá, {2} đá tinh", Mathf.Max(0, left), s.potentialStones, s.potentialCrystals));
            }
            else
                m.Tips(Loc.F("Thua không mất lượt (còn {0} lượt). Chọn tướng khắc hệ {1}, khai phá tiềm năng hoặc thử tầng dễ hơn.", Mathf.Max(0, left), Elements.Name(cave.zone)));
            int up = cave.tier + 1;
            if (cw != null && cw.first && up < cfg.cave.tiers.Count && Potential.CaveCanEnter(s, cfg, cave.day, up))
            {
                var nextRef = new CaveRef { zone = cave.zone, tier = up, day = cave.day };
                m.Button(Loc.T("Tầng sau »"), BtnColor.Green, 230,
                    () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = Potential.CaveStage(d, cave.zone, up).id, team = team, cave = nextRef }));
            }
            if (Potential.CaveCanEnter(s, cfg, cave.day, cave.tier))
                m.Button(win ? Loc.T("Đánh tiếp") : Loc.T("Đánh lại"), win ? BtnColor.Paper : BtnColor.Green, 220,
                    () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stage.id, team = team, cave = cave }));
            m.Button(Loc.T("Về Hang"), BtnColor.Paper, 220, () => App.Router.Go(SceneIds.Cave));
            yield return new WaitForSecondsRealtime(0.12f);
            App.Audio.Play("stamp");
            Haptics.Play(Haptic.Stamp);
        }
    }
}
