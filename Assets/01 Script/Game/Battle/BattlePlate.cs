// Bảng thông tin một bên trên sân (dựng sẵn hai bảng trong prefab Screens/Battle): tên, nhãn hệ, cấp, nhãn BOSS, thanh máu,
// mana, nộ, chip buff và trạng thái (prefab mục Items/TranChip), chấm đội dự bị (Items/TranCham). Chip và chấm dùng lại, thừa thì tắt.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BattlePlate : MonoBehaviour
    {
        [SerializeField] TextMeshProUGUI nameText, level;
        [SerializeField] UiElemTag elemTag;
        [SerializeField] GameObject boss;
        [SerializeField] UiBar hp, mana, rage;
        [SerializeField] RectTransform chips, bench;
        [SerializeField] Image chipPrefab, dotPrefab;

        readonly List<Image> chipPool = new List<Image>();
        readonly List<TextMeshProUGUI> chipTexts = new List<TextMeshProUGUI>();
        readonly List<Image> dotPool = new List<Image>();

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI nameLbl, TextMeshProUGUI levelLbl, UiElemTag tag, GameObject bossTag, UiBar hpBar, UiBar manaBar, UiBar rageBar,
            RectTransform chipRow, RectTransform benchRow, Image chipItem, Image dotItem)
        {
            nameText = nameLbl;
            level = levelLbl;
            elemTag = tag;
            boss = bossTag;
            hp = hpBar;
            mana = manaBar;
            rage = rageBar;
            chips = chipRow;
            bench = benchRow;
            chipPrefab = chipItem;
            dotPrefab = dotItem;
        }

        // tướng đang ra sân: tên, hệ, cấp, BOSS
        public void Fill(Fighter f)
        {
            nameText.text = f.hero.name;
            elemTag.Set(f.hero.elem);
            level.text = $"Lv{f.level}";
            boss.SetActive(f.boss);
        }

        static string Pct(double x) => CardText.Pct(x);

        // thanh số, chip, chấm đội theo ảnh chụp của sự kiện
        public void Apply(Snap s, int side, BalanceConfig cfg)
        {
            var f = s.f[side][s.active[side]];
            hp.Set((float)f.hp, (float)f.maxHp, (float)f.shield, $"{f.hp}/{f.maxHp}{(f.shield > 0 ? $" +{f.shield} khiên" : "")}");
            mana.Set((float)f.mana, cfg.maxMana);
            rage.Set((float)f.rage, cfg.maxRage);
            int n = 0;
            if (f.atkB != 0) Chip(n++, $"Công {(f.atkB > 0 ? "+" : "−")}{Pct(Math.Abs(f.atkB))}", f.atkB > 0);
            if (f.defB != 0) Chip(n++, $"Thủ {(f.defB > 0 ? "+" : "−")}{Pct(Math.Abs(f.defB))}", f.defB > 0);
            foreach (var (id, left) in f.st)
            {
                string nm = id == StatusId.Burn ? "Bỏng" : id == StatusId.Stun ? "Choáng" : id == StatusId.Regen ? "Hồi" : "Né";
                bool bad = id == StatusId.Burn || id == StatusId.Stun;
                Chip(n++, id == StatusId.Burn || id == StatusId.Regen ? $"{nm} {left}" : nm, !bad);
            }
            for (int i = n; i < chipPool.Count; i++) chipPool[i].gameObject.SetActive(false);

            int m = 0;
            if (s.f[side].Count > 1)
                for (int i = 0; i < s.f[side].Count; i++)
                {
                    var x = s.f[side][i];
                    var dot = Dot(m++);
                    dot.color = x.dead ? Theme.Hex("#8a7a6a") : Theme.Green;
                    dot.rectTransform.sizeDelta = i == s.active[side] ? new Vector2(36, 36) : new Vector2(28, 28);
                }
            for (int i = m; i < dotPool.Count; i++) dotPool[i].gameObject.SetActive(false);
        }

        void Chip(int i, string text, bool up)
        {
            if (i >= chipPool.Count)
            {
                var c = Ui.Spawn(chipPrefab, chips);
                c.name = "chip";
                chipPool.Add(c);
                chipTexts.Add(c.GetComponentInChildren<TextMeshProUGUI>(true));
            }
            var bg = chipPool[i];
            bg.gameObject.SetActive(true);
            bg.color = up ? Theme.Hex("#d6f5c8") : Theme.Hex("#ffd2c8");
            chipTexts[i].text = text;
        }

        Image Dot(int i)
        {
            if (i >= dotPool.Count)
            {
                var d = Ui.Spawn(dotPrefab, bench);
                d.name = "cham";
                dotPool.Add(d);
            }
            dotPool[i].gameObject.SetActive(true);
            return dotPool[i];
        }
    }
}
