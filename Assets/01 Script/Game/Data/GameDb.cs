// Gom 4 asset dữ liệu thành GameData của phần lõi (GameData.Current) lúc khởi động.
using System.Collections.Generic;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash.Game
{
    public static class GameDb
    {
        public static GameData Data => GameData.Current;

        public static GameData Build(HeroDb heroes, CardDb cards, ZoneDb zones, BalanceConfigAsset balance)
        {
            // tên theo ngôn ngữ đang dùng (LocService.Init chạy trước): tiếng Việt dùng thẳng đối tượng của asset, ngôn ngữ khác dùng bản sao đã dịch
            var d = new GameData
            {
                Heroes = LocData.All(heroes.heroes, LocData.Hero),
                Minions = LocData.All(heroes.minions, LocData.Hero),
                Starters = new List<string>(heroes.starters),
                LegendMilestoneHero = heroes.legendMilestoneHero,
                Pool = LocData.All(cards.pool, LocData.Card),
                Innate = LocData.All(cards.innate, LocData.Card),
                MinionCards = LocData.All(cards.minions, LocData.Card),
                Traits = LocData.All(cards.traits, LocData.Card),
                Zones = LocData.All(zones.zones, LocData.Zone),
                Stages = LocData.All(zones.stages, LocData.Stage),
                Village = zones.village,
                Cfg = balance.Resolve().Clone(), // ưu tiên bản mã hoá (enc); bản thử chưa re-import thì vẫn là cfg
            }.Index();
            var err = d.Validate();
            foreach (var e in err) Debug.LogError("[Dữ liệu] " + e);
            GameData.Current = d;
            return d;
        }
    }
}
