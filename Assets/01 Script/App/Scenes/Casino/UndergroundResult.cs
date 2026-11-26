// Kết trận Đấu trường ngầm (BattleController gọi khi trận có UgRef; GD_Claude/29_DaoCasino.md mục 6.5): thắng lần đầu trong ngày
// được winMult × lệ phí + mảnh tướng chủ lực + quà bậc; thắng lại hoàn lệ phí + quà nhỏ; thua mất lệ phí (đã trả lúc bấm Đánh).
// Nút: "Đánh lại" (trả lệ phí lần nữa), "Về Hầm đấu" (về scene Hầm đấu kèm UgReturn: Lão Mực phản ứng theo kết quả).
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public static class UndergroundResult
    {
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        public static IEnumerator Run(Battle b, UgRef ug, StageDef stage, List<string> team, BattleResultDialog resultPrefab)
        {
            var s = App.Save.Data;
            var d = App.Data;
            double now = SaveService.Now();
            bool win = b.winner == 0;
            s.stats.battles++;
            if (win) s.stats.wins++;
            var r = Underground.Finish(s, d, ug.tier, win, now, new Rng(Rng.RandomSeed()));
            App.Save.Save();
            App.Audio.Play(win ? "win" : "lose");
            Haptics.Play(win ? Haptic.Win : Haptic.Lose);
            var t = d.Cfg.casino.underground.tiers[ug.tier];
            var m = App.Modals.Open(resultPrefab, mandatory: true);
            m.Show(win, Loc.F("Hầm đấu · {0}: {1}", t.Name, stage.name), 38, Loc.F("{0} hiệp · gây {1} sát thương", b.round, b.dmgDealt[0]));
            if (win)
            {
                if (r.balls > 0) m.Reward().Item(Icon("ball"), $"×{r.balls}", Loc.T("Bi"), Rarity.Common).Tag(r.first ? Loc.T("Lần đầu") : Loc.T("Thắng lại"), Theme.Yellow);
                foreach (var rw in r.rewards)
                {
                    if (rw.k == RewardKind.Shards && d.Hero(rw.res?.hero ?? rw.hero) is HeroDef h) m.Reward().Hero(h, $"×{rw.res?.n ?? rw.n}");
                    else if (rw.k == RewardKind.EvoStones) m.Reward().EvoStones(rw.n);
                    else if (rw.k == RewardKind.Stones) m.Reward().Item(Icon("rock"), $"×{rw.n}", Loc.T("Đá tiềm năng"), Rarity.Epic);
                    else if (rw.k == RewardKind.Crystal) m.Reward().Item(Icon("shard"), $"×{rw.n}", Loc.T("Đá tinh"), Rarity.Legend);
                }
                m.Tips(r.first ? Loc.T("Thắng lần đầu hôm nay: thưởng đầy đủ. Đánh lại vẫn hoàn lệ phí và có quà nhỏ.")
                    : Loc.T("Đã thắng bậc này hôm nay: hoàn lệ phí và quà nhỏ. Mai đội ngầm đổi mới."));
            }
            else
                m.Tips(Loc.T("Thua thì mất lệ phí. Thử đội khắc hệ chủ lực của đối thủ, xem luật ngày, hoặc đánh bậc dễ hơn."));
            int tier = ug.tier;
            // hết lượt đánh trong ngày thì không mời đánh lại
            if (Underground.FightsLeft(s, d, now) > 0 && Underground.TierOpen(s, d, tier) && Underground.TiersToday(d, now).Contains(tier)
                && !(t.weekly && Underground.WonToday(s, d, tier, now)))
                m.Button(Loc.F("Đánh lại · {0} bi", Underground.Fee(s, d, tier)), win ? BtnColor.Paper : BtnColor.Green, 300, () =>
                {
                    if (!Underground.Pay(s, d, tier, SaveService.Now(), out var why))
                    {
                        App.Toasts.Show(why, Icon("lock"));
                        return;
                    }
                    App.Save.Save();
                    App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stage.id, team = team, ug = new UgRef { tier = tier, day = Casino.Today(SaveService.Now()) } });
                });
            m.Button(Loc.T("Về Hầm đấu"), BtnColor.Paper, 260, () => App.Router.Go(SceneIds.CasinoUnderground, new UgReturn { tier = tier, won = win }));
            yield return new WaitForSecondsRealtime(0.12f);
            App.Audio.Play("stamp");
            Haptics.Play(Haptic.Stamp);
        }
    }
}
