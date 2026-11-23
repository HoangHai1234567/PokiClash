// Hộp "Cách chơi" (Sổ tay, GD_Claude/25_FTUE.md mục 6): luật ngắn từng phần, mỗi trang mở khi người chơi đã học tới phần đó
// (Core/Tutorial.Pages), trang chưa mở hiện "???". Prefab Assets/04 Prefabs/Dialogs/CachChoi (biến thể tờ giấy gốc HopThoai), dựng
// bằng menu "PokiClash/Prefab/Khác/Hộp thoại và màn∕Hướng dẫn: hộp Cách chơi, dòng Sổ tay".
using System.Text;
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HowToDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI body;
        [SerializeField] ScrollRect scroll;
        [SerializeField] PokiClash.UI.SketchButton story; // "Xem lại cốt truyện" (App/StoryIntro, vẽ trên hộp thoại)

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextMeshProUGUI text, ScrollRect sc, PokiClash.UI.SketchButton storyButton)
        {
            body = text;
            scroll = sc;
            story = storyButton;
        }

        public static void Open() => App.Modals.Open<HowToDialog>().Show();

        public void Show()
        {
            if (story)
            {
                story.gameObject.SetActive(App.I && App.I.storyPrefab);
                story.SetOnClick(() => StoryIntro.Replay());
            }
            var s = App.Save.Data;
            var sb = new StringBuilder();
            int open = 0, all = 0;
            foreach (var p in Tutorial.Pages())
            {
                all++;
                if (Tutorial.PageOpen(s, p))
                {
                    open++;
                    sb.Append("<b>").Append(p.title).Append("</b>\n").Append(p.text).Append("\n\n");
                }
                else sb.Append("<b>???</b>\n<i>").Append(Loc.T("Mở khi bạn chơi tới phần này.")).Append("</i>\n\n");
            }
            sb.Append("<size=80%><i>").Append(Loc.F("Đã mở {0}/{1} trang.", open, all)).Append("</i></size>");
            body.text = sb.ToString();
            if (scroll)
            {
                Canvas.ForceUpdateCanvases();
                scroll.verticalNormalizedPosition = 1;
            }
        }
    }
}
