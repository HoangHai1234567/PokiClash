// Hộp Chuẩn bị trận dùng chung cho ải đảo, Đền Huy Hiệu, Hang Tiềm Năng (prefab Assets/04 Prefabs/Dialogs/ChuanBiTran):
// đầu hộp và nhãn kiểu, cảnh báo quá sức, đối thủ (Items/DoiThu, kèm lực chiến và Máu, Công, Thủ khi vào trận của từng con, chữ to;
// tướng tiến hóa trong trận chỉ hiện dạng đầu, đầu mục ghi luật tiến hóa), dòng so lực chiến địch / đội bạn và mức
// khó, thưởng là ô hình (Items/OThuong: cái gì, bao nhiêu, độ hiếm), 3 ô đội hình dựng sẵn, "Xuất trận!".
// Ải đảo chưa mở cũng mở được để xem địch (chạm chấm hay bệ ải trên màn Đảo): nút Xuất trận khoá, ghi ải cần qua trước.
// Dòng lực chiến, ô thưởng dựng bằng menu "PokiClash/Prefab/Popup gọn (ô thưởng, đội hình, lực chiến)".
// Ô đội mở theo tiến trình (Progress.TeamSlots): ô chưa mở hiện khoá và điều kiện; chạm ô đã mở thì mở bể tướng (TeamPickerDialog,
// prefab Dialogs/ChonDoi) chọn một lần đủ đội. Lưới kho tướng cũ trong hộp (kho, dòng gợi ý) để ẩn. Mở qua StagePrep.Open / OpenBadge / OpenCave.
// Ải đảo đã thắng có nút "AFK ải này" cạnh Xuất trận (menu "PokiClash/Prefab/AFK theo ải"): chọn ải cho đội AFK (Afk.SetStage);
// ải đang AFK do người chơi chọn ghi "Đang AFK", chạm mở hộp AFK.
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
        [SerializeField] PrepRosterCell cellPrefab;
        [SerializeField] TeamPickerDialog pickerPrefab; // menu "Hộp chọn đội (ChonDoi)" gán
        [SerializeField] TextMeshProUGUI teamTitle, teamHint; // đầu mục đội hình
        [SerializeField] RewardTile tilePrefab; // ô thưởng (Items/OThuong)
        [SerializeField] PowerRow power;
        [Tooltip("Nút AFK ải này (menu PokiClash/Prefab/AFK theo ải)")]
        [SerializeField] SketchButton afkBtn;
        [Tooltip("Chữ đầu mục \"Đối thủ\" (menu PokiClash/Prefab/Hộp chuẩn bị: chỉ số địch)")]
        [SerializeField] TextMeshProUGUI foeTitle;

        // dòng so lực chiến: số của địch, số của đội đang chọn, nhãn mức khó (Dễ / Vừa / Khó / Rất khó)
        [Serializable]
        public struct PowerRow
        {
            public GameObject root;
            public TextMeshProUGUI foe, mine, verdict;
            public Image verdictBg;
        }

        StageDef st;
        BadgeRef badge;
        CaveRef cave;
        HeroDef leadEnemy;
        List<string> team;
        bool locked; // ải đảo chưa mở: chỉ xem
        int foePower;

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, PrepFoe foe, RewardTile tile, PrepRosterCell cell)
        {
            p = parts;
            foePrefab = foe;
            tilePrefab = tile;
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
            locked = badge == null && cave == null && !Progress.StageOpen(s, st);

            p.title.text = cave != null ? $"Hang Tiềm Năng · {d.Cfg.cave.tiers[cave.tier].name}" : badge != null ? $"Đền Huy Hiệu · {Elements.Name(z.id)}" : $"{z.name} · Ải {st.idx}";
            // nhãn: boss, mini boss; đảo 70 ải còn ghi kiểu ải (Tướng mới, Bầy lính, Cửa ải…)
            p.tag.SetActive(st.kind != StageKind.Normal || st.tag != StageTag.None);
            p.tagText.text = cave != null ? "HANG" : badge != null ? "THỬ THÁCH" : st.kind == StageKind.Boss ? "BOSS ĐẢO" : st.kind == StageKind.Mini ? "MINI BOSS"
                : ZoneChapterRow.TagText(st).ToUpperInvariant();
            // ải 1 mỗi đảo là tướng khởi đầu cùng hệ: trùng tướng người chơi đã chọn thì đấu với bóng của nó (15_TuongKhoiDau.md)
            bool mirror = cave == null && badge == null && st.idx == 1 && st.enemies.Count == 1 && st.enemies[0].hero == s.starter;
            string mirrorName = mirror ? d.Hero(st.enemies[0].hero).name : null;
            p.sub.text = cave != null ? $"Boss hệ {Elements.Name(cave.zone)} · thắng mới trừ lượt"
                : badge != null ? $"Huy hiệu {Badges.TierName(d.Cfg, badge.tier)} · Trận {badge.i}/{Badges.Count(d.Cfg, badge.tier)}"
                : mirror ? st.zone == Elem.Thuy ? $"{st.name} · Mặt nước in bóng {mirrorName} của bạn!" : $"{st.name} · Bóng của {mirrorName} chặn đường!"
                : st.name;

            p.warn.SetActive(!locked && s.level < maxLv - 2);
            p.warnText.text = $"Địch cấp {maxLv}, bạn cấp {s.level}: nên nuôi tướng thêm";

            // đối thủ, mỗi con kèm chỉ số khi vào trận; tướng tiến hóa trong trận (ải tướng, boss) chỉ hiện dạng đầu, lực chiến tính cả
            // dòng (như số "Địch" ở dòng lực chiến)
            Clear(p.foes);
            var enemy = Teams.Enemy(st, d);
            foePower = TeamPower.Of(d.Cfg, d, enemy);
            var evo = st.enemies.Any(e => e.evo && d.Hero(e.hero).forms.Length > 1);
            var foes = enemy.members;
            for (int i = 0; i < st.enemies.Count; i++)
            {
                var en = st.enemies[i];
                float x = (i - (st.enemies.Count - 1) / 2f) * 280;
                var h = d.Hero(en.hero);
                Ui.Spawn(foePrefab, p.foes).Bind(h, en, x, HeroStats.InBattle(d.Cfg, h, foes[i]), HeroStats.Power(d.Cfg, h, foes[i]));
            }
            // đầu mục đối thủ: luật tiến hóa (thẻ boss_evo) khi địch tiến hóa trong trận
            if (foeTitle)
            {
                var ec = d.Card(Battle.BossEvoCard);
                double heal = ec.Effects.Count > 0 && ec.Effects[0].K == EffectKind.Evolve ? ec.Effects[0].Pct : 1;
                foeTitle.text = evo ? $"Đối thủ · còn {CardText.Pct(ec.below)} máu thì tiến hóa, hồi {(heal >= 1 ? "đầy" : CardText.Pct(heal))} máu"
                    : "Đối thủ";
            }

            Rewards(d, s);
            p.hint.text = $"Mũi tên xanh: khắc {Elements.Name(leadEnemy.elem)} của {leadEnemy.name}. Mũi tên đỏ: bị khắc.";
            p.go.SetOnClick(Go);
            if (afkBtn) afkBtn.SetOnClick(PickAfk);
            DrawTeam();
            ShowAfk();
        }

        // nút AFK: chỉ ải đảo đã thắng; ải người chơi đã chọn cho đội AFK ghi "Đang AFK"
        void ShowAfk()
        {
            if (!afkBtn) return;
            var s = App.Save.Data;
            bool can = badge == null && cave == null && Progress.StageCleared(s, st);
            afkBtn.gameObject.SetActive(can);
            if (!can) return;
            bool on = Afk.Picked(s, st);
            afkBtn.SetText(on ? "Đang AFK" : "AFK ải này");
            afkBtn.SetRole(on ? BtnColor.Paper : BtnColor.Blue);
        }

        // chọn ải này cho đội AFK; mảnh các giờ tròn đã dồn ở ải cũ nhận luôn. Ải đang AFK thì mở hộp AFK.
        void PickAfk()
        {
            var d = App.Data;
            var s = App.Save.Data;
            if (Afk.Picked(s, st))
            {
                AfkPanel.Open();
                return;
            }
            var r = Afk.SetStage(s, d, st.id, PokiClash.Game.SaveService.Now(), new Rng(Rng.RandomSeed()));
            if (r == null) return;
            App.Save.Save();
            App.Audio.Play("coin");
            var pool = Afk.Pool(st);
            App.Toasts.Show(pool.Count > 0 ? $"Đội AFK ải {st.idx}: rơi mảnh {string.Join(", ", pool.Select(x => d.Hero(x.hero).name))}" : $"Đội AFK ải {st.idx}: ải này chỉ ra rương AFK", Icon("clock"));
            int n = r.shards.Sum(x => x.n);
            if (n > 0) App.Toasts.Show($"Ải cũ: nhặt {n} mảnh tướng", Icon("shard"));
            foreach (var x in r.shards)
                if (x.unlocked) App.Toasts.Show($"Mở khóa {d.Hero(x.hero).name}!", Icon("star"));
            ShowAfk();
            if (App.Router.CurrentRoot is ZoneScene zs) zs.PlaceAfkTag();
        }

        static void Clear(Transform t)
        {
            for (int i = t.childCount - 1; i >= 0; i--) Destroy(t.GetChild(i).gameObject);
        }

        // phần thưởng (ô hình): ải đảo (bi, mảnh kèm tỉ lệ, tướng tặng), Đền Huy Hiệu (bi; trận cuối thêm huy hiệu và rương),
        // Hang (đá tiềm năng)
        void Rewards(GameData d, SaveData s)
        {
            Clear(p.rewards);
            var cfg = d.Cfg;
            int n = 0;
            if (badge != null)
            {
                n++;
                Tile().Item(Icon("ball"), $"×{cfg.badges.ballsBase + cfg.badges.ballsPerTier * badge.tier}", "Bi");
                if (badge.i == Badges.Count(cfg, badge.tier))
                {
                    n += 2;
                    var chest = Pachinko.FromKey(cfg.badges.chest[badge.tier - 1]);
                    Tile().Item(Icon("crown"), "", $"Huy hiệu {Badges.TierName(cfg, badge.tier)}", Rarity.Epic, Theme.Of(badge.zone));
                    Tile().Item(Icon("chest"), "×1", Pachinko.ChestName(chest), ChestRarity(chest));
                }
            }
            else if (cave != null)
            {
                n++;
                Tile().Item(Icon("rock"), $"×{cfg.cave.tiers[cave.tier].stones}", "Đá tiềm năng", Rarity.Epic);
            }
            else
            {
                bool first = !Progress.StageCleared(s, st);
                n++;
                var balls = Tile().Item(Icon("ball"), $"×{Progress.StageBalls(d, st, first)}", "Bi");
                if (first) balls.Tag("Lần đầu", Theme.Yellow);
                foreach (var dr in st.drops)
                {
                    var h = d.Hero(dr.HeroFor(s));
                    if (dr.gift)
                    {
                        if (!first) continue;
                        n++;
                        Tile().Hero(h, "", false).Tag("MỚI!", Theme.Red);
                        continue;
                    }
                    n++;
                    double ch = first ? dr.chance : dr.chance * (dr.chance >= 1 ? 0.5 : 0.8);
                    Tile().Hero(h, dr.min == dr.max ? $"×{dr.min}" : $"×{dr.min}–{dr.max}").Tag(ch < 1 ? CardText.Pct(ch) : "", Theme.Paper2);
                }
            }
            // ô cỡ RewardTile, một hàng tới 5 ô (đếm n vì Destroy của Clear chưa xong trong khung này)
            int perRow = Mathf.Min(5, Mathf.Max(1, n)), rows = (n + perRow - 1) / perRow;
            p.rewardGrid.cellSize = new Vector2(RewardTile.W, RewardTile.H);
            p.rewardGrid.spacing = new Vector2(18, 28); // chừa chỗ nhãn ô hàng dưới
            p.rewardGrid.constraintCount = perRow;
            p.rewardGrid.childAlignment = TextAnchor.UpperCenter;
            p.rewardLayout.preferredHeight = rows * RewardTile.H + (rows - 1) * 28 + 16;
        }

        RewardTile Tile() => Ui.Spawn(tilePrefab, p.rewards);

        public static Rarity ChestRarity(SlotKind k) => k == SlotKind.ChestGold ? Rarity.Legend : k == SlotKind.ChestSilver ? Rarity.Rare : Rarity.Common;

        // lực chiến đội đang chọn so với địch: nhãn mức khó theo tỉ lệ
        void ShowPower()
        {
            if (!power.root) return;
            var d = App.Data;
            int mine = TeamPower.Of(d.Cfg, d, Teams.Player(App.Save.Data, team, d));
            power.foe.text = TeamPower.Text(foePower);
            power.mine.text = TeamPower.Text(mine);
            double r = foePower > 0 ? mine / (double)foePower : 9;
            var (label, color) = r >= 1.25 ? ("Dễ", Theme.Green) : r >= 0.95 ? ("Vừa", Theme.Yellow) : r >= 0.75 ? ("Khó", Theme.Orange) : ("Rất khó", Theme.Red);
            power.verdict.text = label;
            power.verdictBg.color = color;
            power.mine.color = r >= 0.95 ? Theme.GreenD : Theme.RedD;
        }

        // đội hình: ô đã mở chạm để mở bể tướng, ô khoá ghi điều kiện mở
        void DrawTeam()
        {
            var d = App.Data;
            var s = App.Save.Data;
            int open = Progress.TeamSlots(s);
            if (teamTitle) teamTitle.text = $"Đội của bạn ({open}/{p.slots.Length})";
            if (teamHint) teamHint.text = "chạm ô để đổi";
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
                if (emptyText) emptyText.text = locked ? $"Khoá\n<size=70%>{Progress.SlotNeed(i)}</size>" : "Trống\n<size=70%>chạm để chọn</size>";
                slot.click.enabled = true;
                int k = i;
                slot.click.OnClick = () =>
                {
                    if (k >= Progress.TeamSlots(App.Save.Data))
                    {
                        App.Audio.Play("error");
                        App.Toasts.Show($"Ô đội {k + 1} mở khi {Progress.SlotNeed(k)}", Icon("lock"));
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
            p.go.SetText(locked ? "Chưa mở" : "Xuất trận!");
            p.go.Interactable = team.Count > 0 && !locked;
            ShowPower();
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
            if (team.Count == 0 || locked) return;
            var s = App.Save.Data;
            s.team = new List<string>(team);
            App.Save.Save();
            Close();
            App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = st.id, team = new List<string>(team), badge = badge, cave = cave });
        }
    }
}
