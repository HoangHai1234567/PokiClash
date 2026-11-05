// Một đối thủ trong hộp Chuẩn bị trận, mỗi đối thủ một hàng (người dùng dặn 2026-11-04: tướng bên trái, thông tin bên phải, chữ to,
// cấp rõ). Hai prefab cùng component, dựng bằng menu "PokiClash/Prefab/Hộp chuẩn bị: ô đối thủ trái phải":
// - Items/DoiThu: hàng to cho ải một địch: chân dung trái; phải là tên, nhãn hệ và lực chiến, dòng ghi chú, 3 hàng Máu, Công, Thủ;
// - Items/DoiThuGon: hàng gọn cho ải 2–3 địch: ghi chú chung hàng với nhãn hệ, Máu, Công, Thủ xếp ngang.
// Chip cấp ("Cấp 20", cùng kiểu chip cấp người chơi trên thanh trên) ở góc trên trái chân dung, chữ đỏ khi địch hơn người chơi quá
// 2 cấp (như dòng cảnh báo của hộp). Dòng ghi chú: "Boss", "Cường hóa +12%", "Yếu hơn 20%", "Lính, không thu phục".
// Chỉ số không so với tướng người chơi (người dùng dặn 2026-11-04, dễ hiểu lầm). Tướng tiến hóa trong trận (ải tướng, boss) chỉ hiện
// dạng đầu với chỉ số của dạng đó; đầu mục của hộp ghi luật tiến hóa. Hàng neo mép trên khung đối thủ, StagePrepDialog xếp dọc.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class PrepFoe : MonoBehaviour
    {
        [SerializeField] HeroPortrait portrait;
        [Tooltip("Ô chân dung: hình phóng cho phần có hình vừa ô, căn giữa")]
        [SerializeField] RectTransform portraitBox;
        [SerializeField] TextMeshProUGUI heroName;
        [SerializeField] UiChip levelChip;
        [SerializeField] UiElemTag elem;
        [SerializeField] GameObject boss;
        [SerializeField] TextMeshProUGUI power;
        [Tooltip("Số Máu, Công, Thủ")]
        [SerializeField] TextMeshProUGUI[] stats;

        public float Height => ((RectTransform)transform).sizeDelta.y;

        // Dùng khi nướng prefab (Editor).
        public void Setup(HeroPortrait por, RectTransform box, TextMeshProUGUI nameText, UiChip lvChip, UiElemTag elemTag, GameObject note,
            TextMeshProUGUI powerText, TextMeshProUGUI[] statTexts)
        {
            portrait = por;
            portraitBox = box;
            heroName = nameText;
            levelChip = lvChip;
            elem = elemTag;
            boss = note;
            power = powerText;
            stats = statTexts;
        }

        // s: chỉ số khi vào trận (HeroStats.InBattle, tướng tiến hóa là dạng đầu); powerValue: lực chiến (HeroStats.Power, tướng tiến
        // hóa tính cả dòng), 0 thì ẩn; playerLevel: cấp người chơi (tô đỏ chip cấp khi địch hơn quá 2 cấp)
        public void Bind(HeroDef h, StageEnemy en, Stats s, int powerValue, int playerLevel)
        {
            name = "doi_thu_" + h.id;
            Power(powerValue);
            if (stats != null)
                for (int i = 0; i < stats.Length && i < 3; i++)
                    if (stats[i]) stats[i].text = TeamPower.Text((int)Math.Round(i == 0 ? s.hp : i == 1 ? s.atk : s.def));
            int star = Teams.EnemyFormStar(en);
            FitPortrait(h, star);
            heroName.text = h.Form(App.Data.Cfg.formStars, star).name;
            if (levelChip)
            {
                levelChip.Value.text = $"Cấp {en.level}";
                levelChip.Value.color = en.level > playerLevel + 2 ? Theme.RedD : Theme.Ink;
            }
            elem.Set(h.elem);
            // dòng ghi chú: boss (kèm tên bị động boss nếu có, mô tả ở dòng gợi ý của hộp), cường hóa của ải (đảo 70 ải), lính
            string buff = en.buff > 0 ? $"Cường hóa +{Math.Round(en.buff * 100)}%" : en.buff < 0 ? $"Yếu hơn {Math.Round(-en.buff * 100)}%" : null;
            string trait = string.IsNullOrEmpty(en.trait) ? null : App.Data.Card(en.trait)?.name;
            string head = trait != null ? $"Boss · {trait}" : "Boss";
            string line = en.boss ? (buff != null ? $"{head} · {buff}" : head) : buff ?? (h.minion ? "Lính, không thu phục" : null);
            boss.SetActive(line != null);
            if (line == null) return;
            if (h.minion && !en.boss && en.buff != 0) line += " · lính";
            BossText(line, en.boss || en.buff > 0 ? Theme.Red : en.buff < 0 ? Theme.Hex("#3a8a3a") : Theme.Ink2);
        }

        // đặt hàng cách mép trên khung đối thủ y
        public void Place(float y)
        {
            var rt = (RectTransform)transform;
            rt.anchoredPosition = new Vector2(rt.anchoredPosition.x, -y);
        }

        // hình to nhỏ trong khung ảnh khác nhau (lính nhỏ, boss to): phóng phần có hình (PortraitBoxes) vừa ô chân dung, tâm phần có
        // hình vào giữa ô; hình rất nhỏ chỉ phóng tới gấp đôi ô (ảnh 512 phóng quá thì mờ)
        void FitPortrait(HeroDef h, int star)
        {
            var box = portraitBox.sizeDelta;
            var c = PortraitBoxes.Of(HeroArt.FormOf(h, star).aola);
            const float aspect = HeroArt.W / (float)HeroArt.H;
            float height = Mathf.Min(box.y / Mathf.Max(0.05f, c.height), box.x / Mathf.Max(0.05f, c.width * aspect));
            portrait.Bind(h, Mathf.Min(height, box.y * 2), false, star);
            var rt = portrait.Rect;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.pivot = c.center;
            rt.anchoredPosition = Vector2.zero;
        }

        void Power(int v)
        {
            if (!power) return;
            power.transform.parent.gameObject.SetActive(v > 0);
            power.text = TeamPower.Text(v);
        }

        void BossText(string t, Color color)
        {
            var tmp = boss.GetComponentInChildren<TextMeshProUGUI>(true);
            if (!tmp) return;
            tmp.text = t;
            tmp.color = color;
        }
    }
}
