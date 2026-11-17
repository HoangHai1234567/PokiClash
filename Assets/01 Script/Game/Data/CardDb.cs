// Thẻ chung (75 từ 2026-11-17), thẻ riêng của tướng và thẻ của lính, dựng từ Assets/02 Data/Json/cards.json. Cây hiệu ứng giữ dạng JSON trong effectsJson.
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
        public List<CardDef> traits = new List<CardDef>(); // bị động boss của ải
    }
}
