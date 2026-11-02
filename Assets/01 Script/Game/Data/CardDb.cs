// 23 thẻ chung và 33 thẻ riêng, dựng từ Assets/02 Data/Json/cards.json. Cây hiệu ứng giữ dạng JSON trong effectsJson.
using System.Collections.Generic;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash.Game
{
    [CreateAssetMenu(menuName = "PokiClash/CardDb", fileName = "CardDb")]
    public sealed class CardDb : ScriptableObject
    {
        public List<CardDef> pool = new List<CardDef>();
        public List<CardDef> innate = new List<CardDef>();
    }
}
