// Tướng (chép heroesScreen của Web/src/view/screens/heroes.ts): trên là đội hình (TeamLineup: 3 tướng trong đội, vuốt ngang),
// dưới là lưới 3 cột thẻ tướng: chỉ tướng đã có (xếp trước) và tướng chưa mở mà đã có mảnh (bóng sẫm, thanh mảnh, xếp sau); tướng chưa
// có mảnh nào thì ẩn (người dùng dặn 2026-11-03). Mỗi thẻ là một bản sao prefab Items/TheTuong (HeroTile).
// Chạm thẻ mở hộp chi tiết. Prefab màn hình Assets/04 Prefabs/Screens/Heroes.
// Làm mới (lên cấp, tiến hóa, đổi đội: mỗi lần lưu gọi Refresh, hộp chi tiết gọi thêm lần nữa) giữ các ô đã dựng và gán lại dữ liệu,
// chỉ dựng thêm ô khi lưới dài ra: phá đi dựng lại cả lưới mỗi lần bấm làm máy giật (người dùng báo 2026-11-07).
// Lọc và xếp (người dùng dặn 2026-11-17; hàng "loc_xep" giữa đội hình và lưới, menu "PokiClash/Prefab/Hộp thoại và màn/Màn Tướng: độ hiếm, lọc và xếp"):
// - nút tròn Tất cả và 5 hệ (Thủy, Hỏa, Kim, Mộc, Thổ; chạm lại hệ đang chọn là về Tất cả);
// - nút viên xếp đổi vòng Lực chiến (mặc định) → Độ hiếm → Sao (sao tổng 1..20) → Cấp thẻ (tổng cấp 3 thẻ) → Hệ; trùng thì lực chiến;
// - nút tròn mũi tên đảo chiều giảm / tăng dần.
// Tướng đã có luôn đứng trước tướng chưa có. Tướng chưa có xếp theo độ hiếm / hệ nếu đang xếp theo đó, không thì theo phần mảnh đã gom.
// Lựa chọn nhớ giữa các lần mở (PlayerPrefs "heroes.sort", "heroes.desc", "heroes.filter"; đọc ghi bọc try/catch). Đổi lọc, xếp thì
// lưới cuộn về đầu, ô nảy ra lần lượt. Prefab chưa chạy menu (không có nút) thì lưới như cũ: mọi hệ, lực chiến giảm dần.
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
    public sealed class HeroesScene : SceneRoot
    {
        public override string Title => Loc.T("Tướng");

        [SerializeField] RectTransform grid;
        [SerializeField] HeroTile tilePrefab;
        [SerializeField] TeamLineup lineup;

        [Header("Lọc và xếp (menu Màn Tướng: độ hiếm, lọc và xếp)")]
        [SerializeField] SketchButton filterAll;
        [SerializeField] SketchButton[] filterElems = new SketchButton[0]; // theo TeamPickerDialog.FilterOrder
        [SerializeField] Image[] filterIcons = new Image[0]; // icon trên nút hệ (mờ khi không chọn)
        [SerializeField] SketchButton sortButton, dirButton;
        [SerializeField] Image dirIcon; // mũi tên xuống: giảm dần, lên: tăng dần
        [SerializeField] TextMeshProUGUI emptyText; // lọc hệ chưa có tướng nào

        public enum SortKey { Power, Rarity, Star, CardLevel, Elem }
        public static readonly string[] SortNames = { "Xếp: lực chiến", "Xếp: độ hiếm", "Xếp: sao", "Xếp: cấp thẻ", "Xếp: hệ" };
        static Elem[] FilterOrder => TeamPickerDialog.FilterOrder;
        const string PrefSort = "heroes.sort", PrefDesc = "heroes.desc", PrefFilter = "heroes.filter";
        static bool prefsLoaded;
        static SortKey sort = SortKey.Power;
        static bool desc = true;
        static int filter = -1; // -1: mọi hệ, còn lại: chỉ số trong FilterOrder

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform gridRt, HeroTile tile)
        {
            grid = gridRt;
            tilePrefab = tile;
        }

        // Dùng khi dựng hàng lọc, xếp (Editor).
        public void SetupFilters(SketchButton all, SketchButton[] elems, Image[] icons, SketchButton sortBtn, SketchButton dirBtn, Image dirImg,
            TextMeshProUGUI empty)
        {
            filterAll = all;
            filterElems = elems;
            filterIcons = icons;
            sortButton = sortBtn;
            dirButton = dirBtn;
            dirIcon = dirImg;
            emptyText = empty;
        }

        bool popIn; // ô tướng nảy ra lần lượt (vào màn, đổi lọc / xếp; làm mới sau đó thì không)
        float popFirst, popStep; // trễ ô đầu, trễ thêm mỗi ô
        readonly List<HeroTile> tiles = new List<HeroTile>(); // ô đã dựng, theo thứ tự trong lưới

        // prefab chưa có hàng lọc: không lọc, không đảo chiều (lựa chọn cũ trong PlayerPrefs không được làm mất tướng mà không có nút gỡ)
        bool HasFilters => sortButton;

        public override void Enter(object args)
        {
            LoadPrefs();
            WireFilters();
            popIn = true;
            popFirst = 0.12f;
            popStep = 0.04f;
            if (lineup) lineup.Bind(RenderGrid);
            RenderGrid();
            popIn = false;
        }

        public override void Refresh()
        {
            if (lineup) lineup.Bind(RenderGrid);
            RenderGrid();
        }

        void RenderGrid()
        {
            if (!grid) return;
            // lần đầu: bỏ ô mẫu còn trong prefab
            if (tiles.Count == 0)
                for (int i = grid.childCount - 1; i >= 0; i--) Destroy(grid.GetChild(i).gameObject);
            var d = App.Data;
            var s = App.Save.Data;
            // hướng dẫn C9 còn chờ: bỏ lọc hệ để ô tướng đồng hành chắc chắn hiện (lọc cũ nhớ trong PlayerPrefs có thể giấu nó, tour
            // thử 2026-11-23 kẹt ở màn này vì lọc Kim còn sót)
            if (HasFilters && filter >= 0 && !string.IsNullOrEmpty(s.starter) && !Tutorial.Done(s, Tutorial.UpCard) &&
                Progress.CanUpCard(s, d.Cfg, s.starter, CardSlot.Skill))
                filter = -1;
            var list = HasFilters ? Sorted(d, s, filter, sort, desc) : Sorted(d, s, -1, SortKey.Power, true);
            for (int i = 0; i < list.Count; i++)
            {
                string id = list[i].id;
                HeroTile tile;
                if (i < tiles.Count) tile = tiles[i];
                else
                {
                    tile = Ui.Spawn(tilePrefab, grid);
                    tiles.Add(tile);
                    // bộ UI Sa Bàn: ô tướng nhún nhẹ tại chỗ; lúc vào màn thì nảy ra lần lượt từ dưới lên
                    var mo = PokiClash.UI.UiMotion.Of(tile);
                    mo.idleLift = 4;
                    mo.idleTilt = 0.4f;
                    mo.idlePeriod = 3.8f;
                    mo.idle = true;
                    mo.spawnFrom = PokiClash.UI.UiMotion.SpawnFrom.Up;
                }
                tile.gameObject.SetActive(true);
                tile.Bind(list[i], s, d, i, () =>
                {
                    App.Audio.Play("click");
                    HeroDetail.Open(id, Refresh);
                });
                // hướng dẫn người mới (C9): chạm tướng đồng hành để nâng Chiêu bằng 2 bản sao của rương đầu
                if (id == s.starter)
                {
                    Guide.Mark("heroes.starter", tile);
                    if (!Tutorial.Done(s, Tutorial.UpCard) && Progress.CanUpCard(s, d.Cfg, id, CardSlot.Skill))
                        Guide.Force(Tutorial.HeroTile, "heroes.starter", Loc.F("Chạm {0}.", d.Hero(id).name), null, true);
                }
                if (popIn && i < 24) PokiClash.UI.UiMotion.Of(tile).Spawn(popFirst + i * popStep);
            }
            // lưới ngắn lại (lọc hệ): ẩn ô thừa, giữ để dùng lại
            for (int i = list.Count; i < tiles.Count; i++) tiles[i].gameObject.SetActive(false);
            if (emptyText)
            {
                emptyText.gameObject.SetActive(list.Count == 0);
                if (list.Count == 0)
                    emptyText.text = filter >= 0
                        ? Loc.F("Chưa có tướng hệ {0}\n<size=75%>gom mảnh ở ải đảo, máy bi</size>", Elements.Name(FilterOrder[filter]))
                        : Loc.T("Chưa có tướng");
            }
            PaintFilters();
        }

        // tướng hiện trong lưới theo lọc hệ (elemFilter: chỉ số trong FilterOrder, -1 mọi hệ), xếp theo key (giảm dần nếu descending);
        // tướng đã có luôn trước tướng chưa có; trùng thì lực chiến (tướng chưa có: phần mảnh) rồi độ hiếm giảm dần
        public static List<HeroDef> Sorted(GameData d, SaveData s, int elemFilter, SortKey key, bool descending)
        {
            var shown = d.Heroes.Where(h =>
            {
                var hp = s.Hero(h.id);
                return (hp.owned || hp.shards > 0) && (elemFilter < 0 || elemFilter >= FilterOrder.Length || h.elem == FilterOrder[elemFilter]);
            }).ToList();
            var power = new Dictionary<string, int>();
            foreach (var h in shown)
                if (s.Hero(h.id).owned) power[h.id] = HeroStats.Power(d.Cfg, h, Teams.MemberOf(s, h.id, d));
            int sign = descending ? -1 : 1;
            // tướng chưa có: phần mảnh đã gom (gần mở trước)
            double Ratio(HeroDef h) => s.Hero(h.id).shards / (double)Math.Max(1, h.shards);
            double Strength(HeroDef h) => power.TryGetValue(h.id, out var pw) ? pw : Ratio(h);
            double Primary(HeroDef h)
            {
                var hp = s.Hero(h.id);
                switch (key)
                {
                    case SortKey.Rarity: return (int)h.rarity;
                    case SortKey.Elem: return FilterOrder.Length - Array.IndexOf(FilterOrder, h.elem); // giảm dần = Thủy, Hỏa, Kim, Mộc, Thổ
                    case SortKey.Star: return hp.owned ? hp.star : Ratio(h);
                    case SortKey.CardLevel: return hp.owned ? CardLevels(hp) : Ratio(h);
                    default: return Strength(h);
                }
            }
            return shown
                .OrderByDescending(h => s.Hero(h.id).owned)
                .ThenBy(h => sign * Primary(h))
                .ThenByDescending(Strength)
                .ThenByDescending(h => (int)h.rarity)
                .ToList();
        }

        // tổng cấp 3 thẻ riêng (chiêu, tuyệt kỹ, bị động)
        static int CardLevels(HeroProg hp) => hp.skill.lv + hp.ult.lv + hp.passive.lv;

        // ---------- lọc, xếp ----------

        static void LoadPrefs()
        {
            if (prefsLoaded) return;
            prefsLoaded = true;
            try
            {
                sort = (SortKey)Mathf.Clamp(PlayerPrefs.GetInt(PrefSort, (int)SortKey.Power), 0, SortNames.Length - 1);
                desc = PlayerPrefs.GetInt(PrefDesc, 1) != 0;
                filter = Mathf.Clamp(PlayerPrefs.GetInt(PrefFilter, -1), -1, FilterOrder.Length - 1);
            }
            catch (Exception e)
            {
                Debug.LogWarning("[Tướng] Không đọc được lựa chọn lọc / xếp: " + e.Message);
            }
        }

        static void SavePrefs()
        {
            try
            {
                PlayerPrefs.SetInt(PrefSort, (int)sort);
                PlayerPrefs.SetInt(PrefDesc, desc ? 1 : 0);
                PlayerPrefs.SetInt(PrefFilter, filter);
                PlayerPrefs.Save();
            }
            catch (Exception e)
            {
                Debug.LogWarning("[Tướng] Không ghi được lựa chọn lọc / xếp: " + e.Message);
            }
        }

        void WireFilters()
        {
            if (filterAll) filterAll.SetOnClick(() => SetFilter(-1));
            for (int i = 0; i < filterElems.Length; i++)
            {
                int k = i;
                if (filterElems[i]) filterElems[i].SetOnClick(() => SetFilter(filter == k ? -1 : k));
            }
            if (sortButton)
                sortButton.SetOnClick(() =>
                {
                    sort = (SortKey)(((int)sort + 1) % SortNames.Length);
                    Changed();
                });
            if (dirButton)
                dirButton.SetOnClick(() =>
                {
                    desc = !desc;
                    Changed();
                });
        }

        void SetFilter(int f)
        {
            filter = f;
            Changed();
        }

        // lựa chọn đổi: nhớ lại, lưới cuộn về đầu, ô nảy ra lần lượt (nhanh hơn lúc vào màn)
        void Changed()
        {
            SavePrefs();
            popIn = true;
            popFirst = 0.02f;
            popStep = 0.025f;
            RenderGrid();
            popIn = false;
            var sr = grid ? grid.GetComponentInParent<ScrollRect>() : null;
            if (sr) sr.verticalNormalizedPosition = 1;
        }

        // nút đang chọn tô màu (hệ: màu hệ; Tất cả: vàng), còn lại màu giấy, icon hệ mờ; chữ nút xếp; mũi tên chiều
        void PaintFilters()
        {
            if (!HasFilters) return;
            if (filterAll) filterAll.SetColor(filter < 0 ? Theme.Yellow : Theme.Paper3);
            for (int i = 0; i < filterElems.Length && i < FilterOrder.Length; i++)
            {
                if (!filterElems[i]) continue;
                bool on = filter == i;
                filterElems[i].SetColor(on ? Theme.Of(FilterOrder[i]) : Theme.Paper2);
                if (i < filterIcons.Length && filterIcons[i]) filterIcons[i].color = new Color(1, 1, 1, on || filter < 0 ? 1 : 0.45f);
            }
            sortButton.SetText(Loc.T(SortNames[(int)sort]));
            sortButton.FitWidth();
            if (dirIcon)
            {
                var ic = Icon(desc ? "down" : "up");
                if (ic) Theme.SetSprite(dirIcon, ic);
            }
        }
    }
}
