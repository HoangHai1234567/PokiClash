// Một tướng trong danh sách chọn tướng của Trang trại (prefab Assets/04 Prefabs/Items/TuongTrangTrai): chân dung, tên, bi/giờ, giờ làm,
// hợp hệ; tướng rảnh có nút "Đặt" (dat_<id>), tướng bận ghi đang làm ở đâu hoặc nghỉ còn bao lâu.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class FarmHeroRow : MonoBehaviour
    {
        [SerializeField] Image bg;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI heroName, stats, why;
        [SerializeField] SketchButton place;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image panel, HeroPortrait heroPortrait, TextMeshProUGUI nameText, TextMeshProUGUI statsText, TextMeshProUGUI whyText,
            SketchButton placeButton)
        {
            bg = panel;
            portrait = heroPortrait;
            heroName = nameText;
            stats = statsText;
            why = whyText;
            place = placeButton;
        }

        // Nhà: tướng h cho công trình b (năng suất, giờ làm, hợp hệ); rảnh thì có nút "Đặt", bận thì ghi đang làm ở đâu hoặc nghỉ bao lâu
        public void BindHome(GameData d, SaveData s, HeroDef h, HomeBuilding b, double now, Action onPlace)
        {
            string id = h.id;
            var hs = s.home;
            var df = Home.Def(d.Cfg, b.def);
            bool match = df.hasElem && h.elem == df.elem;
            var (at, _) = Home.Working(hs, id);
            double rest = Home.RestLeft(hs, id, now);
            bool free = at < 0 && rest <= 0;
            name = "tuong_" + id;
            bg.color = free ? Color.white : Theme.Paper2;
            portrait.Bind(h, 92, false);
            heroName.text = h.name;
            heroName.color = free ? Theme.Ink : Theme.Ink3;
            stats.text = Loc.F("{0} {1}/giờ · {2} giờ", FarmScene.Dec(Home.Rate(s, d, id, b)), Unit(df.output), FarmScene.Dec(Home.Hours(s, d, id))) + (match ? Loc.F(" · Hợp hệ ×{0}", FarmScene.Num(d.Cfg.farm.match)) : "");
            stats.color = match ? Theme.GreenD : Theme.Ink2;
            place.gameObject.SetActive(free);
            why.gameObject.SetActive(!free);
            if (free)
            {
                place.name = "dat_" + id;
                place.SetOnClick(onPlace);
            }
            else why.text = at >= 0 ? Loc.F("Đang làm ở {0}", Home.Def(d.Cfg, Home.Find(hs, at).def).Name) : Loc.F("Nghỉ còn {0} phút", Math.Ceiling(rest / 60000));
        }

        public static string Unit(string output) => output switch
        {
            "balls" => "bi",
            "wood" => Loc.T("gỗ"),
            "ore" => Loc.T("quặng"),
            "fish" => Loc.T("lần câu"),
            "stones" => Loc.T("đá"),
            "bread" => Loc.T("bánh"),
            _ => "",
        };

        // tướng h cho chỗ spot; onPlace: bấm "Đặt" (chỉ khi tướng rảnh)
        public void Bind(GameData d, SaveData s, FarmState f, HeroDef h, int spot, double now, Action onPlace)
        {
            string id = h.id;
            bool match = h.elem == d.Cfg.farm.spots[spot].elem;
            int at = Farm.Working(f, id);
            double rest = Farm.RestLeft(f, id, now);
            bool free = at < 0 && rest <= 0;
            name = "tuong_" + id;
            bg.color = free ? Color.white : Theme.Paper2;
            portrait.Bind(h, 92, false);
            heroName.text = h.name;
            heroName.color = free ? Theme.Ink : Theme.Ink3;
            stats.text = Loc.F("{0} bi/giờ · {1} giờ", FarmScene.Dec(Farm.Rate(s, d, id, spot)), FarmScene.Dec(Farm.Hours(s, d, id))) + (match ? Loc.F(" · Hợp hệ ×{0}", FarmScene.Num(d.Cfg.farm.match)) : "");
            stats.color = match ? Theme.GreenD : Theme.Ink2;
            place.gameObject.SetActive(free);
            why.gameObject.SetActive(!free);
            if (free)
            {
                place.name = "dat_" + id;
                place.SetOnClick(onPlace);
            }
            else why.text = at >= 0 ? Loc.F("Đang làm ở {0}", d.Cfg.farm.spots[at].Name) : Loc.F("Nghỉ còn {0} phút", Math.Ceiling(rest / 60000));
        }
    }
}
