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
            var d = new GameData
            {
                Heroes = new List<HeroDef>(heroes.heroes),
                Minions = new List<HeroDef>(heroes.minions),
                Starters = new List<string>(heroes.starters),
                LegendMilestoneHero = heroes.legendMilestoneHero,
                Pool = new List<CardDef>(cards.pool),
                Innate = new List<CardDef>(cards.innate),
                MinionCards = new List<CardDef>(cards.minions),
                Zones = new List<ZoneDef>(zones.zones),
                Stages = new List<StageDef>(zones.stages),
                Village = zones.village,
                Cfg = balance.cfg.Clone(),
            }.Index();
            var err = d.Validate();
            foreach (var e in err) Debug.LogError("[Dữ liệu] " + e);
            GameData.Current = d;
            return d;
        }
    }
}
