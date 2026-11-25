// Thay TestData (CoreGoldenTests.cs dùng UnityEngine.Application) khi chạy test ngoài Unity: JSON đọc ở out/data (có khối casino),
// file khác (golden) đọc ở Assets/02 Data thật
using System.IO;
using PokiClash.Core;

namespace PokiClash.Tests
{
    public static class TestData
    {
        public const string OldStarter = "ti_tach";
        public static string DataDir => @"C:\Atomik\PokiWar\Assets\02 Data";
        static GameData cached;

        public static string Read(string rel) =>
            rel.StartsWith("Json/") ? File.ReadAllText(Path.Combine("data", rel.Substring(5))) : File.ReadAllText(Path.Combine(DataDir, rel));

        public static GameData Load() => cached ??= GameData.FromJson(
            Read("Json/heroes.json"), Read("Json/cards.json"), Read("Json/zones.json"), Read("Json/stages.json"), Read("Json/balance.json"));

        public static StageDef AtLevel(StageDef st, int lv)
        {
            var c = new StageDef { id = st.id, zone = st.zone, idx = st.idx, name = st.name, kind = st.kind, tag = st.tag, chapter = st.chapter, drops = st.drops };
            foreach (var e in st.enemies) c.enemies.Add(new StageEnemy { hero = e.hero, level = lv, boss = e.boss, evo = e.evo, buff = e.buff });
            return c;
        }
    }
}
