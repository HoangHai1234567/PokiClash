// Dải tiềm năng trong hộp chi tiết tướng (nằm trong prefab Assets/04 Prefabs/Dialogs/ChiTietTuong): tiêu đề, tổng phần cộng,
// 4 ô nhỏ (màu theo độ hiếm, "Mở ở n sao" khi chưa mở), nút "Khai phá" (mo_tiem_nang) nhịp phồng khi còn kết quả chưa chọn.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class PotentialStrip : MonoBehaviour
    {
        [SerializeField] TextMeshProUGUI totals;
        [SerializeField] Image[] cells;
        [SerializeField] TextMeshProUGUI[] labels;
        [SerializeField] SketchButton open;
        [SerializeField] Pulse pulse;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI totalsText, Image[] cellImgs, TextMeshProUGUI[] cellTexts, SketchButton openBtn, Pulse openPulse)
        {
            totals = totalsText;
            cells = cellImgs;
            labels = cellTexts;
            open = openBtn;
            pulse = openPulse;
        }

        // changed: gọi khi hộp tiềm năng đóng
        public void Bind(string id, Action changed)
        {
            var cfg = App.Data.Cfg;
            var p = App.Save.Data.Hero(id);
            int openSlots = Potential.OpenSlots(cfg, p.star);
            totals.text = PotentialPanel.TotalsText(cfg, p.potential);
            for (int i = 0; i < cells.Length; i++)
            {
                var x = p.potential[i];
                bool on = i < openSlots;
                cells[i].color = on && x != null ? Color.Lerp(PotentialPanel.RarityColor(x.r), Color.white, 0.55f) : on ? Color.white : Theme.Paper2;
                labels[i].text = PotentialPanel.CellText(cfg, x, on, i);
                labels[i].color = on ? Theme.Ink : Theme.Ink3;
            }
            open.SetOnClick(() => PotentialPanel.Open(id, changed));
            bool fresh = p.potentialNew != null;
            pulse.enabled = fresh;
            if (!fresh) open.transform.localScale = Vector3.one;
        }
    }
}
