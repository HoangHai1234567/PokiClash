// Một trận trong danh sách của Đền Huy Hiệu (prefab Assets/04 Prefabs/Items/TranHuyHieu): nền theo trạng thái (đang đánh vàng,
// đã thắng xanh, chưa tới xám), chân dung boss (bóng sẫm nếu chưa tới), "Trận i · Lv · tên địch", nút "Đánh" (danh_tran) hoặc dấu tích / ổ khoá.
using System;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BadgeStageRow : MonoBehaviour
    {
        [SerializeField] Image bg;
        [SerializeField] LayoutElement layout;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI text;
        [SerializeField] SketchButton fight;
        [SerializeField] GameObject wonMark, lockMark;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image panel, LayoutElement layoutElement, HeroPortrait boss, TextMeshProUGUI label, SketchButton fightButton,
            GameObject wonIcon, GameObject lockIcon)
        {
            bg = panel;
            layout = layoutElement;
            portrait = boss;
            text = label;
            fight = fightButton;
            wonMark = wonIcon;
            lockMark = lockIcon;
        }

        // trận i (từ 1) trong n trận của bậc; now: trận đang đánh
        public void Bind(GameData d, StageDef st, int i, int n, bool won, bool now, Action onFight)
        {
            name = "tran_" + i;
            bg.color = now ? Theme.Hex("#fff3c4") : won ? Theme.Hex("#eaf6df") : Theme.Hex("#f3ece0");
            layout.preferredHeight = n > 5 ? 104 : 124;
            portrait.Bind(d.Hero(st.enemies[0].hero), n > 5 ? 86 : 104, !won && !now, Teams.EnemyStar(st.enemies[0].level));
            var names = string.Join(", ", st.enemies.Select(e => d.Hero(e.hero).name));
            text.text = $"Trận {i} · Lv{st.enemies[0].level} · {names}" + (i == n ? " · BOSS" : "");
            text.color = now || won ? Theme.Ink : Theme.Ink3;
            fight.gameObject.SetActive(now);
            fight.SetOnClick(onFight);
            wonMark.SetActive(!now && won);
            lockMark.SetActive(!now && !won);
        }
    }
}
