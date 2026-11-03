// Ô thưởng dùng chung (prefab Assets/04 Prefabs/Items/OThuong, dựng bằng menu "PokiClash/Prefab/Popup gọn (ô thưởng, đội hình, lực chiến)"):
// khung giấy tô màu độ hiếm, dải độ hiếm trên đầu (tên độ hiếm viết hoa), hình to ở giữa (icon, chân dung tướng hoặc hình thẻ),
// tướng chủ thẻ thu nhỏ góc dưới trái, biểu tượng nhỏ góc trên phải (mảnh), số lượng "×n" góc dưới phải, nhãn góc trên trái
// (tỉ lệ rơi, "Lần đầu", "MỚI!"), một dòng tên dưới khung. Ít chữ: cái gì, bao nhiêu, độ hiếm nhìn hình và màu là ra.
// Dùng ở hộp Chuẩn bị trận, mở rương, rương mốc đảo, kết quả trận.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class RewardTile : MonoBehaviour
    {
        // cỡ ô (khung vuông và dòng tên dưới)
        public const float W = 150, Frame = 150, H = 190;

        [System.Serializable]
        public struct Parts
        {
            public Image frame, band, icon, corner, tagBg;
            public HeroPortrait hero, owner;
            public TextMeshProUGUI bandText, count, tag, caption;
        }

        [SerializeField] Parts p;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // bi, XP, đá, rương, huy hiệu: icon, số lượng, tên; rarity null thì khung giấy trơn
        public RewardTile Item(Sprite icon, string count, string caption, Rarity? rarity = null, Color? tint = null)
        {
            Base(rarity, count, caption);
            p.icon.gameObject.SetActive(true);
            Theme.SetSprite(p.icon, icon);
            p.icon.color = tint ?? Color.white;
            return this;
        }

        // mảnh tướng / tướng mới: chân dung theo độ hiếm của tướng, góc trên phải là icon mảnh (shards) hoặc vương miện (tướng mới)
        public RewardTile Hero(HeroDef h, string count, bool shards = true)
        {
            Base(h.rarity, count, h.name);
            p.hero.gameObject.SetActive(true);
            p.hero.Bind(h, Frame * 0.92f);
            p.corner.gameObject.SetActive(true);
            Theme.SetSprite(p.corner, Icon(shards ? "shard" : "crown"));
            return this;
        }

        // bản sao thẻ riêng: hình thẻ trên nền màu độ hiếm, tướng chủ góc dưới trái
        public RewardTile Card(CardDef cd, Sprite icon, HeroDef owner, int n, Rarity rarity)
        {
            Base(rarity, "×" + n, cd.name);
            p.icon.gameObject.SetActive(true);
            Theme.SetSprite(p.icon, icon != null ? icon : Sketch.InkDot);
            p.icon.color = Color.white;
            if (owner == null) return this;
            p.owner.gameObject.SetActive(true);
            p.owner.Bind(owner, Frame * 0.6f);
            return this;
        }

        // nhãn góc trên trái (tỉ lệ rơi, "Lần đầu", "MỚI!")
        public RewardTile Tag(string text, Color fill)
        {
            bool on = !string.IsNullOrEmpty(text);
            p.tagBg.gameObject.SetActive(on);
            if (!on) return this;
            p.tag.text = text; // viên nhãn tự co theo chữ (HorizontalLayoutGroup + ContentSizeFitter trong prefab)
            p.tag.color = fill.grayscale > 0.62f ? Theme.Ink : Color.white;
            p.tagBg.color = fill;
            return this;
        }

        void Base(Rarity? rarity, string count, string caption)
        {
            var rc = rarity.HasValue ? Theme.Of(rarity.Value) : Theme.Paper3;
            p.frame.color = rarity.HasValue ? Color.Lerp(Theme.CardFill, rc, 0.28f) : Theme.CardFill;
            p.band.gameObject.SetActive(rarity.HasValue);
            p.band.color = rc;
            if (rarity.HasValue) p.bandText.text = Elements.RarityName(rarity.Value).ToUpperInvariant();
            p.icon.gameObject.SetActive(false);
            p.hero.gameObject.SetActive(false);
            p.owner.gameObject.SetActive(false);
            p.corner.gameObject.SetActive(false);
            p.tagBg.gameObject.SetActive(false);
            p.count.gameObject.SetActive(!string.IsNullOrEmpty(count));
            p.count.text = count;
            p.caption.text = caption;
            name = "o_thuong_" + caption;
        }
    }
}
