// Một ải trong bảng chặng của đảo 70 ải (prefab Assets/04 Prefabs/Items/DongChang, dựng bằng menu
// "PokiClash/Prefab/Đảo 70 ải (ChamAi, DongChang, BangChang)"): số ải, kiểu ải, bi, tối đa 3 địch (chân dung, nhãn cấp, BOSS,
// cường hóa ±%), dấu qua / chơi / khoá. Nền vàng là ải đang đánh, xanh là đã qua, xám là chưa mở. Chạm mở hộp Chuẩn bị trận.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ZoneChapterRow : MonoBehaviour
    {
        public const float Height = 150;

        [Serializable]
        public struct Foe
        {
            public GameObject root;
            public HeroPortrait portrait;
            public TextMeshProUGUI label;
        }

        [Serializable]
        public struct Parts
        {
            public Image bg, state;
            public ClickCatcher click;
            public TextMeshProUGUI idx, tag, balls;
            public Foe[] foes;
        }

        [SerializeField] Parts p;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // nhãn dưới hình địch: cấp, BOSS, cường hóa (+%) hoặc yếu đi (−%)
        public static string EnemyLabel(StageEnemy e)
        {
            string b = e.buff != 0 ? $" {(e.buff > 0 ? "+" : "−")}{Math.Round(Math.Abs(e.buff) * 100)}%" : "";
            return $"Lv{e.level}{(e.boss ? " BOSS" : "")}{b}";
        }

        // tên kiểu ải: boss, mini boss theo loại ải, còn lại theo kiểu (Islands.TagName)
        public static string TagText(StageDef st) =>
            st.kind == StageKind.Boss ? "Boss đảo" : st.kind == StageKind.Mini ? "Mini boss" : Islands.TagName(st.tag);

        public void Bind(StageDef st, GameData d, bool open, bool cleared, bool current, int balls, Action onClick)
        {
            name = "ai_" + st.idx;
            p.bg.color = !open ? Theme.Hex("#e2dccd") : current ? Theme.Hex("#fff3c4") : cleared ? Theme.Hex("#eaf6df") : Theme.CardFill;
            p.idx.text = st.idx.ToString();
            p.tag.text = TagText(st);
            p.tag.color = st.kind != StageKind.Normal || st.tag == StageTag.Gate || st.tag == StageTag.Elite ? Theme.Red : Theme.Ink;
            p.balls.text = $"+{balls} bi";
            for (int i = 0; i < p.foes.Length; i++)
            {
                var f = p.foes[i];
                bool shown = i < st.enemies.Count;
                f.root.SetActive(shown);
                if (!shown) continue;
                var en = st.enemies[i];
                f.portrait.Bind(d.Hero(en.hero), en.boss ? 116 : 100, !open, Teams.EnemyFormStar(en));
                f.label.text = EnemyLabel(en);
                f.label.color = en.boss || en.buff > 0 ? Theme.Red : Theme.Ink;
            }
            Theme.SetSprite(p.state, Icon(cleared ? "check" : open ? "play" : "lock"));
            p.click.OnClick = onClick;
        }
    }
}
