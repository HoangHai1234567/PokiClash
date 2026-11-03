// Hộp Chuẩn bị trận dùng chung cho ải đảo, Đền Huy Hiệu, Hang Tiềm Năng (prefab Assets/04 Prefabs/Dialogs/ChuanBiTran):
// đầu hộp và nhãn kiểu, cảnh báo quá sức, đối thủ (Items/DoiThu), thưởng (Items/ThuongTran), 3 ô đội hình dựng sẵn, "Xuất trận!".
// Ô đội mở theo tiến trình (Progress.TeamSlots): ô chưa mở hiện khoá và điều kiện; chạm ô đã mở thì mở bể tướng (TeamPickerDialog,
// prefab Dialogs/ChonDoi) chọn một lần đủ đội. Lưới kho tướng cũ trong hộp (kho, dòng gợi ý) để ẩn. Mở qua StagePrep.Open / OpenBadge / OpenCave.
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
        // một ô đội hình: có tướng thì chân dung và tên, trống thì chữ "Trống" (chữ trong empty cũng ghi điều kiện mở ô khoá)
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
        [SerializeField] TeamPickerDialog pickerPrefab; // menu "Hộp chọn đội (ChonDoi)" gán
        [SerializeField] TextMeshProUGUI teamTitle, teamHint; // đầu mục đội hình

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
            team = s.team.Where(t => s.Hero(t)?.owned == true).Take(Progress.TeamSlots(s)).ToList();
            var z = d.Zone(st.zone);
            leadEnemy = d.Hero((st.enemies.FirstOrDefault(e => e.boss) ?? st.enemies[0]).hero);
            int maxLv = st.enemies.Max(e => e.level);

            p.title.text = cave != null ? $"Hang Tiềm Năng · {d.Cfg.cave.tiers[cave.tier].name}" : badge != null ? $"Đền Huy Hiệu · {Elements.Name(z.id)}" : $"{z.name} · Ải {st.idx}";
            // nhãn: boss, mini boss; đảo 70 ải còn ghi kiểu ải (Tướng mới, Bầy lính, Cửa ải…)
            p.tag.SetActive(st.kind != StageKind.Normal || st.tag != StageTag.None);
            p.tagText.text = cave != null ? "HANG" : badge != null ? "THỬ THÁCH" : st.kind == StageKind.Boss ? "BOSS ĐẢO" : st.kind == StageKind.Mini ? "MINI BOSS"
                : ZoneChapterRow.TagText(st).ToUpperInvariant();
            // ải 1 của đảo 70 ải: đấu với bóng của tướng khởi đầu
            bool mirror = st.tag == StageTag.Hero && d.Starters.Contains(st.enemies[0].hero);
            p.sub.text = cave != null ? $"Boss hệ {Elements.Name(cave.zone)} · thắng mới trừ lượt"
                : badge != null ? $"Huy hiệu {Badges.TierName(d.Cfg, badge.tier)} · Trận {badge.i}/{Badges.Count(d.Cfg, badge.tier)}"
                : mirror ? $"{st.name} · Mặt nước in bóng {d.Hero(st.enemies[0].hero).name} của bạn!" : st.name;

            p.warn.SetActive(s.level < maxLv - 2);
            p.warnText.text = $"Cảnh báo: địch cấp {maxLv}, bạn mới cấp {s.level}. Đảo này đang quá mạnh, nên nuôi tướng thêm.";

            // đối thủ; boss tiến hóa (ải 8) đứng một mình nên hiện cả dòng dạng, dạng đầu bên trái
            Clear(p.foes);
            var evo = st.enemies.Count == 1 && st.enemies[0].evo && d.Hero(st.enemies[0].hero).forms.Length > 1 ? st.enemies[0] : null;
            if (evo != null)
            {
                var h = d.Hero(evo.hero);
                for (int i = 0; i < h.forms.Length; i++)
                    Ui.Spawn(foePrefab, p.foes).BindForm(h, evo, i, (i - (h.forms.Length - 1) / 2f) * 280, d.Cfg);
            }
            else
            {
                var foes = Teams.Enemy(st, d).members;
                for (int i = 0; i < st.enemies.Count; i++)
                {
                    var en = st.enemies[i];
                    float x = (i - (st.enemies.Count - 1) / 2f) * 280;
                    Ui.Spawn(foePrefab, p.foes).Bind(d.Hero(en.hero), en, x, foes[i].mods);
                }
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

        // đội hình: ô đã mở chạm để mở bể tướng, ô khoá ghi điều kiện mở
        void DrawTeam()
        {
            var d = App.Data;
            var s = App.Save.Data;
            int open = Progress.TeamSlots(s);
            if (teamTitle) teamTitle.text = $"Đội của bạn ({open}/{p.slots.Length} ô, tướng đầu ra trước)";
            if (teamHint) teamHint.text = "chạm ô để chọn tướng";
            for (int i = 0; i < p.slots.Length; i++)
            {
                string hid = i < team.Count ? team[i] : null;
                var slot = p.slots[i];
                bool locked = i >= open, filled = hid != null && !locked;
                slot.bg.color = locked ? Theme.Hex("#e2dccd") : filled ? Theme.Hex("#eaf6df") : Theme.Hex("#f6efdc");
                slot.portrait.gameObject.SetActive(filled);
                slot.name.gameObject.SetActive(filled);
                slot.empty.SetActive(!filled);
                var emptyText = slot.empty.GetComponentInChildren<TextMeshProUGUI>(true);
                int need = i < Progress.TeamSlotZones.Length ? Progress.TeamSlotZones[i] : 0;
                if (emptyText) emptyText.text = locked ? $"Khoá\n<size=70%>xong {need} đảo</size>" : "Trống\n<size=70%>chạm để chọn</size>";
                slot.click.enabled = true;
                int k = i;
                slot.click.OnClick = () =>
                {
                    if (k >= Progress.TeamSlots(App.Save.Data))
                    {
                        App.Audio.Play("error");
                        App.Toasts.Show($"Ô đội {k + 1} mở khi xong {need} đảo", Icon("lock"));
                        return;
                    }
                    App.Audio.Play("click");
                    OpenPicker();
                };
                if (!filled) continue;
                var h = d.Hero(hid);
                slot.portrait.Bind(h, 165);
                slot.name.text = (i == 0 ? "Ra trước · " : "") + h.name;
            }

            // lưới kho tướng cũ trong hộp: thay bằng bể tướng
            p.roster.gameObject.SetActive(false);
            p.hint.gameObject.SetActive(false);
            p.go.Interactable = team.Count > 0;
        }

        // bể tướng: chọn một lần đủ đội, xong thì vẽ lại ô đội
        void OpenPicker()
        {
            var s = App.Save.Data;
            App.Modals.Open(pickerPrefab).Show(team, Progress.TeamSlots(s), leadEnemy, picked =>
            {
                team = picked;
                DrawTeam();
            });
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
