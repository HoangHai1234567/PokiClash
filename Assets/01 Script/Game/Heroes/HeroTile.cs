// Một ô trong lưới Tướng (prefab Assets/04 Prefabs/Items/TheTuong): dải màu hệ, băng keo, sticker (bóng sẫm nếu chưa có), tên,
// nhãn hệ, huy hiệu hệ, độ hiếm, sao hoặc thanh mảnh, nhãn "TRONG ĐỘI" (thẻ tô vàng), chấm đỏ khi có thẻ nâng được hoặc tiến hóa được.
// Tướng đã có: lực chiến (icon kiếm + số gọn 57.6k) cạnh hàng sao bậc (Đồng, Bạc, Vàng, Kim Cương) ở đáy thẻ (menu "PokiClash/Prefab/Popup
// gọn (ô thưởng, đội hình, lực chiến)" thêm).
// Độ hiếm (người dùng dặn 2026-11-17, menu "PokiClash/Prefab/Màn Tướng: độ hiếm, lọc và xếp" thêm): thẻ là khung ngoài tô màu độ hiếm,
// giấy lót "giay" lùi vào Theme.RarityInset px mang màu trạng thái (kem, vàng khi trong đội, xám khi chưa có); nhãn độ hiếm là viên màu
// chữ trắng; Sử thi, Huyền thoại khung gạch sáp; Huyền thoại khung dày nhất, vương miện thay băng keo. Prefab chưa chạy menu thì như cũ.
using System;
using System.Linq;
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
            public TextMeshProUGUI name, rarity, teamText, power;
            public UiElemTag elemTag;
            public BadgeIcon badge;
            public UiStars stars;
            public UiBar shards;
            public GameObject team;
            // độ hiếm (menu Màn Tướng: độ hiếm, lọc và xếp)
            public Image paper, rarityPill;
            public GameObject crown, tape;
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
            // đội thật: tướng đã có trong danh sách đội, chỉ tới số ô đã mở (như khung đội hình, hộp chuẩn bị trận)
            int order = s.team.Where(h => s.Hero(h)?.owned == true).Take(Progress.TeamSlots(s)).ToList().IndexOf(hero.id);
            bool inTeam = owned && order >= 0;
            var fill = inTeam ? Theme.Hex("#ffefb0") : owned ? Theme.CardFill : Theme.Hex("#efe6d2");
            PaintRarity(hero.rarity, owned, fill);
            p.card.rectTransform.localEulerAngles = new Vector3(0, 0, ((index * 37) % 5) - 2);
            p.click.OnClick = () =>
            {
                PokiClash.UI.UiMotion.Of(this).Punch(0.8f); // bộ UI Sa Bàn: chạm ô tướng thì nảy
                onClick?.Invoke();
            };
            var ec = Theme.Of(hero.elem);
            p.band.color = new Color(ec.r, ec.g, ec.b, 0.35f);
            p.portrait.Bind(hero, 224, !owned);
            p.name.text = hero.name;
            p.elemTag.Set(hero.elem);

            int badge = Badges.Tier(s, hero.elem);
            p.badge.gameObject.SetActive(badge > 0);
            if (badge > 0) p.badge.Bind(hero.elem, badge, 48);

            p.stars.gameObject.SetActive(owned);
            if (owned) p.stars.SetTiered(App.Data.Cfg, hero, hp.star); // bậc theo dạng của tướng (2026-11-19)
            p.shards.gameObject.SetActive(!owned);
            if (!owned) p.shards.Set(hp.shards, hero.shards, 0, $"{hp.shards}/{hero.shards} mảnh", true);

            if (p.power)
            {
                p.power.transform.parent.gameObject.SetActive(owned);
                if (owned) p.power.text = NumFmt.Short(HeroStats.Power(d.Cfg, hero, Teams.MemberOf(s, hero.id, d)));
            }

            p.alert.gameObject.SetActive(owned && Progress.HeroAlerts(s, d, hero.id) > 0);
            p.team.SetActive(inTeam);
            if (inTeam) p.teamText.text = $"TRONG ĐỘI {order + 1}";
        }

        // khung, nhãn, vương miện theo độ hiếm; fill: màu giấy theo trạng thái (kem, vàng trong đội, xám chưa có)
        void PaintRarity(Rarity r, bool owned, Color fill)
        {
            var rc = owned ? Theme.Of(r) : Theme.RarityMuted(r);
            if (p.paper)
            {
                p.card.color = rc;
                var frame = Theme.RarityHatch(r) ? Sketch.CardFrame : Sketch.Panel;
                if (frame) Theme.SetSprite(p.card, frame);
                p.paper.color = fill;
                float w = Theme.RarityInset(r, 1, 7);
                var pr = p.paper.rectTransform;
                pr.offsetMin = new Vector2(w, w);
                pr.offsetMax = new Vector2(-w, -w);
            }
            else p.card.color = fill;

            if (p.rarityPill)
            {
                p.rarityPill.color = rc;
                p.rarity.text = Theme.RarityLabel(r);
                p.rarity.color = Color.white;
            }
            else
            {
                p.rarity.text = Elements.RarityName(r);
                p.rarity.color = Theme.RarityInk(r);
            }

            bool legend = r == Rarity.Legend;
            if (p.crown) p.crown.SetActive(legend);
            if (p.tape) p.tape.SetActive(!legend || !p.crown);
        }
    }
}
