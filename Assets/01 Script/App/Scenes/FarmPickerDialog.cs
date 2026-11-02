// Hộp chọn tướng cho một chỗ của Trang trại (prefab Assets/04 Prefabs/Dialogs/ChonTuongTrangTrai): tiêu đề "chỗ · hợp hệ",
// khung tướng đang làm (sức còn, nghỉ bao lâu nếu rút, nút "Rút ra" rut_ra; ẩn khi chỗ trống), rồi mỗi tướng đã có là một bản sao
// prefab Items/TuongTrangTrai (FarmHeroRow), xếp theo bi/giờ giảm dần.
using System;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class FarmPickerDialog : Dialog
    {
        [SerializeField] RectTransform body; // tờ giấy (dọc, tự giãn): các tướng sinh nối sau khung đang làm
        [SerializeField] TextMeshProUGUI title;
        [SerializeField] GameObject current;
        [SerializeField] HeroPortrait currentPortrait;
        [SerializeField] TextMeshProUGUI currentText, currentRest;
        [SerializeField] SketchButton remove;
        [SerializeField] FarmHeroRow rowPrefab;

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform sheet, TextMeshProUGUI titleText, GameObject currentPanel, HeroPortrait currentHero, TextMeshProUGUI currentLabel,
            TextMeshProUGUI restLabel, SketchButton removeButton, FarmHeroRow row)
        {
            body = sheet;
            title = titleText;
            current = currentPanel;
            currentPortrait = currentHero;
            currentText = currentLabel;
            currentRest = restLabel;
            remove = removeButton;
            rowPrefab = row;
        }

        // chỗ i; changed(reopen): bản lưu đã đổi và hộp đã đóng; reopen: mở lại danh sách của chỗ này (sau khi rút ra)
        public void Show(int i, Action<bool> changed)
        {
            var d = App.Data;
            var s = App.Save.Data;
            double now = SaveService.Now();
            Farm.Tick(s, d, now);
            var f = Farm.Of(s, d.Cfg, now);
            var def = d.Cfg.farm.spots[i];
            var sp = f.spots[i];
            title.text = $"{def.name} · hợp hệ {Elements.Name(def.elem)}";
            current.SetActive(sp.hero != null);
            if (sp.hero != null)
            {
                var h = d.Hero(sp.hero);
                currentPortrait.Bind(h, 110);
                currentText.text = sp.energy > 0 ? $"{h.name}: còn {FarmScene.Clock(sp.energy)} giờ làm" : $"{h.name}: hết sức";
                currentRest.text = $"Rút ra thì nghỉ {Farm.RestMin(s, d, sp.hero):0} phút";
                remove.SetOnClick(() =>
                {
                    Farm.Remove(s, d, SaveService.Now(), i);
                    App.Save.Save();
                    Close();
                    changed(true);
                });
            }
            var heroes = d.Heroes.Where(h => s.Hero(h.id).owned).OrderByDescending(h => Farm.Rate(s, d, h.id, i)).ToList();
            foreach (var h in heroes)
            {
                string id = h.id;
                var row = Ui.Spawn(rowPrefab, body);
                row.Bind(d, s, f, h, i, now, () =>
                {
                    if (sp.hero != null) Farm.Remove(s, d, SaveService.Now(), i);
                    if (Farm.Place(s, d, SaveService.Now(), i, id)) App.Audio.Play("buff");
                    App.Save.Save();
                    Close();
                    changed(false);
                });
            }
        }
    }
}
