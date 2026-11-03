// 45 tướng và 6 lính của ải, dựng từ Assets/02 Data/Json/heroes.json bằng menu "PokiClash/Nhập dữ liệu". Không sửa tay.
using System.Collections.Generic;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash.Game
{
    [CreateAssetMenu(menuName = "PokiClash/HeroDb", fileName = "HeroDb")]
    public sealed class HeroDb : ScriptableObject
    {
        public List<HeroDef> heroes = new List<HeroDef>();
        public List<HeroDef> minions = new List<HeroDef>(); // lính: chỉ làm địch trong ải, không thu phục
        public List<string> starters = new List<string>();
        public string legendMilestoneHero;
    }
}
