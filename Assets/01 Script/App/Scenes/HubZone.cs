// Một vùng đảo trên sảnh (prefab mục Items/BangVung; năm bản sao đặt sẵn theo toạ độ ảnh trong Screens/Hub): vùng chạm tròn,
// bảng tên (icon hệ, tên, nhãn độ khó, cấp đề nghị và tiến độ, thanh tiến độ), mũi tên nhún khi là đảo nên đánh.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HubZone : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Elem zone;
            public Image hit, plaque, icon;
            public ClickCatcher hitClick, plaqueClick;
            public TextMeshProUGUI name, level;
            public DifficultyTag difficulty;
            public ZoneProgressBar bar;
            public GameObject arrow;
        }

        [SerializeField] Parts p;

        public Elem Zone => p.zone;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        // Dùng khi nướng prefab (Editor): icon hệ của vùng (cố định theo vùng).
        public void SetIcon(Sprite s) => p.icon.sprite = s;

        // prog: số ải đã qua (0..8); recommended: đảo nên đánh (hiện mũi tên). Dùng cả lúc nướng với dữ liệu mẫu.
        public void Bind(ZoneDef z, int prog, Progress.Difficulty df, bool recommended)
        {
            p.zone = z.id;
            string key = Keys.Of(z.id);
            name = "o_vung_" + key;
            p.hit.name = "vung_" + key;
            p.plaque.name = "bang_" + key;
            p.plaque.rectTransform.localEulerAngles = new Vector3(0, 0, (z.order % 2 == 1 ? -1 : 1) * 1.5f);
            p.name.text = z.name;
            p.difficulty.Set(df);
            p.level.text = $"Cấp {z.levelMin}–{z.levelMax} · {prog}/8 ải";
            p.bar.Set(Theme.Of(z.id), prog / 8f);
            p.arrow.SetActive(recommended);
        }

        public void SetOnClick(Action open)
        {
            p.hitClick.OnClick = open;
            p.plaqueClick.OnClick = open;
        }
    }
}
