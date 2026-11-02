// Hộp kết quả khai phá, bắt buộc chọn (prefab Assets/04 Prefabs/Dialogs/TiemNangSoSanh): cột Cũ / Mới, 4 dòng ô (dòng của ô
// chưa mở ẩn), mũi tên "»" khi đổi hoặc "=" khi giữ nguyên, tổng hai bên, nút "giu_cu" / "giu_moi".
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class PotentialCompareDialog : Dialog
    {
        // một dòng: ô cũ (nửa trái), ô mới (nửa phải), mũi tên giữa
        [Serializable]
        public struct Row
        {
            public GameObject root;
            public Image oldBg, newBg;
            public TextMeshProUGUI oldText, newText, arrow;
        }

        [SerializeField] Row[] rows;
        [SerializeField] TextMeshProUGUI totals;
        [SerializeField] SketchButton keepOld, keepNew;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Row[] slotRows, TextMeshProUGUI totalsText, SketchButton oldButton, SketchButton newButton)
        {
            rows = slotRows;
            totals = totalsText;
            keepOld = oldButton;
            keepNew = newButton;
        }

        // redraw: vẽ lại hộp tiềm năng sau khi chọn
        public void Show(string id, Action redraw)
        {
            var s = App.Save.Data;
            var cfg = App.Data.Cfg;
            var p = s.Hero(id);
            int open = Potential.OpenSlots(cfg, p.star);
            for (int i = 0; i < rows.Length; i++)
            {
                bool shown = i < open;
                rows[i].root.SetActive(shown);
                if (!shown) continue;
                var o = p.potential[i];
                var n = p.potentialNew[i];
                bool same = o != null && n != null && o.k == n.k && o.r == n.r;
                Cell(rows[i].oldBg, rows[i].oldText, o, cfg, false);
                Cell(rows[i].newBg, rows[i].newText, n, cfg, !same);
                rows[i].arrow.text = same ? "=" : "»";
            }
            totals.text = "Cũ: " + PotentialPanel.TotalsText(cfg, p.potential) + "\nMới: " + PotentialPanel.TotalsText(cfg, p.potentialNew);
            keepOld.SetOnClick(() => Choose(false));
            keepNew.SetOnClick(() => Choose(true));

            void Choose(bool keepNewLines)
            {
                Potential.Keep(s, id, keepNewLines);
                App.Save.Save();
                App.Audio.Play(keepNewLines ? "buff" : "click");
                Close();
                redraw();
            }
        }

        static void Cell(Image bg, TextMeshProUGUI t, PotLine x, BalanceConfig cfg, bool changed)
        {
            bg.color = x != null ? Color.Lerp(PotentialPanel.RarityColor(x.r), Color.white, 0.65f) : Color.white;
            t.text = x == null ? "Trống" : $"{PotentialPanel.LineText(cfg, x)} · {PotentialPanel.RarityName(x.r)}";
            t.color = changed ? Theme.Ink : Theme.Ink2;
        }
    }
}
