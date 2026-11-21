// Hộp chọn tướng cho một chỗ của Trang trại (prefab Assets/04 Prefabs/Dialogs/ChonTuongTrangTrai): tiêu đề "chỗ · hợp hệ",
// khung tướng đang làm (sức còn, nghỉ bao lâu nếu rút, nút "Rút ra" rut_ra; ẩn khi chỗ trống), rồi mỗi tướng đã có là một bản sao
// prefab Items/TuongTrangTrai (FarmHeroRow), xếp theo bi/giờ giảm dần.
// Màn Nhà dùng lại hộp này (ShowHome): một ô tướng của công trình làm ra đồ; quái chỉ vào làm khi người chơi chọn ở đây hoặc kéo thả vào
// công trình (người dùng dặn 2026-11-19, bỏ Tự xếp).
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

        const int MaxHomeRows = 9;

        // Nhà: ô slot của công trình id; changed(reopen) như Show
        public void ShowHome(int id, int slot, Action<bool> changed)
        {
            var d = App.Data;
            var s = App.Save.Data;
            double now = SaveService.Now();
            Home.Tick(s, d, now);
            var h = s.home;
            var b = Home.Find(h, id);
            if (b == null || slot < 0 || slot >= b.slots.Count)
            {
                Close();
                return;
            }
            var df = Home.Def(d.Cfg, b.def);
            var sl = b.slots[slot];
            title.text = Loc.F("{0} · ô {1}", df.Name, slot + 1) + (df.hasElem ? Loc.F(" · hợp hệ {0}", Elements.Name(df.elem)) : "");
            current.SetActive(sl.hero != null);
            if (sl.hero != null)
            {
                var hd = d.Hero(sl.hero);
                currentPortrait.Bind(hd, 110);
                currentText.text = sl.energy > 0 ? Loc.F("{0}: còn {1} giờ làm", hd.name, FarmScene.Clock(sl.energy)) : Loc.F("{0}: hết sức", hd.name);
                currentRest.text = Loc.F("Rút ra thì nghỉ {0:0} phút", Home.RestMin(s, d, sl.hero));
                remove.SetOnClick(() =>
                {
                    Home.Remove(s, d, SaveService.Now(), id, slot);
                    App.Save.Save();
                    Close();
                    changed(true);
                });
            }
            // hộp chưa cuộn được: chỉ tướng rảnh, năng suất cao nhất trước, tối đa MaxHomeRows dòng cho vừa màn
            var heroes = d.Heroes.Where(x => Home.Free(s, h, x.id, now)).OrderByDescending(x => Home.Rate(s, d, x.id, b)).Take(MaxHomeRows).ToList();
            foreach (var hd in heroes)
            {
                string hid = hd.id;
                var row = Ui.Spawn(rowPrefab, body);
                row.BindHome(d, s, hd, b, now, () =>
                {
                    double t = SaveService.Now();
                    if (b.slots[slot].hero != null) Home.Remove(s, d, t, id, slot);
                    var e = Home.Place(s, d, t, id, slot, hid);
                    if (e == HomeErr.Ok) App.Audio.Play("buff");
                    else App.Toasts.Show(e == HomeErr.TotalSlots ? Loc.T("Hết chỗ tướng: nâng Nhà chính") : e == HomeErr.BallSlots ? Loc.T("Hết chỗ ra bi: lên cấp để thêm") : Loc.T("Chưa giao được"), App.Art ? App.Art.Icon("lock") : null);
                    App.Save.Save();
                    Close();
                    changed(false);
                });
            }
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
            title.text = Loc.F("{0} · hợp hệ {1}", def.Name, Elements.Name(def.elem));
            current.SetActive(sp.hero != null);
            if (sp.hero != null)
            {
                var h = d.Hero(sp.hero);
                currentPortrait.Bind(h, 110);
                currentText.text = sp.energy > 0 ? Loc.F("{0}: còn {1} giờ làm", h.name, FarmScene.Clock(sp.energy)) : Loc.F("{0}: hết sức", h.name);
                currentRest.text = Loc.F("Rút ra thì nghỉ {0:0} phút", Farm.RestMin(s, d, sp.hero));
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
