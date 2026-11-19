// Hộp tiềm năng của một tướng (prefab Assets/04 Prefabs/Dialogs/TiemNang): tiêu đề, chip đá, chip đá tinh, các dòng ô (số ô, dòng tiềm
// năng, độ hiếm, nút khoá "khoa_i" hoặc ổ khoá khi ô chưa mở), tổng, dòng bộ, nút "khai_pha" và "khai_pha_tinh" (đá tinh: mọi ô từ Hiếm),
// ghi chú giá. Khai phá xong mở hộp so sánh (Dialogs/TiemNangSoSanh). Mọi phần có sẵn trong prefab, Render bật tắt và gán chữ, màu.
// 2026-11-17: 6 ô, đá tinh, bộ. Ô 5, 6, chip đá tinh, nút đá tinh, dòng bộ do menu "PokiClash/Prefab/Tiềm năng: 6 ô, bộ, đá tinh"
// (Editor/SideMetaUiMenu.cs) dựng; prefab chưa dựng lại thì hộp chạy với số ô có sẵn và ẩn phần mới.
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
    public sealed class PotentialDialog : Dialog
    {
        // một dòng ô tiềm năng
        [Serializable]
        public struct Row
        {
            public Image bg;
            public TextMeshProUGUI text, rarity;
            public SketchButton lockButton;
            public Image lockButtonIcon;
            public GameObject lockIcon; // ổ khoá của ô chưa mở
        }

        [SerializeField] TextMeshProUGUI title, stones;
        [SerializeField] Row[] rows;
        [SerializeField] TextMeshProUGUI totals, note;
        [SerializeField] SketchButton spin;
        [SerializeField] PotentialCompareDialog comparePrefab;
        // 2026-11-17 (menu SideMetaUiMenu dựng; có thể trống)
        [SerializeField] TextMeshProUGUI crystals, sets;
        [SerializeField] SketchButton spinCrystal;

        string id;
        readonly List<bool> locks = Enumerable.Repeat(false, Potential.Slots).ToList();

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, TextMeshProUGUI stonesText, Row[] slotRows, TextMeshProUGUI totalsText, TextMeshProUGUI noteText,
            SketchButton spinButton, PotentialCompareDialog compare)
        {
            title = titleText;
            stones = stonesText;
            rows = slotRows;
            totals = totalsText;
            note = noteText;
            spin = spinButton;
            comparePrefab = compare;
        }

        public void Show(string heroId)
        {
            id = heroId;
            for (int i = 0; i < locks.Count; i++) locks[i] = false;
            for (int i = 0; i < rows.Length; i++)
            {
                int k = i;
                rows[i].lockButton.SetOnClick(() => ToggleLock(k));
            }
            spin.SetOnClick(() => Spin(false));
            if (spinCrystal) spinCrystal.SetOnClick(() => Spin(true));
            Render();
            if (App.Save.Data.Hero(id).potentialNew != null) Compare();
        }

        void Render()
        {
            var d = App.Data;
            var s = App.Save.Data;
            var cfg = d.Cfg;
            var hero = d.Hero(id);
            var p = s.Hero(id);
            int open = Potential.OpenSlots(cfg, p.star);

            title.text = $"Tiềm năng · {hero.name}";
            stones.text = s.potentialStones.ToString();
            if (crystals) crystals.text = s.potentialCrystals.ToString();
            for (int i = 0; i < rows.Length; i++)
            {
                var r = rows[i];
                var x = Potential.LineAt(p.potential, i);
                bool on = i < open;
                r.bg.color = on && x != null ? Color.Lerp(PotentialPanel.RarityColor(x.r), Color.white, 0.7f) : on ? Color.white : Theme.Paper2;
                string set = x != null ? PotentialPanel.SetOf(cfg, x.k) : "";
                r.text.text = !on ? Potential.SlotNeed(cfg, i, hero) : x == null ? "Trống: khai phá để có dòng"
                    : PotentialPanel.LineText(cfg, x) + (set.Length > 0 ? $" <size=70%><color=#7a6f62>· {set}</color></size>" : "");
                r.text.color = on ? Theme.Ink : Theme.Ink3;
                bool line = on && x != null;
                r.rarity.gameObject.SetActive(line);
                r.lockButton.gameObject.SetActive(line);
                r.lockIcon.SetActive(!on);
                if (!line) continue;
                r.rarity.text = PotentialPanel.RarityName(x.r);
                r.rarity.color = PotentialPanel.RarityColor(x.r);
                r.lockButton.SetRole(locks[i] ? BtnColor.Yellow : BtnColor.Paper);
                r.lockButtonIcon.color = locks[i] ? Color.white : new Color(1, 1, 1, 0.45f);
            }

            totals.text = "Tổng: " + PotentialPanel.TotalsText(cfg, p.potential);
            if (sets) sets.text = PotentialPanel.SetsText(cfg, p.potential);
            int cost = Potential.SpinCost(s, cfg, id, locks);
            int lk = Potential.LockCount(s, cfg, id, locks);
            bool canSpin = open - lk > 0 && s.potentialStones >= cost;
            spin.SetText(canSpin ? $"Khai phá ({cost} đá)" : open - lk <= 0 ? "Không còn ô để quay" : $"Cần {cost} đá");
            spin.Interactable = canSpin;
            if (spinCrystal)
            {
                int cc = Potential.SpinCost(s, cfg, id, locks, true);
                bool canC = open - lk > 0 && s.potentialCrystals >= Potential.CrystalCost && s.potentialStones >= cc;
                spinCrystal.gameObject.SetActive(s.potentialCrystals > 0 || canC);
                spinCrystal.SetText(cc > 0 ? $"Đá tinh (1 + {cc} đá)" : "Đá tinh (1)");
                spinCrystal.Interactable = canC;
            }
            note.text = $"Mỗi ô quay 1 đá, mỗi ô khoá thêm {cfg.potential.lockCost} đá, khoá tối đa {cfg.potential.maxLocks} ô. " +
                        "Đá tinh: 1 đá tinh thay đá của các ô quay, mọi ô ra từ Hiếm trở lên. " +
                        "Đá có từ rương máy bi, rương AFK, Hang Tiềm Năng; đá tinh từ Hang, Đền Huy Hiệu.";
        }

        void ToggleLock(int k)
        {
            var cfg = App.Data.Cfg;
            var p = App.Save.Data.Hero(id);
            int open = Potential.OpenSlots(cfg, p.star);
            if (!locks[k] && locks.Where((l, j) => l && Potential.LineAt(p.potential, j) != null && j < open).Count() >= cfg.potential.maxLocks)
            {
                App.Toasts.Show($"Khoá tối đa {cfg.potential.maxLocks} ô", PotentialPanel.Icon("lock"));
                return;
            }
            locks[k] = !locks[k];
            Render();
        }

        void Spin(bool crystal)
        {
            var s = App.Save.Data;
            var res = Potential.Spin(s, App.Data.Cfg, id, locks, new Rng(Rng.RandomSeed()), crystal);
            if (res == null) return;
            App.Save.Save();
            App.Audio.Play("chest");
            Render();
            Compare();
        }

        // so sánh cũ / mới, bắt buộc chọn
        void Compare()
        {
            if (App.Save.Data.Hero(id).potentialNew == null) return;
            App.Modals.Open(comparePrefab).Show(id, Render);
        }
    }
}
