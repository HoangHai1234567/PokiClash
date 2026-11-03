// 23 thẻ chung, 136 thẻ riêng và 18 thẻ của lính, dựng từ Assets/02 Data/Json/cards.json. Cây hiệu ứng giữ dạng JSON trong effectsJson.
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
        public List<CardDef> minions = new List<CardDef>(); // thẻ của lính
    }
}
