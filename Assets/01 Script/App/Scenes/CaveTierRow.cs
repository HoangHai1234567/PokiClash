// Một tầng của Hang Tiềm Năng (prefab Assets/04 Prefabs/Items/TangHang): tên tầng màu theo bậc, cấp đề nghị (đỏ khi người chơi
// thấp hơn 2 cấp), đá thưởng, 2 ô địch (boss và tướng phụ: chân dung kit, "Lv n · Boss"), nút "Vào" (vao_tang_i).
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class CaveTierRow : MonoBehaviour
    {
        static readonly string[] TierColors = { "#6cbf4f", "#4a90d9", "#f39a2d", "#9a3df0" };

        [SerializeField] TextMeshProUGUI title, level, reward;
        [SerializeField] HeroPortrait[] enemies; // boss, tướng phụ
        [SerializeField] TextMeshProUGUI[] enemyLabels;
        [SerializeField] SketchButton go;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, TextMeshProUGUI levelText, TextMeshProUGUI rewardText, HeroPortrait[] enemyPortraits,
            TextMeshProUGUI[] enemyTexts, SketchButton goButton)
        {
            title = titleText;
            level = levelText;
            reward = rewardText;
            enemies = enemyPortraits;
            enemyLabels = enemyTexts;
            go = goButton;
        }

        // elem: hệ boss hôm nay (null: cuối tuần chưa chọn, ẩn ô địch); can: còn lượt và đã có hệ
        public void Bind(GameData d, SaveData s, int tier, Elem? elem, bool can, Action onGo)
        {
            var ct = d.Cfg.cave.tiers[tier];
            name = "tang_" + tier;
            title.text = $"Tầng {ct.name}";
            title.color = Theme.Hex(TierColors[Mathf.Min(tier, 3)]);
            bool low = s.level < ct.level - 2;
            level.text = $"Cấp đề nghị {ct.level}" + (low ? $" (bạn cấp {s.level})" : "");
            level.color = low ? Theme.RedD : Theme.Ink2;
            reward.text = $"Thắng: +{ct.stones} đá tiềm năng";

            var st = elem is Elem z ? Potential.CaveStage(d, z, tier) : null;
            for (int i = 0; i < enemies.Length; i++)
            {
                bool shown = st != null && i < st.enemies.Count;
                enemies[i].gameObject.SetActive(shown);
                enemyLabels[i].gameObject.SetActive(shown);
                if (!shown) continue;
                var en = st.enemies[i];
                enemies[i].Bind(d.Hero(en.hero), en.boss ? 160 : 120, false, Teams.EnemyStar(en.level));
                enemyLabels[i].text = $"Lv{en.level}" + (en.boss ? " · Boss" : "");
                enemyLabels[i].color = en.boss ? Theme.Red : Theme.Ink2;
            }

            go.name = "vao_tang_" + tier;
            go.SetOnClick(onGo);
            go.Interactable = can;
        }
    }
}
