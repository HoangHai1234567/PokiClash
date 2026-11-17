// Kết trận thử thách Đền Huy Hiệu (BattleController gọi khi trận có BadgeRef; 2026-11-17 tách khỏi BattleController để side meta tự sửa):
// - thắng: chấm sao (thắng; không tướng nào gục; thắng trong số hiệp theo số địch), ô thưởng sao (nhãn "Mới!" khi hơn sao cũ), bi (trận
//   đang đánh), đá tiến hóa và đá tinh khi xong bậc, quà mốc sao; dòng ghi điều kiện từng sao;
// - thua: tiến độ giữ, lời khuyên;
// - nút: "Trận tiếp »" (trận đang đánh của dãy), "Đánh lại" (thua, hoặc thắng mà chưa đủ 3 sao), "Về Đền";
// - xong bậc: hộp huy hiệu (phần cộng, đặc tính hệ, phần cộng cả đội) rồi mở rương; mốc sao có rương thì mở tiếp; sau cùng hộp lên cấp.
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public static class BadgeResult
    {
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // "Sao 1 thắng: có · Sao 2 không tướng nào gục: chưa · Sao 3 thắng trong 4 hiệp: có"
        public static string StarLine(BalanceConfig cfg, Battle b)
        {
            var (win, safe, fast) = Badges.StarChecks(cfg, b);
            string Mark(bool ok) => ok ? "có" : "chưa";
            return $"Sao 1 thắng: {Mark(win)} · Sao 2 không tướng nào gục: {Mark(safe)} · Sao 3 thắng trong {Badges.StarRounds(cfg, b.sides[1].fighters.Count)} hiệp: {Mark(fast)}";
        }

        public static IEnumerator Run(Battle b, BadgeRef badge, StageDef stage, List<string> team, BattleResultDialog resultPrefab, BadgeWinDialog badgePrefab)
        {
            var s = App.Save.Data;
            var d = App.Data;
            var cfg = d.Cfg;
            bool win = b.winner == 0;
            int before = s.level;
            var rng = new Rng(Rng.RandomSeed());
            BadgeWin rw = null;
            s.stats.battles++;
            if (win)
            {
                s.stats.wins++;
                rw = Badges.Win(s, d, badge.zone, badge.tier, badge.i, Badges.Grade(cfg, b), rng);
            }
            App.Save.Save();
            App.Audio.Play(win ? "win" : "lose");

            int n = Badges.Count(cfg, badge.tier);
            var m = App.Modals.Open(resultPrefab, mandatory: true);
            m.Show(win, $"Đền · {Elements.Name(badge.zone)} · {Badges.TierName(cfg, badge.tier)} {badge.i}/{n}", 38,
                $"{b.round} hiệp · gây {b.dmgDealt[0]} sát thương");
            if (rw != null)
            {
                bool better = rw.stars > rw.oldStars;
                m.Reward().Item(Icon("star"), $"×{rw.stars}", "Sao trận", rw.stars >= 3 ? Rarity.Legend : rw.stars == 2 ? Rarity.Epic : Rarity.Rare)
                    .Tag(rw.replay ? (better ? "Mới!" : $"Cũ {rw.oldStars}") : "", Theme.Yellow);
                if (rw.balls > 0) m.Reward().Item(Icon("ball"), $"×{rw.balls}", "Bi").Tag(rw.tierDone > 0 ? "Xong bậc!" : $"{badge.i}/{n}", Theme.Yellow);
                if (rw.evo > 0) m.Reward().EvoStones(rw.evo);
                if (rw.crystal > 0) PotentialPanel.CrystalTile(m.Reward(), rw.crystal);
                int gEvo = rw.gifts.Sum(g => g.gift.evo), gCry = rw.gifts.Sum(g => g.gift.crystal), gSt = rw.gifts.Sum(g => g.gift.stones);
                if (gEvo > 0) m.Reward().EvoStones(gEvo).Tag("Mốc sao", Theme.Yellow);
                if (gCry > 0) PotentialPanel.CrystalTile(m.Reward(), gCry).Tag("Mốc sao", Theme.Yellow);
                if (gSt > 0) m.Reward().Item(Icon("rock"), $"×{gSt}", "Đá tiềm năng", Rarity.Epic).Tag("Mốc sao", Theme.Yellow);
                int total = Badges.TotalStars(s, cfg), next = Badges.NextGift(s, cfg);
                m.Tips(StarLine(cfg, b) + $"\nSao đền: {total}" + (next > 0 ? $" · mốc kế {Badges.GiftAt(cfg, next)} sao" : " · đã nhận hết mốc"));
            }
            else
                m.Tips("Thua thì đánh lại trận này, tiến độ vẫn giữ. Chọn tướng khắc hệ " + Elements.Name(badge.zone) +
                       ", nâng thẻ, tiến hóa và khai phá tiềm năng để mạnh hơn.");

            var cur = Badges.Current(s, cfg, badge.zone);
            bool sameAsCur = cur != null && cur.Value.tier == badge.tier && cur.Value.i == badge.i;
            if (win && cur != null && !sameAsCur && (rw == null || rw.tierDone == 0))
            {
                var nextRef = new BadgeRef { zone = badge.zone, tier = cur.Value.tier, i = cur.Value.i };
                m.Button("Trận tiếp »", BtnColor.Green, 240,
                    () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = Badges.StageId(d, nextRef.zone, nextRef.tier, nextRef.i), team = team, badge = nextRef }));
            }
            if (!win || Badges.Stars(s, cfg, badge.zone, badge.tier, badge.i) < 3)
                m.Button("Đánh lại", win ? BtnColor.Paper : BtnColor.Green, 220,
                    () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stage.id, team = team, badge = badge }));
            m.Button("Về Đền", BtnColor.Paper, 220, () => App.Router.Go(SceneIds.Badges, badge.zone));
            yield return new WaitForSecondsRealtime(0.12f);
            App.Audio.Play("stamp");

            if (rw != null && rw.tierDone > 0)
            {
                // hộp huy hiệu rồi mở rương (trên hộp kết quả)
                yield return new WaitForSecondsRealtime(0.5f);
                bool closed = false;
                App.Audio.Play("level");
                var bm = App.Modals.Open(badgePrefab, () => closed = true);
                bm.Show(badge.zone, rw.tierDone, $"Huy hiệu {Elements.Name(badge.zone)} · {Badges.TierName(cfg, rw.tierDone)}", TierBody(cfg, badge.zone, rw.tierDone),
                    $"Mở {Pachinko.ChestName(rw.chest)}");
                while (!closed) yield return null;
                yield return ChestBox.Show(Pachinko.ChestName(rw.chest), rw.chest, null, rw.rewards, "Nhận");
            }
            if (rw != null)
                foreach (var g in rw.gifts.Where(g => !string.IsNullOrEmpty(g.gift.chest)))
                    yield return ChestBox.Show($"Mốc {g.at} sao · {Pachinko.ChestName(g.chest)}", g.chest, null, g.rewards, "Nhận");
            if (s.level > before) Dialogs.LevelUp(before, s.level);
        }

        // chữ hộp huy hiệu: phần cộng, đặc tính hệ (nếu bậc này mở hoặc nâng), phần cộng cả đội
        public static string TierBody(BalanceConfig cfg, Elem z, int tier)
        {
            var lines = new List<string> { $"Tướng hệ {Elements.Name(z)} +{Badges.Bonus(cfg, tier) * 100:0}% Máu, Công, Thủ (bậc cao nhất, không cộng dồn)." };
            int lv = Badges.TraitLevel(cfg, tier);
            if (lv > 0 && cfg.badges.traitTiers.Contains(tier))
                lines.Add((lv == 1 ? "Mở đặc tính " : "Nâng đặc tính ") + Badges.TraitText(cfg, z, lv) + $" cho tướng hệ {Elements.Name(z)}.");
            double team = Badges.TeamBonusOf(cfg, tier);
            if (team > 0) lines.Add($"Mọi tướng +{team * 100:0.#}% Máu, Công, Thủ (cộng với các dãy khác).");
            return string.Join("\n", lines);
        }
    }
}
