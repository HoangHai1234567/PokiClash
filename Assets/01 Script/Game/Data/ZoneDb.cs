// 5 đảo hệ (toạ độ vùng trên đảo lớn, toạ độ ải theo ảnh; đảo có bản đồ dài thêm đường, chỗ ải tướng, bên bảng tên) và các ải,
// dựng từ zones.json và stages.json bằng menu "PokiClash/Nhập dữ liệu". Bản đồ dài đảo Thủy: ArtGen/Islands/build_zone70.py --xuat
// ghi toạ độ vào zones.json.
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
