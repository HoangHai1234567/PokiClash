// 5 đảo hệ (toạ độ vùng trên đảo lớn, toạ độ 8 ải theo ảnh) và 40 ải, dựng từ zones.json và stages.json.
// Thay ảnh đảo thì chỉ sửa toạ độ ở bản web (stages.ts) rồi xuất lại.
using System.Collections.Generic;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash.Game
{
    [CreateAssetMenu(menuName = "PokiClash/ZoneDb", fileName = "ZoneDb")]
    public sealed class ZoneDb : ScriptableObject
    {
        public List<ZoneDef> zones = new List<ZoneDef>();
        public List<StageDef> stages = new List<StageDef>();
        public Pt village;
    }
}
