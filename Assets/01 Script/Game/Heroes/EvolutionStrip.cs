// Thanh mốc tiến hóa dưới ô xem tướng trong hộp chi tiết (prefab Dialogs/ChiTietTuong, dựng bằng menu
// "PokiClash/Prefab/Thêm thanh tiến hóa vào ChiTietTuong"): mỗi dạng của dòng tiến hóa là một mốc, chia đều trên thanh (mốc đầu ở
// đầu thanh, mốc cuối ở cuối thanh, người dùng chốt 2026-11-02); dưới mốc ghi sao bắt đầu dạng đó (sao 1, BalanceConfig.formStars).
// Thanh là tiến độ tới dạng cuối: giữa hai mốc thì đầy dần theo sao, đủ sao của dạng cuối là đầy. Mốc có chân dung dạng đó, số sao
// và tên dạng; dạng chưa tới (hoặc tướng chưa có) là bóng sẫm. Dòng 1 dạng: một mốc, thanh đầy khi đã có tướng, và dòng ghi chú.
// Mọi phần có sẵn trong prefab, Bind chỉ bật tắt và gán.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class EvolutionStrip : MonoBehaviour
    {
        [Serializable]
        public struct Node
        {
            public RectTransform root; // con của rail: neo ngang theo thứ tự mốc trên thanh
            public HeroPortrait portrait;
            public UiStars stars;
            public TextMeshProUGUI name;
        }

        [SerializeField] UiBar bar;
        [SerializeField] RectTransform rail; // cùng bề ngang với thanh, chứa các mốc
        [SerializeField] Node[] nodes = new Node[0];
        [SerializeField] TextMeshProUGUI note; // dòng 1 dạng
        [SerializeField] float portraitHeight = 140;

        // Dùng khi dựng prefab (Editor).
        public void Setup(UiBar barView, RectTransform railRt, Node[] nodeViews, TextMeshProUGUI noteText)
        {
            bar = barView;
            rail = railRt;
            nodes = nodeViews;
            note = noteText;
        }

        // Sao bắt đầu của dạng i (0 là dạng 1).
        public static int StartStar(int[] formStars, int i) => i == 0 ? 1 : formStars[i - 1];

        // Tiến độ tới dạng cuối (0..1) ở sao này: mốc i nằm ở i / (count - 1), giữa hai mốc thì chia theo sao.
        public static float Fill(int[] formStars, int count, int star)
        {
            if (count <= 1) return 1;
            for (int i = 0; i < count - 1; i++)
            {
                int a = StartStar(formStars, i), b = StartStar(formStars, i + 1);
                if (star < b) return (i + Mathf.Clamp01((star - a) / (float)Mathf.Max(1, b - a))) / (count - 1);
            }
            return 1;
        }

        public void Bind(HeroDef hero, int star, bool owned, BalanceConfig cfg)
        {
            int count = Mathf.Max(1, Mathf.Min(hero.forms.Length, Mathf.Min(cfg.formStars.Length + 1, nodes.Length)));
            int cur = owned ? hero.FormIndex(cfg.formStars, star) : -1;
            bar.Set(owned ? Fill(cfg.formStars, count, star) * 100 : 0, 100, 0, "", true);
            for (int i = 0; i < nodes.Length; i++)
            {
                var n = nodes[i];
                n.root.gameObject.SetActive(i < count);
                if (i >= count) continue;
                int from = StartStar(cfg.formStars, i);
                float x = count == 1 ? 0 : i / (count - 1f);
                n.root.anchorMin = new Vector2(x, n.root.anchorMin.y);
                n.root.anchorMax = new Vector2(x, n.root.anchorMax.y);
                bool reached = owned && star >= from;
                n.portrait.Bind(hero, portraitHeight, !reached, from);
                n.stars.Set(reached ? from : 0, from);
                n.name.text = hero.forms.Length > 0 ? hero.forms[i].name : hero.name;
                n.name.fontStyle = i == cur ? FontStyles.Bold : FontStyles.Normal;
                n.name.color = i == cur ? Theme.Ink : Theme.Ink3;
            }
            note.gameObject.SetActive(count == 1);
            if (count == 1) note.text = "Dòng 1 dạng: lên sao không đổi hình";
        }
    }
}
