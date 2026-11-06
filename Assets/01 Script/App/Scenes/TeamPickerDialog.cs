// Hộp chọn đội (prefab Assets/04 Prefabs/Dialogs/ChonDoi, biến thể tờ giấy gốc HopThoai, dựng bằng menu
// "PokiClash/Prefab/Hộp chọn đội (ChonDoi)", ô tướng và khung cuộn ở menu "PokiClash/Prefab/Hộp chọn đội: ô tướng, khung cuộn"):
// mở khi chạm ô đội trong hộp Chuẩn bị trận hoặc nút Đổi đội ở màn Tướng.
// Kho tướng đã có (Items/OChonDoi: dải hệ, chân dung, sao, tên, lực chiến) trong khung cuộn 5 cột: tiêu đề, dòng gợi ý và nút "Xong" luôn
// trên màn dù có bao nhiêu tướng. Xếp một lần lúc mở: tướng đang trong đội trước (theo thứ tự ra trận), rồi lực chiến giảm dần; chạm không
// xếp lại (ô không chạy dưới ngón tay). Chạm để chọn hoặc bỏ, tròn xanh góc ô là thứ tự ra trận; mới mở một ô đội thì chạm tướng khác là
// đổi luôn. Mũi tên khắc hệ theo tướng chính của địch; dòng cuối báo ô đội nào còn khoá. "Xong" trả đội về.
// Hàng lọc trên lưới (menu "PokiClash/Prefab/Hộp chọn đội: lọc theo hệ, xếp"; người dùng nhờ 2026-11-06): nút tròn Tất cả, 5 hệ,
// Khắc (chỉ tướng khắc tướng chính của địch, ẩn khi không có địch) và nút xếp đổi vòng Lực chiến → Sao → Hệ. Tướng đang trong đội
// luôn đứng đầu và luôn hiện. Chọn lọc/xếp thì ô xếp lại và nảy ra; lựa chọn giữ cho lần mở sau trong phiên chơi.
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
    public sealed class TeamPickerDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI title, hint;
        [SerializeField] RectTransform grid;
        [SerializeField] LayoutElement gridLayout;
        [SerializeField] SketchButton done;
        [SerializeField] PrepRosterCell cellPrefab;
        [Tooltip("Khung cuộn quanh lưới (menu Hộp chọn đội: ô tướng, khung cuộn); trống thì lưới giãn theo số tướng như cũ")]
        [SerializeField] ScrollRect scroll;

        [Header("Lọc và xếp (menu Hộp chọn đội: lọc theo hệ, xếp)")]
        [SerializeField] LayoutElement filterRow;
        [SerializeField] SketchButton filterAll, filterCounter, sortButton;
        [SerializeField] SketchButton[] filterElems = new SketchButton[0]; // theo FilterOrder
        [SerializeField] Image[] filterIcons = new Image[0]; // icon trên nút hệ (mờ khi không chọn)

        public static readonly Elem[] FilterOrder = { Elem.Thuy, Elem.Hoa, Elem.Kim, Elem.Moc, Elem.Tho };
        enum SortBy { Power, Star, Elem }
        static readonly string[] SortNames = { "Xếp: lực chiến", "Xếp: sao", "Xếp: hệ" };
        // giữ giữa các lần mở trong phiên chơi
        static int filter = -1; // -1: mọi hệ, còn lại: chỉ số trong FilterOrder
        static bool counterOnly;
        static SortBy sort = SortBy.Power;
        readonly Dictionary<string, int> power = new Dictionary<string, int>();

        // phần tờ giấy ngoài khung cuộn (lề, tiêu đề, gợi ý, hàng nút, khe) và lề trên dưới của màn, để khung cuộn cao vừa màn
        const float SheetRest = 420, ScreenMargin = 260;

        List<string> team;
        int slots;
        HeroDef foe;
        readonly List<(PrepRosterCell cell, HeroDef hero)> cells = new List<(PrepRosterCell, HeroDef)>();

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, TextMeshProUGUI hintText, RectTransform gridRt, LayoutElement gridLe, SketchButton doneBtn,
            PrepRosterCell cell)
        {
            title = titleText;
            hint = hintText;
            grid = gridRt;
            gridLayout = gridLe;
            done = doneBtn;
            cellPrefab = cell;
        }

        // Dùng khi dựng khung cuộn (Editor): lưới nằm trong scroll, gridLe là LayoutElement của khung cuộn.
        public void SetupScroll(ScrollRect scrollRect, RectTransform gridRt, LayoutElement viewLe, PrepRosterCell cell)
        {
            scroll = scrollRect;
            grid = gridRt;
            gridLayout = viewLe;
            cellPrefab = cell;
        }

        // current: đội đang chọn; slotCount: số ô đã mở; leadEnemy: tướng chính của địch (mũi tên khắc hệ, có thể null)
        public void Show(List<string> current, int slotCount, HeroDef leadEnemy, Action<List<string>> onDone)
        {
            slots = slotCount;
            team = current.Take(slots).ToList();
            foe = leadEnemy;
            var locked = Enumerable.Range(slots, Progress.TeamSlotMax - slots)
                .Select(i => $"ô {i + 1} mở khi {Progress.SlotNeed(i)}").ToList();
            hint.text = (foe != null ? $"Mũi tên xanh: khắc {Elements.Name(foe.elem)} của {foe.name}. Mũi tên đỏ: bị khắc." : "")
                        + (locked.Count > 0 ? $"\nĐang mở {slots}/{Progress.TeamSlotMax} ô đội; {string.Join(", ", locked)}." : "");
            done.SetOnClick(() =>
            {
                if (team.Count == 0) return;
                onDone?.Invoke(new List<string>(team));
                Close();
            });
            WireFilters();
            Build();
            Draw();
        }

        // Dùng khi dựng hàng lọc (Editor).
        public void SetupFilters(LayoutElement row, SketchButton all, SketchButton[] elems, Image[] icons, SketchButton counter, SketchButton sortBtn)
        {
            filterRow = row;
            filterAll = all;
            filterElems = elems;
            filterIcons = icons;
            filterCounter = counter;
            sortButton = sortBtn;
        }

        void WireFilters()
        {
            if (!filterRow) return;
            if (foe == null) counterOnly = false;
            if (filterCounter) filterCounter.gameObject.SetActive(foe != null);
            filterAll.SetOnClick(() => SetFilter(-1, counterOnly));
            for (int i = 0; i < filterElems.Length; i++)
            {
                int k = i;
                filterElems[i].SetOnClick(() => SetFilter(filter == k ? -1 : k, counterOnly));
            }
            if (filterCounter) filterCounter.SetOnClick(() => SetFilter(filter, !counterOnly));
            sortButton.SetOnClick(() =>
            {
                sort = (SortBy)(((int)sort + 1) % SortNames.Length);
                Arrange(true);
            });
        }

        void SetFilter(int f, bool counter)
        {
            filter = f;
            counterOnly = counter && foe != null;
            Arrange(true);
        }

        // tướng khắc tướng chính của địch (như mũi tên xanh trên ô)
        bool Counters(HeroDef h) =>
            foe != null && Elements.Mult(h.elem, foe.elem, h.id == App.Save.Data.starter, false) > 1;

        // xếp lại và lọc ô theo lựa chọn; tướng trong đội luôn đầu và luôn hiện. pop: ô hiện ra nảy lần lượt
        void Arrange(bool pop)
        {
            var s = App.Save.Data;
            var ordered = cells
                .OrderBy(c => team.Contains(c.hero.id) ? team.IndexOf(c.hero.id) : int.MaxValue)
                .ThenBy(c => sort == SortBy.Elem ? Array.IndexOf(FilterOrder, c.hero.elem) : 0)
                .ThenByDescending(c => sort == SortBy.Star ? s.Hero(c.hero.id).star : 0)
                .ThenByDescending(c => power.TryGetValue(c.hero.id, out var pw) ? pw : 0)
                .ToList();
            int shown = 0;
            for (int i = 0; i < ordered.Count; i++)
            {
                var (cell, h) = ordered[i];
                cell.transform.SetSiblingIndex(i);
                bool inTeam = team.Contains(h.id);
                bool visible = inTeam || ((filter < 0 || h.elem == FilterOrder[filter]) && (!counterOnly || Counters(h)));
                cell.gameObject.SetActive(visible);
                if (!visible) continue;
                if (pop && shown < 20) UiMotion.Of(cell).Spawn(shown * 0.025f);
                shown++;
            }
            Size(shown);
            PaintFilters();
        }

        // nút đang chọn tô màu (hệ: màu hệ; Tất cả: vàng; Khắc: xanh lá), còn lại màu giấy, icon hệ mờ
        void PaintFilters()
        {
            if (!filterRow) return;
            filterAll.SetColor(filter < 0 ? Theme.Yellow : Theme.Paper3);
            for (int i = 0; i < filterElems.Length && i < FilterOrder.Length; i++)
            {
                bool on = filter == i;
                filterElems[i].SetColor(on ? Theme.Of(FilterOrder[i]) : Theme.Paper2);
                if (i < filterIcons.Length && filterIcons[i]) filterIcons[i].color = new Color(1, 1, 1, on || filter < 0 ? 1 : 0.45f);
            }
            if (filterCounter) filterCounter.SetColor(counterOnly ? Theme.Green : Theme.Paper3);
            sortButton.SetText(SortNames[(int)sort]);
            sortButton.FitWidth();
        }

        // dựng ô một lần: đội trước, rồi lực chiến giảm dần
        void Build()
        {
            var d = App.Data;
            var s = App.Save.Data;
            for (int i = grid.childCount - 1; i >= 0; i--) Destroy(grid.GetChild(i).gameObject);
            cells.Clear();
            power.Clear();
            foreach (var h in d.Heroes.Where(h => s.Hero(h.id).owned)) power[h.id] = HeroStats.Power(d.Cfg, h, Teams.MemberOf(s, h.id, d));
            var owned = d.Heroes.Where(h => power.ContainsKey(h.id))
                .OrderBy(h => team.Contains(h.id) ? team.IndexOf(h.id) : int.MaxValue)
                .ThenByDescending(h => power[h.id]).ToList();
            foreach (var h in owned)
            {
                var cell = Ui.Spawn(cellPrefab, grid);
                cell.SetStats(s.Hero(h.id).star, d.Cfg.maxStar, power[h.id]);
                cells.Add((cell, h));
            }
            if (filterRow) Arrange(false);
            else Size(owned.Count);
        }

        // cao lưới theo số hàng; có khung cuộn thì khung cao vừa màn, lưới cuộn trong khung
        void Size(int n)
        {
            var g = grid.GetComponent<GridLayoutGroup>();
            int cols = g && g.constraint == GridLayoutGroup.Constraint.FixedColumnCount ? g.constraintCount : 6;
            float cellH = g ? g.cellSize.y : 160, gap = g ? g.spacing.y : 16;
            int rows = Mathf.Max(1, (n + cols - 1) / cols);
            float pad = g ? g.padding.top + g.padding.bottom : 0;
            float h = rows * cellH + (rows - 1) * gap + pad;
            if (!scroll)
            {
                gridLayout.preferredHeight = h;
                return;
            }
            grid.sizeDelta = new Vector2(grid.sizeDelta.x, h);
            float screen = ((RectTransform)transform).rect.height;
            if (screen < 1000) screen = PokiCanvas.RefH;
            // ít nhất 2 hàng rưỡi kể cả màn thấp
            float rest = SheetRest + (filterRow && filterRow.gameObject.activeSelf ? filterRow.preferredHeight + 16 : 0);
            float max = Mathf.Max(2.5f * (cellH + gap), screen - rest - ScreenMargin);
            gridLayout.preferredHeight = Mathf.Min(h, max);
            scroll.verticalNormalizedPosition = 1;
        }

        void Draw()
        {
            title.text = $"Chọn đội · {team.Count}/{slots}";
            foreach (var (cell, h) in cells)
            {
                var hero = h;
                bool partner = h.id == App.Save.Data.starter;
                double adv = foe != null ? Elements.Mult(h.elem, foe.elem, partner, false) : 1,
                    bad = foe != null ? Elements.Mult(foe.elem, h.elem, false, partner) : 1;
                bool khac = adv > 1 || bad > 1;
                int order = team.IndexOf(h.id) + 1;
                cell.Bind(h, order > 0, khac, khac ? Icon(adv > 1 ? "up" : "down") : null, () => Tap(hero), order);
            }
            done.Interactable = team.Count > 0;
        }

        void Tap(HeroDef hero)
        {
            App.Audio.Play("click");
            if (team.Contains(hero.id)) team.Remove(hero.id);
            else if (team.Count < slots) team.Add(hero.id);
            else if (slots == 1) team[0] = hero.id; // một ô: đổi luôn
            else
            {
                App.Toasts.Show(slots < Progress.TeamSlotMax ? $"Đang mở {slots} ô đội: ô {slots + 1} mở khi {Progress.SlotNeed(slots)}" : $"Đội tối đa {slots} tướng",
                    Icon("team"));
                return;
            }
            Draw();
        }
    }
}
