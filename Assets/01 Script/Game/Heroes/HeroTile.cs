// Một ô trong lưới Tướng (prefab Assets/04 Prefabs/Items/TheTuong): dải màu hệ, băng keo, sticker (bóng sẫm nếu chưa có), tên,
// nhãn hệ, huy hiệu hệ, độ hiếm, sao hoặc thanh mảnh, nhãn "TRONG ĐỘI", chấm đỏ khi có thẻ nâng được hoặc tiến hóa được.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HeroTile : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image card, band, alert;
            public ClickCatcher click;
            public HeroPortrait portrait;
            public TextMeshProUGUI name, rarity, teamText;
            public UiElemTag elemTag;
            public BadgeIcon badge;
            public UiStars stars;
            public UiBar shards;
            public GameObject team;
        }

        [SerializeField] Parts p;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        // index: vị trí trong lưới (độ nghiêng của thẻ)
        public void Bind(HeroDef hero, SaveData s, GameData d, int index, Action onClick)
        {
            var hp = s.Hero(hero.id);
            bool owned = hp.owned;
            name = "o_" + hero.id;
            p.card.name = "the_" + hero.id;
            p.card.color = owned ? Theme.CardFill : Theme.Hex("#efe6d2");
            p.card.rectTransform.localEulerAngles = new Vector3(0, 0, ((index * 37) % 5) - 2);
            p.click.OnClick = onClick;
            var ec = Theme.Of(hero.elem);
            p.band.color = new Color(ec.r, ec.g, ec.b, 0.35f);
            p.portrait.Bind(hero, 224, !owned);
            p.name.text = hero.name;
            p.elemTag.Set(hero.elem);

            int badge = Badges.Tier(s, hero.elem);
            p.badge.gameObject.SetActive(badge > 0);
            if (badge > 0) p.badge.Bind(hero.elem, badge, 48);

            p.rarity.text = Elements.RarityName(hero.rarity);
            p.rarity.color = Theme.Of(hero.rarity);

            p.stars.gameObject.SetActive(owned);
            if (owned) p.stars.Set(hp.star, d.Cfg.maxStar);
            p.shards.gameObject.SetActive(!owned);
            if (!owned) p.shards.Set(hp.shards, hero.shards, 0, $"{hp.shards}/{hero.shards} mảnh", true);

            p.alert.gameObject.SetActive(owned && Progress.HeroAlerts(s, d, hero.id) > 0);
            bool inTeam = owned && s.team.Contains(hero.id);
            p.team.SetActive(inTeam);
            if (inTeam) p.teamText.text = $"TRONG ĐỘI {s.team.IndexOf(hero.id) + 1}";
        }
    }
}
