// Một dòng mảnh tướng trong hộp mở rương: chân dung và chữ; prefab Items/ThuongManh.
using PokiClash.Core;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class RewardShardRow : MonoBehaviour
    {
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI text;

        // Dùng khi nướng prefab (Editor).
        public void Setup(HeroPortrait por, TextMeshProUGUI label)
        {
            portrait = por;
            text = label;
        }

        public void Bind(HeroDef h, string label)
        {
            portrait.Bind(h, 160);
            text.text = label;
        }
    }
}
