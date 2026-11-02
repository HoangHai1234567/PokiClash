// Hộp Chuẩn bị trận dùng chung cho ải đảo, Đền Huy Hiệu, Hang Tiềm Năng (prefab Assets/04 Prefabs/Dialogs/ChuanBiTran):
// đầu hộp và nhãn kiểu, cảnh báo quá sức, đối thủ (Items/DoiThu), thưởng (Items/ThuongTran), 3 ô đội hình dựng sẵn,
// kho tướng (Items/OKho), "Xuất trận!". Mở qua StagePrep.Open / OpenBadge / OpenCave.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class StagePrepDialog : Dialog
    {
        // một ô đội hình: có tướng thì chân dung và tên (chạm để bỏ), trống thì chữ "Trống"
        [Serializable]
        public struct Slot
        {
            public Image bg;
            public ClickCatcher click;
            public HeroPortrait portrait;
            public TextMeshProUGUI name;
            public GameObject empty;
        }

        [Serializable]
        public struct Parts
        {
            public TextMeshProUGUI title, tagText, sub, warnText, hint;
            public GameObject tag, warn;
            public RectTransform foes, rewards, roster;
            public GridLayoutGroup rewardGrid;
            public LayoutElement rewardLayout, rosterLayout;
            public Slot[] slots;
            public SketchButton go;
        }

        [SerializeField] Parts p;
        [SerializeField] PrepFoe foePrefab;
        [SerializeField] PrepRewardChip chipPrefab;
        [SerializeField] PrepRosterCell cellPrefab;

        StageDef st;
        BadgeRef badge;
        CaveRef cave;
        HeroDef leadEnemy;
        List<string> team;

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, PrepFoe foe, PrepRewardChip chip, PrepRosterCell cell)
        {
            p = parts;
            foePrefab = foe;
            chipPrefab = chip;
            cellPrefab = cell;
        }

        public void Show(StageDef stage, BadgeRef badgeRef, CaveRef caveRef)
        {
            st = stage;
            badge = badgeRef;
            cave = caveRef;
            var d = App.Data;
            var s = App.Save.Data;
            team = s.team.Where(t => s.Hero(t)?.owned == true).Take(3).ToList();
            var z = d.Zone(st.zone);
            leadEnemy = d.Hero((st.enemies.FirstOrDefault(e => e.boss) ?? st.enemies[0]).hero);
            int maxLv = st.enemies.Max(e => e.level);

            p.title.text = cave != null ? $"Hang Tiềm Năng · {d.Cfg.cave.tiers[cave.tier].name}" : badge != null ? $"Đền Huy Hiệu · {Elements.Name(z.id)}" : $"{z.name} · Ải {st.idx}";
            p.tag.SetActive(st.kind != StageKind.Normal);
            p.tagText.text = cave != null ? "HANG" : badge != null ? "THỬ THÁCH" : st.kind == StageKind.Boss ? "BOSS ĐẢO" : "MINI BOSS";
            p.sub.text = cave != null ? $"Boss hệ {Elements.Name(cave.zone)} · thắng mới trừ lượt"
                : badge != null ? $"Huy hiệu {Badges.TierName(d.Cfg, badge.tier)} · Trận {badge.i}/{Badges.Count(d.Cfg, badge.tier)}" : st.name;

            p.warn.SetActive(s.level < maxLv - 2);
            p.warnText.text = $"Cảnh báo: địch cấp {maxLv}, bạn mới cấp {s.level}. Đảo này đang quá mạnh, nên nuôi tướng thêm.";

            // đối thủ
            Clear(p.foes);
            for (int i = 0; i < st.enemies.Count; i++)
            {
                var en = st.enemies[i];
                float x = (i - (st.enemies.Count - 1) / 2f) * 280;
                Ui.Spawn(foePrefab, p.foes).Bind(d.Hero(en.hero), en, x);
            }

            Rewards(d, s);
            p.hint.text = $"Mũi tên xanh: khắc {Elements.Name(leadEnemy.elem)} của {leadEnemy.name}. Mũi tên đỏ: bị khắc.";
            p.go.SetOnClick(Go);
            DrawTeam();
        }

        static void Clear(Transform t)
        {
            for (int i = t.childCount - 1; i >= 0; i--) Destroy(t.GetChild(i).gameObject);
        }

        // phần thưởng: ải đảo (bi, mảnh, tướng tặng), Đền Huy Hiệu (bi; trận cuối thêm huy hiệu và rương), Hang (đá tiềm năng)
        void Rewards(GameData d, SaveData s)
        {
            Clear(p.rewards);
            var cfg = d.Cfg;
            p.rewardGrid.spacing = cave != null ? Vector2.zero : new Vector2(16, 12);
            if (badge != null)
            {
                bool last = badge.i == Badges.Count(cfg, badge.tier);
                p.rewardLayout.preferredHeight = last ? 160 : 76;
                Chip(Icon("ball"), null, $"+{cfg.badges.ballsBase + cfg.badges.ballsPerTier * badge.tier} bi", Theme.CardFill);
                if (!last) return;
                Chip(Icon("crown"), null, $"Huy hiệu {Elements.Name(badge.zone)} · {Badges.TierName(cfg, badge.tier)}", Theme.Hex("#fff3c4"));
                Chip(Icon("chest"), null, Pachinko.ChestName(Pachinko.FromKey(cfg.badges.chest[badge.tier - 1])), Theme.CardFill);
                return;
            }
            if (cave != null)
            {
                p.rewardLayout.preferredHeight = 76;
                Chip(Icon("rock"), null, $"+{cfg.cave.tiers[cave.tier].stones} đá tiềm năng", Theme.Hex("#f4efff"));
                return;
            }
            bool first = !Progress.StageCleared(s, st);
            int chips = 1 + st.drops.Count(x => !x.gift || first);
            p.rewardLayout.preferredHeight = chips > 2 ? 160 : 76;
            Chip(Icon("ball"), null, $"+{Progress.StageBalls(d, st, first)} bi{(first ? " (lần đầu)" : "")}", Theme.CardFill);
            foreach (var dr in st.drops)
            {
                if (dr.gift)
                {
                    if (first) Chip(null, d.Hero(dr.hero), $"{d.Hero(dr.hero).name} gia nhập!", Theme.Hex("#fff3c4"));
                    continue;
                }
                double ch = first ? dr.chance : dr.chance * (dr.chance >= 1 ? 0.5 : 0.8);
                Chip(null, d.Hero(dr.hero), $"{dr.min}–{dr.max} mảnh · {CardText.Pct(ch)}", Theme.CardFill);
            }
        }

        void Chip(Sprite icon, HeroDef hero, string text, Color fill) => Ui.Spawn(chipPrefab, p.rewards).Bind(icon, hero, text, fill);

        // đội hình và kho tướng: vẽ lại mỗi lần thêm bỏ tướng
        void DrawTeam()
        {
            var d = App.Data;
            var s = App.Save.Data;
            for (int i = 0; i < p.slots.Length; i++)
            {
                string hid = i < team.Count ? team[i] : null;
                var slot = p.slots[i];
                bool filled = hid != null;
                slot.bg.color = filled ? Theme.Hex("#eaf6df") : Theme.Hex("#f6efdc");
                slot.portrait.gameObject.SetActive(filled);
                slot.name.gameObject.SetActive(filled);
                slot.empty.SetActive(!filled);
                slot.click.enabled = filled;
                int k = i;
                slot.click.OnClick = !filled ? (Action)null : () =>
                {
                    App.Audio.Play("click");
                    team.RemoveAt(k);
                    DrawTeam();
                };
                if (!filled) continue;
                var h = d.Hero(hid);
                slot.portrait.Bind(h, 128);
                slot.name.text = (i == 0 ? "Ra trước · " : "") + h.name;
            }

            // kho tướng đã có: mũi tên xanh khắc tướng chính của địch, đỏ bị khắc
            Clear(p.roster);
            var owned = d.Heroes.Where(h => s.Hero(h.id).owned).ToList();
            p.rosterLayout.preferredHeight = ((owned.Count + 5) / 6) * 176;
            foreach (var h in owned)
            {
                var hero = h;
                double adv = Elements.Mult(h.elem, leadEnemy.elem), bad = Elements.Mult(leadEnemy.elem, h.elem);
                bool khac = adv > 1 || bad > 1;
                Ui.Spawn(cellPrefab, p.roster).Bind(h, team.Contains(h.id), khac, khac ? Icon(adv > 1 ? "up" : "down") : null, () =>
                {
                    App.Audio.Play("click");
                    if (team.Contains(hero.id)) team.Remove(hero.id);
                    else if (team.Count < 3) team.Add(hero.id);
                    else App.Toasts.Show("Đội tối đa 3 tướng", Icon("team"));
                    DrawTeam();
                });
            }
            p.go.Interactable = team.Count > 0;
        }

        void Go()
        {
            if (team.Count == 0) return;
            var s = App.Save.Data;
            s.team = new List<string>(team);
            App.Save.Save();
            Close();
            App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = st.id, team = new List<string>(team), badge = badge, cave = cave });
        }
    }
}
