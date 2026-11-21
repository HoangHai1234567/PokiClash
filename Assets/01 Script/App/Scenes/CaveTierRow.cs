// Một tầng của Hang Tiềm Năng (prefab Assets/04 Prefabs/Items/TangHang): "Tầng n: tên" màu theo độ sâu, cấp đề nghị (đỏ khi người chơi
// thấp hơn 2 cấp), đá thưởng mỗi lượt và thưởng lần đầu (đá, đá tinh, đá tiến hóa; "Đã qua" khi đã nhận), 2 ô địch (boss và tướng phụ:
// chân dung kit, "Lv n · Boss"), nút "Vào" (vao_tang_i). Tầng chưa mở (chưa qua tầng trước): ghi điều kiện, ẩn ô địch, nút khoá.
// 2026-11-17: 10 tầng mở lần lượt, thưởng lần đầu.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class CaveTierRow : MonoBehaviour
    {
        // màu tên tầng theo độ sâu: xanh lá → lam → cam → tím → đỏ
        static readonly string[] TierColors = { "#6cbf4f", "#4f9d3a", "#4a90d9", "#2f6fc0", "#f39a2d", "#d9771b", "#9a3df0", "#7a2bd0", "#d9443a", "#b8202f" };

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

        // elem: hệ boss hôm nay (null: cuối tuần chưa chọn, ẩn ô địch); can: vào được (đã mở, còn lượt hoặc chưa qua lần đầu, đã có hệ)
        public void Bind(GameData d, SaveData s, int tier, Elem? elem, bool can, Action onGo)
        {
            var cfg = d.Cfg;
            var ct = cfg.cave.tiers[tier];
            bool unlocked = Potential.CaveUnlocked(s, cfg, tier), first = Potential.CaveFirst(s, tier);
            name = "tang_" + tier;
            title.text = Loc.F("Tầng {0}: {1}", tier + 1, ct.Name) + (!first ? Loc.T(" · Đã qua") : "");
            title.color = unlocked ? Theme.Hex(TierColors[Mathf.Min(tier, TierColors.Length - 1)]) : Theme.Ink3;
            bool low = s.level < ct.level - 2;
            level.text = !unlocked ? Loc.F("Qua tầng {0} để mở · cấp {1}", tier, ct.level) : Loc.F("Cấp đề nghị {0}", ct.level) + (low ? Loc.F(" (bạn cấp {0})", s.level) : "");
            level.color = !unlocked ? Theme.Ink3 : low ? Theme.RedD : Theme.Ink2;

            // tối đa 2 dòng ngắn (khung chữ tự co, không xuống dòng): đá mỗi lượt, rồi thưởng lần đầu
            string line1 = Loc.F("Thắng: +{0} đá tiềm năng", ct.stones) +
                           (tier + 1 >= cfg.cave.crystalFloor && cfg.cave.crystalDaily > 0 ? Loc.F(", lượt đầu ngày +{0} đá tinh", cfg.cave.crystalDaily) : "");
            var fp = new List<string>();
            if (first)
            {
                if (ct.firstStones > 0) fp.Add(Loc.F("{0} đá", ct.firstStones));
                if (ct.firstCrystals > 0) fp.Add(Loc.F("{0} đá tinh", ct.firstCrystals));
                if (ct.firstEvo > 0) fp.Add(Loc.F("{0} đá tiến hóa", ct.firstEvo));
            }
            reward.text = fp.Count > 0 ? line1 + Loc.T("\nLần đầu: ") + string.Join(", ", fp) : line1;

            var st = elem is Elem z && unlocked ? Potential.CaveStage(d, z, tier) : null;
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
            go.SetText(!unlocked ? Loc.T("Khoá") : first ? Loc.T("Vượt") : Loc.T("Vào"));
            go.SetOnClick(onGo);
            go.Interactable = can;
        }
    }
}
