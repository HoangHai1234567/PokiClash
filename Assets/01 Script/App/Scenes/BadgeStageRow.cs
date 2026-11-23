// Một trận trong danh sách của Đền Huy Hiệu (prefab Assets/04 Prefabs/Items/TranHuyHieu): nền theo trạng thái (đang đánh vàng,
// đã thắng xanh, chưa tới xám), chân dung boss (bóng sẫm nếu chưa tới), "Trận i · Lv · tên địch", hàng sao (0–3 sao cao nhất), nút "Đánh"
// (trận đang đánh) hoặc "Đánh lại" (trận đã thắng chưa đủ 3 sao; tên danh_tran), dấu tích (đủ 3 sao) / ổ khoá (chưa tới).
// 2026-11-17: sao từng trận, đánh lại lấy sao. Hàng sao do menu "PokiClash/Prefab/Đền Huy Hiệu: sao trận, chọn bậc, mốc sao" dựng
// (Editor/SideMetaUiMenu.cs); prefab chưa dựng lại thì sao ghi vào dòng chữ.
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
        [SerializeField] UiStars stars; // 2026-11-17, có thể trống

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

        // trận i (từ 1) trong n trận của bậc; now: trận đang đánh; star: sao cao nhất (0 chưa thắng)
        public void Bind(GameData d, StageDef st, int i, int n, bool won, bool now, int star, Action onFight)
        {
            name = "tran_" + i;
            bg.color = now ? Theme.Hex("#fff3c4") : won ? Theme.Hex("#eaf6df") : Theme.Hex("#f3ece0");
            layout.preferredHeight = n > 5 ? 104 : 124;
            portrait.Bind(d.Hero(st.enemies[0].hero), n > 5 ? 86 : 104, !won && !now, Teams.EnemyStar(st.enemies[0].level));
            var names = string.Join(", ", st.enemies.Select(e => d.Hero(e.hero).name));
            text.text = Loc.F("Trận {0} · Lv{1} · {2}", i, st.enemies[0].level, names) + (i == n ? " · BOSS" : "") + (won && !stars ? $" · {star}/3 sao" : "");
            text.color = now || won ? Theme.Ink : Theme.Ink3;
            text.textWrappingMode = TextWrappingModes.Normal; // trận nhiều địch xuống hai dòng (một dòng co còn 18, soát UI 2026-11-23)
            if (stars)
            {
                stars.gameObject.SetActive(won);
                if (won) stars.Set(star, 3);
            }
            bool replay = won && star < 3;
            fight.gameObject.SetActive(now || replay);
            fight.SetText(now ? Loc.T("Đánh") : Loc.T("Đánh lại"));
            fight.SetRole(now ? BtnColor.Green : BtnColor.Paper);
            fight.SetOnClick(onFight);
            wonMark.SetActive(!now && won && !replay);
            lockMark.SetActive(!now && !won);
        }
    }
}
