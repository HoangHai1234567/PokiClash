// Hộp kết quả trận (prefab Assets/04 Prefabs/Dialogs/TranKetQua, bắt buộc): con dấu Thắng/Thua, tên ải, số hiệp và sát thương,
// dòng thưởng (Items/TranThuong) hoặc lời khuyên khi thua, tối đa 4 nút (dựng sẵn, bật theo trận: ải thường, Hang, Đền Huy Hiệu).
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BattleResultDialog : Dialog
    {
        [SerializeField] UiStamp stamp;
        [SerializeField] TextMeshProUGUI title, stats, tips;
        [SerializeField] SketchButton[] buttons;
        [SerializeField] BattleRewardRow rowPrefab;
        int used;

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiStamp stampView, TextMeshProUGUI titleText, TextMeshProUGUI statsText, TextMeshProUGUI tipsText, SketchButton[] btns,
            BattleRewardRow row)
        {
            stamp = stampView;
            title = titleText;
            stats = statsText;
            tips = tipsText;
            buttons = btns;
            rowPrefab = row;
        }

        // titleSize: 40 (ải thường), 38 (Hang, Đền). Sau đó gọi Reward / Tips / Button theo thứ tự hiện.
        public void Show(bool win, string titleText, float titleSize, string statsText)
        {
            stamp.Set(win ? "Thắng!" : "Thua rồi", win ? Theme.Red : Theme.Hex("#6f6a7a"));
            title.text = titleText;
            title.fontSize = titleSize;
            stats.text = statsText;
            tips.gameObject.SetActive(false);
            used = 0;
            foreach (var b in buttons) b.gameObject.SetActive(false);
        }

        // dòng thưởng, thêm trước dòng lời khuyên và hàng nút
        public void Reward(Sprite icon, HeroDef hero, string titleText, string sub, Color fill)
        {
            var row = Ui.Spawn(rowPrefab, tips.transform.parent);
            row.transform.SetSiblingIndex(tips.transform.GetSiblingIndex());
            row.Bind(icon, hero, titleText, sub, fill);
        }

        public void Tips(string text)
        {
            tips.gameObject.SetActive(true);
            tips.text = text;
        }

        // nút cỡ nhỏ, bề rộng cố định; bấm thì đóng hộp rồi gọi onClick
        public void Button(string label, BtnColor color, float width, Action onClick)
        {
            if (used >= buttons.Length) return;
            var b = buttons[used++];
            b.gameObject.SetActive(true);
            b.name = "nut_" + label;
            b.SetRole(color);
            b.SetText(label);
            b.Rect.sizeDelta = new Vector2(width, b.Rect.sizeDelta.y);
            var le = b.GetComponent<LayoutElement>();
            if (le) le.preferredWidth = width;
            b.SetOnClick(() =>
            {
                Close();
                onClick?.Invoke();
            });
        }
    }
}
