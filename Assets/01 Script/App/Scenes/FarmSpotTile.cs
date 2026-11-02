// Một chỗ làm của Trang trại (prefab Assets/04 Prefabs/Items/ChoTrangTrai): icon loại chỗ, tên, hệ hợp; chỗ chưa mở: ổ khoá và cấp mở;
// đã mở: bong bóng bi tích, "+ Đặt tướng" hoặc chân dung tướng (nhún khi làm, ngồi nghiêng khi hết sức), vòng sức còn, tên và bi/giờ.
// Chạm (ClickCatcher trên gốc "cho_<i>") mở danh sách chọn tướng. Mọi phần có sẵn trong prefab, Bind bật tắt theo dữ liệu.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class FarmSpotTile : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image bg, kind, ring;
            public ClickCatcher click;
            public TextMeshProUGUI name, lockText, stock, empty, ringText, info;
            public UiElemTag elemTag;
            public GameObject lockIcon, bubble;
            public HeroPortrait portrait;
            public Bob bob; // trên chân dung, bật khi tướng còn sức
        }

        [SerializeField] Parts p;

        Vector2 portraitPos;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        void Awake() => portraitPos = p.portrait.Rect.anchoredPosition;

        // chỗ i; open: đã mở theo cấp người chơi; onClick: mở danh sách chọn tướng (chỉ chỗ đã mở)
        public void Bind(GameData d, SaveData s, int i, bool open, FarmSpot sp, Action onClick)
        {
            var def = d.Cfg.farm.spots[i];
            name = "cho_" + i;
            p.bg.color = open ? Theme.CardFill : new Color(0.9f, 0.87f, 0.8f, 0.92f);
            p.click.enabled = open;
            p.click.OnClick = open ? onClick : null;
            p.kind.sprite = App.Art ? App.Art.Icon(FarmScene.KindIcon(def.kind)) : null;
            p.kind.color = open ? Color.white : new Color(1, 1, 1, 0.5f);
            p.name.text = def.name;
            p.name.color = open ? Theme.Ink : Theme.Ink3;
            p.elemTag.Set(def.elem);

            p.lockIcon.SetActive(!open);
            p.lockText.gameObject.SetActive(!open);
            p.bubble.SetActive(false);
            p.empty.gameObject.SetActive(false);
            SetHero(false);
            if (!open)
            {
                p.lockText.text = $"Mở ở cấp {Farm.SpotLevel(d.Cfg, i)}";
                return;
            }
            if (sp.stock >= 0.05)
            {
                p.bubble.SetActive(true);
                p.stock.text = FarmScene.Dec(sp.stock);
            }
            if (sp.hero == null)
            {
                p.empty.gameObject.SetActive(true);
                return;
            }
            var h = d.Hero(sp.hero);
            bool working = sp.energy > 0;
            SetHero(true);
            p.portrait.Bind(h, 150, false);
            p.bob.enabled = working;
            if (!working) p.portrait.Rect.anchoredPosition = portraitPos;
            p.portrait.Rect.localEulerAngles = working ? Vector3.zero : new Vector3(0, 0, -8);
            // vòng sức còn
            double hours = Farm.Hours(s, d, sp.hero);
            p.ring.color = working ? Theme.Green : Theme.Paper3;
            p.ring.fillAmount = working ? Mathf.Clamp01((float)(sp.energy / hours)) : 1;
            p.ringText.text = working ? FarmScene.Clock(sp.energy) : "hết";
            p.ringText.color = working ? Theme.Ink : Theme.Ink3;
            p.info.text = working ? $"{h.name}\n{FarmScene.Dec(Farm.Rate(s, d, sp.hero, i))} bi/giờ" : $"{h.name}\nHết sức: đổi ca";
            p.info.color = working ? Theme.Ink : Theme.RedD;
        }

        void SetHero(bool on)
        {
            p.portrait.gameObject.SetActive(on);
            p.ring.gameObject.SetActive(on);
            p.ringText.gameObject.SetActive(on);
            p.info.gameObject.SetActive(on);
        }
    }
}
