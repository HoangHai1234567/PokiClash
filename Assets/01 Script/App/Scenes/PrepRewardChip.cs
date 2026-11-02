// Một ô thưởng trong hộp Chuẩn bị trận (prefab Assets/04 Prefabs/Items/ThuongTran): khung giấy màu, biểu tượng hoặc chân dung tướng, chữ.
// Dùng cho bi, mảnh tướng, tướng tặng, huy hiệu, rương, đá tiềm năng.
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class PrepRewardChip : MonoBehaviour
    {
        [SerializeField] Image bg, icon;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI text;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image bgImg, HeroPortrait por, Image iconImg, TextMeshProUGUI label)
        {
            bg = bgImg;
            portrait = por;
            icon = iconImg;
            text = label;
        }

        // hero khác null: chân dung thay biểu tượng
        public void Bind(Sprite iconSprite, HeroDef hero, string label, Color fill)
        {
            bg.color = fill;
            portrait.gameObject.SetActive(hero != null);
            icon.gameObject.SetActive(hero == null);
            if (hero != null) portrait.Bind(hero, 58);
            else icon.sprite = iconSprite;
            text.text = label;
        }
    }
}
