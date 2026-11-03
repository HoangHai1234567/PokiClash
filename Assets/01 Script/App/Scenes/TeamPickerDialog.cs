// Hộp chọn đội (prefab Assets/04 Prefabs/Dialogs/ChonDoi, biến thể tờ giấy gốc HopThoai, dựng bằng menu
// "PokiClash/Prefab/Hộp chọn đội (ChonDoi)"): mở khi chạm ô đội trong hộp Chuẩn bị trận. Kho tướng đã có (Items/OKho):
// chạm để chọn hoặc bỏ, số trước tên là thứ tự ra trận; một lần mở chọn được đủ số ô đã mở (Progress.TeamSlots);
// mũi tên khắc hệ theo tướng chính của địch; dòng cuối báo ô đội nào còn khoá. "Xong" trả đội về.
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

        List<string> team;
        int slots;
        HeroDef foe;

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
            Draw();
        }

        void Draw()
        {
            var d = App.Data;
            var s = App.Save.Data;
            title.text = $"Chọn đội · {team.Count}/{slots}";
            for (int i = grid.childCount - 1; i >= 0; i--) Destroy(grid.GetChild(i).gameObject);
            var owned = d.Heroes.Where(h => s.Hero(h.id).owned).ToList();
            gridLayout.preferredHeight = ((owned.Count + 5) / 6) * 176;
            foreach (var h in owned)
            {
                var hero = h;
                bool partner = h.id == s.starter;
                double adv = foe != null ? Elements.Mult(h.elem, foe.elem, partner, false) : 1,
                    bad = foe != null ? Elements.Mult(foe.elem, h.elem, false, partner) : 1;
                bool khac = adv > 1 || bad > 1;
                int order = team.IndexOf(h.id) + 1;
                Ui.Spawn(cellPrefab, grid).Bind(h, order > 0, khac, khac ? Icon(adv > 1 ? "up" : "down") : null, () =>
                {
                    App.Audio.Play("click");
                    if (team.Contains(hero.id)) team.Remove(hero.id);
                    else if (team.Count < slots) team.Add(hero.id);
                    else
                    {
                        App.Toasts.Show(slots < Progress.TeamSlotMax ? $"Đang mở {slots} ô đội: ô {slots + 1} mở khi {Progress.SlotNeed(slots)}" : $"Đội tối đa {slots} tướng",
                            Icon("team"));
                        return;
                    }
                    Draw();
                }, order);
            }
            done.Interactable = team.Count > 0;
        }
    }
}
