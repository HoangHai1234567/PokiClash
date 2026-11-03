// Hộp chọn bạn đồng hành (prefab Assets/04 Prefabs/Dialogs/ChonTuongKhoiDau, biến thể tờ giấy gốc HopThoai, dựng bằng menu
// "PokiClash/Prefab/Hộp chọn tướng khởi đầu (ChonTuongKhoiDau)"): người chơi mới chọn 1 trong 5 tướng khởi đầu, mỗi hệ một con
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
            pick.SetText($"Chọn {h.name}");
        }

        // hệ, khắc và bị khắc, 3 thẻ ở cấp 1
        public static string Describe(GameData d, HeroDef h)
        {
            string Card(string id)
            {
                var c = d.Card(id);
                return $"<b>{Elements.KindName(c.kind)} · {c.name}:</b> {CardText.Text(c, 1, d.Cfg.cardLvStep)}";
            }
            return $"<b>{h.name}</b> · hệ {Elements.Name(h.elem)} · {h.title}\n" +
                   $"Khắc {Elements.Name(Elements.Beats(h.elem))}, bị {Elements.Name(Progress.CounterOf(h.elem))} khắc " +
                   "(bạn đồng hành không sợ bị khắc)\n" +
                   $"{Card(h.skill)}\n{Card(h.ult)}\n{Card(h.passive)}";
        }

        void Confirm()
        {
            var h = App.Data.Hero(sel);
            App.Modals.Confirm($"Chọn {h.name}?",
                $"{h.name} sẽ là bạn đồng hành suốt chuyến phiêu lưu, không đổi lại được. 4 tướng kia đứng ở ải 1 các đảo khác, thu phục sau.",
                "Chọn", () =>
                {
                    App.Save.Data.ChooseStarter(sel);
                    App.Save.Save();
                    App.Audio.Play("chest");
                    Close();
                    onPicked?.Invoke(sel);
                }, "Xem lại", BtnColor.Green);
        }
    }
}
