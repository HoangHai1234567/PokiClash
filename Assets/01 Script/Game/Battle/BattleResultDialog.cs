// Hộp kết quả trận (prefab Assets/04 Prefabs/Dialogs/TranKetQua, bắt buộc): con dấu Thắng/Thua, tên ải, số hiệp và sát thương,
// hàng ô thưởng (Items/OThuong trong hàng "thuong", menu "PokiClash/Prefab/Khác/Hộp thoại và màn∕Popup gọn (ô thưởng, đội hình, lực chiến)" dựng) hoặc
// lời khuyên khi thua, tối đa 4 nút (dựng sẵn, bật theo trận: ải thường, Hang, Đền Huy Hiệu).
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
        [SerializeField] RewardTile tilePrefab;
        [SerializeField] RectTransform tileRow;
        [SerializeField] SketchButton adButton; // nút quảng cáo riêng dưới lời khuyên (Tiếp sức / Nhận ×2, GD_Claude/26 mục 8.1), menu "PokiClash/Prefab/Khác/Hộp thoại và màn∕Cửa hàng: dựng hết"
        int used;

        // Dùng khi nướng prefab (Editor).
        public void Setup(UiStamp stampView, TextMeshProUGUI titleText, TextMeshProUGUI statsText, TextMeshProUGUI tipsText, SketchButton[] btns,
            RewardTile tile, RectTransform row)
        {
            stamp = stampView;
            title = titleText;
            stats = statsText;
            tips = tipsText;
            buttons = btns;
            tilePrefab = tile;
            tileRow = row;
        }

        // titleSize: 40 (ải thường), 38 (Hang, Đền). Sau đó gọi Reward / Tips / Button theo thứ tự hiện.
        public void Show(bool win, string titleText, float titleSize, string statsText)
        {
            stamp.Set(win ? Loc.T("Thắng!") : Loc.T("Thua rồi"), win ? Theme.Red : Theme.Hex("#6f6a7a"));
            title.text = titleText;
            title.fontSize = titleSize;
            stats.text = statsText;
            tips.gameObject.SetActive(false);
            for (int i = tileRow.childCount - 1; i >= 0; i--) Destroy(tileRow.GetChild(i).gameObject);
            tileRow.gameObject.SetActive(false);
            used = 0;
            foreach (var b in buttons) b.gameObject.SetActive(false);
            if (adButton) adButton.gameObject.SetActive(false);
        }

        // nút quảng cáo thưởng (ghi lượt còn); xem xong thì onOk (hộp vẫn mở nếu keep, không thì đóng rồi gọi)
        public SketchButton AdButton(string label, string placement, bool keep, Action onOk)
        {
            if (!adButton || !Ads.Ready || Ads.Left(placement) <= 0) return null;
            adButton.gameObject.SetActive(true);
            adButton.name = "nut_qc_" + placement;
            adButton.SetRole(BtnColor.Blue);
            Ads.Bind(adButton, label, placement);
            adButton.SetOnClick(() => Ads.Show(placement, ok =>
            {
                if (!ok) return;
                if (keep) adButton.gameObject.SetActive(false);
                else Close();
                onOk?.Invoke();
            }));
            return adButton;
        }

        // một ô thưởng trong hàng thưởng (trước dòng lời khuyên và hàng nút); người gọi gán nội dung (Item / Hero / Tag)
        public RewardTile Reward()
        {
            tileRow.gameObject.SetActive(true);
            var t = Ui.Spawn(tilePrefab, tileRow);
            App.I.StartCoroutine(ChestBox.Pop(t.Rect, 1.15f));
            return t;
        }

        public void Tips(string text)
        {
            tips.gameObject.SetActive(true);
            tips.text = text;
        }

        // nút cỡ nhỏ, bề rộng cố định; bấm thì đóng hộp rồi gọi onClick. Trả về nút (hướng dẫn người mới khoanh nút này), hết chỗ thì null
        public SketchButton Button(string label, BtnColor color, float width, Action onClick)
        {
            if (used >= buttons.Length) return null;
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
            if (want == null || want.Length != buttons.Length) want = new float[buttons.Length];
            want[used - 1] = width;
            FitButtons();
            return b;
        }

        float[] want; // bề rộng xin của từng nút đang bật

        // hàng nút vừa tờ giấy: đủ bốn nút (Máy bi, Ải tiếp, Đánh lại, tên đảo) rộng hơn hàng thì co đều theo bề rộng xin
        // (soát UI 2026-11-23: hai nút ngoài lòi khỏi tờ)
        void FitButtons()
        {
            var row = used > 0 ? buttons[0].Rect.parent as RectTransform : null;
            if (!row) return;
            var hl = row.GetComponent<HorizontalOrVerticalLayoutGroup>();
            float gap = hl ? hl.spacing : 0, pad = hl ? hl.padding.horizontal : 0;
            // hàng tự co theo nút (ContentSizeFitter) nên lấy bề ngang tờ giấy, chừa lề 30 mỗi bên
            var paper = row.parent as RectTransform;
            float rowW = paper ? paper.rect.width - 60 : row.rect.width;
            float avail = rowW - pad - gap * (used - 1), total = 0;
            for (int i = 0; i < used; i++) total += want[i];
            float k = total > avail && total > 0 ? avail / total : 1;
            for (int i = 0; i < used; i++)
            {
                var b = buttons[i];
                float w = want[i] * k;
                b.Rect.sizeDelta = new Vector2(w, b.Rect.sizeDelta.y);
                var le = b.GetComponent<LayoutElement>();
                if (le) le.preferredWidth = w;
            }
        }
    }
}
