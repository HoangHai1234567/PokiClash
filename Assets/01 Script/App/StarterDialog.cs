// Hộp chọn bạn đồng hành (prefab Assets/04 Prefabs/Dialogs/ChonTuongKhoiDau, biến thể tờ giấy gốc HopThoai, dựng bằng menu
// "PokiClash/Prefab/Khác/Hộp thoại và màn∕Hộp chọn tướng khởi đầu (ChonTuongKhoiDau)"): người chơi mới chọn 1 trong 5 tướng khởi đầu, mỗi hệ một con
// (GD_Claude/15_TuongKhoiDau.md). Chạm ô để xem hệ và 3 thẻ; "Chọn …" hỏi lại rồi nhận tướng (đội chỉ có tướng đó). Bắt buộc.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class StarterDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI info;
        [SerializeField] RectTransform grid;
        [SerializeField] SketchButton pick;
        [SerializeField] PrepRosterCell cellPrefab;

        string sel;
        Action<string> onPicked;

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextMeshProUGUI infoText, RectTransform gridRt, SketchButton pickBtn, PrepRosterCell cell)
        {
            info = infoText;
            grid = gridRt;
            pick = pickBtn;
            cellPrefab = cell;
        }

        public void Show(Action<string> picked = null)
        {
            onPicked = picked;
            sel = App.Data.Starters[0];
            pick.SetOnClick(Confirm);
            Draw();
        }

        void Draw()
        {
            var d = App.Data;
            for (int i = grid.childCount - 1; i >= 0; i--) Destroy(grid.GetChild(i).gameObject);
            foreach (var id in d.Starters)
            {
                var hid = id;
                Ui.Spawn(cellPrefab, grid).Bind(d.Hero(id), id == sel, false, null, () =>
                {
                    App.Audio.Play("click");
                    sel = hid;
                    Draw();
                });
            }
            var h = d.Hero(sel);
            info.text = Describe(d, h);
            pick.SetText(Loc.F("Chọn {0}", h.name));
        }

        // người mới chưa biết thẻ là gì (GD_Claude/25_FTUE.md bước A3–A4): chỉ tên, hệ, danh hiệu và một chữ vai. Hệ khắc, 3 thẻ xem ở
        // hộp chi tiết tướng sau. Bản cũ (hệ khắc, 3 thẻ ở cấp 1) giữ ở DescribeFull.
        public static string Describe(GameData d, HeroDef h)
        {
            string role = Tutorial.Role(h.id);
            return Loc.F("<b>{0}</b> · hệ {1}\n", h.name, Elements.Name(h.elem)) +
                   (string.IsNullOrEmpty(role) ? "" : Loc.F("<size=120%><b>{0}</b></size>\n", role)) +
                   $"<i>{h.title}</i>";
        }

        // hệ, khắc và bị khắc, 3 thẻ ở cấp 1
        public static string DescribeFull(GameData d, HeroDef h)
        {
            string Card(string id)
            {
                var c = d.Card(id);
                return $"<b>{Elements.KindName(c.kind)} · {c.name}:</b> {CardText.Text(c, 1, d.Cfg.cardLvStep)}";
            }
            return Loc.F("<b>{0}</b> · hệ {1} · {2}\n", h.name, Elements.Name(h.elem), h.title) +
                   Loc.F("Khắc {0}, bị {1} khắc ", Elements.Name(Elements.Beats(h.elem)), Elements.Name(Progress.CounterOf(h.elem))) +
                   Loc.T("(bạn đồng hành không sợ bị khắc)\n") +
                   $"{Card(h.skill)}\n{Card(h.ult)}\n{Card(h.passive)}";
        }

        void Confirm()
        {
            var h = App.Data.Hero(sel);
            App.Modals.Confirm(Loc.F("Đi cùng {0} nhé?", h.name),
                Loc.T("Không đổi lại được. Bạn sẽ gặp lại 4 bạn kia trên các đảo."),
                Loc.T("Đi thôi!"), () =>
                {
                    App.Save.Data.ChooseStarter(sel);
                    App.Save.Save();
                    // đảo của tướng vừa chọn là đảo vào đầu tiên: nạp gói của nó trước (GD_Claude/27)
                    PokiClash.Game.ContentPacks.Request(PokiClash.Core.Keys.Of(h.elem), true);
                    App.Audio.Play("chest");
                    Haptics.Play(Haptic.Reward);
                    Close();
                    onPicked?.Invoke(sel);
                }, Loc.T("Xem lại"), BtnColor.Green);
        }
    }
}
