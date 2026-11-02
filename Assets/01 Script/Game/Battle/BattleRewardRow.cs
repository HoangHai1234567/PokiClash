// Một dòng thưởng trong hộp kết quả trận (prefab Assets/04 Prefabs/Items/TranThuong): icon (bi, đá) hoặc chân dung tướng
// (mảnh, mở khoá), dòng chính, dòng phụ (tuỳ chọn), nền theo loại thưởng.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BattleRewardRow : MonoBehaviour
    {
        [SerializeField] Image bg, icon;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI title, sub;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bgImg, Image iconImg, HeroPortrait por, TextMeshProUGUI titleText, TextMeshProUGUI subText)
        {
            bg = bgImg;
            icon = iconImg;
            portrait = por;
            title = titleText;
            sub = subText;
        }

        // hero khác null: chân dung thay icon; subText null: không có dòng phụ
        public void Bind(Sprite iconSprite, HeroDef hero, string titleText, string subText, Color fill)
        {
            name = "thuong";
            bg.color = fill;
            portrait.gameObject.SetActive(hero != null);
            if (hero != null) portrait.Bind(hero, 90);
            icon.gameObject.SetActive(hero == null);
            icon.sprite = iconSprite;
            title.text = titleText;
            title.rectTransform.Stretch(130, 8, 20, subText != null ? 46 : 12);
            sub.gameObject.SetActive(subText != null);
            sub.text = subText ?? "";
        }
    }
}
