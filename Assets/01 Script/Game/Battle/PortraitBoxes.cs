// Hộp phần có hình (alpha) của từng chân dung aola, 0..1 theo khung ảnh, gốc dưới trái: hình to nhỏ trong khung khác nhau (lính nhỏ,
// boss to), màn VS và dải tuyệt kỹ cần biết đầu nằm đâu để phóng (HeroArt.FitHead). Đo sẵn trong Editor bằng menu
// "PokiClash/Prefab/Trận: màn VS truyện tranh" (ảnh chân dung không đọc được lúc chạy), lưu ở Resources/BattleIntro/khung_chan_dung;
// nhập thêm tướng thì chạy lại menu. Chưa đo thì cả khung.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed class PortraitBoxes : ScriptableObject
    {
        public const string Res = "BattleIntro/khung_chan_dung";

        [Serializable]
        public struct Entry
        {
            public string aola;
            public Rect box;
        }

        public List<Entry> entries = new List<Entry>();

        static Dictionary<string, Rect> map;

        public static Rect Of(string aola)
        {
            if (map == null)
            {
                map = new Dictionary<string, Rect>();
                var asset = Resources.Load<PortraitBoxes>(Res);
                if (asset)
                    foreach (var e in asset.entries) map[e.aola] = e.box;
            }
            return !string.IsNullOrEmpty(aola) && map.TryGetValue(aola, out var r) ? r : new Rect(0, 0, 1, 1);
        }
    }
}
