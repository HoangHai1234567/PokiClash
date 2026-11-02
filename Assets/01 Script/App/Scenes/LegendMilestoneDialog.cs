// Hộp "Huyền thoại!" của Máy bi (vừa thả đủ mốc bi, nhận tướng Huyền thoại đầu tiên): con dấu cam, chân dung, tên tướng, câu giải thích,
// nút "Tuyệt!". Prefab Assets/04 Prefabs/Dialogs/HuyenThoai.
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class LegendMilestoneDialog : Dialog
    {
        [SerializeField] HeroPortrait portrait;
        [SerializeField] TextMeshProUGUI heroName, line;
        [SerializeField] SketchButton ok;

        // Dùng khi nướng prefab (Editor).
        public void Setup(HeroPortrait por, TextMeshProUGUI nameText, TextMeshProUGUI lineText, SketchButton okButton)
        {
            portrait = por;
            heroName = nameText;
            line = lineText;
            ok = okButton;
        }

        void Awake() => ok.SetOnClick(Close);

        public static string Line(int milestone) => $"Thả đủ {milestone} bi: chắc chắn nhận tướng Huyền thoại đầu tiên.";

        public void Show(HeroDef h, int milestone)
        {
            portrait.Bind(h, 400);
            heroName.text = h.name;
            line.text = Line(milestone);
        }
    }
}
