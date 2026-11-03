// Menu "PokiClash/Nhập dữ liệu": đọc Assets/02 Data/Json/*.json (nguồn số liệu; lần cuối xuất từ bản web 2026-11-03, từ đó sửa thẳng),
// kiểm tra, rồi dựng HeroDb, CardDb, ZoneDb, BalanceConfig trong Assets/02 Data. Không sửa tay các asset này.
// Đừng chạy lại Web/scripts/export_data.ts vào thư mục này: script web còn xuất bộ 8 ải cũ, không có lính.
using System.Collections.Generic;
using System.IO;
using PokiClash.Core;
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class DataImporter
    {
        public const string DataDir = "Assets/02 Data";
        const string JsonDir = DataDir + "/Json";

        [MenuItem("PokiClash/Nhập dữ liệu", priority = 10)]
        public static void Import() => Run(true);

        public static bool Run(bool log)
        {
            GameData d;
            try
            {
                string Read(string f) => File.ReadAllText(Path.Combine(JsonDir, f));
                d = GameData.FromJson(Read("heroes.json"), Read("cards.json"), Read("zones.json"), Read("stages.json"), Read("balance.json"));
            }
            catch (System.Exception e)
            {
                Debug.LogError($"[Dữ liệu] Không đọc được JSON trong {JsonDir}: {e.Message}");
                return false;
            }
            var err = d.Validate();
            foreach (var e in err) Debug.LogError("[Dữ liệu] " + e);
            if (err.Count > 0) return false;

            var heroes = LoadOrCreate<HeroDb>("HeroDb");
            heroes.heroes = d.Heroes;
            heroes.minions = d.Minions;
            heroes.starters = d.Starters;
            heroes.legendMilestoneHero = d.LegendMilestoneHero;
            EditorUtility.SetDirty(heroes);

            var cards = LoadOrCreate<CardDb>("CardDb");
            cards.pool = d.Pool;
            cards.innate = d.Innate;
            cards.minions = d.MinionCards;
            EditorUtility.SetDirty(cards);

            var zones = LoadOrCreate<ZoneDb>("ZoneDb");
            zones.zones = d.Zones;
            zones.stages = d.Stages;
            zones.village = d.Village;
            EditorUtility.SetDirty(zones);

            var bal = LoadOrCreate<BalanceConfigAsset>("BalanceConfig");
            bal.cfg = d.Cfg;
            EditorUtility.SetDirty(bal);

            AssetDatabase.SaveAssets();
            if (log)
                Debug.Log($"[Dữ liệu] Đã nhập: {d.Heroes.Count} tướng, {d.Minions.Count} lính, {d.Pool.Count} thẻ chung, {d.Innate.Count} thẻ riêng, " +
                          $"{d.Zones.Count} đảo, {d.Stages.Count} ải.");
            return true;
        }

        public static T LoadOrCreate<T>(string name) where T : ScriptableObject
        {
            var path = $"{DataDir}/{name}.asset";
            var a = AssetDatabase.LoadAssetAtPath<T>(path);
            if (a) return a;
            a = ScriptableObject.CreateInstance<T>();
            AssetDatabase.CreateAsset(a, path);
            return a;
        }
    }
}
